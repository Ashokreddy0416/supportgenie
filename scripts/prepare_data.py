"""Prepare SupportGenie's data from the Bitext customer-support dataset.

We build this script up across several small steps. Right now it does the
smallest useful thing: download the dataset and confirm it loaded.
"""

from datasets import load_dataset

DATASET_ID = "bitext/Bitext-customer-support-llm-chatbot-training-dataset"


def main() -> None:
    dataset = load_dataset(DATASET_ID, split="train")
    df = dataset.to_pandas()

    print(f"Loaded {len(df):,} rows")
    print(f"Columns: {list(df.columns)}")


if __name__ == "__main__":
    main()