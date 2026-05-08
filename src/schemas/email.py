"""Email-related Pydantic Models"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class EmailRequest(BaseModel):
    """Email request from customer."""

    sender: EmailStr
    subject: str
    body: str
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)


class EmailResponse(BaseModel):
    """Response to be sent to customer."""

    recipient: EmailStr
    subject: str
    body: str
    generated_at: datetime = Field(default_factory=datetime.utcnow)


class EmailThreadMessage(BaseModel):
    """Individual message in email thread."""

    role: str
    content: str
    timestamp: datetime


class EmailContext(BaseModel):
    """Complete email context for processing."""

    email_id: str
    original_email: EmailRequest
    thread: list[EmailThreadMessage] = Field(default_factory=list)
    category: Optional[str] = None
    priority: Optional[str] = None


class ProcessingResult(BaseModel):
    """Result of email processing."""

    email_id: str
    status: str
    response: Optional[EmailResponse] = None
    error: Optional[str] = None
    metadata: Optional[dict] = Field(default_factory=dict)
