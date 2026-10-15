# Review request: IMPLEMENTATION-STATUS-2026-10-15-r96 (shared status board)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/private/tmp/opensip-implementation/reviews/codex-status-board-r96/`).

## Boundaries

Do not edit either repository, the stage or control files. Do not run the compiler, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 held-out entry. Do not use other panes and do not delegate. Read-only hashing, JSON parsing and Git queries (including `git show <commit>:<path>`) are permitted.

## Subject

- **Stage.** `/tmp/opensip-implementation/status-board-r96-stage`
- **Subject manifest.** `docs/implementation/m3/status/2026-10-15-r96-subject.json` inside the stage: 8647 bytes, SHA-256 `ea4f4ddff3714271ef1924269b431846f68641dfa7559b1fe2acaf42692941c5`. Rehash every member.
- **Bases.** Product `ec2d655d264203cd392b4c690c7627766395ecdf` (clean), architecture `c76ef2e62d19b0d43b7ddb972c46e2f374ebd4bf`.

## Context

The accepted predecessor is r95, which you accepted (`docs/implementation/m3/reviews/codex-status-board-r95/`), published at `e0fe80bc56458c9d119a125dbcde5f98e526359d`. Since then the product changed by two commits: B2-b4a's code commit `251e315d3d813500724c736c4aa3738bd5bc30e0` and its inventory v196 lock bind `ec2d655d264203cd392b4c690c7627766395ecdf`. Contract successors are unchanged at 164.

## What to review

**Records.** The 232 accepted r95 records are inherited by value; confirm equality without re-reviewing them. Exactly three records are appended:

| Record | Unit | Architecture | Product | Review |
| --- | --- | --- | --- | --- |
| E233 | B2B4-PLAN-r2 | `bd50e7b9caa8d4452421c6e9132aa54e6b8142fe` | none | `docs/implementation/m3/reviews/codex-b2b4-plan-r2/review.json` (your ACCEPT at round 2; round 1 published as history) |
| E234 | B2-B4A-r2 (code) | `38affd7890ab57985ffb368c62b6d2da7d0e6ae3` | `251e315d3d81…` | `docs/implementation/m3/reviews/codex-b2b4a-r2/review.json` (your ACCEPT-UNIT at round 2; round 1 published as history) |
| E235 | B2-B4A-inventory-v196 | `c76ef2e62d19b0d43b7ddb972c46e2f374ebd4bf` | `ec2d655d2642…` | `docs/implementation/m3/reviews/codex-b2b4a-inventory-v196-r1/review.json` |

Check each record's review pin, architecture commit and product commit references against committed bytes and Git ancestry. Each scope must claim nothing beyond its accepted review. **E234 must state the census outcome exactly:**
- the 2× objects margin fails for aws-sdk-rust, aws-sdk-js-v3 and the smithy-sdk workspace;
- aws-sdk-rust exceeds the 2^20 object cap itself;
- the caps return to the law (M3-B r5 item 12), and no margin is claimed;
- the held-out margin is outstanding.

There is no law change yet.

**Bindings.**
- The 67 contract bindings equal the lock's contract successors 98 to 164 and are unchanged.
- The 59 earlier inventory bindings are inherited by value, and exactly one is appended (v196).
- The result is 67 contract bindings and 60 inventory bindings.

**Validation scopes.** `source.json` `productChangesSinceR95` lists the changed files (the B2-b4a paths, `custody.rs` and the lock). It records that none is in an inherited validation scope's product map. Check this against the Git diff.

**Changed rows and text:**
- **B row:** B2-b3 bound, and B2-b4's plan r2 and B2-b4a bound with inventory v196. The margin fails and the caps return to the law. B2-b4b is next, and the all-entry T2 margin gate is open.
- **Item 6.**
- **Cut-off line:** inventory 196 (156 successors), contracts 164, product changed only by B2-b4a.
- **Line 10:** 235, and inventory binding v137–196.
- **New paragraph:** "accepted work after r95".
- `previousBoard` pins the r95 board at `e0fe80bc5…`, with a byte-identical history snapshot.
- The authorities add the r95 review and assent and the new units' reviews (including earlier rounds), subjects, assents, plan and inventory records.

**Still open:**
- M3 is not complete.
- B2-b is in progress: B2-b4b remains, which brings bytes into the census, then the item-12 amendment and the cap change. Its all-entry T2 margin gate is open.
- B2-c, B3-b, J1, native owner/worker, K1, the SM-11..14 completion round and qualification stay open.

## Output

`review.json` must carry the following, with your independently checked values, plus `nonBlockingObservations`:

```json
{
  "verdict": "ACCEPT",
  "requiredFindings": [],
  "subjectManifestSha256": "ea4f4ddff3714271ef1924269b431846f68641dfa7559b1fe2acaf42692941c5",
  "scopedRecords": 235,
  "inventory": 196,
  "contractSuccessors": 164,
  "productCodeChangedSinceR95ByB2b4aOnly": true,
  "b2b4PlanAndB2b4aRecordedExactly": true,
  "censusFailureAndCapsReturnedStated": true,
  "inventoryBindingsAppendedExactly": true,
  "t2MarginGateStatedOpen": true,
  "noInheritedValidationScopeFileChanged": true,
  "ownerAssentInferred": false,
  "productQualification": false,
  "entirePlanComplete": false
}
```

The lead will give its own assent and run fresh design verification before an architecture-only status commit. Nothing is pushed.
