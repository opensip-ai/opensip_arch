#!/usr/bin/env python3
"""Complete-Run semantic negative: structurally admitted, semantically refused.

Mutate a finding field that is derived from the retained program (severity),
remint dependent identities, admit the graph as well-formed, then independent
complete replay must refuse. Not a missing-record prerequisite refusal.
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v13-pilot-admission.v4/output")
sys.path.insert(0, str(OUT))

from helpers import admit_graph, canonical, evaluator, h, order, store  # noqa: E402
from helpers.store import load_export  # noqa: E402


def main() -> int:
    st = load_export(json.loads((OUT / "runs" / "ts.store.json").read_text()))
    admit_graph.admit_store(st)
    fid = next(i for i in st.objects if i.startswith("finding3:"))
    finding = dict(st.objects[fid])
    orig_sev = finding["severity"]
    finding["severity"] = "note" if orig_sev != "note" else "warning"
    # remint finding
    new_fid = st.put_canonical_record("finding", finding)
    run_id = next(i for i in st.objects if i.startswith("run3:"))
    run = dict(st.objects[run_id])
    evid = dict(st.objects[run["evidenceId"]])
    proof_id = evid["proofBundleId"]
    proof = dict(st.objects[proof_id])
    proof["findingIds"] = order.cset([new_fid if x == fid else x for x in proof.get("findingIds") or []])
    for rr in proof.get("ruleResults") or []:
        rr["findingIds"] = order.cset([new_fid if x == fid else x for x in rr.get("findingIds") or []])
    # drop old proof object so uniqueness of prefix is 1
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

    structural = {"admitted": False}
    try:
        adm = admit_graph.admit_store(st)
        structural = {"admitted": True, "records": len(adm.get("records") or [])}
    except Exception as e:
        structural = {"admitted": False, "error": str(e)[:500], "firstRefusal": getattr(e, "firstRefusal", type(e).__name__)}

    semantic = {"ran": False}
    if structural.get("admitted"):
        replay = evaluator.replay_from_retained(st)
        semantic = {
            "ran": True,
            "proofEqual": replay["comparison"].get("equal"),
            "refused": replay["comparison"].get("refused"),
            "outputMismatches": replay.get("outputMismatches") or [],
            "claimedDigest": replay["comparison"].get("claimedDigest"),
            "derivedDigest": replay["comparison"].get("derivedDigest"),
            "diffs": [d.get("field") for d in (replay["comparison"].get("diffs") or [])],
        }

    ok = bool(structural.get("admitted")) and bool(semantic.get("refused"))
    report = {
        "standing": "Complete-Run semantic negative. Structural admit must pass; independent complete replay must refuse.",
        "mutation": f"finding.severity {orig_sev} -> {finding['severity']}",
        "oldFinding": fid,
        "newFinding": new_fid,
        "newRun": new_run,
        "structuralAdmission": structural,
        "semanticReplay": semantic,
        "ok": ok,
        "notPrerequisiteStructuralRefusal": bool(structural.get("admitted")),
    }
    (OUT / "inventory" / "semantic-negative.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in ("ok", "mutation", "structuralAdmission", "semanticReplay")}, indent=2, default=str))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
