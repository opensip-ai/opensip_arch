#!/usr/bin/env python3
"""Retained checker for the operability contract.

The checker deliberately separates four claims:

  OP-SUBJ   gate class and subject agree
  OP-QUAL   assurance state is supported by retained evidence identities
  OP-REL    the required-property registry is closed and release is derived
  OP-ID     event identities and budgets are lifecycle-phase correct
  OP-PAR    every surface has a typed field map and executable loss fixtures
  OP-AUD    host audit schema/protocol survives crash and redaction controls
  OP-CAP    resource capacity and split authority/fault targets are concrete
  OP-TM     exact threat-property and citation joins resolve
  OP-REQID  RequestId has one host-owned allocation/validation lifecycle,
            collision protocol, custody rule, and semantic exclusion

Usage: python3 artifacts/check-operability.py [contract] [--selftest]
"""
from __future__ import annotations

import copy
import json
import pathlib
import re
import sys

BINDING = "operability.v2.json"
C2 = "c2-plan-stage-schema.v3.json"
TM = "threat-model.v3.json"
RESOLVED_INPUTS = "resolved-inputs.v2.json"
D9 = "d9-exit-contract.v1.6.json"
FACT_PLANE = "fact-plane.v1.json"
FACT_IDENTITY = "fact-identity-policy.v2.json"
EVIDENCE = "evidence.v1.json"
EVIDENCE_DEFERRED = "identity-contracts.evidence-requestid-closure.deferred-patch.v1.json"
R1 = "r1-lifetime-neutrality.conformance.v1.4.json"
HERE = pathlib.Path(__file__).resolve().parent
TOTALITY_ROOT_CASES = (
    ("string", "hostile-root"),
    ("null", None),
    ("list", []),
    ("empty-object", {}),
)
MALFORMED_SHAPE_EXCEPTIONS = (
    AttributeError, IndexError, KeyError, StopIteration, TypeError, ValueError,
)

STATES = {"SPECIFIED", "IMPLEMENTABLE", "QUALIFIED", "DEMONSTRATED",
          "BLOCKED-NO-MECHANISM", "PARTIAL"}
CLASSES = {"design-integrity": "architecture",
           "implementation-conformance": "product"}
FIELDS = {"verdict", "termination", "findings", "severity", "coverage",
          "artifacts", "identities"}
SURFACES = {"json", "exit-code", "human-terminal", "sarif", "agent-mcp"}
LOCAL_PROPERTIES = {"OP.TERMINATION", "OP.COVERAGE", "OP.PROJECTION", "OP.AUDIT",
                    "OP.CORE-CLOSURE", "OP.PROVIDER-FAULT", "OP.DELIVERY"}
EXPECTED_CHECKERS = {
    "artifacts/check-claims.py", "artifacts/check-d9.py",
    "artifacts/check-fact-plane.py", "artifacts/check-c2.py",
    "artifacts/check-evidence.py", "artifacts/check-resolved-inputs.py",
    "artifacts/check-fact-identity.py", "artifacts/check-versioning.py",
    "artifacts/check-operability.py", "artifacts/check-delivery.py",
    "artifacts/check-threat-claims.py", "artifacts/check-r1.py",
}
REQUEST_ID_RE = re.compile(r"^req1_[0-9a-f]{32}$")
REQUEST_NEGATIVES = {
    "request-id-reject-caller-supplied": "REQUEST_ID_CALLER_SUPPLIED",
    "request-id-reject-uppercase": "REQUEST_ID_INVALID_REPRESENTATION",
    "request-id-reject-late-allocation": "REQUEST_ID_ALLOCATION_ORDER_VIOLATION",
    "request-id-reject-collision-exhaustion-as-request": "REQUEST_ID_ALLOCATION_FAILED",
    "request-id-reject-semantic-participation": "REQUEST_ID_SEMANTIC_EXCLUSION_VIOLATION",
}
REQUEST_EXCLUSIONS = {
    "SnapshotId preimage",
    "PlanId preimage",
    "fact identity and fingerprints",
    "FactViewId",
    "EvidenceDigest and evaluation proofs",
    "RunId derivation",
    "sealed Run semantic manifest",
    "Coverage, findings, verdict, policy and termination derivation",
    "cache and regeneration keys",
}
REQUEST_MECHANICAL_JOINS = {
    "SnapshotDescriptorV1",
    "PlanDescriptorV1",
    "C-2 PlanIntent and ExecutionPlan",
    "FactEnvelope, FactRecordV1 and normalized body identity",
    "pure-core serialized input and completion",
    "D9 termination derivation axes",
}
REQUEST_MECHANICAL_JOIN_SOURCES = {
    "SnapshotDescriptorV1": {
        "resolved-inputs.v2.json#snapshotIdContract.descriptorSchema",
    },
    "PlanDescriptorV1": {
        "resolved-inputs.v2.json#planIdContract.preimageFields",
        "resolved-inputs.v2.json#planIdContract.excludedIdentitiesAndInputs",
    },
    "C-2 PlanIntent and ExecutionPlan": {
        "c2-plan-stage-schema.v3.json#planIntent",
        "c2-plan-stage-schema.v3.json#executionPlan.requiredFields",
    },
    "FactEnvelope, FactRecordV1 and normalized body identity": {
        "fact-plane.v1.json#factEnvelope.fields",
        "fact-plane.v1.json#factRecordContractV1.factIdContract",
        "fact-plane.v1.json#factRecordContractV1.requestIdInvarianceVector",
        "fact-identity-policy.v2.json#factRecordIdentityBoundaryV1",
    },
    "pure-core serialized input and completion": {
        "r1-lifetime-neutrality.conformance.v1.4.json#coreApi",
        "r1-lifetime-neutrality.conformance.v1.4.json#coreCompletionSchema",
    },
    "D9 termination derivation axes": {
        "d9-exit-contract.v1.6.json#scenarioAxesSchema.properties",
    },
}
REQUEST_PARKED_SURFACES = {
    "finding fingerprint recipe",
    "FactViewId derivation",
    "EvidenceDigest byte recipe",
    "RunId derivation",
    "sealed Run semantic manifest identity",
    "cache and regeneration key recipes",
}
REQUEST_PENDING_CROSS_SURFACES = {
    "EvidenceBundle unknown-field closure",
}
REQUEST_ALLOCATION_TRIGGERS = {
    "CSPRNG_FAILURE", "RESERVATION_IO_FAILURE", "COLLISION_EXHAUSTION",
}


def load(name: str):
    path = HERE / name
    return json.loads(path.read_text()) if path.exists() else None


def _gate_errors(g: dict) -> list[str]:
    errs: list[str] = []
    status = g.get("status")
    if status not in STATES:
        errs.append(f"unknown status '{status}'")
        return errs
    cls = g.get("class")
    if cls not in CLASSES:
        errs.append(f"unknown class '{cls}'")
    elif g.get("subject") != CLASSES[cls]:
        errs.append(f"class '{cls}' requires subject '{CLASSES[cls]}'")
    if status in {"IMPLEMENTABLE", "QUALIFIED", "DEMONSTRATED"}:
        for key in ("target", "positiveCase", "negativeControls"):
            if not g.get(key):
                errs.append(f"{status} lacks {key}")
    if status in {"QUALIFIED", "DEMONSTRATED"}:
        if not g.get("qualificationEvidenceIds"):
            errs.append(f"{status} lacks qualificationEvidenceIds")
        if "observedFailure" in g:
            errs.append("a boolean observedFailure is not retained evidence")
    if status == "DEMONSTRATED" and not g.get("releaseEvidenceIds"):
        errs.append("DEMONSTRATED lacks releaseEvidenceIds")
    if status == "BLOCKED-NO-MECHANISM":
        if g.get("target") is not None or not g.get("blocker"):
            errs.append("BLOCKED-NO-MECHANISM needs target=null and blocker")
    return errs


def _event_errors(event: dict, contract: dict) -> list[str]:
    req = contract["eventSchema"]["phaseRequirements"].get(event.get("phase"))
    if req is None:
        return ["unknown phase"]
    errs: list[str] = []
    request_id = event.get("requestId")
    if not request_id:
        errs.append("RequestId missing")
    elif not REQUEST_ID_RE.fullmatch(request_id):
        errs.append("RequestId is not canonical REQUEST-ID-V1")
    for field in ("executionId", "runId"):
        mode = req[field]
        present = bool(event.get(field))
        if mode == "required" and not present:
            errs.append(f"{field} required")
        if mode == "forbidden" and present:
            errs.append(f"{field} forbidden")
    if event.get("budgetOwner") != req["budgetOwner"]:
        errs.append(f"budgetOwner must be {req['budgetOwner']}")
    return errs


def _request_d9_errors(req: dict, d9: dict | None) -> list[str]:
    if d9 is None:
        return [f"could not load {D9} for REQUEST_ID_ALLOCATION_FAILED join"]
    errors: list[str] = []
    projection = req.get("d9Projection") or {}
    golden = next((item for item in d9.get("goldenCases", [])
                   if item.get("id") == "pre-admission-host-io-failure"), {})
    context = projection.get("allocationFailure") or {}
    if context.get("referenceGoldenId") != "pre-admission-host-io-failure" or \
            context.get("scenarioAxes") != golden.get("scenarioAxes") or \
            context.get("expectedTermination") != golden.get("expectedTermination"):
        errors.append("RequestId allocation failure drifted from live pre-admission host-io golden")
    exit_codes = {item.get("class"): item.get("code") for item in d9.get("exitClasses", [])}
    if context.get("exitCode") != exit_codes.get(
            (context.get("expectedTermination") or {}).get("class")):
        errors.append("RequestId allocation failure has wrong D9 numeric exit code")
    triggers = projection.get("triggerContexts") or {}
    if set(triggers) != REQUEST_ALLOCATION_TRIGGERS or \
            any(value != "allocationFailure" for value in triggers.values()):
        errors.append("CSPRNG/reservation/collision allocation triggers are not total/exact")
    if projection.get("typedOutcome") != "REQUEST_ID_ALLOCATION_FAILED":
        errors.append("RequestId D9 projection does not bind REQUEST_ID_ALLOCATION_FAILED")
    return errors


def _request_semantic_join_errors(req: dict, resolved_inputs: dict | None,
                                  c2: dict | None, d9: dict | None,
                                  fact_plane: dict | None, fact_identity: dict | None,
                                  evidence: dict | None, r1: dict | None) -> list[str]:
    errors: list[str] = []
    live_fact_vector_id = None
    live_fact_ids: list[str] = []
    semantic = req.get("semanticExclusion") or {}
    coverage = semantic.get("proofStatus") or {}
    joined = coverage.get("mechanicallyJoined") or []
    joined_by_surface = {item.get("surface"): item for item in joined}
    if set(joined_by_surface) != REQUEST_MECHANICAL_JOINS or len(joined) != len(joined_by_surface):
        errors.append("RequestId mechanical semantic-join surface set is not exact")
    else:
        for surface, expected_sources in REQUEST_MECHANICAL_JOIN_SOURCES.items():
            item = joined_by_surface[surface]
            sources = item.get("sources") or []
            if set(sources) != expected_sources or len(sources) != len(set(sources)) or \
                    item.get("proof") != "RequestId is structurally absent from this semantic input":
                errors.append(f"RequestId mechanical join for {surface} has stale sources/proof")
    parked = coverage.get("parkedNoExactRecipe") or []
    parked_by_surface = {item.get("surface"): item for item in parked}
    if set(parked_by_surface) != REQUEST_PARKED_SURFACES or \
            any(item.get("status") != "NORMATIVE-EXCLUSION-NOT-MECHANICALLY-PROVEN"
                for item in parked):
        errors.append("RequestId unimplemented identity recipes are not explicitly parked")
    pending = coverage.get("pendingCrossSurfaceClosure") or []
    pending_by_surface = {item.get("surface"): item for item in pending}
    evidence_pending = pending_by_surface.get("EvidenceBundle unknown-field closure") or {}
    if set(pending_by_surface) != REQUEST_PENDING_CROSS_SURFACES or len(pending) != 1 or \
            evidence_pending.get("status") != "PENDING-OWNER-INTEGRATION" or \
            evidence_pending.get("deferredPatch") != \
            f"artifacts/{EVIDENCE_DEFERRED}" or \
            evidence_pending.get("owner") != "Phase-1A evidence/retention repair lane":
        errors.append("RequestId EvidenceBundle closure is not explicitly pending on its owner")
    deferred = load(EVIDENCE_DEFERRED)
    required_changes = (deferred or {}).get("requiredContractChanges") or {}
    deferred_schema = required_changes.get("schema") or {}
    if (deferred or {}).get("status") != "PENDING-EXTERNAL-PHASE1A-OWNER-INTEGRATION" or \
            deferred_schema.get("closed") is not True or \
            deferred_schema.get("additionalProperties") is not False or \
            deferred_schema.get("unknownFieldOutcome") != "EVIDENCE_BUNDLE_UNKNOWN_FIELD" or \
            deferred_schema.get("forbiddenField") != "requestId" or \
            (required_changes.get("fixture") or {}).get("id") != \
            "evidence-bundle-reject-request-id":
        errors.append("RequestId deferred EvidenceBundle patch is absent or not exact")

    if resolved_inputs is None:
        errors.append(f"could not load {RESOLVED_INPUTS} for Snapshot/Plan joins")
    else:
        snapshot_fields = set((resolved_inputs.get("snapshotIdContract", {})
                               .get("descriptorSchema", {}).get("required", [])))
        snapshot_closed = (resolved_inputs.get("snapshotIdContract", {})
                           .get("descriptorSchema", {}).get("closed"))
        plan_fields = {item.get("name") for item in
                       resolved_inputs.get("planIdContract", {}).get("preimageFields", [])}
        excluded_ids = set((resolved_inputs.get("planIdContract", {})
                            .get("excludedIdentitiesAndInputs", {}).get("identities", [])))
        if snapshot_closed is not True or "requestId" in snapshot_fields or \
                "requestId" in plan_fields or \
                "RequestId" not in excluded_ids:
            errors.append("live Snapshot/Plan identity schema permits RequestId")
    if c2 is None:
        errors.append(f"could not load {C2} for PlanIntent/ExecutionPlan join")
    else:
        plan_intent = c2.get("planIntent") or {}
        semantic_schemas = {
            key: plan_intent.get(key) for key in (
                "wireTypes", "schema", "analysisIntentV1",
                "admissionDescriptorV1", "storedViewIntentV1",
            )
        }
        plan_intent_blob = json.dumps(semantic_schemas)
        execution_fields = set((c2.get("executionPlan") or {}).get("requiredFields", []))
        if "requestId" in plan_intent_blob or "RequestId" in plan_intent_blob or \
                "requestId" in execution_fields:
            errors.append("live C-2 semantic PlanIntent/ExecutionPlan admits RequestId")
    if fact_plane is None:
        errors.append(f"could not load {FACT_PLANE}")
    else:
        envelope = fact_plane.get("factEnvelope") or {}
        envelope_fields = set(envelope.get("fields", {}))
        allowed = set(envelope.get("requiredFields", [])) | \
            set(envelope.get("optionalFields", []))
        if envelope.get("closed") is not True or \
                envelope.get("additionalProperties") is not False or \
                envelope_fields != allowed or "requestId" in allowed or \
                envelope.get("unknownFieldOutcome") != "FACT_ENVELOPE_UNKNOWN_FIELD":
            errors.append("live FactEnvelope is not closed against RequestId/unknown fields")
        fact_record = fact_plane.get("factRecordContractV1") or {}
        fact_id = fact_record.get("factIdContract") or {}
        fact_input_names = {item.get("name") for item in fact_id.get("preimageFields", [])}
        fact_variation = fact_record.get("requestIdInvarianceVector") or {}
        fact_vectors = {item.get("id"): item for item in fact_record.get("vectors", [])
                        if isinstance(item, dict)}
        live_fact_vector_id = fact_variation.get("baseVectorId")
        live_fact_ids = fact_variation.get("expectedFactIds") or []
        live_base_fact_id = (fact_vectors.get(live_fact_vector_id) or {}).get("expectedFactId")
        if fact_record.get("contractId") != "opensip.fact-record.v1" or \
                fact_id.get("id") != "opensip.fact-id.v1" or \
                fact_id.get("owner") != "Rust host only" or \
                "requestId" in fact_input_names or "RequestId" in fact_input_names or \
                "canonicalRelationPayload" not in fact_input_names or \
                len(live_fact_ids) != 2 or live_fact_ids[0] != live_fact_ids[1] or \
                live_fact_ids[0] != live_base_fact_id or \
                any(not isinstance(item, str) or
                    re.fullmatch(r"fact:sha256:[0-9a-f]{64}", item) is None
                    for item in live_fact_ids):
            errors.append("live FACT-ID-V1 computed RequestId-exclusion join is absent or stale")
    if fact_identity is None:
        errors.append(f"could not load {FACT_IDENTITY}")
    else:
        byte_grammar = ((fact_identity.get("canonicalisationSchema") or {}).get("byteGrammar") or {})
        identity_boundary = fact_identity.get("factRecordIdentityBoundaryV1") or {}
        body = identity_boundary.get("normalizedBodyIdentity") or {}
        generic = identity_boundary.get("genericFactRecordIdentity") or {}
        if "RequestId" in json.dumps(byte_grammar) or "requestId" in json.dumps(byte_grammar):
            errors.append("live body-identity byte grammar includes RequestId")
        if identity_boundary.get("id") != "opensip.fact-record-identity-boundary.v1" or \
                body.get("contractId") != "opensip.normalized-body-identity.v1" or \
                generic.get("contractId") != "opensip.fact-id.v1" or \
                body.get("contractId") == generic.get("contractId") or \
                body.get("domainTag") == generic.get("domainTag"):
            errors.append("live normalized-body/generic-fact identity boundary is absent or aliased")
    if evidence is None:
        errors.append(f"could not load {EVIDENCE} while EvidenceBundle closure is pending")
    else:
        bundle = ((evidence.get("bundleSchema") or {}).get("EvidenceBundle") or {})
        if "requestId" in set(bundle.get("required", []) + bundle.get("optional", [])):
            errors.append("live EvidenceBundle explicitly admits RequestId despite pending closure")
    if r1 is None:
        errors.append(f"could not load {R1}")
    else:
        core = r1.get("coreApi") or {}
        sealed_schema = core.get("sealedStageInput") or {}
        attempt_schema = core.get("attemptMetadata") or {}
        sealed = set(sealed_schema.get("contains", []))
        attempt = set(attempt_schema.get("required", []))
        completion = r1.get("coreCompletionSchema") or {}
        if sealed_schema.get("closed") is not True or \
                sealed_schema.get("additionalProperties") is not False or \
                set(sealed_schema.get("required", [])) != sealed or \
                sealed_schema.get("optional") != [] or \
                attempt_schema.get("closed") is not True or \
                attempt_schema.get("additionalProperties") is not False or \
                attempt_schema.get("optional") != [] or \
                "requestId" in sealed or "requestId" in attempt or \
                "requestId" in json.dumps(completion):
            errors.append("live pure-core serialized boundary is open to RequestId")
        if "executionId" not in attempt:
            errors.append("pure-core metadata join drifted; cannot distinguish RequestId exclusion")
    if d9 is None:
        errors.append(f"could not load {D9}")
    else:
        axes = set(((d9.get("scenarioAxesSchema") or {}).get("properties") or {}))
        if "requestId" in axes:
            errors.append("live D9 derivation axes admit RequestId")

    variation = next((item for item in req.get("fixtures", [])
                      if item.get("id") == "request-id-semantic-variation"), {})
    request_ids = variation.get("requestIds", [])
    expected = variation.get("expectedInvariantPairs") or {}
    if len(request_ids) != 2 or request_ids[0] == request_ids[1] or \
            not all(REQUEST_ID_RE.fullmatch(item) for item in request_ids):
        errors.append("RequestId variation fixture does not vary two canonical IDs")
    required_pairs = {"snapshotId", "planId", "factId",
                      "coreCompletion", "d9Termination"}
    if set(expected) != required_pairs or any(
            not isinstance(pair, list) or len(pair) != 2 or pair[0] != pair[1]
            for pair in expected.values()):
        errors.append("RequestId variation fixture does not preserve all mechanically joined results")
    if variation.get("factIdVectorId") != live_fact_vector_id or \
            expected.get("factId") != live_fact_ids:
        errors.append("RequestId variation fixture is not joined to the computed FACT-ID-V1 oracle")
    if set(variation.get("mechanicallyChecked", [])) != REQUEST_MECHANICAL_JOINS or \
            set(variation.get("parked", [])) != REQUEST_PARKED_SURFACES or \
            set(variation.get("pendingCrossSurface", [])) != REQUEST_PENDING_CROSS_SURFACES:
        errors.append("RequestId variation fixture overclaims or omits mechanical coverage")
    return errors


def _request_id_errors(contract: dict, resolved_inputs: dict | None,
                       c2: dict | None = None, d9: dict | None = None,
                       fact_plane: dict | None = None,
                       fact_identity: dict | None = None,
                       evidence: dict | None = None, r1: dict | None = None) -> list[str]:
    errors: list[str] = []
    req = contract.get("requestIdContract") or {}
    assurance = req.get("assurance") or {}
    if req.get("id") != "REQUEST-ID-V1" or req.get("status") != "IMPLEMENTABLE":
        errors.append("REQUEST-ID-V1 absent or not honestly IMPLEMENTABLE")
    if assurance.get("state") != "IMPLEMENTABLE" or \
            assurance.get("evidenceGrade") != "IMPLEMENTABLE_UNEXECUTED" or \
            assurance.get("qualificationEvidenceIds") != [] or \
            assurance.get("releaseEvidenceIds") != []:
        errors.append("RequestId assurance greenwashed beyond IMPLEMENTABLE_UNEXECUTED")
    authority = req.get("authority") or {}
    if authority.get("allocationOwner") != "orchestration host request-ingress adapter" or \
            authority.get("validationOwner") != \
            "orchestration host RequestContext constructor and EventEnvelope validator":
        errors.append("host allocation/validation ownership is not exact")
    if "MUST NOT supply requestId" not in authority.get("callerRule", "") or \
            "clientCorrelationId" not in authority.get("callerRule", ""):
        errors.append("caller-supplied identity is accepted or conflated with correlation metadata")
    allocation = req.get("allocation") or {}
    point = allocation.get("point", "")
    for term in ("first trusted host ingress", "before request parsing",
                 "request validation", "stored-Run lookup", "ExecutionId allocation",
                 "AttemptRecord creation"):
        if term not in point:
            errors.append(f"allocation point omits '{term}'")
    all_requests = " ".join(allocation.get("allRequests", []))
    if "rejected" not in all_requests or "stored-Run" not in all_requests:
        errors.append("rejected or stored-view request allocation is not explicit")
    representation = req.get("representation") or {}
    if representation.get("raw") != "16 uniformly random bytes from the OS CSPRNG" or \
            representation.get("text") != "req1_<32 lowercase hexadecimal characters>" or \
            representation.get("regex") != r"^req1_[0-9a-f]{32}$" or \
            representation.get("schemaVersion") != 1:
        errors.append("RequestId byte/text representation drifted")
    collision = req.get("collisionAndRetry") or {}
    if collision.get("maximumCandidates") != 8 or \
            "atomically reserve" not in collision.get("reservationRule", "") or \
            "fresh independent 16-byte candidate" not in collision.get("onCollision", "") or \
            "REQUEST_ID_ALLOCATION_FAILED" not in collision.get("onExhaustion", "") or \
            "not an idempotency key" not in collision.get("externalRetry", ""):
        errors.append("RequestId reservation/collision/retry protocol is incomplete or drifted")
    semantic = req.get("semanticExclusion") or {}
    if set(semantic.get("excludedFrom", [])) != REQUEST_EXCLUSIONS:
        errors.append("RequestId semantic exclusion set is not exact")
    semantic_rule = semantic.get("rule", "")
    for term in ("SnapshotId", "PlanId", "fact/finding identity", "EvidenceDigest",
                 "RunId", "Run content", "verdict", "termination"):
        if term not in semantic_rule:
            errors.append(f"RequestId semantic invariance omits {term}")
    custody = req.get("custody") or {}
    if not custody.get("requestContext") or "outside the sealed Run manifest" not in \
            custody.get("attemptLink", "") or "HostAuditRecord" not in \
            custody.get("operationalRecords", ""):
        errors.append("RequestId custody/AttemptRecord/audit boundary is incomplete")

    fixtures = {item.get("id"): item for item in req.get("fixtures", [])}
    if {key: fixtures.get(key, {}).get("expected") for key in REQUEST_NEGATIVES} != \
            REQUEST_NEGATIVES:
        errors.append("RequestId exact negative fixture set/outcomes are incomplete")
    rejected = fixtures.get("request-id-valid-rejected-request", {})
    if rejected.get("valid") is not True or rejected.get("allocatedBefore") != "parse" or \
            rejected.get("executionId") is not None or rejected.get("runId") is not None or \
            not REQUEST_ID_RE.fullmatch(rejected.get("requestId", "")):
        errors.append("rejected-request positive fixture does not prove pre-parse allocation")
    stored = fixtures.get("request-id-valid-stored-view", {})
    if stored.get("valid") is not True or stored.get("path") != "stored-run-read" or \
            stored.get("executionId") is not None or not stored.get("runId") or \
            not REQUEST_ID_RE.fullmatch(stored.get("requestId", "")):
        errors.append("stored-view positive fixture does not prove RequestId without ExecutionId")
    retry = fixtures.get("request-id-valid-collision-retry", {})
    candidates = retry.get("candidates", [])
    reserved = set(retry.get("reserved", []))
    if retry.get("valid") is not True or len(candidates) != 2 or \
            candidates[0] not in reserved or candidates[1] in reserved or \
            retry.get("expectedAttempts") != 2 or \
            retry.get("expectedRequestId") != candidates[1] or \
            not all(REQUEST_ID_RE.fullmatch(item) for item in candidates):
        errors.append("collision-retry positive fixture does not exercise atomic retry")
    uppercase = fixtures.get("request-id-reject-uppercase", {}).get("requestId", "")
    if REQUEST_ID_RE.fullmatch(uppercase):
        errors.append("uppercase negative fixture is actually canonical")
    exhaustion = fixtures.get("request-id-reject-collision-exhaustion-as-request", {})
    if exhaustion.get("collisionCount") != 8 or exhaustion.get("eventEmitted") is not False or \
            exhaustion.get("attemptAdmitted") is not False:
        errors.append("collision exhaustion can emit an event or admit an attempt")

    if resolved_inputs is None:
        errors.append(f"could not load {RESOLVED_INPUTS} for PlanId exclusion join")
    else:
        excluded_ids = set((resolved_inputs.get("planIdContract", {})
                            .get("excludedIdentitiesAndInputs", {})
                            .get("identities", [])))
        if "RequestId" not in excluded_ids:
            errors.append("live PLAN-ID-V1 does not exclude RequestId")
    if "requestId" not in set(contract.get("hostAuditSchema", {})
                               .get("HostAuditRecord", {}).get("required", [])):
        errors.append("HostAuditRecord no longer requires RequestId custody")
    if not any(item.get("id") == "OP-10" and item.get("state") == "IMPLEMENTABLE"
               for item in contract.get("conformanceTests", [])):
        errors.append("OP-10 RequestId conformance target is absent")
    errors.extend(_request_d9_errors(req, d9))
    errors.extend(_request_semantic_join_errors(
        req, resolved_inputs, c2, d9, fact_plane, fact_identity, evidence, r1))
    return errors


def _projection_errors(fx: dict) -> list[str]:
    expected = fx.get("expected")
    allowed = {
        ("json", "all-required-fields-exact"),
        ("exit-code", "termination-only"),
        ("human-terminal", "visible-omitted-count-and-retrieval"),
        ("sarif", "coverage-in-opensip-property-bag"),
        ("agent-mcp", "stable-cursor-reaches-all-findings"),
    }
    return [] if (fx.get("surface"), expected) in allowed else [
        f"surface {fx.get('surface')} cannot produce '{expected}'"
    ]


def _audit_errors(fx: dict, transitions: dict) -> list[str]:
    errs: list[str] = []
    path = fx.get("path", [])
    for a, b in zip(path, path[1:]):
        if b not in transitions.get(a, []):
            errs.append(f"invalid transition {a}->{b}")
    if fx.get("mutationVisible") and not fx.get("committedRecord"):
        if not path or path[-1] != "RECOVERY-REQUIRED":
            errs.append("visible mutation has no committed or recovery record")
        elif path[-1] == "RECOVERY-REQUIRED" and fx.get("valid"):
            # A valid fixture may stop in RECOVERY-REQUIRED only when it explicitly
            # represents an in-progress recovery. None of the current goldens do.
            errs.append("visible mutation stops before recovery terminal state")
    if fx.get("containsSecretValue"):
        errs.append("audit record contains resolved secret value")
    if fx.get("sequences") and (len(set(fx["sequences"])) != len(fx["sequences"])
                                or not fx.get("unique")):
        errs.append("concurrent sequences are not unique")
    if fx.get("operation") == "purge" and not (
            fx.get("beforeCommitment") and fx.get("afterCommitment")):
        errs.append("purge lacks before/after commitments")
    return errs


def _check(c: dict, c2: dict | None, tm: dict | None,
           resolved_inputs: dict | None = None) -> list[str]:
    findings: list[str] = []
    resolved_inputs = resolved_inputs if resolved_inputs is not None else load(RESOLVED_INPUTS)
    gates_list = c.get("validationGates", [])
    gates = {g.get("id"): g for g in gates_list}
    if len(gates) != len(gates_list):
        findings.append("OP-REL: duplicate gate id")

    # OP-SUBJ / OP-QUAL.
    classes = {x.get("class"): x for x in c.get("gateSubject", {}).get("classes", [])}
    if set(classes) != set(CLASSES):
        findings.append("OP-SUBJ: gate classes are not the exact closed set")
    if classes.get("design-integrity", {}).get("mayDischargeProductProperty"):
        findings.append("OP-SUBJ: design-integrity may discharge product properties")
    for g in gates_list:
        for err in _gate_errors(g):
            findings.append(f"OP-QUAL {g.get('id')}: {err}")
    for fx in c.get("qualificationFixtures", []):
        errs = _gate_errors(fx["gate"])
        if fx["valid"] and errs:
            findings.append(f"OP-QUAL {fx['id']}: expected valid — {errs[0]}")
        elif not fx["valid"] and not errs:
            findings.append(f"OP-QUAL {fx['id']}: expected rejection by {fx.get('violates')}")
    if set(c.get("designIntegritySuite", {}).get("checkers", [])) != EXPECTED_CHECKERS:
        findings.append("OP-QUAL: G12 design checker target is not the exact 12-checker set")
    if c.get("designIntegritySuite", {}).get("measurementInstrument") != \
            "artifacts/check-completeness.py":
        findings.append("OP-QUAL: completeness instrument is absent or conflated with G12")
    g12 = gates.get("G12", {})
    if g12.get("property") != "the registered contract checkers reject their declared mutations":
        findings.append("OP-QUAL: G12 overclaims semantic/internal coherence")
    if g12.get("target") != "designIntegritySuite.checkers":
        findings.append("OP-QUAL: G12 points at an unbound/imaginary target")

    # OP-REL / OP-TM: the registry is exhaustive and release state is derived.
    registry = c.get("requiredPropertyRegistry", {})
    props_list = registry.get("properties", [])
    props = {p.get("id"): p for p in props_list}
    if not registry.get("closed"):
        findings.append("OP-REL: required property registry is not closed")
    if len(props) != len(props_list):
        findings.append("OP-REL: duplicate required property id")
    tm_ids = {f"TM.{p['id']}" for p in tm.get("requiredProperties", [])} if tm else set()
    expected = tm_ids | LOCAL_PROPERTIES
    missing, extra = expected - set(props), set(props) - expected
    if missing:
        findings.append(f"OP-REL: required properties omitted: {sorted(missing)}")
    if extra:
        findings.append(f"OP-REL: unknown required properties: {sorted(extra)}")
    for pid, prop in props.items():
        if prop.get("subject") != "product" or not prop.get("gateIds"):
            findings.append(f"OP-REL {pid}: missing product subject or gate mapping")
        for gid in prop.get("gateIds", []):
            gate = gates.get(gid)
            if gate is None:
                findings.append(f"OP-REL {pid}: unknown gate {gid}")
            elif gate.get("class") != "implementation-conformance" or \
                    gate.get("subject") != "product":
                findings.append(f"OP-REL {pid}: wrong-subject gate {gid}")
    demonstrated = {
        pid for pid, prop in props.items()
        if any(gates.get(gid, {}).get("status") == "DEMONSTRATED"
               and gates.get(gid, {}).get("releaseEvidenceIds")
               for gid in prop.get("gateIds", []))
    }
    blocked = sorted(set(props) - demonstrated)
    dec = c.get("releaseDecision", {})
    want_state = "RELEASABLE" if not blocked else "BLOCKED"
    if dec.get("state") != want_state or sorted(dec.get("blockedPropertyIds", [])) != blocked:
        findings.append("OP-REL: releaseDecision is not derived from DEMONSTRATED gate evidence")
    if dec.get("demonstratedPropertyCount") != len(demonstrated):
        findings.append("OP-REL: demonstratedPropertyCount is editorial, not derived")
    if tm is None:
        findings.append(f"OP-TM: could not load {TM}")
    else:
        live = {p["id"] for p in tm.get("requiredProperties", [])}
        for g in gates_list:
            for ref in g.get("threatModelRefs", []):
                if ref not in live:
                    findings.append(f"OP-TM {g.get('id')}: unknown required property {ref}")

    # OP-ID.
    phases = c.get("eventSchema", {}).get("phaseRequirements", {})
    if set(phases) != {"request-validation", "attempt-admitted", "attempt-sealed",
                       "stored-run-read"}:
        findings.append("OP-ID: phase requirement set is not closed")
    if c2:
        levels = {x["level"] for x in c2["theAdmissionBoundary"]["levels"]}
        if "attempt-admission" not in levels:
            findings.append("OP-ID: live C-2 has no attempt-admission boundary")
    else:
        findings.append(f"OP-ID: could not load {C2}")
    for fx in c.get("eventFixtures", []):
        errs = _event_errors(fx, c)
        if fx["valid"] and errs:
            findings.append(f"OP-ID {fx['id']}: expected valid — {errs[0]}")
        elif not fx["valid"] and not errs:
            findings.append(f"OP-ID {fx['id']}: expected rejection")
    for err in _request_id_errors(
            c, resolved_inputs, c2, load(D9), load(FACT_PLANE),
            load(FACT_IDENTITY), load(EVIDENCE), load(R1)):
        findings.append(f"OP-REQID: {err}")

    # OP-PAR.
    par = c.get("projectionParity", {})
    if set(par.get("requiredFields", [])) != FIELDS:
        findings.append("OP-PAR: required field set is not the exact canonical set")
    surfaces = {s.get("id"): s for s in par.get("surfaces", [])}
    if set(surfaces) != SURFACES:
        findings.append("OP-PAR: projection surface set is not closed")
    modes = set(par.get("representationModes", []))
    for sid, surface in surfaces.items():
        fmap = surface.get("fieldModes", {})
        if set(fmap) != FIELDS:
            findings.append(f"OP-PAR {sid}: field map is incomplete or contains inventions")
        for mode in fmap.values():
            if mode not in modes:
                findings.append(f"OP-PAR {sid}: unknown representation mode {mode}")
    if any(v != "exact" for v in surfaces.get("json", {}).get("fieldModes", {}).values()):
        findings.append("OP-PAR: JSON is not an exact reference projection")
    if surfaces.get("sarif", {}).get("fieldModes", {}).get("coverage") != "extension":
        findings.append("OP-PAR: SARIF drops Coverage instead of using its property bag")
    if "visible" not in surfaces.get("human-terminal", {}).get("truncation", ""):
        findings.append("OP-PAR: human truncation is not visibly disclosed")
    if "stable cursor" not in surfaces.get("agent-mcp", {}).get("pagination", ""):
        findings.append("OP-PAR: agent pagination has no stable continuation truth")
    run_ids = {r.get("id") for r in par.get("canonicalRuns", [])}
    for need in {"clean-complete", "policy-fail", "partial-indeterminate",
                 "truncated-unavailable"} - run_ids:
        findings.append(f"OP-PAR: canonical Run corpus omits {need}")
    for fx in c.get("projectionFixtures", []):
        errs = _projection_errors(fx)
        if fx["valid"] and errs:
            findings.append(f"OP-PAR {fx['id']}: expected valid — {errs[0]}")
        elif not fx["valid"] and not errs:
            findings.append(f"OP-PAR {fx['id']}: expected rejection")

    # OP-AUD.
    audit = c.get("auditPlane", {})
    for key in ("authority", "boundary", "ordering", "atomicity", "failure", "redaction"):
        if not audit.get(key):
            findings.append(f"OP-AUD: audit protocol omits {key}")
    if "EvidenceDigest" not in audit.get("boundary", ""):
        findings.append("OP-AUD: audit plane is not outside analysis EvidenceDigest")
    schema = c.get("hostAuditSchema", {}).get("HostAuditRecord", {})
    required_audit = {"schemaVersion", "auditId", "mutationId", "requestId", "projectId",
                      "sequence", "actor", "operation", "state", "privacyClasses",
                      "beforeCommitment", "afterCommitment", "retentionClass", "redactions"}
    if set(schema.get("required", [])) != required_audit:
        findings.append("OP-AUD: HostAuditRecord required fields are not exact")
    transitions = c.get("hostAuditSchema", {}).get("transitionTable", {})
    for fx in c.get("hostAuditFixtures", []):
        errs = _audit_errors(fx, transitions)
        if fx["valid"] and errs:
            findings.append(f"OP-AUD {fx['id']}: expected valid — {errs[0]}")
        elif not fx["valid"] and not errs:
            findings.append(f"OP-AUD {fx['id']}: expected rejection")

    # OP-CAP.
    cap = c.get("capacityClasses", {}).get("reference-standard-v1", {})
    for section in ("hardwareFloor", "workload", "limits", "measurement"):
        if not cap.get(section):
            findings.append(f"OP-CAP: reference-standard-v1 omits {section}")
    for field in ("peakRssGiB", "managedDiskGiB", "coldRuntimeSeconds",
                  "cooperativeCancelSeconds", "hardKillSeconds",
                  "orphanProcessesAfterSeconds"):
        if field not in cap.get("limits", {}):
            findings.append(f"OP-CAP: resource limit {field} absent")
    for gid in ("G10", "G11"):
        if gates.get(gid, {}).get("status") != "IMPLEMENTABLE" or not gates.get(gid, {}).get("target"):
            findings.append(f"OP-CAP: {gid} wrongly deferred behind the restricted runtime")
    if gates.get("G9", {}).get("status") != "BLOCKED-NO-MECHANISM" or \
            not gates.get("G9", {}).get("initialProductDisposition"):
        findings.append("OP-CAP: missing runtime mechanism neither blocks nor excludes its features")
    g19 = gates.get("G19", {})
    if g19.get("status") != "BLOCKED-NO-MECHANISM" or \
            "V10" not in g19.get("blocker", "") or \
            "durable-authoritative retention is rejected" not in \
            g19.get("initialProductDisposition", ""):
        findings.append("OP-CAP: V10 retention mechanism is greenwashed or its feature is retained")
    if props.get("TM.R4", {}).get("gateIds") != ["G19"] or \
            "R4" in gates.get("G4", {}).get("threatModelRefs", []):
        findings.append("OP-CAP: storage admission is incorrectly promoted into durable-custody proof")
    return findings


def check(c: object, c2: dict | None, tm: dict | None,
          resolved_inputs: dict | None = None) -> list[str]:
    """Total checker boundary; wrong JSON shapes are controlled findings."""
    if not isinstance(c, dict) or not c:
        return ["OP-TOTALITY-ROOT: contract root must be a non-empty object"]
    if not isinstance(c.get("validationGates"), list):
        return ["OP-TOTALITY-SHAPE: validationGates must be an array"]
    try:
        return _check(c, c2, tm, resolved_inputs)
    except MALFORMED_SHAPE_EXCEPTIONS as exc:
        return [f"OP-TOTALITY-EXCEPTION: malformed contract shape "
                f"({type(exc).__name__})"]


def _drop_gates(c):
    c["validationGates"] = [g for g in c["validationGates"] if g["id"] == "G12"]


def _contradict_event(c):
    c["eventSchema"]["phaseRequirements"]["request-validation"]["executionId"] = "required"


def _imaginary_g12(c):
    c["validationGates"][11]["target"] = "imaginary checker"


def _broad_g12(c):
    c["validationGates"][11]["property"] = "the architecture is internally coherent"


def _arbitrary_fields(c):
    c["projectionParity"]["requiredFields"] = ["foo", "bar", "baz", "qux", "quux"]


def _drop_sarif_coverage(c):
    for s in c["projectionParity"]["surfaces"]:
        if s["id"] == "sarif":
            s["fieldModes"]["coverage"] = "omitted-by-contract"


def _paper_qualify(c):
    g = c["validationGates"][0]
    g["status"] = "QUALIFIED"
    g["observedFailure"] = True


def _false_release(c):
    c["releaseDecision"]["state"] = "RELEASABLE"
    c["releaseDecision"]["blockedPropertyIds"] = []


def _drop_audit_atomicity(c):
    del c["auditPlane"]["atomicity"]


def _drop_capacity(c):
    del c["capacityClasses"]["reference-standard-v1"]["limits"]


def _defer_fault_target(c):
    for g in c["validationGates"]:
        if g["id"] == "G11":
            g["status"] = "BLOCKED-NO-MECHANISM"
            g["target"] = None
            g["blocker"] = "ARCH.PROBE-CONTRACT"


def _greenwash_retention(c):
    c["requiredPropertyRegistry"]["properties"][3]["gateIds"] = ["G4"]
    for g in c["validationGates"]:
        if g["id"] == "G4":
            g["threatModelRefs"].append("R4")


def _allow_caller_request_id(c):
    c["requestIdContract"]["authority"]["callerRule"] = \
        "Public callers MAY supply requestId."


def _allocate_request_id_late(c):
    c["requestIdContract"]["allocation"]["point"] = \
        "After request validation and immediately before attempt admission."


def _accept_uuid_request_id(c):
    c["requestIdContract"]["representation"]["regex"] = \
        r"^[0-9a-f-]{36}$"


def _overwrite_request_collision(c):
    c["requestIdContract"]["collisionAndRetry"]["onCollision"] = \
        "Overwrite the existing request and continue."


def _drop_stored_request_path(c):
    allocation = c["requestIdContract"]["allocation"]
    allocation["allRequests"] = [item for item in allocation["allRequests"]
                                 if "stored-Run" not in item]
    c["requestIdContract"]["fixtures"] = [
        item for item in c["requestIdContract"]["fixtures"]
        if item["id"] != "request-id-valid-stored-view"
    ]


def _let_request_id_enter_plan(c):
    c["requestIdContract"]["semanticExclusion"]["excludedFrom"].remove(
        "PlanId preimage")


def _greenwash_request_id(c):
    assurance = c["requestIdContract"]["assurance"]
    assurance["state"] = "DEMONSTRATED"
    assurance["evidenceGrade"] = "DEMONSTRATED"


def _malform_valid_event_request_id(c):
    c["eventFixtures"][0]["requestId"] = "Q1"


def _fake_collision_retry(c):
    for fixture in c["requestIdContract"]["fixtures"]:
        if fixture["id"] == "request-id-valid-collision-retry":
            fixture["reserved"] = []


def _drift_request_d9(c):
    failure = c["requestIdContract"]["d9Projection"]["allocationFailure"]
    failure["expectedTermination"]["errorCode"] = "HOST.REQUEST_ID_ALLOCATION_FAILED"


def _drop_request_semantic_join(c):
    joined = c["requestIdContract"]["semanticExclusion"]["proofStatus"][
        "mechanicallyJoined"]
    joined.pop()


def _paper_prove_parked_request_surface(c):
    parked = c["requestIdContract"]["semanticExclusion"]["proofStatus"][
        "parkedNoExactRecipe"]
    parked[0]["status"] = "MECHANICALLY_PROVEN"


def _vary_plan_with_request_id(c):
    for fixture in c["requestIdContract"]["fixtures"]:
        if fixture["id"] == "request-id-semantic-variation":
            fixture["expectedInvariantPairs"]["planId"][1] = \
                "plan1:sha256:0000000000000000000000000000000000000000000000000000000000000000"


def _replace_fact_id_pair_with_equal_junk(c):
    for fixture in c["requestIdContract"]["fixtures"]:
        if fixture["id"] == "request-id-semantic-variation":
            fixture["expectedInvariantPairs"]["factId"] = ["equal-junk", "equal-junk"]


def _paper_prove_pending_evidence_closure(c):
    pending = c["requestIdContract"]["semanticExclusion"]["proofStatus"][
        "pendingCrossSurfaceClosure"]
    pending[0]["status"] = "MECHANICALLY_PROVEN"


MUTATIONS = [
    ("delete product gates, making the registry vacuous (R2-OP-01)", _drop_gates),
    ("contradict pre-admission identity (R2-OP-02)", _contradict_event),
    ("point G12 at an imaginary target (R2-OP-03)", _imaginary_g12),
    ("let G12 overclaim semantic coherence (R2-OP-03)", _broad_g12),
    ("replace canonical projection fields with inventions (R2-OP-04)", _arbitrary_fields),
    ("drop Coverage from SARIF despite property bags (R2-OP-04)", _drop_sarif_coverage),
    ("qualify a gate with a bare boolean (R2-OP-03 / FINAL-02)", _paper_qualify),
    ("editorially declare a release ready (R2-OP-01)", _false_release),
    ("drop host-audit atomicity (R2-OP-06)", _drop_audit_atomicity),
    ("delete reference capacity limits (R2-OP-07)", _drop_capacity),
    ("defer buildable fault containment behind capability runtime (R2-OP-05)", _defer_fault_target),
    ("treat storage admission as proof that V10 is resolved (R2-TM-02/04)",
     _greenwash_retention),
    ("accept caller-supplied RequestId (IP-R4-02)", _allow_caller_request_id),
    ("allocate RequestId after validation (IP-R4-02)", _allocate_request_id_late),
    ("replace canonical RequestId with UUID-like aliases (IP-R4-02)",
     _accept_uuid_request_id),
    ("overwrite a RequestId collision (IP-R4-02)", _overwrite_request_collision),
    ("omit RequestId allocation for stored reads (IP-R4-02)", _drop_stored_request_path),
    ("include RequestId in PlanId (IP-R4-02)", _let_request_id_enter_plan),
    ("claim RequestId demonstrated without product evidence (FINAL-02)",
     _greenwash_request_id),
    ("emit a noncanonical RequestId on a valid event (IP-R4-02)",
     _malform_valid_event_request_id),
    ("make collision-retry fixture contain no collision (IP-R4-02)",
     _fake_collision_retry),
    ("invent a RequestId-specific D9 error code (R6-ID-05)", _drift_request_d9),
    ("drop a live RequestId semantic-exclusion join (R6-ID-04)",
     _drop_request_semantic_join),
    ("paper-prove a RequestId exclusion with no exact recipe (R6-ID-04)",
     _paper_prove_parked_request_surface),
    ("let RequestId change PlanId in the invariance fixture (R6-ID-04)",
     _vary_plan_with_request_id),
    ("replace computed FACT-ID-V1 values with equal junk (R6R-IP02-01)",
     _replace_fact_id_pair_with_equal_junk),
    ("paper-prove EvidenceBundle before owner integration (R6-IP02-01)",
     _paper_prove_pending_evidence_closure),
]


def selftest(base: dict, c2: dict | None, tm: dict | None) -> int:
    pre = check(base, c2, tm)
    if pre:
        print(f"REFUSING to self-test: base contract has {len(pre)} finding(s)")
        for item in pre[:8]:
            print("  -", item)
        return 1
    print("mutation self-test — each row must be REJECTED\n")
    escaped = 0
    for name, root in TOTALITY_ROOT_CASES:
        found = check(copy.deepcopy(root), c2, tm)
        if not found:
            escaped += 1
        print(f"  {'reject' if found else 'ESCAPE':>6}  parsed-JSON root {name}")
        print(f"          {found[0] if found else 'NO FINDING — root survived'}")
    for name, mutation in MUTATIONS:
        candidate = copy.deepcopy(base)
        mutation(candidate)
        found = check(candidate, c2, tm)
        if not found:
            escaped += 1
        print(f"  {'reject' if found else 'ESCAPE':>6}  {name}")
        print(f"          {found[0] if found else 'NO FINDING — mutation survived'}")
    print()
    if escaped:
        print(f"{escaped}/{len(MUTATIONS) + len(TOTALITY_ROOT_CASES)} retained cases ESCAPED")
        return 1
    print(f"all {len(MUTATIONS)} semantic mutations and {len(TOTALITY_ROOT_CASES)} "
          "root-shape cases rejected — adjudicated defects are load-bearing")
    return 0


def main() -> int:
    args = [a for a in sys.argv[1:] if a != "--selftest"]
    path = pathlib.Path(args[0]) if args else HERE / BINDING
    if not path.exists():
        print(f"missing contract: {path}", file=sys.stderr)
        return 2
    contract = json.loads(path.read_text())
    c2, tm = load(C2), load(TM)
    if "--selftest" in sys.argv:
        return selftest(contract, c2, tm)
    found = check(contract, c2, tm)
    if found:
        print(f"{len(found)} finding(s) in {path.name}:")
        for item in found:
            print("  -", item)
        return 1
    gates = contract["validationGates"]
    counts = {state: sum(g["status"] == state for g in gates) for state in STATES}
    print(f"operability OK — {path.name}, {len(gates)} gates, "
          "OP-SUBJ / OP-QUAL / OP-REL / OP-ID / OP-REQID / OP-PAR / OP-AUD / "
          "OP-CAP / OP-TM clean")
    print(f"  assurance: {counts['IMPLEMENTABLE']} implementable, "
          f"{counts['BLOCKED-NO-MECHANISM']} mechanism-blocked, "
          f"{counts['QUALIFIED']} qualified, {counts['DEMONSTRATED']} demonstrated")
    print(f"  release decision: {contract['releaseDecision']['state']} — "
          f"{len(contract['releaseDecision']['blockedPropertyIds'])} properties undemonstrated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
