"""LLM Prompt Templates"""

SYSTEM_PROMPT = """You are a professional customer support agent.
Your role is to help customers by providing accurate, helpful, and empathetic responses.
Always maintain a professional tone and follow the company's support guidelines.
Be concise, clear, and solution-oriented."""

EMAIL_CLASSIFICATION_PROMPT = """Classify the following email into one of these categories:
- billing
- technical_support
- general_inquiry
- complaint
- feature_request
- other

Email: {email_content}

Respond with ONLY the category name, nothing else."""

EMAIL_RESPONSE_GENERATION_PROMPT = """You are a professional customer support representative.
Based on the customer's email and the relevant documentation provided, draft a professional and helpful response.

CUSTOMER EMAIL:
Subject: {category}
{email_body}

RELEVANT DOCUMENTATION:
{relevant_documentation}

THREAD HISTORY:
{thread_history}

Please write a professional response that:
1. Acknowledges the customer's concern
2. Provides helpful information based on the documentation
3. Offers next steps if applicable
4. Maintains a friendly and professional tone

Response:"""

SENTIMENT_ANALYSIS_PROMPT = """Analyze the sentiment of the following email text.
Classify it as: positive, negative, or neutral.

Email: {email_content}

Respond with ONLY one word: positive, negative, or neutral."""

ENTITY_EXTRACTION_PROMPT = """Extract key information from the following customer email.
Identify: customer name, account/order ID, main issue/topic.

Email: {email_content}

Format response as:
Name: [extracted name or 'not mentioned']
ID: [extracted ID or 'not mentioned']
Issue: [brief issue summary]"""

URGENCY_ASSESSMENT_PROMPT = """Assess the urgency level of this customer email.
Respond with: HIGH, MEDIUM, or LOW

Consider: complaint severity, financial impact, system down status, customer frustration level.

Email: {email_content}

Respond with ONLY: HIGH, MEDIUM, or LOW"""
