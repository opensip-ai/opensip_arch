CODEX2 review: M3-I1 **r3**, the X12c preview policy pack, as a **record revision** after your r2 acceptance. This is a **law and contract-soundness** review. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex2-preview-pack-i1-r3.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- No product builds, cargo or test runs: other units may be using this machine.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the 413 fixture.
- If you compute digests or diffs, use read-only scratch scripts under your review directory.
- The product is read at main `218465f` (91 contract successors, inventory v135; I1-L bound at `0ceb9ad`, I1-P at `cd5958b`). Every product file this law cites is byte-identical to `2967905`, where r2 read it. Read files or use `git show`; change nothing.

## Subject

The pins are in `hashes.txt`.
- `docs/implementation/m3/preview-pack-i1/PROPOSAL.md` (r3) is the subject of `subjectSha256`. It is uncommitted in arch until acceptance.
- `UNITS.md` keeps its r2 bytes (`0c3c0f44…`, equal to `UNITS-r2.md`). r3 records its additions in the law's "Units after the law".
- **Diff base:** `PROPOSAL-r2.md`, the r2 bytes you accepted (`1eb47d1e…`, 52,522 bytes; `reviews/codex2-preview-pack-i1-r2/`). The live file had carried them with a 2-line acceptance note, which r3 removes. Diff r3 against `PROPOSAL-r2.md`.
- **The verbatim block.** r2's lines 88 to 221 (items 2.1 to 2.9) are the block I1-L's §4a carries verbatim (`0983e395…`). r3 leaves them byte-identical and adds the precisions P0 to P7 after them. Please confirm.
- **Companion drafts.** M3-B r3 (GROK2) and M3-E1 r4 (Codex) are being drafted at the same time, so their live files are drafts. This request pins only accepted snapshots of other laws.

## What r3 records

r3 decides nothing new. Its "r3 changes" table maps each change to its source, and every changed passage is marked "(r3)". The deviations are numbered as in I1-L's README.
1. **I1-L and I1-P are accepted and bound** at product `0ceb9ad` and `cd5958b`.
2. **Item 4, as I1-L bound it:**
   - the form: 11 text overrides, four complete JSON copies and §4a (deviation 1, LD-L1);
   - how a copy treats its parent's bound overrides: it is the parent's effective text (deviation 6, LD-L2);
   - the anchor imprecisions: WS:598's code span, and the one-line WS:603 and IE:214 (deviation 2);
   - the IDS enum placement: appended last (deviation 3, LD-L3);
   - WS's selected effective copy, WSE at 602 and 607 (deviation 5, LD-L5);
   - the five consequential passages item 4 omitted: IE:1266, IE:1334, IE:1544, COMP:109 and the PDS and PPDS `description`. The "Unchanged" list's "IE changes only by the one passage above" is corrected (deviation 4, LD-L4).
3. **P0 to P7,** the choices items 2.3 and 2.5 left open, quoted after item 2.9 from I1-L's §4a (deviation 7, LD-L6).
4. **What I1-a needs for `verify_design`:**
   - the 468a-form record carrying its new admission registry;
   - re-pointed generation and admission source maps;
   - the atom registry's two pins moved;
   - UNITS r2's line references moved (`:1221-1232`, `:2782-2793`, `:4986`, `:296-304`).
5. **I1-P's findings for item 5:**
   - the three digests recompute exactly and are pinned;
   - I1-P fixes the whole `pack-registry.json`, standing text included;
   - S3 passes only after I1-a;
   - S10's oracle is I1-L's `corpus-*` cases.

   I1-b2's fixtures also carry your I1-L-NB-01 cases, as M3-PLAN r9 routes them.
6. **Re-pins.** M3P lines move by −2 to `M3-PLAN-r4.md` (r2 cited the live r4 file with its note, arch `6f85fe717`). X12 lines are unchanged in `PROPOSAL-r3.md`. The X12 short name records that X12 r4 is accepted, and that its item 8 withdraws "the order" from item 7 and supersedes item 8's J "Order" bullet. This file is not edited for that, as X12 r4 states.

**Not taken up:** your r2 observations I1-R2-NB-1 (the "no schema digest enters any identity" wording) and I1-R2-NB-2 (the budget paragraph). No source routes them to this revision, and both sit in item 3 or inside the verbatim block (2.8). They stay open for the next substantive revision.

**Unchanged:** the pack bytes, the three digests, every decision, and the units' number, order and sizes.

## Decide

1. **I1-L.** Does r3 record each I1-L deviation and lead decision faithfully, with nothing widened? In particular: the anchors, the append-last placement, the five consequential passages, WSE, and the effective-copy rule for bound overrides.
2. **P0 to P7.** Are they quoted exactly from I1-L's §4a (`i1-l/atom-section-4a.md:141-148`)? Is the verbatim block untouched?
3. **I1-a.** Are the four `verify_design` needs and the moved lines exactly I1-L's "For I1-a"?
4. **I1-P.** Are its findings recorded faithfully? Is the I1-b2 fixture note a fair record of I1-L-NB-01's routing?
5. **Re-pins and X12 r4.** Does every re-pinned M3P line resolve, in `M3-PLAN-r4.md`, to the text r2 cited? Is the X12 r4 note accurate?
6. **Scope.** Does r3 change anything not in its table?

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: ACCEPT or REQUIRED-FINDINGS;
- `"requiredFindings"`: each with id, location, problem or claim, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectSha256"`: PROPOSAL.md's sha256.

This is a law review, not a `verify_design` unit. Do not commit.
