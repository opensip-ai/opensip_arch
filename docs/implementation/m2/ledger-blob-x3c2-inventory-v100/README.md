# Evidence object publication and prepared commit inventory100

Adds exactly two sources to inventory97 (unit X3b-1b, selected at product 46b1d60):
- crates/storage/src/ledger_store/project_commit.rs
- crates/storage/src/ledger_store/project_commit_tests.rs

It keeps all 772 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 774 planned files. No crate or dependency edge is added: storage already depends on security, platform and identity. The rows are unit X3c-2, law X3c r7 items 4 to 7 and 9 to 11, and item 12a's X3c-2 cases.

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

**Order.** This successor's parent is the inventory the real product lock selects: inventory97 now. X2b-2's inventory99 is also built on inventory97. If X2b-2 integrates first, evidence/build_v100.py rebuilds inventory100 on inventory99 unchanged. It reads the parent from the lock, and maps inventory97 and inventory99 to the successor records that bound their sixteen rows. It refuses to write over any path git already tracks, and while a lock selects inventory100.

**Projection.** The sixteen effective description overrides bound to inventory97 (carried unchanged from inventory96 back to inventory81) stay bound by stable file path, with parent inventory97. verify_projection.py is byte-identical to inventory99's helper, which is inventory97's with its comment corrected. It runs against the real lock at 46b1d60, which selects inventory97. evidence/verify_scratch.py appends inventory100 in memory over the real lock, with a synthetic review and assent.
