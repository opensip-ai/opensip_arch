"""Zero-config selection, disclosure, invocations, public terminations, comparison,
repair/test authorization, mutation replay, purge refusal and required-output failure."""

from __future__ import annotations

import hashlib
import json

import opensip_ref as R
import closure as CL
import world as W
from opensip_ref import C, H, ident, sha256_text, raw, raw_bytes

REQ = "req1_" + "ab" * 16
EXEC0 = "exec1_" + "cd" * 16
EXEC1 = "exec1_" + "ce" * 16
EXEC2 = "exec1_" + "cf" * 16

MATRIX = R.MATRIX
CELLS = R.CELLS
CAPS = R.CAPABILITY_IDS


# ---------------------------------------------------------------------------
# Zero-config default selection (native section 1.4 / admission section 1.1)
# ---------------------------------------------------------------------------


def default_selection(units):
    """The default profile is FIXED BY THE MATRIX, not by a release: for each
    discovered unit request every capability whose (capability, mode) cell is not
    NOT-SELECTED, including UNSUPPORTED-TYPED cells."""
    rows = []
    for root, mode in units:
        for cap in CAPS:
            if CELLS[(cap, mode)]["state"] == "NOT-SELECTED":
                continue
            rows.append({"capabilityId": cap, "languageMode": mode,
                         "workspaceRoot": root, "required": True})
    return rows


def release_absence_notices(rows, declared):
    """A capability the product requires that this release did not declare AVAILABLE
    is still requested; the absence is disclosed, in the ORIGINAL invocation."""
    out = []
    for r in rows:                                  # order is the selection's own
        modes = declared.get(r["capabilityId"])
        if modes is None or r["languageMode"] not in modes:
            out.append({
                "code": "native.capability-unavailable",
                "capabilityId": r["capabilityId"],
                "languageMode": r["languageMode"],
                "workspaceRoot": r["workspaceRoot"],
                "remedy": "install the provider that supplies this capability, "
                          "or narrow analysis.capabilities explicitly",
            })
    return out


def invocation_availability(per_step):
    steps = []
    for step_id, notices in per_step:
        entry = {"stepId": step_id, "noticeCount": len(notices), "notices": notices}
        R.validate("common", "#/$defs/CapabilityAvailabilityStepV1", entry)
        steps.append(entry)
    coll = {"stepCount": len(steps),
            "totalNoticeCount": sum(s["noticeCount"] for s in steps),
            "steps": steps}
    R.validate("common", "#/$defs/CapabilityAvailabilityV1", coll)
    return coll


def scenario_zero_config(results):
    """Z-1/Z-2/Z-3: a multi-unit repository, a release that lacks some advertised
    capabilities INCLUDING a candidate-only one, a single-step command and a named
    multi-step invocation with DIFFERENT selections at different analysis steps."""
    units_all = [(".", "ts-tsconfig"), ("services/api", "rust-cargo"),
                 ("docs", "syntax-only")]
    units_step1 = [(".", "ts-tsconfig")]

    # The installed release declares a SUBSET.  Availability is not scope.
    declared = {
        "inventory": ["ts-tsconfig", "rust-cargo", "syntax-only"],
        "syntax": ["ts-tsconfig", "rust-cargo", "syntax-only"],
        "imports": ["ts-tsconfig", "rust-cargo"],
        "references": ["ts-tsconfig"],
        "calls": ["ts-tsconfig"],
        "types": ["ts-tsconfig"],
        "clones-fact": ["ts-tsconfig", "rust-cargo", "syntax-only"],
        # reachability, unresolved-edge, clones-near and clones-cross-tsjs are NOT declared
    }
    declared_rows = sorted(
        [{"capabilityId": k, "languageModes": sorted(v)} for k, v in declared.items()],
        key=lambda r: C(r))
    R.validate("native", "#/$defs/ReleaseCapabilityRegistryV1", declared_rows)

    rows_all = default_selection(units_all)
    rows_1 = default_selection(units_step1)
    notices_all = release_absence_notices(rows_all, declared)
    notices_1 = release_absence_notices(rows_1, declared)

    single = invocation_availability([(0, notices_1)])
    multi = invocation_availability([(0, notices_1), (2, notices_all)])

    # a step that SELECTED and found nothing absent contributes an EMPTY entry;
    # a step that made no selection contributes NO entry.
    full_declared = {c: list(MATRIX["languageModes"]) for c in CAPS}
    empty_entry = invocation_availability(
        [(0, release_absence_notices(rows_1, full_declared))])

    # precedence: a capability can be undeclared AND unservable at once
    precedence = {
        "case": "references under syntax-only",
        "undeclaredByRelease": True,
        "unservableByTheAdmittedUniverse": True,
        "coveragePair": ["language-tier-unsupported", "capability-missing"],
        "why": "section 10 ranks language-tier-unsupported ahead of provider-unavailable, "
               "so the more specific one wins and the release-absence account never "
               "overrides it",
    }
    candidate_only = {
        "capabilities": [c["id"] for c in MATRIX["capabilities"] if not c["relations"]],
        "coverageEntry": None,
        "projection": "selection-account-only",
        "publicRoute": "CommandEnvelope.availability notice "
                       "(code native.capability-unavailable) -- its ONLY public route",
    }

    results["zero-config-selection"] = {
        "discoveredUnits": [{"workspaceRoot": r, "languageMode": m} for r, m in units_all],
        "defaultIsFixedByTheMatrixNotTheRelease": True,
        "requestedRowsAllUnits": len(rows_all),
        "requestedRowsStep0": len(rows_1),
        "analysisSpecRequestedCapabilitiesBound": 1024,
        "installedReleaseDeclaration": declared_rows,
        "singleStepCommand": {
            "command": "opensip (default: discovery + durable analyze, steps analysis+render)",
            "availability": single,
        },
        "namedMultiStepInvocation": {
            "steps": [
                {"stepId": 0, "kind": "analysis", "selection": "root TypeScript unit only"},
                {"stepId": 1, "kind": "comparison", "selection": "none -> no entry"},
                {"stepId": 2, "kind": "analysis", "selection": "all three units"},
                {"stepId": 3, "kind": "render", "selection": "none -> no entry"},
            ],
            "availability": multi,
            "totalExceedsOneStepBound": multi["totalNoticeCount"] > 0,
        },
        "stepThatCheckedAndFoundNothing": empty_entry,
        "boundedCardinality": {"stepsMax": 64, "noticesPerStepMax": 1024,
                               "noticeCountEqualsArrayLength": all(
                                   s["noticeCount"] == len(s["notices"])
                                   for s in multi["steps"]),
                               "totalIsTheSum": multi["totalNoticeCount"] ==
                               sum(s["noticeCount"] for s in multi["steps"])},
        "ordering": "x-opensip-order: sequence -- the selection's own order",
        "ownershipFieldsAreTyped": ["capabilityId", "languageMode", "workspaceRoot"],
        "codeIsAConst": "native.capability-unavailable",
        "applicableOutputFormats": {
            cmd["name"]: cmd["formats"] for cmd in
            R.doc_json("docs/coop/design-corrections/workflows/command-inventory.v1.json")["commands"]
            if cmd.get("requestClass") == "analysis"},
        "declaredParityFieldPresentOnEveryAnalysisCommand": all(
            "capability-availability" in cmd["parityFields"] for cmd in
            R.doc_json("docs/coop/design-corrections/workflows/command-inventory.v1.json")["commands"]
            if cmd.get("requestClass") == "analysis"),
        "productPromiseVersusInstalledAvailability": precedence,
        "candidateOnlyCapabilities": candidate_only,
        "explicitOverride": {
            "carrier": "product-configuration analysis.capabilities (same vocabulary)",
            "provenance": "explicit override records its own provenance; the default's is DEFAULTED",
            "overridesTheRequestNotTheObligation": True,
        },
        "availabilityIsAdvisory": "terminates nothing, mints no Coverage, grants no "
                                  "Control verdict or repair authority, is never a Candidate",
    }
    return single, multi


# ---------------------------------------------------------------------------
# Internal decision key -> public termination, by ORIGINATING BOUNDARY
# ---------------------------------------------------------------------------

ROUTES = R.ROUTE_REGISTRY["keys"]


def normalize_internal_key(raw_key):
    """Longest registered key followed by a colon; the remainder is subject data.
    A string matching no registered key REFUSES."""
    if raw_key in ROUTES:
        return raw_key, None
    best = None
    for k in ROUTES:
        if raw_key.startswith(k + ":") and (best is None or len(k) > len(best)):
            best = k
    if best is None:
        raise R.Refuse("native.public-route-key-unregistered", raw_key)
    return best, raw_key[len(best) + 1:]


MARKER = "...#sha256:"


def bounded_subject(raw_text):
    """Unicode CODE POINTS for length and slicing; UTF-8 bytes for the digest."""
    if len(raw_text) <= 1024:
        return raw_text
    keep = 1024 - len(MARKER) - 64
    return raw_text[:keep] + MARKER + hashlib.sha256(raw_text.encode("utf-8")).hexdigest()


def public_termination_for(raw_key, origin):
    key, subject = normalize_internal_key(raw_key)
    row = ROUTES[key]
    if origin not in row["possibleOrigins"]:
        raise R.Refuse("native.public-route-origin-not-possible", f"{key}@{origin}")
    route = row["byOriginatingBoundary"][origin] if row.get("originDependent") \
        else row["route"]
    term = {"class": route["class"], "errorCode": route["errorCode"]}
    if "faultCause" in route:
        term["faultCause"] = route["faultCause"]
    if route.get("domainDetail"):
        d = {"code": route["domainDetail"], "remedy": "correct the named input"}
        if subject is not None:
            d["subject"] = bounded_subject(f"{key}:{subject}")
        term["domainDetail"] = d
    R.validate("common", "#/$defs/StepTermination", term)
    return term, route


def failure_envelope(raw_key, origin, request_id=REQ):
    term, route = public_termination_for(raw_key, origin)
    key, subject = normalize_internal_key(raw_key)
    if "domainDetail" in term:
        errors = [term["domainDetail"]]          # exactly that detail; never disagree
    else:
        d = {"code": route["envelopeDetail"], "remedy": "correct the named input"}
        if subject is not None:
            d["subject"] = bounded_subject(f"{key}:{subject}")
        errors = [d]
    exit_code = {"success": 0, "policy-failed": 1, "request-rejected": 2,
                 "indeterminate": 3, "operational-failed": 4, "interrupted": 130}[term["class"]]
    env = {
        "schemaFamily": "opensip.product.envelope",
        "schemaMajor": 2,
        "kind": "failure",
        "requestId": request_id,
        "termination": term,
        "exitCode": exit_code,
        "errors": errors,
    }
    R.validate("command-envelope", "#", env)          # no run envelope is fabricated
    return env


def scenario_public_terminations(results):
    """Z-4/Z-5/Z-6: complete failure envelopes from an actual internal refusal plus
    its ORIGINATING BOUNDARY, and the bounded-diagnostic elision."""
    cases = {
        "configuration-input": (
            "native.requested-capability-unregistered:made-up-capability",
            "external-configuration"),
        "retained-external-input": (
            "native.requested-capability-unregistered:made-up-capability",
            "externally-supplied-spec"),
        "host-generated-invalid-internal-record": (
            "native.requested-capability-unregistered:made-up-capability",
            "host-generated-internal-layer"),
        "producer-boundary-failure": (
            "native.coverage-cause-not-for-deficiency:input-closure-incomplete:capability-missing",
            "producer-boundary"),
        "not-selected-cell-origin-independent": (
            "native.requested-capability-mode-not-selected:clones-cross-tsjs:rust-cargo",
            "external-configuration"),
        "authenticated-release-declaration": (
            "native.release-capability-preview-constant:preview-typescript",
            "authenticated-release-declaration"),
    }
    out = {}
    for name, (key, origin) in cases.items():
        out[name] = failure_envelope(key, origin)

    neg = {}
    try:
        public_termination_for("something.not.registered:x", "external-configuration")
        neg["unregistered-internal-key"] = "ADMITTED(!)"
    except R.Refuse as exc:
        neg["unregistered-internal-key"] = exc.code + ":" + exc.detail
    try:
        public_termination_for("native.release-capability-unregistered:x",
                               "external-configuration")
        neg["origin-a-key-cannot-have"] = "ADMITTED(!)"
    except R.Refuse as exc:
        neg["origin-a-key-cannot-have"] = exc.code + ":" + exc.detail

    long_mode = "m" * 4096
    long_env = failure_envelope(
        "native.requested-capability-mode-unregistered:" + long_mode,
        "external-configuration")
    subj = long_env["errors"][0]["subject"]

    d9 = R.doc_json("docs/coop/artifacts/d9-exit-contract.v1.14.json")
    inherited_causes = d9["scenarioAxesSchema"]["properties"]["faultCause"]["enum"]
    product_causes = R.COMMON["$defs"]["D9FaultCause"]["enum"]
    inherited_codes = d9["codeVocabulary"]["errorCodes"]
    product_codes = R.COMMON["$defs"]["D9ErrorCode"]["enum"]
    fc2ec = d9["codeMaps"]["faultCauseToErrorCode"]

    results["public-terminations"] = {
        "envelopes": out,
        "negatives": neg,
        "boundedSubject": {
            "rawCodePoints": len("native.requested-capability-mode-unregistered:" + long_mode),
            "boundedCodePoints": len(subj),
            "endsWithDigest": subj[-75:-64] == MARKER,
            "registeredKeyPreservedVerbatim":
                subj.startswith("native.requested-capability-mode-unregistered:"),
            "classAndCodeUnchangedByElision": long_env["termination"]["errorCode"],
        },
        "d9ExtensionCheck": {
            "inheritedArtifact": "docs/coop/artifacts/d9-exit-contract.v1.14.json",
            "inheritedFaultCauses": inherited_causes,
            "productFaultCauses": product_causes,
            "addedFaultCauses": sorted(set(product_causes) - set(inherited_causes)),
            "errorCodesUnchanged": sorted(inherited_codes) == sorted(product_codes),
            "classToExitCodeUnchanged": d9["classToExitCode"],
            "hostInvariantMapsToAnExistingErrorCode":
                "SYSTEM.OUTCOME.ILLEGAL_STATE" in inherited_codes,
            "hostInvariantHasNoInheritedPreimage":
                "SYSTEM.OUTCOME.ILLEGAL_STATE" not in fc2ec.values(),
            "injectivityPreserved": True,
            "declaredPrecedence": d9["causeModel"]["precedence"],
            "productPrecedenceAgrees":
                d9["causeModel"]["precedence"][0] == "faultCause",
            "verdict": "the extension is exactly one faultCause member mapped to an "
                       "EXISTING error code; no class, exit code, reason code or error "
                       "code changes, and the inherited map stays total and injective "
                       "over its declared cause domain",
        },
    }


# ---------------------------------------------------------------------------
# ScopeDocumentV1 bound as an analysis-spec parameter, and the scope axis
# ---------------------------------------------------------------------------


def scope_document(include, exclude=()):
    sd = {"schemaFamily": "opensip.product.scope", "schemaMajor": 1,
          "include": list(include), "exclude": list(exclude)}
    R.validate("policy-document", "#/$defs/ScopeDocumentV1", sd)
    return sd


def scenario_scope_parameter(results):
    """W-2: a REAL ScopeDocumentV1 scope-policy parameter bound into the retained
    analysis-spec through its exact registered document and selector, and a
    comparison in which ONLY that scope policy changes."""
    doc_path = "docs/coop/design-corrections/workflows/schemas/policy-document.schema.json"
    row = R.PAYLOAD_REGISTRY["classes"]["parameter"]["rows"][
        "workflows/schemas/policy-document.schema.json#/$defs/ScopeDocumentV1"]
    schema_digest = R.doc_digest(doc_path)

    before = scope_document(["src/**"], ["src/generated/**"])
    after = scope_document(["src/**"])

    spec_before = W.analysis_spec(
        [{"capabilityId": "inventory", "languageMode": "ts-tsconfig",
          "workspaceRoot": ".", "required": True}],
        parameters=[{"schemaDigest": schema_digest, "payloadDigest": raw(before)}])
    spec_after = W.analysis_spec(
        [{"capabilityId": "inventory", "languageMode": "ts-tsconfig",
          "workspaceRoot": ".", "required": True}],
        parameters=[{"schemaDigest": schema_digest, "payloadDigest": raw(after)}])

    # the OTHER scope record: the repository extent actually walked
    extent = W.scope_descriptor(["."], excluded=[".git", "node_modules"])

    # a bounded verifier proving selection membership from the retained spec
    def verify_binding(spec, doc):
        rows = [p for p in spec["parameters"] if p["schemaDigest"] == schema_digest]
        if not rows:
            raise R.Refuse("SCOPE_PARAMETER_NOT_SELECTED", "")
        if not any(p["payloadDigest"] == raw(doc) for p in rows):
            raise R.Refuse("SCOPE_DOCUMENT_NOT_THE_SELECTED_ONE", "")
        return True

    neg = {}
    try:
        verify_binding(spec_before, after)
        neg["document-not-selected"] = "ADMITTED(!)"
    except R.Refuse as exc:
        neg["document-not-selected"] = exc.code
    try:
        verify_binding(W.analysis_spec(
            [{"capabilityId": "inventory", "languageMode": "ts-tsconfig",
              "workspaceRoot": ".", "required": True}]), before)
        neg["spec-selects-no-scope-parameter"] = "ADMITTED(!)"
    except R.Refuse as exc:
        neg["spec-selects-no-scope-parameter"] = exc.code
    unregistered = R.doc_digest("docs/coop/design-corrections/foundation/g13-result-schema.v5.json")
    rows_reg = R.PAYLOAD_REGISTRY["classes"]["parameter"]["rows"]
    known = {R.doc_digest({"foundation/import-source-context.schema.json":
                           R._PATHS["import-source-context"],
                           "workflows/schemas/policy-document.schema.json":
                           R._PATHS["policy-document"]}[v["document"]])
             for v in rows_reg.values()}
    neg["unregistered-parameter-document"] = (
        "PAYLOAD_PARAMETER_ROW_UNREGISTERED" if unregistered not in known else "ADMITTED(!)")

    results["scope-policy-parameter"] = {
        "registeredRowKey":
            "workflows/schemas/policy-document.schema.json#/$defs/ScopeDocumentV1",
        "document": row["document"], "selector": row["selector"],
        "schemaDigestIsTheWholeDocument": schema_digest,
        "scopeDocumentBefore": before, "scopeDocumentAfter": after,
        "payloadDigestBefore": raw(before), "payloadDigestAfter": raw(after),
        "boundVerifierAcceptsTheSelectedDocument": verify_binding(spec_before, before),
        "analysisSpecDigestBefore": raw(spec_before),
        "analysisSpecDigestAfter": raw(spec_after),
        "onlyTheScopePolicyChanged": True,
        "distinctFromTheRepositoryExtent": {
            "foundationScopeDescriptor": extent,
            "planScopeDigest": raw(extent),
            "note": "plan.scopeDigest names the foundation scope-descriptor (the extent "
                    "actually walked); EvaluationContext.scopeDigest names ScopeDocumentV1 "
                    "(the operator's include/exclude glob policy over that extent). "
                    "Neither substitutes for the other and both may appear in one Plan.",
        },
        "negatives": neg,
    }
    return before, after, extent


CLASSIFICATIONS = ["UNCHANGED", "CODE-NET-NEW", "CODE-FIXED", "DETECTION-DELTA",
                   "POLICY-DELTA", "SCOPE-DELTA", "WAIVER-DELTA", "EVIDENCE-DELTA",
                   "INDETERMINATE"]


def _counts(entries):
    c = {k: 0 for k in CLASSIFICATIONS}
    for e in entries:
        c[e["classification"]] += 1
    c["gating"] = sum(1 for e in entries if e["gates"])
    return c


def scenario_comparison(results, scope_before, scope_after, extent):
    """W-1: current-baseline audit with a SCOPE-only axis change, a missing required
    detector pivot, an evidence-availability change, and an EMPTY-result comparison
    that is still indeterminate."""
    base_closure = "closure2:" + "1a" * 32
    cur_closure = "closure2:" + "1b" * 32
    run_id = "run2:" + "2a" * 32
    baseline_id = "baseline2:" + "3a" * 32
    snap_id = "snapshot2:" + "4a" * 32
    policy = W.simple_policy("no-unused-export", "references", "resolved-binding")
    policy_digest = raw(policy)
    waivers_digest = raw(W.EMPTY_WAIVERS)

    def ctx(scope_doc, closures, imports):
        return {
            "policyDigest": policy_digest,
            "scopeDigest": raw(scope_doc),
            "waiverSetDigest": waivers_digest,
            "detectorClosureIds": list(closures),
            "evidenceAvailability": {
                "importKinds": sorted({i["kind"] for i in imports}),
                "relations": ["runtime-observation"] if imports else [],
                "imports": sorted(imports, key=lambda i: i["importId"]),
            },
        }

    imp_a = {"kind": "runtime", "importId": "import2:" + "5a" * 32,
             "payloadDigest": "aa" * 32, "sourceCorrespondenceDigest": "ab" * 32,
             "scopeDigest": "ac" * 32, "observationDigest": "ad" * 32}
    imp_b = dict(imp_a, importId="import2:" + "5b" * 32, payloadDigest="ba" * 32)

    def descriptor(*, base_scope, cur_scope, base_imports, cur_imports,
                   detector_method, entries, verdict, performed=True,
                   whole_reason=None, rule_defs=(), pivots=None):
        d = {
            "schemaFamily": "opensip.product.comparison", "schemaMajor": 1,
            "baselineId": baseline_id, "currentRunId": run_id,
            "currentSnapshotId": snap_id,
            "auditProfile": {"name": "code-regression", "gateCodeNetNew": True,
                             "gateNewlyLiveByPolicyAxes": False,
                             "gateAllCurrentLive": False,
                             "newWaiverSuppressesCodeNetNew": False,
                             "gateRuleUnder": "baseline-or-current"},
            "projectCorrespondence": "same-project",
            "comparisonPerformed": performed,
            "baselineContext": ctx(base_scope, [base_closure], base_imports),
            "currentContext": ctx(cur_scope, [cur_closure], cur_imports),
            "contextDelta": {
                "codeChanged": True,
                "detectorChanged": base_closure != cur_closure,
                "policyChanged": False,
                "scopeChanged": raw(base_scope) != raw(cur_scope),
                "waiversChanged": False,
                "evidenceAvailabilityChanged":
                    sorted(i["importId"] for i in base_imports)
                    != sorted(i["importId"] for i in cur_imports),
            },
            "pivotsAvailable": pivots or {"E0": "not-needed", "E1": "not-needed",
                                          "E2": "not-needed", "E3": "available"},
            "detectors": [detector_method],
            "ruleDeficiencies": list(rule_defs),
            "entries": entries,
            "counts": _counts(entries),
            "verdict": verdict,
        }
        if whole_reason:
            d["wholeIndeterminateReason"] = whole_reason
        result = {"comparisonResultId": "comparison2:" + H("workflow.comparison", d),
                  "descriptor": d}
        R.validate("comparison-result", "#", result)
        return result

    identical = {"detectorId": "unused-export", "baselineClosureId": base_closure,
                 "currentClosureId": base_closure, "baselineSemanticsMajor": 2,
                 "currentSemanticsMajor": 2, "method": "identical-closure"}
    removed = {"detectorId": "unused-export", "baselineClosureId": base_closure,
               "currentClosureId": None, "baselineSemanticsMajor": 2,
               "currentSemanticsMajor": None, "method": "indeterminate",
               "indeterminateReason": "pivot-detector-unavailable"}

    scope_entry = {
        "fingerprint": "finding-key2:" + "6a" * 32, "ruleId": "no-unused-export",
        "detectorId": "unused-export",
        "presence": {"B": True, "E0": None, "E1": True, "E2": True, "E3": False,
                     "E4": False, "waivedB": False, "waivedC": False},
        "classification": "SCOPE-DELTA", "direction": "vanished",
        "subsequentDeltas": [], "liveInCurrent": False, "gates": False,
    }
    scope_only = descriptor(base_scope=scope_before, cur_scope=scope_after,
                            base_imports=[imp_a], cur_imports=[imp_a],
                            detector_method=identical, entries=[scope_entry],
                            verdict="pass")

    missing_entry = {
        "fingerprint": "finding-key2:" + "6b" * 32, "ruleId": "no-unused-export",
        "detectorId": "unused-export",
        "presence": {"B": True, "E0": None, "E1": False, "E2": False, "E3": False,
                     "E4": False, "waivedB": False, "waivedC": False},
        "classification": "INDETERMINATE",
        "indeterminateReason": "pivot-detector-unavailable",
        "subsequentDeltas": [], "liveInCurrent": False, "gates": True,
        "gateReason": "indeterminate-gating-rule",
    }
    missing_pivot = descriptor(
        base_scope=scope_before, cur_scope=scope_before, base_imports=[imp_a],
        cur_imports=[imp_a], detector_method=removed, entries=[missing_entry],
        verdict="indeterminate",
        pivots={"E0": "unavailable", "E1": "not-needed", "E2": "not-needed",
                "E3": "not-needed"})

    evidence_entry = {
        "fingerprint": "finding-key2:" + "6c" * 32, "ruleId": "no-unused-export",
        "detectorId": "unused-export",
        "presence": {"B": True, "E0": None, "E1": True, "E2": True, "E3": True,
                     "E4": True, "waivedB": False, "waivedC": False},
        "classification": "INDETERMINATE",
        "indeterminateReason": "evidence-availability-changed",
        "subsequentDeltas": [], "liveInCurrent": True, "gates": True,
        "gateReason": "indeterminate-gating-rule",
    }
    evidence_changed = descriptor(
        base_scope=scope_before, cur_scope=scope_before, base_imports=[imp_a],
        cur_imports=[imp_b], detector_method=identical, entries=[evidence_entry],
        verdict="indeterminate",
        rule_defs=[{"ruleId": "no-unused-export", "gating": True,
                    "cause": "required-evidence-unavailable"}])

    empty_result = descriptor(
        base_scope=scope_before, cur_scope=scope_before, base_imports=[imp_a],
        cur_imports=[imp_a], detector_method=removed, entries=[],
        verdict="indeterminate",
        rule_defs=[{"ruleId": "no-unused-export", "gating": True,
                    "cause": "required-coverage-unknown"}],
        pivots={"E0": "unavailable", "E1": "not-needed", "E2": "not-needed",
                "E3": "not-needed"})

    results["comparison"] = {
        "scopeAxisOnly": {
            "comparisonResultId": scope_only["comparisonResultId"],
            "contextDelta": scope_only["descriptor"]["contextDelta"],
            "classification": "SCOPE-DELTA",
            "baselineScopeDigest": raw(scope_before),
            "currentScopeDigest": raw(scope_after),
            "planScopeDigestUnchanged": raw(extent),
            "note": "only EvaluationContext.scopeDigest (ScopeDocumentV1) moved; "
                    "plan.scopeDigest (the walked extent) and the snapshot did not",
        },
        "missingRequiredDetectorPivot": {
            "comparisonResultId": missing_pivot["comparisonResultId"],
            "detectorMethod": "indeterminate/pivot-detector-unavailable",
            "verdict": "indeterminate",
            "publicTermination": {"class": "indeterminate", "exitCode": 3,
                                  "reasonCodes": ["BASELINE.RECIPE_UNSUPPORTED"],
                                  "domainDetail": "BASELINE.PIVOT_DETECTOR_UNAVAILABLE"},
        },
        "evidenceAvailabilityChanged": {
            "comparisonResultId": evidence_changed["comparisonResultId"],
            "classification": "INDETERMINATE",
            "reason": "evidence-availability-changed",
            "why": "a gating rule declares required runtime evidence and the bound "
                   "import2 identity changed; replacing an artifact of the same kind "
                   "is still an evidence change",
            "publicTermination": {"class": "indeterminate", "exitCode": 3,
                                  "reasonCodes": ["VERDICT.INDETERMINATE"],
                                  "domainDetail": "COMPARISON.REQUIRED_EVIDENCE_UNAVAILABLE"},
        },
        "emptyResultStillIndeterminate": {
            "comparisonResultId": empty_result["comparisonResultId"],
            "entries": 0, "verdict": "indeterminate",
            "why": "missing required detector re-evaluation makes the comparison "
                   "indeterminate whenever an enabled rule gates, EVEN WHEN BOTH "
                   "observed finding sets are empty; entry counts cannot prove absence",
        },
        "axisOrder": ["code (B->E0)", "detection (E0->E1)", "policy (E1->E2)",
                      "scope (E2->E3)", "waiver (E3->E4)"],
    }


# ---------------------------------------------------------------------------
# Mutation replay scope, repair-apply key, pinned purge, required-output failure
# ---------------------------------------------------------------------------


def scenario_mutation_and_purge(results):
    scope = {"schemaVersion": 1, "requestId": REQ, "stepId": 2,
             "projectId": W.PROJECT_ID, "operation": "baseline-adopt"}
    R.validate("invocation-record", "#/$defs/MutationReplayScopeV1", scope)
    key = H("workflow.mutation-intent", scope)      # bare 64-hex

    other_request = dict(scope, requestId="req1_" + "ef" * 16)
    other_step = dict(scope, stepId=3)
    other_op = dict(scope, operation="waive")

    repair_plan_id = "repairplan2:" + "7a" * 32
    base_snapshot = "snapshot2:" + "7b" * 32
    apply_record = {"operation": "repair-apply", "projectId": W.PROJECT_ID,
                    "repairPlanId": repair_plan_id, "baseSnapshotId": base_snapshot}
    apply_key = raw(apply_record)                   # RAW SHA-256 of the canonical record

    try:
        R.validate("invocation-record", "#/$defs/MutationReplayScopeV1",
                   dict(scope, operation="repair-apply"))
        excluded = "ADMITTED(!)"
    except R.Refuse as exc:
        excluded = exc.code

    pins = sorted([
        {"pinId": "baseline:main", "kind": "baseline"},
        {"pinId": "backup-export:2026-09-01", "kind": "backup-export"},
        {"pinId": "repair-prereq:plan-7a", "kind": "repair-prerequisite"},
    ], key=lambda p: p["pinId"].encode("utf-8"))
    disclosure = {
        "runId": "run2:" + "8a" * 32,
        "activePins": pins,
        "consequences": ["named-pins-revoked", "dependent-evidence-replay-unavailable",
                         "sealed-history-retained"],
    }
    R.validate("common", "#/$defs/PinnedPurgeDisclosure", disclosure)
    detail = {"code": "evidence.pinned", "remedy": "revoke the named pins under the "
                                                   "explicit destructive purge authorization",
              "subject": disclosure["runId"], "purgeDisclosure": disclosure}
    term = {"class": "request-rejected", "errorCode": "REQUEST.PRECONDITION_FAILED",
            "domainDetail": detail}
    R.validate("common", "#/$defs/StepTermination", term)
    purge_env = {"schemaFamily": "opensip.product.envelope", "schemaMajor": 2,
                 "kind": "failure", "requestId": REQ, "termination": term,
                 "exitCode": 2, "errors": [detail]}
    R.validate("command-envelope", "#", purge_env)

    neg = {}
    try:
        R.validate("common", "#/$defs/PinnedPurgeDisclosure",
                   dict(disclosure, activePins=pins[:1]))
        neg["subset-is-schema-valid-but-not-complete"] = (
            "SCHEMA-VALID; completeness is a HOST obligation the schema cannot decide "
            "-- the host compares the disclosed set with the complete current set it "
            "observed under the exclusive purge lease")
    except R.Refuse as exc:
        neg["subset-is-schema-valid-but-not-complete"] = exc.code
    try:
        R.validate("common", "#/$defs/PinnedPurgeDisclosure",
                   dict(disclosure, consequences=["named-pins-revoked"]))
        neg["truncated-consequences"] = "ADMITTED(!)"
    except R.Refuse as exc:
        neg["truncated-consequences"] = exc.code
    try:
        R.validate("common", "#/$defs/DomainDetail",
                   {"code": "evidence.purged", "remedy": "r",
                    "purgeDisclosure": disclosure})
        neg["purge-disclosure-on-another-code"] = "ADMITTED(!)"
    except R.Refuse as exc:
        neg["purge-disclosure-on-another-code"] = exc.code

    # required-output failure AFTER a committed Run
    run_id = "run2:" + "9a" * 32
    delivery_term = {
        "class": "operational-failed", "errorCode": "DELIVERY.REQUIRED_FAILED",
        "faultCause": "delivery-required", "runId": run_id,
        "domainDetail": {"code": "DELIVERY.RENDERER_FAILED_AFTER_COMMIT",
                         "remedy": "re-render from the committed Run; the Run is not rewritten"},
    }
    R.validate("common", "#/$defs/StepTermination", delivery_term)
    delivery_env = {"schemaFamily": "opensip.product.envelope", "schemaMajor": 2,
                    "kind": "failure", "requestId": REQ, "termination": delivery_term,
                    "exitCode": 4, "errors": [delivery_term["domainDetail"]]}
    R.validate("command-envelope", "#", delivery_env)

    # a MISSING parity field is the same operational fault, not an empty result
    missing_field_term = dict(delivery_term)
    missing_field_term.pop("runId")
    R.validate("common", "#/$defs/StepTermination", missing_field_term)

    regen_term = {"class": "operational-failed", "errorCode": "HOST.IO_FAILURE",
                  "faultCause": "host-io",
                  "domainDetail": {"code": "evidence.regeneration-mismatch",
                                   "remedy": "the sealed Run is not replaced; "
                                             "investigate the producing closure"}}
    R.validate("common", "#/$defs/StepTermination", regen_term)

    query_after_purge = {"class": "request-rejected",
                         "errorCode": "REQUEST.PRECONDITION_FAILED",
                         "domainDetail": {"code": "evidence.purged",
                                          "remedy": "the sealed manifest is retained; "
                                                    "evidence bytes are unavailable"}}
    R.validate("common", "#/$defs/StepTermination", query_after_purge)

    ephemeral_term = {"class": "request-rejected", "errorCode": "REQUEST.UNSATISFIABLE",
                      "domainDetail": {"code": "WORKFLOW.EPHEMERAL_CANNOT_SUPPLY_AUTHORITY",
                                       "remedy": "run an authoritative analysis"}}
    R.validate("common", "#/$defs/StepTermination", ephemeral_term)

    results["mutation-purge-and-delivery"] = {
        "genericMutationReplayScope": scope,
        "idempotencyKeyBareHex": key,
        "differentFreshRequestNeverDeduplicates":
            key != H("workflow.mutation-intent", other_request),
        "differentStepIsADifferentKey": key != H("workflow.mutation-intent", other_step),
        "differentOperationIsADifferentKey": key != H("workflow.mutation-intent", other_op),
        "repairApplyIsExcludedFromGenericMutation": excluded,
        "repairApplyKeyRecord": apply_record,
        "repairApplyKeyIsRawSha256OfCanonicalRecord": apply_key,
        "twoKeysAreDifferentRecipes":
            "H(workflow.mutation-intent, scope) vs raw SHA-256 of the canonical "
            "repair-apply record; neither substitutes for the other",
        "pinnedPurgeRefusal": purge_env,
        "pinnedPurgeNegatives": neg,
        "requiredOutputFailureAfterCommit": delivery_env,
        "missingParityFieldIsTheSameFault": missing_field_term,
        "regenerationMismatch": regen_term,
        "queryAfterPurge": query_after_purge,
        "ephemeralCannotSupplyAuthority": ephemeral_term,
    }


# ---------------------------------------------------------------------------
# Invocation records: single-step and named multi-step
# ---------------------------------------------------------------------------


def scenario_invocations(results, single_av, multi_av):
    run_id = "run2:" + "aa" * 32
    plan_id = "plan2:" + "ab" * 32
    exec_plan_id = "exec-plan2:" + "ac" * 32

    analysis_result = {
        "kind": "analysis", "authority": "authoritative", "runId": run_id,
        "planId": plan_id, "verdict": "pass", "requiredCoverage": "satisfied",
        "durability": "committed", "deficiency": "none", "secondaryDeficiencies": [],
    }
    render_result = {"kind": "render", "format": "json", "rendererVersion": 2,
                     "bytes": 4096, "truncation": False, "written": True}
    retention = {"policy": "durable-unbounded", "provenance": "DEFAULTED",
                 "firstUse": True, "storageRoot": "/Users/dev/.opensip/store"}

    def step(sid, kind, params, depends=(), gate="completed", retry="none",
             requirement="required"):
        return {"stepId": sid, "kind": kind, "requirement": requirement,
                "dependsOn": list(depends), "dependencyGate": gate,
                "retryPolicy": retry, "params": params}

    analysis_params = {"kind": "analysis", "profile": "default", "role": "primary",
                       "durability": "authoritative", "snapshotSource": "live-worktree"}
    render_params = {"kind": "render", "format": "json", "destination": "stdout",
                     "sourceSteps": [0], "required": True}

    single = {
        "schemaFamily": "opensip.product.invocation", "schemaMajor": 1,
        "requestId": REQ, "projectId": W.PROJECT_ID,
        "workflow": {"kind": "builtin", "name": "default"},
        "mode": {"interactive": True, "ci": False, "ephemeral": False},
        "orderedSteps": [step(0, "analysis", analysis_params, retry="idempotent-retry"),
                         step(1, "render", render_params, depends=[0], gate="terminal")],
        "stepResults": [
            {"stepId": 0, "outcome": "completed",
             "attempts": [{"executionId": EXEC0, "outcome": "completed",
                           "derivation": {"planId": plan_id, "executionPlanId": exec_plan_id,
                                          "stageCount": 3, "stagesCompleted": 3}}],
             "result": analysis_result, "termination": {"class": "success"}},
            {"stepId": 1, "outcome": "completed", "attempts": [
                {"executionId": EXEC1, "outcome": "completed"}],
             "result": render_result, "termination": {"class": "success"}},
        ],
        "termination": {"class": "success"}, "terminationEmitted": True,
        "retentionDisclosure": retention,
    }
    R.validate("invocation-record", "#", single)

    cmp_params = {"kind": "comparison", "currentStep": 0,
                  "baseline": "opensip.baseline.json", "auditProfile": "code-regression"}
    analysis_delegated = dict(analysis_params, verdictGate="delegated")
    analysis_second = {"kind": "analysis", "profile": "default", "role": "primary",
                       "durability": "authoritative", "snapshotSource": "live-worktree"}
    multi = {
        "schemaFamily": "opensip.product.invocation", "schemaMajor": 1,
        "requestId": REQ, "projectId": W.PROJECT_ID,
        "workflow": {"kind": "profile", "contributionId": "opensip.first-party.workflows",
                     "activationId": "ci-audit-and-fit", "profileVersion": "1.0.0"},
        "mode": {"interactive": False, "ci": True, "ephemeral": False},
        "orderedSteps": [
            step(0, "analysis", analysis_delegated, retry="idempotent-retry"),
            step(1, "comparison", cmp_params, depends=[0]),
            step(2, "analysis", analysis_second, depends=[0]),
            step(3, "render", {"kind": "render", "format": "sarif",
                               "destination": "file", "path": "out.sarif",
                               "sourceSteps": [0, 1, 2], "required": True},
                 depends=[0, 1, 2], gate="terminal"),
        ],
        "termination": {"class": "success"}, "terminationEmitted": True,
        "retentionDisclosure": retention,
    }
    R.validate("invocation-record", "#", multi)

    env_single = {"schemaFamily": "opensip.product.envelope", "schemaMajor": 2,
                  "kind": "run", "requestId": REQ, "projectId": W.PROJECT_ID,
                  "termination": {"class": "success"}, "exitCode": 0,
                  "run": analysis_result, "availability": single_av,
                  "retentionDisclosure": retention}
    R.validate("command-envelope", "#", env_single)
    env_multi = {"schemaFamily": "opensip.product.envelope", "schemaMajor": 2,
                 "kind": "invocation", "requestId": REQ, "projectId": W.PROJECT_ID,
                 "termination": {"class": "success"}, "exitCode": 0,
                 "invocation": multi, "availability": multi_av}
    R.validate("command-envelope", "#", env_multi)

    neg = {}
    try:
        R.validate("invocation-record", "#", dict(single, orderedSteps=[
            step(0, "analysis", analysis_params, depends=[1])]))
        neg["forward-dependency"] = "SCHEMA-VALID (WORKFLOW.DEPENDENCY_CYCLE is a host check)"
    except R.Refuse as exc:
        neg["forward-dependency"] = exc.code
    try:
        R.validate("invocation-record", "#", dict(single, orderedSteps=[
            step(0, "mutation", {"kind": "mutation", "mutationClass": "waive",
                                 "idempotencyKey": "0" * 64}, retry="idempotent-retry")]))
        neg["mutation-with-idempotent-retry"] = "ADMITTED(!)"
    except R.Refuse as exc:
        neg["mutation-with-idempotent-retry"] = exc.code
    try:
        R.validate("invocation-record", "#", dict(single, orderedSteps=[
            step(0, "query", {"kind": "analysis", "profile": "default", "role": "primary",
                              "durability": "authoritative",
                              "snapshotSource": "live-worktree"})]))
        neg["step-kind-differs-from-parameter-kind"] = "ADMITTED(!)"
    except R.Refuse as exc:
        neg["step-kind-differs-from-parameter-kind"] = exc.code
    try:
        R.validate("invocation-record", "#", dict(single, orderedSteps=[
            step(0, "analysis", analysis_params),
            step(1, "query", {"kind": "query", "operation": "finding.list",
                              "view": {"kind": "latest"}, "completeness": "best-effort",
                              "page": {"limit": 10}},
                 depends=[0], gate="terminal")]))
        neg["terminal-gate-on-a-non-render-step"] = "ADMITTED(!)"
    except R.Refuse as exc:
        neg["terminal-gate-on-a-non-render-step"] = exc.code

    results["invocations"] = {
        "singleStep": single,
        "namedMultiStep": multi,
        "envelopeSingleStep": env_single,
        "envelopeMultiStep": env_multi,
        "negatives": neg,
    }
