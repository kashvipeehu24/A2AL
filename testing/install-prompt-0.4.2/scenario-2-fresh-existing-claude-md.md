# Scenario 2 — Fresh install, existing CLAUDE.md with no A2AL block

The target project already has a CLAUDE.md with project-identity content, but no A2AL block. The prompt should detect "no A2AL block" via q1, run a fresh install, and insert the A2AL block immediately after the project's first H2.

## Pre-state

```
~/code/myproj/CLAUDE.md                        exists, contents:

  # MyProj
  
  Project description paragraph.
  
  ## Project Identity
  
  You are MyAgent, doing useful work.
  
  ## Workflow
  
  Commits go to main directly.

~/A2AL/                                        does NOT exist
~/.claude/skills/a2al/                         does NOT exist
```

## Operator message 1

```
Fetch and follow this install prompt:
https://raw.githubusercontent.com/mcornelison/A2AL/main/examples/ClaudeCode/INSTALL-PROMPT.md
```

## Expected agent behavior

1. WebFetch + read prompt.
2. q1 detection:
   - `.claude/skills/a2al/SKILL.md` not found
   - `~/.claude/skills/a2al/SKILL.md` not found
   - `CLAUDE.md` exists but no `## A2AL/0.4` match → `claude_md_has_block = false`
3. Decision: **fresh mode** (no skill anywhere; no A2AL block).
4. Announce: "No existing A2AL install detected — running fresh install."
5. Ask q2–q5; operator answers `Byte/DEV`, no peers, project scope, clone-and-point.
6. e1: clone `~/A2AL`.
7. e2: copy skill + command into `.claude/`.
8. e3: no library copy.
9. e4 (Case B — CLAUDE.md exists, no A2AL block):
   - Extract A2AL block from `~/A2AL/examples/ClaudeCode/CLAUDE-sample.md`.
   - Find the first H2 in target CLAUDE.md: `## Project Identity`.
   - Insert the extracted A2AL block immediately after the `## Project Identity` body and before `## Workflow`.
   - Substitute placeholders: `Byte`, `DEV`, `~/A2AL`, omit Inbox/outbox subsection.
10. e5: smoke test passes.
11. Summary printed.

## Expected post-state

```
~/code/myproj/CLAUDE.md contents (new):

  # MyProj
  
  Project description paragraph.
  
  ## Project Identity
  
  You are MyAgent, doing useful work.
  
  ## A2AL/0.4.1 — Agent-to-Agent Communication
  
  ... (the A2AL block, placeholders filled) ...
  
  ## Workflow
  
  Commits go to main directly.

~/code/myproj/.claude/skills/a2al/SKILL.md     exists
~/code/myproj/.claude/commands/a2al.md         exists
~/A2AL/                                        cloned
```

## Pass criteria

- A2AL block placed after `## Project Identity`, before `## Workflow`
- Existing CLAUDE.md content (Project Identity, Workflow) unchanged
- Placeholders filled correctly
- Inbox/outbox subsection absent (operator answered no peers)
