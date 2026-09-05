#!/usr/bin/env python3
"""Retained checker for the candidate Evidence v4 A-prime contract.

This checker independently regenerates the accepted EP5/RT10 inventory,
SemanticEvidence, EvidenceDigest, RUN-ID-V1 and TerminalRun byte vectors.  It
also binds the exact predecessor/dependency bytes and checks the atomic
publication, capability and authority boundaries.  Success is design evidence
only; the candidate remains not applied and carries no sign-off authority.

Usage: python3 -B check-evidence-v4.py [contract] [--selftest]
"""
from __future__ import annotations

import copy
import hashlib
import json
import pathlib
import sys
from typing import Any

HERE = pathlib.Path(__file__).resolve().parent
BINDING = "evidence.v4.json"

FILES = {
    "evidence.v3.json": "c05c744b21682ab5aa37e6dfab7b6810be80ed7b0fd24b628375bcb5751c68e4",
    "check-evidence.py": "6933d2931912a43e3018dc6037068230af0bbc0c0a00d5d9429c155930bde1af",
    "evaluation-proof.v5.json": "e05f6d8d9dd5f1f98dc1972a178c7fe58981c71b06a69feb00a717e03475988b",
    "check-evaluation-proof.py": "1ccc12c347f0c7598604227179a2ba0cc461466657908b5c5f9645db4f7b99e2",
    "retention-tiers.v10.json": "606b5e7125d4a3a46f44f1a7565f9c9ea69132d9ab2783d00339e1b8aac5e026",
    "check-retention-custody.py": "15816cd8f9d22221b1187b94a160d71f644f9ab8fccb82423931fe18f6fc38d7",
    "versioning-policy.v5.json": "880bdae45e60da8ea06cbfa18aaf25e6dd902874fbe471b68cface4a5e617d66",
    "check-versioning-v5.py": "cacde3a32ca71f22b806fee281946758dc14748e6bd80f42e2c1f034dd12b536",
}

EXPECTED_DEPS = {
    "evaluationProof": {
        "artifact": "evaluation-proof.v5.json",
        "sha256": FILES["evaluation-proof.v5.json"],
        "checker": "check-evaluation-proof.py",
        "checkerSha256": FILES["check-evaluation-proof.py"],
        "grammarSha256": "343889cf713931b0e228d84de82cb67d8cb22cc13ae2b3cc71302476f89ef9e0",
        "acceptedVectorId": "EP5-POS-NOMATCH-PASS",
    },
    "retentionCustody": {
        "artifact": "retention-tiers.v10.json",
        "sha256": FILES["retention-tiers.v10.json"],
        "checker": "check-retention-custody.py",
        "checkerSha256": FILES["check-retention-custody.py"],
        "grammarSha256": "abd8c541da028f2a273cc509bb8a2bc1c19eb78618ea56676ac301a83dd82ef8",
        "acceptedClosureCommitment": "sha256:3e2e151273a69e1f9ccb0272f6a507de45e9fd1f43e4094507537ee1e34cac57",
    },
    "versioning": {
        "artifact": "versioning-policy.v5.json",
        "sha256": FILES["versioning-policy.v5.json"],
        "checker": "check-versioning-v5.py",
        "checkerSha256": FILES["check-versioning-v5.py"],
    },
}

RECORDS = {
    "RawProofInventoryItemV1": ("0x80", [
        ("recordCasRef", "0x85"), ("recordKind", "0x86"),
        ("requiredForCapability", "0x87")]),
    "RawProofInventoryV1": ("0x81", [
        ("schemaVersion", "0x88"), ("projectId", "0x89"),
        ("items", "0x8a")]),
    "SemanticEvidenceV1": ("0x82", [
        ("schemaVersion", "0x90"), ("projectId", "0x91"),
        ("planId", "0x92"), ("evaluationAuthoritySealRef", "0x93"),
        ("evaluationProofBundleCasRef", "0x94"),
        ("universeCommitment", "0x95"),
        ("outcomeSetCommitment", "0x96"),
        ("verdictDerivationCommitment", "0x97"), ("verdict", "0x98"),
        ("sealedCapability", "0x99"), ("rawProofInventory", "0x9a"),
        ("semanticCapabilityClosureCasRef", "0x9b"),
        ("semanticCapabilityClosureCommitment", "0x9c")]),
    "RunIdentityPreimageV1": ("0x83", [
        ("schemaMajor", "0xa0"), ("projectId", "0xa1"),
        ("planId", "0xa2"), ("evaluationAuthoritySealRef", "0xa3"),
        ("evidenceDigest", "0xa4"), ("sealedCapability", "0xa5")]),
    "TerminalRunV1": ("0x84", [
        ("schemaVersion", "0xb0"), ("projectId", "0xb1"),
        ("runId", "0xb2"), ("planId", "0xb3"),
        ("planIntentCommitment", "0xb4"),
        ("executionPlanCommitment", "0xb5"),
        ("activationManifestRef", "0xb6"),
        ("evaluationAuthoritySealRef", "0xb7"),
        ("semanticEvidenceCasRef", "0xb8"), ("evidenceDigest", "0xb9"),
        ("verdict", "0xba"), ("sealedCapability", "0xbb"),
        ("semanticCapabilityClosureCasRef", "0xbc"),
        ("semanticCapabilityClosureCommitment", "0xbd")]),
}


def load(name: str) -> Any:
    return json.loads((HERE / name).read_text())


def digest_file(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")


def sha_ref(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def frame(tag: int, value: Any) -> bytes:
    data = value if isinstance(value, bytes) else str(value).encode("utf-8")
    return bytes([tag]) + len(data).to_bytes(4, "big") + data


def record(tag: int, fields: list[bytes]) -> bytes:
    return bytes([tag]) + b"".join(fields)


def envelope(domain: str, payload: bytes) -> bytes:
    return record(0x8E, [frame(0x8C, domain), frame(0x8D, payload)])


def find_id(value: Any, target: str) -> Any:
    if isinstance(value, dict):
        if value.get("id") == target:
            return value
        for child in value.values():
            found = find_id(child, target)
            if found is not None:
                return found
    elif isinstance(value, list):
        for child in value:
            found = find_id(child, target)
            if found is not None:
                return found
    return None


def _run_bytes(values: dict[str, Any]) -> bytes:
    return record(0x83, [
        frame(0xA0, values["schemaMajor"]), frame(0xA1, values["projectId"]),
        frame(0xA2, values["planId"]),
        frame(0xA3, values["evaluationAuthoritySealRef"]),
        frame(0xA4, values["evidenceDigest"]),
        frame(0xA5, values["sealedCapability"]),
    ])


def regenerate(ep5: dict[str, Any], rt10: dict[str, Any]) -> dict[str, Any]:
    vector = next(x for x in ep5["positiveVectors"]
                  if x["id"] == "EP5-POS-NOMATCH-PASS")
    bundle = vector["bundle"]
    authority = vector["verifiedAuthorityInput"]["evaluationAuthoritySeal"]
    closure = rt10["capabilityClosure"]["semanticClosure"]
    bundle_ref = sha_ref(canonical_json_bytes(bundle))
    closure_ref = sha_ref(canonical_json_bytes(closure))

    item_bytes = sorted(record(0x80, [
        frame(0x85, item["recordCasRef"]), frame(0x86, item["recordKind"]),
        frame(0x87, item["requiredForCapability"]),
    ]) for item in closure["proofRefs"])
    inventory = record(0x81, [
        frame(0x88, 1), frame(0x89, authority["projectId"]),
        frame(0x8A, b"".join(frame(0x8B, item) for item in item_bytes)),
    ])
    evidence = record(0x82, [
        frame(0x90, 1), frame(0x91, authority["projectId"]),
        frame(0x92, authority["planId"]),
        frame(0x93, bundle["evaluationAuthoritySealRef"]),
        frame(0x94, bundle_ref),
        frame(0x95, bundle["requiredUniverse"]["universeCommitment"]),
        frame(0x96, bundle["verdictProof"]["outcomeSetCommitment"]),
        frame(0x97, bundle["verdictProof"]["derivationCommitment"]),
        frame(0x98, bundle["verdictProof"]["verdict"]),
        frame(0x99, closure["sealedCapability"]), frame(0x9A, inventory),
        frame(0x9B, closure_ref), frame(0x9C, closure["closureCommitment"]),
    ])
    evidence_preimage = envelope("opensip.semantic-evidence.v1", evidence)
    evidence_digest = sha_ref(evidence_preimage)
    run_values = {
        "schemaMajor": 1, "projectId": authority["projectId"],
        "planId": authority["planId"],
        "evaluationAuthoritySealRef": bundle["evaluationAuthoritySealRef"],
        "evidenceDigest": evidence_digest,
        "sealedCapability": closure["sealedCapability"],
    }
    run_bytes = _run_bytes(run_values)
    run_preimage = envelope("opensip.run-id.v1", run_bytes)
    run_id = "run1:" + hashlib.sha256(run_preimage).hexdigest()
    terminal = record(0x84, [
        frame(0xB0, 1), frame(0xB1, authority["projectId"]),
        frame(0xB2, run_id), frame(0xB3, authority["planId"]),
        frame(0xB4, authority["planIntentCommitment"]),
        frame(0xB5, authority["executionPlanCommitment"]),
        frame(0xB6, authority["activationManifestRef"]),
        frame(0xB7, bundle["evaluationAuthoritySealRef"]),
        frame(0xB8, sha_ref(evidence)), frame(0xB9, evidence_digest),
        frame(0xBA, bundle["verdictProof"]["verdict"]),
        frame(0xBB, closure["sealedCapability"]), frame(0xBC, closure_ref),
        frame(0xBD, closure["closureCommitment"]),
    ])
    substitutions = [
        ("RUN-SUB-SCHEMA-MAJOR", {"schemaMajor": 2}),
        ("RUN-SUB-PROJECT", {"projectId": "prj1-" + "b" * 64}),
        ("RUN-SUB-PLAN", {"planId": "plan1:sha256:" + "b" * 64}),
        ("RUN-SUB-AUTHORITY", {"evaluationAuthoritySealRef": "sha256:" + "c" * 64}),
        ("RUN-SUB-EVIDENCE", {"evidenceDigest": "sha256:" + "d" * 64}),
        ("RUN-SUB-CAPABILITY", {"sealedCapability": "verifiable"}),
    ]
    run_subs = []
    for ident, mutation in substitutions:
        changed = dict(run_values)
        changed.update(mutation)
        rid = "run1:" + hashlib.sha256(
            envelope("opensip.run-id.v1", _run_bytes(changed))).hexdigest()
        run_subs.append({"id": ident, "mutation": mutation, "expectedRunId": rid})

    values = {
        "projectId": authority["projectId"], "planId": authority["planId"],
        "evaluationAuthoritySealRef": bundle["evaluationAuthoritySealRef"],
        "planIntentCommitment": authority["planIntentCommitment"],
        "executionPlanCommitment": authority["executionPlanCommitment"],
        "activationManifestRef": authority["activationManifestRef"],
        "evaluationProofBundleCasRef": bundle_ref,
        "universeCommitment": bundle["requiredUniverse"]["universeCommitment"],
        "outcomeSetCommitment": bundle["verdictProof"]["outcomeSetCommitment"],
        "verdictDerivationCommitment": bundle["verdictProof"]["derivationCommitment"],
        "verdict": bundle["verdictProof"]["verdict"],
        "sealedCapability": closure["sealedCapability"],
        "semanticCapabilityClosureCasRef": closure_ref,
        "semanticCapabilityClosureCommitment": closure["closureCommitment"],
    }
    return {
        "values": values, "inventory": inventory, "evidence": evidence,
        "evidencePreimage": evidence_preimage, "evidenceDigest": evidence_digest,
        "runBytes": run_bytes, "runPreimage": run_preimage, "runId": run_id,
        "terminal": terminal, "runSealRef": sha_ref(terminal),
        "runSubstitutions": run_subs, "bundle": bundle, "authority": authority,
        "closure": closure,
    }


def check(contract: Any, *, verify_files: bool = True) -> list[str]:
    errors: list[str] = []
    if not isinstance(contract, dict):
        return ["root must be an object"]
    ep5 = load("evaluation-proof.v5.json")
    rt10 = load("retention-tiers.v10.json")
    v5 = load("versioning-policy.v5.json")
    if verify_files:
        for name, expected in FILES.items():
            try:
                actual = digest_file(name)
            except OSError as exc:
                errors.append(f"cannot read {name}: {exc}")
                continue
            if actual != expected:
                errors.append(f"protected file drift: {name} {actual} != {expected}")

    if (contract.get("artifact"), contract.get("version")) != ("opensip.evidence", 4):
        errors.append("artifact/version must be opensip.evidence v4")
    if contract.get("status") != "CANDIDATE-AWAITING-INDEPENDENT-COMBINED-REREVIEW":
        errors.append("candidate status drifted")
    if contract.get("supersedes") != {
        "artifact": "evidence.v3.json", "sha256": FILES["evidence.v3.json"],
        "checker": "check-evidence.py", "checkerSha256": FILES["check-evidence.py"]}:
        errors.append("Evidence v3 predecessor pin drifted")
    authority = contract.get("authority") or {}
    if authority != {
        "candidateState": "NOT-APPLIED", "authorityClaim": "NONE",
        "independentReview": "REQUIRED", "productAcceptance": False,
        "integrationAuthority": "coordinator-only after independent combined rereview and separate CD-RT-5 disposition"}:
        errors.append("candidate/non-authority boundary drifted")

    transfers = contract.get("reviewFindingTransfers") or []
    transfer_by_id = {x.get("id"): x for x in transfers if isinstance(x, dict)}
    expected_transfer_ids = {"R12-EVD-01", "R12-DEP-01", "R14-EVD-TRANSFER",
                             "RR13-01"}
    if set(transfer_by_id) != expected_transfer_ids or len(transfers) != 4 or any(
            item.get("state") != "CANDIDATE-MECHANISM-SPECIFIED-NOT-APPLIED"
            or not item.get("closure") or not item.get("evidence")
            for item in transfer_by_id.values()):
        errors.append("review-finding transfer set/state is not exact candidate-only")
    transfer_blob = json.dumps(transfers, sort_keys=True)
    for required in ("atomic final commit", "no Evidence back-edge",
                     "semantic commitments never serve as physical raw-object keys",
                     "admitted before core invocation"):
        if required not in transfer_blob:
            errors.append(f"review-finding transfer omits: {required}")
    recursive = contract.get("recursiveRequestIdExclusion") or {}
    expected_surfaces = {
        "EP5 EvaluationAuthoritySealV1",
        "EP5 SemanticObjectBindingV1",
        "RT10 SemanticCapabilityClosureV3 semanticRoots/bindings/proofRefs/edges/units",
        "RawProofInventoryV1 and every RawProofInventoryItemV1",
        "SemanticEvidenceV1", "EvidenceDigest preimage",
        "RunIdentityPreimageV1", "TerminalRunV1 and external runSealRef",
    }
    if set(recursive.get("surfaces") or []) != expected_surfaces or \
            len(recursive.get("surfaces") or []) != len(expected_surfaces):
        errors.append("recursive RequestId exclusion surface set is not exact")
    if "Unknown fields reject" not in recursive.get("rule", "") or \
            "Two RequestIds and distinct ExecutionIds" not in recursive.get("differential", "") or \
            "root and each nested" not in recursive.get("negativeControl", ""):
        errors.append("recursive/differential RequestId exclusion rule drifted")

    deps = contract.get("dependencies") or {}
    for key, expected in EXPECTED_DEPS.items():
        if deps.get(key) != expected:
            errors.append(f"dependency pin drift: {key}")
    direction = deps.get("dependencyDirection", "")
    if "EP5 and RT10 feed VERSIONING v5" not in direction or "acyclic" not in direction:
        errors.append("dependency direction/cycle statement drifted")
    cap_join = ((v5.get("historicalSemanticsPolicy") or {}).get("capabilityJoin"))
    if not isinstance(cap_join, dict) or "evidence" in json.dumps(cap_join).lower():
        errors.append("VERSIONING v5 join missing or has forbidden Evidence back-edge")

    imported = contract.get("importedAuthorityContract") or {}
    expected_authority_record = next((x for x in ep5["normativePreimageGrammar"]["records"]
                                      if x.get("name") == "EvaluationAuthoritySealV1"), None)
    expected_binding_record = next((x for x in ep5["normativePreimageGrammar"]["records"]
                                    if x.get("name") == "SemanticObjectBindingV1"), None)
    if imported.get("owner") != "evaluation-proof.v5.json":
        errors.append("EP5 authority ownership drifted")
    if imported.get("record") != expected_authority_record:
        errors.append("imported EvaluationAuthoritySealV1 grammar drifted")
    if imported.get("semanticObjectBinding") != expected_binding_record:
        errors.append("imported SemanticObjectBindingV1 grammar drifted")
    if imported.get("recordGolden") != find_id(ep5, "EP5-REC-EVALUATION-AUTHORITY-SEAL"):
        errors.append("imported authority record golden drifted")
    if imported.get("commitmentGolden") != find_id(ep5, "EP5-COMMIT-EVALUATION-AUTHORITY-SEAL"):
        errors.append("imported authority commitment golden drifted")
    schema = imported.get("bindingSchema") or {}
    if schema.get("required") != ["projectId", "semanticDomain", "semanticRef",
                                  "recordCasRef", "recordKind"] or schema.get("optional") != []:
        errors.append("semantic binding schema is not exact/closed")

    grammar = contract.get("canonicalWireGrammar") or {}
    if grammar.get("id") != "EVIDENCE-RUN-TERMINAL-GRAMMAR-V1":
        errors.append("wire grammar id drifted")
    if grammar.get("domainEnvelope") != {
        "recordTag": "0x8e",
        "fields": [
            {"name": "domain", "tag": "0x8c", "encoding": "blobFrame(ASCII)"},
            {"name": "payload", "tag": "0x8d", "encoding": "blobFrame(bytes)"}],
        "encoding": "0x8e || blob(0x8c, domain ASCII) || blob(0x8d, payload)"}:
        errors.append("domain-envelope grammar drifted")
    expected_tags = {f"0x{x:02x}" for x in list(range(0x80, 0x8F))
                     + list(range(0x90, 0x9D)) + list(range(0xA0, 0xA6))
                     + list(range(0xB0, 0xBE))}
    tags = [x.get("tag") for x in grammar.get("tagRegistry", []) if isinstance(x, dict)]
    if set(tags) != expected_tags or len(tags) != len(expected_tags):
        errors.append("Evidence tag registry is not exact/unique")
    rt_tags = {x.get("tag") for x in rt10["capabilityClosure"]["closureGrammar"]["tagRegistry"]}
    if set(tags) & rt_tags:
        errors.append("Evidence tags collide with RT10 tags")
    records = grammar.get("records") or {}
    for name, (record_tag, field_pairs) in RECORDS.items():
        item = records.get(name) or {}
        actual_pairs = [(x.get("name"), x.get("tag")) for x in item.get("fields", [])]
        if item.get("recordTag") != record_tag or item.get("required") != [x[0] for x in field_pairs] \
                or actual_pairs != field_pairs:
            errors.append(f"{name} exact fields/tags drifted")
    if "runSealRef" not in (records.get("TerminalRunV1") or {}).get("forbidden", []):
        errors.append("TerminalRunV1 does not forbid self-reference")
    if (records.get("RunIdentityPreimageV1") or {}).get("domain") != "opensip.run-id.v1":
        errors.append("RunId domain drifted")
    commitments = grammar.get("commitments") or {}
    if "opensip.semantic-evidence.v1" not in commitments.get("EvidenceDigest", ""):
        errors.append("EvidenceDigest domain recipe drifted")
    if "opensip.run-id.v1" not in commitments.get("RunId", ""):
        errors.append("RunId domain recipe drifted")

    regenerated = regenerate(ep5, rt10)
    golden = contract.get("acceptedGolden") or {}
    if golden.get("id") != "EVD4-GOLDEN-EP5-RT10-NOMATCH-PASS" or \
            golden.get("sourceVectorIds") != ["EP5-POS-NOMATCH-PASS",
                                              "RT10-GOLDEN-SEMANTIC-CAPABILITY-CLOSURE-V3"]:
        errors.append("accepted golden source binding drifted")
    expected_golden = {
        "values": regenerated["values"],
        "rawProofInventoryCount": len(regenerated["closure"]["proofRefs"]),
        "rawProofInventoryLength": len(regenerated["inventory"]),
        "rawProofInventoryEncodedHex": regenerated["inventory"].hex(),
        "rawProofInventorySha256": sha_ref(regenerated["inventory"]),
        "semanticEvidenceLength": len(regenerated["evidence"]),
        "semanticEvidenceEncodedHex": regenerated["evidence"].hex(),
        "semanticEvidenceCasRef": sha_ref(regenerated["evidence"]),
        "evidenceDigestDomain": "opensip.semantic-evidence.v1",
        "evidenceDigestPreimageLength": len(regenerated["evidencePreimage"]),
        "evidenceDigestPreimageHex": regenerated["evidencePreimage"].hex(),
        "evidenceDigest": regenerated["evidenceDigest"],
        "runIdentityRecordLength": len(regenerated["runBytes"]),
        "runIdentityRecordHex": regenerated["runBytes"].hex(),
        "runDomainPreimageLength": len(regenerated["runPreimage"]),
        "runDomainPreimageHex": regenerated["runPreimage"].hex(),
        "runId": regenerated["runId"],
        "terminalRunLength": len(regenerated["terminal"]),
        "terminalRunEncodedHex": regenerated["terminal"].hex(),
        "runSealRef": regenerated["runSealRef"],
    }
    actual_golden = {key: golden.get(key) for key in expected_golden}
    if actual_golden != expected_golden:
        errors.append("accepted combined byte/hash golden does not regenerate")
    if contract.get("runSubstitutionGoldens") != regenerated["runSubstitutions"]:
        errors.append("six RunId substitution goldens do not regenerate")

    closure = regenerated["closure"]
    proof_refs = closure.get("proofRefs") or []
    if len(proof_refs) != 22 or any(set(x) != {"identityKind", "projectId", "recordCasRef",
                                               "recordKind", "requiredForCapability"}
                                    or x.get("identityKind") != "raw-cas"
                                    or x.get("projectId") != closure.get("projectId")
                                    for x in proof_refs):
        errors.append("RT10 raw proof inventory source is not exact/raw-only")
    if len(closure.get("semanticRoots") or []) != 2 or \
            any(x.get("identityKind") != "semantic-commitment"
                for x in closure.get("semanticRoots") or []):
        errors.append("RT10 semantic root boundary drifted")
    if len(closure.get("semanticObjectBindings") or []) != 2:
        errors.append("RT10 semantic-to-raw binding count drifted")
    if any(root.get("semanticRef") == item.get("recordCasRef")
           for root in closure.get("semanticRoots") or [] for item in proof_refs):
        errors.append("semantic commitment was conflated with raw custody key")

    apis = contract.get("apiContract") or {}
    call_text = "\n".join(apis.get("calls") or [])
    for required in ("admit_evaluation_authority_seal_v1", "validate_semantic_bundle_v1",
                     "validate_run_free_closure_v3", "prepare_custody_v1",
                     "finalize_semantic_evidence_v1", "prepare_run_commit_v1",
                     "commit_prepared_run_v1", "read_committed_run_v1", "project_read_v1"):
        if required not in call_text:
            errors.append(f"missing API seam: {required}")
    if "module-private" not in apis.get("constructionRule", "") or \
            "only CommittedRunV1 exposes it" not in apis.get("constructionRule", ""):
        errors.append("opaque construction/precommit RunId rule drifted")

    store = contract.get("storeContract") or {}
    store_records = store.get("records") or {}
    expected_store_fields = {
        "RunFreePreparedCommitV1": ["schemaVersion", "projectId", "executionId",
                                     "expectedAttemptRevision", "semanticEvidenceCasRef",
                                     "preparedCustodyToken"],
        "RunIndexV1": ["schemaVersion", "projectId", "runId", "runSealRef"],
        "AttemptRunLinkV1": ["schemaVersion", "projectId", "executionId",
                             "disposition", "runId", "runSealRef"],
        "RunCustodyRootV1": ["schemaVersion", "projectId", "runId", "runSealRef",
                             "semanticEvidenceCasRef", "unitIds"],
    }
    for name, required in expected_store_fields.items():
        if (store_records.get(name) or {}).get("required") != required:
            errors.append(f"store record drift: {name}")
    if "runId" not in (store_records.get("RunFreePreparedCommitV1") or {}).get("forbidden", []):
        errors.append("prepared journal is not Run-free")
    txn = "\n".join(store.get("transaction") or [])
    recovery = "\n".join(store.get("recovery") or [])
    for required in ("private staging namespace", "one serializable transaction",
                     "RunIndexV1", "AttemptRunLinkV1", "RunCustodyRootV1",
                     "run-committed", "only after commit", "failure emits no RunId"):
        if required not in txn:
            errors.append(f"atomic transaction omits: {required}")
    for required in ("retry", "response was lost", "LEDGER.CORRUPT",
                     "Concurrent semantically identical Attempts"):
        if required not in recovery:
            errors.append(f"recovery protocol omits: {required}")
    visibility = store.get("publicVisibility", "")
    if "forbid the candidate RunId before final commit" not in visibility or \
            "already committed RunId" not in visibility:
        errors.append("precommit/stored-view visibility boundary drifted")

    capability = contract.get("sealedCapabilityContract") or {}
    if "before Attempt/core" not in capability.get("targetTiming", "") or \
            "cannot be selected after observing verdict" not in capability.get("targetTiming", ""):
        errors.append("sealed capability timing drifted")
    if "does not silently demote" not in capability.get("finalization", ""):
        errors.append("sealed capability no-downgrade rule drifted")
    if "RT10 alone derives effectiveCapability" not in capability.get("readTime", ""):
        errors.append("read-time capability ownership drifted")
    if "CD-RT-5 alone decides" not in capability.get("productFork", ""):
        errors.append("CD-RT-5 product-authority boundary drifted")

    d9 = contract.get("d9Mapping") or {}
    if d9.get("finalTransactionFailure") != \
            "DURABILITY.COMMIT_FAILED (ExecutionId only; RunId forbidden)":
        errors.append("failed final commit D9 mapping exposes/drifts RunId")
    if d9.get("vocabularyRule") != \
            "No new D9 class, code, axis, precedence, or exit mapping is introduced.":
        errors.append("Evidence improperly extends D9 vocabulary")
    residuals = {x.get("id"): x for x in contract.get("retainedResiduals", [])
                 if isinstance(x, dict)}
    expected_residual_states = {"CD-RT-5": "UNRESOLVED",
                                "G19": "IMPLEMENTABLE_UNEXECUTED",
                                "RC-R-01": "IMPLEMENTABLE_UNEXECUTED",
                                "INDEPENDENT-REREVIEW": "REQUIRED"}
    if {key: (residuals.get(key) or {}).get("state") for key in expected_residual_states} \
            != expected_residual_states or len(residuals) != 4:
        errors.append("retained residual set/state drifted")
    if contract.get("sealRecommendation") != \
            "DO NOT SEAL OR APPLY. Candidate is implementation-ready at the contract level, but CD-RT-5, live-store evidence, independent combined rereview and coordinator integration remain outstanding.":
        errors.append("no-seal recommendation drifted")
    if {x.get("id") for x in contract.get("invariants", []) if isinstance(x, dict)} != \
            {f"EV4-{i}" for i in range(1, 11)}:
        errors.append("EV4 invariant set is not exact")
    if {x.get("id") for x in contract.get("positiveControls", []) if isinstance(x, dict)} != {
            "EVD4-POS-NOMATCH-PASS", "EVD4-POS-CORRELATION-STABILITY",
            "EVD4-POS-AVAILABILITY-DEGRADE", "EVD4-POS-CAPABILITY-CHANGE",
            "EVD4-POS-RECOVERY"}:
        errors.append("positive control set is not exact")
    return errors


def selftest(contract: dict[str, Any]) -> list[str]:
    mutations: list[tuple[str, Any]] = []

    def add(name: str, mutator: Any) -> None:
        mutations.append((name, mutator))

    add("version", lambda x: x.__setitem__("version", 3))
    add("status", lambda x: x.__setitem__("status", "ACCEPTED"))
    add("authority", lambda x: x["authority"].__setitem__("authorityClaim", "SIGNED"))
    add("finding-transfer", lambda x: x["reviewFindingTransfers"].pop())
    add("recursive-request-id", lambda x: x["recursiveRequestIdExclusion"]["surfaces"].pop())
    add("predecessor", lambda x: x["supersedes"].__setitem__("sha256", "0" * 64))
    add("ep-pin", lambda x: x["dependencies"]["evaluationProof"].__setitem__("sha256", "0" * 64))
    add("rt-pin", lambda x: x["dependencies"]["retentionCustody"].__setitem__("sha256", "0" * 64))
    add("versioning-pin", lambda x: x["dependencies"]["versioning"].__setitem__("sha256", "0" * 64))
    add("ep-checker-pin", lambda x: x["dependencies"]["evaluationProof"].__setitem__("checkerSha256", "0" * 64))
    add("authority-record", lambda x: x["importedAuthorityContract"]["record"].__setitem__("recordTag", "0xff"))
    add("binding-record", lambda x: x["importedAuthorityContract"]["semanticObjectBinding"]["fields"][0].__setitem__("tag", "0xff"))
    add("authority-golden", lambda x: x["importedAuthorityContract"]["recordGolden"].__setitem__("recordSha256", "sha256:" + "0" * 64))
    add("domain-record-tag", lambda x: x["canonicalWireGrammar"]["domainEnvelope"].__setitem__("recordTag", "0xff"))
    add("tag-registry", lambda x: x["canonicalWireGrammar"]["tagRegistry"].pop())
    add("semantic-field", lambda x: x["canonicalWireGrammar"]["records"]["SemanticEvidenceV1"]["fields"][0].__setitem__("tag", "0xff"))
    add("run-domain", lambda x: x["canonicalWireGrammar"]["records"]["RunIdentityPreimageV1"].__setitem__("domain", "wrong"))
    add("terminal-self-ref", lambda x: x["canonicalWireGrammar"]["records"]["TerminalRunV1"]["forbidden"].remove("runSealRef"))
    add("inventory-count", lambda x: x["acceptedGolden"].__setitem__("rawProofInventoryCount", 21))
    add("inventory-byte", lambda x: x["acceptedGolden"].__setitem__("rawProofInventoryEncodedHex", "00"))
    add("evidence-hash", lambda x: x["acceptedGolden"].__setitem__("evidenceDigest", "sha256:" + "0" * 64))
    add("run-hash", lambda x: x["acceptedGolden"].__setitem__("runId", "run1:" + "0" * 64))
    add("terminal-hash", lambda x: x["acceptedGolden"].__setitem__("runSealRef", "sha256:" + "0" * 64))
    add("run-substitution", lambda x: x["runSubstitutionGoldens"][0].__setitem__("expectedRunId", "run1:" + "0" * 64))
    add("api", lambda x: x["apiContract"]["calls"].pop())
    add("prepared-runid", lambda x: x["storeContract"]["records"]["RunFreePreparedCommitV1"]["forbidden"].remove("runId"))
    add("transaction", lambda x: x["storeContract"]["transaction"].pop())
    add("recovery", lambda x: x["storeContract"]["recovery"].pop())
    add("visibility", lambda x: x["storeContract"].__setitem__("publicVisibility", "candidate RunId may be logged"))
    add("cap-timing", lambda x: x["sealedCapabilityContract"].__setitem__("targetTiming", "after verdict"))
    add("cap-demotion", lambda x: x["sealedCapabilityContract"].__setitem__("finalization", "may demote"))
    add("d9-failure", lambda x: x["d9Mapping"].__setitem__("finalTransactionFailure", "DURABILITY.COMMIT_FAILED with RunId"))
    add("residual", lambda x: x["retainedResiduals"][0].__setitem__("state", "RESOLVED"))
    add("seal", lambda x: x.__setitem__("sealRecommendation", "SEAL"))
    failures: list[str] = []
    for name, mutator in mutations:
        candidate = copy.deepcopy(contract)
        mutator(candidate)
        if not check(candidate, verify_files=False):
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
        contract = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 2
    errors = check(contract)
    if not errors and do_selftest:
        errors.extend(selftest(contract))
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print(f"PASS: {path.name} Evidence v4 contract is internally and cross-artifact consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
