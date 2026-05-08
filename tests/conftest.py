"""Pytest Configuration and Fixtures"""

import os

import pytest
from fastapi.testclient import TestClient

os.environ["ENV"] = "test"


@pytest.fixture
def client():
    """Provide FastAPI test client."""
    from src.main import app

    return TestClient(app)


@pytest.fixture
def sample_email():
    """Provide sample email data for testing."""
    return {
        "sender": "customer@example.com",
        "subject": "Need help with my account",
        "body": "I'm unable to login to my account. Can you help?",
    }


@pytest.fixture
async def llm_service():
    """Provide LLM service instance."""
    from src.services.llm_service import LLMService

    return LLMService()


@pytest.fixture
async def email_service():
    """Provide email service instance."""
    from src.services.email_service import EmailService

    return EmailService()
