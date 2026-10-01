Grok review: law 461 r1. An omitted ACL becomes unreadable at the single custody choke point. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-acl-unreadable461-r1. Law review; no product cargo. Product HEAD is d4239a5, with 458c complete; you may read it.

Subject: docs/implementation/m2/acl-omission-unreadable-461/PROPOSAL.md r1 (pin in hashes.txt). Context: CREATOR-PLAN row 461, law 458 §5, 458c r6 items 3, 8 and 9, and 468 r5 item 6.

## Decide

- **Item 1.** Is replacing `possible_acl_writers` with a typed `DescriptorAcl { Omitted, Present(..) }` complete? Does no path remain that turns omission into "no writers"?
- **Items 2 and 3.** Is the choke-point mapping right: `Omitted` gives `AclWrite::Unreadable`, which gives `Refusal::AclUnreadable` in every scope? Is the public row right: the custody row, subject `acl-unreadable`?
- **Item 4.** Is the consumer table complete and correct at d4239a5? Check for any production consumer of the observation that it misses, and for any production path whose outcome changes other than as stated.
- **Item 5 and item 9 (lead decision).** Project roots stay outside the premise and refuse on omission, with a separate project-root custody law required before any project admission. Is that consistent with 458 §5 and 458c item 3, and safe given that nothing admits projects today?
- **Items 6 to 8.** Are the pins, the budget and the unit split right?
- Is anything else wrong?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.
