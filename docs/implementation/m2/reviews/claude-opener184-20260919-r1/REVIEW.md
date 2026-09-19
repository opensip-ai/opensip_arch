# Independent review — frozen `ledger-causal-errors-checkpoint-184`

Reviewer: Claude (independent; Codex remains owner). Date 2026-09-19. Review dir: this directory only (my 183 review's probe outputs are read, not written).
Scope: exactly the frozen 184 product bytes — narrowing the encoding error to a successful observation and keeping SQLite causes. 181 (policy) is reviewed separately. No mapper, custody, write-admission, cumulative or selection approval.

## 1. Identity verified

| Item | Result |
|---|---|
| `subject.tar.xz` | SHA-256 `dae5552d859855b100478aaa7de76a994c6e2587ecb71010963729c82a9ad836`, 4,226,824 B = request = `archive-pin.json` |
| Members | 412, all regular/safe, verified from the tar before extraction; re-verified at end |
| Product pins | 350/350; none unpinned |
| Parent | equals **my own verified 183 extraction**; 349 unchanged; only `crates/storage/src/ledger_store.rs` changed (`5ccbe7c8a9f9f448…`); fixtures unchanged |
| Host receipt 116 | 230 sources equal pins; none failed |

## 2. Owner checks re-run

Fresh scratch copy byte-equal to the product: **62 storage tests pass; strict workspace Clippy exit 0**.

## 3. The change, as read

`LedgerEncodingError` has one variant, `Unsupported(String)`. The encoding query uses plain `?`, so any SQLite failure is `LedgerError::Sql(e)` through the existing `From`. Production delta is three lines; `busy_timeout(ZERO)` stays first. Tests: held-lock assertions now expect `Sql(DatabaseBusy)`; new real first-touch failures (8 KiB non-database → `NotADatabase`; 100-byte truncated header → `DatabaseCorrupt`) with main bytes unchanged; and a transient first-query fault (`SQLITE_LIMIT_SQL_LENGTH = 1`, which later `configure` code restores) expecting `Sql(TooBig)`.

## 4. Reproduction

Byte-identical probe body to my 183 review (`claude-out/probes/opener_probe.rs.txt` → `io-184/opener.txt`), compared with that review's stored 179 and 183 outputs:

- **184 vs 179** (`io/opener-179-vs-184.diff`): the *only* differences are the four held-lock lines, and only in latency (>1 s → <1 s). Every error shape — busy, not-a-database, corrupt header, undefined encoding field, zero-byte, mode 000, mode 400, healthy — is identical to 179, as are main-file bytes and sidecar columns.
- **184 vs 183**: exactly the ten lines that 183 had relabelled `Encoding(Observation(_))` are back to `Sql(_)`.

So 184 = 179's causal shapes + 183's ordering fix + typed `Unsupported`. **183 F-1 is closed at the mechanism level**; a lock is `Sql(DatabaseBusy)` whichever statement meets it, matching the 181 owner text.

## 5. Mutation (`claude-out/probes/mutation.{py,json,log}`; baseline green; none failed to compile)

6 of 7 killed by the owner's tests: 179 F-1 re-applied; failed query silently treated as UTF-8 (killed **only** by the new transient-fault test — the owner's r1 disclosure is accurate: under a persistent fault the next statement fails anyway and hides it); failure reported as `Unsupported("")`; failure reported as `Configuration` with the cause dropped; constant in `Unsupported`; gate for readers only.

### T-1 (low) — one survivor, detected by neither the owner's tests nor my probe
"Failed encoding query treated as UTF-8 **only when the failure is busy**". With a held lock every later statement is busy too, so the opener still returns `Sql(DatabaseBusy)` and nothing observable changes; the transient-limit test does not reach it because its fault is `TooBig`. I do not claim equivalence: if a lock were released between the encoding query and the next statement, this fault would admit a ledger whose encoding was never observed. I could not build a deterministic test for that interleaving with the enabled rusqlite features, so this is reported as an untested residual, not a demonstrated escape. The production code is correct; the point is only that "no error from the encoding query is ever defaulted" is pinned for one error code, not for all. A cheap strengthening: make the transient fault generic by asserting on a small table of injected first-query failures, or assert structurally that `configure` reaches the comparison only through `Ok`.

## 6. Other observations

- **N-1:** the type doc now says what it is ("successfully observed unsupported encoding … SQLite failures stay Sql(e)"). With one variant the enum is slightly over-structured, but it leaves room for a genuinely encoding-specific unobservable case and costs nothing.
- **N-2 (carried, disclosed by the owner):** 183 N-1 — SQLite's silent read-only fallback for `ExistingWriter::open` on an unwritable file and `-wal`/`-shm` creation — is unchanged (my case 9 is byte-identical to 179/183) and is stated as owed. Agreed; not hidden.
- 180/182's "unavailable encoding observation → host-io" now has no dedicated mechanism signal; per 181 the mapper classifies by the owning condition/phase, and the SQLite code is preserved for it. Consistent.

## 7. Closure

| Finding | Status |
|---|---|
| 183 F-1 (`Observation` absorbs busy/corrupt) | **Closed** — variant removed; shapes equal 179's; tests assert neutral `Sql` causes |
| 179 F-1 (5.4 s wait) | Still closed — re-applied fault killed by both ordering tests |
| 179 W-1 (string-keyed encoding refusal) | Closed — `Encoding(Unsupported(observed))`, exact LE/BE values asserted |
| 183 N-1 | Open, tracked by owner |

## 8. Limits

Synthetic fixtures; bundled SQLite; latency bucketed at 1 s. I did not rebuild host receipt 116 or the owner's compiled mutants.

## 9. Verdict (bounded)

**No finding against the production change: it is minimal, restores 179's causal error shapes exactly, keeps 183's ordering fix, and the new transient-fault test closes a real masking gap the owner found in their own r1. T-1 is a residual test-strength note.** No approval of mapping, custody, write admission or cumulative readiness.
