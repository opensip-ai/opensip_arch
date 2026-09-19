# Proposal assistance — 187: inventory of immutable tables, REPLACE exposure, guard design, and the W-2 owner choice

Reviewer: Claude. 2026-09-19. **Assistance only** — read-only inventory and scratch probes; not a frozen review, not acceptance, no approval of any 186/187 draft (none inspected). No source, candidate or repository file was edited.
Subject of the inventory: my verified 185 product tree (`claude-pins185-20260919-r1/…/product`), production code only (everything before `#[cfg(test)]`) in `crates/storage` and `crates/security`.
Evidence: `claude-out/inventory.py` → `inventory.txt`, `inventory.json`; `guard_design.py` → `guard_design.txt`; `production-dml.txt`. **Two of my own runs were wrong and are preserved**: `inventory-r1-CONTAMINATED.*` (I reused one database across verbs, so later verbs saw rows my own cleanup had changed — it even "showed" `INSERT OR IGNORE` rewriting rows) and `guard_design-r1-FAILED.txt` (an attribute my Python lacks). r2 builds a fresh database per (connection setting, verb).

## 0. Headline

- **13 tables** are defined by production DDL (7 storage, 6 security across three carrier formats). **8 are vulnerable** to REPLACE rewriting an existing row on a default connection; **2 are already protected** — by exactly the kind of BEFORE INSERT law you propose; **3 have no triggers at all** and cannot be given any without a format change.
- **No production caller uses `INSERT OR IGNORE`, `INSERT OR REPLACE`, `REPLACE` or `ON CONFLICT`.** All eight production writes are plain `INSERT` (plus one scoped `DELETE` on the mutable projection). A duplicate-key guard breaks nothing in production.
- **A guard on the primary key alone is not enough** (measured): REPLACE resolves a conflict on *any* uniqueness constraint by deleting the conflicting row, so a new primary key that collides on a secondary `UNIQUE` still destroys a historical row. `commit_associations` has two such constraints.
- **No production code creates any of these tables** — every `execute_batch(…DDL)` in production targets an in-memory expectation connection. So for the storage tables the DDL can still be corrected in place rather than migrated, the same standing the attempt-custody DDL correction already relied on.

## 1. Method

Structural: each production raw-string DDL block is instantiated in memory; tables, primary keys, other unique indexes, `WITHOUT ROWID`, and triggers (timing/event) are read back from SQLite. Empirical: for each table a *relaxed twin* (same columns, same keys and uniqueness constraints, the **real** trigger SQL, CHECK/NOT NULL dropped so a synthetic row can be seeded) receives `REPLACE`, `INSERT OR REPLACE` and `INSERT OR IGNORE` of a row with the same key and a changed non-key column, on a default connection and with `recursive_triggers=ON`. The REPLACE/trigger interaction does not depend on CHECKs. For the storage tables this agrees with what I measured on the **real** product connection and rows in the 185 review (cases 1 and 9).

## 2. Inventory

| # | Table (DDL const, file) | Key / other unique | Triggers today | REPLACE on a default connection | With `recursive_triggers=ON` | Immutable by contract? |
|---|---|---|---|---|---|---|
| 1 | `commit_receipts` (`PAIR_DDL`, ledger_store.rs) | PK (store_digest, namespace, execution) | BEFORE UPDATE, BEFORE DELETE | **row rewritten** | refused | yes |
| 2 | `commit_associations` (`PAIR_DDL`) | same PK; **UNIQUE (carrier_digest, grant_generation, journal_seq)**; **UNIQUE (store_digest, namespace, commit_sequence)** | BEFORE UPDATE, BEFORE DELETE | **row rewritten** | refused | yes |
| 3 | `attempt_custody` (`ATTEMPT_DDL`) | PK (store_generation_digest, namespace_id, execution_id) | `ac_monotone` BEFORE UPDATE (only admitted→settled), BEFORE DELETE | **row rewritten** | refused | append-and-settle; identity and a settled row immutable |
| 4 | `evidence_availability` (`AVAILABILITY_DDL`) | PK (store_digest, namespace, run_id, generation) | BEFORE UPDATE, BEFORE DELETE | **row rewritten** | refused | yes |
| 5 | `commit_run_material` (recovery_material.rs) | PK (store_digest, namespace, execution) | BEFORE UPDATE, BEFORE DELETE | **row rewritten** | refused | yes |
| 6 | `pin_change_facts` (pin_transactions.rs) | PK (store_digest, namespace, operation_ref, pin_id) | BEFORE UPDATE, BEFORE DELETE | **row rewritten** | refused | yes |
| 7 | `active_run_pins` (recovery_pins.rs) | PK (store_digest, namespace, run_id, pin_id) | none | rewritten | rewritten | **no — current projection, mutable by design** |
| 8 | `carrier_format` (`CURRENT_CARRIER_DDL`, journal_store.rs) | PK (singleton) | BEFORE UPDATE, BEFORE DELETE | **row rewritten** | refused | yes ("carrier format binding is immutable") |
| 9 | `grant_journal_v3` (`CURRENT_CARRIER_DDL`) | PK (grantGeneration, seq) | BEFORE UPDATE, BEFORE DELETE, **BEFORE INSERT `gj3_append_laws`** | **refused by the existing law**: `NEW.seq` must equal tail+1, so no existing (generation, seq) can be re-inserted | refused | yes |
| 10 | `grant_journal` format 2 (`DDL2`, inherited_schema.rs) | PK (grantGeneration, seq) | + **BEFORE INSERT `gj_seq_contiguous`** | **refused** (same tail+1 law; measured "grant journal sequence must be tail+1") | refused | yes |
| 11 | `grant_journal` format 1 (`DDL1`) | PK (grantGeneration, seq) | BEFORE UPDATE, BEFORE DELETE only | **row rewritten** | refused | yes — but inherited |
| 12 | `carrier_quarantine` (all three formats) | INTEGER PRIMARY KEY grantGeneration | **none** | rewritten | **rewritten** (no delete trigger to fire) | "external, non-appending" marker |
| 13 | `carrier_capacity_pause` (all three formats) | INTEGER PRIMARY KEY grantGeneration | **none** | rewritten | **rewritten** | proven-tail marker |

Notes that change what 187 can do:

- **Rows 9–10 are precedent, not exposure.** The journal's own append law is a BEFORE INSERT guard and it already defeats REPLACE on any connection. Your 187 choice extends an existing pattern of this codebase; say so in the change.
- **Row 3 is the most consequential.** `ac_monotone` makes `settled` final *for UPDATE*; REPLACE is not an UPDATE. I reproduced the shape (guard_design §C): UPDATE settled→admitted is refused, `REPLACE` of the same key with `admitted` succeeds. A settled-`committed` attempt can be returned to `admitted`, or to `refused` — exactly the unresolvable/false-noncommit states `commit-recovery-readonly` §4.2 exists to prevent. (Inferred from the measured mechanism on a twin with the real triggers; I did not run it against a real custody row.)
- **Rows 11–13 cannot be fixed by adding a trigger.** Format 1 is an inherited historical schema; the two side tables are shared by all three formats and the open dispatch requires their stored SQL to be **byte-equal to the frozen definition** (comment at journal_store.rs l.854–857), so any added trigger turns a lawful carrier into a refused one. For these, `recursive_triggers=ON` does nothing either (12–13 have no delete trigger). Their protection is custody plus reader validation, and 187 should say that explicitly rather than appear to cover "all immutable tables". The security crate has **no production DML at all** today (it is reader-only), so nothing in the product can exercise this yet.
- **Row 8** is format-3 DDL with a reference owner (`carrier-format.v3.md` / the reference carrier SQL). Guarding it is right but is a reference change first; it is a singleton, so the guard is simply "refuse any insert when a row exists".
- **Row 3's and rows 1–2/4–6's DDL** also have reference counterparts (`attempt-custody.schema.v1.json` carries the attempt DDL law). 187 is a product checkpoint; note which reference owners must follow.

## 3. Callers a duplicate guard could break

`claude-out/production-dml.txt` — every DML statement in production code of the whole workspace:

| Statement | Site |
|---|---|
| `INSERT INTO attempt_custody(...)` | ledger_store.rs:335 |
| `INSERT INTO commit_receipts` / `commit_associations` | ledger_store.rs:593, 597 |
| `INSERT INTO evidence_availability` | ledger_store.rs:742 |
| `INSERT INTO pin_change_facts` | pin_transactions.rs:113 |
| `DELETE FROM active_run_pins` / `INSERT INTO active_run_pins` | pin_transactions.rs:133, 141 (mutable projection; must **not** get a guard) |

There is **no** `INSERT OR IGNORE`, `INSERT OR REPLACE`, `REPLACE` or `ON CONFLICT` caller, lawful or otherwise, and no settle path other than the `UPDATE` that `ac_monotone` governs. Nothing idempotent relies on silent duplicate handling: a duplicate today fails with a constraint error, and with the guard it still fails.
What does change (guard_design §D): the failure becomes `RAISE(ABORT)` — same primary result code (`SQLITE_CONSTRAINT`, so rusqlite's `ConstraintViolation` is unchanged) but extended code `CONSTRAINT_TRIGGER` instead of `CONSTRAINT_PRIMARYKEY`, and your message instead of "UNIQUE constraint failed". No production code inspects extended codes or messages (grep: the only `ConstraintViolation` match is a test of deferred-FK commit failure, unaffected). Tests asserting on message text would need updating.
One behavioural point to decide deliberately: with the guard, `INSERT OR IGNORE` of a duplicate is **refused**, not ignored (measured). That is what you want for immutability, but it means a future "idempotent republish" must be written as read-compare-then-skip, never as `OR IGNORE`.

## 4. Guard design — measured pitfalls

1. **Cover every uniqueness constraint, not only the PK.** `guard_design §A`: with a PK-only guard, `REPLACE` of a *new* PK that collides on `UNIQUE(u1,u2)` succeeded and the historical row vanished. With the guard's `WHEN EXISTS` covering the PK **or** each UNIQUE tuple, both REPLACE forms and `INSERT OR IGNORE` are refused and a fresh insert is admitted (§B). For `commit_associations` that means three disjuncts. NULLs never conflict in SQLite UNIQUE, so nullable unique columns need no special case.
2. **It is connection-independent** (§E): refused with `recursive_triggers` explicitly OFF. That is the property that makes it the right layer; setting and reading back `recursive_triggers=ON` in `configure()` is still worth doing as a second line, but only protects connections that call `configure()`.
3. **Exact-schema checks must include the new trigger** — they already compare every `sqlite_schema` row for the table, so they will, but each check's negative set should gain "guard missing" (a schema without the guard must be refused, or the guarantee silently degrades to today's).
4. **Do not add a guard to `active_run_pins`** (row 7): delete-and-reinsert is its lawful update.
5. `WITHOUT ROWID` tables have no rowid to REPLACE on; the three rowid tables in the inventory are exactly rows 12–13 (and they are the unguardable ones).
6. A per-table REPLACE negative should run through the **product's own configured connection** on a real row, as my 185 case 9 did, not only on a plain connection.

## 5. W-2 owner choice — "an unordered per-operation diff set, not a replay sequence; order and attempt linkage belong to the host receipt owner; never inferred from op hex"

**I agree with the choice; it is the honest reading of the table as built.** Conditions that make it coherent rather than merely a relabel:

1. **Stop calling it history in a way that implies replay.** README/module docs currently say "immutable operational before/after facts" and "History is append-only"; add that the set is unordered across operations and that the current projection is **not derivable** from it. My 185 replay oracle succeeded only because my operation numbers were monotonic — that test should not be copied as a product invariant.
2. **State the consequence for repair:** since the projection cannot be rebuilt from facts, `active_run_pins` is the sole authority for the current set, and a damaged projection is a custody loss, not something the facts can heal. (That matches "not retained-closure proof" but should be said next to the table.)
3. **What remains checkable, and is worth a test:** within one operation the facts are a well-formed diff (one row per changed pin; `before ≠ after`; not both NULL — already CHECKed). Across operations nothing is promised — in particular a pin's `before_kind` need not equal any other operation's `after_kind` from the table's point of view, because legacy projections have no facts at all.
4. **Make "not inferred from op hex" executable:** a regression with two committed operations whose hex order is the reverse of their commit order, asserting nothing in the mechanism (duplicate check, stage result, reader) depends on the order. Today nothing does; the test pins it.
5. **Linkage stays owed, so say what is *not* checked:** `stage_pin_change` verifies the operation's grammar and non-reuse in scope, not that the operation exists in `attempt_custody` or belongs to any receipt. A fact can therefore name an operation the ledger has never seen. That is acceptable under this choice only because the facts carry no authority; the future receipt owner must perform the join.
6. My 185 N-1 stands under this choice: a noop leaves no trace, so single-use of an operation_ref is not enforceable here and must come from the attempt owner.

## 6. Suggested 187 regression list (beyond those you named)

Per protected table: REPLACE and INSERT OR REPLACE of an existing key on the product connection → refused, bytes unchanged; `commit_associations`: new PK colliding on each secondary UNIQUE → refused; `attempt_custody`: REPLACE settled→admitted and settled-committed→settled-refused → refused; exact-schema check refuses a table missing its guard; `active_run_pins` still accepts the delete/reinsert path; duplicate plain INSERT still reports `ConstraintViolation`; `INSERT OR IGNORE` duplicate is refused; reversed-hex-order operations (§5.4).

## 7. Limits

Production code of two crates in one verified tree; test modules and reference SQL files were not inventoried (the reference carrier DDL and `attempt-custody.schema.v1.json` DDL law are named as owners to follow, not analysed). Empirical REPLACE results for rows 3, 4, 5, 8, 11–13 are on relaxed twins with the real triggers (system SQLite 3.51.0); rows 1, 2, 6 were additionally confirmed on the real product connection in my 185 review. `grant_journal_v3` could not be seeded past its own append law in a twin, so its "refused" is structural (the tail+1 condition) plus the identical law measured on format 2. No approval of any draft is implied.
