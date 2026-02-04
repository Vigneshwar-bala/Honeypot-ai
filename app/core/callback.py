import os
import httpx
from dotenv import load_dotenv

load_dotenv()

CALLBACK_URL = os.getenv("GUVI_CALLBACK_URL")
TIMEOUT = int(os.getenv("CALLBACK_TIMEOUT", "5"))


def send_final_callback(session: dict):
    payload = {
        "sessionId": session["sessionId"],
        "scamDetected": True,
        "totalMessagesExchanged": session["turnCount"],
        "extractedIntelligence": session["extractedIntelligence"],
        "agentNotes": "Automated agentic engagement completed"
    }

    if not CALLBACK_URL:
        print(f"Callback failed: GUVI_CALLBACK_URL not set in environment")
        return

    try:
        with httpx.Client(timeout=TIMEOUT) as client:
            response = client.post(CALLBACK_URL, json=payload)
            response.raise_for_status()
    except Exception as e:
        print(f"Callback failed for session {session.get('sessionId')}: {e}")
