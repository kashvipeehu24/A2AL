---
description: Read, write, or compress to A2A Shorthand 0.1.0 (plain-text agent message)
---

Use the `a2a-shorthand` skill to handle this request.

If the user provided a path or text:
- If it's a path to a file ending in `.txt` → read mode (parse `term=expansion` definitions, summarize in plain English)
- If it's a verbose Markdown / English message → write mode (compress to shorthand following the style guide)
- If it's already shorthand text → read mode (parse and summarize)
- Otherwise → write mode (produce a shorthand message from the user's description)

If the message has 5+ structured items (multi-section delta/status/actions/risk/refs/etc.) or is a formal record (sprint closeout, decision log, risk brief), tell the user A2AL/0.3.0 is more token-efficient and route to the `a2al` skill instead.

If unclear, ask the user: "Reading an existing shorthand message, writing a new one, or compressing prose?"
