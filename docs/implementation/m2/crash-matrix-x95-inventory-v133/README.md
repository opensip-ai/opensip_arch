# Crash-matrix X9-5 inventory133

Adds exactly two files to inventory131 (unit X9-2, selected at product b999ae3 and still at eb0d503, where X9-3 landed with no inventory successor; D1's thirty-nine overrides and D2's four supersessions are already folded into its fifty-five inheritance rows):
- crates/host/tests/commit_matrix_tests.rs
- crates/host/tests/fixtures/crash-matrix/required-runs.v1.json

It keeps all 965 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 967 planned files.

The rows belong to unit X9-5 (law X9 r15 item 12's X9-5 line, with r10's host target, runners, `candidate` child and separate required-runs file, r11's three-run host census, and r13's host rulings; r14 and r15 change nothing of X9-5's).

- **commit_matrix_tests.rs (test).** The crash matrix's host target.
  - **Gate:** built only with an explicit `--features crash-matrix` (`required-features` in host's manifest) and whole-file under the support predicate (law X9 r1 item 2).
  - **Children:** this binary re-executed by X9-0's driver under the scripted wall clock: fixture; `candidate` (r10's host order: one operation entry, `CommitSession::open`, X3d-3's candidate and r12's distinct variant written to disk with the session's core closure, then the session's refused end); `finalize` (host's `finalize_commit` runner); `store-gc` (host's `store_gc` runner); `recover`; and a publisher that revokes the session's core closure under the installation fence.
  - **Parent:** runs each reviewed host row's script by blocking record reads, records r12's timing guard on the monotonic clock where a script arms the observer tick, captures the post state, runs item 8's ladder, and writes one run record per run and the run set's `matrix.json` with r11's host census. Nothing sleeps, polls or waits on a timer.
- **required-runs.v1.json (fixture).** Host's reviewed required runs, in the shape `opensip.x9.required-runs.v1`, with storage's `clockEpoch` 1791072000 (law X9 r10: a file separate from storage's, holding X9-5's rows only).
  - **Rows:** 94: F01 4, F12 2, F16 1, F17 1, F32 76, F39 1, F40 3, F53 6.
  - **Sources:** transcribed from law X9 r15 before any lead run. F32's kill points and their crash-table windows come from the unarmed host census's exhausted-carrier run; every expected value comes from the law's row or the owning law's outcome it names, and is never read back from a run.
  - **Readers:** the host target, `tools/check_crash_matrix.py check-unit --unit X9-5`, and X9-6's `check` beside storage's file.

**Changes to existing rows.** Every row is kept by value. Out-of-date descriptions are left for the next description-only successor, as earlier units left theirs.
- `crates/host/src/crash_matrix_support.rs`:
  - **What changed:** it gains r10's two runners, `finalize_commit` and `store_gc` (each the process's one entry, returning value reports only), the run candidate file's writer and reader (`opensip.x9.run-candidate.v1`), and the fixed delivery phase's renderer.
  - **Description:** "item 6's synthetic run candidate … joins it with X9-5" and "Nothing here returns an authority type" stay true. It is out of date by omission of the two runners and the candidate file.
- `crates/host/Cargo.toml`:
  - **What changed:** the `[[test]] commit_matrix_tests` target with `required-features = ["crash-matrix"]`.
  - **Description:** still true.
- `crates/security/src/crash_matrix_sites.rs`:
  - **What changed:** the site pin names host's matrix target's whole-file support guard; the no-sleep pin covers the host target and admits its one `GuardClock` line, now counted per file.
  - **Description:** it lists the support and census sources, so it is out of date by omission of the host target, as it was for storage's.

**No new edge.** Host's matrix target calls host's support module, storage (`recover`, `NamespaceSweep`), security (`CommitSession`, `RecoveryRequest`, `SessionEnd`), identity and platform (X9-0's driver and barrier API). Each goes along an edge the parent already declares from opensip-host. The builder asserts them.

**Order.** Its parent is the inventory the real product lock selects: inventory131 (unit X9-2) at product eb0d503. The number 132 was assigned to X9-3, which landed with no successor, so 132 is unused. Succession is by the lock's parent pin, not by number. `evidence/build_v133.py`:
- reads the parent from the lock;
- checks each inheritance row against the lock before carrying it;
- writes only its two paths;
- refuses tracked paths, and refuses while a lock selects inventory133.

Reruns reproduce the same bytes.

**Projection.** The fifty-five effective description overrides the lock binds to inventory131 stay bound by stable file path: the sixteen carried from inventory81 onward and D1's thirty-nine, with D2's four supersessions already folded. Only the selectors after the inserted rows move. No contract successor bound at eb0d503 names inventory131 as a supersession parent, so nothing new is folded.

- `verify_projection.py` is inventory131's helper, with its comment updated for this parent. It runs against the real lock at eb0d503: PASS, 55 rows, 278 corruptions refused.
- `evidence/verify_scratch.py` appends inventory133 in memory over the X9-5 worktree's lock. It replaces the inheritance rows with the record's fifty-five, and supplies a synthetic review and assent.
