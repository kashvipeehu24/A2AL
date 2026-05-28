# A2AL Install Prompt (v0.4.2)

You are an AI agent that has been asked to install or re-sync A2AL on a host project. Follow this prompt end-to-end. It works for both fresh installs and re-syncs — re-running it is safe and is the supported upgrade path inside 0.x.x.

Reference design (read if confused): https://github.com/mcornelison/A2AL/blob/main/docs/superpowers/specs/2026-05-21-a2al-0.4.2-install-prompt-design.md

## How this prompt is structured

Two phases. Run them in order:

1. **Phase 1 — Decisions.** Detect existing-install state, then (if fresh) ask the operator five questions one at a time. Conversational.
2. **Phase 2 — Execution.** Clone the A2AL repo, copy files, write or diff the CLAUDE.md A2AL block, run a 3-prompt verification smoke test. Deterministic.

On re-sync, Phase 1 collapses to a single confirmation question, and Phase 2 step e4 becomes a section-by-section diff loop instead of a fresh write.

## Phase 1 — Decisions

_(filled in by Tasks 4–5)_

## Phase 2 — Execution

_(filled in by Tasks 6–9)_

## Re-sync diff loop (Phase 2 step e4 alternate)

_(filled in by Task 11)_

## Verification

_(filled in by Task 9)_

## Error handling

_(filled in by Task 14)_
