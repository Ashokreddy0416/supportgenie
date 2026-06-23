"""Exact-match cache: remember answers to identical questions."""

_cache = {}


def _normalize(question):
    return question.strip().lower()


def get_cached(question):
    key = _normalize(question)
    return _cache.get(key)


def set_cached(question, answer):
    key = _normalize(question)
    _cache[key] = answer


def cache_size():
    return len(_cache)