from fastapi import FastAPI
from pydantic import BaseModel
import os
from .agent import agent
from pathlib import Path

def write_service_account_json():
    creds_path = Path("creds/service_account.json")
    creds_path.parent.mkdir(exist_ok=True)

    if not creds_path.exists():
        creds_json = os.getenv("GOOGLE_CREDS_JSON")
        if not creds_json:
            raise RuntimeError("Missing GOOGLE_CREDS_JSON")
        creds_path.write_text(creds_json)

write_service_account_json()

app = FastAPI()


class Message(BaseModel):
    message: str


@app.post("/chat")
def chat_with_agent(message: Message):
    response = agent.run(message.message)
    return {"response": response}
