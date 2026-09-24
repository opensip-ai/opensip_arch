# Review: running-image identity 463a r1

Grok is the single reviewer. Claude Opus 5.5 leads. Source review of the running-image mechanism and inventory 67. No repository edits.

Product `cd48f87`. `git status` is `lib.rs`, `macos_loader.rs`, and the new `macos_image.rs`. All three hashes match.

## Verdict

**REQUIRED-FINDINGS.** One finding. The kernel join is sound, and inventory 67 is accepted as a layout candidate.

## Answers

1. **The kernel CodeDirectory hash is the identity. The path is only the locator.** `csops(CS_OPS_CDHASH)` is taken first. `proc_pidpath` opens with the charged no-follow parent chain, and the leaf is `open_regular` (`O_NOFOLLOW`). The running CPU's slice is parsed with the loader parser, and that CodeDirectory hash must equal the kernel hash. A substituted file fails that equality, or fails the status comparison if its device, inode, or size changed during the read. A symlink component fails the no-follow open. A rename fails `recheck_exact_names` or the no-follow reopen. The dyld measurement is a different hash and is not accepted as this image. Status flags are returned raw.

2. **The path buffer, the file buffer, and the kernel status word are charged before those calls.** `proc_pidpath` runs inside `path_cost` (two 4096-byte buffers). The file is refused when its status size is 0 or above `max_bytes`, and `file_cost(length)` is charged before the read buffer is allocated. The kernel pair is charged as two calls and 24 bytes. The leaf open and the recheck are short of the status read inside `open_regular`. See RF-1.

3. **The loader's prior behavior is unchanged.** `locate` is `locate_as` with `MH_DYLINKER` and the 16 MiB cap. The file-type check is still that constant; only its error string changed. `cdhash` is the same CommonCrypto SHA-256 truncated to 20 bytes. No loader test asserts the old string.

4. **`csops` and `proc_pidpath` are used at their real sizes.** Status is a 4-byte word. The hash buffer is 20 bytes. A nonzero return is `last_os_error`. The path buffer is `PROC_PIDPATHINFO_MAXSIZE` (4096); a non-positive length, a relative path, or an interior NUL refuses. Both are libSystem. Security.framework is not linked.

## Required findings

### RF-1: The leaf open and the recheck omit `open_regular`'s status read, and the leaf name is copied before the next charge

`open_regular` duplicates the parent, `openat`s the leaf, and calls `metadata()` before it returns. The first leaf step then calls `metadata()` again. Its charge is 2 edges and one status buffer. The recheck charge is 3 edges and two status buffers, which matches the `openat` and the two `metadata()` calls written in `recheck`, and not the status read inside `open_regular`.

Between `path_cost` returning and `open_accounted`, the leaf is copied into an `OsString` and a `String`. Those copies are not inside either charge.

Failure: a ledger whose remaining edges equal the published leaf-open cost (2) and whose remaining bytes equal one status buffer admits the open. The closure still performs `open_regular`'s `metadata()` and the caller's second `metadata()`. The same shortfall is in `file_recheck_cost`. A kernel path whose leaf is long enough that the two name copies exceed what `path_cost` reserved is allocated after that charge has already returned. Price `open_regular`'s status read in both costs, and charge the leaf copies before they are allocated.

## Inventory 67

One added file, `crates/platform/src/macos_image.rs`, at files index 196, role `adapter`. 714 inherited rows are equal by value. `package.json` moves 511 → 512. Packages and pending decisions match v66. The projection helper is byte-identical to the v64–v66 helper (`bb82ef05…`, 2917 bytes). Against the product design lock it reports PASS and 28 corruptions refused.

## Replay

Rust is `/opt/homebrew/Cellar/rust/1.95.0/bin`. `cargo --locked --offline`.

- `rustfmt --edition 2024 --check` on the three pinned `.rs` paths: exit 0.
- `cargo test -p opensip-platform --lib`: 166 passed.
- `cargo clippy --workspace --all-targets -- -D warnings`: exit 0.
- `verify_projection.py` for inventory 67: PASS, 28 corruptions refused.

Do not commit.
