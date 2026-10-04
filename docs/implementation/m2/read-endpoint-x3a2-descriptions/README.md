# X3a-2 description successor

2026-10-04. Claude Opus 5.5, implementation lead. Law X3a r5 item 8 gives unit X3a-2 "description overrides for the changed host and storage readers, including `installation_lineage.rs`, whose description owner §9 requires to stop promising per-node markers". This contract successor carries those overrides. It changes descriptions only: no schema, registry, generated code, inventory or product file.

## Mechanism

One record, `successor.json`. Its only parent is `repository-file-inventory.v136.json`, the unit's own inventory candidate (`read-endpoint-x3a2-inventory-v136`), built on inventory135, which the product lock selects at `3f6f9a5`. Once the lock binds inventory136 and then this record, every entry is on the final selected inventory, so verify_design checks it and projects nothing.

It uses D1's form only: three `passageOverrides` on plain rows. A plain row has no `inventoryPassageInheritance` entry, and its `before` is the row's raw inventory136 description. `evidence/build_descriptions.py` refuses an inherited row, a `before` that is not the raw text, an empty, unchanged or multi-line `after`, and a duplicated path.

## Rows

Each new text was written against the reader as unit X3a-2 leaves it (product `3f6f9a5` plus the X3a-2 diff). The exact before and after text is in `evidence/descriptions.json` and in `successor.json`.

| v136 | File | What was false |
|---|---|---|
| 122 | `crates/host/src/installation_records.rs` | "S equality is not full S/G/K ... admission" described a bundle that checked only S equality between two captures. The bundle's pair and marker now come from the session's admitted endpoint, whose admission checked S, G, K, the chain, the core and `C.store`. |
| 123 | `crates/host/src/installation_selection.rs` | "provisional selection capture" and "Does not admit a selected store": the pair is no longer captured here. It is the session's one read, taken through the session's endpoint admission. |
| 747 | `crates/storage/src/store_root/native_marker.rs` | "on the original native-fenced descendant capture": the marker is no longer captured. It is the endpoint marker of the session's one read, bound to the requested S. |

## Rows not changed

- **`crates/host/src/installation_lineage.rs` (v136 row 121, inherited).** Its effective meaning is the inherited override carried from inventory81 onward and projected at inventory136: "Retain the selected pair, every immutable lineage node and the physically opened selected endpoint store marker under the ordinary binding owner. Admit complete node ancestry without requiring reclaimed intermediate physical stores; recheck all contributing original descriptors and latch failures under one operation budget. ..." It no longer promises per-node markers, which is owner §9's requirement, and it describes the adopted reader (M2-COMPLETE-r3 §3.3: "The description half is already true through an inherited override"). No supersession is needed.
- **The new rows** (`installation_endpoint.rs`, `installation_endpoint_tests.rs`) are written by inventory136 itself.
- **Rows that stay true but understate X3a-2's additions:** `installation_read.rs` (inherited; gains `required_filesystem`), `installation_read_tests.rs` (gains the extended source pin), `store_endpoint.rs` (gains a `selection` accessor), `installation_observation.rs` (inherited; its error constructor becomes crate-visible) and security's `lib.rs` (declares the new module). As in X3a-1's inventory83, they are carried unchanged and left to the next description batch. Item 8 names only the changed readers.
