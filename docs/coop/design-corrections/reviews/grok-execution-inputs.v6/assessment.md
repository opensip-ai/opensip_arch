I'll reproduce the ambient-store digest leak from the probe first, then strip physical retention fields out of the hashed ExecutionInputs record while keeping selectedRefs and operational pointer checks.I’ll reproduce the probe against the current helper, then read how root and admission use the retained-key fields so the replacement API stays exact.Probe reproduced: same Plan and selectedRefs, ambient blob still changes the digest via `hostCapture`. I’ll remove those physical fields from the hashed record and derive promised pointers from selected/owner refs.Root flipped the fixture default to `complete_required_native=True`. I’ll keep that default, and keep the missing-package case explicit with `False` so we don’t invent Coverage.The ambient probe is closed. Same Plan and same `selectedRefs` no longer change `C(ExecutionInputs)` when an unselected blob is added (`changedFields: []`). Physical store census is out of the hashed record.

v5 binding-carrier / per-Coverage pairs / canonical-record dedup and helper stored=capture=admission (before seed seal) are kept. v1–v5 receipts are untouched. This is not a Run.

## Semantic vs operational

`hostCapture.retainedObjectKeys` / `retainedBlobDigests` are **removed** from ExecutionInputsV1 (`additionalProperties: false`). Stage receipts, `selectedRefs`, cell outcomes, and `hostDerivedRefs` stay hashed.

Physical availability is `operationalCapture` metadata only — not a Run preimage. `store_pointers` remains a required **caller kw**, not a record field.

## Integration API for `execution_input_account`

Delete the ambient loops. Do not read `hostCapture.retainedObjectKeys` / `retainedBlobDigests`.

```python
promised = X.promised_pointers(
    manifest, plan, execution, enumeration,
    objects=objects, blobs=blobs,
)
result = X.admit_execution_inputs(
    plan_id=plan_id, plan=plan,
    execution_plan_id=execution_id, execution_plan=execution,
    enumeration_plan=enumeration, analysis_spec=spec,
    execution_inputs=manifest,
    objects=objects, blobs=blobs,
    store_pointers=promised["store_pointers"],  # NOT objects.keys()+blobs.keys()
    inventories={E.sha(i): i for i in inventories},
    closures=closures,
    imports={i.split(":", 1)[1]: objects[i][1] for i in plan["importIds"]},
    candidate_results=records("candidate-producer-result"),
    target_attributions=records("target-attribution"),
    incoming_searches=records("incoming-search"),
    stage_specs={s["stageSpecDigest"]: C.parse(blobs[s["stageSpecDigest"]]) for s in execution["stages"]},
    vcs_observation=C.parse(blobs[objects[plan["snapshotId"]][1]["vcsDigest"]]),
)
# optional, not Run identity:
op = X.operational_capture_receipt(promised, objects, blobs, exclude_blob=ref["digest"])
```

`promised_pointers` is the logical closure of `selectedRefs` plus owner references (plan/snapshot locators, view coverage/scope, coverage `payloadDigest`, stage-spec digests, candidate `groupDigests` and `sourceBodies.contentSha256`). Extra unselected cache objects are excluded.

Distinctions unchanged:

| Condition | Key |
|---|---|
| promised locator absent from `store_pointers` | `EXECUTION_INPUTS_REF_POINTER` |
| pointer present, object/blob absent | `EXECUTION_INPUTS_REF_LOST_BYTES` |
| coverage envelope present, payload blob absent | `EXECUTION_INPUTS_EVIDENCE_UNAVAILABLE` |
| bytes present, hash/parse fails | `EXECUTION_INPUTS_REF_INVALID_BYTES` |

Helper: `attach_host_capture` **before seed seal**. Returns `{graph, manifest, digest, admission, evaluationInputRefs, operationalCapture}`. `evaluationInputRefs = selectedRefs + execution-inputs ref`. Stored blob digest = `C(manifest)` = admission digest. On `complete_required_native=False`: stored=capture=admission `e8711c18123d596f3efb894f91f62e81fce1c0267971089d46244014203f178b`, missing package work described, no invented Coverage.

Root fixture default is now `complete_required_native=True` (unaltered here). Missing-package work is the explicit `False` case.

## Checks

Python 3.12. 52 cases, `mismatches []`, `oracles []`. `--receipt` into v1–v5 refused. Probe: both digests `b0b7f3c845eb0a1cb1304ce88ba802be925b835670e28052bf20b54ea6b44d8a`.

Reports: `/tmp/opensip-design-corrections/grok-execution-inputs.v6/check-receipt.json` and `hashes.json`.

| File | bytes | sha256 |
|---|---|---|
| `execution-inputs.schema.v1.json` | 25562 | `1ce9e7a38110f5de86166b0274fe19cc228b85be5c13aac9d2f24cc7f373baf2` |
| `execution-inputs-contract.v1.md` | 15781 | `bd4cdc8462a0558491f34afdcc3ca966d2d98f818c33e10bdb0d91a1b57f97f1` |
| `execution_inputs_model.v1.py` | 70069 | `b435f21b1da7af31b0aba53923be552df880518014acd305f3bf9d6f49a86547` |
| `check-execution-inputs.v1.py` | 61169 | `7e9cb513597f0d07626882c5fee0c898bc4d9911cb839077bebdb8687de11c6c` |
| `execution_inputs_fixture.v3.py` | 22433 | `a6ec0dcb8d992d1dc358fe544e9deb099799ab391481dcc4735f8a1674ae744a` |

Root still activates `proof.executionInputsDigest` after workflow v9. `evaluator_input_model.v3.py` was not edited.
