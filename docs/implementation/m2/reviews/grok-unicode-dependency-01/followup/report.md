# Independent Grok advisory: proposed pure Unicode NFC dependency

**Reviewer:** Grok (explicitly authorized). Root remains lead. Not Claude agreement.
**Kind:** Bounded proposed registry crate for pure `no_std` identity NFC. **Not runtime selection. Not M2 complete. Not live identity edit. Not graph06.**
**Work tree:** `/tmp/opensip-implementation/m2-grok-unicode-dependency-01/review`. Live product, frozen trials, architecture history, graph06 (`/tmp/opensip-implementation/m2-retained-graph-trial-06`), and commits were not edited.
**Prior:** relation payload boundary advisory archived. Root is implementing relation rules privately.

## Standing

Selected Python 3.14.6 `unicodedata.unidata_version` is independently **16.0.0**. Proposed crate is `unicode-normalization = 0.1.24` with `default-features = false` in **identity**, not contracts. Upstream **0.1.25** tables are Unicode **17.0.0** and are **not interchangeable** with the selected reference.

This is an advisory source/policy review. It is **not** a live dependency selection. Live identity still has only `sha2-const-stable =0.1.0`. Graph06 privately proposes the NFC crates; that trial is not a formal policy selection (its own README says so).

## Verdict

**NOT ACCEPTANCE.**

`unicode-normalization 0.1.24` with `default-features = false` is Unicode-16-aligned and `no_std`+`alloc` capable. Graph06’s private fetch and this review’s private lock both resolved `tinyvec 1.13.3` (`alloc` + empty `default`, **no** `tinyvec_macros`, no `std`, no `build.rs`, no `links`). Official `~/.cargo` archives match checksums `5033c97c…d956` and `fd3ca314…f0ee`. Focused composition-table parity with Python 16.0.0 holds.

It is **not live-ready**. `check_dependencies.py` is **contracts-only** and cannot gate this closure. Identity needs a **separate** pure-identity registry-closure policy (draft: `required-identity-transitive-policy.json`). The published `tinyvec = "1"` float is not a pin. Hangul `from_u32_unchecked` is present (unlike sha2-const-stable). tinyvec adds **Zlib**. Root’s 26,931 relation / 243 law cases are **root-reported** on graph06; they are not this review’s execution and do not install a dependency policy.

## Graph06 fetch (read-only; not edited)

Exact paths named by root, hashed here:

| Artifact | SHA-256 | Bytes |
| --- | --- | ---: |
| `~/.cargo/registry/cache/…/unicode-normalization-0.1.24.crate` | `5033c97c…d956` | 126536 |
| `~/.cargo/registry/cache/…/tinyvec-1.13.3.crate` | `fd3ca314…f0ee` | 60306 |
| graph06 `external-archives/` copies of both | same | same |
| graph06 `product/Cargo.lock` unicode-normalization 0.1.24 | `5033c97c…d956` | |
| graph06 `product/Cargo.lock` tinyvec 1.13.3 | `fd3ca314…f0ee` | |
| `tinyvec_macros` in that lock | **absent** | |

Extracted sources at `/Users/sb/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/{unicode-normalization-0.1.24,tinyvec-1.13.3}` byte-match this review’s earlier source pins (`Cargo.toml`, `lib.rs`, `tables.rs`, `normalize.rs`). `UNICODE_VERSION = (16, 0, 0)`. tinyvec `alloc = []`, `tinyvec_macros = []` (feature flag only). No `build.rs`.

Target-filtered `cargo metadata --locked --offline` from graph06 `product/Cargo.toml` (read-only; output in this review tree): identity’s **production registry walk** is exactly

- `sha2-const-stable 0.1.0` features `[]`
- `unicode-normalization 0.1.24` features `[]` (manifest `default-features = false`, req `=0.1.24`)
- `tinyvec 1.13.3` features `["alloc", "default"]` with `default = []`

Identity manifest in graph06: `unicode-normalization = { version = "=0.1.24", default-features = false }` plus existing sha2. **tinyvec is lock-only**, not a direct identity pin.

Root-reported graph06 results (not re-executed here; relation corpus is ~3.1 GiB uncompressed): 26,931 relation cases (26,391 Unicode strings) match the selected reference; 243 schema-law mutation cases, 126 ok / 117 invalid, `mismatches: []`. That is behavioral evidence for the private trial, **not** a live dependency-policy selection.

## Required pure identity transitive policy

Architecture (current, not replayed history):

- Chapter 14: identity may use **explicitly reviewed pure external libraries**; no OS/provider/store/report-UI dependency.
- Implementation-boundaries Enforcement 1: compare Cargo normal/build/dev/target/feature edges to the inventory graph; **inspect transitive effects/build scripts of pure-layer external libraries**.
- Tooling matrix: Cargo metadata **plus** explicit source/build rules; a dependency list alone does not prove purity; record license/dependency closures when selected.
- Shared pure packages must resolve in the **provider** workspace without inheriting host compiler/dependency settings.
- Foundation-primitives-selection-v2: target-filtered version/source/**feature** tuples must match; unused default features must be disabled (the libc lesson). Identity does not gain a new registry crate without selection.

`tools/check_dependencies.py` hard-codes `opensip-contracts` and `tools/contracts/dependency-policy.json`. That closure **selects** std, proc-macros, and build scripts (`serde_derive`, `syn`, `zmij`, serde `build.rs`) under contracts TCB decisions. Applying it to identity would either false-pass identity (wrong subject) or false-demand contracts effects in a `no_std` `forbid(unsafe_code)` crate. `check_package_edges.py` still covers **internal** edges only.

**Required before live:** a sibling identity checker + policy file (`tools/identity/dependency-policy.json` or the successor’s equivalent), **not** an extra row in the contracts policy. It must:

1. Subject `opensip-identity`; one library production target.
2. Walk identity’s production resolve (`--locked --offline --filter-platform`); exclude `dev` and `cfg(any())`.
3. Allowlist **exactly** the three registry packages above, with lock checksums equal to `.crate` SHA-256.
4. Freeze resolved features as metadata actually emits them (`unicode-normalization` `[]`; `tinyvec` `["alloc","default"]`; sha2 `[]`).
5. Refuse `links`, `custom-build` targets, proc-macro packages, `tinyvec_macros`, `std` on this walk, and any extra crate.
6. Census identity local sources (manifest + `src/**`) the way contracts schemaVersion 2 does.
7. Keep Unicode 16.0.0 / 0.1.24 as a policy field or source pin of `tables.rs`; refuse 0.1.25.
8. Still require separate source review: Hangul `unsafe`, Zlib license identifiers, NFC-only API (`is_nfc`, not NFKC/stream-safe), and the **same** tuples on the provider lock.

Identity should also pin tinyvec in the **manifest** (`=1.13.3`, `default-features = false`, `features = ["alloc"]`) or an equivalent successor lock rule. Leaving `tinyvec = "1"` inside 0.1.24 as the only constraint is how 1.13.2’s proc-macro graph can return.

Draft allowlist and checker obligations: `review/required-identity-transitive-policy.json`.

## Policy analog (current architecture)

Inventory `opensip-identity` purpose: “Pure canonical admission and content identity.” Live `crates/identity/Cargo.toml` (`10ee571d…38f3`, 279 bytes): `#![no_std]`, `unsafe_code = "forbid"`, registry dep **only** `sha2-const-stable = { version = "=0.1.0" }` (lock checksum `5f179d4e…3ed9`).

`tools/check_package_edges.py` covers **internal** package edges only. `tools/contracts/dependency-policy.json` + `check_dependencies.py` are the **contracts** lane (exact versions, checksums, resolved features, local source pins). Identity has **no** equivalent policy file.

canonical-02 accepted sha2-const-stable 0.1.0 as a pure-layer selection on **exact bytes**: no `build.rs`, no FFI, empty normal/build/target deps, no `unsafe`, lock checksum equals the `.crate` archive. Provenance metadata was not treated as evidence.

Any NFC crate in identity needs that same successor shape **before live**, not a 1.x float dropped into `Cargo.toml`.

## Official archived 0.1.24

crates.io `unicode-normalization 0.1.24` (published 2024-09-17, not yanked):

| Field | Value |
| --- | --- |
| checksum / archive SHA-256 | `5033c97c4262335cded6d6fc3e5c18ab755e1a3dc96376350f3d8e9f009ad956` |
| crate bytes | 126536 |
| license | MIT/Apache-2.0 |
| rust-version | 1.36 |
| `build` | `false` (no `build.rs` in the 24-member archive) |
| `links` | none |
| features | `default = ["std"]`, `std = []` |
| normal dep | `tinyvec = { version = "1", features = ["alloc"] }` (`default_features: true` on crates.io) |
| crate-level lint | `#![deny(missing_docs, unsafe_code)]` plus `#![cfg_attr(not(feature = "std"), no_std)]` |

`scripts/unicode.py` and `src/tables.rs` both declare `UNICODE_VERSION = 16.0.0` / `(16, 0, 0)`. Unicode 16.0.0 itself was published 2024-09-10; this crate followed seven days later.

Private Cargo 1.95 `generate-lockfile` reported `unicode-normalization v0.1.24 (available: v0.1.25)` and still locked 0.1.24 because of `=0.1.24`.

## 0.1.25 is not the same Unicode

Official archived **0.1.25** (2025-10-30), checksum `5fd4f6878c9cb28d874b009da9e8d183b5abc80117c40bbd187a1fde336be6e8` / 128462 bytes: `UNICODE_VERSION = (17, 0, 0)`. Selected Python is 16.0.0. **Do not substitute 0.1.25** for 0.1.24. A later Python unidata bump would be a new selection, not a patch of this one.

## Resolved tinyvec (today’s private lock)

`unicode-normalization 0.1.24` does not pin tinyvec. This review’s private lock resolved:

| Field | Value |
| --- | --- |
| version | **1.13.3** (published 2026-09-13) |
| checksum | `fd3ca314f692efd6c868f8408f53fe444634a845f96c028b97d35f6a1f79f0ee` |
| crate bytes | 60306 |
| license | **Zlib OR Apache-2.0 OR MIT** |
| `build` | `false` |
| crate lint | `#![forbid(unsafe_code)]` |
| resolved features | `alloc`, `default` (`default = []` in 1.13.3) |
| resolved deps | **none** |
| `tinyvec_macros` | **not in the graph** |

`cargo tree -e all --target all --locked`: probe → unicode-normalization 0.1.24 → tinyvec feature `alloc` + feature `default` → tinyvec 1.13.3 only.

**Why the float is a selection hole.** At 0.1.24’s publish date the newest tinyvec was 1.8.0. Through **1.13.2**, `alloc = ["tinyvec_macros"]` pulled a **proc-macro** crate (`tinyvec_macros 0.1.1`, checksum `1f3ccbac…2f20`). 1.13.3 changelog: the macros crate is no longer a dependency; an empty `tinyvec_macros = []` feature remains to avoid edge-case breakage. A lock generated against 1.13.2 is a different TCB than 1.13.3. Formal identity selection must pin **exact** tinyvec version + checksum + resolved features, the way sha2-const-stable is `=0.1.0` plus lock checksum — not `tinyvec = "1"`.

tinyvec’s optional `std`, `serde`, `borsh`, `schemars`, `experimental_write_impl` are **off**. `std::io::Write` exists in `tinyvec.rs` behind `#[cfg(feature = "std")]` and is not compiled in this graph.

## Unsafe / build / native / IO

| Surface | 0.1.24 unicode-normalization | tinyvec 1.13.3 (resolved) |
| --- | --- | --- |
| `build.rs` | absent (`build = false`) | absent (`build = false`) |
| `links` / FFI / `extern "C"` | none in `src/` | none in `src/` |
| host IO / net / process | none in `src/` (bench `std::fs` is a bench target, not a dependent lib) | `std::io::Write` cfg-gated on `std` (**off**) |
| proc-macro | no | no at 1.13.3 `alloc`; would appear on 1.13.2 |
| `std` feature | **off** (`features = []`) | **off** |
| alloc | `extern crate alloc`; `TinyVec<[char; 4]>` / `TinyVec<[(u8,char); 4]>` buffers | `alloc` enables `TinyVec` heap spill via `alloc::vec::Vec` |
| unsafe | **yes**, Hangul only (below) | **no** (`forbid(unsafe_code)`; comments mentioning unsafe are not `unsafe` blocks) |

Hangul in `normalize.rs`: `#[allow(unsafe_code)]` around `char::from_u32_unchecked` after `is_hangul_syllable` / Jamo range checks (UAX #15 §3.12 arithmetic). Not OS, not FFI, not IO. Identity’s `unsafe_code = "forbid"` applies to **identity’s own** sources, not to this dependency.

canonical-02’s accepted hash crate had **zero** `unsafe`. A live NFC successor must **record and accept** this Hangul `from_u32_unchecked` (or reject the crate). Silence is not an analog of sha2-const-stable.

No native library, no build-script env/process/file effects in the production graph.

## License implications

| Crate | SPDX / crates.io license | Notices in archive |
| --- | --- | --- |
| unicode-normalization 0.1.24 | MIT/Apache-2.0 | `LICENSE-MIT`, `LICENSE-APACHE` |
| tinyvec 1.13.3 | Zlib OR Apache-2.0 OR MIT | `LICENSE-ZLIB.md`, `LICENSE-MIT.md`, `LICENSE-APACHE.md` |
| sha2-const-stable 0.1.0 (current identity) | MIT/Apache-2.0 family | already selected |

tinyvec introduces **Zlib** into the identity TCB. Apache-2.0 is a common choice among the disjunctions, but the distributed crate carries all three notices. Formal selection must list license identifiers the way the contracts/hash selections do. This review does not invent a license forbid; it records the new family.

Generator `scripts/unicode.py` is not compiled into the library. Tables are checked-in Rust (`tables.rs` 624118 bytes, `69a0faad…7348`).

## Unicode 16 NFC verification (independent)

Python 3.14.6 `-I -B`: `unicodedata.unidata_version == "16.0.0"`.

Crate `UNICODE_VERSION == (16, 0, 0)`. Private no_std lib + std print harness, `default-features = false`, rustc 1.95: printed `UNICODE_VERSION=16.0.0`.

Composition-table parity with Python 16.0.0 (not a full UAX#15 corpus):

- **928 / 928** BMP `COMPOSITION_TABLE_KV` pairs
- **33 / 33** `composition_table_astral` pairs, including Unicode 16 new scripts:

| Script (Unicode 16.0.0 new) | Examples in crate tables |
| --- | --- |
| Todhri | `U+105D2`+`U+0307`→`U+105C9`; `U+105DA`+`U+0307`→`U+105E4` |
| Tulu-Tigalari | `U+113C2`+`U+113C2`→`U+113C5` and the other 1138x/113Cx rows |
| Gurung Khema | `U+1611E` / `U+16121` / `U+16122` / `U+16129` cluster (8 pairs) |
| Kirat Rai | `U+16D67`+`U+16D67`→`U+16D68`; `U+16D63`+`U+16D67`→`U+16D69`; `U+16D69`+`U+16D67`→`U+16D6A` |

Behavioral probe **31 / 31** match Python, including classic NFC (`e`+acute, `Å`→Å, `Ω`→Ω, Hangul `U+1100`+`U+1161`→가, combining-class reorder `a`+`U+0316`+`U+0301`→`á`+`U+0316`), already-NFC pass, empty, ASCII.

NFKC is a **different** form: Python `ﬁ` stays `ﬁ` under NFC and becomes `fi` under NFKC. Identity law is NFC only.

Selected identity-model predicate (live 9/14, `identity_model.py` `619d6e3c…41e6`):

```python
if type(node) is str and unicodedata.normalize('NFC', node) != node:
    raise C.AdmissionError('RELATION_PAYLOAD_NOT_NFC')
```

That is “already NFC”, not “recompose and keep”. Rust should use `unicode_normalization::is_nfc(s)` (authoritative; quick-check `Maybe` falls back to `s.chars().eq(s.chars().nfc())`), **not** NFKC, **not** stream-safe.

## Missing formal dependency selection before live

Required, analog to software-hash-01 + canonical-02 + contracts `dependency-policy.json`:

1. An identity-lane successor (not a silent `Cargo.toml` edit) naming **exact** `unicode-normalization =0.1.24` checksum `5033c97c…d956`.
2. **Exact** `tinyvec =0.1` is wrong; exact **1.13.3** checksum `fd3ca314…f0ee` (or another version that is itself source-reviewed). Do not leave the upstream `"1"` float as the product pin.
3. Resolved features frozen: unicode-normalization **no features** (`default-features = false`); tinyvec **`alloc` only** (empty `default`). Refuse `std`, `tinyvec_macros` as a dep, serde/borsh/schemars.
4. Source-review file hashes for both crates (this tree’s `pins/source-pins.json` is evidence, not the successor).
5. Explicit Hangul `unsafe` acceptance (or a different crate).
6. License identifiers including tinyvec Zlib-or-Apache-or-MIT.
7. `--locked --offline` identity metadata/tree showing only sha2-const-stable + these two packages; no `build.rs`, no `links`.
8. Tests below, against **this** Python 16.0.0, not a later unidata.

Contracts policy must not be reused as if it covered identity.

## Tests needed for parity with the selected reference

Before live, identity tests should prove the **same predicate** as Python 3.14.6 unidata 16.0.0: `is_nfc(s) == (unicodedata.normalize('NFC', s) == s)`.

| Test | Why |
| --- | --- |
| Official Unicode 16.0.0 `NormalizationTest.txt` NFC columns | Full UAX#15 corpus; not run in this advisory |
| `is_nfc` vs `s.nfc().eq(s.chars())` vs Python `normalize==original` | Quick-check `Maybe` path |
| Unicode 16 compositions listed above | New scripts; 33/33 table pairs already match here |
| Hangul LV / LVT / jamo | Exercises the only `unsafe` |
| Combining-class reorder (`a`+below+acute) | CCC, not just composition map |
| Singletons `Å`/`Ω` | Compatibility characters that **are** NFC-composed |
| Already-NFC pass, NFD refuse | Identity refuses `!=`, does not rewrite |
| Empty, ASCII, BMP + supplementary | Scan of relation payload strings |
| `ﬁ` NFC-stable, NFKC=`fi` | Guard against calling `nfkc` |
| Stream-safe APIs unused | Python NFC is not stream-safe |
| 4 MiB bound (`MAX_BYTES`) | Alloc/`TinyVec` heap spill, no host IO |
| `cargo tree` / metadata: no `tinyvec_macros`, no `std`, no `build.rs` | Feature/graph regression |
| Identity still `no_std` + `forbid(unsafe_code)` at **its** crate | Lint does not audit the Hangul `unsafe` in the dep |

This advisory’s 31 harness cases plus 961 composition-map pairs are **not** a substitute for `NormalizationTest.txt`.

## Reproduction (private; root fetches separately)

```
export CARGO_HOME=/tmp/opensip-implementation/m2-grok-unicode-dependency-01/review/cargo-home
export CARGO_TARGET_DIR=/tmp/opensip-implementation/m2-grok-unicode-dependency-01/review/probe-workspace/target
export PATH=/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin
cd /tmp/opensip-implementation/m2-grok-unicode-dependency-01/review/probe-workspace
cargo build --locked --offline
./target/debug/unicode-nfc-probe
```

Pins: `review/pins/source-pins.json`, crate archives under `review/pins/`, lock SHA-256 `bd30e1aa…f851`.

## Coordination

Did not edit live `crates/identity/Cargo.toml`, live/frozen history, or graph06. Relation-payload boundary remains archived. Root implements relation rules and prepares graph06 independently.

## Correction (appended; original text above is unchanged)

Inspected official archived **tinyvec_macros 0.1.1** (crates.io checksum `1f3ccbac311fea05f86f61904b462b55fb3df8837a366dfc601a0161d0532f20`, 5865 bytes). `Cargo.toml` has **no** `[lib] proc-macro = true`. `src/lib.rs` is `#![no_std]`, `#![forbid(unsafe_code)]`, and a `#[macro_export] macro_rules! impl_mirrored` declarative macro. It is an ordinary library crate, **not** a procedural-macro crate.

The earlier statements in this report that 1.13.2 `alloc` “pulled a proc-macro” are **wrong as to crate kind**. The graph fact that remains: 1.13.2 `alloc` still **depends on the extra package** `tinyvec_macros 0.1.1`; 1.13.3 `alloc = []` does not. Identity policy should still refuse that extra unselected crate.

tinyvec 1.13.3 metadata still emits resolved features **`["alloc", "default"]`** with `default = []`. Formal pin is closed identity policy plus `--locked` build recording those exact features. **Do not** require a source patch of unicode-normalization 0.1.24’s upstream `tinyvec = "1"` float.

Root accepted the remaining dependency-review obligations (Hangul `unsafe` recorded, full source pins) before live. This correction does not reopen Unicode 16 / 0.1.24 / 0.1.25 interchange, and it does not change the NOT ACCEPTANCE standing of the original advisory.
