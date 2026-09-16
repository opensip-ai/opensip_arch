# consumer24 workflow author v2: R1, R2, query-step mapping, /tmp read replacement

Coauthor origin f5617310-c7c7-4d85-acdd-31370f220944.

This is an architecture, design and reference correction only. It is not a product implementation, not a commit, and not an acceptance or readiness claim. Pins were not updated.

## Custody

- **Runtime.** `/private/tmp/opensip-design-corrections/claude-consumer24-workflow-author.v2`.
- **Work tree.** `work/source38-work` is a regular copy of v1 `work/source38-work`: 12904 files, each copy re-hashed, with a distinct inode and nlink 1 (`receipts/v1-custody-and-copy.json`).
  - v1, LIVE, frozen38 and every other author tree were read only.
- **Final custody** (`receipts/final-custody-and-diff.json`, sha c8d38d14…, `ok: true`):
  - source38 manifest `2ddfa0db…7e5c5` verified;
  - parent tree re-hashed read-only with 0 mismatches and 0 extras;
  - v1 final receipt still `27e3c03a…`, and the v1 tree has 0 mismatches and 0 extras;
  - v2 tree has 12904 paths, with 0 missing, 0 new files and 0 pycache;
  - every v1→v2 changed path is covered by the edit receipts (`receipts/edits/text-edits.jsonl`, 23 rows): 0 unexpected changes, 0 broken hash chains.
- **Diffs.**

  | Diff | Files | Lines | sha256 |
  |---|---|---|---|
  | `diffs/source38-to-v2.diff` | 22 | 4307 | f5fdab1d758f187ed00622c9b3dba141afbe5bbeb33aa539bacd7c1b5a271600 |
  | `diffs/v1-to-v2.diff` | 15 | 2616 | be055eb71388fc5a71a17f4546b0ebe368ca9c802a16f8c451034197e1341fb9 |

  The hashmaps (source38, v1 and v2 sha per path) are in the final custody receipt.
- **Files changed v1→v2** (v1 sha → v2 sha):
  - `public-detail-registry.v1.json` c4627126→2702e6ca
  - `workflows/check-query-projection.v3.py` 26dac0f9→8e2c2b6b
  - `workflows/check-workflow-projection.v3.py` f357ad17→963b6f36
  - `workflows/command-inventory.v3.json` d456c8d9→5321996c
  - `workflows/query-projection-contract.v3.md` 34b744f1→923ff32f
  - `workflows/query_surface_projection.v3.py` 188d51c3→26106f4e
  - `workflows/schemas/common.schema.json` 7767a195→b7b25d5e
  - `schemas/evaluator3/command-envelope.schema.json` c2205d67→e224b3b5
  - `schemas/evaluator3/command-inventory.schema.json` 42d065d3→34e4b2c0
  - `schemas/evaluator3/common.schema.json` 5e6e0490→ce45b9ff
  - `schemas/evaluator3/comparison-result.schema.json` 0d5c8a96→f82a3070
  - `schemas/evaluator3/invocation-record.schema.json` 56fa2ee9→8c714107 (unchanged in v1, so this is the only newly changed file versus source38)
  - `workflows/workflow-projection-contract.v3.md` 6fe7bf03→cda2d3e3
  - `workflows/workflow_projection_model.v3.py` bca6e1e6→6dea10d0
  - `docs/v2/contracts/product-v1/workflows-and-surfaces.md` 71078934→261e25c4
- **Carried unchanged from v1:**
  - check-composition.v3.py
  - check-replay.v3.py
  - evaluator-composition-contract.v3.md
  - baseline-artifact.schema.json
  - test-execution.schema.json
  - native-evidence.md
  - security-and-lifecycle.md
- **Unaffected:** no new files, no new child commands and no new normative or reference files. Every change is in an existing file.

## R1: absence requires correspondence knowledge (resolved)

**Law** (workflows-and-surfaces §3, workflow-projection-contract §12, comparison-result PivotPresence description, `workflow_projection_model.v3.py`):
- An unmatched occurrence blocks proven absence of a fingerprint (a *correspondence barrier*) unless one of these holds:
  1. its rule differs;
  2. both paths are known and differ;
  3. both subject identities are known and differ (retained kind, language and qualifiedName versus the fingerprint's descriptor subjectKey).
- Where no stronger relation is provable, the barrier is same-rule/same-path. Baseline `unmatchedOccurrences` rows (ruleId and subjectPath only) are always same-rule/same-path barriers.
- The law is symmetric over B and E0–E4 (`current_absence_knowledge`, `baseline_presence_knowledge`, and the pivot loop plus E4 in `compare_admitted_v3`).
- Known hits stay `true`, and policy/scope non-selection `false` is unchanged.
- An unrelated unknown never erases a separately proven hit or CODE-NET-NEW, and an unmatched occurrence never mints a fingerprint.
- Baseline `absenceKnowledge` is preserved: anything not `complete-hit-set` stays null, and there is no unknown→false coercion because `entries[]` is empty.

**Indeterminate reason selection.** It is closed and published in §3, and uses only existing vocabulary, so no new value is added. The order is:
1. `pivot-reevaluation-unavailable`
2. evidence reasons (in evidenceUse order)
3. the detector disposition's reason
4. `baseline-absence-unknown`
5. `current-absence-unknown`

**Example replaced (root decision).**
- The projection §12 example and its check `pivot-only-fp-is-code-net-new-with-subsequent-policy` are replaced by `pivot-only-fp-over-unmatched-baseline-is-baseline-absence-unknown`.
- The pivot-only fingerprint stays in the universe, and the baseline unmatched gating obligation stays (the deficiency is present and the verdict is not pass).
- New genuine complete empty-baseline example `base_empty_x`: `complete-empty-baseline-proves-absence-of-x` and `complete-empty-baseline-pivot-only-fp-is-code-net-new-policy-hidden`.

**Controls.** All go through the actual close_run/compare_admitted path in check-workflow-projection:
- `r1-{gating,nongating}-*`: the collision is INDETERMINATE `current-absence-unknown`, the known hit is UNCHANGED, and the unmatched occurrence is never minted;
- `r1-gating-unrelated-unknown-does-not-erase-separate-code-net-new`;
- law checks: same path; README.md unrelated path; different identity; same identity; other rule;
- pivot collision gives `pivot-reevaluation-unavailable`, and the known hit is POLICY-DELTA;
- baseline barrier over `art_un`: same path gives null, other path gives false.

**Receipts.** r1-1 (610 pass at that point) and final-1.

## R2: public carriers and parity for all nine query-class commands (resolved)

**Carrier.** CommandEnvelope major 3 `querySurface` is closed to nine values, one per query-class command:
- `graph-query-response` carries `queryResponse`, the owner-admitted GraphQueryResponseV1. This is unchanged, and the graph joins stay valid.
- The other eight carry `queryRecord`, a closed oneOf of eight typed records that reuse owner schemas:

| Command | querySurface | Record (owner members) |
|---|---|---|
| recommend | discovery-recommendation | DiscoveryRecommendationRecordV1: native UnitDiscoveryV2 (refused must be null), recommendations (0 rows in this profile), config2Proposals (≤1, `discovery.workspaceRoots`) |
| baseline-show | baseline-inspection | BaselineInspectionRecordV1: baseline:2 artifact, pivotClosureAvailability (missing / revoked / incompatible / available + trustOrigin) |
| policy-show | effective-policy | EffectivePolicyRecordV1: policyDigest, PolicyDocumentV2, waiverSetDigest, WaiverSetV1, WaiverResolutionV1 |
| policy-test | policy-test-result | PolicyTestResultRecordV1: PolicyTestResultV1 |
| candidates | candidate-list | CandidateListRecordV1: GraphQueryResponseContext, includeSuppressed, review:2 Candidate[], evidenceLevels, suppressedCount |
| inspect | candidate-inspection | CandidateInspectionRecordV1: context, review:2 InspectionBundle |
| review-brief | review-brief | ReviewBriefRecordV1: context, review:2 ReviewBrief |
| repair-preview | repair-preview | RepairPreviewRecordV1: invocation:3 RepairPreviewResult, repair:2 RepairPlanV1 |

**Rules on the carrier.**
- `command-owned-summary` is removed.
- A non-query envelope kind forbids all three members.
- No blob or open additionalProperties member exists.
- JSON rendering is the envelope, agent is the envelope plus `agentHints`, and human prints the labelled parity. There is no private wrapper.

**Parity.** `command-inventory.v3.json` `queryDispatch.parityPaths` publishes a JSON pointer for every existing parity field, so parityFields is not reduced. The inventory schema requires `queryDispatch` for requestClass query and forbids it otherwise. The pointers and failure behaviour are tabulated in workflows-and-surfaces §8.

**Order of admission.** Closed record admission and every surface join run before rendering; see `project_command_surface` and `render_command_formats`. The joins are:
- recommend: config2 roots equal the discovered unit roots.
- baseline-show: verify_baseline_artifact_v3, plus pivot rows equal descriptor order.
- policy-show: policy and waiver digests, resolution.
- policy-test: the policytest2 id is recomputed, summary counts match.
- candidates: project, advisory, concrete Run, evidence levels, suppressed count, totalItems.
- inspect: bundle Run, fact order, totalItems.
- review-brief: brief Run, truncation.
- repair-preview: the repairplan2 id is recomputed, the preview equals the descriptor, project.
- all eight: the compact QueryResult join.

A carrier that cannot be delivered is `DELIVERY.REQUIRED_FAILED` / `DELIVERY.REQUIRED_PROJECTION_FAILED` with no runId.

**Owner projections added** (`workflow_projection_model.v3.py`):
- `non_graph_query_context`
- `project_candidate_list`
- `project_inspection_bundle`: facts, coverage and imports are the candidate findings' evidenceRefs, unique and byte-ordered; limitations cover unmatched reasons, incomplete enumeration and truncation; an unknown id refuses `IDENTITY.UNKNOWN` / `REVIEW.CANDIDATE_UNKNOWN`
- `pivot_closure_availability`

**Controls.** check-workflow-projection has 156 `r2-*` checks, all passing. Each non-graph command has positive envelopes built from actual owner records:

| Command | Source |
|---|---|
| candidates | close_run-admitted Run with a real suppressing disposition (listed and hidden) |
| inspect | project_inspection_bundle, plus an unknown-candidate refusal |
| review-brief | W.review_brief, full and truncated |
| policy-show | WF3.resolve_policy + W.resolve_waivers with active and expired waivers, plus a duplicate refusal |
| policy-test | W.run_policy_test over the owner suite, using owner substitution |
| baseline-show | adopt_admitted_baseline_v3 with all pivots available, plus a missing/revoked variant and a no-trust-origin refusal |
| recommend | security discovery → boundary_inventory → native discover_units (P3 fixture), plus a boundary-crossing native refusal |
| repair-preview | admitted closed-world preview |

For each envelope the controls check:
- schema admission;
- parity read at the pointers and recovered identically from human, json and agent;
- mutated human parity detected;
- missing carrier refused by schema, and a pre-commit delivery fault on rendering;
- cross-command record refused;
- another command's surface refused (`QUERY_SURFACE_ENVELOPE_SELECTOR`);
- untyped member refused;
- a schema-valid join mutant refused before rendering with its specific code.

The graph `query` command is controlled in check-query-projection (`r2-query-command-parity-paths-equal-owner-projection`, `r2-query-command-generic-renderer-recovers-parity`). The current-profile projection-control rows were updated for the typed records.

## Query-step mapping (resolved)

- invocation:3 `QueryParams` is oneOf:
  - `PublicQueryParams`: one of the 20 graph-query:3 operations, with the complete GraphQueryRequestV1 whose operation, completeness and page equal the step's (`admit_query_step_params` join);
  - `HostQueryParams`: a separately closed `HostQueryOperation` extension with dotted spelling (`baseline.inspect`, `discovery.recommend`, `policy.show`, `policy.test`, `review.produce-brief`), each with its own closed request record.
- The public Operation enum is still 20 and disjoint from the host ops. The 17 non-graph public operations keep their owners.
- Dispatch:
  - query: all 20 public operations.
  - candidates: `candidate.list`.
  - inspect: `inspection.show`.
  - review-brief: host `review.produce-brief` (`--producer model` gives a model principal with modelClosureId; `heuristic` gives `{policy-rule, opensip.review.heuristic}`).
  - recommend: `discovery.recommend`.
  - baseline-show: `baseline.inspect`.
  - policy-show: `policy.show`.
  - policy-test: `policy.test`.
  - repair-preview: its own `repair-preview` step with 0 operations.
- Inventory drift controls:
  - exactly the nine commands dispatch;
  - no other command does;
  - the surfaces equal the enum;
  - parityPaths equal parityFields;
  - the step is declared;
  - the enum is not widened;
  - schema refusals for a missing dispatch, dispatch on a non-query command, an unclosed operation and the retired selector.

## /tmp historical reads (resolved)

Both external historical reads in check-workflow-projection now read current source:
- The root-clarification read is replaced by `waived-matched-presence-is-current-contract-law`, which reads the current WPC §11 sentence.
- `_chapter_s2` now reads the current `workflows-and-surfaces.md`.

The only remaining `/tmp` strings are the interpreter path in docstrings and the pre-existing `--output` write-destination guard (V12_ROOT), which reads nothing.

## Checks executed on the final tree

| Label | Checker | Result |
|---|---|---|
| final-1 | workflow-projection | 766/766 pass (checker 963b6f36) |
| final-1 | query-projection | 204/204 pass |
| final-1 | current-profile | 38 pass |
| final-1 | comparison-knowledge | 1 pass |
| final-1 | workflows-v1 | 1816 passed, exit 0 |
| final-1 | integration (registry parity) | 412 passed, exit 0 |
| final-1 | composition | 30 |
| final-1 | semantic-replay | 30 |
| final-1 | evaluator-faults | 41 |
| final-1 | replay | 73 |
| final-security | security owner launcher | **exit 1, `sourcePinsValid: false`, 0 cases executed** (22 changed pinned paths). This is the pin gate, not a pass. |
| final-security | security body via `tools/run_security_unpinned.py` (explicitly bypasses the owner pin gate) | 464/464 cases, 11/11 sweeps hold. This is not the owner launcher, and pins are not evaluated. |

**Failed and superseded attempts (preserved).**
- `r2-2-wp`: workflow-projection crashed (TypeError). The policy-test fixture passed the raw suite, and `$` references were unresolved. `tools/apply_r2_fix1.py` switched to the owner checker's substitution, and `r2-3-wp` then passed 763.
- Self-caught design gap after r2-3: `recommendations` had no registered vocabulary, and the policy-test refusal wording was wrong. `tools/apply_r2_fix2.py` closed recommendations to zero rows, fixed the wording and added 3 controls.
- r2-1-query, r2-3-others and r2-4-security are superseded by final-1 and final-security.

## Breaking draft schema and identity effects (pre-release design corrections; the selected majors are retained)

- **comparison:2.** No shape change. comparisonResultId changes for any comparison in which an unmatched occurrence is a barrier: presence moves from `false` to null and the entry becomes INDETERMINATE. Retained comparisons are not relabelled or recomputed.
- **baseline:2.** No descriptor field changed, so baselineId is unaffected. `absenceKnowledge` and `unmatchedOccurrences` are preserved and are now also read as barriers at comparison time.
- **command-envelope:3.** Breaking:
  - the `querySurface` value `command-owned-summary` is removed and 8 values are added;
  - there is a new required typed `queryRecord` for non-graph surfaces.
  
  Draft envelopes that used the old selector no longer validate, and nothing coerces them.
- **invocation:3.** Breaking. `QueryParams` becomes Public|Host, and public query steps now require `request`. Invocation bytes, and any identity computed over query-step params, change. `HostQueryOperation` and five request records are new.
- **command-inventory:3.** Breaking. `queryDispatch` is required for query-class commands, and the v3 inventory instance is updated.
- **Registry and both DomainDetailCode mirrors.** Additive: `REVIEW.CANDIDATE_UNKNOWN` (owner workflows).
- **graph-query:3.** Unchanged.

## Ownership and integration needs for root

- **native823v2.**
  - `DiscoveryRecommendationRecordV1.discovery` is `$ref` native UnitDiscoveryV2.
  - The profile registry and both workflow checkers now load `native/native-evidence.schemas.v2.json`.
  - config2 root normalization uses discovery-defaults `normalize_explicit_root`.
  
  Native changes flow through that `$ref`, and root must bind the shared paragraph.
- **ce3v2.** Termination host joins and the carrier are read-only for ce3v2. `delivery_required_termination` is the existing law and was not changed.
- **Shared paragraphs for root integration:** workflows-and-surfaces §8 (the public query carriers table, parity pointers, query-step operations, query-class failures), §5 (inspection, candidates, policy show) and §2 (baseline show), plus the query-projection-contract §7 carrier sentence.
- **Repair owner.** The reference `repair_preview` constructor still emits a major-1 descriptor. The repair-preview control relabels it as repair:2 (sets schemaMajor 2 and remints the id), and says so in `r2-repair-preview-reference-constructor-emits-historical-major-1`. The repair owner needs a repair:2 constructor.
- **config2.** No config2 document schema is published. This correction closes proposals to explicit `discovery.workspaceRoots` and publishes no other grammar.
- **Recommendations.** They carry zero rows because no recommendation detail is registered. Any vocabulary needs registered details and a successor record.
- **Policy-test suite admission refusal.** It uses the existing registered `CONFIG.INVALID` detail, whose registry row owner is security. Root should confirm that the row covers workflow suite admission.
- **Synthetic inputs in the controls.**
  - host closure `trustOrigin` (host_from_graph does not supply one);
  - waiver documents;
  - a disposition receipt id;
  - the security P3 fixture copied into the workflow checker, with synthetic marker hashes.
- **Not modelled:** HTML renderings.
- **Pins:** not updated. Root rebinds them and runs the owner launcher after integration.

## Standing

These are reference and design corrections with focused reference controls. No independent acceptance, readiness, pin validity or product qualification is claimed.
