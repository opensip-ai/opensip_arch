Grok re-review: law X2 r4 after Grok's r3 findings. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-project-root-x2-r4. Law review; no product cargo.

Subject: docs/implementation/m2/project-root-x2/PROPOSAL.md r4 (pin in hashes.txt). `diff` it against PROPOSAL-r3.md. Earlier findings are in `reviews/codex-project-root-x2-r1/`, `-r2/` and `reviews/grok-project-root-x2-r3/`.

## Changes

- **RF-1.** The replacement method's step 1 reconfirms R0 before RESERVED and R1 before ACTIVE. Item 7 takes N from R's ACTIVE row (R0 if already registered, R2 if just registered), and item 5's one-read rule refers to R.
- **RF-2.** Item 6a reads Git's fixed configuration sources:
  - system: `/etc/gitconfig`, the CLT and Xcode `git-core/gitconfig`, `/opt/homebrew/etc/gitconfig` and `/usr/local/etc/gitconfig`;
  - global: `H/.config/git/config` and `H/.gitconfig`, with H from the account database;
  - the repository `config`.

  Each source is positively absent, or read under custody with a 64 KiB cap and the closed parse, with case-insensitive names. Refuse on:
  - `include` or `includeIf`, `core.worktree`, a true `core.bare`, `extensions.*`, a format version other than 0, `precomposeunicode=false`, or anything the parse can't bound;
  - any `GIT_*` variable, `XDG_CONFIG_HOME`, or a `HOME` that differs from H. Reading the environment only to refuse is not an owner §1a override.

  Item 1's scope now covers the global config under H (lead decision), and the system config on H's volume, which must be root-owned. A Git build with an unlisted system path is a stated limit.
- **RF-3.** Index versions 2, 3 and 4 are decoded exactly:
  - v3 extended flags;
  - NUL-terminated paths with padding, and a length check;
  - v4 prefix compression, with an overlong removal refused;
  - the trailing checksum verified and every byte consumed;
  - `link` or `sdir` extensions, and unknown required extensions, refused.

## Decide

- Are RF-1 to RF-3 closed?
- Is the fixed source list, together with the refusal set, a sound and closed approximation of Git's effective configuration on macOS?
- Is the decoding of index versions 2 to 4 correct per Git's index-format documentation?
- Is the whole law sound?
- Is anything new wrong?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.

Note: r4 also carries a pre-review correction from X3b r2: item 7a step 3 orders X3b's floor step and carrier start inside the single fence hold.
