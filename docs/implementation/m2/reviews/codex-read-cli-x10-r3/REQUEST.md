Codex re-review: law X10 r3 after your r2 findings. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/codex-read-cli-x10-r3. Law review; no product cargo.

Subject: docs/implementation/m2/read-cli-x10/PROPOSAL.md r3 (pin in hashes.txt). `diff` it against PROPOSAL-r2.md.

## Changes

- **RF-2.** Detailed-failure rendering shares the doctor termination renderer:
  - Termination;
  - Error and Fault cause when present, with none invented on request-rejected;
  - each `errors` Detail, Subject and Remedy;
  - Request.
- **RF-3.**
  - Security coverage is now only real `Complete`, `Incomplete` (one finding per kind) and the refusal rows.
  - Host tests split into native-shaped inputs (`Complete` with `other = []`, and `Incomplete`) and explicitly synthetic report-bound inputs through `doctor_installation` (one other plus the note, 255 plus the note versus 256, and partial 256 versus 257). The synthetic inputs are labelled synthetic, and production always passes `other = []`.
  - X10a no longer lists `run_with`. It lists the single-producer ingress and the layered tests. No `run_with` mention remains except as rejected history.

## Decide

Are RF-2 and RF-3 closed? Is anything new wrong? review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.
