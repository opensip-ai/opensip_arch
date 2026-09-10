#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v2/output")
KIT = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v2/subject")
REQ = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v2/requirements.json")

def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

pos = OUT / "runs/syntax-code.store.json"
tamper = OUT / "runs/syntax-code.tamper.store.json"
old_tamper = OUT / "preserved-failures/syntax-code-tamper-structural-inconsistent/runs/syntax-code.tamper.store.json"
tr = json.loads((OUT / "runs/syntax-code.tamper-measured.json").read_text())
t = tr["tamper"]
pr = json.loads((OUT / "runs/syntax-code.replay-measured.json").read_text())
tpr = json.loads((OUT / "runs/syntax-code.tamper-replay-measured.json").read_text())
st = json.loads((OUT / "runs/syntax-code.stale-hash-measured.json").read_text())
frozen = json.loads((OUT / "frozen-this-pass.json").read_text())
builder = json.loads((OUT / "runs/syntax-code.reconstruction-results.json").read_text())

review = {
    "reviewer": "consumer-b.v12-team-pilot-corrections.v2 kit-only reference author correction (same fresh origin; not independent acceptance of these bytes)",
    "verdict": "PILOT_READY_FOR_INDEPENDENT_RECHECK",
    "standing": "Bounded authoring correction of the syntax-code positive pilot and its whole logical-result-tamper replacement graph after kit-only peers withdrew prior acceptance. Not a new origin. Not whole-consumer ACCEPT. Not ACCEPT-RECONSTRUCTABLE. Not ROOT-ADMISSION. Not self-issued independent admission of the new tamper bytes.",
    "python": "/tmp/opensip-architecture-review-env/bin/python -I -B",
    "writeRoot": str(OUT),
    "peerInputsAuthenticated": True,
    "peerOutcomeTreatedAsHypothesis": True,
    "peerClassifications": {
        "assessedAgainst": [
            "evaluator-composition-contract.v3.md §3 none with known match is false",
            "evaluator-composition-contract.v3.md §4 emitWhen true emits exactly one finding3",
            "evaluator-composition-contract.v3.md §7 input admission precedes replay; discriminating controls mutate citations/findings then remint enclosing identities",
            "R-REPLAY-TAMPER preserve valid record identities and citation membership, change claimed logical result, replay refuses",
        ],
        "disposition": "AGREED — not disputed. Prior tamper graph failed structural claimed-output joins. Semantic C-unequal was not a reached replay boundary until the replacement graph is fully admitted.",
        "didNotInventStructuralSemanticRule": True,
        "didNotKeepWitnessMatchesWhileClaimingNoneTrue": True,
    },
    "helperConflicts": [
        {
            "helper": "helper/proof_replay.py logical_result_tamper / export_logical_result_tamper_graph (v1)",
            "conflict": "Preserved witnessDigest while flipping predicate value to true and findingIds []. Composition §3: none with known match is false. Composition §4: emitWhen true emits finding3. Witness is a claimed output (predicate-witness canonical-record), not an input citation.",
            "correction": "Remint witness matchingFactIds=[], value=true (internally consistent with no known match), emit unmatched finding3, join evidence.findingIds, remint proof/evidence/seal/Run. Preserve evaluationInputRefs, executionInputsDigest, plan, snapshot, views, facts, coverage, inventories.",
        }
    ],
    "inputHashes": {
        "kitManifestSha256": sha(KIT / "consumer-input-manifest.json"),
        "requirementsSha256": sha(REQ),
        "peerReviewSelfauditMd": "e1bcd89f017cb3b1dbc13bdae84ce91163c4f8c419f07767887b30c4a39c95c6",
        "peerReviewSelfauditJson": "68df95a6980c53c66ab1310af97b39ab6e32cfe63d6b93e49e94a8e7e4185a3a",
        "peerPilotReviewMd": "3bade29d0ecebe262dc9aa1e9cd314aa2e012048383d46e573cea5a89ba2766a",
        "peerPilotReviewJson": "facb035914fedb2018b13edb14dd2dd2c70b1a80b654c5f7d705d9937aca7bfa",
        "pathCorrectionV5": sha(OUT / "path-correction-record.v5.json"),
        "proofReplayPy": sha(OUT / "helper/proof_replay.py"),
        "replayFromExportPy": sha(OUT / "scripts/replay_from_export.py"),
    },
    "positiveExport": {
        "path": "runs/syntax-code.store.json",
        "sha256": sha(pos),
        "bytes": pos.stat().st_size,
        "runId": pr["runId"],
        "planId": "plan2:61407daf2c6f656c5258e1616907ae949fed63a1f4f6511572c395cfc6326471",
        "snapshotId": "snapshot2:f50135a27d89a1fa20bd4534f45d0e9f1633379a683b47c70dcec907e46911cd",
        "proofId": pr["claimedProofId"],
        "structuralAdmission": "PASS",
        "semanticReplay": "PASS",
        "firstRefusedBoundary": None,
        "independentlyDerived": {
            "usedClaimedProofFields": [],
            "expectedProofId": pr["expectedProofId"],
            "expectedProofCSha256": pr["proofCExpectedSha256"],
            "claimedProofCSha256": pr["proofCClaimedSha256"],
            "completeProofCEqual": pr["proofCompareEqual"],
            "completeEvidenceCEqual": pr["completeEvidenceCEqual"],
            "completeSealCEqual": pr["completeSealCEqual"],
            "completeRunCEqual": pr["completeRunCEqual"],
            "atomValue": pr["derivedAtomValue"],
            "verdict": pr["derivedVerdict"],
            "findingCount": pr["findingCount"],
        },
        "fromScratchBuilderReproducedSameStoreBytes": sha(pos) == "8c3b68ab6d7b8823e59c30ce7432f51416e0ef8bd6bc9718ba33713f360b0158",
        "builderRunId": builder.get("runId"),
        "builderClosureOk": builder.get("closureOk"),
    },
    "tamperExport": {
        "path": "runs/syntax-code.tamper.store.json",
        "sha256": sha(tamper),
        "bytes": tamper.stat().st_size,
        "runId": t["export"]["runId"],
        "proofId": t["export"]["proofId"],
        "evidenceId": t["export"]["evidenceId"],
        "sealId": t["export"]["sealId"],
        "findingIds": t["export"]["findingIds"],
        "planId": t["export"]["planId"],
        "executionInputsDigest": t["export"]["executionInputsDigest"],
        "structuralAdmission": "PASS",
        "semanticReplay": "REFUSE",
        "firstRefusedBoundary": {
            "order": "semantic, after complete structural admission",
            "name": "tamper-complete-proof-C-unequal",
            "selector": "evaluator-composition-contract.v3.md §7 compare C of complete recomputed proof and every referenced output preimage",
            "expectedProofId": t["semanticReplay"]["expectedProofId"],
            "claimedProofId": t["semanticReplay"]["tamperedProofId"],
            "expectedVerdict": "pass",
            "claimedVerdict": "fail",
            "derivedAtomValue": "false",
            "claimedAtomValue": "true",
        },
        "sameSelectedInputs": True,
        "inputCitationsPreserved": True,
        "witnessDigestReminted": True,
        "notStaleHash": True,
        "tamperStoreReplayExit": 1,
        "tamperStoreReplayClosureOk": tpr["closureOk"],
        "tamperStoreReplayProofCompareEqual": tpr["proofCompareEqual"],
    },
    "predecessorTamperPreserved": {
        "path": "preserved-failures/syntax-code-tamper-structural-inconsistent/runs/syntax-code.tamper.store.json",
        "sha256": sha(old_tamper),
        "bytes": old_tamper.stat().st_size,
        "runId": "run3:5d2ee6759163d735640ae160d08d7524812d5a7f80c7c08848bbd8db09123ed8",
        "proofId": "proof3:94c139961110a4277276b573b1dabdc589df017e2b3d3720f3c234f3b9f463c8",
        "structuralAdmission": "REFUSE",
        "semanticReplay": "notReached",
        "firstRefusedBoundary": "claimed-predicate-value-agrees-with-retained-witness-matches-0",
        "laterStructuralRefusals": ["claimed-emitWhen-true-has-finding3-0"],
        "matchingFactIds": ["fact2:852404c12751162c8a75c1c9e67465d2be7b356602fa2f663e03fa838849a717"],
        "note": "Replayed under the corrected structural joins; peer first-refusal name and operands reproduced exactly. Not relabeled accepted.",
    },
    "joinReplayBoundaries": [
        {"boundary": "input-graph-admission", "positive": "PASS", "tamper": "PASS", "owner": "identity-schemas.v3 open_run_closure / annotated digest / payload-registry / selectedRefs / file snapshotJoins"},
        {"boundary": "claimed-output-internal-consistency", "positive": "PASS (none=false with known match; emitWhen false so findingIds=[])", "tamper": "PASS after correction (none=true with matchingFactIds=[]; finding3 present)", "owner": "composition §3–4"},
        {"boundary": "evidence.proofBundleId / findingIds / seal.policyDigest / seal.verdict", "positive": "PASS", "tamper": "PASS", "owner": "identity-schemas.v3 semantic-evidence / evaluation-seal"},
        {"boundary": "independent expected proof without claimed proof fields", "positive": "PASS C/H equal proof3:0388fb97…", "tamper": "expected remains proof3:0388fb97…; claimed proof3:023f6c04…", "owner": "composition §7"},
        {"boundary": "independent expected evidence/seal/run C", "positive": "PASS all equal", "tamper": "all unequal (semantic)", "owner": "composition §7"},
        {"boundary": "semantic replay of tamper", "positive": "n/a", "tamper": "REACHED and REFUSED", "owner": "composition §7; R-REPLAY-TAMPER"},
        {"boundary": "stale-hash control", "positive": "separate; Run identity unchanged", "tamper": "not used as the tamper exhibit", "owner": "composition §7 rather than merely a stale hash"},
        {"boundary": "L1 tokenisation judgment", "positive": "notReached (level-spec freedom)", "tamper": "notReached", "owner": "identity-and-evidence §3 / fact-identity-policy.v2"},
        {"boundary": "component-manifest-schemas.v11 stock", "positive": "CANDIDATE-NOT-APPLIED / notReached", "tamper": "notReached", "owner": "v11 is a prose field contract"},
        {"boundary": "ROOT-ADMISSION", "positive": "not performed", "tamper": "not performed", "owner": "R-ROOT-ADMISSION-EXPORT"},
    ],
    "originalRequirementsAddressed": [
        "R-RUN-SYNTAX-CODE complete positive (retained; from-scratch builder reproduced the same store bytes)",
        "R-REPLAY-AFTER-ADMISSION / R-REPLAY-COMPARE-BUNDLE independent C/H of complete proof, evidence, seal, Run",
        "R-REPLAY-NO-CALLER-TRUTH usedClaimedProofFields=[]",
        "R-REPLAY-TAMPER structurally admitted replacement graph with false logical result; replay refuses (exit 1); stale-hash separate",
        "R-REPLAY-EXPORT tamper and positive stores retained whole",
        "R-NEGATIVE-FIRST-REFUSAL predecessor tamper first refusal measured; new tamper semantic first refusal after admission",
    ],
    "frozenOtherRunsVerifiedByteIdentical": frozen["otherRunsStillByteIdenticalAfterThisPass"],
    "frozenOtherRuns": frozen["otherRuns"],
    "scopeV2Frozen": frozen["scopeV2"],
    "preservedFailures": {
        "original": "8b0f6d826ed04f604ce8614e63b55e9666a9abdd48702f6b155c92c4ce54e654",
        "structuralRefused": "2e74a6b2dd2b94152d6c4ce266dbe1bc4b23dc257b0fea12a6c947d36fe08fe7",
        "evaluationInputRefsRefused": "0a0b2c6217846264b2bff2b013410215b0941c4c50d695bd234a1d5aac14ec36",
        "tamperStructuralInconsistent": "c9c1be48d0e7b3b1b315fb7ae5640c9bba9588201e55fb294f38e68b7a8b9f8e",
    },
    "reproduction": {
        "pathRedirect": "path-correction-record.v5.json before execution",
        "reconstruct": "/tmp/opensip-architecture-review-env/bin/python -I -B /tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v2/output/scripts/pilot_syntax_run.py",
        "replay": "/tmp/opensip-architecture-review-env/bin/python -I -B /tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v2/output/scripts/replay_from_export.py /tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v2/output/runs/syntax-code.store.json",
        "tamper": "/tmp/opensip-architecture-review-env/bin/python -I -B /tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v2/output/scripts/replay_from_export.py --tamper /tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v2/output/runs/syntax-code.store.json",
        "tamperStoreReplay": "/tmp/opensip-architecture-review-env/bin/python -I -B /tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v2/output/scripts/replay_from_export.py /tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v2/output/runs/syntax-code.tamper.store.json",
        "staleHash": "/tmp/opensip-architecture-review-env/bin/python -I -B /tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v2/output/scripts/replay_from_export.py --stale-hash /tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v2/output/runs/syntax-code.store.json",
        "measured": {
            "reconstructExit": 0,
            "replayExit": 0,
            "tamperExportExit": 0,
            "tamperStoreReplayExit": 1,
            "staleHashExit": 0,
        },
    },
    "staleHashControl": st.get("staleHashControl"),
    "wholeConsumerAccept": False,
    "rootAdmission": "not-performed",
    "remaining": [
        "Independent recheck of these NEW tamper bytes. This authoring pass is not that recheck.",
        "ROOT-ADMISSION over exact exported frames is not performed here.",
        "L1 token-stream tokenisation judgment notReached (level-spec freedom).",
        "component-manifest-schemas.v11 remains CANDIDATE-NOT-APPLIED.",
        "Other four Run stores and workflow/scope outputs remain frozen.",
        "Whole-consumer ACCEPT-RECONSTRUCTABLE is not issued.",
    ],
}

md = f"""# Pilot completion review — syntax-code tamper correction (team-pilot-corrections.v2)

**Verdict: `PILOT_READY_FOR_INDEPENDENT_RECHECK`**

This is kit-only reference **author correction** of the syntax-code positive pilot and its whole logical-result-tamper replacement graph, after authenticated kit-only peers withdrew prior acceptance. Same fresh origin, not a new session. **Not** whole-consumer `ACCEPT`, **not** `ACCEPT-RECONSTRUCTABLE`, **not** `ROOT-ADMISSION`, and **not** self-issued independent admission of these new bytes.

Peer grades were treated as hypotheses. Their classifications were assessed against composition §§3–4–7 and `R-REPLAY-TAMPER`. They are **agreed**, not disputed. No invented structural-semantic rule was used to remint.

## Peer findings addressed

Peers reported the v1 tamper export (`c9c1be48…`, `run3:5d2ee675…`, `proof3:94c13996…`) was **not** a complete admitted graph:

1. Composition §3 — claimed `none` value `true` while retained witness `matchingFactIds` still listed `fact2:852404c1…` (known match ⇒ `none` is false).
2. Composition §4 — claimed `emitWhen` true with `findingIds=[]`.
3. Semantic C-unequal was therefore **notReached** as a replay boundary.

Replayed here under the corrected claimed-output joins: first refusal `claimed-predicate-value-agrees-with-retained-witness-matches-0`, later `claimed-emitWhen-true-has-finding3-0`. That predecessor store is preserved and **not** relabeled accepted.

Helper conflict: v1 `export_logical_result_tamper_graph` treated `witnessDigest` as an input citation that must be preserved. Witness is a claimed **output** (`predicate-witness` canonical-record). `R-REPLAY-TAMPER` preserves valid **input** record identities and citation membership (`evaluationInputRefs`, plan, snapshot, views, facts, coverage, inventories). Composition §7 discriminating controls **mutate** citations/findings and remint enclosing identities.

Correction: remint the witness with `matchingFactIds=[]` (so §3 is not internally contradicted), set value `true`, emit one unmatched `finding3`, join `evidence.findingIds`, remint proof/evidence/seal/Run. Independent derivation from selected inputs still yields `none=false` / verdict `pass` / `proof3:0388fb97…`. That C inequality is now a **reached** semantic refusal after structural admission.

Did **not** keep nonempty matches while claiming `none=true` (that would be reminting toward an internally impossible claimed proof). Completeness-based truth of empty matches remains semantic; the structural law used is only “none with known match is false.”

## Exports

| Exhibit | Store SHA-256 | Run | Proof |
|---|---|---|---|
| Positive | `8c3b68ab6d7b8823e59c30ce7432f51416e0ef8bd6bc9718ba33713f360b0158` (889354 B) | `run3:d7b78defeb7524066df48934bbd65cd8e8c3edd7dd083272d0631a86e4bbc6fd` | `proof3:0388fb9721ce4140ab291f8591795e2f59dc600118be51331e3bca141a94760a` |
| NEW tamper | `{sha(tamper)}` ({tamper.stat().st_size} B) | `{t["export"]["runId"]}` | `{t["export"]["proofId"]}` |
| Preserved v1 tamper | `c9c1be48d0e7b3b1b315fb7ae5640c9bba9588201e55fb294f38e68b7a8b9f8e` (889474 B) | `run3:5d2ee675…` | `proof3:94c13996…` |

Plan `plan2:61407daf…` and `executionInputsDigest` `d72fb03c…` are the same selected-input bytes on positive and NEW tamper. NEW tamper finding `{t["export"]["findingIds"][0]}`. Evidence `{t["export"]["evidenceId"]}` seal `{t["export"]["sealId"]}`.

## Positive export (independently re-audited; not assumed accepted)

**First refused boundary: none** among executed applicable laws.

From-scratch builder exit 0 reproduced the **same store bytes** `8c3b68ab…` and `run3:d7b78def…`. Fresh-process replay exit 0. Expected proof derived with `usedClaimedProofFields=[]` from Plan, ExecutionInputs, enumeration, policy projection, view/facts/coverage/inventories. Complete C of proof, evidence, seal, and Run equals the claimed records. `none` over `file@enumerated` is **false**. Verdict **pass**. Finding count 0.

## NEW tamper export

**Structural admission: PASS** (first refusal none). Claimed `none=true` with empty witness matches; `emitWhen` true has `finding3`; evidence/seal/Run identities join the reminted proof.

**Semantic replay: REACHED and REFUSED.** Independent expected remains `proof3:0388fb97…` / verdict `pass` / atom `false`. Claimed `proof3:023f6c04…` / verdict `fail` / atom `true`. Proof/evidence/seal/run C all unequal.

Replay of the tamper store (no `--tamper` flag) **exit 1**: `closureOk` true, `proofCompareEqual` false.

## Stale-hash (separate control)

`--stale-hash` mutates `executionInputsDigest` only. Run identity unchanged `run3:d7b78def…`. C inequality is **not** semantic replay (`semanticReplayNotExercised: true`).

## From-scratch commands (measured)

```text
/tmp/opensip-architecture-review-env/bin/python -I -B \\
  .../scripts/pilot_syntax_run.py
# exit 0; store SHA-256 8c3b68ab… unchanged; run3:d7b78def…

/tmp/opensip-architecture-review-env/bin/python -I -B \\
  .../scripts/replay_from_export.py .../runs/syntax-code.store.json
# exit 0; proofCompareEqual true; complete evidence/seal/run C equal

/tmp/opensip-architecture-review-env/bin/python -I -B \\
  .../scripts/replay_from_export.py --tamper .../runs/syntax-code.store.json
# exit 0; structural ok; semantic refuse; export f6e79d73…

/tmp/opensip-architecture-review-env/bin/python -I -B \\
  .../scripts/replay_from_export.py .../runs/syntax-code.tamper.store.json
# exit 1; closureOk true; proofCompareEqual false

/tmp/opensip-architecture-review-env/bin/python -I -B \\
  .../scripts/replay_from_export.py --stale-hash .../runs/syntax-code.store.json
# exit 0; Run unchanged
```

Path literals in copied helper/scripts were redirected into this tree **before** execution (`path-correction-record.v5.json`, rewritten 18 / unchanged 15).

## Frozen other Runs and workflows (byte-identical)

| Store | SHA-256 |
|---|---|
| `runs/ts.store.json` | `885b8e4575235fe47fbee893d83e97d650aea230f9af870b8a711f25d943075d` |
| `runs/rust.store.json` | `67dc12f88fc19fb320385d30f6a740197c64ca9d574627b8db81cdb2f2000315` |
| `runs/syntax-data.store.json` | `1d07e4c8040035965a8821559a5916cf82014e19198e1e6acaf6e9b5ecdd6092` |
| `runs/rust-partial-clones.store.json` | `b6c2b240e11fff9699aeeacdd8a68a7ee7119f241029e3de0e4c955e2b058246` |

Scope-v2 workflow outputs remain the frozen hashes in `frozen-this-pass.json`. Other Run builders were path-redirected only and **not executed**.

## Remaining

1. Independent recheck of this NEW tamper graph. This authoring pass is not that recheck and not root admission.
2. `ROOT-ADMISSION` of exact exported frames is not performed here.
3. L1 tokenisation judgment notReached (level-spec freedom).
4. `component-manifest-schemas.v11` remains CANDIDATE-NOT-APPLIED.
5. Whole-consumer `ACCEPT-RECONSTRUCTABLE` is **not** issued.
"""

(OUT / "pilot-completion-review.json").write_text(json.dumps(review, indent=2) + "\n")
(OUT / "pilot-completion-review.md").write_text(md)
print("md", sha(OUT/"pilot-completion-review.md"), (OUT/"pilot-completion-review.md").stat().st_size)
print("json", sha(OUT/"pilot-completion-review.json"), (OUT/"pilot-completion-review.json").stat().st_size)
print("verdict", review["verdict"])
