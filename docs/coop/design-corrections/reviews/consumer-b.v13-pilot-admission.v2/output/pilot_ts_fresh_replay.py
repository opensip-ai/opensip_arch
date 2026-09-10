#!/usr/bin/env python3
"""Fresh-process reload of the corrected TS export: admit, close, derive, compare.

Must be invoked as a separate Python process from rebuild.
"""
from __future__ import annotations

import json
import sys
import traceback
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v13-pilot-admission.v2/output")
sys.path.insert(0, str(OUT))

from helpers import admit_graph, closure, store  # noqa: E402
from replay_export import derive_proof_from_store, recompute_identities  # noqa: E402


def dump(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True, default=str) + "\n")


def main() -> int:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else OUT / "runs" / "ts.store.json")
    doc = json.loads(path.read_text())
    st = store.load_export(doc)
    report = {
        "export": str(path),
        "freshProcess": True,
        "objectCount": len(st.objects),
        "blobCount": len(st.blobs),
    }
    try:
        report["schemaAdmission"] = admit_graph.admit_store(st)
    except Exception as e:
        report["schemaAdmission"] = {
            "admitted": False,
            "firstRefusal": getattr(e, "firstRefusal", type(e).__name__),
            "code": getattr(e, "code", type(e).__name__),
            "path": getattr(e, "path", ""),
            "message": str(e),
            "failures": getattr(e, "failures", []),
            "traceback": traceback.format_exc(),
        }
        dump(OUT / "pilot" / "ts-fresh-replay-failure.json", report)
        print("FRESH_ADMIT_REFUSED", report["schemaAdmission"].get("message", "")[:4000])
        return 1
    try:
        report["closure"] = closure.close_run(st)
    except Exception as e:
        report["closure"] = {
            "closed": False,
            "firstRefusal": getattr(e, "firstRefusal", type(e).__name__),
            "code": getattr(e, "code", type(e).__name__),
            "message": str(e),
            "traceback": traceback.format_exc(),
        }
        dump(OUT / "pilot" / "ts-fresh-replay-failure.json", report)
        print("FRESH_CLOSURE_REFUSED", report["closure"].get("message", "")[:4000])
        return 2
    ident = recompute_identities(st)
    report["identities"] = ident
    derived = derive_proof_from_store(st)
    report["proofCompareFresh"] = derived["comparison"]
    report["derivedVerdict"] = derived["derived"]["verdict"]
    report["claimedVerdict"] = derived["claimed"]["verdict"]
    report["source"] = "retained program/evidence in export, not saved replay JSON"
    dump(OUT / "pilot" / "ts-fresh-replay.json", report)
    dump(OUT / "runs" / "ts.from-scratch.json", report)
    print(json.dumps({k: report[k] for k in ("export", "freshProcess", "derivedVerdict", "claimedVerdict") if k in report}, indent=2))
    print("IDENTITIES_OK", ident.get("ok"), "PROOF_REFUSED", derived["comparison"].get("refused"))
    if not ident.get("ok"):
        return 3
    if derived["comparison"].get("refused"):
        return 4
    print("PILOT_TS_FRESH_REPLAY_PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
