This resumed delta review of author06 comes to **changes required**: three required findings, none blocking. It covers only the proposed carrier, joins and owner clarifications. All 11 report-feature design blockers, AUDIT-G10, RP-OBL-C01/C02/K01/P01/L01 and RP-DO-12 stay open.

**Custody:**
- Before and after review, the outer manifest (`3b3153ce…`), inner manifest (`3b7bdc8b…`, 19 listed) and envelope5 (`45de2b0a…`) SHAs match, with all 20 files as an exact set.
- All 82 pins and 3 listings hash correctly; versus author05, 3 pins were added and none changed.
- My closure copy is unchanged and there's no `__pycache__`.
- Root's retained validation under `docs/.../trials/report-projection-06` matches the mutable origin byte for byte, including the wrong-cwd stderr.

**Strict check:** run from the exact copy (with the copy as cwd), it exits 0. It reproduces 184 report cases (28 accepted), 31 envelope, 43 metadata, 22 aggregate, 64 delivered goldens across 16 scenarios, 8 pending, 17 static parity, 323 coverage rows and a document cap of 27,828,318. The contract states 28 accepts; root's summary didn't give an accept count.

**Root's first run did not pass.**
- From the architecture cwd, `bytecode_demo` cleanup opens `__pycache__` relative to a directory fd. The audit event carries no fd, so the hook resolves the name against cwd and refuses it as `UNPINNED-LOAD <arch>/__pycache__`.
- I reproduced this: from a governed cwd the check fails and leaves its scratch directory behind, while from `/` or the copy it passes.
- So the check only works when cwd is the subject copy or outside the governed roots, and the contract doesn't say so.

**Review05 findings:**
- **RPR5-1 (aggregate switch): closed, apart from RPR6-3 below.**
  - My regenerated relabel attacks are refused in all 6 bases: plain relabels get `J-LEDGER-DAG`, and relabels with dropped edges get `J-LEDGER-PLAN`.
  - Eight new mutants are all refused (plan, run and mode joins), and the analyze ephemeral control is still accepted.
  - The bound default and audit shapes match the owner's `workflow-cases` invocation cases.
  - The stated limitation holds: `validate_dag` ran on role-bound params only, and the missing required params are listed.
- **RPR5-2 (page law): closed.** I ran the owner query model myself:
  - Over 100,001 facts, pages 1 and 2 are contiguous, lower-bound, truncated-page at 100000/100000 with no reset. The page at position 99,900 is truncated-bound with no cursor.
  - Out-of-prefix, foreign and malformed cursors are all refused.
  - A visited-cap reach walk and an exact multi-page walk are lawful.
  - Every owner page passes the report's page law, and the correction's before-texts match the pinned lines.
- **RPR5-3 (interruption errors): closed, apart from RPR6-2 below.** Exact ordered real details are accepted; omitted, duplicated, reversed and no-ledger cases are refused, and an earlier indeterminate detail is excluded. This matches interruption04's join. The empty form is still pending.

**Findings**
- **RPR6-1 (required): the hook misattributes fd-relative opens.**
  - It caused root's failed run, and it also lets content through: with cwd `/` and an fd on the architecture's non-governed parent directory, a relative open reads the unpinned mutable `docs/implementation/README.md` (8,763 B).
  - It also falsely refuses non-governed targets when cwd is governed.
  - Fix: treat relative-path events as unattributable, clean up scratch another way, and state or remove the cwd requirement.
- **RPR6-2 (required): a fake detail on a skipped step gets laundered into accepted errors.** `recorded_failure_details` doesn't exclude skipped steps. With a fabricated detail on the skipped query, `errors` of `[CONFIG.INVALID, fabricated]` is accepted and `[CONFIG.INVALID]` alone is refused. The author's case only tests the omission. Interruption04's filter has the same gap.
- **RPR6-3 (required): the planning record isn't complete.**
  - Workflows prose lists `analyze --baseline` and the report schema requires an analyze comparison panel, but no analyze variant plans a comparison and no obligation records the conflict.
  - The owner exercises an optional `export-delivery` step and the subject's own goldens use optional renders, yet no variant covers either.
  - repair-preview binds `evidenceSource` as the label `"runId"`, which is invalid against the owner schema.
  - P01 being non-blocking is supported by owner evidence, but whether analyze import is in M1 scope needs an explicit root decision.

**Advisories (5):**
- **A1:** the C01/C02 register entries point to superseded parents (envelope subject-01, successor03) rather than interruption04; their pending standing is honest.
- **A2:** the corrected query fixture keeps `visitedNodes 4` on neighbor rows, while the owner model gives 1.
- **A3:** the planning evidence covers binding params only, not full StepSpec admission.
- **A4:** K01 (root coverage correction01 still under review) and L01 are correctly pending.
- **A5:** RP-DO-03/05/09/10/11 are being authored separately and remain blockers here.

**Not tested:** no full retained-Run query replay or full StepSpec/`run_invocation` replay. I verified the scratch-alias fix by reading the code, not by re-probing. Hard links, native extensions and races stay outside the claim. I read interruption04 only for its join rule and manifest. No browser, UI, M1, performance or release claim.

Everything is in `m1-report-projection-review-06/`: `review.json`, `review.md`, `work/probes/` and `work/after-verification.json`. Nothing was committed or pushed.
