# Execution-account source-author runtime — v2 follow-up

Same actual-Claude source author (session `823bf66b-…`), continuing on the same isolated exact32
successor copy at `/tmp/opensip-design-corrections/execution-account-successor.v1/source`.

**Not an acceptance.** Not an independent design review, not a blind consumer review, not product
qualification. Whole-design and blind acceptance remain required and are not claimed here. No
frozen or live edit, no pin or planning edit, no product implementation, no commit, no push.

**The v1 runtime is preserved unchanged.** Every v1 report, receipt and before/after image is
untouched; `finalize-report.json` re-hashes them to show it. All v2 output is under this directory.

## What this pass responds to

`root-execution-account-draft-review.v1/assessment.md` (DRAFT-P1, DRAFT-P2, editorial),
`root-execution-account-draft-review.v2/assessment.md` (reporting scope, independence claim,
control naming, F4 qualification) and `root-execution-account-draft-review.v1/primary-pair-probe.json`.

## Deliverables

| File | What |
|---|---|
| `author-review.md` / `author-review.json` | Each finding, the correction, the measured evidence, limits and remaining issues |
| `changed-file-handoff.json` | Six files changed in v2, with v1-handoff / v2-before / v2-after SHA256, line counts and purpose; plus what was deliberately not touched and why |
| `tree-delta.json` | Every file hashed against frozen32: 12 898 files, **9 changed, 0 added, 0 removed** — the same nine as v1, no new file |
| `focused-checks-report.json` | The nine focused current checks, all exit 0, plus the twelve deliberately not re-run and why |
| `finalize-report.json` | Hash drift, v1-runtime integrity, deliverable hashes |

## Starting bytes

All nine v2 BEFORE images equal the v1 handoff AFTER bytes (`before-hashes.json`). The model image
is `4eaf175ff440f6440230cfaa0e00280d29eea89d0b969da73fe7ce7f8a7127f2`, the exact SHA root's
`primary-pair-probe.json` was taken against.

## Receipts

`probes/receipts/<label>/` holds exact argv, full stdout, full stderr and exit code for every
command. Three exit non-zero by design as authoring iterations that caught real mistakes
(`v2-step1-checker` and two earlier `q4` runs); they are kept rather than discarded. The final
checker run is `v2-focused-checks-final` / `suite/execution-inputs.stdout`: **75 cases, 0
mismatches, 0 oracle failures**.

## Source pins

Both authoritative ledgers are read only and remain stale for exactly the same nine files as after
v1. Root performs all authoritative pin/planning rebinds and the full integrated suites on final
bytes, so this pass deliberately ran a focused check set rather than repeating the v1 broad sweep.
