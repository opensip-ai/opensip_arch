# Evidence ledger creation inventory94

Adds exactly three sources to inventory93 (unit X2b-1, selected at product 8452ab9):
- crates/security/src/store_custody.rs
- crates/storage/src/ledger_store/project_ledger.rs
- crates/storage/src/ledger_store/project_ledger_tests.rs

It keeps all 765 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 768 planned files. No crate or dependency edge is added: storage already depends on security. The rows are unit X3c-1, law X3c items 1 to 3, 9 and 10.

- store_custody.rs (service): security's store-data custody for storage, exported from security's lib.rs on macOS: 465 item 3's create-or-admit for a store directory, and the private exclusive create and judged open of one store file.
- project_ledger.rs (store): owner201's ledger and object spellings, directory create-or-admit, ledger creation and its whole-schema open, and durable attempt admission. It is a child module of ledger_store, so the existing DDL and transaction types stay private.
- project_ledger_tests.rs (test): the item 12a cases X3c-1 owns, on a scratch installation with a held test writer lease.

**Order.** This successor depends on inventory93 (X2b-1), which product 8452ab9 selects. It replaces the reviewed inventory89, which had parent inventory87, with the same three rows rebuilt on the current predecessor; inventory89 is left unchanged. evidence/build_v94.py rewrites only this unit's own inventory94 and successor record, and refuses while a lock selects inventory94.

**Changes to existing rows.** security/src/lib.rs gains the store_custody module and its re-export (alongside F3's test-scratch change already on main); storage's ledger_store.rs splits `configure` into `configure_engine` plus the journal-mode check (behaviour unchanged for existing ledgers) and declares the project_ledger module. Their descriptions stay true.

**Projection.** The sixteen effective description overrides bound to inventory93 (carried unchanged from inventory91, 87, 84, 83, 82 and 81) stay bound by stable file path, with parent inventory93. verify_projection.py is inventory93's helper with only its comment corrected, and runs against the real lock at 8452ab9, which selects inventory93. evidence/verify_scratch.py appends inventory94 in memory over the real lock, with a synthetic review and assent.
