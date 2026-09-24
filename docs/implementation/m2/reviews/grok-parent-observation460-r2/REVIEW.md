# Review: parent observation 460 r2

Grok is the single reviewer. Claude Opus 5.5 leads. Re-review of the r1 reservation findings. No repository edits.

Product `9c53c94`. `git status` is exactly the seven pinned paths. All seven hashes match. `filesystem.rs`, `lib.rs`, and both security files are the r1 bytes. The cost changes are in `path_binding.rs`, `directory_open.rs`, and `descriptor_filesystem.rs`.

## Verdict

**ACCEPT-UNIT.** RF-1 and RF-2 are closed. No required findings.

## Answers

`status_read_cost` is one edge and one buffer, the larger of `libc::stat` and `std::fs::Metadata`. On this toolchain `File::metadata` is one `fstat` of `libc::stat` moved into `Metadata`, so that one buffer covers the call.

**RF-1.** For `N` child components, `open` does `N + 1` opens, a kind-check on each retained handle, and one closing `recheck`. `recheck` does, for the root and each child, one reopen, that handle’s kind-check, and two comparison reads. That is `6N + 6` edges and `4(N + 1)` status buffers, which is what `retained_path_open_cost` records. `/` is the `N = 0` case: 4 objects, 6 edges, and 4 status buffers plus the one path byte. `recheck_exact_names_cost` is two of those rechecks plus one name sample per child edge. `open_child_directory_cost` is the `openat` plus the kind-check on the new handle: 2 edges, and bytes for the name, the NUL, and one status buffer. A missing child returns before the kind-check, so that path reserves a read it does not perform.

**RF-2.** `observe_filesystem` still calls `metadata` and then `fstatfs`. The cost is 2 edges, and its bytes add the `statfs` buffer, one `status_read_cost` buffer, and `DescriptorFilesystem`.

`observe_child_absent` is one `fstatat` into a `libc::stat`, with the name and that `stat` buffer reserved. It does not construct `Metadata`, so pricing `size_of::<libc::stat>()` matches the buffer it uses.

No status read, handle, or output buffer in `open`, `recheck`, `recheck_exact_names`, `open_child_directory`, `observe_child_absent`, or `observe_filesystem` is outside its reservation. The security walk is the r1 bytes: omission without a premise still refuses, a foreign premise still latches before the open, `OpenSIP` stays private, and `preview-v1` absence stays the no-follow `fstatat` on the retained parent. Nothing new is wrong.

## Replay

Rust is `/opt/homebrew/Cellar/rust/1.95.0/bin`. `cargo --locked --offline`.

- `rustfmt --edition 2024 --check` on the seven pinned `.rs` paths: exit 0.
- `cargo test -p opensip-platform --lib`: 163 passed.
- `cargo test -p opensip-security --lib -- creator_parent initial_installation installation_root`: 19 passed.
- `cargo clippy --workspace --all-targets -- -D warnings`: exit 0.
- No `opensip-parent460-*`, `opensip-ancestor457-*`, `opensip-binding161-*`, or `opensip-child-directory-*` leftovers.

Do not commit.
