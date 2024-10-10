import logging
from logging.handlers import RotatingFileHandler
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import sqlite3
from dotenv import load_dotenv
from prometheus_client import Counter, Histogram

load_dotenv()

# Configure logging
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_file = '/app/logs/service_name.log'  # Replace 'service_name' with the actual service name
log_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
log_handler.setFormatter(log_formatter)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

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
    logger.info(f"Adding message for session {message.session_id}")
    if HISTORY_STORAGE == "memory":
        if message.session_id not in chat_history:
            chat_history[message.session_id] = []
        chat_history[message.session_id].append(message)
        logger.info(f"Message added to memory storage for session {message.session_id}")
    elif HISTORY_STORAGE == "sqlite":
        try:
            with sqlite3.connect(SQLITE_DB_PATH) as conn:
                c = conn.cursor()
                c.execute("INSERT INTO messages VALUES (?, ?, ?)",
                          (message.session_id, message.role, message.content))
                conn.commit()
            logger.info(f"Message added to SQLite storage for session {message.session_id}")
        except sqlite3.Error as e:
            logger.error(f"SQLite error: {str(e)}")
            raise HTTPException(status_code=500, detail="Database error")
    return {"status": "success"}

@app.get("/get_history/{session_id}")
async def get_history(session_id: str):
    logger.info(f"Retrieving history for session {session_id}")
    if HISTORY_STORAGE == "memory":
        history = chat_history.get(session_id, [])
        logger.info(f"Retrieved {len(history)} messages from memory storage for session {session_id}")
        return history
    elif HISTORY_STORAGE == "sqlite":
        try:
            with sqlite3.connect(SQLITE_DB_PATH) as conn:
                c = conn.cursor()
                c.execute("SELECT role, content FROM messages WHERE session_id = ?", (session_id,))
                messages = [{"role": role, "content": content} for role, content in c.fetchall()]
            logger.info(f"Retrieved {len(messages)} messages from SQLite storage for session {session_id}")
            return messages
        except sqlite3.Error as e:
            logger.error(f"SQLite error: {str(e)}")
            raise HTTPException(status_code=500, detail="Database error")

if __name__ == "__main__":
    import uvicorn
    port = 8003
    logger.info(f"Starting History service on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
    start_http_server(8003)
