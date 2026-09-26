Grok review law 463 r6, a one-entry amendment. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-initial-core463-r6. Law review; no product cargo. Do not read or print the private 413 UUID fixture.

Subject: docs/implementation/m2/initial-core-launch-463/PROPOSAL.md r6 (pin in hashes.txt). `diff` it against PROPOSAL-r5.md. While planning 463c, the lead found that r5 item 5 step 2 verifies the manifest's embedded revocation, but item 2's exhaustive store list does not contain that document. In core_anchor.rs the revocation is a manifest member (`members.revocation`), with its envelope in `members.envelopes`. It is selected through the same EmbeddedCapture index as root-chain members. r6 adds exactly that member and its envelope to the store list, read by the same no-follow opens.

Decide: is this the right and minimal fix? Should anything else the revocation order needs also be in the store? Is anything new wrong?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.
