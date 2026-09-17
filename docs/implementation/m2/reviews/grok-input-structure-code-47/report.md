# Advisory: draft-47 first-evaluation structure (five copied files)

**Reviewer:** Grok. Root remains lead. Not Claude agreement.  
**Kind:** Bounded **code** advisory of five pinned draft files vs accepted SOURCE46. **Not frozen-source acceptance. Not runtime22. Not complete evaluator reconstruction, predicate truth, Run replay, or custody.**  
**Work tree:** `/tmp/opensip-implementation/m2-grok-input-structure-47-advisory/review`. Copied sources, SOURCE46 export, trial-47 product, and live repositories were not edited. Tests used an overlay copy under this tree.

## Verdict

**NO-REQUIRED-FINDINGS** for this draft scope.

`compile_plan_policy` compiles RuleProgramV2 from Plan policy bytes only. `inspect_first_evaluation_structure` closes input-side structural owners from Plan / execution-plan / snapshot / capture without a synthetic Run or proof. Anchors use `snapshot.projectId` (Plan has no `projectId`). Extra `rule-program` on `evaluation_refs` refuses. Ambient unselected historical outputs remain permissible. Run `inspect_policy_program` / `inspect_run_links` / `inspect_retained_walk` keep prior behavior after factoring.

## Pins (copied = trial-47 product; 5/5)

| File | Bytes | sha256 |
| --- | ---: | --- |
| `policy.rs` | 24562 | `dffed77aacc1f59649cf794120a282fa5f1871af511f5867b4451c64372e9c7f` |
| `lib.rs` | 3570 | `ffe3fcee6581a973771a46973b6cb4aa546a564f93fbb5c4978bb1023aaf73dc` |
| `run_links.rs` | 13724 | `59d137d1a5881b1e670afb193343cce9e2c493cb6d3fcb2af600267cdb12d694` |
| `full_walk.rs` | 19067 | `bf852ce6d0ba5cf01036ec06f13a58f6ce5549209f94f960a159e9e58fa0c7fb` |
| `closure.rs` | 57335 | `86e0f428a9276920cdca5a943cbcb29dadda6bb365c2522640dd65d548783e80` |

SOURCE46 baselines: `policy.rs` 22244 / `451f0440…`; `lib.rs` 3422 / `1135264f…` (exact prefix of draft); `run_links.rs` 11849 / `60e5b035…`; `full_walk.rs` 13104 / `01dd5478…`; `closure.rs` 56835 / `1b66d79a…`.

## Selected X / I (checked independently)

X `InputRefV1` domains are exactly `view`, `import`, `coverage`, `subject-inventory`, `target-attribution`, `incoming-search`, `candidate-producer-result`. Capture `selectedRefs` must not name `execution-inputs`. Graph `evaluationInputRefs` = those selected refs **plus exactly one** `execution-inputs` blob. Identity `ProofInputRef` still enumerates extra domains including `rule-program`; that is **not** a license to put a rule-program on first-evaluation refs. Rule programs compile from Plan policy; a proof digest is not an input. Previous optional-rule-program suggestion is incorrect for current X.

Plan descriptors have no `projectId`. Snapshot does. First-evaluation grant/source joins must use `snapshot.projectId`. Ambient unselected old outputs in the store must not be globally banned; C(capture) ignores them.

## Public owners

**`compile_plan_policy(inputs, plan_id, budget)`** — identity-admit Plan; shape-admit PolicyDocumentV2 and WaiverSetV1 from Plan digests; compile `{schemaVersion:2, policyDigest, rules:[{ruleId, ruleProgramRef, emitWhen}]}` from policy rows; shape-admit RuleProgramV2; same enabled/disabled `check_program_laws` as the Run owner. No Run, seal, or proof. Local steps are not a Plan work budget.

**`inspect_policy_program(run_id)`** still loads the proof-held program and checks `RULE_PROGRAM_POLICY_JOIN` / `RULE_PROGRAM_COMPILATION_JOIN` against that compile. Shared `compile_program` / `check_program_laws`. Replay path unchanged.

**`inspect_first_evaluation_structure(inputs, plan_id, execution_id, evaluator_closure, evaluation_refs, limits)`**

1. Separate walk / owner / invocation limits; zero is `Limit`.
2. Plan → snapshot; anchors `{plan_id, Plan.snapshotId, snapshot.projectId}`.
3. **`inspect_execution_input_join` first** (exact one capture, `EVALUATOR_EXECUTION_INPUT_SELECTION`, expected evaluator closure, parameter/enumeration/Plan view/import/stage, X join). Non-ADMIT → `ExecutionRefused(document)` and **no** later owners.
4. Closed structural walks of Plan, execution-plan, snapshot, then the capture record (`inspect_current_record_with_owner`). Shared `ClosedOwner` payload/native-frame/capability/source-plan joins. Historical objects not on those roots are not inspected.
5. `inspect_plan_native`; referenced universes ⊆ retained frames.
6. `inspect_plan_semantic_links`: capability census, snapshot/config/budget, grant at **snapshot.projectId**, VCS inventory. No proof joins.
7. `compile_plan_policy`.

Does not call `inspect_retained_walk`, `inspect_policy_program(run_id)`, `inspect_predicate_witnesses`, or `inspect_evidence_roots`.

**Run factoring:** `inspect_snapshot_config` / `inspect_grant_vcs` extracted; Run still joins `run.projectId` to snapshot (`PROJECT_SNAPSHOT_JOIN`) then grant. `inspect_run_links_with_capabilities` and `inspect_retained_walk` still start at Run. `inspect_current_record` now delegates to `inspect_current_record_with_owner(..., RejectOwner)`.

## Independent overlay (this review tree only)

SOURCE46 product copy + five pinned files. Probe writes redirected off the trial tree.

| Check | Result |
| --- | --- |
| SOURCE46 `execution_inputs_recheck_*` (51 host) | pass |
| `compile_plan_policy` 930 no-Run/no-proof cases | pass |
| First-evaluation structure 24 no-output cases | pass |
| 17 adversarial controls | pass |
| SOURCE46 `full_retained_walk_checks_*` | pass |
| evaluator `--lib` | 18 pass |

Reachable extra-rule-program (packet-0 refs plus `{domain:rule-program, digest}`): execution join `Refused("EVALUATOR_EXECUTION_INPUT_SELECTION")`; structure wraps the same. Ambient historical outputs: both ADMIT. Missing closure/import payloads: X may ADMIT; structure `MissingBlob` / `BlobDigest` — that is the new composition, not a silent skip. Zero/one walk and owner counters: `Limit` / `Graph(Limit)`.

## requiredFindings

None.

## Limits

Draft-47 only. Not frozen SOURCE47, not runtime22, not complete first-evaluation **evaluator** closure (atom truth, reconstruction, replay, custody). Sidecar JSON-schema mismatch can be X-ADMIT then structure `Schema(Mismatch)` because X does not re-shape target-attribution/incoming-search as registered records; structure walk of the capture does. `ProofInputRef` remains a wider identity enum than X `InputRefV1`; first-evaluation refuse of extra `rule-program` is selection, not that enum shrinking. Future freeze needs new bytes.
