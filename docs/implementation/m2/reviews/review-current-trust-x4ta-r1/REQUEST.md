REVIEWER review: X4T-a, the read-only current-trust admission, with inventory v90. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/REVIEWDIR. If you build, use a CARGO_TARGET_DIR under it.

Law: `docs/implementation/m2/trust-admission-x4t/PROPOSAL.md` r5 (accepted). X4T-a's scope: items 1–6 and 8–11, with time report-only and no floor publication.

## Subject

Pins are in hashes.txt.
- **Product:** the worktree `/Users/sb/code/opensip-ai/opensip-x4ta`, based on 5b5f04c. Save its diff as product.diff and report its sha256.
- **Arch:** v90 (parent v87), `current-trust-inventory-v90-subject.json` and `current-trust-inventory-v90/`.

## What it does

The new module is `trust/current_trust_admission.rs`, a child of `ordinary_targets`.
- **Two entry points:** `admit_current_trust` (a supplied capsule, which reuses X3a's capture) and `admit_native` (`capture_p2`, then a recheck of `state.v1`).
- **`AdmittedCurrentTrust`:** the standing, the `TrustEpoch` (versions plus `Effective::digest()`), the fenced `TimeAdmission`, and the revoked subjects.
- **`TrustRefusal`:** carries the 468 item 6 detail and subject.
- **Order of checks:**
  1. F absent;
  2. schema, then the 32-event bound;
  3. `bind` with `bind_trace`, then the `accepted.by` check;
  4. `capsule_clock`, `bind_retained_head`, then the root admission via `Budget::load`;
  5. `authenticate_shared` with `ChainBudget{16, 16 MiB}`;
  6. catalog, revocation, history and time evidence via `Budget::load`, with the catalog envelope reverified and `verify_revocation` run on the loaded bytes;
  7. the closure check, the revoked core, then `merge(Source::Missing, …)`;
  8. `evaluate_retained_ordinary` (fenced reads only);
  9. the continuation standing.
- **Supporting edits:** `role_machine::standing`, `OrdinaryClockProposal::admission()`, `SuppliedP2Current::parts_mut`, `TRUST_VIEW_COST` (128, 2048, 112 MiB), and `view_budget()`.
- **Measured cost:** 23 objects, 44 edges, 35,371 bytes for six roles. A test pins this.

## Judgment calls: please rule on each

1. **X4T-0 fixture fix.** It now lists three envelope rows in the payload closure, which the inventory owner requires. This changes the integrated X4T-0 test file.
2. **X4T-0's source pin.** It now admits X4T-a's `cfg(test)` test file, so v87's fixture-tests description is stale. That is deferred to a description successor.
3. **Item 12 cases the fixture can't build.** A bad signature or wrong quorum, an expired intermediate or final root, a positive revoked core, and a full 40 MiB / 32 / 16 view. These are covered by unit-level bound tests instead. Is that acceptable?
4. The 40 MiB closure total is enforced together with the 16 MiB chain, as 56 MiB.
5. Previously revoked keys are taken as the empty set.
6. Role states come from the capsule. S4's expiry is carried in `TimeAdmission`, not applied to the roles.
7. **Nested owner errors are classified by matching their debug text (`nested_input`).** Is that acceptable, or must the owners expose typed causes?
8. **Row mappings:** an S4 `TimeRange` refusal takes `PAYLOAD-NOT-ADMISSIBLE`, subject `time`; a Recovery role takes the continuation row, subject `recovery`; native digest or absence takes the incomplete row; I/O or the fence takes host I/O.
9. It is not wired into any session yet; that belongs to X4a.

## Checks

- The 14 X4T-a tests and 7 X4T-0 tests pass.
- Clippy and fmt are clean.
- `check_package_edges` passes, and so does verify_scratch.
- **The full workspace was not clean on any of four runs.** Every failure was in `native_census` (the known F3 flake) or in `native_current` and `store_endpoint` under full parallel load. Each of those passes alone. A fix (F3, widened) is in progress.

## Decide

- Does it implement X4T r5's items in scope exactly, especially item 2's loaders and the `accepted.by` check?
- Rule on the judgment calls, especially 3 and 7.
- Is v90 right?
- Is anything else wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256" (the sha256 of current-trust-inventory-v90-subject.json);
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes, sha256 of v90, parent (the v87 pin), successorRecord}.

Write REVIEW.md and review.json. Do not commit.
