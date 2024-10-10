import logging
from logging.handlers import RotatingFileHandler

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Configure logging
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_file = '/app/logs/service_name.log'  # Replace 'service_name' with the actual service name
log_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
log_handler.setFormatter(log_formatter)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

app = FastAPI()

class Message(BaseModel):
    role: str
    content: str

class Conversation(BaseModel):
    messages: List[Message]

class LLMProvider:
    def __init__(self, api_key: str, base_url: str, model_name: str, temperature: float, top_p: float, max_tokens: int):
        logger.info(f"Initializing LLMProvider with model: {model_name}")
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key
        )
        self.model_name = model_name
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens

    def generate_response(self, messages: List[Message]) -> str:
        try:
            logger.info(f"Generating response for {len(messages)} messages")
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": msg.role, "content": msg.content} for msg in messages],
                temperature=self.temperature,
                top_p=self.top_p,
                max_tokens=self.max_tokens
            )
            logger.info("Response generated successfully")
            return completion.choices[0].message.content
        except Exception as e:
            logger.error(f"NVIDIA API request failed: {str(e)}")
            raise HTTPException(status_code=500, detail=f"NVIDIA API request failed: {str(e)}")

# Initialize the LLM provider
llm_provider = LLMProvider(
    api_key=os.getenv("NVIDIA_API_KEY"),
    base_url=os.getenv("NVIDIA_API_BASE_URL"),
    model_name=os.getenv("NVIDIA_MODEL_NAME"),
    temperature=float(os.getenv("NVIDIA_TEMPERATURE", "0.7")),
    top_p=float(os.getenv("NVIDIA_TOP_P", "0.9")),
    max_tokens=int(os.getenv("NVIDIA_MAX_TOKENS", "1024"))
)

@app.post("/generate")
async def generate_response(conversation: Conversation):
    try:
        logger.info(f"Received request to generate response for conversation with {len(conversation.messages)} messages")
        response = llm_provider.generate_response(conversation.messages)
        logger.info("Response generated and returned successfully")
        return {"response": response}
    except Exception as e:
        logger.error(f"Error in generate_response: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("LLM_SERVICE_PORT", 8002))
    logger.info(f"Starting LLM service on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)