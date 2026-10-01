# Evidence object publication and prepared commit inventory102

Adds exactly two sources to inventory99 (unit X2b-2, selected at product 66bdd05):
- crates/storage/src/ledger_store/project_commit.rs
- crates/storage/src/ledger_store/project_commit_tests.rs

It keeps all 774 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 776 planned files. No crate or dependency edge is added: storage already depends on security, platform and identity. The rows are unit X3c-2, law X3c r7 items 4 to 7 and 9 to 11, and item 12a's X3c-2 cases.

- **project_commit.rs (store).** project_ledger.rs's child module `commit`, so the existing ledger types and private stagers stay private. It holds object publication over blob_store, the non-waiting level-3 `PreparedLedger`, staging, the `PreparedLedgerCommit` adapter whose one consuming method performs only `COMMIT`, and the durability classification of that `COMMIT`.
- **project_commit_tests.rs (test).** The X3c-2 cases of item 12a on X3c-1's scratch location.

**Changes to existing rows.**
- `ledger_store/project_ledger.rs`:
  - declares the `commit` child module;
  - `admit_attempt` returns an `AdmittedAttempt` (not Clone), which object publication requires;
  - gains three refusals: `ObjectDeclaration` and `StagingMismatch` on the invariant row, and `CommitUndetermined` on the durability row.

  Its description (since inventory94) ends "No object publication, staging, commit, settlement or read-back." That is still true of the file's own code but now stale for the module, whose child holds publication, staging and commit. An inventory successor carries rows by value, so a later description-only contract successor must refresh it, as for 461b and carrier_floor.rs (inventory97).
- `ledger_store/recovery_material.rs` gains `WriteTransaction::stage_run_material`: the run-material insert, with the same schema check and the same body admission recovery uses. Its description ("Read and join immutable manifest and receipt-inventory material from the recovery ledger snapshot") now understates the file in the same way, and goes to the same description-only successor.
- `ledger_store/project_ledger_tests.rs` shares its fixture with the child's tests (`pub(super)`). The fixture now sits under the per-process scratch parent, F3's `<temp>/opensip-test/<pid>-<nanos>`, rather than directly in the temp directory. Its description stays true.
- `blob_store.rs` widens its private types to `pub(crate)`, and gains a `cfg(test)` byte accessor. Its description stays true.
- `lib.rs` gains a `cfg(test)` `test_scratch` module (F3's per-process scratch parent for storage). Its description stays true.

No other existing source changes.

**Order.** This successor replaces inventory100 (the same two rows on inventory97), which was committed but never reviewed; inventory100 is left unchanged and is never selected. Its parent is the inventory the real product lock selects, inventory99. evidence/build_v102.py reads the parent from the lock and maps it to the successor record that bound its sixteen rows. If X3b-2's inventory101 integrates first, it gets a parent-only rebuild with one more map entry. It refuses to write over any path git already tracks, and while a lock selects inventory102.

**Projection.** The sixteen effective description overrides bound to inventory99 (carried unchanged from inventory97 back to inventory81) stay bound by stable file path, with parent inventory99. verify_projection.py is inventory99's helper with only its comment corrected. It runs against the real lock at 66bdd05, which selects inventory99. evidence/verify_scratch.py appends inventory102 in memory over the real lock, with a synthetic review and assent.
