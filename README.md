# Lead-Gen Automator 🤖

An end-to-end AI lead generation platform that automatically discovers, researches, analyzes, and drafts personalized B2B outreach for target businesses.

🔗 **Live Demo (Streamlit Cloud)**: https://generate-your-leads.streamlit.app/

## Key Features

1. **Targeted Search**: Discovers businesses by niche and location using Tavily Search API.
2. **Deep Scraping & Intel**: Scrapes business websites to extract contact info, emails, and site copy.
3. **AI Intel & Outreach**: Summarizes business fit, extracts pain points, and drafts custom outreach messages using Google Gemini / OpenAI LLMs.
4. **Vector Store Memory**: Persists lead insights into ChromaDB vector database for semantic memory retrieval.
5. **Containerized Architecture**: Fully Dockerized backend & frontend microservices managed via Docker Compose.
6. **Automated CI/CD**: Integrated GitHub Actions workflow for linting, container builds, and deployment verification.

---

## Tech Stack

- **Backend**: FastAPI, LangChain, ChromaDB Vector Store, Pydantic
- **Frontend**: Streamlit
- **AI Models**: Google Gemini (`gemini-2.0-flash`) / OpenAI (`gpt-4o-mini`)
- **Search Provider**: Tavily Search API
- **DevOps & Infrastructure**: Docker, Docker Compose, GitHub Actions CI/CD, Render.com

---

## Project Structure

```text
Lead_gen_automator/
├── backend/
│   └── app/
│       ├── core/          # App configuration & settings
│       ├── schemas/       # Pydantic data models
│       ├── services/      # AI agent logic, web tools, & vector memory
│       └── main.py        # FastAPI endpoints & CORS
├── frontend/
│   └── app.py             # Streamlit user interface
├── .github/
│   └── workflows/
│       └── ci-cd.yml      # GitHub Actions CI/CD pipeline
├── Dockerfile.backend     # Backend Docker image specification
├── Dockerfile.frontend    # Frontend Docker image specification
├── docker-compose.yml     # Orchestration for local development
├── .dockerignore
├── .env.example
└── requirements.txt
```

---

## 🐳 Quick Start with Docker (Recommended)

The easiest way to run the entire application is using Docker Compose:

1. **Clone the repository & copy environment configuration:**
   ```bash
   cp .env.example .env
   ```
2. **Fill in your API keys in `.env`:**
   ```env
   GEMINI_API_KEY=your_gemini_api_key
   TAVILY_API_KEY=your_tavily_api_key
   ```
3. **Launch all services using Docker Compose:**
   ```bash
   docker compose up --build
   ```
4. Access the applications:
   - **Frontend UI**: `http://localhost:8501`
   - **FastAPI Backend**: `http://localhost:8000`
   - **API Docs (Swagger)**: `http://localhost:8000/docs`

---

## 💻 Manual Local Setup (Without Docker)

1. **Create and activate a Python 3.12 environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Backend (Terminal 1):**
   ```bash
   python3 -m uvicorn backend.app.main:app --reload --port 8000
   ```

4. **Run Frontend (Terminal 2):**
   ```bash
   python3 -m streamlit run frontend/app.py
   ```

---

## 🔄 CI/CD Pipeline (GitHub Actions)

This repository includes an automated continuous integration and continuous deployment workflow (`.github/workflows/ci-cd.yml`).

- **Linting & Code Quality**: Validates code syntax on every `push` and `pull_request`.
- **Automated Docker Builds**: Builds backend and frontend Docker containers using Docker Buildx to ensure production container readiness.
- **Continuous Deployment (CD)**: Automatically triggers production deployment webhooks upon merging into `main`.

---

## ☁️ Cloud Deployment Setup

### 1. Backend (FastAPI on Render)
- Connect this GitHub repository to **Render.com**.
- Select **Web Service** and choose **Docker** as runtime.
- Set environment variables (`GEMINI_API_KEY`, `TAVILY_API_KEY`) in Render Settings.

### 2. Frontend (Streamlit Community Cloud)
- Deploy `frontend/app.py` on **Streamlit Cloud**.
- In Streamlit App Settings $\rightarrow$ Secrets, configure:
  ```toml
  BACKEND_URL = "https://your-backend-service.onrender.com"
  ```

---

## API Endpoints

- `GET  /health` - Health check status endpoint
- `POST /api/leads/generate` - Trigger AI lead search, scraping, summarization & memory storage
- `POST /api/leads/search-memory` - Semantic search stored leads in ChromaDB vector database
