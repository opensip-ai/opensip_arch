"""Bounded graph query admission/projection/traversal/cursor. Not a product query engine.

Strong public wrapper execute_graph_query requires an actual retained Run and
closed fact-view admission via identity-model.v3.close_run. Caller-authored
edges are refused unless host.standing is exactly synthetic-admitted-fact-graph
(algorithm goldens only). Native/atom remain owners of absence.

Does not seal a Run, invoke a provider, change storage generations, or mint
negative proof. Public bound constants are schema Bounds; host.testBounds may
only lower visited/produced caps for reference controls.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import re
import sys
from collections import deque
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "foundation"))
import canonical  # noqa: E402
from jsonschema import ValidationError  # noqa: E402
from referencing import Registry, Resource  # noqa: E402
from referencing.jsonschema import DRAFT202012  # noqa: E402

PUBLIC_BOUNDS = {
    "maxPageSize": 1000,
    "defaultPageSize": 100,
    "maxItemsPerOperation": 100000,
    "maxTraversalDepth": 64,
    "maxVisitedNodes": 1000000,
}
GRAPH_OPS = frozenset({"graph.neighbors", "graph.path", "graph.reach"})
ADVISORY_OPS = frozenset({"comparison.diff", "candidate.list", "inspection.show", "review.brief"})
STORED_KINDS = frozenset({"file", "symbol", "package"})
AVAIL_DETAIL = {
    "purged": "evidence.purged",
    "expired": "evidence.expired",
    "corrupt": "evidence.corrupt",
    "unavailable": "evidence.missing",
    "missing": "evidence.missing",
}
CURSOR_RE = re.compile(r"^q3\.([0-9a-f]{64})\.([0-9a-f]{64})\.([0-9]+)$")
SCHEMA_ID = "urn:opensip:product-v1:workflows:evaluator3:graph-query:3"
COMMON_ID = "urn:opensip:product-v1:workflows:evaluator3:common:3"
SYNTHETIC_STANDING = "synthetic-admitted-fact-graph"
_ID3 = None
_REG = None
_TABLE = None


class QueryRefusal(Exception):
    """Public graph-query refusal. termination() is an admitted StepTermination envelope."""

    def __init__(
        self,
        error_code,
        detail=None,
        remedy="see query-projection-contract.v3.md",
        subject=None,
        *,
        klass="request-rejected",
        fault_cause=None,
        run_id=None,
    ):
        super().__init__(error_code)
        self.error_code = error_code
        self.detail = detail
        self.remedy = remedy
        self.subject = subject
        self.klass = klass
        self.fault_cause = fault_cause
        self.run_id = run_id

    def termination(self):
        term = {"class": self.klass}
        if self.klass in ("request-rejected", "operational-failed"):
            term["errorCode"] = self.error_code
        if self.klass == "operational-failed":
            term["faultCause"] = self.fault_cause or "host-io"
        if self.klass == "indeterminate":
            term["reasonCodes"] = [self.error_code]
        if self.detail:
            body = {"code": self.detail, "remedy": self.remedy[:1024]}
            if self.subject is not None:
                body["subject"] = str(self.subject)[:1024]
            term["domainDetail"] = body
        if self.run_id and self.klass != "request-rejected":
            term["runId"] = self.run_id
        return term


def identity3():
    global _ID3
    if _ID3 is None:
        spec = importlib.util.spec_from_file_location(
            "query_identity3", HERE.parent / "foundation" / "identity-model.v3.py"
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _ID3 = mod
    return _ID3


def schema_registry():
    global _REG
    if _REG is None:
        schemas = {}
        e3 = HERE / "schemas" / "evaluator3"
        for path in sorted(e3.glob("*.schema.json")):
            doc = json.loads(path.read_text())
            schemas[doc["$id"]] = doc
        wf = HERE / "schemas"
        for name in (
            "common.schema.json",
            "imported-evidence.schema.json",
            "policy-document.schema.json",
            "policy-document.v2.schema.json",
            "test-execution.schema.json",
        ):
            path = wf / name
            if path.exists():
                doc = json.loads(path.read_text())
                schemas[doc["$id"]] = doc
        _REG = Registry().with_resources(
            [(k, Resource(contents=v, specification=DRAFT202012)) for k, v in schemas.items()]
        )
    return _REG


def validate_schema(ref, value):
    canonical.typed(value)
    canonical.ExactValidator({"$ref": ref}, registry=schema_registry()).validate(value)
    return value


def projection_table():
    """Binary native-id rungs from the existing evaluator projection registry. No invented edges."""
    global _TABLE
    if _TABLE is None:
        path = HERE.parent / "foundation" / "evaluator-projection-registry.v1.json"
        doc = json.loads(path.read_text())
        table = {}
        for name, spec in doc["relations"].items():
            et = spec.get("endpointTarget")
            if et == "forbidden" or not spec.get("targetNativeIdField"):
                continue
            source_kind = spec.get("sourceSubjectKind")
            if source_kind not in STORED_KINDS:
                continue
            target_kinds = tuple(k for k in (spec.get("targetKinds") or []) if k in STORED_KINDS)
            if not target_kinds:
                continue
            if et == "admitted":
                rungs = list(spec.get("ladder") or [])
            elif et == "admitted-at-rung":
                rungs = list(spec.get("endpointTargetRungs") or [])
            else:
                continue
            target_field = spec.get("targetField") or spec.get("targetNativeIdField")
            for rung in rungs:
                table[(name, rung)] = {
                    "relation": name,
                    "minResolution": rung,
                    "sourceField": spec["sourceField"],
                    "targetField": target_field,
                    "sourceKind": source_kind,
                    "targetKinds": target_kinds,
                    "universeRule": spec.get("universeRule"),
                }
        if not table:
            raise RuntimeError("projection table empty")
        _TABLE = table
    return _TABLE


def endpoint_tuple(ep):
    return (
        ep["universe"],
        ep["kind"],
        ep["nativeSubjectId"],
        ep.get("packageManifestPath") or "",
    )


def endpoint_key(ep):
    return (
        ep["universe"].encode("utf-8"),
        ep["kind"].encode("utf-8"),
        ep["nativeSubjectId"].encode("utf-8"),
        (ep.get("packageManifestPath") or "").encode("utf-8"),
    )


def canonical_endpoint(ep):
    out = {
        "kind": ep["kind"],
        "nativeSubjectId": ep["nativeSubjectId"],
        "universe": ep["universe"],
    }
    if ep["kind"] == "package":
        path = ep.get("packageManifestPath")
        if not path:
            return None
        out["packageManifestPath"] = path
    return out


def endpoints_equal(a, b):
    return endpoint_tuple(a) == endpoint_tuple(b)


def admit_endpoint(ep, label):
    if type(ep) is not dict:
        raise QueryRefusal(
            "REQUEST.PRECONDITION_FAILED",
            "QUERY.ENDPOINT_AMBIGUOUS",
            "graph endpoint must be universe+kind+nativeSubjectId",
            label,
        )
    if not ep.get("universe") or not ep.get("kind") or not ep.get("nativeSubjectId"):
        raise QueryRefusal(
            "REQUEST.PRECONDITION_FAILED",
            "QUERY.ENDPOINT_AMBIGUOUS",
            "graph endpoint must name universe, kind, and nativeSubjectId; LogicalPath-only is refused",
            label,
        )
    if ep["kind"] not in STORED_KINDS:
        raise QueryRefusal(
            "REQUEST.PRECONDITION_FAILED",
            "QUERY.PARAMS_MALFORMED",
            "endpoint kind is file|symbol|package",
            label,
        )
    if ep["kind"] == "package" and not ep.get("packageManifestPath"):
        raise QueryRefusal(
            "REQUEST.PRECONDITION_FAILED",
            "QUERY.ENDPOINT_AMBIGUOUS",
            "package endpoints require packageManifestPath",
            label,
        )
    if ep["kind"] != "package" and ep.get("packageManifestPath"):
        raise QueryRefusal(
            "REQUEST.PRECONDITION_FAILED",
            "QUERY.PARAMS_MALFORMED",
            "packageManifestPath is only lawful on kind=package",
            label,
        )
    got = canonical_endpoint(ep)
    if got is None:
        raise QueryRefusal(
            "REQUEST.PRECONDITION_FAILED",
            "QUERY.ENDPOINT_AMBIGUOUS",
            "endpoint could not be canonically named",
            label,
        )
    return got


def work_bounds(host):
    bounds = dict(PUBLIC_BOUNDS)
    injected = (host or {}).get("testBounds") or {}
    for key in ("maxVisitedNodes", "maxItemsPerOperation"):
        if key in injected:
            value = injected[key]
            if type(value) is not int or value < 1 or value > bounds[key]:
                raise QueryRefusal(
                    "REQUEST.PRECONDITION_FAILED",
                    "QUERY.PARAMS_MALFORMED",
                    "testBounds may only lower public visited/produced caps",
                    key,
                )
            bounds[key] = value
    return bounds


def selection_hash(project_id, run_id, fact_view_digests, operation, effective_params):
    record = {
        "factViewDigests": sorted(fact_view_digests),
        "operation": operation,
        "params": effective_params,
        "projectId": project_id,
        "runId": run_id,
    }
    return hashlib.sha256(canonical.canonical(record)).hexdigest()


def encode_cursor(run_id, digest, position):
    token = "q3.%s.%s.%d" % (run_id.split(":", 1)[1], digest, position)
    if len(token) > 256:
        raise QueryRefusal(
            "REQUEST.PRECONDITION_FAILED",
            "QUERY.CURSOR_MISMATCH",
            "cursor exceeds 256 characters",
        )
    return token


def decode_cursor(token):
    match = CURSOR_RE.fullmatch(token)
    if not match:
        raise QueryRefusal(
            "REQUEST.PRECONDITION_FAILED",
            "QUERY.CURSOR_MISMATCH",
            "cursor is not a bound q3 token",
        )
    return {
        "runId": "run3:" + match.group(1),
        "selectionHash": match.group(2),
        "position": int(match.group(3)),
    }


def effective_params(operation, params):
    p = copy.deepcopy(params)
    out = {
        "direction": p["direction"],
        "minResolution": p["minResolution"],
        "relation": p["relation"],
    }
    if operation == "graph.neighbors":
        out["endpoint"] = admit_endpoint(p["endpoint"], "endpoint")
    elif operation == "graph.path":
        out["start"] = admit_endpoint(p["start"], "start")
        out["target"] = admit_endpoint(p["target"], "target")
        out["maxDepth"] = p["maxDepth"]
    elif operation == "graph.reach":
        out["start"] = admit_endpoint(p["start"], "start")
        out["maxDepth"] = p["maxDepth"]
        out["includeStart"] = bool(p["includeStart"]) if "includeStart" in p else False
    return out


def _blob_payload(blobs, digest, label):
    raw = blobs.get(digest)
    if raw is None:
        raise QueryRefusal(
            "HOST.IO_FAILURE",
            "evidence.missing",
            "restore the exact retained payload bytes",
            label,
            klass="operational-failed",
            fault_cause="host-io",
        )
    if type(raw) is not bytes:
        raise QueryRefusal(
            "HOST.IO_FAILURE",
            "evidence.corrupt",
            "retained payload is not raw bytes",
            label,
            klass="operational-failed",
            fault_cause="host-io",
        )
    if hashlib.sha256(raw).hexdigest() != digest:
        raise QueryRefusal(
            "HOST.IO_FAILURE",
            "evidence.corrupt",
            "retained payload digest mismatch",
            label,
            klass="operational-failed",
            fault_cause="host-io",
        )
    try:
        return canonical.parse(raw)
    except canonical.AdmissionError as exc:
        raise QueryRefusal(
            "HOST.IO_FAILURE",
            "evidence.corrupt",
            "retained payload is not exact JSON",
            label,
            klass="operational-failed",
            fault_cause="host-io",
        ) from exc


def _object(objects, key, domain, detail="QUERY.FACT_VIEW_UNAVAILABLE"):
    if key not in objects:
        if detail.startswith("evidence."):
            raise QueryRefusal(
                "HOST.IO_FAILURE",
                detail,
                "restore the exact retained closure bytes",
                key,
                klass="operational-failed",
                fault_cause="host-io",
            )
        raise QueryRefusal(
            "REQUEST.PRECONDITION_FAILED",
            detail,
            "selected fact-view or fact is not admitted on this Run",
            key,
        )
    actual, value = objects[key]
    if actual != domain:
        raise QueryRefusal(
            "HOST.IO_FAILURE",
            "evidence.corrupt",
            "retained object domain mismatch",
            key,
            klass="operational-failed",
            fault_cause="host-io",
        )
    return value


def close_retained_run(run, objects, blobs):
    M = identity3()
    try:
        return M.close_run(run, objects, blobs)
    except M.EvidenceUnavailable as exc:
        raise QueryRefusal(
            "HOST.IO_FAILURE",
            "evidence.missing",
            "restore the exact retained closure bytes or report their unavailability",
            getattr(exc, "reference", None),
            klass="operational-failed",
            fault_cause="host-io",
        ) from exc
    except Exception as exc:
        raise QueryRefusal(
            "HOST.IO_FAILURE",
            "evidence.corrupt",
            "retained Run failed closed fact-view admission",
            str(exc)[:200],
            klass="operational-failed",
            fault_cause="host-io",
        ) from exc


def resolve_run_id(request, host, cursor_bind):
    view = request["view"]
    if cursor_bind is not None:
        if "runId" not in view or view["runId"] != cursor_bind["runId"]:
            raise QueryRefusal(
                "REQUEST.PRECONDITION_FAILED",
                "QUERY.CURSOR_MISMATCH",
                "continuation must reuse the bound runId and must not re-resolve latest or snapshot",
            )
        return cursor_bind["runId"]
    if "runId" in view:
        return view["runId"]
    if view.get("latest") is True:
        rid = (host or {}).get("latestRunId")
        if not rid:
            raise QueryRefusal("IDENTITY.UNKNOWN", None, "latest resolver has empty domain")
        return rid
    snap = view.get("snapshotId")
    ids = list(((host or {}).get("runsForSnapshot") or {}).get(snap) or [])
    if len(ids) == 0:
        raise QueryRefusal("IDENTITY.UNKNOWN", None, "snapshot resolver has empty domain")
    if len(ids) > 1:
        raise QueryRefusal(
            "REQUEST.PRECONDITION_FAILED",
            "QUERY.VIEW_AMBIGUOUS",
            "two or more Runs admit this snapshot; name runId",
            snap,
        )
    return ids[0]


def view_matches_relation(view, objects, relation, min_resolution):
    for sid in view.get("scopeIds") or []:
        if sid not in objects:
            continue
        domain, scope = objects[sid]
        if domain != "subject-scope":
            continue
        if scope.get("relation") == relation and scope.get("resolution") == min_resolution:
            return True
    return False


def select_views(evidence_view_ids, objects, params, requested):
    admitted = list(evidence_view_ids)
    if requested:
        missing = [v for v in requested if v not in admitted]
        if missing:
            raise QueryRefusal(
                "REQUEST.PRECONDITION_FAILED",
                "QUERY.FACT_VIEW_UNAVAILABLE",
                "selected view2 is not admitted on this Run",
                missing[0],
            )
        selected = list(requested)
    else:
        selected = []
        for vid in admitted:
            view = _object(objects, vid, "view")
            if view_matches_relation(view, objects, params["relation"], params["minResolution"]):
                selected.append(vid)
    return sorted(set(selected))


def project_fact(fact_id, fact, payload, table, target_attr=None):
    src_field, tgt_field = table["sourceField"], table["targetField"]
    if type(payload) is not dict or src_field not in payload or tgt_field not in payload:
        return None, {"kind": "unprojectable-fact", "factId": fact_id, "note": "payload lacks native endpoint fields"}
    if payload[src_field] in (None, "") or payload[tgt_field] in (None, ""):
        return None, {"kind": "unprojectable-fact", "factId": fact_id, "note": "native endpoint id empty"}
    source = {
        "universe": fact["sourceUniverse"],
        "kind": table["sourceKind"],
        "nativeSubjectId": payload[src_field],
    }
    if table["universeRule"] == "admitted-target":
        target_universe = fact["targetUniverse"]
    else:
        target_universe = fact["sourceUniverse"]
    kinds = table["targetKinds"]
    package_path = None
    if len(kinds) == 1:
        tkind = kinds[0]
    else:
        if not target_attr or target_attr.get("kind") not in kinds:
            return None, {
                "kind": "unprojectable-fact",
                "factId": fact_id,
                "note": "imports target kind requires admitted target-attribution",
            }
        tkind = target_attr["kind"]
        package_path = target_attr.get("packageManifestPath")
    target = {
        "universe": target_universe,
        "kind": tkind,
        "nativeSubjectId": payload[tgt_field],
    }
    if tkind == "package":
        if not package_path:
            return None, {
                "kind": "unprojectable-fact",
                "factId": fact_id,
                "note": "package target missing packageManifestPath",
            }
        target["packageManifestPath"] = package_path
    src = canonical_endpoint(source)
    tgt = canonical_endpoint(target)
    if src is None or tgt is None:
        return None, {"kind": "unprojectable-fact", "factId": fact_id}
    row = {
        "factId": fact_id,
        "relation": fact["relation"],
        "resolution": fact["resolution"],
        "source": src,
        "target": tgt,
        "producerClosure": fact["producerClosure"],
        "confidenceMillionths": fact["confidenceMillionths"],
    }
    return row, None


def collect_projected_edges(selected_views, objects, blobs, table, host, max_visited):
    target_attrs = (host or {}).get("targetAttributions") or {}
    facts = {}
    limitations = []
    coverage_ids = []
    scope_ids = []
    unresolved_present = False
    for vid in selected_views:
        view = _object(objects, vid, "view")
        coverage_ids.extend(view.get("coverageIds") or [])
        scope_ids.extend(view.get("scopeIds") or [])
        for fid in view.get("facts") or []:
            if fid not in facts:
                facts[fid] = vid
    ordered = sorted(facts)
    projected = []
    visited = 0
    truncated = False
    for fid in ordered:
        if visited >= max_visited:
            truncated = True
            limitations.append({"kind": "unexamined-work-bound", "note": "maxVisitedNodes stopped fact examination"})
            break
        visited += 1
        fact = _object(objects, fid, "fact", "evidence.missing")
        payload = _blob_payload(blobs, fact["payloadDigest"], fid)
        if fact.get("relation") == "unresolved-edge":
            unresolved_present = True
            limitations.append({"kind": "unresolved-edge-present", "factId": fid})
            continue
        key = (fact.get("relation"), fact.get("resolution"))
        if key != (table["relation"], table["minResolution"]):
            if fact.get("relation") == table["relation"]:
                limitations.append({"kind": "unsupported-rung-omitted", "factId": fid})
            continue
        row, limitation = project_fact(fid, fact, payload, table, target_attrs.get(fid))
        if limitation:
            limitations.append(limitation)
            continue
        projected.append(row)
    if unresolved_present is False:
        pass
    return projected, visited, truncated, limitations, sorted(set(coverage_ids)), sorted(set(scope_ids))


def coverage_limitations(coverage_ids, objects, blobs):
    out = []
    for cid in coverage_ids:
        if cid not in objects:
            out.append({"kind": "coverage-unknown", "coverageId": cid, "note": "coverage object not retained"})
            continue
        domain, cov = objects[cid]
        if domain != "coverage":
            out.append({"kind": "coverage-unknown", "coverageId": cid})
            continue
        try:
            payload = _blob_payload(blobs, cov["payloadDigest"], cid)
        except QueryRefusal:
            out.append({"kind": "coverage-unknown", "coverageId": cid, "note": "coverage payload unavailable"})
            continue
        entry = payload.get("entry") if type(payload) is dict else None
        body = entry if type(entry) is dict else payload if type(payload) is dict else {}
        token = body.get("coverage")
        if token == "unknown":
            out.append({"kind": "coverage-unknown", "coverageId": cid})
        elif token == "partial":
            out.append({"kind": "coverage-partial", "coverageId": cid})
        rc = body.get("resolutionCompleteness") if type(body) is dict else None
        if type(rc) is dict:
            if rc.get("examinedExhaustive") is False:
                out.append({"kind": "examined-not-exhaustive", "coverageId": cid, "examinedExhaustive": False})
            state = rc.get("state")
            if state in ("resolution-incomplete", "incomplete"):
                out.append({"kind": "resolution-incomplete", "coverageId": cid})
            if rc.get("unresolvedCount") not in (None, 0):
                out.append({"kind": "resolution-incomplete", "coverageId": cid, "note": "unresolvedCount"})
    return out


def deficiency_citations(run, objects, host):
    rows = []
    supplied = (host or {}).get("evaluationDeficiencies")
    if supplied is not None:
        srcs = supplied
    else:
        srcs = []
        try:
            seal = _object(objects, run["evaluationSealId"], "evaluation-seal", "evidence.missing")
            proof = _object(objects, seal["proofBundleId"], "proof-bundle", "evidence.missing")
            srcs = list(proof.get("executionDeficiencies") or [])
        except QueryRefusal:
            srcs = []
        except Exception:
            srcs = []
    for item in srcs:
        if type(item) is not dict:
            continue
        row = {"source": item.get("source") if item.get("source") in ("native", "enumeration", "execution", "import", "coverage") else "execution"}
        if item.get("cause"):
            row["cause"] = str(item["cause"])[:128]
        if item.get("coverageId"):
            row["coverageId"] = item["coverageId"]
        rows.append(row)
    return rows


def directed_hops(projected, direction):
    hops = []
    for edge in projected:
        if direction in ("outgoing", "both"):
            hops.append((endpoint_tuple(edge["source"]), endpoint_tuple(edge["target"]), edge, edge["source"], edge["target"]))
        if direction in ("incoming", "both"):
            hops.append((endpoint_tuple(edge["target"]), endpoint_tuple(edge["source"]), edge, edge["target"], edge["source"]))
    adj = {}
    for src_k, dst_k, edge, src_ep, dst_ep in hops:
        adj.setdefault(src_k, []).append((edge["factId"], dst_k, edge, src_ep, dst_ep))
    for key in adj:
        adj[key].sort(key=lambda row: row[0].encode("utf-8"))
    return adj


def neighbor_units(projected, endpoint, direction):
    rows = []
    seen = set()
    for edge in projected:
        hit = False
        if direction in ("outgoing", "both") and endpoints_equal(edge["source"], endpoint):
            hit = True
        if direction in ("incoming", "both") and endpoints_equal(edge["target"], endpoint):
            hit = True
        if hit and edge["factId"] not in seen:
            seen.add(edge["factId"])
            rows.append(edge)
    rows.sort(key=lambda r: endpoint_key(r["source"]) + endpoint_key(r["target"]) + (r["factId"].encode("utf-8"),))
    return rows


def path_unit(projected, start, target, direction, max_depth, max_visited):
    start = canonical_endpoint(start)
    target = canonical_endpoint(target)
    visited = 1
    if endpoints_equal(start, target):
        return (
            [
                {
                    "hopCount": 0,
                    "start": start,
                    "target": target,
                    "nodes": [start],
                    "edges": [],
                }
            ],
            visited,
            False,
        )
    adj = directed_hops(projected, direction)
    start_k, target_k = endpoint_tuple(start), endpoint_tuple(target)
    best = {start_k: (0, tuple())}
    found = None
    found_seq = None
    queue = deque([(start_k, 0, tuple(), [start], [])])
    truncated = False
    while queue:
        node_k, depth, seq, nodes, edges = queue.popleft()
        if depth >= max_depth:
            continue
        for fact_id, dst_k, edge, src_ep, dst_ep in adj.get(node_k, []):
            if any(endpoint_tuple(n) == dst_k for n in nodes):
                continue
            new_depth = depth + 1
            new_seq = seq + (fact_id,)
            prior = best.get(dst_k)
            if prior is not None:
                pd, pseq = prior
                if new_depth > pd or (new_depth == pd and new_seq >= pseq):
                    continue
            else:
                visited += 1
                if visited > max_visited:
                    truncated = True
                    break
            best[dst_k] = (new_depth, new_seq)
            hop = {"factId": fact_id, "source": canonical_endpoint(src_ep), "target": canonical_endpoint(dst_ep)}
            new_nodes = nodes + [canonical_endpoint(dst_ep)]
            new_edges = edges + [hop]
            if dst_k == target_k:
                if found is None or new_depth < found["hopCount"] or (
                    new_depth == found["hopCount"] and new_seq < found_seq
                ):
                    found = {
                        "hopCount": new_depth,
                        "start": start,
                        "target": target,
                        "nodes": new_nodes,
                        "edges": new_edges,
                    }
                    found_seq = new_seq
                continue
            queue.append((dst_k, new_depth, new_seq, new_nodes, new_edges))
        if truncated:
            break
    units = [found] if found is not None else []
    return units, visited, truncated


def reach_units(projected, start, direction, max_depth, include_start, max_visited):
    start = canonical_endpoint(start)
    adj = directed_hops(projected, direction)
    start_k = endpoint_tuple(start)
    rows = []
    if include_start:
        rows.append({"endpoint": start, "depth": 0})
    seen = {start_k}
    visited = 1
    truncated = False
    queue = deque([(start_k, 0)])
    while queue:
        node_k, depth = queue.popleft()
        if depth >= max_depth:
            continue
        for fact_id, dst_k, edge, src_ep, dst_ep in adj.get(node_k, []):
            if dst_k in seen:
                continue
            visited += 1
            if visited > max_visited:
                truncated = True
                break
            seen.add(dst_k)
            rows.append({"endpoint": canonical_endpoint(dst_ep), "depth": depth + 1, "viaFactId": fact_id})
            queue.append((dst_k, depth + 1))
        if truncated:
            break
    rows.sort(key=lambda r: endpoint_key(r["endpoint"]))
    return rows, visited, truncated


def apply_produced_cap(units, max_produced, already_truncated):
    if len(units) > max_produced:
        return units[:max_produced], True
    return units, already_truncated


def project_admitted_fact_graph(edges, *, relation, min_resolution):
    """Internal algorithm helper. edges must already be trusted projected rows."""
    table = projection_table()
    key = (relation, min_resolution)
    if key not in table:
        raise QueryRefusal(
            "REQUEST.PRECONDITION_FAILED",
            "QUERY.RELATION_UNSUPPORTED",
            "relation@minResolution is not a binary native-id graph projection",
            "%s@%s" % (relation, min_resolution),
        )
    out = []
    for edge in edges:
        if edge.get("relation") != relation or edge.get("resolution") != min_resolution:
            continue
        out.append(copy.deepcopy(edge))
    return out


def _availability_fault(host):
    avail = (host or {}).get("availability", "retained")
    if avail in AVAIL_DETAIL:
        raise QueryRefusal(
            "HOST.IO_FAILURE",
            AVAIL_DETAIL[avail],
            "unavailable or corrupt retained closure cannot become an empty graph match",
            avail,
            klass="operational-failed",
            fault_cause="host-io",
        )
    return avail if avail in ("retained", "partial") else "retained"


def _validate_request(request):
    if type(request) is not dict:
        raise QueryRefusal("REQUEST.PRECONDITION_FAILED", "QUERY.PARAMS_MALFORMED", "request must be an object")
    if request.get("schemaMajor") != 3:
        raise QueryRefusal(
            "REQUEST.SCHEMA_MAJOR_UNSUPPORTED",
            None,
            "graph-query schemaMajor 3 required",
        )
    if request.get("schemaFamily") != "opensip.product.query":
        raise QueryRefusal("REQUEST.PRECONDITION_FAILED", "QUERY.PARAMS_MALFORMED", "schemaFamily opensip.product.query")
    try:
        validate_schema(SCHEMA_ID + "#/$defs/GraphQueryRequestV1", request)
    except (ValidationError, canonical.AdmissionError) as exc:
        raise QueryRefusal(
            "REQUEST.PRECONDITION_FAILED",
            "QUERY.PARAMS_MALFORMED",
            "graph request failed closed schema admission",
            str(exc).splitlines()[0][:200],
        ) from exc
    if request["operation"] not in GRAPH_OPS:
        raise QueryRefusal(
            "REQUEST.PRECONDITION_FAILED",
            "QUERY.PARAMS_MALFORMED",
            "this projection owner implements graph.neighbors|path|reach only",
            request["operation"],
        )


def execute_graph_query(request, run=None, objects=None, blobs=None, host=None):
    """Strong public graph query. Retained Run/close_run unless synthetic standing is explicit."""
    host = {} if host is None else host
    _validate_request(request)
    operation = request["operation"]
    params = effective_params(operation, request["params"])
    table = projection_table().get((params["relation"], params["minResolution"]))
    if table is None:
        raise QueryRefusal(
            "REQUEST.PRECONDITION_FAILED",
            "QUERY.RELATION_UNSUPPORTED",
            "refuse non-binary or unsupported projection; do not invent edges",
            "%s@%s" % (params["relation"], params["minResolution"]),
        )
    avail = _availability_fault(host)
    bounds = work_bounds(host)
    page = request["page"]
    cursor_bind = decode_cursor(page["cursor"]) if page.get("cursor") else None
    run_id = resolve_run_id(request, host, cursor_bind)
    if run is not None and run.get("projectId") != request["projectId"]:
        raise QueryRefusal(
            "REQUEST.PRECONDITION_FAILED",
            "QUERY.PARAMS_MALFORMED",
            "projectId does not match the admitted Run",
        )

    limitations = []
    coverage_ids = []
    scope_ids = []
    cites = []
    selected_views = []
    visited = 0
    projected = []

    if host.get("standing") == SYNTHETIC_STANDING:
        graph = host.get("admittedFactGraph")
        if type(graph) is not dict:
            raise QueryRefusal(
                "REQUEST.PRECONDITION_FAILED",
                "QUERY.PARAMS_MALFORMED",
                "synthetic-admitted-fact-graph requires host.admittedFactGraph",
            )
        if graph.get("runId") != run_id or graph.get("projectId") != request["projectId"]:
            raise QueryRefusal(
                "REQUEST.PRECONDITION_FAILED",
                "QUERY.CURSOR_MISMATCH" if cursor_bind else "QUERY.PARAMS_MALFORMED",
                "synthetic graph identity does not match the resolved selection",
            )
        selected_views = sorted(graph.get("viewIds") or [])
        if request["params"].get("factViewDigests"):
            wanted = sorted(request["params"]["factViewDigests"])
            if wanted != selected_views and not set(wanted).issubset(set(selected_views)):
                raise QueryRefusal(
                    "REQUEST.PRECONDITION_FAILED",
                    "QUERY.FACT_VIEW_UNAVAILABLE",
                    "synthetic view selection is not in the admitted graph",
                )
            selected_views = wanted
        cache = host.get("cache")
        cache_key = (run_id, tuple(selected_views), params["relation"], params["minResolution"])
        if cache is not None and cache_key in cache:
            projected = copy.deepcopy(cache[cache_key])
        else:
            projected = project_admitted_fact_graph(
                graph.get("edges") or [], relation=params["relation"], min_resolution=params["minResolution"]
            )
            if cache is not None:
                cache[cache_key] = copy.deepcopy(projected)
        coverage_ids = sorted(set(graph.get("coverageIds") or []))
        scope_ids = sorted(set(graph.get("scopeIds") or []))
        limitations = list(graph.get("resolutionLimitations") or [])
        cites = list(graph.get("deficiencies") or [])
        visited = int(graph.get("factsExamined") or len(projected) or 1)
        objects = objects or {}
        blobs = blobs or {}
        run = run or {"projectId": request["projectId"], "evaluationSealId": None}
    else:
        if run is None or objects is None or blobs is None:
            raise QueryRefusal("IDENTITY.UNKNOWN", None, "graph query requires an admitted retained Run")
        admitted_id = close_retained_run(run, objects, blobs)
        if admitted_id != run_id:
            raise QueryRefusal(
                "REQUEST.PRECONDITION_FAILED",
                "QUERY.CURSOR_MISMATCH" if cursor_bind else "QUERY.PARAMS_MALFORMED",
                "admitted close_run identity does not match the resolved view",
                admitted_id,
            )
        evidence = _object(objects, run["evidenceId"], "semantic-evidence", "evidence.missing")
        selected_views = select_views(
            evidence.get("viewIds") or [], objects, params, request["params"].get("factViewDigests")
        )
        cache = host.get("cache")
        cache_key = (run_id, tuple(selected_views), params["relation"], params["minResolution"])
        if cache is not None and cache_key in cache:
            projected = copy.deepcopy(cache[cache_key]["edges"])
            visited = cache[cache_key]["visited"]
            scan_truncated = cache[cache_key]["truncated"]
            limitations = copy.deepcopy(cache[cache_key]["limitations"])
            coverage_ids = list(cache[cache_key]["coverageIds"])
            scope_ids = list(cache[cache_key]["scopeIds"])
        else:
            projected, visited, scan_truncated, limitations, coverage_ids, scope_ids = collect_projected_edges(
                selected_views, objects, blobs, table, host, bounds["maxVisitedNodes"]
            )
            if cache is not None:
                cache[cache_key] = {
                    "edges": copy.deepcopy(projected),
                    "visited": visited,
                    "truncated": scan_truncated,
                    "limitations": copy.deepcopy(limitations),
                    "coverageIds": list(coverage_ids),
                    "scopeIds": list(scope_ids),
                }
        cites = deficiency_citations(run, objects, host)
        limitations = limitations + coverage_limitations(coverage_ids, objects, blobs)

    if host.get("standing") == SYNTHETIC_STANDING:
        scan_truncated = visited > bounds["maxVisitedNodes"]
        if scan_truncated:
            visited = bounds["maxVisitedNodes"]
            if not any(x.get("kind") == "unexamined-work-bound" for x in limitations):
                limitations.append({"kind": "unexamined-work-bound", "note": "synthetic factsExamined exceeded cap"})
    else:
        scan_truncated = any(x.get("kind") == "unexamined-work-bound" for x in limitations)

    bind = selection_hash(request["projectId"], run_id, selected_views, operation, params)
    if cursor_bind is not None and cursor_bind["selectionHash"] != bind:
        raise QueryRefusal(
            "REQUEST.PRECONDITION_FAILED",
            "QUERY.CURSOR_MISMATCH",
            "cursor does not bind this project+Run+fact-views+operation+effective params",
        )
    position = cursor_bind["position"] if cursor_bind is not None else 0

    walk_truncated = scan_truncated
    if operation == "graph.neighbors":
        units = neighbor_units(projected, params["endpoint"], params["direction"])
        units, prod_trunc = apply_produced_cap(units, bounds["maxItemsPerOperation"], walk_truncated)
        walk_truncated = prod_trunc
    elif operation == "graph.path":
        units, path_visited, path_trunc = path_unit(
            projected, params["start"], params["target"], params["direction"], params["maxDepth"], bounds["maxVisitedNodes"]
        )
        visited = max(visited, path_visited)
        walk_truncated = walk_truncated or path_trunc
        units, prod_trunc = apply_produced_cap(units, bounds["maxItemsPerOperation"], walk_truncated)
        walk_truncated = prod_trunc
    else:
        units, reach_visited, reach_trunc = reach_units(
            projected,
            params["start"],
            params["direction"],
            params["maxDepth"],
            params["includeStart"],
            bounds["maxVisitedNodes"],
        )
        visited = max(visited, reach_visited)
        walk_truncated = walk_truncated or reach_trunc
        units, prod_trunc = apply_produced_cap(units, bounds["maxItemsPerOperation"], walk_truncated)
        walk_truncated = prod_trunc

    if not (position == 0 and len(units) == 0) and not (0 <= position < len(units)):
        raise QueryRefusal(
            "REQUEST.PRECONDITION_FAILED",
            "QUERY.CURSOR_MISMATCH",
            "cursor page position is outside the bound produced prefix; continuation cannot pass work caps",
        )

    page_size = page["size"]
    items = units[position : position + page_size]
    more_prefix = position + len(items) < len(units)
    if more_prefix:
        traversal = "truncated-page"
        truncated = False
        next_cursor = encode_cursor(run_id, bind, position + len(items))
    elif walk_truncated:
        traversal = "truncated-bound"
        truncated = True
        next_cursor = None
    else:
        traversal = "complete"
        truncated = False
        next_cursor = None

    if walk_truncated:
        count_basis = "lower-bound"
        total_items = len(units)
        if not any(x.get("kind") == "unexamined-work-bound" for x in limitations):
            limitations.append({"kind": "unexamined-work-bound", "note": "produced or visited cap with owed unexamined work"})
    else:
        count_basis = "exact"
        total_items = len(units)

    evidence = {
        "coverageIds": coverage_ids,
        "scopeIds": scope_ids,
        "deficiencyCitations": cites,
        "resolutionLimitations": limitations,
    }
    context = {
        "projectId": request["projectId"],
        "resolvedView": {"runId": run_id},
        "factViewDigests": selected_views,
        "availability": avail,
        "truncated": truncated,
        "totalItems": total_items,
        "countBasis": count_basis,
        "traversalCoverage": traversal,
        "visitedNodes": visited,
        "producedItems": len(units),
        "advisory": False,
        "evidence": evidence,
    }
    if next_cursor is not None:
        context["nextCursor"] = next_cursor

    termination = {"class": "success"}
    if request["completeness"] == "required" and walk_truncated:
        termination = {"class": "indeterminate", "reasonCodes": ["QUERY.COMPLETENESS_UNMET"], "runId": run_id}

    result = {
        "schemaFamily": "opensip.product.query",
        "schemaMajor": 3,
        "operation": operation,
        "context": context,
        "items": items,
        "termination": termination,
    }
    try:
        validate_schema(SCHEMA_ID + "#/$defs/GraphQueryResponseV1", result)
        validate_schema(COMMON_ID + "#/$defs/StepTermination", termination)
    except (ValidationError, canonical.AdmissionError) as exc:
        raise QueryRefusal(
            "SYSTEM.OUTCOME.ILLEGAL_STATE",
            "HOST.INVARIANT_VIOLATED",
            "graph query produced an inadmissible public envelope",
            str(exc).splitlines()[0][:200],
            klass="operational-failed",
            fault_cause="host-invariant",
        ) from exc
    return result
