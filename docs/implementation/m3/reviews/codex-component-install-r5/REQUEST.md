# Review request: CI r5, the law "component release installation and tree custody", round 5

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-component-install-r5/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or lanes. Do not take the shared lane lock.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, private test keys, held trees, any T2 store, the T2 cache or any held-out material.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries in both repositories.

## Subject

- **Manifest:** `docs/implementation/m3/component-install/proposal-r5-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 1343 bytes, SHA-256 `ad9c4c55d774a0673ad7f098b300db7f9a10eb1da25bd8632bc4a641c7291db4`, 6 members. Rehash all six.
  - `component-install/PROPOSAL-r5.md` is the subject.
  - `PROPOSAL-r4.md` (`1c6a9833…`), r3, r2 and r1 are history and unchanged.
  - `snapshot-plan-c/c2a/X-C2A-1-r1.md` is the input memo, not law.
- **Bases:** as the manifest names, product `b7538549` and architecture `a87c1234`.
- **Your round 4:** `codex-component-install-r4` (REQUIRED-FINDINGS: CI-R4-RF-1, NBO-1), at `/tmp/opensip-implementation/reviews/codex-component-install-r4/`.

## Authority

As in round 4, plus:
- `crates/platform/src/filesystem/descriptor_acl_capture.rs`:116 (`descriptor_acl_capture_cost`);
- the custody chain `crates/security/src/snapshot_source.rs`:444 → `private_access::observe_private_directory` → `capture_descriptor_acl_accounted`.

## What to review

`PROPOSAL-r5.md` opens with an r5 changes table. Judge:
1. **R4-RF-1:**
   - the capability's retained `tree/` handle, charged once in `B_open`;
   - `transfer` defined relative to it, with an explicit path depth `k` and base, and component-by-component no-follow resolution;
   - `B_transfer(f)`'s `k − 1` descents plus the file open;
   - CI-T22's root-level and nested Blob controls, with the sink commit gated on final verification.
2. **R4-NBO-1:** `cust` is the custody helper's actual charge, `descriptor_acl_capture_cost()`, with no substitute allowance and no double charge. P-7 is narrowed to `status_read_cost()`. CI-T22 identifies the call chain.
3. **The lead's final re-derivation:**
   - the explicit **handle discipline**, with at most the stage, `tree/` and the current path's stack open, and no handle per entry;
   - staging's per-member parent-chain descents;
   - the finalization traversal's descents and per-file opens;
   - the `fopen` price throughout;
   - P-3's read-only-handle fallback.
   **Re-check `B_install`, `B_open` and `B_transfer` against items 4 to 6's step lists once more.** The lead intends this as the last pricing round: please say whether every operation is now covered.
4. **No regression** in what rounds 1 to 4 accepted.

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `CI-R5-RF-n` / `CI-R5-NBO-n`. Accepting this law accepts no code, binding or qualification.
