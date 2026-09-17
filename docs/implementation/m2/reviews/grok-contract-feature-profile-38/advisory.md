# Advisory: contracts feature profiles (standalone vs toml-workspace)

**Reviewer:** Grok. Root remains lead. Not Claude agreement.  
**Kind:** Architecture/runtime-selection requirements for an explicit contracts feature lane. **Not approval. Not parser-38, source, or runtime acceptance.**  
**Work tree:** `/tmp/opensip-implementation/m2-grok-contract-feature-profile-38` only. No live/frozen/history edits.

Private source38 provider **build succeeded**. Contracts checker **correctly refused** workspace metadata `serde_core ['alloc','result','std']` against the historical selected `['result','std']`. Isolation-18 invoked trial-38 `check_dependencies.py` on `providers/rust/Cargo.toml` **without** `--feature-profile` (commands.json; expected 0, got 1).

Live checker still has a single `resolvedFeatures` map (no profiles). Trial-38 already drafts selectable profiles; that source is **not frozen**.

## Verdict

Keep **exact** historical standalone enforcement. Add **one** named extra profile, `toml-workspace`, that differs **only** by `serde_core` gaining metadata feature `alloc`. Host and rust-provider **must** pass `--feature-profile toml-workspace`. Standalone contracts (generator / isolated `crates/contracts`) keep the default `standalone` lane. **Do not** auto-union, auto-detect, or rewrite `contracts-dependency-selection-v1` pins.

`alloc` on `serde_core` in workspace **metadata is not the compiled feature set.** `cargo tree -e features` and the rustc fingerprint for the isolation provider build compiled `serde_core` as `["result","std"]` only. The toml-workspace lane is a **metadata-census** exception for the existing checker, not a claim that `cfg(feature = "alloc")` was rustc-enabled.

## Independent evidence

| Probe | Result |
| --- | --- |
| Isolation `cargo metadata` resolve `serde_core@1.0.229` | features `['alloc','result','std']` |
| Isolation rustc fingerprint `lib-serde_core.json` | `"features":"[\"result\", \"std\"]"` |
| `cargo tree -e features` (provider, identity, contracts) | `serde_core` only `result` and `std`; identity tree has **no** `serde_core` |
| Identity `serde_spanned`/`toml_datetime` | `alloc = ["serde_core?/alloc"]` weak; `inactiveOptionalDependencies: serde_core` |
| `serde_core` 1.0.229 `[features]` | `alloc = []`, `std = []` (orthogonal; `std` does not list `alloc`) |
| Isolation checker argv | no `--feature-profile` → default `standalone` → refuse |

Cause: Cargo **feature unification in `cargo metadata`** reports weak `serde_core?/alloc` from the TOML helper crates onto the workspace `serde_core` node because contracts **does** compile `serde_core`. Weak `?` does **not** make `serde_core` a compiled dependency of identity (`cargo tree` identity has none). The contracts checker walks metadata `node['features']`, so it sees `alloc` even when rustc did not pass `--cfg feature="alloc"`.

## Requirements (actionable)

### 1. Two explicit profiles, never a union

- **`standalone`** (default): `policy.resolvedFeatures` unchanged from selected contracts-dependency-selection-v1 / `sourceOwner` `docs/implementation/m1/contracts-dependencies.v1.json`. `serde_core = ["result","std"]`. Eleven checksums and eight local source pins stay.
- **`toml-workspace`**: `policy.resolvedFeatureProfiles.toml-workspace`, same eleven crates and every other feature list **byte-equal** to standalone except `serde_core = ["alloc","result","std"]` (sorted). No other crate may grow features in this profile.

`standalone` must not appear as a key inside `resolvedFeatureProfiles` (trial-38 checker already refuses that). Unknown profile names refuse.

### 2. Caller selects the lane; checker does not infer it

- Default `--feature-profile standalone` (conservative). Workspace presence of identity/TOML **must not** switch lanes automatically (would hide a third member enabling `serde_core/rc` or `serde_json/raw_value`).
- Rust-provider isolation, host workspace, and any metadata whose resolve root includes both `opensip-contracts` and `opensip-identity` (TOML): **`--feature-profile toml-workspace`**.
- Isolated contracts package / generator (`opensip-contract-generator` / `[workspace]` around `crates/contracts` only): **omit the flag** or pass `standalone`.
- `toml-workspace` metadata of an isolated contracts crate **must refuse** (observed `['result','std']` ≠ wanted `['alloc',…]`). Trial-38 `test_standalone_preserves_original_profile` already encodes this.

### 3. Do not rewrite prior contracts history

Do not edit selected `resolvedFeatures` to include `alloc`. That would make standalone generator metadata fail and would alter contracts-dependency-selection-v1 law. The extra profile is additive.

### 4. Identity stays a separate census

Identity parse-only graph still must not compile `serde_core`. Identity checker + `tools/identity/dependency-policy.json` remain the authority for toml/winnow/`inactiveOptionalDependencies`. Do not fold identity crates into the contracts 11-name closure. A workspace metadata run of the **identity** checker must continue to treat `serde_core` as inactive optional on spanned/datetime, not as a new identity production dep.

### 5. Isolation/host command change

Isolation-18 `dependencies` command needs `--feature-profile toml-workspace` (and expected 0 **after** that profile is selected, not before). Same for host isolation. Missing flag must keep failing. That failure is correct.

### 6. Metadata vs compiled: document, do not equate

Runtime/source selection notes must say: toml-workspace accepts **Cargo metadata** `alloc` on `serde_core`. Independent compiled census (`cargo tree -e features`, rustc fingerprint `features`) remains `result`+`std`. A later **compiled-feature** checker would be a new obligation; this lane does not replace it and must not claim `cfg(feature="alloc")`.

`serde_core` with `std` already uses libstd (which includes alloc). The extra `feature = "alloc"` only adds `extern crate alloc` for no_std. Contracts is std. So metadata `alloc` is a census delta, not a new host I/O surface.

## Tests (required before selecting this checker)

Already drafted in trial-38 `test_dependency_policy.py` — keep and run:

1. Workspace metadata + `toml-workspace` passes; reports `featureProfile`.
2. Workspace + `standalone` refuses `serde_core` actual `['alloc','result','std']`.
3. Isolated contracts + `standalone` passes `['result','std']`; + `toml-workspace` refuses.
4. Unknown profile refuses.
5. Profile must cover exact dependency names; features sorted unique; `standalone` key forbidden under `resolvedFeatureProfiles`.
6. Another workspace member cannot expand `serde_json` (or any non-`serde_core` list) even under `toml-workspace`.
7. Local source byte/path census unchanged.

Add isolation-level control: provider export `check_dependencies.py --manifest providers/rust/Cargo.toml --feature-profile toml-workspace` exit 0; same without the flag exit 1.

Do not weaken `check_sources` or checksum equality.

## What this is not

Not parser-38/TOML crate acceptance. Not identity dependency-policy selection. Not a blanket “workspace features = union of members.” Not changing the 11 crate pins. Not claiming compiled `alloc`. Not Claude agreement. Root implements and decides when this checker/policy is a source unit.
