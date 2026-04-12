from backend.app.schemas.lead import Lead
from backend.app.services.tools import scraper_tool, summarizer_tool, web_search_tool
from backend.app.services.vector_store import LeadMemoryStore


class LeadGenAgent:
    def __init__(self) -> None:
        self.memory = LeadMemoryStore()

    def run(self, niche: str, location: str, client_service: str, max_leads: int = 5) -> list[Lead]:
        search_results = web_search_tool(niche=niche, location=location, max_results=max_leads * 2)
        leads: list[Lead] = []
        seen_urls = set()

        for item in search_results:
            if len(leads) >= max_leads:
                break

            url = item.get("url", "")
            if not url or url in seen_urls:
                continue
            seen_urls.add(url)

            scraped = scraper_tool(url)
            company_name = item.get("title", "").split("|")[0].strip() or "Unknown Company"
            summary_data = summarizer_tool(
                company_name=company_name,
                website_text=scraped.get("text", ""),
                client_service=client_service,
            )

            lead = Lead(
                company_name=company_name,
                website=url,
                contact_email=(scraped.get("emails") or [None])[0],
                phone=(scraped.get("phones") or [None])[0],
                summary=summary_data.get("summary", ""),
                pain_points=summary_data.get("pain_points", []),
                outreach_message=summary_data.get("outreach_message", ""),
                source_snippet=item.get("snippet", ""),
            )

            leads.append(lead)
            self.memory.add_lead(lead.model_dump())

        return leads

    def search_memory(self, query: str, top_k: int = 5) -> list[dict]:
        return self.memory.search(query=query, top_k=top_k)
