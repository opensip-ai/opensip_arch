# Independent review — frozen `recovery-limits-checkpoint-179`

Reviewer: Claude (independent; Codex remains owner). Date 2026-09-19. Review dir: this directory (one disclosed exception in §7).
Scope: exactly the frozen 179 product bytes — named recovery read limits, the shared-opener UTF-8 gate, and the regression tests answering my 176 T-1/T-2 and 177 T-1/N-1. The 180 policy is reviewed separately (`claude-encoding180-20260919-r1`); 181 is proposal work and not in scope. No cumulative, host, policy, custody or selection approval.

## 1. Identity verified

| Item | Result |
|---|---|
| `subject.tar.xz` | SHA-256 `6849b47237a6d0b9516e53bd8578eafe55c2b073dee9aff959151f0af96e9d65`, 4,233,832 B = request = `archive-pin.json` |
| Members | 478, all regular/safe, verified from the tar before extraction; re-verified at end |
| Product pins | 350/350; none unpinned |
| Parent | equals **my own verified 177 extraction**; 347 unchanged; changed `ledger_store.rs` (`23f77e97f920f1bf…`), `recovery_material.rs` (`f7ff929eadf8ae03…`), `recovery_pins.rs` (`7e1d12fa0d0f2bcb…`); fixtures unchanged |
| Host receipt 113 | 230 sources equal pins; none failed |

## 2. Owner checks re-run

Fresh scratch copy byte-equal to the product, `--offline --locked`, dedicated target: **58 storage tests pass; strict workspace Clippy exit 0**. Owner typed clients read: the three refusals are the intended diagnostics (E0061 old positional call, E0308 pin-limits passed as material-limits, E0063 missing unit), not incidental failures.

## 3. What changed, as read

- `configure()` — the single function behind `open_existing`, hence behind both `ReadSnapshot::open` and `ExistingWriter::open` — now begins with `PRAGMA main.encoding` and refuses anything but `"UTF-8"` as `Configuration("text_encoding")`. I enumerated every production `Connection::open*` in `crates/`: the storage ledger has exactly this one file opener (the rest are in-memory DDL expectations or the security journal), so the gate is systemic, not per-reader.
- `RecoveryReadLimits { per_record_work, retained_body_bytes }` replaces the adjacent positional `usize`s through material and pin capture; `PinReadLimits` stays a distinct type.
- Tests: non-boundary getter reads, receipt-only charging, foreign store/namespace rows, BLOB pin/kind, extra index/trigger, body budget 0 through pin capture, UTF-16LE/BE opener refusals.

## 4. My probe and mutation

**Probe** (`claude-out/probes/rust_probe.rs.txt` → `io/pins.txt`): my 177 probe ported to the new API. Cases 1–8 are **byte-identical to the 177 output** (980-cell grid 0 wrong, storage classes, schema variants, no-anchor, precedence, 3 MB name, WAL release). Every UTF-16 case — clean names, all six malformed/aliasing sequences from 177 F-1 — now refuses `text_encoding`. Reader and writer refuse LE and BE, admit UTF-8, leave main-file bytes unchanged and create no `-wal`/`-shm` sidecars.

**Mutation** (`claude-out/probes/mutation.{py,json,log}`; baseline green; no compile failure counted): **15/15 killed by the owner's tests.**
- all 8 survivors from my 176/177 reviews (getter = limit; prior charged only with anchor; store filter; namespace filter; BLOB tolerated; companions ignored; body budget ignored by pin capture; units swapped inside pin capture);
- 7 new: encoding gate reader-only / writer-only / LE-only / BE-only; triggers-only ignored; BLOB kind only; material parse work taken from the body budget.

## 5. Findings

### F-1 (medium-low, regression, measured) — the opener now waits ~5.4 s on a locked ledger instead of failing at once
`configure()` runs the encoding query **before** `c.busy_timeout(Duration::ZERO)`. `PRAGMA main.encoding` must read the database header, so it is the first lock-taking statement on the connection, and at that moment rusqlite's default 5,000 ms busy handler is still installed. In 177 the first read came after the timeout had been zeroed.
Measured with the same test in my 177 and 179 scratch trees (`claude-out/probes/busy_probe.rs.txt`, `busy_run.sh`, `io-busy-177/`, `io-busy-179/`):

| Holder | 177 reader / writer | 179 reader / writer |
|---|---|---|
| rollback-journal ledger, other connection in `BEGIN EXCLUSIVE` | `DatabaseBusy` after **0 ms** / 0 ms | `DatabaseBusy` after **5,400 ms** / 5,393 ms |
| WAL ledger, other connection in `locking_mode=EXCLUSIVE` with an open write | 0 ms / 0 ms | **5,387 ms** / 5,372 ms |

The result is the same error; the latency is not. Security S7's lock table gives level 3 as "writers BEGIN IMMEDIATE, **busy_timeout 0**; … Blocking: **never** for readers". A recovery reader that stalls five seconds per open — under the lifecycle fence, whose own bounded wait is 5 s — is outside that law, and no owner test can see it (none opens against a held lock).
Remedy is ordering, not a band-aid: make `busy_timeout(ZERO)` the first act of `configure()`, then the encoding gate, then everything else; and add the held-lock control (assert prompt `DatabaseBusy` for both access modes) so the ordering is pinned. The README's "before any domain text" is still satisfied.

### W-1 (low) — "unknown-custody" is asserted by 180 but not reachable from this error shape without a mapper
`Configuration("text_encoding")` shares the `Configuration(&'static str)` variant with `connection_limit`, `db_config`, `pin_schema`, `pin_storage`, `pin_text`. 180 requires this one to project as `unknown-custody / HOST.IO_FAILURE`; whether the other `Configuration` strings do is a mapper decision not yet made. Host mapping is disclosed as owed; I note only that a string-keyed variant is what the future mapper must match on, and a typo there fails open to whatever the default arm is. A dedicated variant (as `RecoveryBodyBudget`/`PinReadBudget` got) would make the 180 projection exhaustively checkable.

### N-1 (note) — named limits close the transposition by name, not by type
Accurately disclosed ("not a claimed newtype for each scalar"). Swapping the two fields inside a struct literal still compiles; the owner's `work-unit-swapped`/`body-unit-swapped` faults and my own swap mutant are killed by tests, which is the appropriate control for a private, inert config. My probe case 11 (work 0 vs body 0) was too weak to show work forwarding on its own — with no material row and no availability record `per_record_work` is never consumed — so forwarding of `per_record_work` rests on the owner's test and my killed "work taken from body budget" mutant, not on that case.

### N-2 (note) — a zero-byte file passes the encoding gate
SQLite reports `UTF-8` for an empty file (measured in my 180 probe). Correct here — later schema admission refuses it and 180 says the observation proves nothing else — but the ordering "encoding, then exact DDL" is what makes it safe; keep them in one opener path.

## 6. Closure of earlier findings

| Finding | Status in these bytes |
|---|---|
| 176 T-1 getter exactness | **Closed** — reads at `total+1` and `usize::MAX`; my mutant now killed |
| 176 T-2 prior charging without anchor | **Closed** — `unjoined_receipt_is_charged_even_when_material_lookup_is_skipped`; mutant killed |
| 176 N-1 / 177 T-1 transposition | **Closed** as far as claimed (named fields + typed clients + killed swaps) |
| 177 F-1 UTF-16 aliasing | **Closed at the mechanism level** for every sequence I had measured, for both openers; policy owner is 180 (see that report's F-1 for a stale companion owner) |
| 177 T-1 six survivors | **Closed** — all six killed by owner tests |
| 177 N-1 `None` ≠ schema admitted | Closed in the accessor doc |
| 177 N-2, N-3 | Unchanged, still accurate (precedence is now stated in the README) |

## 7. Disclosures and limits

- My first busy-probe loop was written inline in zsh, did not word-split, and ran nothing (cargo found no manifest in the repository cwd and exited; `git status` afterwards shows only the owner's own changes). Rerun as `busy_run.sh`.
- **Outside-directory write, reverted:** to obtain the 177 baseline, `busy_run.sh` appended the busy test to the scratch `build-probe` copy inside my *177* review directory. That file is not hashed evidence; I restored it to its exact prior content (product file + 177 probe), re-checked every line of the 177 `hashes.txt` (all OK) and re-verified the 177 extraction. Build artefacts under that review's `target-probe` were refreshed. No frozen, selected or repository file was touched.
- Synthetic storage fixtures; bundled SQLite 3.53.2; timing measured once on this machine (the 0 ms vs ~5.4 s gap is three orders of magnitude, not noise). I did not rebuild the owner's typed clients or measure heap.

## 8. Verdict (bounded)

**Every gap I reported against 176 and 177 is closed in these bytes and all 15 of my mutants die on the owner's own tests. F-1 is a new, measured regression introduced by the placement of the encoding query and should be fixed (one reordering plus one held-lock test) before this opener is built upon.** No approval of host policy, mapping, custody, any writer/creator, or cumulative readiness.
