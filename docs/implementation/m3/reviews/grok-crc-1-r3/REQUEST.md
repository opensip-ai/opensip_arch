Review: **CRC-1 r3**, M3-C's core role closure successor. Verdict wanted: **ACCEPT-DESIGN-UNIT** (with `subjectManifestSha256`) or **REQUIRED-FINDINGS**. Claude Opus 5.5 leads.

Write only under `/tmp/opensip-implementation/reviews/grok-crc-1-r3`.

**Rules** (as in r2):
- Read-only. No repository edits, commits or delegation.
- Don't run cargo.
- Run light read-only Python (the unit's `build_crc_1.py --check`, `check_crc_1.py` and `verify_scratch.py`) under a private 0700 `TMPDIR`.
- Never touch `~/Library/Application Support/OpenSIP`. Never read the 413 fixture.

## What r3 changes

r3 answers Grok's r2 RF-1 (`reviews/grok-crc-1-r2/`). The lead had renamed the review directory from `grok2-crc-1-r2` to `grok-crc-1-r2`, but the builder still emitted `grok2-crc-1-r2`, so `--check` failed on the unit draft.

r3 changes only these things:
- `crc-1/evidence/build_crc_1.py`: the review path, now `reviews/grok-crc-1-r3/review.json`, and the draft assessment text;
- `crc-1/README.md`: the NBO-2 row, cross-law item 1's SYN-1F digest (now `73645b76…`, rebuilt on r2's strings), and a new "r3 changes" section;
- `crc-1/successor.json`, but only the two candidate pins of the files above. **`passageOverrides` are byte-identical to r2's**, so every meaning-bearing string is unchanged.

r2's versions of the changed members are in `r2-members/` for diffing. GROK2's r1 RF-1 (the "not even explicitly" wording) stays fixed as in r2.

## Checks the lead ran

- `build_crc_1.py --rev cd5958b --check` gives `identical` for every generated file, the unit draft included.
- `check_crc_1.py` passes.
- `verify_scratch.py --rev cd5958b` passes, with contract successors going 82 → 83. A second override of a CRC-1 selector still refuses.

## Decide

1. Is r2's RF-1 resolved?
2. Is any difference from r2 other than the three listed changes?
3. Is anything else blocking acceptance?

## Output

Write `review.json` (`verdict`, `subjectManifestSha256`, `requiredFindings`, `nonBlockingObservations`) and `REVIEW.md`. Don't commit.
