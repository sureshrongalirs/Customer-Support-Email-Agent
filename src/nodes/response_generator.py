"""Response Generation Node for LangGraph Workflow"""

from src.core.logger import setup_logger
from src.services.llm_service import LLMService
from src.prompts.templates import EMAIL_RESPONSE_GENERATION_PROMPT

logger = setup_logger(__name__)


class ResponseGenerator:
    """Node for generating email responses."""

    def __init__(self):
        """Initialize response generator."""
        self.llm_service = LLMService()
        logger.info("ResponseGenerator initialized")

    async def generate(self, state: dict) -> dict:
        """Generate response to customer email.

        Args:
            state: Workflow state

        Returns:
            Updated state with draft response
        """
        if state.get("error"):
            logger.warning(f"Skipping response generation due to error: {state['error']}")
            return state

        logger.info(f"Generating response for: {state.get('email_id')}")

        try:
            kb_results = state.get("knowledge_base_results", {})
            relevant_info = self._format_kb_results(kb_results)

            prompt = EMAIL_RESPONSE_GENERATION_PROMPT.format(
                email_body=state.get("body", ""),
                thread_history="",
                relevant_documentation=relevant_info,
                category=state.get("classification", {}).get("category", "general"),
            )

            response = await self.llm_service.generate_response(prompt)

            state["draft_response"] = response
            logger.info(f"Response generated for: {state.get('email_id')}")

        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            state["error"] = f"Response generation failed: {str(e)}"
            state["draft_response"] = self._generate_fallback_response(state)

        return state

    def _format_kb_results(self, kb_results: dict) -> str:
        """Format knowledge base results for prompt.

        Args:
            kb_results: Knowledge base search results

        Returns:
            Formatted string of relevant information
        """
        if not kb_results.get("found_relevant_docs"):
            return "No relevant documentation found."

        results = kb_results.get("results", [])
        if not results:
            return "No relevant documentation found."

        formatted = "Relevant Documentation:\n"
        for i, result in enumerate(results[:3], 1):
            formatted += f"\n{i}. From {result.get('file')}:\n"
            formatted += f"   {result.get('excerpt', '')}\n"

        return formatted

    def _generate_fallback_response(self, state: dict) -> str:
        """Generate fallback response when LLM fails.

        Args:
            state: Workflow state

        Returns:
            Fallback response text
        """
        category = state.get("classification", {}).get("category", "general")
        sender = state.get("sender", "Valued Customer")

        fallback_responses = {
            "billing": (
                f"Thank you for reaching out about your billing inquiry. "
                f"We take your concern seriously. Please provide more details about your issue, "
                f"and we'll resolve it promptly."
            ),
            "technical_support": (
                f"Thank you for reporting this technical issue. "
                f"Our support team is here to help. Could you provide more details about the error? "
                f"This will help us assist you more effectively."
            ),
            "complaint": (
                f"We sincerely apologize for the issue you experienced. "
                f"Your feedback is important to us. We're committed to making this right. "
                f"Our team will investigate this matter immediately."
            ),
            "feature_request": (
                f"Thank you for your feature suggestion. "
                f"We value your input and will consider this for future updates."
            ),
        }

        return fallback_responses.get(
            category,
            (
                f"Thank you for contacting us. "
                f"We'll review your message and get back to you shortly with assistance."
            ),
        )