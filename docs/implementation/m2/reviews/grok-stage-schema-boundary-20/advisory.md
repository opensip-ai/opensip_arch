# Advisory: stage-output schema owner (post-walk stages)

**Reviewer:** Grok. Root remains lead. Not Claude agreement.
**Kind:** Bounded next-owner map for `admit_stage_output_schema` and the selected stage-loop joins that surround it. **Not ACCEPT-DESIGN-UNIT. Not implementation. Not ReplayedRun. Not view-18 source.**
**Work tree:** `/tmp/opensip-implementation/m2-grok-stage-schema-boundary-20/review`. No live/frozen/history edits.

Selected identity `619d6e3c…41e6` / 158555; selected native `e6784aa1…e2b9` / 319944 (**no** stage-output functions). Live lock independently **16 inventory / 20 contract** (inventory v18, runtime v7 / Coverage-17 installed). `coverage.rs` is live; `view_joins.rs` is not.

## Actual caller order (`open_run_closure`)

`admit_stage_output_schema` is **not** called from schema `walk` / `digest_field`.

Python `digest_field` for `raw-artifact` (992–1001) only `blob()`s, then special-cases `artifactClass==registered-schema-document`. It does **not** mention `producer-interface-stage-output-schema`. Live Walker **784–785** refuses that class as `Unsupported("stage output schema owner join")` — fail-closed until this owner exists. **Blob membership alone is not the owner.**

Selected post-walk loop (**1788–1794**), after policy/program (1768–1784), **before** evaluation-view census (1809) and view-joins (1853):

1. `payload(stage['stageSpecDigest'], 'stage-spec')` (1041–1054): canonical bytes, identity-v3 `#/$defs/stage-spec` shape, `ordered`, **`admit_closure_field_kinds`** (`stage-spec.producerClosure` must be kind **`provider`**, identity-v3 4737), memo, **then `walk`** of the stage-spec (hits `outputSchemaDigest` → blob / live Unsupported).
2. `STAGE_SPEC_PLAN_JOIN` — `spec.planId == run.planId` (1790)
3. `STAGE_SPEC_UNSELECTED_PRODUCER` — `spec.producerClosure ∈ plan.semanticClosures` (1791)
4. `STAGE_SPEC_OUTPUT_DOMAIN_JOIN` — typed-equal `spec.outputDomains` vs `stage.outputDomains` (1792). Empty domains lawful (identity-v3 2996).
5. `STAGE_SPEC_HIDDEN_PARAMETER` — every `spec.parameters` row ∈ `analysis_spec.parameters` (1793)
6. **`admit_stage_output_schema(spec, get(producerClosure,'closure'), blob(outputSchemaDigest))` (1794 / 735–761)**

Later **`admit_cache_entry` (2008–2067)** is **not** this owner: it `close_run`s first, then `CACHE_OUTPUT_SCHEMA_JOIN` digest equality (2044) and `blob(outputSchemaDigest)` (2047) **without** re-running 735–761. A cache hit is not schema ownership.

## Exact owner (`admit_stage_output_schema` 735–761)

Inputs: already shape-admitted **stage-spec** record, retained **producer closure descriptor**, **raw** blob bytes for `spec['outputSchemaDigest']`.

| Step | Law | Refusal |
| --- | --- | --- |
| 729–733 | `operation` matches `^[a-z0-9][a-z0-9._-]{0,127}$` | `STAGE_OUTPUT_SCHEMA_OPERATION_NOT_A_PATH_SEGMENT` (Text shape is not enough; identity-v3 2936–2941) |
| 745–747 | closure `tree` has **exact** path `opensip-interface/stage-output/{operation}.schema.json` | `STAGE_OUTPUT_SCHEMA_UNREGISTERED:<path>` — **not** a lookup-miss fallback (743–744) |
| 748 | `tree[0].sha256` for that path == `spec.outputSchemaDigest` | `STAGE_OUTPUT_SCHEMA_REGISTRATION_MISMATCH:<path>` |
| 749 | `raw` is bytes and `sha256(raw)==outputSchemaDigest` | `BLOB_DIGEST` |
| 752–757 | `C.parse` object; `$schema` **exactly** `https://json-schema.org/draft/2020-12/schema`; `Draft202012Validator.check_schema` | `STAGE_OUTPUT_SCHEMA_DOCUMENT_INVALID:<path>` |
| 758–760 | `C.equal_typed(document['x-opensip-stage-output'], {schemaVersion:1, operation, outputDomains})` | `STAGE_OUTPUT_SCHEMA_DECLARATION_MISMATCH:<path>` |

Returns the **parsed document**. That is **not** instance validation of stage outputs, not replay, not Plan ADMIT.

Identity-v3 `outputSchemaDigest` (2998–3023) `artifactClass: producer-interface-stage-output-schema`; `registeredBy` matches 726–733 and 758–760. `law`: retained bytes are **not** a registration.

## Shape vs producer authority

| What | Authority |
| --- | --- |
| `identity_record_shape` / `payload(...,'stage-spec')` | canonical JSON + identity-v3 shape + collection order + producer **kind** |
| `registered_schema_blob` (live 1311) | membership in **identity payload-registry document set** (product schemas) |
| Walker blob / `inspect_local_structure` | retention of digest-named bytes |
| **This owner** | **producer-closure tree membership** + 2020-12 meta-schema + declaration join |

Using `registered_schema_blob` for stage-output bytes would treat a **producer interface** document as a **product** schema. Forbidden.

Native e678 has **zero** stage-output APIs. Do not invent native H-frames for this document.

## Smallest useful evaluator API

Evaluator (not identity — keeps 2020-12 meta-schema out of identity TCB; no reverse DAG edge):

```
admit_stage_output_schema(
  inputs: &RetainedInputs,
  spec_digest: [u8; 32],          // stage-spec record, rehashed
  producer_closure_id: &str,      // must match spec.producerClosure
  work: usize,
) -> Result<JsonValue, StageOutputError>
```

Inside: `identity_record_shape`/`inspect` stage-spec; `object(producer_closure_id, Closure)` rehash; `blob(outputSchemaDigest)` rehash; then **735–761** on those retained bytes. Caller (later walk orchestrator / `open_run_closure` 1788–1794) still does PLAN / UNSELECTED / OUTPUT_DOMAIN / HIDDEN_PARAMETER **before** this fn, as selected. This fn must **not** accept a caller ADMIT or skip tree membership because the blob is retained.

Reuse: `RetainedInputs::object`, `blob`, `identity_record_shape` (410–418), canonical parse. **Do not** reuse `registered_schema_blob`. Live 784–785 stays Unsupported until this fn is wired through `OwnerJoin` (advisory 19); wiring must call this owner, not map Unsupported → Ok.

Returned document is inert schema JSON. **Not** a Run, cache grant (`grantsEvidenceAuthority: False` at 2066), or Coverage token.

## Trust / resolution limits (selected code)

- Path is a **single** exact tree row, not a prefix walk; `{operation}` is a path **segment**, not an arbitrary string (729–733 vs Text).
- `members[0]` (746–748): if the tree lists the same path twice, **first** row wins; no uniqueness check. Duplicate path + disagreeing sha256 is a trap (first digest must match spec).
- `C.parse` + digest: bytes must be **canonical** identity JSON, not pretty JSON that hashes differently.
- `check_schema` is **schema-of-schema**, not validating stage output instances; not `$ref` retrieval. Selected code does **not** forbid remote `$ref`s in the producer document. A 2020-12 document that `$ref`s the network can still pass `check_schema` if the meta-validator does not fetch. **Do not** add HTTP retrieval; treat unresolved external `$ref` as outside this owner (instance validation / replay later) unless a later unit closes self-contained schemas.
- Empty `outputDomains` is lawful **declaration**; it is not completeness (2996).
- Producer must already be Plan-selected and kind `provider` **before** 1794; this owner does not re-check Plan membership (that's 1791 + `admit_closure_field_kinds`).

## Adversarial cases

| Case | Expect |
| --- | --- |
| Retained blob, path absent from producer tree | `UNREGISTERED:<path>` not MissingBlob-as-success |
| Path present, tree sha256 ≠ spec digest | `REGISTRATION_MISMATCH` |
| Spec digest ≠ sha256(raw) | `BLOB_DIGEST` |
| Operation `Analyze` / empty / `../x` | `OPERATION_NOT_A_PATH_SEGMENT` |
| `$schema` draft-07 or missing | `DOCUMENT_INVALID` |
| Valid 2020-12, declaration operation/domains ≠ spec | `DECLARATION_MISMATCH` |
| Declaration omitted | `DECLARATION_MISMATCH` (`None` vs record) |
| `registered_schema_blob` would accept (product schema digest) but tree lacks path | still `UNREGISTERED` |
| Walker/`inspect_local_structure` on stage-spec without this owner | live `Unsupported("stage output schema owner join")` — **not** Ok |
| Cache key matching digest after a Run | `CACHE_OUTPUT_SCHEMA_JOIN` only; **not** a second ownership proof |
| Hidden parameter not in analysis-spec | `STAGE_SPEC_HIDDEN_PARAMETER` **before** schema owner |
| Unselected producerClosure | `STAGE_SPEC_UNSELECTED_PRODUCER` **before** schema owner |
| Closure kind ≠ provider | `CLOSURE_FIELD_KIND:stage-spec.producerClosure:provider` in `payload()` |

## Semantic traps / missing prereqs

- Silent **blob-only** success (Python walk; forbidden as the owner).
- Treating `identity_record_shape(stage-spec)` as output-schema authority.
- Folding 1788–1793 into this fn (hides PLAN/HIDDEN_PARAMETER as schema faults).
- Implementing 2020-12 `check_schema` via identity product `SchemaHandle.admit_json` (wrong document set).
- Network `$ref` during meta-validate.
- Assuming native e678 owns this.
- Wiring advisory-19 `OwnerJoin` cut 785 to `Ok` without this fn.
- Duplicate tree paths.
- Cache/regeneration as schema owner.

**Missing for a later unit, not this fn:** instance-validate stage outputs against the returned document; replay; view-18; walk `OwnerJoin` glue.

## Verdict

**NOT ACCEPTANCE.** Smallest evaluator owner is `admit_stage_output_schema` over retained stage-spec + producer closure + output-schema blob, matching 735–761 and identity-v3 `registeredBy`. Surrounding 1788–1793 joins stay the orchestrator. No caller ADMIT; no blob-only success; no identity→evaluator.
