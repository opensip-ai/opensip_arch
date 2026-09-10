# Independent design review — candidate-subject.v25 (read-completion continuation 2)

**Verdict: ACCEPT**

This is the same fresh-origin Grok session continued, not a new independent reviewer and not a new blind. Original session id `01a085b3-3a90-7082-a261-3ba4e7e453c4`; origin `/tmp/opensip-design-corrections/grok-independent-design.v25`. Original review bytes and continuation-1 bytes are preserved unchanged. Not Claude; no Claude agreement is claimed. Architecture/design/schema/reference only. No grade, activation, implementation authorization, or application approval.

Subject manifest `fa8cdc796c4dbab514c8b8a91a593b740e3f8e69d19574f4be11c6e00c3a536d` re-verified equal on this continuation. Frozen snapshot `/tmp/opensip-design-corrections/candidate-subject.v25`. `verifiedManifest=true`.

## Original missed reads (corrected across continuations)

Root audited all 19 files the original machine report claimed were read completely.

1. **Continuation 1 (already written, preserved).** `docs/v2/contracts/product-v1/identity-and-evidence.md` lines **1281–1349** were never delivered (surrounding reads ended 1280, resumed 1350). Assessed; no MUST/SHOULD.
2. **This continuation.** Two further tails were never delivered in the original 51-turn review:
   - `docs/coop/design-corrections/foundation/atom-evaluation-contract.v1.md` lines **161–175** (file sha256 `6c4e3bb0a57e693e55c94f509c1f5e8636648712062d57d29c3b968f03835ba2`, 23689 bytes, 175 lines; this is the file tail: §8 API and §9 conceptual cases).
   - `docs/coop/design-corrections/foundation/provider-target-attribution-return.schema.v2.json` lines **161–252** (file sha256 `2d5719b57dc65095278287d173280f789f684737af30a45fc7114e020efa523f`, 19137 bytes, 252 lines; this is the file tail: syntax-only `never`, clone-candidate, closed `never` list, C15 reproducible operand, `x-opensip-new-internal-faults`).

All other claimed files were fully delivered apart from identity 1281–1349. The original `readCompletely=true` assertions for these two files were therefore **false**. This continuation read those exact frozen tails and the owners they cite. Unrelated suites and the 32 independent probes were **not** rerun. No frozen/live design or prior review evidence was edited.

## Assessment of the previously unread atom §8–§9 tail

`evaluate_atom(atom, subject, inputs) → AtomResult` and `admit_atom_inputs(inputs)` are the closed API. Global admission runs even when the policy has no atoms: IncomingSearchV1, TargetAttributionV2 (unused members included), every `planSelectedImportIds` wrapper/scope/flag, and observation/payload joins. Missing selected wrappers refuse `ATOM_IMPORT_WRAPPER_MISSING`. Closed input keys are `evaluator-projection-registry.v1.json#/closedAtomInputs.keys`. `coverageScopes` is `coverage2 → scope2`. `importFlagsAdapter` is `import2 → {consumable, staleness}`. Full scan of owner-admitted facts/imports/scopes/Coverage; no producer expected matches and no oracle/callback flags. Reuses `native_evidence_model.v2.sufficiency_v2` on constructed view entries and does **not** call repair `imported_requirement_outcome`. Return fields are `value`, `knownFactIds`, `uncertainFactIds`, `knownObservationAddresses`, `uncertainObservationAddresses`, `coverageIds`, `scopeIds`, `evaluationInputRefs`, `causes`, `nativeDeficiencies`, `disclosures`. `check-atoms.v1.py` is shape plus discriminating unit checks, not full Run replay.

Those laws match `atom_model.v1.py` (`admit_atom_inputs` docstring, `CLOSED_INPUT_KEYS`, `_result`), the projection-registry closed-key list, atom contract §2 (already delivered: global sidecar admission), native sufficiency, and workflows repair remaining a different owner. §9’s conceptual-case catalog matches the discriminating atom/occupancy checks already exercised (C15, V1 sidecar, missing wrapper with no atom, packageManifestPath, occupancy unknown vs none, mixed-atom global admission).

One parenthetical does not match the closed-key owner: §8 names `ATOM_ORACLE_FLAG_REFUSED` for oracle/callback flags, while the registry and `check-atoms.v1.py` `test_oracle_refused` refuse extra keys such as `expectedValue` as `ATOM_INPUT_KEY_UNKNOWN`. Both refuse; no graph is admitted. Advisory, not a second oracle-flag law.

## Assessment of the previously unread provider-return schema tail

The missed JSON completes the language-mode table and publishes the C15 operand plus the internal-fault registry.

- **syntax-only `never`:** do not advertise resolved imports/file/package occupancy from syntax-only. Complements the already-delivered “omit the attribution token; exact-id ephemeral may resolve symbols; do not invent file/package occupancy from specifier text.” Token omission is FactBatchV2 / occupancy-unknown except exact-id ephemeral, not `PROVIDER_RETURN_UNNEGOTIATED_V3` (that key is V3 payload without Hello token).
- **clone-candidate:** omit the token; candidate member identities are not evaluation-subject identities. Matches enumeration candidate-only cells (`kinds=[]`) and the already-delivered occupancy “never” for clone member IDs.
- **Closed `never` list:** host must not parse `SubjectIdV1` namespace; must not deny advertised file/package target support; must not treat host filesystem/package-manager/cache as provider attestation; must not add a protocol3 or typescript-semantic frame named TargetAttribution; must not add target-attribution to a view-only stage `outputDomains`; must not write ephemeral exact-id projection as this envelope or as TargetAttributionV2. Matches atom contract §2, schema `x-opensip-identity.not` / `notInputs` / `producerSupply.authority` (already delivered).
- **C15:** if ephemeral exact-id first-party identity `I_eph` and sidecar first-party identity `I_sc` disagree, refuse `TARGET_ATTRIBUTION_EPHEMERAL_IDENTITY_CONFLICT` and do not overwrite. Occupancy identity is `(kind, evaluationNativeId)` for file/symbol and `(kind, evaluationNativeId, packageManifestPath)` for package. Reproducible operand: inventory `file:src/a.ts` and `src/b.ts`; payload equals `file:src/a.ts`; sidecar `evaluationNativeId=src/b.ts`. Agreement: equal identities admit; unknown sidecar keeps ephemeral; external vs first-party remains `TARGET_ATTRIBUTION_EXTERNAL_CONTRADICTS_FIRST_PARTY`. Matches atom contract §2, `target-attribution.schema.v2.json` precedence/conflictUniqueness, and the original C15 probe.
- **`x-opensip-new-internal-faults`:** internal keys are not DomainDetailCode and not D9. Public route is the existing evaluator-fault observation: provider-return `EVALUATION.INPUT_REFUSED` / `PROVIDER.PROTOCOL_VIOLATION`; host-internal `HOST.INVARIANT_VIOLATED`. LIVE D9 successor-artifact is not discharged. Schema/join key lists include the keys the original occupancy probes used (`PROVIDER_RETURN_UNNEGOTIATED_V3`, `PROVIDER_RETURN_DISPATCH`, `PROVIDER_RETURN_UNKNOWN_CANDIDATE`, `TARGET_ATTRIBUTION_SCHEMA_VERSION`, `TARGET_ATTRIBUTION_EPHEMERAL_IDENTITY_CONFLICT`). Matches already-delivered `errorHandling` (same file, lines 122–131) and evaluator-fault-contract.v3.md.

No missed, conflicting, or under-specified **semantic** contract in these previously unread tails meets the MUST/SHOULD bar (exact owner, concrete consequence/reproducer, required minimal remedy). Reconsidered verdict after this read: still **ACCEPT**. Original probes, pin-gate, and source-pinned launcher receipts are retained as completed, not re-executed.

## What this successor is

v25 is the frozen **target-identity and proof-contract** successor over source24. Output profile remains 3; native/input identities remain profile 2; PolicyDocument2, required `executionInputsDigest`, and the two required Plan parameters (EnumerationPlanV1, EvaluatorEmissionPlanV1) stay separate axes. Historical source21 is inherited provenance only.

The selected occupancy schema is **TargetAttributionV2**. Worker delivery is **OccupancyCompanionV1** on negotiated **FactBatchV3** (`target-attribution-v2` is an additional optional capability, not an identity token). The host `buffer_fact_batch_occupancy` runs during ANALYZING against required **DispatchBindingV1**; `bind_worker_occupancy` projects V2 after fact2 mint and stageReceipt, filling `planId` / `sourceFactId` / `producerClosure` from retained Plan/stage-spec/view membership. The COMPLETE58 post-fact2 envelope is not delivery. Historical V1 attribution is refused (`TARGET_ATTRIBUTION_SCHEMA_VERSION`). Frozen24 Runs remain replayable only under frozen24’s own selected V1 schema.

Portable occupancy identity (file LogicalPath / packageName+packageManifestPath / symbol SubjectIdV1) is distinct from opaque payload `SubjectIdV1`. Host MUST NOT parse `namespace:opaque` spelling. Exact-id ephemeral projection is independent of sidecar attestation; known ephemeral fields win over sidecar unknown; C15 first-party identity disagreement refuses.

Query schema major 3 strengthens only `graph.neighbors` / `graph.path` / `graph.reach`. All twenty operation names are unchanged. Graph endpoints use occupancy-identity vertices. Traversal completion is not native closed-world. `hydradb-dispositions.proposed.md` accounts all eight proposals without choosing a graph database or claiming measured performance.

Composition §9 is reconstructible: witnesses have no `inputRefs`; atomic `predicateProofs[].inputRefs` equal the complete admitted evaluation input selection; boolean nodes take the canonical union of children; consulted `coverageIds`/`scopeIds` may be narrower; originating required-cell refs are retained beside the execution-inputs digest.

Closure-kind is enforced at each actual owner. Occupancy joins the execution-plan stage-spec **provider** closure, not EnumerationPlan `enumerator.closureId`. Cached payloads and structural `open_run_closure` are not semantic authority.

## Cross-owner joins assessed

Discovery/zero-config/installed availability, typed configuration/admission/authority ordering, acyclic full source/Plan/native/evaluator/proof/evidence/Run, complete enumeration and negative knowledge, atom witnesses/target-attribution/incoming completeness, host-captured execution inputs and candidate-only paths, three-valued composition/waivers/budgets, stable correspondence and unmatched findings, source-bound portable baseline and E0..E4 with non-substituted evidence, optional tree-bound detector listing (component manifest is a different body), import/test/runtime/history evidence, invocation and repair authority, SEAL full replay vs prefix dispatch, output/common fault routes, and capability/platform/qualification boundaries were read as one design.

Continuation 1 assessed the previously unread identity §3 budget/partition/totality/RC-0..2 span. This continuation assessed the previously unread atom API/cases tail and provider-return C15/fault-registry tail. No new MUST/SHOULD.

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
3. Native-evidence §1.2 and `coveragePartitionLaw.standing` still quote identity §3 as “Coverage scopes partition the claimed universe without overlaps or omissions”. Identity §3 now says partition has two halves with different owners and no longer contains that sentence. The two-halves split is agreed and enforced; this is a stale citation, not an admission disagreement. (Continuation 1.)
4. Identity §3's one-line RC-1 gloss (“keeps enumeration completeness separate from resolution completeness”) points at a split native states at RC-3/RC-6. Native RC-1 is applicability / not-applicable minting. Native remains the RC-* owner. Compressed summary, not a second RC-1 law. (Continuation 1.)
5. Atom contract §8 parenthetically names `ATOM_ORACLE_FLAG_REFUSED` for oracle/callback flags. Closed input keys are owned by `evaluator-projection-registry.v1.json#/closedAtomInputs`; extra keys including `expectedValue` refuse `ATOM_INPUT_KEY_UNKNOWN` (`atom_model.v1.py`, `check-atoms.v1.py` `test_oracle_refused`). Both refuse. The parenthetical key is not a second oracle-flag law and is not an admission disagreement. Visible only after the missed atom tail was read.

## Application routing (not applied grades)

All AR-01..AR-16, FW-01..FW-15, DR-001..DR-011, DR-011-R01..R16: `ROUTING-ASSESSED-ONLY-NOT-APPLIED`, `appliedByThisReview=false`, `finalApplicationOutcomeGranted=false`.

DR-201..DR-205: `ROUTED-ONLY`, same two false flags. Historical ACCEPTED standing is provenance of a different subject.

Retained: 30 evaluation residuals; 28 condition-2 obligations (DR-101–107, 109–115, 117–127, 130/131/133). All 32 product qualification gates (DR-G01..G32) remain unperformed.

## Limitations

Not a blind consumer reconstruction. Not Claude review. Not implementation or application authorization. Reference models use synthetic TCB observations. This continuation is the same reviewer completing missed public reads, not a second independent review.

Machine record: `review.json`.
