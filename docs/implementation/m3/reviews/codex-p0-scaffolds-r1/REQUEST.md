Codex review: unit M3-P0 r1, the package scaffolds, with inventory v135 on v134. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT-UNIT**, with an `inventoryCandidateAssessment`.

**Rules:**
- No repository edits, commits, pushes or delegation.
- Write only under /tmp/opensip-implementation/reviews/codex-p0-scaffolds-r1.
- You own the native lane for this review:
  - Use a CARGO_TARGET_DIR under that directory.
  - Use a private 0700 TMPDIR under `$(getconf DARWIN_USER_TEMP_DIR)`, because other worktrees churn the shared temp folder.
  - Run cargo `--locked --offline`.
- Run git read-only, and only against the worktree named below.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.
- No crash-matrix lead run set is needed or wanted (see "Pins checked", X9).

## Inputs

All inputs are pinned in `hashes.txt`. Laws and plans are pinned by their accepted snapshots.

### Plan and laws

- **The unit:** `docs/implementation/m3/M3-PLAN-r6.md:208` (accepted r6), the M3-P0 row: `crates/components` and `crates/syntax` (CH14:284, CH14:288) as members; the provider source layout; dependency-policy rows, including MC item 12's inflater row; one inventory successor; both dependency checkers in its Python lanes (M2C §5 row 20, `M2-COMPLETE-r3.md:408`). "Unblocked now: P0" is at :425.
- **What each law leaves to P0, and what it keeps:**
  - M3-C r7 (`snapshot-plan-c/PROPOSAL-r7.md`): item 12, CRATE-ARCHIVE-1 rule 1, "The inflater is a pure-Rust one (a P0 dependency-policy row)" (:560); the rejected `tar`-crate reader, "A first-party decoder with a pure-Rust inflater is a P0 dependency-policy row" (:663); the P0 gate (:1067); C3a consumes "P0's inflater row" (:1089); `imports.rs` lives in `crates/host` (:519).
  - M3-D r3 (`supervisor-d/PROPOSAL-r3.md`): "M3-P0 creates it" (:100, :1074). The modules go to D2a, D2b, D3a, D3b and D4 (:1140-1147). A general CBOR crate is rejected, so it needs no row (:347).
  - M3-E1 r3 (`syntax-e/PROPOSAL-r3.md`): "P0 creates `crates/syntax` as a workspace member" (:5). The crate is pure (BP:676-683). Its modules go to E2b and E2c (item 20, :708-712). SYN-DEP, `tools/syntax/dependency-policy.json`, belongs to E2b (:695). LP-1, the lead licence allowlist (:698).
  - M3-B r2 (`config-discovery-b/PROPOSAL-r2.md:457`): the `pnpm-workspace.yaml` reader is "chosen in B2-d under M3-P0's dependency policy".
  - The O1 row (`M3-PLAN-r6.md:221`): `tracing` arrives with O1, not P0.
- **Architecture:** CH14 (`docs/v2/architecture/14-repository-and-module-layout.md`): package rows :284 and :288; module lists :368-379 (syntax) and :426-436 (components); providers :502-543; "This is a planning inventory, not an instruction to create empty files" (:305). BP (`implementation-boundaries-and-build-plan.md`): :618-624 (lanes), :676-683 (the pure syntax owner).
- **Since phase 1:** E0's report was accepted (arch `e07f4d049`, `syntax-e/E0-REPORT.md`): **T-native**. It bears on judgment call 5.

### Product

- **Worktree:** `/Users/sb/code/opensip-ai/opensip-p0`, detached at main `cd5958b` (I1-P bound). Nothing is committed. The new files are intent-to-add, so `git diff cd5958b` includes them.
- **Diff:** `git diff cd5958b` is 284261 bytes, sha256 `637ab18a2971942fa4e8bda9bbf022a9c41ebfe3c9def5a0e592ed19fdc28f6b`. It covers 8 files, +885 −183 (the staged `design-lock.json` is +749 −182 of that).
- **Toolchain:** `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin`, Python `python3.14`.

### Inventory

All under `docs/implementation/m2/`, untracked in arch:
- `repository-file-inventory.v135.json` (candidate; parent v134, which the lock at `cd5958b` selects);
- `m3-p0-scaffolds-inventory-v135/` (README, builder, lock stager, scratch verifier, projection verifier and its outputs, verifier anchor, successor record);
- `m3-p0-scaffolds-inventory-v135-subject.json`, sha256 `844d0e18c927c1f8f0863d33e61e9a0fdba1b282112608d55f2c3e003096ad2b`;
- `m3-p0-scaffolds-inventory-v135-unit.json`, a draft the lead completes at integration.

## What P0 changes

| File | Change |
|---|---|
| `Cargo.toml` | `members` gains `"crates/components"` and `"crates/syntax"`. `exclude` is unchanged. |
| `Cargo.lock` | Two path-package entries, `opensip-components` and `opensip-syntax`, each with no dependencies. No registry package changes. |
| `crates/syntax/Cargo.toml` (new) | `opensip-syntax`, in the house `[package]` style with `license = "Apache-2.0"` and `[lib] path`. An empty `[dependencies]` table, with a comment naming the permitted edges. `[lints.rust] unsafe_code = "forbid"` (judgment call 5). |
| `crates/syntax/src/lib.rs` (new) | Doc comment only: the crate's role, its scaffold status, E1 r3 item 20's module owners, and its purity. No module, item or `use`. |
| `crates/components/Cargo.toml` (new) | `opensip-components`, same style. An empty `[dependencies]` table with its comment. No lint table. |
| `crates/components/src/lib.rs` (new) | Doc comment only: role, scaffold status, D r3's module owners. Nothing spawns, launches or admits. |
| `tools/host/dependency-policy.json` (new) | The host-workspace selection policy (judgment call 1). Rows: miniz_oxide 0.9.1 and adler2 2.0.1, selected and not linked. |
| `design-lock.json` | The staged inventory135 binding (see "The staged lock"). |

Nothing else changes. No crate gains a dependency or a source module. The provider trees, every generated file, every npm lock and every X9 source are unchanged.

### The dependency-policy rows

`tools/host/dependency-policy.json` is a **selection** policy for the host workspace (the root Cargo workspace; the same sense as `check_package_edges.py --lane host`). A row selects an external crate ahead of linking. It links nothing: no manifest names either crate, and `Cargo.lock` has neither. The unit that links a row (here C3a) declares the crate exactly as the row says, only in the named consumer, and adds the closure check. Any other version, feature set or consumer is a reviewed row change. The workspace's existing dependencies keep their own owners.

| Row | miniz_oxide | adler2 |
|---|---|---|
| Version and checksum | 0.9.1, `b63fbc4a…4b4c` | 2.0.1, `320119579f…abefa` |
| Archive | 70,519 bytes | 13,366 bytes |
| Licence | MIT OR Zlib OR Apache-2.0 | 0BSD OR MIT OR Apache-2.0 |
| Declaration | `miniz_oxide = { version = "=0.9.1", default-features = false }` | none: only through miniz_oxide |
| Resolved features | `[]` | `[]` |
| Build script, links | `build = false`; none | `build = false`; none |
| Unsafe | `#![forbid(unsafe_code)]`, `src/lib.rs:25` | `#![forbid(unsafe_code)]`, `src/lib.rs:16` |
| Inactive optional deps | alloc, core, serde, simd-adler32 | core |

**Evidence (lead).** Both archives were fetched from `static.crates.io` into the lead's scratch directory. Each one's SHA-256 equals the crates.io sparse-index `cksum` for that version, which is what `Cargo.lock` records. `~/.cargo` was not touched, so neither archive is in the offline registry. The facts above come from the extracted `Cargo.toml` and `src/lib.rs`. With no features, miniz_oxide compiles `inflate::core` and `inflate::stream` but not `deflate` or the allocating helpers (`src/lib.rs:28-33`, `src/inflate/mod.rs:3-12`, `src/inflate/stream.rs:120-143`).

**Selection rule** (in the file): the newest non-yanked crates.io release on 2026-10-04 that is pure Rust (no build script, no `links`, no C or assembly), declares `#![forbid(unsafe_code)]`, and offers a licence inside E1 r3's LP-1 lead allowlist. miniz_oxide's role is raw DEFLATE only. The gzip member, header fields, CRC-32, `ISIZE` and the D1 to D4 decoder counters stay first-party (C r7 item 12).

**Rejected, recorded in the row:** flate2 (its gzip reader owns member and header handling that rule 1 must enforce itself); zlib-rs 0.6.8 (pure Rust, but the crate does not forbid unsafe code and `src/inflate.rs` uses it); C zlib (C in the host); a first-party inflater (C r7 item 12 selects a crate by row).

### The staged lock

The lock change is staged in the worktree, as F8b staged its binding (`m2/reviews/grok-generator-closure-f8b-unit-r1/REQUEST.md`, deviation 6). `evidence/stage_lock_v135.py` writes HEAD's `design-lock.json` plus:
- one `inventorySuccessors` entry: parent v134, candidate v135, record `m3-p0-scaffolds-inventory-v135/successor.json`, all real pins; review `SCRATCH-P0/review.json` (760 bytes, `f8732289…1792`) and assent `SCRATCH-P0/assent.json` (615 bytes, `2011f5e3…dff4`), placeholders;
- `inventoryPassageInheritance` replaced by the one hundred rows re-parented to v135, exactly as the record projects them.

The lock has no separate selected-inventory field: selection is the last inventory successor. The file stays in the lock's canonical formatting (`json.dumps(indent=2, ensure_ascii=True)` plus a newline). The staged lock is 496,918 bytes, sha256 `ede33788b2e1c7e9dc86c0ad6996dcf7b88ee4fe8f415134bbaf6f6243a07b35`.

The placeholder bytes are those of `evidence/verify_scratch.py`'s synthetic overlay. At integration, the lead:
1. copies your review in;
2. completes the unit record;
3. replaces exactly the two placeholder pins with the real `review.json` and unit-record pins;
4. runs plain `verify_design`;
5. commits.

**Plain `verify_design` on the staged lock refuses,** with "missing or escaping regular file: SCRATCH-P0/review.json", as F8b's did. That is correct until review. `verify_scratch.py` asserts this refusal.

**`design-lock.json` stays outside the unit's `sourceBoundary`,** as in every earlier inventory unit (L1's v134 record, for one). Integration changes its bytes when it replaces the two placeholders, so a pin of the staged bytes would be stale at once. Its staged bytes are pinned here, and the diff sha covers them.

## Pins checked

- **X9.** P0 touches no crash-matrix source, fixture, required-runs file or `tools/check_crash_matrix.py`, and no crate code that any crash-matrix row exercises. X9's manifest pin (`crates/platform/src/crash_matrix_tests.rs:240-257` and `:268`, `cargo_files` and `manifest_mentions`) reads every `Cargo.toml` in the repository tree. X8's `feature_pin` test (`crates/host/tests/admission_tests.rs:1489`) reads every workspace member's manifest through `cargo metadata`, so it covers both new manifests. Neither mentions either feature. Both pins pass in the workspace lane, so no lead run set is needed.
- **Dependency policies.** Neither scaffold has a dependency, and `Cargo.lock` gains only path packages, so feature unification and both registry closures are unchanged. Both checkers and their suites pass (Lead results).
- **Package edges.** `opensip-syntax` and `opensip-components`, with their permitted edges, are already package rows of v134. Neither crate declares an edge.
- **Generators and lanes.** `tools/host/` is outside the generator closure, which is a selected pin list, and outside the TypeScript lane registry.

## Lead results

All lanes ran serially on `cd5958b` with this diff (the staged lock included), a private 0700 TMPDIR and `--locked --offline`. `~/Library/Application Support/OpenSIP` was absent before and after.

| Check | Result |
|---|---|
| `cargo fmt --all --check` | Clean |
| `cargo build --workspace --all-targets` | Pass (cold target directory) |
| Clippy `-D warnings`, workspace `--all-targets` | Clean |
| Clippy `-D warnings`, platform, security, storage and host with `crash-matrix` | Clean |
| Clippy `-D warnings`, security, storage and host with `scenario-fixtures` | Clean. Fully cached from the workspace lane, whose test targets already unify `scenario-fixtures` through the dev-dependencies. |
| `cargo test --workspace --all-targets --no-fail-fast`, run 1 | 1731 passed, 0 failed, 3 ignored (20 test binaries, including the empty `opensip_components` and `opensip_syntax` unit binaries) |
| The same, run 2 | 1731 passed, 0 failed, 3 ignored |
| `cargo test --workspace --doc` (reconciliation) | 18 passed. With the 1731, that gives the 1749/0/3 of the lead's confirmation lane on `15c0779`. |
| `cargo test -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets --no-fail-fast` | 1629 passed, 0 failed, 3 ignored. Includes storage's `commit_tests` (8) and host's `commit_matrix_tests` (5), without a run set. |
| `evidence/verify_scratch.py` (staged mode) | Passes. Inventory successors 94 → 95 with v135 selected; 82 contract successors; inheritance 55 → 100, equal to verify_design's own projection; 21 supersessions unchanged. Plain verify_design refuses the staged lock at `SCRATCH-P0/review.json`, as asserted. |
| Plain `verify_design.py --architecture ../opensip_arch --implementation .` on the staged lock | Refuses: "missing or escaping regular file: SCRATCH-P0/review.json" (exit 1). Correct until integration. |
| Plain `verify_design.py` on the unstaged lock (phase 1, same product sources) | Passes: v134 selected, 94 inventory and 82 contract successors, 55 inheritance rows, 21 supersessions, 40 generation and 48 admission sources |
| `verify_projection.py` against the real lock at `cd5958b` | PASS: 100 rows, 503 corruptions refused |
| `evidence/build_v135.py` rerun | Same bytes |
| `check_package_edges.py --lane host`, against v135 and against v134 | Both pass: 12 workspace packages (with `opensip-components` and `opensip-syntax`), 22 declared and 20 resolved internal edges, none new |
| `check_package_edges.py --lane rust-provider` against v135 | Passes: `opensip-rust-provider` only |
| `tools/tests/test_package_edges.py` | 14 run, OK |
| `check_dependencies.py --feature-profile security-crypto-workspace` | Passes: 11 dependencies, 8 local sources |
| `check_identity_dependencies.py` | Passes: 8 dependencies, 305 sources |
| `tools/tests/test_dependency_policy.py` | 9 run, OK |
| `tools/tests/test_identity_dependencies.py` | 5 run, OK |

Commands, from the worktree, with `PY=/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14`, `CARGO=/opt/homebrew/Cellar/rust/1.95.0/bin/cargo`, `AR=~/.cargo/registry/cache/index.crates.io-1949cf8c6b5b557f` and `U=../opensip_arch/docs/implementation/m2/m3-p0-scaffolds-inventory-v135`:

```sh
cargo fmt --all --check
cargo build --workspace --all-targets --locked --offline
cargo clippy --workspace --all-targets --locked --offline -- -D warnings
cargo clippy -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets --locked --offline -- -D warnings
cargo clippy -p opensip-security -p opensip-storage -p opensip-host --features scenario-fixtures --all-targets --locked --offline -- -D warnings
cargo test --workspace --all-targets --no-fail-fast --locked --offline   # twice
cargo test -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets --no-fail-fast --locked --offline
nice -n 19 $PY -I -B $U/evidence/verify_scratch.py .
nice -n 19 $PY -I -B tools/verify_design.py --architecture ../opensip_arch --implementation .   # refuses at SCRATCH-P0
cargo metadata --locked --offline --format-version 1 > host.json
(cd providers/rust && cargo metadata --locked --offline --format-version 1) > provider.json
nice -n 19 $PY -I -B tools/check_package_edges.py --repository . --metadata host.json --inventory ../opensip_arch/docs/implementation/m2/repository-file-inventory.v135.json --lane host
nice -n 19 $PY -I -B tools/check_package_edges.py --repository . --metadata provider.json --inventory ../opensip_arch/docs/implementation/m2/repository-file-inventory.v135.json --lane rust-provider
nice -n 19 $PY -I -B tools/tests/test_package_edges.py -v
nice -n 19 $PY -I -B tools/check_dependencies.py --manifest Cargo.toml --target aarch64-apple-darwin --cargo $CARGO --feature-profile security-crypto-workspace
nice -n 19 $PY -I -B tools/check_identity_dependencies.py --manifest Cargo.toml --target aarch64-apple-darwin --cargo $CARGO --archives $AR --policy tools/identity/dependency-policy.json
nice -n 19 $PY -I -B tools/tests/test_dependency_policy.py --target aarch64-apple-darwin --cargo $CARGO -v
nice -n 19 $PY -I -B tools/tests/test_identity_dependencies.py --target aarch64-apple-darwin --cargo $CARGO --archives $AR -v
```

`verify_projection.py` ran against the real lock at `cd5958b` (the product checkout's, unstaged): `$PY -I -B $U/verify_projection.py --architecture ../opensip_arch --lock ../opensip/design-lock.json`.

## Inventory v135

- **Contents:** v134 plus one row, `tools/host/dependency-policy.json`: package `tooling`, role `registry`, not generated, standing `proposed`. That gives 969 files, with 968 rows equal by value. The packages, their edges and the pending decisions are unchanged; the `tooling` package declares no edge.
- **Planned rows realized or changed, by value unchanged:** `crates/{components,syntax}/{Cargo.toml,src/lib.rs}` (new bytes), `Cargo.toml` and `Cargo.lock` (changed bytes). Each row's description stays true of a scaffold. Check this, especially `crates/syntax/src/lib.rs` ("Expose pure parsing/normalization over immutable admitted inputs; no unchecked Coverage or authoritative finding constructors"), which today exposes nothing.
- **Projection: one hundred rows,** 55 + 45, with 17 supersessions folded:
  - the fifty-five inheritance rows bound to v134;
  - contract successor D3's forty-five direct overrides on v134 (`description-batch-d3/successor.json`), which become inherited once v134 is an ancestor;
  - D3's seventeen supersessions on v134, each naming an inherited row's current meaning and folded into it (law VD1).

  No other bound contract successor has a passage on v134. One projected selector moves, by one: `tools/tests/test_check_crash_matrix.py`, the only projected row sorted after the inserted path.
- **Pins:**
  - candidate: 553173 bytes, sha256 `ac66ee3bd75ace8f21e3122daacfdb2619fe8bb8a432b083414c14cbe3a0c887`;
  - successor record (`m3-p0-scaffolds-inventory-v135/successor.json`): 304648 bytes, sha256 `326cf1a253ab65ba0265305804a5ea43bc0185d8074855b09498c6edd2d25e00`;
  - parent v134: 552176 bytes, sha256 `626cd71996d79de5c0efd914438dd65b3123e701e774ccdad1f8f9681466c58a`.
- **Order:** the lock at `cd5958b` selects v134. Since L1's `2967905`, ten commits have landed (X9-6, D3, F8a, F8b, I1-L, B-S1, B-S2, B-S9, X4-F1 and I1-P), none with an inventory successor.

## Judgment calls

The lead accepted all seven as lead decisions (overnight log). Questions 1, 2 and 5 are where a reviewer could most reasonably differ.

1. **The inflater row's home and shape.**
   - **Decision:** a new host-workspace *selection* policy, `tools/host/dependency-policy.json`, whose rows select without linking. C3a, which writes `imports.rs`, links the crate.
   - **Why:** C r7 item 12 makes the inflater "a P0 dependency-policy row", and B r2:457 expects a "M3-P0's dependency policy" that B2-d can add to. The existing policies are closure policies for one subject package each (contracts, identity). E's SYN-DEP gets its own file under `tools/syntax/`, and the host's closure has no policy.
   - **Rejected:** linking the crate now (an unused dependency, and the archive is not in any reviewer's offline registry); a row in the contracts or identity policy (wrong subject package); a full host closure policy (well beyond scaffolding, with owners that differ).
   - **Question:** is a selection policy the right instrument? Are its fields and standing text clear about what it does not claim? Is the choice of miniz_oxide 0.9.1 with no features right?
2. **No checker for the selection policy in P0.** C3a adds the closure check when it links the rows. **Rejected:** a small check now that every row is absent from the host closure. **Question:** is an unchecked selection file acceptable until C3a?
3. **Provider source layout: no change.**
   - **Why:** the layout is in place. `providers/rust` is its own workspace, excluded from the host's (`Cargo.toml:4`; BP:618-624), with its own lock and toolchain. `providers/typescript` has its package, lock, `tsconfig.json` (`include: src/**/*.ts`) and the generated protocol. Every CH14:502-543 file is already a planned row, and CH14:305 says the inventory is "not an instruction to create empty files". F and G add their modules under these roots. The G2 sidecar's layout waits for S-P.
   - **Rejected:** placeholder provider modules; a provider lib/bin split now.
4. **No dependency edges and no modules at P0.**
   - **Why:** each edge and module arrives with the unit that uses it, within the inventory's permitted edges: syntax → contracts, identity; components → contracts, identity, platform; host → syntax (E3) and host → components (D and J).
   - **Rejected:** declaring the CH14 edges now (unused edges); empty module files.
5. **`unsafe_code = "forbid"` on `crates/syntax` only.**
   - **Why:** it matches the other pure crates (identity and evaluator use the same table). E1 r3:74 places T-native's C "through the `tree-sitter` crate and the grammar crates", so the C and its FFI glue sit in dependencies, not in this crate's code. Components has no lint table; the D units decide.
   - **Against:** E0 chose **T-native** after this decision was made. E0's own native harness compiled the grammar C with `cc` and declared it crate-locally (`e0-probe/harness/src/native.rs:10-27`: `extern "C"` and `unsafe { LanguageFn::from_raw(..) }`). If E2b follows that shape instead of grammar crates, it must lift the lint by a reviewed change.
   - **Question:** keep the lint, or drop it so that the scaffold decides nothing E2b owns?
6. **Rows not added:** `tracing` (O1); a CBOR crate (D r3:347 rejects it); the YAML reader (B2-d decides under this policy); `wasmi` and grammars (E2b's SYN-DEP); CRC-32 (first-party in C3a, or a later reviewed row).
7. **Placement and base.**
   - **Placement:** the inventory and its unit files sit in `docs/implementation/m2/`, beside the chain v1 to v134, under unit name `m3-p0-scaffolds-inventory-v135`. This request is in `m3/reviews/`.
   - **Base:** the worktree was cut at `15c0779` and moved to `cd5958b` when main advanced (I1-P's binding: `design-lock.json` only, no passage on v134). The v135 bytes are identical on either base.

## Decide

- **Faithfulness:** does P0 do what M3-PLAN-r6:208 asks, and nothing a later unit owns? That covers the workspace membership, the two scaffolds, the provider layout call, the inflater rows, and the one inventory successor.
- **The inflater selection:** check the two archives against the policy yourself (fetch from `static.crates.io`, or confirm the sparse-index `cksum`), along with the licence, `build = false`, the absence of `links` and the `forbid` line.
- **Rerun:** run the lanes above yourself: fmt, the workspace build, the three clippy lanes, the workspace tests (twice if time allows), the crash-matrix feature lane, `verify_scratch.py` (staged mode), plain `verify_design` (it must refuse at `SCRATCH-P0/review.json`), both package-edge lanes against v135, `verify_projection.py`, and both dependency checkers with their suites. Also rerun `evidence/build_v135.py` against `../opensip/design-lock.json` (it writes only its two untracked paths, so run it on a scratch copy of arch if you prefer) and confirm the same bytes.
- **Judgment calls:** are calls 1 to 7 acceptable? Answer questions 1, 2 and 5 directly.
- **Inventory v135:** pin it, and assess it as an inventory candidate.

Write REVIEW.md and review.json under the output directory. review.json needs:
- "verdict": ACCEPT-UNIT or REQUIRED-FINDINGS;
- "requiredFindings";
- "subjectSha256": `637ab18a2971942fa4e8bda9bbf022a9c41ebfe3c9def5a0e592ed19fdc28f6b`, the diff's sha256, as a single string;
- "subjectManifestSha256": `844d0e18c927c1f8f0863d33e61e9a0fdba1b282112608d55f2c3e003096ad2b`, as a single string;
- "inventoryCandidateAssessment": verdict, requiredFindings, the candidate's path, bytes and sha256, parent (v134's pin), and successorRecord (the pin of `m3-p0-scaffolds-inventory-v135/successor.json`).

Do not commit.
