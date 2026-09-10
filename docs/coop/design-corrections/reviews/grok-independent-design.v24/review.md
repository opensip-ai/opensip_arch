# Independent design review — candidate-subject.v24

**Verdict: ACCEPT**

Reviewer: actual Grok, fresh session. No coauthor context. Not Claude; no Claude agreement is claimed. This is design/architecture/schema/reference review only. It grants no grade, activation, implementation authorization, or D-372 application.

Subject manifest SHA-256 `a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb` measured match. Frozen snapshot `/tmp/opensip-design-corrections/candidate-subject.v24`: 12,797 files, 734,092,577 bytes, 0 hash/length mismatches, 0 extras. `verifiedManifest=true` only after that measurement. Parent is source23 (`652c8001…`). Historical source21 ACCEPT is inherited provenance of different bytes.

## What was read

All five product contracts were read completely, not as grep excerpts:

| Path | SHA-256 |
|---|---|
| `docs/v2/contracts/product-v1/README.md` | `c53633c2c8e056de5c2469995d9e9a8b5f0698f4c16bdf506803577ba7e703e6` |
| `identity-and-evidence.md` | `9261aff41cfe2c7a2f5e9b81c72cd3ab4aa96563a2732b9362ee53adfd683cf5` |
| `security-and-lifecycle.md` | `12dcebea91fd7ede7af85c3cace29ee931fbfa2d3f55f1773960328526ec496b` |
| `native-evidence.md` | `af2d566f1e1e87c7280512cd9fbee6f9055dde9decea6cf35a7bb2dbabe65fa1` |
| `workflows-and-surfaces.md` | `3d89b511663fe9238ef42dca9625f18f0d38f64f9094cae1b3ddfd7a3c1d98cf` |
| `admission-and-qualification.md` | `69cd6ba3cb41ed191e0a4e5cc20b191f4b8761625843b585426157873dbee6b3` |

Incorporated evaluator3 enumeration/atom/execution/composition/fault contracts, workflow3 projection, and query-projection-contract.v3.md (`9635e810…1044153f`, 18594 bytes) were read completely as one design. Query schema major 3 (`ca1e2bae…806d3093`) strengthens only `graph.neighbors|path|reach`; the twenty operation names are unchanged. All query renderers carry the complete owned `GraphQueryResponseV1`. Output profile 3, unchanged input/native profile 2, PolicyDocument2, required `executionInputsDigest`, and the two required Plan parameters remain separate axes. `hydradb-dispositions.proposed.md` (`9a15484c…be338922c`, 3868 bytes) accounts all eight proposals without choosing a graph database or claiming measured performance.

## Architecture assessment

The intended product is one host for discovery, admission, authority, orchestration, evaluation, custody and output. Native providers contribute facts and Coverage; the evaluator is pure; only authoritative analysis seals a source-bound Run.

Cross-owner joins checked against the owning sections:

- **Discovery / zero-config / availability.** Security S3 custody walk and nested-config boundary, shared `discovery-defaults.py` pruning/cap, native §1.4 units, Config2 layered resolution. Release-undeclared capabilities stay requested and are disclosed on `CommandEnvelope.availability`; they are not silently dropped.
- **Admission / authority order.** Operational grants precede any Plan (S10). Lexical numeric admission precedes schema merge. Evaluator3 Plan construction commits exactly one EnumerationPlanV1 and one EvaluatorEmissionPlanV1; omitting either refuses `EVALUATOR_REQUIRED_PARAMETER_MISSING`.
- **Acyclic identities.** proof3 excludes EvidenceId/RunId; evidence may include proof; seal includes both; Run includes seal. Capability-manifest CVE1, native H frames, and component-manifest digest stay distinct from the optional detector listing.
- **Enumeration / negative knowledge.** Expected inventories are Plan-selected before facts exist. Complete absence for a fingerprint requires complete enumeration plus determinate emitWhen roots; a known hit on another subject does not poison that. Independent mixed-root comparison produced POLICY-DELTA, not indeterminate.
- **Atoms / attribution / incoming completeness.** Target-attribution and incoming-search are globally admitted sidecars; search of U is not proved by Coverage of V.
- **Execution inputs / candidates.** Host-captured ExecutionInputsV1 is required on the proof. Candidate locators are opaque body IDs with snapshot-joined `sourceBodies`; they are not `subject3`.
- **Composition / waivers / budgets.** Strong Kleene; gating fail > indeterminate > pass; waivers preserve findings; required execution deficiencies survive disabled rules; work-budget exhaustion is semantic, output overflow is operational.
- **Correspondence.** Unmatched findings remain findings. Fingerprint-targeted repair/waiver cannot cover them.
- **Baseline / E0..E4.** E1–E3 re-evaluate retained current evidence after stripping only parent locators. E0 may change detector/native context. Snapshot membership is not extraction proof.
- **Detector listing.** `.opensip/detector-compatibility.json` is an optional same-tree Blob. `DetectorManifestV1` is three fields and is not `closure.manifestDigest`.
- **Query (new in this successor).** Graph requests resolve to one concrete retained `run3` before traversal. `{latest:true}` and `{snapshotId}` are trusted host observations; one admitted Run does not prove snapshot uniqueness and cannot mint latest. Endpoints are `(universe, kind, nativeSubjectId[, packageManifestPath])`; the same native id in another universe is `QUERY.ENDPOINT_UNKNOWN`, not ambiguity. Unsupported request rungs refuse; unprojectable facts omit with disclosure. Page fullness (`truncated-page`, `truncated=false`) is not operation truncation; `completenessMet` follows `countBasis=exact` and is not native closed-world. Continuation binds the concrete Run and cannot re-resolve latest or pass work caps. Failure envelopes are `kind=failure`, nonempty `errors`, no `run`. Human/JSON/agent carry the complete `GraphQueryResponseV1`.
- **SEAL.** Linearize fixture, prefix dispatch, and `admit_analysis_seal` are three boundaries. Public analysis SEAL requires `close_run`.
- **Qualification.** Native matrix 66 cells, 0 QUALIFIED. All 32 product gates unperformed.

No missed, conflicting, or under-specified *semantic* requirement was found that meets the MUST/SHOULD bar (owner selector, concrete consequence/reproducer, required minimal remedy). Explicit algorithm freedom is not treated as a missing contract. D9 later published successor remains a carried implementation obligation.

## Independent probes

Script `probes/independent-probes.v1.py` (30 cases; not author oracles):

1. Honest positive graph: `open_run_closure` RunId equals `close_run`.
2. Reviewer-reminted severity mutant and reviewer-reminted false `pass` verdict: structural owner admission **ADMIT**, complete replay **REFUSE** (`EVALUATOR_COMPLETE_PROOF_REPLAY`). The structural API is not semantic authority.
3. The two required evaluator3 parameter rows refuse when either is omitted.
4. Listing schema cannot occupy the component-manifest body.
5. Mixed-root absence constructed by this reviewer: two POLICY-DELTA entries, appeared E1=false / E4=true.
6. Graph query over an owner-admitted retained Run: neighbors resolve to `{runId}` only; `advisory=false`.
7. `latest` without `host.latestRunId`, and `snapshotId` without `host.runsForSnapshot`, refuse `QUERY.VIEW_UNKNOWN`. A stale snapshot map that names a different Run cannot grant the historical selection. Two Runs for one snapshot refuse `QUERY.VIEW_AMBIGUOUS`.
8. `host.cache` / `host.standing` / caller-authored deficiencies do not change neighbor rows or citations.
9. `references@syntactic-name-match` refuses `QUERY.RELATION_UNSUPPORTED` (request, not omission). Same native id in another universe is `QUERY.ENDPOINT_UNKNOWN`.
10. Graph evidence is Coverage/deficiency/limitation disclosure, not a Coverage scalar. Page fullness is not operation truncation; `completenessMet` is true for an exact count with remaining pages. A produced-item cap’s last page is `truncated-bound` with no cursor; `completeness=required` is indeterminate `QUERY.COMPLETENESS_UNMET`.
11. Continuation cannot re-resolve `latest` (`QUERY.CURSOR_MISMATCH`). Live inventory already declares the six required query parity fields; human/JSON/agent preserve the complete owned response.
12. A fully reminted false-result graph: owner **ADMIT**, public `execute_graph_query` **REFUSE** (`evidence.corrupt`, failure envelope has no `run`).
13. Twenty operation names unchanged. Eight HydraDB proposals accounted without a database choice or speedup claim.
14. Pin-gate: tamper of `admission-and-qualification.md` in the disposable copy made `run-evaluator3-checks.py` set `sourcePinsValid=false`, run no children, exit 1. Bytes restored. Original snapshot unaltered.

## Source-pinned receipts

Launchers ran from a disposable exact copy with pin hashes verified first. `/tmp/opensip-architecture-review-env/bin/python -I -B`. Pin-gate refusal is a failure; it was not bypassed.

| Group | Result | Independently recomputed |
|---|---|---|
| foundation 5 children | pass, pins 1216 | 231+1596+24+28+105 = **1984** |
| evaluator3 15 children | pass, pins 1220 | all exit 0, including query-projection (109/109) |
| security | 464/464 + 11 sweeps | |
| native | PASS | **375** cases; 66 cells; 0 QUALIFIED |
| workflows | pass | **14** schemas, **1803** checks, **45** commands |
| integration | 412/412 | synthetic TCB |

These are reference controls, not product qualification.

## Dispositions (routing only, not applied grades)

- **AR-01..AR-16:** `ROUTING-ASSESSED-ONLY-NOT-APPLIED` against the owning contract sections named in `review.json`.
- **FW-01..FW-15:** same, from the current-source map plus those sections.
- **DR-001..DR-011 and DR-011-R01..R16:** same, from inherited-residual maps plus actual owners. DR-011-R10 (fresh blind litmus) stays open as a later session.
- **DR-201..DR-205:** `ROUTED-ONLY`, `appliedByThisReview=false`, `finalApplicationOutcomeGranted=false`. Historical 2026-08-13 ACCEPTED grades are provenance of different subjects.
- **30 evaluation residuals** retained as routing under DR-011-R12, each with its own owning selector and basis in `review.json` (not a copied EP13 containment paragraph).
- **28 condition-2 obligations** (DR-101–107, 109–115, 117–127, 130/131/133) remain OPEN / not MET.
- **all 32 gates** remain unperformed.

## Advisories (not blockers)

1. Security S13 still says 456 cases and ten invariant sweeps; this run measured 464 cases and 11 sweeps. The semantic law is not missing.
2. D9 `host-invariant` successor artifact is a carried implementation obligation, not a new design blocker.

## Limitations

No fresh blind reconstruction is claimed. Selected schemas/registries were read as join dependencies and exercised; not every historical artifact in the snapshot was read as prose. Synthetic TCB inputs are not OS/crypto/compiler proof. Claude successor review remains later.

`newMustIssues` = [] and `newShouldIssues` = []. ACCEPT requires that, and it holds.
