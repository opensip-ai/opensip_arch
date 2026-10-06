# Rust G2 declared compiler-tool/context joins r1 — ACCEPT-UNIT

This accepts the pure check of declared compiler-tool joins on one retained Rust context frame. Full native-context admission, G1, full G2, G2-v launch, and product qualification remain open.

## Subject

Worktree `/Users/sb/code/opensip-ai/opensip-g2-context-tools` is detached at `59389ba7cab1768c94bbc85d4807bb72113a391a`. `providers/rust/src/lib.rs` is modified. `compiler_tools.rs` and `compiler_tools_tests.rs` are untracked. `evidence/g2-context-tools.diff` is 22350 bytes, sha256 `e36f05bdf4333abeaa848c4c7edc79e75503b251b66e61fc2df106e493074b2f`. Both new-file bodies match the worktree. The `lib.rs` hunk applied to `HEAD` matches the worktree.

| Path | Bytes | SHA-256 |
|---|---:|---|
| `providers/rust/src/lib.rs` | 218 | `ce3ac89317d207067764528c0448b6653ded0daeb1f4173dfb579606fe884525` |
| `providers/rust/src/compiler_tools.rs` | 7010 | `a90064d9259ca53d46966502be71ace8f3af39d5d478854d46b0d73d4520e245` |
| `providers/rust/src/compiler_tools_tests.rs` | 13901 | `f6b699b888474223baf869fa6c5027fcb5434e479f90659396c6d2f4d4d884f2` |

`HEAD` `lib.rs` is the accepted 194-byte crate root, sha256 `0d0da199a847df62346ed942881cb17834bedf85c83e787b8513b6e1f96645e3`. The hunk adds `pub mod compiler_tools`. `sealed_vfs.rs`, `compiler_adapter.rs`, `source_snapshot.rs`, `main.rs`, `Cargo.toml`, and `Cargo.lock` match `HEAD`. `main.rs` still returns `ExitCode::FAILURE` before reading a request. `design-lock.json` matches `HEAD` (546403 bytes, sha256 `782e92f52107379524d3d191f26a1683d8bdfe01db0fad53e20b990f357a092f`). Its 103 inheritance rows are parented on inventory v158.

`identity-v3.schema.json` and `native-v2.schema.json` match the subject pins. M3-PLAN-r10, native-evidence, snapshot plan C r6, and the bound v157 source-loader unit record match the authority pins. Inventory v158 remains the accepted parent, 605254 bytes, sha256 `db650c79d493c833179c3a5e5e4a73d4eef7a7879545fb9e55be249e05f5ca34`. The accepted loader, snapshot join, and real-driver composition were not re-reviewed.

## Joins

`check_declared_tools` takes retained inputs, a context digest, an expected host digest, and a schema work budget. `frame_candidate` for `NativeFrameSet::Context` rehashes the retained preimage, requires the `opensip.product.v1` frame, admits the current schema selected for that domain, and requires `hash_canonical_value` of the whole admitted value to equal the digest. The domain must be `native.context.rust.v2`.

`toolchain.rustcDevLlvmDigest` is the bare suffix. The check forms `closure2:` plus that suffix and recomputes the closure. `toolClosure.closureId` is used as the closure id directly. Both calls go through `RetainedInputs::object` on `IdentityDomain::Closure`, so domain, canonical bytes, schema, path order, and the full `closure2` identifier are recomputed. The kinds must be `rust-dev-llvm` and `toolchain`. Each closure's `manifestDigest` is rehashed from retained bytes. Every tree row is rehashed and checked against its declared length, including a repeated digest whose lengths disagree. `rustc`, `cargo`, and `procMacroServer` are required digests. Current `ToolClosureV1` allows null only for `linker` and `ar`; a null `rustc` fails frame admission. A non-null digest must be a member of the toolchain tree. `semanticVersion` must equal `toolchain.rustcVersion`. The context `targetTriple` must equal the toolchain `targetTriple`. The expected host digest is compared with the full context frame digest, so a change outside the tool projection, such as `baseCfg`, mismatches.

`CompilerToolChecks` stores that context digest and whether `linker` was non-null. It selects no executable, path, or environment, emits no `NativeContextVerified` frame, and does not read the sysroot, configuration, dependency, feature, or prepared-input digests carried in the same frame. The owned fixture leaves those bytes unretained; the successful subset check still returns. A null linker stays absent. The local error enum is not a new public refusal code.

The eleven tests cover the whole-frame match, an outsider digest for each of the five tools, null `ar` and `linker`, a digest-only dev closure, both kinds after a fresh identity, descriptor substitution under an old id, a missing manifest and each tree member, a substituted blob and a wrong declared length, version and target drift, a host digest that sees `baseCfg`, and a null `rustc` or substituted frame bytes. The tests read the public registered schema sources and do not execute the owned literals.

## Retained checks

The reviewer did not run rustfmt, Cargo, or the script. `checks.json` completed at `2026-10-06T17:03:53.190595+00:00` on scratch `/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-g2-snapshot-5c_5pgl0`, with `laneOwned` true and `nice` 10. `T1ProducerRan`, `providerLaunched`, `repositoryCodeExecuted`, `fullSnapshotAdmission`, `contextAdmitted`, and `productQualification` are false. `~/Library/Application Support/OpenSIP` was absent at this review, and the Darwin temp `opensip-lanes.lock` was absent. No `HOME` assignment was made.

`unit-tests.log` records 27 tests, 0 failed, 0.12s, after a 16.90s compile: the sixteen accepted source-component tests and the eleven new join tests. `clippy.log` is the `--lib --tests -D warnings` finish (866 bytes) with no warning text, exit 0.

## Inventory v159

Candidate `docs/implementation/m2/repository-file-inventory.v159.json` is 606434 bytes, sha256 `f09cbcbc21482693ae9febda2bf295dd563df643cbac9ed56cfa763060c45eb2`. Parent v158 is 605254 bytes, sha256 `db650c79d493c833179c3a5e5e4a73d4eef7a7879545fb9e55be249e05f5ca34`. Successor record is 307522 bytes, sha256 `ef2021e03e9343e2389ac64c9f7ad0878b26c1c94092eaa515524dc63494ba38`. Subject manifest is 1443 bytes, sha256 `02e1799534a90312137403f2652f9bca414bb6c1ab972c6d390da15d2b232e94`. Its seven member hashes match the staged candidate, README, successor, and four evidence files. The subject manifest is the only staged file outside that list.

v159 adds `providers/rust/src/compiler_tools.rs` at index 797 (package `opensip-rust-provider`, role `validator`, `generated: false`, `standing: proposed`) and `providers/rust/src/compiler_tools_tests.rs` at index 798 (role `test`). Files stay sorted and unique. All 1051 parent rows match by value. `packages` and `pendingDecisions` match. The candidate standing sentence remains the v158 I1-b2 sentence. `plannedRowsChanged` is empty. The successor standing names the Rust G2 declared compiler-tool/context joins.

The 103 design-lock passages, parented on v158, keep their before and effective text by path. One hundred selectors stay. Because both new files sort at indexes 797 and 798, three selectors move by two: `schemas/sources/imported-v1.schema.json` from `/files/860/description` to `/files/862/description`, `tools/check_crash_matrix.py` from `/files/893/description` to `/files/895/description`, and `tools/tests/test_check_crash_matrix.py` from `/files/998/description` to `/files/1000/description`. No `SCRATCH` pin is in the candidate.

Inventory verdict: ACCEPT. No required findings.

Signature, sysroot, standard-library, configuration, dependency, unified-feature, prepared-input, compiler-metadata, and process-policy admission remain upstream. Full G2, G2-v launch, and product qualification remain open.
