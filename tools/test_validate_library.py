"""Test runner for tools/validate_library.py.

Walks tools/_test_fixtures/ and confirms the validator rejects each
intentionally-broken YAML and accepts the clean one. Also runs the
validator against the real library/ to confirm no regressions.

Run: python tools/test_validate_library.py
"""
from __future__ import annotations

import pathlib
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
VALIDATOR = REPO / "tools" / "validate_library.py"
FIXTURES = REPO / "tools" / "_test_fixtures"


def run(library_path: pathlib.Path, *, strict: bool = False) -> tuple[int, str]:
    """Run the validator against a single fixture file (treating it as a library/)."""
    args = [sys.executable, str(VALIDATOR), "--library-dir", str(library_path)]
    if strict:
        args.append("--strict")
    result = subprocess.run(args, capture_output=True, text=True)
    return result.returncode, (result.stdout + result.stderr)


def expect_fail(name: str) -> None:
    """Run the validator on a fixture (its parent dir, single-file dir) and expect non-zero exit."""
    fixture = FIXTURES / name
    # Create a per-fixture temp dir containing only this file
    import tempfile
    import shutil
    with tempfile.TemporaryDirectory() as td:
        target = pathlib.Path(td) / fixture.name
        shutil.copy(fixture, target)
        rc, out = run(pathlib.Path(td))
    if rc == 0:
        print(f"FAIL: {name} should have failed validation but exited 0")
        print(out)
        sys.exit(1)
    print(f"OK: {name} correctly rejected")


def expect_ok(name: str) -> None:
    """Run the validator and expect zero exit."""
    fixture = FIXTURES / name
    import tempfile
    import shutil
    with tempfile.TemporaryDirectory() as td:
        target = pathlib.Path(td) / fixture.name
        shutil.copy(fixture, target)
        rc, out = run(pathlib.Path(td))
    if rc != 0:
        print(f"FAIL: {name} should have passed validation but exited {rc}")
        print(out)
        sys.exit(1)
    print(f"OK: {name} correctly accepted")


def main() -> int:
    # Negative cases
    expect_fail("missing-domain.yaml")
    expect_fail("wrong-domain-name.yaml")
    expect_fail("missing-entries.yaml")
    expect_fail("empty-entries.yaml")
    expect_fail("missing-term.yaml")
    expect_fail("missing-expansion.yaml")
    expect_fail("term-with-dash-dash.yaml")
    expect_fail("expansion-with-newline.yaml")

    # Positive case
    expect_ok("valid.yaml")

    # Real library
    rc, out = run(REPO / "library")
    if rc != 0:
        print("FAIL: real library/ failed validation")
        print(out)
        return 1
    print(f"OK: real library/ passes (output: {out.strip()})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
