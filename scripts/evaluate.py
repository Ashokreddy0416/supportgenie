"""Run evaluation and enforce quality thresholds (a CI-ready gate)."""

import sys

from supportgenie.evaluation.run_eval import run_evaluation

# A small sample so we stay well within Groq's free rate limits.
SAMPLE = [
    ("how do I cancel my order?", "Log into your account and go to your orders to cancel."),
    ("how can I get a refund?", "Check our refund policy and request a refund from your account."),
    ("how do I create an account?", "Click sign up and enter your details to create an account."),
    ("where is my order?", "You can track your order status from your account."),
    ("how do I change my shipping address?", "Update your shipping address in your account settings."),
]

# Minimum acceptable scores. A change that drops below these fails the gate.
THRESHOLDS = {
    "faithfulness": 0.70,
    "answer_relevancy": 0.70,
}


def main():
    print("Running evaluation on 5 questions (this takes a minute)...\n")
    scores = run_evaluation(SAMPLE)

    print("\n=== SCORES vs THRESHOLDS ===")
    passed = True
    for metric, threshold in THRESHOLDS.items():
        score = scores[metric]
        ok = score >= threshold
        status = "PASS" if ok else "FAIL"
        print(f"  {metric:20s}: {score:.2f}  (min {threshold:.2f})  [{status}]")
        if not ok:
            passed = False

    print()
    if passed:
        print("QUALITY GATE PASSED")
        return 0
    else:
        print("QUALITY GATE FAILED — quality below threshold")
        return 1


if __name__ == "__main__":
    sys.exit(main())