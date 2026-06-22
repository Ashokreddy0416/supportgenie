"""The safety policy: run all guardrails and decide the outcome."""

from supportgenie.guardrails.injection import is_injection
from supportgenie.guardrails.pii import redact_pii
from supportgenie.guardrails.groundedness import is_grounded

BLOCKED_MESSAGE = (
    "I'm sorry, but I can't help with that request. "
    "Is there something about your order or account I can assist with?"
)

FALLBACK_MESSAGE = (
    "I'm not fully certain about that based on our help center. "
    "Let me connect you with a human agent who can give you an accurate answer."
)


def check_input(text):
    if is_injection(text):
        return {"allowed": False, "reason": "injection", "text": BLOCKED_MESSAGE}

    cleaned = redact_pii(text)
    return {"allowed": True, "reason": "ok", "text": cleaned}


def check_output(answer, context):
    if not is_grounded(answer, context):
        return {"safe": False, "answer": FALLBACK_MESSAGE}
    return {"safe": True, "answer": answer}