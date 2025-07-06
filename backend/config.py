import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    FASTAPI_URL: str = os.getenv("FASTAPI_URL", "http://localhost:8000")
    CALENDAR_ID: str = os.getenv("CALENDAR_ID")
    GEMINI_MODEL_NAME: str = os.getenv("GEMINI_MODEL_NAME", "models/gemini-pro")

settings = Settings()
