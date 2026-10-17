# Review request: IMPLEMENTATION-STATUS-2026-10-16-r106 (shared status board)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-status-board-r106/`).

## Boundaries

- Do not edit either repository, the stage or the control files.
- Do not run the compiler, Cargo, tests or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 held-out entry.
- Do not use other panes and do not delegate.
- Read-only hashing, JSON parsing and Git queries (including `git show <commit>:<path>`) are permitted.

## Subject

- **Stage.** `/tmp/opensip-implementation/status-board-r106-stage`
- **Subject manifest.** `docs/implementation/m3/status/2026-10-16-r106-subject.json` inside the stage: 8690 bytes, SHA-256 `a50fd06c09f90ef9600728d31e78190c02f5677e27d07b43e12de914fb271f75`. Rehash every member.
- **Bases.** Product `e937dac74c8e529fee3efb6f84439d05280e48ea` (clean), architecture `3f930927dc288f6bdbd9fe9ec826564ad2f74081`.

## Context

The accepted predecessor is r105 (`docs/implementation/m3/reviews/codex-status-board-r105/`), published at `2894884ef33b0434a7c09029d2f727cf5f7a2524`, cut-off product `56d0eb53a888572dd0129fbc595d0c1be16eaf3a`.

**Since then:** C1a2 and its inventory v215, D2a and its inventory v216, and the D2b plan r3. You accepted all of them; this round records them.

## What to review

1. **Records.** The 305 accepted r105 records are inherited by value; confirm equality without re-reviewing them. Exactly 5 records are appended, E306 to E310 (`accepted-work.json`). For each, check:
   - its review pin and verdict;
   - its architecture commit and product commits against committed bytes and Git ancestry;
   - its unit record pin, where one exists. The D2b plan (E309) has none.

   Each scope must claim nothing beyond its accepted review, its unit record and, for D2a, the unit record's correction of its NBO-1, and for v215, its two review rounds.
2. **Bindings.** The 76 contract and 78 inventory bindings are inherited by value. Exactly two inventory bindings (v215, v216) are appended, giving 80. No contract binding is appended (contracts stay 173).
3. **Validation scopes.**
   - `productChangesSinceR105` lists the changed product files and exactly the four commits of `git rev-list --reverse 56d0eb5..e937dac`. **One is in an inherited scope's product map:** `crates/host/src/lib.rs`, which C1a2 changed by adding two module declarations (10 lines added, none removed). Following the precedent of r89 and r90 (`productChangesSinceR88` and `R89`), the inherited host validation scope pins lib.rs at its own product commit and stays historical there, not claimed on main. Check the diff and that this treatment is right.
   - `snapshotAndSupervisorScopes` lists E298 to E310 once.
   - The inherited scope lists, and every earlier `productChangesSince*` record, are unchanged.
4. **Authorities.** `authorityRepins` is empty. Is no inherited authority moved? The new authorities are:
   - the D2b plan r3 and its lead assent;
   - the appended records' reviews and unit records.
5. **Changed rows and text:**
   - **The C row** (`unit-register.json` and the board table): C1a1 and C1a2 accepted and bound (inventory v215), with C1a3 and C1a4 open and the next action leading with them and the M3-C r9 record.
   - **The D row:** D1a and D2a accepted and bound (inventory v216), and the D2b plan accepted (r3); D2b's sub-units, the D3a plan and the rest open.
   - No claim that C1, D2, M3-C, M3-D or M3 is complete.
   - **The cut-off line** (inventory 216 / 176 successors, contracts 173), **line 10** (310; v137–216; 98–173), and the new paragraph "accepted work after r105".
   - **`previousBoard`** pins r105 with a byte-identical snapshot.
6. **Still open.** M3 is not complete. Still open:
   - C1a3, C1a4 (with M3-C r9), C1b and C1c;
   - D1a-L, D1b, D2b's five sub-units, D3a to D5;
   - J1's composition, C2 to C4, the native owner and worker, and K1;
   - the SM-11..14 completion round and qualification.

## Output

`review.json` must carry the following, with your independently checked values, plus `nonBlockingObservations`:

```json
{
  "verdict": "ACCEPT",
  "requiredFindings": [],
  "subjectManifestSha256": "a50fd06c09f90ef9600728d31e78190c02f5677e27d07b43e12de914fb271f75",
  "scopedRecords": 310,
  "inheritedScopedRecords": 305,
  "appendedScopedRecords": 5,
  "inventory": 216,
  "contractSuccessors": 173,
  "inventoryBindings": 80,
  "contractBindings": 76,
  "validationScopeFilesChangedSinceR105": 1,
  "hostValidationScopeHistoricalOnly": true,
  "authorityRepinsAccurate": true,
  "recordCorrectionsAccurate": true,
  "ownerAssentInferred": false,
  "productQualification": false,
  "entirePlanComplete": false
}
```

The lead will give its own assent and run fresh design verification before an architecture-only status commit. Nothing is pushed.
