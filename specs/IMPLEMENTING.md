# Implementing A2AL/2.0

Concise implementer's guide for agents that emit or consume A2AL messages. Companion to `A2A-Grammar.md` (normative grammar) and `A2A-Rulebook.md` (agent obligations).

> **Status:** Draft. Updated alongside the reference validator under `validator/python/`.

---

## 1. Writer Algorithm

A writer translates an internal state change or intent into an A2AL message.

```text
1. CLASSIFY input into exactly one archetype (typ ∈ 1..7).
   - Scope changes        → A1 (typ=1, lane "Δ")
   - Decisions             → A2 (typ=2, lane "D")
   - Metrics / status      → A3 (typ=3, lane "S")
   - Risks / threats       → A4 (typ=4, lane "R")
   - Invariants / gates    → A5 (typ=5, lane "G")
   - Inventory / topology  → A6 (typ=6, lane "I")
   - Action directives     → A7 (typ=7, lane "O")

2. BUILD body items per the archetype's positional shape (see grammar §5).
   Use only int, str, and arr. No null, no float, no object.

3. CANONICALIZE by sorting items per the archetype's ordering rule
   (grammar §7.2). A7 is the exception — preserve emission order.

4. BUILD header: [v=2, ctx, src, dst, typ, mid?, cid?, ts?, pri?].
   Omit trailing fields you don't need. You cannot skip middle fields.

5. SERIALIZE as JSON with no insignificant whitespace. UTF-8, no BOM,
   strings NFC-normalized, integers base-10 with no leading zeros.
```

## 2. Reader Algorithm

```text
1. PARSE the JSON. Expect a top-level array of length 2: [H, B].

2. REJECT forbidden types anywhere in the message tree:
   null, float, object, NaN, Infinity, bool.

3. VALIDATE header positionally:
   - H[0] (v)   MUST equal 2
   - H[1] (ctx) MUST match ctx_id regex
   - H[2..4]    src, dst, typ are ints
   - H[5..8]    mid/cid/ts/pri optional, type-checked if present

4. DISPATCH on typ:
   - Known typ (1..7) → run archetype handler (validate shape, ordering)
   - Unknown typ      → preserve verbatim for relay (forward-compat §8)

5. UPDATE state or EXECUTE actions literally. Do not infer beyond
   what the message says. Reject malformed messages — never repair.
```

## 3. Validation Pipeline

In order, fail-fast at each step:

| Stage | Checks |
|---|---|
| Lex | Valid JSON, UTF-8 |
| Type bans | No null / float / object / bool / NaN |
| Top shape | `[H, B]`, both arrays |
| Header | Length 5..9, positional types, `v == 2` |
| Body lane | `B[0]` matches lane tag for `typ` |
| Body items | Per-archetype shape (grammar §5) |
| Ordering | Per-archetype sort key (grammar §7.2) |
| Forward-compat | Unknown codes preserved, not rewritten |

See `validator/python/validate.py` for a working reference.

## 4. Common Mistakes

- **Using `null` for "field not set."** Trailing positional fields can be omitted; you cannot null them out.
- **Sorting A7 next-actions.** Don't. A7 preserves emission order — execution order matters.
- **Encoding metadata as a JSON object.** Use a KV-list `[[k,v],...]` sorted by `k` ascending.
- **Renumbering existing codes when extending.** Reserve `1000+` for vendor extensions; do not redefine codes below 1000.
- **Repairing malformed input.** Reject. The rulebook explicitly forbids repair.
- **Emitting prose status alongside the message.** Don't. Narrative is for humans, not relays.

## 5. Conformance

An implementation is conformant if it passes every case in `validator/corpus/` (positive cases must validate, negative cases must reject with the documented reason). The corpus is the binding behavioral definition — the prose spec is its rationale.
