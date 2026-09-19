# Independent review — frozen `pin-transactions-checkpoint-185`

Reviewer: Claude (independent; Codex remains owner). Date 2026-09-19. Review dir: this directory only.
Scope: exactly the frozen 185 product bytes — the private transactional pin projection and `pin_change_facts` history. Staged result, not a receipt. No host lease/custody/authority, semantic Fact/View, creator/import/restore, M2, cumulative or product acceptance.

## 1. Identity verified

| Item | Result |
|---|---|
| `subject.tar.xz` | SHA-256 `2d8a7e920682e5466612b1a6337ddf62c08bb5f94423d54091ca31f023ac9dac`, 4,242,168 B = request = `archive-pin.json` |
| Members | 427, all regular/safe, verified from the tar before extraction; re-verified at end |
| Product pins | 351/351; none unpinned |
| Parent | equals **my own verified 184 extraction**; 348 unchanged; changed `ledger_store.rs` (error variant + `mod`), `recovery_pins.rs` (reader body moved to a shared `load_connection`); added `pin_transactions.rs`; fixtures unchanged. `62c03189e0d1d102…` ledger_store/pin_transactions.rs;`906f7ad1c34a671e…` ledger_store.rs;`8e9dc33eef5f25a7…` ledger_store/recovery_pins.rs |
| Host receipt 117 | 231 sources equal pins; none failed |

## 2. Owner checks re-run

Fresh scratch copy byte-equal to the product: **73 storage tests pass; strict workspace Clippy exit 0**.

## 3. What I read

All 176 production lines of `pin_transactions.rs`, its 12 tests, the two deltas, and the pre-existing `paired_run`, `WriteTransaction::commit`/`Drop`. Design as read: inside the caller's `BEGIN IMMEDIATE` transaction — receipt-joined Run (`ContinueCarrier` standing required) → both inventories must name that Run → operation grammar → exact history schema → operation not already used in this store+namespace → complete stored set read through the *same* bounded, schema-checked reader as recovery → equality with the caller's expected set → 174 policy against the **stored** set → one fact per changed name → scoped delete (row count verified) and re-insert of the projection. `poisoned` is set before the work and cleared only on `Ok`; `commit` refuses a poisoned transaction; `Drop` rolls back.

## 4. My probe (`claude-out/probes/rust_probe.rs.txt` → `io/pins.txt`)

| # | Probe | Result |
|---|---|---|
| 2 | **Sequence oracle**: 400 committed stages of random create/release/kind-change over 8 adversarial names (NFC/NFD pair, embedded NUL, space, `/`, astral) | 383 changed, 17 noop, 804 facts = 804 rows; after every commit projection == desired, stage fact count == oracle diff, and **replaying all history from empty reproduces the projection with every `before_kind` chaining**: 0 violations |
| 3a | two stages in one txn, the second reuses the operation | second `OperationAlreadyUsed` (own uncommitted facts are visible); third → `transaction_poisoned`; commit refused; **nothing persisted, including the first, successful stage** |
| 3b/3c | two stages, distinct operations, one commit; staged release then drop | both persisted atomically; drop leaves state untouched |
| 3d | noop, noop again, then a real change, all with the **same** operation | all accepted — a noop does not consume the operation (consistent with "noop adds no history"; see N-1) |
| 4 | operation grammar | upper-case hex, 31/33 digits, `OP-`, non-ASCII, `g` → `InvalidOperation`; all-zero accepted |
| 5 | expected set has the right names but one wrong kind | `StaleInventory`; kind-only change writes exactly one fact (`baseline → other-authorized`) |
| 6 | foreign store / namespace / Run rows, and the same operation_ref already used in a **foreign namespace** | accepted (operation scope is store+namespace, as the PK says); all 3 foreign projection rows byte-identical afterwards |
| 7 | stored legacy 4100 → 4097 | `first_publication=true` → `Policy(Count)`; `false` → admitted (W-1) |
| 8 | second writer while a change is staged | `DatabaseBusy` in <1 s |
| 10 | expected inventory names a different Run with identical rows | `DifferentRun` |
| 1, 9 | immutable-history SQL | **F-1** |

Two probe runs failed on my side and are preserved (`rust_probe-r1-COMPILE-FAILED`, `-r2-ROWID-FAILED`): a borrowed temporary, and an `ORDER BY rowid` on a `WITHOUT ROWID` table — the second led to W-2.

## 5. Mutation (`claude-out/probes/mutation.{py,json,log}`; baseline green; none failed to compile)

14 mutants. **7 killed by the owner's tests** (schema check skipped; `first_publication` ignored; kind-only change writes no fact; before/after swapped; delete not scoped to the Run; poison cleared on failure; unbounded read limits).
**7 survive the owner's 73 tests:**

| Mutant | My probe | Assessment |
|---|---|---|
| expected compared by **names only** | detected (case 5) | real gap — the owner's stale test changes the name set, never only a kind |
| only `desired.run` checked | detected (case 10, added after the mutation run; before that neither suite saw it) | real gap |
| operation grammar accepts upper-case hex | detected (case 4) | real gap in the Rust check; note the DDL CHECK still refuses it (`ConstraintViolation`) — defence in depth works, but the typed `InvalidOperation` is lost and the transaction is poisoned instead |
| operation reuse checked **globally** | detected (case 6) | real gap — no owner test reuses an operation across namespaces |
| operation reuse checked **per Run** | **not detected by either suite** | real behavioural difference (same operation, same namespace, different Run); I could not cheaply build a second receipt-joined Run in one namespace. Untested residual |
| policy evaluated against the caller's expected set | not detected | **equivalent**: the preceding equality check makes `expected` and `actual` identical inputs to the policy |
| deleted-row count not verified | not detected | unreachable defensive check inside one transaction; not a gap |

## 6. Findings

### F-1 (medium) — `REPLACE` rewrites "immutable" history; the no-update/no-delete trigger pair does not make a table append-only
`pin_change_facts` is protected by `BEFORE UPDATE` and `BEFORE DELETE` triggers, and the README says "History is append-only". SQLite's REPLACE conflict resolution deletes the conflicting row **without firing delete triggers unless `recursive_triggers` is ON**, and it is OFF (measured `0`) on both a plain connection and the product's own configured writer connection. Measured on the product connection after a committed fact `(x: NULL → baseline)`:

| Statement | Result |
|---|---|
| `UPDATE`, `DELETE`, `INSERT … ON CONFLICT DO UPDATE` | refused, history unchanged |
| `INSERT OR REPLACE INTO pin_change_facts …` | **succeeded; fact rewritten** to `(repair-prerequisite → backup-export)` |
| `REPLACE INTO pin_change_facts …` | **succeeded; fact rewritten** to `(repair-prerequisite → NULL)` |

The exact-schema check passes before and after, because the schema is unchanged. The production path uses plain `INSERT`, so this is not reachable through `stage_pin_change` today; it is a hole in the *schema-level* guarantee the DDL exists to give, which is what would protect against a future in-crate writer or any other connection.
**It is systemic, not new:** the same two-trigger pattern guards `commit_receipts`, `commit_associations`, `evidence_availability` and `commit_run_material`; probe case 9 shows `REPLACE INTO commit_receipts SELECT * FROM commit_receipts` and the same for associations **succeed** on the product connection. I reviewed those tables in earlier checkpoints and did not test REPLACE; that was my miss.
Remedies measured in `claude-out/probes/replace_remedy.py` → `io/replace_remedy.txt`: (a) `PRAGMA recursive_triggers=ON` makes REPLACE fire the no-delete trigger — but it is per-connection, so it protects only connections that set it; (b) a schema-level `BEFORE INSERT … WHEN EXISTS(row with NEW's key) … RAISE(ABORT)` guard refuses both REPLACE forms on **any** connection and still admits fresh inserts. (b) is the architectural fix — it lives in the exact-schema-verified DDL rather than in connection state — and `configure()` can additionally set and read back (a). Apply to every protected table in one pass, with a REPLACE negative per table.

### W-1 (low) — `first_publication` is caller-asserted and only ever loosens
With a stored over-limit legacy set, `false` admits a reduction that `true` refuses. From an empty or in-limit stored set the flag changes nothing, so its reach is limited to legacy states, and the README lists policy input as owed to the host. Record next to the field that it is an *unverified assertion* and which owner must establish it; the mechanism cannot derive it (a legacy projection has no history to consult).

### W-2 (low-medium, design) — the history has no order
`pin_change_facts` is `WITHOUT ROWID` with key (store, namespace, operation_ref, pin_id) and no sequence or time member; `operation_ref` is opaque hex. My replay oracle works only because my probe issues monotonically increasing operation numbers. With real operation refs the table is a *set* of per-operation diffs: per-pin `before/after` values chain, but cannot order two operations that touch different pins, and cannot disambiguate a pin that returns to a previous kind. If any consumer is ever meant to reconstruct or audit the sequence of inventories — "immutable operational before/after facts" reads that way — the order has to be stored (a per-scope sequence assigned inside the same transaction) or explicitly declared out of scope and owned by the attempt/receipt that carries the operation_ref.

### T-1 — the five real test gaps in §5
Names-only expected comparison; `expected.run` unchecked; upper-case operation hex; operation reuse scope, in both directions (global and per-Run). The per-Run one is untested by both suites.

### N-1 — noops do not consume an operation
Same operation: noop, noop, then a real change — all accepted. Consistent with "noop adds no history" and harmless within this mechanism; but if an operation_ref is meant to be single-use at the attempt level, that uniqueness must come from the attempt-custody owner, not from this table.

### N-2 — upper-case and schema CHECKs agree with the Rust grammar
The DDL's `operation_ref`/`run_id`/kind CHECKs mirror the Rust checks (measured for the upper-case case). Encoding is safe here only because the opener is UTF-8-only (179/184); `length(CAST(pin_id AS BLOB))>0` is an encoding-dependent predicate, which is fine under that law and should cite it.

## 7. Claims checked and confirmed

Atomicity and whole-transaction poisoning including earlier successful stages; rollback on drop; Run taken from the actual receipt/association/attempt join inside the writer transaction; complete current set read under the shared bounded, schema-checked reader; expected-set equality on names **and kinds**; policy against the stored set with first-publication and legacy reduction as 174 defines them; noop writes nothing; duplicate operation refused within scope, including against the transaction's own uncommitted facts; exact history schema including triggers; foreign store/namespace/Run projection rows untouched; writer exclusivity with immediate busy.

## 8. Limits

Synthetic storage fixtures; bundled SQLite 3.53.2 for the product probe and system SQLite 3.51.0 for the remedy check. I did not build a second receipt-joined Run in one namespace (so the per-Run reuse mutant is unconfirmed by execution), did not rebuild the owner's 12 compiled mutants or host receipt 117, and did not test crash durability or sidecar custody.

## 9. Verdict (bounded)

**The transaction mechanism does what it claims on every sequence I could construct (400-step oracle, 0 violations), and poisoning/atomicity/scope hold. F-1 is a real and systemic hole in the schema-level immutability guarantee — REPLACE rewrites history on the product's own connection, here and in four older ledger tables — and should be closed at the schema level before any of these tables is relied on as immutable. W-2 needs an owner decision; T-1 lists five undetected faults.** No cumulative, M2 or product approval.
