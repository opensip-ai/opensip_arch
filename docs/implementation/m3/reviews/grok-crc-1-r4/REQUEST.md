Grok review: **CRC-1 r4**, M3-C's core role closure successor. Verdict wanted: **ACCEPT-DESIGN-UNIT** (with `subjectManifestSha256`) or **REQUIRED-FINDINGS**. Claude Opus 5.5 leads.

Write only under `/tmp/opensip-implementation/reviews/grok-crc-1-r4`.

**Rules:**
- Read-only, with no repository edits, commits or delegation, and no cargo.
- Light read-only Python under a private 0700 `TMPDIR` is fine, for the unit's `build_crc_1.py --check`, `check_crc_1.py` and `verify_scratch.py --rev cd5958b`.
- Never touch `~/Library/Application Support/OpenSIP`, and never read the 413 fixture.

## What r4 changes

r4 answers your r3 RF-1 (`reviews/grok-crc-1-r3/`). It is a README consistency pass, plus the builder's round path:
- `crc-1/README.md`:
  - the status line (Draft r4; an independent ACCEPT-DESIGN-UNIT);
  - the r1-members location (`reviews/grok-crc-1-r2/r1-members/`, after the lead's directory rename);
  - binding step 1, which now names the accepting round's directory generically;
  - the SYN-1F note (resolved: SYN-1F's copy carries r2's corrected sentence);
  - your NBO-2 (r3's "every candidate byte-identical" is corrected);
  - a new "r4 changes" section.
- `crc-1/evidence/build_crc_1.py`: the emitted review path is now `grok-crc-1-r4`, and the draft assessment text.
- `crc-1/successor.json`: only those two candidate pins. **The nine passage overrides are byte-identical to r2's and r3's.**

r3's versions of the changed members are in `r3-members/`.

## Lead checks

- `--check`: identical.
- `check_crc_1.py`: passes.
- `verify_scratch.py --rev cd5958b`: 82 → 83.

## Decide

1. Is your r3 RF-1 resolved?
2. Is any README line still stale against r4?
3. Is anything else blocking acceptance?

## Output

Write `review.json` and `REVIEW.md`. Don't commit.
