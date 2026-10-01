Codex review: law X2 r1, project-root custody, project admission, first registration and namespace leases. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/codex-project-root-x2-r1. Law review; no product cargo. Product HEAD is fdbedf4 or later; you may read it.

Subject: docs/implementation/m2/project-root-x2/PROPOSAL.md r1 (pin in hashes.txt). Context:
- EXIT-PLAN.md rows X2 and X3a, and X3a r1 (its namespace dependency);
- laws 458 (§3 and §5), 458c r6 item 3, 461 r3 item 9, 465 item 4, 468 r5 items 2 and 6, and X1 r1;
- owner.md §8;
- the S3 launch walk, S7 leases, S12, and the project-registry owner.

## Decide

- **Item 1 (lead decision): the premise scope.** It is widened to the directories from H to the root, the root itself, the S3 launch-walk directories, `.opensip/`, and the S3 custody-checked files: the config file and the workspace markers. Those files are user-created and usually omit the ACL. The scope excludes OpenSIP's operational files, I, data-only files, and anything off H's volume. Is this widening sound under 458 §5 and 458c item 3, and closed? Should custody-checked user files instead refuse on omission?
- **Item 2.** Is restricting roots to strictly below H, on H's volume and outside OpenSIP, with an `outside-home` refusal for anything else, right?
- **Items 3 to 5.** The chain walk, `ProjectRootAdmission`, the identity sampler, and the registry classification and read reuse.
- **Item 6.** Is the first-registration write sequence right, including the barriers, the creation of `host/projects` parents, and the VCS and marker-tracked refusals?
- **Item 7.** Namespace admission and the S7 lease; is the result fit as X3a's namespace source?
- **Item 8: rows.** Check each subject and detail against the registry and S12. In particular: the identity contradiction subjects on `PROJECT.ROOT_CUSTODY_REFUSED`, and the class of `PROJECT.SCOPE_LIMIT`.
- **Items 9 and 10.** The budget and the unit split.
- Is anything else wrong?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.
