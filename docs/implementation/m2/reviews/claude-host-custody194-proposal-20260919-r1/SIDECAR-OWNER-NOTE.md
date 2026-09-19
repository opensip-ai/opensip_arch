# SIDECAR-OWNER-NOTE — response to the owner's proposed 195 sidecar law

Reviewer: Claude. 2026-09-19. **Assistance only**; separate from, and not a change to, `REVIEW.md` in this directory (its `hashes.txt` still verifies). Not a frozen review, not approval; no candidate edited; no 195 draft inspected — only `sidecar195-owner-proposal.md` (copied as read under `claude-out/`) and three follow-up chat instructions (keep pre-Step-0 admission strictly write-free; scope any exception to Step 0+ under the admitted SHARED-READ lease; reconcile readonly l.120/244/372 as well as l.141–145; consider a verified `SQLITE_DBCONFIG_NO_CKPT_ON_CLOSE` for every reader).
Evidence: `claude-out/sidecar195_probe.rs.txt` (scratch copy of the verified 191 product, storage crate) → `claude-out/io/sidecar195.txt`. Engine: the **pinned** bundled SQLite 3.53.2 (`libsqlite3-sys 0.38.2`, amalgamation `sqlite3.c`; line numbers below are in that file), rusqlite 0.40.2, macOS.

## 0. Corrections to my 194 report that the owner is right about

1. **WAL is not a disposable index/lock file.** My option (ii) called `-wal`/`-shm` "SQLite-owned lock/index carriers". Wrong for `-wal`: it can hold **committed, un-checkpointed data**. Probe A: a ledger whose WAL held two committed rows and whose main file did not — the reader saw 3 rows, i.e. it read committed data *from the WAL*. Any law must treat an existing WAL as evidence to be preserved, never as scratch.
2. **Authorized groups.** I wrote that after chain custody "the only principals able to [substitute] are the invoking uid and root". S3 also admits directories group-writable by an **explicitly authorized** gid (`--trust-group`). The correct statement is: invoking uid, root, **and members of any explicitly authorized group**; the last are trusted by an explicit invocation-time grant recorded in provenance, not by the TCB sentence. My 191 probe row 5 shows exactly that admission.
3. **`SQLITE_FCNTL_FILE_POINTER` does not yield a native fd portably.** It returns `sqlite3_file*`; the fd lives in the private `unixFile` layout. My option B ("→ unix fd → `fstat`") overclaimed. An `unsafe` handle call does not cross that boundary; only a VFS the project itself supplies (option C) would know its own descriptors. Option B should be read as "not available through any public interface".
4. **B/C do not defeat same-UID in-place modification**, and nothing should be read as requiring that. Agreed; §4 of the report already says no sequence of samples changes what an in-TCB actor can do, and that applies equally to a true-identity check.

## 1. What a read-only connection of the pinned engine actually writes (measured)

Setup for A–D: WAL ledger, `wal_autocheckpoint=0`, the writer closed with `NO_CKPT_ON_CLOSE` so the **WAL holds committed rows** and no connection is open. Reader = `READ_ONLY | NOFOLLOW`, as the product opens it.

| # | Case | main | `-wal` | `-shm` |
|---|---|---|---|---|
| A1 | reader as configured today (`query_only=ON`), `BEGIN`, read, `COMMIT`, **closes as the last connection**, `NO_CKPT_ON_CLOSE` not set | **byte-identical** before / during / after | **byte-identical** (8,272 B) | **bytes changed during the read and stay changed** (same size) |
| A2 | same with `NO_CKPT_ON_CLOSE = true`, read back `Some(true)` | identical | identical | changed |
| A3 | plain `READ_ONLY`, neither setting | identical | identical | changed |
| B | a **writer stays connected**, sidecars pre-exist, reader comes and goes | identical | **unchanged by the reader** | **changed by the reader** |
| C | reader issues `PRAGMA wal_checkpoint(TRUNCATE)` | unchanged | unchanged | — (statement fails "disk I/O error") |
| D | `-shm` **absent**, WAL holds committed rows (crash leftovers) | unchanged | unchanged | **created (32 KiB) and populated** — the reader rebuilt the wal-index; it saw all 3 rows |
| 194 r.2 | both sidecars absent, clean ledger | — | **empty `-wal` created** | created; both remain after close |
| 194 r.2 | same, directory not writable | read fails "attempt to write a readonly database"; nothing created | | |

## 2. Answers to the owner's questions

**"Are SHM updates possible even with existing sidecars, making the persistent-WAL option insufficient to retain a literal no-write claim?" — Yes (row B).** A reader records its snapshot in the wal-index: `walTryBeginRead` (l.70456) stores read marks with `AtomicStore(pInfo->aReadMark+i, mxFrame)` (l.70632; also l.69678), and when the index is missing or stale it runs `walIndexRecover` (l.68826, called at l.70166) which rewrites it (row D). These are writes to the mmapped `-shm` file's **content**, in addition to the byte-range locks. So *no* configuration — persistent WAL, pre-created sidecars, `query_only` — yields a literally write-free reader in WAL mode. The honest claim is "no write to main, none to WAL content; `-shm` read-mark/index state is updated".

**"Does read-only/`query_only` suffice alongside custody and the pinned engine, or is there an unavoidably broader side effect?"** The unavoidable set is exactly three things, and I found nothing broader:
1. `-shm` content updates (always);
2. **creation of `-shm`** when absent — `unixOpenSharedMemory` opens it `O_RDWR|O_CREAT|O_NOFOLLOW` (l.45220) unless `readonly_shm=1`, which the product cannot pass (URIs are refused, `ledger_store.rs` l.43);
3. **creation of an empty `-wal`** when absent — `sqlite3WalOpen` always uses `SQLITE_OPEN_READWRITE|SQLITE_OPEN_CREATE|SQLITE_OPEN_WAL` (l.69161), even for a read-only connection.
`query_only=ON` adds nothing to those three (A1 vs A3 identical) — it blocks SQL-level writes, which `READ_ONLY` already blocks — but it is still worth keeping as the statement-level guard it is. Note what the reader holds: a **writable** WAL descriptor and a writable SHM mapping. It does not *use* the WAL descriptor to write in any case I could construct (A, B, C, D: WAL bytes identical), but the capability exists, which is the reason to pin the engine and to keep §3's close-time rule.

**"Is last-reader close ever allowed to delete/truncate WAL when a READ_ONLY connection uses a writable WAL handle?"** In the pinned source the path exists and is blocked by one condition. `sqlite3PagerClose` passes the checkpoint buffer unless `SQLITE_NoCkptOnClose` is set (l.63794); `sqlite3WalClose` then checkpoints, and deletes or truncates the WAL, **only if** `sqlite3OsLock(pWal->pDbFd, SQLITE_LOCK_EXCLUSIVE)` succeeds (l.69964–65; delete at l.69982/69999, truncate at l.69990). For a `READ_ONLY` connection the main descriptor is `O_RDONLY`, a POSIX write lock on it fails, and nothing happens — measured in A1 and A3: last reader closed over a WAL with committed content, WAL and main byte-identical. So today's behaviour is safe, **but it is safe by an OS locking side effect on a read-only descriptor**, not by any statement of intent.
**I therefore agree with the owner's suggestion: require `SQLITE_DBCONFIG_NO_CKPT_ON_CLOSE = true`, set and read back, on every reader before any SQL.** It is a safe public API (`Connection::set_db_config`, already used by `configure()` for three other options), it turns "cannot checkpoint because the lock fails" into "does not try" (l.63794), A2 shows it changes nothing else, and it removes a dependency on the 183 N-1 fallback direction: a reader that was somehow handed a *writable* main descriptor would otherwise checkpoint and delete the WAL on close. It belongs in the same verified `set_db_config` loop, with a test that a last-reader close over a non-empty WAL leaves main and WAL byte-identical.
Related and worth the same treatment: **the reader must never issue a checkpoint** (C shows it fails with a generic I/O error rather than a typed refusal; the law should forbid the statement, not rely on the failure).

## 3. The proposed owner law, clause by clause

| Clause | Assessment |
|---|---|
| keep read-only recovery free of semantic/durable product mutation | agrees with every measurement: main and WAL content untouched in A–D |
| permit the pinned engine's bounded operational side effects: **creation of an empty missing WAL** and **creation/update of SHM** read/index/lock state | this is exactly the measured unavoidable set (§2). Two precision points: (a) say "**empty**" as a checked post-condition — a WAL the reader caused to exist must be 0 bytes (row 194-2: it is) and must stay so for the reader's own lifetime unless a lawful appender writes it; (b) "SHM … update" must explicitly include **rebuilding a missing index from an existing WAL** (row D) — that is a recovery-shaped act by SQLite and a reader will do it; if the owner does not want that, the only alternative is to refuse when `-wal` is present and `-shm` absent, which I would not recommend (it makes every crash leftover unreadable) |
| require admitted custody for the directory and pre-existing files before calling SQLite | matches 194 §5.0. Add: the directory must be **writable by the reader** for the absent-sidecar case, or the open fails with a misleading "attempt to write a readonly database" (row 194-2) — classify that as a custody/IO refusal, not corruption |
| no application-created sidecars, SQL writes, main modifications, checkpoint/truncation/deletion, replacement of an existing sidecar, schema/marker/witness/floor changes | all consistent with measurement. "No checkpoint/truncation/deletion" is where `NO_CKPT_ON_CLOSE` belongs (§2). "No replacement of an existing sidecar": SQLite opens existing sidecars with `O_NOFOLLOW` and never replaces them; the identity bracket (194 §5 step 9, corrected) is the detection |
| preserve all existing WAL content; fail if the engine needs a write outside this exception | good. Testable form: main and `-wal` byte-identical across the reader's whole lifetime **when no appender is active**; under an active appender only main/WAL *identity* and "WAL never shrinks or is replaced while we hold the snapshot" can be asserted (194 row 7: WAL size changes lawfully) |
| the exception does not waive missing application lease/fence/carrier refusal | essential, and it is the distinction the follow-up instruction draws: see §4 |
| active appenders may change WAL; comparisons must respect concurrency | agreed; 194 §7 "never compare `-wal` size or mtimes" |

## 4. Scoping to Step 0+ and reconciling the readonly owner

The follow-up instruction is right and I would make it structural:

- **Pre-Step-0 admission stays strictly write-free** (R readonly l.141–145: "creates or mutates no durable file, row, registry, binding, lease carrier, trust state, witness, floor or quarantine marker … creating missing carriers or making an installation usable is not [allowed]"). Nothing in admission needs SQLite: fence, registry, store binding, lease acquisition, and — new — the 194 location admission (chain, main-file and sidecar *observation*) are all descriptor reads. **No SQLite call before the SHARED-READ lease is held and Step 0 begins.** That keeps l.141–145 literally true and needs no edit there beyond, at most, a pointer.
- **The exception attaches only to the §2 reader, Step 0 onward, under the admitted SHARED-READ lease**, and it must be reconciled with three more sentences, each of which is currently absolute:
  - **l.120–123** (carrier stage): "creates or initializes no carrier and **writes nothing** on any of these paths" — the security carrier is a SQLite database too (`journal_store.rs` l.409, `READ_ONLY`); if it is in WAL mode the same three side effects occur there. The exception must either cover the carrier explicitly or the text must state the carrier's journal mode makes it inapplicable (my 194 row 2c: a rollback-journal database creates nothing). I have not checked which mode carriers use — that is an owner fact to state.
  - **l.244–249** ("Read-only throughout Steps 0 onward. Prohibited for that entire reader: … any `BEGIN IMMEDIATE`; any `INSERT`/`UPDATE`/`DELETE` … any wait on any lock"): the prohibitions are all *application* acts and stay intact; add that SQLite's engine-internal sidecar effects of §2 are the single enumerated exception and that a reader-issued checkpoint is prohibited.
  - **l.372–374** ("No lock, no wait on the writer, **no mutation**"): "no lock" is already not literally true of SQLite (shared byte-range locks on main and `-shm`); "no mutation" needs the same enumerated exception. Suggest "no application lock, no wait, no mutation other than the engine-internal sidecar state enumerated in …".
- Name the exception once, in one place, as a closed list (empty-WAL creation; SHM creation; SHM read-mark/index update including rebuild from an existing WAL), bind it to the **pinned engine version**, and have the other sentences cite it. A future SQLite upgrade then has an obvious re-qualification obligation: re-run rows A–D.

## 5. Tests that would make the law executable (all are rows above)

last-reader close over a non-empty WAL: main and WAL byte-identical, with and without an appender · `NO_CKPT_ON_CLOSE` set and read back on every reader before SQL; refusal if the read-back is not `true` · reader-issued checkpoint is refused by the product before reaching SQLite · absent sidecars + writable directory: empty WAL (0 B) and SHM appear, main unchanged · absent sidecars + non-writable directory: typed IO/custody refusal, nothing created · `-shm` absent + WAL with committed rows: reader sees the rows, WAL and main unchanged · ordering spy: no SQLite call before the lease is held · the same set against the security carrier, or a test that pins the carrier's journal mode.

## 6. Limits

One platform (macOS), one engine build; byte comparisons of `-shm` are of the file as read back through the filesystem, which for an mmapped file reflects the mapping on this OS but is not guaranteed to on every filesystem. I did not test a reader handed a writable main descriptor (the case `NO_CKPT_ON_CLOSE` defends against) because the product never opens one; I did not examine carriers' journal mode; I did not test big WALs, multiple concurrent readers' read-mark slot contention, or `SQLITE_FCNTL_PERSIST_WAL`. Nothing here is approved or selected.
