Grok re-review: X2b-1 r2 (project admission) after Grok's r1 findings. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-project-admission-x2b1-r2. If you build, use a CARGO_TARGET_DIR under it.

Subject: the worktree `/Users/sb/code/opensip-ai/opensip-x2b`, rebased onto 5b5f04c (v87 selected). Pins are in hashes.txt. Save the diff as product.diff and report its sha256. Inventory v88 is rebuilt with parent v87. The r1 review is `reviews/grok-project-admission-x2b1-r1/`.

## Changes

- **RF-1.** The platform publishes `directory_volume_observation_cost()`: two status reads, two filesystem observations, and the attribute read with its buffer. `sample_incarnation` charges it first. Tests cover one byte short and exactly enough.
- **RF-2.** Capture and filesystem I/O on `opensip.json`, `.opensip` and the marker are now host I/O. Real custody refusals keep their rows (`config_refusal`, `marker_directory_refusal`, `marker_capture_refusal`). Each mapping is tested with injected I/O and with real refusals.
- **Inventory RF-1 (installation_read.rs description).** verify_design (lines 138–140) forbids an inventory successor from changing an inherited row, so v88 carries it unchanged. The correction is deferred to a description-only contract successor, as 461b did. The proposed text is in the v88 README. Is that deferral acceptable?

## Checks

- X2b: 17/17. Clippy and fmt are clean.
- `check_package_edges` passes, and so does verify_scratch (v88).
- Workspace: 1233/0 on one run. Another run failed only the `native_census` flake (F3), which also fails on clean main and is caused by concurrent test processes. A fix is in progress.

## Decide

Are RF-1 and RF-2 closed, and is the description deferral acceptable? Is anything new wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256" (the sha256 of project-admission-inventory-v88-subject.json);
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes, sha256 of v88, parent (the v87 pin), successorRecord}.

Write REVIEW.md and review.json. Do not commit.
