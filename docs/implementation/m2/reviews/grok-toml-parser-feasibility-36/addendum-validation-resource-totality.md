# Addendum: validation / resource / totality boundary (initial 349-case probe)

**Separate from** preserved original `advisory.md` **20839** / `36e35d8dda90632715e712bd54294f55be9539afaa624388aaf2b56637ca18b9` (also `preserved/advisory.md`). This note does **not** rewrite that text.  
**Reviewer:** Grok. Root remains lead. Not Claude agreement.  
**Kind:** Inspection of the preserved initial private probe results, and a precise identity parse-profile boundary. **Not qualification. Not a product parser. Not ACCEPT-DESIGN-UNIT. Not source/runtime/full M2.** Did not edit `/tmp/opensip-implementation/m2-toml-parser-probe-36` (root preserves those bytes and develops corrections separately).

Root follow-up: probe built with `RUSTFLAGS=-F unsafe_code`, `no_std`, no serde/std; pins `toml` 0.9.9+spec-1.0.0 `parse`, `toml_parser` 1.0.5+spec-1.0.0 `alloc`, `toml_datetime` 0.7.4+spec-1.0.0 `alloc`, `serde_spanned` 1.0.4 `alloc`, `winnow` 0.7.13. `result.json` 349 cases. Six defined mismatches plus 128 `UnicodeDecodeError` reference exceptions. Huge ints/floats passed as literals.

## Evidence (initial exploratory classifier only)

Initial `classify` (`initial-parser-differences/src/lib.rs` **934** / `86d624ccfe7c8b04f9789fe8dd3bfeed28277054da9d74dfd0de6fe913d5edcb`): UTF-8 fail → `Syntax`; any `DeTable::parse` fail → `Syntax`; then package/workspace/name key-presence. No calendar walk. No `Limit` class.

| Artifact | Bytes | sha256 |
| --- | ---: | --- |
| Initial `result.json` | 29121 | `cec6cfec01d906dc81476ef27732eef3ee1cda42914244e8c6fcbc1b8c85cd1f` |
| Initial `cases.json` | 53626 | `80a11504e33ecc57b287c8da5da6b327d2d8b68be4e521996fbc101d5569f868` |
| `check_toml_probe36.py` | 4255 | `048000bab0ee7836675845609e318c36013063ed8a90fa51ec293c61b7496959` |

349 cases vs CPython 3.12.13 `tomllib.load(BytesIO)`: **6 defined mismatches**, **128** `reference-exception:UnicodeDecodeError` (not ordinary expected refusal). Expected split of the 349: named 144, syntax 65, classification 8, no-name 2, workspace-only 2, UTF-8 exceptions 128.

Later probe bytes that add a calendar walk and a `Limit` class are **root’s separate corrections**. They are not this addendum’s qualification surface.

## The six defined mismatches

| Label | tomllib | Initial DeTable classifier | Fault class |
| --- | --- | --- | --- |
| `date-0000-01-01` (`x=0000-01-01`) | `syntax` | `named:706b67` | **Validation** (calendar / Python datetime) |
| `date-23:59:60` (`x=23:59:60`) | `syntax` | `named:706b67` | **Validation** (leap second / Python datetime) |
| `depth-127` | `named:706b67` | `syntax` | **Resource** (crate `LIMIT=80` folded into syntax) |
| `depth-128` | `named:706b67` | `syntax` | **Resource** |
| `depth-129` | `named:706b67` | `syntax` | **Resource** |
| `depth-256` | `named:706b67` | `syntax` | **Resource** |

Depths 1/31/32/64 were **named** on both. The crate recursion guard (arrays / inline tables) and dotted-key path cap are 80. Exploratory `Err(_) => Syntax` therefore over-claims grammar at 127+.

Other dates in this 349 (Feb 29 2024 named; Feb 29 2023 / Feb 30 / Apr 31 / day 00 / month 13 / hour 24 / offset `+24:00` / `+00:60` / missing seconds syntax) already agree. Integer/float literals (`2^63`, `2^64`, 80-digit decimal, `inf`/`nan`/`1e9999`) agree because nothing converts them.

## Recommended identity parse profile

Three different refusals. Do not collapse them.

### A. Validation (tomllib datetime profile, after a successful `DeTable::parse`)

`toml_datetime` 0.7.4 follows TOML 1.0 ABNF: four-digit year including `0000`; seconds `00..=60` for leap seconds. CPython `datetime` used by tomllib does not (`date` min year 1; `time` max second 59). Spec-true parse is **not** tomllib syntax.

Identity, not the crate pin, must apply the tomllib profile:

1. After `DeTable::parse` succeeds, walk every `DeValue` (root, arrays, inline tables, nested tables).
2. If `date.year == 0` or `time.second > 59` → **`Syntax`** (same class as `TOMLDecodeError`).
3. Do **not** convert `DeInteger`/`DeFloat` to `i64`/`f64` as a parse gate. Literal retention is why huge ints/floats matched. Classification does not need numeric values.
4. Do **not** enable serde `Value` (that path is i64/f64 and would create new refusals).
5. Walk must be bounded (node budget → **Limit** if exceeded). Root-only scalar checks miss nested datetimes; the 349 corpus only showed root forms, so the walk is required before claiming nested parity.

Month/day/leap-year, hour 0–23, minute 0–59, and illegal offsets already fail inside `toml_datetime` and matched tomllib here. Do not reimplement those.

### B. Resource (crate recursion, not grammar)

Map only these `DeTable::parse` messages to a distinct **`Limit`**, never `Syntax`:

- `cannot recurse further; max recursion depth met` (`RecursionGuard` on array / inline table)
- `recursion limit` (dotted-key path length ≥ 80)

Keep crate `LIMIT=80`. Do **not** enable feature `unbounded`. Do **not** raise 80 to chase tomllib depths 127–256. Real Cargo.toml is shallow; those four rows are pathological.

Membership: `Limit` and `Syntax` both fail named-package projection, so both enter candidate extent as parse failure (selected: named ∪ parse/classification failures). Keep the diagnostic distinct so a 80-deep array is not reported as invalid TOML 1.0.

Optional identity-side byte cap: reuse JSON `MAX_BYTES` (4 MiB) as **Limit**. Not evidenced in the 349 cases; it is the existing identity bound, not a tomllib rule.

### C. Totality (invalid UTF-8 is not `TOMLDecodeError`)

Of 256 `literal-byte-N` documents (`package.name="pkg"\nx="<byte>"`):

| Bytes | tomllib / check script | Initial probe |
| ---: | --- | --- |
| 0–31, 127 (valid UTF-8, illegal in TOML strings) | `syntax` (`TOMLDecodeError`) | `syntax` — match |
| 32–126 except `"` `\` and other string-illegal ASCII | `named` | `named` — match |
| **128–255 (invalid UTF-8)** | **`UnicodeDecodeError`**, recorded as `reference-exception:`** not `syntax` | `from_utf8` fail → `syntax` |

`tomllib.load` on a binary blob decodes UTF-8 **before** TOML. Invalid UTF-8 never becomes `TOMLDecodeError`. Selected `project_named_packages` (advisory35: catch `TOMLDecodeError` → `syntax`) therefore **does not** classify these 128 inputs; they escape as an uncaught exception. That is a reference-totality hole, not a crate disagreement about valid TOML.

Recommend, as two successors, not one silent map:

1. **Identity (bytes in):** `str::from_utf8` fail → distinct `InvalidUtf8`. For enumeration candidate extent, map it to the same bucket as parse failure / `syntax` (JSON already maps `InvalidUtf8` to package.json `syntax`). TOML files are UTF-8; non-UTF-8 is not a named package.
2. **Reference totality (selected Python / replay oracle):** catch `UnicodeDecodeError` from `tomllib.load` on retained bytes and map it to that same bucket **before** claiming identity/Python parity. Until that successor, do not treat probe `syntax` vs `reference-exception:UnicodeDecodeError` as a parser defect, and do not claim the 128 rows are expected refusals.

Do not leave `UnicodeDecodeError` uncaught in the selected projection. An escaped exception is worse than a class mismatch.

## What the 349 cases already settle (no extra gate)

- Key-presence classification (`package` table, non-empty string `name`, `workspace` vs no-name, `package = 1` / `[]` / `[[package]]` classification) matched.
- TOML 1.0 vs 1.1 syntax in this set (newline/trailing comma in inline table, `\e`, optional datetime seconds) matched as syntax.
- Lazy numeric literals: keep. Do not add i64 range, inf-as-error, or float-to-JSON.

## Explicit non-claims

This addendum does not qualify the probe, install a dependency, accept a design unit, or treat later calendar-walk / `Limit` probe edits as product code. Root leads and may apply corrections against the preserved initial 349-case bytes.
