GROK2 re-review: **M3-B r2**, OpenSIP's M3 configuration and discovery law, after your r1 findings. This is a **law and fact** review. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/grok2-config-discovery-b-r2.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- No product builds or test runs. A timing-sensitive crash-matrix run may be using this machine, so run no `cargo`, no tests and no lead sets.
- Never touch the real home. `~/Library/Application Support/OpenSIP` must stay absent. If you run `git` anywhere, redirect `HOME` to a private 0700 scratch directory and turn hooks off.
- Never read the private 413 UUID fixture.
- If you compute digests, use read-only scratch scripts under your review directory.
- The product is read at main `30c5db1`, and every cited product file is byte-identical at `3e64266`. Read files or use `git show`; change nothing.

## Subject

The pins are in `hashes.txt`. The files are untracked in arch until acceptance.
- `docs/implementation/m3/config-discovery-b/PROPOSAL.md` (r2) is the subject of `subjectSha256`.

**Previous round.**
- The r1 bytes are preserved as `PROPOSAL-r1.md` (`da014f54…`, the sha you reviewed).
- Your r1 review is `/tmp/opensip-implementation/reviews/grok2-config-discovery-b-r1/`, copied to `docs/implementation/m3/reviews/grok2-config-discovery-b-r1/`. It raised two required findings and two non-blocking observations.
- r2's "r2 changes" table maps each finding to its change. Diff r1 against r2 and confirm nothing else changed in substance.

## What r2 changes

1. **RF-1: a supplied `workspaceRoots` array suppresses reader membership.** Item 20 now has two branches, chosen by whether the resolved semantic configuration holds an admitted `discovery.workspaceRoots` array (AQ:115).
   - **Branch A, the array is present.** It may come from the project or local layer, or from `--workspace-root`, which is the flags layer of the same field (item 2). The array alone decides membership. Discovery is restricted to exactly its roots, never widened into a scan (NE:917-921; SLM:771-785). The readers declare no member. They record only links whose directories lie inside members the array already admitted; any other reader entry is recorded as dropped.
   - **Branch B, the array is absent.** Only then do the readers declare members.
   - The same rule now appears in:
     - item 13's unit-source row;
     - item 22's Config2-join bullet, which keeps "exactly those roots, never widened";
     - item 23's `--workspace-root` row;
     - a new item 24 row for a dropped reader entry;
     - the forbidden substitutes;
     - S3's content cell in item 25.
   - Item 20's controls add the project-layer, local-layer and CLI cases.
2. **RF-2: the I1:388 conflict.**
   - Item 10 no longer cites I1:381-388 as standing in full. It says that I1:383-386 stands, and that **I1:388's clause that X12 r3's order stands is withdrawn by S2 (X12 r4)**; I1:388's other clauses stand.
   - Item 10 now gives **S2's exact text**, a replacement for X12:125-130, with a "Withdrawal recorded" paragraph. Item 25's S2 row says so.
   - **Found while fixing it:** X12:136 says pack admission "is pure and runs before any custody", which carries the same order. S2 records that its ordering sense is superseded, and keeps its dependency correction (X12 does not depend on X1). **Confirm that this is a faithful extension of your RF-2, not a new change.**
3. **NBO-1.** Item 12 now says the census bounds objects and edges only. Bytes are bounded by item 19's member cap, X2:272's ceilings and SL:126-127's 4 MiB file-custody limit.
4. **NBO-2.** Item 22 now states that U-9 is unchanged. Units inside members count as surviving units; its one fallback unit is at W's root `""`; a member is never a second fallback site. S3's cell cites item 22.

**Unchanged:** every other decision, the units, their sizes and order, the successor list apart from the S2 and S3 cells, and the findings F1-F14.

## Decide

1. Is RF-1 resolved? In particular, is branch A's link rule (links only into array-admitted members, everything else dropped) faithful to NE:917-921 and SLM:771-785?
2. Is RF-2 resolved? Is S2's text narrow enough, and is the X12:136 reading right?
3. Are NBO-1 and NBO-2 handled correctly?
4. Does r2 introduce anything new that is wrong?

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: ACCEPT or REQUIRED-FINDINGS;
- `"requiredFindings"`: each with id, location, problem or claim, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectSha256"`: PROPOSAL.md's sha256.

This is a law review, not a `verify_design` unit. The design units B-S1 and B-S2 and the S9 remedy text will each need an `ACCEPT-DESIGN-UNIT` review of their own. Do not commit.
