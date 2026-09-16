"""R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR: independent reconstruction of graph.neighbors|path|reach over admitted retained Runs.

Owners: workflows/query-projection-contract.v3.md s1-s8; workflows/schemas/evaluator3/graph-query.schema.json (major 3);
workflows-and-surfaces.md s8 lines 1012-1077 (query parity fields and the compact QueryResult joins).
Every execution calls ref/closure.close_run (complete replay) on the retained store before projection; nothing is minted.
Host observations (requestId, latestRunId, runsForSnapshot, availability, cache, testBounds) are explicit synthetic inputs.
cb24 choices (phase 10): projectId mismatch -> QUERY.VIEW_UNKNOWN (the kit table has no row); human rendering label form; the
JSON/agent carrier for the complete query-response (CommandEnvelope major 3 has no such field; measured below).
Writes vectors/graph-query.json.  Usage: python3 tools/runref.py tools/phase9_graph_query.py
"""
import collections
import copy
import hashlib
import json
import re
import sys

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source41.v1/output"
sys.path.insert(0, OUT + "/ref")
sys.path.insert(0, OUT + "/tools")

import canonical as K  # noqa: E402
import closure as CL  # noqa: E402
import schemas  # noqa: E402
from store import Store  # noqa: E402
import phase7_vectors as P7  # noqa: E402

KIT = schemas.kit()
GQ = "workflows/schemas/evaluator3/graph-query.schema.json"
BOUNDS = {k: v["const"] for k, v in KIT.doc(GQ)["$defs"]["Bounds"]["properties"].items()}
TABLE = {("calls", "resolved-callee"): ("caller", "symbol", "resolvedCallee", ["symbol"], "admitted-target"),
         ("references", "resolved-binding"): ("referrer", "symbol", "resolvedBinding", ["symbol"], "admitted-target"),
         ("imports", "resolved-target"): ("importer", "symbol", "resolvedTarget", ["file", "symbol", "package"], "admitted-target"),
         ("control-flow", "syntactic"): ("from", "symbol", "to", ["symbol"], "same-only"),
         ("reachability", "from-resolved-calls"): ("origin", "symbol", "reachable", ["symbol"], "same-only")}
AVAIL_DETAIL = {"purged": "evidence.purged", "expired": "evidence.expired", "corrupt": "evidence.corrupt", "unavailable": "evidence.missing"}
failures = []


def must(name, cond, detail=None):
    if not cond:
        failures.append({"vector": name, "detail": detail})
    return bool(cond)


def enc(s):
    return s.encode()


class QueryRefusal(Exception):
    def __init__(self, klass, code, detail, subject=None, fault=None):
        super().__init__(detail)
        self.klass, self.code, self.detail, self.subject, self.fault = klass, code, detail, subject, fault

    def termination(self):
        t = {"class": self.klass, "errorCode": self.code}
        if self.fault:
            t["faultCause"] = self.fault
        d = {"code": self.detail, "remedy": REMEDY.get(self.detail, "correct the request")}
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
          "evidence.corrupt": "restore the store from custody or re-run the analysis", "evidence.missing": "restore the retained bytes or re-run the analysis"}


def refuse(detail, subject=None):
    code = {"QUERY.SCHEMA_MAJOR_UNSUPPORTED": "REQUEST.SCHEMA_MAJOR_UNSUPPORTED", "QUERY.VIEW_UNKNOWN": "IDENTITY.UNKNOWN"}.get(detail, "REQUEST.PRECONDITION_FAILED")
    return QueryRefusal("request-rejected", code, detail, subject)


# ------------------------------------------------------------------ admitted Run cache (strong path: close_run each distinct store)
ADMITTED = {}


def admit_run(name, exported=None):
    key = name if exported is None else None
    if key and key in ADMITTED:
        return ADMITTED[key]
    if exported is None:
        exported = json.load(open(f"{OUT}/runs/{name}.store.json"))
    try:
        store = Store.load(exported)
    except K.AdmissionError as exc:
        raise QueryRefusal("operational-failed", "HOST.IO_FAILURE", "evidence.corrupt", exc.boundary, "host-io")
    rep = CL.close_run(store, exported["runId"])
    if rep["result"] != "ADMIT":
        first = (rep.get("faultsInStageOrder") or rep["graphAdmission"]["faults"] or rep["semanticReplay"].get("faults") or ["?"])[0]
        detail = "evidence.missing" if "UNAVAILABLE" in first or "MISSING" in first else "evidence.corrupt"
        raise QueryRefusal("operational-failed", "HOST.IO_FAILURE", detail, first, "host-io")
    C = CL.Closure(store)
    g = CL.admit_graph(C, exported["runId"])
    g.update(runId=exported["runId"], store=store, objectCount=len(store.objects), blobCount=len(store.blobs), replay=rep["result"])
    if key:
        ADMITTED[key] = g
    return g


# ------------------------------------------------------------------ request admission
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


def tup(e):
    return (e["universe"], e["kind"], e["nativeSubjectId"], e.get("packageManifestPath", ""))


def ep(t):
    d = {"universe": t[0], "kind": t[1], "nativeSubjectId": t[2]}
    if t[1] == "package":
        d["packageManifestPath"] = t[3]
    return d


def tkey(t):
    return tuple(enc(x) for x in t)


def selection_hash(project_id, run_id, views, op, eff):
    return hashlib.sha256(K.C({"projectId": project_id, "runId": run_id, "factViewDigests": views, "operation": op, "params": eff,
                               "order": "query-projection-contract.v3 s3/s4"})).hexdigest()


# ------------------------------------------------------------------ strong wrapper
def execute(req, run_name, host, exported=None):
    rid = host.get("requestId")
    if not isinstance(rid, str) or not re.fullmatch(r"req1_[0-9a-f]{32}", rid):
        raise ReferenceCallPrecondition("host.requestId")
    try:
        eff = admit_request(req)
        av = host.get("availability")
        if av in AVAIL_DETAIL:
            raise QueryRefusal("operational-failed", "HOST.IO_FAILURE", AVAIL_DETAIL[av], av, "host-io")
        g = admit_run(run_name, exported)
        run_id, run_hex = g["runId"], g["runId"].split(":", 1)[1]
        view = req["view"]
        cursor = req["page"].get("cursor")
        if cursor is not None:
            m = re.fullmatch(r"q3\.([0-9a-f]{64})\.([0-9a-f]{64})\.([0-9]+)", cursor)
            if not m or view.get("runId") != "run3:" + m.group(1) or m.group(1) != run_hex:
                raise refuse("QUERY.CURSOR_MISMATCH", "continuation must name the bound runId")
        if req["projectId"] != g["snapshot"]["projectId"]:
            # HC-25: source39 query-projection-contract s7 publishes this row (REQUEST.PRECONDITION_FAILED / QUERY.PARAMS_MALFORMED); the
            # original cb24 choice QUERY.VIEW_UNKNOWN (no row then) is preserved in preserved/s39-original/tools/phase9_graph_query.py
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
        domain = inventory_vertices | {e["src"] for e in edges} | {e["tgt"] for e in edges}
        op = req["operation"]
        endpoints = [eff["endpoint"]] if op == "graph.neighbors" else [eff["start"]] + ([eff["target"]] if op == "graph.path" else [])
        for e in endpoints:
            hits = [v for v in domain if v == tup(e)]
            if len(hits) > 1:
                raise refuse("QUERY.ENDPOINT_AMBIGUOUS", json.dumps(e))
            if not hits:
                raise refuse("QUERY.ENDPOINT_UNKNOWN", json.dumps(e, sort_keys=True))
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
                        e = next(x for x in edges if x["fid"] == fid)
                        pedges.append({"factId": fid, "source": ep(e["src"]), "target": ep(e["tgt"])})
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
        return {"kind": "failure", "envelope": env}


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


# ------------------------------------------------------------------ vectors
def main():
    base, code, scope_run = admit_run("cmp-base"), admit_run("cmp-code"), admit_run("cmp-scope")
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

    def run_vec(label, classification, request, run_name, h, expect=None, exported=None):
        out = execute(request, run_name, h, exported)
        rec = {"vector": label, "classification": classification, "run": run_name, "request": request, "hostObservations": {k: v for k, v in h.items()}}
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
            rec.update(failureEnvelope=out["envelope"], envelopeFaults=f, firstRefusal=out["envelope"]["termination"]["domainDetail"]["code"])
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
            lambda r: [i["source"]["nativeSubjectId"] for i in items(r)] == [MAIN, HELPER] or items(r))
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
    disclosed = admit_run("syntax-mixed-disclosed")
    run_vec("neighbors-evidence-limitations-with-complete-traversal", "valid",
            req("graph.neighbors", nb(S("sym:src/a.ts#add", uni=disclosed["enum"]["cells"][0]["programBindings"][0]["universe"]), "both", "control-flow", "syntactic"),
                view={"runId": disclosed["runId"]}, project=disclosed["snapshot"]["projectId"]),
            "syntax-mixed-disclosed", host(),
            lambda r: ctx(r)["traversalCoverage"] == "complete" and len(ctx(r)["evidence"]["deficiencyCitations"]) > 0 and len(items(r)) == 1 or ctx(r))
    # --- path
    pp = lambda s, t, d="outgoing", depth=3: {"relation": "calls", "minResolution": "resolved-callee", "direction": d, "start": s, "target": t, "maxDepth": depth}  # noqa: E731
    run_vec("path-shortest-direct-hop", "valid", req("graph.path", pp(S(MAIN), S(PAD))), "cmp-code", host(),
            lambda r: items(r)[0]["hopCount"] == 1 and len(items(r)[0]["edges"]) == 1 or items(r))
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
    for state, detail in AVAIL_DETAIL.items():
        run_vec(f"availability-{state}", "invalid", req("graph.neighbors", nb(S(MAIN))), "cmp-code", host(availability=state),
                lambda r, d=detail: r.get("firstRefusal") == d and r["failureEnvelope"]["termination"] == {"class": "operational-failed", "errorCode": "HOST.IO_FAILURE", "faultCause": "host-io",
                                                                                                           "domainDetail": r["failureEnvelope"]["termination"]["domainDetail"]} or r)
    run_vec("availability-partial-does-not-grant-or-refuse", "valid", req("graph.neighbors", nb(S(MAIN))), "cmp-code", host(availability="partial"),
            lambda r: ctx(r)["availability"] == "partial" or r)
    exported = json.load(open(f"{OUT}/runs/cmp-code.store.json"))
    missing = copy.deepcopy(exported)
    victim = next(h for h, v in missing["blobLabels"].items() if v == "fact-payload:calls")
    del missing["blobs"][victim]
    run_vec("missing-retained-bytes", "invalid", req("graph.neighbors", nb(S(MAIN))), "cmp-code~missing-bytes", host(), lambda r: r.get("firstRefusal") == "evidence.missing" or r,
            exported=missing)
    corrupt = copy.deepcopy(exported)
    import base64
    raw = bytearray(base64.b64decode(corrupt["blobs"][victim]))
    raw[0] ^= 1
    corrupt["blobs"][victim] = base64.b64encode(bytes(raw)).decode()
    run_vec("corrupt-retained-bytes", "invalid", req("graph.neighbors", nb(S(MAIN))), "cmp-code~corrupt-bytes", host(), lambda r: r.get("firstRefusal") == "evidence.corrupt" or r,
            exported=corrupt)
    precondition = None
    try:
        execute(req("graph.neighbors", nb(S(MAIN))), "cmp-code", {"requestId": "request-1"})
    except ReferenceCallPrecondition as exc:
        precondition = str(exc)
    must("host-request-id-precondition", precondition == "host.requestId", precondition)
    # --- summary join and renderer negatives
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
    out = {"classification": "valid", "owners": ["workflows/query-projection-contract.v3.md s1-s8", GQ, "workflows-and-surfaces.md s8 lines 1012-1077"],
           "bounds": BOUNDS, "runs": {"cmp-base": base["runId"], "cmp-code": code["runId"], "cmp-scope": scope_run["runId"]},
           "vectors": vectors, "summaryJoinNegatives": join_negs, "rendererParityNegative": dropped, "hostRequestIdPrecondition": precondition,
           "measuredQueryResponseCarrier": {"envelopeHasQueryResponseField": "queryResponse" in KIT.doc(P7.ENV3)["properties"],
                                            "envelopeAdditionalProperties": KIT.doc(P7.ENV3).get("additionalProperties"),
                                            "querySurface": QUERY_DISPATCH["surface"], "parityPaths": QUERY_DISPATCH["parityPaths"],
                                            "probeAdmitted": sorted({c["admitted"] for c in carrier}),
                                            "note": ("source39 (HC-25): the JSON and agent renderings are the CommandEnvelope major 3 itself (kind=query, "
                                                     "querySurface graph-query-response, complete GraphQueryResponseV1 in queryResponse) and parity is read at the "
                                                     "inventory queryDispatch.parityPaths pointers; the prior {envelope, queryResponse} cb24 carrier is withdrawn")},
           "counts": {"vectors": len(vectors), "valid": sum(1 for v in vectors if v["classification"] == "valid"),
                      "invalid": sum(1 for v in vectors if v["classification"] == "invalid")},
           "assertionFailures": failures}
    with open(f"{OUT}/vectors/graph-query.json", "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print("vectors", len(vectors), "failures", len(failures))
    print(json.dumps(failures, default=str)[:6000])
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
