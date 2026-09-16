"""Deterministic fixtures for the author-04 report/fit successor candidate.

Positive documents are assembled from the pinned witness corpus plus labelled constructions: a small complete fact
graph answered by report_model.MockGraphOwner, invocation ledgers (with the invocation cancellation carrier) following
inventory5 step sequences, and panels produced by the reference byte law against the effective exploration budget.
Shape/join material only; not semantic proof.
"""
import ast
import copy
import hashlib
import importlib.util
import json
import types
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
    failure["schemaMajor"] = 6
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


SKIPPED_TERMINATION = {"class": "request-rejected", "errorCode": "REQUEST.PRECONDITION_FAILED"}


def ledger(m, command, request_id, terminations, run_ids=None, mode_ephemeral=False, cancellation=None, skipped=None, variant=None):
    """Steps are the exact expansion of a plannable owner/builtin-step-planning.v1.json variant (the first plannable one unless named).
    skipped: {stepId: skipReason}. A skipped step is recorded exactly as the owner reference model records it
    (workflows_model.v1.py run_invocation): no attempts, its skipReason and termination request-rejected REQUEST.PRECONDITION_FAILED."""
    variants = [v for v in OWNER.PLANNING_COMMANDS[command] if v["status"] == "plannable"]
    chosen = next(v for v in variants if variant in (None, v["variant"]))
    steps = []
    render_at = next(i for i, spec in enumerate(chosen["steps"]) if spec["kind"] == "render")
    for i, spec in enumerate(chosen["steps"]):
        kind = spec["kind"]
        step = {"stepId": i, "kind": kind, "requirement": spec["requirement"], "dependsOn": list(spec["dependsOn"]), "dependencyGate": spec["dependencyGate"],
                "planRole": spec["planRole"], "recorded": False}
        if i < render_at:
            if skipped and i in skipped:
                step.update(recorded=True, outcome="skipped", skipReason=skipped[i], attempts=[], termination=copy.deepcopy(SKIPPED_TERMINATION))
                steps.append(step)
                continue
            term = terminations.get(i, {"class": "success"})
            outcome = OUTCOME[term["class"]]
            step.update(recorded=True, outcome=outcome, attempts=[{"executionId": "exec1_" + h("exec-%s-%d" % (request_id, i))[:32], "outcome": outcome}], termination=term)
            if run_ids and i in run_ids:
                step["analysisRunId"] = run_ids[i]
        steps.append(step)
    return {"requestId": request_id, "workflow": {"kind": "builtin", "name": command}, "mode": {"interactive": False, "ci": True, "ephemeral": mode_ephemeral},
            "cancellation": copy.deepcopy(cancellation or NO_CANCELLATION), "planVariant": chosen["variant"], "steps": steps, "missingChildren": M.missing_children(steps), "provenance": OWNER.PROVENANCE["ledger"]}


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
    run_envelope = {"schemaFamily": "opensip.product.envelope", "schemaMajor": 6, "kind": "run", "requestId": request_id, "projectId": PRJ,
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
    pivot_ledger = ledger(m, "audit", request_id, {}, {0: "run3:" + h("pivot-run"), 1: R}, variant="with-pivot")
    bases["audit-with-pivot"] = doc("audit", audit_env, pivot_ledger, ctx["exploration"](audit_env, "audit", True, pivot_ledger))

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
    baseline_ledger = ledger(m, "analyze", request_id, {}, {0: R}, variant="baseline-no-pivot")
    bases["analyze-baseline-run"] = doc("analyze", audit_env, baseline_ledger, ctx["exploration"](audit_env, "analyze", True, baseline_ledger))
    export_ledger = ledger(m, "analyze", request_id, {}, {0: R}, variant="primary-with-optional-export")
    export_panels = ctx["exploration"](default_env, "analyze", False, export_ledger)
    export_panels["comparison"] = {"state": "omitted", "reason": "not-selected"}
    bases["analyze-with-optional-export"] = doc("analyze", default_env, export_ledger, export_panels)
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
    # skipped required steps (owner-valid DAGs): the dependency did not complete, the skipped record is preserved and excluded from the aggregate
    bases["fit-analysis-rejected-query-skipped"] = doc("fit", M.failure_envelope(default_env, CONFIG_REFUSAL(m)),
                                                      ledger(m, "fit", request_id, {0: CONFIG_REFUSAL(m)}, skipped={1: "dependency-not-completed"}), fit_panels_none)
    bases["audit-analysis-rejected-comparison-skipped"] = doc("audit", M.failure_envelope(default_env, CONFIG_REFUSAL(m)),
                                                             ledger(m, "audit", request_id, {0: CONFIG_REFUSAL(m)}, skipped={1: "dependency-not-completed"}, variant="no-pivot"),
                                                             {p: no_result for p in OWNER.PANELS["audit"]})

    # query commands ---------------------------------------------------------
    list_context = {"projectId": PRJ, "resolvedView": {"runId": R}, "coverage": "complete", "availability": "retained", "truncated": False, "totalItems": 1, "advisory": True}
    cands_env = {"schemaFamily": "opensip.product.envelope", "schemaMajor": 6, "kind": "query", "requestId": request_id, "projectId": PRJ, "termination": {"class": "success"}, "exitCode": 0,
                 "query": {"kind": "query", "items": 1, "truncated": False, "completenessMet": True, "advisory": True}, "querySurface": "candidate-list",
                 "queryRecord": {"surface": "candidate-list", "context": list_context, "includeSuppressed": False, "candidates": [candidate(0)],
                                 "evidenceLevels": {"proof-backed": 1, "partial-coverage": 0, "advisory-only": 0}, "suppressedCount": 0}}
    cands_ledger = ledger(m, "candidates", request_id, {})
    bases["candidates-run"] = doc("candidates", cands_env, cands_ledger, ctx["exploration"](cands_env, "candidates", False, cands_ledger))

    inspection = m["inspection"]
    facts = sorted(set(inspection["inspection"]["facts"]), key=lambda s: s.encode())
    inspection["inspection"].update(runId=R, facts=facts)
    inspection["context"] = dict(list_context, totalItems=len(facts))
    inspect_env = {"schemaFamily": "opensip.product.envelope", "schemaMajor": 6, "kind": "query", "requestId": request_id, "projectId": PRJ, "termination": {"class": "success"}, "exitCode": 0,
                   "query": {"kind": "query", "items": len(facts), "truncated": False, "completenessMet": True, "advisory": True}, "querySurface": "candidate-inspection", "queryRecord": inspection}
    bases["inspect-run"] = doc("inspect", inspect_env, ledger(m, "inspect", request_id, {}), {"graph": {"state": "omitted", "reason": "not-selected"}})

    brief = m["brief"]
    brief["brief"].update(runId=R, truncated=False)
    brief["context"] = dict(list_context, totalItems=len(brief["brief"]["candidates"]))
    brief_env = {"schemaFamily": "opensip.product.envelope", "schemaMajor": 6, "kind": "query", "requestId": request_id, "projectId": PRJ, "termination": {"class": "success"}, "exitCode": 0,
                 "query": {"kind": "query", "items": len(brief["brief"]["candidates"]), "truncated": False, "completenessMet": True, "advisory": True}, "querySurface": "review-brief", "queryRecord": brief}
    bases["review-brief-run"] = doc("review-brief", brief_env, ledger(m, "review-brief", request_id, {}), {"graph": {"state": "omitted", "reason": "not-selected"}})
    failure = m["failure"]
    bases["review-brief-failure"] = doc("review-brief", failure, ledger(m, "review-brief", failure["requestId"], {0: failure["termination"]}), {"graph": no_result})

    repair = m["repair"]
    descriptor = repair["plan"]["descriptor"]
    descriptor["projectId"] = PRJ
    repair["plan"]["repairPlanId"] = QSP.Wlegacy.wid("repairplan2", "workflow.repair-plan", descriptor)
    repair["preview"].update(repairPlanId=repair["plan"]["repairPlanId"], snapshotId=descriptor["snapshotId"], applicable=descriptor["applicable"], unmetPreconditions=copy.deepcopy(descriptor["unmetPreconditions"]))
    repair_env = {"schemaFamily": "opensip.product.envelope", "schemaMajor": 6, "kind": "query", "requestId": request_id, "projectId": PRJ, "termination": {"class": "success"}, "exitCode": 0,
                  "query": {"kind": "query", "items": len(descriptor["edits"]), "truncated": False, "completenessMet": descriptor["applicable"], "advisory": False},
                  "querySurface": "repair-preview", "queryRecord": repair}
    bases["repair-preview"] = doc("repair-preview", repair_env, ledger(m, "repair-preview", request_id, {}), {})

    inventory = json.loads(OWNER.dump(OWNER.inventory5()))
    return {"schemaVersion": 1,
            "standing": "AUTHOR-08 candidate fixtures: constructed shape/join material from the pinned witness corpus and a mock owner over complete fixture facts, plus interruption goldens produced by the pinned owner model successor, native projector and composite join; no semantic proof, no product qualification",
            "bases": bases, "reportCases": report_cases(bases, m), "envelopeCases": envelope_cases(bases, m) + interruption_join_cases(bases, m), "aggregateCases": aggregate_cases(R),
            "deliveryGoldens": delivery_goldens(m, R, request_id, fit_env, cands_env, inventory, default_env),
            "interruptionGoldens": interruption_goldens(m, R, request_id, inventory),
            "staticParityGoldens": {name: {"textSha256": b["staticParity"]["textSha256"], "textBytes": b["staticParity"]["textBytes"],
                                           "firstLine": M.static_parity_text(b["envelope"], next(c for c in inventory["commands"] if c["name"] == b["command"]), b["disclosures"]).splitlines()[0][:160]}
                                    for name, b in bases.items()},
            "featureMap": FEATURE_MAP, "obligations": OBLIGATIONS, "reviewCounterexamples": REVIEW_MAP}


def CONFIG_REFUSAL(m):
    return {"class": "request-rejected", "errorCode": "REQUEST.PRECONDITION_FAILED", "domainDetail": {"code": "CONFIG.INVALID", "remedy": "fix the effective policy source", "subject": m["plan"]}}


CANONICAL_PATH = ARCH / "docs/coop/design-corrections/foundation/canonical.py"
TRIAL = ARCH / OWNER.INTERRUPTION_TRIAL / "subject"
MODEL_FUNCTIONS = {"Refusal", "terminate", "dd", "analysis_termination", "comparison_termination", "exit_code", "validate_dag", "raw_sha", "synthetic_execution_id", "_exec_id", "run_invocation"}
NOTICE = {"capabilityId": "calls", "languageMode": "js-synthesized", "workspaceRoot": "packages/app"}
GOLDEN_STATUS = "delivered-in-candidate-pending-joint-review"
_OWNERS = {}


def interruption_owners():
    """Pinned owner code executed by the interruption goldens, compiled from verified bytes with no import shim: the workflow model's pure functions in
    the historical form and with exactly the selected line-380 successor, the native availability projector (with the requested-capability vocabulary
    admission used by the L02 regression) and the selected composite ledger join."""
    if _OWNERS:
        return _OWNERS
    canon = types.ModuleType("foundation_canonical")
    exec(compile(CANONICAL_PATH.read_bytes(), "pinned-foundation-canonical", "exec"), canon.__dict__)
    source = (ARCH / OWNER.WORKFLOWS_MODEL).read_bytes()
    successor = json.loads((TRIAL / "model-successor.json").read_bytes())
    assert hashlib.sha256(source).hexdigest() == successor["ownerSha256"] and successor["owner"] == OWNER.WORKFLOWS_MODEL
    text = source.decode()
    span = successor["selector"]
    assert "\n".join(text.splitlines()[span["startLine"] - 1:span["endLine"]]) == successor["before"] and text.count(successor["before"]) == 1
    models = {}
    for label, body in (("historical", text), ("successor", text.replace(successor["before"], successor["after"]))):
        nodes = []
        for node in ast.parse(body).body:
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name in MODEL_FUNCTIONS:
                nodes.append(node)
            elif isinstance(node, ast.Assign):
                names = {t.id for t in node.targets if isinstance(t, ast.Name)}
                if names & MODEL_FUNCTIONS or (names and all(n.isupper() for n in names) and not any(isinstance(n, ast.Call) for n in ast.walk(node.value))):
                    nodes.append(node)
        module = types.ModuleType("scoped_workflow_owner_" + label)
        module.__dict__.update(hashlib=hashlib, json=json, canonical=canon)
        exec(compile(ast.Module(body=nodes, type_ignores=[]), "pinned-workflow-owner#pure-extract-" + label, "exec"), module.__dict__)
        models[label] = module
    native_nodes = [n for n in ast.parse((ARCH / OWNER.NATIVE_MODEL).read_bytes()).body
                    if (isinstance(n, ast.FunctionDef) and n.name in ("release_absence_notices", "invocation_availability", "admit_requested_capabilities"))
                    or (isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "PUBLIC_ROUTE_REMEDIES" for t in n.targets))]
    assert len(native_nodes) == 4
    native = {"CAPABILITY_MATRIX": json.loads((ARCH / OWNER.NATIVE_MATRIX).read_bytes()), "AdmissionError": canon.AdmissionError}
    exec(compile(ast.Module(body=native_nodes, type_ignores=[]), "pinned-native-availability-functions", "exec"), native)
    join = types.ModuleType("interruption_ledger_join")
    exec(compile((TRIAL / "ledger_join.py").read_bytes(), "pinned-interruption-ledger-join", "exec"), join.__dict__)
    _OWNERS.update(canonical=canon, models=models, native=native, join=join, successor=successor)
    return _OWNERS


def owner_step_result(m, spec, run_ids):
    """Schema-valid already-admitted domain results scripted into the owner model (synthetic inputs, not replays)."""
    kind = spec["kind"]
    if kind == "analysis":
        return {"kind": "analysis", "authority": "authoritative", "runId": run_ids[spec["stepId"]], "planId": m["plan"], "verdict": "pass", "requiredCoverage": "satisfied",
                "durability": "committed", "deficiency": "none", "secondaryDeficiencies": []}
    if kind == "comparison":
        return {"kind": "comparison", "comparisonResultId": m["comparison"]["comparisonResultId"], "currentRunId": run_ids[spec["params"]["currentStep"]],
                "baselineId": m["comparison"]["descriptor"]["baselineId"], "verdict": "pass", "comparisonPerformed": True, "counts": {"entries": 0, "gating": 0, "indeterminate": 0}}
    if kind == "query":
        return {"kind": "query", "items": 1, "truncated": False, "completenessMet": True, "advisory": True}
    if kind == "repair-preview":
        return {"kind": "repair-preview", "repairPlanId": m["repair"]["plan"]["repairPlanId"], "snapshotId": m["repair"]["plan"]["descriptor"]["snapshotId"], "applicable": True, "unmetPreconditions": []}
    if kind == "export-delivery":
        return {"kind": "export-delivery", "delivered": True}
    raise AssertionError("no scripted result for " + kind)


def selection_context(record):
    """Synthetic trusted host selection context: one retained selection per started, unskipped analysis/verify step (the first names one absence).
    Completeness of this context is host custody and is not proved here."""
    per_step = []
    for spec, result in zip(record["orderedSteps"], record["stepResults"]):
        if spec["kind"] in ("analysis", "verify") and result["outcome"] != "skipped" and result["attempts"]:
            per_step.append({"stepId": spec["stepId"], "undeclared": [] if per_step else [copy.deepcopy(NOTICE)]})
    return {"requestId": record["requestId"], "workflow": copy.deepcopy(record["workflow"]), "perStep": per_step}


def ledger_steps(record):
    """The report ledger step projection of an owner InvocationRecord (the form report admit_envelope joins)."""
    out = []
    for spec, result in zip(record["orderedSteps"], record["stepResults"]):
        step = {"stepId": spec["stepId"], "kind": spec["kind"], "requirement": spec["requirement"], "recorded": True, "outcome": result["outcome"], "termination": result["termination"]}
        if spec["kind"] in ("analysis", "verify") and result["outcome"] == "completed" and result.get("result", {}).get("runId"):
            step["analysisRunId"] = result["result"]["runId"]
        if result["outcome"] == "skipped":
            step["skipReason"] = result["skipReason"]
        out.append(step)
    return out


def interruption_goldens(m, R, request_id, inventory):
    """RP-OBL-C01/C02 delivered-in-candidate goldens (pending joint review of envelope5 with the interruption unit). Each builtin plannable variant is executed by
    the pinned owner model with the selected line-380 successor; the output carrier is report_model.interruption_envelope and the actual composite entry point
    validate_interruption_delivery admits it with the native invocation_availability projector. Preplanning carriers use validate_preplanning_delivery."""
    owners = interruption_owners()
    successor, historical, join, project = owners["models"]["successor"], owners["models"]["historical"], owners["join"], owners["native"]["invocation_availability"]
    kinds = OWNER.output_kinds()
    scenarios, profile, preplanning, converted = [], [], [], []
    for command, variants in OWNER.PLANNING_COMMANDS.items():
        row = next(c for c in inventory["commands"] if c["name"] == command)
        parity = "capability-availability" in row["parityFields"]
        formats = [f for f in ("human", "json", "agent", "html") if f in row["formats"]]
        assert formats == ["human", "json", "agent", "html"], command
        for variant in variants:
            if variant["status"] != "plannable":
                continue
            specs = [{"stepId": i, "kind": s["kind"], "requirement": s["requirement"], "dependsOn": list(s["dependsOn"]), "dependencyGate": s["dependencyGate"],
                      "retryPolicy": "none", "params": copy.deepcopy(s["representativeParams"])} for i, s in enumerate(variant["steps"])]
            run_ids = {i: (R if s["planRole"] == "primary-analysis" else "run3:" + h("pivot-run")) for i, s in enumerate(variant["steps"]) if s["kind"] == "analysis"}
            render_at = next(i for i, s in enumerate(specs) if s["kind"] == "render")
            completed = {str(i): [{"event": "completed", "result": owner_step_result(m, s, run_ids)}] for i, s in enumerate(specs) if i < render_at}
            rejected = dict(completed, **{"0": [{"event": "rejected", "errorCode": "REQUEST.PRECONDITION_FAILED", "detail": "CONFIG.INVALID", "remedy": "fix the effective policy source"}]})
            base = {"schemaFamily": "opensip.product.invocation", "schemaMajor": 3, "requestId": request_id, "projectId": m["project"], "workflow": {"kind": "builtin", "name": command},
                    "mode": {"interactive": False, "ci": True, "ephemeral": False}, "orderedSteps": specs}
            for name, script in (("signal-before-first-step", {"cancelAt": {"stepId": 0, "signal": "SIGINT"}}),
                                 ("signal-before-required-render", dict(completed, cancelAt={"stepId": render_at, "signal": "SIGTERM"})),
                                 ("first-step-rejected-signal-before-required-render", dict(rejected, cancelAt={"stepId": render_at, "signal": "SIGHUP"}))):
                record, code = successor.run_invocation(copy.deepcopy(base), copy.deepcopy(script))
                old_record, old_code = historical.run_invocation(copy.deepcopy(base), copy.deepcopy(script))
                assert old_record == record and old_code == code == 130, (command, variant["variant"], name)
                selection = selection_context(record)
                envelope = M.interruption_envelope(record, parity, m["project"], project, selection)
                assert join.validate_interruption_delivery(record, envelope, selection, inventory, project)
                assert ("run" if "runId" in record["termination"] else "failure") == envelope["kind"]
                assert envelope["kind"] == kinds[command + "/" + variant["variant"]]["interruptedWithCommittedRun" if envelope["kind"] == "run" else "interruptedWithoutCommittedRun"]
                scenarios.append({"id": "%s/%s/%s" % (command, variant["variant"], name), "command": command, "variant": variant["variant"], "scenario": name, "status": GOLDEN_STATUS,
                                  "formats": formats, "entryPoint": "validate_interruption_delivery", "ownerScript": script, "invocationRecord": record, "selectionContext": selection,
                                  "envelope": envelope, "exitCode": code, "outputKind": envelope["kind"], "artifactDelivered": None,
                                  "historicalOwnerModelIdentical": True, "hostCustody": "synthetic trusted selection context; completeness is a host custody duty"})
    # C02: a generic profile with an optional analysis commit (not a builtin plan); the historical model erases the optional Run, the successor names it
    analysis_params = copy.deepcopy(OWNER.PLANNING_COMMANDS["default"][0]["steps"][0]["representativeParams"])
    profile_specs = [{"stepId": 0, "kind": "analysis", "requirement": "optional", "dependsOn": [], "dependencyGate": "completed", "retryPolicy": "none", "params": analysis_params},
                     {"stepId": 1, "kind": "render", "requirement": "required", "dependsOn": [], "dependencyGate": "terminal", "retryPolicy": "none",
                      "params": {"kind": "render", "format": "json", "destination": "stdout", "sourceSteps": [], "required": True}}]
    workflow = {"kind": "profile", "contributionId": "org.example.workflow", "activationId": "review", "profileVersion": "1.0.0"}
    for signal in ("SIGINT", "SIGTERM", "SIGHUP"):
        base = {"schemaFamily": "opensip.product.invocation", "schemaMajor": 3, "requestId": request_id, "projectId": m["project"], "workflow": workflow,
                "mode": {"interactive": False, "ci": True, "ephemeral": False}, "orderedSteps": profile_specs}
        script = {"0": [{"event": "completed", "result": owner_step_result(m, profile_specs[0], {0: R})}], "cancelAt": {"stepId": 1, "signal": signal}}
        record, code = successor.run_invocation(copy.deepcopy(base), copy.deepcopy(script))
        old_record, old_code = historical.run_invocation(copy.deepcopy(base), copy.deepcopy(script))
        assert code == old_code == 130 and record["stepResults"] == old_record["stepResults"]
        assert record["termination"] == {"class": "interrupted", "signal": signal, "runId": R} and old_record["termination"] == {"class": "interrupted", "signal": signal}
        selection = selection_context(record)
        envelope = M.interruption_envelope(record, True, m["project"], project, selection)
        assert envelope["kind"] == "run" and join.validate_interruption_delivery(record, envelope, selection, inventory, project)
        erased = {k: copy.deepcopy(v) for k, v in envelope.items() if k != "run"}
        erased.update(kind="failure", errors=[], termination=copy.deepcopy(old_record["termination"]))
        profile.append({"id": "profile-optional-analysis-committed/" + signal, "planningOrigin": "generic-profile composition (not a builtin plan; RP-OBL-X01 surface)", "status": GOLDEN_STATUS,
                        "formats": ["json"], "entryPoint": "validate_interruption_delivery", "ownerScript": script, "invocationRecord": record, "historicalOwnerTermination": old_record["termination"],
                        "selectionContext": selection, "envelope": envelope, "exitCode": code, "outputKind": "run", "historicalChoiceEnvelope": erased})
    for command in [None] + list(OWNER.PLANNING_COMMANDS):
        parity = command is not None and "capability-availability" in next(c for c in inventory["commands"] if c["name"] == command)["parityFields"]
        context = {"stage": "before-planning", "requestId": request_id, "signal": "SIGINT"}
        envelope = M.preplanning_envelope(context, parity, project)
        assert join.validate_preplanning_delivery(context, envelope, command, inventory, project)
        assert command is None or envelope["kind"] == kinds[command + "/" + next(v for v in OWNER.PLANNING_COMMANDS[command] if v["status"] == "plannable")["variant"]]["preplanning"]
        preplanning.append({"id": "preplanning/" + (command or "unresolved-command"), "command": command, "status": GOLDEN_STATUS,
                            "formats": ["human", "json", "agent", "html"] if command else None, "entryPoint": "validate_preplanning_delivery", "hostContext": context,
                            "envelope": envelope, "exitCode": 130, "outputKind": "failure", "availability": "explicit empty account" if parity else "absent"})
    fake = {"code": "evidence.purged", "remedy": "re-run the analysis", "subject": R}
    for command, former_steps in (("analyze", "import completed, analysis cancelled, render cancelled (import is not plannable by the declared grammar: RP-OBL-P01; the plannable primary expansion is used)"),
                                  ("candidates", "query cancelled, render cancelled")):
        source = next(s for s in scenarios if s["id"] == command + "/primary/signal-before-first-step")
        env = source["envelope"]
        forms = {"errors-empty": (env, "accept"), "errors-omitted": ({k: v for k, v in env.items() if k != "errors"}, "SCHEMA-ENV"),
                 "unrelated-detail-invented": (dict(copy.deepcopy(env), errors=[fake]), "J-ENV-INTERRUPTION-DETAIL"),
                 "envelope-major-5": (dict(copy.deepcopy(env), schemaMajor=5), "SCHEMA-ENV")}
        if "availability" in env:
            forms["availability-omitted"] = ({k: v for k, v in env.items() if k != "availability"}, "J-ENV-CAPABILITY-AVAILABILITY")
        for fmt in source["formats"]:
            converted.append({"id": "pending-C01-%s-signal-before-commit/%s" % (command, fmt), "formerStatus": "pending-integration: every author-07 form was refused by envelope5",
                              "formerSteps": former_steps, "status": GOLDEN_STATUS, "deliveredBy": source["id"], "format": fmt, "obligation": "RP-OBL-C01",
                              "forms": {name: {"envelope": e, "expectedHostOutcome": code} for name, (e, code) in forms.items()}})
    return {"standing": "delivered in this candidate over envelope6 and the conditionally accepted interruption unit; pending joint independent review with envelope5 and root source selection; no runtime claim",
            "scenarios": scenarios, "profileOptionalCommit": profile, "preplanning": preplanning, "convertedPending": converted}


def QUERY_REFUSAL(run_id):
    return {"class": "request-rejected", "errorCode": "REQUEST.PRECONDITION_FAILED", "runId": run_id, "domainDetail": {"code": "QUERY.VIEW_UNKNOWN", "remedy": "select a sealed run", "subject": run_id}}


def delivery_goldens(m, R, request_id, run_template, query_template, inventory, audit_template):
    """Per-renderer semantic goldens: one recorded query outcome, then each renderer selection. Prior step terminations are carried unchanged."""
    analysis = {"kind": "analysis", "requirement": "required", "recorded": True, "outcome": "completed", "termination": {"class": "success"}, "analysisRunId": R}
    refused = {"kind": "query", "requirement": "required", "recorded": True, "outcome": "rejected", "termination": QUERY_REFUSAL(R)}
    io_failed = {"kind": "query", "requirement": "required", "recorded": True, "outcome": "failed",
                 "termination": {"class": "operational-failed", "errorCode": "HOST.IO_FAILURE", "faultCause": "host-io", "runId": R,
                                 "domainDetail": {"code": "evidence.purged", "remedy": "re-run the analysis", "subject": R}}}
    unrun_refused = {"kind": "query", "requirement": "required", "recorded": True, "outcome": "rejected",
                     "termination": {"class": "request-rejected", "errorCode": "REQUEST.PRECONDITION_FAILED", "domainDetail": {"code": "QUERY.VIEW_UNKNOWN", "remedy": "select a sealed run"}}}
    config_refusal = CONFIG_REFUSAL(m)
    analysis_rejected = {"kind": "analysis", "requirement": "required", "recorded": True, "outcome": "rejected", "termination": config_refusal}
    query_skipped = {"kind": "query", "requirement": "required", "recorded": True, "outcome": "skipped", "skipReason": "dependency-not-completed", "termination": SKIPPED_TERMINATION}
    comparison_skipped = dict(query_skipped, kind="comparison")
    pivot_rejected = {"kind": "analysis", "requirement": "required", "recorded": True, "outcome": "rejected",
                      "termination": {"class": "request-rejected", "errorCode": "REQUEST.PRECONDITION_FAILED", "domainDetail": {"code": "CONFIG.INVALID", "remedy": "admit the baseline pivot closure", "subject": "pivot"}}}
    primary_failed = {"kind": "analysis", "requirement": "required", "recorded": True, "outcome": "failed",
                      "termination": {"class": "operational-failed", "errorCode": "HOST.IO_FAILURE", "faultCause": "host-io", "domainDetail": {"code": "evidence.purged", "remedy": "re-run the analysis", "subject": "primary"}}}
    query_failed = {"kind": "query", "requirement": "required", "recorded": True, "outcome": "failed",
                    "termination": {"class": "operational-failed", "errorCode": "HOST.IO_FAILURE", "faultCause": "host-io", "domainDetail": {"code": "evidence.missing", "remedy": "restore the retained bytes", "subject": R}}}
    sigint = {"requested": True, "signal": "SIGINT", "phase": "before-settle"}
    scenarios = [
        # interruption with genuine earlier recorded details: errors are exactly those details (delivered under envelope5)
        ("audit-pivot-rejected-primary-committed-signal-during-required-render", "audit", [pivot_rejected, analysis, comparison_skipped], {"requirement": "required", "result": "cancelled"}, R, audit_template, sigint),
        ("fit-analysis-rejected-query-skipped-signal-during-required-render", "fit", [analysis_rejected, query_skipped], {"requirement": "required", "result": "cancelled"}, None, run_template, sigint),
        ("review-brief-query-failed-signal-during-required-render", "review-brief", [query_failed], {"requirement": "required", "result": "cancelled"}, None, query_template,
         {"requested": True, "signal": "SIGTERM", "phase": "before-settle"}),
        ("audit-pivot-rejected-primary-failed-signal-during-required-render", "audit", [pivot_rejected, primary_failed, comparison_skipped], {"requirement": "required", "result": "cancelled"}, None, run_template, sigint),
        ("audit-pivot-rejected-primary-committed-comparison-skipped-required-render-failed", "audit", [pivot_rejected, analysis, comparison_skipped], {"requirement": "required", "result": "failed"}, R, run_template),
        ("fit-analysis-rejected-query-skipped-render-written", "fit", [analysis_rejected, query_skipped], {"requirement": "required", "result": "written"}, None, run_template),
        ("fit-analysis-rejected-query-skipped-required-render-failed", "fit", [analysis_rejected, query_skipped], {"requirement": "required", "result": "failed"}, None, run_template),
        ("fit-analysis-rejected-query-skipped-optional-render-failed", "fit", [analysis_rejected, query_skipped], {"requirement": "optional", "result": "failed"}, None, run_template),
        ("audit-analysis-rejected-comparison-skipped-render-written", "audit", [analysis_rejected, comparison_skipped], {"requirement": "required", "result": "written"}, None, run_template),
        ("audit-analysis-rejected-comparison-skipped-required-render-failed", "audit", [analysis_rejected, comparison_skipped], {"requirement": "required", "result": "failed"}, None, run_template),
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
            origin = ("generic-profile-d9-composition (optional render; no builtin plan and no core CLI profile surface, RP-OBL-X01)" if render and render["requirement"] == "optional"
                      else "builtin:" + command + " (D9/envelope semantics over steps of a bound plannable variant; not a ledger document)")
            out.append(dict({"id": sid + "/" + fmt, "scenario": sid, "command": command, "planningOrigin": origin, "priorSteps": prior, "render": render, "committedRunId": run_id},
                            **M.delivery_outcome(fmt, prior, render, template, run_id, row, cancellation)))
    return out


def aggregate_cases(R):
    s = lambda cls, **kw: dict({"class": cls}, **kw)
    step = lambda kind, term, outcome="completed", requirement="required", recorded=True, run=None: dict(
        {"kind": kind, "requirement": requirement, "recorded": recorded, "outcome": outcome, "termination": term}, **({"analysisRunId": run} if run else {}))
    renderer = M.renderer_failure(R)
    io = s("operational-failed", errorCode="HOST.IO_FAILURE", faultCause="host-io", domainDetail={"code": "evidence.purged", "remedy": "re-run"})
    skipped_t = copy.deepcopy(SKIPPED_TERMINATION)
    reject = s("request-rejected", errorCode="REQUEST.PRECONDITION_FAILED", domainDetail={"code": "CONFIG.INVALID", "remedy": "fix the effective policy source"})
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
        # skipped steps: excluded from the D9 ordering exactly as the owner reference model; all-skipped aggregates to success
        {"id": "review-RPR4-2-skipped-required-request-rejected", "steps": [step("analysis", s("success"), run=R), step("query", skipped_t, "skipped")], "cancellation": None, "expect": s("success")},
        {"id": "review-RPR4-2-skipped-required-indeterminate", "steps": [step("analysis", s("success"), run=R), step("query", s("indeterminate", reasonCodes=["VERDICT.INDETERMINATE"]), "skipped")],
         "cancellation": None, "expect": s("success")},
        {"id": "all-required-steps-skipped", "steps": [step("query", skipped_t, "skipped"), step("comparison", skipped_t, "skipped")], "cancellation": None, "expect": s("success")},
        {"id": "required-rejection-then-required-skipped", "steps": [step("analysis", reject, "rejected"), step("query", skipped_t, "skipped")], "cancellation": None, "expect": reject},
        {"id": "required-success-optional-failed-required-skipped", "steps": [step("analysis", s("success"), run=R), step("analysis", io, "failed", "optional"), step("comparison", skipped_t, "skipped")],
         "cancellation": None, "expect": s("success")},
        {"id": "required-policy-failed-optional-skipped", "steps": [step("analysis", s("policy-failed", runId=R), run=R), step("query", skipped_t, "skipped", "optional")], "cancellation": None,
         "expect": s("policy-failed", runId=R)},
        {"id": "skipped-is-settled-before-settle-refused", "steps": [step("analysis", reject, "rejected"), step("query", skipped_t, "skipped")],
         "cancellation": {"requested": True, "signal": "SIGINT", "phase": "before-settle"}, "refusal": "J-LEDGER-CANCELLATION"},
        {"id": "skipped-is-settled-after-settle-not-reclassified", "steps": [step("analysis", reject, "rejected"), step("query", skipped_t, "skipped")],
         "cancellation": {"requested": True, "signal": "SIGTERM", "phase": "after-settle"}, "expect": reject},
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
        case("envelope-major-5-refused", A, [{"op": "set", "path": "/envelope/schemaMajor", "value": 5}], "SCHEMA"),
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
        case("ledger-step-kind-drift", A, [{"op": "set", "path": "/invocationLedger/steps/1/kind", "value": "query"}], "J-LEDGER-PLAN"),
        case("ledger-terminal-gate-on-analysis", A, [{"op": "set", "path": "/invocationLedger/steps/0/dependencyGate", "value": "terminal"}], "J-LEDGER-DAG"),
        case("ledger-forward-dependency", A, [{"op": "set", "path": "/invocationLedger/steps/0/dependsOn", "value": [1]}], "J-LEDGER-DAG"),
        case("ledger-plan-variant-label-mismatch", A, [{"op": "set", "path": "/invocationLedger/planVariant", "value": "with-pivot"}], "J-LEDGER-PLAN"),
        case("ledger-audit-comparison-dependency-dropped", A, [{"op": "set", "path": "/invocationLedger/steps/1/dependsOn", "value": []}], "J-LEDGER-PLAN"),
        case("ledger-audit-pivot-role-swapped", "audit-with-pivot", [{"op": "set", "path": "/invocationLedger/steps/0/planRole", "value": "primary-analysis"},
                                                                     {"op": "set", "path": "/invocationLedger/steps/1/planRole", "value": "pivot-analysis"}], "J-LEDGER-PLAN"),
        case("ledger-envelope-run-from-pivot-step", "audit-with-pivot", [{"op": "set", "path": "/invocationLedger/steps/1/analysisRunId", "value": "run3:" + h("pivot-run")},
                                                                         {"op": "set", "path": "/invocationLedger/steps/0/analysisRunId", "value": m["run"]}], "J-LEDGER-RUN"),
        case("ledger-analyze-planned-import-step", "analyze-ephemeral-local-links", [{"op": "x-plan-import-step"}], "J-LEDGER-PLAN"),
        case("ledger-default-ephemeral-without-flag", "default-run", [{"op": "set", "path": "/invocationLedger/mode/ephemeral", "value": True}], "J-LEDGER-MODE"),
        case("ledger-render-recorded", A, [{"op": "x-ledger-record-render"}], "J-LEDGER-RENDER"),
        case("ledger-missing-child-hidden", A, [{"op": "set", "path": "/invocationLedger/missingChildren", "value": []}], "J-LEDGER-MISSING"),
        case("ledger-duplicate-execution-id", A, [{"op": "x-ledger-duplicate-execution"}], "J-LEDGER-ATTEMPTS"),
        case("ledger-run-not-produced", A, [{"op": "set", "path": "/invocationLedger/steps/0/analysisRunId", "value": other}], "J-LEDGER-RUN"),
        case("ledger-ephemeral-mode-mismatch", "analyze-ephemeral-local-links", [{"op": "set", "path": "/invocationLedger/mode/ephemeral", "value": False}], "J-LEDGER-MODE"),
        case("ledger-aggregate-mismatch", A, [{"op": "set", "path": "/invocationLedger/steps/1/termination", "value": {"class": "indeterminate", "reasonCodes": ["VERDICT.INDETERMINATE"]}}], "J-LEDGER-AGGREGATE"),
        case("ledger-renderer-failure-without-render-record", "fit-after-commit-query-failure", [{"op": "x-delivery-termination"}], "J-LEDGER-AGGREGATE"),
        case("review-D1-renderer-failure-over-query-refusal-in-delivered-report", "fit-after-commit-query-refused", [{"op": "x-delivery-termination"}], "J-LEDGER-AGGREGATE"),
        case("query-refusal-rewritten-in-ledger", "fit-after-commit-query-refused", [{"op": "set", "path": "/invocationLedger/steps/1/termination", "value": M.renderer_failure(m["run"])},
                                                                                   {"op": "set", "path": "/invocationLedger/steps/1/outcome", "value": "failed"},
                                                                                   {"op": "set", "path": "/invocationLedger/steps/1/attempts/0/outcome", "value": "failed"}], "J-LEDGER-AGGREGATE"),
        case("review-D2-interrupted-step-without-cancellation", A, [{"op": "set", "path": "/invocationLedger/steps/1/termination", "value": {"class": "interrupted", "signal": "SIGINT"}},
                                                                    {"op": "set", "path": "/invocationLedger/steps/1/outcome", "value": "cancelled"}], "J-LEDGER-CANCELLATION"),
        case("cancellation-omitted", A, [{"op": "remove", "path": "/invocationLedger/cancellation"}], "SCHEMA"),
        # skipped steps (RPR4-2)
        case("skipped-termination-promoted-to-envelope", "fit-analysis-rejected-query-skipped", [{"op": "set", "path": "/envelope/termination", "value": SKIPPED_TERMINATION}, {"op": "x-refresh"}], "J-LEDGER-AGGREGATE"),
        case("skipped-step-with-attempt", "fit-analysis-rejected-query-skipped", [{"op": "set", "path": "/invocationLedger/steps/1/attempts", "value": [{"executionId": "exec1_" + "8" * 32, "outcome": "rejected"}]}], "J-LEDGER-SKIPPED"),
        case("review-RPR6-2-skipped-termination-fabricated-detail", "fit-analysis-rejected-query-skipped",
             [{"op": "set", "path": "/invocationLedger/steps/1/termination", "value": dict(SKIPPED_TERMINATION, domainDetail={"code": "evidence.purged", "remedy": "fabricated"})}], "J-LEDGER-SKIPPED"),
        case("skipped-termination-other-class", "fit-analysis-rejected-query-skipped",
             [{"op": "set", "path": "/invocationLedger/steps/1/termination", "value": {"class": "operational-failed", "errorCode": "HOST.IO_FAILURE", "faultCause": "host-io"}}], "J-LEDGER-SKIPPED"),
        case("review-RPR6-3-analyze-baseline-ephemeral", "analyze-baseline-run", [{"op": "set", "path": "/invocationLedger/mode/ephemeral", "value": True}], "J-LEDGER-MODE"),
        case("analyze-baseline-labelled-primary", "analyze-baseline-run", [{"op": "set", "path": "/invocationLedger/planVariant", "value": "primary"}], "J-LEDGER-PLAN"),
        case("analyze-baseline-comparison-self-gate-shape", "analyze-baseline-run", [{"op": "set", "path": "/invocationLedger/steps/1/dependsOn", "value": []}], "J-LEDGER-PLAN"),
        case("analyze-optional-export-made-required", "analyze-with-optional-export", [{"op": "set", "path": "/invocationLedger/steps/2/requirement", "value": "required"}], "J-LEDGER-PLAN"),
        case("analyze-comparison-panel-without-baseline-variant", "analyze-with-optional-export", [{"op": "set", "path": "/panels/comparison", "value": {"state": "unavailable", "reason": "evidence-missing"}}], "J-COMPARISON-ID"),
        case("skipped-step-without-skip-reason","fit-analysis-rejected-query-skipped", [{"op": "remove", "path": "/invocationLedger/steps/1/skipReason"}], "SCHEMA"),
        case("skip-reason-on-completed-step", A, [{"op": "set", "path": "/invocationLedger/steps/1/skipReason", "value": "dependency-not-completed"}], "SCHEMA"),
        case("review-RPR4-2-skipped-with-completed-dependency", "fit-sealed", [{"op": "set", "path": "/invocationLedger/steps/1/outcome", "value": "skipped"},
                                                                               {"op": "set", "path": "/invocationLedger/steps/1/skipReason", "value": "dependency-not-completed"},
                                                                               {"op": "set", "path": "/invocationLedger/steps/1/attempts", "value": []},
                                                                               {"op": "set", "path": "/invocationLedger/steps/1/termination", "value": SKIPPED_TERMINATION}], "J-LEDGER-SKIPPED"),
        case("skipped-reason-cancelled-without-cancelled-dependency", "fit-analysis-rejected-query-skipped", [{"op": "set", "path": "/invocationLedger/steps/1/skipReason", "value": "dependency-cancelled"}], "J-LEDGER-SKIPPED"),
        case("skipped-record-erased", "fit-analysis-rejected-query-skipped", [{"op": "set", "path": "/invocationLedger/steps/1/recorded", "value": False}] +
             [{"op": "remove", "path": "/invocationLedger/steps/1/" + k} for k in ("outcome", "skipReason", "attempts", "termination")], "J-LEDGER-MISSING"),
        # RPR5-1: host requirement/dependency relabels that switch the aggregate (reviewer S1 keeps edges, S2 also drops them)
    ] + [case("review-RPR5-1-S1-%s-step%d-relabelled-optional" % (b, s), b, [{"op": "x-relabel-optional", "step": s, "dropEdges": False}], "J-LEDGER-DAG") for b, s in S_TARGETS] + [
        case("review-RPR5-1-S2-%s-step%d-relabelled-optional-edges-dropped" % (b, s), b, [{"op": "x-relabel-optional", "step": s, "dropEdges": True}], "J-LEDGER-PLAN") for b, s in S_TARGETS] + [
        case("audit-skipped-comparison-aggregate-names-comparison", "audit-analysis-rejected-comparison-skipped", [{"op": "set", "path": "/envelope/termination", "value": SKIPPED_TERMINATION}, {"op": "x-refresh"}], "J-LEDGER-AGGREGATE"),
        # interruption carriers inside a report document (RP-OBL-C01): an invented detail is refused; a failure carrier cannot erase the committed Run; an empty
        # list beside a recorded detail is refused; a report is never delivered for a before-settle interruption (J-LEDGER-CANCELLATION cases below)
        case("interrupted-failure-with-invented-detail", "fit-after-commit-query-refused", [{"op": "set", "path": "/envelope/termination", "value": {"class": "interrupted", "signal": "SIGINT"}},
                                                                                           {"op": "set", "path": "/envelope/exitCode", "value": 130},
                                                                                           {"op": "set", "path": "/envelope/errors", "value": [{"code": "evidence.purged", "remedy": "re-run", "subject": m["run"]}]}], "J-ENV-INTERRUPTION-DETAIL"),
        case("interrupted-failure-carrier-erases-committed-run", "fit-after-commit-query-refused", [{"op": "set", "path": "/envelope/termination", "value": {"class": "interrupted", "signal": "SIGINT"}},
                                                                                                   {"op": "set", "path": "/envelope/exitCode", "value": 130}], "J-ENV-INTERRUPTION-RUN-CARRIER"),
        case("interrupted-failure-empty-errors-with-recorded-detail", "fit-after-commit-query-refused", [{"op": "set", "path": "/envelope/termination", "value": {"class": "interrupted", "signal": "SIGINT"}},
                                                                                                        {"op": "set", "path": "/envelope/exitCode", "value": 130}, {"op": "set", "path": "/envelope/errors", "value": []}], "J-ENV-INTERRUPTION-DETAIL"),
        case("cancellation-requested-phase-none", A, [{"op": "set", "path": "/invocationLedger/cancellation", "value": {"requested": True, "signal": "SIGINT", "phase": "none"}}], "J-LEDGER-CANCELLATION"),
        case("cancellation-before-settle-report-not-deliverable", A, [{"op": "x-cancel-before-settle"}], "J-LEDGER-CANCELLATION"),
        case("cancellation-after-settle-claimed-during-render", "default-run", [{"op": "set", "path": "/invocationLedger/cancellation", "value": {"requested": True, "signal": "SIGTERM", "phase": "after-settle"}}], "J-LEDGER-CANCELLATION"),
        case("cancellation-exit-code-not-130", A, [{"op": "x-cancel-before-settle"}, {"op": "set", "path": "/envelope/exitCode", "value": 4}], "J-ENV-EXIT"),
        # mandatory root bounds (reviewer B1 and maximal legal step terminations; no performance claim)
        case("review-B1-control-one-pinned-step", "audit-with-pivot", [{"op": "x-pinned-failure", "bigSteps": 1, "stepPins": "envelope-max", "char": "\U0001F600"}], "accept"),
        case("review-B1-three-pinned-steps-envelope-boundary", "audit-with-pivot", [{"op": "x-pinned-failure", "bigSteps": 3, "stepPins": "envelope-max", "char": "\U0001F600"}], "accept"),
        case("maximal-legal-step-terminations-audit-failure", "audit-with-pivot", [{"op": "x-pinned-failure", "bigSteps": 3, "stepPins": "max-legal", "char": "\x01"}], "accept"),
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
        case("review-RPR4-1-G4-produced-cap-total-forged-sliced", A, [{"op": "x-graph-relabel", "variant": "review04-G4"}], "J-GRAPH-COUNT"),
        case("review-RPR4-1-G5-visited-cap-produced-exceeds-total", A, [{"op": "x-graph-relabel", "variant": "review04-G5"}], "J-GRAPH-COUNT"),
        case("review-RPR4-1-G6-complete-exact-produced-exceeds-total", A, [{"op": "x-graph-relabel", "variant": "review04-G6"}], "J-GRAPH-COUNT"),
        case("graph-total-equals-produced-but-understates-page-set", A, [{"op": "x-graph-relabel", "variant": "produced-equals-total-sliced-no-cursor"}], "J-GRAPH-COUNT"),
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
        case("descriptor-not-retained-count-hidden", A, [{"op": "x-not-retained-replan", "subject": "pkg"}, {"op": "x-disclosure", "key": "graphDescriptorNotRetainedSubjectsHostAsserted", "value": 1}], "J-DISCLOSURES"),
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


S_TARGETS = [("default-degraded", 0), ("fit-after-commit-query-failure", 1), ("fit-after-commit-query-refused", 1), ("fit-analysis-rejected-query-skipped", 0),
             ("audit-analysis-rejected-comparison-skipped", 0), ("review-brief-failure", 0)]


def interruption_join_cases(bases, m):
    """RPR5-3: an interruption failure's errors must equal the exact in-step-order recorded failure details of its ledger."""
    fitskip = bases["fit-analysis-rejected-query-skipped"]
    steps = [s for s in fitskip["invocationLedger"]["steps"] if s["recorded"]] + [
        {"stepId": 2, "kind": "render", "requirement": "required", "recorded": True, "outcome": "cancelled", "attempts": [], "termination": {"class": "interrupted", "signal": "SIGINT"}}]
    real = M.recorded_failure_details(steps)
    env = dict(copy.deepcopy(fitskip["envelope"]), termination={"class": "interrupted", "signal": "SIGINT"}, exitCode=130, errors=real, availability=copy.deepcopy(AVAILABILITY))
    two = [{"stepId": 0, "kind": "analysis", "requirement": "required", "recorded": True, "outcome": "rejected",
            "termination": {"class": "request-rejected", "errorCode": "REQUEST.PRECONDITION_FAILED", "domainDetail": {"code": "CONFIG.INVALID", "remedy": "admit the baseline pivot closure", "subject": "pivot"}}},
           {"stepId": 1, "kind": "analysis", "requirement": "required", "recorded": True, "outcome": "failed",
            "termination": {"class": "operational-failed", "errorCode": "HOST.IO_FAILURE", "faultCause": "host-io", "domainDetail": {"code": "evidence.purged", "remedy": "re-run the analysis", "subject": "primary"}}},
           {"stepId": 2, "kind": "comparison", "requirement": "required", "recorded": True, "outcome": "skipped", "skipReason": "dependency-not-completed", "termination": SKIPPED_TERMINATION},
           {"stepId": 3, "kind": "render", "requirement": "required", "recorded": True, "outcome": "cancelled", "termination": {"class": "interrupted", "signal": "SIGINT"}}]
    env_two = dict(copy.deepcopy(env), errors=M.recorded_failure_details(two))
    fake = {"code": "evidence.purged", "remedy": "fabricated on a non-failure step"}
    fabricated_skip = [dict(s, termination=dict(s["termination"], domainDetail=fake)) if s.get("outcome") == "skipped" else s for s in steps]
    cancelled_with_detail = [dict(s, termination={"class": "request-rejected", "errorCode": "REQUEST.PRECONDITION_FAILED", "domainDetail": fake}) if s.get("outcome") == "cancelled" else s for s in steps]
    run_env = dict(copy.deepcopy(bases["audit-with-pivot"]["envelope"]), termination={"class": "interrupted", "signal": "SIGINT", "runId": m["run"]}, exitCode=130)
    run_env.pop("errors", None)
    primary = {"stepId": 1, "kind": "analysis", "requirement": "required", "recorded": True, "outcome": "completed", "termination": {"class": "success", "runId": m["run"]}, "analysisRunId": m["run"]}
    run_steps_none = [dict(primary, stepId=0),
                      {"stepId": 1, "kind": "comparison", "requirement": "required", "recorded": True, "outcome": "cancelled", "termination": {"class": "interrupted", "signal": "SIGINT"}},
                      {"stepId": 2, "kind": "render", "requirement": "required", "recorded": True, "outcome": "cancelled", "termination": {"class": "interrupted", "signal": "SIGINT"}}]
    run_steps_pivot = [two[0], primary, dict(two[2]), dict(two[3])]
    pivot_details = M.recorded_failure_details(run_steps_pivot)
    def case(cid, command, envelope, ledger_steps, ops, expect):
        return {"id": cid, "command": command, "envelope": envelope, "steps": ledger_steps, "ops": ops, "expect": expect}
    return [
        case("interruption-real-recorded-detail", "fit", env, steps, [], "accept"),
        case("interruption-real-detail-remedy-changed", "fit", env, steps, [{"op": "set", "path": "/errors/0/remedy", "value": "changed"}], "J-ENV-INTERRUPTION-DETAIL"),
        case("interruption-unrecorded-detail", "fit", env, steps, [{"op": "set", "path": "/errors", "value": [{"code": "evidence.purged", "remedy": "re-run", "subject": m["run"]}]}], "J-ENV-INTERRUPTION-DETAIL"),
        case("interruption-real-detail-plus-invented", "fit", env, steps, [{"op": "set", "path": "/errors", "value": real + [{"code": "evidence.purged", "remedy": "re-run"}]}], "J-ENV-INTERRUPTION-DETAIL"),
        case("interruption-two-real-details-in-step-order", "audit", env_two, two, [], "accept"),
        case("interruption-two-real-details-reordered", "audit", env_two, two, [{"op": "set", "path": "/errors", "value": list(reversed(M.recorded_failure_details(two)))}], "J-ENV-INTERRUPTION-DETAIL"),
        case("interruption-without-ledger-join", "fit", env, None, [], "J-ENV-INTERRUPTION-DETAIL"),
        case("interruption-skipped-termination-is-not-a-detail", "fit", env, [dict(s, termination=dict(s["termination"], domainDetail={"code": "CONFIG.INVALID", "remedy": "x"})) if s.get("outcome") == "skipped" else s for s in steps],
             [], "J-ENV-INTERRUPTION-DETAIL"),
        # envelope6 (interruption unit): the empty failure form with no recorded detail and no committed Run; availability stays required by parity
        case("interruption-empty-errors-no-recorded-detail", "fit", dict(copy.deepcopy(env), errors=[]), [steps[-1]], [], "accept"),
        case("interruption-empty-errors-envelope-major-5", "fit", dict(copy.deepcopy(env), errors=[]), [steps[-1]], [{"op": "set", "path": "/schemaMajor", "value": 5}], "SCHEMA-ENV"),
        case("interruption-empty-errors-with-recorded-detail", "fit", dict(copy.deepcopy(env), errors=[]), steps, [], "J-ENV-INTERRUPTION-DETAIL"),
        case("interruption-failure-availability-omitted", "fit", dict(copy.deepcopy(env), errors=[]), [steps[-1]], [{"op": "remove", "path": "/availability"}], "J-ENV-CAPABILITY-AVAILABILITY"),
        case("interruption-query-command-no-availability", "candidates", {k: v for k, v in copy.deepcopy(env).items() if k != "availability"} | {"errors": []}, [steps[-1]], [], "accept"),
        case("interruption-failure-carrier-erases-committed-run", "audit", M.failure_envelope(run_env, {"class": "interrupted", "signal": "SIGINT"}, run_steps_none), run_steps_none, [],
             "J-ENV-INTERRUPTION-RUN-CARRIER"),
        case("interruption-run-carrier-names-other-run", "audit", run_env, run_steps_none, [{"op": "set", "path": "/termination/runId", "value": "run3:" + h("other")},
                                                                                         {"op": "set", "path": "/run/runId", "value": "run3:" + h("other")}], "J-ENV-INTERRUPTION-RUN-CARRIER"),
        # RPR6-2: skipped and cancelled steps never contribute; a fabricated skip termination is refused outright
        case("review-RPR6-2-fabricated-skipped-detail-carried", "fit", dict(copy.deepcopy(env), errors=real + [fake]), fabricated_skip, [], "J-ENV-INTERRUPTION-DETAIL"),
        case("fabricated-skipped-detail-not-carried", "fit", env, fabricated_skip, [], "J-ENV-INTERRUPTION-DETAIL"),
        case("cancelled-step-detail-not-carried", "fit", env, cancelled_with_detail, [], "accept"),
        case("cancelled-step-detail-carried", "fit", dict(copy.deepcopy(env), errors=real + [fake]), cancelled_with_detail, [], "J-ENV-INTERRUPTION-DETAIL"),
        # selected deterministic rule on the run carrier: nonempty recorded list carried exactly, empty list omits errors
        case("run-carrier-no-recorded-detail-errors-absent", "audit", run_env, run_steps_none, [], "accept"),
        case("run-carrier-no-recorded-detail-empty-errors", "audit", dict(copy.deepcopy(run_env), errors=[]), run_steps_none, [], "SCHEMA-ENV"),
        case("run-carrier-real-recorded-detail", "audit", dict(copy.deepcopy(run_env), errors=pivot_details), run_steps_pivot, [], "accept"),
        case("run-carrier-real-recorded-detail-omitted", "audit", run_env, run_steps_pivot, [], "J-ENV-INTERRUPTION-DETAIL"),
        case("run-carrier-invented-detail", "audit", dict(copy.deepcopy(run_env), errors=[fake]), run_steps_none, [], "J-ENV-INTERRUPTION-DETAIL"),
    ]


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
        case("json-fit-major-5", "fit", sealed, [{"op": "set", "path": "/schemaMajor", "value": 5}], "SCHEMA-ENV"),
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
    "RP-OBL-G01": "M1 generation registry: register envelope5 with its envelope6 successor, inventory5 and report-projection:1 source bytes; generator compatibility was not run by this author (review A9 stays open).",
    "RP-OBL-C01": "Envelope owner: the pre-Run interruption form is implemented in this candidate over command-envelope:6 and the conditionally accepted interruption unit (owner/interruption-binding.v1.json, fixtures.json#/interruptionGoldens executed through validate_interruption_delivery/validate_preplanning_delivery); it stays an M1 blocker until joint independent review with envelope5 and root source selection.",
    "RP-OBL-L02": "Capacity/admission owner: a schema-valid required availability account can exceed the 4 MiB envelope codec; no truncation, empty account or invented interrupted/130 versus required-delivery or serialization/4 precedence. Regression in check.py capacity section; open.",
    "RP-OBL-E01": "After acceptance, root rebinds product design lock and emitters to envelope5/inventory5 in new integration records (the metadata-v2 acceptance stays historical) and the workflows reference model admits golden fit-ephemeral-non-authoritative.",
}

REVIEW_MAP = {
    "RPR3-1/G1": "review-G1-complete-lower-bound-sliced", "RPR3-1/G1-truncated-page": "review-G1-truncated-page-lower-bound-sliced",
    "RPR3-1/G2": "review-G2-truncated-bound-sliced-without-cap", "RPR3-1/G3": "review-G3-complete-exact-sliced",
    "RPR3-2/B1": "review-B1-three-pinned-steps-envelope-boundary", "RPR3-2/B1-control": "review-B1-control-one-pinned-step", "RPR3-2/maximal-legal": "maximal-legal-step-terminations-audit-failure",
    "RPR3-3/D1-document": "review-D1-renderer-failure-over-query-refusal-in-delivered-report", "RPR3-3/D2": "review-D2-interrupted-step-without-cancellation",
    "A1/S1": "review-S1-descriptor-not-retained-replan", "A1/S1-uncontradicted": "review-A1-descriptor-not-retained-uncontradicted-steering-disclosed",
    "A2/H1": "review-H1-snapshot-count-understated-host-asserted-disclosed",
    "RPR6-2/fabricated-skipped-detail-envelope": "review-RPR6-2-fabricated-skipped-detail-carried",
    "RPR6-2/fabricated-skipped-termination-ledger": "review-RPR6-2-skipped-termination-fabricated-detail",
    "RPR6-3/analyze-baseline-positive": "positive-analyze-baseline-run", "RPR6-3/analyze-export-positive": "positive-analyze-with-optional-export",
    "RPR6-3/analyze-baseline-ephemeral": "review-RPR6-3-analyze-baseline-ephemeral",
    "RPR5-1/S1-default-degraded":"review-RPR5-1-S1-default-degraded-step0-relabelled-optional",
    "RPR5-1/S1-review-brief-failure": "review-RPR5-1-S1-review-brief-failure-step0-relabelled-optional",
    "RPR5-1/S2-fit-after-commit-query-refused": "review-RPR5-1-S2-fit-after-commit-query-refused-step1-relabelled-optional-edges-dropped",
    "RPR5-1/S2-audit-analysis-rejected": "review-RPR5-1-S2-audit-analysis-rejected-comparison-skipped-step0-relabelled-optional-edges-dropped",
    "RPR5-3/I1-real-recorded-detail": "interruption-real-recorded-detail", "RPR5-3/two-real-details": "interruption-two-real-details-in-step-order",
    "RPR5-3/invented-detail": "interruption-unrecorded-detail", "RPR5-3/reordered": "interruption-two-real-details-reordered",
    "RPR4-1/G4":"review-RPR4-1-G4-produced-cap-total-forged-sliced", "RPR4-1/G5": "review-RPR4-1-G5-visited-cap-produced-exceeds-total",
    "RPR4-1/G6": "review-RPR4-1-G6-complete-exact-produced-exceeds-total", "RPR4-2/skipped-with-completed-dependency": "review-RPR4-2-skipped-with-completed-dependency",
    "RPR4-2/skipped-promoted": "skipped-termination-promoted-to-envelope", "RPR4-3/invented-detail": "interrupted-failure-with-invented-detail",
    "C01/pre-run-empty-errors-envelope6": "interruption-empty-errors-no-recorded-detail", "C01/empty-errors-under-envelope5-major": "interruption-empty-errors-envelope-major-5",
    "C01/failure-carrier-erases-committed-run": "interruption-failure-carrier-erases-committed-run", "C01/availability-omitted": "interruption-failure-availability-omitted",
    "prior/Q1": "review-Q1-fit-truncated-short-page", "prior/S2": "review-S2-slot-items-sliced", "prior/Q7b": "review-Q7b-iterative-depth-200000",
}


if __name__ == "__main__":
    (HERE / "fixtures.json").write_bytes(json.dumps(build(), indent=1, ensure_ascii=False).encode("utf-8") + b"\n")
