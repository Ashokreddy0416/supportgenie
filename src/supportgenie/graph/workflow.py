"""Build and compile the SupportGenie agent graph."""

from langgraph.graph import StateGraph, START, END

from supportgenie.graph.state import AgentState
from supportgenie.graph.nodes import retrieve_node, generate_node


def build_graph():
    builder = StateGraph(AgentState)

    builder.add_node("retrieve", retrieve_node)
    builder.add_node("generate", generate_node)

    builder.add_edge(START, "retrieve")
    builder.add_edge("retrieve", "generate")
    builder.add_edge("generate", END)

    return builder.compile()