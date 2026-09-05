#!/usr/bin/env python3
"""Build g21-fixture-corpus.v34: CC-5 prefix-exactly-at-prehandshake (N=65536, 4 bytes)."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "docs/coop/artifacts"
PAYLOAD_DIR = ART / "fixtures/g21.v26"
PAYLOAD = PAYLOAD_DIR / "G21.cc5.prefix-exactly-at-prehandshake.bin"
SUBJECT = ART / "g21-fixture-corpus.v34.json"

HEAD = "5a45ebf259a2f3094b18add549185223b0a80625"


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> None:
    PAYLOAD_DIR.mkdir(parents=True, exist_ok=True)
    payload = (65536).to_bytes(4, "big")
    assert payload.hex() == "00010000"
    if PAYLOAD.exists():
        os.chmod(PAYLOAD, 0o644)
    PAYLOAD.write_bytes(payload)
    os.chmod(PAYLOAD, 0o444)
    payload_sha = sha256_file(PAYLOAD)
    assert len(payload) == 4

    def h(rel: str) -> str:
        return sha256_file(ROOT / rel)

    coord = h("docs/coop/COORDINATOR-DECISIONS.md")
    file08 = h("docs/v2/architecture/08-decision-and-readiness-register.md")
    assert file08 == "e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e"
    assert coord == "2c47bdb3909b454e8cad411e65d404d27627e079031f1961b7a8627a44237cf5"

    obj = {
        "artifact": "g21-fixture-corpus.v34",
        "version": 34,
        "date": "2026-09-01",
        "documentClass": "DESIGN-CONTRACT-CANDIDATE",
        "registerRow": "DR-G21",
        "registerRowNote": (
            "registerRow is the already-named gate DR-G21 because g21-fixture-corpus.v34 authors leftover-design of one remaining CC-5 injection of the live G21 INPUT-corpus class G21.cc.CC-5: prefix exactly at the preHandshake bound, quoting the recorded preHandshake bound 65536 as the 4-byte big-endian unsigned length N with no body, the direct analogue of G21.cc5.prefix-one-over-prehandshake and G21.cc5.length-prefix-0. file08StatusToken is DR-G21's own live token (OPEN). Occupancy v4 registerRow is DR-114 because G21 is that row's containment gate; g21-fixture-corpus.v34 does not retarget DR-114 leftover. leftover-join.v45 of G21 (D-359) leftoverDesign remains [OBL-G21-FX-AUTHORING]. leftover-design of the D-356 invalid-UTF-8 injection and of the four D-358 copies is stale as an authoring claim. Prefix exactly at the postHandshake bound remains unauthored. N=65536 is not pinned as prefix-only RF-2 because the quoted preHandshake clause and CC-5 intent disagree about N=65536. leftover-join.v14 of sarif remains the current recorded DR-122 leftover remasurement (D-347). g21-fixture-corpus.v34 does not remasure leftover-join.v45 of G21, does not remasure leftover-join.v14 of sarif, does not remasure g21-fixture-corpus.v33, does not remasure g21-fixture-corpus.v31, does not remasure g21-fixture-corpus.v30, does not remasure g21-fixture-corpus.v26, does not steal DR-114 leftover, does not reopen DR-102 SATISFIED, and does not SATISFY DR-114, DR-133, or DR-117. Frozen g21-fixture-corpus.v33 stays unmoved. Frozen fixtures/g21.v25/ stays unmoved. Frozen fixtures/g21.v24/ stays unmoved. Frozen fixtures/g21.v23/ stays unmoved. Frozen fixtures/g21.v22/ stays unmoved."
        ),
        "namedGate": "DR-G21",
        "status": "CANDIDATE-NOT-APPLIED",
        "reviewStatus": "AWAITING-INDEPENDENT-REVIEW",
        "sealRecommendation": "DO-NOT-SEAL",
        "binds": "NOTHING",
        "authorityClaim": (
            "g21-fixture-corpus.v34 PROPOSES leftover-design fixture implementations for one remaining CC-5 injection against already-closed control-protocol-contract.v2 CC-5 intent: G21.cc5.prefix-exactly-at-prehandshake. Prefix exactly at the preHandshake bound is witnessed by the closed 4-byte big-endian unsigned 65536 with no body, quoting control-protocol-contract.v2 transportAndFraming.framing.bounds.preHandshake. 65536 is quoted, not invented. A 4-byte big-endian N=65536 payload is the direct analogue of G21.cc5.prefix-one-over-prehandshake (N=65537, hex 00010001) and G21.cc5.length-prefix-0 (N=0, hex 00000000). Hex 00010000 is not hex 00010001 and is not hex 01000000. The quoted preHandshake clause refuses N greater than 65536 or N equal to 0 from the prefix alone; N=65536 is not that refusal. Occupancy EV-5 oversize-from-prefix does not apply. This injection is not truncated-body (that member is G21.cc5.truncated-body at N=1). CC-5 intent types prefix exactly at as RF-2. N=65536 is not pinned as prefix-only RF-2. That tension is not settled by authoring the prefix bytes. g21-fixture-corpus.v34 does not author prefix exactly at the postHandshake bound. g21-fixture-corpus.v34 does not reuse the 16777216 prefix authored at g21-fixture-corpus.v11. g21-fixture-corpus.v34 does not invent 26214400. leftover-join.v45 of G21 remains the current recorded G21 leftover remasurement (D-359) until a recordable successor is adopted. leftover-join.v14 of sarif remains the current recorded DR-122 leftover remasurement (D-347). Frozen g21-fixture-corpus.v33 remains the D-358 leftover-design per-D-002-platform copies recording. Frozen g21-fixture-corpus.v31 remains the D-356 leftover-design CC-5 invalid-UTF-8 first-authoring. Frozen g21-fixture-corpus.v30 remains the D-354 leftover-design copies recording. Frozen g21-fixture-corpus.v26 remains the D-352 leftover-design truncated-body first-authoring. g21 leftover-join and g21-fixture-corpus are different lineages; their version numbers are unrelated. g21-fixture-corpus.v34 does not SATISFY DR-114. g21-fixture-corpus.v34 does not SATISFY DR-133. g21-fixture-corpus.v34 does not SATISFY DR-117. g21-fixture-corpus.v34 does not remasure leftover-join.v45 of G21. g21-fixture-corpus.v34 does not remasure leftover-join.v14 of sarif. g21-fixture-corpus.v34 does not remasure g21-fixture-corpus.v33. g21-fixture-corpus.v34 does not remasure g21-fixture-corpus.v31. g21-fixture-corpus.v34 does not remasure g21-fixture-corpus.v30. g21-fixture-corpus.v34 does not remasure g21-fixture-corpus.v26. g21-fixture-corpus.v34 does not claim CC-5 fully authored. g21-fixture-corpus.v34 applies nothing and does not authorize docs/v2/implementation/."
        ),
        "purpose": (
            "Author G21.cc5.prefix-exactly-at-prehandshake after D-359. leftoverDesignClosedIfAcceptedAndRecorded []. basedOn.d359.role is the sole last-heading claimant. proposedLaterWork[0] names g21-fixture-corpus.v34. Do not SATISFY DR-114. Do not remasure leftover-join.v45 of G21. Do not remasure leftover-join.v14 of sarif. Do not remasure g21-fixture-corpus.v33. Do not remasure g21-fixture-corpus.v31. Do not remasure g21-fixture-corpus.v30. Do not remasure g21-fixture-corpus.v26. Do not claim CC-5 fully authored. Do not pin N=65536 as prefix-only RF-2. Do not first-author prefix exactly at the postHandshake bound. Do not invent 26214400. Do not reuse the 16777216 prefix authored at g21-fixture-corpus.v11. Do not measure leftover-design of this injection stale as an authoring claim. Do not record leftover-join.v34 of G21 as current. Do not record leftover-join.v40 of G21, leftover-join.v41 of G21, leftover-join.v42 of G21, leftover-join.v43 of G21, or leftover-join.v44 of G21 as current. Do not record g21-fixture-corpus.v32 as current."
        ),
        "basedOn": {
            "d359": {
                "recording": "D-359",
                "commit": HEAD,
                "role": "Last live heading at dispatch. Last-heading custody only. Recorded leftover-join.v45 of G21 as G21 leftover remasurement. leftoverDesign [OBL-G21-FX-AUTHORING]. leftover-design of per-D-002-platform copies of the D-356 bytes is remasured stale as an authoring claim. leftoverDesignClosedIfAcceptedAndRecorded []. remainingNotAuthored.remainingCc5Injections names CC-5 prefix exactly at the operative bound first. g21-fixture-corpus.v34 does not remasure leftover-join.v45 of G21 and does not remasure leftover-join.v14 of sarif.",
            },
            "leftoverJoinV45": {
                "path": "docs/coop/artifacts/g21-leftover-join.v45.json",
                "sha256": "f63925a912cfd97e3cc15fe27987321b2766f7bc28684da6f530e0a7fa1734cc",
                "recording": "D-359",
                "reviews": {
                    "claude": {
                        "path": "docs/coop/artifacts/g21-leftover-join.v45.review-independent.claude2.json",
                        "sha256": "3c75f955bed0d2d3c974e0f62659c68380a57ccb219f8c8c79cb756ef2641124",
                        "verdict": "ACCEPT 0/0",
                    },
                    "codex": {
                        "path": "docs/coop/artifacts/g21-leftover-join.v45.review-independent.codex.json",
                        "sha256": "87139119497b0073000564321ae5371099c5b30cc9597e3121948787a41737b2",
                        "verdict": "ACCEPT 0/0",
                    },
                },
                "role": "Current G21 leftover remasurement recorded at D-359. leftoverDesign [OBL-G21-FX-AUTHORING]. Dual ACCEPT 0/0. remainingNotAuthored.remainingCc5Injections names CC-5 prefix exactly at the operative bound among remaining injections. leftover-design of G21.cc5.invalid-utf-8 remains stale as an authoring claim. leftover-design of per-D-002-platform copies of the D-356 bytes is remasured stale as an authoring claim. Prefix exactly at the operative bound remains a named open decision. N=65536 is not pinned as prefix-only RF-2. g21-fixture-corpus.v34 does not remasure leftover-join.v45 of G21 and does not close leftover-design. g21 leftover-join and g21-fixture-corpus are different lineages; their version numbers are unrelated. Not this artifact's version number.",
            },
            "fixtureCorpusV33": {
                "path": "docs/coop/artifacts/g21-fixture-corpus.v33.json",
                "sha256": "eb74cf87e89f755e4d6dedc7184cd52653ddc197af97175d9371272a953a6e4c",
                "recording": "D-358",
                "reviews": {
                    "claude": {
                        "path": "docs/coop/artifacts/g21-fixture-corpus.v33.review-independent.claude2.json",
                        "sha256": "c4080cdaa3ee3af0bc760759696a7a355e43fcf3350ab0e3dcda36aa5b4f6513",
                        "verdict": "ACCEPT 0/0",
                    },
                    "codex": {
                        "path": "docs/coop/artifacts/g21-fixture-corpus.v33.review-independent.codex.json",
                        "sha256": "c1afdd434e281a4fdace2777156fa98e6efb2a04e22bf4e15467ecd0833e7bca",
                        "verdict": "ACCEPT 0/0",
                    },
                },
                "role": "Current recorded G21 leftover-design per-D-002-platform copies of G21.cc5.invalid-utf-8 (D-358). leftoverDesignClosedIfAcceptedAndRecorded []. Dual ACCEPT 0/0. Frozen fixtures/g21.v25/ stays unmoved. g21-fixture-corpus.v34 does not remasure g21-fixture-corpus.v33. Not this artifact's version number.",
            },
            "fixtureCorpusV31": {
                "path": "docs/coop/artifacts/g21-fixture-corpus.v31.json",
                "sha256": "cf4b98943c0516723599028bafc6190cd9a022e0eff83a96f2d37b873449e37c",
                "recording": "D-356",
                "reviews": {
                    "claude": {
                        "path": "docs/coop/artifacts/g21-fixture-corpus.v31.review-independent.claude2.json",
                        "sha256": "f53d510f7369a12941c0d9b8bcaab1bec7ba11df476594ca333116b8a8ea2c1c",
                        "verdict": "ACCEPT 0/0",
                    },
                    "codex": {
                        "path": "docs/coop/artifacts/g21-fixture-corpus.v31.review-independent.codex.json",
                        "sha256": "d26183d8ad0babb2d1dde6628118085330c9fae6560be01d947031d5e0d0b089",
                        "verdict": "ACCEPT 0/0",
                    },
                },
                "role": "Predecessor first-authoring of G21.cc5.invalid-utf-8. Recorded at D-356. leftover-design of that injection is stale as an authoring claim. Frozen fixtures/g21.v24/ stays unmoved. g21-fixture-corpus.v34 does not remasure g21-fixture-corpus.v31. Not this artifact's version number.",
            },
            "fixtureCorpusV30": {
                "path": "docs/coop/artifacts/g21-fixture-corpus.v30.json",
                "sha256": "349eb379f30519964b5a0eec23bd1c93bed5bd2d1de7ce9cd0be0e97fff14782",
                "recording": "D-354",
                "reviews": {
                    "claude": {
                        "path": "docs/coop/artifacts/g21-fixture-corpus.v30.review-independent.claude2.json",
                        "sha256": "72220c2e0172f2dd8714eb3c6985acfcbecf215ce023949fd4fe278a603e67ce",
                        "verdict": "ACCEPT 0/0",
                    },
                    "codex": {
                        "path": "docs/coop/artifacts/g21-fixture-corpus.v30.review-independent.codex.json",
                        "sha256": "9f9c845744d663a923571104c392dce5e837b22be411a3c8a273dcc8541f917d",
                        "verdict": "ACCEPT 0/0",
                    },
                },
                "role": "Current recorded G21 leftover-design per-D-002-platform copies of G21.cc5.truncated-body (D-354). leftoverDesignClosedIfAcceptedAndRecorded []. Dual ACCEPT 0/0. Frozen fixtures/g21.v23/ stays unmoved. g21-fixture-corpus.v34 does not remasure g21-fixture-corpus.v30. Not this artifact's version number.",
            },
            "fixtureCorpusV26": {
                "path": "docs/coop/artifacts/g21-fixture-corpus.v26.json",
                "sha256": "4c694f7cb57fecfdc38755426413f88b5cb88decc0dfc0dc8b425d074535a445",
                "recording": "D-352",
                "reviews": {
                    "claude": {
                        "path": "docs/coop/artifacts/g21-fixture-corpus.v26.review-independent.claude2.json",
                        "sha256": "f5ebd3b8b6a0d2be1ef86c44e198fac0961798758d2e38a1f04809c75ae12591",
                        "verdict": "ACCEPT 0/0",
                    },
                    "codex": {
                        "path": "docs/coop/artifacts/g21-fixture-corpus.v26.review-independent.codex.json",
                        "sha256": "613a6072d9217c922ea5ffda01be61a587bd1dace920fd2c57ba8c5d0d53203d",
                        "verdict": "ACCEPT 0/0",
                    },
                },
                "role": "Predecessor first-authoring of G21.cc5.truncated-body. Recorded at D-352. leftover-design of that injection is stale as an authoring claim. Frozen fixtures/g21.v22/ stays unmoved. g21-fixture-corpus.v34 does not remasure g21-fixture-corpus.v26. Not this artifact's version number.",
            },
            "d358": {
                "recording": "D-358",
                "commit": "3832a9d6ac9958ec879c7ab843bfa74237690069",
                "role": "Recorded g21-fixture-corpus.v33 as G21 leftover-design per-D-002-platform copies of the D-356 invalid-UTF-8 injection. leftoverDesignClosedIfAcceptedAndRecorded []. Not last-heading. Last-heading custody remains D-359.",
            },
            "d357": {
                "recording": "D-357",
                "commit": "9c9275f92a4d57f1a86efdd6d67bdda7da6d1f66",
                "role": "Recorded leftover-join.v39 of G21 as G21 leftover remasurement. Historical after D-359. Not last-heading. Last-heading custody remains D-359.",
            },
            "d356": {
                "recording": "D-356",
                "commit": "ae9885e08f1f80a68e101da402cce4c988cf6bd7",
                "role": "Recorded g21-fixture-corpus.v31 as G21 leftover-design CC-5 invalid-UTF-8 injection. leftoverDesignClosedIfAcceptedAndRecorded []. Not last-heading. Last-heading custody remains D-359.",
            },
            "d354": {
                "recording": "D-354",
                "commit": "2a6df439402ce686963447482a4e5150e4d8cd32",
                "role": "Recorded g21-fixture-corpus.v30 as G21 leftover-design per-D-002-platform copies of the D-352 truncated-body injection. leftoverDesignClosedIfAcceptedAndRecorded []. Not last-heading. Last-heading custody remains D-359.",
            },
            "d353": {
                "recording": "D-353",
                "commit": "6c14185c1157c6b1ea0d081ee04659f0fd843798",
                "role": "Recorded leftover-join.v32 of G21 as G21 leftover remasurement. Not last-heading. Last-heading custody remains D-359.",
            },
            "d352": {
                "recording": "D-352",
                "commit": "ef219c158f07911481a26e68dce151136bf696c7",
                "role": "Recorded g21-fixture-corpus.v26 as G21 leftover-design CC-5 truncated-body injection. leftoverDesignClosedIfAcceptedAndRecorded []. Not last-heading. Last-heading custody remains D-359.",
            },
            "d293": {
                "recording": "D-293",
                "commit": "c10319d207cb90e2bf9df4c5e5997cfd35a30193",
                "decisionItem": 8,
                "path": "DECISIONS-RECOMMENDED.md",
                "sha256": "42f27394746d4aac569a09a01da719c0cf318cf114086635e73097a6add97370",
                "role": "Adopted owner decisions. Decision 8 delegates fixture authoring for OBL-G21-FX-AUTHORING under the agreed semantic, coverage, dependency and D-000 constraints. One quoted prefix-exactly-at-prehandshake CC-5 witness exercises that delegation. Prefix exactly at the postHandshake bound remains unauthored. N=65536 is not pinned as prefix-only RF-2. Last-heading custody remains D-359.",
            },
            "d056": {
                "path": "docs/coop/artifacts/coordinator-decisions.D-056.turn2.draft.md",
                "sha256": "dfb0c2af39ff31df9bf3609c131f03ee2d87a585dcd684abd633d47ffb11ed82",
                "role": "Authoring fixtures remains lawful design work now. Execution remains qualification. g21-fixture-corpus.v34 is not a SATISFIED-GRADE cycle.",
            },
            "d086": {
                "recording": "D-086",
                "role": "Named DR-G21 as required-now. g21-fixture-corpus.v34 does not unwrite that naming.",
            },
            "occupancyV4": {
                "path": "docs/coop/artifacts/harness.DR-G21.component-failure-containment.v4.json",
                "sha256": "13addb3cc70611efe22876f84dbe9e15d9a27529446d7e03841d2b2a3f552e0b",
                "recording": "D-218",
                "reviews": {
                    "claude": {
                        "path": "docs/coop/artifacts/harness.DR-G21.component-failure-containment.v4.review-independent.claude2.json",
                        "sha256": "08a8cd0cd148d15487ad379e63b3a979038086328bd49ef5a97ffdf5018adb1d",
                        "verdict": "ACCEPT 0/0",
                    },
                    "codex": {
                        "path": "docs/coop/artifacts/harness.DR-G21.component-failure-containment.v4.review-independent.codex.json",
                        "sha256": "82c039e829b87e6712112967936d0a65cb3b0acb9ae3d483aaa6bdf18e92cd57",
                        "verdict": "ACCEPT 0/0",
                    },
                },
                "role": "Current G21 occupancy remasurement. Has no platforms array. passProperty requires independently pinned implementations on every D-002 platform. Occupancy v4 stays unmoved. g21-fixture-corpus.v34 does not occupy the identifier and does not execute G21.",
            },
            "controlProtocolV2": {
                "path": "docs/coop/artifacts/control-protocol-contract.v2.json",
                "sha256": "c50a79fef566ecccbd8913a3d309b0cf7332f7d77f892474a548ef3d7b4ebdca",
                "recording": "D-015",
                "role": "Consumed. CC-5 intent and transportAndFraming.framing.bounds.preHandshake / postHandshake and transportAndFraming.framing.frame are quoted. 65536 and 16777216 are quoted from those clauses, not invented. N=65536 is the quoted preHandshake bound, not a newly invented bound. Not this artifact's version number.",
            },
            "g10OccupancyV2": {
                "path": "docs/coop/artifacts/harness.DR-G10.provider-conformance.ts-major-1.v2.json",
                "sha256": "b0cbce06487b96bbe7f6af1dae62ba3b3ca55aaa41305cb96f531099e86bf7c9",
                "role": "Quoted only for the D-002 platform list at #$.platforms. G21 occupancy v4 has no platforms array. g21-fixture-corpus.v34 does not copy those platforms into fixture directories in this payload authoring and does not occupy G10. harness.DR-G10.provider-conformance.ts-major-1.v2 is a different lineage. Not this artifact's version number.",
            },
            "g23OccupancyV2": {
                "path": "docs/coop/artifacts/harness.DR-G23.provider-well-formed-admission.preview.v2.json",
                "sha256": "f48ba637bdf193785c05906a1686ce268b27b6ce7355de07fa5effefdd84fb0b",
                "recording": "D-223",
                "role": "ORDERED-EQUAL corroboration only for the four D-002 platform tokens. Platforms are quoted from harness.DR-G10.provider-conformance.ts-major-1.v2, not from this file. g21-fixture-corpus.v34 does not take over G23. harness.DR-G23.provider-well-formed-admission.preview.v2 is a different lineage. Not this artifact's version number.",
            },
            "sarifLeftoverJoinV14": {
                "path": "docs/coop/artifacts/sarif-leftover-join.v14.json",
                "sha256": "8ecea58e0b6823968ebffbbe75640ba3473446985047fd709e308a4a7e40bf97",
                "recording": "D-347",
                "role": "Current recorded DR-122 leftover remasurement (D-347). leftoverDesign [OBL-FC-OUTFAIL-FX]. g21-fixture-corpus.v34 does not remasure leftover-join.v14 of sarif. Not last-heading claimant; basedOn.d359.role is the sole last-heading claimant. Not this artifact's version number.",
            },
            "fixtureCorpusV16": {
                "path": "docs/coop/artifacts/g21-fixture-corpus.v16.json",
                "sha256": "5b04ead4cb88950c9ccf43f6b416a71d3157b56825a27cad02f2b323ca36865b",
                "recording": "D-335",
                "role": "Predecessor first-authoring of G21.cc5.prefix-one-over-posthandshake. Recorded at D-335. Frozen. Not this artifact's version number.",
            },
            "fixtureCorpusV11": {
                "path": "docs/coop/artifacts/g21-fixture-corpus.v11.json",
                "sha256": "13ede1101e3d689130557e070bd683b62cd931b30c670ed2188a825a49fefd91",
                "recording": "D-301",
                "role": "Predecessor first-authoring of G21.cc5.prefix-far-over-prehandshake. Recorded at D-301. Frozen. Those bytes are N=16777216 hex 01000000. g21-fixture-corpus.v34 does not reuse them. Not this artifact's version number.",
            },
        },
        "file08Pin": {
            "path": "docs/v2/architecture/08-decision-and-readiness-register.md",
            "sha256": file08,
        },
        "head": HEAD,
        "requiredNowUnchanged": 28,
        "file08StatusToken": "OPEN",
        "g21OccupancyV4HasNoPlatformsArray": True,
        "g21OccupancyV4PassPropertyQuoted": "Once independently pinned fixture implementations exist for every named corpus class, every live retained-evidence member, every CC-1..CC-11 class, DR-133 NT-1/NT-2/NT-6, and FC-NC-CA1-PROCESS-TREE, for every admitted external component identity on every D-002 platform, each retained-evidence member's passProperty holds. Until those bytes exist, this harness cannot be executed and cannot be QUALIFIED. File 08 remains PROPOSED; not QUALIFIED. File 08 carries G21 (D-086). The live G21 row is OPEN and not QUALIFIED. Live required-now is 28. This file existing is not execution and is not a three-limb recording. CC-1..CC-11 and DR-133 NT-1/NT-2/NT-6 are not executed by this file existing.",
        "platformsQuotedFromG10OccupancyV2": [
            "macos/arm64",
            "macos/x86_64",
            "linux/x86_64",
            "linux/arm64",
        ],
        "g23OccupancyV2PlatformsOrderedEqual": True,
        "windowsStandingQuotedFromG10OccupancyV2": "D-002 defers Windows with explicit disposition. Windows is not a G10 preview-runner platform. delivery.v2 platformMatrix listing windows-x86_64-msvc is V1 DELIVERY law, not a D-002 preview-runner cell.",
        "controlFrameEncoding": {
            "frame": "A control frame is: a 4-byte big-endian unsigned length N, followed by exactly N bytes of frame body. N counts the body only, not the prefix.",
            "preHandshakeBoundQuoted": "Until helloAck is accepted, N greater than 65536 or N equal to 0 is refusal family RF-2, detected from the prefix alone; the receiver must refuse without buffering the body. Rationale: bound memory before any trust or negotiation exists.",
            "postHandshakeBoundQuoted": "After helloAck, the operative bound is the negotiated maxControlFrameBytes (handshake field): the component may accept less than the host offer but never less than 65536; the ceiling either side may offer or accept is 16777216. A frame exceeding the negotiated bound is RF-2.",
            "cc5IntentQuoted": "Length prefix 0; prefix exactly at, one over, and far over the operative bound (pre- and post-handshake bounds separately); truncated bodies; invalid UTF-8; duplicate members; unknown members; floats, negative and over-uint53 integers. Each is RF-2 typed; the fixture's pass property includes the observable memory bound - the receiver refuses oversize from the prefix alone without buffering the body.",
            "cc5ClassificationRule": "CC-5 membership is the closed CC-5 intent, the named G21.cc.CC-5 input-corpus state, and occupancy EV-5 exactByteIntent. RF-2 membership does not itself authorize CC-5 membership. non-object top level is in RF-2 covers and is absent from the closed CC-5 intent.",
            "note": "g21-fixture-corpus.v34 quotes prefix exactly at the preHandshake bound using the recorded preHandshake bound 65536 as N. Direct analogue of G21.cc5.prefix-one-over-prehandshake (N=65537) and G21.cc5.length-prefix-0 (N=0): 4-byte prefix, no body. Hex 00010000. The quoted preHandshake clause refuses N greater than 65536 or N equal to 0; N=65536 is not that refusal. Occupancy EV-5 oversize-from-prefix does not apply. This injection is not truncated-body (that member is G21.cc5.truncated-body at N=1). N=65536 is not pinned as prefix-only RF-2. g21-fixture-corpus.v34 does not author prefix exactly at the postHandshake bound. It does not reuse the 16777216 prefix authored at g21-fixture-corpus.v11. It does not invent 26214400. It does not author a ping body schema. It does not classify non-object top level as CC-5.",
            "encodingQuoted": "A frame body is one UTF-8 JSON text (RFC 8259) whose top level is a single object.",
        },
        "whatIsAuthored": "One remaining CC-5 injection: G21.cc5.prefix-exactly-at-prehandshake, a closed 4-byte big-endian unsigned N=65536 with no body, quoting control-protocol-contract.v2 transportAndFraming.framing.bounds.preHandshake. Direct analogue of G21.cc5.prefix-one-over-prehandshake. No per-D-002-platform copies. No NT-6. No FC-NC-CA1-PROCESS-TREE. Prefix exactly at the postHandshake bound is not authored.",
        "whatIsNotAuthored": [
            "a finding schema",
            "a D9 code, exit number, or HostTermination",
            "a pack IR",
            "a section 7.1 recipe",
            "a ping, pong, hello, helloAck, or other per-type body schema",
            "65536 or 16777216 as newly invented bounds",
            "26214400",
            "CC-5 prefix exactly at the postHandshake bound",
            "CC-5 duplicate members",
            "CC-5 unknown members",
            "CC-5 floats",
            "CC-5 negative integers",
            "CC-5 over-uint53 integers",
            "rejected g21-fixture-corpus.v3 RF-2 non-object-top-level payload; not a CC-5 member",
            "NT-6 d9-exit-hosttermination-refused",
            "crash, panic, timeout, resource, malformed, truncated, duplicate, EOF, process-tree, recovery",
            "CC-1 through CC-4",
            "CC-6 through CC-11",
            "FC-NC-CA1-PROCESS-TREE",
            "candidate-buffer digest, subsequent-session view, and host-projection goldens",
            "EV-5 diagnostic/audit bytes",
            "per-platform copies of these bytes",
            "a D-002 platform list",
            "Windows as a copied platform",
            "closure of leftover-design of OBL-G21-FX-AUTHORING",
            "anti-lockstep-hostile-goldens.v3 stolen as G21 leftover",
            "reuse of the 16777216 prefix authored at g21-fixture-corpus.v11",
            "reuse of the 16777217 prefix authored at g21-fixture-corpus.v16",
            "reuse of the 4294967295 prefix authored at g21-fixture-corpus.v21",
            "reuse of the truncated-body bytes authored at g21-fixture-corpus.v26",
            "reuse of the invalid-UTF-8 bytes authored at g21-fixture-corpus.v31",
            "N=65536 pinned as prefix-only RF-2",
        ],
        "authoredCatalog": {
            "standing": "AUTHORED-BYTES-EXIST. Digests recomputed from disk at dispatch. SHA-256 of file bytes, no canonicalization.",
            "doesNotMutate": [
                "docs/coop/artifacts/fixtures/g21.v1/",
                "docs/coop/artifacts/fixtures/g21.v2/",
                "docs/coop/artifacts/fixtures/g21.v3/",
                "docs/coop/artifacts/fixtures/g21.v4/",
                "docs/coop/artifacts/fixtures/g21.v5/",
                "docs/coop/artifacts/fixtures/g21.v6/",
                "docs/coop/artifacts/fixtures/g21.v7/",
                "docs/coop/artifacts/fixtures/g21.v8/",
                "docs/coop/artifacts/fixtures/g23.v3/",
                "docs/coop/artifacts/fixtures/g23.v4/",
                "docs/coop/artifacts/fixtures/g19.v1/",
                "docs/coop/artifacts/fixtures/g20.v1/",
                "docs/coop/artifacts/fixtures/g20.v2/",
                "docs/coop/artifacts/fixtures/anti-lockstep-goldens.v1/",
                "docs/coop/artifacts/fixtures/g21.v9/",
                "docs/coop/artifacts/fixtures/g21.v10/",
                "docs/coop/artifacts/fixtures/g21.v11/",
                "docs/coop/artifacts/fixtures/g21.v12/",
                "docs/coop/artifacts/fixtures/g21.v15/",
                "docs/coop/artifacts/fixtures/g21.v16/",
                "docs/coop/artifacts/fixtures/g21.v20/",
                "docs/coop/artifacts/fixtures/g21.v21/",
                "docs/coop/artifacts/fixtures/g21.v22/",
                "docs/coop/artifacts/fixtures/g21.v23/",
                "docs/coop/artifacts/fixtures/g21.v24/",
                "docs/coop/artifacts/fixtures/g21.v25/",
            ],
            "executionRemains": "Qualification. Pinning authored bytes is not execution and is not SATISFIED. Candidate-buffer digest, subsequent-session view, host-projection goldens, and EV-5 diagnostic/audit bytes remain G21 execution (D-056), not leftover-design.",
            "members": [
                {
                    "id": "G21.cc5.prefix-exactly-at-prehandshake",
                    "class": "CC-5",
                    "inputCorpusId": "G21.cc.CC-5",
                    "path": "docs/coop/artifacts/fixtures/g21.v26/G21.cc5.prefix-exactly-at-prehandshake.bin",
                    "sha256": payload_sha,
                    "byteLength": 4,
                    "mutation": "Closed 4-byte big-endian unsigned length N=65536 and no body. Present in closed CC-5 intent as prefix exactly at the operative bound. The quoted preHandshake bound is 65536; exactly at that bound is N=65536. Hex 00010000. Direct analogue of G21.cc5.prefix-one-over-prehandshake (N=65537, hex 00010001, 4 bytes, no body) and G21.cc5.length-prefix-0 (N=0, hex 00000000, 4 bytes, no body). 65536 is quoted from control-protocol-contract.v2 transportAndFraming.framing.bounds.preHandshake, not invented. The quoted preHandshake clause refuses N greater than 65536 or N equal to 0 from the prefix alone; N=65536 is not that refusal. Occupancy EV-5 oversize-from-prefix does not apply. No body is authored because this injection is the prefix integer of the closed CC-5 intent's prefix-exactly-at limb, analogue of the two prefix-family members at g21-fixture-corpus.v7. This injection is not truncated-body (that member is G21.cc5.truncated-body at N=1). Hex 00010000 is not hex 01000000; g21-fixture-corpus.v34 does not reuse the 16777216 prefix authored at g21-fixture-corpus.v11. g21-fixture-corpus.v34 does not invent 26214400. g21-fixture-corpus.v34 does not author prefix exactly at the postHandshake bound.",
                    "expected": "CC-5 intent types prefix exactly at as RF-2. The quoted preHandshake clause refuses N greater than 65536 or N equal to 0 from the prefix alone; N=65536 is not that refusal. N=65536 is not pinned as prefix-only RF-2. Occupancy EV-5 oversize-from-prefix does not apply. This injection is not truncated-body. Uncommitted candidates discarded.",
                }
            ],
        },
        "leftoverDesignClosedIfAcceptedAndRecorded": [],
        "leftoverDesignRemainingOnG21": ["OBL-G21-FX-AUTHORING"],
        "remainderAfterThisCorpus": "Leftover-design of OBL-G21-FX-AUTHORING remains on leftover-join.v45 of G21 until a later leftover-join remasurement. CC-5 prefix exactly at the postHandshake bound remains unauthored. N=65536 is not pinned as prefix-only RF-2. The quoted preHandshake clause and CC-5 intent still disagree about N=65536; authoring the prefix bytes does not settle that tension as a prefix-only RF-2 pin. The far-over family is witnessed by one non-unique far-over integer on each half and does not exhaust the family. Remaining CC-5 injections also stay unauthored: duplicate members, unknown members, floats, negative integers, and over-uint53 integers. Per-D-002-platform copies of these bytes stay unauthored. NT-6 stays unauthored. FC-NC-CA1-PROCESS-TREE stays unauthored. live-cell crash/panic/timeout/resource/malformed/truncated/duplicate/EOF/process-tree/recovery stay unauthored. CC-1 through CC-4 and CC-6 through CC-11 stay unauthored. G21 execution, including candidate-buffer digest, subsequent-session view, host-projection goldens, and EV-5 diagnostic/audit bytes, remains qualification.",
        "summary": {
            "leftoverDesign": ["OBL-G21-FX-AUTHORING"],
            "authoredMembers": 1,
            "authoredFiles": 1,
            "requiredNowUnchanged": 28,
            "newRowProposed": False,
            "fixturesExecuted": False,
            "findingSchemaInvented": False,
            "d9Invented": False,
            "section71Invented": False,
            "cc5FullyAuthored": False,
            "nt6Authored": False,
            "fcNcAuthored": False,
            "numericBoundInvented": False,
            "classAOpened": False,
            "dr114Satisfied": False,
            "hostileLeftoverStolen": False,
            "windowsCopied": False,
            "platformCopiesAuthored": False,
            "prefixOnlyRf2Pinned": False,
            "leftoverDesignClosedIfAcceptedAndRecorded": [],
        },
        "doesNot": [
            "Does not SATISFY DR-114.",
            "Does not SATISFY DR-133.",
            "Does not SATISFY DR-127.",
            "Does not SATISFY DR-117.",
            "Does not SATISFY DR-102.",
            "Does not SATISFY DR-122.",
            "Does not reopen DR-102 SATISFIED.",
            "Does not open D-056 Class A.",
            "Does not close leftover-design of OBL-G21-FX-AUTHORING.",
            "Does not remasure leftover-join.v45 of G21.",
            "Does not remasure leftover-join.v14 of sarif.",
            "Does not remasure leftover-join.v39 of G21 as a golden.",
            "Does not remasure leftover-join.v35 of G21 as a golden.",
            "Does not remasure leftover-join.v32 of G21 as a golden.",
            "Does not author NT-6.",
            "Does not author FC-NC-CA1-PROCESS-TREE.",
            "Does not claim CC-5 fully authored.",
            "Does not classify non-object top level as CC-5.",
            "Does not classify this injection as truncated-body.",
            "Does not invent a D-002 platform list.",
            "Does not copy onto Windows.",
            "Does not author per-platform copies.",
            "Does not invent 65536 or 16777216 as new bounds.",
            "Does not invent 26214400.",
            "Does not invent a ping body schema.",
            "Does not invent a D9 code, exit number, or HostTermination.",
            "Does not invent a section 7.1 recipe.",
            "Does not steal OBL-HOSTILE-GOLDENS remaining on DR-127.",
            "Does not steal OBL-DOCTOR-FX-AUTHORING, OBL-JOIN-FX-AUTHORING, OBL-FC-C1, or OBL-BLK-1..4.",
            "Does not take over G12, G23, G24, G27, or G28.",
            "Does not execute NT-3, NT-5, NT-4, or NT-7.",
            "Does not add a DR-G* row.",
            "Does not change live required-now 28.",
            "Does not edit file 08.",
            "Does not claim QUALIFIED.",
            "Does not authorize docs/v2/implementation/.",
            "Does not pin N=65536 as prefix-only RF-2.",
            "Does not first-author prefix exactly at the postHandshake bound.",
            "Does not reuse the 16777216 prefix bytes authored at g21-fixture-corpus.v11.",
            "Does not reuse the 16777217 prefix bytes authored at g21-fixture-corpus.v16.",
            "Does not reuse the 4294967295 prefix bytes authored at g21-fixture-corpus.v21.",
            "Does not reuse the truncated-body bytes authored at g21-fixture-corpus.v26.",
            "Does not reuse the invalid-UTF-8 bytes authored at g21-fixture-corpus.v31.",
            "Does not record leftover-join.v34 of G21 as current.",
            "Does not remasure g21-fixture-corpus.v33.",
            "Does not remasure g21-fixture-corpus.v31.",
            "Does not remasure g21-fixture-corpus.v30.",
            "Does not remasure g21-fixture-corpus.v26.",
            "Does not record leftover-join.v40 of G21 as current.",
            "Does not record leftover-join.v41 of G21 as current.",
            "Does not record leftover-join.v42 of G21 as current.",
            "Does not record leftover-join.v43 of G21 as current.",
            "Does not record leftover-join.v44 of G21 as current.",
            "Does not record g21-fixture-corpus.v32 as current.",
            "Does not measure leftover-design of this injection stale as an authoring claim.",
        ],
        "failsIf": [
            "leftover-design of OBL-G21-FX-AUTHORING is claimed closed by this file existing",
            "CC-5 is claimed fully authored",
            "NT-6 is authored",
            "FC-NC-CA1-PROCESS-TREE is authored",
            "non-object top level is classified as CC-5",
            "this injection is classified as truncated-body",
            "a D-002 platform list is invented",
            "65536 or 16777216 is treated as newly invented rather than quoted from control-protocol-contract.v2",
            "26214400 is invented as a bound",
            "a ping, pong, hello, helloAck, or other per-type body schema is invented",
            "a D9 code, exit number, or HostTermination is invented",
            "DR-114 is SATISFIED",
            "DR-133 is SATISFIED",
            "Class A is opened",
            "live required-now is claimed other than 28",
            "OBL-HOSTILE-GOLDENS leftover remaining on DR-127 is stolen",
            "N=65536 is pinned as a prefix-only RF-2 refusal",
            "prefix exactly at the postHandshake bound is first-authored",
            "the 16777216 prefix bytes authored at g21-fixture-corpus.v11 are reused",
            "the 16777217 prefix bytes authored at g21-fixture-corpus.v16 are reused",
            "the 4294967295 prefix bytes authored at g21-fixture-corpus.v21 are reused",
            "the truncated-body bytes authored at g21-fixture-corpus.v26 are reused",
            "the invalid-UTF-8 bytes authored at g21-fixture-corpus.v31 are reused",
            "leftover-join.v45 of G21 is remasured",
            "leftover-join.v14 of sarif is remasured",
            "leftover-join.v32 of G21 is remasured as a golden",
            "leftover-join.v35 of G21 is remasured as a golden",
            "leftover-join.v39 of G21 is remasured as a golden",
            "per-D-002-platform copies are claimed authored by this speaker",
            "g21-fixture-corpus.v32 is recorded as current",
            "leftover-join.v34 of G21 is recorded as current",
            "leftover-join.v34 of G21 is collapsed with g21-fixture-corpus.v34",
            "leftover-join.v45 of G21 is collapsed with g21-fixture-corpus.v45",
            "authoredCatalog.doesNotMutate drops frozen fixture directories that exist on disk and were listed by g21-fixture-corpus.v33",
            "g21-fixture-corpus.v33 is remasured",
            "g21-fixture-corpus.v31 is remasured",
            "g21-fixture-corpus.v30 is remasured",
            "g21-fixture-corpus.v26 is remasured",
            "leftover-design of this injection is measured stale as an authoring claim by this corpus",
            "payload bytes are not hex 00010000",
        ],
        "proposedLaterWork": [
            "A later D-000 recording may pin g21-fixture-corpus.v34. g21-fixture-corpus.v34 does not perform that recording.",
            "A later leftover-join remasurement succeeding leftover-join.v45 of G21 (D-359) may remasure leftover-design of this injection stale as an authoring claim. g21-fixture-corpus.v34 does not remasure leftover-join.v45 of G21.",
            "A later leftover-design cycle may author per-D-002-platform copies of these bytes. g21-fixture-corpus.v34 does not author those copies.",
            "A later leftover-design cycle may author prefix exactly at the postHandshake bound without reusing hex 01000000. g21-fixture-corpus.v34 does not author that half.",
            "N=65536 is not pinned as prefix-only RF-2. g21-fixture-corpus.v34 does not settle that tension.",
            "A later leftover-design cycle may author remaining G21 classes only where types are already closed. g21-fixture-corpus.v34 does not invent those bytes.",
        ],
        "recordedInputs": {
            "DECISIONS-RECOMMENDED.md": "42f27394746d4aac569a09a01da719c0cf318cf114086635e73097a6add97370",
            "docs/coop/artifacts/harness.DR-G21.component-failure-containment.v4.json": "13addb3cc70611efe22876f84dbe9e15d9a27529446d7e03841d2b2a3f552e0b",
            "docs/coop/artifacts/control-protocol-contract.v2.json": "c50a79fef566ecccbd8913a3d309b0cf7332f7d77f892474a548ef3d7b4ebdca",
            "docs/coop/artifacts/harness.DR-G10.provider-conformance.ts-major-1.v2.json": "b0cbce06487b96bbe7f6af1dae62ba3b3ca55aaa41305cb96f531099e86bf7c9",
            "docs/coop/artifacts/harness.DR-G23.provider-well-formed-admission.preview.v2.json": "f48ba637bdf193785c05906a1686ce268b27b6ce7355de07fa5effefdd84fb0b",
            "docs/coop/COORDINATOR-DECISIONS.md": coord,
            "docs/v2/architecture/08-decision-and-readiness-register.md": file08,
            "docs/coop/artifacts/coordinator-decisions.D-056.turn2.draft.md": "dfb0c2af39ff31df9bf3609c131f03ee2d87a585dcd684abd633d47ffb11ed82",
            "HEAD": HEAD,
            "docs/coop/artifacts/g21-fixture-corpus.v11.json": "13ede1101e3d689130557e070bd683b62cd931b30c670ed2188a825a49fefd91",
            "docs/coop/artifacts/g21-fixture-corpus.v16.json": "5b04ead4cb88950c9ccf43f6b416a71d3157b56825a27cad02f2b323ca36865b",
            "docs/coop/artifacts/g21-fixture-corpus.v21.json": "9409f374863cb9aa1b0e8c0f0c76663d0e15e577462b8466f731ea8d9b1ce385",
            "docs/coop/artifacts/g21-fixture-corpus.v21.review-independent.claude2.json": "ea65832d8cf17fa97ac5f85bb62f0061e2096461e5c5246d8d89e24716f3e9e2",
            "docs/coop/artifacts/g21-fixture-corpus.v21.review-independent.codex.json": "f63e2e8f40e515bd8850b69149ceaaae6cf3e91a58b20eb3ede0af248a479be3",
            "docs/coop/artifacts/g21-fixture-corpus.v25.json": "a529674de076ea925c0bb4431f58f5c0b512dc9b89593ee593415c5796a68753",
            "docs/coop/artifacts/g21-fixture-corpus.v25.review-independent.claude2.json": "869017c5f6606a4f6f25721ada597a1f91bc7b681a882414b5a7c7ff1dd48ee8",
            "docs/coop/artifacts/g21-fixture-corpus.v25.review-independent.codex.json": "92d7d85f4503e9085db1a760d1a130b9430f8db750e924cf81a4cba3ca3a5941",
            "docs/coop/artifacts/fixtures/g21.v11/G21.cc5.prefix-far-over-prehandshake.bin": "67abdd721024f0ff4e0b3f4c2fc13bc5bad42d0b7851d456d88d203d15aaa450",
            "docs/coop/artifacts/fixtures/g21.v15/G21.cc5.prefix-one-over-posthandshake.bin": "afa7518106309c22d325df6d2663249d158d2f36f1976269d6d4104d9198a108",
            "docs/coop/artifacts/fixtures/g21.v20/G21.cc5.prefix-far-over-posthandshake.bin": "ad95131bc0b799c0b1af477fb14fcf26a6a9f76079e48bf090acb7e8367bfd0e",
            "docs/coop/artifacts/fixtures/g21.v22/G21.cc5.truncated-body.bin": "b40711a88c7039756fb8a73827eabe2c0fe5a0346ca7e0a104adc0fc764f528d",
            "docs/coop/artifacts/sarif-leftover-join.v14.json": "8ecea58e0b6823968ebffbbe75640ba3473446985047fd709e308a4a7e40bf97",
            "docs/coop/artifacts/g21-leftover-join.v45.json": "f63925a912cfd97e3cc15fe27987321b2766f7bc28684da6f530e0a7fa1734cc",
            "docs/coop/artifacts/g21-leftover-join.v45.review-independent.claude2.json": "3c75f955bed0d2d3c974e0f62659c68380a57ccb219f8c8c79cb756ef2641124",
            "docs/coop/artifacts/g21-leftover-join.v45.review-independent.codex.json": "87139119497b0073000564321ae5371099c5b30cc9597e3121948787a41737b2",
            "docs/coop/artifacts/g21-fixture-corpus.v26.json": "4c694f7cb57fecfdc38755426413f88b5cb88decc0dfc0dc8b425d074535a445",
            "docs/coop/artifacts/g21-fixture-corpus.v26.review-independent.claude2.json": "f5ebd3b8b6a0d2be1ef86c44e198fac0961798758d2e38a1f04809c75ae12591",
            "docs/coop/artifacts/g21-fixture-corpus.v26.review-independent.codex.json": "613a6072d9217c922ea5ffda01be61a587bd1dace920fd2c57ba8c5d0d53203d",
            "docs/coop/artifacts/g21-fixture-corpus.v30.json": "349eb379f30519964b5a0eec23bd1c93bed5bd2d1de7ce9cd0be0e97fff14782",
            "docs/coop/artifacts/g21-fixture-corpus.v30.review-independent.claude2.json": "72220c2e0172f2dd8714eb3c6985acfcbecf215ce023949fd4fe278a603e67ce",
            "docs/coop/artifacts/g21-fixture-corpus.v30.review-independent.codex.json": "9f9c845744d663a923571104c392dce5e837b22be411a3c8a273dcc8541f917d",
            "docs/coop/artifacts/g21-fixture-corpus.v31.json": "cf4b98943c0516723599028bafc6190cd9a022e0eff83a96f2d37b873449e37c",
            "docs/coop/artifacts/g21-fixture-corpus.v31.review-independent.claude2.json": "f53d510f7369a12941c0d9b8bcaab1bec7ba11df476594ca333116b8a8ea2c1c",
            "docs/coop/artifacts/g21-fixture-corpus.v31.review-independent.codex.json": "d26183d8ad0babb2d1dde6628118085330c9fae6560be01d947031d5e0d0b089",
            "docs/coop/artifacts/fixtures/g21.v24/G21.cc5.invalid-utf-8.bin": "ad8cb54a1c4020b3a094ebfa02b0642383cf053976505f392501a45a82ec5f6e",
            "docs/coop/artifacts/g21-fixture-corpus.v33.json": "eb74cf87e89f755e4d6dedc7184cd52653ddc197af97175d9371272a953a6e4c",
            "docs/coop/artifacts/g21-fixture-corpus.v33.review-independent.claude2.json": "c4080cdaa3ee3af0bc760759696a7a355e43fcf3350ab0e3dcda36aa5b4f6513",
            "docs/coop/artifacts/g21-fixture-corpus.v33.review-independent.codex.json": "c1afdd434e281a4fdace2777156fa98e6efb2a04e22bf4e15467ecd0833e7bca",
            "docs/coop/artifacts/fixtures/g21.v26/G21.cc5.prefix-exactly-at-prehandshake.bin": payload_sha,
        },
        "remeasurementClause": "If a cited file moves in a way that is not append-only COORD growth or COORD heading hygiene, with file 08, leftover-join.v45 of G21, leftover-join.v14 of sarif, g21-fixture-corpus.v33, g21-fixture-corpus.v31, g21-fixture-corpus.v30, g21-fixture-corpus.v26, occupancy v4, control-protocol-contract.v2, the G21.cc5.prefix-exactly-at-prehandshake bytes, and g21-fixture-corpus.v34 unmoved, remasure before recording. recordedInputs.HEAD must equal the top-level head. Frozen leftover-join.v45 of G21 remains the current recorded G21 leftover remasurement (D-359) until a recordable successor is adopted. Frozen leftover-join.v14 of sarif remains the current recorded DR-122 leftover remasurement (D-347). Frozen occupancy v4 remains current G21 occupancy remasurement. Frozen g21-fixture-corpus.v33 remains the D-358 copies recording. Frozen g21-fixture-corpus.v31 remains the D-356 invalid-UTF-8 first-authoring. Frozen g21-fixture-corpus.v30 remains the D-354 copies recording. Frozen g21-fixture-corpus.v26 remains the D-352 truncated-body first-authoring.",
        "findingDisposition": {
            "lastHeadingCustody": "basedOn.d359.role is the sole last-heading claimant.",
            "speaker": "proposedLaterWork[0] names g21-fixture-corpus.v34 as the later D-000 recording target.",
            "namedOpenDecision": "N=65536 is not pinned as prefix-only RF-2. The quoted preHandshake clause refuses N greater than 65536 or N equal to 0; N=65536 is not that refusal. CC-5 intent types prefix exactly at as RF-2. Authoring G21.cc5.prefix-exactly-at-prehandshake does not settle that tension. Prefix exactly at the postHandshake bound remains unauthored.",
            "farOverFamily": "The far-over family is not exhausted. leftover-design of remaining far-over members remains.",
            "prefixExactlyAtWitness": "G21.cc5.prefix-exactly-at-prehandshake witnesses prefix exactly at the preHandshake bound with N=65536 and no body, hex 00010000. leftover-design of that injection is for a later leftover-join remasurement succeeding leftover-join.v45 of G21 to measure; g21-fixture-corpus.v34 does not measure it.",
        },
    }

    text = json.dumps(obj, indent=2, ensure_ascii=False) + "\n"
    if SUBJECT.exists():
        os.chmod(SUBJECT, 0o644)
    SUBJECT.write_text(text)
    os.chmod(SUBJECT, 0o444)
    print("payload", payload.hex(), payload_sha, oct(PAYLOAD.stat().st_mode)[-4:])
    print("subject", sha256_file(SUBJECT), SUBJECT.stat().st_size, oct(SUBJECT.stat().st_mode)[-4:])
    loaded = json.loads(SUBJECT.read_text())
    assert loaded["head"] == HEAD
    assert loaded["recordedInputs"]["HEAD"] == HEAD
    assert loaded["authoredCatalog"]["members"][0]["sha256"] == payload_sha
    assert loaded["leftoverDesignClosedIfAcceptedAndRecorded"] == []
    print("ok")


if __name__ == "__main__":
    main()
