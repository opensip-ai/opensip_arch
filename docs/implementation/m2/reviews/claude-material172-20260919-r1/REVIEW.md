# Independent bounded review — Run manifest and commit inventory in the recovery snapshot, 172 (Rust)

Reviewer: Claude (actual independent reviewer; Codex remains implementation owner). 2026-09-19.
Request: `material172-20260919-REQUEST.md` (bytes as read: `claude-out/REQUEST-as-read.md`); README and the full delta
read. Scope: the delta of frozen `recovery-material-checkpoint-172` over frozen 170 —
`storage/src/ledger_store/recovery_material.rs` (new), the receipt borrowed by `LedgerAnchor`
(`recovery_snapshot.rs`), and the entry points / error variant in `ledger_store.rs`. The `commit_run_material` table is
a **proposed private mechanism with no production creator, migration or writer**; references are inventory-named
values, not a transitive closure or proof of live existence; pins, semantic replay, project-current binding,
signatures, custody, host and authority remain owed — I infer none. No frozen/selected/product edit; scratch only,
`-I -B`, dedicated targets; no commit, push or delegation; no cumulative approval.

## 1. Subject verification (before use)
| Item | Value |
|---|---|
| `subject.tar.xz` | 8,159,792 bytes, SHA-256 `b3e6593200203c82d5142a4641a798a759f5f7a6de4ba4c4d8e56046cd91fd9f` = request = `archive-pin.json` |
| Members | 860/860 regular, length + SHA-256 equal to the manifest, from the tar before extraction; 0 unsafe/extra; re-verified at the end |
| Product pins | 347/347; none unpinned |
| Parent | `parent-inputs.json` = **my own** verified 170 extraction (346/346); 344 unchanged, 2 changed, 1 added |
| Host pins | host107 receipt: 227 sources all equal the product pins; no command failed (host106 is historical, as stated) |
| Owner checks, fresh scratch | 45/45 storage tests; strict workspace Clippy clean |

## 2. What it is (read in full)
`capture`: take 170's sealed ledger + availability observation from the caller's `ReadSnapshot`; **only if it offers
an anchor**, look up `commit_run_material` by `(store, namespace, execution)` on the same connection after an exact
definition check; require the row's `run_id` mirror to equal the anchor's Run; admit the manifest with the existing
`IdentityCandidate::from_json(.., IdentityDomain::Run, ..)`, require the stored bytes to be its canonical bytes and its
**content-derived identifier to equal the joined Run**; admit the inventory with the registered
`identity:v3#/$defs/commit-inventory` schema (which carries order and uniqueness), require canonical bytes,
`inventory.runId == Run`, and `raw SHA-256(inventory bytes) == receipt.inventoryDigest` — the receipt now borrowed by
the anchor at construction (`self.receipt.as_ref()?`). Three sealed states (not requested / absent / present with exact
bytes and the two string lists); any failure is `Err` for the whole observation. No new parser, schema or ID grammar.

**The digest law matches the reference.** `identity-model.v3.py::commit_inventory` digests
`sha256(C.canonical(record))` (raw, unframed); the contract calls `commit-inventory` "the record digested by
`commit-receipt.inventoryDigest`". For the inventory the product admitted, the frozen reference produces **byte-equal
canonical bytes and the same digest** (`probes/ref_inventory.py` → `io/ref-inventory.txt`).

## 3. Evidence
**3.1 Joins and single-violation negatives on real SQLite** (`probes/rust_probe.rs.txt` → `io/material.txt`; where a
negative would otherwise also break the digest, the receipt digest is *repaired* to the stored bytes so exactly one
rule is violated):
| # | State | Result |
|---|---|---|
| 1 | joined, table present, no row | **ABSENT** |
| 2 | valid | **PRESENT** — exact manifest and inventory bytes, objects in order, blobs |
| 3 | a *valid* manifest of another Run under this Run | `RunMaterial(RunIdentity)` |
| 4 | `run_id` column names another Run, bodies right | `Configuration("run_material_index")` |
| 5 | `inventory.runId` another Run, digest repaired | `RunMaterial(InventoryRun)` |
| 6 | a different valid inventory than the receipt digests | `RunMaterial(InventoryDigest)` |
| 7 / 8 | one extra space in inventory (digest repaired) / in manifest | `RunMaterial(Noncanonical)` |
| 9 / 10 / 11 | objects out of order / duplicate / unknown member, digest repaired | `RunMaterial(Schema(Mismatch))` — the registered schema is the order owner |
| 12 | joined, table missing | `Configuration("run_material_schema")` — never absence |
| 13 | nothing published, table missing | `UnknownAttemptUnobserved`, **NOT-REQUESTED**, `Ok` |
| 14 | one Run published by executions b and c, material stored only for c | b → ABSENT, c → PRESENT (per-execution key; no borrowing across executions) |
| 15 | material valid, availability body garbage | `Err Availability(..)` — whole observation fails, no splice |
| 16 | forced write + `wal_checkpoint(TRUNCATE)` while holding | completed `Ok` → 0; completed `Err` → 0; direct snapshot open → 1; after drop → 0 |

**3.2 Mutants** (`probes/mutation.py`, 12, all compiled, baseline green; complementary to the owner's eleven): manifest
identity, manifest canonical gate, inventory canonical gate, `inventory.runId`, inventory digest, `run_id` mirror,
keyed by Run instead of execution, failed lookup → absence, table definition not required, objects/blobs exchanged —
**10/10 killed by the owner's tests.** Two survive both suites and are equivalent by construction (disclosed): digest
over the re-encoded value (equal to the stored bytes behind the canonical gate) and anchor digest read from the
association instead of the receipt (the join already requires `r.inventory == a.inventory`).

**3.3 Privacy / lifetime** (`probes/compile-boundaries.log`, clients in the parent module): **10/10 rejected** — whole
observation literal, turning ABSENT/PRESENT into NOT-REQUESTED, swapping the ledger observations, material record
literal, writing through `manifest_bytes()`, view outliving its evidence (E0505), reaching `parse_material` (no
admitted material from caller bytes), reaching the hook, `Clone`, and an anchor literal with a caller-chosen receipt
(the new field, E0451).

The README's account of mutation r1 (a local order-bypass survived because the selected schema already checks order;
the redundant production check was removed and r2 attacks the schema boundary) is consistent with what I see: cases
9–10 are refused by the schema, and there is no second order check in the production code.

## 4. Findings
No defect and no finding of substance.
- **N-1 (note, the claim limit that matters most)** "present" establishes four equalities — manifest bytes ↔ RunId,
  inventory bytes ↔ receipt digest, `inventory.runId` ↔ Run, row key ↔ requested execution — and **nothing about the
  relation between the manifest and the inventory's contents**: whether `objects` contains the identities the manifest
  names (`planId`, `snapshotId`, `evidenceId`, `evaluationSealId`, …) is not checked here, and the fixtures use
  free-text objects (`plan2:first`). The README says references are "inventory-named values, not transitive closure";
  a consumer must not read PRESENT as "the manifest's closure is inventoried". That join belongs to the owed replay /
  closure owner.
- **N-2 (note, inherited shape)** As in 170 N-1 and 150 F-2, a failure in *any* layer (ledger, availability, material)
  discards the layers already read in this snapshot (case 15). Deliberate — "no reread-and-splice fallback" — and the
  right default; the mapper must not rebuild a composite from separate snapshots.
- **N-3 (note, mechanism status)** The DDL constant lives in this reader module and only tests create the table. When a
  writer/publication owner is proposed, the DDL should have one owner shared by creator and reader (as
  `inherited_schema` / `CURRENT_CARRIER_DDL` do), or the two will be compared against different texts. Until then a
  production database can never be PRESENT — only `Configuration("run_material_schema")` — which is the honest state.
- **N-4 (note)** `manifest` and `inventory` are unbounded BLOBs bounded only by the snapshot connection's
  `SQLITE_LIMIT_LENGTH` and the `work` budget of schema admission; the owned copies are retained for the life of the
  observation. Fine for now; a byte budget in the style of 155's `max_body_bytes` will be wanted before this meets
  real manifests.

## 5. Bounded verdict
**172: reviewed, no finding of substance. The Run manifest and the per-execution commit inventory are read in the same
SQL snapshot as the ledger join and availability, only for a joined anchor; the manifest must be canonical bytes whose
content-derived identity equals the joined Run; the inventory must be schema-valid (order, uniqueness, closed shape),
canonical, name that Run and hash — raw SHA-256 of the stored bytes — to the receipt's `inventoryDigest`, which agrees
byte for byte with the frozen reference's `commit_inventory`; "not requested", "absent" and "present" stay distinct and
sealed; every failure is an error for the whole observation and SQL is released on success and on error; the
observation and the anchor's new receipt borrow cannot be forged, edited, cloned or outlived (10/10); my ten meaningful
mutants are killed by the owner's tests and each of my sixteen negatives violates exactly one rule.** Not a claim that
the manifest's closure is inventoried, not retention or existence proof, not a production writer or migration, and not
pins, replay, custody, host, authority or any cumulative standing.

Evidence (`claude-out/`): `pin-verification.json`, `pins.py` → `product-pins.json`, `diffs/`, `owner/`,
`probes/{rust_probe.rs.txt, ref_inventory.py, mutation.py, mutation.json, mutation.log, compile-boundaries.json/.log}`,
`io/{material.txt, ref-inventory.txt}`, `hashes.txt`.
