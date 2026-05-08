"""Intent Classification Node for LangGraph Workflow"""

from src.core.logger import setup_logger
from src.services.llm_service import LLMService
from src.prompts.templates import EMAIL_CLASSIFICATION_PROMPT

logger = setup_logger(__name__)


class IntentClassifier:
    """Node for classifying email intent and category."""

    def __init__(self):
        """Initialize intent classifier."""
        self.llm_service = LLMService()
        logger.info("IntentClassifier initialized")

    async def classify(self, state: dict) -> dict:
        """Classify email intent and category.

        Args:
            state: Workflow state

        Returns:
            Updated state with classification
        """
        if state.get("error"):
            logger.warning(f"Skipping classification due to error: {state['error']}")
            return state

        logger.info(f"Classifying email: {state.get('email_id')}")

        try:
            email_content = f"Subject: {state.get('subject')}\n\n{state.get('body')}"

            classification = await self.llm_service.classify_email(email_content)

            state["classification"] = {
                "category": classification.get("category", "general"),
                "confidence": classification.get("confidence", 0.0),
                "priority": self._determine_priority(classification.get("category")),
            }

            state["priority"] = state["classification"]["priority"]

            logger.info(
                f"Email classified as: {state['classification']['category']} "
                f"(confidence: {state['classification']['confidence']})"
            )

        except Exception as e:
            logger.error(f"Error classifying email: {str(e)}")
            state["error"] = f"Classification failed: {str(e)}"
            state["classification"] = {"category": "general", "confidence": 0.0, "priority": "normal"}

        return state

    def _determine_priority(self, category: str) -> str:
        """Determine priority based on category.

        Args:
            category: Email category

        Returns:
            Priority level (high, normal, low)
        """
        priority_map = {
            "complaint": "high",
            "billing": "high",
            "technical_support": "high",
            "feature_request": "low",
            "general_inquiry": "normal",
        }
        return priority_map.get(category, "normal")