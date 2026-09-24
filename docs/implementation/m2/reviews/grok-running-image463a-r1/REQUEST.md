Grok review 463a r1: the running-image identity mechanism of accepted law 463, and inventory67. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-running-image463a-r1. You own the serial native lane until your report is written. Rust is /opt/homebrew/Cellar/rust/1.95.0/bin. Use cargo --locked --offline in /Users/sb/code/opensip-ai/opensip. Do not read or print the private 413 UUID fixture.

Product HEAD cd48f87. Pins of the three paths are in hashes.txt beside this request; `git status` must show exactly those. Law: /Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/initial-core-launch-463/PROPOSAL.md (accepted r3), section "Evidence (macOS)", first two bullets.

## The unit

- New crates/platform/src/macos_image.rs: `observe_running_image(max_bytes, work)` reads `csops(getpid(), CS_OPS_STATUS)` and `CS_OPS_CDHASH`; takes the kernel path from `proc_pidpath`; retains the parent chain with the charged no-follow `open_accounted`; opens the leaf with `open_regular` (no-follow) on the retained parent; takes its status; refuses a non-regular file, an empty one, or one larger than `max_bytes` before allocating; reads exactly that length and checks the status is unchanged; parses the running CPU's slice with the loader's parser and hashes its CodeDirectory; requires that hash to equal the kernel's; and rechecks the kernel hash, the parent names, and a no-follow reopen of the leaf. Every step is charged to the caller's scope before it runs. The status flags are returned raw; which flags a release requires is policy for the later `InitialCore` unit. `recheck` repeats the kernel, name and reopen checks.
- macos_loader.rs: `locate` becomes a wrapper over `locate_as(raw, cpu, filetype, cap)`, keeping the loader's exact behavior (MH_DYLINKER, 16 MiB); `Located`, `cdhash` and a new `sha256` (same CommonCrypto call) are crate-visible. Only the error string for the file-type check changed wording.
- Nothing here reads release records, judges custody, embeds values in the image, or decides `InitialCore`.
- Inventory67 (docs/implementation/m2/running-image-inventory-v67/, repository-file-inventory.v67.json, subject manifest running-image-inventory-v67-subject.json) adds exactly that file at index 196, role adapter. The projection helper is byte-identical to v64–v66 and passed with 28 corruptions refused.

## Decide

1. Is the kernel hash the identity, with the path only a locator? Can a substituted, renamed or swapped file pass?
2. Is every native call, buffer and read charged before it runs? Is anything allocated before its reservation (note the path buffer, the file buffer, and the status reads)?
3. Does the loader keep its exact prior behavior?
4. Is `csops`/`proc_pidpath` use sound (sizes, error handling, no Security.framework)?

## Lead results

rustfmt clean; workspace clippy -D warnings clean; `cargo test -p opensip-platform --lib` 166 passed (the new test observes the linker-signed test binary: CS_VALID set, kernel hash equal to the parsed hash, SHA-256 and length equal to an independent read); security `native_platform` 7 passed. Replay at least rustfmt, the platform lib suite, clippy and the inventory67 projection helper.

review.json must contain top-level "verdict" ("ACCEPT-UNIT" or "REQUIRED-FINDINGS"), "requiredFindings", "subjectManifestSha256" (SHA-256 of running-image-inventory-v67-subject.json), and "inventoryCandidateAssessment": {"verdict", "requiredFindings", "path", "bytes", "sha256" of repository-file-inventory.v67.json, "parent": {path, bytes, sha256 of v66}, "successorRecord": {path, bytes, sha256 of running-image-inventory-v67/successor.json}}. Paths are relative to the architecture repository. Write REVIEW.md and review.json. Do not commit.
