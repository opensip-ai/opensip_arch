# Reproduction / verification account — native-runtime-selection-v6

Not a live activation. Root remains lead.

## Pins verified (this review)

- Unit subject `docs/implementation/m2/native-runtime-selection-v6-subject.json` 15650 / `a281b51ef4f07383cb50bfeeb86138624b98685310e71f69b453cbce8e57b547`; 70/70 members.
- Implementation `docs/implementation/m2/trials/native-runtime-06/subject.json` 45305 / `96d012a4d0d5d2975e4c4744b894729c8336bf69b9904863235940db4661f77b`; archive 2518666 / `95d33a24807178ae22930b07a627ba142973a61726e7f415621656033bcfe477`; export 249/249.
- Materialization map 7/7 vs unit product and export.
- 234 non-lock product files = frozen capability-support-16; only `design-lock.json` is live 14/18 (`b3aff3e9…bc16` / 44479).
- Four parents disk-match; each is a live contract record or inventory **candidate**. Inventory v16 successor **record** is not a parent.
- Archived capability-support-16 `report.json` pin matches `evidence/prior-advisories.json` (`d8aed94f…60d6` / 6450).
- Host fixture 4158383 bytes, under 4 MiB production parser cap.

## Independent commands (rustc 1.95.0, `--locked --offline`)

Export `/tmp/opensip-implementation/m2-native-runtime-subject-06/product`.

```
python -I -B tools/check_identity_dependencies.py \
  --manifest Cargo.toml --target aarch64-apple-darwin \
  --cargo /opt/homebrew/Cellar/rust/1.95.0/bin/cargo \
  --archives $CARGO_REGISTRY_CACHE \
  --policy tools/identity/dependency-policy.json
```

Result: `passed` true, `sourceFilesVerified` 110, tuples sha2-const-stable 0.1.0 / tinyvec 1.13.3 / unicode-normalization 0.1.24.

```
cargo test --locked --offline -p opensip-host native_support --lib
```

Result: `native_support_uses_selected_suffixes_and_derives_empty_view_disclosures` ok.

Static: `capability_support.rs` does not call `inspect_plan_native`; `closure.rs` still returns `Unsupported("relation body identity owner")` and adds `registered_record_shape`.

## Not re-run

476 MiB `support-requests.ndjson` harness (archived source review classified frozen 660+8). Million-scalar Unicode corpus; 07–12 vector corpora. Full 101-test workspace (recorded in host-isolation: 100 crate tests + 1 evaluator doctest). Root already recorded 660 and 965+383+304+161.

## Isolation evidence accepted as recorded

Host 116/18, tests 101, help/version 0. Provider 25/14, three honest unavailable. Six composed-base checks exit 0. Preflight standing: v6 still unselected; command paths are `candidate-06`.
