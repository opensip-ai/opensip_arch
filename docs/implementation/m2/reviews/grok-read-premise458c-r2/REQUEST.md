Grok re-review law 458c r2 after your r1 findings. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-read-premise458c-r2. Law review; no product cargo.

Subject: docs/implementation/m2/read-premise-458c/PROPOSAL.md r2 (pin in hashes.txt). `diff` it against PROPOSAL-r1.md.

## Changes

- **RF-1.** Steps 2 and 4 run 468 item 3's full recheck set, including the required-file-owner limb (owner, private mode, one link, private ACL):
  - step 2 covers the fence and every required file already retained;
  - step 4 covers every required file captured in step 3, by its retained identity.

  A missing, undecodable or wrongly linked member is a structural finding, not a recheck failure.
- **RF-2.** Item 12 now leaves a reachable incomplete I's doctor report to owner §5 and `doctor-cases.json`, unchanged:
  - one actual defect entry per structural finding, under the existing classifications, with no collapse and no new code;
  - no note;
  - the 256-entry bound, so 257 is `HOST.IO_FAILURE` / `DOCTOR.REPORT_NOT_PRODUCIBLE`, exit 4.

  Doctor does not latch on a structural finding, but a step 4 recheck failure still ends it with no report. Other read commands still end on the incomplete row. (The owner's decision was that doctor fails like any read when it cannot reach I. The one-entry detail was my wording, and I corrected it to follow owner.md.)
- **RF-3.** Item 11 now:
  - paces attempts at `FENCE_POLL` (25 ms), stopping at 5 s or 201 attempts;
  - does not re-walk;
  - reserves all 201 attempts at the lock cost before the first attempt, so the wait ends only in the lock or the busy row, or refuses on budget before any attempt.
- **RF-4.** Step 0 classifies the end of the walk for the observation path:
  - `ObservedAbsent { component }` only when the first missing fixed-suffix component (`Library`, `Application Support`, `OpenSIP`, `preview-v1`) is positively observed absent by a no-follow lookup under its retained, admitted parent. That routes to `INSTALLATION.NOT_INITIALIZED`.
  - A non-directory, symlink, custody refusal, I/O or budget failure is never absence.
  - A missing H is an account refusal.
  - The write gate keeps its own classification.

## Decide

Are RF-1 to RF-4 closed? Is RF-4's rule (positive absence of the first missing suffix component under its retained parent) consistent with owner §5's ban on inferring pristine absence? Is anything new wrong?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.
