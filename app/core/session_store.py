_sessions = {}


def get_or_create_session(session_id: str) -> dict:
    if session_id not in _sessions:
        _sessions[session_id] = {
            "sessionId": session_id,
            "turnCount": 0,
            "conversationHistory": [],
            "extractedIntelligence": {
                "bankAccounts": [],
                "upiIds": [],
                "phishingLinks": [],
                "phoneNumbers": [],
                "suspiciousKeywords": []
            },
            "flags": {},
            "confidence": 0.0
        }
    return _sessions[session_id]


def update_session(session: dict, sender: str, text: str):
    session["turnCount"] += 1
    session["conversationHistory"].append(
        {"sender": sender, "text": text}
    )
