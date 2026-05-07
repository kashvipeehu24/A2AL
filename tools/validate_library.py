"""A2AL library validator.

Walks a library directory (default: library/) and validates each YAML
file against the schema documented in library/README.md.

Exits 0 if all checks pass, 1 with errors on stderr otherwise.
Use --strict to promote warnings to errors.

Run: python tools/validate_library.py
"""
from __future__ import annotations

import argparse
import pathlib
import sys
from typing import Any

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)


REQUIRED_TOP = {"domain", "description", "entries"}
REQUIRED_ENTRY = {"term", "expansion"}
ALLOWED_ENTRY = REQUIRED_ENTRY | {"example", "notes", "tokens", "usage_count", "accepted_date"}


class Issue:
    def __init__(self, level: str, file: str, where: str, msg: str):
        self.level = level  # "ERROR" or "WARN"
        self.file = file
        self.where = where  # "header" or "entry[N]"
        self.msg = msg

    def __str__(self) -> str:
        return f"{self.level}: {self.file}:{self.where}: {self.msg}"


def validate_file(path: pathlib.Path, all_terms: dict[str, str]) -> list[Issue]:
    """Validate one library/*.yaml file. Returns list of issues.

    `all_terms` is a mutable mapping {term -> file} accumulated across files
    for cross-file uniqueness checking. Caller is responsible for passing
    the same mapping to each call.
    """
    issues: list[Issue] = []
    file_label = path.name

    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        issues.append(Issue("ERROR", file_label, "yaml", f"YAML parse error: {e}"))
        return issues

    if not isinstance(data, dict):
        issues.append(Issue("ERROR", file_label, "header", "top-level must be a mapping"))
        return issues

    # Top-level keys
    keys = set(data.keys())
    missing = REQUIRED_TOP - keys
    if missing:
        for m in sorted(missing):
            issues.append(Issue("ERROR", file_label, "header", f"missing required top-level field: {m}"))
    extra = keys - REQUIRED_TOP
    if extra:
        for e in sorted(extra):
            issues.append(Issue("ERROR", file_label, "header", f"unknown top-level field: {e}"))
    if missing or extra:
        # Don't try to validate the rest if header is malformed
        return issues

    # domain matches filename stem
    expected_domain = path.stem
    if data["domain"] != expected_domain:
        issues.append(Issue("ERROR", file_label, "header",
                            f"domain field is {data['domain']!r} but filename stem is {expected_domain!r}"))

    # description type and length
    if not isinstance(data["description"], str) or len(data["description"]) < 10:
        issues.append(Issue("ERROR", file_label, "header",
                            f"description must be a string of >=10 chars; got {data.get('description')!r}"))

    # entries non-empty list
    entries = data["entries"]
    if not isinstance(entries, list) or not entries:
        issues.append(Issue("ERROR", file_label, "header", "entries must be a non-empty list"))
        return issues

    # per-entry validation
    seen_terms_in_file: set[str] = set()
    for i, entry in enumerate(entries):
        where = f"entries[{i}]"
        if not isinstance(entry, dict):
            issues.append(Issue("ERROR", file_label, where, "entry must be a mapping"))
            continue

        # required fields
        for f in REQUIRED_ENTRY:
            if f not in entry:
                issues.append(Issue("ERROR", file_label, where, f"missing required field: {f}"))

        # unknown fields
        for f in entry:
            if f not in ALLOWED_ENTRY:
                issues.append(Issue("ERROR", file_label, where, f"unknown field: {f}"))

        if "term" not in entry or "expansion" not in entry:
            continue

        # term checks
        term = entry["term"]
        if not isinstance(term, str) or not term:
            issues.append(Issue("ERROR", file_label, where, f"term must be a non-empty string; got {term!r}"))
            continue
        if any(c.isspace() for c in term):
            issues.append(Issue("ERROR", file_label, where, f"term must not contain whitespace; got {term!r}"))
        if "--" in term:
            issues.append(Issue("ERROR", file_label, where, f"term must not contain '--' (clashes with spec separator); got {term!r}"))
        if "\n" in term:
            issues.append(Issue("ERROR", file_label, where, f"term must not contain newlines; got {term!r}"))

        # expansion checks
        exp = entry["expansion"]
        if not isinstance(exp, str) or len(exp) < 2:
            issues.append(Issue("ERROR", file_label, where, f"expansion must be a string >=2 chars; got {exp!r}"))
        else:
            if "--" in exp:
                issues.append(Issue("ERROR", file_label, where, f"expansion must not contain '--'; got {exp!r}"))
            if "\n" in exp:
                issues.append(Issue("ERROR", file_label, where, f"expansion must not contain newlines; got {exp!r}"))

        # optional example/notes type-checks
        for opt in ("example", "notes"):
            if opt in entry and not isinstance(entry[opt], str):
                issues.append(Issue("ERROR", file_label, where, f"{opt} must be a string"))
            if opt in entry and isinstance(entry[opt], str) and "\n" in entry[opt]:
                issues.append(Issue("ERROR", file_label, where, f"{opt} must not contain newlines"))

        # within-file duplicate
        if term in seen_terms_in_file:
            issues.append(Issue("ERROR", file_label, where, f"duplicate term within file: {term!r}"))
        seen_terms_in_file.add(term)

        # cross-file duplicate
        if term in all_terms:
            issues.append(Issue("ERROR", file_label, where,
                                f"term {term!r} also appears in {all_terms[term]}; terms must be unique across the library"))
        else:
            all_terms[term] = file_label

        # Style warnings
        if "example" in entry and isinstance(entry["example"], str) and term not in entry["example"]:
            issues.append(Issue("WARN", file_label, where, f"example does not contain the term {term!r}"))
        if isinstance(exp, str) and term in exp.split():
            issues.append(Issue("WARN", file_label, where, f"expansion contains the term {term!r} as its own word; possibly circular"))

    return issues


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--library-dir", default="library", help="Directory containing *.yaml library files")
    p.add_argument("--strict", action="store_true", help="Promote warnings to errors")
    args = p.parse_args()

    lib_dir = pathlib.Path(args.library_dir)
    if not lib_dir.is_dir():
        print(f"ERROR: not a directory: {lib_dir}", file=sys.stderr)
        return 1

    yaml_files = sorted(lib_dir.glob("*.yaml"))
    if not yaml_files:
        print(f"ERROR: no *.yaml files in {lib_dir}", file=sys.stderr)
        return 1

    all_terms: dict[str, str] = {}
    all_issues: list[Issue] = []
    total_entries = 0

    for f in yaml_files:
        issues = validate_file(f, all_terms)
        all_issues.extend(issues)
        # count entries even if issues (best-effort)
        try:
            data = yaml.safe_load(f.read_text(encoding="utf-8"))
            if isinstance(data, dict) and isinstance(data.get("entries"), list):
                total_entries += len(data["entries"])
        except Exception:
            pass

    errors = [i for i in all_issues if i.level == "ERROR"]
    warnings = [i for i in all_issues if i.level == "WARN"]

    for i in all_issues:
        print(str(i), file=sys.stderr)

    if errors or (args.strict and warnings):
        print(f"\n{len(errors)} error(s), {len(warnings)} warning(s); strict={args.strict}", file=sys.stderr)
        return 1

    print(f"OK: {total_entries} entries across {len(yaml_files)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
