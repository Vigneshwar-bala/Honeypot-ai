from app.core.session_store import get_or_create_session, update_session
from app.core.callback import send_final_callback

from app.modules.member2.scam_detection import detect_scam
from app.modules.member2.tactic_classifier import classify_tactic
from app.modules.member2.persona_engine import generate_reply


def process_message(payload):
    session = get_or_create_session(payload.sessionId)

    update_session(session, payload.message.sender, payload.message.text)

    scam_result = detect_scam(session, payload.message.text)
    tactic_result = classify_tactic(session, payload.message.text)
    reply = generate_reply(session, payload.message.text)

    session["confidence"] = scam_result.get("confidence", 0.0)

    is_already_sent = session["flags"].get("callbackSent", False)
    should_exit = not is_already_sent and (
        session["flags"].get("readyForCallback") is True
        or session["turnCount"] >= 12
        or session["confidence"] >= 0.95
    )

    if should_exit:
        send_final_callback(session)
        session["flags"]["callbackSent"] = True

    return {
        "status": "success",
        "reply": reply
    }
