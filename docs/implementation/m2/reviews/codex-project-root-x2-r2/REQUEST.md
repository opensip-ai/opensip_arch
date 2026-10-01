Codex re-review: law X2 r2 after your r1 findings. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/codex-project-root-x2-r2. Law review; no product cargo. Product HEAD is f7acb6d (X1a integrated).

Subject: docs/implementation/m2/project-root-x2/PROPOSAL.md r2 (pin in hashes.txt). `diff` it against PROPOSAL-r1.md.

## Changes

- **RF-1.** Item 7: EXCLUSIVE takes `writer.lease`, then `readers.lease`, both LOCK_EX|NB under the fence. On a partial failure they are released in reverse order before the fence, and any retry happens outside the fence. This builds on `lifecycle::leases`.
- **RF-2.** Item 5: X2 owns the first registry capture: one bounded, charged read, with the original and parent retained and the whole document validated. `v1` must be positively absent, and both checks join the recheck set. A missing or malformed registry is unavailable, never empty.
- **RF-3.** Item 6: one replacement method for both RESERVED and ACTIVE:
  1. reconfirm the old file and its parent;
  2. validate the full document;
  3. write a temporary file, flush it and confirm it;
  4. atomically replace the registry name;
  5. flush the parent directory and recheck.

  The recovery gate and the capacity, collision and occupancy checks run before any effect, and the durable states at each failure point are listed.
- **RF-4.** New step 4: `.opensip` is created or admitted with its own flush and the root's flush, including reused folders, before the marker.
- **RF-5.** New item 6a: the tracking check.
  - It walks from the root to `/`. `.hg`, `.svn`, `.jj` or a `.git` file refuses as `vcs-unsupported`.
  - It reads the nearest `.git` directory's index (versions 2–4, no split or sparse index, at most 4 MiB). A tracked marker path refuses.
  - "Untracked" requires positive lookups at every level.
  - It runs for both reuse and first use, and its evidence is rechecked.
- **RF-6 (lead decision).** X2d returns a `FencedNamespace` and keeps the fence. A new unit, X2e, joins row, root, marker, tracking, namespace and the X3a endpoint into a non-Clone `ProjectOperation` before releasing the fence. Until then, a `FencedNamespace` can only be dropped.
- **RF-7.** Item 8: `PROJECT.SCOPE_LIMIT` is request-rejected, exit 2, `REQUEST.UNSATISFIABLE`, with no fault cause. The subjects are `registry-rows:<n>>4096`, `registry-bytes:<n>>4194304` and `registry-transition-rows:<n>>4096`, and the remedy never suggests deletion.
- **Also.** The birth sampler reuses `RetainedDirectory::observe_birth`. The forbidden-substitutes list is extended, and the units are X2a–X2e.

## Decide

- Are RF-1 to RF-7 closed?
- Is "the nearest `.git` directory wins" sound for nested repositories?
- Is X2e's handoff sound?
- Is anything new wrong?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.
