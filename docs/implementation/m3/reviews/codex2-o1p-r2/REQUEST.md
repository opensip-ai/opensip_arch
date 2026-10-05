CODEX2 review: unit **O1-p** r2 of the accepted law M3-O1 r2 — platform CPU time, harness-descriptor admission, and `dispose`. Grok leads as of 2026-10-04. You are the single reviewer. Round 1 is REQUIRED-FINDINGS (`RF-O1P-1`, `RF-O1P-2`); inventory v141 was ACCEPT and its bytes are unchanged. Verdict wanted: **ACCEPT-UNIT** on the product change and inventory v141, with an **`inventoryCandidateAssessment`**. O1-p binds no contract successor and no design unit.

**Rules:**
- No repository edits, commits, pushes or delegation.
- Write only `REVIEW.md` and `review.json` under `/tmp/opensip-implementation/reviews/codex2-o1p-r2`.
- Run git read-only, and only against the product worktree named below and the architecture tree for the inventory files named below.
- Never touch `~/Library/Application Support/OpenSIP`. It must stay absent.
- Never read the private 413 UUID fixture.
- No crash-matrix lead set is needed. The diff does not touch `crates/security`, `crates/storage`, or `tools/check_crash_matrix.py`. `observe_clock` is unchanged.
- Before any cargo build, test or clippy, take `mkdir "$(getconf DARWIN_USER_TEMP_DIR)opensip-lanes.lock"` and `rmdir` only a lock your own `mkdir` created. If it is held, wait. Do not put `cargo` in a waiter's argv. Use a private 0700 `TMPDIR` and `cargo --locked --offline`. Toolchain: `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin`.

## What r2 changes

Round 1's two findings, and nothing else.

**RF-O1P-1.** `admit_harness_descriptor` still admits inherited descriptor 3: `fstat` FIFO or regular file, `F_GETFL` writable, then `F_SETFD` replaced with `FD_CLOEXEC` on descriptor 3. It no longer returns `File::from_raw_fd(3)`. `F_DUPFD_CLOEXEC` returns a new descriptor, and the `File` owns only that duplicate. Descriptor 3 stays open. A second call cannot alias the first file's descriptor. Failure still leaves descriptor 3 unowned. The same test now admits twice, drops the first file, opens an unrelated file, writes through the second file, and checks that the unrelated file stays empty while the harness file receives both writes. Both owned descriptors differ from 3 and from each other, and descriptor 3 keeps close-on-exec.

**RF-O1P-2.** `process_cpu_time` widens `time_t` and `suseconds_t` with `impl Into<i64>`, so the macOS `i64` seconds are not passed through `i64::try_from` and the `i32` microseconds use an infallible widening. The invalid-observation check is `seconds < 0 || !(0..1_000_000).contains(&micros)`. Negative microseconds and `1_000_000` microseconds still fail that check. The typed failure for a nonzero `getrusage` is unchanged.

`disposition.rs`, `disposition_tests.rs`, `lib.rs`, and inventory v141 are unchanged from r1.

## Inputs

Pins are in `hashes.txt`. The law pin is `PROPOSAL-r2.md` (80638 bytes, `987153221b913fc1c4cc729ecfabad397670502c8dc95a4bb292ebe0506bbbf0`). The live `PROPOSAL.md` is those bytes plus the acceptance note.

- **M3-O1 r2 item 2:** CPU time is `getrusage(RUSAGE_SELF)`, user plus system. The harness descriptor admits the inherited write channel, descriptor 3, and returns an owned writer. S-OP-2b is not accepted by this review. Do not treat it as a law you are accepting here.
- **Item 20 and O1-C11:** unchanged from r1. `dispose` consumes a `Result` and does nothing else. `TestOnly` and `ShutdownPath` are constructed only in `disposition_tests.rs`.
- **Item 23:** platform only. J3a is integrated. The diff does not touch `crates/operability/`, `filesystem.rs`, `filesystem/file_effects.rs`, or `crash_barrier.rs`.
- **O1-C12:** the CPU-time call is non-decreasing and a failed call is typed. Admission refuses a closed descriptor, a read-only one and a directory, and sets close-on-exec on descriptor 3 and on the owned duplicate.

## Product

- **Worktree:** `/Users/sb/code/opensip-ai/opensip-o1p`, detached at product main `e01efff`. Nothing is committed. `design-lock.json` is unchanged. Do not require a staged lock entry; the lead binds v141 after acceptance.
- **Diff:** `git diff e01efff` is 16661 bytes, sha256 `3d1d7bf418175bc0bf4e1bc45f6f9df56abb63491e152c5bf0e862f39214da7f`. Copy: `evidence/o1p.diff`. Five files, +374 −1. The three new files are intent-to-add so the diff contains them.
- **Do not touch** `/Users/sb/code/opensip-ai/opensip-o1a` or any other worktree.

## Tests the lead ran for r2

Under the lane lock, home absent before and after: `cargo test -p opensip-platform --offline --locked --lib` with `--test-threads=1` filtered to `clock::`, the descriptor admission, and the two disposition tests, then `cargo clippy --locked --offline -p opensip-platform --all-targets -- -D warnings`. `rustfmt --check` on `clock.rs` and `harness_descriptor.rs` passed before that run. The summary is `/tmp/opensip-implementation/o1p-r2/summary.txt`.

## Inventory v141

Unchanged from the r1 assessment that accepted it. Parent v140: 584066 bytes, `9eebf35bd89cb76a631f416200d7f2ca654a8d6e6e5cfc8cf2ab81fcc30961de`. Candidate: 585083 bytes, `6f9cddbc0531ff3128e783d8446d05462281b227a116ec84456ba28af642e750`. Successor: 307821 bytes, `5a939e59b7ca01e4a19d1aad40c6f7f8774211cad0ab706d92295119050d6306`.

## Decide

Rerun what you need under the lane lock. Check that `RF-O1P-1` and `RF-O1P-2` are closed and that v141's pins still match the files.

Write `REVIEW.md` and `review.json` in this directory.

`review.json` needs:
- `"verdict"`: `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`: an array, empty on acceptance;
- `"subjectSha256"`: `3d1d7bf418175bc0bf4e1bc45f6f9df56abb63491e152c5bf0e862f39214da7f`;
- `"inventoryCandidateAssessment"`: verdict `ACCEPT` or `REQUIRED-FINDINGS`, `requiredFindings`, the candidate path, bytes and sha256, parent v140's pin, and `successorRecord` pinning the successor file.

No `subjectManifestSha256`. No contract review file.
