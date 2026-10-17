# Review request: CI-PLAN-r1, the component installation implementation plan, round 1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-component-install-plan-r1/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or lanes. Do not take the shared lane lock.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, private test keys, held trees, any T2 store, the T2 cache or any held-out material.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries in both repositories.

## Subject

- **Manifest:** `docs/implementation/m3/component-install/plan-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 380 bytes, SHA-256 `bb4d73dc567deb39c038528af95371fe9c5ccb048e01895d23425972e8c3bb52`. It has 1 member, `component-install/PLAN-r1.md`. Rehash it.
- **Bases:** as the manifest names.

## Authority

- **The accepted law:** `docs/implementation/m3/component-install/PROPOSAL.md` (r5 under its acceptance note; your `codex-component-install-r5`, ACCEPT, with NBO-1 to NBO-3 carried to this plan).
- The C2a plan r4 (`snapshot-plan-c/c2a/PLAN-r4.md`): its C2a-1 bridge and C2a-3's binding.
- The census closures and receipts at the plan base `3742822e` (after the C1a4-blind gate): `tools/security/discovery_census.py` (`CLOSURE`, `receipt_bindings`) and `tools/security/snapshot_ledger_census.py` (`sources()`, `bindings()`, `ANCHORED`). Also the C1b plan r3's stale-receipt rules (`snapshot-plan-c/c1b/PLAN-r3.md`).
- The product files it names: `crates/platform/src/lib.rs`, `custody_entry.rs`, `locks.rs`, `filesystem.rs`:340, `filesystem/path_binding.rs`:118-126, `crates/lifecycle/`, and `crates/security/src/snapshot_source.rs`:444.
- The O1-a package policy (`docs/implementation/m3/operability/o1-package-policy-r1/package-policy.json`).

## What to review

Judge:
1. **The split** into CI-1 to CI-4, its dependencies and order, the files (CI-2 realizes the planned row `crates/lifecycle/src/installation.rs`), and C2a-3's binding of CI-3.
2. **The NBO answers:** LD-CIP-4 (the finalization walk is driven by the TreeCommitment, with no `readdir`), LD-CIP-5 (`R`'s exact derivation and the hand encoder) and LD-CIP-6 (the access mode selected before the charged open, with no retry).
3. **LD-CIP-1 and LD-CIP-2:** P-1 to P-6 in a new platform module outside the census closure, and P-7 as an equal published price checked by a source pin. Does this satisfy LAW item 4?
4. **LD-CIP-3:** lifecycle's fixture-feature forwarders under the joint predicate.
5. **LD-CIP-7:** the single trust bridge, C2a-1's.
6. **LD-CIP-8:** the census and receipt impact per sub-unit and per receipt, every lane's "unchanged" assertion, and the stop-and-re-plan rule.
7. **LD-CIP-9:** the X-CI-1 gate, its trigger, its census impact (`work_ledger.rs` in both receipts' bindings), and the separate unit X-CI-1-a.
8. **The control map:** every LAW control CI-T1 to CI-T26 is assigned, plus CI-PT-1 to CI-PT-4; the mutations; the checks.
9. **Q1 and Q2.**

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `CIPLAN-R1-RF-n` / `CIPLAN-R1-NBO-n`. Accepting this plan accepts no code.
