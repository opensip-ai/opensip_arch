#!/usr/bin/env python3
"""Derived raw-custody checker for retention-tiers.v11.json.

RT11 preserves the reviewed RT10 lease/purge/availability machinery and replaces
its authored 22/16 fixture with the exact EP6 admitted receipt graph.
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
BINDING = "retention-tiers.v11.json"
PREDECESSOR = "retention-tiers.v10.json"
PREDECESSOR_CHECKER = "check-retention-custody.py"
EP = "evaluation-proof.v6.json"
EP_CHECKER = "check-evaluation-proof-v6.py"
PINNED_PREDECESSOR = "606b5e7125d4a3a46f44f1a7565f9c9ea69132d9ab2783d00339e1b8aac5e026"
PINNED_PREDECESSOR_CHECKER = "15816cd8f9d22221b1187b94a160d71f644f9ab8fccb82423931fe18f6fc38d7"
PINNED_FINAL_REVIEW = "9a10cd8a3f02e0d46b9c9e5e8aed7e607f05b946f8d59c0b029bf6758d978f02"
STABLE_SECTIONS = ["leaseProtocol", "storageAndLineage", "d9Derivation", "custodyPolicy", "invariants"]


class DuplicateKeyError(ValueError):
    pass


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def load(name_or_path: str | pathlib.Path) -> Any:
    path = pathlib.Path(name_or_path)
    if not path.is_absolute() and path.parent == pathlib.Path("."):
        path = HERE / path
    return json.loads(path.read_text(), object_pairs_hook=_pairs)


def sha_file(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


def _module(filename: str, name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    if spec is None or spec.loader is None:
        raise ImportError(filename)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def accepted(ep: dict[str, Any]) -> dict[str, Any]:
    return next(row for row in ep["positiveVectors"]
                if row.get("id") == "EP6-POS-NOMATCH-PASS")


def regenerate(contract: dict[str, Any], ep: dict[str, Any], epmod: Any,
               rtmod: Any) -> dict[str, Any]:
    vector = accepted(ep)
    handle = epmod.admit_evaluation_authority(vector["authorityAdmissionInput"])
    proof_refs = epmod.derive_raw_proof_requirements(vector["bundle"], handle)
    edges = epmod.derive_dependency_edges(vector["bundle"], handle)
    roots = sorted(epmod.derive_semantic_requirements(handle), key=canonical)
    grouped = {"verifiable": [], "replayable": []}
    for row in proof_refs:
        grouped[row["requiredForCapability"]].append({
            "projectId": row["projectId"], "recordCasRef": row["recordCasRef"],
            "recordKind": row["recordKind"],
        })
    grammar = contract["capabilityClosure"]["closureGrammar"]
    rtmod._set_closure_grammar(grammar)
    units = []
    for capability in ("verifiable", "replayable"):
        refs = grouped[capability]
        if refs:
            unit = {"unitId": "", "projectId": vector["bundle"]["projectId"],
                    "requiredForCapability": capability, "objectRefs": refs}
            unit["unitId"] = rtmod.derive_unit_id(
                unit["projectId"], capability, refs)
            units.append(unit)
    commitment = rtmod.semantic_closure_commitment(units)
    return {
        "projectId": vector["bundle"]["projectId"],
        "semanticObjectBindings": vector["authorityAdmissionInput"]["semanticObjectBindings"],
        "semanticRoots": roots,
        "proofRefs": proof_refs,
        "dependencyEdges": edges,
        "units": units,
        "closureCommitment": commitment,
        "counts": {
            "rawRequirementCount": len(proof_refs),
            "dependencyEdgeCount": len(edges),
            "unitCount": len(units),
            "verifiableCount": len(grouped["verifiable"]),
            "replayableCount": len(grouped["replayable"]),
        },
    }


def check(value: Any, *, verify_files: bool = True) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["root is not an object"]
    try:
        predecessor = load(PREDECESSOR)
        ep = load(EP)
        rtmod = _module(PREDECESSOR_CHECKER, "rt10_pinned_for_rt11")
        epmod = _module(EP_CHECKER, "ep6_pinned_for_rt11")
    except Exception as exc:
        return [f"dependency load/import failed: {type(exc).__name__}: {exc}"]
    if sha_file(PREDECESSOR) != PINNED_PREDECESSOR or \
            sha_file(PREDECESSOR_CHECKER) != PINNED_PREDECESSOR_CHECKER:
        errors.append("RT10 predecessor artifact/checker drift")
    if sha_file("retention-tiers.v10.rereview-independent-final.json") != PINNED_FINAL_REVIEW:
        errors.append("final predecessor rereview drift")
    if verify_files:
        # A predecessor PASS establishes only the stable mechanisms explicitly
        # inherited below; it is not successor acceptance.
        predecessor_findings = rtmod.check(predecessor)
        if predecessor_findings:
            errors.append(f"pinned RT10 predecessor mechanism is red: {predecessor_findings[0]}")
    if (value.get("artifact"), value.get("version")) != ("opensip.retention-tiers", 11):
        errors.append("artifact/version mismatch")
    if value.get("status") != "CANDIDATE-NOT-APPLIED" or \
            value.get("sealRecommendation") != "DO-NOT-SEAL":
        errors.append("candidate/no-seal boundary drift")
    for key in STABLE_SECTIONS:
        if value.get(key) != predecessor.get(key):
            errors.append(f"protected RT10 mechanism changed: {key}")
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
    transfer = (value.get("authority") or {}).get("reviewTransfer") or {}
    if transfer.get("sha256") != PINNED_FINAL_REVIEW or \
            transfer.get("verdict") != "REQUIRED-CHANGES/DO-NOT-SEAL" or \
            transfer.get("passedPredecessorMechanismsOnly") != [
                "RR13-03", "Versioning custody rejoin"]:
        errors.append("final predecessor review is misrepresented")

    closure_root = value.get("capabilityClosure") or {}
    source = closure_root.get("source") or {}
    if source.get("artifact") != EP or source.get("checker") != EP_CHECKER:
        errors.append("EP6 source names drift")
    if source.get("sha256") != sha_file(EP) or \
            source.get("checkerSha256") != sha_file(EP_CHECKER):
        errors.append("EP6 source hash pins drift")
    required_apis = {
        "admit_evaluation_authority", "resolve_semantic_object_bindings",
        "derive_semantic_requirements", "derive_raw_proof_requirements",
        "derive_dependency_edges", "derive_transitive_requirements",
        "encode_semantic_object_binding", "validate_bundle",
    }
    if set(source.get("requiredCheckerApi") or []) != required_apis:
        errors.append("EP6 checker API import set drift")
    try:
        expected = regenerate(value, ep, epmod, rtmod)
    except Exception as exc:
        errors.append(f"EP6 raw graph regeneration failed: {type(exc).__name__}: {exc}")
        return errors
    closure = closure_root.get("semanticClosure") or {}
    expected_closure = {
        "schemaVersion": 3,
        "projectId": expected["projectId"],
        "sealedCapability": "replayable",
        "semanticObjectBindings": expected["semanticObjectBindings"],
        "semanticRoots": expected["semanticRoots"],
        "proofRefs": expected["proofRefs"],
        "dependencyEdges": expected["dependencyEdges"],
        "units": expected["units"],
        "closureCommitment": expected["closureCommitment"],
    }
    if closure != expected_closure:
        errors.append("SemanticCapabilityClosureV3 is not exact EP6-derived closure")
    counts = (closure_root.get("closureGoldens") or {}).get("derivedCounts")
    if counts != expected["counts"]:
        errors.append("raw requirement/edge/unit counts are authored or stale")
    proof_refs = closure.get("proofRefs") if isinstance(closure, dict) else []
    if not isinstance(proof_refs, list) or any(
            not isinstance(row, dict) or row.get("identityKind") != "raw-cas"
            or "semanticRef" in row or "semanticDomain" in row for row in proof_refs):
        errors.append("proofRefs are not raw-only discriminated identities")
    edges = closure.get("dependencyEdges") if isinstance(closure, dict) else []
    if not isinstance(edges, list) or any(
            not isinstance(edge, dict) or set(edge) != {"fromRef", "toRef", "projectId", "role"}
            for edge in edges):
        errors.append("dependency edges are not exact raw-only records")
    required_receipt_edge = next(
        (edge for edge in expected["dependencyEdges"] if edge["role"] == "admitted-resolved-inputs"), None)
    required_content_edges = [edge for edge in expected["dependencyEdges"]
                              if edge["role"] == "snapshot-content"]
    if required_receipt_edge not in edges or not required_content_edges or \
            any(edge not in edges for edge in required_content_edges):
        errors.append("receipt/resolved-input/snapshot-content typed lineage missing")
    unit_goldens = (closure_root.get("closureGoldens") or {}).get("units")
    if not isinstance(unit_goldens, list) or len(unit_goldens) != len(expected["units"]):
        errors.append("unit goldens incomplete")
    else:
        for row, unit in zip(unit_goldens, expected["units"]):
            preimage = rtmod.unit_id_preimage(
                unit["projectId"], unit["requiredForCapability"], unit["objectRefs"])
            encoded = rtmod.encode_semantic_custody_unit(unit)
            if row.get("value") != unit or row.get("unitIdPreimageHex") != preimage.hex() or \
                    row.get("derivedUnitId") != unit["unitId"] or \
                    row.get("encodedHex") != encoded.hex():
                errors.append(f"unit golden drift: {row.get('id')}")
    availability = closure_root.get("unitAvailabilityRecords") or []
    if len(availability) != len(expected["units"]):
        errors.append("availability record count differs from derived units")
    else:
        for record, unit in zip(availability, expected["units"]):
            if record.get("unitId") != unit["unitId"] or \
                    [{key: item[key] for key in ("projectId", "recordCasRef", "recordKind")}
                     for item in record.get("objectStates", [])] != unit["objectRefs"] or \
                    any(item.get("state") != "AVAILABLE" for item in record.get("objectStates", [])):
                errors.append("availability record is not exact unit projection")
    negative_kinds = {row.get("kind") for row in closure_root.get("negativeFixtures", [])
                      if isinstance(row, dict)}
    if not {"receipt-resolved-input-edge-removed", "snapshot-content-edge-removed",
            "semantic-ref-as-cas"}.issubset(negative_kinds):
        errors.append("RT11 authority/raw adversarial matrix incomplete")
    raw_rule = json.dumps(value.get("rawPhysicalIdentityContract") or {})
    if not all(term in raw_rule for term in ("raw-only", "RawCasRef", "snapshot body")):
        errors.append("raw physical identity rule does not cover successor receipt/body graph")
    return errors


def selftest(contract: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    mutations = []
    def add(label: str, mutate) -> None:
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
    add("review verdict", lambda c: c["authority"]["reviewTransfer"].__setitem__("verdict", "PASS"))
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
        print("PASS: retention-tiers.v11.json; 9 successor mutations rejected; raw-only receipt custody clean")
    else:
        print(f"PASS: retention-tiers.v11.json; {counts['rawRequirementCount']} derived raw refs / "
              f"{counts['dependencyEdgeCount']} canonical edges / {counts['unitCount']} units "
              f"({counts['verifiableCount']} verifiable/{counts['replayableCount']} replayable)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
