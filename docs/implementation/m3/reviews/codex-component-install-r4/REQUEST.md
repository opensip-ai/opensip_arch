# Review request: CI r4, the law "component release installation and tree custody", round 4

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-component-install-r4/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or lanes. Do not take the shared lane lock.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, private test keys, held trees, any T2 store, the T2 cache or any held-out material.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries in both repositories.

## Subject

- **Manifest:** `docs/implementation/m3/component-install/proposal-r4-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 1152 bytes, SHA-256 `33f265779be2cd6a976bb1d279205b387c90bb1876ee109840db0997ecd2e2dc`, 5 members. Rehash all five.
  - `component-install/PROPOSAL-r4.md` is the subject.
  - `PROPOSAL-r3.md` (`3f74b023…`), `PROPOSAL-r2.md` (`e514ee26…`) and `PROPOSAL-r1.md` (`286ebf5a…`) are history and unchanged.
  - `snapshot-plan-c/c2a/X-C2A-1-r1.md` is the input memo, not law.
- **Bases:** as the manifest names, product `b7538549` and architecture `a87c1234`.
- **Your round 3:** `codex-component-install-r3` (REQUIRED-FINDINGS: CI-R3-RF-1, NBO-1, NBO-2), at `/tmp/opensip-implementation/reviews/codex-component-install-r3/`.

## Authority

As in round 3, plus:
- `crates/platform/src/process.rs` `descend_cost` and `READ_COST`, D3a-0's traversal recipe;
- `crates/platform/src/filesystem.rs`:1883 (`descriptor_observation_cost`);
- `filesystem/path_binding.rs`:121 (`status_read_cost`).

## What to review

`PROPOSAL-r4.md` opens with an r4 changes table. Judge:
1. **R3-RF-1:** whether `B_install`, `B_open` and `B_transfer` are now **complete**. Check every operation in items 4 to 6 against the recipe rows, step by step. The rows include:
   - the `tree/` container's create, `fchmod` and barrier, and the stage barrier;
   - `generation.json`'s exclusive create, its owned record, and V2's bounded read and byte comparison;
   - the archive open (P-5), the custody checks and the traversal descents;
   - `pin.lock`'s open, state check and `flock`.
   Then judge:
   - the record length `R`, computed from authenticated release fields with checked arithmetic;
   - the uncharged borrowed-input list;
   - the reserved-versus-executed distinction;
   - the new primitive prices, P-5 to P-7;
   - CI-T22's file-only, nested, metadata-heavy and pre-existing-generation enumerations.
2. **R3-NBO-1:** the explicit split `effect = 0`, `postchecks = exclusive_publication_cost() + directory_barrier_cost()`, with no double charge; and the routes, where a pre-acquisition excess is `install-budget` and an in-operation charge or reservation failure takes law 468's operational route. Check CI-T26.
3. **R3-NBO-2:** an unconfirmed rename may leave the name absent or present after restart, with the three verification outcomes kept.
4. **No regression** in what rounds 1 to 3 accepted.

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `CI-R4-RF-n` / `CI-R4-NBO-n`. Accepting this law accepts no code, binding or qualification.
