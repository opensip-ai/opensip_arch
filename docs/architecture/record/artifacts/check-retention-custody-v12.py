#!/usr/bin/env python3
"""Derived raw-custody checker for retention-tiers.v12.json.

RT12 re-derives the EP7 store-authorized graph and proves that moving store
provenance out of the candidate changes no semantic root, raw proof reference,
edge, unit, availability projection, or closure commitment from RT11.
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
BINDING = "retention-tiers.v12.json"
PREDECESSOR = "retention-tiers.v11.json"
PREDECESSOR_CHECKER = "check-retention-custody-v11.py"
EP = "evaluation-proof.v7.json"
EP_CHECKER = "check-evaluation-proof-v7.py"
RT_CORE_CHECKER = "check-retention-custody.py"
PINNED = {
    PREDECESSOR: "ba36ccf18e5154336ffa062a0c3280c6f3f010bb6eeb3807ea8daec68818c600",
    PREDECESSOR_CHECKER: "2180497df7c1c4a9a2c6a389119e8ccc7d7069c21872af97d58e657707befbfe",
    EP: "92d51e9232c6ee137b7228aa7885a2e32f668f9b4b108d7140fdb52dae864ef8",
    EP_CHECKER: "550a2231264ab6b308b3ddb752199c6496f7c2417a8dbeeb9f21c230569b36c4",
    RT_CORE_CHECKER: "15816cd8f9d22221b1187b94a160d71f644f9ab8fccb82423931fe18f6fc38d7",
}


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


def accepted(ep: dict[str, Any]) -> dict[str, Any]:
    return next(row for row in ep["positiveVectors"]
                if row.get("id") == "EP7-POS-NOMATCH-PASS")


def regenerate(contract: dict[str, Any], ep: dict[str, Any], epmod: Any,
               rtcore: Any) -> dict[str, Any]:
    vector = accepted(ep)
    store = epmod._open_test_project_store(vector["trustedStoreFixture"])
    handle = epmod.authorize_evaluation(store, vector["evaluationAuthorityCandidate"])
    epmod.assert_store_continuity(store, handle)
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
        "semanticObjectBindings": vector["evaluationAuthorityCandidate"]["semanticObjectBindings"],
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
        rt11mod = _module(PREDECESSOR_CHECKER, "rt11_pinned_for_rt12")
        epmod = _module(EP_CHECKER, "ep7_pinned_for_rt12")
        rtcore = _module(RT_CORE_CHECKER, "rtcore_pinned_for_rt12")
    except Exception as exc:
        return [f"dependency load/import failed: {type(exc).__name__}: {exc}"]
    if verify_files:
        predecessor_findings = rt11mod.check(predecessor)
        if predecessor_findings:
            errors.append(f"pinned RT11 predecessor is red: {predecessor_findings[0]}")
        ep_findings = epmod.check(ep)
        if ep_findings:
            errors.append(f"pinned EP7 source is red: {ep_findings[0]}")
    if (value.get("artifact"), value.get("version")) != ("opensip.retention-tiers", 12):
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

    changed_top = {
        "version", "supersedesAsArchitectureCandidate", "capabilityClosure",
        "authority", "retainedResiduals", "identityStabilityFromRT11",
    }
    for key in set(predecessor) - changed_top:
        if value.get(key) != predecessor[key]:
            errors.append(f"RT11 protected surface changed: {key}")
    for key in set(predecessor["capabilityClosure"]) - {"source"}:
        if (value.get("capabilityClosure") or {}).get(key) != predecessor["capabilityClosure"][key]:
            errors.append(f"RT11 exact closure surface changed: {key}")
    stability = value.get("identityStabilityFromRT11") or {}
    if stability.get("predecessorSha256") != PINNED[PREDECESSOR] or \
            stability.get("predecessorCheckerSha256") != PINNED[PREDECESSOR_CHECKER]:
        errors.append("RT11 protected hash window drift")

    source = (value.get("capabilityClosure") or {}).get("source") or {}
    if source.get("artifact") != EP or source.get("checker") != EP_CHECKER or \
            source.get("acceptedVectorId") != "EP7-POS-NOMATCH-PASS" or \
            source.get("sha256") != PINNED[EP] or \
            source.get("checkerSha256") != PINNED[EP_CHECKER]:
        errors.append("EP7 source names/hash pins drift")
    required_apis = {
        "authorize_evaluation", "validate_bundle", "resolve_semantic_object_bindings",
        "derive_semantic_requirements", "derive_raw_proof_requirements",
        "derive_dependency_edges", "derive_transitive_requirements",
        "encode_semantic_object_binding", "assert_store_continuity",
    }
    if set(source.get("requiredCheckerApi") or []) != required_apis:
        errors.append("EP7 checker API import set drift")
    try:
        expected = regenerate(value, ep, epmod, rtcore)
    except Exception as exc:
        errors.append(f"EP7 raw graph regeneration failed: {type(exc).__name__}: {exc}")
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
        errors.append("SemanticCapabilityClosureV3 is not exact EP7-derived closure")
    if closure != predecessor["capabilityClosure"]["semanticClosure"]:
        errors.append("EP7 authority change altered RT11 closure identities")
    counts = (closure_root.get("closureGoldens") or {}).get("derivedCounts")
    if counts != expected["counts"] or counts != {
            "rawRequirementCount": 23, "dependencyEdgeCount": 20,
            "unitCount": 2, "verifiableCount": 19, "replayableCount": 4}:
        errors.append("exact 23/20/2 (19/4) derived counts drift")
    unit_values = [row.get("unitId") for row in expected["units"]]
    if unit_values != [
            "unit3:sha256:5c6c613a74f68e39a5052a06274fa612888a63c327f0a1c8ae03c86ede1b9adc",
            "unit3:sha256:22311dbe7dd9fd958d1946e6795a2add39298a41fa6eb82f918ee61c312054ed"]:
        errors.append("exact RT11 unit identities drift")
    if expected["closureCommitment"] != \
            "sha256:156ac0017a65c026a2e939c728fc189aa81728ad827c2218e1b4ccce8924c626":
        errors.append("exact RT11 closure commitment drift")
    serialized_closure = json.dumps(closure)
    if any(term in serialized_closure for term in (
            "storeInstanceToken", "transactionToken", "indexGeneration",
            "ProjectStoreAuthorityV1")):
        errors.append("operational store token/type leaked into custody identity")
    authority = value.get("authority") or {}
    if authority.get("candidateState") != "NOT-APPLIED" or \
            "operational-only" not in authority.get("storeTokenRule", ""):
        errors.append("store-token authority boundary drift")
    residuals = json.dumps(value.get("retainedResiduals") or [])
    if not all(term in residuals for term in (
            "No production ProjectStoreAuthority", "atomicity", "V10", "CD-RT-5", "G19")):
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
    add("EP7 checker pin", lambda c: c["capabilityClosure"]["source"].__setitem__(
        "checkerSha256", "0" * 64))
    add("predecessor pin", lambda c: c["identityStabilityFromRT11"].__setitem__(
        "predecessorSha256", "0" * 64))
    add("store token in closure", lambda c: c["capabilityClosure"]["semanticClosure"].__setitem__(
        "storeInstanceToken", "forged"))
    add("assurance elevation", lambda c: c["assurance"].__setitem__("state", "QUALIFIED"))
    for label, candidate in mutations:
        if not check(candidate, verify_files=False):
            failures.append(f"{label} escaped")
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
        print("PASS: retention-tiers.v12.json; 12 mutations rejected; exact RT11 identities stable")
    else:
        print(f"PASS: retention-tiers.v12.json; {counts['rawRequirementCount']} derived raw refs / "
              f"{counts['dependencyEdgeCount']} canonical edges / {counts['unitCount']} units "
              f"({counts['verifiableCount']} verifiable/{counts['replayableCount']} replayable)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
