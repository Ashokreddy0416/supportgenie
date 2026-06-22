"""Check whether an answer is grounded in the retrieved context."""

import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

MODEL = "llama-3.3-70b-versatile"

JUDGE_PROMPT = """You are a strict fact-checker. Given CONTEXT and an ANSWER,
decide if every claim in the ANSWER is directly supported by the CONTEXT.

Reply with exactly one word:
- GROUNDED if all claims are supported by the context.
- UNGROUNDED if the answer contains any claim not found in the context.

Do not explain. Reply with only GROUNDED or UNGROUNDED."""


def is_grounded(answer, context):
    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": JUDGE_PROMPT},
            {"role": "user", "content": f"CONTEXT:\n{context}\n\nANSWER:\n{answer}"},
        ],
        temperature=0.0,
    )
    verdict = response.choices[0].message.content.strip().upper()
    return verdict.startswith("GROUNDED")