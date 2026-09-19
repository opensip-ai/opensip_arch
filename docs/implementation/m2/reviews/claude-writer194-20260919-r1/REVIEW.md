# Independent review — frozen `writer-access-checkpoint-194`

Reviewer: Claude (independent; Codex remains owner). Date 2026-09-19. Review dir: this directory only. macOS host, unprivileged.
Scope: exactly the frozen 194 product bytes — the writer access-mode gate. **Closes the main-file half of my 183 N-1 only**; sidecar custody and writability, and the 195 owner exception (a proposal), are not part of it and are not assessed. My 194 *proposal assistance* recommended this gate; that is not acceptance of these bytes. No cumulative approval.

## 1. Identity verified

| Item | Result |
|---|---|
| `subject.tar.xz` | SHA-256 `f66d864225a8c8fef9d5179bd0789df8ab18fefab22a8a88548eaa69182f8a6a`, 4,241,536 B = request = `archive-pin.json` |
| Members | 408, all regular/safe, verified from the tar before extraction; re-verified at end |
| Product pins | 352/352; none unpinned |
| Parent | equals **my own verified 193 extraction**; 351 unchanged; only `crates/storage/src/ledger_store.rs` changed (`dabe200ac161ce7d…`); fixtures unchanged |
| Host receipt 122 | 232 sources equal pins; none failed |

## 2. Owner checks re-run

Fresh scratch copy byte-equal to the product: **82 storage tests pass; strict workspace Clippy exit 0**.

## 3. The change, as read

Production delta is ten lines: a private `LedgerError::ReadOnlyWriter` variant ("No transaction was attempted. This is not a commit/recovery judgment."), and in `open_existing`, **after** `Connection::open_with_flags` and **before** `configure()`:
`if !reader && c.is_readonly(rusqlite::MAIN_DB)? { return Err(LedgerError::ReadOnlyWriter); }`.
`is_readonly` is `sqlite3_db_readonly` — a connection flag lookup, no SQL, no lock, no file access — so placing it before `configure()` means the refusal happens before the first statement that could touch a lock or a sidecar. No `unsafe`, dependency, schema, fixture or encoding change. Readers take the unchanged path.

## 4. My probe (`claude-out/probes/writer_probe.rs.txt` → `io/writer_gate.txt`)

| # | Case | Writer | Reader |
|---|---|---|---|
| 1 | healthy 0600 ledger | Ok | Ok |
| 2 | main **0400** | **`ReadOnlyWriter`**, prompt; no sidecar created by the attempt; main bytes unchanged | Ok |
| 3 | main 0440 | `ReadOnlyWriter`, same | Ok |
| 4 | UTF-16le ledger, writable (control) | `Encoding(Unsupported("UTF-16le"))` | same |
| 4 | **the same ledger made 0400** — two refusals apply | **`ReadOnlyWriter`** wins (the gate precedes `configure()`, where the encoding check lives) | `Encoding(Unsupported)` |
| 5 | writable ledger held exclusively by another connection | `Sql(DatabaseBusy)` — **busy stays busy** (184/181 route preserved) | `Sql(DatabaseBusy)` |
| 6 | 0400 **and** held exclusively | `ReadOnlyWriter` — the access-mode refusal needs no lock, so it precedes busy | `Sql(DatabaseBusy)` |
| 7 | **disclosed limit**: main 0600 inside a 0500 directory, no sidecars | not `ReadOnlyWriter`; the open fails later as `Sql(ReadOnly)` when SQLite cannot create its sidecars | — |

Rows 4 and 6 fix the precedence: *access mode → (busy / encoding / the rest of `configure()`)*. That order is defensible — it is the only check that needs nothing from the file — and it is what the README says ("BEFORE configure/SQL"). A mapper should know that a read-only UTF-16 ledger reports as read-only for writers and as unsupported-encoding for readers; both are refusals on the same public route, so nothing forks.
Row 7 is the limit the owner states ("not … a guarantee that a later write will succeed"; "Closes main fallback only"): a different cause surfaces as a different error, which is the causal behaviour 184 established.

**Regression of everything else:** my 183/184 opener probe (ten first-touch cases, both openers) run **verbatim** on 194 differs from my 184 output in exactly **one line** — the mode-0400 writer, `Ok` → `ReadOnlyWriter`. Latencies, busy/corrupt/not-a-database shapes, reader results and side effects are unchanged.

## 5. Mutation (`claude-out/probes/mutation.{py,json,log}`)

Baseline green; none failed to compile. **7 of 8 killed by the owner's tests:** gate removed; gate applied to readers; gate inverted; gate moved after `configure()` (killed by `writer_refuses_actual_readonly_fallback_before_configuration_or_sidecars` — the ordering is pinned, not just the outcome); gate on the TEMP database; refusal reported as `Configuration`; as `Path`.
**1 survives both suites:** *observation error swallowed* (`is_readonly(...).unwrap_or(false)`). I believe it is unreachable rather than untested: `sqlite3_db_readonly` fails only for an unknown schema name, and `MAIN_DB` always exists on an open connection, so there is no input that makes the `?` fire. The request's "observation errors retain Sql" is therefore true by construction and not demonstrable by a test. Not a gap worth engineering a fault seam for; worth knowing it is a claim about code shape, not behaviour.

## 6. Findings

None against the change.

### N-1 — what this gate is and is not (agrees with the owner's disclosure)
It observes SQLite's own view of the **main** file's access mode at open. It says nothing about `-wal`/`-shm` writability (row 7), about the directory, about custody, or about whether a later write succeeds; the README's r-history shows the owner met that distinction while writing the tests ("restoring main alone leaves a non-writable sidecar and BEGIN refuses Sql(ReadOnly)"). My 194 proposal's S2–S7 remain owed.

### N-2 — tests need an unprivileged runner
As in 193: as root a 0400 file is writable and the fallback does not occur. The owner states the requirement; a loud assertion is preferable to a silent pass if CI ever runs privileged.

## 7. Closure

| Finding | Status |
|---|---|
| 183 N-1, first half (READ_WRITE silently degrades to read-only; `ExistingWriter::open` returned Ok) | **Closed** — typed refusal before any SQL, no side effects, readers unaffected |
| 183 N-1, second half (sidecar creation / custody) | open; owner's 195 proposal and my sidecar note address the law, not these bytes |

## 8. Limits

One platform, unprivileged, bundled SQLite 3.53.2. I did not rebuild the owner's three compiled faults or host receipt 122, and did not test network filesystems or ACL-based write denial (mode bits only).

## 9. Verdict (bounded)

**A minimal, correctly placed gate: read-only fallback of the main file is refused for writers with a typed error before any SQL, lock or sidecar access, busy keeps its own route, readers and every other first-touch behaviour are byte-for-byte what they were in 184, and the ordering is pinned by a test. No finding.** Sidecar custody, writability beyond the main file, and cumulative readiness are not approved or implied.
