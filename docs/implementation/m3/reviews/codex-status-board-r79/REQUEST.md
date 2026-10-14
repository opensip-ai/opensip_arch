# Review request: IMPLEMENTATION-STATUS-2026-10-13-r79 (shared status board)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-status-board-r79/`).

## Boundaries

Do not edit either repository, the stage or control files. Do not run the compiler, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate. Read-only hashing, JSON parsing and Git queries are permitted.

## Subject

- Stage: `/tmp/opensip-implementation/status-board-r79-stage`
- Subject manifest: `docs/implementation/m3/status/2026-10-13-r79-subject.json` inside the stage, 8647 bytes, SHA-256 `356453af2a3c4934b22a0fd6f1468958bdb458c8862d5e9b9f01a734f070ef91`. Rehash every member.
- Bases: product `95279fa8ae086f98bd221cd827f6c0efc156c0c5` (clean), architecture `490d6db4155a230206c957271c22be6fb4264548`.

## Context

This is the routine reconciliation after one new acceptance. The accepted predecessor is r78, which you accepted (`docs/implementation/m3/reviews/codex-status-board-r78/`), published at `32b4ba9bdd352c41e28d3761a3e53c49b0ebea3c`.

## What to review

The 192 accepted r78 records are inherited by value. Confirm by-value equality without re-reviewing them. Exactly one record is appended:

| Record | Unit | Architecture publication | Review |
| --- | --- | --- | --- |
| E193 | SM-COLD-TS-r1 | `490d6db4155a230206c957271c22be6fb4264548` | `docs/implementation/m3/reviews/codex-sm-cold-ts-r2/review.json` (your ACCEPT; any earlier REQUIRED-FINDINGS round is published alongside as history) |

Check E193's review pin and architecture commit against the committed bytes and Git ancestry. Its scope text must claim nothing beyond the accepted review: the TS-row cold-reset series only, cold OpenSIP state with the page cache recorded and never claimed flushed, replay rows as synthetic D-1 scenarios with no real-workload bound, no F, T or outcome, and L not in effect.

Also check:

- There are 193 scoped records. The 51 inventory bindings (v137–v187) and 64 contract bindings (v98–v161) are inherited by value and equal the product lock.
- Product, lock and source are unchanged. Inherited validation is inherited, not rerun.
- `source.json` `previousBoard` pins the r78 board committed at `32b4ba9bd…`, with a byte-identical history snapshot. Its authorities add the r78 review and lead assent, and E193's review, subject and lead assent.
- The evidence cut-off is dated **2026-10-13** and the status directory is `2026-10-13-r79`, matching E193's commit date.
- The front door changes only these: the cut-off line, the r78→r79 links, the 193 count, the new "accepted work after r78" paragraph, and the S-M register row's evidence and next-action cells. Earlier "after rNN" paragraphs are kept as history.
- O7, D3 and D13 stay closed. Full S-M, effective L, native owner/worker, K1 and qualification stay open.

## Output

`review.json` must carry:
- `verdict` (`ACCEPT` or `REQUIRED-FINDINGS`);
- `requiredFindings` (array);
- `subjectManifestSha256` = `356453af2a3c4934b22a0fd6f1468958bdb458c8862d5e9b9f01a734f070ef91`;
- `scopedRecords`: 193, `inventoryUnchanged`: 187 and `contractSuccessorsUnchanged`: 161;
- `productCodeUnchanged`: true;
- `ownerAssentInferred`: false, `productQualification`: false and `entirePlanComplete`: false.

The lead will give its own exact assent and run fresh design and implementation verification before an architecture-only status commit. Nothing is pushed.
