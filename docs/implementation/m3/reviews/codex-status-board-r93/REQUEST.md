# Review request: IMPLEMENTATION-STATUS-2026-10-15-r93 (shared status board)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-status-board-r93/`).

## Boundaries

Do not edit either repository, the stage or control files. Do not run the compiler, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate. Read-only hashing, JSON parsing and Git queries (including `git show <commit>:<path>`) are permitted.

## Subject

- **Stage.** `/tmp/opensip-implementation/status-board-r93-stage`
- **Subject manifest.** `docs/implementation/m3/status/2026-10-15-r93-subject.json` inside the stage: 8647 bytes, SHA-256 `4ebe9e19c5a9ad851ad088d07edac306ebacacd1f148439329bfa8c31d02fce0`. Rehash every member.
- **Bases.** Product `f51769f885dc786168e487033645ad1a4e0ae699` (clean), architecture `8829bb5f67b261b320c29ea572953ce27f6cdd05`.

## Context

The accepted predecessor is r92, which you accepted (`docs/implementation/m3/reviews/codex-status-board-r92/`), published at `424f64a3f331261d0f1e8fb323948492cda5a06d`. Since then the product changed by two commits:
- the lock bind `7d0ac1b59df9a099a4d8edc05d8600f46dd63923` of contract successor 164, B2-b0 (contract successors 163 to 164);
- B2-b1's code commit `f51769f885dc786168e487033645ad1a4e0ae699`.

There is no inventory change: B2-b1 adds no path (LD-B2B1-1, which you accepted).

## What to review

**Records.** The 219 accepted r92 records are inherited by value; confirm equality without re-reviewing them. Exactly three records are appended:

| Record | Unit | Architecture | Product | Review |
| --- | --- | --- | --- | --- |
| E220 | B2B-PLAN-r4 | `3b2a55d48c442b66d188369a4d8a9307fdaeb14b` | none | `docs/implementation/m3/reviews/codex-b2b-plan-r4/review.json` (your ACCEPT at round 4; rounds 1 to 3 published as history) |
| E221 | B2-B0-REFERENCE-r3 | `4fbc0c65011af58948f01986c79061443598a798` | `7d0ac1b59df9…` | `docs/implementation/m3/reviews/codex-b2b0-reference-r3/review.json` (your ACCEPT-DESIGN-UNIT at round 3; rounds 1 and 2 published as history) |
| E222 | B2-B1-r1 (code) | `8829bb5f67b261b320c29ea572953ce27f6cdd05` | `f51769f885dc…` | `docs/implementation/m3/reviews/codex-b2b1-r1/review.json` (your ACCEPT-UNIT with NBO-1 and NBO-2, recorded as corrections in the lead assent) |

Check each record's review pin, architecture commit and product commit references against committed bytes and Git ancestry. Each scope must claim nothing beyond its accepted review. E222's scope must state the public Rust platform APIs, as your NBO-2 corrected. No law change.

**Bindings.**
- The 66 earlier contract bindings equal the lock's contract successors 98 to 163, and exactly one is appended (successor 164).
- The 55 inventory bindings are unchanged and inherited by value.
- The result is 67 contract bindings and 55 inventory bindings.

**Validation scopes.** `source.json` `productChangesSinceR92` lists the changed files (the lock and five platform files) and records that none is in an inherited validation scope's product map. It also states that B2-b1's platform suite was compared serially. Check this.

**Changed rows and text:**
- **B row:** B2-b in progress (plan r4, B2-b0 and B2-b1 bound; B2-b2 next), with the all-entry T2 margin gate stated open.
- **Item 6.**
- **Cut-off line:** inventory 191, contracts **164**, product changed only by B2-b.
- **Line 10:** 222, and contract binding 98–164.
- **New paragraph:** "accepted work after r92".
- `previousBoard` pins the r92 board at `424f64a3f…`, with a byte-identical history snapshot.
- The authorities add the r92 review and assent and the new units' reviews (including earlier rounds), subjects, assents, plan and reference record.

**Still open:** M3 is not complete. B2-b is in progress, and its all-entry T2 margin gate is open. B2-c, B3-b, J1, native owner/worker, K1, the SM-11..14 completion round and qualification stay open.

## Output

`review.json` must carry the following, with your independently checked values, plus `nonBlockingObservations`:

```json
{
  "verdict": "ACCEPT",
  "requiredFindings": [],
  "subjectManifestSha256": "4ebe9e19c5a9ad851ad088d07edac306ebacacd1f148439329bfa8c31d02fce0",
  "scopedRecords": 222,
  "inventory": 191,
  "contractSuccessors": 164,
  "productCodeChangedSinceR92ByB2bOnly": true,
  "b2bPlanReferenceAndB2b1RecordedExactly": true,
  "contractBindingAppendedExactly": true,
  "t2MarginGateStatedOpen": true,
  "noInheritedValidationScopeFileChanged": true,
  "ownerAssentInferred": false,
  "productQualification": false,
  "entirePlanComplete": false
}
```

The lead will give its own assent and run fresh design verification before an architecture-only status commit. Nothing is pushed.
