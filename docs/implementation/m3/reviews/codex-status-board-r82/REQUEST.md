# Review request: IMPLEMENTATION-STATUS-2026-10-14-r82 (shared status board)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-status-board-r82/`).

## Boundaries

Do not edit either repository, the stage or control files. Do not run the compiler, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate. Read-only hashing, JSON parsing and Git queries are permitted.

## Subject

- Stage: `/tmp/opensip-implementation/status-board-r82-stage`
- Subject manifest: `docs/implementation/m3/status/2026-10-14-r82-subject.json` inside the stage, 8647 bytes, SHA-256 `2c144d69ee82f7188a745177c5daf9306f622fbc4afcfbd6417246d4273a6936`. Rehash every member.
- Bases: product `95279fa8ae086f98bd221cd827f6c0efc156c0c5` (clean), architecture `37643eb02a91262abc31861fca30006bc56f1067`.

## Context

This is the routine reconciliation after one new acceptance. The accepted predecessor is r81, which you accepted (`docs/implementation/m3/reviews/codex-status-board-r81/`), published at `bbe41c9a35e8d2544144a452d819547416b75407`.

## What to review

The 195 accepted r81 records are inherited by value. Confirm by-value equality without re-reviewing them. Exactly one record is appended:

| Record | Unit | Architecture publication | Review |
| --- | --- | --- | --- |
| E196 | SM-U2B-DEPENDENCY-SOURCE-SETS-r1 | `37643eb02a91262abc31861fca30006bc56f1067` | `docs/implementation/m3/reviews/codex-sm-u2b-r1/review.json` (your ACCEPT; any earlier REQUIRED-FINDINGS round is published alongside as history) |

Check E196's review pin and architecture commit against the committed bytes and Git ancestry. Its scope text must claim nothing beyond the accepted review: eight dependency-source sets only, generated locks labelled sizing stand-ins, the overlay entry pending, no source authentication, import admission, SM-5 or SM-7 value, and L not in effect.

Also check:

- There are 196 scoped records. The 51 inventory bindings (v137–v187) and 64 contract bindings (v98–v161) are inherited by value and equal the product lock.
- Product, lock and source are unchanged. Inherited validation is inherited, not rerun.
- `source.json` `previousBoard` pins the r81 board committed at `bbe41c9a3…`, with a byte-identical history snapshot. Its authorities add the r81 review and lead assent, and E196's review, subject and lead assent.
- The evidence cut-off is dated **2026-10-14** and the status directory is `2026-10-14-r82`, matching E196's commit date.
- The front door changes only these: the cut-off line, the r81→r82 links, the 196 count, the new "accepted work after r81" paragraph, and the S-M register row's evidence and next-action cells. Earlier "after rNN" paragraphs are kept as history.
- O7, D3 and D13 stay closed. Full S-M, effective L, native owner/worker, K1 and qualification stay open.

## Output

`review.json` must carry:
- `verdict` (`ACCEPT` or `REQUIRED-FINDINGS`);
- `requiredFindings` (array);
- `subjectManifestSha256` = `2c144d69ee82f7188a745177c5daf9306f622fbc4afcfbd6417246d4273a6936`;
- `scopedRecords`: 196, `inventoryUnchanged`: 187 and `contractSuccessorsUnchanged`: 161;
- `productCodeUnchanged`: true;
- `ownerAssentInferred`: false, `productQualification`: false and `entirePlanComplete`: false.

The lead will give its own exact assent and run fresh design and implementation verification before an architecture-only status commit. Nothing is pushed.
