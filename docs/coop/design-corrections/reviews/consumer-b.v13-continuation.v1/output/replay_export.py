#!/usr/bin/env python3
"""From-scratch replay: reload exported store, recompute identities, re-derive proof.

  /tmp/opensip-architecture-review-env/bin/python -I -B \\
    /tmp/opensip-design-corrections/consumer-b.v13-continuation.v1/output/replay_export.py \\
    /tmp/opensip-design-corrections/consumer-b.v13-continuation.v1/output/runs/<id>.store.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v13-continuation.v1/output")
sys.path.insert(0, str(OUT))

from helpers import admit_graph, canonical, closure, evaluator, h, store  # noqa: E402


def recompute_identities(st: store.Store) -> dict:
    results = []
    for ident, obj in st.objects.items():
        if not isinstance(ident, str) or ":" not in ident:
            continue
        prefix, digest = ident.split(":", 1)
        # map prefix back to domain
        inv = {v: k for k, v in h.PREFIX.items()}
        domain = inv.get(prefix)
        if not domain:
            if prefix == "sha256":
                continue
            results.append({"id": ident, "checked": False, "reason": "unknown-prefix"})
            continue
        recomputed = h.h_id(domain, obj)
        results.append({"id": ident, "recomputed": recomputed, "match": recomputed == ident, "domain": domain})
    mismatches = [r for r in results if r.get("match") is False]
    return {"checked": len(results), "mismatches": mismatches, "ok": not mismatches}


def _load_c(st: store.Store, digest: str):
    raw = st.require_blob(digest)
    return json.loads(raw.decode("utf-8"))


def derive_proof_from_store(st: store.Store) -> dict:
    """Recompute the complete proof from retained program + evidence only."""
    run = next(o for i, o in st.objects.items() if i.startswith("run3:"))
    plan = next(o for i, o in st.objects.items() if i.startswith("plan2:"))
    claimed_proof = next(o for i, o in st.objects.items() if i.startswith("proof3:"))
    policy = _load_c(st, plan["policyDigest"])
    ei = _load_c(st, claimed_proof["executionInputsDigest"])
    facts = []
    fact_ids = []
    for ident, rec in st.objects.items():
        if ident.startswith("fact2:"):
            payload = _load_c(st, rec["payloadDigest"])
            rec2 = dict(rec)
            rec2["_payload"] = payload
            rec2["id"] = ident
            facts.append(rec2)
            fact_ids.append(ident)
    coverages = []
    cov_ids = []
    for ident, rec in st.objects.items():
        if ident.startswith("coverage2:"):
            payload = _load_c(st, rec["payloadDigest"])
            rec2 = dict(rec)
            rec2["_payload"] = payload
            rec2["id"] = ident
            coverages.append(rec2)
            cov_ids.append(ident)
    lang_by_path = {}
    for digest, blob in st.blobs.items():
        try:
            rec = json.loads(blob.decode("utf-8"))
        except Exception:
            continue
        if isinstance(rec, dict) and rec.get("kind") in ("file", "symbol", "package") and "rows" in rec:
            for row in rec.get("rows") or []:
                if isinstance(row, dict) and "path" in row:
                    lang_by_path[row["path"]] = row.get("subjectLanguage") or lang_by_path.get(row["path"])
    subjects = []
    for ident, rec in st.objects.items():
        if ident.startswith("subject3:"):
            path = rec["nativeSubjectId"]
            subjects.append(
                {
                    "id": ident,
                    "path": path,
                    "kind": rec["kind"],
                    "language": lang_by_path.get(path) or "typescript",
                    "universe": rec["universe"],
                }
            )
    views = [o for i, o in st.objects.items() if i.startswith("view2:")]
    scope_ids = []
    for v in views:
        scope_ids.extend(v.get("scopeIds") or [])
    detector = plan["semanticClosures"][0]
    for ident, rec in st.objects.items():
        if ident.startswith("closure2:") and rec.get("kind") == "detector":
            detector = ident
            break
    replay = evaluator.compose_proof(
        {
            "policy": policy,
            "planId": claimed_proof["planId"],
            "executionPlanId": claimed_proof["executionPlanId"],
            "evaluatorClosure": claimed_proof["evaluatorClosure"],
            "executionInputs": ei,
            "facts": facts,
            "factIds": fact_ids,
            "coverages": coverages,
            "coverageIds": cov_ids,
            "subjects": subjects,
            "detectorClosure": detector,
            "scopeIds": scope_ids,
            "inventoryRefs": [r for r in ei.get("selectedRefs") or [] if r.get("domain") == "subject-inventory"],
        }
    )
    derived = replay["proof"]
    # finding ids are freshly minted; compare logical proof fields that must match
    # the retained claimed proof. Finding identity depends on detector closure and
    # evidence refs; we compare the retained claimed proof against a derived bundle
    # that uses the same subject/predicate values. Align findingIds from derived.
    cmp = evaluator.compare_proof(claimed_proof, derived)
    return {"derived": derived, "claimed": claimed_proof, "comparison": cmp, "replay": replay}


def main(path: str) -> int:
    doc = json.loads(Path(path).read_text())
    st = store.load_export(doc)
    try:
        adm = admit_graph.admit_store(st)
    except Exception as e:
        print(json.dumps({"export": path, "admitted": False, "error": str(e)}, indent=2))
        return 2
    try:
        cl = closure.close_run(st)
    except Exception as e:
        print(json.dumps({"export": path, "admitted": True, "closed": False, "error": str(e)}, indent=2))
        return 3
    ident = recompute_identities(st)
    derived = derive_proof_from_store(st)
    report = {
        "export": path,
        "identities": ident,
        "objectCount": len(st.objects),
        "blobCount": len(st.blobs),
        "schemaAdmission": {"admitted": True, "recordCount": len(adm.get("records") or [])},
        "closure": {"closed": True, "runId": cl.get("runId")},
        "freshDerivation": True,
        "source": "retained program/evidence in export, not saved replay JSON",
        "proofCompareFresh": derived["comparison"],
        "derivedVerdict": derived["derived"]["verdict"],
        "claimedVerdict": derived["claimed"]["verdict"],
    }
    print(json.dumps(report, indent=2))
    if not ident["ok"]:
        return 1
    if derived["comparison"]["refused"]:
        # still fail the process if complete bundle mismatches
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
