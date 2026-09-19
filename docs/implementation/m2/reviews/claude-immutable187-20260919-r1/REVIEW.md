# Independent review — frozen `immutable-ledger-checkpoint-187`

Reviewer: Claude (independent; Codex remains owner). Date 2026-09-19. Review dir: this directory only (my 185 probe output is read, not written).
Scope: exactly the frozen 187 product bytes — duplicate-key BEFORE INSERT guards on six storage tables, the 185 T-1 regressions and the W-1/W-2 clarifications. My 187 inventory was assistance, not acceptance. `carrier_format`, historical carrier formats and the marker tables are expressly **not** claimed fixed and are not reviewed as such. No creator/upgrade, host, custody, formal-selection or cumulative approval.

## 1. Identity verified

| Item | Result |
|---|---|
| `subject.tar.xz` | SHA-256 `7f3bcf6ed2ae66d459a4875742a14fc9950e519535a5250d4e34ddb03cdbd1e5`, 4,244,992 B = request = `archive-pin.json` |
| Members | 428, all regular/safe, verified from the tar before extraction; re-verified at end |
| Product pins | 352/352; none unpinned |
| Parent | equals **my own verified 185 extraction**; 348 unchanged; modified `ledger_store.rs` (`69a57e4b2ed05642…`), `pin_transactions.rs` (`773a808e0b8a88cf…`), `recovery_material.rs` (`b90840aa36be0190…`); added test-only `immutable_guards.rs` (`f9237340f6d40a94…`, `#[cfg(test)] mod`); fixtures unchanged |
| Host receipt 118 | 232 sources equal pins; none failed |

## 2. Owner checks re-run

Fresh scratch copy byte-equal to the product: **80 storage tests pass; strict workspace Clippy exit 0**.

## 3. The guards, as read

Six `BEFORE INSERT … WHEN EXISTS(SELECT 1 FROM <t> WHERE <key>=NEW.<key>…) BEGIN SELECT RAISE(ABORT,'retained key cannot be replaced'); END;` triggers, one per protected table, each inside the DDL constant that the table's exact-schema check instantiates — so the guard is part of the admitted schema, not connection state.

| Table | Guard key(s) | Matches the table's uniqueness constraints? |
|---|---|---|
| `attempt_custody` | (store_generation_digest, namespace_id, execution_id) | yes (PK) |
| `commit_receipts` | (store_digest, namespace, execution) | yes (PK) |
| `commit_associations` | PK **OR** (store_digest, namespace, commit_sequence) **OR** (carrier_digest, grant_generation, journal_seq) | yes — all three; every key column is `NOT NULL` |
| `evidence_availability` | (store_digest, namespace, run_id, generation) | yes (PK) |
| `commit_run_material` | (store_digest, namespace, execution) | yes (PK) |
| `pin_change_facts` | (store_digest, namespace, operation_ref, pin_id) | yes (PK) |

`active_run_pins` has no guard (correct: delete-and-reinsert is its update path). Production DML is unchanged — still plain `INSERT`.

## 4. My probes

**Adverse SQL on real rows** (`claude-out/probes/guards_probe.rs.txt` → `io/guards.txt`), on the product-configured writer connection **and** a plain connection, `recursive_triggers = 0` measured on both:

| # | Probe | Result (identical on both connections) |
|---|---|---|
| 1 | each of the six tables × `REPLACE`, `INSERT OR REPLACE`, `INSERT OR IGNORE`, plain `INSERT` of an existing row | all 24 refused, `ConstraintViolation` / extended **1811** (`CONSTRAINT_TRIGGER`); table bytes unchanged |
| 2 | `commit_associations`: **new** primary key colliding on (store, namespace, commit_sequence); on (carrier, generation, seq); carrier key with generation/seq presented as **TEXT**, as **REAL**; commit_sequence presented as **INTEGER** | all refused **by the guard** (extended 1811, message "retained key cannot be replaced" — not by a CHECK); original row still present. Control with three fresh keys: accepted |
| 3 | `attempt_custody`: lawfully settled, then `REPLACE` to `admitted`, and to `settled/refused` | refused; row still `settled/committed` |
| 4 | a refused REPLACE inside an open transaction after an earlier lawful insert | statement refused, transaction still open, earlier insert persists after COMMIT — `RAISE(ABORT)` is statement-level, as it should be |
| 5 | receipts guard dropped from an otherwise exact ledger | recovery read refuses `Configuration("receipt_association_schema")` — a guard-less schema is not admitted |

Row 2 mattered to me specifically: a BEFORE INSERT trigger sees `NEW` values, and I wanted to know whether a key presented with a different storage class could slip past the guard's `=` while still colliding in the unique index after column affinity. It cannot here — SQLite's comparison affinity makes the guard's equality agree with the index in every variant I tried, and the refusal is attributable to the trigger by its extended code.

**Regression of everything else** — my 185 probe run **verbatim** on 187 (`probes/rust_probe185-verbatim.rs.txt` → `io/pins.txt`), diffed against my stored 185 output: the *only* differing lines are the six REPLACE lines, which change from "SUCCEEDED / history CHANGED" to "refused / unchanged". The 400-step sequence oracle (0 violations), poisoning, scope isolation, operation grammar, first-publication and writer-exclusivity lines are byte-identical. So original scope and atomicity are untouched and **185 F-1 is closed for these six tables**.

## 5. Mutation (`claude-out/probes/mutation.{py,json,log}`, `mutation_receipts.py`)

Baseline green; none failed to compile. One mutant's anchor was wrong in my first script (recorded there as HARNESS-ERROR and preserved); re-run separately with a correct, segment-confined edit.
**14/14 killed by the owner's tests:**
- my five real 185 T-1 survivors — names-only expected comparison, `expected.run` unchecked, upper-case operation hex, operation reuse global, operation reuse **per Run** (the one neither suite could see in 185; now killed by `operation_reuse_is_namespace_wide_across_distinct_receipt_joined_runs`, which builds two real receipt-joined Runs);
- guards too **narrow**: associations without the carrier key; without the commit_sequence key; attempt guard ignoring namespace;
- guards too **broad** (would refuse lawful appends): availability ignoring `generation`; receipts ignoring `execution`; pin facts ignoring `pin_id`;
- wrong trigger semantics: `RAISE(IGNORE)` on pin facts and on run material (silent skip instead of refusal); receipts guard as `AFTER INSERT`.
Both directions being covered is what I most wanted to see: a guard that is too broad fails just as surely as one that is too narrow, only later and in production.

## 6. Findings

No finding against the change. Notes:

### N-1 — duplicate semantics changed, deliberately; record it where a future writer will look
A plain duplicate `INSERT` still reports `ConstraintViolation`, but with extended code 1811 and the guard's message instead of 1555 / "UNIQUE constraint failed". `INSERT OR IGNORE` of an existing key is now **refused**, not ignored. Nothing in production depends on either (all writes are plain `INSERT`; no code inspects extended codes — re-checked). An idempotent republish, if ever wanted, must be read-compare-skip. The README says this; a one-line comment beside the DDL would reach the person who needs it.

### N-2 — what the guard does not defend, stated accurately by the owner
A connection with schema access can `DROP TRIGGER`, rewrite and re-create; the exact-schema check sees only the end state. That is custody, not schema, and the README disclaims it ("does not … eliminate arbitrary schema/file replacement by an actor outside custody"). Agreed and not counted against this checkpoint.

### N-3 — scope is six of the thirteen tables, as claimed
`carrier_format` (reference 188 first), format-1 `grant_journal`, `carrier_quarantine` and `carrier_capacity_pause` remain as in my inventory; `grant_journal_v3` and format-2 are already protected by their tail+1 law. The README says exactly this and claims nothing more.

### N-4 — W-1/W-2 wording is now in the code
Module docs: "An unordered set of per-operation diffs, not a replayable history. Opaque operation hex never orders commits. The current projection cannot be rebuilt…", "linkage to attempt/receipt is NOT [checked]", "Noops do not consume an operation; host attempt custody owns single use", and `first_publication` documented as an "Unverified host assertion". `operation_hex_order_does_not_order_the_current_projection` commits `f…` then `0…`. That is the choice I assessed, made executable.

## 7. Closure of earlier findings

| Finding | Status |
|---|---|
| 185 F-1 (REPLACE rewrites immutable rows) | **Closed for the six storage tables**, at the schema level, on any connection, including all secondary unique keys and the settled-custody case. Open, and tracked by the owner, for `carrier_format`; not fixable by trigger for the inherited tables |
| 185 T-1 (five real gaps) | **Closed** — all five mutants now killed by owner tests |
| 185 W-1 / W-2 / N-1 | Closed as decisions, documented in code, with the reverse-hex regression |

## 8. Limits

Synthetic storage fixtures; bundled SQLite 3.53.2. The affinity variants in probe 2 are the ones I thought of (TEXT/REAL for integer keys, INTEGER for the text key); I did not try BLOB-typed keys because the column CHECKs refuse them and a BLOB never equals TEXT in a unique index. I did not rebuild the owner's 13 compiled mutants or host receipt 118, and did not test crash durability, sidecars or a production creator (none exists).

## 9. Verdict (bounded)

**The six guards are correct, complete over each table's uniqueness constraints, effective on any connection with `recursive_triggers` off, neither too narrow nor too broad under mutation, and part of the exact-verified schema; everything else in the pin mechanism is byte-identical in behaviour to 185. 185 F-1 is closed for these tables and 185 T-1 is closed.** No approval of the remaining tables, of any creator or upgrade, or cumulative readiness.
