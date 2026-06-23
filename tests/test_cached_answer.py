"""Tests for the cached answer flow, using mocking to avoid real Groq calls."""

from unittest.mock import patch

from supportgenie.cache.exact import set_cached


def test_exact_cache_hit_skips_generation():
    # Pre-load the cache so this question is already known.
    set_cached("what is your return policy", "Returns within 30 days.")

    with patch("supportgenie.cached_answer.generate_answer") as fake_generate:
        from supportgenie.cached_answer import answer_with_cache
        result = answer_with_cache("what is your return policy")

    assert result["source"] == "exact_cache"
    assert result["answer"] == "Returns within 30 days."
    fake_generate.assert_not_called()


def test_cache_miss_calls_generation_and_saves():
    with patch("supportgenie.cached_answer.generate_answer") as fake_generate, \
         patch("supportgenie.cached_answer.get_semantic_cached", return_value=None), \
         patch("supportgenie.cached_answer.set_semantic_cached"):

        fake_generate.return_value = "A freshly generated answer."

        from supportgenie.cached_answer import answer_with_cache
        result = answer_with_cache("a brand new unique question 9876")

    assert result["source"] == "generated"
    assert result["answer"] == "A freshly generated answer."
    fake_generate.assert_called_once()