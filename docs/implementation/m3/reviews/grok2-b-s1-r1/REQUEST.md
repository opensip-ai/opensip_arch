GROK2 review: **B-S1**, round 1. B-S1 is the contract successor that accepted law M3-B r2 names as S3, carrying M3-C's SX-1. This is a **design-unit (contract successor)** review. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT-DESIGN-UNIT** or **REQUIRED-FINDINGS**.

Write only under `/tmp/opensip-implementation/reviews/grok2-b-s1-r1`.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation. Run git only read-only.
- No cargo, no builds, no tests, no crash-matrix binary or checker. A timing-sensitive crash-matrix lead set may be using this machine.
- If you run anything, use only the three evidence scripts named below, or read-only commands, with `nice -n 19` and `python3.14 -I -B` (`/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14`). Use a private 0700 `TMPDIR` under your review directory if you need scratch files.
- Never touch the real home: `~/Library/Application Support/OpenSIP` stays absent. Do not read or create it.
- Never read the private 413 UUID fixture.


**M3-C citations (lead note).** `MC:n` line citations refer to M3-C r6 **with its acceptance note**, the bytes at arch commit `3590205a9`. Read them with `git show 3590205a9:docs/implementation/m3/snapshot-plan-c/PROPOSAL.md` (sha256 `a2f16b7b…`). Run git read-only with a private `HOME`. The live path now holds the M3-C r7 draft, a narrow row-8 amendment in review with CODEX2, which doesn't touch SX-1 or the D15 rows. `PROPOSAL-r6.md` is the same text without the two-line note, so its lines are two lower.

## Subject

The pins are in `hashes.txt`. The subject manifest is `docs/implementation/m3/config-discovery-b/b-s1-subject.json` (1,948 bytes, `f94f5c1d4861759737fc4ef11f7b05c6ba2467e32c20669849d79310eb169899`). Its members, all under `docs/implementation/m3/config-discovery-b/b-s1/`:
- `README.md`: the proposal. Read it first.
- `successor.json`: the record, with 25 passage overrides and no supersession.
- `PASSAGES.md`: every override, rendered with the exact `before` and `after`. It is generated from the same data as the record.
- `schemas/security-lifecycle.schemas.v1.b-s1-additions.json` and `schemas/native-evidence.schemas.v2.b-s1-additions.json`: the V3 discovery records, added to their bundles.
- `registry/workspace-declaration-readers.v1.json`: the closed declaration-reader registry.
- `evidence/build_b_s1.py`, `evidence/check_b_s1.py`, `evidence/verify_scratch.py`.

All of these are untracked in arch until acceptance. `b-s1-unit.json` next to the manifest is the lead's draft, marked `DRAFT-PENDING-REVIEW`. It is not part of the subject.

**S9 is not in this unit.** M3-B's units table puts S9's remedy text in B-S1 (MB:841). By the lead's decision it is split into its own unit, **B-S9** (`docs/implementation/m3/config-discovery-b/b-s9/`, in its own review `grok2-b-s9-r1`). B1-a's dependency "B-S1 (S9 text)" (MB:843) becomes "B-S9". B-S1 touches no native-model file.

**The law it serves.** Read `docs/implementation/m3/config-discovery-b/PROPOSAL.md`, M3-B r2, which you accepted (`92e65825…`), in full:
- items 19, 20, 22 and 24;
- item 25's S3 row (MB:774);
- the units table (MB:839-857).

For SX-1, read `docs/implementation/m3/snapshot-plan-c/PROPOSAL.md` items 1 and 2 (MC:138, MC:218) and the successor row (MC:1047). M3-C r6 is accepted by CODEX2 (`8274bca1…`), and r6 did not change SX-1.

Also read `docs/implementation/m2/project-root-x2/PROPOSAL.md`, X2 r9, accepted, for item 6b, item 8's D15 subjects and the r9 header's remedy note (X2:74, X2:88-89).

**The product** is `/Users/sb/code/opensip-ai/opensip` at main `e093e90` (the F8b binding; 77 contract successors), read-only. `verify_scratch.py --rev e093e90` reads that commit's lock and tool through `git show`.

## What it does

1. **SX-1.** `.opensip` at the selected root and at each admitted D15 member root is an exact discovery anchor, with reason `opensip-custody-state`. It is never source, never inventoried and never a read. It is observed only from its parent's listing. When observed as a directory, it is recorded in `prunedTrees`. It is always a conventional excluded prefix. The overrides are SL:195, SL:205, SL:274, NE:714, NE:939 and IE:552.
2. **D15 in security S3.** A new "Multi-repository workspaces" paragraph follows SL:185. It covers:
   - the shape;
   - MB item 20's two branches, with an array present suppressing reader membership;
   - members as non-boundaries;
   - `memberConfigs`;
   - flag reach;
   - refusals and disclosures;
   - the V3 records.

   Consistency edits are at SL:109, 166, 168, 180, 215, 262, 286 and 298. The member cap and its remedy are at SL:1323.
3. **D15 in native §1.4.**
   - U-8 consumes `AdmittedBoundaryInventoryV3` (NE:822, NE:824). A D15 paragraph follows NE:863: members are not boundaries, the subset test is unchanged, the `vcs-tree` anchor test applies, and U-9 and U-6 are stated unchanged.
   - The Config2 join gains a D15 paragraph after NE:931. "Exactly those roots, never widened" is kept.
   - The V3 names are at NE:719 and NE:730-731, and H-8 at NE:4135.
4. **Records.** These are additions only, each a V2 record plus a declared delta: `DiscoveryProvenanceV3`, `DiscoveryResultV3`, `AdmittedBoundaryInventoryV3` (both bundles), `PrunedTreeRowV3` and `PrunedTreeV3`, `UnitBoundariesV2`, `UnitDiscoveryV3`, and the D15 `$defs`.
5. **Reader registry.** `cargo-config-patch@1` and `npm-workspaces-members@1`, with their carriers, grammar, placement, the cap's count, dispositions, links and closed `unresolved` reasons.

## The lead's runs

- **`build_b_s1.py`** reproduces identical bytes on a second run.
- **`check_b_s1.py`** passes. It covers:
  - every override's `before` against the parents;
  - that the record has no supersession;
  - that the V3 deltas are exact;
  - that 36 `#/` references resolve in the merged bundles;
  - positive and negative sample instances;
  - that the registry's ids and reasons equal the schema enums.
- **`verify_scratch.py`** passes at `--rev e093e90` and on the main checkout:
  - the lock goes from 77 to 78 contract successors, with 25 overrides and no supersession;
  - no bound successor overrides any of the same lines;
  - the selected inventory and inheritance are unchanged;
  - on the checkout, 40 generation sources are verified.
- **A scratch check outside the subject** appended B-S1, B-S2 and B-S9 together to the `e093e90` lock. It passes with 80 successors, so the three units do not conflict.

## Decide

1. **Faithfulness.**
   - Do the overrides and new text state MB items 19, 20, 22 and 24 exactly, with nothing widened? Check against MB's forbidden substitutes (MB:869-898).
   - Is RF-1's rule kept everywhere: a present array suppresses reader membership, and discovery stays exactly the named roots?
   - Is M3-C's SX-1 landed as MC states it?
2. **Judgment calls.** Rule on the README's "Points for the reviewer" (R1 and R6 moved to B-S9):
   - **R2:** MB item 22 and item 24 row 1 against item 24 row 3. The lead keeps `JOIN_CROSSES_NESTED_REPOSITORY`, so projects without D15 keep today's refusal (LD-6). Please rule.
   - **R3:** SX-1's conventional prefix, and version 3 for every project (LD-3, LD-4).
   - **R4:** the cap's count and branch reading, and membership by placement (LD-7, LD-8).
   - **R5:** reader dispositions against MB item 20 (LD-10 and the registry).
   - **R7:** the `vcs-tree` anchor test (LD-13).
3. **Records.**
   - Is each V3 record exactly its V2 record plus the declared delta?
   - Are the new `$defs` closed and bounded?
   - Do the field names match MB item 22 (`memberRepositories[].declaredBy[{source, readerId?, readerVersion?, path?, contentSha256?}]`, `workspaceDeclarations[].unresolved`)?
4. **Registry.** Is it closed and complete for FW-13's row (MB:251)? Can a reader run, write, evaluate a glob or declare a member while an array is present?
5. **Conflicts.** Is the README's list of conflicts and reconciliations complete and right? That covers M3-B r2, including the S9 split, M3-C r6 and X2 r9. Is anything else frozen in the way?
6. **Form.** Is the successor well formed for selection? Anything else wrong?

## Output

Write REVIEW.md and review.json. review.json must contain:
- `"verdict"`: `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`: each with id, location, problem, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectManifestSha256"`: a single string, the sha256 of `b-s1-subject.json`. The lead's value is `f94f5c1d4861759737fc4ef11f7b05c6ba2467e32c20669849d79310eb169899`;
- `"successor"`: `{path, bytes, sha256}` of `b-s1/successor.json`. The lead's value is 26,832 bytes, `8faa376e543493a14e4db9b5cb0aa799b71a0759192f7866f4f21b1ddee266c3`.

This is a contract successor, so it has no `inventoryCandidateAssessment`. If you would change any passage, give the exact replacement text. Do not commit.
