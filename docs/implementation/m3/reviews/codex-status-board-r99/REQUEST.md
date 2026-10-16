# Review request: IMPLEMENTATION-STATUS-2026-10-16-r98 (shared status board)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/private/tmp/opensip-implementation/reviews/codex-status-board-r99/`).

## Boundaries

Do not edit either repository, the stage or control files. Do not run the compiler, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 held-out entry. Do not use other panes and do not delegate. Read-only hashing, JSON parsing and Git queries (including `git show <commit>:<path>`) are permitted.

## Subject

- **Stage.** `/tmp/opensip-implementation/status-board-r99-stage`
- **Subject manifest.** `docs/implementation/m3/status/2026-10-16-r99-subject.json` inside the stage: 8648 bytes, SHA-256 `e009926bc61c156e975425a11d9af38d7b3787b28a69be084ec0b655a0ae40d0`. Rehash every member.
- **Bases.** Product `c0e61a4b9ad48467430af8a5cfbe53ed7e6111c5` (clean), architecture `8d29369ea7ec88c5222183cc5c02daec1c08c40c`.

## Context

The accepted predecessor is r98 (`docs/implementation/m3/reviews/codex-status-board-r98/`), published at `de2388edc19dec8c7ed2bffd0ceef2314d86cddc`.

**Since then:**
- **The owner decided the held-out T2 margin** (2026-10-16: the mechanical blind run). The record is `docs/implementation/m3/owner-decisions/2026-10-16/HELD-OUT-T2-MARGIN.md`, published with the B2-b4 plan r6 at `a5b3fc88f7a84bbff40819679bd76172bcb60004`.
- **The product changed by four commits:**
  - B2-b4c1's code `ab0eb2c970ea23bd9eb53aac2ec93ccd5b665731`;
  - the lock bind of v199 and the B2-b4 description successor, `c1778a167502eb0f963802c64e75b6169052c65f` (contract successor 165);
  - B2-b4c2's commit `c0bbdc86affecf3ed68f077452ea38831c5b5d89`;
  - the v200 lock bind `c0e61a4b9ad48467430af8a5cfbe53ed7e6111c5`.

There is no law change.

## What to review

**Records.** The 244 accepted r98 records are inherited by value; confirm equality without re-reviewing them. Exactly five records are appended:

| Record | Unit | Architecture | Product | Reviews |
| --- | --- | --- | --- | --- |
| E245 | B2B4-PLAN-r6 + owner decision | `a5b3fc88f7a84bbff40819679bd76172bcb60004` | none | `docs/implementation/m3/reviews/codex-b2b4-plan-r6/review.json` (r5 as history) |
| E246 | B2-B4C1-r2 (code) | `adf39de19f855bda24dca366be6d2d35115993d4` | `ab0eb2c970ea…` | `docs/implementation/m3/reviews/codex-b2b4c1-r2/review.json` (r1 as history) |
| E247 | inventory v199 + B2-B4-DESCRIPTIONS-r1 (contract 165) | `039db81fe5558b201d2e22ae92b50a66bf098a76` | `c1778a167502…` | `docs/implementation/m3/reviews/codex-b2b4c1-inventory-v199-r1/review.json`, `docs/implementation/m3/reviews/codex-b2b4-descriptions-r1/review.json` |
| E248 | B2-B4C2-r1 (the blind run) | `c4f99bfe4285ea66e32bd2e4fe04c84c19d52497` | `c0bbdc86affe…` | `docs/implementation/m3/reviews/codex-b2b4c2-r1/review.json` |
| E249 | inventory v200 | `8d29369ea7ec88c5222183cc5c02daec1c08c40c` | `c0e61a4b9ad4…` | `docs/implementation/m3/reviews/codex-b2b4c2-inventory-v200-r1/review.json` |

Check each record's review pins, architecture commit and product commit references against committed bytes and Git ancestry. Each scope must claim nothing beyond its accepted review:
- **E248** states the blind run's result only from the reviewed receipt and census record: 10 of 10 measured and passing, with the smallest margins as recorded.
- **The workspace full-ledger margins stay outstanding.**

**Bindings.**
- The 67 earlier contract bindings and 62 inventory bindings are inherited by value.
- Exactly one contract binding (the description successor) and two inventory bindings (v199 and v200) are appended.
- The result is 68 contract bindings and 64 inventory bindings.

**Decisions.** `decisions.json` and the board's decision table gain `T2-HELD-OUT-MARGIN`. It records the owner's choice exactly, with the record pin, and its execution.

**Validation scopes.** `source.json` `productChangesSinceR98` lists the changed files and records that none is in an inherited validation scope's product map. Check this against the Git diff.

**Changed rows and text:**
- **B row:** the repository-entry margin held; the workspace full-ledger margins outstanding.
- **Item 6.**
- **Cut-off line:** inventory 200 (160 successors), contracts 165, product changed only by B2-b4c1 and B2-b4c2.
- **Line 10:** 249, inventory binding v137–200, and contract binding 98–165.
- **New paragraph:** "accepted work after r98".
- `previousBoard` pins r98, with a byte-identical snapshot.
- The authorities add the r98 review and assent, and the new records' reviews, subjects, assents, plan, owner record, successor records and inventory records.

**Still open:**
- M3 is not complete.
- B2-b is not complete: the workspace full-ledger margins and B2-c remain.
- B3-b, J1, native owner/worker, K1, the SM-11..14 completion round and qualification stay open.

## Output

`review.json` must carry the following, with your independently checked values, plus `nonBlockingObservations`:

```json
{
  "verdict": "ACCEPT",
  "requiredFindings": [],
  "subjectManifestSha256": "e009926bc61c156e975425a11d9af38d7b3787b28a69be084ec0b655a0ae40d0",
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
