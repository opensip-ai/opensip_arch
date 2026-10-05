CODEX2 review: unit **I1-c** r1 of law M3-I1 r3 — the X12c preview pack's release row: `pack-registry.json`'s row and standing, the bundled document `crates/evaluator/src/preview-typescript-pack.v1.policy.json`, the `RELEASE_PACKS.documents` entry, the flipped X12a and X12b tests and the self-checks S1 to S9 — with **inventory v140**. Grok leads as of 2026-10-04 (Claude Opus 5.5 stopped on its weekly limit). You are the single reviewer. You accepted the law (r3), its design units I1-L and I1-P, and the two product units before this one, I1-a and I1-b1. Verdict wanted: **ACCEPT-UNIT** on the product change and inventory v140, with an **`inventoryCandidateAssessment`**. I1-c binds no design (I1-P is already bound), so it has **no contract successor** and needs no contract review file.

**Parent.** v140's parent is **v139**, unit J3a's candidate (`m2/durable-entry-j3a-inventory-v139/`, on v138, which the lock at `083ad5c` selects). J3a is reviewed separately and is not yet integrated. Until it integrates, every I1-c script applies J3a's staged entry in memory, from J3a's own `evidence/verify_scratch.py` with its `SCRATCH-J3A/` placeholders, and the I1-c worktree's staged lock carries that entry before I1-c's own. If J3a integrates before you review, the lead moves the worktree to that main, re-stages (I1-c's entry only), and refreshes the diff and lock pins below; the candidate, record and subject do not change as long as J3a's v139 bytes do not. **If J3a's v139 changes, or another inventory integrates first, v140 must be rebuilt and re-pinned.**

**Rules:**
- No repository edits, commits, pushes or delegation.
- Write only under `/tmp/opensip-implementation/reviews/codex2-i1c-r1`.
- You own the native lane for this review:
  - Use a `CARGO_TARGET_DIR` under that directory.
  - Use a private 0700 `TMPDIR` under `$(getconf DARWIN_USER_TEMP_DIR)`, because other worktrees churn the shared temp folder.
  - Run cargo `--locked --offline`.
  - Write every scratch output (metadata, drift directory, any scratch copy) under your output directory, never into either repository.
- **The generator is shared.** Before the drift gate, check by process name (`ps -Ao comm=`) that no other `opensip-contract-generator` is running.
- Run git read-only, and only against the worktree named below.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.
- No crash-matrix lead run set is needed or wanted (see "Pins checked", X9).

**Shared machine: the lane lock.** Other agents' lanes and X9 lead sets run on this machine under a 5000 ms timing guard, so cargo runs are serialized through one lock directory, `LOCK="$(getconf DARWIN_USER_TEMP_DIR)opensip-lanes.lock"`:
- **Take it** with `mkdir "$LOCK"` before every cargo build, test, clippy or metadata run, and release it with `rmdir "$LOCK"` straight after.
- **Release only a lock you took.** Track it with a flag set only when your own `mkdir` succeeded, and never `rmdir` on any other path (an unconditional exit trap can delete another agent's lock).
- **If it is held, wait in a background poll** (`until mkdir "$LOCK" 2>/dev/null; do sleep 2; done`). Keep the word `cargo` out of the waiting process's command line: put the cargo commands in a script file and run the script. Another agent's "is anything running" check matches command lines, and a waiter whose argv names cargo can block it.
- Never hold the lock while reading or editing. The Python-only lanes need no lock.

## Inputs

All inputs are pinned in `hashes.txt`. Laws are pinned by their accepted snapshots, never by a live `PROPOSAL.md`.

### Law and design parent

- **The law: M3-I1 r3** (`docs/implementation/m3/preview-pack-i1/PROPOSAL-r3.md`, 68025 bytes, `204f8ee8…`, your r3 ACCEPT in `reviews/codex2-preview-pack-i1-r3/`). The live `PROPOSAL.md` is these bytes plus the acceptance note.
  - **Item 5** (:321-397): 5.1 identity, 5.2 the document's bytes (:328-332), 5.3 the digests (:342-355), 5.4 the row (:357-363, "I1-c copies it"), 5.5 placement (:365-369: "the sole entry of `RELEASE_PACKS.documents` … under the name the row's `policyDocument` gives … one row and one document … Nothing is read at run time"), and **5.6, the self-checks S1 to S10** (:371-397).
  - **Item 7** (:415-421): X12 r3's "zero rows" become "exactly the one row", and NT-1's preview bullet becomes "that ID admits, and its variants stay row 1", effective when I1-c lands.
  - **LD-11** (:463): I1-c may land before I1-b2; evaluation still refuses the op structurally (`ATOM_OP`) until then.
  - **"Units after the law"** (:484): "I1-c: the row, the document and the self-checks S1 to S9. **(r3)** It copies I1-P's two data files, the registry file and the document, byte for byte."
  - **Forbidden substitutes** (:518, :532, :540): shipping with bytes other than 5.2's; a document whose bytes differ from its canonical bytes; any second release row.
- **The unit row:** `UNITS-r2.md` (`0c3c0f44…`, equal to the live `UNITS.md`), row I1-c (:33): the row and standing, the document, the `RELEASE_PACKS.documents` entry; "Flips the tests: `policy_pack_tests.rs:151-175`, `:580-600`, `:603-640` (the `include_bytes!(` count goes from 7 to 8); `crates/host/src/configuration_tests.rs:102-134`. Adds self-checks S1 to S9. Inventory successor." Edges: I1-b1 → I1-c (:37).
- **The design parent, I1-P** (your ACCEPT-DESIGN-UNIT in `reviews/codex2-i1-p-r2/`; bound at product `cd5958b`): `i1-p/README.md`, `pack-contract.json` (S1 to S10 and the pinned values), `materialization-map.json` (the two files I1-c ships, before and after), and the two product candidates under `i1-p/product/crates/evaluator/src/`.
- **X12 r3** (`m2/policy-admission-x12/PROPOSAL-r3.md`, `11628912…`): item 4 (:67), item 6 (:87-101), the `Supplied` refusal of bundled bytes (:92, :207), NT-1 (:160) and the release self-check (:169), the lines item 7 amends.
- **I1-b1's review** (`reviews/codex2-i1b1-r1/`, ACCEPT-UNIT, integrated at `083ad5c`) and **I1-a's review** (`reviews/codex2-i1a-r1/`, I1A-NB-1).

### Product

- **Worktree:** `/Users/sb/code/opensip-ai/opensip-i1c`, detached at main `083ad5c` (I1-b1: 101 contract successors and 5 contract passage supersessions, 98 inventory successors, v138 selected). Nothing is committed. The one new file is intent-to-add, so `git diff 083ad5c` includes it.
- **Diff:** `git diff 083ad5c` is 366473 bytes, sha256 `5f3e7716991a57074ac652c7e34200b18217e2236de8b59f33831a4e93e495e7`. It covers 6 files, +760 −448, of which the staged `design-lock.json` is +468 −414. A copy is at `evidence/i1c.diff`.
- **Provisioned trees:** the worktree also holds the ignored `tools/contracts/node_modules` and `tools/contracts/python-packages`, copied from the main checkout, for the drift gate.
- **Toolchain:** `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin`; Python `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14`; generator `~/opensip-deps/contracts-generator-rebuild-02/opensip-contract-generator`; Node `~/.nvm/versions/node/v24.16.0/bin/node`.

### Inventory (arch, untracked)

All under `docs/implementation/m2/`:
- `repository-file-inventory.v140.json` (candidate; parent v139);
- `preview-pack-i1c-inventory-v140/` (README, builder, lock stager, scratch verifier, drift gate, projection verifier and its outputs, verifier anchor, successor record);
- `preview-pack-i1c-inventory-v140-subject.json`, sha256 `238cb70f72af846fd379aa47c06788de71f4e6346c59d5401c77acefbb3bc3ca`;
- `preview-pack-i1c-inventory-v140-unit.json`, a DRAFT-PENDING-REVIEW record the lead completes at integration (not in the subject).
- **The parent, J3a's unit** (untracked, reviewed separately): `repository-file-inventory.v139.json`, `durable-entry-j3a-inventory-v139/` (its successor record, README, `evidence/verify_scratch.py` and `stage_lock_j3a.py`, which I1-c's scripts load) and `durable-entry-j3a-inventory-v139-subject.json`.

## What I1-c changes

| Product file | Before (`083ad5c`) | After | Change |
|---|---|---|---|
| `crates/evaluator/src/preview-typescript-pack.v1.policy.json` (new) | — | 574, `96675a5e…` | I1-P's candidate byte for byte, which is law item 5.2's block (no trailing newline) |
| `crates/evaluator/src/pack-registry.json` | 305, `f95eeef1…` | 679, `d08a85de…` | I1-P's candidate byte for byte: the one row of 5.4 and the standing I1-P fixes (LD-P1). Its `before` equals `materialization-map.json`'s. |
| `crates/evaluator/src/policy.rs` | 52669, `1282915f…` | 52972, `fd60e44c…` | `RELEASE_PACKS.documents` gains its one entry, `("preview-typescript-pack.v1.policy.json", include_bytes!("preview-typescript-pack.v1.policy.json"))`, and the const's doc comment says one row. Nothing else. |
| `crates/evaluator/src/policy_pack_tests.rs` | 40942, `3b9f3032…` | 49019, `52701733…` | The three flipped X12a tests, three new tests, the pinned constants, and comments (below) |
| `crates/host/src/configuration_tests.rs` | 17821, `8c38c802…` | 19677, `055658bd…` | The flipped X12b test, one new test, the pinned constants, `every_row`'s row-1 input (stop item 1), and comments |
| `design-lock.json` | 520396, `97097b51…` | 522447, `a2c555b2…` | Staged: J3a's v139 entry, then the v140 entry (see "The staged lock") |

No other file changes: no manifest, `Cargo.lock`, feature, schema, generated file, `atom-registry.json`, fixture, crash point or generator input. `configuration.rs` and the evaluator's public API are unchanged. Every byte of the two data files was copied from I1-P's candidates and checked against `materialization-map.json`'s `after` pins and the law's 5.2 block; none was retyped.

**What it does not do.** Evaluation still refuses the op (`atoms.rs`, `ATOM_OP`) until I1-b2 (LD-11). Admission compiles the program and `check_plan_pack` joins a Plan's digest; neither evaluates. No product path builds a Plan or calls `admit_policy_selection` outside its tests yet (C4a and J2 do that later). S10 is I1-b2's.

## Tests

`policy_pack_tests.rs` is `policy.rs`'s `cfg(test)` module. New constants hold the values I1-P pins (S5): `PREVIEW_ID`, `PREVIEW_DOCUMENT` (an independent `include_bytes!` of the file, in the test module), `PREVIEW_SHA` (`96675a5e…`), `PREVIEW_RULE_PROGRAM_DIGEST` (`8e8936af…`) and `PREVIEW_PROGRAM_SHA` (`e796f817…`). The host tests carry the same ID, document, policy digest and compiled-program digest.

### The flipped tests (the law's four ranges)

| Law range (at `2967905`; now) | Test | Before | After |
|---|---|---|---|
| `policy_pack_tests.rs:151-175` (now :164-209) | `nt1_wrong_pack_identity_is_not_bundled`, the DR-131 block | `…pack:1` itself is row 1 on both registries | `…pack:1` admits from `RELEASE_PACKS` and is row 1 in the test registry. Seventeen variants are row 1 on both: `:2`, the bare name, `:01`, `:+1`, `:`, three case variants, a trailing newline, a leading and a trailing space, a trailing NUL, `opensip.preview.typescript:1`, `opensip.preview.typescript`, two other names, and the test ID on the release registry. The first half of the test, over the test registry, is unchanged. |
| `:580-600` (now :612-648) | `release_registry_has_zero_rows_…` → `release_registry_has_one_row_and_every_row_passes_item_6` (S1, S3) | zero rows, empty documents table | exactly one row: packId, its document bytes, `policySha256`, contribution set `{opensip.preview.typescript}`; the documents table has one entry; the row admits by its ID. The test-registry half is unchanged. |
| `:603-640` (now :650-697) | `source_pin_release_build_holds_no_test_row_or_runtime_read` (S6) | `documents: &[]`; 7 `include_bytes!(` | the exact const text with its one document; `include_bytes!("pack-registry.json")` and `include_bytes!("preview-typescript-pack.v1.policy.json")` once each; neither data file names `opensip.test`; **8** `include_bytes!(`; `&RELEASE_PACKS` still exactly twice; `PackRegistry {` once; the forbidden strings and the `cfg(test)` module pin unchanged |
| `configuration_tests.rs:102-134` (now :111-145) | `nt1_wrong_pack_identity_is_row_1_with_the_presented_id` (S7, S9) | `…pack:1` is row 1 | `…pack:1` is removed from the list (it admits: next test); a trailing-space variant is added; every other entry, and the row-1 termination check, is unchanged |

### New tests

| Test | Self-checks | What it checks |
|---|---|---|
| `release_document_is_canonical_and_carries_the_pinned_digests` (evaluator) | S2, S3, S4, S5 | The file is its own canonical bytes, 574 bytes, no trailing newline, SHA-256 `PREVIEW_SHA`, equal to the row's `policySha256`; the documents table is exactly `[(name, file bytes)]`; each rule's `programDigest` is SHA-256(C(`emitWhen`)) and equals `8e8936af…`; through the **public** `admit_pack`: the packId, the policy digest, a 457-byte compiled program whose digest is `e796f817…` and whose `policyDigest` and `emitWhen` are the document's; the classifier finds no imperative member (step 6.2). |
| `nt1_the_release_documents_exact_bytes_supplied_are_row_2` (evaluator) | S7 | The release document's exact bytes, and with a newline, supplied by user or third party, are row 2 on both registries, with the digest subject. |
| `check_plan_pack_joins_the_release_pack_by_its_policy_digest` (evaluator) | S8 | Through the **public** `check_plan_pack`, a Plan naming `…pack:1` with `policyDigest` `96675a5e…` joins; zero, the test pack's digest, the rule's `programDigest` and the compiled program's digest are each `PLAN_POLICY_PACK_DIGEST`; `:2` is `PLAN_POLICY_PACK_NOT_BUNDLED`; two IDs are `PLAN_POLICY_PACK_COUNT`; the test registry does not bundle the release ID. Plans are derived from the existing synthetic Plan fixture, as X12a's test derives them. |
| `the_release_pack_is_admitted_by_its_exact_id` (host) | S9, S7 | `admit_policy_selection(&[Named(…pack:1)])` returns the evaluator's `AdmittedPack` with I1-P's policy and compiled-program digests; the release document's exact bytes supplied are row 2 with the `CONFIG.INVALID` termination. |

**Where each self-check is.** S1: `release_registry_has_one_row…`. S2, S4, S5: `release_document_is_canonical…`. S3: both of those (the release row admits through every step, and the public owner). S6: the source pin. S7: the flipped evaluator and host NT-1 tests and both row-2 tests. S8: `check_plan_pack_joins_the_release_pack…`. S9: `the_release_pack_is_admitted…`, with every other host test unchanged in expectation (stop item 1). S10 is I1-b2's (UNITS; LD-11).

**Which existing tests flip.** `evidence/flip-check.txt` runs the **base** test files (`083ad5c`) against I1-c's product bytes, in a scratch copy under the lane lock. Exactly six fail, three per crate. In the evaluator they are the law's three ranges (base :171, :583, :614). In the host one is the law's `:102-134`, and the other two, `every_row_maps_to_its_published_route_and_generated_members` and `rows_1_2_and_3a_emit_the_x12_0_remedy_byte_for_byte`, both panic in `refuse()`'s `unwrap_err` through `every_row()`'s row-1 input (stop item 1). Every other pack and configuration test passes on the base files.

### Comments outside the flipped ranges

No expectation changes, only text that the row makes false: the test module's header (it now names I1-c's tests); `check_plan_pack_joins_analysis_spec_and_policy_digest`'s "In M2 the release registry bundles nothing" (:877, now "does not bundle the test pack"; the assertion, the test ID on the release registry being `NOT_BUNDLED`, is unchanged); and in `configuration_tests.rs` the header's "which has zero rows" and `every_row`'s "(zero rows, pinned schema sources)".

## Stop-and-report items (lead rulings)

1. **`every_row`'s row-1 input, outside the law's flip ranges.** `configuration_tests.rs`'s `every_row()` (:284) builds row 1 as `named("opensip.preview.typescript.pack:1")`, whose helper calls `admit_policy_selection(…).unwrap_err()`. With the row shipped, that ID admits and the helper panics, which fails `every_row_maps_to_its_published_route_and_generated_members` and `rows_1_2_and_3a_emit_the_x12_0_remedy_byte_for_byte` (`evidence/flip-check.txt`). UNITS names only `:102-134` for the host. I1-c changes the **input** to `opensip.preview.typescript.pack:2`, another NT-1 variant. **No expected value changes:** both tests compute the subject from the refusal (`pack.subject()`), and row 1's class, exit, codes, detail, remedy and human rendering are asserted exactly as before. **Recommendation:** accept it as I1-c's. It is the minimal change that keeps row 1 exercised through the real release registry, and S9 itself asks that "every other host row is unchanged", which only holds if row 1's example input moves off the one ID that now admits. The rejected alternative, building row 1 directly as `PackRefusal::NotBundled` (as row 4 is), would stop exercising row 1 through admission. **Lead ruling (2026-10-04): accepted.** The row-1 example input moves to `opensip.preview.typescript.pack:2`. No expected value changes. The diff and its pins stay as written.
2. **Three inventory descriptions go out of date** (`pack-registry.json`, `policy_pack_tests.rs`, `configuration_tests.rs`; quoted in v140's README). An inventory successor carries rows by value, so they are left for the next description-only contract successor, as inventory88, 101, 106, 118, 122, 125, 129 and 133 left theirs; the README suggests replacement texts. `policy.rs`'s row stays true. **Recommendation:** follow that precedent; I1-c's law row asks for an inventory successor only, and an inventory successor cannot change an inherited row. **Lead ruling (2026-10-04): accepted.** The three descriptions stay inherited. The next description-only successor carries the replacement texts the v140 README suggests.

## I1A-NB-1: not taken up

I1-a's observation (`atom-registry.json:945-948`, `scannerIdentitySchema.fixturePath`) is routed to "the next unit that edits `atom-registry.json`". **I1-c does not edit `atom-registry.json`** (its bytes are I1-a's accepted candidate, `9aabc999…`, unchanged), so the observation stays open for that unit or a record-maintenance follow-up.

## The staged lock

The lock change is staged in the worktree, as E2a staged v138 on J2a's staged v137. `preview-pack-i1c-inventory-v140/evidence/stage_lock_i1c.py` writes HEAD's `design-lock.json` plus:
- J3a's `inventorySuccessors` entry for v139, exactly as J3a's `stage_lock_j3a.py` writes it in its own worktree (checked equal to `/Users/sb/code/opensip-ai/opensip-j3a/design-lock.json`'s), with its `SCRATCH-J3A/` review (762 bytes, `214a92d4…`) and assent (618 bytes, `1c87f89f…`) placeholders;
- I1-c's entry: parent v139, candidate v140, record `preview-pack-i1c-inventory-v140/successor.json`, all real pins. Its review `SCRATCH-I1C/review.json` (761 bytes, `552aab6b…`) and assent `SCRATCH-I1C/assent.json` (617 bytes, `a4a0b7d2…`) are placeholders;
- `inventoryPassageInheritance` replaced by the 103 rows re-parented to v140, exactly as the record projects them.

The staged lock is 522447 bytes, sha256 `a2c555b2f15edd701bb440be33e7025c568e228fffe1f350aade47553a42f957`, in the lock's canonical formatting; rerunning the stager reproduces it. At integration, after J3a's, the lead:
1. copies your review in, to `m3/reviews/codex2-i1c-r1/review.json`;
2. completes `preview-pack-i1c-inventory-v140-unit.json`;
3. re-stages I1-c's entry on the integrated lock and replaces exactly I1-c's two placeholder pins;
4. runs plain `verify_design`;
5. commits.

**Plain `verify_design` on the staged lock refuses** at the first placeholder, J3a's: "missing or escaping regular file: SCRATCH-J3A/review.json". That is correct until review, and `verify_scratch.py` asserts it. `design-lock.json` stays outside the unit's `sourceBoundary`, as in every inventory unit; its staged bytes are pinned here, and the diff sha covers them.

## Pins checked

- **X9: no harness source changes, so no run set.** The diff names no X9 harness source (`tools/check_crash_matrix.py` and its test, `crates/platform`, storage's and host's `tests/` with both `required-runs.v1.json`, `commit_tests.rs`, `commit_matrix_tests.rs`, security's crash-matrix census and sites, the `crash_matrix_support` modules) and no `Cargo.toml`. It adds no `crash_barrier!`, `crash_scope!`, clock sample, file write or `cfg(feature …)` site. The host's configuration tests also run in the crash-matrix feature lane, and pass there.
- **Dependency policies and package edges.** No manifest, lock, feature or edge changes. None of the five product files is pinned by `tools/contracts`, `tools/host` or `tools/identity`'s dependency policy, `tools/typescript-lanes.json` or `tools/check_crash_matrix.py`. `include_bytes!` reads a sibling file at compile time.
- **Generators.** No schema, generator input or TypeScript lane source changes. The drift gate passes with `changed: []`.
- **Inventory coverage.** Every file of the worktree, tracked or intent-to-add, is a v140 row.
- **No consumer of the old registry bytes.** `f95eeef1…` (the base `pack-registry.json`) appears in no product file, and in arch only in historical records (X12a's unit record `m2/policy-pack-x12a-inventory-v104-unit.json` and its review's `hashes.txt`) and as I1-P's `materialization-map.json` `before`. No product file, tool or test pins `pack-registry.json`'s bytes, and `verify_design` reads no materialization map.
- **Line references.** The law's `policy.rs` lines are from `2967905`; at `083ad5c` `RELEASE_PACKS` is at `policy.rs:750-756` after this change, and the include count assertion is at `policy_pack_tests.rs:695`.
- **Inputs.** All `hashes.txt` pins were rechecked against the files after the lanes.

## Lead results

Recorded from the lane logs under the Claude scratch `i1c-lanes/`, after the diff had settled at `5f3e7716…`. Home `~/Library/Application Support/OpenSIP` was absent before and after both phases. The diff sha was the same after the design phase.

- **fmt** exit 0 (1s). The log is empty, which is `cargo fmt --check` with nothing to print.
- **workspace build** exit 0. Incremental: `Finished dev profile in 0.04s`.
- **clippy `-D warnings`:** workspace exit 0 (21s), crash-matrix feature exit 0 (9s), scenario-fixtures exit 0.
- **workspace tests, twice:** each run 1795 passed, 0 failed, 3 ignored, 20 binaries. Doc tests: 20 passed, 0 failed, 12 binaries.
- **crash-matrix feature lane:** 1686 passed, 0 failed, 3 ignored, 10 binaries.
- **drift** exit 0, `changed: []`, 40 sources, 8 outputs.
- **verify_scratch** staged exit 0. **Plain verify_design** on the staged lock exit 1 with `missing or escaping regular file: SCRATCH-J3A/review.json` (expected). Plain verify_design on HEAD's lock exit 0.
- **package edges** exit 0. **dependency checkers** exit 0 (2s for the pair).

## Inventory v140

- **Contents:** v139 plus 1 row, `crates/evaluator/src/preview-typescript-pack.v1.policy.json` in package `opensip-evaluator`, role `registry`, not generated, standing `proposed` (judgment call 2). That gives 1012 files, with the 1011 v139 rows equal by value. The packages, their edges and the pending decisions are unchanged. Check the description against the file.
- **Planned rows changed, by value unchanged:** `pack-registry.json`, `policy.rs`, `policy_pack_tests.rs`, `configuration_tests.rs` (`plannedRowsChanged`). `policy.rs`'s row stays true; the other three go out of date (stop item 2).
- **Projection: 103 rows,** every meaning a lock selecting v139 binds to it, by stable file path: its 103 inheritance rows as v139 projected them (v138's, which are v136's 100 and the three direct overrides of `read-endpoint-x3a2-descriptions` on v136). No bound contract successor has a passage on v139, and no supersession is folded. One hundred projected rows, sorted after the inserted path, move. None of the five touched paths carries a bound meaning.
- **Pins:**
  - candidate: 584066 bytes, sha256 `9eebf35bd89cb76a631f416200d7f2ca654a8d6e6e5cfc8cf2ab81fcc30961de`;
  - successor record (`preview-pack-i1c-inventory-v140/successor.json`): 307873 bytes, sha256 `146e42e424a912540d1802cd768e17be348c52609c640e658eeb3d5d70e64e3a`;
  - parent v139 (J3a's candidate): 583181 bytes, sha256 `f3bf66a6584e4fd41cef228aee9062c97ff670228c5f919c27ccd4762ad3061c`.
- **Order:** the lock at `083ad5c` selects v138. J3a's v139 is the highest existing candidate, so the lead assigned I1-c v140 on it.

## Judgment calls

The lead takes each as a lead decision (2026-10-04). Calls 1 and 2 are where a reviewer could most reasonably differ.

1. **The self-checks' home.** S1 to S8 are evaluator tests in `policy_pack_tests.rs` beside the X12a tests they flip, and S9 is a host test in `configuration_tests.rs` beside X12b's; both are existing `cfg(test)` modules, so no file is added for tests. S3 and S5 run through the **public** owners (`admit_pack`, `check_plan_pack`) as well as `admit_from`, so the shipped `RELEASE_PACKS` is what is checked. S5 compares with literal constants equal to `pack-contract.json`'s pins, not with values recomputed by the code under test. **Question:** do the tests discharge S1 to S9 as item 5.6 states them?
2. **The new row's role and text.** Role `registry`, as for `pack-registry.json` and the evaluator's other embedded data (`body-registry.json`, `import-registry.json`); not `fixture`, which marks test-only bytes. Its description states what 5.2 to 5.5 fix and what the file never is.
3. **One document entry, written inline.** The documents table holds the tuple `(policyDocument name, include_bytes!(same name))`, so the name the row gives and the file compiled in cannot drift apart without the source pin failing. No helper constant is added, which keeps `PackRegistry {` and `&RELEASE_PACKS` counts unchanged (S6).
4. **The NT-1 variants are widened,** not just reduced by one: `:+1`, `:`, two more case variants, a trailing space and NUL, and two name truncations in the evaluator; a trailing space in the host. They are all row 1 under the unchanged byte-exact match; they make "its variants stay row 1" (item 7) explicit for the one real ID.
5. **No change to X12's record.** Item 7 says its three amendments "take effect when unit I1-c lands"; the law itself is the amending text, so X12's snapshot is not edited.

## Decide

- **Faithfulness:** are the two data files I1-P's candidates byte for byte (and so law 5.2's block and 5.4's row)? Is `RELEASE_PACKS.documents` the one entry 5.5 names, with nothing read at run time? Does the diff stay inside I1-c's row: nothing I1-b2 (semantics, S10), C4a or J2 owns?
- **Tests:** are the four flipped ranges flipped as the law assigns, and do the tests discharge S1 to S9? Is any self-check missing a case?
- **Stop items 1 and 2:** do you agree with the rulings?
- **Rerun the lanes above,** each cargo lane under the lane lock: fmt, the workspace build, the three clippy lanes, the workspace tests (twice if time allows), the doc tests, the crash-matrix feature lane, the drift gate (`drift_scratch_i1c.py`), `verify_scratch.py` in staged mode and plain `verify_design` (which must refuse at `SCRATCH-J3A/review.json`), `verify_projection.py`, both package-edge lanes against v140, and both dependency checkers with their suites. Optionally rerun the flip check on a scratch copy of your own.
- **I1A-NB-1:** do you agree it stays open?
- **Judgment calls:** are calls 1 to 5 acceptable? Answer the question in 1 directly.
- **Inventory v140:** pin it, and assess it as an inventory candidate.

Write REVIEW.md and review.json under the output directory.

review.json needs:
- `"verdict"`: `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`;
- `"subjectSha256"`: `5f3e7716991a57074ac652c7e34200b18217e2236de8b59f33831a4e93e495e7`, the diff's sha256, as a single string;
- `"subjectManifestSha256"`: `238cb70f72af846fd379aa47c06788de71f4e6346c59d5401c77acefbb3bc3ca`, as a single string;
- `"inventoryCandidateAssessment"`: verdict (`ACCEPT` or `REQUIRED-FINDINGS`), requiredFindings, the candidate's path, bytes and sha256, parent (v139's pin), and successorRecord (the pin of `preview-pack-i1c-inventory-v140/successor.json`).

No `review-contract.json` is needed: I1-c has no contract successor. Do not commit.
