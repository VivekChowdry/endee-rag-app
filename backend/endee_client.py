"""
Endee vector database client.
Handles connection, index management, and vector operations.
"""

import requests
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class EndeeClient:
    """Client for interacting with Endee vector database."""

    def __init__(self, host: str = "localhost", port: int = 8080):
        """
        Initialize Endee client.

        Args:
            host: Endee server host
            port: Endee server port
        """
        self.base_url = f"http://{host}:{port}"
        self.session = requests.Session()

    def create_index(self, index_name: str, dimension: int = 384) -> Dict[str, Any]:
        """
        Create a new index.

        Args:
            index_name: Name of the index
            dimension: Dimension of vectors (default 384 for Sentence Transformers)

        Returns:
            Response from Endee
        """
        try:
            response = self.session.post(
                f"{self.base_url}/api/v1/index/create",
                json={"name": index_name, "dimension": dimension},
            )
            response.raise_for_status()
            logger.info(f"Created index: {index_name}")
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to create index {index_name}: {e}")
            raise

    def list_indices(self) -> List[str]:
        """
        List all indices.

        Returns:
            List of index names
        """
        try:
            response = self.session.get(f"{self.base_url}/api/v1/index/list")
            response.raise_for_status()
            return response.json().get("indices", [])
        except requests.RequestException as e:
            logger.error(f"Failed to list indices: {e}")
            raise

    def insert_vectors(
        self, index_name: str, vectors: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Insert vectors into an index.

        Args:
            index_name: Name of the index
            vectors: List of vectors with id, vector, and optional metadata

        Returns:
            Response from Endee
        """
        try:
            payload = {
                "index_name": index_name,
                "vectors": vectors,
            }
            response = self.session.post(
                f"{self.base_url}/api/v1/upsert",
                json=payload,
            )
            response.raise_for_status()
            logger.info(f"Inserted {len(vectors)} vectors into {index_name}")
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to insert vectors: {e}")
            raise

    def search(
        self,
        index_name: str,
        query_vector: List[float],
        top_k: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Search for similar vectors.

        Args:
            index_name: Name of the index
            query_vector: Query vector embedding
            top_k: Number of top results to return

        Returns:
            List of search results with id, score, and metadata
        """
        try:
            payload = {
                "index_name": index_name,
                "vector": query_vector,
                "k": top_k,
            }
            response = self.session.post(
                f"{self.base_url}/api/v1/search",
                json=payload,
            )
            response.raise_for_status()
            results = response.json().get("results", [])
            logger.info(f"Search completed for {index_name}, found {len(results)} results")
            return results
        except requests.RequestException as e:
            logger.error(f"Search failed: {e}")
            raise

    def delete_index(self, index_name: str) -> Dict[str, Any]:
        """
        Delete an index.

        Args:
            index_name: Name of the index to delete

        Returns:
            Response from Endee
        """
        try:
            response = self.session.post(
                f"{self.base_url}/api/v1/index/delete",
                json={"name": index_name},
            )
            response.raise_for_status()
            logger.info(f"Deleted index: {index_name}")
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to delete index {index_name}: {e}")
            raise
