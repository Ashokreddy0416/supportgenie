"""Answer questions with caching, with rich Langfuse tracing."""

import logging

from langfuse import observe, get_client

from supportgenie.generator import answer as generate_answer
from supportgenie.cache.exact import get_cached, set_cached
from supportgenie.cache.semantic import get_semantic_cached, set_semantic_cached

logger = logging.getLogger("supportgenie.cache")


@observe()
def answer_with_cache(question):
    langfuse = get_client()
    langfuse.update_current_span(input={"question": question})

    # 1. Exact-match cache — cheapest check first.
    cached = get_cached(question)
    if cached is not None:
        logger.info("Exact cache HIT")
        langfuse.update_current_span(
            output={"answer": cached},
            metadata={"cache": "exact_hit"},
        )
        return {"answer": cached, "source": "exact_cache"}

    # 2. Semantic cache — catches similar-meaning questions.
    cached = get_semantic_cached(question)
    if cached is not None:
        logger.info("Semantic cache HIT")
        langfuse.update_current_span(
            output={"answer": cached},
            metadata={"cache": "semantic_hit"},
        )
        return {"answer": cached, "source": "semantic_cache"}

    # 3. Miss — do the real (expensive) work.
    logger.info("Cache MISS — running full RAG pipeline")
    reply = generate_answer(question)

    # 4. Save to both caches for next time.
    set_cached(question, reply)
    set_semantic_cached(question, reply)

    langfuse.update_current_span(
        output={"answer": reply},
        metadata={"cache": "miss"},
    )
    return {"answer": reply, "source": "generated"}