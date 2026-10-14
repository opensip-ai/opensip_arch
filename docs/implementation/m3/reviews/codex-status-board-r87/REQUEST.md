# Review request: IMPLEMENTATION-STATUS-2026-10-14-r87 (shared status board)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-status-board-r87/`).

## Boundaries

Do not edit either repository, the stage or control files. Do not run the compiler, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate. Read-only hashing, JSON parsing and Git queries are permitted.

## Subject

- Stage: `/tmp/opensip-implementation/status-board-r87-stage`
- Subject manifest: `docs/implementation/m3/status/2026-10-14-r87-subject.json` inside the stage, 8647 bytes, SHA-256 `cbc05a510666c64feb8dfd7058d6f7e3538a9fde71661e07fdec17a383120589`. Rehash every member.
- Bases: product `95279fa8ae086f98bd221cd827f6c0efc156c0c5` (clean), architecture `737c75b82a6f698487394d306a02af43e8ea210b`.

## Context

This is an **expanded reconciliation**: three publications since r86, recorded together as you allowed for r82. The accepted predecessor is r86, which you accepted (`docs/implementation/m3/reviews/codex-status-board-r86/`), published at `f3a753304677365b7344e7ec3bbdcd3151ed4a97`. It also carries a **status correction**: M3-L r7's acceptance put M3-L in effect.

## What to review

The 201 accepted r86 records are inherited by value. Confirm by-value equality without re-reviewing them. Exactly three records are appended:

| Record | Unit | Architecture publication | Review |
| --- | --- | --- | --- |
| E202 | SM-O3-O4-PROPOSAL-r1 | `d43a961a86fc7b5b3002ed3c19cb75b07651c804` | `docs/implementation/m3/reviews/codex-sm-o3o4-proposal-r1/review.json` (your ACCEPT) |
| E203 | OWNER-DECISIONS-2026-10-14-r1 | `17049baf9a508fb69bd6c28394dcd8b5091ec79d` | `docs/implementation/m3/reviews/codex-owner-decisions-2026-10-14-r1/review.json` (your ACCEPT) |
| E204 | M3-L-r7 | `737c75b82a6f698487394d306a02af43e8ea210b` | `docs/implementation/m3/reviews/codex-provider-protocol-l-r7/review.json` (your ACCEPT) |

Check each record's review pin and architecture commit against the committed bytes and Git ancestry (E202, then E203, then E204, which is the evidence head). Each scope text must claim nothing beyond its accepted review:
- **E202:** a proposal, with no owner decision recorded.
- **E203:** the owner's O3-a and O4-a selections verbatim, with no law, budget or staging change.
- **E204:** item 9's values, every outcome (preliminary, conditional on D-1), the owner's answers, the S-M round's part of SM-11 to SM-14, and every gate item met, so **M3-L in effect from 2026-10-14**.

**Status correction.** Check that every corrected statement is exact, and that no other dependency or open item is weakened:
- **Rows and next actions.** The C2a, B, C, CF/D and S-M rows, Next actions items 1, 4 and 5, the C2a note after them, and the C2A-MAJOR decision row now say that effective L is met, and keep every other wait.
- **S-M row.** It records the accepted report and delta round, with the completion round of SM-11 to SM-14 owed after effect.
- **History.** Earlier "after rNN" paragraphs, including their historical "L remains not in effect" sentences, are kept as history.
- **Checks.** `checks.json` records `effectiveL` true (2026-10-14, basis M3-L r7) and `SMRoundComplete` true. `fullSMComplete` stays false.

Also check:

- There are 204 scoped records. The 51 inventory bindings (v137–v187) and 64 contract bindings (v98–v161) are inherited by value and equal the product lock.
- Product, lock and source are unchanged. Inherited validation is inherited, not rerun.
- `source.json` `previousBoard` pins the r86 board committed at `f3a753304…`, with a byte-identical history snapshot. Its authorities add the r86 review and lead assent, and the three records' reviews, subjects and lead assents.
- The evidence cut-off is dated **2026-10-14**, and the status directory is `2026-10-14-r87`, matching E204's commit date.
- The front door changes only these: the cut-off line, the r86→r87 links, the 204 count, the new "accepted work after r86" paragraph, the register rows named above, and the status-correction sentences.
- O7, D3 and D13 stay closed. M3 is not complete. Native owner/worker, K1 and qualification stay open.

## Output

`review.json` must carry:
- `verdict` (`ACCEPT` or `REQUIRED-FINDINGS`);
- `requiredFindings` (array);
- `subjectManifestSha256` = `cbc05a510666c64feb8dfd7058d6f7e3538a9fde71661e07fdec17a383120589`;
- `scopedRecords`: 204, `inventoryUnchanged`: 187 and `contractSuccessorsUnchanged`: 161;
- `productCodeUnchanged`: true;
- `effectiveLRecordedCorrectly`: true;
- `ownerAssentInferred`: false, `productQualification`: false and `entirePlanComplete`: false.

The lead will give its own exact assent and run fresh design and implementation verification before an architecture-only status commit. Nothing is pushed.
