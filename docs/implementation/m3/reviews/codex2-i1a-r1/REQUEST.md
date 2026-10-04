CODEX2 review: unit **I1-a** r1 of law M3-I1 r2 — the schemas, pins and generated enums for the `cycle-representative` atom — with its contract-successor record. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT-UNIT** for the product change, with an **ACCEPT-DESIGN-UNIT** assessment of the contract-successor record. There is **no inventory successor**, so no `inventoryCandidateAssessment` (judgment call 1).

**Rules:**
- No repository edits, commits, pushes or delegation.
- Write only under `/tmp/opensip-implementation/reviews/codex2-i1a-r1`.
- You own the native lane for this review:
  - Use a `CARGO_TARGET_DIR` under that directory.
  - Use a private 0700 `TMPDIR` under `$(getconf DARWIN_USER_TEMP_DIR)`, because other worktrees churn the shared temp folder.
  - Run cargo `--locked --offline`.
  - Write every scratch output (generation and drift directories) under your output directory, never into either repository.
- **The generator is shared with X4T-c (P5-3).** Before running `run_generation_i1a.py` or `drift_scratch_i1a.py`, check that no other `opensip-contract-generator` or `generate_contracts.py` process is running.
- Run git read-only, and only against the worktree named below.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.
- No crash-matrix lead run set is needed or wanted (see "Pins checked", X9). Before the crash-matrix feature lane, check that no other cargo test or matrix process is running.

## Inputs

All inputs are pinned in `hashes.txt`. Laws and plans are pinned by their accepted snapshots.

### Law and design parent

- **The law:** `docs/implementation/m3/preview-pack-i1/PROPOSAL-r2.md` (`1eb47d1e…`, your r2 ACCEPT). Item 4 (:264-285), its table at :268-277 and its last line: "The product copies (… `policy-v2.schema.json:296-303`; `identity-v3.schema.json:1221-1231`, `:2781-2791` and the `majorLaw` at `:4984`), their registry pins and the generated enums change in unit I1-a" (:285). Units and order: :431-445. LD-11 (:427): evaluation refuses the op structurally until I1-b2.
- **The unit row:** `UNITS-r2.md` (`0c3c0f44…`), row I1-a and the edges I1-L → I1-a → I1-b1 → I1-c.
- **The design parent, I1-L** (your ACCEPT-DESIGN-UNIT in `reviews/codex2-i1-l-r1/`; bound at product main). `i1-l/README.md`'s section "For I1-a" lists what `verify_design` will require: the source maps re-pointed to I1-L's copies, a 468a-form record carrying a new admission-registry architecture copy, and the atom registry's `fieldFilterSchema` pin moving path. `i1-l/materialization-map.json` gives the two product copies byte for byte.
- **Precedents:** 468a (`m2/existing-root-diagnostics-468a/README.md`, a contract successor that carries its product materialization and a new admission-registry copy); F8b (`m2/generator-closure-f8b/README.md`, rebuild-02 and the staged binding); P0's request (`m3/reviews/codex-p0-scaffolds-r1/REQUEST.md`, the staged-lock lanes); 458b (`m2/reviews/grok-profile-set-v2-458b-r1/review-contract.json`, one unit with a separate contract review file).

### Product

- **Worktree:** `/Users/sb/code/opensip-ai/opensip-i1a`, detached at main `5e25d04` (P0 integrated: 87 contract successors, 95 inventory successors, v135 selected). Nothing is committed and no file is added.
- **Diff:** `git diff 5e25d04` is 3,612,849 bytes, sha256 `fa7f4fda73b3eb213da91921ca868f3fa4feaf5e75c72f982704ebb849bd36c4`. It covers 16 files, +215 −63, of which the staged `design-lock.json` is +22. Its size is `report.ts`'s single-line embedded schema table.
- **Provisioned trees:** the worktree also holds the ignored `tools/contracts/node_modules` and `tools/contracts/python-packages`, copied from the main checkout. The generator checks all their closure pins.
- **Toolchain:** `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin`; Python `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14`; generator `~/opensip-deps/contracts-generator-rebuild-02/opensip-contract-generator` (7202304 B, `4647471c…`, the selected pin); Node `~/.nvm/versions/node/v24.16.0/bin/node`.

### The record (arch, untracked)

- **Subject manifest:** `docs/implementation/m3/preview-pack-i1/i1-a-subject.json`, 5591 bytes, sha256 `3c89d7da193e25d5c8c6dcb8a5410b2d2be4fe0b6133402349e55b14e2fd7bcf`. It holds 26 members: 25 candidates and the record.
- **Record:** `docs/implementation/m3/preview-pack-i1/i1-a/successor.json`, 8748 bytes, sha256 `7d6c04e9914809409e01027e63d7b9cde670c6e8757538a13b743b9d0af5a03d`. It has 12 parents, no passage overrides and no supersessions.
- **Candidates:** `README.md` (the unit's own account), `materialization-map.json`, `schemas/admission-registry.json` (the architecture copy the admission map now names), 13 `product/` copies, and `evidence/` (six scripts and three reports).
- **Not in the subject:** `i1-a-unit.json`, a DRAFT-PENDING-REVIEW record the lead completes at integration.

## What I1-a changes

| Product file | Before | After | Change |
|---|---|---|---|
| `schemas/sources/identity-v3.schema.json` | 197480, `311c1feb…` | 198423, `eb6ec957…` | I1-L's product copy, byte for byte |
| `schemas/sources/policy-v2.schema.json` | 26534, `b221b5ed…` | 26677, `0ff24ae6…` | I1-L's product copy, byte for byte |
| `schemas/source-map.json` | 28547, `6796d7ec…` | 28565, `76409db5…` | both rows' `architectureSource` → I1-L's copies |
| `schemas/admission-source-map.json` | 20049, `9ed543dd…` | 20057, `fcd0f34e…` | the same two rows; `registryArchitectureSource` → `i1-a/schemas/admission-registry.json` |
| `schemas/admission-registry.json` | 17170, `595fc28d…` | 17170, `15457b75…` | two source rows and the policy-v2 alias row |
| `schemas/registry.json` | 20211, `eecde992…` | 20211, `ca65e1b2…` | two `sourceSha256`, the sorted recipe `sourceSha256s`, `generatorClosureSha256` |
| `tools/contracts/generator-closure.json` | 68280, `bb093a9c…` | 68280, `9dc40660…` | 3 of 349 rows: `schemas/source-map.json` and the two sources |
| `crates/identity/src/schema_registry.rs` | 26806, `82ae11b3…` | 26808, `ea3cc09e…` | both `SourcePin` lengths and digests (`:161`, `:188`) |
| `crates/evaluator/src/atom-registry.json` | 30466, `8f37ed00…` | 30488, `9aabc999…` | `fieldFilterSchema` → I1-L's design copy (path, bytes, sha256); `scannerIdentitySchema` bytes and sha256 |
| `crates/contracts/src/generated/identity.rs` | 283889, `af42ad22…` | 284396, `ee275003…` | regenerated |
| `crates/contracts/src/generated/evidence.rs` | 1570438, `9fcce094…` | 1570759, `510cbc79…` | regenerated |
| `apps/report/src/generated/report.ts` | 2167115, `90d643db…` | 2168287, `dfe3001e…` | regenerated |
| `tools/contracts/dependency-policy.json` | 5199, `353c2af7…` | 5199, `f283f3a1…` | the generated `evidence.rs` and `identity.rs` rows |
| `tools/identity/dependency-policy.json` | 56471, `ae739105…` | 56471, `03deeac6…` | the `src/schema_registry.rs` row |
| `crates/host/src/schema_sources.rs` | 52054, `4c0f2d36…` | 57322, `6181bcd5…` | one new test |
| `design-lock.json` | 501382, `9afddcbe…` | 502181, `c376f76e…` | staged: the I1-a `contractSuccessors` entry (outside the map) |

**The schema bytes.** I1-L's edits only: `cycle-representative` appended last to policy `Atom.op` (now `:296-304`), to the identity `predicateProofs[].operation` enum (`:1221-1232`) and to `program-predicate.operation` (`:2782-2793`); the r2 `majorLaw` sentence (`:4986`); the policy `description` (line 5); and the two lock-bound PIDS overrides I1-L's copy carries (predicate-matching-v2's `program-predicate` description, stage-meta's registration `law`). These are the line references I1-L's README predicted.

**Generated outputs** (rebuild-02, through `run_generation_i1a.py`):
- `Policy2AtomOp`, `Identity3ProgramPredicateOperation` and `Identity3ProofBundlePredicateProofsItemOperation` each gain `CycleRepresentative` with its `Display` and `FromStr` arms.
- Two doc comments follow the schema descriptions: `Policy2Root` and `Identity3ProgramPredicate`.
- `report.ts`: the member in three unions, the embedded schema bytes, and the two provenance header lines (registry and closure digests).
- The other five outputs are byte-identical.

**The test** (`schema_sources.rs`, `cycle_representative_is_admitted_by_current_policy_and_identity_schemas_only`):
- The member is admitted through policy-document:2 `/$defs/Atom`, identity:v3 `/$defs/program-predicate` and `/$defs/proof-bundle`, and the three generated enums.
- It is refused through policy-document:1 `/$defs/Atom` and `Policy1AtomOp`.
- Four near spellings (`cycle_representative`, `Cycle-Representative`, `cycle-representatives`, `cycle`) are refused by every selector and enum.
- An existing member is the control on every selector.

**No behaviour change at evaluation.** `atoms.rs:3262-3268` still refuses the op (`ATOM_OP`). No pack row, policy document or fixture uses it, and no hand-written code matches on the three enums. See judgment call 6 for policy admission.

### The staged lock

The lock change is staged in the worktree, as F8b and P0 staged theirs. `evidence/stage_lock_i1a.py` writes HEAD's `design-lock.json` plus one `contractSuccessors` entry:
- record `i1-a/successor.json` and subject `i1-a-subject.json`, both real pins;
- review `SCRATCH-I1A/review.json` (150 bytes, `e048b5f3…`) and assent `SCRATCH-I1A/assent.json` (611 bytes, `5998db07…`), placeholders whose bytes are `verify_scratch_i1a.py`'s synthetic overlay.

The inventory chain and the 100 inheritance rows are unchanged. The staged lock is 502,181 bytes, sha256 `c376f76e19032dfee95fb699901d59d99b4bb4b14bfa84aaae77e2fbd2679f11`, in the lock's canonical formatting.

At integration, the lead:
1. copies your review files in;
2. completes `i1-a-unit.json` (`ACCEPTED-DESIGN-UNIT`, pinning `review-contract.json`);
3. replaces exactly the two placeholder pins;
4. runs plain `verify_design` and the public `generate_contracts.py`, which must report `changed: []`;
5. commits.

**Plain `verify_design` and the plain public generator refuse the staged lock,** with "missing or escaping regular file: SCRATCH-I1A/review.json". That is correct until review, and `verify_scratch_i1a.py` asserts it. `design-lock.json` stays outside the materialization map, as in F8b and P0; its staged bytes are pinned here, and the diff sha covers them.

## Pins checked

- **X9.** I1-a touches no crash-matrix source, fixture, required-runs file or `tools/check_crash_matrix.py`, and no `Cargo.toml`, so X9's manifest pin and X8's `feature_pin` read unchanged bytes. The crash-matrix feature lane passes without a run set.
- **Every consumer of the old digests.** On base, `311c1feb…` and `b221b5ed…` appear only in the two source maps, both registries, the closure and the atom registry; the closure's `6796d7ec…` (source map) only in the closure; `bb093a9c…` (closure) only in `registry.json` and `report.ts`; `eecde992…` (registry) only in `report.ts`; `595fc28d…` (admission registry) only in the admission map; the generated `evidence.rs` and `identity.rs` digests only in the contracts dependency policy; and `schema_registry.rs`'s only in the identity dependency policy. All are re-pinned. `schema_registry.rs` carries the two source digests as decimal byte arrays, and the byte counts `197480` and `26534` appear only at these sites.
- **TypeScript lanes.** `tools/typescript-lanes.json` pins none of the 15 files. The TypeScript lanes themselves still cannot run on this Mac (esbuild 0.28.2 is not in the offline cache), unchanged from F8b.
- **Inventory.** Every changed file is a planned row of v135, and no row's description becomes false. See judgment call 1.
- **Generator.** `run_generation_i1a.py` checked all 349 closure pins, the registry joins (every `sourceSha256` against its file) and rebuild-02's receipt before running.

## Lead results

All lanes ran serially on `5e25d04` plus this diff (the staged lock included), with a private 0700 TMPDIR and `--locked --offline`. `~/Library/Application Support/OpenSIP` was absent before and after.

**One record-only refreeze after the cargo lanes.** A docstring in `verify_scratch_i1a.py` said the admission registry is selected once; the script asserts twice (the architecture copy and its `product/` copy). The docstring was corrected and the record refrozen, which changed only arch files and the staged lock's record, subject and placeholder pins. Every product source byte is unchanged, and no cargo test or tool test reads `design-lock.json`. So the cargo and Python lanes stand; `verify_scratch_i1a.py`, `drift_scratch_i1a.py`, plain `verify_design` and the plain public generator were rerun on the final bytes, with the results below.

| Check | Result |
|---|---|
| Baseline: public `generate_contracts.py` on the unmodified worktree | Passes, `changed: []` |
| `cargo fmt --all --check` | Clean |
| `cargo build --workspace --all-targets` | Pass (warm target directory) |
| Clippy `-D warnings`, workspace `--all-targets` | Clean |
| Clippy `-D warnings`, platform, security, storage and host with `crash-matrix` | Clean |
| Clippy `-D warnings`, security, storage and host with `scenario-fixtures` | Clean |
| `cargo test --workspace --all-targets --no-fail-fast`, run 1 | 1732 passed, 0 failed, 3 ignored (20 binaries; P0's 1731 plus the new test) |
| The same, run 2 | 1732 passed, 0 failed, 3 ignored |
| `cargo test --workspace --doc` | 18 passed |
| `cargo test -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets --no-fail-fast` | 1630 passed, 0 failed, 3 ignored (P0's 1629 plus the new test). Includes storage's `commit_tests` and host's `commit_matrix_tests`, without a run set. |
| `evidence/drift_scratch_i1a.py` (staged mode; the real public `generate_contracts.generate`, write false) | Passes: 40 sources, 8 outputs, `changed: []`, generator closure selected |
| Plain public `generate_contracts.py` on the staged lock | Refuses at `SCRATCH-I1A/review.json` (exit 1). Correct until integration. |
| `evidence/verify_scratch_i1a.py` (staged mode) | Passes. Contract successors 87 → 88, I1-a with 25 inputs and no overrides; inventory successors 95, v135 selected, 100 inheritance rows and 21 supersessions unchanged; 40 generation sources; 48 admission sources and 15 aliases. The closure is selected once (by I1-a) and the admission registry twice (I1-a's two copies). HEAD's lock alone passes, and on this tree refuses with "admission source is not selected by accepted design". |
| Plain `verify_design.py --architecture ../opensip_arch --implementation .` on the staged lock | Refuses: "missing or escaping regular file: SCRATCH-I1A/review.json" (exit 1) |
| `check_package_edges.py --lane host`, against v135 | Passes: 12 workspace packages, 22 declared and 20 resolved internal edges, none new |
| `check_package_edges.py --lane rust-provider`, against v135 | Passes: `opensip-rust-provider` only |
| `tools/tests/test_package_edges.py` | 14 run, OK |
| `check_dependencies.py --feature-profile security-crypto-workspace` | Passes: 11 dependencies, 8 local sources. With the base (`5e25d04`) policy as `--policy` it refuses: "local contracts source bytes differ: src/generated/evidence.rs". |
| `check_identity_dependencies.py` | Passes: 8 dependencies, 305 sources. With the base policy it refuses: "source bytes differ: …/crates/identity/src/schema_registry.rs". |
| `tools/tests/test_dependency_policy.py` | 9 run, OK |
| `tools/tests/test_identity_dependencies.py` | 5 run, OK |

Commands, from the worktree, with `PY=/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14`, `CARGO=/opt/homebrew/Cellar/rust/1.95.0/bin/cargo`, `AR=~/.cargo/registry/cache/index.crates.io-1949cf8c6b5b557f`, `E=../opensip_arch/docs/implementation/m3/preview-pack-i1/i1-a/evidence` and `OUT=/tmp/opensip-implementation/reviews/codex2-i1a-r1`:

```sh
cargo fmt --all --check
cargo build --workspace --all-targets --locked --offline
cargo clippy --workspace --all-targets --locked --offline -- -D warnings
cargo clippy -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets --locked --offline -- -D warnings
cargo clippy -p opensip-security -p opensip-storage -p opensip-host --features scenario-fixtures --all-targets --locked --offline -- -D warnings
cargo test --workspace --all-targets --no-fail-fast --locked --offline   # twice
cargo test --workspace --doc --locked --offline
cargo test -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets --no-fail-fast --locked --offline
nice -n 19 $PY -I -B $E/verify_scratch_i1a.py .
nice -n 19 $PY -I -B $E/drift_scratch_i1a.py . $OUT/drift-scratch
nice -n 19 $PY -I -B tools/verify_design.py --architecture ../opensip_arch --implementation .   # refuses at SCRATCH-I1A
cargo metadata --locked --offline --format-version 1 > $OUT/host.json
(cd providers/rust && cargo metadata --locked --offline --format-version 1) > $OUT/provider.json
nice -n 19 $PY -I -B tools/check_package_edges.py --repository . --metadata $OUT/host.json --inventory ../opensip_arch/docs/implementation/m2/repository-file-inventory.v135.json --lane host
nice -n 19 $PY -I -B tools/check_package_edges.py --repository . --metadata $OUT/provider.json --inventory ../opensip_arch/docs/implementation/m2/repository-file-inventory.v135.json --lane rust-provider
nice -n 19 $PY -I -B tools/tests/test_package_edges.py -v
nice -n 19 $PY -I -B tools/check_dependencies.py --manifest Cargo.toml --target aarch64-apple-darwin --cargo $CARGO --feature-profile security-crypto-workspace
nice -n 19 $PY -I -B tools/check_identity_dependencies.py --manifest Cargo.toml --target aarch64-apple-darwin --cargo $CARGO --archives $AR --policy tools/identity/dependency-policy.json
nice -n 19 $PY -I -B tools/tests/test_dependency_policy.py --target aarch64-apple-darwin --cargo $CARGO -v
nice -n 19 $PY -I -B tools/tests/test_identity_dependencies.py --target aarch64-apple-darwin --cargo $CARGO --archives $AR -v
```

**Replaying the materialization** (optional, on a scratch worktree of your own at `5e25d04` with the two provisioned trees copied in): `apply_i1a.py W pins`, then `run_generation_i1a.py W $OUT/gen --write`, then `apply_i1a.py W policies`, then add the test from the `product/` copy of `schema_sources.rs`. The tree must then equal the subject's `product/` copies and I1-L's two schema copies byte for byte. Each `apply_i1a.py` phase refuses unless every value it changes still holds its `5e25d04` value.

## Judgment calls

The lead took each as a lead decision. Questions 1, 2 and 5 are where a reviewer could most reasonably differ.

1. **No inventory successor.**
   - **Why:** UNITS r2 says "Inventory successor", but I1-a adds no file, and every changed file is a planned row of v135 whose description stays true. An inventory successor with no added row is refused by `verify_design` ("inventory successor must contain sorted unique additions"), and a description refresh needs a passage override, which nothing here calls for. v136 stays unused.
   - **Question:** do you agree that no row of the 15 changed files needs a new meaning?
2. **Two review files.**
   - **Why:** the lead asked for ACCEPT-UNIT, but the lock binds a contract successor only to a review whose top-level verdict is `ACCEPT-DESIGN-UNIT` (`verify_design.py:198-199`). 458b's precedent is one unit with a separate contract review file.
   - **So:** `review.json` carries the unit verdict, and `review-contract.json` is the file the lock binds (shapes under "Decide").
   - **Question:** is that split acceptable, or would you rather give one ACCEPT-DESIGN-UNIT `review.json`, as F8b and 468a did?
3. **Members UNITS and I1-L's list omit:** the generator closure (`generate_contracts.py` requires its exact bytes to be an accepted design input, as in 468a and F8b) and the two dependency policies (both checkers refuse stale local-source pins). UNITS's `evidence.rs:38891` is `Policy1AtomOp`'s `count-at-most` arm; the widened enum is `Policy2AtomOp` (`:40075`).
4. **The materialization map points the two schema sources at I1-L's copies,** instead of duplicating them under `i1-a/product/`. So each byte string has one authority, and the source maps pin the same paths. The other 13 files are copied, as in 468a.
5. **`scannerIdentitySchema.fixturePath` is kept.** I1-L says only that the pin "moves to the PIDS copy's bytes". The `fixturePath` names a file in reconstruction-48's reference tree, which no product code or tool reads; it now sits beside a byte count and digest that tree's file does not have. **Question:** keep it, or should it name I1-L's product copy? If the latter, that is a one-line change and a refreeze, and the lead would want your exact replacement value.
6. **Policy admission between I1-a and I1-b1.** Before I1-a the policy-document:2 schema refused the op. After it, the schema admits the op, and `atom_law` (`policy.rs:229-331`) does not check op names. So a rule using the op with subject kind `symbol` over `imports` would now pass policy admission and refuse only at evaluation (`ATOM_OP`). The law's own pack form (subject kind `file`) still refuses at the source-kind check (`policy.rs:260-289`), as UNITS says.
   - No path reaches this today: the release registry has zero rows, `PackSource::Supplied` always refuses, and no product source writes a policy using the op.
   - I1-b1 adds item 2.2's op law next.
   - **The lead's reading:** this is inherent in the law's unit order (I1-a → I1-b1), so it is recorded, not changed. A guard in I1-a would be I1-b1's work done early.
   - **Question:** do you agree?
7. **Parents.** The twelve parents are the selected architecture copies of the changed files' base bytes (468a's six, F8b's three) plus I1-L's three copies that I1-a pins. `identity.rs`, `atom-registry.json` and the two dependency policies have no selected copy of their base bytes, so they have no parent. `freeze_i1a.py` asserts each parent equals its file's base bytes.

## Decide

- **Faithfulness:** do the product schema sources equal I1-L's accepted copies byte for byte? Does every other change follow mechanically from those bytes, with nothing a later unit (I1-b1, I1-b2, I1-c) owns?
- **The record:** check it as a contract successor: the subject covers every candidate, parents are accepted bases at their pinned bytes, there are no overrides, and no candidate path is already accepted. Is the materialization map exact against the worktree?
- **Generation:** rerun `drift_scratch_i1a.py` yourself (with your own output path). Optionally rerun `run_generation_i1a.py` without `--write` into your output directory and confirm the summary.
- **Rerun the lanes above:** fmt, the workspace build, the three clippy lanes, the workspace tests (twice if time allows), the doc tests, the crash-matrix feature lane, `verify_scratch_i1a.py` (staged mode), plain `verify_design` (it must refuse at `SCRATCH-I1A/review.json`), both package-edge lanes against v135, and both dependency checkers with their suites.
- **The test:** does it show what UNITS asks ("schema admission of the token")? Are the controls sufficient?
- **Judgment calls:** are calls 1 to 7 acceptable? Answer questions 1, 2, 5 and 6 directly.

Write REVIEW.md, `review.json` and `review-contract.json` under the output directory.

`review.json` (the unit) needs:
- "verdict": ACCEPT-UNIT or REQUIRED-FINDINGS;
- "requiredFindings";
- "subjectSha256": `fa7f4fda73b3eb213da91921ca868f3fa4feaf5e75c72f982704ebb849bd36c4`, the diff's sha256, as a single string;
- "subjectManifestSha256": `3c89d7da193e25d5c8c6dcb8a5410b2d2be4fe0b6133402349e55b14e2fd7bcf`, as a single string;
- "contractSuccessorAssessment": verdict (ACCEPT-DESIGN-UNIT or REQUIRED-FINDINGS), requiredFindings, and "successor", the record's pin (path `docs/implementation/m3/preview-pack-i1/i1-a/successor.json`, 8748 bytes, sha256 `7d6c04e9914809409e01027e63d7b9cde670c6e8757538a13b743b9d0af5a03d`).

`review-contract.json` (the file the lock binds) needs:
- "verdict": ACCEPT-DESIGN-UNIT or REQUIRED-FINDINGS;
- "requiredFindings";
- "subjectManifestSha256": `3c89d7da193e25d5c8c6dcb8a5410b2d2be4fe0b6133402349e55b14e2fd7bcf`, as a single string;
- "successor": the same record pin.

There is no inventory successor, so neither file carries an `inventoryCandidateAssessment`.

Do not commit.
