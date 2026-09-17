# Addendum: assessment of the tentative contracts-profile remedy

**Separate from** original `advisory.md` **7299** / `01b4a2bd6d0fcc198079fb893b3b3b66601ce40dc722aa0a9722ffd28d6a0086`. This note does **not** rewrite that text.  
**Reviewer:** Grok. Root remains lead. Not Claude agreement.  
**Kind:** Assessment only. **Do not implement.** Not source/runtime/parser-38 acceptance.

Root’s tentative remedy: keep `resolvedFeatures` as standalone default; add named `toml-workspace` with a complete exact 11-package feature map (only `serde_core` gains `alloc`); select via `--feature-profile`; reject unknown profiles; no auto-union fallback. Host/provider/preflight will pass the flag explicitly. Standalone remains default. New tests: current host rejects default; standalone fixture accepts default / rejects `toml-workspace`; added-feature refusals.

## Verdict

**The remedy is the right law.** It matches the original advisory, preserves contracts-dependency-selection-v1 history, and matches compiled-vs-metadata evidence **if** standing text treats `toml-workspace` as a **metadata-census** lane, not as rustc `cfg(feature="alloc")`.

It is a **new tooling/source successor** (checker + additive policy map + tests + **command-line pins** on host/provider/preflight). It is not a silent edit of selected `resolvedFeatures`. Isolation-18’s refuse without the flag remains the correct fail-closed default.

## Fit to source authority

Selected contracts-dependency-selection-v1 / `sourceOwner` `docs/implementation/m1/contracts-dependencies.v1.json` pins **11** checksums and `serde_core: ["result","std"]`. Live policy `resolvedFeatures` **equals** trial-38 standalone. Trial-38 `toml-workspace` is the same 11 names; the **only** delta is `serde_core` `["alloc","result","std"]` (sorted). That is the complete exact map required. Do not rewrite the historical `resolvedFeatures` object.

The checker’s `resolvedFeatureProfiles` must not contain a `standalone` key (duplicate of default). Unknown names refuse. Profiles must cover the exact dependency name set with sorted unique feature lists. Trial-38 checker already encodes this.

## Fit to runtime / preflight authority

Historical runtime materialization (`native-runtime-materialization-15` receipt `live-dependencies`) runs:

`check_dependencies.py --manifest <product>/Cargo.toml --target aarch64-apple-darwin --cargo …`

**no** `--feature-profile`, expected exit 0. Same pattern in `select_native_runtime03.py` and admission-runtime checks. After this remedy, those **workspace-root** invocations **must** add `--feature-profile toml-workspace` or they fail closed (that is the “host rejects default” test). That is a **command pin** change on source38/runtime isolation, not a contracts crate pin change.

Standalone generator (`build_contracts.py` / isolated `crates/contracts`) must **not** pass `toml-workspace`. Isolation-18 provider command must add the flag **after** the profile is selected; until then expected 0 is wrong.

Do not auto-select `toml-workspace` because identity is a workspace member. Explicit argv is the enforcement. A forgotten preflight path failing is the intended signal.

## Fit to compile evidence

Unchanged from the original advisory:

| Census | `serde_core` features |
| --- | --- |
| Isolation `cargo metadata` resolve | `alloc`, `result`, `std` |
| rustc fingerprint `lib-serde_core.json` | `result`, `std` |
| `cargo tree -e features` (provider / contracts / identity) | `result`, `std`; identity has **no** `serde_core` |

The checker compares **metadata** `node['features']`. Therefore `toml-workspace` must list metadata `alloc`. Source/runtime standing **must not** say the provider compiled `serde_core` with `alloc`. Identity remains a separate census (`inactiveOptionalDependencies: serde_core`). Do not put `--feature-profile toml-workspace` on `check_identity_dependencies.py` unless that tool grows the same flag; today it does not.

## Tests vs the stated set

Root’s three tests are necessary and already drafted in trial-38 `test_dependency_policy.py`:

| Stated test | Existing control |
| --- | --- |
| current host rejects default | `test_workspace_needs_explicit_profile` (`feature_profile='standalone'`) |
| standalone fixture accepts default / rejects `toml-workspace` | `test_standalone_preserves_original_profile` |
| added-feature refusals | `test_another_workspace_member_cannot_expand_features` (`serde_json` `raw_value` even under workspace profile) |

Also keep: unknown profile; profile coverage/sorted/unique; local source census. CLI default must remain `standalone` even if the **test helper** defaults to `toml-workspace` when probing the host tree.

Still required at isolation/runtime composition (not only unit tests): provider/host **argv** with the flag exits 0; without it exits 1. Do not change `check_sources` or the 11 checksums.

## Limits

Not implementation. Not approval of trial-38 checker/policy as a source unit. Not parser-38. Not a compiled-feature checker. Root implements and pins host/provider/preflight commands when composing.
