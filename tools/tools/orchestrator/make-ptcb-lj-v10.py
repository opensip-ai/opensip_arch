#!/usr/bin/env python3
"""Build leftover-join.v10 of platform-tcb after D-361 / platform-tcb-contract.v48."""
from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "docs/coop/artifacts"
V9 = ART / "platform-tcb-leftover-join.v9.json"
SUBJECT = ART / "platform-tcb-leftover-join.v10.json"

HEAD = "111a2e70e41d11065216e505e9bdbeafb64e734b"
COORD = "241ad5b4d7efeb0fc3deea9904f3bea16d635d133c44e7b5c2060e966339371f"
FILE08 = "e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e"
SPEAKER = "leftover-join.v10 of platform-tcb"
PRED = "leftover-join.v9 of platform-tcb"

V9_SHA = "1774427e9500940d24f75fbaee622142a8be72547d68a026e18d6e957369e26a"
V9_CLAUDE = "408c6fde1428ea3c7e5ed88ea345882e996c3784b7fe2e48d249f92463be1251"
V9_CODEX = "1383c328558062138ce5c3b090afc468d1e8d2a93e8e8cd32c7db90a4f81d078"
V48 = "9511fca3f795ff66b101257796d4bf80d49c754271cc76139a015efed5fbb98c"
V48_CLAUDE = "8b0801ddcf8fd679a1009f912b5d7e44ba9ae992db6257f61117686cf61c6139"
V48_CODEX = "1c2667d9d8648da20516d83c8085eb943a9cab7b85163df05183db1a256ea40f"
V47 = "44229ea1f23a6af743fac6c1dcfd9b0d069100dad9991ef86449ee179c4dfe97"
V47_CLAUDE = "c68b790630178ff795f49abcac0f39a882f875e23e221b1c0cc1317a2da34031"
V47_CODEX = "1df157780b71a6452d917dc5d8bc7a2ea136416ec1aca98163dc63832ff428da"
G22LJ5 = "70e0efd68e9003d7828c93e2d7d26dad81664adebfcb1c8d38b006c80e620d3f"
G22LJ5_CLAUDE = "1879de4fa51ef72f44c07e8e31337c2954ffa1d200091cfd374d1f5345e98551"
G22LJ5_CODEX = "35454c10cbcd5097afbc1f9a49ffaedc0ae7f518ec2f106b0b34e993be4224bb"
G21LJ45 = "f63925a912cfd97e3cc15fe27987321b2766f7bc28684da6f530e0a7fa1734cc"
SARIF14 = "8ecea58e0b6823968ebffbbe75640ba3473446985047fd709e308a4a7e40bf97"
OCC2 = "2973cda2adac1b612c084b64606e4fc5b5ed5b78317fc64780a7311172ff1307"
V45 = "da87bdb4d100c90e9450fb82744b7d327ae6b7332db550ea808bdbdb0444a7e5"


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> None:
    obj = copy.deepcopy(json.loads(V9.read_text()))
    obj["artifact"] = "platform-tcb-leftover-join.v10"
    obj["version"] = 10
    obj["date"] = "2026-09-01"
    obj["head"] = HEAD
    obj["file08Pin"]["sha256"] = FILE08
    obj["requiredNowUnchanged"] = 28
    obj["file08StatusToken"] = "OPEN"
    obj["status"] = "CANDIDATE-NOT-APPLIED"
    obj["reviewStatus"] = "AWAITING-INDEPENDENT-REVIEW"
    obj["sealRecommendation"] = "DO-NOT-SEAL"
    obj["binds"] = "NOTHING"

    obj["registerRowNote"] = (
        "registerRow is DR-126 because leftover-join.v10 of platform-tcb remasures leftover-design of DR-126 after occupancy v2 (D-219) and after D-361 recorded platform-tcb-contract.v48 as the DR-126 C4-c application-grade TCB successor that makes the selector grammar governing. "
        "file08StatusToken is DR-126's own live token (OPEN). leftover-join.v9 of platform-tcb remains the current recorded DR-126 leftover remasurement (D-268) until a recordable successor is adopted. "
        "leftover-join.v6 of platform-tcb remains frozen and is not current. leftover-join.v7 of platform-tcb is CANDIDATE-NOT-APPLIED (split Claude REJECT CLAUDE-PTLJ-V7-SF1 / Codex ACCEPT 0/0; not Dual ACCEPT; not Dual REJECT) and is not current. "
        "leftover-join.v8 of platform-tcb is CANDIDATE-NOT-APPLIED (Dual REJECT CLAUDE-PTLJ-V8-SF1 / CODEX-PTLJ-V8-SF1) and is not current. "
        "leftover-join.v10 of platform-tcb does not steal OBL-RESERVED-TABLES, does not populate reserved TCB tables, does not apply platform-tcb-contract.v48, and does not SATISFY DR-126."
    )
    obj["authorityClaim"] = (
        "leftover-join.v10 of platform-tcb PROPOSES an execution-remainder join successor for DR-126 leftovers. "
        "leftover-join.v10 of platform-tcb remasures leftover-join.v9 of platform-tcb after D-361 recorded platform-tcb-contract.v48 as the DR-126 C4-c application-grade TCB successor that makes the selector grammar governing. "
        "leftoverDesign remains [OBL-G22-FX-AUTHORING, OBL-RESERVED-TABLES]. Making the selector grammar governing does not populate a table. "
        "leftover-join.v10 of platform-tcb does not SATISFY DR-126. leftover-join.v10 of platform-tcb does not close leftover-design of OBL-G22-FX-AUTHORING or OBL-RESERVED-TABLES. "
        "leftover-join.v10 of platform-tcb does not populate a TCB table, does not add a DR-G* row, does not change live required-now 28, does not execute fixtures, applies nothing, and does not authorize docs/v2/implementation/. "
        "Frozen leftover-join.v45 of G21 remains the D-359 current recorded G21 leftover remasurement. Frozen leftover-join.v14 of sarif remains the D-347 current recorded DR-122 leftover remasurement. "
        "Does not first-author prefix exactly at the operative bound."
    )
    obj["purpose"] = (
        "Remasure leftover-join.v9 of platform-tcb against live HEAD after D-361. Cite occupancy v2 as the current G22 occupancy remasurement. Cite leftover-join.v5 of G22 as the current G22 leftover remasurement (D-271). "
        "Cite platform-tcb-contract.v48 as the current recorded DR-126 C4-c application-grade TCB successor that makes the selector grammar governing (D-361). "
        "CLAUE-PTLJ-V8-SF1 and CODEX-PTLJ-V8-SF1 remain landed at leftover-join.v9 of platform-tcb. CLAUDE-PTLJ-V3-SF1 remains landed at leftover-join.v5 of platform-tcb. CLAUDE-PTLJ-V7-SF1 remains landed at leftover-join.v8 of platform-tcb. leftover-join.v10 of platform-tcb does not re-land them. "
        "Preserve leftoverDesign [OBL-G22-FX-AUTHORING, OBL-RESERVED-TABLES]. Frozen leftover-join.v6 of platform-tcb, leftover-join.v7 of platform-tcb, leftover-join.v8 of platform-tcb, and leftover-join.v9 of platform-tcb stay unmoved. "
        "Do not SATISFY DR-126. Do not populate a TCB table or invent fixture bytes. Do not steal OBL-RESERVED-TABLES. Do not apply platform-tcb-contract.v48. Do not complete C4-d. Do not remasure leftover-join.v45 of G21. Do not remasure leftover-join.v14 of sarif. Do not first-author prefix exactly at the operative bound."
    )
    # typo CLAUE -> CLAUDE
    obj["purpose"] = obj["purpose"].replace("CLAUE-PTLJ", "CLAUDE-PTLJ")

    b = obj["basedOn"]
    b["contractV45"]["role"] = (
        "Predecessor leftover T2-02 successor candidate recorded at D-125. Dual ACCEPT 0/0. Not applied. Not SATISFIED. binds NOTHING. "
        "Historical after D-361. Current recorded DR-126 C4-c application-grade TCB successor that makes the selector grammar governing is platform-tcb-contract.v48 (D-361). "
        "leftover-join.v10 of platform-tcb does not apply platform-tcb-contract.v45 and does not remasure it as a golden. Not this artifact's version number."
    )
    b["d056"]["role"] = (
        "Authoring harness specifications remains design work. Authoring fixtures remains design work. Execution remains qualification. leftover-join.v10 of platform-tcb is not a SATISFIED-GRADE cycle."
    )
    b["namedCatalog"]["role"] = (
        "Named the one live G22 occupancy namedCorpusNotAuthored class. No fixture bytes. No TCB table invented. leftover-join.v10 of platform-tcb consumes that naming. leftover-join.v10 of platform-tcb does not close OBL-G22-FX-AUTHORING."
    )
    b["occupancyV2"]["role"] = (
        "Current G22 occupancy remasurement recorded at D-219. Dual ACCEPT 0/0. leftover-join.v9 of platform-tcb cited occupancy v2 as the current occupancy remasurement. Occupancy v2 stays unmoved. "
        "leftover-join.v10 of platform-tcb does not occupy the identifier and does not execute G22. Not this artifact's version number."
    )
    b["d267"]["role"] = (
        "Not last-heading. Last-heading custody remains D-361. Recorded leftover-join.v9 of platform-tcb was not yet current at that HEAD. Not this artifact's version number."
    )
    b["predecessorV6"]["role"] = (
        "Predecessor. Unmoved. Dual ACCEPT 0/0. Recorded as current DR-126 leftover-join at D-185. Cited occupancy v1 as the specification. leftover-join.v9 of platform-tcb remasured occupancy v1 stale after occupancy v2 (D-219). "
        "Not this artifact's version number. Frozen leftover-join.v6 of platform-tcb Findings land at leftover-join.v9 of platform-tcb for CLAUDE-PTLJ-V8-SF1 / CODEX-PTLJ-V8-SF1. Do not rewrite that landing."
    )
    b["d185"]["role"] = (
        "Recorded leftover-join.v6 of platform-tcb as current DR-126 leftover-join. Not last-heading. Not this artifact's version number."
    )
    b["predecessorV7"]["role"] = (
        "Predecessor. Unmoved. Split. Claude REJECT CLAUDE-PTLJ-V7-SF1. Codex ACCEPT 0/0. Not Dual REJECT. Not Dual ACCEPT. CANDIDATE-NOT-APPLIED. Charged that findingDisposition attributed CLAUDE-PTLJ-V3-SF1 landing to leftover-join.v6 of platform-tcb; it landed at leftover-join.v5 of platform-tcb. leftover-join.v8 of platform-tcb landed CLAUDE-PTLJ-V7-SF1. leftover-join.v10 of platform-tcb does not re-land it. Not this artifact's version number."
    )
    b["predecessorV8"]["role"] = (
        "Predecessor. Unmoved. Dual REJECT CLAUDE-PTLJ-V8-SF1 / CODEX-PTLJ-V8-SF1 (same class: predecessorV6.role retained leftover this-v7 speaker). CANDIDATE-NOT-APPLIED. leftover-join.v9 of platform-tcb remasured that speaker label. leftover-join.v10 of platform-tcb does not re-land CLAUDE-PTLJ-V8-SF1 or CODEX-PTLJ-V8-SF1. Not this artifact's version number."
    )
    b["d219"]["role"] = (
        "Recorded G22 occupancy remasurement v2. Not last-heading. Not this artifact's version number."
    )

    b["predecessorV9"] = {
        "path": "docs/coop/artifacts/platform-tcb-leftover-join.v9.json",
        "sha256": V9_SHA,
        "recording": "D-268",
        "reviews": {
            "claude": {
                "path": "docs/coop/artifacts/platform-tcb-leftover-join.v9.review-independent.claude2.json",
                "sha256": V9_CLAUDE,
                "verdict": "ACCEPT 0/0",
            },
            "codex": {
                "path": "docs/coop/artifacts/platform-tcb-leftover-join.v9.review-independent.codex.json",
                "sha256": V9_CODEX,
                "verdict": "ACCEPT 0/0",
            },
        },
        "role": (
            "Current recorded DR-126 leftover remasurement at D-268 until a recordable successor is adopted. Dual ACCEPT 0/0. leftoverDesign [OBL-G22-FX-AUTHORING, OBL-RESERVED-TABLES]. "
            "Cited platform-tcb-contract.v45 as the leftover T2-02 successor candidate. leftover-join.v10 of platform-tcb remasures leftover-design after D-361 recorded platform-tcb-contract.v48. "
            "Not last-heading. Last-heading custody remains D-361. leftover-join.v10 of platform-tcb does not remasure leftover-join.v9 of platform-tcb as a golden. Not this artifact's version number."
        ),
    }
    b["d268"] = {
        "recording": "D-268",
        "role": (
            "Recorded leftover-join.v9 of platform-tcb as DR-126 leftover remasurement. leftoverDesign [OBL-G22-FX-AUTHORING, OBL-RESERVED-TABLES]. Not last-heading. Last-heading custody remains D-361. Not this artifact's version number."
        ),
    }
    b["d361"] = {
        "recording": "D-361",
        "commit": HEAD,
        "role": (
            "Last live heading at dispatch. Last-heading custody only. Recorded platform-tcb-contract.v48 as DR-126 C4-c application-grade TCB successor that makes the selector grammar governing. "
            "leftover-design of OBL-RESERVED-TABLES remains true. leftover-design of OBL-G22-FX-AUTHORING remains true. leftover-join.v10 of platform-tcb does not remasure leftover-join.v45 of G21 and does not remasure leftover-join.v14 of sarif."
        ),
    }
    b["contractV48"] = {
        "path": "docs/coop/artifacts/platform-tcb-contract.v48.json",
        "sha256": V48,
        "recording": "D-361",
        "reviews": {
            "claude": {
                "path": "docs/coop/artifacts/platform-tcb-contract.v48.review-independent.claude2.json",
                "sha256": V48_CLAUDE,
                "verdict": "ACCEPT 0/0",
            },
            "codex": {
                "path": "docs/coop/artifacts/platform-tcb-contract.v48.review-independent.codex.json",
                "sha256": V48_CODEX,
                "verdict": "ACCEPT 0/0",
            },
        },
        "role": (
            "Current recorded DR-126 C4-c application-grade TCB successor that makes the selector grammar governing (D-361). Dual ACCEPT 0/0. Dual gradeRuling SUSTAINED FOR APPLICATION. status CANDIDATE-NOT-APPLIED. binds NOTHING. selectorGrammar.standing GOVERNING. Selector values and per-OS profiles stay RESERVED. "
            "leftover-join.v10 of platform-tcb does not apply platform-tcb-contract.v48, does not complete C4-d, and does not choose a binds value reviewers have not granted. Not this artifact's version number."
        ),
    }
    b["contractV47"] = {
        "path": "docs/coop/artifacts/platform-tcb-contract.v47.json",
        "sha256": V47,
        "recording": "D-360",
        "reviews": {
            "claude": {
                "path": "docs/coop/artifacts/platform-tcb-contract.v47.review-independent.claude2.json",
                "sha256": V47_CLAUDE,
                "verdict": "ACCEPT 0/0",
            },
            "codex": {
                "path": "docs/coop/artifacts/platform-tcb-contract.v47.review-independent.codex.json",
                "sha256": V47_CODEX,
                "verdict": "ACCEPT 0/0",
            },
        },
        "role": (
            "Predecessor C4-c application-grade TCB successor candidate recorded at D-360. Dual ACCEPT 0/0. Dual gradeRuling SUSTAINED FOR APPLICATION. Does not make the TCB selector grammar governing. Historical after D-361. leftover-join.v10 of platform-tcb does not remasure platform-tcb-contract.v47 as a golden. Not this artifact's version number."
        ),
    }
    b["g22LeftoverJoinV5"] = {
        "path": "docs/coop/artifacts/g22-leftover-join.v5.json",
        "sha256": G22LJ5,
        "recording": "D-271",
        "reviews": {
            "claude": {
                "path": "docs/coop/artifacts/g22-leftover-join.v5.review-independent.claude2.json",
                "sha256": G22LJ5_CLAUDE,
                "verdict": "ACCEPT 0/0",
            },
            "codex": {
                "path": "docs/coop/artifacts/g22-leftover-join.v5.review-independent.codex.json",
                "sha256": G22LJ5_CODEX,
                "verdict": "ACCEPT 0/0",
            },
        },
        "role": (
            "Current G22 leftover remasurement recorded at D-271. leftoverDesign [OBL-G22-FX-AUTHORING]. leftover-join.v10 of platform-tcb does not steal that remainder and does not remasure leftover-join.v5 of G22 as a golden. leftover-join of G22 and leftover-join of platform-tcb are different lineages; their version numbers are unrelated. Not this artifact's version number."
        ),
    }
    b["leftoverJoinV45OfG21"] = {
        "path": "docs/coop/artifacts/g21-leftover-join.v45.json",
        "sha256": G21LJ45,
        "recording": "D-359",
        "role": (
            "Current recorded G21 leftover remasurement at D-359. leftover-join.v10 of platform-tcb does not remasure leftover-join.v45 of G21. leftover-join of G21 and leftover-join of platform-tcb are different lineages; their version numbers are unrelated. Not this artifact's version number."
        ),
    }
    b["leftoverJoinV14OfSarif"] = {
        "path": "docs/coop/artifacts/sarif-leftover-join.v14.json",
        "sha256": SARIF14,
        "recording": "D-347",
        "role": (
            "Current recorded DR-122 leftover remasurement at D-347. leftover-join.v10 of platform-tcb does not remasure leftover-join.v14 of sarif. leftover-join of sarif and leftover-join of platform-tcb are different lineages; their version numbers are unrelated. Not this artifact's version number."
        ),
    }

    obj["leftoverDesignOpenStanding"] = (
        "The live DR-126 token is OPEN. leftover-design of an unauthored T2-02 contract is stale as an authoring claim after platform-tcb-contract.v45 (D-125) and after platform-tcb-contract.v48 (D-361). "
        "leftover-design of an unauthored G22 specification is stale as an authoring claim after occupancy v2 (D-219). leftover-design of unnamed corpus classes is stale as a naming claim after g22-named-corpus-catalog.v1. "
        "leftover-design of G22 fixture implementations remains. leftover-design of reserved TCB tables and selector values remains: platform-tcb-contract.v48 makes the selector grammar governing and leaves selector values and per-OS profiles RESERVED. "
        "DR-126 is not SATISFIED. G22 is not QUALIFIED."
    )

    ri = obj["recordedInputs"]
    ri["docs/coop/COORDINATOR-DECISIONS.md"] = COORD
    ri["docs/v2/architecture/08-decision-and-readiness-register.md"] = FILE08
    ri["HEAD"] = HEAD
    ri["docs/coop/artifacts/platform-tcb-leftover-join.v9.json"] = V9_SHA
    ri["docs/coop/artifacts/platform-tcb-leftover-join.v9.review-independent.claude2.json"] = V9_CLAUDE
    ri["docs/coop/artifacts/platform-tcb-leftover-join.v9.review-independent.codex.json"] = V9_CODEX
    ri["docs/coop/artifacts/platform-tcb-contract.v48.json"] = V48
    ri["docs/coop/artifacts/platform-tcb-contract.v48.review-independent.claude2.json"] = V48_CLAUDE
    ri["docs/coop/artifacts/platform-tcb-contract.v48.review-independent.codex.json"] = V48_CODEX
    ri["docs/coop/artifacts/platform-tcb-contract.v47.json"] = V47
    ri["docs/coop/artifacts/g22-leftover-join.v5.json"] = G22LJ5
    ri["docs/coop/artifacts/g21-leftover-join.v45.json"] = G21LJ45
    ri["docs/coop/artifacts/sarif-leftover-join.v14.json"] = SARIF14

    obj["remeasurementClause"] = (
        "If a cited file moves in a way that is not append-only COORD growth or COORD heading hygiene, with file 08, leftover-join.v9 of platform-tcb, leftover-join.v8 of platform-tcb, leftover-join.v7 of platform-tcb, leftover-join.v6 of platform-tcb, occupancy v2, leftover-join.v5 of G22, platform-tcb-contract.v48, leftover-join.v45 of G21, leftover-join.v14 of sarif, and this draft unmoved, remasure before recording. "
        "recordedInputs.HEAD must equal the top-level head. leftover-join.v10 of platform-tcb does not unwrite D-086 or D-167 through D-361. "
        "Frozen leftover-join.v9 of platform-tcb remains the D-268 current recorded DR-126 leftover remasurement until a recordable successor is adopted. Frozen leftover-join.v8 of platform-tcb remains Dual REJECT CANDIDATE-NOT-APPLIED and is not current. Frozen occupancy v2 remains current G22 occupancy remasurement. Frozen leftover-join.v5 of G22 remains current G22 leftover remasurement."
    )

    for o in obj["obligations"]:
        if o["id"] == "OBL-CONTRACT-V45":
            o["reason"] = (
                "D-125 recorded platform-tcb-contract.v45 as DR-126's leftover T2-02 successor candidate at dual ACCEPT 0/0. D-360 recorded platform-tcb-contract.v47 as a C4-c successor candidate. D-361 recorded platform-tcb-contract.v48 as the C4-c successor that makes the selector grammar governing. "
                "Recording those candidates is not leftover-design of a new class and is not SATISFIED. leftover-join.v10 of platform-tcb does not apply platform-tcb-contract.v45, platform-tcb-contract.v47, or platform-tcb-contract.v48."
            )
        elif o["id"] == "OBL-G22-HARNESS-SPEC":
            o["reason"] = (
                "G22 is named (D-086) and occupancy remasurement v2 exists at harness.DR-G22.platform-abi-loader.v2 (D-219; dual ACCEPT 0/0; CANDIDATE-NOT-APPLIED; not QUALIFIED). Leftover-design of authoring that specification is therefore stale as an authoring claim. leftover-join.v6 of platform-tcb measured OBL-G22-HARNESS-SPEC leftoverDesign false. leftover-join.v10 of platform-tcb does not reopen that closure and does not execute G22."
            )
        elif o["id"] == "OBL-G22-NAMED-CATALOG":
            o["reason"] = (
                "g22-named-corpus-catalog.v1.json names the one live G22 occupancy namedCorpusNotAuthored class in order (Claude ACCEPT 0/0; Codex not reviewed; CANDIDATE-NOT-APPLIED; binds NOTHING). leftover-design of unnamed corpus classes is therefore stale as a naming claim. This obligation is not leftover-design of fixture implementations. leftover-join.v10 of platform-tcb does not close OBL-G22-FX-AUTHORING."
            )
        elif o["id"] == "OBL-G22-FX-AUTHORING":
            o["reason"] = (
                "Occupancy v2 namedCorpusNotAuthored carries one live harness-cell corpus class. Fixtures are unauthored. g22-named-corpus-catalog.v1 named that class; that naming is OBL-G22-NAMED-CATALOG, leftoverDesign false. The filesystem token of that class is the TCB filesystem selector; that axis is RESERVED and is OBL-RESERVED-TABLES, not a populated fixture set. leftover-join.v5 of G22 still measures OBL-G22-FX-AUTHORING leftoverDesign true. D-056 Decision clause 5: authoring fixtures remains design work. leftover-join.v10 of platform-tcb does not invent those fixture bytes, does not steal leftover-join.v5 of G22, and does not populate reserved TCB tables."
            )
        elif o["id"] == "OBL-G22-EXECUTION":
            o["reason"] = (
                "G22's live claim owns executed-closure use of only declared platform TCB dependencies. Execution remains qualification (D-056). leftover-join.v10 of platform-tcb does not execute fixtures and does not claim QUALIFIED."
            )
        elif o["id"] == "OBL-RESERVED-TABLES":
            o["reason"] = (
                "platform-tcb-contract.v48 (D-361) makes the selector grammar governing and leaves selector values and per-OS profiles RESERVED (D-314 item 9). D-341 assigned the DR-126 population packet to Security + release + platform owners; the packet remains a later different artifact. "
                "G22 leftoverNameNote and occupancy v2 fields keep per-OS tables, filesystem selectors, version/build selectors, ikconfigParserVectors, and NT-TCB-KEXEC RESERVED. filesystems.standing is RESERVED; matrixStanding is INCOMPLETE on the filesystem selector axis. versionOrBuildSelector.standing is RESERVED; requiredBeforeAllowlistFreeze remains true. "
                "platform-tcb-contract.v48 whatThisDoesNotDo includes 'Does not populate per-OS allowlist rows.' Making the selector grammar governing does not populate a table. Undecided tables and selector values are leftover-design (D-056). leftover-join.v10 of platform-tcb does not populate them, does not freeze an allowlist, and does not complete C4-d."
            )
        elif o["id"] == "OBL-ADVISORY-HONESTY":
            o["reason"] = (
                "D-125 records Claude advisories CLAUDE-V45-A1 / CLAUDE-V45-A2 / CLAUDE-V45-A3 and Claude D-000 advisory CLAUDE-D125-A1 travel as honesty work. D-361 recites CLAUDE-V47-A1 / CLAUDE-V47-A2 / CLAUDE-V47-A3 and CLAUDE-V48-A1 / CLAUDE-V48-A2 and CLAUDE-D361-A1 / CLAUDE-D361-A2 as advisories; they travel as honesty work. Honesty work is not leftover-design and is not SATISFIED. leftover-join.v10 of platform-tcb does not discharge them."
            )
        elif o["id"] == "OBL-G07-BOUNDARY":
            o["reason"] = (
                "platform-tcb-contract.v48 whatThisDoesNotDo includes 'Does not re-own archive extraction / symlink / TOCTOU (DR-G07).' G22 filesystems.notG07CoverageDomain: G07's supported-filesystems exact-bytes coverage domain is a different question. It is not leftover-design to close on DR-126. leftover-join.v10 of platform-tcb does not retarget G07."
            )

    obj["doesNotCloseLeftoverAlone"] = (
        "leftover-join.v10 of platform-tcb does not SATISFY DR-126 and does not make G22 QUALIFIED. OBL-G22-FX-AUTHORING and OBL-RESERVED-TABLES remain leftover-design. OBL-G22-NAMED-CATALOG naming is measured closed. Gates 2 and 3 do not hold. Class A is not opened. Not SATISFIED."
    )
    obj["proposedLaterWork"] = [
        "A later D-000 recording may pin leftover-join.v10 of platform-tcb. leftover-join.v10 of platform-tcb does not perform that recording.",
        "A later leftover-design cycle may author remaining G22 classes only where types are already closed. leftover-join.v10 of platform-tcb does not invent those bytes.",
        "D-341 assigned the DR-126 population packet to Security + release + platform owners. A later packet may supply filesystem and version/build selector values. leftover-join.v10 of platform-tcb does not populate those selectors and does not author that packet.",
        "A later dedicated SATISFIED-GRADE cycle may test DR-126 only when D-056 five gates hold. Gate 1 Class A remains unopened. leftover-join.v10 of platform-tcb is not that cycle.",
    ]
    obj["doesNot"] = [
        "Does not SATISFY DR-126.",
        "Does not open D-056 Class A.",
        "Does not close leftover-design.",
        "Does not close OBL-RESERVED-TABLES.",
        "Does not close OBL-G22-FX-AUTHORING.",
        "Does not drop advisory honesty.",
        "Does not populate a TCB table.",
        "Does not add a DR-G* row.",
        "Does not change live required-now 28.",
        "Does not apply platform-tcb-contract.v45.",
        "Does not apply platform-tcb-contract.v47.",
        "Does not apply platform-tcb-contract.v48.",
        "Does not complete C4-d.",
        "Does not choose a binds value reviewers have not granted.",
        "Does not execute fixtures.",
        "Does not author fixture bytes.",
        "Does not populate per-OS allowlist rows.",
        "Does not populate filesystem selectors or version/build selectors.",
        "Does not populate ikconfigParserVectors.",
        "Does not execute NT-TCB-KEXEC.",
        "Does not invent a D-006 unit.",
        "Does not put language-runtime/Node into the core TCB.",
        "Does not retarget G07.",
        "Does not edit file 08.",
        "Does not invent a D9 code or a section 7.1 recipe.",
        "Does not authorize docs/v2/implementation/.",
        "Does not discharge traveling honesty advisories.",
        "Does not occupy the identifier.",
        "Does not invent fixture bytes.",
        "Does not record occupancy v1 as current occupancy.",
        "Does not record leftover-join.v5 of platform-tcb as current DR-126 leftover-join.",
        "Does not record leftover-join.v6 of platform-tcb as current.",
        "Does not record leftover-join.v7 of platform-tcb as current.",
        "Does not record leftover-join.v7 of platform-tcb as Dual ACCEPT or Dual REJECT.",
        "Does not record leftover-join.v8 of platform-tcb as current.",
        "Does not record leftover-join.v8 of platform-tcb as Dual ACCEPT.",
        "Does not record leftover-join.v9 of platform-tcb as current after leftover-join.v10 of platform-tcb is recorded.",
        "Does not remasure leftover-join.v9 of platform-tcb as a golden.",
        "Does not remasure leftover-join.v5 of G22 as a golden.",
        "Does not remasure leftover-join.v45 of G21.",
        "Does not remasure leftover-join.v14 of sarif.",
        "Does not first-author prefix exactly at the operative bound.",
        "Does not re-land CLAUDE-PTLJ-V3-SF1.",
        "Does not re-land CLAUDE-PTLJ-V7-SF1.",
        "Does not re-land CLAUDE-PTLJ-V8-SF1.",
        "Does not re-land CODEX-PTLJ-V8-SF1.",
        "Does not collapse the DR-126 owner cell with the DR-G22 owner cell.",
    ]

    obj["findingDisposition"] = [
        {
            "id": "CLAUDE-PTLJ-V3-SF1",
            "severity": "SHOULD-FIX",
            "disposition": "ACCEPTED. Landed in this lineage at leftover-join.v5 of platform-tcb. leftover-join.v10 of platform-tcb does not re-land it.",
            "landedAt": [
                "artifact",
                "version",
                "basedOn.predecessorJoin.role",
                "basedOn.predecessorV1.role",
            ],
        },
        {
            "id": "CLAUDE-PTLJ-V7-SF1",
            "severity": "SHOULD-FIX",
            "disposition": "ACCEPTED. Landed in this lineage at leftover-join.v8 of platform-tcb. leftover-join.v10 of platform-tcb does not re-land it.",
            "landedAt": [
                "findingDisposition[0].disposition",
            ],
        },
        {
            "id": "CLAUDE-PTLJ-V8-SF1",
            "severity": "SHOULD-FIX",
            "disposition": "ACCEPTED. Landed in this lineage at leftover-join.v9 of platform-tcb. Shared class with CODEX-PTLJ-V8-SF1: predecessorV6.role leftover this-v7 speaker. Both identifiers are named. leftover-join.v9 of platform-tcb remasured predecessorV6.role to speaker-label leftover-join.v9 of platform-tcb. leftover-join.v10 of platform-tcb does not re-land it.",
            "landedAt": [
                "basedOn.predecessorV6.role",
            ],
        },
        {
            "id": "CODEX-PTLJ-V8-SF1",
            "severity": "SHOULD-FIX",
            "disposition": "ACCEPTED. Landed in this lineage at leftover-join.v9 of platform-tcb. Shared class with CLAUDE-PTLJ-V8-SF1. Both identifiers are named. leftover-join.v10 of platform-tcb does not invent a third identifier and does not re-land it.",
            "landedAt": [
                "basedOn.predecessorV6.role",
            ],
        },
    ]

    obj["parentReview"]["role"] = (
        "Independent dual ACCEPT 0/0 of the current occupancy of the already-named G22 identifier. leftover-join.v10 of platform-tcb is a DR-126 leftover remasurement. Naming parent of G22 is naming leftover-join.v6 of platform-tcb (D-145), not leftover-join.v8 of platform-tcb. D-086 named DR-G22."
    )

    text = json.dumps(obj, indent=2, ensure_ascii=False) + "\n"
    if SUBJECT.exists():
        os.chmod(SUBJECT, 0o644)
    SUBJECT.write_text(text)
    os.chmod(SUBJECT, 0o444)

    loaded = json.loads(SUBJECT.read_text())
    assert loaded["binds"] == "NOTHING"
    assert loaded["status"] == "CANDIDATE-NOT-APPLIED"
    assert loaded["version"] == 10
    assert loaded["summary"]["leftoverDesign"] == ["OBL-G22-FX-AUTHORING", "OBL-RESERVED-TABLES"]
    assert loaded["head"] == HEAD
    assert "This v10" not in text
    assert "This join" not in text
    assert "This leftover-join" not in text
    assert "This v9" not in text
    assert "ProductBuildVersion" not in text
    # historical landings must still name leftover-join.v9 of platform-tcb as the V8 landing
    assert "Landed in this lineage at leftover-join.v9 of platform-tcb" in text
    assert "Landed in this lineage at leftover-join.v5 of platform-tcb" in text
    assert "Landed in this lineage at leftover-join.v8 of platform-tcb" in text
    print("subject", sha256_file(SUBJECT), SUBJECT.stat().st_size, oct(SUBJECT.stat().st_mode)[-4:])
    print("ok")


if __name__ == "__main__":
    main()
