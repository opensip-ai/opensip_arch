# Review: running-image identity 463a r2

Grok is the single reviewer. Claude Opus 5.5 leads. Re-review after r1 RF-1. No repository edits.

Product `5faf0a5` (`5faf0a594e646c905443b96543a08930c5cf4c5e`, "saving the files modified before llm models crashed"). Working tree clean. The four pinned paths match `hashes.txt` byte for byte. `lib.rs` and `macos_loader.rs` are the r1 bytes. Against `cd48f87`, `filesystem.rs` adds only `RetainedDirectory::open_regular_cost`.

Host: macOS 27.0 (26A428), Apple M5 Max, `hw.cputype` `0x0100000c`, `hw.cpusubtype` 2. Rustc `1.95.0` (`59807616e`, Homebrew LLVM 22.1.3) at `/opt/homebrew/Cellar/rust/1.95.0/bin`. `cargo --locked --offline`.

## Verdict

**REQUIRED-FINDINGS.** r1 RF-1 is closed. One new finding: the file-read reservation still omits the parser vectors `locate_as` allocates inside that charge.

## r1 RF-1 is closed

`open_regular` of one component duplicates the parent, builds one NUL-terminated name, `openat`s, and kind-checks with `metadata`. `open_regular_cost` prices that as 3 objects, 3 edges, and `len + 1 + status` bytes. Each further component adds a name, an `openat`, a handle, and a kind-check, which is what the loop does.

`leaf_open_cost` adds the caller's second `metadata` (one edge, one status buffer). `file_recheck_cost` adds the reopened-file `metadata` and the held-file `metadata` (two edges, two status buffers) on top of the kind-check already inside `open_regular_cost`. For the leaf `opensip` that is 4 edges and 5 edges, which the new test pins. `status_bytes` and `status_read_cost` are the same quantity: the larger of `libc::stat` and `std::fs::Metadata`.

`kernel_path` now runs inside `path_cost`. That charge is one `proc_pidpath`, the 4096-byte path buffer, and the three owned copies made before it returns: the parent `PathBuf`, the leaf `OsString`, and the leaf `String`. `OsString::from_vec` takes the path buffer without a further allocation. Four objects and `4 * 4096` bytes cover those four buffers. The copies no longer sit between `path_cost` returning and `open_accounted`.

The file-read charge no longer includes that open. The open is only in `leaf_open_cost` / `file_recheck_cost`.

## Answers

The kernel CodeDirectory hash is still the identity, and the path is still only the locator. r2 does not change that join. `csops(CS_OPS_CDHASH)` is taken first, the parent chain is the charged no-follow open, the leaf is `open_regular` (`O_NOFOLLOW`), and `locate_as` plus `cdhash` must equal the kernel hash. A substituted file fails the equality or the before/after status compare. A symlink component fails the no-follow open. A rename fails the name recheck or the no-follow reopen.

Every status read and both leaf-name copies in the r1 finding are now inside a reservation that covers them. The parser vectors below are still outside the file-read reservation. No other new status read, copy, or allocation is outside its reservation. `getpid` beside `csops` and `proc_pidpath` is the same unpriced call r1 accepted.

The two failing tests are the loader law on this host's `/usr/lib/dyld`, not a 463a regression. `macos_loader.rs` is the r1 pin. `locate_as` selects on CPU type `0x0100000c` and returns `Malformed("ambiguous architecture")` when a second slice has that type. I read the fat header: three slices, `nfat_arch` 3.

| slice | cputype | cpusubtype |
| --- | --- | --- |
| x86_64 | `0x01000007` | `0x00000003` |
| arm64e | `0x0100000c` | `0x80000002` |
| arm64e.x1 | `0x0100000c` | `0x8000000c` |

Both ARM64 slices match the process family, so the loader refuses rather than guess. The running CPU subtype is 2, the `0x80000002` slice. `capture_system_loader` is the only caller in the two failures:

- `macos_loader::tests::macos_loader_actual_system_artifact_reports_digest_without_authority` panics at `macos_loader.rs:731` with `Malformed("ambiguous architecture")`.
- `macos_image::tests::a_different_file_does_not_match_the_kernel_hash` panics at `macos_image.rs:373` on the same `capture_system_loader` error, before the hash comparison.

The other 463a tests do not depend on the macOS 26 dyld layout. On this host, `the_test_binary_matches_its_kernel_code_directory_hash` passed: the test binary is a thin `MH_MAGIC_64` image (`0xcffaedfe`, CPU `0x0100000c`), `CS_VALID` is set, and its length and SHA-256 match an independent read. `a_bound_below_the_file_refuses_before_allocation` passed. `leaf_costs_count_the_dup_the_open_and_every_status_read` is arithmetic on this compiler's type sizes and passed. None of the three reads `/usr/lib/dyld`.

## Required findings

### RF-1: `file_cost` does not reserve the vectors `locate_as` allocates inside the file-read charge

`file_cost` reserves 2 objects and `length + 1 + status + 64` bytes: the file buffer, the post-read status, and the two 32-byte hash outputs. The closure then calls `locate_as`. Every successful parse allocates `Vec<Range<usize>>` and `Vec<u32>` at the signature-slot capacity (`1..=64`). A fat image also allocates `Vec<Range<usize>>` at the architecture capacity (`1..=32`) before that. `Range<usize>` is 16 bytes and `u32` is 4, so the unpriced buffers are `20 * entries` bytes on a thin image and that plus `16 * n` on a fat image.

Failure: a ledger whose remaining objects are 2 and whose remaining bytes equal `file_cost(length).bytes` admits the read. A thin image still creates the file vector plus the two signature vectors. A fat image creates those plus the architecture vector. The cost test pins the leaf-open counts and does not run `locate_as` under this reservation, so the suite stays green. The passing image test is thin, so it does not take the fat path either.

Price, inside `file_cost`, the signature-range vector, the signature-slot vector, and the fat architecture vector at their parser caps (`64`, `64`, and `32`).

## Inventory 67

Unchanged from the accepted r1 assessment. Re-hashed:

| path | bytes | sha256 |
| --- | ---: | --- |
| `docs/implementation/m2/running-image-inventory-v67-subject.json` | 1649 | `5463d782f630102f19c589fa4a72fcb6419620b7a4ca39bf44cb323a548caa6d` |
| `docs/implementation/m2/repository-file-inventory.v67.json` | 286435 | `4ee3c6467bbd0ef466770e5735d619ca274a78d0ee76783f3cf86ce04d7c3beb` |
| `docs/implementation/m2/repository-file-inventory.v66.json` | 285776 | `a03ac52a29b1e6a50bd47fbb591a24b5625d3a44b89a7fed8b35980718196bcf` |
| `docs/implementation/m2/running-image-inventory-v67/successor.json` | 5949 | `1169ca8a57030857d58516494848d6c9fa0fb42829a5bfa8a28c52a432c00344` |

Layout verdict remains **ACCEPT**. The projection helper was not re-run; the bytes are the r1 bytes.

## Replay

- `rustfmt --edition 2024 --check` on the four pinned `.rs` paths: exit 0.
- `cargo test --locked --offline -p opensip-platform --lib`: exit 101. 165 passed, 2 failed, both `Malformed("ambiguous architecture")`, named above.
- `cargo clippy --locked --offline --workspace --all-targets -- -D warnings`: exit 0.

Do not commit.
