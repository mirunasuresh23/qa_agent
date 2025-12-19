"""Configuration settings for the Data QA Agent backend."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    app_name: str = "Data QA Agent Backend"
    debug: bool = False
    
    # Google Cloud
    google_cloud_project: str = "miruna-sandpit"
    vertex_ai_location: str = "us-central1"
    vertex_ai_model: str = "gemini-2.5-flash"
    
    # CORS
    cors_origins: list[str] = [
        "http://localhost:3000",
        "https://data-qa-agent-*.run.app",
        "https://data-qa-agent-frontend-750147355601.us-central1.run.app"
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
