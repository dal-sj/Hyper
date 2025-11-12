import os
from pathlib import Path
from dotenv import load_dotenv

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel, Field
from typing import List, Dict

# Google Gemini SDK
from google import genai
from google.genai import types as gemini_types
from google.genai.types import GenerationConfig
from google.genai import errors as genai_errors

# OpenAI SDK
# import openai

# Anthropic SDK
# from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

# Load environment variables
load_dotenv()

# Paths
BASE_DIR = Path(__file__).resolve().parent

# FastAPI app
app = FastAPI()
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# --- 클라이언트 초기화 및 모델 메타데이터 동적 로딩 ---

OPENAI_KEY = os.getenv("OPENAI_KEY", "")

CLAUDE_KEY = os.getenv("CLAUDE_KEY", "")

GEMINI_KEY = os.getenv("GEMINI_KEY", "")



# Gemini 클라이언트 및 모델 목록

gemini_client = None

gemini_models = [

    {"id": "gemini-1.5-flash-latest", "label": "Gemini 1.5 Flash", "desc": "최신 Flash"}

]

if GEMINI_KEY:
    try:
        gemini_client = genai.Client(api_key=GEMINI_KEY)
        
        fetched_models = []
        for m in gemini_client.models.list():
            if 'generateContent' in m.supported_actions:
                model_id = m.name.split('/')[-1]
                # 간단한 설명을 위해 모델 ID에서 일부 정보 추출
                desc = f"{m.display_name}"
                fetched_models.append({"id": model_id, "label": m.display_name, "desc": desc})
        
        if fetched_models:
            gemini_models = fetched_models
            
    except Exception as e:
        print(f"Gemini 모델 목록을 가져오는 데 실패했습니다: {e}")
        # 실패 시 기본 모델 목록 유지



# Model metadata -> 메인페이지에 뜨는 모델과 버전 관리

MODEL_METADATA = {

    "chatgpt": {

        "label": "ChatGPT",

        "description": "OpenAI의 GPT 기반 모델",

        "default": "gpt-4o",

        "versions": [

            {"id": "gpt-4o", "label": "GPT-4o", "desc": "멀티모달 지원, 최신"},

            {"id": "gpt-3.5-turbo", "label": "GPT-3.5 Turbo", "desc": "가볍고 빠름"}

        ]

    },

    "claude": {

        "label": "Claude",

        "description": "Anthropic의 고성능 언어 모델",

        "default": "claude-3",

        "versions": [

            {"id": "claude-3", "label": "Claude 3", "desc": "표준 버전"},

            {"id": "claude-2.1", "label": "Claude 2.1", "desc": "경량화 버전"}

        ]

    },

    "gemini": {

        "label": "Gemini",

        "description": "Google의 최신 대형 언어 모델",

        "default": gemini_models[0]["id"] if gemini_models else "",

        "versions": gemini_models

    }

}



# Index & chat page routes

@app.get("/", response_class=HTMLResponse)

async def index(request: Request):

    return templates.TemplateResponse("index.html", {"request": request, "models": MODEL_METADATA})



@app.get("/chat", response_class=HTMLResponse)

async def chat_page(request: Request, model: str, version: str = None):

    # 동적으로 로드된 모델 메타데이터 사용

    current_model_metadata = MODEL_METADATA

    

    meta = current_model_metadata.get(model)

    if not meta:

        raise HTTPException(404, "Unknown model")

    

    version = version or meta.get("default")

    if not version or version not in [v["id"] for v in meta["versions"]]:

        # 동적 로딩으로 인해 버전이 없을 경우를 대비

        if meta["versions"]:

            version = meta["versions"][0]["id"]

        else:

            raise HTTPException(400, "No versions available for this model")



    # 모델별 API_KEY 읽기

    key_env = {

        "chatgpt": "OPENAI_KEY",

        "claude":  "CLAUDE_KEY",

        "gemini":  "GEMINI_KEY"

    }[model]

    api_key = os.getenv(key_env, "")

    

    return templates.TemplateResponse(

        "chat.html",

        {

            "request": request, 

            "models": current_model_metadata, 

            "model": model, 

            "version": version, 

            "api_key": api_key

        },

    )



# OpenAI 클라이언트

if OPENAI_KEY:

    # openai.api_key = OPENAI_KEY

    pass



# Anthropic 클라이언트

# if CLAUDE_KEY:

    # anthropic_client = Anthropic(api_key=CLAUDE_KEY)

# else:

    # anthropic_client = None



# Request/Response schemas

class ChatRequest(BaseModel):

    model: str

    version: str

    history: List[Dict[str, str]] = Field(default_factory=list)

    message: str



class ChatResponse(BaseModel):

    response: str

    history: List[Dict[str, str]]



@app.post("/api/chat", response_model=ChatResponse)

async def chat(req: ChatRequest):

    # Validate model/version

    meta = MODEL_METADATA.get(req.model)

    if not meta or req.version not in [v["id"] for v in meta["versions"]]:

        raise HTTPException(400, "Invalid model or version")



    # 분기 처리: 모델별 API 호출

    # chatgpt, claude는 아마 gemini와 호출방식이 다를 것. 유의할 것. 높은 확률로 아래 갈아 엎어야 함.

    # 모델 gemini 선택택

    if req.model == "gemini":
        if not gemini_client:
            raise HTTPException(401, "Invalid API key for Gemini")
        
        # Prepare contents for the conversation
        contents = []
        for m in req.history:
            part = gemini_types.Part.from_text(text=m["content"])
            contents.append(
                gemini_types.UserContent(parts=[part]) if m["role"] == "user"
                else gemini_types.ModelContent(parts=[part])
            )
        # Add the current message
        user_part = gemini_types.Part.from_text(text=req.message)
        contents.append(gemini_types.UserContent(parts=[user_part]))

        # Call generate_content
        result = gemini_client.models.generate_content(
            model=f"models/{req.version}",
            contents=contents
        )
        reply = result.text



    # 모델 gpt 선택택

    elif req.model == "chatgpt":

        if not OPENAI_KEY:

            raise HTTPException(401, "Invalid API key for ChatGPT")

        # OpenAI ChatCompletion 호출

        messages = []

        for m in req.history:

            messages.append({"role": m["role"], "content": m["content"]})

        messages.append({"role": "user", "content": req.message})



        resp = openai.ChatCompletion.create(

            model=req.version,

            messages=messages

        )

        reply = resp.choices[0].message.content



    # 모델 claude 선택

    elif req.model == "claude":

        if not anthropic_client:

            raise HTTPException(401, "Invalid API key for Claude")

        # Anthropic Claude 호출

        # Anthropic SDK는 단순히 프롬프트를 합친 뒤 HUMAN_PROMPT/AI_PROMPT 토큰을 써서 요청

        prompt = ""

        for m in req.history:

            if m["role"] == "user":

                prompt += HUMAN_PROMPT + m["content"]

            else:

                prompt += AI_PROMPT + m["content"]

        prompt += HUMAN_PROMPT + req.message + AI_PROMPT



        resp = anthropic_client.completions.create(

            model=req.version,

            prompt=prompt,

            max_tokens=512,

            temperature=0.7,

        )

        reply = resp.completion



    else:

        # 절대 도달하지 않음

        raise HTTPException(400, "Unsupported model")



    # 3) 히스토리 업데이트

    new_history = req.history + [

        {"role": "user",      "content": req.message},

        {"role": "assistant", "content": reply},

    ]

    return ChatResponse(response=reply, history=new_history)
