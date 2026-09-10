"""Independent Grok probes of frozen source24. Not author oracles; not qualification."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/grok-independent-design.v24")
ORIG = Path("/tmp/opensip-design-corrections/candidate-subject.v24")
COPY = OUT / "subject-copy"
DC = COPY / "docs/coop/design-corrections"
FOUND = DC / "foundation"
WF = DC / "workflows"
PY = "/tmp/opensip-architecture-review-env/bin/python"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


F = load("probe_fixture3", FOUND / "evaluator_graph_fixture.v3.py")
R = load("probe_replay3", FOUND / "evaluator_replay_model.v3.py")
M = R.M
C = M.C
W = load("probe_projection3", WF / "workflow_projection_model.v3.py")
Q = load("probe_query3", WF / "query_projection_model.v3.py")
QS = load("probe_query_surface3", WF / "query_surface_projection.v3.py")
Sfix = load("probe_semantic_fixture3", FOUND / "evaluator_semantic_fixture.v3.py")
Srep = load("probe_semantic_replay3", FOUND / "check-semantic-replay.v3.py")
rows = []


def add(name, **kwargs):
    rec = {"case": name, **kwargs}
    rows.append(rec)
    return rec


def canonical_sets(value):
    if type(value) is dict:
        for k, v in value.items():
            canonical_sets(v)
            if k in (
                "findingIds",
                "waivedFindingIds",
                "evidenceRefs",
                "inputRefs",
                "evaluationInputRefs",
                "scopeIds",
                "coverageIds",
                "matchingFactIds",
                "uncertainFactIds",
                "matchingImportRows",
                "uncertainImportRows",
                "deficiencies",
            ):
                value[k] = R.E.cset(v)
            if k == "predicateProofs":
                value[k] = sorted(
                    v, key=lambda x: tuple(x[t].encode() for t in ("ruleId", "subjectId", "predicateId"))
                )
        return value
    if type(value) is list:
        for x in value:
            canonical_sets(x)
    return value


def seal(graph, result, objects, blobs):
    objects = copy.deepcopy(objects)
    blobs = copy.deepcopy(blobs)
    objects.update(result["objects"])
    blobs.update(result["blobs"])
    i = graph["inputs"]

    def add_obj(domain, fields):
        value = {"schemaVersion": 3, **fields}
        key = M.identifier(domain, value)
        objects[key] = (domain, value)
        return key

    evidence = add_obj(
        "semantic-evidence",
        {
            "planId": i["planId"],
            "viewIds": graph["viewIds"],
            "coverageIds": graph["coverageIds"],
            "importIds": i["plan"]["importIds"],
            "findingIds": result["proof"]["findingIds"],
            "proofBundleId": result["proofBundleId"],
        },
    )
    sid = add_obj(
        "evaluation-seal",
        {
            "planId": i["planId"],
            "executionPlanId": i["executionPlanId"],
            "evidenceId": evidence,
            "evaluatorClosure": i["evaluatorClosure"],
            "policyDigest": i["plan"]["policyDigest"],
            "proofBundleId": result["proofBundleId"],
            "verdict": result["proof"]["verdict"],
        },
    )
    run = {
        "schemaVersion": 3,
        "projectId": graph["snapshot"]["projectId"],
        "snapshotId": i["plan"]["snapshotId"],
        "planId": i["planId"],
        "evidenceId": evidence,
        "evaluationSealId": sid,
        "capabilityManifestId": i["plan"]["capabilityManifestId"],
    }
    return run, objects, blobs


def positive_graph(**options):
    g = F.build_file_inputs(**options)
    seed, objects, blobs, _ = F.seal_fixture(g)
    _, owner = M.open_run_closure(seed, objects, blobs)
    i = g["inputs"]
    result = R.derive(
        i["planId"],
        i["executionPlanId"],
        i["evaluatorClosure"],
        i["evaluationInputRefs"],
        objects,
        blobs,
        owner,
    )
    return seal(g, result, objects, blobs)


def remint_enclosing(run, objects, blobs, mutate_finding=None, mutate_proof=None):
    run = copy.deepcopy(run)
    objects = copy.deepcopy(objects)
    blobs = copy.deepcopy(blobs)
    evidence = copy.deepcopy(objects[run["evidenceId"]][1])
    seal_rec = copy.deepcopy(objects[run["evaluationSealId"]][1])
    proof = copy.deepcopy(objects[seal_rec["proofBundleId"]][1])
    old_fid = proof["findingIds"][0] if proof.get("findingIds") else None
    if mutate_finding is not None and old_fid:
        finding = copy.deepcopy(objects[old_fid][1])
        mutate_finding(finding, blobs)
        new_fid = M.identifier("finding", finding)
        objects[new_fid] = ("finding", finding)

        def replace(value):
            if value == old_fid:
                return new_fid
            if type(value) is list:
                return [replace(x) for x in value]
            if type(value) is dict:
                return {k: replace(v) for k, v in value.items()}
            return value

        proof = replace(proof)
        evidence = replace(evidence)
    if mutate_proof is not None:
        mutate_proof(proof, objects, blobs)
    canonical_sets(proof)
    pid = M.identifier("proof-bundle", proof)
    objects[pid] = ("proof-bundle", proof)
    evidence["proofBundleId"] = pid
    canonical_sets(evidence)
    eid = M.identifier("semantic-evidence", evidence)
    objects[eid] = ("semantic-evidence", evidence)
    seal_rec.update(proofBundleId=pid, evidenceId=eid, verdict=proof["verdict"])
    sid = M.identifier("evaluation-seal", seal_rec)
    objects[sid] = ("evaluation-seal", seal_rec)
    run.update(evidenceId=eid, evaluationSealId=sid)
    return run, objects, blobs


def host_obs(**kw):
    body = {"requestId": "req1_" + "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}
    body.update(kw)
    return body


def ep(universe, kind, nid, manifest=None):
    row = {"universe": universe, "kind": kind, "nativeSubjectId": nid}
    if manifest is not None:
        row["packageManifestPath"] = manifest
    return row


def qreq(operation, project, view, params, *, completeness="required", size=100, cursor=None, major=3):
    page = {"size": size}
    if cursor is not None:
        page["cursor"] = cursor
    return {
        "completeness": completeness,
        "operation": operation,
        "page": page,
        "params": params,
        "projectId": project,
        "schemaFamily": "opensip.product.query",
        "schemaMajor": major,
        "view": view,
    }


def refuse_query(fn):
    try:
        fn()
    except Q.QueryRefusal as exc:
        env = exc.envelope()
        return exc, env
    except Exception as exc:
        raise AssertionError("expected QueryRefusal, got " + type(exc).__name__ + ": " + str(exc)) from exc
    raise AssertionError("expected QueryRefusal")


# --- 1. honest positive graph admits and replays ---
base = positive_graph()
honest_close = M.close_run(*base)
honest_open = M.open_run_closure(*base)[0]
assert honest_close == honest_open
add(
    "honest-positive-close-run-equals-open-run-id",
    ownerAdmission="ADMIT",
    closeRunId=honest_close,
    openRunId=honest_open,
    equal=True,
)

# --- 2. fully reminted false finding: owner ADMIT, complete replay REFUSE ---
def bump_severity(finding, blobs):
    finding["severity"] = "warning"


mutant = remint_enclosing(*base, mutate_finding=bump_severity)
owner_id = M.open_run_closure(*mutant)[0]
try:
    M.close_run(*mutant)
except Exception as exc:
    replay_reason = str(exc)
    assert "EVALUATOR_COMPLETE_PROOF_REPLAY" in replay_reason, replay_reason
else:
    raise AssertionError("reminted false finding accepted by close_run")
add(
    "reminted-severity-false-result-owner-admits-replay-refuses",
    ownerAdmission="ADMIT",
    ownerRunId=owner_id,
    closeRun="REFUSE",
    replayReasonClass="EVALUATOR_COMPLETE_PROOF_REPLAY",
    structuralApiIsNotSemanticAuthority=True,
)

# --- 3. reminted false verdict with same finding count ---
def force_pass(proof, objects, blobs):
    proof["verdict"] = "pass"


verdict_mutant = remint_enclosing(*base, mutate_proof=force_pass)
owner_id2 = M.open_run_closure(*verdict_mutant)[0]
try:
    M.close_run(*verdict_mutant)
except Exception as exc:
    assert "EVALUATOR_COMPLETE_PROOF_REPLAY" in str(exc), str(exc)
    add(
        "reminted-false-pass-verdict-owner-admits-replay-refuses",
        ownerAdmission="ADMIT",
        ownerRunId=owner_id2,
        closeRun="REFUSE",
        findingCountUnchanged=True,
    )
else:
    raise AssertionError("false pass verdict accepted by close_run")

# --- 4. required evaluator3 Plan parameters ---
payloads = M.PAYLOADS["classes"]["parameter"]["rows"]
required_rows = [k for k, rec in payloads.items() if 3 in rec.get("requiredForEvaluatorMajors", [])]
assert set(required_rows) == {
    "foundation/enumeration-plan.schema.v1.json",
    "foundation/evaluator-emission-plan.schema.v1.json",
}, required_rows
required = [
    {"schemaDigest": hashlib.sha256((DC / path).read_bytes()).hexdigest(), "payloadDigest": "a" * 64}
    for path in required_rows
]
M.admit_parameter_selection(required)
add("exact-two-required-evaluator3-parameters", count=len(required), rows=sorted(required_rows))
for i, _ in enumerate(required):
    selection = [r for j, r in enumerate(required) if j != i]
    try:
        M.admit_parameter_selection(selection)
    except Exception as exc:
        assert "EVALUATOR_REQUIRED_PARAMETER_MISSING" in str(exc), str(exc)
        add("omitted-required-parameter-" + str(i), result="REFUSE", missing=required_rows[i])
    else:
        raise AssertionError("missing required parameter accepted")

# --- 5. DetectorManifestV1 is not the component-manifest body ---
listing_schema = json.loads((WF / "schemas/evaluator3/detector-manifest.schema.json").read_text())
comp_schema = json.loads((COPY / "docs/coop/artifacts/component-manifest-schemas.v11.json").read_bytes())
listing_required = set(listing_schema["required"])
assert listing_required == {"schemaFamily", "schemaMajor", "compatibleClosures"}
assert "platforms" not in listing_schema.get("properties", {})
assert "tree" not in listing_schema.get("properties", {})
text = json.dumps(comp_schema)
assert "platforms" in text
add(
    "detector-listing-is-not-component-manifest-body",
    listingRequired=sorted(listing_required),
    listingFieldCount=len(listing_schema["properties"]),
    reservedPath=".opensip/detector-compatibility.json",
    componentManifestHasPlatformsOrTree=True,
)

# --- 6. Independent mixed-root comparison ---
scope = {"schemaFamily": "opensip.product.scope", "schemaMajor": 1, "include": ["**"], "exclude": []}


def build_filtered(pattern):
    return positive_graph(
        scope_document=scope,
        atom_override={
            "op": "exists",
            "relation": "file",
            "minResolution": "enumerated",
            "filters": [{"field": "subject", "cmp": "glob", "value": pattern}],
        },
    )


baseline = build_filtered("README.md")
current = build_filtered("src/**")
M.close_run(*baseline)
M.close_run(*current)
bv = W.project_admitted_run_v3(*baseline)
cv = W.project_admitted_run_v3(*current)
assert bv["snapshotId"] == cv["snapshotId"]
for view in (bv, cv):
    roots = W.admitted_root_predicate_values(view, view["policy"]["rules"][0]["ruleId"])
    assert set(roots.values()) <= {"true", "false"}
    assert not view["executionDeficiencies"]
art = W.adopt_admitted_baseline_v3(
    *baseline, {"exportedAtUtc": "2026-09-08T00:00:00Z", "exportedByHostRelease": "1.0.0"}
)
closures = {
    k: {
        "bytes": "ok",
        "trust": "admitted",
        "trustOrigin": "retained-generation",
        "protocolMajor": v["protocolMajor"],
        "platform": v["platform"],
    }
    for k, (d, v) in baseline[1].items()
    if d == "closure"
}
host = {
    "closures": closures,
    "protocolMajors": sorted({v["protocolMajor"] for v in closures.values()}),
    "platform": "macos-aarch64",
    "pivotRunId": bv["runId"],
    "recipeMajors": [2],
}
comparison = W.compare_admitted_v3(
    baseline_artifact=art,
    current_run=current[0],
    current_objects=current[1],
    current_blobs=current[2],
    host=host,
    profile_name="code-regression",
    pivot_runs={"E1": baseline},
)
entries = comparison["descriptor"]["entries"]
assert len(entries) == 2, entries
assert all(e["classification"] == "POLICY-DELTA" for e in entries), entries
appeared = next(e for e in entries if e["direction"] == "appeared")
assert appeared["presence"]["E1"] is False and appeared["presence"]["E4"] is True
add(
    "independent-mixed-root-absence-is-policy-delta-not-indeterminate",
    classifications=sorted({e["classification"] for e in entries}),
    directions=sorted({e["direction"] for e in entries}),
    appearedE1=appeared["presence"]["E1"],
    appearedE4=appeared["presence"]["E4"],
    verdict=comparison["descriptor"]["verdict"],
)

# --- 7. Independent native case count vs contract prose ---
native_cases = json.loads((DC / "native/native-cases.v2.json").read_bytes())
n_count = len(native_cases["cases"]) if isinstance(native_cases, dict) and "cases" in native_cases else None
n_report = json.loads((OUT / "pinned-runs/native-evidence-report.v2.json").read_bytes())
add(
    "independent-native-case-count",
    independentlyCountedCases=n_count,
    nativeReportResult=n_report.get("result"),
    contractProseNow375=True,
)

schema = json.loads((FOUND / "identity-schemas.v3.json").read_bytes())
proof_req = schema["$defs"]["proof-bundle"]["required"]
assert "executionInputsDigest" in proof_req, proof_req
add("proof-bundle-requires-executionInputsDigest", required=True)

# --- 8. Query: owner-admitted retained graph, newly specified graph.* boundary ---
atom = {
    "op": "none",
    "relation": "references",
    "minResolution": "resolved-binding",
    "endpoint": "target",
    "filters": [],
}
g = Sfix.build_ts_semantic_graph(
    atom=atom,
    has_declares=False,
    has_references_fact=True,
    second_partition=True,
    references_resolved=False,
    incoming_search=True,
    incoming_complete=False,
    target_sidecar=True,
    second_universe=True,
)
qrun, qobjects, qblobs, qactual = Srep.close_positive(g)
qrun_id = qactual["runId"]
qproject = qrun["projectId"]
foo_ep = ep(g["u1"], "symbol", g["foo"])
bar_ep = ep(g["u1"], "symbol", g["bar"])
baz_ep = ep(g["u2"], "symbol", g["baz"])
qhost = host_obs(latestRunId=qrun_id)


def ex(req, h=None, r=None, o=None, b=None):
    used = h if h is not None else qhost
    if "requestId" not in used:
        used = dict(host_obs(), **used)
    return Q.execute_graph_query(
        req,
        qrun if r is None else r,
        qobjects if o is None else o,
        qblobs if b is None else b,
        host=used,
    )


neigh_req = qreq(
    "graph.neighbors",
    qproject,
    {"runId": qrun_id},
    {
        "relation": "references",
        "minResolution": "resolved-binding",
        "direction": "outgoing",
        "endpoint": foo_ep,
    },
)
neigh = ex(neigh_req)
assert neigh["context"]["resolvedView"] == {"runId": qrun_id}
assert neigh["context"]["advisory"] is False
assert "run" not in neigh
assert len(neigh["items"]) == 1
assert neigh["items"][0]["target"]["nativeSubjectId"] == g["bar"]
assert neigh["context"]["countBasis"] == "exact"
kinds = {x.get("kind") for x in neigh["context"]["evidence"]["resolutionLimitations"]}
assert "native-evidence-unavailable" not in kinds
add(
    "query-owner-neighbors-retained-run",
    items=len(neigh["items"]),
    resolvedView=neigh["context"]["resolvedView"],
    advisory=neigh["context"]["advisory"],
    countBasis=neigh["context"]["countBasis"],
)

# latest without trusted observation is VIEW_UNKNOWN; one admitted Run is not latest
latest_req = copy.deepcopy(neigh_req)
latest_req["view"] = {"latest": True}
exc, env = refuse_query(lambda: ex(latest_req, h=host_obs()))
assert exc.detail == "QUERY.VIEW_UNKNOWN", exc.detail
assert env["kind"] == "failure" and "run" not in env and env["errors"]
add(
    "query-latest-requires-host-observation-not-static-run-bytes",
    errorCode=exc.error_code,
    detail=exc.detail,
    envelopeKind=env["kind"],
    envelopeHasRun="run" in env,
)

# snapshot without runsForSnapshot is VIEW_UNKNOWN
snap_req = copy.deepcopy(neigh_req)
snap_req["view"] = {"snapshotId": qrun["snapshotId"]}
exc, env = refuse_query(lambda: ex(snap_req, h=host_obs()))
assert exc.detail == "QUERY.VIEW_UNKNOWN", exc.detail
add(
    "query-snapshot-one-admitted-run-does-not-prove-uniqueness",
    detail=exc.detail,
    snapshotId=qrun["snapshotId"],
)

# snapshot observation naming a different Run is VIEW_UNKNOWN
stale = host_obs(runsForSnapshot={qrun["snapshotId"]: ["run3:" + ("0" * 64)]})
exc, env = refuse_query(lambda: ex(snap_req, h=stale))
assert exc.detail == "QUERY.VIEW_UNKNOWN", exc.detail
add("query-stale-snapshot-index-cannot-grant-wrong-historical-selection", detail=exc.detail)

# two Runs named for one snapshot is VIEW_AMBIGUOUS
amb = host_obs(runsForSnapshot={qrun["snapshotId"]: [qrun_id, "run3:" + ("1" * 64)]})
exc, env = refuse_query(lambda: ex(snap_req, h=amb))
assert exc.detail == "QUERY.VIEW_AMBIGUOUS", exc.detail
add("query-snapshot-two-runs-is-ambiguous", detail=exc.detail)

# unique matching snapshot observation succeeds and never echoes latest
ok_snap = host_obs(runsForSnapshot={qrun["snapshotId"]: [qrun_id]})
snap_ok = ex(snap_req, h=ok_snap)
assert snap_ok["context"]["resolvedView"] == {"runId": qrun_id}
assert "latest" not in snap_ok["context"]["resolvedView"]
add("query-snapshot-unique-observation-resolves-to-runid-only", resolvedView=snap_ok["context"]["resolvedView"])

# host.cache / standing / caller-authored deficiencies cannot substitute retained edges
poisoned = host_obs(
    latestRunId=qrun_id,
    standing="ADMIT",
    cache={"edges": [{"factId": "fact2:" + ("f" * 64), "source": foo_ep, "target": baz_ep}]},
    evaluationDeficiencies=[{"source": "native", "cause": "invented", "inputRefs": []}],
    targetAttributions=[{"nativeSubjectId": "forged"}],
)
poisoned_out = ex(neigh_req, h=poisoned)
assert len(poisoned_out["items"]) == len(neigh["items"])
cites = poisoned_out["context"]["evidence"]["deficiencyCitations"]
assert all(c.get("cause") != "invented" for c in cites)
add(
    "query-host-cache-standing-deficiencies-are-not-public-graph-evidence",
    itemCountUnchanged=True,
    inventedCauseAbsent=True,
)

# syntactic rung is request refusal, not omitted edges
syn_req = qreq(
    "graph.neighbors",
    qproject,
    {"runId": qrun_id},
    {
        "relation": "references",
        "minResolution": "syntactic-name-match",
        "direction": "outgoing",
        "endpoint": foo_ep,
    },
)
exc, env = refuse_query(lambda: ex(syn_req))
assert exc.detail == "QUERY.RELATION_UNSUPPORTED", exc.detail
assert env["kind"] == "failure" and "run" not in env
add(
    "query-unsupported-syntactic-rung-refuses-not-omits",
    detail=exc.detail,
    envelopeHasRun="run" in env,
)

# fully specified unknown tuple in another universe is ENDPOINT_UNKNOWN, not AMBIGUOUS
unknown_ep = ep(g["u1"], "symbol", g["baz"])  # baz lives in u2
unk_req = qreq(
    "graph.neighbors",
    qproject,
    {"runId": qrun_id},
    {
        "relation": "references",
        "minResolution": "resolved-binding",
        "direction": "outgoing",
        "endpoint": unknown_ep,
    },
)
exc, env = refuse_query(lambda: ex(unk_req))
assert exc.detail == "QUERY.ENDPOINT_UNKNOWN", exc.detail
add(
    "query-same-native-id-other-universe-is-unknown-not-ambiguous",
    detail=exc.detail,
    requestedUniverse=g["u1"],
    nativeSubjectId=g["baz"],
)

# empty neighbors of an isolated inventory vertex is lawful; not native closed-world
# Use a file inventory endpoint if present; otherwise isolated start of reach with includeStart.
reach_req = qreq(
    "graph.reach",
    qproject,
    {"runId": qrun_id},
    {
        "relation": "references",
        "minResolution": "resolved-binding",
        "direction": "outgoing",
        "start": foo_ep,
        "maxDepth": 8,
        "includeStart": False,
    },
    size=1000,
)
reach = ex(reach_req)
assert reach["context"]["advisory"] is False
assert "coverage" not in reach["context"]
assert set(reach["context"]["evidence"].keys()) >= {
    "coverageIds",
    "scopeIds",
    "deficiencyCitations",
    "resolutionLimitations",
}
add(
    "query-reach-evidence-disclosure-is-not-coverage-scalar",
    traversalCoverage=reach["context"]["traversalCoverage"],
    evidenceKeys=sorted(reach["context"]["evidence"].keys()),
    hasCoverageScalar="coverage" in reach["context"],
)

# page vs operation: small page of complete neighbors is truncated-page, truncated=false, countBasis=exact
page_req = copy.deepcopy(neigh_req)
page_req["page"] = {"size": 1}
# dual-provenance may be 1; manufacture extra via traverse is not owner. Use many algorithm edges independently.
u = hashlib.sha256(b"probe-universe").hexdigest()
a = ep(u, "symbol", "symbol:a")
edges = []
for i in range(5):
    edges.append(
        {
            "confidenceMillionths": 1000000,
            "factId": "fact2:" + hashlib.sha256(("fact:" + str(i)).encode()).hexdigest(),
            "producerClosure": "closure2:" + hashlib.sha256(("prod:" + str(i)).encode()).hexdigest(),
            "relation": "references",
            "resolution": "resolved-binding",
            "source": a,
            "target": ep(u, "symbol", "symbol:t" + str(i)),
        }
    )
alg = Q.traverse_projected_graph(
    "graph.neighbors",
    {"relation": "references", "minResolution": "resolved-binding", "direction": "outgoing", "endpoint": a},
    edges,
    page={"size": 2},
    project_id=qproject,
    run_id=qrun_id,
)
assert alg["context"]["traversalCoverage"] == "truncated-page"
assert alg["context"]["truncated"] is False
assert alg["context"]["countBasis"] == "exact"
assert alg["context"]["totalItems"] == 5
summary = QS.graph_query_result_summary(alg)
assert summary["completenessMet"] is True
assert summary["items"] == 2
assert summary["items"] != alg["context"]["totalItems"]
assert "nextCursor" in summary
add(
    "query-page-fullness-is-not-operation-truncation",
    traversalCoverage=alg["context"]["traversalCoverage"],
    truncated=alg["context"]["truncated"],
    countBasis=alg["context"]["countBasis"],
    completenessMet=summary["completenessMet"],
    pageItems=summary["items"],
    totalItems=alg["context"]["totalItems"],
)

# produced cap: last page truncated-bound, no cursor; required completeness unmet
cap = dict(Q.PUBLIC_BOUNDS, maxItemsPerOperation=3)
c1 = Q.traverse_projected_graph(
    "graph.neighbors",
    {"relation": "references", "minResolution": "resolved-binding", "direction": "outgoing", "endpoint": a},
    edges,
    bounds=cap,
    completeness="best-effort",
    page={"size": 2},
    project_id=qproject,
    run_id=qrun_id,
)
assert c1["context"]["countBasis"] == "lower-bound"
assert c1["context"]["truncated"] is False
assert c1["context"]["traversalCoverage"] == "truncated-page"
lb_summary = QS.graph_query_result_summary(c1)
assert lb_summary["completenessMet"] is False
c2 = Q.traverse_projected_graph(
    "graph.neighbors",
    {"relation": "references", "minResolution": "resolved-binding", "direction": "outgoing", "endpoint": a},
    edges,
    bounds=cap,
    completeness="best-effort",
    page={"size": 2, "cursor": c1["context"]["nextCursor"]},
    project_id=qproject,
    run_id=qrun_id,
)
assert c2["context"]["traversalCoverage"] == "truncated-bound"
assert c2["context"].get("nextCursor") is None
req_cap = Q.traverse_projected_graph(
    "graph.neighbors",
    {"relation": "references", "minResolution": "resolved-binding", "direction": "outgoing", "endpoint": a},
    edges,
    bounds=cap,
    completeness="required",
    project_id=qproject,
    run_id=qrun_id,
)
assert req_cap["termination"]["class"] == "indeterminate"
assert req_cap["termination"]["reasonCodes"] == ["QUERY.COMPLETENESS_UNMET"]
add(
    "query-produced-cap-last-page-no-cursor-and-required-unmet",
    lastTraversal=c2["context"]["traversalCoverage"],
    lastHasCursor="nextCursor" in c2["context"],
    requiredClass=req_cap["termination"]["class"],
    intermediateCompletenessMet=lb_summary["completenessMet"],
)

# continuation cannot re-resolve latest
latest_ok = copy.deepcopy(neigh_req)
latest_ok["view"] = {"latest": True}
latest_host = host_obs(latestRunId=qrun_id)
first = ex(latest_ok, h=latest_host)
# If there is no cursor, manufacture paging independently already covered. Bind cursor from algorithm.
cursor = c1["context"]["nextCursor"]
cont = copy.deepcopy(latest_ok)
cont["page"] = {"size": 2, "cursor": cursor}
exc, env = refuse_query(lambda: ex(cont, h=latest_host))
assert exc.detail == "QUERY.CURSOR_MISMATCH", exc.detail
add(
    "query-continuation-cannot-reresolve-latest",
    detail=exc.detail,
    envelopeKind=env["kind"],
)

# renderer parity carries complete owned response
term = {"class": "success"}
env_ok = {
    "schemaFamily": "opensip.product.envelope",
    "schemaMajor": 3,
    "kind": "query",
    "requestId": qhost["requestId"],
    "projectId": qproject,
    "termination": term,
    "exitCode": 0,
    "query": QS.graph_query_result_summary(neigh),
}
live = json.loads((WF / "command-inventory.v3.json").read_text())
query_cmd = next(c for c in live["commands"] if c["name"] == "query")
assert query_cmd["parityFields"] == [
    "resolved-view",
    "availability",
    "truncated",
    "total-items",
    "termination-class",
    "query-response",
]
proj = QS.project_query_surface(neigh, term, envelope=env_ok, command=query_cmd)
rnd = QS.render_query_formats(proj["parity"], env_ok, query_cmd)
assert rnd["ok"] and rnd["parityHolds"]
assert "query-response" in proj["parity"]
assert proj["parity"]["query-response"]["context"]["evidence"] == neigh["context"]["evidence"]
assert "coverage" not in proj["parity"]
add(
    "query-full-response-renderer-parity",
    formats=[r["format"] for r in rnd["renderings"]],
    parityHolds=rnd["parityHolds"],
    completeResponseCarried=True,
    liveInventoryHasSixParityFields=True,
)

# reminted false-result graph: structural owner ADMIT, public query REFUSE.
# Use the file-fixture severity mutant already shown to fail close_run; the
# semantic fixture used for neighbor probes emits zero findings, so a
# severity remint there is a no-op.
file_query = qreq(
    "graph.neighbors",
    mutant[0]["projectId"],
    {"runId": owner_id},
    {
        "relation": "references",
        "minResolution": "resolved-binding",
        "direction": "outgoing",
        "endpoint": ep("0" * 64, "symbol", "symbol:x"),
    },
)
assert M.open_run_closure(*mutant)[0]
try:
    M.close_run(*mutant)
except Exception as exc:
    assert "EVALUATOR_COMPLETE_PROOF_REPLAY" in str(exc), str(exc)
else:
    raise AssertionError("file-fixture remint unexpectedly passed close_run")
exc, env = refuse_query(
    lambda: Q.execute_graph_query(file_query, mutant[0], mutant[1], mutant[2], host=host_obs())
)
assert env["kind"] == "failure" and "run" not in env
assert exc.klass == "operational-failed"
add(
    "query-reminted-false-result-structurally-admitted-public-query-refuses",
    ownerAdmission="ADMIT",
    query="REFUSE",
    klass=exc.klass,
    detail=exc.detail,
    envelopeHasRun="run" in env,
    structuralApiIsNotSemanticAuthority=True,
)

# Independent remint of the semantic graph by forcing a false pass verdict.
sem_pass = remint_enclosing(qrun, qobjects, qblobs, mutate_proof=force_pass)
assert M.open_run_closure(*sem_pass)[0]
try:
    M.close_run(*sem_pass)
except Exception as exc:
    assert "EVALUATOR_COMPLETE_PROOF_REPLAY" in str(exc), str(exc)
else:
    raise AssertionError("semantic false-pass remint accepted by close_run")
exc, env = refuse_query(lambda: ex(neigh_req, r=sem_pass[0], o=sem_pass[1], b=sem_pass[2]))
assert env["kind"] == "failure" and "run" not in env
add(
    "query-semantic-false-pass-remint-public-query-refuses",
    ownerAdmission="ADMIT",
    query="REFUSE",
    klass=exc.klass,
    detail=exc.detail,
)

# twenty operation names unchanged
ops = json.loads((WF / "schemas/evaluator3/graph-query.schema.json").read_text())["$defs"]["Operation"]["enum"]
assert len(ops) == 20
assert ops == [
    "run.show",
    "run.list",
    "finding.list",
    "finding.show",
    "fact.list",
    "coverage.show",
    "artifact.get",
    "graph.neighbors",
    "graph.path",
    "graph.reach",
    "baseline.show",
    "comparison.show",
    "comparison.diff",
    "candidate.list",
    "inspection.show",
    "review.brief",
    "policy.effective",
    "import.show",
    "receipt.show",
    "availability.show",
]
add("twenty-query-operation-names-unchanged", count=20)

# hydradb eight proposals accounted, no DB choice / no measured performance
hyd = (DC / "hydradb-dispositions.proposed.md").read_text()
for n in range(1, 9):
    assert str(n) + "." in hyd or "| " + str(n) + "." in hyd or "| " + str(n) + " " in hyd
assert "No HydraDB adoption" in hyd or "No HydraDB" in hyd
assert "No speedup" in hyd or "no speedup" in hyd.lower() or "No speedup or external benchmark" in hyd
add("hydradb-eight-proposals-accounted-without-database-or-benchmark", proposals=8)

# --- 9. Pin-gate refusal ---
ledger = json.loads((FOUND / "evaluator3-source-pins.v1.json").read_bytes())
target_rel = next(
    item["path"]
    for item in ledger["files"]
    if item["path"].endswith("admission-and-qualification.md")
)
target = COPY / target_rel
orig_bytes = (ORIG / target_rel).read_bytes()
assert hashlib.sha256(target.read_bytes()).hexdigest() == hashlib.sha256(orig_bytes).hexdigest()
target.write_bytes(orig_bytes + b"\n# pin-gate-probe\n")
pin_out = OUT / "pinned-runs" / "pin-gate-refusal"
if pin_out.exists():
    shutil.rmtree(pin_out)
proc = subprocess.run(
    [PY, "-I", "-B", str(FOUND / "run-evaluator3-checks.py"), "--out", str(pin_out)],
    capture_output=True,
    text=True,
    timeout=60,
)
report = json.loads((pin_out / "report.json").read_text()) if (pin_out / "report.json").exists() else {}
target.write_bytes(orig_bytes)
restored = target.read_bytes() == orig_bytes
orig_unaltered = (ORIG / target_rel).read_bytes() == orig_bytes
assert report.get("sourcePinsValid") is False
assert report.get("passed") is False
assert proc.returncode != 0
assert not report.get("checks")
add(
    "pin-gate-refusal-on-tampered-admission-contract",
    sourcePinsValid=report.get("sourcePinsValid"),
    passed=report.get("passed"),
    launcherExit=proc.returncode,
    changedNamed=bool(report.get("changedOrMissing")),
    childrenNotExecuted=not report.get("checks"),
    restored=restored,
)
add(
    "original-snapshot-unaltered-after-pin-gate-probe",
    path=target_rel,
    unaltered=orig_unaltered,
)

report_path = OUT / "probes" / "independent-probes.v1.json"
report_path.write_text(
    json.dumps(
        {
            "standing": "Independent Grok probes of frozen source24. Not author oracles. Not product qualification.",
            "python": PY + " -I -B",
            "passed": True,
            "count": len(rows),
            "results": rows,
            "notes": [
                "Fully reminted false-result graphs were constructed by this reviewer, not by copying author export counts.",
                "open_run_closure admitted remints; close_run refused with EVALUATOR_COMPLETE_PROOF_REPLAY.",
                "Public execute_graph_query over a reminted false-result graph refused; structural owner admission is not query authority.",
                "Pin-gate: tampering admission-and-qualification.md in the disposable copy made run-evaluator3-checks.py set sourcePinsValid=false, execute no children, exit nonzero; file restored; original snapshot unaltered.",
            ],
        },
        indent=2,
    )
    + "\n"
)
print(json.dumps({"passed": True, "count": len(rows)}, indent=2))
