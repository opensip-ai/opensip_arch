"""Executed kit laws for bounded workflow reconstructions.

Independent of saved consumer vectors. Does not import a reference model.
Literal unconditional throws are not used as admission.
"""
from __future__ import annotations

import hashlib
from typing import Any

from helper.body_identity import (
    body_identity,
    body_identity_frame,
    body_language_version,
    l0_payload,
    language_version_bytes,
)
from helper.canonical import C
from helper.errors import AdmissionError
from helper.evaluator import eval_atom
from helper.identity import H

GRAPH_PROJECTABLE = {
    ("calls", "resolved-callee"),
    ("references", "resolved-binding"),
    ("imports", "resolved-target"),
    ("control-flow", "syntactic"),
    ("reachability", "from-resolved-calls"),
}

SYNTAX_SUFFIX_TABLE = {
    ".rs": "rust-syntax",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".js": "javascript",
    ".jsx": "javascript",
    ".d.ts": "typescript-declaration",
}

CLASSIFICATIONS = (
    "UNCHANGED",
    "CODE-NET-NEW",
    "CODE-FIXED",
    "DETECTION-DELTA",
    "POLICY-DELTA",
    "SCOPE-DELTA",
    "WAIVER-DELTA",
    "EVIDENCE-DELTA",
    "INDETERMINATE",
)


def raw_sha256_c(obj: Any) -> str:
    return hashlib.sha256(C(obj)).hexdigest()


def committed_id(prefix: str, domain: str, descriptor: Any) -> str:
    return f"{prefix}{H(domain, descriptor)}"


def repair_apply_key(*, project_id: str, repair_plan_id: str, base_snapshot_id: str) -> dict:
    preimage = {
        "operation": "repair-apply",
        "projectId": project_id,
        "repairPlanId": repair_plan_id,
        "baseSnapshotId": base_snapshot_id,
    }
    return {"preimage": preimage, "key": raw_sha256_c(preimage), "recipe": "raw SHA-256 of C({operation, projectId, repairPlanId, baseSnapshotId})"}


def mutation_intent_key(scope: dict) -> str:
    if scope.get("operation") == "repair-apply":
        raise AdmissionError("MUTATION_SCOPE_REPAIR_APPLY", "repair-apply is excluded from MutationReplayScopeV1.operation")
    return H("workflow.mutation-intent", scope)


def unit_id(*, marker_path: str, target_kind: str, target_name: str) -> str:
    pre = {
        "schemaVersion": 1,
        "markerPath": marker_path,
        "targetKind": target_kind,
        "targetName": target_name,
    }
    return "sha256:" + H("native.compilation-unit.v1", pre)


def derive_rust_edition(*, ownership: dict, body_path: str, edition_map: dict[str, int]) -> int:
    """identity-schemas.v3 rust languageVersionBinding selectionLaw. Ownership never enters BLV."""
    if not ownership:
        raise AdmissionError("BODY_LANGUAGE_OWNERSHIP_REQUIRED", "no committed SourceUnitOwnershipV1")
    if ownership.get("enumeration") != "complete":
        raise AdmissionError("BODY_LANGUAGE_OWNER_UNENUMERATED", "partial enumeration refuses before row lookup")
    units = {u["unitId"]: u for u in ownership["units"]}
    selected = set(ownership["selectedUnitIds"])
    rows = [r for r in ownership["ownership"] if r["path"] == body_path]
    if not rows:
        raise AdmissionError("BODY_LANGUAGE_OWNER_NOT_COMPILED", "no ownership row whose path equals the body path")
    selected_rows = [r for r in rows if r["unitId"] in selected]
    if not selected_rows:
        raise AdmissionError("BODY_LANGUAGE_OWNER_NOT_SELECTED", "path compiled only by unselected targets")
    editions = []
    for r in selected_rows:
        u = units.get(r["unitId"])
        if u is None:
            raise AdmissionError("BODY_LANGUAGE_OWNERSHIP_REQUIRED", "ownership names unbound unitId")
        te = u.get("targetEdition")
        if te is None:
            if u["crateName"] not in edition_map:
                raise AdmissionError("BODY_LANGUAGE_DIALECT_ABSENT", "package default edition missing")
            te = edition_map[u["crateName"]]
        editions.append(int(te))
    if len(set(editions)) != 1:
        raise AdmissionError("BODY_LANGUAGE_DIALECT_AMBIGUOUS", "selected owners disagree on edition")
    return editions[0]


def rust_body_l0(*, edition: int, span: bytes, compiler_version: str = "1.76.0", compiler_build: str, level_spec_bytes: bytes = b"opensip.l0-verbatim.spec.v1") -> str:
    """L0 from retained span + derived BLV. dialect.edition is the closed integer enum, never a string."""
    retained = rust_body_l0_retained(
        edition=edition,
        span=span,
        compiler_version=compiler_version,
        compiler_build=compiler_build,
        level_spec_bytes=level_spec_bytes,
    )
    return retained["bodyIdentity"]


def rust_body_l0_retained(*, edition: int, span: bytes, compiler_version: str = "1.76.0", compiler_build: str, level_spec_bytes: bytes = b"opensip.l0-verbatim.spec.v1") -> dict:
    blv = body_language_version(
        language_id="rust",
        compiler_name="rustc",
        compiler_version=compiler_version,
        compiler_build=compiler_build,
        dialect={"edition": int(edition)},
    )
    lv = language_version_bytes(blv)
    payload = l0_payload(span)
    frame = body_identity_frame(
        level_id="L0-verbatim",
        level_spec_bytes=level_spec_bytes,
        language_id="rust",
        language_version=lv,
        payload=payload,
    )
    bid = "sha256:" + hashlib.sha256(frame).hexdigest()
    return {
        "span": span.decode("utf-8"),
        "spanSha256": hashlib.sha256(span).hexdigest(),
        "byteLength": len(span),
        "compilerName": "rustc",
        "compilerVersion": compiler_version,
        "compilerBuild": compiler_build,
        "levelSpecSha256": hashlib.sha256(level_spec_bytes).hexdigest(),
        "levelSpecUtf8": level_spec_bytes.decode("utf-8"),
        "bodyLanguageVersion": blv,
        "languageVersionHex": lv.hex(),
        "frameSha256": hashlib.sha256(frame).hexdigest(),
        "frameHex": frame.hex(),
        "bodyIdentity": bid,
        "effectiveEdition": int(edition),
    }


def admit_syntax_suffix(path: str) -> str:
    """Longest matching suffix in the bundled syntax dialect table. Unknown suffix refuses."""
    name = path.rsplit("/", 1)[-1]
    hits = [s for s in SYNTAX_SUFFIX_TABLE if name.endswith(s)]
    if not hits:
        raise AdmissionError("unsupported-file", "no-bundled-grammar", path=path)
    best = max(hits, key=len)
    return SYNTAX_SUFFIX_TABLE[best]


def admit_config_path(path: str, inventory_paths: set[str]) -> str:
    if path not in inventory_paths:
        raise AdmissionError("CONFIG.CUSTODY_REFUSED", "config path is not snapshot-inventoried", path=path)
    return path


def admit_edition_map_crate(crate: str, crate_roots: set[str]) -> str:
    if crate not in crate_roots:
        raise AdmissionError("native.capability-spec-invalid", "edition map names a crate not in the admitted unit", extra={"crate": crate})
    return crate


def admit_clones_fact(*, anchors: list, level_spec_bytes: bytes | None, language_id: str, provider_language: str) -> dict:
    if len(anchors) != 1:
        raise AdmissionError("FACT_ANCHOR_CARDINALITY", f"clones body-identity class requires cardinality 1; observed {len(anchors)}")
    if not level_spec_bytes:
        raise AdmissionError("CLONE_LEVEL_SPEC_MISSING", "normalisationVersion must name retained level specification bytes")
    if language_id == provider_language and language_id == "typescript":
        # JS body through TS must carry javascript
        raise AdmissionError("BODY_LANGUAGE_MISMATCH", ".js body through TS engine must carry javascript not typescript")
    return {"anchors": anchors, "languageId": language_id, "providerLanguageId": provider_language}


def repair_target_join(*, target: str, matched_fingerprints: set[str]) -> str:
    if target not in matched_fingerprints:
        raise AdmissionError(
            "REPAIR.TARGET_CORRESPONDENCE_UNAVAILABLE",
            "unmatched occurrence cannot satisfy fingerprint-targeted repair",
            extra={"target": target},
        )
    return target


def classify_presence(presence: dict) -> tuple[str, bool]:
    """First axis of change along B→E0→E1→E2→E3→E4. liveInCurrent = E4 true and not waivedC."""
    b = presence.get("B")
    e0 = presence.get("E0")
    e1 = presence.get("E1")
    e2 = presence.get("E2")
    e3 = presence.get("E3")
    e4 = presence.get("E4")
    waived_c = bool(presence.get("waivedC"))
    live = e4 is True and not waived_c
    chain = [("CODE-NET-NEW" if (e0 is True and b is not True) else "CODE-FIXED" if (b is True and e0 is False) else None, b, e0),
             ("DETECTION-DELTA", e0, e1),
             ("POLICY-DELTA", e1, e2),
             ("SCOPE-DELTA", e2, e3),
             ("WAIVER-DELTA", e3, e4)]
    # first axis where boolean presence changes (None means not evaluated / not-needed)
    def changed(prev, cur):
        if prev is None or cur is None:
            return False
        return bool(prev) != bool(cur)

    if e0 is not None and b is not None and bool(b) != bool(e0):
        return ("CODE-NET-NEW" if (not b and e0) else "CODE-FIXED"), live
    if e0 is not None and e1 is not None and bool(e0) != bool(e1):
        return "DETECTION-DELTA", live
    if e1 is not None and e2 is not None and bool(e1) != bool(e2):
        return "POLICY-DELTA", live
    if e2 is not None and e3 is not None and bool(e2) != bool(e3):
        return "SCOPE-DELTA", live
    if e3 is not None and e4 is not None and (bool(e3) != bool(e4) or waived_c):
        return "WAIVER-DELTA", live
    # pivot-only: present in a pivot, absent from B and E4
    pivot_true = any(presence.get(k) is True for k in ("E0", "E1", "E2", "E3"))
    if b is False and pivot_true and e4 is False:
        if e0 is True:
            return "CODE-NET-NEW", live
        return "DETECTION-DELTA", live
    return "UNCHANGED", live


def counts_from_entries(entries: list[dict]) -> dict:
    c = {k: 0 for k in CLASSIFICATIONS}
    c["gating"] = 0
    for e in entries:
        cls = e["classification"]
        if cls not in c:
            raise AdmissionError("COMPARISON_CLASSIFICATION", cls)
        c[cls] += 1
        if e.get("gates"):
            c["gating"] += 1
    return c


def finish_comparison(desc: dict) -> dict:
    desc = dict(desc)
    desc["counts"] = counts_from_entries(desc.get("entries") or [])
    cid = committed_id("comparison2:", "workflow.comparison", desc)
    return {"comparisonResultId": cid, "descriptor": desc}


def finish_baseline(desc: dict, custody: dict) -> dict:
    bid = committed_id("baseline2:", "workflow.baseline", desc)
    return {"baselineId": bid, "descriptor": desc, "custody": custody}


def finish_repair_plan(desc: dict) -> dict:
    rid = committed_id("repairplan2:", "workflow.repair-plan", desc)
    return {"repairPlanId": rid, "descriptor": desc}


def kind_from_config_path(path: str) -> str:
    base = path.rsplit("/", 1)[-1]
    if base == "tsconfig.json":
        return "tsconfig"
    if base == "jsconfig.json":
        return "jsconfig"
    return "other"


def config_graph(*, entry: str | None, nodes: list[dict]) -> dict:
    clean = []
    for n in nodes:
        kind = kind_from_config_path(n["path"])
        if n.get("kind") not in (None, kind):
            raise AdmissionError("native.config-graph-kind-contradicts-path", n["path"])
        clean.append({
            "path": n["path"],
            "contentSha256": n["contentSha256"] if "contentSha256" in n else hashlib.sha256(n["bytes"]).hexdigest(),
            "kind": kind,
            "extendsResolved": list(n["extendsResolved"]),
        })
    clean.sort(key=lambda n: n["path"].encode())
    g = {"schemaVersion": 1, "entryConfigPath": entry, "nodes": clean}
    return {"graph": g, "graphDigestSha256": raw_sha256_c(g)}


def endpoint_key(ep: dict) -> tuple:
    return (ep["universe"], ep["kind"], ep["nativeSubjectId"], ep.get("packageManifestPath") or "")


def project_edges(facts: list[dict], *, relation: str, min_resolution: str) -> list[dict]:
    if (relation, min_resolution) not in GRAPH_PROJECTABLE:
        raise AdmissionError("QUERY.RELATION_UNSUPPORTED", f"{relation}@{min_resolution} is not graph-projectable")
    source_field = {
        ("calls", "resolved-callee"): ("caller", "resolvedCallee"),
        ("references", "resolved-binding"): ("referrer", "resolvedBinding"),
        ("imports", "resolved-target"): ("importer", "resolvedTarget"),
        ("control-flow", "syntactic"): ("from", "to"),
        ("reachability", "from-resolved-calls"): ("origin", "reachable"),
    }[(relation, min_resolution)]
    src_f, tgt_f = source_field
    edges = []
    for f in facts:
        if f["relation"] != relation or f["resolution"] != min_resolution:
            continue
        pl = f["payload"]
        if src_f not in pl or tgt_f not in pl:
            continue
        if relation == "imports" and not f.get("targetAttribution"):
            continue
        src = {
            "universe": f["sourceUniverse"],
            "kind": "symbol" if relation != "imports" else "symbol",
            "nativeSubjectId": pl[src_f],
        }
        tgt_kind = "symbol"
        if relation == "imports":
            tgt_kind = f["targetAttribution"]["kind"]
        tgt = {
            "universe": f.get("targetUniverse") or f["sourceUniverse"],
            "kind": tgt_kind,
            "nativeSubjectId": pl[tgt_f],
        }
        edges.append({
            "factId": f["factId"],
            "relation": relation,
            "resolution": min_resolution,
            "source": src,
            "target": tgt,
        })
    edges.sort(key=lambda e: (
        endpoint_key(e["source"]) + endpoint_key(e["target"]) + (e["factId"],)
    ))
    return edges


def neighbors(*, edges: list[dict], endpoint: dict, direction: str) -> list[dict]:
    out = []
    for e in edges:
        if direction in ("outgoing", "both") and e["source"] == endpoint:
            out.append(e)
        if direction in ("incoming", "both") and e["target"] == endpoint:
            out.append(e)
    # unique by factId
    seen = set()
    uniq = []
    for e in out:
        if e["factId"] in seen:
            continue
        seen.add(e["factId"])
        uniq.append(e)
    uniq.sort(key=lambda e: (
        endpoint_key(e["source"]) + endpoint_key(e["target"]) + (e["factId"],)
    ))
    return uniq


def shortest_path(*, edges: list[dict], start: dict, target: dict, max_depth: int, direction: str = "outgoing") -> dict | None:
    if start == target:
        return {"hopCount": 0, "start": start, "target": target, "nodes": [start], "edges": []}
    adj: dict[tuple, list] = {}
    for e in edges:
        if direction in ("outgoing", "both"):
            adj.setdefault(endpoint_key(e["source"]), []).append(e)
        if direction in ("incoming", "both"):
            rev = {**e, "source": e["target"], "target": e["source"]}
            adj.setdefault(endpoint_key(e["target"]), []).append(rev)
    for k in adj:
        adj[k].sort(key=lambda e: e["factId"])
    from collections import deque
    q = deque([(start, [start], [])])
    visited = {endpoint_key(start)}
    while q:
        node, nodes, path_edges = q.popleft()
        if len(path_edges) >= max_depth:
            continue
        for e in adj.get(endpoint_key(node), []):
            nxt = e["target"]
            nk = endpoint_key(nxt)
            if nk in visited:
                continue
            visited.add(nk)
            nn = nodes + [nxt]
            ne = path_edges + [{"factId": e["factId"], "source": e["source"], "target": e["target"]}]
            if nxt == target:
                return {"hopCount": len(ne), "start": start, "target": target, "nodes": nn, "edges": ne}
            q.append((nxt, nn, ne))
    return None


def reach(*, edges: list[dict], start: dict, max_depth: int, include_start: bool, direction: str = "outgoing") -> list[dict]:
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
    from collections import deque
    q = deque([(start, 0, None)])
    seen = {endpoint_key(start)}
    while q:
        node, depth, via = q.popleft()
        if depth >= max_depth:
            continue
        for e in adj.get(endpoint_key(node), []):
            nxt = e["target"]
            nk = endpoint_key(nxt)
            if nk in seen:
                continue
            seen.add(nk)
            nd = depth + 1
            rows.append({"endpoint": nxt, "depth": nd, "viaFactId": e["factId"]})
            q.append((nxt, nd, e["factId"]))
    rows.sort(key=lambda r: endpoint_key(r["endpoint"]))
    return rows


def selection_hash(*, project_id: str, run_id: str, fact_view_digests: list[str], operation: str, params: dict) -> str:
    rec = {
        "projectId": project_id,
        "runId": run_id,
        "factViewDigests": list(fact_view_digests),
        "operation": operation,
        "params": params,
    }
    return raw_sha256_c(rec)


def cursor_token(*, run_id: str, selection: str, position: int) -> str:
    hex64 = run_id.split(":", 1)[-1]
    return f"q3.{hex64}.{selection}.{position}"


def page_items(items: list, *, size: int, position: int = 0) -> tuple[list, str | None]:
    sl = items[position : position + size]
    nxt = None
    if position + size < len(items):
        nxt = str(position + size)
    return sl, nxt


def render_parity(response: dict, formats: list[str], termination: dict | None = None) -> dict:
    """Same six parity fields for human/json/agent. query-response is the complete GraphQueryResponseV1.

    termination-class is taken from the enclosing command StepTermination when supplied;
    if the response carries termination, callers must pass that same object.
    """
    ctx = response["context"]
    term = termination if termination is not None else response.get("termination")
    fields = {
        "resolved-view": ctx.get("resolvedView"),
        "availability": ctx.get("availability"),
        "truncated": ctx.get("truncated"),
        "total-items": ctx.get("totalItems"),
        "termination-class": None if term is None else term.get("class"),
        "query-response": response,
    }
    out = {}
    for fmt in formats:
        if fmt == "json":
            out[fmt] = dict(fields)
        elif fmt == "human":
            qr = fields["query-response"]
            out[fmt] = {
                "resolved-view": fields["resolved-view"],
                "availability": fields["availability"],
                "truncated": fields["truncated"],
                "total-items": fields["total-items"],
                "termination-class": fields["termination-class"],
                "query-response": qr,
            }
        elif fmt == "agent":
            out[fmt] = {
                "resolved-view": fields["resolved-view"],
                "availability": fields["availability"],
                "truncated": fields["truncated"],
                "total-items": fields["total-items"],
                "termination-class": fields["termination-class"],
                "query-response": fields["query-response"],
            }
    return out


def zero_config_unit(*, workspace_root: str, advertised: list[str], installed: list[str], candidate_only: list[str], candidate_paths: dict[str, list[str]]) -> dict:
    missing = [c for c in advertised if c not in installed]
    cells = []
    for cap in advertised:
        if cap in candidate_only:
            cells.append({
                "capabilityId": cap,
                "workspaceRoot": workspace_root,
                "kinds": [],
                "extents": [],
                "candidateSourcePaths": list(candidate_paths.get(cap, [])),
                "selectedCompleteClones": False,
            })
        elif cap in installed:
            cells.append({
                "capabilityId": cap,
                "workspaceRoot": workspace_root,
                "kinds": ["file"],
                "candidateOnly": False,
            })
        else:
            cells.append({
                "capabilityId": cap,
                "workspaceRoot": workspace_root,
                "installed": False,
                "kinds": None,
            })
    g = config_graph(entry=None, nodes=[])
    return {
        "workspaceRoot": workspace_root,
        "configGraph": g["graph"],
        "graphDigestSha256": g["graphDigestSha256"],
        "advertised": advertised,
        "installed": installed,
        "missingAdvertised": missing,
        "cells": cells,
    }
