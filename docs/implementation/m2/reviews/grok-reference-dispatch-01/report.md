# Advisory: ExactValidator dialect switch on retrieved `$schema`

Not an acceptance. Not M2 completion. Frozen/live/design records were not modified. Work stayed under `/tmp/opensip-implementation/m2-grok-reference-dispatch-review-01/review`.

Selected oracle `docs/coop/design-corrections/foundation/canonical.py` SHA-256 `d47f25db0fb09ceb84282a89fdf74055cb81ccb9de26f85a5a70b032b9a6b442` (6465 bytes) matches the lock pin. Trial `/tmp/opensip-implementation/m2-schema-engine-trial-01` has 75 files excluding Cargo `target`; its 40 schema pins match current product `schemas/sources/*` and `schemas/source-map.json`.

## Diagnosis

`ExactValidator` is `validators.extend(Draft202012Validator, {const, enum, x-opensip-order}, integer := type is int)`. jsonschema **4.25.1** `Validator.evolve` does:

```python
NewValidator = validator_for(schema, default=self.__class__)
```

`validator_for` returns stock `Draft202012Validator` when the retrieved document has `"$schema": "https://json-schema.org/draft/2020-12/schema"`. All 40 selected sources have that keyword. Custom exact-const/enum/integer-type and **`x-opensip-order` are dropped**. Stock treats `x-opensip-order` as an unknown annotation and ignores it.

Independently reproduced (Python 3.14 metadata-reference-env, jsonschema 4.25.1):

| Entry | `[1, true]` / `[2, 1]` with `x-opensip-order: numeric` |
|---|---|
| `ExactValidator(schema)` | **reject** (`integer order required` / `strict unique order required`) |
| `ExactValidator({$ref:'urn:probe#'}, registry)` | **admit** |
| nested `{$ref:urn:mid#}` → mid `$ref` probe (both documents have `$schema`) | **admit** |
| `ExactValidator({$ref:'urn:doc#/$defs/nums'})` (defs node has no `$schema`) | **reject** (custom class kept) |
| stock `Draft202012Validator(schema)` | **admit** |
| Resource contents **omit `$schema`**, `specification=DRAFT202012` | wrapped and nested **reject** again |

So: this is not a Rust/Python instance-codec disagreement on a generated fixture. It is an **oracle profile** hole on **document-root `$ref`**. Fragment `$ref` into `$defs` currently keeps ExactValidator.

The trial itself built `Resource.from_contents(full_document)` and `ExactValidator({$ref: entry}, registry)` for 839 selected entries. **Document-root entries therefore ran stock jsonschema.** `$defs` entries did not. Corpus values such as `[1, true]` rarely hit `x-opensip-order` on object document roots, so 486986 cases / 0 mismatches did not surface it. Rust uses one interpreter: `$schema` is a dialect assertion (`probe/src/schema.rs`), not a class switch, so it still enforces order on both paths.

## Selected registry: 15 root-ref sites

Current product, all profile `opensip-exact-schema-reference-1`:

- 15 unique `(file, $ref)` **document-root** refs (no JSON pointer beyond the foreign `$id`)
- 1069 foreign **fragment** refs (`#/$defs/…`)
- 925 internal `#` refs
- 517 `x-opensip-order` sites
- 21 `x-maxUtf8Bytes` sites, **all** in `control-v3.schema.json`

The 15 root refs (the evolve hazards):

- `fact-batch-v3` → occupancy-companion
- `explicit-history-panel-v1` → explicit-history
- `envelope-v3` → invocation:3, baseline:2
- `envelope-v4` → invocation:3, metadata:1, baseline:2
- `command-envelope-v7` → invocation:5, metadata:1, baseline:2
- `report-v1` → command-envelope:7, explicit-history, comparison:2, explicit-history-panel, configuration-disclosure

Direct `$defs` entrypoints do **not** protect these. Validating envelope7 by `$ref` to its `$id` (or any of those 15 edges) evaluates the **target document** with stock jsonschema, so nested `x-opensip-order` on metadata `closureIds` (`utf8`) and similar is not applied.

## Root intent vs owners

**Exact const/enum/integer/order throughout a registered-profile ref closure: yes.**

- identity-and-evidence §3: `x-opensip-order` is the machine-readable keyword; vocabulary is exactly `canonical.py`; unknown annotations refuse; owning schema order is mandatory before hash.
- Every source-map row is `opensip-exact-schema-reference-1`.
- Selected metadata-v2 `check_metadata.py` already states that jsonschema 4.25.1 `evolve` loses ExactValidator unless `$schema` is omitted from Resource contents while keeping Draft 2020-12 as Resource specification. That adapter is a **local checker**, not the generic `canonical.validate()`.

**`x-maxUtf8Bytes` is not that profile keyword.** It is not in `ExactValidator`. Direct ExactValidator admits a 6-byte string under `x-maxUtf8Bytes: 4`. All 21 sites live on `control-v3.schema.json` with `semanticValidatorOwner` `crates/components/src/control_protocol.rs` (inventory/layout: control-frame codec, M3). Do not fold this into ExactValidator.

## Suggested correction (minimal, no frozen-schema rewrite)

Do **not** rewrite the 40 schema files or historical trial corpora. Treat this as a **canonical.py / registry-construction successor** (and the same law for any selected runtime interpreter).

1. **Oracle (required for a correct ExactValidator contract)**  
   - `exact_registry(documents)`: `Resource(contents={k:v without $schema}, specification=DRAFT202012)` — same pattern as metadata-v2.  
   - **Also** override `ExactValidator.evolve` so that when the retrieved schema’s `$schema` is draft/2020-12 (or absent), `validator_for` is not allowed to substitute stock `Draft202012Validator`; keep `self.__class__`. That closes `Resource.from_contents(full_doc)` callers (including the trial).  
   - Do **not** assign ExactValidator into jsonschema’s global `_META_SCHEMAS`.

2. **Runtime selection law**  
   Profile is chosen at the **entry** validator and applies to the **closed registry**. Retrieved `$schema` must equal the registered dialect or refuse; it must not switch implementation class. The Rust trial already matches this.

3. **Tests (new, small)**  
   - Direct numeric order: refuse `[1, true]`, `[2, 1]`; admit `[0, 1]`.  
   - Wrapped `{$ref: id}` with `$schema` on the stored document: same refusals **after** the fix.  
   - Nested mid→probe root refs: same.  
   - Fragment `id#/$defs/nums`: refuse before and after.  
   - `x-maxUtf8Bytes` still does not fail at ExactValidator.  
   - Pinned schema **files** still contain `$schema`.

4. **Not required**  
   Changing identity-schemas or product `$id`s; implementing `x-maxUtf8Bytes` in the generic engine; claiming M2 descriptor admission.

If product callers only ever used the metadata-v2 Resource adapter, an evolve override would still be needed for `canonical.validate(..., registry=from_contents(...))` and for the 15 envelope/report root refs if those go through the generic oracle.

## Limits

jsonschema 4.25.1 only. Fragment-ref safety is an implementation accident of “defs nodes lack `$schema`”; do not rely on it without the evolve fix. Did not re-run 486986 cases. Did not implement the successor. Bounded grep also hit `ACTIVE-WORK.md` and a trial03 `x-maxUtf8Bytes` addendum; owners above are from identity-and-evidence, source-map, control schema, canonical.py, and metadata-v2 `check_metadata.py`, not from those review narratives.
