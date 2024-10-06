# Setup and Run Guide

This guide will walk you through setting up and running the chatbot system.

## Prerequisites

- Docker
- Docker Compose

## Setup Steps

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
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
   Replace `your_api_key_here` and `your_chosen_model` with your actual NVIDIA API credentials.

3. Build and start the services:
   ```
   docker-compose up --build
   ```

4. Once everything is running, open a web browser and go to:
   ```
   http://localhost:8501
   ```

You should now see the chat interface and be able to start interacting with the chatbot!

## Stopping the System

To stop the system, press `Ctrl+C` in the terminal where you ran `docker-compose up`, or run:

`docker-compose down`

## Troubleshooting

- If you encounter any "address already in use" errors, make sure no other services are running on ports 8000, 8002, 8003, or 8501.
- If the UI can't connect to other services, ensure all services are running and check the console output for any error messages.
