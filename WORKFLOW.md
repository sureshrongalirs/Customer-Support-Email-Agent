# Email Processing Workflow

## Overview

This document describes the complete email processing workflow implemented using LangGraph. The system processes incoming customer support emails through a series of nodes that classify, analyze, and respond to customer inquiries.

## Workflow Architecture

```
┌─────────────┐
│ Parse Email │
└──────┬──────┘
       │
       ▼
┌──────────────────┐
│ Classify Intent  │
└────────┬─────────┘
         │
         ▼
┌──────────────────────┐
│ Search Knowledge Base │
└────────┬─────────────┘
         │
         ▼
┌─────────────────────┐
│ Generate Response   │
└────────┬────────────┘
         │
         ▼
┌───────────────────────┐
│ Human Review Router   │
└────────┬──────────────┘
         │
    ┌────┴─────────────┐
    │                  │
    ▼                  ▼
PENDING REVIEW   ┌─────────────┐
                 │ Send Email  │
                 └────────┬────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ Schedule Followup │
                 └──────────────────┘
```

## Nodes Description

### 1. Email Parser (`src/nodes/email_processor.py`)

**Purpose**: Parse and validate incoming customer emails

**Inputs**:
- `sender`: Email sender address
- `subject`: Email subject line
- `body`: Email body content

**Processing**:
- Validates email format (sender is valid email)
- Checks that subject and body are not empty
- Extracts key information from email body
- Identifies customer name, account ID, issue description

**Outputs**:
```python
{
    "sender": "customer@example.com",
    "subject": "Help with my account",
    "body": "I cannot login...",
    "extracted_entities": {
        "customer_name": "",
        "account_id": "",
        "issue_description": "..."
    },
    "error": None  # If validation fails
}
```

### 2. Intent Classifier (`src/nodes/intent_classifier.py`)

**Purpose**: Classify email into predefined categories

**Categories**:
- `billing` - Payment, refund, invoice issues
- `technical_support` - Software bugs, installation, performance
- `general_inquiry` - Product info, account questions
- `complaint` - Service issues, negative experiences
- `feature_request` - Enhancement suggestions
- `other` - Unknown or uncategorized

**Processing**:
- Uses LLM to classify email
- Determines priority based on category
- Calculates confidence score

**Priority Mapping**:
- **HIGH**: complaints, billing issues, technical support
- **NORMAL**: general inquiries
- **LOW**: feature requests

**Outputs**:
```python
{
    "classification": {
        "category": "technical_support",
        "confidence": 0.95,
        "priority": "high"
    },
    "priority": "high"
}
```

### 3. Knowledge Base Search (`src/nodes/knowledge_base_search.py`)

**Purpose**: Find relevant documentation for the customer's issue

**Processing**:
- Builds search query from email content and category
- Searches files in `knowledge_base/` directory
- Scores documents by relevance
- Extracts relevant excerpts

**Search Strategy**:
1. Match category keywords
2. Search for query terms in documents
3. Calculate relevance score
4. Return top 5 most relevant documents

**Outputs**:
```python
{
    "knowledge_base_results": {
        "query": "technical_support unable to login",
        "found_relevant_docs": true,
        "results": [
            {
                "file": "login_issues.txt",
                "relevance_score": 8,
                "matched_keywords": ["technical", "support"],
                "excerpt": "To reset your password..."
            }
        ]
    }
}
```

### 4. Response Generator (`src/nodes/response_generator.py`)

**Purpose**: Generate appropriate response to customer

**Processing**:
- Formats knowledge base results for context
- Creates LLM prompt with relevant documentation
- Generates professional response
- Falls back to template if LLM fails

**Fallback Responses**:
- **Billing**: Payment inquiry acknowledgment
- **Technical Support**: Issue investigation acknowledgment
- **Complaint**: Apology and escalation notice
- **Feature Request**: Thank you message
- **Default**: Generic helpful response

**Outputs**:
```python
{
    "draft_response": "Thank you for reaching out about your login issue. "
                      "Based on our documentation, here are steps to reset your password..."
}
```

### 5. Human Review Router (`src/nodes/human_review_router.py`)

**Purpose**: Determine if email needs human review

**Escalation Criteria**:
1. Processing errors occurred
2. High priority (billing, complaints, technical issues)
3. No relevant documentation found
4. Low classification confidence (< 60%)
5. Complaint or unknown category emails

**Additional Checks for High Priority**:
- **Billing**: Keywords like "refund", "fraud", "unauthorized"
- **Technical Support**: No documentation found
- **Complaint**: Always escalate

**Outputs**:
```python
{
    "requires_human_review": true,
    "human_review_reason": "High priority email requiring human attention"
}
```

### 6. Email Sender (`src/nodes/email_sender.py`)

**Purpose**: Send final email response to customer

**Processing**:
- Skips sending if human review required
- Validates recipient email address
- Attempts SMTP delivery if configured
- Falls back to simulation mode if SMTP unavailable

**Email Construction**:
```
To: {customer_email}
Subject: Re: {original_subject}
Body: {draft_response}
```

**Outputs**:
```python
{
    "sent": true,
    "final_response": "Response body...",
    "error": None
}
```

### 7. Followup Scheduler (`src/nodes/followup_scheduler.py`)

**Purpose**: Schedule follow-up actions for customer issues

**Scheduling Logic**:

| Category | Delay | Followup Type |
|----------|-------|---------------|
| Technical Support | 24 hours | solution_check |
| Billing | 48 hours | verification |
| Complaint | 12 hours | satisfaction_check |
| Feature Request | 7 days | acknowledgment |
| General Inquiry | 72 hours | confirmation |
| High Priority | 4 hours | status_check |

**Outputs**:
```python
{
    "follow_up_scheduled": true,
    "followup_schedule": {
        "email_id": "email_abc123",
        "scheduled_for": "2024-01-15T10:30:00",
        "delay_hours": 24,
        "followup_type": "solution_check",
        "notes": "Verify technical issue is resolved"
    }
}
```

## State Machine Transitions

### Happy Path (Automated Response)
1. Parse Email ✓
2. Classify Intent ✓
3. Search Knowledge Base ✓
4. Generate Response ✓
5. Human Review Router → Ready to Send
6. Send Email ✓
7. Schedule Followup ✓

### Escalation Path (Human Review)
1. Parse Email ✓
2. Classify Intent ✓
3. Search Knowledge Base ✓
4. Generate Response ✓
5. Human Review Router → Needs Review
6. **END (Routed to human queue)**

## API Endpoints

### Process Email
```
POST /api/v1/emails/process

Request:
{
    "sender": "customer@example.com",
    "subject": "Help with my account",
    "body": "I cannot login to my account"
}

Response:
{
    "email_id": "email_abc123def456",
    "status": "completed",
    "response": null,
    "error": null,
    "metadata": {
        "category": "technical_support",
        "priority": "high",
        "sent": true,
        "requires_human_review": false,
        "follow_up_scheduled": true
    }
}
```

### Get Email Status
```
GET /api/v1/emails/{email_id}

Response:
{
    "email_id": "email_abc123def456",
    "status": "completed",
    "category": "technical_support",
    "priority": "high",
    "sent": true,
    "requires_human_review": false,
    "follow_up_scheduled": true,
    "error": null
}
```

### Get Email Details
```
GET /api/v1/emails/{email_id}/details

Response:
{
    "email_id": "email_abc123def456",
    "sender": "customer@example.com",
    "subject": "Help with my account",
    "classification": {
        "category": "technical_support",
        "confidence": 0.95,
        "priority": "high"
    },
    "knowledge_base_results": {
        "found_relevant_docs": true,
        "results": [...]
    },
    "draft_response": "Thank you for reaching out...",
    "final_response": "...",
    "priority": "high",
    "requires_human_review": false,
    "follow_up_schedule": {...},
    "sent": true,
    "error": null
}
```

### Get Statistics
```
GET /api/v1/stats

Response:
{
    "total_emails": 42,
    "sent_emails": 38,
    "pending_review": 3,
    "with_errors": 1,
    "by_category": {
        "technical_support": 12,
        "billing": 8,
        "general_inquiry": 15,
        "complaint": 4,
        "feature_request": 3
    }
}
```

## Configuration

### Environment Variables
- `OPENAI_API_KEY` - OpenAI API key (required)
- `OPENAI_MODEL` - Model name (default: gpt-4)
- `KNOWLEDGE_BASE_PATH` - Path to knowledge base documents
- `SMTP_SERVER` - SMTP server for email sending
- `SMTP_PORT` - SMTP port (default: 587)
- `SMTP_USERNAME` - SMTP username
- `SMTP_PASSWORD` - SMTP password
- `LOG_LEVEL` - Logging level (default: INFO)

### Knowledge Base Format

Create `.txt` files in `knowledge_base/` directory:

```
knowledge_base/
├── login_issues.txt
├── payment_problems.txt
├── billing_faq.txt
├── technical_support.txt
└── feature_roadmap.txt
```

Each file can contain documentation, FAQs, or reference information.

## Error Handling

### Validation Errors
- Invalid sender email → Routes to human review
- Empty subject/body → Routes to human review

### LLM Errors
- Classification failure → Uses "general" category
- Response generation failure → Uses fallback template

### Knowledge Base Errors
- File not found → Continues with empty results
- File read error → Logs warning, continues

### Processing Errors
- Any error → Routes to human review with error message

## Performance Considerations

- **Knowledge Base Search**: O(n*m) where n=files, m=query terms
- **LLM Calls**: 3-4 calls per email (classify, generate, sentiment)
- **Typical Processing Time**: 5-15 seconds per email

## Future Enhancements

1. **Embeddings-based Search**: Use vector similarity for KB search
2. **Caching**: Cache LLM responses for common queries
3. **Multi-language**: Support multiple languages
4. **Sentiment Analysis**: Add sentiment tracking
5. **A/B Testing**: Test different response templates
6. **Analytics**: Track resolution rates, customer satisfaction
7. **Integration**: Connect to CRM, ticketing systems
8. **Scheduled Tasks**: Implement actual followup sending