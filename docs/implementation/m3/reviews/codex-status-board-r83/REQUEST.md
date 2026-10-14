# Review request: IMPLEMENTATION-STATUS-2026-10-14-r83 (shared status board)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-status-board-r83/`).

## Boundaries

Do not edit either repository, the stage or control files. Do not run the compiler, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate. Read-only hashing, JSON parsing and Git queries are permitted.

## Subject

- Stage: `/tmp/opensip-implementation/status-board-r83-stage`
- Subject manifest: `docs/implementation/m3/status/2026-10-14-r83-subject.json` inside the stage, 8647 bytes, SHA-256 `765569b44d42a10a9e16b4e6ba91b40565407b03aea422c92b27c2d4fdbb869e`. Rehash every member.
- Bases: product `95279fa8ae086f98bd221cd827f6c0efc156c0c5` (clean), architecture `8d27c2c52d0de68aac5c97be1d12b86e25705b50`.

## Context

This is the routine reconciliation after one new acceptance. The accepted predecessor is r82, which you accepted in round 2 (`docs/implementation/m3/reviews/codex-status-board-r82-r2/`), published at `a49151299650642be278813941c0957e739b3eb7`. r82 appended two records (E196 and E197).

## What to review

The 197 accepted r82 records are inherited by value. Confirm by-value equality without re-reviewing them. Exactly one record is appended:

| Record | Unit | Architecture publication | Review |
| --- | --- | --- | --- |
| E198 | SM-U2C-r2 | `8d27c2c52d0de68aac5c97be1d12b86e25705b50` | `docs/implementation/m3/reviews/codex-sm-u2c-r2/review.json` (your round-2 ACCEPT; round 1's REQUIRED-FINDINGS is published alongside it under `codex-sm-u2c-r1/`) |

Check E198's review pin and architecture commit against the committed bytes and Git ancestry. Its scope text must claim nothing beyond the accepted review:
- SM-5 is measured in two labelled parts from one timed span, and SM-7 r3 carries every NE §9.2 dependency field, for all nine Rust entries.
- R8 is given as two-entry sums.
- Earlier series are retained as superseded history.
- Generated locks are labelled sizing stand-ins.
- These are inputs only: no S-M value, F or T, placeholder fill, admission, protocol conformance or gate effect, and L is not in effect.

Also check:

- There are 198 scoped records. The 51 inventory bindings (v137–v187) and 64 contract bindings (v98–v161) are inherited by value and equal the product lock.
- Product, lock and source are unchanged. Inherited validation is inherited, not rerun.
- `source.json` `previousBoard` pins the r82 board committed at `a49151299…`, with a byte-identical history snapshot. Its authorities add the r82 round-2 review and lead assent, and E198's review, subject and lead assent.
- The evidence cut-off is dated **2026-10-14**, and the status directory is `2026-10-14-r83`, matching E198's commit date (8d27c2c5, 2026-10-14 01:28 -0700). E198 is the evidence head, so no publication between it and the base is unrecorded.
- The front door changes only these: the cut-off line, the r82→r83 links, the 198 count, the new "accepted work after r82" paragraph, and the S-M register row's evidence and next-action cells. Earlier "after rNN" paragraphs are kept as history.
- O7, D3 and D13 stay closed. Full S-M, effective L, native owner/worker, K1 and qualification stay open.

## Output

`review.json` must carry:
- `verdict` (`ACCEPT` or `REQUIRED-FINDINGS`);
- `requiredFindings` (array);
- `subjectManifestSha256` = `765569b44d42a10a9e16b4e6ba91b40565407b03aea422c92b27c2d4fdbb869e`;
- `scopedRecords`: 198, `inventoryUnchanged`: 187 and `contractSuccessorsUnchanged`: 161;
- `productCodeUnchanged`: true;
- `ownerAssentInferred`: false, `productQualification`: false and `entirePlanComplete`: false.

The lead will give its own exact assent and run fresh design and implementation verification before an architecture-only status commit. Nothing is pushed.
