# Claude Project Configuration

## Project Overview
Customer Support Email Agent - A LangGraph-based intelligent email automation system powered by FastAPI and OpenAI.

## Tech Stack
- **Python**: 3.11+
- **Framework**: FastAPI
- **Graph Orchestration**: LangGraph
- **LLM**: LangChain + OpenAI
- **Data Validation**: Pydantic
- **Server**: Uvicorn

## Project Structure

```
├── src/
│   ├── main.py                 # FastAPI app entry point
│   ├── api/                    # API routes
│   ├── graph/                  # LangGraph workflows
│   ├── nodes/                  # Graph node processors
│   ├── services/               # Business logic services
│   ├── prompts/                # LLM prompt templates
│   ├── schemas/                # Pydantic models
│   ├── core/                   # Configuration & logging
│   └── utils/                  # Helper utilities
├── knowledge_base/             # Knowledge base files
├── tests/                      # Test suite
├── requirements.txt            # Dependencies
├── pyproject.toml              # Project metadata
├── Dockerfile                  # Docker configuration
└── docker-compose.yml          # Docker Compose setup
```

## Setup Instructions

### 1. Prerequisites
- Python 3.11 or higher
- pip package manager

### 2. Install Dependencies
```bash
python -m venv venv
source venv/Scripts/activate  # Windows
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
cp .env.example .env.local
# Edit .env.local with your API keys
```

### 4. Run Locally
```bash
uvicorn src.main:app --reload
```

API will be available at: `http://localhost:8000`
- Docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Key Modules

### API Routes (`src/api/routes.py`)
- `POST /api/v1/emails/process` - Process customer email
- `GET /api/v1/emails/{email_id}` - Get email status
- `GET /health` - Health check

### Services
- **EmailService**: Handle email validation, sending, and thread retrieval
- **LLMService**: LLM interactions, classification, entity extraction

### LangGraph Workflow (`src/graph/workflow.py`)
Defines the multi-step email processing pipeline:
1. Email parsing and validation
2. Classification and analysis
3. Response generation
4. Email sending

### Nodes (`src/nodes/`)
- **EmailProcessor**: Handles email classification and entity extraction

## Development Workflow

### Running Tests
```bash
pytest tests/ -v
pytest tests/ -v --cov=src  # With coverage
```

### Code Formatting
```bash
black src/ tests/
ruff check src/ tests/
```

### Adding New Endpoints
1. Create route in `src/api/routes.py`
2. Define schema in `src/schemas/`
3. Implement logic in appropriate service

### Adding New Graph Nodes
1. Create node class in `src/nodes/`
2. Register in `src/graph/workflow.py`
3. Add corresponding tests

## Environment Variables

Required:
- `OPENAI_API_KEY` - OpenAI API key

Optional:
- `ENV` - development/production
- `LOG_LEVEL` - INFO/DEBUG/WARNING
- `SMTP_*` - Email configuration

See `.env.example` for complete list.

## Deployment

### Docker
```bash
docker build -t customer-support-agent .
docker run -p 8000:8000 --env-file .env customer-support-agent
```

### Docker Compose
```bash
docker-compose up
```

## Common Issues

1. **Import errors**: Ensure virtual environment is activated
2. **API key issues**: Verify `OPENAI_API_KEY` in `.env.local`
3. **Port already in use**: Change API_PORT in `.env.local`

## Next Steps

1. ✅ Project scaffold created
2. ⬜ Implement LangGraph workflow with full nodes
3. ⬜ Integrate email validation and processing
4. ⬜ Add comprehensive test coverage
5. ⬜ Configure knowledge base integration
6. ⬜ Deploy and monitor

## Notes for Future Development

- Keep prompts organized in `src/prompts/`
- Use Pydantic models for all data validation
- Implement proper error handling in all nodes
- Document complex business logic inline
- Write tests for new features before implementation
