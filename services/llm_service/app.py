from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from abc import ABC, abstractmethod
from openai import OpenAI
from typing import Generator

# Load environment variables
load_dotenv()

app = FastAPI()

class Message(BaseModel):
    content: str

class LLMProvider(ABC):
    @abstractmethod
    def generate_response(self, content: str) -> str:
        pass

class NvidiaLLMProvider(LLMProvider):
    def __init__(self, api_key: str, base_url: str, model_name: str, temperature: float, top_p: float, max_tokens: int):
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key
        )
        self.model_name = model_name
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens

    def generate_response(self, content: str) -> str:
        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": content}],
                temperature=self.temperature,
                top_p=self.top_p,
                max_tokens=self.max_tokens,
                stream=True
            )
            
            return self._process_stream(completion)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"NVIDIA API request failed: {str(e)}")

    def _process_stream(self, completion: Generator) -> str:
        full_response = ""
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
        return full_response

class LocalLLMProvider(LLMProvider):
    def __init__(self, model_path: str):
        self.model_path = model_path
        # Initialize your local LLM here
        # self.model = load_model(model_path)

    def generate_response(self, content: str) -> str:
        # Use your local model to generate a response
        # return self.model.generate(content)
        return f"Local LLM response to: {content}"  # Placeholder

# Choose the LLM provider based on environment variables
if os.getenv("USE_NVIDIA_API", "false").lower() == "true":
    print("Using NVIDIA API")
    llm_provider = NvidiaLLMProvider(
        api_key=os.getenv("NVIDIA_API_KEY"),
        base_url=os.getenv("NVIDIA_API_BASE_URL"),
        model_name=os.getenv("NVIDIA_MODEL_NAME"),
        temperature=float(os.getenv("NVIDIA_TEMPERATURE", 0.2)),
        top_p=float(os.getenv("NVIDIA_TOP_P", 0.7)),
        max_tokens=int(os.getenv("NVIDIA_MAX_TOKENS", 1024))
    )
else:
    llm_provider = LocalLLMProvider(model_path=os.getenv("LOCAL_MODEL_PATH"))

@app.post("/generate")
async def generate_response(message: Message):
    try:
        response = llm_provider.generate_response(message.content)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("LLM_SERVICE_PORT", 8001)))
