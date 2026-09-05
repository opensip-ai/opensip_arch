#!/usr/bin/env python3
"""Build platform-tcb-contract.v48: C4-c grammar-governing successor after D-360."""
from __future__ import annotations

import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "docs/coop/artifacts"
V47 = ART / "platform-tcb-contract.v47.json"
SUBJECT = ART / "platform-tcb-contract.v48.json"
HEAD = "d5d52aae3d21b94c4dd100379bdc22db5131f504"
COORD = "6f47306805b8eb7f6ff201a13e3995251b19ed0c51e316809a0f460320324b89"
FILE08 = "e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e"
FILE04 = "a74b451169382e1c8f855afb8f4eda2511fb74ec7ffa81c4e42d7b8118119e06"
D098_T2 = "1be52e83df90b1ac7c02b0937cb62f861821b517c77c45905cda0dd7f4479a1b"
D098_T3 = "5ad6884a06aa450bc2cbc0f286b3366eb9e029922e92a0ae6937868e37e05031"
V47_SHA = "44229ea1f23a6af743fac6c1dcfd9b0d069100dad9991ef86449ee179c4dfe97"
CLAUDE_V47 = "c68b790630178ff795f49abcac0f39a882f875e23e221b1c0cc1317a2da34031"
CODEX_V47 = "1df157780b71a6452d917dc5d8bc7a2ea136416ec1aca98163dc63832ff428da"


def sha256_file(p: Path) -> str:
    import hashlib

    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> None:
    obj = json.loads(V47.read_text())
    obj["artifact"] = "platform-tcb-contract.v48"
    obj["version"] = 48
    obj["date"] = "2026-09-01"
    obj["authorityClaim"] = (
        "platform-tcb-contract.v48 PROPOSES the C4-c application-grade successor of platform-tcb-contract.v47 after D-360. "
        "It authors selectorGrammar.standing GOVERNING, quoting D-293 Decision 6 (an application-grade TCB successor that makes the grammar governing) and the recorded GOVERNING vocabulary already used by vectorRosterRule and hexEncodingRule. "
        "Selector values and per-OS profiles stay RESERVED (D-314 item 9 / Q5 named, not answered). "
        "status CANDIDATE-NOT-APPLIED. binds NOTHING. sealRecommendation DO-NOT-SEAL. "
        "D-293 does not state a binds value. platform-tcb-contract.v48 does not choose a binds value reviewers have not granted. "
        "Making the selector grammar governing is not applying the contract, not SATISFYING DR-126, not QUALIFYING G22, not opening D-056 Class A, and not C4-d. "
        "It lands Claude v47 advisories CLAUDE-V47-A1, CLAUDE-V47-A2, and CLAUDE-V47-A3 as honesty work. "
        "platform-tcb-contract.v48 applies nothing, does not populate per-OS package tables, does not re-own DR-G07 extraction, does not re-decide D-006 numbers, and does not authorize docs/v2/implementation/. "
        "DR-126 stays OPEN. G22 stays not QUALIFIED. Windows remains D-002 absent. "
        "Frozen platform-tcb-contract.v47 remains the D-360 recorded DR-126 C4-c application-grade TCB successor candidate. "
        "Frozen leftover-join.v45 of G21 remains the D-359 current recorded G21 leftover remasurement. "
        "Frozen leftover-join.v14 of sarif remains the D-347 current recorded DR-122 leftover remasurement. "
        "Frozen platform-tcb leftover-join.v9 remains the D-268 current recorded DR-126 leftover remasurement. "
        "Does not first-author prefix exactly at the operative bound."
    )
    obj["purpose"] = (
        "C4-c successor after D-360: author selectorGrammar.standing GOVERNING; land CLAUDE-V47-A1 on D-098 CONTESTED citation standing and the turn-3 draft's deletion of the bare sw_vers preflight item; land CLAUDE-V47-A2 by stating the closed roster is a permission list; land CLAUDE-V47-A3 by adding standing on reMeasurementAtV2 through reMeasurementAtV5. "
        "Does not populate tables. Does not choose a binds value reviewers have not granted. Does not SATISFY DR-126. Does not open D-056 Class A. Does not complete C4-d. "
        "Does not first-author prefix exactly at the operative bound. Does not remasure leftover-join.v45 of G21. Does not remasure leftover-join.v14 of sarif. "
        "basedOn last-heading custody only: D-360."
    )
    obj["recordedInputs"]["governingSources"][2]["sha256"] = FILE08
    obj["recordedInputs"]["governingSources"][2]["role"] = "Live DR-126 and DR-G22 rows at D-360 HEAD."

    sg = obj["platformProfile"]["selectorGrammar"]
    new_sg = {"standing": "GOVERNING"}
    new_sg.update(sg)
    obj["platformProfile"]["selectorGrammar"] = new_sg

    mp = obj["platformProfile"]["selectorGrammar"]["supportedVersionOrBuildSelector"]["identifierSchemes"]["macos-product-build"]
    mp["citationStanding"] = (
        "D-098 is CONTESTED, not adopted. COORD heading ## D-098 records Status CONTESTED after three turns under D-000 clause 2. Not adopted. No forced consensus. Parked. File 08 not edited. "
        "The D-098 turn-2 draft is provenance against invention, not delegated authority, matching how this lineage annotates borrowed pins (INHERITED-V1-AUTHORING-PIN on governingSources[1]; HISTORICAL-AT-VN and LIVE on remasurement blocks)."
    )
    mp["turn3Draft"] = (
        "coordinator-decisions.D-098.turn3.draft.md deleted the bare sw_vers preflight item. "
        "The family token sw_vers remains in that turn-3 draft only inside sw_vers -productVersion, which this scheme excludes. "
        "The observation CLI family named by source remains sw_vers as recorded on both the turn-2 draft and the turn-3 draft."
    )

    pkt = obj["platformProfile"]["populationPacket"]
    obj["platformProfile"]["populationPacket"] = pkt.replace("platform-tcb-contract.v47", "platform-tcb-contract.v48")

    obj["whatThisDoesNotDo"].append(
        "Does not treat selectorGrammar.standing GOVERNING as a binds value, as SATISFIED, or as QUALIFIED."
    )
    obj["whatThisDoesNotDo"].append(
        "Does not remasure leftover-join.v14 of sarif."
    )
    obj["reviewGuidance"]["forTheIndependentReviewer"].extend(
        [
            "Attack any silent v47-to-v48 path outside basedOn.method.",
            "Attack a selectorGrammar.standing other than GOVERNING, or a claim that GOVERNING on the grammar populates a selector value.",
            "Attack D-098 cited as adopted, or an unrecorded Apple key invented.",
            "Attack reMeasurementAtV2 through reMeasurementAtV5 still carrying no standing field.",
            "Attack a binds value other than NOTHING, a status other than CANDIDATE-NOT-APPLIED, or a populated selector or per-OS table row.",
            "Attack SATISFY DR-126, QUALIFY G22, open D-056 Class A, invent Windows, first-author prefix exactly at the operative bound, or treat C4-d as this successor.",
            "Do not mark DR-126 SATISFIED. Answer the D-005-form grade question in top-level gradeRuling. Answering SUSTAINED FOR APPLICATION does not open Class A and marks nothing SATISFIED.",
        ]
    )

    obj["basedOn"] = {
        "predecessor": "docs/coop/artifacts/platform-tcb-contract.v47.json",
        "sha256": V47_SHA,
        "method": (
            "v48 is v47 with targeted C4-c succession after D-360. Closed roster: /artifact, /version, /date, /authorityClaim, /purpose, "
            "/recordedInputs/governingSources[2]/sha256, /recordedInputs/governingSources[2]/role, "
            "/platformProfile/selectorGrammar/standing, "
            "/platformProfile/selectorGrammar/supportedVersionOrBuildSelector/identifierSchemes/macos-product-build/citationStanding, "
            "/platformProfile/selectorGrammar/supportedVersionOrBuildSelector/identifierSchemes/macos-product-build/turn3Draft, "
            "/platformProfile/populationPacket, /whatThisDoesNotDo (append), /reviewGuidance/forTheIndependentReviewer (append), "
            "/basedOn, /appliesFindingsOf/claude2v47, /appliesFindingsOf/codexv47, /appliesFindingsOf/idCollisionNote (append v47 sentence), "
            "/reMeasurementAtV2/standing, /reMeasurementAtV2/note, /reMeasurementAtV3/standing, /reMeasurementAtV3/note, "
            "/reMeasurementAtV4/standing, /reMeasurementAtV4/note, /reMeasurementAtV5/standing, /reMeasurementAtV5/note, "
            "/reMeasurementAtV47/standing, /reMeasurementAtV47/note, /reMeasurementAtV48. "
            "The closed roster is a permission list, not an exact-delta assertion (CLAUDE-V47-A2). Naming a held-still path is settled lineage practice. "
            "status remains CANDIDATE-NOT-APPLIED. reviewStatus remains AWAITING-INDEPENDENT-REVIEW. sealRecommendation remains DO-NOT-SEAL. binds remains NOTHING. "
            "platform-tcb-contract.v48 does not choose a binds value reviewers have not granted. "
            "Every path neither the roster nor succession metadata names load-equals the same path on platform-tcb-contract.v47. "
            "Standing rule: whenever a new remasurement block is added, the prior LIVE block is named on this roster because it is demoted. "
            "slice1ProfileStems stay RESERVED. identityRuleShape.populatedTables stays RESERVED as G22 qualification evidence. taxonomy load-equals platform-tcb-contract.v47. "
            "g22.ikconfigParserVectors stays RESERVED as G22 evidence. whatThisDoesNotDo[1] remains 'Does not populate per-OS allowlist rows.' "
            "Claude v47 ACCEPT 0/0 with advisories CLAUDE-V47-A1 CLAUDE-V47-A2 CLAUDE-V47-A3 and gradeRuling SUSTAINED FOR APPLICATION; Codex v47 ACCEPT 0/0 gradeRuling SUSTAINED FOR APPLICATION. "
            "CLAUDE-V47-A1 lands at macos-product-build citationStanding / turn3Draft quoting COORD ## D-098 CONTESTED and the turn-3 draft's deletion of the bare sw_vers preflight item. "
            "CLAUDE-V47-A2 lands in this method sentence: the roster is a permission list. "
            "CLAUDE-V47-A3 lands at reMeasurementAtV2 through reMeasurementAtV5 standing HISTORICAL-AT-VN. "
            "selectorGrammar.standing is GOVERNING. Does not SATISFY DR-126. Does not open D-056 Class A. Does not QUALIFY G22. Does not complete C4-d. "
            "Does not first-author prefix exactly at the operative bound. Windows remains D-002 absent. Last-heading custody is D-360."
        ),
    }

    note = obj["appliesFindingsOf"]["idCollisionNote"]
    obj["appliesFindingsOf"]["idCollisionNote"] = note + (
        " Claude v47 used CLAUDE-V47-A1/A2/A3; Codex v47 used no findings (ACCEPT 0/0)."
    )
    obj["appliesFindingsOf"]["claude2v47"] = {
        "path": "docs/coop/artifacts/platform-tcb-contract.v47.review-independent.claude2.json",
        "sha256": CLAUDE_V47,
        "verdict": "ACCEPT",
        "blockers": [],
        "shouldFix": [],
        "advisories": ["CLAUDE-V47-A1", "CLAUDE-V47-A2", "CLAUDE-V47-A3"],
        "gradeRuling": "SUSTAINED FOR APPLICATION",
        "reservationSweep": [],
    }
    obj["appliesFindingsOf"]["codexv47"] = {
        "path": "docs/coop/artifacts/platform-tcb-contract.v47.review-independent.codex.json",
        "sha256": CODEX_V47,
        "verdict": "ACCEPT",
        "blockers": [],
        "shouldFix": [],
        "advisories": [],
        "gradeRuling": "SUSTAINED FOR APPLICATION",
        "reservationSweep": [],
    }

    hist_note = (
        "HISTORICAL-AT-V{n}. Not this-generation live. Live digest is the remasurement block whose standing is LIVE. Does not SATISFY DR-126."
    )
    for n in (2, 3, 4, 5):
        block = obj[f"reMeasurementAtV{n}"]
        block["note"] = hist_note.format(n=n)
        block["standing"] = f"HISTORICAL-AT-V{n}"

    obj["reMeasurementAtV47"]["standing"] = "HISTORICAL-AT-V47"
    obj["reMeasurementAtV47"]["note"] = (
        "HISTORICAL-AT-V47. Not this-generation live. Live digest is the remasurement block whose standing is LIVE. Does not SATISFY DR-126."
    )
    obj["reMeasurementAtV48"] = {
        "docs/coop/COORDINATOR-DECISIONS.md": COORD,
        "docs/v2/architecture/08-decision-and-readiness-register.md": FILE08,
        "docs/v2/architecture/04-lifecycle-delivery-and-operations.md": FILE04,
        "docs/coop/artifacts/coordinator-decisions.D-098.turn2.draft.md": D098_T2,
        "docs/coop/artifacts/coordinator-decisions.D-098.turn3.draft.md": D098_T3,
        "measuredAtHead": HEAD,
        "note": "This is the only this-generation live COORD claim (standing LIVE). Remeasured after D-360. Append-only COORD after this remasurement, with file 08 and this subject unmoved, is PASS-NO-SCOPE-EFFECT. Does not SATISFY DR-126. Does not open D-056 Class A. Does not first-author prefix exactly at the operative bound.",
        "standing": "LIVE",
    }

    text = json.dumps(obj, indent=2, ensure_ascii=False) + "\n"
    if SUBJECT.exists():
        os.chmod(SUBJECT, 0o644)
    SUBJECT.write_text(text)
    os.chmod(SUBJECT, 0o444)
    print("subject", sha256_file(SUBJECT), SUBJECT.stat().st_size, oct(SUBJECT.stat().st_mode)[-4:])
    loaded = json.loads(SUBJECT.read_text())
    assert loaded["binds"] == "NOTHING"
    assert loaded["status"] == "CANDIDATE-NOT-APPLIED"
    assert loaded["version"] == 48
    assert loaded["platformProfile"]["selectorGrammar"]["standing"] == "GOVERNING"
    for n in (2, 3, 4, 5):
        assert loaded[f"reMeasurementAtV{n}"]["standing"] == f"HISTORICAL-AT-V{n}"
    assert loaded["reMeasurementAtV47"]["standing"] == "HISTORICAL-AT-V47"
    assert loaded["reMeasurementAtV48"]["standing"] == "LIVE"
    mp = loaded["platformProfile"]["selectorGrammar"]["supportedVersionOrBuildSelector"]["identifierSchemes"]["macos-product-build"]
    assert "CONTESTED" in mp["citationStanding"]
    assert "turn3" in mp["turn3Draft"]
    assert "ProductBuildVersion" not in text
    assert "This v48" not in text
    assert "This leftover-join" not in text
    assert "This join" not in text
    print("ok")


if __name__ == "__main__":
    main()
