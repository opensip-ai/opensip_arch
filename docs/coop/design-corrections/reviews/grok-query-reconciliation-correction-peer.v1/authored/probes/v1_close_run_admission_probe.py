"""Seed-time V1 sidecar through derive/close_run vs helper catch.

Distinguishes TARGET_ATTRIBUTION_SCHEMA_VERSION admission from later
REFERENCE_IDENTITY on a mutated sealed proof. Helper-only results stay labeled.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import traceback
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/grok-query-reconciliation-correction-peer.v1/output")
FOUND = OUT / "disposable" / "work" / "docs" / "coop" / "design-corrections" / "foundation"
WORKF = OUT / "disposable" / "work" / "docs" / "coop" / "design-corrections" / "workflows"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


S = load("v1_fixture", FOUND / "evaluator_semantic_fixture.v3.py")
R = load("v1_replay", FOUND / "evaluator_replay_model.v3.py")
Q = load("v1_query", WORKF / "query_projection_model.v3.py")
AM = Q.atom_model()
C = R.M.C
replay = load("v1_check_semantic", FOUND / "check-semantic-replay.v3.py")

IMPORTS_EXISTS = {
    "op": "exists",
    "relation": "imports",
    "minResolution": "resolved-target",
    "endpoint": "target",
    "filters": [],
}
ROWS = []


def rec(cid, ok, **extra):
    row = {"id": cid, "ok": bool(ok)}
    row.update(extra)
    ROWS.append(row)
    return bool(ok)


def replace_sidecar(graph, mutate):
    g = copy.deepcopy(graph)
    objects, blobs = g["objects"], g["blobs"]
    refs = list(g["inputs"]["evaluationInputRefs"])
    new_refs = []
    replaced = 0
    for ref in refs:
        if ref.get("domain") != "target-attribution":
            new_refs.append(ref)
            continue
        sc = C.parse(blobs[ref["digest"]])
        mutated = mutate(dict(sc))
        raw = C.canonical(mutated)
        digest = hashlib.sha256(raw).hexdigest()
        blobs[digest] = raw
        new_refs.append({"domain": "target-attribution", "digest": digest})
        replaced += 1
    g["inputs"]["evaluationInputRefs"] = type(g["inputs"]["evaluationInputRefs"])(new_refs) if not isinstance(new_refs, list) else new_refs
    # evaluationInputRefs may be a cset
    try:
        g["inputs"]["evaluationInputRefs"] = R.E.cset(new_refs)
    except Exception:
        g["inputs"]["evaluationInputRefs"] = new_refs
    return g, replaced


def try_close(graph):
    try:
        run, objects, blobs, actual = replay.close_positive(graph)
        return {"kind": "ADMIT", "runId": actual.get("runId"), "verdict": actual.get("verdict")}
    except Exception as exc:
        return {
            "kind": type(exc).__name__,
            "msg": str(exc)[:500],
            "atom_key": getattr(exc, "key", None),
            "traceback_tail": traceback.format_exc()[-800:],
        }


def host_obs():
    return {"requestId": "req1_" + "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}


def main():
    base = S.build_ts_semantic_graph(
        atom=IMPORTS_EXISTS,
        subject_kind="file",
        has_declares=False,
        has_references_fact=False,
        second_partition=False,
        imports_occupancy="mapped-file",
    )
    good = try_close(base)
    rec("seed-v2-mapped-file-still-admits", good.get("kind") == "ADMIT", result=good)

    def to_v1_drop_eval(sc):
        sc = dict(sc)
        sc["schemaVersion"] = 1
        sc.pop("evaluationNativeId", None)
        return sc

    def to_v1_keep_eval(sc):
        sc = dict(sc)
        sc["schemaVersion"] = 1
        return sc

    g1, n1 = replace_sidecar(base, to_v1_drop_eval)
    rec("seed-v1-replaced-count", n1 >= 1, replaced=n1)
    r1 = try_close(g1)
    rec(
        "seed-v1-close-run-refuses",
        r1.get("kind") != "ADMIT",
        result=r1,
    )
    rec(
        "seed-v1-admission-key-is-schema-version-or-atom",
        r1.get("kind") != "ADMIT"
        and (
            r1.get("atom_key") == "TARGET_ATTRIBUTION_SCHEMA_VERSION"
            or "TARGET_ATTRIBUTION_SCHEMA_VERSION" in str(r1.get("msg"))
            or r1.get("kind") in ("AtomAdmissionError", "AdmissionError")
        ),
        result=r1,
    )

    g2, n2 = replace_sidecar(base, to_v1_keep_eval)
    rec("seed-wrong-v1-with-eval-id-replaced", n2 >= 1, replaced=n2)
    r2 = try_close(g2)
    rec(
        "seed-wrong-v1-with-leftover-eval-id-refuses",
        r2.get("kind") != "ADMIT",
        result=r2,
    )

    # Public execute_graph_query cannot be called on a non-admitted Run. Confirm derive refuses
    # before any neighbor success body.
    rec(
        "seed-v1-never-yields-closed-run-for-query",
        r1.get("kind") != "ADMIT" and r2.get("kind") != "ADMIT" and "runId" not in r1,
        v1=r1.get("kind"),
        wrong=r2.get("kind"),
    )

    # Helper still omits if occupancy_inputs are hand-fed V1 after a good close.
    run, objects, blobs, actual = replay.close_positive(base)
    proof = objects[objects[run["evaluationSealId"]][1]["proofBundleId"]][1]
    plan = objects[run["planId"]][1]
    occ = Q.occupancy_inputs_from_retained(proof, plan, objects, blobs)
    helper_inputs = copy.deepcopy(occ)
    for fid, sc in list(helper_inputs["targetAttributions"].items()):
        helper_inputs["targetAttributions"][fid] = to_v1_keep_eval(sc)
    evidence = objects[run["evidenceId"]][1]
    table = Q.projection_table()[("imports", "resolved-target")]
    projected, limits, _, _ = Q.collect_projected_edges(
        evidence.get("viewIds") or [], objects, blobs, table, helper_inputs
    )
    rec(
        "helper-wrong-v1-still-unprojectable-after-good-close",
        projected == []
        and any("TARGET_ATTRIBUTION_SCHEMA_VERSION" in str(x.get("note")) for x in limits),
        projectedCount=len(projected),
        limitations=limits,
        standing="helper-only; occupancy_inputs were mutated after close_run; not public execute_graph_query",
    )

    failed = [r for r in ROWS if not r["ok"]]
    report = {
        "standing": "seed-time V1 sidecar through derive/close_run vs helper catch; not pin suite",
        "passed": not failed,
        "count": len(ROWS),
        "failedCount": len(failed),
        "failed": failed,
        "checks": ROWS,
    }
    dest = OUT / "receipts" / "v1-close-run-admission.json"
    dest.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"passed": report["passed"], "count": report["count"], "failedCount": report["failedCount"], "failedIds": [r["id"] for r in failed], "rows": [{k: r[k] for k in ("id", "ok") if k in r} | {k: r[k] for k in r if k in ("result", "atom_key")} for r in ROWS]}, indent=2))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
