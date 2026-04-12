# Lead-Gen Automator

An end-to-end AI lead generation assistant that:

1. Finds potential businesses by niche and location.
2. Researches each business website.
3. Summarizes fit for your service.
4. Drafts personalized outreach messages.
5. Stores leads in a vector store for semantic retrieval.

## Tech Stack

- Backend: FastAPI + LangChain + Chroma
- Frontend: Streamlit
- LLM: OpenAI (`gpt-4o-mini` by default)
- Search provider: Tavily API
- Scraping: Requests + BeautifulSoup

## Project Structure

```text
Lead_gen_automator/
  backend/
    app/
      core/
      schemas/
      services/
      main.py
  frontend/
    app.py
  .env.example
  requirements.txt
```

## Quick Start

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy environment file and fill keys:

```bash
cp .env.example .env
```

Required keys:
- `OPENAI_API_KEY`
- `TAVILY_API_KEY`

4. Run FastAPI backend:

```bash
uvicorn backend.app.main:app --reload --port 8000
```

5. Run Streamlit frontend:

```bash
streamlit run frontend/app.py
```

## API Endpoints

- `GET /health`
- `POST /api/leads/generate`
- `POST /api/leads/search-memory`

## Notes

- This is an MVP architecture for agentic lead generation.
- Scraping quality depends on site structure and anti-bot policies.
- For production, add retries, rate limiting, job queues, and auth.
# Lead-Gen-Automator
# Lead-Gen-Automator
# Lead-Gen-Automator
