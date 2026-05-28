# Scenario 6 — Clone collision

`~/A2AL` exists but is some other directory (or a clone of a different repo). The prompt must stop, ask the operator for an alternate clone path, and proceed without overwriting `~/A2AL`.

## Pre-state

```
~/code/myproj/                                 target project, Claude session here
~/A2AL/                                        exists, contents unrelated to A2AL
                                               (e.g., a personal notes folder, or a
                                                clone of a different "A2AL" repo)
~/.claude/skills/a2al/                         does NOT exist
```

## Operator message 1

```
Fetch and follow this install prompt:
https://raw.githubusercontent.com/mcornelison/A2AL/main/examples/ClaudeCode/INSTALL-PROMPT.md
```

## Expected agent behavior

1. WebFetch + read prompt.
2. q1: fresh mode (no skills found, no A2AL block in CLAUDE.md).
3. q2–q5: operator answers identity, no peers, project scope, clone-and-point.
4. e1:
   - `~/A2AL` exists.
   - Run `git -C ~/A2AL remote get-url origin`. Either fails (not a git repo) or returns a URL that does not end in `mcornelison/A2AL`.
   - **Stop.** Print:
     > `~/A2AL` exists but is not the A2AL clone (`git remote get-url origin` returned `<actual-url-or-error>`). I don't want to overwrite an unknown directory. Where should I clone A2AL instead? (e.g., `~/code/A2AL`)
   - **Operator answers:** `~/code/A2AL`
5. Retry e1 with the new path: `git clone https://github.com/mcornelison/A2AL.git ~/code/A2AL`. Succeeds.
6. e2: copy skill + command from `~/code/A2AL/examples/ClaudeCode/` into `.claude/`.
7. e3: no library copy (clone-and-point; library path is `~/code/A2AL/library/`).
8. e4: write CLAUDE.md, library path filled as `~/code/A2AL/library/`.
9. e5: smoke test passes.
10. Summary printed.

## Expected post-state

```
~/A2AL/                                        UNCHANGED — operator's original dir intact
~/code/A2AL/                                   freshly cloned A2AL
~/code/myproj/.claude/skills/a2al/SKILL.md     exists
~/code/myproj/.claude/commands/a2al.md         exists
~/code/myproj/CLAUDE.md                        exists, A2AL block; library at ~/code/A2AL/library/
```

## Pass criteria

- `~/A2AL` byte-identical before and after the install
- CLAUDE.md library path points at `~/code/A2AL/library/`, not `~/A2AL/library/`
- No git error proceeds to Phase 2 without operator answering the alternate-path question
