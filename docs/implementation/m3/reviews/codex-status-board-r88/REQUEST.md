# Review request: IMPLEMENTATION-STATUS-2026-10-14-r88 (shared status board)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-status-board-r88/`).

## Boundaries

Do not edit either repository, the stage or control files. Do not run the compiler, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate. Read-only hashing, JSON parsing and Git queries are permitted.

## Subject

- **Stage.** `/tmp/opensip-implementation/status-board-r88-stage`
- **Subject manifest.** `docs/implementation/m3/status/2026-10-14-r88-subject.json` inside the stage: 8647 668f430d5de43b473d2011469a0ddbf2a1febe3b833abad89dda575bd97b78a2 bytes, SHA-256 ``. Rehash every member.
- **Bases.** Product `08527ebf732b432d7bfe8fce9c749cbfab51d9c1` (clean), architecture `87a51e2c1f171cfcda8bc84099b9f69c844a0ffd`.

## Context

This is an **expanded reconciliation**: three publications since r87, recorded together. The accepted predecessor is r87, which you accepted in round 2 (`docs/implementation/m3/reviews/codex-status-board-r87-r2/`), published at `0deeb0d32`.

Unlike r87, **the product changed**:
- B-S10's product code commit `c019e9ef0e8eaa03e4a0b9e3d8a83ab69162d517`;
- its separate lock bind `08527ebf732b432d7bfe8fce9c749cbfab51d9c1` (contract successors 161 to 162; inventory unchanged at 187).

The board also carries one **work-boundary correction**: the reviewer line named Herdr w2:p1 (Grok). The reviewer is you, Codex at Herdr w5:p1.

## What to review

The 204 accepted r87 records are inherited by value. Confirm by-value equality without re-reviewing them. Exactly three records are appended:

| Record | Unit | Architecture publication | Product commits | Review |
| --- | --- | --- | --- | --- |
| E205 | B1A-PLAN-r2 | `54e336d81911a0e0eaeb815163e25ea992026e54` | none | `docs/implementation/m3/reviews/codex-b1a-plan-r2/review.json` (your ACCEPT) |
| E206 | B-S10 | `d8950a8d1a6f4fbefd49e98bbc8afe0ff272a90b` | `c019e9ef…`, `08527ebf…` | `docs/implementation/m3/reviews/codex-b-s10-r2/review.json` (your ACCEPT-DESIGN-UNIT) |
| E207 | B-S10-CENSUS | `87a51e2c1f171cfcda8bc84099b9f69c844a0ffd` | `c019e9ef…` | `docs/implementation/m3/reviews/codex-b-s10-census-r1/review.json` (your ACCEPT) |

**Each record.** Check its review pin, architecture commit and product commit references against the committed bytes and Git ancestry. Each scope text must claim nothing beyond its accepted review:
- **E205:** a plan only, with no product code.
- **E206:** PCS admitted for generation and admission, and the preview v1 carrier admitted only; exact copies and pinned generation; the code commit and a separate lock bind. No resolver semantics, law change or qualification.
- **E207:** one census row 135 to 150, committed with the B-S10 code.

Also check that `c019e9ef` holds exactly the 14 published B-S10 product copies plus `tools/operability/exceptions.json`, and that `08527ebf` changes only `design-lock.json`, appending one contract successor that pins the B-S10 record, subject, review and assent.

**Inherited validation scopes.** These are host key-record data, root observation and slot execution. `source.json` `productChangesSinceR87` lists the files B-S10 changed and the files pinned by those scopes' product maps. Confirm the two sets are disjoint, so the scopes stand at their own product commits and were not rerun.

**Changed rows and text:**
- **B row** (`B1-a/b; B2-a/b/c/d; B3-a/b/c`), in the front door and `unit-register.json`: the status records B-S10 bound, the B1-a plan accepted and B1-a code next. The evidence appends the three scopes, and the next action names B1-a code from product `08527ebf`, then B3-a and B2-a, and keeps every other wait.
- **Next actions:** a new item 6 for configuration/discovery.
- **Work boundaries:** the reviewer line names Codex at Herdr w5:p1, and the GROK2/w6 boundary is unchanged.
- **Kept as history:** the decision register's historical "Grok reviews proposal" ownership cells.

**Counts and bindings:**
- There are 207 scoped records.
- The 51 inventory bindings (v137–v187) are inherited by value. The contract bindings are now 65 (v98–v162); the 64 earlier ones are inherited by value, and the new one equals the product lock's last contract successor.
- `source.json` `previousBoard` pins the r87 board committed at `0deeb0d32…`, with a byte-identical history snapshot. Its authorities add the r87 review and lead assent, and each new record's review, subject and assent (`b-s10-unit.json` and `b-s10-census-unit.json` are the B-S10 assents).
- The evidence cut-off is dated **2026-10-14**, and the status directory is `2026-10-14-r88`.

**Front-door changes.** Only these change:
- the cut-off line (product `08527ebf`, contracts 162, product changed only by B-S10);
- the r87→r88 links, the 207 count, and the contract binding range 98–162;
- the new "accepted work after r87" paragraph;
- the B row, item 6 and the reviewer line.

**Still open:** M3 is not complete. The B1-a resolver is not implemented. Native owner/worker, K1, the SM-11..14 completion round and qualification stay open. O7, D3 and D13 stay closed.

## Output

`review.json` must carry:
- `verdict` (`ACCEPT` or `REQUIRED-FINDINGS`);
- `requiredFindings` (array);
- `subjectManifestSha256` = ``;
- `scopedRecords`: 207, `inventoryUnchanged`: 187 and `contractSuccessors`: 162;
- `productCodeChangedSinceR87ByBS10Only`: true;
- `b1aPlanBS10AndCensusRecordedExactly`: true and `reviewerLineCorrected`: true;
- `ownerAssentInferred`: false, `productQualification`: false and `entirePlanComplete`: false.

The lead will give its own exact assent and run fresh design and implementation verification before an architecture-only status commit. Nothing is pushed.
