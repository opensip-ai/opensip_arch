# Independent review: private publication corrections draft106 — Claude, r1

Reviewer: Claude (independent; Codex remains implementation owner). Date: 2026-09-18.
Scope, as requested: closure of my publication78/79/88 findings **M-1** (macOS fallback was not an `fsync`),
**T-1** (unpinned protections), **R78-1** (local-POSIX-filesystem condition), **M-2** (replacement resets
metadata) and **M-3** (staging namespace not reserved) in the single changed file
`crates/platform/src/filesystem.rs`; adjudication of the owner's surviving length-guard mutant.

**Not covered and not approved:** reference107 (separate subject), the rest of `filesystem.rs` inherited
from 105 — including `confirm_existing_regular` / `ExistingFileReceipt`, which is outside this delta and
which I have not reviewed — all other crates, Linux / musl / cross-target behaviour, power-loss or
hardware-fault qualification, dependency acceptance, custody, semantic publication, formal selection.

## Bounded verdict

**No blocking finding. M-1, T-1, R78-1, M-2 and M-3 are closed.** One nonblocking follow-up (N-1: the
production wiring of the fallback is still unpinned) and an agreement with the owner's equivalence ruling.

| Finding | Adjudication |
|---|---|
| **M-1** fallback re-issued `F_FULLFSYNC` | **Closed in source.** The fallback is now a direct `libc::fsync`, called once, reached only for `EINVAL` / `ENOTSUP` / `ENOTTY`. Reverting it to `File::sync_all` is **killed** by two tests. Not runtime-observable on this Mac, as the owner states and as I found in the previous review. |
| **T-1** unpinned protections | **Closed.** Native read-back, fallback errno filter, staging `O_EXCL` and the separate cleanup error are each now killed when removed. |
| **R78-1** local POSIX filesystem | **Closed as a named caller obligation** in the module contract. Correctly *not* claimed as enforced. |
| **M-2** metadata reset | **Closed by documentation**, accurately worded (new inode, requested `0600` subject to umask, old owner / ACL / xattrs / flags not copied, parent defaults may inherit). |
| **M-3** staging namespace | **Closed.** `.opensip-stage-` is refused as a publication target, a confirmation target and as **any component** of a read path; crash-leftover cleanup is assigned to fenced managed-state maintenance, explicitly not to readers. |
| Owner's surviving mutant (initial length guard) | **Agreed: equivalent under stable custody.** Details below; my own run adds that the *trailing-byte* guard is likewise individually redundant, and both-removed is killed. |

## Reviewed bytes (independently verified)

| Item | SHA-256 | Result |
|---|---|---|
| `trials/publication-corrections-draft-checkpoint-106/subject.tar.xz` | `4fcbe721fe2c2e48692d441d28fb5911f6e0bf253e9a0c7f2ab69a15bf41afc2` | = `archive-pin.json` |
| `subject.json` (387 members) | `aba52347e5b9ea368d1651918d06d62fc9b9365d568ad6319d1796b8a338bc38` | every member re-hashed from the tar **before** extraction |
| `product-inputs.json` | — | **330 / 330** product pins match; 0 unlisted |
| vs frozen105 product pins | — | **exactly 1 file changed** (`crates/platform/src/filesystem.rs`), 329 unchanged, 0 added, 0 removed |
| `filesystem-before106.rs` | — | byte-identical to frozen105's `filesystem.rs` |

0 symlinks / non-regular members / unsafe paths; extraction unchanged after all work; builds, probes and
mutants ran only in scratch copies. `Cargo.lock` is byte-identical to 105's, so the vendor set I verified
against lock checksums in the 105 review applies unchanged. **Owner tests reproduced: 28 passed.**

## The delta, adjudicated

### M-1 — fallback
```
sync_directory (macOS) = directory_barrier_with(parent, full_flush_directory, fsync_directory)
directory_barrier_with: full_flush ok            → FullFlush
                        EINVAL|ENOTSUP|ENOTTY    → fsync(parent)?  → Fsync     (one call, no retry)
                        any other error          → propagate
fsync_directory = libc::fsync(fd)        // comment: File::sync_all on Apple is F_FULLFSYNC
```
This is the right structure: the errno predicate is a pure function and the orchestration takes its two
syscalls as closures, so the table test can drive it. The test covers exactly the cases I asked for —
`EINVAL`, `ENOTSUP`, `ENOTTY` fall back; `EIO`, `ENOSPC`, `EINTR`, `EBADF` and an errno-less error do not;
a failing fallback is called once and its `EIO` is returned, not masked. Linux calls `fsync_directory`
directly. `DirectoryBarrier::Fsync` is now a truthful label.

### T-1 — seams
The native new-file path gained a private function-pointer seam on the **write only**
(`NativeNewPublication { write_staging }`, production constant `NATIVE_NEW_PUBLICATION`), so the
corruption / truncation / append tests now run through the real `verify_staged_bytes`, the real rename and
the real barriers. Two default trait methods (`staging_nonce`, `cleanup`) let a test force a staging-name
collision — proving `O_EXCL` refuses with `EEXIST` at `Prepare` and leaves the other file's bytes intact —
and force a cleanup failure, proving the primary `ENOSPC` and the cleanup `EIO` are reported separately and
visibility stays `Unchanged`. None of the seams is reachable from outside the module.

### R78-1, M-2, M-3 — contract text and prefix reservation
The module header now states each obligation in the terms I would have used, and does not overclaim: the
filesystem condition is "callers must bind", not "this module checks". The prefix is checked with
`starts_with` on the basename for publication and confirmation, and on **every path component** in
`open_regular`, so `dir/.opensip-stage-x/file` is refused as well as the leaf.

## Independent evidence

**Public-API probe re-run** (`rust-publication-probe-106.json`; the same integration test I wrote for
draft88, on APFS plus scratch FAT32 / exFAT / HFS+ images). Compared observation by observation with the 88
run, **exactly one behaviour changed**: a target named `.opensip-stage-0000…` was a RECEIPT on 88 and is now
`Prepare` / `Unchanged` / `InvalidInput`, and no staging-named file is left behind. Everything else is
identical, including the ones that matter most: 150 × 8 exclusive race → one winner every round; exFAT
exclusive rename → real `ENOTSUP`, refused with no fallback; real out-of-space on a 40 MiB volume →
`WriteTemporary` / `Unchanged` / `ENOSPC` with the old target intact; 3,000 replacements against a
symlink-flipping thread → the outside victim never modified; descriptor count 10 → 10.

**Mutation run** (`mutation.json`; 14 mutants, all applied and compiled, each against the crate's own tests
in a scratch tree): **10 killed, 4 survive.**

| Mutant | Result |
|---|---|
| fallback calls `File::sync_all` again (the M-1 regression) | **killed** (2 tests) |
| fallback retried after failure | **killed** |
| fallback widened to `EIO` | **killed** |
| fallback narrowed (drops `ENOTTY`) | **killed** |
| fallback result mislabelled `FullFlush` | **killed** |
| native read-back skipped | **killed** |
| staging `O_EXCL` removed | **killed** |
| cleanup error dropped | **killed** |
| prefix reservation removed — publication | **killed** |
| prefix reservation removed — read | **killed** |
| prefix reservation removed — confirmation | survives — **equivalent**: `confirm_existing_regular` calls `open_regular`, which refuses the prefix anyway |
| read-back: initial length check removed | survives — **equivalent under stable custody** (owner's case) |
| read-back: trailing-byte check removed | survives — **equivalent under stable custody** (mine) |
| **production passes `full_flush_directory` as the fallback closure** | **survives — N-1** |

### The length-guard equivalence — I agree with the owner, with one refinement
`verify_staged_bytes` has three guards: metadata length, `read_exact` per chunk, and a trailing one-byte
read. For a **static** file they overlap: truncation is caught by the length check *and* by `read_exact`
(`UnexpectedEof`); appended bytes are caught by the length check *and* by the trailing read. So removing
either outer guard alone changes only the error kind, never the refusal — I confirmed both single removals
survive and the owner confirmed both-removed is killed. Accepting `InvalidData | UnexpectedEof` in the test
rather than asserting a diagnostic string to force a kill is the honest choice, and the right one.

The refinement: the two guards are *not* equivalent when the file changes **during** verification. The
metadata check samples length once, before reading; only the trailing read observes growth that happens
after it. Under the stated custody assumption (a `0600` staging file this call created exclusively) that
cannot happen, which is why the mutants are equivalent in practice — but it is the reason to keep both, and
the module already does.

## Nonblocking follow-up

### N-1 — the production *wiring* of the fallback is unpinned
`directory_barrier_with` is fully tested, but the one line that supplies its arguments in production is not:
replacing `fsync_directory` with `full_flush_directory` in
`directory_barrier_with(parent, full_flush_directory, fsync_directory)` reintroduces exactly M-1 and passes
all 28 tests. That is inherent in making both syscalls parameters. Two cheap ways to close it: make only the
`full_flush` step injectable and have the function call `fsync_directory` itself, or add a test that the
production path's fallback is `fsync_directory` (e.g. compare function pointers through a small
`const NATIVE_DIRECTORY_BARRIER: (fn, fn)`). Low risk — it needs a deliberate edit to go wrong — but it is
the one place this correction could silently regress.

## Remaining, outside this verdict
1. **M-1 at run time.** Directory `F_FULLFSYNC` succeeded on every filesystem I could mount, in this review
   and the last. The fallback branch has therefore never executed against a real kernel refusal; the
   correction rests on source (`libc::fsync`) and on injected errnos. The owner says the same.
2. **M-4 / M-5 from my previous review** carry forward unchanged and are now stated in the module header:
   read-back is cache evidence, not media evidence; barriers are never retried. `renameat2` on a static-musl
   core is still unverified because nothing Linux was built or run.
3. **Inherited code.** `confirm_existing_regular` appeared between draft88 and 105. It opens read-only,
   verifies bytes, applies file and directory barriers and returns a receipt. It is outside this delta and I
   have not reviewed it; in particular I have not assessed what an `ExistingFileReceipt` is allowed to mean.
4. Reference107 (the stage law and the filesystem-admission prerequisite) is a separate subject.

## Commands and outcomes (all under `claude-out/`)

| Command | Outcome |
|---|---|
| `verify_extract.py` (before extraction; after all work) | 387 / 387 verified from tar; 0 unsafe; unchanged |
| product pin check / comparison with frozen105 | 330 / 330; exactly 1 file changed |
| `cargo test -p opensip-platform --offline --locked` (scratch) | 28 passed |
| `tests/claude_probe.rs` (scratch; APFS + 3 scratch disk images) | 49 observations; 1 intended change vs draft88 |
| `probes/mutation.py` | 14 mutants: 10 killed, 3 equivalent, 1 real (N-1) |

No probe failed this round. Scratch disk images were detached and deleted. Toolchain: Rust 1.95.0,
macOS aarch64.

## Limits
1. macOS only; no Linux code executed.
2. Real faults produced: out-of-space, unsupported exclusive rename, permission denied, deleted directory,
   over-long name. No `EIO`, no barrier failure, no power loss — those remain injected.
3. Review is of the 105→106 delta in one file; the rest of that file and the workspace is inherited.
4. No dependency, target, custody, semantic-publication or cumulative acceptance.
