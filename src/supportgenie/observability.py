"""Langfuse observability setup."""

from langfuse import Langfuse

from supportgenie.config import settings

_langfuse = None


def get_langfuse():
    global _langfuse
    if _langfuse is None:
        _langfuse = Langfuse(
            public_key=settings.langfuse_public_key.get_secret_value(),
            secret_key=settings.langfuse_secret_key.get_secret_value(),
            host=settings.langfuse_host,
        )
    return _langfuse


def is_enabled():
    return (
        settings.langfuse_public_key is not None
        and settings.langfuse_secret_key is not None
    )