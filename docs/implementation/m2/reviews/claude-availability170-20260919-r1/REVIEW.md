# Independent bounded review — ledger evidence + Run availability in one snapshot, 170 (Rust)

Reviewer: Claude (actual independent reviewer; Codex remains implementation owner). 2026-09-19.
Request: `availability170-20260919-REQUEST.md` (bytes as read: `claude-out/REQUEST-as-read.md`); README and the whole
delta read. Scope: the delta of frozen `recovery-availability-checkpoint-170` over frozen 168 —
`storage/src/ledger_store/recovery_availability.rs` (new, 70 production lines) and its entry points / test visibility
in `ledger_store.rs`. **Not** a complete Step 1 (manifests, object references, pins are absent), not retention proof,
authority, custody, a host facade or a public mapper; I infer none. No frozen/selected/product edit; scratch only,
`-I -B`, dedicated targets; no commit, push or delegation; no cumulative approval.

## 1. Subject verification (before use)
| Item | Value |
|---|---|
| `subject.tar.xz` | 4,220,632 bytes, SHA-256 `2da05d582d15a807dacb560516f8e0604098948a39459f62bcdc844ed5c28eeb` = request = `archive-pin.json` |
| Members | 425/425 regular, length + SHA-256 equal to the manifest, from the tar before extraction; 0 unsafe/extra; re-verified at the end |
| Product pins | 346/346; none unpinned |
| Parent | `parent-inputs.json` = **my own** verified 168 extraction (345/345); 344 unchanged, 1 changed, 1 added; no security file changed |
| Host pins | host105 receipt: 226 sources all equal the product pins; no command failed |
| Owner checks, fresh scratch | 41/41 storage tests; strict workspace Clippy clean |

## 2. What it is (read in full)
`capture(snapshot, schemas, binding, work)`: take the sealed `CapturedLedger` (157/163) from the caller's
`ReadSnapshot`; **only if it offers an anchor** (`ContinueCarrier`, association bound) take `anchor.run()` and call the
*existing* `load_current_availability` on the **same connection** — exact-definition check, latest row by
`length(generation) DESC, generation DESC`, existing parser, and the existing index/body agreement
(`record.run() == run`, `generation` text equals the body's). The result seals three states: `None` (no Run admitted —
no read attempted), `Some(view)` without a record (admitted row absence), `Some(view)` with the parsed record and its
exact bytes. Any lookup failure is `Err` for the whole capture. `read_recovery_with_availability` opens and drops the
snapshot; the `ReadSnapshot` method keeps the caller's. No new parser, schema or SQL ordering.

## 3. Evidence
**3.1 Joins and error behaviour on real SQLite** (`probes/rust_probe.rs.txt` → `io/availability.txt`):
| # | State | Result |
|---|---|---|
| 1 | joined, table present, no row | `ContinueCarrier`, **ABSENT** for the joined Run |
| 2–3 | generations 0, 9, 10, then `u64::MAX` | **PRESENT** gen 10, then gen 18446744073709551615 — numeric, not text, order; bytes retained |
| 4 | a non-canonical `'010'` sorting above `'9'` (CHECK bypassed) | `Err Configuration("availability_index")` — not silently the lower row |
| 5 | index says 5, body says 4 | `Err Configuration("availability_index")` |
| 6 | latest body garbage | `Err Availability(Admission(Schema(Json)))` |
| 7 | an **older** body garbage, latest valid | PRESENT (only the latest row is read — N-2) |
| 8 | rows only under another Run key | ABSENT |
| 9–10 | index dropped / table missing, with an anchor | `Err Configuration("availability_schema")` — never absence |
| 11 | nothing published, table missing | `UnknownAttemptUnobserved`, **NOT-REQUESTED**, `Ok` — a skipped lookup does not trip on the missing schema |
| 12 | the 157 state (foreign association body under the requested execution) with availability present **for the foreign Run** | `UnknownCustody`, no anchor, **NOT-REQUESTED** — the foreign Run is never looked up |
| 13 | SQL release, forced write + `wal_checkpoint(TRUNCATE)` while holding the value | completed `Ok` → 0; completed **`Err`** → 0; direct snapshot still open → 1, after drop → 0 |

**3.2 Mutants** (`probes/mutation.py`, 7, all compiled, baseline green; complementary to the owner's seven): failed
lookup → absence; failed lookup → not-requested (ledger kept); lookup whenever an association exists (anchor gate
ignored); availability read in a **second** snapshot; view's Run emptied; absent reported as not-requested; lookup
skipped while settlement is pending — **7/7 killed by the owner's tests.** The owner's interleaving test is the right
one: a real writer settles the attempt *and* inserts availability between the two reads, and the capture still shows
`Admitted` + absent while a new read shows `Committed` + present.

**3.3 Privacy / lifetime** (`probes/compile-boundaries.log`, clients in the parent module): **8/8 rejected** — whole
observation literal, turning ABSENT into NOT-REQUESTED on genuine evidence, swapping the ledger under genuine
availability, run-availability literal, view literal, view outliving its evidence (E0505), reaching the hook, `Clone`.
Two compile and are the stated surface (read-only use; direct snapshot keeps the caller's reader).

## 4. Findings
No defect and no finding of substance.
- **N-1 (note, for the mapper that does not exist) — a failed availability lookup discards the ledger evidence too.**
  `?` on the lookup returns `Err` for the whole capture, so a caller that gets `availability_schema` / `_index` /
  parse errors has no `CapturedLedger` in hand, although one was read successfully in that snapshot. That is the same
  deliberate shape as 150 F-2 (second-capture failure) and I do not ask for it to change — "failed lookup never becomes
  absence" is the property that matters and it holds — but the host must not answer such an error by calling
  `read_recovery` separately and presenting the pair as one observation: that would be two snapshots. If the ledger
  standing is wanted despite an availability failure, it has to come from this owner, in this snapshot.
- **N-2 (note, scope of "latest")** Only the newest row is read and admitted; an older malformed row is invisible (case
  7), and the successor chain is checked by the *writer* (`check_successor`), not by this reader. Accurate as "latest
  actual availability"; it is not admission of the availability history.
- **N-3 (note)** The lookup key is the joined association's Run (`anchor.run()`), which the join already equated with
  the receipt's Run; the pre-existing `current_availability` derives it through `paired_run`. Two routes to the same
  value today — if the join law ever relaxes `r.run == a.run`, they diverge; the anchor route is the better one to keep.
- **N-4 (disclosed)** My probe needed `pair_fixture` visible to the child test module; I widened it in my scratch copy
  only (the frozen test module keeps it private). The README's statement that fixture generation gaps are not lawful
  writer examples is right: my cases 4–6 insert rows no lawful writer produces (one needs `ignore_check_constraints`).

## 5. Bounded verdict
**170: reviewed, no finding of substance. The ledger join and the latest availability of the joined Run are read in
one SQL snapshot through the existing schema check, ordering and parser; "not requested", "admitted absence" and
"present with exact bytes" stay distinct and sealed; every lookup failure is an error and never absence; a foreign Run
is never looked up; numeric uint64 ordering holds up to `u64::MAX`; a completed read releases SQL on success **and** on
error while a direct snapshot keeps the caller's reader; the observation cannot be forged, edited, cloned or outlived
(8/8); all 7 of my mutants are killed by the owner's tests.** Not a complete Step 1, not retention proof, authority,
custody, a host facade or mapper, and not any cumulative standing.

Evidence (`claude-out/`): `pin-verification.json`, `pins.py` → `product-pins.json`, `diffs/`, `owner/`,
`probes/{rust_probe.rs.txt, mutation.py, mutation.json, mutation.log, compile-boundaries.json/.log}`,
`io/availability.txt`, `hashes.txt`.
