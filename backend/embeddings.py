"""
Embedding service using Sentence Transformers.
Generates vector embeddings for text.
"""

from sentence_transformers import SentenceTransformer
import logging
from typing import List

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Service for generating text embeddings."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize embedding service.

        Args:
            model_name: Sentence Transformer model name (default: all-MiniLM-L6-v2, dimension=384)
        """
        logger.info(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        logger.info(f"Embedding dimension: {self.dimension}")

    def embed(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for texts.

        Args:
            texts: List of text strings

        Returns:
            List of embedding vectors
        """
        try:
            embeddings = self.model.encode(texts, convert_to_tensor=False)
            logger.info(f"Generated embeddings for {len(texts)} texts")
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"Failed to generate embeddings: {e}")
            raise

    def embed_single(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.

        Args:
            text: Text string

        Returns:
            Embedding vector
        """
        return self.embed([text])[0]
