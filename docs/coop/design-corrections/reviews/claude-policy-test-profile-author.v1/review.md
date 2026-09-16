# Policy-test profile correction: evaluator3 PolicyTestSuiteV2 (author correction)

Coauthor origin 823bf66b-e92a-4789-ab81-63a1a9dc371d. Runtime `R=/private/tmp/opensip-design-corrections/claude-policy-test-profile-author.v1`.

**Standing.**
- Bounded, authorized AUTHOR correction of the completed REAL-GAP assessment (F1–F9).
- Done in my own regular-file copy of the mutable successor.
- Architecture, design and reference correction only.

**Not done:**
- no product work, commits or pushes;
- no planning, pin, launcher or grade edits;
- no final acceptance or readiness claim.

The checks and probes are author reference evidence, not independent review. I did not read the ce3 tree, blind inputs or private/session logs. The completed assessment runtime is untouched.

The machine record is `R/review.json` (sha256 `7f1af85c35765a7656ec10421beb0700372f64d30acda5807174aff65324cd93`). `R/build_review.py` assembled it by recomputing every claim below from custody, receipts and probe outputs; it refuses if any claim fails.

## 1. Custody

**Source copy.**

| item | value |
|---|---|
| input (mutable) | `/tmp/opensip-design-corrections/consumer24-corrections-successor.v1/source` |
| capture | `R/work/source`, taken by `R/capture_source.py` |
| size | 12905 files, 737522254 bytes |
| copy method | fresh `open(…,'xb')` regular files; link count checked; no hardlinks |
| drift / copy faults | none in two hash passes / none |
| file-list manifest sha256 | `a1c2fd53d26e1dde44017c6913e4cf4e7ddd175faef92bab06c7742bf6a1d7e4` |
| custody record | `R/custody/captured-source.json` |

**Differences from earlier captures.**
- **Versus the assessment's fixed capture:** only `workflows_model.v3.py`, `workflows-and-surfaces.md` and three `docs/v2/architecture/*` files differ. This is the f561 integration.
- **Versus my earlier author-package-migration capture:** 30 paths differ. They are listed in the custody record.

**Pre-edit snapshot.** `R/work/baseline-files` holds 54 files: all of `workflows/` and `docs/v2/contracts/product-v1/`, indexed in `R/custody/baseline-files.json`. Exact diffs are taken against it.

**After the edits.** The builder verifies:
- the edited copy differs from the capture only in the 12 authorized paths;
- no `__pycache__` was written.

## 2. What changed

Exact before/after hashes are below. The full diff is `R/output/correction.diff` (1529 lines, sha256 `beaef5336ff88ac913e0e5ad371c4cee4a7710f788d172614fdcd14715037088`); the manifest is `R/custody/correction-manifest.json`.

| status | path (under `docs/`) | before sha256 → after sha256 |
|---|---|---|
| added | `coop/design-corrections/workflows/schemas/evaluator3/policy-test.schema.json` | — → `963d5bb1977991b26fce4be333aac544291cbc3908717388ee8509acf20fd3bd` |
| added | `coop/design-corrections/workflows/policy_test_model.v3.py` | — → `8138e2e8a4c4c0087dfb655522dbec254209c6ed1e82b49157b2cb6d87801b93` |
| added | `coop/design-corrections/workflows/policy-test-cases.v3.json` | — → `d1e94da920a28a13a320fe2f344e1266eb7930fe518c24a484c61717969ec256` |
| modified | `coop/design-corrections/workflows/workflows_model.v3.py` (policy part only) | `e2dbb665…90948185` → `0c016406…2c888d50` |
| modified | `coop/design-corrections/workflows/check-workflow-projection.v3.py` | `56647271…9d5fddc2` → `d0b4e952…3fe133ca` |
| modified | `coop/design-corrections/workflows/command-inventory.v3.json` | `2aa72b52…fc014020` → `d303cc64…397a4e66` |
| modified | `coop/design-corrections/workflows/schemas/evaluator3/command-envelope.schema.json` | `6fb8f428…a9f0cefb` → `09292fc1…ee318830` |
| modified | `coop/design-corrections/workflows/schemas/evaluator3/invocation-record.schema.json` | `8c714107…c4bb74a7` → `65980226…6247ddc8` |
| modified | `coop/design-corrections/workflows/workflow-projection-contract.v3.md` | `3bdb5c1e…75cfd60d` → `421e3eb2…d2d6a84e` |
| modified | `coop/design-corrections/workflows/README.md` | `2b220e3e…a6b26d1c` → `1fca693c…76da21cb` |
| modified | `coop/design-corrections/workflows/schemas/evaluator3/README.md` | `67d552db…ecad6474` → `66c8cc1e…87052c31` |
| modified | `v2/contracts/product-v1/workflows-and-surfaces.md` | `8ea51b97…2f7d0d319` → `707d8147…34bfcc6d` |

Values are the first 8 and last 8 hex digits. Full 64-hex values for every row are in the manifest and in `review.json` → `correction.changes`.

**Byte-unchanged owners** (verified against the capture):
- `workflows_model.v1.py`
- retained `schemas/policy-test.schema.json` (PolicyTestSuiteV1)
- both policy documents
- `workflow-cases.v1.json`, `check_workflows.v1.py`, `command-inventory.v1.json`
- `repair_closed_world_selection.v1.py`
- `foundation/atom_model.v1.py` and the evaluator projection registry
- `workflow_projection_model.v3.py`, `query_surface_projection.v3.py`
- the public detail registry

**Repair code untouched.** In `workflows_model.v3.py`, the repair closed-world selector and repair:2 constructor region (96 lines, sha256 `7c7356e4…1702efd3c`) are byte-identical, as is everything from the file header through `admit_policy_rule`. Proof: `R/custody/repair-region-unchanged.json`.

## 3. Root decisions as implemented

### 1. Suite
New owner `urn:opensip:product-v1:workflows:evaluator3:policy-test:2` defines `PolicyTestSuiteV2`:
- `schemaMajor` const 2;
- `candidatePolicy` → `urn:opensip:product-v1:policy-document:2#/$defs/PolicyDocumentV2`;
- waivers `WaiverSetV1`, and the retained `Case`/`Override` definitions, unchanged.

Result shape is unchanged: `PolicyTestResultV1`, the `policytest2` prefix and the `PolicyTestResultRecordV1` carrier stay. Identity:
- `suiteDigest` = H(`workflow.policy-test-suite`, admitted SuiteV2), whose preimage now carries major 2 and the V2 candidate;
- candidate/effective digests are raw SHA-256 over PolicyDocumentV2 bytes.

This is an explicit **breaking input/profile change**. A retained SuiteV1 and its results stay historical evidence and are not re-evaluated.

### 2. Owner
`workflows_model.v3` now defines its own `run_policy_test` and `run_admitted_policy_test`. The imported legacy function stays available as `_base.run_policy_test`. The new functions:
- resolve with the v3 `resolve_policy` and atom owner;
- resolve waivers with the unchanged WaiverSetV1 owner;
- evaluate cases through the new focused owner `policy_test_model.v3.py`.

The grammar classifier now reads `policy-document.v2.schema.json`, rooted at `PolicyDocumentV2`. The f561 positional oneOf/anyOf/allOf helper is byte-unchanged.

**Admission precedence** is published in the new schema as `x-opensip-admission-precedence`:
1. suite major;
2. candidate major → `REQUEST.SCHEMA_MAJOR_UNSUPPORTED` / `EVALUATION.MIXED_OUTPUT_MAJOR`, the same refusal `workflow_projection_model.v3` uses. An integer major is checked before any grammar classification, so a wrong major is never called an imperative key.
3. closed SuiteV2 schema → `CONFIG.INVALID` with `POLICY.IMPERATIVE_KEY_REFUSED` or the shared `CONFIG.INVALID` detail;
4. fixture and override admission → `CONFIG.INVALID`;
5. current resolver details.

`resolve_policy` also refuses a non-V2 document with the same typed major refusal. `identity-model.v3` never calls `resolve_policy`. No new D9 code or detail was added.

### 3. Semantics
Evaluation reuses the current atom owner:
- its registry;
- `_rung_ge`, the string/integer comparators and `_and_fr`;
- native quantifier law mirrored from `_eval_native`.

It adds no relation table. It covers endpoint source and target, kind applicability (enforced at admission by the atom owner), filter projections and Kleene logic. Two drift guards refuse to load if the fixture field map stops matching the V2 `FieldFilter` enum and `FactRecordCandidate`, or if the selector map stops matching the registry's observation selectors.

**Target endpoint through the corrected public route.** Over the same edge `src/b.ts → src/a.ts` with `targetKind` `file`:
- target rule `unimported-file` finds `src/b.ts`;
- source rule `import-free-export` finds `src/a.ts`.

### 4. I4: unrepresentable inputs
The new schema publishes the facts-fixture law as `x-opensip-fixture-representation`:
- **Unrepresentable fields are UNKNOWN:** the endpoint universe domain, `testResult`, `exitStatus`.
- **Unrepresentable selectors are UNKNOWN:** `test-execution`, `test-case`.
- **Representable imported rows** (`runtime-subject`, `history-subject`) can only establish known matches. Absence never proves absence.
- **Target kind:** an absent `targetKind` is unknown; `external` never matches.

**Expectations and outcomes.**
- Affected finding and no-finding expectations are `indeterminate` unless a known finding decides them.
- Known hits, the optional-evidence-absent disclosure, strong Kleene and gating are preserved.
- `PolicyTestResultV1`/`CaseResult` shape is unchanged; the result carries no per-rule unknown cause (stated as a limit).
- No imported observation is invented, and sources cases stay `not-executable`.

### 5. References
**Contract (`workflows-and-surfaces.md`):**
- Dispatch paragraph: the `policy test` input is SuiteV2; "test" means the retained `test-execution.schema.json` documents.
- §5 authoring test: rewritten for SuiteV2, including the precedence, the representation law and the breaking-change/history statement.
- §8: surface row, host-operation prose and query-class failures.
- §9: new golden row.
- §10: suite preimage.

**Other owners:**
- Projection contract §1: dispatch table row plus a major-refusal sentence.
- Evaluator3 envelope `PolicyTestResultRecordV1` and invocation `PolicyTestRequestV1` descriptions.
- Both READMEs.
- `command-inventory.v3.json`: `policy-test-suite-inadmissible` text now names SuiteV2, and there is exactly one new golden, **`policy-test-suite-major-unsupported`** (request-rejected 2, `REQUEST.SCHEMA_MAJOR_UNSUPPORTED`, `EVALUATION.MIXED_OUTPUT_MAJOR`). Goldens go 44 → 45.

No new `##` sections. `identity-model.v3.py`, `workflow_projection_model.v3.py` and the query owners needed no change: they glob the evaluator3 schemas or never reference the suite.

### 6. Controls
There are 24 new `pt2-*` checks in the existing `check-workflow-projection.v3.py` child; all prior checks remain present and passing.

**Current route**
- The owner-admitted authored SuiteV2 (schema and resolver admitted, V1 definition refused) reaches the exact authored outcomes (5 passed / 0 failed / 3 indeterminate / 1 not-executable) and a valid carried result. The existing R2 envelope/parity/mutant checks for `policy-test` now run on this V2 result.
- Target vs source endpoint discrimination through the public route.
- The V2 test-filter rule is admitted by the resolver, then honestly unknown.
- An absent imported row never proves absence.

**Major and resolver refusals**
- Historical V1 suite, a V1 candidate inside a V2 suite, and a V1 candidate carrying `hook` all refuse on the typed major route. That includes a failure envelope and the golden.
- The current resolver refuses a V1 policy typed.
- A policy only the legacy resolver accepts (`history-change` + `confidenceMillionths`) is schema-admitted, then refused `POLICY.UNKNOWN_RULE` (`ATOM_FILTER_FIELD_FORBIDDEN`) and not carried. So is a forbidden file target endpoint (`ATOM_ENDPOINT_UNAVAILABLE`). The historical resolver alone still accepts the first.

**Grammar and generic routes**
- A valid V2 `endpoint` member is not treated as an imperative key.
- Unknown override rule, wrong override type and an off-ladder fixture rung each refuse `CONFIG.INVALID`.
- A lawful override changes only the effective policy.
- The existing oc2 routes stay closed on SuiteV2: missing cases, enum violation, waiver extra member, hook, string expression, positional include, duplicate waiver (golden), residual golden.

**Historical route**
- `pt2-historical-workflow1-policy-test-route-unchanged` pins `policytest2:5ce020d40b29ce7f1592189d66efd007d732c699a4c612e75b6c788cd497ee27`.
- The retained workflow1 checker's stdout is byte-identical.

## 4. Receipts and results (`R/receipts/`)

| receipt | exit | result |
|---|---|---|
| baseline-check-workflow-projection-v3 | 0 | 795/795 passed (pre-edit) |
| post-edit-check-workflow-projection-v3 | 0 | **819/819** passed; 0 removed, 0 flipped, 24 added (all `pt2-*`) |
| baseline-check-query-projection-v3 | 2 | retained failure: my command omitted the required `--report` |
| baseline-check-query-projection-v3.2 / post-edit-check-query-projection-v3 | 0 / 0 | 204/204 before and after |
| baseline-check-workflows-v1 / post-edit-check-workflows-v1 | 0 / 0 | 1816/1816; stdout byte-identical. Its report differs only in its `sourceSha256` table, which hashes current files it lists; all check rows are identical |
| baseline-check-array-orders / post-edit-check-array-orders | 0 / 0 | 121 → 123 (the new schema's 2 arrays are declared) |
| post-edit-check-policy-derivation-v3 | 0 | 6/6: a foundation child whose close_run loads the edited `workflows_model.v3.py` |
| pre-edit-route-probe | 1 | retained failure: my probe lacked the checker's `$ARGV` constants |
| pre-edit-route-probe.2 | 0 | V1 suite admitted (legacy id `5ce020d4…`); lawful V2 suite refused `POLICY.IMPERATIVE_KEY_REFUSED` |
| post-edit-route-probe | 0 | historical id unchanged; V1 suite refused by typed major; V2 suite → `policytest2:d7fcc42c3e728460c73449913755331ff7ab232994d1abe286c4b8b2c14b5f67`, 5/0/3/1 |
| fixture-semantics-probe | 0 | 17/17 focused controls through the corrected route |
| make-diff | 0 | manifest and diff above |

The 17 focused controls cover:
- count-at-most known above N, and under partial Coverage;
- or/and/not under unknowns;
- universe filter unknown; confidence filter representable;
- mixed optional-absent plus unrepresentable causes; optional-absent alone disclosed;
- export and external `targetKind`; cross-universe fact;
- `maxCount` and no-finding with unknown subjects;
- non-integer major goes to the schema route;
- unregistered fixture relation;
- deterministic, key-order-independent identity.

No background process is running.

## 5. Root integration

- **No new child checker is required.** The controls live in the existing workflow-projection child, and the 17-job launcher list is unchanged.
- **Pins (root):** update the five pin sets for the 9 modified paths and add the 3 new paths:
  - `workflows/source-pins.v1.json`
  - `foundation/source-pins.v1.json`
  - `foundation/evaluator3-source-pins.v1.json`
  - `security/source-pins.v1.json`
  - `native/source-pins.v2.json`
- **Planning (root):** the M5 host policy row for golden `policy-test-suite-major-unsupported` (goldens 45). Planning files were not edited.
- **Reports:** the retained `workflows/workflows-report.v1.json` was not regenerated; it already differed from a fresh run at baseline. Root regenerates receipts under the new pins.
- **ce3 merge:** the repair region and `repair_closed_world_selection.v1.py` are byte-identical here. Expect overlap only in `check-workflow-projection.v3.py` and contract prose, which need a three-way merge.
- **Full suites:** root reruns the full launcher and suites. I ran only the checkers listed above.

## 6. Limits

- **Scope of semantics.** These are bounded standalone authoring-test semantics over finite facts fixtures. They are not production evaluator, provider, full Run or native qualification, and sources cases remain not-executable.
- **Fixture representation.** A fixture fact has one universe, no endpoint-universe domain, no test payloads and no import-wrapper completeness. By the published law these evaluate unknown.
- **Row matching.** Runtime and history rows match by subject path. The atom owner's overload and row-ambiguity refusals are not modelled.
- **Result carrier.** The result carries no per-rule unknown cause. The retained legacy `CaseResult` description text is narrower than the new §5 law and is left byte-unchanged; no shape change was needed.
- **Behaviour change.** An unknown override rule or wrong override type is now `CONFIG.INVALID` on the current route; the historical model raised an untyped `KeyError`.
- **Oracle.** Expected outcomes in `policy-test-cases.v3.json` and the probe are author expectations; independent review is the oracle.
- **Checks run.** Only the checkers listed in §4 were run.
- **Root-owned and untouched:** pins, planning, launcher, grades, source acceptance.
