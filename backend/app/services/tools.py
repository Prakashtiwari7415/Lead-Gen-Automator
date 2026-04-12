import json
import re
from typing import Any

import requests
from bs4 import BeautifulSoup
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from tavily import TavilyClient

from backend.app.core.config import get_settings, require_gemini_key, require_tavily_key


def _safe_get(url: str, timeout: int = 12) -> str:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/122.0 Safari/537.36"
        )
    }
    response = requests.get(url, headers=headers, timeout=timeout)
    response.raise_for_status()
    return response.text


def web_search_tool(niche: str, location: str, max_results: int = 10) -> list[dict[str, Any]]:
    settings = get_settings()
    require_tavily_key(settings)
    tavily = TavilyClient(api_key=settings.tavily_api_key)
    query = f"{niche} companies in {location} official website"
    result = tavily.search(query=query, max_results=max_results, search_depth="basic")

    leads = []
    for item in result.get("results", []):
        leads.append(
            {
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "snippet": item.get("content", ""),
            }
        )
    return leads


def scraper_tool(url: str) -> dict[str, Any]:
    try:
        html = _safe_get(url)
    except Exception:
        return {
            "url": url,
            "text": "",
            "emails": [],
            "phones": [],
        }

    soup = BeautifulSoup(html, "html.parser")

    for s in soup(["script", "style", "noscript"]):
        s.extract()

    text = " ".join(soup.get_text(separator=" ").split())
    text = text[:6000]
    email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    phone_pattern = r"(?:\+?\d{1,3}[-.\s]?)?(?:\d{3,5}[-.\s]?){2,4}\d{2,4}"

    emails = list(dict.fromkeys(re.findall(email_pattern, text)))[:5]
    phones = list(dict.fromkeys(re.findall(phone_pattern, text)))[:5]

    return {
        "url": url,
        "text": text,
        "emails": emails,
        "phones": phones,
    }


def summarizer_tool(company_name: str, website_text: str, client_service: str) -> dict[str, Any]:
    settings = get_settings()
    
    # Try to use Gemini API first
    try:
        require_gemini_key(settings)
        llm = ChatGoogleGenerativeAI(model=settings.gemini_model, api_key=settings.gemini_api_key, temperature=0.2)

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    (
                        "You are a professional B2B sales researcher.\n"
                        "Given website text and client offering, extract practical sales intel.\n"
                        "Return ONLY valid JSON with keys: summary, pain_points, outreach_message."
                    ),
                ),
                (
                    "human",
                    (
                        "Company: {company_name}\n"
                        "Client Service: {client_service}\n"
                        "Website Text: {website_text}\n"
                        "Create concise output."
                    ),
                ),
            ]
        )

        raw = llm.invoke(
            prompt.format_messages(
                company_name=company_name,
                client_service=client_service,
                website_text=website_text[:4500],
            )
        ).content

        try:
            data = json.loads(raw)
            return data
        except Exception:
            pass  # Fall through to mock response
            
    except Exception as e:
        print(f"Gemini API unavailable: {e}")
    
    # Mock fallback response when API is not available
    return {
        "summary": f"{company_name} appears to be a business that could potentially benefit from {client_service}. Based on available information, they may be looking to improve their digital presence and operational efficiency.",
        "pain_points": [
            "Limited online visibility",
            "Potential operational inefficiencies", 
            "Need for better digital solutions"
        ],
        "outreach_message": (
            f"Hi {company_name} team,\n\n"
            f"I came across your company and believe our {client_service} could help enhance your business operations and digital presence.\n\n"
            f"Would you be open to a brief 15-minute call to discuss how we can support your goals?\n\n"
            f"Best regards"
        ),
    }
