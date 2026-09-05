#!/usr/bin/env python3
"""OPERABILITY v4 exact OP2 projection and Evidence-v5/D9 rebind checker."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import pathlib
import sys
from typing import Any


HERE = pathlib.Path(__file__).resolve().parent
BINDING = "operability.v4.json"
PINS = {
    "operability.v3.json": "63f6bd846167d3ea011dcc3d34476cda1540ddf95fd87dfe08ada9825937ca81",
    "check-operability-v3.py": "532e7cba2208d5b9969b348403d433fd638b3d6c5907e7fe847c6dac9905b49c",
    "operability.v2.json": "43e63e4bca8e238e933a6b3e0c91112fb29b52da5f92d64ff2438d79140e6f04",
    "check-operability.py": "925496916ef2c7075c02f7a767353aa6ff047cf55557304f3983e17e1c5256e2",
    "d9-exit-contract.v1.7.json": "d199aef6ac2edc7652325ef8d26f75cfda35a94f3e234d10aafd984d9088b2eb",
    "check-d9-v1.7.py": "ead1dd8d3635a355475ba8d71611515497a29e59cdfc5d232f167588dd9fb6d3",
}
ENVELOPE = ["version", "status", "supersedes", "author", "reviewStatus"]


def load(name_or_path: str | pathlib.Path) -> Any:
    path = pathlib.Path(name_or_path)
    if not path.is_absolute() and path.parent == pathlib.Path("."):
        path = HERE / path
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


def gate(value: dict[str, Any], gate_id: str) -> dict[str, Any] | None:
    return next((row for row in value.get("validationGates", [])
                 if isinstance(row, dict) and row.get("id") == gate_id), None)


def project_op2(value: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(value)
    successor = result.pop("aPrimeSuccessor")
    changed = successor["compatibilityProjection"]["changedRootFields"]
    if set(changed) != set(ENVELOPE):
        raise ValueError("projection changedRootFields is not exact five-field envelope")
    for key in ENVELOPE:
        result[key] = changed[key]["before"]
    return result


def _strings(value: Any):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for child in value.values():
            yield from _strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from _strings(child)


def check(value: Any, *, verify_files: bool = True) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["root is not an object"]
    try:
        op3 = load("operability.v3.json")
        op2 = load("operability.v2.json")
        evidence = load("evidence.v5.json")
        retention = load("retention-tiers.v11.json")
        d9 = load("d9-exit-contract.v1.7.json")
        op3mod = module("check-operability-v3.py", "op3_pinned_for_op4")
        evmod = module("check-evidence-v5.py", "evidence_v5_for_op4")
        rtmod = module("check-retention-custody-v11.py", "rt11_for_op4")
    except Exception as exc:
        return [f"dependency import failed: {type(exc).__name__}: {exc}"]
    for name, expected in PINS.items():
        if sha_file(name) != expected:
            errors.append(f"protected predecessor/D9 drift: {name}")
    if verify_files:
        prior = op3mod.check(op3)
        if prior:
            errors.append(f"OPERABILITY v3 predecessor red: {prior[0]}")
        for label, checker, artifact in (
                ("Evidence v5", evmod, evidence), ("RT11", rtmod, retention)):
            child = checker.check(artifact)
            if child:
                errors.append(f"{label} dependency red: {child[0]}")
    if (value.get("artifact"), value.get("version")) != ("opensip.operability", 4):
        errors.append("artifact/version mismatch")
    if "NOT APPLIED" not in value.get("status", "") or \
            value.get("supersedes") != {
                "artifact": "operability.v3.json", "sha256": PINS["operability.v3.json"],
                "checker": "check-operability-v3.py",
                "checkerSha256": PINS["check-operability-v3.py"]}:
        errors.append("OP4 candidate/supersession envelope drift")
    successor = value.get("aPrimeSuccessor") or {}
    if successor.get("id") != "OPERABILITY-V4-A-PRIME-SUCCESSOR" or \
            successor.get("applicationState") != "NOT-APPLIED" or \
            successor.get("authorityClaim") != "NONE" or \
            successor.get("productAcceptance") is not False or \
            successor.get("independentCombinedRereview") != "REQUIRED":
        errors.append("OP4 candidate/non-authority boundary drift")

    compat = successor.get("compatibilityProjection") or {}
    if compat.get("id") != "OP4-TO-OP2-EXACT-PROJECTION" or \
            compat.get("predecessor") != {
                "artifact": "operability.v2.json", "sha256": PINS["operability.v2.json"],
                "checker": "check-operability.py", "checkerSha256": PINS["check-operability.py"]}:
        errors.append("OP2 compatibility predecessor pin/id drift")
    expected_changed = {
        key: {"before": op2[key], "after": value[key]} for key in ENVELOPE}
    if compat.get("changedRootFields") != expected_changed:
        errors.append("closed five-field OP4->OP2 delta drift")
    expected_unchanged = [key for key in op2 if key not in ENVELOPE]
    if compat.get("unchangedTopLevelKeys") != expected_unchanged:
        errors.append("OP2 unchanged subtree denominator drift")
    try:
        if project_op2(value) != op2:
            errors.append("OP4 does not mechanically project exact-deep-equal to OP2")
    except Exception as exc:
        errors.append(f"OP2 projection failed: {exc}")
    for key in expected_unchanged:
        if value.get(key) != op2.get(key):
            errors.append(f"OP2 root subtree changed outside overlay: {key}")
    if value.get("projectionParity") != op2.get("projectionParity") or \
            value.get("projectionFixtures") != op2.get("projectionFixtures"):
        errors.append("OP2 projectionParity/projectionFixtures are not exact")
    if gate(value, "G19") != gate(op2, "G19") or \
            (gate(value, "G19") or {}).get("status") != "BLOCKED-NO-MECHANISM":
        errors.append("live OP2 G19 changed or was promoted")

    deps = successor.get("dependencies") or {}
    expected_deps = {
        "evidence": ("evidence.v5.json", "check-evidence-v5.py", "E5"),
        "retentionCustody": ("retention-tiers.v11.json", "check-retention-custody-v11.py", "RT11"),
        "d9": ("d9-exit-contract.v1.7.json", "check-d9-v1.7.py", "D9"),
    }
    for key, (artifact, checker, token) in expected_deps.items():
        row = deps.get(key) or {}
        if row.get("artifact") != artifact or row.get("checker") != checker:
            errors.append(f"OP4 dependency name drift: {key}")
            continue
        if key == "d9":
            if row.get("sha256") != PINS[artifact] or row.get("checkerSha256") != PINS[checker] or \
                    row.get("compatibilityInvariant") != "D18":
                errors.append("unchanged D9 v1.7 pin/invariant drift")
        elif row.get("sha256") != sha_file(artifact) or \
                row.get("checkerSha256") != sha_file(checker):
            errors.append(f"OP4 dependency hash drift: {key}")

    golden = next((row for row in d9["goldenCases"]
                   if row.get("id") == "analysis-durability-failed"), None)
    failed = (((successor.get("lifecycle") or {}).get("identityVisibility") or {})
              .get("failedFinalCommit") or {})
    if not golden or failed.get("d9Golden") != \
            "d9-exit-contract.v1.7.json#analysis-durability-failed" or \
            failed.get("termination") != golden.get("expectedTermination") or \
            failed.get("termination") != {
                "class": "operational-failed", "errorCode": "DURABILITY.COMMIT_FAILED",
                "executionId": "$EXEC_ID"}:
        errors.append("failed-commit projection is not exact D9 v1.7 golden")
    if not {"runId", "runSealRef", "terminalRunCasRef", "runAuthorityIndex"}.issubset(
            set(failed.get("forbidden") or [])):
        errors.append("failed commit permits Run/Terminal/authority-index publication")
    successor_repair = successor.get("successorRepair") or {}
    if successor_repair.get("exactFailedCommitProjection") != golden.get("expectedTermination") or \
            successor_repair.get("candidateState") != "NOT-APPLIED" or \
            set(successor_repair.get("nonClaims") or []) != {
                "no runtime execution", "no product qualification", "no integration",
                "no independent acceptance", "no seal"}:
        errors.append("OP4 repair/non-claim record drift")
    all_text = json.dumps(value)
    if "$EXECUTION_ID" in all_text or all_text.count("$EXEC_ID") < 2:
        errors.append("OP4 does not use exact D9 symbolic $EXEC_ID")

    accepted = evidence["acceptedGolden"]
    run_ids = {text for text in _strings(successor) if text.startswith("run1:")}
    if run_ids != {accepted["runId"]}:
        errors.append(f"OP4 lifecycle examples do not use regenerated Evidence v5 RunId: {run_ids}")
    recursive = successor.get("recursiveRequestIdExclusion") or {}
    source = recursive.get("evidenceSource") or {}
    if source.get("artifact") != "evidence.v5.json#recursiveRequestIdExclusion" or \
            source.get("artifactSha256") != sha_file("evidence.v5.json") or \
            source.get("checker") != "check-evidence-v5.py" or \
            source.get("checkerSha256") != sha_file("check-evidence-v5.py"):
        errors.append("OP4 recursive Evidence source pin drift")
    if recursive.get("surfaces") != evidence["recursiveRequestIdExclusion"]["surfaces"] or \
            recursive.get("variationFixture") != evidence.get("correlationDifferential") or \
            recursive.get("availabilityFixture") != evidence.get("availabilityDifferential"):
        errors.append("OP4 does not exactly project Evidence v5 correlation/availability closure")
    g19 = successor.get("g19CandidateMechanism") or {}
    if g19.get("liveGateStatus") != "BLOCKED-NO-MECHANISM" or \
            g19.get("productState") != "BLOCKED" or \
            g19.get("productDecision") != "CD-RT-5 UNRESOLVED" or \
            "IMPLEMENTABLE_UNEXECUTED" not in g19.get("evidenceGrade", ""):
        errors.append("G19/CD-RT-5 candidate state was promoted or lost")
    residuals = {row.get("id"): row.get("state") for row in successor.get("retainedResiduals", [])
                 if isinstance(row, dict)}
    if residuals != {"V10": "UNRESOLVED", "CD-RT-5": "BLOCKED", "G19": "BLOCKED",
                     "INDEPENDENT-COMBINED-REREVIEW": "REQUIRED"}:
        errors.append("OP4 V10/CD-RT-5/G19/review residual matrix drift")
    return errors


def selftest(value: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    cases = []
    def add(label, mutate):
        candidate = copy.deepcopy(value); mutate(candidate); cases.append((label, candidate))
    add("D9 execution placeholder", lambda c: c["aPrimeSuccessor"]["lifecycle"]["identityVisibility"]["failedFinalCommit"]["termination"].__setitem__("executionId", "$EXECUTION_ID"))
    add("D9 error code", lambda c: c["aPrimeSuccessor"]["lifecycle"]["identityVisibility"]["failedFinalCommit"]["termination"].__setitem__("errorCode", "STORE.COMMIT_FAILED"))
    add("OP2 projection subtree", lambda c: c["projectionFixtures"].pop())
    add("OP2 changed denominator", lambda c: c["aPrimeSuccessor"]["compatibilityProjection"]["changedRootFields"].pop("author"))
    add("G19 promotion", lambda c: next(row for row in c["validationGates"] if row["id"] == "G19").__setitem__("status", "IMPLEMENTABLE"))
    add("Evidence RunId", lambda c: c["aPrimeSuccessor"]["lifecycle"]["fixtures"][2].__setitem__("runId", "run1:" + "0" * 64))
    add("failed commit index publication", lambda c: c["aPrimeSuccessor"]["lifecycle"]["identityVisibility"]["failedFinalCommit"]["forbidden"].remove("runAuthorityIndex"))
    add("product qualification", lambda c: c["aPrimeSuccessor"]["successorRepair"]["nonClaims"].remove("no product qualification"))
    for label, candidate in cases:
        if not check(candidate, verify_files=False):
            failures.append(f"{label} escaped")
    return failures


def main(argv: list[str]) -> int:
    positional = [arg for arg in argv[1:] if arg != "--selftest"]
    path = pathlib.Path(positional[0]) if positional else HERE / BINDING
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
        print("PASS: operability.v4.json; 8 successor mutations rejected")
    else:
        print("PASS: operability.v4.json; exact OP2 projection; D9 $EXEC_ID; Evidence v5 terminal authority")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
