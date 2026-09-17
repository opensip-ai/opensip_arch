# Advisory: TOML package-projection semantic compatibility (trial-38)

**Reviewer:** Grok. Root remains lead. Not Claude agreement.  
**Kind:** Bounded independent semantic probe of the private identity borrowed parser + evaluator package projection. **Not source acceptance. Not dependency acceptance. Not ACCEPT-DESIGN-UNIT. Not runtime/full M2. Not qualification of trial-38.**  
**Work tree:** `/tmp/opensip-implementation/m2-grok-toml-semantics-38` only. Did not edit the root trial, product, architecture, locks, or history. Did not retest unsafe or recursion/byte-limit resource depth (assigned elsewhere).

Root archived feasibility-36 unchanged. Totality-37 (`E689620`) maps invalid UTF-8 to syntax. Trial-38 wrapper now rejects a **leading** UTF-8 BOM; resource Limit aborts the whole projection as a typed error (not `parseFailed`). Initial BOM mismatch is preserved at `m2-package-parser-trial-38/initial-bom-difference`. Current trial `package-result.json` reports 0 mismatches on its 1121 cases (7 of those are local Limits).

## Verdict

**Not tomllib-identical on incomplete radix integers.** Other requested semantic families in this probe matched selected CPython 3.12.13 `tomllib` classification.

`toml` 0.9.9+spec-1.0.0 `DeTable` accepts `0x` / `0o` / `0b` with **no digits**. Selected `tomllib.load` raises `TOMLDecodeError`. Official toml-test v1.6.0 lists those three as TOML 1.0 **invalid**. Because identity does not convert `DeInteger` (lazy literals), the bad value never becomes syntax. Evaluator then classifies a successful tree:

| Document | Selected (tomllib) | Trial-38 | Candidate extent |
| --- | --- | --- | --- |
| `x=0x` only | `parseFailed` `syntax` | `unnamed` `no-name` | selected: yes; trial: **no** |
| `[package]\nname="p"\nx=0x` | `parseFailed` `syntax` | **`named` `p`** | selected: failed candidate; trial: **named subject** |

That is a full-document classification defect, not a spec-validity footnote. Same hole in arrays, inline tables, dotted keys, and `0x` before a comment or trailing space.

Leading BOM now matches. BOM in other positions, CRLF/multiline escapes, duplicate/dotted/array-table shapes, calendar year-0 / leap-second, unicode, and TOML 1.1 syntax (as 1.0 invalid) matched in this corpus.

## Pins

| Artifact | Bytes | sha256 |
| --- | ---: | --- |
| Copied probe `bin/opensip-package-probe` | 2633816 | `73508e9aa4c2fae5ce1a987ca27ceae3d48c41fd5f15cd794eee0748bf762009` |
| Trial identity `toml.rs` (BOM wrapper present) | 5782 | `b9e90932eba465fc1c11060ca07f0b29e80e78be5a67ca219901a50641a7ffed` |
| Initial `toml.rs` (pre-BOM wrapper) | 3041 | `e3a4cffca46f692fb96939a6793af3e4f62c47cec886c121e95969c49c299ff3` |
| Trial evaluator `enumeration.rs` | 26596 | `5f11a3791d24a6f6779a8fea4edd685ece86bdc85735aa02a42099c7de157a14` |
| `check_packages38.py` | 5739 | `8d0e313d1925e0dbd33122c7ac8801ec9b00378f099646a577a8dcc84b37e0d7` |
| Selected totality-37 `enumeration_model.v1.py` | 49833 | `689620ec7c1e2ecc417a8ccdbc379cd94c8ca985118a44b727126f15a3af9072` |
| Overlay parent foundation enumeration | 49811 | `69b0eee39a45a941d7ab1ef22c0c8be161edd436b1441b27017f98fd1bcffe85` |
| Current trial `package-result.json` | 458 | `b8957e2c47ad69d8d1cadc02a630e30dc7e0209e42f99be6d14a2a7ddead7e5e` |
| Initial BOM `package-result.json` | 1378 | `b5d156e24dbbf47137c67568e2f9b1d9a36ccf70992dacaa79e8392101461410` |
| toml-test v1.6.0 tarball | 79497 | `79ee1f9edef786e28cc54504179672071dbc7bad24d73348e8e7d7e766068abc` |
| This probe script | 11057 | `2165946bf72d9fb521decaed5ae2c14d30503ff7b8d075d23201378f3f92f723` |
| `probes/semantics-result.json` | 3270 | `a9a0da56fe8740d80cd88bf7a027bf05a8bcc3b00bf10f8f5d7be8c9b58eebbc` |

Reference: `/tmp/opensip-implementation/native-case15-reference-env/bin/python -I -B` **CPython 3.12.13**, selected `project_named_packages` overlaid as in `check_packages38.py` (`except (tomllib.TOMLDecodeError, UnicodeDecodeError)` → syntax). Probe wire is full `project_enumeration_packages` classification, not `DeTable` validity alone.

## Probe scope (675 + 18 follow-up)

Hand-crafted Cargo.toml documents plus every `.toml` path in toml-test v1.6.0 `tests/files-toml-1.0.0` as a whole `Cargo.toml`. Also prefixed the nine TOML 1.0-invalid / 1.1-valid official files after `[package]\nname="p"\n`.

Not in this probe: recursion 80 / depths 127–256 / 4 MiB byte cap / winnow unsafe / JSON `package.json` beyond what trial-38 already ran.

## Exact repros (preserve)

Official toml-test v1.6.0 (TOML 1.0 invalid list):

| File | sha256 | bytes | Selected | Trial |
| --- | --- | --- | --- | --- |
| `invalid/integer/incomplete-hex.toml` | `95d6ff6bb3a2858075205f8e8173d4a3efa50a105eb43d1518be636073add7ba` | `incomplete-hex = 0x\n` | `parseFailed` syntax | `unnamed` no-name |
| `invalid/integer/incomplete-oct.toml` | `0033413ec904a131025d97bc0fec763a5593ec0b93edc46c84a26503659cf9e6` | `incomplete-oct = 0o\n` | syntax | no-name |
| `invalid/integer/incomplete-bin.toml` | `c0a5b80a6c5a3d7d786c7e575b7960fce4b78a36b62434e06115d631bd080907` | `incomplete-bin = 0b\n` | syntax | no-name |

Named-package poison (same root cause; follow-up probe):

| Label | UTF-8 | hex | Selected | Trial |
| --- | --- | --- | --- | --- |
| `named-incomplete-hex` | `[package]\nname="p"\nx=0x\n` | `5b7061636b6167655d0a6e616d653d2270220a783d30780a` | syntax | **named `p`** |
| `named-incomplete-oct` | `[package]\nname="p"\nx=0o\n` | `5b7061636b6167655d0a6e616d653d2270220a783d306f0a` | syntax | named `p` |
| `named-incomplete-bin` | `[package]\nname="p"\nx=0b\n` | `5b7061636b6167655d0a6e616d653d2270220a783d30620a` | syntax | named `p` |
| `named-incomplete-hex-space` | `[package]\nname="p"\nx=0x \n` | `5b7061636b6167655d0a6e616d653d2270220a783d3078200a` | syntax | named `p` |
| `comment-after-0x` | `[package]\nname="p"\nx=0x#c\n` | `5b7061636b6167655d0a6e616d653d2270220a783d307823630a` | syntax | named `p` |
| `array-incomplete-hex` | `[package]\nname="p"\nx=[0x]\n` | `5b7061636b6167655d0a6e616d653d2270220a783d5b30785d0a` | syntax | named `p` |
| `inline-incomplete-hex` | `[package]\nname="p"\nx={a=0x}\n` | `5b7061636b6167655d0a6e616d653d2270220a783d7b613d30787d0a` | syntax | named `p` |
| `dotted-incomplete-hex` | `[package]\nname="p"\na.b=0x\n` | `5b7061636b6167655d0a6e616d653d2270220a612e623d30780a` | syntax | named `p` |

Cause in pinned `toml_parser` 1.0.5 `decode_zero_prefix`: after `0x`/`0o`/`0b`, `ensure_radixed_value` loops digits and reports nothing when the remainder is empty. `DeInteger` keeps an empty literal. Identity’s existing walk rejects year 0 / second > 59 but does **not** inspect integers. `0x0` / `0x00` named on both. `0x_`, `0xg`, `0b2`, `0o8`, `+0x1` syntax on both.

## Families that matched (this corpus)

- **BOM:** leading EF BB BF now syntax (wrapper). Space/tab/LF/CRLF then BOM, BOM before `name`, between keys, EOF, comment, inside basic/literal/multiline strings, `\uFEFF` in a name, quoted/bare BOM keys, double BOM, UTF-16 BOM → same class as tomllib.
- **Newlines:** LF, CRLF, mixed, bare CR, multiline first-line trim, `\`+LF / `\`+CRLF / `\`+CR, escaped `\n`/`\r`, raw CR in a basic string.
- **Tables:** duplicate keys/headers, parent/sub order, dotted then `[package]`, inline then header, `[[package]]`, AOT vs table clashes, quoted vs bare duplicate, case-sensitive keys, dotted/inline `package.name`.
- **Datetime/number/unicode:** year 0000 and `23:59:60` still syntax (walk); leap day, offsets, `inf`/`nan`/`1e9999`/huge int; NFC/NFD names; `\u0041`; unescaped SOH; invalid UTF-8; surrogate `\uD800`.
- **TOML 1.1 as 1.0 invalid:** trailing comma / newline in inline table, `\e`, `\x41`, datetime/time without seconds — syntax on both, including when placed after a valid `package.name` (does not hide the failure).

## Suggested identity-side profile (not implemented here)

In the existing `parse_toml` walk, beside the datetime checks: if a `DeValue` is an integer whose radix is 2/8/16 and `as_str()` is empty → `TomlError::Syntax`. Do not convert to `i64`. Do not enable serde `Value`. Do not treat this as a crate upgrade to spec-1.1.

Until that (or equivalent) exists, trial-38 must not be treated as tomllib classification.

## Unqualified limits

Not a live install; not a dependency-policy successor; not a claim that 675 cases exhaust TOML; not a re-audit of Limit vs `parseFailed`; not unsafe/geiger work; not JSON-profile work. Root leads any wrapper correction against the preserved repros.
