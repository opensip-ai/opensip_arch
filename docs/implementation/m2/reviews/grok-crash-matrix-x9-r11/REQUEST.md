Grok review: law X9 r11, which answers your X9 r10 RF-1. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT**.

**Rules:**
- No repository edits, commits, pushes or delegation.
- Write only under /tmp/opensip-implementation/reviews/grok-crash-matrix-x9-r11.
- This is a law review with no product cargo. Run git read-only, against product main `b999ae3`.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.

## What changed

Pins are in hashes.txt. `crash-matrix-x9/PROPOSAL-r10.md` holds the r10 bytes you reviewed: 109725 bytes, `27dd6f48…`. Diff PROPOSAL.md against it.

The lead took your first option. r10 was not accepted, so r11 corrects it in place. These are the only changes:
- **Title:** r10 becomes r11.
- **r10 header:** an r11 note names RF-1 and the fix.
- **The census point:**
  - **Its title** now names the `store_gc` run.
  - **"What X9-5 found"** gains the F53 sentence: no `finalize` run calls `maintenance::run` or `settlement_sweep`, and `x6.sweep` is durable.
  - **The decision is three unarmed runs.** The new one is (c), a `store_gc` run in a fresh process after an unarmed (a) on the same root.
    - The sweep settles (a)'s attempt `committed`, as it settles any lawful commit's attempt (r8's R3 value), so the run reaches `x6.sweep.settle.commit`.
    - A (c) trace without that point is a `HARNESS-ERROR`.
    - Only the `store_gc` child's trace counts as (c).
  - **Each of (a), (b) and (c)** runs twice and must be equal.
  - **The union** takes the largest occurrence count.
  - **The trace digest** is over (a), then (b), then (c).
  - **Rejected:** your alternative, moving F53's process-death kills to X9-3's file. Item 12 gives F53's `store-gc` step to X9-5.
- **The item 5 and item 12 r10 notes** name the `store_gc` run.

Nothing else changes. F53's store-gc rows stay in X9-5.

Your non-finding about the runner owing the one-entry refusal when a first call returned at replay, before `operation`, is already covered by r10's "at most one call to any of the three entries and the two runners together". X9-5 implements it by setting the flag in the runner itself.

## Decide

- Does r11 resolve RF-1 exactly?
- Does it change nothing else?
- Is anything else wrong?

Write REVIEW.md and review.json under the output directory. review.json needs:
- "verdict";
- "requiredFindings";
- "noAcceptedOutcomeChanged";
- "subjectSha256";
- "subject" (path, bytes, sha256);
- "preservedSnapshot": the accepted r9, `PROPOSAL-r9.md`, 95579 bytes, `e6ff60c1…`.

Do not commit.
