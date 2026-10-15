# Review request: IMPLEMENTATION-STATUS-2026-10-16-r98 (shared status board)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/private/tmp/opensip-implementation/reviews/codex-status-board-r98/`).

## Boundaries

Do not edit either repository, the stage or control files. Do not run the compiler, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 held-out entry. Do not use other panes and do not delegate. Read-only hashing, JSON parsing and Git queries (including `git show <commit>:<path>`) are permitted.

## Subject

- **Stage.** `/tmp/opensip-implementation/status-board-r98-stage`
- **Subject manifest.** `docs/implementation/m3/status/2026-10-16-r98-subject.json` inside the stage: 8647 bytes, SHA-256 `8366cb8ad6734817f5f23d2854d4a4a825fbaa49dcba5b7584e179a5fe13dddb`. Rehash every member.
- **Bases.** Product `d33df45ac0a5422efbebb43eee9c652d17ee742a` (clean), architecture `845daebc0e812ec39e4ca6622a69f617f3a8676a`.

## Context

The accepted predecessor is r97 (`docs/implementation/m3/reviews/codex-status-board-r97/`), published at `194fcad1d89f20db50491e3a574342ff608ace50`. Since then:
- the product changed by three commits: B2-b3d's code commit `6115329a1d59f718611964df36247c9a4039e5b4`, its v198 lock bind `79c816096310711663104a5e9217717718f8f510`, and B2-b4b3's code commit `d33df45ac0a5422efbebb43eee9c652d17ee742a` (no lock change);
- law M3-B r7 was accepted and published at `8d2f4557cd8d28526b3564057fd68d045eded531`.

Contract successors are unchanged at 164.

## What to review

**Records.** The 239 accepted r97 records are inherited by value; confirm equality without re-reviewing them. Exactly five records are appended:

| Record | Unit | Architecture | Product | Review |
| --- | --- | --- | --- | --- |
| E240 | B2B3D-PLAN-r2 | `a1f14786e4ecb0c780d25b093c438821e6a5c3d8` | none | `docs/implementation/m3/reviews/codex-b2b3d-plan-r2/review.json` (round 1 as history) |
| E241 | B2-B3D-r2 (code) | `2df9b5cffa939c632723d412f2bee0045fba2c70` | `6115329a1d59…` | `docs/implementation/m3/reviews/codex-b2b3d-r2/review.json` (round 1 as history) |
| E242 | B2-B3D-inventory-v198 | `230c7df884a5584911aab0daf9af03369fd5cb78` | `79c816096310…` | `docs/implementation/m3/reviews/codex-b2b3d-inventory-v198-r1/review.json` |
| E243 | M3-B-r7 (law) | `8d2f4557cd8d28526b3564057fd68d045eded531` | none | `docs/implementation/m3/reviews/codex-m3b-r7-r1/review.json` |
| E244 | B2-B4B3-r1 (code) | `845daebc0e812ec39e4ca6622a69f617f3a8676a` | `d33df45ac0a5…` | `docs/implementation/m3/reviews/codex-b2b4b3-r1/review.json` |

Check each record's review pin, architecture commit and product commit references against committed bytes and Git ancestry. Each scope must claim nothing beyond its accepted review:
- **E243 and E244** state the caps exactly (2^22, 2^21, 2^30) and the margin held for the lead-readable entries.
- **Workspace full-ledger margins and the held-out margin stay outstanding.**

**Bindings.**
- The 67 contract bindings are unchanged.
- The 61 earlier inventory bindings are inherited by value, and exactly one is appended (v198).
- The result is 67 contract bindings and 62 inventory bindings.

**Validation scopes.** `source.json` `productChangesSinceR97` lists the changed files and records that none is in an inherited validation scope's product map. Check this against the Git diff.

**Changed rows and text:**
- **B row:** the caps recorded and the margin held for the lead-readable entries; the held-out margin (an owner decision) and the workspace full-ledger margins outstanding; the all-entry gate open; the inventory-description follow-up.
- **Item 6.**
- **Cut-off line:** inventory 198 (158 successors), contracts 164, product changed only by B2-b3d and B2-b4b3, and law r7 accepted.
- **Line 10:** 244, and inventory binding v137–198.
- **New paragraph:** "accepted work after r97".
- `previousBoard` pins r97, with a byte-identical snapshot.
- The authorities add the r97 review and assent, and the new records' reviews, subjects, assents, plan, law and inventory records.

**Still open:**
- M3 is not complete.
- B2-b is not complete: its all-entry margin gate stays open.
- B2-c, B3-b, J1, native owner/worker, K1, the SM-11..14 completion round and qualification stay open.

## Output

`review.json` must carry the following, with your independently checked values, plus `nonBlockingObservations`:

```json
{
  "verdict": "ACCEPT",
  "requiredFindings": [],
  "subjectManifestSha256": "8366cb8ad6734817f5f23d2854d4a4a825fbaa49dcba5b7584e179a5fe13dddb",
  "scopedRecords": 244,
  "inventory": 198,
  "contractSuccessors": 164,
  "productCodeChangedSinceR97ByB2b3dAndB2b4b3Only": true,
  "b2b3dPlanB2b3dLawR7AndB2b4b3RecordedExactly": true,
  "capsRecordedAndOutstandingMarginsStated": true,
  "inventoryBindingsAppendedExactly": true,
  "t2MarginGateStatedOpen": true,
  "noInheritedValidationScopeFileChanged": true,
  "ownerAssentInferred": false,
  "productQualification": false,
  "entirePlanComplete": false
}
```

The lead will give its own assent and run fresh design verification before an architecture-only status commit. Nothing is pushed.
