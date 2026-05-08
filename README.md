# Customer Support Email Agent

A LangGraph-based intelligent customer support email agent built with FastAPI, LangChain, and OpenAI.

## Overview

This project implements an automated customer support system that:
- Processes incoming customer support emails
- Routes emails to appropriate support categories
- Generates intelligent, context-aware responses
- Maintains conversation history and context
- Leverages LangGraph for complex workflow orchestration

## Tech Stack

- **Python 3.11+** - Programming language
- **FastAPI** - Modern web framework for building APIs
- **LangGraph** - Graph-based workflow orchestration
- **LangChain** - LLM orchestration and chain management
- **LangChain OpenAI** - OpenAI integration
- **Pydantic** - Data validation and settings management
- **Uvicorn** - ASGI server

## Project Structure

```
.
├── src/
│   ├── api/                 # FastAPI routes and endpoints
│   ├── graph/               # LangGraph workflow definitions
│   ├── nodes/               # Individual graph nodes (processors)
│   ├── services/            # Business logic services
│   ├── prompts/             # LLM prompt templates
│   ├── schemas/             # Pydantic data models
│   ├── core/                # Core configuration and settings
│   ├── utils/               # Utility functions and helpers
│   └── main.py              # FastAPI application entry point
├── knowledge_base/          # Domain knowledge and reference data
├── tests/                   # Test suite
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables template
├── .env.local              # Local environment overrides (git-ignored)
├── pyproject.toml          # Project metadata
└── README.md               # This file
```

## Installation

### Prerequisites
- Python 3.11 or higher
- pip or uv package manager

### Setup Steps

1. **Clone or navigate to the project directory**
   ```bash
   cd "d:Customer Support Email Agent"
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   # or
   source venv/bin/activate      # On macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env .env.local
   # Edit .env.local with your configuration
   ```

5. **Set up API keys**
   - Add your OpenAI API key to `.env.local`
   - Configure email settings if needed

## Quick Start

### Run the API Server

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Development

```bash
# Format code
black src tests

# Run linting
ruff check src tests

# Run tests
pytest tests/
```

## Module Overview

### `src/api/`
Contains FastAPI route handlers for:
- Email submission endpoints
- Status checking
- Response retrieval

### `src/graph/`
LangGraph workflow definitions that orchestrate the multi-step processing:
- Email analysis workflow
- Response generation workflow
- State management

### `src/nodes/`
Individual processing nodes that execute specific tasks:
- Email parsing and analysis
- Classification and routing
- Response generation
- Email sending

### `src/services/`
Business logic services:
- `email_service.py` - Email handling and SMTP integration
- `llm_service.py` - LLM interactions and prompt management

### `src/schemas/`
Pydantic models for data validation:
- Email request/response models
- Internal state models

### `src/core/`
Core application configuration:
- `config.py` - Settings management
- `logger.py` - Logging configuration

### `src/utils/`
Helper utilities for common operations

### `knowledge_base/`
Domain-specific knowledge and reference documents

## Configuration

All configuration is managed through environment variables in `.env` and `.env.local`.

Key variables:
- `OPENAI_API_KEY` - OpenAI API key
- `OPENAI_MODEL` - Model to use (default: gpt-4)
- `API_PORT` - API server port (default: 8000)
- `LOG_LEVEL` - Logging level

## Development

### Adding a New Node

1. Create a new file in `src/nodes/`
2. Define the node function
3. Register it in the LangGraph workflow

### Adding a New API Endpoint

1. Create a route in `src/api/routes.py`
2. Define request/response schemas in `src/schemas/`
3. Implement the business logic in appropriate services

## Testing

```bash
pytest tests/ -v
```

## Deployment

### Using Docker

```bash
docker build -t customer-support-agent .
docker run -p 8000:8000 --env-file .env customer-support-agent
```

### Using Docker Compose

```bash
docker-compose up
```

## Environment Variables Reference

| Variable | Description | Default |
|----------|-------------|---------|
| `ENV` | Environment (development/production) | development |
| `API_HOST` | API server host | 0.0.0.0 |
| `API_PORT` | API server port | 8000 |
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `OPENAI_MODEL` | OpenAI model name | gpt-4 |
| `LOG_LEVEL` | Logging level | INFO |
| `KNOWLEDGE_BASE_PATH` | Path to knowledge base | ./knowledge_base |

## Best Practices

- Keep prompts organized in `src/prompts/`
- Use Pydantic models for all data validation
- Implement proper error handling in nodes
- Write tests for new features
- Document complex business logic

## Troubleshooting

### Import Errors
Ensure the virtual environment is activated and all dependencies are installed:
```bash
pip install -r requirements.txt
```

### API Port Already in Use
Change the port using:
```bash
uvicorn src.main:app --port 8001
```

### OpenAI API Key Issues
Verify your API key is correctly set in `.env.local`:
```bash
echo $OPENAI_API_KEY  # Should print your key
```

## Contributing

1. Create a feature branch
2. Make changes following project structure
3. Write tests for new features
4. Update documentation as needed

## License

[Specify your license]

## Support

For issues or questions, please open an issue in the project repository.

## Next Steps

1. Configure `.env.local` with your credentials
2. Implement core services in `src/services/`
3. Define email schema and processing nodes
4. Create LangGraph workflow in `src/graph/`
5. Build API endpoints in `src/api/`
6. Add tests in `tests/`
