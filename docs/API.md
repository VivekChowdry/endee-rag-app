# API Reference

## Base URL

```
http://localhost:8000 (development)
https://api.yourdomain.com (production)
```

## Authentication

Not required for open-mode Endee deployment. Configure in `.env`:

```env
ENDEE_AUTH_MODE=open  # or token-based
ENDEE_AUTH_TOKEN=your-token
```

## Response Format

All endpoints return JSON with consistent structure:

```json
{
  "status": "success",
  "data": { },
  "error": null,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## Index Management

### Create Index

**Request**
```http
POST /api/v1/index/create
?index_name=documents
&dimension=384
```

**Response**
```json
{
  "index": "documents",
  "dimension": 384,
  "status": "created",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### List Indices

**Request**
```http
GET /api/v1/index/list
```

**Response**
```json
{
  "indices": [
    {
      "name": "documents",
      "dimension": 384,
      "vector_count": 5000,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

---

## Document Operations

### Index Documents (Batch)

**Request**
```http
POST /api/v1/documents/index?index_name=documents
Content-Type: application/json

{
  "documents": [
    {
      "id": "doc_001",
      "content": "Machine learning is a subset of AI...",
      "metadata": {
        "source": "tutorial.txt",
        "author": "John Doe",
        "date": "2024-01-15"
      }
    },
    {
      "id": "doc_002",
      "content": "Neural networks are inspired by biology...",
      "metadata": {
        "source": "guide.txt"
      }
    }
  ]
}
```

**Response**
```json
{
  "indexed": 2,
  "index": "documents",
  "status": "success",
  "processing_time_ms": 245
}
```

### Upload Document File

**Request**
```http
POST /api/v1/documents/upload?index_name=documents
Content-Type: multipart/form-data

file: @document.txt
```

**Response**
```json
{
  "filename": "document.txt",
  "chunks_indexed": 8,
  "status": "success",
  "tokens_processed": 2048
}
```

---

## Semantic Search

### Search Endpoint

**Request**
```http
POST /api/v1/search/semantic?index_name=documents
Content-Type: application/json

{
  "query": "machine learning algorithms",
  "top_k": 5
}
```

**Query Parameters**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `index_name` | string | Yes | Name of the index to search |
| `top_k` | integer | No | Number of results (default: 5, max: 100) |

**Response**
```json
{
  "query": "machine learning algorithms",
  "results": [
    {
      "id": "doc_001_chunk_0",
      "content": "Machine learning algorithms are methods that enable...",
      "similarity": 0.892,
      "metadata": {
        "source": "tutorial.txt",
        "chunk_index": 0
      }
    },
    {
      "id": "doc_002_chunk_1",
      "content": "Classification is a supervised learning algorithm...",
      "similarity": 0.845,
      "metadata": {
        "source": "guide.txt"
      }
    }
  ],
  "search_time_ms": 34,
  "total_results": 2
}
```

### Query Similarity Scores

- **0.9+**: Highly relevant
- **0.7-0.9**: Relevant
- **0.5-0.7**: Somewhat related
- **<0.5**: Weakly related (usually not shown)

---

## RAG (Retrieval-Augmented Generation)

### Query Endpoint

**Request**
```http
POST /api/v1/rag/query?index_name=documents
Content-Type: application/json

{
  "question": "What are the main types of machine learning?",
  "top_k": 5
}
```

**Response**
```json
{
  "question": "What are the main types of machine learning?",
  "answer": "Based on the provided context, the main types of machine learning are:\n\n1. **Supervised Learning**: Uses labeled data to train models for prediction tasks like classification and regression.\n\n2. **Unsupervised Learning**: Discovers patterns in unlabeled data through clustering and dimensionality reduction.\n\n3. **Reinforcement Learning**: Trains agents to make sequential decisions by rewarding desired behaviors.\n\nThese approaches form the foundation of modern machine learning applications.",
  "sources": [
    {
      "id": "doc_001_chunk_0",
      "content": "Supervised learning uses labeled data where each example has a known output. Common algorithms include decision trees, random forests, and neural networks.",
      "similarity": 0.923,
      "metadata": {
        "source": "ml_intro.txt",
        "page": 12
      }
    },
    {
      "id": "doc_001_chunk_2",
      "content": "Unsupervised learning finds hidden patterns in data without labels. Clustering and dimensionality reduction are key techniques in this domain.",
      "similarity": 0.891,
      "metadata": {
        "source": "ml_intro.txt",
        "page": 15
      }
    }
  ],
  "generation_time_ms": 1250,
  "retrieval_time_ms": 45
}
```

---

## Error Handling

### Error Response Format

```json
{
  "error": {
    "code": "INVALID_INDEX",
    "message": "Index 'documents' not found",
    "details": {
      "available_indices": ["documents", "research_papers"]
    }
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Common Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `INVALID_INDEX` | 404 | Index does not exist |
| `INVALID_QUERY` | 400 | Query parameter validation failed |
| `EMPTY_QUERY` | 400 | Query/question is empty |
| `EMBEDDING_FAILED` | 500 | Failed to generate embeddings |
| `SEARCH_FAILED` | 500 | Search operation failed |
| `SERVER_ERROR` | 500 | Internal server error |

### Error Resolution

**Index not found**
```bash
# Create the index first
curl -X POST "http://localhost:8000/api/v1/index/create?index_name=documents"
```

**Empty results**
```bash
# Verify documents are indexed
curl -X GET "http://localhost:8000/api/v1/index/list"

# Upload sample documents
curl -X POST "http://localhost:8000/api/v1/documents/upload?index_name=documents" \
  -F "file=@sample.txt"
```

---

## Rate Limiting

| Endpoint | Limit | Window |
|----------|-------|--------|
| `/search/semantic` | 100 | 60s |
| `/rag/query` | 50 | 60s |
| `/documents/index` | 10 | 60s |
| `/documents/upload` | 5 | 60s |

---

## Pagination

Supported for list operations:

```http
GET /api/v1/results?index_name=documents&limit=20&offset=40
```

---

## Examples

### Python Client

```python
import requests

BASE_URL = "http://localhost:8000"

# Semantic search
response = requests.post(
    f"{BASE_URL}/api/v1/search/semantic?index_name=documents",
    json={"query": "neural networks", "top_k": 5}
)
print(response.json())

# RAG query
response = requests.post(
    f"{BASE_URL}/api/v1/rag/query?index_name=documents",
    json={"question": "How do neural networks learn?", "top_k": 5}
)
print(response.json()["answer"])
```

### JavaScript/Fetch

```javascript
const search = async (query) => {
  const response = await fetch('/api/v1/search/semantic?index_name=documents', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, top_k: 5 })
  });
  return await response.json();
};

const rag = async (question) => {
  const response = await fetch('/api/v1/rag/query?index_name=documents', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question, top_k: 5 })
  });
  return await response.json();
};
```

### cURL

```bash
# Search
curl -X POST http://localhost:8000/api/v1/search/semantic?index_name=documents \
  -H "Content-Type: application/json" \
  -d '{
    "query": "artificial intelligence",
    "top_k": 5
  }' | jq .

# RAG
curl -X POST http://localhost:8000/api/v1/rag/query?index_name=documents \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is machine learning?",
    "top_k": 5
  }' | jq .answer
```
