# Review: running-image identity 463a r3

Grok is the single reviewer. Claude Opus 5.5 leads. Re-review after r2 RF-1. No repository edits.

Product HEAD `5faf0a5` holds the r2 bytes. The r3 change is uncommitted. `git status` is `macos_image.rs` and `macos_loader.rs`. The four pinned paths match `hashes.txt` byte for byte. `filesystem.rs` and `lib.rs` are the r2 pins.

Host: macOS 27.0 (26A428), Apple M5 Max. Rustc `1.95.0` (`59807616e`) at `/opt/homebrew/Cellar/rust/1.95.0/bin`. `cargo --locked --offline`.

## Verdict

**ACCEPT-UNIT.** r2 RF-1 is closed. No new finding.

## r2 RF-1 is closed

`MAX_ARCHITECTURES` is 32 and `MAX_SIGNATURE_SLOTS` is 64. `locate_as` refuses `n > MAX_ARCHITECTURES` before the fat vector and `entries > MAX_SIGNATURE_SLOTS` before the signature vectors. Those are the same limits as the literals they replace. Each accepted vector is `Vec::with_capacity` of that count, and each loop pushes once per element, so the buffer does not grow.

`parser_cost` reserves 3 objects and `(32 + 64) * size_of::<Range<usize>>() + 64 * size_of::<u32>()` bytes. On this host that is 1792 bytes: the fat `Vec<Range<usize>>`, the signature `Vec<Range<usize>>`, and the signature `Vec<u32>`. `file_cost` adds that cost. The file-read charge is 5 objects, the previous read and hash bytes, and those 1792 bytes. The charge is taken before the read, so it covers a fat image and a thin one. A thin image does not allocate the fat vector; the reservation is the cap.

`the_file_read_reserves_the_parser_vectors_at_their_caps` pins those counts and passed.

## Answers

`locate_as` allocates those three vectors and nothing else. `Range` clones are two-word copies. `cdhash` and `sha256` write a stack `[u8; 32]` through `CC_SHA256` and return that array or its first 20 bytes. Those 64 bytes are already in `file_cost`. Neither hash allocates on the heap.

The parser's accept and refuse behavior is unchanged. The kernel-hash join, the no-follow open, and the r2 leaf and path charges are unchanged.

The two suite failures are the loader law 348 dyld refusals from r2. Both panic with `Malformed("ambiguous architecture")`:

- `macos_loader::tests::macos_loader_actual_system_artifact_reports_digest_without_authority` at `macos_loader.rs:736`
- `macos_image::tests::a_different_file_does_not_match_the_kernel_hash` at `macos_image.rs:403`

Naming the caps does not change that comparison. Slice selection stays with proposal 348a.

## Inventory 67

Unchanged. Re-hashed to the r1 and r2 bytes: subject manifest `5463d782f630102f19c589fa4a72fcb6419620b7a4ca39bf44cb323a548caa6d` (1649), v67 `4ee3c6467bbd0ef466770e5735d619ca274a78d0ee76783f3cf86ce04d7c3beb` (286435), v66 `a03ac52a29b1e6a50bd47fbb591a24b5625d3a44b89a7fed8b35980718196bcf` (285776), successor `1169ca8a57030857d58516494848d6c9fa0fb42829a5bfa8a28c52a432c00344` (5949). Layout verdict remains **ACCEPT**.

## Replay

- `rustfmt --edition 2024 --check` on the four pinned `.rs` paths: exit 0.
- `cargo test --locked --offline -p opensip-platform --lib`: exit 101. 168 tests, 166 passed, 2 failed, both named above. The new cap test passed.
- `cargo clippy --locked --offline --workspace --all-targets -- -D warnings`: exit 0.

Do not commit.
