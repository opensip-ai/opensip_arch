Grok review: law 461 r3, a correction after r2 acceptance found while implementing 461a. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-acl-unreadable461-r3. Law review; no product cargo.

Subject: docs/implementation/m2/acl-omission-unreadable-461/PROPOSAL.md r3 (pin in hashes.txt). `diff` it against PROPOSAL-r2.md.

## Changes

- **Item 6.** On macOS 27, removing a file's last ACL entry makes the `filesec` observer report `Omitted`, while the bounded capture sees `Entries(0)`. The pin records that fact and fails closed (unreadable). `Present(vec![])` is now pinned by a file whose entries grant no mutation right.
- **Item 3.** No choke-point `Refusal` reaches 468c at d4239a5: installation reads route through the gate and session refusals, and the policy-capture path has no 468c row. So 461a adds no subject arm. The first unit that routes one publicly adds exactly `acl-unreadable`.

## Decide

Are both corrections sound and fail-closed? Is the claim that no choke-point `Refusal` reaches 468c true at d4239a5? Is anything new wrong?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.
