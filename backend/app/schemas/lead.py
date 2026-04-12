from typing import List, Optional

from pydantic import BaseModel, Field


class Lead(BaseModel):
    company_name: str
    website: str
    contact_email: Optional[str] = None
    phone: Optional[str] = None
    summary: str
    pain_points: List[str] = Field(default_factory=list)
    outreach_message: str
    source_snippet: Optional[str] = None


class GenerateLeadsRequest(BaseModel):
    niche: str = Field(..., description="Example: IT services")
    location: str = Field(..., description="Example: Noida")
    client_service: str = Field(..., description="What your client provides")
    max_leads: int = Field(default=5, ge=1, le=20)


class GenerateLeadsResponse(BaseModel):
    leads: List[Lead]


class MemorySearchRequest(BaseModel):
    query: str
    top_k: int = Field(default=5, ge=1, le=20)
