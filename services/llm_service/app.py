from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

app = FastAPI()

class Message(BaseModel):
    role: str
    content: str

class Conversation(BaseModel):
    messages: List[Message]

class LLMProvider:
    def __init__(self, api_key: str, base_url: str, model_name: str, temperature: float, top_p: float, max_tokens: int):
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
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": msg.role, "content": msg.content} for msg in messages],
                temperature=self.temperature,
                top_p=self.top_p,
                max_tokens=self.max_tokens
            )
            return completion.choices[0].message.content
        except Exception as e:
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
        response = llm_provider.generate_response(conversation.messages)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("LLM_SERVICE_PORT", 8002)))