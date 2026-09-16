**Verdict: accept-conditional.** Correction02 works as a design/reference fix but isn't ready to select, and this is not a promotion. The envelope6 schema is byte-identical to subject01 and keeps its earlier conditional acceptance. It also stays conditional on envelope5, which is still an unaccepted report04 candidate. Nothing here implies the report is ready. The review is in `review.json` and `review.md` in the review-02 directory.

**Custody:**
- The manifest SHA matches. The 46 files match exactly on the original and on my copy, both before and after.
- All 37 input pins match their source files.
- Compared with subject01: 35 files are unchanged, 5 changed and 6 were added.
- Root `check.py` exits 0 from my copy (reference environment, `-I -B`, own TMPDIR) and its output equals `root-result.json` (42 / 27 / 43, plus the prose check). I wrote only inside the review directory.

**My earlier findings:**
- **F1 fixed:** the exact prose override is checked against the pinned text, and the metadata exception is kept.
- **F2 fixed as a reference join.**
- **F3 withdrawn; my premise was wrong.** `candidates`, `inspect` and `review-brief` are query+render only, and owner text says "A query never commits a Run" (:1211). A historical Run in query parameters is correctly treated as an input, not a commit.
- **F4 fixed:** I also confirmed that valid `invocation`, `run`, `findings`, `availability` and `advisoryReport` payloads are refused on the new form.
- **F5 maintained.**

**My own tests (`work/probes.py`, 36 rows, all as expected):**
- **Against the owner model:** I ran the pinned `run_invocation` over 46 ledgers covering default, fit, a two-analysis workflow and candidates, at every cancel point and signal. The join accepts all 46: 15 use the new form, 12 are after-settle and keep their settled class.
- **Refused as they should be:**
  - erasing a committed Run, with both shapes valid;
  - substituting an earlier Run, even when record and envelope both name it;
  - phase or signal mismatches;
  - relabelling or reclassifying an after-settle ledger.
- **Admitted, which these findings cover:** one ledger where the cancellation signals don't match, and one where a render completes after a cancelled step. The owner model can produce neither.

**Remaining findings:**
- **F-A (medium, blocks the prose):** the override says the form applies when there is "no earlier committed Run". But the rule it adopts, in both the model and the join, only looks at required steps. A Run committed by an optional step ends up as the empty failure form with no Run named. The owner has to decide which is intended.
- **F-B (medium, blocks the host duty):** your challenge holds. The join relies on invocation-record checks that no pinned owner implements:
  - cancelled steps always carry the interrupted termination with the same signal;
  - every step after a cancellation is itself cancelled;
  - result kind matches step kind; a query step carrying an `AnalysisResult` is schema-valid and would count as a commit.

  A malformed record also fails with an untyped `KeyError`. Those prerequisites need to be named as host duties or folded into the join.
- **F-C (low-medium):** when no Run was committed, the join doesn't check which output form is used. It accepts an unrelated made-up error detail, a query result for a query that was cancelled, and an invocation carrier holding a different record. So the contract's "no invented detail or completion" isn't enforced.
- **F-D (low-medium):** a signal before planning has no invocation record to check against, since a record needs at least one step. Yet the new prose makes the check mandatory. Report04's ledger also allows unrecorded steps, which the join refuses.

After-settle behaviour matches the owner model. I'm not claiming anything about live signals, delivery, browser, source integration or host custody.
