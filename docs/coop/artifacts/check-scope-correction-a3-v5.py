#!/usr/bin/env python3
"""Exact-delta checker for scope-correction-a3.v5.json.

Usage: python3 -B check-scope-correction-a3-v5.py [contract] [--selftest]
"""
from __future__ import annotations

import copy
import hashlib
import json
import pathlib
import sys
from typing import Any

HERE = pathlib.Path(__file__).resolve().parent
BINDING = "scope-correction-a3.v5.json"
PREDECESSOR = "scope-correction-a3.v4.json"
PREDECESSOR_SHA = "a343581691314ff806e042825d0dadb540c913fc1862835aaa505604ea9c96cf"

RESOLUTION = (
    "SUPERSEDED IN v5. v4 conflated RunId with per-attempt ExecutionId. "
    "Identical semantic inputs and sealed capability require content-derived "
    "Run/evidence/terminal parity; EC-6 requires only ExecutionIds to differ."
)
EC3_FALSIFIER = (
    "under identical semantic inputs and identical admitted sealedCapability: "
    "any divergence between a resident and a cold host in SemanticEvidence, "
    "EvidenceDigest, evaluation outcomes, exact Coverage, content-derived RunId, "
    "TerminalRun, or runSealRef. ExecutionIds differ per attempt under EC-6. "
    "effectiveCapability and current availability are mutable read-time "
    "projections and are excluded."
)
EC3_ADJUDICATION = (
    "CORRECTED IN v5. v4 wrongly applied EC-6 to RunId. EC-6 requires only the "
    "per-attempt ExecutionId to differ; content-derived Run identity belongs to "
    "the sealed result and therefore matches for identical semantic inputs and "
    "admitted sealedCapability."
)
LIMITATION = (
    "EC-3 required a second correction in v5: v4 conflated content-derived RunId "
    "with per-attempt ExecutionId. Extraction and later adjudication did not "
    "carry the R-1 identity distinction forward."
)
OLD_LIMITATION = (
    "EC-3's defect was a correction already made at detailed-design level (r1 "
    "v1.3 LN-13) and lost during extraction. Extraction does not carry "
    "corrections forward."
)


def load(name: str) -> Any:
    return json.loads((HERE / name).read_text())


def ec(root: dict[str, Any], ident: str) -> dict[str, Any] | None:
    rows: list[dict[str, Any]] = []
    for value in root.values():
        if isinstance(value, dict):
            for child in value.values():
                if isinstance(child, list):
                    rows.extend(x for x in child if isinstance(x, dict)
                                and x.get("id") == ident)
        elif isinstance(value, list):
            rows.extend(x for x in value if isinstance(x, dict) and x.get("id") == ident)
    return rows[0] if len(rows) == 1 else None


def expected_successor(predecessor: dict[str, Any]) -> dict[str, Any]:
    expected = copy.deepcopy(predecessor)
    expected["version"] = 5
    expected["supersedes"] = 4
    expected["status"] = "CANDIDATE-UNREVIEWED / NOT-APPLIED"
    expected["resolves"]["B-TOEC-03"] = RESOLUTION
    row = ec(expected, "EC-3")
    if row is None:
        raise ValueError("predecessor lacks unique EC-3")
    row["falsifiedBy"] = EC3_FALSIFIER
    row["adjudication"] = EC3_ADJUDICATION
    limitations = expected["knownLimitations"]
    index = limitations.index(OLD_LIMITATION)
    limitations[index] = LIMITATION
    return expected


def check(candidate: Any, predecessor: Any, *, verify_hash: bool = True) -> list[str]:
    errors: list[str] = []
    if not isinstance(candidate, dict) or not isinstance(predecessor, dict):
        return ["candidate and predecessor roots must be objects"]
    if verify_hash:
        actual = hashlib.sha256((HERE / PREDECESSOR).read_bytes()).hexdigest()
        if actual != PREDECESSOR_SHA:
            errors.append(f"protected v4 drift: {actual} != {PREDECESSOR_SHA}")
    try:
        expected = expected_successor(predecessor)
    except (KeyError, ValueError) as exc:
        return errors + [f"cannot derive exact successor: {exc}"]
    if candidate != expected:
        errors.append("v5 differs outside the closed metadata/EC-3/limitation delta")
    if candidate.get("artifact") != "opensip.scope-correction" or \
            candidate.get("version") != 5 or candidate.get("supersedes") != 4 or \
            candidate.get("status") != "CANDIDATE-UNREVIEWED / NOT-APPLIED":
        errors.append("candidate envelope drifted")
    ec3 = ec(candidate, "EC-3") or {}
    ec6 = ec(candidate, "EC-6")
    old_ec6 = ec(predecessor, "EC-6")
    if ec3.get("falsifiedBy") != EC3_FALSIFIER or \
            ec3.get("adjudication") != EC3_ADJUDICATION:
        errors.append("EC-3 RunId/ExecutionId correction drifted")
    if ec6 is None or ec6 != old_ec6:
        errors.append("EC-6 was not preserved exact")
    if "effectiveCapability and current availability" not in ec3.get("falsifiedBy", ""):
        errors.append("EC-3 does not exclude mutable availability projection")
    return errors


def selftest(candidate: dict[str, Any], predecessor: dict[str, Any]) -> list[str]:
    mutations: list[tuple[str, Any]] = [
        ("version", lambda x: x.__setitem__("version", 4)),
        ("status", lambda x: x.__setitem__("status", "APPLIED")),
        ("resolution", lambda x: x["resolves"].__setitem__("B-TOEC-03", "UPHELD")),
        ("ec3-run", lambda x: ec(x, "EC-3").__setitem__("falsifiedBy", "RunId differs")),
        ("ec3-exec", lambda x: ec(x, "EC-3").__setitem__("adjudication", "ExecutionId matches")),
        ("ec6", lambda x: ec(x, "EC-6").__setitem__("invariant", "RunId differs")),
        ("availability", lambda x: ec(x, "EC-3").__setitem__("falsifiedBy", EC3_FALSIFIER.replace(" and current availability", ""))),
        ("limitation", lambda x: x["knownLimitations"].remove(LIMITATION)),
        ("unrelated", lambda x: x.__setitem__("purpose", "changed")),
    ]
    failures: list[str] = []
    for name, fn in mutations:
        changed = copy.deepcopy(candidate)
        fn(changed)
        if not check(changed, predecessor, verify_hash=False):
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
        candidate = json.loads(path.read_text())
        predecessor = load(PREDECESSOR)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 2
    errors = check(candidate, predecessor)
    if not errors and do_selftest:
        errors.extend(selftest(candidate, predecessor))
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print(f"PASS: {path.name} exact EC-3 successor; EC-6 preserved")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
