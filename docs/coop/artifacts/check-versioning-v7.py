#!/usr/bin/env python3
"""Conformance checker for VERSIONING v7 EP7/RT12 custody rejoin."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import pathlib
import sys
from typing import Any


HERE = pathlib.Path(__file__).resolve().parent
DEFAULT = HERE / "versioning-policy.v7.json"
PREDECESSOR = "versioning-policy.v6.json"
PREDECESSOR_CHECKER = "check-versioning-v6.py"
EP = "evaluation-proof.v7.json"
EP_CHECKER = "check-evaluation-proof-v7.py"
RT = "retention-tiers.v12.json"
RT_CHECKER = "check-retention-custody-v12.py"
PINS = {
    PREDECESSOR: "97ab3ece4a51d466feae8277c348b856ee5cd502153d1aab540e2f8948d0aa57",
    PREDECESSOR_CHECKER: "f93145f2b50703382e7bdf0c2deda029097eab0409a45d5e5b5a5dd91e6cb6f8",
    EP: "92d51e9232c6ee137b7228aa7885a2e32f668f9b4b108d7140fdb52dae864ef8",
    EP_CHECKER: "550a2231264ab6b308b3ddb752199c6496f7c2417a8dbeeb9f21c230569b36c4",
    RT: "1a034746512de51605b7a4bcc4fb0936bdc167db057a3018be74a2a047376dab",
    RT_CHECKER: "104a8f9bd01e92226c11c41c234358b5a9d991b42cf12ec9318582ed12b57851",
}
RAW_KINDS = [
    "resolved-inputs", "plan-id-verification-receipt",
    "authority-seal-verification-receipt", "activation-manifest-record",
    "evaluation-authority-seal-record", "file-bytes", "symlink-target-bytes",
]
CHANGED = {"version", "knownLimitations", "supersedes", "role", "successorRevision"}


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
        oldmod = module(PREDECESSOR_CHECKER, "versioning_v6_pinned_for_v7")
        epmod = module(EP_CHECKER, "ep7_pinned_for_versioning_v7")
        rtmod = module(RT_CHECKER, "rt12_pinned_for_versioning_v7")
    except Exception as exc:
        return [f"predecessor/dependency import failed: {type(exc).__name__}: {exc}"]
    if verify_files:
        old_errors = oldmod.check(predecessor)
        if old_errors:
            errors.append(f"VERSIONING v6 predecessor is red: {old_errors[0]}")
        ep_errors = epmod.check(load(HERE / EP))
        if ep_errors:
            errors.append(f"EP7 dependency is red: {ep_errors[0]}")
        rt_errors = rtmod.check(load(HERE / RT))
        if rt_errors:
            errors.append(f"RT12 dependency is red: {rt_errors[0]}")
    if set(value) != set(predecessor):
        errors.append("top-level surface differs from VERSIONING v6")
    for key in set(predecessor) - CHANGED:
        if value.get(key) != predecessor.get(key):
            errors.append(f"protected VERSIONING v6 section changed: {key}")
    if (value.get("artifact"), value.get("version")) != ("opensip.versioning-policy", 7):
        errors.append("artifact/version mismatch")
    if value.get("status") != "CANDIDATE-NOT-APPLIED" or \
            value.get("reviewStatus") != "AWAITING-INDEPENDENT-COMBINED-REREVIEW" or \
            value.get("supersedes") != 6:
        errors.append("candidate/supersession state drift")
    revision = value.get("successorRevision") or {}
    if revision.get("id") != "VERSIONING-v7-STORE-PROVENANCE-SUCCESSOR" or \
            revision.get("candidateState") != "NOT-APPLIED" or \
            revision.get("rawAuthorityKinds") != RAW_KINDS or \
            revision.get("rawAuthorityKinds") != \
            predecessor["successorRevision"]["rawAuthorityKinds"] or \
            revision.get("custodyRule") != predecessor["successorRevision"]["custodyRule"]:
        errors.append("exact v6 raw authority/custody contract drift")
    if revision.get("supersedesCandidate") != {
            "artifact": PREDECESSOR, "sha256": PINS[PREDECESSOR],
            "checker": PREDECESSOR_CHECKER,
            "checkerSha256": PINS[PREDECESSOR_CHECKER]}:
        errors.append("VERSIONING v6 protected predecessor pin drift")
    inputs = revision.get("inputs") or {}
    expected_inputs = {
        "evaluationProof": {
            "artifact": EP, "sha256": PINS[EP], "checker": EP_CHECKER,
            "checkerSha256": PINS[EP_CHECKER]},
        "retentionCustody": {
            "artifact": RT, "sha256": PINS[RT], "checker": RT_CHECKER,
            "checkerSha256": PINS[RT_CHECKER]},
    }
    if inputs != expected_inputs:
        errors.append("EP7/RT12 dependency pins drift")
    if "RawCasRef" not in revision.get("custodyRule", "") or \
            "Semantic commitments cannot be physical keys" not in revision.get("custodyRule", ""):
        errors.append("semantic/raw versioning custody rule drift")
    if not all(term in revision.get("storeAuthorityRule", "") for term in (
            "operational-only", "nonserializable", "excluded")):
        errors.append("store authority identity-exclusion rule incomplete")
    identity = revision.get("identityStability") or {}
    if identity != {
            "predecessor": "VERSIONING-v6",
            "state": "EXACT-CUSTODY-IDENTITIES-UNCHANGED",
            "reason": "Only authority provenance/port continuity changed."}:
        errors.append("v6 identity stability statement drift")
    forbidden = revision.get("forbiddenBackEdge", "")
    if not all(term in forbidden for term in (
            "Evidence", "RunId", "TerminalRunV1", "RunAuthorityIndexV1",
            "ProjectStoreAuthority token", "store transaction token")):
        errors.append("forbidden downstream/store-token back-edge rule incomplete")
    if any("evidence" in json.dumps(row).lower()
           for row in inputs.values() if isinstance(row, dict)):
        errors.append("VERSIONING v7 contains an Evidence dependency back-edge")
    protected_identity = json.dumps({
        "custodyClasses": value.get("custodyClasses"),
        "versionedIdentities": value.get("versionedIdentities"),
        "rules": value.get("rules"),
        "rawAuthorityKinds": revision.get("rawAuthorityKinds"),
        "custodyRule": revision.get("custodyRule"),
    })
    if any(term in protected_identity for term in (
            "storeInstanceToken", "transactionToken", "ProjectStoreAuthorityV1")):
        errors.append("operational store token/type leaked into versioned identity")
    expected_discharge = {
        "state": "SPECIFIED", "evidenceGrade": "IMPLEMENTABLE_UNEXECUTED",
        "candidateState": "NOT-APPLIED", "qualificationEvidenceIds": [],
        "releaseEvidenceIds": [], "V10": "UNRESOLVED", "CD-RT-5": "BLOCKED",
        "G19": "BLOCKED", "seal": "DO-NOT-SEAL",
    }
    if value.get("dischargeStatus") != expected_discharge:
        errors.append("VERSIONING v7 discharge/non-authority state drift")
    limitations = json.dumps(value.get("knownLimitations") or [])
    if not all(term in limitations for term in (
            "not-applied", "not executed", "independently accepted",
            "No production store/transaction", "atomicity")):
        errors.append("successor limitations omit not-applied/unexecuted/unaccepted state")
    return errors


def selftest(value: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    cases = []

    def add(label: str, mutate: Any) -> None:
        candidate = copy.deepcopy(value)
        mutate(candidate)
        cases.append((label, candidate))

    add("raw kind omission", lambda c: c["successorRevision"]["rawAuthorityKinds"].pop())
    add("semantic physical key", lambda c: c["successorRevision"].__setitem__(
        "custodyRule", "SemanticCommitmentRef is physical"))
    add("Evidence back-edge", lambda c: c["successorRevision"]["inputs"].__setitem__(
        "evidence", {"artifact": "evidence.v6.json"}))
    add("store token identity", lambda c: c["versionedIdentities"].append(
        {"kind": "ProjectStoreAuthorityV1", "identity": "storeInstanceToken"}))
    add("EP7 pin", lambda c: c["successorRevision"]["inputs"]["evaluationProof"].__setitem__(
        "sha256", "0" * 64))
    add("RT12 pin", lambda c: c["successorRevision"]["inputs"]["retentionCustody"].__setitem__(
        "checkerSha256", "0" * 64))
    add("discharge inflation", lambda c: c["dischargeStatus"].__setitem__("state", "DISCHARGED"))
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
        print("PASS: versioning-policy.v7.json; 8 successor mutations rejected")
    else:
        print("PASS: versioning-policy.v7.json; EP7/RT12 exact raw custody rejoined; "
              "store tokens operational-only; no Evidence back-edge")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
