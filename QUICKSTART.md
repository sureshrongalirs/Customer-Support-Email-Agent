# Quick Start Guide

Get up and running with the Customer Support Email Agent in 5 minutes.

## Prerequisites
- Python 3.11 or higher
- OpenAI API key

## Step 1: Environment Setup

```bash
# Clone/navigate to project
cd "d:\Projects\Claude\Customer Support Email Agent"

# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Configure API Keys

```bash
# Copy environment template
cp .env.example .env.local

# Edit .env.local and add your OpenAI API key
# OPENAI_API_KEY=sk-your-actual-key-here
```

## Step 3: Run the Server

```bash
uvicorn src.main:app --reload
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

## Step 4: Test the API

### Option A: Using Swagger UI
Open your browser: `http://localhost:8000/docs`

### Option B: Using cURL
```bash
curl -X GET "http://localhost:8000/health"
```

Expected response:
```json
{
  "status": "healthy",
  "service": "Customer Support Email Agent"
}
```

## Step 5: Process Your First Email

```bash
curl -X POST "http://localhost:8000/api/v1/emails/process" \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "customer@example.com",
    "subject": "Help with my account",
    "body": "I cannot login to my account"
  }'
```

## Project Structure at a Glance

```
Customer Support Email Agent/
├── src/                    # Main application code
│   ├── main.py            # FastAPI app
│   ├── api/               # API endpoints
│   ├── graph/             # LangGraph workflows
│   ├── nodes/             # Processing nodes
│   ├── services/          # Business logic
│   ├── schemas/           # Data models
│   ├── prompts/           # LLM prompts
│   ├── core/              # Config & logging
│   └── utils/             # Helper functions
├── knowledge_base/        # Reference documents
├── tests/                 # Test suite
├── requirements.txt       # Dependencies
├── .env.local            # Your local config (create from .env.example)
└── README.md             # Full documentation
```

## Common Commands

```bash
# Run tests
pytest tests/ -v

# Format code
black src/ tests/

# Check code style
ruff check src/

# View API docs
# Open browser to http://localhost:8000/docs

# Run with specific port
uvicorn src.main:app --port 8001

# Production mode
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

## Next Steps

1. ✅ Environment is set up
2. ⬜ Customize knowledge base in `knowledge_base/`
3. ⬜ Update prompts in `src/prompts/templates.py`
4. ⬜ Implement graph nodes in `src/graph/workflow.py`
5. ⬜ Add more API endpoints as needed
6. ⬜ Configure SMTP for email sending
7. ⬜ Add comprehensive tests

## Troubleshooting

### Port 8000 already in use?
```bash
uvicorn src.main:app --port 8001
```

### OpenAI API key not found?
Make sure `.env.local` is in the project root and contains:
```
OPENAI_API_KEY=sk-your-key-here
```

### Import errors?
Verify virtual environment is activated:
```bash
source venv/Scripts/activate  # Windows
```

## Documentation

- [Full README](./README.md)
- [Project Configuration](./CLAUDE.md)
- [Python Requirements](./requirements.txt)

## Support

For detailed documentation, see `README.md` and `CLAUDE.md` in the project root.

---

You're all set! The API is ready for development. 🚀
