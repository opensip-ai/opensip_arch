"""PROBE C5 — full-response renderer parity at the boundary actually claimed:
the query command's `query-response` parity field must be the COMPLETE owner-admitted
GraphQueryResponseV1; the four scalars must be exact projections of its context; and
the compact envelope QueryResult's completenessMet must be true exactly when
countBasis == exact."""
import importlib.util, json, os, sys

DC = '/tmp/opensip-design-corrections/candidate-subject.v26/docs/coop/design-corrections'
sys.path.insert(0, os.path.join(DC, 'foundation'))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


Q = load('qp3', os.path.join(DC, 'workflows/query_projection_model.v3.py'))
QS = load('qsp3', os.path.join(DC, 'workflows/query_surface_projection.v3.py'))
S = load('sf3', os.path.join(DC, 'foundation/evaluator_semantic_fixture.v3.py'))
RP = load('csr3', os.path.join(DC, 'foundation/check-semantic-replay.v3.py'))
R = {}


def rec(k, v):
    R[k] = v
    print('%-56s %s' % (k, json.dumps(v)[:260] if not isinstance(v, str) else v))


atom = {"op": "none", "relation": "references", "minResolution": "resolved-binding",
        "endpoint": "target", "filters": []}
g = S.build_ts_semantic_graph(atom=atom, has_declares=False, has_references_fact=True,
                              second_partition=True, references_resolved=False,
                              incoming_search=True, incoming_complete=False,
                              target_sidecar=True, second_universe=True)
run, objects, blobs, actual = RP.close_positive(g)
run_key, project = actual["runId"], run["projectId"]
HOST = {"requestId": "req1_" + "a" * 32, "latestRunId": run_key}
foo = {"universe": g["u1"], "kind": "symbol", "nativeSubjectId": g["foo"]}
bar = {"universe": g["u1"], "kind": "symbol", "nativeSubjectId": g["bar"]}


def req(op, params, completeness="required", size=100):
    return {"completeness": completeness, "operation": op, "page": {"size": size},
            "params": params, "projectId": project, "schemaFamily": "opensip.product.query",
            "schemaMajor": 3, "view": {"runId": run_key}}


for label, host in (("complete", dict(HOST)),
                    ("truncated-bound", dict(HOST, testBounds={"maxVisitedNodes": 1}))):
    resp = Q.execute_graph_query(
        req("graph.path", {"relation": "references", "minResolution": "resolved-binding",
                           "direction": "outgoing", "start": foo, "target": bar, "maxDepth": 4}),
        run, objects, blobs, host=host)
    term = resp.get("termination") or {"class": "success"}
    proj = QS.project_query_surface(resp, term)
    par = proj.get("parity") or {}
    rec('%s.parity_keys' % label, sorted(par.keys()))
    rec('%s.query_response_is_complete_owned_response' % label, par.get("query-response") == resp)
    ctx = resp["context"]
    rec('%s.scalars_exact' % label, {
        "resolved-view": par.get("resolved-view") == ctx.get("resolvedView"),
        "availability": par.get("availability") == ctx.get("availability"),
        "truncated": par.get("truncated") == ctx.get("truncated"),
        "total-items": par.get("total-items") == ctx.get("totalItems"),
        "termination-class": par.get("termination-class") == term.get("class"),
    })
    rec('%s.values' % label, {k: par.get(k) for k in
                              ("resolved-view", "availability", "truncated", "total-items",
                               "termination-class")})
    gs = proj.get("graphSummary") or {}
    rec('%s.graphSummary' % label, gs)
    rec('%s.countBasis' % label, ctx.get("countBasis"))
    if "completenessMet" in gs:
        rec('%s.completenessMet_iff_exact' % label,
            gs["completenessMet"] == (ctx.get("countBasis") == "exact"))
    rec('%s.advisory_is_false' % label, ctx.get("advisory") is False and gs.get("advisory") is False)

# required parity field list the command inventory declares for `query`
inv = json.load(open(os.path.join(DC, 'workflows/command-inventory.v3.json'), encoding='utf-8'))
qrow = [c for c in inv["commands"] if c.get("name") == "query"]
rec('command_inventory_query_parityFields', qrow[0].get("parityFields") if qrow else None)
rec('query_surface_required_parity', getattr(QS, 'REQUIRED_PARITY_FIELDS', None))

json.dump(R, open('/tmp/opensip-design-corrections/claude-independent-design.v26/receipts/probeCD3.json', 'w'), indent=1)
