"""Run the conformance corpus against the reference validator.

Usage:
    python test_corpus.py

Exit 0 if every case in valid.json passes and every case in invalid.json
fails. Otherwise prints a per-case summary and exits 1.
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from validate import A2ALError, validate

CORPUS = pathlib.Path(__file__).resolve().parents[1] / "corpus"


def _load(name: str):
    return json.loads((CORPUS / name).read_text(encoding="utf-8"))["cases"]


def main() -> int:
    failures = []

    for case in _load("valid.json"):
        try:
            validate(case["msg"])
        except A2ALError as e:
            failures.append(f"[valid:{case['name']}] expected VALID, got: {e}")

    for case in _load("invalid.json"):
        try:
            validate(case["msg"])
        except A2ALError:
            continue
        failures.append(
            f"[invalid:{case['name']}] expected INVALID ({case['reason']}), but validator accepted"
        )

    n_valid = len(_load("valid.json"))
    n_invalid = len(_load("invalid.json"))

    if failures:
        for f in failures:
            print(f, file=sys.stderr)
        print(f"\n{len(failures)} failure(s) of {n_valid + n_invalid} cases", file=sys.stderr)
        return 1

    print(f"OK: {n_valid} valid + {n_invalid} invalid cases")
    return 0


if __name__ == "__main__":
    sys.exit(main())
