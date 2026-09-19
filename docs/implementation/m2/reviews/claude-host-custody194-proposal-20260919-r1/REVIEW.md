# Proposal assistance — 194: SQLite main/WAL/SHM path custody and lease-held capture

Reviewer: Claude. 2026-09-19. **Assistance only** — not a frozen review, not approval, not a design decision; the owner reviews before choosing. No candidate, product or repository file was edited; nothing installed, committed or pushed; no other agent used.
Trees read (both verified in my own reviews): product = `claude-custody191-20260919-r1/…/product` ("P"); reference = `claude-reference192-20260919-r1/…/candidate` ("R"). Line numbers are in those trees.
Request: first received as a chat message, then as `host-custody194-proposal-20260919-REQUEST.md` (both reproduced under `claude-out/`); this report was extended after reading the file — §2 rows 6–7, §3.1, §5.0, §5 step 9 (corrected), §7 and §8 are the additions. r1 of the probe and its output are preserved.
Probe: `claude-out/sqlite_custody_probe.rs.txt` appended to a **scratch copy** of P's `crates/storage/src/lib.rs`, run once → `claude-out/io/sqlite_custody.txt` (bundled SQLite 3.53.2, rusqlite 0.40.2, macOS). The scratch build tree is kept beside it; its target directory was removed.

## 0. Short answers

1. **Can a public SQLite API retain or verify the identity of the file SQLite opened, without `unsafe` outside platform? No.** rusqlite's only route to the underlying handle is `pub unsafe fn handle()` (rusqlite `lib.rs` l.952); `Connection::path()` (l.632) and `PRAGMA database_list` return a *name*. `SQLITE_FCNTL_FILE_POINTER`/a custom VFS would work but are FFI, so they would have to live in `opensip-platform`. What safe APIs *can* do is bracket the open with identity samples taken through the platform's retained directory; that detects a persistent substitution and is blind to ABA (measured, §2 row 5).
2. **READWRITE read-only fallback is detectable with a safe public API**: `Connection::is_readonly("main")` (rusqlite l.1075) returns `true` for a 0400 ledger opened `READ_WRITE` — and `BEGIN IMMEDIATE` *succeeds* on it, so the transaction is not a usable test (§2 row 1).
3. **Sidecars: a read-only connection on a cleanly checkpointed WAL ledger creates `-wal` and `-shm` and leaves them behind** (§2 row 2). That is in tension with the reader law "creates or mutates no durable file… creating missing carriers … is not [allowed]" (R `commit-recovery-readonly.v3.md` l.141–145). It needs an owner decision (blocker B-1); I give the options, not a choice.
4. **Same-UID actors cannot be excluded by any of this, and the owners already say so** (§4). What directory-chain custody *does* buy, grounded in S3, is that every principal able to rename or replace anything on the path is the invoking uid or root — i.e. inside the stated TCB.
5. **Smallest next integration**: one private storage-crate admission step for an existing ledger location (chain custody → main-file custody → sidecar observation → open → `is_readonly`/mode gates → identity bracket), reusing 191 and the 149 bracket pattern, plus nothing public. Lease-held capture is a second, separate step that is currently blocked by crate layering (B-3).

## 1. What exists today (P)

| Component | Fact | Where |
|---|---|---|
| Ledger opener | absolute, normal components only; `symlink_metadata().is_file()`; `READ_ONLY`/`READ_WRITE` + `NO_MUTEX` + `PRIVATE_CACHE` + `NOFOLLOW`; then `configure()` (busy 0, UTF-8, limits, `query_only` for readers, WAL required). Comment: "Ancestor/inode custody throughout SQLite and its sidecars is a supplied precondition, not established by this metadata sample or NOFOLLOW" | `storage/src/ledger_store.rs` l.42–58, l.59–, l.107– |
| Carrier opener | same shape, read-only only | `security/src/journal_store.rs` l.409–431 |
| Retained directory chain | `RetainedDirectoryPath::open`, `recheck()`, `observe_directories()`, `directory()` | `platform/src/filesystem/path_binding.rs` l.76, l.130, l.138, l.150 |
| Open a regular file *relative to a retained directory* | `RetainedDirectory::open_regular(relative)` — `openat`, `O_NOFOLLOW`, returns `std::fs::File`; identity via safe `MetadataExt` | `platform/src/filesystem.rs` l.113 |
| Descriptor observation (metadata + ACL writers, macOS; Linux `UnsupportedPlatform`) | `observe_descriptor` | `platform/src/filesystem.rs` l.1372 |
| Chain policy | `inspect_directory_path` (private, no caller; 193 will scope it) | `security/src/custody.rs` l.397 |
| File-scope predicate | `Scope::ConfigurationFile` = regular, link count 1, **≤ 4 MiB**; `Scope::Directory` | `security/src/custody.rs` l.33–36, l.112–118 |
| Bracketed capture precedent | before/after operational-bytes observations around one SQL snapshot | `security/src/journal_store/bracketed_capture.rs` (my 149 review) |
| Leases | private composition "over **supplied** installation and namespace handles… asserted custody inputs" | `lifecycle/src/leases.rs` l.1–3 |
| Crate edges | `storage → identity, platform`; `security → evaluator, identity, platform`; `lifecycle → platform`; `host → contracts, evaluator, identity, platform, reporting`. **Nothing depends on both storage and lifecycle, or on storage and security** | each `Cargo.toml` |

## 2. Measured SQLite behaviour (`io/sqlite_custody.txt`)

| # | Case | Result |
|---|---|---|
| 1 | `READ_WRITE` open of a 0600 / **0400** ledger | both `Ok`; `is_readonly("main")` = `false` / **`true`**; `BEGIN IMMEDIATE` `Ok` in **both**; `path()` equals the supplied path |
| 2 | reader, WAL ledger, **no sidecars on disk**, directory 0700 | read ok; `-wal` and `-shm` **created, and still present after close** |
| 2 | same, directory 0500 | read fails "attempt to write a readonly database"; nothing created |
| 2b | reader, sidecars **already present**, directory 0500 | read ok |
| 2c | reader on a rollback-journal ledger | read ok, nothing created (but P requires WAL) |
| 3 | `NOFOLLOW`: symlink as leaf; symlink as an **ancestor directory** | both refused — SQLite applies it to the whole path (hence the canonical-path requirement I hit in 155) |
| 4 | `-wal` pre-planted as a symlink to another file, writer with `NOFOLLOW` | open refused; **0 bytes written through the symlink** |
| 5 | identity bracket via `open_regular` before/after, **persistent** swap | detected (inode differs) |
| 5 | **ABA**: impostor in place only while SQLite opens, original restored before the second sample | **not detected**; chain `recheck()` also says unchanged; SQLite is reading the impostor and no safe API can say so |
| 6 | **writer** on a cleanly checkpointed WAL ledger | no sidecars after open with no statement; `-wal`+`-shm` appear at the **first write**; when the writer is the last connection to close they are **removed** |
| 6 | writer closes while a reader is open; the **read-only connection closes last** | sidecars **remain** — a read-only last closer cannot remove them |
| 7 | lawful concurrent APPEND-WRITE (200 commits + passive checkpoint) while a reader holds its snapshot | reader's result unchanged (snapshot stable); main inode, size and mtime unchanged; `-wal` inode unchanged but **size changed**; `-shm` inode unchanged |

## 3. Identity: what is possible at each level of cost

| Option | Needs | Gives | Verdict |
|---|---|---|---|
| A. Bracket: `open_regular(main)` → (dev, ino, nlink, uid, mode) **before** the SQLite open; hold that `File`; open SQLite; establish the snapshot (first read inside `BEGIN`); sample again + chain `recheck()` | safe std + existing platform API | detects persistent substitution and any change visible at the second sample; not ABA | **smallest; do this** |
| B. Platform FFI: `sqlite3_file_control(SQLITE_FCNTL_FILE_POINTER)` → unix fd → `fstat`, compared with A's sample | `unsafe` in `opensip-platform`, and a way to pass rusqlite's raw handle across (rusqlite's `handle()` is itself `unsafe`, so storage would need an `unsafe` call or platform would need a rusqlite dependency) | true identity of SQLite's main fd (not the sidecars') | real fix for main-file ABA; **not** small; conflicts with storage's no-unsafe posture — owner decision |
| C. Platform VFS shim opening main/WAL/SHM via `openat` on the retained directory | a registered VFS in platform (FFI) | identity for all three by construction | the architecturally complete answer; largest |
| D. `/dev/fd/N` or `immutable=1` URI tricks | — | sidecar names derive from the path string → WAL broken; `immutable` is wrong with a live writer; P refuses URIs anyway (l.43) | rejected |

### 3.1 `SQLITE_FCNTL_HAS_MOVED` specifically
- **Not reachable safely.** rusqlite 0.40.2 has no public `file_control`; the only `FCNTL` use in its source is an internal `SIZE_LIMIT` in `serialize.rs`. The constant exists in `libsqlite3-sys`, so using it means `sqlite3_file_control(conn.handle(), …)` — two `unsafe` steps, neither allowed outside platform, and platform has no rusqlite dependency today.
- **Not complete identity even if reachable.** The unix VFS answers "does the path I was opened with still name my inode?" at one instant, for the **main file only**. It does not bind SQLite's descriptor to the inode *we* admitted: with HAS_MOVED = 0 at t1 and our retained-directory sample = X at t2, an ABA between t1 and t2 still leaves SQLite on an impostor. It says nothing about `-wal`/`-shm`.
- **Unsupported providers must fail closed.** A VFS that does not implement the opcode returns `SQLITE_NOTFOUND`; that, and any error, has to be a typed "identity unobservable" refusal, never "not moved". If the owner ever adopts it, it is a *supplementary* check under option B, not a substitute for it.

I recommend **A now**, with the doc comment saying exactly what row 5 shows, and B/C recorded as the owed route to closing 124 F-1 for SQLite. A is honest only if it never uses the words "same file as SQLite opened".

## 4. What cannot be guaranteed against same-UID actors — and the owner text that already says so

- R `security-completion.v8.md` §1 (l.98–100): the TCB includes "first-party trusted code running with the invoking user's ambient authority; the host itself runs unprivileged".
- R `03-configuration-and-security.md` l.136: "Host brokers used voluntarily by an unconstrained same-user process do not create confinement."
- R `commit-recovery-readonly.v3.md` l.225–227: the lease is "cooperating protocol exclusion, not proof against arbitrary external filesystem mutation, path replacement or ABA; physical custody checks remain required."
- P `custody.rs` doc (191): samples "do not exclude ABA, concurrent permission changes, mount substitution or writes after return."

Concretely, a process running as the invoking uid (or root) can, at any time and without touching a lease: rename/replace the ledger or a sidecar, including ABA inside any sample window; edit bytes in place; chmod an ancestor between samples; drop and re-create a trigger (187 N-2); delete `-shm`; truncate `-wal`; hold or ignore the advisory `flock` leases (`platform/src/locks.rs` l.14–17 says as much). **No sequence of samples changes that, and the plan must not say it does.**
What S3 custody *does* establish — and this is the grounding for the gate, not a new policy — is the converse: if every directory from `/` to the ledger's parent passes S3 "Custody of a directory" (R `security-and-lifecycle.md` S3: owner is the invoking uid or root; no other-write; no group-write unless the gid is explicitly authorized; no ACL write grant to anyone else; ACL readable) and the three files are owned by the invoker with no foreign write path, then **the only principals able to perform any of the substitutions above are the invoking uid and root**, which the threat model places inside the TCB. So the honest claim is: *at the sample instants, no principal outside the TCB had a DAC path to substitute or modify these files.* It is a statement about who could, not about what happened, and it lapses the moment an in-TCB actor changes a mode.

## 5. Proposed smallest integration (storage crate only; private; no public policy)

### 5.0 What must be admitted *before* SQLite is called (the answer in one list)
(1) path grammar and a single-component leaf; (2) the parent chain retained, every ancestor passing the operational chain predicate; (3) the supplied local-filesystem precondition recorded as *supplied* (B-6); (4) the main file opened relative to the retained directory, held, and passing the file predicate (regular, one link, owner, no foreign write path); (5) each sidecar classified present / absent / unobservable, present ones passing the same predicate; (6) the absent-sidecar decision applied (B-1) — for a reader this is where a no-write admission either refuses or knowingly lets SQLite create two files inside the directory it has just custody-checked; for a writer creation is expected (row 6: at the first write, not at open); (7) when composed with leases (§7), the lease guard already held and the ledger's parent directory proven to stand in the owner-stated relation to the namespace lease directory (B-8). SQLite is called only after all seven.

A private `ledger_location` admission used by both `ReadSnapshot::open` and `ExistingWriter::open`, replacing `existing_path`'s single `symlink_metadata` sample. Steps, each mapped to an existing owner:

1. **Path grammar** — unchanged (l.46–52). Split into canonical parent + leaf name; the leaf must be a single normal component.
2. **Retain the parent chain** — `RetainedDirectoryPath::open(parent, bound)`. Owner: 161/191.
3. **Chain custody** — 193's operational/store-scoped chain predicate (S3 "Custody of a directory", no waiver). Refusal → the existing `unknown-custody` route; carries the component index for diagnostics only.
   *Layering note:* the predicate is in `security`, and `storage → security` is the **planned** edge (R build plan l.35–37: "`opensip-storage` depends directly on `opensip-evaluator` and `opensip-security`"), not yet present in P. Until it is, the step can only be specified, or the pure predicate must move to where storage can reach it — owner call (B-2).
4. **Main file custody** — `directory().open_regular(leaf)` → hold the `File`; `observe_descriptor` → a file-scope predicate: regular, **link count 1**, owner, no other/group/ACL write. `Scope::ConfigurationFile` cannot be reused as is: its 4 MiB cap is S3's *config* rule ("Custody of a config file adds: regular file, link count 1, at most 4 MiB"). A ledger needs the same properties **without the size cap**. That is a private scope variant, not a new public policy, but the owner must say it (B-4).
5. **Sidecar observation** — `open_regular(leaf+"-wal")`, `(leaf+"-shm")`: each is *present* (apply step 4's predicate), *absent* (`NotFound`), or *unobservable* (any other error → unknown-custody; never treated as absent — same three-way rule as S9.3 markers and my Q1 note). A present sidecar that is a symlink, non-regular, multiply linked or foreign-writable refuses. (Row 4 shows SQLite itself refuses a symlinked `-wal` under `NOFOLLOW`; the gate makes it a typed custody refusal *before* the open instead of a generic open error.)
6. **Absent sidecars** — behaviour depends on B-1; see §6.
7. **Open** — unchanged flags; `configure()` unchanged (busy 0 first, UTF-8, WAL).
8. **Writer only: `is_readonly("main")` must be `false`**, else a typed refusal before any `BEGIN` (closes the first half of 183 N-1; row 1 shows `BEGIN IMMEDIATE` cannot stand in for it).
9. **Establish the snapshot / transaction, then bracket** — after the first read inside `BEGIN` (reader) or after `BEGIN IMMEDIATE` (writer): re-sample main via `open_regular` and compare (dev, ino, nlink, uid, mode); re-observe sidecars. **Correction after measuring rows 6–7:** a sidecar's identity may lawfully change between the *pre-open* observation and this one — a concurrent lawful writer that closes last deletes both files and the next writer recreates them with new inodes — so the pre-open sidecar observation is a custody check only, not an identity baseline. The sidecar identity baseline is taken here, *after* our own connection holds its snapshot (from then on our connection keeps them alive), and is compared again at the end of consumption (§7). Size and mtime of `-wal` are never compared: row 7 shows they change under lawful APPEND-WRITE while the snapshot stays stable; `recheck()` the chain. Any mismatch → unknown-custody, connection dropped.
10. **Return** the connection together with the retained chain and the held main-file handle, so the pair lives exactly as long as the snapshot. No accessor exposes either.

Error classes stay inside the existing vocabulary: everything here is `unknown-custody` → `operational-failed` / `HOST.IO_FAILURE` / `host-io`, `domainDetail` omitted (R readonly §1 l.66; identity §"Project ledger text encoding"), with busy kept on its own route exactly as 184/181 decided. Internally the refusals should be a typed enum (name-observation / name-changed / descriptor / chain-predicate{component} / file-predicate{which} / sidecar-unobservable / readonly-fallback / identity-changed), mirroring 191's four classes — a mapper can then be exhaustive.

What this step advances, stated narrowly: **183 N-1** (fallback: closed; sidecar creation: decided by B-1), **124 F-1 / 149 N-2** for the ledger (the three files are now related to one retained, custody-checked directory instead of three caller-chosen paths; persistent relocation is detected), **118 I-2** (one more admission row stops being prose: "typed file presence" for main/WAL/SHM). It does **not** close 124 F-1 (ABA remains — option B/C), and it says nothing about the security carrier, which needs the same step in `journal_store.rs` l.409 as a second, identical integration.

## 6. Sidecar creation — the decision I cannot make for the owner (B-1)

Facts: WAL mode is required (P l.114–116; R S7 l.744 "SQLite WAL"). SQLite removes `-wal`/`-shm` when the last connection closes cleanly, so *absent sidecars is the normal resting state*. A reader then creates both and cannot remove them (row 2). The reader law forbids creating durable files and "creating missing carriers" (R readonly l.141–145).

| Option | Effect | Cost |
|---|---|---|
| (i) **Refuse** a read-only open when either sidecar is absent | literal compliance | read-only recovery is unavailable on every cleanly closed ledger — i.e. most of the time. Probably unacceptable, but it is what the text says today |
| (ii) **Owner amends the law**: SQLite's `-wal`/`-shm` are SQLite-owned lock/index carriers of an *admitted* ledger, not product state; a reader may cause their creation inside the custody-checked directory; they are observed before and after (step 5/9) and never interpreted | matches SQLite's design; needs one sentence in readonly §2 and in 182's writer paragraph; the directory must be writable by the reader, which S3 custody already implies for the owner | it is a change to an owner rule — must be the owner's, not mine |
| (iii) Writers keep sidecars persistent (`SQLITE_FCNTL_PERSIST_WAL`) so readers never create them | readers stay write-free | FFI (platform), and a never-yet-opened ledger still has none |
| (iv) `immutable=1` for readers when sidecars are absent | no files | unsound with a concurrent APPEND-WRITE writer, which S7 allows alongside SHARED-READ; P refuses URIs. Rejected |

My recommendation to the owner is (ii), with (i) as the behaviour until the sentence exists. Whichever is chosen, row 2's "directory 0500 → read fails" should be a test, because it is the observable difference.

## 7. Lease-held capture through consumption (149 N-1/N-2) — second step

**What the real guards are** (`lifecycle/src/leases.rs`): `SuppliedLeaseDomain { install: RetainedDirectory, namespaces: BTreeMap<String, RetainedDirectory> }`; the fence is `install.open_regular("lifecycle.fence")` + `FileLock::try_acquire(Exclusive)`; `ProjectHeld<'a>` holds `readers`/`writer` `FileLock`s, borrows the domain, releases on `release()` or `Drop`. So the lease files are **already opened relative to retained directories**, which is exactly the anchor the ledger lacks; but those directories are single handles, "asserted custody inputs" (l.1–3), not custody-checked chains.

**Owner law** (R readonly l.222–231): SHARED-READ excludes GC, sweep, purge, repair-apply, migration and core transitions for the lease lifetime; "`APPEND-WRITE` may coexist; one coherent ledger snapshot is still necessary. This is cooperating protocol exclusion, not proof against arbitrary external filesystem mutation, path replacement or ABA"; and "The lease outlives the read **and consumption/projection of its observation**."

**Composition, in order** (the type system can carry most of it):
1. Build the lease domain from **chain-checked** `RetainedDirectoryPath`s (install root and namespace), so the lease carriers inherit step 3's custody instead of an assertion. `RetainedDirectoryPath::directory()` already yields the `RetainedDirectory` the domain needs.
2. Acquire fence → project lease exactly as today (S7 order unchanged; no fence while holding a lease).
3. Admit the ledger location (§5) and additionally require a **stated relation between the ledger's parent directory and the namespace lease directory**, checked by (dev, ino) on retained handles with safe `metadata()`. This is the missing relation of 149 N-2. *Caveat I checked after first writing this:* S7 fixes the lease files at `<namespace>/writer.lease` and `<namespace>/readers.lease` (R S&L l.742–743), but in the owners I searched (S&L, identity, build plan) I found **no sentence placing the ledger file relative to `<namespace>/`**. I had assumed "same directory". Whether it is the same directory or a named child is an owner layout decision (B-8); the mechanism is identical either way — walk from the retained namespace directory with `open_regular`/a retained child, never from an independent path string.
4. Run the read inside a borrow of the guard: `fn with_shared_read<R>(&ProjectHeld<'_>, …, f: impl FnOnce(&ReadSnapshot) -> R) -> R`. The snapshot cannot outlive the guard; the closure's owned result is, by the law above, historical once the guard drops. "Through consumption" means the *projection* of the observation happens inside `f` or before the guard is released by the caller — so the API should return a value that still borrows the guard (`Consumed<'lease, R>`), and only an explicit `into_historical()` detaches it. That makes "used after release" a visible, typed act rather than a default.
5. End-of-consumption recheck: chain `recheck()`, main identity, sidecar identity against the post-snapshot baseline (§5 step 9 as corrected). Failure downgrades the result to unknown-custody; it does not retroactively prove anything about the interval.

**Accounting for lawful concurrency.** Under SHARED-READ a concurrent APPEND-WRITE may commit, checkpoint, and (if it closes while we are open) leave sidecars to us; another SHARED-READ may open and close. None of that changes main/`-wal`/`-shm` inode identity while our connection is open (row 7), and SQLite's snapshot isolation covers content. What it *does* change — `-wal` size, mtimes, sidecar existence before we open — must therefore never be compared. Under APPEND-WRITE (a writer's own capture) the same holds, plus `is_readonly` (step 8).

**Where it can live.** No crate depends on both `storage` and `lifecycle` today. The build plan sanctions the direction: "Lifecycle may continue to use storage without a reverse storage → lifecycle edge… Storage never calls lifecycle backwards" (R build plan l.37, l.146). So step 4 belongs in `lifecycle`, behind a new `lifecycle → storage` dependency — a real graph change the owner must make deliberately (B-3); I am not proposing it be added silently.

**Against a same-UID non-cooperating actor:** nothing above helps. It can ignore `flock`, and everything in §4 applies. The lease contributes exclusion of *cooperating* OpenSIP processes only, which is what the owner text already says.

## 8. Staged plan — what can proceed as mechanism, what needs an owner decision first

| Stage | Content | Can proceed now? |
|---|---|---|
| **S1** | Writer `is_readonly("main")` refusal + test (0400 ledger; reader still admitted) | **Yes** — pure mechanism, no owner text involved; closes half of 183 N-1 |
| **S2** | Storage-local location admission *without* policy: retain chain, open main relative to it, three-way sidecar observation, post-snapshot identity baseline, bracket, typed refusals, ordering spy, limit vectors (ABA admitted; post-sample chmod unseen) | **Yes** — uses only `storage → platform`, which exists. It must be labelled "identity and presence observation; **no custody predicate applied**" so it is not mistaken for completion |
| **S3** | Apply the chain and file predicates inside S2 | **Blocked on B-2** (no `storage → security` edge) **and B-4** (operational-file scope without the 4 MiB config cap) — owner decisions |
| **S4** | Reader behaviour when sidecars are absent | **Blocked on B-1** — until decided, the only behaviour consistent with the current text is refusal; implement that and make the 0500-directory case a test |
| **S5** | Same admission for the security carrier opener (`journal_store.rs` l.409) | mechanism, after S2's shape is reviewed; carrier encodings differ (not UTF-8-only) |
| **S6** | Lease-held capture in `lifecycle` (§7) | **Blocked on B-3** (new `lifecycle → storage` edge) and on S3 (otherwise the lease domain is still asserted custody) |
| **S7** | True SQLite descriptor identity (option B or C) | **Blocked on B-7** — platform FFI and a decision on how a rusqlite handle may cross into platform |

Anything short of S3+S6 must not be described as custody: S1–S2 replace a single `symlink_metadata` sample with a held, bracketed, typed observation, which is strictly better and still a *supplied-custody* precondition for the predicate half. Say so in the README of whatever lands.

## 8.1 Blockers, in the order they bite

- **B-1** sidecar creation vs the read-only no-write law (§6) — owner text decision.
- **B-2** storage cannot call the chain predicate: `storage → security` is planned, not present (§5.3). Either land the edge or move the pure predicate; do not duplicate it.
- **B-3** no crate can hold a lease and a snapshot together (§7) — needs the `lifecycle → storage` edge.
- **B-4** file-scope predicate without the 4 MiB config cap — owner must state the operational-file scope (S3 currently defines only directory and config-file custody).
- **B-5** Linux: `observe_descriptor` is `UnsupportedPlatform`, so every step from 3 on fails closed there. Correct, but it means this integration is macOS-only until the Linux ACL observer exists.
- **B-6** local-filesystem admission: S3/§"Publication failure phase" (R S&L l.552–557) requires an "admitted local POSIX filesystem" for inference from retained handles; nothing in P admits one. The gate must carry it as a supplied precondition, as `existing_path` does today, and must not imply it checked.
- **B-7** true main-file identity (ABA) needs platform FFI (option B/C) — explicitly out of this step.
- **B-8** physical layout: where the ledger (and the security carrier) sit relative to `<namespace>/` is not stated in the owners I searched; §7 step 3 needs that sentence.

## 9. Tests the step should arrive with (each corresponds to a measured row or an owner sentence)

fallback: 0400 ledger → writer refusal before `BEGIN`, reader still admitted · sidecars: absent/present/symlink/hard-linked/foreign-writable/unobservable, each typed; absent + directory 0500 · chain: reuse 193's synthetic and real chain tests through this entry point · bracket: persistent swap of main → refusal; swap of `-wal` identity between samples → refusal; sidecars *appearing* between samples → admitted · **limit vectors kept as tests, like 188's wrong-id vectors**: ABA during open is admitted; ancestor chmod after the second sample is not seen — so the documented limits cannot silently change · ordering spy: no SQLite open before steps 2–5 succeed; no `BEGIN` before step 8 · both openers, UTF-8 and the 179/184 busy/encoding behaviour byte-identical (rerun my 183/184 opener probe verbatim).

## 10. Limits of this assistance

One machine, macOS, bundled SQLite; I did not test network filesystems, Linux, `SQLITE_FCNTL_*`, or a VFS. I read `leases.rs` for its surface and standing only, not its algorithms. Owner sentences are quoted from the 192 reference tree; if a later checkpoint changed them, re-ground before use. Nothing here is approved, selected or implemented.
