# Independent review — frozen `ledger-opener-checkpoint-183`

Reviewer: Claude (independent; Codex remains owner). Date 2026-09-19. Review dir: this directory only (the 179 baseline tree used for comparison is a copy made **inside** this directory from my verified 179 extraction).
Scope: exactly the frozen 183 product bytes — the opener ordering fix for my 179 F-1 and the typed encoding error for 179 W-1. 182 (policy) and 181 are separate. No host-mapper, custody, writer/creator, cumulative or selection approval.

## 1. Identity verified

| Item | Result |
|---|---|
| `subject.tar.xz` | SHA-256 `eb483de0bad15bb707f2a5a2eeb15d6c763c6ba3093198ed9ce529a374224ab7`, 4,230,672 B = request = `archive-pin.json` |
| Members | 399, all regular/safe, verified from the tar before extraction; re-verified at end |
| Product pins | 350/350; none unpinned |
| Parent | equals **my own verified 179 extraction**; 349 unchanged; only `crates/storage/src/ledger_store.rs` changed (`cb65b95a3b81cef4…`); fixtures unchanged |
| Host receipt 114 | 230 sources equal pins; none failed |

## 2. Owner checks re-run

Fresh scratch copy byte-equal to the product: **60 storage tests pass; strict workspace Clippy exit 0** (`claude-out/owner/`).

## 3. The change, as read

`configure()` now sets `busy_timeout(ZERO)` as its first act, then queries `PRAGMA main.encoding`. A query failure becomes `LedgerError::Encoding(LedgerEncodingError::Observation(sqlite_error))`; a non-UTF-8 value becomes `…::Unsupported(observed)`. Nothing else in production changed. Two new tests: a sentinel busy handler (counts invocations — ordering is detected without sleeping), and a held-lock test for both openers on rollback-journal and WAL ledgers with unlocked controls.

## 4. Reproduction (my probe, same test text in a 179 tree and the 183 tree)

`claude-out/probes/opener_probe.rs.txt`, `opener_run.sh` → `io-179/opener.txt`, `io-183/opener.txt`, `io/opener-179-vs-183.diff`.

| Case | 179 | 183 |
|---|---|---|
| 1 rollback-journal ledger held `BEGIN EXCLUSIVE` | `Sql(DatabaseBusy)`, **>1 s** (whole test 21.6 s) | `Encoding(Observation(DatabaseBusy))`, **<1 s** (whole test 0.03 s) |
| 2 WAL ledger held in exclusive locking mode with an open write | same as 1 | same as 1 |
| 3 WAL ledger, ordinary writer mid-transaction | Ok / Ok | Ok / Ok (no false refusal) |
| 4 8 KiB of `A` | `Sql(NotADatabase)` | `Encoding(Observation(NotADatabase))` |
| 5 zero-byte file | `Configuration("journal_mode")` | same (passes the encoding gate, refused by the next one — as I predicted in 179 N-2) |
| 6 valid header truncated to 100 B | `Sql(DatabaseCorrupt)` | `Encoding(Observation(DatabaseCorrupt))` |
| 7 header text-encoding field = 7 | `Sql(DatabaseCorrupt)` | `Encoding(Observation(DatabaseCorrupt))` |
| 8 file mode 000 | `Sql(CannotOpen)` | same (fails before `configure`) |
| 9 file mode 400 | Ok / Ok | same |
| 10 healthy ledger | Ok / Ok | Ok / Ok |

**179 F-1 is fixed**: held-lock refusal is prompt for both openers and both journal modes. **Side effects:** main-file bytes unchanged in every case and the sidecar columns are identical line-for-line between 179 and 183 — the diff consists only of latency and error shape. **Precedence:** unchanged — encoding, then limits/db-config, then journal mode; the only re-ordered statement is the timeout.

## 5. Mutation (`claude-out/probes/mutation.{py,json,log}`; baseline green; no compile failure counted)

7/7 killed by the owner's tests: 179 F-1 re-applied (killed by **both** new tests); timeout 1500 ms and 50 ms; `Unsupported` carrying a constant; observation failure reported as `Unsupported("")`; observation failure treated as UTF-8 (fail-open); gate for readers only.
Worth recording: the two non-zero-timeout mutants were not killed by the 2-second timing allowance (1500 ms sits inside it) but by `configure()`'s own existing read-back guard `("busy_timeout", 0)`, which makes every opener fail. So "zero wait" is enforced by production code, and the generous test allowance is not the control — which is the right way round.

## 6. Findings

### F-1 (medium-low) — `Observation` relabels every first-touch failure as an encoding fact, including *busy*, which has its own public route
Because the encoding query is now the first statement to touch the file, whatever is wrong with the ledger surfaces there, and all of it is wrapped as `Encoding(Observation(_))`: a lock held by another process (cases 1–2), a non-database (4), a truncated or corrupt header (6–7). In 177 and 179 these were `Sql(DatabaseBusy)`, `Sql(NotADatabase)`, `Sql(DatabaseCorrupt)`. The type's doc comment says the variants are "typed observations for the future host mapper", the README says the mapper "has typed captured facts", and 182 says an unavailable encoding observation projects as `HOST.IO_FAILURE` / `host-io`. Put together, the natural mapper sends a merely **busy** ledger to `host-io`. The existing owners give busy a different route: `commit-recovery-readonly.v3.md` §1 `unavailable-busy` → `LEDGER.BUSY_TIMEOUT` / `ledger-busy` / `PROJECT.BUSY`, and workflows §"Retries" makes `ledger-busy` the *only* retryable fault while "`host-io` … never retried". The same lock met one statement later still arrives as `Sql(DatabaseBusy)`, so the classification of an identical condition now depends on which statement happened to hit it. The owner's two new tests assert the `Encoding(Observation(DatabaseBusy))` shape, so the relabelling is pinned as intended behaviour.
The inner `rusqlite::Error` is preserved, so nothing is lost and a careful mapper can unwrap it — this is a classification hazard, not a wrong answer today (no mapper exists). But 179 W-1's purpose was to make the 180/182 projection *exhaustively checkable from the type*; with busy and corruption inside `Observation` the type again under-determines the route.
Systemic remedy (owner's choice of shape): an encoding fact should be only what was learned about encoding. Either keep first-touch SQLite failures as `Sql(e)` (as before) and reserve `Encoding` for a *successfully observed* unsupported value plus a genuinely encoding-specific unobservable case; or introduce a neutral first-touch variant and classify busy before wrapping. Then assert in the held-lock tests that busy is reported as busy.

### N-1 (note, pre-existing, outside the delta) — `ExistingWriter::open` succeeds on a read-only file
Case 9: on a mode-400 ledger both openers return Ok, identically in 179. SQLite silently degrades a READ_WRITE open to read-only; the failure would surface later at the first write. Separately, opening that checkpointed WAL ledger created `-wal`/`-shm` sidecars (also identical in 179). Neither is introduced here; I record them because "existing writer admission" is being built on this opener and 182 speaks of refusing "before any mutation".

### N-2 (note) — timing assertions
The 2 s allowance is disclosed as scheduling tolerance. The sentinel-handler test is the real ordering control and is deterministic; good design. The timing test adds the end-to-end check through the actual openers. Both kill the re-applied fault.

## 7. Closure of earlier findings

| Finding | Status |
|---|---|
| 179 F-1 (5.4 s wait) | **Closed** — reproduced fixed; my re-applied fault killed by both new tests |
| 179 W-1 (string-keyed `text_encoding`) | **Closed as stated** for the unsupported case (`Unsupported(observed)`, exact value asserted for LE and BE, both openers); the `Observation` half introduces F-1 above |
| 179 N-2 (zero-byte file passes the gate) | unchanged, confirmed (case 5) |

## 8. Limits

Synthetic fixtures; bundled SQLite; latency bucketed at 1 s in my probe (the whole-test wall time 21.6 s vs 0.03 s is the quantitative evidence). I did not rebuild host receipt 114 or test big-endian hosts. No mapper exists, so F-1 is about what these types invite, judged against the existing public-route owners.

## 9. Verdict (bounded)

**The 179 F-1 regression is fixed, without new side effects or precedence change, and is now guarded by a deterministic test plus the production read-back of `busy_timeout`. The typed error is right for `Unsupported`; `Observation` is too wide (F-1) and should be narrowed before a mapper is written against it.** No approval of mapping, custody, any writer/creator, or cumulative readiness.
