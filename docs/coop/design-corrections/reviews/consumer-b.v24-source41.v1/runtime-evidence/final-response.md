The verdict for source41 is **ACCEPT-RECONSTRUCTABLE**, with no MUST or SHOULD issues. All 123 requirements and 8 standing rules were executed with none failed, and the verdict is derived from those results by `tools/finalize_review.py`. Root admission of the exported bytes is a separate gate that I haven't seen, and nothing in this review claims product qualification or acceptance.

**Kit custody.**
- The manifest (`31369cc8…`, parent `eb7a4c48…`, 104 members) verified at the start and again at the end.
- Compared with my source39 rows, exactly five documents changed. I read all five in full, plus the charter and requirements.

**How I got there.**
- I ported my own source39.v3 helpers and ran them unchanged against source41 first. That whole state is preserved (`preserved/s41-original-state/`) and can be re-run from `preserved/pre-s41/`.
- I corrected helpers only from the kit or from errors in my own tools, as HC-39 to HC-46, keeping each original failure:
  - **HC-39:** three native laws my helper didn't implement: the TS/JS `unitKind` rule, mode selection from the effective `allowJs`, and the U-0 unit-root check. With the unchanged helper, the source39 s39-M1 alternative spelling passed every check.
  - **HC-40:** a phase-6 vector still spelled the old universe flags; no result depended on it.
  - **HC-41:** the non-object termination key is now published, so it replaces my own `cb24.` name.
  - **HC-42:** execution-inputs §3 view attribution was not derived. Over the unchanged helpers' own bytes, the corrected closure refuses four syntax positives with `EXECUTION_INPUTS_VIEW_TOTALITY:1:0`. My first version of this fix also broke two vector tools, and a mock vector lacked `relation`; both were fixed and re-run.
  - **HC-43, HC-44:** custody tools asserted source39 hashes, and the negatives' "pre" column pointed at a source39 copy that isn't in this runtime.
  - **HC-45, HC-46:** my first omitted-view control built no mutation and admitted, and my phase-11 check compared the review against the interim verdict.
- After the last change I rebuilt every store and re-ran every closure-dependent result (logs `s41-fin-*`).

**Results.**
- **Positives:** all 27 claimed complete positives pass owning-schema admission including kit keywords, owner joins, the independent retained-closure walk, and replay with byte-equal proofs and reachable-set equality. Exports are `runs/<run>.store.json`; the run IDs are in `blind-review.md`.
- **Negatives and controls:** the designed negative refuses, all 32 retention negatives pass, and all four new source41 controls refuse under the corrected code. The unchanged helpers admitted two of those four.
- **Mutations:** of 66 mutation stores, 29 admit (the 27 positives plus two lawful controls) and 37 refuse.
- **Vectors:** 0 failures across discovery (29), run termination (28 Runs), graph query (53) and phases 1–8.

**Issues.**
- **s39-M1 is resolved by the kit**, and I measured it: native U-4b.2 and U-4b.5 now fix the TS/JS unit kind, so the old alternative spelling refuses.
- **Resolved by the kit:** A-n2 through A-n5.
- **Carried or new advisories (nonblocking):** A-c1–3, A-n1, A-n6, A-v2-1–3, plus two new wording notes:
  - **A-s41-1:** §7.6 step 1 names no key for a non-object candidate.
  - **A-s41-2:** U-1's "defaults to false" clause reads against §1.2's `checkJs` fallback.
- **A-n6 re-examined:** a Rust unit's mode is fixed by the mode table, but no retained-record enforcement is published for it.
- **Not exercised:** PolicyTestSuiteV2 (changed in source41) and the U-8 boundary-inventory join. No original requirement constructs either.

Everything is under `output/`: `blind-review.md` and `.json`, `requirement-status.json`, checkpoints 0–11 (all clean), notes and logs. No subprocess is still running.
