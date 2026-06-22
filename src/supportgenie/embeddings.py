"""Turn text into vectors (lists of numbers that capture meaning)."""

from sentence_transformers import SentenceTransformer

MODEL_NAME = "BAAI/bge-small-en-v1.5"


def load_embedder():
    return SentenceTransformer(MODEL_NAME)


def embed(model, texts):
    return model.encode(texts, normalize_embeddings=True)