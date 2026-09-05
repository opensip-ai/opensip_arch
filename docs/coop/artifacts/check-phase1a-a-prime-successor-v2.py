#!/usr/bin/env python3
"""Umbrella integrity checker for the Phase-1A A-prime successor response v2."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import pathlib
import sys
from typing import Any


HERE = pathlib.Path(__file__).resolve().parent
BINDING = "phase1a-a-prime-successor.response.v2.json"
TOP = {
    "artifact", "version", "date", "status", "author", "authority",
    "selectedRepairMethod", "reviewLineage", "protectedInputHashWindow",
    "successorPacket", "mechanicalClosure", "evidenceTransfer",
    "retainedResiduals", "verificationContract", "recommendation",
}
PROTECTED = {
    "evaluation-proof.v5.json": "e05f6d8d9dd5f1f98dc1972a178c7fe58981c71b06a69feb00a717e03475988b",
    "check-evaluation-proof.py": "1ccc12c347f0c7598604227179a2ba0cc461466657908b5c5f9645db4f7b99e2",
    "retention-tiers.v10.json": "606b5e7125d4a3a46f44f1a7565f9c9ea69132d9ab2783d00339e1b8aac5e026",
    "check-retention-custody.py": "15816cd8f9d22221b1187b94a160d71f644f9ab8fccb82423931fe18f6fc38d7",
    "versioning-policy.v5.json": "880bdae45e60da8ea06cbfa18aaf25e6dd902874fbe471b68cface4a5e617d66",
    "check-versioning-v5.py": "cacde3a32ca71f22b806fee281946758dc14748e6bd80f42e2c1f034dd12b536",
    "evidence.v4.json": "4a5d2dc8d9067af103b6f8c898c83f08fdd59ee22ce49fb4cf12a1329c416c70",
    "check-evidence-v4.py": "fd8db2ab77261ba31351d0647cf62ba4de92db35ba7a15426cb8f4bcf28865bc",
    "operability.v3.json": "63f6bd846167d3ea011dcc3d34476cda1540ddf95fd87dfe08ada9825937ca81",
    "check-operability-v3.py": "532e7cba2208d5b9969b348403d433fd638b3d6c5907e7fe847c6dac9905b49c",
    "d9-exit-contract.v1.7.json": "d199aef6ac2edc7652325ef8d26f75cfda35a94f3e234d10aafd984d9088b2eb",
    "check-d9-v1.7.py": "ead1dd8d3635a355475ba8d71611515497a29e59cdfc5d232f167588dd9fb6d3",
    "scope-correction-a3.v5.json": "6ca4bd407b80d80aba9035dfb4d66d28d8704ccf30a729854810396c6f66c7af",
    "check-scope-correction-a3-v5.py": "5d777c42dfa6fb3826916b157f53955d66d07e93ce08acbdb1c27a027b753c0c",
    "c2-plan-stage-schema.v3.json": "3c488ff66a1ec9ab746e99e0701d59460aff3e1d66cd072d9d564a1382b9d285",
    "check-c2.py": "4f31d57cd1cd252d47eeb520aa31b5fe8c4fd3b0f0f067a6840b008b1fe176f3",
    "resolved-inputs.v2.json": "0114205aaa5d3f7c0aecc58c10522711aacaa6aa404a41563245627b27b88f43",
    "check-resolved-inputs.py": "7ffed1c0e66e345a72c5e0e7feaf332508d0842c1ecdba8572f872997917ffa0",
    "fact-plane.v1.json": "9057200822c5be59bcf8e691e3755cfa1acf2c89f0b1c2bc89237afaa0925b4d",
    "product-dispositions.v1.json": "b9a87839606981a5be46f62aca2d85a17c3da5082c8d0aad02a211f3025fd91c",
    "check-product-dispositions.py": "f73cb878ade9376f6f8a9c19a459742c1721932ad16625e6b63cd0d1645d732e",
    "threat-model.v3.json": "56734a4047b61e1fc702f75ccb21e8721b334adb449093d266756d0b08adc499",
    "claim-register.v1.json": "2338f7e08d24dead2540f04f9f2a071af42870b34c851393ed863f9d89ab1b42",
    "operability.v2.json": "43e63e4bca8e238e933a6b3e0c91112fb29b52da5f92d64ff2438d79140e6f04",
    "check-operability.py": "925496916ef2c7075c02f7a767353aa6ff047cf55557304f3983e17e1c5256e2",
    "phase1a-a-prime-successor.review-independent-evidence-op.json": "0410274d99b201f8dbb629120050f1af70649bd856ab077fdbe9dd569fe7cda6",
    "retention-tiers.v10.rereview-independent-final.json": "9a10cd8a3f02e0d46b9c9e5e8aed7e607f05b946f8d59c0b029bf6758d978f02",
}
OUTPUT_NAMES = [
    ("EP6", "evaluation-proof.v6.json", "check-evaluation-proof-v6.py"),
    ("RT11", "retention-tiers.v11.json", "check-retention-custody-v11.py"),
    ("VERSIONING-v6", "versioning-policy.v6.json", "check-versioning-v6.py"),
    ("EVIDENCE-v5", "evidence.v5.json", "check-evidence-v5.py"),
    ("OPERABILITY-v4", "operability.v4.json", "check-operability-v4.py"),
]


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


def check(value: Any, *, verify_children: bool = True) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict) or set(value) != TOP:
        return ["response root is not exact/closed"]
    if (value.get("artifact"), value.get("version")) != \
            ("opensip.phase1a-a-prime-successor.response", 2):
        errors.append("artifact/version mismatch")
    if value.get("status") != "CANDIDATE-NOT-APPLIED-AWAITING-INDEPENDENT-COMBINED-REREVIEW":
        errors.append("response candidate state drift")
    authority = value.get("authority") or {}
    if authority != {
            "candidateState": "NOT-APPLIED", "authorityClaim": "NONE",
            "productAcceptance": False, "independentCombinedRereview": "REQUIRED",
            "seal": "DO-NOT-SEAL", "signoff": "NONE"}:
        errors.append("response authority/no-seal boundary drift")

    window = value.get("protectedInputHashWindow") or {}
    rows = window.get("capturedBeforeAuthoring") or []
    actual_matrix = {pathlib.Path(row.get("path", "")).name: row.get("sha256")
                     for row in rows if isinstance(row, dict)}
    if actual_matrix != PROTECTED or len(rows) != len(PROTECTED):
        errors.append("protected input before-window is incomplete or stale")
    if window.get("requiredAfterAuthoring") != "BYTE-IDENTICAL-TO-BEFORE" or \
            window.get("interpreter") != "python3 -B" or \
            window.get("pycPolicy") != "do-not-delete-existing-pycs; -B forbids new bytecode writes":
        errors.append("protected after-window/interpreter/pyc rule drift")
    for name, expected in PROTECTED.items():
        try:
            actual = sha_file(name)
        except OSError as exc:
            errors.append(f"protected input missing: {name}: {exc}")
            continue
        if actual != expected:
            errors.append(f"protected input changed: {name} {actual} != {expected}")

    packet = value.get("successorPacket") or {}
    outputs = packet.get("outputs") or []
    by_id = {row.get("id"): row for row in outputs if isinstance(row, dict)}
    if set(by_id) != {row[0] for row in OUTPUT_NAMES} or len(outputs) != len(OUTPUT_NAMES):
        errors.append("successor output pair set incomplete/duplicated")
    for ident, artifact, checker in OUTPUT_NAMES:
        row = by_id.get(ident) or {}
        expected = {
            "id": ident, "artifact": f"docs/coop/artifacts/{artifact}",
            "artifactSha256": sha_file(artifact),
            "checker": f"docs/coop/artifacts/{checker}",
            "checkerSha256": sha_file(checker),
            "status": "CANDIDATE-NOT-APPLIED",
        }
        if row != expected:
            errors.append(f"successor output hash/status drift: {ident}")
    response_checker = packet.get("responseChecker") or {}
    if response_checker != {
            "path": "docs/coop/artifacts/check-phase1a-a-prime-successor-v2.py",
            "sha256": sha_file("check-phase1a-a-prime-successor-v2.py"),
            "artifactHashRule": "response artifact hash is reported externally after this non-self-referential manifest is complete"}:
        errors.append("response checker/output hash rule drift")
    reused = packet.get("reusedUnchanged") or []
    expected_reused = [
        {"id": "D9-v1.7", "artifact": "docs/coop/artifacts/d9-exit-contract.v1.7.json",
         "artifactSha256": PROTECTED["d9-exit-contract.v1.7.json"],
         "checker": "docs/coop/artifacts/check-d9-v1.7.py",
         "checkerSha256": PROTECTED["check-d9-v1.7.py"]},
        {"id": "SCOPE-v5", "artifact": "docs/coop/artifacts/scope-correction-a3.v5.json",
         "artifactSha256": PROTECTED["scope-correction-a3.v5.json"],
         "checker": "docs/coop/artifacts/check-scope-correction-a3-v5.py",
         "checkerSha256": PROTECTED["check-scope-correction-a3-v5.py"]},
    ]
    if reused != expected_reused:
        errors.append("D9/scope unchanged reuse pins drift")
    edges = set((packet.get("dependencyGraph") or {}).get("edges") or [])
    required_edges = {
        "C2+RI -> EP6", "EP6 -> RT11", "EP6+RT11 -> VERSIONING-v6",
        "EP6+RT11+VERSIONING-v6 -> EVIDENCE-v5",
        "EVIDENCE-v5+RT11+D9-v1.7 -> OPERABILITY-v4",
    }
    if edges != required_edges or (packet.get("dependencyGraph") or {}).get("acyclic") is not True or \
            (packet.get("dependencyGraph") or {}).get("forbiddenBackEdge") != \
            "VERSIONING-v6 contains no Evidence/Run/Terminal/RunAuthorityIndex dependency":
        errors.append("successor dependency graph/back-edge rule drift")

    lineage = value.get("reviewLineage") or {}
    evidence_review = lineage.get("evidenceOperabilityReview") or {}
    retention_review = lineage.get("retentionFinalRereview") or {}
    if evidence_review.get("path") != \
            "docs/coop/artifacts/phase1a-a-prime-successor.review-independent-evidence-op.json" or \
            evidence_review.get("sha256") != PROTECTED[
                "phase1a-a-prime-successor.review-independent-evidence-op.json"] or \
            evidence_review.get("verdict") != "REQUIRED-CHANGES" or \
            evidence_review.get("finding") != "IR-E4OP3-01":
        errors.append("Evidence/OP independent review lineage drift/overstatement")
    if retention_review.get("path") != \
            "docs/coop/artifacts/retention-tiers.v10.rereview-independent-final.json" or \
            retention_review.get("sha256") != PROTECTED[
                "retention-tiers.v10.rereview-independent-final.json"] or \
            retention_review.get("verdict") != "REQUIRED-CHANGES/DO-NOT-SEAL" or \
            retention_review.get("blockers") != [
                "RR13-01 opaque admission", "cross-project aaaa/0000 authority lineage"] or \
            retention_review.get("passedPredecessorMechanismsOnly") != [
                "RR13-03", "Versioning custody rejoin"]:
        errors.append("retention final review lineage drift/overstatement")
    if lineage.get("adjudicationRule") != \
            "Conditional PASS observations prove only named predecessor mechanisms; neither review accepts superseded EP/RT or this successor packet.":
        errors.append("review conditional-PASS non-acceptance rule drift")

    try:
        ep = load("evaluation-proof.v6.json")
        rt = load("retention-tiers.v11.json")
        evidence = load("evidence.v5.json")
        op = load("operability.v4.json")
    except Exception as exc:
        errors.append(f"successor artifact load failed: {exc}")
        return errors
    closure = value.get("mechanicalClosure") or {}
    expected_same_project = {
        "projectId": "prj1-" + "a" * 64,
        "planIntentCommitment": ep["c2AuthorityJoin"]["expectedPlanIntentCommitment"],
        "snapshotId": ep["resolvedInputsAuthorityJoin"]["snapshotId"],
        "planId": ep["resolvedInputsAuthorityJoin"]["planId"],
        "acceptedVectorId": "EP6-POS-NOMATCH-PASS",
    }
    if closure.get("sameProjectAuthorityChain") != expected_same_project:
        errors.append("same-project C2/RI chain summary drift")
    counts = rt["capabilityClosure"]["closureGoldens"]["derivedCounts"]
    if closure.get("rawCustodyCounts") != counts or counts != {
            "rawRequirementCount": 23, "dependencyEdgeCount": 20,
            "unitCount": 2, "verifiableCount": 19, "replayableCount": 4}:
        errors.append("derived raw custody count summary drift")
    golden = evidence["acceptedGolden"]
    if closure.get("evidenceGoldens") != {key: golden[key] for key in (
            "evidenceDigest", "runId", "runSealRef")}:
        errors.append("Evidence digest/run/terminal summary drift")
    if closure.get("runAuthorityIndex") != golden["runAuthorityIndex"]:
        errors.append("RunAuthorityIndex summary drift")
    exact_d9 = op["aPrimeSuccessor"]["successorRepair"]["exactFailedCommitProjection"]
    if closure.get("operabilityFailedCommit") != exact_d9 or exact_d9 != {
            "class": "operational-failed", "errorCode": "DURABILITY.COMMIT_FAILED",
            "executionId": "$EXEC_ID"}:
        errors.append("OP4 exact D9 projection summary drift")
    required_matrix = {
        "project substitution", "opaque/arbitrary receipt", "missing/ambiguous store index",
        "receipt-to-resolved-input edge removal", "Terminal authority mismatch",
        "RunAuthorityIndex collision", "caller-constructed/serialized opaque handle",
        "RunAuthorityIndex content cycle",
    }
    if set(closure.get("adversarialMatrix") or []) != required_matrix:
        errors.append("required successor adversarial matrix incomplete")

    transfers = value.get("evidenceTransfer") or []
    states = {row.get("id"): row.get("state") for row in transfers if isinstance(row, dict)}
    if states != {
            "IR-E4OP3-01": "REPAIRED-IN-CANDIDATE-NOT-APPLIED",
            "RR13-01": "MECHANICALLY-CLOSED-IN-CANDIDATE-NOT-APPLIED",
            "RR13-03": "PREDECESSOR-PASS-MECHANISM-PRESERVED",
            "R12-EVD-01": "CANDIDATE-MECHANISM-SPECIFIED-NOT-APPLIED",
            "R12-DEP-01": "CANDIDATE-MECHANISM-SPECIFIED-NOT-APPLIED",
            "R14-EVD-TRANSFER": "CANDIDATE-MECHANISM-SPECIFIED-NOT-APPLIED"}:
        errors.append("finding transfer matrix drift/overstatement")
    residuals = {row.get("id"): row.get("state") for row in value.get("retainedResiduals", [])
                 if isinstance(row, dict)}
    if residuals != {"V10": "UNRESOLVED", "CD-RT-5": "BLOCKED", "G19": "BLOCKED",
                     "INDEPENDENT-COMBINED-REREVIEW": "REQUIRED",
                     "PRODUCT-QUALIFICATION": "ABSENT", "SEAL-SIGNOFF": "FORBIDDEN"}:
        errors.append("retained residual matrix drift")
    if value.get("recommendation") != \
            "DO NOT SEAL OR APPLY. Candidate is SPECIFIED / IMPLEMENTABLE_UNEXECUTED and requires independent combined rereview, CD-RT-5 disposition, implementation evidence and coordinator integration.":
        errors.append("recommendation/no-seal language drift")

    verification = value.get("verificationContract") or {}
    commands = verification.get("normalAndSelftest") or []
    expected_commands = []
    for _, artifact, checker in OUTPUT_NAMES:
        expected_commands.extend([
            f"python3 -B docs/coop/artifacts/{checker}",
            f"python3 -B docs/coop/artifacts/{checker} --selftest",
        ])
    expected_commands.extend([
        "python3 -B docs/coop/artifacts/check-d9-v1.7.py",
        "python3 -B docs/coop/artifacts/check-d9-v1.7.py --selftest",
        "python3 -B docs/coop/artifacts/check-scope-correction-a3-v5.py",
        "python3 -B docs/coop/artifacts/check-scope-correction-a3-v5.py --selftest",
    ])
    if commands != expected_commands or verification.get("interpreter") != "python3 -B" or \
            verification.get("evidenceClass") != "DESIGN-INTEGRITY-ONLY":
        errors.append("verification command/interpreter/evidence class drift")

    if verify_children:
        for ident, artifact, checker in OUTPUT_NAMES:
            try:
                checker_module = module(checker, "umbrella_" + ident.lower().replace("-", "_"))
                findings = checker_module.check(load(artifact))
                if findings:
                    errors.append(f"{ident} child checker red: {findings[0]}")
            except Exception as exc:
                errors.append(f"{ident} child checker import/run failed: {type(exc).__name__}: {exc}")
    return errors


def selftest(value: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    cases = []
    def add(label, mutate):
        candidate = copy.deepcopy(value); mutate(candidate); cases.append((label, candidate))
    add("review PASS inflation", lambda c: c["reviewLineage"]["evidenceOperabilityReview"].__setitem__("verdict", "PASS"))
    add("retention blocker omission", lambda c: c["reviewLineage"]["retentionFinalRereview"]["blockers"].pop())
    add("protected input hash", lambda c: c["protectedInputHashWindow"]["capturedBeforeAuthoring"][0].__setitem__("sha256", "0" * 64))
    add("output hash", lambda c: c["successorPacket"]["outputs"][0].__setitem__("artifactSha256", "0" * 64))
    add("custody count", lambda c: c["mechanicalClosure"]["rawCustodyCounts"].__setitem__("rawRequirementCount", 22))
    add("adversarial omission", lambda c: c["mechanicalClosure"]["adversarialMatrix"].pop())
    add("G19 promotion", lambda c: next(row for row in c["retainedResiduals"] if row["id"] == "G19").__setitem__("state", "IMPLEMENTABLE"))
    add("seal recommendation", lambda c: c.__setitem__("recommendation", "SEAL"))
    for label, candidate in cases:
        if not check(candidate, verify_children=False):
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
        print("PASS: phase1a-a-prime-successor.response.v2.json; 8 packet mutations rejected")
    else:
        print("PASS: phase1a-a-prime-successor.response.v2.json; 5 successor pairs + unchanged D9/scope; DO-NOT-SEAL")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
