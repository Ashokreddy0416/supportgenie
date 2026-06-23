"""Semantic cache: return cached answers for similar-meaning questions."""

from qdrant_client.models import Distance, VectorParams, PointStruct

from supportgenie.embeddings import load_embedder, embed
from supportgenie.vector_store import get_client

CACHE_COLLECTION = "answer_cache"
VECTOR_SIZE = 384
SIMILARITY_THRESHOLD = 0.92

_next_id = 0


def ensure_cache_collection(client):
    existing = [c.name for c in client.get_collections().collections]
    if CACHE_COLLECTION not in existing:
        client.create_collection(
            collection_name=CACHE_COLLECTION,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
        )


def get_semantic_cached(question):
    model = load_embedder()
    query_vector = embed(model, [question])[0]

    client = get_client()
    ensure_cache_collection(client)

    response = client.query_points(
        collection_name=CACHE_COLLECTION,
        query=query_vector.tolist(),
        limit=1,
    )

    if response.points and response.points[0].score >= SIMILARITY_THRESHOLD:
        return response.points[0].payload["answer"]
    return None


def set_semantic_cached(question, answer):
    global _next_id
    model = load_embedder()
    vector = embed(model, [question])[0]

    client = get_client()
    ensure_cache_collection(client)

    client.upsert(
        collection_name=CACHE_COLLECTION,
        points=[PointStruct(id=_next_id, vector=vector.tolist(), payload={"question": question, "answer": answer})],
    )
    _next_id += 1