# Reproduction / verification account — native-runtime-selection-v4

Not a live activation. Root remains lead.

## Pins verified (this review)

- Unit subject `docs/implementation/m2/native-runtime-selection-v4-subject.json` 16347 / `468f76a4467eb73c84ab9fcd837654134215f765e15933b0479e72a605baa9ab`; 73/73 members.
- Implementation `docs/implementation/m2/trials/native-runtime-04/subject.json` 45234 / `a40cb2ced4e0fc3d44c0e5fe54563d7269234afa577a6456c9a66638d3ff5caf`; archive 2007484 / `36fbf822173ec3e5b0285ec5460bec5a3b928524f65e3e75769a119abe00615a`; export 249/249.
- Materialization map 10/10 vs unit product and export.
- 230 non-lock product files = frozen plan-native-14; only `design-lock.json` is live 12/16.
- Four parents disk-match; each is a live contract record or inventory **candidate**.
- Five archived 10–14 advisory `report.json` pins match `evidence/prior-advisories.json`.

## Independent commands (rustc 1.95.0, `--locked --offline`)

Export `/tmp/opensip-implementation/m2-native-runtime-subject-04/product`.

```
python -I -B tools/check_identity_dependencies.py \
  --manifest Cargo.toml --target aarch64-apple-darwin \
  --cargo /opt/homebrew/Cellar/rust/1.95.0/bin/cargo \
  --archives $CARGO_REGISTRY_CACHE \
  --policy tools/identity/dependency-policy.json
```

Result: `passed` true, `sourceFilesVerified` 110, tuples sha2-const-stable 0.1.0 / tinyvec 1.13.3 / unicode-normalization 0.1.24.

```
cargo test --locked --offline -p opensip-host plan_native --lib
```

Result: `plan_native_preserves_selection_and_preparation_fault_order` ok.

Static: `plan_native.rs` still emits `UNIVERSE_CONTEXT_NOT_SELECTED` before `frame_candidate(Context)` and grant after bind.

## Not re-run

Million-scalar Unicode corpus; syntax/TS/Rust 10–12 vector corpora; full 383/304 oracles (bytes identical to frozen 14, already independently replayed in the archived 14 advisory). Full 99-test workspace (recorded in host-isolation: 98 crate tests + 1 evaluator doctest).

## Isolation evidence accepted as recorded

Host 112 sources / 18 archives; provider 25 / 14; three unavailable exit 1; source-guard 64; design generation 40 / admission 48 / aliases 15; contracts-dependencies 11 (contracts crate, not identity TCB); metadata + package-edge DAG.
