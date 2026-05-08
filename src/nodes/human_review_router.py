"""Human Review Router Node for LangGraph Workflow"""

from src.core.logger import setup_logger

logger = setup_logger(__name__)


class HumanReviewRouter:
    """Node for routing emails to human review when necessary."""

    def __init__(self):
        """Initialize human review router."""
        logger.info("HumanReviewRouter initialized")

    async def route(self, state: dict) -> dict:
        """Route email to human review if needed.

        Args:
            state: Workflow state

        Returns:
            Updated state with human review decision
        """
        logger.info(f"Evaluating human review requirement: {state.get('email_id')}")

        try:
            requires_review = self._should_route_to_human(state)
            state["requires_human_review"] = requires_review

            if requires_review:
                reason = self._get_review_reason(state)
                logger.info(f"Email routed to human review: {reason}")
                state["human_review_reason"] = reason
            else:
                logger.info(f"Email ready for automated sending")

        except Exception as e:
            logger.error(f"Error in human review routing: {str(e)}")
            state["requires_human_review"] = True
            state["human_review_reason"] = "Error occurred during processing"

        return state

    def _should_route_to_human(self, state: dict) -> bool:
        """Determine if email should be routed to human.

        Args:
            state: Workflow state

        Returns:
            True if human review is needed
        """
        if state.get("error"):
            return True

        priority = state.get("priority", "normal")
        if priority == "high":
            return self._should_escalate_high_priority(state)

        if not state.get("knowledge_base_results", {}).get("found_relevant_docs"):
            return True

        classification_confidence = (
            state.get("classification", {}).get("confidence", 0.0)
        )
        if classification_confidence < 0.6:
            return True

        category = state.get("classification", {}).get("category", "")
        if category in ["complaint", "other"]:
            return True

        return False

    def _should_escalate_high_priority(self, state: dict) -> bool:
        """Determine if high-priority email needs human review.

        Args:
            state: Workflow state

        Returns:
            True if human review needed
        """
        category = state.get("classification", {}).get("category", "")

        if category == "complaint":
            return True

        if category == "billing":
            body_lower = state.get("body", "").lower()
            keywords = ["refund", "charge", "payment", "fraud", "unauthorized"]
            if any(keyword in body_lower for keyword in keywords):
                return True

        if category == "technical_support":
            if not state.get("knowledge_base_results", {}).get("found_relevant_docs"):
                return True

        return False

    def _get_review_reason(self, state: dict) -> str:
        """Get reason for human review routing.

        Args:
            state: Workflow state

        Returns:
            Reason for review
        """
        if state.get("error"):
            return f"Processing error: {state['error']}"

        priority = state.get("priority", "normal")
        if priority == "high":
            return "High priority email requiring human attention"

        if not state.get("knowledge_base_results", {}).get("found_relevant_docs"):
            return "No relevant documentation found - needs human expertise"

        classification_confidence = (
            state.get("classification", {}).get("confidence", 0.0)
        )
        if classification_confidence < 0.6:
            return f"Low classification confidence ({classification_confidence:.1%})"

        category = state.get("classification", {}).get("category", "")
        if category == "complaint":
            return "Customer complaint requires human review"

        if category == "other":
            return "Unknown category - needs human review"

        return "Flagged for quality assurance"