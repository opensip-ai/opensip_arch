#!/usr/bin/env python3
"""Reminted semantic negative: SAME full structural function, then SAME semantic replay.

Exports exact object table + all blobs/frames. Schema-only admit is not structural.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v13-pilot-admission.v6/output")
sys.path.insert(0, str(OUT))

from helpers import closure, evaluator, order, store  # noqa: E402
from helpers.store import load_export  # noqa: E402


def dump(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True, default=str) + "\n")


def main() -> int:
    st = load_export(json.loads((OUT / "runs" / "ts.store.json").read_text()))
    run_id = st.meta["runId"]
    struct_pos = closure.structural_admit(st, run_id)

    fid = next(i for i in st.objects if i.startswith("finding3:"))
    finding = dict(st.objects[fid])
    orig_sev = finding["severity"]
    finding["severity"] = "note" if orig_sev != "note" else "warning"
    new_fid = st.put_canonical_record("finding", finding)
    run = dict(st.objects[run_id])
    evid = dict(st.objects[run["evidenceId"]])
    proof_id = evid["proofBundleId"]
    proof = dict(st.objects[proof_id])
    proof["findingIds"] = order.cset([new_fid if x == fid else x for x in proof.get("findingIds") or []])
    for rr in proof.get("ruleResults") or []:
        rr["findingIds"] = order.cset([new_fid if x == fid else x for x in rr.get("findingIds") or []])
    del st.objects[proof_id]
    new_proof_id = st.put_canonical_record("proof-bundle", proof)
    evid["findingIds"] = proof["findingIds"]
    evid["proofBundleId"] = new_proof_id
    del st.objects[run["evidenceId"]]
    new_evid = st.put_canonical_record("semantic-evidence", evid)
    seal_id = run["evaluationSealId"]
    seal = dict(st.objects[seal_id])
    seal["evidenceId"] = new_evid
    seal["proofBundleId"] = new_proof_id
    del st.objects[seal_id]
    new_seal = st.put_canonical_record("evaluation-seal", seal)
    run["evidenceId"] = new_evid
    run["evaluationSealId"] = new_seal
    del st.objects[run_id]
    new_run = st.put_canonical_record("run", run)
    st.meta["runId"] = new_run
    st.meta["proofId"] = new_proof_id

    export = st.export()
    dump(OUT / "runs" / "ts-semantic-negative.store.json", export)

    # fresh-process structural + semantic on the exported bytes
    st2 = load_export(json.loads((OUT / "runs" / "ts-semantic-negative.store.json").read_text()))
    structural = {"admitted": False}
    try:
        s = closure.structural_admit(st2, st2.meta.get("runId"))
        structural = {"admitted": True, "runId": s["runId"], "function": "closure.structural_admit"}
    except Exception as e:
        structural = {
            "admitted": False,
            "function": "closure.structural_admit",
            "code": getattr(e, "code", type(e).__name__),
            "message": str(e)[:800],
        }

    semantic = {"ran": False}
    if structural.get("admitted"):
        try:
            closure.semantic_replay(st2, st2.meta.get("runId"))
            semantic = {"ran": True, "refused": False, "function": "closure.semantic_replay"}
        except Exception as e:
            semantic = {
                "ran": True,
                "refused": True,
                "function": "closure.semantic_replay",
                "code": getattr(e, "code", type(e).__name__),
                "message": str(e)[:800],
            }

    ok = bool(structural.get("admitted")) and bool(semantic.get("refused"))
    report = {
        "standing": "Same structural_admit as positive; same semantic_replay. Exact export retained.",
        "positiveStructuralFunction": "closure.structural_admit",
        "mutation": f"finding.severity {orig_sev} -> {finding['severity']}",
        "export": str(OUT / "runs" / "ts-semantic-negative.store.json"),
        "objectCount": len(st2.objects),
        "blobCount": len(st2.blobs),
        "frameCount": len(st2.frames),
        "newRun": new_run,
        "structuralAdmission": structural,
        "semanticReplay": semantic,
        "ok": ok,
        "notPrerequisiteStructuralRefusal": bool(structural.get("admitted")),
        "positiveStructuralRunId": struct_pos.get("runId"),
    }
    dump(OUT / "inventory" / "semantic-negative.json", report)
    print(json.dumps({k: report[k] for k in ("ok", "mutation", "structuralAdmission", "semanticReplay", "objectCount", "blobCount")}, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
