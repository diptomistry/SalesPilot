"""Configuration settings for the AI Sales CRM."""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Groq API Configuration
    GROQ_API_KEY: Optional[str] = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = "llama-3.1-70b-versatile"
    GROQ_API_URL: str = "https://api.groq.com/openai/v1/chat/completions"
    
    # MailHog SMTP Configuration
    SMTP_HOST: str = os.getenv("SMTP_HOST", "mailhog")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "1025"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    SMTP_FROM_EMAIL: str = os.getenv("SMTP_FROM_EMAIL", "sales@example.com")
    SMTP_FROM_NAME: str = os.getenv("SMTP_FROM_NAME", "Sales Team")
    
    # Application Settings
    CSV_FILE_PATH: str = os.getenv("CSV_FILE_PATH", "/app/data/leads.csv")
    REPORTS_DIR: str = os.getenv("REPORTS_DIR", "/app/reports")
    
    # LLM Settings
    MAX_RETRIES: int = 3
    REQUEST_TIMEOUT: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

