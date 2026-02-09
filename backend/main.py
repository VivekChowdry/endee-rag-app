"""
FastAPI server for Endee RAG + Semantic Search application.
Provides endpoints for document indexing, semantic search, and RAG retrieval.
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv
import logging

from endee_client import EndeeClient
from embeddings import EmbeddingService
from rag_engine import RAGEngine

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Endee RAG & Semantic Search API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
endee_client = EndeeClient(
    host=os.getenv("ENDEE_HOST", "localhost"),
    port=int(os.getenv("ENDEE_PORT", 8080)),
)
embedding_service = EmbeddingService()
rag_engine = RAGEngine(
    embedding_service=embedding_service,
    endee_client=endee_client,
    llm_api_key=os.getenv("LLM_API_KEY"),
    llm_model=os.getenv("LLM_MODEL", "gpt-3.5-turbo"),
)


# Request/Response models
class DocumentChunk(BaseModel):
    id: str
    content: str
    metadata: dict = {}


class SearchQuery(BaseModel):
    query: str
    top_k: int = 5


class RAGQuery(BaseModel):
    question: str
    top_k: int = 5


class SearchResult(BaseModel):
    id: str
    content: str
    similarity: float
    metadata: dict


class RAGResponse(BaseModel):
    answer: str
    sources: List[SearchResult]


# Health check
@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Endee RAG & Semantic Search API"}


# Index management
@app.post("/api/v1/index/create")
async def create_index(index_name: str, dimension: int = 384):
    """Create a new index in Endee."""
    try:
        result = endee_client.create_index(index_name, dimension)
        logger.info(f"Created index: {index_name}")
        return {"index": index_name, "dimension": dimension, "status": "created"}
    except Exception as e:
        logger.error(f"Failed to create index: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/index/list")
async def list_indices():
    """List all indices in Endee."""
    try:
        indices = endee_client.list_indices()
        return {"indices": indices}
    except Exception as e:
        logger.error(f"Failed to list indices: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Document indexing
@app.post("/api/v1/documents/index")
async def index_documents(
    index_name: str,
    documents: List[DocumentChunk],
):
    """Index documents with embeddings in Endee."""
    try:
        # Generate embeddings for documents
        texts = [doc.content for doc in documents]
        embeddings = embedding_service.embed(texts)

        # Index in Endee
        vectors = [
            {
                "id": doc.id,
                "vector": embeddings[i],
                "metadata": {
                    "content": doc.content,
                    **doc.metadata,
                },
            }
            for i, doc in enumerate(documents)
        ]

        endee_client.insert_vectors(index_name, vectors)
        logger.info(f"Indexed {len(documents)} documents in {index_name}")
        return {
            "indexed": len(documents),
            "index": index_name,
            "status": "success",
        }
    except Exception as e:
        logger.error(f"Failed to index documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Semantic search
@app.post("/api/v1/search/semantic")
async def semantic_search(index_name: str, query: SearchQuery) -> dict:
    """Perform semantic search using embeddings."""
    try:
        # Embed query
        query_embedding = embedding_service.embed([query.query])[0]

        # Search in Endee
        results = endee_client.search(
            index_name, query_embedding, top_k=query.top_k
        )

        # Format results
        formatted_results = [
            SearchResult(
                id=r["id"],
                content=r["metadata"].get("content", ""),
                similarity=r.get("score", 0),
                metadata=r.get("metadata", {}),
            )
            for r in results
        ]

        logger.info(f"Semantic search completed for query: {query.query}")
        return {
            "query": query.query,
            "results": [r.dict() for r in formatted_results],
        }
    except Exception as e:
        logger.error(f"Semantic search failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# RAG retrieval
@app.post("/api/v1/rag/query")
async def rag_query(index_name: str, query: RAGQuery) -> dict:
    """Perform RAG query: retrieve context + generate answer."""
    try:
        # Retrieve context using semantic search
        query_embedding = embedding_service.embed([query.question])[0]
        search_results = endee_client.search(
            index_name, query_embedding, top_k=query.top_k
        )

        # Extract sources
        sources = [
            SearchResult(
                id=r["id"],
                content=r["metadata"].get("content", ""),
                similarity=r.get("score", 0),
                metadata=r.get("metadata", {}),
            )
            for r in search_results
        ]

        # Generate answer using RAG
        answer = await rag_engine.generate_answer(query.question, sources)

        logger.info(f"RAG query completed for question: {query.question}")
        return {
            "question": query.question,
            "answer": answer,
            "sources": [s.dict() for s in sources],
        }
    except Exception as e:
        logger.error(f"RAG query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Document upload (simplified)
@app.post("/api/v1/documents/upload")
async def upload_document(
    index_name: str,
    file: UploadFile = File(...),
):
    """Upload and index a document."""
    try:
        content = await file.read()
        text = content.decode("utf-8")

        # Split into chunks (simple implementation)
        chunks = text.split("\n\n")[:10]  # Limit to 10 chunks for demo

        documents = [
            DocumentChunk(
                id=f"{file.filename}_{i}",
                content=chunk,
                metadata={"source": file.filename, "chunk_index": i},
            )
            for i, chunk in enumerate(chunks)
            if chunk.strip()
        ]

        # Index documents
        embeddings = embedding_service.embed([doc.content for doc in documents])
        vectors = [
            {
                "id": doc.id,
                "vector": embeddings[i],
                "metadata": {
                    "content": doc.content,
                    **doc.metadata,
                },
            }
            for i, doc in enumerate(documents)
        ]

        endee_client.insert_vectors(index_name, vectors)
        logger.info(f"Uploaded and indexed {file.filename}")
        return {
            "filename": file.filename,
            "chunks_indexed": len(documents),
            "status": "success",
        }
    except Exception as e:
        logger.error(f"Document upload failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
