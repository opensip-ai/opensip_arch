# Independent review — frozen `recovery-read-budget-checkpoint-176`

Reviewer: Claude (independent; Codex remains owner). Date 2026-09-19. Review dir: this directory only.
Scope: exactly the frozen 176 bytes — the aggregate retained-body budget in the recovery material reader, and the three fixture rows added for my 174 T-1. Not 175, not 177 (unfrozen, not read), not 178, no cumulative/authority/host/release approval.

## 1. Identity verified

| Item | Result |
|---|---|
| `subject.tar.xz` SHA-256 | `0ea90050d9847aea6e6548a6fe841d1a60cf309c564fa63e496a6d8adf5cf2ae`, 8,168,076 B — equals request and `archive-pin.json` |
| Members | 818, every one a regular file with a safe relative path, verified from the tar before extraction; re-verified at the end (`claude-out/pin-verification.json`, `mode: re-verified`) |
| Product pins | 349/349 equal (`claude-out/product-pins.json`) |
| Parent | compared with **my own verified 174 extraction**: 345 unchanged; changed exactly `ledger_store.rs`, `ledger_store/recovery_material.rs`, `pin_inventory.rs`, `fixtures/pin-budget174.json` |
| `pin_inventory.rs` | everything before `#[cfg(test)]` byte-identical to 174; test delta is the case count 46→49 only |
| Host receipt 111 | 229 sources equal product pins; none failed |
| Changed-file SHA-256 | `ledger_store.rs e8994cf6…141e`; `recovery_material.rs 5096f70c…9814`; `pin_inventory.rs 213a15d1…7832`; `pin-budget174.json f57f6016…5d9a` (39,919 B) |

## 2. Owner checks re-run (fresh scratch copy, `--offline --locked`, dedicated target)

50 storage tests pass; strict workspace Clippy (`-D warnings`, all targets) exit 0 (`claude-out/owner/`). Scratch source tree is byte-equal to the frozen product (`diff -r`).

## 3. What the change is, as read

`read_recovery_material(path, schemas, binding, per_record_work, retained_body_bytes)`; a private `BodyBudget{remaining, used}` with `charge` = `checked_sub` on remaining then `checked_add` on used, both mapped to the new `LedgerError::RecoveryBodyBudget`, state updated only after both succeed. `prior()` charges the raw lengths of receipt, association and latest availability record when present. `load` now borrows the row through `ValueRef`: `run_id` must be `Text` byte-equal to the Run, manifest and inventory must be `Blob`; **both blob lengths are charged before either `to_vec()` or parse**. `retained_body_bytes()` returns `used`. No default cap, no public policy, no mapping — consistent with the claim.

## 4. My probe (`claude-out/probes/rust_probe.rs.txt` → `claude-out/io/budget.txt`)

Independent fixture with all five bodies: receipt 333 + association 724 + availability 170 + manifest 547 + inventory 227 = **2001**.

| Probe | Result |
|---|---|
| Every limit 0..=2003, exhaustively | `Ok` iff limit ≥ 2001, and then `used == 2001` regardless of limit; otherwise `RecoveryBodyBudget`. **0 wrong answers of 2004** |
| `usize::MAX` | Ok, used 2001 (no overflow route) |
| No availability, no material | exact 1057 Ok; 1056 Err |
| Nothing published | limit 0 Ok, used 0, material not requested |
| Receipt only (unknown custody, material not requested) | exact 333 Ok; 332 Err — prior bodies are charged even when no anchor/material read follows |
| Garbage manifest, budget full | `RunMaterial(Candidate…)`; one byte short → `RecoveryBodyBudget` (budget precedes parse) |
| 3 MB garbage inventory, budget covers manifest only | `RecoveryBodyBudget`; covers both → schema error. The large body is refused from its borrowed length; it is never copied or parsed |
| Forced write + `wal_checkpoint(TRUNCATE)` while holding a budget-failure result | busy = 0 (reader released) |
| Failure shape | always whole-capture `Err`; never `Ok(None)`, never partial material, never truncation |

r1 of this probe is preserved as failed evidence (`io/budget-FAILED-r1-…txt`): my availability record named another Run, so `availability_index` masked two cases. It was my fixture error, not a product fault; r2 re-issues the record for my Run (the owner's test does the same).

## 5. Mutation (`claude-out/probes/mutation.py`, `.json`, `.log`)

Scratch copy, source pins not involved (cargo tests only), baseline green first; no compile failure is counted.

| Mutant | Owner tests | My probe |
|---|---|---|
| 174 T-1: DEL counted as escaped | **KILLED** | — |
| 174 T-1: solidus escaped | **KILLED** | — |
| 174 T-1: first publication gets legacy exception | **KILLED** | — |
| receipt / association / availability / manifest / inventory not charged (5) | KILLED | — |
| off by one | KILLED | — |
| inventory charged after parsing | KILLED | — |
| budget failure reported as absence | KILLED | — |
| getter returns the **limit** instead of bytes used | **SURVIVED** | detected |
| prior bodies charged only when an anchor exists | **SURVIVED** | detected |

## 6. Findings

No blocking finding. Production behaviour matched my oracle on every case.

### T-1 (test gap, low–medium) — the "exact checked count getter" is only ever observed where used == limit
Every owner `Ok` assertion on `retained_body_bytes()` reads at exactly the boundary (`read_budget(ledger_bytes)`, `read_budget(total)`, `read_budget(prior)`, and `0,0`). At that point "bytes used" and "limit supplied" are the same number, so a getter that echoes the caller's limit passes all 50 tests. The getter is the one new externally visible value in this checkpoint and the request names it as a claim; its exactness is currently evidenced by my probe (used = 2001 at limits 2002, 2003, `usize::MAX`), not by an owner test. Remedy: one assertion at `total + 1` (or `usize::MAX`) expecting `total`.

### T-2 (test gap, low) — prior-body charging is never exercised without an anchor
All owner budget tests publish a receipt+association pair. Gating `prior()` on anchor presence survives. My receipt-only case (333 exact / 332 refused) distinguishes it. This matters because the README's law is "actual retained bodies", and the unknown-custody route still retains the receipt bytes. Remedy: a receipt-only boundary pair.

### N-1 (note, design) — two adjacent positional `usize` limits with different units
`per_record_work` and `retained_body_bytes` sit side by side in three signatures. A transposition compiles, and with the owner tests' values (2,000,000 vs ~1–2 kB) would mostly fail loudly, but in a host that chooses similar magnitudes it would silently swap a per-record work bound for an aggregate retention bound. The project's own guardrail style (private newtypes elsewhere in this crate) suggests a one-field newtype when the host policy owner lands. Not a defect in these bytes.

### N-2 (note, accuracy of claim — agrees with disclosure)
The budget charges prior bodies *after* they were read and owned under the existing per-record 4 MiB cap; only the two material blobs are refused before copy. The README says this plainly ("not peak heap"); I confirm the code matches that statement and nothing stronger. Worst-case transient retention before refusal is therefore three prior records, not zero.

## 7. Closure of earlier findings

- **174 T-1 (DEL, solidus, first-publication decreasing count): closed.** The 49-case fixture recomputes with 0 differences under my independent `fixture_check.py` against the reference law; the original 46 cases are equal as data and `run` is equal; all three of my 174 survivors are now killed by `exact_reference_counters_and_mutation_dispositions`. As the owner states, this remains differential evidence through the same expander, not an independent oracle — my recomputation is the independent leg.
- **174 N-1:** corrected separately in my 174 `NOTES.md` (4 MiB; I had measured characters). Nothing in 176 depends on it.
- 172 N-1 (manifest↔inventory contents not joined), 175 F-1/F-2: not in scope here; remain with their owners (178 decision for 175).

## 8. Limits

Storage-crate synthetic fixtures only; no replayed Runs. I did not measure heap. No additional privacy client was written: the new surface is one scalar getter on an already-private type and the owner claims no new privacy qualification; I checked only that fields stay private and the E0515 fix did not widen visibility (none of the production items changed visibility vs 174). In my probe scratch copy only, the test helper `insert_recovery_material` was widened to `pub(super)`. Host policy, mapping, custody, pin SQL observation (177), and everything downstream remain owed and unreviewed.

## 9. Verdict (bounded)

**The frozen 176 bytes do what the request says, within the stated boundary: no blocking finding; T-1 and T-2 are test gaps the owner should close; 174 T-1 is closed.** This is not approval of any other checkpoint, of a product cap/policy, or cumulative readiness.
