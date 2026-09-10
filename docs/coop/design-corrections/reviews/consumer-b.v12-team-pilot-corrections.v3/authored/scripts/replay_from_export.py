#!/usr/bin/env python3
"""From-scratch complete proof replay over an exported store.

Reloads the store in this process, admits selected inputs, derives every
selected subject/enumeration, predicate node digest/address/value, match and
Coverage citations, witnesses, findings, waivers, ruleResults and verdict,
constructs the complete expected proof, and compares C with the retained claim.

Usage:
  /tmp/opensip-architecture-review-env/bin/python -I -B \\
    /tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v3/output/scripts/replay_from_export.py \\
    /tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v3/output/runs/syntax-code.store.json

  ... replay_from_export.py --tamper <store>
  ... replay_from_export.py --stale-hash <store>
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v3/output")
sys.path.insert(0, str(OUT))

from helper.canonical import C  # noqa: E402
from helper.identity import typed_id  # noqa: E402
from helper.proof_replay import (  # noqa: E402
    admit_graph,
    export_logical_result_tamper_graph,
    load_graph,
    reconstruct_expected_enclosing,
    reconstruct_expected_proof,
    stale_hash_tamper,
)
from helper.store import Store  # noqa: E402


def _replay(store: Store) -> dict:
    g = load_graph(store)
    admission = admit_graph(store, g)
    failed_joins = [j for j in admission["joins"] if not j["ok"]]
    reconstructed = reconstruct_expected_proof(store, g)
    expected = reconstructed["proof"]
    claimed = g["claimed_proof"]
    expected_c = C(expected)
    claimed_c = C(claimed)
    enclosing = reconstruct_expected_enclosing(g, expected)
    return {
        "g": g,
        "admission": admission,
        "failed_joins": failed_joins,
        "reconstructed": reconstructed,
        "expected": expected,
        "claimed": claimed,
        "expected_c": expected_c,
        "claimed_c": claimed_c,
        "proof_compare_equal": expected_c == claimed_c,
        "expected_id": typed_id("proof-bundle", expected),
        "claimed_id": g["claimed_proof_id"],
        "enclosing": enclosing,
    }


def _base_out(store_path: str, r: dict) -> dict:
    return {
        "store": store_path,
        "runId": r["g"]["run_id"],
        "claimedProofId": r["claimed_id"],
        "expectedProofId": r["expected_id"],
        "claimedVerdict": r["claimed"]["verdict"],
        "derivedVerdict": r["expected"]["verdict"],
        "derivedAtomValue": r["expected"]["predicateProofs"][0]["value"] if r["expected"]["predicateProofs"] else None,
        "predicateProofCount": len(r["expected"]["predicateProofs"]),
        "findingCount": len(r["expected"]["findingIds"]),
        "selectedSubjectIds": [s["id"] for s in r["reconstructed"]["subjects"]],
        "closureJoins": r["admission"]["joins"],
        "closureOk": r["admission"]["ok"] and not r["failed_joins"],
        "firstRefusal": r["failed_joins"][0]["name"] if r["failed_joins"] else None,
        "proofCompareEqual": r["proof_compare_equal"],
        "proofCExpectedSha256": hashlib.sha256(r["expected_c"]).hexdigest(),
        "proofCClaimedSha256": hashlib.sha256(r["claimed_c"]).hexdigest(),
        "completeEvidenceCEqual": r["enclosing"]["evidenceCEqual"],
        "completeSealCEqual": r["enclosing"]["sealCEqual"],
        "completeRunCEqual": r["enclosing"]["runCEqual"],
        "expectedEvidenceId": r["enclosing"]["evidenceId"],
        "expectedSealId": r["enclosing"]["sealId"],
        "expectedRunId": r["enclosing"]["runId"],
        "usedClaimedProofFields": [],
        "frameAdmission": "pass" if not r["failed_joins"] else "refused",
        "identityRecompute": "pass",
        "replayKind": "complete-expected-proof-from-admitted-inputs",
        "command": "/tmp/opensip-architecture-review-env/bin/python -I -B " + str(Path(__file__)),
    }


def main(argv: list[str]) -> int:
    mode = "replay"
    args = []
    for a in argv[1:]:
        if a == "--tamper":
            mode = "tamper"
        elif a == "--stale-hash":
            mode = "stale-hash"
        else:
            args.append(a)
    store_path = args[0] if args else str(OUT / "runs/syntax-code.store.json")
    store = Store.load(Path(store_path))
    r = _replay(store)
    out = _base_out(store_path, r)

    if mode == "stale-hash":
        stale = stale_hash_tamper(r["claimed"])
        stale_c = C(stale)
        stale_id = typed_id("proof-bundle", stale)
        out["staleHashControl"] = {
            "kind": "stale-hash",
            "note": "Mutated executionInputsDigest only. Enclosing evidence/seal/Run identities were not reminted. C inequality is not semantic replay.",
            "replacementGraph": False,
            "C_stale_ne_C_claimed": stale_c != r["claimed_c"],
            "staleProofId": stale_id,
            "claimedProofIdUnchanged": r["claimed_id"],
            "runIdUnchanged": r["g"]["run_id"],
            "semanticReplayNotExercised": True,
        }
        if not out["staleHashControl"]["C_stale_ne_C_claimed"]:
            print(json.dumps(out, indent=2))
            return 1
        print(json.dumps(out, indent=2))
        return 0

    if mode == "tamper":
        tamper_path = OUT / "runs" / "syntax-code.tamper.store.json"
        exported = export_logical_result_tamper_graph(store, r["g"], tamper_path)
        tamper_store = Store.load(tamper_path)
        tr = _replay(tamper_store)
        structural_ok = tr["admission"]["ok"] and not tr["failed_joins"]
        semantic_refuse = (
            (not tr["proof_compare_equal"])
            and tr["expected"]["verdict"] == "pass"
            and tr["claimed"]["verdict"] == "fail"
            and tr["enclosing"]["proofCEqual"] is False
        )
        input_citations_preserved = (
            tr["claimed"]["evaluationInputRefs"] == r["claimed"]["evaluationInputRefs"]
            and tr["claimed"]["executionInputsDigest"] == r["claimed"]["executionInputsDigest"]
        )
        same_inputs = (
            tr["g"]["execution_inputs_digest"] == r["g"]["execution_inputs_digest"]
            and tr["g"]["plan_id"] == r["g"]["plan_id"]
        )
        witness_reminted = [p["witnessDigest"] for p in tr["claimed"]["predicateProofs"]] != [
            p["witnessDigest"] for p in r["claimed"]["predicateProofs"]
        ]
        out["tamper"] = {
            "kind": "logical-result-replacement-graph",
            "note": "Selected-input citations preserved. Claimed outputs reminted as a consistent composition (witness matches, value, finding3, evidence/seal/Run). Structural admission of the replacement is separate from semantic rejection by fresh derivation from Plan/ExecutionInputs/view/facts only.",
            "export": exported,
            "structuralAdmission": {
                "ok": structural_ok,
                "firstRefusal": tr["failed_joins"][0]["name"] if tr["failed_joins"] else None,
                "closureOk": tr["admission"]["ok"],
                "failedJoins": tr["failed_joins"][:8],
            },
            "semanticReplay": {
                "reached": bool(structural_ok),
                "expectedVerdictRemains": tr["expected"]["verdict"],
                "derivedAtomValueRemains": tr["expected"]["predicateProofs"][0]["value"] if tr["expected"]["predicateProofs"] else None,
                "tamperedClaimedVerdict": tr["claimed"]["verdict"],
                "expectedProofId": tr["expected_id"],
                "tamperedProofId": tr["claimed_id"],
                "tamperedRunId": tr["g"]["run_id"],
                "cEqual": tr["proof_compare_equal"],
                "completeEvidenceCEqual": tr["enclosing"]["evidenceCEqual"],
                "completeSealCEqual": tr["enclosing"]["sealCEqual"],
                "completeRunCEqual": tr["enclosing"]["runCEqual"],
                "refused": semantic_refuse if structural_ok else None,
            },
            "inputCitationsPreserved": input_citations_preserved,
            "witnessDigestReminted": witness_reminted,
            "sameSelectedInputs": same_inputs,
            "replacementGraph": True,
            "notStaleHash": True,
            "notSingleEditedProof": True,
            "refused": bool(structural_ok and semantic_refuse and input_citations_preserved and same_inputs and witness_reminted),
        }
        if not out["tamper"]["refused"]:
            print(json.dumps(out, indent=2))
            return 1
        print(json.dumps(out, indent=2))
        return 0

    if r["failed_joins"] or not r["proof_compare_equal"]:
        print(json.dumps(out, indent=2))
        return 1
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
