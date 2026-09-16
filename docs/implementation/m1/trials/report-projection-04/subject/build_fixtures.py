"""Deterministic fixtures for the author-04 report/fit successor candidate.

Positive documents are assembled from the pinned witness corpus plus labelled constructions: a small complete fact
graph answered by report_model.MockGraphOwner, invocation ledgers (with the invocation cancellation carrier) following
inventory5 step sequences, and panels produced by the reference byte law against the effective exploration budget.
Shape/join material only; not semantic proof.
"""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
WITNESSES = Path("/tmp/opensip-implementation/m1-schema-witnesses-01/witnesses.json")
ENV = "urn:opensip:product-v1:workflows:evaluator3:command-envelope:4"
COMMON = ARCH / "docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


M = load("report_model", HERE / "report_model.py")
OWNER = load("build_owner", HERE / "build_owner.py")
QSP = load("query_surface_projection", ARCH / "docs/coop/design-corrections/workflows/query_surface_projection.v3.py")
canonical = M.canonical
NO_CANCELLATION = {"requested": False, "signal": "SIGINT", "phase": "none"}


def h(n):
    return hashlib.sha256(("report-projection-fixture:" + str(n)).encode()).hexdigest()


def pick(cases, ref, kind=None, index=0):
    rows = [c["value"] for c in cases if c["ref"] == ref and (kind is None or c["origin"]["kind"] == kind)]
    return copy.deepcopy(rows[index])


AVAILABILITY = {"stepCount": 0, "totalNoticeCount": 0, "steps": []}


def pinned_termination(pins, run_id, char, text_chars=1024):
    """Owner-shaped evidence.pinned request rejection with a complete PinnedPurgeDisclosure (never truncated)."""
    consequences = json.loads(COMMON.read_bytes())["$defs"]["PinnedPurgeDisclosure"]["properties"]["consequences"]["const"]
    active = [{"pinId": ("%04d" % i) + char * 252, "kind": "other-authorized"} for i in range(pins)]
    return {"class": "request-rejected", "errorCode": "REQUEST.PRECONDITION_FAILED", "runId": run_id,
            "domainDetail": {"code": "evidence.pinned", "remedy": char * text_chars, "subject": char * text_chars,
                             "purgeDisclosure": {"runId": run_id, "consequences": consequences, "activePins": sorted(active, key=lambda p: p["pinId"].encode())}}}


def material():
    cases = json.loads(WITNESSES.read_bytes())["cases"]
    m = {}
    reach = pick(cases, "urn:opensip:product-v1:workflows:evaluator3:graph-query:3#/$defs/GraphQueryResponseV1", "harvest-seed")
    m["run"] = reach["context"]["resolvedView"]["runId"]
    m["project"] = reach["context"]["projectId"]
    m["coverageId"] = reach["context"]["evidence"]["coverageIds"][0]
    m["template"] = reach["context"]
    m["prior"] = pick(cases, "urn:opensip:product-v1:workflows:evaluator3:invocation:3#/$defs/AnalysisResult", "harvest-seed")
    m["plan"] = m["prior"]["planId"]
    comparison = pick(cases, "urn:opensip:product-v1:workflows:evaluator3:comparison:2#")
    comparison["descriptor"]["currentRunId"] = m["run"]
    m["comparison"] = comparison
    m["coverage"] = pick(cases, "urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/CoverageResultV3")
    m["rule"] = pick(cases, "urn:opensip:product-v1:policy-document:2#/$defs/Rule")
    failure = pick(cases, "urn:opensip:product-v1:workflows:evaluator3:command-envelope:3#", "harvest-seed")
    failure["schemaMajor"] = 5
    m["failure"] = failure
    m["inspection"] = pick(cases, ENV + "#/$defs/CandidateInspectionRecordV1")
    m["brief"] = pick(cases, ENV + "#/$defs/ReviewBriefRecordV1")
    m["repair"] = pick(cases, ENV + "#/$defs/RepairPreviewRecordV1")
    universe = reach["items"][0]["endpoint"]["universe"]
    sym = lambda path, name: {"universe": universe, "kind": "symbol", "nativeSubjectId": "ts:src/%s.ts#%s" % (path, name)}
    m["main"] = reach["items"][0]["endpoint"]
    m["helper"], m["util"] = sym("helper", "helper"), sym("util", "util")
    m["legacy"] = {"universe": universe, "kind": "file", "nativeSubjectId": "src/legacy.js"}
    m["pkg"] = {"universe": universe, "kind": "package", "nativeSubjectId": "npm:@fixture/util", "packageManifestPath": "packages/util/package.json"}
    m["spill"] = [sym("spill", "s%03d" % i) for i in range(105)]

    def fact(tag, relation, rung, source, target):
        return {"factId": "fact2:" + h("fact-" + tag), "relation": relation, "resolution": rung, "source": source, "target": target}
    facts = [fact("main-helper", "calls", "resolved-callee", m["main"], m["helper"]), fact("helper-util", "calls", "resolved-callee", m["helper"], m["util"]),
             fact("main-util", "calls", "resolved-callee", m["main"], m["util"]), fact("main-legacy", "imports", "resolved-target", m["main"], m["legacy"]),
             fact("util-pkg", "imports", "resolved-target", m["util"], m["pkg"])]
    facts += [fact("main-spill-%d" % i, "calls", "resolved-callee", m["main"], s) for i, s in enumerate(m["spill"])]
    m["facts"] = facts
    m["descriptors"] = {M.subject_id(e): e for e in [m["main"], m["helper"], m["util"], m["legacy"], m["pkg"]]}
    return m


def finding(rule_id, subject_id, path, kind, name, severity, tag):
    row = {"findingId": "finding3:" + h("finding-" + tag), "ruleId": rule_id, "subjectId": subject_id, "subjectPath": path, "subjectKind": kind,
           "severity": severity, "messageCode": rule_id, "correspondence": {"state": "matched", "reason": None},
           "fingerprint": "finding-key2:" + h("fp-" + tag), "waived": False, "parameterDigest": h("param-" + tag),
           "partialFingerprints": {"opensip/finding-key2": "finding-key2:" + h("fp-" + tag)}}
    if name:
        row["qualifiedName"] = name
    return row


def resolution_for(m, envelope, command, not_retained=()):
    rows = []
    for sid in M.policy_subjects(envelope, command):
        if sid in m["descriptors"] and sid not in not_retained:
            rows.append({"subjectId": sid, "state": "resolved", "endpoint": m["descriptors"][sid]})
        else:
            rows.append({"subjectId": sid, "state": "descriptor-not-retained"})
    return rows


OUTCOME = {"success": "completed", "policy-failed": "completed", "indeterminate": "completed", "request-rejected": "rejected", "operational-failed": "failed", "interrupted": "cancelled"}


def inventory_row(command):
    return next(c for c in json.loads(OWNER.dump(OWNER.inventory5()))["commands"] if c["name"] == command)


def ledger(m, command, request_id, terminations, run_ids=None, mode_ephemeral=False, recorded_count=None, cancellation=None):
    kinds = inventory_row(command)["steps"]
    steps = []
    for i, kind in enumerate(kinds):
        step = {"stepId": i, "kind": kind, "requirement": "required", "dependsOn": [i - 1] if i else [], "recorded": False}
        if kind != "render" and (recorded_count is None or i < recorded_count):
            term = terminations.get(i, {"class": "success"})
            outcome = OUTCOME[term["class"]]
            step.update(recorded=True, outcome=outcome, attempts=[{"executionId": "exec1_" + h("exec-%s-%d" % (request_id, i))[:32], "outcome": outcome}], termination=term)
            if run_ids and i in run_ids:
                step["analysisRunId"] = run_ids[i]
        steps.append(step)
    return {"requestId": request_id, "workflow": {"kind": "builtin", "name": command}, "mode": {"interactive": False, "ci": True, "ephemeral": mode_ephemeral},
            "cancellation": copy.deepcopy(cancellation or NO_CANCELLATION), "steps": steps, "missingChildren": M.missing_children(steps), "provenance": OWNER.PROVENANCE["ledger"]}


def static_parity(envelope, command, panels):
    text = M.static_parity_text(envelope, inventory_row(command), M.document_disclosures(panels)).encode("utf-8")
    return {"format": M.STATIC_FORMAT, "textSha256": M.sha(text), "textBytes": len(text)}


def exploration_budget(envelope, ledger_value):
    return M.effective_exploration_budget(OWNER.budget(), envelope, ledger_value, OWNER.ROOT_KEYS)


def build_context(m):
    R, PRJ = m["run"], m["project"]
    f_main = finding("no-unused-export", M.subject_id(m["main"]), "src/index.ts", "symbol", "main", "error", "main")
    f_helper = finding("no-unused-export", M.subject_id(m["helper"]), "src/helper.ts", "symbol", "helper", "warning", "helper")
    f_pkg = finding("no-legacy-import", M.subject_id(m["pkg"]), "packages/util/package.json", "package", None, "warning", "pkg")
    f_legacy = finding("no-legacy-import", M.subject_id(m["legacy"]), "src/legacy.js", "file", None, "note", "legacy")
    # Same path as the file endpoint but a different subject3 whose descriptor is not retained: never joined by path.
    f_lookalike = finding("no-legacy-import", "subject3:" + h("lookalike-subject"), "src/legacy.js", "file", None, "note", "lookalike")
    findings = sorted([f_main, f_helper, f_pkg, f_legacy, f_lookalike], key=lambda r: r["findingId"].encode())
    rules = []
    for rule_id in sorted({f["ruleId"] for f in findings}):
        rule = copy.deepcopy(m["rule"])
        rule["ruleId"] = rule_id
        rule["ruleProgramRef"]["ruleStableId"] = rule_id
        rules.append(rule)
    declarations = [{"capabilityId": "typescript-semantic-facts", "languageModes": ["javascript", "typescript"]}]
    P = OWNER.PROVENANCE
    catalog = {"rules": {"state": "present", "data": {"source": {"kind": "run-plan-effective-policy", "planId": m["plan"], "policyDigest": h("policy")}, "gateSeverityAtLeast": "warning", "rules": rules, "provenance": P["rules"]}},
               "capabilities": {"state": "present", "data": {"source": {"kind": "release-capability-registry", "registrySha256": M.sha(canonical(declarations))}, "declarations": declarations, "provenance": P["capabilities"]}}}
    request_id = "req1_" + h("request")[:32]
    current = {"kind": "analysis", "authority": "authoritative", "runId": R, "planId": m["plan"], "verdict": "pass", "requiredCoverage": "satisfied",
               "durability": "committed", "deficiency": "none", "secondaryDeficiencies": [], "coverageId": m["coverageId"],
               "comparisonResultId": m["comparison"]["comparisonResultId"]}
    run_envelope = {"schemaFamily": "opensip.product.envelope", "schemaMajor": 5, "kind": "run", "requestId": request_id, "projectId": PRJ,
                    "termination": {"class": "success"}, "exitCode": 0, "run": current, "availability": copy.deepcopy(AVAILABILITY), "findings": findings}

    def prior(tag):
        row = copy.deepcopy(m["prior"])
        row["runId"] = "run3:" + h("prior-" + tag)
        return row
    receipts = [{"runId": "run3:" + h("prior-p1"), "commitSequence": 41}, {"runId": "run3:" + h("prior-p2"), "commitSequence": 38},
                {"runId": "run3:" + h("prior-p3"), "commitSequence": 30}, {"runId": "run3:" + h("prior-p4"), "commitSequence": 44}]

    def history_rows(selection):
        rows = []
        by_seq = {r["runId"]: r["commitSequence"] for r in selection["priorRuns"]}
        for run_id in selection["requestedRunIds"]:
            if run_id == "run3:" + h("prior-p2"):
                rows.append({"state": "unavailable", "runId": run_id, "availability": "purged"})
                continue
            analysis = copy.deepcopy(m["prior"]) if run_id == m["prior"]["runId"] else prior(run_id[-8:])
            analysis["runId"] = run_id
            rows.append({"state": "present", "runId": run_id, "commitSequence": by_seq.get(run_id), "run": analysis,
                         "findings": [dict(f_main, findingId="finding3:" + h("hist-" + run_id))] if run_id == m["prior"]["runId"] else []})
        return rows

    def exploration(envelope, command, with_comparison, ledger_value, not_retained=()):
        resolution = resolution_for(m, envelope, command, not_retained)
        owner = M.MockGraphOwner(m["facts"], m["template"])
        plan = M.plan_slots(resolution, PRJ, R)
        baseline_source = m["prior"]["runId"] if with_comparison else None
        selection = M.history_selection(42, receipts, baseline_source, m["comparison"]["descriptor"]["baselineId"] if with_comparison else None, OWNER.budget()["maxHistoryRuns"])
        sources = {"comparison": {"comparison": m["comparison"], "provenance": P["comparison"]}, "catalog": catalog,
                   "evidence": {"coverageId": m["coverageId"], "entries": [m["coverage"]], "cap": OWNER.budget()["maxEvidenceEntries"]},
                   "history": {"selection": selection, "runs": history_rows(selection), "cap": OWNER.budget()["maxHistoryFindingsPerRun"]}}
        return M.project_exploration(sources, P, OWNER.PANELS[command], exploration_budget(envelope, ledger_value), resolution, owner, plan)

    return {"R": R, "PRJ": PRJ, "request_id": request_id, "run_envelope": run_envelope, "findings": {"main": f_main, "lookalike": f_lookalike},
            "catalog": catalog, "exploration": exploration, "receipts": receipts}


def doc(command, envelope, ledger_value, panels, path=None):
    return {"schemaFamily": "opensip.product.report-projection", "schemaMajor": 1, "command": command, "renderer": {"format": "html", "version": 1},
            "envelope": envelope, "invocationLedger": ledger_value, "staticParity": static_parity(envelope, command, panels), "disclosures": M.document_disclosures(panels),
            "supportedReportViews": OWNER.VIEWS[command], "featureStates": OWNER.feature_states(command), "budgetProfile": OWNER.budget(),
            "documentProvenance": OWNER.PROVENANCE["document"], "reportObservedAt": "2026-09-14T12:00:00Z",
            "pathDisclosure": path or {"mode": "relative-only"}, "panels": panels}


def refresh(document):
    """Recompute the derived root members after a construction step changed envelope or panels."""
    document["staticParity"] = static_parity(document["envelope"], document["command"], document["panels"])
    document["disclosures"] = M.document_disclosures(document["panels"])
    return document


def build():
    m = material()
    ctx = build_context(m)
    R, PRJ, request_id = ctx["R"], ctx["PRJ"], ctx["request_id"]

    bases = {}
    audit_env = ctx["run_envelope"]
    audit_ledger = ledger(m, "audit", request_id, {}, {0: R})
    bases["audit-full"] = doc("audit", audit_env, audit_ledger, ctx["exploration"](audit_env, "audit", True, audit_ledger))

    default_env = copy.deepcopy(audit_env)
    del default_env["run"]["comparisonResultId"]
    default_ledger = ledger(m, "default", request_id, {}, {0: R})
    bases["default-run"] = doc("default", default_env, default_ledger, ctx["exploration"](default_env, "default", False, default_ledger))

    degraded = copy.deepcopy(default_env)
    degraded["termination"] = {"class": "policy-failed", "runId": R}
    degraded["exitCode"] = 1
    degraded["run"]["verdict"] = "fail"
    refused = {"code": "CONFIG.INVALID", "remedy": "fix the effective policy source", "subject": m["plan"]}
    bases["default-degraded"] = doc("default", degraded, ledger(m, "default", request_id, {0: {"class": "policy-failed", "runId": R}}, {0: R}), {
        "evidence": {"state": "unavailable", "reason": "evidence-purged"}, "graph": {"state": "corrupt", "reason": "retained-bytes-corrupt"},
        "history": {"state": "unavailable", "reason": "evidence-missing"},
        "catalog": {"state": "present", "data": {"rules": {"state": "unavailable", "reason": "source-refused", "detail": refused},
                                                 "capabilities": {"state": "omitted", "reason": "exploration-budget-exceeded"}}}})

    ephemeral = copy.deepcopy(default_env)
    ephemeral["run"] = {"kind": "analysis", "authority": "ephemeral", "planId": m["plan"], "evidenceId": "evidence3:" + h("evidence"), "verdict": "pass",
                        "requiredCoverage": "satisfied", "durability": "not-required", "deficiency": "none", "secondaryDeficiencies": [], "coverageId": m["coverageId"]}
    ephemeral["projectRoot"] = "/home/dev/fixture"
    eph_panels = {"evidence": {"state": "present", "data": {"coverageId": m["coverageId"], "entries": [m["coverage"]], "entriesProjection": {"total": 1, "omitted": 0, "omissionCause": "none"}, "provenance": OWNER.PROVENANCE["evidence"]}},
                  "graph": {"state": "unavailable", "reason": "no-run-identity"}, "comparison": {"state": "omitted", "reason": "not-selected"},
                  "history": {"state": "unavailable", "reason": "no-run-identity"}, "catalog": {"state": "present", "data": ctx["catalog"]}}
    bases["analyze-ephemeral-local-links"] = doc("analyze", ephemeral, ledger(m, "analyze", request_id, {}, None, mode_ephemeral=True), eph_panels,
                                                 {"mode": "local-editor-links", "editorScheme": "vscode"})

    no_result = {"state": "unavailable", "reason": "no-admitted-result"}

    # fit ------------------------------------------------------------------
    f_main = ctx["findings"]["main"]

    def candidate(index, kind="finding", level="proof-backed"):
        row = {"candidateId": "candidate2:" + h("candidate-%d" % index), "runId": R, "kind": kind, "evidenceLevel": level, "subjectPath": "src/index.ts", "controlBearing": False, "suppressed": False}
        if kind == "finding":
            row.update(fingerprint=f_main["fingerprint"], ruleId=f_main["ruleId"], findingIds=[f_main["findingId"]],
                       occurrences=[{"findingId": f_main["findingId"], "subjectId": f_main["subjectId"], "subjectPath": f_main["subjectPath"], "parameterDigest": f_main["parameterDigest"],
                                     "correspondence": f_main["correspondence"], "waived": False}])
        return row

    def fit_report(candidates_all):
        ordered = sorted(candidates_all, key=lambda c: c["candidateId"].encode())
        page = ordered[:100]
        truncated = len(ordered) > len(page)
        levels = {lvl: sum(1 for c in page if c["evidenceLevel"] == lvl) for lvl in ("proof-backed", "partial-coverage", "advisory-only")}
        context = {"projectId": PRJ, "resolvedView": {"runId": R}, "coverage": "complete", "availability": "retained", "truncated": truncated, "totalItems": len(ordered), "advisory": True}
        cursor = M.fit_cursor(PRJ, R) if truncated else None
        if cursor:
            context["nextCursor"] = cursor
        record = {"surface": "candidate-list", "context": context, "includeSuppressed": False, "candidates": page, "evidenceLevels": levels, "suppressedCount": 0}
        return {"state": "sealed-run-first-page",
                "parity": {"runId": R, "candidates": page, "evidenceLevels": levels, "candidatesTruncated": truncated, "candidatesTotalItems": len(ordered),
                           "candidatesNextCursor": cursor, "candidatesAvailability": "sealed-run-first-page"},
                "request": {"schemaFamily": "opensip.product.query", "schemaMajor": 3, "projectId": PRJ, "view": {"runId": R}, "operation": "candidate.list",
                            "params": {"includeSuppressed": False}, "completeness": "best-effort", "page": {"size": 100}},
                "candidateList": record}

    fit_ledger = ledger(m, "fit", request_id, {}, {0: R})
    fit_env = copy.deepcopy(default_env)
    fit_env["advisoryReport"] = fit_report([candidate(0)])
    bases["fit-sealed"] = doc("fit", fit_env, fit_ledger, ctx["exploration"](fit_env, "fit", False, fit_ledger))
    fit_big = copy.deepcopy(default_env)
    fit_big["advisoryReport"] = fit_report([candidate(0)] + [candidate(i, "low-confidence-unused", ["proof-backed", "partial-coverage", "advisory-only"][i % 3]) for i in range(1, 150)])
    bases["fit-sealed-truncated-150"] = doc("fit", fit_big, fit_ledger, ctx["exploration"](fit_big, "fit", False, fit_ledger))
    fit_eph = copy.deepcopy(ephemeral)
    del fit_eph["projectRoot"]
    fit_eph["advisoryReport"] = {"state": "unavailable-ephemeral-analysis", "parity": {"runId": None, "candidates": None, "evidenceLevels": None, "candidatesTruncated": None,
                                                                                      "candidatesTotalItems": None, "candidatesNextCursor": None, "candidatesAvailability": "unavailable-ephemeral-analysis"}}
    bases["fit-ephemeral"] = doc("fit", fit_eph, ledger(m, "fit", request_id, {}, None, mode_ephemeral=True), {
        "evidence": eph_panels["evidence"], "graph": {"state": "unavailable", "reason": "no-run-identity"}, "history": {"state": "unavailable", "reason": "no-run-identity"}, "catalog": eph_panels["catalog"]})
    purged = {"code": "evidence.purged", "remedy": "re-run the analysis; the review projection bytes were purged", "subject": R}
    query_fail = {"class": "operational-failed", "errorCode": "HOST.IO_FAILURE", "faultCause": "host-io", "runId": R, "domainDetail": purged}
    fit_panels_none = {"evidence": no_result, "graph": no_result, "history": no_result, "catalog": no_result}
    bases["fit-after-commit-query-failure"] = doc("fit", M.failure_envelope(default_env, query_fail), ledger(m, "fit", request_id, {1: query_fail}, {0: R}), fit_panels_none)
    bases["fit-after-commit-query-refused"] = doc("fit", M.failure_envelope(default_env, QUERY_REFUSAL(R)), ledger(m, "fit", request_id, {1: QUERY_REFUSAL(R)}, {0: R}), fit_panels_none)

    # query commands ---------------------------------------------------------
    list_context = {"projectId": PRJ, "resolvedView": {"runId": R}, "coverage": "complete", "availability": "retained", "truncated": False, "totalItems": 1, "advisory": True}
    cands_env = {"schemaFamily": "opensip.product.envelope", "schemaMajor": 5, "kind": "query", "requestId": request_id, "projectId": PRJ, "termination": {"class": "success"}, "exitCode": 0,
                 "query": {"kind": "query", "items": 1, "truncated": False, "completenessMet": True, "advisory": True}, "querySurface": "candidate-list",
                 "queryRecord": {"surface": "candidate-list", "context": list_context, "includeSuppressed": False, "candidates": [candidate(0)],
                                 "evidenceLevels": {"proof-backed": 1, "partial-coverage": 0, "advisory-only": 0}, "suppressedCount": 0}}
    cands_ledger = ledger(m, "candidates", request_id, {})
    bases["candidates-run"] = doc("candidates", cands_env, cands_ledger, ctx["exploration"](cands_env, "candidates", False, cands_ledger))

    inspection = m["inspection"]
    facts = sorted(set(inspection["inspection"]["facts"]), key=lambda s: s.encode())
    inspection["inspection"].update(runId=R, facts=facts)
    inspection["context"] = dict(list_context, totalItems=len(facts))
    inspect_env = {"schemaFamily": "opensip.product.envelope", "schemaMajor": 5, "kind": "query", "requestId": request_id, "projectId": PRJ, "termination": {"class": "success"}, "exitCode": 0,
                   "query": {"kind": "query", "items": len(facts), "truncated": False, "completenessMet": True, "advisory": True}, "querySurface": "candidate-inspection", "queryRecord": inspection}
    bases["inspect-run"] = doc("inspect", inspect_env, ledger(m, "inspect", request_id, {}), {"graph": {"state": "omitted", "reason": "not-selected"}})

    brief = m["brief"]
    brief["brief"].update(runId=R, truncated=False)
    brief["context"] = dict(list_context, totalItems=len(brief["brief"]["candidates"]))
    brief_env = {"schemaFamily": "opensip.product.envelope", "schemaMajor": 5, "kind": "query", "requestId": request_id, "projectId": PRJ, "termination": {"class": "success"}, "exitCode": 0,
                 "query": {"kind": "query", "items": len(brief["brief"]["candidates"]), "truncated": False, "completenessMet": True, "advisory": True}, "querySurface": "review-brief", "queryRecord": brief}
    bases["review-brief-run"] = doc("review-brief", brief_env, ledger(m, "review-brief", request_id, {}), {"graph": {"state": "omitted", "reason": "not-selected"}})
    failure = m["failure"]
    bases["review-brief-failure"] = doc("review-brief", failure, ledger(m, "review-brief", failure["requestId"], {0: failure["termination"]}), {"graph": no_result})

    repair = m["repair"]
    descriptor = repair["plan"]["descriptor"]
    descriptor["projectId"] = PRJ
    repair["plan"]["repairPlanId"] = QSP.Wlegacy.wid("repairplan2", "workflow.repair-plan", descriptor)
    repair["preview"].update(repairPlanId=repair["plan"]["repairPlanId"], snapshotId=descriptor["snapshotId"], applicable=descriptor["applicable"], unmetPreconditions=copy.deepcopy(descriptor["unmetPreconditions"]))
    repair_env = {"schemaFamily": "opensip.product.envelope", "schemaMajor": 5, "kind": "query", "requestId": request_id, "projectId": PRJ, "termination": {"class": "success"}, "exitCode": 0,
                  "query": {"kind": "query", "items": len(descriptor["edits"]), "truncated": False, "completenessMet": descriptor["applicable"], "advisory": False},
                  "querySurface": "repair-preview", "queryRecord": repair}
    bases["repair-preview"] = doc("repair-preview", repair_env, ledger(m, "repair-preview", request_id, {}), {})

    inventory = json.loads(OWNER.dump(OWNER.inventory5()))
    return {"schemaVersion": 1,
            "standing": "AUTHOR-04 candidate fixtures: constructed shape/join material from the pinned witness corpus and a mock owner over complete fixture facts; no semantic proof, no product qualification",
            "bases": bases, "reportCases": report_cases(bases, m), "envelopeCases": envelope_cases(bases, m), "aggregateCases": aggregate_cases(R),
            "deliveryGoldens": delivery_goldens(m, R, request_id, fit_env, cands_env, inventory),
            "staticParityGoldens": {name: {"textSha256": b["staticParity"]["textSha256"], "textBytes": b["staticParity"]["textBytes"],
                                           "firstLine": M.static_parity_text(b["envelope"], next(c for c in inventory["commands"] if c["name"] == b["command"]), b["disclosures"]).splitlines()[0][:160]}
                                    for name, b in bases.items()},
            "featureMap": FEATURE_MAP, "obligations": OBLIGATIONS, "reviewCounterexamples": REVIEW_MAP}


def QUERY_REFUSAL(run_id):
    return {"class": "request-rejected", "errorCode": "REQUEST.PRECONDITION_FAILED", "runId": run_id, "domainDetail": {"code": "QUERY.VIEW_UNKNOWN", "remedy": "select a sealed run", "subject": run_id}}


def delivery_goldens(m, R, request_id, run_template, query_template, inventory):
    """Per-renderer semantic goldens: one recorded query outcome, then each renderer selection. Prior step terminations are carried unchanged."""
    analysis = {"kind": "analysis", "requirement": "required", "recorded": True, "outcome": "completed", "termination": {"class": "success"}, "analysisRunId": R}
    refused = {"kind": "query", "requirement": "required", "recorded": True, "outcome": "rejected", "termination": QUERY_REFUSAL(R)}
    io_failed = {"kind": "query", "requirement": "required", "recorded": True, "outcome": "failed",
                 "termination": {"class": "operational-failed", "errorCode": "HOST.IO_FAILURE", "faultCause": "host-io", "runId": R,
                                 "domainDetail": {"code": "evidence.purged", "remedy": "re-run the analysis", "subject": R}}}
    unrun_refused = {"kind": "query", "requirement": "required", "recorded": True, "outcome": "rejected",
                     "termination": {"class": "request-rejected", "errorCode": "REQUEST.PRECONDITION_FAILED", "domainDetail": {"code": "QUERY.VIEW_UNKNOWN", "remedy": "select a sealed run"}}}
    scenarios = [
        ("fit-query-refused-render-written", "fit", [analysis, refused], {"requirement": "required", "result": "written"}, R, run_template),
        ("fit-query-refused-required-render-failed", "fit", [analysis, refused], {"requirement": "required", "result": "failed"}, R, run_template),
        ("fit-query-refused-optional-render-failed", "fit", [analysis, refused], {"requirement": "optional", "result": "failed"}, R, run_template),
        ("fit-query-refused-no-render-selected", "fit", [analysis, refused], None, R, run_template),
        ("fit-query-io-failed-required-render-failed-tie", "fit", [analysis, io_failed], {"requirement": "required", "result": "failed"}, R, run_template),
        ("candidates-no-run-query-refused-required-render-failed", "candidates", [unrun_refused], {"requirement": "required", "result": "failed"}, None, query_template),
        ("fit-signal-during-required-render-before-settle", "fit", [analysis, {"kind": "query", "requirement": "required", "recorded": True, "outcome": "completed", "termination": {"class": "success"}}],
         {"requirement": "required", "result": "cancelled"}, R, run_template, {"requested": True, "signal": "SIGINT", "phase": "before-settle"}),
    ]
    out = []
    for sid, command, prior, render, run_id, template, *rest in scenarios:
        cancellation = rest[0] if rest else None
        row = next(c for c in inventory["commands"] if c["name"] == command)
        for fmt in ("human", "json", "agent", "html"):
            assert fmt in row["formats"]
            out.append(dict({"id": sid + "/" + fmt, "scenario": sid, "command": command, "priorSteps": prior, "render": render, "committedRunId": run_id},
                            **M.delivery_outcome(fmt, prior, render, template, run_id, row, cancellation)))
    return out


def aggregate_cases(R):
    s = lambda cls, **kw: dict({"class": cls}, **kw)
    step = lambda kind, term, outcome="completed", requirement="required", recorded=True, run=None: dict(
        {"kind": kind, "requirement": requirement, "recorded": recorded, "outcome": outcome, "termination": term}, **({"analysisRunId": run} if run else {}))
    renderer = M.renderer_failure(R)
    io = s("operational-failed", errorCode="HOST.IO_FAILURE", faultCause="host-io", domainDetail={"code": "evidence.purged", "remedy": "re-run"})
    return [
        {"id": "fit-success", "steps": [step("analysis", s("success"), run=R), step("query", s("success"))], "cancellation": None, "expect": s("success")},
        {"id": "fit-policy-failed-query-success", "steps": [step("analysis", s("policy-failed", runId=R), run=R), step("query", s("success"))], "cancellation": None, "expect": s("policy-failed", runId=R)},
        {"id": "review-D1-query-refused-then-required-render-failed", "steps": [step("analysis", s("success"), run=R), step("query", QUERY_REFUSAL(R), "rejected"), step("render", renderer, "failed")],
         "cancellation": None, "expect": renderer},
        {"id": "query-refused-then-optional-render-failed", "steps": [step("analysis", s("success"), run=R), step("query", QUERY_REFUSAL(R), "rejected"), step("render", renderer, "failed", "optional")],
         "cancellation": None, "expect": QUERY_REFUSAL(R)},
        {"id": "operational-tie-keeps-first-detail", "steps": [step("analysis", s("success"), run=R), step("query", io, "failed"), step("render", renderer, "failed")], "cancellation": None, "expect": io},
        {"id": "cancel-before-settle-after-commit", "steps": [step("analysis", s("success"), run=R), step("query", s("interrupted", signal="SIGINT"), "cancelled")],
         "cancellation": {"requested": True, "signal": "SIGINT", "phase": "before-settle"}, "expect": s("interrupted", signal="SIGINT", runId=R)},
        {"id": "cancel-before-settle-no-commit", "steps": [step("analysis", s("interrupted", signal="SIGTERM"), "cancelled"), step("query", s("interrupted", signal="SIGTERM"), "cancelled")],
         "cancellation": {"requested": True, "signal": "SIGTERM", "phase": "before-settle"}, "expect": s("interrupted", signal="SIGTERM")},
        {"id": "cancel-after-settle-not-reclassified", "steps": [step("analysis", s("policy-failed", runId=R), run=R), step("query", s("success"))],
         "cancellation": {"requested": True, "signal": "SIGHUP", "phase": "after-settle"}, "expect": s("policy-failed", runId=R)},
        {"id": "review-D2-interrupted-without-cancellation", "steps": [step("analysis", s("success"), run=R), step("query", s("interrupted", signal="SIGINT"), "cancelled")],
         "cancellation": None, "refusal": "J-LEDGER-CANCELLATION"},
        {"id": "interrupted-termination-completed-outcome", "steps": [step("analysis", s("interrupted", signal="SIGINT"))], "cancellation": None, "refusal": "J-LEDGER-CANCELLATION"},
        {"id": "after-settle-with-unsettled-required-step", "steps": [step("analysis", s("success"), run=R), step("query", None, None, recorded=False)],
         "cancellation": {"requested": True, "signal": "SIGINT", "phase": "after-settle"}, "refusal": "J-LEDGER-CANCELLATION"},
        {"id": "after-settle-claimed-during-required-render", "steps": [step("analysis", s("success"), run=R), step("query", s("success")), step("render", None, None, recorded=False)],
         "cancellation": {"requested": True, "signal": "SIGTERM", "phase": "after-settle"}, "refusal": "J-LEDGER-CANCELLATION"},
        {"id": "before-settle-claimed-when-all-settled", "steps": [step("analysis", s("success"), run=R), step("query", s("success"))],
         "cancellation": {"requested": True, "signal": "SIGINT", "phase": "before-settle"}, "refusal": "J-LEDGER-CANCELLATION"},
        {"id": "cancelled-step-signal-differs-from-carrier", "steps": [step("analysis", s("success"), run=R), step("query", s("interrupted", signal="SIGTERM"), "cancelled")],
         "cancellation": {"requested": True, "signal": "SIGINT", "phase": "before-settle"}, "refusal": "J-LEDGER-CANCELLATION"},
    ]


def report_cases(bases, m):
    A, GS, other = "audit-full", "/panels/graph/data/slots", "run3:" + h("other")
    H = "/panels/history/data"
    def case(cid, base, ops, expect):
        return {"id": cid, "base": base, "ops": ops, "expect": expect}
    out = [case("positive-" + name, name, [], "accept") for name in bases]
    out += [
        case("positive-review-P7-history-row-current-findings-host-asserted", A, [{"op": "x-history-copy-current-findings"}], "accept"),
        case("positive-review-P10-empty-registry-host-asserted", A, [{"op": "x-empty-registry"}], "accept"),
        case("positive-owner-depth-chain-27", A, [{"op": "x-deep-rule-predicate", "notChain": 27}], "accept"),
        case("positive-reissued-smaller-page-at-budget-edge", A, [{"op": "x-reissue-slot", "slot": 0, "size": 50}, {"op": "x-fill-to-budget-edge"}], "accept"),
        # gating and closed shapes
        case("gate-command-query", A, [{"op": "set", "path": "/command", "value": "query"}], "SCHEMA"),
        case("gate-renderer-version-2", A, [{"op": "set", "path": "/renderer/version", "value": 2}], "SCHEMA"),
        case("gate-views-missing-history", A, [{"op": "set", "path": "/supportedReportViews", "value": [v for v in OWNER.VIEWS["audit"] if v != "history"]}], "SCHEMA"),
        case("gate-fit-without-candidate-view", "fit-sealed", [{"op": "set", "path": "/supportedReportViews", "value": [v for v in OWNER.VIEWS["fit"] if v != "candidate-list"]}], "SCHEMA"),
        case("feature-state-silently-dropped", A, [{"op": "x-remove-index", "path": "/featureStates", "index": 0}], "SCHEMA"),
        case("feature-state-wrong-reason", A, [{"op": "x-feature-reason", "featureId": "entry-point-recognition", "reason": "no-admitted-owner"}], "SCHEMA"),
        case("feature-state-step-duration-dropped", A, [{"op": "x-remove-feature", "featureId": "step-duration"}], "SCHEMA"),
        case("ledger-omitted", A, [{"op": "remove", "path": "/invocationLedger"}], "SCHEMA"),
        case("static-parity-omitted", A, [{"op": "remove", "path": "/staticParity"}], "SCHEMA"),
        case("closed-envelope-extra-panel-field", A, [{"op": "set", "path": "/envelope/history", "value": []}], "SCHEMA"),
        case("envelope-major-4-refused", A, [{"op": "set", "path": "/envelope/schemaMajor", "value": 4}], "SCHEMA"),
        case("panel-forbidden-on-repair-preview", "repair-preview", [{"op": "set", "path": "/panels/catalog", "value": {"state": "omitted", "reason": "not-selected"}}], "SCHEMA"),
        case("provenance-host-assertion-hidden", A, [{"op": "set", "path": "/panels/catalog/data/capabilities/data/provenance/hostAsserted", "value": []}], "SCHEMA"),
        case("provenance-overclaim-registry-verified", A, [{"op": "set", "path": "/panels/catalog/data/capabilities/data/provenance/verifiedInDocument", "value": ["registry-is-host-release-declaration"]}], "SCHEMA"),
        case("review-A2-provenance-snapshot-count-claimed-verified", A, [{"op": "x-provenance-move", "panel": "history", "label": "prior-runs-in-snapshot-count"}], "SCHEMA"),
        case("graph-request-latest-view", A, [{"op": "set", "path": GS + "/0/request/view", "value": {"latest": True}}], "SCHEMA"),
        case("graph-request-with-cursor", A, [{"op": "set", "path": GS + "/1/request/page", "value": {"size": 100, "cursor": "q3.x"}}], "SCHEMA"),
        case("graph-page-size-off-ladder", A, [{"op": "set", "path": GS + "/0/request/page/size", "value": 7}], "SCHEMA"),
        case("review-P8-graph-duplicate-ordinal", A, [{"op": "set", "path": GS + "/1/ordinal", "value": 0}], "SCHEMA"),
        case("review-P5-audit-comparison-not-selected", A, [{"op": "remove", "path": "/envelope/run/comparisonResultId"}, {"op": "set", "path": "/panels/comparison", "value": {"state": "omitted", "reason": "not-selected"}}], "SCHEMA"),
        case("budget-profile-altered", A, [{"op": "set", "path": "/budgetProfile/maxGraphSlots", "value": 8}], "SCHEMA"),
        case("budget-profile-document-cap-altered", A, [{"op": "set", "path": "/budgetProfile/documentMaxBytes", "value": 9306112}], "SCHEMA"),
        case("history-five-runs", A, [{"op": "x-append-copy", "path": H + "/runs"}], "SCHEMA"),
        # envelope5 host admission
        case("review-P1-fit-run-without-advisory-report", "fit-sealed", [{"op": "remove", "path": "/envelope/advisoryReport"}], "J-ENV-FIT-CARRIER"),
        case("review-Q1-fit-truncated-short-page", "fit-sealed", [{"op": "x-fit-truncate-claim", "extra": 500}], "J-ENV-FIT-PAGE"),
        case("review-Q2a-fit-post-commit-failure-as-kind-run", "fit-sealed", [{"op": "remove", "path": "/envelope/advisoryReport"},
                                                                              {"op": "set", "path": "/envelope/termination", "value": M.renderer_failure(m["run"])},
                                                                              {"op": "set", "path": "/envelope/exitCode", "value": 4}], "J-ENV-FIT-CARRIER"),
        case("fit-parity-differs-from-page", "fit-sealed-truncated-150", [{"op": "set", "path": "/envelope/advisoryReport/parity/candidatesTotalItems", "value": 151}], "J-ENV-FIT-PARITY"),
        case("fit-cursor-wrong-position", "fit-sealed-truncated-150", [{"op": "x-fit-cursor", "value": "position-99"}], "J-ENV-FIT-CURSOR"),
        case("fit-request-other-run", "fit-sealed", [{"op": "set", "path": "/envelope/advisoryReport/request/view/runId", "value": other}], "J-ENV-FIT-RUN"),
        case("fit-ephemeral-sealed-carrier", "fit-ephemeral", [{"op": "set", "path": "/envelope/advisoryReport", "value": bases["fit-sealed"]["envelope"]["advisoryReport"]}], "SCHEMA"),
        case("fit-ephemeral-invented-empty-list", "fit-ephemeral", [{"op": "set", "path": "/envelope/advisoryReport/parity/candidates", "value": []}], "SCHEMA"),
        case("review-P2-candidates-evidence-levels-miscount", "candidates-run", [{"op": "set", "path": "/envelope/queryRecord/evidenceLevels/proof-backed", "value": 7}], "J-ENV-QUERY_SURFACE_EVIDENCE_LEVEL_JOIN"),
        case("candidates-latest-view", "candidates-run", [{"op": "set", "path": "/envelope/queryRecord/context/resolvedView", "value": {"latest": True}}], "J-ENV-QUERY_SURFACE_CONCRETE_RUN_REQUIRED"),
        case("review-P3-inspect-context-run-not-bundle-run", "inspect-run", [{"op": "set", "path": "/envelope/queryRecord/context/resolvedView", "value": {"runId": other}}], "J-ENV-QUERY_SURFACE_CANDIDATE_RUN_JOIN"),
        case("review-P3b-inspect-context-other-project", "inspect-run", [{"op": "set", "path": "/envelope/queryRecord/context/projectId", "value": "prj1-" + "0" * 64}], "J-ENV-QUERY_SURFACE_PROJECT_JOIN"),
        case("repair-plan-id-forged", "repair-preview", [{"op": "set", "path": "/envelope/queryRecord/plan/repairPlanId", "value": "repairplan2:" + h("forged")}], "J-ENV-QUERY_SURFACE_REPAIR_PLAN_ID_JOIN"),
        case("audit-run-without-comparison-id", A, [{"op": "remove", "path": "/envelope/run/comparisonResultId"}], "J-ENV-AUDIT-COMPARISON"),
        case("analysis-missing-capability-availability", A, [{"op": "remove", "path": "/envelope/availability"}], "J-ENV-CAPABILITY-AVAILABILITY"),
        case("exit-termination-mismatch", A, [{"op": "set", "path": "/envelope/exitCode", "value": 1}], "J-ENV-EXIT"),
        # ledger, D9 and cancellation
        case("ledger-request-id-other", A, [{"op": "set", "path": "/invocationLedger/requestId", "value": "req1_" + "0" * 32}], "J-LEDGER-REQUEST"),
        case("review-Q6-audit-envelope-labelled-analyze", A, [{"op": "set", "path": "/command", "value": "analyze"}, {"op": "set", "path": "/featureStates", "value": OWNER.feature_states("analyze")},
                                                              {"op": "set", "path": "/supportedReportViews", "value": OWNER.VIEWS["analyze"]}], "J-LEDGER-COMMAND"),
        case("ledger-step-kind-drift", A, [{"op": "set", "path": "/invocationLedger/steps/2/kind", "value": "query"}], "J-LEDGER-STEPS"),
        case("ledger-render-recorded", A, [{"op": "x-ledger-record-render"}], "J-LEDGER-RENDER"),
        case("ledger-missing-child-hidden", A, [{"op": "set", "path": "/invocationLedger/missingChildren", "value": []}], "J-LEDGER-MISSING"),
        case("ledger-duplicate-execution-id", A, [{"op": "x-ledger-duplicate-execution"}], "J-LEDGER-ATTEMPTS"),
        case("ledger-run-not-produced", A, [{"op": "set", "path": "/invocationLedger/steps/0/analysisRunId", "value": other}], "J-LEDGER-RUN"),
        case("ledger-ephemeral-mode-mismatch", "analyze-ephemeral-local-links", [{"op": "set", "path": "/invocationLedger/mode/ephemeral", "value": False}], "J-LEDGER-MODE"),
        case("ledger-aggregate-mismatch", A, [{"op": "set", "path": "/invocationLedger/steps/2/termination", "value": {"class": "indeterminate", "reasonCodes": ["VERDICT.INDETERMINATE"]}}], "J-LEDGER-AGGREGATE"),
        case("ledger-renderer-failure-without-render-record", "fit-after-commit-query-failure", [{"op": "x-delivery-termination"}], "J-LEDGER-AGGREGATE"),
        case("review-D1-renderer-failure-over-query-refusal-in-delivered-report", "fit-after-commit-query-refused", [{"op": "x-delivery-termination"}], "J-LEDGER-AGGREGATE"),
        case("query-refusal-rewritten-in-ledger", "fit-after-commit-query-refused", [{"op": "set", "path": "/invocationLedger/steps/1/termination", "value": M.renderer_failure(m["run"])},
                                                                                   {"op": "set", "path": "/invocationLedger/steps/1/outcome", "value": "failed"},
                                                                                   {"op": "set", "path": "/invocationLedger/steps/1/attempts/0/outcome", "value": "failed"}], "J-LEDGER-AGGREGATE"),
        case("review-D2-interrupted-step-without-cancellation", A, [{"op": "set", "path": "/invocationLedger/steps/1/termination", "value": {"class": "interrupted", "signal": "SIGINT"}},
                                                                    {"op": "set", "path": "/invocationLedger/steps/1/outcome", "value": "cancelled"}], "J-LEDGER-CANCELLATION"),
        case("cancellation-omitted", A, [{"op": "remove", "path": "/invocationLedger/cancellation"}], "SCHEMA"),
        case("cancellation-requested-phase-none", A, [{"op": "set", "path": "/invocationLedger/cancellation", "value": {"requested": True, "signal": "SIGINT", "phase": "none"}}], "J-LEDGER-CANCELLATION"),
        case("cancellation-before-settle-report-not-deliverable", A, [{"op": "x-cancel-before-settle"}], "J-LEDGER-CANCELLATION"),
        case("cancellation-after-settle-claimed-during-render", "default-run", [{"op": "set", "path": "/invocationLedger/cancellation", "value": {"requested": True, "signal": "SIGTERM", "phase": "after-settle"}}], "J-LEDGER-CANCELLATION"),
        case("cancellation-exit-code-not-130", A, [{"op": "x-cancel-before-settle"}, {"op": "set", "path": "/envelope/exitCode", "value": 4}], "J-ENV-EXIT"),
        # mandatory root bounds (reviewer B1 and maximal legal step terminations; no performance claim)
        case("review-B1-control-one-pinned-step", A, [{"op": "x-pinned-failure", "bigSteps": 1, "stepPins": "envelope-max", "char": "\U0001F600"}], "accept"),
        case("review-B1-three-pinned-steps-envelope-boundary", A, [{"op": "x-pinned-failure", "bigSteps": 3, "stepPins": "envelope-max", "char": "\U0001F600"}], "accept"),
        case("maximal-legal-step-terminations-audit-failure", A, [{"op": "x-pinned-failure", "bigSteps": 3, "stepPins": "max-legal", "char": "\x01"}], "accept"),
        # codecs
        case("review-P6-owner-refused-chain-28", A, [{"op": "x-deep-rule-predicate", "notChain": 28}], "CODEC-OWNER-DEPTH"),
        case("report-depth-exceeded-chain-40", A, [{"op": "x-deep-rule-predicate", "notChain": 40}], "CODEC-DEPTH"),
        case("review-Q7b-iterative-depth-200000", A, [{"op": "x-bytes", "kind": "deep-array"}], "CODEC-DEPTH"),
        case("worst-case-envelope-85-findings", A, [{"op": "x-worst-findings", "count": 85}], "ENVELOPE-SERIALIZATION-BOUNDARY"),
    ] + [case("lexical-" + k, A, [{"op": "x-bytes", "kind": k}], code) for k, code in [
        ("duplicate-key", "CODEC-LEXICAL"), ("negative-zero", "CODEC-LEXICAL"), ("float", "CODEC-LEXICAL"), ("exponent", "CODEC-LEXICAL"), ("nan", "CODEC-LEXICAL"),
        ("integer-out-of-range", "CODEC-LEXICAL"), ("lone-surrogate", "CODEC-LEXICAL"), ("invalid-utf8", "CODEC-LEXICAL"),
        ("noncanonical-whitespace", "CODEC-NONCANONICAL"), ("noncanonical-key-order", "CODEC-NONCANONICAL"), ("oversize", "CODEC-BYTES")]] + [
        # graph slot policy and owner page law
        case("slot-subjects-reordered", A, [{"op": "x-swap-resolution", "a": 0, "b": 1}], "J-SLOT-SUBJECTS"),
        case("slot-policy-relation-swapped", A, [{"op": "x-slot-relation", "slot": 1, "relation": "references", "rung": "resolved-binding"}], "J-SLOT-POLICY"),
        case("review-S2-slot-items-sliced", A, [{"op": "x-slice-slot-items", "slot": 3, "count": 0}], "J-GRAPH-COUNT"),
        case("review-G1-complete-lower-bound-sliced", A, [{"op": "x-graph-relabel", "variant": "complete-lower-bound"}], "J-GRAPH-COUNT"),
        case("review-G1-truncated-page-lower-bound-sliced", A, [{"op": "x-graph-relabel", "variant": "truncated-page-lower-bound"}], "J-GRAPH-COUNT"),
        case("review-G2-truncated-bound-sliced-without-cap", A, [{"op": "x-graph-relabel", "variant": "truncated-bound-lower-bound"}], "J-GRAPH-COUNT"),
        case("review-G3-complete-exact-sliced", A, [{"op": "x-graph-relabel", "variant": "complete-exact"}], "J-GRAPH-COUNT"),
        case("graph-lower-bound-at-public-item-cap", A, [{"op": "x-slot-public-cap-spill"}], "accept"),
        case("graph-lower-bound-at-public-item-cap-labelled-complete", A, [{"op": "x-slot-public-cap-spill"}, {"op": "x-graph-relabel", "variant": "cap-spill-complete", "keepItems": True}], "J-GRAPH-COUNT"),
        case("graph-lower-bound-at-public-item-cap-continuation-complete-page-set", A, [{"op": "x-slot-public-cap-spill"}, {"op": "set", "path": GS + "/0/hostProjection/continuation", "value": "complete-page-set"}], "J-GRAPH-CONTINUATION"),
        case("graph-exact-complete-labelled-operation-truncated", A, [{"op": "set", "path": GS + "/1/hostProjection/continuation", "value": "operation-truncated-no-continuation"}], "J-GRAPH-CONTINUATION"),
        case("slot-cursor-wrong", A, [{"op": "x-slot-cursor", "slot": 0}], "J-GRAPH-CURSOR"),
        case("review-Q5-row-below-min-resolution", A, [{"op": "x-row-resolution", "slot": 1, "row": 0, "resolution": "syntactic-callee-name"}], "J-GRAPH-RESOLUTION"),
        case("row-kind-outside-table", A, [{"op": "x-row-target", "slot": 1, "row": 0, "target": "legacy"}], "J-GRAPH-KINDS"),
        case("neighbor-rows-out-of-order", A, [{"op": "x-reverse-slot-items", "slot": 0}], "J-GRAPH-ORDER"),
        case("review-Q13-path-node-not-on-edge", A, [{"op": "x-path-extra-node"}], "J-GRAPH-PATH"),
        case("reach-depth-zero-without-include-start", A, [{"op": "x-reach-depth-zero"}], "J-GRAPH-REACH"),
        case("review-Q4-byte-budget-reduced-on-small-document", A, [{"op": "x-reissue-slot", "slot": 0, "size": 50}], "J-BUDGET-CAUSE"),
        case("page-cause-reduced-on-ladder-first-size", A, [{"op": "set", "path": GS + "/1/hostProjection", "value": {"continuation": "complete-page-set", "pageSizeCause": "byte-budget-reduced", "rejectedByteDelta": 1}}], "J-GRAPH-PAGE-CAUSE"),
        case("graph-continuation-hidden", A, [{"op": "set", "path": GS + "/0/hostProjection/continuation", "value": "complete-page-set"}], "J-GRAPH-CONTINUATION"),
        case("graph-response-other-run", A, [{"op": "set", "path": GS + "/1/response/context/resolvedView/runId", "value": other}], "J-GRAPH-RUN"),
        case("subject-index-mismatch", A, [{"op": "x-subject-index-forge-last"}], "J-SUBJECT-INDEX-MISMATCH"),
        case("subject-index-missing-endpoint", A, [{"op": "x-remove-index", "path": "/panels/graph/data/subjectIndex", "index": 0}], "J-SUBJECT-INDEX-COVERAGE"),
        case("resolution-endpoint-forged", A, [{"op": "x-resolution-endpoint", "index": 0, "target": "util"}], "J-SUBJECT-INDEX-MISMATCH"),
        case("review-S1-descriptor-not-retained-replan", A, [{"op": "x-not-retained-replan", "subject": "main"}], "J-SLOT-RESOLUTION-CONTRADICTED"),
        case("review-A1-descriptor-not-retained-uncontradicted-steering-disclosed", A, [{"op": "x-not-retained-replan", "subject": "pkg"}], "accept"),
        case("descriptor-not-retained-count-hidden", A, [{"op": "x-not-retained-replan", "subject": "pkg"}, {"op": "x-disclosure", "key": "graphUnresolvedSubjects", "value": 1}], "J-DISCLOSURES"),
        case("graph-on-ephemeral-run", "analyze-ephemeral-local-links", [{"op": "set", "path": "/panels/graph", "value": bases[A]["panels"]["graph"]}], "J-ANCHOR"),
        case("graph-not-selected-with-subjects", A, [{"op": "set", "path": "/panels/graph", "value": {"state": "omitted", "reason": "not-selected"}}], "J-NOT-SELECTED"),
        # evidence, comparison, history, catalog, budget
        case("evidence-other-coverage", A, [{"op": "set", "path": "/panels/evidence/data/coverageId", "value": "coverage2:" + h("cov")}], "J-EVIDENCE-COVERAGE"),
        case("evidence-count-hidden-omission", A, [{"op": "set", "path": "/panels/evidence/data/entriesProjection/total", "value": 5}], "J-EVIDENCE-COUNTS"),
        case("review-Q3-evidence-byte-budget-on-small-document", A, [{"op": "set", "path": "/panels/evidence/data/entriesProjection", "value": {"total": 3001, "omitted": 3000, "omissionCause": "byte-budget", "rejectedByteDelta": 1063}}], "J-BUDGET-CAUSE"),
        case("comparison-other-current-run", A, [{"op": "set", "path": "/panels/comparison/data/comparison/descriptor/currentRunId", "value": other}], "J-COMPARISON-RUN"),
        case("review-P4-history-when-comparison-unavailable", A, [{"op": "set", "path": "/panels/comparison", "value": {"state": "unavailable", "reason": "evidence-purged"}}], "J-HISTORY-PREREQUISITE"),
        case("history-baseline-source-without-comparison", "default-run", [{"op": "set", "path": H + "/selection/baselineSourceRunId", "value": m["prior"]["runId"]}], "J-HISTORY-BASELINE"),
        case("history-baseline-source-listed-as-prior", A, [{"op": "x-history-baseline-as-prior"}], "J-HISTORY-BASELINE"),
        case("history-prior-not-descending", A, [{"op": "x-history-swap-prior"}], "J-HISTORY-ORDER"),
        case("history-prior-at-or-above-current", A, [{"op": "set", "path": H + "/selection/currentCommitSequence", "value": 41}], "J-HISTORY-ORDER"),
        case("history-count-at-limit-with-baseline-source", A, [{"op": "set", "path": H + "/selection/priorRunsInSnapshot", "value": 9}, {"op": "x-refresh"}], "accept"),
        case("history-count-under-selected", "default-run", [{"op": "set", "path": H + "/selection/priorRunsInSnapshot", "value": 9}, {"op": "x-refresh"}], "J-HISTORY-COUNT"),
        case("review-H1-snapshot-count-understated-host-asserted-disclosed", "default-run", [{"op": "x-history-understate"}], "accept"),
        case("history-snapshot-count-disclosure-hidden", "default-run", [{"op": "x-history-understate"}, {"op": "x-disclosure", "key": "historyPriorRunsInSnapshotHostAsserted", "value": 3}], "J-DISCLOSURES"),
        case("history-requested-substituted", A, [{"op": "set", "path": H + "/selection/requestedRunIds/1", "value": "run3:" + h("prior-p4")}], "J-HISTORY-POLICY"),
        case("history-row-substituted", A, [{"op": "set", "path": H + "/runs/1/runId", "value": "run3:" + h("prior-p4")}, {"op": "set", "path": H + "/runs/1/run/runId", "value": "run3:" + h("prior-p4")}], "J-HISTORY-SELECTION"),
        case("history-row-sequence-drift", A, [{"op": "set", "path": H + "/runs/1/commitSequence", "value": 40}], "J-HISTORY-SEQUENCE"),
        case("history-run-record-misjoin", A, [{"op": "set", "path": H + "/runs/0/run/runId", "value": other}], "J-HISTORY-RUN"),
        case("catalog-registry-digest-forged", A, [{"op": "set", "path": "/panels/catalog/data/capabilities/data/source/registrySha256", "value": h("forged")}], "J-CATALOG-DIGEST"),
        case("catalog-finding-rule-missing", A, [{"op": "x-finding-rule", "value": "unlisted-rule"}], "J-CATALOG-RULES"),
        case("budget-order-violated", A, [{"op": "set", "path": "/panels/evidence", "value": {"state": "omitted", "reason": "exploration-budget-exceeded"}}, {"op": "x-refresh"}], "J-BUDGET-ORDER"),
        case("budget-exploration-bytes-exceeded", A, [{"op": "x-inflate-evidence", "count": 3956}], "J-BUDGET-BYTES"),
        case("static-parity-digest-drift", A, [{"op": "set", "path": "/staticParity/textBytes", "value": 1}], "J-STATIC-PARITY"),
        case("state-no-admitted-result-on-run", A, [{"op": "set", "path": "/panels/evidence", "value": {"state": "unavailable", "reason": "no-admitted-result"}}, {"op": "x-refresh"}], "J-STATE-REASON"),
        case("failure-panel-wrong-reason", "review-brief-failure", [{"op": "set", "path": "/panels/graph", "value": {"state": "unavailable", "reason": "evidence-purged"}}], "J-FAILURE-PANELS"),
    ]
    return out


def envelope_cases(bases, m):
    other = "run3:" + h("other")
    sealed = bases["fit-sealed"]["envelope"]
    big = bases["fit-sealed-truncated-150"]["envelope"]
    eph = bases["fit-ephemeral"]["envelope"]
    fail = bases["fit-after-commit-query-failure"]["envelope"]
    refused = bases["fit-after-commit-query-refused"]["envelope"]
    renderer_fail = M.failure_envelope(fail, M.renderer_failure(m["run"]))
    def case(cid, command, envelope, ops, expect):
        return {"id": cid, "command": command, "envelope": envelope, "ops": ops, "expect": expect}
    return [
        case("json-fit-sealed-first-page", "fit", sealed, [], "accept"),
        case("json-fit-sealed-truncated-150", "fit", big, [], "accept"),
        case("json-fit-ephemeral-null-parity", "fit", eph, [], "accept"),
        case("json-fit-policy-failed", "fit", sealed, [{"op": "set", "path": "/termination", "value": {"class": "policy-failed", "runId": m["run"]}}, {"op": "set", "path": "/exitCode", "value": 1},
                                                       {"op": "set", "path": "/run/verdict", "value": "fail"}], "accept"),
        case("json-fit-after-commit-query-failure", "fit", fail, [], "accept"),
        case("json-fit-after-commit-query-refused", "fit", refused, [], "accept"),
        case("json-fit-renderer-failure-after-commit", "fit", renderer_fail, [], "accept"),
        case("json-fit-missing-carrier", "fit", sealed, [{"op": "remove", "path": "/advisoryReport"}], "J-ENV-FIT-CARRIER"),
        case("json-fit-ephemeral-run-with-sealed-carrier", "fit", sealed, [{"op": "set", "path": "/run", "value": eph["run"]}], "SCHEMA-ENV"),
        case("json-fit-sealed-run-with-ephemeral-carrier", "fit", eph, [{"op": "set", "path": "/run", "value": sealed["run"]}], "SCHEMA-ENV"),
        case("json-fit-ephemeral-invented-list", "fit", eph, [{"op": "set", "path": "/advisoryReport/parity/candidates", "value": []}], "SCHEMA-ENV"),
        case("json-fit-page-size-50", "fit", sealed, [{"op": "set", "path": "/advisoryReport/request/page", "value": {"size": 50}}], "SCHEMA-ENV"),
        case("json-fit-request-include-suppressed", "fit", sealed, [{"op": "set", "path": "/advisoryReport/request/params", "value": {"includeSuppressed": True}}], "SCHEMA-ENV"),
        case("json-fit-request-with-cursor", "fit", sealed, [{"op": "set", "path": "/advisoryReport/request/page", "value": {"size": 100, "cursor": "q3.x"}}], "SCHEMA-ENV"),
        case("json-fit-request-other-run", "fit", sealed, [{"op": "set", "path": "/advisoryReport/request/view/runId", "value": other}], "J-ENV-FIT-RUN"),
        case("json-fit-truncation-hidden", "fit", big, [{"op": "set", "path": "/advisoryReport/candidateList/context/truncated", "value": False}, {"op": "remove", "path": "/advisoryReport/candidateList/context/nextCursor"},
                                                        {"op": "set", "path": "/advisoryReport/parity/candidatesTruncated", "value": False}, {"op": "set", "path": "/advisoryReport/parity/candidatesNextCursor", "value": None}],
             "J-ENV-QUERY_SURFACE_TOTAL_ITEMS_JOIN"),
        case("json-fit-cursor-on-complete-page", "fit", sealed, [{"op": "x-fit-cursor", "value": "add"}], "J-ENV-FIT-PAGE"),
        case("json-fit-parity-not-page", "fit", big, [{"op": "set", "path": "/advisoryReport/parity/candidates", "value": []}], "J-ENV-FIT-PARITY"),
        case("json-fit-kind-run-delivery-termination", "fit", sealed, [{"op": "remove", "path": "/advisoryReport"}, {"op": "set", "path": "/termination", "value": renderer_fail["termination"]},
                                                                       {"op": "set", "path": "/exitCode", "value": 4}], "J-ENV-FIT-CARRIER"),
        case("json-analyze-with-fit-carrier", "analyze", sealed, [], "J-ENV-FIT-CARRIER"),
        case("json-fit-major-4", "fit", sealed, [{"op": "set", "path": "/schemaMajor", "value": 4}], "SCHEMA-ENV"),
        case("json-renderer-failure-without-committed-run-names-run", "candidates", M.failure_envelope(fail, M.renderer_failure(None)), [{"op": "set", "path": "/termination/runId", "value": m["run"]}], "SCHEMA-ENV"),
    ]


FEATURE_MAP = {
    "R01": [{"kind": "report", "ref": "/properties/envelope"}, {"kind": "report", "ref": "/$defs/StaticParityV1"}, {"kind": "obligation", "ref": "RP-OBL-B01"}],
    "R02": [{"kind": "report", "ref": "/additionalProperties"}, {"kind": "report", "ref": "/$defs/PanelsV1/additionalProperties"}, {"kind": "envelope", "ref": "/additionalProperties"}],
    "R03": [{"kind": "report", "ref": "/$defs/InvocationLedgerV1"}, {"kind": "report", "ref": "/$defs/LedgerStepV1"}, {"kind": "envelope", "ref": "/properties/termination"},
            {"kind": "featureState", "ref": "step-duration"}],
    "R04": [{"kind": "envelope", "ref": "/properties/findings"}, {"kind": "obligation", "ref": "RP-OBL-B01"}],
    "R05": [{"kind": "report", "ref": "/$defs/RuleCatalogV1"}, {"kind": "report", "ref": "/$defs/CapabilityCatalogV1"}, {"kind": "featureState", "ref": "rule-descriptions"},
            {"kind": "featureState", "ref": "capability-descriptions"}, {"kind": "featureState", "ref": "catalog-run-statistics"}],
    "R06": [{"kind": "envelope", "ref": "/$defs/RepairPreviewRecordV1/properties/plan"}, {"kind": "featureState", "ref": "recipe-descriptions"}, {"kind": "featureState", "ref": "recipe-parameters"}],
    "R07": [{"kind": "report", "ref": "/$defs/GraphPanelV1/properties/subjectIndex"}, {"kind": "report", "ref": "/$defs/SubjectResolutionV1"}, {"kind": "featureState", "ref": "symbol-metrics"}, {"kind": "featureState", "ref": "test-reachability"}],
    "R08": [{"kind": "report", "ref": "/$defs/GraphSlotV1/properties/purpose"}, {"kind": "featureState", "ref": "coupling-importer-package-membership"}],
    "R09": [{"kind": "report", "ref": "/$defs/GraphSlotV1/properties/request"}, {"kind": "envelope", "ref": "/properties/requestId"}, {"kind": "obligation", "ref": "RP-OBL-B01"}],
    "R10": [{"kind": "report", "ref": "/$defs/GraphPanelV1"}, {"kind": "report", "ref": "/$defs/BudgetProfileV1/properties/browserLimits"}],
    "R11": [{"kind": "report", "ref": "/$defs/GraphPanelV1/properties/subjectIndex"}, {"kind": "envelope", "ref": "/properties/findings"}],
    "R12": [{"kind": "report", "ref": "/$defs/GraphSlotV1/properties/anchorSubjectIds"}, {"kind": "featureState", "ref": "entry-point-recognition"}],
    "R13": [{"kind": "report", "ref": "/$defs/ComparisonPanelV1"}, {"kind": "envelope", "ref": "/properties/run"}, {"kind": "envelope", "ref": "/properties/advisoryReport"}],
    "R14": [{"kind": "report", "ref": "/$defs/HistoryPanelV1/properties/selection"}, {"kind": "report", "ref": "/$defs/HistoryRunV1"}, {"kind": "featureState", "ref": "explicit-older-run-selection"}],
    "R15": [{"kind": "report", "ref": "/$defs/BudgetProfileV1"}, {"kind": "report", "ref": "/$defs/ItemProjectionV1"}, {"kind": "report", "ref": "/$defs/GraphSlotV1/properties/hostProjection"}],
    "R16": [{"kind": "report", "ref": "/$defs/PanelNotPresentV1"}, {"kind": "report", "ref": "/$defs/StaticParityV1"}, {"kind": "report", "ref": "/$defs/DisclosuresV1"}],
    "R17": [{"kind": "report", "ref": "/$defs/BudgetProfileV1/properties/maxJsonDepth"}, {"kind": "obligation", "ref": "RP-OBL-B01"}],
    "R18": [{"kind": "obligation", "ref": "RP-OBL-B02"}],
    "R19": [{"kind": "report", "ref": "/properties/featureStates"}, {"kind": "obligation", "ref": "RP-OBL-B02"}],
    "R20": [{"kind": "report", "ref": "/$defs/PathDisclosureV1"}, {"kind": "envelope", "ref": "/properties/projectRoot"}],
    "R21": [{"kind": "obligation", "ref": "RP-OBL-H01"}],
    "R22": [{"kind": "envelope", "ref": "/properties/requestId"}, {"kind": "obligation", "ref": "RP-OBL-H01"}],
    "R23": [{"kind": "envelope", "ref": "/properties/retentionDisclosure"}, {"kind": "envelope", "ref": "/properties/availability"}, {"kind": "featureState", "ref": "declared-configuration"}],
    "R24": [{"kind": "report", "ref": "/properties/supportedReportViews"}, {"kind": "envelope", "ref": "/properties/advisoryReport"}, {"kind": "envelope", "ref": "/properties/queryRecord"}],
}

OBLIGATIONS = {
    "RP-OBL-B01": "M4 browser lane on the built single file: offline/no-fetch, script-safe embedding, generated runtime validation with the report codec, static parity section equality with staticParityGoldens, exports. Not executed.",
    "RP-OBL-B02": "M4 accessibility and help lane, including feature-state text. Not executed.",
    "RP-OBL-H01": "Host delivery/platform: guarded browser opening and atomic publication bound to requestId/Run; delivery goldens are semantic references only. Not executed.",
    "RP-OBL-M01": "M4 measurement plan (contract section 9). Not executed; no performance claim.",
    "RP-OBL-G01": "M1 generation registry: register envelope5, inventory5 and report-projection:1 source bytes; generator compatibility was not run by this author (review A9 stays open).",
    "RP-OBL-C01": "Envelope owner: an invocation interrupted before any committed Run has no admissible command-envelope:5 kind=failure form (errors must be non-empty; no DomainDetailCode names an interruption). Not invented here.",
    "RP-OBL-E01": "After acceptance, root rebinds product design lock and emitters to envelope5/inventory5 in new integration records (the metadata-v2 acceptance stays historical) and the workflows reference model admits golden fit-ephemeral-non-authoritative.",
}

REVIEW_MAP = {
    "RPR3-1/G1": "review-G1-complete-lower-bound-sliced", "RPR3-1/G1-truncated-page": "review-G1-truncated-page-lower-bound-sliced",
    "RPR3-1/G2": "review-G2-truncated-bound-sliced-without-cap", "RPR3-1/G3": "review-G3-complete-exact-sliced",
    "RPR3-2/B1": "review-B1-three-pinned-steps-envelope-boundary", "RPR3-2/B1-control": "review-B1-control-one-pinned-step", "RPR3-2/maximal-legal": "maximal-legal-step-terminations-audit-failure",
    "RPR3-3/D1-document": "review-D1-renderer-failure-over-query-refusal-in-delivered-report", "RPR3-3/D2": "review-D2-interrupted-step-without-cancellation",
    "A1/S1": "review-S1-descriptor-not-retained-replan", "A1/S1-uncontradicted": "review-A1-descriptor-not-retained-uncontradicted-steering-disclosed",
    "A2/H1": "review-H1-snapshot-count-understated-host-asserted-disclosed",
    "prior/Q1": "review-Q1-fit-truncated-short-page", "prior/S2": "review-S2-slot-items-sliced", "prior/Q7b": "review-Q7b-iterative-depth-200000",
}


if __name__ == "__main__":
    (HERE / "fixtures.json").write_bytes(json.dumps(build(), indent=1, ensure_ascii=False).encode("utf-8") + b"\n")
