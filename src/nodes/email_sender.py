"""Email Sender Node for LangGraph Workflow"""

from src.core.logger import setup_logger
from src.services.email_service import EmailService
from src.schemas.email import EmailResponse

logger = setup_logger(__name__)


class EmailSender:
    """Node for sending final email responses."""

    def __init__(self):
        """Initialize email sender."""
        self.email_service = EmailService()
        logger.info("EmailSender initialized")

    async def send(self, state: dict) -> dict:
        """Send email response to customer.

        Args:
            state: Workflow state

        Returns:
            Updated state with send status
        """
        if state.get("requires_human_review"):
            logger.info(f"Skipping send - email pending human review: {state.get('email_id')}")
            state["sent"] = False
            return state

        logger.info(f"Sending email response: {state.get('email_id')}")

        try:
            response = EmailResponse(
                recipient=state.get("sender", ""),
                subject=f"Re: {state.get('subject', 'Your Inquiry')}",
                body=state.get("draft_response", ""),
            )

            if not response.recipient:
                raise ValueError("Recipient email address is missing")

            success = await self.email_service.send_email(response)

            if success:
                state["sent"] = True
                state["final_response"] = response.body
                logger.info(f"Email sent successfully to {response.recipient}")
            else:
                state["sent"] = False
                logger.error(f"Failed to send email to {response.recipient}")
                state["error"] = "Failed to send email"

        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            state["sent"] = False
            state["error"] = f"Email sending failed: {str(e)}"

        return state