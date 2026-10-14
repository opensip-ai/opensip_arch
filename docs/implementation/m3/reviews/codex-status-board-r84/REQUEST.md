# Review request: IMPLEMENTATION-STATUS-2026-10-14-r84 (shared status board)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-status-board-r84/`).

## Boundaries

Do not edit either repository, the stage or control files. Do not run the compiler, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate. Read-only hashing, JSON parsing and Git queries are permitted.

## Subject

- Stage: `/tmp/opensip-implementation/status-board-r84-stage`
- Subject manifest: `docs/implementation/m3/status/2026-10-14-r84-subject.json` inside the stage, 8647 bytes, SHA-256 `cd6905e151cf4d58178f6fa8b63aefe00fae961cbe4c29cf81d3d8c53d2f1247`. Rehash every member.
- Bases: product `95279fa8ae086f98bd221cd827f6c0efc156c0c5` (clean), architecture `e7cd213b3b3741b976bb6d77a48e1677741ac1a3`.

## Context

This is the routine reconciliation after one new acceptance. The accepted predecessor is r83, which you accepted (`docs/implementation/m3/reviews/codex-status-board-r83/`), published at `d7abc70d0886ff8a66bb82f76d066a99a6dd54ac`.

## What to review

The 198 accepted r83 records are inherited by value. Confirm by-value equality without re-reviewing them. Exactly one record is appended:

| Record | Unit | Architecture publication | Review |
| --- | --- | --- | --- |
| E199 | SM-COLD-RUST-r1 | `e7cd213b3b3741b976bb6d77a48e1677741ac1a3` | `docs/implementation/m3/reviews/codex-sm-cold-rust-r1/review.json` (your ACCEPT) |

Check E199's review pin and architecture commit against the committed bytes and Git ancestry. Its scope text must claim nothing beyond the accepted review:
- the cold reset (U-5a's module byte-equal; state absent, fresh per-run TMPDIR, page cache recorded and never claimed flushed) before every child;
- the five Rust-row components (SM-3, SM-5, SM-7, SM-9 at the eight Rust sizes under D-1 with no lower bound, and SM-4);
- confined diffs, controls reproducing the warm populations, and R8 two-entry sums;
- the current interpretation superseding inherited standings;
- inputs only: no F, T, outcome or placeholder fill, and L is not in effect.

Also check:

- There are 199 scoped records. The 51 inventory bindings (v137–v187) and 64 contract bindings (v98–v161) are inherited by value and equal the product lock.
- Product, lock and source are unchanged. Inherited validation is inherited, not rerun.
- `source.json` `previousBoard` pins the r83 board committed at `d7abc70d0…`, with a byte-identical history snapshot. Its authorities add the r83 review and lead assent, and E199's review, subject and lead assent.
- The evidence cut-off is dated **2026-10-14**, and the status directory is `2026-10-14-r84`, matching E199's commit date. E199 is the evidence head, so no publication between it and the base is unrecorded.
- The front door changes only these: the cut-off line, the r83→r84 links, the 199 count, the new "accepted work after r83" paragraph, and the S-M register row's evidence and next-action cells. Earlier "after rNN" paragraphs are kept as history.
- O7, D3 and D13 stay closed. Full S-M, effective L, native owner/worker, K1 and qualification stay open.

## Output

`review.json` must carry:
- `verdict` (`ACCEPT` or `REQUIRED-FINDINGS`);
- `requiredFindings` (array);
- `subjectManifestSha256` = `cd6905e151cf4d58178f6fa8b63aefe00fae961cbe4c29cf81d3d8c53d2f1247`;
- `scopedRecords`: 199, `inventoryUnchanged`: 187 and `contractSuccessorsUnchanged`: 161;
- `productCodeUnchanged`: true;
- `ownerAssentInferred`: false, `productQualification`: false and `entirePlanComplete`: false.

The lead will give its own exact assent and run fresh design and implementation verification before an architecture-only status commit. Nothing is pushed.
