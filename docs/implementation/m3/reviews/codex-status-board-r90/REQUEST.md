# Review request: IMPLEMENTATION-STATUS-2026-10-14-r90 (shared status board)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-status-board-r90/`).

## Boundaries

Do not edit either repository, the stage or control files. Do not run the compiler, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate. Read-only hashing, JSON parsing and Git queries (including `git show <commit>:<path>`) are permitted.

## Subject

- **Stage.** `/tmp/opensip-implementation/status-board-r90-stage`
- **Subject manifest.** `docs/implementation/m3/status/2026-10-14-r90-subject.json` inside the stage: 8647 bytes, SHA-256 `9883998c1563f62cc64476a79a9637734b2e0f62943f9856e72f2c39dfb444f6`. Rehash every member.
- **Bases.** Product `ec70009de1490449a6173c238a7eaf0a03e106c4` (clean), architecture `97a0ba895cb8cfdf87a3ee9d4a6afee3d25d7819`.

## Context

The accepted predecessor is r89, which you accepted (`docs/implementation/m3/reviews/codex-status-board-r89/`), published at `93960ed5327615ead9af08845a4bc27ce3409e76`. Since then the product changed:
- B1-b's code commit `0bc66c63f8b07169fdfdf3f7323cbb231512e190`;
- the separate inventory v189 lock bind `ec70009de1490449a6173c238a7eaf0a03e106c4` (inventory successors 148 to 149; contract successors unchanged at 162).

## What to review

**Records.** The 209 accepted r89 records are inherited by value; confirm equality without re-reviewing them. Exactly three records are appended:

| Record | Unit | Architecture | Product | Review |
| --- | --- | --- | --- | --- |
| E210 | B1B-PLAN-r3 + M3-B r5 | `b98932720200253f671814d9cb728ba0615c1085` | none | `docs/implementation/m3/reviews/codex-b1b-plan-r3/review.json` (your ACCEPT; rounds 1 and 2 published as history) |
| E211 | B1-B-r4 (code) | `eef3a72cf2d5192eadae157dc2f83f2f6bba39d4` | `0bc66c63f8b0…` | `docs/implementation/m3/reviews/codex-b1b-r4/review.json` (your ACCEPT-UNIT; rounds 1 to 3 published as history) |
| E212 | B1-B-inventory-v189 | `97a0ba895cb8cfdf87a3ee9d4a6afee3d25d7819` | `ec70009de149…` | `docs/implementation/m3/reviews/codex-b1b-inventory-v189-r1/review.json` (your ACCEPT-UNIT) |

Check each record's review pin, architecture commit and product commit references against committed bytes and Git ancestry. Each scope must claim nothing beyond its accepted review. E210 must record M3-B r5 as changing only item 9's enforcement exception list. `source.json` adds an `acceptedLawDeltaScopes` row for it.

**The inherited host validation scope.** B1-b changed `crates/host/src/lib.rs` by adding the private module declaration `#[allow(dead_code)] mod invocation_mode;` with its comment, removing no line. The inherited host key-record-data validation scope (300 host tests at product `76d30ee`) pins `lib.rs`. `source.json` `productChangesSinceR89` states this, and that the scope stays historical at its own commit, not claimed on main. The status integrator verifies every inherited scope's product-map pins at that scope's own commit.

Check:
- that the `lib.rs` diff since r89 is exactly that addition;
- that the statement is honest;
- that the root-observation and slot-execution scopes are untouched.

**Changed rows and text:**
- **B row** (front door and `unit-register.json`): B1-a and B1-b bound; the evidence appends the three scopes; the next action is B3-a, then B2-a, with J1 composing the analysis path, and every other wait kept.
- **Next actions:** item 6 updated.
- **Cut-off line:** product `ec70009d`, inventory **189** (149), contracts 162, product changed only by B1-b.
- **Line 10:** the 212 count and the inventory binding range v137–189.
- **New paragraph:** "accepted work after r89".

**Counts and bindings:**
- There are 212 scoped records.
- There are 53 inventory bindings: the 52 earlier ones inherited by value, and the new one equal to the lock's last inventory successor.
- The 65 contract bindings are unchanged.
- `previousBoard` pins the r89 board at `93960ed53…`, with a byte-identical history snapshot.
- The authorities add the r89 review and assent and the new units' reviews, subjects, assents, plan and law.

**Still open:** M3 is not complete. B1-a and B1-b have no caller (J1 wires them). Native owner/worker, K1, the SM-11..14 completion round and qualification stay open.

## Output

`review.json` must carry the following, with your independently checked values, plus `nonBlockingObservations`:

```json
{
  "verdict": "ACCEPT",
  "requiredFindings": [],
  "subjectManifestSha256": "9883998c1563f62cc64476a79a9637734b2e0f62943f9856e72f2c39dfb444f6",
  "scopedRecords": 212,
  "inventory": 189,
  "contractSuccessors": 162,
  "productCodeChangedSinceR89ByB1bOnly": true,
  "b1bPlanLawCodeAndInventoryRecordedExactly": true,
  "hostValidationScopeStatedHistorical": true,
  "ownerAssentInferred": false,
  "productQualification": false,
  "entirePlanComplete": false
}
```

The lead will give its own assent and run fresh design verification before an architecture-only status commit. Nothing is pushed.
