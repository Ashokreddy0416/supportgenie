"""Prepare SupportGenie's data from the Bitext customer-support dataset.

We build this script up across several small steps. Right now it does the
smallest useful thing: download the dataset and confirm it loaded.
"""

from datasets import load_dataset
import json
from pathlib import Path

DATASET_ID = "bitext/Bitext-customer-support-llm-chatbot-training-dataset"

def explore(df):
    print(f"Rows: {len(df):,}")
    print(f"Categories: {df['category'].nunique()}")
    print(df["category"].value_counts())
    print(f"Intents: {df['intent'].nunique()}")
    print(df["instruction"].head(5).to_string())

def build_knowledge_base(df):
    df = df.assign(length=df["response"].str.len())
    best_rows = df.groupby("intent")["length"].idxmax()
    kb = df.loc[best_rows, ["intent", "category", "response"]]
    return kb.reset_index(drop=True)

def build_eval_set(df, kb, per_intent=5, seed=42):
    answer_for = dict(zip(kb["intent"], kb["response"]))
    pool = df.drop_duplicates(subset=["instruction"])
    sample = pool.groupby("intent").sample(n=per_intent, random_state=seed)

    exam = sample[["instruction", "intent", "category"]].copy()
    exam["correct_answer"] = exam["intent"].map(answer_for)
    return exam.reset_index(drop=True)

def save_jsonl(df, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in df.to_dict(orient="records"):
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"Saved {len(df)} rows to {path}")


def main() -> None:
    dataset = load_dataset(DATASET_ID, split="train")
    df = dataset.to_pandas()

    kb = build_knowledge_base(df)
    exam = build_eval_set(df, kb)

    save_jsonl(kb, "data/processed/knowledge_base.jsonl")
    save_jsonl(exam, "data/processed/eval_set.jsonl")


if __name__ == "__main__":
    main()