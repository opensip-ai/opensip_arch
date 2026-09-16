# Follow-up: schema-description override vs current admitted identity-v3 (311c)

**Reviewer:** Grok. Root remains lead. Not Claude agreement.  
**Kind:** Independent packaging assessment after original 04bf reference review. Original `review.md` / `review.json` and the 04bf subject are **unchanged**. Not a silent inheritance claim. Not schema regeneration. Not runtime acceptance.

**Original unit (preserved):** subject `docs/implementation/m2/predicate-matching-reference-selection-v1-subject.json` 1842 / `04bf748e2796592f2691a5eff76bfd59e0828de192fcaae67b6ff2e1ce6ac463`. Successor 5363 / `006c225d8fa17b3fd9cf4bd71b4e55b45cb5162a642c71986a91b22f99ae1fc6`. This tree’s `review.md` 7588 / `5997c7b1…147d`; `review.json` 8566 / `2591412c…268d`; verdict `ACCEPT-DESIGN-UNIT` as packaged.

## Question

The original successor’s schema-description passage override targets historical `docs/coop/design-corrections/foundation/identity-schemas.v3.json` **196987** / `a76c9e2f07e8f8e52ee611f157548f6a09061866308652e3a0f7e3c24893db21`. Should the same ASCII-ordinal clarification **also** or **instead** target current admitted `docs/implementation/m1/source-selection-v2/schemas/sources/identity.v3.schema.json` **197480** / `311c1feb09ff8cd0b207233d2ec0d7440bb1c72fc0470de277ee1891c24bb68f`?

## What is actually admitted

`source-selection-v2` `current-dispatch.json` / `source-map.json` / `generation-source-map.json` bind `urn:opensip:product-v1:identity:v3` to **311c**, not a76c. Recognition-derived `evidence/check-derived.py` loads that same 311c path. Live `schemas/sources/identity-v3.schema.json` is byte-identical to 311c. Observed live lock: **17** inventory / **22** contract, last contract `native-runtime-selection-v9`; predicate-matching is **not** a contract successor.

a76c and 311c share `$id` `urn:opensip:product-v1:identity:v3` but are **different files**. Independent structural walk: one extra key only in 311c, `x-opensip-payload-registry/classes/parameter/rows/foundation/framework-recognition-plan.schema.v1.json`. `program-predicate` (including `predicateId` `$ref: Text` 1–4096, no digit pattern) is object-equal. That equality is not an alias and does not move a pin-addressed passage override.

## Description text today

Both files still say “zero-based, shortest decimal” at `/$defs/program-predicate/description`. That string is exactly the original override `before`. Neither file contains “ASCII decimal”. Live 311c is the same.

Product prose line 1272 is already an explicit override on `identity-and-evidence.md` `c82404f3…d31f`. That does **not** rewrite 311c (or a76c) schema description. No silent inheritance from prose or from a76c to 311c.

Original successor parents include source-selection-v2 successor **and** a76c, but **not** the 311c schema file, and no override parent is 311c.

## Disposition: ALSO, not INSTEAD

The semantic clarification should **also** target current 311c as a **description-only selected passage override**. Physical 311c bytes stay unchanged. No full schema regeneration.

Same selector and strings apply because the descriptions currently match:

- parent pin: `docs/implementation/m1/source-selection-v2/schemas/sources/identity.v3.schema.json` 197480 / `311c1feb09ff8cd0b207233d2ec0d7440bb1c72fc0470de277ee1891c24bb68f`
- `jsonPointer`: `/$defs/program-predicate/description`
- `before`: existing “shortest decimal” sentence (identical to the a76c `before`)
- `after`: existing a76c `after` (“shortest ASCII decimal 0 or [1-9][0-9]*; non-ASCII digits are refused, never normalized”)

**Not INSTEAD**, unless root re-parents the unit off a76c. The a76c override remains a valid pin-local clarification of the historical foundation document the original successor actually listed. Dropping it while leaving a76c as a parent would un-clarify that parent. Adding 311c as parent + override closes the admitted-schema gap.

Root may author a corrected successor/manifest. This follow-up does not edit frozen bytes, the 04bf subject, or the original review.

## Limits

Not a reopen of glob/ordinal helper review. Not Rust/runtime. Not a live overlay of this still-unselected reference unit. Helper law and identity recipes are unchanged by this packaging note.
