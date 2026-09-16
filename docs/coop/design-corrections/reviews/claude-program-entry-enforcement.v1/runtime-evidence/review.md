# Explicit TS/JS binding with a null `programEntry`: enforcement follow-up (frozen41)

**Author:** bounded AUTHOR f5617310-c7c7-4d85-acdd-31370f220944, following up my own source observation. This is architecture, design and reference work only. It is **a proposal**, not independent acceptance. Nothing was written to LIVE, frozen41, the root successor or old runtimes. No consumer material was used.

**Base.** `candidate-subject.v41`, manifest sha256 `eb7a4c48d86c844914ffc0ef70743752655a411e453bbaa066cfaee572312236`. All 12912 members were verified before and after the work (`receipts/frozen41-verify.json`, `receipts/frozen41-verify-final.json`: 737732367 bytes, 0 missing, 0 mismatched, 0 extra). The relevant sources match the manifest:

| File | sha256 |
|---|---|
| `enumeration_model.v1.py` | `e54741c6…` |
| `enumeration-plan.schema.v1.json` | `10627cb6…` |
| `enumeration-contract.v1.md` | `ae4523a2…` |
| `check-enumeration.v1.py` | `65be4126…` |
| `evaluator_semantic_fixture.v3.py` | `567498c3…` |
| `native-evidence.md` | `66c6b82b…` |
| `native-evidence.schemas.v2.json` | `2d37b810…` |

## Disposition

| Question | Disposition |
|---|---|
| Explicit TS/JS binding with a null `programEntry` | **CORRECTION_REQUIRED**. The published law is unenforced, as measured at admission **and** in a closed Run. |
| Unavailable bindings: path or null | **NO_CHANGE_REQUIRED**. This is retained Plan-selection input, with no contradiction and no missing rule. |
| Explicit Rust `programEntry` path | **NO_CHANGE_REQUIRED**. It is a Plan-provided label; the universe H is the program key. |
| Root's scope correction to my prose | **Correct and necessary.** No further change. |

## 1. The law and what enforces it

- **Law.** `enumeration-plan.schema.v1.json#/$defs/AvailableProgramBindingV1/properties/programEntry.description`: "TS/JS extra program: non-null LogicalPath of the selected inventoried config (snapshot member). U-1 default uses null …". Contract §1 `:22` defines `explicit-plan-selection` as the extra programs the Plan selected.
- **Model** (`enumeration_model.v1.py:797-812`), available bindings:
  - (a) A non-null entry must be a snapshot `LogicalPath`, and a non-null `default-unit` binding refuses.
  - (b) For `TS_MODES`, `expected = programEntry if non-null else _u1_entry(unit)`, compared to the retained `entryConfigPath`.
  - **Nothing checks provenance when the entry is null.** An explicit null binding is refused only incidentally, when the U-1-derived entry differs from the retained graph entry (guard b).

## 2. Measured (owner graphs, controls)

**Admission** (`admit_enumeration` on the maintained `check-enumeration` harness; `receipts/probe-admission-base.json`, `probe-admission-jssyn-base.json`)

| Case (only the named binding fields differ) | frozen41 |
|---|---|
| TS default, null (maintained positive) | ADMIT |
| TS default null + explicit `tsconfig.build.json` (maintained) | ADMIT |
| TS explicit `tsconfig.json`, which names the marker config (semantic-fixture shape) | ADMIT |
| **TS default control with provenance only changed to explicit (null)** | **ADMIT** |
| TS explicit null whose retained graph entry is `tsconfig.build.json` | REFUSE `ENUMERATION_BINDING_PROGRAM_ENTRY` (guard b, incidental) |
| TS default with `tsconfig.json` | REFUSE `ENUMERATION_BINDING_PROGRAM_ENTRY` (guard a) |
| `js-synthesized` default null / explicit null (matching js-synthesized context) | ADMIT / **ADMIT** |
| Rust default null / explicit null / explicit `Cargo.toml` | ADMIT / ADMIT / ADMIT |
| `syntax-only` default null / explicit null / explicit path | ADMIT / ADMIT / ADMIT |
| Unavailable: default null / explicit null / default `tsconfig.json` / explicit `tsconfig.build.json` | ADMIT (all four) |

**Full Run closure** (`receipts/probe-fullrun-base.json`)
- **World.** The maintained TypeScript semantic fixture has no U-1 unit. The probe runs a **variant executed from its own source bytes** with exactly two asserted substitutions:
  1. membership from `N.discover_units` over the snapshot markers, which yields one `ts-tsconfig` unit with `markerPath: "tsconfig.json"`;
  2. the inventory binding's provenance and `programEntry`.
- **Driver.** Everything else is maintained. Runs use the `check-semantic-replay.v3.close_positive` sequence, and Run closure calls `admit_enumeration` (`evaluator_input_model.v3.py:103`).

| World | frozen41 |
|---|---|
| R0 maintained (no unit, explicit `tsconfig.json`) | closes `fail`, exactManifest |
| R1 unit + explicit `tsconfig.json` (non-null control) | closes `fail`, exactManifest |
| R2 unit + default null (default control) | closes `fail`, exactManifest |
| **R3 unit + explicit null (R2 with provenance only changed)** | **closes `fail`, exactManifest** |
| R4 unit + default `tsconfig.json` | `EVALUATOR_ENUMERATION_JOIN:ENUMERATION_BINDING_PROGRAM_ENTRY` |
| R5 no unit + explicit null | `EVALUATOR_ENUMERATION_JOIN:ENUMERATION_BINDING_PROGRAM_ENTRY` (guard b, incidental) |

**Conclusion.** No existing guard rejects an explicit TS/JS binding whose null entry happens to equal the U-1 derivation. That is the exact published law, and it is unenforced.

**Failed attempt (preserved).** My first `js-synthesized` harness world refused `ENUMERATION_BINDING_ENGINE_DOMAIN` for both provenances, because `check-enumeration.admit` hardcodes a `ts-tsconfig` native context. The direct retry with a `js-synthesized` context is what the table reports.

## 3. Proposed correction (smallest; existing refusal key)

`correction.patch` has sha256 `89097b0c257f0dc2df68111a520f3ef969613425b3fc7f6bc45fc341d651817c` (8662 bytes). `delta-manifest.json` lists each file below; both base files are byte-identical to frozen41.

| File | Base sha256 | After sha256 |
|---|---|---|
| `foundation/enumeration_model.v1.py` | `e54741c6ac46904b1c06ccaf71700611f15cd5c354ef5c2c6384e9c65361ab46` | `69b0eee39a45a941d7ab1ef22c0c8be161edd436b1441b27017f98fd1bcffe85` |
| `foundation/check-enumeration.v1.py` | `65be412616ca19d4cc2b6da9486e21e6adc819c811066b9896fb0895da5abea9` | `bdeeb765e9ddbc293f8771af61274ed3da97bd9c1c52085b09611383a6728e41` |

**Model.** On an **available** binding, `elif programEntry is None and provenance == "explicit-plan-selection" and languageMode in TS_MODES` adds `ENUMERATION_BINDING_PROGRAM_ENTRY`. The following are untouched:
- defaults;
- non-null entries;
- Rust and `syntax-only`;
- candidate-only cells (not TS/JS mode);
- unavailable bindings.

The schema, policy and identity recipes are unchanged.

**`js-synthesized`.** The rule covers it because the published text says "TS/JS". Explicit selection names a config, so a synthesized program's single lawful encoding stays the default-unit null binding. No maintained admission-reaching fixture has an explicit `js-synthesized` binding. If owners intend explicit synthesized programs, excluding that one mode is a one-token change, but it would first need owner wording.

**Checker.**
- The `admit()` harness accepts a `native_contexts` override; the default is unchanged.
- 8 focused cases:
  - `available-explicit-ts-null-entry-refused` and `available-explicit-js-synthesized-null-entry-refused` (the discriminators);
  - `available-default-unit-nonnull-entry-refused` (a pre-existing behaviour guard);
  - `available-explicit-ts-names-marker-config-admits`, `available-js-synthesized-default-null-admits`, `available-explicit-rust-null-entry-admits`, `available-explicit-syntax-null-entry-admits` and `unavailable-explicit-null-entry-admits` (preservation).
- An exact-refusal check requires `["ENUMERATION_BINDING_PROGRAM_ENTRY"]` on the three refusals.

**Receipts** (runtime copies, `receipts/copy-trees.json`: 1346 files ×2, 0 mismatches)

| Run | Cases | Mismatches | Receipt sha256 |
|---|---|---|---|
| `check-enumeration` base | 46 | 0 (exit 0) | `b6ae241bee79b3862866ad70ef0d04f06cefa046763fc5145026658218bcb40a` |
| patched | 54 | 0 (exit 0) | `59d5f655e8a032d0b48d2556637bdc21813edc431eb1a5517cb7ead2e067a3cc` |
| controls-only (base model + patched checker) | 54 | 4 (exit 1) | `16a3f0158ac81f8b3c47d19c4183dc5c49826dc49c26e89e5eb71422f7ebc473` |

- **Controls-only failures** are exactly the two null-entry refusals and their exact-refusal checks.
- **Comparison** (`receipts/compare-enumeration.json`): the 46 shared cases are identical between base and patched.
- **Patched full Run** (`probe-fullrun-patched.json`): R3 is now `EVALUATOR_ENUMERATION_JOIN:ENUMERATION_BINDING_PROGRAM_ENTRY`. R0, R1 and R2 still close on the exact manifest; R4 and R5 are unchanged.
- **Patched admission** (`probe-admission-patched.json`): the provenance-only change refuses. Rust, syntax and all unavailable variants still admit.

**Maintained shapes this would make non-admissible, if ever admitted.** Some maintained explicit-null bindings in `ts-tsconfig` cells never call `admit_enumeration`, so they are unaffected at runtime:
- `check-atoms.v1.py:1390-1393`, `:1481-1484`, `:1549-1552`, `:2000-2003`;
- `workflows/check-workflow-projection.v3.py:3045-3047`, which has no mode and is explicitly "NOT claimed here as a full Run".

They are reported, not changed. The other admission-reaching fixtures use default null, or explicit null only in `syntax-only`/candidate cells (`evaluator_graph_fixture.v3.py:120`, `check-execution-inputs.v1.py:1202`).

## 4. The two other open notes

**Unavailable binding `programEntry` (path or null): retained Plan-selection input, NO_CHANGE_REQUIRED.**
- **No comparison is possible.** An unavailable binding has `universe=null` and no retained native entry, so admission can only require a non-null value to be a snapshot path (`enumeration_model.v1.py:817-819`). All four measured variants admit.
- **No consumer reads it.** None of the evaluator, execution-input or native models reads `programEntry`; its only readers are the enumeration model, fixtures and checkers. No join depends on it.
- **The value records a selection.** It says which Plan-selected program is unavailable: an explicit extra program keeps its config path for disclosure.
- **Different values are different Plans.** They produce different `EnumerationPlanV1` bytes, but they are different Plan inputs, not nondeterminism.
- **No owner is violated.** None claims a canonical encoding for unavailable bindings (schema `UnavailableProgramBindingV1.programEntry` has no description; contract §1 `:28` states no value).
- **Not proposed.** Extending the available default-null convention to unavailable defaults would be a new canonicalization rule, and nothing currently requires it.

**Explicit Rust `programEntry` path: Plan label, NO_CHANGE_REQUIRED.**
- **No native input.** `bind_rust_universe` consumes the admitted context, the retained `DependencySourceSetV1`/`UnifiedFeaturesV1`/`PreparedOutputSetV3` and the snapshot inventory, but no `programEntry` (`native-evidence.md:1268-1277`).
- **The universe H is the key.** The schema says "Rust extra programs are distinct universe H values … programEntry is not a complete program key", and contract §9 agrees. Duplicate universe H in a cell refuses (`ENUMERATION_BINDING_DUPLICATE_UNIVERSE`), which distinguishes programs.
- **Only existing constraint.** A non-null path must be a snapshot `LogicalPath` (model `:799-800`). Default null, explicit null and explicit `Cargo.toml` all admit.
- **No missing rule.** No join or deterministic construction depends on the value.
- **Prose note only.** Contract §1 `:24` ("Universe **must** be the native owner admission of … this `programEntry` … (`bind_rust_universe` / `bind_syntax_universe`)") overstates `programEntry` as a Rust/syntax bind input. That is imprecision, not a contradiction that changes behaviour, and it is outside this bounded fix.

## 5. Root's scope correction

The replacement of "It never copies the U-1 marker …" with "**For an available default-unit binding,** it never copies …" is correct and necessary.
- **Lawful explicit selection names the marker.** Explicit selection that names the marker config is a maintained lawful shape: `evaluator_semantic_fixture.v3.py:397-399` (R0 closes), `check-atoms.v1.py:477-479`, and the admitted probe case `TS-explicit-selects-marker-config-nonnull`. The unscoped sentence would contradict them.
- **The scoped sentence matches the enforced rule exactly:** available `default-unit` with non-null refuses. It does not reach unavailable bindings, consistent with §4.

No further wording change is proposed.

## 6. Limitations

- **Standing.** Admission results are the enumeration owner join. Closed-Run results use the maintained semantic sequence on a **probe variant** of the semantic fixture: executed from its own bytes, no file written, and the two substitutions asserted.
- **Fixture defect not corrected.** The file fixture's own membership has no TS unit.
- **Not run:** broad suites, pins, planning, `check-atoms`, workflow checks, or other Run checkers. The claim that no other maintained admission-reaching fixture uses an explicit TS/JS null rests on source search, not execution.
- **Integration.** Owned hashes of the two files change, and any pin update belongs to root integration.
- **Not read:** anything under `reviews/` beyond the formal manifest file.
