I’ll write the three isolated draft files from the v2 law plus these root decisions, then run schema/meta checks only under the helper tree. First I’ll pull the frozen FieldFilter, engine-family, and analysis-spec shapes so the drafts join the existing registries.I’ll write the three draft artifacts next: target-attribution schema, projection registry, and atom-evaluation contract.Draft files are in the isolated successor tree only. Frozen/live sources were not edited. G3–G5 are **not closed**.

## Written

| File | SHA-256 | bytes |
|---|---|---|
| `evaluator-successor.v1/docs/coop/design-corrections/foundation/evaluator-projection-registry.v1.json` | `ceec03df06f98edccb2364b5319482951b0bc53f63eea30f123aace1c32ba325` | 48334 |
| `evaluator-successor.v1/docs/coop/design-corrections/foundation/target-attribution.schema.v1.json` | `632b41fffd57a78954e13ef818979f97bc080cb2397d9797bb824872e1d35bb1` | 9035 |
| `evaluator-successor.v1/docs/coop/design-corrections/foundation/atom-evaluation-contract.v1.md` | `21fee3673dc96081646b4bfd6a18f70f7ef857938c3ae8c0e424819c0e0e75fb` | 15651 |

Helpers (not normative):

| File | SHA-256 |
|---|---|
| `grok-atom-contract.v3/check-atom-drafts.py` | `d0b528b802352c512f95537b73d9dd05ddfa42e1fbc8445af1fc878e668bcc16` |
| `grok-atom-contract.v3/check-atom-drafts.report.json` | `5e122d4693ba9aef462e4530e1f380425eea1bbe63eed3f0e13e3ebd672561e5` |

## Checks

`/tmp/opensip-architecture-review-env/bin/python -I -B grok-atom-contract.v3/check-atom-drafts.py` → **ok**. Draft 2020-12 metaschema on both JSON documents; 13 native + 4 imported relations each have all 10 filter slots; imports target kinds `file|symbol|package` with source kind still `symbol`; export is not a kind token; repair producers stay `runtime-observation`/`history-change`; TargetAttributionV1 admits first-party file/symbol and external package, refuses `kind=export`, first-party `logicalPath`, and `exported` on file; FieldFilterSuccessorV1 admits integer `exitStatus in` and string `subject in`, refuses the swapped array types and `confidenceMillionths eq`; ObservationAddress `test-execution` requires `ordinal=null`. Frozen `canonical.py` typed-admitted one attribution example (`C` digest `5ba9b196…1c64`). **Not Run replay.**

## Root decisions encoded

- Sidecar INPUT `TargetAttributionV1`; no native payload field; fact has no backlink; native-id compare before kind; metadata absence is unknown, not false.
- Kind filters `file|symbol|package` only. Export remains `subjectEnumeration.subjectKind=export`.
- Owed sources from **all** EnumerationPlan bindings for the atom’s capability; unavailable binding is an unknown obligation; incoming same-family sources including zero facts; outgoing does not invent empty target-universe keys; `ATOM_CROSS_FAMILY_EDGE_NOT_OWED` labeled; existing cross-program facts still match.
- Known hit ⇒ `none` false / count>N ⇒ `count-at-most` false despite partial siblings. Negatives require every **Plan-selected** relevant wrapper, not only `evaluationInputRefs`.
- Test process result from actual `TestPayloadV1` fields only; coarse `test-execution`; `tests=[]`+`exitStatus=1` is failed scope; `test-result` only with `subjectPath`.
- Inline `ObservationAddressV1`; no `import-observation-row` root; boolean empty matches; cause **set**; optional unknown stays indeterminate + non-gating disclosure.
- Runtime order kept (path, absent-symbol-before-present, symbol), not whole-row canonical-set.

## Remaining (root)

ProofInputRef/`byDomain` for `target-attribution`; FieldFilter/`Atom.endpoint` into `policy-document`; evidence-relation-registry growth vs repair producer subset; `canonical.py` comparator token; public-detail/D9 for every NEW/internal key; proof-bundle discriminator; G6 grouping; disabled-rule G6. No source assent.
