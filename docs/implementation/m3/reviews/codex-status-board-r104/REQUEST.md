# Review request: IMPLEMENTATION-STATUS-2026-10-16-r104 (shared status board)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-status-board-r104/`).

## Boundaries

- Do not edit either repository, the stage or the control files.
- Do not run the compiler, Cargo, tests or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 held-out entry.
- Do not use other panes and do not delegate.
- Read-only hashing, JSON parsing and Git queries (including `git show <commit>:<path>`) are permitted.

## Subject

- **Stage.** `/tmp/opensip-implementation/status-board-r104-stage`
- **Subject manifest.** `docs/implementation/m3/status/2026-10-16-r104-subject.json` inside the stage: 8690 bytes, SHA-256 `9a6fe0d79a98c41bef98cc4e8dad42d9fad09e903ae64a1d2d03058e5e38d940`. Rehash every member.
- **Bases.** Product `808ad6476fb848f84e732ee233a47229370081f4` (clean), architecture `8310f16a0e7fb7e009241bec2e797c2b452c4aee`.

## Context

The accepted predecessor is r103 (`docs/implementation/m3/reviews/codex-status-board-r103-r2/`, after round `codex-status-board-r103`), published at `10cb57bce72c6613d77bf0734fe5a0526bdbd0cb`, cut-off product `9501ec9d167200e82580fbeab73afd2d1cbd7159`.

**Since then:** law M3-B r10 (O-1), S10b (contract successor 172), B2-c2b and its description successor (contract successor 173). All were accepted by you; this round records them.

## What to review

1. **Records.** The 293 accepted r103 records are inherited by value; confirm equality without re-reviewing them. Exactly 4 records are appended, E294 to E297 (`accepted-work.json`). For each, check:
   - its review pin and verdict;
   - its architecture commit and product commits against committed bytes and Git ancestry;
   - its unit record pin, where one exists (E294, a law, has none).

   Each scope must claim nothing beyond its accepted review and unit record.
2. **Bindings.** The 74 contract and 76 inventory bindings are inherited by value. Exactly two contract bindings (172, 173) are appended, giving 76; no inventory binding (inventory stays v212).
3. **Validation scopes.** `productChangesSinceR103` lists the changed product files and exactly the three commits of `git rev-list --reverse 9501ec9..808ad64`. None is in an inherited validation scope's product map. Check this. `configurationDiscoveryScopes` is the 88 inherited entries plus E294 to E297 once.
4. **Authority repin.** `source.json` `authorityRepins` repins one authority, the live `config-discovery-b/PROPOSAL.md`, which M3-B r10's publication changed. Is that the only moved authority, and is the repin right?
5. **Changed rows and text:**
   - **The B row** (`unit-register.json` and the board table): B2-c2b closes O-1 (M3-B r10; S10b, contract 172; descriptions, contract 173), and the next action no longer lists O-1 as open. No claim that B2, M3-B or M3 is complete.
   - **Item 6:** the O-1 sentence before "J1 is next".
   - **The cut-off line** (inventory 212 / 172 successors, contracts 173), **line 10** (297; v137–212; 98–173), and the new paragraph "accepted work after r103".
   - **`previousBoard`** pins r103 with a byte-identical snapshot.
6. **Still open.** M3 is not complete. Still open: J1's composition (through C1 custody and J2b), C1 to C4, native owner/worker, K1, the SM-11..14 completion round and qualification.

## Output

`review.json` must carry the following, with your independently checked values, plus `nonBlockingObservations`:

```json
{
  "verdict": "ACCEPT",
  "requiredFindings": [],
  "subjectManifestSha256": "9a6fe0d79a98c41bef98cc4e8dad42d9fad09e903ae64a1d2d03058e5e38d940",
  "scopedRecords": 297,
  "inheritedScopedRecords": 293,
  "appendedScopedRecords": 4,
  "inventory": 212,
  "contractSuccessors": 173,
  "inventoryBindings": 76,
  "contractBindings": 76,
  "validationScopeFilesChangedSinceR103": 0,
  "authorityRepinsAccurate": true,
  "recordCorrectionsAccurate": true,
  "ownerAssentInferred": false,
  "productQualification": false,
  "entirePlanComplete": false
}
```

The lead will give its own assent and run fresh design verification before an architecture-only status commit. Nothing is pushed.
