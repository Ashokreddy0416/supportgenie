"""Detect prompt-injection and jailbreak attempts."""

INJECTION_PATTERNS = (
    "ignore previous instructions",
    "ignore all previous",
    "ignore your instructions",
    "disregard the above",
    "disregard your instructions",
    "you are now",
    "act as dan",
    "developer mode",
    "pretend the rules",
    "reveal your system prompt",
    "show me your prompt",
    "forget your instructions",
    "bypass your",
    "no restrictions",
)


def is_injection(text):
    lowered = text.lower()
    for pattern in INJECTION_PATTERNS:
        if pattern in lowered:
            return True
    return False


def check_injection(text):
    lowered = text.lower()
    matched = [p for p in INJECTION_PATTERNS if p in lowered]
    return matched