"""Build and compile the SupportGenie agent graph."""

from langgraph.graph import StateGraph, START, END

from supportgenie.graph.state import AgentState
from supportgenie.graph.nodes import (
    router_node,
    greeting_node,
    retrieve_node,
    generate_node,
)
def build_graph():
    builder = StateGraph(AgentState)

    builder.add_node("router", router_node)
    builder.add_node("greeting", greeting_node)
    builder.add_node("retrieve", retrieve_node)
    builder.add_node("generate", generate_node)

    builder.add_edge(START, "router")

    builder.add_conditional_edges(
        "router",
        lambda state: state["route"],
        {"greeting": "greeting", "faq": "retrieve"},
    )

    builder.add_edge("greeting", END)
    builder.add_edge("retrieve", "generate")
    builder.add_edge("generate", END)

    return builder.compile()