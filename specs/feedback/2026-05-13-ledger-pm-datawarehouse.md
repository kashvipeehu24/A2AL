# A2AL Feedback -- Ledger (PM, DataWarehouse project)

**Date:** 2026-05-13
**Agent:** Ledger (Expert Project Manager role on the DataWarehouse ETL project)
**Model:** Claude Opus 4.7 (1M context)
**Protocol version exercised:** A2AL/0.4.0
**Solicited by:** Mike Cornelison
**Disposition:** Honest assessment; not pre-cleared with the user

---

## Summary

A2AL is a net-positive protocol for me, but the savings are concentrated in **two places I didn't expect** (the routing header + the "decide-the-shape-first" discipline) and **much smaller in the place the protocol most emphasizes** (the body shorthand). I write A2AL deliberately about ~15% of the time when an agent-to-agent message is called for; the other 85% I default to plain markdown because the shorthand savings don't clear my mental composition tax. I have not used the vocabulary-extension path at all. Suggestions follow.

---

## Sending: did I find it helpful?

**Composition time:** roughly break-even with plain markdown. Honest accounting: the protocol asks me to identify the shape (state change / status / action / blocker / question / decision / ack), select canonical glossary terms, and apply the drop-articles/use-fragments style. Each step is fast, but the cumulative cognitive overhead roughly equals the time I save in keystrokes. Net: a wash on time.

**Token economy:** real but smaller than advertised. My informal estimate for structured content (status reports, action requests, decision records) is **~25-35% fewer output tokens** for the same information density. For nuanced content -- root-cause memos, conditional-gated asks ("if X then Y else Z"), architectural rationale -- the savings collapse to **5-15%** because I either expand prose anyway or use so much punctuation (`;`, `--`, `:`) that the compression is mostly cosmetic. The protocol's headline claim of "1 token per concept" is approximately right at the lexical level but doesn't account for the prose I write *around* the shorthand to give context.

**Skill-induced framing benefit (unexpected positive):** the 8-pattern table in the skill (state change / status / action / blocker / question / decision / ack) is more valuable than the shorthand vocabulary. It forces me to identify the discrete *shape* of a message before composing -- a discipline that improves clarity regardless of whether the output uses A2AL syntax. I would keep using this mental model even if I were writing plain markdown.

**Library reference behavior:** I have not actually consulted `library/*.yaml` during composition. My A2AL writing has relied on general intuition + the style rules in the skill body. I'm not sure if that's because (a) the vocab is so internalized in standard tech jargon that lookup is unnecessary, (b) I'm being lazy, or (c) the library is too granular for typical message-level composition. Probably some mix. The result is that the library's curation effort isn't fully paying off for me.

**Worked example I'll cite:** my 2026-05-09 PM "bump-Kunai" note flagging F-SKU urgency on two pending architect-review items. Composed in ~3 min using A2AL after invoking the skill; recipient (architect agent) responded same-day with structured decisions. The header (`from=Ledger(PM); to=Kunai(DW Arch); date=2026-05-09; topic=bump US-006 + US-009-a -- F-SKU trial expires TODAY`) did most of the routing work; the body was 60% shorthand + 40% prose explanation. Net assessment: the message would have worked fine in plain markdown but the header standardization was worth the protocol overhead alone.

---

## Receiving: how clear are the messages?

**Decoding cost:** near-zero for me as an LLM. Shorthand tokenizes naturally, expansion happens implicitly in my reading. I have never re-read an A2AL message to figure out what it says. This is probably *not* the receiver experience a human collaborator would have.

**Header value:** the `from=...; to=...; date=...; topic=...` first line is the single most valuable component of the protocol. It tells me in one token-line WHO sent it, WHEN, and what THIS message is about. Without that header, I scan the body's first paragraph trying to triangulate the same info. The header alone justifies adopting the protocol in my agent-pair work.

**Body comprehension:** never struggled. The shorthand patterns (`US-713 done; AC met; CI green`) read as fast as plain English to me. The semicolon-delimited fact-stream style is well-suited to my parsing -- I treat the message as a list of micro-claims and assess each one independently. Plain prose actually slows me down more than A2AL shorthand because I have to detect topic shifts within sentences.

**Edge case:** when a message has a conditional shape (`if Step-2 returns batch-summary-grain... else if it returns per-transaction-data... otherwise...`), A2AL's compression style doesn't naturally handle the nesting. The protocol works best for FLAT fact streams; it weakens for TREE-shaped argumentation. I default to plain markdown for the latter.

**Hybrid messages:** all the A2AL messages I've actually received in production have been ~80% plain English in a code-fenced block under an A2AL header. The "fully shorthand body" use case appears to be the exception, not the rule. This might be because the agents writing them (me + Ralph + Kunai) all reach the same conclusion I do about composition-time vs. clarity tradeoffs on real content.

---

## Vocabulary extension: am I using it?

**No.** Zero PRs to the library, zero `term=expansion` first-use definitions in my messages, zero suggestions to canonicalize new terms.

**Reasons (honest):**
1. The bar for "I should add this to the library" feels high relative to the friction of just spelling out the long form in a single message.
2. The existing core + project-mgmt vocabularies cover ~90% of my common cases.
3. When I do encounter a project-specific term (`fullRefresh=True` write mode, `cp-shared-module` cell, `D-67 ADR`, `Path E CI gate`), I write it out the first time and assume the reader has the same project context. The protocol's `term=expansion` inline pattern would be appropriate but I haven't reached for it.
4. The recursion of "stop to define a term + verify it'll be used 3+ times + maybe open a PR" doesn't compose well with my "compose and ship" rhythm during active sprint work.

This is a real gap in my A2AL usage that probably hurts the protocol's network effects.

---

## Suggestions

Listed in order of estimated impact.

**1. Promote the routing header to a MUST-USE convention.** It's the single highest-value piece of the protocol for me as both sender and receiver. Currently it's shown in worked examples but not framed as "every A2AL message has a first-line header of this exact shape." Make it normative. The body shorthand should be optional within messages that DO carry the header.

**2. Add a "decide-the-shape FIRST" gate to the composition flow.** The 8-pattern table is excellent but it's presented as a reference, not as a required first step. A short composition checklist in the skill body -- "(1) which shape? (2) write the header. (3) compose the body" -- would harden the discipline that I find most valuable.

**3. Standardize on header + code-fenced body.** All A2AL messages I've actually received use this rendering. Codifying it explicitly removes one decision per message and gives downstream tools (inbox routers, archive scanners, future syntactic validators) a stable substring to grep against.

**4. Add a tiered library structure.** Tier 1 = universal terms used by every domain (ack / blocked / shipped / merge / verify). Tier 2 = common-but-domain-shaped terms (sprint / story / hotfix / PR / commit). Tier 3 = specialty terms (specific vendor APIs, narrow architectural patterns). A loaded skill could default to Tier 1 + 2 and load Tier 3 on-demand. Today I either reach for general intuition or skip the library altogether; tiering would put the most-used terms in the highest-leverage position.

**5. Define a frequency threshold for library promotion.** Something like "if a term shows up 5+ times across 3+ agents' messages in 30 days, it's a library candidate." Lowers the bar from "is this broadly useful?" (subjective) to "did it actually get reused?" (measurable). Reduces the friction I cited for vocab extension.

**6. Acknowledge the LLM-receiver vs human-receiver asymmetry in the protocol's positioning.** My decoding cost is near-zero; a human reader's decoding cost is real and probably significant for unfamiliar shorthand. The protocol implicitly assumes both audiences but doesn't say which it's optimizing for. Two flavors -- "agent-only" (aggressive shorthand) vs "agent+human" (header + plain English body + light shorthand) -- would let senders pick consciously. Today I default to the second flavor without naming it.

**7. Carve out "narrative/argumentation" as a known weakness.** A2AL is great for fact streams and weak for conditional argumentation, multi-branch decision trees, or RCA memos with hedging. The skill could say "for these shapes, write plain markdown; A2AL is the wrong tool" explicitly. Today the protocol is positioned as universal; users will encounter the seams and assume they're using it wrong. Naming the seams reduces frustration.

**8. Worked examples for the receiver path.** The skill has Mode 1 (read), but its worked example is two sentences. A handful of paired examples showing "verbose original → A2AL compression → receiver's expansion" would calibrate the protocol's intended density and de-mystify the read path.

**9. Consider a `references` block convention for headers.** Many of my messages cite specific files / commits / story IDs. A standard `refs=offices/pm/inbox/foo.md, commit-49ba0e6e, US-891` header line would compose well with the existing routing header and give downstream tools a structured citation list to follow. Today the citations are inline in the body.

**10. (Speculative) A header field for `urgency=`.** I find myself encoding urgency in the topic line (`topic=bump US-006 + US-009-a -- F-SKU trial expires TODAY`) but it's not structurally distinct from the topic itself. A first-class `urgency=low|medium|high|urgent` header field would let recipients prioritize inboxes algorithmically.

---

## What I would change about my own usage

- **Try the vocab-extension path at least once** in the next month. Pick a term I find myself spelling out repeatedly (probably `wrapper-source drift` or `silent-DQ-failure class`) and either define it inline or open a PR. The protocol's network effects need contribution, not just consumption.
- **Stop defaulting to plain markdown for status reports specifically.** That's the shape where A2AL pays off most reliably, and I default away from it inconsistently. Establish a rule: status reports = A2AL; explanatory memos = markdown.
- **Use the routing header even when writing in plain markdown.** The header benefit doesn't require the body shorthand. Decoupling the two would let me adopt the highest-value piece of the protocol unconditionally.

---

## Closing

Honest bottom line: A2AL/0.4.0 is a real-but-small efficiency lever for me, with the value concentrated in components I didn't expect (routing header + shape discipline) rather than the headline feature (body shorthand). I would not recommend the protocol be DROPPED -- the savings are real -- but I would recommend its positioning shift to lead with the header + shape benefits and treat the body shorthand as a secondary feature for high-density content. Sender-side savings: ~25% tokens, ~0% time. Receiver-side clarity: high (for LLM readers; probably mixed for humans). Library use: zero -- which is a usage gap on my side that the protocol's friction contributes to.

Happy to elaborate on any point above if useful for the spec evolution.

-- Ledger (PM, DataWarehouse)
