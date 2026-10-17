# Review request: IMPLEMENTATION-STATUS-2026-10-16-r105 (shared status board)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-status-board-r105/`).

## Boundaries

- Do not edit either repository, the stage or the control files.
- Do not run the compiler, Cargo, tests or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 held-out entry.
- Do not use other panes and do not delegate.
- Read-only hashing, JSON parsing and Git queries (including `git show <commit>:<path>`) are permitted.

## Subject

- **Stage.** `/tmp/opensip-implementation/status-board-r105-stage`
- **Subject manifest.** `docs/implementation/m3/status/2026-10-16-r105-subject.json` inside the stage: 8690 bytes, SHA-256 `4fe2bcd2e6480ab548b1cb018abe990be759e695f78871b118822c2a26de2369`. Rehash every member.
- **Bases.** Product `56d0eb53a888572dd0129fbc595d0c1be16eaf3a` (clean), architecture `c99177f865c41d8d22881a5587a0d7bc235cb39e`.

## Context

The accepted predecessor is r104 (`docs/implementation/m3/reviews/codex-status-board-r104-r2/`), published at `43402bbc8543b0e4f265bcb4fd482c1c113f562c`, cut-off product `808ad6476fb848f84e732ee233a47229370081f4`.

**Since then:** the C1a plan r4 and its r6 amendment, the D1a plan r2, D1a and its inventory v213, C1a1 and its inventory v214, and the D2a plan r1. You accepted all of them; this round records them.

## What to review

1. **Records.** The 297 accepted r104 records are inherited by value; confirm equality without re-reviewing them. Exactly 8 records are appended, E298 to E305 (`accepted-work.json`). For each, check:
   - its review pin and verdict;
   - its architecture commit and product commits against committed bytes and Git ancestry;
   - its unit record pin, where one exists. The four plans (E298 to E300 and E305) have none.

   Each scope must claim nothing beyond its accepted review, its unit record and, for the D2a plan, the lead assent's carried observations.
2. **Bindings.** The 76 contract and 76 inventory bindings are inherited by value. Exactly two inventory bindings (v213, v214) are appended, giving 78. No contract binding is appended (contracts stay 173).
3. **Validation scopes.**
   - `productChangesSinceR104` lists the changed product files and exactly the four commits of `git rev-list --reverse 808ad64..56d0eb5`. None is in an inherited validation scope's product map; check this.
   - `snapshotAndSupervisorScopes` is new and lists E298 to E305 once.
   - The inherited scope lists are unchanged.
4. **Authorities.** `authorityRepins` is empty. Is no inherited authority moved? The new authorities are:
   - the C1a plans, the D1a plan and the D2a plan, with the D2a plan's lead assent;
   - the appended records' reviews and unit records.
5. **Changed rows and text:**
   - **The C row** (`unit-register.json` and the board table): the C1a plan accepted (r4, amended r6) and C1a1 accepted and bound (inventory v214), with C1a2 to C1a4 open and the next action leading with them.
   - **The D row:** D1a accepted and bound (macOS; inventory v213), and the D2a plan accepted with its codec built; the rest open.
   - No claim that C1, D1, D2, M3-C, M3-D or M3 is complete.
   - **The cut-off line** (inventory 214 / 174 successors, contracts 173), **line 10** (305; v137–214; 98–173), and the new paragraph "accepted work after r104".
   - **`previousBoard`** pins r104 with a byte-identical snapshot.
6. **Still open.** M3 is not complete. Still open:
   - C1a2 to C1a4 (with M3-C r9), C1b and C1c;
   - D1a-L, D1b, D2a's unit, and D2b to D5;
   - J1's composition, C2 to C4, the native owner and worker, and K1;
   - the SM-11..14 completion round and qualification.

## Output

`review.json` must carry the following, with your independently checked values, plus `nonBlockingObservations`:

```json
{
  "verdict": "ACCEPT",
  "requiredFindings": [],
  "subjectManifestSha256": "4fe2bcd2e6480ab548b1cb018abe990be759e695f78871b118822c2a26de2369",
  "scopedRecords": 305,
  "inheritedScopedRecords": 297,
  "appendedScopedRecords": 8,
  "inventory": 214,
  "contractSuccessors": 173,
  "inventoryBindings": 78,
  "contractBindings": 76,
  "validationScopeFilesChangedSinceR104": 0,
  "authorityRepinsAccurate": true,
  "recordCorrectionsAccurate": true,
  "ownerAssentInferred": false,
  "productQualification": false,
  "entirePlanComplete": false
}
```

The lead will give its own assent and run fresh design verification before an architecture-only status commit. Nothing is pushed.
