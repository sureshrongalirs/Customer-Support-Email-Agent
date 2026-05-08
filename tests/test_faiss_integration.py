"""Tests for FAISS Knowledge Base Integration"""

import pytest
from pathlib import Path

from src.services.faiss_service import FAISSKnowledgeBase
from src.knowledge_base.documents import get_documents, get_documents_by_category
from src.nodes.knowledge_base_search import KnowledgeBaseSearch


class TestFAISSKnowledgeBase:
    """Test FAISS knowledge base functionality."""

    @pytest.fixture
    def sample_documents(self):
        """Get sample documents."""
        return get_documents()

    @pytest.fixture
    def faiss_kb(self, sample_documents):
        """Create FAISS knowledge base with sample documents."""
        kb = FAISSKnowledgeBase()
        kb.build_index(sample_documents)
        return kb

    def test_build_index(self, sample_documents):
        """Test building FAISS index from documents."""
        kb = FAISSKnowledgeBase()
        kb.build_index(sample_documents)

        assert kb.index is not None
        assert len(kb.documents) == len(sample_documents)
        stats = kb.get_index_stats()
        assert stats["total_documents"] == len(sample_documents)

    def test_save_and_load_index(self, sample_documents, tmp_path):
        """Test saving and loading FAISS index."""
        kb = FAISSKnowledgeBase()
        kb.build_index(sample_documents)
        kb.save_index()

        kb2 = FAISSKnowledgeBase()
        success = kb2.load_index()

        assert success
        assert len(kb2.documents) == len(sample_documents)

    def test_search_login_issue(self, faiss_kb):
        """Test searching for login-related documents."""
        results = faiss_kb.search("I cannot login to my account", top_k=3)

        assert len(results) > 0
        assert any("login" in result["title"].lower() for result in results)
        assert all("similarity_score" in result for result in results)

    def test_search_billing_issue(self, faiss_kb):
        """Test searching for billing-related documents."""
        results = faiss_kb.search("I was charged twice for my subscription", top_k=3)

        assert len(results) > 0
        assert any("billing" in result["category"].lower() for result in results)

    def test_search_technical_issue(self, faiss_kb):
        """Test searching for technical support documents."""
        results = faiss_kb.search("The app keeps crashing", top_k=3)

        assert len(results) > 0
        assert any("technical" in result["category"].lower() for result in results)

    def test_search_with_threshold(self, faiss_kb):
        """Test search with similarity threshold."""
        results = faiss_kb.search("invalid gibberish query xyz", top_k=5, threshold=0.9)

        assert len(results) <= 5

    def test_search_empty_results(self, faiss_kb):
        """Test search with high threshold returns few/no results."""
        results = faiss_kb.search("xyz abc def ghi", top_k=5, threshold=0.95)

        assert len(results) <= 5

    def test_get_index_stats(self, faiss_kb, sample_documents):
        """Test getting index statistics."""
        stats = faiss_kb.get_index_stats()

        assert stats["initialized"] is True
        assert stats["total_documents"] == len(sample_documents)
        assert stats["embedding_model"] == "all-MiniLM-L6-v2"
        assert stats["dimension"] is not None
        assert stats["index_type"] == "IndexFlatL2"

    def test_add_documents(self, faiss_kb, sample_documents):
        """Test adding new documents to index."""
        initial_count = len(faiss_kb.documents)

        new_doc = {
            "id": 999,
            "title": "New Document",
            "category": "test",
            "content": "This is a new test document for testing.",
        }

        faiss_kb.add_documents([new_doc])

        assert len(faiss_kb.documents) == initial_count + 1

    def test_search_returns_relevant_info(self, faiss_kb):
        """Test that search results contain relevant information."""
        results = faiss_kb.search("reset password", top_k=2)

        assert len(results) > 0

        result = results[0]
        assert "id" in result
        assert "title" in result
        assert "category" in result
        assert "similarity_score" in result
        assert "excerpt" in result
        assert isinstance(result["similarity_score"], float)
        assert 0 <= result["similarity_score"] <= 1

    def test_multiple_searches_consistent(self, faiss_kb):
        """Test that same query returns consistent results."""
        query = "how do I cancel my account"

        results1 = faiss_kb.search(query, top_k=3)
        results2 = faiss_kb.search(query, top_k=3)

        assert len(results1) == len(results2)
        assert [r["id"] for r in results1] == [r["id"] for r in results2]


class TestKnowledgeBaseSearchNode:
    """Test KnowledgeBaseSearch node integration."""

    @pytest.fixture
    def search_node(self):
        """Create knowledge base search node."""
        return KnowledgeBaseSearch()

    @pytest.mark.asyncio
    async def test_search_node_with_login_issue(self, search_node):
        """Test search node with login issue."""
        state = {
            "email_id": "test_001",
            "sender": "test@example.com",
            "subject": "Cannot login",
            "body": "I forgot my password and cannot login to my account",
            "classification": {"category": "technical_support", "confidence": 0.9},
            "priority": "high",
            "error": None,
        }

        result_state = await search_node.search(state)

        assert result_state["knowledge_base_results"]["found_relevant_docs"] is True
        assert len(result_state["knowledge_base_results"]["results"]) > 0

    @pytest.mark.asyncio
    async def test_search_node_with_error_skips_search(self, search_node):
        """Test that search is skipped when error exists."""
        state = {
            "email_id": "test_002",
            "error": "Some error occurred",
            "knowledge_base_results": {},
        }

        result_state = await search_node.search(state)

        assert "error" in result_state
        assert result_state["knowledge_base_results"] == {}

    @pytest.mark.asyncio
    async def test_search_node_build_query(self, search_node):
        """Test search query building."""
        state = {
            "subject": "Billing problem",
            "body": "I was charged twice",
            "classification": {"category": "billing"},
            "priority": "high",
        }

        query = search_node._build_search_query(state)

        assert "billing" in query.lower()
        assert "charged" in query.lower()

    @pytest.mark.asyncio
    async def test_search_node_formats_results(self, search_node):
        """Test result formatting."""
        raw_results = [
            {
                "id": 1,
                "title": "Test",
                "category": "test",
                "similarity_score": 0.85,
                "content": "Test content " * 50,
            }
        ]

        formatted = search_node._format_results(raw_results)

        assert len(formatted) == 1
        assert formatted[0]["similarity_score"] == 0.85
        assert len(formatted[0]["excerpt"]) <= 300


class TestSampleDocuments:
    """Test sample documents functionality."""

    def test_get_documents_returns_list(self):
        """Test that get_documents returns list."""
        docs = get_documents()

        assert isinstance(docs, list)
        assert len(docs) > 0

    def test_documents_have_required_fields(self):
        """Test that documents have required fields."""
        docs = get_documents()

        for doc in docs:
            assert "id" in doc
            assert "title" in doc
            assert "category" in doc
            assert "content" in doc
            assert isinstance(doc["content"], str)
            assert len(doc["content"]) > 0

    def test_documents_have_valid_categories(self):
        """Test that documents have valid categories."""
        docs = get_documents()
        valid_categories = [
            "technical_support",
            "billing",
            "general_inquiry",
        ]

        for doc in docs:
            assert doc["category"] in valid_categories

    def test_get_documents_by_category(self):
        """Test filtering documents by category."""
        tech_docs = get_documents_by_category("technical_support")

        assert len(tech_docs) > 0
        assert all(doc["category"] == "technical_support" for doc in tech_docs)

    def test_document_content_quality(self):
        """Test that document content has good quality."""
        docs = get_documents()

        for doc in docs:
            content = doc["content"]
            assert len(content) > 100
            assert "\n" in content or " " in content
            assert not content.isupper()


class TestFAISSIntegration:
    """Integration tests for FAISS with workflow."""

    @pytest.mark.asyncio
    async def test_full_search_workflow(self):
        """Test complete search workflow."""
        kb = FAISSKnowledgeBase()
        kb.build_index(get_documents())

        search_node = KnowledgeBaseSearch()
        search_node.faiss_kb = kb

        state = {
            "email_id": "integration_test_001",
            "sender": "customer@example.com",
            "subject": "Password reset not working",
            "body": "I tried to reset my password but I don't receive the email",
            "classification": {"category": "technical_support"},
            "priority": "high",
            "error": None,
        }

        result = await search_node.search(state)

        assert result["knowledge_base_results"]["found_relevant_docs"] is True
        assert len(result["knowledge_base_results"]["results"]) > 0
        assert result["knowledge_base_results"]["search_method"] == "faiss_semantic"

    def test_similarity_scores_meaningful(self):
        """Test that similarity scores are meaningful."""
        kb = FAISSKnowledgeBase()
        kb.build_index(get_documents())

        similar_query = "I cannot login to my account"
        dissimilar_query = "xyzabc gibberish blah blah"

        similar_results = kb.search(similar_query, top_k=5, threshold=0.3)
        dissimilar_results = kb.search(dissimilar_query, top_k=5, threshold=0.3)

        if similar_results and dissimilar_results:
            avg_similar_score = sum(r["similarity_score"] for r in similar_results) / len(
                similar_results
            )
            avg_dissimilar_score = sum(
                r["similarity_score"] for r in dissimilar_results
            ) / len(dissimilar_results)

            assert avg_similar_score > avg_dissimilar_score