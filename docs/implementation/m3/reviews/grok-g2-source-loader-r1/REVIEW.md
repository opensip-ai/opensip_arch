# Rust G2 immutable source-loader authoring component r1 — ACCEPT-UNIT

This accepts the immutable source-loader and its pinned `FileLoader` bridge as one G2 authoring component. Full G2, G2-v launch, T1, confinement, prepared-output integration, and product qualification remain open.

## Subject

Worktree `/Users/sb/code/opensip-ai/opensip-g2a` is detached at `90e0f36e8018be6f9d6ad4352c18a5c97e362933`. The only untracked paths are the three product files. None of them exist at `HEAD`. `evidence/g2-source-loader.diff` is 9859 bytes, sha256 `167c9a5199280c0ec1900a4952373d24f36013626e68b04e13a6fd34630c270e`. Each added body matches the worktree file byte for byte.

| Path | Bytes | SHA-256 |
|---|---:|---|
| `providers/rust/src/compiler_adapter.rs` | 1012 | `0e97afd6b86988d2a50d4652c6246ced7c0cfd2fc3314a3ed4d5be8c1eedfa44` |
| `providers/rust/src/lib.rs` | 169 | `509caa649bcf00f486754aaa523a338ce057766b21e7349857caa9375464b708` |
| `providers/rust/src/sealed_vfs.rs` | 7814 | `20e7bd8bc9192a12e6bfe908433ec0db3ffbfb864927739c5815784c0cc49d27` |

`providers/rust/Cargo.toml` (291 bytes), `providers/rust/Cargo.lock` (4805 bytes), and `providers/rust/src/main.rs` match `HEAD`. The manifest has edition 2024, `rust-version` 1.95, and no `[features]`. `design-lock.json` matches `HEAD` (544203 bytes, sha256 `dc89d8a622b964bb8f5fc2d0364c55136dc6e28714f079f975c8f761f7f362a8`). `main.rs` still writes the development-build refusal and returns `ExitCode::FAILURE` before reading a request.

M3-PLAN-r10, native-evidence, the accepted S-P report, and `rust-component-pins.json` match the subject authority pins. Plan r10 places G2 authoring after accepted S-P and places lawful launch G2-v after O7 and D1b.

## Loader

The official 1.95 `FileLoader` in `rustc_span::source_map` declares exactly four methods and gives them no defaults: `file_exists`, `read_file`, `read_binary_file`, and `current_directory`. `RealFileLoader` implements them with `path.exists`, `File::open`, and `std::env::current_dir`. `compiler_adapter.rs` implements all four for `SealedSource` and is the private rustc bridge. `lib.rs` exposes only `pub mod sealed_vfs`. The bridge is compiled by the retained driver, which path-includes both files and assigns `config.file_loader` before `after_analysis` returns `Compilation::Stop`.

`SealedSource` stores an absolute virtual directory and a `BTreeMap<PathBuf, Arc<[u8]>>`. The constructor accepts an absolute UTF-8 root of `RootDir` and `Normal` components whose canonical `OsStr` equals the supplied path, and relative non-empty UTF-8 `Normal` names with the same canonical equality. It refuses a duplicate key and a name whose ancestor is already a file. Reads are lexical: an absolute path must strip the virtual directory, `CurDir` is skipped, `ParentDir` pops and refuses an escape, and any other component refuses. `file_exists` is map membership. `read_binary_file` returns the stored `Arc` or `NotFound`. `read_file` uses strict UTF-8 and returns `InvalidData` otherwise. `current_directory` returns the stored path. The three sources contain no `std::fs`, `std::env`, `read_link`, or `canonicalize` call.

The six unit tests share one `Arc` across relative, absolute, `./`, and lexical `..` reads; keep the bytes `00 FF 0D 0A`; refuse invalid UTF-8; refuse `/etc/hosts`, a missing name, escapes, a foreign prefix, a directory prefix, and `SRC/lib.rs`; refuse duplicate and file/directory collisions; refuse noncanonical names and roots; and show that an empty map does not expose an ambient file. Case-collision and logical-path admission stay upstream. The constructor takes admitted names and bytes and does not take a digest, catalog, or context.

## Retained checks

The reviewer did not run rustfmt, Cargo, rustc, `checks.py`, or `acquire.py`. The retained `checks.json` completed at `2026-10-06T16:28:59.146212+00:00` on scratch `/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-g2-source-wtxf3gbn`, with `laneOwned` true and `nice` 10. `T1ProducerRan`, `providerLaunched`, `repositoryCodeExecuted`, `confinementClaimed`, and `productionToolchainSelected` are false. `~/Library/Application Support/OpenSIP` was absent at this review, and the Darwin temp `opensip-lanes.lock` was absent. No `HOME` assignment was made.

`unit-tests.log` records the six `sealed_vfs` tests, 6 passed, 0 failed, after a 0.19s compile. `clippy.log` is the two-line `--lib --tests -D warnings` finish (169 bytes) with no warning text, exit 0. `driver-build.log` is empty and the build exit is 0. The staged `driver.rs` matches `/tmp/opensip-implementation/g2-authoring/driver.rs`. `RUSTC_BOOTSTRAP=1` is set on that wrapper build only. The analysis environment has it removed. The wrapper link line uses `/usr/bin/cc`.

The positive run exits 0 and its log is exactly `SEALED_AFTER_ANALYSIS` plus a newline. The owned virtual entries are `lib.rs`, `helper.rs`, `data.bin` (`00 FF`), and `text.txt` (`sealed`), and the check asserts that `lib.rs` is absent on disk. The missing-module run exits 101 with E0583 for module `forbidden`. The missing-binary run exits 101 because `forbidden.bin` was not found. The invalid-text run exits 101 because `data.bin` is not UTF-8 at byte 255. The physical decoys contain `AMBIENT_FALLBACK_EXECUTED`; no driver log contains that text or `.rmeta`. The check writes `checks.json` only after asserting that the namespace has no `*.rmeta`.

The three cached official 2026-04-16 `aarch64-apple-darwin` archives were rehashed in this review and match the accepted S-P pins and `acquisition.json`: rustc 67652240 bytes `149e85a285b6eba58eb6c8bdf7deb1b93763890598e62cb635a712e3a8454f04`, rust-std 27317176 bytes `9b30089b0f767cb91b2190ffec55a9beeb2a21a1405d8da0f664d7e09d08e6d8`, rustc-dev 118646732 bytes `c9f65810f625b8435c2d4e8486340f93f03f3d7393b4ee2c22865f2444298e48`. `sysroot/bin/rustc` is present. The acquisition standing is authoring toolchain only.

## Inventory v157

Candidate `docs/implementation/m2/repository-file-inventory.v157.json` is 604664 bytes, sha256 `a4a327db896a68e359c8a099aa328176d0152f0e8cd0d176651c5b20a58385fe`. Parent v156 is 604292 bytes, sha256 `4076e785811752ccb9124ce0232e8eba6c420553cddff4550c4401f5d45963a4`. Successor record is 307447 bytes, sha256 `d6016d0b1f1996295f35836b2c9380778b9ec1c1a2c5de9951eac228961561c0`. Subject manifest is 3073 bytes, sha256 `0c37d4d094bb2367e818b4a423da99b7d6ab286cd597a14cf37ea1ed498bf88b`. Its fifteen member hashes match the staged candidate, README, successor, and twelve evidence files. The subject manifest is the only staged file outside that list.

v157 adds exactly `providers/rust/src/lib.rs` at index 801 (package `opensip-rust-provider`, role `entrypoint`, `generated: false`, `standing: proposed`). Its description is the library exposure of this authoring component, with snapshot, context, closure, and lawful launch left separately gated. Files stay sorted and unique. All 1049 parent rows match by value. `packages` and `pendingDecisions` match. The candidate standing sentence remains the v156 I1-b2 sentence. `providers/rust/src/compiler_adapter.rs` and `providers/rust/src/sealed_vfs.rs` were already planned rows and are unchanged. `plannedRowsChanged` is empty. The successor standing names the Rust G2 immutable source-loader authoring component.

The 103 design-lock passages, parented on v156, keep their before and effective text by path. One hundred selectors stay. Because the new file sorts at index 801, three selectors move by one: `schemas/sources/imported-v1.schema.json` from `/files/858/description` to `/files/859/description`, `tools/check_crash_matrix.py` from `/files/891/description` to `/files/892/description`, and `tools/tests/test_check_crash_matrix.py` from `/files/996/description` to `/files/997/description`. No `SCRATCH` pin is in the candidate.

Inventory verdict: ACCEPT. No required findings.

Full G2, G2-v launch under O7 and D1b, T1, confinement, prepared-output and metadata integration, and product qualification remain open.
