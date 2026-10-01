REVIEWER review: X2a, the project-root chain walk, custody and birth sample, with inventory v84. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/REVIEWDIR. If you build, use a CARGO_TARGET_DIR under that directory.

Law: `docs/implementation/m2/project-root-x2/PROPOSAL.md` r5 (accepted), X2a's scope per its unit list.

## Subject

Pins are in hashes.txt.
- **Product:** the worktree `/Users/sb/code/opensip-ai/opensip-x2a`, based on 84a8bfd. Save `git -C <worktree> diff` (new files are intent-to-add) as product.diff and report its sha256.
- **Arch:** `repository-file-inventory.v84.json` (parent v83, which is under review with X3a-1), `project-chain-inventory-v84-subject.json` and `project-chain-inventory-v84/`.

## What it does

The code is in `custody/project_chain.rs`.
- **`ProjectChainPolicy::new(premise, home_filesystem, trust_groups)`.** It borrows the receipt's premise, the H-filesystem check and the explicit trust groups.
- **`walk_project_chain`.** It is charged throughout:
  1. a path-only placement check before any open: the root must be strictly below H, and not under `Library/Application Support/OpenSIP` (compared ignoring case). Otherwise it is `OutsideHome`;
  2. `RetainedDirectoryPath::open_project_root`, with at most 256 components;
  3. from `/` to the root's parent, the shared `judge_ancestor` with the premise. The root itself uses S3 directory custody;
  4. every directory from H down must be on H's volume;
  5. the names are rechecked;
  6. the root's birth is sampled with `observe_birth`, charged.
- **`check_project_root`.** The shared `check` with trust groups, then the ACL. A write allow must name the user, root or a trusted group.
- **`ProjectChain`.** Not Clone, grants nothing, and has a recheck that compares names, custody, volume and birth.
- **`ProjectChainRefusal::row()`.** One of `RootCustody(subject)`, `ExplicitPath` or `HostIo`, using item 8's subjects.
- **Cost.** A 64-level chain costs 577 objects, 10,937 edges and about 1.09 MB.

## Judgment calls: please rule on each

1. No `InstallationTermination` or host projection yet. Those are X2b's.
2. A symlink component reports `ENOTDIR` on macOS no-follow opens, so it takes the explicit-path row. `ELOOP` maps to `symlink`, by comparing the raw value 62, because there is no `libc` dependency and `FilesystemLoop` is unstable.
3. A missing, non-directory, bad or relative root is the explicit-path row (S3).
4. Every directory from H down must pass the volume check, not only the ones the premise admits.
5. Only birth is sampled. The volume UUID is left to X2b.
6. The only overlap with X3a-1 is the module declaration in `custody.rs`.

## Checks

- Workspace: 1186/0, on two runs. 14 new tests. Clippy and fmt are clean.
- `check_package_edges --lane host` passes.
- verify_scratch (v83 then v84) passes.

## Decide

- Does X2a implement the X2 r5 items in its scope exactly: placement, the premise scope for directories, the chain walk, custody, volume, birth and recheck?
- Rule on the judgment calls.
- Is v84 right?
- Is anything else wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": a single string, the sha256 of project-chain-inventory-v84-subject.json;
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes and sha256 of v84, parent (the v83 pin), successorRecord}.

Write REVIEW.md and review.json. Do not commit.
