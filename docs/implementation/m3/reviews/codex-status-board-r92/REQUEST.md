# Review request: IMPLEMENTATION-STATUS-2026-10-15-r92 (shared status board)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-status-board-r92/`).

## Boundaries

Do not edit either repository, the stage or control files. Do not run the compiler, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate. Read-only hashing, JSON parsing and Git queries (including `git show <commit>:<path>`) are permitted.

## Subject

- **Stage.** `/tmp/opensip-implementation/status-board-r92-stage`
- **Subject manifest.** `docs/implementation/m3/status/2026-10-15-r92-subject.json` inside the stage: 8647 bytes, SHA-256 `89fc2f26559088e13716c79eeb2f24f85c35eb4ceb5c8c6f923e52ad5d0d87c2`. Rehash every member.
- **Bases.** Product `94e5fdebd63a174694dadbb5e647063855614b77` (clean), architecture `9f42a19c31d51b7f35fb9e7f1aeaee6e561eec51`.

## Context

The accepted predecessor is r91, which you accepted (`docs/implementation/m3/reviews/codex-status-board-r91/`), published at `bf4a42f8736feede1b487e7d79c6bc065eff14cd`. Since then the product changed by three commits:
- the lock bind `6d425bcd685b5b73f4c5474695d73964cc769af2` of contract successor 163, the B2-a reference refresh (contract successors 162 to 163);
- B2-a's code commit `6c5b8e8ba1086426ffe719198192a4c4bc530b55`;
- the inventory v191 lock bind `94e5fdebd63a174694dadbb5e647063855614b77` (inventory successors 150 to 151).

The status directory is dated `2026-10-15`, the date of the evidence head; r91's is `2026-10-14`.

## What to review

**Records.** The 215 accepted r91 records are inherited by value; confirm equality without re-reviewing them. Exactly four records are appended:

| Record | Unit | Architecture | Product | Review |
| --- | --- | --- | --- | --- |
| E216 | B2A-PLAN-r1 | `ccb8b07cc43ba5debc77c600b1f77e06611cf47b` | none | `docs/implementation/m3/reviews/codex-b2a-plan-r1/review.json` (your ACCEPT) |
| E217 | B2-A-REFERENCE-r2 | `a0a2e47d471030d2251465eb61d5de1c48f6111a` | `6d425bcd685b…` | `docs/implementation/m3/reviews/codex-b2a-reference-r2/review.json` (your ACCEPT-DESIGN-UNIT; round 1 published as history) |
| E218 | B2-A-r1 (code) | `370424e58eaaa9da26959bfed81390dced511da2` | `6c5b8e8ba108…` | `docs/implementation/m3/reviews/codex-b2a-r1/review.json` (your ACCEPT-UNIT) |
| E219 | B2-A-inventory-v191 | `9f42a19c31d51b7f35fb9e7f1aeaee6e561eec51` | `94e5fdebd63a…` | `docs/implementation/m3/reviews/codex-b2a-inventory-v191-r1/review.json` (your ACCEPT-UNIT) |

Check each record's review pin, architecture commit and product commit references against committed bytes and Git ancestry. Each scope must claim nothing beyond its accepted review. There is no law change, so no `acceptedLawDeltaScopes` row is added.

**Bindings.**
- The 65 earlier contract bindings are inherited by value and equal the lock's contract successors 98 to 162. Exactly one is appended, equal to the lock's last (successor 163).
- The 54 earlier inventory bindings are inherited by value. One is appended, equal to the lock's last inventory successor.
- The result is 66 contract bindings and 55 inventory bindings.

**Inherited validation scopes.** `source.json` `productChangesSinceR91` records the changed files since r91: the lock, `crates/security/src/custody.rs`, the four new B2-a paths. It also records that none of them is in an inherited validation scope's product map. Check the diff and that statement.

**Changed rows and text:**
- **B row** (front door and `unit-register.json`): B1-a, B1-b, B3-a and B2-a bound. The evidence appends the four scopes. The next action is B2-b, including the CI trace that B2-a's plan left to it. Every other wait is kept.
- **Next actions:** item 6 updated.
- **Cut-off line:** dated 2026-10-15; product `94e5fdeb`; inventory **191** (151); contracts **163**; product changed only by B2-a.
- **Line 10:** the 219 count, inventory binding v137–191, and contract binding 98–163.
- **New paragraph:** "accepted work after r91".
- `previousBoard` pins the r91 board at `bf4a42f87…`, with a byte-identical history snapshot.
- The authorities add the r91 review and assent, and the new units' reviews (including reference round 1), subjects, assents, plan and reference record.

**Still open:** M3 is not complete. The discovery rule has no consumer (B2-b and B2-c). B3-a's records and choice have no consumer or caller. B1-a and B1-b have no caller (J1). Native owner/worker, K1, the SM-11..14 completion round and qualification stay open.

## Output

`review.json` must carry the following, with your independently checked values, plus `nonBlockingObservations`:

```json
{
  "verdict": "ACCEPT",
  "requiredFindings": [],
  "subjectManifestSha256": "89fc2f26559088e13716c79eeb2f24f85c35eb4ceb5c8c6f923e52ad5d0d87c2",
  "scopedRecords": 219,
  "inventory": 191,
  "contractSuccessors": 163,
  "productCodeChangedSinceR91ByB2aOnly": true,
  "b2aPlanReferenceCodeAndInventoryRecordedExactly": true,
  "contractBindingAppendedExactly": true,
  "noInheritedValidationScopeFileChanged": true,
  "ownerAssentInferred": false,
  "productQualification": false,
  "entirePlanComplete": false
}
```

The lead will give its own assent and run fresh design verification before an architecture-only status commit. Nothing is pushed.
