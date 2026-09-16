# Frozen trial review: body-identity-15

**Reviewer:** Grok. Root remains lead. Not Claude agreement.
**Kind:** Scoped source review of private clone body-identity diagnostics. **Not runtime selection. Not full Run/replay/release/product qualification.** Layout v15 is a **separate** accepted inventory unit; this source is **not** live-installed.
**Work tree:** `/tmp/opensip-implementation/m2-grok-body-identity-review-15/review`. Live, frozen, and history not edited. No commits.

The body-join advisory/correction is **not** acceptance and **not** a fresh-blind of this source. That correction is used only for walk-before-Plan order.

## Subject pin

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/implementation/m2/trials/body-identity-15/subject.json` | 51854 | `6539a71f9b7a5b8f437fe5e20788e02b3bccfe45cae44642b79cd2666fc15956` |
| adjacent `subject.tar.gz` / `archive-pin.json` | 90807436 | `192ba5c1a164b1afa0d9882b99f5d0fa5c047b7f609ddd2c2cec900e6bfa2dea` |
| adjacent `body-result.json` | 314 | `17f1ffd3d983f998c5f54a1c2722d2704beb3a71fc24e74dae95f2f6a6bedd4d` |
| adjacent `final-replay-result.json` | 648 | `e89cafc61881ae64d4c62a23a1e22dfd31716e6932d4b6c7a2d587fbc80d5adb` |
| adjacent `oracle-scope-account.json` | 2606 | `b8474a1e78767c6e79d0c0aae5ef01b2d26c384694515d1d9d26358ab04abcaa` |
| export | `/tmp/opensip-implementation/m2-body-identity-subject-15` | 292/292 member pins match; tar 292/292; 0 extra; 0 missing |

292 `files[].path` values are unique and both string-sorted and pathlib-component-sorted.

Dependency pins hash-match: plan-native-14 subject `a08387ba…57e5`; runtime-v4 unit `bee2e5e0…3382`; inventory-v15 subject `09fe80dd…c518`; grok body-join correction `b08790c7…1f9d`; selected native e678 `e6784aa1…e2b9`; selected identity 619d `619d6e3c…41e6`.

Live lock independently observed **13 inventory / 17 contract** (last inventory **candidate** v15 `c761fd99…f28e`; last contract native-runtime v4). Layout v15 is installed as inventory only. Live tree still has no `body_identity.rs` / `body-registry.json`.

## Source delta vs installed runtime v4

Identity `lib.rs` and identity/evaluator `Cargo.toml` are byte-identical to live v4. External dependency TCB unchanged (`sha2-const-stable=0.1.0`, `tinyvec 1.13.3`, `unicode-normalization=0.1.24` default-features=false). Identity source policy **110** files independently passed: only local `src/closure.rs` pin updated `48663/4ea092d6…` → `49900/7f6ea3be…`.

| Path | Role | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| `product/crates/evaluator/src/body_identity.rs` | clone body diagnostic owner | 20453 | `7cb5781c26e2b4fdfb9216544ff5a753be9c9d727073d46f90470d303b49498c` |
| `product/crates/evaluator/src/body-registry.json` | kebab closed extract | 7031 | `a9f7f2cb42407383451d398cd3e47980f7cba9f736deb009cefd999e87d7a538` |
| `product/crates/evaluator/src/lib.rs` | export `inspect_body_identity` | 1146 | `99ac4340eb071130e9100066d961f56a4981bda87a91fa7e526ca7f211caf396` |
| `product/crates/identity/src/closure.rs` | snapshot split + inert derived shape | 49900 | `7f6ea3be2385e4c9f6ff32dda040c3778ab9011df897e271903698d464bf39e2` |
| `product/crates/host/src/native_owner_tests.rs` | integer edition / L0 vs L1 / Unsupported / Limit | 25230 | `5457e96e00d621373b13a3e10bc9cb23b1b34629cf93f3d39648e807d24440ad` |

Unchanged vs live v4: `plan_native.rs`, `native_retention.rs`, `native_universe.rs`, `native-plan-registry.json`. Closed metadata equals the adjacent `body-registry-sources.json` extract of identity-v3 `normalizationSpecificationLaw` + relation-payload-v2 clones row (only `bodyIdentityJoin`; `snapshotJoins` `[]`). Not a caller registry.

Helper refactor: `inspect_relation_sources` now calls `inspect_relation_snapshot` then **still** `Unsupported("relation body identity owner")` when `bodyIdentityJoin` is present. `identity_record_shape` delegates schema/order to `check_identity_value_shape` so derived `body-language-version` can be checked without a retained blob or reference walk.

## Law vs selected I `body_identity_join` (619d 1480–1547) during walk **before** Plan (1650 then 1689)

Public `inspect_body_identity(inputs, fact_id, budget)` — no admission argument, no Plan census, no `inspect_plan_native`:

1. **Budget.** `steps==0` or `depth==0` → `BodyIdentityError::Limit`. Token-stream `count > steps` → `Limit`. Normalization-map schema `SchemaError::Limit` stays `Limit`, not `BODY_NORMALIZATION_MAP_INVALID`.
2. Fact must be relation `clones`. Payload/schema via **`inspect_relation_snapshot`** (not the generic body-refusing sources API).
3. Closed registry join: rehash framed body + level specification bytes. Domain/level/version field joins.
4. **Mandatory frame-input retention:** crate-private `inspect_native_frame_inputs` on the universe (`bind_universe=false`, no early context follow) **then** on the universe’s own `contextField` as `Context`. Context arm still runs **actual** `inspect_native_context`.
5. Interpreting-closure normalization map (missing/member/level/version/order/canonical). Derived compiler/grammar + dialect projection (`check_identity_value_shape` on `body-language-version`). Rust editions are **integers** from selected owning compilation units; missing/partial/uncompiled/unselected/ambiguous ownership refuse. TS/syntax use the body’s longest suffix, including JS vs TS.
6. L0 (`recomputableAt`) recomputes the Python span recipe from the fact anchor; L1–L3 parse retained token framing/custody only. Neither qualifies a normalizer.
7. `RELATION_ANCHOR_LAW_DRIFT` is registry cardinality disagreement only. Extra anchors are not this API’s Plan/full-anchor claim.

Reference `body_identity_join` runs inside `walk` at 1650, **before** the native Plan block at 1689. The separate body-join **correction** already stated that; this source does not require or return a Plan token. Oracle AST uses the ten selected I functions plus body helpers, an explicit **closure-only visit shim**, and **excludes** `syntax_capability_supported` from local `relation_payload_rules`.

Generic identity `inspect_relation_sources` remains Unsupported for clones even after a passing evaluator diagnostic (host test asserts both).

## Reproduction (independent, rustc 1.95.0, `--locked --offline`)

- `cargo test --locked --offline --workspace` on the **export** product: **100** passed (same group sums as frozen `workspace.stdout`). Host `body_identity_uses_integer_rust_editions_and_separates_normalized_custody` ok: L0 goldens, L1 token custody, trailing `BODY_TOKEN_STREAM_TRAILING` (Refused, not Limit), `steps:0` → `Limit`, `inspect_relation_sources` → Unsupported.
- Frozen 965-row actual/expected independently classified: **965/965**, **307 checked**, **0 mismatch**. Extra blob does not change golden digests. JS suffix variants change languageVersion. Rust ownership missing/partial/uncompiled refuse by named cause; target-edition integer changes the projection (`BODY_IDENTITY_LANGUAGE_VERSION_JOIN`, not `RegistryLaw`).
- Initial **927** preserved: 134 mismatches, all `Owner(RegistryLaw)` starting at `golden-rust` (string edition). Corrected927 then 0 mismatch; expanded 965.
- Final replay hashes independently match: body `8228e14c…93f0` / 965, Plan `340d3bdd…4fcb` / 383, retention `591d2c50…5404` / 304, source `0c08af51…39a6` / 161.
- Identity policy independently passed: `sourceFilesVerified: 110`. Frozen `clippy.stderr` is `-D warnings` compile-only (no diagnostics).

Did not re-pipe the 702 MiB `body-requests.ndjson` through a rebuilt harness; comparison used the frozen actual/expected pair plus independent export tests. Did not re-exec Unicode-15 or 07–12 corpora.

## requiredFindings

None.

## Limits (not required findings)

- Local diagnostic counts/fields are not Plan selection, native capability/Coverage, complete anchor path/range admission, full Run, `close_run`, or ReplayedRun.
- Walk-time universe+context retention is not `UNIVERSE_CONTEXT_NOT_SELECTED` / SET_JOIN.
- L0 span uses `min` Python slicing, not full anchor custody.
- `rust-ownership-not-selected` hits nested-record schema mismatch (`invalid`) before `BODY_LANGUAGE_OWNER_NOT_SELECTED`; that named join still exists in source.
- The 965 oracle budget is large; typed `Limit` is covered by host `steps:0` and the map-schema Limit mapping in source.
- Layout v15 acceptance does not install these bytes. Live product still lacks the body owner.

## Verdict

No required findings. Private source matches the selected walk-time body join: closed pinned metadata, mandatory context owner + frame-input retention, interpreter map, derived dialect, integer Rust editions, L0 span vs L1–L3 token custody, identity snapshot split with generic sources still Unsupported, no Plan token. Not a live/runtime/full-Run selection.
