# Review request: IMPLEMENTATION-STATUS-2026-10-16-r107 (shared status board), round 2

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-status-board-r107-r2/`).

## Boundaries

- Do not edit either repository, the stage or the control files.
- Do not run the compiler, Cargo, tests or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 held-out entry.
- Do not use other panes and do not delegate.
- Read-only hashing, JSON parsing and Git queries (including `git show <commit>:<path>`) are permitted.

## Subject

- **Stage.** `/tmp/opensip-implementation/status-board-r107-r2-stage`
- **Subject manifest.** `docs/implementation/m3/status/2026-10-16-r107-subject.json` inside the stage: 8690 bytes, SHA-256 `56e1aa6825fa122d1923b1c95f4e12b29969ee67eaee184ff3481408c354ee05`. Rehash every member.
- **Bases.** Product `23b3871269c6553c96097084dd412b3aa95dec68` (clean), architecture `ae83833d05d956a0562e188f0ad04fc37a63944b`.

## Context

The accepted predecessor is r106 (`docs/implementation/m3/reviews/codex-status-board-r106/`), published at `24fbf182c3d3144d8a159bee7d9d2a0e6418996c`, cut-off product `e937dac74c8e529fee3efb6f84439d05280e48ea`.

**Since then:** the D3a plan r4 (with the LD-D3A-17 amendment), C1a3 and its inventory v217, the M3-C r9 law record, D2b-1 and its inventory v218. You accepted all of them; this round records them.

## Round 2

Your round 1 (`/tmp/opensip-implementation/reviews/codex-status-board-r107/`, subject `02119f5f…`) returned REQUIRED-FINDINGS with one finding. **STATUS-R107-RF-1:** the D row's evidence carried an unescaped pipe in the scratch-retention reason, which split its GFM cell. The fix:
- The reason now reads "io-failure with its errno (K2 Errno) or work-exhausted with no errno", in the board row, in `unit-register.json` and in E311's scope, so all three agree. The meaning is unchanged.
- The D row has four cells, and its next action (from "D1a (macOS), D2a and D2b-1 are accepted and bound") is the final cell.
- The prepare now checks every table in the board: each row must have exactly its header's count of unescaped delimiter pipes, and no unit-register field may contain a pipe. The same check fails on round 1's board.

Round 1's stage and review are unchanged. Nothing else differs from round 1 except the subject pins this fix moves; check that too.

## What to review

1. **Records.** The 310 accepted r106 records are inherited by value; confirm equality without re-reviewing them. Exactly 6 records are appended, E311 to E316 (`accepted-work.json`). For each, check:
   - its review pin and verdict;
   - its architecture commit and product commits against committed bytes and Git ancestry;
   - its unit record pin, where one exists. The D3a plan (E311) and the M3-C r9 law record (E314) have none; their lead assents are authorities.

   Each scope must claim nothing beyond its accepted review, its unit record or lead assent, and its review rounds. In particular, E314's caps are conditional on C1a4, and no snapshot profile exists.
2. **Bindings.** The 76 contract and 80 inventory bindings are inherited by value. Exactly two inventory bindings (v217, v218) are appended, giving 82. No contract binding is appended (contracts stay 173).
3. **Validation scopes.**
   - `productChangesSinceR106` lists the changed product files and exactly the four commits of `git rev-list --reverse e937dac..23b3871`.
   - **One changed file is in an inherited scope's product map:** `crates/host/src/lib.rs`, which C1a3 changed by adding one module declaration with its comment (4 lines added, none removed). Following the precedent of r89, r90 and r106, the inherited host validation scope pins lib.rs at its own product commit and stays historical there, not claimed on main. Check the diff and that this treatment is right.
   - D2b-1's change to `crates/identity/src/lib.rs` (11 lines appended) is in no scope map.
   - `snapshotAndSupervisorScopes` lists E298 to E316 once.
   - The inherited scope lists, and every earlier `productChangesSince*` record, are unchanged.
4. **Authorities.** `authorityRepins` is empty. Is no inherited authority moved? The new authorities are:
   - the D3a plan r4 and its lead assent;
   - the M3-C r9 record (`c1a-r9/RECORD-r9.md`) and its lead assent;
   - the appended records' reviews and unit records;
   - r106's review and lead assent.
5. **Changed rows and text:**
   - **The C row** (`unit-register.json` and the board table): C1a1 to C1a3 accepted and bound (inventory v217); the M3-C r9 law record accepted, with its caps conditional on C1a4; C1a4 open; and the next action leading with C1a4 and the blind refresh it makes necessary.
   - **The D row:** D1a, D2a and D2b-1 accepted and bound (inventory v218); the D2b plan (r3) and the D3a plan (r4, with LD-D3A-17) accepted. D2b-0, D2b-2 to D2b-4, D3a-0 to D3a-3 and the rest are open.
   - No claim that C1, D2, D3, M3-C, M3-D or M3 is complete.
   - **The cut-off line** (inventory 218 / 178 successors, contracts 173), **line 10** (316; v137–218; 98–173), and the new paragraph "accepted work after r106".
   - **`previousBoard`** pins r106 with a byte-identical snapshot.
6. **Still open.** M3 is not complete. Still open:
   - C1a4 (with the blind refresh), C1b and C1c;
   - D1a-L, D1b, D2b-0, D2b-2 to D2b-4, D3a-0 to D3a-3, D3b, D4 and D5;
   - J1's composition, C2 to C4, the native owner and worker, and K1;
   - the SM-11..14 completion round and qualification.

## Output

`review.json` must carry the following, with your independently checked values, plus `nonBlockingObservations`:

```json
{
  "verdict": "ACCEPT",
  "requiredFindings": [],
  "subjectManifestSha256": "56e1aa6825fa122d1923b1c95f4e12b29969ee67eaee184ff3481408c354ee05",
  "scopedRecords": 316,
  "inheritedScopedRecords": 310,
  "appendedScopedRecords": 6,
  "inventory": 218,
  "contractSuccessors": 173,
  "inventoryBindings": 82,
  "contractBindings": 76,
  "validationScopeFilesChangedSinceR106": 1,
  "hostValidationScopeHistoricalOnly": true,
  "authorityRepinsAccurate": true,
  "recordCorrectionsAccurate": true,
  "ownerAssentInferred": false,
  "productQualification": false,
  "entirePlanComplete": false
}
```

The lead will give its own assent and run fresh design verification before an architecture-only status commit. Nothing is pushed.
