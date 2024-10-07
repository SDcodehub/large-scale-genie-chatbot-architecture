from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import httpx
import json
import os
from dotenv import load_dotenv
from typing import List, Dict

from prometheus_client import start_http_server, Counter, Histogram
import time

# Define metrics
http_requests_total = Counter('http_requests_total', 'Total number of HTTP requests', ['method', 'endpoint'])
request_duration = Histogram('request_duration_seconds', 'Duration of HTTP requests')

load_dotenv()



app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LLM_SERVICE_URL = os.getenv("LLM_SERVICE_URL", "http://localhost:8002/generate")

async def get_llm_response(messages: List[Dict[str, str]]):
    async with httpx.AsyncClient() as client:
        response = await client.post(LLM_SERVICE_URL, json={"messages": messages})
        if response.status_code == 200:
            return response.json()["response"]
        else:
            return f"Error: Received status code {response.status_code} from LLM service"

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    conversation_history = []
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            conversation_history.append({"role": "user", "content": message["content"]})
            llm_response = await get_llm_response(conversation_history)
            conversation_history.append({"role": "assistant", "content": llm_response})
            await websocket.send_text(json.dumps({"content": llm_response}))
    except WebSocketDisconnect:
        print("WebSocket disconnected")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    start_http_server(8000)
