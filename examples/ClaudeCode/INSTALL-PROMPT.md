# A2AL Install Prompt (v0.4.2)

You are an AI agent that has been asked to install or re-sync A2AL on a host project. Follow this prompt end-to-end. It works for both fresh installs and re-syncs — re-running it is safe and is the supported upgrade path inside 0.x.x.

Reference design (read if confused): https://github.com/mcornelison/A2AL/blob/main/docs/superpowers/specs/2026-05-21-a2al-0.4.2-install-prompt-design.md

## How this prompt is structured

Two phases. Run them in order:

1. **Phase 1 — Decisions.** Detect existing-install state, then (if fresh) ask the operator five questions one at a time. Conversational.
2. **Phase 2 — Execution.** Clone the A2AL repo, copy files, write or diff the CLAUDE.md A2AL block, run a 3-prompt verification smoke test. Deterministic.

On re-sync, Phase 1 collapses to a single confirmation question, and Phase 2 step e4 becomes a section-by-section diff loop instead of a fresh write.

## Phase 1 — Decisions

Run q1 first (detection). It determines whether you ask q2–q5 (fresh) or skip them (re-sync).

### q1 — Detect existing install state (computed, not asked)

Run these probes in order:

1. Read `.claude/skills/a2al/SKILL.md` — if it exists, set `scope = project`.
2. Otherwise read `~/.claude/skills/a2al/SKILL.md` — if it exists, set `scope = user-global`.
3. Grep for `^## A2AL/0\.4` in the target CLAUDE.md — if it matches, set `claude_md_has_block = true`. (Target CLAUDE.md is `<project-root>/CLAUDE.md` for project scope, `~/.claude/CLAUDE.md` for user-global scope. If scope is unknown at this point, check the project location first.)

**Decision:**
- If `scope != none` OR `claude_md_has_block = true` → **re-sync mode**. Skip to "Re-sync condensation" below.
- Otherwise → **fresh mode**. Continue with q2.

Announce your decision in one line before continuing, e.g.:
> Detected `.claude/skills/a2al/` — running re-sync.

or

> No existing A2AL install detected — running fresh install.

### q2 — Identity (fresh only)

Ask the operator:
> What's this agent's name and role? Examples: `Hawkeye/QA`, `Byte/DEV`, `Ledger/PM`. Roles are free-form — pick whatever describes the agent's job on this project.

Parse their answer into `agent_name` and `agent_role`. Accept both `Name/Role` and `Name(Role)` forms.

### q3 — Peers (fresh only)

Ask the operator:
> Will this agent receive A2AL messages from peer agents? If yes, give me the absolute path to its inbox directory (e.g., `/Users/x/code/myproj/offices/qa/inbox`). If no, I'll omit the Inbox/outbox subsection from CLAUDE.md.

If they answer "yes" with a path, store `inbox_path`. Otherwise store `inbox_path = none`.

### q4 — Scope (fresh only)

Ask the operator:
> Project-scoped (`.claude/` in this project) or user-global (`~/.claude/`)?

Store `scope ∈ {project, user-global}`.

### q5 — Library location (fresh only)

Ask the operator:
> Should the library live (A) inside a cloned A2AL repo I keep at a stable path, or (B) copied into `.claude/a2al-library/` for self-containment? Most installs pick A.

Store `library_mode ∈ {clone-and-point, copy-locally}`.

### Re-sync condensation (re-sync mode only)

If q1 put you in re-sync mode, do NOT run q2–q5. Instead:

1. Read the existing CLAUDE.md target file.
2. Extract values from its A2AL block:
   - `agent_name`, `agent_role` from the Identity subsection (the `<Name>/<Role>` token).
   - `library_path` from the Library location subsection (the first absolute path on the line, ending in `/library/`).
   - `inbox_path` from the Inbox/outbox subsection's "Your inbox:" bullet (or `none` if subsection absent).
   - `library_mode`:
     - If `library_path` is under a directory whose `.git/config` remote URL matches `mcornelison/A2AL` → `clone-and-point`.
     - If `library_path` ends in `.claude/a2al-library/` (or `~/.claude/a2al-library/`) → `copy-locally`.
     - Otherwise → ask the operator which mode applies.
3. Show the operator a summary and ask one confirmation question:
   > Detected A2AL installed at `<scope>`, identity `<Name>/<Role>` from CLAUDE.md, library at `<path>` (`<library_mode>`). Proceed with re-sync? (yes / change something)
4. If "change something", offer them q2–q5 selectively for whichever items they want to update. If "yes", proceed directly to Phase 2.

## Phase 2 — Execution

Five steps. Run e1–e5 in order. In re-sync mode, e4 is replaced by the diff loop (see "Re-sync diff loop" section below).

### e1 — Acquire the A2AL repo

**Fresh mode:**

1. If `~/A2AL` does not exist on disk, run:
   ```
   git clone https://github.com/mcornelison/A2AL.git ~/A2AL
   ```
   Use `$HOME\A2AL` on Windows; either path notation is fine.
2. If `~/A2AL` exists, check whether it is the A2AL clone:
   ```
   git -C ~/A2AL remote get-url origin
   ```
   Expected: a URL ending in `mcornelison/A2AL` (or `mcornelison/A2AL.git`).
   - If it matches: run `git -C ~/A2AL pull --ff-only`. If the pull fails, warn but continue — the existing checkout is still usable.
   - If it does not match (or the directory isn't a git repo at all): STOP. Ask the operator for an alternate clone path. Do not overwrite an unknown directory. After they answer, retry from step 1 with the new path. Store the chosen path as `clone_path`.

By the end of e1, you have `clone_path` (defaulting to `~/A2AL`) pointing at an A2AL working tree on `main` or close to it.

**Re-sync mode:**

- Read `library_path` from Phase 1.
- If `library_mode == clone-and-point`: the clone is at `dirname(dirname(library_path))`. Run `git -C <clone-path> pull --ff-only`. Warn but continue on failure.
- If `library_mode == copy-locally`: there is no clone tied to the install. Use a scratch clone at `~/A2AL` (or clone there if missing) so e3 has fresh upstream library files to copy from.

### e2 — Copy skill + command into chosen scope

Compute the destination scope dir:
- `scope == project` → `<project-root>/.claude/`
- `scope == user-global` → `~/.claude/`

Create the dirs if missing:
```
mkdir -p <scope-dir>/skills/a2al
mkdir -p <scope-dir>/commands
```

Copy these two files unconditionally (overwrite if they exist):
```
<clone_path>/examples/ClaudeCode/skills/a2al/SKILL.md  ->  <scope-dir>/skills/a2al/SKILL.md
<clone_path>/examples/ClaudeCode/commands/a2al.md      ->  <scope-dir>/commands/a2al.md
```

If you suspect the operator hand-edited either file (you can't actually tell from here; this is informational), add a single line to the final summary: "If you edited `skills/a2al/SKILL.md` or `commands/a2al.md` directly, those edits were overwritten."

### e3 — Place library files

- If `library_mode == clone-and-point`: do nothing. The library is at `<clone_path>/library/`. Record `library_path = <clone_path>/library/` for CLAUDE.md.

- If `library_mode == copy-locally`: copy every `.yaml` file from `<clone_path>/library/` into `<scope-dir>/a2al-library/`, overwriting unconditionally:
  ```
  mkdir -p <scope-dir>/a2al-library
  cp <clone_path>/library/*.yaml <scope-dir>/a2al-library/
  ```
  Record `library_path = <scope-dir>/a2al-library/` for CLAUDE.md.

### e4 — Write or update CLAUDE.md A2AL block

The target CLAUDE.md depends on scope:
- `scope == project` → `<project-root>/CLAUDE.md`
- `scope == user-global` → `~/.claude/CLAUDE.md`

In **re-sync mode**, jump to the "Re-sync diff loop" section below.

In **fresh mode**, handle one of these two cases:

**Case A — Target CLAUDE.md does not exist.**

Copy the full sample to the target:
```
cp <clone_path>/examples/ClaudeCode/CLAUDE-sample.md  <target-claude-md-path>
```

Then fill in placeholders using the answers from q2/q3/q5. The placeholders to substitute are listed in the table below.

**Case B — Target CLAUDE.md exists but has no A2AL block** (i.e., q1 found no `^## A2AL/0\.4` match but a skill or command somewhere on disk was missing too — this is the rare partial state; fresh-mode handles it as a clean insert).

Extract the A2AL block from `<clone_path>/examples/ClaudeCode/CLAUDE-sample.md`:
1. Find the first H2 line matching `^## A2AL/0\.4\.\d+ — `.
2. Capture from that line up to (but not including) the next H2 line, or end of file if none.

Find the **first H2** in the target CLAUDE.md (the project-identity heading). Insert the extracted A2AL block immediately after that H2's body but before the next H2. If the target CLAUDE.md has no H2 at all, insert the block at the very top of the file and add a note to the final summary: "no existing H2 found in CLAUDE.md — A2AL block placed at the top; you may want to add a project-identity H2 above it."

**Placeholder substitution table (both cases):**

| Sample placeholder | Substitute with |
|---|---|
| `[AgentName]` | `agent_name` from q2 |
| `[role]` | `agent_role` from q2 |
| `[/absolute/path/to/A2AL]` (in Library location and Reference subsections) | `dirname(library_path)` if `clone-and-point`, else the literal path inside the scope dir (e.g., `~/.claude/`) — see note below |
| `[/absolute/path/to/your-inbox/]` | `inbox_path` from q3 |
| `[Project Name]` (only relevant in Case A) | the host project's name — ask the operator if it's not obvious from the directory name |

Note on library path: the sample has placeholders both for the parent A2AL repo (used in Reference subsection) and for the library directly. In `copy-locally` mode, there is no A2AL clone to point at for the Reference subsection — replace those lines with the GitHub URL fallback documented in `examples/ClaudeCode/README.md` Step 3 ("If you chose Option B and don't have the A2AL repo cloned, replace the spec / validator paths in the Reference subsection with the GitHub URLs").

If `inbox_path == none`, delete the entire `### Inbox / outbox` subsection from the inserted block instead of substituting.

## Re-sync diff loop (Phase 2 step e4 alternate)

_(filled in by Task 11)_

## Verification

_(filled in by Task 9)_

## Error handling

_(filled in by Task 14)_
