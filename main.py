from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time, re

# Initialize FastAPI app
app = FastAPI()
API_KEY = "MY_SECRET_KEY"  # replace with your own

# Input schema
class MessageInput(BaseModel):
    api_key: str
    conversation_id: str
    message: str
    history: list[str]

# Scam detection keywords
SCAM_KEYWORDS = ["bank", "lottery", "upi", "password", "account", "link"]

def detect_scam(message: str) -> bool:
    return any(word in message.lower() for word in SCAM_KEYWORDS)

def extract_intelligence(message: str):
    bank_accounts = re.findall(r"\b\d{10,16}\b", message)
    upi_ids = re.findall(r"\b[\w.-]+@[\w.-]+\b", message)
    urls = re.findall(r"https?://\S+", message)
    return {"bank_accounts": bank_accounts, "upi_ids": upi_ids, "phishing_urls": urls}

def agent_response(message: str) -> str:
    if "bank" in message.lower():
        return "Oh, which bank are you calling from?"
    elif "upi" in message.lower():
        return "Can you share the UPI ID for verification?"
    elif "account" in message.lower():
        return "Could you please provide the account number so I can check?"
    elif "link" in message.lower():
        return "I’m not sure, could you resend the link?"
    else:
        return "Could you explain more?"

@app.post("/message")
async def process_message(input: MessageInput):
    if input.api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    scam_detected = detect_scam(input.message)
    intelligence = extract_intelligence(input.message)
    agent_reply = agent_response(input.message) if scam_detected else None

    return {
        "scam_detected": scam_detected,
        "engagement_metrics": {
            "turns": len(input.history) + 1,
            "duration_seconds": int(time.time())
        },
        "extracted_intelligence": intelligence,
        "agent_reply": agent_reply
    }