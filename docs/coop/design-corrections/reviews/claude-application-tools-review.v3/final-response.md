Bounded v3 review complete. `review.md` and `review.json` written; probe sources and results under `scratch/`.

## Verdict: TOOLING_REVIEW_PASS — G1–G4 scope only, never a final application ACCEPT, no grades

**Custody.** Manifest `7e1e0165…d47f` matches; all **26** files verified byte-exact. 6 changed, 20 unchanged, nothing new or removed. `check-retain-public.v1.py` and `freeze-application.py` read fully (the former for the first time in any of my reviews); the other four changed files rest on v2 full reads by this same origin plus the **complete, untruncated** diff against those exact bytes — I state that as a custody basis rather than calling it a fresh full read. All three inputs trees (v1, v2, v3) verified untouched afterwards.

**All four follow-ups implemented as described and independently verified.**

- **G1** — 60/60 helper matrix, 6/6 vendor guard, 12/12 end-to-end. The ordering is right: the stdout check runs *after* the vendor branch, so the Claude exemption **cannot** defeat the raw-stdout rule. Authored `summary.json`/`plan.json` now retained; all 15 other conservative names, and private directories at any component, still excluded for both vendors.
- **G2** — line 480 now reads the live root. I ran a differential using the assembler's own helpers: with the assent inside `accepted_files` and the snapshot differing, the v2 expression was snapshot-bound and insensitive to live-root mutation, while v3 catches the tamper. The line-124 pre-output guard still executes and governs.
- **G3** — 20/20, and in all 19 refusals **none** of the four freeze outputs appeared. Includes the sharp case: a report with a non-empty `failed` list is refused *even when its hash matches*.
- **G4** — 7/7 contract cases with **zero** files created on any refusal, including the fresh path supplied alongside the offending one, which is what actually proves refusal precedes execution. Re-measured independently: retain **69/0**, envelope **35/0**, IDs identical in set *and order* to my v2 run.

**Cohesion.** +33/−8 lines, 10 assertions added, 3 removed — all three exactly the intended in-place replacements. Test identifiers 79→79, none dropped. The fresh retain report is still byte-identical to the pinned historical digest, so adding required arguments preserved reproducibility of that evidence.

**Preserved failure.** I independently confirmed `preparation-failure.md`'s custody claim: all four finalizer copies are byte-identical and both support pins still match. That no process was launched is attested, not verifiable from these inputs.

**Two INFO observations, and I want to be clear they are not requirements.** H1: the retain suite reads one external absolute path that is neither manifested nor pinned, unlike the fixture v3 correctly bundled — I flag it only because it is the same class of dependency as F6, whose path really was missing. H2: needs a deliberate misconfiguration and needs no action. Neither blocks.

**Scope I did not perform, stated plainly:** G3 was a bounded guard execution on a synthetic stage, not an end-to-end freeze; G2's line-480 check was verified statically and by differential, not reached by execution; the assembler, `prepare-validation` and `verify-applied` again were not run end to end. The 69/35 counts are my own measurement — root's separate claim of 15 focused controls was not supplied to me and I neither confirm nor dispute it. All 32 product gates remain unperformed and condition 5 remains NOT MET.
