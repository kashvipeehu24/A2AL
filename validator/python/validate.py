"""A2AL/2.0 reference validator.

Reads one A2AL message as JSON from stdin (or a file path argument)
and exits 0 if valid, 1 with a reason on stderr if invalid.

This is a reference implementation tracking the prose specification at
specs/A2A-Grammar.md. The conformance test corpus at validator/corpus/
is the binding behavioral definition; this file is one realization.

Status: WIP. Will evolve alongside the spec.
"""

from __future__ import annotations

import json
import re
import sys

VERSION = 2

LANE_TAGS = {1: "Δ", 2: "D", 3: "S", 4: "R", 5: "G", 6: "I", 7: "O"}

CTX_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")


class A2ALError(Exception):
    """Raised on any spec violation. Readers MUST reject, not repair."""


def validate(msg) -> None:
    """Validate a parsed A2AL message. Raises A2ALError on failure."""
    if not isinstance(msg, list) or len(msg) != 2:
        raise A2ALError("MSG must be a 2-element array [H, B]")
    H, B = msg
    _reject_forbidden_types(msg, "MSG")
    _validate_header(H)
    typ = H[4]
    _validate_body(B, typ)


def _reject_forbidden_types(node, path: str) -> None:
    """Recursively reject null, bool, float, dict (grammar §1.2)."""
    if node is None:
        raise A2ALError(f"null forbidden at {path}")
    if isinstance(node, bool):
        raise A2ALError(f"bool forbidden at {path}")
    if isinstance(node, float):
        raise A2ALError(f"float forbidden at {path}")
    if isinstance(node, dict):
        raise A2ALError(f"object forbidden at {path}")
    if isinstance(node, list):
        for i, child in enumerate(node):
            _reject_forbidden_types(child, f"{path}[{i}]")


def _validate_header(H) -> None:
    if not isinstance(H, list):
        raise A2ALError("header must be array")
    if not 5 <= len(H) <= 9:
        raise A2ALError(f"header length {len(H)} not in [5, 9]")
    v, ctx, src, dst, typ = H[0], H[1], H[2], H[3], H[4]
    if not (isinstance(v, int) and v == VERSION):
        raise A2ALError(f"v MUST equal {VERSION}, got {v!r}")
    if not (isinstance(ctx, str) and CTX_RE.match(ctx)):
        raise A2ALError(f"ctx must match {CTX_RE.pattern!r}, got {ctx!r}")
    for name, val in (("src", src), ("dst", dst), ("typ", typ)):
        if not isinstance(val, int):
            raise A2ALError(f"{name} must be int, got {type(val).__name__}")
    if typ < 1:
        raise A2ALError(f"typ must be >= 1, got {typ}")


def _validate_body(B, typ: int) -> None:
    if not isinstance(B, list) or not B:
        raise A2ALError("body must be a non-empty array")
    expected_lane = LANE_TAGS.get(typ)
    if expected_lane is None:
        # Unknown future archetype — preserve verbatim, do not reject (§8).
        return
    if B[0] != expected_lane:
        raise A2ALError(
            f"body lane {B[0]!r} does not match typ={typ} (expected {expected_lane!r})"
        )
    items = B[1:]
    {1: _a1, 2: _a2, 3: _a3, 4: _a4, 5: _a5, 6: _a6, 7: _a7}[typ](items)


# A1 Scope Delta: ΔITEM = [op, etype, id, meta?], sorted by (op, etype, id) asc.
def _a1(items) -> None:
    keys = []
    for it in items:
        if not isinstance(it, list) or len(it) < 3:
            raise A2ALError("A1 ΔITEM needs at least [op, etype, id]")
        op, etype, eid = it[0], it[1], it[2]
        if not isinstance(op, int):
            raise A2ALError("A1 op must be int")
        if not isinstance(etype, int):
            raise A2ALError("A1 etype must be int")
        if not isinstance(eid, str):
            raise A2ALError("A1 id must be str")
        keys.append((op, etype, eid))
    if keys != sorted(keys):
        raise A2ALError("A1 ΔITEMs not sorted ascending by (op, etype, id)")


# A2 Decision: DPAIR = [dkey, dval], sorted by dkey asc.
def _a2(items) -> None:
    keys = []
    for it in items:
        if not isinstance(it, list) or len(it) != 2:
            raise A2ALError("A2 DPAIR must be [dkey, dval]")
        if not isinstance(it[0], int):
            raise A2ALError("A2 dkey must be int")
        keys.append(it[0])
    if keys != sorted(keys):
        raise A2ALError("A2 DPAIRs not sorted by dkey ascending")


# A3 Status: MET = [mkey, mval], sorted by mkey asc.
def _a3(items) -> None:
    keys = []
    for it in items:
        if not isinstance(it, list) or len(it) != 2:
            raise A2ALError("A3 MET must be [mkey, mval]")
        if not isinstance(it[0], int):
            raise A2ALError("A3 mkey must be int")
        keys.append(it[0])
    if keys != sorted(keys):
        raise A2ALError("A3 METs not sorted by mkey ascending")


# A4 Risk: RISK = [sev, vec, impact, action, refs?], sort by (sev desc, vec asc).
def _a4(items) -> None:
    pairs = []
    for it in items:
        if not isinstance(it, list) or len(it) < 4:
            raise A2ALError("A4 RISK needs [sev, vec, impact, action]")
        sev, vec = it[0], it[1]
        if not isinstance(sev, int) or not 0 <= sev <= 4:
            raise A2ALError(f"A4 sev out of range 0..4: {sev!r}")
        pairs.append((sev, vec))
    if pairs != sorted(pairs, key=lambda p: (-p[0], p[1])):
        raise A2ALError("A4 RISKs not sorted by (sev desc, vec asc)")


# A5 Gates: GATE = [scope, invariant, test?], sort by (scope, invariant) asc.
def _a5(items) -> None:
    keys = []
    for it in items:
        if not isinstance(it, list) or len(it) < 2:
            raise A2ALError("A5 GATE needs [scope, invariant]")
        if not isinstance(it[0], str) or not isinstance(it[1], str):
            raise A2ALError("A5 scope and invariant must be str")
        keys.append((it[0], it[1]))
    if keys != sorted(keys):
        raise A2ALError("A5 GATEs not sorted by (scope, invariant)")


# A6 Inventory: ITEM = [kind, id, KV*], sort by (kind, id); KV by k asc.
def _a6(items) -> None:
    item_keys = []
    for it in items:
        if not isinstance(it, list) or len(it) < 2:
            raise A2ALError("A6 ITEM needs [kind, id, KV*]")
        kind, eid = it[0], it[1]
        if not isinstance(kind, int):
            raise A2ALError("A6 kind must be int")
        if not isinstance(eid, str):
            raise A2ALError("A6 id must be str")
        kv_keys = []
        for kv in it[2:]:
            if not isinstance(kv, list) or len(kv) != 2:
                raise A2ALError(f"A6 KV must be [k, v] in {eid!r}")
            if not isinstance(kv[0], int):
                raise A2ALError(f"A6 KV key must be int in {eid!r}")
            kv_keys.append(kv[0])
        if kv_keys != sorted(kv_keys):
            raise A2ALError(f"A6 KVs not sorted by k for {eid!r}")
        item_keys.append((kind, eid))
    if item_keys != sorted(item_keys):
        raise A2ALError("A6 ITEMs not sorted by (kind, id)")


# A7 Next Actions: OP = [actor, verb, target, params?]. ORDER PRESERVED.
def _a7(items) -> None:
    for it in items:
        if not isinstance(it, list) or len(it) < 3:
            raise A2ALError("A7 OP needs [actor, verb, target]")
        if not isinstance(it[0], (int, str)):
            raise A2ALError("A7 actor must be int or str")
        if not isinstance(it[1], (int, str)):
            raise A2ALError("A7 verb must be int or str")
        if not isinstance(it[2], (str, list)):
            raise A2ALError("A7 target must be str or arr")


def _main() -> int:
    raw = open(sys.argv[1]).read() if len(sys.argv) > 1 else sys.stdin.read()
    msg = json.loads(raw)
    try:
        validate(msg)
    except A2ALError as e:
        print(f"INVALID: {e}", file=sys.stderr)
        return 1
    print("VALID")
    return 0


if __name__ == "__main__":
    sys.exit(_main())
