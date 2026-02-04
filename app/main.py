import os
from fastapi import FastAPI, Header, HTTPException, Depends
from dotenv import load_dotenv

from app.schemas.request_response import RequestPayload, HoneypotResponse
from app.modules.member1.orchestrator import process_message

load_dotenv()

app = FastAPI(title="Agentic Scam Honeypot", version="0.1.0")
API_KEY = os.getenv("API_KEY", "guvi-demo-key")


def validate_api_key(x_api_key: str | None):
    if not x_api_key or x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/")
async def root_ping(x_api_key: str = Header(None)):
    """
    Required compatibility endpoint for GUVI Honeypot Tester.
    Accepts empty body and only validates API key.
    """
    validate_api_key(x_api_key)
    return {"status": "ok"}


@app.post("/honeypot/test")
async def honeypot_test(x_api_key: str = Header(None)):
    """
    Dedicated endpoint for GUVI Tester UI.
    Accepts no body, validates x-api-key, returns success JSON.
    """
    validate_api_key(x_api_key)
    return {
        "status": "ok",
        "message": "Honeypot endpoint reachable"
    }


@app.post(
    "/honeypot/message",
    response_model=HoneypotResponse
)
def handle_message(payload: RequestPayload, x_api_key: str = Header(None)):
    validate_api_key(x_api_key)
    return process_message(payload)
