"""Follow-up Scheduler Node for LangGraph Workflow"""

from datetime import datetime, timedelta

from src.core.logger import setup_logger

logger = setup_logger(__name__)


class FollowupScheduler:
    """Node for scheduling follow-up emails."""

    def __init__(self):
        """Initialize follow-up scheduler."""
        logger.info("FollowupScheduler initialized")

    async def schedule(self, state: dict) -> dict:
        """Schedule follow-up for email if needed.

        Args:
            state: Workflow state

        Returns:
            Updated state with follow-up schedule
        """
        logger.info(f"Evaluating follow-up scheduling: {state.get('email_id')}")

        try:
            needs_followup = self._should_schedule_followup(state)

            if needs_followup:
                followup_schedule = self._create_followup_schedule(state)
                state["follow_up_scheduled"] = True
                state["followup_schedule"] = followup_schedule
                logger.info(
                    f"Follow-up scheduled for {state.get('email_id')}: "
                    f"{followup_schedule.get('scheduled_for')}"
                )
            else:
                state["follow_up_scheduled"] = False
                logger.info(f"No follow-up needed for: {state.get('email_id')}")

        except Exception as e:
            logger.error(f"Error scheduling follow-up: {str(e)}")
            state["follow_up_scheduled"] = False
            state["error"] = f"Follow-up scheduling failed: {str(e)}"

        return state

    def _should_schedule_followup(self, state: dict) -> bool:
        """Determine if follow-up should be scheduled.

        Args:
            state: Workflow state

        Returns:
            True if follow-up should be scheduled
        """
        if state.get("error"):
            return True

        if state.get("requires_human_review"):
            return True

        category = state.get("classification", {}).get("category", "")
        if category == "technical_support":
            return True

        if category == "billing":
            return True

        if state.get("priority") == "high":
            return True

        return False

    def _create_followup_schedule(self, state: dict) -> dict:
        """Create follow-up schedule for email.

        Args:
            state: Workflow state

        Returns:
            Follow-up schedule details
        """
        category = state.get("classification", {}).get("category", "")
        priority = state.get("priority", "normal")

        followup_delay_hours = self._get_followup_delay(category, priority)

        scheduled_for = datetime.utcnow() + timedelta(hours=followup_delay_hours)

        return {
            "email_id": state.get("email_id"),
            "scheduled_for": scheduled_for.isoformat(),
            "delay_hours": followup_delay_hours,
            "followup_type": self._get_followup_type(category),
            "priority": priority,
            "notes": self._get_followup_notes(state),
        }

    def _get_followup_delay(self, category: str, priority: str) -> int:
        """Get follow-up delay in hours.

        Args:
            category: Email category
            priority: Email priority

        Returns:
            Hours until follow-up
        """
        if priority == "high":
            return 4

        delay_map = {
            "technical_support": 24,
            "billing": 48,
            "complaint": 12,
            "feature_request": 168,
            "general_inquiry": 72,
        }

        return delay_map.get(category, 48)

    def _get_followup_type(self, category: str) -> str:
        """Get type of follow-up.

        Args:
            category: Email category

        Returns:
            Follow-up type
        """
        followup_map = {
            "technical_support": "solution_check",
            "billing": "verification",
            "complaint": "satisfaction_check",
            "feature_request": "acknowledgment",
            "general_inquiry": "confirmation",
        }

        return followup_map.get(category, "status_check")

    def _get_followup_notes(self, state: dict) -> str:
        """Get notes for follow-up.

        Args:
            state: Workflow state

        Returns:
            Follow-up notes
        """
        if state.get("requires_human_review"):
            return f"Check human review status. Reason: {state.get('human_review_reason')}"

        category = state.get("classification", {}).get("category", "")
        if category == "technical_support":
            return "Verify technical issue is resolved"

        if category == "billing":
            return "Verify billing issue is resolved"

        if category == "complaint":
            return "Check customer satisfaction with resolution"

        return "Follow up on customer inquiry"