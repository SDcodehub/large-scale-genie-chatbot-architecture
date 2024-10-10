# AI Chatbot System

Welcome to our AI Chatbot System! This project implements a modular, scalable chatbot architecture using modern web technologies and AI.

## Features

- Real-time chat interface using Streamlit
- AI-powered responses using NVIDIA's language models
- Multiple chat sessions support with dynamic session naming
- Persistent chat history
- Modular, microservices-based architecture using Docker and Docker Compose
- Flexible chat history storage with options for in-memory or SQLite database

## How It Works

1. Users interact with a Streamlit-based web interface.
2. Messages are sent to our backend services.
3. The LLM service processes these messages using NVIDIA's AI models and generates responses.
4. Responses are sent back to the user and displayed in the UI.
5. All conversations are saved in the History service and can be resumed later.

## Architecture

Our system is composed of four main services:

1. **UI Service**: A Streamlit-based web interface users interact with.
2. **LLM Service**: Processes messages using NVIDIA's AI models.
3. **Chat Service**: Manages communication between services.
4. **History Service**: Stores conversation histories.

These services work together to provide a seamless chat experience. For more details, see our [Architecture Documentation](docs/architecture.md).

## Getting Started

To set up and run the system, follow our [Setup and Run Guide](docs/setup_and_run.md).

## Environment Variables

The system uses the following environment variables, which should be set in a `.env` file:

```
NVIDIA_API_KEY=your_api_key_here
NVIDIA_API_BASE_URL=https://api.nvidia.com/v1
NVIDIA_MODEL_NAME=your_chosen_model
NVIDIA_TEMPERATURE=0.7
NVIDIA_TOP_P=0.9
NVIDIA_MAX_TOKENS=1024
HISTORY_STORAGE=memory  # Options: 'memory' or 'sqlite'
SQLITE_DB_PATH=/app/data/chat_history.sqlite  # Only used if HISTORY_STORAGE is 'sqlite'
```

## Detailed Documentation

- [UI Service](docs/ui_service.md)
- [LLM Service](docs/llm_service.md)
- [Chat Service](docs/chat_service.md)
- [History Service](docs/history_service.md)

## Project Structure

```
root/
│
├── services/
│   ├── ui_service/
│   ├── llm_service/
│   ├── chat_service/
│   └── history_service/
│
├── docs/
│   ├── architecture.md
│   ├── setup_and_run.md
│   ├── ui_service.md
│   ├── llm_service.md
│   ├── chat_service.md
│   └── history_service.md
│
├── docker-compose.yml 
├── .env
└── README.md
```

## Future Scope for Expansion

- Database Integration: Implement persistent storage for the History Service.
- User Authentication: Add user registration and authentication.
- Analytics Service: Analyze chat data and provide insights.
- Multi-language Support: Expand UI and LLM services to support multiple languages.
- Customization Options: Allow users to customize the AI's personality or knowledge base.
- Integration with External Services: Add capabilities to integrate with calendar, email, or other productivity tools.
- Voice Interface: Expand the UI service to support voice input and output.
- Mobile App: Develop a mobile application that interfaces with the existing services.
- Admin Panel: Create a separate interface for system administrators.
- Scalability Improvements: Implement load balancing and service discovery.

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
