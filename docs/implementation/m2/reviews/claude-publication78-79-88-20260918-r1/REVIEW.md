# Independent review: publication group — reference78, Rust draft79, Rust draft88 — Claude, r1

Reviewer: Claude (independent; Codex remains implementation owner). Date: 2026-09-18.
Scope: the phase-aware visibility / durability law of reference78 and its conditional mechanism
implementation in private Rust drafts 79 (retained-directory replacement) and 88 (exclusive new-file
publication, which supersedes 79's `filesystem.rs`).

**Not covered and not approved:** unrelated inherited Rust (locks, clock, ACL observation, identity,
security), custody / fencing / root selection (caller obligations by design), semantic publication or digest
acceptance, Linux runtime behaviour (source only — nothing Linux was executed), power-loss or hardware-fault
qualification (none of my faults are that either), dependency / target qualification, formal selection.
A mechanism receipt is not custody, not a commit, not authority.

## Bounded verdicts

| Subject | Verdict |
|---|---|
| **Reference78** — phase-aware failure law | **Correct, and the selected-contract mismatch it reports is real: adopt it.** One condition must be written into the law (R78-1: it holds only on a local POSIX filesystem). |
| **Draft79** — replacement mechanism | **No blocking finding.** Behaviour matched the law under real races, real out-of-space and adversarial names. Findings M-1 (macOS fallback is not an `fsync`) and M-2 (replacement silently resets mode) apply. |
| **Draft88** — exclusive new-file mechanism | **No blocking finding in behaviour; changes required in its tests before it is relied on.** The exclusive-rename and no-fallback claims held on four real filesystems and under an 8-way race. But two of its headline protections — the staging read-back and the "EIO cannot be hidden by fallback" rule — are **not pinned by any test** (T-1): removing them passes all 22. |

## Reviewed bytes (independently verified)

| Item | SHA-256 | Members |
|---|---|---|
| `trials/publication-reference-78/subject.tar.xz` | `a42f64e3d295d71ae2a4818174d6e7af60718a8869e6ddee7ef59b7aeeed0f17` | 15 |
| 78 `subject.json` | `4bbb2b95c30bf30e0944a42f60f84abe6b447dc3cd7cc46d6d401e942ce15933` | |
| `trials/publication-draft-checkpoint-79/subject.tar.xz` | `45578bf2c00120c02127d0735d37b228c848ff73f992139734b161bf9daffdda` | 357 |
| 79 `subject.json` | `472e6d50889f7d06e7fcaa6a28472ab8054d74e0c508c223dbd4b9ae29ff20fa` | |
| `trials/new-publication-draft-checkpoint-88/subject.tar.xz` | `b41df2454130da08279fa94111958fd4e6371b2f56982dc3c3d8b7d90a6ec711` | 360 |
| 88 `subject.json` | `60d2ec6caec4f7268edbeb2ecbb65e1194f442c94ca819b20f623c8ecea3e4c8` | |

Every member re-hashed from the tar stream against its manifest and the archive against its pin **before**
extraction; 0 symlinks / non-regular members / unsafe paths. All three extractions re-verified
byte-identical after all work. Builds, probes and mutants ran only in scratch copies
(`claude-out/build79`, `build88`, per-mutant temp trees, all removed). Dependencies: all 40 registry packages
in 88's `Cargo.lock` are satisfied by the vendor directory I verified archive-by-archive against
`Cargo.lock` checksums in my crypto59/62 review (`libc 0.2.189` = `3eaf3ede…`, `getrandom 0.4.3` =
`300e883d…`); builds were `--offline --locked`.

Owner tests reproduced in my scratch builds: **79 → 11 passed; 88 → 22 passed.**

---

# Part 1 — Reference78: adjudication of the selected-contract mismatch

**The retained owner (security-completion v8 §5.6) says:** "Before visibility (`ENOSPC`, `EDQUOT`, `EIO`,
`EROFS`, short write, failed rename): no partial state; the previous durable state is retained by the
temp-then-rename pattern."

**POSIX says** (the source 78 cites, `rename()`): if `rename()` fails *for any reason other than `[EIO]`*,
any file named by `new` shall be unaffected. So for a failed rename with `EIO` the standard explicitly
withholds the guarantee v8 asserts. 78's two synthetic traces (`rename-eio-probes.json`) show both target
outcomes are lawful after a rename `EIO`; v8 would report "previous durable state retained" and
`reconcile: null` for both, which is wrong for one of them.

**Adjudication: 78 is right and v8 §5.6 is over-broad on exactly this point.** The proposal is also
correctly *narrow*: it does not make every `EIO` indeterminate — an `EIO` while writing or syncing the
private staging file leaves the target untouched, because the target has not been named yet. The rule is
about the **stage**, with errno only distinguishing the rename case. I checked `publication_reference.py`
line by line against that statement:

- `sync-directory` → always indeterminate (the replacement already happened);
- `rename` → indeterminate unless a **captured non-EIO errno** is present (`ENOSPC`, `EDQUOT`, `EROFS`,
  `OTHER_NON_EIO`); `EIO`, `UNKNOWN` and the errno-less labels are indeterminate;
- earlier stages → unchanged; `retryWithoutReconcile` only for `ENOSPC`/`EDQUOT` and never when uncertain;
- staging cleanup always separate; D9 unchanged (`operational-failed` / 4 / `HOST.IO_FAILURE`), existing
  detail codes reused — no public vocabulary minted.

The preserved before-image is a genuine catch: the first draft treated the errno-less `RENAME_FAILED` label
as "known non-EIO". A label that has *lost* the errno proves nothing, and the freeze correctly inverts the
test to an allow-list of captured errnos.

### R78-1 (medium) — the "captured non-EIO errno ⇒ unchanged" rule is only true on a local POSIX filesystem
The POSIX guarantee is a property of the filesystem, not of the errno. Network filesystems break it in the
other direction: a rename can be applied by the server while the client reports a **non-EIO** error (a lost
reply followed by a non-idempotent retry surfaces as `ENOENT`/`ESTALE`/timeout). On such a volume a
"known non-EIO" errno does not establish an unchanged target, and neither 78 nor drafts 79/88 check or state
the filesystem. Platform admission does restrict the *install root* to apfs/ext4/xfs/btrfs, but nothing
binds a `RetainedDirectory` to an admitted filesystem. Required: state in the law that the unchanged-target
conclusion is conditional on a retained directory on an admitted local filesystem, and make that a named
caller obligation beside custody (or check `f_fstypename` at handle admission).

### R78-2 (low) — three smaller points
(a) The model accepts stage/error pairs that cannot occur (e.g. `write-temp` + `RENAME_FAILED`); harmless
because every such pair resolves conservatively, but 315 cases therefore include impossible ones.
(b) The contract paragraph says the macOS fallback is allowed "only for a captured unsupported-operation
response" without naming the errnos; draft79 picks `EINVAL | ENOTSUP | ENOTTY`. Name them in the law.
(c) "No receipt until the required barriers succeed" says nothing about *what the barrier proves*: on macOS
`F_FULLFSYNC` asks the drive to flush; whether the device honours it is outside this mechanism. The
paragraph's closing disclaimer covers this; I note it so "receipt" is never read as "on stable media".

---

# Part 2 — Drafts 79 and 88: mechanism

## What the code does (read in full: `filesystem.rs` l.1-181, 305-578, and the test modules)

`replace_with(name, bytes, ops)`: basename check → `fstatat(AT_SYMLINK_NOFOLLOW)` and refuse unless regular
or absent → 16 bytes from the OS CSPRNG → `openat(O_RDWR|O_CREAT|O_EXCL|O_NOFOLLOW|O_CLOEXEC, 0600)` of
`.opensip-stage-<32 hex>` in the **same** retained directory → write → file barrier → rename → mark staging
unlinked → directory barrier → receipt. Any error is wrapped by `publication_failure(stage, error)`, which
derives visibility from the stage and, at `Rename`, from `raw_os_error()` (`n > 0 && n != EIO`). Staging is
unlinked on every failure path and its error is carried separately in `cleanup_error`. 88 adds
`NativeNewPublication`: write + full read-back compare, then `renameatx_np(RENAME_EXCL)` on macOS /
`renameat2(RENAME_NOREPLACE)` on Linux, with no fallback.

**Errno provenance is sound.** Every FFI call is followed immediately by `io::Error::last_os_error()` with no
intervening call; synthetic errors (`InvalidInput`, `InvalidData`, `WriteZero`) carry no OS errno and so are
"unknown" — indeterminate at `Rename`, unchanged earlier — which is the conservative direction at the only
stage where it matters. **Receipts are constructed in exactly one place, after the directory barrier
returns `Ok`.** **Handle ownership:** each `openat` result is wrapped in `File` on the next line; my probe
measured open descriptors before and after 1,200 mixed success/failure calls: **10 → 10**.

**Bindings checked against the pinned `libc 0.2.189` source:** `F_FULLFSYNC = 51`,
`RENAME_EXCL = 0x4` (`c_uint`), `renameatx_np` declared for Apple; `RENAME_NOREPLACE = 1` and `renameat2`
declared for Linux gnu **and musl**. The preserved compile failure (variadic `mode` must be `c_uint`) is
correctly fixed.

## Independent probe — public API only, real filesystem effects (`rust-publication-probe.json`)

An integration test added to the **scratch** crate, using only exported items. I mounted scratch FAT32,
exFAT and HFS+ disk images besides APFS to get real filesystem diversity.

| Claim tested | Result |
|---|---|
| Exclusive publish, 4 filesystems | APFS / FAT32 / HFS+: receipt, `FullFlush`, no staging left. **exFAT: `renameatx_np` returns `ENOTSUP` (45) → refused at `Rename`, `Unchanged`, nothing published, no staging left, no fallback.** A *real* unsupported-exclusive-rename, not an injected one. |
| `EEXIST` is not evidence | Publishing identical bytes over an existing file: `Rename` / `Unchanged` / errno 17 — no receipt. (On exFAT: `ENOTSUP`.) |
| Exclusive race | 150 rounds × 8 threads, distinct 70 KB bodies: **exactly one winner in all 150 rounds**; published bytes are always the winner's complete body; every loser is `Rename` / `Unchanged` / `EEXIST`; 0 staging files left. |
| Concurrent replacement | 6 threads × 60 replacements: final content is one whole input; 0 staging left. |
| Symlink TOCTOU | 3,000 replacements against a thread flipping the target between a regular file and a symlink to a file *outside* the directory (3,428 flips): 1,576 succeeded, 1,424 refused at `Prepare`, **the outside victim was never modified** — `renameat` replaces the link, it never follows it. |
| Names | `""`, `.`, `..`, `a/b`, `a\b`, embedded NUL → `Prepare` / `Unchanged`; 300-byte name → `ENAMETOOLONG` at `Prepare`; replace *and* new over a directory or a symlink → refused at `Prepare`. |
| Retained handle | Directory renamed after the handle was taken → publication follows the handle, not the path. Directory deleted → `Prepare` / `ENOENT`. Read-only directory → `Prepare` / `EACCES`, target intact. |
| **Real out-of-space** | 64 MiB into a 40 MiB HFS+ volume: `WriteTemporary` / `Unchanged` / `ENOSPC` (28), existing target intact, staging removed — for both replacement and exclusive publish. |
| Hard links | Replacing a hard-linked target leaves the other link with the old bytes (rename semantics; the module header already lists hard links as a caller concern). |

Every one of these agrees with the law. None of it is power-loss or hardware-fault evidence.

## Findings

### T-1 (changes required in tests) — two of draft88's stated protections are unpinned
Mutation run, 15 mutants of `filesystem.rs`, each built and run against the crate's own tests in a scratch
tree (`mutation.json`; all 15 compiled). **10 killed, 5 survive:**

| Surviving mutant | Why it matters |
|---|---|
| **staging read-back skipped** in `NativeNewPublication::write` | README: "full staging readback … staging corruption/truncation … tested." The tests exercise corruption through a separate `FaultOps` double that calls the verifier itself; nothing checks that the *native* path calls it. Deleting the call passes all 22 tests. |
| **read-back ignores length** | same cause |
| **macOS directory fallback widened to `EIO`** | The contract's central sentence — "device I/O errors cannot be hidden by falling back" — has no test. There is no injection seam below `PublicationOps::sync_directory`, so the errno filter is unreachable from tests. |
| staging `O_EXCL` removed | unpinned; only reachable with injected entropy |
| `cleanup_error` dropped | "cleanup outcome is separate" is asserted only as `is_none()` on success paths |

Killed, with named tests: `EIO` at rename treated as known; lost errno treated as unchanged;
directory-barrier failure reported unchanged; receipt despite directory-barrier failure; file barrier
skipped; exclusive rename replaced by plain rename; staging mode 0666; target-kind check removed; target
stat following symlinks; staging not cleaned on failure. So the *law* is well pinned; the two newer
mechanisms are not. Required: route the native read-back through a seam a test can corrupt (or test the
native ops against a file the test truncates between write and verify), and factor the fallback errno
predicate into a pure function with a table test including `EIO`, `ENOSPC`, `EINTR`.

### M-1 (medium) — on macOS the "fsync fallback" is not an `fsync`
`sync_directory` falls back to `parent.sync_all()`. In the pinned toolchain's standard library
(`library/std/src/sys/fs/unix.rs` l.1381-1392, Rust 1.95.0) `File::sync_all` on `target_vendor = "apple"`
**is `fcntl(fd, F_FULLFSYNC)`**, not `fsync(2)`. So after `F_FULLFSYNC` fails with an unsupported-operation
errno, the fallback issues `F_FULLFSYNC` again; it fails again; and the publication ends
`SyncDirectory` / `Indeterminate` **after a successful rename**. Consequences: the contract's allowed
fallback is not implemented, `DirectoryBarrier::Fsync` cannot truthfully be returned on macOS, and a volume
that really lacks directory `F_FULLFSYNC` would make *every* publication indeterminate. The failure is in
the safe direction (no false receipt). I could not observe it at run time: directory `F_FULLFSYNC`
succeeded on all four filesystems I could mount (`fullfsync-by-filesystem.json`), so this is established
from source, not from execution. Fix: call `libc::fsync` directly in the fallback. (Linux is unaffected:
there `sync_all` is `fsync`.)

### M-2 (medium) — replacement silently resets permissions and metadata
The staging file is created `0600` and renamed over the target, so a `0644` target becomes `0600` on
APFS/HFS+ (measured; FAT/exFAT report their fixed `0700`). Ownership, ACLs, extended attributes and flags
of the old target are likewise dropped. For private state files this is probably what is wanted, but it is
undocumented, and the same crate carries ACL-observation code — a caller that observed a target's ACL and
then "replaces" it will get a different object. Either state "the published file always has mode 0600 and
no inherited metadata" as part of the primitive's contract, or take the mode as a parameter.

### M-3 (low) — the staging namespace is not reserved
`.opensip-stage-<32 hex>` is accepted as a *target* name (my probe got a receipt), `open_regular` will open
a staging file by name, and a name containing a newline is accepted. A collision needs a 2⁻¹²⁸ guess, so
this is not an attack; but any future sweeper that deletes `.opensip-stage-*` would delete a published
file, and nothing sweeps today: a crash between create and rename leaves the staging file forever (128-bit
names never collide, so they only accumulate). Reserve the prefix (refuse it as a target and in
`open_regular`) and name the owner of crash-leftover cleanup.

### M-4 (low) — the read-back verifies the page cache, not the medium
`verify_staged_bytes` reads the file back **before** the file barrier, so it compares against what the
kernel cached from the same process a moment earlier. It catches a short write or a concurrent writer to the
staging inode; it cannot catch media corruption. The README's "full staging readback" is accurate; I note
the limit so it is never cited as integrity evidence — consistent with the request's "not content or
durability evidence".

### M-5 (low, Linux, unexecuted) — two things to confirm before Linux is claimed
`renameat2` is declared for musl in the pinned `libc`, but a declaration is not a symbol: the static-PIE
musl core named in v8 §8 needs a musl new enough to export it, otherwise the link fails (safe, but a build
break). And on Linux a failed `fsync` may leave dirty pages marked clean, so *retrying* a failed barrier can
falsely succeed; the draft never retries (good) — that property should be stated so nobody adds a retry.

## What the mechanism relies on the caller for (assumptions, tested where possible)
- **Custody of the retained directory and exclusion of competing namespace writers.** My races show the
  primitive stays correct under same-privilege concurrency for the things it controls (one exclusive winner;
  never following a swapped-in symlink), but replacement is last-writer-wins by design.
- **The retained handle, not the path, is the identity** (confirmed). Who selected it is not authenticated.
- **A local POSIX filesystem** (R78-1) — not currently stated.
- **Never use on live lock carriers** (stated in the doc comment; rename replaces the inode locks live on).

## Commands and outcomes (all under `claude-out/`)

| Command | Outcome |
|---|---|
| `verify_extract.py` (before extraction; after all work) | 15 + 357 + 360 members verified from tar; 0 unsafe; unchanged |
| vendor coverage check for 88's `Cargo.lock` | 40/40 satisfied by archives verified in my crypto review |
| `cargo test -p opensip-platform --offline --locked` (scratch 79 / 88) | 11 passed / 22 passed |
| `fullfsync-by-filesystem` (Python, scratch disk images) | directory and file `F_FULLFSYNC` and `fsync` succeed on APFS, FAT32, exFAT, HFS+ — so the macOS fallback branch was **not** reachable at run time here |
| `tests/claude_probe.rs` (scratch 88, public API) | 49 recorded observations; table above |
| `probes/mutation.py` | 15 mutants, all applied and compiled; 10 killed, 5 survive |

No probe failed this round; one experiment produced a **negative result that I am reporting as such**: I
tried to make the macOS directory fallback observable by finding a filesystem that refuses directory
`F_FULLFSYNC`, and did not find one among the four I could mount, so M-1 rests on the standard-library
source, not on an observed run. The scratch disk images were detached and deleted.

Toolchain: Rust 1.95.0, macOS (Darwin 25.6.0, aarch64). Python 3.12.13 for harnesses.

## Limits
1. macOS only. No Linux code was executed; `renameat2`, Linux `fsync` semantics and ext4/xfs/btrfs are
   reviewed as source.
2. Real faults I produced: out-of-space, unsupported exclusive rename, permission denied, deleted
   directory, name too long. **No `EIO`, no barrier failure, no power loss** — the `EIO`/post-rename paths
   are covered only by the owner's injected doubles and by my mutation run over them.
3. `unsafe` blocks in `filesystem.rs` were read for pointer / lifetime / ownership correctness in the
   publication paths (l.56-62, 110-131, 408-445, 464, 509-549); `locks.rs`, `macos.rs`, `linux.rs`,
   `clock.rs` and the ACL code were not reviewed.
4. The 315 reference cases were read through the model, not re-derived; I did not re-run the archived
   comparison scripts.
5. No dependency, target or cumulative acceptance; no custody or semantic-publication acceptance.
