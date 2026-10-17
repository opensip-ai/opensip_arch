# Review request: C1C-PLAN-r4 (the `node_modules` read set, M3-C r8 item 3), round 4

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-c1c-plan-r4/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or lanes.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries.

## Subject

- **Manifest:** `docs/implementation/m3/snapshot-plan-c/c1c-plan-r4-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 950 bytes, SHA-256 `fe38baf6d718ecc3b1025f4a1e111eace35da39ec0a02afcb4cab4ee0bd0c752`, 4 members: `c1c/PLAN-r4.md` (the subject), and `c1c/PLAN-r3.md`, `PLAN-r2.md` and `PLAN-r1.md` (history, unchanged). Rehash all four.
- **Bases:** product main `b753854` and architecture `bd77891d`, as the manifest names. The plan states that every cited product file is byte-identical to its version at `3d1d771`; verify this with Git.
- **Your round 3:** `codex-c1c-plan-r3` (REQUIRED-FINDINGS: C1CPLAN-R3-RF-1, RF-2), at `/tmp/opensip-implementation/reviews/codex-c1c-plan-r3/`.

## Authority

As in rounds 1 to 3. Also cited:
- `crates/security/src/snapshot_walk.rs`, the Cargo-key charge and its removal on frame exit;
- `snapshot_source.rs`'s `key_cost`;
- `custody/discovery_walk.rs`'s `owned`;
- `custody/discovery_rule.rs`'s `classify_path` Cargo test;
- `workspace_declarations.rs` and `identity/src/descriptors.rs`, for the member bound.

## What to review

`PLAN-r4.md` opens with an r4 changes table. Judge:
1. **R3-RF-1:** C1c-0's ownership of the `WalkEvidence` retention's charge change, model and anchor changes, soundness vectors, r9 fixed-cap and 2× evidence, and companion receipt impact. Check LD-C1C-13's statement of what is new and what is moved:
   - **the Cargo roots:** keeping the already-charged keys is zero-increment, and keeping a non-ancestor root changes no classification. Check the argument and the exact charge-equivalence control;
   - **the member roots:** a new charged copy, bounded by 64 members of at most 16,384 bytes each.

   Is LD-C1C-9's accounting now consistent, and does C1c-1 extend the accepted recipe rather than re-price it?
2. **R3-RF-2:** the guard requires at least one eligible authorization. Preparation records, under charge, the longest eligible prefix as a chosen authorization, and sealing checks it allocation-free. The per-layout-row digest joins and the single capture are kept. Check the new overlapping-`realPath` control and the mutations.
3. **No regression** in what rounds 1 to 3 accepted.

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `C1CPLAN-R4-RF-n` / `C1CPLAN-R4-NBO-n`.
