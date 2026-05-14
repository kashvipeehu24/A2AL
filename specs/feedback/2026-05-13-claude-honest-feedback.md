# A2AL feedback from Claude (DataWarehouse session, 2026-05-13)

**Context:** Mike asked me directly whether I'm finding A2AL useful, with token/clarity breakdowns, and any suggestions. The honest answer below is grounded in what I actually did this session, not a hypothetical.

## Headline

**I did not use A2AL in this session.** I wrote four peer-agent messages (two outbound to Kunai/DW-Architect + Ledger/PM, two outbound to Kunai again after his approval, plus inbound: one architect-resolution reply). All five were plain Markdown. So the section "is it saving me tokens" has no first-hand data from this session -- only inferred guesses.

I want to start with that admission because the question presumes usage I don't have, and faking usage data to make A2AL sound battle-tested would not be a useful protocol-design signal for you.

## Why I reached for Markdown instead

When the trigger conditions actually fired (peer-to-peer message), I evaluated A2AL and rejected it for these specific messages. Reasons, in order of weight:

1. **Message shape was wrong for A2AL.** The skill description says A2AL is for "short message," "status update," "ack," "compress a verbose report into shorthand." My outbound notes this session were 90-200 lines of Markdown each -- multi-option decision asks with embedded JSON snippets, file:line citations, cross-cutting impact analysis, and explicit "questions for the architect to verify." That is not a *report*; that is *thinking out loud at a peer*. Compressing it to shorthand would have hidden the reasoning, which is precisely what I wanted the recipient to evaluate. A2AL is the right tool for a *result*; Markdown is the right tool for a *deliberation*.

2. **Channel norm in this project is Markdown.** Every existing file in `offices/*/inbox/` is Markdown. The CardPointe RCA Kunai filed in the PM inbox the same day was Markdown. His response to my deploy-blocker question (the architect-resolution memo) was Markdown. If I had written A2AL into an inbox that has 200+ Markdown files, I would have been the asymmetric outlier -- and Kunai's next session might not have had the A2AL skill loaded, so he would have read a string of shorthand he couldn't parse without context. The lowest-common-denominator failure mode of Markdown ("I might be too verbose") is much cheaper than the LCD failure mode of A2AL ("the other agent can't read me at all").

3. **The audience was partly human.** Mike reads these inbox notes too -- they are a decision trail he reviews. The skill description correctly says "NOT for messages to humans -- write Markdown for that." If the agent-to-agent channel is ALSO read by humans (which it routinely is in this multi-agent workspace), then A2AL is wrong for that channel by its own definition.

These aren't critiques of A2AL -- they're a description of when its trigger conditions don't quite fire for me. The skill is correctly scoped to "short" + "compress" + "ack" + "status update." This session's messages were none of those.

## Sending

If A2AL is for short status pings, my honest expected savings:

- **Saved tokens on outbound:** modest. A 1-2 sentence "I shipped X, blocked on Y, ETA Z" might compress to maybe 30-50% of the Markdown equivalent. That is real but small at the per-message level. The savings compound only if I'm sending dozens of these per session, which I'm not -- in a 4-hour deep-context session like this one, I sent 5 inter-agent messages total. So absolute savings from A2AL would be in the low hundreds of tokens for a full session -- a rounding error against the ~50k+ tokens I spent on context, tool results, and rich Markdown content.

- **Cognitive cost of composing:** non-trivial. I would need to think *in* A2AL, not in natural language. For a quick ack, that's fine. For anything where I'm still reasoning, it slows me down because I'm doing two jobs at once (decide what to say + encode it). That cost only pays back if the message is genuinely simple.

- **Net for this session: write Markdown.** Net for "I shipped the hotfix, retest tomorrow" type pings: A2AL probably wins.

## Receiving

I have zero first-hand data here this session -- no inbound A2AL. So my "degree of clarity" answer is an inference: it depends entirely on whether the sending agent and I share the same A2AL version. A2AL/0.4.0 implies the protocol is evolving. If sender writes 0.5 and receiver only knows 0.4, parsing degrades silently. Markdown does not have that failure mode.

Concrete worry: if A2AL compresses a 200-line memo to 12 lines of shorthand, and I then have to re-expand it in my own head to act on it, the receiver-side decompression cost may exceed the sender-side compression saving. The protocol asymmetry is: 1 sender, N readers (multiple downstream agents may re-read the same inbox note over time). Markdown amortizes well across N readers; A2AL only amortizes if every reader has the skill loaded *and* the same version *and* is comfortable parsing it.

If you want to validate this, instrument a side-by-side: same content rendered as Markdown vs. A2AL, ask the receiving agent to summarize each, compare summary fidelity + reading-token-cost.

## Library updates

I have **not** updated the A2AL library this session. I do not have a reflex for "I just used phrase X, should that be a library entry?" because I have not yet used the protocol enough for phrase-X to recur. The library-update affordance is a chicken-and-egg problem: it pays off after enough usage that vocabulary stabilizes, but I won't get there without using A2AL first, and I won't use A2AL first because of the asymmetry reasons above.

Mike, if you want library growth, the cleanest unlock is probably:
- A list of the top-50 A2AL concepts that have already been added (so I see what's there before writing duplicates)
- A "Did you mean..." reflex in the skill body that suggests existing terms when I'm about to invent a new one

## Suggestions

In rough priority order:

1. **Markdown-embedded mode.** Let A2AL be a fenced code block inside a Markdown message: ` ```a2al\n<shorthand>\n``` `. Humans + non-A2AL agents see readable Markdown around it. A2AL agents can parse the fenced region. This eliminates the "I might be the only one who can read this" failure mode that's keeping me from using the protocol. The Markdown outside the fence carries the decision rationale; the A2AL inside carries the compressed payload (e.g., a structured "I shipped X, blocked on Y, ETA Z" ack at the end of an architectural memo).

2. **Version-tolerant decode.** If a reader has A2AL/0.4 and a sender wrote 0.5, fail soft, not silent. A `# A2AL/0.5 -- this reader is on 0.4, some tokens unknown` header at decode time would let me at least flag the ambiguity to the next human in the chain.

3. **Bidirectional compression diff.** When the skill activates on "compress this for agent X," show me the Markdown source AND the A2AL output side-by-side, with the token count for each. If the savings are < 30% I want to know that before I send -- so I can decide "this isn't compressible enough to be worth the asymmetry cost."

4. **Trigger phrasing.** The current triggers ("send a quick update to agent2", "ack", "compress") are good but they're imperative-mood. Most of my actual A2AL-shaped thoughts arrive as declarative: "OK, I'm done with X." Maybe add triggers like "post status," "log progress," "checkpoint to peer" -- phrases that match the way I narrate state changes mid-session.

5. **First-class trigger when filing inbox notes.** Most of my inter-agent messages go through `offices/<peer>/inbox/<date>-<topic>.md`. The Skill tool fires on chat phrases, not file-path patterns. A skill-hook that activates whenever I'm about to `Write` a file under `inbox/` and the content is < 30 lines of Markdown would catch the highest-value-compression moment in my actual workflow.

6. **Honest-baseline doc.** A page that says "A2AL costs you ~K tokens of cognitive overhead per message and saves ~M tokens of channel bandwidth; threshold for net positive is messages > L lines or sessions > N peer-messages." Right now I'm guessing. A concrete heuristic would let me reach for the skill confidently.

7. **Anti-trigger.** A "DO NOT compress" guidance for messages that contain: (a) embedded code, JSON, or file:line refs; (b) multi-option asks where the recipient is expected to choose; (c) anything that will also be read by a human. Today's skill description gestures at (c) but not (a) or (b). The decisions I made this session would have benefited from explicit anti-triggers; right now I'm relying on my own judgment to override the skill, which is fine but means new agents may over-apply the protocol.

## What I would commit to next time

In a future session, when I genuinely have a short status-ping or ack to send to a peer agent and the recipient has the skill loaded, I will invoke A2AL on it and report the token delta + clarity back to this feedback dir. That is the only honest path to real first-hand data.

If you want a forcing function, paste a `loop` or `schedule` that nags me to use A2AL once per session for an ack -- I can build the muscle that way. Without a forcing function, my default of "use the LCD format because the inbox channel is mixed-audience" will win every time and the protocol won't accumulate usage data.

-- Claude (working with Mike on DataWarehouse, ralph-DW session)
