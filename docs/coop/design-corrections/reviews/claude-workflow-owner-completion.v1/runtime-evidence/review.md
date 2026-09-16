# Workflow owner completion v1: repair:2 constructor and policy-test CONFIG.INVALID route

Coauthor origin f5617310-c7c7-4d85-acdd-31370f220944.

This is an architecture, design and reference change only. It is not a product change, a commit, a push, a pin/planning/package/grade update, or an acceptance or readiness claim. The retained workflow-v2 runtime is byte-unchanged (verified below).

## Custody

- **Source (read only).** `/tmp/opensip-design-corrections/consumer24-corrections-successor.v1/source`, 12905 files. Full manifest digest `3a85464b…d774`; the recipe is sha256 over the sorted `path<TAB>sha256<LF>` lines.
- **Copy.** `work/source` is a regular independent copy of the 1360 core files. `docs/coop/design-corrections/reviews/**` (11545 historical-evidence files) was hashed but not copied.
  - Each file was written from bytes read once and re-hashed; distinct inode, nlink 1; no symlinks.
  - Core manifest digest `bdf97c11…405f`.
  - Receipts: `receipts/source-custody-and-copy.json` (385e13cb…) and `receipts/source-full-manifest.json` (7e73e9d3…).
- **Final custody** (`receipts/final-custody-and-diff.json`, sha 30475fe7…, `ok: true`):
  - capture re-hashed read-only: 0 mismatches since the copy, same digest;
  - retained v2 runtime: review.md 609011cd…, review.json 6dbde41b…, final receipt c8d38d14…, both diffs and edit log unchanged, and its 12904-file work tree matches its own final hashmap (0 mismatches);
  - work tree: 1360 files, 7 changed, 0 new, 0 missing, 0 pycache;
  - every change is in `receipts/edits/text-edits.jsonl` (9 rows, sha 3e773cb2…); 0 unexpected changes, unbroken hash chain, and each first edit starts from the capture hash.
- **Minimal delta.** `diffs/capture-to-work.diff`: 7 files, 509 lines, sha 518c6a37333d9db40e3aa4c08ab24a62defc95484d1f054769a782f73a548788. All other captured files are preserved byte for byte.

| File (under `docs/`) | capture sha256 | work sha256 |
|---|---|---|
| `coop/design-corrections/workflows/workflows_model.v1.py` | 1d89bd285b77f0b3b8f852965320ed5447038196640a55b99b3c790752bdcdd3 | be37023f173f339edcd49b2019a2c6f3d424360a2c9cdcbf95bd382fa72066dc |
| `coop/design-corrections/workflows/workflows_model.v3.py` | 6922428b625f0af2f5a63bc7dbc4b1ca472cebff249e773d325d892024404e15 | e2dbb66566eedc96ad9e966691c03cf209861124cc5729659b0b047a90948185 |
| `coop/design-corrections/workflows/check-workflow-projection.v3.py` | 963b6f3624ee76ae652ef0d38df8db27c05f5c23dfae730fe6064ebf0a1f8c7a | 56647271dbd7b288f2b3274ac4d4e394b6ba503147f5c39cedc7887b9d5fddc2 |
| `coop/design-corrections/workflows/command-inventory.v3.json` | 5321996cd07e87364fed08c95576c23ed4ccfdbcfa75bdaa47e8c738416a6685 | 2aa72b52da5a9eef611ad07cda81647323569c67fa1065eae1fdf0c8fc014020 |
| `coop/design-corrections/workflows/schemas/evaluator3/command-envelope.schema.json` | e224b3b519c8cec65f8412f8dbd0510cd23a52b27d87e86b5f71984450335746 | 6fb8f42893183ae880f4dea93b8dbb5566c5dcc98e2607391ce62e47a9f0cefb |
| `coop/design-corrections/workflows/workflow-projection-contract.v3.md` | cda2d3e3f8890cfe9e2e9f29d5b68b9209f37dea43f4eac5677e2245591e9bec | 3bdb5c1e6e03033f093c7c096e61b6205781967e8a7d3810489bef4775cfd60d |
| `v2/contracts/product-v1/workflows-and-surfaces.md` | 58893373f7bdbabd66519ed2d5d18ae63a26efc2a7beddc28db4ce6271eeef83 | 8ea51b977f1362a3ece19b5d04ec86200d99c0a76f3ba4ef13a4cd52f7d0d319 |

There are no new files, child commands, public detail codes, registry rows, schema majors or normative/reference files.

## 1. Current-profile repair:2 constructor

**Boundary found.**
- `workflows_model.v3.py` is the evaluator3 workflow owner. It loads a private instance of `workflows_model.v1.py` (`_base`), installs the retained-record closed-world selector there, and re-exports `_base.repair_preview`. That is why the current preview path (`WF3.repair_preview`, called by check-workflow-projection `_cw_preview`) emitted a major-1 descriptor.
- `workflow_projection_model.v3.py` is the pure projection. It loads its own historical v1 instance (no selector) and owns the repair target law `project_repair_targets` plus the evaluator3 schema registry. It does not own preview.
- The historical callers are separate and use major 1 with the legacy `repair.schema.json`: `check_workflows.v1.py` (`M.repair_preview`, pinned `repairplan2` ids in `workflow-cases.v1.json`) and `check-integration.py` through the integration host (`M.W.repair_preview` validated against the legacy schema).
- The projection contract (§1 table) already selected `evaluator3:repair:2` (major 2, `evidenceRunId` run3), so no global major replacement was needed.

**Change.**
- **Historical builder (`workflows_model.v1.repair_preview`).** Gains one additive keyword-only parameter, `descriptor_major=1`, which is used where the descriptor is built. Values other than 1 or 2 raise. With the default, every historical caller is byte-identical: the workflows-v1 and integration stdout hashes equal the unmodified-capture baseline.
- **Current owner entry (`workflows_model.v3.repair_preview`).** Before any descriptor exists, it refuses:
  - non-authoritative evidence: `REQUEST.PRECONDITION_FAILED` / `REPAIR.EVIDENCE_RUN_NOT_AUTHORITATIVE` (authority is still checked first);
  - a missing retained closure, or a retained closure whose `planId` is another Run's: `REPAIR.EVIDENCE_RUN_UNAVAILABLE`;
  - a non-run3 evidence Run: `REQUEST.SCHEMA_MAJOR_UNSUPPORTED` / `EVALUATION.MIXED_OUTPUT_MAJOR`;
  - any target that is not a matched finding-key2 of the retained Run, or has incompatible metadata, via the projection owner's `project_repair_targets`: `REPAIR.TARGET_CORRESPONDENCE_UNAVAILABLE` / `REPAIR.TARGET_METADATA_AMBIGUOUS`.

  It then runs the shared builder (retained-record selector, edits, trust, requirements) at `descriptor_major=2` and returns only a plan that `admit_repair_plan_v2` admits.
- **`admit_repair_plan_v2`.**
  - a plan whose major is not 2 refuses `REQUEST.SCHEMA_MAJOR_UNSUPPORTED` / `EVALUATION.MIXED_OUTPUT_MAJOR` (no coercion);
  - the closed repair:2 schema is checked through the evaluator3 registry;
  - a `repairPlanId` that does not recompute refuses `CONFIG.INVALID` / `IMPORT.ARTIFACT_CORRUPT`, the existing plan-validation detail.

  The descriptor is built at its major before identity exists, so nothing is relabelled or reminted.
- **Checker.**
  - The v2 r2 relabel block and its check (`r2-repair-preview-reference-constructor-emits-historical-major-1`) are removed. The repair-preview carrier now carries `cw_pos_plan` exactly as the owner returned it.
  - Stale statements in the `_cw_preview` docstring, section header and report `projectionScope`/`notClaimed` are corrected.
- **Normative text.**
  - projection-contract §5 gains a constructor bullet (entry point, refusals, admission, historical constructor).
  - workflows-and-surfaces §6 gains one sentence: evaluator3 preview emits repair:2, with targets joined to the retained Run, and neither major is relabelled into the other.

**Controls** (check-workflow-projection, over the existing fully admitted closed-world Runs, all pass):
- **Positive:**
  - `oc1-current-constructor-plan-is-repair-2-and-owner-admitted`
  - `oc1-every-current-preview-control-plan-is-repair-2` (positive, conflicting negative, alternative requirements, create-only, dynamic-dispatch plans)
  - `oc1-repair-preview-command-surface-admits-the-owner-plan-without-relabel` (reaches the R2 closed carrier and joins)
  - the existing selector controls (including `repair-cw-evaluator3-refuses-a-caller-selected-record`) still pass on the owner path
- **Historical preserved:**
  - `oc1-current-and-historical-profiles-are-separate-module-instances`
  - `oc1-historical-constructor-keeps-a-keyword-only-major-1-default`
  - `oc1-historical-profile-still-emits-major-1-from-a-caller-selected-record`
  - `oc1-historical-profile-trusts-a-caller-listed-target` (a recorded contrast, not a change)
- **Refused:**
  - `oc1-current-constructor-refuses-a-target-not-matched-in-the-retained-run`: the adapter lists the target, and the historical profile would build the plan
  - `oc1-current-constructor-refuses-a-retained-closure-of-another-run`
  - `oc1-current-constructor-refuses-a-historical-run2-evidence-run`
  - `oc1-current-constructor-keeps-authority-first`
  - `oc1-current-admission-refuses-a-historical-major-1-plan`
  - `oc1-unreminted-relabel-is-schema-valid` together with `oc1-current-admission-refuses-an-unreminted-relabel`

**Goldens.**
- The pinned `repairplan2` values are historical major-1 outputs of the v1 constructor (workflow-cases, security authorization cases). Their owner history is unchanged, and so are they.
- The current-profile closed-world plan ids were never pinned. They now differ because descriptor major 2 enters the preimage; this is the identity effect root should bind.

## 2. CONFIG.INVALID for policy-test suite admission

**Error code and detail are different things.**
- `CONFIG.INVALID` as **errorCode** is the D9 rejection-cause code (`config-invalid`, request-rejected, exit 2; `common:3 D9ErrorCode`).
- `CONFIG.INVALID` as **detail** is one member of the single closed public `DomainDetailCode` registry. Its row is `owner: security`, selector `security_lifecycle_model_v1.py` (`SECURITY_PUBLIC_DETAIL_CODES`).

**Finding: the detail lawfully covers the residual suite-admission route.**
- The registry `owner` field records which unit registered a code, not an exclusive emitter.
- Nothing enforces exclusivity. check-integration only requires every row to admit as a DomainDetail. The security sweep constrains what security emits.
- Other owners already reuse this exact detail on their own routes:
  - native, for external configuration (registry `newInThisCorrection`: "external configuration keeps CONFIG.INVALID");
  - identity-and-evidence ("existing public `CONFIG.INVALID` carrier and detail").

  So the owner label is not a contradiction, and no new code is warranted.

**Contradiction found and corrected (my v2 sentence, workflows-and-surfaces §8).** It routed every suite that fails `PolicyTestSuiteV1` admission to the CONFIG.INVALID detail, and called resolver refusals "result data with `resolverAccepted=false`". Both conflict with the workflows owner's own law:
- **(a)** A policy key outside the closed grammar, or a string expression, is `POLICY.IMPERATIVE_KEY_REFUSED`. See workflows-and-surfaces §5 (policy paragraph), inventory golden `policy-test-imperative-key` and its golden observation.
- **(b)** A resolver refusal is a request rejection. See goldens `policy-test-duplicate-waiver` and `policy-test-imperative-key` (request-rejected 2), and `run_policy_test` returning the refusal.

**Smallest closed correction** (owner law plus its mirrors):
- **§5 authoring test.** Admission precedes evaluation, and every refusal has errorCode `CONFIG.INVALID`. The detail is:
  - `POLICY.IMPERATIVE_KEY_REFUSED` when the candidate policy has a member no closed alternative declares at that position, or a string where every alternative there is an object;
  - otherwise the shared registered `CONFIG.INVALID` detail, with an explicit cross-reference to its security registry row and the native reuse;
  - for an admitted suite that the resolver refuses, the same termination with the resolver's detail. Its `resolverAccepted=false` result is not a carrier.
- **§8.** The query-class failure clause is corrected, and the policy-test carrier cell now reads `resolverAccepted=true` only.
- **§9.** Selected goldens gain the row "policy test suite otherwise inadmissible | request-rejected 2 | `CONFIG.INVALID` | `CONFIG.INVALID`".
- **Inventory mirror.** New golden `policy-test-suite-inadmissible` (policy-test, request-rejected, 2, `CONFIG.INVALID` / `CONFIG.INVALID`). It is additive and within the 128 bound.
- **Carrier mirror.** `command-envelope:3` `PolicyTestResultRecordV1` now requires `result.resolverAccepted` const true, with its description stating the route.
- **Owner reference** (`workflows_model.v3`):
  - `admit_policy_test_suite` and `run_admitted_policy_test`;
  - positional `policy_grammar_violation` over the policy-document grammar: only `oneOf`/`anyOf` branches are alternatives, and structural `allOf` members are followed while `if`/`then` members are not;
  - suite schema through the evaluator3 profile registry.
- The public detail registry and both DomainDetailCode mirrors are unchanged.

**Controls** (check-workflow-projection, all pass):
- **Positive:** `oc2-admitted-suite-runs-the-same-authoring-test`.
- **Typed refusals, each through a schema-valid failure envelope with exit 2 that asserts errorCode and detail separately:**
  - `oc2-suite-missing-cases-is-config-invalid-with-the-shared-config-invalid-detail`
  - `oc2-policy-enum-violation-is-not-a-grammar-violation`
  - `oc2-waiver-set-member-is-not-a-policy-grammar-refusal`
  - `oc2-owner-imperative-key-case-is-policy-imperative-key-refused` (the owner's workflow-cases fixture)
  - `oc2-owner-string-expression-case-is-policy-imperative-key-refused` (the owner fixture)
  - `oc2-grammar-law-is-positional-for-a-member-declared-elsewhere` (`include`), plus `oc2-include-is-a-declared-member-elsewhere-in-the-policy-grammar`
  - `oc2-grammar-law-does-not-flag-the-admitted-candidate-policy`
- **Resolver refusal:**
  - `oc2-resolver-refusal-of-an-admitted-suite-is-the-request-rejection-its-golden-names`
  - `oc2-resolver-refused-result-is-still-a-valid-policy-test-result`
  - `oc2-resolver-refused-result-is-never-a-policy-test-carrier`
  - `oc2-resolver-accepted-result-is-a-policy-test-carrier`
- **Mirrors:**
  - `oc2-residual-route-golden-is-the-owner-termination`
  - `oc2-imperative-key-golden-is-the-owner-termination`
  - `oc2-config-invalid-is-a-d9-error-code-and-a-separately-registered-shared-detail`

## Command receipts (actual)

All commands were run as `/tmp/opensip-architecture-review-env/bin/python -I -B …` via `tools/run_checks.py` against `work/source`. Every subprocess finished before this report.

| Label | Checker | Result | Receipt sha256 |
|---|---|---|---|
| baseline-capture (unmodified copy) | workflow-projection | 766/766 pass | cc9d5ed8… |
| baseline-capture | query-projection | 204 pass | da2ca020… |
| baseline-capture | current-profile | 38 pass | 58b99e59… |
| baseline-capture | workflows-v1 | 1816 passed, exit 0 | 63b9d4f5… |
| baseline-capture | integration | 412 passed, exit 0 | f14e7ea8… |
| **oc-1 (FAILED, preserved)** | workflow-projection | 794/795. `oc2-owner-string-expression-case-is-policy-imperative-key-refused` returned `CONFIG.INVALID`: the classifier treated Atom's `allOf` `if`/`then` members as scalar-admitting alternatives. Fixed by `tools/apply_owner_completion_fix1.py`. | 8bb08fb1… |
| oc-1-others, final-others | 9 other checkers | all pass (superseded by final-2) | — |
| final-1 | workflow-projection | 795/795. Then `tools/apply_owner_completion_fix2.py` aligned the §5 wording with the classifier law (text only). | 45d114bf… |
| **final-2 (final tree)** | workflow-projection | 795/795 pass. Versus baseline: 1 check removed (the r2 relabel), 30 oc1/oc2 added. | ce6fe63e… |
| final-2-others | workflows-v1 | 1816 passed; stdout identical to baseline (8eff3089…) | 704a3adb… |
| final-2-others | integration | 412 passed; stdout identical to baseline (3fccd9e3…) | 7c93c030… |
| final-2-others | query-projection | 204 pass; stdout identical to baseline (7fd0b56b…) | f0f1cef4… |
| final-2-others | current-profile | 38 pass; stdout identical to baseline (19c461f8…) | 58b99e59… |
| final-2-others | comparison-knowledge | 1 pass | e57f8309… |
| final-2-others | composition | 30 pass | 0c5775ab… |
| final-2-others | semantic-replay | 31 pass | 1f435ac0… |
| final-2-others | evaluator-faults | 41 pass | f5bb4f98… |
| final-2-others | replay | 73 pass | 6bacf361… |
| final-2-security | security owner launcher | **exit 1, `sourcePinsValid: false`, 0 cases executed.** This is the pin gate, not a pass. It lists 55 changed-or-missing pinned paths: the 7 files of this delta; 3 `reviews/*-author-feedback.v1.md` files absent only because this copy excludes `reviews/`; and 45 paths whose bytes equal the capture, so those mismatches predate this delta. | b2bd03e5… |
| final-2-security | security body via `tools/run_security_unpinned.py` (explicitly bypasses the owner pin gate) | 464/464 cases, 11/11 sweeps hold. Not the owner launcher. | 1ce6d703… |

The baseline was taken only for the five checkers above. The other five (comparison-knowledge, composition, semantic-replay, evaluator-faults, replay) have post-edit receipts only.

## Identity and schema effects for root binding

- **Evaluator3 `repairPlanId` values change.** Current-profile plans are now built at descriptor major 2 (repair:2, run3). No historical or pinned identity changes, and there is no remint or coercion in either direction.
- **`command-envelope:3` `PolicyTestResultRecordV1` narrowing.** `resolverAccepted` must be true. This is breaking only for a draft carrier the existing goldens already made unlawful. The major stays 3.
- **`command-inventory.v3.json`** gains one golden (additive).
- **Owner API** (additive, `workflows_model.v3`):
  - `repair_preview` (the evaluator3 override)
  - `admit_repair_plan_v2`
  - `projection_owner`
  - `policy_grammar_violation`
  - `admit_policy_test_suite`
  - `run_admitted_policy_test`
  - constants `REPAIR_PLAN_MAJOR`, `REPAIR_PLAN_REF`, `POLICY_TEST_SUITE_REF`

  `workflows_model.v1.repair_preview` gains keyword-only `descriptor_major` (default 1).
- **New intra-unit dependency.** `workflows_model.v3` now lazily loads `workflow_projection_model.v3` for the target law and the evaluator3 schema registry. No cycle: the projection model does not load v3.
- **Shared paragraphs root must integrate:**
  - workflows-and-surfaces §5 (authoring-test admission route), §6 (evaluator3 repair:2 sentence), §8 (failure clause and policy-test cell) and §9 (golden row);
  - projection-contract §5 (constructor bullet).

## Substantive limitations

- **Snapshot and preimage joins.** Snapshot equality is still judged against the synthetic host adapter's `fixture_tree_snapshot_id`, not the retained Run's snapshot. Real-Run snapshot, project and preimage joins remain not claimed, as the checker report says.
- **Evidence Run binding.** The constructor binds the evidence Run to the retained closure by `planId` and the run3 prefix. It does not re-derive the run3 identity from the retained closure: the retained run record carries no `runId`, and the identity is minted by `close_run`.
- **Metadata ambiguity.** `REPAIR.TARGET_METADATA_AMBIGUOUS` is reached through `project_repair_targets` but is not exercised on a full admitted Run here; the fixture has no incompatible multi-configuration fingerprint.
- **Policy-test suite family.** The suite is still `PolicyTestSuiteV1` with a `PolicyDocumentV1` candidate policy. There is no successor, and none was designed.
- **Grammar classifier scope.** The classifier is reference code for suite admission only. The analysis-time routing of `PolicyDocumentV2` imperative keys is unchanged, and so is the fixture-observation-driven golden reach in `check_workflows.v1`.
- **Unchanged reported scope.** The config2 roots-only proposal, zero registered recommendations and HTML rendering remain as previously reported. No owning normative contradiction was found that would change them.
- **Pins and planning.** Pins, planning, packages and grades are not updated. The owner launcher stays pin-gated until root rebinds.

## Standing

These are reference and design corrections with focused reference controls. No independent acceptance, readiness, pin validity or product qualification is claimed. Root integrates, binds and runs the global suites and independent review.
