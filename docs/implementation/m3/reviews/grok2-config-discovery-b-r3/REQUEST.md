GROK2 review: **M3-B r3**, OpenSIP's M3 configuration and discovery law, as a **record revision** after your r2 acceptance. This is a **law and fact** review. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/grok2-config-discovery-b-r3.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- No product builds or test runs. Other units may be using this machine, so run no `cargo`, no tests and no lead sets.
- Never touch the real home. `~/Library/Application Support/OpenSIP` must stay absent. If you run `git` anywhere, redirect `HOME` to a private 0700 scratch directory and turn hooks off.
- Never read the private 413 UUID fixture.
- If you compute digests or diffs, use read-only scratch scripts under your review directory.
- The product is read at main `218465f` (91 contract successors, inventory v135). That is `5214350` plus three binding-only commits (CR-1, SYN-1 and SYN-1F), which touch `design-lock.json` only. Every product file this law cites is byte-identical to main `30c5db1`, where r2 read it, except `schemas/registry.json`, whose cited lines (60-66 and 132-138) are unchanged. Read files or use `git show`; change nothing.

## Subject

The pins are in `hashes.txt`.
- `docs/implementation/m3/config-discovery-b/PROPOSAL.md` (r3) is the subject of `subjectSha256`. It is uncommitted in arch until acceptance.
- **Diff base:** `PROPOSAL-r2.md`, the r2 bytes you accepted (`92e65825…`, 94,762 bytes; `reviews/grok2-config-discovery-b-r2/`). The live file had carried them with a 2-line acceptance note, which r3 removes. Diff r3 against `PROPOSAL-r2.md`.
- r3's "r3 changes" table maps each change to its source, and every changed passage is marked "(r3)". Confirm that nothing else changed.
- **Companion drafts.** M3-E1 r4 (for Codex) and M3-I1 r3 (for CODEX2) are being drafted at the same time, so their live files are drafts. r3 and this request pin only accepted snapshots of other laws: `preview-pack-i1/PROPOSAL-r2.md`, never the live I1 file.

## What r3 records

r3 decides nothing new. "RBS1" is your review of B-S1 (`reviews/grok2-b-s1-r1/REVIEW.md`).
1. **Item 24 row 3, under your ruling RBS1 R2.** An explicit or config member when W fails W2 now takes row 1's `PROJECT.EXPLICIT_PATH_INVALID` / `CONFIG.INVALID` with `JOIN_CROSSES_NESTED_REPOSITORY`, as item 22 says. `workspace-root-inside-repository` is applied to no explicit or config member, and item 21's subject list points to item 24.
2. **Item 24 rows 5 and 6, under RBS1 R4 and R5** (B-S1 LD-7, LD-10 and LD-17).
   - n counts distinct repositories after placement, before X2 r9 item 6b's reads.
   - n > 64 refuses in both branches, and nothing is dropped to fit.
   - Row 5 cites B-S1's SL:1323 remedy.
   - Row 6 excludes the cap, and records the readers' disclosure when W fails W2.
3. **The bound design units.** B-S1 (with SX-1) is at `9c11c53`, B-S2 at `240a795` and B-S9 at `8adfe0c`. They are recorded in item 25, the units table's gates and rows, and "Not claimed".
4. **S9 is B-S9.** The units table gains a B-S9 row, and B-S1's row drops S9. **B1-a depends on B-S9.** B1-a embeds B-S9's string at `configuration.rs:24` (reused at `doctor_ingress.rs:216`) and repins `configuration_tests.rs:338-343`. Item 4's S9 paragraph points to B-S9.
5. **F9 and F10 are settled by B-S1.** F9 by its SL:286 and NE:4135 overrides; F10 by SX-1, with item 22's member `.opensip/` sentence pointing to it. B2-a implements SX-1's anchor and owes the `discovery-defaults.py` refresh (BS1-F3, LD-14). B2-a, B2-b and B3-b owe B-S1's listed controls.
6. **S1 and S2 are accepted:** X2 r9 and X12 r4.
7. **ML is cited by item** (M3-L r5's X10). ML:494-509 becomes ML item 17.
8. **Re-pins to accepted snapshots.**
   - M3P lines move by −2 to `M3-PLAN-r4.md`, because r2 cited the live r4 file with its note (arch `6f85fe717`).
   - I1 lines move by −2 to `preview-pack-i1/PROPOSAL-r2.md` (live bytes at arch `b412bce73`). The S2 passage quoted in item 10 is X12 r4's accepted text and keeps its own citations.
   - X2 and X12 lines are unchanged in `PROPOSAL-r8.md` and `PROPOSAL-r3.md`, because each acceptance sentence sat inside an existing line (arch `bf3007f0f` and `0f69f15fc`).
   - X4's live r7 file has no snapshot and is pinned by sha256.
   - The r2 history table keeps its reviewed citations.

**Unchanged:** every decision, the units' sizes and order, findings F1 to F8 and F11 to F14, the forbidden substitutes, and items 1 to 20 apart from the marked notes in items 4, 9, 10 and 18.

## Decide

1. **Row 3.** Does it now agree with item 22 and row 1 exactly as your RBS1 R2 ruling states? Is item 21's new pointer consistent with X2 r9's subject list and its deferral to item 24 (`project-root-x2/PROPOSAL-r9.md:87`, :325, :374)?
2. **Rows 5 and 6.** Do they state the cap and the W2-failure disclosure exactly as your R4 and R5 rulings and B-S1's LD-7, LD-10 and LD-17 do, with nothing widened?
3. **Bound units.** Are the B-S9 split, B1-a's dependency and product lines, B2-a's obligations, and the F9 and F10 settlements faithful to the READMEs and reviews of B-S1, B-S2 and B-S9?
4. **Re-pins.** Does every re-pinned citation resolve, in its named snapshot, to the text r2 cited? Please spot-check the M3P −2 and I1 −2 shifts, the unchanged X2 and X12 lines, and ML item 17 (in r1 and r5).
5. **Scope.** Does r3 change anything not in its table, or record as settled anything that is not?

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: ACCEPT or REQUIRED-FINDINGS;
- `"requiredFindings"`: each with id, location, problem or claim, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectSha256"`: PROPOSAL.md's sha256.

This is a law review, not a `verify_design` unit. Do not commit.
