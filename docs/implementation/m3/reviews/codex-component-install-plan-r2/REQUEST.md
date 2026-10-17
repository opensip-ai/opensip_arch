# Review request: CI-PLAN-r2, the component installation implementation plan, round 2

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-component-install-plan-r2/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or lanes. Do not take the shared lane lock.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, private test keys, held trees, any T2 store, the T2 cache or any held-out material.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries in both repositories.

## Subject

- **Manifest:** `docs/implementation/m3/component-install/plan-r2-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 567 bytes, SHA-256 `4441a858d82ccba0dd3a2e6efa39b8b6e43be114aa75fca180e8dc26e3bafa2a`. It has 2 members, `component-install/PLAN-r2.md` and, as history, `component-install/PLAN-r1.md` (unchanged since your round 1). Rehash both.
- **Bases:** as the manifest names (product `3742822e`, architecture `4088af76`).
- **Round 1:** your `codex-component-install-plan-r1` (`REVIEW.md` and `review.json` in its directory): REQUIRED-FINDINGS, with CIPLAN-R1-RF-1, CIPLAN-R1-RF-2, CIPLAN-R1-NBO-1 and CIPLAN-R1-NBO-2, and the rulings on Q1 and Q2.

## Authority

- **The accepted law:** `docs/implementation/m3/component-install/PROPOSAL.md` (r5 under its acceptance note).
- **RF-1's authority:** `crates/platform/src/locks.rs` (`FileLock::try_acquire`, `try_acquire_retaining`:50-94, `release`/`unlock`/`Drop`:100-123), and `crates/platform/src/filesystem/directory_publication.rs`:60-61 (descriptor closes are not counted).
- **RF-2's authority:** `crates/platform/src/filesystem/file_effects.rs` (`FileBarrierReceipt`:80-92 and its constructors, `write_new_regular_accounted`:195-216).
- Everything round 1's request named: the C2a plan r4 (`snapshot-plan-c/c2a/PLAN-r4.md`), including its R3-RF-2 sort recipe; `tools/security/discovery_census.py` (`CLOSURE`, `receipt_bindings`); `tools/security/snapshot_ledger_census.py` (`sources()`, `bindings()`, `ANCHORED`); the C1b plan r3's stale-receipt rules; and the O1-a package policy.

## What to review

Judge whether r2 resolves each round-1 item, as its "r2 changes" table maps them:
1. **CIPLAN-R1-RF-1 (LD-CIP-1, LD-CIP-11, CI-PT-5):** P-6 is no longer `FileLock`. It is a one-attempt native lock in `component_tree.rs` that makes exactly one `flock(LOCK_SH | LOCK_NB)`, or `LOCK_EX | LOCK_NB` for GC's probe. It accepts only P-4's opened-file type, so close-on-exec and regular-file kind hold by construction. Release is the uncounted close on drop, with no `LOCK_UN` and no duplicate descriptor. Is LAW's one-edge price now exact over the full native call sequence, including release?
2. **CIPLAN-R1-RF-2 (LD-CIP-1, LD-CIP-10, CI-PT-6):** P-3 returns a new opaque `StandaloneBarrierReceipt<'file>`, produced only by `component_tree::barrier_file`. It witnesses one completed `F_FULLFSYNC` on that exact handle (`is_for` by pointer identity), has no public constructor and claims no bytes. `FileBarrierReceipt` stays unchanged and unused. Is it constructible, correctly scoped and outside the bound sources?
3. **CIPLAN-R1-NBO-1 (LD-CIP-4 r2):** a branch-contiguous, manifest-driven DFS post-order with a retained current-branch stack. Each directory is entered once and finalized after its descendants, with no `readdir`. The priced auxiliary index uses a charged bottom-up merge sort.
4. **CIPLAN-R1-NBO-2 (LD-CIP-8):** the stop-and-re-plan rule now covers each receipt's full bound-input set. For discovery, that is everything `receipt_bindings` binds. For the companion, it is everything `bindings()` binds, including snapshotSources and `ANCHORED`. The changed-file set is computed from the binding code. `--check` results and byte-equal receipts are not treated as freshness.
5. **The Q rulings applied:** Q1 in §2 (CI-1 first, then CI-2 and CI-3 as one package, lane and review, with separate control ownership and no claim of standalone CI-2 completion). Q2 in LD-CIP-6 (macOS only; every other target fails closed through the typed unsupported-platform route before any native call, with no fallback; LAW's platform table is unchanged).
6. **The new mutations (§5) and checks (§6)** for directory re-entry, P-6 over `FileLock` or with `LOCK_UN`, and P-3's receipt without a barrier or with `is_for` by inode.
7. **The matching law corrections, LC-1 and LC-2** (header). LC-1: LAW item 4's P-3 names `FileBarrierReceipt`, but the plan uses `StandaloneBarrierReceipt`. LC-2: LAW's `B_install` step 4 has no row for the ordering index and comparisons. These are flagged for the lead, who will decide whether a law amendment is needed. Judge whether each is a correct and complete statement of the divergence, whether any other law text diverges from r2 (the plan says P-6 needs none), and whether the plan is acceptable conditional on the lead's disposition.
8. **Regressions:** has any r2 change broken a round-1 conclusion that you accepted?

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `CIPLAN-R2-RF-n` / `CIPLAN-R2-NBO-n`. Accepting this plan accepts no code.
