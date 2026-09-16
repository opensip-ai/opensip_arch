Candidate03 still needs changes. There are six findings: two blocking and four required. The candidate itself passes its own strict check. The files are intact before and after review: the manifest SHA `42144cde…fe118` matches, all 16 files match, and there are no extra files or `__pycache__`, in both the frozen subject and my closure copy.

The strict check (`check.py --architecture ARCH --subject-strict`) exited 0 from a copy of exactly the 16 files. My first attempt also passed `--out` pointing into `/tmp/opensip-implementation`; every check finished, then the checker's own audit hook refused to write the result file (advisory A3).

**Blocking**
- **RPR3-1 – a cut graph page is still admitted as complete.** I took a 100-row owner page, cut it to 1 row and relabelled it complete with `countBasis=lower-bound`. Admission accepted it as `complete-page-set`, because `check.py:434-436` only compares counts when the basis is `exact`. The owner law says complete requires exact (`query-projection-contract.v3.md:140`).
- **RPR3-2 – the budget does not bound the required root data.** The 917,504 B root allowance was derived from a placeholder (`build_owner.py:392`). A single owner-valid step termination can reach 4,193,710 B.
  - I built a failure report whose joins all hold and whose panels are only 323 B. It is refused `CODEC-BYTES` at 10,489,377 B, over the 9,306,112 B document cap.
  - With one large step instead of three, it is accepted.

**Required**
- **RPR3-3 – termination rules.**
  - The reference D9 aggregate lets a renderer failure replace a query refusal, which the root decision forbids; `contract.md:104` allows it and there is no golden.
  - An owner-valid `interrupted` step termination crashes admission with an uncaught `ValueError`.
  - The ledger leaves out cancellation, so the owned cancellation rules can't be recomputed.
- **RPR3-4 – the child checker bypasses the closure.** The historical metadata checker runs as a subprocess outside the audit hook (`check.py:899`).
  - My trace shows it opening 7 unpinned architecture files, one of them a `.pyc`, plus one unpinned directory listing.
  - A small demo shows that `-I -B` runs a matching stale `.pyc` instead of the hash-checked source. The architecture's `.pyc` files don't currently match, so this isn't live today. The parent process's closure is exact: 73 of 73 opens pinned.
- **RPR3-5 – the coverage overlay hides a real drift.**
  - The check only compares the validator's first error, which the base coverage already fails.
  - With that pre-existing condition set aside, the base is valid but the overlay fails `Command metadata drift`: its `fit` row lists 5 parity fields where inventory5 has 9.
- **RPR3-6 – F01–F10 have no way to close.**
  - These obligations have no owner, milestone, gate or retirement path, and the coverage rows count the "unavailable" state itself as delivery.
  - F03 and F05 are design decisions inside existing owners, not missing owners.
  - R03's required duration disappears with no feature state.

**Closure of RPR2 findings:**

| Finding | Status | Residual |
|---|---|---|
| RPR2-1 | Partly closed | RPR3-3 |
| RPR2-2 | Partly closed | RPR3-1 |
| RPR2-3 | Partly closed | RPR3-3, RPR3-6 |
| RPR2-4 | Mostly closed | Graph provenance overclaim until RPR3-1 is fixed |
| RPR2-5 | Partly closed | RPR3-4 |
| RPR2-6 | Closed | — |

**What checked out independently:**
- subject3 IDs match on all 517 index rows.
- All 13 static-parity goldens match.
- The four fit truncation/cursor/availability parity lines are present.
- u64 integer limits behave correctly.
- `--ephemeral` behaviour is unchanged.
- The metadata-v2 files are byte-identical to the accepted subject.

**Advisories (9):** among them, the host can steer slot and history selection through claims admission can't verify, and the documented `--out` usage fails as above.

**Untested:** no generator, browser, renderer or performance work was run. The probes use the subject's mock graph owner. The oversized pinned termination in RPR3-2 is schema-valid, but I haven't shown a real workflow that produces it.

Everything was written only under `m1-report-projection-review-03/`; nothing was committed or pushed.

Files are in `m1-report-projection-review-03/`:
- review.json
- review.md
- work/probes/
- work/after-verification.json
