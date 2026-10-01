Grok re-review: law X4T r5 after Grok's r4 finding. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-trust-admission-x4t-r5. Law review; no product cargo. Product HEAD is 8bfc78a.

Subject: docs/implementation/m2/trust-admission-x4t/PROPOSAL.md r5 (pin in hashes.txt). `diff` it against PROPOSAL-r4.md, which equals the reviewed r4 (sha f6a9a27b…).

## Changes (RF-1)

- Item 1 names what each binder really opens, checked against 8bfc78a.
- The root admission, the catalog and revocation heads (body, envelope, admission), `history` and `timeEvidence` are opened by X4T-a itself, through the same `retained_metadata_index::Budget::load` that `bind_retained_head` uses.
- `verify_revocation` verifies the bytes that load supplied.
- The `accepted.by` join is X4T-a's own check: an accepted role must name a loaded current-descriptor event, or the installation is incomplete.
- Items 2, 12 and 13 and the X4 note follow.

## Decide

Is RF-1 closed? Is every function named correct at 8bfc78a? Is anything new wrong? review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.
