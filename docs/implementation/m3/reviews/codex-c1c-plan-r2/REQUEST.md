# Review request: C1C-PLAN-r2 (the `node_modules` read set, M3-C r8 item 3), round 2

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-c1c-plan-r2/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or lanes.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries.

## Subject

- **Manifest:** `docs/implementation/m3/snapshot-plan-c/c1c-plan-r2-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 572 bytes, SHA-256 `2dee52328359d82c57112c12cd9d109b071f03a5cd599f4c3f8d5ce6d9b397bb`, 2 members: `c1c/PLAN-r2.md` (the subject) and `c1c/PLAN-r1.md` (history, unchanged). Rehash both.
- **Bases:** product main `3d1d771` and architecture `2d169666`, as the manifest names.
- **Your round 1:** `codex-c1c-plan-r1` (REQUIRED-FINDINGS: C1CPLAN-R1-RF-1 to RF-3, NBO-1, NBO-2, and rulings on Q1 to Q5), at `/tmp/opensip-implementation/reviews/codex-c1c-plan-r1/`.

## Authority

As in round 1. Also cited:
- `crates/security/src/custody/discovery_rule.rs` (`classify_path`, `cargo_roots_from_markers`, the private segment tables);
- `crates/security/src/snapshot_walk.rs` (`SnapshotExtent`);
- `tools/security/discovery_census.py` (`receipt_bindings`, CLOSURE).

## What to review

`PLAN-r2.md` opens with an r2 changes table. Judge:
1. **RF-1:** the new shared-rule API `read_set_path` beside `classify_path` in `discovery_rule.rs`:
   - the authorized directory's own ancestry;
   - ordinary descendants admitted;
   - a further exact `node_modules` segment stopping descent;
   - VCS segments excluded throughout the whole path;
   - the package-local Cargo-root derivation over the same private tables;
   - discovery's `classify_path` semantics and vectors unchanged;
   - its controls (ordinary `lib/x.ts`, pnpm paths, nested packages, VCS above, at and below `realPath`, package-local Cargo output).
   C1c-0 owns it, with the whole-file CLOSURE re-pin.
2. **RF-2:** LD-C1C-12 binds the walk's own `SnapshotExtent`, with same-root provenance as a composition precondition, and applies it before descent, reach and origin change, and admission. Excluded required manifests stay leftovers and refuse. Check the ignored-package and excluded-boundary controls, including one with a C2-captured manifest, and that the workspace-link behaviour is kept.
3. **RF-3:** LD-C1C-9's receipt-specific evidence:
   - what each receipt binds;
   - which sub-unit changes which receipt;
   - an empty delta for an unchanged receipt;
   - stale rendering only where bindings changed;
   - the joining-C1b's-batch case versus the standalone case;
   - every receipt current at the final refresh.
4. **NBO-1:** LD-C1C-8's full-ledger inputs, the per-layout 100,000 limit, the typed-refusal placement and the Q5-ruled gate.
5. **NBO-2:** C2b's obligations inside a standalone interval.
6. **The folded rulings** (Q1 to Q5), the per-row manifest join under deduplication and the workspace-link join, and **no regression** in what round 1 accepted.

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `C1CPLAN-R2-RF-n` / `C1CPLAN-R2-NBO-n`.
