# Setup and Run Guide

This guide will walk you through setting up and running the AI Chatbot System.

## Prerequisites

- Docker (version 20.10 or later)
- Docker Compose (version 1.29 or later)
- Git

## Setup Steps

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ai-chatbot-system.git
   cd ai-chatbot-system
   ```

2. Create a `.env` file in the root directory with the following content:
   ```
   NVIDIA_API_KEY=your_api_key_here
   NVIDIA_API_BASE_URL=https://api.nvidia.com/v1
   NVIDIA_MODEL_NAME=your_chosen_model
   NVIDIA_TEMPERATURE=0.7
   NVIDIA_TOP_P=0.9
   NVIDIA_MAX_TOKENS=1024
   ```
   Replace `your_api_key_here` and `your_chosen_model` with your actual NVIDIA API credentials and preferred model.

3. Build and start the services:
   ```
   docker-compose up --build
   ```

4. Once everything is running, open a web browser and go to:
   ```
   http://localhost:8501
   ```

You should now see the Streamlit chat interface and be able to start interacting with the chatbot!

## Service Ports

- UI Service: 8501
- LLM Service: 8002
- Chat Service: 8000
- History Service: 8003

Make sure these ports are available on your system.

## Stopping the System

To stop the system, press `Ctrl+C` in the terminal where you ran `docker-compose up`, or run:

```
docker-compose down
```

## Troubleshooting

- If you encounter any "address already in use" errors, make sure no other services are running on the ports listed above.
- If the UI can't connect to other services, ensure all services are running and check the Docker logs for any error messages:
  ```
  docker-compose logs
  ```
- If you're having issues with the NVIDIA API, double-check your API key and other credentials in the `.env` file.

## Updating the System

To update the system with the latest changes:

1. Stop the running services:
   ```
   docker-compose down
   ```

2. Pull the latest changes:
   ```
   git pull origin main
   ```

3. Rebuild and start the services:
   ```
   docker-compose up --build
   ```

## Environment Variables

Here's a sample `.env` file with explanations:

```
# Your NVIDIA API key
NVIDIA_API_KEY=your_api_key_here

# The base URL for the NVIDIA API
NVIDIA_API_BASE_URL=https://api.nvidia.com/v1

# The name of the NVIDIA language model you want to use
NVIDIA_MODEL_NAME=your_chosen_model

# Controls randomness in the model's output (0.0 to 1.0)
NVIDIA_TEMPERATURE=0.7

# Controls diversity of model's output (0.0 to 1.0)
NVIDIA_TOP_P=0.9

# Maximum number of tokens in the model's response
NVIDIA_MAX_TOKENS=1024

# Storage type for chat history: 'memory' or 'sqlite'
HISTORY_STORAGE=memory

# Path to SQLite database file (only used if HISTORY_STORAGE is 'sqlite')
SQLITE_DB_PATH=/app/data/chat_history.sqlite
```

Adjust these values according to your needs and the NVIDIA API documentation.
