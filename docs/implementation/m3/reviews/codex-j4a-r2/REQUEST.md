Codex review: unit J4a r2, the shared primitives of the resume/repair writer and their X3c and X3b uses. r2 answers your r1 finding **J4A-RF-01** (`m3/reviews/codex-j4a-r1/`, REQUIRED-FINDINGS) and rebases the unit onto product main `1d24900`. It implements accepted law J-RW r4 item 11's J4a row, through X3c r9 (RW-S3) and X3b r11 (RW-S4). Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT-UNIT** on the r2 diff. The unit still adds no file, so it has no inventory successor and no design selection.

**Rules:**
- No repository edits, commits, pushes or delegation.
- Write only under `/tmp/opensip-implementation/reviews/codex-j4a-r2`. If you build or test, use a `CARGO_TARGET_DIR` under that directory.
- Run git read-only, and only against the worktree named below.
- Several implementation agents share this machine. Take the lane lock before any cargo run: `LOCK="$(getconf DARWIN_USER_TEMP_DIR)opensip-lanes.lock"; mkdir "$LOCK"` (wait while it exists). Release it with `rmdir "$LOCK"` straight after, and only if your `mkdir` succeeded.
- Don't run a crash-matrix run set. None is needed: the X9 position is r1's (below).
- Run every command at `nice -n 19`, with a private 0700 `TMPDIR` under `$(getconf DARWIN_USER_TEMP_DIR)`, and cargo `--locked --offline`.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.

## r1, and what carries forward

Your r1 review (`codex-j4a-r1/review.json` and `REVIEW.md`, pinned) found one P2 item, J4A-RF-01, and answered the ten judgment calls. **Everything r1's request (`codex-j4a-r1/REQUEST.md`, pinned) describes stands unchanged in r2, except C-SUFFIX's final confirmation (below) and the base.** That covers the primitives' other parts, the three uses, the typed result, the scopes, the controls table and the stale descriptions.

**Your answers, carried as the lead's rulings:**
- **Calls 1 to 3, 5 to 7 and 10: accepted.** They cover:
  - the `project_ledger.rs` edit;
  - the four `.repair` names `x3c.ledger-create.projects.repair`, `x3c.ledger-create.namespace.repair`, `x3c.object.objects.repair` and `x3c.object.sha256.repair`;
  - an ACL-omitted length-0 ledger with a `-wal` keeping `Custody("private")`;
  - the typed result;
  - P-ACL observation failures;
  - `carrier-floors`' remaining steps;
  - RW-P2's `.repair` scope holding no durability point, so RW-K5's kill set is empty.
- **Call 4 (budget): accepted with RF-01's correction,** which r2 makes. C-SUFFIX's reservation now includes the final read-back.
- **Call 8: was RF-01.** It is now answered.
- **Call 9 and the integration constraints, unchanged:**
  - X3c-3 integrates first.
  - J4a's integration is held until X9 r17 §RW is accepted. It then lands in one commit with exactly the six RW-F00 storage re-transcriptions (`evidence/x9-rows.txt`) and a full storage lead set.
  - §RW records the four `.repair` names and RW-K5's empty kill set.
  - The three stale descriptions go to the next description batch.
  - After acceptance, the unit is rebased onto the integration base.

## J4A-RF-01 and the change

**The finding.** `complete_private_suffix` relied on `write_regular_suffix_reserved`'s byte read-back, which runs before the file barrier. After the parent's directory barrier it compared only device, inode and length. J-RW r4 item 3.2 (`PROPOSAL-r4.md:246`, the Action) orders the steps as:
1. the missing suffix write;
2. `F_FULLFSYNC`;
3. the directory barrier;
4. an exact-length capped read-back on the same device and inode.

Item 8 (`:514`) requires post-effect confirmations to be reserved.

**r2's C-SUFFIX** (`private_access.rs`, `complete_private_suffix` and its private `complete_private_suffix_with`). Steps 1 to 3 are unchanged. Step 4 is now:
1. a no-follow reopen of `name` under the retained parent;
2. a check that its device and inode are the written handle's, else `SuffixError::Confirm`;
3. the **capped read-back through that reopened, confirmed object** (`read_back_capped`).

**How the read-back works.** It uses one buffer of `expected.len() + 1` bytes. It makes positioned reads from offset zero, at most `SUFFIX_READBACK_CALLS` (4) of them, and stops at the end or at a full buffer. Only `Some(n)` with `n == expected.len()` and the buffer's first `n` bytes equal to `expected` confirms; that is, exactly the owner's bytes followed by the end. Every other result refuses:
- a longer file fills the buffer and returns `None`, so `Confirm`;
- a shorter or different file is `Confirm`;
- an unended read (calls exhausted) is `Confirm`;
- a failed read is `SuffixError::ConfirmIo`.

The length-only comparison is gone, because the read-back subsumes it.

**Reservation.** `suffix_cost` now adds `suffix_readback_cost(len)`: 1 object, 4 edges and `len + 1` bytes. The whole cost is still taken by one `work.effect` before C-ACL's first effect (or the suffix write's, when the ACL was private). The read-back spends it with `post.spend` before allocating its buffer.

**Unchanged:**
- platform's `write_new_regular_*` and `write_regular_suffix_*`, including the early verification inside the suffix write, which stays as a check before the barrier;
- `judge_private_prefix`, C-ACL, the three uses and every other file.

The private seam `complete_private_suffix_with(…, read_back)` takes `read_back_capped` in production, the platform's own "private seam" pattern. Tests replace it to change the file, or fail the read, at the confirmation point after both barriers.

## Subject

- **Worktree:** `/Users/sb/code/opensip-ai/opensip-j4a`, detached at product main `1d24900` (X4-F3). Nothing is committed or staged, and no file is added, removed or renamed.
- **The full r2 diff:** `git -C /Users/sb/code/opensip-ai/opensip-j4a diff 1d24900` is 137310 bytes, sha256 `9c6496aeaca917a489a9ac2bc997c424339f7169942a57559ce717cc0aa60461`. It covers the same 11 files as r1, +2826 −42. A copy is at `evidence/j4a-r2.diff`.
- **The base: r1's subject** (`4fbe89f1684846c70f1da639549669a31ee98775e526760f65bfcdede69f8bda`, `codex-j4a-r1/evidence/j4a.diff`).
  - `1d24900` changes none of J4a's files, so r1's diff applies to `1d24900` byte for byte. Before the fix, `git diff 1d24900` in the worktree had that same sha256.
- **The delta from r1 to r2:** only `crates/security/src/private_access.rs` changes, by 19949 bytes, sha256 `cda40970243b85efc1bf501db6da5000af7d2d7e72807b5cd93d843a098a0576`, in `evidence/r1-to-r2.diff`.
  - **To reproduce it:** write `1d24900`'s 11 files to a scratch tree and apply r1's `j4a.diff` there. Then `diff -u` each file against the worktree. Only `private_access.rs` differs.
- **What the delta does:**
  - C-SUFFIX, +100 −21, in the hunks at `@@ -781`, `-815`, `-855`, `-866` and `-879`:
    - `SuffixError`'s two confirmation variants are re-documented;
    - it adds `SUFFIX_READBACK_CALLS`, `suffix_readback_cost` and `read_back_capped`;
    - `suffix_cost` gains the read-back;
    - `complete_private_suffix` delegates to `_with`;
    - step 4 is replaced.
  - The test module, +195 −15, in the hunks at `@@ -2050` and after:
    - `suffixed` delegates to the new `suffixed_with`, which takes a read-back hook and returns the ledger's `used()`;
    - `an_unreservable_c_suffix_writes_nothing` is strengthened;
    - `c_suffix_reads_the_bytes_back_after_both_barriers` is added.
- **Toolchain:** as in r1.
- **Evidence:** `evidence/` here, every file pinned in `hashes.txt`:
  - `lanes.sh`, r1's script rebased onto `1d24900`, as run;
  - `lanes-summary.txt`, and `results.json` with its summarizer `results.py`;
  - `j4a-r2.diff` and `r1-to-r2.diff`;
  - `x9-rows.txt`, the six storage rows, unchanged at `1d24900`;
  - `parallel-files.txt`, the other worktrees' changed files and X4-F3's files.

## The rebase onto `1d24900`

`d2c00a9..1d24900` is five commits:
- four bind contracts only (REG v3, CRC-2, ENUM-1, SD-8), changing only `design-lock.json`;
- **X4-F3** (`1d24900`) changes `commit_authority.rs`, `custody/commit_session.rs`, `custody/operation_guard.rs`, `custody/operation_handoff.rs` and `revocation.rs`, with their tests, and `design-lock.json`.

**X4-F3 touches nothing J4a calls.** J4a's code calls into:
- `private_access`;
- platform's ACL, name, scan, write and barrier primitives;
- `store_custody`;
- `carrier_floor`'s floor step;
- `project_ledger`.

None of these changed. The one J4a-touched type X4-F3's files use is `OperationFloor`, and `operation_handoff.rs` still only calls `operation_floor_step` and passes the result on. X4-F3 changed that file's guard-start error mapping, not this call. The X9 harness sources and both `required-runs.v1.json` files are byte-identical at `d2c00a9` and `1d24900`, and so are the census pins' inputs on J4a's paths.

## Tests changed and added (C-SUFFIX only)

- **`c_suffix_reads_the_bytes_back_after_both_barriers` (new; RF-01's regression).** Each case starts from a private file holding a 5-byte prefix of `expected`. P-PREFIX is judged, then C-SUFFIX runs with a hook at the final read-back, which is after the suffix write, its early verification, `F_FULLFSYNC` and the parent's barrier.
  - **`changed`:** the hook overwrites byte 3 through a separate handle, then reads back natively. The early verification had already passed, so only the post-barrier read can see the change. The result is `Confirm`.
  - **`longer`:** the hook appends one byte. The end check gives `Confirm`.
  - **`shorter`:** the hook shrinks the file by one byte, giving `Confirm`.
  - **`failed`:** the hook's read returns an I/O error, giving `ConfirmIo`.
  - **`unended`:** the hook returns no end within the cap, giving `Confirm`.
  - **`intact`:** at the hook, the reopened object has the written handle's device and inode, the buffer is `expected.len() + 1` bytes, and the name already holds every byte. The hook runs exactly once, and the completion confirms.
  - **The native `read_back_capped`:** the end within the cap gives `Some(len)`; a full buffer gives `None`; an empty file gives `Some(0)`.
- **`an_unreservable_c_suffix_writes_nothing` (r1's RW-C12 test for C-SUFFIX, strengthened).** It runs for a private prefix and for an ACL-omitted empty file.
  - **The sum:** `suffix_cost` equals the sum of every step, which is C-ACL's sample, append and sample when omitted, the suffix write, the directory barrier, the reopen, two status reads and the read-back. `suffix_readback_cost` is pinned at 1 object, 4 edges and `len + 1` bytes.
  - **Short limits:** with one edge short, and with one byte short (the read-back buffer's last byte), the result is the budget row. The read-back hook never runs, the file keeps its length, and an omitted ACL stays omitted.
  - **Exact limits:** with exactly the reservation as the ledger's limit, the completion succeeds, the read-back runs once, and `used()` equals the reservation. So nothing, the final read included, is charged outside it.
- **No other test changes.** The workspace count is r1's 1760 plus this one new test.

## Lead results

All lanes ran serially on `1d24900` plus the r2 diff (`evidence/lanes.sh`). Each step took the shared lane lock and released it only if it had taken it. They ran at `nice -n 10`, with a private 0700 TMPDIR and `--locked --offline`. The diff's sha256 was `9c6496ae…` before and after the lanes. The real home was absent before and after. Summary: `evidence/lanes-summary.txt`; counts: `evidence/results.json`. Other units' lanes ran between J4a's locked steps.

| Check | Result |
|---|---|
| `cargo fmt --all --check` | Clean |
| `cargo build --workspace --all-targets` | Pass |
| Clippy `-D warnings`, workspace `--all-targets` | Clean |
| Clippy `-D warnings`, platform, security, storage and host with `crash-matrix` | Clean |
| Clippy `-D warnings`, security, storage and host with `scenario-fixtures` | Clean |
| `cargo test --workspace --all-targets --no-fail-fast`, run 1 | 1773 passed, 0 failed, 3 ignored (20 binaries). That is `1d24900`'s 1750 (r1's base of 1738 plus X4-F3's 12) plus J4a's 23 (r1's 22 plus RF-01's regression). |
| The same, run 2 | 1773 passed, 0 failed, 3 ignored |
| `cargo test --workspace --doc` | 20 passed |
| `cargo test -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets --no-fail-fast` | 1671 passed, 0 failed, 3 ignored. That is r1's 1658, plus X4-F3's 12, plus 1. Security's and storage's census pins, `every_test_feature_site_is_on_the_pinned_list` and `no_manifest_enables_the_crash_matrix_feature` pass. |
| `tools/generate_contracts.py` drift check | Passes: `passed: true`, 40 source schemas, 8 outputs, `changed: []` |
| `verify_design.py --architecture ../opensip_arch --implementation .` | Passes: v136 selected, 96 inventory and 101 contract successors, 100 inheritance rows, 21 inventory and 5 contract passage supersessions |
| `check_package_edges.py --lane host` against v136 | Passes: 22 declared and 20 resolved internal edges, none new |
| `check_package_edges.py --lane rust-provider` | Passes |
| `tools/tests/test_package_edges.py` | 14 run, OK |
| `check_dependencies.py --feature-profile security-crypto-workspace` | Passes: 11 dependencies, 8 local sources |
| `check_identity_dependencies.py` | Passes: 8 dependencies, 305 sources |
| `tools/tests/test_dependency_policy.py` | 9 run, OK |
| `tools/tests/test_identity_dependencies.py` | 5 run, OK |

**Main has moved since.** J2a (`174aa30`) and E2a (`b7b87b7`) integrated after the rebase. `1d24900..b7b87b7` changes no file under `crates/platform`, `crates/security` or `crates/storage`, no `required-runs.v1.json` and no crash-matrix checker. It changes only `crates/host`, `crates/syntax`, `tools/grammar`, `tools/README.md`, a tools test and `design-lock.json`. So r2's diff applies there unchanged. As r1's ruling says, the integration commit rebases it anyway.

## Decide

- **J4A-RF-01:** does r2 perform item 3.2's exact-length capped read-back after the suffix write, `F_FULLFSYNC` and the directory barrier, through the reopened object confirmed to be the written one by device and inode? Is that work reserved before the first effect, with `write_new_regular` unchanged and the early verification kept but not relied on? Does the regression establish the post-barrier byte check and its refusals, and do the budget cases cover the final confirmation before mutation?
- **Nothing else:** does the r1-to-r2 delta change only C-SUFFIX and its tests? Does the rebase onto `1d24900` change nothing J4a depends on?
- **Rerun:** run `evidence/lanes.sh`'s lanes yourself, with your own target directory, TMPDIR and output paths and the lane lock, or at least the platform, security and storage lib tests and the crash-matrix feature lane.

Write REVIEW.md and review.json under the output directory. review.json needs:
- `"verdict"`: `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`;
- `"subjectSha256"`: `9c6496aeaca917a489a9ac2bc997c424339f7169942a57559ce717cc0aa60461`, the r2 diff's sha256, as a single string.

No `subjectManifestSha256` or `inventoryCandidateAssessment` is needed: the unit adds no file. Do not commit.
