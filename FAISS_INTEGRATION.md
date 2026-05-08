# FAISS Knowledge Base Integration Guide

## Overview

This guide explains the FAISS (Facebook AI Similarity Search) integration for semantic knowledge base search in the Customer Support Email Agent.

## What is FAISS?

FAISS is an open-source library for efficient similarity search and clustering of dense vectors. It provides:

- **Semantic Search**: Find documents by meaning, not just keywords
- **Fast Retrieval**: Optimized for searching millions of vectors
- **Flexible Indexing**: Multiple index types for different use cases
- **Production Ready**: Used by Meta, Microsoft, and other companies

## Architecture

```
Sample Documents
    ↓
Sentence Transformers (all-MiniLM-L6-v2)
    ↓
Generate Embeddings (384 dimensions)
    ↓
FAISS Index (IndexFlatL2)
    ↓
Save to Disk
    ↓
Load when Needed
```

## Components

### 1. FAISSKnowledgeBase Service (`src/services/faiss_service.py`)

Main service for FAISS operations:

```python
from src.services.faiss_service import FAISSKnowledgeBase

kb = FAISSKnowledgeBase(model_name="all-MiniLM-L6-v2")
kb.build_index(documents)
results = kb.search("query text", top_k=5, threshold=0.7)
```

**Key Methods**:
- `build_index(documents)` - Build index from documents
- `load_index()` - Load saved index from disk
- `save_index()` - Save index to disk
- `search(query, top_k, threshold)` - Semantic search
- `add_documents(new_docs)` - Add to existing index
- `update_document(id, doc)` - Update a document
- `delete_document(id)` - Delete a document
- `get_index_stats()` - Get index statistics

### 2. Sample Documents (`src/knowledge_base/documents.py`)

Pre-built documentation with 10 comprehensive documents:

- Account Login Issues
- Billing and Payment Issues
- Technical Support and Errors
- Feature Usage Guide
- Security and Privacy
- Account Settings
- Common Error Codes
- Getting Started Guide
- API Integration Guide
- System Status and Maintenance

**Create Custom Documents**:

```python
SAMPLE_DOCUMENTS = [
    {
        "id": 1,
        "title": "Your Document Title",
        "category": "your_category",
        "content": "Complete document text..."
    },
    # More documents...
]
```

### 3. Index Builder (`src/knowledge_base/build_faiss_index.py`)

Script to build and manage FAISS index:

```bash
# Build index from sample documents
python -m src.knowledge_base.build_faiss_index build

# Test search functionality
python -m src.knowledge_base.build_faiss_index test

# Show index statistics
python -m src.knowledge_base.build_faiss_index stats
```

### 4. Knowledge Base Search Node

Updated to use FAISS instead of keyword matching:

```python
from src.nodes.knowledge_base_search import KnowledgeBaseSearch

search_node = KnowledgeBaseSearch()
state = await search_node.search(workflow_state)
```

## Setup Instructions

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

New packages:
- `faiss-cpu>=1.7.4` - FAISS library
- `sentence-transformers>=2.2.2` - Embedding models
- `numpy>=1.24.0` - Numerical computations

### Step 2: Build the Index

```bash
python -m src.knowledge_base.build_faiss_index build
```

This creates:
- `knowledge_base/faiss_index.bin` - FAISS index file
- `knowledge_base/faiss_metadata.pkl` - Document metadata

### Step 3: Test the Integration

```bash
# Run FAISS tests
pytest tests/test_faiss_integration.py -v

# Test search functionality
python -m src.knowledge_base.build_faiss_index test

# Check index statistics
python -m src.knowledge_base.build_faiss_index stats
```

## How Semantic Search Works

### 1. Document Embedding

Each document is converted to a 384-dimensional vector using a pre-trained sentence transformer:

```
Document: "How do I reset my password?"
    ↓
Sentence Transformer
    ↓
Vector: [0.123, -0.456, 0.789, ..., 0.234] (384 values)
```

### 2. Index Building

All document vectors are stored in a FAISS index:

```
FAISS Index
├── Document 1 Vector
├── Document 2 Vector
├── Document 3 Vector
└── ... (all documents)
```

### 3. Query Search

When searching:

```
Query: "I can't login"
    ↓
Embed query to vector
    ↓
FAISS finds closest vectors
    ↓
Returns top-k most similar documents
    ↓
Filter by similarity threshold
    ↓
Return results
```

### 4. Similarity Scoring

Similarity score = 1 / (1 + distance)

- Score = 1.0: Perfect match
- Score = 0.5: Somewhat relevant
- Score = 0.0: Not relevant

Default threshold = 0.7 (70% similar)

## Example Usage

### Build Index from Documents

```python
from src.services.faiss_service import FAISSKnowledgeBase
from src.knowledge_base.documents import get_documents

kb = FAISSKnowledgeBase(model_name="all-MiniLM-L6-v2")
documents = get_documents()
kb.build_index(documents)
kb.save_index()
```

### Search Documents

```python
kb = FAISSKnowledgeBase()
kb.load_index()

results = kb.search(
    "I cannot login to my account",
    top_k=5,
    threshold=0.7
)

for result in results:
    print(f"Title: {result['title']}")
    print(f"Category: {result['category']}")
    print(f"Similarity: {result['similarity_score']:.2%}")
    print(f"Content: {result['content'][:200]}...")
```

### Add New Documents

```python
new_docs = [
    {
        "id": 100,
        "title": "New FAQ",
        "category": "general_inquiry",
        "content": "..."
    }
]

kb.add_documents(new_docs)
```

### Update Existing Document

```python
updated_doc = {
    "id": 1,
    "title": "Updated Title",
    "category": "technical_support",
    "content": "Updated content..."
}

kb.update_document(0, updated_doc)
```

## Customizing Documents

### Add Your Knowledge Base

Create documents for your specific use case:

```python
# src/knowledge_base/documents.py

SAMPLE_DOCUMENTS = [
    {
        "id": 1,
        "title": "Product Overview",
        "category": "general_inquiry",
        "content": """
        Our product provides...
        Key features include...
        Pricing starts at...
        """
    },
    {
        "id": 2,
        "title": "Troubleshooting Guide",
        "category": "technical_support",
        "content": """
        Common issues:
        1. Issue A - Solution...
        2. Issue B - Solution...
        """
    },
    # ... more documents
]
```

### Build Custom Index

```bash
# After updating documents.py
python -m src.knowledge_base.build_faiss_index build
```

## Performance Tuning

### Index Types

Current: `IndexFlatL2` (exact search, slower but accurate)

Other options:
- `IndexHNSW`: Fast approximate search
- `IndexIVF`: Inverted file index
- `IndexLSH`: Locality-sensitive hashing

### Similarity Threshold

Adjust based on your needs:

```python
# Strict (only very relevant results)
results = kb.search(query, threshold=0.85)

# Moderate (default)
results = kb.search(query, threshold=0.70)

# Loose (more results, including somewhat relevant)
results = kb.search(query, threshold=0.50)
```

### Embedding Model

Current: `all-MiniLM-L6-v2` (fast, 384 dimensions)

Better models (slower, more accurate):
- `all-mpnet-base-v2` (768 dimensions, more accurate)
- `allenai-specter` (768 dimensions, scientific papers)
- `cross-encoder/mmarco-mMiniLMv2-L12-H384-multilingual` (multilingual)

Change model:

```python
kb = FAISSKnowledgeBase(model_name="all-mpnet-base-v2")
```

## Index Statistics

Get information about your index:

```python
stats = kb.get_index_stats()
# {
#     'initialized': True,
#     'total_documents': 10,
#     'index_type': 'IndexFlatL2',
#     'dimension': 384,
#     'embedding_model': 'all-MiniLM-L6-v2'
# }
```

## File Locations

```
knowledge_base/
├── __init__.py
├── documents.py               # Sample documents
├── build_faiss_index.py       # Builder script
├── sample_data.txt            # (old keyword search format)
├── faiss_index.bin            # FAISS index (binary)
└── faiss_metadata.pkl         # Document metadata
```

## Workflow Integration

The knowledge base search is integrated into the workflow:

```
Email Input
    ↓
Parse Email
    ↓
Classify Intent
    ↓
[Search Knowledge Base] ← Uses FAISS semantic search
    ↓
Generate Response
    ↓
Route to Human (if needed)
    ↓
Send Email
    ↓
Schedule Followup
```

Search results are used to provide context for response generation:

```python
knowledge_base_results = state["knowledge_base_results"]

if knowledge_base_results["found_relevant_docs"]:
    relevant_docs = knowledge_base_results["results"]
    # Use these docs in LLM response generation
```

## Troubleshooting

### Issue: Index not found

**Solution**: Build the index first

```bash
python -m src.knowledge_base.build_faiss_index build
```

### Issue: Slow search

**Possible causes**:
- Large number of documents
- Using slower embedding model
- Using IndexFlatL2 (accurate but slow)

**Solutions**:
- Use faster embedding model
- Consider using approximate index (HNSW)
- Implement caching for common queries

### Issue: Poor search results

**Possible causes**:
- Threshold too high (only exact matches)
- Poor document quality
- Query too vague

**Solutions**:
- Lower similarity threshold
- Improve document content quality
- Make search queries more specific
- Add more documents

### Issue: Out of memory with many documents

**Solutions**:
- Use approximate index (HNSW)
- Reduce embedding model size
- Split index into multiple indices
- Use GPU-based FAISS (faiss-gpu)

## Advanced Usage

### Batch Search

```python
queries = [
    "How do I reset password?",
    "Billing issues",
    "System down"
]

for query in queries:
    results = kb.search(query)
    # Process results
```

### Category-Specific Search

```python
# Filter results by category
results = kb.search(query, top_k=10)
tech_results = [r for r in results if r["category"] == "technical_support"]
```

### Implement Caching

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_search(query):
    return kb.search(query)
```

## Testing

Run FAISS integration tests:

```bash
# Run all FAISS tests
pytest tests/test_faiss_integration.py -v

# Run specific test class
pytest tests/test_faiss_integration.py::TestFAISSKnowledgeBase -v

# Run with coverage
pytest tests/test_faiss_integration.py -v --cov=src.services.faiss_service
```

## Production Deployment

### Index Persistence

The index is automatically saved to disk:
- `knowledge_base/faiss_index.bin`
- `knowledge_base/faiss_metadata.pkl`

Ensure these files are:
- Backed up regularly
- Available during deployment
- Version controlled (or reproducible)

### Scaling

For production with many documents:

1. **Use GPU-accelerated FAISS**:
   ```bash
   pip install faiss-gpu
   ```

2. **Use approximate index**:
   ```python
   # In faiss_service.py, change index type
   index = faiss.IndexHNSW(d, 32)  # M=32
   ```

3. **Implement batch indexing**:
   ```python
   # Index documents in batches for large datasets
   ```

4. **Add monitoring**:
   - Track search latency
   - Monitor index size
   - Log search queries for optimization

## References

- [FAISS Documentation](https://github.com/facebookresearch/faiss)
- [Sentence Transformers](https://www.sbert.net/)
- [Vector Search Concepts](https://voxel51.com/blog/vector-search/)

## Next Steps

1. ✅ FAISS service implemented
2. ✅ Sample documents created
3. ✅ Index builder created
4. ✅ Integration tests added
5. Build the index: `python -m src.knowledge_base.build_faiss_index build`
6. Run tests: `pytest tests/test_faiss_integration.py -v`
7. Deploy: Include index files in deployment