"""R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR: independent reconstruction of graph.neighbors|path|reach over admitted retained Runs.

Owners:
  workflows/query-projection-contract.v3.md s1-s8;
  workflows/schemas/evaluator3/graph-query.schema.json (major 3);
  workflows-and-surfaces.md s8 lines 1012-1077 (query parity fields and the compact QueryResult joins);
  foundation/evaluator-fault-observation.schema.v3.json#/x-opensip-routes (loss, retained-regeneration and host-internal carriers).

Every execution calls ref/closure.close_run (complete replay) on the retained store before projection; nothing is minted. Host observations
(requestId, latestRunId, runsForSnapshot, availability, availabilityRecord, hostMode, cache, testBounds) are explicit synthetic inputs.
Named readings (phase 10):
  - the human rendering label form;
  - context.availability reports 'retained' when no observation is supplied and close_run admits;
  - remedies for evidence.purged/expired/corrupt are this reconstruction's own text.

source43 (HC-54): re-audited against the source43 bytes of query-projection-contract.v3.md, the only kit member changed since source42
(my own source42 custody row sha256 923ff32f..., 29699 bytes; current 30278 bytes). Corrected laws:
  - s4: graph.path edges report the traversal hop nodes[i] -> nodes[i+1];
  - s7: closed host availability vocabulary including `missing`; a present null/wrong-type/unknown observation is a reference-call
    precondition (after request admission); a host adapter's out-of-vocabulary observation routes host-invariant; a retained availability
    record is admitted against identity availability with runId equal to the queried Run, else evidence.corrupt;
  - s7: close_run's four typed outcomes (EvidenceUnavailable, CompleteReplayMismatch -> evidence.regeneration-mismatch, other admission
    refusal, non-typed exception -> HOST.INVARIANT_VIOLATED) are selected by outcome type, not message text; loss and regeneration use the
    registered carrier remedies verbatim;
  - s2: the endpoint admission keeps the closed ENDPOINT_AMBIGUOUS refusal.
The source42.v3 version is preserved at preserved/s42-v3-final/tools/phase9_graph_query.py and executed as the pre column.
Writes vectors/graph-query.json.  Usage: python3 tools/runref.py tools/phase9_graph_query.py
"""
import collections
import copy
import hashlib
import importlib.util
import json
import re
import sys

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source43.v1/output"
sys.path.insert(0, OUT + "/ref")
sys.path.insert(0, OUT + "/tools")

import canonical as K  # noqa: E402
import closure as CL  # noqa: E402
import schemas  # noqa: E402
from store import Store  # noqa: E402
import phase7_vectors as P7  # noqa: E402

KIT = schemas.kit()
GQ = "workflows/schemas/evaluator3/graph-query.schema.json"
CONTRACT = "coop/design-corrections/workflows/query-projection-contract.v3.md"
CONTRACT_PATH = OUT.replace("/output", "/subject/docs/") + CONTRACT
CONTRACT_SOURCE42 = {"sha256": "923ff32fc9e063f8c9af00bb7943f77bb47a09d876826ca425e0cd580cee8a4b", "bytes": 29699,
                     "selector": "preserved/s42-v3-final/vectors/phase0-custody.json#/fileRows (own source42 custody row)"}
BOUNDS = {k: v["const"] for k, v in KIT.doc(GQ)["$defs"]["Bounds"]["properties"].items()}
ROUTES = KIT.doc("foundation/evaluator-fault-observation.schema.v3.json")["x-opensip-routes"]
LOSS_ROUTE, REGEN_ROUTE, HOST_ROUTE = "promised-bytes-lost:evidence-store", "complete-replay-mismatch:retained-regeneration", "input-schema-invalid:host-internal"
TABLE = {("calls", "resolved-callee"): ("caller", "symbol", "resolvedCallee", ["symbol"], "admitted-target"),
         ("references", "resolved-binding"): ("referrer", "symbol", "resolvedBinding", ["symbol"], "admitted-target"),
         ("imports", "resolved-target"): ("importer", "symbol", "resolvedTarget", ["file", "symbol", "package"], "admitted-target"),
         ("control-flow", "syntactic"): ("from", "symbol", "to", ["symbol"], "same-only"),
         ("reachability", "from-resolved-calls"): ("origin", "symbol", "reachable", ["symbol"], "same-only")}
# s7: the reference host observation vocabulary is closed; `missing` is a direct host report of missing bytes, not an identity state
AVAIL_VOCAB = ("retained", "partial", "purged", "expired", "corrupt", "unavailable", "missing")
AVAIL_DETAIL = {"purged": "evidence.purged", "expired": "evidence.expired", "corrupt": "evidence.corrupt", "unavailable": "evidence.missing", "missing": "evidence.missing"}
IDENTITY_AVAILABILITY = ("foundation/identity-schemas.v3.json", "#/$defs/availability")
failures = []


def must(name, cond, detail=None):
    if not cond:
        failures.append({"vector": name, "detail": detail})
    return bool(cond)


def enc(s):
    return s.encode()


class QueryRefusal(Exception):
    def __init__(self, klass, code, detail, subject=None, fault=None, remedy=None, diagnostic=None):
        super().__init__(detail)
        self.klass, self.code, self.detail, self.subject, self.fault = klass, code, detail, subject, fault
        self.remedy = remedy or REMEDY.get(detail, "correct the request")
        self.diagnostic = diagnostic  # retained privately; never selects the route

    def termination(self):
        t = {"class": self.klass, "errorCode": self.code}
        if self.fault:
            t["faultCause"] = self.fault
        d = {"code": self.detail, "remedy": self.remedy}
        if self.subject:
            d["subject"] = str(self.subject)[:1024]
        t["domainDetail"] = d
        return t


class ReferenceCallPrecondition(Exception):
    pass


REMEDY = {"QUERY.SCHEMA_MAJOR_UNSUPPORTED": "send a graph-query request with schemaMajor 3",
          "QUERY.PARAMS_MALFORMED": "send the closed per-operation params with a complete native endpoint tuple",
          "QUERY.RELATION_UNSUPPORTED": "query a relation@rung row of the graph projection table",
          "QUERY.ENDPOINT_AMBIGUOUS": "name one admitted vertex", "QUERY.ENDPOINT_UNKNOWN": "name an endpoint in the admitted vertex domain",
          "QUERY.VIEW_AMBIGUOUS": "select the Run by runId", "QUERY.VIEW_UNKNOWN": "select an admitted Run by runId",
          "QUERY.CURSOR_MISMATCH": "restart paging or continue with the bound runId and identical parameters",
          "QUERY.FACT_VIEW_UNAVAILABLE": "select fact-views admitted on this Run",
          "evidence.purged": "re-run the analysis; the Run's evidence was purged", "evidence.expired": "re-run the analysis; retention expired",
          "evidence.corrupt": "restore the store from custody or re-run the analysis",
          # evaluator-fault-contract.v3 line 98: the loss route uses the existing carrier remedy verbatim
          "evidence.missing": ROUTES[LOSS_ROUTE]["remedy"]}


def refuse(detail, subject=None):
    code = {"QUERY.SCHEMA_MAJOR_UNSUPPORTED": "REQUEST.SCHEMA_MAJOR_UNSUPPORTED", "QUERY.VIEW_UNKNOWN": "IDENTITY.UNKNOWN"}.get(detail, "REQUEST.PRECONDITION_FAILED")
    return QueryRefusal("request-rejected", code, detail, subject)


def routed(route_key, subject, diagnostic=None):
    r = ROUTES[route_key]
    t = r["termination"]
    return QueryRefusal(t["class"], t["errorCode"], r["detail"], subject, t.get("faultCause"), r["remedy"], diagnostic)


def corrupt(subject, diagnostic=None):
    return QueryRefusal("operational-failed", "HOST.IO_FAILURE", "evidence.corrupt", subject, "host-io", diagnostic=diagnostic)


# ------------------------------------------------------------------ identity typed outcomes of close_run (s7)
class EvidenceUnavailable(Exception):
    pass


class CompleteReplayMismatch(Exception):
    pass


class IdentityAdmissionError(Exception):
    pass


MISSING_KEYS = {"EVIDENCE_UNAVAILABLE", "RETAINED_CLOSURE.RETENTION.PREIMAGE_MISSING", "RETAINED_CLOSURE.RETENTION.DERIVED_SOURCE_MISSING",
                "RETAINED_CLOSURE.RETENTION.FRAGMENT_OWNER_MISSING"}
INTERNAL_KEYS = {"cb24.CLOSURE_INTERNAL_ERROR", "RETAINED_CLOSURE.WALKER.cb24.RETAINED_CLOSURE_INTERNAL_ERROR"}
REPLAY_STAGES = {"semantic-replay", "reachable-output-set-equality"}


def identity_outcome(report):
    """Normalize ref/closure.close_run's structured refusal into the identity typed outcomes the query boundary selects on.

    Only the refusing stage and the leading typed key of its first fault are used. The detail text after the key never selects a route;
    it becomes the subject of a missing reference only.
    - A checker-internal key is not an identity outcome.
    - A lost-bytes key is EvidenceUnavailable.
    - A refusal at semantic replay or reachable-output equality, other than the evaluator refusing its admitted inputs, is
      CompleteReplayMismatch: owner admission and the retained closure both admitted first.
    - Everything else is an identity admission refusal."""
    first = report.get("firstRefusal") or {}
    fault = first.get("fault") or ""
    key = fault.split(":", 1)[0]
    rest = fault[len(key) + 1:] if ":" in fault else ""
    if key in INTERNAL_KEYS:
        return RuntimeError(key)
    if key in MISSING_KEYS:
        return EvidenceUnavailable(rest or key)
    if first.get("stage") in REPLAY_STAGES and key != "EVALUATION_REFUSED":
        return CompleteReplayMismatch(report["runId"])
    return IdentityAdmissionError(key)


# ------------------------------------------------------------------ admitted Run cache (strong path: close_run each distinct store)
ADMITTED, STORES = {}, {}


def stored(name):
    if name not in STORES:
        STORES[name] = json.load(open(f"{OUT}/runs/{name}.store.json"))
    return STORES[name]


def admit_run(name, exported, close=None):
    key = name if close is None and STORES.get(name) is exported else None
    if key and key in ADMITTED:
        return ADMITTED[key]
    try:
        store = Store.load(exported)
    except K.AdmissionError as exc:
        raise corrupt(exc.boundary)
    except Exception as exc:  # not an identity typed outcome: host-owned admission-path defect
        raise routed(HOST_ROUTE, "close_run", f"{type(exc).__name__}:{exc}")
    try:
        rep = (close or CL.close_run)(store, exported["runId"])
    except Exception as exc:  # s7 outcome 4
        raise routed(HOST_ROUTE, "close_run", f"{type(exc).__name__}:{exc}")
    if rep["result"] != "ADMIT":
        outcome = identity_outcome(rep)
        diag = (rep.get("firstRefusal") or {}).get("fault")
        if isinstance(outcome, EvidenceUnavailable):
            raise routed(LOSS_ROUTE, str(outcome), diag)
        if isinstance(outcome, CompleteReplayMismatch):
            raise routed(REGEN_ROUTE, exported["runId"], diag)
        if isinstance(outcome, IdentityAdmissionError):
            raise corrupt(str(outcome), diag)
        raise routed(HOST_ROUTE, "close_run", diag)
    C = CL.Closure(store)
    g = CL.admit_graph(C, exported["runId"])
    g.update(runId=exported["runId"], store=store, objectCount=len(store.objects), blobCount=len(store.blobs), replay=rep["result"],
             closeRunStage=None)
    if key:
        ADMITTED[key] = g
    return g


# ------------------------------------------------------------------ request admission and host observations
def admit_request(req):
    if not isinstance(req, dict):
        raise refuse("QUERY.PARAMS_MALFORMED", "request is not an object")
    if req.get("schemaMajor") != 3:
        raise refuse("QUERY.SCHEMA_MAJOR_UNSUPPORTED", req.get("schemaMajor"))
    r = KIT.admit(req, GQ, "#/$defs/GraphQueryRequestV1")
    if not r["ok"]:
        raise refuse("QUERY.PARAMS_MALFORMED", (r["stock"][:1] or r["order"][:1] or [r["typed"]])[0])
    if req["operation"] not in ("graph.neighbors", "graph.path", "graph.reach"):
        raise refuse("QUERY.PARAMS_MALFORMED", "not a graph operation")
    eff = dict(req["params"])
    if req["operation"] == "graph.reach":
        eff.setdefault("includeStart", False)
    if (eff["relation"], eff["minResolution"]) not in TABLE:
        raise refuse("QUERY.RELATION_UNSUPPORTED", f"{eff['relation']}@{eff['minResolution']}")
    return eff


def consume_availability(host, run_id):
    """s7 availability observation, consumed after request admission and before close_run. Returns the observed state or None."""
    adapter = host.get("hostMode") == "adapter"
    if "availabilityRecord" in host:
        raw = host["availabilityRecord"]
        try:
            rec = K.parse_raw(raw) if isinstance(raw, (bytes, bytearray)) else raw
        except K.AdmissionError as exc:
            raise corrupt("availability-record", exc.boundary)
        r = KIT.admit(rec, *IDENTITY_AVAILABILITY)
        if not r["ok"]:
            raise corrupt("availability-record", (r["stock"][:1] or [r["typed"]])[0])
        if rec["runId"] != run_id:
            raise corrupt("availability-record", "runId is not the queried Run")
        av = rec["state"]
    elif "availability" in host:
        av = host["availability"]
        if type(av) is not str or av not in AVAIL_VOCAB:
            if adapter:
                raise routed(HOST_ROUTE, "host.availability", f"out-of-vocabulary observation {av!r}")
            raise ReferenceCallPrecondition("host.availability")
    else:
        return None
    if av in AVAIL_DETAIL:
        raise routed(LOSS_ROUTE, av) if AVAIL_DETAIL[av] == "evidence.missing" else \
            QueryRefusal("operational-failed", "HOST.IO_FAILURE", AVAIL_DETAIL[av], av, "host-io")
    return av


def tup(e):
    return (e["universe"], e["kind"], e["nativeSubjectId"], e.get("packageManifestPath", ""))


def ep(t):
    d = {"universe": t[0], "kind": t[1], "nativeSubjectId": t[2]}
    if t[1] == "package":
        d["packageManifestPath"] = t[3]
    return d


def tkey(t):
    return tuple(enc(x) for x in t)


def admit_endpoint(vertex_records, e):
    """s2 steps 2-4 over vertex records (schema admission, step 1, already ran). A complete tuple names at most one vertex of a derived
    domain, so step 2 is unreachable through execute; it is kept as the closed refusal for duplicate vertex records."""
    hits = [v for v in vertex_records if v == tup(e)]
    if len(hits) > 1:
        raise refuse("QUERY.ENDPOINT_AMBIGUOUS", json.dumps(e, sort_keys=True))
    if not hits:
        raise refuse("QUERY.ENDPOINT_UNKNOWN", json.dumps(e, sort_keys=True))
    return hits[0]


def selection_hash(project_id, run_id, views, op, eff):
    return hashlib.sha256(K.C({"projectId": project_id, "runId": run_id, "factViewDigests": views, "operation": op, "params": eff,
                               "order": "query-projection-contract.v3 s3/s4"})).hexdigest()


# ------------------------------------------------------------------ strong wrapper
def execute(req, run_name, host, exported=None, close=None):
    rid = host.get("requestId")
    if not isinstance(rid, str) or not re.fullmatch(r"req1_[0-9a-f]{32}", rid):
        raise ReferenceCallPrecondition("host.requestId")
    diagnostic = None
    try:
        eff = admit_request(req)
        if exported is None:
            exported = stored(run_name)
        av = consume_availability(host, exported["runId"])
        g = admit_run(run_name, exported, close)
        run_id, run_hex = g["runId"], g["runId"].split(":", 1)[1]
        view = req["view"]
        cursor = req["page"].get("cursor")
        if cursor is not None:
            m = re.fullmatch(r"q3\.([0-9a-f]{64})\.([0-9a-f]{64})\.([0-9]+)", cursor)
            if not m or view.get("runId") != "run3:" + m.group(1) or m.group(1) != run_hex:
                raise refuse("QUERY.CURSOR_MISMATCH", "continuation must name the bound runId")
        if req["projectId"] != g["snapshot"]["projectId"]:
            # HC-25: s7 table row (REQUEST.PRECONDITION_FAILED / QUERY.PARAMS_MALFORMED)
            raise refuse("QUERY.PARAMS_MALFORMED", "projectId does not own the admitted Run")
        if "runId" in view:
            if view["runId"] != run_id:
                raise refuse("QUERY.VIEW_UNKNOWN", view["runId"])
        elif "snapshotId" in view:
            obs = host.get("runsForSnapshot", {}).get(view["snapshotId"])
            if not obs:
                raise refuse("QUERY.VIEW_UNKNOWN", "no trusted runsForSnapshot observation")
            if len(set(obs)) > 1:
                raise refuse("QUERY.VIEW_AMBIGUOUS", view["snapshotId"])
            if obs[0] != run_id or g["plan"]["snapshotId"] != view["snapshotId"]:
                raise refuse("QUERY.VIEW_UNKNOWN", "observation does not name this Run for this snapshot")
        else:
            if host.get("latestRunId") != run_id:
                raise refuse("QUERY.VIEW_UNKNOWN", "latest observation missing or names another Run")
        rel, rung = eff["relation"], eff["minResolution"]
        views = g["views"]
        if "factViewDigests" in eff:
            for d in eff["factViewDigests"]:
                if d not in views:
                    raise refuse("QUERY.FACT_VIEW_UNAVAILABLE", d)
            selected = sorted(eff["factViewDigests"], key=enc)
        else:
            selected = sorted([v for v in views if any((g["scopes"][s]["relation"], g["scopes"][s]["resolution"]) == (rel, rung) for s in views[v]["scopeIds"])], key=enc)
        matching = [v for v in selected if any((g["scopes"][s]["relation"], g["scopes"][s]["resolution"]) == (rel, rung) for s in views[v]["scopeIds"])]
        # vertex domain (s2): selected subject-inventory rows + projected fact endpoints
        inv_sel = {r["digest"] for r in g["proof"]["evaluationInputRefs"] if r["domain"] == "subject-inventory"}
        inventory_vertices = set()
        for (ci, po, kind), (dig, rec) in g["index"]["inventories"].items():
            if dig in inv_sel:
                U = g["enum"]["cells"][ci]["programBindings"][po]["universe"]
                for row in rec["rows"]:
                    inventory_vertices.add((U, row["kind"], row["nativeSubjectId"], row["path"] if row["kind"] == "package" else ""))
        sf, sk, tf, tks, urule = TABLE[(rel, rung)]
        edges, limitations, seen = [], [], set()
        for vid in matching:
            for fid in views[vid]["facts"]:
                if fid in seen:
                    continue
                f = g["facts"][fid]
                if f["relation"] != rel:
                    continue
                seen.add(fid)
                if f["resolution"] != rung:
                    limitations.append({"kind": "unsupported-rung-omitted", "factId": fid, "relation": rel, "minResolution": rung})
                    continue
                p = g["payloads"].get(fid) or {}
                if p.get(sf) is None or p.get(tf) is None:
                    limitations.append({"kind": "unprojectable-fact", "factId": fid, "note": "payload endpoint field absent"})
                    continue
                src = (f["sourceUniverse"], sk, p[sf], "")
                tu = f["targetUniverse"] if urule == "admitted-target" else f["sourceUniverse"]
                if len(tks) == 1:
                    tgt = (tu, tks[0], p[tf], "")
                else:
                    exact = sorted({v for v in inventory_vertices if v[0] == tu and v[2] == p[tf]}, key=tkey)
                    if len(exact) != 1:
                        limitations.append({"kind": "unprojectable-fact", "factId": fid,
                                            "note": "no reconciled occupancy: no unique exact-id inventory identity and no selected TargetAttributionV2 sidecar"})
                        continue
                    tgt = exact[0]
                edges.append({"fid": fid, "src": src, "tgt": tgt, "fact": f})
        edges.sort(key=lambda e: enc(e["fid"]))
        vertex_records = sorted(inventory_vertices | {e["src"] for e in edges} | {e["tgt"] for e in edges}, key=tkey)
        op = req["operation"]
        endpoints = [eff["endpoint"]] if op == "graph.neighbors" else [eff["start"]] + ([eff["target"]] if op == "graph.path" else [])
        for e in endpoints:
            admit_endpoint(vertex_records, e)
        bounds = dict(BOUNDS)
        for k, v in (host.get("testBounds") or {}).items():
            if k in ("maxVisitedNodes", "maxItemsPerOperation"):
                bounds[k] = min(bounds[k], v)
        direction = eff["direction"]

        def hops(v):
            out = []
            for e in edges:
                if direction in ("outgoing", "both") and e["src"] == v:
                    out.append((e["fid"], e["tgt"]))
                if direction in ("incoming", "both") and e["tgt"] == v and (e["fid"], e["src"]) not in out:
                    out.append((e["fid"], e["src"]))
            return sorted(out, key=lambda h: enc(h[0]))
        bound_hit = False
        if op == "graph.neighbors":
            ev = tup(eff["endpoint"])
            visited = 1
            rows = []
            for e in edges:
                inc = (direction in ("outgoing", "both") and e["src"] == ev) or (direction in ("incoming", "both") and e["tgt"] == ev)
                if inc:
                    rows.append((e["src"], e["tgt"], e["fid"], e["fact"]))
            rows.sort(key=lambda r: tkey(r[0]) + tkey(r[1]) + (enc(r[2]),))
            # s4: neighbors rows keep the projected fact's own source->target
            units = [{"factId": fid, "relation": rel, "resolution": rung, "source": ep(s), "target": ep(t), "producerClosure": f["producerClosure"],
                      "confidenceMillionths": f["confidenceMillionths"]} for s, t, fid, f in rows]
        else:
            start = tup(eff["start"])
            visited_set, visited = {start}, 1
            queue = collections.deque([(start, 0)])
            parent, reach_rows, found = {start: None}, [], None
            if op == "graph.path" and start == tup(eff["target"]):
                found = start
            while queue and found is None:
                v, d = queue.popleft()
                if d >= eff["maxDepth"]:
                    continue
                for fid, w in hops(v):
                    if w in visited_set:
                        continue
                    if visited >= bounds["maxVisitedNodes"]:
                        bound_hit = True
                        break
                    visited_set.add(w)
                    visited += 1
                    parent[w] = (v, fid)
                    reach_rows.append({"endpoint": w, "depth": d + 1, "viaFactId": fid})
                    if op == "graph.path" and w == tup(eff["target"]):
                        found = w
                        break
                    queue.append((w, d + 1))
                if bound_hit:
                    break
            if op == "graph.path":
                units = []
                if found is not None:
                    nodes, pedges, cur = [found], [], found
                    while parent[cur] is not None:
                        pv, fid = parent[cur]
                        # HC-54 (s4): edges[i] is the directed hop from nodes[i] to nodes[i+1] as walked; under incoming/both it may be the
                        # reverse of the stored fact's orientation, and factId still names the stored fact
                        pedges.append({"factId": fid, "source": ep(pv), "target": ep(cur)})
                        nodes.append(pv)
                        cur = pv
                    nodes.reverse()
                    pedges.reverse()
                    units = [{"hopCount": len(pedges), "start": ep(start), "target": ep(tup(eff["target"])), "nodes": [ep(n) for n in nodes], "edges": pedges}]
                    bound_hit = False  # a witness established before the cap is complete; remaining branches are not owed
            else:
                rows = [dict(r, endpoint=ep(r["endpoint"])) for r in reach_rows]
                if eff["includeStart"]:
                    rows.append({"endpoint": ep(start), "depth": 0})
                units = sorted(rows, key=lambda r: tkey(tup(r["endpoint"])))
        produced = units[:bounds["maxItemsPerOperation"]]
        if len(units) > len(produced):
            bound_hit = True
        # disclosure (s6)
        rel_cov = {cid for cid, (cd, p) in g["coverages"].items() if p and p["key"]["relation"] == rel}
        sel_cov = {cid for v in selected for cid in views[v]["coverageIds"]}
        cov_ids = sorted(sel_cov | rel_cov, key=enc)
        scope_ids = sorted({s for v in selected for s in views[v]["scopeIds"]} | {g["coverages"][c][0]["scopeId"] for c in rel_cov}, key=enc)
        cites = [{k: d[k] for k in ("source", "cause", "subjectId", "predicateId", "inputRefs", "nativeCause")} for d in g["proof"]["executionDeficiencies"]]
        lim = []
        for cid in sorted(rel_cov, key=enc):
            entry, key = g["coverages"][cid][1]["entry"], g["coverages"][cid][1]["key"]
            rc = entry["resolutionCompleteness"]
            base = {"coverageId": cid, "relation": key["relation"], "minResolution": key["resolution"], "coverage": entry["coverage"],
                    "resolutionState": rc["state"], "attempted": rc["attempted"], "examinedExhaustive": rc["examinedExhaustive"], "unresolvedEdgeCount": rc["unresolvedEdgeCount"]}
            if rc["state"] in ("incomplete", "partial", "not-attempted"):
                lim.append(dict(base, kind={"incomplete": "resolution-incomplete", "partial": "resolution-partial", "not-attempted": "resolution-not-attempted"}[rc["state"]]))
            if entry["coverage"] != "complete":
                lim.append(dict(base, kind="coverage-unknown" if entry["coverage"] == "unknown" else "coverage-partial"))
            if not rc["examinedExhaustive"]:
                lim.append(dict(base, kind="examined-not-exhaustive"))
        for fid, f in sorted(g["facts"].items()):
            if f["relation"] == "unresolved-edge" and (g["payloads"].get(fid) or {}).get("relation") == rel:
                lim.append({"kind": "unresolved-edge-present", "factId": fid, "relation": rel})
        lim += limitations
        if not matching:
            lim.append({"kind": "native-evidence-unavailable", "relation": rel, "minResolution": rung})
        if bound_hit:
            lim.append({"kind": "unexamined-work-bound", "note": "a work bound stopped the logical operation with owed work remaining"})
        position = int(cursor.split(".")[-1]) if cursor else 0
        sel_hash = selection_hash(req["projectId"], run_id, selected, op, eff)
        if cursor and (cursor.split(".")[2] != sel_hash or position > len(produced)):
            raise refuse("QUERY.CURSOR_MISMATCH", "selection or position does not match the bound continuation")
        size = req["page"]["size"]
        page = produced[position:position + size]
        more = position + size < len(produced)
        ctx = {"projectId": req["projectId"], "resolvedView": {"runId": run_id}, "factViewDigests": selected, "availability": av or "retained",
               "truncated": bound_hit, "totalItems": len(produced), "countBasis": "lower-bound" if bound_hit else "exact",
               "traversalCoverage": "truncated-bound" if bound_hit else ("truncated-page" if more else "complete"), "visitedNodes": visited,
               "producedItems": len(produced), "advisory": False,
               "evidence": {"coverageIds": cov_ids, "scopeIds": scope_ids, "deficiencyCitations": cites, "resolutionLimitations": lim}}
        if more:
            ctx["nextCursor"] = f"q3.{run_hex}.{sel_hash}.{position + size}"
        resp = {"schemaFamily": "opensip.product.query", "schemaMajor": 3, "operation": op, "context": ctx, "items": page}
        if bound_hit and req["completeness"] == "required":
            term = {"class": "indeterminate", "reasonCodes": ["QUERY.COMPLETENESS_UNMET"], "runId": run_id}
            resp["termination"] = term
        else:
            term = {"class": "success"}
        return {"kind": "response", "response": resp, "termination": term, "mintedObjects": len(g["store"].objects) - g["objectCount"]}
    except QueryRefusal as q:
        t = q.termination()
        env = {"schemaFamily": "opensip.product.envelope", "schemaMajor": 3, "kind": "failure", "requestId": rid, "termination": t,
               "exitCode": P7.EXIT[t["class"]], "errors": [t["domainDetail"]]}
        if isinstance(req, dict) and isinstance(req.get("projectId"), str) and re.fullmatch(r"prj1-[0-9a-f]{64}", req["projectId"]):
            env["projectId"] = req["projectId"]
        return {"kind": "failure", "envelope": env, "diagnostic": q.diagnostic}


# ------------------------------------------------------------------ renderers and compact summary joins
PARITY = ["resolved-view", "availability", "truncated", "total-items", "termination-class", "query-response"]


def parity_fields(resp, term):
    c = resp["context"]
    return {"resolved-view": c["resolvedView"], "availability": c["availability"], "truncated": c["truncated"], "total-items": c["totalItems"],
            "termination-class": term["class"], "query-response": resp}


QUERY_DISPATCH = P7.INVENTORY["query"]["queryDispatch"]


def pointer(doc, ptr):
    cur = doc
    for part in ptr.split("/")[1:]:
        part = part.replace("~1", "/").replace("~0", "~")
        cur = cur[int(part)] if isinstance(cur, list) else cur[part]
    return cur


def parity_from_envelope(env):
    """workflows-and-surfaces s8 lines 1197-1239: parity is read from the envelope at the inventory queryDispatch.parityPaths pointers."""
    return {field: pointer(env, ptr) for field, ptr in QUERY_DISPATCH["parityPaths"].items()}


def render_all(out, host):
    resp, term = out["response"], out["termination"]
    c = resp["context"]
    qr = {"kind": "query", "items": len(resp["items"]), "truncated": c["truncated"], "completenessMet": c["countBasis"] == "exact", "advisory": False}
    if "nextCursor" in c:
        qr["nextCursor"] = c["nextCursor"]
    # HC-25: source39 public query carrier - CommandEnvelope major 3 kind=query, querySurface equal to the inventory queryDispatch.surface,
    # and the complete owner-admitted GraphQueryResponseV1 in queryResponse. The JSON rendering IS that envelope; the agent rendering is
    # the same envelope plus agentHints. The original {envelope, queryResponse} cb24 carrier is preserved in preserved/s39-original/tools/.
    env = {"schemaFamily": "opensip.product.envelope", "schemaMajor": 3, "kind": "query", "requestId": host["requestId"], "projectId": c["projectId"],
           "termination": term, "exitCode": P7.EXIT[term["class"]], "query": qr, "querySurface": QUERY_DISPATCH["surface"], "queryResponse": resp}
    probe_ok, probe_errs = P7.admit(env, P7.ENV3, "#")
    pf = parity_from_envelope(env)
    json_r = K.C(env).decode()
    human = "\n".join(f"{field}: {K.C(value).decode()}" for field, value in pf.items())
    agent_r = K.C(dict(env, agentHints=["graph rows are stored-edge results; zero rows do not prove absence"])).decode()
    return {"envelope": env, "envelopeFaults": P7.check_envelope(env), "queryResponseCarrierProbe": {"admitted": probe_ok, "errors": probe_errs},
            "renderings": {"json": json_r, "human": human, "agent": agent_r}, "parity": pf}


def parse_rendering(fmt, text):
    if fmt in ("json", "agent"):
        o = json.loads(text)
        return parity_from_envelope(o), o
    parsed = {field: json.loads(value) for field, value in (line.split(": ", 1) for line in text.split("\n"))}
    missing = [f for f in QUERY_DISPATCH["parityPaths"] if f not in parsed]
    if missing:
        raise KeyError(missing[0])
    return parsed, None


def summary_join_faults(env, resp):
    f = []
    c, q = resp["context"], env["query"]
    if q["items"] != len(resp["items"]):
        f.append("cb24.QUERY_SUMMARY_ITEMS")
    if q["truncated"] != c["truncated"]:
        f.append("cb24.QUERY_SUMMARY_TRUNCATED")
    if q["advisory"] is not False:
        f.append("cb24.QUERY_SUMMARY_ADVISORY")
    if q.get("nextCursor") != c.get("nextCursor"):
        f.append("cb24.QUERY_SUMMARY_CURSOR")
    if q["completenessMet"] != (c["countBasis"] == "exact"):
        f.append("cb24.QUERY_SUMMARY_COMPLETENESS")
    if "termination" in resp and resp["termination"] != env["termination"]:
        f.append("cb24.QUERY_RESPONSE_TERMINATION_DIFFERS")
    if env.get("projectId") != c["projectId"]:
        f.append("cb24.QUERY_PROJECT_DIFFERS")
    return f


# ------------------------------------------------------------------ pre column: the unchanged source42.v3 helper
def load_s42v3_helper():
    spec = importlib.util.spec_from_file_location("gq_s42v3", OUT + "/preserved/s42-v3-final/tools/phase9_graph_query.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def outcome_summary(fn):
    try:
        out = fn()
    except Exception as exc:  # recorded, e.g. an uncaught exception or a reference precondition
        return {"exception": f"{type(exc).__name__}:{str(exc)[:160]}"}
    if out["kind"] == "failure":
        t = out["envelope"]["termination"]
        return {"failure": t["domainDetail"]["code"], "class": t["class"], "errorCode": t["errorCode"], "subject": t["domainDetail"].get("subject"),
                "remedy": t["domainDetail"]["remedy"]}
    r = out["response"]
    return {"response": r["operation"], "availability": r["context"]["availability"], "items": r["items"][:2]}


# ------------------------------------------------------------------ vectors
def main():
    base, code, scope_run = admit_run("cmp-base", stored("cmp-base")), admit_run("cmp-code", stored("cmp-code")), admit_run("cmp-scope", stored("cmp-scope"))
    U = code["enum"]["cells"][0]["programBindings"][0]["universe"]
    pid = code["snapshot"]["projectId"]
    n = [0]

    def host(**kw):
        n[0] += 1
        h = {"requestId": P7.req_id(5000 + n[0])}
        h.update(kw)
        return h

    def S(nid, kind="symbol", uni=None, manifest=None):
        e = {"universe": uni or U, "kind": kind, "nativeSubjectId": nid}
        if manifest is not None:
            e["packageManifestPath"] = manifest
        return e

    def req(op, params, view=None, size=100, cursor=None, completeness="best-effort", project=None):
        r = {"schemaFamily": "opensip.product.query", "schemaMajor": 3, "projectId": project or pid, "view": view or {"runId": code["runId"]},
             "operation": op, "params": params, "completeness": completeness, "page": {"size": size}}
        if cursor:
            r["page"]["cursor"] = cursor
        return r
    MAIN, HELPER, UNUSED, PAD = "ts:src/index.ts#main", "ts:src/util.ts#helper", "ts:src/util.ts#unused", "npm:left-pad@1.3.0#pad"
    vectors = []

    def run_vec(label, classification, request, run_name, h, expect=None, exported=None, close=None):
        out = execute(request, run_name, h, exported, close)
        rec = {"vector": label, "classification": classification, "run": run_name, "request": request,
               "hostObservations": {k: (v if not isinstance(v, (bytes, bytearray)) else {"rawBytesHex": bytes(v).hex()}) for k, v in h.items()}}
        if out["kind"] == "response":
            r = out["response"]
            ok, errs = P7.admit(r, GQ, "#/$defs/GraphQueryResponseV1")
            rend = render_all(out, h)
            parity_ok = all(parse_rendering(fmt, txt)[0] == rend["parity"] for fmt, txt in rend["renderings"].items())
            joins = summary_join_faults(rend["envelope"], r)
            rec.update(response=r, termination=out["termination"], responseAdmitted=ok, responseErrors=errs, mintedObjects=out["mintedObjects"],
                       envelope=rend["envelope"], envelopeFaults=rend["envelopeFaults"], queryResponseCarrierProbe=rend["queryResponseCarrierProbe"],
                       renderings=rend["renderings"], parityPreserved=parity_ok, summaryJoinFaults=joins)
            must(f"{label}:response-schema", ok, errs)
            must(f"{label}:envelope", not rend["envelopeFaults"], rend["envelopeFaults"])
            must(f"{label}:parity", parity_ok)
            must(f"{label}:summary-joins", not joins, joins)
            must(f"{label}:read-only", out["mintedObjects"] == 0)
        else:
            f = P7.check_envelope(out["envelope"])
            rec.update(failureEnvelope=out["envelope"], envelopeFaults=f, firstRefusal=out["envelope"]["termination"]["domainDetail"]["code"],
                       privateDiagnostic=out.get("diagnostic"))
            must(f"{label}:failure-envelope", not f, f)
        if expect:
            res = expect(rec)
            # HC-28 (own tool error, logs/s39-p89.1.phase9_graph_query.log): a failed expectation returns the record itself, which made the
            # vector file circular; the failure detail is summarized instead
            summary = True if res is True else {k: rec.get(k) for k in ("firstRefusal", "termination") if k in rec} or "expectation-false"
            rec["expectation"] = summary
            must(f"{label}:expectation", res is True, summary)
        vectors.append(rec)
        return rec

    def items(rec):
        return rec.get("response", {}).get("items", [])
    ctx = lambda rec: rec["response"]["context"]  # noqa: E731
    nb = lambda e, d="outgoing", rel="calls", rung="resolved-callee", **kw: dict({"relation": rel, "minResolution": rung, "direction": d, "endpoint": e}, **kw)  # noqa: E731

    # --- neighbors, order, rows per fact
    run_vec("neighbors-calls-outgoing-main", "valid", req("graph.neighbors", nb(S(MAIN))), "cmp-code", host(),
            lambda r: [i["target"]["nativeSubjectId"] for i in items(r)] == [PAD, HELPER] and ctx(r)["countBasis"] == "exact" and ctx(r)["visitedNodes"] == 1 or items(r))
    run_vec("neighbors-calls-incoming-pad-external-vertex", "valid", req("graph.neighbors", nb(S(PAD), "incoming")), "cmp-code", host(),
            lambda r: [i["source"]["nativeSubjectId"] for i in items(r)] == [MAIN, HELPER] and all(i["target"]["nativeSubjectId"] == PAD for i in items(r)) or items(r))
    run_vec("neighbors-control-flow-self-loop-once", "valid", req("graph.neighbors", nb(S(MAIN), "both", "control-flow", "syntactic")), "cmp-code", host(),
            lambda r: len(items(r)) == 1 and items(r)[0]["source"] == items(r)[0]["target"] or items(r))
    run_vec("neighbors-isolated-inventory-vertex", "valid", req("graph.neighbors", nb(S(UNUSED), "both")), "cmp-code", host(),
            lambda r: items(r) == [] and ctx(r)["traversalCoverage"] == "complete" or ctx(r))
    run_vec("neighbors-package-endpoint-admitted", "valid", req("graph.neighbors", nb(S("web", "package", manifest="package.json"), "both")), "cmp-code", host(),
            lambda r: items(r) == [] or items(r))
    run_vec("neighbors-imports-multi-kind-occupancy", "valid", req("graph.neighbors", nb(S("ts:src/index.ts"), "outgoing", "imports", "resolved-target")), "cmp-code", host(),
            lambda r: [(i["target"]["kind"], i["target"]["nativeSubjectId"]) for i in items(r)] == [("symbol", "ts:src/util.ts")]
            and [x["kind"] for x in ctx(r)["evidence"]["resolutionLimitations"]].count("unprojectable-fact") == 2 or (items(r), ctx(r)["evidence"]))
    run_vec("neighbors-references-no-selected-view", "valid", req("graph.neighbors", nb(S(MAIN), "both", "references", "resolved-binding")), "cmp-code", host(),
            lambda r: items(r) == [] and ctx(r)["traversalCoverage"] == "complete" and ctx(r)["factViewDigests"] == [] and
            {"kind": "native-evidence-unavailable", "relation": "references", "minResolution": "resolved-binding"} in ctx(r)["evidence"]["resolutionLimitations"] or ctx(r))
    # source39: under the bodyEligibilityLaw census ts-clones-required seals pass with no execution deficiency, so the complete-traversal-
    # with-retained-deficiencies control uses syntax-mixed-disclosed (its required clones account holds a disclosed unknown partition)
    disclosed = admit_run("syntax-mixed-disclosed", stored("syntax-mixed-disclosed"))
    run_vec("neighbors-evidence-limitations-with-complete-traversal", "valid",
            req("graph.neighbors", nb(S("sym:src/a.ts#add", uni=disclosed["enum"]["cells"][0]["programBindings"][0]["universe"]), "both", "control-flow", "syntactic"),
                view={"runId": disclosed["runId"]}, project=disclosed["snapshot"]["projectId"]),
            "syntax-mixed-disclosed", host(),
            lambda r: ctx(r)["traversalCoverage"] == "complete" and len(ctx(r)["evidence"]["deficiencyCitations"]) > 0 and len(items(r)) == 1 or ctx(r))
    # --- path
    pp = lambda s, t, d="outgoing", depth=3: {"relation": "calls", "minResolution": "resolved-callee", "direction": d, "start": s, "target": t, "maxDepth": depth}  # noqa: E731
    run_vec("path-shortest-direct-hop", "valid", req("graph.path", pp(S(MAIN), S(PAD))), "cmp-code", host(),
            lambda r: items(r)[0]["hopCount"] == 1 and len(items(r)[0]["edges"]) == 1 and items(r)[0]["edges"][0]["source"] == S(MAIN)
            and items(r)[0]["edges"][0]["target"] == S(PAD) or items(r))
    run_vec("path-zero-hop-admitted", "valid", req("graph.path", pp(S(UNUSED), S(UNUSED))), "cmp-code", host(),
            lambda r: items(r)[0]["hopCount"] == 0 and items(r)[0]["edges"] == [] and len(items(r)[0]["nodes"]) == 1 or items(r))
    run_vec("path-none-complete", "valid", req("graph.path", pp(S(HELPER), S(MAIN))), "cmp-code", host(),
            lambda r: items(r) == [] and ctx(r)["countBasis"] == "exact" and ctx(r)["totalItems"] == 0 or ctx(r))
    run_vec("path-both-direction", "valid", req("graph.path", pp(S(HELPER), S(MAIN), "both")), "cmp-code", host(),
            lambda r: items(r)[0]["hopCount"] == 1 or items(r))
    run_vec("path-depth-bound-semantic", "valid", req("graph.path", {"relation": "reachability", "minResolution": "from-resolved-calls", "direction": "outgoing",
                                                                     "start": S(MAIN), "target": S(HELPER), "maxDepth": 1}), "cmp-code", host(),
            lambda r: items(r)[0]["hopCount"] == 1 or items(r))
    run_vec("path-visited-cap-one-edge-best-effort", "valid", req("graph.path", pp(S(MAIN), S(PAD))), "cmp-code", host(testBounds={"maxVisitedNodes": 1}),
            lambda r: items(r) == [] and ctx(r)["traversalCoverage"] == "truncated-bound" and ctx(r)["visitedNodes"] == 1 and "termination" not in r["response"] or ctx(r))
    run_vec("path-visited-cap-required-indeterminate", "valid", req("graph.path", pp(S(MAIN), S(PAD)), completeness="required"), "cmp-code",
            host(testBounds={"maxVisitedNodes": 1}),
            lambda r: r["termination"] == {"class": "indeterminate", "reasonCodes": ["QUERY.COMPLETENESS_UNMET"], "runId": code["runId"]} and r["envelope"]["exitCode"] == 3 or r["termination"])
    run_vec("path-zero-hop-exactly-at-cap-complete", "valid", req("graph.path", pp(S(MAIN), S(MAIN)), completeness="required"), "cmp-code",
            host(testBounds={"maxVisitedNodes": 1}), lambda r: ctx(r)["traversalCoverage"] == "complete" and r["termination"]["class"] == "success" or ctx(r))
    # --- reach
    rp = lambda s, d="outgoing", depth=2, **kw: dict({"relation": "calls", "minResolution": "resolved-callee", "direction": d, "start": s, "maxDepth": depth}, **kw)  # noqa: E731
    run_vec("reach-outgoing-default-excludes-start", "valid", req("graph.reach", rp(S(MAIN))), "cmp-code", host(),
            lambda r: [(i["endpoint"]["nativeSubjectId"], i["depth"]) for i in items(r)] == [(PAD, 1), (HELPER, 1)] or items(r))
    run_vec("reach-include-start", "valid", req("graph.reach", rp(S(MAIN), includeStart=True)), "cmp-code", host(),
            lambda r: [i["endpoint"]["nativeSubjectId"] for i in items(r)] == [PAD, MAIN, HELPER] and "viaFactId" not in items(r)[1] or items(r))
    run_vec("reach-incoming-depth2", "valid", req("graph.reach", rp(S(PAD), "incoming")), "cmp-code", host(),
            lambda r: sorted(i["endpoint"]["nativeSubjectId"] for i in items(r)) == [MAIN, HELPER] or items(r))
    run_vec("reach-items-cap-lower-bound", "valid", req("graph.reach", rp(S(MAIN))), "cmp-code", host(testBounds={"maxItemsPerOperation": 1}),
            lambda r: ctx(r)["countBasis"] == "lower-bound" and ctx(r)["totalItems"] == 1 and ctx(r)["truncated"] and r["envelope"]["query"]["completenessMet"] is False or ctx(r))
    run_vec("reach-visited-cap-prefix", "valid", req("graph.reach", rp(S(MAIN))), "cmp-code", host(testBounds={"maxVisitedNodes": 2}),
            lambda r: len(items(r)) == 1 and ctx(r)["visitedNodes"] == 2 and ctx(r)["traversalCoverage"] == "truncated-bound" or ctx(r))
    # --- paging, cursor, latest change, cache loss
    p1 = run_vec("page1-latest-size1", "valid", req("graph.neighbors", nb(S(MAIN)), view={"latest": True}, size=1), "cmp-base", host(latestRunId=base["runId"]),
                 lambda r: ctx(r)["traversalCoverage"] == "truncated-page" and not ctx(r)["truncated"] and "nextCursor" in ctx(r) and
                 r["envelope"]["query"]["completenessMet"] is True and ctx(r)["resolvedView"] == {"runId": base["runId"]} or ctx(r))
    cur = p1["response"]["context"]["nextCursor"]
    p2 = run_vec("page2-after-newer-latest-bound-run", "valid", req("graph.neighbors", nb(S(MAIN)), view={"runId": base["runId"]}, size=1, cursor=cur), "cmp-base",
                 host(latestRunId=code["runId"], cache=None),
                 lambda r: ctx(r)["traversalCoverage"] == "complete" and "nextCursor" not in ctx(r) and len(items(r)) == 1 or ctx(r))
    full = run_vec("single-page-reference", "explanatory", req("graph.neighbors", nb(S(MAIN)), view={"runId": base["runId"]}), "cmp-base", host())
    must("pages-concatenate-to-full-selection", items(p1) + items(p2) == items(full), (items(p1), items(p2), items(full)))
    cached = run_vec("page2-with-host-cache-present", "valid", req("graph.neighbors", nb(S(MAIN)), view={"runId": base["runId"]}, size=1, cursor=cur), "cmp-base",
                     host(latestRunId=code["runId"], cache={"edges": ["caller-authored"], "standing": "complete"}))
    must("cache-presence-does-not-change-result", cached["response"] == p2["response"], None)
    run_vec("continuation-with-latest-view-refused", "invalid", req("graph.neighbors", nb(S(MAIN)), view={"latest": True}, size=1, cursor=cur), "cmp-base",
            host(latestRunId=code["runId"]), lambda r: r.get("firstRefusal") == "QUERY.CURSOR_MISMATCH" or r)
    run_vec("continuation-on-newer-run-refused", "invalid", req("graph.neighbors", nb(S(MAIN)), view={"runId": code["runId"]}, size=1, cursor=cur), "cmp-code",
            host(), lambda r: r.get("firstRefusal") == "QUERY.CURSOR_MISMATCH" or r)
    run_vec("continuation-with-changed-params-refused", "invalid", req("graph.neighbors", nb(S(MAIN), "both"), view={"runId": base["runId"]}, size=1, cursor=cur), "cmp-base",
            host(), lambda r: r.get("firstRefusal") == "QUERY.CURSOR_MISMATCH" or r)
    # --- selection
    snap = base["plan"]["snapshotId"]
    run_vec("snapshot-view-unique-observation", "valid", req("graph.neighbors", nb(S(MAIN)), view={"snapshotId": snap}), "cmp-base",
            host(runsForSnapshot={snap: [base["runId"]]}), lambda r: ctx(r)["resolvedView"] == {"runId": base["runId"]} or ctx(r))
    run_vec("snapshot-view-no-observation", "invalid", req("graph.neighbors", nb(S(MAIN)), view={"snapshotId": snap}), "cmp-base", host(),
            lambda r: r.get("firstRefusal") == "QUERY.VIEW_UNKNOWN" and r["failureEnvelope"]["termination"]["errorCode"] == "IDENTITY.UNKNOWN" or r)
    run_vec("snapshot-view-two-runs", "invalid", req("graph.neighbors", nb(S(MAIN)), view={"snapshotId": snap}), "cmp-base",
            host(runsForSnapshot={snap: [base["runId"], scope_run["runId"]]}), lambda r: r.get("firstRefusal") == "QUERY.VIEW_AMBIGUOUS" or r)
    run_vec("snapshot-view-stale-map", "invalid", req("graph.neighbors", nb(S(MAIN)), view={"snapshotId": code["plan"]["snapshotId"]}), "cmp-base",
            host(runsForSnapshot={code["plan"]["snapshotId"]: [base["runId"]]}), lambda r: r.get("firstRefusal") == "QUERY.VIEW_UNKNOWN" or r)
    run_vec("latest-view-missing-observation", "invalid", req("graph.neighbors", nb(S(MAIN)), view={"latest": True}), "cmp-base", host(),
            lambda r: r.get("firstRefusal") == "QUERY.VIEW_UNKNOWN" or r)
    run_vec("explicit-fact-view-not-on-run", "invalid", req("graph.neighbors", nb(S(MAIN), factViewDigests=sorted(base["views"]))), "cmp-code", host(),
            lambda r: r.get("firstRefusal") == "QUERY.FACT_VIEW_UNAVAILABLE" or r)
    run_vec("explicit-fact-view-on-run", "valid", req("graph.neighbors", nb(S(MAIN), factViewDigests=sorted(code["views"]))), "cmp-code", host(),
            lambda r: len(items(r)) == 2 or items(r))
    # --- malformed / unsupported / endpoints
    bad = req("graph.neighbors", nb(S(MAIN)))
    run_vec("schema-major-2", "invalid", dict(bad, schemaMajor=2), "cmp-code", host(),
            lambda r: r.get("firstRefusal") == "QUERY.SCHEMA_MAJOR_UNSUPPORTED" and r["failureEnvelope"]["termination"]["errorCode"] == "REQUEST.SCHEMA_MAJOR_UNSUPPORTED" or r)
    run_vec("extra-param-property", "invalid", req("graph.neighbors", dict(nb(S(MAIN)), limit=5)), "cmp-code", host(), lambda r: r.get("firstRefusal") == "QUERY.PARAMS_MALFORMED" or r)
    run_vec("logical-path-subject-on-graph-op", "invalid", req("graph.neighbors", {"relation": "calls", "minResolution": "resolved-callee", "direction": "outgoing", "subject": "src/index.ts"}),
            "cmp-code", host(), lambda r: r.get("firstRefusal") == "QUERY.PARAMS_MALFORMED" or r)
    run_vec("package-endpoint-without-manifest-path", "invalid", req("graph.neighbors", nb(S("web", "package"), "both")), "cmp-code", host(),
            lambda r: r.get("firstRefusal") == "QUERY.PARAMS_MALFORMED" or r)
    run_vec("manifest-path-on-symbol", "invalid", req("graph.neighbors", nb(S(MAIN, manifest="package.json"))), "cmp-code", host(),
            lambda r: r.get("firstRefusal") == "QUERY.PARAMS_MALFORMED" or r)
    run_vec("non-projectable-rung", "invalid", req("graph.neighbors", nb(S(MAIN), rung="syntactic-callee-name")), "cmp-code", host(),
            lambda r: r.get("firstRefusal") == "QUERY.RELATION_UNSUPPORTED" or r)
    run_vec("non-graph-relation-clones", "invalid", req("graph.neighbors", nb(S(MAIN), rel="clones", rung="normalized-body-hash")), "cmp-code", host(),
            lambda r: r.get("firstRefusal") == "QUERY.RELATION_UNSUPPORTED" or r)
    run_vec("endpoint-other-universe-unknown", "invalid", req("graph.neighbors", nb(S(MAIN, uni="0" * 64))), "cmp-code", host(),
            lambda r: r.get("firstRefusal") == "QUERY.ENDPOINT_UNKNOWN" or r)
    run_vec("endpoint-absent-native-id-unknown", "invalid", req("graph.path", pp(S("ts:src/nope.ts#x"), S("ts:src/nope.ts#x"))), "cmp-code", host(),
            lambda r: r.get("firstRefusal") == "QUERY.ENDPOINT_UNKNOWN" or r)
    run_vec("project-id-not-run-owner", "invalid", req("graph.neighbors", nb(S(MAIN)), project="prj1-" + "a" * 64), "cmp-code", host(),
            lambda r: r.get("firstRefusal") == "QUERY.PARAMS_MALFORMED" and r["failureEnvelope"]["termination"]["errorCode"] == "REQUEST.PRECONDITION_FAILED"
            and r["failureEnvelope"].get("projectId") == "prj1-" + "a" * 64 or r)
    run_vec("malformed-project-id-omitted-from-envelope", "invalid", req("graph.neighbors", nb(S(MAIN)), project="not-a-project"), "cmp-code", host(),
            lambda r: r.get("firstRefusal") == "QUERY.PARAMS_MALFORMED" and "projectId" not in r["failureEnvelope"] or r)
    # --- availability and retained bytes
    for state in ("purged", "expired", "corrupt", "unavailable"):
        run_vec(f"availability-{state}", "invalid", req("graph.neighbors", nb(S(MAIN))), "cmp-code", host(availability=state),
                lambda r, d=AVAIL_DETAIL[state]: r.get("firstRefusal") == d and r["failureEnvelope"]["termination"] == {"class": "operational-failed", "errorCode": "HOST.IO_FAILURE", "faultCause": "host-io",
                                                                                                                         "domainDetail": r["failureEnvelope"]["termination"]["domainDetail"]} or r)
    run_vec("availability-partial-does-not-grant-or-refuse", "valid", req("graph.neighbors", nb(S(MAIN))), "cmp-code", host(availability="partial"),
            lambda r: ctx(r)["availability"] == "partial" or r)
    exported = stored("cmp-code")
    missing = copy.deepcopy(exported)
    victim = next(h for h, v in missing["blobLabels"].items() if v == "fact-payload:calls")
    del missing["blobs"][victim]
    run_vec("missing-retained-bytes", "invalid", req("graph.neighbors", nb(S(MAIN))), "cmp-code~missing-bytes", host(), lambda r: r.get("firstRefusal") == "evidence.missing" or r,
            exported=missing)
    corrupt_store = copy.deepcopy(exported)
    import base64
    raw = bytearray(base64.b64decode(corrupt_store["blobs"][victim]))
    raw[0] ^= 1
    corrupt_store["blobs"][victim] = base64.b64encode(bytes(raw)).decode()
    run_vec("corrupt-retained-bytes", "invalid", req("graph.neighbors", nb(S(MAIN))), "cmp-code~corrupt-bytes", host(), lambda r: r.get("firstRefusal") == "evidence.corrupt" or r,
            exported=corrupt_store)
    precondition = None
    try:
        execute(req("graph.neighbors", nb(S(MAIN))), "cmp-code", {"requestId": "request-1"})
    except ReferenceCallPrecondition as exc:
        precondition = str(exc)
    must("host-request-id-precondition", precondition == "host.requestId", precondition)

    # ================================================================ source43 re-audit vectors (HC-54)
    s43_start = len(vectors)
    # s4: path edges report traversal hops
    stored_main_pad = next(i for i in items(vectors[0]) if i["target"]["nativeSubjectId"] == PAD)
    stored_main_helper = next(i for i in items(vectors[0]) if i["target"]["nativeSubjectId"] == HELPER)
    run_vec("path-incoming-edges-report-traversal-hop", "valid", req("graph.path", pp(S(PAD), S(MAIN), "incoming")), "cmp-code", host(),
            lambda r: items(r)[0]["nodes"] == [S(PAD), S(MAIN)] and items(r)[0]["edges"] == [{"factId": stored_main_pad["factId"], "source": S(PAD), "target": S(MAIN)}]
            and stored_main_pad["source"] == S(MAIN) or items(r))
    run_vec("path-both-edges-report-traversal-hop", "valid", req("graph.path", pp(S(HELPER), S(MAIN), "both")), "cmp-code", host(),
            lambda r: items(r)[0]["nodes"] == [S(HELPER), S(MAIN)] and items(r)[0]["edges"] == [{"factId": stored_main_helper["factId"], "source": S(HELPER), "target": S(MAIN)}]
            and stored_main_helper["source"] == S(MAIN) or items(r))
    # s7: closed availability vocabulary
    run_vec("availability-missing-direct-host-report", "invalid", req("graph.neighbors", nb(S(MAIN))), "cmp-code", host(availability="missing"),
            lambda r: r.get("firstRefusal") == "evidence.missing" and r["failureEnvelope"]["termination"]["errorCode"] == "HOST.IO_FAILURE"
            and r["failureEnvelope"]["termination"]["faultCause"] == "host-io" and r["failureEnvelope"]["exitCode"] == 4
            and r["failureEnvelope"]["termination"]["domainDetail"]["remedy"] == ROUTES[LOSS_ROUTE]["remedy"] or r)
    run_vec("availability-retained-observed", "valid", req("graph.neighbors", nb(S(MAIN))), "cmp-code", host(availability="retained"),
            lambda r: ctx(r)["availability"] == "retained" or r)
    preconditions = []
    for label, value in (("null", None), ("wrong-type", 3), ("unknown-token", "stale"), ("identity-state-spelling", "Retained")):
        try:
            execute(req("graph.neighbors", nb(S(MAIN))), "cmp-code", host(availability=value))
            got = "no precondition raised"
        except ReferenceCallPrecondition as exc:
            got = str(exc)
        ok = must(f"availability-precondition-{label}", got == "host.availability", got)
        preconditions.append({"vector": f"availability-precondition-{label}", "classification": "invalid", "observation": value, "firstRefusal": got,
                              "boundary": "ReferenceCallPrecondition (reference harness; no public envelope)", "masksLater": [], "pass": ok})
    run_vec("availability-out-of-vocabulary-after-malformed-request", "invalid", req("graph.neighbors", dict(nb(S(MAIN)), limit=1)), "cmp-code", host(availability="stale"),
            lambda r: r.get("firstRefusal") == "QUERY.PARAMS_MALFORMED" or r)
    run_vec("adapter-out-of-vocabulary-observation-host-invariant", "invalid", req("graph.neighbors", nb(S(MAIN))), "cmp-code", host(availability="stale", hostMode="adapter"),
            lambda r: r["failureEnvelope"]["termination"] == {"class": "operational-failed", "errorCode": "SYSTEM.OUTCOME.ILLEGAL_STATE", "faultCause": "host-invariant",
                                                             "domainDetail": {"code": "HOST.INVARIANT_VIOLATED", "remedy": ROUTES[HOST_ROUTE]["remedy"], "subject": "host.availability"}}
            and r["failureEnvelope"]["exitCode"] == 4 or r)
    adapter_rid = None
    try:
        execute(req("graph.neighbors", nb(S(MAIN))), "cmp-code", {"requestId": "bad", "availability": "stale", "hostMode": "adapter"})
    except ReferenceCallPrecondition as exc:
        adapter_rid = str(exc)
    must("adapter-without-valid-request-id-stays-precondition", adapter_rid == "host.requestId", adapter_rid)
    preconditions.append({"vector": "adapter-without-valid-request-id-stays-precondition", "classification": "invalid", "firstRefusal": adapter_rid,
                          "boundary": "adapter precondition (no envelope can be built)", "masksLater": ["host.availability out-of-vocabulary"], "pass": adapter_rid == "host.requestId"})
    record = {"schemaVersion": 2, "runId": code["runId"], "generation": 3, "state": "purged", "missingRefs": [], "reason": "retention purge"}
    run_vec("retained-availability-record-purged", "invalid", req("graph.neighbors", nb(S(MAIN))), "cmp-code", host(availabilityRecord=K.C(record)),
            lambda r: r.get("firstRefusal") == "evidence.purged" or r)
    run_vec("retained-availability-record-partial", "valid", req("graph.neighbors", nb(S(MAIN))), "cmp-code", host(availabilityRecord=K.C(dict(record, state="partial"))),
            lambda r: ctx(r)["availability"] == "partial" or r)
    run_vec("retained-availability-record-other-run-corrupt", "invalid", req("graph.neighbors", nb(S(MAIN))), "cmp-code",
            host(availabilityRecord=K.C(dict(record, runId=base["runId"], state="retained"))), lambda r: r.get("firstRefusal") == "evidence.corrupt" or r)
    run_vec("retained-availability-record-missing-state-corrupt", "invalid", req("graph.neighbors", nb(S(MAIN))), "cmp-code",
            host(availabilityRecord=K.C(dict(record, state="missing"))), lambda r: r.get("firstRefusal") == "evidence.corrupt" or r)
    dup = K.C(dict(record, state="retained"))[:-1] + b',"state":"purged"}'
    run_vec("retained-availability-record-duplicate-key-bytes-corrupt", "invalid", req("graph.neighbors", nb(S(MAIN))), "cmp-code", host(availabilityRecord=dup),
            lambda r: r.get("firstRefusal") == "evidence.corrupt" and r["failureEnvelope"]["termination"]["domainDetail"]["subject"] == "availability-record" or r)
    # s7: close_run typed outcomes
    import tamper_outputs as TO  # own tool: re-mints enclosing identities after one semantic change (tools/tamper_outputs.py)
    tstore = Store.load(exported)
    trun = TO.get(tstore, exported["runId"], "run")
    tproof = copy.deepcopy(TO.get(tstore, TO.get(tstore, trun["evaluationSealId"], "evaluation-seal")["proofBundleId"], "proof-bundle"))
    tproof["verdict"] = "fail" if tproof["verdict"] != "fail" else "pass"
    tampered_run = TO.remint(tstore, exported["runId"], tproof, {})
    tampered = tstore.export({"runId": tampered_run})
    trep = CL.close_run(Store.load(tampered), tampered_run)
    regen_stage = {"result": trep["result"], "firstRefusal": trep["firstRefusal"], "graphAdmissionFaults": trep["graphAdmission"]["faults"][:3],
                   "retainedClosure": trep["retainedClosure"]["result"]}
    must("tampered-store-admitted-by-owner-and-closure-refused-by-replay", trep["graphAdmission"]["faults"] == [] and trep["retainedClosure"]["result"] == "ADMIT"
         and (trep["firstRefusal"] or {}).get("stage") in REPLAY_STAGES, regen_stage)
    run_vec("close-run-complete-replay-mismatch-regeneration", "invalid", req("graph.neighbors", nb(S(MAIN)), view={"runId": tampered_run}), "cmp-code~verdict-reminted",
            host(), lambda r: r["failureEnvelope"]["termination"] == {"class": "operational-failed", "errorCode": "HOST.IO_FAILURE", "faultCause": "host-io",
                                                                      "domainDetail": {"code": "evidence.regeneration-mismatch", "remedy": ROUTES[REGEN_ROUTE]["remedy"], "subject": tampered_run}}
            and r["failureEnvelope"]["exitCode"] == 4 or r, exported=tampered)

    def owner_key_lookalike(store, run_id):
        raise RuntimeError("EVIDENCE_UNAVAILABLE:text that resembles an owner key")
    run_vec("close-run-non-typed-exception-host-invariant", "invalid", req("graph.neighbors", nb(S(MAIN))), "cmp-code", host(),
            lambda r: r["failureEnvelope"]["termination"] == {"class": "operational-failed", "errorCode": "SYSTEM.OUTCOME.ILLEGAL_STATE", "faultCause": "host-invariant",
                                                             "domainDetail": {"code": "HOST.INVARIANT_VIOLATED", "remedy": ROUTES[HOST_ROUTE]["remedy"], "subject": "close_run"}} or r,
            exported=copy.deepcopy(exported), close=owner_key_lookalike)
    typed = [{"report": {"runId": "run3:x", "firstRefusal": {"stage": s, "fault": f}}, "expected": e} for s, f, e in (
        ("owner-graph-admission", "EVIDENCE_UNAVAILABLE:fact-payload", "EvidenceUnavailable"),
        ("retained-closure", "RETAINED_CLOSURE.RETENTION.PREIMAGE_MISSING:$.x", "EvidenceUnavailable"),
        ("owner-graph-admission", "SCHEMA_REFUSED:plan:EVIDENCE_UNAVAILABLE-like text", "IdentityAdmissionError"),
        ("semantic-replay", "SEMANTIC_REPLAY_PROOF_MISMATCH:$.verdict", "CompleteReplayMismatch"),
        ("semantic-replay", "SEMANTIC_REPLAY_OUTPUT_OBJECT_MISSING:finding3:x", "CompleteReplayMismatch"),
        ("semantic-replay", "EVALUATION_REFUSED:ATOM_UNKNOWN", "IdentityAdmissionError"),
        ("reachable-output-set-equality", "SEMANTIC_REPLAY_REACHABLE_OUTPUT_NOT_RECOMPUTED:finding3:x", "CompleteReplayMismatch"),
        ("owner-graph-admission", "cb24.CLOSURE_INTERNAL_ERROR:KeyError", "RuntimeError"))]
    for t in typed:
        t["observed"] = type(identity_outcome(t["report"])).__name__
        t["classification"] = "explanatory"
        must(f"typed-outcome:{t['report']['firstRefusal']['fault'][:40]}", t["observed"] == t["expected"], t)
    # s2: closed endpoint-ambiguity refusal
    ambiguous = None
    try:
        admit_endpoint([tup(S(MAIN)), tup(S(MAIN))], S(MAIN))
    except QueryRefusal as q:
        ambiguous = q.detail
    must("endpoint-ambiguous-closed-refusal", ambiguous == "QUERY.ENDPOINT_AMBIGUOUS", ambiguous)
    endpoint_controls = [{"vector": "endpoint-duplicate-vertex-records-refused", "classification": "invalid", "firstRefusal": ambiguous, "masksLater": [],
                          "note": "s2 step 2 closed refusal; execute derives vertex records as a set of complete tuples, so the step is unreachable there"}]

    # --- pre column: the unchanged source42.v3 helper on every source43 vector input
    # Both columns go through the same outcome_summary of each helper's execute on identical inputs, so a difference is behavioural. Own tool error in
    # logs/s43-hc54b.0.phase9_graph_query.log: the corrected column was hand-built with fewer fields than the unchanged column, so every failure vector
    # "differed" by shape alone (e.g. both helpers refuse QUERY.PARAMS_MALFORMED for availability-out-of-vocabulary-after-malformed-request).
    old = load_s42v3_helper()
    pre_post = []
    for v in vectors[s43_start:]:
        h = {k: v["hostObservations"][k] for k in v["hostObservations"]}
        if "availabilityRecord" in h:
            h["availabilityRecord"] = bytes.fromhex(h["availabilityRecord"]["rawBytesHex"])
        if v["vector"] == "close-run-non-typed-exception-host-invariant":
            saved = old.CL.close_run
            old.CL.close_run = owner_key_lookalike
            try:
                before = outcome_summary(lambda: old.execute(v["request"], "cmp-code", dict(h), copy.deepcopy(exported)))
            finally:
                old.CL.close_run = saved
            after = outcome_summary(lambda: execute(v["request"], "cmp-code", dict(h), copy.deepcopy(exported), owner_key_lookalike))
        else:
            exp = tampered if v["run"] == "cmp-code~verdict-reminted" else None
            before = outcome_summary(lambda: old.execute(v["request"], v["run"], dict(h), exp))
            after = outcome_summary(lambda: execute(v["request"], v["run"], dict(h), exp))
        pre_post.append({"vector": v["vector"], "unchangedSource42v3Helper": before, "correctedHelper": after, "differs": before != after})
    for pc in preconditions:
        if pc["vector"].startswith("availability-precondition-"):
            hh = host(availability=pc["observation"])
            before = outcome_summary(lambda: old.execute(req("graph.neighbors", nb(S(MAIN))), "cmp-code", dict(hh)))
            after = outcome_summary(lambda: execute(req("graph.neighbors", nb(S(MAIN))), "cmp-code", dict(hh)))
            pre_post.append({"vector": pc["vector"], "unchangedSource42v3Helper": before, "correctedHelper": after, "differs": before != after})
    law_audit = [
        {"selector": "s1 selection table", "law": "runId/snapshotId/latest selection, fact-view set", "unchangedHelper": "implemented", "vectors": "snapshot-view-*, latest-view-*, explicit-fact-view-*"},
        {"selector": "s2 fault precedence step 1", "law": "schema-first; package endpoint without packageManifestPath -> QUERY.PARAMS_MALFORMED", "unchangedHelper": "implemented",
         "vectors": "package-endpoint-without-manifest-path, manifest-path-on-symbol"},
        {"selector": "s2 fault precedence step 2", "law": "ENDPOINT_AMBIGUOUS only for duplicate vertex records of one complete tuple; unreachable through execute_graph_query",
         "unchangedHelper": "implicit (set domain)", "correction": "explicit closed refusal kept (admit_endpoint)", "vectors": "endpoint-duplicate-vertex-records-refused"},
        {"selector": "s3 projection table, occupancy, order", "law": "binary native-id rungs; unprojectable/unsupported-rung limitations; public order tuples",
         "unchangedHelper": "implemented", "vectors": "neighbors-*"},
        {"selector": "s4 graph.path row", "law": "edges[i] is the directed hop nodes[i]->nodes[i+1]; under incoming/both it may reverse the stored fact; neighbors keep stored orientation",
         "unchangedHelper": "OMITTED: path edges carried the stored fact orientation", "correction": "HC-54", "vectors": "path-incoming-edges-report-traversal-hop, path-both-edges-report-traversal-hop"},
        {"selector": "s4 canonical bounded walk", "law": "FIFO BFS, fact2 order, cap before entry, no expansion at maxDepth, reach prefix stop, path witness stop",
         "unchangedHelper": "implemented", "vectors": "path-*, reach-*"},
        {"selector": "s5 cursor, paging, bounds", "law": "visited/produced laws, cursor binding, page vs operation truncation", "unchangedHelper": "implemented", "vectors": "page*, continuation-*, *-cap-*"},
        {"selector": "s6 disclosure", "law": "coverage/scope ids, deficiency citations, resolution limitations, native-evidence-unavailable", "unchangedHelper": "implemented",
         "vectors": "neighbors-references-no-selected-view, neighbors-evidence-limitations-with-complete-traversal"},
        {"selector": "s7 availability observation vocabulary", "law": "closed {retained, partial, purged, expired, corrupt, unavailable, missing}; missing -> evidence.missing; "
         "present null/wrong type/unknown token -> ReferenceCallPrecondition host.availability; request-schema admission precedes consumption",
         "unchangedHelper": "OMITTED: missing and unknown tokens were silently treated as a grant", "correction": "HC-54",
         "vectors": "availability-missing-direct-host-report, availability-precondition-*, availability-out-of-vocabulary-after-malformed-request"},
        {"selector": "s7 product host adapter", "law": "adapter's own out-of-vocabulary observation with a valid RequestId -> SYSTEM.OUTCOME.ILLEGAL_STATE / HOST.INVARIANT_VIOLATED subject host.availability",
         "unchangedHelper": "OMITTED", "correction": "HC-54", "vectors": "adapter-out-of-vocabulary-observation-host-invariant, adapter-without-valid-request-id-stays-precondition"},
        {"selector": "s7 retained availability record", "law": "record failing identity availability admission or naming another runId -> evidence.corrupt; admitted record supplies its state",
         "unchangedHelper": "OMITTED", "correction": "HC-54", "vectors": "retained-availability-record-*"},
        {"selector": "s7 close_run four outcomes", "law": "EvidenceUnavailable -> evidence.missing; CompleteReplayMismatch -> evidence.regeneration-mismatch subject RunId; other "
         "AdmissionError -> evidence.corrupt; other exception -> HOST.INVARIANT_VIOLATED subject close_run; never selected by message text",
         "unchangedHelper": "OMITTED: routed by message substring (UNAVAILABLE/MISSING), replay mismatch reported as evidence.corrupt, exceptions uncaught",
         "correction": "HC-54", "vectors": "close-run-complete-replay-mismatch-regeneration, close-run-non-typed-exception-host-invariant, typedOutcomeControls"},
        {"selector": "s7 carrier remedies; evaluator-fault-contract.v3 line 98", "law": "loss and retained-regeneration routes use the registered carrier remedies verbatim",
         "unchangedHelper": "OMITTED: own remedy text", "correction": "HC-54", "vectors": "availability-missing-direct-host-report, close-run-complete-replay-mismatch-regeneration"},
        {"selector": "s7 fault table (request rows)", "law": "schema major, params, project mismatch, relation, endpoint, view, cursor, fact-view rows", "unchangedHelper": "implemented",
         "vectors": "schema-major-2, extra-param-property, project-id-not-run-owner, non-projectable-rung, endpoint-*, snapshot-view-*, continuation-*"},
        {"selector": "s8 strong wrapper order", "law": "admit request -> observation -> close_run -> view join -> projection -> endpoints -> traversal -> disclosure",
         "unchangedHelper": "implemented (observation consumption now explicit)", "vectors": "availability-out-of-vocabulary-after-malformed-request"}]
    contract_bytes = open(CONTRACT_PATH, "rb").read()
    ref = next(v for v in vectors if v["vector"] == "reach-items-cap-lower-bound")
    join_negs = []
    for label, mutate, expect in (("summary-completeness-claimed-on-lower-bound", lambda e: e["query"].update(completenessMet=True), "cb24.QUERY_SUMMARY_COMPLETENESS"),
                                  ("summary-items-counts-total-not-page", lambda e: e["query"].update(items=5), "cb24.QUERY_SUMMARY_ITEMS"),
                                  ("summary-cursor-dropped", lambda e: e["query"].update(nextCursor="q3.x"), "cb24.QUERY_SUMMARY_CURSOR")):
        env = copy.deepcopy(ref["envelope"])
        mutate(env)
        fl = summary_join_faults(env, ref["response"])
        ok = bool(fl) and fl[0] == expect
        must(f"join-negative:{label}", ok, fl)
        join_negs.append({"vector": label, "classification": "invalid", "firstRefusal": fl[0] if fl else None, "masksLater": fl[1:], "pass": ok})
    human = ref["renderings"]["human"]
    try:
        parse_rendering("human", "\n".join(line for line in human.split("\n") if not line.startswith("termination-class")))
        dropped = None
    except KeyError as exc:
        dropped = f"cb24.RENDERER_PARITY_FIELD_MISSING:{exc}"
    must("renderer-dropping-termination-class-refused", dropped is not None, dropped)
    carrier = [v["queryResponseCarrierProbe"] for v in vectors if "queryResponseCarrierProbe" in v]
    # positive agreement controls: laws the unchanged helper already met, so both columns must agree (own control error in the first s43-hc54 run,
    # logs/s43-hc54.0.phase9_graph_query.log, asserted that every source43 vector differs)
    agree = {"availability-retained-observed", "availability-out-of-vocabulary-after-malformed-request"}
    for p in pre_post:
        p["expected"] = "agree" if p["vector"] in agree else "differ"
    must("source43-vectors-discriminate-unchanged-helper", all(p["differs"] == (p["expected"] == "differ") for p in pre_post),
         [(p["vector"], p["expected"]) for p in pre_post if p["differs"] != (p["expected"] == "differ")])
    out = {"classification": "valid", "owners": ["workflows/query-projection-contract.v3.md s1-s8", GQ, "workflows-and-surfaces.md s8 lines 1012-1077",
                                                 "foundation/evaluator-fault-observation.schema.v3.json#/x-opensip-routes"],
           "bounds": BOUNDS, "runs": {"cmp-base": base["runId"], "cmp-code": code["runId"], "cmp-scope": scope_run["runId"]},
           "vectors": vectors, "summaryJoinNegatives": join_negs, "rendererParityNegative": dropped, "hostRequestIdPrecondition": precondition,
           "measuredQueryResponseCarrier": {"envelopeHasQueryResponseField": "queryResponse" in KIT.doc(P7.ENV3)["properties"],
                                            "envelopeAdditionalProperties": KIT.doc(P7.ENV3).get("additionalProperties"),
                                            "querySurface": QUERY_DISPATCH["surface"], "parityPaths": QUERY_DISPATCH["parityPaths"],
                                            "probeAdmitted": sorted({c["admitted"] for c in carrier}),
                                            "note": ("source39 (HC-25): the JSON and agent renderings are the CommandEnvelope major 3 itself (kind=query, "
                                                     "querySurface graph-query-response, complete GraphQueryResponseV1 in queryResponse) and parity is read at the "
                                                     "inventory queryDispatch.parityPaths pointers; the prior {envelope, queryResponse} cb24 carrier is withdrawn")},
           "source43ReAudit": {"contract": {"path": "docs/" + CONTRACT, "source43Sha256": hashlib.sha256(contract_bytes).hexdigest(), "source43Bytes": len(contract_bytes),
                                            "source42": CONTRACT_SOURCE42,
                                            "priorBytesInCustody": False,
                                            "method": "the source42 bytes are not in my custody (only their hash); every law of the current text was audited against the helper"},
                               "lawAudit": law_audit, "vectorIds": [v["vector"] for v in vectors[s43_start:]], "preconditionVectors": preconditions,
                               "typedOutcomeControls": typed, "endpointControls": endpoint_controls, "tamperedStoreCloseRun": regen_stage, "prePost": pre_post},
           "counts": {"vectors": len(vectors), "valid": sum(1 for v in vectors if v["classification"] == "valid"),
                      "invalid": sum(1 for v in vectors if v["classification"] == "invalid"), "source43Vectors": len(vectors) - s43_start,
                      "preconditionVectors": len(preconditions), "typedOutcomeControls": len(typed)},
           "assertionFailures": failures}
    with open(f"{OUT}/vectors/graph-query.json", "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True, default=lambda o: {"rawBytesHex": bytes(o).hex()} if isinstance(o, (bytes, bytearray)) else str(o))
    print("vectors", len(vectors), "source43", len(vectors) - s43_start, "failures", len(failures))
    print(json.dumps(failures, default=str)[:6000])
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
