# Follow-up: `predicate_node_at` digits vs “shortest decimal”

**Reviewer:** Grok. Root remains lead. Not Claude agreement.
**Kind:** Probe of selected helper 651–665 vs identity-v3 2758 prose. Original advisory21 bytes **unchanged**. **Not ACCEPT-DESIGN-UNIT.**
**Original pins:** `advisory.md` 12386 / `55f48b2e1522163fd806d3e05b7247439ae3ba4cda525f333f155f9d65a5e1c6`; `advisory.json` 3342 / `b0c4dffb2832d3553846dec54d8e801ca665a372e5519112a8b7fef09c8b7bb5`.
**Probe:** `probes/predicate_address_digits.py` against the selected function (exec 646–665). Do **not** infer a Rust ASCII equivalent.

## Laws in play

| Layer | What it actually says |
| --- | --- |
| Schema `predicateId` | `$ref: Text` — string length 1–4096, **no** `[0-9]` / `^p(\.[1-9][0-9]*\|\.0)*$` pattern (identity-v3 2778–2779). Unicode digits are **schema-valid**. |
| Prose (identity-v3 2758 + helper docstring 653) | Root `p`; `a.i` zero-based; **“shortest decimal, no leading zero.”** |
| Helper 657–661 | `part.isdigit()` **or** (`len>1` and `part[0]=='0'`) → named `PREDICATE_ADDRESS`; else `index=int(part)`. |

`part[0]=='0'` is the **ASCII** code point U+0030 only. `str.isdigit()` is Unicode (Nd and some No). `int(part)` accepts Unicode **decimal** digits (Nd), not superscripts.

## Probe (and-node, two exists leaves)

| Address | `isdigit` | ASCII `0`-prefix | `int` | Helper |
| --- | --- | --- | --- | --- |
| `p.0` / `p.1` | True | no | 0 / 1 | **ok** (leaf) |
| `p.01` | True | **yes** | 1 | named **`PREDICATE_ADDRESS`** |
| `p.` + Arabic-Indic `٠` / `١` | True | no (`٠!='0'`) | 0 / 1 | **ok** (same nodes as ASCII) |
| `p.` + `٠١` or `٠`+`1` | True | no | 1 | **ok** — **leading zero not refused** |
| `p.0١` | True | **yes** (ASCII 0) | 1 | named **`PREDICATE_ADDRESS`** |
| `p.` + fullwidth `０` / `１` / `０１` / `０1` | True | no | 0 / 1 | **ok** — **leading fullwidth zero not refused** |
| `p.` + superscript `⁰` `¹` `²` `⁰¹` | **True** | no | **ValueError** | **uncaught `ValueError`**, not `AdmissionError('PREDICATE_ADDRESS')` |

Python 3.14.6 in the probe env: superscripts are `isdigit()==True` and `int()` raises `invalid literal for int() with base 10`. The `or (len>1 and part[0]=='0')` short-circuit never runs for a single superscript; `int(part)` is reached.

## Schema vs helper vs prose

- **Schema permits** these strings as `predicateId`.
- **Prose** claims shortest decimal / no leading zero (unspecified alphabet).
- **Helper** enforces no-leading-zero **only for ASCII `0`**. Arabic-Indic and fullwidth leading zeros **navigate** (`int` value 1). Superscripts **do not** name `PREDICATE_ADDRESS`; they **raise `ValueError`**, which `open_run_closure` 1844 does not wrap.

`predicate_child_addresses` (647–649) emits **ASCII** `str(i)` / `'.0'`. A witness that stored Arabic `p.١` could still **locate** the same node as `p.1` if the helper is used as-is; `WITNESS_CHILD_ADDRESS_JOIN` compares `sorted(witness['childPredicateIds'])` to those **ASCII** emissions, so mixed alphabets fail that join even when `predicate_node_at` succeeds.

## Disposition for the next owner

Do **not** copy `isdigit`+`int` and call it “shortest decimal.” Choose an explicit alphabet (typically ASCII `[0-9]` with the existing leading-zero rule) and map every reject to **`PREDICATE_ADDRESS`** (no raw `ValueError`). This follow-up does not select that alphabet. Rust `is_ascii_digit` / `parse::<u32>` is **not** inferred here.

Original advisory21’s address-law bullet remains directionally right for **ASCII `01`**; it did not record Unicode digits or the uncaught `ValueError`.
