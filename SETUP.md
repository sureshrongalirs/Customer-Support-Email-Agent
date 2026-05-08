# Setup and Testing Guide

## Installation

### 1. Create Virtual Environment

```cmd
python -m venv venv
.\venv\Scripts\activate
```

### 2. Install Dependencies

```cmd
pip install -r requirements.txt
```

If you encounter dependency conflicts, use flexible version constraints:

```cmd
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

## Configuration

### 1. Set Up Environment Variables

```cmd
cp .env.example .env.local
```

Edit `.env.local` and add your OpenAI API key:

```
OPENAI_API_KEY=sk-your-actual-key-here
OPENAI_MODEL=gpt-4
```

### 2. Populate Knowledge Base

Add sample documentation to `knowledge_base/`:

```bash
knowledge_base/
├── login_issues.txt
├── billing_help.txt
├── technical_faq.txt
└── features.txt
```

Example `knowledge_base/login_issues.txt`:
```
LOGIN AND PASSWORD TROUBLESHOOTING

Issue: Cannot login to account
Solution: 
1. Clear browser cache and cookies
2. Try the "Forgot Password" link to reset
3. Ensure you're using the correct email address
4. Try incognito/private browsing mode

Issue: Password reset not working
Solution:
1. Check your email spam folder
2. Wait 5-10 minutes and try again
3. Contact support if you still have issues
```

## Running the Application

### Start the Server

```cmd
uvicorn src.main:app --reload
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Access the API

- **Interactive Docs**: http://localhost:8000/docs
- **API Root**: http://localhost:8000/
- **Health Check**: http://localhost:8000/health

## Testing the Workflow

### Test 1: Simple Email Processing

**Using cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/emails/process" \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "customer@example.com",
    "subject": "I cannot login",
    "body": "I am unable to access my account. The password reset is not working."
  }'
```

**Expected Response:**
```json
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

### Test 2: Check Email Status

```bash
curl -X GET "http://localhost:8000/api/v1/emails/email_abc123def456"
```

### Test 3: Get Detailed Information

```bash
curl -X GET "http://localhost:8000/api/v1/emails/email_abc123def456/details"
```

### Test 4: View Statistics

```bash
curl -X GET "http://localhost:8000/api/v1/stats"
```

### Test 5: Using Swagger UI

1. Open http://localhost:8000/docs in your browser
2. Click on "POST /api/v1/emails/process"
3. Click "Try it out"
4. Enter test data:
```json
{
  "sender": "test@example.com",
  "subject": "Billing question",
  "body": "Why was I charged twice for my subscription?"
}
```
5. Click "Execute"

## Workflow Testing

### Test Case 1: Automatic Response (Happy Path)

**Email:**
```
From: customer@example.com
Subject: How do I reset my password?
Body: I forgot my password and need to reset it. Can you help?
```

**Expected Flow:**
1. ✓ Email parsed successfully
2. ✓ Classified as: `general_inquiry` or `technical_support`
3. ✓ Knowledge base: Found documentation on password reset
4. ✓ Response generated automatically
5. ✓ Human review: Not required
6. ✓ Email sent to customer
7. ✓ Follow-up scheduled

**Status**: `completed`

### Test Case 2: Escalation to Human Review

**Email:**
```
From: angry-customer@example.com
Subject: UNACCEPTABLE SERVICE!
Body: This is absolutely unacceptable! Your service is terrible and I want a refund now!
```

**Expected Flow:**
1. ✓ Email parsed successfully
2. ✓ Classified as: `complaint`
3. ✓ Priority: `high`
4. ✓ Human review router: **Routes to human**

**Status**: `pending_review`

**Reason**: "Customer complaint requires human review"

### Test Case 3: Missing Documentation

**Email:**
```
From: user@example.com
Subject: Custom integration with API
Body: We need help integrating your API with our custom system. Can someone help?
```

**Expected Flow:**
1. ✓ Email parsed successfully
2. ✓ Classified as: `technical_support`
3. ✓ Knowledge base: No matching documentation
4. ✓ Human review router: **Routes to human**

**Status**: `pending_review`

**Reason**: "No relevant documentation found - needs human expertise"

### Test Case 4: Billing Complaint

**Email:**
```
From: billing@company.com
Subject: Fraudulent charge on account
Body: I see an unauthorized charge on my account. This was not approved by me!
```

**Expected Flow:**
1. ✓ Email parsed successfully
2. ✓ Classified as: `billing`
3. ✓ Priority: `high`
4. ✓ Keyword detection: "unauthorized" found
5. ✓ Human review router: **Routes to human**

**Status**: `pending_review`

## Running Tests

### Run All Tests

```cmd
pytest tests/ -v
```

### Run Specific Test Class

```cmd
pytest tests/test_example.py::TestEmailService -v
```

### Run with Coverage

```cmd
pytest tests/ -v --cov=src
```

### Run Only Integration Tests

```cmd
pytest tests/ -v -k "integration"
```

## Monitoring and Debugging

### View Application Logs

The application logs to both console and file:

```
logs/
└── app.log
```

View logs in real-time:
```cmd
tail -f logs/app.log
```

### Change Log Level

In `.env.local`:
```
LOG_LEVEL=DEBUG
```

### Test with Different Models

In `.env.local`:
```
OPENAI_MODEL=gpt-3.5-turbo
```

## Troubleshooting

### Issue: ModuleNotFoundError: No module named 'src'

**Solution:**
```cmd
pip install -e .
```

### Issue: OpenAI API Key Errors

**Solution:**
1. Verify API key is set:
   ```cmd
   echo %OPENAI_API_KEY%
   ```
2. Restart Python environment after changing .env

### Issue: Port 8000 Already in Use

**Solution:**
```cmd
uvicorn src.main:app --port 8001
```

### Issue: Knowledge Base Search Returns No Results

**Solution:**
1. Check `knowledge_base/` directory exists
2. Add `.txt` files to directory
3. Check file permissions (readable)
4. Verify file contains relevant keywords

### Issue: LLM Response Generation Fails

**Solution:**
1. Check internet connection
2. Verify OpenAI API is accessible
3. Check API rate limits
4. Review error message in logs

## Performance Testing

### Load Testing

Use ApacheBench:
```cmd
ab -n 100 -c 10 http://localhost:8000/health
```

### Simulating Concurrent Requests

```python
import asyncio
import httpx

async def test_concurrent():
    async with httpx.AsyncClient() as client:
        tasks = [
            client.post("http://localhost:8000/api/v1/emails/process",
                       json={
                           "sender": f"user{i}@example.com",
                           "subject": "Test",
                           "body": "Test message"
                       })
            for i in range(10)
        ]
        results = await asyncio.gather(*tasks)
        return results

# Run: asyncio.run(test_concurrent())
```

## Production Deployment

### Using Docker

```bash
docker build -t customer-support-agent .
docker run -p 8000:8000 --env-file .env.local customer-support-agent
```

### Using Docker Compose

```bash
docker-compose up
```

### Environment Configuration for Production

Update `.env.local` for production:
```
ENV=production
LOG_LEVEL=WARNING
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=sk-...
```

## Next Steps

1. ✓ Complete setup and verify installation
2. ✓ Test workflow with sample emails
3. ✓ Populate knowledge base with real documentation
4. ✓ Configure SMTP for actual email sending
5. ✓ Set up monitoring and logging
6. ✓ Deploy to production
7. Monitor performance and adjust as needed

## Support

For issues or questions:
1. Check logs in `logs/app.log`
2. Review error messages in API responses
3. Test individual nodes with unit tests
4. Enable DEBUG logging for detailed output