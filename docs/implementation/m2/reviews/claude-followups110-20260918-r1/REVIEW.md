# Independent bounded review — review follow-ups 110 (105 N-1/N-2, 106 N-1)

Reviewer: Claude (actual independent reviewer; Codex remains implementation owner). 2026-09-18.
Request: `REQUEST.md`. Scope: the two changed files of frozen `review-followups-draft-checkpoint-110`
as closures of my crypto105 N-1/N-2 and publication106 N-1. Codec 109 and signed-security 106 have
their own verdicts and are not re-reviewed. No frozen/selected/product edit, commit, push or
delegation; builds and mutants ran in scratch copies.

## 1. Subject verification (before extraction)

| Item | Value |
|---|---|
| `subject.tar.xz` | 4,146,604 bytes, SHA-256 `bcda1e92b1a86185d94835786082697452842c28e6f16628251875aaf5158e15` = `archive-pin.json` |
| `subject.json` | SHA-256 `574f1b71002c3c5e38960240b8d01260db1e681da6064b8f843682ebd1de101e` |
| Members | 377/377 regular, each length + SHA-256 equal to the manifest from the tar; 0 unsafe/extra; re-verified after all work |
| Product pins | 330/330 equal; no unpinned file |
| Parent | `parent-inputs.json` equals **my own** verified extraction of frozen 109 file by file; 328 unchanged, 0 added/removed |
| Changed | `crates/security/src/trust.rs` `ad2c655cdbc463c37b90428211b721de545d7ddcf3ddbb7e91c3f706242cdc0c` (58 added lines, 0 removed — tests only) · `crates/platform/src/filesystem.rs` `177cd3b569aa204d9b0be4f7b248c3aa05612f11e8a780e7d5663e99a1934e9e` |

`filesystem.rs`: unit struct `NativePublication` becomes a struct with one macOS-only
`full_flush: fn(&File) -> io::Result<()>`; a `const NATIVE_PUBLICATION` carries
`full_flush_directory`; 15 call sites are renamed mechanically; `sync_directory` passes
`self.full_flush` as the first syscall and the **literal** `fsync_directory` as the fallback; one
new macOS test. No public item, dependency, fixture or inventory changed (pins confirm).

## 2. Evidence

**Owner checks, fresh scratch build** (Rust 1.95.0, offline, locked, verified 51-crate vendor):
platform 29 passed, security 62 passed, 0 failed; `cargo clippy --workspace --all-targets -- -D
warnings` clean.

**Curve facts checked with my own arithmetic** (`probes/point-facts.json`): `ff×32` decodes, raw
y = p + 18, canonical encoding `1200…0080` ≠ input, not small-order (8·P ≠ O) — so it isolates the
*canonical-encoding* clause from the *weak-key* clause, which is exactly what 105 N-1 asked for.
`c7176a70…037a` is canonical and has order exactly 8.

**Control for the root test (mine).** `every_root_key_is_checked…` expects `RetainedPolicy`, the same
error `retained_root_semantics::assess` returns just before the key loop, so by itself it cannot
show *why* the root was refused. I added, in a scratch copy only, the same construction with a
**valid** unreferenced key (the canonical form of the point above): admitted under both schemas; the
same entry re-spelt as `ff×32` is refused. So the refusal in the owner's test is caused by the key
gate, and root admission also enforces canonical encoding for unreferenced keys.

**Mutation** (`probes/mutation.py`; baseline green first; no compile failure occurred, none would
have been counted):

| Mutant | Result |
|---|---|
| production fallback is `full_flush_directory` again | killed by the new wiring test |
| seam bypassed (`sync_directory` ignores `self.full_flush`) | killed by the new wiring test |
| `EBADF` added to the unsupported list | killed (retained errno test) |
| canonical check uses original-byte accessor `key.to_bytes()` | killed — by the new direct test and one other |
| weak check removed | killed (4 tests) |
| first-key-only root admission | killed (new root test + payload test) |
| last key skipped at root admission | killed **only** by the new root test |
| **production first flush is plain `fsync`, still labelled `FullFlush`** | **survived** |

7 of 8 killed. I confirm the owner's three.

## 3. Closure of the named findings

- **105 N-1 (canonical check vacuous under `to_bytes()`) — closed.** The direct test fails under the
  accessor mutant independently of any fixture.
- **105 N-2 (root admission must check every key, including unreferenced) — closed.** "Last key
  skipped" is killed by the new test alone; the control shows the cause is the key gate.
- **106 N-1 (production fallback wiring unpinned) — closed for the fallback argument.** The socket
  trick is sound and honestly labelled: `fsync(socket)` = `EINVAL`, `F_FULLFSYNC(socket)` = `EBADF`
  (both asserted first, so a platform change fails loudly rather than silently weakening the test),
  the injected first flush returns `ENOTSUP`, and the observed `EINVAL` can only come from a real
  `fsync`. The real-directory positive control returns `DirectoryBarrier::Fsync`. It claims nothing
  about a filesystem refusing full flush; my earlier negative result (no such filesystem found on
  this host) stands.

## 4. Findings

No blocking finding.

- **N-1 (low) — the other half of the production wiring is still unpinned: the constant's *first*
  syscall.** With `NATIVE_PUBLICATION.full_flush = fsync_directory` every test passes and the barrier
  is reported as `FullFlush` while only `fsync` ran — the label would overstate durability on the
  one platform where the difference is the whole point. The new seam makes this a one-line pin using
  the owner's own socket: `NATIVE_PUBLICATION.sync_directory(&socket)` must fail with `EBADF`
  (`F_FULLFSYNC`'s errno, not in the unsupported list, returned unchanged). I verified in scratch
  that this assertion passes on the frozen bytes and kills the mutant
  (`probes/first-flush-pin.json`). Recommend adding it to the same test.
- **N-2 (note) — the seam is a private field on a private type, macOS-only, and the constant is the
  only non-test constructor**; no caller can inject a flush. The Linux arm is unchanged by reading
  (`NativePublication {}` with the field compiled out), but **I could not compile a Linux target
  here** (only `aarch64-apple-darwin` std is installed). Host 65 is the owner's evidence for that,
  not mine.
- **N-3 (note) — root test label** reads "TEST ONLY unreferenced order8"; test-only keys carry no
  authority, and none is signed with. Fine.

Unresolved: no Linux/musl/x86_64 lane, no hardware or power-loss claim, 104 N-4 remains recorded.

## 5. Bounded verdict

**Follow-ups 110: reviewed, no blocking findings. 105 N-1 closed, 105 N-2 closed, 106 N-1 closed for
the fallback path; N-1 above (first-flush constant) is a small residual of the same family.** Not
cumulative approval, not selection, and no current-authority, target or dependency qualification.

Evidence: `claude-out/pin-verification.json`, `product-pins.json`, `trust.diff`, `filesystem.diff`,
`probes/mutation.{py,json}`, `probes/first_flush_pin.py`, `probes/first-flush-pin.json`,
`probes/point-facts.json`, `hashes.txt`.
