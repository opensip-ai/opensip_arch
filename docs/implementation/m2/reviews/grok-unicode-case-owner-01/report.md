# Advisory: TypeScript `lib_name_fold` and Unicode-16 FULL lowercase in Rust

**Reviewer:** Grok. Root remains lead. Not Claude agreement.
**Kind:** Bounded case-conversion owner note for native-context `lib` join. **Not selection. Not acceptance. Not a live identity dependency.**
**Work tree:** `/tmp/opensip-implementation/m2-grok-unicode-case-owner-01/review`. Live, frozen, private07, and private08 were not edited.

Native-boundary02 is archived. This note does not reopen Plan capability join. Root’s CAPABILITY_BYTES_JOIN-before-ADMIT ordering is in the selected identity source (`identity_model.py` ~1657–1662); that precheck is identity-structural and stays out of this fold.

## Authority (selected native e678)

`docs/implementation/m2/capability-totality-reference-selection-v1/reference/native_evidence_model.py` `e6784aa1…e2b9`:

```
UNICODE_CASE_DATA_VERSION = "15.0.0"
lib_name_fold(name):
    if unicodedata.unidata_version != UNICODE_CASE_DATA_VERSION:
        raise ReferenceEnvironmentError(...)   # not AdmissionError
    return name.lower()
```

Published operation (docstring, native-evidence §2.4): Unicode Default Case Conversion **`toLowercase(X)`**, FULL, non-tailored, context-sensitive.

| Required | Forbidden |
| --- | --- |
| Full mapping (`SpecialCasing.txt` + UnicodeData field 13) | Simple_Lowercase_Mapping alone (U+0130 → U+0069 only) |
| Final_Sigma (string context) | Per-code-point `char::to_lowercase` as the string op |
| Root locale (no `tr`/`az`/`lt` rows) | Locale tailoring (Turkish `I`→`ı`) |
| Identity for unassigned | Case_Folding (`ß`→`ss`) |
| | NFC/NFKC before or after |

Current compiler `lib` vocabulary is ASCII, where full/simple/fold coincide. That is **not** a field restriction. The fold must still be the published full operation.

**Custody is a gate, not a comment.** Selected Python 3.14.6 `unicodedata.unidata_version` is **16.0.0**, so `lib_name_fold` **refuses today** with `ReferenceEnvironmentError` on the NFC-selected interpreter. That is the designed environment fault, not a lib-selection refusal.

A Rust implementation that used Unicode **16** tables would **not** satisfy the published `UNICODE_CASE_DATA_VERSION = "15.0.0"` unless a later successor rebinds that constant. Rebinding 15→16 is a separate native-reference selection (and would align the fold with Python 3.14.6 / NFC 16). This advisory does not rebind it.

## Rust 1.95 is Unicode 17 — do not call std

Homebrew `rustc 1.95.0 (59807616e 2026-04-14)`:

`library/core/src/unicode/unicode_data.rs` `pub const UNICODE_VERSION: (u8, u8, u8) = (17, 0, 0);`  
SHA-256 `a752707d…6460` / 118749 bytes.

Private probe (`review/probe/std_lower.rs`): `str::to_lowercase` is context-sensitive (Final_Sigma); `char::to_lowercase` is **not** (`"ΑΣ"` → `ασ` via char-map, `ας` via `str`). On the discriminating scalars below, Unicode 17 `str::to_lowercase` happened to match Python 16. That does **not** license using std: the bound version is 15.0.0 (selected) or 16.0.0 (only after rebind), never 17.

## Feasibility of a deterministic FULL default lowercase (Unicode 16 tables)

**Yes**, as a small owned algorithm plus **closed generated tables**, without std and without a new live crate.

Default `toLowercase` (Unicode Standard §3.13; UCD `SpecialCasing.txt`):

1. Walk the original string by scalar value (not NFC, not grapheme).
2. For each `C`:
   - If `C` is U+03A3 and **Final_Sigma** holds on the **original** context → U+03C2.
   - Else if an **unconditional** full lowercase mapping exists (SpecialCasing with empty condition list, else UnicodeData field 13) → that 1–3 scalar sequence.
   - Else → `C` (unassigned and uncased stay themselves).
3. Skip every SpecialCasing row whose condition list contains a language id (`tr`, `az`, `lt`) or `After_Soft_Dotted` / `More_Above` / `After_I` / `Not_Before_Dot`. Those are tailored. Default lowercase uses **only** Final_Sigma among context conditions.

**Final_Sigma** (same file; DerivedCoreProperties):

- Before: `\p{Cased} \p{Case_Ignorable}*`
- After: not `\p{Case_Ignorable}* \p{Cased}`
- Context is the original string, not the already-lowercased prefix.

**U+0130:** unconditional `0130; 0069 0307; …` → `i` + combining dot. Simple mapping (field 13) is the single `i` — that is the explicit anti-example in `lib_name_fold`. Turkic row `0130; 0069; …; tr` must **not** win.

**Supplementary / unassigned:** same tables; no BMP-only shortcut. Unassigned in the bound UCD → identity.

**Do not:** `str.casefold()`, `unicode_normalization`, locale `to_lowercase`, NFC “to make casing easier” (SpecialCasing’s NFC remark is about **uppercase** of iota-subscript, not this fold).

Official sources (pin, do not vendor UnicodeData in this review):

| File | Role | This review |
| --- | --- | --- |
| `https://www.unicode.org/Public/16.0.0/ucd/SpecialCasing.txt` | Full lc + Final_Sigma; ignore language rows | 16809 bytes, SHA `8d5de354…0c451` |
| `https://www.unicode.org/Public/15.0.0/ucd/SpecialCasing.txt` | Same SpecialCasing **data rows** as 16 (119/119 equal) | 16832 bytes, SHA `78b29c64…f494` |
| `UnicodeData.txt` field 13 at the **bound** version | Simple_Lowercase_Mapping | not downloaded (large); required for a generator |
| `DerivedCoreProperties.txt` `Cased` / `Case_Ignorable` | Final_Sigma | same |
| Unicode Standard §3.13 Default Case Algorithms | Procedure | — |

SpecialCasing 15 vs 16 bodies are identical. 15↔16 lowercase **divergence is new cased assignments** in UnicodeData (the custody paragraph in `lib_name_fold`), not SpecialCasing edits.

## Generated closed table vs pure dependency

**Recommend generated closed tables owned by the native/evaluator slice, bound to the selected `UNICODE_CASE_DATA_VERSION`, after a generator pin — not a live std or crate fold.**

Reasons:

- rustc 1.95 std is Unicode **17**.
- `unicode-case-mapping 1.0.0` (crates.io 2024-10-08, checksum `4e902650…a9db`, Apache-2.0) advertises Unicode **16** **per-char** maps (`to_lowercase('İ')` etc.). It does **not** implement Final_Sigma or expose Cased/Case_Ignorable. Insufficient as `lib_name_fold`. Identity-lane selection would still be required (same bar as NFC). Not selected here.
- ICU4X `icu_casemap` pulls a CLDR/ICU Unicode train, not “exactly 15.0.0” or “exactly 16.0.0” without its own selection.
- Table size is small (rustc’s own `to_lower` is ~12 KiB plus Cased/Case_Ignorable bitsets).

Generator (offline, not a `build.rs` in identity): read the three UCD files at the **declared** version; emit a sparse lc map (only non-identity images) plus two property bitsets; record UCD file SHA-256s in the successor. Runtime is `no_std`+`alloc`, no `unsafe` required.

If UNICODE_CASE_DATA_VERSION stays **15.0.0**, generate from Public/15.0.0. If a later unit rebinds to **16.0.0** to match Python 3.14.6/NFC, generate from Public/16.0.0. Do not mix.

## Discriminating cases (small; not a UCD sweep)

| Input | FULL default lowercase | Distinguishes |
| --- | --- | --- |
| `ES2022`, `dom` | `es2022`, `dom` | ASCII lib vocabulary |
| `İ` U+0130 | `i`+U+0307 | Full vs simple |
| `ß` U+00DF | `ß` | vs `casefold` → `ss` |
| `I` | `i` | vs Turkish `ı` |
| `ΑΣ` | `ας` (final sigma) | Final_Sigma |
| `ΣΑ` | `σα` | non-final |
| `ΟΣ.` | `ος.` | Case_Ignorable after |
| lone `Σ` | `σ` | no preceding Cased |
| unassigned BMP / supplementary with no lc | identity | version-custody class |
| `I`+U+0307 (two scalars) | `i`+U+0307 | not NFC-composed to U+0130 first |

Do not treat TypeScript `lib` ASCII-only fixtures as proof of the fold.

## Integration check strategy

1. **Environment gate:** Rust must refuse (operational, not `adm-*`) if its tables’ recorded UCD version ≠ `UNICODE_CASE_DATA_VERSION`. Mirror `ReferenceEnvironmentError`. Never fold with “whatever rustc has.”
2. **Oracle:** generate expected strings from the **same** pinned UCD as the tables (not from Python 3.14.6 `str.lower()`, which is Unicode 16 while the selected constant is 15). If the constant is rebound to 16, then Python 3.14.6 `str.lower()` becomes a valid cross-check **after** the version gate passes.
3. **Unit tests:** the table above, plus `char` vs string Final_Sigma, plus one language-tailoring negative (`I` must not become `ı`).
4. **Native-context join:** `libSelection` vs `honoredOptions.lib` set equality after fold; `lib.{fold(n)}.d.ts` ∈ declared components (`admit_native_context` ~2361–2389). One TS context fixture with mixed-case `DOM`/`dom` is enough for that join; keep U+0130/sigma in the fold unit tests, not necessarily in a compiler lib name.
5. **No giant suite.** No CaseFolding.txt corpus. No Unicode 17 rustc `str::to_lowercase` as oracle.

## Verdict

**NOT SELECTION.** FULL default lowercase in Rust is feasible with closed UCD tables. rustc 1.95 **must not** be the fold. Selected custody is **Unicode 15.0.0**; Unicode 16 tables are the right generator input only after rebinding `UNICODE_CASE_DATA_VERSION`. `unicode-case-mapping` is not a drop-in `lib_name_fold`.
