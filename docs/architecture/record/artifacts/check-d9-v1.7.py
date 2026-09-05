#!/usr/bin/env python3
"""Executable successor checker for d9-exit-contract.v1.7.json.

The reviewed v1.6 checker remains byte-for-byte frozen.  This checker delegates
all D0..D16 checks to it, then proves the v1.7 delta is closed:

  D17 RunId is never exposed by a failed final commit and every RunId-bearing
      retained golden denotes a committed Run.
  D18 v1.7 is exactly v1.6 plus metadata rollover, one lifecycle invariant,
      updated reproduction commands, and removal of the single stale RunId.

Usage: python3 artifacts/check-d9-v1.7.py [contract]  ·  --selftest
Exit:  0 clean · 1 findings · 2 IO error
"""
from __future__ import annotations

import copy
import importlib.util
import json
import pathlib
import sys
from typing import Any


HERE = pathlib.Path(__file__).resolve().parent
BINDING = "d9-exit-contract.v1.7.json"
PREDECESSOR = "d9-exit-contract.v1.6.json"
EXPECTED_VERSION = "v1.7"
EXPECTED_STATUS = (
    "CANDIDATE-UNREVIEWED (v1.7 RunId commit-visibility repair over v1.6; "
    "NOT APPLIED)"
)
FAILED_COMMIT_ID = "analysis-durability-failed"
FAILED_COMMIT_RUN_ID = "$RUN_ID"
LIFECYCLE_INVARIANT = {
    "id": "invariant-runid-commit-visibility",
    "text": (
        "RunId is externally observable only for a committed Run. A failed final "
        "authoritative commit omits runId, retains executionId for attempt "
        "correlation, and cannot expose a pre-commit candidate identity."
    ),
}
REPRODUCE = (
    "python3 -B artifacts/check-d9-v1.7.py         # defaults to the binding "
    "v1.7 artifact"
)
MUTATION_PROOF = (
    "python3 -B artifacts/check-d9-v1.7.py --selftest  # asserts the checker "
    "REJECTS legacy and lifecycle mutations"
)


def _load_v16_checker():
    path = HERE / "check-d9.py"
    spec = importlib.util.spec_from_file_location("opensip_check_d9_v16", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load predecessor checker: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


V16 = _load_v16_checker()


def _as_v16(candidate: dict[str, Any]) -> dict[str, Any]:
    projected = copy.deepcopy(candidate)
    projected["version"] = "v1.6"
    return projected


def _golden(root: dict[str, Any], golden_id: str) -> dict[str, Any] | None:
    cases = root.get("goldenCases")
    if not isinstance(cases, list):
        return None
    matches = [g for g in cases if isinstance(g, dict) and g.get("id") == golden_id]
    return matches[0] if len(matches) == 1 else None


def _expected_successor(predecessor: dict[str, Any]) -> dict[str, Any]:
    expected = copy.deepcopy(predecessor)
    expected["version"] = EXPECTED_VERSION
    expected["status"] = EXPECTED_STATUS
    expected["supersedes"] = PREDECESSOR

    invariants = expected["invariants"]
    insert_at = next(
        i for i, row in enumerate(invariants)
        if row.get("id") == "invariant-durability"
    ) + 1
    invariants.insert(insert_at, copy.deepcopy(LIFECYCLE_INVARIANT))

    failed = _golden(expected, FAILED_COMMIT_ID)
    if failed is None:
        raise ValueError(f"predecessor lacks unique golden {FAILED_COMMIT_ID}")
    del failed["expectedTermination"]["runId"]

    claim = expected["conformanceClaims"][0]
    claim["reproduce"] = REPRODUCE
    claim["mutationProof"] = MUTATION_PROOF
    return expected


def _first_difference(actual: Any, expected: Any, path: str = "$") -> str | None:
    if type(actual) is not type(expected):
        return f"{path}: type {type(actual).__name__} != {type(expected).__name__}"
    if isinstance(actual, dict):
        actual_keys = list(actual)
        expected_keys = list(expected)
        if actual_keys != expected_keys:
            return f"{path}: ordered keys {actual_keys!r} != {expected_keys!r}"
        for key in expected_keys:
            diff = _first_difference(actual[key], expected[key], f"{path}.{key}")
            if diff:
                return diff
        return None
    if isinstance(actual, list):
        if len(actual) != len(expected):
            return f"{path}: length {len(actual)} != {len(expected)}"
        for index, (left, right) in enumerate(zip(actual, expected)):
            diff = _first_difference(left, right, f"{path}[{index}]")
            if diff:
                return diff
        return None
    if actual != expected:
        return f"{path}: {actual!r} != {expected!r}"
    return None


def check(candidate: object, predecessor: object) -> list[str]:
    findings: list[str] = []
    if not isinstance(candidate, dict) or not candidate:
        return ["D9-TOTALITY-ROOT: v1.7 contract root must be a non-empty object"]
    if not isinstance(predecessor, dict) or not predecessor:
        return ["D18-PREDECESSOR: v1.6 predecessor root must be a non-empty object"]

    legacy = V16.check(_as_v16(candidate))
    if legacy:
        return [f"D0..D16 successor projection: {finding}" for finding in legacy]

    if candidate.get("version") != EXPECTED_VERSION:
        findings.append(
            f"D17: contract version is {candidate.get('version')!r}; expected "
            f"{EXPECTED_VERSION!r}"
        )

    invariant_rows = candidate.get("invariants")
    lifecycle_rows = [] if not isinstance(invariant_rows, list) else [
        row for row in invariant_rows
        if isinstance(row, dict) and row.get("id") == LIFECYCLE_INVARIANT["id"]
    ]
    if lifecycle_rows != [LIFECYCLE_INVARIANT]:
        findings.append(
            "D17: exact invariant-runid-commit-visibility declaration is absent, "
            "duplicated, or mutated"
        )

    failed = _golden(candidate, FAILED_COMMIT_ID)
    if failed is None:
        findings.append(f"D17: {FAILED_COMMIT_ID} is absent or duplicated")
    else:
        termination = failed.get("expectedTermination")
        axes = failed.get("scenarioAxes")
        if not isinstance(termination, dict) or not isinstance(axes, dict):
            findings.append(f"D17 {FAILED_COMMIT_ID}: malformed axes or termination")
        else:
            if axes.get("durability") != "failed":
                findings.append(
                    f"D17 {FAILED_COMMIT_ID}: durability must remain 'failed'"
                )
            if "runId" in termination:
                findings.append(
                    f"D17 {FAILED_COMMIT_ID}: failed final commit exposes runId"
                )
            if termination.get("executionId") != "$EXEC_ID":
                findings.append(
                    f"D17 {FAILED_COMMIT_ID}: executionId attempt correlation was lost"
                )

    cases = candidate.get("goldenCases")
    if isinstance(cases, list):
        for row in cases:
            if not isinstance(row, dict):
                continue
            termination = row.get("expectedTermination")
            axes = row.get("scenarioAxes")
            if not isinstance(termination, dict) or "runId" not in termination:
                continue
            if not isinstance(axes, dict) or axes.get("durability") != "committed":
                findings.append(
                    f"D17 {row.get('id', '?')}: runId is present without a committed "
                    "Run lifecycle"
                )

    try:
        expected = _expected_successor(predecessor)
    except (KeyError, StopIteration, TypeError, ValueError) as exc:
        findings.append(f"D18-PREDECESSOR: cannot derive closed successor ({exc})")
    else:
        diff = _first_difference(candidate, expected)
        if diff:
            findings.append(
                "D18: successor differs outside the closed v1.7 delta; first "
                f"difference: {diff}"
            )

    return findings


def _mut_restore_failed_run_id(root):
    _golden(root, FAILED_COMMIT_ID)["expectedTermination"]["runId"] = FAILED_COMMIT_RUN_ID


def _mut_drop_failed_execution_id(root):
    del _golden(root, FAILED_COMMIT_ID)["expectedTermination"]["executionId"]


def _mut_expose_other_failed_run_id(root):
    _golden(root, "analysis-cas-link-failed")["expectedTermination"]["runId"] = "$RUN_ID"


def _mut_drop_lifecycle_invariant(root):
    root["invariants"] = [
        row for row in root["invariants"]
        if row.get("id") != LIFECYCLE_INVARIANT["id"]
    ]


def _mut_reword_lifecycle_invariant(root):
    for row in root["invariants"]:
        if row.get("id") == LIFECYCLE_INVARIANT["id"]:
            row["text"] = "RunId may be exposed before commit."


def _mut_drop_retained_committed_run_id(root):
    del _golden(root, "analysis-policy-fail")["expectedTermination"]["runId"]


def _mut_change_exit_class_code(root):
    root["classToExitCode"]["operational-failed"] = 5


def _mut_change_axis(root):
    root["scenarioAxesSchema"]["properties"]["durability"]["enum"].append("prepared")


MUTATIONS = [
    ("restore RunId on failed final commit", _mut_restore_failed_run_id),
    ("drop ExecutionId on failed final commit", _mut_drop_failed_execution_id),
    ("expose RunId on another failed publication", _mut_expose_other_failed_run_id),
    ("delete lifecycle invariant", _mut_drop_lifecycle_invariant),
    ("weaken lifecycle invariant", _mut_reword_lifecycle_invariant),
    ("delete one of the 12 retained committed RunIds", _mut_drop_retained_committed_run_id),
    ("change a preserved exit mapping", _mut_change_exit_class_code),
    ("change a preserved axis", _mut_change_axis),
]


def selftest(candidate: dict[str, Any], predecessor: dict[str, Any]) -> int:
    base_findings = check(candidate, predecessor)
    if base_findings:
        print(f"REFUSING to self-test: base has {len(base_findings)} finding(s)")
        for finding in base_findings[:5]:
            print("  -", finding)
        return 1

    print("retained v1.6 mutation proof")
    if V16.selftest(_as_v16(candidate)) != 0:
        return 1

    print("\nv1.7 lifecycle/differential mutation proof — every row must be REJECTED\n")
    escaped = 0
    for name, mutate in MUTATIONS:
        changed = copy.deepcopy(candidate)
        mutate(changed)
        findings = check(changed, predecessor)
        if not findings:
            escaped += 1
        print(f"  {'reject' if findings else 'ESCAPE':>6}  {name}")
        print(f"          {findings[0] if findings else 'NO FINDING — mutation survived'}")
    print()
    if escaped:
        print(f"{escaped}/{len(MUTATIONS)} v1.7 mutations ESCAPED")
        return 1
    print(f"all {len(MUTATIONS)} v1.7 lifecycle/differential mutations rejected")
    return 0


def main() -> int:
    args = [arg for arg in sys.argv[1:] if arg != "--selftest"]
    path = pathlib.Path(args[0]) if args else HERE / BINDING
    predecessor_path = HERE / PREDECESSOR
    try:
        candidate = json.loads(path.read_text())
        predecessor = json.loads(predecessor_path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(f"cannot load D9 contract inputs: {exc}", file=sys.stderr)
        return 2

    if "--selftest" in sys.argv:
        if not isinstance(candidate, dict) or not isinstance(predecessor, dict):
            print("selftest requires object roots", file=sys.stderr)
            return 1
        return selftest(candidate, predecessor)

    findings = check(candidate, predecessor)
    if not findings:
        count = len(candidate["goldenCases"])
        run_ids = sum(
            1 for row in candidate["goldenCases"]
            if "runId" in row["expectedTermination"]
        )
        print(
            f"D9 contract OK — {path.name}, {count} goldens, {run_ids} committed "
            "RunId rows, D0..D18 clean"
        )
        return 0
    print(f"{len(findings)} finding(s) in {path.name}:")
    for finding in findings:
        print("  -", finding)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
