# Advisory: recognitionId H-identity / PREFIX composition gap

Not an acceptance. Not a successor. Frozen/live/history not edited. Graph04 `check_retained_records04.py` and `record-result.json` copied under `copies/` only.

## Fault

Selected `identity_model.proposed.v3.py` `digest_field` (line 1009):

```python
if representation=='h-identity':
    if 'domain' in annotation:
        return visit(PREFIX[annotation['domain']]+':'+value, annotation['domain'])
    return admit_frame(value, annotation['domainSet'])
```

`PREFIX` has the **19 core identity domains** (`fact`→`fact2`, …). It does **not** contain `native.framework-recognition.v1`.

Current live `framework-recognition-plan-v1.schema.json` (`49aacd86…`, same bytes as source-selection-v2) annotates `UnitRecognitionV1.recognitionId`:

```json
"x-opensip-digest": {
  "representation": "h-identity",
  "domain": "native.framework-recognition.v1",
  "form": "sha256-text",
  "retention": "derived",
  "authority": "native"
}
```

Selected `feature_model.py` `admit_framework_recognition_plan` / `J-FRP-ID` (line 875):

```python
need(row["recognitionId"] == native_h(RECOGNITION_DOMAIN, row["recognition"]), "J-FRP-ID")
# native_h = "sha256:" + C.identity(domain, record)
# RECOGNITION_DOMAIN = "native.framework-recognition.v1"
```

`digest_field` never reads `form` or `authority`. It always does `PREFIX[domain]`. That is a **KeyError**, not `AdmissionError`, and not a derived skip.

**Do not** skip all `retention: derived` (that would drop J-FRP-ID). **Do not** map KeyError → `invalid` (graph04 rust harness did that; python `reference-fault` is closer but still not a typed law).

## Counterexample (schema-valid + correct native_h)

`evidence/counterexample-unit-recognition.json`

- `C.validate` of `UnitRecognitionV1`: **OK**
- `C.validate` of full `FrameworkRecognitionPlanV1` with that unit: **OK**
- `recognitionId == native_h(RECOGNITION_DOMAIN, recognition)`: **True** (`sha256:1df5e0b1…6248`)
- `digest_field` on that field: **`KeyError('native.framework-recognition.v1')`**

Graph04 corpus row `schema:8369` used a dummy `sha256:aaa…` id (not the recipe) and still KeyError’d **before** any recipe compare. The same KeyError fires when the id **is** correct.

## Input-only defs vs bound Plan

`new_plan_admission.py`: **“Retained closure never invokes this entry point.”** Pre-Plan duty `admit_new_plan_recognition_parameter` only requires exactly one parameter row for new compiler-mode Plans. Predecessor Runs without the parameter stay admissible (`not-plan-bound`).

**Retained walk of a plan-bound FRP is different:** `foreign_payload(..., foundation/framework-recognition-plan.schema.v1.json, #)` walks `units[].recognitionId` and hits line 1009. A **schema-valid fully bound current Plan parameter therefore fails identity closure**, not only isolated `$defs` fixtures.

`admit_recognition_plan` still owns inventory/evidence/summary joins (`J-FRP-*`). Identity must not claim those. It also must not explode before the native owner can run J-FRP-ID.

## Same-class gaps (live product schemas)

`h-identity` + `domain` **not** in PREFIX and **no** `domainSet`:

| Site | domain | form | retention |
|---|---|---|---|
| FRP `recognitionId` | `native.framework-recognition.v1` | sha256-text | **derived** |
| native-v2 + report-v1 `unitId` / `selectedUnitIds` | `native.compilation-unit.v1` | sha256-text | **derived** |
| native-v2 context/universe/nested ids | `native.context.*`, `native.semantic-universe.*`, nested sets | sha256-text or bare-hex | **preimage-frame** (not in identity-v3 `DIGESTS.retention` four-value set) |

`preimage-frame` is a second composition hole (`DIGEST_RETENTION` if walked). `form` is ignored everywhere (PREFIX:hex vs `sha256:` vs bare-hex vs suffix). Template domains `native.context.<language>.v2` are not literal PREFIX or domainSet keys.

## Owner correction (proposal, not a waiver)

1. **identity `digest_field` h-identity**
   - If `domain in PREFIX`: apply `form` (`bare-hex` / `sha256-text` strip) then `visit(PREFIX[d]+':'+hex, d)`.
   - Elif `domain` ∈ `domainSets` (or nested): `admit_frame` after form strip — still **not** `admit_native_context`.
   - Elif `retention=='derived'` and `authority=='native'`: **typed** `AdmissionError('H_IDENTITY_NATIVE_DERIVED:'+domain)` **or** a declared recipe (`derivedFrom` sibling, e.g. `recognition`) so identity can check `value == 'sha256:'+identity(domain, sibling[field])` **without** `visit`/`PREFIX`. Missing recipe → typed error, never KeyError.
2. **Do not** skip derived as a class. Capability-manifest `derived` stays its own representation branch.
3. **feature_model** remains owner of J-FRP-ID **plus** J-FRP-EVIDENCE/ENTRY/SUMMARY. Identity recipe-check ≠ Plan admission.
4. **Rust walker:** `IdentityDomain::parse` → `Law`/`invalid` is the same misclassification as KeyError→invalid. Need an explicit native-derived/unsupported **or** recipe path.
5. **Controls:** (a) counterexample KeyError today; (b) after fix, matching `native_h` does not KeyError; (c) matching id still does **not** skip J-FRP-EVIDENCE; (d) `compilation-unit.v1` derived rows same class; (e) graph04 must not assert `invalid` for this fault.

## Limits

Did not edit models/schemas. Did not run native compilers. Graph04 harness mismatch (`reference-fault` vs rust `invalid`) is evidence of misclassification, not a product pass. Root decides successor vs port.
