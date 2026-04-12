from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.app.schemas.lead import GenerateLeadsRequest, GenerateLeadsResponse, MemorySearchRequest
from backend.app.services.lead_agent import LeadGenAgent

app = FastAPI(title="Lead-Gen Automator API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = LeadGenAgent()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/leads/generate", response_model=GenerateLeadsResponse)
def generate_leads(payload: GenerateLeadsRequest) -> GenerateLeadsResponse:
    try:
        leads = agent.run(
            niche=payload.niche,
            location=payload.location,
            client_service=payload.client_service,
            max_leads=payload.max_leads,
        )
    except ValueError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return GenerateLeadsResponse(leads=leads)


@app.post("/api/leads/search-memory")
def search_memory(payload: MemorySearchRequest) -> dict:
    try:
        results = agent.search_memory(query=payload.query, top_k=payload.top_k)
    except ValueError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return {"results": results}
