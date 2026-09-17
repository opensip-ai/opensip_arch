# Advisory: identity inactive-optional dependency exception

**Reviewer:** Grok. Root remains lead. Not Claude agreement.  
**Kind:** Bounded security/correctness advisory of the private identity checker’s `inactiveOptionalDependencies` exception. **Not parser acceptance. Not SOURCE38. Not runtime. Not live install. Not frozen-unit selection.**  
**Work tree:** `/tmp/opensip-implementation/m2-grok-identity-optional-edges-38` only. Trial product `/tmp/opensip-implementation/m2-package-parser-trial-38/product` was read-only. No live/frozen/history edits.

Inventory26 is selected 24/34; no parser code installed. Layout DAG vs live Cargo is root’s disposition (live identity has no internal deps; live evaluator depends only on identity). Not reopened. toml.rs policy pin in the copied inputs lags the current trial `src/toml.rs` (6102/`901ee4fb…` vs 6333/`03202a1e…`); this note does not accept that source.

## Verdict

**The exception is not a blanket optional-ignore. It is fail-closed for the hide paths this probe could construct (enabled features, non-optional/build/target/dev-only/duplicate/absent/hyphen, cross-workspace serde unification). It is required because `cargo metadata` puts a `serde_core` resolve edge on `toml_datetime` / `serde_spanned` from the weak `serde_core?/alloc` feature, while `cargo tree -p opensip-identity` does not compile that crate.**

Hardening remains: an omitted name is checked against `package.dependencies`, not against `node.deps`. Policy may list an unused optional that is not even on the resolve node (`toml`’s `serde_core`, `winnow`’s `memchr`). That did not hide an active identity edge in this graph.

## Pins (copied inputs)

| Artifact | Bytes | sha256 |
| --- | ---: | --- |
| Prompt | 1927 | `2fad07e603719c1234a7e3948aa52a9a689c62e6b9d3c28f31be363290a448d1` |
| `inputs.json` | 778 | `f1e4e6c88f2bd5e0cb826616da56b1b59bc01494169e67ee9ac7ff8164b2c4f4` |
| `tools/check_identity_dependencies.py` | 9628 | `d1dedd6c907f1f404aaf021741fd6227dc368272c9ec615957547d8189d244a7` |
| `tools/tests/test_identity_dependencies.py` | 6283 | `e10a58b8379d5b01db367e586a3a654878a5475af20222df71550083d23b1144` |
| `tools/identity/dependency-policy.json` | 55526 | `09cf25f663a9324854d0d6d1083b0ee01517285f866e9b9f4174fe788acc10d8` |
| `crates/identity/Cargo.toml` | 750 | `876739b9d5a7be6a8aee5eb3379e6f543425d67594acf40a411af1146c73dff9` |
| `Cargo.lock` | 6111 | `36889e3d10e48464c0729c54031b15351320462ac164a0fa226af07ac57c5621` |

Copied checker/tests/Cargo.toml/lock **byte-equal** the current trial product. Copied policy differs **only** in `localSources` `src/toml.rs` (trial policy `55526` / `91ca011253f1832662a9a68642e80d11dd29e461da042f0f7b930c1f96fd5f74`). Tests were reproduced on an isolated product copy that keeps the trial policy+toml.rs pair so census can pass. Checker bytes are the pinned ones.

Tool: Homebrew cargo/rustc 1.95.0, target `aarch64-apple-darwin`, archives `/Users/sb/.cargo/registry/cache/index.crates.io-1949cf8c6b5b557f`, python `/tmp/opensip-implementation/metadata-reference-env/bin/python`.

Policy `inactiveOptionalDependencies`: **only** `serde_spanned` and `toml_datetime`, each `["serde_core"]`. Not on `toml`, `toml_parser`, `winnow`, identity root.

## Mechanism (source)

`inactive_optional_edges` (checker 76–115):

1. Names must be a sorted unique `list[str]`. Empty → no exception (not a blanket skip of all optionals).
2. Expand **actual** `node['features']` through `package['features']`: `dep:foo` and strong `foo/bar` mark `foo` active; weak `foo?/bar` does **not**.
3. Each named exception must be **exactly one** `package.dependencies` row with `(rename or name) == name`, `optional is True`, `kind is None`, `target is None` (unconditional optional **normal** dep; not build/dev/cfg).
4. Name must **not** be in the active set.
5. Omit set is `name.replace('-', '_')`, compared to resolve `edge['name']` (rustc extern name).

Walk (166–168) skips omitted names and already skips `kind==dev` and `target==cfg(any())`. For each **visited** package, resolved-feature pin, registry checksum, crate archive, and source census run **before** omit. Omitted packages are never censused (intended).

## Evidence

### Metadata vs compiled tree

`cargo tree -p opensip-identity -e features --offline --locked`: eight crates, `serde_spanned`/`toml_datetime` feature `alloc` only, **no `serde_core`**. `cargo tree -i serde_core -p opensip-identity`: nothing to print.

`cargo metadata` resolve, same platform:

- `toml_datetime` features `['alloc']`, **node.deps includes `serde_core`** `kind=None target=None`. Feature `alloc = ["serde_core?/alloc"]`.
- `serde_spanned` same.
- `toml` features `['parse']`: optional `serde_core` is in **package.dependencies** but **not** in `node.deps` (`parse` does not weakly mention it).
- Identity root features `[]`; no serde_core edge.

Workspace `target/debug/deps` **does** contain `libserde_core` because contracts/reporting/cli compile `serde`. `toml_datetime`/`serde_spanned` `.d` files list only `lib.rs`+`datetime.rs` / `lib.rs`+`spanned.rs` (not `de.rs`/`ser.rs`). Identity `.d` has no `serde_core`. Workspace rlib presence is not identity-closure membership.

### Checker + five tests (isolated copy)

`check(...)` → `passed`, `dependencyCount` **8**, registry tuples exclude `serde_core`, `sourceFilesVerified` 299, `productQualification` false.

| Test | Result |
| --- | --- |
| selected closure excludes only inactive optional edges | ok |
| no implicit optional exception (pop all exceptions) | ok (refuse) |
| another workspace member enabling `toml` `serde` | ok (`resolved features differ`) |
| added identity `src/unselected.rs` | ok (`source census differs`) |
| only disabled optional decls can be omitted (dep:/strong `/` / alias; optional/build/target; dup/absent) | ok |

Without exceptions, a full `check` on this metadata refuses **`build/proc-macro target not selected`** because visiting `serde_core` sees `custom-build` `build.rs` — fail-closed, not a silent extra crate. The unit test does not pin that message.

### Independent hide / alias probes

| Probe | Outcome |
| --- | --- |
| Rename field `core`, policy still `serde_core` | refuse (declaration) |
| Policy `core` (rename) | omit set `{core}`; resolve edge name remains `serde_core` → walk would still visit (fail-closed, does **not** hide) |
| `target=cfg(unix)` / `kind=build` / `optional=False` | refuse |
| duplicate / unsorted / absent / `serde-core` hyphen | refuse |
| `serde_core/alloc` or `dep:serde_core` or alias→`serde` on node.features | refuse `is enabled` |
| `serde_core?/alloc` extra weak feature | still omits (correct: weak does not enable) |
| `toml` listed `serde_core` though not in `node.deps` | **allowed** (declaration-only) |
| `winnow` listed `memchr` though `node.deps` empty | **allowed** (declaration-only) |

Cross-workspace feature unification is pinned by `resolvedFeatures` **before** omit. Enabling `toml` `serde` from reporting cannot sneak `serde_core` past a `parse`-only pin.

## Fail-closedness / ordering

Visited package: no `links`; no custom-build/proc-macro; identity features `== rootFeatures`; else name/version in policy, crates.io source, lock checksum, archive sha256, **source census**, production targets ⊆ census; **then** omit; then follow remaining non-dev, non-`cfg(any())` edges; finally `found == expected`.

Cannot skip `toml_datetime` census by omitting `serde_core`. Cannot omit a required/build/cfg/dev-only edge. Cannot omit an edge whose resolved features enable it via `dep:` / strong `/` / alias. Rename mismatch does not drop the rustc edge name. Dev edges are skipped independently (`kind==dev`) and cannot be named as this exception.

Residual: the checker does not read `cargo tree` or rlib `--extern` lines. It trusts Cargo’s feature metadata. A Cargo bug that compiled a weak-only optional would not be caught here; it was **not** observed (`tree -i serde_core` empty; datetime/spanned `.d` without serde modules).

## Actionable findings

1. **Require the omitted name to appear on that package’s `node.deps` (and still pass the declaration + not-enabled checks).** Today a policy row may list any matching optional *declaration*, including ones cargo did not put on the resolve node (`toml`/`serde_core`, `winnow`/`memchr`). Tightening binds the exception to the actual metadata quirk (weak feature ⇒ resolve edge) and stops pre-authorizing unused optionals. Does not change the two legitimate `serde_core` edges.

2. **Pin the no-exception refuse class in the unit test** (`unselected` vs `build/proc-macro` vs `is enabled`) so a future graph cannot swap which fail-closed path is being exercised without notice.

Neither is a demonstrated hide of an **active** identity dependency on this graph.

## Limits

Not SOURCE38/parser/runtime/live install. Not a memory-safety or sandbox proof (`productQualification`/`memorySafetyProof` already false). Not a census of workspace-wide serde (host/report compile serde_core; identity tree does not). Not MIRI/geiger. toml.rs pin lag is recorded, not accepted. Root leads.
