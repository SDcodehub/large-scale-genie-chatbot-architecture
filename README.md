# AI Chatbot System

Welcome to our AI Chatbot System! This project implements a modular, scalable chatbot architecture using modern web technologies and AI.

## Table of Contents

- [AI Chatbot System](#ai-chatbot-system)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Architecture Overview](#architecture-overview)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Configuration](#configuration)
  - [Running the System](#running-the-system)
  - [Using the Chatbot](#using-the-chatbot)
  - [Monitoring and Debugging](#monitoring-and-debugging)
  - [Services](#services)
  - [Logging and Analytics](#logging-and-analytics)
  - [Troubleshooting](#troubleshooting)
  - [Future Scope](#future-scope)
  - [Contributing](#contributing)
  - [License](#license)

## Features

- Real-time chat interface using Streamlit
- AI-powered responses using NVIDIA's language models
- Multiple chat sessions support with dynamic session naming
- Persistent chat history
- Modular, microservices-based architecture using Docker and Docker Compose
- Flexible chat history storage with options for in-memory or SQLite database
- Comprehensive logging system using ELK stack (Elasticsearch, Logstash, Kibana)

## Architecture Overview

Our system consists of four main services and a logging stack:

1. **UI Service**: A Streamlit-based web interface for user interaction
2. **LLM Service**: Processes messages using NVIDIA's AI models
3. **Chat Service**: Manages real-time communication between services
4. **History Service**: Stores and retrieves conversation histories
5. **ELK Stack**: Handles logging and log analysis

For a detailed architecture diagram and explanation, see our [Architecture Documentation](docs/architecture.md).

## Getting Started

### Prerequisites

- Docker (version 20.10 or later)
- Docker Compose (version 1.29 or later)
- Git

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ai-chatbot-system.git
   cd ai-chatbot-system
   ```

2. Create necessary directories:
   ```
   mkdir logs data
   ```

### Configuration

1. Create a `.env` file in the root directory with the following content:
   ```
   NVIDIA_API_KEY=your_api_key_here
   NVIDIA_API_BASE_URL=https://api.nvidia.com/v1
   NVIDIA_MODEL_NAME=your_chosen_model
   NVIDIA_TEMPERATURE=0.7
   NVIDIA_TOP_P=0.9
   NVIDIA_MAX_TOKENS=1024
   HISTORY_STORAGE=memory
   SQLITE_DB_PATH=/app/data/chat_history.sqlite
   ```
   Replace `your_api_key_here` and `your_chosen_model` with your actual NVIDIA API credentials and preferred model.

2. Review and adjust the configurations in `services/common/filebeat.yml` and `services/common/logstash.conf` if needed.

## Running the System

1. Build and start the services:
   ```
   docker-compose up --build
   ```

2. Once everything is running, open a web browser and go to:
   ```
   http://localhost:8501
   ```

3. To stop the system, press `Ctrl+C` in the terminal where you ran `docker-compose up`, or run:
   ```
   docker-compose down
   ```

## Using the Chatbot

1. Open `http://localhost:8501` in your web browser.
2. Start a new chat session or select an existing one.
3. Type your message in the input box and press Enter or click the "Send" button.
4. View the AI's response in the chat window.
5. Use the sidebar to switch between different chat sessions or start a new one.

For more details on the user interface, see the [UI Service Documentation](docs/ui_service.md).

## Monitoring and Debugging

1. Access Kibana for log analysis:
   - Open `http://localhost:5601` in your web browser
   - Go to "Discover" in the left sidebar
   - Create an index pattern "genie-chatbot-logs-*" if prompted
   - Use the Discover view to search and analyze logs

2. View service logs:
   ```
   docker-compose logs <service_name>
   ```
   Replace `<service_name>` with ui_service, llm_service, chat_service, history_service, elasticsearch, logstash, kibana, or filebeat.

3. Check Elasticsearch indices:
   ```
   curl http://localhost:9200/_cat/indices
   ```

For more debugging tips, see the [Troubleshooting](#troubleshooting) section.

## Services

- [UI Service](docs/ui_service.md): Handles user interaction (Port 8501)
- [LLM Service](docs/llm_service.md): Processes messages with AI (Port 8002)
- [Chat Service](docs/chat_service.md): Manages real-time communication (Port 8000)
- [History Service](docs/history_service.md): Stores chat histories (Port 8003)

## Logging and Analytics

Our system uses the ELK (Elasticsearch, Logstash, Kibana) stack for comprehensive logging:

- Filebeat: Collects logs from each service
- Logstash: Processes and transforms logs
- Elasticsearch: Stores and indexes logs
- Kibana: Visualizes and analyzes logs

For more details on setting up and using the logging system, see the [Logging and Analytics Guide](docs/logging_and_analytics.md).

## Troubleshooting

- If services fail to start, check the Docker logs for error messages:
  ```
  docker-compose logs
  ```

- If you can't connect to a service, ensure all services are running:
  ```
  docker-compose ps
  ```

- For issues with the NVIDIA API, verify your API key and credentials in the `.env` file.

- If logs are not appearing in Kibana:
  1. Check that log files are being created in the `./logs` directory
  2. Verify Filebeat is reading logs: `docker-compose logs filebeat`
  3. Check Logstash is processing logs: `docker-compose logs logstash`
  4. Ensure Elasticsearch is receiving data: `curl http://localhost:9200/_cat/indices`

For more troubleshooting tips, see the [Troubleshooting Guide](docs/troubleshooting.md).

## Future Scope

- Database Integration for persistent storage
- User Authentication
- Analytics Service for chat data insights
- Multi-language Support
- Customization Options for AI personality
- Integration with External Services (calendar, email, etc.)
- Voice Interface
- Mobile App development
- Admin Panel for system management
- Scalability Improvements (load balancing, service discovery)

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.