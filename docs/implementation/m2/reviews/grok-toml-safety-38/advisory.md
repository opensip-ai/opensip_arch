# Advisory: TOML parser dependency unsafe + DeTable resource safety

**Reviewer:** Grok. Root remains lead. Not Claude agreement.  
**Kind:** Bounded dependency/resource-safety advisory on the exact crates.io graph already named by feasibility-36. **Not ACCEPT-DESIGN-UNIT. Not source acceptance. Not runtime acceptance. Not full M2. Not a live install. Not probe qualification. Not a selected-law change.**  
**Work tree:** `/tmp/opensip-implementation/m2-grok-toml-safety-38` only. Did not edit the root probe, product, architecture frozen files, or live locks. No network install.

Root continues implementation. This note answers two questions: (1) which winnow/`toml_parser` `unsafe` is compiled vs reachable under the parse-only feature set; (2) whether a ≤4 MiB document can stack-overflow `DeTable::parse` / Drop despite crate recursion 80. Package semantic projection is root’s concurrent work and is not reopened here.

Selected UTF-8 totality is now `enumeration_model.v1.py` **49833** / `689620ec7c1e2ecc417a8ccdbc379cd94c8ca985118a44b727126f15a3af9072` (newE). Full enumeration remains unimplemented.

## Verdict

**Compiled winnow `unsafe` is TCB; it is not a reachable `DeTable::parse` callsite under this feature set. Crate LIMIT 80 bounds tree depth, not stack use on a tiny thread. Preparse 4 MiB + ordinary process stack + iterative postparse walk is the resource boundary.**

`RUSTFLAGS=-F unsafe_code` is not transitive absence proof: Cargo passes `--cap-lints allow` to registry deps, and a rebuild with that flag still compiled winnow 0.7.13.

## Pins

| Artifact | Bytes | sha256 |
| --- | ---: | --- |
| This prompt | 1679 | `d3b3c56532b1174585603821671d126259d5ff93cf0393b6a761541404ff843c` |
| Feasibility-36 `advisory.md` | 20839 | `36e35d8dda90632715e712bd54294f55be9539afaa624388aaf2b56637ca18b9` |
| Root probe `Cargo.toml` (unedited) | 550 | `4099d2c77621ff080964f7f74dce8fb4b549e46142db4dcf6c80be29119911b9` |
| Root probe `Cargo.lock` (unedited) | 2838 | `c369680ab5d53058cd43aa3a822713c09e182894fa27f1bfbcc1b19d59bbd1cc` |
| Root probe `src/lib.rs` (unedited) | 1927 | `4e36696af4cc44ddafcd8efa2d68cd3fc3d51d507f896be83c5a81fa143a9d7f` |
| Safety-38 probe `Cargo.toml` | 550 | `0b2c85dfb8ca610a01acff0e73d4f08ef146ca1f9eef0254ef0a26da59949f0a` |
| Safety-38 probe `Cargo.lock` | 2836 | `b903bbee5393b49df2082ffe04d31f13fefec91776bb90fde16b75905f3a44e3` |
| Safety-38 probe `src/main.rs` | 5763 | `83fa88081037108fcbe41c324e07ea25a2ffb9296befb8ca72d97e13bdce3294` |
| Selected `enumeration_model.v1.py` | 49833 | `689620ec7c1e2ecc417a8ccdbc379cd94c8ca985118a44b727126f15a3af9072` |

Exact crates.io checksums (root probe lock; safety-38 lock is the same five checksums):

| Crate | Metadata version | checksum |
| --- | --- | --- |
| `toml` | `0.9.9+spec-1.0.0` | `eb5238e643fc34a1d5d7e753e1532a91912d74b63b92b3ea51fde8d1b7bc79dd` |
| `toml_parser` | `1.0.5+spec-1.0.0` | `4c03bee5ce3696f31250db0bbaff18bc43301ce0e8db2ed1f07cbb2acf89984c` |
| `toml_datetime` | `0.7.4+spec-1.0.0` | `fe3cea6b2aa3b910092f6abd4053ea464fab5f9c170ba5e9a6aead16ec4af2b6` |
| `serde_spanned` | `1.0.4` | `f8bbf91e5a4d6315eee45e704372590b30e260ee83af6639d64557f51b067776` |
| `winnow` | `0.7.13` | `21a0236b59786fed61e2a80582dd500fe61f18b5dca67a4a067d0bc9039339cf` |

Inspected sources: `~/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/{toml-0.9.9+spec-1.0.0,toml_parser-1.0.5+spec-1.0.0,toml_datetime-0.7.4+spec-1.0.0,serde_spanned-1.0.4,winnow-0.7.13}`.

Tool: Homebrew `rustc 1.95.0 (59807616e 2026-04-14)`, `/opt/homebrew/Cellar/rust/1.95.0/bin/cargo --offline --locked`. Host stack soft limit 8176 KiB.

Compiled feature tree (`cargo tree -e features` on the safety-38 probe): `toml` `parse`; `toml_parser` `alloc`; `toml_datetime` `alloc`; `serde_spanned` `alloc`; `winnow` no features. Release `deps/*.rlib`: those five only. No `libserde_core`. Features **off**: `toml_parser/unsafe`, `toml_parser/simd`, `winnow/simd`, `winnow/std`, `unbounded`, `serde`, `preserve_order`.

## 1. Unsafe accounting (generic methods vs reachable callsites)

### Forbid crates

`toml` 0.9.9, `toml_datetime` 0.7.4, `serde_spanned` 1.0.4: `#![forbid(unsafe_code)]`. No executable `unsafe` in `src/`.

`toml_parser` 1.0.5: `#![cfg_attr(not(feature = "unsafe"), forbid(unsafe_code))]`. Every `next_slice_unchecked` / `get_unchecked` body is `#[cfg(feature = "unsafe")]` with a `next_slice` / `get` else-branch. Feature `unsafe` is off, so **no compiled `unsafe` in `toml_parser`**. Lexer stream type is `winnow::stream::LocatingSlice<&str>` (`lexer/mod.rs`).

### winnow 0.7.13 (`default-features = false`, no features)

Distinguish three layers:

1. **Trait default methods** (`stream/mod.rs` `Stream::next_slice_unchecked` / `peek_slice_unchecked`): documented “inherent impl to allow callers to have `unsafe`-free code”. Bodies call **safe** `next_slice` / `peek_slice`. These are generic `unsafe fn` signatures, not executed unsafety unless an impl overrides them.

2. **Concrete overrides with real `unsafe` blocks** (compiled even with no features):
   - `&str` and `&[T]`: `get_unchecked` in `next_slice_unchecked` / `peek_slice_unchecked`.
   - `Bytes` / `BStr`: `mem::transmute` in constructors plus `get_unchecked` on the unchecked slice methods.
   - Wrappers `LocatingSlice`, `TokenSlice`, `Stateful`, `Partial`: forward to inner `next_slice_unchecked` **if invoked**.
   - `Recoverable`: `cfg(feature = "unstable-recover", feature = "std")` — **not compiled**.

3. **Combinator `unsafe` not on the Stream trait:** `ascii::dec_uint` / `ascii::dec_int` use `from_utf8_unchecked` after parsing ASCII digits. Module `ascii` is always compiled. `toml_parser` does **not** call `winnow::ascii::*`; it has its own `ensure_dec_uint`. Combinator / `parser.rs` contain **zero** `next_slice_unchecked` callsites.

**Reachable from `DeTable::parse` under this feature set:** lexer and decoder call `next_slice` (safe) because `toml_parser/unsafe` is off. Event reconstruction uses `TokenSlice` `next_token`, not unchecked. No `Bytes`/`BStr` constructor on this path. No `dec_uint`/`dec_int`. **No executed winnow `unsafe` block identified on the parse path.** Compiled winnow `unsafe` remains in the rlib and is the unicode-normalization-class TCB item feasibility-36 deferred.

### Cargo lint cap (empirical)

Safety-38 package has `[lints.rust] unsafe_code = "forbid"` (local crate only). Rebuild:

`RUSTFLAGS='-F unsafe_code' cargo build --offline --locked -v`

Exit 0. Registry rustc lines end with `--cap-lints allow -F unsafe_code`. Local bin has `--forbid=unsafe_code` and `-F unsafe_code` and **no** `--cap-lints`. winnow still compiled. **`RUSTFLAGS=-F unsafe_code` is not a census of transitive `unsafe`.** Successor must keep a source-level account (this section) or an equivalent compiled-feature + source census. Do not treat a green forbid-unsafe build as memory-safety of winnow.

## 2. DeTable parse / Drop resource safety

### What LIMIT 80 actually counts

`toml` `src/de/parser/mod.rs`: `const LIMIT: u32 = 80` (absent feature `unbounded`). `RecursionGuard` wraps the event receiver.

- **Increments:** `array_open` and `inline_table_open` only (`toml_parser` `parser/event.rs`). Error text `cannot recurse further; max recursion depth met`. Depth starts at 0; 80 nested arrays/inline tables are allowed (`depth <= 80`); 81st is refused. On refuse, `on_array_open` / `on_inline_table_open` call **iterative** `ignore_to_value_close` (nested `[]`/`{}` counts, no further recursive parse).
- **Does not increment:** `std_table_open`, `array_table_open`.
- **Separate cap:** dotted-key path in `toml` `de/parser/key.rs`: `LIMIT <= result_path.len()` → `recursion limit`. `result_path` is every key **except the last**, so 80 keys succeed and 81 fail. **Standard and array table headers go through `on_key`**, so a chain `[k0]\n[k0.k1]\n…\n[k0.…kN]` is bounded by the **last header’s dotted path**, not by RecursionGuard.

`descend_path` is a loop. `document()` is a token/event loop. `on_array` / `on_inline_table` **do recurse** on nested value events (up to the 80 recorded opens). `DeValue` has no custom `Drop`; nested `Table`/`Array` Drop is ordinary recursive enum drop. `DeTable::parse` always builds a tree then returns `Err` on the first sink error, so error paths still Drop a (depth-capped) tree.

### Independent subprocess probes

Safety-38 binary, timeouts 30–120 s, debug then release. Representative results:

| Case | Debug main | Release 64 KiB thread | Release 128 KiB+ / main (~8 MiB) |
| --- | --- | --- | --- |
| nested array 80 | ok | **stack overflow** | ok |
| nested array 81 | `cannot recurse further…` | — | same Limit |
| nested inline 80 | ok (main); **overflow at 512 KiB debug thread** | **stack overflow** | ok |
| nested inline 81 | Limit | — | Limit |
| dotted key 80 / 81 | ok / `recursion limit` | — | same |
| std-table chain 80 / 81 | ok / `recursion limit` | 80 ok at 64 KiB release | same |
| array-table chain 80 / 81 | ok / `recursion limit` | — | same |
| unclosed arrays 80 | `unclosed array, expected ]` | — | same |
| unclosed arrays 200 / 10000 | Limit (iterative skip) | — | same |
| 4 MiB `'['` after `x = ` | Limit, 262 ms debug / 34 ms release | **overflow** | Limit, no overflow |
| 4 MiB sibling `[tN]` (307528 tables) | ok + Drop, ~1.1 s debug / 144 ms release | **ok at 64 KiB release** | ok |
| mixed 80 tables + 80 arrays | ok | **overflow** | ok |
| duplicate table / unclosed `{` / trailing junk | `duplicate key` / `unclosed inline table` / `missing table open` | — | same |
| empty | ok keys=0 | — | same |

**Answer:** a ≤4 MiB TOML **can** stack-overflow **despite LIMIT 80** if parse runs on a **too-small thread stack**. It did so on a 64 KiB **release** thread for 80 nested arrays, 80 nested inline tables, mixed 80+80, and 4 MiB unclosed brackets (the last still walks 80 recursive `on_array_open` frames before the iterative skip). It did **not** overflow the host main thread (~8 MiB) or release threads ≥128 KiB for any case in this set, including 4 MiB sibling tables (wide BTree, log-height Drop). Debug frames are much larger (80 nested inline tables overflowed a 512 KiB debug thread).

LIMIT 80 is a **tree-depth / recursion-guard** bound, not a stack-budget proof. 4 MiB is a **byte** envelope, not a stack envelope.

No partial-TOML claim: these are full-document `DeTable::parse` outcomes, then Drop.

## Recommended identity boundary (not selected law)

Apply around a full `DeTable::parse`. Do not substitute a Cargo-subset lexer.

1. **Preparse (before the crate):** `raw.len() > 4 * 1024 * 1024` → **Limit**. `str::from_utf8` fail → **InvalidUtf8** (candidate syntax; selected 689620 already maps `UnicodeDecodeError`). Do not call `DeTable::parse` on oversized or non-UTF-8 bytes.
2. **Parse:** `DeTable::parse` only. Map exact messages `recursion limit` and `cannot recurse further; max recursion depth met` → **Limit**. Any other error → **Syntax**. No `parse_recoverable`. No `unbounded`. No serde `Table`/`Value`.
3. **Stack:** run parse+Drop on the ordinary process/thread stack (this host 8 MiB). Do **not** parse on worker threads with stack &lt; 1 MiB. Release 128 KiB survived this probe; 1 MiB is the conservative identity floor so debug and mixed nesting stay inside the envelope.
4. **Postparse (after Ok):** iterative walk with a node budget → **Limit** if exceeded; `year == 0` or `second > 59` → **Syntax**. Do not recurse on `DeValue` for the walk. Classify on the same stack; drop the borrowed tree with the input bytes.

That is a resource/profile boundary around a full 1.0 document parse. It is not a claim that a truncated prefix is a valid Cargo.toml.

## Actionable findings

1. **Record winnow compiled `unsafe` in the identity dependency-policy successor** the same way unicode-normalization Hangul `unsafe` was recorded. Do not claim “no unsafe” from package `forbid` or from `RUSTFLAGS=-F unsafe_code`. Keep `toml_parser/unsafe` and `simd` off so parse-path callsites stay on `next_slice`.
2. **Install the preparse 4 MiB Limit before `DeTable::parse`**, keep crate 80 mapped to Limit, walk iteratively after Ok, and do not parse TOML on sub-1 MiB stacks. LIMIT 80 plus a 4 MiB byte cap does not by itself prove stack safety.

## Explicit limits

This advisory does not: accept a design unit; freeze source; install a live dependency; claim full M2 / runtime / replay; claim tomllib parity; claim TOML spec equals tomllib; change selected law; qualify the root or safety-38 probe as product code; claim exhaustive stack testing across platforms, LTO, or panic=abort variants; claim a geiger/MIRI proof; census optional lockfile `serde_core` as compiled (it is not); allow caret versions or spec-1.1 crates; allow `unbounded` / `serde` / `preserve_order` / `simd` / `toml_parser/unsafe`; claim partial-document Cargo semantics.

Root leads. Next product step remains the identity dependency-policy successor with this graph, this unsafe account, and the preparse/postparse boundary above.
