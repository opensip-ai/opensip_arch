# Independent design review — OpenSIP source37

**Verdict: CHANGES_REQUIRED.** No MUST issue was found. Three new SHOULD issues (S37-01 whole-Run cause order/coverageId, S37-02 report hooks versus product boundary, S37-03 query advisory cross-join) need owner corrections before ACCEPT. The reference groups, planning checks and author package verification all pass on verified exact copies.

- Subject manifest: `/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v37.json`, SHA-256 `245ef613243aafeaac2dcdca7f0b398d5a770ec338abbf712039fdfd91676680` (verified).
- Archive: SHA-256 `f840507695e310811656a167cbef96b7e3c5ea43d400d0ecf61ef5088d659920`, 12900 members, every member verified.
- Parent36: snapshot verified. Delta: 1 added, 15 changed files (`receipts/parent-delta.json`).
- No grade, activation, application or implementation authorization is granted.
- This is not a blind reconstruction, and source36 acceptance does not cover source37.

## New MUST issues

None found.

## New SHOULD issues

### S37-01 — Whole-Run primary/secondary cause order and coverageId attribution have no owner; the host termination is not a function of the sealed Run

**Owner selectors**

- docs/v2/contracts/product-v1/native-evidence.md §10 "Native stage selection, and where it stops" lines 2946-2963 ("This section does not define how requirement, proof-cause, import or verdict outcomes are ordered in that reduction")
- docs/coop/artifacts/d9-exit-contract.v1.14.json#/concurrentConditionReducer (primary=deficiencies[0] in pre-reduction host input order) and #/causeModel/codeDerivation
- docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json#/$defs/StepTermination (reasonCodes x-opensip-order sequence; coverageId optional, no selection law)
- docs/coop/design-corrections/workflows/workflow-projection-contract.v3.md line 138 (EVALUATION.WORK_BUDGET_EXHAUSTED: sealed Run "may reuse" budget-exhausted)
- docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md §5 / evaluator_composition_model.v3.py compose(): ruleResults[].deficiencies and executionDeficiencies retained only as canonical sets
- docs/v2/contracts/product-v1/workflows-and-surfaces.md §9 D9 goldens and typed detail (host finalizer owner, no ordering law)

**Consequence.** Two conforming host finalizers can emit different reasonCodes[0] (the remedy class a caller acts on first, D9 TO-7), different secondary order, and a different or absent coverageId for byte-identical sealed Run evidence. The retained proof keeps deficiencies only as canonical sets, so no verifier can re-derive which termination was lawful, D9 goldens cannot pin it, and query/command parity of the enclosing termination is not reproducible across hosts. Class and exit (indeterminate/3) and all identities are unaffected, hence SHOULD rather than MUST.

**Reproducer**

- **A.** Actual closed indeterminate Run run3:f9b48563b2a7a96f9ee8637eb2db5c277ac2b466c424d2f9010825dad94d801b carries 2 deficient Coverage records (both resolution-incomplete); StepTermination with either coverageId, or none, is schema-valid (True). Retained deficiency order is the canonical set order (True). Native cause coverage-unknown has no D9 or native-bridge route.
- **B.** Actual native run_termination over a clean budget-exhausted stage terminal and a resolution-incomplete entry returns stage primary COVERAGE.BUDGET_EXHAUSTED while the typed detail names resolution-incomplete, so a coverageId naming that record carries a deficiency whose route differs from reasonCodes[0].
- **C.** D9 reducer applied to the same three concurrent conditions from different owners (requirement sufficiency required-relation-missing, native stage terminal budget-exhausted, verdict composition verdict-indeterminate) in the six lawful pre-reduction orders gives 6 distinct schema-valid reasonCodes sequences and primary codes ['COVERAGE.BUDGET_EXHAUSTED', 'COVERAGE.REQUIRED_RELATION_MISSING', 'VERDICT.INDETERMINATE'].
- Receipts: `receipts/probe-cause-attribution.json`, `receipts/probe-semantic-boundaries.json#P-CAUSE`.

**Minimal remedy.** In one owner (the host finalizer section of workflows-and-surfaces §9, or a D9 successor row), define a total pre-reduction order across condition sources as a function of retained Run content (for example native stage selections by §10 precedence, then requirement sufficiency, then required execution/import obligations, then verdict-indeterminate last, canonical tie-break); make the evaluator-only cause bridge explicit (coverage-unknown, required-cell-unsatisfied, incomplete-inventory and import causes route through verdict-indeterminate; replace "may reuse" for work-budget-exhausted with MUST or MUST NOT); and select coverageId deterministically (for example the canonically least coverage2 whose entry.deficiency equals the primary, omitted when the primary has no entry carrier). Add retained goldens for A, B and C.

Related rows: AR-16, DR-007, DR-011-R08, FW-06, FW-08.

### S37-02 — Prototype report inventory selects executable "registered external report hooks" in a worker lane, contradicting the selected product boundary and without any owner

**Owner selectors**

- docs/v2/architecture/prototype-report-inventory.md:37 (R02 "Registered external report hooks execute only in the supervised isolated worker lane; there is no in-host fallback")
- docs/v2/architecture/prototype-report-inventory.md:179 (R24 External tools "isolated registered report hooks")
- docs/v2/contracts/product-v1/admission-and-qualification.md §5 items 1, 3, 4 and 5 (lines 341-345: one first-party registry; only the host owns rendering; no untrusted native/WASM admission and no sandbox claim; imperative contributions/project hooks not admitted)
- docs/v2/architecture/implementation-coverage.v1.json groups.reportFeatures R02/R24 (owners apps/report/src/report-view.ts and crates/reporting/src/projection.rs only; no worker-lane owner, schema, D9 route or gate)

**Consequence.** The planning inventory, which chapter 14 and the file inventory ask reviewers to accept as R01-R24 dispositions, directs implementers toward an executable external rendering-hook lane that the product boundary excludes. Accepting R02/R24 as written would silently widen scope and the trusted-code account (TCB-SCOPE-01) without admission contract, isolation claim, failure route or qualification gate; rejecting it leaves no stated replacement for external-tool presentation.

**Reproducer**

Text comparison of the cited selectors; searching all non-review snapshot docs for "report hook" or "external report" finds only prototype-report-inventory.md lines 37 and 179.

**Minimal remedy.** Replace the hook language in R02 and R24 with versioned host-approved data projections only (no executable report hooks), or route an explicit reviewed scope change through admission §5 with an owner, admission schema, D9 routes and gate.

Related rows: DR-010, DR-011-R16, DR-205, AR-15.

### S37-03 — GraphQueryResponseV1 admits advisory=true for non-advisory non-graph operations although the contract and schema description say advisory is true exactly for four operations

**Owner selectors**

- docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json#/$defs/GraphQueryResponseV1/allOf[4] (AdvisoryOperation then advisory const true; no else branch), lines 1164-1190
- graph-query.schema.json#/$defs/GraphQueryResponseContext/properties/advisory (type boolean), lines 947-950, versus the schema description at line 5 ("false for graph.* and the remaining non-advisory operations")
- docs/v2/contracts/product-v1/workflows-and-surfaces.md:1050-1066 ("advisory is true exactly for comparison.diff, candidate.list, inspection.show and review.brief"; query-response is the complete owner-admitted GraphQueryResponseV1)

**Consequence.** A finding.list or run.show response labelled advisory passes owner schema admission, and so does the query-response parity field built from it. Renderers and agent consumers that rely on admission for the Control versus Map authority distinction can present authoritative findings as advisory. The half-enforced "exactly" law is not caught by the existing controls, which only test the graph-true and advisory-diff-true branches.

**Reproducer**

- **results.** {"run.show advisory=true (non-advisory op)": true, "finding.list advisory=true (non-advisory op)": true, "candidate.list advisory=false (advisory op)": "INVALID:exact const type/value mismatch", "run.show advisory=false": true, "run.show context omitted advisory": "INVALID:'advisory' is a required property", "graph response without evidence": "INVALID:'evidence' is a required property", "graph response resolvedView latest": "INVALID:Additional properties are not allowed ('latest' was unexpected)", "graph response advisory true": "INVALID:exact const type/value mismatch"}
- Receipts: `receipts/probe-query-boundary.json#Q4`.

**Minimal remedy.** Add else: advisory const false for operations outside AdvisoryOperation (a schema successor with re-registration if these bytes are registered), plus negative controls for run.show and finding.list.

Related rows: AR-13, HYDRA-3.

## Advisories (separate from issues)

### A37-01 — carrierFormat 3 DDL grammar CHECKs verify only the first character after the prefix

GLOB patterns "op-[0-9a-f]*", "run3:[0-9a-f]*" and "[0-9a-f]*" with a length check admit uppercase or non-hex tails; body_sha256/prev_sha256 and attempt_custody execution_id have length-only checks. Probe admitted op-a+Z*31, run3:c+Q*63, non-hex body_sha256, project_key_digest and migration_op_ref, and a non-hex execution_id. The inherited carrierFormat 2 DDL has the same pattern. carrier-format.v3.md:158 states the grammar as a preserved law.

- Selectors: `docs/coop/design-corrections/security/grant-journal.carrier.v3.sql:21-22,30-32,48-49,56-60`; `docs/v2/architecture/attempt-custody.schema.v1.json#/proposedPrivateDDL`; `docs/coop/design-corrections/security/carrier-format.v3.md:158`.
- Receipt: `receipts/probe-carrier-ddl.json`.
- Disposition: ROUTE-TO-IMPLEMENTATION-DDL: add a "NOT GLOB '*[^0-9a-f]*'" tail test or state that host record admission alone owns grammar and the DDL is defence in depth only.

### A37-02 — first_generation law is not DDL-enforced in the {A,B} footprint

With the v3 objects present and no carrier_format row, an append at grantGeneration 1 is admitted, and the row is then published with first_generation=5 while v3 holds generation 1. The carrier-migration {A,B} resume procedure verifies definitions, not rows.

- Selectors: `docs/coop/design-corrections/security/grant-journal.carrier.v3.sql`; `docs/coop/design-corrections/security/carrier-migration.v1.md:159`; `docs/coop/design-corrections/security/carrier-dispatch.v3.json:322`.
- Receipt: `receipts/probe-carrier-ddl.json`.
- Disposition: ROUTE-TO-CARRIER-OWNER: at act C require grant_journal_v3 to be empty, or add a publication-time check that no v3 row precedes first_generation.

### A37-03 — MIGRATION.CORRUPT carries a projectKeyDigest mismatch that may be a swapped carrier

carrier-dispatch.v3.json:212 and carrier-format.v3.md:274 route a published carrierFormat 3 projectKeyDigest mismatch to MIGRATION.CORRUPT (LEDGER.CORRUPT). S12:1306 routes a foreign or swapped carrier on read-only recovery to EXTENSION.ADMISSION_REJECTED/RECOVERY.REFUSED, and S12:1308 explicitly keeps MIGRATION.CORRUPT to one remedy. Partial-object and definition failures of the migration itself are coherent uses.

- Selectors: `docs/coop/design-corrections/security/carrier-dispatch.v3.json:212`; `docs/coop/design-corrections/security/carrier-format.v3.md:274`; `docs/v2/contracts/product-v1/security-and-lifecycle.md:1300,1306,1308`.
- Disposition: ROUTE-TO-SECURITY-OWNER: state whether a digest mismatch is migration corruption or foreign binding on each path.

### A37-04 — F46 unknown-carrier-incompatible and F51 split-brain-custody-condition have no public projection row

The build plan and commit-recovery plan define these conclusions, but neither S12 nor commit-recovery-readonly.v3 gives a class, exit or code for them.

- Selectors: `docs/v2/architecture/implementation-boundaries-and-build-plan.md:578,583`; `docs/v2/architecture/commit-recovery-plan.v1.json:562,612`; `docs/v2/contracts/product-v1/security-and-lifecycle.md §S12`; `docs/v2/architecture/commit-recovery-readonly.v3.md §1`.
- Disposition: ROUTE-TO-SECURITY-OWNER: add the two rows before F46/F51 implementation.

### A37-05 — Unknown graph availability observation value is silently ignored

The reference treats host availability "not-a-state" like an omitted observation (ADMIT; close_run still decides). Query §7 names only purged/expired/corrupt/unavailable, retained/partial and omitted; "missing" is also accepted as a direct host report.

- Selectors: `docs/coop/design-corrections/workflows/query-projection-contract.v3.md:160`; `docs/coop/design-corrections/workflows/query_projection_model.v3.py:1425-1450`.
- Receipt: `receipts/probe-query-boundary.json#Q3`.
- Disposition: ROUTE-TO-QUERY-OWNER: state that an out-of-vocabulary observation is a host invariant violation, or that it is ignored.

### A37-06 — Complete-replay disagreement on the graph query path collapses into the corrupt-retained-bytes row

Fully reminted false-result Runs are refused by the query with HOST.IO_FAILURE/evidence.corrupt, subject EVALUATOR_COMPLETE_PROOF_REPLAY. Identity §4 (lines 1465-1467) keeps complete replay disagreement a distinct typed boundary observation, but query §7 has no row for it.

- Selectors: `docs/coop/design-corrections/workflows/query-projection-contract.v3.md:162-177`; `docs/v2/contracts/product-v1/identity-and-evidence.md:1465-1467`.
- Receipt: `receipts/probe-semantic-boundaries.json#P-REMINT`.
- Disposition: ROUTE-TO-QUERY-OWNER: add an explicit row; evidence.corrupt is acceptable if chosen deliberately.

### A37-07 — Stale standing prose after the v5 normative-input binding

The build plan still says the planning checker verifies candidate25 (lines 10, 19, 1041, 1045, 1085), but the executed checker binds implementation-normative-inputs.v5 (29 files, all hashes ok). carrier-format.v3.md:4 and commit-recovery-readonly.v3.md:5 say "authored against Source25"; store-instance-lineage.v1.json:469,506 cites an "F00-F37" matrix while the plan has F00-F53.

- Selectors: `docs/v2/architecture/implementation-boundaries-and-build-plan.md:10,19,1041,1045,1085`; `docs/coop/design-corrections/security/carrier-format.v3.md:4`; `docs/v2/architecture/commit-recovery-readonly.v3.md:5`; `docs/v2/architecture/store-instance-lineage.v1.json:469,506`.
- Disposition: EDITORIAL: add current-standing notes in the next successor. No semantic effect found.

### A37-08 — Registered native schema annotation still states a superseded three-code list

The native §10 supersession law (lines 2933-2944) is coherent: editing the annotation would change payloadSchemaDigest and every coverage2 identity. Readers of the schema alone still see the stale list.

- Selectors: `docs/v2/contracts/product-v1/native-evidence.md:2933-2944`; `native-evidence.schemas.v2.json#/x-opensip-deficiency-cause-registry/perRequirementConsumerBoundary/threeDistinctThingsNotToConflate/publicD9Termination`.
- Disposition: ACCEPTED-AS-DESIGNED; fold the correction into the next registered schema successor.

## Independent probes

### P-CROSS — cross-unit claim: evaluator proof and public graph query project the same retained references facts per subject across two native universes

- Script: `probes/probe_semantic_boundaries.py`.
- Receipt: `receipts/probe-semantic-boundaries.json#P-CROSS`.
- Discriminating: yes: a per-subject fact-set equality in both universes would fail under any union, universe conflation or occupancy divergence between atom and query.
- Result: `{"passed": true, "runId": "run3:08079ab5ed5d326e6aceef6baf27ddb79111334e0f78167a1a7f5a8140dad7a7", "mismatches": [], "rows": 3, "crossUniverseEdges": false}`.

### P-TARGET — target/proof boundary: target-side predicate values versus the incoming graph result; an empty or complete traversal is never proof

- Script: `probes/probe_semantic_boundaries.py`.
- Receipt: `receipts/probe-semantic-boundaries.json#P-TARGET-complete,P-TARGET-incomplete`.
- Discriminating: yes: foo is indeterminate in proof while the query returns zero rows with traversal complete, and must disclose incoming-search-incomplete/resolution-not-attempted.
- Result: `{"complete": true, "incomplete": true, "incompleteRows": [{"nativeSubjectId": "symbol:bar", "predicateValue": "false", "queryFactIds": ["fact2:65225291bafa92949578aa66d69d473bea89e9c64cb83af24462975a4b8c30f3"], "queryTraversal": "complete", "queryLimitationKinds": ["incoming-search-incomplete", "resolution-not-attempted"]}, {"nativeSubjectId": "symbol:foo", "predicateValue": "indeterminate", "queryFactIds": [], "queryTraversal": "complete", "queryLimitationKinds": ["incoming-search-incomplete", "resolution-not-attempted"]}]}`.

### P-QUERY — retained graph query boundary: schema-first endpoint admission, package tuple identity, availability mapping, response parity, cursor binding, visit caps

- Script: `probes/probe_query_boundary.py`.
- Receipt: `receipts/probe-query-boundary.json`.
- Discriminating: yes for Q1 (malformed package endpoint with no Run and with a purged observation), Q3 and Q4; Q4 found S37-03.

- Q1 schema-first: True.
- Q2 ambiguous reachable: False.
- Q3 availability mapping: True (unknown state: ADMIT).
- Q4 parity: {"run.show advisory=true (non-advisory op)": true, "finding.list advisory=true (non-advisory op)": true, "candidate.list advisory=false (advisory op)": "INVALID:exact const type/value mismatch", "run.show advisory=false": true, "run.show context omitted advisory": "INVALID:'advisory' is a required property", "graph response without evidence": "INVALID:'evidence' is a required property", "graph response resolvedView latest": "INVALID:Additional properties are not allowed ('latest' was unexpected)", "graph response advisory true": "INVALID:exact const type/value mismatch"}.
- Q5 cursor: {"first-page": ["ADMIT", null], "continue-identical": ["ADMIT", null], "continue-includeStart-omitted(effective false)": ["REFUSE", "QUERY.CURSOR_MISMATCH"], "continue-latest-selector": ["REFUSE", "QUERY.CURSOR_MISMATCH"], "continue-different-page-size": ["ADMIT", null], "includeStart-false-vs-omitted-same-selection": [true, 1, 1]}.
- Q6 caps: {"uncapped": ["ADMIT", "complete"], "cap=visited": ["ADMIT", "complete"], "cap=visited-1 required": ["ADMIT", "truncated-bound"], "cap=visited-1 best-effort": ["ADMIT", "truncated-bound"], "testBounds raise refused": ["REFUSE", null]}.

### P-REMINT — fully reminted false-result graphs (witness blobs, proof, evidence, seal, Run) pass structural owner admission but fail complete replay and every public boundary

- Script: `probes/probe_semantic_boundaries.py`.
- Receipt: `receipts/probe-semantic-boundaries.json#P-REMINT`.
- Discriminating: yes: all three mutants (fail to pass, indeterminate laundered to false, execution deficiency erased) get new valid identities and ADMIT at open_run_closure; close_run and execute_graph_query refuse. These differ from the checker's same-count metadata mutants. The SEAL adapter delegates to close_run by source reading and was not executed..

- **fail-to-pass: known findings erased (declares-exists).**
  - structural `open_run_closure`: ADMIT (new RunId).
  - complete replay: REFUSE `EVALUATOR_COMPLETE_PROOF_REPLAY`.
  - `close_run`: REFUSE.
  - graph query: REFUSE HOST.IO_FAILURE/evidence.corrupt, exit 4.
- **indeterminate-to-pass: unknown laundered to known-false (incoming incomplete).**
  - structural `open_run_closure`: ADMIT (new RunId).
  - complete replay: REFUSE `EVALUATOR_COMPLETE_PROOF_REPLAY`.
  - `close_run`: REFUSE.
  - graph query: REFUSE HOST.IO_FAILURE/evidence.corrupt, exit 4.
- **execution-deficiency erased: missing required inventory to pass.**
  - structural `open_run_closure`: ADMIT (new RunId).
  - complete replay: REFUSE `EVALUATOR_COMPLETE_PROOF_REPLAY`.
  - `close_run`: REFUSE.
  - graph query: REFUSE HOST.IO_FAILURE/evidence.corrupt, exit 4.

### P-CAUSE — whole-Run cause order and coverageId attribution

- Script: `probes/probe_semantic_boundaries.py + probes/probe_cause_attribution.py`.
- Receipt: `receipts/probe-semantic-boundaries.json#P-CAUSE, receipts/probe-cause-attribution.json`.
- Discriminating: yes: several schema-valid terminations for one sealed Run; found S37-01. Part C drives the D9 reducer text over constructed condition lists because no product host finalizer exists; A and B use actual owners.

- Actual run: `{"runId": "run3:f9b48563b2a7a96f9ee8637eb2db5c277ac2b466c424d2f9010825dad94d801b", "verdict": "indeterminate", "findingCount": 0}`.
- Deficient coverage records: 2.
- Causes with no route: ['coverage-unknown'].
- A: {"runId": "run3:f9b48563b2a7a96f9ee8637eb2db5c277ac2b466c424d2f9010825dad94d801b", "deficientCoverageRecords": 2, "allValid": true}.
- B: {"stagePrimaryCode": "COVERAGE.BUDGET_EXHAUSTED", "entryTypedDetailDeficiency": "resolution-incomplete", "differs": true}.
- C: {"distinctPrimaryCodes": ["COVERAGE.BUDGET_EXHAUSTED", "COVERAGE.REQUIRED_RELATION_MISSING", "VERDICT.INDETERMINATE"], "distinctCodeSequences": 6, "allValid": true}.

### P-CARRIER — carrierFormat 3 DDL enforcement of its stated grammar and first_generation law

- Script: `probes/probe_carrier_ddl.py`.
- Receipt: `receipts/probe-carrier-ddl.json`.
- Discriminating: yes; found A37-01 and A37-02.
- Result: `{"v3Sha256": "23902324163196cfb8203a2a016072fd16a3b7a53c82e518e26c0c4fff0e863b", "v3_lawful_seal": "ADMIT", "v3_op_ref_nonhex_uppercase": "ADMIT", "v3_run_id_nonhex_tail": "ADMIT", "v3_body_sha256_nonhex": "ADMIT", "v3_project_key_digest_nonhex_tail": "ADMIT", "v3_migration_op_ref_nonhex_tail": "ADMIT", "attempt_custody_execution_id_nonhex_tail": "ADMIT", "v3_append_without_format_row_gen1": "ADMIT", "v3_row_published_after_lower_generation_append": {"formatRowAdmitted": true, "v3GenerationsBelowFirst": [1]}, "v2_operation_ref_check_text": ["operation_ref TEXT   NOT NULL CHECK (operation_ref GLOB 'op-[0-9a-f]*' AND length(operation_ref) = 35),"], "interpretation": {"claim": "carrier-format.v3 §5 lists operation_ref grammar op- plus 32 lowercase hex among laws preserved/re-executed", "ddlGlobOnlyChecksFirstCharacter": true}}`.

## Check receipts

- subject manifest and frozen source verification: `receipts/manifest-verification.json` (`3e14af37c2c6b306…`); result key: True.
- archive and every member verification plus disposable exact copies: `receipts/archive-verification.json` (`960d601ade099c75…`); result key: True.
- parent36 snapshot verification and full delta: `receipts/parent-delta.json` (`3986383d3707f978…`); result key: .
- six pinned reference groups (-I -B, verified copy): `receipts/reference/groups-report.json` (`535d64c4f53fc3f4…`); result key: True.
- current planning checks: `receipts/planning-checks.json` (`040060aeec046ffc…`); result key: .
- nonblind author package v14 verifier on a second verified exact copy: `receipts/package-verification/verification.json` (`0950071fa402ecf2…`); result key: True.
- independent probe run probe_semantic_boundaries: `receipts/probes/probe_semantic_boundaries.run.json` (`7a8395b64d8c0926…`); result key: 0.
- independent probe run probe_query_boundary: `receipts/probes/probe_query_boundary.run.json` (`3189b5916cfc4362…`); result key: 0.
- independent probe run probe_cause_attribution: `receipts/probes/probe_cause_attribution.run.json` (`f3fe9ab632213d3a…`); result key: 0.

Six groups ran (exit, seconds):

- evaluator3: 0, 262.2.
- foundation: 0, 126.2.
- integration: 0, 16.0.
- native: 0, 2.9.
- security: 0, 0.9.
- workflows: 0, 9.5.

The checkers changed no copy files.

**Planning checks**

- `check_implementation_planning`: `PASS: 320 source-bound mappings, 54 planned failure cases, private schema, owners and generated plan`.
- `check_repository_file_inventory`: `PASS: 198 unique paths, naming/ownership checks, acyclic package dependencies, chapter matches`.

## Assessments

- **wholeRunCauseOrderAndCoverageId.** CHANGES REQUIRED (S37-01). Native §10 now correctly delegates the Run termination to the host finalizer and D9 reducer, but no owner fixes the pre-reduction order or coverageId; a stage-implied primary can differ from the entry detail named by coverageId (probe B).
- **nativeDeficiencyToD9Routing.** ACCEPTABLE. The nine-row route equals the D9 map (five self-mapped members; the four bridge members go to verdict-indeterminate, i.e. VERDICT.INDETERMINATE). The source37 correction of LANGUAGE_TIER/CONFIDENCE_FLOOR/REQUIRED_RELATION to their COVERAGE.* codes agrees with D9 v1.14. The native group passes, including route drift.
- **strictPackageEndpointAdmission.** ACCEPTABLE. Schema-first QUERY.PARAMS_MALFORMED precedes Run presence, availability observation and vertex lookup; same-name packages with distinct manifests are distinct vertices; an unknown manifest is ENDPOINT_UNKNOWN; ENDPOINT_AMBIGUOUS is unreachable from one retained Run (P-QUERY Q1/Q2).
- **graphEvidenceAvailabilityMapping.** ACCEPTABLE with advisories A37-05/06. purged, expired, corrupt and unavailable route to HOST.IO_FAILURE exit 4 with evidence.purged/expired/corrupt/missing; retained, partial and omitted neither refuse nor grant; corrupt bytes still refuse under a retained or partial observation (Q3).
- **dependencySameKindTotality.** ASSESSED BY READING AND REFERENCE GROUP ONLY. The atom contract's evaluate-with-and-without-gap-positions law, required-relation-missing for removed positions, vacuous empty owed set and whole-source different-kind are coherent with composition §9. The atoms group passed. No independent probe.
- **partialEvidenceCitationsBooleanScopeUnion.** ACCEPTABLE. Boolean nodes union child scopeIds/inputRefs/deficiencies while witness coverageIds stay narrower. Finding evidenceRefs cite witness, facts, coverage and imports from descendants. P-TARGET-incomplete shows retained witness deficiencies with matching query disclosure.
- **importedHistoryRuntimeAndWireVersionTokens.** ASSESSED BY READING. Runtime/test/history do not become Coverage; negotiated FactBatchV3 token target-attribution-v2 and occupancy companion/dispatch binding are coherent. No independent probe.
- **repairPerRequirementDisclosures.** ACCEPTABLE BY READING. One requirement's outcome stays its DeficiencyV2 member and is not a per-requirement D9 code (native §10).
- **fullQueryResponseParity.** CHANGES REQUIRED (S37-03). The parity law (workflows §8) is otherwise coherent: graph context requires evidence, run-only resolvedView and advisory const false (Q4 negatives confirmed).
- **nativeSchemaAnnotationSupersession.** ACCEPTABLE (A37-08). Bytes are kept because payloadSchemaDigest identifies coverage2; §10 governs.
- **packageDependencyDirections.** ACCEPTABLE. The 20-package graph is acyclic: contracts <- identity <- evaluator/syntax pure layers; security depends on evaluator; storage on evaluator and security. apps/cli is Cargo package opensip-cli with binary opensip.
- **reportDispositions.** CHANGES REQUIRED (S37-02) for R02/R24 hook language; the other rows are coherent with offline host-projection ownership.
- **milestonesM0toM6.** CONSISTENT. Checker PASS on 320 mappings; moduleFirstMilestone and milestoneOrder are coherent; all verification standings not-executed.
- **phaseSensitiveRecovery.** CONSISTENT across identity §5, S12, read-only v3, attempt custody, store lineage phase markers and plan F52/F53; 54/54 cases not executed. Advisories A37-01..04.

## TCB-SCOPE-01 (one shared assumption, 13 dependent accounts)

**Dependent accounts:** RES-EP13-02, RES-EP13-04, RES-EP13-12, RES-EP13-13, RES-EP13-16, RES-EP13-18, IR-EP13-NB-01, IR-EP13-NB-03, IR-EP13-NB-04, AX6, AX9, MD5, RX2c.

**Assumption.** Selected authenticated in-process host/evaluator code is trusted; adversarial code sharing that process is outside this product threat model. Untrusted inputs are inert typed data and provider process boundaries still require real qualification.

- COHERENT AS A SCOPE SELECTION, NOT A CONTAINMENT CLAIM. It agrees with admission §5 items 3-5: only the host constructs findings, verdicts and rendering; no untrusted native/WASM admission; no sandbox claim; no imperative contributions. It also agrees with identity §4, where open_run_closure grants no correctness.
- What it relies on is visible and was probed. Fully reminted false-result graphs with valid new identities pass structural admission and are refused only by complete replay (P-REMINT). Outside the trusted process, correctness therefore rests on the replaying evaluator code and retained inputs, not on identity checks. If that code is adversarial, nothing in the design detects it, which is exactly what the assumption excludes.
- One planning text is inconsistent with it. S37-02 selects executable external report hooks in a worker lane, which would put non-host rendering code outside this account. Resolving S37-02 as recommended keeps the assumption intact.
- The assumption rests on an exact authenticated closure/TCB inventory and on provider process boundaries (DR-G29/G30 and related gates). All 32 gates remain unperformed, so it is design-coherent and unqualified.
- Consequence retained: rejecting or changing it reopens all thirteen dependent accounts together. It does not repair the historical attacks or establish containment. No grade is assigned, all thirteen author grades stay PENDING, and final application adjudication is still required and is not granted here.

**Standing.** ASSESSED-COHERENT-UNQUALIFIED; final application adjudication required; not granted

## Author package v14 (nonblind)

- On a verified exact copy of source37 (12900 source files, 329 package files verified), every verifier group passed. There are seven valid synthetic Runs (checkpoint3 1, normalized-examples6 4, rust-selection-examples1 2), each owner ADMIT and semantic ADMIT. The three reminted semantic negative controls (severity, unrelated-scope, collapsed-deficiencies) are owner ADMIT and complete-replay REFUSE with EVALUATOR_COMPLETE_PROOF_REPLAY. Of the three binding controls, two are lawful ADMIT and ts-invalid-default-entry is REFUSE with EVALUATOR_ENUMERATION_JOIN:ENUMERATION_BINDING_PROGRAM_ENTRY. There are seven query checks. The group exitCode 1 for semantic-controls1 and binding-controls is the expected refusal signal, with passed=true.
- semantic-controls1/construction-provenance.json: "AUTHOR-assisted construction. Not independent reconstruction, not blind acceptance, not product qualification". It was built against the source33 kit with package-v10 author helpers and transported by check-export.v4.py. This mixed construction provenance is preserved and is not upgraded by passing on source37.
- The A9/A10 limitations named by the charter are preserved as stated there. The literal tokens "A9"/"A10"/"A-9"/"A-10" do not appear in the current top-level v14 package files searched (historical subdirectories excluded), so their wording was not re-read here.
- This review's own discriminating mutants (P-REMINT, P-CAUSE, P-QUERY) were designed independently of the package controls and do not reuse its stores.

**Standing.** NONBLIND AUTHOR PACKAGE VERIFIED AS REFERENCE EVIDENCE; no blind reconstruction claimed; no grade or acceptance conferred

## Disposition rows (107)

Every row has `appliedByThisReview=false` and `finalApplicationOutcomeGranted=false`. Full text is in review.json.

### fDispositions (14)

| id | disposition | note |
|---|---|---|
| F-01 | CARRIED-NOT-REGRADED | -completion-assessment.v1. The F row content is defined in earlier review records outside this snapshot; this review did not re-derive it, and source36 standing is not inherited as source37 acceptance. No source37 delta file is among its owners in that record. |
| F-02 | CARRIED-NOT-REGRADED | -completion-assessment.v1. The F row content is defined in earlier review records outside this snapshot; this review did not re-derive it, and source36 standing is not inherited as source37 acceptance. No source37 delta file is among its owners in that record. |
| F-03 | CARRIED-NOT-REGRADED | -completion-assessment.v1. The F row content is defined in earlier review records outside this snapshot; this review did not re-derive it, and source36 standing is not inherited as source37 acceptance. No source37 delta file is among its owners in that record. |
| F-04 | CARRIED-NOT-REGRADED | -completion-assessment.v1. The F row content is defined in earlier review records outside this snapshot; this review did not re-derive it, and source36 standing is not inherited as source37 acceptance. No source37 delta file is among its owners in that record. |
| F-05 | CARRIED-NOT-REGRADED | -completion-assessment.v1. The F row content is defined in earlier review records outside this snapshot; this review did not re-derive it, and source36 standing is not inherited as source37 acceptance. No source37 delta file is among its owners in that record. |
| F-06 | CARRIED-NOT-REGRADED | -completion-assessment.v1. The F row content is defined in earlier review records outside this snapshot; this review did not re-derive it, and source36 standing is not inherited as source37 acceptance. No source37 delta file is among its owners in that record. |
| F-07 | CARRIED-NOT-REGRADED | -completion-assessment.v1. The F row content is defined in earlier review records outside this snapshot; this review did not re-derive it, and source36 standing is not inherited as source37 acceptance. No source37 delta file is among its owners in that record. |
| F-08 | CARRIED-NOT-REGRADED | -completion-assessment.v1. The F row content is defined in earlier review records outside this snapshot; this review did not re-derive it, and source36 standing is not inherited as source37 acceptance. No source37 delta file is among its owners in that record. |
| F-09 | CARRIED-NOT-REGRADED | -completion-assessment.v1. The F row content is defined in earlier review records outside this snapshot; this review did not re-derive it, and source36 standing is not inherited as source37 acceptance. No source37 delta file is among its owners in that record. |
| F-10 | CARRIED-NOT-REGRADED | -completion-assessment.v1. The F row content is defined in earlier review records outside this snapshot; this review did not re-derive it, and source36 standing is not inherited as source37 acceptance. No source37 delta file is among its owners in that record. |
| F-11 | CARRIED-NOT-REGRADED | -completion-assessment.v1. The F row content is defined in earlier review records outside this snapshot; this review did not re-derive it, and source36 standing is not inherited as source37 acceptance. No source37 delta file is among its owners in that record. |
| F-12 | CARRIED-NOT-REGRADED | -completion-assessment.v1. The F row content is defined in earlier review records outside this snapshot; this review did not re-derive it, and source36 standing is not inherited as source37 acceptance. No source37 delta file is among its owners in that record. |
| F-13 | CARRIED-NOT-REGRADED | -completion-assessment.v1. The F row content is defined in earlier review records outside this snapshot; this review did not re-derive it, and source36 standing is not inherited as source37 acceptance. No source37 delta file is among its owners in that record. |
| F-14 | CARRIED-NOT-REGRADED | -completion-assessment.v1. The F row content is defined in earlier review records outside this snapshot; this review did not re-derive it, and source36 standing is not inherited as source37 acceptance. No source37 delta file is among its owners in that record. |

### evaluationResidualDispositions (30)

| id | disposition | note |
|---|---|---|
| RES-EP13-01 | ASSESSED-CONSISTENT-GRADE-PENDING [author grade PENDING] | dary). The historical limitation or observation is preserved unchanged, and no historical guard is claimed repaired. Checked against evaluator3 execution-inputs and composition: Plan/derivation joins are recomputed in replay (evaluator_replay_model.v3.replay). |
| RES-EP13-02 | ASSESSED-CONSISTENT-GRADE-PENDING [author grade PENDING] [depends on TCB-SCOPE-01] | he proposed prospective replacement is consistent with the source37 contracts read (identity §4 complete replay at close_run; admission §5 boundary). The historical limitation or observation is preserved unchanged, and no historical guard is claimed repaired.  |
| RES-EP13-03 | ASSESSED-CONSISTENT-GRADE-PENDING [author grade PENDING] | he proposed prospective replacement is consistent with the source37 contracts read (identity §4 complete replay at close_run; admission §5 boundary). The historical limitation or observation is preserved unchanged, and no historical guard is claimed repaired.  |
| RES-EP13-04 | ASSESSED-CONSISTENT-GRADE-PENDING [author grade PENDING] [depends on TCB-SCOPE-01] | he proposed prospective replacement is consistent with the source37 contracts read (identity §4 complete replay at close_run; admission §5 boundary). The historical limitation or observation is preserved unchanged, and no historical guard is claimed repaired.  |
| RES-EP13-05 | ASSESSED-CONSISTENT-GRADE-PENDING [author grade PENDING] | he proposed prospective replacement is consistent with the source37 contracts read (identity §4 complete replay at close_run; admission §5 boundary). The historical limitation or observation is preserved unchanged, and no historical guard is claimed repaired.  |
| RES-EP13-06 | ASSESSED-CONSISTENT-GRADE-PENDING [author grade PENDING] | he proposed prospective replacement is consistent with the source37 contracts read (identity §4 complete replay at close_run; admission §5 boundary). The historical limitation or observation is preserved unchanged, and no historical guard is claimed repaired.  |
| RES-EP13-07 | ASSESSED-CONSISTENT-GRADE-PENDING [author grade PENDING] | ission §5 boundary). The historical limitation or observation is preserved unchanged, and no historical guard is claimed repaired. P-REMINT confirms the seal binds proof, evidence, verdict and Run: every reminted identity is new and complete replay refuses it. |
| RES-EP13-08 | ASSESSED-CONSISTENT-GRADE-PENDING [author grade PENDING] | he proposed prospective replacement is consistent with the source37 contracts read (identity §4 complete replay at close_run; admission §5 boundary). The historical limitation or observation is preserved unchanged, and no historical guard is claimed repaired.  |
| RES-EP13-09 | ASSESSED-CONSISTENT-GRADE-PENDING [author grade PENDING] | ission §5 boundary). The historical limitation or observation is preserved unchanged, and no historical guard is claimed repaired. Provenance and correctness stay separate: P-REMINT mutants have valid provenance-style identities and are refused only by replay. |
| RES-EP13-10 | ASSESSED-CONSISTENT-GRADE-PENDING [author grade PENDING] | on §5 boundary). The historical limitation or observation is preserved unchanged, and no historical guard is claimed repaired. Candidate self-counters are not admission: this review ran pinned groups and independent probes rather than relying on author counts. |
| RES-EP13-11 | ASSESSED-CONSISTENT-GRADE-PENDING [author grade PENDING] | he proposed prospective replacement is consistent with the source37 contracts read (identity §4 complete replay at close_run; admission §5 boundary). The historical limitation or observation is preserved unchanged, and no historical guard is claimed repaired.  |
| RES-EP13-12 | ASSESSED-CONSISTENT-GRADE-PENDING [author grade PENDING] [depends on TCB-SCOPE-01] | he proposed prospective replacement is consistent with the source37 contracts read (identity §4 complete replay at close_run; admission §5 boundary). The historical limitation or observation is preserved unchanged, and no historical guard is claimed repaired.  |
| RES-EP13-13 | ASSESSED-CONSISTENT-GRADE-PENDING [author grade PENDING] [depends on TCB-SCOPE-01] | ete replay at close_run; admission §5 boundary). The historical limitation or observation is preserved unchanged, and no historical guard is claimed repaired. This review's own probes deep-copy inputs before mutation (fixture isolation only; no sandbox claim). |
| RES-EP13-14 | ASSESSED-CONSISTENT-GRADE-PENDING [author grade PENDING] | he proposed prospective replacement is consistent with the source37 contracts read (identity §4 complete replay at close_run; admission §5 boundary). The historical limitation or observation is preserved unchanged, and no historical guard is claimed repaired.  |
| RES-EP13-15 | ASSESSED-CONSISTENT-GRADE-PENDING [author grade PENDING] | he proposed prospective replacement is consistent with the source37 contracts read (identity §4 complete replay at close_run; admission §5 boundary). The historical limitation or observation is preserved unchanged, and no historical guard is claimed repaired.  |
| RES-EP13-16 | ASSESSED-CONSISTENT-GRADE-PENDING [author grade PENDING] [depends on TCB-SCOPE-01] | he proposed prospective replacement is consistent with the source37 contracts read (identity §4 complete replay at close_run; admission §5 boundary). The historical limitation or observation is preserved unchanged, and no historical guard is claimed repaired.  |
| RES-EP13-17 | ASSESSED-CONSISTENT-GRADE-PENDING [author grade PENDING] | he proposed prospective replacement is consistent with the source37 contracts read (identity §4 complete replay at close_run; admission §5 boundary). The historical limitation or observation is preserved unchanged, and no historical guard is claimed repaired.  |
| RES-EP13-18 | ASSESSED-CONSISTENT-GRADE-PENDING [author grade PENDING] [depends on TCB-SCOPE-01] | he proposed prospective replacement is consistent with the source37 contracts read (identity §4 complete replay at close_run; admission §5 boundary). The historical limitation or observation is preserved unchanged, and no historical guard is claimed repaired.  |
| RES-EP13-19 | ASSESSED-CONSISTENT-GRADE-PENDING [author grade PENDING] | e_run; admission §5 boundary). The historical limitation or observation is preserved unchanged, and no historical guard is claimed repaired. Substantive semantic review was performed and found S37-01..03; pins and passing counts were not treated as acceptance. |
| IR-EP13-NB-01 | ASSESSED-CONSISTENT-GRADE-PENDING [author grade PENDING] [depends on TCB-SCOPE-01] | he proposed prospective replacement is consistent with the source37 contracts read (identity §4 complete replay at close_run; admission §5 boundary). The historical limitation or observation is preserved unchanged, and no historical guard is claimed repaired.  |
| IR-EP13-NB-02 | ASSESSED-CONSISTENT-GRADE-PENDING [author grade PENDING] | entity §4 complete replay at close_run; admission §5 boundary). The historical limitation or observation is preserved unchanged, and no historical guard is claimed repaired. No name or punctuation scan decides scope in the source37 query/evaluator owners read. |
| IR-EP13-NB-03 | ASSESSED-CONSISTENT-GRADE-PENDING [author grade PENDING] [depends on TCB-SCOPE-01] | he proposed prospective replacement is consistent with the source37 contracts read (identity §4 complete replay at close_run; admission §5 boundary). The historical limitation or observation is preserved unchanged, and no historical guard is claimed repaired.  |
| IR-EP13-NB-04 | ASSESSED-CONSISTENT-GRADE-PENDING [author grade PENDING] [depends on TCB-SCOPE-01] | he proposed prospective replacement is consistent with the source37 contracts read (identity §4 complete replay at close_run; admission §5 boundary). The historical limitation or observation is preserved unchanged, and no historical guard is claimed repaired.  |
| IR-EP13-NB-05 | ASSESSED-CONSISTENT-GRADE-PENDING [author grade PENDING] | y at close_run; admission §5 boundary). The historical limitation or observation is preserved unchanged, and no historical guard is claimed repaired. Contradictory prose still needs substantive review; S37-02 is an example found by reading, not by any checker. |
| IR-EP13-NB-06 | ASSESSED-CONSISTENT-GRADE-PENDING [author grade PENDING] | he proposed prospective replacement is consistent with the source37 contracts read (identity §4 complete replay at close_run; admission §5 boundary). The historical limitation or observation is preserved unchanged, and no historical guard is claimed repaired.  |
| IR-EP13-NB-07 | ASSESSED-CONSISTENT-GRADE-PENDING [author grade PENDING] | he proposed prospective replacement is consistent with the source37 contracts read (identity §4 complete replay at close_run; admission §5 boundary). The historical limitation or observation is preserved unchanged, and no historical guard is claimed repaired.  |
| AX6 | ASSESSED-CONSISTENT-GRADE-PENDING [author grade PENDING] [depends on TCB-SCOPE-01] | he proposed prospective replacement is consistent with the source37 contracts read (identity §4 complete replay at close_run; admission §5 boundary). The historical limitation or observation is preserved unchanged, and no historical guard is claimed repaired.  |
| AX9 | ASSESSED-CONSISTENT-GRADE-PENDING [author grade PENDING] [depends on TCB-SCOPE-01] | he proposed prospective replacement is consistent with the source37 contracts read (identity §4 complete replay at close_run; admission §5 boundary). The historical limitation or observation is preserved unchanged, and no historical guard is claimed repaired.  |
| MD5 | ASSESSED-CONSISTENT-GRADE-PENDING [author grade PENDING] [depends on TCB-SCOPE-01] | he proposed prospective replacement is consistent with the source37 contracts read (identity §4 complete replay at close_run; admission §5 boundary). The historical limitation or observation is preserved unchanged, and no historical guard is claimed repaired.  |
| RX2c | ASSESSED-CONSISTENT-GRADE-PENDING [author grade PENDING] [depends on TCB-SCOPE-01] | he proposed prospective replacement is consistent with the source37 contracts read (identity §4 complete replay at close_run; admission §5 boundary). The historical limitation or observation is preserved unchanged, and no historical guard is claimed repaired.  |

### arDispositions (16)

| id | disposition | note |
|---|---|---|
| AR-01 | NO-NEW-ISSUE | Numeric/schema admission read completely; probes observed exact schema admission on query requests and StepTermination. |
| AR-02 | NO-NEW-ISSUE | Custody, semantic correctness and qualification remain separate; all 32 gates are DESIGN-CONTRACT-PENDING-REVIEW with qualified=false. |
| AR-03 | NO-NEW-ISSUE | Discovery joins verified by the security reference group only. |
| AR-04 | NO-NEW-ISSUE | Trust time read; no probe. |
| AR-05 | NO-NEW-ISSUE | Root chain/revocation read; no probe. |
| AR-06 | NO-NEW-ISSUE | Platform vocabulary joins pass in the security group; the carrier DDL platform enum matches the four machine ids. |
| AR-07 | NO-NEW-ISSUE | Native §§3/5/9 read; native group 377/377. |
| AR-08 | NO-NEW-ISSUE | Invocation and repair read; per-requirement repair disclosure stays a DeficiencyV2 member (native §10, lines 2965 onward). |
| AR-09 | ADVISORY-ONLY | The close_run complete-replay boundary is confirmed by P-REMINT; see A37-06 for the query route of replay disagreement. |
| AR-10 | NO-NEW-ISSUE | Baseline/comparison read; comparison-knowledge group passed. |
| AR-11 | NO-NEW-ISSUE | Imported evidence wrapper and history/runtime limits read; no independent import probe. |
| AR-12 | NO-NEW-ISSUE | Native §4 sufficiency read; dependency same-kind totality assessed by reading and the atoms group. |
| AR-13 | CHANGES-REQUIRED-ROUTED | Workflow output parity: S37-03. |
| AR-14 | ADVISORY-ONLY | Stage transition and lease model consistent with store lineage; A37-03 on MIGRATION.CORRUPT use. |
| AR-15 | CHANGES-REQUIRED-ROUTED | The index/D-372 application is coherent; the planning layer contradicts the admission boundary on report hooks (S37-02). |
| AR-16 | CHANGES-REQUIRED-ROUTED | The D9 native route is corrected and total, but the whole-Run reduction order and coverageId are unowned: S37-01. |

### fwDispositions (15)

| id | disposition | note |
|---|---|---|
| FW-01 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | The source row and owner module match the current-source-map row and the chapter 14 inventory; implementation not executed.  |
| FW-02 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | The source row and owner module match the current-source-map row and the chapter 14 inventory; implementation not executed.  |
| FW-03 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | The source row and owner module match the current-source-map row and the chapter 14 inventory; implementation not executed.  |
| FW-04 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | The source row and owner module match the current-source-map row and the chapter 14 inventory; implementation not executed. Runtime/test/history stay non-Coverage per workflows §4 (read); no probe. |
| FW-05 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | The source row and owner module match the current-source-map row and the chapter 14 inventory; implementation not executed.  |
| FW-06 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | The source row and owner module match the current-source-map row and the chapter 14 inventory; implementation not executed. S37-01: the typed termination projection is not yet a deterministic function of the sealed Run. |
| FW-07 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | The source row and owner module match the current-source-map row and the chapter 14 inventory; implementation not executed.  |
| FW-08 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | The source row and owner module match the current-source-map row and the chapter 14 inventory; implementation not executed. A37-05 and A37-06 on the query unavailable/operational-fault distinction. |
| FW-09 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | The source row and owner module match the current-source-map row and the chapter 14 inventory; implementation not executed.  |
| FW-10 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | The source row and owner module match the current-source-map row and the chapter 14 inventory; implementation not executed.  |
| FW-11 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | The source row and owner module match the current-source-map row and the chapter 14 inventory; implementation not executed.  |
| FW-12 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | The source row and owner module match the current-source-map row and the chapter 14 inventory; implementation not executed.  |
| FW-13 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | The source row and owner module match the current-source-map row and the chapter 14 inventory; implementation not executed. S37-03: typed registry/schema admission gap for the advisory cross-join. |
| FW-14 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | The source row and owner module match the current-source-map row and the chapter 14 inventory; implementation not executed.  |
| FW-15 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | The source row and owner module match the current-source-map row and the chapter 14 inventory; implementation not executed.  |

### inheritedResidualDispositions (27)

| id | disposition | note |
|---|---|---|
| DR-001 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | The proposed successor routing in inherited-residuals.proposed.md is consistent with the source37 contracts read; the original custody and standing are preserved.  |
| DR-002 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | The proposed successor routing in inherited-residuals.proposed.md is consistent with the source37 contracts read; the original custody and standing are preserved.  |
| DR-003 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | ng in inherited-residuals.proposed.md is consistent with the source37 contracts read; the original custody and standing are preserved. G19 and native carrier custody remain release obligations; the 54 recovery cases are not executed; A37-01, A37-02 and A37-04. |
| DR-004 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | The proposed successor routing in inherited-residuals.proposed.md is consistent with the source37 contracts read; the original custody and standing are preserved.  |
| DR-005 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | The proposed successor routing in inherited-residuals.proposed.md is consistent with the source37 contracts read; the original custody and standing are preserved. Executable custody reference groups pass; native product carrier qualification is still required. |
| DR-006 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | The proposed successor routing in inherited-residuals.proposed.md is consistent with the source37 contracts read; the original custody and standing are preserved.  |
| DR-007 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | The proposed successor routing in inherited-residuals.proposed.md is consistent with the source37 contracts read; the original custody and standing are preserved. S37-01: the cause reduction order and coverageId join are not closed. |
| DR-008 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | The proposed successor routing in inherited-residuals.proposed.md is consistent with the source37 contracts read; the original custody and standing are preserved.  |
| DR-009 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | The proposed successor routing in inherited-residuals.proposed.md is consistent with the source37 contracts read; the original custody and standing are preserved.  |
| DR-010 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | The proposed successor routing in inherited-residuals.proposed.md is consistent with the source37 contracts read; the original custody and standing are preserved. S37-02: report hooks conflict with bounded first-party scope. |
| DR-011 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | cessor routing in inherited-residuals.proposed.md is consistent with the source37 contracts read; the original custody and standing are preserved. Individual dispositions exist; the blind implementer litmus follows final integration and was not performed here. |
| DR-011-R01 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | The proposed successor routing in inherited-residuals.proposed.md is consistent with the source37 contracts read; the original custody and standing are preserved.  |
| DR-011-R02 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | The proposed successor routing in inherited-residuals.proposed.md is consistent with the source37 contracts read; the original custody and standing are preserved.  |
| DR-011-R03 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | The proposed successor routing in inherited-residuals.proposed.md is consistent with the source37 contracts read; the original custody and standing are preserved.  |
| DR-011-R04 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | The proposed successor routing in inherited-residuals.proposed.md is consistent with the source37 contracts read; the original custody and standing are preserved.  |
| DR-011-R05 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | The proposed successor routing in inherited-residuals.proposed.md is consistent with the source37 contracts read; the original custody and standing are preserved.  |
| DR-011-R06 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | The proposed successor routing in inherited-residuals.proposed.md is consistent with the source37 contracts read; the original custody and standing are preserved.  |
| DR-011-R07 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | The proposed successor routing in inherited-residuals.proposed.md is consistent with the source37 contracts read; the original custody and standing are preserved.  |
| DR-011-R08 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | The proposed successor routing in inherited-residuals.proposed.md is consistent with the source37 contracts read; the original custody and standing are preserved. S37-01 affects the closed host-owned outcome for concurrent deficiencies. |
| DR-011-R09 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | The proposed successor routing in inherited-residuals.proposed.md is consistent with the source37 contracts read; the original custody and standing are preserved.  |
| DR-011-R10 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | The proposed successor routing in inherited-residuals.proposed.md is consistent with the source37 contracts read; the original custody and standing are preserved. Remains OPEN: this nonblind review cannot close the fresh blind implementer litmus. |
| DR-011-R11 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | The proposed successor routing in inherited-residuals.proposed.md is consistent with the source37 contracts read; the original custody and standing are preserved. Real platform durability is still unmeasured; carrier advisories A37-01..04. |
| DR-011-R12 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | The proposed successor routing in inherited-residuals.proposed.md is consistent with the source37 contracts read; the original custody and standing are preserved. Depends on TCB-SCOPE-01 (assessed once below). |
| DR-011-R13 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | The proposed successor routing in inherited-residuals.proposed.md is consistent with the source37 contracts read; the original custody and standing are preserved.  |
| DR-011-R14 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | The proposed successor routing in inherited-residuals.proposed.md is consistent with the source37 contracts read; the original custody and standing are preserved.  |
| DR-011-R15 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | The proposed successor routing in inherited-residuals.proposed.md is consistent with the source37 contracts read; the original custody and standing are preserved.  |
| DR-011-R16 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | The proposed successor routing in inherited-residuals.proposed.md is consistent with the source37 contracts read; the original custody and standing are preserved. S37-02. |

### scopedReviewOwnerDispositions (5)

| id | disposition | note |
|---|---|---|
| DR-201 | ROUTING-ASSESSED-ONLY-NOT-APPLIED | ister 08 records ACCEPTED 2026-08-13 for the earlier scope (line 326) and OPEN for full-product integration (line 412). DR-201..205 remain the condition-3 owners (line 391). This review is an input to that integrated review and is not applied. Related: S37-01. |
| DR-202 | ROUTING-ASSESSED-ONLY-NOT-APPLIED | r 08 records ACCEPTED 2026-08-13 for the earlier scope (line 327) and OPEN for full-product integration (line 412). DR-201..205 remain the condition-3 owners (line 391). This review is an input to that integrated review and is not applied. Related: A37-01..04. |
| DR-203 | ROUTING-ASSESSED-ONLY-NOT-APPLIED | Register 08 records ACCEPTED 2026-08-13 for the earlier scope (line 328) and OPEN for full-product integration (line 412). DR-201..205 remain the condition-3 owners (line 391). This review is an input to that integrated review and is not applied. |
| DR-204 | ROUTING-ASSESSED-ONLY-NOT-APPLIED | Register 08 records ACCEPTED 2026-08-13 for the earlier scope (line 329) and OPEN for full-product integration (line 412). DR-201..205 remain the condition-3 owners (line 391). This review is an input to that integrated review and is not applied. |
| DR-205 | ROUTING-ASSESSED-ONLY-NOT-APPLIED | ister 08 records ACCEPTED 2026-08-13 for the earlier scope (line 330) and OPEN for full-product integration (line 412). DR-201..205 remain the condition-3 owners (line 391). This review is an input to that integrated review and is not applied. Related: S37-02. |

## Retained

- 30 evaluation residuals (all author grades PENDING).
- 28 condition-2 obligations (docs/v2/architecture/08-decision-and-readiness-register.md:385-391 (DR-101-107, DR-109-115, DR-117-127, DR-130/131/133)).
- 32 qualification gates unperformed.
- 54 recovery cases not executed.

## Contracts read completely (41)

| path | sha256 | lines |
|---|---|---|
| docs/v2/contracts/product-v1/README.md | `c53633c2c8e056de5c2469995d9e9a8b5f0698f4c16bdf506803577ba7e703e6` | 60 |
| docs/v2/contracts/product-v1/identity-and-evidence.md | `39b06021d2233825d28dd646340fb907f15499da6315e57247bebfd1d3dea6a5` | 1735 |
| docs/v2/contracts/product-v1/security-and-lifecycle.md | `42bafae698cf624f70b1789fb1395c92afd7a2b0b0c7b36d93d23070db01ead1` | 1519 |
| docs/v2/contracts/product-v1/native-evidence.md | `ffa5b5691bfe932f9749c4082d1232dd87f820b9fc918b68f6009390f567bc33` | 3792 |
| docs/v2/contracts/product-v1/workflows-and-surfaces.md | `b2530a314a7653eb45aa2f99aedc3dba5a389db2ca15d4deada029ce801615d0` | 1453 |
| docs/v2/contracts/product-v1/admission-and-qualification.md | `69cd6ba3cb41ed191e0a4e5cc20b191f4b8761625843b585426157873dbee6b3` | 349 |
| docs/coop/design-corrections/foundation/enumeration-contract.v1.md | `ae4523a224bf6e21371c5575381f661e5feda634488b692513117c236d6ee689` | 163 |
| docs/coop/design-corrections/foundation/atom-evaluation-contract.v1.md | `8649b8b079ccbd8f3a7646018343b3bff82ef6707de8feacccb2a7dda5f65899` | 451 |
| docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md | `4889ab4baef50fa7aa12334f627cb20300e5eedd83d8fbf111e0bc215e69d569` | 289 |
| docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md | `1640740f71ab501818cf8498153354228f6fb84e920a03f7c5c96f1b3ced4bda` | 330 |
| docs/coop/design-corrections/foundation/evaluator-fault-contract.v3.md | `5731b41d191d36f0b7c64ddbf46bcf0a66e93c302b8cfca854ec4dd0f4b311ab` | 98 |
| docs/coop/design-corrections/foundation/target-attribution.schema.v2.json | `bd938f11c584be65e914bc1446193fdf3dd4a15f7b78630cc3eb628c5bca1d53` | 491 |
| docs/coop/design-corrections/foundation/provider-target-attribution-return.schema.v2.json | `2d5719b57dc65095278287d173280f789f684737af30a45fc7114e020efa523f` | 252 |
| docs/coop/design-corrections/workflows/workflow-projection-contract.v3.md | `e890bcdaad86996ad5e2950cf47ad88a70c207cbd7ead69ea065df4ae76cb19a` | 223 |
| docs/coop/design-corrections/workflows/query-projection-contract.v3.md | `04a5e31179317ff6ffa32dbb0fa92ab0545b1afd6a9fd839774af1c7dd1f680a` | 191 |
| docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json | `ca1e2baed58df6dd3a25ec3c0c62961d9debd533cc3636de1a30541c806d3093` | 1194 |
| docs/coop/design-corrections/native/fact-batch.schema.v3.json | `a963abd38fb2cf8a7b3b78a36469a7d166a4e315cd5f9c63cdbbff55c04c0de2` | 124 |
| docs/coop/design-corrections/native/occupancy-companion.schema.v1.json | `983864b16ec8ea9c196b57e4bb2cbdb9d38066c0cb13f599b97b4a78d5c6861b` | 332 |
| docs/coop/design-corrections/native/dispatch-binding.schema.v1.json | `868c3cf241af9ecc205ba7d078354e38a7db5132974120c046ac23a2dd1df938` | 89 |
| docs/coop/design-corrections/hydradb-dispositions.proposed.md | `9a15484c69509257f69dce6b5bf5d011d378492a439183aad499e03be338922c` | 39 |
| docs/coop/design-corrections/inherited-residuals.proposed.md | `4b2b992b06abd9cdc955ea1defd40f1019591f97898d3c2f21e44ca1d9e062d5` | 46 |
| docs/coop/design-corrections/current-source-map.proposed.md | `5229359680be8e36c6ea236a95206427179d0225cf09df9fa7c18e465a52206a` | 86 |
| docs/v2/architecture/14-repository-and-module-layout.md | `6fa513a8a140bfce44402c1b575850295516cdb2f3788cfbeeceb1d08d1abb09` | 731 |
| docs/v2/architecture/implementation-boundaries-and-build-plan.md | `666461f0c53dd8718b0914d139ad3bce2040824025dd74e61d2c3ce4f3bd0ff8` | 1127 |
| docs/v2/architecture/commit-recovery-plan.v1.json | `cbaac9b1651fe02e80dd314433805972df84c3c500f11811cef4ed60b90ecbb5` | 681 |
| docs/v2/architecture/commit-recovery-readonly.v3.md | `a60b048c82db55e69c5939d96905605fb53fda8d0c043835ca225b9489c71153` | 439 |
| docs/v2/architecture/store-instance-lineage.v1.json | `2ff48b40760ac5accd093120bca4533421e07145078501f83a1204a4d1f67c83` | 626 |
| docs/v2/architecture/report-asset-binding.v1.json | `71363c0637d4405d9394782f805f33c294588834990614388a26a2dbd98027a6` | 385 |
| docs/v2/architecture/attempt-custody.schema.v1.json | `37f1445c573a31be3ef4bc06360bf19e89d04bf7110a4822e70de0970d160990` | 171 |
| docs/v2/architecture/prototype-report-inventory.md | `3c9901d1071dae5a115df2eea7f331709810fca62a05841ece9305eeefff7f87` | 236 |
| docs/v2/architecture/implementation-normative-inputs.v5.json | `4b4b35b78192833027a26f0936c31c8b4523e228c03ccac7e1fc20d8ab0d091a` | 150 |
| docs/v2/architecture/implementation-planning-sources.v1.json | `b66a060bf260dae7b9d9ceeb10e7c3960236c5645b377043e491a42c371437e3` | 1065 |
| docs/v2/architecture/repository-file-inventory.v1.json | `970640a36f35f45721a4a6b495e27fad2466487b80d403fdd2706b5821f9f7b8` | 1815 |
| docs/v2/architecture/implementation-coverage.v1.json | `a818b71453ecf6c05f0ec8693036b99cd5d3672ba0af52d32dfacd707eaecd8f` | 8929 |
| docs/coop/design-corrections/security/carrier-format.v3.md | `04e6271d5700f976732607e4521fdb4cf1b53ec2f599da0408e087b5b1064a99` | 536 |
| docs/coop/design-corrections/security/carrier-migration.v1.md | `0295d5e03d2017fa165d3b258503436f04fb042a9b5bce7b687cd6016d1a26b2` | 247 |
| docs/coop/design-corrections/security/grant-journal.carrier.v3.sql | `23902324163196cfb8203a2a016072fd16a3b7a53c82e518e26c0c4fff0e863b` | 115 |
| docs/coop/design-corrections/security/carrier-highwater.schema.v1.json | `1bbfd9135bd9492ef5b1df328aacdb959b0440a9e21312763f88609f4b966f82` | 63 |
| docs/coop/design-corrections/security/carrier-dispatch.v3.json | `0603be7f2316dda23138b430e2b8d9d8555fa4c1208ddc217770133c5d13593f` | 458 |
| docs/operations/check_implementation_planning.py | `dc7ac14ab75b0013494dea9c81b24855be8cf352d4a054ba342f323aa84c3848` | 291 |
| docs/operations/check_repository_file_inventory.py | `ea2e171e03fb7b64a830eadbd6ec31fd93ff1f939eaa67b97c85ba5d2feb803e` | 156 |

### Partially read

- docs/coop/artifacts/d9-exit-contract.v1.14.json: lines 840-939, 2565-2764, plus causeModel, concurrentConditionReducer and codeMaps/deficiencyToReasonCode extracted in full
- docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json: $defs/StepTermination (lines 742-971)
- docs/coop/design-corrections/native/native_evidence_model.v2.py: lines 3625-3764 (native_deficiency_d9, stage_authority, run_termination), PRECEDENCE_V2, STAGE_TERMINAL_DEFICIENCY
- docs/coop/design-corrections/workflows/query_projection_model.v3.py: lines 1-669 and 1186-1565
- docs/coop/design-corrections/foundation/identity-model.v3.py: lines 600-779 (close_run, open_run_closure)
- docs/coop/design-corrections/foundation/evaluator_replay_model.v3.py: complete (96 lines)
- docs/coop/design-corrections/foundation/evaluator_composition_model.v3.py: lines 60-209 (compose, compare_complete_replay)
- docs/coop/design-corrections/foundation/atom_model.v1.py: lines 560-629 (occupancy reconciliation and conflicts)
- docs/coop/design-corrections/foundation/check-semantic-replay.v3.py: lines 1-479
- docs/coop/design-corrections/workflows/check-query-projection.v3.py: lines 100-189, 236-287, 418-597
- docs/coop/design-corrections/workflows/workflows_model.v1.py: lines 190-234 (analysis_termination)
- docs/coop/design-corrections/foundation/identity-schemas.v3.json: x-opensip-evaluator-deficiency-registry extracted
- docs/coop/design-corrections/security/security_lifecycle_model_v1.py: admit_analysis_seal (lines 1527-1552)
- docs/v2/architecture/08-decision-and-readiness-register.md: lines 40-41, 326-330, 380-421, 495, 530
- docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json: all 30 items, key fields
- docs/coop/design-corrections/correction-crosswalk.proposed.json: all 16 AR items, key fields
- docs/coop/design-corrections/qualification-gates.proposed.json: all 32 gate ids, standing and qualified fields

## Limitations

- Nonblind review: the reviewer read the author package, its verifier and prior root receipts. No blind reconstruction is claimed, and no blind consumer artifact, root blind diagnosis or replay oracle was read.
- Source36 acceptance is not treated as covering source37. The parent36 delta (1 added, 15 changed) was verified, and the whole design was re-read under this charter.
- Reference models are Python design references over synthetic native-admitted inputs. No product code exists. Nothing here qualifies a compiler, provider, host, OS durability or platform; all 32 qualification gates remain unperformed (qualified=false), and the 54 recovery cases are not executed.
- Partially read files are listed under partiallyRead. Many checker scripts were executed rather than read.
- P-CAUSE part C applies the D9 reducer algorithm text to constructed condition lists because no product host finalizer exists. Parts A and B use actual owners and an actual closed Run.
- The SEAL adapter (admit_analysis_seal) was not executed; its delegation to close_run is from source reading.
- Dependency same-kind totality, imported history/runtime evidence, wire version tokens and repair disclosures were assessed by reading plus reference groups, without independent probes.
- F-01..F-14 content lives in earlier review records outside the snapshot and was not re-derived. Issue novelty is judged against the snapshot documents; an item may duplicate a finding in earlier review rounds this reviewer did not read.
- No grade, activation, application or implementation authorization is granted. The 30 residuals and 28 condition-2 obligations are retained unchanged.
