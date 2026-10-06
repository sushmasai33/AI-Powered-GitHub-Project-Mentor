import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI-Powered GitHub Project Mentor"
    API_V1_STR: str = "/api"
    PORT: int = 8000
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./project_mentor.db")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    NVIDIA_API_KEY: str = os.getenv("NVIDIA_API_KEY", "")
    NVIDIA_MODEL: str = os.getenv("NVIDIA_MODEL", "meta/llama-3.2-11b-vision-instruct")
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "*"
    ]
    CACHE_DIR: str = os.path.expanduser("~/.project_mentor_cache")

    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")

settings = Settings()
