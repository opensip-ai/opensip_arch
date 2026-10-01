# Grant-journal append inventory101

Adds exactly two sources to inventory102 (unit X3c-2, selected at product 920941b):
- crates/security/src/journal_store/carrier_append.rs
- crates/security/src/journal_store/carrier_append_tests.rs

It keeps all 776 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 778 planned files. No crate or dependency edge is added: the module uses only `opensip-identity`, `opensip-platform` and `rusqlite`, which security already depends on. The rows are unit X3b-2: law X3b r6 items 5, 6, 8 and 9, and item 11's X3b-2 cases.

- **carrier_append.rs (composition).** carrier_floor.rs's macOS child module `append`, beside X3b-1b's `start`, so the carrier's private types stay private. It holds `JournalAppendLock` (level 4), the level-3 `JournalTransaction`, the held `JournalAppendHeld`, record building for `SEAL`, `REV`, `CLN`, `RA` and `TERMINAL`, the append protocol with the witness file protocol around the commit, the classification of each failure as certain or undetermined, and the latched reconciliation through X3b-1b's `reconcile_after_uncertain`.
- **carrier_append_tests.rs (test).** The X3b-2 cases of item 11 on X3b-1a's scratch fixture.

**Changes to existing rows.**
- `journal_store/carrier_floor.rs`:
  - declares the `append` child module;
  - `CarrierRow` gains `Invariant` (`SYSTEM.OUTCOME.ILLEGAL_STATE`, `host-invariant`, detail `HOST.INVARIANT_VIOLATED`, as X3d r3 item 9 and X3c r7 item 10 give a broken composition);
  - `CarrierRefusal` gains `Append(AppendRefusal)`, whose row is the append refusal's own.

  Its description (since inventory91) says "the public mapping, the carrier start's witness writes, the end step and the append are later units". The start and the end step moved to `start` at inventory97, and the append is now in `append`; the file's own code is unchanged in substance. An inventory successor carries rows by value, so the same later description-only contract successor that inventory97 and inventory102 named must refresh it.

No other existing source changes. `carrier_start.rs` is used unchanged (`CarrierStart::tail`, `reconcile_after_uncertain`).

**Order.** This successor's parent is the inventory the real product lock selects: inventory102 (unit X3c-2) at product 920941b. It was first built on inventory99 at 66bdd05; X3c-2 integrated first, so evidence/build_v101.py rebuilt it on inventory102 with the same two rows. The number 101 is lower than its parent's 102 because both were reserved while X2b-2 was in flight; succession is by the lock's parent pin, not by number, and verify_design accepts it (evidence/verify_scratch.py). The builder reads the parent from the lock, and maps inventory99 and inventory102 to the successor records that bound their sixteen rows. It refuses to write over any path git already tracks, and while a lock selects inventory101.

**Projection.** The sixteen effective description overrides bound to inventory102 (carried unchanged from inventory99 back to inventory81) stay bound by stable file path, with parent inventory102. verify_projection.py is inventory102's helper with only its comment corrected to name its parent. It runs against the real lock at 920941b, which selects inventory102. evidence/verify_scratch.py appends inventory101 in memory over the real lock, with a synthetic review and assent.
