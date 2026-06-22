"""Connect to Qdrant (embedded) and manage our FAQ collection."""

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

DB_PATH = "data/qdrant"
COLLECTION = "faqs"
VECTOR_SIZE = 384


def get_client():
    return QdrantClient(path=DB_PATH)


def create_collection(client):
    client.recreate_collection(
        collection_name=COLLECTION,
        vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
    )
    print(f"Collection '{COLLECTION}' ready ({VECTOR_SIZE}-dim, cosine distance)")

def close_client(client):
    client.close()