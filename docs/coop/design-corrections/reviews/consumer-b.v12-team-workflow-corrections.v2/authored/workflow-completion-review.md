# Workflow completion (peer-refusal author correction)

**Verdict: `WORKFLOWS_INCOMPLETE`**

Same fresh kit-only origin. This is reference **author correction**, not product implementation and not independent acceptance of these new bytes. Peer `WORKFLOW_SCOPE_REFUSED` grades were hypotheses assessed against original requirement kinds/verbs. Frozen Run stores were not rewritten; their `close_run` remains unverified. Not whole-consumer ACCEPT.

Peer first refusal `R-CONFIG-CUSTOM-MULTI-BASE` is corrected. The remaining incomplete item is the original chain’s complete-Run arrow.

## Custody

| Object | SHA-256 | Result |
|---|---|---|
| kit manifest | `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8` | 80/80 PASS |
| parent | `a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb` | match |
| requirements.json | `855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495` | unchanged |
| team-inputs (4 files) | as in `team-inputs.json` | authenticated |

Five Run stores remain byte-identical (`frozen-run-hashes.json`). Peer-refused predecessors preserved under `preserved-failures/workflow-selfaudit-v4-peer-refused/`. Historical v2-refused originals remain under `preserved-failures/workflow-review-v2-refused-original/`. Path redirects: `path-correction-record.v4.json`.

## From-scratch isolated command

```bash
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-team-workflow-corrections.v2/output/scripts/workflow_correct.py
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-team-workflow-corrections.v2/output/scripts/workflow_correct_test.py
```

Last run: both exit 0. Tests fail nonzero on a failed assertion.

## Per-peer finding changes (no disputes)

| ID | Peer | This pass | Change |
|---|---|---|---|
| `R-CONFIG-CUSTOM-MULTI-BASE` | REFUSED | corrected | `extendsResolved` is the sequence `[base, strict, base]`; later entry wins; repeated edges retained. A diamond is not a repeated-base sequence. |
| `R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR` | REFUSED | corrected | All six parity fields; `query-response` is complete `GraphQueryResponseV1` on human/json/agent; `neighborsPaged` is `truncated-page` with `truncated=false`; page-2 continuation retained (`fact2:ae187938…`). |
| `R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE` | REFUSED | corrected | Retained span, `compilerBuild`, integer-edition BLV, and FACT-IDENTITY frame. L0 remints from those preimages. Ownership never enters BLV. |
| `R-MIN-RESOLUTION-THREE-LEVELS` | REFUSED | corrected | Syntactic / resolved / type each retain qualifying and insufficient facts/Coverage. Values recomputed from those records. |
| `R-EMPTY-PARTIAL-UNAVAILABLE-MISSING` | REFUSED | corrected | Distinct `SubjectInventoryV1` complete-empty package, partial file with known rows, unavailable symbol, and `EXECUTION_INPUTS_REF_LOST_BYTES` pointer-without-blob. |
| `R-CHAIN-ZERO-CONFIG-TO-RECEIPT` | INCOMPLETE | **still incomplete** | Traces and frozen Run store hashes now mapped. `close_run` of those frozen bytes is pending and **not** an accepted flag. |

No peer finding is disputed. No new schema was invented.

## Remaining chain dependency (concrete)

`close_run` (identity-and-evidence §3 / identity-schemas.v3) of the exact frozen bytes `runs/syntax-code.store.json` SHA-256 `2e74a6b2dd2b94152d6c4ce266dbe1bc4b23dc257b0fea12a6c947d36fe08fe7`, joined to already-executed `traces/complete.json`, `traces/terminal.json`, `envelopes/single-step.json`, and `envelopes/receipt-availability.json`. Same-byte `ts.store.json` / `rust.store.json` if those universes are the chain’s complete-Run arrow. This pass does not rewrite those stores and does not claim `close_run`.

## Helper impacts

- `helper/workflow_laws.py`: integer rust `dialect.edition`; retained L0 preimages; complete query-response parity. Does not change frozen Run stores.
- `helper/schema_admit.py`: KIT path redirected to this v2 subject copy.

## 134 original IDs

Full rows: `workflow-completion-review.json#/originalRequirementIds`. Copied historical claims are **not** accepted by copy.

| reviewedScope | Count |
|---|---:|
| in-scope-executed | 47 |
| in-scope-INCOMPLETE | 1 |
| standing of consumer continuation (not re-executed) | 24 |
| historical vector notReached | 23 |
| out-of-scope frozen Run | 24 |
| out-of-scope frozen Run replay | 12 |
| futureQualification | 3 |
| **total** | **134** |

All 48 in-scope IDs were re-executed. 47 complete; `R-CHAIN-ZERO-CONFIG-TO-RECEIPT` incomplete pending the named `close_run`. Per-ID artifacts: `workflow-completion-review.json#/all48Disposition`.

## Limitations

- Frozen Run `close_run` / other-Run replay stay out of scope.
- Query examples retain `underlyingRunAdmissionUnverified`.
- Synthetic TCB observations are labeled.
- This file is an authoring completion record, not independent acceptance.
