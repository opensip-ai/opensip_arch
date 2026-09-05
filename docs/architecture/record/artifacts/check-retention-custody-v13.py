#!/usr/bin/env python3
"""Cold-derived raw-custody checker for retention-tiers.v13.json.

RT13 opens EP8's durable-row fixture as a never-warm store and obtains the sole
authority handle through resolve_stored_evaluation.  It proves that cold
reconstruction changes no RT12 semantic root, raw proof reference, edge, unit,
availability/purge/lease/D9 surface, or closure commitment.  This checker is
architecture evidence only; it makes no production restart or store claim.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import pathlib
import sys
from typing import Any


HERE = pathlib.Path(__file__).resolve().parent
BINDING = "retention-tiers.v13.json"
PREDECESSOR = "retention-tiers.v12.json"
PREDECESSOR_CHECKER = "check-retention-custody-v12.py"
EP = "evaluation-proof.v8.json"
EP_CHECKER = "check-evaluation-proof-v8.py"
RT_CORE_CHECKER = "check-retention-custody.py"
PINNED = {
    PREDECESSOR: "1a034746512de51605b7a4bcc4fb0936bdc167db057a3018be74a2a047376dab",
    PREDECESSOR_CHECKER: "104a8f9bd01e92226c11c41c234358b5a9d991b42cf12ec9318582ed12b57851",
    EP: "4bb33f772c8c510c470643082f6bfb8a4df28a050b4720dda6cdd5187bd3e303",
    EP_CHECKER: "c80ac50e21dcd350e5f5285958a6cfb94d52c5c3f7d64f2396d91b544fa82769",
    RT_CORE_CHECKER: "15816cd8f9d22221b1187b94a160d71f644f9ab8fccb82423931fe18f6fc38d7",
}

EXPECTED_COUNTS = {
    "rawRequirementCount": 23,
    "dependencyEdgeCount": 20,
    "unitCount": 2,
    "verifiableCount": 19,
    "replayableCount": 4,
}
EXPECTED_UNIT_IDS = [
    "unit3:sha256:5c6c613a74f68e39a5052a06274fa612888a63c327f0a1c8ae03c86ede1b9adc",
    "unit3:sha256:22311dbe7dd9fd958d1946e6795a2add39298a41fa6eb82f918ee61c312054ed",
]
EXPECTED_CLOSURE_COMMITMENT = \
    "sha256:156ac0017a65c026a2e939c728fc189aa81728ad827c2218e1b4ccce8924c626"
EXPECTED_PROJECTION_HASHES = {
    "semanticClosure": "70ce71b8fc31551809c7c800a165fa5d9a8a8e04a7e5523e7668324fce8a977c",
    "availability": "f53af4bc27a771ef5b72a7be1b7b39b66a58b4831bf9402b47c1fcafbca22916",
    "purgeAndLineage": "09c03454779cb884d4d904df66511c45942056e6c4b22579723979bff0325145",
    "leaseProtocol": "a0023a4ab71568ceb902a0fba356d2483d152d2d3762e68541285d3f2b853c7b",
    "d9Derivation": "fd7b659debd36f3c955cfb26a9af4a97968707d0d22fd54cb2cb275106317e87",
}
SELFTEST_MUTATION_COUNT = 21


class DuplicateKeyError(ValueError):
    pass


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise DuplicateKeyError(key)
        value[key] = item
    return value


def load(name_or_path: str | pathlib.Path) -> Any:
    path = pathlib.Path(name_or_path)
    if not path.is_absolute() and path.parent == pathlib.Path("."):
        path = HERE / path
    return json.loads(path.read_text(), object_pairs_hook=_pairs)


def sha_file(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


def _module(filename: str, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    if spec is None or spec.loader is None:
        raise ImportError(filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def canonical_sha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def accepted(ep: dict[str, Any]) -> dict[str, Any]:
    return next(row for row in ep["positiveVectors"]
                if row.get("id") == "EP8-POS-NOMATCH-PASS")


def regenerate(contract: dict[str, Any], ep: dict[str, Any], epmod: Any,
               rtcore: Any) -> dict[str, Any]:
    vector = accepted(ep)
    fixture = copy.deepcopy(vector["trustedStoreFixture"])
    candidate = vector["evaluationAuthorityCandidate"]
    store = epmod._open_test_project_store(fixture)
    # This is the decisive construction boundary.  The newly opened store has
    # only flattened immutable CAS and index rows.  It has never received the
    # candidate and no warm cache/inventory member may exist.
    if any(hasattr(store._state, name)
           for name in ("_candidate", "_candidates", "_inventory", "_cache")):
        raise ValueError("never-warm store contains candidate/cache/inventory state")
    eas_ref = candidate["evaluationAuthorityAdmission"]["evaluationAuthoritySealRef"]
    handle = epmod.resolve_stored_evaluation(store, eas_ref)
    if handle._candidate != candidate:
        raise ValueError("cold reconstruction differs from accepted EP8 candidate")
    epmod.assert_store_continuity(store, handle)
    findings = epmod.validate_bundle(vector["bundle"], handle)
    if findings:
        raise ValueError(f"cold-reconstructed handle rejected by pure core: {findings[0]}")
    proof_refs = epmod.derive_raw_proof_requirements(vector["bundle"], handle)
    edges = epmod.derive_dependency_edges(vector["bundle"], handle)
    roots = sorted(epmod.derive_semantic_requirements(handle), key=canonical)
    grouped = {"verifiable": [], "replayable": []}
    for row in proof_refs:
        grouped[row["requiredForCapability"]].append({
            "projectId": row["projectId"], "recordCasRef": row["recordCasRef"],
            "recordKind": row["recordKind"],
        })
    rtcore._set_closure_grammar(contract["capabilityClosure"]["closureGrammar"])
    units = []
    for capability in ("verifiable", "replayable"):
        refs = grouped[capability]
        if refs:
            unit = {"unitId": "", "projectId": vector["bundle"]["projectId"],
                    "requiredForCapability": capability, "objectRefs": refs}
            unit["unitId"] = rtcore.derive_unit_id(unit["projectId"], capability, refs)
            units.append(unit)
    return {
        "projectId": vector["bundle"]["projectId"],
        "semanticObjectBindings": copy.deepcopy(handle._candidate["semanticObjectBindings"]),
        "semanticRoots": roots,
        "proofRefs": proof_refs,
        "dependencyEdges": edges,
        "units": units,
        "closureCommitment": rtcore.semantic_closure_commitment(units),
        "counts": {
            "rawRequirementCount": len(proof_refs),
            "dependencyEdgeCount": len(edges), "unitCount": len(units),
            "verifiableCount": len(grouped["verifiable"]),
            "replayableCount": len(grouped["replayable"]),
        },
    }


def check(value: Any, *, verify_files: bool = True) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["root is not an object"]
    try:
        for filename, expected in PINNED.items():
            if sha_file(filename) != expected:
                raise ValueError(f"pinned input drift: {filename}")
        predecessor = load(PREDECESSOR)
        ep = load(EP)
        rt12mod = _module(PREDECESSOR_CHECKER, "rt12_pinned_for_rt13")
        epmod = _module(EP_CHECKER, "ep8_pinned_for_rt13")
        rtcore = _module(RT_CORE_CHECKER, "rtcore_pinned_for_rt13")
    except Exception as exc:
        return [f"dependency load/import failed: {type(exc).__name__}: {exc}"]
    if verify_files:
        predecessor_findings = rt12mod.check(predecessor)
        if predecessor_findings:
            errors.append(f"pinned RT12 predecessor is red: {predecessor_findings[0]}")
        ep_findings = epmod.check(ep)
        if ep_findings:
            errors.append(f"pinned EP8 source is red: {ep_findings[0]}")
    if (value.get("artifact"), value.get("version")) != ("opensip.retention-tiers", 13):
        errors.append("artifact/version mismatch")
    if value.get("status") != "CANDIDATE-NOT-APPLIED" or \
            value.get("sealRecommendation") != "DO-NOT-SEAL":
        errors.append("candidate/no-seal boundary drift")
    assurance = value.get("assurance") or {}
    if assurance != {
            "state": "SPECIFIED", "evidenceGrade": "IMPLEMENTABLE_UNEXECUTED",
            "qualificationEvidenceIds": [], "releaseEvidenceIds": [],
            "candidateState": "NOT-APPLIED"}:
        errors.append("assurance exceeds specified/implementable-unexecuted")
    integration = value.get("integrationState") or {}
    if {key: integration.get(key) for key in ("V10", "CD-RT-5", "G19")} != {
            "V10": "UNRESOLVED", "CD-RT-5": "BLOCKED", "G19": "BLOCKED"}:
        errors.append("V10/CD-RT-5/G19 residual state drift")

    changed_predecessor_top = {
        "version", "supersedesAsArchitectureCandidate", "capabilityClosure",
        "authority", "retainedResiduals", "identityStabilityFromRT11",
    }
    expected_top = (set(predecessor) - changed_predecessor_top) | {
        "version", "supersedesAsArchitectureCandidate", "capabilityClosure",
        "authority", "retainedResiduals", "identityStabilityFromRT12",
    }
    if set(value) != expected_top:
        errors.append("RT13 root is not the exact closed successor shape")
    if value.get("supersedesAsArchitectureCandidate") != PREDECESSOR:
        errors.append("RT12 successor binding drift")
    for key in set(predecessor) - changed_predecessor_top:
        if value.get(key) != predecessor[key]:
            errors.append(f"RT12 protected surface changed: {key}")
    for key in set(predecessor["capabilityClosure"]) - {"source"}:
        if (value.get("capabilityClosure") or {}).get(key) != predecessor["capabilityClosure"][key]:
            errors.append(f"RT12 exact closure surface changed: {key}")

    stability = value.get("identityStabilityFromRT12") or {}
    expected_stability = {
        "predecessorArtifact": PREDECESSOR,
        "predecessorSha256": PINNED[PREDECESSOR],
        "predecessorChecker": PREDECESSOR_CHECKER,
        "predecessorCheckerSha256": PINNED[PREDECESSOR_CHECKER],
        "exactUnchanged": [
            "semantic roots/bindings",
            "23 proof refs and 20 dependency edges",
            "two UNIT-ID-V3 values",
            "closure commitment",
            "availability projections",
            "purge/lineage semantics",
            "lease semantics",
            "D9 derivation semantics",
        ],
        "identityGoldens": {
            "derivedCounts": EXPECTED_COUNTS,
            "unitIds": EXPECTED_UNIT_IDS,
            "closureCommitment": EXPECTED_CLOSURE_COMMITMENT,
            "canonicalSha256": EXPECTED_PROJECTION_HASHES,
        },
        "operationalExclusions": [
            "cold reconstruction traversal",
            "EvaluationAuthorityIndexV1",
            "candidate/cache/inventory state",
            "store/host/transaction capabilities",
        ],
        "reason": "EP8 cold reconstruction is operational admission machinery and is excluded from semantic/raw custody identity.",
    }
    if stability != expected_stability:
        errors.append("RT12 identity-stability/hash window drift")

    source = (value.get("capabilityClosure") or {}).get("source") or {}
    required_apis = {
        "resolve_stored_evaluation", "validate_bundle", "resolve_semantic_object_bindings",
        "derive_semantic_requirements", "derive_raw_proof_requirements",
        "derive_dependency_edges", "derive_transitive_requirements",
        "encode_semantic_object_binding", "assert_store_continuity",
    }
    expected_source = {
        "artifact": EP,
        "sha256": PINNED[EP],
        "checker": EP_CHECKER,
        "checkerSha256": PINNED[EP_CHECKER],
        "acceptedVectorId": "EP8-POS-NOMATCH-PASS",
        "requiredCheckerApi": sorted(required_apis),
        "coldGraphConstruction": {
            "stateOrigin": "trustedStoreFixture immutable CAS records plus EvaluationAuthorityIndexV1 rows",
            "handleConstructor": "resolve_stored_evaluation",
            "resolverArguments": ["ProjectStoreAuthorityV1", "EvaluationAuthoritySealRef"],
            "callerCandidateInput": "FORBIDDEN",
            "warmAuthorization": "FORBIDDEN",
            "candidateCacheOrInventory": "FORBIDDEN",
        },
    }
    if source != expected_source:
        errors.append("EP8 cold source/API/hash binding drift")
    try:
        expected = regenerate(value, ep, epmod, rtcore)
    except Exception as exc:
        errors.append(f"EP8 cold raw graph regeneration failed: {type(exc).__name__}: {exc}")
        return errors
    closure_root = value.get("capabilityClosure") or {}
    expected_closure = {
        "schemaVersion": 3, "projectId": expected["projectId"],
        "sealedCapability": "replayable",
        "semanticObjectBindings": expected["semanticObjectBindings"],
        "semanticRoots": expected["semanticRoots"], "proofRefs": expected["proofRefs"],
        "dependencyEdges": expected["dependencyEdges"], "units": expected["units"],
        "closureCommitment": expected["closureCommitment"],
    }
    closure = closure_root.get("semanticClosure") or {}
    if closure != expected_closure:
        errors.append("SemanticCapabilityClosureV3 is not exact cold EP8-derived closure")
    if closure != predecessor["capabilityClosure"]["semanticClosure"]:
        errors.append("EP8 cold reconstruction altered RT12 closure identities")
    counts = (closure_root.get("closureGoldens") or {}).get("derivedCounts")
    if counts != expected["counts"] or counts != EXPECTED_COUNTS:
        errors.append("exact 23/20/2 (19/4) derived counts drift")
    unit_values = [row.get("unitId") for row in expected["units"]]
    if unit_values != EXPECTED_UNIT_IDS:
        errors.append("exact RT12 UNIT-ID-V3 identities drift")
    if expected["closureCommitment"] != EXPECTED_CLOSURE_COMMITMENT:
        errors.append("exact RT12 closure commitment drift")

    availability = {
        "unitAvailabilityRecords": closure_root.get("unitAvailabilityRecords"),
        "availabilityFixtures": closure_root.get("availabilityFixtures"),
    }
    projections = {
        "semanticClosure": closure,
        "availability": availability,
        "purgeAndLineage": value.get("storageAndLineage"),
        "leaseProtocol": value.get("leaseProtocol"),
        "d9Derivation": value.get("d9Derivation"),
    }
    observed_hashes = {key: canonical_sha(item) for key, item in projections.items()}
    if observed_hashes != EXPECTED_PROJECTION_HASHES:
        errors.append("RT12 availability/purge/lease/D9 projection identity drift")

    identity_projection = {
        "semanticClosure": closure,
        "closureGoldens": closure_root.get("closureGoldens"),
        "closureGrammar": closure_root.get("closureGrammar"),
        "unitAvailabilityRecords": closure_root.get("unitAvailabilityRecords"),
        "availabilityFixtures": closure_root.get("availabilityFixtures"),
    }
    serialized_identity = canonical(identity_projection).decode("utf-8").lower()
    forbidden_operational_terms = (
        "projectstoreauthority", "trustedstorestate", "hostprojectadmission",
        "evaluationauthorityindex", "coldreconstruction", "warmprocess",
        "candidatecache", "inventoryassertion", "storeinstancetoken",
        "transactiontoken", "indexgeneration", "fixtureonly",
        "trustedstorefixture", "_candidate", "_inventory", "_cache",
    )
    if any(term in serialized_identity for term in forbidden_operational_terms):
        errors.append("cold reconstruction/index/cache machinery leaked into retention identity")
    authority = value.get("authority") or {}
    expected_authority = {
        "candidateState": "NOT-APPLIED",
        "authorityClaim": "NONE",
        "source": "EP8 resolve_stored_evaluation over a never-warm durable-row fixture and the unchanged exact raw receipt graph",
        "coldResolutionRule": "The accepted graph is regenerated only from a newly opened fixture store plus EvaluationAuthoritySealRef; caller candidate, warm authorize_evaluation, cache and inventory assertions are forbidden.",
        "storeTokenRule": "ProjectStoreAuthority/store/transaction tokens and cold index traversal are operational-only and forbidden from semantic roots, proof refs, edges, units, closure commitment, availability keys and retention identity.",
        "productionExecutionClaim": "NONE; checker-only in-memory cold fixture reconstruction is not a production restart, store, durability, recovery or atomicity demonstration.",
    }
    if authority != expected_authority:
        errors.append("cold/store-token authority boundary drift")
    residuals = json.dumps(value.get("retainedResiduals") or [])
    if not all(term in residuals for term in (
            "No production ProjectStoreAuthority", "not a production restart",
            "atomicity", "V10", "CD-RT-5", "G19")):
        errors.append("required implementation/atomicity/residual limits absent")
    return errors


def selftest(contract: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    mutations = []

    def add(label: str, mutate: Any) -> None:
        candidate = copy.deepcopy(contract)
        mutate(candidate)
        mutations.append((label, candidate))

    add("proof ref removal", lambda c: c["capabilityClosure"]["semanticClosure"]["proofRefs"].pop())
    add("dependency edge removal", lambda c: c["capabilityClosure"]["semanticClosure"]["dependencyEdges"].pop())
    add("receipt edge removal", lambda c: c["capabilityClosure"]["semanticClosure"]["dependencyEdges"].__setitem__(
        slice(None), [edge for edge in c["capabilityClosure"]["semanticClosure"]["dependencyEdges"]
                      if edge["role"] != "admitted-resolved-inputs"]))
    add("snapshot content edge removal", lambda c: c["capabilityClosure"]["semanticClosure"]["dependencyEdges"].__setitem__(
        slice(None), [edge for edge in c["capabilityClosure"]["semanticClosure"]["dependencyEdges"]
                      if edge["role"] != "snapshot-content"]))
    add("semantic ref as raw", lambda c: c["capabilityClosure"]["semanticClosure"]["proofRefs"][0].__setitem__(
        "semanticRef", "sha256:" + "0" * 64))
    add("authored count", lambda c: c["capabilityClosure"]["closureGoldens"]["derivedCounts"].__setitem__(
        "rawRequirementCount", 22))
    add("unit ref removal", lambda c: c["capabilityClosure"]["semanticClosure"]["units"][0]["objectRefs"].pop())
    add("closure commitment", lambda c: c["capabilityClosure"]["semanticClosure"].__setitem__(
        "closureCommitment", "sha256:" + "f" * 64))
    add("EP8 artifact pin", lambda c: c["capabilityClosure"]["source"].__setitem__(
        "sha256", "0" * 64))
    add("EP8 checker pin", lambda c: c["capabilityClosure"]["source"].__setitem__(
        "checkerSha256", "0" * 64))
    add("EP8 accepted vector", lambda c: c["capabilityClosure"]["source"].__setitem__(
        "acceptedVectorId", "EP8-POS-ERROR"))
    add("warm-authorize substitution", lambda c: c["capabilityClosure"]["source"]
        ["coldGraphConstruction"].__setitem__("handleConstructor", "authorize_evaluation"))
    add("caller candidate substitution", lambda c: c["capabilityClosure"]["source"]
        ["coldGraphConstruction"].__setitem__("callerCandidateInput", "REQUIRED"))
    add("predecessor artifact pin", lambda c: c["identityStabilityFromRT12"].__setitem__(
        "predecessorSha256", "0" * 64))
    add("predecessor checker pin", lambda c: c["identityStabilityFromRT12"].__setitem__(
        "predecessorCheckerSha256", "0" * 64))
    add("cold index leakage into closure", lambda c: c["capabilityClosure"]
        ["semanticClosure"].__setitem__("evaluationAuthorityIndexRef", "sha256:" + "7" * 64))
    add("cache leakage into proof ref", lambda c: c["capabilityClosure"]
        ["semanticClosure"]["proofRefs"][0].__setitem__("candidateCacheKey", "warm"))
    add("index leakage into edge", lambda c: c["capabilityClosure"]
        ["semanticClosure"]["dependencyEdges"][0].__setitem__("indexGeneration", 1))
    add("inventory leakage into unit", lambda c: c["capabilityClosure"]
        ["semanticClosure"]["units"][0]["objectRefs"][0].__setitem__(
            "inventoryAssertion", True))
    add("cold machinery in retention identity", lambda c: c["capabilityClosure"]
        ["closureGoldens"].__setitem__("candidateCache", "forged"))
    add("assurance elevation", lambda c: c["assurance"].__setitem__("state", "QUALIFIED"))
    for label, candidate in mutations:
        if not check(candidate, verify_files=False):
            failures.append(f"{label} escaped")
    if len(mutations) != SELFTEST_MUTATION_COUNT:
        failures.append(
            f"selftest mutation inventory drift: {len(mutations)} != {SELFTEST_MUTATION_COUNT}")
    return failures


def main(argv: list[str]) -> int:
    path = pathlib.Path(next((arg for arg in argv[1:] if arg != "--selftest"),
                             str(HERE / BINDING)))
    try:
        value = load(path)
    except (OSError, UnicodeError, json.JSONDecodeError, DuplicateKeyError) as exc:
        print(f"ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    errors = check(value)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    counts = value["capabilityClosure"]["closureGoldens"]["derivedCounts"]
    if "--selftest" in argv[1:]:
        failures = selftest(value)
        if failures:
            for failure in failures:
                print(f"SELFTEST-FAIL: {failure}")
            return 1
        print(f"PASS: retention-tiers.v13.json; {SELFTEST_MUTATION_COUNT} mutations rejected; "
              "cold EP8 derivation; exact RT12 identities stable")
    else:
        print(f"PASS: retention-tiers.v13.json; {counts['rawRequirementCount']} cold-derived raw refs / "
              f"{counts['dependencyEdgeCount']} canonical edges / {counts['unitCount']} units "
              f"({counts['verifiableCount']} verifiable/{counts['replayableCount']} replayable)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
