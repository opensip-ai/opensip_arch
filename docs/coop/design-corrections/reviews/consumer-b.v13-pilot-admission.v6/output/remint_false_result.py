#!/usr/bin/env python3
"""Fully reminted false-result graph over the admitted TS Run.

Structural identities/joins still admit. Independent complete-proof derivation
rejects the altered claimed result.
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v13-pilot-admission.v6/output")
sys.path.insert(0, str(OUT))

from helpers import admit_graph, canonical, closure, evaluator, h, store  # noqa: E402
from replay_export import derive_proof_from_store, recompute_identities  # noqa: E402


def dump(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True, default=str) + "\n")


def remint_identity(st: store.Store, old_id: str, obj: dict, domain: str) -> str:
    new_id = h.h_id(domain, obj)
    if old_id in st.objects:
        del st.objects[old_id]
    st.objects[new_id] = obj
    cx = canonical.encode(obj)
    st.blobs[h.raw_sha256(cx)] = cx
    return new_id


def main() -> int:
    src = OUT / "runs" / "ts.store.json"
    doc = json.loads(src.read_text())
    st = store.load_export(doc)
    admit_graph.admit_store(st)
    closure.close_run(st)

    run_id, run = next((i, o) for i, o in st.objects.items() if i.startswith("run3:"))
    evid_id, evid = next((i, o) for i, o in st.objects.items() if i.startswith("evidence3:"))
    seal_id, seal = next((i, o) for i, o in st.objects.items() if i.startswith("seal3:"))
    proof_id, proof = next((i, o) for i, o in st.objects.items() if i.startswith("proof3:"))

    true_verdict = proof["verdict"]
    false_verdict = "pass" if true_verdict != "pass" else "fail"
    proof2 = copy.deepcopy(proof)
    proof2["verdict"] = false_verdict
    # keep predicateProofs/findingIds/identities of facts; only the sealed result is reminted false
    new_proof_id = remint_identity(st, proof_id, proof2, "proof-bundle")

    evid2 = copy.deepcopy(evid)
    evid2["proofBundleId"] = new_proof_id
    new_evid_id = remint_identity(st, evid_id, evid2, "semantic-evidence")

    seal2 = copy.deepcopy(seal)
    seal2["evidenceId"] = new_evid_id
    seal2["proofBundleId"] = new_proof_id
    seal2["verdict"] = false_verdict
    new_seal_id = remint_identity(st, seal_id, seal2, "evaluation-seal")

    run2 = copy.deepcopy(run)
    run2["evidenceId"] = new_evid_id
    run2["evaluationSealId"] = new_seal_id
    new_run_id = remint_identity(st, run_id, run2, "run")

    export = st.export()
    path = OUT / "runs" / "ts-false-result.store.json"
    dump(path, export)

    st2 = store.load_export(json.loads(path.read_text()))
    report = {
        "sourceRun": src.name,
        "trueVerdict": true_verdict,
        "claimedFalseVerdict": false_verdict,
        "reminted": {
            "runId": new_run_id,
            "proofId": new_proof_id,
            "evidenceId": new_evid_id,
            "sealId": new_seal_id,
        },
        "structuralFactsUnchanged": True,
    }
    try:
        report["schemaAdmission"] = admit_graph.admit_store(st2)
    except Exception as e:
        report["schemaAdmission"] = {"admitted": False, "message": str(e), "failures": getattr(e, "failures", [])}
        dump(OUT / "vectors" / "false-result-remint.json", report)
        print("STRUCTURAL_ADMIT_REFUSED", e)
        return 1
    try:
        report["closure"] = closure.close_run(st2)
    except Exception as e:
        msg = str(e)
        report["closure"] = {"closed": False, "message": msg, "code": getattr(e, "code", type(e).__name__)}
        report["replayRejectedAlteredResult"] = "REPLAY_PROOF_MISMATCH" in msg
        report["observation"] = (
            "Structural owning-schema admission passed. Public close_run complete replay "
            "refused the reminted claimed verdict (identity §4). That is the required negative."
        )
        dump(OUT / "vectors" / "false-result-remint.json", report)
        dump(OUT / "runs" / "ts-false-result.replay.json", report["closure"])
        print("FALSE_RESULT_REPLAY_REFUSED", report["replayRejectedAlteredResult"], msg[:400])
        return 0 if report["replayRejectedAlteredResult"] and report["schemaAdmission"].get("admitted") else 2
    ident = recompute_identities(st2)
    report["identities"] = ident
    derived = derive_proof_from_store(st2)
    report["proofCompareFresh"] = derived["comparison"]
    report["derivedVerdict"] = derived["derived"]["verdict"]
    report["claimedVerdict"] = derived["claimed"]["verdict"]
    report["replayRejectedAlteredResult"] = bool(derived["comparison"].get("refused"))
    report["observation"] = (
        "Structural identities and registry joins admitted on the reminted graph. "
        "Independent derivation from retained program/evidence produced the true complete proof, "
        "which does not equal the reminted claimed proof."
    )
    dump(OUT / "vectors" / "false-result-remint.json", report)
    dump(OUT / "runs" / "ts-false-result.replay.json", derived["comparison"])
    print(json.dumps({k: report[k] for k in ("trueVerdict", "claimedFalseVerdict", "derivedVerdict", "claimedVerdict", "replayRejectedAlteredResult") if k in report}, indent=2))
    if not ident.get("ok"):
        return 3
    if not report["schemaAdmission"].get("admitted"):
        return 4
    if not report["closure"].get("closed"):
        return 5
    if not report["replayRejectedAlteredResult"]:
        print("FALSE_RESULT_NOT_REJECTED")
        return 6
    if derived["derived"]["verdict"] != true_verdict:
        print("DERIVED_VERDICT_DRIFT")
        return 7
    print("FALSE_RESULT_REPLAY_REJECTED_AS_REQUIRED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
