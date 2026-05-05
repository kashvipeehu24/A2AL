# A2AL Examples

Worked examples for A2AL/2.0. **Status: work in progress.** Examples here are drafts and may not yet satisfy every canonical-ordering rule in `specs/A2A-Grammar.md` §7.2 — the reference validator under `validator/` will normalize them as it matures.

## Per-Archetype Examples

Each file shows one realistic message in an indented (human-readable) JSON form. Production output should be canonical (no whitespace).

| File | Archetype | Lane | Description |
|---|---|---|---|
| [Example-A1.txt](./Example-A1.txt) | Scope Delta | `Δ` | Add/remove/modify entity ids |
| [Example-A2.txt](./Example-A2.txt) | Decision Record | `D` | Approval, priority, scope, owner |
| [Example-A3.txt](./Example-A3.txt) | Execution Status | `S` | Sprint metrics |
| [Example-A4.txt](./Example-A4.txt) | Risk / Threat | `R` | Severity-ranked threats with action |
| [Example-A5.txt](./Example-A5.txt) | Signals & Gates | `G` | Per-scope invariants |
| [Example-A6.txt](./Example-A6.txt) | Inventory / Topology | `I` | DBs, APIs, integrations |
| [Example-A7.txt](./Example-A7.txt) | Next Actions | `O` | Actor → verb → target |
| [Example-Scenario-Conversation.txt](./Example-Scenario-Conversation.txt) | (multi) | — | Sequence of messages forming an end-to-end flow |

## Other Examples

- [Markdown-to-A2AL.md](./Markdown-to-A2AL.md) — concrete Markdown → A2AL transpilation showing token reduction

## Planned

- `archetypes/` — minimal canonical (one-liner) variants alongside the realistic ones
- `roundtrip/` — writer → relay → reader chain demonstrating §8 forward-compat preservation

## Known Issues (to be fixed by validator pass)

Some current draft examples may violate canonical ordering or use forbidden types (e.g., `null`). They will be normalized once `validator/python/validate.py` is wired into a pre-commit check. Until then, treat the contents as illustrative rather than canonical.
