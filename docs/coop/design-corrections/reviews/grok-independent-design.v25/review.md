# Independent design review — candidate-subject.v25

**Verdict: ACCEPT**

Reviewer: actual Grok, fresh independent session. Not Claude; no Claude agreement is claimed. Architecture/design/schema/reference only. No grade, activation, implementation authorization, or application approval.

Subject manifest `fa8cdc796c4dbab514c8b8a91a593b740e3f8e69d19574f4be11c6e00c3a536d` measured equal. Frozen snapshot `/tmp/opensip-design-corrections/candidate-subject.v25`: 12,869 files, 735,108,187 bytes, 0 hash/length mismatches, 0 missing, 0 undeclared extras. `verifiedManifest=true`.

## What this successor is

v25 is the frozen **target-identity and proof-contract** successor over source24. Output profile remains 3; native/input identities remain profile 2; PolicyDocument2, required `executionInputsDigest`, and the two required Plan parameters (EnumerationPlanV1, EvaluatorEmissionPlanV1) stay separate axes. Historical source21 is inherited provenance only.

The selected occupancy schema is **TargetAttributionV2**. Worker delivery is **OccupancyCompanionV1** on negotiated **FactBatchV3** (`target-attribution-v2` is an additional optional capability, not an identity token). The host `buffer_fact_batch_occupancy` runs during ANALYZING against required **DispatchBindingV1**; `bind_worker_occupancy` projects V2 after fact2 mint and stageReceipt, filling `planId` / `sourceFactId` / `producerClosure` from retained Plan/stage-spec/view membership. The COMPLETE58 post-fact2 envelope is not delivery. Historical V1 attribution is refused (`TARGET_ATTRIBUTION_SCHEMA_VERSION`). Frozen24 Runs remain replayable only under frozen24’s own selected V1 schema.

Portable occupancy identity (file LogicalPath / packageName+packageManifestPath / symbol SubjectIdV1) is distinct from opaque payload `SubjectIdV1`. Host MUST NOT parse `namespace:opaque` spelling. Exact-id ephemeral projection is independent of sidecar attestation; known ephemeral fields win over sidecar unknown; C15 first-party identity disagreement refuses.

Query schema major 3 strengthens only `graph.neighbors` / `graph.path` / `graph.reach`. All twenty operation names are unchanged. Graph endpoints use occupancy-identity vertices. Traversal completion is not native closed-world. `hydradb-dispositions.proposed.md` accounts all eight proposals without choosing a graph database or claiming measured performance.

Composition §9 is reconstructible: witnesses have no `inputRefs`; atomic `predicateProofs[].inputRefs` equal the complete admitted evaluation input selection; boolean nodes take the canonical union of children; consulted `coverageIds`/`scopeIds` may be narrower; originating required-cell refs are retained beside the execution-inputs digest.

Closure-kind is enforced at each actual owner. Occupancy joins the execution-plan stage-spec **provider** closure, not EnumerationPlan `enumerator.closureId`. Cached payloads and structural `open_run_closure` are not semantic authority.

## Cross-owner joins assessed

Discovery/zero-config/installed availability, typed configuration/admission/authority ordering, acyclic full source/Plan/native/evaluator/proof/evidence/Run, complete enumeration and negative knowledge, atom witnesses/target-attribution/incoming completeness, host-captured execution inputs and candidate-only paths, three-valued composition/waivers/budgets, stable correspondence and unmatched findings, source-bound portable baseline and E0..E4 with non-substituted evidence, optional tree-bound detector listing (component manifest is a different body), import/test/runtime/history evidence, invocation and repair authority, SEAL full replay vs prefix dispatch, output/common fault routes, and capability/platform/qualification boundaries were read as one design.

No missed, conflicting, or under-specified **semantic** contract was found that meets the MUST/SHOULD bar (exact owner, concrete consequence/reproducer, required minimal remedy). Explicit algorithm freedom is not a missing contract. Product/compiler/OS/crypto qualification is future work. Synthetic TCB observations are assumptions.

## Independent probes

Python: `/tmp/opensip-architecture-review-env/bin/python -I -B`. Script `probes/independent-probes.v1.py`, 32 cases, all passed.

- **Proof boundary.** Honest graph: `close_run` equals `open_run_closure`. Fully reminted severity change and false-pass verdict: owner `open_run_closure` **ADMIT**, `close_run` **REFUSE** `EVALUATOR_COMPLETE_PROOF_REPLAY`. Structural admission is not semantic authority.
- **Cross-unit occupancy.** Buffer during ANALYZING does not require receipts. `retainedStageOrdinal=7` is not `analyzeRequestOrdinal=0`. Host-projected V2 `evaluationNativeId=src/a.ts` is not opaque `targetNativeId=file:src/a.ts`. Extra companion ordinal refuses. V3 without the token refuses `PROVIDER_RETURN_UNNEGOTIATED_V3`. V1 sidecar refuses. C15 ephemeral/sidecar first-party conflict refuses. Producer kind is provider, not enumerator.
- **Retained graph query.** `execute_graph_query` after `close_run` on an imports graph: first-party file vertex is inventory `a.ts`, not payload `file:a.ts`. `host.targetAttributions` does not grant occupancy. `{latest:true}` without trusted observation is `QUERY.VIEW_UNKNOWN` and a `kind=failure` envelope with no `run`. Syntactic rung is `QUERY.RELATION_UNSUPPORTED`. Evidence disclosure is present independently of row count. Schema major 2 is unsupported.

Pin-gate: mutating `admission-and-qualification.md` in the disposable copy made `run-evaluator3-checks.py` refuse (`sourcePinsValid=false`, no checks executed). The file was restored to its pinned hash.

## Source-pinned launchers (disposable copy)

Pin ledgers were byte-identical to the frozen snapshot and verified before execution.

| Unit | Result |
|---|---|
| evaluator3 launcher (16 jobs including provider-attribution-return, query-projection, analysis-seal) | pins valid, all exit 0 |
| foundation launcher | pins valid, passed |
| security lifecycle | 464/464 cases, 11 sweeps |
| native evidence | 375/375 cases |
| workflows launcher | pins valid, passed |
| integration | 412 passed, synthetic TCB |
| pin-gate refusal | failed closed as required |

Passing these is not product qualification.

## Advisories (not blockers)

1. Security S13 still writes “456 cases” and “ten invariant sweeps”; this run measured 464 and 11. Stale reference-evidence count, not a missing law.
2. D9 `host-invariant` successor artifact remains a carried implementation obligation. Historical `d9-exit-contract.v1.14` bytes stay immutable. Not a new design-level blocker under this charter.

## Application routing (not applied grades)

All AR-01..AR-16, FW-01..FW-15, DR-001..DR-011, DR-011-R01..R16: `ROUTING-ASSESSED-ONLY-NOT-APPLIED`, `appliedByThisReview=false`, `finalApplicationOutcomeGranted=false`.

DR-201..DR-205: `ROUTED-ONLY`, same two false flags. Historical ACCEPTED standing is provenance of a different subject.

Retained: 30 evaluation residuals; 28 condition-2 obligations (DR-101–107, 109–115, 117–127, 130/131/133). All 32 product qualification gates (DR-G01..G32) remain unperformed.

## Limitations

Not a blind consumer reconstruction. Not Claude review. Not implementation or application authorization. Reference models use synthetic TCB observations.

Machine record: `review.json`.
