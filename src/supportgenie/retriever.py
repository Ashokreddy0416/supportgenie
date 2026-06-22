"""Find the most relevant FAQ cards for a customer's question."""

from supportgenie.embeddings import load_embedder, embed
from supportgenie.vector_store import get_client


def search(question, top_k=3):
    model = load_embedder()
    query_vector = embed(model, [question])[0]

    client = get_client()
    response = client.query_points(
        collection_name="faqs",
        query=query_vector.tolist(),
        limit=top_k,
    )

    hits = []
    for r in response.points:
        hits.append({
            "score": round(r.score, 3),
            "intent": r.payload["intent"],
            "answer": r.payload["response"],
        })
    return hits