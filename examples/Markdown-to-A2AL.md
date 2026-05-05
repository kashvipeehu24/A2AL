# Markdown → A2AL Transpilation Example

A worked example showing how a verbose Markdown status report compresses into a single A2AL/2.0 A3 (Execution Status) message. The point is not pretty output — it's that **the receiving agent's behavior is identical**, with 80–90% fewer tokens and zero ambiguity.

> **Status:** Illustrative draft. Token counts are approximate.

---

## Source: Markdown Sprint Report (~ 90 tokens)

```markdown
# Sprint 2 Status Report

We're tracking well overall this sprint. The team has been heads-down
on the bronze-data-integrity epic and made significant progress.

## Summary
- 12 of 12 user stories passed QA
- All 172 unit tests pass
- Build is green
- Branch ralph/sprint-2-tech-debt-and-auth merged to main yesterday

## Confidence
We're confident this is ready to ship. No defects open.
```

## Target: A2AL/2.0 A3 Execution Status (~ 30 tokens, canonical)

```text
[[2,"mcp-server",0,7,3,"sprint-2-status"],["S",[1,100],[2,0],[3,[12,12]],[4,[172,172]],[5,0],[7,1],[8,"sprint-2"],[9,"ralph/sprint-2-tech-debt-and-auth"],[10,"main"]]]
```

## What Was Stripped, What Was Kept

| Markdown content | A2AL? | Why |
|---|---|---|
| "We're tracking well overall this sprint" | ✗ | Narrative — does not change behavior |
| "The team has been heads-down…" | ✗ | Framing |
| "12 of 12 user stories passed QA" | ✓ | `[3, [12, 12]]` (mkey=stories_passed) |
| "All 172 unit tests pass" | ✓ | `[4, [172, 172]]` (mkey=tests_passed) |
| "Build is green" | ✓ | `[7, 1]` (mkey=build_quality) |
| "Branch … merged to main" | ✓ | `[9, ...]`, `[10, "main"]` |
| "We're confident this is ready to ship" | ✗ | Subjective framing |
| "No defects open" | ✓ | `[5, 0]` (mkey=defects_open) |
| Implicit: percent_complete = 100 | ✓ | `[1, 100]` |
| Implicit: stoplight = green (0) | ✓ | `[2, 0]` |

## Why This Matters

A2AL is not "Markdown without formatting." It is a **closed semantic lane** — every kept item maps to a registered metric key with deterministic meaning. A receiver does not need to parse English to act on the message; it dispatches on integer keys.

For 100 status reports per day across 10 agents, the token savings compound, and so does the elimination of inference errors from prose.
