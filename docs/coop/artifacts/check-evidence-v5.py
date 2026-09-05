#!/usr/bin/env python3
"""Evidence v5 wire, identity, and atomic RunAuthorityIndex checker."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import pathlib
import sys
from typing import Any


HERE = pathlib.Path(__file__).resolve().parent
BINDING = "evidence.v5.json"
PINS = {
    "evidence.v4.json": "4a5d2dc8d9067af103b6f8c898c83f08fdd59ee22ce49fb4cf12a1329c416c70",
    "check-evidence-v4.py": "fd8db2ab77261ba31351d0647cf62ba4de92db35ba7a15426cb8f4bcf28865bc",
}
INDEX_FIELDS = [
    "schemaVersion", "projectId", "runId", "runSealRef",
    "planAuthorityReceiptRef", "evaluationAuthorityAdmissionRef", "planId",
    "planIntentCommitment", "executionPlanCommitment", "activationManifestRef",
    "evaluationAuthoritySealRef",
]
ATOMIC_PEERS = [
    "TerminalRunV1", "RunIndexV1", "AttemptRunLinkV1", "CustodyRootV1",
    "outbox",
]
FINAL_WRITES = [
    "TerminalRunV1", "RunIndexV1", "AttemptRunLinkV1", "CustodyRootV1",
    "RunAuthorityIndexV1", "outbox",
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


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def raw_golden(ident: str, value: dict[str, Any]) -> dict[str, Any]:
    encoded = b"opensip.run-authority-index.v1\0" + canonical(value)
    return {
        "id": ident, "recordType": "RunAuthorityIndexV1",
        "domainUtf8": "opensip.run-authority-index.v1", "value": value,
        "encodedHex": encoded.hex(), "byteLength": len(encoded),
        "rawCasRef": "sha256:" + hashlib.sha256(encoded).hexdigest(),
    }


def _vector(ep: dict[str, Any]) -> dict[str, Any]:
    return next(row for row in ep["positiveVectors"]
                if row.get("id") == "EP6-POS-NOMATCH-PASS")


def regenerate(ep: dict[str, Any], rt: dict[str, Any], evmod: Any) -> dict[str, Any]:
    vector = _vector(ep)
    authority_input = vector["authorityAdmissionInput"]
    temp_ep = {"positiveVectors": [{
        "id": "EP5-POS-NOMATCH-PASS", "bundle": vector["bundle"],
        "verifiedAuthorityInput": {
            "evaluationAuthoritySeal": authority_input["evaluationAuthoritySeal"]},
    }]}
    generated = evmod.regenerate(temp_ep, rt)
    values = generated["values"]
    index = {
        "schemaVersion": 1,
        "projectId": values["projectId"],
        "runId": generated["runId"],
        "runSealRef": generated["runSealRef"],
        "planAuthorityReceiptRef": vector["authorityGoldens"]["planAuthorityReceiptRef"],
        "evaluationAuthorityAdmissionRef": vector["authorityGoldens"]["evaluationAuthorityAdmissionRef"],
        "planId": values["planId"],
        "planIntentCommitment": values["planIntentCommitment"],
        "executionPlanCommitment": values["executionPlanCommitment"],
        "activationManifestRef": values["activationManifestRef"],
        "evaluationAuthoritySealRef": values["evaluationAuthoritySealRef"],
    }
    accepted = {
        "id": "EVIDENCE5-ACCEPTED-EP6-NOMATCH",
        "sourceVectorId": "EP6-POS-NOMATCH-PASS",
        "values": values,
        "rawProofInventoryLength": len(generated["inventory"]),
        "rawProofInventoryHex": generated["inventory"].hex(),
        "semanticEvidenceLength": len(generated["evidence"]),
        "semanticEvidenceHex": generated["evidence"].hex(),
        "semanticEvidenceCasRef": evmod.sha_ref(generated["evidence"]),
        "evidenceDigestDomain": "opensip.semantic-evidence.v1",
        "evidenceDigestPreimageLength": len(generated["evidencePreimage"]),
        "evidenceDigestPreimageHex": generated["evidencePreimage"].hex(),
        "evidenceDigest": generated["evidenceDigest"],
        "runIdentityRecordLength": len(generated["runBytes"]),
        "runIdentityRecordHex": generated["runBytes"].hex(),
        "runDomainPreimageLength": len(generated["runPreimage"]),
        "runDomainPreimageHex": generated["runPreimage"].hex(),
        "runId": generated["runId"],
        "terminalRunLength": len(generated["terminal"]),
        "terminalRunEncodedHex": generated["terminal"].hex(),
        "runSealRef": generated["runSealRef"],
        "runAuthorityIndex": index,
        "runAuthorityIndexRaw": raw_golden("EVIDENCE5-RUN-AUTHORITY-INDEX", index),
    }
    return {"accepted": accepted, "substitutions": generated["runSubstitutions"],
            "generated": generated, "vector": vector}


def _has_key(value: Any, target: str) -> bool:
    if isinstance(value, dict):
        return target in value or any(_has_key(child, target) for child in value.values())
    if isinstance(value, list):
        return any(_has_key(child, target) for child in value)
    return False


def check(value: Any, *, verify_files: bool = True) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["root is not an object"]
    try:
        predecessor = load("evidence.v4.json")
        ep = load("evaluation-proof.v6.json")
        rt = load("retention-tiers.v11.json")
        versioning = load("versioning-policy.v6.json")
        evmod = module("check-evidence-v4.py", "evidence_v4_pinned_for_v5")
        epmod = module("check-evaluation-proof-v6.py", "ep6_for_evidence_v5")
        rtmod = module("check-retention-custody-v11.py", "rt11_for_evidence_v5")
        vmod = module("check-versioning-v6.py", "versioning_v6_for_evidence_v5")
    except Exception as exc:
        return [f"dependency import failed: {type(exc).__name__}: {exc}"]
    for name, expected in PINS.items():
        if sha_file(name) != expected:
            errors.append(f"Evidence v4 predecessor drift: {name}")
    if verify_files:
        old_errors = evmod.check(predecessor)
        if old_errors:
            errors.append(f"Evidence v4 predecessor mechanism red: {old_errors[0]}")
        for label, checker, artifact in (
                ("EP6", epmod, ep), ("RT11", rtmod, rt), ("VERSIONING-v6", vmod, versioning)):
            child_errors = checker.check(artifact)
            if child_errors:
                errors.append(f"{label} dependency red: {child_errors[0]}")
    if (value.get("artifact"), value.get("version")) != ("opensip.evidence", 5):
        errors.append("artifact/version mismatch")
    if value.get("status") != "CANDIDATE-NOT-APPLIED" or \
            value.get("sealRecommendation") != "DO-NOT-SEAL":
        errors.append("candidate/no-seal status drift")
    if value.get("supersedes") != {
            "artifact": "evidence.v4.json", "sha256": PINS["evidence.v4.json"],
            "checker": "check-evidence-v4.py",
            "checkerSha256": PINS["check-evidence-v4.py"]}:
        errors.append("Evidence v4 predecessor pin drift")
    authority = value.get("authority") or {}
    if authority != {
            "candidateState": "NOT-APPLIED", "authorityClaim": "NONE",
            "independentReview": "REQUIRED", "productAcceptance": False,
            "integrationAuthority": "coordinator-only after independent combined rereview and separate CD-RT-5 disposition"}:
        errors.append("Evidence candidate/non-authority boundary drift")
    residuals = json.dumps(value.get("retainedResiduals") or [])
    if not all(term in residuals for term in ("V10", "CD-RT-5", "G19", "no seal")):
        errors.append("Evidence residual/no-seal matrix incomplete")

    dependencies = value.get("dependencies") or {}
    expected_deps = {
        "evaluationProof": ("evaluation-proof.v6.json", "check-evaluation-proof-v6.py", "EP6"),
        "retentionCustody": ("retention-tiers.v11.json", "check-retention-custody-v11.py", "RT11"),
        "versioning": ("versioning-policy.v6.json", "check-versioning-v6.py", "V6"),
    }
    for key, (artifact, checker, token) in expected_deps.items():
        row = dependencies.get(key) or {}
        if row.get("artifact") != artifact or row.get("checker") != checker or \
                row.get("sha256") != sha_file(artifact) or \
                row.get("checkerSha256") != sha_file(checker):
            errors.append(f"dependency pin drift: {key}")
    direction = dependencies.get("dependencyDirection", "")
    if not all(term in direction for term in (
            "EP6", "RT11", "VERSIONING v6", "post-core RunAuthorityIndexV1", "acyclic")):
        errors.append("dependency direction/cycle statement incomplete")
    if "evidence" in json.dumps((versioning.get("successorRevision") or {}).get("inputs") or {}).lower():
        errors.append("VERSIONING v6 has forbidden Evidence back-edge")

    # The byte grammar is retained exactly; only owner/version labels roll.
    expected_grammar = json.loads(json.dumps(predecessor["canonicalWireGrammar"])
                                  .replace("EP5", "EP6").replace("RT10", "RT11"))
    if value.get("canonicalWireGrammar") != expected_grammar:
        errors.append("retained Evidence v4 wire grammar changed beyond owner labels")
    imported = value.get("importedAuthorityContract") or {}
    if imported.get("owner") != "evaluation-proof.v6.json" or \
            imported.get("capabilityType") != "AdmittedEvaluationAuthorityV1 (module-private, non-serializable)" or \
            imported.get("admissionInputType") != "EvaluationAuthorityAdmissionInputV1":
        errors.append("EP6 authority ownership/capability import drift")
    if imported.get("records") != ep.get("rawAuthorityRecordGrammar", {}).get("records") or \
            imported.get("recordGoldens") != ep.get("rawAuthorityGoldens") or \
            imported.get("storeIndex") != ep.get("evaluationAuthorityStoreIndex") or \
            imported.get("dependencyGraph") != ep.get("authorityDependencyGraph"):
        errors.append("EP6 raw authority grammar/goldens/index/graph not imported exactly")
    text = json.dumps(value)
    for stale in ("EP5", "RT10", "VERSIONING v5", "VerifiedEvaluationAuthorityInputV2",
                  "VerifiedEvaluationAuthorityV2"):
        if stale in text:
            errors.append(f"stale predecessor owner label remains: {stale}")

    try:
        expected = regenerate(ep, rt, evmod)
    except Exception as exc:
        errors.append(f"wire regeneration failed: {type(exc).__name__}: {exc}")
        return errors
    if value.get("acceptedGolden") != expected["accepted"]:
        errors.append("EvidenceDigest/RunId/Terminal/RunAuthorityIndex golden does not regenerate")
    if value.get("runSubstitutionGoldens") != expected["substitutions"]:
        errors.append("six RunId substitution goldens do not regenerate")
    closure = rt["capabilityClosure"]["semanticClosure"]
    inventory_items = expected["accepted"]["values"]
    if len(closure["proofRefs"]) != 23 or \
            {row["requiredForCapability"] for row in closure["proofRefs"]} != {
                "verifiable", "replayable"}:
        errors.append("accepted inventory source is not actual RT11 23-ref closure")

    index_contract = value.get("runAuthorityIndexContract") or {}
    if index_contract.get("type") != "RunAuthorityIndexV1" or \
            index_contract.get("key") != ["projectId", "runId"] or \
            index_contract.get("required") != INDEX_FIELDS or \
            index_contract.get("optional") != [] or \
            index_contract.get("atomicPeers") != ATOMIC_PEERS:
        errors.append("RunAuthorityIndexV1 closed schema/key/atomic peers drift")
    if not all(term in index_contract.get("cycleExclusion", "") for term in (
            "post-content", "SemanticEvidenceV1", "EvidenceDigest",
            "RunIdentityPreimageV1", "RunId", "TerminalRunV1", "No pre-core RunId")):
        errors.append("RunAuthorityIndex content-cycle exclusion incomplete")
    if "byte-identical" not in index_contract.get("collisionRule", "") or \
            "corruption" not in index_contract.get("collisionRule", ""):
        errors.append("RunAuthorityIndex collision rule incomplete")
    index = expected["accepted"]["runAuthorityIndex"]
    if list(index) != INDEX_FIELDS:
        errors.append("RunAuthorityIndex field order/shape drift")
    vector = expected["vector"]
    receipt = vector["authorityAdmissionInput"]["planAuthorityReceipt"]
    admission = vector["authorityAdmissionInput"]["evaluationAuthorityAdmission"]
    terminal_equalities = {
        "projectId": admission["projectId"], "planId": receipt["planId"],
        "planIntentCommitment": receipt["planIntentCommitment"],
        "executionPlanCommitment": vector["authorityAdmissionInput"]["evaluationAuthoritySeal"]["executionPlanCommitment"],
        "activationManifestRef": admission["activationManifestRef"],
        "evaluationAuthoritySealRef": admission["evaluationAuthoritySealRef"],
    }
    if any(index[key] != expected_value for key, expected_value in terminal_equalities.items()):
        errors.append("RunAuthorityIndex does not equality-rejoin Terminal to admitted receipts")
    final_tx = (value.get("storeContract") or {}).get("finalTransaction") or {}
    if final_tx.get("boundary") != "ONE_PROJECT_LEDGER_TRANSACTION" or \
            final_tx.get("writes") != FINAL_WRITES or \
            "RunAuthorityIndex" not in final_tx.get("visibility", "") or \
            "collision" not in final_tx.get("retry", ""):
        errors.append("atomic final RunAuthorityIndex transaction drift")
    index_raw = expected["accepted"]["runAuthorityIndexRaw"]
    if bytes.fromhex(index_raw["encodedHex"]) != \
            b"opensip.run-authority-index.v1\0" + canonical(index):
        errors.append("RunAuthorityIndex raw golden encoding drift")
    # The post-core index cannot affect any content identity.
    index_ref = index_raw["rawCasRef"]
    if index_ref.encode("ascii") in expected["generated"]["evidence"] or \
            index_ref.encode("ascii") in expected["generated"]["runBytes"] or \
            index_ref.encode("ascii") in expected["generated"]["terminal"] or \
            any(row["recordCasRef"] == index_ref for row in closure["proofRefs"]):
        errors.append("RunAuthorityIndex entered EvidenceDigest/RunId/Terminal/raw closure cycle")
    if _has_key(vector["authorityAdmissionInput"], "runId"):
        errors.append("pre-core authority contains RunId")
    adversarial = value.get("adversarialControls") or {}
    required_terminal = {"Terminal activationManifestRef mismatch",
                         "Terminal evaluationAuthoritySealRef mismatch"}
    required_store = {"same ProjectId+RunId different RunAuthorityIndex",
                      "RunAuthorityIndex included in EvidenceDigest or any pre-core/content identity cycle"}
    if not required_terminal.issubset(set(adversarial.get("terminal") or [])) or \
            not required_store.issubset(set(adversarial.get("store") or [])):
        errors.append("Terminal authority/collision/content-cycle adversarial controls incomplete")
    return errors


def selftest(value: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    cases = []
    def add(label, mutate):
        candidate = copy.deepcopy(value); mutate(candidate); cases.append((label, candidate))
    add("Terminal authority mismatch", lambda c: c["acceptedGolden"]["runAuthorityIndex"].__setitem__(
        "evaluationAuthoritySealRef", "sha256:" + "0" * 64))
    add("Terminal manifest mismatch", lambda c: c["acceptedGolden"]["runAuthorityIndex"].__setitem__(
        "activationManifestRef", "sha256:" + "0" * 64))
    add("Run-index collision weakening", lambda c: c["runAuthorityIndexContract"].__setitem__(
        "collisionRule", "last writer wins"))
    add("content cycle", lambda c: c["runAuthorityIndexContract"].__setitem__(
        "cycleExclusion", "index is included in EvidenceDigest"))
    add("index raw golden", lambda c: c["acceptedGolden"]["runAuthorityIndexRaw"].__setitem__(
        "encodedHex", "00"))
    add("Evidence digest", lambda c: c["acceptedGolden"].__setitem__(
        "evidenceDigest", "sha256:" + "1" * 64))
    add("RunId", lambda c: c["acceptedGolden"].__setitem__(
        "runId", "run1:" + "2" * 64))
    add("run seal", lambda c: c["acceptedGolden"].__setitem__(
        "runSealRef", "sha256:" + "3" * 64))
    add("atomic peer omission", lambda c: c["storeContract"]["finalTransaction"]["writes"].pop())
    add("dependency direction", lambda c: c["dependencies"].__setitem__(
        "dependencyDirection", "Evidence feeds VERSIONING"))
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
        print("PASS: evidence.v5.json; 10 successor mutations rejected")
    else:
        golden = value["acceptedGolden"]
        print(f"PASS: evidence.v5.json; EvidenceDigest {golden['evidenceDigest']}; "
              f"RunId {golden['runId']}; atomic RunAuthorityIndexV1 clean")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
