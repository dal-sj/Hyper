# Hyper

가벼운 LLM 중계 플랫폼입니다. 사용자는 ChatGPT, Claude, Google Gemini 모델 중 원하는 모델과 버전을 선택하여 대화를 나눌 수 있습니다. 프론트엔드(HTML/CSS/JavaScript)와 백엔드(FastAPI)로 구성되어 있습니다.

## 🚀 주요 기능

* 모델 및 버전 선택 (ChatGPT, Claude, Gemini)
* Markdown 지원 채팅 인터페이스
* 통합 `/api/chat` 엔드포인트로 모델별 API 호출 라우팅
* API 키 누락/유효하지 않을 때 에러 처리

## 📁 디렉터리 구조

```
Hyper
├── frontend
│   ├── index.html        # 메인 페이지: 모델·버전 선택 UI
│   ├── chat.html         # 채팅 페이지 템플릿 (Markdown 렌더링)
│   └── style.css         # 공통 및 페이지별 스타일
├── backend
│   ├── main.py           # FastAPI 앱 진입점
│   └── requirements.txt  # Python 의존성 목록
└── .env                  # 환경 변수 파일 (API 키)
```

## 🛠️ 사전 준비

* Python 3.9 이상
* `pip` (또는 `venv`) 설치
* (옵션) Node.js — 프론트엔드 독립 서버로 실행할 경우

## ⚙️ 설치 및 실행

1. **레포지토리 클론**

   ```bash
   git clone https://github.com/<your-username>/hyper.git
   cd hyper
   ```

2. **가상환경 생성 및 활성화**

   ```bash
   python -m venv venv
   # macOS/Linux
   source venv/bin/activate
   # Windows
   venv\Scripts\activate
   ```

3. **백엔드 의존성 설치**

   ```bash
   pip install -r backend/requirements.txt
   ```

4. **환경 변수 설정**

   `.env.example` 파일을 `.env`로 복사 후, 아래 키를 입력하세요:

   ```ini
   # .env
   OPENAI_KEY=<OpenAI API 키>
   CLAUDE_KEY=<Anthropic API 키>
   GEMINI_KEY=<Google Gemini API 키>
   ```

### 5. 애플리케이션 실행

#### 백엔드 (FastAPI)

프로젝트 루트에서:

```bash
cd backend
uvicorn main:app --reload
```

기본 포트 `8000`에서 서버가 시작됩니다 (`http://127.0.0.1:8000`).

#### 프론트엔드

FastAPI가 정적 파일을 서빙하므로 별도 서버 없이 브라우저에서 열면 됩니다:

```
http://127.0.0.1:8000/
```

원한다면 `frontend` 폴더를 다른 정적 서버로도 제공할 수 있습니다.

## 🔄 사용 방법

1. 메인 페이지 접속
2. 모델(ChatGPT, Claude, Gemini) 및 버전 선택
3. **시작하기** 클릭 → 채팅 페이지 진입
4. 메시지 입력 → 응답 확인 (Markdown 렌더링)

## ⚠️ 에러 처리

* API 키가 없거나 유효하지 않으면 백엔드에서 HTTP 401 에러 반환
* 프론트엔드 `status` 영역에 에러 메시지 표시

## 📝 커스터마이징

* **모델/버전**: `backend/main.py`의 `MODEL_METADATA` 수정
* **스타일**: `frontend/style.css` 편집

---

*즐거운 채팅 되세요!*
