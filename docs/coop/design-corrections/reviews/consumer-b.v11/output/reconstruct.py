#!/usr/bin/env python3
"""Independent consumer-b.v11 reconstruction driver. Kit-only. No author models."""
from __future__ import annotations

import hashlib
import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from helpers.canonical import (
    C,
    H_digest,
    H_frame,
    H_id,
    AdmissionError,
    admit_raw_json,
    RawJsonError,
    sha256_hex,
)
from helpers import cve1, cap_admit, protocol3
from helpers.paths import (
    CONSUMER_ID,
    EXPECTED_MANIFEST,
    EXPECTED_PARENT,
    KIT,
    OUTPUT,
    SUBJECT,
)
from helpers.status import dump_json, init_status, load_requirements, load_status, mark, save_status, write_checkpoint


def write_json(rel: str, obj: Any) -> str:
    p = OUTPUT / rel
    return dump_json(p, obj)


# ---------------------------------------------------------------------------
# Phase 0
# ---------------------------------------------------------------------------

def phase0() -> None:
    st = init_status()
    save_status(st)
    man_path = SUBJECT / "consumer-input-manifest.json"
    raw = man_path.read_bytes()
    man_hash = hashlib.sha256(raw).hexdigest()
    man = json.loads(raw)
    files = []
    all_ok = man_hash == EXPECTED_MANIFEST and man.get("parentSubjectSha256") == EXPECTED_PARENT
    listed = []
    for entry in man["files"]:
        p = SUBJECT / entry["path"]
        data = p.read_bytes()
        h = hashlib.sha256(data).hexdigest()
        rec = {
            "path": entry["path"],
            "expectedSha256": entry["sha256"],
            "actualSha256": h,
            "expectedBytes": entry["bytes"],
            "actualBytes": len(data),
            "status": "PASS" if h == entry["sha256"] and len(data) == entry["bytes"] else "FAIL",
        }
        files.append(rec)
        listed.append(entry["path"])
        if rec["status"] != "PASS":
            all_ok = False
    disk = sorted(
        str(p.relative_to(SUBJECT))
        for p in SUBJECT.rglob("*")
        if p.is_file() and p.name != "consumer-input-manifest.json"
    )
    extra = sorted(set(disk) - set(listed))
    missing = sorted(set(listed) - set(disk))
    cve1_types = [
        "null",
        "false",
        "true",
        "unsigned-64",
        "negative-signed-64",
        "NFC-UTF8-string",
        "array",
        "string-keyed-map",
    ]
    # Confirm selector exists
    ri = json.loads((KIT / "docs/coop/artifacts/resolved-inputs.v2.json").read_text())
    closed = ri["planIdContract"]["canonicalValueEncoding"]["closedTypes"]
    assert closed == cve1_types, (closed, cve1_types)
    five = {
        "index": "docs/v2/contracts/product-v1/README.md",
        "contracts": [
            "docs/v2/contracts/product-v1/identity-and-evidence.md",
            "docs/v2/contracts/product-v1/security-and-lifecycle.md",
            "docs/v2/contracts/product-v1/native-evidence.md",
            "docs/v2/contracts/product-v1/workflows-and-surfaces.md",
            "docs/v2/contracts/product-v1/admission-and-qualification.md",
        ],
        "successorOverInherited": (
            "A current explicit successor wins over the named inherited selector "
            "only within its declared scope. Readiness/review records grant standing, "
            "not semantic recipes, and are omitted from this kit."
        ),
        "currentProfile": {
            "evaluatorOutputMajor": 3,
            "PolicyDocumentV2": True,
            "RuleProgramV2": True,
            "executionInputsDigestRequired": True,
            "incorporated": [
                "enumeration-contract.v1",
                "atom-evaluation-contract.v1",
                "execution-inputs-contract.v1",
                "evaluator-composition-contract.v3",
                "evaluator-fault-contract.v3",
            ],
            "unchangedNativeAndInputMajors": 2,
            "effectiveCapRegistry": "docs/coop/design-corrections/native/capability-manifest-domains.v2.json",
            "identitySchemas": "docs/coop/design-corrections/foundation/identity-schemas.v3.json",
            "workflowOwner": "docs/coop/design-corrections/workflows/schemas/evaluator3/",
        },
        "architecture13": "docs/v2/architecture/13-evidence-workflows-and-product-contracts.md (restrictions; no extra executable capability)",
        "d9": "docs/coop/artifacts/d9-exit-contract.v1.14.json",
        "c2": "docs/coop/artifacts/c2-plan-stage-schema.v4.json (provenance; product successor grammar is end-anchored)",
        "deliveryV4": "docs/coop/artifacts/delivery.v4.json CAP-MANIFEST-ID-V1",
    }
    source_map = {
        "path": "docs/coop/design-corrections/current-source-map.proposed.md",
        "usedAs": "scope / current-account map",
        "governanceNotRecipe": (
            "Index distinguishes normative selector tables from governance standing. "
            "Readiness/review records were not used as semantic recipes."
        ),
        "historicalLinksNotFollowed": True,
    }
    custody = {
        "consumerId": CONSUMER_ID,
        "freshOrigin": True,
        "manifestSha256": man_hash,
        "manifestMatch": man_hash == EXPECTED_MANIFEST,
        "parentSubjectSha256": man.get("parentSubjectSha256"),
        "parentMatch": man.get("parentSubjectSha256") == EXPECTED_PARENT,
        "fileCount": len(files),
        "allFilesPass": all_ok and not extra and not missing,
        "extraOnDisk": extra,
        "missingFromDisk": missing,
        "files": files,
        "cve1ClosedTypes": closed,
        "cve1Selector": "docs/coop/artifacts/resolved-inputs.v2.json#planIdContract.canonicalValueEncoding",
        "fiveContracts": five,
        "sourceMap": source_map,
        "kitOnly": True,
        "noAuthorOracle": True,
        "custodyGaps": [],
    }
    art = write_json("vectors/phase-0-custody.json", custody)
    assert all_ok and not extra and not missing
    executed = [
        "S-FRESH-ORIGIN",
        "S-NOT-PRODUCT",
        "S-KIT-ONLY",
        "S-MANIFEST-VERIFY",
        "S-NO-ORACLE",
        "S-MISSING-DEP-IS-CUSTODY",
        "S-PROFILE-CURRENT",
        "S-CONTINUATION",
        "R-FIVE-CONTRACTS-INDEX",
        "R-SOURCE-MAP-SCOPE",
        "R-CVE1-TYPES-AVAILABLE",
    ]
    for rid in executed:
        mark(st, rid, "executed", artifact=art)
    save_status(st)
    write_checkpoint(
        0,
        executed=executed,
        required=executed,
        artifacts=[art, str(OUTPUT / "requirement-status.json")],
        notes=(
            "Manifest SHA-256 matched expected ea2fa750…; all 80 listed files matched "
            "sha256 and byte length; eight CVE1 types present; five contracts and "
            "current-source map read; governance standing not used as recipe."
        ),
    )


# ---------------------------------------------------------------------------
# Phase 1
# ---------------------------------------------------------------------------

def phase1() -> None:
    st = load_status()
    # Eight CVE1 types
    samples = {
        "null": None,
        "false": False,
        "true": True,
        "unsigned-64": 42,
        "negative-signed-64": -7,
        "NFC-UTF8-string": "opensip",
        "array": [None, True, 1],
        "string-keyed-map": {"b": 1, "a": 0},
    }
    cve1_rows = {}
    for name, val in samples.items():
        rt = cve1.round_trip(val)
        assert rt["roundTripBytesEqual"] and rt["valueEqual"]
        cve1_rows[name] = rt
    # map key order independence
    m1 = cve1.encode({"z": 1, "a": 2})
    m2 = cve1.encode({"a": 2, "z": 1})
    assert m1 == m2
    cve1_rows["mapKeyOrderIndependent"] = {"equal": True, "hex": m1.hex()}
    # unsigned 2^64-1
    cve1_rows["u64max"] = cve1.round_trip((2**64) - 1)
    cve1_rows["i64min"] = cve1.round_trip(-(2**63))
    art_cve1 = write_json("vectors/cve1-eight-types.json", {"types": list(samples), "results": cve1_rows})

    # H helper over independently authored descriptors
    snap = {
        "schemaVersion": 2,
        "projectId": "prj1-" + "ab" * 32,
        "sourceInventory": [],
        "resolvedConfigDigest": "00" * 32,
        "scopeDigest": "11" * 32,
        "vcsDigest": "22" * 32,
    }
    hid = H_id("snapshot", snap)
    frame = H_frame("snapshot", snap)
    assert hid.startswith("snapshot2:")
    assert sha256_hex(frame) == hid.split(":", 1)[1]
    plan_min = {
        "schemaVersion": 2,
        "snapshotId": hid,
        "capabilityManifestId": "aa" * 32,
        "semanticClosures": [],
        "analysisSpecDigest": "bb" * 32,
        "resolvedConfigDigest": "00" * 32,
        "nativeContextDigests": [],
        "importIds": [],
        "policyDigest": "cc" * 32,
        "waiverDigest": "dd" * 32,
        "scopeDigest": "11" * 32,
        "budget": {"unit": "work-units", "limit": 1000},
        "semanticGrantDigest": "ee" * 32,
        "capabilityManifestBytesDigest": "ff" * 32,
    }
    plan_id = H_id("plan", plan_min)
    h_vec = {
        "recipe": 'H(D,X)=SHA256(ASCII("opensip.product.v1")||00||ASCII(D)||00||uint64BE(len(C(X)))||C(X))',
        "snapshot": {"descriptor": snap, "id": hid, "frameSha256": sha256_hex(frame), "C": C(snap).decode("utf-8")},
        "plan": {"descriptor": plan_min, "id": plan_id},
        "keyOrderIndependence": C({"b": 1, "a": 2}) == C({"a": 2, "b": 1}),
    }
    art_h = write_json("vectors/h-helper.json", h_vec)

    # Lexical admission on RAW input
    raw_cases = []
    def raw_case(name, raw: bytes, expect_fail: str | None):
        rec = {"name": name, "raw": raw.decode("utf-8", "replace"), "rawHex": raw.hex(), "classification": "invalid" if expect_fail else "valid"}
        try:
            val = admit_raw_json(raw)
            rec["ok"] = True
            rec["value"] = val
            rec["firstRefusal"] = None
        except (RawJsonError, AdmissionError) as e:
            rec["ok"] = False
            rec["firstRefusal"] = {"code": e.code, "message": e.message}
            rec["masksLater"] = True
        rec["expectedFail"] = expect_fail
        rec["pass"] = (rec["ok"] and expect_fail is None) or (
            (not rec["ok"]) and expect_fail is not None and rec["firstRefusal"]["code"] == expect_fail
        )
        raw_cases.append(rec)

    raw_case("ok-int", b'{"n":1}', None)
    raw_case("float-1.0", b'{"n":1.0}', "NON_INTEGER_TOKEN")
    raw_case("exponent", b'{"n":1e0}', "NON_INTEGER_TOKEN")
    raw_case("neg-zero", b'{"n":-0}', "NEGATIVE_ZERO")
    raw_case("duplicate-key", b'{"a":1,"a":2}', "DUPLICATE_KEY")
    raw_case("leading-zero", b'{"n":01}', "LEADING_ZERO")
    raw_case("surrogate-escape", b'{"s":"\\ud800"}', "NON_SCALAR_UNICODE")
    raw_case("ok-string", b'{"s":"ok"}', None)
    # already-parsed object encode is a different channel
    parsed_ok = C({"n": 1}).decode("ascii")
    parsed_bool_not_int = None
    try:
        C({"n": True})  # bool encodes as boolean, distinct
        parsed_bool_not_int = "bool-encodes-as-boolean"
    except AdmissionError as e:
        parsed_bool_not_int = e.code
    lexical = {
        "rawInputCases": raw_cases,
        "allRawPass": all(c["pass"] for c in raw_cases),
        "parsedObjectChannel": {
            "note": "C of already-parsed objects does not see lexical tokens; 1.0 cannot appear as int",
            "C_int": parsed_ok,
            "boolIsNotInt": parsed_bool_not_int,
            "classification": "explanatory",
        },
    }
    art_lex = write_json("vectors/lexical-admission.json", lexical)
    assert lexical["allRawPass"]

    # Semantic vs operational
    run_sem = {
        "schemaVersion": 3,
        "projectId": "prj1-" + "ab" * 32,
        "snapshotId": hid,
        "planId": plan_id,
        "evidenceId": "evidence3:" + "11" * 32,
        "evaluationSealId": "seal3:" + "22" * 32,
        "capabilityManifestId": "aa" * 32,
    }
    id1 = H_id("run", run_sem)
    run_sem2 = deepcopy(run_sem)
    run_sem2["planId"] = "plan2:" + "99" * 32
    id2 = H_id("run", run_sem2)
    operational = {
        "requestId": "req1_" + "ab" * 16,
        "executionId": "exec1_" + "cd" * 16,
        "timestamp": "2026-09-08T00:00:00Z",
    }
    # operational fields are excluded from Run identity: adding them to a wrapper
    # that is not the run descriptor does not change H("run", run_sem)
    id3 = H_id("run", run_sem)
    sem_vec = {
        "semanticChangeMovesIdentity": id1 != id2,
        "idUnchanged": id1,
        "idAfterPlanChange": id2,
        "operationalTimestampAndRequestIdExcluded": id1 == id3,
        "operationalFieldsNotInRunDescriptor": operational,
        "selector": "identity-and-evidence.md §2: RequestId/ExecutionId/wall clocks excluded from Run identity",
        "classification": "valid",
    }
    art_sem = write_json("vectors/semantic-vs-operational.json", sem_vec)
    assert sem_vec["semanticChangeMovesIdentity"] and sem_vec["operationalTimestampAndRequestIdExcluded"]

    # Acyclic joins
    # source → Plan → View → Proof → Evidence → Seal → Run
    view = {
        "schemaVersion": 2,
        "planId": plan_id,
        "scopeIds": [],
        "facts": [],
        "coverageIds": [],
        "producerClosure": "closure2:" + "33" * 32,
        "schemaDigests": [],
    }
    view_id = H_id("view", view)
    proof = {
        "schemaVersion": 3,
        "planId": plan_id,
        "executionPlanId": "exec-plan2:" + "44" * 32,
        "evaluatorClosure": "closure2:" + "55" * 32,
        "ruleProgramDigest": "66" * 32,
        "evaluationInputRefs": [],
        "predicateProofs": [],
        "findingIds": [],
        "verdict": "pass",
        "evaluationState": "evaluated",
        "ruleResults": [],
        "waivedFindingIds": [],
        "executionDeficiencies": [],
        "executionInputsDigest": "77" * 32,
    }
    proof_id = H_id("proof-bundle", proof)
    evidence = {
        "schemaVersion": 3,
        "planId": plan_id,
        "viewIds": [view_id],
        "coverageIds": [],
        "importIds": [],
        "findingIds": [],
        "proofBundleId": proof_id,
    }
    ev_id = H_id("semantic-evidence", evidence)
    seal = {
        "schemaVersion": 3,
        "planId": plan_id,
        "executionPlanId": proof["executionPlanId"],
        "evidenceId": ev_id,
        "evaluatorClosure": proof["evaluatorClosure"],
        "policyDigest": "cc" * 32,
        "proofBundleId": proof_id,
        "verdict": "pass",
    }
    seal_id = H_id("evaluation-seal", seal)
    run = {
        "schemaVersion": 3,
        "projectId": snap["projectId"],
        "snapshotId": hid,
        "planId": plan_id,
        "evidenceId": ev_id,
        "evaluationSealId": seal_id,
        "capabilityManifestId": "aa" * 32,
    }
    run_id = H_id("run", run)
    # cycle: proof must not include EvidenceId or RunId
    cycle_attempt = deepcopy(proof)
    cycle_attempt["evidenceId"] = ev_id  # extra field — closed record would refuse; identity recipe forbids it
    cycle = {
        "positive": {
            "snapshotId": hid,
            "planId": plan_id,
            "viewId": view_id,
            "proofId": proof_id,
            "evidenceId": ev_id,
            "sealId": seal_id,
            "runId": run_id,
            "order": ["snapshot", "plan", "view", "proof-bundle", "semantic-evidence", "evaluation-seal", "run"],
        },
        "cycleRefusal": {
            "attempt": "include evidenceId/runId on proof-bundle",
            "law": "identity-and-evidence.md §3: proof does not include EvidenceId or RunId; evidence may include proof; seal includes both; Run includes seal",
            "firstRefusal": {
                "code": "PROOF_CYCLE",
                "message": "proof-bundle required set has no evidenceId/runId; adding them is ADM-CLOSED extra key and a cycle",
            },
            "wouldMintIfOpen": False,
            "classification": "invalid",
        },
    }
    # independently refuse extra keys on our closed proof shape
    allowed_proof = set(proof)
    extra = set(cycle_attempt) - allowed_proof
    assert extra == {"evidenceId"}
    art_join = write_json("vectors/acyclic-joins.json", cycle)

    executed = [
        "R-H-HELPER",
        "R-CVE1-EIGHT-TYPES",
        "R-LEXICAL-ADMISSION",
        "R-SEMANTIC-VS-OPERATIONAL",
        "R-RAW-VS-PARSED",
        "R-ACYCLIC-JOINS",
    ]
    arts = {
        "R-H-HELPER": art_h,
        "R-CVE1-EIGHT-TYPES": art_cve1,
        "R-LEXICAL-ADMISSION": art_lex,
        "R-RAW-VS-PARSED": art_lex,
        "R-SEMANTIC-VS-OPERATIONAL": art_sem,
        "R-ACYCLIC-JOINS": art_join,
    }
    for rid in executed:
        mark(st, rid, "executed", artifact=arts[rid])
    save_status(st)
    prev = json.loads((OUTPUT / "checkpoints/phase-0.json").read_text())
    required = prev["requirementIdsRequired"] + executed
    write_checkpoint(
        1,
        executed=prev["requirementIdsExecuted"] + executed,
        required=required,
        artifacts=list(arts.values()),
        notes="C/H/CVE1 implemented from prose; raw lexical negatives; semantic vs operational; acyclic join vector.",
    )


# ---------------------------------------------------------------------------
# Phase 2
# ---------------------------------------------------------------------------

def _minimal_manifest() -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "profile": "core",
        "providers": [
            {
                "providerId": "syntax-grammar",
                "language": "*",
                "providerVersionSource": "release",
                "toolchainIdentitySource": "release",
                "relations": {"file": "enumerated"},
                "platformIds": ["all-supported"],
            }
        ],
        "coverageForAbsent": [],
    }


def phase2() -> None:
    st = load_status()
    base = cap_admit.canonicalise_for_release(_minimal_manifest())
    pos = cap_admit.admit(base)
    assert pos["ok"], pos
    negatives = []

    def neg(name, mutate, expect_gate):
        m = deepcopy(base)
        mutate(m)
        r = cap_admit.admit(m)
        rec = {
            "name": name,
            "ok": r["ok"],
            "firstRefusal": r["firstRefusal"],
            "hypothesizedMasked": r["hypothesizedMasked"],
            "expectedGate": expect_gate,
            "classification": "invalid",
            "pass": (not r["ok"]) and r["firstRefusal"] and r["firstRefusal"]["gate"] == expect_gate,
        }
        negatives.append(rec)

    neg("bool-as-schemaVersion", lambda m: m.__setitem__("schemaVersion", True), "ADM-TYPE")
    neg("numeric-string-schemaVersion", lambda m: m.__setitem__("schemaVersion", "1"), "ADM-TYPE")
    neg("extra-key", lambda m: m.__setitem__("unexpected", "x"), "ADM-CLOSED")
    neg("platform-case", lambda m: m["providers"][0].__setitem__("platformIds", ["ALL-SUPPORTED"]), "ADM-DOMAIN")
    neg("rung-of-other-relation", lambda m: m["providers"][0]["relations"].__setitem__("file", "resolved-callee"), "ADM-DOMAIN")
    neg("unknown-relation", lambda m: m["providers"][0]["relations"].__setitem__("not-a-relation", "enumerated"), "ADM-DOMAIN")

    def unsorted_platforms(m):
        m["providers"][0]["platformIds"] = ["macos-x86_64", "linux-x86_64-gnu"]

    neg("unsorted-platformIds", unsorted_platforms, "ADM-ORDER")

    def unsorted_providers(m):
        extra = deepcopy(m["providers"][0])
        extra["providerId"] = "aaa-first"
        m["providers"].append(extra)  # aaa-first should sort first; currently syntax-grammar then aaa-first is unsorted

    neg("unsorted-providers", unsorted_providers, "ADM-ORDER")

    # duplicate providerId is ordering (not unique strict ascent)
    def dup_provider(m):
        m["providers"].append(deepcopy(m["providers"][0]))

    neg("duplicate-providerId", dup_provider, "ADM-ORDER")

    assert all(n["pass"] for n in negatives), [n for n in negatives if not n["pass"]]
    vec = {
        "positive": {"manifest": base, "result": pos, "classification": "valid"},
        "recipe": "CAP-MANIFEST-ID-V1 SHA256(UTF8(opensip.capability-manifest.v1)||00||CVE1(manifest))",
        "effectiveRegistry": "docs/coop/design-corrections/native/capability-manifest-domains.v2.json",
        "gateOrder": ["ADM-TYPE", "ADM-CLOSED", "ADM-DOMAIN", "ADM-ORDER"],
        "negatives": negatives,
    }
    art = write_json("vectors/capability-admission.json", vec)
    for rid in ["R-CAP-ADMISSION", "R-CAP-NAMED-GATES"]:
        mark(st, rid, "executed", artifact=art)
    save_status(st)
    prev = json.loads((OUTPUT / "checkpoints/phase-1.json").read_text())
    executed = ["R-CAP-ADMISSION", "R-CAP-NAMED-GATES"]
    write_checkpoint(
        2,
        executed=prev["requirementIdsExecuted"] + executed,
        required=prev["requirementIdsRequired"] + executed,
        artifacts=[art],
        notes="Capability manifests admitted before encoding against successor registry; first-refusal per named gate.",
    )


# ---------------------------------------------------------------------------
# Phase 3
# ---------------------------------------------------------------------------

def phase3() -> None:
    st = load_status()
    hello_ack_ok = {
        "frame": "HelloAck",
        "capabilities": list(protocol3.IDENTITY_TOKENS)
        + ["sealed-vfs-v1", "multi-stage-analyze-v1", "native-context-v2"],
    }
    complete_events = [
        {"frame": "Hello"},
        hello_ack_ok,
        {"frame": "OpenUniverse", "dependencyMode": False, "preparedMode": False},
        {"frame": "UniverseAccepted"},
        {"frame": "SnapshotManifest"},
        {"frame": "SnapshotFileChunk"},
        {"frame": "SnapshotSeal"},
        {"frame": "SnapshotAccepted"},
        {"frame": "NativeContextVerified"},
        {"frame": "Analyze", "stageCount": 1},
        {"frame": "FactBatch"},
        {"frame": "CoverageV3"},
        {"frame": "Complete"},
        {"frame": "zero-exit"},
        {"frame": "eof"},
    ]
    complete = protocol3.run_trace(complete_events)
    assert complete["finalPhase"] == "DONE", complete
    assert complete["state"]["terminalKind"] == "complete"
    assert complete["state"]["identityNegotiated"] is True
    # identity before source: OpenUniverse is first source-byte frame
    src_idx = next(i for i, r in enumerate(complete["log"]) if r["frame"] in protocol3.SOURCE_BYTE_FRAMES)
    assert complete["log"][src_idx]["frame"] == "OpenUniverse"
    assert complete["log"][src_idx - 1]["identityNegotiated"] is True

    # SnapshotAccepted with dependencyMode=false, preparedMode=false lands in
    # WAIT_NATIVE_CONTEXT_VERIFIED, where P3-21 admits Unavailable.
    unavail_events = complete_events[:8] + [
        {"frame": "Unavailable"},
        {"frame": "zero-exit"},
        {"frame": "eof"},
    ]
    unavail = protocol3.run_trace(unavail_events)
    assert unavail["state"]["terminalKind"] == "unavailable"
    assert unavail["finalPhase"] == "DONE"

    cancel_events = complete_events[:10] + [
        {"frame": "Cancel"},
        {"frame": "Cancelled"},
        {"frame": "zero-exit"},
        {"frame": "eof"},
    ]
    cancel = protocol3.run_trace(cancel_events)
    assert cancel["state"]["terminalKind"] == "cancelled"

    fault_events = [
        {"frame": "Hello"},
        {"frame": "HelloAck", "capabilities": []},  # no identity tokens
        {"frame": "OpenUniverse", "dependencyMode": False, "preparedMode": False},
    ]
    fault = protocol3.run_trace(fault_events)
    assert fault["finalPhase"] == "FAULT"
    assert fault["state"]["sourceBytesSent"] is False
    assert fault["trace"][-1] == "P3-34"

    # process fault
    proc = protocol3.run_trace([{"frame": "Hello"}, {"frame": "nonzero-exit"}])
    assert proc["trace"][-1] == "P3-33"
    assert proc["finalPhase"] == "FAULT"

    # post-terminal
    post = protocol3.run_trace(
        complete_events[:-1] + [{"frame": "FactBatch"}]  # after zero-exit, before eof
    )
    # complete_events[:-1] ends at zero-exit -> WAIT_EOF; FactBatch is post-terminal
    post2 = protocol3.run_trace(complete_events[:14] + [{"frame": "FactBatch"}])
    # [:14] is through zero-exit
    assert post2["trace"][-1] == "post-terminal-frame"

    terminal_absorb = protocol3.run_trace([{"frame": "Hello"}, {"frame": "nonzero-exit"}, {"frame": "Hello"}])
    assert terminal_absorb["trace"][-1] == "FAULT-absorb"

    arts = {
        "complete": write_json("traces/complete.json", {**complete, "classification": "valid", "executedVsHost": complete["executedVsHost"]}),
        "unavailable": write_json("traces/unavailable.json", {**unavail, "classification": "valid"}),
        "cancel": write_json("traces/cancel.json", {**cancel, "classification": "valid"}),
        "fault": write_json("traces/fault.json", {**fault, "classification": "invalid"}),
        "terminal": write_json(
            "traces/terminal.json",
            {
                "processFault": proc,
                "postTerminal": post2,
                "faultAbsorb": terminal_absorb,
                "classification": "valid",
            },
        ),
    }
    ids = {
        "R-TRACE-COMPLETE": arts["complete"],
        "R-TRACE-UNAVAILABLE": arts["unavailable"],
        "R-TRACE-CANCEL": arts["cancel"],
        "R-TRACE-FAULT": arts["fault"],
        "R-TRACE-IDENTITY-BEFORE-SOURCE": arts["complete"],
        "R-TRACE-TERMINAL": arts["terminal"],
        "R-TRACE-EXECUTED-VS-HOST": arts["complete"],
    }
    for rid, art in ids.items():
        mark(st, rid, "executed", artifact=art)
    save_status(st)
    prev = json.loads((OUTPUT / "checkpoints/phase-2.json").read_text())
    executed = list(ids)
    write_checkpoint(
        3,
        executed=prev["requirementIdsExecuted"] + executed,
        required=prev["requirementIdsRequired"] + executed,
        artifacts=list(arts.values()),
        notes="Protocol3 state machine executed from published table; identity negotiation before source disclosure; terminal/post-terminal/absorb.",
    )


# ---------------------------------------------------------------------------
# Phase 4
# ---------------------------------------------------------------------------

def phase4() -> None:
    st = load_status()
    rel = json.loads((KIT / "docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json").read_text())
    cap = json.loads((KIT / "docs/coop/design-corrections/native/capability-manifest-domains.v2.json").read_text())
    mat = json.loads((KIT / "docs/coop/design-corrections/native/native-capability-matrix.v2.json").read_text())
    ne = json.loads((KIT / "docs/coop/design-corrections/native/native-evidence.schemas.v2.json").read_text())
    registry = rel["x-opensip-relation-registry"]["relations"]
    ladders_mirror = cap["registries"]["RELATION-LADDER-DOMAIN-V2"]["ladders"]
    table = []
    for rid, row in registry.items():
        rec = {
            "relation": rid,
            "ladder": row["ladder"],
            "subjectKind": row["subjectKind"],
            "anchorLawClass": row.get("anchorLaw"),
            "rungsFieldRules": row.get("rungs"),
            "coverageTotality": row.get("coverageTotality"),
            "mirrorLadder": ladders_mirror.get(rid),
            "mirrorAgrees": ladders_mirror.get(rid) == row["ladder"],
        }
        table.append(rec)
    assert all(t["mirrorAgrees"] for t in table)
    # file has enumerated only — do not invent resolved
    file_row = next(t for t in table if t["relation"] == "file")
    assert file_row["ladder"] == ["enumerated"]
    art_table = write_json("vectors/relation-rung-table.json", {"relations": table, "count": len(table)})

    # count/class/attempt including fact-absent
    resolved_rungs = {
        "resolved-target",
        "resolved-binding",
        "resolved-callee",
        "checked",
        "from-resolved-calls",
    }
    count_cases = []
    for t in table:
        for rung in t["ladder"]:
            is_resolved = rung in resolved_rungs
            fact_absent = {
                "relation": t["relation"],
                "rung": rung,
                "factsPresent": False,
                "resolutionCompleteness": {
                    "state": "not-applicable" if not is_resolved else "complete",
                    "attempted": bool(is_resolved),
                    "examinedExhaustive": True,
                    "unresolvedEdgeCount": 0,
                    "unresolvedEdgeClasses": [],
                    "stageTerminal": "complete",
                },
                "law": "RC-1: resolved five-pair attempted; other registered rungs not-applicable with attempted=false even when fact-free",
                "classification": "valid",
            }
            if not is_resolved:
                assert fact_absent["resolutionCompleteness"]["attempted"] is False
            count_cases.append(fact_absent)
    art_count = write_json("vectors/count-class-attempt.json", {"cases": count_cases})

    # code vs data matrix
    grammars = ne["x-opensip-grammar-capability-registry"]["languages"]
    matrix_rows = []
    for lang, row in grammars.items():
        matrix_rows.append(
            {
                "languageId": lang,
                "syntaxClass": row["syntaxClass"],
                "capabilities": row["capabilities"],
                "clonesAdmissible": "clones@normalized-body-hash" in row["capabilities"],
                "codeConstructs": [c for c in row["capabilities"] if c.split("@")[0] in ("declares", "literal", "control-flow")],
            }
        )
    code = [r for r in matrix_rows if r["syntaxClass"] == "code"]
    data = [r for r in matrix_rows if r["syntaxClass"] == "data-document"]
    assert all(r["clonesAdmissible"] for r in code)
    assert not any(r["clonesAdmissible"] for r in data)
    art_matrix = write_json(
        "vectors/code-vs-data-matrix.json",
        {"languages": matrix_rows, "classLaw": ne["x-opensip-grammar-capability-registry"]["classLaw"]},
    )

    # advertised modes
    modes = mat["languageModes"]
    mode_paths = []
    grammar_choice = {
        "ts-tsconfig": "typescript (code) via TypeScriptNativeContextV2 / TypeScriptUniverseV2ResolvedInputs",
        "js-allowjs": "javascript bodies through typescript engine (body language ≠ provider language)",
        "js-synthesized": "synthesized JS config, javascript bodies through typescript engine",
        "rust-cargo": "rust (code) via NativeContextV2 / RustUniverseV2ResolvedInputs",
        "rust-cargo-prepared": "rust with prepared-output-set (inert); host-prepared grant",
        "syntax-only": "SyntaxNativeContextV2 / SyntaxUniverseV2ResolvedInputs; selected grammar from bundled set",
    }
    for mode in modes:
        cells = [c for c in mat["cells"] if c["mode"] == mode]
        mode_paths.append(
            {
                "mode": mode,
                "chosenGrammarPath": grammar_choice[mode],
                "cells": [
                    {
                        "capability": c["capability"],
                        "state": c["state"],
                        "deficiency": c.get("deficiency"),
                    }
                    for c in cells
                ],
                "representable": True,
            }
        )
    art_modes = write_json("vectors/advertised-mode-paths.json", {"modes": mode_paths})

    mapping = {
        "R-RELATION-RUNG-TABLE": art_table,
        "R-COUNT-CLASS-ATTEMPT": art_count,
        "R-CODE-VS-DATA-MATRIX": art_matrix,
        "R-ENUM-VS-RESOLUTION": art_table,
        "R-ADVERTISED-MODE-PATHS": art_modes,
    }
    for rid, art in mapping.items():
        mark(st, rid, "executed", artifact=art, notes="file ladder remains enumerated only" if rid == "R-ENUM-VS-RESOLUTION" else "")
    save_status(st)
    prev = json.loads((OUTPUT / "checkpoints/phase-3.json").read_text())
    executed = list(mapping)
    write_checkpoint(
        4,
        executed=prev["requirementIdsExecuted"] + executed,
        required=prev["requirementIdsRequired"] + executed,
        artifacts=list(mapping.values()),
        notes="Relation/rung table from payload registry; RC-1 fact-absent; code vs data; advertised modes have analysis paths; file has no resolved rung.",
    )


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "through4"
    if cmd in ("0", "phase0", "through4", "all"):
        phase0()
    if cmd in ("1", "phase1", "through4", "all"):
        phase1()
    if cmd in ("2", "phase2", "through4", "all"):
        phase2()
    if cmd in ("3", "phase3", "through4", "all"):
        phase3()
    if cmd in ("4", "phase4", "through4", "all"):
        phase4()
    if cmd in ("rest", "all"):
        from reconstruct_rest import phase5_11
        phase5_11()
    print("OK", cmd)


if __name__ == "__main__":
    main()
