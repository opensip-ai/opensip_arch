# Addendum: decimal-integer reference totality (`int_max_str_digits`)

**Separate from** original `advisory.md` **8474** / `3e2c8365df8c690652994fae8d5127e3609637df976b279f87b28535ec12c56d` (also `preserved/advisory.md`). This note does **not** rewrite that text or its 675-case probe.  
**Reviewer:** Grok. Root remains lead. Not Claude agreement.  
**Kind:** Bounded advice on CPython 3.12.13 `tomllib` integer conversion vs selected `E689620` exception totality. **Not a new reference unit. Not source/dependency acceptance. Not silent ValueError→syntax. Not parity.** Did not edit selected E, the original probe, or product/trial.

Root reproduced the original incomplete-prefix findings, preserved `initial-empty-radix-difference`, and added `DeInteger.as_str().is_empty()` syntax in the trial wrapper. That correction is **out of this addendum’s qualification surface**. This note answers the new decimal-digit totality hole root observed: 4300 decimal digits accepted, 4301/5000 raise raw `ValueError` because ambient `sys.int_max_str_digits` is 4300; hex of 5000 digits is accepted.

## Evidence (pinned CPython 3.12.13, default limit 4300)

`/tmp/opensip-implementation/native-case15-reference-env/bin/python -I -B`: `sys.get_int_max_str_digits() == 4300`.

Document shape `[package]\nname="p"\nx=<literal>\n` (huge integer is a **package field**, so conversion runs before classification returns). `tomllib.load` / `loads` identical.

Exact constructions (UTF-8, no BOM):

| Label | Literal | Construction |
| --- | --- | --- |
| decimal-4300 | `1` + 4299 zeros | `b'[package]\nname="p"\nx=' + b'1' + b'0'*4299 + b'\n'` |
| decimal-4301 | `1` + 4300 zeros | `b'[package]\nname="p"\nx=' + b'1' + b'0'*4300 + b'\n'` |
| decimal-5000 | `1` + 4999 zeros | `b'[package]\nname="p"\nx=' + b'1' + b'0'*4999 + b'\n'` |
| hex-5000 | `0x` + 5000 `f` | `b'[package]\nname="p"\nx=0x' + b'f'*5000 + b'\n'` |
| sibling-4301 | dotted package, root `x` | `b'package.name="p"\nx=' + b'1' + b'0'*4300 + b'\n'` |

`PYTHONINTMAXSTRDIGITS` overrides the same cap. Independent replay of these bytes is not stable until the oracle pins 0 or N.

| Literal | Result |
| --- | --- |
| decimal 80, 4299, **4300** digits | OK, named `p` |
| decimal **4301**, 4302, 5000 digits | **`ValueError`**: `Exceeds the limit (4300 digits) for integer string conversion` |
| decimal 4301 with underscores (digit count 4301) | same `ValueError` |
| negative decimal 4301 | same `ValueError` |
| hex / oct / bin **4301 and 5000** digits | OK, named `p` |
| `1e9999` float | OK, named `p` |
| after `sys.set_int_max_str_digits(0)`: decimal 4301 and 5000 | OK, named `p` |

Selected `project_named_packages` (**402**): `except (tomllib.TOMLDecodeError, UnicodeDecodeError)`. **`ValueError` is not caught.** Same class of hole as pre-totality-37 `UnicodeDecodeError`: the reference can abort instead of classifying.

This is **outside** the 80-digit scalar cases in probe-36 / trial-38. Identity `DeTable` retains the decimal literal and does not call `int()`; a 4301-digit unused field still yields a successful tree and a named package.

## Do not map this to syntax

`ValueError` here is CPython’s conversion DoS cap (PEP 3319 / 3.11+), not TOML 1.0 grammar. TOML 1.0 integers are unbounded. Hex/bin/oct of the same length already succeed under the same interpreter. Treating `ValueError` as `parseFailed` `syntax` would:

- disagree with TOML 1.0 and with the trial’s lazy `DeInteger`;
- disagree with hex/bin/oct of equal or greater length;
- follow **ambient** `sys.int_max_str_digits` / `PYTHONINTMAXSTRDIGITS`, so the same bytes would classify differently across hosts.

A Rust-only decimal `Limit` does **not** repair the reference: selected E still raises. Mapping Python to syntax while Rust returns `EnumerationExtentError::Limit` would also mismatch (row-level `parseFailed` vs abort of the whole projection; trial Limit is already not a selected `parseFailed` reason).

## Bounded correction (advice, not a unit)

Pick **one** profile before writing a reference successor. Do not mix them.

### Option A (recommended while tomllib remains the oracle)

Make the oracle unbounded, matching TOML 1.0 and lazy identity integers.

- In the **next** totality/reference unit only: around `tomllib.load`, `old = sys.get_int_max_str_digits(); sys.set_int_max_str_digits(0)` and restore `old` in `finally`.
- Or require `PYTHONINTMAXSTRDIGITS=0` for every replay host and assert it at the start of the projection.
- Identity: **no** new decimal-digit Limit. Keep literals; do not call `to_i64`.
- Classification of 4301 decimal digits: **named** (if `package.name` is a non-empty string), same as 80 digits and same as hex-5000.

This removes ambient config from classification. Cost is large-int CPU in the Python oracle only; identity already avoided that conversion.

### Option B (explicit resource bound, both sides)

If a digit cap is product law, it must be **chosen and pinned**, not “CPython’s current default”.

- State N (if copying today’s default, N=4300) as identity/oracle law: count **decimal digits only** (sign ignored, underscores ignored), matching CPython’s count.
- Identity: if any `DeInteger` with radix 10 has `as_str()` digit count > N → **`TomlError` resource variant** (`NodeLimit` sibling or a new `DigitLimit`), which evaluator already maps to **`EnumerationExtentError::Limit`** (abort whole projection).
- Reference: do **not** rely on uncaught `ValueError`. Either `set_int_max_str_digits(N)` and catch `ValueError` as the same **Limit** (new selected behavior: not `parseFailed`, not syntax), or pre-scan decimal literals and refuse Limit without calling `int()`.
- Hex/bin/oct: leave unbounded unless separately pinned (CPython already accepts 5000 hex digits at default N).
- Selected E today has **no** resource reason in `parseFailed`. Limit abort vs per-row syntax is a law change and needs the successor, including mixed-snapshot tests (one huge Cargo.toml among many).

Do not ship B on Rust only. Do not ship B by catching `ValueError` as syntax.

## Tests required before any new reference unit

Use the pinned 3.12.13 binary with the successor’s documented `int_max_str_digits` policy, and the identity wrapper:

1. decimal 4300 → named `p`
2. decimal 4301 and 5000 → named under A; **Limit** (not syntax, not uncaught) under B
3. hex/bin/oct 5000 → named under both
4. decimal 4301 with underscores and with leading `-`
5. huge decimal as a sibling of `[package]` (`package.name="p"\nx=…`) and as a field inside `[package]`
6. assert the oracle’s `get_int_max_str_digits()` equals the pinned policy (0 or N) for the duration of `tomllib.load`
7. incomplete `0x`/`0o`/`0b` remain **syntax** (root’s empty-literal refusal); that is grammar, not this digit cap
8. do not treat `ValueError` as `TOMLDecodeError`

## Unqualified

Not an edit of `E689620`. Not a claim that trial-38 after empty-radix is qualified. Not a chosen N unless root picks A or B. Original 675-case incomplete-radix report stays as written against copied probe `73508e9aa4c2fae5ce1a987ca27ceae3d48c41fd5f15cd794eee0748bf762009`.
