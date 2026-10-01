# Evidence ledger creation inventory89

Adds exactly three sources to inventory84 (unit X2a, selected at product 8bfc78a):
- crates/security/src/store_custody.rs
- crates/storage/src/ledger_store/project_ledger.rs
- crates/storage/src/ledger_store/project_ledger_tests.rs

It keeps all 758 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 761 planned files. No crate or dependency edge is added: storage already depends on security. The rows are unit X3c-1, law X3c r6 items 1 to 3, 9 and 10.

- store_custody.rs (service): security's store-data custody for storage, exported from security's lib.rs on macOS: 465 item 3's create-or-admit for a store directory, and the private exclusive create and judged open of one store file.
- project_ledger.rs (store): owner201's ledger and object spellings, directory create-or-admit, ledger creation and its whole-schema open, and durable attempt admission. It is a child module of ledger_store, so the existing DDL and transaction types stay private.
- project_ledger_tests.rs (test): the item 12a cases X3c-1 owns, on a scratch installation with a held test writer lease.

**Numbering.** 89 is reserved for X3c-1. Inventories 85 (X3b-1a), 87 (X4T-0) and 88 (X2b) are other units in flight and 86 is reserved; this successor is rebuilt on the real predecessor at integration. evidence/build_v89.py refuses to write over any path git already tracks.

**Changes to existing rows.** security/src/lib.rs gains the store_custody module and its re-export; storage's ledger_store.rs splits `configure` into `configure_engine` plus the journal-mode check (behaviour unchanged for existing ledgers) and declares the project_ledger module. Their descriptions stay true.

**Projection.** The sixteen effective description overrides bound to inventory84 (carried unchanged from inventory83, 82 and 81) stay bound by stable file path, with parent inventory84. verify_projection.py is inventory84's helper with only its comment corrected, and runs against the real lock at 8bfc78a, which selects inventory84. evidence/verify_scratch.py appends inventory89 in memory over the real lock, with a synthetic review and assent.
