"""Build evaluation records by running questions through the RAG pipeline."""

from supportgenie.retriever import search
from supportgenie.generator import answer as generate_answer


def build_eval_record(question, ground_truth):
    hits = search(question, top_k=3)
    contexts = [h["answer"] for h in hits]
    response = generate_answer(question)

    return {
        "question": question,
        "answer": response,
        "contexts": contexts,
        "ground_truth": ground_truth,
    }