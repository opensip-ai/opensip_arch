#!/usr/bin/env python3
"""From-scratch replay: reload exported store, recompute identities, re-derive proof.

  /tmp/opensip-architecture-review-env/bin/python -I -B \\
    /tmp/opensip-design-corrections/consumer-b.v13-pilot-admission.v4/output/replay_export.py \\
    /tmp/opensip-design-corrections/consumer-b.v13-pilot-admission.v4/output/runs/<id>.store.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v13-pilot-admission.v4/output")
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
    try:
        return json.loads(raw.decode("utf-8"))
    except Exception:
        _domain, cx = h.parse_h_frame(raw)
        return json.loads(cx.decode("utf-8"))


def derive_proof_from_store(st: store.Store) -> dict:
    """Recompute the complete proof from retained program + evidence only.

    Independent derivation: subjects come from retained inventories + policy,
    not from stored subject3/finding lists. Saved replay JSON is not an oracle.
    """
    result = evaluator.replay_from_retained(st)
    return {
        "derived": result["proof"],
        "claimed": result["claimed"],
        "comparison": result["comparison"],
        "replay": result["replay"],
        "subjectsDerived": result.get("subjects"),
        "outputMismatches": result.get("outputMismatches") or [],
        "source": result.get("source"),
    }


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
