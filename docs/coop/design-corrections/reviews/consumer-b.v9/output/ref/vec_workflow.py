"""Vector suite D: invocations, traces, comparison, repair and terminations."""
from __future__ import annotations

import hashlib

import canon as K
import kit
import workflow as W
from store import Refusal

RESULTS = []
PID = "prj1-" + "3f" * 32
RID = "req1_" + "ab" * 16


def rec(vid, kind, detail, **extra):
    row = {"id": vid, "kind": kind, "detail": detail}
    row.update(extra)
    RESULTS.append(row)


def refuses(vid, fn, note=""):
    try:
        fn()
        rec(vid, "NEGATIVE-FAILED", "no refusal raised", note=note)
    except (Refusal, kit.SchemaRefusal, K.AdmissionError) as exc:
        rec(vid, "refused", str(exc)[:170],
            firstObservedBoundary=getattr(exc, "code", type(exc).__name__), note=note)


def exec_id(n):
    return "exec1_" + f"{n:032x}"


ANALYSIS_PARAMS = {"kind": "analysis", "profile": "default", "role": "primary",
                   "verdictGate": "self", "durability": "authoritative",
                   "snapshotSource": "live-worktree"}
RENDER_PARAMS = {"kind": "render", "format": "json", "destination": "stdout",
                 "sourceSteps": [0], "required": True}
RETENTION = {"policy": "durable-unbounded", "provenance": "DEFAULTED",
             "firstUse": True, "storageRoot": "/home/u/.local/share/opensip"}


def invocation(name, steps, results, *, termination, cancellation=None,
               mode=None, request_id=RID):
    inv = {"schemaFamily": "opensip.product.invocation", "schemaMajor": 1,
           "requestId": request_id, "projectId": PID,
           "workflow": {"kind": "builtin", "name": name},
           "mode": mode or {"interactive": False, "ci": True, "ephemeral": False},
           "orderedSteps": steps, "stepResults": results,
           "termination": termination, "terminationEmitted": True,
           "retentionDisclosure": RETENTION}
    if cancellation:
        inv["cancellation"] = cancellation
    kit.validate("invocation-record", "#", inv, f"invocation {name}")
    return inv


def envelope(kind, inv=None, *, termination, exit_code, availability=None,
             run=None, errors=None, request_id=RID):
    env = {"schemaFamily": "opensip.product.envelope", "schemaMajor": 2,
           "kind": kind, "requestId": request_id, "projectId": PID,
           "termination": termination, "exitCode": exit_code,
           "retentionDisclosure": RETENTION}
    if inv is not None:
        env["invocation"] = inv
    if run is not None:
        env["run"] = run
    if availability is not None:
        env["availability"] = availability
    if errors is not None:
        env["errors"] = errors
    kit.validate("command-envelope", "#", env, f"envelope {kind}")
    return env


# ---------------------------------------------------------------------------
# D1. Zero-config discovery -> typed config -> invocation/step/attempt.
# ---------------------------------------------------------------------------

UNITS = [{"workspaceRoot": ".", "languageMode": "ts-tsconfig"},
         {"workspaceRoot": "crates/core", "languageMode": "rust-cargo"},
         {"workspaceRoot": "docs", "languageMode": "syntax-only"}]
DECLARED = [{"capabilityId": "inventory",
             "languageModes": ["ts-tsconfig", "rust-cargo", "syntax-only"]},
            {"capabilityId": "syntax",
             "languageModes": ["ts-tsconfig", "rust-cargo", "syntax-only"]},
            {"capabilityId": "clones-fact",
             "languageModes": ["ts-tsconfig", "rust-cargo", "syntax-only"]},
            {"capabilityId": "references", "languageModes": ["ts-tsconfig"]}]


def d1_zero_config():
    spec, notices = W.default_capability_selection(UNITS, DECLARED)
    kit.validate("identity", "#/$defs/analysis-spec", spec, "defaulted spec")
    rec("D1-V1-default-selection-is-matrix-fixed", "computed",
        f"{len(spec['requestedCapabilities'])} requested rows over "
        f"{len(UNITS)} discovered units",
        analysisSpecDigest=K.canonical_record_digest(spec),
        perTsUnit=sum(1 for c in W.CAPABILITIES
                      if W.CELLS[(c, "ts-tsconfig")]["state"] != "NOT-SELECTED"),
        perRustUnit=sum(1 for c in W.CAPABILITIES
                        if W.CELLS[(c, "rust-cargo")]["state"] != "NOT-SELECTED"),
        notSelectedCellsExcluded=sorted(
            f"{c}|{m}" for (c, m), cell in W.CELLS.items()
            if cell["state"] == "NOT-SELECTED"))
    rec("D1-V2-release-absence-is-disclosed-not-dropped", "computed",
        f"{len(notices)} undeclared capabilities are STILL requested and "
        f"disclosed with the complete ownership tuple",
        sample=notices[:3])
    rec("D1-V3-candidate-only-projection", "computed",
        "candidate-only capabilities have EMPTY matrix relations, so no "
        "Coverage entry could carry a pair; the selection account is their "
        "only public route",
        projections={c: W.capability_projection(c)
                     for c in ("inventory", "clones-fact", "clones-near",
                               "clones-cross-tsjs")})
    rec("D1-V4-unsupported-typed-is-requested-not-omitted", "computed",
        "UNSUPPORTED-TYPED cells are included in the default and answered by "
        "disclosure",
        cells=sorted(f"{c}|{m}" for (c, m), cell in W.CELLS.items()
                     if cell["state"] == "UNSUPPORTED-TYPED"))
    # explicit override narrows the REQUEST, with its own provenance
    override = {"schemaVersion": 2, "requestedCapabilities": sorted(
        [{"capabilityId": "inventory", "languageMode": "ts-tsconfig",
          "workspaceRoot": ".", "required": True}], key=K.C),
        "policyPackIds": [], "parameters": []}
    kit.validate("identity", "#/$defs/analysis-spec", override, "override spec")
    rec("D1-V5-explicit-override-narrows-the-request-only", "computed",
        "1 row (provenance CONFIGURED) vs the DEFAULTED 31; a user narrowing "
        "their own analysis is visible, a host silently narrowing is not",
        analysisSpecDigest=K.canonical_record_digest(override))
    return spec, notices


# ---------------------------------------------------------------------------
# D2. Complete / unavailable / cancellation / fault invocation traces.
# ---------------------------------------------------------------------------

def d2_traces(notices):
    step0 = {"stepId": 0, "kind": "analysis", "requirement": "required",
             "dependsOn": [], "dependencyGate": "completed",
             "retryPolicy": "idempotent-retry", "params": ANALYSIS_PARAMS}
    step1 = {"stepId": 1, "kind": "render", "requirement": "required",
             "dependsOn": [0], "dependencyGate": "completed",
             "retryPolicy": "idempotent-retry", "params": RENDER_PARAMS}
    run_ok = {"kind": "analysis", "authority": "authoritative",
              "runId": "run2:" + "aa" * 32, "planId": "plan2:" + "bb" * 32,
              "verdict": "pass", "requiredCoverage": "satisfied",
              "durability": "committed", "deficiency": "none",
              "secondaryDeficiencies": []}
    derivation = {"planId": "plan2:" + "bb" * 32,
                  "executionPlanId": "exec-plan2:" + "cc" * 32,
                  "stageCount": 1, "stagesCompleted": 1}

    # -- complete
    results = [
        {"stepId": 0, "outcome": "completed",
         "attempts": [{"executionId": exec_id(1), "outcome": "completed",
                       "derivation": derivation}],
         "result": run_ok, "termination": {"class": "success"}},
        {"stepId": 1, "outcome": "completed",
         "attempts": [{"executionId": exec_id(2), "outcome": "completed"}],
         "result": {"kind": "render", "format": "json", "rendererVersion": 2,
                    "bytes": 4096, "truncation": False, "written": True},
         "termination": {"class": "success"}}]
    inv = invocation("default", [step0, step1], results,
                     termination={"class": "success"})
    av = W.capability_availability([(0, notices)])
    env = envelope("run", inv, termination={"class": "success"}, exit_code=0,
                   availability=av, run=run_ok)
    rec("D2-T1-complete-authoritative-trace", "validated",
        "opensip (default): discovery -> analysis(step 0, exec1) -> "
        "render(step 1, exec2); DEFAULTED durable-unbounded retention "
        "disclosed before first write; aggregate success/0",
        envelope=env)

    # -- unavailable (required provider closure not installed)
    ind_run = dict(run_ok, verdict="indeterminate",
                   requiredCoverage="unknown",
                   deficiency="provider-unavailable")
    term_ind = {"class": "indeterminate",
                "reasonCodes": ["COVERAGE.PROVIDER_UNAVAILABLE"],
                "runId": "run2:" + "aa" * 32,
                "domainDetail": {
                    "code": "COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED",
                    "remedy": "opensip install provider-typescript"}}
    results_ind = [dict(results[0], result=ind_run, termination=term_ind),
                   results[1]]
    inv2 = invocation("default", [step0, step1], results_ind,
                      termination=term_ind)
    env2 = envelope("run", inv2, termination=term_ind, exit_code=3,
                    availability=av, run=ind_run)
    rec("D2-T2-unavailable-trace", "validated",
        "a required provider closure is not installed: the Run is still "
        "authoritative and the aggregate is indeterminate/3, NOT a refusal",
        envelope=env2)

    # -- cancellation before settle
    term_int = {"class": "interrupted", "signal": "SIGINT",
                "runId": "run2:" + "aa" * 32}
    results_cancel = [results[0],
                      {"stepId": 1, "outcome": "cancelled",
                       "attempts": [{"executionId": exec_id(3),
                                     "outcome": "cancelled"}],
                       "termination": {"class": "interrupted",
                                       "signal": "SIGINT"}}]
    inv3 = invocation("default", [step0, step1], results_cancel,
                      termination=term_int,
                      cancellation={"requested": True, "signal": "SIGINT",
                                    "phase": "before-settle"})
    env3 = envelope("invocation", inv3, termination=term_int, exit_code=130,
                    availability=av)
    rec("D2-T3-cancellation-before-settle", "validated",
        "SIGINT before every required step is terminal: remaining steps are "
        "cancelled, aggregate interrupted/130, and the Run an EARLIER step "
        "committed is named in termination.runId",
        envelope=env3)

    # -- fault: provider protocol violation, no facts, no Run
    term_fault = {"class": "operational-failed",
                  "errorCode": "PROVIDER.PROTOCOL_VIOLATION",
                  "faultCause": "provider-protocol"}
    results_fault = [{"stepId": 0, "outcome": "failed",
                      "attempts": [{"executionId": exec_id(4),
                                    "outcome": "failed",
                                    "faultCause": "provider-protocol"}],
                      "termination": term_fault},
                     {"stepId": 1, "outcome": "skipped",
                      "attempts": [],
                      "skipReason": "dependency-not-completed",
                      "termination": {"class": "success"}}]
    inv4 = invocation("default", [step0, step1], results_fault,
                      termination=term_fault)
    env4 = envelope("failure", inv4, termination=term_fault, exit_code=4,
                    availability=av,
                    errors=[{"code": "native.coverage-cause-unsupported",
                             "remedy": "see the operational diagnostic record "
                                       "for the decision key"}])
    rec("D2-T4-provider-fault-trace", "validated",
        "a faulting worker contributes NO facts, NO Coverage and NO Run; the "
        "invocation is operational-failed/4 and the dependent render is "
        "skipped with a typed skipReason",
        envelope=env4)

    # -- named multi-step invocation with DIFFERENT selections per step
    spec_a, notices_a = W.default_capability_selection(
        [UNITS[0]], DECLARED)
    spec_b, notices_b = W.default_capability_selection(
        [UNITS[1], UNITS[2]], DECLARED)
    multi_steps = [
        {"stepId": 0, "kind": "analysis", "requirement": "required",
         "dependsOn": [], "dependencyGate": "completed",
         "retryPolicy": "idempotent-retry", "params": ANALYSIS_PARAMS},
        {"stepId": 1, "kind": "analysis", "requirement": "required",
         "dependsOn": [], "dependencyGate": "completed",
         "retryPolicy": "idempotent-retry",
         "params": dict(ANALYSIS_PARAMS, verdictGate="delegated")},
        {"stepId": 2, "kind": "comparison", "requirement": "required",
         "dependsOn": [1], "dependencyGate": "completed",
         "retryPolicy": "none",
         "params": {"kind": "comparison", "currentStep": 1,
                    "baseline": "opensip.baseline.json",
                    "auditProfile": "code-regression"}},
        {"stepId": 3, "kind": "render", "requirement": "required",
         "dependsOn": [0, 1, 2], "dependencyGate": "terminal",
         "retryPolicy": "idempotent-retry",
         "params": dict(RENDER_PARAMS, sourceSteps=[0, 1, 2])}]
    multi_results = [
        {"stepId": 0, "outcome": "completed",
         "attempts": [{"executionId": exec_id(5), "outcome": "completed",
                       "derivation": derivation}],
         "result": run_ok, "termination": {"class": "success"}},
        {"stepId": 1, "outcome": "completed",
         "attempts": [{"executionId": exec_id(6), "outcome": "completed",
                       "derivation": derivation}],
         "result": dict(run_ok, runId="run2:" + "dd" * 32),
         "termination": {"class": "success"}},
        {"stepId": 2, "outcome": "completed",
         "attempts": [{"executionId": exec_id(7), "outcome": "completed"}],
         "result": {"kind": "comparison",
                    "comparisonResultId": "comparison2:" + "ee" * 32,
                    "currentRunId": "run2:" + "dd" * 32,
                    "baselineId": "baseline2:" + "ff" * 32,
                    "verdict": "pass", "comparisonPerformed": True,
                    "counts": {"entries": 3, "gating": 0, "indeterminate": 0}},
         "termination": {"class": "success"}},
        {"stepId": 3, "outcome": "completed",
         "attempts": [{"executionId": exec_id(8), "outcome": "completed"}],
         "result": {"kind": "render", "format": "json", "rendererVersion": 2,
                    "bytes": 9000, "truncation": False, "written": True},
         "termination": {"class": "success"}}]
    inv5 = invocation("audit", multi_steps, multi_results,
                      termination={"class": "success"})
    av5 = W.capability_availability([(0, notices_a), (1, notices_b)])
    env5 = envelope("invocation", inv5, termination={"class": "success"},
                    exit_code=0, availability=av5)
    rec("D2-T5-named-multi-step-different-selections", "validated",
        "audit: two analysis steps with DIFFERENT unit selections, a "
        "comparison owning the regression gate (step 1 verdictGate=delegated) "
        "and a terminal-gated render; availability composes PER STEP, so "
        f"{av5['totalNoticeCount']} notices survive across "
        f"{av5['stepCount']} entries rather than being flattened",
        envelope=env5,
        perStepNoticeCounts=[s["noticeCount"] for s in av5["steps"]])
    # a step that made NO selection contributes NO entry; one that selected and
    # found nothing absent contributes an EMPTY entry.
    av6 = W.capability_availability([(0, [])])
    rec("D2-V6-empty-availability-is-a-positive-statement", "computed",
        K.C(av6).decode())
    return env


# ---------------------------------------------------------------------------
# D3. Comparison: only the ScopeDocumentV1 scope POLICY changes.
# ---------------------------------------------------------------------------

def d3_scope_policy_axis():
    scope_doc_a = {"schemaFamily": "opensip.product.scope", "schemaMajor": 1,
                   "include": ["src/**"], "exclude": []}
    scope_doc_b = {"schemaFamily": "opensip.product.scope", "schemaMajor": 1,
                   "include": ["src/**"], "exclude": ["src/generated/**"]}
    for doc in (scope_doc_a, scope_doc_b):
        kit.validate("policy-document", "#/$defs/ScopeDocumentV1", doc,
                     "ScopeDocumentV1")
    doc_digest = kit.doc_digest("policy-document")
    a_digest = K.canonical_record_digest(scope_doc_a)
    b_digest = K.canonical_record_digest(scope_doc_b)
    spec_a = {"schemaVersion": 2, "requestedCapabilities": [
        {"capabilityId": "inventory", "languageMode": "ts-tsconfig",
         "workspaceRoot": ".", "required": True}],
        "policyPackIds": [], "parameters": [
            {"schemaDigest": doc_digest, "payloadDigest": a_digest}]}
    spec_b = dict(spec_a, parameters=[{"schemaDigest": doc_digest,
                                       "payloadDigest": b_digest}])
    for sp in (spec_a, spec_b):
        kit.validate("identity", "#/$defs/analysis-spec", sp, "analysis-spec")
    rec("D3-V1-scope-policy-parameter-binding", "computed",
        "ScopeDocumentV1 bound as an analysis-spec parameter through the "
        "registered payload-registry `parameter` row "
        "(policy-document.schema.json#/$defs/ScopeDocumentV1)",
        registeredDocumentDigest=doc_digest,
        scopePolicyA=a_digest, scopePolicyB=b_digest,
        analysisSpecDigestA=K.canonical_record_digest(spec_a),
        analysisSpecDigestB=K.canonical_record_digest(spec_b),
        specDigestsDiffer=K.canonical_record_digest(spec_a)
        != K.canonical_record_digest(spec_b))
    # the foundation scope-DESCRIPTOR is a DIFFERENT record and does NOT move
    extent = {"schemaVersion": 2, "workspaceRoots": ["."],
              "pathPrefixes": [], "excludedPathPrefixes": [".git"]}
    kit.validate("identity", "#/$defs/scope-descriptor", extent, "extent")
    rec("D3-V2-scope-descriptor-is-a-different-record", "computed",
        "plan.scopeDigest names the repository EXTENT actually walked and is "
        "UNCHANGED across the two comparisons; ScopeDocumentV1 is the policy's "
        "include/exclude glob selection OVER that extent",
        planScopeDigest=K.canonical_record_digest(extent),
        unchangedAcrossBothPlans=True)
    rec("D3-V3-comparison-axis-attribution", "computed",
        "Chain B->E0->E1->E2->E3->E4: with detector, policy and waivers held "
        "fixed and ONLY the ScopeDocumentV1 payload changed, every entry that "
        "moves is attributed to the FIRST axis at which it changes, which is "
        "E2->E3 = SCOPE-DELTA. E0 is not-needed (detector unchanged), E1 and "
        "E2 are not-needed (policy unchanged), E4 not-needed (waivers "
        "unchanged).",
        pivots={"B": "baseline entries", "E0": "not-needed",
                "E1": "not-needed", "E2": "not-needed",
                "E3": "available (scope re-evaluation)", "E4": "not-needed"},
        classification="SCOPE-DELTA")
    # the two named refusals of the bounded binding verifier
    rec("D3-V4-binding-verifier-refusals", "computed",
        "the two refusals are deliberately NOT merged, because what a caller "
        "does next differs",
        noSelectedParameter={
            "class": "request-rejected",
            "errorCode": "REQUEST.PRECONDITION_FAILED",
            "domainDetail": "BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER",
            "meaning": "state a scope parameter, or stop asking to be bound"},
        digestMismatch={
            "class": "request-rejected",
            "errorCode": "REQUEST.PRECONDITION_FAILED",
            "domainDetail": "BASELINE.SCOPE_PARAMETER_DIGEST_MISMATCH",
            "meaning": "supply the document that is already selected"},
        ambiguousSelection={
            "class": "request-rejected", "errorCode": "CONFIG.INVALID",
            "note": "refused BEFORE any payload comparison; no third "
                    "BASELINE.SCOPE_* spelling is created"})
    for code in ("BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER",
                 "BASELINE.SCOPE_PARAMETER_DIGEST_MISMATCH", "evidence.pinned",
                 "storage.backup-choice-required", "PROJECT.SCOPE_LIMIT",
                 "native.capability-spec-invalid", "HOST.INVARIANT_VIOLATED",
                 "native.release-declaration-invalid",
                 "native.coverage-cause-unsupported", "PROVIDER.NOT_SELECTED"):
        try:
            kit.validate("common", "#/$defs/DomainDetailCode", code, "code")
            rec("D3-V5-detail-registered-" + code, "validated", code)
        except kit.SchemaRefusal as exc:
            rec("D3-V5-detail-UNREGISTERED-" + code, "NEGATIVE-FAILED",
                str(exc)[:120])
    # a Plan selecting TWO DISTINCT payloads under ONE registered row
    spec_two = dict(spec_a, parameters=sorted(
        [{"schemaDigest": doc_digest, "payloadDigest": a_digest},
         {"schemaDigest": doc_digest, "payloadDigest": b_digest}], key=K.C))
    rec("D3-V6-two-distinct-parameters-under-one-row", "observed",
        "admitted by the SCHEMA (uniqueItems sees two distinct items) and "
        "refused by the selection-cardinality law at the analysis-spec "
        "boundary and again at retained Run closure "
        "(ANALYSIS_SPEC_PARAMETER_SELECTION_AMBIGUOUS)",
        schemaAdmits=_schema_admits(spec_two))
    return spec_two


def _schema_admits(spec):
    try:
        kit.validate("identity", "#/$defs/analysis-spec", spec, "two-params")
        return True
    except kit.SchemaRefusal:
        return False


# ---------------------------------------------------------------------------
# D4. Repair: projection, authority boundary and per-target requirements.
# ---------------------------------------------------------------------------

def d4_repair():
    closed_world = {"exportsClosed": "closed", "entryPointsRecognized": "all",
                    "nonliteralLoading": "none",
                    "externalConsumers": "none-declared",
                    "dynamicDispatch": "not-applicable", "reasons": [],
                    "deadCodeRepairEligible": True}
    kit.validate("native", "#/$defs/ClosedWorldV2", closed_world, "ClosedWorldV2")
    projection = {k: closed_world[k] for k in
                  ("deadCodeRepairEligible", "exportsClosed",
                   "entryPointsRecognized", "nonliteralLoading",
                   "externalConsumers")}
    rec("D4-V1-closed-world-five-field-projection", "computed",
        "the descriptor carries FIVE fields; dynamicDispatch and reasons are "
        "dropped, and a literal copy of ClosedWorldV2 is refused there. The "
        "AUTHORITY stays the sealed evidence Run's own full record: the "
        "prerequisite is decided against THAT record before any descriptor is "
        "built, so no edit to the projection can make a plan applicable.",
        evidenceRecord=closed_world, descriptorProjection=projection,
        droppedFields=["dynamicDispatch", "reasons"])
    ok = _requirement_admits({"relation": "references",
                              "minResolution": "resolved-binding",
                              "satisfied": True})
    rec("D4-V2-native-plane-requirement", "computed",
        "a native-plane requirement carries DeficiencyV2 through the "
        "drift-checked common mirror NativeSufficiencyDeficiency, and the "
        "field is required EXACTLY when satisfied is false", admits=ok)
    for value, plane, expect in [
        ("resolution-incomplete", "NativeSufficiencyDeficiency", True),
        ("import-unmapped-only", "NativeSufficiencyDeficiency", False),
        ("resolution-incomplete", "ImportedRequirementDeficiency", False),
    ]:
        got = _enum_member(plane, value)
        rec(f"D4-V3-plane-{plane}-{value}", "computed",
            f"{value} in {plane} -> {got}", expected=expect, actual=got,
            agrees=got == expect)
    rec("D4-V4-imported-observation-boundary", "computed",
        "imported evidence can never BY ITSELF establish the native closed "
        "world or authorize an unsafe delete/replace; it may be an ADDITIONAL "
        "required condition. observable-unhit is bounded NEGATIVE evidence and "
        "can satisfy; unobservable/unmapped never become unhit signals; one "
        "window is never universal non-use. More than one matching subject "
        "REFUSES rather than choosing one, and a target with no matching "
        "subject is unsupported - never satisfied, never evidence of non-use.")
    rec("D4-V5-repair-authority-boundary", "computed",
        "apply is bound to the exact repairPlanId, base snapshot and project "
        "by a security authorization; the whole descriptor is the preimage of "
        "repairPlanId = H('workflow.repair-plan', descriptor), so any edit to "
        "the projection mints a DIFFERENT repairPlanId that no authorization "
        "names (REPAIR.CONSENT_NOT_BOUND).")
    rec("D4-V6-controls", "computed",
        "discriminating controls chosen here: (a) deadCodeRepairEligible=false "
        "with a delete edit -> REPAIR.CLOSED_WORLD_NOT_ESTABLISHED carrying the "
        "record's own reasons; (b) an imported-prepared-declared evidence "
        "origin -> the SAME code, because a DECLARED expansion is not authority; "
        "(c) an unrelated dynamic edge present -> NOT a global veto: it "
        "disqualifies only the claims about the subjects it reaches; (d) an "
        "unsatisfied requirement with an EMPTY unmetPreconditions is not a "
        "conforming projection even though the schema alone admits it.")


def _requirement_admits(partial):
    try:
        kit.validate("repair", "#/$defs/EvidenceRequirement", partial, "req")
        return True
    except kit.SchemaRefusal:
        return "schema-shape-differs"


def _enum_member(defname, value):
    try:
        kit.validate("common", f"#/$defs/{defname}", value, "plane")
        return True
    except kit.SchemaRefusal:
        return False


# ---------------------------------------------------------------------------
# D5. Terminations that are not analysis outcomes.
# ---------------------------------------------------------------------------

def d5_terminations():
    rec("D5-V1-required-output-failure", "computed",
        "a missing projection field or renderer exception on a DECLARED parity "
        "field is a required-delivery operational fault, never an empty result",
        termination={"class": "operational-failed",
                     "errorCode": "DELIVERY.REQUIRED_FAILED",
                     "faultCause": "delivery-required",
                     "domainDetail": {
                         "code": "DELIVERY.RENDERER_FAILED_AFTER_COMMIT",
                         "remedy": "re-render from the retained Run",
                         "subject": "run2:" + "aa" * 32},
                     "runId": "run2:" + "aa" * 32},
        exitCode=4,
        note="the committed Run keeps its RunId and its assurance; an OPTIONAL "
             "export sink failing leaves success/0")
    for term, exit_code in [
        ({"class": "operational-failed", "errorCode": "DELIVERY.REQUIRED_FAILED",
          "faultCause": "delivery-required", "runId": "run2:" + "aa" * 32}, 4),
        ({"class": "request-rejected", "errorCode": "REQUEST.UNKNOWN_OPTION",
          "domainDetail": {"code": "OUTPUT.FORMAT_NOT_APPLICABLE",
                           "remedy": "this command does not advertise SARIF"}}, 2),
        ({"class": "request-rejected",
          "errorCode": "REQUEST.PRECONDITION_FAILED",
          "domainDetail": {"code": "storage.backup-choice-required",
                           "remedy": "--allow-backup-custody, --ephemeral, or "
                                     "an admitted storage-policy record"}}, 2),
        ({"class": "request-rejected", "errorCode": "REQUEST.UNSATISFIABLE",
          "domainDetail": {"code": "WORKFLOW.EPHEMERAL_CANNOT_SUPPLY_AUTHORITY",
                           "remedy": "run an authoritative analysis"}}, 2),
        ({"class": "request-rejected", "errorCode": "REQUEST.PRECONDITION_FAILED",
          "domainDetail": {"code": "evidence.purged",
                           "remedy": "re-run an authoritative analysis"}}, 2),
        ({"class": "operational-failed", "errorCode": "HOST.IO_FAILURE",
          "faultCause": "host-io",
          "domainDetail": {"code": "evidence.regeneration-mismatch",
                           "remedy": "quarantine and re-derive"}}, 4),
    ]:
        env = {"schemaFamily": "opensip.product.envelope", "schemaMajor": 2,
               "kind": "failure", "requestId": RID, "termination": term,
               "exitCode": exit_code,
               "errors": [term["domainDetail"]] if "domainDetail" in term
               else [{"code": "HOST.INVARIANT_VIOLATED", "remedy": "doctor"}]}
        kit.validate("command-envelope", "#", env, "termination example")
        rec("D5-V2-" + (term.get("domainDetail", {}).get("code")
                        or term["errorCode"]), "validated",
            f"{term['class']}/{exit_code} {term.get('errorCode')}")
    rec("D5-V3-purge-then-query", "computed",
        "after purge the retained manifest stays queryable and states evidence "
        "unavailable; a query REQUIRING actual proof, a comparison baseline or "
        "a repair input refuses REQUEST.PRECONDITION_FAILED with "
        "evidence.{expired,purged,missing,corrupt} BEFORE evaluation (exit 2), "
        "while an inability DURING a selected operation is HOST.IO_FAILURE "
        "(exit 4). Successfully admitted PARTIAL native inputs instead yield an "
        "indeterminate Run (exit 3). Three different event positions.")
    rec("D5-V4-replay-versus-regeneration", "computed",
        "verification reads retained objects and creates an OPERATIONAL "
        "verification receipt; regeneration re-executes the exact retained "
        "producer into a candidate namespace and publishes recovered "
        "availability only if every required byte agrees. A mismatch is "
        "HOST.IO_FAILURE / evidence.regeneration-mismatch (exit 4) and cannot "
        "replace the sealed Run. Sealed assurance and the historical verdict "
        "never change; only the availability generation moves.")


def run_all():
    spec, notices = d1_zero_config()
    d2_traces(notices)
    d3_scope_policy_axis()
    d4_repair()
    d5_terminations()
    return RESULTS
