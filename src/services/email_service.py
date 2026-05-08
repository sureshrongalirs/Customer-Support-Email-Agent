"""Email Service for Handling Email Operations"""

import re

from src.core.config import settings
from src.core.logger import setup_logger
from src.schemas.email import EmailResponse

logger = setup_logger(__name__)


class EmailService:
    """Service for email handling and operations."""

    def __init__(self):
        """Initialize email service."""
        logger.info("Initializing EmailService")
        self.email_threads = {}

    async def send_email(self, response: EmailResponse) -> bool:
        """Send email response to customer.

        Args:
            response: Email response to send

        Returns:
            True if email sent successfully, False otherwise
        """
        try:
            logger.info(f"Sending email to {response.recipient}")

            if not self._is_valid_email(response.recipient):
                logger.error(f"Invalid recipient email: {response.recipient}")
                return False

            if settings.smtp_server and settings.smtp_username:
                success = await self._send_via_smtp(response)
            else:
                logger.warning("SMTP not configured, simulating email send")
                success = True

            if success:
                logger.info(f"Email sent successfully to {response.recipient}")
            else:
                logger.error(f"Failed to send email to {response.recipient}")

            return success

        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return False

    async def validate_email(self, sender: str, subject: str, body: str) -> bool:
        """Validate incoming email.

        Args:
            sender: Sender email address
            subject: Email subject
            body: Email body

        Returns:
            True if email is valid, False otherwise
        """
        try:
            logger.info(f"Validating email from {sender}")

            if not self._is_valid_email(sender):
                logger.warning(f"Invalid sender email: {sender}")
                return False

            if not subject or not subject.strip():
                logger.warning("Email subject is empty")
                return False

            if not body or not body.strip():
                logger.warning("Email body is empty")
                return False

            return True

        except Exception as e:
            logger.error(f"Error validating email: {str(e)}")
            return False

    async def get_email_thread(self, email_id: str) -> list:
        """Get email thread history.

        Args:
            email_id: ID of the email

        Returns:
            List of messages in the thread
        """
        logger.info(f"Retrieving email thread for {email_id}")
        return self.email_threads.get(email_id, [])

    async def store_email_thread(self, email_id: str, messages: list) -> None:
        """Store email thread.

        Args:
            email_id: ID of the email
            messages: List of messages in thread
        """
        logger.info(f"Storing email thread for {email_id}")
        self.email_threads[email_id] = messages

    def _is_valid_email(self, email: str) -> bool:
        """Validate email format.

        Args:
            email: Email address

        Returns:
            True if valid email format
        """
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    async def _send_via_smtp(self, response: EmailResponse) -> bool:
        """Send email via SMTP.

        Args:
            response: Email response

        Returns:
            True if sent successfully
        """
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart

            msg = MIMEMultipart()
            msg["From"] = settings.smtp_username
            msg["To"] = response.recipient
            msg["Subject"] = response.subject

            msg.attach(MIMEText(response.body, "plain"))

            with smtplib.SMTP(settings.smtp_server, settings.smtp_port) as server:
                server.starttls()
                server.login(settings.smtp_username, settings.smtp_password)
                server.send_message(msg)

            logger.info(f"Email sent via SMTP to {response.recipient}")
            return True

        except Exception as e:
            logger.error(f"Error sending via SMTP: {str(e)}")
            return False
