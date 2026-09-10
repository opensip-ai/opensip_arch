# Independent design review — candidate-subject.v23

**Verdict: ACCEPT**

Reviewer: actual Grok, fresh session. No coauthor context. Not Claude; no Claude agreement is claimed. This is design/architecture/schema/reference review only. It grants no grade, activation, implementation authorization, or D-372 application.

Subject manifest SHA-256 `652c800166a8d3f37eacfbf273c9786bb84f6fd6b5c6ead57b5a254315859a25` measured match. Frozen snapshot `/tmp/opensip-design-corrections/candidate-subject.v23`: 12,391 files, 721,238,130 bytes, 0 hash/length mismatches, 0 extras. `verifiedManifest=true` only after that measurement. Historical source21 ACCEPT is inherited provenance of different bytes.

## What was read

All five product contracts were read completely, not as grep excerpts:

| Path | SHA-256 |
|---|---|
| `docs/v2/contracts/product-v1/README.md` | `c53633c2…e703e6` |
| `identity-and-evidence.md` | `9261aff4…683cf5` |
| `security-and-lifecycle.md` | `12dcebea…ec496b` |
| `native-evidence.md` | `e1ee0315…7fd35b` |
| `workflows-and-surfaces.md` | `0a8e923c…9a1f3b` |
| `admission-and-qualification.md` | `69cd6ba3…bee6b3` |

Incorporated evaluator3 enumeration/atom/execution/composition/fault contracts and the workflow3 projection were read completely as one design. Output profile 3, unchanged input/native profile 2, PolicyDocument2, required `executionInputsDigest`, and the two required Plan parameters remain separate axes.

## Architecture assessment

The intended product is one host for discovery, admission, authority, orchestration, evaluation, custody and output. Native providers contribute facts and Coverage; the evaluator is pure; only authoritative analysis seals a source-bound Run.

Cross-owner joins that this session actually checked against the owning sections:

- **Discovery / zero-config / availability.** Security S3 custody walk and nested-config boundary, shared `discovery-defaults.py` pruning/cap, native §1.4 units, Config2 layered resolution. Release-undeclared capabilities stay requested and are disclosed on `CommandEnvelope.availability`; they are not silently dropped.
- **Admission / authority order.** Operational grants precede any Plan (S10). Lexical numeric admission precedes schema merge. Evaluator3 Plan construction commits exactly one EnumerationPlanV1 and one EvaluatorEmissionPlanV1; omitting either refuses `EVALUATOR_REQUIRED_PARAMETER_MISSING`.
- **Acyclic identities.** proof3 excludes EvidenceId/RunId; evidence may include proof; seal includes both; Run includes seal. Capability-manifest CVE1, native H frames, and component-manifest digest stay distinct from the optional detector listing.
- **Enumeration / negative knowledge.** Expected inventories are Plan-selected before facts exist. Complete absence for a fingerprint requires complete enumeration plus determinate emitWhen roots; a known hit on another subject does not poison that. Independent mixed-root comparison produced POLICY-DELTA, not indeterminate.
- **Atoms / attribution / incoming completeness.** Target-attribution and incoming-search are globally admitted sidecars; search of U is not proved by Coverage of V.
- **Execution inputs / candidates.** Host-captured ExecutionInputsV1 is required on the proof. Candidate locators are opaque body IDs with snapshot-joined `sourceBodies`; they are not `subject3`.
- **Composition / waivers / budgets.** Strong Kleene; gating fail > indeterminate > pass; waivers preserve findings; required execution deficiencies survive disabled rules; work-budget exhaustion is semantic, output overflow is operational.
- **Correspondence.** Unmatched findings remain findings. Fingerprint-targeted repair/waiver cannot cover them.
- **Baseline / E0..E4.** E1–E3 re-evaluate retained current evidence after stripping only parent locators. E0 may change detector/native context. Snapshot membership is not extraction proof.
- **Detector listing.** `.opensip/detector-compatibility.json` is an optional same-tree Blob. `DetectorManifestV1` is three fields and is not `closure.manifestDigest` (DR-103 component-manifest body).
- **SEAL.** Linearize fixture, prefix dispatch, and `admit_analysis_seal` are three boundaries. Public analysis SEAL requires `close_run`.
- **Qualification.** Native matrix 66 cells, 0 QUALIFIED. All 32 product gates unperformed.

No missed, conflicting, or under-specified *semantic* requirement was found that meets the MUST/SHOULD bar (owner selector, concrete consequence/reproducer, required minimal remedy). Explicit algorithm freedom is not treated as a missing contract. D9 later published successor remains a carried implementation obligation.

## Independent probes

Script `probes/independent-probes.v1.py` (not author oracles):

1. Honest positive graph: `open_run_closure` RunId equals `close_run`.
2. Reviewer-reminted severity mutant and reviewer-reminted false `pass` verdict: structural owner admission **ADMIT**, complete replay **REFUSE** (`EVALUATOR_COMPLETE_PROOF_REPLAY`). The structural API is not semantic authority.
3. The two required evaluator3 parameter rows refuse when either is omitted.
4. Listing schema cannot occupy the component-manifest body.
5. Mixed-root absence constructed by this reviewer: two POLICY-DELTA entries, appeared E1=false / E4=true.
6. Pin-gate: tamper of `admission-and-qualification.md` in the disposable copy made `run-evaluator3-checks.py` set `sourcePinsValid=false`, run no children, exit 1. Bytes restored. Original snapshot unaltered.

## Source-pinned receipts

Launchers ran from a disposable exact copy with pin hashes verified first. `/tmp/opensip-architecture-review-env/bin/python -I -B`. Pin-gate refusal is a failure; it was not bypassed.

| Group | Result | Independently recomputed |
|---|---|---|
| foundation 5 children | pass, pins 1211 | 231+1596+24+28+105 = **1984** |
| evaluator3 14 children | pass, pins 1215 | all exit 0, no timeouts |
| security | 464/464 + 11 sweeps | |
| native | PASS | **375** cases; 66 cells; 0 QUALIFIED |
| workflows | pass | **14** schemas, **1803** checks |
| integration | 412/412 | synthetic TCB |

These are reference controls, not product qualification.

## Dispositions (routing only, not applied grades)

- **AR-01..AR-16:** `ROUTING-ASSESSED-ONLY-NOT-APPLIED` against the owning contract sections named in `review.json`.
- **FW-01..FW-15:** same, from the current-source map plus those sections.
- **DR-001..DR-011 and DR-011-R01..R16:** same, from inherited-residual maps plus actual owners. DR-011-R10 (fresh blind litmus) stays open as a later session.
- **DR-201..DR-205:** `ROUTED-ONLY`, `appliedByThisReview=false`, `finalApplicationOutcomeGranted=false`. Historical 2026-08-13 ACCEPTED grades are provenance of different subjects.
- **30 evaluation residuals** retained as routing under DR-011-R12.
- **28 condition-2 obligations** (DR-101–107, 109–115, 117–127, 130/131/133) remain OPEN / not MET.
- **all 32 gates** remain unperformed.

## Advisories (not blockers)

1. Native §12 still says 132 cases; the file has 375.
2. Workflows §11 still says thirteen schemas; the checker reports 14.
3. `open_run_closure` docstring still sounds like the strong public boundary; contract and behavior do not.
4. D9 `host-invariant` successor artifact is a carried implementation obligation, not a new design blocker.

## Limitations

No fresh blind reconstruction is claimed. Selected schemas/registries were read as join dependencies and exercised; not every historical artifact in the snapshot was read as prose. Synthetic TCB inputs are not OS/crypto/compiler proof. Claude successor review remains later.

`newMustIssues` = [] and `newShouldIssues` = []. ACCEPT requires that, and it holds.
