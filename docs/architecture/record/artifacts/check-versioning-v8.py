#!/usr/bin/env python3
"""Conformance checker for the narrow VERSIONING v8 EP8/RT13 cold-read rejoin."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import pathlib
import sys
from typing import Any


HERE = pathlib.Path(__file__).resolve().parent
DEFAULT = HERE / "versioning-policy.v8.json"
PREDECESSOR = "versioning-policy.v7.json"
PREDECESSOR_CHECKER = "check-versioning-v7.py"
EP = "evaluation-proof.v8.json"
EP_CHECKER = "check-evaluation-proof-v8.py"
RT = "retention-tiers.v13.json"
RT_CHECKER = "check-retention-custody-v13.py"
PINS = {
    PREDECESSOR: "0c0f2d7396c32854c3cd5a6aff794c6a0e1be2ffe833816f9ff66f0089b49985",
    PREDECESSOR_CHECKER: "27cc2e22dd909de2ee3050387f87129477ee050e5b25c541dcf305902fbb9d76",
    EP: "4bb33f772c8c510c470643082f6bfb8a4df28a050b4720dda6cdd5187bd3e303",
    EP_CHECKER: "c80ac50e21dcd350e5f5285958a6cfb94d52c5c3f7d64f2396d91b544fa82769",
    RT: "3f79668a6d26b5ecc7fd843be71aef90e779ac024a1ac54bb5cc2c8fc3e0a349",
    RT_CHECKER: "0290b4ae22816843c2fbce1288ea36f21e78b396361fa6c0bf5291338be519f6",
}
CHANGED = {
    "version", "decisionDependencies", "knownLimitations", "supersedes",
    "role", "successorRevision",
}
CURRENT_DEPENDENCY_LABELS = [
    "evaluation-proof.v8.json (durable cold stored-read authority reconstruction; current candidate)",
    "retention-tiers.v13.json (cold-reconstruction custody identity rejoin; current candidate)",
]
ADDED_LIMITATIONS = [
    "VERSIONING v8 preserves v7 historical-verifier custody and every semantic/versioned identity; it only rejoins current authority to EP8/RT13 cold stored-read reconstruction.",
    "EP8/RT13 exercise an in-memory cold-open specification. They do not demonstrate a production restart, durable backend, transaction, recovery or atomicity implementation.",
    "EP8/RT13 are the only current successor dependencies. Older EP/RT labels retained in protected predecessor material describe historical candidate lineage, not current inputs.",
]
OPERATIONAL_EXCLUSIONS = [
    "EvaluationAuthorityIndexV1",
    "cold reconstruction traversal",
    "candidate cache and inventory assertions",
    "ProjectStoreAuthorityV1/store-instance/transaction tokens",
]
EXPECTED_REVISION_KEYS = {
    "id", "candidateState", "supersedesCandidate", "inputs",
    "rawAuthorityKinds", "custodyRule", "storeAuthorityRule",
    "identityStability", "forbiddenBackEdge", "coldStoredReadRejoin",
    "dependencyLabelRule",
}


def load(path: pathlib.Path) -> Any:
    return json.loads(path.read_text())


def sha_file(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


def module(filename: str, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    if spec is None or spec.loader is None:
        raise ImportError(filename)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def check(value: Any, *, verify_files: bool = True) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["root is not an object"]
    try:
        for name, expected in PINS.items():
            if sha_file(name) != expected:
                raise ValueError(f"pinned input drift: {name}")
        predecessor = load(HERE / PREDECESSOR)
        ep = load(HERE / EP)
        rt = load(HERE / RT)
        oldmod = module(PREDECESSOR_CHECKER, "versioning_v7_pinned_for_v8")
        epmod = module(EP_CHECKER, "ep8_pinned_for_versioning_v8")
        rtmod = module(RT_CHECKER, "rt13_pinned_for_versioning_v8")
    except Exception as exc:
        return [f"predecessor/dependency import failed: {type(exc).__name__}: {exc}"]

    if verify_files:
        old_errors = oldmod.check(predecessor)
        if old_errors:
            errors.append(f"VERSIONING v7 predecessor is red: {old_errors[0]}")
        ep_errors = epmod.check(ep)
        if ep_errors:
            errors.append(f"EP8 dependency is red: {ep_errors[0]}")
        rt_errors = rtmod.check(rt)
        if rt_errors:
            errors.append(f"RT13 dependency is red: {rt_errors[0]}")

    if set(value) != set(predecessor):
        errors.append("top-level surface differs from VERSIONING v7")
    for key in set(predecessor) - CHANGED:
        if value.get(key) != predecessor.get(key):
            errors.append(f"protected VERSIONING v7 section changed: {key}")

    if (value.get("artifact"), value.get("version")) != (
            "opensip.versioning-policy", 8):
        errors.append("artifact/version mismatch")
    if value.get("status") != "CANDIDATE-NOT-APPLIED" or \
            value.get("reviewStatus") != "AWAITING-INDEPENDENT-COMBINED-REREVIEW" or \
            value.get("supersedes") != 7:
        errors.append("candidate/review/supersession state drift")
    if value.get("role") != \
            "A-prime v4 cold stored-read reconstruction versioning rejoin":
        errors.append("narrow successor role drift")

    expected_dependencies = (
        predecessor.get("decisionDependencies", [])[:-2] +
        CURRENT_DEPENDENCY_LABELS
    )
    if value.get("decisionDependencies") != expected_dependencies:
        errors.append("current dependency labels are not exactly EP8/RT13")
    if value.get("knownLimitations") != \
            predecessor.get("knownLimitations", []) + ADDED_LIMITATIONS:
        errors.append("successor limitation delta is not exact")

    revision = value.get("successorRevision") or {}
    if set(revision) != EXPECTED_REVISION_KEYS:
        errors.append("successor revision is not closed")
    if revision.get("id") != "VERSIONING-v8-COLD-STORED-READ-SUCCESSOR" or \
            revision.get("candidateState") != "NOT-APPLIED":
        errors.append("successor identity/state drift")
    if revision.get("supersedesCandidate") != {
            "artifact": PREDECESSOR,
            "sha256": PINS[PREDECESSOR],
            "checker": PREDECESSOR_CHECKER,
            "checkerSha256": PINS[PREDECESSOR_CHECKER],
    }:
        errors.append("VERSIONING v7 protected predecessor pin drift")
    expected_inputs = {
        "evaluationProof": {
            "artifact": EP, "sha256": PINS[EP], "checker": EP_CHECKER,
            "checkerSha256": PINS[EP_CHECKER],
        },
        "retentionCustody": {
            "artifact": RT, "sha256": PINS[RT], "checker": RT_CHECKER,
            "checkerSha256": PINS[RT_CHECKER],
        },
    }
    if revision.get("inputs") != expected_inputs:
        errors.append("EP8/RT13 dependency pins drift")
    if any("evidence" in json.dumps(row).lower()
           for row in (revision.get("inputs") or {}).values()
           if isinstance(row, dict)):
        errors.append("VERSIONING v8 contains an Evidence dependency back-edge")

    old_revision = predecessor.get("successorRevision") or {}
    for key in ("rawAuthorityKinds", "custodyRule", "storeAuthorityRule"):
        if revision.get(key) != old_revision.get(key):
            errors.append(f"exact v7 raw/custody contract changed: {key}")
    if revision.get("identityStability") != {
            "predecessor": "VERSIONING-v7",
            "state": "EXACT-CUSTODY-IDENTITIES-UNCHANGED",
            "reason": "Only cold stored-read reconstruction/port continuity changed.",
    }:
        errors.append("v7 identity stability statement drift")
    forbidden = revision.get("forbiddenBackEdge", "")
    if not all(term in forbidden for term in (
            "Evidence", "RunId", "TerminalRunV1", "RunAuthorityIndexV1",
            "ProjectStoreAuthority token", "store transaction token",
            "VERSIONING-v8")):
        errors.append("forbidden downstream/store-token back-edge rule incomplete")

    cold = revision.get("coldStoredReadRejoin") or {}
    if set(cold) != {
            "state", "sourceContracts", "rule", "operationalIdentityExclusions",
            "identityRule", "productionRestartClaim"}:
        errors.append("cold stored-read rejoin is not closed")
    if cold.get("state") != "SPECIFIED-IMPLEMENTABLE-UNEXECUTED" or \
            cold.get("sourceContracts") != {
                "evaluationProof": "storedAuthorityReconstructionContract",
                "retentionCustody": "authority",
            }:
        errors.append("cold stored-read authority sources/state drift")
    if cold.get("operationalIdentityExclusions") != OPERATIONAL_EXCLUSIONS:
        errors.append("index/traversal/cache/store-token exclusions drift")
    identity_rule = cold.get("identityRule", "")
    if not all(term in identity_rule for term in (
            "Index rows", "traversal", "cache/inventory", "store/transaction",
            "operational-only", "semantic commitment", "raw custody identity",
            "versioned identity")):
        errors.append("operational identity-exclusion rule incomplete")
    cold_rule = cold.get("rule", "")
    if not all(term in cold_rule for term in (
            "newly opened", "immutable CAS rows", "EvaluationAuthorityIndexV1",
            "Caller candidate", "warm cache", "not authority")):
        errors.append("cold stored-read reconstruction rule incomplete")
    runtime_claim = cold.get("productionRestartClaim", "")
    if not runtime_claim.startswith("NONE;") or not all(
            term in runtime_claim for term in (
                "not a production restart", "durable store", "transaction",
                "recovery", "atomicity")):
        errors.append("no-production-restart claim drift")
    if revision.get("dependencyLabelRule") != (
            "Current successor inputs are exactly evaluation-proof.v8.json and "
            "retention-tiers.v13.json. Older EP/RT labels in byte-preserved "
            "predecessor sections are historical lineage only."):
        errors.append("current-versus-historical dependency label rule drift")

    ep_stability = ep.get("identityStabilityFromEP7") or {}
    if ep_stability.get("predecessorArtifact") != "evaluation-proof.v7.json" or \
            ep_stability.get("predecessorSha256") != \
            "92d51e9232c6ee137b7228aa7885a2e32f668f9b4b108d7140fdb52dae864ef8" or \
            ep_stability.get("allowedChange") != (
                "Durable cold stored-read reconstruction only; no semantic/content/"
                "proof identity input changes."):
        errors.append("EP8 semantic-identity stability declaration drift")
    ep_cold = ep.get("storedAuthorityReconstructionContract") or {}
    if "candidate cache" not in ep_cold.get("forbiddenAuthorityInputs", []) or \
            "warm process state" not in ep_cold.get("forbiddenAuthorityInputs", []) or \
            "not a production" not in ep_cold.get("notRuntimeClaim", ""):
        errors.append("EP8 cold-reconstruction non-authority/non-runtime rule drift")

    rt_stability = rt.get("identityStabilityFromRT12") or {}
    if rt_stability.get("operationalExclusions") != [
            "cold reconstruction traversal", "EvaluationAuthorityIndexV1",
            "candidate/cache/inventory state", "store/host/transaction capabilities",
    ] or rt_stability.get("reason") != (
            "EP8 cold reconstruction is operational admission machinery and is "
            "excluded from semantic/raw custody identity."):
        errors.append("RT13 custody-identity stability declaration drift")
    rt_authority = rt.get("authority") or {}
    if not rt_authority.get("productionExecutionClaim", "").startswith("NONE;") or \
            "cold index traversal" not in rt_authority.get("storeTokenRule", ""):
        errors.append("RT13 operational-only/no-production claim drift")

    expected_discharge = {
        "state": "SPECIFIED", "evidenceGrade": "IMPLEMENTABLE_UNEXECUTED",
        "candidateState": "NOT-APPLIED", "qualificationEvidenceIds": [],
        "releaseEvidenceIds": [], "V10": "UNRESOLVED", "CD-RT-5": "BLOCKED",
        "G19": "BLOCKED", "seal": "DO-NOT-SEAL",
    }
    if value.get("dischargeStatus") != expected_discharge:
        errors.append("VERSIONING v8 discharge/non-authority state drift")
    return errors


def selftest(value: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    cases: list[tuple[str, dict[str, Any]]] = []

    def add(label: str, mutate: Any) -> None:
        candidate = copy.deepcopy(value)
        mutate(candidate)
        cases.append((label, candidate))

    add("historical verifier custody", lambda c: c["historicalSemanticsPolicy"].__setitem__(
        "bindingRule", "changed"))
    add("custody class", lambda c: c["custodyClasses"][0].__setitem__("class", "INTERNAL"))
    add("versioned identity", lambda c: c["versionedIdentities"].pop())
    add("raw kind omission", lambda c: c["successorRevision"]["rawAuthorityKinds"].pop())
    add("custody rule", lambda c: c["successorRevision"].__setitem__(
        "custodyRule", "SemanticCommitmentRef is physical"))
    add("predecessor pin", lambda c: c["successorRevision"]["supersedesCandidate"].__setitem__(
        "sha256", "0" * 64))
    add("EP8 pin", lambda c: c["successorRevision"]["inputs"]["evaluationProof"].__setitem__(
        "sha256", "0" * 64))
    add("RT13 pin", lambda c: c["successorRevision"]["inputs"]["retentionCustody"].__setitem__(
        "checkerSha256", "0" * 64))
    add("stale current label", lambda c: c["decisionDependencies"].__setitem__(
        -2, "evaluation-proof.v7.json (current)"))
    add("index identity leak", lambda c: c["successorRevision"]["coldStoredReadRejoin"][
        "operationalIdentityExclusions"].pop(0))
    add("warm cache authority", lambda c: c["successorRevision"]["coldStoredReadRejoin"].__setitem__(
        "rule", "Warm cache is authority."))
    add("production restart inflation", lambda c: c["successorRevision"][
        "coldStoredReadRejoin"].__setitem__("productionRestartClaim", "DEMONSTRATED"))
    add("Evidence back-edge", lambda c: c["successorRevision"]["inputs"].__setitem__(
        "evidence", {"artifact": "evidence.v7.json"}))
    add("identity stability inflation", lambda c: c["successorRevision"][
        "identityStability"].__setitem__("state", "CHANGED"))
    add("seal inflation", lambda c: c["dischargeStatus"].__setitem__("seal", "SEAL"))
    for label, candidate in cases:
        if not check(candidate, verify_files=False):
            failures.append(f"{label} escaped")
    return failures


def main(argv: list[str]) -> int:
    positional = [arg for arg in argv[1:] if arg != "--selftest"]
    path = pathlib.Path(positional[0]) if positional else DEFAULT
    try:
        value = load(path)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    errors = check(value)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    if "--selftest" in argv[1:]:
        failures = selftest(value)
        if failures:
            for failure in failures:
                print(f"SELFTEST-FAIL: {failure}")
            return 1
        print("PASS: versioning-policy.v8.json; 15 successor mutations rejected")
    else:
        print("PASS: versioning-policy.v8.json; EP8/RT13 cold stored-read rejoined; "
              "v7 custody/identities exact; no production restart or Evidence back-edge")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
