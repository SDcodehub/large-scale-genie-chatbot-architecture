# Chat Service

The Chat Service acts as a bridge between the UI Service and the LLM Service, managing real-time communication.

## What does it do?

- Establishes and maintains WebSocket connections with the UI Service.
- Receives messages from the UI in real-time.
- Forwards these messages to the LLM Service for processing.
- Sends the LLM Service's responses back to the UI in real-time.

## How does it work?

1. When a user opens the chat interface, the UI Service establishes a WebSocket connection with the Chat Service.
2. As the user sends messages, they're immediately sent through this WebSocket connection to the Chat Service.
3. The Chat Service forwards these messages to the LLM Service.
4. When the LLM Service responds, the Chat Service immediately sends this response back through the WebSocket.

## Technical Details

- Built using FastAPI, which provides WebSocket support.
- Uses the `websockets` library for handling WebSocket connections.
- Uses `httpx` for making asynchronous HTTP requests to the LLM Service.

## Why is it important?

The Chat Service enables real-time, two-way communication between the user interface and the AI. It's like a telephone operator, ensuring that messages are passed back and forth quickly and efficiently. This real-time capability makes the chat feel more natural and responsive.

## What is a WebSocket?

A WebSocket is a technology that allows a web page to maintain a continuous, two-way connection with a server. Unlike regular web requests:

- The connection stays open, so data can be sent back and forth without delay.
- Both the web page and the server can send messages at any time.
- It's very efficient for real-time applications like chat.

Think of it like a phone call, where both parties can speak and listen at any time, as opposed to sending letters back and forth.
