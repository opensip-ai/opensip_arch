Both root corrections get **ACCEPT-CORRECTION**. That covers only these two corrections: it is not independent or source acceptance, and root still owns the pin rebind, final suites, freeze and independent review.

**SEAL adapter correction** (`security_lifecycle_model_v1.py` and its checker).
- **The failure was my v2 change.** The false Run now raises `CompleteReplayMismatch`, which the adapter's name list didn't include.
- **Reproduced.** The adapter checker fails at that case on root's before-bytes (exit 1) and passes 16 of 16 on the after-bytes.
- **No misrouting.** I pushed real `close_run` outcomes through `admit_analysis_seal`:
  - The lawful Run is admitted, and again after the test patches are restored.
  - Refused as SEAL refusals, each with its exact typed cause from the security loader's own identity copy: the reminted false Run, a structural mismatch, a corrupt blob, a missing proof object, and a declared atom refusal from inside the replay stack.
  - Propagated as host faults: a foreign class named `AdmissionError`, a `RuntimeError` carrying an owner key, and a `TypeError` inside the comparison.
- **It also fixes a second bug.** Under the old name matching, the foreign same-named class was treated as a lawful refusal.
- **Live-host boundary.** The adapter emits only a security-local refusal with no termination or public route, so it does not impose the retained-regeneration route. The chained cause is the origin-free condition, not the `RegenerationMismatch` carrier. The outer host still decides origin, e.g. host-internal for a live evaluator contradicting itself.
  - **Advisory:** that host must route by the cause type, not by parsing the diagnostic text in the refusal key. No such outer projection exists in the reviewed files.
- **No other caller depends on the changed class names.**
  - The two remaining name matches (security journal-record validation, and the atom model's native commitment check) don't wrap `close_run`.
  - `check-execution-replay`'s name assertions still hold.
  - The termination owner, the workflow projection adapter, identity cache-key admission and `EvidenceStore.prepare` propagate exceptions without matching names.
- **Security owner suite is blocked by stale pins.** `check-security-lifecycle.v1` exits 1 at its pin gate, flagging exactly the two corrected files, and runs no cases. That is not a pass and not a regression. None of its 22 case files uses analysis-seal, so it would not exercise the changed code anyway. Root needs to rebind the pins and rerun it.

**QF-I1 fault-check correction.** The corrected checker passes 41 rows. A probe against the unmodified production model shows both protections separately:
- The illegal pair is refused by the schema alone.
- The legal but wrong pair passes the schema and is refused only by the owner parity check.
- The exit-code and detail mismatches are still parity refusals, and the lawful envelope is admitted.

Schema validation still runs before parity, and the production fault files are byte-identical to source37, so no production law was weakened. Keeping the schema check and the parity check as separate controls is better than either alternative I had suggested.

**Correcting my v2 report (v2 left unedited).** v2 said `close_run` refusal "messages and class names are unchanged". Messages, decisions and diagnostic keys are unchanged, and so are the class names for structural, digest, join, execution-input and missing-bytes refusals. Four things changed on purpose:
- Replay disagreement now raises `CompleteReplayMismatch`.
- Every refusal is now a class from the caller's own identity copy.
- The graph query routes the false-Run case to `evidence.regeneration-mismatch` instead of `evidence.corrupt`.
- `restore` raises `RegenerationMismatch`.

My v2 caller search also left out security/, which is how this adapter was missed.

**Other checks.** The query checker passes 193 of 193 on the integrated copy. The successor source, both root proposals, root's final38 reference and my v1/v2 runtimes all re-hashed unchanged after the work. No processes are still running.

Files are in /private/tmp/opensip-design-corrections/claude-source38-seal-integration-assessment.v1:
- review.md
- review.json (sha `130986c0…`)
- receipts/runs/
