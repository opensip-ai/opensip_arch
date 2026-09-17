# Advisory: TOML parser feasibility (identity parse-only route)

**Reviewer:** Grok. Root remains lead. Not Claude agreement.  
**Kind:** Bounded feasibility of a parse-only `no_std` / no-serde route through `toml::de::DeTable` / `DeValue`, before any product dependency proposal. **Not ACCEPT-DESIGN-UNIT. Not source acceptance. Not runtime acceptance. Not full M2. Not a live install. Not qualification of the private probe as a product parser.**  
**Work tree:** `/tmp/opensip-implementation/m2-grok-toml-parser-feasibility-36/review` only. No live/frozen/history/product/lock edits. No network install of a product dependency.

Root already read advisory35 plus the JSON-parse addendum: exact-profile JSON admits pretty / unsorted bytes; `syntax` is profile refusal, not `raw != C.canonical`. Selected `project_named_packages` still parses `Cargo.toml` with **full** CPython `tomllib.load` (TOML **1.0.0**). Evaluator stays identity-only. This note does not reopen those ownership claims as selected law.

Root private probe `/tmp/opensip-implementation/m2-toml-parser-probe-36` supplied crates.io metadata, checksum-verified `toml` 0.9.8 / 0.9.9 crates, and a standalone `no_std` classifier. Root follow-up (`probe-followup.md`) asked for a precise validation / resource / totality boundary after the first 349-case differences and the later 946-case corrected run. This advisory inspects those artifacts; it does **not** edit the probe.

## Verdict

**Implementable identity profile exists. Not a product change.**

A parse-only graph through `toml::de::DeTable::parse` can live on identity, keep evaluator classification on a borrowed TOML view, and avoid coercing floats / datetimes into `JsonValue`. It is **not** tomllib-identical by crate defaults. Identity must add a small tomllib-profile layer (UTF-8, calendar year/leap-second, resource Limit vs Syntax) and exact-pin five crates at the last TOML **1.0.0-spec** line. Caret versions, the current crates.io default (`toml` 1.1.6+spec-1.1.0), and the entire `toml` **1.0.x** line (also spec-1.1.0) are incompatible with the selected oracle.

Do not install this graph until an identity dependency-policy successor (unicode-normalization class) records compiled features, checksums, source census, and winnow unsafe accounting. Until that successor, Cargo.toml projection stays fail-closed as advisory35 already required.

## Pins (this assessment)

| Artifact | Bytes | sha256 |
| --- | ---: | --- |
| Prompt | 1835 | `45ad2aaa71ec9d0a07b4306b6b89e45d33a2507d53568f9b34f3585c68b5a3cf` |
| Root follow-up | 1219 | `2430c609b23db127e944cb90ea4e419511fdfa60087d55712db3ce450933aafc` |
| `check_toml_probe36.py` | 4255 | `048000bab0ee7836675845609e318c36013063ed8a90fa51ec293c61b7496959` |
| Probe `Cargo.toml` (current) | 550 | `4099d2c77621ff080964f7f74dce8fb4b549e46142db4dcf6c80be29119911b9` |
| Probe `Cargo.lock` | 2838 | `c369680ab5d53058cd43aa3a822713c09e182894fa27f1bfbcc1b19d59bbd1cc` |
| Current probe `src/lib.rs` | 1927 | `4e36696af4cc44ddafcd8efa2d68cd3fc3d51d507f896be83c5a81fa143a9d7f` |
| Initial probe `src/lib.rs` | 934 | `86d624ccfe7c8b04f9789fe8dd3bfeed28277054da9d74dfd0de6fe913d5edcb` |
| Current `cases.json` (946) | 143638 | `e86e8d8d45691ea6eae88db16840cabae0fd699a909243662a89dd824ba7b724` |
| Current `result.json` | 28753 | `3fb5f4baaa426e86714ec648efdb5e7466a816a438531d0ce111b72d5e0eac5a` |
| Initial `result.json` (349) | 29121 | `cec6cfec01d906dc81476ef27732eef3ee1cda42914244e8c6fcbc1b8c85cd1f` |
| `toml-0.9.9+spec-1.0.0.crate` | 56573 | `eb5238e643fc34a1d5d7e753e1532a91912d74b63b92b3ea51fde8d1b7bc79dd` |
| `toml-0.9.8.crate` (probe archive) | 56104 | `f0dc8b1fb61449e27716ec0e1bdf0f6b8f3e8f6b05391e8497b8b6d7804ea6d8` |
| Live identity `Cargo.toml` | 354 | `d275f9399ab6ba83ef2f4c23d6177ec28c0bdfc8b6092350bab06eee91622a3e` |
| Live evaluator `Cargo.toml` | 261 | `cef1245cbfec7e96892ea2cc7ffdead83d82cf3bc425c1ea98bd106d730b2f56` |
| Selected `enumeration_model.v1.py` (advisory35) | 49811 | `69b0eee39a45a941d7ab1ef22c0c8be161edd436b1441b27017f98fd1bcffe85` |

Reference oracle named by the probe: **CPython 3.12.13 `tomllib`**. Identity production deps remain sha2-const-stable `=0.1.0` and unicode-normalization `=0.1.24` `default-features=false`. Evaluator still depends only on identity.

## 1. Minimal compiled graph (parse-only, `no_std`, no serde)

**Not** `toml` with only `default-features = false`. `toml` always depends on `toml_datetime` and `serde_spanned` even without the `serde` feature. `Table` / `Value` / `from_str` are serde-gated. `DeTable` / `DeValue` / `DeInteger` / `DeFloat` / `DeString` / `DeArray` are public under feature `parse`.

Root probe already compiled this graph with `RUSTFLAGS=-F unsafe_code` and `#![no_std]` + `forbid(unsafe_code)` on the probe library:

```toml
toml = { version = "=0.9.9", default-features = false, features = ["parse"] }
toml_parser = { version = "=1.0.5", default-features = false, features = ["alloc"] }
toml_datetime = { version = "=0.7.4", default-features = false, features = ["alloc"] }
serde_spanned = { version = "=1.0.4", default-features = false, features = ["alloc"] }
winnow = { version = "=0.7.13", default-features = false }
```

Exact crates.io checksums (also the probe lockfile):

| Crate | Version metadata | checksum |
| --- | --- | --- |
| `toml` | `0.9.9+spec-1.0.0` | `eb5238e643fc34a1d5d7e753e1532a91912d74b63b92b3ea51fde8d1b7bc79dd` |
| `toml_parser` | `1.0.5+spec-1.0.0` | `4c03bee5ce3696f31250db0bbaff18bc43301ce0e8db2ed1f07cbb2acf89984c` |
| `toml_datetime` | `0.7.4+spec-1.0.0` | `fe3cea6b2aa3b910092f6abd4053ea464fab5f9c170ba5e9a6aead16ec4af2b6` |
| `serde_spanned` | `1.0.4` | `f8bbf91e5a4d6315eee45e704372590b30e260ee83af6639d64557f51b067776` |
| `winnow` | `0.7.13` | `21a0236b59786fed61e2a80582dd500fe61f18b5dca67a4a067d0bc9039339cf` |

**Enable:** `toml/parse`, `toml_parser/alloc`, `toml_datetime/alloc`, `serde_spanned/alloc`.  
**Do not enable:** `std`, `serde`, `display`, `preserve_order`, `fast_hash`, `debug`, `unbounded`, `toml_parser/unsafe`, `toml_parser/simd`, `winnow/simd`, `winnow/std`, `winnow/default`, `winnow/debug`. `preserve_order` requires `std` + indexmap; identity stays on `BTreeMap` lexicographic keys. That is enough for `"package"` / `"workspace"` / `"name"` classification.

`cargo tree -e features` on the private probe (rustc 1.95.0) compiled **only**:

- `toml` `0.9.9+spec-1.0.0` feature `parse`
- `toml_parser` `1.0.5+spec-1.0.0` feature `alloc`
- `toml_datetime` `0.7.4+spec-1.0.0` feature `alloc`
- `serde_spanned` `1.0.4` feature `alloc`
- `winnow` `0.7.13` (no features)

No `libserde_core*.rlib` in `probe/target/debug/deps`. `serde_core` / `serde_derive` / `syn` / `quote` / `proc-macro2` appear in `Cargo.lock` because `serde_spanned` and `toml_datetime` declare **optional** `serde_core`. Feature `alloc` uses `serde_core?/alloc` (enabled only if serde is on). **Census the compiled feature tree, not the lockfile package list.** A later accidental `serde` feature would pull that graph; the successor must forbid it.

## 2. Semver drift to TOML 1.1 — exact pins required

crates.io as of this probe metadata:

- Current default `toml` is `1.1.6+spec-1.1.0`.
- **Last TOML 1.0.0-spec `toml` is `0.9.9+spec-1.0.0`.** Next is `0.9.10+spec-1.1.0`.
- **Every `toml` 1.0.x line is `+spec-1.1.0`.** Do not read “toml 1.0” as TOML spec 1.0.
- Last 1.0-spec `toml_parser` is `1.0.5+spec-1.0.0`. Next `1.0.6+spec-1.1.0` is caret-compatible with `1.0.5`.
- Last 1.0-spec `toml_datetime` is `0.7.4+spec-1.0.0`. Next `0.7.5+spec-1.1.0` is caret-compatible with `0.7.4`.
- `winnow` `0.7.14` / `0.7.15` exist; caret on `0.7.13` would move.

`toml` 0.9.9’s own `Cargo.toml` uses **caret** `toml_parser = "1.0.5"`, `toml_datetime = "0.7.4"`, `winnow = "0.7.13"`. Depending on `toml = "0.9.9"` without `=` and without exact transitive pins **will** resolve spec-1.1 parser/datetime crates. Identity must `=` pin all five and lock checksums. Later 1.1 lines must not be selected while CPython tomllib remains the 1.0 oracle.

Private probe already refused TOML 1.1 syntax that tomllib refuses: newline in inline table (`syntax-0`), trailing comma in inline table (`syntax-1`), `\e` (`syntax-2`). Array trailing commas remain lawful TOML 1.0 (`syntax-8`). Optional datetime seconds (`1979-05-27T07:32Z`, `07:32`) are syntax on both.

## 3. Public API route

- `toml::de::DeTable::parse(&'i str) -> Result<Spanned<DeTable<'i>>, Error>` is the document parser. Public under `parse`.
- `DeValue` is `String` / `Integer` / `Float` / `Boolean` / `Datetime` / `Array` / `Table`. Integers and floats are **literal** `Cow<'i, str>` plus radix, not `i64`/`f64`.
- `Table` / `Value` / `from_str` / `Deserializer` require `serde`. Identity must not take that route and must not deserialize into product structs.
- `DeTable::parse_recoverable` can emit a dummy empty `Datetime` after reporting an error. **Do not use recoverable parse.** Fail closed on the first `Error`.
- `make_owned()` exists but **does not** convert `DeInteger` / `DeFloat` Cows (only strings, arrays, tables). Do not treat it as a complete owned tree. Classification can keep the borrowed view and drop it with the input bytes.

## 4. Syntax versus lazy numeric / eager datetime

| Kind | When validated | tomllib (CPython 3.12.13) | Consequence for classification |
| --- | --- | --- | --- |
| Structure, keys, duplicates, escapes, 1.0 inline-table rules | Eager in `toml_parser` + `DeTable::parse` | Eager `TOMLDecodeError` | Match on the 946-case corpus except depth/UTF-8/calendar noted below |
| Integer | **Lazy.** Stored as `DeInteger { inner, radix }`. `to_i64`/`to_u64`/`to_i128` only if later conversion | Python `int` unbounded | Huge ints (`2^63`, `2^64`, 80-digit decimal, wide hex) stayed **named** on both because classification does not convert |
| Float | **Lazy.** `DeFloat` literal. `to_f64` rejects overflow-to-inf unless the source contains `inf` | Python `float` (1e9999 → inf) | `inf`/`nan`/`1e9999` stayed **named** on both. Do not call `to_f64` in identity parse |
| Datetime | **Eager.** `decoded.parse::<toml_datetime::Datetime>()` during scalar decode | CPython `datetime` via tomllib | Calendar month/day/leap-year, hour 0–23, minute 0–59, offset 24:00 already match. **Year 0000 and second 60 do not** (see §7) |

Do not smash this tree into identity `JsonValue` (no float, integer range `-(2^63)..=2^64-1`). A lawful Cargo.toml may contain floats and datetimes beside a string `package.name`. Parse must succeed on the whole document; classification only reads key presence and `package.name` as a non-empty string.

## 5. Resource bounds

Crate default (feature `unbounded` off):

- `LIMIT: u32 = 80` in `toml` 0.9.9 `src/de/parser/mod.rs`.
- `toml_parser::parser::RecursionGuard` increments on **array** and **inline table** open; error text `cannot recurse further; max recursion depth met`.
- Dotted-key path length uses the same 80 with error text `recursion limit`.
- Standard `[table]` headers do **not** increment that guard.

Private current probe maps those two messages to **`Limit`**, not `Syntax`. That is the right identity split: resource refusal is not a TOML grammar claim. Do **not** enable `unbounded` (stack overflow on Drop/Debug of deep trees; crate docs say so). Do **not** raise 80 to chase tomllib. Real Cargo.toml is shallow. Depth 64 nested arrays parsed; 127/128/129/256 hit the crate limit.

Identity-side bounds (not in the crate; current probe already does the first two):

| Bound | Proposal | Relation to existing identity JSON |
| --- | --- | --- |
| Input bytes | Refuse `raw.len() > 4 * 1024 * 1024` as **Limit** | Same `canonical::MAX_BYTES` |
| Recursion | Crate 80 → **Limit** | JSON `MAX_DEPTH` is 32 and is profile syntax; do **not** copy 32 onto TOML |
| Calendar walk nodes | Bound the post-parse walk (probe used 1_000_000) as **Limit** | Needed only if identity walks every value for year/leap-second |
| `unbounded` | Forbidden | — |

Membership: Limit and Syntax both fail named-package projection, so both enter candidate extent as parse failure. Keep the diagnostic distinct. Mapping Limit to Syntax (initial probe) over-claimed grammar.

## 6. Unsafe and host I/O

| Crate | Unsafe | Host I/O in parse |
| --- | --- | --- |
| `toml` 0.9.9 | `#![forbid(unsafe_code)]` | `DeTable::parse` takes `&str`. No `std::fs` / `std::net` in `src/` |
| `toml_datetime` 0.7.4 | `#![forbid(unsafe_code)]` | None |
| `serde_spanned` 1.0.4 | `#![forbid(unsafe_code)]` | None |
| `toml_parser` 1.0.5 | `forbid(unsafe_code)` unless feature `unsafe` | None. Feature `unsafe` is opt-in slice shortcuts; **must stay off** |
| `winnow` 0.7.13 | Contains `unsafe` inherent `next_slice_unchecked` / `from_utf8_unchecked` | None at this feature set. `simd` would pull `memchr`; keep off |

Identity crate stays `#![no_std] #![forbid(unsafe_code)]`. That lint does not prove the transitive graph. unicode-normalization was admitted with an explicit Hangul `unsafe` account. **winnow is the new TCB item** of the same class: successor must census compiled `unsafe` and accept or reject it. This advisory does not perform that geiger-level census and does not claim memory-safety.

No host I/O in the parse path. Host still only supplies retained bytes. Do not parse from paths.

## 7. Borrowed view vs evaluator classification

Yes: a borrowed parsed-TOML view on identity can keep evaluator classification separate and avoid JSON coercion.

Recommended split (choice for the successor, not selected law):

1. **Identity** `parse_toml(raw: &[u8]) -> Result<TomlView<'_>, TomlError>` wrapping `Spanned<DeTable>` (do not re-export `toml` types as identity’s stable API). Errors: `ByteLimit`, `RecursionLimit`, `InvalidUtf8`, `Syntax`. After a successful `DeTable::parse`, walk values and refuse `date.year == 0` or `time.second > 59` as **Syntax** (tomllib profile, not crate default). Do not convert integers/floats. Do not emit `JsonValue`.
2. **Evaluator** `project_named_packages` consumes that view: `"package"` / `"workspace"` key presence; `package` must be a table; `name` absent → unnamed / workspace-only; `name` non-empty `str` → named; otherwise classification. Same key-presence law as selected Python (`check_toml_probe36.py` / advisory35 table).
3. **Host** supplies bytes only.

The view borrows the UTF-8 input. Classify on the same stack and drop the tree. If a later owner needs an owned tree, identity must copy integer/float literals itself (`make_owned` is incomplete).

Do not put the toml crate on evaluator. Do not accept a caller-claimed table.

## 8. Actual mismatches vs CPython 3.12.13 tomllib

**Spec compliance is not tomllib classification.** `toml_datetime` follows TOML 1.0 ABNF (year four digits including 0000; seconds 00–60 for leap seconds). CPython `datetime` used by tomllib does not.

### Initial probe (349 cases, no calendar walk, recursion mapped to syntax)

Defined mismatches (non-UTF-8): **6**.

| Label | tomllib | DeTable default | Notes |
| --- | --- | --- | --- |
| `date-0000-01-01` | syntax | named | Year 0 lawful in toml_datetime; `datetime.date` min year 1 |
| `date-23:59:60` | syntax | named | Second 60 lawful leap second; `datetime.time` max second 59 |
| `depth-127/128/129/256` | named | syntax (then) | Crate LIMIT 80; initial probe folded Limit into Syntax |

Nested shapes `[{value=DATE}]`, `{value=[DATE]}`, `[[DATE]]` for year 0000 / 23:59:60 are the same datetime policy (must walk, not only root scalars).

### Current probe (946 cases, calendar walk + Limit class)

Defined mismatches: **0**. Remaining rows:

| Class | Count | expected → actual | Recommendation |
| --- | --- | --- | --- |
| Recursion resource | 4 | `named:706b67` → `limit` | Keep **Limit**. Document tomllib-deeper-than-80 as identity resource bound, not grammar |
| Invalid UTF-8 bytes 128–255 | 128 | `reference-exception:UnicodeDecodeError` → `syntax` | Identity: `from_utf8` fail → `InvalidUtf8`, mapped to syntax for candidate extent (JSON already has `InvalidUtf8`). **Selected Python catches only `TOMLDecodeError`.** That is a reference-totality successor, not a crate bug |

Huge ints/floats/inf/nan: no mismatch; literals retained.

Calendar month/day/leap-year (588 `calendar-*` dates across years 0000, 0001, 1900, 2000, 2023, 2024, 9999): crate already matches tomllib once year 0000 is refused by the identity walk. Feb 29 2024 named; Feb 29 2023 / Feb 30 / Apr 31 / day 00 / month 13 syntax on both.

**Do not treat the current probe as qualification.** It is a private difference list. Year-0000 and leap-second agreement depends on the identity walk remaining in the product parser. Recursion Limit remains a documented divergence.

## 9. Required conformance corpus (successor, not this probe)

Minimum, same bytes, CPython 3.12.13 `tomllib.load` vs identity `parse_toml` + evaluator classification:

- All current 946 labels (basic classification, scalars, dates, 1.0-vs-1.1 syntax, depths 1/31/32/64/127+, calendar grid, nested datetime, every byte 0–255 in a string).
- Mixed-type arrays (TOML 1.0 allows; not in this corpus).
- UTF-8 BOM, CR-LF, comments, dotted `package.name` (already `basic-7`), `[package]` + `[workspace]`, `[[package]]` array-of-tables (`basic-18` classification).
- Duplicate keys / duplicate tables (already `basic-15/16`).
- Bare non-ASCII key vs quoted (`syntax-13/14`).
- Floats and datetimes **not** in `package.name` (already scalar/date rows).
- Explicit Limit cases: nested arrays 80 and 81; dotted-key path length 80; input `MAX_BYTES+1`.
- Year 0000 and `23:59:60` at root, in arrays, in inline tables, in nested tables.
- Invalid UTF-8 as `InvalidUtf8` / syntax, with the Python reference catching `UnicodeDecodeError` the same way.

Drift against that corpus is a product defect, not a fixture preference. Passing BurntSushi toml-test or “TOML 1.0 spec” is **not** sufficient.

## 10. Implementable profile (primary source pins)

For a later identity dependency-policy successor **only** (root implements; this is not an install):

```toml
# opensip-identity, additional to existing exact pins
toml = { version = "=0.9.9", default-features = false, features = ["parse"] }
toml_parser = { version = "=1.0.5", default-features = false, features = ["alloc"] }
toml_datetime = { version = "=0.7.4", default-features = false, features = ["alloc"] }
serde_spanned = { version = "=1.0.4", default-features = false, features = ["alloc"] }
winnow = { version = "=0.7.13", default-features = false }
```

Identity parse profile (tomllib 1.0, not raw crate):

1. `len > MAX_BYTES` → Limit.
2. `str::from_utf8` fail → InvalidUtf8 (candidate syntax).
3. `DeTable::parse`; messages `recursion limit` / `cannot recurse further; max recursion depth met` → Limit; any other error → Syntax.
4. Walk tables/arrays (bounded); `year == 0` or `second > 59` → Syntax.
5. Return borrowed view. No `to_i64` / `to_f64`. No `parse_recoverable`. No serde `Table`/`Value`.

Evaluator classification unchanged from selected Python key-presence law.

Licenses: toml / toml_parser / toml_datetime / serde_spanned **MIT OR Apache-2.0**; winnow **MIT**. rust-version of these crates is 1.76 / 1.65; identity is 1.95.

## 11. Explicit unqualified limits

This advisory does **not**:

- accept a design unit, freeze source, install a live dependency, or claim full M2 / runtime / replay;
- claim Claude agreement or root assent;
- claim tomllib parity (depth ≥ 80 remains Limit; UTF-8 totality is a selected-Python gap until the reference catches `UnicodeDecodeError`);
- claim TOML spec compliance equals tomllib classification;
- approve winnow `unsafe` (successor census required, unicode-normalization class);
- treat `Cargo.lock` optional `serde_core` as compiled, or treat lockfile listing as the census;
- allow caret `toml 0.9` / `toml 1` / `toml_parser 1.0` / `toml_datetime 0.7` / `winnow 0.7`;
- allow `toml` 1.0.x or 1.1.x (spec-1.1.0);
- allow `unbounded`, `preserve_order`, `serde`, `std`, `simd`, `toml_parser/unsafe`;
- allow host-claimed tables, partial Cargo subset lexers, or JSON coercion;
- treat the private probe or its `Limit` / calendar walk as product code;
- replace fail-closed Cargo.toml projection before the identity successor.

JSON path stays identity `parse` / `C.parse` (pretty/unsorted admitted). TOML path is full-document 1.0 with the pins and profile above.

## What root still owns

Root leads. Root may keep the private comparison probe and develop corrections separately. Next product step remains: identity dependency-policy successor with this exact graph + compiled-feature census + winnow unsafe account + tomllib corpus, then evaluator classification over the borrowed view. Until then, package cells that see a scoped `Cargo.toml` stay fail-closed.
