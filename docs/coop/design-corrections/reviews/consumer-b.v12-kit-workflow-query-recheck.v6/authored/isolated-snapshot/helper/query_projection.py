"""Query projection contract v3 — reusable public wrapper.

execute_graph_query(request, run, objects, blobs, host) requires a real
close_run of retained Run bytes, then projects views/facts/payloads/
TargetAttributionV1/Coverage from THAT admitted closure. Caller-authored
edges, limitation arrays, host.cache/standing/targetAttributions/
evaluationDeficiencies, and synthetic positive close_run flags are not
public graph evidence.

traverse_projected_graph is labeled algorithmic only.

Does not mint a Run. Cursor binding is an operational digest, not a
published identity recipe. Target kind/occupancy come from retained
TargetAttributionV1; SubjectId spelling is never parsed to invent them.
"""
from __future__ import annotations

import base64
import hashlib
from collections import deque
from typing import Any, Callable

from helper.canonical import C
from helper.closure_admit import parse_typed_h, rehash
from helper.errors import AdmissionError
from helper.identity import parse_h_frame, typed_id
from helper.store import Store
from helper.workflow_laws import (
    GRAPH_PROJECTABLE,
    cursor_token,
    endpoint_key,
    page_items,
    render_parity,
    selection_hash,
)

CLASS_TO_EXIT = {
    "success": 0,
    "policy-failed": 1,
    "request-rejected": 2,
    "indeterminate": 3,
    "operational-failed": 4,
    "interrupted": 130,
}

PUBLIC_BOUNDS = {
    "maxPageSize": 1000,
    "defaultPageSize": 100,
    "maxItemsPerOperation": 100000,
    "maxTraversalDepth": 64,
    "maxVisitedNodes": 1000000,
}

PROJECTION_TABLE = {
    ("calls", "resolved-callee"): {
        "src": "caller", "tgt": "resolvedCallee",
        "srcKind": "symbol", "tgtKind": "symbol", "universe": "admitted-target",
    },
    ("references", "resolved-binding"): {
        "src": "referrer", "tgt": "resolvedBinding",
        "srcKind": "symbol", "tgtKind": "symbol", "universe": "admitted-target",
    },
    ("imports", "resolved-target"): {
        "src": "importer", "tgt": "resolvedTarget",
        "srcKind": "symbol", "tgtKind": None, "universe": "admitted-target",
    },
    ("control-flow", "syntactic"): {
        "src": "from", "tgt": "to",
        "srcKind": "symbol", "tgtKind": "symbol", "universe": "same-only",
    },
    ("reachability", "from-resolved-calls"): {
        "src": "origin", "tgt": "reachable",
        "srcKind": "symbol", "tgtKind": "symbol", "universe": "same-only",
    },
}

REQUEST_KEYS = {
    "schemaFamily", "schemaMajor", "projectId", "view", "operation",
    "params", "completeness", "page", "fieldSelection",
}

PRJ_PREFIX = "prj1-"


class QueryRefusal(AdmissionError):
    def __init__(self, code: str, message: str, *, klass: str, error_code: str, extra=None):
        super().__init__(code, message, extra=extra)
        self.klass = klass
        self.error_code = error_code

    def envelope(self, *, request_id: str, project_id: str | None = None) -> dict:
        term = {
            "class": self.klass,
            "errorCode": self.error_code,
            "domainDetail": {"code": self.code, "remedy": self.message},
        }
        if self.klass == "operational-failed":
            term["faultCause"] = (self.extra or {}).get("faultCause", "host-io")
        env = {
            "schemaFamily": "opensip.product.envelope",
            "schemaMajor": 3,
            "kind": "failure",
            "requestId": request_id,
            "termination": term,
            "exitCode": CLASS_TO_EXIT[self.klass],
            "errors": [term["domainDetail"]],
        }
        if project_id:
            env["projectId"] = project_id
        return env


def _host_request_id(host: dict | None) -> str:
    rid = (host or {}).get("requestId")
    if not isinstance(rid, str) or not rid.startswith("req1_") or len(rid) != 37:
        raise QueryRefusal(
            "REFERENCE_CALL_PRECONDITION",
            "host.requestId must be an already reserved req1_+32hex observation",
            klass="request-rejected",
            error_code="REQUEST.PRECONDITION_FAILED",
        )
    if any(c not in "0123456789abcdef" for c in rid[5:]):
        raise QueryRefusal(
            "REFERENCE_CALL_PRECONDITION",
            "host.requestId must be req1_+32hex",
            klass="request-rejected",
            error_code="REQUEST.PRECONDITION_FAILED",
        )
    return rid


def _page_size(request: dict, bounds: dict) -> int:
    page = request.get("page") or {}
    if not isinstance(page, dict):
        raise QueryRefusal("QUERY.PARAMS_MALFORMED", "page not object", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
    extra = set(page) - {"size", "cursor"}
    if extra:
        raise QueryRefusal("QUERY.PARAMS_MALFORMED", f"page extra {sorted(extra)}", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
    size = page.get("size", bounds["defaultPageSize"])
    if not isinstance(size, int) or size < 1 or size > bounds["maxPageSize"]:
        raise QueryRefusal("QUERY.PARAMS_MALFORMED", "page.size out of bounds", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
    return size


def _admitted_project_id(project_id: Any) -> str | None:
    if isinstance(project_id, str) and project_id.startswith(PRJ_PREFIX) and len(project_id) == 4 + 1 + 64:
        hexpart = project_id[5:]
        if all(c in "0123456789abcdef" for c in hexpart):
            return project_id
    return None


def admit_request(request: dict) -> None:
    if not isinstance(request, dict):
        raise QueryRefusal("QUERY.PARAMS_MALFORMED", "request not an object", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
    extra_top = set(request) - REQUEST_KEYS
    if extra_top:
        raise QueryRefusal("QUERY.PARAMS_MALFORMED", f"extra request properties {sorted(extra_top)}", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
    if request.get("schemaFamily") != "opensip.product.query":
        raise QueryRefusal("QUERY.PARAMS_MALFORMED", "schemaFamily", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
    if request.get("schemaMajor") != 3:
        raise QueryRefusal("QUERY.SCHEMA_MAJOR_UNSUPPORTED", "schemaMajor must be 3", klass="request-rejected", error_code="REQUEST.SCHEMA_MAJOR_UNSUPPORTED")
    if request.get("operation") not in ("graph.neighbors", "graph.path", "graph.reach"):
        raise QueryRefusal("QUERY.PARAMS_MALFORMED", "not a graph operation in this reconstruction", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
    if request.get("completeness") not in ("required", "best-effort"):
        raise QueryRefusal("QUERY.PARAMS_MALFORMED", "completeness", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
    if "page" not in request:
        raise QueryRefusal("QUERY.PARAMS_MALFORMED", "page required", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
    view = request.get("view")
    if not isinstance(view, dict):
        raise QueryRefusal("QUERY.PARAMS_MALFORMED", "view", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
    vkeys = set(view)
    if vkeys == {"runId"} or vkeys == {"snapshotId"} or vkeys == {"latest"}:
        pass
    else:
        raise QueryRefusal("QUERY.PARAMS_MALFORMED", "view selector must be exactly {runId}|{snapshotId}|{latest:true}", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
    if "latest" in view and view.get("latest") is not True:
        raise QueryRefusal("QUERY.PARAMS_MALFORMED", "latest must be true", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
    params = request.get("params")
    if not isinstance(params, dict):
        raise QueryRefusal("QUERY.PARAMS_MALFORMED", "params", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
    extra = set(params) - {
        "relation", "minResolution", "direction", "endpoint", "start", "target",
        "maxDepth", "includeStart", "factViewDigests",
    }
    if extra:
        raise QueryRefusal("QUERY.PARAMS_MALFORMED", f"extra params {sorted(extra)}", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
    op = request["operation"]
    for forbidden in ("subject", "logicalPath"):
        if forbidden in params:
            raise QueryRefusal("QUERY.PARAMS_MALFORMED", f"LogicalPath/non-graph bag {forbidden} forbidden on graph ops", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
    required = ["relation", "minResolution"]
    if op == "graph.neighbors":
        required += ["direction", "endpoint"]
    elif op == "graph.path":
        required += ["direction", "start", "target", "maxDepth"]
    else:
        required += ["start", "maxDepth"]
    for key in required:
        if key not in params:
            raise QueryRefusal("QUERY.PARAMS_MALFORMED", f"missing {key}", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
    if "direction" in params and params["direction"] not in ("outgoing", "incoming", "both"):
        raise QueryRefusal("QUERY.PARAMS_MALFORMED", "direction", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
    if "includeStart" in params and not isinstance(params["includeStart"], bool):
        raise QueryRefusal("QUERY.PARAMS_MALFORMED", "includeStart", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
    if "maxDepth" in params:
        md = params["maxDepth"]
        if not isinstance(md, int) or md < 0 or md > PUBLIC_BOUNDS["maxTraversalDepth"]:
            raise QueryRefusal("QUERY.PARAMS_MALFORMED", "maxDepth", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
    if "factViewDigests" in params:
        fvd = params["factViewDigests"]
        if not isinstance(fvd, list) or any(not isinstance(x, str) or not x.startswith("view2:") for x in fvd):
            raise QueryRefusal("QUERY.PARAMS_MALFORMED", "factViewDigests", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
    for key in ("endpoint", "start", "target"):
        ep = params.get(key)
        if ep is None:
            continue
        if not isinstance(ep, dict):
            raise QueryRefusal("QUERY.PARAMS_MALFORMED", f"{key} not object", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
        if "logicalPath" in ep or ("path" in ep and "universe" not in ep):
            raise QueryRefusal("QUERY.PARAMS_MALFORMED", f"{key} LogicalPath-only endpoint forbidden", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
        extra_ep = set(ep) - {"universe", "kind", "nativeSubjectId", "packageManifestPath"}
        if extra_ep:
            raise QueryRefusal("QUERY.PARAMS_MALFORMED", f"{key} extra {sorted(extra_ep)}", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
        uni = ep.get("universe")
        if not isinstance(uni, str) or len(uni) != 64 or any(c not in "0123456789abcdef" for c in uni):
            raise QueryRefusal("QUERY.PARAMS_MALFORMED", f"{key} universe not 64-hex", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
        if ep.get("kind") not in {"file", "symbol", "package"}:
            raise QueryRefusal("QUERY.PARAMS_MALFORMED", f"{key} kind", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
        if not ep.get("nativeSubjectId"):
            raise QueryRefusal("QUERY.PARAMS_MALFORMED", f"{key} empty native id", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
        if ep.get("kind") != "package" and ep.get("packageManifestPath"):
            raise QueryRefusal("QUERY.PARAMS_MALFORMED", "packageManifestPath on non-package", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")


def join_view(*, request: dict, admitted_run: dict, host: dict) -> dict:
    view = request.get("view") or {}
    run_id = admitted_run["runId"]
    if "runId" in view:
        if view["runId"] != run_id:
            raise QueryRefusal("QUERY.VIEW_UNKNOWN", "request runId is not the admitted Run", klass="request-rejected", error_code="IDENTITY.UNKNOWN")
        return {"runId": run_id}
    if "snapshotId" in view:
        obs = (host.get("runsForSnapshot") or {}).get(view["snapshotId"]) or []
        if not obs:
            raise QueryRefusal("QUERY.VIEW_UNKNOWN", "missing host.runsForSnapshot observation", klass="request-rejected", error_code="IDENTITY.UNKNOWN")
        distinct = sorted(set(obs))
        if len(distinct) > 1:
            raise QueryRefusal("QUERY.VIEW_AMBIGUOUS", "two Runs named for one snapshot", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
        if distinct[0] != run_id or view["snapshotId"] != admitted_run["snapshotId"]:
            raise QueryRefusal("QUERY.VIEW_UNKNOWN", "snapshot resolver does not name the admitted Run", klass="request-rejected", error_code="IDENTITY.UNKNOWN")
        return {"runId": run_id}
    if view.get("latest") is True:
        latest = host.get("latestRunId")
        if latest != run_id:
            raise QueryRefusal("QUERY.VIEW_UNKNOWN", "host.latestRunId missing or unequal to admitted Run", klass="request-rejected", error_code="IDENTITY.UNKNOWN")
        return {"runId": run_id}
    raise QueryRefusal("QUERY.VIEW_UNKNOWN", "view selector empty", klass="request-rejected", error_code="IDENTITY.UNKNOWN")


def operational_bind(*, project_id: str, run_id: str, fact_view_digests: list[str], operation: str, params: dict) -> str:
    """Operational continuation digest. Not a published identity domain."""
    return selection_hash(
        project_id=project_id,
        run_id=run_id,
        fact_view_digests=fact_view_digests,
        operation=operation,
        params=params,
    )


def parse_cursor(token: str) -> dict:
    if not isinstance(token, str) or len(token) > 256:
        raise QueryRefusal("QUERY.CURSOR_MISMATCH", "cursor length", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
    parts = token.split(".")
    if len(parts) != 4 or parts[0] != "q3":
        raise QueryRefusal("QUERY.CURSOR_MISMATCH", "cursor form", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
    _, run_hex, sel, pos = parts
    if len(run_hex) != 64 or len(sel) != 64:
        raise QueryRefusal("QUERY.CURSOR_MISMATCH", "cursor hex width", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
    try:
        position = int(pos)
    except ValueError as e:
        raise QueryRefusal("QUERY.CURSOR_MISMATCH", "cursor position", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED") from e
    return {"runHex": run_hex, "selection": sel, "position": position}


def visit_capped_path(*, edges: list[dict], start: dict, target: dict, max_depth: int, max_visited: int, direction: str = "outgoing") -> tuple[dict | None, dict]:
    if endpoint_key(start) == endpoint_key(target):
        return {"hopCount": 0, "start": start, "target": target, "nodes": [start], "edges": []}, {"visitedNodes": 1, "truncatedBound": False}
    adj: dict[tuple, list] = {}
    for e in edges:
        if direction in ("outgoing", "both"):
            adj.setdefault(endpoint_key(e["source"]), []).append(e)
        if direction in ("incoming", "both"):
            adj.setdefault(endpoint_key(e["target"]), []).append({**e, "source": e["target"], "target": e["source"]})
    for k in adj:
        adj[k].sort(key=lambda e: e["factId"])
    visited = {endpoint_key(start)}
    q = deque([(start, [start], [])])
    truncated = False
    while q:
        node, nodes, path_edges = q.popleft()
        if len(path_edges) >= max_depth:
            continue
        for e in adj.get(endpoint_key(node), []):
            nxt = e["target"]
            nk = endpoint_key(nxt)
            if nk in visited:
                continue
            if len(visited) >= max_visited:
                truncated = True
                continue
            visited.add(nk)
            nn = nodes + [nxt]
            ne = path_edges + [{"factId": e["factId"], "source": e["source"], "target": e["target"]}]
            if endpoint_key(nxt) == endpoint_key(target):
                return {"hopCount": len(ne), "start": start, "target": target, "nodes": nn, "edges": ne}, {"visitedNodes": len(visited), "truncatedBound": False}
            q.append((nxt, nn, ne))
    return None, {"visitedNodes": len(visited), "truncatedBound": truncated}


def visit_capped_reach(*, edges: list[dict], start: dict, max_depth: int, max_visited: int, include_start: bool, direction: str = "outgoing") -> tuple[list[dict], dict]:
    rows = []
    if include_start:
        rows.append({"endpoint": start, "depth": 0})
    adj: dict[tuple, list] = {}
    for e in edges:
        if direction in ("outgoing", "both"):
            adj.setdefault(endpoint_key(e["source"]), []).append(e)
        if direction in ("incoming", "both"):
            adj.setdefault(endpoint_key(e["target"]), []).append({**e, "source": e["target"], "target": e["source"]})
    for k in adj:
        adj[k].sort(key=lambda e: e["factId"])
    seen = {endpoint_key(start)}
    q = deque([(start, 0)])
    truncated = False
    while q:
        node, depth = q.popleft()
        if depth >= max_depth:
            continue
        for e in adj.get(endpoint_key(node), []):
            nxt = e["target"]
            nk = endpoint_key(nxt)
            if nk in seen:
                continue
            if len(seen) >= max_visited:
                truncated = True
                continue
            seen.add(nk)
            nd = depth + 1
            rows.append({"endpoint": nxt, "depth": nd, "viaFactId": e["factId"]})
            q.append((nxt, nd))
    rows.sort(key=lambda r: endpoint_key(r["endpoint"]))
    return rows, {"visitedNodes": len(seen), "truncatedBound": truncated}


def neighbors_rows(*, edges: list[dict], endpoint: dict, direction: str) -> list[dict]:
    ek = endpoint_key(endpoint)
    out = []
    for e in edges:
        if direction in ("outgoing", "both") and endpoint_key(e["source"]) == ek:
            out.append(e)
        if direction in ("incoming", "both") and endpoint_key(e["target"]) == ek:
            out.append(e)
    seen = set()
    uniq = []
    for e in out:
        if e["factId"] in seen:
            continue
        seen.add(e["factId"])
        uniq.append(e)
    uniq.sort(key=lambda e: endpoint_key(e["source"]) + endpoint_key(e["target"]) + (e["factId"],))
    return uniq


def vertex_domain(*, inventories: list[dict], edges: list[dict], default_universe: str | None = None) -> list[dict]:
    verts = []
    seen = set()
    for inv in inventories:
        kind = inv.get("kind")
        u = inv.get("universe") or default_universe
        for row in inv.get("rows") or []:
            ep = {"universe": u, "kind": kind, "nativeSubjectId": row["nativeSubjectId"]}
            if kind == "package":
                ep["packageManifestPath"] = row.get("path")
            k = endpoint_key(ep)
            if k not in seen:
                seen.add(k)
                verts.append(ep)
    for e in edges:
        for ep in (e["source"], e["target"]):
            k = endpoint_key(ep)
            if k not in seen:
                seen.add(k)
                verts.append(ep)
    return verts


def admit_endpoint(ep: dict, vertices: list[dict]) -> dict:
    # Contract §2 fault precedence: package identity without packageManifestPath
    # is ENDPOINT_AMBIGUOUS even when only one package vertex exists.
    if ep.get("kind") == "package" and not ep.get("packageManifestPath"):
        raise QueryRefusal(
            "QUERY.ENDPOINT_AMBIGUOUS",
            "package identity without packageManifestPath",
            klass="request-rejected",
            error_code="REQUEST.PRECONDITION_FAILED",
        )
    matches = [
        v for v in vertices
        if v["universe"] == ep["universe"] and v["kind"] == ep["kind"] and v["nativeSubjectId"] == ep["nativeSubjectId"]
    ]
    if ep.get("kind") == "package":
        matches = [v for v in matches if v.get("packageManifestPath") == ep.get("packageManifestPath")]
    if len(matches) > 1:
        raise QueryRefusal("QUERY.ENDPOINT_AMBIGUOUS", "tuple matches more than one vertex", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
    if not matches:
        raise QueryRefusal("QUERY.ENDPOINT_UNKNOWN", "well-formed endpoint outside vertex domain", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
    return matches[0]


def availability_refuse(host: dict) -> None:
    avail = host.get("availability")
    if avail in {"purged", "expired", "unavailable", "corrupt"}:
        code = "evidence." + avail if avail != "unavailable" else "evidence.missing"
        raise QueryRefusal(code, f"host availability {avail} refuses access", klass="operational-failed", error_code="HOST.IO_FAILURE", extra={"faultCause": "host-io"})


def _decode_blob(v: Any) -> bytes:
    if isinstance(v, bytes):
        return v
    if isinstance(v, str):
        try:
            return base64.b64decode(v, validate=False)
        except Exception as e:
            raise QueryRefusal("evidence.corrupt", "blob is not retained bytes", klass="operational-failed", error_code="HOST.IO_FAILURE", extra={"faultCause": "host-io"}) from e
    raise QueryRefusal("evidence.corrupt", "blob type", klass="operational-failed", error_code="HOST.IO_FAILURE", extra={"faultCause": "host-io"})


def materialize_store(objects: dict | None, blobs: dict | None) -> Store:
    if objects is None or blobs is None:
        raise QueryRefusal("evidence.missing", "retained objects/blobs missing", klass="operational-failed", error_code="HOST.IO_FAILURE", extra={"faultCause": "host-io"})
    store = Store()
    store.object_table = dict(objects)
    for k, v in blobs.items():
        raw = _decode_blob(v)
        got = hashlib.sha256(raw).hexdigest()
        if got != k:
            raise QueryRefusal("evidence.corrupt", f"blob {k} rehashes to {got}", klass="operational-failed", error_code="HOST.IO_FAILURE", extra={"faultCause": "host-io"})
        store.blobs[k] = raw
    return store


def _store_from_objects_blobs(objects, blobs) -> Store:
    store = Store()
    store.object_table = dict(objects)
    for k, v in blobs.items():
        if isinstance(v, bytes):
            raw = v
        elif isinstance(v, str):
            raw = base64.b64decode(v)
        else:
            raise AdmissionError("CLOSE_RUN_BLOB_TYPE", str(type(v)))
        got = hashlib.sha256(raw).hexdigest()
        if got != k:
            raise AdmissionError("BLOB_REHASH", f"{k} rehashes to {got}")
        store.blobs[k] = raw
    return store


def _parse_canonical_or_missing(store: Store, digest: str) -> Any:
    if digest not in store.blobs:
        raise AdmissionError("CLOSE_RUN_MISSING_BLOB", digest)
    raw = rehash(store, digest)
    from helper.lexical import admit_raw
    obj = admit_raw(raw)
    if C(obj) != raw:
        raise AdmissionError("CANONICAL_REMAINDER", digest)
    return obj


def universe_for_inventory(inv: dict, enum_plan: dict | None) -> str | None:
    """EnumerationPlan program binding (cellOrdinal, programOrdinal) is the universe owner."""
    if not enum_plan:
        return None
    cells = enum_plan.get("cells") or []
    cell_i = inv.get("cellOrdinal")
    prog_i = inv.get("programOrdinal")
    if not isinstance(cell_i, int) or cell_i < 0 or cell_i >= len(cells):
        return None
    bindings = cells[cell_i].get("programBindings") or []
    for b in bindings:
        if b.get("ordinal") == prog_i:
            return b.get("universe")
    if isinstance(prog_i, int) and 0 <= prog_i < len(bindings):
        return bindings[prog_i].get("universe")
    return None


def admit_selected_closure(store: Store, run_body: dict) -> dict:
    """Selected views/inventories/TA/Coverage/IncomingSearch of THIS Run.

    Authority is semantic-evidence.viewIds and proof.evaluationInputRefs
    (plus execution-inputs selectedRefs when that digest is retained).
    Object-table occupancy is not admission.
    """
    view_ids: list[str] = []
    coverage_ids: list[str] = []
    ei_refs: list[dict] = []
    evidence = None
    proof = None
    evidence_id = run_body.get("evidenceId")
    if evidence_id and evidence_id in store.object_table:
        evidence = parse_typed_h(store, evidence_id, "semantic-evidence")
        view_ids.extend(evidence.get("viewIds") or [])
        coverage_ids.extend(evidence.get("coverageIds") or [])
        proof_id = evidence.get("proofBundleId")
        if proof_id and proof_id in store.object_table:
            proof = parse_typed_h(store, proof_id, "proof-bundle")
            ei_refs.extend(proof.get("evaluationInputRefs") or [])
            ei_d = proof.get("executionInputsDigest")
            if ei_d and ei_d in store.blobs:
                ei = _parse_canonical_or_missing(store, ei_d)
                ei_refs.extend(ei.get("selectedRefs") or [])

    def refs(domain: str) -> list[str]:
        return [r["digest"] for r in ei_refs if r.get("domain") == domain and r.get("digest")]

    for d in refs("view"):
        vid = d if d.startswith("view2:") else f"view2:{d}"
        if vid not in view_ids:
            view_ids.append(vid)
    for d in refs("coverage"):
        cid = d if d.startswith("coverage2:") else f"coverage2:{d}"
        if cid not in coverage_ids:
            coverage_ids.append(cid)

    views = {}
    for vid in view_ids:
        if vid not in store.object_table:
            raise AdmissionError("CLOSE_RUN_MISSING_BLOB", vid)
        views[vid] = parse_typed_h(store, vid, "view")

    facts = {}
    payloads = {}
    for view in views.values():
        for fid in view.get("facts") or []:
            if fid in facts:
                continue
            if fid not in store.object_table:
                raise AdmissionError("CLOSE_RUN_MISSING_BLOB", fid)
            rec = parse_typed_h(store, fid, "fact")
            facts[fid] = rec
            payloads[fid] = _parse_canonical_or_missing(store, rec["payloadDigest"])
        for cid in view.get("coverageIds") or []:
            if cid not in coverage_ids:
                coverage_ids.append(cid)

    coverages = {}
    for cid in coverage_ids:
        if cid not in store.object_table:
            continue
        crec = parse_typed_h(store, cid, "coverage")
        payload = _parse_canonical_or_missing(store, crec["payloadDigest"])
        coverages[cid] = {"record": crec, "payload": payload}

    attributions = {}
    for d in refs("target-attribution"):
        obj = _parse_canonical_or_missing(store, d)
        if isinstance(obj, dict) and obj.get("sourceFactId"):
            attributions[obj["sourceFactId"]] = obj

    inventories = []
    for d in refs("subject-inventory"):
        obj = _parse_canonical_or_missing(store, d)
        if isinstance(obj, dict) and "rows" in obj:
            inventories.append(obj)

    incoming_searches = []
    for d in refs("incoming-search"):
        obj = _parse_canonical_or_missing(store, d)
        if isinstance(obj, dict):
            incoming_searches.append({"digest": d, "record": obj})

    enum_plan = None
    for d in refs("enumeration-plan"):
        enum_plan = _parse_canonical_or_missing(store, d)
        break

    for inv in inventories:
        uni = universe_for_inventory(inv, enum_plan)
        if uni:
            inv["universe"] = uni

    deficiencies = []
    if proof:
        for d in proof.get("executionDeficiencies") or []:
            deficiencies.append(d)

    return {
        "views": views,
        "facts": facts,
        "payloads": payloads,
        "coverages": coverages,
        "attributions": attributions,
        "inventories": inventories,
        "incomingSearches": incoming_searches,
        "enumPlan": enum_plan,
        "deficiencies": deficiencies,
        "admittedViewIds": list(view_ids),
        "runBody": run_body,
        "evidence": evidence,
        "proof": proof,
    }


def close_retained_run(run: dict, objects=None, blobs=None):
    """Query-scoped selected-closure close.

    Rehashes blobs, parses run3, then admits only evidence.viewIds and
    proof.evaluationInputRefs of this Run. Not identity-and-evidence §3
    complete-graph close of a B12 positive. A boolean success flag is not
    an admitted closure.
    """
    if run is None or objects is None or blobs is None:
        raise AdmissionError("CLOSE_RUN_MISSING", "close_run requires run/objects/blobs")
    store = _store_from_objects_blobs(objects, blobs)
    run_id = run.get("runId") if isinstance(run, dict) else None
    if not run_id or run_id not in store.object_table:
        raise AdmissionError("CLOSE_RUN_RUN_ABSENT", "run3 not in object table")
    body = parse_typed_h(store, run_id, "run")
    recomputed = typed_id("run", body)
    if recomputed != run_id:
        raise AdmissionError("RUN_H_MISMATCH", f"{recomputed} != {run_id}")
    if run.get("snapshotId") and body.get("snapshotId") != run["snapshotId"]:
        raise AdmissionError("RUN_SNAPSHOT_JOIN", "locator snapshotId != retained run body")
    if run.get("projectId") and body.get("projectId") != run["projectId"]:
        raise AdmissionError("RUN_PROJECT_JOIN", "locator projectId != retained run body")
    rec = store.object_table[run_id]
    if rec.get("digest"):
        rehash(store, rec["digest"])
    records = admit_selected_closure(store, body)
    return {
        "ok": True,
        "runBody": body,
        "runId": run_id,
        "records": records,
        "admittedViewIds": records["admittedViewIds"],
        "label": "query-scoped-selected-closure",
        "completeGraphClose": False,
    }


def _map_close_run_error(e: AdmissionError) -> QueryRefusal:
    missing = {"CLOSE_RUN_MISSING", "CLOSE_RUN_RUN_ABSENT", "CLOSE_RUN_MISSING_BLOB", "not retained"}
    corrupt = {"BLOB_REHASH", "H_FRAME_PREFIX", "H_FRAME_NOT_CANONICAL", "H_FRAME_LENGTH_MISMATCH", "CLOSE_RUN_BLOB_TYPE"}
    if e.code in missing or "not retained" in str(e):
        return QueryRefusal("evidence.missing", str(e), klass="operational-failed", error_code="HOST.IO_FAILURE", extra={"faultCause": "host-io"})
    if e.code in corrupt:
        return QueryRefusal("evidence.corrupt", str(e), klass="operational-failed", error_code="HOST.IO_FAILURE", extra={"faultCause": "host-io"})
    return QueryRefusal("QUERY.VIEW_UNKNOWN", f"close_run refused: {e.code}", klass="request-rejected", error_code="IDENTITY.UNKNOWN")


def _parse_canonical_blob(store: Store, digest: str) -> Any:
    raw = rehash(store, digest)
    from helper.lexical import admit_raw
    obj = admit_raw(raw)
    if C(obj) != raw:
        raise QueryRefusal("evidence.corrupt", f"canonical remainder {digest}", klass="operational-failed", error_code="HOST.IO_FAILURE", extra={"faultCause": "host-io"})
    return obj


def load_closure_records(store: Store, *, run_id: str, run_body: dict) -> dict:
    """Deprecated scan path. Public wrapper must use close_run admitted records."""
    return admit_selected_closure(store, run_body)


def view_matches_relation(view: dict, facts: dict, coverages: dict, relation: str, rung: str) -> bool:
    for fid in view.get("facts") or []:
        rec = facts.get(fid)
        if rec and rec.get("relation") == relation and rec.get("resolution") == rung:
            return True
    for cid in view.get("coverageIds") or []:
        cov = coverages.get(cid)
        if not cov:
            continue
        key = (cov["payload"].get("key") or {})
        if key.get("relation") == relation and key.get("resolution") == rung:
            return True
    return False


def project_from_closure(*, records: dict, relation: str, rung: str, selected_view_ids: list[str]) -> tuple[list[dict], list[dict], list[dict]]:
    spec = PROJECTION_TABLE[(relation, rung)]
    edges = []
    limitations = []
    selected_facts = []
    for vid in selected_view_ids:
        view = records["views"][vid]
        if not view_matches_relation(view, records["facts"], records["coverages"], relation, rung):
            continue
        for fid in view.get("facts") or []:
            rec = records["facts"].get(fid)
            if rec is None:
                continue
            selected_facts.append((fid, rec))
    seen_f = set()
    for fid, rec in selected_facts:
        if fid in seen_f:
            continue
        seen_f.add(fid)
        if rec.get("relation") != relation:
            continue
        if rec.get("resolution") != rung:
            if rec.get("relation") == relation:
                limitations.append({"kind": "unsupported-rung-omitted", "factId": fid, "relation": relation, "minResolution": rec.get("resolution")})
            continue
        pl = records["payloads"].get(fid) or {}
        src_f, tgt_f = spec["src"], spec["tgt"]
        if src_f not in pl or tgt_f not in pl:
            limitations.append({"kind": "unprojectable-fact", "factId": fid, "relation": relation, "minResolution": rung})
            continue
        tgt_kind = spec["tgtKind"]
        tgt_pmp = None
        if relation == "imports":
            ta = records["attributions"].get(fid)
            # TargetAttributionV1 is the owner. Do not parse native id spelling.
            if not ta or ta.get("kind") not in {"file", "symbol", "package"}:
                limitations.append({"kind": "unprojectable-fact", "factId": fid, "relation": relation, "minResolution": rung})
                continue
            if ta.get("targetNativeId") != pl[tgt_f]:
                limitations.append({"kind": "unprojectable-fact", "factId": fid, "relation": relation, "minResolution": rung})
                continue
            tgt_kind = ta["kind"]
            if tgt_kind == "package":
                tgt_pmp = ta.get("packageManifestPath")
                if not tgt_pmp:
                    limitations.append({"kind": "unprojectable-fact", "factId": fid, "relation": relation, "minResolution": rung})
                    continue
        src = {
            "universe": rec["sourceUniverse"],
            "kind": spec["srcKind"],
            "nativeSubjectId": pl[src_f],
        }
        tgt_uni = rec["targetUniverse"] if spec["universe"] == "admitted-target" else rec["sourceUniverse"]
        tgt = {
            "universe": tgt_uni,
            "kind": tgt_kind,
            "nativeSubjectId": pl[tgt_f],
        }
        if tgt_pmp:
            tgt["packageManifestPath"] = tgt_pmp
        row = {
            "factId": fid,
            "relation": relation,
            "resolution": rung,
            "source": src,
            "target": tgt,
        }
        if rec.get("producerClosure"):
            row["producerClosure"] = rec["producerClosure"]
        edges.append(row)
    edges.sort(key=lambda e: endpoint_key(e["source"]) + endpoint_key(e["target"]) + (e["factId"],))
    return edges, limitations, selected_view_ids


def disclose_evidence(*, records: dict, selected_view_ids: list[str], relation: str, rung: str, projection_limitations: list[dict], selected_match: bool) -> dict:
    coverage_ids = []
    scope_ids = []
    for vid in selected_view_ids:
        view = records["views"][vid]
        for sid in view.get("scopeIds") or []:
            if sid not in scope_ids:
                scope_ids.append(sid)
        for cid in view.get("coverageIds") or []:
            if cid not in coverage_ids:
                coverage_ids.append(cid)
    # other retained Coverage whose key relation is the declared query relation
    for cid, cov in records["coverages"].items():
        key = (cov["payload"].get("key") or {})
        if key.get("relation") == relation and cid not in coverage_ids:
            coverage_ids.append(cid)
    coverage_ids = sorted(set(coverage_ids))
    scope_ids = sorted(set(scope_ids))

    def_cites = []
    for d in records.get("deficiencies") or []:
        src = d.get("source")
        if src not in {"enumeration", "native", "import", "execution", "correspondence"}:
            continue  # unknown source is not coerced
        cite = {
            "source": src,
            "cause": d.get("cause") or "unspecified",
            "inputRefs": list(d.get("inputRefs") or []),
        }
        if "subjectId" in d:
            cite["subjectId"] = d["subjectId"]
        if "predicateId" in d:
            cite["predicateId"] = d["predicateId"]
        def_cites.append(cite)

    limitations = list(projection_limitations)
    if not selected_match:
        limitations.append({"kind": "native-evidence-unavailable", "relation": relation, "minResolution": rung})
    for cid, cov in records["coverages"].items():
        payload = cov["payload"]
        key = payload.get("key") or {}
        entry = payload.get("entry") or {}
        # CoverageResultV3: resolutionCompleteness/coverage/deficiency live on entry.
        rc = entry.get("resolutionCompleteness") if isinstance(entry.get("resolutionCompleteness"), dict) else {}
        state = rc.get("state")
        if state == "incomplete":
            limitations.append({
                "kind": "resolution-incomplete",
                "coverageId": cid,
                "resolutionState": "incomplete",
                "relation": key.get("relation") or entry.get("relation"),
                "minResolution": key.get("resolution") or key.get("minResolution") or entry.get("resolution"),
                "attempted": rc.get("attempted"),
                "examinedExhaustive": rc.get("examinedExhaustive"),
            })
        elif state == "partial":
            limitations.append({"kind": "resolution-partial", "coverageId": cid, "resolutionState": "partial"})
        elif state == "not-attempted":
            limitations.append({"kind": "resolution-not-attempted", "coverageId": cid, "resolutionState": "not-attempted"})
        cov_state = entry.get("coverage")
        if cov_state == "partial":
            limitations.append({"kind": "coverage-partial", "coverageId": cid, "coverage": "partial"})
        elif cov_state == "unknown":
            limitations.append({"kind": "coverage-unknown", "coverageId": cid, "coverage": "unknown"})
        if rc.get("examinedExhaustive") is False:
            limitations.append({"kind": "examined-not-exhaustive", "coverageId": cid, "examinedExhaustive": False})
        n = rc.get("unresolvedEdgeCount")
        if n:
            limitations.append({"kind": "unresolved-edge-present", "coverageId": cid, "unresolvedEdgeCount": n})
        if entry.get("deficiency"):
            limitations.append({"kind": "resolution-incomplete" if state == "incomplete" else "coverage-unknown", "coverageId": cid})

    # IncomingSearchV1 of the declared relation when search is not complete.
    for item in records.get("incomingSearches") or []:
        rec = item.get("record") or {}
        if rec.get("relation") != relation:
            continue
        if rec.get("minResolution") not in (None, rung):
            continue
        complete = rec.get("completeSearch") is True and rec.get("coverage") == "complete"
        if not complete:
            limitations.append({
                "kind": "incoming-search-incomplete",
                "incomingSearchDigest": item.get("digest"),
                "relation": rec.get("relation"),
                "minResolution": rec.get("minResolution") or rung,
            })

    # unresolved-edge facts on admitted Run views even when query selects another relation
    for fid, rec in records["facts"].items():
        if rec.get("relation") == "unresolved-edge":
            limitations.append({"kind": "unresolved-edge-present", "factId": fid})

    return {
        "coverageIds": coverage_ids,
        "scopeIds": scope_ids,
        "deficiencyCitations": def_cites,
        "resolutionLimitations": limitations,
    }


def compact_query_result(response: dict) -> dict:
    ctx = response["context"]
    qr = {
        "kind": "query",
        "items": ctx["producedItems"],
        "truncated": ctx["truncated"],
        "completenessMet": ctx["countBasis"] == "exact",
        "advisory": False,
    }
    if ctx.get("nextCursor"):
        qr["nextCursor"] = ctx["nextCursor"]
    return qr


def success_envelope(*, request_id: str, project_id: str | None, response: dict) -> dict:
    term = response.get("termination") or {"class": "success"}
    klass = term.get("class", "success")
    env = {
        "schemaFamily": "opensip.product.envelope",
        "schemaMajor": 3,
        "kind": "query",
        "requestId": request_id,
        "termination": term,
        "exitCode": CLASS_TO_EXIT.get(klass, 0),
        "query": compact_query_result(response),
    }
    if project_id:
        env["projectId"] = project_id
    return env


def execute_graph_query(
    request: dict,
    run: dict | None,
    objects: dict | None,
    blobs: dict | None,
    host: dict | None,
    close_run: Callable[..., Any] | None = None,
) -> dict:
    """Public wrapper. Signature matches contract §8. Does not seal a Run."""
    host = host or {}
    request_id = _host_request_id(host)
    # Ignore host.cache / standing / targetAttributions / evaluationDeficiencies (contract §8 step 4).
    _ignored = {
        "cache": "cache" in host,
        "standing": "standing" in host,
        "targetAttributions": "targetAttributions" in host,
        "evaluationDeficiencies": "evaluationDeficiencies" in host,
    }
    try:
        availability_refuse(host)
        admit_request(request)
        if close_run is None or run is None:
            raise QueryRefusal(
                "QUERY.VIEW_UNKNOWN",
                "execute_graph_query requires close_run of retained Run bytes; a standalone edge walk is not retained Run admission",
                klass="request-rejected",
                error_code="IDENTITY.UNKNOWN",
            )
        try:
            closed = close_run(run, objects=objects, blobs=blobs)
        except TypeError:
            closed = close_run(run, objects, blobs)
        except QueryRefusal:
            raise
        except AdmissionError as e:
            raise _map_close_run_error(e) from e
        except KeyError as e:
            raise QueryRefusal("evidence.missing", str(e), klass="operational-failed", error_code="HOST.IO_FAILURE", extra={"faultCause": "host-io"}) from e
        if not isinstance(closed, dict) or "records" not in closed:
            raise QueryRefusal(
                "QUERY.VIEW_UNKNOWN",
                "close_run did not return an admitted selected closure; a boolean/synthetic success flag is not public graph evidence",
                klass="request-rejected",
                error_code="IDENTITY.UNKNOWN",
            )
        records = closed["records"]
        run_body = closed.get("runBody") or records.get("runBody")
        if not isinstance(run_body, dict):
            raise QueryRefusal("QUERY.VIEW_UNKNOWN", "admitted closure missing run body", klass="request-rejected", error_code="IDENTITY.UNKNOWN")
        run_id = closed.get("runId") or run["runId"]
        admitted = {
            "runId": run_id,
            "snapshotId": run_body["snapshotId"],
            "projectId": run_body["projectId"],
        }
        if request.get("projectId") != admitted["projectId"]:
            raise QueryRefusal("QUERY.VIEW_UNKNOWN", "projectId != admitted Run project", klass="request-rejected", error_code="IDENTITY.UNKNOWN")
        resolved = join_view(request=request, admitted_run=admitted, host=host)
        params = request["params"]
        rel, rung = params["relation"], params["minResolution"]
        if (rel, rung) not in GRAPH_PROJECTABLE:
            raise QueryRefusal("QUERY.RELATION_UNSUPPORTED", f"{rel}@{rung} is not graph-projectable", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")

        admitted_view_ids = list(closed.get("admittedViewIds") or records.get("admittedViewIds") or records["views"])
        explicit = params.get("factViewDigests")
        if explicit is not None:
            for d in explicit:
                if d not in records["views"]:
                    raise QueryRefusal("QUERY.FACT_VIEW_UNAVAILABLE", "view2 not admitted on this Run", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
            selected = list(explicit)
        else:
            selected = [vid for vid in admitted_view_ids if view_matches_relation(records["views"][vid], records["facts"], records["coverages"], rel, rung)]
        selected_match = any(view_matches_relation(records["views"][vid], records["facts"], records["coverages"], rel, rung) for vid in selected)

        edges, proj_lim, _ = project_from_closure(records=records, relation=rel, rung=rung, selected_view_ids=selected)
        default_uni = None
        for rec in records["facts"].values():
            default_uni = rec.get("sourceUniverse")
            break
        invs = []
        for inv in records["inventories"]:
            uni = inv.get("universe") or universe_for_inventory(inv, records.get("enumPlan"))
            invs.append({**inv, "universe": uni})
        verts = vertex_domain(inventories=invs, edges=edges, default_universe=None)

        bounds = dict(PUBLIC_BOUNDS)
        test_bounds = host.get("testBounds") or {}
        for k in ("maxVisitedNodes", "maxItemsPerOperation"):
            if k in test_bounds and isinstance(test_bounds[k], int) and 1 <= test_bounds[k] <= bounds[k]:
                bounds[k] = test_bounds[k]
        op = request["operation"]
        size = _page_size(request, bounds)
        page = request.get("page") or {}
        include_start = params.get("includeStart", False)
        eff_params = dict(params)
        if op == "graph.reach" and "includeStart" not in params:
            eff_params["includeStart"] = False
        bind = operational_bind(
            project_id=admitted["projectId"],
            run_id=resolved["runId"],
            fact_view_digests=selected,
            operation=op,
            params=eff_params,
        )
        position = 0
        if page.get("cursor"):
            cur = parse_cursor(page["cursor"])
            if cur["runHex"] != resolved["runId"].split(":")[-1]:
                raise QueryRefusal("QUERY.CURSOR_MISMATCH", "continuation runId != bound Run", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
            req_view = request.get("view") or {}
            if req_view.get("runId") != resolved["runId"]:
                raise QueryRefusal("QUERY.CURSOR_MISMATCH", "continuation requires view.runId equal to the bound Run", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
            if cur["selection"] != bind:
                raise QueryRefusal("QUERY.CURSOR_MISMATCH", "selection bind mismatch", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
            position = cur["position"]

        items: list = []
        visited = 1
        truncated_bound = False
        direction = params.get("direction", "outgoing")
        if op == "graph.neighbors":
            ep = admit_endpoint(params["endpoint"], verts)
            items = neighbors_rows(edges=edges, endpoint=ep, direction=direction)
            visited = 1
        elif op == "graph.path":
            start = admit_endpoint(params["start"], verts)
            target = admit_endpoint(params["target"], verts)
            path, meta = visit_capped_path(edges=edges, start=start, target=target, max_depth=params["maxDepth"], max_visited=bounds["maxVisitedNodes"], direction=direction)
            visited = meta["visitedNodes"]
            truncated_bound = meta["truncatedBound"] and path is None
            items = [path] if path is not None else []
        else:
            start = admit_endpoint(params["start"], verts)
            rows, meta = visit_capped_reach(
                edges=edges, start=start, max_depth=params["maxDepth"], max_visited=bounds["maxVisitedNodes"],
                include_start=include_start, direction=direction,
            )
            items = rows
            visited = meta["visitedNodes"]
            truncated_bound = meta["truncatedBound"]
        produced_all = items
        if len(produced_all) > bounds["maxItemsPerOperation"]:
            produced_all = produced_all[: bounds["maxItemsPerOperation"]]
            truncated_bound = True
        page_slice, nxt_pos = page_items(produced_all, size=size, position=position)
        next_cursor = None
        traversal = "complete"
        truncated = False
        count_basis = "exact"
        if truncated_bound:
            traversal = "truncated-bound"
            truncated = True
            count_basis = "lower-bound"
        elif nxt_pos is not None:
            traversal = "truncated-page"
            truncated = False
            next_cursor = cursor_token(run_id=resolved["runId"], selection=bind, position=int(nxt_pos))
            count_basis = "exact"
        evidence = disclose_evidence(
            records=records, selected_view_ids=selected, relation=rel, rung=rung,
            projection_limitations=proj_lim, selected_match=selected_match,
        )
        ctx = {
            "projectId": admitted["projectId"],
            "resolvedView": {"runId": resolved["runId"]},
            "factViewDigests": selected,
            "availability": host.get("availability") or "retained",
            "truncated": truncated,
            "totalItems": len(produced_all),
            "countBasis": count_basis,
            "traversalCoverage": traversal,
            "visitedNodes": visited,
            "producedItems": len(page_slice),
            "advisory": False,
            "evidence": evidence,
        }
        if next_cursor:
            ctx["nextCursor"] = next_cursor
        response = {
            "schemaFamily": "opensip.product.query",
            "schemaMajor": 3,
            "operation": op,
            "context": ctx,
            "items": page_slice,
        }
        if truncated_bound and request.get("completeness") == "required":
            response["termination"] = {
                "class": "indeterminate",
                "reasonCodes": ["QUERY.COMPLETENESS_UNMET"],
                "runId": resolved["runId"],
            }
        env = success_envelope(
            request_id=request_id,
            project_id=_admitted_project_id(request.get("projectId")),
            response=response,
        )
        if response.get("termination") is not None and env["termination"] != response["termination"]:
            raise RuntimeError("response termination must equal enclosing envelope termination")
        parity = render_parity(response, ["human", "json", "agent"], termination=env["termination"])
        qr = env["query"]
        if qr.get("nextCursor") != ctx.get("nextCursor"):
            raise RuntimeError("QueryResult.nextCursor must equal context token")
        if qr["truncated"] != ctx["truncated"] or qr["completenessMet"] != (ctx["countBasis"] == "exact"):
            raise RuntimeError("QueryResult compact summary join failed")
        if qr["items"] != ctx["producedItems"] or qr["advisory"] is not False:
            raise RuntimeError("QueryResult items/advisory join failed")
        return {
            "ok": True,
            "kind": "query",
            "response": response,
            "envelope": env,
            "parity": parity,
            "requestId": request_id,
            "didNotSealRun": True,
            "ignoredHost": _ignored,
        }
    except QueryRefusal as e:
        env = e.envelope(request_id=request_id, project_id=_admitted_project_id(request.get("projectId") if isinstance(request, dict) else None))
        if "run" in env:
            raise RuntimeError("query failure envelope must not carry run")
        if env.get("kind") != "failure" or not env.get("errors"):
            raise RuntimeError("failure envelope composition")
        return {"ok": False, "kind": "failure", "response": None, "envelope": env, "requestId": request_id, "didNotSealRun": True, "refusal": e.as_dict()}


def traverse_projected_graph(*, edges: list[dict], operation: str, params: dict, max_visited: int = 1000000) -> dict:
    """Algorithm goldens over already-projected edges. Not Run admission."""
    if operation == "graph.neighbors":
        return {"items": neighbors_rows(edges=edges, endpoint=params["endpoint"], direction=params["direction"]), "label": "algorithmic"}
    if operation == "graph.path":
        path, meta = visit_capped_path(
            edges=edges, start=params["start"], target=params["target"],
            max_depth=params["maxDepth"], max_visited=max_visited, direction=params.get("direction", "outgoing"),
        )
        return {"items": [path] if path else [], "meta": meta, "label": "algorithmic"}
    rows, meta = visit_capped_reach(
        edges=edges, start=params["start"], max_depth=params["maxDepth"], max_visited=max_visited,
        include_start=params.get("includeStart", False), direction=params.get("direction", "outgoing"),
    )
    return {"items": rows, "meta": meta, "label": "algorithmic"}
