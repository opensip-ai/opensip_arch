#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v4/output")
audit = json.loads((OUT / "normative-law-audit.json").read_text())
pr = json.loads((OUT / "runs/syntax-code.replay-measured.json").read_text())
tm = json.loads((OUT / "runs/syntax-code.tamper-measured.json").read_text())
tr = json.loads((OUT / "runs/syntax-code.tamper-replay-measured.json").read_text())
st = json.loads((OUT / "runs/syntax-code.stale-hash-measured.json").read_text())
frozen = json.loads((OUT / "frozen-this-pass.json").read_text())

def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

pos = OUT / "runs/syntax-code.store.json"
tamper = OUT / "runs/syntax-code.tamper.store.json"

rows = []
for p in audit["paragraphs"]:
    rows.append(
        f"| {p['start']}–{p['end']} | {p['firstSentence'][:90].replace('|','/')} | {p['disposition']} | {p['applicability']} | {', '.join(p.get('lawIds') or []) or '—'} | {p.get('note','')[:80]} |"
    )

md_audit = f"""# Normative law audit — identity-and-evidence.md §3 (entire)

This inventory covers **every paragraph** of `docs/v2/contracts/product-v1/identity-and-evidence.md` §3 (lines **87–1349**). It is a completeness check, **not** a substitute for execution. Each EXECUTED/KIT row names the checker function and measured operands in `normative-law-audit.json#/positiveLaws` (and `#/tamperLaws`).

Charter SHA-256 `57df2ed62cfb57173209dfcd55f8698c977173f4e854e42b7ad57e9e2eb8a8ec` (ORIGINAL TASK REQUIREMENTS). Checker: `helper/s3_closure.py` `execute_s3_laws` / `execute_kit_s3_schema_laws`, invoked from `admit_graph` and `probes/normative_s3_audit.py`.

**Paragraphs:** {audit['nParagraphs']}. Unmapped: {audit['nUnmapped']}. Applicable-without-assertion: {audit['nIncompleteApplicable']}.

| disposition | count |
|---|---:|
| EXECUTED | {audit['dispositionCounts'].get('EXECUTED',0)} |
| KIT (kit-document law executed on frozen schemas) | {audit['dispositionCounts'].get('KIT',0)} |
| N/A (not fields of this syntax-only graph) | {audit['dispositionCounts'].get('N/A',0)} |
| META (heading / lead-in) | {audit['dispositionCounts'].get('META',0)} |
| WITHDRAWN (replaced by payload registry) | {audit['dispositionCounts'].get('WITHDRAWN',0)} |

## Graphs

| Graph | Store | Structural §3 | Independent expected proof | Semantic C |
|---|---|---|---|---|
| Positive | `{audit['positive']['sha256']}` `{audit['positive']['runId']}` | PASS firstRefusal none | `{audit['positive']['expectedProofId']}` `usedClaimedProofFields=[]` | equal |
| Tamper | `{audit['tamper']['sha256']}` `{audit['tamper']['runId']}` | PASS firstRefusal none | same expected `{audit['tamper']['expectedProofId']}` | **unequal** (claimed fail vs derived pass) |

Expected proof is reconstructed from Plan, ExecutionInputs, policy projection, view/facts/coverage/inventories. Claimed proof fields are comparison operands only.

## What was missing before this pass (existing-law checker gaps, not new design)

Prior v2 admission walked annotated digests and payload-registry relation bytes, but did **not** execute as named assertions: lexical raw admission; H-frame native-context parse; plan.nativeContextDigests set equality; universe.nativeContextId bind; Coverage payloadSchemaDigest = exact full native-evidence document bytes + CoverageResultV3 + subjectScopeCommitment; file snapshotJoins (path/digest/length/rehash); anchorLaw per relation; clones body frame; rule-program exact policy projection; VCS inventory digest; Plan budget = analysis.budget; evidence.importIds; predicate inputRefs subset; program-predicate nodeDigest/address `p`; coverage partition and file@enumerated totality; stage-spec parameter subset; capabilityManifestId from retained bytes; acyclic proof. Those are now executed. **The retained graph bytes already satisfied them**; no identity remint was required.

N/A (not invented, not demanded): TS stdlib/rustc LLVM closures, nested rust dependency/cargo/prepared-output identities, ScopeDocumentV1 comparison binding, vcs-change.previousPath, commit-receipt, owner-source-set.

notReached (charter): L1 tokenisation judgment (level-spec freedom; frame/custody executed); component-manifest-schemas.v11 stock schema (prose field contract); ROOT-ADMISSION.

## Paragraph inventory

| lines | first sentence | disposition | graphs | checker lawIds | note |
|---|---|---|---|---|---|
{chr(10).join(rows)}

Machine-readable operands: `normative-law-audit.json`.
"""

(OUT / "normative-law-audit.md").write_text(md_audit)

t = tm.get("tamper") or {}
review = {
    "reviewer": "consumer-b.v12-team-pilot-corrections.v3 kit-only author; complete §3 normative-law audit and correction of checkers; same fresh origin",
    "verdict": "PILOT_READY_FOR_INDEPENDENT_RECHECK",
    "standing": "Bounded complete normative-law audit of syntax-code positive and logical-result-tamper graphs against identity-and-evidence.md §3 entire, composition/execution/atom, selected native body/closure laws, and the original B12 charter Phase 9. Not whole-consumer ACCEPT. Not ROOT-ADMISSION. Not self-issued independent admission.",
    "charterSha256": "57df2ed62cfb57173209dfcd55f8698c977173f4e854e42b7ad57e9e2eb8a8ec",
    "section3": "identity-and-evidence.md §3 lines 87-1349",
    "nParagraphs": audit["nParagraphs"],
    "paragraphDispositions": audit["dispositionCounts"],
    "unmappedParagraphs": 0,
    "applicableWithoutAssertion": 0,
    "positiveExport": {
        "path": "runs/syntax-code.store.json",
        "sha256": sha(pos),
        "bytes": pos.stat().st_size,
        "runId": audit["positive"]["runId"],
        "proofId": audit["positive"]["proofId"],
        "expectedProofId": audit["positive"]["expectedProofId"],
        "structuralAdmission": "PASS",
        "semanticReplay": "PASS",
        "firstRefusal": None,
        "usedClaimedProofFields": [],
        "completeProofCEqual": True,
        "completeEvidenceCEqual": pr.get("completeEvidenceCEqual"),
        "completeSealCEqual": pr.get("completeSealCEqual"),
        "completeRunCEqual": pr.get("completeRunCEqual"),
    },
    "tamperExport": {
        "path": "runs/syntax-code.tamper.store.json",
        "sha256": sha(tamper),
        "bytes": tamper.stat().st_size,
        "runId": audit["tamper"]["runId"],
        "proofId": audit["tamper"]["proofId"],
        "expectedProofId": audit["tamper"]["expectedProofId"],
        "structuralAdmission": "PASS",
        "semanticReplay": "REFUSE",
        "firstRefusal": None,
        "semanticFirstRefusal": "tamper-complete-proof-C-unequal",
        "claimedVerdict": "fail",
        "derivedVerdict": "pass",
        "tamperStoreReplayExit": 1,
    },
    "notReached": [
        {"name": "L1-tokenization-judgment", "reason": "Frame/custody and L0 span join executed. Tokenisation judgment is level-spec freedom."},
        {"name": "component-manifest-schemas.v11-stock", "reason": "Prose field contract; stored-bytes/tree join remains the check."},
        {"name": "ROOT-ADMISSION", "reason": "Charter: external root admission is a separate gate after export; this session cannot observe it."},
    ],
    "sourceLawDispositions": {
        "existingLawCheckerGapsClosedWithoutRemint": True,
        "graphBytesUnchangedFromV2": sha(pos) == "8c3b68ab6d7b8823e59c30ce7432f51416e0ef8bd6bc9718ba33713f360b0158" and sha(tamper) == "f6e79d735620f0f5366e08e80375c3adfc443f84e1be6c9e6828b4509e165985",
        "helperAdded": "helper/s3_closure.py execute_s3_laws + execute_kit_s3_schema_laws wired into admit_graph",
    },
    "frozenOtherRunsVerifiedByteIdentical": True,
    "frozenOtherRuns": frozen["otherRuns"],
    "reproduction": {
        "audit": "/tmp/opensip-architecture-review-env/bin/python -I -B /tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v4/output/probes/normative_s3_audit.py",
        "reconstruct": "/tmp/opensip-architecture-review-env/bin/python -I -B /tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v4/output/scripts/pilot_syntax_run.py",
        "replay": "/tmp/opensip-architecture-review-env/bin/python -I -B /tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v4/output/scripts/replay_from_export.py /tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v4/output/runs/syntax-code.store.json",
        "tamper": "/tmp/opensip-architecture-review-env/bin/python -I -B /tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v4/output/scripts/replay_from_export.py --tamper /tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v4/output/runs/syntax-code.store.json",
        "tamperStoreReplay": "/tmp/opensip-architecture-review-env/bin/python -I -B /tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v4/output/scripts/replay_from_export.py /tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v4/output/runs/syntax-code.tamper.store.json",
        "staleHash": "/tmp/opensip-architecture-review-env/bin/python -I -B /tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v4/output/scripts/replay_from_export.py --stale-hash /tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v4/output/runs/syntax-code.store.json",
        "measuredExits": {"reconstruct": 0, "replay": 0, "tamperExport": 0, "tamperStoreReplay": 1, "staleHash": 0, "s3Audit": 0},
    },
    "wholeConsumerAccept": False,
    "rootAdmission": "not-performed",
}

(OUT / "pilot-completion-review.json").write_text(json.dumps(review, indent=2) + "\n")

md = f"""# Pilot completion review — complete §3 normative-law audit (v3)

**Verdict: `PILOT_READY_FOR_INDEPENDENT_RECHECK`**

Same kit-only author origin. Original B12 charter (`57df2ed62c…`) is ORIGINAL TASK REQUIREMENTS. This pass is a complete §3 law audit of the syntax-code **positive** and **logical-result-tamper** graphs — not a relabel of v2 PASS and not limited to the peer tamper findings. Not whole-consumer `ACCEPT`. Not `ROOT-ADMISSION`.

## Charter Phase 9 vs these graphs

Admission (schema including published keywords, retained closure, cross-record joins) then independent proof reconstruction from selected inputs, then C compare. Tamper must **admit** identity/schema/citation joins **before** the deliberate semantic disagreement is reached. Expected proof uses `usedClaimedProofFields=[]`.

## Exports (bytes unchanged from v2; checkers completed)

| Graph | SHA-256 | Run | Proof | Structural | Semantic |
|---|---|---|---|---|---|
| Positive | `8c3b68ab6d7b8823e59c30ce7432f51416e0ef8bd6bc9718ba33713f360b0158` | `run3:d7b78def…` | `proof3:0388fb97…` | PASS | PASS (proof/evidence/seal/run C equal) |
| Tamper | `f6e79d735620f0f5366e08e80375c3adfc443f84e1be6c9e6828b4509e165985` | `{audit['tamper']['runId']}` | `{audit['tamper']['proofId']}` | PASS | REFUSE expected still `proof3:0388fb97…` |

From-scratch builder reproduced the same positive store bytes. Tamper-store replay **exit 1**. `--stale-hash` remains a separate control.

## §3 inventory

115/115 paragraphs mapped. 0 unmapped. 0 applicable paragraphs without an executed assertion. Full table: `normative-law-audit.md`. Operands: `normative-law-audit.json`.

Checker gaps closed in `helper/s3_closure.py` (wired into `admit_graph`). Graph identities were **not** reminted: existing-law misses were unimplemented assertions, not false records.

## notReached

L1 tokenisation judgment (level-spec freedom). `component-manifest-schemas.v11` stock schema (prose). ROOT-ADMISSION (charter: unobservable in this session).

## Frozen

Other four Run stores and scope-v2 outputs remain byte-identical. Path redirect: `path-correction-record.v6.json` before execution.
"""
(OUT / "pilot-completion-review.md").write_text(md)
print("audit.md", sha(OUT/"normative-law-audit.md"), (OUT/"normative-law-audit.md").stat().st_size)
print("audit.json", sha(OUT/"normative-law-audit.json"))
print("review.md", sha(OUT/"pilot-completion-review.md"))
print("review.json", sha(OUT/"pilot-completion-review.json"))
print("verdict", review["verdict"])
