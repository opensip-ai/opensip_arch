# Addendum: exact-profile JSON parse vs canonical-byte equality

**Separate from** preserved original `advisory.md` **14704** / `7644e1228957eb80e53e7fffa606e254ecc90999bfd2c2d57c843fadf965603e` (also `preserved/advisory.md`). This note does **not** rewrite that text.  
**Reviewer:** Grok. Root remains lead. Not Claude agreement.

Original advisory35 said, under compatibility risks, that non-canonical `package.json` is `syntax`. That sentence over-identifies **canonical encoding** with **parse admission**.

## Selected `C.parse` (enumeration_model `project_named_packages` **382–388**)

`C.parse` is the exact JSON **profile** (`canonical.py` **40–65**; product identity `parse` **61–72**):

- UTF-8 bytes, document ≤ `MAX_BYTES`, depth ≤ 32
- Integers in `[-(2^63), 2^64-1]`, no `-0`
- No floats / non-finite (`FLOAT_OR_NONFINITE_FORBIDDEN`)
- No duplicate keys
- No trailing commas, no unquoted keys

It **skips** JSON insignificant whitespace (`space`, `tab`, `CR`, `LF`) and **does not** require object keys in UTF-8 order. `json.loads(..., object_pairs_hook=pairs)` and the Rust `Parser::whitespace` / `BTreeMap` insert both accept pretty-printed and unsorted objects.

Independent probe (selected `canonical.py` via native-case15 env):

| Input | `C.parse` | `raw == C.canonical(parsed)` |
| --- | --- | --- |
| Compact sorted `{"name":"pkg","version":"1.0.0"}` | OK | yes |
| Pretty-printed (newlines, 2-space indent) | OK | **no** |
| Compact **unsorted** `{"version":"1.0.0","name":"pkg"}` | OK | **no** |
| Spaces around `:` / `,` | OK | no |
| Duplicate key | `DUPLICATE_KEY` | — |
| `"x": 1.0` | `FLOAT_OR_NONFINITE_FORBIDDEN` | — |
| Trailing comma | fail | — |

`C.canonical` / identity `encode` then emits compact UTF-8-sorted keys. Pretty and unsorted inputs that parse produce the **same** canonical bytes as the compact sorted form. Named-path **sort keys** in `project_named_packages` use `C.canonical(path)` on path **strings**, not on manifest bytes.

## What is `syntax` for `package.json`

`AdmissionError` from `C.parse` → `reason: "syntax"` (**385–387**). That is **profile** refusal (floats, duplicates, invalid UTF-8, trailing commas, type/range), **not** “bytes differ from `C.canonical`”.

A pretty-printed or key-unsorted `package.json` that is otherwise exact-profile is **named** (if `name` is a non-empty string), not `syntax`.

Canonical-byte equality is a **later** identity/hash/sort obligation (`raw_digest`, `canon_str_list`), after a value exists. Do not treat it as the parse gate.

TOML remains full `tomllib` (TOML 1.0.0) as in the original advisory; this addendum only corrects the JSON parse/canonical mix-up.
