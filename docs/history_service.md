# History Service

The History Service is responsible for storing and retrieving chat histories for different user sessions.

## What does it do?

- Stores messages from each chat session.
- Retrieves the full history of a chat session when requested.
- Allows the chatbot to remember previous conversations.

## How does it work?

1. Every time a message is sent or received in a chat:
   - The UI Service sends this message to the History Service.
   - The History Service stores this message, associating it with a unique session ID.

2. When a user returns to a previous chat session:
   - The UI Service requests the history for that session ID.
   - The History Service retrieves all stored messages for that session.
   - These messages are sent back to the UI Service, allowing the conversation to be reconstructed.

## Technical Details

- Built using FastAPI, a modern Python web framework.
- Currently uses in-memory storage (data is lost when the service restarts).
- Could be extended to use a database for persistent storage.

## Why is it important?

The History Service is like the chatbot's memory. It allows conversations to persist over time, enabling users to return to previous chats and allowing the AI to maintain context over long periods. This makes interactions feel more natural and allows for more complex, multi-session interactions.
