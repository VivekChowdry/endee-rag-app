## Architecture Overview

### System Components

1. **Endee Vector Database**
   - Role: Stores and indexes document embeddings
   - Algorithm: HNSW (Hierarchical Navigable Small World)
   - Capacity: Up to 1 billion vectors per node
   - Dimensionality: 384-768 (configurable based on embedding model)

2. **Sentence Transformers (Embeddings)**
   - Role: Converts text to vector embeddings
   - Model: `all-MiniLM-L6-v2` (384 dims, lightweight)
   - Process: Text → normalize → embed → 384-dim vector
   - Library: `sentence-transformers` (HuggingFace)

3. **FastAPI Backend**
   - Role: REST API for search, RAG, indexing
   - Framework: FastAPI with async support
   - Key endpoints: `/search/semantic`, `/rag/query`, `/documents/index`
   - Async patterns: For concurrent vector operations

4. **React Frontend**
   - Role: User interface for search and Q&A
   - Framework: React 18 + Vite
   - Features: Dual-mode (search/RAG), document upload, results display
   - Styling: Dark mode, responsive design

### Data Flow

#### Indexing Pipeline

```
Document → Chunking → Embedding → Endee Insert
  |           |            |            |
  v           v            v            v
Raw text   Split by    S-Transform   HNSW index
          para/sent    (384-dim)    (GPU-ready)
```

#### Search Pipeline

```
Query → Embedding → Endee Search → Rerank → Format
  |        |            |            |        |
  v        v            v            v        v
"ML?"   384-dim      Top-1000      Similarity  JSON
        vector       results       scored      results
```

#### RAG Pipeline

```
Question → Embedding → Search → Retrieve → Generate → Output
   |         |           |        |          |        |
   v         v           v        v          v        v
"How?"    Vector      Endee    Context   LLM+Prompt  Answer+
                      top-5    strings   (OpenAI)    Sources
```

---

## Vector Search Algorithm (HNSW)

### Why HNSW?

- **Fast**: O(log N) search complexity
- **Scalable**: Handles 1B+ vectors efficiently
- **Accurate**: Approximate but high-recall results
- **Memory**: Low overhead for index

### How It Works

1. Build hierarchical layers (level-0 to level-M)
2. Insert vectors with random entry points
3. Search via layer traversal (coarse → fine)
4. Return top-k nearest neighbors

---

## Deployment Topology

### Development (Docker Compose)

```
Local Machine
├── Frontend (React)    :3000
├── Backend (FastAPI)   :8000
├── Endee Server        :8080
└── Volumes             (docker-named)
```

### Production (Kubernetes/Cloud)

```
Cloud Platform
├── Frontend Pod
│   └── React App (exposed via Ingress)
├── Backend Pods (replicated)
│   └── FastAPI + embeddings service
└── Endee Stateful Set
    └── Persistent storage for vectors
```
