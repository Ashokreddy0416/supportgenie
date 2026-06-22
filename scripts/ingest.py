"""Load the FAQ knowledge base into Qdrant as searchable points."""

import json
from pathlib import Path

from qdrant_client.models import PointStruct

import sys
sys.path.insert(0, "src")

from supportgenie.embeddings import load_embedder, embed
from supportgenie.vector_store import get_client, create_collection, close_client

KB_PATH = "data/processed/knowledge_base.jsonl"


def read_kb(path):
    rows = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        rows.append(json.loads(line))
    return rows


def main():
    kb = read_kb(KB_PATH)
    print(f"Read {len(kb)} FAQ cards")

    model = load_embedder()
    vectors = embed(model, [row["response"] for row in kb])

    points = []
    for i, row in enumerate(kb):
        points.append(
            PointStruct(
                id=i,
                vector=vectors[i].tolist(),
                payload=row,
            )
        )

    client = get_client()
    create_collection(client)
    client.upsert(collection_name="faqs", points=points)
    print(f"Stored {len(points)} points in Qdrant")
    close_client(client)


if __name__ == "__main__":
    main()