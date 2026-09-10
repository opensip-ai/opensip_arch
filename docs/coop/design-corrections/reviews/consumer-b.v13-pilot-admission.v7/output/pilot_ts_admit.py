#!/usr/bin/env python3
"""Pilot: admit the TypeScript Run store. Preserve original failure bytes."""
from __future__ import annotations

import json
import sys
import traceback
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v13-pilot-admission.v7/output")
sys.path.insert(0, str(OUT))

from helpers import admit, admit_graph, closure, store  # noqa: E402


def main() -> int:
    path = OUT / "runs" / "ts.store.json"
    doc = json.loads(path.read_text())
    st = store.load_export(doc)
    report = {"store": str(path), "objectCount": len(st.objects), "blobCount": len(st.blobs)}
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
        (OUT / "pilot" / "ts-original-admission-failure.json").parent.mkdir(parents=True, exist_ok=True)
        (OUT / "pilot" / "ts-original-admission-failure.json").write_text(json.dumps(report, indent=2) + "\n")
        fails = report["schemaAdmission"]
        (OUT / "pilot").mkdir(parents=True, exist_ok=True)
        (OUT / "pilot" / "ts-original-admission-failure.json").write_text(json.dumps(report, indent=2) + "\n")
        print("FIRST_REFUSAL", fails.get("firstRefusal"), fails.get("path"))
        print(fails.get("message", "")[:2000])
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
        (OUT / "pilot").mkdir(parents=True, exist_ok=True)
        (OUT / "pilot" / "ts-original-closure-failure.json").write_text(json.dumps(report, indent=2) + "\n")
        print(json.dumps(report["closure"], indent=2)[:4000])
        return 2
    (OUT / "pilot").mkdir(parents=True, exist_ok=True)
    (OUT / "pilot" / "ts-original-admission-pass.json").write_text(json.dumps(report, indent=2) + "\n")
    print("PILOT ORIGINAL ADMISSION+CLOSURE PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
