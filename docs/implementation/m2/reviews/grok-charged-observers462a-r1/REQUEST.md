Grok review 462a (charged platform observers), r1. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-charged-observers462a-r1. You own the serial native lane until your report is written. Host macOS 27.0. Rust is /opt/homebrew/Cellar/rust/1.95.0/bin. Use cargo --locked --offline. Do not read or print the private 413 UUID fixture.

Law: docs/implementation/m2/initial-platform-462/PROPOSAL.md item 3 (accepted): every native observation is charged to the attempt ledger before it runs. Product HEAD 43c5e45. Seven uncommitted platform-crate files are pinned in hashes.txt. No file is added, and the existing unaccounted functions are unchanged.

## Changes

- `observe_macos_process_accounted` and `macos_process_observation_cost`: 0 objects, 1 call, 12 bytes.
- `observe_macos_boot_accounted` and `macos_boot_observation_cost`: two bounded sysctls, two csr_check calls and the two owned strings, charged once before the first call.
- `capture_system_loader_accounted`, `MacosLoaderObservation::recheck_accounted` and `filesystem_accounted` (fstatfs on the retained loader file), with public `system_loader_capture_cost` and `system_loader_recheck_cost`. Private helpers price:
  - the 348a header read;
  - the retained /usr/lib open and the name rechecks;
  - the leaf open and the observations;
  - the read at IMAGE_CAP plus 1, charged before any byte;
  - the parser vectors;
  - the hash;
  - the retained copy.

  The accounted capture allocates size+1 so that growth cannot reallocate beyond the charge.
- New shared costs:
  - `descriptor_observation_cost` (filesystem.rs);
  - `descriptor_acl_cost` (macos.rs), priced at 128 entries via a new `MAX_ACL_ENTRIES` constant with the same behaviour as before;
  - `recheck_exact_names_cost_for(components)` (path_binding.rs), to which the existing method now delegates.
- Tests:
  - each accounted observer equals its unaccounted twin live, and `ledger.used()` equals the published cost;
  - the costs are pinned;
  - a ledger one byte short of the loader read refuses before reading, on /usr/lib and on a fixture, where the after-read hook never runs.

## Lead's replay

Platform lib 177/0; workspace 984/0; clippy `-D warnings` and fmt pass.

## Stated limits

- libSystem ACL allocations count as objects with no bytes, and the directory-service lookup as one call.
- Kernel work inside sysctl and csr_check is not measured.
- Reads assume no short reads, as in macos_image.
- The loader read and the retained copy are charged at the 16 MiB cap, about 32 MiB of the 256 MiB ledger.

## Decide

Does every native call and allocation sit inside a prior charge? Are the costs honest, and are the limits acceptably documented? Are the accounted and unaccounted observations truly equal? Does the loader still select by the mapped dyld header (348a) and keep all 348 checks? Is the 32 MiB cap charge acceptable given the ledger must also cover InitialCore (about 96 MiB image cap) and later steps? Anything else wrong? Replay the platform lib, the workspace, clippy and fmt.

review.json must contain top-level "verdict" (ACCEPT-UNIT or REQUIRED-FINDINGS) and "requiredFindings". Write REVIEW.md and review.json. Do not commit.
