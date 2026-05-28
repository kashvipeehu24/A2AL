# 0.4.2 Install Prompt — Scenario Walkthroughs

Field-test scenarios for `examples/ClaudeCode/INSTALL-PROMPT.md`. Each file describes:

- **Pre-state** — what files exist before the operator pastes anything
- **Operator messages** — verbatim chat input the human sends
- **Expected agent behavior** — numbered steps the installing agent should take
- **Expected post-state** — what files should exist (and at what version) after the install completes

These are not automated. Mike (or another human) runs them as walkthroughs by carrying them out in a fresh Claude Code session against an empty directory.

| Scenario | Covers |
|---|---|
| 1. Fresh bare | Nothing on disk; full happy-path install |
| 2. Fresh, existing CLAUDE.md | CLAUDE.md exists but has no A2AL block — block is inserted after the first H2 |
| 3. Re-sync, no drift | Already installed at current version; sample unchanged — no-op summary |
| 4. Re-sync, spec drift | Sample has changed since install; diff loop fires for the changed subsection |
| 5. Re-sync, operator edits | Operator hand-edited a subsection; placeholder normalization isolates real drift |
| 6. Clone collision | `~/A2AL` exists but is not the A2AL repo; prompt asks for an alternate clone path |

Reference design: [`../../docs/superpowers/specs/2026-05-21-a2al-0.4.2-install-prompt-design.md`](../../docs/superpowers/specs/2026-05-21-a2al-0.4.2-install-prompt-design.md).
