"""Email Parsing Node for LangGraph Workflow"""

from src.core.logger import setup_logger
from src.services.email_service import EmailService

logger = setup_logger(__name__)


class EmailProcessor:
    """Node for parsing and validating incoming emails."""

    def __init__(self):
        """Initialize email processor."""
        self.email_service = EmailService()
        logger.info("EmailProcessor initialized")

    async def parse(self, state: dict) -> dict:
        """Parse and validate email.

        Args:
            state: Workflow state containing email data

        Returns:
            Updated state with parsed email
        """
        logger.info(f"Parsing email from {state.get('sender')}")

        try:
            is_valid = await self.email_service.validate_email(
                sender=state.get("sender"),
                subject=state.get("subject"),
                body=state.get("body"),
            )

            if not is_valid:
                state["error"] = "Invalid email format"
                logger.warning(f"Invalid email: {state.get('email_id')}")
                return state

            state["extracted_entities"] = await self.extract_key_info(
                state.get("body", "")
            )
            logger.info(f"Email parsed successfully: {state.get('email_id')}")

        except Exception as e:
            logger.error(f"Error parsing email: {str(e)}")
            state["error"] = str(e)

        return state

    async def extract_key_info(self, email_body: str) -> dict:
        """Extract key information from email body.

        Args:
            email_body: Email body text

        Returns:
            Extracted key information
        """
        return {
            "customer_name": "",
            "account_id": "",
            "issue_description": email_body,
        }
