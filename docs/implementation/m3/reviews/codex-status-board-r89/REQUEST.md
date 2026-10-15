# Review request: IMPLEMENTATION-STATUS-2026-10-14-r89 (shared status board)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-status-board-r89/`).

## Boundaries

Do not edit either repository, the stage or control files. Do not run the compiler, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate. Read-only hashing, JSON parsing and Git queries (including `git show <commit>:<path>`) are permitted.

## Subject

- **Stage.** `/tmp/opensip-implementation/status-board-r89-stage`
- **Subject manifest.** `docs/implementation/m3/status/2026-10-14-r89-subject.json` inside the stage: 8647 bytes, SHA-256 `bc60b82bd83e89d405de4f1e77be9436191bc7116fdfc4c0d833cb7cd60cebed`. Rehash every member.
- **Bases.** Product `c0151bc6b7fdb6db9157124fa068c8be5061f5d4` (clean), architecture `a5d2c7af125b2ef1d410161baf92c3b9cd4ad295`.

## Context

The accepted predecessor is r88, which you accepted (`docs/implementation/m3/reviews/codex-status-board-r88/`), published at `6450467bfc5345cb0727dda571a3de27409b16b2`. Since then, the product changed:
- B1-a's code commit `50cefc64173b6e5daa8f1d2d9d410045544d1f9c`;
- the separate inventory v188 lock bind `c0151bc6b7fdb6db9157124fa068c8be5061f5d4` (inventory successors 147 to 148; contract successors unchanged at 162).

## What to review

**Records.** The 207 accepted r88 records are inherited by value; confirm equality without re-reviewing. Exactly two records are appended:

| Record | Unit | Architecture | Product | Review |
| --- | --- | --- | --- | --- |
| E208 | B1-A-r2 (code) | `7ff769c9e1626967f4fe9ece0fa78b8621891a15` | `50cefc64173b…` | `docs/implementation/m3/reviews/codex-b1a-r2/review.json` (your ACCEPT-UNIT; round 1 REQUIRED-FINDINGS is published as history) |
| E209 | B1-A-inventory-v188 | `a5d2c7af125b2ef1d410161baf92c3b9cd4ad295` (record `90d6035020c4…`, then the lead assent in its own commit) | `c0151bc6b7fd…` | `docs/implementation/m3/reviews/codex-b1a-inventory-v188-r2/review.json` (your ACCEPT-UNIT; round 1 published as history) |

Check each record's review pin, architecture commit and product commit references against committed bytes and Git ancestry. Each scope must claim nothing beyond its accepted review.

E209's scope states three facts. Check each against the commits:
- v188 also covers the two schema sources B-S10 added (lead decision LD-B1A-INV-1).
- Round 2 only re-issued round 1's acceptance, in the shape `verify_design` reads.
- The record commit omitted the lead assent, which landed in the next architecture commit with the pinned bytes.

**The inherited host validation scope.** B1-a changed `crates/host/src/lib.rs` by the comment above `mod configuration` only. The inherited host key-record-data validation scope (300 host tests at product `76d30ee`) pins `lib.rs`.

`source.json` `productChangesSinceR88` states this, and that the scope stays historical at its own commit, not claimed on main. The status integrator now verifies every inherited scope's product-map pins at that scope's own product commit with `git show`, not on the working tree.

Check:
- that the `lib.rs` diff since r88 is comment-only;
- that the statement is honest;
- that the root-observation and slot-execution scopes are untouched.

**Changed rows and text:**
- **B row** (front door and `unit-register.json`): the status records B1-a bound; the evidence appends both scopes; the next action names B1-b, then B3-a and B2-a, keeping every other wait.
- **Next actions:** item 6 updated.
- **Cut-off line:** product `c0151bc6`, inventory **188** (148), contracts 162, product changed only by B1-a.
- **Line 10:** the 209 count and the inventory binding range v137–188.
- **New paragraph:** "accepted work after r88".

**Counts and bindings:**
- There are 209 scoped records.
- There are 52 inventory bindings: the 51 earlier ones inherited by value, and the new one equal to the product lock's last inventory successor.
- The 65 contract bindings are unchanged.
- `previousBoard` pins the r88 board at `6450467bf…`, with a byte-identical history snapshot.
- The authorities add the r88 review and assent, and both new units' reviews (round 1 and round 2), subjects and assents.

**Still open:** M3 is not complete. B1-a has no caller. Native owner/worker, K1, the SM-11..14 completion round and qualification stay open.

## Output

`review.json` must carry the following, with your independently checked values, plus `nonBlockingObservations`:

```json
{
  "verdict": "ACCEPT",
  "requiredFindings": [],
  "subjectManifestSha256": "bc60b82bd83e89d405de4f1e77be9436191bc7116fdfc4c0d833cb7cd60cebed",
  "scopedRecords": 209,
  "inventory": 188,
  "contractSuccessors": 162,
  "productCodeChangedSinceR88ByB1aOnly": true,
  "b1aCodeAndInventoryRecordedExactly": true,
  "hostValidationScopeStatedHistorical": true,
  "ownerAssentInferred": false,
  "productQualification": false,
  "entirePlanComplete": false
}
```

The lead will give its own assent and run fresh design verification before an architecture-only status commit. Nothing is pushed.
