Grok review 465a (charged directory barrier and exclusive-create primitives), r1. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-directory-effects465a-r1. You own the serial native lane until your report is written. Host macOS 27.0. Rust is /opt/homebrew/Cellar/rust/1.95.0/bin. Use cargo --locked --offline. Do not read or print the private 413 UUID fixture.

Law: docs/implementation/m2/initial-parent-preparation-465/PROPOSAL.md items 2, 3 and 6 (accepted). Product HEAD 000c5ce. The uncommitted files are pinned in hashes.txt. **crates/platform/src/filesystem/directory_effects.rs is a new file with no inventory row yet.** It will be added in inventory71 together with 465b's new files, and 465a will be integrated with 465b. This review is of the code only.

## Changes

- **`directory_barrier_cost()`:** 0 objects; 4 edges on macOS (status, F_FULLFSYNC, the always-reserved fallback fsync, status) or 3 on Linux; two status buffers. `confirm_directory_barrier_accounted` and `_reserved` charge everything before the first status read and reuse `confirm_directory_with`, so the fallback and error precedence are unchanged.
- **`create_exclusive_directory_cost(name)`:** 4 objects, 12 edges, and `name+1 + 2·status + dirent` bytes, charged before the name copy.
  - Accounted and reserved variants return `ExclusiveDirectoryOutcome::{Created(RetainedDirectory), EntryExists}`, where EntryExists means a raw EEXIST and keeps the scope open.
  - Other failures are `ExclusiveDirectoryError::{Name, Create(io), AfterCreate(io), NotFresh}`. NotFresh is the synthetic case, where mkdirat succeeded but the entry is not a fresh, empty, euid-owned directory.
  - The charged scan is bounded to 3 reads.
  - The existing `create_exclusive_directory` and its only caller (private_access.rs `create_private_directory`) are unchanged in behaviour. The freshness helpers are split into `is_fresh_owned_directory` and `empty_directory_within`, with the old helpers as wrappers.
- **`open_child_directory_reserved` and `observe_filesystem_reserved`**, which were missing.
- **A private `after_mkdir` test hook** (a no-op in production).

## Tests

- Costs are pinned.
- A live barrier gives the same kind as the unaccounted one, and `used()` equals the cost. A short ledger never calls the barrier.
- The fallback fires only for EINVAL, ENOTSUP and ENOTTY; EIO, ENOSPC and EINTR latch.
- Creation: a new directory is charged exactly and made 0700. An existing directory, file or dangling symlink gives EntryExists with nothing changed and no symlink followed. The hook-planted file or subdirectory gives NotFresh. Name, Create and AfterCreate are each covered.
- Reserved variants run inside `WorkScope::effect`, and a ledger that cannot hold all the postchecks never enters the effect.
- The new fixtures use /tmp, because the per-user temp directory made an existing test (`native_filesystem_original_file_lock_and_all_path_components_stay_owned`) flaky.

## Lead's replay

Platform lib 189/0; the workspace passes; clippy `-D warnings` and fmt pass. The Linux cfg branches are not compiled here.

## Decide

Is every call and allocation charged first? Is the barrier behaviour identical to the unaccounted path? Is EEXIST distinguished exactly as law item 3 requires, with no path that admits a directory we made but cannot verify? Is the existing API unchanged for its caller? Is the /tmp fixture choice acceptable? Anything else wrong? Replay the platform lib, the workspace, clippy and fmt.

review.json must contain top-level "verdict" (ACCEPT-UNIT or REQUIRED-FINDINGS) and "requiredFindings". Write REVIEW.md and review.json. Do not commit.
