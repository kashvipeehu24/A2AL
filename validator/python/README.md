# A2AL Reference Validator (Python)

Reference implementation tracking `specs/A2A-Grammar.md`. **Status: WIP.**

## Requirements

Python 3.9+ (standard library only — no external dependencies).

## Run a single message

```bash
echo '[[2,"ctx",0,2,1],["Δ",[1,0,"ID-1"]]]' | python validate.py
# VALID

python validate.py path/to/msg.json
```

Exits 0 if valid, 1 with a reason on stderr if invalid.

## Run the conformance corpus

```bash
python test_corpus.py
```

The corpus lives at `../corpus/valid.json` and `../corpus/invalid.json`. Every positive case must be accepted; every negative case must be rejected (the documented reason is illustrative — exact error wording is implementation-defined).

## What this validator checks

- Type bans (no null / bool / float / object) anywhere in the tree
- Top-level shape `[H, B]`
- Header positional types and `v == 2`
- Body lane tag matches `typ`
- Per-archetype item shape (A1–A7)
- Canonical ordering per `specs/A2A-Grammar.md` §7.2
- Forward-compat: unknown `typ` values are accepted (preserved by relays)

## What it does not yet check

- `mid` / `cid` regex shape
- `ctx` NFC normalization
- Whitespace canonicalization (operates on already-parsed JSON)
- Whether trailing positional fields exceed defined positions

These will be added as the validator matures.
