"""Graph query reconstruction from query-projection-contract.v3.md §§1–8."""
from __future__ import annotations

import hashlib
import json
from collections import deque
from typing import Any

from helpers.canonical import C, sha256_hex
from helpers.store import Store

PROJECTABLE = {
    ("calls", "resolved-callee"): {
        "sourceField": "caller",
        "sourceKind": "symbol",
        "targetField": "resolvedCallee",
        "targetKinds": ["symbol"],
        "universe": "admitted-target",
    },
    ("references", "resolved-binding"): None,  # unused here
    ("imports", "resolved-target"): None,
    ("control-flow", "syntactic"): None,
    ("reachability", "from-resolved-calls"): None,
}

MAX_PAGE = 1000
DEFAULT_PAGE = 100
MAX_ITEMS = 100000
MAX_DEPTH = 64
MAX_VISITED = 1000000


def _endpoint_key(e: dict) -> tuple:
    return (
        e.get("universe") or "",
        e.get("kind") or "",
        e.get("nativeSubjectId") or "",
        e.get("packageManifestPath") or "",
    )


def _end_obj(universe, kind, native, pkg=None):
    o = {"universe": universe, "kind": kind, "nativeSubjectId": native}
    if pkg is not None:
        o["packageManifestPath"] = pkg
    return o


def project_edges(store: Store, view_ids: list[str], relation: str, rung: str) -> tuple[list[dict], list[dict]]:
    edges = []
    limitations = []
    spec = PROJECTABLE.get((relation, rung))
    if spec is None and (relation, rung) not in PROJECTABLE:
        return [], [{"kind": "relation-unsupported", "relation": relation, "minResolution": rung}]
    # collect facts from views
    fact_ids = []
    for vid in view_ids:
        v = store.objects[vid]["descriptor"]
        fact_ids.extend(v["facts"])
    for fid in fact_ids:
        f = store.objects[fid]["descriptor"]
        if f["relation"] != relation:
            continue
        if f["resolution"] != rung:
            limitations.append({"kind": "unsupported-rung-omitted", "factId": fid})
            continue
        payload = json.loads(store.blobs[f["payloadDigest"]])
        if relation == "calls":
            if "resolvedCallee" not in payload:
                limitations.append({"kind": "unprojectable-fact", "factId": fid})
                continue
            src = _end_obj(f["sourceUniverse"], "symbol", payload["caller"])
            tgt = _end_obj(f["targetUniverse"], "symbol", payload["resolvedCallee"])
            edges.append({"factId": fid, "relation": relation, "resolution": rung, "source": src, "target": tgt, "producerClosure": f["producerClosure"], "confidenceMillionths": f["confidenceMillionths"]})
    return edges, limitations


def neighbor_order_key(row: dict) -> bytes:
    s, t = row["source"], row["target"]
    tup = (
        s["universe"], s["kind"], s["nativeSubjectId"], s.get("packageManifestPath") or "",
        t["universe"], t["kind"], t["nativeSubjectId"], t.get("packageManifestPath") or "",
        row["factId"],
    )
    return ("\x1f".join(tup)).encode("utf-8")


def selection_hash(run_id: str, view_ids: list[str], op: str, params: dict) -> str:
    pre = C({"runId": run_id, "views": sorted(view_ids), "op": op, "params": params})
    return sha256_hex(pre)


def cursor_token(run_id: str, sel: str, pos: int) -> str:
    hexpart = run_id.split(":")[-1]
    return f"q3.{hexpart}.{sel}.{pos}"


def execute(store: Store, run_id: str, request: dict, *, host: dict) -> dict:
    """Return {ok, response?} or {ok:False, envelope}."""
    project = request.get("projectId")
    run = store.objects[run_id]["descriptor"]
    if project != run["projectId"]:
        return _fail("QUERY.VIEW_UNKNOWN", "projectId must equal admitted Run project", host, request)
    view = request.get("view") or {}
    if "runId" in view:
        if view["runId"] != run_id:
            return _fail("QUERY.VIEW_UNKNOWN", "runId must equal admitted Run", host, request)
    elif view.get("latest") is True:
        if host.get("latestRunId") != run_id:
            return _fail("QUERY.VIEW_UNKNOWN", "latestRunId host observation missing or unequal", host, request)
    elif "snapshotId" in view:
        obs = (host.get("runsForSnapshot") or {}).get(view["snapshotId"]) or []
        if not obs:
            return _fail("QUERY.VIEW_UNKNOWN", "missing host.runsForSnapshot observation", host, request)
        if len(set(obs)) > 1:
            return _fail("QUERY.VIEW_AMBIGUOUS", "multiple runs for snapshot", host, request)
        if obs[0] != run_id:
            return _fail("QUERY.VIEW_UNKNOWN", "snapshot observation does not name this Run", host, request)
    else:
        return _fail("QUERY.PARAMS_MALFORMED", "view must be runId, snapshotId, or latest", host, request)

    op = request.get("operation")
    params = request.get("params") or {}
    if op not in ("graph.neighbors", "graph.path", "graph.reach"):
        return _fail("QUERY.PARAMS_MALFORMED", "not a graph operation in this reconstruction", host, request)
    rel = params.get("relation")
    rung = params.get("minResolution")
    if (rel, rung) not in {("calls", "resolved-callee"), ("references", "resolved-binding"), ("imports", "resolved-target"), ("control-flow", "syntactic"), ("reachability", "from-resolved-calls")}:
        return _fail("QUERY.RELATION_UNSUPPORTED", f"{rel}@{rung} is not graph-projectable", host, request)

    # fact views
    run_views = [oid for oid, o in store.objects.items() if o["domain"] == "view" and o["descriptor"]["planId"] == run["planId"]]
    explicit = params.get("factViewDigests")
    if explicit:
        selected = []
        for d in explicit:
            vid = d if d.startswith("view2:") else f"view2:{d}"
            if vid not in run_views:
                return _fail("QUERY.FACT_VIEW_UNAVAILABLE", f"{d} not a view of this Run", host, request)
            selected.append(vid)
    else:
        selected = []
        for vid in run_views:
            scopes = store.objects[vid]["descriptor"]["scopeIds"]
            for sid in scopes:
                sc = store.objects[sid]["descriptor"]
                if sc["relation"] == rel and sc["resolution"] == rung:
                    selected.append(vid)
                    break

    edges, lims = project_edges(store, selected, rel, rung)
    page = request.get("page") or {"size": DEFAULT_PAGE}
    size = min(int(page.get("size") or DEFAULT_PAGE), MAX_PAGE)
    start_pos = 0
    if page.get("cursor"):
        cur = page["cursor"]
        parts = cur.split(".")
        if len(parts) != 4 or parts[0] != "q3":
            return _fail("QUERY.CURSOR_MISMATCH", "malformed cursor", host, request)
        if parts[1] != run_id.split(":")[-1]:
            return _fail("QUERY.CURSOR_MISMATCH", "cursor bound to a different Run", host, request)
        start_pos = int(parts[3])

    evidence = {
        "coverageIds": [],
        "scopeIds": [],
        "deficiencyCitations": [],
        "resolutionLimitations": lims,
    }
    for vid in selected:
        v = store.objects[vid]["descriptor"]
        evidence["coverageIds"].extend(v["coverageIds"])
        evidence["scopeIds"].extend(v["scopeIds"])
    evidence["coverageIds"] = sorted(set(evidence["coverageIds"]))
    evidence["scopeIds"] = sorted(set(evidence["scopeIds"]))
    if not selected:
        evidence["resolutionLimitations"].append({"kind": "native-evidence-unavailable", "relation": rel, "minResolution": rung})

    if op == "graph.neighbors":
        ep = params.get("endpoint") or {}
        if not isinstance(ep, dict) or ep.get("kind") not in ("file", "symbol", "package"):
            return _fail("QUERY.PARAMS_MALFORMED", "malformed endpoint", host, request)
        direction = params.get("direction", "outgoing")
        rows = []
        for e in edges:
            if direction in ("outgoing", "both") and _endpoint_key(e["source"]) == _endpoint_key(ep):
                rows.append(e)
            if direction in ("incoming", "both") and _endpoint_key(e["target"]) == _endpoint_key(ep):
                # reverse display? contract: incoming follows reverse; row still has source/target of the fact
                rows.append(e)
        # unique by factId
        by_f = {r["factId"]: r for r in rows}
        rows = sorted(by_f.values(), key=neighbor_order_key)
        visited = 1
        items = rows[start_pos : start_pos + size]
        produced = start_pos + len(items)
        total = len(rows)
        nxt = None
        trav = "complete"
        truncated = False
        if produced < total:
            nxt = cursor_token(run_id, selection_hash(run_id, selected, op, params), produced)
            if produced >= MAX_ITEMS:
                trav = "truncated-bound"
                truncated = True
            else:
                trav = "truncated-page"
                truncated = False
        resp = _ok(op, run, run_id, selected, items, evidence, total, "exact" if trav == "complete" else "lower-bound", trav, visited, len(items), truncated, nxt)
        return {"ok": True, "response": resp, "classification": "valid"}

    # path / reach BFS
    start = params.get("start") or params.get("endpoint")
    max_depth = int(params.get("maxDepth", 1))
    direction = params.get("direction", "outgoing")
    adj: dict[tuple, list[tuple[dict, dict]]] = {}
    for e in sorted(edges, key=lambda r: r["factId"].encode()):
        if direction in ("outgoing", "both"):
            adj.setdefault(_endpoint_key(e["source"]), []).append((e["target"], e))
        if direction in ("incoming", "both"):
            adj.setdefault(_endpoint_key(e["target"]), []).append((e["source"], e))
        if direction == "both":
            # undirected already added both ways
            pass

    if op == "graph.path":
        target = params.get("target")
        if _endpoint_key(start) == _endpoint_key(target):
            items = [{"hopCount": 0, "start": start, "target": target, "nodes": [start], "edges": []}]
            resp = _ok(op, run, run_id, selected, items, evidence, 1, "exact", "complete", 1, 1, False, None)
            return {"ok": True, "response": resp, "classification": "valid"}
        # BFS
        q = deque([(start, [], 0)])
        seen = {_endpoint_key(start)}
        visited = 1
        found = None
        while q:
            node, path_edges, depth = q.popleft()
            if depth >= max_depth:
                continue
            hops = sorted(adj.get(_endpoint_key(node), []), key=lambda x: x[1]["factId"].encode())
            for nxt_ep, edge in hops:
                k = _endpoint_key(nxt_ep)
                if k in seen:
                    continue
                if visited >= MAX_VISITED:
                    resp = _ok(op, run, run_id, selected, [], evidence, 0, "lower-bound", "truncated-bound", visited, 0, True, None)
                    return {"ok": True, "response": resp, "classification": "valid"}
                seen.add(k)
                visited += 1
                new_path = path_edges + [edge]
                if k == _endpoint_key(target):
                    found = new_path
                    break
                q.append((nxt_ep, new_path, depth + 1))
            if found is not None:
                break
        items = []
        if found is not None:
            nodes = [start]
            for e in found:
                nodes.append(e["target"] if _endpoint_key(e["source"]) == _endpoint_key(nodes[-1]) else e["source"])
            items = [{
                "hopCount": len(found),
                "start": start,
                "target": target,
                "nodes": nodes,
                "edges": [{"factId": e["factId"], "source": e["source"], "target": e["target"]} for e in found],
            }]
        resp = _ok(op, run, run_id, selected, items, evidence, len(items), "exact", "complete", visited, len(items), False, None)
        return {"ok": True, "response": resp, "classification": "valid"}

    # reach
    include_start = bool(params.get("includeStart", False))
    q = deque([(start, 0, None)])
    seen = {_endpoint_key(start)}
    visited = 1
    rows = []
    if include_start:
        rows.append({"endpoint": start, "depth": 0})
    while q:
        node, depth, _via = q.popleft()
        if depth >= max_depth:
            continue
        hops = sorted(adj.get(_endpoint_key(node), []), key=lambda x: x[1]["factId"].encode())
        for nxt_ep, edge in hops:
            k = _endpoint_key(nxt_ep)
            if k in seen:
                continue
            if visited >= MAX_VISITED:
                break
            seen.add(k)
            visited += 1
            rows.append({"endpoint": nxt_ep, "depth": depth + 1, "viaFactId": edge["factId"]})
            q.append((nxt_ep, depth + 1, edge["factId"]))
    rows = sorted(rows, key=lambda r: _endpoint_key(r["endpoint"]))
    items = rows[start_pos : start_pos + size]
    total = len(rows)
    produced = start_pos + len(items)
    nxt = cursor_token(run_id, selection_hash(run_id, selected, op, params), produced) if produced < total else None
    trav = "complete" if nxt is None else "truncated-page"
    resp = _ok(op, run, run_id, selected, items, evidence, total, "exact" if trav == "complete" else "lower-bound", trav, visited, len(items), False, nxt)
    return {"ok": True, "response": resp, "classification": "valid"}


def _ok(op, run, run_id, selected, items, evidence, total, basis, trav, visited, produced, truncated, nxt):
    ctx = {
        "projectId": run["projectId"],
        "resolvedView": {"runId": run_id},
        "factViewDigests": sorted(selected),
        "availability": "retained",
        "truncated": truncated,
        "totalItems": total,
        "countBasis": basis,
        "traversalCoverage": trav,
        "visitedNodes": visited,
        "producedItems": produced,
        "advisory": False,
        "evidence": evidence,
    }
    if nxt:
        ctx["nextCursor"] = nxt
    return {
        "schemaFamily": "opensip.product.query",
        "schemaMajor": 3,
        "operation": op,
        "context": ctx,
        "items": items,
    }


def _fail(code: str, remedy: str, host: dict, request: dict) -> dict:
    rid = host.get("requestId")
    env = {
        "schemaFamily": "opensip.product.envelope",
        "schemaMajor": 3,
        "kind": "failure",
        "requestId": rid,
        "termination": {
            "class": "request-rejected",
            "errorCode": "REQUEST.PRECONDITION_FAILED",
            "domainDetail": {"code": code, "remedy": remedy},
        },
        "exitCode": 2,
        "errors": [{"code": code, "remedy": remedy}],
    }
    if request.get("projectId") and str(request.get("projectId")).startswith("prj1-"):
        env["projectId"] = request["projectId"]
    return {"ok": False, "envelope": env, "classification": "invalid", "firstRefusal": {"code": code, "remedy": remedy}, "masksLater": True}
