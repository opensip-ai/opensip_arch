# Follow-up: portable `check_schema` choice (not Python `re` as product law)

**Reviewer:** Grok. Root remains lead. Not Claude agreement.  
**Kind:** Architecture judgment after root challenge of advisory24’s recommended Python 3.12 `re.compile` pin. Original `advisory.md` / `advisory.json` **unchanged**. **Not ACCEPT-DESIGN-UNIT. Not implementation. Not a silent law change.**

**Original pins:** `advisory.md` 8781 / `0459cd3e…e430`; `advisory.json` 3696 / `d9c104e0…a70b`.  
**Probes:** `probes/meta_schema_format_graph.py` against bundled `jsonschema_specifications` 2025.9.1 Draft 2020-12 resources and `Draft202012Validator.check_schema` with default FORMAT_CHECKER vs `format_checker=None`.

## Reachable formats (root suspicion confirmed)

`check_schema` instance-validates the producer document against `https://json-schema.org/draft/2020-12/schema`. Walking that resource plus every 2020-12 `meta/*` document it `allOf`s, the **only** `"format"` names in the graph are:

| format | where | applied to producer field |
| --- | --- | --- |
| `regex` | `meta/validation` `properties/pattern` | `pattern` **value** |
| `regex` | `meta/applicator` `properties/patternProperties/propertyNames` | `patternProperties` **keys** |
| `uri` | `meta/core` `$defs/uriString` | `$schema`; `$vocabulary` property names |
| `uri-reference` | `meta/core` `$defs/uriReferenceString` | `$id`, `$ref`, `$dynamicRef` |

**Not in the graph:** `date`, `email`, `idn-email`, `ipv4`, `ipv6`, `uuid`. Those seven ambient checkers from advisory24 are **irrelevant** to `check_schema` except `regex`. A producer `"format": "email"` is only a string under format-annotation (`type: string`); the format **name** is not enumerated.

Default meta-schema `$vocabulary` includes **format-annotation: true** and does **not** include **format-assertion**. JSON Schema 2020-12: annotation format MUST NOT fail validation. jsonschema 4.25.1 still asserts `format` when `format_checker` is set (`_keywords.format`). Selected env has `uri` / `uri-reference` **unregistered**, so only **`regex` actually fires**. That is why `"pattern": "("` is `DOCUMENT_INVALID` today and `$id: "not a uri"` is not.

`$id` fragment rule `^[^#]*#?$` is a meta-schema **`pattern` keyword**, not `format`. It still fails under `format_checker=None` (`https://example.invalid/x#foo`). That pattern is ASCII; it does not require a Python regex product.

## Does 756 certify an executable schema?

**No.** Selected 735–761 returns the parsed document. Correction (4): schema-as-instance of the 2020-12 meta-schema; not instance-validation of stage outputs; not `$ref` fetch. Identity-v3 `registeredBy` names tree path, declaration, and refusal codes — not an evaluation engine.

The Python-`re` compile of `pattern` / `patternProperties` keys is an **accidental assertion** (library default FORMAT_CHECKER + the one reachable registered format). It is not a declared “this schema is executable in our engine” obligation. Pinning Python 3.12 `re.compile` would freeze that accident, including Unicode/version/`re` parser semantics, into Rust. That is the wrong product law.

JSON Schema Validation’s `format: regex` is **ECMA-262**, not Python `re`. The selected helper is already spec-divergent on that point. Faithful accident translation is not spec fidelity.

## Options (none is silent 756)

**A. Bundled 2020-12 meta-schema + `format_checker=None` (format-annotation)**  
Instance-validate against the default meta-schema graph (core, applicator, unevaluated, validation, meta-data, format-annotation, content). Do not apply format assertions. Keep helper 754–755 (dict + exact `$schema` URL), `C.parse` (pretty lawful), unknown keywords, nested bools, no retrieve.

Named delta vs selected 756 (must be an **explicit successor**, not a silent patch):

| Producer document | 756 today | A |
| --- | --- | --- |
| `"pattern": "("` | `DOCUMENT_INVALID` | **ADMIT** shape |
| `patternProperties` key `"("` | `DOCUMENT_INVALID` | **ADMIT** shape |
| `"(?P<name>.)"` / lookbehind | ADMIT (Python `re`) | ADMIT (format not asserted) |
| `$id` extra fragment | `DOCUMENT_INVALID` (`pattern` keyword) | same |
| `$id` / `$ref` non-URI | ADMIT (`uri-reference` unregistered) | ADMIT |
| `"format": "email"` / unknown keywords / remote `$ref` / nested bool / pretty | ADMIT | ADMIT |
| date/email/ipv4/uuid checkers | never reached | never reached |

Later **output-instance / execution owner** (not this stage owner) must **declare** regex compilation: compiling `pattern` values and `patternProperties` keys with a **pinned** dialect (JSON Schema’s `format: regex` is ECMA-262; that pin belongs there). Invalid pattern accepted by shape, rejected by execution-owner — stated, not hidden.

**B. ECMA-262 as `format: regex` assertion at stage admission**  
More like 756’s *timing* (refuse uncompilable patterns now) and closer to Validation spec *text* for format:regex, but **against** default `$vocabulary` format-annotation. Requires an ECMA-262 engine in the stage owner. Delta vs 756: Python named groups currently ADMIT, ECMA would refuse. Still freezes a regex product into registration.

**C. Closed producer schema profile** (selected keywords only, identity-like)  
Would refuse `format`, `exclusiveMaximum`, `multipleOf`, `unevaluatedProperties`, `$comment`, `type: number`, unresolved `$ref`, `x-opensip-stage-output` unless added. That is a **new dialect**, not 756 and not 2020-12. Largest narrowing. Only if OpenSIP explicitly wants producer interfaces on the **product** dialect — that is a separate law, not a translation of 756.

Do not mix A/B/C silently. Do not claim A ≡ 756.

## Recommendation

**A**, as an explicit reviewed successor, parented by identity-v3 2998–3023 + selected 756 + this probe graph.

**Correctness:** Matches the bundled default meta-schema and format-annotation vocabulary. Does not invent Python `re` as a Rust TCB. `uri`/`uri-reference` stay annotations (spec-correct for this meta-schema; also matches today’s unregistered formats). Stage owner certifies **document shape + registration + declaration**, which is what 735–761 and correction (4) actually describe.

**Extension:** Producers may use `format` as annotation without the stage owner growing format libraries. Instance-validation can later opt into format-assertion or a pinned regex dialect without re-opening registration.

**Trust:** A registered schema may contain a `pattern` that will not compile. That is the honest split: registration is not execution. The execution owner already needs a regex engine to evaluate instances; putting compilation there avoids a second, accidental engine at admission. The successor **must** name the delta (`pattern: "("` moves from `DOCUMENT_INVALID` to later execution refusal) so consumers are not surprised.

**Not B** as the stage-owner default: it still treats format as assertion under a format-annotation meta-schema, and it still embeds a regex product at registration. **Not C** unless a later unit explicitly selects a closed producer profile (new law).

Evaluator still owns the meta-check (identity TCB unchanged). Live Walker cut stays Unsupported until the stage owner is wired. No product/native code in this follow-up.

## Verdict

Original advisory24 preserved. Portable pin of Python 3.12 `re.compile` **withdrawn** as the recommended product law. Recommended successor: **bundled 2020-12 meta-schema instance validation with format annotations not asserted**, plus a **separately declared** regex compilation obligation on the output-instance owner. That is a named successor, not equivalence with 756.
