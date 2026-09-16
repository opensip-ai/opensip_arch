# Query-fault coauthor proposal for RC37-01 and RC37-A1 (source37 root overlay), v2 completion

**Standing.** This is a bounded design/reference coauthor proposal by the same session (f5617310…). It is not independent acceptance, and it is not a whole-design, application, readiness or grade decision. All product qualification gates and recovery cases remain unperformed. Nothing was rebound, frozen, activated, committed or pushed.

**Outcome.**
- **RC37-01:** corrected in this proposal.
- **RC37-A1:** addressed in this proposal.
- **QF-I1 (new, pre-existing, root):** the overlay breaks the maintained `check-evaluator-faults.v3`.
- **QF-I2 (integration):** pins are stale for the six files. They were not rebound.

Exact hashes, commands and every run receipt are in `review.json`, which is assembled from the receipts by `probes/build_review.py`.

## v1 terminated incomplete

The v1 CLI exited 0, but its final response said it was waiting on two `run_in_background` checker batches. Those batches were stopped at teardown, so no batch summary and no review exist.

v1 did complete these receipts:
- the copy verifications
- the before/after exception-identity probe
- `check-query-projection` on the edited tree (193 checks, 0 failed)
- `edit-hashes.json` and `proposed-edits.diff`
- `check-composition` on both trees

v2 treats none of that as a pass. It reran every focused check in the foreground here. The v1 runtime (25,832 files) is byte-identical before and after this continuation.

## Inputs verified

| Input | Verification |
|---|---|
| Immutable overlay manifest `db9b7b3f…` and parent frozen37 manifest `245ef613…` | Verified |
| Reviewer's overlay copy | All 12,900 files verified; no mismatch, no extra |
| v1 `edit-hashes.json` | Recorded diff hash `8167db3b…` equals the actual diff |
| `work/source37-pristine` | Equals the input exactly |
| `work/source37-coauthor` | Differs only in the six files, each equal to its v1 after-hash |
| `work/source37-frozen` | Frozen37 verified, for failure attribution only |
| v1 probes | Ported by changing only the runtime path. Two were then edited in v2: the runner now records a timeout instead of being killed, and the probe picks the pristine tree for `before`. Final script hashes are in `review.json`. |

## Proposal: six files, before → after (SHA-256)

| File | Before | After | +/- |
|---|---|---|---|
| foundation/identity-model.v3.py | 204e0f00bc18d468… | 9376aaae10a7fbe6… | +34/-6 |
| foundation/evaluator_replay_model.v3.py | 59d3fc336d8a2681… | 26e88580acff3d93… | +16/-4 |
| foundation/evaluator_composition_model.v3.py | c2e7f58f65c3043a… | cceeb42bd2fb2212… | +5/-3 |
| workflows/query_projection_model.v3.py | 0d4433aef51f7cac… | bb9de8f7c7fece1b… | +105/-16 |
| workflows/query-projection-contract.v3.md | f7b2e7ca031d7605… | 6a504eb5657ab9a2… | +13/-3 |
| workflows/check-query-projection.v3.py | cfe85f887ccd4e41… | 82eddd7487af9863… | +221/-24 |

- `proposed-edits.diff` is against the immutable 12-file overlay, SHA-256 `8167db3b03d1da53c806d3791ee8ed1710a41e02cac68b93635535fb718facf4`, identical to v1's diff.
- The root successor still holds the before bytes for all six files, so there is no overlap with root's host-finalizer integration.

## RC37-01: CORRECTED-IN-COAUTHOR-PROPOSAL

### What the before-probe measured on the input overlay

Every one of these cases returned `HOST.IO_FAILURE` / `evidence.corrupt`:
- four fully reminted semantic false results (severity, fail→pass, indeterminate laundered, execution deficiency erased)
- a structural `REFERENCE_IDENTITY` refusal
- a `RuntimeError` carrying `EVALUATOR_COMPLETE_PROOF_REPLAY` text
- a `KeyError` carrying `EVIDENCE_UNAVAILABLE` text
- a foreign identity-copy class
- a `TypeError` inside the loaded replay comparison

Type identity, measured:
- Every refusal escaping `close_run` was a class object from the separately loaded replay stack (`composition_identity3` / `identity_canonical`).
- None was an instance of the query identity copy's classes, so `isinstance(exc, M.EvidenceUnavailable)` was never true.
- The `EVIDENCE_UNAVAILABLE` message prefix was therefore the actual missing-bytes route.

### Correction

**Identity (`identity-model.v3`).**
- New condition-only `CompleteReplayMismatch(C.AdmissionError)`. It carries the exact comparison key as message and `diagnostic`, and has no termination and no origin.
- `close_run` normalizes the replay stack's declared outcomes into its own module's classes by exact class object, then chains the original:
  - `UNAVAILABLE` → `EvidenceUnavailable`
  - `MISMATCHES` → `CompleteReplayMismatch`
  - declared owner `REFUSALS` → `C.AdmissionError`
  - any other exception propagates unchanged
- `EvidenceStore.restore` is a retained regeneration boundary. It maps the mismatch to the existing `RegenerationMismatch` carrier.

**Replay and composition.**
- The complete proof/object/blob comparison and the proof-id/evidence/seal/Run comparisons raise the mismatch with unchanged keys.
- The replay model declares its exact class-object tuples, the same idiom as `execution_inputs_model.CATCH`.

**Query model (`close_retained_run`).** It routes by the query identity copy's types only:

| `close_run` outcome | Public route |
|---|---|
| Identity `EvidenceUnavailable` | `evidence.missing` |
| `CompleteReplayMismatch` | Identity `RegenerationMismatch` carrier projected verbatim: `complete-replay-mismatch:retained-regeneration`, `HOST.IO_FAILURE` / host-io / `evidence.regeneration-mismatch`, subject = refused RunId |
| Other identity `AdmissionError` | `evidence.corrupt` |
| Anything else | Existing host-internal law: `SYSTEM.OUTCOME.ILLEGAL_STATE` / host-invariant / `HOST.INVARIANT_VIOLATED`, subject `close_run` |

The exact owner text is kept in `QueryRefusal.diagnostic` and never selects a route. No prefix or split parsing remains.

**Contract §7.** The A06 paragraph that legitimized `evidence.corrupt` is replaced by the four typed outcomes, and the table rows are updated. The query is a retained read, so it takes retained-regeneration. A live first-party evaluator that contradicts its own reconstruction keeps `complete-replay-mismatch:host-internal` at its own boundary.

### Result: after-probe and the maintained checker (193 checks, 0 failed)

**Routes.**
- All four semantic mutants: structurally admitted with new RunIds, then refused via `evidence.regeneration-mismatch` with subject = RunId. The termination equals the identity carrier and equals `evaluator_fault_model.route(owner_observation(carrier))` (condition `complete-replay-mismatch`, origin `retained-regeneration`). Exit 4, `errors` equal the `domainDetail`, no Run.
- Structural corruption: `evidence.corrupt` (cause is identity `AdmissionError`).
- Missing proof object: `evidence.missing` (subject = proof id).
- All four host defects: host-invariant, with detail and remedy equal to the registry's host-internal row.

**Distinctness and typing.**
- Four distinct routes, none of them provider-protocol or `CONFIG.INVALID`.
- The lawful Run replays and queries unchanged after the monkeypatches are restored.
- The replay stack is proven to be a separate identity load.
- `close_retained_run` contains no prefix parsing.

**Origin law is unchanged.**
- A row-isolated replica of `check-evaluator-faults` gives all 24 routes and details identical across frozen37, the input overlay and the edited tree.
- Owner carriers admit.
- A condition-only `CompleteReplayMismatch` is refused as an owner carrier (`EVALUATOR_FAULT_OWNER_CARRIER`), so the condition cannot bypass origin assignment.

**Maintained RunIds are identical:**
- declares-exists `run3:0cd01b29…`
- incoming-incomplete `run3:f9b48563…`
- missing-inventory `run3:a3185cc7…`

## RC37-A1: ADDRESSED-IN-COAUTHOR-PROPOSAL

`ReferenceCallPrecondition` stays the right signal for the reference entry, where the observation is a call argument. The existing behavior is unchanged: an omitted observation is allowed; present null, wrong type or unknown values are refused; request-schema and missing-Run refusals still take precedence.

The contract now scopes that precondition and adds two reference laws, with no new public code:

1. **A product host adapter's own out-of-vocabulary observation** is an invalid host-generated internal layer.
   - With a valid reserved RequestId: operational-failed / `SYSTEM.OUTCOME.ILLEGAL_STATE` / host-invariant / exit 4 / `HOST.INVARIANT_VIOLATED`, subject `host.availability` (`host_adapter_refusal`).
   - Without a valid RequestId, or for the RequestId precondition itself, no envelope exists and the precondition is re-raised.
2. **A retained availability record** read from the store is a different cause.
   - Bytes failing identity `$defs/availability` admission, or naming another Run: `HOST.IO_FAILURE` / `evidence.corrupt` (`observe_retained_availability`).
   - An admitted record supplies its state as the observation.

The new controls pass:
- typed precondition
- adapter host-invariant route, with a valid envelope at exit 4
- no RequestId → precondition
- RequestId precondition not projected
- an admitted record's `purged` state routes to `evidence.purged`
- unparseable, unknown-state and other-Run records → `evidence.corrupt`

## Admitted-behavior impact of the foundation typed boundaries

The foundation edits change exception classes, not decisions or messages:
- `close_run` refusal messages and class names are unchanged.
- Comparison refusals remain `AdmissionError` subclasses with the same keys.
- One behavior change: `restore` now raises `RegenerationMismatch` for a semantically disagreeing retained Run, where it previously let an unnormalized `AdmissionError` escape.

On the input tree versus the edited tree, 11 affected maintained owners produce byte-identical stdout and stderr. Two of them (`check-execution-inputs` stdout, `check-evaluator-faults` stderr) are identical only after normalizing the tree directory name in file paths. Only the query checker differs, by design.

## Focused receipts (v2, foreground, pinned interpreter `-I -B`; no run changed any tree file)

| Checker | Input overlay | Edited |
|---|---|---|
| check-query-projection.v3 | exit 0, 162/0 | exit 0, 193/0 |
| check-identity | exit 0, 1596/0 | exit 0, 1596/0 |
| check-workflow-projection.v3 | exit 0, 493/0 | exit 0, 493/0 |
| check-replay.v3 | exit 0, 68 | exit 0, 68 |
| check-semantic-replay.v3 | exit 0, 18 | exit 0, 18 |
| check-execution-replay.v3 | exit 0, 8 | exit 0, 8 |
| check-candidate-replay.v3 | exit 0, 4 | exit 0, 4 |
| check-composition.v3 | exit 0, 20 | exit 0, 20 |
| check-provider-attribution-return.v2 | exit 0, 47/0 | exit 0, 47/0 |
| check-execution-inputs.v1 | exit 0 | exit 0 |
| check-comparison-knowledge.v3 | exit 0 | exit 0 |
| **check-evaluator-faults.v3** | **exit 1 (preserved failure)** | **exit 1 (identical)** |

check-evaluator-faults.v3 also ran on frozen37: exit 0, 40 rows.

Probes (all exit 0):
- exception-identity, before on the input tree and after on the edited tree
- fault-owner rows on frozen37, the input overlay and the edited tree; the only row not as expected on the input overlay and on the edited tree is `envelope-termination-origin`

## QF-I1: the root overlay breaks the maintained check-evaluator-faults.v3 (pre-existing)

**Failure.** Control `envelope-termination-origin` sets `errorCode` to `HOST.IO_FAILURE` while `faultCause` stays `provider-protocol`.
- The overlay's common StepTermination operational pair law (R2) now refuses it with a jsonschema `ValidationError` inside `validate_profile`.
- That happens before `validate_envelope` reaches `EVALUATOR_FAULT_ENVELOPE_PARITY`.
- The checker re-raises and aborts before the owner-carrier rows.
- The mutated envelope is still refused, so the checker's abort does not open a hole; the maintained control is broken.

**Attribution.** frozen37 passes this checker. The input overlay and the edited tree fail identically. The completed independent review did not run this checker.

**Remedy (root / evaluator-fault owner).** Either accept the earlier pair-law refusal in that control, or check parity before profile validation. Then rerun the checker. The checker is not one of the owned files here, so it was not edited.

## Registered identity, RunIds and pins

- No registered payload or digest-domain schema changed; all six files are `.py` or `.md`. The fault schema, identity schemas, public-detail registry and common schemas are untouched.
- The lawful RunIds and the replay, identity and semantic checker outputs are unchanged.
- **QF-I2:** all six files are pinned in the five source-pins files.
  - The three foundation files are newly stale.
  - The three query files were already stale from the root overlay (RC37-A2), including their `workflows-report` rows.
  - None of the six is a v5 normative input.
  - No rebind was performed.

## Limitations

- These are reference Python models over synthetic native-admitted fixtures. No product host adapter, evidence store, compiler, provider or platform is qualified.
- `REFUSALS` is a closed, explicit list. An owner that later raises a new refusal class will surface as a host-invariant fault until that class is listed.
  - The measured corpus (structural, missing, semantic and execution-input refusals) contained only listed classes.
  - Atom, enumeration and native refusal classes were not individually triggered through `close_run`.
- Host-defect controls monkeypatch in-process; they model untyped failures, not real host faults.
- The live first-party evaluator host-internal boundary is contract law only here. Its producer belongs to the whole-Run host termination owner.
- The rows of check-evaluator-faults skipped by its abort were exercised only by the replica probe, which is not the maintained checker.
- Not run: global suites, pin and planning checkers, freeze, host-finalizer, security carrier, semantic fixture, new termination owners, product gates and recovery cases.
