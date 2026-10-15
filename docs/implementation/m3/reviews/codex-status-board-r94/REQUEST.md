# Review request: IMPLEMENTATION-STATUS-2026-10-15-r94 (shared status board)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/private/tmp/opensip-implementation/reviews/codex-status-board-r94/`).

## Boundaries

Do not edit either repository, the stage or control files. Do not run the compiler, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate. Read-only hashing, JSON parsing and Git queries (including `git show <commit>:<path>`) are permitted.

## Subject

- **Stage.** `/tmp/opensip-implementation/status-board-r94-stage`
- **Subject manifest.** `docs/implementation/m3/status/2026-10-15-r94-subject.json` inside the stage: 8647 bytes, SHA-256 `6be130afc89760f330c934916dc82b91309d572d5a58df2fe40d532f31ed6c56`. Rehash every member.
- **Bases.** Product `f3384b59a0d6487975dc2655bca0dbab23d4f03c` (clean), architecture `62f4d27aa819a9edb21da319e7be109c02da5c04`.

## Context

The accepted predecessor is r93, which you accepted (`docs/implementation/m3/reviews/codex-status-board-r93/`), published at `588e3e847379e871d9b86d73c4b86a27f08f9998`. Since then the product changed by four commits:
- B2-b2's code commit `a725a68ecc6529094775764631a6ac58ececc8f9` and its inventory v192 lock bind `3b3ab6e0e354c8f81e4ac030ed3102757be43085`;
- B2-b3a's code commit `2d8f60903d59963ac2c813c02e4122c6a2056497` and its inventory v193 lock bind `f3384b59a0d6487975dc2655bca0dbab23d4f03c`.

Contract successors are unchanged at 164.

## What to review

**Records.** The 222 accepted r93 records are inherited by value; confirm equality without re-reviewing them. Exactly five records are appended:

| Record | Unit | Architecture | Product | Review |
| --- | --- | --- | --- | --- |
| E223 | B2-B2-r2 (code) | `3afa8830625f4c063afacfca5f3a0b32daf99129` | `a725a68ecc65…` | `docs/implementation/m3/reviews/codex-b2b2-r2/review.json` (your ACCEPT-UNIT at round 2; round 1 published as history; NBO-1 recorded as a correction) |
| E224 | B2-B2-inventory-v192 | `47bee3b55292a973e90bbff6e81e3c509b28f3c0` | `3b3ab6e0e354…` | `docs/implementation/m3/reviews/codex-b2b2-inventory-v192-r1/review.json` |
| E225 | B2B3-PLAN-r2 | `363303dc906030edd4e522ad5061fce87b42a3ca` | none | `docs/implementation/m3/reviews/codex-b2b3-plan-r2/review.json` (your ACCEPT at round 2; round 1 published as history) |
| E226 | B2-B3A-r2 (code) | `ce8cfce3ae8aece562b8ed323b94cde8d14b84e4` | `2d8f60903d59…` | `docs/implementation/m3/reviews/codex-b2b3a-r2/review.json` (your ACCEPT-UNIT at round 2; round 1 published as history; R2-NBO-1 recorded as a B2-b3b follow-up) |
| E227 | B2-B3A-inventory-v193 | `62f4d27aa819a9edb21da319e7be109c02da5c04` | `f3384b59a0d6…` | `docs/implementation/m3/reviews/codex-b2b3a-inventory-v193-r1/review.json` |

Check each record's review pin, architecture commit and product commit references against committed bytes and Git ancestry. Each scope must claim nothing beyond its accepted review. No law change.

**Bindings.**
- The 67 contract bindings equal the lock's contract successors 98 to 164 and are unchanged.
- The 55 earlier inventory bindings are inherited by value, and exactly two are appended (v192 and v193).
- The result is 67 contract bindings and 57 inventory bindings.

**Validation scopes.** `source.json` `productChangesSinceR93` lists the changed files (the lock and the B2-b2 and B2-b3a paths) and records that none is in an inherited validation scope's product map. Check this.

**Changed rows and text:**
- **B row:** B2-b in progress (B2-b0, B2-b1, B2-b2, the B2-b3 plan r2 and B2-b3a bound; inventory v193; B2-b3b next), with the all-entry T2 margin gate stated open.
- **Item 6.**
- **Cut-off line:** inventory 193 (153 successors), contracts 164, product changed only by B2-b.
- **Line 10:** 227, and inventory binding v137–193.
- **New paragraph:** "accepted work after r93".
- `previousBoard` pins the r93 board at `588e3e847…`, with a byte-identical history snapshot.
- The authorities add the r93 review and assent and the new units' reviews (including earlier rounds), subjects, assents, plan and inventory records.

**Still open:** M3 is not complete. B2-b is in progress (B2-b3b, B2-b3c and B2-b4 remain), and its all-entry T2 margin gate is open. B2-c, B3-b, J1, native owner/worker, K1, the SM-11..14 completion round and qualification stay open.

## Output

`review.json` must carry the following, with your independently checked values, plus `nonBlockingObservations`:

```json
{
  "verdict": "ACCEPT",
  "requiredFindings": [],
  "subjectManifestSha256": "6be130afc89760f330c934916dc82b91309d572d5a58df2fe40d532f31ed6c56",
  "scopedRecords": 227,
  "inventory": 193,
  "contractSuccessors": 164,
  "productCodeChangedSinceR93ByB2bOnly": true,
  "b2b2B2b3PlanAndB2b3aRecordedExactly": true,
  "inventoryBindingsAppendedExactly": true,
  "t2MarginGateStatedOpen": true,
  "noInheritedValidationScopeFileChanged": true,
  "ownerAssentInferred": false,
  "productQualification": false,
  "entirePlanComplete": false
}
```

The lead will give its own assent and run fresh design verification before an architecture-only status commit. Nothing is pushed.
