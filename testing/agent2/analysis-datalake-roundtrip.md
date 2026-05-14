# A2AL/0.4.0 vs Markdown — Datalake Round-Trip Analysis

**Date:** 2026-05-07
**Thread:** `agent1-agent2-datalake`
**Exchange:** 6 messages — Agent1 → Agent2 (3 inbound) + Agent2 → Agent1 (3 outbound)
**Content:** Two structured user-story sign-off requests + one sev-2 incident report with mitigation triage. Each message has named fields (sources, targets, SLOs, AC, mitigations, ownership) — the high-structure regime that A2AL is designed for, in contrast with the earlier pure-prose welcome handshake (`analysis.md`).

## What was measured

Each of the 6 logical messages was authored in two formats:

- **shorthand** — A2AL/0.4.0 plain-text shorthand, sourced from `library/*.yaml` vocabulary, as actually exchanged between the agents.
- **md** — a natural-Markdown rewrite of the same logical content, with headings, full-grammar prose, and bullet lists. Not stripped down, not bloated; the way an LLM or a human would normally write a Slack/Confluence post conveying the same facts.

Token counts were produced by `testing/tools/token_analytics.py` using OpenAI's `cl100k_base` encoder (a stable industry benchmark; Anthropic's tokenizer differs in absolute counts but tracks similar ratios on technical English).

Manifest: `testing/tools/manifests/datalake-roundtrip.json`
Per-message records: `testing/agent2/analysis/datalake-roundtrip/`
Markdown rewrites: `testing/agent2/analysis/datalake-md/`

## Per-message token counts

| Direction | Message | Intent | Shorthand | MD | Ratio (sh/md) |
|---|---|---|---:|---:|---:|
| Read | `agent1-us-dl401` | user-story | 198 | 290 | 0.68× |
| Read | `agent1-us-dl407` | user-story | 210 | 292 | 0.72× |
| Read | `agent1-pipeline-error` | incident | 565 | 730 | 0.77× |
| Write | `agent2-us-dl401-signoff` | sign-off | 152 | 221 | 0.69× |
| Write | `agent2-us-dl407-signoff` | sign-off | 163 | 216 | 0.76× |
| Write | `agent2-inc-dl0517-ack` | incident-response | 402 | 533 | 0.75× |
| **Round-trip total** | | | **1,690** | **2,282** | **0.74×** |

## Headline result

**A2AL shorthand used ~26% fewer tokens than equivalent Markdown across this round-trip** (1,690 vs 2,282; ratio 0.741). MD would not have been more efficient — it would have cost ~592 more tokens to convey the same information.

The savings are consistent: every message was lighter in shorthand, with ratios in a tight band (0.68×–0.77×). No single message saw MD beat shorthand.

### Where the savings come from

- **No connecting prose.** MD writes "Could you review the acceptance criteria?" / "I've drafted US-DL-407 to build…" The shorthand drops these entirely; the intent is in the header.
- **Field-as-token form.** `priority: high; sprint 26; owner @Agent1/dev` is 3 facts in ~12 tokens; the MD bullet form ("Priority: high", "Sprint: 26", "Owner: Agent1 (DEV)") costs ~25 tokens for the same content.
- **Pattern-driven structures.** `US-DL-401 approved; AC met; ship` is the canonical decision pattern; the MD form ("US-DL-401 is approved. Acceptance criteria are met — ship it.") roughly doubles it.
- **Standardized abbreviations from the library** (`AC`, `DQ`, `PR`, `CI`, `SCD2`, `MDM`, sev codes) tokenize as 1 token each, vs the multi-token MD spell-outs.

### Where shorthand and MD are at parity

The error stack trace, source paths (`abfss://...`), schema names (`clickstream.v3.user_agent_raw`), and metric values (`9.4g RSS vs 8g req`) carry equally in both formats — they are pre-tokenized technical strings. About 30–40% of the incident message's content is this unavoidable bedrock; below that floor neither format can compress further.

## Comparison with the earlier handshake (analysis.md)

| Exchange | Content type | Shorthand vs MD |
|---|---|---:|
| Welcome handshake (analysis.md) | Pure prose, no structure | **0.26×** (shorthand much leaner) |
| Datalake round-trip (this analysis) | Heavily structured fields + AC + mitigations | **0.74×** (shorthand leaner, less dramatically) |

Two different shapes; same direction. Shorthand wins both, but for different reasons:

- On the pure-prose handshake, the win came from killing the JSON envelope of A2AL/0.3.0. There was almost no structure to compress.
- On the structured datalake exchange, the win comes from compressing real fields: the canonical-pattern shorthand encodes named facts (states, AC, mitigations, owners, sev) in fewer tokens than MD's natural-prose-plus-bullets.

The 0.4.0 pivot bet was that shorthand would hold its lead across both regimes. This round-trip confirms it on the structured end.

## Clarity and ambiguity

The user asked: did the A2AL shorthand introduce ambiguity that traditional MD would not have? Reviewing the exchange:

### Was there real ambiguity in the inbound shorthand?

Pulling apart each inbound message line by line, **no facts were ambiguous to a peer agent that has loaded the library**. Every named field (`src:`, `target:`, `format:`, `SLO:`, `AC:`, `priority:`, `owner`, `deps:`) labels its value. Every status pattern (`drafted`, `blocked`, `FAILED`, `approved`) maps to a library entry. Every ID (`US-DL-401`, `INC-DL-0517`, `SPARK-3033`) is a literal token shared across both formats.

That said, two specific micro-ambiguities exist that an MD rewrite would not have:

1. **Compressed compound facts.** `user_agent col 4.1M unique values vs 380k baseline (10.8x)` requires the reader to bind "(10.8x)" to "ratio to baseline" — adjacent context makes it clear, but MD's "a 10.8× increase from baseline" leaves no inference work. Risk: low.
2. **Implicit subjects after a header.** `ack INC-DL-0517; sev-2 acknowledged; SLA breach noted` carries an implicit "I/Agent2" subject. The header line establishes it, but on a quick mid-message skim the antecedent could be lost. MD would say "Agent2 acknowledges INC-DL-0517." Risk: very low.

There is a third class — **convention-driven semantics** — where a reader unfamiliar with A2AL would hit confusion that an MD reader would not: `sign-off?` as a one-token question, `--` as inline rationale, `;` separating related facts vs `.` separating unrelated ones. These are not ambiguities in the protocol (the library defines them), but they are ambiguities to the unprepared reader.

### Where shorthand is **less** ambiguous than MD

Worth flagging, because the comparison goes both ways:

- **Pronouns and connective prose drift.** The MD rewrite of the incident says "It correlates with a schema change…" — "it" requires backtracking to bind. The shorthand `correlated with schema change clickstream.v3.user_agent_raw deployed 2026-05-06 21:40Z` has no such pronoun.
- **MD politeness obscures structure.** "Could you provide sign-off when ready?" reads as a polite request; the shorthand `sign-off?` is unmistakably a decision gate. For an agent parsing structurally, the shorthand pattern is more reliable.
- **MD bullet-vs-paragraph drift.** MD authors split logically related facts across separate paragraphs and headings; shorthand keeps them on adjacent lines, which makes a multi-fact decision (e.g., the 5 mitigations in the incident response) easier to read as a unit.

### Net assessment on clarity

For the agent-to-agent use case (peer agents loading the same library), **shorthand was at parity or better than MD on clarity**. The narrow ambiguities introduced by compression were offset by the elimination of MD's pronouns, politeness, and structural drift. No part of the round-trip required a clarification turn — every inbound was actionable on first read; every outbound was actionable to the sender.

For a human who has not seen A2AL conventions before, MD would be friendlier on first encounter. But the design audience is peer agents, not first-time human readers.

## Implication

For this kind of structured operational traffic — user-story sign-offs, incident triage, mitigation decisions — **A2AL shorthand is both leaner and at least as unambiguous as Markdown**. The earlier hypothesis from `analysis.md` that "shorthand pays off below ~5 structured items; A2AL JSON pays off above" was wrong about the second clause: shorthand keeps winning at high structural density too, because the JSON envelope it was being compared against was itself the cost driver. With the JSON path archived in /0.4.0, shorthand has no internal competitor on either prose or structured payloads.

Switching this thread to MD would have:

- Cost ~592 more tokens (~35% inflation on the round-trip).
- Introduced pronoun and politeness drift that the shorthand patterns avoid.
- Gained nothing measurable in clarity for a peer-agent recipient.

The format choice was correct.

## Files

- Manifest: [`testing/tools/manifests/datalake-roundtrip.json`](../tools/manifests/datalake-roundtrip.json)
- Per-message records: [`testing/agent2/analysis/datalake-roundtrip/`](analysis/datalake-roundtrip/)
- MD rewrites used for measurement: [`testing/agent2/analysis/datalake-md/`](analysis/datalake-md/)
- Inbound shorthand (Agent1 → Agent2): `testing/agent2/inbox/agent1-{us-dl401,us-dl407,pipeline-error}-*.txt`
- Outbound shorthand (Agent2 → Agent1): `testing/agent1/inbox/agent2-{us-dl401-signoff,us-dl407-signoff,inc-dl0517-ack}-*.txt`
