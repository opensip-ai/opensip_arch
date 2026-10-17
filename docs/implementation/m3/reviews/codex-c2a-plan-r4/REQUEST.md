# Review request: C2A-PLAN-r4 (the C2a implementation plan: closure admission and the core role closures; M3-C r8 items 7, 8 and 9), round 4

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-c2a-plan-r4/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or lanes.
- No network.
- Do not read the private 413 fixture, the installation directory, **signing keys or private test keys**, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries. Do not run the scratch programs; read their source and logs.

## Subject

- **Manifest:** `docs/implementation/m3/snapshot-plan-c/c2a-plan-r4-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 2602 bytes, SHA-256 `a0da4eb0a9c4049eaec79acac6efcdd584a974d675f8a52b7413e9ffe32ab859`, 12 members:
  - `c2a/PLAN-r4.md` (the subject);
  - `c2a/PLAN-r3.md`, `PLAN-r2.md` and `PLAN-r1.md` (history);
  - `c2a/X-C2A-1-r1.md` and `c2b/C2B-GATING-r1.md` (context);
  - `c2a/evidence/size-check-r3/` and `c2a/evidence/funding-check-r4/`, each its `Cargo.toml`, `src/main.rs` and `run.log`: scratch programs run against the real `opensip_identity` crate, as evidence, not product code.

  Rehash all twelve.
- **Bases:** as the manifest names. Product is `3742822`; since round 3's `b753854` it moved only by the C1a4 blind gate (`snapshot_ledger_census.*`, `snapshot_walk_tests.rs`, a census test), which touches no file the plan cites.
- **Your round 3:** `codex-c2a-plan-r3` (REQUIRED-FINDINGS: R3-RF-1, R3-RF-2), at `/tmp/opensip-implementation/reviews/codex-c2a-plan-r3/`.

## Authority

As in round 3. In addition:
- `opensip/crates/identity/src/canonical.rs`:315-320 (the integer path);
- `crates/host/src/snapshot_seal.rs` (C1a3's accepted hand encoders and their equality controls);
- std's `slice::sort_unstable_by` (the sort the plan no longer uses).

## What to review

`PLAN-r4.md` opens with an r4 changes table. Judge:
1. **R3-RF-1** (LD-C2A-3, LD-C2A-10): C2a now hand-encodes the descriptor into exactly one `Vec::with_capacity(D)`, with digits from a stack buffer and no `String`, `format!` or `write!`, in C1a3's pattern, with equality to `canonical_bytes` as a control. Is the whole first encoding then exactly one charged allocation of D bytes? Check:
   - that the dropped `JsonValue` descriptor tree removes its prices without leaving an unpriced allocation;
   - that the identity-admission exception stays scoped to `IdentityCandidate` internals;
   - the controls: large integer widths, every escape class, exact funding against one-short funding, and the allocation pin;
   - the counting-allocator evidence (14 allocations for `canonical_bytes` on 6 integers, against 1 for the hand encoder).
2. **R3-RF-2** (LD-C2A-10): the deterministic bottom-up merge sort over indices that charges one edge before each comparison, with `Budget` propagating. Check:
   - its published reference bound of n·⌈log₂ n⌉ and its argument;
   - the two index buffers' prices;
   - the duplicate pass;
   - the controls: reverse-ordered 20 paths, adversarial larger orders, and a scope funding only r3's estimate making no unfunded comparison;
   - the recorded evidence.
3. **No regression** from rounds 1 to 3.

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `C2APLAN-R4-RF-n` / `C2APLAN-R4-NBO-n`.
