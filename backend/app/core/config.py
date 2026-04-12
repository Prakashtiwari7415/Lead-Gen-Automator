from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Optional at process start so uvicorn can boot before .env is filled.
    openai_api_key: str | None = None
    gemini_api_key: str | None = None
    tavily_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"
    gemini_model: str = "gemini-2.0-flash"
    embedding_model: str = "text-embedding-3-small"
    chroma_persist_dir: str = "./data/chroma"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()


def _missing_msg(name: str, purpose: str) -> str:
    return f"Set {name} in your environment or .env file ({purpose})."


def require_openai_key(settings: Settings) -> None:
    if not (settings.openai_api_key and settings.openai_api_key.strip()):
        raise ValueError(_missing_msg("OPENAI_API_KEY", "embeddings, summaries, and lead memory"))


def require_gemini_key(settings: Settings) -> None:
    if not (settings.gemini_api_key and settings.gemini_api_key.strip()):
        raise ValueError(_missing_msg("GEMINI_API_KEY", "embeddings, summaries, and lead memory"))


def require_tavily_key(settings: Settings) -> None:
    if not (settings.tavily_api_key and settings.tavily_api_key.strip()):
        raise ValueError(_missing_msg("TAVILY_API_KEY", "web search for leads"))
