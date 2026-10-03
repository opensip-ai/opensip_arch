Codex review: unit L1 r1, the product licence (Apache-2.0, owner decision D14), with inventory v134 on v133. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT-UNIT**, with an `inventoryCandidateAssessment`.

**Rules:**
- No repository edits, commits, pushes or delegation.
- Write only under /tmp/opensip-implementation/reviews/codex-licence-l1-r1.
- You own the native lane for this review:
  - Use a CARGO_TARGET_DIR under that directory.
  - Use a private 0700 TMPDIR under `$(getconf DARWIN_USER_TEMP_DIR)`, because other worktrees churn the shared temp folder.
  - Run cargo `--locked --offline`.
- Run git read-only, and only against the worktree named below.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.

## Inputs

All inputs are pinned in `hashes.txt`.

### Decision

- **D14** (`docs/implementation/m3/analysis-quality/PLAN.md`, decided 2026-10-03): the owner chose Apache-2.0. T3 waits for the unit that lands the product licence, which is this one.
- **The licence text:** arch's root `LICENSE`, the canonical apache.org text: 11358 bytes, sha256 `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30`.

### Product

- **Worktree:** `/Users/sb/code/opensip-ai/opensip-l1`, detached at main `91cb45a` (X9-4 integrated). Nothing is committed. The new `LICENSE` is intent-to-add, so `git diff 91cb45a` includes it.
- **Diff:** `git diff 91cb45a` is 18165 bytes, sha256 `d2b605ef4c852681b1c977de92fb94150ae3aa9e027b14739bbbf25e3f26d7aa`. It covers 18 files, +224 −4.
- **Toolchain:** `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin`, Python `python3.14`, Node 24.16.0 at `~/.nvm/versions/node/v24.16.0`.

### Inventory

- `repository-file-inventory.v134.json` (candidate; parent v133, which the lock at `91cb45a` selects);
- `licence-l1-inventory-v134/`;
- `licence-l1-inventory-v134-subject.json`, sha256 `04659e4758ec5c6ddac525948606c8dd96c3aae099c4d8e06bd08b75b6a4946c`;
- `licence-l1-inventory-v134-unit.json`, a draft the lead completes at integration.

They are untracked in arch.

## What L1 changes

| File | Change |
|---|---|
| `LICENSE` (new) | Byte-identical copy of arch's `LICENSE` (sha above) |
| `apps/cli`, `crates/{contracts,evaluator,host,identity,lifecycle,platform,reporting,security,storage}`, `providers/rust`: `Cargo.toml` (11) | `license = "Apache-2.0"` on the line after `publish = false` in `[package]`, in each manifest's own spacing (`license="Apache-2.0"` in the compact evaluator, security and storage manifests) |
| `package.json`, `apps/report/package.json`, `providers/typescript/package.json` | `"license": "Apache-2.0",` after `"private": true,`, two-space indent kept |
| `README.md` | A `## Licence` section at the end: "OpenSIP is licensed under the [Apache License, Version 2.0](LICENSE)." |
| `tools/contracts/dependency-policy.json` | `localSources` row `Cargo.toml` (crates/contracts): 250 → 273 bytes, `6bd8e0bd…` → `c9831759…` |
| `tools/identity/dependency-policy.json` | `localSources` row `Cargo.toml` (crates/identity): 750 → 773 bytes, `876739b9…` → `8fec4be9…` |

Nothing else changes. `Cargo.lock` doesn't change, because the field is metadata. The npm lockfiles, `design-lock.json` and every generated file are unchanged.

## Pins checked

- **verify_design and design-lock.json** pin no manifest, README or root file.
- **Feature and source pins:** a `license` key in `[package]` satisfies all three.
  - X10's pin (`apps/cli/tests/doctor_tests.rs`): no `[features]` text in cli and reporting, and only `crash-matrix` and `scenario-fixtures` keys in the `[features]` tables of host, security and storage.
  - X8's `feature_pin` (`crates/host/tests/admission_tests.rs`) checks only `scenario-fixtures`.
  - X9's `manifest_mentions` (`crates/platform/src/crash_matrix_tests.rs`) checks only `crash-matrix`.

  No Rust test pins `Cargo.toml` bytes.
- **Hash pins in the product tree:** a `git grep` for every changed file's old sha256 finds none left after the two policy edits.
- **Excluded tooling manifests** (judgment call 1):
  - `tools/contracts/generator-closure.json` (selected by contract successor `existing-root-diagnostics-468a`) pins `tools/contracts/{Cargo.toml,package.json,package-lock.json}`.
  - `tools/contracts/build-receipt.json` (selected by `native-repin-selection-v1`; an observed generator build) pins `tools/contracts/Cargo.toml`.
  - `tools/typescript-lanes.json` (selected by `typescript-closure-selection-v2`) pins `tools/typescript-boundary/{package.json,package-lock.json}`.

  `generate_contracts.py` and `check_typescript.py` each refuse a registry that no accepted design unit selects. The closure sha also appears in `schemas/registry.json` and in each generated module's header.

## Lead results

All checks ran on `91cb45a` with this diff and a private 0700 TMPDIR.

| Check | Result |
|---|---|
| `cargo test --workspace --all-targets --no-fail-fast` | 1726 passed, 0 failed, 3 ignored |
| `cargo test -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets --no-fail-fast` | 1621 passed, 0 failed, 3 ignored, including storage's `commit_tests` (6) and host's `commit_matrix_tests` (4) without a run set |
| Clippy `-D warnings`: workspace; the four crates with `crash-matrix`; security, storage and host with `scenario-fixtures` | Clean |
| `cargo fmt --all --check` | Clean |
| `providers/rust` (own workspace): `cargo test`, clippy `-D warnings`, `fmt --check` | Clean (0 tests) |
| `check_package_edges.py --lane host` against v134 | Passed |
| `tools/tests/`: `test_package_edges` (14), `test_check_crash_matrix` (18), `test_typescript_check` (3) | OK |
| `verify_design.py --architecture ../opensip_arch --implementation .` with the lock unchanged | Passed: v133 selected, 93 inventory and 75 contract successors, 55 inheritance rows, 40 generation and 48 admission sources |
| `evidence/verify_scratch.py` (v134 selected in memory) | Passed: 94 inventory successors, 75 contract successors, 55 inheritance rows, v134 selected |
| `verify_projection.py` against the lock at `91cb45a` | PASS, 55 rows, 278 corruptions refused |
| `evidence/build_v134.py` rerun | Same bytes |

**npm lockfiles (unchanged).** `npm ci --offline --ignore-scripts --no-audit --no-fund` ran with `~/opensip-deps/npm-cache` and empty user and global configs:
- **`providers/typescript`** (licensed `package.json`, unchanged lock): installed. In a scratch copy, the same lock with `typescript` changed to 6.0.2 refuses with `EUSAGE` ("can only install packages when your package.json and package-lock.json … are in sync"). So the sync check runs, and it accepts the `license` field.
- **`tools/contracts`** (unchanged): installed.
- **`apps/report`** and **`tools/typescript-boundary`**: `ENOTCACHED` for `esbuild-0.28.2.tgz`. It is absent from this Mac's cache, and the base `apps/report/package.json` fails identically. The lanes do not fetch substitutes.

**Not runnable here, and the same at base:**
- **`check_typescript.py`:** the boundary checker needs `tools/typescript-boundary/node_modules` with esbuild, which can't be provisioned (see above).
- **`generate_contracts.py` drift check:** it refuses "input digest mismatch: tools/verify_design.py". The closure pins the 33654-byte `verify_design.py` from before VD1 (`96dd114`). L1 touches neither file.
- **`check_dependencies.py` and `check_identity_dependencies.py`, and their tests:** both refuse on stale rows L1 doesn't touch.
  - Contracts: `src/generated/evidence.rs`, regenerated at `f482f98`.
  - Identity: the source census adds six files, and `src/lib.rs` and `src/schema_registry.rs` changed.

  The two test suites fail identically on `91cb45a` and on this diff:
  - `test_dependency_policy`: 2 failures and 2 errors;
  - `test_identity_dependencies`: 2 failures and 1 error.

  With a scratch copy of the contracts policy whose `evidence.rs` row is refreshed, `check_dependencies.py --feature-profile security-crypto-workspace` passes on this diff. Every `localSources` row other than those named stale above matches, including both `Cargo.toml` rows.

## Inventory v134

- **Contents:** v133 plus one row, `LICENSE`. The row is package `repository`, role `documentation`, not generated, standing `proposed`. That gives 968 files, with 967 rows equal by value. There is no new edge; the `repository` package declares none.
- **Projection:** 55 rows, `supersessionsFolded: 0`. Only selectors after the inserted row move.
- **Pins:**
  - candidate: 552176 bytes, sha256 `626cd71996d79de5c0efd914438dd65b3123e701e774ccdad1f8f9681466c58a`;
  - successor record (`licence-l1-inventory-v134/successor.json`): 145062 bytes, sha256 `8193a7d22ca4fa07540a42616b1af7015a45b24d5d5873d64793fee126a37986`;
  - parent v133: 551621 bytes, sha256 `36ffd87a7cadb8b551e2c9e1816160a68fd0df42339f2595bb5644b015f775e1`.
- **The lock:** at `91cb45a` it is byte-identical to `8dcfe37`'s, so it still selects v133.

## Judgment calls

1. **Three tooling manifests are excluded (lead decision, option A, 2026-10-03).**
   - **Which:** `tools/contracts/Cargo.toml`, `tools/contracts/package.json` and `tools/typescript-boundary/package.json` keep their bytes and get no `license` field.
   - **Why:** they are private, `publish = false` tooling outside the product graph, and the root `LICENSE` covers the whole repository.
   - **When they get it:** with the next generator-closure or lane-registry successor, which will happen for other reasons.
   - **Rejected, option B:** a design successor plus a generator rebuild now. For metadata alone that costs a full review cycle and changes nothing in the product.
   - **Recorded:** a one-line "L1 follow-up" bullet in `EXIT-PLAN.md`, uncommitted.
2. **The field is set per crate.** The workspace has no `[workspace.package]`. `providers/rust` is a separate workspace but a product crate, so it counts, for 11 manifests.
3. **Placement.** In each Cargo manifest, `license` goes after `publish`. In each `package.json`, it goes after `private`. Each file keeps its own spacing.
4. **The dependency policies are edited by hand.**
   - **Why by hand:** no generator writes them, and no live check pins either policy file. Arch's older baselines quote their previous hashes only as history.
   - **What changed:** only the `Cargo.toml` rows. The stale rows named under Lead results are left alone, because they are outside L1.
5. **The npm lockfiles are unchanged.** npm would copy `license` into a lock's `packages[""]` on the next `npm install`. `npm ci` accepts the mismatch (see Lead results). Two of the locks are pinned by the closure and the lane registry, and option A leaves their `package.json` alone anyway.
6. **LICENSE is intent-to-add** (`git add -N`), so the subject diff includes it. Nothing is staged otherwise.
7. **The "candidate selected" check is `verify_scratch.py`.** It is the in-memory form of what the integration script does to the lock (append the successor, re-project the inheritance), with a synthetic review and assent. The CLI ran with the unchanged lock.
8. **No crash-matrix lead sets were run.** The change is metadata only. The matrix targets still compile and pass their plain tests under the feature lane.

## Decide

- **Faithfulness:** does L1 adopt Apache-2.0 faithfully and nothing more? That covers the byte-identical `LICENSE`, the 11 crates, the 3 `package.json` files and the README section.
- **Pins:** confirm, or refute, the pin analysis:
  - no feature, source, lock or design pin is disturbed;
  - the two policy edits are exact;
  - the three exclusions are forced by design-selected pins.
- **Rerun:** run the lanes above yourself: the workspace, the feature lane, clippy, fmt, the provider workspace, `check_package_edges` against v134, `verify_projection.py` and `evidence/verify_scratch.py`. Also confirm `npm ci --offline` on `providers/typescript`.
- **Judgment calls:** are calls 1 to 8 acceptable?
- **Inventory v134:** pin it, and assess it as an inventory candidate.

Write REVIEW.md and review.json under the output directory. review.json needs:
- "verdict": ACCEPT-UNIT or REQUIRED-FINDINGS;
- "requiredFindings";
- "subjectSha256": `d2b605ef4c852681b1c977de92fb94150ae3aa9e027b14739bbbf25e3f26d7aa`, the diff's sha256, as a single string;
- "subjectManifestSha256": `04659e4758ec5c6ddac525948606c8dd96c3aae099c4d8e06bd08b75b6a4946c`, as a single string;
- "inventoryCandidateAssessment": verdict, requiredFindings, the candidate's path, bytes and sha256, parent (v133's pin), and successorRecord (the pin of `licence-l1-inventory-v134/successor.json`).

Do not commit.
