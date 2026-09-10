#!/usr/bin/env python3
"""Fresh-process admit+close+complete-proof replay for every claimed complete Run."""
from __future__ import annotations

import json
import sys
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v13-pilot-admission.v7/output")
sys.path.insert(0, str(OUT))

from helpers import admit_graph, closure, store  # noqa: E402
from replay_export import derive_proof_from_store, recompute_identities  # noqa: E402


def dump(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True, default=str) + "\n")


def one(name: str) -> dict:
    path = OUT / "runs" / f"{name}.store.json"
    st = store.load_export(json.loads(path.read_text()))
    report = {"name": name, "export": str(path), "freshProcess": True, "objectCount": len(st.objects), "blobCount": len(st.blobs)}
    report["schemaAdmission"] = admit_graph.admit_store(st)
    report["closure"] = closure.close_run(st)
    ident = recompute_identities(st)
    report["identities"] = ident
    derived = derive_proof_from_store(st)
    report["proofCompareFresh"] = derived["comparison"]
    report["derivedVerdict"] = derived["derived"]["verdict"]
    report["claimedVerdict"] = derived["claimed"]["verdict"]
    report["ok"] = bool(ident.get("ok") and not derived["comparison"].get("refused") and report["schemaAdmission"].get("admitted") and report["closure"].get("closed"))
    dump(OUT / "runs" / f"{name}.from-scratch.json", report)
    dump(OUT / "pilot" / f"{name}-fresh-replay.json", report)
    return report


def main() -> int:
    names = sys.argv[1:] or ["ts", "rust", "rust-partial", "syntax-code", "syntax-data"]
    rc = 0
    summary = []
    for name in names:
        r = one(name)
        print(name, "ok", r["ok"], "verdict", r.get("derivedVerdict"), flush=True)
        summary.append({"name": name, "ok": r["ok"], "runId": (r.get("closure") or {}).get("runId")})
        if not r["ok"]:
            rc = 4
    dump(OUT / "pilot" / "fresh-replay-all.json", summary)
    return rc


if __name__ == "__main__":
    sys.exit(main())
