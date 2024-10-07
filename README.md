# AI Chatbot System

Welcome to our AI Chatbot System! This project implements a modular, scalable chatbot architecture using modern web technologies and AI.

## Features

- Real-time chat interface
- AI-powered responses using NVIDIA's language models
- Multiple chat sessions support
- Persistent chat history
- Modular, microservices-based architecture

## How It Works

1. Users interact with a web-based chat interface.
2. Messages are sent in real-time to our backend services.
3. An AI model processes these messages and generates responses.
4. Responses are sent back to the user in real-time.
5. All conversations are saved and can be resumed later.

## Architecture

Our system is composed of four main services:

1. **UI Service**: The web interface users interact with.
2. **Chat Service**: Manages real-time communication.
3. **LLM Service**: Processes messages using AI.
4. **History Service**: Stores conversation histories.

These services work together to provide a seamless chat experience. For more details, see our [Architecture Documentation](docs/architecture.md).

## Getting Started

To set up and run the system, follow our [Setup and Run Guide](docs/setup_and_run.md).

## Detailed Documentation

- [UI Service](docs/ui_service.md)
- [LLM Service](docs/llm_service.md)
- [Chat Service](docs/chat_service.md)
- [History Service](docs/history_service.md)

## Stress Testing

We have implemented various stress tests to ensure the robustness and scalability of our system. These tests are located in the `stress_tests/` directory:

- `locust/locustfile.py`: HTTP load testing using Locust
- `websocket_test.py`: WebSocket connection stress test
- `database_test.py`: Database operations stress test
- `api_gateway_test.py`: API gateway load test
- `long_conversation_test.py`: Long-running conversation simulation
- `chaos_test.py`: Chaos testing for system resilience

To run these tests, navigate to the `stress_tests/` directory and run the desired Python script. For Locust tests, use the command `locust -f locust/locustfile.py`.

## Monitoring

We use Prometheus and Grafana for real-time monitoring of our system. Configuration files can be found in the `monitoring/` directory:

- `prometheus.yml`: Prometheus configuration
- `grafana_dashboard.json`: Grafana dashboard configuration

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
├── tests/
│   └── unit/
│
├── stress_tests/
│   ├── locust/
│   ├── websocket_test.py
│   ├── database_test.py
│   ├── api_gateway_test.py
│   ├── long_conversation_test.py
│   └── chaos_test.py
│
├── monitoring/
│   ├── prometheus.yml
│   └── grafana_dashboard.json
│
└── README.md
```

## Future Scope for Expansion:
- Database Integration: The History Service could be expanded to use a database for persistent storage instead of in-memory storage.
- User Authentication: A new service could be added to handle user registration and authentication.
- Analytics Service: A service could be added to analyze chat data and provide insights.
- Multi-language Support: The UI and LLM services could be expanded to support multiple languages.
- Customization Options: Allow users to customize the AI's personality or knowledge base.
- Integration with External Services: Add capabilities to integrate with calendar, email, or other productivity tools.
- Voice Interface: Expand the UI service to support voice input and output.
- Mobile App: Develop a mobile application that interfaces with the existing services.
- Admin Panel: Create a separate interface for system administrators to monitor and manage the chatbot system.
- Scalability Improvements: Implement load balancing and service discovery for better scalability.

This structure provides a solid foundation for the current system while allowing for future expansion and improvements.

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
