"""Knowledge Base Search Node using FAISS for LangGraph Workflow"""

from src.core.config import settings
from src.core.logger import setup_logger
from src.services.faiss_service import FAISSKnowledgeBase

logger = setup_logger(__name__)


class KnowledgeBaseSearch:
    """Node for searching knowledge base documents using FAISS semantic search."""

    def __init__(self):
        """Initialize knowledge base search with FAISS."""
        self.faiss_kb = None
        self.index_built = False
        self._init_faiss()

    def _init_faiss(self):
        """Initialize FAISS (lazy loading)."""
        try:
            self.faiss_kb = FAISSKnowledgeBase(model_name="all-MiniLM-L6-v2")

            if not self.faiss_kb.load_index():
                logger.warning("FAISS index not found. Index will be built on first search.")
                self.index_built = False
            else:
                self.index_built = True
                stats = self.faiss_kb.get_index_stats()
                logger.info(f"Loaded FAISS index: {stats['total_documents']} documents")
        except Exception as e:
            logger.warning(f"FAISS initialization deferred: {str(e)}")
            self.faiss_kb = None
            self.index_built = False

    async def search(self, state: dict) -> dict:
        """Search knowledge base using FAISS semantic similarity.

        Args:
            state: Workflow state

        Returns:
            Updated state with search results
        """
        if state.get("error"):
            logger.warning(f"Skipping KB search due to error: {state['error']}")
            return state

        logger.info(f"Searching FAISS knowledge base for: {state.get('email_id')}")

        try:
            if self.faiss_kb is None:
                logger.warning("FAISS not initialized, using empty results")
                results = []
            else:
                query = self._build_search_query(state)
                results = self.faiss_kb.search(
                    query,
                    top_k=5,
                    threshold=0.5,
                )

            formatted_results = self._format_results(results)

            state["knowledge_base_results"] = {
                "query": query,
                "results": formatted_results,
                "found_relevant_docs": len(formatted_results) > 0,
                "search_method": "faiss_semantic",
            }

            logger.info(f"Found {len(formatted_results)} relevant documents")

        except Exception as e:
            logger.error(f"Error searching FAISS knowledge base: {str(e)}")
            state["knowledge_base_results"] = {
                "query": "",
                "results": [],
                "found_relevant_docs": False,
                "error": str(e),
                "search_method": "faiss_semantic",
            }

        return state

    def _build_search_query(self, state: dict) -> str:
        """Build search query from email content.

        Args:
            state: Workflow state

        Returns:
            Search query string
        """
        category = state.get("classification", {}).get("category", "")
        subject = state.get("subject", "")
        body = state.get("body", "")

        priority = state.get("priority", "")

        query_parts = [part for part in [category, subject, body, priority] if part]
        query = " ".join(query_parts)

        return query[:500]

    def _format_results(self, results: list[dict]) -> list[dict]:
        """Format FAISS search results for response.

        Args:
            results: Raw FAISS results

        Returns:
            Formatted results
        """
        formatted = []

        for result in results:
            excerpt = result.get("content", "")[:300]

            formatted_result = {
                "id": result.get("id"),
                "title": result.get("title"),
                "category": result.get("category"),
                "similarity_score": result.get("similarity_score", 0.0),
                "excerpt": excerpt,
                "full_content": result.get("content", ""),
            }

            formatted.append(formatted_result)

        return formatted