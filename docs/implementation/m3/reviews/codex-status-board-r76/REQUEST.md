# Review request: IMPLEMENTATION-STATUS-2026-10-13-r76 (shared status board)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-status-board-r76/`).

## Boundaries

Do not edit either repository, the stage or control files. Do not run the compiler, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate. Read-only hashing, JSON parsing and Git queries are permitted.

## Subject

- Stage: `/tmp/opensip-implementation/status-board-r76-stage`
- Subject manifest: `docs/implementation/m3/status/2026-10-13-r76-subject.json` inside the stage, 8647 bytes, SHA-256 `e47e13d193a43591a7a6282fec90e7e4b461d91a5c3861da38f46ea63b4c7698`. Rehash every member.
- Bases: product `95279fa8ae086f98bd221cd827f6c0efc156c0c5` (clean), architecture `622c0545e68ce892cd22b9b7a7127e67a7244614`.

## Context

This is the routine reconciliation after one new acceptance. The accepted predecessor is r75, which you accepted (`docs/implementation/m3/reviews/codex-status-board-r75/`), published at `fe77f91641c34f3b0c2997e34f53726b99d09149`.

## What to review

The 189 accepted r75 records are inherited by value. Confirm by-value equality without re-reviewing them. Exactly one record is appended:

| Record | Unit | Architecture publication | Review |
| --- | --- | --- | --- |
| E190 | S-M-DESK-U4A-r1 | `622c0545e68ce892cd22b9b7a7127e67a7244614` | `docs/implementation/m3/reviews/codex-s-m-desk-u4a-r1/review.json` (your ACCEPT) |

Check E190's review pin and architecture commit against the committed bytes and Git ancestry. Its scope text must claim nothing beyond the accepted review: desk records of SM-8 (D-6) and S_eff's first term (D-9) only, no placeholder, S_eff, F, T or outcome, and L not in effect. The gate wording must keep only L-G1 open.

Also check:

- There are 190 scoped records. The 51 inventory bindings (v137–v187) and 64 contract bindings (v98–v161) are inherited by value and equal the product lock.
- Product, lock and source are unchanged. Inherited validation is inherited, not rerun.
- `source.json` `previousBoard` pins the r75 board committed at `fe77f9164…`, with a byte-identical history snapshot. Its authorities add the r75 review and lead assent, and E190's review, subject and lead assent.
- The evidence cut-off is dated **2026-10-13** and the status directory is `2026-10-13-r76`, matching E190's commit date.
- The front door changes only these: the cut-off line, the r75→r76 links, the 190 count, the new "accepted work after r75" paragraph, and the S-M register row's evidence and next-action cells. Earlier "after rNN" paragraphs are kept as history.
- O7, D3 and D13 stay closed. Full S-M, effective L, native owner/worker, K1 and qualification stay open.

## Output

`review.json` must carry:
- `verdict` (`ACCEPT` or `REQUIRED-FINDINGS`);
- `requiredFindings` (array);
- `subjectManifestSha256` = `e47e13d193a43591a7a6282fec90e7e4b461d91a5c3861da38f46ea63b4c7698`;
- `scopedRecords`: 190, `inventoryUnchanged`: 187 and `contractSuccessorsUnchanged`: 161;
- `productCodeUnchanged`: true;
- `ownerAssentInferred`: false, `productQualification`: false and `entirePlanComplete`: false.

The lead will give its own exact assent and run fresh design and implementation verification before an architecture-only status commit. Nothing is pushed.
