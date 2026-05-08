# Project Structure and File Guide

## Complete File Listing

```
Customer Support Email Agent/
├── src/                              # Main application code
│   ├── __init__.py                  # Package initializer
│   ├── main.py                      # FastAPI application entry point
│   │
│   ├── api/                         # REST API endpoints
│   │   ├── __init__.py
│   │   └── routes.py                # Email processing and status endpoints
│   │
│   ├── graph/                       # LangGraph workflow orchestration
│   │   ├── __init__.py
│   │   └── workflow.py              # Complete workflow definition
│   │
│   ├── nodes/                       # Individual processing nodes
│   │   ├── __init__.py
│   │   ├── email_processor.py       # Email parsing and validation
│   │   ├── intent_classifier.py     # Email classification
│   │   ├── knowledge_base_search.py # Documentation search
│   │   ├── response_generator.py    # Response creation
│   │   ├── human_review_router.py   # Escalation logic
│   │   ├── email_sender.py          # Email transmission
│   │   └── followup_scheduler.py    # Scheduling logic
│   │
│   ├── services/                    # Business logic services
│   │   ├── __init__.py
│   │   ├── email_service.py         # Email operations (validation, sending)
│   │   └── llm_service.py           # LLM interactions
│   │
│   ├── schemas/                     # Pydantic data models
│   │   ├── __init__.py
│   │   └── email.py                 # Email request/response models
│   │
│   ├── prompts/                     # LLM prompt templates
│   │   ├── __init__.py
│   │   └── templates.py             # All prompt templates
│   │
│   ├── core/                        # Core configuration
│   │   ├── __init__.py
│   │   ├── config.py                # Settings management (Pydantic)
│   │   └── logger.py                # Logging configuration
│   │
│   └── utils/                       # Utility functions
│       ├── __init__.py
│       └── helpers.py               # Helper functions
│
├── knowledge_base/                  # Knowledge base documents
│   ├── __init__.py
│   └── sample_data.txt              # Sample documentation
│
├── tests/                           # Test suite
│   ├── __init__.py
│   ├── conftest.py                  # Pytest configuration and fixtures
│   └── test_example.py              # Comprehensive test cases
│
├── logs/                            # Application logs (auto-created)
│   └── app.log                      # Main application log
│
├── .env                             # Environment variables template
├── .env.example                     # Example environment config (for sharing)
├── .env.local                       # Local configuration (create from .env.example)
├── .gitignore                       # Git ignore patterns
├── requirements.txt                 # Python dependencies
├── pyproject.toml                   # Project metadata and tools config
├── Dockerfile                       # Docker image definition
├── docker-compose.yml               # Docker Compose configuration
│
├── README.md                        # Main project documentation
├── QUICKSTART.md                    # 5-minute quick start guide
├── SETUP.md                         # Detailed setup and testing guide
├── WORKFLOW.md                      # Workflow architecture documentation
├── CLAUDE.md                        # Claude Code project configuration
├── PROJECT_STRUCTURE.md             # This file
└── LICENSE                          # Project license (if applicable)
```

## File Descriptions

### Root Configuration Files

| File | Purpose |
|------|---------|
| `requirements.txt` | Python package dependencies |
| `.env` | Environment variables template |
| `.env.example` | Safe example config for sharing |
| `.gitignore` | Git ignore patterns |
| `pyproject.toml` | Project metadata, build config, tool settings |
| `Dockerfile` | Docker image build instructions |
| `docker-compose.yml` | Multi-container orchestration |

### Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Comprehensive project documentation |
| `QUICKSTART.md` | 5-minute setup guide |
| `SETUP.md` | Detailed installation, testing, troubleshooting |
| `WORKFLOW.md` | Workflow architecture and node descriptions |
| `CLAUDE.md` | Claude Code configuration and development guide |
| `PROJECT_STRUCTURE.md` | This file - project organization |

### Application Code

#### `src/main.py`
- FastAPI application entry point
- Application factory function
- Health check and root endpoints
- CORS middleware configuration
- Router registration

#### `src/api/routes.py`
- REST API endpoints for email processing
- Email processing endpoint (POST)
- Email status endpoint (GET)
- Email details endpoint (GET)
- Statistics endpoint (GET)

#### `src/graph/workflow.py`
- LangGraph workflow definition
- State machine (EmailProcessingState)
- Node registration
- Edge connections
- Workflow execution function

#### `src/nodes/email_processor.py`
- Email parsing and validation
- Key information extraction
- Email format validation

#### `src/nodes/intent_classifier.py`
- Email classification into categories
- Priority determination
- Confidence scoring
- LLM-based classification

#### `src/nodes/knowledge_base_search.py`
- Document search and retrieval
- Relevance scoring
- Excerpt extraction
- Category-aware search

#### `src/nodes/response_generator.py`
- LLM-based response generation
- Knowledge base context integration
- Fallback template responses

#### `src/nodes/human_review_router.py`
- Escalation criteria evaluation
- Human review routing logic
- Reason documentation

#### `src/nodes/email_sender.py`
- Email transmission (SMTP or simulated)
- Recipient validation
- Email construction

#### `src/nodes/followup_scheduler.py`
- Follow-up scheduling logic
- Category-based delay calculation
- Schedule creation

#### `src/services/email_service.py`
- Email validation
- SMTP configuration
- Email sending
- Email thread management

#### `src/services/llm_service.py`
- OpenAI integration (ChatOpenAI)
- LLM response generation
- Email classification
- Entity extraction
- Sentiment analysis

#### `src/schemas/email.py`
- Pydantic models for requests
- Pydantic models for responses
- State models
- Processing result models

#### `src/prompts/templates.py`
- System prompt
- Classification prompt
- Response generation prompt
- Sentiment analysis prompt
- Entity extraction prompt
- Urgency assessment prompt

#### `src/core/config.py`
- Settings management using Pydantic
- Environment variable loading
- Default configuration values
- Settings caching

#### `src/core/logger.py`
- Logging configuration
- Console and file handlers
- Log formatting
- Log level management

#### `src/utils/helpers.py`
- Email ID generation
- Text truncation
- Email content parsing
- Safe dictionary access
- Timestamp formatting

### Test Files

#### `tests/conftest.py`
- Pytest configuration
- Test client fixture
- Sample data fixtures
- Service fixtures

#### `tests/test_example.py`
- Helper function tests
- Application startup tests
- Email service tests
- Intent classifier tests
- Human review router tests
- API endpoint tests
- Workflow integration tests

### Knowledge Base

#### `knowledge_base/sample_data.txt`
- Sample support documentation
- Common issues and solutions
- Company information
- Response guidelines
- Escalation criteria

## Node Workflow Graph

```
Input Email
    ↓
[parse_email]
    ↓
[classify_intent]
    ↓
[search_knowledge_base]
    ↓
[generate_response]
    ↓
[human_review_router] ← Decision Point
    ├─→ requires_review: TRUE → END (Queue for human)
    └─→ requires_review: FALSE
            ↓
        [send_email]
            ↓
        [schedule_followup]
            ↓
          END
```

## Data Flow

### Request Flow
```
HTTP POST /api/v1/emails/process
    ↓
EmailRequest (Pydantic validation)
    ↓
API Route Handler
    ↓
generate_email_id()
    ↓
Create EmailProcessingState
    ↓
execute_workflow()
    ↓
Return ProcessingResult
```

### State Updates Through Nodes
```
Initial State:
{
    email_id: str
    sender: str
    subject: str
    body: str
    classification: {}
    extracted_entities: {}
    knowledge_base_results: {}
    draft_response: ""
    requires_human_review: bool
    priority: str
    final_response: ""
    sent: bool
    follow_up_scheduled: bool
    error: None
}

After parse_email:
+ extracted_entities: {...}

After classify_intent:
+ classification: {...}
+ priority: str

After search_knowledge_base:
+ knowledge_base_results: {...}

After generate_response:
+ draft_response: str

After human_review_router:
+ requires_human_review: bool
+ human_review_reason: str

After send_email:
+ sent: bool
+ final_response: str

After schedule_followup:
+ follow_up_scheduled: bool
+ followup_schedule: {...}
```

## Configuration Hierarchy

1. **Default Values** (hardcoded in config.py)
2. **Environment Variables** (from .env file)
3. **Runtime Overrides** (programmatically set)

Example:
```
config.api_port = 8000                    # Default
api_port = 8001  # from OPENAI_API_KEY=... in .env
OPENAI_API_KEY=sk-xxx              # At runtime
```

## Dependencies Map

```
FastAPI → Uvicorn (HTTP server)
  ↓
LangChain → OpenAI (LLM)
  ↓
LangGraph → State management
  ↓
Pydantic → Data validation
  ↓
python-dotenv → Configuration
```

## Environment Variables Reference

| Variable | Type | Default | Required |
|----------|------|---------|----------|
| ENV | string | development | No |
| API_HOST | string | 0.0.0.0 | No |
| API_PORT | int | 8000 | No |
| OPENAI_API_KEY | string | - | **Yes** |
| OPENAI_MODEL | string | gpt-4 | No |
| LOG_LEVEL | string | INFO | No |
| SMTP_SERVER | string | - | No |
| SMTP_PORT | int | 587 | No |
| SMTP_USERNAME | string | - | No |
| SMTP_PASSWORD | string | - | No |
| KNOWLEDGE_BASE_PATH | string | ./knowledge_base | No |

## File Sizes and Complexity

| File | Lines | Complexity | Purpose |
|------|-------|-----------|---------|
| workflow.py | ~120 | High | Core orchestration |
| routes.py | ~180 | High | API endpoints |
| email_sender.py | ~60 | Medium | Email transmission |
| response_generator.py | ~100 | Medium | Response creation |
| knowledge_base_search.py | ~140 | High | Document search |
| human_review_router.py | ~130 | High | Escalation logic |
| intent_classifier.py | ~90 | Medium | Classification |
| email_service.py | ~120 | Medium | Email operations |
| llm_service.py | ~180 | High | LLM integration |

## Development Workflow

1. **Code Changes**
   - Edit files in `src/`
   - Update tests in `tests/`
   - Run `pytest` to verify

2. **Configuration Changes**
   - Update `.env.local`
   - Restart server

3. **Prompt Changes**
   - Edit `src/prompts/templates.py`
   - Test with `/api/v1/emails/process` endpoint

4. **Adding New Nodes**
   - Create file in `src/nodes/`
   - Define node class with async method
   - Register in `src/graph/workflow.py`
   - Add tests in `tests/`

5. **API Changes**
   - Update routes in `src/api/routes.py`
   - Update schemas in `src/schemas/`
   - Test endpoints with curl or Swagger UI

## Deployment Files

| File | Usage |
|------|-------|
| `Dockerfile` | Build container image |
| `docker-compose.yml` | Multi-container deployment |
| `requirements.txt` | Package installation |
| `pyproject.toml` | Build and packaging info |

## Best Practices

1. **Never commit secrets** - Use `.env.local` for API keys
2. **Keep logs organized** - Use structured logging
3. **Test node functions** - Each node should be testable
4. **Document prompts** - Add comments to complex prompts
5. **Validate inputs** - Use Pydantic models
6. **Handle errors gracefully** - Try/except with logging
7. **Update knowledge base** - Keep documentation current
8. **Monitor performance** - Check logs for errors

## Future Enhancements

- [ ] Database integration for storing email history
- [ ] User authentication for API
- [ ] Email attachment handling
- [ ] Multi-language support
- [ ] Advanced analytics and reporting
- [ ] Integration with CRM systems
- [ ] Machine learning-based classification
- [ ] Real-time email notifications
- [ ] Admin dashboard
- [ ] Email template customization