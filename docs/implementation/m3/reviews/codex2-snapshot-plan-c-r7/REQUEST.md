CODEX2 review: M3-C r7, the sealed snapshot and Plan law. This is a **law and contract-soundness** review, round 7. It is a narrow amendment. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex2-snapshot-plan-c-r7.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- No product builds or test runs: a timing-sensitive crash-matrix run may be using this machine.
- Never touch the real home.
- Never read the 413 fixture.
- Use read-only scratch scripts under your review directory if you need them.

## Subject

The pins are in `hashes.txt`.
- **The subject:** `docs/implementation/m3/snapshot-plan-c/PROPOSAL.md`, the r7 law. It is the subject of `subjectSha256`.
- **For diffing:** `docs/implementation/m3/snapshot-plan-c/PROPOSAL-r6.md` (`8274bca1…`), the r6 bytes you accepted in review, without the acceptance note.
- **The source of the amendment:** M3-D r3, the supervisor law, accepted by GROK2 (`docs/implementation/m3/supervisor-d/PROPOSAL-r3.md`, `9679dbc4…`). Read:
  - item 24 (lines 708-746), especially "What it admits" and "MC's closure admission" (lines 718-719);
  - its forbidden substitutes (line 742);
  - successor SD-6 (line 1092) and cross-law finding F11 (line 1111).

  M3-D cites this law as "MC r5". Row 8 is byte-identical in r5 and r6.
- **The companion:** J1 r4 (`docs/implementation/m3/host-pipeline-j/PROPOSAL.md`), reviewed separately by GROK2 under `grok2-host-pipeline-j-r4`. It adds row R10a, its ephemeral counterpart ER10a (item 6) and successor S19, which records this narrowing. J1 r3's accepted bytes are pinned for the order R10 to R12.
- **The product:** `/Users/sb/code/opensip-ai/opensip` at main `e093e90` (F8b), read-only. r7 cites no product path.

**Scope.** r7 applies **exactly** SD-6's narrowing of item 16's row 8, and changes nothing else. Diff r6 against r7. Every change should belong to SD-6, or to the header and the "r7 changes" table. The one exception is owner question R1's wording. It was already in the live r6 file beside the acceptance note, as your C6-NB-01 asked, and r7 lists it in its table.

## What r7 changes

**Row 8 (item 16)** becomes a **selection** among the component manifests already admitted at J1 r4's row R10a, or at ER10a on the ephemeral path.
- It adds no admission of its own. Item 7's admission path has therefore already run for those manifests, no later than R10a, before any analysis-attempt ExecutionId is drawn.
- Item 7's retention covers the closures row 8 selects. That is the same population r6's row 8 admitted, not every manifest R10a admitted.
- The core evaluator and detector closures (item 9) are core-inventory projections, not component manifests. R10a does not admit them, and row 8 keeps them unchanged.
- If J1 r4's review changes R10a, row 8 follows the accepted text.
- The gate is unchanged: the law takes effect once M3-L is accepted, and X12 r4 is already accepted.

## Decide

1. **Faithfulness.** Does the narrowed row 8 match M3-D r3 item 24 and SD-6?
2. **The core role closures.** M3-D's sentences say row 8 "selects only among manifests D4 has already admitted". Its forbidden substitute forbids "a closure admitted at MC row 8 that R10a did not admit". Read literally, both would exclude item 9's core closures, which are not manifests. Is r7 right to keep them outside the narrowing?
3. **Retention.** Is the retention sentence a lawful part of the narrowing, rather than a change to item 7? Without it, would r7 widen item 7's "every admitted closure" to every manifest R10a admits?
4. **Order.** Does row 8 still consume only what earlier steps admitted, now that its input is R10a's admitted set (J1 r4) as well as step 7?
5. **Scope.** Does r7 change anything else in r6?

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: ACCEPT or REQUIRED-FINDINGS;
- `"requiredFindings"`: each with id, location, problem or claim, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectSha256"`: PROPOSAL.md's sha256.

This is a law review, not a `verify_design` unit. CRC-1 still needs its own `ACCEPT-DESIGN-UNIT`. The law still takes effect only once M3-L is accepted. Do not commit.
