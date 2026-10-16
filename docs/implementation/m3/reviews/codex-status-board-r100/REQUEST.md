# Review request: IMPLEMENTATION-STATUS-2026-10-16-r100 (shared status board)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-status-board-r100/`).

## Boundaries

- Do not edit either repository, the stage or the control files.
- Do not run the compiler, Cargo, tests or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 held-out entry.
- Do not use other panes and do not delegate.
- Read-only hashing, JSON parsing and Git queries (including `git show <commit>:<path>`) are permitted.

## Subject

- **Stage.** `/tmp/opensip-implementation/status-board-r100-stage`
- **Subject manifest.** `docs/implementation/m3/status/2026-10-16-r100-subject.json` inside the stage: 8689 bytes, SHA-256 `f50ea8df9c229832aaffddb884ba9978b2b6eee0baed1228832f15562ee07ee0`. Rehash every member.
- **Bases.** Product `01c73e2d54e037e3e41adc2f5d97df854552921e` (clean), architecture `959e8726080ee226410a614dc5e631305cefa0f4`.

## Context

The accepted predecessor is r99 (`docs/implementation/m3/reviews/codex-status-board-r99/`), published at `ecd3c5a52a2faa10c91ac1ef96b62cde5a8152a0`.

**Since then:**
- **The B2-c plan r2** was published at `7c55cdab1bd1c24144e2222496296e10a54dde34`.
- **B2-c0, the current native unit reference,** was bound as contract successor 166. Lock `b0154f08f9193bbf3ca368420c2dae2006c11661`, architecture `b6e42226f103642306e8c0cd1ac2ddc1b633587a`. It carries an NE line-838 passage override, LD-B2C0-1.
- **B2-c1, the native unit instrument,** was committed at `ed44559f06c5d1e10af4579415e75a49e39a9ffa`.
- **Inventory v201** was bound at `01c73e2d54e037e3e41adc2f5d97df854552921e`.

There is no law change.

## What to review

**Records.** The 249 accepted r99 records are inherited by value; confirm equality without re-reviewing them. Exactly four records are appended:

| Record | Unit | Architecture | Product | Review |
| --- | --- | --- | --- | --- |
| E250 | B2C-PLAN-r2 | `7c55cdab1bd1c24144e2222496296e10a54dde34` | none | `docs/implementation/m3/reviews/codex-b2c-plan-r2/review.json` (r1 as history) |
| E251 | B2-C0-REFERENCE-r2 (contract 166) | `b6e42226f103642306e8c0cd1ac2ddc1b633587a` | `b0154f08f919…` (lock) | `docs/implementation/m3/reviews/codex-b2c0-reference-r2/review.json` (r1 as history) |
| E252 | B2-C1-r3 (code) | `9ea5ad18ba56b44434bc29bc10717cf8c3f199c9` | `ed44559f06c5…` | `docs/implementation/m3/reviews/codex-b2c1-r3/review.json` (r1 and r2 as history) |
| E253 | B2-C1-inventory-v201 | `959e8726080ee226410a614dc5e631305cefa0f4` | `01c73e2d54e0…` | `docs/implementation/m3/reviews/codex-b2c1-inventory-v201-r1/review.json` |

Check each record's review pin, architecture commit and product commit references against committed bytes and Git ancestry. Each scope must claim nothing beyond its accepted review. **E251** states the NE line-838 override.

**Bindings.**
- The 68 earlier contract bindings and 64 inventory bindings are inherited by value.
- Exactly one contract binding (166) and one inventory binding (v201) are appended.
- The result is 69 contract bindings and 65 inventory bindings.

**Validation scopes.** `source.json` `productChangesSinceR99` lists the changed files. Exactly `crates/host/src/lib.rs` is in an inherited validation scope's product map: the combined host scope, historical at its own commit, as in r89, r90 and r95. Its added lines (`libRsAddedLines`) must be only comments, a dead-code-allowed library module declaration and a test-only, macOS-only test module. Check this against the Git diff.

**Changed rows and text:**
- **B row:** B2-b's state unchanged; B2-c in progress with B2-c0 and B2-c1; M3-B r8 and B2-c2 next.
- **Item 6.**
- **Cut-off line:** inventory 201 (161 successors), contracts 166, product changed only by the B2-c0 lock, B2-c1 and v201.
- **Line 10:** 253, inventory binding v137–201, and contract binding 98–166.
- **New paragraph:** "accepted work after r99".
- `previousBoard` pins r99, with a byte-identical snapshot.
- The authorities add the r99 review and assent, and the new records' reviews, plan, successor, assents and inventory records.

**Still open:**
- M3 is not complete.
- B2-b is not complete: workspace full-ledger margins.
- B2-c is not complete: r8 and B2-c2.
- B2-d, B3-b, J1, native owner/worker, K1, the SM-11..14 completion round and qualification stay open.

## Output

`review.json` must carry the following, with your independently checked values, plus `nonBlockingObservations`:

```json
{
  "verdict": "ACCEPT",
  "requiredFindings": [],
  "subjectManifestSha256": "f50ea8df9c229832aaffddb884ba9978b2b6eee0baed1228832f15562ee07ee0",
  "scopedRecords": 253,
  "inheritedScopedRecords": 249,
  "appendedScopedRecords": 4,
  "inventory": 201,
  "contractSuccessors": 166,
  "inventoryBindings": 65,
  "contractBindings": 69,
  "productCodeChangedSinceR99ByB2c1Only": true,
  "b2cPlanB2c0B2c1V201RecordedExactly": true,
  "ne838OverrideStated": true,
  "hostLibRsHistoricalScopeSound": true,
  "ownerAssentInferred": false,
  "productQualification": false,
  "entirePlanComplete": false
}
```

The lead will give its own assent and run fresh design verification before an architecture-only status commit. Nothing is pushed.
