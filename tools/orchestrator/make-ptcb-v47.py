#!/usr/bin/env python3
"""Build platform-tcb-contract.v47: land Claude v46 grade reservation on macos-product-build."""
from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "docs/coop/artifacts"
V46 = ART / "platform-tcb-contract.v46.json"
SUBJECT = ART / "platform-tcb-contract.v47.json"
HEAD = "5a45ebf259a2f3094b18add549185223b0a80625"
COORD = "2c47bdb3909b454e8cad411e65d404d27627e079031f1961b7a8627a44237cf5"
FILE08 = "e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e"
FILE04 = "a74b451169382e1c8f855afb8f4eda2511fb74ec7ffa81c4e42d7b8118119e06"
D098 = "1be52e83df90b1ac7c02b0937cb62f861821b517c77c45905cda0dd7f4479a1b"


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> None:
    obj = json.loads(V46.read_text())
    obj["artifact"] = "platform-tcb-contract.v47"
    obj["version"] = 47
    obj["date"] = "2026-09-01"
    obj["authorityClaim"] = (
        "platform-tcb-contract.v47 PROPOSES the C4-c application-grade successor of platform-tcb-contract.v46 after D-359. It lands Claude v46 advisory CLAUDE-V46-A1 / gradeRuling reservationSweep on macos-product-build by quoting the recorded D-098 sw_vers observation family and excluding sw_vers -productVersion as the near neighbour, and by stating absent/unobservable refusal, without inventing a selector value. Selector values and per-OS profiles stay RESERVED. status CANDIDATE-NOT-APPLIED. binds NOTHING. sealRecommendation DO-NOT-SEAL. platform-tcb-contract.v47 applies nothing, does not populate per-OS package tables, does not re-own DR-G07 extraction, does not re-decide D-006 numbers, does not QUALIFY G22, does not open D-056 Class A, does not SATISFY DR-126, and does not authorize docs/v2/implementation/. DR-126 stays OPEN. G22 stays not QUALIFIED. Windows remains D-002 absent. Frozen platform-tcb-contract.v46 stays unrecorded. Frozen leftover-join.v45 of G21 remains the D-359 current recorded G21 leftover remasurement. Does not first-author prefix exactly at the operative bound."
    )
    obj["purpose"] = (
        "C4-c successor after D-359: land CLAUDE-V46-A1 on macos-product-build using only recorded D-098 observation-family quotes. Does not populate tables. Does not choose a binds value reviewers have not granted. Does not SATISFY DR-126. Does not open D-056 Class A. Does not first-author prefix exactly at the operative bound. Does not remasure leftover-join.v45 of G21. basedOn last-heading custody only: D-359."
    )
    obj["recordedInputs"]["governingSources"][2]["sha256"] = FILE08
    obj["recordedInputs"]["governingSources"][2]["role"] = "Live DR-126 and DR-G22 rows at D-359 HEAD."

    mp = obj["platformProfile"]["selectorGrammar"]["supportedVersionOrBuildSelector"]["identifierSchemes"]["macos-product-build"]
    mp["source"] = (
        "Observation CLI family recorded at coordinator-decisions.D-098.turn2.draft.md preflight: sw_vers. This scheme observes the macOS product-build string as Apple publishes it through that CLI family."
    )
    mp["notThisField"] = (
        "sw_vers -productVersion is not this field. That recorded D-098 preflight observes product version, the near neighbour, not the product-build string."
    )
    mp["absent"] = (
        "If the product-build string is unobservable, missing, or empty after Unicode NFC and trim of leading/trailing ASCII whitespace, the profile refuses. sw_vers -productVersion is not a substitute."
    )
    mp["normalization"] = "Unicode NFC and trim of leading/trailing ASCII whitespace. No case-fold."
    mp["canonicalIdentifier"] = {
        "serialization": "the NFC-then-trimmed product-build string",
        "equality": "byte-exact after this serialization",
        "normalizationReferent": "EXACT-BUILD.equality 'after normalization' means this scheme's named normalization followed by this serialization",
    }
    mp["notAdmitted"] = (
        "No second form. sw_vers -productVersion is not this scheme. uname is not this scheme."
    )

    pkt = obj["platformProfile"]["populationPacket"]
    obj["platformProfile"]["populationPacket"] = pkt.replace("platform-tcb-contract.v46", "platform-tcb-contract.v47")

    obj["whatThisDoesNotDo"].append(
        "Does not first-author prefix exactly at the operative bound."
    )
    obj["whatThisDoesNotDo"].append(
        "Does not invent an unrecorded macOS build-string key; the named interface is the recorded D-098 sw_vers observation family."
    )
    obj["whatThisDoesNotDo"].append(
        "Does not remasure leftover-join.v45 of G21."
    )
    obj["reviewGuidance"]["forTheIndependentReviewer"].extend(
        [
            "Attack any silent v46-to-v47 path outside basedOn.method.",
            "Attack a macos-product-build source that invents an unrecorded Apple key rather than quoting the recorded D-098 sw_vers family.",
            "Attack a binds value other than NOTHING, a status other than CANDIDATE-NOT-APPLIED, or a populated selector or per-OS table row.",
            "Attack SATISFY DR-126, QUALIFY G22, open D-056 Class A, invent Windows, first-author prefix exactly at the operative bound, or treat C4-d as this successor.",
            "Do not mark DR-126 SATISFIED. Answer the D-005-form grade question in top-level gradeRuling. Answering SUSTAINED FOR APPLICATION does not open Class A and marks nothing SATISFIED.",
        ]
    )

    obj["basedOn"] = {
        "predecessor": "docs/coop/artifacts/platform-tcb-contract.v46.json",
        "sha256": "b2b4a08741d179bd9046e4ebb0f1d2c26ebb3892c7df890c6a1da84734658b15",
        "method": (
            "v47 is v46 with targeted C4-c succession after D-359 landing CLAUDE-V46-A1. Closed roster: /artifact, /version, /date, /authorityClaim, /purpose, /recordedInputs/governingSources[2]/sha256, /recordedInputs/governingSources[2]/role, /platformProfile/selectorGrammar/supportedVersionOrBuildSelector/identifierSchemes/macos-product-build, /platformProfile/populationPacket, /whatThisDoesNotDo (append), /reviewGuidance/forTheIndependentReviewer (append), /basedOn, /appliesFindingsOf/claude2v46, /appliesFindingsOf/codexv46, /appliesFindingsOf/idCollisionNote (append v45 and v46 sentences), /reMeasurementAtV46/standing, /reMeasurementAtV46/note, /reMeasurementAtV47. status remains CANDIDATE-NOT-APPLIED. reviewStatus remains AWAITING-INDEPENDENT-REVIEW. sealRecommendation remains DO-NOT-SEAL. binds remains NOTHING. platform-tcb-contract.v47 does not choose a binds value reviewers have not granted. Every path neither the roster nor succession metadata names load-equals the same path on platform-tcb-contract.v46. Standing rule: whenever a new remasurement block is added, the prior LIVE block is named on this roster because it is demoted. slice1ProfileStems stay RESERVED. identityRuleShape.populatedTables stays RESERVED as G22 qualification evidence. taxonomy load-equals platform-tcb-contract.v46. g22.ikconfigParserVectors stays RESERVED as G22 evidence. whatThisDoesNotDo[1] remains 'Does not populate per-OS allowlist rows.' Claude v46 ACCEPT 0/0 with advisories CLAUDE-V46-A1 CLAUDE-V46-A2 CLAUDE-V46-A3 and gradeRuling NOT SUSTAINED; Codex v46 ACCEPT 0/0 gradeRuling SUSTAINED FOR APPLICATION. CLAUDE-V46-A1 lands at macos-product-build source / notThisField / absent / normalization / canonicalIdentifier / notAdmitted quoting D-098 sw_vers and excluding sw_vers -productVersion. Does not SATISFY DR-126. Does not open D-056 Class A. Does not QUALIFY G22. Does not first-author prefix exactly at the operative bound. Windows remains D-002 absent. Last-heading custody is D-359."
        ),
    }

    note = obj["appliesFindingsOf"]["idCollisionNote"]
    obj["appliesFindingsOf"]["idCollisionNote"] = note + (
        " Claude v45 used CLAUDE-V45-A1/A2/A3; Codex v45 used no findings (ACCEPT 0/0). Claude v46 used CLAUDE-V46-A1/A2/A3; Codex v46 used no findings (ACCEPT 0/0)."
    )
    obj["appliesFindingsOf"]["claude2v46"] = {
        "path": "docs/coop/artifacts/platform-tcb-contract.v46.review-independent.claude2.json",
        "sha256": "927b43af7f9220be4b36ac59b6f56b31ef0f5c7c23f9a73ea1addce9e8cddb29",
        "verdict": "ACCEPT",
        "blockers": [],
        "shouldFix": [],
        "advisories": ["CLAUDE-V46-A1", "CLAUDE-V46-A2", "CLAUDE-V46-A3"],
        "gradeRuling": "NOT SUSTAINED",
        "qualifiedIds": {},
    }
    obj["appliesFindingsOf"]["codexv46"] = {
        "path": "docs/coop/artifacts/platform-tcb-contract.v46.review-independent.codex.json",
        "sha256": "996fe0d22e811ab4603c629415832cf88d260a6a955f45b151450397a5bdf101",
        "verdict": "ACCEPT",
        "blockers": [],
        "shouldFix": [],
        "advisories": [],
        "gradeRuling": "SUSTAINED FOR APPLICATION",
    }

    obj["reMeasurementAtV46"]["standing"] = "HISTORICAL-AT-V46"
    obj["reMeasurementAtV46"]["note"] = (
        "HISTORICAL-AT-V46. Not this-generation live. Live digest is the remasurement block whose standing is LIVE. Does not SATISFY DR-126."
    )
    obj["reMeasurementAtV47"] = {
        "docs/coop/COORDINATOR-DECISIONS.md": COORD,
        "docs/v2/architecture/08-decision-and-readiness-register.md": FILE08,
        "docs/v2/architecture/04-lifecycle-delivery-and-operations.md": FILE04,
        "docs/coop/artifacts/coordinator-decisions.D-098.turn2.draft.md": D098,
        "measuredAtHead": HEAD,
        "note": "This is the only this-generation live COORD claim (standing LIVE). Remeasured after D-359. Append-only COORD after this remasurement, with file 08 and this subject unmoved, is PASS-NO-SCOPE-EFFECT. Does not SATISFY DR-126. Does not open D-056 Class A. Does not first-author prefix exactly at the operative bound.",
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
    assert loaded["version"] == 47
    mp = loaded["platformProfile"]["selectorGrammar"]["supportedVersionOrBuildSelector"]["identifierSchemes"]["macos-product-build"]
    assert "sw_vers -productVersion is not this field" in mp["notThisField"]
    assert "ProductBuildVersion" not in text
    assert "This v47" not in text
    print("ok")


if __name__ == "__main__":
    main()
