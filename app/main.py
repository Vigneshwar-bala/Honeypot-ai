from fastapi import FastAPI, Depends
from app.schemas.request_response import RequestPayload, HoneypotResponse
from app.modules.member1.orchestrator import process_message
from app.core.security import verify_api_key

app = FastAPI(title="Agentic Scam Honeypot", version="0.1.0")


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/", dependencies=[Depends(verify_api_key)])
async def root_endpoint():
    """
    Required compatibility endpoint for GUVI Honeypot Tester.
    Accepts empty body and returns standard reachability JSON.
    """
    return {
        "status": "ok",
        "message": "Honeypot API reachable"
    }


@app.post(
    "/honeypot/message",
    response_model=HoneypotResponse,
    dependencies=[Depends(verify_api_key)]
)
def handle_message(payload: RequestPayload):
    return process_message(payload)
