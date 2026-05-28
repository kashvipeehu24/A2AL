# Scenario 3 — Re-sync, no drift

A2AL is already installed at the current version. Sample on `main` has not changed since install. The prompt should refresh files deterministically, confirm CLAUDE.md is in sync, and exit with a "no changes" summary.

## Pre-state

```
~/code/myproj/.claude/skills/a2al/SKILL.md     exists (matches upstream)
~/code/myproj/.claude/commands/a2al.md         exists (matches upstream)
~/code/myproj/CLAUDE.md                        exists, A2AL block at top, placeholders filled
  - Identity:   Byte/DEV
  - Library:    ~/A2AL/library/
  - Inbox:      (absent)
~/A2AL/                                        exists, clean, on main, up to date
```

## Operator message 1

```
Fetch and follow this install prompt:
https://raw.githubusercontent.com/mcornelison/A2AL/main/examples/ClaudeCode/INSTALL-PROMPT.md
```

## Expected agent behavior

1. WebFetch the URL; read the prompt.
2. Run q1 detection: `.claude/skills/a2al/SKILL.md` exists → `scope = project`. CLAUDE.md has `## A2AL/0.4.1`.
3. Announce: "Detected `.claude/skills/a2al/` — running re-sync."
4. Read CLAUDE.md, extract: identity `Byte/DEV`, library path `~/A2AL/library/`, no inbox, library mode `clone-and-point` (path is inside an A2AL clone).
5. Confirmation question: "Detected A2AL installed at project scope, identity `Byte/DEV` from CLAUDE.md, library at `~/A2AL/library/` (clone-and-point). Proceed with re-sync? (yes / change something)"
   - **Operator answers:** `yes`
6. e1: `git -C ~/A2AL pull --ff-only` — succeeds, no new commits.
7. e2: overwrite `.claude/skills/a2al/SKILL.md` and `.claude/commands/a2al.md` from clone. Files are byte-identical to what was already there.
8. e3: no copy needed (clone-and-point).
9. e4 (diff loop): for each of the six H3 subsections in CLAUDE.md's A2AL block, extract operator's normalized version and the sample's. Compare:
   - Identity: equal → silent
   - Library location: equal → silent
   - Audience rule: equal → silent
   - Routing header: equal → silent
   - Inbox/outbox: equal (both absent) → silent
   - Reference: equal → silent
10. No subsection prompted; CLAUDE.md is unmodified.
11. e5: smoke test passes.
12. Summary:
    ```
    A2AL re-sync complete.
      Skill, command, library: refreshed (no actual changes).
      CLAUDE.md A2AL block: 0.4.1 -> 0.4.1 (no changes).
        Identity: unchanged
        Library location: unchanged
        Audience rule: unchanged
        Routing header: unchanged
        Inbox/outbox: unchanged
        Reference: unchanged
    ```

## Expected post-state

Identical to pre-state. No files changed (modified timestamps may change on copy targets — that's fine).

## Pass criteria

- The single confirmation question is the only one asked
- No subsection-level prompts fire
- Summary explicitly reports all subsections as "unchanged"
- CLAUDE.md content byte-identical to pre-state
