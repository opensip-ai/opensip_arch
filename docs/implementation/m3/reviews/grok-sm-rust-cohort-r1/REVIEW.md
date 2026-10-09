# S-M-RUST-DIRECT-LIBRARY-COHORT-PARTIAL-R1

ACCEPT. These are preliminary direct-rustc virtual-source library-cohort observations for the seven Rust medium dev repositories and the named serde-json overlay. SM-4, SM-11, full S-M, L-G1, effective L, source admission, confinement, and product qualification stay open. Accepted S-P, the earlier S-M records, the owner decisions, and the L law stay closed.

## Subject

`subject.json` is 226850 bytes, SHA-256 `314350b4ae853398c724306d903191652483c28fb55e7c87130b10b9b920b15e`, schemaVersion 1, unit `S-M-RUST-DIRECT-LIBRARY-COHORT-PARTIAL-R1`. It pins 1000 sorted unique members, and every hash matches the stage. The archive path `docs/implementation/m3/spikes/s-m-rust-typecheck-2026-10-09` is absent at architecture `2aeee986365db187b2510164ec3cea7fde54da03` (log: “Record preliminary sealed TypeScript configuration cohort measurements.”). Product `37581132d8099b8fb4ad9ef8fb2f90ff8b89d02d` is clean. The architecture tree’s only untracked path is `docs/implementation/m3/syntax-e/e2s/`, outside this packet. Product `design-lock.json` remains 615658 bytes, SHA-256 `018dbfe27c1bbba48dedcf88ff6625ce62072b01bfb0fae0aee8c3dc463fc283`, with inventory v179, 139 inventory successors, and 155 contract successors. The packet names none of those successors. The recorded host is macOS 27.0.1, build `26A434`.

The nine authority pins match that architecture tree, including L-law `PROPOSAL-r5.md` at 172198 bytes, SHA-256 `f654ee4e9149e62693ebae8177adcc1f3a8a595b745c1e7503e5f279b80e3e88`, and the T2 manifest at 322483 bytes, SHA-256 `c8cc48e1549a05e9d563728fcac776ceca6c2ba63fa2004779385bd2fa4b7578`.

## Driver

The wrapper is first-party `rustc_driver` code, 3885 bytes, SHA-256 `e19c84cd6f9d9fbb6d1b732d04020b611370c3e94581a320beb7a0bcf7acb17f`. The build invokes the retained sysroot `rustc` directly, with `RUSTC_BOOTSTRAP=1` only in that build environment. The retained first-attempt log records the two pinned API mismatches: no `Lrc` in `rustc_data_structures::sync`, and `FileLoader` missing `current_directory`. The retained driver implements `current_directory` and returns `Arc<[u8]>` from `read_binary_file`. Its successful build log is empty. The executable is 180840 bytes, SHA-256 `47da498d466972cd2e2bc0ccf3d3f72533f0ac946882c0853b99320ea86faa3e`, and the bytes still on disk match that pin.

The retained sysroot `rustc` is 412504 bytes, SHA-256 `b829b733131d4e1673eeebd1f34d06ae1e9ff4977b051313cf42e2a9e79ecf1c`. `librustc_driver` is 203876200 bytes, SHA-256 `d41766d9ed6e9c7959eeb7678b9a6bb301f70948664cd39a8a0d2d83ad23d54e`, and those bytes contain the version `1.95.0` and commit `59807616e`. Both files match the packet’s runtime pins. This review did not rebuild the wrapper.

`config` installs that `FileLoader` before parsing. Source text and binary reads resolve through lexical absolute-path normalization against the in-memory map. A miss increments the denied counter and returns not-found. The driver’s only filesystem read of its own is the prepared map. Compiler metadata and runtime IO, including the sysroot, sit outside that callback. The boundary is the SourceMap callback. `sourceAdmissionClaimed` and `confinementClaimed` stay false. `after_analysis` returns `Compilation::Stop`. The child command passes `--emit metadata`, and the measurement asserted each owned output directory was empty before removing it.

Analyzed children receive a fresh environment of `PATH`, `CARGO_HOME`, `TMPDIR`, `HOME` when already set, and `LANG`, `LC_ALL`, and `TZ` when already set. `RUSTC_BOOTSTRAP` is absent from that environment. The command has no `--extern`. No build script, package script, or proc-macro native code is launched.

## Cohort rows

The seven workloads are `counts.rust.medium.devIds`, in that order, followed by workspace `mr-rs-medium-serde-json`. Every repository and both overlay members have `heldOut` false. Each recorded verification pair equals that repository’s T2 tree digest and content digest. This review did not call `store.verify`. The overlay definition’s canonical digest equals the manifest’s `overlayDigest`, and each named mount is a symlink to that member’s store directory.

This review walked each member with `followlinks` false, re-read every regular file with `O_NOFOLLOW`, and checked inode, size, and timestamps. The sorted path, byte, and SHA-256 rows match the inventories: 644, 567, 498, 138, 347, 92, 883, and 439 for the overlay. The overlay count is the serde and serde-json row counts together. Nonregular and symlink-directory exclusions match. Rebuilding each prepared map from those bytes and the retained absolute names reproduces `sourceMapSha256`. The map files themselves were removed after the measurement. The inventories keep the rows, the digest, and the argv fields.

Library selection is every retained `Cargo.toml` with a package and a retained explicit or default library root. Replaying that selector on the rehashed bytes reproduces every library root and every skipped manifest. The skip reasons that occur are `no-package-declaration` and `no-retained-declared-library-root`. Edition is the package edition, or a string edition from a retained ancestor workspace manifest when the package asks for the workspace edition. Default-feature labels are the bare local names reachable from `features.default`. Labels containing `/` or beginning with `dep:` are left out. Every selected root records `buildScriptExecuted` false and `dependencyExternsSupplied` false. Five selected roots use crate type `proc-macro`. None of those five is among the roots that reach `after_analysis`.

Eight root sets contain 48 roots. Each set has three warmup passes and seven measured passes, one fresh child per root: 480 children. Phase, exit, callback events, and read counts are identical across the ten passes of each root. Stderr error-code sets match `checks.json`. Seven roots reach `after_analysis` with exit 0 on all ten passes, 70 children. The other 41 roots stay short of `after_analysis`, 410 children. Exit codes in the retained rows are 0 and 101. No native failure route is inferred from exit 101 or from the diagnostic text.

The seven roots that reach `after_analysis` are the three `optional-napi-derive` fixture libraries, `crates/build/src/lib.rs`, `tests-build/src/lib.rs`, `tests-integration/src/lib.rs`, and `tokio/src/lib.rs`.

| Workload | Library roots | After-analysis roots | Median root-set ns | Max root-set ns |
| --- | ---: | ---: | ---: | ---: |
| poly-medium-napi-rs | 18 | 4 | 2556407542 | 2563789250 |
| rs-medium-aws-lambda-rust-runtime | 6 | 0 | 1795055917 | 1817478042 |
| rs-medium-axum | 4 | 0 | 645128250 | 646790875 |
| rs-medium-hyper | 1 | 0 | 41487333 | 42037834 |
| rs-medium-serde | 4 | 0 | 511129250 | 521599083 |
| rs-medium-serde-json | 2 | 0 | 290329125 | 420399542 |
| rs-medium-tokio | 7 | 3 | 417672166 | 421651750 |
| mr-rs-medium-serde-json | 6 | 0 | 805380583 | 808975334 |

The median and maximum are the seven measured whole-root-set spans. Each span runs from before the set’s first child through the last child, so it includes spawn, runtime, map decode, failed and successful invocations, and output-directory bookkeeping. `progress.json` carries the same medians and maxima. These spans are the cohort’s recorded cost, including the 41 incomplete roots.

Native `wait4` `ru_maxrss` is stored as `rssNative` with unit `bytes`. The ranges are napi 75907072–321372160, aws-lambda 64569344–163332096, axum 92995584–157810688, hyper 97320960–97533952, serde 47693824–260587520, serde-json 52019200–170082304, tokio 65781760–133054464, and the overlay 49250304–261455872. They stay informational. Empty output directories are the measurement’s per-child assertion. They are not a peak-scratch measurement.

SM-4 in the accepted L law is Rust analysis through type checking, with build-script and proc-macro expansion disclosed as unavailable. These rows are an exploratory per-library direct-rustc cohort. Forty-one roots do not reach `after_analysis`, dependency externs and generated build output are absent, and the recorded times include the failed roots. `SM4PlaceholderFilled` stays false. SM-11 is SM-4’s time, SM-10’s peak RSS, and the worker’s peak scratch, each divided by the measured subject count. This packet has no such per-subject quotient. `SM11PlaceholderFilled` stays false. No F or T budget is derived.

## Controls

Six synthetic controls are retained. The positive crate reaches `after_analysis` with exit 0, one read, and zero denied reads. The nested crate reaches `after_analysis` with exit 0 and four reads: the root, the child module, `include_str!`, and `include_bytes!`, with zero denied reads. The type-error crate reaches `after_expansion`, records E0308, exits 101, and does not reach `after_analysis`. The missing `OUT_DIR` crate and the unavailable `absent_derive` crate likewise reach `after_expansion`, exit 101, and do not reach `after_analysis`. The denied include reaches `after_expansion` with `readCalls` 2 and `deniedReadCalls` 1, exits 101, and does not reach `after_analysis`. Its stderr contains the outside-map denial once. The marker text is absent from the retained source map. The control script checked that owned marker’s digest after the run. That denial is the in-memory map’s answer. `confinementClaimed` is false.

## Disposition

`verify_design.py` was not run. Archival is architecture-only, after this acceptance, root assent, and the actual design check. This review binds no lock and pushes nothing. Inventory stays 179. Contract successors stay 155. Product code stays unchanged.
