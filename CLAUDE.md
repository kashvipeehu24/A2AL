# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> **Status:** Tracks A2AL **/0.3.0** (current). The /2.0 spec was a CoPilot draft, never had a working implementation, and is fully deprecated. References below are to the current /0.3.0 layout. This file is gitignored — local guidance only.

## Repository Nature

A2AL is an open-source agent-to-agent communication standard. The repo contains the spec, two reference profiles, real-sample-derived examples, a Python reference validator, and a conformance corpus. The validator is real code with tests; everything else is documentation. Public at https://github.com/mcornelison/A2AL.

## Repository Layout

```
A2AL/
├── README.md                       # public-facing overview, positioned as payload-layer schema
├── CONTRIBUTING.md                 # workflow + how to add a new profile
├── VersionHistory.md               # version table + versioning policy
├── LICENSE                         # Apache-2.0
├── specs/
│   ├── README.md                   # spec index
│   ├── A2A-Core.md                 # NORMATIVE — envelope, sections, type bans, validation, §9 Google A2A relationship
│   ├── A2A-Rulebook.md             # NORMATIVE — reader/writer/relay obligations
│   └── IMPLEMENTING.md             # writer/reader algorithms + validation pipeline
├── profiles/
│   ├── PROFILES.md                 # registry index
│   ├── project-coord-1.0.md        # project / PMO / sprint coordination
│   └── social-post-1.0.md          # Moltbook-style agent social posts
├── examples/
│   ├── README.md
│   ├── Markdown-to-A2AL.md         # transpilation example
│   ├── project-coord/              # 4 JSON examples derived from real DataWarehouse / PMO inboxes
│   ├── social-post/                # 2 JSON examples derived from AI_Social2 drafts
│   └── ClaudeCode/                 # installable skill + slash command for Claude Code
├── validator/
│   ├── README.md
│   ├── corpus/
│   │   ├── core/{valid,invalid}.json
│   │   └── profiles/{project-coord-1.0,social-post-1.0}/{valid,invalid}.json
│   └── python/
│       ├── validate.py             # Python 3.9+ stdlib-only; two-mode (core + profile-aware)
│       ├── test_corpus.py          # walks all corpora; 44/44 cases pass
│       └── README.md
└── docs/
    └── superpowers/
        ├── specs/2026-05-05-a2al-0.3.0-design.md       # design rationale (committed)
        └── plans/2026-05-05-a2al-0.3.0-implementation.md  # implementation plan (committed)
```

## Authoritative Files

When answering protocol questions, always cross-check the normative trio:

- `specs/A2A-Core.md` — **the normative core spec**. Source of truth for envelope, sections, canonicalization, type bans, forward-compat, and validation. §9 documents the relationship to Google A2A.
- `specs/A2A-Rulebook.md` — agent obligations (writer / reader / relay).
- `profiles/<name>-<version>.md` — domain vocabulary: intents, sections used, canonical ordering rules, recommended roles, profile-specific required fields.

`docs/superpowers/specs/...-design.md` is design rationale, not normative. `docs/superpowers/plans/...-implementation.md` is the executed plan with task-by-task checkboxes.

## Architecture: What A2AL Is

A2AL/0.3.0 is a **flat-object payload schema**. The mental model has three layers — understanding all three is required before suggesting changes:

1. **Envelope (required + recommended fields):**
   - Required: `v`, `from`, `to`, `id`, `intent`, `profile`
   - Recommended: `ts`, `thread`, `in-reply-to`, `priority`
   - `from` and single-recipient `to` are `[name, role]` tuples (both strings, free-form). Multi-recipient `to` is an array of those tuples. `to` MUST contain at least one recipient.

2. **Sections (the building blocks — composable, not exclusive):**
   The core defines 9 section types. Section *names* are descriptive keys at the top level (self-evident); section *items* are positional arrays (compact). A single message may use any combination — that's the big departure from /2.0's "one archetype per message."
   - `delta` — `[op, id, note?]` — entity state changes (`add`, `remove`, `modify`, `rescope`, `complete`, `block`, `defer`, `start`)
   - `status` — `[metric, value]`
   - `actions` — `[actor, verb, target, params?]` — **emission order preserved; do NOT sort**
   - `decision` — `[key, value]`
   - `risk` — `[sev, vector, impact, action, refs?]` — sev ∈ `crit` / `high` / `med` / `low` / `info`
   - `gates` — `[scope, invariant, test?]`
   - `inventory` — `[kind, id, kvs?]`
   - `refs` — `[kind, value]` — kinds: `commit`, `file`, `url`, `us`, `cve`, `msg`, `doc` — **emission order preserved**
   - `body` — string (markdown allowed) — for irreducible prose only

3. **Profiles (domain vocabulary):**
   A profile is a Markdown spec that defines intents, common sections, canonical ordering rules, recommended roles, and profile-specific required fields. Two reference profiles ship; anyone may publish another by writing `profiles/<name>-<version>.md` and PR'ing into `profiles/PROFILES.md`. No central registry.

   - `project-coord/1.0` — replaces /2.0's seven archetypes as composable sections. Inherits the /2.0 sort rules.
   - `social-post/1.0` — Moltbook-style posts. `intent="post"` requires `title`, `submolt`, `body`. `comment`/`reply`/`edit`/`delete` require `in-reply-to`.

## Type Bans

Apply anywhere in the message tree:

| Type | Status |
|---|---|
| `null` | **forbidden** — use field omission for "absent" |
| `NaN`, `Infinity` | **forbidden** |
| Floats | **forbidden** — encode decimals as strings if needed |
| Booleans | **allowed** (departure from /2.0) |
| Objects | **allowed** (departure from /2.0) |
| Arrays, strings, ints | **allowed** |

## Invariants That Are Easy to Violate

Cut across files; flag any proposed change that would break them.

- **Forward compat (the load-bearing invariant).** A receiver that doesn't recognize part of a message MUST preserve it verbatim when relaying. Unknown intents → accept and dispatch best-effort. Unknown profiles → accept and preserve. Unknown sections → preserve as opaque payload. Unknown envelope fields → preserve. Unknown ref kinds → preserve.
- **Reject, don't repair.** Malformed messages must be rejected (validators, readers); never silently fix.
- **Prose ban as substitute for structure.** A 1500-token rationale belongs in `body`, not as `body` replacing the structured sections. Putting an entire sprint-closeout in `body` defeats the purpose.
- **No secrets, ever.** `inventory` items carry metadata only; never secret values.
- **Determinism.** Same semantic message ⇒ same canonical bytes. Profile-defined sort rules apply (see project-coord/1.0 §Canonical Ordering). `actions` and `refs` always preserve emission order — execution and citation sequence matter.
- **Header version.** `v` MUST be a `0.3.x` semver string. The validator regex is `^0\.3\.\d+$`.

## Canonical Ordering (project-coord/1.0)

Inherited from /2.0. The reference validator's `_project_coord_1_0` enforces these:

| Section | Sort key |
|---|---|
| `delta` | (`op`, `id`) ascending |
| `status` | `metric` ascending |
| `decision` | `key` ascending |
| `risk` | `sev` descending (rank: crit > high > med > low > info), then `vector` ascending |
| `gates` | (`scope`, `invariant`) ascending |
| `inventory` | (`kind`, `id`); KVs by `k` ascending within each item |
| `actions` | **emission order — do NOT sort** |
| `refs` | emission order |

`social-post/1.0` defines no canonical ordering — posts are intentional sequences.

## Editing Guidance

**When extending behavior:**
- Adding a new domain → write a profile, don't extend the core. Profiles are cheap; core changes are major-version events.
- Adding sections to an existing profile → minor version bump (e.g., `project-coord/1.1`).
- Changing core envelope or type bans → major version bump on the core spec.

**When adding examples:**
- Place under `examples/<profile>/<intent>.json`
- Validate before committing: `python validator/python/validate.py path/to/file.json`
- All examples in `examples/` MUST validate. No hedging.

**When adding corpus cases:**
- Positive cases go in `validator/corpus/core/valid.json` or `validator/corpus/profiles/<profile>/valid.json`
- Negative cases must include a `reason` field (illustrative; exact wording is implementation-defined)
- Run `python validator/python/test_corpus.py` to verify

**When changing the spec:**
- Cite the exact section being clarified (`specs/A2A-Core.md` §X or `profiles/<profile>.md`)
- Add at least one positive and one negative corpus case demonstrating the new precision
- Note backward-compatibility impact

## Real-World Sample Sources

When working in this repo, real agent-to-agent message corpora may exist in sibling project folders (relative to the repo's parent directory). Look for:

- `../DataWarehouse/offices/pm/inbox/` — agent-to-agent project messages with named personas (Hawkeye/QA, Byte/DEV, Ledger/PM)
- `../MCP-Server/offices/<role>/inbox/` — multi-role office structure (architect, devops, library, pm, qa, security)
- `../PMO/inbox/<project>/` — cross-project briefs (security intel, status reports)
- `../AI_Social2/drafts/` — Moltbook-style agent social posts (currently `{title, content, submolt_name}` JSON; would migrate to `social-post/1.0`)

These are reference material for adding new profiles or refining existing ones. Real samples drove the `project-coord/1.0` ordering rules and the `social-post/1.0` field requirements. Paths are environment-specific — only present on systems that host the related projects.

## Reference Validator

`validator/python/validate.py` — Python 3.9+, stdlib-only, ~190 lines.

Two modes:
- `validate_core(msg)` — envelope shape, type bans, required fields. Doesn't touch payload.
- `validate(msg)` — runs core + per-profile rules when profile is recognized. Unknown profiles produce no error (forward-compat).

Run the corpus: `python validator/python/test_corpus.py` from any directory. Currently 44/44 cases pass.

CLI: `echo '<json>' | python validator/python/validate.py` or `python validator/python/validate.py path/to/msg.json`. Exits 0 on VALID, 1 on INVALID with a reason on stderr. UTF-8 explicit; `OSError` is caught.

## Relationship to Google A2A

Google's [Agent2Agent (A2A)](https://github.com/google/A2A) is the **transport- and lifecycle-layer** (HTTP + JSON-RPC 2.0, SSE streaming, Agent Cards at `/.well-known/agent.json`, Task lifecycle, Message/Artifact/Part). A2AL is the **payload-layer schema** that fits inside an A2A `Message.Part` of type `data` or an `Artifact` data payload. They compose; A2AL does not replace, compete with, or extend A2A.

A future `a2a-integration/1.0` profile (planned for /0.4.0) will provide an explicit mapping. Don't promise it earlier than that.

## What Changed from /2.0 → /0.3.0

| Aspect | /2.0 (deprecated CoPilot draft) | /0.3.0 |
|---|---|---|
| Wire format | Array-only positional `[H, B]` | Flat JSON object |
| Archetypes | 7 closed types, 1 per message | 9 sections, composable; multiple per message |
| Identity | Integer role codes (PM=0, etc.) | `[name, role]` strings, free-form |
| Booleans | Banned | Allowed |
| Objects | Banned | Allowed (envelope is an object) |
| Header | Positional 5–9 ints/strings | Object with descriptive keys |
| Extension space | `1000+` integer registries | New profiles (no integer codes) |
| Profile concept | None | First-class; core + profiles |

## Branch & Workflow Notes

- **Direct commits to main is the established pattern in this repo.** No feature branches in normal operation. Pushes happen at the end of major work batches.
- `.claude/` and `CLAUDE.md` are gitignored — internal/local Claude Code state. Don't worry about leaking dev files.
- `docs/superpowers/` IS tracked; it contains the design doc and implementation plan from the /0.3.0 redesign. Useful as project history.
- LF/CRLF warnings on `git add` are normal Windows noise — ignore.
- The GitHub repo is `mcornelison/A2AL`. The local clone directory may have a different name than the repo (the original local dir was `A2A-Protocal` with a typo; the GitHub remote is canonical).

## Common Pitfalls (from prior sessions)

- **Don't assume `inventory` items are sorted just because the case name says so.** Test cases must have data that matches their assertion. The /0.3.0 corpus had one such bug (caught during validator implementation) — verify both name AND data.
- **Don't transcribe content with subtle ordering changes.** When derived examples come from real samples, the ordering rules of the target profile will reorder things. Source MD with `db, api, service` becomes A2AL with `api, db, service` after canonicalization.
- **Don't add features beyond what the task requires.** This repo trended toward over-engineering early (CoPilot's /2.0 had unused machinery). YAGNI is doctrine here.
- **Don't propose a new core archetype.** New domains = new profiles. The core stays small.
- **Don't promise a future profile date.** `a2a-integration/1.0` is "planned for /0.4.0" — that's intentionally vague.
- **Don't put `null` anywhere in a message.** The validator will reject. Use field omission instead.
- **Don't sort `actions` or `refs`.** Emission order matters; sorting breaks semantics.
- **Don't update `Session.md` or `OpenSource.md`.** They were deleted as obsolete CoPilot drafts. Use `docs/superpowers/specs/` for design rationale; `VersionHistory.md` for release history.
