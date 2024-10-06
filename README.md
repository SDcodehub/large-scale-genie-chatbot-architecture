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

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
