# Reproduction / verification account — native-runtime-selection-v7

Not a live activation. Root remains lead.

## Pins verified (this review)

- Unit subject `docs/implementation/m2/native-runtime-selection-v7-subject.json` 15174 / `2ae6ec928066ca62d947990ca66e26e35bd03761c581e00ebe6282910c09730d`; 68/68 members.
- Implementation `docs/implementation/m2/trials/native-runtime-07/subject.json` 45675 / `ba65784df51615858a29e7e81cf4fd010e158081256f43fd0423f61bb0ea1ae4`; archive 2527462 / `b1aa1fbc8549c06270a18f5651206909fb02ec6462b70aee3021f2f797589bee`; export 251/251.
- Materialization map 5/5 vs unit product and export.
- 236 non-lock product files = frozen coverage-producer-17; only `design-lock.json` is live 15/19 (`dee08df9…4d88` / 46495).
- Four parents disk-match; each is a live contract record or inventory **candidate**. Inventory v17 successor **record** is not a parent.
- Archived 17 `report.json` `ea139b48…b79a` / 5783 and `correction.json` `c5646fc0…c78a` / 2849 match `evidence/prior-advisories.json`. Original report.md `f6fdeee2…8593` / 7311 preserved.
- Capability-support-16 subject `b3d1c76c78cf7d6ae43b4673b90d2458f01c8139bbf818076f2bd88d9a16be28`.
- Host fixture 4052701 bytes, under 4 MiB production parser cap.

## Independent commands (rustc 1.95.0, `--locked --offline`)

Export `/tmp/opensip-implementation/m2-native-runtime-subject-07/product`.

```
python -I -B tools/check_identity_dependencies.py \
  --manifest Cargo.toml --target aarch64-apple-darwin \
  --cargo /opt/homebrew/Cellar/rust/1.95.0/bin/cargo \
  --archives $CARGO_REGISTRY_CACHE \
  --policy tools/identity/dependency-policy.json
```

Result: `passed` true, `sourceFilesVerified` 110, tuples sha2-const-stable 0.1.0 / tinyvec 1.13.3 / unicode-normalization 0.1.24.

```
cargo test --locked --offline -p opensip-host coverage_producer --lib
```

Result: `coverage_producer_recomputes_scope_and_preserves_rc3_rc4_rc6` ok.

Static: `coverage.rs` does not call `inspect_plan_native` or 16 prerequisite APIs; identity/policy/capability-support files match live v6.

## Not re-run

436 MiB `coverage-requests.ndjson` harness (archived source review classified frozen 775, 229 ADMIT). Million-scalar Unicode corpus; 07–12 vector corpora. Full 102-test workspace (recorded in host-isolation: 101 crate tests + 1 evaluator doctest).

## Isolation evidence accepted as recorded

Host 118/18, tests 102, help/version 0. Provider 25/14, three honest unavailable. Six composed-base checks exit 0. Preflight standing: v7 still unselected; command paths are `candidate-07`.
