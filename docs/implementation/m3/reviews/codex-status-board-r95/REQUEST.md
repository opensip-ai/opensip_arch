# Review request: IMPLEMENTATION-STATUS-2026-10-15-r95 (shared status board)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/private/tmp/opensip-implementation/reviews/codex-status-board-r95/`).

## Boundaries

Do not edit either repository, the stage or control files. Do not run the compiler, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate. Read-only hashing, JSON parsing and Git queries (including `git show <commit>:<path>`) are permitted.

## Subject

- **Stage.** `/tmp/opensip-implementation/status-board-r95-stage`
- **Subject manifest.** `docs/implementation/m3/status/2026-10-15-r95-subject.json` inside the stage: 8647 bytes, SHA-256 `3585498871501f74d47bfc64006beb5c923074ed9449739aeaa98fca7a67e1f3`. Rehash every member.
- **Bases.** Product `02fd45c813e2b1e87b086cdef4ecac1aacfbb867` (clean), architecture `90fbc3c3e6397e6bf426ac455228b73ec7e93f98`.

## Context

The accepted predecessor is r94, which you accepted (`docs/implementation/m3/reviews/codex-status-board-r94/`), published at `c1690efbe14b1502b2c080f222117569064031e7`. Since then the product changed by four commits:
- B2-b3b's code commit `9b87d27042c19107e097212e0cc26097e24a66ee` and its inventory v194 lock bind `aa037d09995f7710bda5f8993ff9133f829e3df3`;
- B2-b3c's code commit `74eda8ced526277dc1c0895bcac258ba5a056edc` and its inventory v195 lock bind `02fd45c813e2b1e87b086cdef4ecac1aacfbb867`.

Contract successors are unchanged at 164.

## What to review

**Records.** The 227 accepted r94 records are inherited by value; confirm equality without re-reviewing them. Exactly five records are appended:

| Record | Unit | Architecture | Product | Review |
| --- | --- | --- | --- | --- |
| E228 | B2-B3B-r3 (code) | `3b3ce5a230de0382acf58db2af9e278c07c0c424` | `9b87d27042c1…` | `docs/implementation/m3/reviews/codex-b2b3b-r3/review.json` (your ACCEPT-UNIT at round 3; rounds 1 and 2 published as history) |
| E229 | B2-B3B-inventory-v194 | `c568f47930163bc3c8a85457c060a09eff0a4e34` | `aa037d09995f…` | `docs/implementation/m3/reviews/codex-b2b3b-inventory-v194-r1/review.json` |
| E230 | B2B3-PLAN-r3 | `4d30d0a00473179625cf9403d208531cd0746666` | none | `docs/implementation/m3/reviews/codex-b2b3-plan-r3/review.json` (your ACCEPT; the LD-B2B3-12 amendment only) |
| E231 | B2-B3C-r2 (code) | `68eca8090d6d4c01dabebe891c732457b8c48d20` | `74eda8ced526…` | `docs/implementation/m3/reviews/codex-b2b3c-r2/review.json` (your ACCEPT-UNIT at round 2; round 1 published as history) |
| E232 | B2-B3C-inventory-v195 | `90fbc3c3e6397e6bf426ac455228b73ec7e93f98` | `02fd45c813e2…` | `docs/implementation/m3/reviews/codex-b2b3c-inventory-v195-r1/review.json` |

Check each record's review pin, architecture commit and product commit references against committed bytes and Git ancestry. Each scope must claim nothing beyond its accepted review. No law change.

**Bindings.**
- The 67 contract bindings equal the lock's contract successors 98 to 164 and are unchanged.
- The 57 earlier inventory bindings are inherited by value, and exactly two are appended (v194 and v195).
- The result is 67 contract bindings and 59 inventory bindings.

**Validation scopes.** `source.json` `productChangesSinceR94` lists the changed files. Exactly one, `crates/host/src/lib.rs`, is in an inherited validation scope's product map (the combined host scope). Its added lines (`libRsAddedLines`) are only a comment and a test-only, macOS-only module declaration, with nothing removed. As in r89 and r90, that scope stays historical at its own commit and is not claimed on main. The root-observation and slot-execution scopes are untouched. Check this against the Git diff.

**Changed rows and text:**
- **B row:** B2-b3 complete (the plan r3, B2-b3a, B2-b3b and B2-b3c bound; inventory v195), B2-b in progress with B2-b4 next, and the all-entry T2 margin gate stated open.
- **Item 6.**
- **Cut-off line:** inventory 195 (155 successors), contracts 164, product changed only by B2-b3.
- **Line 10:** 232, and inventory binding v137–195.
- **New paragraph:** "accepted work after r94".
- `previousBoard` pins the r94 board at `c1690efbe…`, with a byte-identical history snapshot.
- The authorities add the r94 review and assent and the new units' reviews (including earlier rounds), subjects, assents, plan and inventory records.

**Still open:** M3 is not complete. B2-b is in progress (B2-b4 remains), and its all-entry T2 margin gate is open. B2-c, B3-b, J1 (which owns `crates/host/tests/discovery_tests.rs`), native owner/worker, K1, the SM-11..14 completion round and qualification stay open.

## Output

`review.json` must carry the following, with your independently checked values, plus `nonBlockingObservations`:

```json
{
  "verdict": "ACCEPT",
  "requiredFindings": [],
  "subjectManifestSha256": "3585498871501f74d47bfc64006beb5c923074ed9449739aeaa98fca7a67e1f3",
  "scopedRecords": 232,
  "inventory": 195,
  "contractSuccessors": 164,
  "productCodeChangedSinceR94ByB2b3Only": true,
  "b2b3bPlanR3AndB2b3cRecordedExactly": true,
  "inventoryBindingsAppendedExactly": true,
  "t2MarginGateStatedOpen": true,
  "onlyLibRsInValidationScopeChangedAndScopeStaysHistorical": true,
  "ownerAssentInferred": false,
  "productQualification": false,
  "entirePlanComplete": false
}
```

The lead will give its own assent and run fresh design verification before an architecture-only status commit. Nothing is pushed.
