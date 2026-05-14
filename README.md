# A2AL — Open Vocabulary for Agent Communication

A2AL is an open, contributable vocabulary library that lets AI agents communicate in token-efficient shorthand. It is plain text, English-derived, designed to tokenize as 1 token per concept on modern LLM tokenizers. Agents share a common dictionary and extend it for their domain.

**Status:** A2AL/0.4.1. Pre-1.0; subject to refinement before /1.0.

**License:** Apache-2.0 — see [LICENSE](./LICENSE).

## Why

In real multi-agent execution, 60–90% of inter-agent tokens are mechanical waste — narrative prose, framing, justification, JSON envelope overhead. A2AL strips that out and exchanges only state and intent in tight shorthand the LLM already speaks. Empirically, A2AL is **~0.26× the token cost** of plain Markdown on a typical handshake — and far less than the JSON-envelope approach we tried in /0.3.0 (now archived).

## How A2AL looks

A complete agent-to-agent message — one routing header line, then the body:

```text
from=Byte(DEV); to=Ledger(PM); date=2026-05-13; topic=US-713 closeout; audience=agent
US-713 done; AC met; CI green; PR ready -- merge?
```

That's the whole format. No envelope. No JSON. Plain text. The receiving agent has the vocabulary library loaded into its context, expands the shorthand internally, and acts. The header is mandatory (see `specs/A2A-Core.md` §3); the body uses the style guide and library.

For a domain example (security):

```text
from=Audrey(SEC); to=Byte(DEV); date=2026-05-13; topic=CVE-2026-30856; audience=agent; urgency=urgent
crit: RCE in MCP stdio config -- patch ASAP. CVE-2026-30856.
```

For a status report:

```text
from=Byte(DEV); to=Ledger(PM); date=2026-05-13; topic=preflight status; audience=agent
tests 21/21; preflight 878/878; ruff pass; build green.
```

See [`examples/`](./examples) for full worked examples.

## When to write A2AL vs Markdown

A2AL is **mandatory** when the audience is agent-only and **wrong** when a human is in the audience. No hybrid mode; no duplication.

| Situation | Format |
|---|---|
| Agent → agent, no human review expected | A2AL MUST |
| Sender identified itself as an AI agent in an inbound message | A2AL MUST (reactive rule) |
| Human will read or review the message at any point | Markdown |
| Audience ambiguous or mixed | Markdown (default) |
| RCAs, ADRs, design specs, long-form deliberation | Markdown (humans return to these) |

Channels can also be declared agent-only by convention (e.g., paths under `agent-channel/`, `.a2a/`, `*/inbox-internal/`).

## How to install

A2AL/0.4.1 is plain text — no runtime, no compiler. Install means making the vocabulary library and the agent helper skill available to your AI agent.

### For Claude Code agents (per-project)

```bash
git clone https://github.com/mcornelison/A2AL.git /path/to/a2al
mkdir -p .claude/skills .claude/commands
cp -r /path/to/a2al/examples/ClaudeCode/skills/a2al .claude/skills/
cp /path/to/a2al/examples/ClaudeCode/commands/a2al.md .claude/commands/
```

For user-global install (any Claude Code project), substitute `~/.claude/` for `.claude/`. Restart Claude Code.

### For other LLM platforms

The vocabulary library at `library/*.yaml` is plain YAML — load any subset into your agent's system prompt. The `specs/A2A-Core.md` style guide is normative and platform-agnostic.

### For library contributors

```bash
git clone https://github.com/mcornelison/A2AL.git
cd A2AL
pip install pyyaml
python tools/validate_library.py
```

## Configuring your agent

Once the skill files are in `.claude/skills/` and `.claude/commands/`, the skill is **auto-discovered** by Claude Code on next restart — no manual "enable" step. What you do need is a CLAUDE.md block telling the agent its identity, where to find the library, and (if peers exist) the inbox conventions. Same recipe for new and existing agents — only difference is whether you create CLAUDE.md from scratch or append to an existing one.

### CLAUDE.md block (copy / paste)

For an **existing CLAUDE.md**: append this section. For a **new project**: this can be the whole file, or supplement with project-specific guidance.

````markdown
## A2AL/0.4.1 — Agent-to-Agent Communication

This project uses [A2AL/0.4.1](https://github.com/mcornelison/A2AL) for peer-to-peer agent messages.

### Identity
You are **[AgentName]**, a [role] agent. When sending A2AL messages, sign as `[AgentName]/[role]` or `[AgentName]([role])` in the routing header (e.g., `Hawkeye/QA`, `Byte(DEV)`). Roles are free-form.

### Repo location
The A2AL repo is cloned at `[/absolute/path/to/A2AL]`. The vocabulary library is at `[/absolute/path/to/A2AL]/library/`.

### When to use A2AL (audience rule)
- **Agent-only audience → A2AL MUST.** Both sender and recipient are agents; no human will read or review.
- **Human in the audience → Markdown.** A human will triage, archive, or review at any point.
- **Inbound says `audience=agent` or sender is identified as an AI agent → reply MUST be A2AL** (reactive rule).
- **Default → Markdown** when audience is ambiguous or mixed.

### Routing header
Every A2AL message begins with one line:
```text
from=<Name>(<Role>); to=<Name>(<Role>); date=<ISO>; topic=<short label>
```
Optional fields: `audience=agent|mixed`, `urgency=low|medium|high|urgent`, `refs=<id>,<id>`, `in-reply-to=<id>`.

### Loading the library
Always have `[/absolute/path/to/A2AL]/library/core.yaml` available (~77 universal terms). Add domain extensions per the conversation:

| Topic | Load |
|---|---|
| Code review / dev process | + `programming.yaml` |
| Cloud / orchestration / data | + `infrastructure.yaml` |
| Sprint, project, program management | + `project-mgmt.yaml` |
| Security review / threat modeling | + `security.yaml` |
| LLM / agent / RAG topics | + `ai-agents.yaml` |

The `a2al` skill and `/a2al` command both use these.

### Inbox / outbox (only if you have peer agents)
- **Your inbox:** `[/absolute/path/to/your-inbox/]` (`.txt` files, one A2AL message per file)
- **Filename:** `<sender>-<intent>-<unix-ts>.txt`
- **Threading:** reference prior message id in the body — `re: <id>` or `in-reply-to: <id>`

### Reference
- Spec: `[/absolute/path/to/A2AL]/specs/A2A-Core.md`
- Library schema: `[/absolute/path/to/A2AL]/library/README.md`
- Validator (validates library YAML, not messages): `python [/absolute/path/to/A2AL]/tools/validate_library.py`
````

The bracketed `[...]` placeholders are what you fill in:

- `[AgentName]` and `[role]` — your agent's name and what it does
- `[/absolute/path/to/A2AL]` — wherever you cloned this repo
- `[/absolute/path/to/your-inbox/]` — only if peers can send you messages

If the agent is solo (no peers), the inbox section is optional. The skill is still useful for "compress this report" or "send this to <other agent>" prompts.

### Verifying the install

After restarting Claude Code, prompt the agent:

```
Verify A2AL is wired up:
1. Read [/absolute/path/to/A2AL]/library/core.yaml and report how many entries it has plus 3 sample terms.
2. Compose this as an A2AL message to peer "Agent2": "all tests pass, build is green, PR ready to merge". Include the routing header.
3. Confirm /a2al is registered as a slash command.
```

Expected: ~77 entries reported (sample terms like `done`, `merge`, `PR`); a two-line output with a `from=...; to=Agent2; date=...; topic=...; audience=agent` header followed by a body like `tests pass; build green; PR ready -- merge?`; `/a2al` recognized. If any step fails, check that the skill files actually copied into `.claude/skills/a2al/` and `.claude/commands/a2al.md`, and that you restarted Claude Code.

### Multi-agent setup

If you have multiple agents talking to each other peer-to-peer, each agent gets its own `.claude/skills/a2al/`, its own `.claude/commands/a2al.md`, and its own CLAUDE.md with its own `[AgentName]/[role]` identity. The path to the A2AL repo and the library is the same for all of them; only identity and inbox path differ.

### What you don't need to do

- ❌ No "enable skill" command — Claude Code auto-discovers skills on startup
- ❌ No daemon, server, or service
- ❌ No registration step in any external system
- ❌ No special launch flag — just restart Claude Code after copying the files

## How to use

### Sending a message to a peer agent

In Claude Code, just describe the message:

> "Send Agent2 a quick update — US-713 is done, all tests pass, PR ready to merge."

The `a2al` skill kicks in and produces a header + body:

```text
from=Byte(DEV); to=Agent2; date=2026-05-13; topic=US-713 closeout; audience=agent
US-713 done; AC met; CI green; PR ready -- merge?
```

Drop that text into the peer's inbox (or send via whatever transport the agents share).

### Reading a peer agent message

Hand the `.txt` file to the skill (or paste the content). The agent expands shorthand to plain English internally and acts on the meaning.

### Slash command

Explicit invocation: `/a2al` — useful when you want to specifically request shorthand output, or to read a file by path.

### Loading domain extensions

The skill loads `library/core.yaml` automatically. To add domain vocabulary (e.g., when working on infrastructure or security), instruct the agent: "Load `library/security.yaml` for this thread." The agent merges that vocabulary into its dictionary for the session.

## Repository Layout

| Path | Purpose |
|---|---|
| [`specs/A2A-Core.md`](./specs/A2A-Core.md) | Normative A2AL/0.4.1 spec (audience rule, routing header, style guide) |
| [`library/`](./library) | Vocabulary library — `core.yaml` + 5 domain extensions |
| [`examples/`](./examples) | Worked shorthand examples |
| [`examples/ClaudeCode/`](./examples/ClaudeCode) | Reference Claude Code skill + slash command |
| [`tools/`](./tools) | Validator (`validate_library.py`) + tests |
| [`.github/`](./.github) | PR template, CI workflow, issue templates |
| [`testing/`](./testing) | Local agent test harness (gitignored .claude/, tracked test inputs) |
| [`archive/0.3.0/`](./archive/0.3.0) | Deprecated /0.3.0 JSON envelope spec — historical reference |

Start with [`specs/A2A-Core.md`](./specs/A2A-Core.md) for the style guide and [`library/README.md`](./library/README.md) for the vocabulary structure.

## Contributing to the Library

The library grows through community contributions:

1. Pick the right file (universal terms → `core.yaml`, domain-specific → matching extension)
2. Add an entry with `term`, `expansion`, and `example` (see [`library/README.md`](./library/README.md) for schema)
3. **Run `python tools/validate_library.py` before opening a PR.** Submissions that fail validation will be blocked by CI; running locally first saves the round trip.
4. Open a PR using the [PR template](./.github/PULL_REQUEST_TEMPLATE.md)
5. CI runs the validator on every PR; merges are blocked on validation failure

See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for the full workflow including non-library contributions (spec edits, validator improvements, new domains).

## Versioning

A2AL follows semantic versioning. Adding library entries is a minor bump. Renaming or removing a term, or changing the spec's style rules, is a major bump. Pre-1.0 means breaking changes are expected; /1.0 is reached when at least one production agent emits and consumes A2AL successfully and the cross-LLM compatibility (Moltbook beta) has been demonstrated.

## Status & Roadmap

| Version | Theme | Status |
|---|---|---|
| 0.3.0 | JSON envelope (deprecated) | archived in [`archive/0.3.0/`](./archive/0.3.0) |
| 0.4.0 | Hard pivot — shorthand library is A2AL | superseded by 0.4.1 |
| **0.4.1** | **Audience rule + routing header (normative)** | **current** |
| 0.4.2 | Tokenization validator tooling (Claude, GPT, Llama) | future |
| 0.4.3 | Auto-harvested PR candidates from agent traffic | future |
| 0.5.0 | Moltbook beta — cross-LLM validation | future |
| 1.0.0 | Production agents using A2AL successfully + Moltbook beta proven | gated on real-world adoption |
