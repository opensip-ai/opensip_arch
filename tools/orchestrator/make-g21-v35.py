#!/usr/bin/env python3
"""Build g21-fixture-corpus.v35 landing v34 Stage A dual REJECT."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "docs/coop/artifacts"
V34 = ART / "g21-fixture-corpus.v34.json"
PAYLOAD_DIR = ART / "fixtures/g21.v27"
PAYLOAD = PAYLOAD_DIR / "G21.cc5.prefix-exactly-at-prehandshake.bin"
SUBJECT = ART / "g21-fixture-corpus.v35.json"
HEAD = "5a45ebf259a2f3094b18add549185223b0a80625"
PAYLOAD_SHA = "bf5e8ffa51a9e748985800c1d3d7f1a2a6ae7435136593ca8d9637e3f87c699c"


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def speak(s: str) -> str:
    """Rename this-cycle speaker only. Do not touch leftover-join.v34 of G21."""
    return s.replace("g21-fixture-corpus.v34", "g21-fixture-corpus.v35")


def speak_obj(o):
    if isinstance(o, str):
        return speak(o)
    if isinstance(o, list):
        return [speak_obj(x) for x in o]
    if isinstance(o, dict):
        return {k: speak_obj(v) for k, v in o.items()}
    return o


def main() -> None:
    obj = json.loads(V34.read_text())
    obj = speak_obj(obj)
    obj["artifact"] = "g21-fixture-corpus.v35"
    obj["version"] = 35
    obj["date"] = "2026-09-01"

    PAYLOAD_DIR.mkdir(parents=True, exist_ok=True)
    payload = (65536).to_bytes(4, "big")
    if PAYLOAD.exists():
        os.chmod(PAYLOAD, 0o644)
    PAYLOAD.write_bytes(payload)
    os.chmod(PAYLOAD, 0o444)
    assert sha256_file(PAYLOAD) == PAYLOAD_SHA

    obj["registerRowNote"] = (
        "registerRow is the already-named gate DR-G21 because g21-fixture-corpus.v35 authors leftover-design of the prefix integer of one remaining CC-5 injection of the live G21 INPUT-corpus class G21.cc.CC-5: prefix exactly at the preHandshake bound, quoting the recorded preHandshake bound 65536 as the 4-byte big-endian unsigned length N with no body, the direct analogue of G21.cc5.prefix-one-over-prehandshake and G21.cc5.length-prefix-0 sanctioned at DECISION-PACKETS/D1-plan/G21.md axis E item 27. Delivery of 65536 body bytes is not authored. The observable refusal route for these bytes is not pinned. file08StatusToken is DR-G21's own live token (OPEN). Occupancy v4 registerRow is DR-114 because G21 is that row's containment gate; g21-fixture-corpus.v35 does not retarget DR-114 leftover. leftover-join.v45 of G21 (D-359) leftoverDesign remains [OBL-G21-FX-AUTHORING]. leftover-design of the D-356 invalid-UTF-8 injection and of the four D-358 copies is stale as an authoring claim. Prefix exactly at the postHandshake bound remains unauthored. N=65536 is not pinned as prefix-only RF-2 because the quoted preHandshake clause and CC-5 intent disagree about N=65536. leftover-join.v14 of sarif remains the current recorded DR-122 leftover remasurement (D-347). g21-fixture-corpus.v35 does not remasure leftover-join.v45 of G21, does not remasure leftover-join.v14 of sarif, does not remasure g21-fixture-corpus.v33, does not remasure g21-fixture-corpus.v31, does not remasure g21-fixture-corpus.v30, does not remasure g21-fixture-corpus.v26, does not steal DR-114 leftover, does not reopen DR-102 SATISFIED, and does not SATISFY DR-114, DR-133, or DR-117. Frozen g21-fixture-corpus.v34 stays unmoved. Frozen g21-fixture-corpus.v9 stays unmoved. Frozen g21-fixture-corpus.v10 stays unmoved. Frozen g21-fixture-corpus.v33 stays unmoved. Frozen fixtures/g21.v26/ stays unmoved. Frozen fixtures/g21.v25/ stays unmoved. Frozen fixtures/g21.v24/ stays unmoved. Frozen fixtures/g21.v23/ stays unmoved. Frozen fixtures/g21.v22/ stays unmoved. Frozen fixtures/g21.v9/ stays unmoved."
    )
    obj["authorityClaim"] = (
        "g21-fixture-corpus.v35 PROPOSES leftover-design of the prefix integer of one remaining CC-5 injection against already-closed control-protocol-contract.v2 CC-5 intent: G21.cc5.prefix-exactly-at-prehandshake. Prefix exactly at the preHandshake bound is witnessed by the closed 4-byte big-endian unsigned 65536 with no body, quoting control-protocol-contract.v2 transportAndFraming.framing.bounds.preHandshake. 65536 is quoted, not invented. A 4-byte big-endian N=65536 payload is the direct analogue of G21.cc5.prefix-one-over-prehandshake (N=65537, hex 00010001) and G21.cc5.length-prefix-0 (N=0, hex 00000000), sanctioned at DECISION-PACKETS/D1-plan/G21.md axis E item 27. Hex 00010000 is not hex 00010001 and is not hex 01000000. The quoted preHandshake clause refuses N greater than 65536 or N equal to 0 from the prefix alone; N=65536 is not that refusal. Occupancy EV-5 oversize-from-prefix does not apply. N=65536 is in-bound against the quoted preHandshake clause. The receiver must read the body. Body length 0 is less than claimed N=65536. g21-fixture-corpus.v35 does not assert the truncated-body class of G21.cc5.truncated-body and does not deny the recorded truncated-body predicate. The observable refusal route for these bytes is not pinned. Delivery of 65536 body bytes is not authored. CC-5 intent types prefix exactly at as RF-2. N=65536 is not pinned as prefix-only RF-2. That tension is not settled by authoring the prefix integer. Bytes recur at frozen fixtures/g21.v9/G21.cc5.prefix-exactly-at-prehandshake.bin and frozen fixtures/g21.v26/G21.cc5.prefix-exactly-at-prehandshake.bin. g21-fixture-corpus.v35 does not author prefix exactly at the postHandshake bound. g21-fixture-corpus.v35 does not reuse the 16777216 prefix authored at g21-fixture-corpus.v11. g21-fixture-corpus.v35 does not invent 26214400. leftover-join.v45 of G21 remains the current recorded G21 leftover remasurement (D-359) until a recordable successor is adopted. leftover-join.v14 of sarif remains the current recorded DR-122 leftover remasurement (D-347). Frozen g21-fixture-corpus.v33 remains the D-358 leftover-design per-D-002-platform copies recording. Frozen g21-fixture-corpus.v31 remains the D-356 leftover-design CC-5 invalid-UTF-8 first-authoring. Frozen g21-fixture-corpus.v30 remains the D-354 leftover-design copies recording. Frozen g21-fixture-corpus.v26 remains the D-352 leftover-design truncated-body first-authoring. Frozen g21-fixture-corpus.v34 stays unrecorded. Frozen g21-fixture-corpus.v9 stays unrecorded. Frozen g21-fixture-corpus.v10 stays unrecorded. g21 leftover-join and g21-fixture-corpus are different lineages; their version numbers are unrelated. g21-fixture-corpus.v35 does not SATISFY DR-114. g21-fixture-corpus.v35 does not SATISFY DR-133. g21-fixture-corpus.v35 does not SATISFY DR-117. g21-fixture-corpus.v35 does not remasure leftover-join.v45 of G21. g21-fixture-corpus.v35 does not remasure leftover-join.v14 of sarif. g21-fixture-corpus.v35 does not remasure g21-fixture-corpus.v33. g21-fixture-corpus.v35 does not remasure g21-fixture-corpus.v31. g21-fixture-corpus.v35 does not remasure g21-fixture-corpus.v30. g21-fixture-corpus.v35 does not remasure g21-fixture-corpus.v26. g21-fixture-corpus.v35 does not claim CC-5 fully authored. g21-fixture-corpus.v35 applies nothing and does not authorize docs/v2/implementation/."
    )
    obj["purpose"] = (
        "Land g21-fixture-corpus.v34 Stage A Claude CLAUDE-G21FXV34-M-1 and CLAUDE-G21FXV34-S-1 and Codex 1 unlabeled MUST-FIX. Frozen g21-fixture-corpus.v34 stays unmoved. Frozen g21-fixture-corpus.v9 stays unmoved. leftoverDesignClosedIfAcceptedAndRecorded []. basedOn.d359.role is the sole last-heading claimant. proposedLaterWork[0] names g21-fixture-corpus.v35. Frozen g21-fixture-corpus.v34 Findings land at g21-fixture-corpus.v35. Do not record g21-fixture-corpus.v34 as current. Do not record g21-fixture-corpus.v9 or g21-fixture-corpus.v10 as current. Do not SATISFY DR-114. Do not remasure leftover-join.v45 of G21. Do not remasure leftover-join.v14 of sarif. Do not remasure g21-fixture-corpus.v33. Do not remasure g21-fixture-corpus.v31. Do not remasure g21-fixture-corpus.v30. Do not remasure g21-fixture-corpus.v26. Do not claim CC-5 fully authored. Do not pin N=65536 as prefix-only RF-2. Do not pin the observable refusal route for these bytes. Do not first-author prefix exactly at the postHandshake bound. Do not invent 26214400. Do not reuse the 16777216 prefix authored at g21-fixture-corpus.v11. Do not measure leftover-design of this injection stale as an authoring claim. Do not record leftover-join.v35 of G21 as current. Do not record leftover-join.v34 of G21 as current. Do not record leftover-join.v40 of G21, leftover-join.v41 of G21, leftover-join.v42 of G21, leftover-join.v43 of G21, or leftover-join.v44 of G21 as current. Do not record g21-fixture-corpus.v32 as current. Do not invent an identifier for the unlabeled Codex MUST-FIX."
    )

    predecessor_v34 = {
        "path": "docs/coop/artifacts/g21-fixture-corpus.v34.json",
        "sha256": "d0888bd9789620c3e9359406a3984cd2395a141a6dcece98e6d473d96971c501",
        "recording": "unrecorded",
        "reviews": {
            "claude": {
                "path": "docs/coop/artifacts/g21-fixture-corpus.v34.review-independent.claude2.json",
                "sha256": "aa530da91aa8a4d0b3366f23e289ffcfefe58edf99555f5c11f2063f26cf7aff",
                "verdict": "REJECT 1 MUST-FIX CLAUDE-G21FXV34-M-1, 1 SHOULD-FIX CLAUDE-G21FXV34-S-1",
            },
            "codex": {
                "path": "docs/coop/artifacts/g21-fixture-corpus.v34.review-independent.codex.json",
                "sha256": "df0f46e4c5f6befb1a03b6383ca59d090bb5060414beda6aa31b609459df0b5d",
                "verdict": "REJECT 1 unlabeled MUST-FIX",
            },
        },
        "role": "Predecessor. Unmoved. Unrecorded. Frozen g21-fixture-corpus.v34 Stage A Claude REJECT 1 MUST-FIX CLAUDE-G21FXV34-M-1, 1 SHOULD-FIX CLAUDE-G21FXV34-S-1; Codex REJECT 1 unlabeled MUST-FIX. Findings land at g21-fixture-corpus.v35. Payload bytes at fixtures/g21.v26/ stay frozen and unmoved. Do not record g21-fixture-corpus.v34 as current. Not last-heading. Not this artifact's version number.",
    }
    predecessor_v9 = {
        "path": "docs/coop/artifacts/g21-fixture-corpus.v9.json",
        "sha256": "0289fd23c8e337f29e1ffbc818bef9dd23d3f7b8305435d33d7f12f762753b32",
        "recording": "unrecorded",
        "reviews": {
            "claude": {
                "path": "docs/coop/artifacts/g21-fixture-corpus.v9.review-independent.claude2.json",
                "sha256": "73482345259c35a668533dd1f74f962f3d47f65ba9f46a2f2e23958c038ef3a5",
                "verdict": "REJECT 2 MUST-FIX CLAUDE-G21FXV9-M-1 CLAUDE-G21FXV9-M-2, 1 SHOULD-FIX CLAUDE-G21FXV9-S-1",
            },
            "codex": {
                "path": "docs/coop/artifacts/g21-fixture-corpus.v9.review-independent.codex.json",
                "sha256": "3f5fa55cbb68eac6367e574e9a0ca64d4e1b82988c21a23febdc65328e980a8e",
                "verdict": "REJECT 2 unlabeled MUST-FIX",
            },
        },
        "role": "Predecessor. Unmoved. Unrecorded. Dual REJECT. D-301 ordered Frozen g21-fixture-corpus.v9 stay frozen; do not record it as current. G21.cc5.prefix-exactly-at-prehandshake bytes at fixtures/g21.v9/ are byte-identical to this payload (digest bf5e8ffa51a9e748985800c1d3d7f1a2a6ae7435136593ca8d9637e3f87c699c). CLAUDE-G21FXV9-M-1 pinned RF-2 typed refusal from the prefix alone on N=65536; g21-fixture-corpus.v35 does not pin that. CLAUDE-G21FXV9-M-2 required splitting postHandshake remainder; remainderAfterThisCorpus keeps CC-5 prefix exactly at the postHandshake bound unauthored. Not last-heading. Not this artifact's version number.",
    }
    predecessor_v10 = {
        "path": "docs/coop/artifacts/g21-fixture-corpus.v10.json",
        "sha256": "a9fb227a500867340f8e2d1b032791ae684779579678d7f3877bff8d5b9fa78a",
        "recording": "unrecorded",
        "reviews": {
            "claude": {
                "path": "docs/coop/artifacts/g21-fixture-corpus.v10.review-independent.claude2.json",
                "sha256": "d5ef958cee3a34de0a2d980d6c97bf9083c0e463a46a7775d38413f90e957667",
                "verdict": "ACCEPT 0/0 with advisories",
            },
            "codex": {
                "path": "docs/coop/artifacts/g21-fixture-corpus.v10.review-independent.codex.json",
                "sha256": "cf613c0981094b5c12133eae29afa4fac7b82f2aa942c2c9e0e79b62fed84d46",
                "verdict": "REJECT 0 MUST-FIX 1 SHOULD-FIX unlabeled",
            },
        },
        "role": "Predecessor. Unmoved. Unrecorded. D-301 ordered Frozen g21-fixture-corpus.v10 stay frozen; do not record it as current. Authored the far-over-prehandshake half after g21-fixture-corpus.v9 dual REJECT. Not this payload's member. Not last-heading. Not this artifact's version number.",
    }

    based = obj["basedOn"]
    new_based = {"d359": based["d359"], "predecessorV34": predecessor_v34, "predecessorV9": predecessor_v9, "predecessorV10": predecessor_v10}
    for k, v in based.items():
        if k != "d359":
            new_based[k] = v
    obj["basedOn"] = new_based
    obj["basedOn"]["d359"]["role"] = (
        "Last live heading at dispatch. Last-heading custody only. Recorded leftover-join.v45 of G21 as G21 leftover remasurement. leftoverDesign [OBL-G21-FX-AUTHORING]. leftover-design of per-D-002-platform copies of the D-356 bytes is remasured stale as an authoring claim. leftoverDesignClosedIfAcceptedAndRecorded []. remainingNotAuthored.remainingCc5Injections names CC-5 prefix exactly at the operative bound first. g21-fixture-corpus.v35 does not remasure leftover-join.v45 of G21 and does not remasure leftover-join.v14 of sarif."
    )

    obj["controlFrameEncoding"]["note"] = (
        "g21-fixture-corpus.v35 quotes prefix exactly at the preHandshake bound using the recorded preHandshake bound 65536 as N. Direct analogue of G21.cc5.prefix-one-over-prehandshake (N=65537) and G21.cc5.length-prefix-0 (N=0): 4-byte prefix, no body, sanctioned at DECISION-PACKETS/D1-plan/G21.md axis E item 27. Hex 00010000. The quoted preHandshake clause refuses N greater than 65536 or N equal to 0; N=65536 is not that refusal. Occupancy EV-5 oversize-from-prefix does not apply. N=65536 is in-bound against the quoted preHandshake clause. The receiver must read the body. Body length 0 is less than claimed N=65536. g21-fixture-corpus.v35 does not assert the truncated-body class and does not deny the recorded truncated-body predicate. The observable refusal route for these bytes is not pinned. Delivery of 65536 body bytes is not authored. N=65536 is not pinned as prefix-only RF-2. g21-fixture-corpus.v35 does not author prefix exactly at the postHandshake bound. It does not reuse the 16777216 prefix authored at g21-fixture-corpus.v11. It does not invent 26214400. It does not author a ping body schema. It does not classify non-object top level as CC-5. Bytes recur at frozen fixtures/g21.v9/ and frozen fixtures/g21.v26/."
    )
    obj["whatIsAuthored"] = (
        "The prefix integer of one remaining CC-5 injection: G21.cc5.prefix-exactly-at-prehandshake, a closed 4-byte big-endian unsigned N=65536 with no body, quoting control-protocol-contract.v2 transportAndFraming.framing.bounds.preHandshake. Direct analogue of G21.cc5.prefix-one-over-prehandshake. Delivery of 65536 body bytes is not authored. The observable refusal route is not pinned. No per-D-002-platform copies. No NT-6. No FC-NC-CA1-PROCESS-TREE. Prefix exactly at the postHandshake bound is not authored."
    )
    # keep whatIsNotAuthored from speaker-renamed v34; add pins
    extra_not = [
        "delivery of 65536 body bytes",
        "the observable refusal route for N=65536",
        "g21-fixture-corpus.v9 or g21-fixture-corpus.v10 recorded as current",
        "g21-fixture-corpus.v34 recorded as current",
    ]
    for x in extra_not:
        if x not in obj["whatIsNotAuthored"]:
            obj["whatIsNotAuthored"].append(x)

    dnm = obj["authoredCatalog"]["doesNotMutate"]
    if "docs/coop/artifacts/fixtures/g21.v26/" not in dnm:
        dnm.append("docs/coop/artifacts/fixtures/g21.v26/")
    obj["authoredCatalog"]["doesNotMutate"] = dnm
    m = obj["authoredCatalog"]["members"][0]
    m["path"] = "docs/coop/artifacts/fixtures/g21.v27/G21.cc5.prefix-exactly-at-prehandshake.bin"
    m["sha256"] = PAYLOAD_SHA
    m["byteLength"] = 4
    m["mutation"] = (
        "Closed 4-byte big-endian unsigned length N=65536 and no body. Present in closed CC-5 intent as prefix exactly at the operative bound. The quoted preHandshake bound is 65536; exactly at that bound is N=65536. Hex 00010000. Direct analogue of G21.cc5.prefix-one-over-prehandshake (N=65537, hex 00010001, 4 bytes, no body) and G21.cc5.length-prefix-0 (N=0, hex 00000000, 4 bytes, no body). 65536 is quoted from control-protocol-contract.v2 transportAndFraming.framing.bounds.preHandshake, not invented. The quoted preHandshake clause refuses N greater than 65536 or N equal to 0 from the prefix alone; N=65536 is not that refusal. Occupancy EV-5 oversize-from-prefix does not apply. N=65536 is in-bound against the quoted preHandshake clause. The receiver must read the body. Body length 0 is less than claimed N=65536. g21-fixture-corpus.v35 does not assert the truncated-body class of G21.cc5.truncated-body and does not deny the recorded truncated-body predicate of g21-fixture-corpus.v26 (N greater than 0 with fewer than N body bytes). The observable refusal route for these bytes is not pinned. Delivery of 65536 body bytes is not authored. Hex 00010000 is not hex 01000000; g21-fixture-corpus.v35 does not reuse the 16777216 prefix authored at g21-fixture-corpus.v11. g21-fixture-corpus.v35 does not invent 26214400. g21-fixture-corpus.v35 does not author prefix exactly at the postHandshake bound. Bytes recur at frozen fixtures/g21.v9/G21.cc5.prefix-exactly-at-prehandshake.bin and frozen fixtures/g21.v26/G21.cc5.prefix-exactly-at-prehandshake.bin."
    )
    m["expected"] = (
        "CC-5 intent types prefix exactly at as RF-2. The quoted preHandshake clause refuses N greater than 65536 or N equal to 0 from the prefix alone; N=65536 is not that refusal. N=65536 is not pinned as prefix-only RF-2. Occupancy EV-5 oversize-from-prefix does not apply. The observable refusal route for these bytes is not pinned by g21-fixture-corpus.v35. Uncommitted candidates discarded."
    )

    obj["remainderAfterThisCorpus"] = (
        "Leftover-design of OBL-G21-FX-AUTHORING remains on leftover-join.v45 of G21 until a later leftover-join remasurement. CC-5 prefix exactly at the postHandshake bound remains unauthored. Delivery of 65536 body bytes at the preHandshake exact bound is not authored. N=65536 is not pinned as prefix-only RF-2. The observable refusal route for these bytes is not pinned. The quoted preHandshake clause and CC-5 intent still disagree about N=65536; authoring the prefix integer does not settle that tension as a prefix-only RF-2 pin. The far-over family is witnessed by one non-unique far-over integer on each half and does not exhaust the family. Remaining CC-5 injections also stay unauthored: duplicate members, unknown members, floats, negative integers, and over-uint53 integers. Per-D-002-platform copies of these bytes stay unauthored. NT-6 stays unauthored. FC-NC-CA1-PROCESS-TREE stays unauthored. live-cell crash/panic/timeout/resource/malformed/truncated/duplicate/EOF/process-tree/recovery stay unauthored. CC-1 through CC-4 and CC-6 through CC-11 stay unauthored. G21 execution, including candidate-buffer digest, subsequent-session view, host-projection goldens, and EV-5 diagnostic/audit bytes, remains qualification."
    )

    does = [x for x in obj["doesNot"] if x not in (
        "Does not classify this injection as truncated-body.",
    )]
    for line in [
        "Does not pin the observable refusal route for these bytes.",
        "Does not author delivery of 65536 body bytes.",
        "Does not deny the recorded truncated-body predicate.",
        "Does not record g21-fixture-corpus.v9 as current.",
        "Does not record g21-fixture-corpus.v10 as current.",
        "Does not record g21-fixture-corpus.v34 as current.",
        "Does not record leftover-join.v35 of G21 as current.",
        "Does not invent an identifier for the unlabeled Codex g21-fixture-corpus.v34 MUST-FIX.",
    ]:
        if line not in does:
            does.append(line)
    obj["doesNot"] = does

    fails = [x for x in obj["failsIf"] if x not in (
        "this injection is classified as truncated-body",
        "leftover-join.v34 of G21 is collapsed with g21-fixture-corpus.v34",
    )]
    for line in [
        "N=65536 is pinned as a prefix-only RF-2 refusal",
        "the observable refusal route for these bytes is pinned",
        "delivery of 65536 body bytes is claimed authored",
        "the recorded truncated-body predicate is denied as a byte fact",
        "g21-fixture-corpus.v9 or g21-fixture-corpus.v10 is recorded as current",
        "g21-fixture-corpus.v34 is recorded as current",
        "leftover-join.v35 of G21 is recorded as current",
        "leftover-join.v35 of G21 is collapsed with g21-fixture-corpus.v35",
        "leftover-join.v34 of G21 is collapsed with g21-fixture-corpus.v34",
        "an identifier is invented for the unlabeled Codex g21-fixture-corpus.v34 MUST-FIX",
        "g21-fixture-corpus.v9 is unnamed as the byte-identical predecessor",
        "CLAUDE-G21FXV34-M-1 is unlanded",
        "CLAUDE-G21FXV34-S-1 is unlanded",
        "payload bytes are not hex 00010000",
    ]:
        if line not in fails:
            fails.append(line)
    obj["failsIf"] = fails

    obj["proposedLaterWork"] = [
        "A later D-000 recording may pin g21-fixture-corpus.v35. g21-fixture-corpus.v35 does not perform that recording.",
        "A later leftover-join remasurement succeeding leftover-join.v45 of G21 (D-359) may remasure leftover-design of this prefix integer stale as an authoring claim. g21-fixture-corpus.v35 does not remasure leftover-join.v45 of G21.",
        "A later leftover-design cycle may author per-D-002-platform copies of these bytes. g21-fixture-corpus.v35 does not author those copies.",
        "A later leftover-design cycle may author prefix exactly at the postHandshake bound without reusing hex 01000000. g21-fixture-corpus.v35 does not author that half.",
        "A later leftover-design cycle may author delivery of 65536 body bytes if OQ-G21-4 is settled. g21-fixture-corpus.v35 does not author that delivery.",
        "N=65536 is not pinned as prefix-only RF-2. The observable refusal route is not pinned. g21-fixture-corpus.v35 does not settle that tension.",
        "A later leftover-design cycle may author remaining G21 classes only where types are already closed. g21-fixture-corpus.v35 does not invent those bytes.",
    ]

    ri = obj["recordedInputs"]
    ri["docs/coop/artifacts/g21-fixture-corpus.v9.json"] = "0289fd23c8e337f29e1ffbc818bef9dd23d3f7b8305435d33d7f12f762753b32"
    ri["docs/coop/artifacts/g21-fixture-corpus.v9.review-independent.claude2.json"] = "73482345259c35a668533dd1f74f962f3d47f65ba9f46a2f2e23958c038ef3a5"
    ri["docs/coop/artifacts/g21-fixture-corpus.v9.review-independent.codex.json"] = "3f5fa55cbb68eac6367e574e9a0ca64d4e1b82988c21a23febdc65328e980a8e"
    ri["docs/coop/artifacts/g21-fixture-corpus.v10.json"] = "a9fb227a500867340f8e2d1b032791ae684779579678d7f3877bff8d5b9fa78a"
    ri["docs/coop/artifacts/g21-fixture-corpus.v10.review-independent.claude2.json"] = "d5ef958cee3a34de0a2d980d6c97bf9083c0e463a46a7775d38413f90e957667"
    ri["docs/coop/artifacts/g21-fixture-corpus.v10.review-independent.codex.json"] = "cf613c0981094b5c12133eae29afa4fac7b82f2aa942c2c9e0e79b62fed84d46"
    ri["docs/coop/artifacts/g21-fixture-corpus.v34.json"] = "d0888bd9789620c3e9359406a3984cd2395a141a6dcece98e6d473d96971c501"
    ri["docs/coop/artifacts/g21-fixture-corpus.v34.review-independent.claude2.json"] = "aa530da91aa8a4d0b3366f23e289ffcfefe58edf99555f5c11f2063f26cf7aff"
    ri["docs/coop/artifacts/g21-fixture-corpus.v34.review-independent.codex.json"] = "df0f46e4c5f6befb1a03b6383ca59d090bb5060414beda6aa31b609459df0b5d"
    ri["docs/coop/artifacts/fixtures/g21.v9/G21.cc5.prefix-exactly-at-prehandshake.bin"] = PAYLOAD_SHA
    ri["docs/coop/artifacts/fixtures/g21.v26/G21.cc5.prefix-exactly-at-prehandshake.bin"] = PAYLOAD_SHA
    ri["docs/coop/artifacts/fixtures/g21.v27/G21.cc5.prefix-exactly-at-prehandshake.bin"] = PAYLOAD_SHA
    # drop v34 payload key if speaker-renamed incorrectly
    ri.pop("docs/coop/artifacts/fixtures/g21.v26/G21.cc5.prefix-exactly-at-prehandshake.bin", None)
    ri["docs/coop/artifacts/fixtures/g21.v26/G21.cc5.prefix-exactly-at-prehandshake.bin"] = PAYLOAD_SHA
    obj["recordedInputs"] = ri

    obj["remeasurementClause"] = (
        "If a cited file moves in a way that is not append-only COORD growth or COORD heading hygiene, with file 08, leftover-join.v45 of G21, leftover-join.v14 of sarif, g21-fixture-corpus.v33, g21-fixture-corpus.v31, g21-fixture-corpus.v30, g21-fixture-corpus.v26, occupancy v4, control-protocol-contract.v2, the G21.cc5.prefix-exactly-at-prehandshake bytes, frozen g21-fixture-corpus.v34, frozen g21-fixture-corpus.v9, and g21-fixture-corpus.v35 unmoved, remasure before recording. recordedInputs.HEAD must equal the top-level head. Frozen leftover-join.v45 of G21 remains the current recorded G21 leftover remasurement (D-359) until a recordable successor is adopted. Frozen leftover-join.v14 of sarif remains the current recorded DR-122 leftover remasurement (D-347). Frozen occupancy v4 remains current G21 occupancy remasurement. Frozen g21-fixture-corpus.v33 remains the D-358 copies recording. Frozen g21-fixture-corpus.v31 remains the D-356 invalid-UTF-8 first-authoring. Frozen g21-fixture-corpus.v30 remains the D-354 copies recording. Frozen g21-fixture-corpus.v26 remains the D-352 truncated-body first-authoring. Frozen g21-fixture-corpus.v34 Findings land at g21-fixture-corpus.v35. Frozen g21-fixture-corpus.v9 stays unrecorded."
    )
    obj["findingDisposition"] = {
        "lastHeadingCustody": "basedOn.d359.role is the sole last-heading claimant.",
        "speaker": "proposedLaterWork[0] names g21-fixture-corpus.v35 as the later D-000 recording target.",
        "namedOpenDecision": "N=65536 is not pinned as prefix-only RF-2. The observable refusal route for these bytes is not pinned. The quoted preHandshake clause refuses N greater than 65536 or N equal to 0; N=65536 is not that refusal. CC-5 intent types prefix exactly at as RF-2. Authoring the prefix integer of G21.cc5.prefix-exactly-at-prehandshake does not settle that tension. Prefix exactly at the postHandshake bound remains unauthored. Delivery of 65536 body bytes remains unauthored (OQ-G21-4).",
        "farOverFamily": "The far-over family is not exhausted. leftover-design of remaining far-over members remains.",
        "prefixExactlyAtWitness": "G21.cc5.prefix-exactly-at-prehandshake witnesses the prefix integer of prefix exactly at the preHandshake bound with N=65536 and no body, hex 00010000. leftover-design of that prefix integer is for a later leftover-join remasurement succeeding leftover-join.v45 of G21 to measure; g21-fixture-corpus.v35 does not measure it.",
        "findingsLandV34": "Frozen g21-fixture-corpus.v34 Findings land at g21-fixture-corpus.v35.",
        "claudeV34M1": "MUST-FIX CLAUDE-G21FXV34-M-1. Landed: expected, mutation, doesNot, and failsIf no longer deny truncated-body as a byte fact. Byte facts recites N=65536 is in-bound, the receiver must read the body, and body length 0 is less than claimed N. The observable refusal route is not pinned, symmetric with N=65536 is not pinned as prefix-only RF-2.",
        "claudeV34S1": "SHOULD-FIX CLAUDE-G21FXV34-S-1. Landed: basedOn.predecessorV9 names g21-fixture-corpus.v9 path, digest, both Stage A verdict strings, byte-identical payload, and D-301 freeze. basedOn.predecessorV10 names g21-fixture-corpus.v10. recordedInputs pins those files and reviews. doesNot denies recording g21-fixture-corpus.v9 or g21-fixture-corpus.v10 as current. mutation recites bytes recur at frozen fixtures/g21.v9/.",
        "codexV34MustFix": "UNLABELED. Landed: whatIsAuthored and mutation state delivery of 65536 body bytes is not authored; these four bytes are the prefix integer, not a complete frame of N body bytes; complete-injection and not-truncated claims are withdrawn. identifierInvented false.",
        "claudeV9M1": "MUST-FIX CLAUDE-G21FXV9-M-1. Landed: expected does not pin RF-2 typed refusal from the prefix alone on N=65536.",
        "claudeV9M2": "MUST-FIX CLAUDE-G21FXV9-M-2. Landed: remainderAfterThisCorpus and whatIsNotAuthored keep CC-5 prefix exactly at the postHandshake bound unauthored.",
    }

    text = json.dumps(obj, indent=2, ensure_ascii=False) + "\n"
    # speaker-rename must not have rewritten leftover-join.v34 of G21
    assert "leftover-join.v34 of G21" in text
    assert "g21-fixture-corpus.v35" in text
    assert "Does not record leftover-join.v35 of G21 as current." in text
    if SUBJECT.exists():
        os.chmod(SUBJECT, 0o644)
    SUBJECT.write_text(text)
    os.chmod(SUBJECT, 0o444)
    print("payload", payload.hex(), sha256_file(PAYLOAD), oct(PAYLOAD.stat().st_mode)[-4:])
    print("subject", sha256_file(SUBJECT), SUBJECT.stat().st_size, oct(SUBJECT.stat().st_mode)[-4:])
    loaded = json.loads(SUBJECT.read_text())
    assert loaded["head"] == HEAD
    assert loaded["recordedInputs"]["HEAD"] == HEAD
    assert loaded["leftoverDesignClosedIfAcceptedAndRecorded"] == []
    assert loaded["basedOn"]["predecessorV34"]["role"].startswith("Predecessor")
    assert "Findings land at g21-fixture-corpus.v35" in loaded["basedOn"]["predecessorV34"]["role"]
    assert "This injection is not truncated-body" not in text
    print("ok")


if __name__ == "__main__":
    main()
