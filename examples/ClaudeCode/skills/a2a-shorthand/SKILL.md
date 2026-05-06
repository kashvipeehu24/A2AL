---
name: a2a-shorthand
description: Use when the user asks to send a short conversational agent-to-agent message, write a quick status update, ack a peer, or compress a verbose MD report into a tight English shorthand. Plain-text format, no envelope. Triggers on phrases like "send a quick update", "ack that", "shorthand this", "tell agent2 X", short conversational asks. NOT for sprint closeouts, decision logs, risk briefs, or messages with 5+ structured items — those use the a2al skill.
---

# A2A Shorthand Skill

A2A Shorthand is a plain-text style for short agent-to-agent messages. It is sibling to A2AL/0.3.0; the two are complementary.

Reference: https://github.com/mcornelison/A2AL — `specs/A2A-Shorthand.md` and `examples/shorthand/`.

## When to use

- Handshakes, acks, single-fact updates
- Conversational coordination ("merge?", "blocked on X")
- Status updates with ≤3 metrics or ≤3 deltas
- Quick action requests

## When NOT to use (route to a2al instead)

If the message has 5+ structured items, spans 3+ section types, needs structured citations (refs), or is a formal record (sprint closeout, decision log, risk brief), use the `a2al` skill — A2A Shorthand is net-negative on tokens for those shapes.

## Style rules

### Drop
- Articles (`the`, `a`, `an`)
- Helping/linking verbs (`is`, `are`, `was`) when state is unambiguous
- Subjective framing (`I think`, `it seems`)
- Politeness (`please`, `could you`)
- Filler (`in order to` → `to`)
- Repeated subjects across fragments — use `;`

### Use
- Sentence fragments
- Imperative mood for actions
- Past tense / status adjectives for state
- Standard tech jargon: `PR`, `AC`, `CI`, `CD`, `DQ`, `RCE`, `CVE`, `CVSS`, etc.
- IDs as bare tokens: `US-713`, `commit-98b483d`

### Punctuation
- `;` between related facts (same topic)
- `.` between unrelated facts
- `:` after subject to expand
- `/` for ratios
- `?` for questions
- `--` for inline rationale

### Avoid
- Creative abbreviations (`cmplt`, `prgm`) — usually tokenize as 2–3 tokens
- Rare Unicode (✓ ⟳ ✗) — usually multi-token in Claude's vocab
- Single-letter codes (`c`, `b`, `r`) — ambiguous

## Patterns

| Pattern | Form | Example |
|---|---|---|
| State change | `<id> <state>` | `US-713 done` |
| Multi-fact state | `<id> <state>; <fact>; <fact>` | `US-713 done; AC met; CI green` |
| Status report | `<metric> <value>; ...` | `tests 21/21; preflight 878/878; build green` |
| Action | `<verb> <target>` or `<actor>: <verb> <target>` | `merge ralph/auth-fix` |
| Blocker | `<id> blocked: <reason>` | `US-718 blocked: no household source in Silver` |
| Question | `<verb>?` or `<id> <verb>?` | `merge?`, `US-713 sign-off?` |
| Decision | `<decision>: <id> -- <rationale>` | `approved: US-713 PRD -- 1 AC added` |
| Ack | `ack <id>` | `ack US-713 closeout` |

## Mode 1 — Read

When given a shorthand message:
1. Parse `term=expansion` definitions on first occurrence; remember within the thread
2. Expand the message in your head (don't echo the expansion to the user unless asked)
3. Summarize key facts in 1–2 plain-English sentences for the user

## Mode 2 — Write

When the user asks to compose a message:
1. Identify the structural shape (state change / status / action / blocker / question / decision / ack)
2. Pick the matching pattern from the table above
3. Use canonical glossary terms where possible; expand to full English for novel concepts
4. Apply style rules — drop fillers, use fragments, semicolons between related facts
5. **Check the routing:** if you're producing 5+ structured items or multiple section types, **stop** and tell the user to use the `a2al` skill instead

## Mode 3 — Vocabulary extension

If the user wants to introduce a new shortening:
1. Verify the term will be used 3+ times in the thread (else just write it out in full)
2. On first use, write `<term>=<expansion>` (no spaces in the expansion)
3. After first use, use the bare term

Example: `DR=design-review. DR sched Tuesday; PR ready post-DR.`

## Worked example — write

User: "Tell Agent1 the sprint hotfix is done — 713 needed no code change, 714 implemented warnOnly DQ flag, all tests pass, ready to merge."

You produce:

```
US-713 done; no code change -- already in main from US-671.
US-714 done; warnOnly DQ flag; 21/21 DQ tests; preflight 878/878.
merge ralph/pipeline-hotfix-2026-04-17?
```

You write that to the file/inbox the user specified, then summarize: "Wrote sprint hotfix update to Agent1. Three lines, ~30 tokens vs ~95 in verbose English. Asks Agent1 to merge."

## Worked example — read

User: "What does this say?" (provides `US-713 done; AC met; CI green; PR ready -- merge?`)

You reply: "US-713 is complete with acceptance criteria met and CI green. Sender's PR is ready and they're asking permission to merge."

## When to stop and route to a2al

If the user's intent compresses better in A2AL — i.e., it has structured fields like multi-item delta, status, actions, refs, decision, risk, gates, inventory — stop and say: "This message has [N] structured items / spans [M] section types. A2AL/0.3.0 will be more token-efficient here. Switch to the `a2al` skill?"

Specifically:
- 5+ deltas → A2AL
- Multiple sections + body rationale → A2AL
- Citations (`refs` of commits/files/CVEs) → A2AL
- Sprint closeout, decision log, risk brief → A2AL

For everything else, A2A Shorthand wins.
