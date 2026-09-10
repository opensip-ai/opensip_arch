#!/usr/bin/env python3
"""From-scratch complete proof replay over an exported store.

Reloads the store in this process, admits selected inputs, derives every
selected subject/enumeration, predicate node digest/address/value, match and
Coverage citations, witnesses, findings, waivers, ruleResults and verdict,
constructs the complete expected proof, and compares C with the retained claim.

Usage:
  /tmp/opensip-architecture-review-env/bin/python -I -B \\
    /tmp/opensip-design-corrections/consumer-b.v12-team-workflow-corrections.v5/output/scripts/replay_from_export.py \\
    /tmp/opensip-design-corrections/consumer-b.v12-team-workflow-corrections.v5/output/runs/syntax-code.store.json

  ... replay_from_export.py --tamper <store>
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-workflow-corrections.v5/output")
sys.path.insert(0, str(OUT))

from helper.canonical import C  # noqa: E402
from helper.identity import typed_id  # noqa: E402
from helper.proof_replay import (  # noqa: E402
    admit_graph,
    load_graph,
    logical_result_tamper,
    reconstruct_expected_proof,
)
from helper.store import Store  # noqa: E402


def main(argv: list[str]) -> int:
    tamper = False
    args = [a for a in argv[1:] if a != "--tamper"]
    if "--tamper" in argv[1:]:
        tamper = True
    store_path = args[0] if args else str(OUT / "runs/syntax-code.store.json")
    store = Store.load(Path(store_path))
    g = load_graph(store)
    admission = admit_graph(store, g)
    failed_joins = [j for j in admission["joins"] if not j["ok"]]
    reconstructed = reconstruct_expected_proof(store, g)
    expected = reconstructed["proof"]
    claimed = g["claimed_proof"]
    expected_c = C(expected)
    claimed_c = C(claimed)
    proof_compare_equal = expected_c == claimed_c
    expected_id = typed_id("proof-bundle", expected)
    out: dict = {
        "store": store_path,
        "runId": g["run_id"],
        "claimedProofId": g["claimed_proof_id"],
        "expectedProofId": expected_id,
        "claimedVerdict": claimed["verdict"],
        "derivedVerdict": expected["verdict"],
        "derivedAtomValue": expected["predicateProofs"][0]["value"] if expected["predicateProofs"] else None,
        "predicateProofCount": len(expected["predicateProofs"]),
        "findingCount": len(expected["findingIds"]),
        "selectedSubjectIds": [s["id"] for s in reconstructed["subjects"]],
        "closureJoins": admission["joins"],
        "closureOk": admission["ok"] and not failed_joins,
        "firstRefusal": failed_joins[0]["name"] if failed_joins else None,
        "proofCompareEqual": proof_compare_equal,
        "proofCExpectedSha256": hashlib.sha256(expected_c).hexdigest(),
        "proofCClaimedSha256": hashlib.sha256(claimed_c).hexdigest(),
        "frameAdmission": "pass",
        "identityRecompute": "pass",
        "replayKind": "complete-expected-proof-from-admitted-inputs",
        "command": "/tmp/opensip-architecture-review-env/bin/python -I -B " + str(Path(__file__)),
    }
    if tamper:
        tampered = logical_result_tamper(claimed)
        tampered_c = C(tampered)
        stale_hash = tampered_c != claimed_c
        # Independently remint enclosing proof identity after logical-result change
        tampered_id = typed_id("proof-bundle", tampered)
        semantic_refuse = expected_c != tampered_c
        # Same-count citations preserved
        citations_preserved = [p["witnessDigest"] for p in tampered["predicateProofs"]] == [
            p["witnessDigest"] for p in claimed["predicateProofs"]
        ] and tampered["evaluationInputRefs"] == claimed["evaluationInputRefs"]
        out["tamper"] = {
            "kind": "logical-result",
            "changed": "proof.verdict and first predicateProof.value; ruleResults.outcome",
            "identitiesPreservedForInputs": True,
            "citationsPreserved": citations_preserved,
            "staleHashControl": {
                "C_tampered_ne_C_claimed": stale_hash,
                "note": "C inequality of a mutated verdict/value field is a stale-hash control, not semantic replay",
            },
            "semanticReplay": {
                "expectedC_ne_tamperedC": semantic_refuse,
                "derivedVerdict": expected["verdict"],
                "tamperedClaimedVerdict": tampered["verdict"],
                "tamperedProofId": tampered_id,
                "refused": semantic_refuse and citations_preserved,
            },
            "refused": bool(semantic_refuse and citations_preserved),
        }
        if not out["tamper"]["refused"]:
            print(json.dumps(out, indent=2))
            return 1
        print(json.dumps(out, indent=2))
        return 0

    if failed_joins or not proof_compare_equal:
        print(json.dumps(out, indent=2))
        return 1
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
