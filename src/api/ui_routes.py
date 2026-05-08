"""UI Routes for Web Interface"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from src.core.logger import setup_logger
from src.services.email_store import EmailStore

logger = setup_logger(__name__)

router = APIRouter(tags=["ui"])
email_store = EmailStore()


@router.get("/inbox")
async def get_inbox(limit: int = 50, offset: int = 0) -> dict:
    """Get inbox emails with pagination.

    Args:
        limit: Maximum number of emails
        offset: Offset for pagination

    Returns:
        List of inbox emails
    """
    try:
        emails = email_store.get_all_emails(limit=limit, offset=offset)
        stats = email_store.get_statistics()

        return {
            "emails": emails,
            "total": stats["total_emails"],
            "limit": limit,
            "offset": offset,
        }

    except Exception as e:
        logger.error(f"Error fetching inbox: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch inbox",
        )


@router.get("/inbox/{email_id}")
async def get_email_detail(email_id: str) -> dict:
    """Get detailed email information.

    Args:
        email_id: Email ID

    Returns:
        Email details with processing results
    """
    try:
        email = email_store.get_email(email_id)

        if not email:
            raise HTTPException(
                status_code=404,
                detail=f"Email {email_id} not found",
            )

        return email

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching email details: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch email details",
        )


@router.get("/inbox/stats")
async def get_inbox_stats() -> dict:
    """Get inbox statistics.

    Returns:
        Inbox statistics
    """
    try:
        return email_store.get_statistics()

    except Exception as e:
        logger.error(f"Error fetching statistics: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch statistics",
        )


@router.get("/inbox/filter/status/{status}")
async def get_emails_by_status(status: str) -> dict:
    """Get emails filtered by status.

    Args:
        status: Email status

    Returns:
        Filtered emails
    """
    try:
        emails = email_store.get_emails_by_status(status)

        return {
            "status": status,
            "emails": emails,
            "total": len(emails),
        }

    except Exception as e:
        logger.error(f"Error filtering emails: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to filter emails",
        )


@router.get("/inbox/filter/category/{category}")
async def get_emails_by_category(category: str) -> dict:
    """Get emails filtered by category.

    Args:
        category: Email category

    Returns:
        Filtered emails
    """
    try:
        emails = email_store.get_emails_by_category(category)

        return {
            "category": category,
            "emails": emails,
            "total": len(emails),
        }

    except Exception as e:
        logger.error(f"Error filtering emails: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to filter emails",
        )


def get_ui_router():
    """Get UI router with static files."""
    return router