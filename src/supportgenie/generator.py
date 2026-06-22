"""Generate a grounded answer using Groq, based on retrieved FAQ context."""

import os

from dotenv import load_dotenv
from groq import Groq

from supportgenie.retriever import search

load_dotenv()

MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """You are SupportGenie, a helpful customer-support assistant.
Answer the customer's question using ONLY the provided FAQ context.
If the context doesn't contain the answer, say you don't have that information
and offer to connect them to a human agent. Be warm, clear, and concise."""


def answer(question):
    hits = search(question, top_k=3)
    context = "\n\n".join(f"- {h['answer']}" for h in hits)

    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"FAQ context:\n{context}\n\nCustomer question: {question}"},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content