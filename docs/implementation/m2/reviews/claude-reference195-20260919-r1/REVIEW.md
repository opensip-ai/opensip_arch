# Independent review — frozen `sqlite-sidecar-reference-checkpoint-195`

Reviewer: Claude (independent; Codex remains owner). Date 2026-09-19. Review dir: this directory only.
Scope: exactly the frozen 195 reference bytes — an **owner decision in prose** (five documents): the closed SQLite reader side-effect exception, the before-SQL / before-query control sequence, and retained operational file custody. My 194 proposal and `SIDECAR-OWNER-NOTE.md` were assistance, not acceptance; this review reconciles them with the exact text and tests the text's factual claims against the pinned engine. It is **not** approval of any physical implementation (196 is separate), nor cumulative approval.

## 1. Identity verified

| Item | Result |
|---|---|
| `subject.tar.xz` | SHA-256 `4a59f51df11993c22f97a665d2c9acf05b0ce4d8328b06de22c3afa09a6facfa`, 2,226,312 B = request = `archive-pin.json` |
| Members | 1,442, all regular/safe, verified from the tar before extraction; re-verified at end |
| Candidate pins | 1,299/1,299; none unpinned; declared change list equals computed |
| Parent | equals **my own verified 192 extraction**; 10 changed: five owner documents + five manifests; **91/91 Python byte-identical**, as are all schemas, SQL, models and fixtures (unchanged pins) |
| Behaviour unchanged | beyond the pins: my `sweep`, `binding` and `phasec` probes re-run on this tree are byte-identical to my 192 outputs |

## 2. Owner checks re-run

Reference order, `-I -B`, fresh outputs: all seven lanes exit 0; integration 1,787 / 0 failed, carrier 479 / 0 failed (my run). As the README says, none of these executes a SQLite side effect.

## 3. The factual claims of the text, tested on the pinned engine

`claude-out/probes/effects195_probe.rs.txt` (scratch copy of my verified 194 product; bundled SQLite 3.53.2) → `io/effects195.txt`.

| Claim in 195 | Measured |
|---|---|
| "Creation of an **empty** missing `-wal`" | after a reader's first database query on a clean ledger with no sidecars: `-wal` **0 B**, `-shm` 32,768 B, main hash unchanged. *(Disclosure: my sidecar note asserted "0 bytes" citing a row that had only recorded existence; this is the first time I measured the size. It was right.)* |
| the prescribed sequence is **possible in that order** without touching the database: `READ_ONLY` open → `is_readonly` → `NO_CKPT_ON_CLOSE` set + read-back → `busy_timeout(0)` via API → `PRAGMA query_only=ON` → verify `query_only`/`busy_timeout` → data | step by step, **no file-system effect of any kind** until the first database-touching statement; both pragmas are connection-control only. `is_readonly` = true, config read-back = true, `query_only` = 1, `busy_timeout` = 0 |
| "A failed control check refuses without proceeding to reads; the engine must not attempt a close-time checkpoint on that refusal path" | open + API check + close with **no SQL**, over a ledger whose WAL holds committed rows: main, `-wal`, `-shm` all byte-identical. The WAL is never opened on that path, so there is nothing to checkpoint |
| SHM is written even with existing sidecars; index rebuild from an existing WAL; main/WAL untouched by a reader incl. last-reader close; reader-issued checkpoint fails | all measured in my sidecar-note probe (`…194-proposal…/claude-out/io/sidecar195.txt`), unchanged engine |

So the text is physically accurate for this engine build, and its ordering is achievable.

## 4. Reconciliation with my 194 proposal and sidecar note

| Item | 195 | Assessment |
|---|---|---|
| WAL is evidence-bearing, never scratch | stated in three owners | agrees with the correction the owner made to me |
| explicit-group principals | S7: "Root, the invoker and explicitly authorized group members can change their own permissions or files… group grants retain their invocation-time provenance" | agrees |
| no native fd from `FILE_POINTER`; `HAS_MOVED`/path/reported path ≠ descriptor identity; no VFS selected | S7 | agrees; nothing overclaimed |
| exception scoped to Step 0+, under the held SHARED-READ lease; admission stays write-free | readonly §2 and l.141–145 ("creating missing **application** carriers…"; "does not authorize any admission-time file creation") | agrees with the follow-up instruction |
| l.120, l.244, l.372 reconciled | all three edited; each now points at the single §2 exception; "No new application lock… Engine-internal nonblocking SQLite read locks are not additional lifecycle/project leases" | done; one exception, cited, not restated |
| `NO_CKPT_ON_CLOSE` verified before SQL; reader-issued checkpoint prohibited | both present | agrees |
| three-way sidecar observation; pre-open sample is not an identity baseline; baseline after snapshot; recheck before release; lease through consumption | present, in those words | agrees (this was my own correction after measuring) |
| **owner refinement: no post-open WAL-zero or size-monotonic assertion** | "The empty-WAL creation rule constrains this reader's engine effects, not a later file size… do not require identical main/WAL/SHM bytes, sizes or timestamps… or infer corruption from a changed WAL size" | **the owner is right and my note was too strong.** I had suggested asserting "WAL never shrinks or is replaced while we hold the snapshot". A reader whose snapshot needs no WAL frames does not pin the WAL; a lawful appender may then restart or reset it. Snapshot isolation, not file bytes, owns consistency |
| owner refinement: no global ban on SQLite before the lease — only ledger and journal | "Installation registry/trust/transition observations before the lease retain their separate write-free admission law" | coherent; correctly leaves that implementation owed rather than pretending it is covered |
| operational-file scope without the 4 MiB cap (my B-4) | S7: regular, not a symlink, one hard link, same owner/mode/ACL predicates, no waiver, "each operational role retains its own byte/read limits, and no unlimited read is granted" | closes B-4 as an owner statement |
| empty chain refuses (my 193 N-1) | S7: "An empty chain is not a successful observation" | law stated; implementation is 196 |
| B-2/B-3 edges | build plan: implement the planned `storage→security` and `lifecycle→storage` edges; "do not duplicate custody predicates in storage or add a reverse… edge" | deliberate, as asked |
| B-5 Linux, B-6 local filesystem, B-7 identity, B-8 layout | all named as owed ("Admitted local-filesystem/mount behavior, actual location relationships… remain separate required checks"; build plan: "bind ledger, security carrier, witness, floor and lease locations to the same admitted… layout. Independent caller-supplied paths do not establish that relation") | honestly open |

## 5. Findings

No contradiction between the five documents, no impossible ordering, and no grant I could not ground in the existing threat model (the exception gives the *engine* three effects inside a custody-checked directory under a cooperating lease; it gives the application nothing). Two low points and notes:

### N-0 (note; drafted as a finding, withdrawn on checking) — where "the security journal is a WAL database" is owned
§2 opens: "The §2 reader uses an existing admitted **WAL** database for the project ledger **and for each security-journal capture, including inherited/current carrier dispatch**." My first draft called the journal half an unstated premise. **That was wrong, and I caught it only because I re-checked my own citation before finishing**: the draft cited a search log I had not saved. The saved search (`claude-out/io/wal_premise_search.txt`, every `WAL`/`journal_mode` occurrence in the frozen docs) shows the pinned `security-completion.v1.md` §5.4: "`grant-journal.sqlite`, opened WAL with `synchronous=FULL`". `carrier-format.v3.md` l.62–66 names exactly that section as the carrierFormat 1 owner, and v8 §5.4 carries "Encoding, DDL… as v2 §5.4" (v2 is not in this tree; v1 and v8 are). Since WAL was law from format 1, inherited carriers are covered too, and the product agrees (`journal_store.rs` l.463 checks `journal_mode`).
What remains is small: the statement lives only in the historical v1 lineage, reached through a v2 that this tree does not contain; neither `carrier-format.v3.md` nor the security contract repeats or cites it, while the ledger's WAL mode *is* stated in the current contract (S7 lock table, level 3). Since 195 now hangs an exception on the mode, one citing sentence in the current carrier owner — plus the disposition of a non-WAL carrier (refusal, as the product does) — would make the premise findable. Not a contradiction.

### W-1 (low) — the "read/coordination locks" include a transient **exclusive WAL write lock**
Item 3 allows "engine-internal nonblocking read/coordination locks needed for this snapshot". When the wal-index must be (re)built, `walIndexReadHdr` takes `walLockExclusive(pWal, WAL_WRITE_LOCK, 1)` before `walIndexRecover` (pinned `libsqlite3-sys-0.38.2/sqlite3/sqlite3.c`, 3.53.2: function at l.70096; the `WAL_WRITE_LOCK` acquisition and the `walIndexRecover` call are l.70150 and l.70166). So a *reader* can momentarily make a lawful APPEND-WRITE see `SQLITE_BUSY`. With `busy_timeout=0` on both sides nothing waits, S7's "never [blocking] for readers" stays true, and the writer's existing busy route handles it (my probe: a commit immediately after a rebuild succeeds). But "read lock" undersells it; say that index rebuild takes the engine's WAL write lock briefly and that a concurrent appender's busy result in that window is lawful and causal, not a custody signal.

### W-2 (low) — which readers the exception covers, and report-only surfaces
The readonly owner scopes the exception to "the §2 reader"; S7 says "the project ledger and security-journal **readers**". Other SHARED-READ consumers of the same ledger (`query`, `inspect`, `doctor` project checks, agent-serve requests) incur identical engine effects. If S7's plural is meant to cover them, the readonly owner should say the exception is the property of *any* admitted SHARED-READ ledger/journal reader, not only recovery. Conversely the fence-only report-only surfaces — workflows l.1746 "`doctor`, `trust doctor` and `store status` retain their existing diagnostic projection and **write nothing**"; S7 lease map "(report-only, no write)" — hold **no** project lease and so have no exception: they must not open these WAL databases (or must take SHARED-READ first). One sentence either way prevents a `store status` implementation from quietly creating sidecars under a "writes nothing" contract.

### N-1 — consequence for 196 (not a defect here)
In today's product `configure()` the first database-touching statement is `PRAGMA main.encoding` (that is exactly where my probe sees the sidecars appear), and `query_only=ON` is set later. 195 requires `query_only` before any data/schema query. The reorder is compatible with 184 (busy timeout first) and 180 (encoding before domain text); 196 should carry an ordering spy like 194's.

### N-2 — qualification clause is the right shape
"Qualification must pin the SQLite engine/build, VFS and platform… A future engine, VFS or platform change requires this effect qualification again… Pure reference tests and successful configuration calls alone do not discharge these obligations." The listed tests are the rows I measured, asked for separately for ledger and journal readers. Nothing to add except W-1's window as a concurrency case.

## 6. Limits

An owner-text review plus an engine fact-check on one platform and one engine build. No reference lane executes these obligations, so nothing here is differential. I did not re-read unaffected sections of the five documents beyond a tree-wide scan for absolute "writes nothing / no write / write-free" statements (hits classified in §5 W-2; the sweep table's "no write" rows are about settlement writes by a lease-holding writer and are unaffected). I did not examine what `store status` or `trust doctor` actually read.

## 7. Verdict (bounded)

**The decision is coherent across all five owners, physically accurate for the pinned engine (empty WAL = 0 B; the control sequence touches nothing before the first database query; a no-SQL close is inert), correctly scoped to Step 0+ under the lease with admission still write-free, and it adopts the corrections to my assistance while rightly rejecting my over-strong WAL-size suggestion. No blocking finding. W-1 and W-2 ask for precision about one lock and about which readers are covered; N-0 asks only for a citation (the journal's WAL mode is owned by the historical v1 §5.4, which I first missed).** No approval of a physical implementation, of 196, or cumulative readiness.
