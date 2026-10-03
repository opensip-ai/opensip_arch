Grok review: law X9 r16, an amendment found while preparing X9-6, the M2 exit gate. Claude Opus 5.5 leads. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

**Rules:**
- No repository edits, commits, pushes or delegation.
- Write only under /tmp/opensip-implementation/reviews/grok-crash-matrix-x9-r16.
- Run git read-only, against product main `2967905` (X9-0 to X9-5, F7 and L1 integrated).
- The X9-6 worktree `/Users/sb/code/opensip-ai/opensip-x9-6` is uncommitted and may be read. It has the two-target `check`, the `coverage` command and `x9_6_matrix`. The coverage output is at `/private/tmp/claude-501/-Users-sb-code/8baf40a9-970f-46bc-bd52-a3dde4a615a1/scratchpad/x96/coverage.json`.
- Never touch the real home. Never read the 413 fixture.
- This is a law review: don't run lead sets.

**Subject:** `docs/implementation/m2/crash-matrix-x9/PROPOSAL.md`, 185750 bytes, sha256 `f08efe95deba681f2940a043c80c91b4faae4e4c804ca5865c024e0e083c0a85`. **Previous:** `docs/implementation/m2/crash-matrix-x9/PROPOSAL-r15.md`, the accepted r15 (`0d195ff1…`). The current file also carries r15's "ACCEPTED" stamp.

## What r16 changes

**G-A, coverage.** The union census is storage 259 points and host 218, giving a union of 321 points and a kill set of 383. The rows of X9-2 to X9-5 kill 333 of those points, leaving 50 with no row. These are:
- `x4.checkpoint` 12;
- `x3c.object` 9;
- `x2.lease` 6;
- seal 5;
- `x7.delivery` 4;
- evidence 3;
- finish 3;
- fence 2;
- publish 2;
- gate 2;
- sweep 2.

Each of the 50 gets a process-death row, placed by its crash window and taking the expected values of the existing row for that window (F02, F07, F11, F13, F14, the F19 script, F53, F16/F17). None is exempted. The new rows carry `"unit": "X9-6"`.

**One new scored prediction:** R2's witness action is OK in F11's window, from F10's row and X3b item 4.

**G-A2, the occurrence-count risk:** checked; it does not occur.

**G-B, evidence layout:**
- lead-1's full storage and host `matrix.json`, census traces and `runs/`;
- lead-2's two `matrix.json` files;
- the `check` output;
- the release-absence record;
- `hashes.txt`;
- LFS when `runs/` exceeds 64 MB per target.

**G-C, census order:** recorded.

**G-D, release order:** asserted in every commit child, for acquisition and for release. A violation fails the run.

There are 15 in-place notes, and the title is now r16.

## Decide

1. Is each of the 50 rows' expected value the owning law's outcome for its window? Spot-check the placement against the census trace order and the owning laws.
2. Is "no exemption" right? Should any point be covered by an equivalent rather than killed?
3. Are G-B and G-D sound?
4. Does r16 change nothing else?

Write REVIEW.md and review.json. review.json needs:
- "verdict";
- "requiredFindings";
- "noAcceptedOutcomeChanged";
- "subjectSha256";
- "subject" (path, bytes, sha256);
- "preservedSnapshot": the accepted r15, `PROPOSAL-r15.md`.

Do not commit.
