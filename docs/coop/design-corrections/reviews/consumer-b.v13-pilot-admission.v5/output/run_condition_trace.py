#!/usr/bin/env python3
"""Exact required-occurrences MINUS executed-occurrences.

Key is (document, pointer, instance, field). No (condition,instance) fallback.
Document identity is the kit-relative path. Schema $id aliases are explicit and
narrow. One field's comparison cannot discharge another field or document.
Process exits 1 if any required occurrence is missing.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v13-pilot-admission.v5/output")
sys.path.insert(0, str(OUT))

from helpers import admit_graph, closure, condtrace, kit_schemas  # noqa: E402
from helpers.store import load_export  # noqa: E402

# Explicit, narrow document-identity aliases. $id of a selected schema document
# is the same document as its kit path. Never alias across documents.
DOCUMENT_ALIASES: dict[str, str] = {}
for sid, p in kit_schemas.SCHEMA_PATHS.items():
    posix = p.as_posix()
    rel = posix.split("/subject/", 1)[-1] if "/subject/" in posix else posix
    DOCUMENT_ALIASES[sid] = rel
    DOCUMENT_ALIASES[rel] = rel
    DOCUMENT_ALIASES[posix] = rel


def norm_ptr(p: str) -> str:
    s = (p or "").replace("~1", "/").rstrip("/")
    if s.startswith("#"):
        s = s[1:]
    if not s.startswith("/"):
        s = "/" + s if s else "/"
    return s if s != "/" else "/"


def norm_doc(d: str | None) -> str:
    if not d:
        return ""
    d = str(d).replace("\\", "/")
    if "/subject/" in d:
        d = d.split("/subject/", 1)[-1]
    return DOCUMENT_ALIASES.get(d, d)


def norm_field(f: str | None) -> str:
    s = str(f or "/").strip()
    if s in ("", "/"):
        return "/"
    return s.rstrip("/")


def occ_key(o: dict) -> tuple[str, str, str, str]:
    doc = o.get("document") or o.get("kitPath") or o.get("schemaId") or ""
    return (norm_doc(doc), norm_ptr(o.get("condition") or o.get("pointer") or ""), str(o.get("instance")), norm_field(o.get("field")))


def main():
    st = load_export(json.loads((OUT / "runs" / "ts.store.json").read_text()))
    condtrace.reset()
    try:
        admit_graph.admit_store(st)
        admit_ok = True
        admit_err = None
    except Exception as e:
        admit_ok = False
        admit_err = str(e)[:500]
    try:
        cl = closure.close_run(st)
        close_ok = True
        close_err = None
    except Exception as e:
        cl = None
        close_ok = False
        close_err = str(e)[:800]
    traces = condtrace.snapshot()
    (OUT / "executed-condition-trace.json").write_text(
        json.dumps(
            {
                "standing": "Traces emitted at comparison sites during admit_store+close_run. Each row carries owning document, pointer, instance, field.",
                "admitOk": admit_ok,
                "admitError": admit_err,
                "closeOk": close_ok,
                "closeError": close_err,
                "traceCount": len(traces),
                "traces": traces,
            },
            indent=2,
        )
        + "\n"
    )
    req = json.loads((OUT / "required-occurrences.json").read_text())["occurrences"]
    executed = {occ_key(t) for t in traces}
    missing = []
    for o in req:
        k = occ_key(o)
        if k not in executed:
            missing.append({**o, "exactKey": list(k)})
    weak_missing = []
    weak_ci = {(norm_ptr(t.get("condition")), str(t.get("instance"))) for t in traces}
    for o in req:
        if (norm_ptr(o.get("condition")), str(o.get("instance"))) not in weak_ci:
            weak_missing.append(o)
    report = {
        "standing": "Exact (document, pointer, instance, field). Weak (pointer, instance) retained for comparison; it is not the checkpoint.",
        "requiredCount": len(req),
        "traceCount": len(traces),
        "missingCount": len(missing),
        "open": missing,
        "weakPointerInstanceMissingCount": len(weak_missing),
        "v3WeakMatcherClaimedMissing": 0,
        "admitOk": admit_ok,
        "closeOk": close_ok,
        "closeError": close_err,
        "documentAliases": {k: v for k, v in DOCUMENT_ALIASES.items() if k.startswith("urn:") or k.startswith("opensip.")},
        "fieldAliases": {"empty-or-slash": "/"},
    }
    (OUT / "coverage-difference.json").write_text(json.dumps(report, indent=2) + "\n")
    print("admit", admit_ok, "close", close_ok, close_err)
    print("traces", len(traces), "required", len(req), "exact-missing", len(missing), "weak-ci-missing", len(weak_missing))
    from collections import Counter
    c = Counter()
    for m in missing:
        c["/".join(norm_ptr(m["condition"]).strip("/").split("/")[:4])] += 1
    for k, n in c.most_common(20):
        print(f"  {n:4d} {k}")
    if missing:
        (OUT / "inventory" / "v4-exact-matching-first.json").write_text(json.dumps(report, indent=2) + "\n")
    return 0 if close_ok and admit_ok and not missing else 1


if __name__ == "__main__":
    sys.exit(main())
