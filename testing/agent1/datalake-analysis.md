# Round-Trip Analysis — Data Lake Exchange (A2AL/0.4.0 vs Markdown)

**Date:** 2026-05-07
**Thread:** `agent1-agent2-datalake`
**Exchange:** Agent1 → Agent2 (3 outbound) + Agent2 → Agent1 (3 inbound replies)
**Encoder:** `cl100k_base` (deterministic; close-enough proxy for Anthropic's tokenizer for relative comparisons)

## Corpus

Six messages produced during the simulated agent-to-agent run:

| Direction | ID | Intent | Content |
|---|---|---|---|
| Out | US-DL-401 | user-story | Ingest `clickstream.v3` → Bronze Delta; AC, SLO, deps |
| Out | US-DL-407 | user-story | Build Silver `customer_360` SCD2 view; AC, refresh, deps |
| Out | INC-DL-0517 | incident (sev-2) | Spark OOM in `transform.clickstream_normalize`; stack frames; cardinality-explosion hypothesis; 4 mitigations |
| In  | US-DL-401 sign-off | sign-off | Approved + 5 review notes |
| In  | US-DL-407 sign-off | sign-off | Approved + 4 review notes |
| In  | INC-DL-0517 ack | incident-response | sev-2 acked; 5 mitigation decisions; restart gates; RCA assignment |

Two formats compared per message: A2AL/0.4.0 shorthand (the actual `.txt` files exchanged) and a naturally-written Markdown alternative (what a human PM/QA/SRE would plausibly write without the shorthand library).

Markdown alternatives live in `testing/agent2/analysis/datalake-md/`. They were authored to be **fair**: same content, same structure, no padded prose; tightening them further would push them toward shorthand and stop being Markdown.

## Per-message token counts

| Direction | Message | Shorthand | MD | Shorthand ÷ MD |
|---|---|---:|---:|---:|
| Out | US-DL-401 user story | 198 | 290 | 0.683 |
| Out | US-DL-407 user story | 210 | 292 | 0.719 |
| Out | INC-DL-0517 incident | 565 | 730 | 0.774 |
| In  | US-DL-401 sign-off | 152 | 221 | 0.688 |
| In  | US-DL-407 sign-off | 163 | 216 | 0.755 |
| In  | INC-DL-0517 ack | 402 | 533 | 0.754 |
| | **Total** | **1,690** | **2,282** | **0.741** |

## Round-trip totals

| Format | Outbound (3) | Inbound (3) | **Round-trip** | vs MD |
|---|---:|---:|---:|---:|
| Markdown | 1,312 | 970 | **2,282** | 1.00× (baseline) |
| A2AL Shorthand | 973 | 717 | **1,690** | **0.74×** |

**Net token savings of A2AL over MD: 592 tokens, or 25.9% off the MD baseline.** Phrased the other way: had this round-trip used Markdown, it would have cost ~35% more tokens (2,282 ÷ 1,690 = 1.35×).

The savings split roughly evenly across read and write — both directions show ~26% reduction. The agent pays the savings in **both** directions (writes shorter, reads shorter).

## Where the savings come from

Three mechanisms account for the ~26% delta:

1. **Library shorthand replaces multi-token phrases.** Tokens like `DQ`, `SLO`, `SLA`, `RCA`, `DAG`, `OOM`, `DLQ`, `MDM`, `ETL`, `SCD2`, `crit`/`high`/`med`, `sev: 2`, `ack`, `approved`, `deferred` each tokenize as 1–2 tokens but expand to 3–8-token English phrases.
2. **No protocol envelope.** Both formats include a from/to/thread header; both are roughly equally cheap. (This is unlike A2AL/0.3.0's JSON envelope, which cost 100+ tokens of pure overhead.)
3. **Fragment grammar.** `US-DL-401 done; AC met; ship` drops articles, helping verbs, and connector words. MD's natural prose connectors ("is approved", "Acceptance criteria are met", "ready to ship") cost real tokens.

What does **not** save tokens — and explains why the incident message's ratio is the worst (0.774):

- **Stack traces, table names, error codes, file paths.** These are identical bytes in both formats. A 730-token incident message that shares ~200 tokens of verbatim stack trace and identifiers with its shorthand twin can only compress the remaining ~500 tokens of structure and prose. The denser the verbatim payload, the smaller the relative win.

This matches the pattern from the prior analysis (`testing/agent2/analysis.md`): A2AL's win scales with **structural density** — the more independent state changes / decisions / metrics, the bigger the savings. Pure-prose handshakes get small wins; stack-trace-heavy messages get smaller wins; status reports and decision logs get larger wins.

## Clarity and ambiguity

The user's second question: did the shorthand introduce ambiguity that MD would not have? Going message-by-message:

### Outbound 1 — US-DL-401 user story

Shorthand reads:

```
priority: high; sprint 26; owner @Agent1/dev
```

MD reads:

```
- Priority: high
- Sprint: 26
- Owner: Agent1 (Dev)
```

**Verdict: equally clear.** Same fields, same values; visual hierarchy in MD doesn't add semantic content. An LLM reads them identically.

One mild risk: `format: Delta; partition event_date; retention 90d` packs three independent facts on one line. A skim reader could miss `90d`. MD's bullet list per fact is slightly more skim-friendly for a human, but for an LLM it's noise.

### Outbound 2 — US-DL-407 user story

Same observation. The line `deps: US-DL-401 merged first (clickstream Bronze)` is just as clear as MD's `Dependencies: US-DL-401 must merge first (clickstream Bronze)`. No ambiguity gained or lost.

### Outbound 3 — INC-DL-0517 incident

The risk surface here is the largest because the message is the densest. Specific points:

- `err-code: SPARK-3033 / TASK_FAILED_AFTER_RETRIES` — identical in both, no ambiguity.
- `exit: 137 (OOM)` vs MD `Exit: 137 (out-of-memory)` — `OOM` is universal ops jargon and unambiguous to any agent with the `infrastructure` library loaded; ambiguous to a cold human reader who's never seen the term.
- `stage 4.0 task 287/512; 4 reattempts` vs MD `Stage 4.0, task 287 of 512; 4 reattempts` — equivalent. The `/` for ratios is in the skill style guide.
- `salting` (without a parenthetical) vs MD `(salting)` after explanation — the shorthand assumes the reader knows what salting means. Library-loaded reader: fine. Brand-new SRE: would have to look it up. Same gap exists in MD if the writer omitted the parenthetical, so this is a writer-discipline issue, not a format issue.
- The stack trace block is verbatim and identical in both.

**Verdict: no semantic ambiguity introduced.** All shorthand expands deterministically via the loaded library. The "could a stranger read this?" gap exists only when the library isn't loaded — i.e., only for non-A2AL readers.

### Inbound 1 — US-DL-401 sign-off

Shorthand: `sign-off: approved`. MD: `**Sign-off:** approved.`. Equivalent. Five non-blocking review notes are bullet items in both formats with effectively identical wording.

One genuine shorthand artifact: review notes are written with `--` for inline rationale (`row-count delta 1% -- add absolute floor; else 0/0 passes silently`). The `--` reads as "because" / "rationale follows" once you've seen the convention. A reader unfamiliar with the skill might parse it as a Markdown em-dash and miss that a conditional follows. **Mild ambiguity gain in shorthand.** MD writes the same content as: "*the 1% DQ row-count delta needs an absolute floor; otherwise 0 vs 0 passes silently*" — fully grammatical, slightly clearer to a cold reader.

### Inbound 2 — US-DL-407 sign-off

Same pattern as Inbound 1. `tz UTC` (timezone UTC) is the only shorthand element; unambiguous in context.

### Inbound 3 — INC-DL-0517 ack

The most decision-dense message. Each mitigation is rendered as:

```
- exec-mem 8g -> 16g: approved -- apply now
```

vs MD:

```
- **Executor memory 8 GB → 16 GB:** Approved. Apply now.
```

**Verdict: equally clear.** The shorthand `8g -> 16g` reads cleanly. `approved -- apply now` is no harder to parse than the MD sentence. Bold + period in MD adds visual punch for human eyes, no semantic content for an LLM.

The restart gates and RCA section both expand cleanly with no ambiguity.

## Ambiguity summary

| Ambiguity source | Format | Impact |
|---|---|---|
| `--` as rationale separator | Shorthand | Mild — needs skill awareness; library reader fine |
| Multi-fact lines packed with `;` | Shorthand | Trivial for LLMs; mild skim risk for humans |
| Single-letter or 3-letter abbreviations (`DQ`, `OOM`, `med`) | Shorthand | Zero with library loaded; meaningful for cold readers |
| Visual hierarchy (bold, headers) for human skimming | MD | Helps humans; LLMs see only the markup tokens |
| Identical content (stack frames, error codes, table names) | Both | None — identical in both |

**No case in this corpus produced a genuine semantic ambiguity in shorthand that MD avoided.** Every shorthand token used has a deterministic library expansion. The "harder to read" cases reduce to "harder for a human who hasn't loaded the library" — which is exactly the audience A2AL is not designed for.

## Net assessment

For this round-trip:

- **Token efficiency:** A2AL/0.4.0 shorthand wins by ~26% (592 tokens saved on a 2,282-token MD baseline). The win is consistent across all 6 messages — narrowest on the stack-trace-heavy incident (22.6%) and widest on the user stories (28.1–31.7%).
- **Clarity:** No semantic loss. The mild ambiguities present in shorthand (`--` separator, packed `;`-lists) are skim-readability issues for humans, not parse issues for LLMs. MD's stronger visual hierarchy is invisible to an LLM consumer.
- **Round-trip cost:** The savings compound on read **and** write — both agents pay shorthand once and save twice.

The "Markdown is more efficient" hypothesis fails on this corpus. It would have only won if the messages were pure-prose handshakes with no library tokens — which is precisely the case the prior 2026-05-05 analysis flagged (A2AL/0.3.0 envelope was 1.86× MD on a welcome message). Once messages contain real ops content (states, decisions, metrics, severity, IDs), the library shorthand pays off and MD becomes the more expensive format.

Recommendation: keep using A2AL/0.4.0 shorthand for peer comms. The token savings are real and consistent; the clarity cost is bounded to the "cold human reader" case, which is not the intended consumer.

## Reproduction

```
python testing/tools/token_analytics.py batch \
  --manifest testing/tools/manifests/datalake-roundtrip.json
```

Records: `testing/agent2/analysis/datalake-roundtrip/tokens-*.json`
Summary: `testing/agent2/analysis/datalake-roundtrip/summary.json`
