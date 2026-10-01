Grok review: law X2 r7, an amendment found while implementing X2b-2. Write only under /tmp/opensip-implementation/reviews/grok-project-root-x2-r7. Law review; no product cargo.

Subject: docs/implementation/m2/project-root-x2/PROPOSAL.md r7 (pin in hashes.txt). Diff it against PROPOSAL-r6.md, which equals the accepted r6.

## Why

X2b-2 implemented item 1's custody rule for system Git config sources literally, and it refuses every repository on a stock Mac:
- `/` is on the sealed system volume, off H's volume, with no ACL;
- `/etc` is a symbolic link;
- `/opt/homebrew/etc` is user-owned and admin group-writable.

## Change (lead decision)

System sources become refusal-only evidence:
- each is opened by its fixed path, following links, charged and capped at 64 KiB;
- each is absent or parsed with the same closed parse;
- no custody is judged; their only effect is to refuse;
- an unreadable, non-regular or oversized source is `vcs-unsupported`;
- they are rechecked by re-reading (same absence, or same bytes).

Global and repository sources keep custody. Item 1's scope no longer lists system sources.

Rejected: root-ownership custody, and skipping system sources.

## Decide

- Is the amendment sound? Can a system source that is read without custody ever admit, select or relax anything?
- Is following links for system paths acceptable?
- Is anything new wrong?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.
