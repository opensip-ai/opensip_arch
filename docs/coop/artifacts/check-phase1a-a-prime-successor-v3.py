#!/usr/bin/env python3
"""Umbrella integrity checker for the Phase-1A A-prime response v3."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import pathlib
import sys
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[3]
HERE = pathlib.Path(__file__).resolve().parent
BINDING = "phase1a-a-prime-successor.response.v3.json"
TOP = {
    "artifact", "version", "date", "status", "author", "authority",
    "selectedRepairMethod", "reviewLineage", "protectedInputHashWindow",
    "successorPacket", "mechanicalClosure", "evidenceTransfer",
    "retainedResiduals", "verificationContract", "recommendation",
}
REVIEW_PINS = {
    "docs/coop/artifacts/phase1a-a-prime-successor-v2.review-independent-evidence-op.json":
        "9e863b925b77579603e8e449c25f58563edd710d4b720adce6882f125b249861",
    "docs/coop/artifacts/retention-tiers.v11.rereview-independent-final.json":
        "86f592ec6f553fadee789a3d08002139ab88da670f82704ac2d591be71dd0612",
}
OUTPUTS = {
    "EP7": (
        "evaluation-proof.v7.json", "92d51e9232c6ee137b7228aa7885a2e32f668f9b4b108d7140fdb52dae864ef8",
        "check-evaluation-proof-v7.py", "550a2231264ab6b308b3ddb752199c6496f7c2417a8dbeeb9f21c230569b36c4"),
    "RT12": (
        "retention-tiers.v12.json", "1a034746512de51605b7a4bcc4fb0936bdc167db057a3018be74a2a047376dab",
        "check-retention-custody-v12.py", "104a8f9bd01e92226c11c41c234358b5a9d991b42cf12ec9318582ed12b57851"),
    "VERSIONING-v7": (
        "versioning-policy.v7.json", "0c0f2d7396c32854c3cd5a6aff794c6a0e1be2ffe833816f9ff66f0089b49985",
        "check-versioning-v7.py", "27cc2e22dd909de2ee3050387f87129477ee050e5b25c541dcf305902fbb9d76"),
    "EVIDENCE-v6": (
        "evidence.v6.json", "a941cd24365ce4b0bd43de45698dc045d292005e378ed87e5e6884732e83e102",
        "check-evidence-v6.py", "ad3aa393abac0a5094678c3f29b2a4478eccb651b747c0e19e2e69499cab92f4"),
    "OPERABILITY-v5": (
        "operability.v5.json", "89a18ffde1df3255b6a766aa74d1ad496ee3c7ed09cf5d69aa0ef34451699d8f",
        "check-operability-v5.py", "047afb978bc02b62402e4036bb42659a7ac14d427408ef06d59d8a8d7438ef70"),
}
D9_SCOPE = {
    "d9-exit-contract.v1.7.json": "d199aef6ac2edc7652325ef8d26f75cfda35a94f3e234d10aafd984d9088b2eb",
    "check-d9-v1.7.py": "ead1dd8d3635a355475ba8d71611515497a29e59cdfc5d232f167588dd9fb6d3",
    "scope-correction-a3.v5.json": "6ca4bd407b80d80aba9035dfb4d66d28d8704ccf30a729854810396c6f66c7af",
    "check-scope-correction-a3-v5.py": "5d777c42dfa6fb3826916b157f53955d66d07e93ce08acbdb1c27a027b753c0c",
}


def load(name_or_path: str | pathlib.Path) -> Any:
    path = pathlib.Path(name_or_path)
    if not path.is_absolute():
        if path.parts and path.parts[0] == "docs":
            path = ROOT / path
        elif path.parent == pathlib.Path("."):
            path = HERE / path
    return json.loads(path.read_text())


def sha_path(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha_file(name: str) -> str:
    return sha_path(HERE / name)


def module(filename: str, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    if spec is None or spec.loader is None:
        raise ImportError(filename)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def _protected_manifest() -> dict[str, str]:
    review_path = ROOT / next(iter(REVIEW_PINS))
    if sha_path(review_path) != next(iter(REVIEW_PINS.values())):
        raise ValueError("primary final review drift before protected manifest read")
    review = load(review_path)
    locked = review.get("inputLock") or {}
    manifest = locked.get("manifest")
    if locked.get("inputCount") != 77 or not isinstance(manifest, dict) or len(manifest) != 77:
        raise ValueError("primary final review 77-input lock malformed")
    result = dict(manifest)
    result.update(REVIEW_PINS)
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


def check(value: Any, *, verify_children: bool = True) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict) or set(value) != TOP:
        return ["response root is not exact/closed"]
    if (value.get("artifact"), value.get("version")) != \
            ("opensip.phase1a-a-prime-successor.response", 3):
        errors.append("artifact/version mismatch")
    if value.get("status") != "CANDIDATE-NOT-APPLIED-AWAITING-INDEPENDENT-COMBINED-REREVIEW":
        errors.append("response candidate state drift")
    authority = value.get("authority") or {}
    if authority != {
            "candidateState": "NOT-APPLIED", "authorityClaim": "NONE",
            "productAcceptance": False, "independentCombinedRereview": "REQUIRED",
            "seal": "DO-NOT-SEAL", "signoff": "NONE"}:
        errors.append("response authority/no-seal boundary drift")

    try:
        protected = _protected_manifest()
    except Exception as exc:
        return [f"protected manifest load failed: {type(exc).__name__}: {exc}"]
    window = value.get("protectedInputHashWindow") or {}
    rows = window.get("capturedBeforeAuthoring") or []
    actual_matrix = {row.get("path"): row.get("sha256")
                     for row in rows if isinstance(row, dict)}
    if actual_matrix != protected or len(rows) != 79:
        errors.append("protected 77-input baseline plus two final reviews is incomplete/stale")
    if window.get("requiredAfterAuthoring") != "BYTE-IDENTICAL-TO-BEFORE" or \
            window.get("interpreter") != "python3 -B" or \
            window.get("pycPolicy") != "do-not-delete-existing-pycs; -B forbids new bytecode writes":
        errors.append("protected after-window/interpreter/pyc rule drift")
    for relpath, expected in protected.items():
        path = ROOT / relpath
        if not path.exists():
            errors.append(f"protected input missing: {relpath}")
            continue
        actual = sha_path(path)
        if actual != expected:
            errors.append(f"protected input changed: {relpath} {actual} != {expected}")

    packet = value.get("successorPacket") or {}
    outputs = packet.get("outputs") or []
    by_id = {row.get("id"): row for row in outputs if isinstance(row, dict)}
    if set(by_id) != set(OUTPUTS) or len(outputs) != len(OUTPUTS):
        errors.append("successor output pair set incomplete/duplicated")
    for ident, (artifact, artifact_hash, checker, checker_hash) in OUTPUTS.items():
        if sha_file(artifact) != artifact_hash or sha_file(checker) != checker_hash:
            errors.append(f"hard-pinned output changed: {ident}")
        expected = {
            "id": ident, "artifact": f"docs/coop/artifacts/{artifact}",
            "artifactSha256": artifact_hash,
            "checker": f"docs/coop/artifacts/{checker}",
            "checkerSha256": checker_hash, "status": "CANDIDATE-NOT-APPLIED",
        }
        if by_id.get(ident) != expected:
            errors.append(f"successor output hash/status drift: {ident}")
    if packet.get("reviewOrder") != list(OUTPUTS):
        errors.append("successor review order drift")
    response_checker = packet.get("responseChecker") or {}
    if response_checker != {
            "path": "docs/coop/artifacts/check-phase1a-a-prime-successor-v3.py",
            "sha256": sha_file("check-phase1a-a-prime-successor-v3.py"),
            "artifactHashRule": "response artifact hash is reported externally after this non-self-referential manifest is complete"}:
        errors.append("response checker/output hash rule drift")
    reused = packet.get("reusedUnchanged") or []
    expected_reused = [
        {"id": "D9-v1.7", "artifact": "docs/coop/artifacts/d9-exit-contract.v1.7.json",
         "artifactSha256": D9_SCOPE["d9-exit-contract.v1.7.json"],
         "checker": "docs/coop/artifacts/check-d9-v1.7.py",
         "checkerSha256": D9_SCOPE["check-d9-v1.7.py"]},
        {"id": "SCOPE-v5", "artifact": "docs/coop/artifacts/scope-correction-a3.v5.json",
         "artifactSha256": D9_SCOPE["scope-correction-a3.v5.json"],
         "checker": "docs/coop/artifacts/check-scope-correction-a3-v5.py",
         "checkerSha256": D9_SCOPE["check-scope-correction-a3-v5.py"]},
    ]
    if reused != expected_reused:
        errors.append("D9/scope unchanged reuse pins drift")
    for name, expected in D9_SCOPE.items():
        if sha_file(name) != expected:
            errors.append(f"D9/scope protected input changed: {name}")
    graph = packet.get("dependencyGraph") or {}
    expected_edges = {
        "C2+RI+host ProjectStoreAuthority -> EP7",
        "EP7 -> RT12", "EP7+RT12 -> VERSIONING-v7",
        "EP7+RT12+VERSIONING-v7 -> EVIDENCE-v6",
        "EVIDENCE-v6+RT12+D9-v1.7 -> OPERABILITY-v5",
    }
    if set(graph.get("edges") or []) != expected_edges or graph.get("acyclic") is not True or \
            graph.get("forbiddenBackEdge") != \
            "VERSIONING-v7 contains no Evidence/Run/Terminal/RunAuthorityIndex/store-token dependency":
        errors.append("successor dependency graph/back-edge rule drift")

    lineage = value.get("reviewLineage") or {}
    review1_row = lineage.get("evidenceOperabilityReview") or {}
    review2_row = lineage.get("retentionFinalRereview") or {}
    review1_path = "docs/coop/artifacts/phase1a-a-prime-successor-v2.review-independent-evidence-op.json"
    review2_path = "docs/coop/artifacts/retention-tiers.v11.rereview-independent-final.json"
    if review1_row != {
            "path": review1_path, "sha256": REVIEW_PINS[review1_path],
            "verdict": "REQUIRED-CHANGES", "finding": "IR-E5OP4-01",
            "conditionalMechanismsOnly": [
                "regenerated identities/wire bytes/terminal-index transaction design internally coherent",
                "OP2 projection, D9 mapping and blocked product state internally coherent"],
            "withheld": ["RR13-01", "R12-DEP", "R14", "packet acceptance", "seal/application"]}:
        errors.append("E5/OP4 final review lineage drift/overstatement")
    if review2_row != {
            "path": review2_path, "sha256": REVIEW_PINS[review2_path],
            "verdict": "REQUIRED-CHANGES/DO-NOT-SEAL",
            "blockers": ["R17-P1A-RR13-01-STORE-PROVENANCE"],
            "closedPredecessorFindingsOnly": [
                "R16-P1A-PROJECT-IDENTITY-JOIN", "RR13-03",
                "R15-P1A-VERSIONING-REJOIN-01 at the EP/RT custody boundary"]}:
        errors.append("RT11 final rereview lineage drift/overstatement")
    if lineage.get("adjudicationRule") != \
            "Both exact REQUIRED-CHANGES reviews diagnose the superseded EP6 packet. Their conditional mechanism observations are retained, but neither review accepts EP7/RT12/V7/E6/OP5 or response v3.":
        errors.append("review non-acceptance adjudication rule drift")
    try:
        review1 = load(review1_path)
        review2 = load(review2_path)
        ids1 = {row.get("id") for row in review1.get("blockingFindings", [])}
        verdict2 = review2.get("verdict") or {}
        if review1.get("verdict") != "REQUIRED-CHANGES" or ids1 != {"IR-E5OP4-01"}:
            errors.append("primary review content differs from pinned summary")
        if verdict2.get("decision") != "REQUIRED-CHANGES" or \
                verdict2.get("sealRecommendation") != "DO-NOT-SEAL" or \
                verdict2.get("blockingFindings") != ["R17-P1A-RR13-01-STORE-PROVENANCE"]:
            errors.append("retention rereview content differs from pinned summary")
    except Exception as exc:
        errors.append(f"review content load failed: {exc}")

    try:
        ep = load("evaluation-proof.v7.json")
        rt = load("retention-tiers.v12.json")
        evidence = load("evidence.v6.json")
        op = load("operability.v5.json")
        epmod = module("check-evaluation-proof-v7.py", "ep7_for_response_v3")
    except Exception as exc:
        errors.append(f"successor artifact load failed: {exc}")
        return errors
    closure = value.get("mechanicalClosure") or {}
    expected_same_project = {
        "projectId": "prj1-" + "a" * 64,
        "planIntentCommitment": ep["c2AuthorityJoin"]["expectedPlanIntentCommitment"],
        "snapshotId": ep["resolvedInputsAuthorityJoin"]["snapshotId"],
        "planId": ep["resolvedInputsAuthorityJoin"]["planId"],
        "acceptedVectorId": "EP7-POS-NOMATCH-PASS",
    }
    if closure.get("sameProjectAuthorityChain") != expected_same_project:
        errors.append("same-project C2/RI chain summary drift")
    vector = next(row for row in ep["positiveVectors"]
                  if row.get("id") == "EP7-POS-NOMATCH-PASS")
    candidate = vector["evaluationAuthorityCandidate"]
    if "evaluationAuthorityStoreIndex" in candidate:
        errors.append("accepted untrusted candidate carries store index")
    try:
        store = epmod._open_test_project_store(vector["trustedStoreFixture"])
        handle = epmod.authorize_evaluation(store, candidate)
        epmod.assert_store_continuity(store, handle)
    except Exception as exc:
        errors.append(f"store-proven authority summary does not execute: {exc}")
    store_summary = closure.get("storeProvenance") or {}
    if store_summary != {
            "candidateType": "EvaluationAuthorityCandidateV1",
            "candidateCarriesIndex": False,
            "storePortType": "ProjectStoreAuthorityV1 (opaque/nonserializable/project+instance-bound)",
            "authorizeOrder": ["raw+C2+RI+semantic recomputation", "CAS publish-or-exact-verify",
                               "unique index insert-or-exact-verify", "trusted reread",
                               "mint store-bound admitted handle"],
            "finalization": "Evidence v6 commit_run requires identical store instance and admitted handle",
            "fixtureOnly": True}:
        errors.append("store provenance/continuity summary drift")
    raw_rows = [{"recordType": row["recordType"], "byteLength": row["byteLength"],
                 "rawCasRef": row["rawCasRef"]} for row in ep["rawAuthorityGoldens"]]
    if closure.get("rawAuthorityGoldens") != raw_rows:
        errors.append("raw authority golden summary drift")
    if closure.get("semanticGoldens") != vector["authorityGoldens"]:
        errors.append("semantic/raw/index golden summary drift")
    counts = rt["capabilityClosure"]["closureGoldens"]["derivedCounts"]
    if closure.get("rawCustodyCounts") != counts or counts != {
            "rawRequirementCount": 23, "dependencyEdgeCount": 20,
            "unitCount": 2, "verifiableCount": 19, "replayableCount": 4}:
        errors.append("derived raw custody count summary drift")
    expected_units = [{
        "unitId": row["unitId"], "requiredForCapability": row["requiredForCapability"],
        "objectCount": len(row["objectRefs"])}
        for row in rt["capabilityClosure"]["semanticClosure"]["units"]]
    if closure.get("custodyUnits") != expected_units:
        errors.append("exact custody unit summary drift")
    golden = evidence["acceptedGolden"]
    if closure.get("evidenceGoldens") != {key: golden[key] for key in (
            "semanticEvidenceCasRef", "evidenceDigest", "runId", "runSealRef")} or \
            closure.get("runAuthorityIndex") != golden["runAuthorityIndex"] or \
            closure.get("runAuthorityIndexRaw") != {
                "byteLength": 996,
                "rawCasRef": "sha256:bf50d2d6b01dcdc09ef13f830a1b8ed208547c549e53816ba282c99e53185dad"}:
        errors.append("Evidence identity/RunAuthorityIndex summary drift")
    exact_d9 = op["aPrimeSuccessor"]["successorRepair"]["exactFailedCommitProjection"]
    if closure.get("operabilityFailedCommit") != exact_d9 or exact_d9 != {
            "class": "operational-failed", "errorCode": "DURABILITY.COMMIT_FAILED",
            "executionId": "$EXEC_ID"}:
        errors.append("OP5 exact D9 projection summary drift")
    required_matrix = {
        "forged candidate index field", "plain-dict/string/boolean/ref store",
        "wrong-project store", "absent/duplicate/conflicting trusted index",
        "missing trusted CAS", "caller-created/serialized store or handle",
        "different-store finalizer", "TOCTOU index replacement",
        "RunAuthorityIndex collision with no partial publication",
        "store token content-identity injection", "exact D9 failed-commit non-publication",
    }
    if set(closure.get("adversarialMatrix") or []) != required_matrix:
        errors.append("required store-provenance adversarial matrix incomplete")
    if closure.get("assurance") != \
            "SPECIFIED / IMPLEMENTABLE_UNEXECUTED; candidate NOT-APPLIED; no runtime/store/transaction/atomicity/product qualification evidence":
        errors.append("mechanical assurance/non-claim summary drift")

    transfers = value.get("evidenceTransfer") or []
    states = {row.get("id"): row.get("state") for row in transfers if isinstance(row, dict)}
    if states != {
            "IR-E4OP3-01": "PREDECESSOR-SAME-PROJECT-REPAIR-PRESERVED",
            "IR-E5OP4-01": "REPAIRED-IN-CANDIDATE-NOT-APPLIED",
            "R17-P1A-RR13-01-STORE-PROVENANCE": "REPAIRED-IN-CANDIDATE-NOT-APPLIED",
            "RR13-01": "STORE-PROVENANCE-REPAIRED-IN-CANDIDATE-NOT-APPLIED",
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
            "DO NOT SEAL OR APPLY. Candidate is SPECIFIED / IMPLEMENTABLE_UNEXECUTED. The two pinned reviews are REQUIRED-CHANGES reviews of the superseded packet, not acceptance of v3; fresh independent combined rereview, CD-RT-5 disposition, implementation evidence and coordinator integration remain required.":
        errors.append("recommendation/no-seal/review language drift")

    verification = value.get("verificationContract") or {}
    commands = verification.get("normalAndSelftest") or []
    expected_commands = []
    for artifact, _, checker, _ in OUTPUTS.values():
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
            verification.get("evidenceClass") != "DESIGN-INTEGRITY-ONLY" or \
            verification.get("explicitNonClaim") != \
            "Green guarded in-memory normal/selftests are not production runtime/store/transaction execution, atomicity demonstration, product qualification, independent acceptance, integration, seal or signoff.":
        errors.append("verification command/interpreter/evidence-class/non-claim drift")
    if verification.get("umbrella") != [
            "python3 -B docs/coop/artifacts/check-phase1a-a-prime-successor-v3.py",
            "python3 -B docs/coop/artifacts/check-phase1a-a-prime-successor-v3.py --selftest"]:
        errors.append("umbrella verification command drift")

    if verify_children:
        for ident, (artifact, _, checker, _) in OUTPUTS.items():
            try:
                checker_module = module(checker, "umbrella_v3_" + ident.lower().replace("-", "_"))
                findings = checker_module.check(load(artifact))
                if findings:
                    errors.append(f"{ident} child checker red: {findings[0]}")
            except Exception as exc:
                errors.append(f"{ident} child checker import/run failed: {type(exc).__name__}: {exc}")
    return errors


def selftest(value: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    cases = []

    def add(label: str, mutate: Any) -> None:
        candidate = copy.deepcopy(value)
        mutate(candidate)
        cases.append((label, candidate))

    add("review PASS inflation", lambda c: c["reviewLineage"]["evidenceOperabilityReview"].__setitem__("verdict", "PASS"))
    add("retention blocker omission", lambda c: c["reviewLineage"]["retentionFinalRereview"]["blockers"].pop())
    add("protected input hash", lambda c: c["protectedInputHashWindow"]["capturedBeforeAuthoring"][0].__setitem__("sha256", "0" * 64))
    add("output hash", lambda c: c["successorPacket"]["outputs"][0].__setitem__("artifactSha256", "0" * 64))
    add("candidate index authority", lambda c: c["mechanicalClosure"]["storeProvenance"].__setitem__("candidateCarriesIndex", True))
    add("custody count", lambda c: c["mechanicalClosure"]["rawCustodyCounts"].__setitem__("rawRequirementCount", 22))
    add("adversarial omission", lambda c: c["mechanicalClosure"]["adversarialMatrix"].pop())
    add("G19 promotion", lambda c: next(row for row in c["retainedResiduals"] if row["id"] == "G19").__setitem__("state", "IMPLEMENTABLE"))
    add("atomicity overclaim", lambda c: c["mechanicalClosure"].__setitem__("assurance", "DEMONSTRATED"))
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
        print("PASS: phase1a-a-prime-successor.response.v3.json; 10 packet mutations rejected")
    else:
        print("PASS: phase1a-a-prime-successor.response.v3.json; 5 successor pairs + "
              "79 protected inputs + unchanged D9/scope; DO-NOT-SEAL")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
