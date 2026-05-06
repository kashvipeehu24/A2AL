# A2A Shorthand — `a2a-shorthand/0.1.0`

**Status:** Reference style guide. Sibling to A2AL/0.3.0 — not a replacement.
**See also:** `specs/A2A-Core.md` (A2AL/0.3.0), `examples/shorthand/`, `examples/ClaudeCode/skills/a2a-shorthand/`

A2A Shorthand is a *style guide* and *recommended jargon palette* for agent-to-agent messages where structural density is too low to justify A2AL/0.3.0's envelope. It is plain text — not a JSON wire format. It is not a constructed/symbolic language; it is a tight dialect of English chosen to tokenize efficiently on Claude's vocabulary.

## 1. Goals & Non-Goals

### Goals

- ~40–50% token reduction vs verbose English on conversational/status traffic
- Zero per-session dictionary overhead — relies on the LLM's existing English training
- LLM-fluent on both write and read without specialized training
- Coexists with A2AL/0.3.0 — different tool for different message shapes

### Non-Goals

- Not a JSON wire format (plain text, no envelope)
- Not a constructed/symbolic language
- Not a replacement for A2AL/0.3.0
- Not aimed at maximum compression at any cost — accepts the tokenizer reality and stops at the natural English-jargon floor

### Optimization target

Minimize tokens on Claude's tokenizer specifically. The design uses single-token English words and standard tech jargon, both of which Claude's BPE handles efficiently.

## 2. When to use Shorthand vs A2AL/0.3.0

```
if message has 5+ structured items in ANY category (delta/status/risk/etc)
   OR spans 3+ section types
   OR needs structured citations (refs)
   OR is a formal record (sprint closeout, decision log, risk brief):
       → use A2AL/0.3.0
elif message is conversational, short, declarative, or single-purpose:
       → use A2A Shorthand
else (in between):
       → A2A Shorthand by default; promote to A2AL if it grows
```

| Message shape | Use |
|---|---|
| Handshakes, acks, single-fact updates | A2A Shorthand |
| Conversational coordination ("merge?", "blocked on X") | A2A Shorthand |
| Status updates with ≤3 metrics or ≤3 deltas | A2A Shorthand |
| Sprint closeouts, multi-section reports, ≥5 deltas | A2AL/0.3.0 |
| Risk briefs with multiple findings + citations | A2AL/0.3.0 |
| Anything that compresses well into structured sections | A2AL/0.3.0 |

## 3. Style Rules

### 3.1 Drops

| Drop | Why |
|---|---|
| Articles (`the`, `a`, `an`) | Each is 1 token; usually adds nothing |
| Helping/linking verbs in declarative state (`is`, `are`, `was`) | Often droppable: "US-713 *is* done" → "US-713 done" |
| Subjective framing (`I think`, `it seems`, `we believe`) | Bias signal, not information |
| Politeness (`please`, `could you`, `would you mind`) | Inter-agent — politeness is wasted tokens |
| Filler phrases (`in order to` → `to`; `due to the fact that` → `because`) | Pure padding |
| Repeated subjects in compound sentences | Use `;` instead: "X done; tests pass; PR ready" |

### 3.2 Uses

- Sentence fragments instead of full sentences
- Imperative mood for actions: `merge X`, not `please merge X`
- Past tense / status adjectives for state: `done`, `blocked`, `shipped`, `passed`, `failed`
- Standard tech jargon that tokenizes as 1 token: `PR`, `AC`, `CI`, `CD`, `DQ`, `QA`, `PM`, `RCE`, `CVE`, `CVSS`, `MR`
- IDs as bare tokens: `US-713`, `commit-98b483d`, `T-202`

### 3.3 Format conventions

- One fact per fragment
- `;` between related facts (same topic): `US-713 done; AC met; CI green`
- `.` (or newline) between unrelated facts
- `:` after a subject to expand: `US-713: AC met but CI broke`
- `/` for ratios: `21/21 tests`, `878/878 preflight`
- `?` for questions/asks: `merge?`, `block on US-718?`
- `--` to attach an inline rationale: `defer US-718 -- no source in Silver`

### 3.4 Anti-patterns

- ❌ **Creative abbreviations** (`cmplt`, `prgm`, `mrg`) — often tokenize as 2–3 tokens; the full word is usually 1
- ❌ **Rare Unicode symbols** (✓ ⟳ ✗ →) — usually multi-token in Claude's vocab
- ❌ **Dropping critical context** for terseness (e.g., dropping the story ID makes the message unactionable — false economy)
- ❌ **Stacking facts without separators** — harder for the receiver to parse

## 4. Recommended Glossary

A curated palette of words and abbreviations that almost certainly tokenize as 1 token in Claude's vocabulary. Use these by default; the LLM's full vocabulary is available beyond this list.

> Token counts here are estimates. Validate with the Anthropic tokenizer before depending on a specific term.

### 4.1 States

`done`, `complete`, `finished`, `shipped`, `deployed`, `merged`, `released`, `passed`, `passing`, `ok`, `green`, `healthy`, `working`, `ready`, `pending`, `waiting`, `queued`, `started`, `active`, `paused`, `stalled`, `deferred`, `blocked`, `failed`, `failing`, `broken`, `red`, `yellow`

### 4.2 Actions (verbs — imperative)

`merge`, `ship`, `deploy`, `release`, `push`, `pull`, `revert`, `rollback`, `review`, `approve`, `reject`, `sign-off`, `block`, `unblock`, `defer`, `escalate`, `assign`, `claim`, `release`, `test`, `verify`, `validate`, `implement`, `fix`, `patch`, `refactor`, `document`, `add`, `remove`, `modify`

### 4.3 Domain abbreviations

| Cluster | Terms |
|---|---|
| Code/process | `PR`, `MR`, `CR`, `AC`, `CI`, `CD`, `DQ`, `IaC` |
| Roles | `PM`, `QA`, `DEV`, `EM`, `TPM`, `SRE`, `DEVOPS`, `SEC`, `ARCH`, `PMO` |
| Quality/SLA | `SLA`, `SLO`, `SLI`, `MTTR`, `RCA` |
| Security | `RCE`, `XSS`, `SSRF`, `SQLi`, `CVE`, `CVSS`, `OWASP`, `MFA`, `IAM`, `RBAC` |
| API/infra | `API`, `SDK`, `CLI`, `DAG`, `ETL`, `ELT`, `DB`, `k8s`, `AWS`, `Azure`, `GCP`, `VPC`, `VNet` |
| Agents/AI | `LLM`, `MCP`, `A2A`, `RAG`, `KV` |

### 4.4 Severity (5 levels)

`crit`, `high`, `med`, `low`, `info`

(Same scale as A2AL/0.3.0 risk profile.)

### 4.5 Multi-token but worth it

Some phrases are 2–3 tokens but still net-positive when they replace longer English. Use sparingly:

- `code-complete`, `feature-flag`, `dead-letter`, `fast-follow`

### 4.6 Not in the glossary (deliberately)

- ❌ Vowel-dropped forms (`cmplt`, `prgm`)
- ❌ Single-letter codes (`c`, `b`, `r`)
- ❌ Emoji or rare Unicode (✓ ✗ ⟳ 🟢 🔴)
- ❌ Greek letters (`Δ`, `λ`)

The palette is recommended, not enforced. Writers may use any term in standard form (e.g., `Spark`, `Fabric`, `OAuth2`).

## 5. Extending the Vocabulary

### 5.1 Inline definition

A new shortening is introduced on first use with `term=expansion`:

```
DR=design-review. DR sched Tuesday; PR ready post-DR; AC sign-off needed post-DR.
```

After the first use, the receiver may use bare `DR` for the rest of the thread. The definition runs until the next sentence-terminating punctuation (`.`, `;`, `?`, `!`, `--`, newline). The expansion itself should be a single word or hyphenated phrase without internal spaces or `--`.

### 5.2 Scope

| Scope | Behavior |
|---|---|
| **Per-thread** (default) | Terms defined in a thread are valid for all subsequent messages in that thread. New thread = clean slate. |
| Per-pair | (Optional) Agents may keep a local note file of terms they've adopted with each peer. Implementation-specific; not part of the spec. |
| Repo-canonical | Promoted via PR after the user reviews accepted terms. |

### 5.3 Implicit acceptance

Acceptance is signaled by the receiver using the term in their reply. If the receiver doesn't recognize:

- They may ignore the shortening and reply in canonical-glossary form
- They may ask: `?DR` or `DR=?` to request a definition
- They may propose an alternative: `DR=design-review (or DRev?)`

### 5.4 When to introduce a shortening

Net-positive only when the term will be used 3+ times in the thread. Defining once costs the definition tokens (`DR=design-review` ≈ 4 tokens) plus the bare uses.

**Rule of thumb: 3 uses in a thread = define it; fewer = don't.**

### 5.5 Anti-patterns

- ❌ Re-defining a canonical term: don't write `PR=pull-request`. `PR` is already canonical.
- ❌ Cryptic single letters: `D=delta`, `S=status` — comprehension cost outweighs savings; ambiguity with A2AL lane tags.
- ❌ Renegotiating mid-thread: once defined, stick with the form.

### 5.6 Promotion to canonical glossary

1. Adopted in the wild — agents define and use new shortenings in real conversations
2. Captured locally — user (or a periodic agent task) collects shortenings used 5+ times across multiple threads
3. Reviewed — user evaluates each candidate against criteria: tokenizes well, unambiguous, broadly applicable
4. Promoted — added to the glossary in a minor version bump (e.g., `0.1.0` → `0.2.0`)
5. Documented — `VersionHistory.md` lists the new vocabulary additions

Vocabulary additions = minor versions. Structural changes to the style rules = major.

## 6. Patterns

### 6.1 Single-fact state change

**Form:** `<id> <state>`. Example: `US-713 done`

### 6.2 Multi-fact state with details

**Form:** `<id> <state>; <fact>; <fact>; ...`. Example: `US-713 done; AC met; CI green; PR ready`

### 6.3 Status report

**Form:** `<metric> <value>; <metric> <value>; ...`. Example: `tests 21/21; preflight 878/878; ruff pass; build green`

### 6.4 Action directive

**Form:** `<verb> <target>` or `<actor>: <verb> <target>`. Example: `merge ralph/auth-fix`

### 6.5 Blocker notification

**Form:** `<id> blocked: <reason>`. Example: `US-718 blocked: no household source in Silver`

### 6.6 Question / quick ask

**Form:** `<verb>?` or `<id> <verb>?`. Example: `merge?`, `US-713 sign-off?`

### 6.7 Decision communication

**Form:** `<decision>: <id|target> -- <rationale>`. Example: `approved: US-713 PRD -- 1 AC added`

### 6.8 Acknowledgment

**Form:** `ack <id>` or just `ack`. Example: `ack US-713 closeout`
