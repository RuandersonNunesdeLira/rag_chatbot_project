from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
from src.core.rag_processor import RagProcessor
from src.app.evolution_client import EvolutionAPIClient

class TextMessage(BaseModel):
    text: str


class Message(BaseModel):
    textMessage: TextMessage


class Sender(BaseModel):
    from_number: str = Field(..., alias='from')


class EvolutionWebHookPayLoad(BaseModel):
    message: Message
    sender: Sender


app = FastAPI()

rag_processor = RagProcessor()
evolution_client = EvolutionAPIClient()

@app.get("/")
async def root():
    return {"message": "Bem vindo à API do ChatBot RAG"}


@app.get("/health")
async def health():
    return {"status": "OK"}

@app.post('/webhook')
async def receive_webhook(payload: EvolutionWebHookPayLoad):
    question = payload.message.textMessage.text
    sender_number = payload.sender.from_number
    if question is None:
        return
    if payload.message.textMessage:
        return

    try:
        answer = rag_processor.ask(question)
    except:
        pass

    evolution_client.send_message(sender_number, answer)

    return {"status": "message processed"}

