"""Test Routes - Simplified Email Processing Without Heavy Dependencies"""

from fastapi import APIRouter
from datetime import datetime

from src.core.logger import setup_logger
from src.schemas.email import EmailRequest, ProcessingResult
from src.utils.helpers import generate_email_id
from src.services.email_store import EmailStore

logger = setup_logger(__name__)

router = APIRouter(prefix="/api/v1", tags=["emails"])
email_store = EmailStore()


@router.post("/emails/process", response_model=ProcessingResult)
async def process_email_simple(email: EmailRequest) -> ProcessingResult:
    """Simplified email processing for testing.

    Args:
        email: Email request

    Returns:
        Processing result
    """
    email_id = generate_email_id()
    logger.info(f"Processing email {email_id} from {email.sender}")

    try:
        # Simple classification based on keywords
        subject_lower = email.subject.lower()
        body_lower = email.body.lower()
        combined = f"{subject_lower} {body_lower}"

        category = "general_inquiry"
        priority = "normal"
        requires_review = False

        # Simple keyword-based classification
        if any(word in combined for word in ["login", "password", "access", "account"]):
            category = "technical_support"
            priority = "high"

        elif any(word in combined for word in ["charge", "billing", "payment", "refund", "money"]):
            category = "billing"
            priority = "high"
            requires_review = True

        elif any(word in combined for word in ["crash", "bug", "error", "broken", "not working"]):
            category = "technical_support"
            priority = "high"

        elif any(word in combined for word in ["terrible", "awful", "hate", "complaint", "angry", "upset"]):
            category = "complaint"
            priority = "high"
            requires_review = True

        elif any(word in combined for word in ["feature", "request", "suggest", "idea"]):
            category = "feature_request"
            priority = "low"

        # Generate simple response
        responses = {
            "technical_support": "Thank you for reporting this technical issue. Our support team is investigating and will resolve this shortly.",
            "billing": "We appreciate you bringing this to our attention. Our billing team will review your account and contact you within 24 hours.",
            "complaint": "We sincerely apologize for the experience you had. A manager will contact you shortly to make this right.",
            "feature_request": "Thank you for your excellent suggestion! We'll consider this for future updates.",
            "general_inquiry": "Thank you for your inquiry. We'll get back to you with the information you need shortly.",
        }

        draft_response = responses.get(category, responses["general_inquiry"])

        result = ProcessingResult(
            email_id=email_id,
            status="pending_review" if requires_review else "completed",
            response=None,
            error=None,
            metadata={
                "category": category,
                "priority": priority,
                "sent": not requires_review,
                "requires_human_review": requires_review,
                "follow_up_scheduled": True,
            },
        )

        # Store email
        email_store.store_email(
            {
                "sender": email.sender,
                "subject": email.subject,
                "body": email.body,
            },
            result.dict() if hasattr(result, "dict") else result,
        )

        logger.info(f"Email {email_id} processed: {category}")
        return result

    except Exception as e:
        logger.error(f"Error processing email: {str(e)}")
        raise