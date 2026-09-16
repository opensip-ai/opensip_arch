# Reproduction / verification account — native-runtime-selection-v9

Not a live activation. Root remains lead.

## Pins verified (this review)

- Unit subject `docs/implementation/m2/native-runtime-selection-v9-subject.json` 14937 / `f7acbd0c2b2ecff3c9c4c8d9df1ae81725b7cfd7f0da361883e0a0dffc7e5029`; 67/67 members.
- Implementation `docs/implementation/m2/trials/native-runtime-09/subject.json` 46237 / `ca9c5a057b8518be5869fcaadd0dd48ea56b071086db117e1ef0cfdea7a2b707`; archive 2219624 / `be555de92330eab8d079e231ddf6f343ea96c5e4a47e5f186fdd0ac3b8a56220`; export 254/254.
- Materialization map 4/4 vs unit product and export.
- 239 non-lock product files = frozen run-links-19; only `design-lock.json` is live 17/21 (`96f8fdb4…7689` / 50518).
- Four parents disk-match; each is a live contract record or inventory **candidate**. Original and corrected inventory-19 successor **records** are not parents.
- Archived 19 `report.json` `1503570d…86c2` / 4971 matches `evidence/prior-advisories.json`.
- Host fixture 1500257 bytes, under 4 MiB production parser cap.
- Original inventory-19 successor 566 / `52ace802…3174` still lacks `inheritedRowsEqualByValue`; corrected 756 / `7970af18…5b82` selected the same candidate.

## Independent commands (rustc 1.95.0, `--locked --offline`)

Export `/tmp/opensip-implementation/m2-native-runtime-subject-09/product`.

```
python -I -B tools/check_identity_dependencies.py \
  --manifest Cargo.toml --target aarch64-apple-darwin \
  --cargo /opt/homebrew/Cellar/rust/1.95.0/bin/cargo \
  --archives $CARGO_REGISTRY_CACHE \
  --policy tools/identity/dependency-policy.json
```

Result: `passed` true, `sourceFilesVerified` 110, tuples sha2-const-stable 0.1.0 / tinyvec 1.13.3 / unicode-normalization 0.1.24.

```
cargo test --locked --offline -p opensip-host run_links --lib
```

Result: `run_links_and_evidence_roots_rehash_their_selected_inputs` ok (36 host controls; `steps:0` Limit; interned body packets restored by `native_fixture`).

Static: identity/policy/prior runtime bodies match live v8; `run_links.rs` calls `admit_plan_capability` and does not call `inspect_plan_native`; foreign capability census is commented as walk-census.

## Not re-run

187 MiB `links-requests.ndjson` harness (archived source review classified frozen 252, 153 checked, 0 mismatch). Million-scalar Unicode corpus; 07–12 vector corpora. Full 104-test workspace (recorded in host-isolation: 103 crate tests + 1 evaluator doctest). Clippy `--deny warnings` recorded on frozen source-19, not re-piped here.

## Isolation evidence accepted as recorded

Host 121/18, tests 104, help/version 0. Provider 25/14, three honest unavailable. Six composed-base checks exit 0. Preflight standing: v9 still unselected; command paths are `candidate-09`.
