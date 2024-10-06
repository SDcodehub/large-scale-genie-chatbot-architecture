# LLM Service

The LLM (Large Language Model) Service is the brain of our chatbot system. It's responsible for understanding user messages and generating appropriate responses.

## What does it do?

- Receives messages from the UI Service.
- Processes these messages using a powerful AI model.
- Generates human-like responses based on the conversation context.
- Sends these responses back to the UI Service.

## How does it work?

1. When a user sends a message, it's received by the LLM Service.
2. The service prepares this message, along with previous messages from the same conversation, to send to the AI model.
3. The AI model (in this case, a model from NVIDIA) processes this information.
4. The model generates a response, which the LLM Service then sends back.

## Technical Details

- Built using FastAPI, a modern Python web framework.
- Uses the OpenAI library to interact with the NVIDIA API.
- Configurable parameters like temperature and max tokens allow fine-tuning of the AI's responses.

## Why is it important?

The LLM Service is like the brain of our chatbot. It's what allows the chatbot to understand context, generate relevant responses, and engage in human-like conversation. Without it, our chatbot would just be a simple program that gives pre-programmed responses.
