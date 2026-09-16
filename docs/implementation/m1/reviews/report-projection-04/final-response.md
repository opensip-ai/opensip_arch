Author04 still needs changes before the carrier unit (the fit carrier, report ledger/panels/codec/bounds and delivery goldens) can be accepted: one blocking finding and two required. The report design stays blocked on the 11 design blockers, and AUDIT-G10 and RP-OBL-C01 stay open. I don't treat the obligation register as delivered features.

**Integrity:** before and after the review, the outer manifest SHA (`5e43e1a1…9e317b20e`) and inner SHA (`c66c1e34…a39a37`) match. All 18 files match and the set is exact. All 79 pins and both listings still hash correctly. My closure copy is unchanged, and neither directory has a `__pycache__`.

**Strict check:** run from a copy of only the declared files (own `TMPDIR`, `-I -B`, fresh `-X pycache_prefix`, `--out` outside the copy), it exited 0 and reproduced every root count. That is 146/25 report, 22 envelope, 43 metadata, 14 D9 cases, 28 delivery goldens, 323 coverage rows, 79 pins/2 listings, 20 compiles, 1421 re-hashed opens and 0 child processes.

**What I reproduced independently**
- **Byte bounds:** I built my own maximal owner-valid step termination at 6,471,125 B; it is under the author's 6,476,835 B bound.
  - A maximal audit document of 25,524,326 B is accepted, with the envelope at the 4 MiB limit, a 17.1 MB ledger and panels filling the 4 MiB remaining budget. One more evidence entry is refused `J-BUDGET-BYTES`.
- **D9 and cancellation:** my own implementation, written from the workflows text, matches all 14 aggregate cases and all 28 goldens.
  - Every format keeps the original step terminations separate from the aggregate.
  - A required renderer failure outranks a query refusal, with no report-specific exception.
  - On an interrupt before all steps finish, the run chosen matches the owner reference model.
  - Any requested cancellation inside a delivered report is refused.
- **Closure:** a whole-process trace shows no unpinned governed reads, no child processes and no architecture `.pyc` opens. The declared `--out` is written and never read.
  - My proof-of-concept with a forged but header-valid `.pyc` for the real pinned `canonical.py` runs under the stock loader but not the enforced one.
  - Unpinned copies, bytecode-only modules, undeclared writes, subprocesses, and pin or listing drift at use are all refused.
- **Coverage:** applying only the recorded `assets.rs`→M1 fix, base and overlay both pass the full owned validator. Reverting the old `fit` parity fields fails independently with "Command metadata drift".
- **metadata-v2:** all 10 files equal the accepted subject's bytes.

**Findings**
- **RPR4-1 (blocking):** the page law never checks `producedItems` against `totalItems` or the embedded rows, so pages the context proves were cut are still admitted. The owner law requires completeness to be `complete` plus `exact`, and a lower-bound total to be the produced prefix.
  - A slice labelled `complete-page-set` with 1 row but 1000 produced is accepted.
  - Two truncated-bound slices with no cursor are accepted: one claims produced at the 100000 cap with total forged to 1, the other reaches the visited cap with 50 produced but 1 embedded.
- **RPR4-2 (required):** the D9 aggregate counts skipped required steps. The pinned owner reference model excludes them (`workflows_model.v1.py:385-388`). With an analysis success and a skipped query, the subject gives `request-rejected` where the owner rule gives `success`.
- **RPR4-3 (required):** the RP-OBL-C01 gap is real and predates this candidate. An interruption before any committed Run has no admissible failure envelope in envelope4 or envelope5, unless the emitter invents an unrelated detail code, which both schemas accept. It is recorded only in the contract and fixtures, not in the register, coverage review issues or goldens, so integration could pass coverage without it.

**Advisories (9):** the ones that matter most:
- **A1:** a case-variant path (`OPENSIP_ARCH`) reads an unpinned file past the closure hook. The checker never uses such a path, but the enforcement can be bypassed.
- **A2:** `tempfile.gettempdir()` writes a probe file into `TMPDIR` before the hook is installed. The summary also reports `declaredOutWrites: 0` even though `--out` was written.
- **A3:** my maximal termination is refused by the owner's 4 MiB canonical codec. If invocation records go through that codec, the 27.8 MB bound is far above anything reachable; the owner should say which applies.
- **A4:** the static section doesn't mark `graphUnresolvedSubjects` as host-asserted, unlike the history count. The document can't prove what the host retained, so browser admission shouldn't present internal checks as proof.

The rest cover the R05 coverage row and conditional RP-DO-02, the M1 workaround value, the register's standing with other owners, RP-DO-12 still being open, and the generator not having been run.

**Not tested:** no browser, renderer, generator, performance or release work. The probes use the subject's mock graph owner. I only tried case-variant aliases, not symlinks, because I couldn't write outside the review directory. I didn't attempt `fork` or concurrent-writer races.

Everything is in `m1-report-projection-review-04/`; nothing was committed or pushed.

Files are in `m1-report-projection-review-04/`:
- review.json
- review.md
- work/probes/
- work/after-verification.json
