# Follow-up: Format-Annotation 7.2.1 phrasing (opt-in assertions)

**Reviewer:** Grok. Root remains lead. Not Claude agreement.  
**Kind:** Bounded standards-precision correction of followup-portable-choice wording. Original advisory24 and portable-choice follow-up **unchanged**. **Not ACCEPT-DESIGN-UNIT. Not a review or acceptance of root’s private projection.** Option A remains the proposed explicit successor, not selected.

**Preserved pins:** advisory.md 8781 / `0459cd3e…e430`; advisory.json 3696 / `d9c104e0…a70b`; followup-portable-choice.md 7654 / `6311493c…641a`; followup-portable-choice.json 2985 / `e43cbf98…ee81`.

## Spec (independently read)

[JSON Schema Validation 2020-12 §7.2.1](https://json-schema.org/draft/2020-12/json-schema-validation#name-format-annotation-vocabular) (Format-Annotation vocabulary):

- `format` MUST be collected as an annotation if the implementation supports annotation collection.
- Implementations **MAY** still treat `format` as an **assertion** in addition to an annotation.
- They **MUST** provide options to enable and disable that evaluation, and it **MUST be disabled by default**.
- Enabling annotation-vocab format checks is **not** equivalent to declaring the Format-Assertion vocabulary (7.2.1 last sentence). Format-Assertion (7.2.2) is the stronger, optional vocabulary.

So: default-off is required; **opt-in is permitted**. Phrases in portable-choice that `format` “MUST NOT fail” under Format-Annotation, or that option B is inherently “against vocabulary,” **overstate**. jsonschema 4.25.1 `check_schema` defaulting `FORMAT_CHECKER` on is an **implementation choosing to enable** (and its `check_schema` default is on, which is the library’s default, not a proof that every explicit library check always violates the spec). Option A `format_checker=None` is a **deliberate portable profile** matching the spec’s **default-off**, not a claim that 756 is always illegal.

Option B (ECMA-262 regex assertion at stage admission) remains **not recommended** for the stage owner (regex product in registration; still not Format-Assertion vocab). That is an architecture/profile choice. Under 7.2.1 it would be a permitted **opt-in**, not a vocabulary contradiction.

## Two fixed meta-schema `pattern` keywords (Python `$`)

These are **validation-vocab `pattern`**, not `format: regex`. They still apply under `format_checker=None`. jsonschema implements `pattern` with `re.search`. Python `$` matches end-of-string **or before a trailing LF**, not before CR.

Independently probed (`probes/meta_pattern_dollar.py`):

| Instance | `$anchor` `^[A-Za-z_][-A-Za-z0-9._]*$` | `$id` `^[^#]*#?$` |
| --- | --- | --- |
| `a` | ADMIT | ADMIT |
| `a\n` | **ADMIT** (`re.search`; `fullmatch` would refuse) | — |
| `a\r` | refuse | — |
| `a#\n` | — | **ADMIT** |
| `a#\r` / `a#foo` | — | refuse |

Same under default FORMAT_CHECKER and `format_checker=None`. A successor or Rust checker that uses `fullmatch`, “end of string only,” or ECMA `$` without this LF exception would **silently tighten** (`a\n` / `a#\n` newly refused). Finite explicit predicates for these two ASCII patterns **must preserve** this compatibility. That does **not** require a generic Python regex engine.

## Root projection (not reviewed as a unit)

Root reports a private finite projection (`/tmp/opensip-implementation/m2-stage-meta-exploration-24`, standing EXPLORATORY NOTSELECTED): **6332** integer-only cases, **0** mismatch vs `check_schema(..., format_checker=None)`, **15** intentional ambient-vs-annotation changes (invalid `pattern` / `patternProperties` keys). This follow-up **does not** accept that projection or treat it as a complete unit. It only notes the count as context that option A’s named delta is the format-regex assertions going quiet.

## Verdict

Portable-choice recommendation **A stands**, with this phrasing correction. `format_checker=None` is the spec default-off profile, explicitly successor-not-yet-selected. Do not describe 756 as always spec-illegal, and do not describe opt-in format assertion as vocabulary-forbidden. Preserve the two `$` pattern outcomes so a later checker does not tighten them.
