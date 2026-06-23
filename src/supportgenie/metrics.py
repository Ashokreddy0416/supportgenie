"""Custom Prometheus metrics for SupportGenie."""

from prometheus_client import Counter

cache_hits = Counter(
    "supportgenie_cache_hits_total",
    "Total number of cache hits",
    ["cache_type"],
)

cache_misses = Counter(
    "supportgenie_cache_misses_total",
    "Total number of cache misses (full RAG runs)",
)