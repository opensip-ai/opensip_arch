Grok re-review law 468 r5 after your r4 finding. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-existing-root468-r5. Law review; no product cargo.

Subject: docs/implementation/m2/existing-root-admission-468/PROPOSAL.md r5 (pin in hashes.txt). `diff` it against PROPOSAL-r4.md.

## Change (RF-1)

Item 4 now says:
- The observation path reaches the same fence only through item 3's steps 0 and 1: the charged, retained walk, then the no-follow fence attempt. It never uses `NativeInstallationFence::try_acquire`. It has its own ledger, no barrier, and a recheck under the held fence.
- A read command has no `InitialPlatform`, so its step 0 premise can only be the 458c receipt. Until 458c is accepted, 468 builds no observation path.
- 468c ships the write path and the public routing. The observation path, the doctor note and the 256-slot rule move with 458c/461.
- It records an open scope question for 458c: item 9 says root to H, but step 0 also reaches `Library` and `Application Support`.

## Decide

- Is RF-1 closed?
- Is it acceptable to defer the observation path and doctor note to 458c/461 (the item 5 note rules remain law)?
- Is anything new wrong?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.
