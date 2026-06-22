"""The worker nodes that make up the agent graph."""

import os

from dotenv import load_dotenv
from groq import Groq

from supportgenie.retriever import search
from supportgenie.graph.state import AgentState

load_dotenv()

MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """You are SupportGenie, a helpful customer-support assistant.
Answer using ONLY the provided FAQ context. If the context doesn't contain the
answer, say you don't have that information and offer a human agent.
Be warm, clear, and concise."""


def retrieve_node(state: AgentState) -> dict:
    hits = search(state["question"], top_k=3)
    return {"hits": hits}


def generate_node(state: AgentState) -> dict:
    context = "\n\n".join(f"- {h['answer']}" for h in state["hits"])

    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"FAQ context:\n{context}\n\nCustomer question: {state['question']}"},
        ],
        temperature=0.3,
    )
    return {"answer": response.choices[0].message.content}

def router_node(state: AgentState) -> dict:
    question = state["question"].lower().strip()
    greetings = ("hi", "hello", "hey", "good morning", "good evening", "thanks", "thank you")
    if any(question.startswith(g) for g in greetings):
        return {"route": "greeting"}
    return {"route": "faq"}


def greeting_node(state: AgentState) -> dict:
    return {"answer": "Hello! I'm SupportGenie. How can I help you with your order or account today?"}