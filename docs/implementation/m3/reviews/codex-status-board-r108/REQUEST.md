# Review request: IMPLEMENTATION-STATUS-2026-10-17-r108 (shared status board)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-status-board-r108/`).

## Boundaries

- Do not edit either repository, the stage or the control files.
- Do not run the compiler, Cargo, tests or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 held-out entry.
- Do not use other panes and do not delegate.
- Read-only hashing, JSON parsing and Git queries (including `git show <commit>:<path>`) are permitted.

## Subject

- **Stage.** `/tmp/opensip-implementation/status-board-r108-stage`
- **Subject manifest.** `docs/implementation/m3/status/2026-10-17-r108-subject.json` inside the stage: 8690 bytes, SHA-256 `7d1a709bb28510e3806c376faee463443befe902bba33ef7248a69f4f03f6be1`. Rehash every member.
- **Bases.** Product `01769e93db878836612d9e3d483a054f7ad1da94` (clean; the v223 lock), architecture `8fde46bb981e1304a79aa997ed154cdc4435632a`.

## Context

The accepted predecessor is r107 (round 2, `docs/implementation/m3/reviews/codex-status-board-r107-r2/`), published at `3b4171a8d887a926c5952937a854b822bb07d5e8`, cut-off product `23b3871269c6553c96097084dd412b3aa95dec68`.

**Since then:** 24 architecture commits, every one an accepted record you reviewed. This round records them, one record per commit and in commit order. They are: D2b-0 and its inventory v219, D3a-0, D2b-2 and its v220, C1a4 and its v221, the C1b plan r3, D2b-0b, the C1c plan r4, the C2b-0 plan r3 (with A-C2B0-1), the C1a4 blind gate, the C2a plan r4, the component installation law r5, the C1a4 blind run, D3a-1 (with LD-D3A-18 and LD-D3A-19), the component installation plan r3 (with CI-A1), the combined inventory v222, C1b-0, D3a-2, C1c-0, the C1b plan r6, C2a-1 and the combined inventory v223.

## What to review

1. **Records.** The 316 accepted r107 records are inherited by value; confirm equality without re-reviewing them. Exactly 24 records are appended, E317 to E340 (`accepted-work.json`), one for each architecture commit of `git rev-list --reverse 3b4171a8..8fde46bb`, in that order. For each, check:
   - its review pin and verdict, which is the final round's review;
   - its architecture commit and product commits against committed bytes and Git ancestry. Design units bound as contract successors (D2b-0, D2b-0b, C1b-0) cite both their code commit and their bind commit;
   - its unit record pin, where one exists. The six plan and law records have none; their lead assents are authorities.

   Each scope must claim nothing beyond its accepted review, its unit record or lead assent, and its review rounds. E340 cites the combined v223 review, which supersedes the C1c-0-only review of the same inventory.
2. **Bindings.** The 76 contract and 82 inventory bindings are inherited by value. Exactly three contract bindings (successors 174 to 176) and five inventory bindings (v219 to v223) are appended, giving 79 and 87.
3. **Validation scopes.**
   - `productChangesSinceR107` lists the changed product files and exactly the 20 commits of `git rev-list --reverse 23b3871..01769e9`.
   - **No changed file is in an inherited scope's product map** (`validationScopeMappedFilesChanged` is empty), so no scope changes standing. Check that independently from the scope pins.
   - `snapshotAndSupervisorScopes` lists E298 to E340 once.
   - The inherited scope lists, and every earlier `productChangesSince*` record, are unchanged.
4. **Authorities.** `authorityRepins` is empty. Is no inherited authority moved? The new authorities are:
   - the C1b plan r3 and r6, the C1c plan r4, the C2b-0 plan r3, the C2a plan r4, the component installation law r5 (and the live PROPOSAL.md carrying CI-A1), and its plan r3, each with its lead assent;
   - the appended records' reviews and unit records;
   - r107 round 2's review and lead assent.
5. **Changed rows and text:**
   - **The C row:** C1a1 to C1a4 bound (v221), the C1a4 blind run accepted, the M3-C r9 law record, the C1b plan (r6) with C1b-0 bound (contract 176), and the C1c plan (r4) with C1c-0 bound (v223). C1b-1, C1b-2 and C1c-1 are open, and the open C1b census batch leaves both blind receipts stale until the one reviewed refresh after C1b-2.
   - **The D row:** D2b-0, D2b-0b and D2b-2 bound (v220; contracts 174 and 175), and D3a-0 to D3a-2 bound (v222). D2b-3, D2b-4 and D3a-3 are next.
   - **The C2 row** (`C2a; C2b; C2c`): the C2a plan (r4) with C2a-1 bound (v223), the C2b-0 plan (r3, with A-C2B0-1), and the component installation law (r5) and plan (r3, with CI-A1), with the parent units still open.
   - **The board table:** every row has exactly its header's count of unescaped delimiter pipes (the check of r107 round 2, kept in the prepare), and `unit-register.json` agrees with it.
   - No claim that C1, C2, D2, D3, M3-C, M3-D or M3 is complete.
   - **The cut-off line** (inventory 223 / 183 successors, contracts 176), **line 10** (340; v137–223; 98–176), and the new paragraph "accepted work after r107".
   - **`previousBoard`** pins r107 with a byte-identical snapshot.
6. **Still open.** M3 is not complete. Still open:
   - C1b-1, C1b-2, C1c-1 and the blind refresh;
   - D1a-L, D1b, D2b-3, D2b-4, D3a-3, D3b, D4 and D5;
   - C2a-2 to C2a-4, C2b-0's code, CI-1 to CI-4, C3 and C4;
   - J1's composition, the native owner and worker, and K1;
   - the SM-11..14 completion round and qualification.

## Output

`review.json` must carry the following, with your independently checked values, plus `nonBlockingObservations`:

```json
{
  "verdict": "ACCEPT",
  "requiredFindings": [],
  "subjectManifestSha256": "7d1a709bb28510e3806c376faee463443befe902bba33ef7248a69f4f03f6be1",
  "scopedRecords": 340,
  "inheritedScopedRecords": 316,
  "appendedScopedRecords": 24,
  "inventory": 223,
  "contractSuccessors": 176,
  "inventoryBindings": 87,
  "contractBindings": 79,
  "validationScopeFilesChangedSinceR107": 0,
  "authorityRepinsAccurate": true,
  "recordCorrectionsAccurate": true,
  "ownerAssentInferred": false,
  "productQualification": false,
  "entirePlanComplete": false
}
```

The lead will give its own assent and run fresh design verification before an architecture-only status commit. Nothing is pushed.
