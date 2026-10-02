# Crash-matrix X9-2 inventory131

Adds exactly one file to inventory130 (unit X3d-3, selected at product a2c5e8b and still at cdd4589, where X8c landed; D1's thirty-nine overrides and D2's four supersessions are already folded into its fifty-five inheritance rows):
- crates/storage/tests/fixtures/crash-matrix/required-runs.v1.json

It keeps all 964 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 965 planned files.

**Already planned rows.** X9-2's matrix target, `crates/storage/tests/commit_tests.rs`, is a planned row: "Exercise the actual carrier at each object/journal/ledger/acknowledgement fault point, lock order, revoked sessions and fresh-process recovery". Its bytes are new; the row is unchanged. `tools/check_crash_matrix.py` and `tools/tests/test_check_crash_matrix.py` are also planned rows, and both gain `check-unit` and L11.

**No new edge.** The matrix target calls security (the support surface's three driver entries, `CommitSession`, `RecoveryRequest`), storage's public facade (`prepare_commit`, `recover`, `sweep_namespace`, the synthetic run candidate), the evaluator (`replay_run`), identity and platform (X9-0's driver and barrier API). Each goes along an edge the parent declares from opensip-storage. The builder asserts them.

The row belongs to unit X9-2 (law X9 r9 item 12, with r4's three entries and per-unit check, r5–r7's synthetic candidate, r6's F00 split, r8's F00/F07 R2 and L11, and r9's per-occurrence X4T dependency rule).

- **required-runs.v1.json (fixture).** The reviewed required runs, in the shape `opensip.x9.required-runs.v1`, with `clockEpoch` 1791072000.
  - **Rows:** X9-2's 231 rows: F00 174, F02 3, F03 6, F04 7, F05 6, F07 11, F08 2, F09 3, F10 10, F20 2, F21 1, F22 2, F31 2 and F46 2.
  - **Sources:** they are transcribed from law X9 r9 before any run:
    - the kill points and their order come from the unarmed census of the commit driver (two equal runs);
    - each X4T dependency occurrence's R2 comes from r9's unarmed reference run;
    - every expected value comes from the law's row and is never read back.
  - **Readers:** the matrix target reads it, and the checker's `check` and `check-unit` check run sets against it. Later X9 units append their rows.

**Changes to existing rows.** Every row is kept by value. Where a lock inheritance row overrides a row, the effective description is the text judged here. Out-of-date descriptions are left for the next description-only successor, as earlier units left theirs.
- `crates/security/src/crash_matrix_support.rs`:
  - **What changed:** it gains X9 r4's three driver entries (`operation`, `recovery_admission` and `settlement_sweep`), the one-entry-per-process flag, and `publish_revocation`'s refusal after an entry.
  - **Description:** it says "never an authority type". That is out of date by omission of r4's three-entry exception.
- `crates/security/src/custody/namespace_lease.rs`:
  - **What changed:** `try_lock`, which X6c added, now takes its lock inside the `x2.lease.writer` / `x2.lease.readers` scope, as `lock` does (X9-2 judgment call; EXIT-PLAN), inside the same charged step. The carrier name is bound as `_name`, because without the feature `crash_scope!` is its block alone and compiles to nothing else.
  - **Description:** still true.
- `crates/security/src/custody/{recovery_admission,settlement_sweep,read_premise,installation_admission,installation_read_fixture}.rs`:
  - **What changed:** five crate-private items are widened to `pub(crate)` for the entries: `admit_on`, `allocate` and `RECOVERY_ALLOCATED`; `admit_on`; `produce_for`; `HomeSource`; `admitted_writer`.
  - **Descriptions:** still true.
- `crates/security/src/crash_matrix_sites.rs`:
  - **What changed:** the no-sleep pin names the matrix target and the run candidate, and the site list pins the matrix target's whole-file support guard.
  - **Description:** it lists the support and census sources, so it is out of date by omission of the matrix target.
- `crates/security/src/crash_matrix_support/post_state.rs`:
  - **What changed:** a BLOB column holding UTF-8 text is dumped as `blobText`, so item 7's normalizer reaches the drawn values inside JSON bodies. The object set is recorded by each name's shape, sorted, because content digests derived from the drawn ProjectId make its listing order a drawn permutation. Each object's bytes stay in `raw`.
  - **Description:** still true; it already says "lists the object sets".
- `crates/storage/Cargo.toml`:
  - **What changed:** the `[[test]] commit_tests` target with `required-features = ["crash-matrix"]` (law X9 r1 item 2).
  - **Description:** still true.
- `tools/check_crash_matrix.py`:
  - **What changed:** `check-unit` (law X9 r4 item 7) and limits L1 to L11 (r8).
  - **Description:** "the limits are exactly L1..L10" is now out of date, and the description omits `check-unit`.
- `tools/tests/test_check_crash_matrix.py`:
  - **What changed:** four `check-unit` tests and L11.
  - **Description:** still true.

**Order.** Its parent is the inventory the real product lock selects: inventory130 (unit X3d-3) at product cdd4589. The number 131 was assigned by the lead after 130 went to X3d-3. Succession is by the lock's parent pin, not by number. `evidence/build_v131.py`:
- reads the parent from the lock;
- checks each inheritance row against the lock before carrying it;
- writes only its two paths;
- refuses tracked paths, and refuses while a lock selects inventory131.

Reruns reproduce the same bytes.

**Projection.** The fifty-five effective description overrides the lock binds to inventory130 stay bound by stable file path: the sixteen carried from inventory81 onward and D1's thirty-nine, with D2's four supersessions already folded. Only the selectors after the inserted row move, by one. No contract successor bound at a2c5e8b names inventory130 as a supersession parent, so nothing new is folded (`supersessionsFolded: 0`).

- `verify_projection.py` is inventory130's helper, with its comment updated for this parent. It runs against the real lock at cdd4589: PASS, 55 rows, 278 corruptions refused.
- `evidence/verify_scratch.py` appends inventory131 in memory over the X9-2 worktree's lock. It replaces the inheritance rows with the record's fifty-five, and supplies a synthetic review and assent.
