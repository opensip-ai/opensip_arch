"""Deterministic fixture builder for the report-projection author candidate.

Positive documents are assembled from the pinned independent witness corpus
(m1-schema-witnesses-01) plus small labelled constructions. They are shape and
join test material only; they are not semantic evidence about any repository.
"""
import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
WITNESSES = Path("/tmp/opensip-implementation/m1-schema-witnesses-01/witnesses.json")
ENV = "urn:opensip:product-v1:workflows:evaluator3:command-envelope:4"


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def pick(cases, ref, kind=None, index=0):
    rows = [c["value"] for c in cases if c["ref"] == ref and (kind is None or c["origin"]["kind"] == kind)]
    return copy.deepcopy(rows[index])


def h(n):
    return hashlib.sha256(("report-projection-fixture:" + str(n)).encode()).hexdigest()


def build():
    schema = json.loads((HERE / "report-projection.schema.json").read_bytes())
    budget = {k: v["const"] for k, v in schema["$defs"]["BudgetProfileV1"]["properties"].items() if "const" in v}
    budget["browserLimits"] = {k: v["const"] for k, v in schema["$defs"]["BudgetProfileV1"]["properties"]["browserLimits"]["properties"].items()}
    views = {}
    for block in schema["allOf"]:
        cmd = block.get("if", {}).get("properties", {}).get("command", {}).get("const")
        if cmd:
            views[cmd] = block["then"]["properties"]["supportedReportViews"]["const"]
    cases = json.loads(WITNESSES.read_bytes())["cases"]

    reach = pick(cases, "urn:opensip:product-v1:workflows:evaluator3:graph-query:3#/$defs/GraphQueryResponseV1", "harvest-seed")
    run_id = reach["context"]["resolvedView"]["runId"]
    project = reach["context"]["projectId"]
    coverage_id = reach["context"]["evidence"]["coverageIds"][0]
    prior = pick(cases, "urn:opensip:product-v1:workflows:evaluator3:invocation:3#/$defs/AnalysisResult", "harvest-seed")
    plan_id = prior["planId"]
    comparison = pick(cases, "urn:opensip:product-v1:workflows:evaluator3:comparison:2#")
    comparison["descriptor"]["currentRunId"] = run_id
    baseline_id = comparison["descriptor"]["baselineId"]
    coverage = pick(cases, "urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/CoverageResultV3")
    rule = pick(cases, "urn:opensip:product-v1:policy-document:2#/$defs/Rule")
    rule["ruleId"] = "no-unused-export"
    rule["ruleProgramRef"]["ruleStableId"] = "no-unused-export"
    failure = pick(cases, "urn:opensip:product-v1:workflows:evaluator3:command-envelope:3#", "harvest-seed")
    failure["schemaMajor"] = 4
    candidate_list = pick(cases, ENV + "#/$defs/CandidateListRecordV1")
    inspection = pick(cases, ENV + "#/$defs/CandidateInspectionRecordV1")
    repair = pick(cases, ENV + "#/$defs/RepairPreviewRecordV1")

    finding = {
        "findingId": "finding3:" + h("finding"), "ruleId": "no-unused-export", "subjectId": "subject3:" + h("subject"),
        "subjectPath": "src/legacy.js", "subjectKind": "file", "severity": "warning", "messageCode": "unused-export",
        "correspondence": {"state": "matched", "reason": None}, "fingerprint": "finding-key2:" + h("fp"), "waived": False,
        "parameterDigest": h("param"), "partialFingerprints": {"opensip/finding-key2": "finding-key2:" + h("fp")},
    }
    current = {"kind": "analysis", "authority": "authoritative", "runId": run_id, "planId": plan_id, "verdict": "pass",
               "requiredCoverage": "satisfied", "durability": "committed", "deficiency": "none", "secondaryDeficiencies": [],
               "coverageId": coverage_id, "comparisonResultId": comparison["comparisonResultId"]}
    request_id = "req1_" + h("request")[:32]
    run_envelope = {"schemaFamily": "opensip.product.envelope", "schemaMajor": 4, "kind": "run", "requestId": request_id,
                    "projectId": project, "termination": {"class": "success"}, "exitCode": 0, "run": current, "findings": [finding]}

    start = reach["items"][0]["endpoint"]
    near = reach["items"][1]["endpoint"]
    base_request = {"schemaFamily": "opensip.product.query", "schemaMajor": 3, "projectId": project, "view": {"runId": run_id},
                    "completeness": "best-effort", "page": {"size": 100}}

    def context(total, produced, visited, coverage_state, basis, cursor=None):
        ctx = copy.deepcopy(reach["context"])
        ctx.update(totalItems=total, producedItems=produced, visitedNodes=visited, traversalCoverage=coverage_state,
                   countBasis=basis, truncated=coverage_state == "truncated-bound")
        if cursor:
            ctx["nextCursor"] = cursor
        return ctx

    reach_slot = {"ordinal": 0, "purpose": "reach",
                  "request": dict(base_request, operation="graph.reach", params={"relation": "calls", "minResolution": "resolved", "direction": "outgoing", "start": start, "maxDepth": 1, "includeStart": True, "factViewDigests": reach["context"]["factViewDigests"]}),
                  "response": reach, "hostProjection": {"continuation": "complete-page-set"}}
    neighbor_row = {"factId": reach["items"][1]["viaFactId"], "relation": "calls", "resolution": "resolved", "source": start, "target": near}
    neighbor_slot = {"ordinal": 1, "purpose": "neighborhood",
                     "request": dict(base_request, operation="graph.neighbors", page={"size": 1}, params={"relation": "calls", "minResolution": "resolved", "direction": "outgoing", "endpoint": start}),
                     "response": {"schemaFamily": "opensip.product.query", "schemaMajor": 3, "operation": "graph.neighbors",
                                  "context": context(2, 1, 2, "truncated-page", "exact", "q3." + run_id[5:] + "." + h("selection") + ".1"), "items": [neighbor_row]},
                     "hostProjection": {"continuation": "not-embedded"}}
    pkg_a = {"universe": start["universe"], "kind": "package", "nativeSubjectId": "npm:@fixture/app", "packageManifestPath": "package.json"}
    pkg_b = {"universe": start["universe"], "kind": "package", "nativeSubjectId": "npm:@fixture/util", "packageManifestPath": "packages/util/package.json"}
    coupling_slot = {"ordinal": 2, "purpose": "package-coupling",
                     "request": dict(base_request, operation="graph.neighbors", params={"relation": "imports", "minResolution": "resolved", "direction": "outgoing", "endpoint": pkg_a}),
                     "response": {"schemaFamily": "opensip.product.query", "schemaMajor": 3, "operation": "graph.neighbors",
                                  "context": context(1, 1, 2, "complete", "exact"),
                                  "items": [{"factId": "fact2:" + h("pkg-edge"), "relation": "imports", "resolution": "resolved", "source": pkg_a, "target": pkg_b}]},
                     "hostProjection": {"continuation": "complete-page-set"}}
    path_slot = {"ordinal": 3, "purpose": "path",
                 "request": dict(base_request, operation="graph.path", params={"relation": "calls", "minResolution": "resolved", "direction": "outgoing", "start": start, "target": near, "maxDepth": 4}),
                 "response": {"schemaFamily": "opensip.product.query", "schemaMajor": 3, "operation": "graph.path",
                              "context": context(1, 1, 2, "complete", "exact"),
                              "items": [{"hopCount": 1, "start": start, "target": near, "nodes": [start, near], "edges": [{"factId": neighbor_row["factId"], "source": start, "target": near}]}]},
                 "hostProjection": {"continuation": "complete-page-set"}}

    declarations = [{"capabilityId": "typescript-semantic-facts", "languageModes": ["javascript", "typescript"]}]
    catalog = {"state": "present", "data": {
        "rules": {"state": "present", "data": {"source": {"kind": "run-plan-effective-policy", "planId": plan_id, "policyDigest": h("policy")}, "gateSeverityAtLeast": "warning", "rules": [rule]}},
        "capabilities": {"state": "present", "data": {"source": {"kind": "release-capability-registry", "registrySha256": hashlib.sha256(canonical(declarations)).hexdigest()}, "declarations": declarations}}}}
    evidence = {"state": "present", "data": {"coverageId": coverage_id, "entries": [coverage], "entriesProjection": {"total": 1, "omitted": 0, "omissionCause": "none"}}}

    def doc(command, envelope, panels, path=None):
        return {"schemaFamily": "opensip.product.report-projection", "schemaMajor": 1, "command": command,
                "renderer": {"format": "html", "version": 1}, "envelope": envelope, "supportedReportViews": views[command],
                "budgetProfile": budget, "reportObservedAt": "2026-09-14T12:00:00Z",
                "pathDisclosure": path or {"mode": "relative-only"}, "panels": panels}

    bases = {}
    bases["audit-full"] = doc("audit", run_envelope, {
        "evidence": evidence,
        "graph": {"state": "present", "data": {"slots": [reach_slot, neighbor_slot, coupling_slot, path_slot]}},
        "comparison": {"state": "present", "data": {"comparison": comparison}},
        "history": {"state": "present", "data": {"selection": {"source": "audit-baseline-source-run", "baselineId": baseline_id, "requestedRunIds": [prior["runId"]]},
                                                 "runs": [{"state": "present", "runId": prior["runId"], "run": prior, "findings": [], "findingsProjection": {"total": 0, "omitted": 0, "omissionCause": "none"}}]}},
        "catalog": catalog})

    failed = copy.deepcopy(run_envelope)
    failed["termination"] = {"class": "policy-failed", "runId": run_id}
    failed["exitCode"] = 1
    failed["run"]["verdict"] = "fail"
    del failed["run"]["comparisonResultId"]
    refused = {"code": "CONFIG.INVALID", "remedy": "fix the effective policy source", "subject": plan_id}
    bases["default-degraded"] = doc("default", failed, {
        "evidence": {"state": "unavailable", "reason": "evidence-purged"},
        "graph": {"state": "corrupt", "reason": "retained-bytes-corrupt"},
        "catalog": {"state": "present", "data": {"rules": {"state": "unavailable", "reason": "source-refused", "detail": refused},
                                                 "capabilities": {"state": "omitted", "reason": "exploration-budget-exceeded"}}}})

    ephemeral = copy.deepcopy(run_envelope)
    ephemeral["run"] = {"kind": "analysis", "authority": "ephemeral", "planId": plan_id, "evidenceId": "evidence3:" + h("evidence"), "verdict": "pass",
                        "requiredCoverage": "satisfied", "durability": "not-required", "deficiency": "none", "secondaryDeficiencies": [], "coverageId": coverage_id}
    ephemeral["projectRoot"] = "/home/dev/fixture"
    bases["analyze-ephemeral-local-links"] = doc("analyze", ephemeral, {
        "evidence": evidence, "graph": {"state": "unavailable", "reason": "no-run-identity"},
        "comparison": {"state": "omitted", "reason": "not-selected"}, "catalog": catalog},
        {"mode": "local-editor-links", "editorScheme": "vscode"})

    fit = copy.deepcopy(run_envelope)
    del fit["run"]["comparisonResultId"]
    bases["fit-budget-omission"] = doc("fit", fit, {
        "evidence": {"state": "omitted", "reason": "exploration-budget-exceeded"},
        "graph": {"state": "omitted", "reason": "exploration-budget-exceeded"}, "catalog": catalog})

    query_result = {"kind": "query", "items": 0, "truncated": False, "completenessMet": True, "advisory": True}
    candidate_list["context"]["projectId"] = project
    candidate_list["context"]["resolvedView"] = {"latest": True}
    bases["candidates-latest-view"] = doc("candidates", {"schemaFamily": "opensip.product.envelope", "schemaMajor": 4, "kind": "query", "requestId": request_id,
                                                          "projectId": project, "termination": {"class": "success"}, "exitCode": 0, "query": query_result,
                                                          "querySurface": "candidate-list", "queryRecord": candidate_list},
                                          {"graph": {"state": "unavailable", "reason": "no-run-identity"}})

    inspection["context"]["projectId"] = project
    inspection["context"]["resolvedView"] = {"runId": run_id}
    inspection["inspection"]["runId"] = run_id
    only_neighbor = copy.deepcopy(neighbor_slot)
    only_neighbor["ordinal"] = 0
    bases["inspect-run-graph"] = doc("inspect", {"schemaFamily": "opensip.product.envelope", "schemaMajor": 4, "kind": "query", "requestId": request_id,
                                                  "projectId": project, "termination": {"class": "success"}, "exitCode": 0, "query": query_result,
                                                  "querySurface": "candidate-inspection", "queryRecord": inspection},
                                     {"graph": {"state": "present", "data": {"slots": [only_neighbor]}}})

    bases["review-brief-failure"] = doc("review-brief", failure, {"graph": {"state": "unavailable", "reason": "no-admitted-result"}})

    repair["plan"]["descriptor"]["projectId"] = project
    bases["repair-preview"] = doc("repair-preview", {"schemaFamily": "opensip.product.envelope", "schemaMajor": 4, "kind": "query", "requestId": request_id,
                                                      "projectId": project, "termination": {"class": "success"}, "exitCode": 0, "query": query_result,
                                                      "querySurface": "repair-preview", "queryRecord": repair}, {})

    A = "audit-full"
    G = "/panels/graph/data/slots"
    def case(cid, base, ops, expect):
        return {"id": cid, "base": base, "ops": ops, "expect": expect}
    cases_out = [case("positive-" + name, name, [], "accept") for name in bases]
    cases_out += [
        case("positive-large-envelope-8000-findings", A, [{"op": "x-inflate-findings", "count": 8000}], "accept"),
        case("positive-deep-policy-predicate", A, [{"op": "x-deep-rule-predicate", "notChain": 27}], "accept"),
        # renderer gating and closed-shape refusals
        case("gate-command-query", A, [{"op": "set", "path": "/command", "value": "query"}], "SCHEMA"),
        case("gate-command-repair-verify", A, [{"op": "set", "path": "/command", "value": "repair-verify"}], "SCHEMA"),
        case("gate-renderer-version-2", A, [{"op": "set", "path": "/renderer/version", "value": 2}], "SCHEMA"),
        case("gate-renderer-sarif", A, [{"op": "set", "path": "/renderer/format", "value": "sarif"}], "SCHEMA"),
        case("gate-views-omitted", A, [{"op": "remove", "path": "/supportedReportViews"}], "SCHEMA"),
        case("gate-views-missing-history", A, [{"op": "set", "path": "/supportedReportViews", "value": [v for v in views["audit"] if v != "history"]}], "SCHEMA"),
        case("gate-views-extra-history-on-default", "default-degraded", [{"op": "set", "path": "/supportedReportViews", "value": views["audit"]}], "SCHEMA"),
        case("gate-analysis-command-query-envelope", "inspect-run-graph", [{"op": "set", "path": "/command", "value": "default"}, {"op": "set", "path": "/supportedReportViews", "value": views["default"]}], "SCHEMA"),
        case("gate-surface-mismatch", "candidates-latest-view", [{"op": "set", "path": "/command", "value": "review-brief"}, {"op": "set", "path": "/supportedReportViews", "value": views["review-brief"]}], "SCHEMA"),
        case("closed-envelope-extra-panel-field", A, [{"op": "set", "path": "/envelope/history", "value": []}], "SCHEMA"),
        case("closed-envelope-agent-hints", A, [{"op": "set", "path": "/envelope/agentHints", "value": ["hint"]}], "SCHEMA"),
        case("closed-envelope-meta-kind", A, [{"op": "set", "path": "/envelope/kind", "value": "meta"}], "SCHEMA"),
        case("path-relative-with-project-root", A, [{"op": "set", "path": "/envelope/projectRoot", "value": "/home/dev/fixture"}], "SCHEMA"),
        case("path-unlisted-editor-scheme", "analyze-ephemeral-local-links", [{"op": "set", "path": "/pathDisclosure/editorScheme", "value": "javascript"}], "SCHEMA"),
        case("panel-required-missing", "default-degraded", [{"op": "remove", "path": "/panels/graph"}], "SCHEMA"),
        case("panel-forbidden-history-on-default", "default-degraded", [{"op": "set", "path": "/panels/history", "value": {"state": "omitted", "reason": "not-selected"}}], "SCHEMA"),
        case("panel-forbidden-on-repair-preview", "repair-preview", [{"op": "set", "path": "/panels/catalog", "value": {"state": "omitted", "reason": "not-selected"}}], "SCHEMA"),
        case("panel-unknown-state-partial", A, [{"op": "set", "path": "/panels/evidence/state", "value": "partial"}], "SCHEMA"),
        case("panel-present-without-data", A, [{"op": "remove", "path": "/panels/comparison/data"}], "SCHEMA"),
        case("panel-untyped-blob", A, [{"op": "set", "path": "/panels/graph/data/raw", "value": {"anything": True}}], "SCHEMA"),
        case("panel-refused-without-detail", "default-degraded", [{"op": "remove", "path": "/panels/catalog/data/rules/detail"}], "SCHEMA"),
        case("panel-failure-envelope-with-present-panel", "review-brief-failure", [{"op": "set", "path": "/panels/graph", "value": bases["inspect-run-graph"]["panels"]["graph"]}], "SCHEMA"),
        case("graph-untyped-non-graph-operation", A, [{"op": "set", "path": G + "/0/request/operation", "value": "run.list"}, {"op": "set", "path": G + "/0/response/operation", "value": "run.list"}], "SCHEMA"),
        case("graph-request-latest-view", A, [{"op": "set", "path": G + "/0/request/view", "value": {"latest": True}}], "SCHEMA"),
        case("graph-purpose-operation-mismatch", A, [{"op": "set", "path": G + "/3/purpose", "value": "reach"}], "SCHEMA"),
        case("graph-response-failed-termination", A, [{"op": "set", "path": G + "/0/response/termination", "value": {"class": "request-rejected", "errorCode": "REQUEST.PRECONDITION_FAILED"}}], "SCHEMA"),
        case("graph-too-many-slots", A, [{"op": "x-graph-slots", "count": 7}], "SCHEMA"),
        case("budget-profile-altered", A, [{"op": "set", "path": "/budgetProfile/maxGraphSlots", "value": 8}], "SCHEMA"),
        case("budget-profile-prototype-history", A, [{"op": "set", "path": "/budgetProfile/maxHistoryRuns", "value": 20}], "SCHEMA"),
        case("history-two-runs", A, [{"op": "x-append-copy", "path": "/panels/history/data/runs"}], "SCHEMA"),
        # cross-record misjoins
        case("exit-termination-mismatch", A, [{"op": "set", "path": "/envelope/exitCode", "value": 1}], "J-EXIT"),
        case("graph-response-other-run", A, [{"op": "set", "path": G + "/0/response/context/resolvedView/runId", "value": "run3:" + h("other")}], "J-GRAPH-RUN"),
        case("graph-request-other-run", A, [{"op": "set", "path": G + "/2/request/view/runId", "value": "run3:" + h("other")}], "J-GRAPH-RUN"),
        case("graph-other-project", A, [{"op": "set", "path": G + "/2/response/context/projectId", "value": "prj1-" + h("other-project")}], "J-GRAPH-PROJECT"),
        case("graph-page-overflow", A, [{"op": "set", "path": G + "/0/request/page/size", "value": 2}], "J-GRAPH-PAGE"),
        case("graph-continuation-hidden", A, [{"op": "set", "path": G + "/1/hostProjection/continuation", "value": "complete-page-set"}], "J-GRAPH-CONTINUATION"),
        case("graph-fact-views-differ", A, [{"op": "set", "path": G + "/0/request/params/factViewDigests", "value": ["view2:" + h("view")]}], "J-GRAPH-VIEWS"),
        case("graph-coupling-row-symbol", A, [{"op": "set", "path": G + "/2/response/items/0/target", "value": near}], "J-GRAPH-COUPLING"),
        case("graph-neighbor-row-wrong-endpoint", A, [{"op": "set", "path": G + "/1/response/items/0/source", "value": pkg_a}, {"op": "set", "path": G + "/1/response/items/0/target", "value": pkg_b}], "J-GRAPH-ENDPOINT"),
        case("graph-neighbor-row-wrong-relation", A, [{"op": "set", "path": G + "/1/response/items/0/relation", "value": "imports"}], "J-GRAPH-RELATION"),
        case("graph-path-row-other-target", A, [{"op": "set", "path": G + "/3/request/params/target", "value": pkg_b}], "J-GRAPH-ENDPOINT"),
        case("graph-reach-start-not-requested", A, [{"op": "set", "path": G + "/0/request/params/includeStart", "value": False}], "J-GRAPH-ENDPOINT"),
        case("graph-on-ephemeral-run", "analyze-ephemeral-local-links", [{"op": "set", "path": "/panels/graph", "value": bases[A]["panels"]["graph"]}], "J-ANCHOR"),
        case("graph-on-latest-candidate-view", "candidates-latest-view", [{"op": "set", "path": "/panels/graph", "value": bases["inspect-run-graph"]["panels"]["graph"]}], "J-ANCHOR"),
        case("graph-inspect-other-run", "inspect-run-graph", [{"op": "set", "path": "/envelope/queryRecord/inspection/runId", "value": "run3:" + h("other")}], "J-GRAPH-RUN"),
        case("evidence-other-coverage", A, [{"op": "set", "path": "/panels/evidence/data/coverageId", "value": "coverage2:" + h("cov")}], "J-EVIDENCE-COVERAGE"),
        case("evidence-without-run-coverage", A, [{"op": "remove", "path": "/envelope/run/coverageId"}], "J-EVIDENCE-COVERAGE"),
        case("evidence-count-hidden-omission", A, [{"op": "set", "path": "/panels/evidence/data/entriesProjection/total", "value": 5}], "J-EVIDENCE-COUNTS"),
        case("evidence-item-limit-not-reached", A, [{"op": "set", "path": "/panels/evidence/data/entriesProjection", "value": {"total": 2, "omitted": 1, "omissionCause": "item-limit"}}], "J-EVIDENCE-COUNTS"),
        case("evidence-duplicate-key", A, [{"op": "x-append-copy", "path": "/panels/evidence/data/entries"}, {"op": "set", "path": "/panels/evidence/data/entriesProjection/total", "value": 2}], "J-EVIDENCE-KEYS"),
        case("comparison-other-id", A, [{"op": "set", "path": "/panels/comparison/data/comparison/comparisonResultId", "value": "comparison2:" + h("cmp")}], "J-COMPARISON-ID"),
        case("comparison-other-current-run", A, [{"op": "set", "path": "/panels/comparison/data/comparison/descriptor/currentRunId", "value": "run3:" + h("other")}], "J-COMPARISON-RUN"),
        case("comparison-selected-but-not-selected", A, [{"op": "set", "path": "/panels/comparison", "value": {"state": "omitted", "reason": "not-selected"}}], "J-NOT-SELECTED"),
        case("not-selected-on-graph", A, [{"op": "set", "path": "/panels/graph", "value": {"state": "omitted", "reason": "not-selected"}}], "J-NOT-SELECTED"),
        case("comparison-present-without-run-id", "analyze-ephemeral-local-links", [{"op": "set", "path": "/panels/comparison", "value": bases[A]["panels"]["comparison"]}], "J-COMPARISON-ID"),
        case("history-substituted-run", A, [{"op": "set", "path": "/panels/history/data/runs/0/runId", "value": run_id}, {"op": "set", "path": "/panels/history/data/runs/0/run/runId", "value": run_id}], "J-HISTORY-SELECTION"),
        case("history-run-record-misjoin", A, [{"op": "set", "path": "/panels/history/data/runs/0/run/runId", "value": "run3:" + h("other")}], "J-HISTORY-RUN"),
        case("history-selects-current-run", A, [{"op": "set", "path": "/panels/history/data/selection/requestedRunIds", "value": [run_id]}, {"op": "set", "path": "/panels/history/data/runs/0/runId", "value": run_id}, {"op": "set", "path": "/panels/history/data/runs/0/run/runId", "value": run_id}], "J-HISTORY-CURRENT"),
        case("history-other-baseline", A, [{"op": "set", "path": "/panels/history/data/selection/baselineId", "value": "baseline2:" + h("baseline")}], "J-HISTORY-BASELINE"),
        case("history-findings-count-hidden", A, [{"op": "set", "path": "/panels/history/data/runs/0/findingsProjection/total", "value": 3}], "J-HISTORY-COUNTS"),
        case("catalog-other-plan", A, [{"op": "set", "path": "/panels/catalog/data/rules/data/source/planId", "value": "plan2:" + h("plan")}], "J-CATALOG-PLAN"),
        case("catalog-finding-rule-missing", A, [{"op": "set", "path": "/envelope/findings/0/ruleId", "value": "unlisted-rule"}], "J-CATALOG-RULES"),
        case("catalog-registry-digest-forged", A, [{"op": "set", "path": "/panels/catalog/data/capabilities/data/source/registrySha256", "value": h("forged")}], "J-CATALOG-DIGEST"),
        case("state-no-run-identity-with-run", A, [{"op": "set", "path": "/panels/graph", "value": {"state": "unavailable", "reason": "no-run-identity"}}], "J-STATE-REASON"),
        case("state-no-admitted-result-on-run", A, [{"op": "set", "path": "/panels/evidence", "value": {"state": "unavailable", "reason": "no-admitted-result"}}], "J-STATE-REASON"),
        case("failure-panel-wrong-reason", "review-brief-failure", [{"op": "set", "path": "/panels/graph", "value": {"state": "unavailable", "reason": "evidence-purged"}}], "J-FAILURE-PANELS"),
        case("budget-order-violated", A, [{"op": "set", "path": "/panels/graph", "value": {"state": "omitted", "reason": "exploration-budget-exceeded"}}], "J-BUDGET-ORDER"),
        case("budget-exploration-bytes-exceeded", A, [{"op": "x-inflate-evidence", "count": 3956}], "J-BUDGET-BYTES"),
        case("budget-depth-exceeded", A, [{"op": "x-deep-rule-predicate", "notChain": 40}], "CODEC-DEPTH"),
    ]
    measurement = {"neighborRow": neighbor_row | {"target": {"universe": start["universe"], "kind": "symbol", "nativeSubjectId": "ts:packages/core/src/auth/token-store.ts#TokenStore.read"},
                                                   "source": {"universe": start["universe"], "kind": "symbol", "nativeSubjectId": "ts:packages/core/src/services/session-manager.ts#SessionManager.refreshToken"},
                                                   "producerClosure": "closure2:" + h("closure"), "confidenceMillionths": 1000000},
                   "finding": finding | {"subjectPath": "packages/core/src/services/session-manager.ts", "subjectKind": "symbol", "qualifiedName": "SessionManager.refreshToken"},
                   "coverage": coverage}
    return {"schemaVersion": 1,
            "standing": "AUTHOR CANDIDATE fixtures: constructed shape/join material from the pinned witness corpus; no semantic proof, no product qualification",
            "bases": bases, "cases": cases_out, "measurementSamples": measurement,
            "featureMap": FEATURE_MAP, "viewSources": VIEW_SOURCES, "openObligations": OPEN}


FEATURE_MAP = {
    "R01": {"report": ["/properties/envelope", "/properties/panels", "/$defs/BudgetProfileV1/properties/documentMaxCanonicalBytes"], "envelope": [], "presentationalOnly": "single-file inline assembly, no fetch: html_embedding/assets, not document fields"},
    "R02": {"report": ["/additionalProperties", "/properties/envelope", "/$defs/PanelsV1/additionalProperties"], "envelope": ["/additionalProperties"], "presentationalOnly": None},
    "R03": {"report": ["/$defs/HistoryPanelV1/properties/selection", "/$defs/ItemProjectionV1"], "envelope": ["/properties/run", "/properties/termination", "/properties/availability", "/properties/retentionDisclosure"], "presentationalOnly": "invocation/step/attempt ledger is kind=invocation, which has no html; not projected"},
    "R04": {"report": [], "envelope": ["/properties/findings"], "presentationalOnly": "sorting, grouping and pagination over envelope.findings"},
    "R05": {"report": ["/$defs/CatalogPanelV1", "/$defs/RuleCatalogV1", "/$defs/CapabilityCatalogV1"], "envelope": [], "presentationalOnly": "search/tag/source filters; historical run statistics have no owner and are not shown"},
    "R06": {"report": [], "envelope": ["/$defs/RepairPreviewRecordV1/properties/plan"], "presentationalOnly": "recipe row from repair-plan RecipeRef/recipeTrust; no admitted recipe description or parameter catalogue exists"},
    "R07": {"report": ["/$defs/GraphSlotV1/properties/response", "/$defs/GraphSlotV1/properties/request"], "envelope": [], "presentationalOnly": "symbol table over embedded GraphEndpoint identities; degree counts labelled embedded-subset; metrics/test reachability have no owner"},
    "R08": {"report": ["/$defs/GraphSlotV1/properties/purpose", "/$defs/GraphSlotV1/properties/response"], "envelope": [], "presentationalOnly": "matrix aggregation over package-coupling slots with their context disclosures"},
    "R09": {"report": ["/properties/envelope", "/$defs/GraphSlotV1/properties/response"], "envelope": ["/properties/requestId"], "presentationalOnly": "local formula-safe CSV of displayed rows with request/run/completeness context"},
    "R10": {"report": ["/$defs/GraphPanelV1", "/$defs/GraphSlotV1/properties/hostProjection", "/$defs/BudgetProfileV1/properties/browserLimits"], "envelope": [], "presentationalOnly": "layout, pan/zoom, highlight legend"},
    "R11": {"report": ["/$defs/GraphSlotV1/properties/response"], "envelope": ["/properties/findings"], "presentationalOnly": "card keyed by exact GraphEndpoint {universe, kind, nativeSubjectId}; no subject3<->endpoint join exists, so no path/body-hash matching"},
    "R12": {"report": ["/$defs/GraphSlotV1/properties/request", "/$defs/GraphSlotV1/properties/response"], "envelope": [], "presentationalOnly": "path purpose slot from explicit start/target; entry-point recognition is not projected"},
    "R13": {"report": ["/$defs/ComparisonPanelV1"], "envelope": ["/properties/run", "/properties/findings"], "presentationalOnly": None},
    "R14": {"report": ["/$defs/HistoryPanelV1", "/$defs/HistoryRunV1"], "envelope": [], "presentationalOnly": None},
    "R15": {"report": ["/$defs/BudgetProfileV1", "/$defs/GraphSlotV1/properties/hostProjection", "/$defs/ItemProjectionV1", "/$defs/PanelNotPresentV1"], "envelope": [], "presentationalOnly": None},
    "R16": {"report": ["/$defs/PanelNotPresentV1", "/$defs/PanelsV1"], "envelope": [], "presentationalOnly": "document-level shape failure is a report-data.ts display error"},
    "R17": {"report": ["/additionalProperties", "/$defs/BudgetProfileV1/properties/maxJsonDepth"], "envelope": [], "presentationalOnly": "script-safe embedding and text DOM construction"},
    "R18": {"report": [], "envelope": [], "presentationalOnly": "keyboard, focus and accessibility behaviour; no data"},
    "R19": {"report": ["/properties/supportedReportViews"], "envelope": [], "presentationalOnly": "help text keyed by ReportViewId; claims limited to the payload's states"},
    "R20": {"report": ["/$defs/PathDisclosureV1"], "envelope": ["/properties/projectRoot"], "presentationalOnly": None},
    "R21": {"report": [], "envelope": [], "presentationalOnly": "host delivery/platform process choice after required delivery; not a document field"},
    "R22": {"report": [], "envelope": ["/properties/requestId", "/properties/run"], "presentationalOnly": "host delivery publication/cleanup; not a document field"},
    "R23": {"report": ["/$defs/EvidencePanelV1", "/$defs/RuleCatalogV1/properties/source", "/$defs/CapabilityCatalogV1/properties/source"], "envelope": ["/properties/retentionDisclosure", "/properties/availability"], "presentationalOnly": "declared configuration beyond these fields has no selected redaction owner; not projected"},
    "R24": {"report": ["/properties/supportedReportViews", "/$defs/ReportViewId"], "envelope": ["/properties/queryRecord"], "presentationalOnly": "generic tabs from supportedReportViews; no simulation or legacy tab"},
}

VIEW_SOURCES = {
    "overview": {"envelope": ["/properties/run", "/properties/termination", "/properties/exitCode", "/properties/availability", "/properties/retentionDisclosure", "/properties/errors"], "report": ["/properties/reportObservedAt"]},
    "findings": {"envelope": ["/properties/findings"], "report": []},
    "candidate-list": {"envelope": ["/$defs/CandidateListRecordV1"], "report": []},
    "candidate-inspection": {"envelope": ["/$defs/CandidateInspectionRecordV1"], "report": []},
    "review-brief": {"envelope": ["/$defs/ReviewBriefRecordV1"], "report": []},
    "repair-preview": {"envelope": ["/$defs/RepairPreviewRecordV1"], "report": []},
    "evidence": {"envelope": ["/properties/availability"], "report": ["/$defs/EvidencePanelV1"]},
    "comparison": {"envelope": ["/properties/run"], "report": ["/$defs/ComparisonPanelV1"]},
    "history": {"envelope": [], "report": ["/$defs/HistoryPanelV1"]},
    "catalog": {"envelope": ["/$defs/RepairPreviewRecordV1/properties/plan"], "report": ["/$defs/CatalogPanelV1"]},
    "graph": {"envelope": [], "report": ["/$defs/GraphPanelV1", "/$defs/BudgetProfileV1/properties/browserLimits"]},
    "symbol-detail": {"envelope": ["/properties/findings"], "report": ["/$defs/GraphSlotV1/properties/response"]},
}

OPEN = [
    {"id": "RP-OBL-1", "owner": "envelope/inventory owner", "text": "fit declares html and parity fields candidates/evidence-levels, but inventory4 has no queryDispatch for fit and envelope4 kind=run has no candidate carrier. Until an envelope successor selects that carrier, the host must fail fit HTML required delivery. This projection does not add candidate data outside the envelope."},
    {"id": "RP-OBL-2", "owner": "report integration lane (M4)", "text": "Execute the measurement plan on the actual built report: parse/validate/first-render time, memory and bundle size at the listed scale points. Replace or confirm the development limits by a reviewed qualification. No limit here is a measured performance claim."},
    {"id": "RP-OBL-4", "owner": "reporting projection (M4) with query owner", "text": "Choose the host graph-slot selection policy: which endpoints and relations are pre-projected for each command. Endpoints must come from host-side admitted endpoint resolution, never from unpacking subject3 or browser path matching. The policy affects only usefulness. Slot shape, the six-slot bound, run pinning, deterministic ordinals and every join are already fixed here."},
    {"id": "RP-OBL-3", "owner": "generation registry (M1)", "text": "Register report-projection:1 as a source of recipe outputs output.rs and report.ts, and give the report-profile exact codec (maxJsonDepth 38, documentMaxCanonicalBytes) a named semanticValidatorOwner. The accepted 4 MiB/32 trial codec stays unchanged for its own callers."},
]


if __name__ == "__main__":
    (HERE / "fixtures.json").write_bytes(json.dumps(build(), indent=1, ensure_ascii=False).encode("utf-8") + b"\n")
