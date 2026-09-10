#!/usr/bin/env python
"""CB3-MUST-1 decisive probe: reach the ladder guard for the EIGHT relations
whose per-rung field-rule table is empty.

Attempt 1 (p2) was insufficient and I record why: swapping only `relation`
left the `references` payload in place, so those cases refused at
PAYLOAD_RECORD before the ladder check was ever evaluated. A refusal that never
reaches the guard under test is not evidence about that guard.

Here each case substitutes a VALID payload for the target relation, the correct
subjectKind, and a matching subject-scope, so admission genuinely arrives at the
ladder membership check. Each relation gets BOTH:
  * a positive control at its own (single) rung, which must ADMIT, and
  * a foreign rung from another relation's ladder, which must REFUSE with
    RELATION_RUNG_NOT_IN_LADDER specifically -- not some earlier cause.
Under the old `and row['rungs']` guard the foreign-rung case would have admitted.
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
M, C = F.M, F.C
REG = json.loads((HERE / "foundation/relation-payload-schemas.v2.json")
                 .read_text())["x-opensip-relation-registry"]
LADDERS = {k: v["ladder"] for k, v in REG["relations"].items()}
ALL_RUNGS = sorted({r for lad in LADDERS.values() for r in lad})

# Valid payloads for the four symbol-kind, snapshot-join-free relations.
SYMBOL_PAYLOADS = {
    # Attempt 3 correction: declarationKind/edgeKind are closed enums and my
    # first guesses ("const", "sequence") were not members, so those cases died
    # at PAYLOAD_RECORD instead of reaching the ladder guard.
    "declares": {"container": "symbol:m", "declared": "symbol:foo",
                 "declarationKind": "variable"},
    "literal": {"owner": "symbol:foo", "literalKind": "string",
                "valueText": "x"},
    "control-flow": {"from": "symbol:m", "to": "symbol:foo",
                     "edgeKind": "branch-true"},
    "reachability": {"origin": "symbol:m", "reachable": "symbol:foo"},
}

results = []


def run_case(case, relation, resolution, payload, subject_kind, subjects,
             expect, want_cause=None):
    try:
        run, objects, blobs = F.build(resolved=True, has_match=True)
        fid = next(k for k, (d, v) in objects.items() if d == "fact")
        fact = dict(objects[fid][1])
        fact["relation"] = relation
        fact["resolution"] = resolution
        # Attempt 2 correction: `subjectKind`/`subjects` are subject-scope
        # fields, not fact fields; the fact record is closed and refuses them.
        fact["payloadDigest"] = F.put_blob(blobs, payload)
        F.rekey(objects, fid, fact, run)
        sid = next((k for k, (d, v) in objects.items()
                    if d == "subject-scope"), None)
        if sid is not None:
            scope = dict(objects[sid][1])
            scope["relation"] = relation
            scope["resolution"] = resolution
            scope["subjects"] = subjects
            F.rekey(objects, sid, scope, run)
        # Moving the scope moves its commitment, so the Coverage payload and the
        # witness must be rebuilt over the CURRENT retained scope or the run
        # refuses for an unrelated (and misleading) reason.
        F.resync_coverage(objects, blobs, run)
        F.resync_witness(objects, blobs, run)
        F.resync_proof_refs(objects, blobs, run)
    except Exception as exc:
        results.append({"case": case, "expected": expect,
                        "observed": "fixture-error",
                        "cause": f"{type(exc).__name__}: {str(exc)[:160]}",
                        "reachedLadderGuard": False, "agrees": False})
        return
    try:
        rid = M.close_run(run, objects, blobs)
        obs, cause = "admits", None
    except Exception as exc:
        obs, cause = "refuses", str(exc)[:200]
    reached = bool(cause and cause.startswith("RELATION_RUNG_NOT_IN_LADDER"))
    agrees = (obs == expect)
    if expect == "refuses" and want_cause:
        agrees = agrees and bool(cause and cause.startswith(want_cause))
    results.append({"case": case, "expected": expect, "observed": obs,
                    "cause": cause, "wantCause": want_cause,
                    "reachedLadderGuard": reached, "agrees": agrees})


def main():
    for rel, payload in sorted(SYMBOL_PAYLOADS.items()):
        own = LADDERS[rel]
        assert len(own) == 1, rel
        rung = own[0]
        # Positive control at the relation's own rung.
        run_case(f"{rel}/positive-control@{rung}", rel, rung, payload,
                 "symbol", ["symbol:foo"], "admits")
        # Every foreign rung must refuse AT THE LADDER GUARD.
        for foreign in ALL_RUNGS:
            if foreign in own:
                continue
            run_case(f"{rel}/foreign@{foreign}", rel, foreign, payload,
                     "symbol", ["symbol:foo"], "refuses",
                     want_cause="RELATION_RUNG_NOT_IN_LADDER")

    controls = [r for r in results if "positive-control" in r["case"]]
    foreigns = [r for r in results if "/foreign@" in r["case"]]
    summary = {
        "relationsProbed": sorted(SYMBOL_PAYLOADS),
        "total": len(results),
        "agreeing": sum(1 for r in results if r["agrees"]),
        "disagreeing": [r for r in results if not r["agrees"]],
        "positiveControlsAdmitting": sum(
            1 for r in controls if r["observed"] == "admits"),
        "positiveControlCount": len(controls),
        "foreignRungCases": len(foreigns),
        "foreignRungRefusedAtLadderGuard": sum(
            1 for r in foreigns if r["reachedLadderGuard"]),
        "results": results,
    }
    print(json.dumps(summary, indent=2))
    return 0 if not summary["disagreeing"] else 1


if __name__ == "__main__":
    sys.exit(main())
