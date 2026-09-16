Author05 still needs changes before the carrier unit can be accepted: one blocking finding and two required. This covers only the narrow carrier unit. The 11 report-feature design blockers, AUDIT-G10, RP-OBL-C01/K01/L01 and RP-DO-12 all stay open. Root's check is still running, so nothing here counts as its success.

**Custody:** before and after review, the outer manifest (`a9f6c22a…de2a4`), inner manifest (`0d6a4154…f45dbf`) and envelope5 (`45de2b0a…`) SHAs match. All 18 files are an exact set, all 79 pins and 2 listings re-hash with no drift, my closure copy is unchanged, and there's no `__pycache__`.

**Strict check:** run from my 18-file copy (own `TMPDIR`, `-I -B`, fresh pycache prefix), it exited 0 and printed `declared-out writes observed: 1`. It reproduced 162/27 report, 22 envelope, 22 aggregate, 48 delivery, 8 pending, 16 static-parity, 79 pins/2 listings, 0 child processes.

**Review04 findings:**
- **RPR4-1 (page law): closed**, apart from RPR5-2 below.
  - My own oracle produced lawful multi-page exact, capped, exactly-at-cap, single and empty sets.
  - Of 132 context mutants, every contradiction is refused. The only accepted mutants are relabels the host could assert and no document can prove.
- **RPR4-2 (skipped steps): closed**, apart from RPR5-1 below. I actually ran the owner reference model (`run_invocation`) on 6 fit scenarios. The subject's aggregate agrees 6/6, and every owner skip record passes `J-LEDGER-SKIPPED`.
- **RPR4-3 (RP-OBL-C01): now properly tracked**, apart from RPR5-3 below. It is in the register, on 13 coverage rows, and has 8 pending goldens not counted as delivered. Envelope6 is not adopted.
- **Advisories:**
  - **Closed:**
    - **A1:** case-variant, symlink and out-alias paths are refused, and a forged cache is ignored.
    - **A2:** my trace shows no `TMPDIR` access before pin checks and `--out` written but never read.
    - **A4, A5, A7:** closed.
  - **Moved to obligations:** A3 as L01 (correctly non-blocking) and A6 as K01, which is a necessary coverage-owner duty and not a feature waiver.
  - **Still open:** A8 (RP-DO-12) and A9 (generator not run).

**Findings**
- **RPR5-1 (blocking): a failed invocation can be shown as success.** Step `requirement` and `dependsOn` come from the host and are never checked against the owner's rule that required steps can't depend on optional ones, nor against any builtin step spec.
  - In all 6 bases with a failed required step, relabelling it `optional` switches the aggregate to success, and the document is accepted.
  - Even after also dropping the dependency edges, so the generic rule is satisfied, 4 switches are still accepted.
- **RPR5-2 (required): the page law rejects an owner-valid page shape.** The owner's reference model has a positive lower-bound page with total and produced both 2, a cursor, and no cap reached. The subject's law refuses it, and the same shape as a report's first graph page refuses the whole document (`J-GRAPH-COUNT`), so required delivery would fail. Accepting it wouldn't hide a cut, since the cursor still discloses more rows. The query owner needs to state which reading of `producedItems` is correct.
- **RPR5-3 (required): `J-ENV-INTERRUPTION-DETAIL` is too broad.** It refuses any `errors` beside an interrupted failure, including real earlier step details. I ran the owner model: analysis rejected with `CONFIG.INVALID`, then SIGINT, gives an interrupted aggregate. An envelope carrying that real recorded detail is valid under envelope5 but refused. This contradicts owner prose and root correction02's stated preservation of real earlier details. Kind=run interruptions are unaffected.

**Advisories (7):**
- **A1:** a symlink inside the active scratch directory can read an unpinned file.
- **A2:** the page law doesn't bind cursor position itself, and some relabels can't be proven either way.
- **A3:** L01/K01 standing is appropriate.
- **A4:** once RPR5-3 is fixed, tie the invented-detail pending golden to the ledger.
- **A5:** profile workflows weren't exercised.
- **A6:** hard links, native modules and races are outside the stated trust claim.
- **A7:** RP-DO-12 and the generator remain open.

**Not tested:** my owner-model runs covered only fit-shaped records I wrote. Graph probes used the subject's mock owner, not the product engine. I don't decide the eager-versus-lazy `producedItems` question, only that the subject refuses the owner's positive fixture. There's no browser, runtime or release claim. Correction02 I read only for its error-form policy.

Everything is in `m1-report-projection-review-05/` (`review.json`, `review.md`, `work/`, including `work/after-verification.json`); nothing was committed or pushed.
