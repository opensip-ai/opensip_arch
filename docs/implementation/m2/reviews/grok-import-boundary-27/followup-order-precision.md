# Follow-up: SourceMappingV1 order/duplicate is `REGISTERED_RECORD`, not SHAPE

**Reviewer:** Grok. Root remains lead. Not Claude agreement.  
**Kind:** Bounded correction of one original-advisory expectation. Original `advisory.md` / `advisory.json` are **not rewritten**. **Not ACCEPT-DESIGN-UNIT. Not source27 approval.**  
**Work tree:** `/tmp/opensip-implementation/m2-grok-import-boundary-27/review`. Originals remain **22963** / `b52c4b27…40cb` and **8216** / `9c3acef7…d327`.

The original test table said unsorted or duplicate `generatedPath` at correspondence is `IMPORT_CORRESPONDENCE_SHAPE` (internal `IMPORT.ARTIFACT_CORRUPT`). That treated `admit_source_mapping`’s extra sort check as the first public fault. Selected ExactValidator already registers `x-opensip-order`, and SourceMappingV1.entries carries `{by:["generatedPath"]}`. `foreign_payload` therefore refuses **before** those extra checks.

## Actual selected path

`open_run_closure` 1972 is inside the `try`, but `foreign_payload` does not raise `imports.Refusal`:

1. `canonical_bytes` (`NONCANONICAL_FOREIGN_RECORD` if non-canonical).
2. `validate_registered_record` for a non-`foundation/` document calls `workflow_admission().validate_import_record`.
3. `validate_import_record` uses **canonical `ExactValidator`**, not generic Draft 2020-12. `x-opensip-order` is a registered validator.
4. On `Refusal` / `ValidationError` it wraps as `AdmissionError('REGISTERED_RECORD:'+selector)` — here **`REGISTERED_RECORD:#/$defs/SourceMappingV1`**.
5. `except imports.Refusal` at 1976–1977 does **not** catch that `AdmissionError`. Extra `admit_source_mapping` snapshot/inventory/sort runs only after shape admission returns.

The checker in `check_imports27.py` then classifies: `AdmissionError` whose string starts with `IMPORT_` / `ANALYSIS_SPEC_PARAMETER_` / `EVALUATOR_REQUIRED_PARAMETER_` / `CLOSURE_FIELD_KIND:import.` → `{result:refused, cause:<string>}`; **any other** `AdmissionError` (including `REGISTERED_RECORD:…`) → **`{result: invalid}`** with no `cause` field.

This follow-up executed selected exact-schema-profile `canonical.py` **8995** / `ad88e58f…96f7` (`ExactValidator.VALIDATORS` contains `x-opensip-order`) against product/coop `imported-v1` **46315** / `edce21a3…4b9e`, and selected `workflows_model.v1.py` `validate_import_record`. Generic `Draft202012Validator` does **not** register `x-opensip-order`.

## Independent results

| Case | Exact profile | Generic Draft 2020-12 | `validate_import_record` | Extra `admit_source_mapping` | Identity string | Harness (`check_imports27` / 408-row corpus) |
| --- | --- | --- | --- | --- | --- | --- |
| `mapping-duplicate` (byte-identical second entry) | refuse `uniqueItems` | refuse `uniqueItems` | `Refusal` `CONFIG.INVALID` | **not reached** | `REGISTERED_RECORD:#/$defs/SourceMappingV1` | `{result: invalid}` (index 76) |
| `mapping-same-generated` (same `generatedPath`, different `generatedSha256`) | refuse **`x-opensip-order`** (“strict unique order required”) | **accept** | `Refusal` `CONFIG.INVALID` | **not reached** | `REGISTERED_RECORD:#/$defs/SourceMappingV1` | `{result: invalid}` (index 77) |
| `mapping-bad-order` (`generated.js` then `a`) | refuse **`x-opensip-order`** | **accept** | `Refusal` `CONFIG.INVALID` | **not reached** | `REGISTERED_RECORD:#/$defs/SourceMappingV1` | `{result: invalid}` (index 78) |
| `mapping-wrong-snapshot` | accept | accept | accept | `IMPORT.SOURCE_MAPPING_REQUIRED` | `IMPORT_CORRESPONDENCE_SHAPE` | `{result: refused, cause: IMPORT_CORRESPONDENCE_SHAPE}` (index 70) |
| `mapping-source-sha` / `mapping-source-path` | accept | accept | accept | `IMPORT.SOURCE_MAPPING_REQUIRED` | `IMPORT_CORRESPONDENCE_SHAPE` | same SHAPE (indices 73 / 72) |
| `mapping-empty` | refuse `minItems` | refuse `minItems` | `Refusal` | not reached | `REGISTERED_RECORD:#/$defs/SourceMappingV1` | `{result: invalid}` |
| `mapping-generated-dotdot` / `mapping-source-dotdot` | refuse LogicalPath `not` | refuse LogicalPath `not` | `Refusal` | not reached | `REGISTERED_RECORD:#/$defs/SourceMappingV1` | `{result: invalid}` |
| `mapping-two-rows` (sorted unique `generated.js`, `z`) | accept | accept | accept | ok | (checked) | `{result: checked, imports: 1}` |

`same-generated` and `bad-order` are the cases generic jsonschema would mis-admit. Duplicate whole items fail `uniqueItems` even without `exact_order`; they still never become SHAPE at this closure.

Trial corpus `/tmp/opensip-implementation/m2-import-joins-trial-27/imports-requests.ndjson` with `check_imports27.py`: **408 cases, 0 mismatch**. Observed as classification evidence only. Mutable `import_joins.rs` is **not** reviewed or accepted here. Root’s module name `import_joins.rs` is consistent with `view_joins.rs` / `run_links.rs`; that naming is not a law change. Closed parameter metadata derived from actual 311c rows + `DOCUMENT_ALIASES` (no caller registry) matches the original reuse recommendation.

## Disposition

**Withdrawn from the original test table:** unsorted / duplicate `generatedPath` → `IMPORT_CORRESPONDENCE_SHAPE`. Replace with `REGISTERED_RECORD:#/$defs/SourceMappingV1` (harness `{result: invalid}`).

**Withdrawn from original successor-worthiness as stated:** listing “order” among mapping `Refusal`s collapsed to SHAPE. At this closure, order/uniqueness of `generatedPath` is ExactValidator/`uniqueItems` shape. SHAPE remains the catch for **post-shape** mapping snapshot-id and inventory-digest `Refusal`s only. The extra sort/unique block inside `admit_source_mapping` is still selected law for **direct** callers; `open_run_closure` does not reach it for these order/duplicate inputs.

**Unchanged:** named `IMPORT_SOURCE_MAPPING_REQUIRED` only for a null correspondence mapping pointer; exact-snapshot never `classify_staleness`; host `imports.rs` cannot own pure admission; full-walk two-key `payloadClass==import` remains **outstanding and not bypassed** (the 408-row oracle used an explicit local payload-walk shim). Inventory prose that assigned imported-schema semantic admission to host `imports.rs` stays a future runtime-unit correction, as root noted.

Original advisory bytes preserved. This note is not a new design acceptance and not an exact-source review of source27.
