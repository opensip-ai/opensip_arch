# Review request: IMPLEMENTATION-STATUS-2026-10-16-r97 (shared status board)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/private/tmp/opensip-implementation/reviews/codex-status-board-r97/`).

## Boundaries

Do not edit either repository, the stage or control files. Do not run the compiler, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 held-out entry. Do not use other panes and do not delegate. Read-only hashing, JSON parsing and Git queries (including `git show <commit>:<path>`) are permitted.

## Subject

- **Stage.** `/tmp/opensip-implementation/status-board-r97-stage`
- **Subject manifest.** `docs/implementation/m3/status/2026-10-16-r97-subject.json` inside the stage: 8647 bytes, SHA-256 `b90b58c87206254dc58579a4d06776424f3cdf8f5a435f99e303c1d9cc7c3459`. Rehash every member.
- **Bases.** Product `84caf3f58d8379c9386fda42a41e5513ac81ebbb` (clean), architecture `fa0ee631aff243de4ad300fdd69da8fb33e0f4d5`.

## Context

The accepted predecessor is r96 (`docs/implementation/m3/reviews/codex-status-board-r96/`), published at `a84239c2ea6ca1ded1326d854daa4a98d6e87cc3`. Since then:
- the product changed by two commits: B2-b4b1's code commit `c172d8d5a7e002fe9609518d42581ef5e98f773c` and its inventory v197 lock bind `84caf3f58d8379c9386fda42a41e5513ac81ebbb`;
- law M3-B r6 (item 12 only) was accepted and published at `fa0ee631aff243de4ad300fdd69da8fb33e0f4d5`.

Contract successors are unchanged at 164.

## What to review

**Records.** The 235 accepted r96 records are inherited by value; confirm equality without re-reviewing them. Exactly four records are appended:

| Record | Unit | Architecture | Product | Review |
| --- | --- | --- | --- | --- |
| E236 | B2B4-PLAN-r4 | `6d9bcfd9e2b71aaf52c483ae0f66864b33e5cb14` | none | `docs/implementation/m3/reviews/codex-b2b4-plan-r4/review.json` (your ACCEPT at round 4; round 3 published as history) |
| E237 | B2-B4B1-r2 (code) | `43895c7fa55a4f5d723ea7707262ab9d536ad53c` | `c172d8d5a7e0…` | `docs/implementation/m3/reviews/codex-b2b4b1-r2/review.json` (your ACCEPT-UNIT at round 2; round 1 published as history) |
| E238 | B2-B4B1-inventory-v197 | `86362b0c88450c989badd4ecd4d222b0dc93a412` | `84caf3f58d83…` | `docs/implementation/m3/reviews/codex-b2b4b1-inventory-v197-r1/review.json` |
| E239 | M3-B-r6 (law) | `fa0ee631aff243de4ad300fdd69da8fb33e0f4d5` | none | `docs/implementation/m3/reviews/codex-m3b-r6-r2/review.json` (your ACCEPT at round 2; round 1 published as history) |

Check each record's review pin, architecture commit and product commit references against committed bytes and Git ancestry. Each scope must claim nothing beyond its accepted review:
- **E237** states the byte census outcome exactly: `aws-sdk-rust` fails 2× at every R and exceeds 2^30 at R = 1,024, and no byte margin is claimed.
- **E239** states r6 exactly: the walker storage redesign; the caps provisional until its census; the member-observation bound outstanding until B3-b; the held-out margin outstanding.

**Bindings.**
- The 67 contract bindings are unchanged.
- The 60 earlier inventory bindings are inherited by value, and exactly one is appended (v197).
- The result is 67 contract bindings and 61 inventory bindings.

**Validation scopes.** `source.json` `productChangesSinceR96` lists the changed files and records that none is in an inherited validation scope's product map. Check this against the Git diff.

**Changed rows and text:**
- **B row:** B2-b4b1 and law r6 are recorded, with the redesign next and the all-entry T2 margin gate open.
- **Item 6.**
- **Cut-off line:** inventory 197 (157 successors), contracts 164, product changed only by B2-b4b1, and law r6 accepted.
- **Line 10:** 239, and inventory binding v137–197.
- **New paragraph:** "accepted work after r96".
- `previousBoard` pins the r96 board, with a byte-identical history snapshot.
- The authorities add the r96 review and assent, and the new units' and law's reviews (including earlier rounds), subjects, assents, plan, law and inventory records.

**Still open:**
- M3 is not complete.
- B2-b is in progress (the walker storage redesign, then the caps), and its all-entry T2 margin gate is open.
- B2-c, B3-b, J1, native owner/worker, K1, the SM-11..14 completion round and qualification stay open.

## Output

`review.json` must carry the following, with your independently checked values, plus `nonBlockingObservations`:

```json
{
  "verdict": "ACCEPT",
  "requiredFindings": [],
  "subjectManifestSha256": "b90b58c87206254dc58579a4d06776424f3cdf8f5a435f99e303c1d9cc7c3459",
  "scopedRecords": 239,
  "inventory": 197,
  "contractSuccessors": 164,
  "productCodeChangedSinceR96ByB2b4b1Only": true,
  "b2b4PlanR4B2b4b1AndLawR6RecordedExactly": true,
  "byteCensusOutcomeAndLawR6Stated": true,
  "inventoryBindingsAppendedExactly": true,
  "t2MarginGateStatedOpen": true,
  "noInheritedValidationScopeFileChanged": true,
  "ownerAssentInferred": false,
  "productQualification": false,
  "entirePlanComplete": false
}
```

The lead will give its own assent and run fresh design verification before an architecture-only status commit. Nothing is pushed.
