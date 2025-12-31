# Hyper

A lightweight, self-hosted relay for interacting with multiple Large Language Models (LLMs) through a unified chat interface.

This project provides a simple web UI to select and chat with different models, currently supporting Google Gemini out-of-the-box with placeholders for others.

## Key Features

*   **Unified Chat Interface:** Talk to different LLMs from a single UI.
*   **Model Selection:** Choose your preferred model and version.
*   **Markdown Rendering:** Displays formatted responses from the models.
*   **Simple to Run:** Includes a one-click startup script for Windows.

## Getting Started

### 1. Prerequisites

*   You need [Python 3.9+](https://www.python.org/downloads/) installed.

### 2. Setup

First, get the code and install the necessary Python packages.

```bash
# Clone the repository (or download the ZIP)
git clone https://github.com/<your-username>/hyper.git
cd hyper

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure API Keys

Create a file named `.env` in the project's main directory. Add your Google Gemini API key to it:

```env
GEMINI_KEY=<Your Google Gemini API Key>
```

## Running the Application

On Windows, simply double-click the `run.bat` file.

This will start the server and open the application in your browser at `http://127.0.0.1:8000`.
