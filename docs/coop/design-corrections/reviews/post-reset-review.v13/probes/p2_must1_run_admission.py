#!/usr/bin/env python
"""CB3-MUST-1 substantive probe: ladder membership at ACTUAL Run admission.

The blind finding was that the registry the identity contract names carries no
ladder, and that `rungs` -- a field-rule table that is {} for eight of thirteen
relations -- was being read as the ladder. The v13 source comment claims the old
`and row['rungs']` guard made the check vacuous for exactly those eight.

I do not take that on trust and I do not test the schema enum. Every case here
builds a real Run graph, mutates one fact (and its scope) and calls the real
close_run, so an "admits"/"refuses" result is a Run-admission result.

Positive controls are as important as the refusals: a probe where everything
refuses proves nothing.
"""
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(
    "/tmp/opensip-design-corrections/post-reset-review.v13/work/subject-copy"
    "/docs/coop/design-corrections")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


F = load("fx", HERE / "integration-fixtures.py")
M = F.M
C = F.C
REG = json.loads((HERE / "foundation/relation-payload-schemas.v2.json")
                 .read_text())["x-opensip-relation-registry"]
LADDERS = {k: v["ladder"] for k, v in REG["relations"].items()}
RUNGS = {k: v.get("rungs", {}) for k, v in REG["relations"].items()}
ALL_RUNGS = sorted({r for lad in LADDERS.values() for r in lad})

results = []


def record(case, expect, got, cause=None, detail=None):
    results.append({"case": case, "expected": expect, "observed": got,
                    "cause": cause, "detail": detail,
                    "agrees": expect == got})


def attempt(case, expect, mutate):
    """Build a fresh graph, apply `mutate`, close the Run for real."""
    try:
        run, objects, blobs = F.build(resolved=True, has_match=True)
    except Exception as exc:  # construction, not admission
        record(case, expect, "fixture-error", type(exc).__name__, str(exc)[:200])
        return
    try:
        mutate(run, objects, blobs)
    except Exception as exc:
        record(case, expect, "fixture-error", type(exc).__name__, str(exc)[:200])
        return
    try:
        rid = M.close_run(run, objects, blobs)
        record(case, expect, "admits", None, str(rid)[:40])
    except Exception as exc:
        record(case, expect, "refuses", str(exc)[:160], type(exc).__name__)


def set_fact_resolution(relation=None, resolution=None, scope_too=True):
    """Rewrite the single fact's relation/resolution and re-mint upward."""
    def go(run, objects, blobs):
        fid = next(k for k, (d, v) in objects.items() if d == "fact")
        fact = dict(objects[fid][1])
        if relation is not None:
            fact["relation"] = relation
        if resolution is not None:
            fact["resolution"] = resolution
        F.rekey(objects, fid, fact, run)
        if scope_too:
            sid = next((k for k, (d, v) in objects.items()
                        if d == "subject-scope"), None)
            if sid is not None:
                scope = dict(objects[sid][1])
                if relation is not None:
                    scope["relation"] = relation
                if resolution is not None:
                    scope["resolution"] = resolution
                F.rekey(objects, sid, scope, run)
    return go


def main():
    # --- Positive control: the unmodified graph closes. ------------------
    attempt("control/unmodified-graph-closes", "admits", lambda r, o, b: None)

    # --- Positive control: the fact's own weakest rung. -------------------
    attempt("control/references@syntactic-name-match", "admits",
            set_fact_resolution(resolution="syntactic-name-match"))

    # --- The empty-table bypass, relation by relation. -------------------
    # For each of the EIGHT relations whose `rungs` field-rule table is {},
    # try a rung that belongs to a DIFFERENT relation's ladder. Under the old
    # `and row['rungs']` guard every one of these would have been admitted.
    empty_table = sorted(k for k, v in RUNGS.items() if not v)
    for rel in empty_table:
        own = set(LADDERS[rel])
        foreign = next(r for r in ALL_RUNGS if r not in own)
        attempt(f"empty-table-bypass/{rel}@{foreign}(foreign)", "refuses",
                set_fact_resolution(relation=rel, resolution=foreign))

    # --- Cross-relation rungs for the FIVE relations that do have tables. -
    for rel in sorted(k for k, v in RUNGS.items() if v):
        own = set(LADDERS[rel])
        foreign = next(r for r in ALL_RUNGS if r not in own)
        attempt(f"cross-relation/{rel}@{foreign}(foreign)", "refuses",
                set_fact_resolution(relation=rel, resolution=foreign))

    # --- The exact counterexample the source comment names. --------------
    attempt("named-counterexample/declares@resolved-callee", "refuses",
            set_fact_resolution(relation="declares",
                                resolution="resolved-callee"))

    # --- A rung that is in NO ladder at all. ------------------------------
    attempt("unknown-rung/references@not-a-rung", "refuses",
            set_fact_resolution(resolution="not-a-rung"))

    # --- An unknown relation entirely. ------------------------------------
    attempt("unknown-relation/no-such-relation@syntactic", "refuses",
            set_fact_resolution(relation="no-such-relation",
                                resolution="syntactic"))

    # --- `syntactic` is shared by three relations: it must still be
    # refused for a relation that does NOT list it, proving membership is
    # per-relation and not against the flat vocabulary. -------------------
    attempt("flat-vocabulary-insufficient/references@syntactic", "refuses",
            set_fact_resolution(resolution="syntactic"))
    attempt("flat-vocabulary-insufficient/clones@syntactic", "refuses",
            set_fact_resolution(relation="clones", resolution="syntactic"))

    # --- Per-rung required/forbidden field rules must survive. ------------
    def drop_payload_field(field):
        def go(run, objects, blobs):
            fid = next(k for k, (d, v) in objects.items() if d == "fact")
            fact = dict(objects[fid][1])
            payload = C.parse(blobs[fact["payloadDigest"]])
            payload.pop(field, None)
            fact["payloadDigest"] = F.put_blob(blobs, payload)
            F.rekey(objects, fid, fact, run)
        return go

    def add_payload_field(field, value):
        def go(run, objects, blobs):
            fid = next(k for k, (d, v) in objects.items() if d == "fact")
            fact = dict(objects[fid][1])
            payload = C.parse(blobs[fact["payloadDigest"]])
            payload[field] = value
            fact["payloadDigest"] = F.put_blob(blobs, payload)
            F.rekey(objects, fid, fact, run)
        return go

    ref_rungs = RUNGS.get("references", {})
    req = ref_rungs.get("resolved-binding", {}).get("required", [])
    forb = ref_rungs.get("syntactic-name-match", {}).get("forbidden", [])
    results.append({"case": "meta/references-rung-field-rules",
                    "expected": None, "observed": None, "agrees": True,
                    "detail": json.dumps(ref_rungs)})
    for f in req:
        attempt(f"rung-field-rule/required-{f}-dropped", "refuses",
                drop_payload_field(f))
    for f in forb:
        def combo(field=f):
            a = set_fact_resolution(resolution="syntactic-name-match")
            b = add_payload_field(field, "symbol:foo")

            def go(run, objects, blobs):
                a(run, objects, blobs)
                b(run, objects, blobs)
            return go
        attempt(f"rung-field-rule/forbidden-{f}-present-at-weak-rung",
                "refuses", combo())

    # --- Cross-universe law: source/target universes. ---------------------
    def break_universe(which):
        def go(run, objects, blobs):
            fid = next(k for k, (d, v) in objects.items() if d == "fact")
            fact = dict(objects[fid][1])
            fact[which] = "0" * 64
            F.rekey(objects, fid, fact, run)
        return go

    for which in ("sourceUniverse", "targetUniverse"):
        attempt(f"universe/unregistered-{which}", "refuses",
                break_universe(which))

    ok = [r for r in results if r["agrees"]]
    bad = [r for r in results if not r["agrees"]]
    summary = {
        "total": len(results),
        "agreeing": len(ok),
        "disagreeing": len(bad),
        "emptyTableRelations": empty_table,
        "ladders": LADDERS,
        "results": results,
    }
    print(json.dumps(summary, indent=2, sort_keys=False))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
