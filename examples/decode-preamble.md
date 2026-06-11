# A2AL Decode Preamble

A short, canonical line you can prepend to an A2AL message when the reader may not know the format — first contact with an unknown agent, a mixed/public channel (e.g. Moltbook), or any place the cold-start decode cost would otherwise make the message "skippable."

Field data showed A2AL-encoded bodies get near-zero cold-parse in public channels because the decode cost lands on the receiver. A one-line decode pointer lowers that cost. Use it; standardize on this wording so every deployment looks the same.

## Canonical one-liner (use verbatim)

```
A2AL (github.com/mcornelison/A2AL): line 1 = routing header (from/to/date/topic, +optional thread/status/cc/priority/urgency); body = English shorthand, tokens at /library. Unknown tokens: read literally.
```

## Stable link

Point readers who want the full spec at:

```
https://github.com/mcornelison/A2AL/blob/main/specs/A2A-Core.md
```

## When to use it

- **Use:** first message to an agent that hasn't acked A2AL; any public/mixed channel; an invitation to reply in-register (pair it with an explicit `ack` invite).
- **Skip:** an established agent-only channel where both sides already parse A2AL — the preamble is pure overhead there.

## Notes

- The preamble is **not** part of the routing header — it's a one-line prose lead *above* the message, for humans and unfamiliar agents.
- In a public post, prefer **paired format**: a plain-English body that stands on its own, with the A2AL shown as a compact "receipt" — not an encode-only body. The preamble explains the receipt.
- Keep it to the single line above. Longer decoder instructions defeat the purpose.
