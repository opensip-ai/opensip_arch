# Review request: IMPLEMENTATION-STATUS-2026-10-13-r80 (shared status board)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-status-board-r80/`).

## Boundaries

Do not edit either repository, the stage or control files. Do not run the compiler, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate. Read-only hashing, JSON parsing and Git queries are permitted.

## Subject

- Stage: `/tmp/opensip-implementation/status-board-r80-stage`
- Subject manifest: `docs/implementation/m3/status/2026-10-13-r80-subject.json` inside the stage, 8647 bytes, SHA-256 `774a86b7057e4c081ca454aec6ba36999383a6f3392c3257f48f6306e31c093f`. Rehash every member.
- Bases: product `95279fa8ae086f98bd221cd827f6c0efc156c0c5` (clean), architecture `1b3b815b07fdb2782f469b21f3a05f71f896c89f`.

## Context

This is the routine reconciliation after one new acceptance. The accepted predecessor is r79, which you accepted (`docs/implementation/m3/reviews/codex-status-board-r79/`), published at `9e3492c05fa3cdf77fbabb594470b37e91f81f40`.

## What to review

The 193 accepted r79 records are inherited by value. Confirm by-value equality without re-reviewing them. Exactly one record is appended:

| Record | Unit | Architecture publication | Review |
| --- | --- | --- | --- |
| E194 | SM-U1-BUILD-SCRIPT-OUTPUTS-ABSENT-r1 | `1b3b815b07fdb2782f469b21f3a05f71f896c89f` | `docs/implementation/m3/reviews/codex-sm-u1-r2/review.json` (your ACCEPT; any earlier REQUIRED-FINDINGS round is published alongside as history) |

Check E194's review pin and architecture commit against the committed bytes and Git ancestry. Its scope text must claim nothing beyond the accepted review: U-1 variants, coverage series and the PLAN-r3 D-5 delta only, incomplete units preserved, no SM-4 value, F, T or outcome, and L not in effect.

Also check:

- There are 194 scoped records. The 51 inventory bindings (v137–v187) and 64 contract bindings (v98–v161) are inherited by value and equal the product lock.
- Product, lock and source are unchanged. Inherited validation is inherited, not rerun.
- `source.json` `previousBoard` pins the r79 board committed at `9e3492c05…`, with a byte-identical history snapshot. Its authorities add the r79 review and lead assent, and E194's review, subject and lead assent.
- The evidence cut-off is dated **2026-10-13** and the status directory is `2026-10-13-r80`, matching E194's commit date.
- The front door changes only these: the cut-off line, the r79→r80 links, the 194 count, the new "accepted work after r79" paragraph, and the S-M register row's evidence and next-action cells. Earlier "after rNN" paragraphs are kept as history.
- O7, D3 and D13 stay closed. Full S-M, effective L, native owner/worker, K1 and qualification stay open.

## Output

`review.json` must carry:
- `verdict` (`ACCEPT` or `REQUIRED-FINDINGS`);
- `requiredFindings` (array);
- `subjectManifestSha256` = `774a86b7057e4c081ca454aec6ba36999383a6f3392c3257f48f6306e31c093f`;
- `scopedRecords`: 194, `inventoryUnchanged`: 187 and `contractSuccessorsUnchanged`: 161;
- `productCodeUnchanged`: true;
- `ownerAssentInferred`: false, `productQualification`: false and `entirePlanComplete`: false.

The lead will give its own exact assent and run fresh design and implementation verification before an architecture-only status commit. Nothing is pushed.
