# Agentic Honeypot API

A FastAPI-based honeypot service to detect scam messages, extract intelligence, and simulate agent responses.
Deployed live on Render.

# Endpoints

1. GET /
Health check route.

**Response:**
```Json```
{"message": "Agentic Honeypot API is live!"}

--------------------

2. POST /message
Detects scams in text messages, extracts intelligence, and generates agent replies.

```Python```
class MessageInput(BaseModel):
    api_key: str
    conversation_id: str
    message: str
    history: list[str]

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
            "timestamp": int(time.time())
        },
        "extracted_intelligence": intelligence,
        "agent_reply": agent_reply
    }

**Request Example:**
```Json```
{
  "api_key": "<YOUR_API_KEY>",
  "conversation_id": "123",
  "message": "Hello, I am from your bank, please click http://fakebank.com",
  "history": ["previous message"]
}

**Response Example:**
```Json```
{
  "scam_detected": true,
  "engagement_metrics": {
    "turns": 2,
    "timestamp": 1738350000
  },
  "extracted_intelligence": {
    "bank_accounts": [],
    "upi_ids": [],
    "phishing_urls": ["http://fakebank.com"]
  },
  "agent_reply": "Oh, which bank are you calling from?"
}

--------------------

3. POST /voice (Basic Stub)
Accepts audio input in Base64 format.
This is a placeholder endpoint for hackathon testing — it validates fields and returns a structured response.

```Python```
class AudioInput(BaseModel):
    api_key: str
    language: str
    audio_format: str
    audio_base64: str

@app.post("/voice")
async def process_voice(input: AudioInput):
    if input.api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    if not input.audio_base64:
        raise HTTPException(status_code=400, detail="Audio data missing")

    return {
        "voice_detected": True,
        "language": input.language,
        "audio_format": input.audio_format,
        "analysis": {
            "result": "This is a placeholder response for demo purposes."
        }
    }

**Request Example:**
```Json```
{
  "api_key": "<YOUR_API_KEY>",
  "language": "en",
  "audio_format": "wav",
  "audio_base64": "UklGRiQAAABXQVZFZm10IBAAAA..."
}

**Response Example:**
```Json```
{
  "voice_detected": true,
  "language": "en",
  "audio_format": "wav",
  "analysis": {
    "result": "This is a placeholder response for demo purposes."
  }
}

--------------------

# Authentication
Set an environment variable in Render:

API_KEY = <YOUR_API_KEY>

All requests must include this key in the JSON payload or header (x-api-key).

**Usage Example (curl)**
```Bash```
curl -X 'POST' \
  'https://<YOUR-RENDER-URL>/message' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "api_key": "<YOUR_API_KEY>",
  "conversation_id": "123",
  "message": "Hello, I am from your bank, please click http://fakebank.com",
  "history": ["previous message"]
}'

--------------------

# Live Demo

- Base URL: https://honeypot-sentinel.onrender.com
- Swagger Docs: https://honeypot-sentinel.onrender.com/docs