import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import sqlite3
from dotenv import load_dotenv
from prometheus_client import Counter, Histogram

load_dotenv()

# Define metrics
http_requests_total = Counter('http_requests_total', 'Total number of HTTP requests', ['method', 'endpoint'])
request_duration = Histogram('request_duration_seconds', 'Duration of HTTP requests')

app = FastAPI()

class Message(BaseModel):
    session_id: str
    role: str
    content: str

# Choose storage based on environment variable
HISTORY_STORAGE = os.getenv("HISTORY_STORAGE", "memory")
SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", "chat_history.sqlite")

if HISTORY_STORAGE == "memory":
    chat_history: Dict[str, List[Message]] = {}
elif HISTORY_STORAGE == "sqlite":
    conn = sqlite3.connect(SQLITE_DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (session_id TEXT, role TEXT, content TEXT)''')
    conn.commit()
else:
    raise ValueError("Invalid HISTORY_STORAGE option")

@app.post("/add_message")
async def add_message(message: Message):
    if HISTORY_STORAGE == "memory":
        if message.session_id not in chat_history:
            chat_history[message.session_id] = []
        chat_history[message.session_id].append(message)
    elif HISTORY_STORAGE == "sqlite":
        with sqlite3.connect(SQLITE_DB_PATH) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO messages VALUES (?, ?, ?)",
                      (message.session_id, message.role, message.content))
            conn.commit()
    return {"status": "success"}

@app.get("/get_history/{session_id}")
async def get_history(session_id: str):
    if HISTORY_STORAGE == "memory":
        return chat_history.get(session_id, [])
    elif HISTORY_STORAGE == "sqlite":
        with sqlite3.connect(SQLITE_DB_PATH) as conn:
            c = conn.cursor()
            c.execute("SELECT role, content FROM messages WHERE session_id = ?", (session_id,))
            messages = [{"role": role, "content": content} for role, content in c.fetchall()]
            return messages

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
    start_http_server(8003)
