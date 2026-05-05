# A2AL Reference Validator

Reference validator and conformance test corpus for A2AL/2.0.

> **Status:** WIP. Python reference implementation lives in [`python/`](./python/).

## Layout

| Path | Contents |
|---|---|
| [`python/`](./python) | Reference validator (`validate.py`) and corpus runner (`test_corpus.py`) |
| [`corpus/valid.json`](./corpus/valid.json) | Positive cases — every conformant validator MUST accept |
| [`corpus/invalid.json`](./corpus/invalid.json) | Negative cases — every conformant validator MUST reject |

## Quick Start

```bash
cd python
python test_corpus.py
```

## Scope

- **Validator** — verify type bans, archetype shape, ordering, and forward-compat preservation rules per `specs/A2A-Grammar.md`.
- **Conformance corpus** — golden positive and negative test cases. Implementations in any language may run against `corpus/*.json` directly; the corpus is the binding behavioral definition.

## Non-Goals

- Repairing malformed messages — the rulebook explicitly forbids this.
- Decoding into a domain object model — A2AL is intentionally schema-less above the grammar layer.
- Transport adapters (HTTP/WS/MQTT/etc.) — A2AL is transport-agnostic.

## Other Languages

Ports to TypeScript, Go, and Rust are welcome. Any port should pass the corpus untouched.
