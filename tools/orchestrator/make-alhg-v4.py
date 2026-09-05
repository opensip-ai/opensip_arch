#!/usr/bin/env python3
"""Build anti-lockstep-hostile-goldens.v4: per-D-002-platform copies of D-300 citation files."""
from __future__ import annotations

import copy
import hashlib
import json
import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "docs/coop/artifacts"
V3 = ART / "anti-lockstep-hostile-goldens.v3.json"
SUBJECT = ART / "anti-lockstep-hostile-goldens.v4.json"
SRC_DIR = ART / "fixtures/anti-lockstep-goldens.v1"
DST_ROOT = ART / "fixtures/anti-lockstep-goldens.v2"

HEAD = "f7a98a70e650d0ed2639f815fa932bff21a99b83"
COORD = "bae06532b8417800414ee4fbdcd980135365185ce88b2244f92f6767412f264f"
FILE08 = "e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e"
V3_SHA = "8be1b6c59515d0e00aff5fe0de584d0ab1aabbdf3091bf878e3258a1c639fd31"
V3_CLAUDE = "e060c52771821de5fdc9438600781b21999ef1a9b7b1cb98c827ac6b06439cb6"
V3_CODEX = "753dfeb7981f8cd008a1e73f77417f6bcd27ffcaecc0498f078cbf52d9685b03"
LJ6 = "bebf1103b8640b6c9e4e0adb7dc7bca9fef1e6857df6b6f03eb6c05eafb134af"
LJ6_CLAUDE = "6a3d1a2a1ddd074129c6b3b8cafcd764062ddba6a3ea9c5ca4a07073572d25c7"
LJ6_CODEX = "ad44a6d8f07a549ab20a21c8ec00a088b9da3ce54639e791ca3520de1dcd8fbf"
G21LJ45 = "f63925a912cfd97e3cc15fe27987321b2766f7bc28684da6f530e0a7fa1734cc"
SARIF14 = "8ecea58e0b6823968ebffbbe75640ba3473446985047fd709e308a4a7e40bf97"
PTCBLJ11 = "31f945ec892b6647c8d1ae2ac104905750502ffa54c2918b352e5ecdc89fa8d8"
G10 = "b0cbce06487b96bbe7f6af1dae62ba3b3ca55aaa41305cb96f531099e86bf7c9"
G23 = "f48ba637bdf193785c05906a1686ce268b27b6ce7355de07fa5effefdd84fb0b"

PLATFORMS = ["macos/arm64", "macos/x86_64", "linux/x86_64", "linux/arm64"]
SPEAKER = "anti-lockstep-hostile-goldens.v4"


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def plat_dir(p: str) -> str:
    return p.replace("/", "-")


def main() -> None:
    src_files = sorted(SRC_DIR.glob("HG.*.bin"))
    assert len(src_files) == 16, len(src_files)
    copies_by_name = {}
    for src in src_files:
        digest = sha256_file(src)
        copies = []
        for plat in PLATFORMS:
            dest_dir = DST_ROOT / plat_dir(plat)
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest = dest_dir / src.name
            shutil.copyfile(src, dest)
            os.chmod(dest, 0o444)
            assert sha256_file(dest) == digest
            copies.append(
                {
                    "platform": plat,
                    "path": str(dest.relative_to(ROOT)),
                    "sha256": digest,
                }
            )
        copies_by_name[src.name] = {"sha256": digest, "copies": copies}

    obj = copy.deepcopy(json.loads(V3.read_text()))
    obj["artifact"] = SPEAKER
    obj["version"] = 4
    obj["date"] = "2026-09-01"
    obj["head"] = HEAD
    obj["file08Pin"]["sha256"] = FILE08
    obj["requiredNowUnchanged"] = 28
    obj["status"] = "CANDIDATE-NOT-APPLIED"
    obj["reviewStatus"] = "AWAITING-INDEPENDENT-REVIEW"
    obj["sealRecommendation"] = "DO-NOT-SEAL"
    obj["binds"] = "NOTHING"

    obj["registerRowNote"] = (
        "registerRow is the architecture row DR-127 because anti-lockstep-hostile-goldens.v4 authors leftover-design of per-D-002-platform copies of the sixteen D-300 citation implementations. "
        "file08StatusToken is DR-127's own live token (OPEN). There is no DR-G* occupancy. leftover-join.v6 of anti-lockstep remains the current recorded DR-127 leftover remasurement (D-326). "
        "anti-lockstep-hostile-goldens.v4 does not remasure leftover-join.v6 of anti-lockstep, does not remasure leftover-join.v45 of G21, does not remasure leftover-join.v14 of sarif, does not steal G21 leftover remaining on leftover-join.v45 of G21, and does not SATISFY DR-127. "
        "Frozen anti-lockstep-hostile-goldens.v3 stays unmoved. Frozen fixtures/anti-lockstep-goldens.v1/ stays unmoved. Frozen leftover-join.v6 of anti-lockstep remains the current recorded DR-127 leftover remasurement until a recordable successor is adopted."
    )
    obj["authorityClaim"] = (
        "anti-lockstep-hostile-goldens.v4 PROPOSES leftover-design per-D-002-platform copies of the sixteen D-300 citation implementations under fixtures/anti-lockstep-goldens.v1/. "
        "The four D-002 tokens copied onto are quoted from harness.DR-G10.provider-conformance.ts-major-1.v2 #$.platforms, ORDERED-EQUAL against harness.DR-G23.provider-well-formed-admission.preview.v2. "
        "Each copy's sha256 equals the corresponding fixtures/anti-lockstep-goldens.v1/ digest, recomputed from disk. The warrant is D-293 Decision 8. D-314 G3-HOSTILE leaves the seven live v3 within-class universal sets including CC-6 named-open and supplies no per-class totals; anti-lockstep-hostile-goldens.v4 does not author those sets. "
        "anti-lockstep-hostile-goldens.v4 does not invent a D-002 platform list and does not copy onto Windows. It does not mutate fixtures/anti-lockstep-goldens.v1/. It does not first-author prefix exactly at the operative bound. "
        "leftoverDesignClosedIfAcceptedAndRecorded []. leftoverDesign remains [OBL-HOSTILE-GOLDENS, OBL-AL3-CORE-ROLLBACK, OBL-AL1-AL2-AL5]. "
        "anti-lockstep-hostile-goldens.v4 does not SATISFY DR-127. It does not remasure leftover-join.v6 of anti-lockstep. It does not remasure leftover-join.v45 of G21. It does not remasure leftover-join.v14 of sarif. It applies nothing and does not authorize docs/v2/implementation/."
    )
    obj["purpose"] = (
        "Author per-D-002-platform copies of the sixteen D-300 citation implementations after D-362. leftoverDesignClosedIfAcceptedAndRecorded []. basedOn.d362.role is the sole last-heading claimant. proposedLaterWork[0] names anti-lockstep-hostile-goldens.v4. "
        "Do not SATISFY DR-127. Do not remasure leftover-join.v6 of anti-lockstep. Do not remasure leftover-join.v45 of G21. Do not remasure leftover-join.v14 of sarif. Do not remasure leftover-join.v11 of platform-tcb. "
        "Do not author the seven named-open within-class universal sets. Do not invent a per-class total. Do not first-author prefix exactly at the operative bound. Do not copy onto Windows. Do not invent a D-002 platform list. "
        "Do not measure leftover-design of these copies stale as an authoring claim. Do not mutate fixtures/anti-lockstep-goldens.v1/. Do not record anti-lockstep-hostile-goldens.v1 or anti-lockstep-hostile-goldens.v2 or anti-lockstep-hostile-goldens.v3 as current after anti-lockstep-hostile-goldens.v4 is recorded."
    )

    obj["basedOn"]["d362"] = {
        "recording": "D-362",
        "commit": HEAD,
        "role": (
            "Last live heading at dispatch. Last-heading custody only. Recorded leftover-join.v11 of platform-tcb as DR-126 leftover remasurement. leftoverDesign [OBL-G22-FX-AUTHORING, OBL-RESERVED-TABLES]. "
            "anti-lockstep-hostile-goldens.v4 does not remasure leftover-join.v11 of platform-tcb, does not remasure leftover-join.v45 of G21, and does not remasure leftover-join.v14 of sarif."
        ),
    }
    obj["basedOn"]["d299"]["role"] = (
        "Not last-heading. Last-heading custody remains D-362. Recorded g19-fixture-corpus.v2 as DR-G19 leftover-design fixture implementations. anti-lockstep-hostile-goldens.v4 does not remasure leftover-join of G19."
    )
    obj["basedOn"]["leftoverJoinV3"]["role"] = (
        "Predecessor DR-127 leftover remasurement recorded at D-186. leftoverDesign [OBL-HOSTILE-GOLDENS, OBL-AL3-CORE-ROLLBACK, OBL-AL1-AL2-AL5]. Dual ACCEPT 0/0. Historical after D-326. Current recorded DR-127 leftover remasurement is leftover-join.v6 of anti-lockstep (D-326). anti-lockstep-hostile-goldens.v4 does not remasure leftover-join.v3 of anti-lockstep. Not this artifact's version number."
    )
    obj["basedOn"]["leftoverJoinV6"] = {
        "path": "docs/coop/artifacts/anti-lockstep-leftover-join.v6.json",
        "sha256": LJ6,
        "recording": "D-326",
        "reviews": {
            "claude": {
                "path": "docs/coop/artifacts/anti-lockstep-leftover-join.v6.review-independent.claude2.json",
                "sha256": LJ6_CLAUDE,
                "verdict": "ACCEPT 0/0",
            },
            "codex": {
                "path": "docs/coop/artifacts/anti-lockstep-leftover-join.v6.review-independent.codex.json",
                "sha256": LJ6_CODEX,
                "verdict": "ACCEPT 0/0",
            },
        },
        "role": (
            "Current recorded DR-127 leftover remasurement at D-326. leftoverDesign [OBL-HOSTILE-GOLDENS, OBL-AL3-CORE-ROLLBACK, OBL-AL1-AL2-AL5]. Dual ACCEPT 0/0. remainingNotAuthored includes per-platform copies. "
            "anti-lockstep-hostile-goldens.v4 does not remasure leftover-join.v6 of anti-lockstep and does not close leftover-design. leftover-join of anti-lockstep and anti-lockstep-hostile-goldens are different lineages; their version numbers are unrelated. Not this artifact's version number."
        ),
    }
    obj["basedOn"]["leftoverJoinV45OfG21"] = {
        "path": "docs/coop/artifacts/g21-leftover-join.v45.json",
        "sha256": G21LJ45,
        "recording": "D-359",
        "role": (
            "Current recorded G21 leftover remasurement at D-359. leftover-join.v45 of G21 leftoverDesign [OBL-G21-FX-AUTHORING]. anti-lockstep-hostile-goldens.v4 does not remasure leftover-join.v45 of G21 and does not steal G21 leftover. Not this artifact's version number."
        ),
    }
    obj["basedOn"]["leftoverJoinV14OfSarif"] = {
        "path": "docs/coop/artifacts/sarif-leftover-join.v14.json",
        "sha256": SARIF14,
        "recording": "D-347",
        "role": (
            "Current recorded DR-122 leftover remasurement at D-347. anti-lockstep-hostile-goldens.v4 does not remasure leftover-join.v14 of sarif. Not this artifact's version number."
        ),
    }
    obj["basedOn"]["predecessorV3"] = {
        "path": "docs/coop/artifacts/anti-lockstep-hostile-goldens.v3.json",
        "sha256": V3_SHA,
        "recording": "D-300",
        "reviews": {
            "claude": {
                "path": "docs/coop/artifacts/anti-lockstep-hostile-goldens.v3.review-independent.claude2.json",
                "sha256": V3_CLAUDE,
                "verdict": "ACCEPT 0/0",
            },
            "codex": {
                "path": "docs/coop/artifacts/anti-lockstep-hostile-goldens.v3.review-independent.codex.json",
                "sha256": V3_CODEX,
                "verdict": "ACCEPT 0/0",
            },
        },
        "role": (
            "Predecessor first-authoring of the sixteen citation implementations recorded at D-300. Dual ACCEPT 0/0. leftover-design of those sixteen implementations is remasured stale as an authoring claim by leftover-join.v6 of anti-lockstep (D-326). Frozen fixtures/anti-lockstep-goldens.v1/ stays unmoved. anti-lockstep-hostile-goldens.v4 copies those bytes onto quoted G10 occupancy v2 platforms and does not remasure anti-lockstep-hostile-goldens.v3. Not this artifact's version number."
        ),
    }
    if "g21LeftoverJoinV13" in obj["basedOn"]:
        obj["basedOn"]["g21LeftoverJoinV13"]["role"] = (
            "Predecessor G21 leftover remasurement. Historical. Current recorded G21 leftover remasurement is leftover-join.v45 of G21 (D-359). anti-lockstep-hostile-goldens.v4 does not remasure leftover-join.v45 of G21 and does not steal G21 leftover. Not this artifact's version number."
        )

    for m in obj["authoredCatalog"]["members"]:
        name = Path(m["path"]).name
        info = copies_by_name[name]
        assert m["sha256"] == info["sha256"]
        m["sourcePayload"] = {"path": m["path"], "sha256": m["sha256"]}
        m["copies"] = info["copies"]

    obj["whatIsAuthored"] = (
        "Sixty-four platform-indexed copies of the sixteen D-300 citation implementations. Platforms are harness.DR-G10.provider-conformance.ts-major-1.v2 four D-002 tokens, ORDERED-EQUAL to harness.DR-G23.provider-well-formed-admission.preview.v2. "
        "Each copy's sha256 equals the corresponding fixtures/anti-lockstep-goldens.v1/ digest, recomputed from disk. Windows is not copied. fixtures/anti-lockstep-goldens.v1/ is unmoved."
    )
    obj["leftoverDesignClosedIfAcceptedAndRecorded"] = []
    obj["leftoverDesignRemainingOnDR127"] = [
        "OBL-HOSTILE-GOLDENS",
        "OBL-AL3-CORE-ROLLBACK",
        "OBL-AL1-AL2-AL5",
    ]
    obj["remainderAfterThisCorpus"] = (
        "Leftover-design of OBL-HOSTILE-GOLDENS remains on leftover-join.v6 of anti-lockstep because seven classes carry unenumerated within-class quantifiers; D-314 G3-HOSTILE leaves those seven live v3 within-class universal sets including CC-6 named-open and supplies no per-class totals. "
        "Whether leftover-design of these per-D-002-platform copies is stale as an authoring claim after this recording is for a later leftover-join remasurement succeeding leftover-join.v6 of anti-lockstep to measure; anti-lockstep-hostile-goldens.v4 does not measure it. "
        "leftover-design of OBL-AL3-CORE-ROLLBACK and OBL-AL1-AL2-AL5 remains. leftover-design of OBL-G21-FX-AUTHORING remains on leftover-join.v45 of G21. DR-127 execution remains qualification (D-056). Not SATISFIED."
    )
    obj["summary"]["platformCopiesAuthored"] = True
    obj["summary"]["leftoverDesignOfOblHostileGoldensClosed"] = False
    obj["summary"]["leftoverDesign"] = [
        "OBL-HOSTILE-GOLDENS",
        "OBL-AL3-CORE-ROLLBACK",
        "OBL-AL1-AL2-AL5",
    ]

    obj["proposedLaterWork"] = [
        "A later D-000 recording may pin anti-lockstep-hostile-goldens.v4. anti-lockstep-hostile-goldens.v4 does not perform that recording.",
        "A later leftover-join remasurement succeeding leftover-join.v6 of anti-lockstep may measure leftover-design of these per-D-002-platform copies stale as an authoring claim. anti-lockstep-hostile-goldens.v4 does not measure that.",
        "Within-class universal quantifiers on CC-1, CC-2, CC-4, CC-5, CC-6, CC-7, and CC-9 remain unenumerated and named-open under D-314 G3-HOSTILE. anti-lockstep-hostile-goldens.v4 does not author those sets and does not invent a per-class total.",
        "Whether golden bytes may be shared with OBL-G21-FX-AUTHORING is not decided here.",
        "DR-127 execution remains qualification.",
        "A later dedicated SATISFIED-GRADE cycle may test DR-127 only when D-056 five gates hold. Gate 1 Class A remains unopened. anti-lockstep-hostile-goldens.v4 is not that cycle.",
    ]
    extra_does_not = [
        "Does not remasure leftover-join.v6 of anti-lockstep.",
        "Does not remasure leftover-join.v45 of G21.",
        "Does not remasure leftover-join.v14 of sarif.",
        "Does not remasure leftover-join.v11 of platform-tcb.",
        "Does not first-author prefix exactly at the operative bound.",
        "Does not author the seven named-open within-class universal sets.",
        "Does not invent a per-class total.",
        "Does not mutate fixtures/anti-lockstep-goldens.v1/.",
        "Does not copy onto Windows.",
        "Does not invent a D-002 platform list.",
        "Does not record anti-lockstep-hostile-goldens.v3 as current after anti-lockstep-hostile-goldens.v4 is recorded.",
        "Does not remasure g21-fixture-corpus.v30 as a golden.",
        "Does not remasure leftover-join.v32 of G21 as a golden.",
    ]
    for s in extra_does_not:
        if s not in obj["doesNot"]:
            obj["doesNot"].append(s)

    obj["failsIf"].extend(
        [
            "a D-002 platform list is invented rather than quoted from harness.DR-G10.provider-conformance.ts-major-1.v2 #$.platforms",
            "Windows is copied",
            "a copy digest differs from its fixtures/anti-lockstep-goldens.v1/ source",
            "fixtures/anti-lockstep-goldens.v1/ is mutated",
            "the seven named-open within-class universal sets are authored",
            "a per-class total is invented",
            "prefix exactly at the operative bound is first-authored",
            "leftover-join.v6 of anti-lockstep is remasured as a golden",
            "leftover-join.v45 of G21 is remasured",
            "leftover-join.v14 of sarif is remasured",
        ]
    )

    ri = obj["recordedInputs"]
    ri["docs/coop/COORDINATOR-DECISIONS.md"] = COORD
    ri["HEAD"] = HEAD
    ri["docs/v2/architecture/08-decision-and-readiness-register.md"] = FILE08
    ri["docs/coop/artifacts/anti-lockstep-hostile-goldens.v3.json"] = V3_SHA
    ri["docs/coop/artifacts/anti-lockstep-leftover-join.v6.json"] = LJ6
    ri["docs/coop/artifacts/g21-leftover-join.v45.json"] = G21LJ45
    ri["docs/coop/artifacts/sarif-leftover-join.v14.json"] = SARIF14
    ri["docs/coop/artifacts/platform-tcb-leftover-join.v11.json"] = PTCBLJ11
    ri["docs/coop/artifacts/harness.DR-G10.provider-conformance.ts-major-1.v2.json"] = G10
    ri["docs/coop/artifacts/harness.DR-G23.provider-well-formed-admission.preview.v2.json"] = G23
    for src in src_files:
        ri[str(src.relative_to(ROOT))] = copies_by_name[src.name]["sha256"]
        for c in copies_by_name[src.name]["copies"]:
            ri[c["path"]] = c["sha256"]

    obj["remeasurementClause"] = (
        "If a cited file moves in a way that is not append-only COORD growth or COORD heading hygiene, with file 08, leftover-join.v6 of anti-lockstep, leftover-join.v45 of G21, leftover-join.v14 of sarif, anti-lockstep-hostile-goldens.v3, fixtures/anti-lockstep-goldens.v1/, and this draft unmoved, remasure before recording. recordedInputs.HEAD must equal the top-level head. anti-lockstep-hostile-goldens.v4 does not unwrite D-086 or D-167 through D-362."
    )

    text = json.dumps(obj, indent=2, ensure_ascii=False) + "\n"
    if SUBJECT.exists():
        os.chmod(SUBJECT, 0o644)
    SUBJECT.write_text(text)
    os.chmod(SUBJECT, 0o444)

    loaded = json.loads(SUBJECT.read_text())
    assert loaded["binds"] == "NOTHING"
    assert loaded["version"] == 4
    assert loaded["leftoverDesignClosedIfAcceptedAndRecorded"] == []
    assert loaded["summary"]["leftoverDesign"] == [
        "OBL-HOSTILE-GOLDENS",
        "OBL-AL3-CORE-ROLLBACK",
        "OBL-AL1-AL2-AL5",
    ]
    assert loaded["summary"]["platformCopiesAuthored"] is True
    assert "This join" not in text
    assert "This v4" not in text
    assert "This leftover-join" not in text
    assert "This v3" not in text
    n_copies = sum(len(m["copies"]) for m in loaded["authoredCatalog"]["members"])
    assert n_copies == 64, n_copies
    print("subject", sha256_file(SUBJECT), SUBJECT.stat().st_size, oct(SUBJECT.stat().st_mode)[-4:])
    print("copies", n_copies)
    print("ok")


if __name__ == "__main__":
    main()
