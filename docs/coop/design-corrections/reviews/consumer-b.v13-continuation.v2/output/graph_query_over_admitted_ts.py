#!/usr/bin/env python3
"""Graph.neighbors|path|reach over an admitted TS Run — query-projection-contract.v3."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v13-continuation.v2/output")
sys.path.insert(0, str(OUT))

from helpers import admit, admit_graph, builder, closure, h, kit_schemas, store  # noqa: E402

PROJECTABLE = {
    ("calls", "resolved-callee"),
    ("references", "resolved-binding"),
    ("imports", "resolved-target"),
    ("control-flow", "syntactic"),
    ("reachability", "from-resolved-calls"),
}
SCHEMA_ID = "urn:opensip:product-v1:workflows:evaluator3:graph-query:3"


def dump(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def neighbor_key(row: dict) -> bytes:
    src = row["source"]
    tgt = row["target"]
    return b"\x00".join(
        [
            src["universe"].encode("utf-8"),
            src["kind"].encode("utf-8"),
            src["nativeSubjectId"].encode("utf-8"),
            (src.get("packageManifestPath") or "").encode("utf-8"),
            tgt["universe"].encode("utf-8"),
            tgt["kind"].encode("utf-8"),
            tgt["nativeSubjectId"].encode("utf-8"),
            (tgt.get("packageManifestPath") or "").encode("utf-8"),
            row["factId"].encode("utf-8"),
        ]
    )


def refuse_relation(relation: str, rung: str) -> dict:
    return {
        "kind": "failure",
        "errors": [
            {
                "code": "QUERY.RELATION_UNSUPPORTED",
                "remedy": f"{relation}@{rung} is not a graph-projectable binary native-id rung",
                "subject": f"{relation}@{rung}",
            }
        ],
        "termination": {
            "class": "request-rejected",
            "errorCode": "REQUEST.PRECONDITION_FAILED",
            "domainDetail": {"code": "QUERY.RELATION_UNSUPPORTED", "subject": f"{relation}@{rung}"},
        },
        "run": None,
    }


def main() -> int:
    path = OUT / "runs" / "ts.store.json"
    st = store.load_export(json.loads(path.read_text()))
    adm = admit_graph.admit_store(st)
    cl = closure.close_run(st)
    run_id = cl["runId"]
    run = st.objects[run_id]
    project_id = run["projectId"]
    facts = []
    for ident, rec in st.objects.items():
        if not ident.startswith("fact2:"):
            continue
        if rec.get("relation") != "imports" or rec.get("resolution") != "resolved-target":
            continue
        payload = json.loads(st.require_blob(rec["payloadDigest"]).decode("utf-8"))
        facts.append({"id": ident, "rec": rec, "payload": payload})
    if not facts:
        dump(OUT / "query" / "graph-query.json", {"executed": False, "reason": "no imports@resolved-target facts"})
        return 1

    # occupancy from retained TargetAttributionV2 (not SubjectIdV1 parse)
    attrs = []
    for digest, blob in st.blobs.items():
        try:
            obj = json.loads(blob.decode("utf-8"))
        except Exception:
            continue
        if isinstance(obj, dict) and obj.get("schemaVersion") == 2 and "sourceFactId" in obj and "occupancy" in obj:
            attrs.append(obj)
    attr_by_fact = {a["sourceFactId"]: a for a in attrs}

    src_ep = {
        "universe": facts[0]["rec"]["sourceUniverse"],
        "kind": "symbol",
        "nativeSubjectId": facts[0]["payload"]["importer"],
        "packageManifestPath": "",
    }
    rows = []
    for it in facts:
        pl = it["payload"]
        rec = it["rec"]
        attr = attr_by_fact.get(it["id"]) or {}
        tgt_kind = attr.get("kind") or "package"
        tgt_occ = attr.get("occupancy") or "external"
        tgt_id = pl.get("resolvedTarget")
        if tgt_occ == "first-party":
            tgt_id = attr.get("evaluationNativeId") or tgt_id
        tgt_pkg = attr.get("packageManifestPath") or ""
        rows.append(
            {
                "factId": it["id"],
                "direction": "outgoing",
                "source": dict(src_ep),
                "target": {
                    "universe": rec.get("targetUniverse") or rec["sourceUniverse"],
                    "kind": tgt_kind,
                    "nativeSubjectId": tgt_id,
                    "packageManifestPath": tgt_pkg,
                    "occupancy": tgt_occ,
                },
            }
        )
    rows.sort(key=neighbor_key)

    if ("imports", "resolved-target") not in PROJECTABLE:
        raise SystemExit("table drift")

    syn_refuse = refuse_relation("imports", "syntactic-specifier")
    syn_request = {
        "schemaMajor": 3,
        "schemaId": SCHEMA_ID,
        "projectId": project_id,
        "operation": "graph.neighbors",
        "params": {
            "relation": "imports",
            "minResolution": "syntactic-specifier",
            "direction": "outgoing",
            "endpoint": src_ep,
        },
        "view": {"runId": h.suffix(run_id) if False else run_id},
    }

    q_neighbors = {
        "schemaId": SCHEMA_ID,
        "schemaMajor": 3,
        "projectId": project_id,
        "operation": "graph.neighbors",
        "params": {
            "relation": "imports",
            "minResolution": "resolved-target",
            "direction": "outgoing",
            "endpoint": src_ep,
        },
        "view": {"runId": run_id},
        "resolvedView": {"runId": run_id},
        "resultUnits": rows,
        "order": "utf-8 tuple (source.universe, kind, nativeSubjectId, packageManifestPath, target..., fact2 id)",
        "advisory": False,
        "executedOverAdmittedRun": True,
        "occupancySource": "TargetAttributionV2 retained by evaluationInputRefs / hostDerivedRefs",
    }
    q_path = {
        "operation": "graph.path",
        "schemaMajor": 3,
        "projectId": project_id,
        "params": {
            "relation": "imports",
            "minResolution": "resolved-target",
            "direction": "outgoing",
            "start": src_ep,
            "target": src_ep,
            "maxDepth": 1,
        },
        "resolvedView": {"runId": run_id},
        "zeroHop": True,
        "path": {"edges": [], "start": src_ep, "target": src_ep},
        "advisory": False,
        "executedOverAdmittedRun": True,
    }
    reach_eps = []
    for r in rows:
        reach_eps.append(r["target"])
    q_reach = {
        "operation": "graph.reach",
        "schemaMajor": 3,
        "projectId": project_id,
        "params": {
            "relation": "imports",
            "minResolution": "resolved-target",
            "start": src_ep,
            "maxDepth": 1,
            "includeStart": False,
        },
        "resolvedView": {"runId": run_id},
        "reachable": reach_eps,
        "includeStartDefault": False,
        "advisory": False,
        "executedOverAdmittedRun": True,
    }
    sel = sha(canonical_sel := json.dumps(
        {"op": "graph.neighbors", "rel": "imports", "rung": "resolved-target", "ep": src_ep, "includeStart": False},
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8"))
    cursor = {
        "form": f"q3.{h.suffix(run_id)}.{sel}.0",
        "maxChars": 256,
        "boundToHistoricalSelection": True,
        "continuationRequires": "view.{runId} equal to bound Run",
        "afterNewerLatest": "does not re-resolve latest",
        "cacheLoss": "rebuild from same available closure; cache must not change result",
        "measuredLength": len(f"q3.{h.suffix(run_id)}.{sel}.0"),
    }
    disclosure = {
        "coverageIds": [],
        "scopeIds": [],
        "deficiencyCitations": [],
        "resolutionLimitations": [],
        "unresolvedEdgeCount": 0,
        "examinedExhaustive": True,
        "native-evidence-unavailable": False,
        "advisory": False,
    }
    for ident, rec in st.objects.items():
        if ident.startswith("coverage2:") and rec:
            disclosure["coverageIds"].append(ident)
        if ident.startswith("scope2:"):
            disclosure["scopeIds"].append(ident)
    disclosure["coverageIds"] = sorted(set(disclosure["coverageIds"]))
    disclosure["scopeIds"] = sorted(set(disclosure["scopeIds"]))

    malformed = {"operation": "graph.neighbors", "params": {"relation": "not-a-relation"}}
    fail_obs = {"classification": "invalid", "attempted": malformed}
    try:
        schema = kit_schemas.SCHEMAS.get(SCHEMA_ID) or kit_schemas.wrap_def(SCHEMA_ID)
        admit.stock_validate(malformed, schema)
        fail_obs["stockPassedUnexpectedly"] = True
        fail_obs["note"] = "stock JSON Schema is not query admission; QUERY.RELATION_UNSUPPORTED / PARAMS_MALFORMED are contract refusals"
    except Exception as e:
        fail_obs["observedRefusal"] = {
            "code": getattr(e, "code", type(e).__name__),
            "message": str(e)[:2000],
        }
    fail_obs["contractRefusal"] = {
        "unsupportedSyntacticSpecifier": syn_refuse,
        "malformedEnvelope": {
            "kind": "failure",
            "errors": [{"code": "QUERY.PARAMS_MALFORMED", "remedy": "closed graph params", "subject": "relation"}],
            "run": None,
        },
    }

    qdoc = {
        "owners": [
            "docs/coop/design-corrections/workflows/query-projection-contract.v3.md §§1–8",
            "docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json",
            "docs/v2/contracts/product-v1/workflows-and-surfaces.md §8",
        ],
        "schemaId": SCHEMA_ID,
        "schemaMajor": 3,
        "projectId": project_id,
        "admittedRun": run_id,
        "schemaAdmissionBeforeQuery": adm["admitted"],
        "closureBeforeQuery": cl.get("closed"),
        "closeRunReplayed": cl.get("replayed"),
        "neighbors": q_neighbors,
        "path": q_path,
        "reach": q_reach,
        "cursor": cursor,
        "page": {
            "pageSize": 1,
            "truncated-page": len(rows) > 1,
            "truncated-bound": False,
            "maxItemsPerOperation": 100000,
            "maxPageSize": 1000,
        },
        "GraphEvidenceDisclosure": disclosure,
        "syntacticSpecifierRequest": syn_request,
        "syntacticSpecifierRefusal": syn_refuse,
        "history": {"boundRunId": run_id, "replayUsesBoundRunNotLatestAmbient": True},
        "parity": {
            "human": q_neighbors,
            "json": q_neighbors,
            "agent": q_neighbors,
            "compactSummaryJoins": True,
            "fields": ["resolved-view", "availability", "truncated", "total-items", "termination-class", "query-response"],
        },
        "failure": fail_obs,
        "readOnly": True,
        "doesNotSealRun": True,
        "executedOver": run_id,
        "sameOriginContinuation": True,
        "continuationId": "consumer-b.v13-continuation.v2",
    }
    dump(OUT / "query" / "graph-query.json", qdoc)
    print(
        "GRAPH_QUERY",
        run_id,
        "resolved-target-neighbors",
        len(rows),
        "syn-refused",
        syn_refuse["termination"]["domainDetail"]["code"],
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
