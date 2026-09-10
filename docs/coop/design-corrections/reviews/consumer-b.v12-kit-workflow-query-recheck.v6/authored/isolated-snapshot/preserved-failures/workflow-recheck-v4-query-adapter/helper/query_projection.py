"""Query projection contract v3 — reusable reference reconstruction.

Public execute_graph_query requires close_run of retained Run bytes.
traverse_projected_graph is algorithmic only (caller-authored edges).
Does not mint a Run. Does not invent a published selectionHash identity recipe:
cursor binding uses an operational digest of independently re-admitted params.
"""
from __future__ import annotations

from collections import deque
from typing import Any, Callable

from helper.canonical import C
from helper.errors import AdmissionError
from helper.identity import H
from helper.workflow_laws import (
    GRAPH_PROJECTABLE,
    cursor_token,
    endpoint_key,
    page_items,
    project_edges,
    raw_sha256_c,
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


class QueryRefusal(AdmissionError):
    def __init__(self, code: str, message: str, *, klass: str, error_code: str, extra=None):
        super().__init__(code, message, extra=extra)
        self.klass = klass
        self.error_code = error_code

    def envelope(self, *, request_id: str, project_id: str | None = None) -> dict:
        term = {"class": self.klass, "errorCode": self.error_code, "domainDetail": {"code": self.code, "remedy": self.message}}
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
    return rid


def _page_size(request: dict, bounds: dict) -> int:
    page = request.get("page") or {}
    size = page.get("size", bounds["defaultPageSize"])
    if not isinstance(size, int) or size < 1 or size > bounds["maxPageSize"]:
        raise QueryRefusal("QUERY.PARAMS_MALFORMED", "page.size out of bounds", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
    return size


def admit_request(request: dict) -> None:
    if not isinstance(request, dict):
        raise QueryRefusal("QUERY.PARAMS_MALFORMED", "request not an object", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
    if request.get("schemaFamily") != "opensip.product.query":
        raise QueryRefusal("QUERY.PARAMS_MALFORMED", "schemaFamily", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
    if request.get("schemaMajor") != 3:
        raise QueryRefusal("QUERY.SCHEMA_MAJOR_UNSUPPORTED", "schemaMajor must be 3", klass="request-rejected", error_code="REQUEST.SCHEMA_MAJOR_UNSUPPORTED")
    if request.get("operation") not in ("graph.neighbors", "graph.path", "graph.reach"):
        raise QueryRefusal("QUERY.PARAMS_MALFORMED", "not a graph operation in this reconstruction", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
    params = request.get("params") or {}
    if not isinstance(params, dict):
        raise QueryRefusal("QUERY.PARAMS_MALFORMED", "params", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
    extra = set(params) - {
        "relation", "minResolution", "direction", "endpoint", "start", "target",
        "maxDepth", "includeStart", "factViewDigests",
    }
    if extra:
        raise QueryRefusal("QUERY.PARAMS_MALFORMED", f"extra params {sorted(extra)}", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
    for key in ("endpoint", "start", "target"):
        ep = params.get(key)
        if ep is None:
            continue
        if not isinstance(ep, dict):
            raise QueryRefusal("QUERY.PARAMS_MALFORMED", f"{key} not object", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
        if "logicalPath" in ep or "path" in ep and "universe" not in ep:
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
    if start == target:
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
            if nxt == target:
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
    out = []
    for e in edges:
        if direction in ("outgoing", "both") and e["source"] == endpoint:
            out.append(e)
        if direction in ("incoming", "both") and e["target"] == endpoint:
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


def vertex_domain(*, inventories: list[dict], edges: list[dict], universe: str | None = None) -> list[dict]:
    verts = []
    seen = set()
    for inv in inventories:
        kind = inv.get("kind")
        u = inv.get("universe") or universe
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
    matches = [v for v in vertices if v["universe"] == ep["universe"] and v["kind"] == ep["kind"] and v["nativeSubjectId"] == ep["nativeSubjectId"]]
    if ep.get("kind") == "package":
        pmp = ep.get("packageManifestPath")
        if not pmp:
            if len(matches) > 1:
                raise QueryRefusal("QUERY.ENDPOINT_AMBIGUOUS", "package identity without packageManifestPath", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
        else:
            matches = [v for v in matches if v.get("packageManifestPath") == pmp]
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


def execute_graph_query(
    request: dict,
    *,
    run: dict | None,
    objects: dict | None,
    blobs: dict | None,
    host: dict | None,
    close_run: Callable[..., Any] | None = None,
    projected_edges: list[dict] | None = None,
    inventories: list[dict] | None = None,
    coverage_ids: list[str] | None = None,
    scope_ids: list[str] | None = None,
    fact_view_digests: list[str] | None = None,
    limitations: list[dict] | None = None,
) -> dict:
    """Public wrapper. close_run is required. Query does not seal a Run."""
    host = host or {}
    request_id = _host_request_id(host)
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
        close_run(run, objects=objects, blobs=blobs)
        admitted = {"runId": run["runId"], "snapshotId": run["snapshotId"], "projectId": run["projectId"]}
        if request.get("projectId") != admitted["projectId"]:
            raise QueryRefusal("QUERY.VIEW_UNKNOWN", "projectId != admitted Run project", klass="request-rejected", error_code="IDENTITY.UNKNOWN")
        resolved = join_view(request=request, admitted_run=admitted, host=host)
        params = request["params"]
        rel, rung = params["relation"], params["minResolution"]
        if (rel, rung) not in GRAPH_PROJECTABLE:
            raise QueryRefusal("QUERY.RELATION_UNSUPPORTED", f"{rel}@{rung} is not graph-projectable", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
        bounds = dict(PUBLIC_BOUNDS)
        test_bounds = host.get("testBounds") or {}
        for k in ("maxVisitedNodes", "maxItemsPerOperation"):
            if k in test_bounds and isinstance(test_bounds[k], int) and 1 <= test_bounds[k] <= bounds[k]:
                bounds[k] = test_bounds[k]
        views = fact_view_digests or []
        explicit = params.get("factViewDigests")
        if explicit is not None:
            for d in explicit:
                if d not in views:
                    raise QueryRefusal("QUERY.FACT_VIEW_UNAVAILABLE", "view2 not admitted on this Run", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
            views = list(explicit)
        edges = list(projected_edges or [])
        verts = vertex_domain(inventories=inventories or [], edges=edges)
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
            fact_view_digests=views,
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
        native_unavail = not edges and not any(True for _ in views)
        items: list = []
        visited = 1
        truncated_bound = False
        if op == "graph.neighbors":
            ep = admit_endpoint(params["endpoint"], verts)
            items = neighbors_rows(edges=edges, endpoint=ep, direction=params["direction"])
            visited = 1
        elif op == "graph.path":
            start = admit_endpoint(params["start"], verts)
            target = admit_endpoint(params["target"], verts)
            max_depth = params["maxDepth"]
            if max_depth > bounds["maxTraversalDepth"]:
                raise QueryRefusal("QUERY.PARAMS_MALFORMED", "maxDepth", klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED")
            path, meta = visit_capped_path(edges=edges, start=start, target=target, max_depth=max_depth, max_visited=bounds["maxVisitedNodes"], direction=params["direction"])
            visited = meta["visitedNodes"]
            truncated_bound = meta["truncatedBound"] and path is None
            items = [path] if path is not None else []
        else:
            start = admit_endpoint(params["start"], verts)
            max_depth = params["maxDepth"]
            rows, meta = visit_capped_reach(
                edges=edges, start=start, max_depth=max_depth, max_visited=bounds["maxVisitedNodes"],
                include_start=include_start, direction=params.get("direction", "outgoing"),
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
        lim = list(limitations or [])
        if native_unavail or (not edges and (rel, rung) in GRAPH_PROJECTABLE):
            lim.append({"kind": "native-evidence-unavailable", "relation": rel, "resolution": rung})
        ctx = {
            "projectId": admitted["projectId"],
            "resolvedView": {"runId": resolved["runId"]},
            "factViewDigests": views,
            "availability": host.get("availability") or "retained",
            "truncated": truncated,
            "totalItems": len(produced_all),
            "countBasis": count_basis,
            "traversalCoverage": traversal,
            "visitedNodes": visited,
            "producedItems": len(page_slice),
            "advisory": False,
            "evidence": {
                "coverageIds": list(coverage_ids or []),
                "scopeIds": list(scope_ids or []),
                "deficiencyCitations": [],
                "resolutionLimitations": lim,
            },
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
            response["termination"] = {"class": "indeterminate", "reasonCodes": ["QUERY.COMPLETENESS_UNMET"]}
        return {"ok": True, "kind": "success", "response": response, "envelope": None, "requestId": request_id, "didNotSealRun": True, "ignoredHostCache": "cache" in host}
    except QueryRefusal as e:
        env = e.envelope(request_id=request_id, project_id=request.get("projectId") if isinstance(request.get("projectId"), str) and str(request.get("projectId")).startswith("prj1-") else None)
        if "run" in env:
            raise RuntimeError("query failure envelope must not carry run")
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
