# Correction: stage20 advisory semantic errors (1)–(4)

**Reviewer:** Grok. Root remains lead. Not Claude agreement.
**Kind:** Separate correction of advisory-20. Original `advisory.md` / `advisory.json` **unchanged**. **Not ACCEPT-DESIGN-UNIT.**
**Original pins:** `advisory.md` 9409 / `041be1cf2a0c5821867bf499191e278904674ac949516570b3f35c9776b31b97`; `advisory.json` 2342 / `23bf03f3ad1117a7455c2612961a1071d283fc79cd0afd0868256ecfe2ca79f8`.
**Probes:** `probes/run_probes.py` against selected `admit_stage_output_schema` 735–761, `ordered` 189–214, `get` 917–922, live `identity_record_shape` 410–443, jsonschema 4.25.1 `Draft202012Validator.check_schema`.

## (1) Canonical bytes vs `C.parse` — advisory overstated

`admit_stage_output_schema` 752 is **`C.parse(raw)` only**. There is **no** `C.canonical(document)==raw` (contrast `canonical_bytes` / `payload` 1037–1039, and `admit_normalization_specification` 777).

Selected `parse` (exact-profile `canonical.py` 43–68) is `json.loads` with `parse_int` / `parse_float=forbidden`. JSON **whitespace between tokens is valid**. Lexical **non-integers are not**: `1.0` → `FLOAT_OR_NONFINITE_FORBIDDEN`; `01` is not a JSON integer token (`AdmissionError` from the decoder).

**Probe:** pretty-printed 2020-12 document (indent=2) parses; `canonical(parse(raw)) != raw`; **`admit_stage_output_schema` ADMITs** when `outputSchemaDigest` / tree sha256 are the digest of those **pretty bytes**. Compact canonical bytes also ADMIT when they are the registered digest.

So: the **registered artifact may be non-canonical whitespace** if that is what was hashed into the closure tree. It may **not** be a float/leading-zero integer. Future evaluator owner must not require `canonical(parse(raw))==raw` unless a later unit adds that law. Digest still binds the **exact retained bytes** (749).

## (2) Duplicate tree paths — helper vs admitted `get(closure)`

`ordered` 198–213: `name in ['sourceInventory','tree','blobs']` keys `path` UTF-8; `keys!=sorted(keys) or len(keys)!=len(set(keys))` → `ORDER_OR_DUPLICATE`.

`get` 917–922: `identifier(domain,value)==key` then `admit_closure_field_kinds`. `identifier` 218–221: schema + **`ordered(value)`**.

**Probe:** two tree rows, same path, different sha256 → `ordered` `ORDER_OR_DUPLICATE`. Helper `members[0]` (746–748): spec digest matching **first** row proceeds to `BLOB_DIGEST`; spec digest matching **second** row → `REGISTRATION_MISMATCH` (second row never selected).

Full caller **1794** `get(spec['producerClosure'],'closure')` therefore **cannot** present a duplicate-path tree. `members[0]` as “first of many” is **helper-only**, unreachable for an identifier-admitted closure. Do not implement a duplicate-path policy in the owner beyond exact path match on a unique tree. Schema `uniqueItems` on `tree` is whole-item equality (identity-v3 290–296), not path uniqueness; **path uniqueness is `ordered`**, not uniqueItems.

## (3) `identity_record_shape` is not selected `payload()`

Live `identity_record_shape` 407–418 / `check_identity_value_shape` 420–443: canonical record + identity-v3 shape + `descriptors::ordered`. Comment: **no identity, references or admission**. It does **not** call `admit_closure_field_kinds`.

Selected `payload(...,'stage-spec')` 1041–1054 **does** `admit_closure_field_kinds` (1051) so `stage-spec.producerClosure` kind is **`provider`** (identity-v3 4737) **before** 1794.

Advisory-20’s shape-vs-authority table listing `identity_record_shape` as including producer **kind** is **wrong**. Kind is a **caller/API obligation**: `get`/`payload`/`admit_closure_field_kinds`, or the future evaluator fn must check it explicitly. Reusing only `identity_record_shape` would admit a non-provider closure descriptor as stage-spec shape and still need a separate role check before tree membership.

## (4) `Draft202012Validator.check_schema` (jsonschema 4.25.1)

Selected 756: `Draft202012Validator.check_schema(document)` with **default** `format_checker = Validator.FORMAT_CHECKER`.

Live FormatChecker names: `date`, `email`, `idn-email`, `ipv4`, `ipv6`, `regex`, `uuid`. **`uri` is absent.**

**Probe:**

| Schema | `check_schema` |
| --- | --- |
| unknown `x-opensip-stage-output` | **accept** |
| `"$ref": "https://example.invalid/schema.json"` | **accept** (no retrieval) |
| `"pattern": "("` | **SchemaError** `'(' is not a 'regex'` (meta-schema `format: regex`) |
| `"$id": "not-an-email"` | **accept** (`$id` is uri-reference; **uri not checked**) |

This validates the document **as an instance of the 2020-12 meta-schema**. It does not instance-validate stage outputs, does not fetch `$ref`, and does not apply identity exact-integer / `x-opensip-order` / registered-document law.

**Identity schema engine** (`crates/identity/src/schema.rs`) compiles the **product** dialect (selected keywords, `x-opensip-order`, exact integers, `registered_schema_blob` document set). It is **not** a replacement for producer-published Draft 2020-12 meta-schema checking. Using `SchemaHandle.admit_json` or `registered_schema_blob` would apply the wrong program to the wrong document set.

## Disposition

| # | Advisory-20 | Correction |
| --- | --- | --- |
| 1 | implied canonical encoding of schema bytes | **Withdraw.** Parse+digest only; pretty whitespace lawful if registered; floats/leading-zero ints not |
| 2 | `members[0]` duplicate-path trap | **Narrow.** Unreachable after `get`/`identifier`/`ordered`; keep as helper-only |
| 3 | `identity_record_shape` includes producer kind | **Withdraw.** Shape/order only; role is caller/`payload`/`admit_closure_field_kinds` |
| 4 | remote `$ref` / unknown keywords | **Sharpen.** Unknown keywords and remote `$ref` accepted; invalid `pattern` regex refused; no `uri` format; identity compile ≠ this meta-check |

Future evaluator `admit_stage_output_schema` should follow **735–761 as written** (parse, not canonical-eq; unique tree via admitted closure; explicit producer kind in caller; jsonschema `check_schema` or a documented equivalent of that meta-schema, not identity `schema.rs`).

`requiredFindings` for this correction: none as a selection unit. Original advisory remains a non-acceptance map with these four overstatements corrected here.
