Grok re-review: 461a r2 after your r1 finding. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-acl-unreadable461a-r2.

Subject: the same worktree `/Users/sb/code/opensip-ai/opensip-461a`. The updated subject.diff is in your output directory, and the pins are in hashes.txt.

## Change (RF-1)

The only change is the doc comments of `DescriptorAcl` in `crates/platform/src/filesystem.rs`:
- `Omitted` now states that on macOS 27 an ACL whose last entry was removed is observed as `Omitted` (law 461 item 6).
- `Present` now says only "a present ACL whose entries grant no write", for the empty-writer case.

No code changes. fmt, clippy and the platform tests are clean.

## Decide

Is RF-1 closed? Is anything new wrong? review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256" (the sha256 of subject.diff). Write REVIEW.md and review.json. Do not commit.
