# Exact schema profile selection v1 — scoped design-unit review

**Verdict: `ACCEPT-DESIGN-UNIT`**

Not runtime admission. Not M2 completion. Frozen/live/history not edited. This is the oracle dispatch successor proposed after the reference-semantics audit: keep the already selected exact const/enum/integer/order law across document-root `$ref`, without rewriting schema bytes or identity encoding.

Subject `docs/implementation/m2/exact-schema-profile-selection-v1-subject.json` SHA-256 `9d32384320d2816317df9316cad319c961316c0ba9daaf61a1ce57b6a8e4f79a` (1968 bytes, 9 files). Implementation subject SHA-256 `965be52560f975ce3e5eb0f6cabd4bb34f077ad1b602d5a44affacdb1fdefab9` (5 files). Archive SHA-256 `0ab7a3afdf597d40266c0ec02eedbc9bd86445b04a341d5caaf52fe781fbc215` matches the unit pin.

## Custody

Parents are sorted unique and pin-match:

1. original `foundation/canonical.py` `d47f25db…f442` (6465 bytes) — **unchanged**
2. `combined-corrections-selection-v1/successor.json` `219a9277…b65e`

Candidates (8) are sorted unique and cover the subject minus the successor record. `passageOverrides: []`. New paths only. Combined unit is an accepted parent for packaging lineage, not a claim that this oracle is already live-selected.

## What the code does

New `reference/canonical.py` (8995 bytes, `ad88e58f…8496f7`) keeps parse/canonical/identity/typed/equal_typed/exact_const/exact_enum/exact_order **AST-identical** to the original (independently dumped). `validate` adds dialect preflight.

`ExactValidator` still extends Draft 2020-12 with those three keywords plus a `$schema` **keyword guard**. Wrong dialect raises `AdmissionError('UNREGISTERED_SCHEMA_DIALECT')`, not `ValidationError`. `is_valid` therefore does **not** return false; `not` / `anyOf` / `allOf` / `if` cannot invert a bad dialect into instance success (reproduced).

`evolve` no longer calls `validator_for`. It requires the declared 2020-12 dialect (or absent/`bool` schema), copies every **attrs init field by alias** (`schema`, `resolver`, `format_checker`, `registry`, `_resolver`), and constructs `self.__class__(**changes)`. Independently: evolved instance is still `ExactValidator`, `_registry` is the same object, wrapped `[1, true]` still refuses.

`exact_registry` clones via `parse(canonical(document))` so caller objects/bytes are not edited; requires dict `$id` without `#`, unique IDs, declared dialect; stores `Resource(contents without $schema, specification=DRAFT202012)`; `Registry()` has no retriever. Missing `$ref` is `_WrappedReferencingError`, not a fetch. All **40** current product schemas load (no `#` in `$id`, dialect present); retrieved occupancy contents omit `$schema`; inputs still have `$schema`.

Full `Resource.from_contents(original doc)` callers are also fixed by the evolve guard. The helper strip is compatibility with the existing metadata-v2 adapter, not a second profile.

`validators.validator_for({$schema: 2020-12})` remains stock `Draft202012Validator` — no global `_META_SCHEMAS` mutation.

`x-maxUtf8Bytes` still ignored (`😀` admitted under limit 1). Identity golden `identity('vector', None)` still `ae2a3ea9…c26c`.

Predecessor wrapped `$ref` still **admits** `[1, true]` — retained as negative evidence, not relabelled pass.

## Independent tests

Retargeted `check-profile.py` off `/tmp/.../m2-exact-profile-candidate-01` and `A.parent/opensip` onto this private subject plus combined product schemas: **87/87**. Extra probes: 40-schema registry, dialect faults through combinators, closed missing ref, evolve registry identity, global dispatch unchanged.

## requiredFindings

None.

## shouldFix

`evidence/check-profile.py` hardcodes the original candidate path and `opensip` checkout for raw schema pins. Reviewers must retarget. Not an oracle-law miss.

## Scope and limits

This unit is the **selected proposed M2 oracle** after assent. Older frozen Python models still import original `canonical.py` until separately composed. Did not re-run 486986 trial cases or full envelope instances on the 15 product root-ref edges (the synthetic wrapped/nested/fragment matrix plus 40-schema load covers the declared law). jsonschema 4.25.1 only. No product schema/digest/public-profile change. No full M2 or M6.
