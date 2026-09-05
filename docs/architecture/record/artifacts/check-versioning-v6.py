#!/usr/bin/env python3
"""Conformance checker for the VERSIONING v6 EP6/RT11 raw-custody rejoin."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import pathlib
import sys
from typing import Any


HERE = pathlib.Path(__file__).resolve().parent
DEFAULT = HERE / "versioning-policy.v6.json"
PREDECESSOR = "versioning-policy.v5.json"
PREDECESSOR_CHECKER = "check-versioning-v5.py"
PINS = {
    PREDECESSOR: "880bdae45e60da8ea06cbfa18aaf25e6dd902874fbe471b68cface4a5e617d66",
    PREDECESSOR_CHECKER: "cacde3a32ca71f22b806fee281946758dc14748e6bd80f42e2c1f034dd12b536",
    "retention-tiers.v10.rereview-independent-final.json": "9a10cd8a3f02e0d46b9c9e5e8aed7e607f05b946f8d59c0b029bf6758d978f02",
}
CHANGED = {
    "version", "status", "reviewStatus", "decisionDependencies", "supersedes",
    "dischargeStatus", "knownLimitations", "role", "successorRevision",
}
RAW_KINDS = [
    "resolved-inputs", "plan-id-verification-receipt",
    "authority-seal-verification-receipt", "activation-manifest-record",
    "evaluation-authority-seal-record", "file-bytes", "symlink-target-bytes",
]


def load(path: pathlib.Path) -> Any:
    return json.loads(path.read_text())


def sha_file(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


def module(filename: str, name: str):
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
        predecessor = load(HERE / PREDECESSOR)
        oldmod = module(PREDECESSOR_CHECKER, "versioning_v5_pinned_for_v6")
    except Exception as exc:
        return [f"predecessor import failed: {type(exc).__name__}: {exc}"]
    for name, expected in PINS.items():
        if sha_file(name) != expected:
            errors.append(f"pinned predecessor/review drift: {name}")
    if verify_files:
        old_errors = oldmod.check(predecessor)
        if old_errors:
            errors.append(f"VERSIONING v5 predecessor is red: {old_errors[0]}")
    if set(value) != set(predecessor):
        errors.append("top-level surface differs from predecessor")
    for key in set(predecessor) - CHANGED:
        if value.get(key) != predecessor.get(key):
            errors.append(f"protected VERSIONING v5 section changed: {key}")
    if (value.get("artifact"), value.get("version")) != ("opensip.versioning-policy", 6):
        errors.append("artifact/version mismatch")
    if value.get("status") != "CANDIDATE-NOT-APPLIED" or \
            value.get("reviewStatus") != "AWAITING-INDEPENDENT-COMBINED-REREVIEW" or \
            value.get("supersedes") != 5:
        errors.append("candidate/supersession state drift")
    revision = value.get("successorRevision") or {}
    if revision.get("candidateState") != "NOT-APPLIED" or \
            revision.get("rawAuthorityKinds") != RAW_KINDS:
        errors.append("successor raw authority kind registry drift")
    predecessor_pin = revision.get("supersedesCandidate") or {}
    if predecessor_pin != {
            "artifact": PREDECESSOR, "sha256": PINS[PREDECESSOR],
            "checker": PREDECESSOR_CHECKER,
            "checkerSha256": PINS[PREDECESSOR_CHECKER]}:
        errors.append("VERSIONING v5 predecessor pin drift")
    inputs = revision.get("inputs") or {}
    expected_names = {
        "evaluationProof": ("evaluation-proof.v6.json", "check-evaluation-proof-v6.py"),
        "retentionCustody": ("retention-tiers.v11.json", "check-retention-custody-v11.py"),
    }
    for key, (artifact, checker) in expected_names.items():
        row = inputs.get(key) or {}
        if row.get("artifact") != artifact or row.get("checker") != checker or \
                row.get("sha256") != sha_file(artifact) or \
                row.get("checkerSha256") != sha_file(checker):
            errors.append(f"successor dependency pin drift: {key}")
    if "RawCasRef" not in revision.get("custodyRule", "") or \
            "Semantic commitments cannot be physical keys" not in revision.get("custodyRule", ""):
        errors.append("semantic/raw versioning custody rule drift")
    forbidden = revision.get("forbiddenBackEdge", "")
    if not all(term in forbidden for term in (
            "Evidence", "RunId", "TerminalRunV1", "RunAuthorityIndexV1")):
        errors.append("forbidden Evidence/content back-edge rule incomplete")
    # No actual dependency object may point downstream into Evidence.
    if any("evidence" in json.dumps(row).lower()
           for row in inputs.values() if isinstance(row, dict)):
        errors.append("VERSIONING v6 contains an Evidence dependency back-edge")
    transfer = revision.get("reviewTransfer") or {}
    if transfer.get("sha256") != PINS["retention-tiers.v10.rereview-independent-final.json"] or \
            transfer.get("verdict") != "REQUIRED-CHANGES/DO-NOT-SEAL" or \
            transfer.get("passedPredecessorMechanismsOnly") != [
                "RR13-03", "Versioning custody rejoin"]:
        errors.append("predecessor final review transfer is overstated")
    discharge = value.get("dischargeStatus") or {}
    expected_discharge = {
        "state": "SPECIFIED", "evidenceGrade": "IMPLEMENTABLE_UNEXECUTED",
        "candidateState": "NOT-APPLIED", "qualificationEvidenceIds": [],
        "releaseEvidenceIds": [], "V10": "UNRESOLVED", "CD-RT-5": "BLOCKED",
        "G19": "BLOCKED", "seal": "DO-NOT-SEAL",
    }
    if discharge != expected_discharge:
        errors.append("VERSIONING v6 discharge/non-authority state drift")
    limitations = json.dumps(value.get("knownLimitations") or [])
    if not all(term in limitations for term in ("not-applied", "not executed", "independently accepted")):
        errors.append("successor limitations omit not-applied/unexecuted/unaccepted state")
    return errors


def selftest(value: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    cases = []
    def add(label, mutate):
        candidate = copy.deepcopy(value); mutate(candidate); cases.append((label, candidate))
    add("raw kind omission", lambda c: c["successorRevision"]["rawAuthorityKinds"].pop())
    add("semantic physical key", lambda c: c["successorRevision"].__setitem__("custodyRule", "SemanticCommitmentRef is physical"))
    add("Evidence back-edge", lambda c: c["successorRevision"]["inputs"].__setitem__(
        "evidence", {"artifact": "evidence.v5.json"}))
    add("review pass inflation", lambda c: c["successorRevision"]["reviewTransfer"].__setitem__("verdict", "PASS"))
    add("discharge inflation", lambda c: c["dischargeStatus"].__setitem__("state", "DISCHARGED"))
    add("seal inflation", lambda c: c["dischargeStatus"].__setitem__("seal", "SEAL"))
    add("protected role mutation", lambda c: c["custodyClasses"].pop())
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
        print("PASS: versioning-policy.v6.json; 7 successor mutations rejected")
    else:
        print("PASS: versioning-policy.v6.json; EP6/RT11 raw custody rejoined; no Evidence back-edge")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
