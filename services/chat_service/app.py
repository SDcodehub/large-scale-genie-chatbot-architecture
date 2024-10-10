import logging
from logging.handlers import RotatingFileHandler

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import httpx
import json
import os
from dotenv import load_dotenv
from typing import List, Dict

from prometheus_client import start_http_server, Counter, Histogram
import time

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
    logger.info(f"Requesting LLM response for {len(messages)} messages")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(LLM_SERVICE_URL, json={"messages": messages})
            if response.status_code == 200:
                logger.info("LLM response received successfully")
                return response.json()["response"]
            else:
                logger.error(f"LLM service returned status code {response.status_code}")
                return f"Error: Received status code {response.status_code} from LLM service"
        except httpx.RequestError as e:
            logger.error(f"Error connecting to LLM service: {str(e)}")
            return f"Error: Unable to connect to LLM service. {str(e)}"

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("WebSocket connection established")
    conversation_history = []
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            logger.info(f"Received message: {message['content'][:50]}...")  # Log first 50 chars of the message
            conversation_history.append({"role": "user", "content": message["content"]})
            llm_response = await get_llm_response(conversation_history)
            conversation_history.append({"role": "assistant", "content": llm_response})
            await websocket.send_text(json.dumps({"content": llm_response}))
            logger.info(f"Sent response: {llm_response[:50]}...")  # Log first 50 chars of the response
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")

if __name__ == "__main__":
    import uvicorn
    port = 8000
    logger.info(f"Starting Chat service on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
    start_http_server(8000)
