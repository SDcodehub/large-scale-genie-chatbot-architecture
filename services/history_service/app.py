from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

from prometheus_client import start_http_server, Counter, Histogram
import time

# Define metrics
http_requests_total = Counter('http_requests_total', 'Total number of HTTP requests', ['method', 'endpoint'])
request_duration = Histogram('request_duration_seconds', 'Duration of HTTP requests')

app = FastAPI()

# In-memory storage for chat history
chat_history: Dict[str, List[Dict[str, str]]] = {}

class Message(BaseModel):
    session_id: str
    role: str
    content: str

@app.post("/add_message")
async def add_message(message: Message):
    if message.session_id not in chat_history:
        chat_history[message.session_id] = []
    chat_history[message.session_id].append({"role": message.role, "content": message.content})
    return {"status": "success"}

@app.get("/get_history/{session_id}")
async def get_history(session_id: str):
    if session_id not in chat_history:
        raise HTTPException(status_code=404, detail="Session not found")
    return chat_history[session_id]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
    start_http_server(8003)
