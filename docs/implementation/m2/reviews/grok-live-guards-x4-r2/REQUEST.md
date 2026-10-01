Grok re-review: law X4 r2 after Codex's r1 findings. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-live-guards-x4-r2. Law review; no product cargo. Product HEAD is f7acb6d.

Subject: docs/implementation/m2/live-guards-x4/PROPOSAL.md r2 (pin in hashes.txt). `diff` it against PROPOSAL-r1.md. The r1 findings are in `docs/implementation/m2/reviews/codex-live-guards-x4-r1/`.

## Changes

- **RF-1 (trust reader).** A new prerequisite unit, X4T, with its own law, provides native current-trust admission. Until it exists, no guard or effect permit can exist (lead decision).
- **RF-2 (first read).** The monitor and gate are created inside X2e under the fence, and X4T's admission is the monitor's first timed read. There is one monitor history.
- **RF-3 (mutable trust).** The observer works through retained trust-directory handles: open `state.v1` by name, read the named records, admit through X4T, reopen to check. It gets one retry on a mixed read. Unrelated revocation and grant-preserving policy changes count as drift, and the start state is never replaced.
- **RF-4 (operation owner).** `OperationGuard` lives inside X2 r3's `ProjectOperation`, with a closed mandatory guard set; the registry and pair are provenance only. There are no new ledgers. The abstract lock exists only in test builds.
- **RF-5 (timing).** The checkpoint order is:
  1. blocking guard rechecks;
  2. the final timed observation and revocation;
  3. the latch;
  4. one clock sample, then admission with no blocking in between.

  X3b and X3d repeat the checkpoint after blocking journal work (F19). The remaining gap before admission is stated as an obligation to measure.
- **Alignment.** The checkpoint runs under X3b r1's `JournalAppendLock`.

## Decide

- Are RF-1 to RF-5 closed?
- Is splitting out X4T sound?
- Is the one-retry rule for a mixed read sound?
- Is the drift classification closed?
- Is anything new wrong?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.
