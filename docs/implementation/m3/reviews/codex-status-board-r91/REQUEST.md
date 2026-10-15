# Review request: IMPLEMENTATION-STATUS-2026-10-14-r91 (shared status board)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-status-board-r91/`).

## Boundaries

Do not edit either repository, the stage or control files. Do not run the compiler, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate. Read-only hashing, JSON parsing and Git queries (including `git show <commit>:<path>`) are permitted.

## Subject

- **Stage.** `/tmp/opensip-implementation/status-board-r91-stage`
- **Subject manifest.** `docs/implementation/m3/status/2026-10-14-r91-subject.json` inside the stage: 8647 bytes, SHA-256 `39f497b6d85d4f9ecfbf821c60eb43e13883d9e8e96d449e0d1f8868ac92f375`. Rehash every member.
- **Bases.** Product `2191674d873ed7c0eb4459683dcc29cf7da42440` (clean), architecture `dda9f42ec4727eacd4fcafa773b0a26c16733c74`.

## Context

The accepted predecessor is r90, which you accepted (`docs/implementation/m3/reviews/codex-status-board-r90/`), published at `127a6429fd378957c9621bbb65cc73a18bcc0ad4`. Since then the product changed:
- B3-a's code commit `eea381f5736ae9fef2f280f9c6b36a12d69d8f3b`;
- the separate inventory v190 lock bind `2191674d873ed7c0eb4459683dcc29cf7da42440` (inventory successors 149 to 150; contract successors unchanged at 162).

## What to review

**Records.** The 212 accepted r90 records are inherited by value; confirm equality without re-reviewing them. Exactly three records are appended:

| Record | Unit | Architecture | Product | Review |
| --- | --- | --- | --- | --- |
| E213 | B3A-PLAN-r1 | `70950d53ce1ab79c99c51c5340b5d101b397801b` | none | `docs/implementation/m3/reviews/codex-b3a-plan-r1/review.json` (your ACCEPT, first round) |
| E214 | B3-A-r1 (code) | `8597ffe8e2beece34c8bbbcd48ee91054d315a0a` | `eea381f5736a…` | `docs/implementation/m3/reviews/codex-b3a-r1/review.json` (your ACCEPT-UNIT, first round) |
| E215 | B3-A-inventory-v190 | `dda9f42ec4727eacd4fcafa773b0a26c16733c74` | `2191674d873e…` | `docs/implementation/m3/reviews/codex-b3a-inventory-v190-r1/review.json` (your ACCEPT-UNIT) |

Check each record's review pin, architecture commit and product commit references against committed bytes and Git ancestry. Each scope must claim nothing beyond its accepted review. There is no law change in this round, so no `acceptedLawDeltaScopes` row is added.

**Inherited validation scopes.** B3-a changed only security files (`grants.rs` and its tests and vectors, a private module declaration in `crates/security/src/lib.rs`, and `ProjectChainPolicy::from_grants` with its test) and added `tools/security/storage_choice_vectors.py`. `source.json` `productChangesSinceR90` records that none of these is in an inherited validation scope's product map. Check:
- that the product diff since r90 is exactly those files plus `design-lock.json`;
- that no inherited scope's mapped file changed;
- that the statement is honest.

**Changed rows and text:**
- **B row** (front door and `unit-register.json`): B1-a, B1-b and B3-a bound. The evidence appends the three scopes. The next action is B2-a, with B2-b and B3-b consuming the B3-a waiver and groups, J1 composing the analysis path, and J's first source-derived write calling the S3.1 choice. Every other wait is kept.
- **Next actions:** item 6 updated.
- **Cut-off line:** product `2191674d`, inventory **190** (150), contracts 162, product changed only by B3-a.
- **Line 10:** the 215 count and the inventory binding range v137–190.
- **New paragraph:** "accepted work after r90".

**Counts and bindings:**
- There are 215 scoped records.
- There are 54 inventory bindings: the 53 earlier ones inherited by value, and the new one equal to the lock's last inventory successor.
- The 65 contract bindings are unchanged.
- `previousBoard` pins the r90 board at `127a6429f…`, with a byte-identical history snapshot.
- The authorities add the r90 review and assent and the new units' reviews, subjects, assents and plan.

**Still open:** M3 is not complete. B3-a's records and choice have no consumer or caller (B2-b, B3-b and J). B1-a and B1-b have no caller (J1). Native owner/worker, K1, the SM-11..14 completion round and qualification stay open.

## Output

`review.json` must carry the following, with your independently checked values, plus `nonBlockingObservations`:

```json
{
  "verdict": "ACCEPT",
  "requiredFindings": [],
  "subjectManifestSha256": "39f497b6d85d4f9ecfbf821c60eb43e13883d9e8e96d449e0d1f8868ac92f375",
  "scopedRecords": 215,
  "inventory": 190,
  "contractSuccessors": 162,
  "productCodeChangedSinceR90ByB3aOnly": true,
  "b3aPlanCodeAndInventoryRecordedExactly": true,
  "noInheritedValidationScopeFileChanged": true,
  "ownerAssentInferred": false,
  "productQualification": false,
  "entirePlanComplete": false
}
```

The lead will give its own assent and run fresh design verification before an architecture-only status commit. Nothing is pushed.
