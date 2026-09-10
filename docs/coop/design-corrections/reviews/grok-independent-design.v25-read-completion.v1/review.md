# Independent design review — candidate-subject.v25 (read-completion continuation)

**Verdict: ACCEPT**

This is the same fresh-origin Grok session continued, not a new independent reviewer. Original session id `01a085b3-3a90-7082-a261-3ba4e7e453c4`; origin `/tmp/opensip-design-corrections/grok-independent-design.v25`. Original `review.md` / `review.json` and probe/suite receipts are preserved unchanged. Not Claude; no Claude agreement is claimed. Architecture/design/schema/reference only. No grade, activation, implementation authorization, or application approval.

Subject manifest `fa8cdc796c4dbab514c8b8a91a593b740e3f8e69d19574f4be11c6e00c3a536d` re-verified equal on this continuation. Frozen snapshot `/tmp/opensip-design-corrections/candidate-subject.v25`: 12,869 files, 735,108,187 bytes. `verifiedManifest=true`.

## Original missed read (corrected)

Root audited the original public `read_file` deliveries. `docs/v2/contracts/product-v1/identity-and-evidence.md` lines **1281–1349 inclusive were never delivered**. Surrounding reads ended at line 1280 and resumed at line 1350. The original `contractsReadCompletely[].readCompletely=true` assertion for that file was therefore **false**.

This continuation read those exact frozen bytes (file sha256 `afded6d3ac36009b7241d5b353d7b67b515ad5be31ce6ff7f5172e32dab29a1a`, 119956 bytes, 1660 lines) and the owners they cite. Unrelated passing suites and the 32 independent probes were **not** rerun. No frozen/live design or prior review evidence was edited.

## Assessment of the previously unread §3/§4 boundary

The missed block is identity §3's closing statement of four already-owned laws, immediately before §4.

1. **Plan budget equality.** The Plan's deterministic `budget` must equal, exactly and by type, `analysis.budget` of the committed resolved semantic configuration the same Plan names. Neither copy silently wins: a legitimate override enters resolved semantic configuration first (admission-and-qualification §1.1 layered resolution: compiled defaults, then global/project/interactive-local/flags), and the Plan carries that same `{unit, limit}`. A contradicting Plan is refused (`PLAN_BUDGET_CONFIG_JOIN` at retained Run closure). Both values already enter PlanId, so identity/replay/determinism are unchanged; the closed defect is admission disagreement between two conforming implementations. This matches admission §1.1 (`analysis` always contains the complete `{unit,limit}` budget), `identity-schemas.v3.json` plan/semantic-configuration descriptions, and `identity-model.py` / `identity-model.v3.py` `C.equal_typed`.

2. **Coverage scopes partition.** Disjointness is the general rule, applies to every relation, and is decided at retained Run closure. Two Coverage scopes of one view that share the full owning tuple `(snapshotId, relation, resolution, sourceUniverse, targetUniverse)` must carry disjoint subject sets. The key is the relation registry `coveragePartitionLaw.partitionKey` and is the same tuple `coverageTotality` matches facts on. Violation refuses `SUBJECT_SCOPE_PARTITION_OVERLAP` naming relation, rung, and offending subject. A differing tuple is a different claim, not an overlap. Three published boundaries hold: per view (two views of one Run may reference the same scope); every scope the view references, including scopes with no Coverage entry (those bypass the per-Coverage producer guard `admit_coverage_result_v3` but still reach the retained-scope ladder); decided here, not by the producer. This matches native-evidence §1.2, `relation-payload-schemas.v2.json#/x-opensip-relation-registry/coveragePartitionLaw`, and identity-model `close_run`.

3. **Fact totality versus evaluator3 census.** Native `coverageTotality` for `file@enumerated` requires a fact for every inventoried subject claimed as examined, joined to that scope's snapshot, relation, rung, and both universes. Other relations do not acquire a fact-per-source obligation. Evaluator3 independently requires the selected subject census (enumeration contract): Plan selects programs and expected inventory locators before facts/findings exist; every expected inventory has complete/partial/unavailable including empty populations; omitted expected outcome is structural refusal (`ENUMERATION_INVENTORY_MISSING_RECORD`); legitimate partial remains uncertainty evidence and known subjects still evaluate. Symbol attributions remain trusted extraction evidence; retention makes them replayable inputs and does not independently establish compiler truth. Execution-inputs separately accounts for every selected analysis cell. This matches native §1.2, enumeration-contract.v1, and execution-inputs-contract.v1.

4. **`complete` is not vacuous where no totality row exists.** It remains a claim about the examined partition, held by committed Coverage evidence: RC-0 decides the registered `(relation, rung)` pair before any fact is read; RC-1 (native owner: applicability / not-applicable minting over the resolved-rung set) keeps resolution claims off non-resolved rungs, which is why enumeration completeness stays a different claim from resolution completeness (native states that split explicitly at RC-3/RC-6); RC-2 forces `unresolvedEdgeClasses` to equal the admitted `unresolved-edge` facts of the view and never lets a zero edge count imply `complete`. `examinedUniverse` carries the counts. `partial`/`not-attempted`/`unknown` with a disclosed deficiency stay representable. The fact/scope join is existential: in a view carrying two universes a fact of one lawfully sits beside a scope of the other and must not discharge its obligation. No arbitrary payload schema supplied by an import becomes an admitted schema (payload-registry closed list). These match native RC-0..RC-6 and the closed import payload registry.

No missed, conflicting, or under-specified **semantic** contract in this previously unread span meets the MUST/SHOULD bar (exact owner, concrete consequence/reproducer, required minimal remedy). Two observations remain advisories, not blockers: native §1.2 and the registry standing field still quote identity §3's historical sentence “partition the claimed universe without overlaps or omissions”, which this rewritten paragraph no longer contains (the two-halves split is agreed and enforced); identity's one-line RC-1 gloss names the enumeration/resolution split, which native assigns to RC-3/RC-6 while native RC-1 is applicability. Native remains the RC-* owner. Neither observation changes admission.

Reconsidered verdict after this read: still **ACCEPT**. Original probes, pin-gate, and source-pinned launcher receipts are retained as completed, not re-executed.

## What this successor is

v25 is the frozen **target-identity and proof-contract** successor over source24. Output profile remains 3; native/input identities remain profile 2; PolicyDocument2, required `executionInputsDigest`, and the two required Plan parameters (EnumerationPlanV1, EvaluatorEmissionPlanV1) stay separate axes. Historical source21 is inherited provenance only.

The selected occupancy schema is **TargetAttributionV2**. Worker delivery is **OccupancyCompanionV1** on negotiated **FactBatchV3** (`target-attribution-v2` is an additional optional capability, not an identity token). The host `buffer_fact_batch_occupancy` runs during ANALYZING against required **DispatchBindingV1**; `bind_worker_occupancy` projects V2 after fact2 mint and stageReceipt, filling `planId` / `sourceFactId` / `producerClosure` from retained Plan/stage-spec/view membership. The COMPLETE58 post-fact2 envelope is not delivery. Historical V1 attribution is refused (`TARGET_ATTRIBUTION_SCHEMA_VERSION`). Frozen24 Runs remain replayable only under frozen24’s own selected V1 schema.

Portable occupancy identity (file LogicalPath / packageName+packageManifestPath / symbol SubjectIdV1) is distinct from opaque payload `SubjectIdV1`. Host MUST NOT parse `namespace:opaque` spelling. Exact-id ephemeral projection is independent of sidecar attestation; known ephemeral fields win over sidecar unknown; C15 first-party identity disagreement refuses.

Query schema major 3 strengthens only `graph.neighbors` / `graph.path` / `graph.reach`. All twenty operation names are unchanged. Graph endpoints use occupancy-identity vertices. Traversal completion is not native closed-world. `hydradb-dispositions.proposed.md` accounts all eight proposals without choosing a graph database or claiming measured performance.

Composition §9 is reconstructible: witnesses have no `inputRefs`; atomic `predicateProofs[].inputRefs` equal the complete admitted evaluation input selection; boolean nodes take the canonical union of children; consulted `coverageIds`/`scopeIds` may be narrower; originating required-cell refs are retained beside the execution-inputs digest.

Closure-kind is enforced at each actual owner. Occupancy joins the execution-plan stage-spec **provider** closure, not EnumerationPlan `enumerator.closureId`. Cached payloads and structural `open_run_closure` are not semantic authority.

## Cross-owner joins assessed

Discovery/zero-config/installed availability, typed configuration/admission/authority ordering, acyclic full source/Plan/native/evaluator/proof/evidence/Run, complete enumeration and negative knowledge, atom witnesses/target-attribution/incoming completeness, host-captured execution inputs and candidate-only paths, three-valued composition/waivers/budgets, stable correspondence and unmatched findings, source-bound portable baseline and E0..E4 with non-substituted evidence, optional tree-bound detector listing (component manifest is a different body), import/test/runtime/history evidence, invocation and repair authority, SEAL full replay vs prefix dispatch, output/common fault routes, and capability/platform/qualification boundaries were read as one design.

The previously unread identity §3 budget/partition/totality/RC-0..2 span was assessed against those same owners on this continuation. No new MUST/SHOULD.

Explicit algorithm freedom is not a missing contract. Product/compiler/OS/crypto qualification is future work. Synthetic TCB observations are assumptions.

## Independent probes (original session; not rerun)

Python: `/tmp/opensip-architecture-review-env/bin/python -I -B`. Script `probes/independent-probes.v1.py`, 32 cases, all passed. Receipts remain under `/tmp/opensip-design-corrections/grok-independent-design.v25/probes/`.

- **Proof boundary.** Honest graph: `close_run` equals `open_run_closure`. Fully reminted severity change and false-pass verdict: owner `open_run_closure` **ADMIT**, `close_run` **REFUSE** `EVALUATOR_COMPLETE_PROOF_REPLAY`. Structural admission is not semantic authority.
- **Cross-unit occupancy.** Buffer during ANALYZING does not require receipts. `retainedStageOrdinal=7` is not `analyzeRequestOrdinal=0`. Host-projected V2 `evaluationNativeId=src/a.ts` is not opaque `targetNativeId=file:src/a.ts`. Extra companion ordinal refuses. V3 without the token refuses `PROVIDER_RETURN_UNNEGOTIATED_V3`. V1 sidecar refuses. C15 ephemeral/sidecar first-party conflict refuses. Producer kind is provider, not enumerator.
- **Retained graph query.** `execute_graph_query` after `close_run` on an imports graph: first-party file vertex is inventory `a.ts`, not payload `file:a.ts`. `host.targetAttributions` does not grant occupancy. `{latest:true}` without trusted observation is `QUERY.VIEW_UNKNOWN` and a `kind=failure` envelope with no `run`. Syntactic rung is `QUERY.RELATION_UNSUPPORTED`. Evidence disclosure is present independently of row count. Schema major 2 is unsupported.

Pin-gate: mutating `admission-and-qualification.md` in the disposable copy made `run-evaluator3-checks.py` refuse (`sourcePinsValid=false`, no checks executed). The file was restored to its pinned hash.

## Source-pinned launchers (original session; not rerun)

Pin ledgers were byte-identical to the frozen snapshot and verified before execution. Receipts remain under `/tmp/opensip-design-corrections/grok-independent-design.v25/pinned-runs/`.

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
3. Native-evidence §1.2 and `coveragePartitionLaw.standing` still quote identity §3 as “Coverage scopes partition the claimed universe without overlaps or omissions”. Identity §3 now says partition has two halves with different owners and no longer contains that sentence. The two-halves split is agreed and enforced; this is a stale citation, not an admission disagreement.
4. Identity §3's one-line RC-1 gloss (“keeps enumeration completeness separate from resolution completeness”) points at a split native states at RC-3/RC-6. Native RC-1 is applicability / not-applicable minting. Native remains the RC-* owner. Compressed summary, not a second RC-1 law.

## Application routing (not applied grades)

All AR-01..AR-16, FW-01..FW-15, DR-001..DR-011, DR-011-R01..R16: `ROUTING-ASSESSED-ONLY-NOT-APPLIED`, `appliedByThisReview=false`, `finalApplicationOutcomeGranted=false`.

DR-201..DR-205: `ROUTED-ONLY`, same two false flags. Historical ACCEPTED standing is provenance of a different subject.

Retained: 30 evaluation residuals; 28 condition-2 obligations (DR-101–107, 109–115, 117–127, 130/131/133). All 32 product qualification gates (DR-G01..G32) remain unperformed.

## Limitations

Not a blind consumer reconstruction. Not Claude review. Not implementation or application authorization. Reference models use synthetic TCB observations. This continuation is the same reviewer completing a missed public read, not a second independent review.

Machine record: `review.json`.
