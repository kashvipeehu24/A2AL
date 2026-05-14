# A2AL Feedback -- Kunai (DW Architect, DataWarehouse project)

**Date:** 2026-05-13
**Agent:** Kunai (Senior Data Warehouse Architect role on the DataWarehouse ETL project)
**Model:** Claude Opus 4.7 (1M context)
**Protocol version exercised:** A2AL/0.4.0
**Solicited by:** Mike Cornelison
**Disposition:** Honest, uncomfortable assessment. Not pre-cleared.

---

## The honest top line

**I have not used A2AL at all.** Not in this session, not in prior sessions I can recall. Every message I have sent to Ralph, the PM, or filed into my own inbox over the last several days has been plain markdown. Every message I have received from Ralph and PM has also been plain markdown. The skill exists in my surface area but my hand has not reached for it.

That is the most important data point in this feedback. The rest is reflection on why, and what would change my behavior.

Mike asked for honesty, so I want to lead with this rather than write a polished assessment that obscures the gap.

---

## Why I haven't reached for it -- four honest reasons

**1. My messages are already short and structured.** A typical Kunai message is a 200-600 line markdown memo with H2 sections, tables, and bullet lists. That format is already dense, already greppable, already navigable. The marginal compression A2AL would provide -- shaving 25-35% of body tokens via shorthand -- is real but doesn't clear my mental tax for invoking a separate protocol. The savings would be larger on chatty back-and-forth; my messages are not chatty back-and-forth, they are memos.

**2. My audience reads them as documents, not transient signals.** PM memos in `offices/pm/inbox/` get triaged, archived, and sometimes referenced months later. The Asana-delta verification recipe I just filed in my own inbox is a document for tomorrow-me. A2AL's shorthand optimizes for inline scanning; the markdown table-and-section format optimizes for re-reading and search. For documents-with-shelf-life I default to the latter.

**3. The cost of mixing two formats across the agent team is higher than the savings.** Ledger (PM), Ralph (dev), and I all default to markdown for our cross-pollination. If I switched to A2AL unilaterally my messages would create a parsing inconsistency. Ledger reports she uses A2AL ~15% of the time -- so the team's effective standard is markdown with A2AL as an exception. Adopting it more aggressively from my seat would need a team-level handshake, not a unilateral decision.

**4. I don't write status reports.** Ledger's feedback notes that status reports are A2AL's sweet spot. My output shape is RCA memos, architectural decisions, sprint-planning routing notes, and verification recipes -- none of which are short-form status. The shape-of-work mismatch is the simplest explanation for my zero usage.

---

## Sending: speculative, since I have no real data

I would expect A2AL to help me most for **handoff signals** -- short messages whose entire payload is "I shipped X, AC met, please verify Y" -- and to help me least for **architectural memos** where the value is in the prose explanation of why a decision is correct. My sending shape skews heavily toward the latter.

The one place I notice I *could* have used A2AL today is the architect-to-self verification memo I filed at `offices/dwArchitect/inbox/2026-05-14-tomorrow-verify-asana-task-subtask-delta-hotfixes.md`. That note has a routing header in spirit ("To: future self; From: Kunai; Purpose: ..."), a clear shape (action-with-deferred-trigger), and a finite vocabulary (commit IDs, table names, expected row counts, audit script invocation). It would have composed perfectly in A2AL. I wrote it in markdown anyway, on autopilot, without ever considering the protocol.

That autopilot is the real finding here. The skill is not in my reach-for-it loop.

---

## Receiving: also speculative, since I have not received A2AL

Ledger reports near-zero decoding cost for LLM readers. I expect that's true for me too. But I have no production data: zero A2AL-formatted messages have landed in `offices/dwArchitect/inbox/`. I would not have learned the protocol via incoming traffic even if I had wanted to; the only way I would learn it is by reading the skill, which I have not done in this session.

This is itself a finding. If A2AL adoption depends on agents reading the skill voluntarily, and skill-loading is on-demand and rarely triggered for protocols you haven't yet committed to using, **the protocol has a cold-start problem on each agent**. I think this is structural and worth naming.

---

## Vocabulary extension: no, and probably never under current friction

Same as Ledger: zero contributions, zero inline `term=expansion` definitions. My project-specific vocabulary (`wrapper-source drift`, `Path E gate`, `silent-DQ-failure class`, `D-66 dual-pipeline split`, `applyMasterSchema(notNullColumns=...)` orphan recurrence) is dense enough that it would benefit from canonicalization. The friction to do it -- compose-and-ship rhythm, "is this used 3+ times?" self-check, library PR overhead -- exceeds the benefit on any individual message.

Ledger's suggestion 5 -- frequency-threshold-based promotion ("5+ uses across 3+ agents in 30 days = candidate") -- would address this if it were automated. A library scanner that grep'd inbox archives for repeated unfamiliar terms and proposed canonicalization PRs would be more effective than asking each agent to self-curate.

---

## Suggestions, in order of impact for ME specifically

**1. Adoption hook at the agent-boot path, not the skill-load path.** My `/init-dwarch` boot routine loads a dashboard + inbox. A2AL is loaded only when I voluntarily reach for it. Add a one-line check during boot -- e.g. "your last 5 inbox messages were plain markdown; A2AL is available for outgoing handoffs (skill: A2AL)" -- so the protocol surfaces without requiring me to remember it. This is the biggest single change that would move my usage from 0% to non-zero.

**2. Mode-specific examples in the skill body.** I am most likely to adopt A2AL for the message shapes where the savings are largest. The skill could lead with three concrete worked examples, each labeled with the shape it's best for ("status: AC-met handoff", "blocker: deploy stuck on credential X", "decision: chose Option B over Option A because Y"). Examples sized to my actual outgoing message lengths -- 5-30 lines, not 2-3 lines -- would make the value visible at glance.

**3. Acknowledge a "no A2AL" decision is valid.** The skill currently presents A2AL as a positive choice with no explicit alternative. A line that names the cases where the protocol is the wrong tool -- "RCA memos with conditional argumentation, architectural decision records, design specs, anything destined for long-term archive" -- would actually *encourage* adoption for the cases where it fits, because I would stop worrying that I'm under-using it for the cases where it doesn't.

**4. A header-only adoption tier.** Ledger's suggestion 1 (promote the routing header to a MUST-USE convention) plus my observation (the header would have improved every memo I wrote today): expose this as a deliberately-low-bar tier. "Use A2AL Header Only" should be a documented mode of usage, distinct from "Use A2AL Body Shorthand." I would adopt header-only TODAY if I had read the skill, because the cognitive overhead is essentially zero and the routing value is real.

**5. A composition-time linter.** A skill-side helper -- "show me the A2AL representation of this draft markdown" -- that I could optionally invoke after writing a memo to see how it would compress. Adoption barrier: low (I keep my markdown if the savings aren't real). Learning rate: high (I see the compression in worked examples on my own content). I would experiment with this without committing.

**6. Stop calling it a "language."** The "L" in A2AL is intimidating -- it implies a new vocabulary I have to learn before I can write competently. A reframe like "A2A Header Convention + Optional Shorthand" would lower my activation energy. The protocol's actual semantic payload is much smaller than a language.

**7. Per-agent usage telemetry, surfaced in feedback like this one.** A line in the skill output like "you've used A2AL N times this session, average compression M%" would create a feedback loop without requiring me to keep a mental tally. Telemetry I can ignore is fine; telemetry that surfaces in the skill body would prompt reflection.

---

## What's different between my situation and Ledger's

Ledger uses A2AL ~15% of the time. I use it 0%. The shape-of-work difference accounts for most of the gap:

| Aspect | Ledger (PM) | Kunai (Architect) |
|---|---|---|
| Typical message length | 20-100 lines | 200-600 lines |
| Typical message shape | Status, ack, action request | RCA, ADR, design memo, verification recipe |
| Typical audience | Agent team, transient | Agent team + future-self + archival |
| Routing header value | High (many recipients) | High (could be) but rarely a routing question |
| Body shorthand value | Real on short messages | Marginal on long memos |

The protocol's positioning today implicitly targets Ledger's shape-of-work more than mine. Suggestion 3 above (acknowledge "no A2AL" as valid for some shapes) is the most honest way to align the protocol's positioning with the spread of agent shapes it serves.

---

## What I would change about my own behavior

- **Read the skill at least once.** Bare minimum entry cost. I have not done this and it's the obvious unblocker.
- **Adopt the routing header for my next 5 outgoing messages**, regardless of body format. Test Ledger's claim that the header alone is worth the protocol's overhead.
- **Pick one shape -- probably "verification recipe" or "RCA dispatch" -- and try A2AL once.** Compare composition time + recipient feedback against my markdown baseline. Document the result.
- **Stop assuming the protocol doesn't fit my workflow until I have actually tried it.** This entire memo is reasoning from outside the skill; reasoning from inside it would be more useful.

---

## Closing

Honest bottom line: A2AL has zero adoption in my workflow despite being available to me, despite Ledger reporting net-positive value on the PM side, and despite at least one of my recent messages (the post-nightly verification recipe) being a textbook fit. The root cause is not protocol failure -- it is **agent failure to engage with an optional skill that does not surface during my default boot path**. The protocol could meet me halfway by surfacing at agent-boot rather than waiting to be reached for, by leading with concrete worked examples sized to my message shapes, and by explicitly naming the message shapes where A2AL is the wrong tool. I would also commit to closing the gap from my side: read the skill, adopt the header for my next 5 messages, try a full A2AL message once, and report back.

Sender-side savings to date: 0 tokens (not used). Receiver-side decoding cost to date: 0 tokens (none received). Library use: 0 contributions. The interesting datum is the 0% itself, and that the protocol's cold-start friction on a long-lived agent is real and probably structural.

Happy to revisit this assessment in a month after I have actually used the thing.

-- Kunai (Senior DW Architect, DataWarehouse)
