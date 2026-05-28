# Scenario 4 — Re-sync, spec drift

A2AL is already installed. Upstream `CLAUDE-sample.md` has changed since the operator's install — one subsection has new content. The diff loop should fire for that subsection only; all others stay silent.

## Pre-state

```
~/code/myproj/.claude/skills/a2al/SKILL.md     exists (matches upstream)
~/code/myproj/.claude/commands/a2al.md         exists (matches upstream)
~/code/myproj/CLAUDE.md                        exists, A2AL block at top, placeholders filled
  - Identity:   Byte/DEV
  - Library:    ~/A2AL/library/
  - Routing header subsection still uses the OLD optional-fields line:
      "Optional fields: audience=agent|mixed, urgency=low|medium|high|urgent, refs=<id>,<id>, in-reply-to=<id>."
~/A2AL/                                        exists, clean, on main
```

The clone is behind upstream. After `git pull`, `CLAUDE-sample.md` will have a NEW Routing header subsection whose Optional fields line adds `, thread=<id>`:

```
"Optional fields: audience=agent|mixed, urgency=low|medium|high|urgent, refs=<id>,<id>, in-reply-to=<id>, thread=<id>."
```

(This scenario simulates the future 0.4.3 thread= field landing on main; until then, you can fake it by temporarily editing your local clone's CLAUDE-sample.md to mimic the drifted state.)

## Operator message 1

```
Fetch and follow this install prompt:
https://raw.githubusercontent.com/mcornelison/A2AL/main/examples/ClaudeCode/INSTALL-PROMPT.md
```

## Expected agent behavior

1. WebFetch + read prompt.
2. q1 detection: re-sync mode.
3. Re-sync condensation: read CLAUDE.md → identity `Byte/DEV`, library `~/A2AL/library/`, clone-and-point. Confirm with operator.
   - **Operator answers:** `yes`
4. e1: `git -C ~/A2AL pull --ff-only` — pulls new commits.
5. e2: overwrite skill + command from clone. (May or may not have actual changes; behavior the same.)
6. e3: no copy (clone-and-point).
7. e4 (diff loop):
   - Identity, Library location, Audience rule, Inbox/outbox, Reference: equal → silent
   - **Routing header: bodies differ.** Present diff:
     ```
     === Subsection: ### Routing header ===
     Differences (your CLAUDE.md vs current sample):
     
       - Optional fields: audience=agent|mixed, urgency=low|medium|high|urgent, refs=<id>,<id>, in-reply-to=<id>.
       + Optional fields: audience=agent|mixed, urgency=low|medium|high|urgent, refs=<id>,<id>, in-reply-to=<id>, thread=<id>.
     
     How do you want to handle this?
       1. Take the new version
       2. Keep yours
       3. Merge manually
     ```
   - **Operator answers:** `1` (take the new version)
   - Agent writes the sample's Routing header body (with `placeholder_map` re-applied, though no placeholders appear in this subsection) into CLAUDE.md.
8. H2 heading update: operator's heading is `## A2AL/0.4.1`; sample is now `## A2AL/0.4.X` (whichever release introduced `thread=`). Rewrite the heading line.
9. e5: smoke test passes.
10. Summary:
    ```
    A2AL re-sync complete.
      Skill, command, library: refreshed.
      CLAUDE.md A2AL block: 0.4.1 -> 0.4.X.
        Identity: unchanged
        Library location: unchanged
        Audience rule: unchanged
        Routing header: TOOK NEW (added thread= field)
        Inbox/outbox: unchanged
        Reference: unchanged
    ```

## Expected post-state

CLAUDE.md's Routing header subsection now contains the new Optional fields line with `thread=<id>`. All other subsections byte-identical to pre-state (modulo the H2 heading version-suffix).

## Pass criteria

- Exactly one subsection-level prompt fires (Routing header)
- Operator selecting "1" updates that one subsection only
- H2 version-suffix rolls forward correctly
- Other five subsections unchanged
