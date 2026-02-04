from fastapi import FastAPI, Depends, Header, HTTPException
from dotenv import load_dotenv
import os

from app.schemas.request_response import RequestPayload, HoneypotResponse
from app.modules.member1.orchestrator import process_message

load_dotenv()

API_KEY = os.getenv("API_KEY")

app = FastAPI(title="Agentic Scam Honeypot", version="0.1.0")


def verify_api_key(x_api_key: str = Header(...)):
    if not API_KEY or x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")


@app.get("/")
def health():
    return {"status": "ok"}


@app.post(
    "/honeypot/message",
    response_model=HoneypotResponse,
    dependencies=[Depends(verify_api_key)]
)
def handle_message(payload: RequestPayload):
    return process_message(payload)
