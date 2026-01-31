from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time, re, os

# Initialize FastAPI app
app = FastAPI(title="Agentic Honeypot API", description="Scam detection and intelligence extraction API")

# Always use environment variable for security
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise RuntimeError("API_KEY environment variable not set!")

# Input schema for text messages
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
    return {
        "bank_accounts": bank_accounts,
        "upi_ids": upi_ids,
        "phishing_urls": urls
    }

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

# Root route for homepage
@app.get("/")
def read_root():
    return {"message": "Agentic Honeypot API is live!"}

# Scam detection endpoint
@app.post("/message")
async def process_message(input: MessageInput):
    # Authentication
    if input.api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # Detection + intelligence extraction
    scam_detected = detect_scam(input.message)
    intelligence = extract_intelligence(input.message)
    agent_reply = agent_response(input.message) if scam_detected else None

    # Response payload
    return {
        "scam_detected": scam_detected,
        "engagement_metrics": {
            "turns": len(input.history) + 1,
            "timestamp": int(time.time())
        },
        "extracted_intelligence": intelligence,
        "agent_reply": agent_reply
    }