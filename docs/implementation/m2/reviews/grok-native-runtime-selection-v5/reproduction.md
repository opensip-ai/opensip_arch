# Reproduction / verification account — native-runtime-selection-v5

Not a live activation. Root remains lead.

## Pins verified (this review)

- Unit subject `docs/implementation/m2/native-runtime-selection-v5-subject.json` 15631 / `f943b844e9e756d57449c126c5eb5facf07cdb63b169e85b1be14faf7738acd2`; 70/70 members.
- Implementation `docs/implementation/m2/trials/native-runtime-05/subject.json` 45966 / `1e31dafa3f07e0c5d24ee82223951146515f65f86b242e469e094ad8d11ef552`; archive 2486632 / `64c8fb5886d1c3f14fe4194f0375eabdcfb2fce7bf6b213ae25ead94d64d374b`; export 253/253.
- Materialization map 7/7 vs unit product and export.
- 232 non-lock product files = frozen body-identity-15; only `design-lock.json` is live 13/17 (`dddad14a…d6a5` / 42459).
- Four parents disk-match; each is a live contract record or inventory **candidate**. Inventory v15 successor **record** is not a parent.
- Archived body15 `report.json` pin matches `evidence/prior-advisories.json` (`dc26af16…4c57` / 6314).

## Independent commands (rustc 1.95.0, `--locked --offline`)

Export `/tmp/opensip-implementation/m2-native-runtime-subject-05/product`.

```
python -I -B tools/check_identity_dependencies.py \
  --manifest Cargo.toml --target aarch64-apple-darwin \
  --cargo /opt/homebrew/Cellar/rust/1.95.0/bin/cargo \
  --archives $CARGO_REGISTRY_CACHE \
  --policy tools/identity/dependency-policy.json
```

Result: `passed` true, `sourceFilesVerified` 110, tuples sha2-const-stable 0.1.0 / tinyvec 1.13.3 / unicode-normalization 0.1.24.

```
cargo test --locked --offline -p opensip-host body_identity --lib
```

Result: `body_identity_uses_integer_rust_editions_and_separates_normalized_custody` ok.

Static: `body_identity.rs` does not call `inspect_plan_native`; `closure.rs` still returns `Unsupported("relation body identity owner")`.

## Not re-run

702 MiB `body-requests.ndjson` harness (archived source review classified the frozen 965 pair; did not re-pipe). Million-scalar Unicode corpus; 07–12 vector corpora. Full 100-test workspace (recorded in host-isolation: 99 crate tests + 1 evaluator doctest). Root already recorded 965+383+304+161 byte-identical suites.

## Isolation evidence accepted as recorded

Host 114/18, tests 100, help/version 0. Provider 25/14, three honest unavailable. Six composed-base checks exit 0. Preflight standing still says “v4 … unselected”; README discloses that; command paths are v5. Provider edges used inventory v12; those provider rows are unchanged in v15.
