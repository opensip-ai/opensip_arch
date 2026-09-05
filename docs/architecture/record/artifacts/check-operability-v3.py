#!/usr/bin/env python3
"""Checker for candidate OPERABILITY v3 and its exact OP2 projection.

The checker proves that every OP2 subtree is recoverable byte-semantically by
one closed projection, then checks the additive A-prime committed-only Run
lifecycle, recursive RequestId exclusion and still-blocked G19 mechanism.

Usage: python3 -B check-operability-v3.py [contract] [--selftest]
"""
from __future__ import annotations

import copy
import hashlib
import json
import pathlib
import re
import sys
from typing import Any

HERE = pathlib.Path(__file__).resolve().parent
BINDING = "operability.v3.json"

FILES = {
    "operability.v2.json": "43e63e4bca8e238e933a6b3e0c91112fb29b52da5f92d64ff2438d79140e6f04",
    "check-operability.py": "925496916ef2c7075c02f7a767353aa6ff047cf55557304f3983e17e1c5256e2",
    "evidence.v4.json": "4a5d2dc8d9067af103b6f8c898c83f08fdd59ee22ce49fb4cf12a1329c416c70",
    "check-evidence-v4.py": "fd8db2ab77261ba31351d0647cf62ba4de92db35ba7a15426cb8f4bcf28865bc",
    "d9-exit-contract.v1.7.json": "d199aef6ac2edc7652325ef8d26f75cfda35a94f3e234d10aafd984d9088b2eb",
    "check-d9-v1.7.py": "ead1dd8d3635a355475ba8d71611515497a29e59cdfc5d232f167588dd9fb6d3",
    "retention-tiers.v10.json": "606b5e7125d4a3a46f44f1a7565f9c9ea69132d9ab2783d00339e1b8aac5e026",
    "check-retention-custody.py": "15816cd8f9d22221b1187b94a160d71f644f9ab8fccb82423931fe18f6fc38d7",
}

OLD_ENVELOPE = {
    "version": 2,
    "status": "CANDIDATE-REPAIRED-PENDING-INDEPENDENT-REREVIEW (product gates intentionally undemonstrated)",
    "supersedes": 1,
    "author": "agent-3; repaired by agent-b; RequestId closure by identity-contract owner",
    "reviewStatus": "The v2 base and first RequestId repair were independently reviewed. Reviewer6 finding R6-XID-04 is repaired and awaits independent rereview. R6R-IP02-01's generic FactId residual is repaired by a computed FACT-ID-V1 join and awaits DELIVERY integration/rereview. R6-IP02-01 is repaired for the six live closed Snapshot/Plan/C-2/fact/pure-core/D9 surfaces; EvidenceBundle unknown-field closure remains pending on the external Phase-1A owner under the exact deferred patch. Green checkers are design-integrity evidence only.",
}

NEW_ENVELOPE = {
    "version": 3,
    "status": "CANDIDATE-AWAITING-INDEPENDENT-COMBINED-REREVIEW (A-prime lifecycle; G19 remains blocked pending CD-RT-5; NOT APPLIED)",
    "supersedes": {
        "artifact": "operability.v2.json", "sha256": FILES["operability.v2.json"],
        "checker": "check-operability.py", "checkerSha256": FILES["check-operability.py"]},
    "author": "agent-3; repaired by agent-b; RequestId closure by identity-contract owner; A-prime successor by phase1a-evidence-successor-lane",
    "reviewStatus": "OPERABILITY v3 is a candidate-only A-prime overlay over an exact mechanically projected v2 base. The lifecycle/Evidence/G19 mechanism awaits independent combined rereview, CD-RT-5 product disposition and coordinator integration. Green checkers are design-integrity evidence only; no product gate is promoted.",
}

PHASE_REQUIREMENTS = {
    "request-validation": {"executionId": "forbidden", "runId": "forbidden",
                           "budgetOwner": "RequestId"},
    "attempt-admitted": {"executionId": "required", "runId": "forbidden",
                         "budgetOwner": "ExecutionId"},
    "run-committed": {"executionId": "required", "runId": "required",
                      "budgetOwner": "ExecutionId"},
    "stored-run-read": {"executionId": "forbidden", "runId": "required-existing-only",
                        "budgetOwner": "RequestId"},
}

CONSUMERS = {
    "assurance-state.v1.json and check-assurance.py":
        ["assuranceStateMachine", "validationGates", "requiredPropertyRegistry",
         "releaseDecision"],
    "c2-plan-stage-schema.v3.json and check-c2.py": ["requestIdContract"],
    "delivery.v2.json and check-delivery.py":
        ["assuranceStateMachine", "validationGates#G16", "requestIdContract"],
    "retention-tiers.v10.json and check-retention-custody.py":
        ["validationGates#G19"],
    "threat-model.v3.json and check-threat-claims.py":
        ["validationGates", "requiredPropertyRegistry", "releaseDecision"],
    "check-completeness.py": ["requiredPropertyRegistry", "releaseDecision"],
}

REQ_RE = re.compile(r"^req1_[0-9a-f]{32}$")


def load(name: str) -> Any:
    return json.loads((HERE / name).read_text())


def digest_file(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


def gate(root: dict[str, Any], gate_id: str) -> dict[str, Any] | None:
    rows = [x for x in root.get("validationGates", [])
            if isinstance(x, dict) and x.get("id") == gate_id]
    return rows[0] if len(rows) == 1 else None


def project_v2(candidate: dict[str, Any]) -> dict[str, Any]:
    projected = copy.deepcopy(candidate)
    projected.pop("aPrimeSuccessor", None)
    for key, value in OLD_ENVELOPE.items():
        projected[key] = copy.deepcopy(value)
    return projected


def _event_errors(event: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    phase = event.get("phase")
    if phase not in PHASE_REQUIREMENTS:
        return ["unknown/legacy v3 public phase"]
    req = PHASE_REQUIREMENTS[phase]
    request_id = event.get("requestId")
    if not isinstance(request_id, str) or REQ_RE.fullmatch(request_id) is None:
        errors.append("missing/noncanonical RequestId")
    for field in ("executionId", "runId"):
        present = isinstance(event.get(field), str) and bool(event[field])
        mode = req[field]
        if mode.startswith("required") and not present:
            errors.append(f"{field} required")
        if mode == "forbidden" and present:
            errors.append(f"{field} forbidden")
    if phase == "stored-run-read" and event.get("runOrigin") != "already-committed":
        errors.append("stored read RunId is not proven already committed")
    if event.get("budgetOwner") != req["budgetOwner"]:
        errors.append("wrong budget owner")
    return errors


def _closed_no_request_id(schema: dict[str, Any]) -> bool:
    required = schema.get("required") or []
    optional = schema.get("optional")
    return optional == [] and "requestId" not in required and "executionId" not in required


def check(contract: Any, *, verify_files: bool = True) -> list[str]:
    errors: list[str] = []
    if not isinstance(contract, dict):
        return ["root must be an object"]
    predecessor = load("operability.v2.json")
    evidence = load("evidence.v4.json")
    ep5 = load("evaluation-proof.v5.json")
    rt10 = load("retention-tiers.v10.json")
    d9 = load("d9-exit-contract.v1.7.json")

    if verify_files:
        for name, expected in FILES.items():
            try:
                actual = digest_file(name)
            except OSError as exc:
                errors.append(f"cannot read {name}: {exc}")
                continue
            if actual != expected:
                errors.append(f"protected file drift: {name} {actual} != {expected}")

    if contract.get("artifact") != "opensip.operability":
        errors.append("wrong artifact id")
    for key, expected in NEW_ENVELOPE.items():
        if contract.get(key) != expected:
            errors.append(f"v3 envelope drift: {key}")
    successor = contract.get("aPrimeSuccessor") or {}
    if successor.get("id") != "OPERABILITY-V3-A-PRIME-SUCCESSOR" or \
            successor.get("applicationState") != "NOT-APPLIED" or \
            successor.get("authorityClaim") != "NONE" or \
            successor.get("productAcceptance") is not False or \
            successor.get("independentCombinedRereview") != "REQUIRED":
        errors.append("candidate-only/non-authority boundary drifted")

    compat = successor.get("compatibilityProjection") or {}
    if compat.get("id") != "OP3-TO-OP2-EXACT-PROJECTION" or \
            compat.get("predecessor") != NEW_ENVELOPE["supersedes"]:
        errors.append("OP2 compatibility predecessor pin drifted")
    expected_changed = {key: {"before": OLD_ENVELOPE[key], "after": NEW_ENVELOPE[key]}
                        for key in OLD_ENVELOPE}
    if compat.get("changedRootFields") != expected_changed:
        errors.append("closed five-field envelope delta drifted")
    expected_unchanged = [key for key in predecessor if key not in OLD_ENVELOPE]
    if compat.get("unchangedTopLevelKeys") != expected_unchanged:
        errors.append("unchanged OP2 top-level key denominator drifted")
    projected = project_v2(contract)
    if projected != predecessor:
        errors.append("OP3 does not project exact-deep-equal to protected OP2")
    for key in expected_unchanged:
        if contract.get(key) != predecessor.get(key):
            errors.append(f"OP2 subtree drift outside closed delta: {key}")
    if "every nested key/list/scalar" not in compat.get("deepEqualityRule", ""):
        errors.append("compatibility projection is not explicitly recursive/exact")

    bindings = compat.get("consumerBindings") or []
    binding_map = {x.get("consumer"): x for x in bindings if isinstance(x, dict)}
    if len(binding_map) != len(bindings) or not set(CONSUMERS).issubset(binding_map):
        errors.append("known OP2 consumer binding set incomplete/duplicated")
    for consumer, paths in CONSUMERS.items():
        if (binding_map.get(consumer) or {}).get("predecessorPaths") != paths:
            errors.append(f"consumer path projection drift: {consumer}")
    all_reader = binding_map.get("check-operability.py and all other v2 readers") or {}
    if all_reader.get("predecessorPaths") != expected_unchanged:
        errors.append("complete OP2 reader projection is not closed")
    boundary = compat.get("integrationBoundary", "")
    if "narrow successor or external integration disposition" not in boundary or \
            "exact re-review" not in boundary or "not permission" not in boundary:
        errors.append("post-product integration/re-review boundary drifted")

    if gate(contract, "G16") != gate(predecessor, "G16"):
        errors.append("G16 compatibility changed")
    live_g19 = gate(contract, "G19")
    if live_g19 != gate(predecessor, "G19") or not live_g19 or \
            live_g19.get("status") != "BLOCKED-NO-MECHANISM":
        errors.append("live G19 must remain exact and blocked")

    deps = successor.get("dependencies") or {}
    expected_deps = {
        "evidence": {
            "artifact": "evidence.v4.json", "sha256": FILES["evidence.v4.json"],
            "checker": "check-evidence-v4.py", "checkerSha256": FILES["check-evidence-v4.py"]},
        "d9": {
            "artifact": "d9-exit-contract.v1.7.json", "sha256": FILES["d9-exit-contract.v1.7.json"],
            "checker": "check-d9-v1.7.py", "checkerSha256": FILES["check-d9-v1.7.py"],
            "compatibilityInvariant": "D18"},
        "retentionCustody": {
            "artifact": "retention-tiers.v10.json", "sha256": FILES["retention-tiers.v10.json"],
            "checker": "check-retention-custody.py",
            "checkerSha256": FILES["check-retention-custody.py"]},
    }
    if deps != expected_deps:
        errors.append("A-prime dependency/checker pins drifted")

    lifecycle = successor.get("lifecycle") or {}
    replacement = lifecycle.get("phaseReplacement") or {}
    if replacement.get("legacy") != "attempt-sealed" or \
            replacement.get("successor") != "run-committed" or \
            "only after the final atomic transaction commits" not in replacement.get("rule", ""):
        errors.append("attempt-sealed/run-committed phase replacement drifted")
    schema = lifecycle.get("eventSchemaV3") or {}
    if schema.get("phaseRequirements") != PHASE_REQUIREMENTS or \
            schema.get("closedPhases") != list(PHASE_REQUIREMENTS):
        errors.append("v3 event phase schema drifted")
    if schema.get("required") != predecessor["eventSchema"]["EventEnvelope"]["required"] or \
            schema.get("optional") != predecessor["eventSchema"]["EventEnvelope"]["optional"] or \
            schema.get("closedPlanes") != predecessor["eventSchema"]["EventEnvelope"]["closedPlanes"]:
        errors.append("v3 event envelope lost OP2-compatible vocabulary")
    fixtures = lifecycle.get("fixtures") or []
    fixtures_by_id = {x.get("id"): x for x in fixtures if isinstance(x, dict)}
    if len(fixtures) != 9 or len(fixtures_by_id) != 9:
        errors.append("v3 lifecycle fixture denominator is not exact nine")
    for row in fixtures:
        observed_valid = not _event_errors(row)
        if bool(row.get("valid")) != observed_valid:
            errors.append(f"lifecycle fixture disagrees with schema: {row.get('id')}")
    expected_negative_ids = {
        "op3-reject-precommit-run", "op3-reject-failed-commit-run",
        "op3-reject-run-committed-missing-run", "op3-reject-stored-read-execution",
        "op3-reject-legacy-attempt-sealed"}
    if {x.get("id") for x in fixtures if x.get("valid") is False} != expected_negative_ids:
        errors.append("v3 lifecycle negative control set drifted")

    visibility = lifecycle.get("identityVisibility") or {}
    for phrase in ("non-Display/non-Serialize", "before commit"):
        if phrase not in visibility.get("candidateRunId", ""):
            errors.append(f"precommit candidate rule omits {phrase}")
    for phrase in ("RunIndexV1", "AttemptRunLinkV1", "RunCustodyRootV1",
                   "one serializable transaction"):
        if phrase not in visibility.get("commitPoint", ""):
            errors.append(f"atomic commit point omits {phrase}")
    if "Only CommittedRunV1 exposes RunId/runSealRef" not in visibility.get("success", ""):
        errors.append("committed-only RunId exposure drifted")
    failed = visibility.get("failedFinalCommit") or {}
    expected_failed_term = {"class": "operational-failed",
                            "errorCode": "DURABILITY.COMMIT_FAILED",
                            "executionId": "$EXECUTION_ID"}
    if failed.get("termination") != expected_failed_term or \
            failed.get("forbidden") != ["runId", "runSealRef", "terminalRunCasRef"] or \
            "Run-free prepared journal" not in failed.get("rule", ""):
        errors.append("failed final commit identity boundary drifted")
    d9_failed = [x for x in d9.get("goldenCases", [])
                 if x.get("id") == "analysis-durability-failed"]
    if len(d9_failed) != 1 or "runId" in (d9_failed[0].get("expectedTermination") or {}):
        errors.append("D9 v1.7 failed-commit golden exposes/drifts RunId")
    if "already committed RunId" not in visibility.get("storedView", "") or \
            "no new ExecutionId" not in visibility.get("storedView", ""):
        errors.append("stored-view existing-Run/no-Execution boundary drifted")

    recursive = successor.get("recursiveRequestIdExclusion") or {}
    evidence_recursive = evidence.get("recursiveRequestIdExclusion") or {}
    if recursive.get("surfaces") != evidence_recursive.get("surfaces") or \
            recursive.get("closureRule") != evidence_recursive.get("rule") or \
            recursive.get("recursiveNegative") != evidence_recursive.get("negativeControl"):
        errors.append("recursive RequestId exclusion does not exactly transfer Evidence v4")
    source = recursive.get("evidenceSource") or {}
    if source != {
            "artifact": "evidence.v4.json#recursiveRequestIdExclusion",
            "artifactSha256": FILES["evidence.v4.json"],
            "checker": "check-evidence-v4.py",
            "checkerSha256": FILES["check-evidence-v4.py"]}:
        errors.append("recursive RequestId exclusion source pin drifted")

    ep_records = {x.get("name"): x for x in ep5["normativePreimageGrammar"]["records"]}
    for name in ("EvaluationAuthoritySealV1", "SemanticObjectBindingV1"):
        item = ep_records.get(name) or {}
        forbidden = item.get("forbiddenFields") or []
        fields = [x.get("name") for x in item.get("fields", [])]
        if "requestId" not in forbidden or "executionId" not in forbidden or \
                "requestId" in fields or "executionId" in fields:
            errors.append(f"EP5 {name} RequestId/ExecutionId closure drifted")
    rt_grammar = rt10["capabilityClosure"]["closureGrammar"]
    if not _closed_no_request_id(rt_grammar.get("semanticUnitSchema") or {}) or \
            not _closed_no_request_id(rt_grammar.get("semanticClosureSchema") or {}):
        errors.append("RT10 exact semantic schemas admit RequestId/ExecutionId")
    ev_grammar = evidence.get("canonicalWireGrammar") or {}
    if "no optional or undeclared bytes" not in (ev_grammar.get("recordRules") or {}).get("presence", ""):
        errors.append("Evidence exact decoder no longer rejects unknown fields")
    for name, item in (ev_grammar.get("records") or {}).items():
        required = item.get("required") or []
        fields = [x.get("name") for x in item.get("fields", [])]
        if any(x in required or x in fields for x in ("requestId", "executionId")):
            errors.append(f"Evidence semantic record admits operational identity: {name}")

    variation = recursive.get("variationFixture") or {}
    if len(set(variation.get("requestIds") or [])) != 2 or \
            len(set(variation.get("executionIds") or [])) != 2:
        errors.append("correlation stability fixture lacks two distinct identities")
    golden = evidence.get("acceptedGolden") or {}
    expected_equal = {
        "semanticEvidenceCasRef": [golden.get("semanticEvidenceCasRef")] * 2,
        "evidenceDigest": [golden.get("evidenceDigest")] * 2,
        "runId": [golden.get("runId")] * 2,
        "runSealRef": [golden.get("runSealRef")] * 2,
    }
    if variation.get("expectedEqual") != expected_equal or \
            variation.get("expectedDistinct") != ["RequestId", "ExecutionId",
                                                  "AttemptRunLinkV1"]:
        errors.append("RequestId/ExecutionId semantic differential fixture drifted")
    availability = recursive.get("availabilityFixture") or {}
    if availability.get("changesOnly") != ["effectiveCapability", "authoritative",
                                            "currentAvailability", "typedRefusal"] or \
            availability.get("invariant") != ["SemanticEvidenceV1", "EvidenceDigest",
                                               "RunId", "TerminalRunV1", "runSealRef",
                                               "sealedCapability"]:
        errors.append("availability-only projection differential drifted")

    g19 = successor.get("g19CandidateMechanism") or {}
    expected_g19_fields = {
        "liveGateId": "G19", "liveGateStatus": "BLOCKED-NO-MECHANISM",
        "candidateStatus": "SPECIFIED-PENDING-CD-RT-5-AND-INDEPENDENT-REREVIEW",
        "productState": "BLOCKED", "productDecision": "CD-RT-5 UNRESOLVED",
        "evidenceGrade": "CANDIDATE-DESIGN-INTEGRITY-ONLY",
    }
    if any(g19.get(key) != value for key, value in expected_g19_fields.items()):
        errors.append("G19 candidate/live/product state drifted")
    mechanism = g19.get("mechanism", "")
    for phrase in ("EP5", "RT10", "UNIT-ID-V3", "Evidence v4",
                   "atomic committed-only Run", "VERSIONING v5"):
        if phrase not in mechanism:
            errors.append(f"G19 candidate mechanism omits {phrase}")
    if "Do not change G19 to IMPLEMENTABLE, QUALIFIED or DEMONSTRATED" not in \
            g19.get("forbiddenPromotion", ""):
        errors.append("G19 forbidden promotion boundary drifted")
    if "narrow successor or external integration disposition" not in \
            g19.get("postProductIntegration", "") or \
            "independent re-review" not in g19.get("postProductIntegration", ""):
        errors.append("G19 post-product integration disposition drifted")

    if successor.get("reviewFindingTransfers") != evidence.get("reviewFindingTransfers"):
        errors.append("Evidence v4 review-finding transfers drifted in OP3")
    transfer_ids = {x.get("id") for x in successor.get("reviewFindingTransfers", [])
                    if isinstance(x, dict)}
    if transfer_ids != {"R12-EVD-01", "R12-DEP-01", "R14-EVD-TRANSFER", "RR13-01"}:
        errors.append("required review-finding transfer denominator incomplete")
    residuals = {x.get("id"): x.get("state") for x in successor.get("retainedResiduals", [])
                 if isinstance(x, dict)}
    if residuals != {
            "CD-RT-5": "UNRESOLVED",
            "G19": "BLOCKED-PENDING-PRODUCT-DECISION-AND-IMPLEMENTATION",
            "INDEPENDENT-COMBINED-REREVIEW": "REQUIRED",
            "POST-PRODUCT-INTEGRATION": "REQUIRED-AFTER-CD-RT-5"}:
        errors.append("OP3 residual set/state drifted")
    if not successor.get("sealRecommendation", "").startswith("DO NOT SEAL OR APPLY"):
        errors.append("OP3 no-seal/no-apply recommendation drifted")
    return errors


def selftest(contract: dict[str, Any]) -> list[str]:
    mutations: list[tuple[str, Any]] = []

    def add(name: str, fn: Any) -> None:
        mutations.append((name, fn))

    add("version", lambda x: x.__setitem__("version", 2))
    add("status", lambda x: x.__setitem__("status", "APPLIED"))
    add("authority", lambda x: x["aPrimeSuccessor"].__setitem__("authorityClaim", "SIGNED"))
    add("product", lambda x: x["aPrimeSuccessor"].__setitem__("productAcceptance", True))
    add("predecessor-pin", lambda x: x["supersedes"].__setitem__("sha256", "0" * 64))
    add("deep-subtree", lambda x: x["assuranceStateMachine"]["states"].pop())
    add("request-contract", lambda x: x["requestIdContract"]["representation"].__setitem__("regex", ".*"))
    add("g16", lambda x: gate(x, "G16").__setitem__("status", "DEMONSTRATED"))
    add("live-g19", lambda x: gate(x, "G19").__setitem__("status", "IMPLEMENTABLE"))
    add("compat-before", lambda x: x["aPrimeSuccessor"]["compatibilityProjection"]["changedRootFields"]["version"].__setitem__("before", 1))
    add("compat-keys", lambda x: x["aPrimeSuccessor"]["compatibilityProjection"]["unchangedTopLevelKeys"].pop())
    add("compat-consumer", lambda x: x["aPrimeSuccessor"]["compatibilityProjection"]["consumerBindings"].pop())
    add("integration-boundary", lambda x: x["aPrimeSuccessor"]["compatibilityProjection"].__setitem__("integrationBoundary", "automatic"))
    add("evidence-pin", lambda x: x["aPrimeSuccessor"]["dependencies"]["evidence"].__setitem__("sha256", "0" * 64))
    add("d9-pin", lambda x: x["aPrimeSuccessor"]["dependencies"]["d9"].__setitem__("sha256", "0" * 64))
    add("rt-pin", lambda x: x["aPrimeSuccessor"]["dependencies"]["retentionCustody"].__setitem__("sha256", "0" * 64))
    add("legacy-phase", lambda x: x["aPrimeSuccessor"]["lifecycle"]["phaseReplacement"].__setitem__("successor", "attempt-sealed"))
    add("precommit-schema", lambda x: x["aPrimeSuccessor"]["lifecycle"]["eventSchemaV3"]["phaseRequirements"]["attempt-admitted"].__setitem__("runId", "required"))
    add("fixture", lambda x: x["aPrimeSuccessor"]["lifecycle"]["fixtures"].pop())
    add("candidate-display", lambda x: x["aPrimeSuccessor"]["lifecycle"]["identityVisibility"].__setitem__("candidateRunId", "log candidate"))
    add("commit-atomicity", lambda x: x["aPrimeSuccessor"]["lifecycle"]["identityVisibility"].__setitem__("commitPoint", "publish event first"))
    add("failed-run", lambda x: x["aPrimeSuccessor"]["lifecycle"]["identityVisibility"]["failedFinalCommit"]["termination"].__setitem__("runId", "run1:x"))
    add("stored-execution", lambda x: x["aPrimeSuccessor"]["lifecycle"]["identityVisibility"].__setitem__("storedView", "allocate ExecutionId"))
    add("recursive-surface", lambda x: x["aPrimeSuccessor"]["recursiveRequestIdExclusion"]["surfaces"].pop())
    add("variation", lambda x: x["aPrimeSuccessor"]["recursiveRequestIdExclusion"]["variationFixture"]["expectedEqual"]["runId"].__setitem__(1, "run1:" + "0" * 64))
    add("availability", lambda x: x["aPrimeSuccessor"]["recursiveRequestIdExclusion"]["availabilityFixture"]["invariant"].pop())
    add("g19-status", lambda x: x["aPrimeSuccessor"]["g19CandidateMechanism"].__setitem__("candidateStatus", "IMPLEMENTABLE"))
    add("g19-promotion", lambda x: x["aPrimeSuccessor"]["g19CandidateMechanism"].__setitem__("forbiddenPromotion", "may promote"))
    add("transfer", lambda x: x["aPrimeSuccessor"]["reviewFindingTransfers"].pop())
    add("residual", lambda x: x["aPrimeSuccessor"]["retainedResiduals"][0].__setitem__("state", "RESOLVED"))
    add("seal", lambda x: x["aPrimeSuccessor"].__setitem__("sealRecommendation", "SEAL"))
    failures: list[str] = []
    for name, fn in mutations:
        candidate = copy.deepcopy(contract)
        fn(candidate)
        if not check(candidate, verify_files=False):
            failures.append(name)
        else:
            print(f"SELFTEST reject {name}")
    if failures:
        return ["selftest accepted mutation(s): " + ", ".join(failures)]
    print(f"SELFTEST PASS ({len(mutations)} mutations rejected)")
    return []


def main(argv: list[str]) -> int:
    args = list(argv)
    do_selftest = "--selftest" in args
    args = [x for x in args if x != "--selftest"]
    path = pathlib.Path(args[0]) if args else HERE / BINDING
    try:
        contract = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 2
    errors = check(contract)
    if not errors and do_selftest:
        errors.extend(selftest(contract))
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print(f"PASS: {path.name} exact OP2 projection and A-prime overlay are consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
