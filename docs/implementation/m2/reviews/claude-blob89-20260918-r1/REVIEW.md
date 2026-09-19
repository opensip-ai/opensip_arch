# Independent bounded review — private digest-bound blob store 89 (full source)

Reviewer: Claude (actual independent reviewer; Codex remains implementation owner). 2026-09-18.
Request: `REQUEST.md`. Scope: the read/store **mechanism** — all of `crates/storage/src/blob_store.rs`, its
private facade (`lib.rs`), and the platform pieces it relies on: `RetainedDirectory::{from_retained_handle,
open_regular, publish_new_regular, confirm_existing_regular}`, `verify_staged_bytes`, `ExistingFileReceipt`.
Stated preconditions are taken as given and not extended: explicit root custody, an admitted local POSIX
filesystem, publication by replacement. Not ledger, Run authority, custody, OS qualification or cumulative
approval. No frozen/selected/product edit; scratch builds with dedicated target directories; no commit,
push or delegation.

## 1. Subject verification (before execution)

| Item | Value |
|---|---|
| `subject.tar.xz` | 3,990,496 bytes, SHA-256 `d8125f47c3eee670cf0c71903d383d1aafec770dc8e55d17d5f44b7bb5878d57` = request and `archive-pin.json` |
| Members | 363/363 regular, each length + SHA-256 equal to the manifest from the tar; 0 unsafe/extra; re-verified clean afterwards |
| Product pins | 327/327 equal; none unpinned |
| Parent | `parent-inputs.json` (324) equals **my own** verified extraction of frozen 88; 4 changed (`Cargo.lock`, `Cargo.toml`, platform `filesystem.rs`, `lib.rs`), 3 added (storage `Cargo.toml`, `blob_store.rs`, `lib.rs`), 0 removed |

**Inherited differences against the latest frozen 121**: `blob_store.rs` is **byte-identical**
(`8cd54891…`), as is platform `lib.rs`. Storage `lib.rs`/`Cargo.toml` differ only by later sibling modules
(`availability`, `ledger_store`, `recovery`, `rusqlite`); none references the blob store. Platform
`filesystem.rs` differs (106–113 corrections: private staging mode, reserved staging prefix, native
full-flush seam). `confirm_existing_regular` in 121 is the same sequence plus a staging-prefix refusal, and
`verify_staged_bytes` is unchanged — so **every finding below applies to 121 as well**.

## 2. What the mechanism does (read in full)
`VerifiedBlob::from_owned` checks exact length and SHA-256 and owns the bytes. `publish` names the blob by
lowercase hex digest and calls the exclusive (`RENAME_EXCL`) publication; only on `AlreadyExists` **with no
cleanup error** does it fall to `confirm_existing_regular`, which opens the name with
`O_NOFOLLOW|O_NONBLOCK`, requires a regular file, compares every byte (length pre-check, 64 KiB chunks,
trailing-byte check), then applies its own file and directory barriers. `read` refuses above the caller's
bound before opening, pre-checks the metadata length, reserves exactly `size` with `try_reserve_exact`,
reads exactly `size`, requires EOF, and re-verifies the digest. Nothing replaces or deletes an entry.
Arithmetic: `u64 → usize` via `try_from`; no unchecked addition; the read buffer is fixed.

## 3. Evidence

Scratch build (Rust 1.95.0, offline, locked): storage **4 passed / 0 failed**.

**Existing-state probe on a real filesystem** (`probes/probe.txt`) — what `publish` does when the digest
name already holds something:

| Existing entry | Result | Entry afterwards |
|---|---|---|
| same length, different bytes / shorter / longer / empty | `Err(Io InvalidData)` | preserved byte-for-byte |
| directory, FIFO, symlink to a file with the **correct** bytes, dangling symlink | `Err(Publication stage=Prepare, InvalidInput)`; FIFO does not block | preserved |
| correct bytes, mode 000 | `Err(Io PermissionDenied)` | preserved |
| correct bytes, mode 0666 | **`Ok(ConfirmedExisting)`** | preserved |
| correct bytes, **hard link** to another name (nlink 2) | **`Ok(ConfirmedExisting)`**; an in-place write through the other name afterwards makes `read` return `Err(Digest)` | — |

No staging leftovers in any case. **`read` boundaries**: exact bound ok, bound−1 `Limit`, declared length
±1 `Length`, `u64::MAX` `Length`, absent `Io NotFound`, 1 TiB sparse file with a 4 KiB bound `Limit` in
0 ms (no allocation, no read). **Concurrency**: 40 rounds × 16 identical publishers →
`PublishedNew` 40, `ConfirmedExisting` 600, 0 errors, 0 anomalous rounds.

**Name substitution between verification and the barrier** (`probes/probeD.txt`; my first attempt was
mistimed and is preserved as `probeD.FAILED-r1.txt`): calling `confirm_existing_regular` on a 256 MiB file
and re-pointing or unlinking the name 8 ms later — **8 of 8 trials return a receipt**: 4 while the name now
holds *other bytes*, 4 while the name *no longer exists*.

**Mutation** (16 mutants, all compiled, baseline green): **8 killed, 8 survived.**
Killed: existing name trusted without verification; digest or length unchecked in `from_owned`; caller
bound ignored or off by one; `read` returning bytes without re-verifying the digest; confirm without byte
verification; verification of the first chunk only.

## 4. Findings

- **F-1 (medium) — `ExistingFileReceipt` does not bind the verified inode to the name.** The function
  verifies and fsyncs a *descriptor*, then fsyncs the directory, and the receipt reads as "this name
  durably holds these bytes". If the name is re-pointed or unlinked in between, the receipt is still
  issued (8/8). Under the stated preconditions other blob publishers cannot do this (they only
  `RENAME_EXCL`), so the realistic actor is whatever later **removes** blobs — purge or GC — or anything
  using `replace_regular` in the same directory. The check is cheap and needs no new precondition: after
  the directory barrier, re-open the name with `O_NOFOLLOW` and compare `(st_dev, st_ino)` with the
  verified descriptor; on mismatch or `ENOENT` return an error instead of a receipt. Until then the
  caller contract must say that no unlink or replacement of a digest name may run concurrently with
  `publish`, and the purge design must provide that exclusion.
- **F-2 (medium–low) — the durability half of the receipt is untested.** "File barrier skipped" and
  "directory barrier skipped but still reported as `FullFlush`" both survive, in 89 and by construction
  in 121 (the call is a direct `NATIVE_PUBLICATION.sync_*`). The publication paths got an injectable
  `PublicationOps` in 106; `confirm_existing_regular` did not. Route it through the same seam and pin:
  order verify → file barrier → directory barrier; a failure of either yields an error and **no receipt**.
- **F-3 (low) — a hard-linked or world-writable existing blob is confirmed.** Content is right at
  confirmation time and later tampering is caught by `read` (`Err(Digest)`), so integrity holds; what is
  lost is *availability* of a blob a receipt called durable. Under root custody nobody else can create
  such links, so this is hardening: refuse `st_nlink != 1` and group/other-writable modes on the existing
  path (new publications already get a private mode since 106).
- **F-4 (low, tests) — masked and class-only survivors.** (a) The metadata length pre-check and the
  trailing-byte check mask each other in both `read` and `verify_staged_bytes`: either can be removed
  alone. They differ only under concurrent growth or for a *shorter* file, where the class changes
  (`Length` vs `Io UnexpectedEof`); add a shorter-file read case and keep both. (b) "Any publication
  failure treated as existing" survives: it still errors when the name is absent and legitimately
  confirms when it matches, so it is a class change (`Io` instead of `Publication` with its stage and
  visibility) — but that stage information is exactly what a caller needs after an indeterminate rename,
  so pin it with one injected-failure case once the seam of F-2 exists. (c) "AlreadyExists accepted even
  when staging cleanup failed" needs the same injection.
- **F-5 (note)** — `debug_assert_eq!(receipt.byte_len(), …)` vanishes in release builds; harmless, since
  the value is the caller's own length, but it is not a check. The `AlreadyExists` test does not look at
  `e.stage()`; an `EEXIST` from staging-name creation would also route to confirmation, which then
  verifies or refuses — safe, merely imprecise.

## 5. What I did not find
No path that overwrites, truncates or deletes an existing entry; no way to obtain a `VerifiedBlob` without
a digest check; no allocation driven by file metadata or by an unchecked caller value; no blocking on
FIFOs; no symlink following at the leaf; no arithmetic that can wrap.

## 6. Not examined
`publish_new_regular` and its staging protocol beyond what `publish` depends on (covered by my 88 and 106
publication reviews); `ledger_store.rs`, `availability.rs`, `recovery.rs` (121 only); Linux; hardware or
power-loss behaviour; directory custody itself.

## 7. Bounded verdict
**Blob store 89 (identical in 121): reviewed in full; the store/read mechanism is sound on content —
corrupt or foreign entries are never replaced, never confirmed, and never read back as valid — with two
findings on what the *existing-file receipt* claims: F-1 (name not re-bound after the barrier; 8/8
reproduced) and F-2 (barriers unpinned by any test).** F-3 to F-5 are hardening and tests. Not approval
of ledger, Run authority, purge, custody, OS, targets, or any cumulative standing.

Evidence: `claude-out/pin-verification.json`, `product-pins.json`, `probes/rust_probe.rs.txt`, `probe.txt`,
`rust_probe2.rs.txt`, `probeD.txt`, `probeD.FAILED-r1.txt`, `mutation.{py,json,log}`, `hashes.txt`.
