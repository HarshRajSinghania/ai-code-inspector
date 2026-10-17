# app/config.py
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    WEBHOOK_SECRET: str = os.getenv("WEBHOOK_SECRET", "")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Global settings
settings = Settings()