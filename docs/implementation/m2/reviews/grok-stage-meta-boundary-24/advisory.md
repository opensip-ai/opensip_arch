# Advisory: portable Draft 2020-12 `check_schema` for the stage-output owner

**Reviewer:** Grok. Root remains lead. Not Claude agreement.  
**Kind:** Bounded technical map so a later stage-output owner can own **exact** selected `Draft202012Validator.check_schema(document)` behavior in Rust. **Not ACCEPT-DESIGN-UNIT. Not implementation. Not runtime-11. Not predicates-23.**  
**Work tree:** `/tmp/opensip-implementation/m2-grok-stage-meta-boundary-24/review`. No live/frozen/history edits.

Stage-20 `advisory.md` / `correction.md` are **read, not rewritten**. Correction (4) is the starting point; this note answers whether that meta-check is already a pinned portable dialect or still ambient helper behavior.

Live lock independently **18 inventory / 24 contract**, last contract `native-runtime-selection-v10`. Selected helper: `predicate-matching-reference-selection-v1/reference/identity_model.py` **158607** / `7f840b9a…89e9` `admit_stage_output_schema` 735–761 (same 735–761 text as 619d). Probes: `native-case15-reference-env` Python **3.12.13** / jsonschema **4.25.1**.

## What 756 actually does

`Draft202012Validator.check_schema(document)` with default `format_checker=Validator.FORMAT_CHECKER` (jsonschema 4.25.1 `validators.py` 308–317):

1. Treats `document` as an **instance** of `Draft202012Validator.META_SCHEMA` (bundled `jsonschema_specifications` 2025.9.1 / `referencing` 0.37.0). **No HTTP.**
2. Uses import-time `draft202012_format_checker`.
3. Raises `SchemaError` on the first meta-schema violation.

It is **not** instance-validation of stage outputs, not `$ref` retrieval of the producer document, not identity exact-integer / `x-opensip-order` / `registered_schema_blob` law.

Helper **754–755** separately requires a **dict** and `$schema` **exactly** `https://json-schema.org/draft/2020-12/schema`. That guard is **not** inside `check_schema` (draft-07 URL and missing `$schema` still pass `check_schema`). Pretty JSON is lawful at `C.parse` (correction 1). Root `true`/`false` pass `check_schema` but fail the dict guard.

## Observed format dialect (this env)

`FORMAT_CHECKER` names: `date`, `email`, `idn-email`, `ipv4`, `ipv6`, `regex`, `uuid`.

**Absent** (optional packages not installed): `uri`, `uri-reference`, `hostname`, `idn-hostname`, `iri`, `iri-reference`, `date-time`, `time`, `duration`, `json-pointer`, `relative-json-pointer`, `uri-template`. Packages `rfc3987`, `rfc3986_validator`, `rfc3987_syntax`, `fqdn`, `idna`, `rfc3339_validator`, `jsonpointer`, `uri_template`, `isoduration` are all **missing**. `format: regex` is `re.compile` (Python 3.12), not ECMA-262.

jsonschema registers `uri` **only if** rfc3987 or rfc3986_validator is importable at module load (`_format.py` 303–392). The selected helper does **not** pin that absence. Installing an optional URI package in the helper environment would **silently add** `uri` / `uri-reference` checks. Root stage-20 disposition already required pinning environment format support if translated.

## Probe table (local, no network)

| Case | `check_schema` |
| --- | --- |
| unknown `x-opensip-stage-output` / `fooBar` | accept |
| `"$ref": "https://example.invalid/schema.json"` (root or in properties) | accept, no fetch |
| `"pattern": "("` | **SchemaError** `'(' is not a 'regex'` (meta-schema `format: regex`) |
| `"pattern": "^foo$"` / `(?P<name>.)` / `(?<=a)b` | accept (Python `re`) |
| `"$id": "not-an-email"` / `"not a uri"` | accept (`uri-reference` not registered) |
| nested bool `additionalProperties: false`, `items: true`, `$defs.deny: false` | accept |
| root `true` / `false` | accept (`check_schema` only) |
| `"format": "email"` / `"not-a-registered-format"` | accept (meta-schema does not enum format names) |
| `exclusiveMaximum`, `multipleOf`, `unevaluatedProperties`, `dependentRequired`, `$comment` | accept |
| pretty `json.loads` then `check_schema` | accept; canonical≠raw |
| draft-07 `$schema` or missing `$schema` | accept (`check_schema` only; helper 754–755 still refuses) |

## Design does **not** pin a portable dialect

Identity-v3 `outputSchemaDigest.registeredBy` (2998–3023) names tree path, declaration, and refusal codes. It does **not** name jsonschema 4.25.1, the seven format checkers, Python `re`, `jsonschema-specifications` 2025.9.1, or “optional URI packages off.”

The selected helper **imports** `jsonschema` at call time. Behavior is the **process** dialect, not a reviewed successor record.

Therefore: **missing portable behavior.** A Rust owner cannot “just call a jsonschema crate” or identity `schema.rs` and claim 756. An **explicit reviewed successor** is required before or as parent of the stage-output implementation unit.

## Identity `schema.rs` is the wrong program (named differences)

Product engine (`crates/identity/src/schema.rs`, TCB: `sha2-const-stable=0.1.0`, `unicode-normalization=0.1.24`; **no** jsonschema crate). Evaluator depends **only** on identity. `Program::check_schema` is the **product** dialect:

| Producer 2020-12 fact | `check_schema` 4.25.1 | identity compile |
| --- | --- | --- |
| `x-opensip-stage-output` | accept (unknown keyword) | **Schema** (not in `annotation()`) |
| `"format": "email"` | accept | **Schema** (no `format` arm) |
| `exclusiveMaximum` / `multipleOf` / `unevaluatedProperties` / `dependentRequired` / `$comment` | accept | **Schema** (unselected keyword) |
| `"$ref": "https://example.invalid/…"` | accept, no fetch | **Reference** (must resolve to a **supplied** document) |
| `"pattern": "^foo$"` | accept (`re`) | **Pattern** (closed `schema_patterns` TABLE only) |
| nested bool schemas | accept | accept |
| pretty whitespace | N/A (already parsed) | product parse forbids floats/`01`; whitespace is a **byte** issue at 749, not compile |

Using identity compile as `check_schema` would **silently narrow** the accepted producer-document space. Forbidden. Do not treat `SchemaHandle.admit_json` / `registered_schema_blob` as meta-schema equivalence. Do not add `x-opensip-stage-output` to `annotation()` as a substitute for 756.

## Feasible Rust ownership

Keep 2020-12 meta-check **out of identity TCB** (stage-20 API: evaluator owner). Identity stays parse/digest/tree/declaration joins and product dialect.

**Route (minimal, ordered):**

1. **Portable meta-check successor** (design/reference unit, reviewed, parented by identity-v3 2998–3023 + selected helper 756 + this probe table). Pin:
   - instance-validate against Draft 2020-12 **meta-schema** bytes (bundled; no retrieve);
   - closed format set **exactly** `{date, email, idn-email, ipv4, ipv6, regex, uuid}` and **explicit absence** of `uri` / `uri-reference` / hostname / datetime / duration / json-pointer;
   - `format: regex` = **Python 3.12 `re.compile`** (named groups and lookbehind accept; unclosed `(` refuse);
   - unknown keywords accept; nested bool schemas accept; producer `$ref` strings are not fetched;
   - does **not** require `$schema` URL (helper 754–755 stays in the stage owner).
2. **Stage-output implementation unit** (evaluator `admit_stage_output_schema`): retained stage-spec + producer closure + blob; 729–733 path segment; tree membership; digest of **exact retained bytes** (pretty lawful if registered); `C.parse` equivalent; **754–755 dict + exact `$schema` URL**; then the successor from (1); then declaration `equal_typed`. Caller still does 1788–1793 and **provider kind** (`payload` / `admit_closure_field_kinds`), not `identity_record_shape` alone (correction 3). No caller ADMIT. Live Walker 784–785 stays `Unsupported` until `OwnerJoin` wires **this** fn.
3. Probe table in (1) is the acceptance gate for any Rust crate. Off-the-shelf `jsonschema` crates using Rust `regex` are **not** 756 until a successor proves pair-equality, including Python-`re` `format: regex`. Adding rfc3987-class crates is a **law change**, not a dependency convenience.

Do **not** implement a “safe subset” of 2020-12 (drop `format`, require canonical bytes, require local `$ref` only, or only TABLE patterns). That is a new law, not a translation.

## Scope limits

Not instance-validation of stage outputs, replay, cache-as-owner, native H-frames, predicates-23, runtime-11, walk glue, or product qualification. Not a pin of jsonschema 4.25.1 into identity Cargo. Pretty JSON remains correction 1. Duplicate tree paths remain correction 2 (identifier/`ordered`).

## Verdict

**NOT ACCEPTANCE.** Design does **not** already pin the meta-schema/format dialect. Selected 756 is ambient jsonschema 4.25.1 + import-time optional formats. Rust stage-output ownership needs an **explicit reviewed portable `check_schema` successor**, then the evaluator owner from stage-20 as corrected. Identity `schema.rs` is not that successor.
