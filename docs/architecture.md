# System Architecture

Our chatbot system is composed of several interconnected services, each with a specific role. This modular design allows for flexibility, scalability, and easier maintenance.

## Overview

```
+------------+    +---------------+    +------------+
|            |    |               |    |            |
| UI Service |<-->| Chat Service  |<-->| LLM Service|
|            |    |               |    |            |
+------------+    +---------------+    +------------+
       ^                                     ^
       |                                     |
       v                                     v
+------------------+              +------------------+
|                  |              |                  |
| History Service  |              |   NVIDIA API     |
|                  |              |                  |
+------------------+              +------------------+
```

## Components

1. **UI Service**: The user interface, built with Streamlit.
2. **Chat Service**: Manages real-time communication using WebSockets.
3. **LLM Service**: Processes messages and generates responses using AI.
4. **History Service**: Stores and retrieves chat histories.
5. **NVIDIA API**: External AI service used by the LLM Service.

## How They Work Together

1. A user interacts with the UI Service in their web browser.
2. The UI Service establishes a WebSocket connection with the Chat Service.
3. User messages are sent through this WebSocket to the Chat Service.
4. The Chat Service forwards these messages to the LLM Service.
5. The LLM Service processes the message using the NVIDIA API and generates a response.
6. This response is sent back through the Chat Service to the UI Service.
7. The UI Service displays the response to the user.
8. Throughout this process, the UI Service sends messages to the History Service to be stored.

This architecture allows for real-time, stateful conversations with an AI, while maintaining a history of these conversations for future reference.
