# Independent Grok advisory: relation payload row/rung boundary

**Reviewer:** Grok (explicitly authorized). Root remains lead. Not Claude agreement.
**Kind:** Bounded next-owner test-vector advisory for graph05 relation `registered_payload`. **Not runtime selection. Not M2 complete. Not native ADMIT. Not ReplayedRun.**
**Work tree:** `/tmp/opensip-implementation/m2-grok-relation-payload-boundary-01/review`. Live product, frozen trials, architecture history, and commits were not edited.
**Prior:** records04 advisory archived. Recognition-derived identity model is the live-selected reference (lock **9/14**), not a pending proposal.

## Standing

Root is implementing parameter/coverage `registered_payload` privately. Next owner slice is **relation** payload row/rung checks. Passing those checks is **not** complete native evidence: `relation_payload_rules` still calls syntax capability and snapshot/body-identity joins, and `admitted-target` is not decided in that function at all.

## Pins (independent)

Live lock: **9 inventory / 14 contract**. Last contract `docs/implementation/m2/recognition-derived-reference-selection-v1/successor.json` `4b771e6e…4711`, Grok review `8aa13c04…603e`, assent `5c84dad9…e54f`.

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| selected `identity_model.py` | 158555 | `619d6e3c…41e6` |
| accepted exact-profile `canonical.py` | 8995 | `ad88e58f…96f7` |
| current `relation-payload-v2.schema.json` | 57623 | `53380a24…be9a` |
| current `identity-v3.schema.json` | 197480 | `311c1feb…b68f` |

Private overlay places those exact bytes at `review/overlay/docs/coop/design-corrections/foundation/` so `HERE.parent` matches `validate_registered_record`’s `foundation/…` keys. Remaining local-registry foundation documents are current live admission sources (or the existing current overlay for identity-v2 / target-attribution-v1). No untrusted registry.

Identity payload-registry class `relation`: keyed by `fact.relation`; document `foundation/relation-payload-schemas.v2.json`; `payloadSchemaDigest` is SHA of **this full file** (`53380a24…`).

## Actual reference functions

`registry_row` (inside `open_run_closure`): if `payload_class=='relation'` and the name is not in `RELATIONS` → `PAYLOAD_RELATION_UNREGISTERED`; else `relation_annotation_closure(name)` and return `{document, selector, relation}`.

`relation_annotation_closure` is a **pure schema** function: digest-law coverage, retention, residue, join-field existence. Independently: all **13** names close on the current document. Unknown name is not in `RELATIONS` (`PAYLOAD_RELATION_UNREGISTERED`); calling the closure is `KeyError:'not-a-relation'`.

`relation_payload_rules(value, row, fact)` order:

1. `ladder` membership (never `rungs` as the ladder)
2. `anchor_law` (registry cardinality)
3. **`syntax_capability_supported`** — native owner
4. per-rung required/forbidden fields
5. `universeRule == same-only` → sourceUniverse == targetUniverse
6. NFC / no negative integers
7. **`relation_source_joins`** — snapshot inventory, retained bytes, then **`body_identity_join`** for clones

`universeRule: admitted-target` is published on `calls`, `imports`, `references` and is **not implemented** in `relation_payload_rules`. That is a later native/universe join, not a silent same-only.

## 13 closed rows

| Relation | Selector | Ladder (weakest first) | Rung field rules | universeRule | Anchors | Later owner joins |
| --- | --- | --- | --- | --- | --- | --- |
| calls | `#/$defs/CallsPayloadV1` | syntactic-callee-name, resolved-callee | weak forbids `resolvedCallee`; strong requires it | **admitted-target** | source-text ≥1 | syntax capability; admitted-target |
| clones | `#/$defs/ClonesPayloadV1` | normalized-body-hash | empty `rungs` | same-only | body-identity =1 | syntax capability; **bodyIdentityJoin** |
| control-flow | `#/$defs/ControlFlowPayloadV1` | syntactic | empty | same-only | source-text ≥1 | syntax capability |
| declares | `#/$defs/DeclaresPayloadV1` | syntactic | empty | same-only | source-text ≥1 | syntax capability |
| file | `#/$defs/FilePayloadV1` | enumerated | empty | same-only | inventory =0 | syntax (no-op if not syntax universe); **inventoried-file** snapshot/blob; **coverageTotality** at complete Coverage |
| imports | `#/$defs/ImportsPayloadV1` | syntactic-specifier, resolved-target | weak forbids `resolvedTarget`; strong requires it | **admitted-target** | source-text ≥1 | syntax; admitted-target |
| literal | `#/$defs/LiteralPayloadV1` | syntactic | empty | same-only | source-text ≥1 | syntax |
| package | `#/$defs/PackagePayloadV1` | manifest-declared | empty | same-only | inventory =0 | **inventoried-path** `manifestPath` |
| reachability | `#/$defs/ReachabilityPayloadV1` | from-resolved-calls | empty | same-only | source-text ≥1 | syntax |
| references | `#/$defs/ReferencesPayloadV1` | syntactic-name-match, resolved-binding | weak forbids `resolvedBinding`; strong requires it | **admitted-target** | source-text ≥1 | syntax; admitted-target |
| types | `#/$defs/TypesPayloadV1` | annotated, checked | weak forbids `checkedType`; strong requires it | same-only | source-text ≥1 | syntax |
| unresolved-edge | `#/$defs/UnresolvedEdgePayloadV1` | observed | empty required/forbidden | same-only | source-text ≥1 | syntax |
| vcs-change | `#/$defs/VcsChangePayloadV1` | vcs-reported | empty | same-only | inventory =0 | **inventoried-path** unless `changeKind==deleted` |

**Pure (this vector suite executes):** annotation closure, selector ExactValidator on current relation bytes, ladder, `anchor_law`, rung fields, `same-only`, NFC/non-negative.

**Owner remaining (not executed as pass):** `syntax_capability_supported`, `relation_source_joins`, `body_identity_join`, admitted-target universe, coverage totality/dialect/source-variant, native frames, replay.

## Reproduction

```
/tmp/opensip-implementation/metadata-reference-env/bin/python -I -B \
  /tmp/opensip-implementation/m2-grok-relation-payload-boundary-01/review/probes/run_vectors.py
```

Results: `review/results/vectors.json`.

The runner loads the selected model from the overlay, calls **actual** `relation_annotation_closure` and `validate_registered_record`, and runs **AST-extracted** `anchor_law` plus `relation_payload_rules` with only the two owner call-statements removed (`syntax_capability_supported`, `relation_source_joins`). That is not a fabricated ADMIT of those joins; they are classified remaining.

| Class | Count | Result |
| --- | ---: | --- |
| Positive pure (every closed rung + deleted vcs) | 18 | **18/18 ok** |
| Negative pure | 9 | **9/9 refuse** |
| Limit: admitted-target mismatch | 1 | **ok** (pure layer does not check it) |

All **17** closed rungs of all **13** relations have a schema-valid payload that passes the pure rules with lawful anchors and matching universes.

Negatives (actual refusal strings):

- `declares@resolved-callee` → `RELATION_RUNG_NOT_IN_LADDER` (foreign `calls` rung)
- `calls@syntactic-callee-name` + `resolvedCallee` → `RELATION_RUNG_FORBIDDEN_FIELD`
- `calls@resolved-callee` without `resolvedCallee` → `RELATION_RUNG_REQUIRED_FIELD` (schema still accepts: field is optional)
- `file` source≠target → `RELATION_UNIVERSE_RULE:same-only`
- `file` with an anchor → `FACT_ANCHOR_CARDINALITY:file:inventory:expected=0`
- `declares` zero anchors → `FACT_ANCHOR_CARDINALITY:…minimum=1`
- `clones` zero anchors → `FACT_ANCHOR_CARDINALITY:…expected=1`
- combining-acute `sym:é` → `RELATION_PAYLOAD_NOT_NFC` (schema allowed; payload scan refused)
- `byteLength: -1` → schema `REGISTERED_RECORD:#/$defs/FilePayloadV1` (UInt64 before scan)

`imports` with source≠target **passes** pure rules: `admitted-target` is not this function. Do not treat that as native target admission.

## Findings

**Required:** none for this bounded vector task.

**Owner implementation notes (not this review’s acceptance):**

1. Graph05 relation `registered_payload` should run ladder/rungs/`same-only`/NFC/anchor_law against the **closed row** from `relation_annotation_closure`, selector from that row, digest `53380a24…`.
2. Do not read empty `rungs` as an absent ladder.
3. Do not implement admitted-target, snapshot joins, clones body-identity, or syntax capability inside the pure payload helper and then call it native evidence.
4. `file@enumerated` coverage totality is a Coverage/view obligation, not a payload-shape vector.

## Limits

- Advisory. Not acceptance of graph05, native evidence, A04/A05, or M2.
- Did not execute `syntax_capability_supported`, `relation_source_joins`, `body_identity_join`, `open_run_closure`, or compiler/native qualification.
- Did not construct a ReplayedRun or a trusted native universe map.
- Overlay copies extra foundation documents only so `validate_registered_record` can build its pinned local registry; relation authority is the current relation file SHA.
- Root continues code and tests independently.

**Verdict: NOT ACCEPTANCE.** Thirteen-row pure vectors are executable and reproducible. They bound the next relation `registered_payload` helper. They are not complete native evidence.
