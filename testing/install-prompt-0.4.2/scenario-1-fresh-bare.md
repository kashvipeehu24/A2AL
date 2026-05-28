# Scenario 1 — Fresh install, bare disk

Happy path. Nothing on disk except a target project directory with a CLAUDE.md that has no A2AL content (or no CLAUDE.md at all). Operator pastes the WebFetch one-liner; agent drives the full install.

## Pre-state

```
~/code/myproj/                   # target project, Claude session running here
~/code/myproj/CLAUDE.md          # may or may not exist; in this scenario, does not exist
~/A2AL/                          # does NOT exist
~/.claude/skills/a2al/           # does NOT exist
~/.claude/commands/a2al.md       # does NOT exist
```

## Operator message 1 (entry point)

```
Fetch and follow this install prompt:
https://raw.githubusercontent.com/mcornelison/A2AL/main/examples/ClaudeCode/INSTALL-PROMPT.md
```

## Expected agent behavior

1. WebFetch the URL; read the prompt.
2. Run q1 detection probes:
   - `.claude/skills/a2al/SKILL.md` not found
   - `~/.claude/skills/a2al/SKILL.md` not found
   - `CLAUDE.md` does not exist (or has no `## A2AL/0.4` heading)
3. Announce: "No existing A2AL install detected — running fresh install."
4. Ask q2 (identity): "What's this agent's name and role? Examples: `Hawkeye/QA`, `Byte/DEV`."
   - **Operator answers:** `Byte/DEV`
5. Ask q3 (peers): "Will this agent receive A2AL messages from peer agents? If yes, give me the absolute path to its inbox."
   - **Operator answers:** `no`
6. Ask q4 (scope): "Project-scoped (`.claude/` in this project) or user-global (`~/.claude/`)?"
   - **Operator answers:** `project`
7. Ask q5 (library): "Should the library live (A) inside a cloned A2AL repo, or (B) copied into `.claude/a2al-library/`?"
   - **Operator answers:** `A` (clone-and-point)
8. e1 — clone: `git clone https://github.com/mcornelison/A2AL.git ~/A2AL` (succeeds).
9. e2 — copy skill + command:
   ```
   ~/A2AL/examples/ClaudeCode/skills/a2al/SKILL.md  ->  ./.claude/skills/a2al/SKILL.md
   ~/A2AL/examples/ClaudeCode/commands/a2al.md      ->  ./.claude/commands/a2al.md
   ```
10. e3 — library: no copy needed (clone-and-point); the library lives at `~/A2AL/library/`.
11. e4 — write CLAUDE.md: copy `~/A2AL/examples/ClaudeCode/CLAUDE-sample.md` to `./CLAUDE.md`. Fill placeholders:
    - `[AgentName]` → `Byte`
    - `[role]` → `DEV`
    - `[/absolute/path/to/A2AL]` → `~/A2AL`
    - Inbox/outbox subsection: omitted (operator said no peers)
12. e5 — verify (in the same chat session):
    - Read `~/A2AL/library/core.yaml`, report entry count + 3 sample terms (expect ~77 entries).
    - Compose a test A2AL message from `Byte(DEV)` to `Agent2`.
    - Confirm `/a2al` is registered.

## Expected post-state

```
~/code/myproj/.claude/skills/a2al/SKILL.md       exists (matches upstream)
~/code/myproj/.claude/commands/a2al.md           exists (matches upstream)
~/code/myproj/CLAUDE.md                          exists, A2AL block at top, placeholders filled
~/A2AL/                                          exists, freshly cloned
```

The CLAUDE.md A2AL block:
- Heading: `## A2AL/0.4.1 — Agent-to-Agent Communication` (sample's current version)
- Identity subsection: `Byte/DEV`
- Library location subsection: points at `~/A2AL/library/`
- Inbox/outbox subsection: absent
- Reference subsection: paths point at `~/A2AL/`

## Pass criteria

- All 12 expected steps occurred in order
- No errors during git clone or file copies
- e5 smoke test passed all three probes
- Post-state matches exactly
