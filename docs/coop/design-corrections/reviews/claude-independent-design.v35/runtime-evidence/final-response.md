I accept source35: the verdict is **ACCEPT**, covering only the design and reference bytes. **MUST-34-01 is closed, A-12 is closed**, and there is no new MUST or SHOULD. One new advisory, **A-13**, records a pre-existing path in the reference code that retained Runs can't reach. This grants no application outcome, readiness, qualification, or package or blind acceptance. The separate application review still has to happen, and this reviewer can't satisfy it.

All writes stayed in this runtime; source, prior reports and the live repo were read-only, and frozen35 showed no drift after every run.
- `review.json`: sha256 `d7dc035c532968df80334809815f1257a49b83fd47f880e3a89630df9669cd52`
- `review.md`: sha256 `687ed3dda5c07e7f8def8e824aff7c135a5cca9a1d91d8705e36bfff010d5a7b`
- 67 consistency checks over the report pass.

**Custody:** all 12,899 files (736,823,249 bytes) match the manifest, the archive equals it, and the parent is the source34 I reviewed. My delta from the two manifests is 10 changed files, matching root's inventory. Four carry substance (contract §4, `atom_model`, `check-atoms`, and a metadata-only line in `incoming-search.schema`); six only update pins. I tested the final bytes, including root's three edits made after the author finished.

**MUST-34-01 closed.** All controls below are my own and run at the synthetic atom API, compared against frozen34:
- I wrote a predictor from the new §4 prose. It matches the actual answer on all 192 matrix cases.
- No incoming "none"/"exists false" answer appears unless the subject's own program has an available binding.
- Outgoing results and the no-binding case are unchanged from source34 on all 48 outgoing cases.
- Everything that changed from source34 is the new guard: 92 cases, 28 of them value changes.
- Known matches still decide the answer. With the subject's program unbound, a count bound of 1 is still false, while a bound of 2 or 3 becomes unknown.
- Results don't depend on order: 240, 1,440 and 240 orderings each gave one result.

None of this touches a real Run: package12's retained Runs contain no incoming atoms. Whether product configuration can actually express per-unit narrowing is still unestablished, but the law no longer depends on it.

**A-12 closed.**
- Scope-less provider groups can't hold an attestation. An empty `scopeRefs` is rejected at schema; a borrowed or nonexistent one is rejected as a scope misjoin. Both reject the whole input set.
- An explicit empty-subject scope closes an empty program only with complete Coverage or a qualifying attestation, and it can't hide real inventoried subjects.
- Missing-key carrier bypass: I tested all 8 required scope fields, absent and null, on 4 consumption paths. The 18 frozen34 cases that used a malformed scope as evidence now refuse.

**A-13 (advisory, found by me, same behaviour on source34):**
- **What happens:** when no exact dependency scope exists, the dependency mapping fallback in `_select_dep_coverages` still accepts a scope whose relation, resolution or source universe is missing or wrong. It turns a reachability answer into true.
- **Why it's only advisory:** retained Runs can't reach it, because `close_run` re-validates every Coverage against its retained scope. It is still looser than the new §4 sentence says.

**Verification:**
- Suites all pass: check-atoms 89/89, evaluator3 launcher 16/16 with pins valid, foundation, integration, native 375/375, security, workflows, and both planning checks.
- The ordering determinism I relied on for source34 still holds after re-running it on the changed scope-pairing path.
- Layer4 is kept: its 29 inputs are unchanged.
- Package12: 317/317 members verify, and all 13 exports are byte-identical to package11. All 13 cases pass through both `open_run_closure` and `close_run`, and all 7 queries pass.

**The 107 rows:**
- 91 are inherited on exact bytes, 11 F rows are re-verified on package12, and 5 carry changed-law consequences. AR-12 and FW-08 are restored now that the MUST is closed; FW-06, DR-009 and AR-16 still hold, re-measured on source35.
- All nine legacy reading-standing corrections are kept.
- I added correction **C35-01** to my own source34 record. It said a scope without `enumeratorClosure` is refused once it's paired, but that only held for null. An absent key skipped the check on source34.
- Unchanged: 28 condition-2 obligations, 32 gates with condition 5 NOT MET, 54 unexecuted recovery cases, TCB-SCOPE-01 over 13 rows, D9 on DR-007/DR-011-R08, and all 30 author proposals PENDING. Every row has both authority flags false.

**My own mistakes, kept on the record:**
- An outgoing predictor wrongly treated a non-blocking disclosure as blocking.
- Two checks were framed too strictly, and I recomputed them from the same receipt.
- I first wrote the ordering counts in my probe-error note wrongly; the consistency checks caught it before finishing.

**Still open, outside this review:** A-13 is advisory. Also open: the residual grades, gates, recovery cases, TCB-SCOPE-01, D9, blind reconstruction, closed enumeration and retained-Run reach of the incoming law, and the application review.
