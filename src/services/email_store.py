"""In-Memory Email Store Service"""

from datetime import datetime
from typing import Optional

from src.core.logger import setup_logger

logger = setup_logger(__name__)


class EmailStore:
    """In-memory store for processed emails."""

    _instance = None
    _emails = {}
    _counter = 0

    def __new__(cls):
        """Singleton pattern for email store."""
        if cls._instance is None:
            cls._instance = super(EmailStore, cls).__new__(cls)
        return cls._instance

    def store_email(self, email_data: dict, processing_result: dict) -> str:
        """Store email with processing result.

        Args:
            email_data: Original email data
            processing_result: Processing result from workflow

        Returns:
            Email ID
        """
        try:
            self._counter += 1
            email_id = f"email_{self._counter:06d}"

            stored_email = {
                "id": email_id,
                "sender": email_data.get("sender"),
                "subject": email_data.get("subject"),
                "body": email_data.get("body"),
                "timestamp": datetime.utcnow().isoformat(),
                "status": processing_result.get("status"),
                "category": processing_result.get("metadata", {}).get("category"),
                "priority": processing_result.get("metadata", {}).get("priority"),
                "sent": processing_result.get("metadata", {}).get("sent"),
                "requires_human_review": processing_result.get("metadata", {}).get(
                    "requires_human_review"
                ),
                "follow_up_scheduled": processing_result.get("metadata", {}).get(
                    "follow_up_scheduled"
                ),
                "error": processing_result.get("error"),
                "full_result": processing_result,
            }

            self._emails[email_id] = stored_email
            logger.info(f"Stored email: {email_id}")

            return email_id

        except Exception as e:
            logger.error(f"Error storing email: {str(e)}")
            raise

    def get_email(self, email_id: str) -> Optional[dict]:
        """Get email by ID.

        Args:
            email_id: Email ID

        Returns:
            Email data or None if not found
        """
        return self._emails.get(email_id)

    def get_all_emails(self, limit: int = 50, offset: int = 0) -> list[dict]:
        """Get all emails with pagination.

        Args:
            limit: Maximum number of emails
            offset: Offset for pagination

        Returns:
            List of emails
        """
        all_emails = list(self._emails.values())
        all_emails.sort(key=lambda x: x["timestamp"], reverse=True)

        return all_emails[offset : offset + limit]

    def get_emails_by_status(self, status: str) -> list[dict]:
        """Get emails filtered by status.

        Args:
            status: Email status (completed, pending_review, etc)

        Returns:
            List of matching emails
        """
        return [
            email
            for email in self._emails.values()
            if email.get("status") == status
        ]

    def get_emails_by_category(self, category: str) -> list[dict]:
        """Get emails filtered by category.

        Args:
            category: Email category

        Returns:
            List of matching emails
        """
        return [
            email
            for email in self._emails.values()
            if email.get("category") == category
        ]

    def get_statistics(self) -> dict:
        """Get email statistics.

        Returns:
            Statistics dictionary
        """
        total = len(self._emails)
        sent = sum(1 for e in self._emails.values() if e.get("sent"))
        pending_review = sum(1 for e in self._emails.values() if e.get("requires_human_review"))
        errors = sum(1 for e in self._emails.values() if e.get("error"))

        categories = {}
        for email in self._emails.values():
            cat = email.get("category", "unknown")
            categories[cat] = categories.get(cat, 0) + 1

        return {
            "total_emails": total,
            "sent_emails": sent,
            "pending_review": pending_review,
            "with_errors": errors,
            "by_category": categories,
        }

    def clear_all(self) -> None:
        """Clear all emails (for testing)."""
        self._emails = {}
        self._counter = 0
        logger.info("Cleared all emails")