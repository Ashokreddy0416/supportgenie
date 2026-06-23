"""Run a small RAGAS evaluation and print the scores."""

from supportgenie.evaluation.run_eval import run_evaluation

# A small sample so we stay well within Groq's free rate limits.
SAMPLE = [
    ("how do I cancel my order?", "Log into your account and go to your orders to cancel."),
    ("how can I get a refund?", "Check our refund policy and request a refund from your account."),
    ("how do I create an account?", "Click sign up and enter your details to create an account."),
    ("where is my order?", "You can track your order status from your account."),
    ("how do I change my shipping address?", "Update your shipping address in your account settings."),
]


def main():
    print("Running RAGAS evaluation on 5 questions (this takes a minute)...\n")
    result = run_evaluation(SAMPLE)
    print("\n=== RAGAS SCORES ===")
    print(result)


if __name__ == "__main__":
    main()