# Review request: C1C-PLAN-r3 (the `node_modules` read set, M3-C r8 item 3), round 3

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-c1c-plan-r3/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or lanes.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries.

## Subject

- **Manifest:** `docs/implementation/m3/snapshot-plan-c/c1c-plan-r3-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 761 bytes, SHA-256 `4ebb6fd9db35799dbf61b1ac717d2658e1ae971299a4aa879c132a285a1cff66`, 3 members: `c1c/PLAN-r3.md` (the subject), and `c1c/PLAN-r2.md` and `c1c/PLAN-r1.md` (history, unchanged). Rehash all three.
- **Bases:** product main `3d1d771` and architecture `2d169666`, as the manifest names.
- **Your round 2:** `codex-c1c-plan-r2` (REQUIRED-FINDINGS: C1CPLAN-R2-RF-1, RF-2, NBO-1), at `/tmp/opensip-implementation/reviews/codex-c1c-plan-r2/`.

## Authority

As in rounds 1 and 2. Also cited:
- `crates/security/src/snapshot_walk.rs`, the walk's incremental Cargo-root derivation;
- `crates/security/src/custody/discovery_rule.rs`, `custody_state` as `classify_path` uses it.

## What to review

`PLAN-r3.md` opens with an r3 changes table. Judge:
1. **R2-RF-1:** `read_set_path` over the full authorized path plus descendant. It must:
   - exclude Cargo build output at any depth, using first-party roots from the walk's retained derivation and dependency-tree roots from the reader's observations;
   - exclude the exact root and member `.opensip` custody anchors;
   - exclude VCS segments throughout;
   - keep the allowed lookalikes eligible;
   - run before opening or descending a package, before a capture is reached or its origin changes, before admission, and in sealing's guard.

   Check LD-C1C-13's evidence sources and their provenance:
   - `WalkEvidence` retained by the session;
   - the member-root equality with the walk's extent;
   - the charged `Cargo.toml` observations.

   Also check the new controls: `target/node_modules/a`, a package inside another package's `target`, `.opensip/node_modules/a`, the lookalikes, and the no-open timing spy.
2. **R2-RF-2:** LD-C1C-9's interval rules:
   - joining an open interval only before its freeze;
   - otherwise C1c-1 opening and owning a new interval, after a closed C1b batch and after a separately refreshed C1c-0;
   - receipt-specific deltas against a fresh accepted baseline;
   - no earlier refresh covering a later edit.
3. **R2-NBO-1:** LD-C1C-7's split between charged preparation and retained evidence, and the allocation-free, source-free guard over it. Does LD-C1C-8 now price the added evidence?
4. **No regression** in what rounds 1 and 2 accepted.

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `C1CPLAN-R3-RF-n` / `C1CPLAN-R3-NBO-n`.
