# Review request: IMPLEMENTATION-STATUS-2026-10-14-r85 (shared status board)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-status-board-r85/`).

## Boundaries

Do not edit either repository, the stage or control files. Do not run the compiler, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate. Read-only hashing, JSON parsing and Git queries are permitted.

## Subject

- Stage: `/tmp/opensip-implementation/status-board-r85-stage`
- Subject manifest: `docs/implementation/m3/status/2026-10-14-r85-subject.json` inside the stage, 8647 bytes, SHA-256 `99db180af54672801eeb4ef8c6fe0998957344618d18c9891a8d5ce6da515e81`. Rehash every member.
- Bases: product `95279fa8ae086f98bd221cd827f6c0efc156c0c5` (clean), architecture `cb1aa04e802721714f167f7cc600198f9a08343d`.

## Context

This is the routine reconciliation after one new acceptance. The accepted predecessor is r84, which you accepted (`docs/implementation/m3/reviews/codex-status-board-r84/`), published at `9dd254013a7b5c68f300ce67df84f3d657523c69`.

## What to review

The 199 accepted r84 records are inherited by value. Confirm by-value equality without re-reviewing them. Exactly one record is appended:

| Record | Unit | Architecture publication | Review |
| --- | --- | --- | --- |
| E200 | SM-DESK-U4B-r2 | `cb1aa04e802721714f167f7cc600198f9a08343d` | `docs/implementation/m3/reviews/codex-sm-desk-u4b-r2/review.json` (your round-2 ACCEPT; round 1's REQUIRED-FINDINGS is published alongside it under codex-sm-desk-u4b-r1/) |

Check E200's review pin and architecture commit against the committed bytes and Git ancestry. Its scope text must claim nothing beyond the accepted review:
- SM-10 for all 14 rows and every F/T component under both resets (native bytes, checked conversion; SM-4 largest compiler child; R8 per entry and larger of two, not summed), with Express SM-2 from the synthesized program only (D-4) and the cohort Express entry informational;
- SM-11 labelled coverage for the medium Rust rows with no quotient;
- round 1 RF-01 resolved;
- desk only: no placeholder, F, T, outcome or gate effect, and L is not in effect.

Also check:

- There are 200 scoped records. The 51 inventory bindings (v137–v187) and 64 contract bindings (v98–v161) are inherited by value and equal the product lock.
- Product, lock and source are unchanged. Inherited validation is inherited, not rerun.
- `source.json` `previousBoard` pins the r84 board committed at `9dd254013…`, with a byte-identical history snapshot. Its authorities add the r84 review and lead assent, and E200's review, subject and lead assent.
- The evidence cut-off is dated **2026-10-14**, and the status directory is `2026-10-14-r85`, matching E200's commit date. E200 is the evidence head, so no publication between it and the base is unrecorded.
- The front door changes only these: the cut-off line, the r84→r85 links, the 200 count, the new "accepted work after r84" paragraph, and the S-M register row's evidence and next-action cells. Earlier "after rNN" paragraphs are kept as history.
- O7, D3 and D13 stay closed. Full S-M, effective L, native owner/worker, K1 and qualification stay open.

## Output

`review.json` must carry:
- `verdict` (`ACCEPT` or `REQUIRED-FINDINGS`);
- `requiredFindings` (array);
- `subjectManifestSha256` = `99db180af54672801eeb4ef8c6fe0998957344618d18c9891a8d5ce6da515e81`;
- `scopedRecords`: 200, `inventoryUnchanged`: 187 and `contractSuccessorsUnchanged`: 161;
- `productCodeUnchanged`: true;
- `ownerAssentInferred`: false, `productQualification`: false and `entirePlanComplete`: false.

The lead will give its own exact assent and run fresh design and implementation verification before an architecture-only status commit. Nothing is pushed.
