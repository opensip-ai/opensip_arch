# Rust G2 declared universe/context field joins r1

Verdict: ACCEPT-UNIT.

`check_declared_universe_context` recomputes the current Rust context frame and the semantic-universe frame, then checks the native §2.1 overlapping fields. `UniverseContextChecks` records the two digests, the cfg-set count, and whether preparation consumed inert products. It is not `bind_rust_universe`, a native admission, `NativeContextVerified`, Plan binding, or an execution grant. Full G2, provider launch, and product qualification stay open.

## Field joins

Both frames are loaded and domain-checked (`native.context.rust.v2`, `native.semantic-universe.rust.v2`) before the host digest and `nativeContextId` comparisons. The host check uses the full context digest. `nativeContextId` must be `sha256:` plus that digest.

`dependencySourceSetId`, `unifiedFeaturesId`, and `preparedOutputSetId` are compared with `JsonValue` equality, as is the whole `rustflags` object against `configProjection.rustflags`, so honored and stripped sequences keep their order. `configProjectionSha256` is `digest_hex` of `hash_canonical_value("native.cargo-config-projection.v2", projection)`, the H identity of the whole projection. It is not `projectionSha256` and not the raw SHA-256 of the canonical projection bytes.

`executionCapableResolution` must equal `preparedResolution != "none"`. `preparedOutputSetId` is null exactly in that `none` case. Every cfg set must contain every `baseCfg` member, and `cfgSetId` values are unique even when the cfg payloads differ. The function does not select extra cfgs or apply a flag allowlist, and it does not reorder the declared sequences. Local errors are `UniverseContextError` values, not wire refusal strings. The library performs no filesystem, tool, compiler, provider, or measurement call. Empty nested and snapshot fixtures do not stand in for the remaining binding joins.

The worktree is detached at `0cc355582b4dde21b7282b7061d879bd141d2eab`. The only product changes are `lib.rs` adding `universe_context`, plus the two new files. The evidence diff is 23941 bytes, sha256 `11d42dbf5b593d8e6dc4187e06795a613afea9073561eb4bff96bab969ab8c71`, and the two new-file bodies match the worktree. Pinned schemas and the four architecture authorities match. The author log records 49 library tests, including the 11 new universe-context tests, and warning-denied Clippy, both exit 0, under `nice -n 10` and a mode `0700` scratch. This review did not rerun Cargo, rustfmt, or Clippy.

## Inventory

Subject manifest sha256 `b4066c12a39fa57d769b444864e6bd04f492d7bf8eab6991d93d9b5c97a29a4a` (1461 bytes). Its seven files match.

Candidate `repository-file-inventory.v162.json` is 609843 bytes, sha256 `410352b3e06ee724734a6971fe078ea0b908891fa757f389cbcb5e856e6afa26`. Parent v161 is 608759 bytes, sha256 `e2ebb6cb8ac26dc97872d55190bd9cbd8c68f8e8c6f1acd2f5c424952f2b9c76`. Successor `docs/implementation/m2/rust-g2-universe-context-inventory-v162/successor.json` is 307528 bytes, sha256 `79bba9b426900ee2e41fe7335cee383545c8c06fc506a84577e561dcf1ccc693`.

v162 has 1059 sorted unique paths. The additions are `providers/rust/src/universe_context.rs` at index 811 (package `opensip-rust-provider`, role validator) and `providers/rust/src/universe_context_tests.rs` at index 812 (role test). All 1057 parent rows are unchanged. Packages stay 20 and pending decisions stay 9. The candidate standing sentence remains the v161 I1-b2 sentence. The successor standing names the Rust G2 declared universe/context field joins. All 103 description projections keep the v161 before and effective text, keyed by stable path. Three selectors move by two: `schemas/sources/imported-v1.schema.json` 864 to 866, `tools/check_crash_matrix.py` 897 to 899, and `tools/tests/test_check_crash_matrix.py` 1004 to 1006.
