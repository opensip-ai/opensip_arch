# Frozen trial review: package-parser-38

**Reviewer:** Grok. Root remains lead. Not Claude agreement.  
**Kind:** Scoped source review of identity TOML 1.0 parse-only graph, opaque borrowed document, evaluator package projection, and identity/contracts dependency guards. **Not runtime selection, not full enumeration, native providers, Run, replay, or custody.** Concurrent bounded feature advisory (other Grok) is **not** this approval.  
**Work tree:** `/tmp/opensip-implementation/m2-grok-package-parser-source-38-review/review`. Frozen/export/live/history not edited. No commits. Source is frozen: follow-up would need a new version.

## Subject pin

**subjectManifestSha256** `d7f581ebf2d756a79365c4630ab08a7c797e97465646f0c4c32044e449b2ee46`

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/implementation/m2/trials/package-parser-38/subject.json` | 101519 | `d7f581ebf2d756a79365c4630ab08a7c797e97465646f0c4c32044e449b2ee46` |
| `archive-pin.json` → `subject.tar.xz` | 3346236 | `c5176b18de00685db23a4cf867532949a882bb8994d72ec0f32c103820a4089f` |
| export | `/tmp/opensip-implementation/m2-package-parser-subject-38` | **529/529** members, sorted unique, 0 mismatches |

## Base / owned delta

Product lock equals selected live **24 inventory / 35 contract** (`72063` / `ecae54f79143183b65204f0a821827ebe3e0824307bb6aadaddb9eda9d3b8e2c`). Last inventory candidate **v26** (`147952` / `1a861b0cd3bc6dcbb952e2b136299bd7e3a4492f2eb488039e90e89ac740a324`). Last contract: enumeration-integer-profile reference **v1** (E39). `source-delta.json`: **241** unchanged + **13** changed + **3** new = **257** non-lock product files; `design-lock.json` is the 258th product path in the subject. Owned **16**. New planned paths: `crates/identity/src/toml.rs`, `crates/host/tests/fixtures/package-fixtures.json`, `tools/tests/test_identity_dependencies.py`.

Evaluator `Cargo.toml` still depends only on `opensip-identity`. Identity remains `#![no_std] #![forbid(unsafe_code)]`.

## Algorithm / ownership / errors / resources

**Identity `parse_toml`** (`toml.rs` **6333** / `03202a1e52a7aa87420cfe325ea49c0bc327a8094597acc61127ec4c6582e339`):

1. `len > MAX_BYTES` (4 MiB, same JSON constant) → `ByteLimit`.
2. `from_utf8` fail → `InvalidUtf8`.
3. Leading U+FEFF → `Syntax` (tomllib; crate would accept). Embedded BOM in a string remains data.
4. `DeTable::parse` only (no `parse_recoverable`). Messages `recursion limit` / `cannot recurse further; max recursion depth met` → `RecursionLimit`; else `Syntax`.
5. Iterative walk, node budget 1_000_000 → `NodeLimit`. Empty `DeInteger` literal (`0x`/`0o`/`0b`) → `Syntax`. `year == 0` or `second > 59` anywhere → `Syntax`. Integers/floats stay literals (no `to_i64`/`to_f64`).

`TomlDocument` / `TomlTableView` / `TomlValueView` are opaque wrappers. Public surface is `table`/`get`/`contains_key`/`as_table`/`as_str` only. Upstream TOML types are not identity’s API. Host must keep input bytes alive. Comment records 2 MiB development stack; the helper cannot inspect it.

**Evaluator `project_enumeration_packages`** (`enumeration.rs` **26586** / `81bbcfbe8670173c4e517702060ce65f4242726fa629f11802df28ffc34706fc`):

- File-extent first, then filename `package.json` / `Cargo.toml` only.
- Missing blob or optional snapshot hash/length mismatch → `ENUMERATION_ADMISSION_PRECONDITION` (not syntax). Hash is `raw_sha256` hex vs index `sha256`/`bytes`.
- JSON: `parse_json`; profile violations (including JSON byte/depth) → `parseFailed` `syntax`. Name rules on object `name`.
- TOML: `InvalidUtf8`/`Syntax` → `parseFailed` `syntax`; `ByteLimit`/`RecursionLimit`/`NodeLimit` → **`EnumerationExtentError::Limit` abort, no partial named/unnamed/failed lists**.
- Classification: no `package` → unnamed (`workspace-only` if root has `workspace`, else `no-name`); non-table `package` or empty/non-string `name` → `classification`.
- `steps` copied independently for extent vs package visits. Public result is data + refusals; no subject/Run.

**Guards.** Identity checker now requires omitted names to be one unconditional optional **normal declaration** and **exactly one** `node.deps` edge with `dep_kinds == [{kind: None, target: None}]`, plus feature-walk (`dep:` / strong `/` enable; `?/` does not). Before-hardening checker **9628** / `d1dedd6c…44a7`; frozen **9935** / `62fc4dd17c4bf70b355807a15f00945178d1fd6cb90425d85ff39e6ee94d43b9`. Tests pin no-exception reason `build/proc-macro target not selected` and refuse absent/duplicate/renamed/build/target resolve edges plus `toml`/`winnow` declaration-without-edge. Both prior optional-edge findings are corrected. Not blanket optional ignore.

Contracts checker: explicit `--feature-profile`; default `standalone`; additional map cannot reuse that name; selected profile must cover the exact dependency set with sorted unique features; **no union/auto-fallback**. `toml-workspace` vs `standalone` differs only by adding `alloc` to `serde_core` (`result,std` → `alloc,result,std`). Original provider guard without the flag: `unselected resolved features: serde_core ['alloc', 'result', 'std']`. Resumed isolation uses `--feature-profile toml-workspace`.

Exact parse-only pins: toml `=0.9.9` `parse`; toml_parser `=1.0.5` `alloc`; toml_datetime `=0.7.4` `alloc`; serde_spanned `=1.0.4` `alloc`; winnow `=0.7.13` no features; defaults off. Policy `rootFeatures` `[]`. Identity closure 8 registry tuples, 299 sources. Winnow compiled-unsafe TCB is stated in `TOML-PROFILE.md` (not a memory-safety proof; `-F unsafe_code` is not transitive). Policy JSON `unsafeAccounting` remains the Hangul account.

`profile-package-result.json` still says `proposedReferenceSha256` / unselected wording. **Current** portable result uses `selectedReferenceSha256`.

## Reproduction

Pinned CPython **3.12.13** `-I -B -X int_max_str_digits=0`, unicode 15.0.0, isolated writable copy of checker/harness/product crates/full 157-member reference (E39 overlay `d32883fdfb7a40395169dfb078c1590844a7f6e85e2c15cc2315ab8990626992`). Independent `check-packages.py` → **1940** cases, **1933** reference comparisons, **7** local Limits, **0** mismatches; output **byte-equal** frozen `portable-reproduction/result.json`.

Independently (readonly product, `CARGO_TARGET_DIR` in this work tree, rustc 1.95.0 `--locked --offline`): identity **43** tests including four `toml::tests::*`; host `retained_package_projection_matches_selected_reference_and_local_limits` (1939 durable fixture cases, **2692951** / `1e22b9c9…89f1` under 4 MiB); host `toml_parser_and_drop_fit_selected_development_worker_stack` (explicit 2 MiB worker: depth 80/81, mixed 80 tables+80 arrays, 4 MiB unclosed `[`). Frozen workspace stdout sums to **130** passed. Frozen identity/contracts test stderr: **5** and **9** OK. Isolation receipts: host **138** sources / **23** archives; provider **26** sources / **19** archives.

Adversarial checks in source: leading vs embedded BOM; unused nested year-0 / leap-second; empty radix; resource vs syntax; missing/hash-join precondition vs Limit abort; cross-workspace toml `serde` unification refuses; unused optional decls without resolve edges refuse.

## requiredFindings

None.

## Limits (not required findings)

- Does not implement complete enumeration, native compiler integration, Run, replay, or custody.
- Does not accept runtime installation; formal runtime selection is separate.
- Concurrent winnow/feature advisory is not this review’s approval.
- Does not prove stack safety off the selected 2 MiB development worker, or transitive memory safety of winnow.
- JSON `package.json` profile refusals remain `syntax`; TOML resource exhaustion is typed `Limit`.
- Policy JSON Hangul `unsafeAccounting` is not a winnow census; `TOML-PROFILE.md` is.
- Live 24/35 is this trial’s selected product lock, not a private 9/15 inheritance.

## Verdict

No required findings. Frozen parse/projection/guards match the selected E39 oracle on 1933 comparisons, keep TOML resource errors distinct from syntax, keep the public document opaque, and record exact parse-only pins plus the corrected optional-edge and contracts feature-profile controls.
