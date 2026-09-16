# Reproduction / verification account — native-runtime-selection-v8

Not a live activation. Root remains lead.

## Pins verified (this review)

- Unit subject `docs/implementation/m2/native-runtime-selection-v8-subject.json` 15414 / `44c05d8104d9bbe2dc605021301f330090edcb80ba34cd367731746b8f96969e`; 69/69 members.
- Implementation `docs/implementation/m2/trials/native-runtime-08/subject.json` 46034 / `aaed9d1cfbc2c477e8a65cb84b2fed818ea985697142936fbad85372fa2525c2`; archive 2550968 / `292ee424631dfcd53b8ae790badbd7eb7878255a98842aea250f484a119f95cc`; export 253/253.
- Materialization map 6/6 vs unit product and export.
- 238 non-lock product files = frozen view-joins-18; only `design-lock.json` is live 16/20 (`f23a451b…4b2c` / 48493).
- Four parents disk-match; each is a live contract record or inventory **candidate**. Inventory v18 successor **record** is not a parent.
- Archived 18 `report.json` `e09eba33…8cdc` / 5499 matches `evidence/prior-advisories.json`.
- Host fixture 4160885 bytes, under 4 MiB production parser cap.

## Independent commands (rustc 1.95.0, `--locked --offline`)

Export `/tmp/opensip-implementation/m2-native-runtime-subject-08/product`.

```
python -I -B tools/check_identity_dependencies.py \
  --manifest Cargo.toml --target aarch64-apple-darwin \
  --cargo /opt/homebrew/Cellar/rust/1.95.0/bin/cargo \
  --archives $CARGO_REGISTRY_CACHE \
  --policy tools/identity/dependency-policy.json
```

Result: `passed` true, `sourceFilesVerified` 110, tuples sha2-const-stable 0.1.0 / tinyvec 1.13.3 / unicode-normalization 0.1.24.

```
cargo test --locked --offline -p opensip-host view_joins --lib
```

Result: `view_joins_keep_partition_totality_and_unresolved_census_local` ok.

Static: `capability_support.rs` vs live v7 is `pub(crate) fn eligibility` only; identity/policy/coverage files match live v7; `view_joins.rs` does not call `inspect_plan_native`.

## Not re-run

177 MiB `view-requests.ndjson` harness (archived source review classified frozen 241, 158 checked). Million-scalar Unicode corpus; 07–12 vector corpora. Full 103-test workspace (recorded in host-isolation: 102 crate tests + 1 evaluator doctest).

## Isolation evidence accepted as recorded

Host 120/18, tests 103, help/version 0. Provider 25/14, three honest unavailable. Six composed-base checks exit 0. Preflight standing: v8 still unselected; command paths are `candidate-08`.
