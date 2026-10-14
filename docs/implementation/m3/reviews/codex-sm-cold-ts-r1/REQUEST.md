# Review request: SM-COLD-TS-r1 (U-5a)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-sm-cold-ts-r1/`).

## Boundaries

Do not edit either repository, the stage, the working directory or control files. Do not run Node, the compiler, Cargo, any runner, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Permitted:
- read-only file reading, hashing, JSON parsing and Git queries;
- reading the archive members without extracting them to a shared location;
- re-running the read-only audit `nice -n 10 python3 -I -B /tmp/opensip-implementation/sm-cold-ts-2026-10-13/audit_cold_ts.py`, which must reproduce `cold-ts-checks.json` byte for byte.

## Subject

- **Stage.** `/tmp/opensip-implementation/sm-cold-ts-r1-stage`
- **Subject file.** `subject.json`: 137997 bytes, SHA-256 `6d04c3812e79538a1a94e97468adcb016d17679853995946be15c219ff3d0a21`, 607 members. Rehash every member.
- **Bases.** Product `95279fa8ae086f98bd221cd827f6c0efc156c0c5` (clean); architecture `32b4ba9bdd352c41e28d3761a3e53c49b0ebea3c`.
- **Authority.**
  - PLAN-r2, D-7 and U-5 (your `codex-s-m-report-plan-r2`).
  - Q0 §9.2 (`docs/implementation/m3/harness/DESIGN.md:796-807`).
  - The accepted component spikes named in each `ACCEPTED-RUNNER-SOURCE`.

## What to review

1. **The reset.**
   - Does `cold_reset.py` implement §9.2's cold reset: OpenSIP state deleted or absent, disposable caches deleted, a new process, and the page-cache state recorded and never claimed flushed?
   - Is the fresh per-run TMPDIR a sound reading of "the disposable analyzer caches"?
2. **Placement.**
   - In every cold runner, is the reset the first statement of the measured loop, before any timestamp?
   - Is it called once per child, warmups included?
   - Is the transfer control launch outside the loop correctly left alone?
3. **The diffs.** Each cold runner against its accepted runner. Confirm:
   - only the stated insertions are present, plus the replay size restriction and output redirect;
   - no recipe, input, bound or pin is changed.
4. **Records and series.** Check:
   - one record per child, in order;
   - medians and maxima recomputed;
   - the replay children replay fully with `findings == count`;
   - the retained attempt 0 and its cause.
5. **The archive.** Members against `raw-evidence-index.json`.
6. **Scope.** No F, T, outcome or placeholder. The warm column is information only.

O7, D3 and D13 are closed, and only L-G1 remains open.

## Output

`review.json` must carry:
- `verdict` (`ACCEPT` or `REQUIRED-FINDINGS`);
- `requiredFindings` (array);
- `nonBlockingObservations` (array);
- exactly these expected fields, with your independently checked values. Report the actual value, and raise a finding if any differs:

```json
{
  "verdict": "ACCEPT",
  "requiredFindings": [],
  "subjectManifestSha256": "6d04c3812e79538a1a94e97468adcb016d17679853995946be15c219ff3d0a21",
  "coldResetMatchesQ0": true,
  "resetBeforeEveryRunUntimed": true,
  "allDiffsConfined": true,
  "oneResetRecordPerChild": true,
  "pageCacheRecordedNotFlushed": true,
  "recipesOtherwiseUnchanged": true,
  "attempt0Retained": true,
  "archiveMatchesIndex": true,
  "FComputed": false,
  "TComputed": false,
  "outcomeRecorded": false,
  "placeholderFilled": false,
  "SMComplete": false,
  "LG1Met": false,
  "effectiveL": false,
  "productQualification": false
}
```

The lead will then give its own exact assent and run fresh design verification before an architecture-only publication. Nothing is pushed.
