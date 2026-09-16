# Consumer24 native corrections — author review (v2, continuation of partial v1)

**Standing.** This is correction evidence from the same actual Claude coauthor (session `823bf66b-e92a-4789-ab81-63a1a9dc371d`). It is architecture, design and reference work only.

It does not include product implementation, commits, pushes, pin or planning edits, grades, or any acceptance or readiness claim. Frozen source38 was only read, and the v1 runtime was only read. Root's integrated successor tree was not touched.

## 1. Inputs and custody

- **Parent:** `candidate-subject.v38.json` (`2ddfa0db…f37e5c5`).
  - `probes/diff_report.py` refuses unless every changed file's source38 bytes still match that manifest, and it passed.
  - I did not re-hash the whole parent (dispatch: not needed).
- **v1 continuation:** root's partial capture `partial-public-artifact-manifest.json` (`14f29c96…22b91c`).
  - All 12,905 v1 `source/` files matched it (0 mismatches, 0 missing, 0 unlisted).
  - They were copied into this runtime's `source/` as regular files (`copy_v1.py`, receipt `copy-v1`).
  - v1 was never written.
- **v1 check run.** v1's full run (`*-p6-all`) did not finish.
  - `query-projection-p6-all` has no exit record, and the checkers after it never ran.
  - No v1 child process remained when v2 started.
  - Its receipts are unchanged; this runtime reran everything as `*-v2-final`.
- **A5 inputs:**
  - root `root-consumer24-js-options.v1/changes.diff` (`928930d8…`);
  - ce3 `a5-review/proposed-amendment.r2.diff` (`e86be974…`).
  - Both were merged by exact changed-section matching (`probes/apply_hunks.py`): each hunk's old block had to occur exactly once. There were no whole-file overwrites.
  - Fidelity: the merged law paragraph, the `ts-tsconfig` mode row and the F11 case region are byte-identical to ce3 `amended.r2`, and the model hunk is byte-identical to root's after-file.

## 2. Finding dispositions (11)

For each item: the owner selectors before and after, and the controls that exercise it. Control counts come from `check-native-consumer24-corrections.v1.py` (see §5).

### M1 — clone census eligibility (corrected)
- **Before:**
  - `execution_inputs_model.v1.py` `expected_source_census` owed a `clones` partition for every file-inventory row, so every default mixed Run was indeterminate.
  - `scopeCapabilityLaw` gated only closed-suffix-table dialects, so Rust was never gated.
- **After:**
  - `identity-schemas.v3.json#/x-opensip-digest-domains/bodyEligibilityLaw`.
  - Per universe, `…/domainSets/native-semantic-universe/<domain>/languageVersionBinding/bodyEligibility`: TypeScript and syntax use `dialect-table`; Rust uses `closed-suffix-set [".rs"]`.
  - `scopeCapabilityLaw.appliesToBodyEligibility`.
  - `identity-model.v3.py` `body_eligibility_table` refuses `BODY_ELIGIBILITY_UNDECLARED` / `BODY_ELIGIBILITY_FORM`. It is used by `coverage_source_variant_prerequisite` and by the producer-boundary dialect.
  - `execution_inputs_model.v1.py` `body_eligible_census`.
  - `execution-inputs-contract.v1.md` §5 supported-available row, and `native-evidence.md` "What a default `clones-fact` cell is owed".
- **Behaviour:**
  - The broad file inventory is kept.
  - Eligibility is suffix plus domain only: never ownership, membership, grammar selection or resolution.
  - An explicit request over ineligible paths is admitted as the published unknown disclosure.
- **Fixture:** `evaluator_graph_fixture.v3.py` option `clones_fact_subjects` (default OFF).
- **Real Runs:** eligible code → `pass`; missing eligible code → `indeterminate`; explicit ineligible scope → disclosed `indeterminate`, not refused.

### M2 — Predicate fragment record (corrected)
- **Before:** `program-predicate.nodeDigest` named `workflows/schemas/policy-document.schema.json#/$defs/Predicate` (v1), and the record was never validated.
- **After:**
  - `…/program-predicate/properties/nodeDigest/x-opensip-digest/record` = `workflows/schemas/policy-document.v2.schema.json#/$defs/Predicate`.
  - `identity-model.v3.py` `admit_program_predicate_node` at the program-predicate node join, refusing `PROGRAM_PREDICATE_NODE_RECORD`.
  - Identity §3 retention table, `fragment` row.
- **Real Runs:**
  - The v2 endpoint `target` and `source` atoms close.
  - The same Runs refuse under the pre-correction v1 record, with every loaded identity copy patched.
  - Eight invalid discriminators refuse.

### M3 — deterministic discovery and membership (corrected)
- **Before:**
  - U-4a delegated its rules to `discovery-defaults.py`.
  - Unit and row order existed only in the implementation.
  - Closure re-derived membership only when a derivation witness was supplied, which Run closure never does.
- **After:**
  - `native-evidence.md` §1.4 U-4a makes the prose the authority and the script a reference implementation.
  - New **U-4b** states markers, unit construction, order and ordinals, the first-match row decision, and enforcement.
  - `enumeration_model.v1.py` `_membership_order_law` runs at every enumeration admission: `ENUMERATION_MEMBERSHIP_ORDER` and `ENUMERATION_MEMBERSHIP_ROW_DERIVATION` (internal keys, added to `INTERNAL_FAULTS` and `enumeration-plan.schema.v1.json#/x-opensip-new-internal-faults`).
- **Migration:** the maintained `check-enumeration.v1.py` `membership()` fixture now sorts rows by UTF-8 path. It was non-canonical and caused 18 mismatches in v1 attempt `enumeration-p4-s3m3`, which is preserved.
- **Real Runs:**
  - reversed rows → `ORDER`;
  - a rewritten row reason → `ROW_DERIVATION`;
  - a mis-numbered unit → `ORDER`;
  - a dropped projection → `ORDER`;
  - missing and duplicate rows refuse.

### S1 — stage output schema ownership (corrected)
- **Before:** `stage-spec.outputSchemaDigest` was "registered", yet any retained blob was admitted.
- **After:**
  - `…/$defs/stage-spec/properties/outputSchemaDigest/x-opensip-digest` gains `artifactClass: producer-interface-stage-output-schema` and a `registeredBy` selector: `producerClosure` tree member at `opensip-interface/stage-output/{operation}.schema.json`, with declaration `x-opensip-stage-output {schemaVersion 1, operation, outputDomains}`.
  - `identity-model.v3.py` `stage_output_schema_member_path` / `admit_stage_output_schema` in the stage loop.
  - Refusals: `STAGE_OUTPUT_SCHEMA_OPERATION_NOT_A_PATH_SEGMENT`, `_UNREGISTERED`, `_REGISTRATION_MISMATCH`, `_DOCUMENT_INVALID`, `_DECLARATION_MISMATCH`.
  - Identity §3 "Who registers a stage output schema".
- **Migration:** the provider closures of `evaluator_graph_fixture.v3.py` and `evaluator_semantic_fixture.v3.py` now carry their stage output schema as that tree member. `integration-fixtures.py` feeds the historical v2 identity model and is unchanged.
- **Real Runs:** a registered schema closes. A schema retained but registered at another path, a declaration for another operation, and a document without the 2020-12 dialect each refuse by name.

### S2 — per-level normalization specification map (corrected)
- **Before:** `body_identity_join` admitted any retained blob as `normalisationVersion`.
- **After:**
  - `identity-schemas.v3.json#/$defs/normalization-specification-map`.
  - `…/x-opensip-digest-domains/normalizationSpecificationLaw` (`closureTreePath: opensip-interface/normalization/specification-map.v1.json`).
  - Per universe `languageVersionBinding.normalizationClosure`: TypeScript and Rust `toolClosure.closureId` (toolchain), syntax `grammarBundle.closureId` (grammar).
  - `identity-model.v3.py` `admit_normalization_specification`, called from `body_identity_join`.
  - Refusals: `BODY_NORMALIZATION_MAP_MISSING`, `_MAP_INVALID`, `_LEVEL_UNMAPPED`, `_LEVEL_VERSION_MISMATCH`, `_SPECIFICATION_NOT_IN_CLOSURE`; absent bytes remain retention loss.
  - Identity §3 clones bullet.
- **Unchanged:** the registered relation document's bytes; `SyntaxGrammarBundleV1.normalizer.specificationDigest` keeps its native meaning.
- **Fixture:** `evaluator_graph_fixture.v3.py` option `clone_body_fact` (default OFF).
- **Real Runs (syntax universe):** a mapped L0 specification closes. A missing map, an unmapped level, another closure member swapped in, and a specification outside the closure each refuse by name.

### S3 — zero-config syntax-only fallback (corrected)
- **Before:** a marker-free repository produced zero units and an empty, successful default request.
- **After:**
  - `native_evidence_model.v2.py` `SYNTAX_ONLY_FALLBACK_UNIT`, emitted by `discover_units` (no explicit roots, no rust/tsjs unit, root not boundary-excluded).
  - `default_capability_selection([])` refuses `NATIVE_DEFAULT_SELECTION_WITHOUT_UNIT` (internal host invariant).
  - `native-evidence.md` §1.4 **U-9**. Mixed repositories get no fallback: grammar-readable files outside units stay `syntax-only/no-program-unit-for-language` and are not claimed as covered. Explicit roots are unchanged.
  - Native case `units-bare-js-directory-without-a-marker-is-not-a-unit` now expects the fallback unit.
- **Real Run:** a marker-free membership with the fallback closes. The security boundary sweep still holds.

### S4 — account `targetUniverse` (corrected)
- **Before:** a nullable hex that was "deliberately not joined", giving two admissible encodings.
- **After:**
  - `execution-inputs.schema.v1.json#/$defs/NativeCoverageAccountV1/properties/targetUniverse` is `{"type":"null"}`.
  - `…/x-opensip-external-joins/singleCanonicalTargetUniverse`.
  - `execution-inputs-contract.v1.md` §5. The `sourceUniverse` join is unchanged; cross-universe targets stay on Coverage and fact records.
  - Builders now emit `null`: `execution_inputs_fixture.v3.py` and the `check-execution-inputs.v1.py` reference manifest.
  - The maintained control `cross-universe-target-universe-is-not-constrained` (expected ADMIT) becomes `account-target-universe-null-admits-in-a-two-universe-run` (ADMIT) plus `account-target-universe-non-null-refuses` (REFUSE).
- **Real Runs:** closes with null; a hashed ExecutionInputsV1 carrying a non-null value does not close.

### A1 — foundation digest annotations (corrected)
- **Before:** 16 unannotated bare-hex positions in `execution-inputs.schema.v1.json` and 3 in `incoming-search.schema.v1.json`.
- **After:**
  - 15 execution-inputs annotations (S4 removed the 16th) and 3 incoming-search annotations, each with its own representation: `canonical-record`, `h-identity` domain or domain set, `by-domain`, `raw-artifact`.
  - `identity-model.v3.py` `foundation_digest_annotation_coverage` / `admit_foundation_digest_law`, applied in `foreign_payload`, refusing `FOUNDATION_DIGEST_UNANNOTATED:<document>:<position>`.
  - Identity §3 closing-law extension.
- **Real Runs:** closes over the annotated record; refuses when the walked document loses an annotation.

### A2 — v2 references in v3-era documents (corrected)
- **After:**
  - `enumeration-plan.schema.v1.json` `scopeDigest` record `document` → `foundation/identity-schemas.v3.json`, plus three descriptions.
  - `subject-inventory.schema.v1.json` LogicalPath description → v3.
- The registered-document consequence is in §3.

### A4 — `sourceInventory` and read set (corrected)
- **Before:**
  - Undecided which files the inventory contains.
  - U-4a said read bytes "enter the snapshot read set".
  - The registered `ResolvedNodeModulesLayoutV1` description said no inventory row "could exist".
- **After:**
  - Identity §3 **"What `sourceInventory` contains"**: the first-party custody walk plus exactly the bytes actually read from in-project pruned trees under a committed read set.
  - External required inputs (compiler, stdlib, Rust dependency sources) stay in their owning closures and records and are never flattened into snapshot paths.
  - The paragraph also states what bytes-only replay cannot prove.
  - `identity-model.v3.py` `snapshot_pruned_tree_faults` refuses `SNAPSHOT_PRUNED_TREE_NOT_A_READ` in `open_run_closure`. A dependency-tree row must lie under a retained layout `installPath`/`realPath`; VCS and Cargo `target` rows are never reads.
  - Native U-4a sentence.
  - **Registered** `native-evidence.schemas.v2.json#/$defs/ResolvedNodeModulesLayoutV1/description` corrected (dispatch-authorized).
- **Fixture:** the semantic fixture's file extent excludes `host-ignore-convention` rows; existing callers are byte-identical.
- **Real Runs:** a file inside a listed package closes. An unlisted dependency file and a `.git` file each refuse.

### A5 — JavaScript option and universe-flag derivation (merged and completed)
- **Merged:**
  - root's `typescript_mode` change: omitted `allowJs` derives from effective `checkJs`; jsconfig defaults to `true`.
  - root's mode row and law paragraph, as amended by ce3 r2:
    - **C1:** every `jsconfig` graph node supplies `allowJs=true` per file before inheritance; own options win over bases, later `extends` win; then an `allowJs` value wins (including `false`), otherwise it derives from `checkJs`.
    - **C3:** the `ts-tsconfig` row covers a jsconfig entry that writes `false`, with `configOrigin` derived.
    - **C2:** the stale F11 case is renamed `ts-tsconfig-explicit-allowjs-false-excludes-js`, and three cases are added: `tsconfig-checkjs-only-admits-js`, `tsconfig-checkjs-only-without-js-roots`, `jsconfig-explicit-allowjs-false-excludes-js`.
- **My additions:**
  - The flags law states it introduces **no** compiler-option diagnostic refusal, 5052 included. No deficiency, cause or carrier is created, and no owner is claimed to route such a diagnostic (a stated limit).
  - `native/README.md` F11 row selector updated.
  - `native/native-evidence-report.v2.json` regenerated through the checker's own `main()`. Only its pin gate was bypassed, and the report records the real pin faults.
- **Unchanged:** effective values, typed context, schema admission. TypeScript 5.6.3 stays bounded supporting evidence, not a product pin. The 52 compiler observations (root's 32 plus ce3's 20) were not rerun.

## 3. Registration and identity consequences

**Changed registered payload schema documents** (receipt `registered-documents-v2`; the other six are unchanged):

| Document | source38 | corrected |
|---|---|---|
| `foundation/enumeration-plan.schema.v1.json` (A2, M3 keys) | `62ff499e024b83150fee7ce62c449553a3bc2021e0476975f922cdceef806237` | `10627cb6a22a9ff1674c16c5fa4863a58dc86e5df8ac7ae55c45747b0e60197c` |
| `native/native-evidence.schemas.v2.json` (A4 description) | `3e37c7b7a6a620dcadc0aaed862eed242065ebd0ce9910da16faa25464f8b0b0` | `2d37b810bd9ffed741d74241fc8a11051606862d8af2f152eed16b92bdc66043` |

**Identity chains that change for current evaluator3 Runs:**
- **Enumeration-plan bytes:** the `parameters[].schemaDigest` of every analysis-spec carrying EnumerationPlanV1 → `analysisSpecDigest` → `plan2` → every downstream execution-plan, evidence, seal and `run3` id.
- **Native schema bytes:** `payloadSchemaDigest` of every `coverage2` under the native registry and every `view.schemaDigests` → `coverage2`/`view2`/`evidence3`/`seal3`/`run3`.
- **S1:** producer closure trees → `closure2` → Plan `semanticClosures` → Plan and Run.
- **S4:** the account value → ExecutionInputsV1 digest → proof → Run.
- **A5:** checkJs-only configurations now select `js-allowjs` → context, universe and Plan identities for such units.
- **Not identity inputs:** `identity-schemas.v3.json` and the non-registered foundation schemas change closure law, not digests. The M1, M3, S2, S3 and A4 laws change admission and derivation.

**Historical:** frozen source38, `identity-schemas.v2.json`, `identity-model.py` (v2), `check-identity.py` and `integration-fixtures.py` (the v2 lane) are unchanged. Historical exports keep their bytes; nothing is re-read under the new laws.

**Run-termination goldens** (`foundation/run-termination-goldens.v1.json`, now `ac921583…`):
- All 16 pinned ids were remapped by stable scope key from source38 to the corrected source.
- `probes/goldens_rewrite.py` only succeeds when every substituted expectation equals the corrected Run's own derived termination.
- Under v2 identities no carrier-role exchange was needed. v1's single exchange was under v1 identities and is superseded.
- The `run3:000…0` placeholder is untouched.
- The current derived terminations are listed in `review.json#/goldens/currentDerivedTerminations`.
- Checker child commands: `python -I -B docs/coop/design-corrections/foundation/check-semantic-replay.v3.py` (existing) and, **added**, `python -I -B docs/coop/design-corrections/foundation/check-native-consumer24-corrections.v1.py`.

## 4. Changed files

- **vs source38:** 22 modified and 1 added (`foundation/check-native-consumer24-corrections.v1.py`).
  - Manifest with before/after SHA-256 and bytes: `output/changed-files.v1.json`.
  - Full diff: `output/source38-to-corrected.diff` (`5c0fe92b6046da0a51c36a168615eac658db5a05d810e9d5468e8eaced379a9d`).
- **Incremental vs v1:** 9 modified. Manifest `output/v1-to-v2.changed-files.json`; diff `output/v1-to-v2.diff` (`d3cff0318996b8387bd3fc1e109940bb4da54e65e818906534c587f185ad73bb`).
- **New or changed normative and reference files for root pin, kit, launcher and ownership updates:** every path in `changed-files.v1.json`. In particular:
  - normative prose: `identity-and-evidence.md`, `native-evidence.md`, `execution-inputs-contract.v1.md`;
  - schemas: `identity-schemas.v3.json`, `execution-inputs.schema.v1.json`, `incoming-search.schema.v1.json`, `subject-inventory.schema.v1.json`, and the registered `enumeration-plan.schema.v1.json` and `native-evidence.schemas.v2.json`;
  - models: `identity-model.v3.py`, `enumeration_model.v1.py`, `execution_inputs_model.v1.py`, `native_evidence_model.v2.py`;
  - fixtures: `evaluator_graph_fixture.v3.py`, `evaluator_semantic_fixture.v3.py`, `execution_inputs_fixture.v3.py`;
  - reference data: `native-cases.v2.json`, `run-termination-goldens.v1.json`, `native-evidence-report.v2.json`, `native/README.md`;
  - checkers: `check-enumeration.v1.py`, `check-execution-inputs.v1.py`, and the **new** `check-native-consumer24-corrections.v1.py`.

## 5. Checks actually executed

All on the final v2 source, through `run_checks.py v2-final`: 24 jobs, receipts `receipts/<job>-v2-final/` (argv, cwd, exit, stdout/stderr SHA-256, seconds). No check process was left running.

| Job | Exit | Result |
|---|---|---|
| current-profile, atoms, composition, policy-derivation, evaluator-faults, provider-attribution, analysis-seal, comparison-knowledge, workflow-projection, query-projection | 0 | pass |
| enumeration | 0 | 0 mismatches, after the U-4b fixture migration |
| execution-inputs | 0 | 0 mismatches, including the migrated S4 controls |
| full-replay, execution-replay, candidate-replay | 0 | pass |
| semantic-replay | 0 | pass, including all 8 run-termination goldens with the rewritten ids |
| identity (historical v2 lane `check-identity.py`) | 0 | 1596 passed, 0 failed |
| workflows | 0 | 1816/1816 |
| integration (historical v2 lane) | 0 | 412 passed |
| native-cases (`probes/native_cases.py`) | 0 | 380/380 (377 + 3 new A5 cases) |
| native-no-pins (`check_native_evidence.v2.py` `main()`, pin gate only bypassed) | 0 | PASS; 380/380; ladder, syntax-vocabulary, open-object, digest-law and matrix sweeps clean; 21 real pin faults suppressed and reported |
| security-no-pins (security lifecycle cases and sweeps, pin gate only bypassed) | 0 | 464 cases, 0 failed; 11/11 sweeps hold, including the native boundary join with the S3 fallback |
| **security** (`check-security-lifecycle.v1.py`) | **1** | **stops at its source-pin gate** (`sourcePinsValid: false`, 21 changed pinned paths). No case ran under this entry point; the same cases and sweeps pass under security-no-pins. Pins are root's. |
| corrections (`check-native-consumer24-corrections.v1.py`, new) | 0 | 159/159: M1 23, M2 20, M3 21, S1 23, S2 17, S3 12, S4 8, A1 17, A2 6, A4 12 |

**Other v2 receipts, all exit 0:**
- `copy-v1`, `a5-apply-root`, `a5-apply-ce3-r2`;
- `native-no-pins-a5a4` (380/380 before goldens and report);
- `goldens-ids-parent`, `goldens-ids-corrected`, `goldens-rewrite-dryrun`, `goldens-rewrite-apply`;
- `native-report-regenerate` (PASS, 21 pin faults recorded in the report);
- `registered-documents-v2`, `diff-vs-source38`, `diff-v1-to-v2`, `build-review`.

One v2 command was refused by permission (it used `mkdir`; no receipt) and was retried with a Python-created directory.

**v1 failures preserved as receipts** (not rerun as passes):
- `corrections-m2`: the control patched only the outer identity copy.
- `corrections-p3`: two M1 verdict expectations were wrong.
- `corrections-m3s3a4`: a duplicate-row expectation was wrong, a fixture-helper patch never reached the fixture, and the A4 positive hit a fixture extent defect.
- `enumeration-p4-s3m3`: the non-canonical fixture, 18 mismatches.
- `execution-inputs-p2-m2s4a1` and `semantic-replay-p2-m2s4a1`: contaminated by edits made while they ran.
- `goldens-rewrite-dryrun`: an unmapped placeholder id and an unhandled carrier exchange.
- `semantic-replay-p6-all`: stale golden ids.
- `query-projection-p6-all`: no exit record; the v1 run was interrupted.

**Limits of this evidence:**
- Pin ledgers and planning registries were not regenerated. The six global groups, full historical suites and the gated `main()` of the native and security checkers were not run as integration checks.
- The frozen parent was not fully re-hashed; changed-file parents were verified.
- For A5, no TypeScript compiler was run here. It relies on root's 32 and ce3's 20 retained observations.
- S2 real Runs are syntax-universe only.
- The historical v2 lanes pass but are not governed by the new evaluator3 laws.
- All fixtures are synthetic; no product, provider or compiler qualification is claimed.

## 6. Cross-owner needs and limits

- **Root pins and planning (not edited):**
  - `native/source-pins.v2.json`, `foundation/evaluator3-source-pins.v1.json`, `foundation/source-pins.v1.json`, `security/source-pins.v1.json` and `workflows/source-pins.v1.json` still pin changed files. The native report records 21 pin faults.
  - `docs/v2/architecture/implementation-*` registries pin `identity-and-evidence.md`, `native-evidence.md` and `identity-schemas.v3.json`.
  - Root also owns the six global groups and the author-package rebuild.
- **Security S3 "Pruned trees and the read set" (root merges).** Proposed shared text:
  > A pruned tree is never custody-walked. Its files enter the snapshot source inventory only when a Plan-selected context actually read them under a committed read set. Today that means `node_modules` package directories listed by a retained `ResolvedNodeModulesLayoutV1` of a context with `nodeModulesInReadSet`. Such rows are `host-ignore-convention` members joined at Run closure, refusing `SNAPSHOT_PRUNED_TREE_NOT_A_READ`. VCS trees and Cargo build output are never reads. Required inputs outside the project root stay in their owning closures. Which files inside a listed package were read, and that the custody walk was complete, are host TCB observations that bytes-only replay cannot prove.
- **Security discovery agreement (S3):** the fallback unit is not a marker directory, so security's marker-directory unit list does not contain it. The shared boundary sweep still holds; root should record the agreement.
- **A4 granularity:** the read set is package-directory granular. File-level read evidence would need a new native record (not introduced).
- **S2 coverage:** real-Run controls exist only for the syntax universe. No current v3 fixture mints TypeScript or Rust clone bodies. Their toolchain closures must ship the map, and the reference TypeScript/Rust toolchain closures in current fixtures do not yet carry one (no current v3 Run needs it).
- **S1 migration:** any current author-package or root fixture that builds evaluator3 stage specs must register the output schema in its producer closure.
- **A5 limits:**
  - 5052 and option diagnostics have no named routing owner.
  - The model helper has no `extends` input; per-node inheritance is prose plus compiler evidence only.
  - Compiler 5.6.3 is supporting evidence.
- **Goldens:** root merges these native goldens with other authors' `run-termination-goldens` additions.
- **Not claimed:** source full acceptance, readiness, qualification, or product toolchain pins.
