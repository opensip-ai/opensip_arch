# Bounded execution-account source-author runtime

Fresh actual-Claude **source author** for root's six execution-account decisions, working on the
isolated exact32 successor copy at
`/tmp/opensip-design-corrections/execution-account-successor.v1/source`.

**Not an acceptance.** Not an independent design or consumer review. Not product qualification. No
product implementation, no live edit, no commit, no push. This session is on the final
application's exclusion list and cannot serve as its acceptor.

## Deliverables

| File | What |
|---|---|
| `author-review.md` / `author-review.json` | The corrections per decision, tests, boundaries, limitations, remaining issues |
| `assessment-corrections.md` | F1–F4 restated against the corrected source; root's diagnostic qualifications and how each was honoured |
| `changed-file-handoff.json` | Nine changed files: before/after SHA256, byte and line counts, per-file purpose, and what was deliberately not touched |
| `tree-delta.json` | Every file of the working copy hashed against frozen32: 12 898 files, **9 changed, 0 added, 0 removed** |
| `suite-report.json` | All 16 current `run-evaluator3-checks.py` jobs over the edited source — all exit 0 |
| `suite2-report.json` | All 5 `run-reference-checks.py` children over the edited source — all exit 0 |
| `finalize-report.json` | Consistency check, deliverable hashes, full receipt index |

## Preserved images

`before/` and `after/` hold a copy of every file inspected for editing, with
`before-hashes.json` / `after-hashes.json`.

## Receipts

`probes/receipts/<label>/` holds the exact `argv`, full `stdout`, full `stderr` and `exit` code of
every command run. Two labels exit non-zero on purpose: `step2-` and `step3-check-execution-inputs`
are intermediate authoring iterations that caught real mistakes, kept rather than discarded. The
final checker run is `step5-check-execution-inputs` and the suite copy at
`suite/execution-inputs.stdout`: **71 cases, 0 mismatches, 0 oracle failures, exit 0**.

## Source pins

The authoritative ledgers `foundation/evaluator3-source-pins.v1.json` and
`foundation/source-pins.v1.json` are **unchanged** and are now stale for exactly the nine changed
files. Root owns the real pin/planning rebinding and the final current-suite run.

To execute the suites at all, this runtime holds a clearly labelled **disposable, test-only**
rebinding — `DISPOSABLE-rebound-source-pins.json`, driven by `disposable-pin-rebind-launcher.py`
and `disposable-reference-children.py`. It is never copied back into the source, and the stale-pin
fact is reported rather than repaired. All check reports were redirected into this runtime so no
report file in the source was overwritten.

## Tools in this runtime

`runner.py` (receipt-recording command wrapper), `snapshot.py` (before/after images),
`build-handoff.py`, `build-author-review-json.py`, `verify-tree-delta.py`, `finalize.py`,
`probes/p1…p9_*.py`.
