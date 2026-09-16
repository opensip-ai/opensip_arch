# Stage-meta reference selection v1 — scoped design-unit review

**Verdict: `ACCEPT-DESIGN-UNIT`**

Root remains lead. Not Claude agreement. Frozen **proposal**, **not selected**. Not Rust, runtime, instance execution, regex compilation, full Run, replay, or live install. Archived advisory24 / portable-choice / standards-precision are **advisories, not acceptance**. Root assent and private activation remain required.

**subjectManifestSha256** `91cd4c585a6605990ac5fc2a81e52da9a9c79fd236edccff89a5afbacaa69269`  
`docs/implementation/m2/stage-meta-reference-selection-v1-subject.json` **4858** bytes, **21/21** files, paths sorted unique, 0 pin mismatches.

Successor `docs/implementation/m2/stage-meta-reference-selection-v1/successor.json` **10621** / `129bceca5f8e27cf3e14377453f8688b4169dd7b65aef1519f2bbdffc6880cb5`. Candidates (20) equal the subject minus that record.

## What this unit is

Concrete Option A: replace ambient `Draft202012Validator.check_schema` (import-time FORMAT_CHECKER) with instance-validation against **eight pinned** Draft 2020-12 **default** meta-schema resources, **`format_checker=None`**. Format-assertion vocabulary is **not** in the bundle (present in jsonschema-specifications but unreachable from the default root). No network retrieve. Optional URI/regex packages cannot add assertions.

`admit_stage_output_schema` is the **only** identity function changed versus selected predecessor `7f840b9a…89e9` / 158607. Remainder AST is identical (delta +132 bytes). Tree membership, raw digest, `C.parse`, dict + exact `$schema` URL, and typed declaration are preserved. Pretty registered bytes still ADMIT. jsonschema is no longer imported from `identity_model.py`; the profile lives in sibling `stage_schema_model.v1.py` plus `stage-meta-2020-12/`.

Named compatibility delta (explicit, not silent): `"pattern": "("` and `patternProperties` key `"("` move from `DOCUMENT_INVALID` to structurally admitted. Registration does **not** compile producer regex or execute instances. A later execution owner must declare a deterministic dialect and fail closed before claiming validated outputs. No such execution is added here.

## Parents (live 18/25 accepted map)

Independently rebuilt as `verify_design.py`: source+application manifests, inventory candidates, contract records and their candidates. Observed live lock **18/25**, last contract `native-runtime-selection-v11`; this unit **not** selected. Historical source-selection-v2 successor is **not** in the map.

| Parent | Live class |
| --- | --- |
| `identity-schemas.v3.json` a76c | application/source manifest |
| `identity.v3.schema.json` 311c 197480 | contract-candidate of **source-selection-v3** |
| `source-selection-v3/successor.json` `e638c55c…4ae4` | contract-record |
| predicate-matching-v1 `identity_model.py` `7f840b9a…` | contract-candidate of **predicate-matching-v2** |
| `predicate-matching-reference-selection-v2/successor.json` `99df59c0…` | contract-record |
| `identity-and-evidence.md` `c82404f3…` | application/source manifest |

Workflow glob/interruption correction remains selected as a v2 candidate (`workflows_model.v1.py` `1d5212d5…`). Physical schema bytes unchanged (overrides on `registeredBy/law` and prose line 1314 only). Dual 311c+a76c description-law bind; three override keys unique; each `before` exact.

## Profile pin

Manifest lists eight resources; each disk pin and `$id` match; each JSON object equals `jsonschema-specifications` 2025.9.1 `REGISTRY.contents(id)`. Reachable formats still only `regex`, `uri`, `uri-reference`; none asserted (`format_checker=None`). Two fixed meta-schema **pattern** keywords remain assertions, including trailing-LF `$` (`$anchor` `a\n` ADMIT, `a\r` refuse; `$id` `a#\n` ADMIT). COPYING present. Corrupt bundle bytes raise tooling `STAGE_META_REFERENCE_*`, not document admission.

Closed `Registry` of those eight ids only: producer `$ref` strings are inert. Product identity `schema.rs` is not substituted. Identity crate TCB unchanged (this unit is Python reference). jsonschema 4.25.1 / referencing 0.37.0 implement the **pinned documents**, not a new product crate.

## Evidence (not the helper)

Frozen `check-stage-meta.py` independently rerun (Python 3.12.13): **6332** corpus rows, candidate ≡ `check_schema(None)`, **0** mismatches, **15** intentional vs ambient FORMAT_CHECKER; **20** actual `admit_stage_output_schema` cases (invalid-pattern / invalid-pattern-property are the only helper deltas); **4** ambient format-mutation controls still ADMIT. Output equals pinned `check-result.json` `a5df2ada…895b`. Projection generator/corpus is **evidence**, not the normative helper.

Archived advisory24 + portable-choice + standards-precision pin-match this reviewer’s private tree. Root disposition: Option A, not selected by advisory.

## requiredFindings

None.

## Limits / not claimed

Not selected, not M2 complete, not Rust meta-checker, not instance/regex execution, not walk `OwnerJoin` wiring, not full Run/replay. Successor/Rust checkers must not silently tighten the two ASCII `$` patterns. Execution-owner dialect remains a later unit.
