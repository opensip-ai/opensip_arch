#!/usr/bin/env python3
"""Rebuild remaining required Runs through owning-schema admission + closure.

Does not overwrite original-first-pass artifacts. TS already piloted.
"""
from __future__ import annotations

import json
import sys
import traceback
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v13-continuation.v2/output")
sys.path.insert(0, str(OUT))

from helpers import admit_graph, closure, runs, store  # noqa: E402


def dump(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True, default=str) + "\n")


BUILDERS = {
    "rust": runs.build_rust_run,
    "rust-partial": runs.build_rust_partial,
    "syntax-code": lambda: runs.build_syntax_run(data_document=False),
    "syntax-data": lambda: runs.build_syntax_run(data_document=True),
}


def process(name: str) -> dict:
    original = OUT / "pilot" / "original-first-pass" / f"{name}.store.json"
    g = BUILDERS[name]()
    export = g["store"].export()
    dump(OUT / "runs" / f"{name}.store.json", export)
    dump(OUT / "runs" / f"{name}.replay.json", g["replay"])
    st = store.load_export(export)
    report = {
        "name": name,
        "store": str(OUT / "runs" / f"{name}.store.json"),
        "originalPreserved": str(original) if original.exists() else None,
        "objectCount": len(st.objects),
        "blobCount": len(st.blobs),
        "runId": g["store"].meta.get("runId"),
        "planId": g["store"].meta.get("planId"),
        "proofId": g["store"].meta.get("proofId"),
        "verdict": (g.get("objects") or {}).get("proof", {}).get("verdict") or (g.get("replay") or {}).get("proof", {}).get("verdict"),
        "properties": g.get("properties") or {},
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
        dump(OUT / "pilot" / f"{name}-corrected-admission-failure.json", report)
        return report
    try:
        cl = closure.close_run(st)
        report["closure"] = cl
        dump(OUT / "runs" / f"{name}.closure.json", cl)
    except Exception as e:
        report["closure"] = {
            "closed": False,
            "firstRefusal": getattr(e, "firstRefusal", type(e).__name__),
            "code": getattr(e, "code", type(e).__name__),
            "message": str(e),
            "traceback": traceback.format_exc(),
        }
        dump(OUT / "pilot" / f"{name}-corrected-closure-failure.json", report)
        return report
    dump(OUT / "pilot" / f"{name}-corrected-admission.json", report)
    return report


def main() -> int:
    names = sys.argv[1:] or list(BUILDERS)
    rc = 0
    summary = []
    for name in names:
        print("BUILD", name, flush=True)
        report = process(name)
        admitted = (report.get("schemaAdmission") or {}).get("admitted")
        closed = (report.get("closure") or {}).get("closed")
        print("  admitted", admitted, "closed", closed, "runId", report.get("runId"), flush=True)
        if not admitted:
            print("  FIRST", (report.get("schemaAdmission") or {}).get("message", "")[:2000], flush=True)
            rc = 1
        elif not closed:
            print("  CLOSURE", (report.get("closure") or {}).get("message", "")[:2000], flush=True)
            rc = 2
        summary.append({"name": name, "admitted": admitted, "closed": closed, "runId": report.get("runId")})
    dump(OUT / "pilot" / "expand-runs-summary.json", summary)
    return rc


if __name__ == "__main__":
    sys.exit(main())
