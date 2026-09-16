#!/usr/bin/env python3
"""Build leftover-join.v11 of platform-tcb: land CLAUDE-PTLJ-V10-SF1/SF2 and Codex v10 advisory."""
from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "docs/coop/artifacts"
V10 = ART / "platform-tcb-leftover-join.v10.json"
SUBJECT = ART / "platform-tcb-leftover-join.v11.json"

HEAD = "111a2e70e41d11065216e505e9bdbeafb64e734b"
COORD = "241ad5b4d7efeb0fc3deea9904f3bea16d635d133c44e7b5c2060e966339371f"
FILE08 = "e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e"
V10_SHA = "43c963d95e4e4f2e6cadf2c93d3872a95ea59dfc5587682eb76bcfcf4183a989"
V10_CLAUDE = "3d72c59d0bd602ce7843244bc146670f242ebce89fd6b643389cc85c7eb1d2b8"
V10_CODEX = "4c23561ea5ecf6d3084fd847734c70c635095fb8480ecde86590f4635f945016"
V47_CLAUDE = "c68b790630178ff795f49abcac0f39a882f875e23e221b1c0cc1317a2da34031"
V47_CODEX = "1df157780b71a6452d917dc5d8bc7a2ea136416ec1aca98163dc63832ff428da"
G22LJ5_CLAUDE = "1879de4fa51ef72f44c07e8e31337c2954ffa1d200091cfd374d1f5345e98551"
G22LJ5_CODEX = "35454c10cbcd5097afbc1f9a49ffaedc0ae7f518ec2f106b0b34e993be4224bb"


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def walk_replace(obj, old: str, new: str):
    if isinstance(obj, str):
        return obj.replace(old, new)
    if isinstance(obj, list):
        return [walk_replace(x, old, new) for x in obj]
    if isinstance(obj, dict):
        return {k: walk_replace(v, old, new) for k, v in obj.items()}
    return obj


def main() -> None:
    obj = copy.deepcopy(json.loads(V10.read_text()))
    # Speaker bump only of the stemmed current-version phrase.
    obj = walk_replace(obj, "leftover-join.v10 of platform-tcb", "leftover-join.v11 of platform-tcb")
    obj["artifact"] = "platform-tcb-leftover-join.v11"
    obj["version"] = 11
    obj["date"] = "2026-09-01"
    obj["head"] = HEAD
    obj["file08Pin"]["sha256"] = FILE08

    obj["parentReview"]["role"] = (
        "Independent dual ACCEPT 0/0 of the current occupancy of the already-named G22 identifier. leftover-join.v11 of platform-tcb is a DR-126 leftover remasurement. Naming parent of G22 is gate-harness-naming.v6 (D-145), not leftover-join.v8 of platform-tcb. D-086 named DR-G22."
    )
    obj["basedOn"]["predecessorV6"]["role"] = (
        "Predecessor. Unmoved. Dual ACCEPT 0/0. Recorded as current DR-126 leftover-join at D-185. Cited occupancy v1 as the specification. leftover-join.v9 of platform-tcb remasured occupancy v1 stale after occupancy v2 (D-219). "
        "Frozen leftover-join.v8 of platform-tcb Findings CLAUDE-PTLJ-V8-SF1 / CODEX-PTLJ-V8-SF1 land at leftover-join.v9 of platform-tcb, at this field. Do not rewrite that landing. Not this artifact's version number."
    )

    obj["basedOn"]["predecessorV10"] = {
        "path": "docs/coop/artifacts/platform-tcb-leftover-join.v10.json",
        "sha256": V10_SHA,
        "reviews": {
            "claude": {
                "path": "docs/coop/artifacts/platform-tcb-leftover-join.v10.review-independent.claude2.json",
                "sha256": V10_CLAUDE,
                "verdict": "REJECT 0 MUST-FIX 2 SHOULD-FIX CLAUDE-PTLJ-V10-SF1 CLAUDE-PTLJ-V10-SF2",
            },
            "codex": {
                "path": "docs/coop/artifacts/platform-tcb-leftover-join.v10.review-independent.codex.json",
                "sha256": V10_CODEX,
                "verdict": "ACCEPT 0/0",
            },
        },
        "role": (
            "Predecessor. Unmoved. Stage A split. Claude REJECT 0 MUST-FIX 2 SHOULD-FIX CLAUDE-PTLJ-V10-SF1 CLAUDE-PTLJ-V10-SF2. Codex ACCEPT 0/0 with one unlabeled advisory. CANDIDATE-NOT-APPLIED. Not Dual ACCEPT. Not Dual REJECT. Frozen leftover-join.v10 of platform-tcb Findings land at leftover-join.v11 of platform-tcb. Do not record leftover-join.v10 of platform-tcb as current. leftover-join.v9 of platform-tcb remains the current recorded DR-126 leftover remasurement until a recordable successor is adopted. Not this artifact's version number."
        ),
    }

    obj["registerRowNote"] = (
        "registerRow is DR-126 because leftover-join.v11 of platform-tcb remasures leftover-design of DR-126 after occupancy v2 (D-219) and after D-361 recorded platform-tcb-contract.v48 as the DR-126 C4-c application-grade TCB successor that makes the selector grammar governing. "
        "file08StatusToken is DR-126's own live token (OPEN). leftover-join.v9 of platform-tcb remains the current recorded DR-126 leftover remasurement (D-268) until a recordable successor is adopted. "
        "Frozen leftover-join.v10 of platform-tcb stays unrecorded. Frozen leftover-join.v10 of platform-tcb Findings land at leftover-join.v11 of platform-tcb. "
        "leftover-join.v6 of platform-tcb remains frozen and is not current. leftover-join.v7 of platform-tcb is CANDIDATE-NOT-APPLIED (split Claude REJECT CLAUDE-PTLJ-V7-SF1 / Codex ACCEPT 0/0; not Dual ACCEPT; not Dual REJECT) and is not current. "
        "leftover-join.v8 of platform-tcb is CANDIDATE-NOT-APPLIED (Dual REJECT CLAUDE-PTLJ-V8-SF1 / CODEX-PTLJ-V8-SF1) and is not current. "
        "leftover-join.v11 of platform-tcb does not steal OBL-RESERVED-TABLES, does not populate reserved TCB tables, does not apply platform-tcb-contract.v48, and does not SATISFY DR-126."
    )
    obj["purpose"] = (
        "Remasure leftover-join.v9 of platform-tcb against live HEAD after D-361. Land CLAUDE-PTLJ-V10-SF1 at parentReview.role (gate-harness-naming.v6 at D-145). Land CLAUDE-PTLJ-V10-SF2 at basedOn.predecessorV6.role (Frozen leftover-join.v8 of platform-tcb Findings land at leftover-join.v9 of platform-tcb). Land the unlabeled Codex leftover-join.v10 of platform-tcb advisory by adding the four structured review pins to recordedInputs. "
        "Cite occupancy v2 as the current G22 occupancy remasurement. Cite leftover-join.v5 of G22 as the current G22 leftover remasurement (D-271). Cite platform-tcb-contract.v48 as the current recorded DR-126 C4-c application-grade TCB successor that makes the selector grammar governing (D-361). "
        "CLAUDE-PTLJ-V8-SF1 and CODEX-PTLJ-V8-SF1 remain landed at leftover-join.v9 of platform-tcb. CLAUDE-PTLJ-V3-SF1 remains landed at leftover-join.v5 of platform-tcb. CLAUDE-PTLJ-V7-SF1 remains landed at leftover-join.v8 of platform-tcb. leftover-join.v11 of platform-tcb does not re-land them. "
        "Preserve leftoverDesign [OBL-G22-FX-AUTHORING, OBL-RESERVED-TABLES]. Frozen leftover-join.v10 of platform-tcb Findings land at leftover-join.v11 of platform-tcb. Do not SATISFY DR-126. Do not populate a TCB table. Do not apply platform-tcb-contract.v48. Do not complete C4-d. Do not remasure leftover-join.v45 of G21. Do not remasure leftover-join.v14 of sarif. Do not first-author prefix exactly at the operative bound."
    )

    obj["findingDisposition"].extend(
        [
            {
                "id": "CLAUDE-PTLJ-V10-SF1",
                "severity": "SHOULD-FIX",
                "disposition": "ACCEPTED. Landed in this lineage at leftover-join.v11 of platform-tcb. parentReview.role now names gate-harness-naming.v6 (D-145), not leftover-join.v6 of platform-tcb.",
                "landedAt": ["parentReview.role"],
            },
            {
                "id": "CLAUDE-PTLJ-V10-SF2",
                "severity": "SHOULD-FIX",
                "disposition": "ACCEPTED. Landed in this lineage at leftover-join.v11 of platform-tcb. basedOn.predecessorV6.role now sources CLAUDE-PTLJ-V8-SF1 / CODEX-PTLJ-V8-SF1 to leftover-join.v8 of platform-tcb, landing at leftover-join.v9 of platform-tcb. Do not rewrite that landing.",
                "landedAt": ["basedOn.predecessorV6.role"],
            },
        ]
    )

    ri = obj["recordedInputs"]
    ri["docs/coop/COORDINATOR-DECISIONS.md"] = COORD
    ri["HEAD"] = HEAD
    ri["docs/coop/artifacts/platform-tcb-leftover-join.v10.json"] = V10_SHA
    ri["docs/coop/artifacts/platform-tcb-leftover-join.v10.review-independent.claude2.json"] = V10_CLAUDE
    ri["docs/coop/artifacts/platform-tcb-leftover-join.v10.review-independent.codex.json"] = V10_CODEX
    ri["docs/coop/artifacts/platform-tcb-contract.v47.review-independent.claude2.json"] = V47_CLAUDE
    ri["docs/coop/artifacts/platform-tcb-contract.v47.review-independent.codex.json"] = V47_CODEX
    ri["docs/coop/artifacts/g22-leftover-join.v5.review-independent.claude2.json"] = G22LJ5_CLAUDE
    ri["docs/coop/artifacts/g22-leftover-join.v5.review-independent.codex.json"] = G22LJ5_CODEX

    extra = [
        "Does not record leftover-join.v10 of platform-tcb as current.",
        "Does not remasure leftover-join.v10 of platform-tcb as a golden.",
        "Does not rewrite CLAUDE-PTLJ-V8-SF1 / CODEX-PTLJ-V8-SF1 Findings-land targets off leftover-join.v9 of platform-tcb.",
    ]
    for s in extra:
        if s not in obj["doesNot"]:
            obj["doesNot"].append(s)

    text = json.dumps(obj, indent=2, ensure_ascii=False) + "\n"
    if SUBJECT.exists():
        os.chmod(SUBJECT, 0o644)
    SUBJECT.write_text(text)
    os.chmod(SUBJECT, 0o444)

    loaded = json.loads(SUBJECT.read_text())
    assert loaded["version"] == 11
    assert loaded["binds"] == "NOTHING"
    assert loaded["summary"]["leftoverDesign"] == ["OBL-G22-FX-AUTHORING", "OBL-RESERVED-TABLES"]
    assert "This join" not in text
    assert "This v11" not in text
    assert "This leftover-join" not in text
    assert "Landed in this lineage at leftover-join.v9 of platform-tcb" in text
    assert "Landed in this lineage at leftover-join.v5 of platform-tcb" in text
    assert "Landed in this lineage at leftover-join.v8 of platform-tcb" in text
    assert "gate-harness-naming.v6 (D-145)" in loaded["parentReview"]["role"]
    assert "Frozen leftover-join.v8 of platform-tcb Findings" in loaded["basedOn"]["predecessorV6"]["role"]
    assert "Frozen leftover-join.v6 of platform-tcb Findings land at leftover-join.v9" not in text
    assert ri["docs/coop/artifacts/platform-tcb-contract.v47.review-independent.claude2.json"] == V47_CLAUDE
    print("subject", sha256_file(SUBJECT), SUBJECT.stat().st_size, oct(SUBJECT.stat().st_mode)[-4:])
    print("ok")


if __name__ == "__main__":
    main()
