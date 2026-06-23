"""Lightweight RAG evaluation using our own LLM-as-judge (no RAGAS needed)."""

import os
import re

from dotenv import load_dotenv
from groq import Groq

from supportgenie.evaluation.build_records import build_eval_record

load_dotenv()

MODEL = "llama-3.3-70b-versatile"

FAITHFULNESS_PROMPT = """You are evaluating a customer-support answer.
Given the CONTEXT and the ANSWER, rate how well the answer is supported by the
context — i.e. does it avoid making up facts not in the context?

Give a score from 0 to 10, where 10 means every claim is supported by the
context, and 0 means the answer is entirely unsupported.
Reply with ONLY the number."""

RELEVANCY_PROMPT = """You are evaluating a customer-support answer.
Given the QUESTION and the ANSWER, rate how well the answer actually addresses
the question that was asked.

Give a score from 0 to 10, where 10 means the answer fully addresses the
question, and 0 means it is completely off-topic.
Reply with ONLY the number."""


def _score(client, system_prompt, user_content):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        temperature=0.0,
    )
    text = response.choices[0].message.content.strip()
    match = re.search(r"\d+", text)
    if match is None:
        return 0.0
    return min(int(match.group()), 10) / 10.0


def run_evaluation(qa_pairs):
    client = Groq(api_key=os.environ["GROQ_API_KEY"])

    faithfulness_scores = []
    relevancy_scores = []

    for question, ground_truth in qa_pairs:
        record = build_eval_record(question, ground_truth)
        context = "\n".join(record["contexts"])

        f = _score(
            client,
            FAITHFULNESS_PROMPT,
            f"CONTEXT:\n{context}\n\nANSWER:\n{record['answer']}",
        )
        r = _score(
            client,
            RELEVANCY_PROMPT,
            f"QUESTION:\n{question}\n\nANSWER:\n{record['answer']}",
        )

        faithfulness_scores.append(f)
        relevancy_scores.append(r)
        print(f"  '{question[:40]}...' -> faithfulness={f:.2f}, relevancy={r:.2f}")

    return {
        "faithfulness": sum(faithfulness_scores) / len(faithfulness_scores),
        "answer_relevancy": sum(relevancy_scores) / len(relevancy_scores),
    }