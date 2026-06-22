"""The shared state that flows through the agent graph."""

from typing import TypedDict


class AgentState(TypedDict):
    question: str
    route: str
    hits: list
    answer: str