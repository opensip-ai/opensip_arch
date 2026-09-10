# v8 — candidate full-Run reference and v7 advice dispositions

**Standing.** Architecture/reference only. Isolated successor. Not a Run. Not a freeze review. v7 history is retained and not rewritten. Core M3/schema/I/E were not edited.

**Python.** `/tmp/opensip-architecture-review-env/bin/python -I -B` (3.12).

## Candidate-only public full-Run (S2 accepted)

New exclusive files:

- `foundation/evaluator_candidate_fixture.v3.py`
- `foundation/check-candidate-replay.v3.py`

Composes `F.build_file_inputs` (owner-admitted **syntax** universe, `syntax-only`). Matrix cell `clones-near @ syntax-only` is `SUPPORTED-DESIGN`. Does not bind a TypeScript universe to a syntax-only request. Remints Plan / analysis-spec / enumeration cells / execution-plan / views / inventories so clones-near is a real required `requestedCapabilities` row. `near_candidate_kw` remains a bounded join fixture and is not a full Run.

Controls (`check-candidate-replay.stdout.json`, 4/4):

| Case | Result |
|---|---|
| complete-empty-candidate-full-run | `close_run` ADMIT, verdict `pass`, digest `820ed010…29ff` |
| group-bearing-candidate-full-run | `close_run` ADMIT, group `authority=candidate-only` |
| missing-required-candidate-indeterminate | retained unavailable envelope, verdict `indeterminate`, cause `provider-unavailable` |
| forbidden-fact-authority-group | owner seed ADMIT, semantic `EXECUTION_INPUTS_CANDIDATE_GROUP` |

Reconstruct reads group/source bodies from blobs with `groups={}` (same as root `execution_input_account`).

Helper tweak (needed for the retained unavailable envelope): selected+non-null-U unavailable rows keep `stageOrdinal` non-null so `CellProgramOutcomeV1` is schema-valid. v6 52 still `mismatches []`; execution-replay 8 still PASS.

## v7 advice dispositions (no history rewrite)

**S1 — qualified, no new field.** `requiredCellDeficiencies.cause=native-work-incomplete` is the join category. Originating native `deficiency=provider-unavailable` is what proof `executionDeficiencies` carry; `nativeCause` is the lawful null for that token. Full replay recomputes the account. No originating native pair is lost. A second cause field would duplicate the registry projection.

**S2 — done.** Candidate path is public-bound as above.

**S3 — nonblocking, no model change.** One-pass `promised_pointers` is not a valid-case bug: well-typed `selectedRefs` include coverage, missing payload is `EVIDENCE_UNAVAILABLE`. An optional second walk is not a freeze blocker.

**A1 — declined as a named key.** `close_run` is complete replay and already refuses digest vs selection mismatch (`EVALUATOR_COMPLETE_PROOF_REPLAY`). Public close fulfills the law.

**A2 — withdrawn as a general gap.** `check-replay.v3.py` already drives nonempty `runtime` / `test` / `history` `import_specs` with a captured manifest (runtime-known-hit, history-complete-zero, test-row-exact-location, …). v7 A2 only observed the default file graph’s empty `importIds`, not the public 38.

**A3 — not unfinished architecture.** Host-derived typed inputs (inventory, candidate, target, incoming) are the selectedRefs law while stage `outputDomains` remain `view`. Product host implementation is out of scope.

## Receipts

- `/tmp/opensip-design-corrections/grok-execution-inputs.v8/check-candidate-replay.stdout.json`
- `check-execution-replay.stdout.json` (8 PASS, helper-compatible)
- `execution-inputs-check-receipt.json` (52, mismatches [])
- `hashes.json`

Root may freeze the required candidate path. No extra optional refactors.
