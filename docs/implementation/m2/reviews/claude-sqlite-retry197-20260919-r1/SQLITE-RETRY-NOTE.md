# SQLITE-RETRY-NOTE — engine-internal WAL retries and sleeps with `busy_timeout=0`

Separate note for the 197 owner; bounded assistance, **not** a frozen review or approval. My archived 195 `REVIEW.md` is unchanged (its `hashes.txt` still verifies); this note and its evidence are covered by `hashes-with-retry-note.txt`. No candidate, product or vendor byte was edited; the engine was instrumented only as a scratch copy (diff retained, copy deleted; pinned `sqlite3.c` hash re-checked afterwards).

**Your concern is correct, and it goes beyond my 195 W-1.** W-1 named the reader's transient write lock; it said nothing about the reader itself sleeping. It does.

## 1. Source (pinned `libsqlite3-sys-0.38.2/sqlite3/sqlite3.c`, 3.53.2)

- `walTryBeginRead` l.70456; `WAL_RETRY_PROTOCOL_LIMIT 100` l.70399. From the 6th call it calls `sqlite3OsSleep`: 1 µs for calls 6–9, then `(cnt-9)²·39` µs for calls 10–100; call 101 returns `SQLITE_PROTOCOL`.
- Requested sleep sum = 4 + 39·Σ₁⁹¹k² = 4 + 39·255,346 = **9,958,498 µs** (95 sleeps; last 322,959 µs). The instrumented run counted exactly 95 sleeps / 9,958,498 µs.
- The loop is driven by `walBeginReadTransaction2` (l.70848) — and by `walBeginWriteTransaction`'s re-read (l.71343) — *inside* the engine. No busy handler is consulted, so `busy_timeout=0` cannot disable it; there is no pragma, config or file-control for it.
- `unixSleep` (l.47334): this build has neither `HAVE_NANOSLEEP=0` nor `HAVE_USLEEP`, so it takes the default `nanosleep` branch — real microsecond sleeps. (A build landing in the third branch would round every 1 µs sleep up to **one second**: ~95 s. A compile-option comparison must include these two macros, not only SETLK.)
- WAL_RETRY sources in that function: (a) BUSY from `walIndexReadHdr` while the `-shm` is **not yet mapped** → retry **unconditionally** (l.≈70519; the RECOVER lock is not consulted); (b) BUSY from `walIndexReadHdr` with shm mapped and `WAL_RECOVER_LOCK` free → retry (your l.70527 point), RECOVER busy → `SQLITE_BUSY_RECOVERY` immediately; (c) read-mark 0 / read-mark slot lock busy (l.70596, 70644, 70659); (d) header changed after the read lock was taken (l.70701).

## 2. Compile options — measured from the built product binary, not assumed

`PRAGMA compile_options` from the rusqlite-linked engine (`io/retry197.txt`, 51 options): **no `ENABLE_SETLK_TIMEOUT`**, no `HAVE_USLEEP`/`HAVE_NANOSLEEP`; `THREADSAFE=1`. `build.rs` never defines SETLK, **but** it passes `LIBSQLITE3_FLAGS` from the environment straight to the compiler (l.321–332; unset in my run, recorded). So a build environment can silently turn SETLK on; under SETLK the same loop *blocks in `fcntl(F_SETLKW)`-style waits* for up to `nDelay` per try (l.70490–70505) and `busy_timeout` semantics change. 197's "do not silently enable" therefore needs a concrete check: qualification compares the binary's `compile_options` to a pinned list and refuses a non-empty `LIBSQLITE3_FLAGS`.

## 3. Reproduction (external process holds the byte locks; all runs bounded — lockers self-exit ≤30 s and are killed when the reader returns)

`-shm` lock bytes: WRITE 120, CKPT 121, RECOVER 122, READ(0–4) 123–127, DMS 128 (checked from a third process). Reader: `READ_ONLY|NOFOLLOW`, `busy_timeout=0` verified, `query_only=ON`; timed statement is the first data query.

Product-linked engine (`probes/retry197_probe.rs.txt` → `io/retry197.txt`, `io/retry197-variants.txt`):

| Case | First data query | Result |
|---|---|---|
| C no external lock | 0.6 ms | Ok |
| B WRITE held 1.0 s | **1.030 s** | Ok — the reader *waited out* the holder |
| A WRITE held throughout | **10.48 s** | `SQLITE_PROTOCOL` (15) |
| A′ same, READ_WRITE connection | 10.48 s | `SQLITE_PROTOCOL` |
| F CKPT only | 10.50 s | `SQLITE_PROTOCOL` |
| H all five read-mark locks | 10.49 s | `SQLITE_PROTOCOL` |
| E RECOVER only | 1.8 ms | `SQLITE_BUSY_RECOVERY` (261) |
| G READ(0) only | 0.6 ms | Ok |
| D WRITE+RECOVER | 10.5 s | `SQLITE_PROTOCOL` — **I predicted 261; wrong**, see below |

Every case succeeds in <1.5 ms once the locker is gone: no damage, purely availability.

Instrumented scratch engine, same source (`c-harness/instrumentation.diff` → `io/retry197-instrumented*.txt`): A/D/F/H each show 95 sleeps, 9,958,498 µs requested, **10.49–10.57 s end-to-end** (≈0.55 s, 5 %, of lock syscalls and scheduler overshoot on an idle machine). D is explained: with no peer attached the reader is first opener, truncates `-shm` to 3 bytes, page 0 is unmapped, and branch (a) retries without looking at RECOVER. With a peer attached (DMS held shared, shm mapped):

| Case | Result |
|---|---|
| M1 valid header, WRITE held (an ordinary open write transaction) | 0.000 s Ok, zero sleeps |
| M2 valid header, WRITE+CKPT held | 0.000 s Ok |
| M3 invalid header, WRITE held (writer stalled mid header update) | 10.49 s `SQLITE_PROTOCOL`, 100 × branch (b) |
| M4 same, released after 0.5 s | 0.541 s Ok, 35 sleeps / 406,228 µs |
| M5 invalid header, WRITE+RECOVER (recovery running, shm mapped) | 0.000 s `SQLITE_BUSY_RECOVERY` |

## 4. What this means for the owner text

1. **A lawful APPEND-WRITE does not trigger it in the steady state** (M1/M2): a reader reads a valid header without any lock. The path needs an invalid/unmapped index *and* a held WRITE lock, or held CKPT/read-mark locks. Lawful occurrences are windows: a peer mid-`walIndexWriteHdr` that is descheduled/SIGSTOPped; first-attach races before the peer's recovery extends the shm; a checkpointing peer (none of ours checkpoints as a reader, the writer may). Otherwise it is a same-UID non-cooperating actor — availability only, already outside what the threat model defends.
2. **"The reader waits on no lock" is false as an engine statement** (B, M4: it outlasted the holder) and true only as an application statement. Your proposed wording draws exactly that line; I agree with it, with these precisions:
   - say "**bounded requested sleep (< 10 s on the examined build: 9,958,498 µs over at most 100 attempts per read-transaction start)**", and that **end-to-end latency has no bound** (measured +5 % idle; OS scheduling/I/O unbounded). Do not print 10 s as a deadline.
   - the bound is **per read-transaction start**, not per command: a capture that opens N transactions (ledger + each journal + the second tail observation) can incur it N times. The prescribed captures should not add their own retry on `SQLITE_PROTOCOL`/busy, as you say.
   - "each ordinary lock attempt remains nonblocking" is true here **only because SETLK is absent**; bind it to the compile-option check in §2.
   - it applies to **writers too** (A′; and l.71343) — the APPEND-WRITE busy route should expect `SQLITE_PROTOCOL` as well as `SQLITE_BUSY`.
3. **Causal preservation:** the three outcomes are distinct and should stay distinct — `SQLITE_BUSY` (5), `SQLITE_BUSY_RECOVERY` (261), `SQLITE_PROTOCOL` (15). 15 is *not* a busy code: `(rc & 0xFF) == SQLITE_BUSY` classifiers will miss it. My 183 F-1 / 184 T-1 were about the opener's error mapping absorbing classes; 197/physical work should add an explicit PROTOCOL row (availability, retryable by the *user*, never missing/corrupt/committed/not-committed). I have not checked how the current product maps 15 — owed to the frozen review that touches it.
4. **Lease interaction:** up to ~10 s of engine sleep happens *while SHARED-READ is held*, against S7's fence budget ("at most 5 seconds of fence…") which is a different clock: the lease is already held, the fence is not. Worth one sentence so nobody reads the 5 s fence bound as a total-read bound — you already say not to promise one.
5. **Qualification list additions:** cases A/B/E/F/H and M1/M3/M5 are deterministic with an external `fcntl` locker and cost ~10.5 s each for the PROTOCOL ones; M1 is the valuable negative (ordinary writer transaction ⇒ zero sleeps).

## 5. Limits

macOS, one engine build, idle machine; POSIX byte locks taken by a Python process standing in for a peer (a real SQLite peer was not stalled mid-header-write — M3/M4 *simulate* that state by zeroing the header copies). The instrumented engine was compiled with plain `cc -O1`, not the crate's flags; its sleep accounting equals the arithmetic and its timings equal the product-linked run. Linux not run. No statement about Windows.
