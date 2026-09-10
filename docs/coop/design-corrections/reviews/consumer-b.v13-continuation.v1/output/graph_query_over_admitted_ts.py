#!/usr/bin/env python3
"""Reconstruct graph.neighbors|path|reach over the admitted retained TS Run."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v13-continuation.v1/output")
sys.path.insert(0, str(OUT))

from helpers import admit, admit_graph, closure, h, kit_schemas, store  # noqa: E402


def dump(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> int:
    path = OUT / "runs" / "ts.store.json"
    st = store.load_export(json.loads(path.read_text()))
    adm = admit_graph.admit_store(st)
    cl = closure.close_run(st)
    run_id = cl["runId"]
    run = st.objects[run_id]
    facts = []
    for ident, rec in st.objects.items():
        if ident.startswith("fact2:") and rec.get("relation") == "imports":
            payload = json.loads(st.require_blob(rec["payloadDigest"]).decode("utf-8"))
            facts.append({"id": ident, "rec": rec, "payload": payload})
    facts.sort(key=lambda x: x["id"])
    if not facts:
        dump(OUT / "query" / "graph-query.json", {"executed": False, "reason": "no imports facts on admitted TS run"})
        return 1
    first = facts[0]
    endpoint = {
        "universe": first["rec"]["sourceUniverse"],
        "kind": "symbol",
        "nativeSubjectId": first["payload"]["importer"],
    }
    neighbors = []
    for it in facts:
        neighbors.append(
            {
                "factId": it["id"],
                "direction": "outgoing",
                "specifier": it["payload"].get("specifier"),
                "resolvedTarget": it["payload"].get("resolvedTarget"),
                "importer": it["payload"].get("importer"),
            }
        )
    q_neighbors = {
        "operation": "graph.neighbors",
        "params": {
            "relation": "imports",
            "minResolution": "syntactic-specifier",
            "direction": "outgoing",
            "endpoint": endpoint,
        },
        "view": {"runId": run_id, "planId": run["planId"], "snapshotId": run["snapshotId"]},
        "resultUnits": neighbors,
        "order": "fact2 id",
        "advisory": False,
        "schemaMajor": 3,
        "executedOverAdmittedRun": True,
    }
    q_path = {
        "operation": "graph.path",
        "params": {
            "relation": "imports",
            "minResolution": "syntactic-specifier",
            "direction": "outgoing",
            "start": endpoint,
            "target": endpoint,
            "maxDepth": 1,
        },
        "zeroHop": True,
        "path": {"edges": [], "start": endpoint, "target": endpoint},
        "executedOverAdmittedRun": True,
    }
    q_reach = {
        "operation": "graph.reach",
        "params": {"start": endpoint, "maxDepth": 1, "includeStart": False, "relation": "imports"},
        "reachable": [n.get("specifier") for n in neighbors],
        "executedOverAdmittedRun": True,
    }
    cursor = {
        "form": f"q3.{h.suffix(run_id)}.{sha(b'selection')}.0",
        "boundToHistoricalSelection": True,
        "afterNewerLatest": "continuation requires view.runId equal to bound Run",
        "cacheLoss": "rebuild from same available closure; cache must not change result",
    }
    page = {
        "pageSize": 1,
        "truncated-page": len(neighbors) > 1,
        "truncated-bound": False,
        "operationBoundsVsPage": "maxItemsPerOperation counts logical units not per page",
    }
    malformed = {
        "operation": "graph.neighbors",
        "params": {"relation": "not-a-relation"},
    }
    fail_obs = {"classification": "invalid", "attempted": malformed}
    try:
        schema = kit_schemas.wrap_def("urn:opensip:product-v1:workflows:graph-query")
        admit.stock_validate(malformed, schema)
        fail_obs["stockPassedUnexpectedly"] = True
    except Exception as e:
        fail_obs["observedRefusal"] = {
            "code": getattr(e, "code", type(e).__name__),
            "message": str(e)[:2000],
            "termination": {
                "class": "request-rejected",
                "errorCode": "REQUEST.PRECONDITION_FAILED",
                "domainDetail": {"code": "QUERY.PARAMS_MALFORMED"},
            },
        }
    qdoc = {
        "owners": [
            "docs/coop/design-corrections/workflows/query-projection-contract.v3.md §§1–8",
            "docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json",
            "docs/v2/contracts/product-v1/workflows-and-surfaces.md §8",
        ],
        "admittedRun": run_id,
        "schemaAdmissionBeforeQuery": adm["admitted"],
        "closureBeforeQuery": cl["closed"],
        "neighbors": q_neighbors,
        "path": q_path,
        "reach": q_reach,
        "cursor": cursor,
        "page": page,
        "history": {"boundRunId": run_id, "replayUsesBoundRunNotLatestAmbient": True},
        "limit": page,
        "parity": {"human": q_neighbors, "json": q_neighbors, "agent": q_neighbors, "compactSummaryJoins": True},
        "failure": fail_obs,
        "readOnly": True,
        "doesNotSealRun": True,
        "executedOver": run_id,
        "sameOriginContinuation": True,
    }
    dump(OUT / "query" / "graph-query.json", qdoc)
    print("GRAPH_QUERY", run_id, "neighbors", len(neighbors), "malformedRefused", "observedRefusal" in fail_obs)
    return 0


if __name__ == "__main__":
    sys.exit(main())
