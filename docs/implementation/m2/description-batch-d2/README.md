# Stale inherited inventory descriptions: contract successor D2

2026-10-01. Claude Opus 5.5, implementation lead. This is unit D2 of law VD1 r1 item 6. It is the follow-up to D1's "Deferred to VD1" rows. It changes descriptions only: no schema, registry, generated code, product file or inventory successor.

## Mechanism

D2 makes four `passageSupersessions` (law VD1 r1, verify_design at product 96dd114). Its only parent is `repository-file-inventory.v122.json`, which the product lock selects. Each supersession:
- selects the row's `/files/N/description` on v122;
- has `before` equal to the row's current effective text, which is the `after` of its one `inventoryPassageInheritance` entry;
- names, in `supersedes`, the meaning it ends. No row has an earlier supersession, so each names its root passage override.

| v122 | File | Superseded meaning (record, parent and selector) |
|---|---|---|
| 273 | crates/identity/src/store_lineage.rs | `existing-root-diagnostics-468a/successor.json`, v74 `/files/158/description` |
| 372 | crates/security/src/custody/installation_session.rs | `stale-descriptions-461b/successor.json`, v80 `/files/247/description` |
| 388 | crates/security/src/custody/read_premise.rs | `stale-descriptions-461b/successor.json`, v80 `/files/250/description` |
| 398 | crates/security/src/initial_installation.rs | `existing-root-diagnostics-468a/successor.json`, v74 `/files/242/description` |

**No D1-era link.** D1 made only direct overrides of plain rows on v119; `build_d1.py` refused inherited rows. Inventory122 carried D1's 39 meanings into the projection, which grew from 16 to 55 rows. None of those 39 is one of these four files. Each of the four rows has exactly one inheritance entry, and no row has an earlier supersession. `build_d2.py` asserts both, and it would name the chain tail if a supersession existed.

The supersessions are on the selected inventory, so verify_design checks them and does not project them. `inventoryPassageInheritance` stays at its 55 rows, unchanged.

## What was stale (product main 96dd114)

Each new description keeps every sentence of the old effective text that is still true, word for word. The one exception is `read_premise.rs`'s second sentence, which now says "The read receipt" instead of "The receipt", because there are now two receipts. The new descriptions add clauses for what the file now does.

- **`read_premise.rs`.** "Library only: no CLI command is wired" is false: `opensip doctor` (X10a) reaches the read receipt through doctor's installation check. The old text also omitted:
  - X1's typing by purpose: `PlatformReceipt<Read|Write>`, `produce_write_platform`, and the write receipt's `DurableBarrierQualification` lending;
  - the write receipt's later lendings: `bootstrap_source` (X4B-b), `charge` (X2e), `charge_guarded` (X4a), and the end-path settlement reserve and spend (X3d-1);
  - `selected_core` (X3a);
  - the invariant row for a foreign receipt;
  - its consumers: the ordinary writer's admission and the operation handoff.

  This supersedes X1b's text (`stale-descriptions-x1b/`), which was checked against f7acb6d.
- **`installation_session.rs`.** "Library only: no CLI command is wired" is false (`opensip doctor`). The old text also omitted:
  - X3a-1's additions to the one read: the core finding, the trust current record read once under its cap (the current-store finding), the generation-bound chain finding against the session limit's budget row, and the endpoint values a complete I keeps;
  - the second receipt recheck after step 4;
  - `retain` (458c-b2).
- **`store_lineage.rs`.** It omitted `SuppliedChain::into_nodes` (X3a-1), which the write gate's one read and the observation session use to keep the chain for the selected store endpoint.
- **`initial_installation.rs`.** It omitted three things:
  - that the same attempt also stands behind the read and write receipts;
  - the borrowed-scope and handoff rechecks (`recheck_actor_in`, `recheck_storage_in` and `recheck_handoff_storage`; law 467, and X4a's guard);
  - X3d-1's end-path settlement reserve: `reserve_end_path_settlement` and `settle_end_path`, the only production callers of `WorkLedger::reserve_settlement` and `settle`.

## After selection

Once D2 is selected, the next inventory successor must do two things:
- carry the four rows by value;
- fold each supersession into its row's inheritance entry (law VD1 item 3). The entry's `before` stays the raw text, and its `after` becomes D2's `after`.

The projection helper's row count stays at 55. That helper reads only `passageOverrides`, so it must also read `passageSupersessions` and fold them.

If another inventory is selected before D2, `build_d2.py` rebuilds D2 on it with no edit, because it finds rows by path. That rebuild needs a new review.

## Evidence

- **`evidence/descriptions.json`** holds each row's path, its exact current effective text (`before`) and its new text (`after`).
- **`evidence/build_d2.py`** rebuilds `successor.json` and `description-batch-d2-subject.json` deterministically from the lock-selected inventory and the lock's contract successors. It refuses on any of these:
  - a row without exactly one inheritance entry;
  - a `before` that is not the current meaning;
  - an ambiguous root;
  - an empty, unchanged or multi-line `after`;
  - a duplicate path.
- **`evidence/verify_scratch.py`** runs the product checkout's real verify_design over a scratch lock: the real lock with this binding appended, and a synthetic review and assent held in memory. It asserts:
  - the scratch lock passes;
  - 4 supersessions are checked;
  - the 55 inheritance rows and the selected inventory are unchanged;
  - every `before` is its row's current meaning.
