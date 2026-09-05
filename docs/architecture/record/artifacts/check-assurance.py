#!/usr/bin/env python3
"""Cross-artifact assurance-state checker.

R2-FINAL-02 found that several otherwise green surface checkers promoted an
``implementable:true`` declaration to DISCHARGED even though no product, corpus,
or retained execution existed.  OPERABILITY already contained the right state
machine; this checker makes it the single source and adapts every load-bearing
surface to it without confusing Run custody capabilities with product evidence.

Usage: python3 artifacts/check-assurance.py [contract] [--selftest]
"""
from __future__ import annotations

import copy
import json
import pathlib
import sys
from typing import Any


HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
BINDING = "assurance-state.v1.json"
REGISTER = "claim-register.v1.json"
TOTALITY_ROOT_CASES = (
    ("string", "hostile-root"),
    ("null", None),
    ("list", []),
    ("empty-object", {}),
)
MALFORMED_SHAPE_EXCEPTIONS = (
    AttributeError, IndexError, KeyError, StopIteration, TypeError, ValueError,
)

CANONICAL_STATES = [
    "SPECIFIED",
    "IMPLEMENTABLE",
    "QUALIFIED",
    "DEMONSTRATED",
    "BLOCKED-NO-MECHANISM",
    "PARTIAL",
]
EXPECTED_MODES = {
    "D9": "NO-LIVE-ASSURANCE-TABLE",
    "FACT-PLANE": "NO-LIVE-ASSURANCE-TABLE",
    "C-2": "LEGACY-PROPERTY-TABLE",
    "EVIDENCE": "RUN-ASSURANCE-ORTHOGONAL",
    "RESOLVED-INPUTS": "NO-LIVE-ASSURANCE-TABLE",
    "FACT-IDENTITY": "LEGACY-PROPERTY-TABLE",
    "VERSIONING": "LEGACY-PROPERTY-TABLE",
    "OPERABILITY": "CANONICAL-GATES",
    "DELIVERY": "CANONICAL-PROPERTY-TABLE",
    "TM": "DERIVED-PUBLICATION",
    "R-1": "LEGACY-PROPERTY-TABLE",
}
ARCH_ASSURANCE_KEYS = {
    "dischargeStatus", "assuranceStatus", "assuranceStateMachine", "releaseDecision"
}


def load_json(path: pathlib.Path) -> dict:
    return json.loads(path.read_text())


def at_path(value: Any, dotted: str) -> Any:
    current = value
    for part in dotted.split(".") if dotted else []:
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def named_key_paths(value: Any, names: set[str], prefix: str = "") -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            path = f"{prefix}.{key}" if prefix else key
            if key in names:
                found.append(path)
            found.extend(named_key_paths(child, names, path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(named_key_paths(child, names, f"{prefix}[{index}]"))
    return found


def record_errors(record: dict) -> list[str]:
    """Validate one generic assurance record used by contract fixtures."""
    errors: list[str] = []
    state = record.get("state")
    allowed = set(CANONICAL_STATES) | {"DISCHARGED", "NOT DISCHARGED", "CONDITIONAL"}
    if state not in allowed:
        return [f"unknown state {state!r}"]
    if state in {"IMPLEMENTABLE", "QUALIFIED", "DEMONSTRATED"}:
        for key in ("target", "positiveCase", "negativeControls"):
            if not record.get(key):
                errors.append(f"{state} lacks {key}")
    if state in {"QUALIFIED", "DEMONSTRATED"}:
        if not record.get("qualificationEvidenceIds"):
            errors.append(f"{state} lacks qualificationEvidenceIds")
        if "observedFailure" in record:
            errors.append("a boolean observedFailure is not retained evidence")
    if state == "DEMONSTRATED" and not record.get("releaseEvidenceIds"):
        errors.append("DEMONSTRATED lacks releaseEvidenceIds")
    if state == "DISCHARGED" and (
            record.get("evidenceGrade") != "DEMONSTRATED"
            or not record.get("demonstrationEvidenceIds")):
        errors.append("DISCHARGED lacks DEMONSTRATED grade and demonstrationEvidenceIds")
    if state == "CONDITIONAL" and not record.get("condition"):
        errors.append("CONDITIONAL lacks its enumerated condition")
    return errors


def binding_artifacts(register: dict, overrides: dict[str, dict] | None = None) -> tuple[dict, list[str]]:
    by_id = {claim.get("id"): claim for claim in register.get("claims", [])}
    artifacts: dict[str, dict] = {}
    errors: list[str] = []
    overrides = overrides or {}
    for claim_id in EXPECTED_MODES:
        if claim_id in overrides:
            artifacts[claim_id] = overrides[claim_id]
            continue
        claim = by_id.get(claim_id)
        binding = claim.get("bindingArtifact") if claim else None
        if not binding:
            errors.append(f"AS-COVER {claim_id}: no live bindingArtifact in the register")
            continue
        rel = binding.split("#", 1)[0]
        path = ROOT / rel
        if not path.exists():
            errors.append(f"AS-COVER {claim_id}: live binding {rel} is missing")
            continue
        try:
            artifacts[claim_id] = load_json(path)
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"AS-COVER {claim_id}: cannot load {rel}: {exc}")
    return artifacts, errors


def check_legacy_table(claim_id: str, artifact: dict, path: str) -> list[str]:
    errors: list[str] = []
    table = at_path(artifact, path)
    if not isinstance(table, dict) or not isinstance(table.get("properties"), list):
        return [f"AS-STATE {claim_id}: {path} is not a property assurance table"]
    rule = str(table.get("rule", "")).lower()
    bad_rules = ("only implementable tests discharge",
                 "discharged only by tests marked implementable:true")
    explicitly_non_evidentiary = (
        " not " in rule or "never" in rule or "feasibility metadata only" in rule
    )
    if any(text in rule for text in bad_rules) or not (
            "demonstrat" in rule and "implementable" in rule
            and explicitly_non_evidentiary):
        errors.append(
            f"AS-STATE {claim_id}: table rule does not forbid implementable-only discharge"
        )
    tests = {item.get("id"): item for item in artifact.get("conformanceTests", [])}
    allowed = set(CANONICAL_STATES) | {"DISCHARGED", "NOT DISCHARGED", "CONDITIONAL"}
    for prop in table["properties"]:
        name = prop.get("property", "?")
        state = prop.get("status")
        refs = prop.get("dischargedBy", [])
        if state not in allowed:
            errors.append(f"AS-STATE {claim_id}/{name}: unknown state {state!r}")
            continue
        for test_id in refs:
            test = tests.get(test_id)
            if test is None:
                errors.append(f"AS-STATE {claim_id}/{name}: unknown test {test_id}")
            elif not test.get("implementable"):
                errors.append(
                    f"AS-STATE {claim_id}/{name}: test reference {test_id} is not implementable"
                )
        if state == "SPECIFIED" and refs and \
                prop.get("evidenceGrade") != "IMPLEMENTABLE_UNEXECUTED":
            errors.append(
                f"AS-STATE {claim_id}/{name}: unexecuted specification lacks "
                "IMPLEMENTABLE_UNEXECUTED grade"
            )
        if state in {"DISCHARGED", "DEMONSTRATED"} and (
                prop.get("evidenceGrade") != "DEMONSTRATED"
                or not prop.get("demonstrationEvidenceIds")):
            errors.append(
                f"AS-STATE {claim_id}/{name}: {state} lacks retained DEMONSTRATED evidence"
            )
        if state == "QUALIFIED" and not prop.get("qualificationEvidenceIds"):
            errors.append(f"AS-STATE {claim_id}/{name}: QUALIFIED lacks retained evidence")
        if state == "CONDITIONAL" and not prop.get("condition"):
            errors.append(f"AS-STATE {claim_id}/{name}: CONDITIONAL lacks a condition")
    return errors


def check_operability(artifact: dict) -> list[str]:
    errors: list[str] = []
    machine = artifact.get("assuranceStateMachine", {})
    if machine.get("states") != CANONICAL_STATES or not machine.get("closed"):
        errors.append("AS-CANON: OPERABILITY state machine is not the exact closed source")
    rules = " ".join(machine.get("rules", [])).lower()
    if "implementable:true never means qualified or demonstrated" not in rules:
        errors.append("AS-CANON: canonical rules permit an implementable-only promotion")

    gates = {gate.get("id"): gate for gate in artifact.get("validationGates", [])}
    for gate_id, gate in gates.items():
        state = gate.get("status")
        if state not in CANONICAL_STATES:
            errors.append(f"AS-OP {gate_id}: unknown canonical state {state!r}")
            continue
        probe = {**gate, "state": state}
        for error in record_errors(probe):
            errors.append(f"AS-OP {gate_id}: {error}")

    props = artifact.get("requiredPropertyRegistry", {}).get("properties", [])
    demonstrated = {
        prop.get("id") for prop in props
        if any(gates.get(gid, {}).get("status") == "DEMONSTRATED"
               and gates.get(gid, {}).get("qualificationEvidenceIds")
               and gates.get(gid, {}).get("releaseEvidenceIds")
               for gid in prop.get("gateIds", []))
    }
    blocked = sorted({prop.get("id") for prop in props} - demonstrated)
    decision = artifact.get("releaseDecision", {})
    expected = "RELEASABLE" if not blocked else "BLOCKED"
    if decision.get("state") != expected or \
            sorted(decision.get("blockedPropertyIds", [])) != blocked or \
            decision.get("demonstratedPropertyCount") != len(demonstrated):
        errors.append("AS-OP: releaseDecision is not derived from DEMONSTRATED evidence")
    return errors


def check_delivery(artifact: dict) -> list[str]:
    errors: list[str] = []
    table = artifact.get("assuranceStatus", {})
    if table.get("vocabularySource") != \
            "artifacts/operability.v2.json#assuranceStateMachine":
        errors.append("AS-DL: DELIVERY does not cite the canonical state machine")
    properties = table.get("properties", [])
    for prop in properties:
        state = prop.get("state")
        if state not in CANONICAL_STATES:
            errors.append(f"AS-DL {prop.get('id')}: unknown state {state!r}")
            continue
        probe = {**prop, "state": state}
        # DELIVERY's testIds are its SPECIFIED/IMPLEMENTABLE target until a
        # property advances; higher states must carry retained identities here.
        if state in {"QUALIFIED", "DEMONSTRATED"}:
            for error in record_errors(probe):
                errors.append(f"AS-DL {prop.get('id')}: {error}")
    all_demo = bool(properties) and all(
        prop.get("state") == "DEMONSTRATED"
        and prop.get("qualificationEvidenceIds")
        and prop.get("releaseEvidenceIds")
        for prop in properties
    )
    expected = "DEMONSTRATED" if all_demo else "NOT-DEMONSTRATED"
    if table.get("releaseState") != expected:
        errors.append("AS-DL: releaseState is not derived from retained property evidence")
    return errors


def check_threat(model: dict, operability: dict) -> list[str]:
    errors: list[str] = []
    gates = {gate.get("id"): gate for gate in operability.get("validationGates", [])}
    demonstrated = {
        gid for gid, gate in gates.items()
        if gate.get("status") == "DEMONSTRATED"
        and gate.get("qualificationEvidenceIds")
        and gate.get("releaseEvidenceIds")
    }
    properties = model.get("requiredProperties", [])
    blocked = sorted(
        prop.get("id") for prop in properties
        if not prop.get("gateIds")
        or not all(gate_id in demonstrated for gate_id in prop.get("gateIds", []))
    )
    current = model.get("shipGate", {}).get("currentState", {})
    expected_publication = "BLOCKED" if blocked else "PUBLISHABLE"
    if not current.get("derived") or \
            sorted(current.get("demonstratedGateIds", [])) != sorted(demonstrated) or \
            sorted(current.get("blockedPropertyIds", [])) != blocked or \
            current.get("publicationState") != expected_publication:
        errors.append("AS-TM: publication state is not derived from DEMONSTRATED gates")
    return errors


def _check(policy: dict, register: dict,
           overrides: dict[str, dict] | None = None) -> list[str]:
    errors: list[str] = []

    canonical = policy.get("canonicalStateMachine", {})
    if canonical.get("source") != "artifacts/operability.v2.json#assuranceStateMachine" or \
            canonical.get("states") != CANONICAL_STATES or \
            not canonical.get("noImplicitTransition"):
        errors.append("AS-CANON: policy does not bind the exact OPERABILITY state machine")
    invariant_ids = {item.get("id") for item in policy.get("invariants", [])}
    if invariant_ids != {f"AS-{index}" for index in range(1, 9)}:
        errors.append("AS-CANON: invariant set is not exactly AS-1..AS-8")
    compat = policy.get("compatibilityVocabulary", {})
    if compat.get("DISCHARGED", {}).get("mapsTo") != "DEMONSTRATED" or \
            compat.get("IMPLEMENTABLE_UNEXECUTED", {}).get("countsAsExecutionEvidence") is not False:
        errors.append("AS-CANON: compatibility vocabulary permits a paper discharge")

    coverage = policy.get("surfaceCoverage", {})
    adapters_list = coverage.get("adapters", [])
    adapters = {adapter.get("claimId"): adapter for adapter in adapters_list}
    if coverage.get("exactCount") != len(EXPECTED_MODES) or \
            len(adapters) != len(adapters_list) or set(adapters) != set(EXPECTED_MODES):
        errors.append("AS-COVER: adapter denominator is not the exact eleven surfaces")
    for claim_id, mode in EXPECTED_MODES.items():
        if adapters.get(claim_id, {}).get("mode") != mode:
            errors.append(f"AS-COVER {claim_id}: missing or wrong adapter mode")

    artifacts, load_errors = binding_artifacts(register, overrides)
    errors.extend(load_errors)
    for claim_id, expected_mode in EXPECTED_MODES.items():
        artifact = artifacts.get(claim_id)
        adapter = adapters.get(claim_id, {})
        if artifact is None:
            continue
        if expected_mode in {"NO-LIVE-ASSURANCE-TABLE", "RUN-ASSURANCE-ORTHOGONAL"}:
            unexpected = named_key_paths(artifact, ARCH_ASSURANCE_KEYS)
            if unexpected:
                errors.append(
                    f"AS-COVER {claim_id}: unadapted architecture assurance tables {unexpected}"
                )
        elif expected_mode == "LEGACY-PROPERTY-TABLE":
            errors.extend(check_legacy_table(claim_id, artifact, adapter.get("path", "")))
        elif expected_mode == "CANONICAL-GATES":
            errors.extend(check_operability(artifact))
        elif expected_mode == "CANONICAL-PROPERTY-TABLE":
            errors.extend(check_delivery(artifact))

    if "TM" in artifacts and "OPERABILITY" in artifacts:
        errors.extend(check_threat(artifacts["TM"], artifacts["OPERABILITY"]))

    fixture_ids: set[str] = set()
    for fixture in policy.get("fixtures", []):
        fixture_id = fixture.get("id")
        if fixture_id in fixture_ids:
            errors.append(f"AS-FX {fixture_id}: duplicate fixture id")
        fixture_ids.add(fixture_id)
        got = record_errors(fixture.get("record", {}))
        if fixture.get("valid") and got:
            errors.append(f"AS-FX {fixture_id}: expected valid — {got[0]}")
        elif not fixture.get("valid") and not got:
            errors.append(f"AS-FX {fixture_id}: expected rejection")
    if len(fixture_ids) < 8:
        errors.append("AS-FX: fixture corpus is incomplete")
    return errors


def check(policy: object, register: dict,
          overrides: dict[str, dict] | None = None) -> list[str]:
    """Total policy boundary for every parsed JSON root shape."""
    if not isinstance(policy, dict) or not policy:
        return ["AS-TOTALITY-ROOT: policy root must be a non-empty object"]
    coverage = policy.get("surfaceCoverage")
    if not isinstance(coverage, dict) or not isinstance(coverage.get("adapters"), list):
        return ["AS-TOTALITY-SHAPE: surfaceCoverage.adapters must be an array"]
    try:
        return _check(policy, register, overrides)
    except MALFORMED_SHAPE_EXCEPTIONS as exc:
        return [f"AS-TOTALITY-EXCEPTION: malformed policy shape "
                f"({type(exc).__name__})"]


def selftest(policy: dict, register: dict) -> int:
    base_artifacts, load_errors = binding_artifacts(register)
    base = load_errors + check(policy, register, base_artifacts)
    if base:
        print(f"REFUSING to self-test: base policy has {len(base)} finding(s)")
        for item in base[:10]:
            print("  -", item)
        return 1

    def mutate_policy_drop_adapter(p: dict, _: dict[str, dict]) -> None:
        p["surfaceCoverage"]["adapters"].pop()

    def mutate_discharge(surface: str, property_index: int = 0):
        def mutation(_: dict, artifacts: dict[str, dict]) -> None:
            prop = artifacts[surface]["dischargeStatus"]["properties"][property_index]
            prop["status"] = "DISCHARGED"
            prop.pop("evidenceGrade", None)
            prop.pop("demonstrationEvidenceIds", None)
        return mutation

    def mutate_op_qualified(_: dict, artifacts: dict[str, dict]) -> None:
        artifacts["OPERABILITY"]["validationGates"][0]["status"] = "QUALIFIED"
        artifacts["OPERABILITY"]["validationGates"][0]["observedFailure"] = True

    def mutate_op_demo_without_release(_: dict, artifacts: dict[str, dict]) -> None:
        gate = artifacts["OPERABILITY"]["validationGates"][0]
        gate["status"] = "DEMONSTRATED"
        gate["qualificationEvidenceIds"] = ["qe-1"]
        gate["releaseEvidenceIds"] = []

    def mutate_false_release(_: dict, artifacts: dict[str, dict]) -> None:
        decision = artifacts["OPERABILITY"]["releaseDecision"]
        decision["state"] = "RELEASABLE"
        decision["blockedPropertyIds"] = []

    def mutate_delivery_demo(_: dict, artifacts: dict[str, dict]) -> None:
        artifacts["DELIVERY"]["assuranceStatus"]["properties"][0]["state"] = "DEMONSTRATED"

    def mutate_threat_publish(_: dict, artifacts: dict[str, dict]) -> None:
        current = artifacts["TM"]["shipGate"]["currentState"]
        current["publicationState"] = "PUBLISHABLE"
        current["blockedPropertyIds"] = []

    def mutate_hidden_table(_: dict, artifacts: dict[str, dict]) -> None:
        artifacts["D9"]["assuranceStatus"] = {"properties": []}

    def mutate_canonical_machine(_: dict, artifacts: dict[str, dict]) -> None:
        artifacts["OPERABILITY"]["assuranceStateMachine"]["states"].remove("QUALIFIED")

    mutations = [
        ("omit one surface adapter (AS-8)", mutate_policy_drop_adapter),
        ("C-2 implementable:true becomes DISCHARGED (AS-1/4)", mutate_discharge("C-2", 1)),
        ("FACT-IDENTITY implementable:true becomes DISCHARGED (AS-1/4)",
         mutate_discharge("FACT-IDENTITY", 0)),
        ("VERSIONING implementable:true becomes DISCHARGED (AS-1/4)",
         mutate_discharge("VERSIONING", 0)),
        ("R-1 implementable:true becomes DISCHARGED (AS-1/4)", mutate_discharge("R-1", 1)),
        ("QUALIFIED uses a boolean instead of retained evidence (AS-2)", mutate_op_qualified),
        ("DEMONSTRATED omits release evidence (AS-3)", mutate_op_demo_without_release),
        ("editorially declare release ready (AS-6)", mutate_false_release),
        ("DELIVERY property demonstrated without evidence (AS-3)", mutate_delivery_demo),
        ("publish threat claims from implementable gates (AS-6)", mutate_threat_publish),
        ("hide an unadapted assurance table on D9 (AS-8)", mutate_hidden_table),
        ("drift the canonical state set (AS-1..6)", mutate_canonical_machine),
    ]

    print("assurance mutation self-test — each row must be REJECTED\n")
    escaped = 0
    for name, root in TOTALITY_ROOT_CASES:
        findings = check(copy.deepcopy(root), register, base_artifacts)
        if not findings:
            escaped += 1
        print(f"  {'reject' if findings else 'ESCAPE':>6}  parsed-JSON root {name}")
        print(f"          {findings[0] if findings else 'NO FINDING — root survived'}")
    for name, mutation in mutations:
        candidate_policy = copy.deepcopy(policy)
        candidate_artifacts = copy.deepcopy(base_artifacts)
        mutation(candidate_policy, candidate_artifacts)
        findings = check(candidate_policy, register, candidate_artifacts)
        if not findings:
            escaped += 1
        print(f"  {'reject' if findings else 'ESCAPE':>6}  {name}")
        print(f"          {findings[0] if findings else 'NO FINDING — mutation survived'}")
    print()
    if escaped:
        print(f"{escaped}/{len(mutations) + len(TOTALITY_ROOT_CASES)} retained cases ESCAPED")
        return 1
    print(f"all {len(mutations)} semantic mutations and {len(TOTALITY_ROOT_CASES)} "
          "root-shape cases rejected — implementability cannot self-promote")
    return 0


def main() -> int:
    args = [arg for arg in sys.argv[1:] if arg != "--selftest"]
    path = pathlib.Path(args[0]) if args else HERE / BINDING
    if not path.exists():
        print(f"missing contract: {path}", file=sys.stderr)
        return 2
    try:
        policy = load_json(path)
        register = load_json(HERE / REGISTER)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"cannot load assurance inputs: {exc}", file=sys.stderr)
        return 2
    if "--selftest" in sys.argv:
        return selftest(policy, register)
    findings = check(policy, register)
    if findings:
        print(f"{len(findings)} assurance finding(s):")
        for item in findings:
            print("  -", item)
        return 1
    print("assurance state OK — 11/11 surfaces adapted; AS-1..AS-8 clean")
    print("  architecture checks remain design integrity; product release remains evidence-derived")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
