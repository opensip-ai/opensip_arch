Grok review: law X2 r3, project-root custody, admission, first registration and namespace leases. Claude Opus 5.5 leads. You are the single reviewer for this round. Codex reviewed r1 and r2; its findings are in `docs/implementation/m2/reviews/codex-project-root-x2-r1/` and `-r2/`. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-project-root-x2-r3. Law review; no product cargo. Product HEAD is f7acb6d.

Subject: docs/implementation/m2/project-root-x2/PROPOSAL.md r3 (pin in hashes.txt). `diff` it against PROPOSAL-r2.md, and read the whole law.

## Changes in r3 (answering Codex r2 RF-1 to RF-4)

- **RF-1 (outer repositories).** Every enclosing `.git` from the root up to `/` has its index checked.
  - A `.git` at or above H, or off H's volume, refuses as `vcs-unsupported`.
  - Gitlink entries neither match nor clear an outer index.
- **RF-2 (registry evidence advances).** There is one current registry owner, R:
  - R0 is the initial capture;
  - R1 is the confirmed RESERVED state, and is ACTIVE's predecessor;
  - R2 is the confirmed ACTIVE state, and the only source for Eligible and the handoff.

  The must-be-absent names pass to their owners only through their own publication. The table of durable states at each failure point is corrected.
- **RF-3 (premise scope for Git files).** The closed premise scope names each enclosing `.git` directory strictly below H, plus its `config` and `index`, each through its own retained descriptor. `commondir` and `config.worktree` are absence-only lookups.
- **RF-4 (worktree root and hash format).** One closed layout:
  - the config is custody-read, capped at 64 KiB, and parsed with a closed subset;
  - `repositoryformatversion` must be absent or 0, which means SHA-1;
  - `core.bare` must be false, `core.worktree` absent, and there may be no includes;
  - `commondir` and `config.worktree` must be absent;
  - index entries must be 20 bytes;
  - the ASCII relative root is compared case-insensitively.

  Everything else is `vcs-unsupported`. An ordinary clone, such as this repository's own, stays admissible.

## Decide

- Are Codex's r2 RF-1 to RF-4 closed?
- Is the whole law now sound and closed: the premise scope, root placement, chain walk, `ProjectRootAdmission`, the registry capture and replacement, the `.opensip` and marker durability, the tracking check, namespace leases, the X2e handoff, rows and budget?
- Is the Git closed-subset approach correct about Git's own semantics, for example config parsing, gitlinks and case folding?
- Is anything else wrong?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.
