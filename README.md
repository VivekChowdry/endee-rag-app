# Comprehensive README for Endee RAG & Semantic Search Application

## 🚀 Overview

**Endee RAG & Semantic Search** is a full-stack application that combines:
- **Semantic Search**: Vector-based similarity search using embeddings
- **RAG (Retrieval-Augmented Generation)**: Question answering with retrieved context
- **Endee Vector Database**: High-performance HNSW-based vector store (up to 1B vectors/node)

This project demonstrates how to build modern AI applications using vector embeddings for intelligent document retrieval and context-aware generation.

### Key Features

✅ **Semantic Search**: Find semantically similar documents using vector embeddings
✅ **RAG Pipeline**: Answer questions based on document context
✅ **Document Indexing**: Batch index and retrieve documents
✅ **Streaming API**: FastAPI backend with async support
✅ **Beautiful UI**: React + Vite frontend with dark mode
✅ **Full Docker Setup**: One-command deployment with Docker Compose
✅ **Production Ready**: Error handling, logging, health checks

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    React Frontend                        │
│              (Semantic Search + RAG UI)                  │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ↓ HTTP/API
┌─────────────────────────────────────────────────────────┐
│              FastAPI Backend (Main)                      │
│  • /api/v1/search/semantic  (Vector similarity)         │
│  • /api/v1/rag/query        (Q&A with context)          │
│  • /api/v1/documents/index  (Batch indexing)            │
│  • /api/v1/documents/upload (File upload)               │
└──────────────┬──────────────────────────────────────────┘
               │
      ┌────────┴────────┐
      ↓                  ↓
┌───────────────┐   ┌──────────────────┐
│ Embeddings    │   │ Endee Vector DB  │
│ (Sentence     │   │ (HNSW Index)     │
│ Transformers) │   │ ~384 dim vectors │
└───────────────┘   └──────────────────┘
```

### Data Flow

1. **Indexing**: Documents → Chunk → Embed → Upsert to Endee
2. **Semantic Search**: Query → Embed → Vector Search → Rank Results
3. **RAG**: Question → Embed → Vector Search → Retrieve Context → LLM Generate → Return Answer + Sources

---

## 📦 Tech Stack

| Component | Technology | Role |
|-----------|-----------|------|
| **Vector DB** | Endee | High-performance vector indexing (1B+ vectors) |
| **Backend** | FastAPI (Python) | REST API, async operations |
| **Embeddings** | Sentence Transformers | Text → 384-dim vectors |
| **Frontend** | React 18 + Vite | Modern, responsive UI |
| **LLM** | OpenAI/Ollama (optional) | Answer generation |
| **Container** | Docker + Compose | Development & deployment |
| **DB** | Endee HNSW | Vector similarity search |

---

## 🛠️ Installation & Setup

### Prerequisites

- Docker & Docker Compose (recommended)
- OR: Python 3.11+, Node 20+, Endee server

### Option 1: Docker Compose (Recommended)

```bash
# Clone repository
git clone https://github.com/yourusername/endee-rag-app.git
cd endee-rag-app

# Copy and configure environment
cp backend/.env.example backend/.env
# Edit backend/.env if needed (e.g., add LLM_API_KEY)

# Start all services
docker-compose up -d

# Wait for services to be healthy (~30 seconds)
docker-compose ps

# Access application
# Frontend:  http://localhost:3000
# Backend:   http://localhost:8000
# Docs:      http://localhost:8000/docs
# Endee:     http://localhost:8080
```

### Option 2: Local Development

**1. Start Endee Server**

```bash
# Using Docker
docker run -p 8080:8080 endeeio/endee:latest

# OR install locally (Ubuntu/Debian)
wget https://github.com/endee-io/endee/releases/download/v1.0.0/endee-ubuntu-latest.tar.gz
tar -xzf endee-ubuntu-latest.tar.gz
./endee-server --port 8080
```

**2. Setup Backend**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env

# Start FastAPI server
python -m uvicorn main:app --reload
# Backend runs at http://localhost:8000
```

**3. Setup Frontend**

```bash
cd frontend
npm install
npm run dev
# Frontend runs at http://localhost:3000
```

---

## 📚 API Documentation

### Base URL

- **Docker Compose**: `http://localhost:8000`
- **Local Dev**: `http://localhost:8000`

### Interactive Docs

Visit http://localhost:8000/docs (Swagger UI) for interactive API testing.

### Endpoints

#### Health Check
```http
GET /health
```
Response:
```json
{
  "status": "healthy",
  "service": "Endee RAG & Semantic Search API"
}
```

#### Create Index
```http
POST /api/v1/index/create?index_name=documents&dimension=384
```

#### List Indices
```http
GET /api/v1/index/list
```

#### Semantic Search
```http
POST /api/v1/search/semantic?index_name=documents
Content-Type: application/json

{
  "query": "machine learning algorithms",
  "top_k": 5
}
```

Response:
```json
{
  "query": "machine learning algorithms",
  "results": [
    {
      "id": "doc_1_chunk_0",
      "content": "Machine learning is a subset of artificial intelligence...",
      "similarity": 0.89,
      "metadata": {
        "source": "tutorial.txt",
        "chunk_index": 0
      }
    }
  ]
}
```

#### RAG Query (Q&A)
```http
POST /api/v1/rag/query?index_name=documents
Content-Type: application/json

{
  "question": "What is the difference between supervised and unsupervised learning?",
  "top_k": 5
}
```

Response:
```json
{
  "question": "What is the difference between supervised and unsupervised learning?",
  "answer": "Based on the provided context, supervised learning uses labeled data...",
  "sources": [
    {
      "id": "doc_1_chunk_2",
      "content": "Supervised learning algorithms...",
      "similarity": 0.92,
      "metadata": {"source": "tutorial.txt"}
    }
  ]
}
```

#### Index Documents
```http
POST /api/v1/documents/index?index_name=documents
Content-Type: application/json

{
  "documents": [
    {
      "id": "doc_001",
      "content": "Document content here...",
      "metadata": {"source": "file.txt", "author": "John"}
    },
    {
      "id": "doc_002",
      "content": "Another document...",
      "metadata": {"source": "file2.txt"}
    }
  ]
}
```

#### Upload Document
```http
POST /api/v1/documents/upload?index_name=documents
Content-Type: multipart/form-data

file: @document.txt
```

---

## 🎯 Usage Examples

### Example 1: Index and Search Documents

**Step 1: Upload a document**
```bash
curl -X POST "http://localhost:8000/api/v1/documents/upload?index_name=documents" \
  -F "file=@sample.txt"
```

**Step 2: Perform semantic search**
```bash
curl -X POST "http://localhost:8000/api/v1/search/semantic?index_name=documents" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "artificial intelligence",
    "top_k": 5
  }'
```

### Example 2: Ask Questions (RAG)

```bash
curl -X POST "http://localhost:8000/api/v1/rag/query?index_name=documents" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the applications of machine learning?",
    "top_k": 5
  }'
```

### Example 3: Programmatic Usage

```python
import requests

BASE_URL = "http://localhost:8000"
INDEX = "documents"

# Semantic search
response = requests.post(
    f"{BASE_URL}/api/v1/search/semantic?index_name={INDEX}",
    json={"query": "neural networks", "top_k": 5}
)
print(response.json())

# RAG query
response = requests.post(
    f"{BASE_URL}/api/v1/rag/query?index_name={INDEX}",
    json={"question": "How do neural networks work?", "top_k": 5}
)
print(response.json())
```

---

## 🚢 Deployment

### Docker Compose (Recommended)

```bash
docker-compose up -d
# All services start: Endee, FastAPI backend, React frontend
```

### Kubernetes / Cloud Platforms

**AWS ECS**
```bash
# Build images
docker build -t myregistry/endee-backend:latest ./backend
docker build -t myregistry/endee-frontend:latest ./frontend

# Push to ECR
# Create ECS task definition from docker-compose.yml
# Deploy to ECS cluster
```

**Azure Container Instances**
```bash
az container create \
  --resource-group mygroup \
  --name endee-app \
  --image myregistry/endee-backend:latest \
  --ports 8000 \
  --environment-variables ENDEE_HOST=endee ENDEE_PORT=8080
```

**Railway.app, Render, or Fly.io**
- Push repo to GitHub
- Connect and deploy (auto-detects docker-compose.yml)

---

## 📊 Performance & Scaling

### Vector Database Performance (Endee)

| Metric | Value |
|--------|-------|
| Max vectors per node | 1,000,000,000 (1B) |
| Indexing speed | ~100K vectors/sec |
| Search latency (1M vecs) | <50ms |
| Index algorithm | HNSW (Hierarchical Navigable Small World) |

### Optimization Tips

1. **Batch Indexing**: Index documents in batches of 1000+
2. **Dimension Reduction**: Use smaller embeddings if speed critical (e.g., 256 dims)
3. **Caching**: Cache frequently searched queries
4. **Async API**: Leverage FastAPI async for concurrent requests
5. **LLM Optimization**: Use smaller models (Ollama) for local deployment

---

## 🔧 Configuration

### Environment Variables

Create `backend/.env`:

```env
# Endee Server
ENDEE_HOST=localhost
ENDEE_PORT=8080

# LLM Configuration
LLM_API_KEY=sk-your-api-key-here
LLM_MODEL=gpt-3.5-turbo

# Server
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000

# Embeddings
EMBEDDING_MODEL=all-MiniLM-L6-v2  # 384-dim, lightweight
# EMBEDDING_MODEL=all-mpnet-base-v2  # 768-dim, better quality
```

### Supported Embedding Models

- `all-MiniLM-L6-v2` (384 dims) - Fast, good balance
- `all-mpnet-base-v2` (768 dims) - Better quality
- `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` - Multilingual
- `sentence-transformers/all-roberta-large-v1` (1024 dims) - High quality

---

## 📝 Development

### Project Structure

```
endee-rag-app/
├── backend/
│   ├── main.py                 # FastAPI app
│   ├── endee_client.py         # Endee integration
│   ├── embeddings.py           # Sentence Transformers
│   ├── rag_engine.py           # RAG pipeline
│   ├── requirements.txt        # Python dependencies
│   ├── Dockerfile              # Container image
│   ├── .env.example            # Environment template
│   └── .gitignore
├── frontend/
│   ├── src/
│   │   ├── App.jsx             # Main component
│   │   ├── App.css             # Styling
│   │   ├── main.jsx            # Entry point
│   │   └── index.css           # Global styles
│   ├── index.html              # HTML template
│   ├── package.json            # Node dependencies
│   ├── vite.config.js          # Vite config
│   ├── Dockerfile              # Container image
│   ├── .gitignore
│   └── .dockerignore
├── docker-compose.yml          # Multi-container orchestration
├── README.md                   # This file
└── .gitignore
```

### Running Tests

```bash
# Backend tests (create tests/ directory)
pytest backend/tests/ -v

# Frontend tests
cd frontend
npm test
```

### Code Style

```bash
# Backend
pip install black isort
black backend/
isort backend/

# Frontend
npx prettier --write frontend/src/
```

---

## 🐛 Troubleshooting

### Endee Connection Error

**Problem**: `Connection refused: localhost:8080`

**Solution**:
```bash
# Check if Endee is running
docker ps | grep endee

# Restart Endee
docker-compose restart endee

# Check logs
docker-compose logs endee
```

### Search Returns No Results

**Problem**: Empty results despite documents indexed

**Solution**:
1. Verify index was created: `GET /api/v1/index/list`
2. Check documents were indexed: Upload via UI and verify response
3. Try broader query terms
4. Check Endee logs for errors: `docker-compose logs endee`

### Slow Search Performance

**Problem**: Searches taking >1 second

**Solution**:
1. Verify Endee has CPU/memory resources
2. Use smaller embedding model (all-MiniLM-L6-v2)
3. Reduce `top_k` parameter
4. Use vector quantization if available

### LLM Integration Not Working

**Problem**: RAG queries fail or return template answers

**Solution**:
1. Configure LLM in `backend/.env`:
   ```env
   LLM_API_KEY=sk-your-openai-key
   LLM_MODEL=gpt-3.5-turbo
   ```
2. OR use local Ollama:
   ```bash
   ollama pull llama2
   ollama serve
   # Then point LLM_MODEL to ollama endpoint
   ```

---

## 📖 Learning Resources

- [Endee GitHub](https://github.com/endee-io/endee)
- [Sentence Transformers Docs](https://www.sbert.net/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [RAG Pattern Overview](https://www.promptingguide.ai/applications/rag)
- [Vector Search Patterns](https://www.pinecone.io/learn/vector-search/)

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m "Add amazing feature"`)
4. Push to branch (`git push origin feature/amazing`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 🙋 Support & Questions

- **Issues**: Create GitHub Issue
- **Discussions**: Start discussion in GitHub Discussions
- **Email**: support@endee.io
- **Community**: Join Discord community

---

## 📈 Roadmap

- [ ] Multi-index query federation
- [ ] GraphQL endpoint
- [ ] Streaming responses
- [ ] Fine-tuning pipeline
- [ ] Hybrid search (keyword + semantic)
- [ ] Multi-language support
- [ ] Real-time collaboration

---

Built with ❤️ using Endee, FastAPI, and React
