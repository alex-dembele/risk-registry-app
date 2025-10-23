from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/riskdb")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your_secret_key_here")
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost"]  # Pour frontend React

    class Config:
        env_file = ".env"

settings = Settings()