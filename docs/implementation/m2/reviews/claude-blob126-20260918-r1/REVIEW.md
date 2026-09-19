# Independent bounded review — blob confirmation 126 (Rust)

Reviewer: Claude (actual independent reviewer; Codex remains implementation owner). 2026-09-18.
Request: `REQUEST.md`. Scope: the delta of frozen `blob-confirmation-checkpoint-126` over frozen 124 —
`platform/src/filesystem.rs` (existing-file confirmation) and `storage/src/blob_store.rs` — as correction of
my blob89 F-1 to F-5. Mechanism only: not ledger, custody, purge/GC design, OS or cumulative approval. The
124 F-2/F-3 follow-ups are tracked separately and are not re-raised. No frozen/selected/product edit;
scratch builds with dedicated target directories; no commit, push or delegation.

## 1. Subject verification (before use)

| Item | Value |
|---|---|
| `subject.tar.xz` | 4,099,448 bytes, SHA-256 `c4af9e9fe479bc6b8a2e58cef8d15d72541b727d3da8054db3878ad58781680c` = request and `archive-pin.json` |
| Members | 430/430 regular, each length + SHA-256 equal to the manifest from the tar; 0 unsafe/extra; re-verified clean afterwards |
| Product pins | 330/330 equal; none unpinned |
| Parent | `parent-inputs.json` equals **my own** verified 124 extraction; 328 unchanged |
| Host pins | `host-isolation76/receipt.json` lists 210 sources; **all 210 equal the product pins**, including both changed files |
| Changed | `crates/platform/src/filesystem.rs` `409f848e…`, `crates/storage/src/blob_store.rs` `112261f6…` |

## 2. What changed (read in full)
`confirm_existing_regular` → `confirm_existing_with(…, ops: &impl PublicationOps)`: parent `is_reachable`;
open by name (`O_NOFOLLOW`, regular); `confirmation_metadata` refuses `nlink != 1` and group/other-writable
modes; full byte verification; **file barrier, then directory barrier, through the injectable ops**;
parent reachable again; **re-open the name and require the same `(st_dev, st_ino)`** (with the link-count
and mode checks repeated on the re-opened file); only then the receipt. The doc comment now says what the
receipt is *not*: the caller must exclude GC, purge, unlink, replacement and in-place writers for the
consuming operation, and the post-check is not permanent retention.
`blob_store`: the fallback to confirmation is a named policy,
`stage == Rename && visibility == Unchanged && kind == AlreadyExists && !cleanup_failed`; every other
failure keeps its `PublicationFailure`; a private publish seam; `read` split after the length sample so
growth and EOF are deterministic to test.

## 3. Evidence
Scratch build: platform **33**, storage **33** passed, 0 failed.

**My blob89 probes, re-run unchanged against 126** (`probes/probe.txt`, `probeD.txt`):

| Probe | 89 | 126 |
|---|---|---|
| confirm while the name is re-pointed or unlinked (256 MiB, 8 trials) | **8 receipts** (4 other bytes, 4 no name) | **0 receipts, 8 refused** |
| correct bytes, mode 0666 | `ConfirmedExisting` | `Err(InvalidData)` |
| correct bytes, hard link (nlink 2) | `ConfirmedExisting` | `Err(InvalidData)` |
| wrong bytes / shorter / longer / empty / directory / FIFO / symlink to correct bytes / dangling symlink / mode 000 | refused, entry preserved | identical |
| `read` bounds (exact, −1, ±1 length, `u64::MAX`, absent, 1 TiB sparse) | as designed | identical |
| 40 rounds × 16 identical publishers | 40 new / 600 confirmed / 0 errors | **40 / 600 / 0**, 0 anomalous rounds — the new link-count and mode checks do not disturb legitimate concurrent publishers (exclusive rename never creates a second link, and new publications get a private mode) |

**Mutation** (20 mutants, all compiled, baseline green): **16 killed, 4 survived.**
Killed: post-barrier re-binding removed; compared on device only; **re-binding moved before the barriers**;
file barrier skipped; directory barrier skipped but reported; barriers in the wrong order; hard link
accepted; group/other-writable accepted; only other-writable refused; each of the four fallback conditions
dropped; `read` length pre-check removed; both trailing-byte checks removed. On 89, seven of these
survived.

## 4. Closure of blob89

| 89 finding | Status |
|---|---|
| **F-1** receipt not bound to the name | **Closed** — post-barrier `(dev, ino)` re-binding, pinned (three mutants), reproduced 8/8 → 0/8. The remaining window after the check is stated as a caller obligation, which is the honest limit. |
| **F-2** durability half untested | **Closed at the seam** — order and fail-closed behaviour pinned through `PublicationOps`; see N-1 for the one line that is not. |
| **F-3** hard link / world-writable | **Closed** — both refused, on the first open and again on the re-open. |
| **F-4** masked length/trailing checks; class-only fallback | **Closed** — each check is now individually pinned (deterministic growth/EOF tests); the fallback is an explicit four-condition policy with an 80-cell grid and a real injected `Prepare` failure with matching bytes. |
| **F-5** `debug_assert`, stage not inspected | Stage and visibility are now inspected; noted. |

## 5. Findings

- **N-1 (low) — the production entry's choice of native barriers is unpinned.** Replacing
  `&NATIVE_PUBLICATION` in `confirm_existing_regular` with an ops object whose barriers are no-ops that
  still report `FullFlush` passes all 66 tests. (My first attempt at this mutant was a no-op by
  construction and proved nothing; both are recorded.) The seam tests pin *what confirmation does with an
  ops object*; nothing pins *which* object production passes. The 110/113 socket technique does not
  transfer, because confirmation requires a regular file. It is one token in a one-expression function and
  the constant's own wiring is pinned by 113, so the residual is small — but it is the same family as
  106 N-1, and a cheap structural answer exists: make the production entry the only caller able to name
  `NATIVE_PUBLICATION` for this path (e.g. a private constructor returning the ops), so a wrong choice is
  a visible diff in one place.
- **N-2 (note, equivalent survivors) — the two `is_reachable` checks in confirmation do not change any
  outcome I could construct.** Both survive, and I believe both are redundant *here*: a directory must be
  empty to be unlinked, so in an unlinked parent the open (before) or the re-open (after) already fails
  with `NotFound`; and a *relocated* parent is reachable by definition (124 F-1). They are harmless and
  cheap; say in a comment that they add no case beyond the re-open, so nobody later treats them as the
  name binding.
- **N-3 (note) — legacy group-writable blobs.** A pre-126 blob created under a permissive umask (0664) is
  now refused for confirmation and, because nothing replaces an existing entry, that digest can never be
  confirmed again. New publications get a private mode, and no product persistence is deployed, so this
  is a statement to make rather than a migration to write.

## 6. Bounded verdict
**126: reviewed, no blocking finding. blob89 F-1, F-2, F-3 and F-4 are closed; the false receipt I
reproduced 8/8 on 89 is refused 8/8 on 126, and legitimate concurrent publishers are unaffected. N-1 is a
small residual of the native-wiring family; N-2 and N-3 are notes.** Not approval of ledger, Run authority,
purge/GC exclusion, custody, OS or any cumulative standing.

Evidence: `claude-out/pin-verification.json`, `product-pins.json`, `host-pins.json`, `filesystem.diff`,
`blob_store.diff`, `probes/rust_probe*.rs.txt`, `probe.txt`, `probeD.txt`, `mutation.{py,json,log}`,
`hashes.txt`.
