from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from backend.app.core.config import get_settings, require_gemini_key


class LeadMemoryStore:
    def __init__(self) -> None:
        self._store: Chroma | None = None

    def _ensure_store(self) -> Chroma:
        if self._store is not None:
            return self._store
        settings = get_settings()
        
        # Always use mock embeddings for now due to API quota issues
        from langchain_community.embeddings import FakeEmbeddings
        embeddings = FakeEmbeddings(size=384)
        print("Using mock embeddings for demonstration")
        
        self._store = Chroma(
            collection_name="lead_memory",
            embedding_function=embeddings,
            persist_directory=settings.chroma_persist_dir,
        )
        return self._store

    def add_lead(self, payload: dict) -> None:
        store = self._ensure_store()
        text = (
            f"Company: {payload.get('company_name', '')}\n"
            f"Website: {payload.get('website', '')}\n"
            f"Summary: {payload.get('summary', '')}\n"
            f"Pain points: {', '.join(payload.get('pain_points', []))}\n"
            f"Outreach: {payload.get('outreach_message', '')}"
        )
        doc = Document(page_content=text, metadata=payload)
        store.add_documents([doc])

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        store = self._ensure_store()
        results = store.similarity_search_with_relevance_scores(query, k=top_k)
        formatted = []
        for doc, score in results:
            formatted.append(
                {
                    "score": score,
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                }
            )
        return formatted
