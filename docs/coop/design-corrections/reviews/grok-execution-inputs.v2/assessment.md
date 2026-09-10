I’ll fix the four execution-input files against real owner records: Plan locator, Coverage envelope, view2 H identity, and EvidenceStore custody—without touching root or the v1 review pin.Coverage is the foundation `coverage2` envelope (scopeId + payload), not a stub key. I’ll rework schema and model around owner `objects`/`blobs` and derived account state.Rewriting the four files to close the false passes: owner envelopes, H-suffix locators, required store pointers, and derived coverage state.Same four files only. v1 pin at `grok-execution-inputs.v1` was not overwritten. Root/enum files were not edited. Coauthor correction, not acceptance.

Python 3.12.13: **19 cases, 0 mismatches.** Default prints JSON to stdout; `--receipt` wrote `grok-execution-inputs.v2` (v1 refused). Owner graphs come from `evaluator_graph_fixture.v3.py`.

### False passes closed
- `accountState=complete` with empty `coverageIds` is schema-invalid.
- Self-asserted `coverage` / `examinedExhaustive` must **derive** from owner `coverage2` envelope + payload `entry`; mismatch is `EXECUTION_INPUTS_COVERAGE_DERIVE`.
- `store_pointers` is required; missing mapped record is pointer/lost/mismatch, never a skip.
- View locators are **view2 H suffixes** (re-identified with M3). Blob hash ≠ H suffix. Inventory C-digest mismatch is `REF_MISMATCH`, not pointer; bad bytes are `REF_INVALID_BYTES`.
- Inventories: exactly one digest per kind, `ci/po` join. Duplicate same-kind is schema/join refuse.
- VCS `kind=none` makes `vcs-change` **inapplicable** from the admitted VCS observation; `not-applicable` resolution alone cannot claim complete Coverage.

### Settled law
- Post-Plan INPUT, raw C identity, **not** a Plan parameter. `plan_id` is an explicit locator.
- Selected complete outputs: `stageOrdinal` non-null. Unavailable/unselected may null with typed reason. Enumerator, stage producer, view `planId`, and scope U are checked.
- Required unsupported/unavailable/incomplete native work → **ADMIT + `requiredCellDeficiencies`** (semantic indeterminate), including all-rules-disabled. Owner file graph ADMITs with `native-work-incomplete` on **package** (fixture has file Coverage only — not a fake complete).
- Candidate envelope binds cell/program/U/producer/stage/capability/mode/extent; groups are real `CloneCandidateGroupV2` bytes. Missing required pointer is protocol; retained unavailable/partial is one execution deficiency per binding.
- Host capture is a **TCB trust boundary**. Replay can equate proof selection to this inventory; it cannot certify a malicious host omission. Stage receipts are rooted in the execution-plan; the store is not the selection.

### Counts / files

| File | SHA-256 |
|---|---|
| `execution-inputs.schema.v1.json` | `fbf4f17501232e6664242adc9c2186def6d6bf5e04f90b9170335423b615efe0` |
| `execution-inputs-contract.v1.md` | `1a7b62dd17c41cdca7c631a3eb2ec537c3b316b38160c62c1e54283bf2ef60e9` |
| `execution_inputs_model.v1.py` | `245fb508aed0126bf70f16ab691442be922050acdb9cb4a4fb7e6aad62f0219e` |
| `check-execution-inputs.v1.py` | `ae254c37ad49b2113a7a741502a0da056b91d8997fe7609529025537f76ec46d` |

### Remaining limitations (registration, not open architecture)
- Root ProofInputRef / reconstruct wiring still next.
- Owner fixture has no `clones-near` cell; group-bytes join is a dedicated admit case, not the file-positive graph.
- Package Coverage absence on the fixture is reported as incomplete required work, not invented complete-empty Coverage.
