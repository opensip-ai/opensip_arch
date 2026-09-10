#!/usr/bin/env python3
"""Bounded controls for newly implemented native/prose comparisons.

Each control mutates one operand of a retained instance and runs the SAME
admit_coverage_result_v3 / admit_native_context function. An inapplicable
example is not reported as a malformed-input refusal. The pre-correction
full-graph RC-1 refusal is preserved separately.
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v13-pilot-admission.v6/output")
sys.path.insert(0, str(OUT))

from helpers import closure  # noqa: E402
from helpers.store import load_export  # noqa: E402
from helpers.evaluator import _load_c  # noqa: E402


def dump(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True, default=str) + "\n")


def main() -> int:
    st = load_export(json.loads((OUT / "runs" / "ts.store.json").read_text()))
    results = []

    # Control 1: RC-6 — complete coverage with examinedExhaustive=false
    cov_id = None
    payload = None
    rec = None
    for i, o in st.objects.items():
        if not i.startswith("coverage2:"):
            continue
        p = _load_c(st, o["payloadDigest"])
        e = p.get("entry") or {}
        if e.get("coverage") == "complete" and (e.get("resolutionCompleteness") or {}).get("examinedExhaustive") is True:
            cov_id, rec, payload = i, o, p
            break
    mutated = copy.deepcopy(payload)
    mutated["entry"]["resolutionCompleteness"]["examinedExhaustive"] = False
    errs = closure.admit_coverage_result_v3(st, cov_id + "#rc6-mut", rec, mutated)
    rc6 = any(str(e).startswith("RC6_") for e in errs)
    results.append(
        {
            "id": "CTRL-RC6-COMPLETE-NOT-EXHAUSTIVE",
            "selector": "native-evidence.md#/4.3 RC-6",
            "boundary": "coverage=complete AND examinedExhaustive=false on a retained CoverageResultV3",
            "instance": cov_id,
            "errors": errs,
            "refused": rc6,
            "ok": rc6,
            "notMalformedInput": True,
            "notInapplicable": True,
        }
    )

    # Control 2: RC-1 — non-resolved rung claiming state=complete
    cov_id = rec = payload = None
    for i, o in st.objects.items():
        if not i.startswith("coverage2:"):
            continue
        p = _load_c(st, o["payloadDigest"])
        e = p.get("entry") or {}
        k = p.get("key") or {}
        pair = (k.get("relation") or e.get("relation"), k.get("resolution") or e.get("resolution"))
        if pair not in closure.RESOLVED_RUNGS and (e.get("resolutionCompleteness") or {}).get("state") == "not-applicable":
            cov_id, rec, payload = i, o, p
            break
    mutated = copy.deepcopy(payload)
    mutated["entry"]["resolutionCompleteness"]["state"] = "complete"
    mutated["entry"]["resolutionCompleteness"]["attempted"] = True
    errs = closure.admit_coverage_result_v3(st, cov_id + "#rc1-mut", rec, mutated)
    rc1 = any("RC1_NON_RESOLVED" in str(e) for e in errs)
    results.append(
        {
            "id": "CTRL-RC1-NON-RESOLVED-COMPLETE",
            "selector": "native-evidence.md#/4.3 RC-1",
            "boundary": "non-resolved registered pair with state=complete attempted=true",
            "instance": cov_id,
            "pair": {
                "relation": (payload.get("key") or {}).get("relation"),
                "resolution": (payload.get("key") or {}).get("resolution"),
            },
            "errors": errs,
            "refused": rc1,
            "ok": rc1,
            "notMalformedInput": True,
            "notInapplicable": True,
        }
    )

    # Control 3: §4.1a commitment mismatch
    cov_id = rec = payload = None
    for i, o in st.objects.items():
        if i.startswith("coverage2:"):
            cov_id, rec, payload = i, o, _load_c(st, o["payloadDigest"])
            break
    mutated = copy.deepcopy(payload)
    mutated["key"]["subjectScopeCommitment"] = "sha256:" + ("0" * 64)
    errs = closure.admit_coverage_result_v3(st, cov_id + "#41a-mut", rec, mutated)
    c41 = any("subject-scope-commitment-mismatch" in str(e) for e in errs)
    results.append(
        {
            "id": "CTRL-41A-COMMITMENT-MISMATCH",
            "selector": "native-evidence.md#/4.1a subjectScopeCommitment",
            "boundary": "key.subjectScopeCommitment is not sha256-text of the bound scope2",
            "instance": cov_id,
            "errors": errs,
            "refused": c41,
            "ok": c41,
            "notMalformedInput": True,
            "notInapplicable": True,
        }
    )

    # Control 4: libSelection component not retained
    ctx_id = ctx = None
    for i, o in st.objects.items():
        if i.startswith("sha256:") and isinstance(o, dict) and "compilerName" in (o.get("toolchain") or {}):
            ctx_id, ctx = i, o
            break
    snap = next(o for i, o in st.objects.items() if i.startswith("snapshot2:"))
    mutated_ctx = copy.deepcopy(ctx)
    mutated_ctx["toolchain"]["libSelection"] = ["dom"]
    # keep honoredOptions in agreement so the failure is the component-membership join
    mutated_ctx["configProjection"]["honoredOptions"]["lib"] = ["dom"]
    errs = closure.admit_native_context(mutated_ctx, "native.context.typescript.v2", snap, st, instance_id=ctx_id + "#lib-mut")
    lib = any("lib-not-retained" in str(e) for e in errs)
    results.append(
        {
            "id": "CTRL-LIB-COMPONENT-NOT-RETAINED",
            "selector": "native-evidence.md#/2.4 libSelection-component-membership",
            "boundary": "libSelection name whose component(n)=lib.dom.d.ts is absent from standardLibraryComponentDigests",
            "instance": ctx_id,
            "errors": errs,
            "refused": lib,
            "ok": lib,
            "notMalformedInput": True,
            "notInapplicable": True,
        }
    )

    # Control 5: inapplicable grammar gate is NOT a refusal
    g_errs = closure.check_grammar_capability_registry(st)
    results.append(
        {
            "id": "CTRL-GRAMMAR-INAPPLICABLE-NOT-REFUSAL",
            "selector": "native/native-evidence.schemas.v2.json#/x-opensip-grammar-capability-registry",
            "boundary": "typescript-v2 universe: grammar gate does not apply",
            "errors": g_errs,
            "refused": bool(g_errs),
            "ok": not g_errs,
            "notMalformedInput": True,
            "inapplicableRecorded": True,
            "note": "Inapplicability is recorded with universe-domain operands; it is not a malformed-input refusal.",
        }
    )

    ok = all(r.get("ok") for r in results)
    report = {
        "standing": "Bounded native/prose comparison controls against the SAME admit functions used by structural_admit.",
        "ok": ok,
        "fullGraphRc1FirstRefusal": "inventory/v5-first-rc1-structural-refusal.json",
        "controls": results,
    }
    dump(OUT / "inventory" / "native-prose-controls.json", report)
    print(json.dumps({"ok": ok, "ids": [(r["id"], r["ok"]) for r in results]}, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
