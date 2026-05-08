"""Test Cases for Customer Support Email Agent"""

import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.utils.helpers import generate_email_id, truncate_text
from src.services.email_service import EmailService
from src.nodes.intent_classifier import IntentClassifier
from src.nodes.human_review_router import HumanReviewRouter


class TestHelpers:
    """Test helper utility functions."""

    def test_generate_email_id(self):
        """Test email ID generation."""
        email_id = generate_email_id()
        assert email_id.startswith("email_")
        assert len(email_id) > 0

    def test_truncate_text(self):
        """Test text truncation."""
        long_text = "a" * 1000
        truncated = truncate_text(long_text, max_length=100)
        assert len(truncated) == 103  # 100 chars + "..."
        assert truncated.endswith("...")

    def test_truncate_text_no_truncation(self):
        """Test truncation when text is shorter than limit."""
        short_text = "Hello world"
        result = truncate_text(short_text, max_length=100)
        assert result == short_text


class TestApplication:
    """Test application configuration."""

    def test_app_startup(self):
        """Test application can start."""
        assert app is not None
        assert app.title == "Customer Support Email Agent API"

    def test_health_endpoint(self):
        """Test health check endpoint."""
        client = TestClient(app)
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_root_endpoint(self):
        """Test root endpoint."""
        client = TestClient(app)
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "endpoints" in data


class TestEmailService:
    """Test email service functionality."""

    @pytest.mark.asyncio
    async def test_validate_email_valid(self):
        """Test email validation with valid email."""
        service = EmailService()
        result = await service.validate_email(
            sender="test@example.com",
            subject="Test Subject",
            body="Test body content",
        )
        assert result is True

    @pytest.mark.asyncio
    async def test_validate_email_invalid_sender(self):
        """Test email validation with invalid sender."""
        service = EmailService()
        result = await service.validate_email(
            sender="invalid-email",
            subject="Test Subject",
            body="Test body content",
        )
        assert result is False

    @pytest.mark.asyncio
    async def test_validate_email_empty_subject(self):
        """Test email validation with empty subject."""
        service = EmailService()
        result = await service.validate_email(
            sender="test@example.com",
            subject="",
            body="Test body content",
        )
        assert result is False

    def test_email_format_validation(self):
        """Test email format validation."""
        service = EmailService()
        assert service._is_valid_email("user@example.com") is True
        assert service._is_valid_email("user.name@example.co.uk") is True
        assert service._is_valid_email("invalid@") is False
        assert service._is_valid_email("invalid.email") is False


class TestIntentClassifier:
    """Test intent classification."""

    @pytest.mark.asyncio
    async def test_priority_determination(self):
        """Test priority determination based on category."""
        classifier = IntentClassifier()
        assert classifier._determine_priority("complaint") == "high"
        assert classifier._determine_priority("billing") == "high"
        assert classifier._determine_priority("technical_support") == "high"
        assert classifier._determine_priority("general_inquiry") == "normal"
        assert classifier._determine_priority("feature_request") == "low"
        assert classifier._determine_priority("unknown") == "normal"


class TestHumanReviewRouter:
    """Test human review routing logic."""

    @pytest.mark.asyncio
    async def test_escalate_complaint(self):
        """Test that complaints are escalated to human review."""
        router = HumanReviewRouter()
        state = {
            "classification": {"category": "complaint", "confidence": 0.9},
            "priority": "high",
            "knowledge_base_results": {"found_relevant_docs": True},
            "error": None,
        }
        assert router._should_route_to_human(state) is True

    @pytest.mark.asyncio
    async def test_escalate_low_confidence(self):
        """Test that low confidence classifications are escalated."""
        router = HumanReviewRouter()
        state = {
            "classification": {"category": "general_inquiry", "confidence": 0.4},
            "priority": "normal",
            "knowledge_base_results": {"found_relevant_docs": True},
            "error": None,
        }
        assert router._should_route_to_human(state) is True

    @pytest.mark.asyncio
    async def test_escalate_no_documentation(self):
        """Test that emails with no relevant documentation are escalated."""
        router = HumanReviewRouter()
        state = {
            "classification": {"category": "technical_support", "confidence": 0.9},
            "priority": "high",
            "knowledge_base_results": {"found_relevant_docs": False},
            "error": None,
        }
        assert router._should_route_to_human(state) is True


class TestAPIEndpoints:
    """Test API endpoints."""

    def test_process_email_endpoint(self):
        """Test email processing endpoint."""
        client = TestClient(app)
        response = client.post(
            "/api/v1/emails/process",
            json={
                "sender": "customer@example.com",
                "subject": "Help with my account",
                "body": "I cannot login to my account. Can you help?",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "email_id" in data
        assert "status" in data
        assert data["status"] in ["completed", "pending_review"]

    def test_process_email_invalid_sender(self):
        """Test email processing with invalid sender."""
        client = TestClient(app)
        response = client.post(
            "/api/v1/emails/process",
            json={
                "sender": "invalid-email",
                "subject": "Help",
                "body": "I need help",
            },
        )
        # Should still process but with error
        assert response.status_code == 200

    def test_get_stats_endpoint(self):
        """Test statistics endpoint."""
        client = TestClient(app)
        response = client.get("/api/v1/stats")
        assert response.status_code == 200
        data = response.json()
        assert "total_emails" in data
        assert "sent_emails" in data
        assert "pending_review" in data
        assert "with_errors" in data
        assert "by_category" in data

    def test_get_nonexistent_email(self):
        """Test getting non-existent email."""
        client = TestClient(app)
        response = client.get("/api/v1/emails/nonexistent_id")
        assert response.status_code == 404


class TestWorkflowIntegration:
    """Test workflow integration."""

    @pytest.mark.asyncio
    async def test_workflow_state_initialization(self):
        """Test that workflow state initializes correctly."""
        from src.graph.workflow import EmailProcessingState

        state: EmailProcessingState = {
            "email_id": "test_id",
            "sender": "test@example.com",
            "subject": "Test",
            "body": "Test body",
            "classification": {},
            "extracted_entities": {},
            "knowledge_base_results": {},
            "draft_response": "",
            "requires_human_review": False,
            "priority": "normal",
            "final_response": "",
            "sent": False,
            "follow_up_scheduled": False,
            "error": None,
        }
        assert state["email_id"] == "test_id"
        assert state["priority"] == "normal"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
