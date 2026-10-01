Grok re-review law 461 r2 after your r1 findings. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-acl-unreadable461-r2. Law review; no product cargo.

Subject: docs/implementation/m2/acl-omission-unreadable-461/PROPOSAL.md r2 (pin in hashes.txt). `diff` it against PROPOSAL-r1.md.

## Changes

- **RF-1.** Item 2: the `AclUnreadable` arm stays after the kind, owner, mode and group arms. Earlier refusals win, and the 18851-case fixture keeps its codes.
- **RF-2.** Item 3: the subject is `acl-unreadable`, hyphenated, as one new arm in 468c's custody-subject mapping. It is not derived from `Refusal::code`.
- **RF-3.** Item 6: the `AclWrite::Known` source pin covers only platform observations, through `DescriptorAcl::Present` in `check_descriptor_observation`. It names one allowed exception: the `check_external_ancestor` `Known(Vec::new())` order placeholder, which stays unchanged, while the ancestor ACL is judged by `external_ancestor_acl`.

## Decide

Are RF-1 to RF-3 closed? Is anything new wrong? review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.
