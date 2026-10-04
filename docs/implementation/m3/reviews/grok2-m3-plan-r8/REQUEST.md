GROK2 review: **M3-PLAN r8**, a narrow round that answers your two r7 findings. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**, on factual accuracy. Claude Opus 5.5 leads.

Write only under `/tmp/opensip-implementation/reviews/grok2-m3-plan-r8`.

**Rules** (as in r7): read-only; no repository edits, commits or delegation; no cargo; never touch `~/Library/Application Support/OpenSIP`; never read the 413 fixture.

## Subject

The pins are in `hashes.txt`.
- **The subject:** `docs/implementation/m3/M3-PLAN.md`, r8.
- **The base:** `M3-PLAN-r7.md`, your r7 subject (`4ff335ec…`). Diff the two. Every change should be one of the three rows in the "r8 changes" table.
- **Your r7 review:** copied to `reviews/grok2-m3-plan-r7/`.

**Recorded since your r7 review** (the plan need not say so):
- M3-H r3 was accepted by Grok. Its live file now carries an acceptance note. r8 still cites MH by its r3 bytes, which are pinned here as `fact-admission-h/PROPOSAL-r3.md`.
- CRC-1 is at r3 with Grok.

## Decide

1. Are RF-1 and RF-2 resolved?
   - RF-1: X-H3's widening is named M3-C r8 with CRC-2 everywhere.
   - RF-2: X4-F1's confirmation lane is recorded as passed.
2. Is the treatment of NBO-1 acceptable? It is recorded, and the rename is routed to M3-L's next revision.
3. Did r8 introduce any new error?

## Output

Write `review.json` and `REVIEW.md`. `review.json` needs `verdict`, `subjectSha256`, `requiredFindings` and `nonBlockingObservations`. Don't commit.
