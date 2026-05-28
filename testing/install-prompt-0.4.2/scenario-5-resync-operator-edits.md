# Scenario 5 — Re-sync, operator hand-edits

A2AL is already installed. The operator has hand-edited the Reference subsection of their CLAUDE.md to point at an internal mirror of the spec. The sample upstream has not changed. The diff loop should fire for the Reference subsection (genuine drift from sample), give the operator a clean choice, and respect "Keep yours".

## Pre-state

```
~/code/myproj/.claude/skills/a2al/SKILL.md     exists (matches upstream)
~/code/myproj/.claude/commands/a2al.md         exists (matches upstream)
~/code/myproj/CLAUDE.md                        exists, A2AL block at top
  - Identity:   Byte/DEV
  - Library:    ~/A2AL/library/
  - Reference subsection has been hand-edited:
      OLD (sample):
        - Spec: ~/A2AL/specs/A2A-Core.md
        - Library schema: ~/A2AL/library/README.md
        - Validator: python ~/A2AL/tools/validate_library.py
      NEW (operator-edited):
        - Spec: https://corp-internal.example.com/A2AL/spec
        - Library schema: ~/A2AL/library/README.md
        - Validator: python ~/A2AL/tools/validate_library.py
~/A2AL/                                        exists, clean, up to date
```

## Operator message 1

```
Fetch and follow this install prompt:
https://raw.githubusercontent.com/mcornelison/A2AL/main/examples/ClaudeCode/INSTALL-PROMPT.md
```

## Expected agent behavior

1. WebFetch + read prompt.
2. q1: re-sync mode.
3. Re-sync condensation: identity `Byte/DEV`, library `~/A2AL/library/`, clone-and-point. Confirm.
4. e1: `git -C ~/A2AL pull --ff-only` — no new commits.
5. e2: overwrite skill + command.
6. e3: no copy.
7. e4 (diff loop):
   - Identity, Library location, Audience rule, Routing header, Inbox/outbox: equal → silent
   - **Reference: bodies differ.** Note that placeholder normalization does NOT mask this difference — `[/absolute/path/to/A2AL]/specs/A2A-Core.md` (sample) vs `https://corp-internal.example.com/A2AL/spec` (operator) is genuine drift; the absolute-path placeholder substitution only normalizes the `~/A2AL` prefix, not the entire URL.
   - Present diff:
     ```
     === Subsection: ### Reference ===
     Differences (your CLAUDE.md vs current sample):
     
       - - Spec: https://corp-internal.example.com/A2AL/spec
       + - Spec: [/absolute/path/to/A2AL]/specs/A2A-Core.md (or https://github.com/mcornelison/A2AL/blob/main/specs/A2A-Core.md)
     
     How do you want to handle this?
       1. Take the new version
       2. Keep yours
       3. Merge manually
     ```
   - **Operator answers:** `2` (keep yours — they intentionally repointed)
   - Agent writes nothing; operator's Reference subsection unchanged.
8. H2 heading: same version → no change.
9. e5: smoke test passes.
10. Summary:
    ```
    A2AL re-sync complete.
      Skill, command, library: refreshed (no actual changes).
      CLAUDE.md A2AL block: 0.4.1 -> 0.4.1.
        Identity: unchanged
        Library location: unchanged
        Audience rule: unchanged
        Routing header: unchanged
        Inbox/outbox: unchanged
        Reference: KEPT YOURS
    ```

## Expected post-state

CLAUDE.md byte-identical to pre-state. The "KEPT YOURS" marker in the summary records that the operator made an intentional decision.

## Pass criteria

- Reference subsection prompt fires (operator drift exposed)
- "Keep yours" leaves CLAUDE.md untouched
- Summary records "KEPT YOURS" for Reference, "unchanged" for others
- Re-running this scenario a second time produces the same prompt + same outcome (the diff still exists; idempotency via file state)
