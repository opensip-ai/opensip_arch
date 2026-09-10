#!/usr/bin/env python3
"""Rebuild the TypeScript pilot Run after kit-selector construction fixes.

Preserves original-first-pass bytes. Does not re-export other Runs.
"""
from __future__ import annotations

import json
import sys
import traceback
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v13-continuation.v1/output")
sys.path.insert(0, str(OUT))

from helpers import admit_graph, closure, runs, store  # noqa: E402


def dump(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True, default=str) + "\n")


def main() -> int:
    original = OUT / "pilot" / "original-first-pass" / "ts.store.json"
    if not original.exists():
        print("MISSING original-first-pass store; refuse to overwrite")
        return 2
    g = runs.build_ts_run()
    export = g["store"].export()
    store_path = OUT / "runs" / "ts.store.json"
    dump(store_path, export)
    dump(OUT / "runs" / "ts.replay.json", g["replay"])
    dump(OUT / "pilot" / "ts-corrected.store.json", export)

    st = store.load_export(export)
    report = {
        "store": str(store_path),
        "originalPreserved": str(original),
        "objectCount": len(st.objects),
        "blobCount": len(st.blobs),
        "runId": g["store"].meta.get("runId"),
        "planId": g["store"].meta.get("planId"),
        "proofId": g["store"].meta.get("proofId"),
    }
    try:
        adm = admit_graph.admit_store(st)
        report["schemaAdmission"] = adm
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
        dump(OUT / "pilot" / "ts-corrected-admission-failure.json", report)
        print("SCHEMA_REFUSED", report["schemaAdmission"].get("firstRefusal"), report["schemaAdmission"].get("path"))
        print(str(report["schemaAdmission"].get("message", ""))[:4000])
        return 1
    try:
        cl = closure.close_run(st)
        report["closure"] = cl
    except Exception as e:
        report["closure"] = {
            "closed": False,
            "firstRefusal": getattr(e, "firstRefusal", type(e).__name__),
            "code": getattr(e, "code", type(e).__name__),
            "message": str(e),
            "traceback": traceback.format_exc(),
        }
        dump(OUT / "pilot" / "ts-corrected-closure-failure.json", report)
        print("CLOSURE_REFUSED", report["closure"].get("message", "")[:4000])
        return 2
    dump(OUT / "pilot" / "ts-corrected-admission.json", report)
    dump(OUT / "runs" / "ts.closure.json", cl)
    print("PILOT_TS_REBUILD_ADMIT_CLOSE_PASS", report["runId"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
