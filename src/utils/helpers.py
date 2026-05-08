"""Utility Helper Functions"""

import uuid
from datetime import datetime
from typing import Any

from src.core.logger import setup_logger

logger = setup_logger(__name__)


def generate_email_id() -> str:
    """Generate unique email ID.

    Returns:
        Unique email identifier
    """
    return f"email_{uuid.uuid4().hex[:12]}"


def format_timestamp(dt: datetime) -> str:
    """Format datetime to ISO format string.

    Args:
        dt: Datetime object

    Returns:
        Formatted timestamp string
    """
    return dt.isoformat()


def parse_email_content(raw_email: str) -> dict[str, str]:
    """Parse raw email content into components.

    Args:
        raw_email: Raw email content

    Returns:
        Parsed email components
    """
    return {
        "sender": "",
        "subject": "",
        "body": "",
    }


def truncate_text(text: str, max_length: int = 1000) -> str:
    """Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def safe_get(data: dict, key: str, default: Any = None) -> Any:
    """Safely get value from dictionary.

    Args:
        data: Dictionary to access
        key: Key to retrieve
        default: Default value if key not found

    Returns:
        Value from dictionary or default
    """
    return data.get(key, default)
