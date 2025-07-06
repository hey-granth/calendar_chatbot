from fastapi import FastAPI
from pydantic import BaseModel
from .agent import agent

app = FastAPI()


class Message(BaseModel):
    message: str

@app.post("/chat")
def chat_with_agent(message: Message):
    response = agent.run(message.message)
    return {"response": response}