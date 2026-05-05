# A2AL — Claude Code Integration

Reference skill and slash command for Claude Code that let an agent read, write, and validate A2AL/0.3.0 messages.

## Files

| Path | Purpose |
|---|---|
| [`skills/a2al/SKILL.md`](./skills/a2al/SKILL.md) | Skill definition — invoke when reading or writing A2AL messages |
| [`commands/a2al.md`](./commands/a2al.md) | Slash command `/a2al` — explicit invocation by the user |

## Installing

**Per-project (recommended for adoption tests):**

```bash
mkdir -p .claude/skills .claude/commands
cp -r examples/ClaudeCode/skills/a2al .claude/skills/
cp examples/ClaudeCode/commands/a2al.md .claude/commands/
```

**User-global (any project):**

```bash
mkdir -p ~/.claude/skills ~/.claude/commands
cp -r examples/ClaudeCode/skills/a2al ~/.claude/skills/
cp examples/ClaudeCode/commands/a2al.md ~/.claude/commands/
```

After installing, restart Claude Code. The agent will surface the `a2al` skill when relevant; you can also explicitly invoke it via `/a2al`.

## What it does

- **Read:** parse a JSON file, validate the envelope against `specs/A2A-Core.md`, and summarize the profile, intent, and sections in plain English
- **Write:** produce a canonical A2AL message given a recipient, intent, and content; apply profile-specific canonical ordering
- **Validate:** check a message against the core spec and (when known) the profile rules

The skill references the public spec at https://github.com/mcornelison/A2AL.
