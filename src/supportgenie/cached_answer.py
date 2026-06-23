"""Answer questions with caching: check caches first, do RAG only on a miss."""

import logging

from supportgenie.generator import answer as generate_answer
from supportgenie.cache.exact import get_cached, set_cached
from supportgenie.cache.semantic import get_semantic_cached, set_semantic_cached

logger = logging.getLogger("supportgenie.cache")


def answer_with_cache(question):
    # 1. Exact-match cache — cheapest check first.
    cached = get_cached(question)
    if cached is not None:
        logger.info("Exact cache HIT")
        return {"answer": cached, "source": "exact_cache"}

    # 2. Semantic cache — catches similar-meaning questions.
    cached = get_semantic_cached(question)
    if cached is not None:
        logger.info("Semantic cache HIT")
        return {"answer": cached, "source": "semantic_cache"}

    # 3. Miss — do the real (expensive) work.
    logger.info("Cache MISS — running full RAG pipeline")
    reply = generate_answer(question)

    # 4. Save to both caches for next time.
    set_cached(question, reply)
    set_semantic_cached(question, reply)

    return {"answer": reply, "source": "generated"}