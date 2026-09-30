Grok re-review law 458c r4 after your r3 findings. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-read-premise458c-r4. Law review; no product cargo.

Subject: docs/implementation/m2/read-premise-458c/PROPOSAL.md r4 (pin in hashes.txt). `diff` it against PROPOSAL-r3.md.

## Changes

Both answers adopt the write gate's existing classification (468b, mapped by 468c) rather than inventing rows.

- **RF-1.** H failures take the gate's rows:
  - a missing H goes to custody;
  - a permission-refused open or other I/O goes to `HOST.IO_FAILURE`;
  - an unsupported filesystem goes to `NT-TCB-BOOT` / `INSTALL_ROOT_FS`.
- **RF-2.** Every lock `Err`, including a carrier that is no longer a regular file, goes to `HOST.IO_FAILURE`, `host-io`, exit 4, as `lock_fence` does. A replaced carrier is caught by the step 2 recheck on custody.

## Decide

Are RF-1 and RF-2 closed, and do these rows match 468b and 468c in the product at 7237f93? Is anything new wrong? review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.
