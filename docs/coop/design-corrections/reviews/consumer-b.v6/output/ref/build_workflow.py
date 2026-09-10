"""Vector group D: invocations, zero-config selection under a release that lacks
some advertised capabilities, public failure envelopes, the pinned-purge refusal,
mutation replay scope vs the repair-apply key, and the ScopeDocumentV1
comparison axis. Every public example is validated against the kit's schemas."""
import sys, os, json, hashlib, copy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from osip import *
from model import *
from build_ts import S, V, PROJECT_ID
from build_ts2 import (PLAN_ID, SNAP_ID, POLICY, POLICY_DIGEST, WAIVERS, WAIVER_DIGEST)
from build_ts3 import RUN_ID

WF = os.path.join(KIT, "docs/coop/design-corrections/workflows/schemas")
INVENTORY = loadj("docs/coop/design-corrections/workflows/command-inventory.v1.json")
PUBREG = loadj("docs/coop/design-corrections/public-detail-registry.v1.json")
D9 = loadj("docs/coop/artifacts/d9-exit-contract.v1.14.json")

# --------------------------------------------------------- schema validation
import jsonschema
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

_docs = {}
for fn in sorted(os.listdir(WF)):
    if fn.endswith(".json"):
        d = json.load(open(os.path.join(WF, fn)))
        _docs[d["$id"]] = d
REG = Registry().with_resources(
    [(k, Resource.from_contents(v)) for k, v in _docs.items()])


def validate(schema_id, pointer, instance):
    root = _docs[schema_id]
    sch = {"$ref": schema_id + pointer} if pointer else {"$ref": schema_id}
    v = Draft202012Validator(sch, registry=REG)
    errs = sorted(v.iter_errors(instance), key=lambda e: list(e.path))
    return [f"{list(e.path)}: {e.message}" for e in errs]


CLASS_EXIT = D9["classToExitCode"]

# ================================================== D-1  the ORIGINAL invocation
CMD = {c["name"]: c for c in INVENTORY["commands"]}
DEFAULT_CMD = CMD["default"]
V["WF-1-what-the-ORIGINAL-invocation-discloses"] = {
    "command": DEFAULT_CMD["cli"], "requestClass": DEFAULT_CMD["requestClass"],
    "authority": DEFAULT_CMD["authority"], "steps": DEFAULT_CMD["steps"],
    "formats": DEFAULT_CMD["formats"], "parityFields": DEFAULT_CMD["parityFields"],
    "writesTrackedIntent": DEFAULT_CMD["writesTrackedIntent"],
    "firstSourceWrite": DEFAULT_CMD["firstSourceWrite"],
    "repositoryExecution": DEFAULT_CMD["repositoryExecution"],
    "boundedCardinality": {"stepsPerInvocation": 64, "attemptsPerStep": 3,
                           "stagesPerAttempt": 1024,
                           "availabilityStepsMax": 64,
                           "availabilityNoticesPerStepMax": 1024,
                           "requestedCapabilitiesMax": 1024,
                           "workspaceRootsMax": 1024,
                           "discoveryFirstPartyUnitCap": 4096},
    "ordering": {"stepDag": "ordered acyclic, dependsOn names LOWER StepIds only",
                 "availabilityNotices": "x-opensip-order sequence, the selection's own order",
                 "activePins": "x-opensip-order by pinId"},
    "retention": "DEFAULTED durable-unbounded (CD-RT-5), disclosed with the storage root "
                 "BEFORE the first source-derived write; no policy file is written",
    "commandsInTheClosedInventory": len(INVENTORY["commands"]),
    "commandsAdvertisingSARIF": sorted(c["name"] for c in INVENTORY["commands"]
                                       if "sarif" in c.get("formats", []))}

# ============================ D-2  zero-config selection when the release lacks rows
MATRIX_CAPS = {c["id"]: c for c in MATRIX["capabilities"]}
CELLS = {(c["capability"], c["mode"]): c["state"] for c in MATRIX["cells"]}
MODES = list(MATRIX["languageModes"])


def required_default(mode):
    """The default profile is fixed BY THE MATRIX, not by the release registry:
    every capability whose (capability, mode) cell is not NOT-SELECTED."""
    return sorted(cid for cid in MATRIX_CAPS
                  if CELLS[(cid, mode)] != "NOT-SELECTED")


UNITS = [{"workspaceRoot": "apps/web", "languageMode": "ts-tsconfig"},
         {"workspaceRoot": "apps/legacy", "languageMode": "js-synthesized"},
         {"workspaceRoot": "services/api", "languageMode": "rust-cargo"},
         {"workspaceRoot": "docs", "languageMode": "syntax-only"}]

# an installed release that does NOT declare everything (incl. a candidate-only one)
RELEASE_ROWS = [
    {"capabilityId": cid, "languageModes": [m for m in MODES
                                            if CELLS[(cid, m)] != "NOT-SELECTED"]}
    for cid in sorted(MATRIX_CAPS)
    if cid not in {"clones-near", "clones-cross-tsjs", "unresolved-edge"}]
DECLARED = {r["capabilityId"]: set(r["languageModes"]) for r in RELEASE_ROWS}


def select(step_id, units):
    requested, notices = [], []
    for u in units:
        for cid in required_default(u["languageMode"]):
            requested.append({"capabilityId": cid, "languageMode": u["languageMode"],
                              "workspaceRoot": u["workspaceRoot"], "required": True})
            if u["languageMode"] not in DECLARED.get(cid, set()):
                notices.append({"code": "native.capability-unavailable",
                                "capabilityId": cid, "languageMode": u["languageMode"],
                                "workspaceRoot": u["workspaceRoot"],
                                "remedy": "install or enable the provider release that "
                                          "declares this capability"})
    return requested, {"stepId": step_id, "noticeCount": len(notices), "notices": notices}


REQ0, STEP0 = select(0, UNITS)
REQ2, STEP2 = select(2, [UNITS[0], UNITS[2]])     # a DIFFERENT selection at step 2
AVAIL_SINGLE = {"stepCount": 1, "totalNoticeCount": STEP0["noticeCount"],
                "steps": [STEP0]}
AVAIL_MULTI = {"stepCount": 2, "totalNoticeCount": STEP0["noticeCount"] + STEP2["noticeCount"],
               "steps": [STEP0, STEP2]}

V["WF-2-zero-config-selection-with-an-incomplete-release-declaration"] = {
    "matrixCapabilityIds": sorted(MATRIX_CAPS),
    "capabilityIdIsNotARelationAtRung": {
        cid: MATRIX_CAPS[cid].get("relations", []) for cid in sorted(MATRIX_CAPS)},
    "notSelectedCells": sorted(f"{c}@{m}" for (c, m), s in CELLS.items()
                               if s == "NOT-SELECTED"),
    "requiredDefaultPerMode": {m: required_default(m) for m in MODES},
    "unitsDiscovered": UNITS,
    "requestedRowsSingleStep": len(REQ0),
    "undeclaredByThisRelease": sorted({"clones-near", "clones-cross-tsjs", "unresolved-edge"}),
    "singleStepAvailability": AVAIL_SINGLE,
    "multiStepAvailability": AVAIL_MULTI,
    "differentSelectionsAtDifferentSteps": {
        "step0Units": [u["workspaceRoot"] for u in UNITS],
        "step2Units": [UNITS[0]["workspaceRoot"], UNITS[2]["workspaceRoot"]]},
    "sameOwnershipTupleMayRecurAcrossSteps": True,
    "candidateOnlyCapabilitiesHaveNoCoverageEntry": {
        cid: (MATRIX_CAPS[cid].get("relations", []) == [])
        for cid in ("clones-near", "clones-cross-tsjs")},
    "candidateOnlyProjection": "selection-account-only  (their ONLY public route is "
                               "CommandEnvelope.availability; requiring a Coverage entry "
                               "would mean fabricating a relation)",
    "factProducingProjection": "coverage-entry",
    "precedenceWhenBothApply": "language-tier-unsupported / capability-missing OUTRANKS "
                               "provider-unavailable / capability-missing (sec.10 precedence), "
                               "so `references` under syntax-only keeps the more specific pair",
    "productPromiseVsInstalledAvailability":
        "the default REQUEST is fixed by the matrix and does not shrink with the release; "
        "the release declaration states AVAILABILITY only and never scope",
    "explicitOverride": "product-configuration.analysis.capabilities overrides the REQUEST "
                        "with its own provenance; the default's provenance is DEFAULTED",
    "semanticPrerequisite": "a capability the admitted universe cannot serve is answered by "
                            "the Coverage pair, not by the availability account",
    "availabilityIsADeclaredParityFieldOfEveryAnalysisCommand": sorted(
        c["name"] for c in INVENTORY["commands"]
        if "capability-availability" in c.get("parityFields", [])),
    "schemaErrors_single": validate("urn:opensip:product-v1:workflows:common",
                                    "#/$defs/CapabilityAvailabilityV1", AVAIL_SINGLE),
    "schemaErrors_multi": validate("urn:opensip:product-v1:workflows:common",
                                   "#/$defs/CapabilityAvailabilityV1", AVAIL_MULTI)}

# ======================================= D-3  public failure envelopes, four origins
def envelope(kind, req_id, termination, errors=None, extra=None):
    e = {"schemaFamily": "opensip.product.envelope", "schemaMajor": 2, "kind": kind,
         "requestId": req_id, "termination": termination,
         "exitCode": CLASS_EXIT[termination["class"]]}
    if errors is not None:
        e["errors"] = errors
    if extra:
        e.update(extra)
    return e


REQ_ID = "req1_" + "a1" * 16


def failure_envelope(name, termination, envelope_detail):
    """failure_envelope_errors: where the termination carries a detail, errors IS
    exactly that detail; where it does not, the route's own envelopeDetail supplies one."""
    errs = [termination["domainDetail"]] if "domainDetail" in termination else [envelope_detail]
    env = envelope("failure", REQ_ID, termination, errs)
    return {"termination": termination, "envelope": env,
            "errorsEqualsTerminationDetail": ("domainDetail" in termination
                                              and errs[0] == termination["domainDetail"]),
            "schemaErrors": validate("urn:opensip:product-v1:workflows:command-envelope",
                                     "", env)}


ROUTES = {}
# (a) EXTERNAL CONFIGURATION: a capability the user configured is unregistered
ROUTES["WF-3a-external-configuration-capability-spec-invalid"] = failure_envelope(
    "a",
    {"class": "request-rejected", "errorCode": "CONFIG.INVALID",
     "domainDetail": {"code": "CONFIG.INVALID",
                      "remedy": "remove the unregistered capability from "
                                "analysis.capabilities",
                      "subject": "native.requested-capability-unregistered:made-up-capability"}},
    None)
# (b) RETAINED / EXTERNALLY SUPPLIED spec, origin known external: no public detail
ROUTES["WF-3b-externally-supplied-retained-spec"] = failure_envelope(
    "b",
    {"class": "request-rejected", "errorCode": "REQUEST.PRECONDITION_FAILED"},
    {"code": "native.capability-spec-invalid",
     "remedy": "supply an analysis specification whose capabilities are registered",
     "subject": "native.requested-capability-unregistered:made-up-capability"})
# (c) HOST-GENERATED INVALID INTERNAL RECORD: operational-failed / host-invariant
ROUTES["WF-3c-host-generated-invalid-internal-record"] = failure_envelope(
    "c",
    {"class": "operational-failed", "errorCode": "SYSTEM.OUTCOME.ILLEGAL_STATE",
     "faultCause": "host-invariant"},
    {"code": "HOST.INVARIANT_VIOLATED",
     "remedy": "report the defect with the request id; the host minted an invalid "
               "analysis specification",
     "subject": "native.requested-capability-unregistered:made-up-capability"})
# (d) PRODUCER BOUNDARY failure: Coverage cause/carrier violation
ROUTES["WF-3d-producer-boundary-coverage-cause-violation"] = failure_envelope(
    "d",
    {"class": "operational-failed", "errorCode": "PROVIDER.PROTOCOL_VIOLATION",
     "faultCause": "provider-protocol"},
    {"code": "native.coverage-cause-unsupported",
     "remedy": "the provider emitted an unsupported deficiency/cause pair; update the provider",
     "subject": "native.coverage-cause-not-for-deficiency:"
                "input-closure-incomplete:capability-missing"})
V["WF-3-public-failure-envelopes-from-an-internal-refusal-and-its-origin"] = ROUTES

# bounded diagnostic subject
def bounded_subject(raw_subject):
    if len(raw_subject) <= 1024:
        return raw_subject
    marker = "...#sha256:"
    keep = 1024 - len(marker) - 64
    return (raw_subject[:keep] + marker
            + hashlib.sha256(raw_subject.encode("utf-8")).hexdigest())


_long = "native.requested-capability-mode-unregistered:" + ("m" * 4096)
_b = bounded_subject(_long)
V["WF-4-bounded-diagnostic-subject"] = {
    "rawScalarLength": len(_long), "boundedScalarLength": len(_b),
    "boundedIsExactly1024": len(_b) == 1024,
    "registeredKeyPreservedVerbatim": _b.startswith(
        "native.requested-capability-mode-unregistered:"),
    "digestOfUntruncatedUtf8": hashlib.sha256(_long.encode("utf-8")).hexdigest(),
    "unitsAreUnicodeCodePointsNotUtf8Bytes": True,
    "codeClassAndOriginUnchangedByTheElision": True,
    "boundedSubjectTail": _b[-90:],
    "schemaErrors": validate("urn:opensip:product-v1:workflows:common",
                             "#/$defs/DomainDetail",
                             {"code": "native.capability-spec-invalid",
                              "remedy": "narrow the request", "subject": _b})}

# ======================================================= D-4  pinned purge refusal
PINS = sorted([{"pinId": "baseline:main", "kind": "baseline"},
               {"pinId": "backup:2026-09-01", "kind": "backup-export"},
               {"pinId": "repair:rp-17", "kind": "repair-prerequisite"}],
              key=lambda p: p["pinId"].encode())
DISCLOSURE = {"runId": RUN_ID, "activePins": PINS,
              "consequences": ["named-pins-revoked",
                               "dependent-evidence-replay-unavailable",
                               "sealed-history-retained"]}
PURGE_TERM = {"class": "request-rejected", "errorCode": "REQUEST.PRECONDITION_FAILED",
              "domainDetail": {"code": "evidence.pinned",
                               "remedy": "revoke the named pins under lifecycle "
                                         "authorization, or purge a Run that is not pinned",
                               "subject": RUN_ID, "purgeDisclosure": DISCLOSURE}}
PURGE_ENV = envelope("failure", REQ_ID, PURGE_TERM, [PURGE_TERM["domainDetail"]])
V["WF-5-complete-pinned-purge-refusal"] = {
    "owner": "foundation-owned detail evidence.pinned (identity sec.5); "
             "workflows sec.12 specifies the projection",
    "projection": {"class": "request-rejected", "errorCode": "REQUEST.PRECONDITION_FAILED",
                   "exit": 2, "detail": "evidence.pinned"},
    "disclosure": DISCLOSURE,
    "pinsSortedUniquelyByPinId": [p["pinId"] for p in PINS],
    "noPinOmittedTruncatedOrAggregatedIntoACount": True,
    "threeOrderedConsequences": DISCLOSURE["consequences"],
    "detailInBothTerminationAndErrors": PURGE_ENV["errors"][0] == PURGE_TERM["domainDetail"],
    "disclosureConfersNoAuthority": "a later destructive attempt still requires the explicit "
                                    "lifecycle authorization and disclosure of its THEN-CURRENT "
                                    "complete pin set; a changed inventory requires renewed "
                                    "disclosure before destruction",
    "bounds": {"pinIdMaxScalars": 256, "activePinsMaxPerRun": 4096},
    "envelope": PURGE_ENV,
    "schemaErrors": validate("urn:opensip:product-v1:workflows:command-envelope", "", PURGE_ENV)}

# negative: a schema-valid SUBSET of the observed pin set
V["WF-5N-a-schema-valid-subset-does-not-satisfy-the-completeness-obligation"] = {
    "observedUnderTheExclusivePurgeLease": [p["pinId"] for p in PINS],
    "disclosedSubset": [PINS[0]["pinId"]],
    "schemaErrors": validate("urn:opensip:product-v1:workflows:common",
                             "#/$defs/PinnedPurgeDisclosure",
                             dict(DISCLOSURE, activePins=[PINS[0]])),
    "schemaAcceptsIt": True,
    "hostObligation": "the host compares the disclosed named pins with the COMPLETE current "
                      "set observed under the exclusive lease before emitting the refusal; "
                      "validate_pinned_purge_refusal cannot establish inventory completeness "
                      "without the host ledger. This is a stated host responsibility, not a "
                      "schema-decidable property."}

# ==================================== D-5  mutation replay scope vs repair-apply key
MUT_SCOPE = {"schemaVersion": 1, "requestId": REQ_ID, "stepId": 3,
             "projectId": PROJECT_ID, "operation": "waiver-change"}
MUT_KEY = H("workflow.mutation-intent", MUT_SCOPE)
_other_req = dict(MUT_SCOPE, requestId="req1_" + "b2" * 16)
REPAIR_PLAN_ID = "repairplan2:" + "3c" * 32
REPAIR_KEY = raw({"operation": "repair-apply", "projectId": PROJECT_ID,
                  "repairPlanId": REPAIR_PLAN_ID, "baseSnapshotId": SNAP_ID})
V["WF-6-generic-mutation-replay-scope-vs-the-repair-apply-key"] = {
    "genericMutation": {
        "retainedScope": MUT_SCOPE,
        "closedFieldSet": ["schemaVersion", "requestId", "stepId", "projectId", "operation"],
        "operationEqualsMutationParamsMutationClass": True,
        "recipe": 'bare 64-hex H("workflow.mutation-intent", MutationReplayScopeV1)',
        "idempotencyKey": MUT_KEY,
        "isOperationalNotContentDerived": True,
        "aDifferentFreshRequestNeverDeduplicates":
            H("workflow.mutation-intent", _other_req) != MUT_KEY,
        "otherRequestKey": H("workflow.mutation-intent", _other_req),
        "receiptLookupIsNotAnEffectAuthorization": True,
        "repairApplyIsExcludedFromMutationClass": True,
        "schemaErrors": validate("urn:opensip:product-v1:workflows:invocation-record",
                                 "#/$defs/MutationReplayScopeV1", MUT_SCOPE)},
    "repairApply": {
        "recipe": 'raw SHA-256 of C({operation:"repair-apply", projectId, repairPlanId, '
                  'baseSnapshotId})  - CONTENT-derived, not H, and a DEDICATED step',
        "preimage": {"operation": "repair-apply", "projectId": PROJECT_ID,
                     "repairPlanId": REPAIR_PLAN_ID, "baseSnapshotId": SNAP_ID},
        "idempotencyKey": REPAIR_KEY,
        "differsFromTheGenericRecipe": REPAIR_KEY != MUT_KEY,
        "equalCompletedKeyPerformsNoSecondEffect": True,
        "replayProducesASeparatelyIdentifiedReceiptWithReplayedTrue": True,
        "originalReceiptImmutable": True},
    "distinctionInOneSentence":
        "the generic key is OPERATIONAL and scoped to one host-minted request/step, so two "
        "fresh requests never deduplicate each other; the repair-apply key is CONTENT-derived "
        "over the plan and base snapshot, so an equal completed key across requests is a "
        "lawful replay with no second effect."}

# ================================ D-6  the ScopeDocumentV1 comparison axis (E2->E3)
SCOPE_DOC_A = {"schemaFamily": "opensip.product.scope", "schemaMajor": 1,
               "include": ["src/**"], "exclude": ["src/generated/**"]}
SCOPE_DOC_B = {"schemaFamily": "opensip.product.scope", "schemaMajor": 1,
               "include": ["src/**"], "exclude": []}
SCOPE_DOC_A_D = S.put_record(SCOPE_DOC_A, "ScopeDocumentV1 A")
SCOPE_DOC_B_D = S.put_record(SCOPE_DOC_B, "ScopeDocumentV1 B")
POLICY_DOC_BYTES_DIGEST = rawbytes(load("docs/coop/design-corrections/workflows/schemas/"
                                        "policy-document.schema.json"))
PARAM_ROW_A = {"schemaDigest": POLICY_DOC_BYTES_DIGEST, "payloadDigest": SCOPE_DOC_A_D}
PARAM_ROW_B = {"schemaDigest": POLICY_DOC_BYTES_DIGEST, "payloadDigest": SCOPE_DOC_B_D}

SPEC_A = {"schemaVersion": 2, "requestedCapabilities": [], "policyPackIds": ["pack.default"],
          "parameters": [PARAM_ROW_A]}
SPEC_B = {"schemaVersion": 2, "requestedCapabilities": [], "policyPackIds": ["pack.default"],
          "parameters": [PARAM_ROW_B]}
SPEC_A_D, SPEC_B_D = S.put_record(SPEC_A, "spec A"), S.put_record(SPEC_B, "spec B")

CTX_PRIOR = {"policyDigest": POLICY_DIGEST, "scopeDigest": SCOPE_DOC_A_D,
             "waiverSetDigest": WAIVER_DIGEST,
             "detectorClosureIds": ["closure2:" + "7d" * 32],
             "evidenceAvailability": {"importKinds": [], "relations": [], "imports": []}}
CTX_CURRENT = dict(CTX_PRIOR, scopeDigest=SCOPE_DOC_B_D)

V["WF-7-scope-policy-parameter-binding-and-the-E2-to-E3-comparison-axis"] = {
    "registeredParameterRow": {
        "class": "parameter", "keyedBy": "the cited schemaDigest (the DOCUMENT digest)",
        "document": "workflows/schemas/policy-document.schema.json",
        "selector": "#/$defs/ScopeDocumentV1",
        "documentDigest": POLICY_DOC_BYTES_DIGEST},
    "boundParameterRowPrior": PARAM_ROW_A, "boundParameterRowCurrent": PARAM_ROW_B,
    "scopeDocumentPrior": SCOPE_DOC_A, "scopeDocumentCurrent": SCOPE_DOC_B,
    "analysisSpecDigestPrior": SPEC_A_D, "analysisSpecDigestCurrent": SPEC_B_D,
    "onlyTheScopePOLICYChanges": {
        "policyDigestEqual": CTX_PRIOR["policyDigest"] == CTX_CURRENT["policyDigest"],
        "waiverDigestEqual": CTX_PRIOR["waiverSetDigest"] == CTX_CURRENT["waiverSetDigest"],
        "detectorsEqual": CTX_PRIOR["detectorClosureIds"] == CTX_CURRENT["detectorClosureIds"],
        "scopeDigestChanged": CTX_PRIOR["scopeDigest"] != CTX_CURRENT["scopeDigest"]},
    "axis": "E2 -> E3 (scope)", "classification": "SCOPE-DELTA",
    "distinctFromDiscoveryScope": {
        "planScopeDigest_namesTheFoundationScopeDescriptor":
            "the repository extent actually walked: workspaceRoots / pathPrefixes / "
            "excludedPathPrefixes",
        "comparisonScopeDigest_namesScopeDocumentV1":
            "the operator's include/exclude GLOB policy over that extent",
        "neitherSubstitutesForTheOther": True,
        "bothMayAppearInOnePlan": True},
    "verifierPrecondition":
        "adopt_baseline is a PURE PROJECTION over documents the caller must already have "
        "admitted; with the retained analysis spec supplied it verifies that the scope "
        "document's canonical digest is the payloadDigest of a SELECTED parameter row citing "
        "the registered ScopeDocumentV1 document digest. Without the spec the scope binding "
        "is a CALLER ASSERTION and the contract says so rather than implying a join.",
    "boundedLimitation": "the class is keyed by the DOCUMENT digest, so a future second "
                         "parameter row selecting another $def out of policy-document.schema.json "
                         "refuses PAYLOAD_PARAMETER_AMBIGUOUS_ROW rather than being chosen "
                         "arbitrarily. Today's two rows are distinguishable.",
    "scopeDocumentSchemaErrorsA": validate(
        "urn:opensip:product-v1:workflows:policy-document", "#/$defs/ScopeDocumentV1", SCOPE_DOC_A),
    "evaluationContextSchemaErrors": validate(
        "urn:opensip:product-v1:workflows:comparison-result", "#/$defs/EvaluationContext",
        CTX_CURRENT)}

# ================================================== D-7  the selected D9 extension
FCM = D9["codeMaps"]["faultCauseToErrorCode"]
SUCCESSOR_FCM = dict(FCM, **{"host-invariant": "SYSTEM.OUTCOME.ILLEGAL_STATE"})
COMMON = json.load(open(os.path.join(WF, "common.schema.json")))
V["WF-8-selected-D9-extension-checked-against-the-inherited-contract"] = {
    "inheritedArtifact": "docs/coop/artifacts/d9-exit-contract.v1.14.json (bytes unchanged)",
    "inheritedFaultCauseCount": len(FCM),
    "successorFaultCauseCount": len(SUCCESSOR_FCM),
    "addedMember": "host-invariant -> SYSTEM.OUTCOME.ILLEGAL_STATE",
    "errorCodeIsAlreadyInTheInheritedCLOSEDVocabulary":
        "SYSTEM.OUTCOME.ILLEGAL_STATE" in D9["codeVocabulary"]["errorCodes"],
    "itHadNoCausePreimageInEitherInheritedMap":
        "SYSTEM.OUTCOME.ILLEGAL_STATE" not in set(FCM.values())
        and "SYSTEM.OUTCOME.ILLEGAL_STATE" not in set(
            D9["codeMaps"]["rejectionCauseToErrorCode"].values()),
    "codeMapsRuleIsAboutTheDECLAREDCAUSEDOMAIN": D9["codeMaps"]["rule"],
    "successorMapStillInjective":
        len(set(SUCCESSOR_FCM.values())) == len(SUCCESSOR_FCM),
    "successorMapStillTotalOverTheCauseDomain": True,
    "noNewClassExitReasonOrErrorCode": {
        "classes": D9["exitClasses"] if isinstance(D9.get("exitClasses"), list) else list(CLASS_EXIT),
        "classToExitCode": CLASS_EXIT,
        "errorCodesUnchanged": sorted(COMMON["$defs"]["D9ErrorCode"]["enum"])
                               == sorted(D9["codeVocabulary"]["errorCodes"]),
        "reasonCodesUnchanged": sorted(COMMON["$defs"]["D9ReasonCode"]["enum"])
                                == sorted(D9["codeVocabulary"]["reasonCodes"])},
    "declaredPrecedence": D9["causeModel"]["precedence"],
    "precedenceRespectedByTheOriginRouting":
        "a host-generated invalid internal record is a faultCause, which by the inherited "
        "precedence (faultCause > rejectionCause > deficiency) dominates the request rejection "
        "the same malformed record would otherwise produce - so routing it to operational-failed "
        "rather than request-rejected is what the inherited precedence already requires",
    "exclusivityRespected": "each example termination carries at most ONE cause family",
    "itIS_a_vocabularyExtension": "faultCause grows by one member; the successor contract says "
                                  "so explicitly rather than claiming nothing changed",
    "residualObligation": "publishing the successor D9 ARTIFACT belongs to the D9 unit; the "
                          "inherited v1.14 bytes still omit the member, so a checker reading "
                          "the artifact alone would refuse a lawful host-invariant termination"}

# ==================================== D-8  required-output failure after commit
DELIV_TERM = {"class": "operational-failed", "errorCode": "DELIVERY.REQUIRED_FAILED",
              "faultCause": "delivery-required", "runId": RUN_ID,
              "domainDetail": {"code": "DELIVERY.RENDERER_FAILED_AFTER_COMMIT",
                               "remedy": "re-render from the committed Run; the Run is not "
                                         "rewritten", "subject": RUN_ID}}
DELIV_ENV = envelope("failure", REQ_ID, DELIV_TERM, [DELIV_TERM["domainDetail"]])
V["WF-9-required-output-failure-after-a-committed-run"] = {
    "termination": DELIV_TERM, "exitCode": DELIV_ENV["exitCode"],
    "runIdRetained": True, "runNotRewritten": True,
    "aMissingParityFieldIsThisSameFault":
        "the host projection must be TOTAL over the selected command's parityFields before a "
        "renderer consumes it; a missing field or a projection exception is a required-delivery "
        "operational fault, never an empty result or a successful partial rendering",
    "anEmptyFindingsArrayIsARealEmptyResult": True,
    "optionalExportSinkFailureLeavesSuccess": True,
    "nonApplicableFormat": {"class": "request-rejected", "errorCode": "REQUEST.UNKNOWN_OPTION",
                            "detail": "OUTPUT.FORMAT_NOT_APPLICABLE", "exit": 2},
    "schemaErrors": validate("urn:opensip:product-v1:workflows:command-envelope", "", DELIV_ENV)}

# =========================== D-9  test / preparation / repair authorization boundary
V["WF-10-explicit-test-preparation-and-repair-authorization"] = {
    "testExecution": {
        "step": "test-execution (request class `execution`), retryPolicy=none, NO Plan",
        "requires": ["security RepoExecutionGrantV2, principal repository-code, "
                     "workflow spelling P-TRUSTED-REPO, execution class test-runner",
                     "bound to this project, snapshot digest and the exact argv digest",
                     "argv[0] a LogicalPath member of the sealed snapshot or of the declared "
                     "toolchain closure2 (TEST.ARGV_NOT_IN_CLOSURE)",
                     "allowlisted environment; PATH never copied (TEST.ENV_NOT_ALLOWLISTED)",
                     "CI uses a pre-existing policy record (TEST.INTERACTIVE_CONSENT_IN_CI)"],
        "ownersIsEmptyAndOwnerSourceDigestIsTheEmptyArrayDigest":
            raw([]) [:12] + "... (canonical empty-owner bookkeeping; binds nothing)",
        "emptyOwnerArrayDigest": raw([]),
        "outcome": "a TestPayloadV1 wrapped as an import2 of kind `test` - evidence, never "
                   "Coverage and never a verdict",
        "testCodeIsNotAnAnalysisSemanticGrantOperation": True,
        "confinement": "DISCLOSURE-ONLY unless the security platform truth table measures a "
                       "primitive; a claimed enforcement without one refuses "
                       "TEST.CONFINEMENT_CLAIM_REFUSED"},
    "preparation": {
        "step": "native-preparation, retryPolicy=none, returns a receipt and ONE admitted "
                "prepared import, never a Run",
        "grantOperationProjection": {"host-prepared": "prepare-code",
                                     "imported-inert": "read-import", "none": None},
        "authorizationRefIsExcludedFromThePlanDescriptor": True,
        "planTimeJoin": "admit_plan_execution_projection requires the plan2 semantic grant to "
                        "project EXACTLY the trusted-repository-code principals of the consumed "
                        "preparation grants; a test-runner grant offered as a consumed grant "
                        "refuses PLAN.TEST_RUNNER_HAS_NO_PLAN"},
    "repairApply": {
        "authorization": "security RepairApplyAuthorizationV1, bound to the exact repairPlanId, "
                         "baseSnapshotId and projectId; repositoryExecution is the constant false",
        "isNotARepositoryExecutionGrant": True,
        "closedWorldGate": "EVERY delete and EVERY replace edit requires the evidence Run's own "
                           "ClosedWorldV2.deadCodeRepairEligible; an imported-prepared-declared "
                           "origin reports REPAIR.CLOSED_WORLD_NOT_ESTABLISHED",
        "descriptorProjectionIsFiveFields": ["deadCodeRepairEligible", "exportsClosed",
                                             "entryPointsRecognized", "nonliteralLoading",
                                             "externalConsumers"],
        "droppedFromTheProjection": ["dynamicDispatch", "reasons"],
        "authorityBoundary": "the projection grants NO evidence authority of its own; the whole "
                             "descriptor is the preimage of repairPlanId and apply requires an "
                             "authorization bound to that exact id, so no edit to the projection "
                             "can make a plan applicable. The authority stays the sealed Run "
                             "named by evidenceRunId, INCLUDING the two members the descriptor "
                             "does not carry.",
        "dynamicDispatchIsNotAGlobalVeto": "affected_targets makes a dynamic edge TARGET-RELATIVE; "
                                           "it disqualifies claims about the subjects it reaches, "
                                           "not an unrelated target in the same Run",
        "perTargetRequirement": "preview ADMITS each EvidenceRequirement's relation/minResolution "
                                "against the registered vocabulary and that relation's own ladder, "
                                "then CONSUMES that requirement's own `satisfied` value; the "
                                "semantic sufficiency is native sufficiency_v2's, per requirement",
        "importedObservationBoundary": "an imported runtime/test/history observation is advisory: "
                                       "observable-unhit is bounded negative evidence with its "
                                       "window and population, never universal non-use, and never "
                                       "OpenSIP Coverage",
        "verify": "always admits a FRESH snapshot after apply; a differing snapshot is "
                  "REQUEST.PRECONDITION_FAILED / REPAIR.SOURCE_MOVED and seals no Run"}}


# ============== D-10  the command -> mutationClass mapping is not published
MUTOPS = json.load(open(os.path.join(WF, "repair.schema.json")))["$defs"]["MutationOperation"]["enum"]
MUT_CMDS = [c["name"] for c in INVENTORY["commands"] if c["requestClass"] == "mutation"]
V["WF-11-command-name-to-mutationClass-mapping"] = {
    "mutationOperationEnum": MUTOPS,
    "mutationClassCommands": MUT_CMDS,
    "commandRecordFields": sorted({k for c in INVENTORY["commands"] for k in c}),
    "commandRecordCarriesNoMutationClassField": "mutationClass" not in {
        k for c in INVENTORY["commands"] for k in c},
    "commandsWithNoSameNamedOperation": sorted(set(MUT_CMDS) - set(MUTOPS)),
    "inferredButUnpublished": {"waive": "waiver-change", "policy-init": "policy-write",
                               "baseline-upgrade": "baseline-upgrade-apply"},
    "whyItMatters": "mutationClass is a PUBLIC envelope field and MutationReplayScopeV1.operation "
                    "equals it, so it enters the H(\"workflow.mutation-intent\", scope) preimage "
                    "of the published idempotencyKey. No document maps the closed command name "
                    "vocabulary onto the closed MutationOperation vocabulary.",
    "boundedImpact": "requestId is host-minted and unique per invocation, so a spelling difference "
                     "cannot cause a false dedupe or a missed dedupe ACROSS hosts, and the key "
                     "grants no authority. The gap is that a consumer reading a public envelope "
                     "cannot derive the expected mutationClass for three of the ten mutation "
                     "commands from the contracts alone."}
