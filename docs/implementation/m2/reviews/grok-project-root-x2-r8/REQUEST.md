Grok re-review: law X2 r8 (project-root custody), after your r7 RF-1. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-project-root-x2-r8.

Subject: `/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/project-root-x2/PROPOSAL.md`, r8, sha256 c31d9a020f91650fb1c85f6697bffac1902bf3607d501e5821f48cd8c4b301b5. r7 is preserved as PROPOSAL-r7.md. Your r7 review is `/tmp/opensip-implementation/reviews/grok-project-root-x2-r7/`. Diff r7 to r8 and check that only item 1 and the header changed.

Change (item 1 only):
- The sub-bullets about no-follow descriptor admission, the premise, the H-volume constraints and `.git` strictly below H now hang under a new bullet, "How the Git evidence in scope is admitted". That bullet covers the `.git` evidence and the global files only.
- A separate bullet says the fixed system Git configuration files are not in scope. They are refusal-only evidence, opened by fixed path following links, with no custody, premise or H-volume constraint. Item 6a refuses one only when it is unreadable, not a regular file, oversized, or fails the closed parse. Their location is never a refusal.
- In "never covers", the location refusal now names a `.git` at or above H or off H's volume, and the system files are listed separately as refusal-only evidence.

Decide: is RF-1 closed, and does anything new conflict with item 6a, with other X2 items, or with accepted laws?

review.json: "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings", "subjectSha256". Write REVIEW.md and review.json. Do not commit.
