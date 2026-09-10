#!/usr/bin/env python3
"""Native-evidence prose vs every retained native instance, including no-fact Coverage.

Schema-keyword inventory is not this account. Applicability is derived from the
actual relation/rung/context/universe and field values using published owners.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v13-pilot-admission.v7/output")
sys.path.insert(0, str(OUT))

from helpers import closure, condtrace, kit_schemas  # noqa: E402
from helpers.store import load_export  # noqa: E402
from helpers.evaluator import _load_c  # noqa: E402


def main() -> int:
    st = load_export(json.loads((OUT / "runs" / "ts.store.json").read_text()))
    condtrace.reset()
    run_id = st.meta.get("runId")
    struct = closure.structural_admit(st, run_id)
    traces = list(condtrace.snapshot())
    native_docs = (
        "native-evidence.md",
        "native-evidence.schemas.v2.json",
        "relation-payload-schemas.v2.json",
    )
    native_traces = [
        t
        for t in traces
        if any(d in str(t.get("document") or "") or str(t.get("condition") or "").startswith("native-evidence") for d in native_docs)
        or str(t.get("condition") or "").startswith("/x-opensip-relation-registry")
        or str(t.get("condition") or "").startswith("/x-opensip-grammar-capability-registry")
        or str(t.get("condition") or "").startswith("/x-opensip-config-node-kind-law")
        or str(t.get("condition") or "").startswith("/x-opensip-digest-domains")
    ]

    rel = kit_schemas.relation_schema()["x-opensip-relation-registry"]["relations"]
    pairs = []
    present = {}
    coverage_instances = []
    for i, o in st.objects.items():
        if not i.startswith("coverage2:"):
            continue
        p = _load_c(st, o["payloadDigest"])
        e = p.get("entry") or {}
        k = p.get("key") or {}
        pair = (k.get("relation") or e.get("relation"), k.get("resolution") or e.get("resolution"))
        present.setdefault(pair, []).append(i)
        scope = st.objects.get(o.get("scopeId")) or {}
        facts_for = [
            fid
            for fid, f in st.objects.items()
            if fid.startswith("fact2:")
            and f.get("relation") == pair[0]
            and f.get("resolution") == pair[1]
        ]
        coverage_instances.append(
            {
                "id": i,
                "relation": pair[0],
                "rung": pair[1],
                "factCount": len(facts_for),
                "factIds": facts_for,
                "subjectCount": len(scope.get("subjects") or []),
                "coverage": e.get("coverage"),
                "state": (e.get("resolutionCompleteness") or {}).get("state"),
                "attempted": (e.get("resolutionCompleteness") or {}).get("attempted"),
                "examinedExhaustive": (e.get("resolutionCompleteness") or {}).get("examinedExhaustive"),
                "unresolvedEdgeCount": (e.get("resolutionCompleteness") or {}).get("unresolvedEdgeCount"),
                "commitment": k.get("subjectScopeCommitment"),
                "scopeId": o.get("scopeId"),
            }
        )

    for name, row in rel.items():
        for rung in row.get("ladder") or []:
            key = (name, rung)
            insts = present.get(key) or []
            rec = {
                "relation": name,
                "rung": rung,
                "resolved": key in closure.RESOLVED_RUNGS,
                "rc1Expect": "resolved-never-not-applicable" if key in closure.RESOLVED_RUNGS else "non-resolved-not-applicable",
                "instances": insts,
                "applicable": bool(insts),
            }
            if not insts:
                rec["inapplicableOperands"] = {
                    "reason": "no CoverageResultV3 for this registered pair in the selected TS graph",
                    "relation": name,
                    "rung": rung,
                    "ladder": row.get("ladder"),
                    "selectedPlanRequested": "matrix cell may still be inapplicable-vcs or weaker-rung not produced",
                }
            pairs.append(rec)

    facts = []
    for i, o in st.objects.items():
        if not i.startswith("fact2:"):
            continue
        facts.append(
            {
                "id": i,
                "relation": o.get("relation"),
                "resolution": o.get("resolution"),
                "sourceUniverse": o.get("sourceUniverse"),
                "anchorCount": len(o.get("anchors") or []),
                "payloadDigest": o.get("payloadDigest"),
            }
        )

    natives = []
    for i, o in st.objects.items():
        if not i.startswith("sha256:") or not isinstance(o, dict):
            continue
        kind = None
        if o.get("languageMode") and "toolchain" in o and "compilerName" in (o.get("toolchain") or {}):
            kind = "native.context.typescript.v2"
        elif o.get("tsconfigGraphHash"):
            kind = "native.semantic-universe.typescript.v2"
        elif o.get("grammarBundle"):
            kind = "native.context.syntax.v2"
        elif o.get("selectedGrammarIds") is not None:
            kind = "native.semantic-universe.syntax.v2"
        elif o.get("crateRootPaths") is not None:
            kind = "native.semantic-universe.rust.v2"
        elif o.get("targetTriple"):
            kind = "native.context.rust.v2"
        if kind:
            natives.append({"id": i, "domain": kind, "keys": sorted(o.keys())})

    account = {
        "standing": (
            "Registered relation/rung pairs from relation-payload-schemas.v2.json; "
            "RC-0/RC-1/RC-2/RC-4/RC-5/RC-6 and §4.1a/§4.5 from native-evidence.md; "
            "grammar-capability-registry applicability from actual universe domain. "
            "Traces are executed comparisons from structural_admit, not family labels."
        ),
        "structuralFunction": "closure.structural_admit",
        "structuralRunId": struct["runId"],
        "registeredPairs": len(pairs),
        "pairsWithInstance": sum(1 for p in pairs if p["applicable"]),
        "pairsWithoutInstance": sum(1 for p in pairs if not p["applicable"]),
        "coverageInstances": coverage_instances,
        "factInstances": facts,
        "nativeContextAndUniverse": natives,
        "pairs": pairs,
        "nativeTraceCount": len(native_traces),
        "nativeTraces": native_traces,
        "grammarCapability": {
            "selector": "native/native-evidence.schemas.v2.json#/x-opensip-grammar-capability-registry",
            "applicable": any(n["domain"].endswith("syntax.v2") for n in natives),
            "operands": {
                "universeDomainsPresent": sorted({n["domain"] for n in natives}),
                "reason": "grammar gate binds facts/scopes under a syntax universe; this selected TS graph retains typescript-v2",
            },
        },
    }
    (OUT / "inventory" / "native-prose-account.json").write_text(json.dumps(account, indent=2) + "\n")
    print(
        "pairs",
        len(pairs),
        "with-instance",
        sum(1 for p in pairs if p["applicable"]),
        "coverages",
        len(coverage_instances),
        "facts",
        len(facts),
        "nativeTraces",
        len(native_traces),
        "run",
        struct["runId"],
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
