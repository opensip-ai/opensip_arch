# Addendum: residual float-alias is outside JSON-C

**Reviewer:** Grok. Root remains lead. Not Claude agreement.  
**Kind:** Precision addendum to completed totality-42 advisory. **Does not rewrite** `advisory.md` / `advisory.json`.  
**Preserved originals:** `advisory.md` **14380** / `7a4f55838ac5f8c956749611ed60ef92f13db7fd64e4ecab5df23e2aad7131c2`; `advisory.json` **6087** / `6c45791a9f56f886e037176652fbcedf7ab40f7c218d37b18225b107e87f1e54`. Independently re-hashed after this file was written; bytes unchanged.

Root fully read the original reports. This addendum corrects one precision claim only.

## Withdrawal

The original residual `0.0 == 0` occupancy note is **outside JSON-C**. It was an in-memory Python probe (`float` objects constructed in the harness), not an admitted JSON-C locator. It is **not** a totality hole, **not** a kernel matching obligation, and **not** a product feature.

**Do not add float alias or product float support.**

The original verdict stands: preserve defined outputs; TypeError-catch candidate is sound as a totality correction; not selected by that advisory. Python bool/int schema-failed occupancy (`False==0` / `True==1`) remains in-profile because JSON-C **does** include Bool.

## Independent confirmation

Selected `canonical.py` **8995** / `ad88e58fe90fe66531dbe39f4694f20ad3bc6ce2099ae4fc762c0251468496f7` (trial41 overlay, same pin as the new 159-file fixture):

| Probe | Result |
| --- | --- |
| `typed(0.0)` / `typed(1.5)` / `canonical(0.0)` | `AdmissionError: EXACT_JSON_TYPE_REQUIRED` |
| `parse(b"0.0")` / `b"1.0"` / `b"1e0"` / `b"NaN"` | `AdmissionError: FLOAT_OR_NONFINITE_FORBIDDEN` (`parse_float` / `parse_constant` = forbidden) |
| `parse(b"0")` / `typed(0)` / `typed(False)` | admitted |
| `C.equal_typed(False, 0)` | False (types distinct) |
| Python `False == 0` | True (in-profile Bool/Integer alias on schema-failed membership only) |

`typed()` accepts only `None`, `bool`, `int`, `str`, `list`, `dict`. A Python `float` is not a JSON-C value.

Rust `crates/identity/src/canonical.rs` **11878** / `e524652830590943dfb33c917b95ae0e87255588df66fcad114ffccad9c3fcb1`:

```rust
pub enum Value {
    Null,
    Bool(bool),
    Integer(Integer),
    String(String),
    Array(Vec<Value>),
    Object(BTreeMap<String, Value>),
}
```

No `Float` variant. `lib.rs` exports `Value as JsonValue`. Lexical `integer()` returns `Error::FloatForbidden` on `.` / `e` / `E`. Kernel `number()` matching `V::Integer` only is the JSON-C integer case, not a missing float alias.

Private probe: `probes/float-jsonc-confirmation.json` (this review42 tree only).

## What remains from the original advisory

- 18 unhashable array/object locators must not throw.
- Unhashable locators do not occupy `schema_failed` → SCHEMA then MISSING.
- All previously defined E39 outputs preserved, including schemaVersion-array SCHEMA-only and True SCHEMA+MISSING.
- False numeric SCHEMA-only is selected E39 Python membership on schema-failed rows only; do not silently switch to typed Bool≠Integer inside the totality patch.
- Formal reference-unit review is separate.

No product, architecture, frozen, or original-advisory edits.
