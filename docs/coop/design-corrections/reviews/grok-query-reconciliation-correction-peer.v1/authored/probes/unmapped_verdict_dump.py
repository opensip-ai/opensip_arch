"""Dump unmapped-file Run predicate values vs verdict. Not a pin run."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/grok-query-reconciliation-correction-peer.v1/output")
FOUND = OUT / "disposable" / "work" / "docs" / "coop" / "design-corrections" / "foundation"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


S = load("u_fix", FOUND / "evaluator_semantic_fixture.v3.py")
replay = load("u_sem", FOUND / "check-semantic-replay.v3.py")
C = replay.C

IMPORTS_EXISTS = {
    "op": "exists",
    "relation": "imports",
    "minResolution": "resolved-target",
    "endpoint": "target",
    "filters": [],
}
IMPORTS_NONE = {
    "op": "none",
    "relation": "imports",
    "minResolution": "resolved-target",
    "endpoint": "target",
    "filters": [],
}


def dump(atom, occupancy, subject_kind):
    g = S.build_ts_semantic_graph(
        atom=atom,
        subject_kind=subject_kind,
        has_declares=False,
        has_references_fact=False,
        second_partition=False,
        imports_occupancy=occupancy,
    )
    run, objects, blobs, actual = replay.close_positive(g)
    proof = objects[objects[run["evaluationSealId"]][1]["proofBundleId"]][1]
    pop = g["inputs"]["population"]
    rows = []
    counts = {"true": 0, "false": 0, "indeterminate": 0, "other": 0}
    for p in proof["predicateProofs"]:
        if p["predicateId"] != "p":
            continue
        item = pop.get(p["subjectId"], {})
        w = C.parse(blobs[p["witnessDigest"]])
        rows.append({
            "subjectId": p["subjectId"],
            "kind": item.get("kind"),
            "native": (item.get("row") or {}).get("nativeSubjectId"),
            "path": (item.get("row") or {}).get("path"),
            "value": p["value"],
            "matchingFactIds": w.get("matchingFactIds"),
            "uncertainFactIds": w.get("uncertainFactIds"),
        })
        counts[p["value"] if p["value"] in counts else "other"] += 1
    return {
        "occupancy": occupancy,
        "op": atom["op"],
        "subject_kind": subject_kind,
        "verdict": actual["verdict"],
        "findingCount": actual["findingCount"],
        "predicateCount": len(proof["predicateProofs"]),
        "valueCounts": counts,
        "predicates": rows,
        "executionDeficiencies": proof.get("executionDeficiencies"),
    }


report = {
    "unmapped-exists-file": dump(IMPORTS_EXISTS, "unmapped-file", "file"),
    "unmapped-none-file": dump(IMPORTS_NONE, "unmapped-file", "file"),
    "mapped-exists-file": dump(IMPORTS_EXISTS, "mapped-file", "file"),
    "exact-exists-symbol": dump(IMPORTS_EXISTS, "exact-id-symbol", "symbol"),
}
(OUT / "receipts" / "unmapped-verdict-dump.json").write_text(json.dumps(report, indent=2) + "\n")
summary = {k: {sk: report[k][sk] for sk in ("verdict", "findingCount", "valueCounts", "executionDeficiencies")} for k in report}
print(json.dumps(summary, indent=2))
