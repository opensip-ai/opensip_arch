REVIEWER review: X2b-1, project root selection, the R0 registry capture, ProjectRootAdmission and classification, with inventory v88. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/REVIEWDIR. If you build, use a CARGO_TARGET_DIR under that directory.

Law: `docs/implementation/m2/project-root-x2/PROPOSAL.md` r5 (accepted). The X2b split: X2b-1 here; X2b-2 is the Git tracking check (item 6a), still to come.

## Subject

Pins are in hashes.txt.
- **Product:** the worktree `/Users/sb/code/opensip-ai/opensip-x2b`, based on 8bfc78a (X2a integrated). Save `git -C <worktree> diff` (new files are intent-to-add) as product.diff and report its sha256.
- **Arch:** v88 (provisional; parent v84), `project-admission-inventory-v88-subject.json` and `project-admission-inventory-v88/`.

## What it does

The code is in `custody/project_admission.rs`.
- **`select_project_root` (S3).**
  - An explicit path is examined once.
  - Otherwise the walk goes upward over retained no-follow handles, at most 256 levels, using the new `path_binding::visit_directories_upward`:
    - a custody failure at the launch refuses; one at an ancestor is a boundary;
    - an `opensip.json` is custody-checked and selects its directory;
    - otherwise a VCS marker selects the repository root;
    - home, `/` and a mount change all select the launch.
- **`capture_registry` (item 5).** The registry is read once, capped at 4 MiB, with full metadata equal to the session's judgment before and after, the whole document decoded, and v1 positively absent. A failure is unavailable.
- **The marker.** `.opensip` is checked with S3 custody under the premise. The marker is judged private, then read exactly and decoded.
- **The incarnation.** The volume UUID is read through `observe_volume`, charged, on the same file as X2a's birth sample.
- **`classify`.** Implements the registry owner's table.
- **`admit_project_root`.** Runs in law order. `ProjectRootAdmission` is not Clone; its `recheck` covers the chain, volume, marker and registry. It grants nothing until X2b-2.
- **`ReadSession::admit_project_root`.** Runs on the session ledger, rechecks, and latches on failure.
- **Supporting edits.** `project_chain.rs` generalises the root judgment to `judge_project_object`. `Chain` records H as walked. `installation_read.rs` gets the entry point.

## Judgment calls: please rule on each

1. The X2b-1 / X2b-2 split.
2. H is taken from the session's walk, not from the account record, so fixture and real sessions stay consistent.
3. There is no write-gate entry yet; that is X2c and X2d.
4. The marker is judged private, as OpenSIP's own operational file outside the premise. A custody failure is root custody with the new subjects `marker-custody` and `marker-directory-custody`. A non-regular object, wrong size or wrong frame is Contradiction.
5. Registry rows: missing, oversized, malformed or v1 present is incomplete; a metadata mismatch is `required-files-changed`; a read error is host I/O.
6. Registry decoding is charged as one step.
7. Selection examines up to and including H.
8. There is no `--trust-project-owner`, and an explicit path must already be resolved.
9. The mount boundary is untested in scratch.
10. v88 is provisional, and `project_chain.rs`'s description is now stale.

## Checks

- Workspace: 1224/0, on two runs. 15 new tests. Clippy and fmt are clean.
- `check_package_edges` passes.
- verify_scratch (v88) passes.

## Decide

- Does X2b-1 implement X2 r5 items 3 to 5 and the S3 selection exactly?
- Rule on the judgment calls, in particular the new marker subjects.
- Is v88 right?
- Is anything else wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256" (the sha256 of project-admission-inventory-v88-subject.json);
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes, sha256 of v88, parent (the v84 pin), successorRecord}.

Write REVIEW.md and review.json. Do not commit.
