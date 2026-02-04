import re

def detect_scam(session: dict, message: str) -> dict:
    """
    Returns:
    {
        "scamDetected": bool,
        "confidence": float,
        "signals": list[str]
    }
    """
    # Initialize intelligence if missing (Matches SessionStore initialization)
    if "extractedIntelligence" not in session:
        session["extractedIntelligence"] = {
            "bankAccounts": [],
            "upiIds": [],
            "phishingLinks": [],
            "phoneNumbers": [],
            "suspiciousKeywords": []
        }
    
    intel = session["extractedIntelligence"]
    signals = []
    confidence = 0.0
    msg_lower = message.lower()

    # Intelligence Extraction
    # UPI IDs
    upis = re.findall(r'[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}', message)
    for upi in upis:
        if upi not in intel["upiIds"]:
            intel["upiIds"].append(upi)
            signals.append(f"UPI detected: {upi}")
            confidence += 0.3

    # Bank accounts
    banks = re.findall(r'\b\d{9,18}\b', message)
    for bank in banks:
        if bank not in intel["bankAccounts"]:
            intel["bankAccounts"].append(bank)
            signals.append("Bank account pattern")
            confidence += 0.2

    # URLs
    urls = re.findall(r'https?://\S+', message)
    for url in urls:
        if url not in intel["phishingLinks"]:
            intel["phishingLinks"].append(url)
            signals.append(f"URL: {url}")
            confidence += 0.3

    # Phone numbers
    phones = re.findall(r'\b\d{10,12}\b', message)
    for phone in phones:
        if phone not in intel["phoneNumbers"]:
            intel["phoneNumbers"].append(phone)
            signals.append(f"Phone: {phone}")
            confidence += 0.1

    # Heuristics
    keywords = {"kyc": 0.4, "lottery": 0.5, "urgent": 0.3, "block": 0.3, "win": 0.4, "otp": 0.5}
    for kw, weight in keywords.items():
        if kw in msg_lower:
            if kw not in intel["suspiciousKeywords"]:
                intel["suspiciousKeywords"].append(kw)
            signals.append(f"Keyword: {kw}")
            confidence += weight

    confidence = min(1.0, confidence)
    
    return {
        "scamDetected": confidence > 0.4,
        "detected": confidence > 0.4, # Member 1 compatibility
        "confidence": round(confidence, 2),
        "signals": list(set(signals))
    }
