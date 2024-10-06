# UI Service

The UI Service is the face of our chatbot system. It's what users see and interact with in their web browsers.

## What does it do?

- Displays a chat interface where users can type messages and see responses.
- Manages different chat sessions, allowing users to switch between conversations.
- Sends user messages to the LLM Service for processing.
- Displays the chatbot's responses.
- Saves and loads chat history using the History Service.

## How does it work?

1. When you open the chat in your web browser, you see a chat interface.
2. Each time you send a message:
   - It's displayed in the chat.
   - It's sent to the LLM Service for a response.
   - The response is then displayed in the chat.
   - Both your message and the response are saved to the chat history.

3. You can start new chat sessions or switch between existing ones using buttons on the side of the screen.

## Technical Details

- Built using Streamlit, a Python library for creating web apps.
- Communicates with other services using HTTP requests.
- Stores current session information and chat messages temporarily in the web browser.

## Why is it important?

The UI Service makes the complex AI chatbot system user-friendly. It's like the steering wheel of a car - it's how you control and interact with the powerful engine (the AI) underneath.
