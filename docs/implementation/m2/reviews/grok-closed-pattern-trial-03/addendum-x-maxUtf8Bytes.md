# Trial03 addendum: `x-maxUtf8Bytes` is not generic selected shape

**Standing:** Same advisory as trial03. **NOT ACCEPT-DESIGN-UNIT.** Does not change the closed-matcher verdict. Does not authorize folding this annotation into ExactValidator or a Rust shape evaluator.

## Flag

The selected profile does **not** explicitly mandate `x-maxUtf8Bytes` as a generic shape-validation keyword.

Porting `tools/contracts/runtime/schema.ts` byte checks into host/evaluator shape would **silently tighten** admission relative to selected `canonical.py` `ExactValidator` + jsonschema 4.25.1 Draft 2020-12. Keep the annotation as a distinct extra admission law, with an owner, until a profile unit adds it the way `x-opensip-order` was added.

## Selected reference shape

`docs/coop/design-corrections/foundation/canonical.py` SHA `d47f25db0fb09ceb84282a89fdf74055cb81ccb9de26f85a5a70b032b9a6b442` / 6465.

`ExactValidator = validators.extend(Draft202012Validator, validators={const, enum, x-opensip-order}, type_checker integer is Python int)`.

Independent check: extra keyword vs Draft 2020-12 is only `x-opensip-order`. `x-maxUtf8Bytes` is **not** in `VALIDATORS`. A string of 6 UTF-8 bytes under `"x-maxUtf8Bytes": 4` is **admitted** by both Draft 2020-12 and `canonical.validate`. Unknown Draft keywords do not fail.

`identity-and-evidence.md` names `x-opensip-order` as the machine-readable validator keyword implemented in `canonical.py`, including refuse-unknown-vocabulary. No v2 contract text names `x-maxUtf8Bytes` as a shape keyword.

## Occurrences

Among the 40 selected registry sources: **21** annotations, **all** in `schemas/sources/control-v3.schema.json` (`urn:opensip:design:control-schema:3`, profile `opensip-exact-schema-reference-1`). None in identity-v3 or other selected sources.

Registry `semanticValidatorOwner` is `crates/components/src/control_protocol.rs`. That file is **not** in the live product. No live `.rs` / `.py` matcher implements the annotation. Control-generation unit (M1, carriers + TS shape only) already noted a **separate** UTF-8 extension besides jsonschema, and that four of 21 sites are dominated by `pattern` / `maxLength` (not boundary-informative).

## Trial TS is not selected shape

`tools/contracts/runtime/schema.ts` line 1: “Trial interpreter for the selected schema vocabulary. Shape is not semantic authority.” It lists `x-maxUtf8Bytes` in `known` / `counts` and refuses strings whose UTF-8 byte length exceeds the annotation. That is trial shape, including the accepted control-generation **carrier/TS** unit, not `ExactValidator`.

## Relation to trial03 resource model

Same three-way split: pattern/shape false ≠ unknown keyword ≠ owner/resource law. Folding `x-maxUtf8Bytes` into generic shape would invent a cap the selected validator does not apply, including on control strings already bounded by UUID/hex `pattern`. Do not do that by copying the TS trial.
