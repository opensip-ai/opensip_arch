"""R2 controls in check-workflow-projection.v3.py: inventory drift, closed query-step params, and typed carriers for the
eight non-graph query-class commands over actual owner records (the graph query command is controlled in
check-query-projection.v3.py over an owner-admitted retained Run)."""
import json, sys
sys.path.insert(0, '/private/tmp/opensip-design-corrections/claude-consumer24-workflow-author.v2/tools')
from textedit import apply  # noqa: E402

CWP = 'docs/coop/design-corrections/workflows/check-workflow-projection.v3.py'

R2_CONTROLS = r'''
# ----------------------------------------------------------------------------- R2 (v2): closed dispatch and typed public carriers for all nine query-class commands
_qs_spec = importlib.util.spec_from_file_location("r2_query_surface", HERE / "query_surface_projection.v3.py")
QS = importlib.util.module_from_spec(_qs_spec)
_qs_spec.loader.exec_module(QS)
_R2_INV = json.loads((HERE / "command-inventory.v3.json").read_text())
_R2_CMD = {c["name"]: c for c in _R2_INV["commands"]}
_R2_QUERY_CLASS = [c for c in _R2_INV["commands"] if c["requestClass"] == "query"]
_R2_ENV = U + "command-envelope:3"
_R2_GQ_OPS = SCHEMAS[U + "graph-query:3"]["$defs"]["Operation"]["enum"]
_R2_HOST_OPS = SCHEMAS[U + "invocation:3"]["$defs"]["HostQueryOperation"]["enum"]
_R2_NINE = ["query", "recommend", "baseline-show", "policy-show", "policy-test", "candidates", "inspect", "review-brief", "repair-preview"]

check("r2-inventory-exactly-the-nine-query-class-commands-dispatch", sorted(c["name"] for c in _R2_QUERY_CLASS) == sorted(_R2_NINE) and all("queryDispatch" in c for c in _R2_QUERY_CLASS))
check("r2-inventory-no-other-command-dispatches", all("queryDispatch" not in c for c in _R2_INV["commands"] if c["requestClass"] != "query"))
check("r2-inventory-surfaces-are-the-closed-envelope-selector", sorted(c["queryDispatch"]["surface"] for c in _R2_QUERY_CLASS) == sorted(SCHEMAS[_R2_ENV]["properties"]["querySurface"]["enum"]))
check("r2-inventory-parity-paths-cover-exactly-parity-fields", all(set(c["queryDispatch"]["parityPaths"]) == set(c["parityFields"]) for c in _R2_QUERY_CLASS))
check("r2-inventory-dispatch-step-is-a-declared-command-step", all(c["queryDispatch"]["stepKind"] in c["steps"] for c in _R2_QUERY_CLASS))
check("r2-public-graph-query-operation-enum-is-not-widened", len(_R2_GQ_OPS) == 20 and not (set(_R2_HOST_OPS) & set(_R2_GQ_OPS)))
check("r2-query-command-dispatches-exactly-the-twenty-public-operations", _R2_CMD["query"]["queryDispatch"]["operations"] == _R2_GQ_OPS)
check("r2-host-operations-are-exactly-the-mapped-host-dispatches", sorted(op for c in _R2_QUERY_CLASS for op in c["queryDispatch"]["operations"] if op not in _R2_GQ_OPS) == sorted(_R2_HOST_OPS))
check("r2-single-operation-commands-and-repair-preview-own-step",
      all(len(_R2_CMD[n]["queryDispatch"]["operations"]) == 1 for n in _R2_NINE if n not in ("query", "repair-preview"))
      and _R2_CMD["repair-preview"]["queryDispatch"]["stepKind"] == "repair-preview" and _R2_CMD["repair-preview"]["queryDispatch"]["operations"] == [])
check("r2-candidates-and-inspect-dispatch-public-operations", [_R2_CMD[n]["queryDispatch"]["operations"][0] for n in ("candidates", "inspect")] == ["candidate.list", "inspection.show"])
must_valid("r2-inventory-instance-admitted", U + "command-inventory:3", _R2_INV)
_r2_mut = copy.deepcopy(_R2_CMD["candidates"])
del _r2_mut["queryDispatch"]
must_invalid("r2-inventory-query-class-command-without-dispatch-refused", U + "command-inventory:3#/$defs/Command", _r2_mut)
_r2_mut = copy.deepcopy(_R2_CMD["import"])
_r2_mut["queryDispatch"] = copy.deepcopy(_R2_CMD["candidates"]["queryDispatch"])
must_invalid("r2-inventory-non-query-command-with-dispatch-refused", U + "command-inventory:3#/$defs/Command", _r2_mut)
_r2_mut = copy.deepcopy(_R2_CMD["candidates"])
_r2_mut["queryDispatch"]["operations"] = ["candidates.list"]
must_invalid("r2-inventory-unclosed-operation-refused", U + "command-inventory:3#/$defs/Command", _r2_mut)
_r2_mut = copy.deepcopy(_R2_CMD["candidates"])
_r2_mut["queryDispatch"]["surface"] = "command-owned-summary"
must_invalid("r2-inventory-retired-selector-refused", U + "command-inventory:3#/$defs/Command", _r2_mut)

_r2_public_step = {"kind": "query", "operation": qreq["operation"], "completeness": qreq["completeness"], "page": qreq["page"], "request": qreq}
check("r2-public-query-step-admitted-with-request-join", QS.admit_query_step_params(_r2_public_step) is _r2_public_step)
must_invalid("r2-public-query-step-without-request-refused", U + "invocation:3#/$defs/QueryParams", {k: v for k, v in _r2_public_step.items() if k != "request"})
try:
    QS.admit_query_step_params(dict(_r2_public_step, operation="finding.list"))
    check("r2-public-query-step-request-operation-join", False, "admitted")
except QS.QuerySurfaceProjectionError as _r2_exc:
    check("r2-public-query-step-request-operation-join", _r2_exc.code == "QUERY_SURFACE_STEP_REQUEST_JOIN", _r2_exc.code)
_r2_host_requests = {
    "baseline.inspect": {"operation": "baseline.inspect", "path": "opensip.baseline.json"},
    "discovery.recommend": {"operation": "discovery.recommend", "emitConfigProposalPath": "opensip.config.proposal.json"},
    "policy.show": {"operation": "policy.show"},
    "policy.test": {"operation": "policy.test", "suitePath": "policy-tests/suite.json"},
    "review.produce-brief": {"operation": "review.produce-brief", "view": {"latest": True}, "producer": {"kind": "policy-rule", "id": "opensip.review.heuristic"}},
}
check("r2-every-host-operation-has-an-admitted-closed-request",
      sorted(_r2_host_requests) == sorted(_R2_HOST_OPS)
      and all(QS.admit_query_step_params({"kind": "query", "operation": op, "request": req}) for op, req in _r2_host_requests.items()))
must_invalid("r2-host-operation-with-another-operation-request-refused", U + "invocation:3#/$defs/QueryParams", {"kind": "query", "operation": "policy.test", "request": _r2_host_requests["policy.show"]})
must_invalid("r2-host-operation-with-graph-request-refused", U + "invocation:3#/$defs/QueryParams", {"kind": "query", "operation": "policy.test", "completeness": "required", "page": {"size": 1}, "request": qreq})
must_invalid("r2-public-operation-spelled-as-host-operation-refused", U + "invocation:3#/$defs/QueryParams", {"kind": "query", "operation": "candidate.list", "request": {"operation": "candidate.list"}})
must_invalid("r2-host-request-extra-member-refused", U + "invocation:3#/$defs/QueryParams", {"kind": "query", "operation": "policy.show", "request": {"operation": "policy.show", "asOfDate": "2026-09-12"}})
must_invalid("r2-model-producer-without-closure-refused", U + "invocation:3#/$defs/QueryParams", {"kind": "query", "operation": "review.produce-brief", "request": {"operation": "review.produce-brief", "view": {"latest": True}, "producer": {"kind": "model", "id": "m"}}})


def _r2_envelope(surface, record, project):
    env = {"schemaFamily": "opensip.product.envelope", "schemaMajor": 3, "kind": "query", "requestId": "req1_" + "d" * 32,
           "projectId": project, "termination": {"class": "success"}, "exitCode": 0, "querySurface": surface, "queryRecord": record}
    env["query"] = QS.command_surface_summary(surface, record, env)
    return env


_R2_ENVS = {}
_R2_COMMAND_OF = {}
# candidates / inspect / review brief over a close_run-admitted Run with one real suppressing disposition.
_r2_graph = RC.positive(symbol_rows=[_S7_X1, _S7_X2], scope_document=SCOPE_ALL)
_r2_view0 = P.project_admitted_run_v3(*_r2_graph)
_r2_suppressed_id = _r2_view0["candidates"][0]["candidateId"]
_r2_view = P.project_admitted_run_v3(*_r2_graph, dispositions={_r2_suppressed_id: {"disposition": "reject", "suppressUntil": "2026-12-31", "receiptId": hid("receipt2", "r2-review")}},
                                     suppression_today="2026-09-12")
_r2_project = _r2_view["projectId"]
check("r2-candidates-fixture-has-one-suppressed-candidate", len(_r2_view["candidates"]) == 2 and sum(1 for c in _r2_view["candidates"] if c["suppressed"]) == 1)
for _incl, _key in ((True, "candidates"), (False, "candidates-hidden")):
    _r2_list = P.project_candidate_list(_r2_view, _incl)
    _R2_ENVS[_key] = _r2_envelope("candidate-list", {"surface": "candidate-list", "context": P.non_graph_query_context(_r2_view, len(_r2_list["candidates"]), True),
                                                     "includeSuppressed": _incl, "candidates": _r2_list["candidates"], "evidenceLevels": _r2_list["evidenceLevels"],
                                                     "suppressedCount": _r2_list["suppressedCount"]}, _r2_project)
    _R2_COMMAND_OF[_key] = "candidates"
check("r2-hidden-listing-still-counts-suppressed", _R2_ENVS["candidates-hidden"]["queryRecord"]["suppressedCount"] == 1 and len(_R2_ENVS["candidates-hidden"]["queryRecord"]["candidates"]) == 1)
_r2_inspect_id = next(c["candidateId"] for c in _r2_view["candidates"] if not c["suppressed"])
_r2_bundle = P.project_inspection_bundle(_r2_view, _r2_inspect_id)
_R2_ENVS["inspect"] = _r2_envelope("candidate-inspection", {"surface": "candidate-inspection", "context": P.non_graph_query_context(_r2_view, len(_r2_bundle["facts"]), True),
                                                            "inspection": _r2_bundle}, _r2_project)
_R2_COMMAND_OF["inspect"] = "inspect"
must_valid("r2-inspection-bundle-owner-schema", U + "review:2#/$defs/InspectionBundle", _r2_bundle)
reject("r2-inspect-unknown-candidate-refused", lambda: P.project_inspection_bundle(_r2_view, hid("candidate2", "unknown")), "IDENTITY.UNKNOWN", "REVIEW.CANDIDATE_UNKNOWN")
_r2_ids = [c["candidateId"] for c in _r2_view["candidates"]]
_r2_producer = {"kind": "model", "id": "fixture-model", "modelClosureId": DET}
_R2_ENVS["review-brief"] = _r2_envelope("review-brief", {"surface": "review-brief", "context": P.non_graph_query_context(_r2_view, len(_r2_ids), True),
                                                         "brief": P.W.review_brief(_r2_view["runId"], _r2_ids, _r2_producer)}, _r2_project)
_R2_ENVS["review-brief-truncated"] = _r2_envelope("review-brief", {"surface": "review-brief", "context": P.non_graph_query_context(_r2_view, len(_r2_ids), True, truncated=True),
                                                                   "brief": P.W.review_brief(_r2_view["runId"], _r2_ids, _r2_producer, limit=1)}, _r2_project)
_R2_COMMAND_OF["review-brief"] = _R2_COMMAND_OF["review-brief-truncated"] = "review-brief"
# policy show through the owner resolvers.
_r2_policy = WF3.resolve_policy(copy.deepcopy(_r2_view["policy"]))
_r2_fp = next(o["finding"]["fingerprint"] for o in _r2_view["occurrences"] if o["finding"]["fingerprint"])
_r2_waivers = {"schemaFamily": "opensip.product.waivers", "schemaMajor": 1, "waivers": [
    {"waiverId": "w-active", "target": {"ruleId": _r2_view["policy"]["rules"][0]["ruleId"], "subjectPath": "src/index.ts"}, "reason": "reviewed", "expires": None},
    {"waiverId": "w-expired", "target": {"fingerprint": _r2_fp}, "reason": "superseded", "expires": "2026-01-01"}]}
_r2_effective, _r2_resolution = P.W.resolve_waivers(_r2_waivers, "2026-09-12")
check("r2-policy-show-resolution-discloses-expired-waiver", _r2_resolution["expired"] == ["w-expired"] and _r2_resolution["effectiveCount"] == 1)
_R2_ENVS["policy-show"] = _r2_envelope("effective-policy", {"surface": "effective-policy", "policyDigest": P.doc_digest(_r2_policy), "policy": _r2_policy,
                                                            "waiverSetDigest": P.doc_digest(_r2_effective), "effectiveWaivers": _r2_effective, "waiverResolution": _r2_resolution}, _r2_project)
_R2_COMMAND_OF["policy-show"] = "policy-show"
reject("r2-policy-show-duplicate-waiver-is-a-refusal", lambda: P.W.resolve_waivers({"schemaFamily": "opensip.product.waivers", "schemaMajor": 1,
                                                                                    "waivers": [_r2_waivers["waivers"][0], dict(_r2_waivers["waivers"][0], waiverId="w-dup")]}, "2026-09-12"),
       "CONFIG.INVALID", "POLICY.DUPLICATE_WAIVER")
# policy test through the owner authoring test over the retained suite fixture.
_r2_policy_result, _r2_policy_refusal = P.W.run_policy_test(json.loads((HERE / "workflow-cases.v1.json").read_text())["policySuite"])
check("r2-policy-test-owner-result-produced", _r2_policy_refusal is None and _r2_policy_result["resolverAccepted"] is True)
_R2_ENVS["policy-test"] = _r2_envelope("policy-test-result", {"surface": "policy-test-result", "result": _r2_policy_result}, _r2_project)
_R2_COMMAND_OF["policy-test"] = "policy-test"
# baseline show through adoption, admission and current-trust pivot resolution.
_r2_art = P.adopt_admitted_baseline_v3(*_r2_graph, CUSTODY)
_r2_host = host_from_graph({"runId": _r2_art["descriptor"]["runId"]}, _r2_graph[1])
for _r2_rec in _r2_host["closures"].values():
    _r2_rec["trustOrigin"] = "retained-generation"
_r2_rows = P.pivot_closure_availability(_r2_art, _r2_host)
check("r2-baseline-show-all-pivots-available", bool(_r2_rows) and all(r["state"] == "available" and r["trustOrigin"] == "retained-generation" for r in _r2_rows))
_R2_ENVS["baseline-show"] = _r2_envelope("baseline-inspection", {"surface": "baseline-inspection", "baseline": _r2_art, "pivotClosureAvailability": _r2_rows}, _r2_project)
_r2_host_bad = copy.deepcopy(_r2_host)
_r2_pivots = [p["closureId"] for p in _r2_art["descriptor"]["pivotClosure"]]
_r2_host_bad["closures"].pop(_r2_pivots[0])
if len(_r2_pivots) > 1:
    _r2_host_bad["closures"][_r2_pivots[1]]["trust"] = "revoked"
_r2_rows_bad = P.pivot_closure_availability(_r2_art, _r2_host_bad)
check("r2-baseline-show-missing-and-revoked-pivots-are-data",
      _r2_rows_bad[0]["state"] == "missing" and "trustOrigin" not in _r2_rows_bad[0] and (len(_r2_pivots) < 2 or _r2_rows_bad[1]["state"] == "revoked"))
_R2_ENVS["baseline-show-unavailable"] = _r2_envelope("baseline-inspection", {"surface": "baseline-inspection", "baseline": _r2_art, "pivotClosureAvailability": _r2_rows_bad}, _r2_project)
_R2_COMMAND_OF["baseline-show"] = _R2_COMMAND_OF["baseline-show-unavailable"] = "baseline-show"
_r2_no_origin = copy.deepcopy(_r2_host)
next(iter(_r2_no_origin["closures"].values())).pop("trustOrigin")
reject("r2-baseline-show-available-without-trust-origin-refused", lambda: P.pivot_closure_availability(_r2_art, _r2_no_origin), "REQUEST.PRECONDITION_FAILED", "EVALUATION.PROJECTION_INPUT_INCOMPLETE")
# recommend through security discovery joined by native unit discovery (fixture copied from the security owner's P3 case).
_r2_sec_spec = importlib.util.spec_from_file_location("r2_security_model", HERE.parent / "security" / "security_lifecycle_model_v1.py")
_R2_SEC = importlib.util.module_from_spec(_r2_sec_spec)
_r2_sec_spec.loader.exec_module(_R2_SEC)
_r2_nat_spec = importlib.util.spec_from_file_location("r2_native_model", HERE.parent / "native" / "native_evidence_model.v2.py")
_R2_NAT = importlib.util.module_from_spec(_r2_nat_spec)
_r2_nat_spec.loader.exec_module(_R2_NAT)
_R2_ROOT = "/home/alice/repo"


def _r2_dir(**kw):
    return dict({"kind": "dir", "uid": 1000, "mode": "0755", "dev": 1}, **kw)


def _r2_file():
    return {"kind": "file", "uid": 1000, "mode": "0644", "nlink": 1, "size": 10}


_r2_fs = {"/": {"kind": "dir", "uid": 0, "mode": "0755", "dev": 1}, "/home": {"kind": "dir", "uid": 0, "mode": "0755", "dev": 1},
          "/home/alice": _r2_dir(mode="0700"), _R2_ROOT: _r2_dir(vcs=True), _R2_ROOT + "/package.json": _r2_file(),
          _R2_ROOT + "/vendor": _r2_dir(), _R2_ROOT + "/vendor/lib": _r2_dir(vcs=True), _R2_ROOT + "/vendor/lib/package.json": _r2_file(), _R2_ROOT + "/vendor/lib/src": _r2_dir(),
          _R2_ROOT + "/vendor/lib/node_modules": _r2_dir(), _R2_ROOT + "/vendor/lib/node_modules/x": _r2_dir(), _R2_ROOT + "/vendor/lib/node_modules/x/package.json": _r2_file(),
          _R2_ROOT + "/apps": _r2_dir(), _R2_ROOT + "/apps/site": _r2_dir(), _R2_ROOT + "/apps/site/opensip.json": _r2_file(), _R2_ROOT + "/apps/site/package.json": _r2_file(),
          _R2_ROOT + "/apps/site/sub": _r2_dir(), _R2_ROOT + "/apps/site/sub/Cargo.toml": _r2_file()}
_r2_sd = _R2_SEC.discovery({"invokingUid": 1000, "accountHome": "/home/alice", "cwd": _R2_ROOT, "fs": _r2_fs})
_r2_inv = _R2_SEC.boundary_inventory(_r2_sd)
_r2_markers = {p[len(_R2_ROOT) + 1:]: {"sha256": "1" * 64} for p, e in _r2_fs.items()
               if p.startswith(_R2_ROOT + "/") and e["kind"] == "file" and p.rpartition("/")[2] in _R2_SEC.WORKSPACE_MARKERS}
_r2_discovery = _R2_NAT.discover_units(_r2_markers, None, _r2_inv)
check("r2-recommend-discovery-is-boundary-admitted-native-output",
      _r2_sd["status"] == "ACCEPT" and _r2_discovery["refused"] is None and _r2_discovery["boundaries"]["source"] == "security.discovery" and bool(_r2_discovery["units"]))
_r2_roots = sorted({QS.DD.spell_root(u["rootPath"]) for u in _r2_discovery["units"]})
_R2_ENVS["recommend"] = _r2_envelope("discovery-recommendation", {"surface": "discovery-recommendation", "advisory": True, "discovery": _r2_discovery, "recommendations": [],
                                                                  "config2Proposals": [{"key": "discovery.workspaceRoots", "workspaceRoots": _r2_roots,
                                                                                        "unitOrdinals": [u["unitOrdinal"] for u in _r2_discovery["units"]]}]}, _r2_project)
_R2_COMMAND_OF["recommend"] = "recommend"
_r2_refused = _R2_NAT.discover_units(_r2_markers, ["vendor/lib"], _r2_inv)
check("r2-recommend-boundary-crossing-root-is-a-native-refusal", _r2_refused["refused"] is not None and _r2_refused["refused"]["detail"] == "native.explicit-root-crosses-boundary")
_r2_refused_env = copy.deepcopy(_R2_ENVS["recommend"])
_r2_refused_env["queryRecord"]["discovery"] = _r2_refused
must_invalid("r2-recommend-refused-discovery-is-never-carried", _R2_ENV, _r2_refused_env)
_r2_unregistered = copy.deepcopy(_R2_ENVS["recommend"])
_r2_unregistered["queryRecord"]["recommendations"] = [{"code": "RECOMMEND.ANYTHING", "remedy": "r"}]
must_invalid("r2-recommend-unregistered-recommendation-refused", _R2_ENV, _r2_unregistered)
# repair preview from the admitted closed-world preview; the reference constructor still emits a major-1 descriptor.
_r2_desc = copy.deepcopy(cw_pos_plan["descriptor"])
check("r2-repair-preview-reference-constructor-emits-historical-major-1", _r2_desc["schemaMajor"] == 1)
_r2_desc["schemaMajor"] = 2
_r2_plan = {"repairPlanId": P.W.wid("repairplan2", "workflow.repair-plan", _r2_desc), "descriptor": _r2_desc}
must_valid("r2-repair-preview-plan-admitted-as-repair-2", U + "repair:2#/$defs/RepairPlanV1", _r2_plan)
_r2_preview = {"kind": "repair-preview", "repairPlanId": _r2_plan["repairPlanId"], "snapshotId": _r2_desc["snapshotId"], "applicable": _r2_desc["applicable"],
               "unmetPreconditions": copy.deepcopy(_r2_desc["unmetPreconditions"])}
must_valid("r2-repair-preview-result-owner-schema", U + "invocation:3#/$defs/RepairPreviewResult", _r2_preview)
_R2_ENVS["repair-preview"] = _r2_envelope("repair-preview", {"surface": "repair-preview", "preview": _r2_preview, "plan": _r2_plan}, _r2_desc["projectId"])
_R2_COMMAND_OF["repair-preview"] = "repair-preview"


def _r2_bump(path, delta=1):
    def mutate(env):
        node = env
        for token in path[:-1]:
            node = node[token]
        node[path[-1]] = node[path[-1]] + delta
    return mutate


def _r2_set(path, value):
    def mutate(env):
        node = env
        for token in path[:-1]:
            node = node[token]
        node[path[-1]] = value
    return mutate


_R2_MUTANTS = {
    "candidates": (_r2_bump(["queryRecord", "evidenceLevels", "proof-backed"]), "QUERY_SURFACE_EVIDENCE_LEVEL_JOIN"),
    "candidates-hidden": (_r2_set(["queryRecord", "includeSuppressed"], True), "QUERY_SURFACE_SUPPRESSED_COUNT_JOIN"),
    "inspect": (_r2_bump(["queryRecord", "context", "totalItems"]), "QUERY_SURFACE_TOTAL_ITEMS_JOIN"),
    "review-brief": (_r2_set(["queryRecord", "brief", "truncated"], True), "QUERY_SURFACE_TRUNCATED_JOIN"),
    "review-brief-truncated": (_r2_set(["queryRecord", "context", "totalItems"], 1), "QUERY_SURFACE_TOTAL_ITEMS_JOIN"),
    "policy-show": (_r2_set(["queryRecord", "policyDigest"], "0" * 64), "QUERY_SURFACE_POLICY_DIGEST_JOIN"),
    "policy-test": (_r2_bump(["queryRecord", "result", "summary", "passed"]), "QUERY_SURFACE_POLICY_TEST_ID_JOIN"),
    "baseline-show": (lambda env: env["queryRecord"]["pivotClosureAvailability"].pop(), "QUERY_SURFACE_PIVOT_AVAILABILITY_JOIN"),
    "baseline-show-unavailable": (_r2_set(["queryRecord", "baseline", "baselineId"], "baseline2:" + "0" * 64), "QUERY_SURFACE_BASELINE_NOT_ADMITTED"),
    "recommend": (_r2_set(["queryRecord", "config2Proposals", 0, "workspaceRoots"], ["not/discovered"]), "QUERY_SURFACE_CONFIG2_ROOT_NOT_DISCOVERED"),
    "repair-preview": (lambda env: env["queryRecord"]["preview"].__setitem__("applicable", not env["queryRecord"]["preview"]["applicable"]), "QUERY_SURFACE_REPAIR_PREVIEW_JOIN"),
}
check("r2-every-non-graph-command-has-positive-envelopes", sorted(set(_R2_COMMAND_OF.values())) == sorted(n for n in _R2_NINE if n != "query") and sorted(_R2_MUTANTS) == sorted(_R2_ENVS))
for _key, _name in _R2_COMMAND_OF.items():
    _cmd = _R2_CMD[_name]
    _env = _R2_ENVS[_key]
    must_valid("r2-%s-positive-envelope-admitted" % _key, _R2_ENV, _env)
    try:
        _proj = QS.project_command_surface(_env, _cmd)
        _rnd = QS.render_command_formats(_env, _cmd, hints=["advisory hint"])
        _bodies = {r["format"]: r["body"] for r in _rnd["renderings"]}
        check(
            "r2-%s-parity-read-at-paths-and-recovered-from-every-rendering" % _key,
            _rnd["ok"] and _rnd["parityHolds"] and set(_bodies) == {"human", "json", "agent"}
            and all(canonical.equal_typed(_proj["parity"][f], QS.json_pointer(_env, p)) for f, p in _cmd["queryDispatch"]["parityPaths"].items())
            and _bodies["json"] == _env and _bodies["agent"]["agentHints"] == ["advisory hint"],
            _rnd.get("ok"),
        )
        _lines = _bodies["human"].splitlines()
        _label = _lines[0].partition(": ")[0]
        _lines[0] = _label + ": " + json.dumps({"mutated": True})
        check("r2-%s-mutated-human-parity-detected" % _key, not canonical.equal_typed(QS.parity_from_human("\n".join(_lines) + "\n")[_label], _rnd["parity"][_label]))
    except Exception as _r2_exc:
        check("r2-%s-parity-read-at-paths-and-recovered-from-every-rendering" % _key, False, type(_r2_exc).__name__ + ": " + str(_r2_exc)[:200])
    _missing = copy.deepcopy(_env)
    del _missing["queryRecord"]
    must_invalid("r2-%s-missing-carrier-refused" % _key, _R2_ENV, _missing)
    _missing_render = QS.render_command_formats(_missing, _cmd)
    check("r2-%s-missing-carrier-is-precommit-delivery-fault" % _key,
          _missing_render["ok"] is False and "runId" not in _missing_render["deliveryTermination"]
          and _missing_render["deliveryTermination"]["domainDetail"]["code"] == "DELIVERY.REQUIRED_PROJECTION_FAILED")
    _other = next(e for e in _R2_ENVS.values() if e["querySurface"] != _env["querySurface"])
    _cross = copy.deepcopy(_env)
    _cross["queryRecord"] = copy.deepcopy(_other["queryRecord"])
    must_invalid("r2-%s-cross-command-carrier-refused" % _key, _R2_ENV, _cross)
    try:
        QS.project_command_surface(copy.deepcopy(_other), _cmd)
        check("r2-%s-another-command-surface-refused" % _key, False, "admitted")
    except QS.QuerySurfaceProjectionError as _r2_exc:
        check("r2-%s-another-command-surface-refused" % _key, _r2_exc.code == "QUERY_SURFACE_ENVELOPE_SELECTOR", _r2_exc.code)
    _untyped = copy.deepcopy(_env)
    _untyped["queryRecord"]["data"] = {"untyped": True}
    must_invalid("r2-%s-untyped-member-refused" % _key, _R2_ENV, _untyped)
    _mutate, _code = _R2_MUTANTS[_key]
    _mutant = copy.deepcopy(_env)
    _mutate(_mutant)
    must_valid("r2-%s-join-mutant-is-schema-valid" % _key, _R2_ENV, _mutant)
    try:
        QS.project_command_surface(_mutant, _cmd)
        check("r2-%s-join-mutant-refused-before-rendering" % _key, False, "admitted")
    except QS.QuerySurfaceProjectionError as _r2_exc:
        check("r2-%s-join-mutant-refused-before-rendering" % _key, _r2_exc.code == _code, _r2_exc.code)
_r2_summary_mutant = copy.deepcopy(_R2_ENVS["candidates"])
_r2_summary_mutant["query"]["items"] += 1
try:
    QS.project_command_surface(_r2_summary_mutant, _R2_CMD["candidates"])
    check("r2-compact-query-result-join-refused", False, "admitted")
except QS.QuerySurfaceProjectionError as _r2_exc:
    check("r2-compact-query-result-join-refused", _r2_exc.code == "QUERY_SURFACE_QUERYRESULT_JOIN", _r2_exc.code)
'''

row = apply('R2 controls', CWP, [
    ('''      and P.baseline_presence_knowledge("finding-key2:" + "f" * 64, _r1b_rule, {}, _r1b_rules, art_un["descriptor"], "src/other.ts") is False)
''', '''      and P.baseline_presence_knowledge("finding-key2:" + "f" * 64, _r1b_rule, {}, _r1b_rules, art_un["descriptor"], "src/other.ts") is False)
''' + R2_CONTROLS),
])
print(json.dumps(row, indent=1))
