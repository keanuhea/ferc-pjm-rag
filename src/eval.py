"""Run the eval set: 10 hardcoded questions, retrieved + answered, printed for review.

This is a manual-review eval, not a scored one. The point is to read the
generated answers alongside their citations and form a judgment about
retrieval quality and cross-document reasoning.
"""

from __future__ import annotations

import json
from pathlib import Path

from src.query import ask, format_citations

EVAL_PATH = Path(__file__).resolve().parent.parent / "eval_set.json"


def run_eval() -> None:
    questions = json.loads(EVAL_PATH.read_text())
    for i, item in enumerate(questions, 1):
        q = item["question"]
        print("=" * 80)
        print(f"[{i}/{len(questions)}] {q}")
        print("=" * 80)
        result = ask(q)
        print(f"\n{result.answer}\n")
        print("Sources:")
        print(format_citations(result.citations))
        print()


if __name__ == "__main__":
    run_eval()
