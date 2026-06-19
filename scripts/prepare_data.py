"""Prepare SupportGenie's data from the Bitext customer-support dataset.

We build this script up across several small steps. Right now it does the
smallest useful thing: download the dataset and confirm it loaded.
"""

from datasets import load_dataset

DATASET_ID = "bitext/Bitext-customer-support-llm-chatbot-training-dataset"

def explore(df):
    print(f"Rows: {len(df):,}")
    print(f"Categories: {df['category'].nunique()}")
    print(df["category"].value_counts())
    print(f"Intents: {df['intent'].nunique()}")
    print(df["instruction"].head(5).to_string())


def main() -> None:
    dataset = load_dataset(DATASET_ID, split="train")
    df = dataset.to_pandas()
    explore(df)


if __name__ == "__main__":
    main()