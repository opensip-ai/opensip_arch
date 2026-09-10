"""Independent schema probes over frozen v23 evaluator3 graph-query:2.

Review-only. No graph engine, sealed Run, or product implementation.
Schema admission is not proof that a query owner accepts the semantics.
"""
from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path

from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

ROOT = Path("/tmp/opensip-design-corrections/candidate-subject.v23")
WF = ROOT / "docs/coop/design-corrections/workflows/schemas"
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "docs/coop/design-corrections/foundation"))
import canonical  # noqa: E402

docs = [json.loads(p.read_text()) for p in sorted((WF / "evaluator3").glob("*.schema.json"))]
for name in (
    "common.schema.json",
    "imported-evidence.schema.json",
    "policy-document.schema.json",
    "policy-document.v2.schema.json",
    "test-execution.schema.json",
):
    docs.append(json.loads((WF / name).read_text()))
reg = Registry().with_resources((d["$id"], Resource(contents=d, specification=DRAFT202012)) for d in docs)
BASE = "urn:opensip:product-v1:workflows:evaluator3:graph-query:2"


def admitted(selector, value):
    try:
        canonical.typed(value)
        canonical.ExactValidator({"$ref": BASE + "#/$defs/" + selector}, registry=reg).validate(value)
        return {"schemaAdmitted": True}
    except Exception as exc:
        return {"schemaAdmitted": False, "error": str(exc).splitlines()[0][:240]}


PRJ = "prj1-" + "1" * 64
RUN = "run3:" + "2" * 64
SNAP = "snapshot2:" + "4" * 64
BASELINE = "baseline2:" + "3" * 64

req = {
    "schemaFamily": "opensip.product.query",
    "schemaMajor": 2,
    "projectId": PRJ,
    "view": {"runId": RUN},
    "operation": "graph.path",
    "params": {},
    "completeness": "required",
    "page": {"size": 1},
}
cx = {
    "projectId": PRJ,
    "resolvedView": {"latest": True},
    "coverage": "complete",
    "availability": "retained",
    "truncated": False,
    "totalItems": 0,
    "advisory": False,
}
n = copy.deepcopy(req)
n["operation"] = "graph.neighbors"
n["params"] = {"baselineId": BASELINE}
p = copy.deepcopy(req)
p["params"] = {
    "relation": "calls",
    "subject": "src/a.ts",
    "target": "src/b.ts",
    "direction": "both",
    "maxDepth": 2,
}
snap = copy.deepcopy(req)
snap["view"] = {"snapshotId": SNAP}
latest_req = copy.deepcopy(req)
latest_req["view"] = {"latest": True}
cx_run = copy.deepcopy(cx)
cx_run["resolvedView"] = {"runId": RUN}
cx_adv = copy.deepcopy(cx_run)
cx_adv["advisory"] = True
cx_trunc = copy.deepcopy(cx_run)
cx_trunc["truncated"] = True
cx_trunc["totalItems"] = 0
cx_trunc["nextCursor"] = "opaque-token"
reach = copy.deepcopy(req)
reach["operation"] = "graph.reach"
reach["params"] = {"relation": "calls", "subject": "src/a.ts"}

cases = [
    ("graph.path-without-endpoints", "GraphQueryRequestV1", req),
    ("graph.path-snapshot-only-view", "GraphQueryRequestV1", snap),
    ("graph.path-latest-request", "GraphQueryRequestV1", latest_req),
    ("graph.neighbors-irrelevant-baseline-only", "GraphQueryRequestV1", n),
    ("graph.path-logicalpath-endpoints-only", "GraphQueryRequestV1", p),
    ("graph.reach-path-only-subject", "GraphQueryRequestV1", reach),
    ("response-latest-still-unresolved", "GraphQueryResponseContext", cx),
    ("response-concrete-run-ok", "GraphQueryResponseContext", cx_run),
    ("graph-context-advisory-true-not-cross-joined", "GraphQueryResponseContext", cx_adv),
    ("truncated-zero-total-with-cursor", "GraphQueryResponseContext", cx_trunc),
]

schema_path = WF / "evaluator3" / "graph-query.schema.json"
hist_path = WF / "graph-query.schema.json"
result = {
    "standing": "review-only schema observations over frozen v23; not query execution or Run admission",
    "subjectManifestSha256": "652c800166a8d3f37eacfbf273c9786bb84f6fd6b5c6ead57b5a254315859a25",
    "currentSchema": {
        "path": "docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json",
        "id": BASE,
        "sha256": hashlib.sha256(schema_path.read_bytes()).hexdigest(),
        "bytes": schema_path.stat().st_size,
    },
    "historicalSchema": {
        "path": "docs/coop/design-corrections/workflows/schemas/graph-query.schema.json",
        "id": json.loads(hist_path.read_text())["$id"],
        "sha256": hashlib.sha256(hist_path.read_bytes()).hexdigest(),
        "bytes": hist_path.stat().st_size,
        "note": "historical non-evaluator3 parser; not the current owner",
    },
    "probes": [{"name": n, "selector": s, "value": v, **admitted(s, v)} for n, s, v in cases],
}
HERE.joinpath("query-schema-probe.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({r["name"]: r["schemaAdmitted"] for r in result["probes"]}, indent=2))
