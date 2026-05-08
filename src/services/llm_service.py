"""LLM Service for Interfacing with Language Models"""

from src.core.config import settings
from src.core.logger import setup_logger
from src.prompts.templates import (
    SYSTEM_PROMPT,
    EMAIL_CLASSIFICATION_PROMPT,
    SENTIMENT_ANALYSIS_PROMPT,
)

logger = setup_logger(__name__)


class LLMService:
    """Service for LLM interactions and prompt management."""

    def __init__(self):
        """Initialize LLM service."""
        self.model = None
        self._initialized = False
        self._init_error = None
        self._init_model()

    def _init_model(self):
        """Initialize the model (lazy loading)."""
        try:
            from langchain_openai import ChatOpenAI

            self.model = ChatOpenAI(
                api_key=settings.openai_api_key,
                model_name=settings.openai_model,
                temperature=0.7,
            )
            self._initialized = True
            logger.info(f"Initialized LLM with model: {settings.openai_model}")
        except Exception as e:
            logger.warning(f"LLM initialization deferred: {str(e)}")
            self._init_error = str(e)
            self._initialized = False

    async def generate_response(self, prompt: str) -> str:
        """Generate response using LLM.

        Args:
            prompt: Prompt to send to LLM

        Returns:
            Generated response text
        """
        logger.info("Generating LLM response")

        try:
            if not self.model:
                logger.warning("LLM not initialized, returning default response")
                return "Thank you for your inquiry. We will address your concern shortly."

            from langchain.schema import HumanMessage, SystemMessage

            messages = [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=prompt),
            ]

            response = self.model.invoke(messages)
            return response.content

        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return "Thank you for reaching out. We will assist you shortly."

    async def classify_email(self, email_content: str) -> dict:
        """Classify email into categories.

        Args:
            email_content: Email content to classify

        Returns:
            Classification result with category and confidence
        """
        logger.info("Classifying email")

        try:
            if not self.model:
                logger.warning("LLM not initialized, returning default classification")
                return {"category": "general", "confidence": 0.5}

            prompt = EMAIL_CLASSIFICATION_PROMPT.format(email_content=email_content)

            messages = [HumanMessage(content=prompt)]
            response = self.model.invoke(messages)
            category = response.content.strip().lower().replace("_", " ")

            categories = [
                "billing",
                "technical support",
                "general inquiry",
                "complaint",
                "feature request",
                "other",
            ]

            if any(cat in category for cat in categories):
                matched_category = next(
                    (cat.replace(" ", "_") for cat in categories if cat in category),
                    "general",
                )
            else:
                matched_category = "general"

            return {
                "category": matched_category,
                "confidence": 0.8,
                "raw_response": response.content,
            }

        except Exception as e:
            logger.error(f"Error classifying email: {str(e)}")
            return {"category": "general", "confidence": 0.0, "error": str(e)}

    async def extract_entities(self, text: str) -> dict:
        """Extract entities from email text.

        Args:
            text: Text to extract entities from

        Returns:
            Extracted entities
        """
        logger.info("Extracting entities from text")

        try:
            if not self.model:
                return {}

            prompt = f"Extract key entities (names, dates, amounts) from: {text[:500]}"
            messages = [HumanMessage(content=prompt)]
            response = self.model.invoke(messages)

            return {
                "raw_extraction": response.content,
                "success": True,
            }

        except Exception as e:
            logger.error(f"Error extracting entities: {str(e)}")
            return {"error": str(e)}

    async def analyze_sentiment(self, text: str) -> dict:
        """Analyze sentiment of text.

        Args:
            text: Text to analyze

        Returns:
            Sentiment analysis result
        """
        logger.info("Analyzing sentiment")

        try:
            if not self.model:
                return {"sentiment": "neutral", "confidence": 0.5}

            prompt = SENTIMENT_ANALYSIS_PROMPT.format(email_content=text)
            messages = [HumanMessage(content=prompt)]
            response = self.model.invoke(messages)
            sentiment = response.content.strip().lower()

            valid_sentiments = ["positive", "negative", "neutral"]
            if sentiment not in valid_sentiments:
                sentiment = "neutral"

            return {"sentiment": sentiment, "confidence": 0.8}

        except Exception as e:
            logger.error(f"Error analyzing sentiment: {str(e)}")
            return {"sentiment": "neutral", "confidence": 0.0}
