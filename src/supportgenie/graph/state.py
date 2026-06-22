"""The shared state that flows through the agent graph."""

from typing import Annotated, TypedDict

from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    question: str
    route: str
    hits: list
    answer: str
    messages: Annotated[list, add_messages]