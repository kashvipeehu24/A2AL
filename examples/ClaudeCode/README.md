# A2AL — Claude Code Integration

Reference skill and slash command for Claude Code that let an agent read, write, and validate A2AL/0.3.0 messages.

## Files

| Path | Purpose |
|---|---|
| [`skills/a2al/SKILL.md`](./skills/a2al/SKILL.md) | A2AL/0.3.0 skill — invoke for **structured payloads** (sprint closeouts, decision logs, risk briefs, ≥5 structured items) |
| [`skills/a2a-shorthand/SKILL.md`](./skills/a2a-shorthand/SKILL.md) | A2A Shorthand skill — invoke for **short conversational messages** (handshakes, acks, ≤3-item updates) |
| [`commands/a2al.md`](./commands/a2al.md) | Slash command `/a2al` — explicit user invocation of the A2AL skill |
| [`commands/a2a-shorthand.md`](./commands/a2a-shorthand.md) | Slash command `/a2a-shorthand` — explicit user invocation of the A2A Shorthand skill |

## Choosing between the two skills

The two skills are complementary, not competing:

| Message shape | Skill |
|---|---|
| Handshake / ack / single-fact update | `a2a-shorthand` |
| Status update with ≤3 metrics | `a2a-shorthand` |
| Sprint closeout / decision log / risk brief | `a2al` |
| Multi-section structured payload (≥5 deltas) | `a2al` |
| Anything with structured citations (refs) | `a2al` |

The `a2a-shorthand` skill self-routes back to `a2al` when its threshold is exceeded; `a2al` self-routes to `a2a-shorthand` when the message is conversational. Either skill is a valid entry point.

## Installing

**Per-project (recommended for adoption tests):**

```bash
mkdir -p .claude/skills .claude/commands
cp -r examples/ClaudeCode/skills/a2al .claude/skills/
cp -r examples/ClaudeCode/skills/a2a-shorthand .claude/skills/
cp examples/ClaudeCode/commands/a2al.md .claude/commands/
cp examples/ClaudeCode/commands/a2a-shorthand.md .claude/commands/
```

**User-global (any project):**

```bash
mkdir -p ~/.claude/skills ~/.claude/commands
cp -r examples/ClaudeCode/skills/a2al ~/.claude/skills/
cp -r examples/ClaudeCode/skills/a2a-shorthand ~/.claude/skills/
cp examples/ClaudeCode/commands/a2al.md ~/.claude/commands/
cp examples/ClaudeCode/commands/a2a-shorthand.md ~/.claude/commands/
```

After installing, restart Claude Code. The agent will surface both skills when relevant; you can also explicitly invoke them via `/a2al` or `/a2a-shorthand`.

## What it does

- **Read:** parse a JSON file, validate the envelope against `specs/A2A-Core.md`, and summarize the profile, intent, and sections in plain English
- **Write:** produce a canonical A2AL message given a recipient, intent, and content; apply profile-specific canonical ordering
- **Validate:** check a message against the core spec and (when known) the profile rules

The skill references the public spec at https://github.com/mcornelison/A2AL.
