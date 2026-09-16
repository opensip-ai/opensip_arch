# Author package migration to native-v2 laws (author-package-migration.v1)

Coauthor origin 823bf66b-e92a-4789-ab81-63a1a9dc371d. Runtime `R=/private/tmp/opensip-design-corrections/claude-author-package-migration.v1`.

**What this is:** provisional AUTHOR-constructor migration evidence, built against a **captured copy** of the mutable successor.
**What this is not:**
- independent review, blind work or acceptance
- frozen-candidate39 acceptance
- a whole-source review
- product implementation

It passes owner replay, but only as author-derived self-consistency. It is not an independent implementation. It makes no aggregate acceptance or readiness claim. I made no commits, pushes, live edits, source-law changes, global pins or grades, and I did not read the blind consumer.

The machine record is `R/review.json` (sha256 `19624c5dc84e0b52b5935b1f035d95900deb631551fa8131f11964bd6eb5bcfb`). `build_review.py` assembled it from the custody files, manifests, reports and receipts. It refuses unless the final rebuild, all 7 group outcomes and the probe passed.

## 1. Input custody

### Captured source
- **Command:** `capture_source.py`, receipt `receipts/capture-source` (exit 0). Record: `custody/captured-source.json`.
- **Input:** `/tmp/opensip-design-corrections/consumer24-corrections-successor.v1/source`, copied as regular files without `__pycache__` to `R/source`.
- **Size:** 12905 files, 737307500 bytes.
- **Checks:** hashed in two passes. Input drift during capture: none. Copy faults: none.
- **Hashes:**
  - `capturedFileListSha256` `e9cb76d52bdf2498d2921d3c02ed14157c9b3f50f25e557e1e7c1731f00c2e20`
  - package-format source manifest (`{"files":[…]}`, indent 1) sha256 `8a942a832b914046122a73e1c5ddc43c877a8c4962fa4272e2c6a769b6293688`. This is pinned into the new `verify-package.py`.
- **Source38 provenance:** compared with the source38 manifest, 33 files are modified and 1 is added (`check-native-consumer24-corrections.v1.py`); none are missing. The exact lists are in `custody/captured-source.json` → `source38`.
  - Workflows: the only change is the prose in `docs/.../workflows-and-surfaces.md`. No workflows code changed.
- **Registered documents in the capture:**
  - native schema `2d37b810bd9ffed741d74241fc8a11051606862d8af2f152eed16b92bdc66043`
  - enumeration-plan schema `10627cb6a22a9ff1674c16c5fa4863a58dc86e5df8ac7ae55c45747b0e60197c`
- **Rechecked at end of task** (`custody/end-of-task-recheck.json`, inline python, no receipt): all 12905 captured files still match, with no unlisted files. The source manifest sha is also identical across attempts 1, 2 and 3.

### Package15
- **Command:** `copy_package.py`, receipt `receipts/copy-package15` (exit 0). Record: `custody/package15-copy.json`.
- **Result:** `artifact-manifest.json` sha256 matched `6a8d4feca9db7ea48e91debf3a080415f769ac7271b8bf67df145263148b701e`. All 335 listed files verified, with no unlisted files. The copy is at `R/package15`.
- **Rechecked at end of task:** the original `/tmp/.../claude-author-package-successor.v15` and `R/package15` both still verify (335/335, no unlisted files). No prior tree, package or export byte was changed.

## 2. Baseline: package15 against the captured source

Script `baseline.py`; receipts `receipts/baseline-*`; summary `work/baseline-summary.json`.

- **Old exports (historical, not repaired):**
  - All 13 fail owner admission (exit 1) with `PAYLOAD_SCHEMA_NOT_THE_REGISTERED_DOCUMENT:native/native-evidence.schemas.v2.json`.
  - This is expected: the registered native schema changed.
- **Old constructors:**
  - `build-checkpoint3.py` and `build-binding-controls.py` construct (exit 0; construction only).
  - `build-normalized-examples6.py` and `build-rust-selection-examples.py` exit 0, but every case is refused:
    - `rust`, `syntax-code`, `rust-bin`, `rust-lib-only`: `BODY_NORMALIZATION_MAP_MISSING`
    - `rust-partial`, `syntax-data`: `STAGE_OUTPUT_SCHEMA_UNREGISTERED:…author-synthetic-analysis`
  - This confirms root's finding: the finalizer's stage spec pointed at `builder.NAT_DIGEST`, and no producer-interface member was registered for it.

## 3. Migration overlay: changed and new constructors

- **Overlay:** `R/overlay/`, an exact overlay on package15.
- **Manifest:** `R/overlay/overlay-manifest.json`, sha256 `07c3185f0fca2d191fda26e584293b409ca43a9f081ad620e906388f5e36e7a1`. It records the package15 base digest of every file. `rebuild-author-package.v2.py` refuses if a base digest does not match.
- **Diff:** `R/output/overlay/overlay-vs-package15.diff` (1196 lines, content sha256 `4617b3d9936a1dfa2c82c09fd3e1c870f3540e31ad3bfa757a7eac4a0dabfdf8`).

| path | status | package15 sha256 → new sha256 |
|---|---|---|
| author-helpers/native_v2.py | added | — → 0a12dc1c… |
| author-helpers/runs.py | modified | 638626cc… → ac2b983b… |
| author-helpers/ts_pilot.py | modified | 7801111a… → 3074b4d3… |
| build-normalized-examples6.py | modified | 7b7a0b74… → e95ad50a… |
| build-rust-selection-examples.py | modified | 5cfda59c… → 4ed2766f… |
| build-normalization-map-controls.py | added | — → 65bea825… |
| probe-native-v2.py | added | — → 5ec5496d… |
| rebuild-author-package.v2.py | added | — → 53f75a07… |
| verify-package.py | modified | f278f5cb… → ef69c72c… |
| README.md | modified | 16785ba6… → 205f7aad… |
| author-delivery-commands.md | modified | c35592fb… → 8dd61e0f… |

The overlay manifest holds the full digests.

### What each law change does

**S1: stage output registration**
- `native_v2.stage_output_member(operation, domains)` emits `opensip-interface/stage-output/<operation>.schema.json`. It is a canonical JSON Schema 2020-12 document carrying `x-opensip-stage-output {schemaVersion 1, operation, outputDomains}`. The treePath and operation segment come from the kit's identity-schemas.v3 registeredBy law.
- `runs.make_provider_closure(..., stage_outputs)` adds these members to the provider closure.
- Stage specs use `native_v2.stage_output_schema_digest(operation, domains)`, which replaces the unregistered `builder.NAT_DIGEST`:
  - Rust, rust-partial and syntax helper Runs register `analyze` with `[coverage, fact, view]`.
  - `ts_pilot` registers `analyze` with `[view]`.
- The normalized and Rust-selection finalizers relabel their stage as `author-synthetic-analysis`/`[view]`. They register it through `runs.EXTRA_STAGE_OUTPUTS`, so the operation, schema and producer closure agree.

**S2: per-level normalization maps**
- These live in the actual interpreting closures:
  - **TS toolchain closure** (`ts_pilot`): specs L0-verbatim and L1-lexical plus `opensip-interface/normalization/specification-map.v1.json`.
  - **Rust toolchain closure** (`build_rust_run`): L0-verbatim plus the map.
  - **Syntax grammar closure** (`make_grammar_closure(level_specs=…)`): L0-verbatim plus the map for `syntax-code`. `syntax-data` has no clone fact, so its grammar closure carries no map.
- The spec bytes are the level-spec bytes that the clone facts already cite, so body identity is unchanged by intent.
- `ts_pilot.NORMALIZATION_CONTROL` is a hook for bounded negatives; it is `None` in every positive.

**S4:** every `NativeCoverageAccountV1.targetUniverse` is `null` (`runs._empty_ei`, `ts_pilot`).

**U-4b (U-9) membership:** `native_v2.membership(units, paths)` implements the source law:
- units sorted by `(rootPath, family)`, with ordinal = index
- first-match row decision: pruned → host-ignore; family none → grammar-only by bundled extension, else unsupported; no unit → no-program-unit-for-language; otherwise the deepest unit
- `unsupportedFiles` is the row-order projection
- the syntax-only fallback unit is `{rootPath "", none, syntax-only, markerPath "", markerSha256 null, syntax-only-fallback, DEFAULTED}`

It is used by the Rust workspace, Rust package, syntax and TS Runs.

**Native and enumeration schema hash changes:** the helpers read registered bytes from `OPENSIP_AUTHOR_KIT` (= `--source`). Identities are therefore reconstructed from the captured law through the constructors; no identity value is hand-set.

### AUTHOR REPAIR (the only helper/constructor repair beyond law migration)

**Scope:** `build-normalized-examples6.py` and `build-rust-selection-examples.py`. The same one-line repair is in each, recorded in their docstrings and in the diff (overlay diff lines 482–484 and 688–690):

```
+ # AUTHOR REPAIR (author-package-migration.v1): parameters is x-opensip-order canonical-set and the payloadDigest
+ # rewrites above can reorder it; package15 was canonical only because its old digests happened to sort that way.
+ spec['parameters']=order.cset(spec['parameters'])
```

**Evidence:**
- Attempt 1 (`runs/attempt1`, receipt `receipts/rebuild-attempt1`, exit 1; retained) failed to construct `normalized-examples6:rust` and `normalized-examples6:syntax-code`. The error was the owner schema check `array order canonical-set: strict unique order required` on `parameters`.
- This is a latent constructor ordering defect, not a law contradiction. No validator, expectation or verdict was changed.

## 4. Orchestration and receipts

**Command** (portable; no fixed historic `/tmp` inputs):

```
PY=/tmp/opensip-architecture-review-env/bin/python
$PY -I -B $OVERLAY/rebuild-author-package.v2.py --source $SRC --package $PKG15 \
    --package-manifest-sha256 6a8d4feca9db7ea48e91debf3a080415f769ac7271b8bf67df145263148b701e \
    --overlay $OVERLAY --out $OUT [--source-manifest <frozen {"files":[…]} JSON>]
```

**What it does, in order:**
1. Verifies package15 and every overlay base digest, then hashes `--source`. If `--source-manifest` is given, it refuses unless `--source` equals it.
2. Constructs `OUT/work/constructors` from package15 plus the overlay.
3. Runs 6 constructors into `OUT/work/build`.
4. Assembles `OUT/package`:
   - package15 exports and the files bound to source38 move to `historical-source38-before-native-v2/`, byte for byte;
   - writes `source-manifest.json` and pins its sha into `verify-package.py`;
   - writes `predecessor-artifact-manifest.json` and `artifact-manifest.json`.
5. Runs `verify-package.py` (owner `open_run_closure` plus full `close_run` for every Run, and the 7 query checks) and `probe-native-v2.py`.
6. Writes `OUT/rebuild-report.json`, including export id comparisons.

**Runs:**

| attempt | location | receipt | result |
|---|---|---|---|
| 1 | `runs/attempt1` | `receipts/rebuild-attempt1` | exit 1; construction failure above; retained |
| 2 | `runs/attempt2` | `receipts/rebuild-attempt2` | exit 0; built before the delivery-commands doc joined the overlay |
| 3 (final) | `runs/attempt3-portable/from-another-cwd` | `receipts/rebuild-attempt3-portable` | exit 0 |

Attempt 3 ran with `cwd=/tmp`. Its inputs were `R/source`, `R/package15` and `R/overlay`. Its child receipts are in `OUT/work/receipts`:

| child | exit | seconds |
|---|---|---|
| construct-checkpoint3 | 0 | 1.8 |
| construct-normalized | 0 | 4.8 |
| construct-rust-selection | 0 | 4.3 |
| construct-binding-controls | 0 | 5.1 |
| construct-normalization-map-controls | 0 | 6.7 |
| construct-semantic-controls | 0 | 0.1 |
| verify-package | 0 | 46.5 |
| probe-native-v2-membership | 0 | 8.6 |

**Other receipts, all in `R/receipts/`, all exit 0:**
- `overlay-manifest{,.2,.3}`
- `attempt2-author-properties`, `attempt2-mixed-universe-view`
- `final-author-properties`, `final-mixed-universe-view`
- `package-diff`, `compare-attempt2-attempt3`, `build-review-json`

Every receipt holds `command.json`, stdout, stderr, the exit code and digests. No compiler downloads ran, and the full six groups were not rerun. No background children are live.

**Determinism and portability:** attempt 2 (runtime cwd) and attempt 3 (`/tmp` cwd) were compared in `output/attempt2-vs-attempt3.json`.
- All 127 export, claims and variants files are byte-identical.
- The only differing files are:
  - the 6 `construction-provenance.json` files, which differ only in absolute `--package`/`--out` paths (checked by diff);
  - `artifact-manifest.json`;
  - `overlay-manifest.json` and `author-delivery-commands.md`, which were added to the overlay after attempt 2.

## 5. Output package

- **Package:** `R/runs/attempt3-portable/from-another-cwd/package`
- **Manifest:** `artifact-manifest.json` sha256 **`b2fca539d71ed03dcb0ebdefe237a954e0bb1cac0b532c1c7d65358b0a0dee45`**. 382 listed files, all rechecked at end of task.
- **Source pin:** `8a942a83…` (the captured source, which is provisional).
- **Predecessor:** `6a8d4fec…`
- **Diff vs package15:** `R/output/package-vs-package15.{json,diff}` (diff sha256 `85ce637f…`).
  - 37 modified, 14 added, 288 unchanged.
  - 11 package15 paths moved byte-identically into `historical-source38-before-native-v2/`, plus 44 historical copies of package15 files.
  - No package15 file was removed without a historical copy.

## 6. Structural and semantic results on the captured source

All results come from `verify-package.py` inside attempt 3. Owner = owner `open_run_closure`; semantic = full `close_run` replay.

| group | Run | owner | semantic | reason |
|---|---|---|---|---|
| checkpoint3 | author-ts | ADMIT | ADMIT | |
| normalized-examples6 | rust / rust-partial / syntax-code / syntax-data | ADMIT | ADMIT | |
| rust-selection-examples1 | rust-bin / rust-lib-only | ADMIT | ADMIT | |
| semantic-controls1 | severity / unrelated-scope / collapsed-deficiencies | ADMIT | REFUSE | EVALUATOR_COMPLETE_PROOF_REPLAY |
| binding-controls | ts-lawful-default | ADMIT | ADMIT | |
| binding-controls | ts-invalid-default-entry | ADMIT | REFUSE | EVALUATOR_ENUMERATION_JOIN:ENUMERATION_BINDING_PROGRAM_ENTRY |
| binding-controls | ts-lawful-explicit-selection | ADMIT | ADMIT | |
| normalization-map-controls1 (new) | ts-map-absent | REFUSE | NOT-REACHED | BODY_NORMALIZATION_MAP_MISSING:opensip-interface/normalization/specification-map.v1.json |
| normalization-map-controls1 (new) | ts-map-level-unmapped | REFUSE | NOT-REACHED | BODY_NORMALIZATION_LEVEL_UNMAPPED:L0-verbatim |
| normalization-map-controls1 (new) | ts-map-level-swapped | REFUSE | NOT-REACHED | BODY_NORMALIZATION_LEVEL_VERSION_MISMATCH:L0-verbatim |
| normalization-map-controls1 (new) | ts-spec-outside-closure | REFUSE | NOT-REACHED | BODY_NORMALIZATION_SPECIFICATION_NOT_IN_CLOSURE:L0-verbatim |

**Coverage of the requested cases:**
- **Seven positives:** reach full `close_run` ADMIT.
- **Three semantic negatives:** pass structural admission and are refused at complete proof replay, which is their intended boundary. Their constructor still asserts 2 execution deficiencies.
- **Three binding controls:** the lawful default and explicit selection admit, and the invalid default entry is refused at the enumeration join (intended boundary).
- **New map controls:** each is a real Run with a real store. It is built through the same `ts_pilot` path as the positive and changes only the S2 control. The owner refuses it structurally at its intended S2 token, so `close_run` is correctly not reached. For each of the 4 controls, `verify-package.py` requires owner REFUSE, semantic NOT-REACHED, and a reason containing that variant's `expectedStructuralBoundary` token from `variants.json`.

**Mapped-clone positives** (from `probe-native-v2.py` over owner functions, 9 Runs, no faults):

| Run | stages | clones | closure | levels |
|---|---|---|---|---|
| author-ts, ts-lawful-default, ts-lawful-explicit-selection | `analyze` registered | 2 each | TS toolchain `closure2:a298b8e7…` | L1-lexical and L0-verbatim; map member present and level mapped |
| rust, rust-bin, rust-lib-only | `author-synthetic-analysis` registered | 1 each | Rust toolchain `closure2:c2cbdf8a…` | L0-verbatim; mapped |
| syntax-code | `author-synthetic-analysis` registered | 1 | grammar `closure2:3c89fb9b…` | L0-verbatim; mapped |
| rust-partial, syntax-data | `author-synthetic-analysis` registered | none | — | map law not exercised by these Runs |

- Every positive calls full `close_run` (table above).
- The probe's account check confirms `targetUniverse` is null.
- U-4b: owner `assign_membership` and `discover_units` both agree with the author rows and units for all 9 Runs:
  - Rust: `unsupportedFiles ["Cargo.lock"]`; workspace member roots `crates/alpha` and `crates/foo#bar`.
  - Syntax: the DEFAULTED fallback unit.
  - TS: the `typescript-config` unit.

**Historical property probes rerun on the final package** (`work/probes-final`, identical to the attempt 2 outputs):
- `check-author-properties.py` passes its 6 checks: the edition map, literal `#` marker, body identity versus edition, universe versus selection, 32-byte version, and the partial-ownership indeterminate verdict.
- `probe-mixed-universe-view.py`: unmerged is ADMIT/ADMIT. Merged is structural ADMIT but capture REFUSE `EXECUTION_INPUTS_COVERAGE_DERIVE` and semantic REFUSE `EVALUATOR_EXECUTION_INPUTS_JOIN:EXECUTION_INPUTS_COVERAGE_DERIVE`. This matches package15's historical outcome.

## 7. Query checks and pending workflow law

- The existing 7 query checks (`check-author-query.py` plus assessment, over the admitted checkpoint3 TS Run) all pass with unchanged expectations. Report sha256 `3f959d32…`.
- They load `workflows/check-query-projection.v3.py` from `--source`. The capture contains no workflows code changes versus source38, so these results reflect the **pre-workflow-v2** query projection.
- The workflow-v2 author's pending law, including any query output schema change, is **not** in this capture. Its effect is unmeasured here, and root must replay these checks after the frozen successor lands. I did not weaken or pre-adapt any expectation.

## 8. New export id comparison (package15 → migrated; `runId` prefix)

| group/Run | package15 | migrated |
|---|---|---|
| checkpoint3/author-ts (= binding ts-lawful-default) | run3:0f6b13af01a… | run3:52cae22644b… |
| normalized/rust | run3:c4f8a8e1976… | run3:1a22aedd948… |
| normalized/rust-partial | run3:40a7b9d2139… | run3:8c135158ac2… |
| normalized/syntax-code | run3:c4ee12b72f9… | run3:e9aed8ce5dd… |
| normalized/syntax-data | run3:3d1a55647b8… | run3:b193caaf82b… |
| selection/rust-bin | run3:59dfa404ec2… | run3:d5e396e6d99… |
| selection/rust-lib-only | run3:56f9b1dd402… | run3:436519cef5d… |
| semantic/severity | run3:803bfad36ec… | run3:51e0318f0e9… |
| semantic/unrelated-scope | run3:4021c30a1e4… | run3:b5b86d6fd41… |
| semantic/collapsed-deficiencies | run3:d785ab9b2b6… | run3:67947edc8cc… |
| binding/ts-invalid-default-entry | run3:9f433416524… | run3:5dced4e0aef… |
| binding/ts-lawful-explicit-selection | run3:80c4ab7d482… | run3:2e2e33c2abe… |
| map/ts-map-absent (new) | — | run3:b009ae65bf2… |
| map/ts-map-level-unmapped (new) | — | run3:e69a549c8fd… |
| map/ts-map-level-swapped (new) | — | run3:111b6787faf… |
| map/ts-spec-outside-closure (new) | — | run3:28f72aa09e7… |

`rebuild-report.json` → `exportComparison` and `review.json` hold the full runIds and export sha256s.

- **Why every id changed:** the registered schema digests, closure members, stage digests, account targets and membership rows are all lawful identity inputs.
- **The package15 = binding-control default equality is preserved:** checkpoint3 `author-ts` still equals `ts-lawful-default`.

## 9. Unexercised boundaries and limits (explicit, not success claims)

**Unexercised or limited boundaries:**
- **S2 negatives cover the TS toolchain closure only.** There are no Rust-toolchain or syntax-grammar map negatives under actual Runs. The owner code path is shared, but that is not exercised here.
- **No S1 negatives under actual Runs in this package:** no unregistered operation, declaration mismatch or invalid document. The baseline shows `STAGE_OUTPUT_SCHEMA_UNREGISTERED` reached only incidentally, on old constructors.
- **No U-4b negative Run.** Examples would be misordered units, a wrong deepest unit or a wrong `unsupportedFiles` projection. Membership agreement is checked positively, against the owner functions.
- **S4:** only the null target is exercised; there is no non-null negative.
- **Partial helper scope stays limited:** exists/none only. and/or/not are unexercised; count-at-most and all-covered are unimplemented.
- **Two-binding qualification** remains incomplete.
- **All 30 independent grades** remain PENDING.

**Scope and standing limits:**
- **Historical preparation files stay bound to source38 and are not rebound.** Examples are `evaluation-residual-author-assessment.json` and `source-binding.v*.json`.
- **Not frozen-candidate39 acceptance.** The captured source is a mutable integration snapshot, and the package's source pin binds only that capture.
- **No blind output was repaired or imported.** No old export bytes were repaired; they remain historical and refused under the new law.
- **No concrete law contradiction was found.** The one construction failure was the author ordering defect in §3.

## 10. Root final-freeze integration instructions

1. **Freeze the successor** after all merges, including host/recovery-v2, workflow-v2 and any later root changes. Produce its `{"files":[{path,sha256,bytes}]}` manifest.
2. **Rebuild from inputs.** Do not re-pin this package.
   - Take package15 (manifest `6a8d4fec…`) and this overlay (`R/overlay`, manifest `07c3185f…`). Copy both if `/tmp` retention is uncertain.
   - Run `rebuild-author-package.v2.py --source <FROZEN> --source-manifest <FROZEN manifest> --package <package15> --package-manifest-sha256 6a8d4fec… --overlay <overlay> --out <fresh>`.
   - It refuses on any base-digest or source mismatch.
3. **Require from the rebuild:**
   - `rebuild-report.json` `passed: true`;
   - the §6 outcomes, with the same reason tokens;
   - probe `passed` with no units-vs-discovery disagreement.
4. **Compare export ids** with §8 / `review.json`:
   - Identical ids mean the frozen law bytes that feed these Runs match the capture.
   - Different ids are expected if the registered native, enumeration, identity or stage/normalization law bytes changed. Record the new ids; do not reuse these.
5. **On any refusal:** retain the attempt and classify it as either an author-constructor limitation (repair only in AUTHOR helpers, with the exact diff) or a law contradiction (report it; do not change the law to fit). Never adjust verifier expectations to pass.
6. **Replay the 7 query checks on the frozen source containing workflow-v2.** If the query output schema changed, the author query checks and assessment need a root-directed replay or migration; this capture did not measure it.
7. **Root-owned follow-ups:**
   - Rebind the source38-bound preparation files: assessment, source-binding and pins.
   - Record the frozen package manifest.
   - Keep the §9 limits and PENDING grades.
8. **Custody:** never supply this package, overlay or its outputs to a blind consumer.
