#!/usr/bin/env python3
"""Packet checker for the Phase-1A A-prime candidate response.

Usage: python3 -B check-phase1a-a-prime-successor.py [response] [--selftest]
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
ROOT = HERE.parents[2]
BINDING = "phase1a-a-prime-successor.response.v1.json"

PROTECTED = {
    "docs/coop/artifacts/evaluation-proof.v5.json": "e05f6d8d9dd5f1f98dc1972a178c7fe58981c71b06a69feb00a717e03475988b",
    "docs/coop/artifacts/check-evaluation-proof.py": "1ccc12c347f0c7598604227179a2ba0cc461466657908b5c5f9645db4f7b99e2",
    "docs/coop/artifacts/retention-tiers.v10.json": "606b5e7125d4a3a46f44f1a7565f9c9ea69132d9ab2783d00339e1b8aac5e026",
    "docs/coop/artifacts/check-retention-custody.py": "15816cd8f9d22221b1187b94a160d71f644f9ab8fccb82423931fe18f6fc38d7",
    "docs/coop/artifacts/versioning-policy.v4.json": "8e6933b287a8082ea27647860938bd9cdae93b37132bba21221c2c24b40069e6",
    "docs/coop/artifacts/check-versioning.py": "67a45b275908afc4bd04cee6c15400f5d429f9f209854630c1caf5a43cf13227",
    "docs/coop/artifacts/evidence.v3.json": "c05c744b21682ab5aa37e6dfab7b6810be80ed7b0fd24b628375bcb5751c68e4",
    "docs/coop/artifacts/check-evidence.py": "6933d2931912a43e3018dc6037068230af0bbc0c0a00d5d9429c155930bde1af",
    "docs/coop/artifacts/operability.v2.json": "43e63e4bca8e238e933a6b3e0c91112fb29b52da5f92d64ff2438d79140e6f04",
    "docs/coop/artifacts/check-operability.py": "925496916ef2c7075c02f7a767353aa6ff047cf55557304f3983e17e1c5256e2",
    "docs/coop/artifacts/d9-exit-contract.v1.6.json": "c633614e17f6757cab74753d462eed53ade09dc234923d73b70d3042c6367046",
    "docs/coop/artifacts/check-d9.py": "9f8e16a0000e59d2f1326f97f1b8afcc5c7121eb0c57b6c440d76b9c401346a7",
    "docs/coop/artifacts/scope-correction-a3.v4.json": "a343581691314ff806e042825d0dadb540c913fc1862835aaa505604ea9c96cf",
    "docs/coop/artifacts/claim-register.v1.json": "2338f7e08d24dead2540f04f9f2a071af42870b34c851393ed863f9d89ab1b42",
    "docs/coop/artifacts/threat-model.v3.json": "56734a4047b61e1fc702f75ccb21e8721b334adb449093d266756d0b08adc499",
    "docs/coop/artifacts/product-dispositions.v1.json": "b9a87839606981a5be46f62aca2d85a17c3da5082c8d0aad02a211f3025fd91c",
    "docs/coop/artifacts/check-product-dispositions.py": "f73cb878ade9376f6f8a9c19a459742c1721932ad16625e6b63cd0d1645d732e",
}

OUTPUTS = {
    "VERSIONING-v5": ("docs/coop/artifacts/versioning-policy.v5.json",
                       "880bdae45e60da8ea06cbfa18aaf25e6dd902874fbe471b68cface4a5e617d66",
                       "docs/coop/artifacts/check-versioning-v5.py",
                       "cacde3a32ca71f22b806fee281946758dc14748e6bd80f42e2c1f034dd12b536", 21),
    "EVIDENCE-v4": ("docs/coop/artifacts/evidence.v4.json",
                    "4a5d2dc8d9067af103b6f8c898c83f08fdd59ee22ce49fb4cf12a1329c416c70",
                    "docs/coop/artifacts/check-evidence-v4.py",
                    "fd8db2ab77261ba31351d0647cf62ba4de92db35ba7a15426cb8f4bcf28865bc", 34),
    "D9-v1.7": ("docs/coop/artifacts/d9-exit-contract.v1.7.json",
                "d199aef6ac2edc7652325ef8d26f75cfda35a94f3e234d10aafd984d9088b2eb",
                "docs/coop/artifacts/check-d9-v1.7.py",
                "ead1dd8d3635a355475ba8d71611515497a29e59cdfc5d232f167588dd9fb6d3", 29),
    "SCOPE-v5": ("docs/coop/artifacts/scope-correction-a3.v5.json",
                 "6ca4bd407b80d80aba9035dfb4d66d28d8704ccf30a729854810396c6f66c7af",
                 "docs/coop/artifacts/check-scope-correction-a3-v5.py",
                 "5d777c42dfa6fb3826916b157f53955d66d07e93ce08acbdb1c27a027b753c0c", 9),
    "OPERABILITY-v3": ("docs/coop/artifacts/operability.v3.json",
                       "63f6bd846167d3ea011dcc3d34476cda1540ddf95fd87dfe08ada9825937ca81",
                       "docs/coop/artifacts/check-operability-v3.py",
                       "532e7cba2208d5b9969b348403d433fd638b3d6c5907e7fe847c6dac9905b49c", 31),
}

ORDER = ["VERSIONING-v5", "EVIDENCE-v4", "D9-v1.7", "SCOPE-v5",
         "OPERABILITY-v3"]
D9_CONSUMERS = {
    "c2-plan-stage-schema.v3.json / check-c2.py",
    "delivery.v2.json / check-delivery.py",
    "fact-plane.v1.json / check-fact-plane.py",
    "resolved-inputs.v2.json / check-resolved-inputs.py",
    "retention-tiers.v10.json / check-retention-custody.py",
    "versioning-policy.v5.json / check-versioning-v5.py",
    "operability.v2.json / check-operability.py",
}


def load_path(path: pathlib.Path) -> Any:
    return json.loads(path.read_text())


def file_hash(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(name: str, module_name: str) -> Any:
    spec = importlib.util.spec_from_file_location(module_name, HERE / name)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _architecture() -> tuple[list[dict[str, str]], str]:
    entries = []
    for path in sorted((ROOT / "docs/coop/architecture").glob("*.md")):
        relative = path.relative_to(ROOT).as_posix()
        entries.append({"path": relative, "sha256": file_hash(path)})
    payload = "".join(f"{x['path']}\0{x['sha256']}\n" for x in entries).encode()
    return entries, hashlib.sha256(payload).hexdigest()


def _component_findings() -> list[str]:
    findings: list[str] = []
    versioning = load_module("check-versioning-v5.py", "packet_versioning")
    evidence_checker = load_module("check-evidence-v4.py", "packet_evidence")
    d9_checker = load_module("check-d9-v1.7.py", "packet_d9")
    scope_checker = load_module("check-scope-correction-a3-v5.py", "packet_scope")
    op_checker = load_module("check-operability-v3.py", "packet_op")
    values = {
        "VERSIONING-v5": versioning.check(load_path(HERE / "versioning-policy.v5.json")),
        "EVIDENCE-v4": evidence_checker.check(load_path(HERE / "evidence.v4.json")),
        "D9-v1.7": d9_checker.check(load_path(HERE / "d9-exit-contract.v1.7.json"),
                                      load_path(HERE / "d9-exit-contract.v1.6.json")),
        "SCOPE-v5": scope_checker.check(load_path(HERE / "scope-correction-a3.v5.json"),
                                         load_path(HERE / "scope-correction-a3.v4.json")),
        "OPERABILITY-v3": op_checker.check(load_path(HERE / "operability.v3.json")),
    }
    for ident, errors in values.items():
        findings.extend(f"{ident}: {error}" for error in errors)
    return findings


def check(response: Any, *, verify_files: bool = True,
          verify_components: bool = True) -> list[str]:
    errors: list[str] = []
    if not isinstance(response, dict):
        return ["root must be an object"]
    evidence = load_path(HERE / "evidence.v4.json")
    operability = load_path(HERE / "operability.v3.json")

    if (response.get("artifact"), response.get("version")) != \
            ("opensip.phase1a-a-prime-successor-response", 1):
        errors.append("response artifact/version drifted")
    if response.get("status") != \
            "CANDIDATE-AWAITING-INDEPENDENT-COMBINED-REREVIEW / NOT-APPLIED":
        errors.append("response status drifted")
    if response.get("authority") != {
            "authorityClaim": "NONE", "signoff": False,
            "applicationState": "NOT-APPLIED", "productAcceptance": False,
            "independentReview": "REQUIRED",
            "coordinatorIntegration": "REQUIRED-AFTER-REREVIEW-AND-CD-RT-5"}:
        errors.append("response authority/no-signoff boundary drifted")
    method = response.get("selectedRepairMethod") or {}
    if method.get("choice") != "MECHANICAL-COMPATIBILITY-PROJECTIONS" or \
            method.get("alternativeNotTaken") != "patch every protected predecessor consumer" or \
            "D18" not in method.get("reason", "") or \
            "OP3-TO-OP2-EXACT-PROJECTION" not in method.get("reason", "") or \
            "not successor integration evidence" not in method.get("limitation", ""):
        errors.append("selected compatibility method/limitation drifted")

    protected_rows = response.get("protectedInputMatrix") or []
    protected_map = {x.get("path"): x for x in protected_rows if isinstance(x, dict)}
    if set(protected_map) != set(PROTECTED) or len(protected_map) != len(protected_rows):
        errors.append("protected input denominator is not exact/unique")
    for name, expected in PROTECTED.items():
        row = protected_map.get(name) or {}
        if row.get("sha256") != expected or not row.get("role"):
            errors.append(f"protected matrix pin/role drift: {name}")
        if verify_files:
            path = ROOT / name
            if not path.exists() or file_hash(path) != expected:
                errors.append(f"protected file missing/drifted: {name}")

    arch = response.get("protectedArchitectureNarratives") or {}
    actual_entries, actual_tree = _architecture()
    if arch.get("formula") != \
            "sha256(concat(sort(path) map path || NUL || sha256(fileBytes) || LF))" or \
            arch.get("entryCount") != 12 or arch.get("entries") != actual_entries or \
            arch.get("treeSha256") != actual_tree or arch.get("mutationAuthority") != "NONE":
        errors.append("protected architecture narrative commitment drifted")

    packet = response.get("successorPacket") or {}
    if packet.get("reviewOrder") != ORDER:
        errors.append("VERSIONING-first packet/review order drifted")
    output_rows = packet.get("outputs") or []
    output_map = {x.get("id"): x for x in output_rows if isinstance(x, dict)}
    if set(output_map) != set(OUTPUTS) or len(output_map) != len(output_rows):
        errors.append("successor output denominator is not exact/unique")
    for ident, (artifact, artifact_hash, checker, checker_hash, count) in OUTPUTS.items():
        expected_row = {
            "id": ident, "artifact": artifact, "artifactSha256": artifact_hash,
            "checker": checker, "checkerSha256": checker_hash,
            "mutationCount": count, "status": "CANDIDATE-NOT-APPLIED"}
        if output_map.get(ident) != expected_row:
            errors.append(f"successor output row drift: {ident}")
        if verify_files:
            for name, expected in ((artifact, artifact_hash), (checker, checker_hash)):
                path = ROOT / name
                if not path.exists() or file_hash(path) != expected:
                    errors.append(f"successor file missing/drifted: {name}")
    graph = packet.get("dependencyGraph") or {}
    expected_edges = {
        "EP5 -> VERSIONING-v5", "RT10 -> VERSIONING-v5",
        "EP5 -> EVIDENCE-v4", "RT10 -> EVIDENCE-v4",
        "VERSIONING-v5 -> EVIDENCE-v4", "D9-v1.7 -> SCOPE-v5",
        "EVIDENCE-v4 -> OPERABILITY-v3", "D9-v1.7 -> OPERABILITY-v3",
        "RT10 -> OPERABILITY-v3",
    }
    if set(graph.get("edges") or []) != expected_edges or \
            len(graph.get("edges") or []) != len(expected_edges) or \
            graph.get("acyclic") is not True or \
            "contains no Evidence" not in graph.get("forbiddenBackEdge", ""):
        errors.append("successor dependency graph/cycle boundary drifted")

    compat = response.get("compatibilityAdjudication") or {}
    d9 = compat.get("d9") or {}
    if d9.get("projection") != "check-d9-v1.7.py#D18" or \
            d9.get("predecessor") != {
                "artifact": "d9-exit-contract.v1.6.json",
                "sha256": PROTECTED["docs/coop/artifacts/d9-exit-contract.v1.6.json"],
                "checker": "check-d9.py",
                "checkerSha256": PROTECTED["docs/coop/artifacts/check-d9.py"]}:
        errors.append("D9 D18 projection/predecessor pin drifted")
    if d9.get("closedDelta") != [
            "metadata rollover v1.6 -> v1.7 candidate/not-applied",
            "one invariant-runid-commit-visibility insertion",
            "remove only analysis-durability-failed.expectedTermination.runId while retaining executionId",
            "update only the two checker reproduction command strings"]:
        errors.append("D9 D18 closed delta drifted")
    consumers = d9.get("consumers") or []
    if {x.get("consumer") for x in consumers if isinstance(x, dict)} != D9_CONSUMERS or \
            len(consumers) != len(D9_CONSUMERS) or any(not x.get("predecessorSurface")
                                                       for x in consumers):
        errors.append("D9 predecessor consumer denominator incomplete")
    d9_boundary = d9.get("validityBoundary", "")
    for phrase in ("only through D18", "predecessor evidence only",
                   "explicit narrow consumer rebind or external integration disposition",
                   "no stale v1.6 reference"):
        if phrase not in d9_boundary:
            errors.append(f"D9 compatibility boundary omits: {phrase}")

    op = compat.get("operability") or {}
    source_compat = operability["aPrimeSuccessor"]["compatibilityProjection"]
    expected_op = {
        "projection": "operability.v3.json#aPrimeSuccessor.compatibilityProjection / check-operability-v3.py",
        "predecessor": source_compat["predecessor"],
        "changedRootFields": source_compat["changedRootFields"],
        "unchangedTopLevelKeys": source_compat["unchangedTopLevelKeys"],
        "consumerBindings": source_compat["consumerBindings"],
        "validityBoundary": source_compat["integrationBoundary"],
    }
    if op != expected_op:
        errors.append("OPERABILITY exact projection/consumer matrix drifted")

    transfer = response.get("evidenceTransfer") or {}
    if transfer.get("findings") != evidence.get("reviewFindingTransfers") or \
            {x.get("id") for x in transfer.get("findings", [])} != {
                "R12-EVD-01", "R12-DEP-01", "R14-EVD-TRANSFER", "RR13-01"}:
        errors.append("Evidence review-finding transfers drifted")
    if "SemanticObjectBindingV1" not in transfer.get("semanticRawSeparation", "") or \
            "raw keys only" not in transfer.get("semanticRawSeparation", ""):
        errors.append("semantic/raw identity separation drifted")
    if "non-Display/non-Serialize" not in transfer.get("committedOnlyRunId", "") or \
            "failed commit carries ExecutionId and no RunId" not in transfer.get("committedOnlyRunId", ""):
        errors.append("committed-only RunId transfer drifted")
    if transfer.get("recursiveRequestIdExclusion") != \
            evidence.get("recursiveRequestIdExclusion") or \
            transfer.get("correlationDifferential") != operability["aPrimeSuccessor"]["recursiveRequestIdExclusion"]["variationFixture"] or \
            transfer.get("availabilityDifferential") != operability["aPrimeSuccessor"]["recursiveRequestIdExclusion"]["availabilityFixture"]:
        errors.append("recursive/correlation/availability Evidence transfer drifted")

    lifecycle = response.get("lifecycleAndProductAdjudication") or {}
    if lifecycle.get("publicSuccessPhase") != "run-committed" or \
            "forbidden in new v3 public events" not in lifecycle.get("legacyPhase", "") or \
            "ExecutionId only" not in lifecycle.get("failedCommit", "") or \
            "existing committed RunId" not in lifecycle.get("storedView", ""):
        errors.append("lifecycle adjudication drifted")
    if lifecycle.get("g19") != operability["aPrimeSuccessor"]["g19CandidateMechanism"]:
        errors.append("G19 candidate mechanism transfer drifted")
    if "CD-RT-5 remains UNRESOLVED" not in lifecycle.get("productBoundary", "") or \
            "G19 remains blocked" not in lifecycle.get("productBoundary", "") or \
            "V10/threat/product/claim authorities are unchanged" not in lifecycle.get("productBoundary", "") or \
            "not IMPLEMENTABLE product evidence" not in lifecycle.get("productBoundary", ""):
        errors.append("product/CD-RT-5/V10 boundary drifted")
    if "narrow successor or external integration disposition" not in \
            lifecycle.get("postProductBoundary", "") or \
            "independent re-review" not in lifecycle.get("postProductBoundary", ""):
        errors.append("post-product narrow integration boundary drifted")

    residuals = {x.get("id"): x.get("state") for x in response.get("retainedResiduals", [])
                 if isinstance(x, dict)}
    if residuals != {
            "CD-RT-5": "UNRESOLVED",
            "G19": "BLOCKED-PENDING-PRODUCT-DECISION-AND-IMPLEMENTATION",
            "LIVE-STORE": "IMPLEMENTABLE-UNEXECUTED",
            "PHYSICAL-ISOLATION": "IMPLEMENTABLE-UNEXECUTED",
            "INDEPENDENT-COMBINED-REREVIEW": "REQUIRED",
            "COORDINATOR-INTEGRATION": "REQUIRED-AFTER-PREREQUISITES",
            "EVIDENCE-V3-PREDECESSOR-CHECKER-API-DRIFT":
                "KNOWN-RED-PREDECESSOR-ONLY"}:
        errors.append("retained residual set/state drifted")
    legacy_residual = next((x for x in response.get("retainedResiduals", [])
                            if x.get("id") ==
                            "EVIDENCE-V3-PREDECESSOR-CHECKER-API-DRIFT"), {})
    if "reports 12 findings" not in legacy_residual.get("effect", "") or \
            "MUST NOT be called green or successor integration evidence" not in \
            legacy_residual.get("effect", ""):
        errors.append("known-red Evidence v3 predecessor caveat drifted")
    verification = response.get("verificationContract") or {}
    expected_commands = []
    for ident in ORDER:
        checker = OUTPUTS[ident][2]
        expected_commands.extend([f"python3 -B {checker}",
                                  f"python3 -B {checker} --selftest"])
    if verification.get("interpreter") != "python3 -B" or \
            verification.get("normalAndSelftest") != expected_commands or \
            verification.get("evidenceClass") != "DESIGN-INTEGRITY-ONLY" or \
            "do not constitute product qualification" not in \
            verification.get("explicitNonClaim", ""):
        errors.append("verification/non-claim contract drifted")
    expected_audit = [
        {"id": "VERSIONING-v4", "result": "PASS-PREDECESSOR-ONLY"},
        {"id": "EVIDENCE-v3", "result": "KNOWN-RED-PREDECESSOR-ONLY",
         "findingCount": 12,
         "cause": "Frozen check-evidence.py consumes superseded shared checker APIs: validate_bundle now requires authority and the retired retention v7 closure APIs are absent."},
        {"id": "OPERABILITY-v2", "result": "PASS-PREDECESSOR-ONLY"},
        {"id": "D9-v1.6", "result": "PASS-PREDECESSOR-ONLY"},
        {"id": "EP5", "result": "PASS-PROTECTED-INPUT"},
        {"id": "RT10", "result": "PASS-PROTECTED-INPUT"},
        {"id": "PRODUCT-DISPOSITIONS", "result": "PASS-PROTECTED-INPUT"},
    ]
    if verification.get("predecessorAudit") != expected_audit or \
            "known-red Evidence v3 result is retained explicitly" not in \
            verification.get("predecessorAuditRule", "") or \
            "none of these rows establishes successor rebind or integration" not in \
            verification.get("predecessorAuditRule", ""):
        errors.append("honest predecessor audit/result boundary drifted")
    if not response.get("recommendation", "").startswith("DO NOT SEAL OR APPLY"):
        errors.append("packet recommendation drifted")

    if verify_components:
        try:
            errors.extend(_component_findings())
        except Exception as exc:  # controlled boundary: imported checker failure
            errors.append(f"could not execute component checkers: {type(exc).__name__}: {exc}")
    return errors


def selftest(response: dict[str, Any]) -> list[str]:
    mutations: list[tuple[str, Any]] = []

    def add(name: str, fn: Any) -> None:
        mutations.append((name, fn))

    add("status", lambda x: x.__setitem__("status", "APPLIED"))
    add("signoff", lambda x: x["authority"].__setitem__("signoff", True))
    add("method", lambda x: x["selectedRepairMethod"].__setitem__("choice", "PATCH-CONSUMERS"))
    add("protected", lambda x: x["protectedInputMatrix"].pop())
    add("architecture", lambda x: x["protectedArchitectureNarratives"].__setitem__("treeSha256", "0" * 64))
    add("order", lambda x: x["successorPacket"]["reviewOrder"].reverse())
    add("output-hash", lambda x: x["successorPacket"]["outputs"][0].__setitem__("artifactSha256", "0" * 64))
    add("output-status", lambda x: x["successorPacket"]["outputs"][0].__setitem__("status", "APPLIED"))
    add("graph", lambda x: x["successorPacket"]["dependencyGraph"]["edges"].pop())
    add("cycle", lambda x: x["successorPacket"]["dependencyGraph"].__setitem__("acyclic", False))
    add("d9-delta", lambda x: x["compatibilityAdjudication"]["d9"]["closedDelta"].pop())
    add("d9-consumer", lambda x: x["compatibilityAdjudication"]["d9"]["consumers"].pop())
    add("d9-boundary", lambda x: x["compatibilityAdjudication"]["d9"].__setitem__("validityBoundary", "automatically integrated"))
    add("op-projection", lambda x: x["compatibilityAdjudication"]["operability"]["unchangedTopLevelKeys"].pop())
    add("finding", lambda x: x["evidenceTransfer"]["findings"].pop())
    add("semantic-raw", lambda x: x["evidenceTransfer"].__setitem__("semanticRawSeparation", "same hash"))
    add("commit", lambda x: x["evidenceTransfer"].__setitem__("committedOnlyRunId", "precommit visible"))
    add("request-id", lambda x: x["evidenceTransfer"]["recursiveRequestIdExclusion"]["surfaces"].pop())
    add("correlation", lambda x: x["evidenceTransfer"]["correlationDifferential"]["expectedEqual"]["runId"].__setitem__(1, "run1:" + "0" * 64))
    add("phase", lambda x: x["lifecycleAndProductAdjudication"].__setitem__("publicSuccessPhase", "attempt-sealed"))
    add("g19", lambda x: x["lifecycleAndProductAdjudication"]["g19"].__setitem__("productState", "ENABLED"))
    add("product", lambda x: x["lifecycleAndProductAdjudication"].__setitem__("productBoundary", "CD-RT-5 resolved"))
    add("post-product", lambda x: x["lifecycleAndProductAdjudication"].__setitem__("postProductBoundary", "automatic"))
    add("residual", lambda x: x["retainedResiduals"][0].__setitem__("state", "RESOLVED"))
    add("verification", lambda x: x["verificationContract"]["normalAndSelftest"].pop())
    add("predecessor-audit", lambda x: x["verificationContract"]["predecessorAudit"][1].__setitem__("result", "PASS"))
    add("recommendation", lambda x: x.__setitem__("recommendation", "SEAL"))
    failures: list[str] = []
    for name, fn in mutations:
        changed = copy.deepcopy(response)
        fn(changed)
        if not check(changed, verify_files=False, verify_components=False):
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
        response = load_path(path)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 2
    errors = check(response)
    if not errors and do_selftest:
        errors.extend(selftest(response))
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print(f"PASS: {path.name} candidate packet, projections and protected matrix are consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
