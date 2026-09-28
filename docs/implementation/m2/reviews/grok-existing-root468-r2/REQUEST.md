Grok re-review law 468 r2 after your r1 findings. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-existing-root468-r2. Law review; no product cargo.

Subject: docs/implementation/m2/existing-root-admission-468/PROPOSAL.md r2 (pin in hashes.txt). `diff` it against PROPOSAL-r1.md.

## Changes

- **RF-1.** Item 3 now:
  - stops a busy fence at `PROJECT.BUSY`, with no recheck, barrier or effect;
  - defines one recheck set under the held fence: account, I-parent name, I and fence identity, custody of I and the I-parent (owner, mode, ACL), and the required file owners (fence, registry, pair, marker, node chain, trust current: owner, private mode, one link, private ACL);
  - runs that set before the barriers and again after them, including after a failed barrier.
- **RF-2.** Item 6 is now a total routing table with class, exit, D9 error code and detail for every refusal family of 459–468:
  - the two new request-rejected details use `REQUEST.PRECONDITION_FAILED`;
  - other core refusals use `EXTENSION.ADMISSION_REJECTED` with `NT-TCB-IDENTITY`;
  - platform refusals use their decision's `NT-TCB-*` detail, or `NT-TCB-PROFILE-UNQUALIFIED` / `NT-TCB-BOOT:INSTALL_ROOT_FS`;
  - custody refusals, and a stage validation or name failure before the rename, use `CONFIG.CUSTODY_REFUSED`;
  - NotPerformed, indeterminate, post-rename, barrier and I/O failures use `HOST.IO_FAILURE`;
  - budget uses the new `WORK.BUDGET_EXHAUSTED`.

  Totality is enforced by an exhaustive match. Where the existing registry fixes a class for a detail, the registry prevails.

## Decide

Are RF-1 and RF-2 closed? Check each existing detail's class and code against public-detail-registry.json and diagnostic-routes.json, and name any row that disagrees. Is anything new wrong?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.
