CODEX2 review: unit **I1-b1** r1 of law M3-I1 r3 — evaluator admission of the preview pack's `cycle-representative` op (PROPOSAL 2.2's op law in `policy.rs`). Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT-UNIT** on the diff. I1-b1 adds no file and binds no design, so it has **no inventory successor and no contract successor**: no `subjectManifestSha256`, `inventoryCandidateAssessment` or contract review file is needed (judgment call 7).

**Rules:**
- No repository edits, commits, pushes or delegation.
- Write only under `/tmp/opensip-implementation/reviews/codex2-i1b1-r1`.
- You own the native lane for this review:
  - Use a `CARGO_TARGET_DIR` under that directory.
  - Use a private 0700 `TMPDIR` under `$(getconf DARWIN_USER_TEMP_DIR)`, because other worktrees churn the shared temp folder.
  - Run cargo `--locked --offline`.
  - Write every scratch output (the drift directory, cargo metadata) under your output directory, never into either repository.
- **The generator is shared.** Before the drift check, check that no other `opensip-contract-generator` or `generate_contracts.py` process is running.
- Run git read-only, and only against the worktree named below.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.
- No crash-matrix lead run set is needed or wanted (see "Pins checked", X9).

**Shared machine.** Other agents' lanes and X9 lead sets run on this machine under a 5000 ms timing guard. Before any cargo build, test or clippy run, take the shared lane lock with `mkdir "$(getconf DARWIN_USER_TEMP_DIR)opensip-lanes.lock"`, and remove it with `rmdir` straight after. If the lock is held, wait until it is free with a background poll. Python-only lanes need no lock.

## Inputs

All inputs are pinned in `hashes.txt`. Laws are pinned by their accepted snapshots, never by a live `PROPOSAL.md`.

### Law

- **The law: M3-I1 r3** (`docs/implementation/m3/preview-pack-i1/PROPOSAL-r3.md`, 68025 bytes, `204f8ee8…`, your r3 ACCEPT in `reviews/codex2-preview-pack-i1-r3/`). The live `PROPOSAL.md` is these bytes plus the acceptance note.
  - **Item 2.2** (:115-128), the op law: the atom is its rule's whole `emitWhen`; `relation` is `imports` and `minResolution` is `resolved-target`; `filters` is `[]`; `endpoint` and `evidence` are absent; the rule's `subjectEnumeration.subjectKind` is `file`. "Any violation is the existing rule-law detail `POLICY.UNKNOWN_RULE`", in a bundled document X12 row 4. "For this op only, the subject-kind check is 'the subject is a file'. It replaces the relation source-kind check (`policy.rs:260-289`)."
  - **Item 2.1** (:108-113), the syntax, and **LD-11** (:463): evaluation refuses the op structurally (`ATOM_OP`) until I1-b2.
- **The unit row:** `UNITS-r2.md` (`0c3c0f44…`, equal to the live `UNITS.md`), row I1-b1: "PROPOSAL 2.2 in `policy.rs` … This holds in both the policy pass and the program pass (`policy.rs:332-373`, `:608-642`), with `POLICY.UNKNOWN_RULE` on any violation. **Tests:** under a `cfg(test)` registry, a test pack using the op admits, and each violation is row 4 with `PackDefect::RuleLaw`." Edges: I1-a → I1-b1 → I1-c, I1-b1 → I1-b2. Case 13 (op-law refusals) is the I1-L model's and I1-b2's; I1-b1's tests cover its admission half.
- **The bound contract text:** I1-L's §4a (`i1-l/atom-section-4a.md`, `f21e1ef7…`, lines 12-25), which carries item 2.2 verbatim into the atom contract.
- **X12 r3** (`m2/policy-admission-x12/PROPOSAL-r3.md`, `11628912…`): item 6.6, "the existing `check_program_laws` over the policy and its compiled program, which gives `POLICY.UNKNOWN_RULE` or `IMPORT.ABSENT_FOR_PREDICATE`" (:96), and row 4 (:111).
- **I1-a's review** (`reviews/codex2-i1a-r1/`): judgment call 6 (the interim symbol-kind admission I1-b1 closes) and the observation I1A-NB-1 (see "I1A-NB-1" below).

### Product

- **Worktree:** `/Users/sb/code/opensip-ai/opensip-i1b1`, detached at main `0765f8c` (I1-a integrated at `4c761e8`; 101 contract successors and 5 passage supersessions, 96 inventory successors, v136 selected). Nothing is committed and no file is added.
- **Diff:** `git diff 0765f8c` is 16054 bytes, sha256 `4371f9dfa2aba740747ac5ea887fa95b0ec53acac2305196f9f920725d13e822`. It covers 2 files, +313 −10, both in `crates/evaluator`: `policy.rs` +38 −9 and `policy_pack_tests.rs` +275 −1. A copy is at `evidence/i1b1.diff`.
- **Toolchain:** `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin`; Python `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14`; generator `~/opensip-deps/contracts-generator-rebuild-02/opensip-contract-generator`; Node `~/.nvm/versions/node/v24.16.0/bin/node`. The worktree also holds the ignored `tools/contracts/node_modules` and `tools/contracts/python-packages`, copied from the main checkout for the drift check.

## What I1-b1 changes

| File | Change |
|---|---|
| `crates/evaluator/src/policy.rs` | The op law of item 2.2, in the policy pass and the program pass (below). Nothing public changes. |
| `crates/evaluator/src/policy_pack_tests.rs` | Its `cfg(test)` module (`#[path]` from `policy.rs`): four tests and their helpers, appended, and one sentence in the module comment. No existing test changes. |

Nothing else changes: no other crate, manifest, `Cargo.lock`, feature, schema, generated file, registry (`atom-registry.json`, `pack-registry.json`), fixture, crash point or design input.

### `policy.rs`

| Part | What it does |
|---|---|
| `cycle_representative_law(atom, subject_kind, root)` (new, private) | Item 2.2's conjuncts, exactly: `root`; `relation` is `"imports"`; `minResolution` is `"resolved-target"`; `filters` equals `[]`; no `endpoint` member; no `evidence` member; `subject_kind` is `file`, or `None` in the program pass (judgment call 1). |
| `atom_law` gains `root: bool` | For an atom whose `op` is `cycle-representative`, it first requires the op law and returns false on any violation. The shared atom law then runs as before, except that the relation's source-kind check is skipped for this op (`if !cycle && !kinds…`): item 2.2's "the subject is a file" replaces it. Every other op takes exactly the old path; `root` is read only by the op law. |
| `rule_law` (the policy pass) | Passes `depth == 1`: the root of `emitWhen` is the only node at depth 1. Any `false` is the existing `POLICY.UNKNOWN_RULE`, so a bundled document's violation is `POLICY_RULE_NOT_ADMISSIBLE:policy:<ruleId>:POLICY.UNKNOWN_RULE`, row 4 via `admit_from`'s `PackDefect::RuleLaw`. |
| `check_program_laws`'s program loop (the program pass) | The stack carries `(node, root)`, with `true` only for the rule's `emitWhen`; operands of `and`, `or` and `not` are pushed with `false`. Any `false` is the existing `POLICY_ATOM_NOT_ADMISSIBLE:program:<ruleId>:POLICY.UNKNOWN_RULE`. |

All three owners that call `check_program_laws` (`inspect_policy_program`, `compile_plan_policy`, `admit_from`) get the law with no further change. The op still refuses at evaluation (`atoms.rs:3263-3268`, `ATOM_OP`) until I1-b2 (LD-11), and the release registry still has zero rows until I1-c.

**What I1-b1 closes.** I1-a's judgment call 6: between I1-a and I1-b1 the widened schema admitted the token and `atom_law` did not check op names, so an `imports` rule over `symbol` subjects using the op passed policy admission (and the file-kind form refused at the source-kind check). After I1-b1 the symbol form is refused (`symbol`, `export` and `package` are three of the tests' cases) and the file form admits.

## Tests

All four are in `policy_pack_tests.rs`. The first three run on synthetic documents: the bundled test document (`tests/fixtures/policy-pack-test-fixture.policy.json`) with its one rule's `emitWhen`, `subjectKind` and, in one case, `evidenceUse` replaced, bundled under the test ID in a one-row `cfg(test)` registry built in memory, as `bundled_defects_are_row_4_never_row_3` already does. No fixture file is added.

1. **`cycle_representative_test_pack_admits_under_its_op_law`.** A test pack whose rule is item 2.1's atom over `file` subjects admits through `admit_from`: its pack ID, its policy digest, a one-rule program whose `emitWhen` is the atom, its program digest, and determinism. **"For this op only" controls:** an `exists` atom over `imports` with `file` subjects is still refused by the unchanged source-kind check (row 4, `RuleLaw`), and with `symbol` subjects it admits, both at the root and under `not`, since root-only is this op's alone.
2. **`cycle_representative_op_law_violations_are_row_4_rule_law`.** Seventeen violations, each a schema-admissible bundled document refused as `HostInvariant { subject: "pack:opensip.test.fixture.pack:1", defect: RuleLaw("POLICY_RULE_NOT_ADMISSIBLE:policy:no-consumer:POLICY.UNKNOWN_RULE") }`:
   - **position:** under `not`; an operand of `and`; an operand of `or`; both operands of `and`; under `not` under `and`;
   - **relation and rung:** `references` at `resolved-binding`; `file` at `enumerated`; `imports` at `syntactic-specifier`;
   - **filters:** a `subject` `prefix` filter; a `resolution` `eq resolved-target` filter (a filter that restates the rung is still a filter);
   - **endpoint:** `target`; `source`, written out (judgment call 3);
   - **evidence:** `runtime` undeclared, and `runtime` declared in `evidenceUse` (judgment call 4);
   - **subject kind:** `symbol`, `export`, `package`.

   Each of the atom's own violations other than `evidence` would pass the shared atom law with the kind check skipped (the relation is registered, the rung is on its ladder, `imports` admits `endpoint: target` at `resolved-target`, and both filters are admissible), so each is refused by the op law, not by an older check. Through admission, two conjuncts are also implied by the shared law with today's registry: no ladder but `imports`' holds `resolved-target`, so a relation violation also breaks the rung conjunct; and `imports` is native, so `evidence` is also refused by the plane check. Test 4 checks both on their own. **Control:** `n` on the atom is the schema's to refuse (PDS:339-363), so it is `PackDefect::Schema`, before the rule law.
3. **`cycle_representative_op_law_holds_in_the_program_pass`.** `check_program_laws` directly, with a lawful policy beside a program whose `emitWhen` is the lawful atom (passes) or each of the thirteen `emitWhen` violations above (each refused with `POLICY_ATOM_NOT_ADMISSIBLE:program:no-consumer:POLICY.UNKNOWN_RULE`). Then the kind: a `symbol` policy with its own compiled program is refused by the policy pass (`POLICY_RULE_NOT_ADMISSIBLE:policy:…`), and the `file` policy passes. Through the three owners, a program always equals its policy's compilation (`compile_program`, or `RULE_PROGRAM_COMPILATION_JOIN` for a retained one), so the program pass can only be reached with a violation directly (judgment call 5).
4. **`cycle_representative_op_law_stands_alone`.** `cycle_representative_law` itself, independent of the registry: the lawful atom passes with `Some("file")` and with `None`; it fails off the root, and with `symbol`, `export` or `package`; and each of six single-member violations (relation `references`, rung `syntactic-specifier`, a filter, `endpoint` `source` and `target`, `evidence`) fails with `Some("file")` and with `None`.

**Mutation check** (`evidence/mutants.py`, `evidence/mutants.json`). Each mutant of `policy.rs` was built and the four tests run, under the lane lock, with the unmutated tree as the control (it passes). All twelve mutants are killed:
- dropping the root, relation, rung, filters, endpoint, evidence or kind conjunct (M1 to M7);
- demanding `Some("file")` in the program pass (M8);
- keeping the source-kind check for the op (M9);
- never applying the op law (M10);
- treating every node as the root in the policy pass (M11, caught by test 2 only) or in the program pass (M12, caught by test 3 only).

M2 (relation) and M6 (evidence) are caught by test 4 only, for the reason given under test 2. On base `policy.rs` (HEAD) the first three tests all fail: see `evidence/mutants-first-run.txt`, a run made before test 4 existed, in which M2 and M6 survived and every other mutant was killed as now. With test 4, base `policy.rs` no longer compiles against the tests, since test 4 names the new function.

**Source pin.** `source_pin_release_build_holds_no_test_row_or_runtime_read` reads `policy.rs` and passes unchanged: still 7 `include_bytes!(`, one `PackRegistry {`, two `&RELEASE_PACKS`, and none of its forbidden strings.

## Pins checked

- **X9: no row moves, so no run set.** The diff touches only `crates/evaluator`, which no crash-matrix row, census point, `required-runs.v1.json`, X9 source or `tools/check_crash_matrix.py` names, and no `Cargo.toml`. It adds no `crash_barrier!`, `crash_scope!`, clock sample, file write or `cfg(feature …)` site. The crash-matrix feature lane passes without a run set.
- **No existing test changes.** The diff only appends to `policy_pack_tests.rs` (and one module-comment sentence); every earlier test's body and expected values are byte-identical, and they pass in every run below. The host's policy fixtures (`plan-policy-fixtures.json`, `configuration_tests.rs`) use no `cycle-representative` atom, and I1-a's schema test is schema-only.
- **Inventory.** No file is added, removed or renamed, so v136 (selected at `0765f8c`) stands. `policy.rs`'s row ("Admit and compile the closed declarative policy language …") and `policy_pack_tests.rs`'s row (which lists "rule-law … defects … as host-invariant faults" and "the test pack admitted with its policy and program digests") stay true. See judgment call 7.
- **Dependency policies and package edges.** No manifest, lock, feature or edge changes. `crates/evaluator` sources are not pinned by either dependency policy (both checkers pass on the unchanged policies, Lead results).
- **Generators.** No schema, generator input or TypeScript lane source changes. The drift check on HEAD's lock reports `changed: []`. `design-lock.json` is unchanged.
- **Inputs.** All `hashes.txt` pins were rechecked against the files after the lanes.

## Lead results

All lanes ran serially on `0765f8c` plus this diff (`evidence/lanes.sh`), each under the lane lock, with a private 0700 TMPDIR, `nice -n 10` and `--locked --offline`. `~/Library/Application Support/OpenSIP` was absent before and after, and the diff's sha256 was the same before and after (`evidence/lanes-summary.txt`). Other agents' lanes ran between these, under the same lock. Main's counts below are those J2a's request gives for `d2c00a9`; no commit since (REG v3, CRC-2, ENUM-1, SD-8) changes a Rust file.

| Check | Result |
|---|---|
| `cargo fmt --all --check`, and `rustfmt --edition 2024 --check` on the `#[path]` module `policy_pack_tests.rs` | Clean |
| `cargo build --workspace --all-targets` | Pass |
| Clippy `-D warnings`, workspace `--all-targets` | Clean |
| Clippy `-D warnings`, platform, security, storage and host with `crash-matrix` | Clean |
| Clippy `-D warnings`, security, storage and host with `scenario-fixtures` | Clean |
| `cargo test --workspace --all-targets --no-fail-fast`, run 1 | 1742 passed, 0 failed, 3 ignored (20 test binaries, 515 s): main's 1738 plus I1-b1's four. |
| The same, run 2 | 1742 passed, 0 failed, 3 ignored (502 s) |
| `cargo test --workspace --doc` | 20 passed, as main |
| `cargo test -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets --no-fail-fast` | 1636 passed, 0 failed, 3 ignored (10 binaries, 524 s), equal to main: this lane does not run `opensip-evaluator`'s own tests. It includes storage's `commit_tests` and host's `commit_matrix_tests`, without a run set. |
| The four new tests and the twelve earlier `pack_tests` | Pass in both workspace runs, the source pin included |
| Mutation check (`evidence/mutants.json`) | Control passes; 12 of 12 mutants killed |
| `generate_contracts.py` drift check, HEAD's lock (unchanged) | Passes: 40 sources verified, 8 outputs, `changed: []`. No generator was running (the process check matched only another agent's lane wrapper waiting for the lock), and the check ran under the lock. |
| Plain `verify_design.py --architecture ../opensip_arch --implementation .` | Passes: 101 contract successors and 5 passage supersessions, 96 inventory successors with v136 selected, 100 inheritance rows, 21 inventory supersessions, 46 inputs; 40 generation sources; 48 admission sources and 15 aliases |
| `check_package_edges.py --lane host`, against v136 | Passes: 12 workspace packages, 22 declared and 20 resolved internal edges, none new |
| `check_package_edges.py --lane rust-provider`, against v136 | Passes: `opensip-rust-provider` only |
| `tools/tests/test_package_edges.py` | 14 run, OK |
| `check_dependencies.py --feature-profile security-crypto-workspace` | Passes: 11 dependencies, 8 local sources |
| `check_identity_dependencies.py` | Passes: 8 dependencies, 305 sources |
| `tools/tests/test_dependency_policy.py` | 9 run, OK |
| `tools/tests/test_identity_dependencies.py` | 5 run, OK |

Commands, from the worktree, with `PY=/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14`, `PYAPP=/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/Resources/Python.app/Contents/MacOS/Python` (the generator's pinned interpreter), `CARGO=/opt/homebrew/Cellar/rust/1.95.0/bin/cargo`, `AR=~/.cargo/registry/cache/index.crates.io-1949cf8c6b5b557f`, `V=../opensip_arch/docs/implementation/m2/repository-file-inventory.v136.json` and `OUT=/tmp/opensip-implementation/reviews/codex2-i1b1-r1`:

```sh
cargo fmt --all --check
rustfmt --edition 2024 --check crates/evaluator/src/policy_pack_tests.rs
cargo build --workspace --all-targets --locked --offline
cargo clippy --workspace --all-targets --locked --offline -- -D warnings
cargo clippy -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets --locked --offline -- -D warnings
cargo clippy -p opensip-security -p opensip-storage -p opensip-host --features scenario-fixtures --all-targets --locked --offline -- -D warnings
cargo test --workspace --all-targets --no-fail-fast --locked --offline   # twice
cargo test --workspace --doc --locked --offline
cargo test -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets --no-fail-fast --locked --offline
cargo test -p opensip-evaluator --lib --locked --offline -- pack_tests::cycle_representative   # I1-b1's four
$PY -I -B tools/generate_contracts.py --architecture ../opensip_arch --output $OUT/drift --node ~/.nvm/versions/node/v24.16.0/bin/node --generator ~/opensip-deps/contracts-generator-rebuild-02/opensip-contract-generator --python $PYAPP
$PY -I -B tools/verify_design.py --architecture ../opensip_arch --implementation .
cargo metadata --locked --offline --format-version 1 > $OUT/host.json
(cd providers/rust && cargo metadata --locked --offline --format-version 1) > $OUT/provider.json
$PY -I -B tools/check_package_edges.py --repository . --metadata $OUT/host.json --inventory $V --lane host
$PY -I -B tools/check_package_edges.py --repository . --metadata $OUT/provider.json --inventory $V --lane rust-provider
$PY -I -B tools/tests/test_package_edges.py -v
$PY -I -B tools/check_dependencies.py --manifest Cargo.toml --target aarch64-apple-darwin --cargo $CARGO --feature-profile security-crypto-workspace
$PY -I -B tools/check_identity_dependencies.py --manifest Cargo.toml --target aarch64-apple-darwin --cargo $CARGO --archives $AR --policy tools/identity/dependency-policy.json
$PY -I -B tools/tests/test_dependency_policy.py --target aarch64-apple-darwin --cargo $CARGO -v
$PY -I -B tools/tests/test_identity_dependencies.py --target aarch64-apple-darwin --cargo $CARGO --archives $AR -v
```

`evidence/mutants.py` rewrites its `ROOT`'s `policy.rs` in place and restores it. To rerun it, copy the worktree under your output directory and point `ROOT` at the copy; never run it against `opensip-i1b1`.

## I1A-NB-1: recorded for I1-b1, not taken up

Your I1-a review left one observation, I1A-NB-1: `scannerIdentitySchema.fixturePath` (`crates/evaluator/src/atom-registry.json:945-948`) is a historical reference-fixture locator beside I1-L's current byte pin; "align or relabel it when that reference-fixture metadata is next maintained". The work log recorded it for I1-b1 ("I1-a accepted by CODEX2"). I1-b1 does not change it, for three reasons:
1. **Its trigger has not occurred.** I1-b1 is item 2.2's op law in `policy.rs`. Policy admission reads four members of the atom registry (`relations`, `comparatorTable`, `portableUniverseDomains`, `policyUniverseMap`) and never `scannerIdentitySchema`; I1-b1 maintains no reference-fixture metadata. No product code or tool reads `fixturePath` at all.
2. **No law settles the value.** I1-L says only that the pin "moves to the PIDS copy's bytes", and your judgment-call-5 answer required no replacement value. Pointing it at I1-L's product copy, relabelling the key, or removing it is a choice none of M3-I1, I1-L or I1-a makes, and the lead's instruction for this unit is to stop rather than decide such a choice.
3. **The file is a materialized member of I1-a's record.** `atom-registry.json`'s current bytes are I1-a's accepted candidate `i1-a/product/crates/evaluator/src/atom-registry.json` (30488 bytes, `9aabc999…`). Changing them here would leave that record's copy describing bytes the product no longer has, which is a record change for a unit that re-records the file.

**Recommendation (for the lead):** take it up in the next unit that edits `atom-registry.json` for its own reasons, with the value chosen and recorded there; failing that, a record-maintenance follow-up. It blocks nothing: the locator has no consumer, and the bytes it sits beside are independently pinned.

## Judgment calls

The lead takes each as a lead decision (2026-10-04). Calls 1, 3 and 5 are where a reviewer could most reasonably differ.

1. **The kind conjunct in the program pass.** A `RuleProgramV2` rule carries `ruleId`, `ruleProgramRef` and `emitWhen` only (the closed schema), so the program pass has no `subjectEnumeration` and calls `atom_law` with `None`, as it always has. For this op, `None` passes the kind conjunct, and every other conjunct (root, relation, rung, filters, endpoint, evidence) is enforced in both passes. The kind is enforced by the policy pass, which `check_program_laws` runs first over the policy whose compilation the program is. Item 2.2 states the conjunct as "the rule's `subjectEnumeration.subjectKind`", which only the policy has, so the lead reads "holds in both passes" as each conjunct holding wherever its operand exists. **Rejected:** refusing `None` (it would refuse every lawful program), and deriving a kind from the registry for this op (the registry's `imports` source kind is `symbol`, which is exactly the check item 2.2 replaces). **Question:** do you agree that this meets UNITS's "both passes"?
2. **The op law is checked first, then the shared atom law with only the source-kind check skipped.** Item 2.2 says the rule law "also requires" the op law, and that the file check "replaces the relation source-kind check". So the shared law (registry relation, ladder rung, endpoint, evidence plane, filters) still runs for this op. With today's registry it is implied by the op law, but the registry stays its authority.
3. **"Absent" is literal.** `"endpoint":"source"` written out is refused, although `source` is the default (2.1: "It has no `endpoint`"; 2.2: "`endpoint` and `evidence` are absent"). The schema already forbids `null` for both. **Question:** agree that an explicit `source` is a violation?
4. **Declared evidence.** An `evidence` member is refused by the op law even when `evidenceUse` declares it, and an undeclared one gives `POLICY.UNKNOWN_RULE`, not `IMPORT.ABSENT_FOR_PREDICATE`: the op law runs inside `atom_law`, before `rule_law`'s evidence join. Item 2.2: "Any violation is the existing rule-law detail `POLICY.UNKNOWN_RULE`."
5. **Where the root bit lives.** `atom_law` takes `root`, set by its two callers: `depth == 1` in `rule_law`, and a carried flag in the program pass. Only the op law reads it. The program pass cannot be reached with a violation through the three owners (a program equals its policy's compilation), so test 3 calls `check_program_laws` directly with a program that differs from its policy. **Question:** is that direct test the right evidence for the program pass?
6. **A synthetic test pack, not I1-P's document.** UNITS asks for "a test pack using the op". The tests use the bundled test document with item 2.1's atom as its rule (byte-identical `emitWhen` to I1-P's 5.2 document), not 5.2's bytes: those, their registry row and their self-checks S1 to S9 are I1-c's.
7. **No inventory successor and no new file.** The lead told this unit to put its tests in an existing file. They are in `policy_pack_tests.rs`, `policy.rs`'s existing `cfg(test)` module for pack admission, beside the X12a row-4 tests they extend. Neither row's description becomes false, so there is no description successor either, as with I1-a's `schema_sources.rs` test and X4-F2.

## Lead rulings (Claude Opus 5.5, before sending)

- **I1-a's `fixturePath` observation** is left out of I1-b1. That is confirmed: policy admission never reads it, no law sets its replacement, and the bytes belong to I1-a's accepted record. It goes to the next unit that edits `atom-registry.json`, or to a record-maintenance follow-up.
- **Product main has moved** from `0765f8c` to `b7b87b7` (X4-F3, J2a and E2a). None of them touches `crates/evaluator`, so integration rebases.

## Decide

- **Faithfulness:** does the diff implement item 2.2 exactly, each conjunct in the policy pass and every conjunct whose operand a program carries in the program pass, with `POLICY.UNKNOWN_RULE` on any violation and row 4 with `PackDefect::RuleLaw` for a bundled document? Is the source-kind check replaced for this op only, with every other op's path unchanged? Does it do nothing I1-b2 (semantics, `atoms.rs`, `composition.rs`) or I1-c (the row, the document, the flipped tests) owns?
- **Tests:** does test 1 show "a test pack using the op admits", and tests 2 and 3 "each violation is row 4 with `PackDefect::RuleLaw`" and the program pass? Are the controls (other ops unchanged, `n` as a schema refusal) and the mutation check sufficient? Is any violation missing?
- **Rerun the lanes above,** each cargo lane under the lane lock: fmt (with `rustfmt --edition 2024 --check` on the `#[path]` test module), the workspace build, the three clippy lanes, the workspace tests (twice if time allows), the doc tests, the crash-matrix feature lane, the drift check, plain `verify_design`, both package-edge lanes against v136, and both dependency checkers with their suites. Optionally rerun the targeted tests with `cargo test -p opensip-evaluator --lib -- pack_tests::cycle_representative`.
- **I1A-NB-1:** do you agree it is outside I1-b1, and with the routing?
- **Judgment calls:** are calls 1 to 7 acceptable? Answer the questions in 1, 3 and 5 directly.

Write REVIEW.md and review.json under the output directory. review.json needs:
- `"verdict"`: `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`;
- `"subjectSha256"`: `4371f9dfa2aba740747ac5ea887fa95b0ec53acac2305196f9f920725d13e822`, the diff's sha256, as a single string.

No `subjectManifestSha256`, `inventoryCandidateAssessment` or `review-contract.json` is needed: the unit has no inventory or design selection. Do not commit.
