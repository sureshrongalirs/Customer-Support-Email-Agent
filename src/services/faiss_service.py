"""FAISS-based Knowledge Base Service for Semantic Search"""

import os
import pickle
from pathlib import Path
from typing import Optional

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from src.core.config import settings
from src.core.logger import setup_logger

logger = setup_logger(__name__)


class FAISSKnowledgeBase:
    """FAISS-based knowledge base for semantic search."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize FAISS knowledge base.

        Args:
            model_name: Sentence transformer model name
        """
        self.model_name = model_name
        self.embedding_model = SentenceTransformer(model_name)
        self.index: Optional[faiss.IndexFlatL2] = None
        self.documents = []
        self.index_path = Path("knowledge_base/faiss_index.bin")
        self.metadata_path = Path("knowledge_base/faiss_metadata.pkl")

        logger.info(f"Initialized FAISS with model: {model_name}")

    def build_index(self, documents: list[dict]) -> None:
        """Build FAISS index from documents.

        Args:
            documents: List of document dicts with 'content' and 'title'
        """
        logger.info(f"Building FAISS index from {len(documents)} documents")

        try:
            self.documents = documents
            embeddings = self._generate_embeddings([doc["content"] for doc in documents])

            embedding_dim = embeddings.shape[1]
            self.index = faiss.IndexFlatL2(embedding_dim)
            self.index.add(embeddings.astype(np.float32))

            self.save_index()
            logger.info(f"Successfully built FAISS index with {len(documents)} documents")

        except Exception as e:
            logger.error(f"Error building FAISS index: {str(e)}")
            raise

    def load_index(self) -> bool:
        """Load FAISS index from disk.

        Returns:
            True if index loaded successfully
        """
        try:
            if not self.index_path.exists() or not self.metadata_path.exists():
                logger.warning("FAISS index files not found")
                return False

            self.index = faiss.read_index(str(self.index_path))

            with open(self.metadata_path, "rb") as f:
                self.documents = pickle.load(f)

            logger.info(f"Loaded FAISS index with {len(self.documents)} documents")
            return True

        except Exception as e:
            logger.error(f"Error loading FAISS index: {str(e)}")
            return False

    def save_index(self) -> None:
        """Save FAISS index to disk."""
        try:
            self.index_path.parent.mkdir(parents=True, exist_ok=True)

            faiss.write_index(self.index, str(self.index_path))

            with open(self.metadata_path, "wb") as f:
                pickle.dump(self.documents, f)

            logger.info(f"Saved FAISS index to {self.index_path}")

        except Exception as e:
            logger.error(f"Error saving FAISS index: {str(e)}")
            raise

    def search(
        self,
        query: str,
        top_k: int = 5,
        threshold: float = 0.7,
    ) -> list[dict]:
        """Search knowledge base using semantic similarity.

        Args:
            query: Search query
            top_k: Number of results to return
            threshold: Similarity threshold (0-1)

        Returns:
            List of relevant documents with scores
        """
        if self.index is None or not self.documents:
            logger.warning("FAISS index not initialized")
            return []

        try:
            query_embedding = self._generate_embeddings([query])
            distances, indices = self.index.search(
                query_embedding.astype(np.float32), top_k
            )

            results = []
            for distance, idx in zip(distances[0], indices):
                if idx != -1:
                    similarity_score = 1 / (1 + float(distance))

                    if similarity_score >= threshold:
                        doc = self.documents[int(idx)].copy()
                        doc["similarity_score"] = float(similarity_score)
                        doc["distance"] = float(distance)
                        results.append(doc)

            logger.info(f"Found {len(results)} relevant documents for query")
            return results

        except Exception as e:
            logger.error(f"Error searching FAISS index: {str(e)}")
            return []

    def _generate_embeddings(self, texts: list[str]) -> np.ndarray:
        """Generate embeddings for texts.

        Args:
            texts: List of texts to embed

        Returns:
            Numpy array of embeddings
        """
        try:
            embeddings = self.embedding_model.encode(
                texts,
                convert_to_numpy=True,
                show_progress_bar=False,
            )
            return embeddings.astype(np.float32)

        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise

    def add_documents(self, new_documents: list[dict]) -> None:
        """Add new documents to existing index.

        Args:
            new_documents: List of documents to add
        """
        if self.index is None:
            logger.warning("Index not initialized, building new index")
            self.build_index(new_documents)
            return

        try:
            logger.info(f"Adding {len(new_documents)} documents to index")

            new_embeddings = self._generate_embeddings(
                [doc["content"] for doc in new_documents]
            )

            self.index.add(new_embeddings.astype(np.float32))
            self.documents.extend(new_documents)

            self.save_index()
            logger.info("Successfully added documents to index")

        except Exception as e:
            logger.error(f"Error adding documents: {str(e)}")
            raise

    def get_index_stats(self) -> dict:
        """Get statistics about the index.

        Returns:
            Index statistics
        """
        if self.index is None:
            return {"initialized": False}

        return {
            "initialized": True,
            "total_documents": len(self.documents),
            "index_type": type(self.index).__name__,
            "dimension": self.index.d if hasattr(self.index, "d") else None,
            "embedding_model": self.model_name,
        }

    def update_document(self, doc_id: int, updated_doc: dict) -> bool:
        """Update a document in the index.

        Args:
            doc_id: Document ID to update
            updated_doc: Updated document

        Returns:
            True if update successful
        """
        try:
            if doc_id >= len(self.documents):
                logger.error(f"Document ID {doc_id} out of range")
                return False

            self.documents[doc_id] = updated_doc

            embedding = self._generate_embeddings([updated_doc["content"]])
            self.index.reset()
            all_embeddings = self._generate_embeddings(
                [doc["content"] for doc in self.documents]
            )
            self.index.add(all_embeddings.astype(np.float32))

            self.save_index()
            logger.info(f"Updated document {doc_id}")
            return True

        except Exception as e:
            logger.error(f"Error updating document: {str(e)}")
            return False

    def delete_document(self, doc_id: int) -> bool:
        """Delete a document from the index.

        Note: FAISS doesn't support direct deletion, so we rebuild.

        Args:
            doc_id: Document ID to delete

        Returns:
            True if deletion successful
        """
        try:
            if doc_id >= len(self.documents):
                logger.error(f"Document ID {doc_id} out of range")
                return False

            del self.documents[doc_id]

            if self.documents:
                all_embeddings = self._generate_embeddings(
                    [doc["content"] for doc in self.documents]
                )
                embedding_dim = all_embeddings.shape[1]
                self.index = faiss.IndexFlatL2(embedding_dim)
                self.index.add(all_embeddings.astype(np.float32))

            self.save_index()
            logger.info(f"Deleted document {doc_id}")
            return True

        except Exception as e:
            logger.error(f"Error deleting document: {str(e)}")
            return False