from pydantic import BaseModel
from typing import Optional

class MessageContent(BaseModel):
    sender: str
    text: str

class RequestPayload(BaseModel):
    sessionId: str
    message: MessageContent

class HoneypotResponse(BaseModel):
    status: str
    reply: str
