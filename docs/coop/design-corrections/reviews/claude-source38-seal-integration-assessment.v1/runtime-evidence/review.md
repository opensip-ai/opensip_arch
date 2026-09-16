# Source38 SEAL integration fallout: coauthor assessment

**Standing.** Same query-fault coauthor origin (f5617310…) as v1/v2. This is a bounded integration assessment of root's two proposed corrections.
- It is not independent acceptance, source acceptance, final design, application, readiness or grades.
- Nothing was edited in source, live, pins or planning, and nothing was frozen, activated, committed or pushed.
- Root owns pin rebind, final suites, freeze and independent review.
- All product gates and recovery cases remain unperformed.

Exact hashes, commands, exit codes and probe rows are in `review.json`, built from receipts by `probes/build_review38.py`.

## Verdicts

| Subject | Verdict |
|---|---|
| root-final38-seal-correction.v1 (`security_lifecycle_model_v1.py` `fca87329…→d0ef9814…`, `check-analysis-seal-adapter.v1.py` `200635ed…→b0afeb84…`) | **ACCEPT-CORRECTION**. Pins stay stale; root must rebind and rerun the security owner suite. |
| root-source38-fault-check-correction.v1 (`check-evaluator-faults.v3.py` `79d4fc15…→57e0d9d8…`) | **ACCEPT-CORRECTION** |

## Inputs (verified)

- **Integrated source.** `termination-exclusivity-successor.v1/source` (12,904 files) already holds both root after-images and my six v2 after-images, byte-exact.
  - `work/source38-integrated` is an exact copy, equal file for file.
  - `work/source38-seal-before` is hardlinked from it; only root's two SEAL files are unlinked and rewritten with root's before-bytes.
- **Unchanged production fault law.** These equal the verified source37 overlay bytes:
  - `evaluator_fault_model.v3.py`
  - `evaluator-fault-observation.schema.v3.json`
  - evaluator3 common and command-envelope schemas
  - `workflow_projection_model.v3.py`
- **Immutability.** The successor, both root proposals, the root final38 reference, and my v1 (25,832 files) and v2 (38,825 files) runtimes all re-hashed equal to their snapshots after the work.

## Findings

### SI-1: the name-based SEAL catch let my typed replay mismatch escape (resolved by root's correction)

**Failure.** The root final38 `analysis-seal` child exited 1:
- For the reminted, semantically false Run, identity `close_run` raised `CompleteReplayMismatch`.
- The adapter matched only the names `AdmissionError`, `EvidenceUnavailable` and `RegenerationMismatch`, so the exception escaped.

**Reproduction on copies here:**
- On root's before-bytes, check-analysis-seal-adapter exits 1 at the same case.
- On root's after-bytes, it exits 0 with 16 of 16 passing.

**Own process finding.** My v1/v2 caller search covered `close_run` callers in foundation, workflows and native, but not security. So this adapter was outside my v2 regression set.

### SI-2: lawful refusals versus host faults over real `close_run` paths (no misrouting after the correction)

This probe is new here; it drives actual `close_run` outcomes through `admit_analysis_seal`:

| Case | Before-bytes | After-bytes (root correction) |
|---|---|---|
| Lawful full Run; again after restore | ADMIT | ADMIT |
| Reminted semantically false Run | **PROPAGATED** `CompleteReplayMismatch` (the root failure) | REJECT `SEAL_CLOSE_RUN_REFUSED:EVALUATOR_COMPLETE_PROOF_REPLAY`, cause exactly `IM.CompleteReplayMismatch` |
| Structural `REFERENCE_IDENTITY` | REJECT | REJECT, cause `IM.C.AdmissionError` |
| Corrupt blob `BLOB_DIGEST` | REJECT | REJECT, cause `IM.C.AdmissionError` |
| Missing proof object | REJECT | REJECT, cause `IM.EvidenceUnavailable` |
| Declared atom owner refusal inside the replay stack | REJECT | REJECT (normalized; inner `AtomAdmissionError`) |
| Undeclared same-named `AdmissionError` class inside the stack | **REJECT (misrouted by name)** | PROPAGATED |
| `RuntimeError` carrying an owner key / `TypeError` in the comparison | PROPAGATED | PROPAGATED |

- `IM` is the security loader's own identity copy.
- `close_run` converts its separately loaded replay stack's declared outcomes into `IM` classes.
- So `except IM.C.AdmissionError` is the exact-identity boundary for every declared owner refusal.
- The correction also fixes a latent opposite misroute: under name matching, a foreign class named `AdmissionError` was treated as an owner refusal.

### SI-3: the SEAL boundary does not impose the retained-regeneration route at a live host

**What the adapter emits.** `admit_analysis_seal` raises only the security-local `Reject` key.
- `Reject` carries no termination.
- `SEAL_CLOSE_RUN_REFUSED` has no D9 or public-detail mapping.

**What the outer host still decides.** The chained cause is the origin-free identity condition (`CompleteReplayMismatch`), not the retained `RegenerationMismatch` carrier. So the outer host keeps the origin decision: a live first-party contradiction takes `complete-replay-mismatch:host-internal`.

**Other paths.** `EvidenceStore.prepare` and `run_termination_model.retained_population` also propagate the condition uncarried. Only retained `restore` maps it to `RegenerationMismatch`.

**Advisory SI-A1.** An outer host projection must select by the `Reject.__cause__` type, never by parsing the diagnostic text embedded in the key. No outer live-host projection exists in the files reviewed.

### SI-4: no remaining downstream dependency on the changed class names

**Corrected.** `admit_analysis_seal`.

**Unaffected, with reasons:**
- **Security `admit_journal_record` name match (line 1481):** it wraps JournalRecord schema validation, not `close_run`.
- **Atom `_is_owner_admission` name match:** it handles exceptions from native `subject_scope_commitment`, which uses the historical identity model.
- **`check-execution-replay` name assertions:** the normalized classes keep the names `EvidenceUnavailable` and `AdmissionError`.
- **No name matching at all:** the run-termination owner, the workflow projection adapter, identity cache-key admission and `prepare` all propagate.

**Intentional.** `restore`, and query `close_retained_run`, which routes by type.

### SI-5: the pin-gated security owner suite gives no post-correction case evidence yet (limitation)

`check-security-lifecycle.v1` exits 1 at its source-pin gate (`sourcePinsValid:false`). The stale pins are exactly the two corrected files, and no cases ran. That is neither a pass nor a regression.

It does not hide coverage of the change:
- None of the 22 security JSON case documents uses `model:analysis-seal`.
- The suite's own case text says complete analysis-SEAL cases live in the adapter checker.
- Root's final38 security group passed on the before-bytes.

### QF-1: the QF-I1 remedy keeps both protections

The corrected checker runs 41 rows and passes. A discrimination probe against the unmodified production model shows each protection separately:

| Mutated envelope | Schema alone | Owner `validate_envelope` |
|---|---|---|
| Illegal pair (provider-protocol, `HOST.IO_FAILURE`) | REFUSE: `ValidationError`, `anyOf` at `/termination` | Same schema error |
| Legal but wrong pair (host-io, `HOST.IO_FAILURE`) | **ADMIT** | REFUSE `EVALUATOR_FAULT_ENVELOPE_PARITY` |
| Exit mismatch / public-detail mismatch | ADMIT | REFUSE `EVALUATOR_FAULT_ENVELOPE_PARITY` |
| Lawful envelope | — | ADMIT |

- Schema validation still runs before parity.
- The production bytes are unchanged, so no production law was weakened.
- Root's separate controls are better than either alternative I had suggested.
- Optional nit: the illegal-pair assertion (`anyOf` at `/termination`) would also match other termination `anyOf` failures. It is adequate for this single-field mutation.

## Qualification of the v2 sentence (v2 left unedited)

v2 said "close_run refusal messages and class names are unchanged". Precisely:

**Unchanged:**
- admission decisions and diagnostic message keys
- class names for structural, digest, join and execution-input refusals (`AdmissionError`)
- class names for promised-byte loss (`EvidenceUnavailable`)

**Intentionally changed:**
- Complete replay disagreement now raises `CompleteReplayMismatch`; previously the replay stack's `AdmissionError` escaped.
- Every `close_run` refusal is now a class object of the caller's identity copy, not of the replay stack copy.
- The public graph query routes that case to `evidence.regeneration-mismatch` (previously `evidence.corrupt`).
- `restore` raises `RegenerationMismatch`.

v2's comparison of 11 owners with byte-identical output did not include the security analysis-seal adapter, which depended on class names.

## Focused runs (foreground, pinned interpreter `-I -B`; every run left its tree unchanged)

| Run | Tree | Exit | Result |
|---|---|---|---|
| check-analysis-seal-adapter.v1 | integrated | 0 | 16/16 |
| check-analysis-seal-adapter.v1 | seal-before | **1** | reproduces the root final38 failure |
| check-security-lifecycle.v1 | integrated | **1** | pin gate only; exactly the 2 stale files; no cases run |
| check-evaluator-faults.v3 | integrated | 0 | 41 |
| check-query-projection.v3 | integrated | 0 | 193/0 |
| probe_seal_boundary | integrated / seal-before | 0 / 0 | table above |
| probe_fault_parity | integrated | 0 | all three verdicts true |
| setup38 snapshot / verify | read-only inputs | 0 | copies exact; inputs unchanged |

## Limitations

- Everything here is reference models and synthetic fixtures; no product host, outer live-host projection or store exists.
- Host-defect cases are in-process monkeypatches.
- The full evaluator3 six-group suite was not rerun here; root's final38 results are evidence only.
- Pins remain stale for the two SEAL files.
