"""Build FAISS index from sample documents"""

import sys
from pathlib import Path

from src.knowledge_base.documents import get_documents
from src.services.faiss_service import FAISSKnowledgeBase
from src.core.logger import setup_logger

logger = setup_logger(__name__)


def build_index():
    """Build FAISS index from sample documents."""
    logger.info("Starting FAISS index build")

    try:
        kb = FAISSKnowledgeBase(model_name="all-MiniLM-L6-v2")

        documents = get_documents()
        logger.info(f"Loading {len(documents)} documents")

        kb.build_index(documents)

        stats = kb.get_index_stats()
        logger.info(f"Index statistics: {stats}")

        print("\n" + "=" * 60)
        print("FAISS INDEX BUILD SUCCESSFUL!")
        print("=" * 60)
        print(f"Total Documents: {stats['total_documents']}")
        print(f"Embedding Model: {stats['embedding_model']}")
        print(f"Embedding Dimension: {stats['dimension']}")
        print(f"Index Type: {stats['index_type']}")
        print("=" * 60)
        print(f"Index saved to: knowledge_base/faiss_index.bin")
        print(f"Metadata saved to: knowledge_base/faiss_metadata.pkl")
        print("=" * 60 + "\n")

        return True

    except Exception as e:
        logger.error(f"Error building index: {str(e)}")
        print(f"\nERROR: Failed to build FAISS index: {str(e)}\n")
        return False


def test_search():
    """Test the search functionality."""
    logger.info("Testing FAISS search")

    try:
        kb = FAISSKnowledgeBase()

        if not kb.load_index():
            logger.error("Could not load index")
            return False

        test_queries = [
            "How do I reset my password?",
            "I was charged twice for my subscription",
            "The app keeps crashing on my phone",
            "How do I cancel my account?",
            "I need to export my data",
        ]

        print("\n" + "=" * 60)
        print("TESTING FAISS SEARCH")
        print("=" * 60 + "\n")

        for query in test_queries:
            print(f"Query: {query}")
            results = kb.search(query, top_k=3, threshold=0.5)

            if results:
                for i, result in enumerate(results, 1):
                    print(f"\n  Result {i}:")
                    print(f"    Title: {result['title']}")
                    print(f"    Category: {result['category']}")
                    print(f"    Similarity: {result['similarity_score']:.2%}")
                    preview = result['content'][:100].replace("\n", " ").strip()
                    print(f"    Preview: {preview}...")
            else:
                print("  No results found")

            print()

        print("=" * 60)
        print("SEARCH TEST COMPLETE")
        print("=" * 60 + "\n")

        return True

    except Exception as e:
        logger.error(f"Error testing search: {str(e)}")
        print(f"\nERROR: Search test failed: {str(e)}\n")
        return False


def show_index_stats():
    """Display index statistics."""
    logger.info("Retrieving index statistics")

    try:
        kb = FAISSKnowledgeBase()

        if not kb.load_index():
            print("No FAISS index found. Run build_faiss_index.py first.\n")
            return False

        stats = kb.get_index_stats()

        print("\n" + "=" * 60)
        print("FAISS INDEX STATISTICS")
        print("=" * 60)
        print(f"Status: {'Ready' if stats['initialized'] else 'Not initialized'}")
        print(f"Total Documents: {stats['total_documents']}")
        print(f"Embedding Model: {stats['embedding_model']}")
        print(f"Embedding Dimension: {stats['dimension']}")
        print(f"Index Type: {stats['index_type']}")
        print("=" * 60 + "\n")

        return True

    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        print(f"\nERROR: {str(e)}\n")
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "build":
            success = build_index()
            sys.exit(0 if success else 1)
        elif command == "test":
            success = test_search()
            sys.exit(0 if success else 1)
        elif command == "stats":
            success = show_index_stats()
            sys.exit(0 if success else 1)
        else:
            print(f"Unknown command: {command}")
            print("\nUsage:")
            print("  python -m src.knowledge_base.build_faiss_index build  - Build FAISS index")
            print("  python -m src.knowledge_base.build_faiss_index test   - Test search functionality")
            print("  python -m src.knowledge_base.build_faiss_index stats  - Show index statistics")
            sys.exit(1)
    else:
        print("\nFAISS Index Builder")
        print("=" * 60)
        success = build_index()

        if success:
            test_search()
            show_index_stats()

        sys.exit(0 if success else 1)