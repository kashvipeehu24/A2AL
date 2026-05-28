# A2AL Install Prompt (v0.4.2)

You are an AI agent that has been asked to install or re-sync A2AL on a host project. Follow this prompt end-to-end. It works for both fresh installs and re-syncs — re-running it is safe and is the supported upgrade path inside 0.x.x.

Reference design (read if confused): https://github.com/mcornelison/A2AL/blob/main/docs/superpowers/specs/2026-05-21-a2al-0.4.2-install-prompt-design.md

## How this prompt is structured

Two phases. Run them in order:

1. **Phase 1 — Decisions.** Detect existing-install state, then (if fresh) ask the operator five questions one at a time. Conversational.
2. **Phase 2 — Execution.** Clone the A2AL repo, copy files, write or diff the CLAUDE.md A2AL block, run a 3-prompt verification smoke test. Deterministic.

On re-sync, Phase 1 collapses to a single confirmation question, and Phase 2 step e4 becomes a section-by-section diff loop instead of a fresh write.

## Phase 1 — Decisions

Run q1 first (detection). It determines whether you ask q2–q5 (fresh) or skip them (re-sync).

### q1 — Detect existing install state (computed, not asked)

Run these probes in order:

1. Read `.claude/skills/a2al/SKILL.md` — if it exists, set `scope = project`.
2. Otherwise read `~/.claude/skills/a2al/SKILL.md` — if it exists, set `scope = user-global`.
3. Grep for `^## A2AL/0\.4` in the target CLAUDE.md — if it matches, set `claude_md_has_block = true`. (Target CLAUDE.md is `<project-root>/CLAUDE.md` for project scope, `~/.claude/CLAUDE.md` for user-global scope. If scope is unknown at this point, check the project location first.)

**Decision:**
- If `scope != none` OR `claude_md_has_block = true` → **re-sync mode**. Skip to "Re-sync condensation" below.
- Otherwise → **fresh mode**. Continue with q2.

Announce your decision in one line before continuing, e.g.:
> Detected `.claude/skills/a2al/` — running re-sync.

or

> No existing A2AL install detected — running fresh install.

## Phase 2 — Execution

_(filled in by Tasks 6–9)_

## Re-sync diff loop (Phase 2 step e4 alternate)

_(filled in by Task 11)_

## Verification

_(filled in by Task 9)_

## Error handling

_(filled in by Task 14)_
