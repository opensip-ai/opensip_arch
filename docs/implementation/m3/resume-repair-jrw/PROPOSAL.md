# The resume/repair writer — proposal J-RW r4

2026-10-04. Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the overnight autonomous run. Law **J-RW** of the accepted M3 unit plan, owned by M3-J under lead decision P5-1 (M3P:217, :236, :572-575).

**Draft r4, not accepted. Not code.** It must be accepted before M3 day 0, which is M3-L's acceptance (M3P:236, :259). Its code unit J4 follows it and does not wait for J3 (M3P:251, :311, :574).

r1 (`PROPOSAL-r1.md`, sha256 `0002c005…`, 61,626 bytes) was reviewed by Codex (`reviews/codex-resume-repair-jrw-r1`; REQUIRED-FINDINGS, 3 required, 3 non-blocking). r2 answered all six, and re-pinned X3c at its accepted r8 bytes and every law at its snapshot.

r2 (`PROPOSAL-r2.md`, sha256 `7bff3d55…`, 87,080 bytes) was reviewed by Codex (`reviews/codex-resume-repair-jrw-r2`; REQUIRED-FINDINGS, 2 required at P2, 1 non-blocking). Codex closed JRW-R1-02 and the three r1 observations, and left JRW-R1-01 and JRW-R1-03 to the new findings. r3 answers all three r2 items. Beyond those answers it changes only product line pins: main is now `cd5958b`, and every line it cites in X4-F1's changed files is re-checked there.

r3 (`PROPOSAL-r3.md`, sha256 `9aa30410…`, 103,333 bytes) was reviewed by Codex (`reviews/codex-resume-repair-jrw-r3`; REQUIRED-FINDINGS, 2 required at P2, no new observations). Codex closed JRW-R2-01, JRW-R2-02 and JRW-R2-NB-01; its union recount agrees: 15. r4 answers both r3 findings. Beyond those answers it changes only pins: the product base for the X4-F2 code is now `d2c00a9`, X4T is cited at its accepted r12 snapshot, and two RW-S7/RW-S8 records are noted as landed.

## r4 changes and review responses

| Finding | Change |
|---|---|
| **JRW-R3-01** (the DDL breakdown is wrong) | **Accepted.** `selected_ddl()` holds **7 tables, 1 explicit index and 18 triggers**; r3's 6/1/19 was a miscount. `PAIR_DDL` creates two tables, `commit_receipts` and `commit_associations`.<br>Corrected everywhere: the r3 response row below, item 3.3 (now with a per-fragment table) and RW-C17.<br>- **k = 26 is unchanged**, as are the per-fragment totals, RW-C5, its stop rule and the N-L0 fallback.<br>- **RW-C17's census** now enumerates, by kind and name, the statements `selected_ddl()` actually selects. The product DDL is never changed to fit the text.<br>Codex's text-only enumeration is at `reviews/codex-resume-repair-jrw-r3/sql-source-census.json`. |
| **JRW-R3-02** (compose with X4-F2's clocked refusal) | **Accepted, as lead decision LD-16.**<br>**The route.** Under accepted X4T r12, integrated as X4-F2, a fenced read whose `EV-CLOCK` refuses still performs the mandatory floor write-ahead before returning the clocked continuation refusal (X4T:170-175, :205). In the product, `publish` at `floor_publication.rs:993` runs before `into_view` at `:995`; see also `current_trust_admission.rs:243-289` and `:1113-1125` (all at `d2c00a9`).<br>**The decision.** C-TRUST and C-TDIR are authorized on that path. They rest on the same authority as the publication: the closure the read authenticated, and the pending write the admission carries. They manufacture no view and grant no lease. The completed publication returns exactly X4T r12's unchanged clocked refusal, at the same precedence.<br>**Unchanged:** earlier authentication and time refusals, and report-only reads, stay effect-free; the non-reference proof, the fence and the N-T2a/N-T2b mappings stand.<br>**Rejected:** a successful-view gate.<br>**Updated:** item 2 (the T row and a new authorization bullet), items 3.5 and 3.6, item 4's terminals for RW-T1 to RW-T3, RW-C14, RW-C15, J4d, the forbidden substitutes, and new X-RW-13.<br>**New controls:** RW-C18 (completion, then the unchanged clocked refusal) and RW-C19 (native, custody, non-prefix and budget failures on that path each keep their own row; early refusals and report-only reads stay effect-free).<br>**RW-S5** becomes X4T r13, the next successor after the accepted r12, keeping r12's clock and write-ahead rules. |
| **Context** | **Pins.**<br>- **Product:** main is now `d2c00a9`. Of the files J-RW cites, only `floor_publication.rs` (after line 944), `current_trust_admission.rs` and `Cargo.lock` changed since `cd5958b`. Every r3 line cited in them holds or is re-pinned, and r4's new X4-F2 cites are read at `d2c00a9`.<br>- **X4T:** now cited at the accepted r12 snapshot (`cf566db7…`). Its r11 lines are re-mapped to the same r12 passages (short names).<br>**Records.**<br>- **RW-S7** (P5-1's owner list) has landed: M3-PLAN r7, current at r9, `M3-PLAN-r9.md:284`.<br>- **RW-S8's `repair recover` correction** has landed: J1 r4, carried in accepted r5, `PROPOSAL-r5.md:815`. Replacing item 11's recommendation is still owed.<br>J-RW's other J1 and M3P cites stay on their r3 and r6 snapshots. |

## r3 changes and review responses

| Finding | Change |
|---|---|
| **JRW-R2-01** (the schema cookie wraps, so cookie 0 does not prove no history) | **Accepted. C-LEDGER is kept, and its guarantee is now stated exactly** (item 3.3).<br>**The wrap.** In the bundled engine, SQLite 3.53.2, the cookie is a wrapping 32-bit counter. It gains 1 per schema statement and 1 per VACUUM, and the engine's own comment allows that it can "be set back to prior value" (`sqlite3.c:128440-128455`, `:161652-161670`).<br>**The bound.** The guarantee rests on **k = 26**: the most cookie increments OpenSIP's writers can commit in a ledger's lifetime. That is X3c item 2's one DDL transaction of 26 `CREATE` statements (7 tables, 1 index, 18 triggers, as corrected in r4; `project_ledger.rs:33-43` and the six fragments it names). The transaction commits at most once (`project_ledger.rs:537-564`), each statement increments exactly once (`sqlite3.c:129318`, `:130875-130877`, `:158430`), and no other product SQL changes a ledger's schema (the census in item 3.3, list item 4). So for every OpenSIP writer, cookie 0 means no schema change committed.<br>**Foreign writers.** A non-OpenSIP same-uid writer that commits 2³² − k or more schema changes joins raw-byte forgery under "Not established". r2's "not reachable", and its coverage of "any writer that changes the schema only by SQL schema statements or VACUUM", are withdrawn.<br>**Unchanged:** the stop rule and the N-L0 fallback.<br>**New:** control RW-C17, a census of product SQL with its owner, and RW-C5's pin of cookie 26 after creation. Carried into RW-S3, X-RW-9 and the forbidden substitutes. Withdrawing C-LEDGER now is rejected. |
| **JRW-R2-02** (N-T2's routing) | **Accepted. N-T2 is split at the existing failure boundary** (item 3.6, item 5).<br>- **N-T2a.** A symlink or non-directory at a publication-parent name fails `open_private`'s native open (`O_DIRECTORY`, `O_NOFOLLOW`; `crates/platform/src/filesystem/directory_open.rs:61-73`, `:134-150`). It keeps the host I/O row, `HOST.IO_FAILURE` (`floor_publication.rs:164-166`; `current_trust_admission.rs:100` at `cd5958b`).<br>- **N-T2b.** Only a directory that is opened and reaches the custody judgment takes `installation-incomplete` (`floor_publication.rs:170`; `current_trust_admission.rs:107`), as RW-N12's case does.<br>- **Budget.** A budget failure keeps the budget row (`floor_publication.rs:58-69`). X4T r11 item 10's preserved host I/O and budget rows are unchanged (X4T:233).<br>C-ACL runs only on the retained directory that `open_private` returned, never after a native failure. RW-C15 is fixed to match. RW-N12 is unchanged. |
| **JRW-R2-NB-01** (point identities and physical records) | Taken (item 1, item 3.6, item 4, RW-D1).<br>- **Host traces.** `-a` (1009 records, 11 `create.after` bases) and `-b` (165 records, 7 bases) share only three bases, so their union has 15. The bases are listed in item 1. Codex counted 14; r3's recount lists them so the count can be checked.<br>- **Physical events.** Storage's `dependency/create.after#6` is one point identity with two physical records: the commit child at `census-trace.txt:112` and the refused-end child at `:1256`. So there are three trace/point selections (storage #6, host `-a` #5, host `-b` #5) and four physical directory events.<br>RW-D1 selects the commit child explicitly, and the refused-end occurrence leaves the same RW-T3 state. |
| **Context** | Product main is now `cd5958b`. After `e093e90`, crates changed only in X4-F1's ten files (`15c0779`). Of these, r3 cites only `current_trust_admission.rs`, read at `cd5958b`: its rows are 4 lines lower than at `e093e90`. `floor_publication.rs`, `private_access.rs`, the storage crate and the platform crate are unchanged since `e093e90`. |

## r2 changes and review responses

| Finding | Change |
|---|---|
| **JRW-R1-01** (L-UNC admits a database whose committed history was compacted away) | **Accepted. Item 3.3 is rewritten.** L-UNC gains a creation-history discriminator: the **schema cookie** (`PRAGMA schema_version`, header offset 40) must be 0. SQLite increments it on every schema change and counts VACUUM as one (SQ-PRAGMA; SQ-FORMAT §1.3.9), so the CREATE, INSERT, DROP and VACUUM counterexample ends at 3 or more and is refused. The product's ledger connections run in defensive mode, where `PRAGMA schema_version=N` is a silent no-op (`crates/storage/src/ledger_store.rs:125-133`; SQ-DEFENSIVE). r1's categorical "never held evidence" sentence is replaced by the guarantee actually established and its threat model (item 3.3). RW-C5 now pins both positive crash views **and** the compacted-history counterexample, plus five other committed-history fixtures. The stop rule gains a fallback: if either positive view fails any observable, C-LEDGER is withdrawn, RW-L1 keeps `LEDGER.CORRUPT` as neighbour N-L0, and L11 stays open, narrowed to that state (item 10). The boundary is carried into RW-S3 and X-RW-9. New neighbour N-L2 and mutation row RW-N11. |
| **JRW-R1-02** (C-REG admits an absent namespace with a partial marker) | **Accepted. Item 3.4's join is closed to item 4's states.** Either N and the marker are both positively absent, or N is present with its complete footprint and the marker is absent, exact or P-PREFIX. **A present marker of any form, with N absent, is never the join.** That includes an exact, zero-length, strict-prefix, ACL-omitted or private marker. The join is decided before any effect (X2:238-247; `first_registration.rs:2260-2293`; REG:76). New neighbour N-R9 with its existing rows, `marker-custody` or `identity-contradiction`, and mutation row RW-N10 (three variants). The conditional is carried into RW-S1 and RW-S2. |
| **JRW-R1-03** (a created-but-not-private trust-publication directory) | **Accepted. New state RW-T3 and new completion C-TDIR** (item 3.6). A directory that `may_create` lets a publication create (`trust/floor_publication.rs:406-414`) is completed by C-ACL at `parent_dir`, under the fence, before `write_dependency`. The fenced read admits the unchanged view, and the completion happens later, inside the publication's own step, so no trust admission is relaxed. **Census:** one occurrence in each pinned census child that publishes:<br>- storage `dependency/create.after#6` (`census-trace.txt:112`);<br>- host `#5` (`census-trace-a.txt:40`, `census-trace-b.txt:40`).<br>None is in a kill set, so no run executed it. New neighbour N-T2. New X9 rows RW-D1 (the state itself) and RW-K10 (crash during its completion), and mutation row RW-N12. J4d and RW-S5 gain the parent-directory step. Item 1 now records r2's full enumeration of `create.after` occurrences in both pinned censuses. **L11 is no longer retired outright.** X9 r17 retires it only when J4e's lead set passes every RW row and J4c's pins hold. Otherwise it stays open, narrowed (item 10). |
| **JRW-R1-NB-01** (byte preservation) | Taken. The principle now forbids rewriting an existing byte of a marker, a trust record or any evidence. It names C-LEDGER's SQLite schema transaction, and the header, WAL and checkpoint changes the engine makes on an L-UNC file, as the one exception (item 3). |
| **JRW-R1-NB-02** (neighbour wording) | Taken. N-R4 and N-T1 now say "neither exactly equal nor a strict prefix", so they no longer overlap RW-R7 or the ordinary equal-bytes admission (`floor_publication.rs:470-481`). |
| **JRW-R1-NB-03** (the "39" example) | Taken. The Problem section now cites the pinned EV storage census: seven `dependency/create.after` occurrences, six files and one directory (#6). The 39 came from security's own X9-1 self-census table (`crates/security/src/crash_matrix_census.rs:826`), which counts a different, five-operation child. It is not the pinned evidence and is not used. |
| Codex's request item 7 | J4c no longer depends on J4a. It reports through its owner's own `LedgerDisposition::Completed`, and J4e joins every unit's typed result (item 11). |
| Codex's request item 2 | Codex found that IE:47-50 needs no passage successor for this design. X-RW-1 records that, and review question R1 is closed. |
| **Context** | **X3c r8** is accepted by GROK2 with no findings (`m2/ledger-blob-x3c/PROPOSAL-r8.md`, `ba638efb…`; `m2/reviews/grok2-ledger-blob-x3c-r8`). J-RW's X3c joins are rechecked against it: X-RW-9 is rewritten, and RW-S3 is now X3c r9 on r8's accepted bytes. Every other law is cited by its snapshot. Product: main `e093e90`, as the lead directs. Main has since advanced to `0ceb9ad` (I1-L), which changes no file under `crates/`, so every cited product line is the same at all three commits. |

**What this law is.** P5-1 asks for "the resume/repair writer's successor to X2 item 8, X3c item 10 and the X4T dependency-publication rule, with its X9 coverage rows" (M3P:217, :573). M2 leaves three families of crash states permanently refused: an interrupted first registration, a created owner not yet sampled private, and a partial ledger WAL (EXIT:186-191; M2C:349-356, limit L11; X9:163-168). This law:
1. enumerates every such state by owner and census occurrence (item 1, item 4);
2. fixes where, under which lock and on whose authority the writer completes each one (item 2);
3. fixes each completion as the owner's own interrupted step, finished in place (item 3);
4. fixes the states it must keep refusing (item 5), its idempotence and crash-during-repair rules (item 6), its disclosure (item 7) and its rows (item 8);
5. names its controls, its X9 r17 rows, J4's sub-units and the successors the owners must write (items 9 to 12);
6. records the cross-law items, X3c r8's included (item 13).

**Standing direction.** Every item that says "lead decision" is made under the owner's standing direction of 2026-09-30 to proceed on the lead's recommendation. Each names the alternatives it rejects. The owner may reverse any of them. No item blocks on an owner decision ("Open questions").

**The owners' assent.** The laws this one amends are the lead's: X2 r9, X3c r8, X3b r10, X4T r12 (r4; r11 until r3) and X4B r5, and the registry owner selection v2. Their amendments are written here as successors RW-S1 to RW-S5 (item 12), as lead decisions under the standing direction. None of them changes before J-RW is accepted, and each is reviewed with J-RW or right after it.

## Short names

Arch paths are under `docs/`. The sha256 prefixes are of the bytes read for this draft. Every law is cited by its accepted snapshot, never by another law's live `PROPOSAL.md`. X1 and L465 have only one accepted revision, so their single file is the snapshot.

| Name | Document | sha256 |
|---|---|---|
| **M3P** | `implementation/m3/M3-PLAN-r6.md`, the accepted r6 bytes | `a6956e88…` |
| **J1** | `implementation/m3/host-pipeline-j/PROPOSAL-r3.md`, the r3 bytes CODEX2 accepted | `ad887c90…` |
| **M2C** | `implementation/m2/M2-COMPLETE.md` (r2, COMPLETE; a record) | `b8d6053a…` |
| **EXIT** | `implementation/m2/EXIT-PLAN.md` (a record) | `fee07b44…` |
| **X2** | `implementation/m2/project-root-x2/PROPOSAL-r9.md`, the r9 bytes Grok accepted | `0d68e3a5…` |
| **X3C** | `implementation/m2/ledger-blob-x3c/PROPOSAL-r8.md`, the r8 bytes GROK2 accepted | `ba638efb…` |
| **X3B** | `implementation/m2/journal-x3b/PROPOSAL-r10.md`, the accepted r10 bytes | `25a60824…` |
| **X4T** | **(r4)** `implementation/m2/trust-admission-x4t/PROPOSAL-r12.md`, the r12 bytes Codex accepted (`reviews/grok2-x4t-f2-r1`). X4T r12 carries X4-F2's clock rule. Every X4T line J-RW cites is r12's: r3's r11 cites `:97-102`, `:102`, `:120`, `:141` and `:153` are now `:164-169`, `:169`, `:193`, `:216` and `:233`, the same passages. | `cf566db7…` |
| **X4B** | `implementation/m2/trust-bootstrap-x4b/PROPOSAL-r5.md`, the accepted r5 bytes | `97c2eef3…` |
| **X3D** | `implementation/m2/commit-session-x3d/PROPOSAL-r8.md`, the r8 bytes | `5e491b92…` |
| **X6** | `implementation/m2/carrier-recovery-x6/PROPOSAL-r4.md`, the r4 bytes | `20df341c…` |
| **X1** | `implementation/m2/ordinary-platform-x1/PROPOSAL-r1.md` (r1, the accepted bytes; the live file is being amended to r2 by J1's S3) | `d747adf0…` |
| **X9** | `implementation/m2/crash-matrix-x9/PROPOSAL-r16.md`, the accepted r16 bytes | `f08efe95…` |
| **EV** | X9's evidence record at C = `3d2d5b5`, `crash-matrix-x9/evidence/3d2d5b5a…/` (its `hashes.txt` is `97f8367e…`):<br>- `storage/matrix.json`;<br>- the storage census `storage/census-trace.txt` (`c82cf452…`);<br>- the host censuses `host/census-trace-a.txt` (`15a580b8…`) and `-b.txt` (`a85e8fe9…`) | `5585bc42…` (matrix) |
| **L465** | `implementation/m2/initial-parent-preparation-465/PROPOSAL.md` (the only revision) | `b34eae39…` |
| **REG** | `implementation/m2/project-registry-owner-selection-v2/owner.md`, the selected registry owner | `2d4b65c9…` |
| **OWN** | `implementation/m2/initial-root-binding-owner-selection-v1/owner.md` | `35953d09…` |
| **OPP** | `implementation/m3/operability/PLAN-r3.md`, the r3 bytes Codex accepted | `b49035f2…` |
| **SOP2** | `implementation/m3/operability/s-op-2/PROPOSAL-r6.md`, the r6 bytes Codex accepted | `ce8d3a4b…` |
| **SL, IE** | `v2/contracts/product-v1/{security-and-lifecycle, identity-and-evidence}.md` | `a319da39…`, `c82404f3…` |
| **BP** | `v2/architecture/implementation-boundaries-and-build-plan.md` | `8e6e8bab…` |
| **CINV** | `coop/design-corrections/workflows/command-inventory.v3.json` | `d303cc64…` |
| **SQ-SRC (r3)** | The bundled engine's own source, the `libsqlite3-sys` 0.38.2 amalgamation that `rusqlite` 0.40.2 builds (`Cargo.lock:168-169`, `:322-323` at `d2c00a9`): `~/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/libsqlite3-sys-0.38.2/sqlite3/sqlite3.c`, 9,507,037 bytes. It declares `SQLITE_VERSION "3.53.2"` (`sqlite3.c:470`). It is outside both repositories, so it is cited by hash. | `0a409f16…` |
| **SQ-PRAGMA, SQ-FORMAT, SQ-DEFENSIVE, SQ-VACUUM** | SQLite's own documentation, fetched 2026-10-04:<br>- <https://www.sqlite.org/pragma.html#pragma_schema_version>;<br>- <https://www.sqlite.org/fileformat2.html> (§1.3.6, §1.3.9);<br>- <https://www.sqlite.org/c3ref/c_dbconfig_defensive.html>;<br>- <https://www.sqlite.org/lang_vacuum.html>.<br>The engine is the SQLite that `rusqlite` 0.40.2 bundles (`crates/storage/Cargo.toml:13`). J4c pins what this law relies on against that engine (RW-C5). | web; not pinned by hash |

Product paths are under `opensip/` at main **`d2c00a9`** (r4). They were read, not run.
- **(r4)** From `cd5958b` to `d2c00a9`, the product integrated X4-F2 (`988f6ed`), X3a-2 and other units. Of the files J-RW cites, only three changed:
  - `crates/security/src/trust/floor_publication.rs` changed only after line 944, so every r3 cite in it holds. Its new cites (`:938-1001`, `fenced_first_read`) are read at `d2c00a9`;
  - `crates/security/src/trust/current_trust_admission.rs`: `:95`, `:100`, `:101` and `:107` are unchanged. Its new cites (`:243-289`, `:1113-1125`) are read at `d2c00a9`;
  - `Cargo.lock`: `rusqlite` 0.40.2 is now at `:322-323`. `libsqlite3-sys` 0.38.2 is unchanged at `:168-169`.

  Every other cited product line is the same at `cd5958b` and `d2c00a9`.

r3's pins, for the record:
- From `3e64266` to `e093e90`, no file under `crates/` changed.
- After `e093e90`, crates changed only in X4-F1's ten files (`15c0779`), all in `crates/security/src/`: `custody/operation_guard.rs`, `custody/operation_live_tests.rs`, `trust_time.rs`, and, under `trust/`, `current_trust_admission.rs`, `current_trust_admission_tests.rs`, `floor_publication_tests.rs`, `live_observation.rs`, `live_observation_tests.rs`, `role_machine.rs` and `trust_bootstrap_tests.rs`.
- r3 cites only `current_trust_admission.rs` among these, and reads it at `cd5958b`.
- Every other cited product line is the same at `3e64266`, `e093e90`, `0ceb9ad` and `cd5958b`.

## Problem

**What exists at `d2c00a9`.** Each owner fails closed on its own interrupted act, and nothing completes it.
- **First registration** (X2 item 6). The RESERVED row is durable before the namespace, `.opensip` and marker exist, and ACTIVE comes last (X2:236-248).
  - Admission classifies a matching RESERVED row as `RecoveryNeeded` and grants nothing (X2:177, :184; `crates/security/src/custody/project_admission.rs:678-719`). The row is `PROJECT.ROOT_CUSTODY_REFUSED` / `identity-recovery-required` (X2:366; `custody/first_registration.rs:214-222`).
  - A marker that exists but is not judged private refuses earlier, as `marker-custody` (`project_admission.rs:602-603`). An empty or partial private marker is `Malformed`, so `Contradiction` (`project_admission.rs:616`, `:684-685`).
  - The writer itself says that "each leftover is the registry owner's explicit-recovery case, which is not implemented here" (`first_registration.rs:18-21`; X2:256).
- **Private creation.** A new private directory or file is made by `mkdirat 0700` or an exclusive `0600` create, and only then does it get its zero-rights owner allow (`private_access.rs:120-126`; `store_custody.rs:105-154`). The private predicate refuses an omitted ACL (`private_access.rs:55`). An existing object is judged as it stands and is never changed (`store_custody.rs:110`; L465:17). So a kill between the create and the allow refuses on every later admission:
  - X3c's store directories and ledger file: custody `private` (`ledger_store/project_ledger.rs:260`);
  - X3b's `trust/carrier-floors/`: X3b's host I/O row (`journal_store/carrier_floor.rs:237`, `:841-844`). This one blocks **every project of the installation**, not one;
  - X2's `I/host` and `I/host/projects`: inside registration, behind `identity-recovery-required`;
  - the marker: `marker-custody`, above;
  - **(r2)** a trust-publication directory: `installation-incomplete` at the next publication's `parent_dir` (`trust/floor_publication.rs:416-451`, `open_private` at `:158-172`), installation-wide (item 3.6);
  - an X4T dependency leaf, below.
- **The ledger WAL** (X3c item 2). WAL is selected, then one DDL transaction commits (`project_ledger.rs:452-509`; barriers `wal` at `:491` and `ddl.commit.before` at `:499`). On the next open, only an empty file with no `-wal` resumes (`project_ledger.rs:540-552`). Any other stored state is `LEDGER.CORRUPT` (`:425-432`, `:438-449`; X3C:85, :216).
- **An X4T dependency leaf** (X4T item 7). Each dependency is created only when its content-addressed name is absent. An existing name is admitted only when it is private and holds exactly the bytes (`floor_publication.rs:455-488`). A leaf left empty, or torn, is never named by the unchanged pointer, so it is harmless until a later publication writes **that same name**. Then it refuses `CONFIG.CUSTODY_REFUSED` / `installation-incomplete` (X4T:216; `floor_publication.rs:470`, `:479`), installation-wide.

**What X9 measured.** In X9-2's kill set, 57 F00 kill points leave the next writer refused on these rows (X9:136-161; EV, F00 runs). They are tabulated in item 4. The census holds more occurrences of the same windows than the sampled kill set, which samples the first, a middle and the last occurrence of a repeated protocol (X9:920).
- **(r2, JRW-R1-NB-03)** For example, the pinned storage census has **seven** `x4t.floor-publication.dependency/create.after` occurrences (`census-trace.txt:72-118`), and the kill set samples #1, #4 and #7.
  - Six of the seven are dependency files.
  - #6 is a directory: no write follows it, and its own and its parent's directory barriers do.
- This law covers states, not only the sampled points. Item 1 records the full enumeration.

**Why it matters.** The owner uses OpenSIP daily. A crash in the first analysis of a project, in the installation's first carrier floor, or inside a trust floor publication leaves the project, or every project, refused with no remedy OpenSIP can name. X9 deliberately added no writer for these states (X9:157). Writing one is M3's work.

## Decisions

### 1. Scope: exactly L11's three families, by owner (lead decision)

| Family | States (item 4) | Owner law and item | Product owner | Census windows |
|---|---|---|---|---|
| **R** interrupted first registration | RW-R1 to RW-R7 | X2 item 6, under REG's explicit reservation recovery (REG:72-78) | `custody/first_registration.rs`, `custody/project_admission.rs` | `x2.fence.register.reserved/rename.after` through `x2.fence.register.active/rename.before` |
| **P** created, not yet private | RW-P1 to RW-P3; also inside R (RW-R2, RW-R5) and T (RW-T1, **RW-T3**) | X3c items 1 and 2; X3b item 2 (X3B:52); X2 item 6 step 3; **(r2)** X4T item 7's parent directories | `store_custody.rs`, `ledger_store/project_ledger.rs`, `journal_store/carrier_floor.rs`, `trust/floor_publication.rs` | every `…/create.after` of a private create, before its allow |
| **L** partial ledger WAL | RW-L1 | X3c item 2 (X3C:78-85) | `ledger_store/project_ledger.rs` | `x3c.ledger-create.wal` and `x3c.ledger-create.ddl.commit.before` |
| **T** an X4T publication's interrupted dependency | RW-T1, RW-T2 (a leaf at a re-written name); **(r2)** RW-T3 (a parent directory) | X4T item 7 (X4T:164-169), shared with X4B item 5 | `trust/floor_publication.rs` | `x4t.floor-publication.dependency/create.after` and `/write.before` |

- **Owner list (cross-law item X-RW-7).** P5-1 names X2, X3c and X4T (M3P:573). Family P also has X3b's floor directory (X3B:52), and family R has REG as the recovery owner. Both are added here; M3P's next revision records it (RW-S7).
- **The full enumeration (r2, JRW-R1-03).** r2 classified every `/create.after` occurrence in both pinned censuses against item 4 and item 5.
  - **The storage census** (`census-trace.txt`, 1379 records) has 22 `create.after` bases. Every occurrence the kill set samples is in item 4, or ends Committed in its F00 or F-row. The unsampled occurrences are:
    - `x2.fence.register.namespace/create.after#3`: RW-R1;
    - `x3c.object/create.after` #2 to #40 and #42 to #81: object temporary files written after the attempt row. These are F02 to F05's never-adopted residue, not L11;
    - `x4t.floor-publication.dependency/create.after` #2, #3 and #5: files. Each is RW-T1 when the next publication writes its name, and an unreferenced, harmless leaf otherwise;
    - **#6, the predecessor directory: RW-T3.** (r3, NB-01) This one point identity has two physical records: the commit child's at `census-trace.txt:112` and the refused-end child's at `:1256`. Both leave the same RW-T3 state.
  - **(r3, NB-01) The host census traces `-a` and `-b` share the dependency shape, but not their other bases.**
    - **`-a`** has 1009 records and 11 `create.after` bases. Besides the 3 shared ones, it has `x3b.append.seal.witness-committed`, `x3b.append.seal.witness-pending`, `x3c.ledger-create`, `x3c.ledger-create.namespace`, `x3c.ledger-create.projects`, `x3c.object`, `x3c.object.objects` and `x3c.object.sha256`.
    - **`-b`** has 165 records and 7 bases. Besides the 3 shared ones, it has `x3b.append.terminal.witness-committed`, `x3b.append.terminal.witness-pending`, `x3b.floor.write` and `x3b.rollover.open.witness`.
    - **The 3 shared bases** are `x3b.end.floor.write`, `x4t.floor-publication.dependency` and `x4t.floor-publication.pointer`, so the union has 15.
    - **Each trace has one directory point,** `dependency/create.after#5` at line 40: RW-T3. Their unsampled file occurrences (`#2`, `#4`) are RW-T1 or harmless, as in storage. Every other base is covered by item 4's P states or by its existing owner, as in storage.
    - **Trace `-c`** has 21 records and no `create.after` point.
  - **Counting the directory state.** There are three trace/point selections (storage `#6`, host `-a` `#5`, host `-b` `#5`) and four physical directory events (storage's two records and one in each host trace).
  - **No other occurrence leaves an L11 state.** Codex independently found the same for the registration window's eight unsampled points (Codex r1 review, request item 1).
- **Out of scope**, each with its existing owner, unchanged:
  - `admitted` attempt rows and orphan SEALs: X6's sweep (X6 item 7; X3D:213). Its CLI is `store-gc` at M5.
  - Any `CommitUndetermined`: X3c item 7 and X6. A re-commit over a landed commit is X3c r8's (X3C:114-133), not J-RW's.
  - Journal, witness and carrier states: X3b's floor step and start already reconcile them (X3B items 3, 3a, 4).
  - Quarantine rows, migration (X9 L5), orphan objects (L6).
  - Power-loss variants of every state here: X9 L1. Process death keeps page-cache data, and that is the only crash this law's rows execute.
  - A RESERVED row whose root has since changed identity (moved, or re-cloned at the same path): REG's authenticated move and abandonment (REG:78-86). That needs the user's authorization, which no M3 surface carries.
  - Adopt-kind reservations: REG:76 requires a fresh admitted adoption context. Adoption is not at M3.
  - A transition slot (`TransitionActive`, the incomplete row): the S9.2 transition recovery owner.
- **Rejected:** a general "repair" of any refused state. The safety bias needs closed predicates per owner, and every state outside them already has an owner.

### 2. The writer: the next admitted durable write, at each owner's own step (lead decision)

- **Decision.** There is no separate repair operation. Each family is completed **inside the next admitted durable write request that reaches that owner's step, by that owner, under that owner's lock**:

  | Family | Where in the durable request (J1:297-311) | Lock | Charged to |
  |---|---|---|---|
  | R (and RW-R2's parents, RW-R5's marker) | R9, in place of X2 item 6 when the classification is item 3.4's join | installation fence (write gate) | the gate's ledger (X2 item 9) |
  | RW-P3 (`carrier-floors`) | R10, X3b's floor step | fence, no project lock (X3B:59) | the gate's ledger |
  | T (RW-T1 to RW-T3) | R10, X4T's floor write-ahead, or X4B's acceptance publication (same protocol). **(r4)** The write-ahead runs on both ends of the fenced read: an admitted view, or X4T r12's clocked continuation refusal (X4T:170-175, :205; `floor_publication.rs:977-995` at `d2c00a9`). RW-T3 is completed at `parent_dir`, RW-T1 and RW-T2 at `write_dependency`. | fence, no project lock (X4T:169) | the gate's ledger |
  | RW-P1, RW-P2, RW-L1 | inside `prepare_commit`, at `admit_layout` (`crates/storage/src/commit.rs:370-375`), before the attempt row, so J1's phase A | namespace writer lease (X3C:76, :196) | the operation's attempt ledger (X3C item 9) |

  - **Who.** The writer is an X1 ordinary writer reached through J1 item 3's durable entry, never the creator act (J1:689). Matrix children and tests reach the same owners through their existing drivers.
  - **Never** on a read path: not the 458c read session, `doctor`, the read-only recovery selector (X2:336), the sweep, or the ephemeral entry (J1 item 6). These keep today's refusals byte for byte.
  - **Never in the crashed process.** A failed or uncertain step still latches its owner's ledger, with no later step and no retry (X2:212; X3C item 7). Completion is a later, separately admitted operation.
- **Authorization for family T on X4T r12's clocked path (r4, JRW-R3-02, lead decision).** X4-F2 (integrated; X4T r12, accepted) lets the fenced read end in a clocked continuation refusal instead of a view.
  - **The route.** After items 2 to 5 have authenticated the closure and S4 has admitted tEval, item 6's `EV-CLOCK` may refuse. The admission is then `Admission::Clocked`, carrying the read's floors, its time admission and its pending write-ahead (`current_trust_admission.rs:249-259`, `:1113-1125` at `d2c00a9`). `fenced_first_read` still runs check 3 and, when S4 proposes a change, the mandatory floor write-ahead: `publish` at `floor_publication.rs:993`. Only after that does `into_view` return the refusal (`:995`; `current_trust_admission.rs:286-289`). X4T r12 states this order (X4T:170-175) and places the refusal before every lease and later operation effect (X4T:205).
  - **The decision.** C-TRUST and C-TDIR are authorized on that publication too.
    - **On whose authority.** The same as the publication's own: the closure the read authenticated, and the pending write the admission carries. Completion is a step of that mandatory publication, under the same fence, at the same lease-free point.
    - **What it is not.** It is not a view. Completion manufactures no admitted view, grants no lease and starts no later step.
  - **What follows completion.** The completed publication confirms, and the owner advances, as X4T r12 item 7 requires. `into_view` then returns **exactly X4T r12's clocked continuation refusal, unchanged**: request-rejected, exit 2, `EXTENSION.ADMISSION_REJECTED`, detail `CONTINUE-CORE-NOT-TRUSTED`, with its role subject such as `core:expired` (X4T:218-221; `current_trust_admission.rs:95` at `d2c00a9`). It takes the same precedence, before every lease and later operation effect (X4T:205). That refusal is sticky by X4T r12's own rule (X4T:174).
  - **What is unchanged:**
    - **Earlier refusals stay effect-free.** A refusal raised before time is admitted writes nothing and completes nothing: items 2 to 5, the stored-state join of item 1, and S4's steps 1 to 4 (X4T:172).
    - **Report-only reads stay effect-free.** They write and complete nothing (X4T:172).
    - **The non-reference proof** (items 3.5, 3.6), the fence, check 3 and the closing rechecks run where they run today.
    - **The N-T2a and N-T2b mappings.** A completion or publication failure on this path ends on its own row, which `publish` returns before `into_view` runs: `HOST.IO_FAILURE`, `installation-incomplete` or the budget row (`floor_publication.rs:993`).
  - **Rejected:** a successful-view gate, which completes only when the read admits a view. A repairable, OpenSIP-owned leaf or directory would then block a mandatory write-ahead that X4T r12 requires before the clocked refusal. That publication would fail on `installation-incomplete` instead of confirming the floor, and the sticky refusal X4T r12 relies on would never be written.
- **Authorization for family R (lead decision).** REG requires that "existing operation owners must supply authorization for … explicit recovery" (REG:9), and that recovery be "an independently authorized local operation, not the constructor's fallback" (REG:74). This law is that operation owner.
  - **The authorization:** an `OrdinaryWriteAdmission` (X1 item 2), for a durable request on the same root, whose locator and incarnation agree with the row, authorizes completion of an `allocationKind: random` reservation.
  - **Why it suffices.** That is the same authorization class, on the same root, that created the reservation (OWN:21, the durable commands' first-write effect).
  - **Not a fallback.** The completion runs as its own classified step in a later operation, never as the constructor's in-process fallback.
  - **Adopt-kind rows** still need REG:76's fresh adoption context, and refuse.
- **Basis:**
  - J1's constraints and recommendation (J1:689-690);
  - SL's precedent: transition crash recovery "runs as the first act under the next fence acquisition, before any admission" (SL:648-651, :939-950);
  - L465 item 5, an owner decision: "the creator may add exactly that zero-rights owner allow … It completes the interrupted creation step and is not a permission repair" (L465:19-25);
  - X3b already resumes its own interrupted creation: "an empty database left by a crash is reused only if it holds no schema objects" (X3B:86; `carrier_floor_tests.rs:401-410`).
- **Rejected:**
  - **A separate repair command or library entry.**
    - No analysis word is wired at M3 (J1 item 1), and CINV has no storage-repair command.
    - `repair-recover` is the source-repair journal command, "`opensip repair recover REQUEST-ID [--apply-recovery]`" (CINV:988; BP:973; SL:673), not storage repair.
    - A new command needs a CINV successor and its renderer milestone (BP:895). Meanwhile the daily user stays refused until M4 or M5.
  - **Completion by the crashed process,** as a retry. That is the latched-ledger rule's opposite (X2:212), and it is REG:74's "constructor's fallback".
  - **Completion on a read path or in `doctor`.** Read receipts never write (X2:406; OPP:214-216; OWN:95).
  - **Abandoning the reservation and allocating afresh.** Abandonment leaves an exact marker one-sided, refused for good (REG:78). It also needs proof that no ACTIVE binding was ever admitted, which is more than completion needs.
  - **A consent flag for completion.** There is no CLI at M3. Completion grants nothing the original request did not already ask for.

### 3. Each completion is the owner's own interrupted step, finished in place (lead decision)

**The principle.** A completion finishes the step the crash interrupted, on the same object, by the owner's own primitive:
- **Never deletes,** never truncates, never renames an existing object away, never adopts a staging or temporary name.
- **Never creates a name** the owner's step would not create.
- **Never changes a mode bit,** and appends no ACE but the one zero-rights owner allow a fresh creation appends.
- **(r2, JRW-R1-NB-01) Never rewrites an existing byte of a marker, a trust record or any evidence.** There is one exception: C-LEDGER (item 3.3) runs the selected SQLite schema transaction over an L-UNC file. The engine then changes its own header, WAL and checkpoint state through its normal transaction machinery (`write_schema`, `project_ledger.rs:452-509`). Such a file holds no evidence (item 3.3), and its payload is exactly what X3c item 2's creation would have written.

It acts only when the object satisfies its predicate below. Anything else keeps today's row (item 5). Each predicate is judged under the owner's lock, through the owner's retained parent, no-follow, charged before it runs, and **before any effect** of the completion.

**3.1 C-ACL: completing a private creation (predicate P-ACL).** This is L465 item 5, applied to the L11 owners.
- **P-ACL.** All of these hold:
  1. The object is at the owner's fixed name, at the step where the owner creates or admits that name, on its parent's filesystem.
  2. It is owned by the invoking user. Its mode is exactly `0700` for a directory and `0600` for a file, and a file has one link.
  3. Its ACL attribute is **omitted** (`CapturedAclState::NotReturned`). A NOACL sentinel, an inconsistent capture or a present ACL is not omission. A present ACL is judged as it stands, as today.
  4. **A directory** holds no entry except `.` and `..`, by one bounded scan. **A file** has length 0, or, for item 3.2's targets, satisfies P-PREFIX.
- **Action.** Append exactly one zero-rights owner allow and sample again, through the fresh path's own step (`prepare_fresh_private_sample`, `private_access.rs:120-126`).
  - The new sample must judge private, or the object refuses on today's row. The allow stays, as on the fresh path (`private_access.rs:121-124`).
  - Then the owner's remaining steps run unchanged: exact name, filesystem, the object's own barrier and its parent's.
- **Where:**
  - X3c's `projects/`, `projects/N/`, `objects/` and `objects/sha256/`;
  - `ledger.sqlite` at length 0, after which X3c item 2's existing resumable-empty path runs;
  - X3b's `trust/carrier-floors/`;
  - X2's `I/host` and `I/host/projects`;
  - the marker;
  - **(r2)** a trust-publication directory that `may_create` permits (item 3.6);
  - an X4T dependency leaf.
- **Why it is safe.** The allow grants nothing (L465:25). Every clause is the fresh path's own precondition, so the completed object is indistinguishable from a fresh creation. An empty object carries no content to adopt.
- **Rejected:**
  - quarantine-renaming the object and creating it afresh, which needs new names and has crash states of its own;
  - setting the mode or replacing the ACL, which would be a permission repair (OWN:120);
  - completing a non-empty directory, which this law cannot attribute to the owner's own crash.

**3.2 C-SUFFIX: completing an interrupted file write (predicate P-PREFIX).** For the marker (X2 item 6 step 5) and an X4T dependency leaf (X4T item 7).
- **P-PREFIX.** The object is a regular file that meets two conditions:
  - it satisfies P-ACL clauses 1 and 2, and its ACL is either omitted (then C-ACL runs first) or judged private;
  - its bytes, read through a bounded read of at most the expected length plus one, are a **strict prefix** (the empty prefix included) of the exact bytes the owner's step writes at that name. For the marker, those are the marker frame of the RESERVED row's ProjectId (`first_registration.rs:860`). For a leaf, they are the dependency's canonical bytes, whose digest the leaf's name addresses (`floor_publication.rs:253-261`).
- **Action.** Write the missing suffix at offset = the existing length. Then the file barrier (`F_FULLFSYNC`), the directory barrier, and an exact-length capped read-back that must equal the expected bytes, on the same device and inode. No existing byte is rewritten. The file only ever holds a prefix of its own content, or all of it.
- **Rejected:**
  - **an atomic replacement** (a temporary name, then a rename over the leaf). It would leave temporary names in the trust collections on a crash. The structural trust scan reads every name returned (`trust/directory_name_scan.rs`, `trust/directory_record_capture.rs:183-193`), and X4B rejects replacing records (X4B:125). The marker is no-replace by law (X2:247; REG:60);
  - **truncating and rewriting**, which destroys bytes before the new ones are durable;
  - **completing a non-prefix**, which is foreign or corrupt content.

**3.3 C-LEDGER: completing a ledger in which no OpenSIP writer ever committed a schema change (predicate L-UNC; r2, JRW-R1-01; r3, JRW-R2-01).**
- **L-UNC.** `ledger.sqlite` passes `open_store_file` (private, `store_custody.rs:251-274`) and is the retained, judged file (`same_file`). The engine opens it through item 2's own path, `configure_engine` (`ledger_store.rs:100-150`). That path runs SQLite's WAL recovery and sets defensive mode on (`:125-133`). Then **all** of these hold:
  1. **The schema cookie is 0.** `PRAGMA schema_version` returns 0. It reads "the schema-version integer at offset 40 in the database header" (SQ-PRAGMA), which is "the schema cookie" (SQ-FORMAT §1.3.9).
  2. The main schema holds **no object** (`whole_schema` is empty, `project_ledger.rs:377-386`).
  3. `page_count` is 1 and `freelist_count` is 0.
  4. `journal_mode` is `wal`, `encoding` is `UTF-8`, and `user_version` and `application_id` are 0.
- **What the cookie records (r3, JRW-R2-01).** SQLite's documentation says:
  - "SQLite automatically increments the schema-version whenever the schema changes" (SQ-PRAGMA);
  - "The schema cookie is a 4-byte big-endian integer at offset 40 that is incremented whenever the database schema changes" (SQ-FORMAT §1.3.9);
  - "For the purposes of this pragma, the VACUUM command is considered a schema change" (SQ-PRAGMA).

  **The counter wraps.** The bundled engine (SQ-SRC, SQLite 3.53.2):
  - adds 1 per schema statement, in unsigned 32-bit arithmetic: `(int)(1+(unsigned)…schema_cookie)` (`sqlite3.c:128449-128455`), stored by `OP_SetCookie` (`:100736-100741`);
  - adds 1 per VACUUM ("Add one to the old schema cookie", `:161652-161670`);
  - says so itself: "It is possible for the schema to change multiple times and for the cookie to be set back to prior value … 1 chance in 2^32" (`:128440-128444`).

  So a cookie of 0 alone proves only that the number of committed increments is a multiple of 2³². r2's claim that it proves no schema change ever committed, through any ordinary SQL writer, was an overclaim, and is withdrawn. L-UNC's history claim rests instead on the bound k below.
- **The bound k (r3).** Over a ledger's whole lifetime, OpenSIP's writers commit at most **k = 26** cookie increments.
  1. **One DDL transaction.** The only schema SQL any product path runs against a ledger is X3c item 2's DDL transaction: `write_schema` (`project_ledger.rs:452-509`) over the six fragments of `selected_ddl()` (`project_ledger.rs:33-43`). They hold 26 statements:
     - `ATTEMPT_DDL`: 4 (`ledger_store.rs:441-469`);
     - `PAIR_DDL`: 8 (`:476-503`);
     - `AVAILABILITY_DDL`: 5 (`:761-774`);
     - `recovery_material::DDL`: 4 (`ledger_store/recovery_material.rs:13-26`);
     - `recovery_pins::DDL`: 1 (`ledger_store/recovery_pins.rs:14-23`);
     - `pin_transactions::DDL`: 4 (`ledger_store/pin_transactions.rs:16-31`).

     That is 7 `CREATE TABLE`, 1 `CREATE INDEX` and 18 `CREATE TRIGGER`: `PAIR_DDL` creates two tables, `commit_receipts` and `commit_associations` (r4, JRW-R3-01; r3 said 6 and 19 in error). The per-fragment totals and k are unchanged.

     | Fragment | Tables | Explicit indexes | Triggers | Total |
     |---|---:|---:|---:|---:|
     | `ATTEMPT_DDL` | 1 | 0 | 3 | 4 |
     | `PAIR_DDL` | 2 | 0 | 6 | 8 |
     | `AVAILABILITY_DDL` | 1 | 1 | 3 | 5 |
     | `recovery_material::DDL` | 1 | 0 | 3 | 4 |
     | `recovery_pins::DDL` | 1 | 0 | 0 | 1 |
     | `pin_transactions::DDL` | 1 | 0 | 3 | 4 |
     | **Total** | **7** | **1** | **18** | **26** |
  2. **One increment per statement.** Each statement increments the cookie exactly once in the bundled engine:
     - `sqlite3EndTable` for a table (`sqlite3.c:129318`);
     - `sqlite3CreateIndex` only for an explicit `CREATE INDEX` (`:130875-130877`). A table's own constraint indexes add none;
     - `sqlite3FinishTrigger` for a trigger (`:158430`).
  3. **At most one commit per ledger.** Once the transaction commits, the file holds the selected schema. Every later open takes the `Existing` path (`project_ledger.rs:537-564`) and never re-enters `write_schema`. An attempt that never committed adds nothing.
  4. **No other product SQL changes a ledger's schema.** A census of product source at `cd5958b` (RW-C17) found:
     - In `crates/storage/src`, every `DROP` statement is inside a `#[cfg(test)]` module:
       - `ledger_store.rs:1746-2427` (module `tests`, from `:887-888`);
       - `ledger_store/immutable_guards.rs` (declared under `#[cfg(test)]` at `ledger_store.rs:2458-2459`);
       - `recovery_pins.rs:359-363` (from `:120-121`);
       - `recovery_material.rs:447`, `:504` (from `:339-340`);
       - `pin_transactions.rs:637`, `:751` (from `:185-186`, `:743`).
     - No `VACUUM`, `ALTER`, `ANALYZE`, `REINDEX`, `PRAGMA optimize`, `auto_vacuum`, `incremental_vacuum`, `writable_schema` or `schema_version` statement appears in any non-test, non-generated product source under `crates/*/src`. The only textual matches are generated contract field names and an unrelated reporting asset field (`crates/reporting/src/assets.rs:14`).
     - The security crate's `DROP` and `ALTER` statements act on the grant journal, never on the ledger. They are journal-store test modules, or `cfg(any(test, feature = "crash-matrix"))` test support (`journal_store/carrier_operation.rs:207-223`).
     - In production, only two paths open a ledger file: `open_existing` (`ledger_store.rs:151-176`) and `write_schema` (`project_ledger.rs:462`). Both run `configure_engine` with defensive mode (`ledger_store.rs:89-90`, `:125-133`; `project_ledger.rs:474`). The other connections are in-memory DDL comparisons, or test seams (`scenario.rs` under `scenario-fixtures`, `lib.rs:25-27`; `project_commit_census.rs` under the test-only crash-matrix build).
  5. **No migration exists.** X3c item 2 forbids one (X3C:85).

  So k = 26 < 2³².
- **The guarantee L-UNC establishes, and its threat model (r3, exact).**
  - **Established.** The file is OpenSIP's ledger name, under private custody at the owner's fixed path, under the writer lease, and created exclusively by `create_store_file`. Consider a ledger whose history since that creation is OpenSIP's writers' effects only:
    - its cookie starts at 0, which RW-C5 pins at both crash points;
    - it rises by exactly one per committed schema statement, to at most k = 26, with no wraparound.

    **So, for every OpenSIP writer, a recovered cookie of 0 means that no schema change committed.** Hence no table and no row, so no attempt row, receipt or other evidence, was ever committed in the file. Completing it creates the selected schema and nothing else, so it can never make a Run look committed. This meets X3c r8's CL-3 constraint (X3C:355).
  - **Not established:**
    - **who created the file.** Custody, not L-UNC, bounds that;
    - **any history written outside OpenSIP's writers.** A same-uid process that writes the ledger outside OpenSIP can return the cookie to 0 in three ways:
      - by raw bytes;
      - through a non-defensive connection's `PRAGMA schema_version=` or `writable_schema`;
      - with ordinary SQL, by committing 2³² − k or more schema changes. Codex's JRW-R2-01 counterexample is one: CREATE, INSERT and DROP, then 2³² − 2 VACUUMs.

      That actor is outside the custody threat model already: it can equally write a complete forged ledger with the selected DDL, which X3c item 2 admits today (X3C:85), or a receipt, or a marker. L-UNC claims no more than X3c's own stored-schema check does;
    - **power-loss states** (X9 L1).
  - **Withdrawn from r2:** "not reachable" for wraparound, and the claim that the guarantee holds against "any writer that changes the schema only by SQL schema statements or VACUUM".
- **Keeping k true (r3).** RW-C17 (item 9) re-takes the census of product SQL on every change, and RW-C5 pins the cookie at 26 after creation.
  - **Owner.** J4c authors RW-C17. X3c's law owner (storage) keeps it.
  - **The rule.** Any unit that adds schema-changing SQL to a ledger path must re-establish k and L-UNC in its own review. That means a `VACUUM`, `DROP`, `ALTER`, `ANALYZE` or `REINDEX`, a migration, or a `CREATE` outside `selected_ddl()`. The same holds for a ledger connection without defensive mode. RW-S3 writes this rule into X3c r9's forbidden substitutes.
- **What it is.** This is the committed view at `x3c.ledger-create.wal`. There, `PRAGMA journal_mode=WAL` has written the header page and no transaction has committed since. It is also the view at `ddl.commit.before`, because recovery does not apply WAL frames that lack a commit record. Both views are pinned (stop rule, below), not assumed.
- **Action.** X3c item 2 steps 2 to 5 on that file:
  - `write_schema` from its `BEGIN IMMEDIATE` (`project_ledger.rs:452-509`). Selecting WAL again is a no-op;
  - then the namespace barrier and `open_verified`.

  The disposition is a new value, `Completed`, beside `Resumed` (`project_ledger.rs:348-356`).
- **Stop rule and fallback (lead direction).** Before C-LEDGER is enabled, J4c pins every L-UNC observable, the cookie included, at **both positive crash points**, with the bundled engine. It also pins the **negative fixtures** of RW-C5, the compacted-history counterexample among them.
  - **If either positive view fails any observable, C-LEDGER is withdrawn.** RW-L1 then keeps `LEDGER.CORRUPT` as neighbour **N-L0** (item 5). J4c lands only the negative controls, and L11 stays open, narrowed to that state (item 10).
  - The predicate is never widened to fit a run.
- **Basis.** X3b's carrier already resumes "an empty database … only if it holds no schema objects" (X3B:86; `carrier_floor.rs:405-425`; `carrier_dispatch.rs:153-163`). L-UNC is stricter: no schema object of any name, no freelist page, **and, within the bound k, no schema history committed by an OpenSIP writer**.
- **Rejected:**
  - **r1's L-UNC without a history discriminator** (JRW-R1-01). Current emptiness does not prove that nothing committed.
  - **The file change counter (header offset 24) as the discriminator.** "In WAL mode, … the change counter might not be incremented on each transaction" (SQ-FORMAT §1.3.6).
  - **The cookie alone.** It says nothing about the creation footprint. Clauses 2 to 4 stay.
  - **(r3) Withdrawing C-LEDGER now, because the cookie wraps.** Within the stated threat model the bound argument is sound, and withdrawal would leave L11 open for two crash points.
  - **(r3) A 2³²-iteration stress run.** It proves nothing that k does not, and the bound is checked by RW-C17's census and RW-C5's pin of 26 instead.
  - **(r3) A separate creation-history record beside the ledger.** It is a new state class with no custody owner.
  - **Renaming the file aside and creating afresh.** It leaves an unadmitted file in the namespace and adds a rename to the store.
  - **Deleting the file.**

**3.4 C-REG: completing an ordinary reservation (the reservation join; r2, JRW-R1-02).** It runs under the write gate, after X2 item 5's one capture and whole-document validation (no early match). The join is decided in full **before any effect**: before C-ACL, C-SUFFIX or namespace publication.
- **The join.** All of these hold:
  1. Exactly one relevant live row, by item 4's relevance rule (`project_admission.rs:688-704`). Its status is RESERVED and its `allocationKind` is `random`.
  2. The row's locator (platform, path bytes) and incarnation (volume UUID, inode, birth) agree with the admitted root.
  3. **(r2) The namespace and the marker, together.** Exactly one of these holds:
     - **(a)** `I/host/projects/N` (N the row's `namespaceId`) is positively absent, **and** the marker is positively absent;
     - **(b)** N is present with exactly X2 item 6's complete footprint: a private directory with exactly two empty private lease files (`first_registration.rs:1551-1621`; REG:70). The marker is absent, exact with the row's ProjectId, or a file satisfying P-PREFIX against the row's marker frame.

     Every other combination is not the join. In particular, **a present marker of any form, with N absent**, is never the join: exact, zero-length, a strict prefix, ACL-omitted or private (N-R2, N-R9).
     - X2 item 6 publishes and confirms the complete N in step 3, before step 5 even creates the marker (X2:238-247). The product enforces that order (`first_registration.rs:2260-2293`).
     - So under process death, any present marker implies a complete N. REG:76 already refuses the exact-marker case for that reason.
  4. `I/host` and `I/host/projects` are each absent, private, or P-ACL.
  5. X2 item 6's preconditions hold: the active-transition gate (`first_registration.rs:1310`), capacity for the ACTIVE document, item 6a's tracking observation (the marker path untracked), and the recheck set.
- **Action.** Run X2 item 6's remaining steps from the first incomplete one. The registry owner R is taken from item 5's capture, which already holds the RESERVED row.
  - **Step 3,** only in case (a). Parents are created or admitted, with C-ACL where P-ACL holds. Then N is published from positive absence through a **fresh** stage. In case (b), the complete N is admitted, and its own and `projects`' barriers are reconfirmed (REG:70).
  - **Step 4:** `.opensip` is created or admitted.
  - **Step 5:** the marker is created; or completed by C-ACL and C-SUFFIX, only in case (b); or, when exact, its file barrier and `.opensip`'s and the root's barriers are reconfirmed.
  - **Step 6:** every current owner is rechecked, then RESERVED becomes ACTIVE through X2's replacement primitive, with a fresh temporary file.

  Item 7's namespace admission and the handoff then follow, as after a fresh registration.
- **What it never does:**
  - It never touches an unpublished stage or a temporary file left by the crash (REG:70; `first_registration.rs:1228`).
  - It never moves, abandons or rewrites the row except to its ACTIVE.
  - It never converts a random row to an adopt row, or the reverse.
  - It never acts on a present marker while N is absent.
- **On every path other than this step,** admission's classification and its row are exactly today's. A zero-length marker therefore still reads `marker-custody` or `identity-contradiction` to `doctor` and to read sessions (control RW-C4).

**3.5 C-TRUST: completing a dependency leaf at a re-written name.** At `write_dependency` (`floor_publication.rs:459-488`), when the name is present:
- **The predicate.** The leaf satisfies P-PREFIX against `bytes`, and its ACL is omitted or private.
- **Action.** C-ACL if the ACL is omitted, then C-SUFFIX.
- **Why the leaf cannot be referenced.** The fenced first read admitted a closure that does not name it: a named, torn leaf would have refused that read as incomplete (X4T:216). **(r4)** That holds on both of the read's ends. The closure is read and authenticated by items 1 to 5, before item 6's clock decision, so a clocked refusal comes only after the same closure has been admitted (X4T:170-171). The publication writes only its own determined list of names (X9:146-153). J4d asserts this and adds no read (control RW-C14).
- **What is never visited.** A torn leaf at a name no later publication writes stays unreferenced and harmless, as today (X4B:127; `floor_publication.rs:513-517`).
- **The shared protocol.** X4B's acceptance publication uses the same protocol, with one owner (X4T:169), and gains the same completion. Nothing is deleted, so X4B:130's "no deletion" holds unchanged.
- **(r4) On the clocked path.** C-TRUST also runs when the publication is X4T r12's write-ahead before a clocked refusal (item 2). The completed publication is followed by that refusal, unchanged, and never by a view.

**3.6 C-TDIR: completing a trust-publication directory (r2, JRW-R1-03).** At `parent_dir` (`floor_publication.rs:416-451`), before `write_dependency`:
- **The state.** A publication creates a missing parent only where `may_create` permits it (`floor_publication.rs:406-414`):
  - the `trust/publications/by-predecessor` bucket;
  - its predecessor directory `by-predecessor/<P>`, where P names the publication's predecessor, the current `state.v1`;
  - `trust/objects`, which X4B-a's first acceptance creates.

  Each is created by `create_private_directory` (`private_access.rs:209-238`): `mkdirat 0700`, then the zero-rights owner allow. A kill at the census point `x4t.floor-publication.dependency/create.after` on a directory occurrence leaves the directory empty, `0700`, with its ACL omitted. The pointer was never replaced, so `state.v1` and its admitted closure are unchanged.
- **Today.** The next fenced first read admits the unchanged closure. **(r4)** It ends either in a view or in X4T r12's clocked refusal, and either end performs the write-ahead when S4 proposes a change. It never opens the current capsule's successor bucket: X4T rejects probing `trust/publications/by-predecessor/<sha256 of this state.v1>` (X4T:193), and its read set is reference-directed (X4T item 2).
  - The next publication from the same pointer needs the same directories (X9:146-153). Every floor write-ahead from that pointer writes its descriptor under the same `<P>`.
  - So `parent_dir` calls `open_private` (`:434`). It judges the existing directory (`:158-172`), and the omitted ACL refuses `TrustRow::Incomplete`, that is `installation-incomplete` (`:170`; `private_access.rs:55`).
  - That happens at every later publication from that pointer: at every later durable request whose fenced read must advance the floor (X4T item 7). It is installation-wide.
- **Census.**
  - **The predecessor directory** occurs once in each pinned census child that publishes:
    - storage `dependency/create.after#6` (`census-trace.txt:112`), followed by its own and its parent's barriers (#6, #7) and the descriptor file (#7, `:113-118`). The same point identity recurs in the refused-end child (`:1256`): one point, two physical records (r3, NB-01);
    - host `#5` in traces `-a` and `-b` (`census-trace-a.txt:40`, `census-trace-b.txt:40`), followed by barriers #5 and #6.
  - **No kill set samples them** (storage #1, #4, #7; host #1, #3, #6), so no run executed this state.
  - **The bucket and `trust/objects`** occur in neither pinned census: the fixtures' stores are already accepted, so no census child runs X4B-a's first acceptance. They are covered by the same rule and by J4d's in-process controls (RW-C15).
- **The predicate.** All of these hold:
  - the name is one that `may_create` permits at that depth;
  - **(r3, JRW-R2-02)** `open_private`'s native open has succeeded, returning the retained directory (`floor_publication.rs:164-166`);
  - P-ACL holds, observed on that retained handle: an empty directory, owned by the invoking user, `0700`, ACL omitted, on its parent's filesystem;
  - the publication has reached that parent step under the held fence, whichever end the fenced read will take: an admitted view, or **(r4)** X4T r12's clocked refusal, which is returned unchanged after the publication confirms (item 2).

  A native open failure is never reclassified or completed. That includes a symlink (`O_NOFOLLOW`) or a non-directory (`O_DIRECTORY`) at the name (`crates/platform/src/filesystem/directory_open.rs:61-73`, `:134-150`).
- **Action.** C-ACL. Then the creation path's own barrier and its parent's (`floor_publication.rs:439-446`). Then the publication continues, to `write_dependency` and the pointer.
- **Why trust admission is not relaxed.** The fenced read admits exactly what it admits today, and **(r4)** refuses exactly what it refuses today. The completion runs after that read's authentication and time admission, inside the publication protocol's own step, under the fence (X4T:169). On the clocked path the read's own refusal follows, unchanged (item 2). It touches a directory that the admitted closure does not name, and skips no trust check. **(r3, JRW-R2-02) Every other outcome keeps its row today:**
  - a native open failure keeps the host I/O row, `HOST.IO_FAILURE` (`floor_publication.rs:164-166`; `current_trust_admission.rs:100` at `cd5958b`). That covers a symlink or a non-directory at the name (N-T2a);
  - an opened directory whose judgment fails other than by P-ACL keeps `installation-incomplete` (`floor_publication.rs:170`; `current_trust_admission.rs:107`) (N-T2b);
  - a budget failure keeps the budget row (`floor_publication.rs:58-69`).

  These are X4T item 10's preserved rows, unchanged from r11 to r12 (X4T:216, :233).
- **Rejected:**
  - **retaining the state as a residual L11 limit.** That leaves an installation-wide permanent refusal in a family this law claims;
  - **completing any parent directory.** Every parent outside `may_create` must already exist, from P0 or from a completed publication (`floor_publication.rs:406-409`);
  - **renaming the directory aside.** That needs a new name in the trust tree.

### 4. The crash states, the writer's action and the terminal state

The counts are of X9-2's sampled F00 kill set (EV), 57 in all. Each state covers every census occurrence in its window, not only the sampled ones (item 1). "Today" is the next writer's row at `d2c00a9`, the same as at `e093e90`. "Terminal" is what the next admitted durable write reaches.

| State | Window and the object it leaves | Kill points in the kill set | Today | Writer action | Terminal |
|---|---|---|---|---|---|
| **RW-R1** | RESERVED visible; N absent (a stage may be left); **no marker**. From `x2.fence.register.reserved/rename.after` through the namespace step before its publication | 25 for RW-R1 to RW-R3 together: `reserved/rename.after`, `reserved/directory-barrier.*`, and the `namespace/*` points. X9 r17's transcription assigns each one by its object (item 10). | `identity-recovery-required` | C-REG from step 3: parents, a fresh stage published to N, `.opensip`, marker, ACTIVE | ACTIVE (R2), Eligible, then Committed |
| **RW-R2** | As RW-R1, with `I/host` or `I/host/projects` created but not private | within the 25, at `namespace/create.after` of a parent | `identity-recovery-required` | C-ACL on that parent inside C-REG, then as RW-R1 | as RW-R1 |
| **RW-R3** | RESERVED; N published with its complete footprint, its barriers possibly pending; no marker. From `namespace/link.after` | within the 25 | `identity-recovery-required` | C-REG: admit N, reconfirm its and `projects`' barriers, then step 4 | as RW-R1 |
| **RW-R4** | RESERVED; N complete; `.opensip` created or admitted (under the S3 premise); marker absent. `marker-directory/*`, `marker/create.before` | 7 | `identity-recovery-required` | C-REG from step 5 | as RW-R1 |
| **RW-R5** | RESERVED; **N complete**; marker zero-length, ACL omitted. `marker/create.after` | 1 | `marker-custody` | C-ACL, then C-SUFFIX on the marker; step 6 | as RW-R1 |
| **RW-R6** | RESERVED; **N complete**; marker private, empty (or a strict prefix). `marker/write.before` | 1 | `identity-contradiction` | C-SUFFIX on the marker; step 6 | as RW-R1 |
| **RW-R7** | RESERVED; **N complete**; marker exact; ACTIVE not visible (an ACTIVE temporary may be left in I). `marker/write.after` through `active/rename.before` | 12 (5 `marker/*`, 7 `active/*`) | `identity-recovery-required` | C-REG: reconfirm the marker's and parents' barriers, recheck, ACTIVE with a fresh temporary | as RW-R1 |
| **RW-P1** | An X3c store directory (`projects`, `projects/N`, `objects`, `objects/sha256`) created, empty, ACL omitted | 4: `x3c.ledger-create.projects/create.after`, `.namespace/create.after`, `x3c.object.objects/create.after`, `x3c.object.sha256/create.after` | `Custody { subject: "private" }` | C-ACL, then create-or-admit's remaining checks and barriers | layout admitted; Committed |
| **RW-P2** | `ledger.sqlite` created, length 0, ACL omitted, no `-wal` | 1: `x3c.ledger-create/create.after` | custody `private` | C-ACL, then X3c item 2's resumable-empty path | ledger created; Committed |
| **RW-P3** | `I/trust/carrier-floors/` created, empty, ACL omitted. Installation-wide. | 1: `x3b.floor.directory/create.after` | X3b's host I/O row | C-ACL under the fence, then the floor write | floor written; Committed |
| **RW-L1** | `ledger.sqlite` private, WAL header only, schema cookie 0, no committed schema. At `ddl.commit.before`, uncommitted frames are in `-wal`. | 2: `x3c.ledger-create.wal`, `x3c.ledger-create.ddl.commit.before` | `LEDGER.CORRUPT` | C-LEDGER, only if J4c's pins hold (item 3.3); otherwise none (N-L0) | ledger with the selected schema; Committed |
| **RW-T1** | A dependency leaf at a name the next publication writes: zero-length, ACL omitted | 1: `x4t.floor-publication.dependency/create.after#1` | `installation-incomplete` | C-ACL, then C-SUFFIX | publication confirmed; then Committed, or **(r4)** X4T r12's unchanged clocked refusal if the read clock-refuses (item 2) |
| **RW-T2** | The same leaf private and torn (a strict prefix) | 2: `dependency/write.before#1`, `#3` | `installation-incomplete` | C-SUFFIX | as RW-T1 |
| **RW-T3 (r2)** | A trust-publication directory that `may_create` permits, created, empty, ACL omitted; the pointer unchanged. Installation-wide. | 0 sampled. Three trace/point selections: storage `dependency/create.after#6`, host `#5` in traces `-a` and `-b`. Four physical events, because storage's #6 recurs in the refused-end child (r3, NB-01). | `installation-incomplete` at the next publication | C-TDIR: C-ACL at `parent_dir`, then its barriers | publication confirmed; then Committed, or **(r4)** X4T r12's unchanged clocked refusal (item 2) |

46 R + 6 P + 2 L + 3 T = 57 sampled points, plus RW-T3's three unsampled trace/point selections (four physical events). Leaves at names the next publication does not write (for example `dependency/write.before#6`) are already Committed and are not visited.

### 5. States the writer keeps refusing (the safety bias)

When a state is not exactly one of item 4's, the writer does nothing, and the request ends on today's row with today's subject. The row is the disclosure.

| Neighbour | Today's row, unchanged | Why it is not completed |
|---|---|---|
| **N-R1** An adopt-kind RESERVED row | `identity-recovery-required` | REG:76 requires a fresh admitted adoption context |
| **N-R2** RESERVED, an exact marker, N absent | `identity-recovery-required` | not a lawful crash prefix (REG:76) |
| **N-R3** RESERVED, N present but not exactly the complete footprint (an extra entry, a missing or non-empty lease, not private, a symlink) | `identity-recovery-required` | "an occupied incomplete or foreign namespace is unavailable" (REG:70) |
| **N-R4** RESERVED, a marker that is **neither exactly equal to nor a strict prefix of** the row's frame (r2, NB-02) | `identity-contradiction` | foreign or corrupt content |
| **N-R5** A RESERVED row whose locator or incarnation disagrees with the root (moved, re-cloned) | `identity-contradiction` | REG's move or abandonment, which needs user authorization |
| **N-R6** More than one relevant live row; ACTIVE with no marker; a marker with no row | `identity-contradiction` / `identity-recovery-required` | not a crash state of one registration (REG:41-43) |
| **N-R7** A zero-length or prefix marker with no matching RESERVED row | `marker-custody` / `identity-contradiction` | nothing proves it is OpenSIP's |
| **N-R8** A tracked marker path | `marker-tracked` | X2 item 6a |
| **N-R9 (r2)** RESERVED, N **absent**, and a marker present that is not exact: zero-length or a strict prefix, ACL omitted or private | `marker-custody` (ACL omitted, `project_admission.rs:602-603`) / `identity-contradiction` (private, `:616`, `:684-685`) | not a lawful crash prefix: the complete N precedes the marker (X2:238-247; `first_registration.rs:2260-2293`; REG:76) |
| **N-P1** A P-ACL candidate that is non-empty, has the wrong owner, mode or link count, is on another filesystem, is a symlink, or has a present non-private ACL | today's custody row for its owner | not the fresh path's own prefix |
| **N-P2** `ledger.sqlite` at length 0 with a `-wal` beside it | `LEDGER.CORRUPT` | X3c item 2, unchanged (`project_ledger_tests.rs:294-298`) |
| **N-L0 (r2, conditional)** RW-L1, if J4c's pins fail (item 3.3) | `LEDGER.CORRUPT` | C-LEDGER withdrawn; L11 stays open, narrowed to this state |
| **N-L1** Any committed schema object; a freelist page; more than one page; another journal mode or encoding; a nonzero `user_version` or `application_id`; not a database | `LEDGER.CORRUPT` | committed history, or not OpenSIP's creation (`project_ledger_tests.rs:292-340`) |
| **N-L2 (r2)** Any schema cookie other than 0, including an empty, one-page, free-page-less database whose history was compacted (CREATE, INSERT, DROP, VACUUM) | `LEDGER.CORRUPT` | committed schema history (JRW-R1-01; SQ-PRAGMA) |
| **N-T1** A leaf whose bytes are **neither exactly equal to nor a strict prefix of** the publication's bytes (r2, NB-02); a non-regular leaf; the wrong owner, mode or links | `installation-incomplete` | foreign or corrupt content (X4T:216). An exactly equal private leaf is today's ordinary admission (`floor_publication.rs:470-481`) |
| **N-T2a (r3, JRW-R2-02)** A symlink or a non-directory at a publication-parent name. `open_private`'s native open fails (`O_NOFOLLOW`, `O_DIRECTORY`; `crates/platform/src/filesystem/directory_open.rs:61-73`, `:134-150`). | the host I/O row, `HOST.IO_FAILURE` (`floor_publication.rs:164-166`; `current_trust_admission.rs:100` at `cd5958b`) | never reaches the custody judgment, so it is never reclassified or completed (X4T:233) |
| **N-T2b (r2; r3 scope)** A directory that opens and reaches the custody judgment, but fails it other than by P-ACL: it holds any entry with its ACL omitted; it has the wrong owner or mode; its ACL is present and not private; or it is ACL-omitted at a name `may_create` does not permit (for example `trust/records`) | `installation-incomplete` (`floor_publication.rs:170`; `current_trust_admission.rs:107` at `cd5958b`) | not a publication's own interrupted creation |
| **N-X1** An active transition slot | the incomplete row | S9.2's transition recovery |

### 6. Idempotence, crash during repair, cancellation and concurrency (law)

The X9 rows of item 10 cover each rule.
- **CR-1. A crash inside a completion stays in its family.** Each completion effect is one of the owner's own steps on the same object. A kill inside it leaves the same state, the next state of the same family, or the completed object. The next admitted write completes it.
  - C-ACL killed after the append leaves a private object. That covers C-TDIR too: a private, empty predecessor directory is admitted by `open_private` as today.
  - C-SUFFIX killed mid-write leaves a longer prefix.
  - C-LEDGER killed before `COMMIT` leaves L-UNC again, with the cookie still 0, because the schema change never committed.
  - C-REG killed in step 3 leaves RW-R1, RW-R2 or RW-R3 (marker still absent). Killed in step 4 or 5, it leaves one of RW-R4 to RW-R7 (N complete). Killed at its ACTIVE rename, it leaves RW-R7, or ACTIVE.
- **CR-2. Monotone, so it terminates.** Every completion moves its object forward along the owner's step order, and never back:
  - the registry row: RESERVED to ACTIVE;
  - the ACL: omitted to private;
  - file bytes: a prefix, to a longer prefix, to complete;
  - the schema: empty to selected.

  No state recurs after a later one. A run of crashes cannot cycle, and each completion that returns leaves strictly less to do.
- **CR-3. Idempotent.** A completion over an already completed object is the owner's ordinary admit path: no effect, and only the observation is charged. A second request after a completion performs no completion for that object.
- **CR-4. No retry inside a process.** A completion's failed or uncertain step latches its owner's ledger, as any of that owner's steps does (X2:212; X3C item 7). The request ends on that owner's row, and a later request resumes.
- **CR-5. Cancellation.** Every completion runs in J1's phase A, before attempt admission (J1:500). A signal during a completion lets the native effect in flight finish. The request then ends `interrupted` 130 with no runId (J1:661), and the state is resumable by CR-1.
- **CR-6. Concurrency.** Completions run only under the fence (R, RW-P3, RW-T1 to RW-T3) or the namespace writer lease (RW-P1, RW-P2, RW-L1), so a competing writer gets its busy row. A fence-free `recover(ExecutionId)` reading a ledger during C-LEDGER sees one of two lawful views: before the commit, `ledger-unreadable` (UC); after it, no attempt row (UAU) (X6 item 4).
- **CR-7. Stacking.** Several families can be pending after successive crashes. One request completes them in J1's order (R9, then R10, then `admit_layout`). Each completion touches only its own owner's objects.

### 7. Disclosure, `doctor` and the operational record (lead decision)

- **No public surface changes.** There is no new code, class, exit, detail, subject, envelope member or remedy text (J1:689). A completed request's envelope is an ordinary one.
  - Completing a registration is not installation creation, so J1's `firstUse` stays false (J1:588).
  - A refusal keeps its existing row and subject, which is the disclosure the safety bias asks for.
- **The operational record.** Each completion emits one event, `host.repair.completed`, with:
  - `kind`, from a closed code table: `registration`, `store-directory`, `ledger-file`, `ledger-schema`, `carrier-floors`, `trust-directory` (r2), `trust-dependency`;
  - `state`, the item 4 state ID.

  It carries no path, ProjectId or bytes. It is an ordinary registration under SOP2 (SOP2:226-231), reviewed in J4's units. Until S-OP-1 the sink is nonpersistent (OPP:209-216).
  - **No new edge.** S-OP-2's registry lands with O1 (M3P:314, day 4). A J4 unit that integrates before O1 returns the completion in its typed result only. The first J4 unit after O1, or O1 itself, adds the event. J4 gains no edge on O1.
- **Recovery never reads logs or crash records** (OPP:209, :311). Every predicate is a fresh observation of the owner's own objects.
- **`doctor` is unchanged.** It writes nothing (OPP:214), and it reports today's rows for these states. The next admitted durable request completes them. This is a stated limit, not a defect.
- **Rejected:**
  - **a new detail, subject or envelope member** ("repaired"): it would be a new public code, and it gives the user nothing to act on;
  - **no record at all:** support then could not tell a resumed project from a fresh one.

### 8. Rows and budget (law)

- **No new row.** Every refusal is an owner's existing row (X2 item 8; X3C item 10; X3B item 8; X4T item 10), now with narrower reach:
  - `identity-recovery-required`, `marker-custody` and `identity-contradiction` no longer arise from RW-R1 to RW-R7 on the write gate;
  - custody `private` no longer arises from RW-P1 or RW-P2;
  - X3b's host I/O row no longer arises from RW-P3;
  - `LEDGER.CORRUPT` no longer arises from RW-L1, unless N-L0 applies;
  - `installation-incomplete` no longer arises from RW-T1, RW-T2 or RW-T3.
  - **(r3)** X4T item 10's host I/O and budget rows are unchanged (X4T:233; r11's rows, kept in r12). N-T2a keeps `HOST.IO_FAILURE`.

  Each row's text, class and exit are unchanged.
- **Budget.** Each completion is charged to its owner's ledger before it runs, and reserves its post-effect confirmations, as the owner's own step does (X2 item 9; X3C item 9; X4T item 11). Its read of an existing prefix is bounded by the expected length plus one. If the reservation cannot be taken, the request refuses `WORK.BUDGET_EXHAUSTED` before the completion's first effect.

### 9. Controls

All of these run on scratch installations with labelled synthetic signed profiles and fixtures, as X2c's, X3c-1's, X3b's and X4T's tests do. No production seam is added.
- **RW-C1, each state.** Build each item 4 state, by the owner's crate-private step hooks or a matrix child, then run the owner's step. It completes to the terminal state. The test asserts that the only effects are the owner's own step effects on the named objects: nothing is deleted, and no name is created beyond the owner's own step (the fresh stage, the ACTIVE temporary).
- **RW-C2, each neighbour.** Each item 5 neighbour gives today's row and subject byte for byte. It writes nothing beyond the request's earlier lawful effects.
- **RW-C3, idempotence.** A completion over a completed object performs no effect. A second request performs no completion. CR-3.
- **RW-C4, read paths.** Run the 458c read session, `doctor` (core and project modes), `recover(ExecutionId)`, the sweep and the ephemeral entry over every item 4 state. Each one writes nothing and gives today's outcome byte for byte.
- **RW-C5, L-UNC pins (r2).** These run with the bundled engine, before C-LEDGER is enabled.
  - **Positive:** the committed views at `x3c.ledger-create.wal` and `ddl.commit.before` each satisfy every L-UNC clause, schema cookie 0 included. The test records each observable.
  - **(r3) The bound k:** at `x3c.ledger-create.ddl.commit.after`, the completed ledger's cookie is exactly 26 = k, one per `selected_ddl()` statement. This checks item 3.3's per-statement count against the bundled engine. A different value stops J4c, as a failed positive view does.
  - **Negative,** each `LEDGER.CORRUPT` and each failing L-UNC:
    - every fixture of `every_other_creation_footprint_is_ledger_corrupt` (`project_ledger_tests.rs:292-340`);
    - **the compacted-history counterexample:** CREATE TABLE, INSERT, DROP TABLE, VACUUM, each committed;
    - CREATE then DROP then VACUUM;
    - CREATE alone;
    - `user_version = 1`;
    - `application_id = 1`.
  - Each negative fixture's cookie is recorded.
  - **Defensive mode:** a product ledger connection's `PRAGMA schema_version = 0` and `PRAGMA writable_schema = ON` leave the file unchanged.
  - Item 3.3's stop rule and fallback apply.
- **RW-C6, P-ACL.** Negating each clause in turn refuses on today's row. Metadata before and after shows exactly one zero-rights owner allow appended, and no mode bit changed.
- **RW-C7, P-PREFIX.** The prefix's inode and bytes are unchanged and only the suffix is written. A neither-equal-nor-prefix file refuses. An exactly equal file takes the ordinary admission.
- **RW-C8, authorization.** Adopt-kind and identity-changed reservations refuse. C-REG compiles only against the write gate's `OrdinaryWriteAdmission` path: a compile-fail fixture shows that no read receipt reaches it.
- **RW-C9, no Run manufactured.** After every completion the ledger holds only what the request's own commit wrote. `recover` of a killed child's ExecutionId never reports committed.
- **RW-C10, census.** The lawful first commit's census (X9-0's) is unchanged by J4. Every new durability point lies under a `.repair` scope (item 10). Release absence covers the new scope names.
- **RW-C11, cancellation.** A phase-A signal during each completion ends `interrupted`, and the next request completes the state. CR-5.
- **RW-C12, budget.** An unreservable completion refuses on the budget row before its first effect.
- **RW-C13, the record.** Each completion emits exactly one `host.repair.completed`, with no path or identity in it.
- **RW-C14, trust names.** C-TRUST and C-TDIR create no new name in any trust collection. After a killed C-TRUST, the structural name scan sees only canonical names. A leaf the admitted closure names is never a strict prefix at publication time. **(r4)** That holds on the clocked path too.
- **RW-C15, trust directories (r2; r3, JRW-R2-02).** C-TDIR completes each of the three `may_create` directories: the bucket, the predecessor directory, and `trust/objects` on an X4B-a acceptance. The fenced read before it ends exactly as today: an admitted view, or **(r4)** X4T r12's clocked refusal. Each neighbour keeps its row today, on either end:
  - N-T2a (a symlink, or a regular file, at the name) keeps `HOST.IO_FAILURE`;
  - N-T2b's opened directories keep `installation-incomplete`;
  - a budget failure at the step keeps `WORK.BUDGET_EXHAUSTED`.

  C-ACL is never applied after a native open failure.
- **RW-C16, join order (r2).** Before any effect, C-REG refuses each case of N-R2 and N-R9 on its existing row: an exact, zero-length, strict-prefix, ACL-omitted or private marker with N absent. The installation is byte-unchanged afterwards.
- **RW-C17, the product-SQL census (r3, JRW-R2-01).** This is a code-inspection lint in storage's ordinary test lanes, with no 2³² loop. **Owner:** J4c authors it; X3c's law owner (storage) keeps it. It asserts three things:
  1. **The DDL (r4, JRW-R3-01).** The census enumerates, by kind and name, the `CREATE` statements that `selected_ddl()` actually selects. It asserts exactly 26: 7 tables, 1 explicit index and 18 triggers. That is k.
     - The expected list is item 3.3's table, with every statement named: the tables `attempt_custody`, `commit_receipts`, `commit_associations`, `evidence_availability`, `commit_run_material`, `active_run_pins` and `pin_change_facts`; the index `availability_latest`; and the 18 named triggers.
     - A mismatch fails the census. The product DDL is never changed to fit this text.
  2. **No other schema SQL.** No product source under `crates/*/src` issues `VACUUM`, `DROP`, `ALTER`, `ANALYZE`, `REINDEX`, `PRAGMA optimize`, `auto_vacuum`, `incremental_vacuum`, `PRAGMA schema_version=` or `writable_schema`, nor any `CREATE` outside those fragments, on a ledger path. Excluded from the scan: `#[cfg(test)]` modules, `cfg(any(test, feature = …))` test support, and `generated/` code.
  3. **Only defensive openers.** The only production openers of a ledger file are `open_existing` and `write_schema`, and both run `configure_engine` with defensive mode.

  A unit that makes any of these fail must re-establish k and L-UNC in its own review (item 3.3, "Keeping k true").
- **RW-C18, completion before X4T r12's clocked refusal (r4, JRW-R3-02).** Build each of RW-T1, RW-T2 and RW-T3 in an authenticated store where S4 proposes a floor advance and `EV-CLOCK` at tEval refuses, for example `core:expired` or `core:stale-revocation`. In each case:
  - the completion runs and the floor publication confirms, and the owner advances (X4T:171, :173);
  - the read then returns X4T r12's clocked continuation refusal, unchanged: request-rejected, exit 2, `CONTINUE-CORE-NOT-TRUSTED`, with its role subject (X4T:218-221);
  - no view is returned, and no lease, X3b floor step, carrier start or later operation effect follows (X4T:205);
  - a second fenced read refuses again at tEval′ ≥ tEval (X4T:174).

  This mirrors the integrated X4-F2 test `a_clocked_refusal_comes_after_its_confirmed_write_ahead_and_is_sticky` (`floor_publication_tests.rs:801-852` at `d2c00a9`), which was inspected, not run.
- **RW-C19, the clocked path's failures and its effect-free reads (r4, JRW-R3-02).** On the same clocked route, each failure keeps its own row, which `publish` returns before `into_view` (`floor_publication.rs:993`):
  - N-T2a, a symlink or non-directory at a parent name: `HOST.IO_FAILURE`;
  - N-T2b, a failed custody judgment: `installation-incomplete`;
  - N-T1, a non-prefix leaf: `installation-incomplete`;
  - an unreservable step: `WORK.BUDGET_EXHAUSTED`.

  None of them becomes the clocked refusal, and none completes anything. Two kinds of read stay effect-free, writing nothing and completing nothing (X4T:172):
  - a refusal raised before time is admitted: items 2 to 5, the stored-state join, and S4's steps 1 to 4;
  - a report-only read over the same store.
- **J-C22 (J3d's, answering J1:691). One host durable request over an RW-R5 fixture ends Committed, with one receipt and an ordinary envelope (`firstUse: false`). One over an N-R2 fixture ends on `identity-recovery-required`, with nothing written.

### 10. X9 r17 rows (record)

These are the rows X9 r17 carries for J-RW. They form a named section beside J1's `S12-` rows (J1:708-714, :733) and X3c r8's `RC-` rows (X3C:262-325, :354).
- Each row is transcribed into `required-runs.v1.json` before any run, and none is ever read back from a run (X9:1089, :1233).
- All are storage-target rows, driven by the existing `commit` driver. No fourth driver entry is added (X9:1236).
- Every RW row commits each Run once per namespace, so none is a re-commit (X3C item 6a).

The rows:
- **RW-F00, F00 re-transcribed.** F00's 57 L11 kill points (item 4), killed as F00 kills them:
  - **R2** becomes Committed. R2's run record names the completions it performed, taken from the product's typed completion results, never from a filesystem diff;
  - **R3** as F00's Committed cells, scored against the killed attempt;
  - **R1** as F00 r5;
  - **R4** returns to F00 r5's UAU at the seven `x3c.*` points (RW-P1, RW-P2, RW-L1), where R2 now creates the ledger. X9 r8's "R4 stays UC" clause is withdrawn for them.

  The other F00 cells stand. Each point's state is assigned by its object, from the same unarmed reference run X9 r9 uses for dependency occurrences (X9:146-153). If N-L0 applies, RW-L1's two points keep F00 r8's `LEDGER.CORRUPT` cells.
- **RW-D1 (r2), the trust-directory state.** Child 1 is held, then killed, at storage `x4t.floor-publication.dependency/create.after#6`, the predecessor-directory occurrence (item 3.6). This point is outside F00's sampled kill set, so the row names it explicitly. The row arms it in the commit child. The refused-end child's record of the same point (`census-trace.txt:1256`) leaves the same RW-T3 state and needs no second row (r3, NB-01). X9:146-153 already foresaw "a later census that puts one there … under X4T's parent-directory step".
  - **R2** is Committed, naming the completion `trust-directory`.
  - **R1 and R4** are not applicable: the floor publication runs before the ExecutionId draw.
  - **R3** as F00's Committed cells.
- **RW-K1 to RW-K10, crash during repair.** A three-child ladder:
  1. child 1 is killed at a start point;
  2. child 2, the repairing writer, is held, then killed at every durability point of its `.repair` scopes;
  3. child 3 commits.

  Start points:
  - RW-K1: `x2.fence.register.reserved/rename.after#1`;
  - RW-K2: `namespace/create.after#1`;
  - RW-K3: `marker/create.after#1`;
  - RW-K4: `x3c.ledger-create.projects/create.after#1`;
  - RW-K5: `x3c.ledger-create/create.after#1`;
  - RW-K6: `x3c.ledger-create.ddl.commit.before#1` (dropped if N-L0 applies);
  - RW-K7: `x3b.floor.directory/create.after#1`;
  - RW-K8: `x4t.floor-publication.dependency/create.after#1`;
  - RW-K9: `dependency/write.before#1`;
  - **RW-K10 (r2): `dependency/create.after#6`**, the predecessor directory.

  **Expected:** child 3 is Committed, and the completions it names are exactly those whose final effect child 2 had not passed. A kill at a completion's last `.after` point is CR-3's cross-process idempotence row: child 3 names no completion for that object. R1 and R4 run for each killed child that drew an ExecutionId.
- **RW-N1 to RW-N12, refused neighbours** (exec (mut), labelled `mutation`; R1 and R2 only, X9:1079). The parent builds the neighbour on a fresh fixture, then one commit child runs:
  - RW-N1, N-R1: adopt kind;
  - RW-N2, N-R2: an exact marker with N absent;
  - RW-N3, N-R3: N with an extra entry;
  - RW-N4, N-R4: a marker neither equal to nor a prefix of the frame;
  - RW-N5, N-R7: a zero-length marker with no row;
  - RW-N6, N-P1: a non-empty ACL-omitted `objects/`;
  - RW-N7, N-P2: length 0 with a `-wal`;
  - RW-N8, N-L1: CREATE-then-DROP;
  - RW-N9, N-T1: a leaf neither equal to nor a prefix of the publication's bytes, at a name the publication writes;
  - **RW-N10 (r2), N-R9: a present non-exact marker with N absent,** in three variants:
    - (a) private, zero-length: `identity-contradiction`;
    - (b) private, a non-empty strict prefix: `identity-contradiction`;
    - (c) zero-length, ACL omitted: `marker-custody`;
  - **RW-N11 (r2), N-L2:** the compacted-history ledger (CREATE TABLE, INSERT, DROP TABLE, VACUUM), placed by the parent at the namespace's ledger path: `LEDGER.CORRUPT`;
  - **RW-N12 (r2), N-T2b:** an ACL-omitted predecessor directory that holds one entry: `installation-incomplete` (unchanged in r3: it is opened and reaches the custody judgment).

  **Expected:** today's row and subject, no completion named, and nothing written past the request's earlier lawful effects.
- **RW-B, contention during repair.**
  - Writer A is held inside C-REG at `x2.fence.register.repair.marker/write.before#1`, with the fence held.
  - Process B, a competing writer of the same root, gets the busy row with no state change.
  - The sweep, C, skips and retains.
  - A is resumed and ends Committed.
- **The census for these rows (law for X9 r17).** J4's census is the census of its own driver runs (X9:170): the unarmed reference run of each RW-K start state, from child 1's kill. RW-K's kill set is every durability point in those traces whose scope carries the `.repair` component, at `#1`, and at the first, a middle and the last occurrence of a repeated protocol (X9:920). C-ACL's append is not itself a durability point, so RW-K10's kill points are C-TDIR's directory barriers.
- **Scope names (lead decision).** Each completion's effects run in a scope named after its owner's, with the component `repair` inserted. Examples:
  - `x2.fence.register.repair.namespace/…`, `x2.fence.register.repair.marker/…`, `x2.fence.register.repair.active/…`;
  - `x3c.ledger-create.repair/…`, `x3c.object.repair/…`;
  - `x3b.floor.directory.repair/…`;
  - `x4t.floor-publication.dependency.repair/…`, which covers C-TRUST and C-TDIR.

  X9-1's site list and X9 r17's scope table gain them.
  - **Rejected:** reusing the first-registration names. A trace could not then tell a completion from a first act, and F00's transcription by window would misattribute points.
- **L11, retired only on evidence (r2, JRW-R1-03).** X9 r17 retires L11, so that `limits` becomes L1 to L10 and the checker's list follows in `check` and `check-unit`, **only when both of these hold:**
  - J4e's lead set passes every RW row, RW-D1 and RW-K10 included;
  - J4c's RW-C5 pins hold.

  Until then L11 stays in `limits`, and its reason names the states not yet covered by a passing row. If N-L0 applies, L11 stays open, narrowed to the bare-WAL ledger state, with its owner "a later ledger law". Item 1's enumeration finds no other L11 state in either pinned census. The power-loss variants stay L1. The neighbours are executed as RW-N rows, not recorded as limits.
- **The lead set.** One serialized lead set on J4e's integration commit, with both targets: storage, F00 to F53 plus the RW rows, and host. It is serialized with every other lead set because of the 5000 ms timing guard (M3P:421).
  - X3c-3's lead set and J4's are independent (X3C:261). Whichever integrates second reruns both units' rows: `RC-` and `RW-`.
  - J4 gains no edge on X3c-3 (P5-1's DAG is kept; M3P:311).

### 11. Units: J4's sub-units

Each is reviewed on its own, with an inventory successor numbered at build time under the linear-chain rule.

| Unit | Content | Depends on | Size |
|---|---|---|---|
| **J4a** | **The shared primitives:** C-ACL over P-ACL in `security::private_access`, used through `store_custody`, and C-SUFFIX over P-PREFIX. **Their X3c and X3b uses:** the store directories (RW-P1), the length-0 ledger file (RW-P2), and `trust/carrier-floors/` (RW-P3). Also the typed completion result these uses return, and `host.repair.completed` once O1 has landed (item 7). Tests RW-C1, C2, C3, C6, C7, C10 and C12 for these states. | J-RW, RW-S3, RW-S4 | M |
| **J4b** | **Registration.** `project_admission`'s marker observation and the join classification, on the write gate only. `first_registration`'s C-REG (item 3.4), steps 3 to 6 from the found state, with the join decided before any effect. Tests RW-C1 to C4, RW-C8 and RW-C16 for RW-R1 to RW-R7 and N-R1 to N-R9. | J4a, RW-S1, RW-S2 | M |
| **J4c** | **The ledger.** L-UNC with its schema cookie, and C-LEDGER, in `project_ledger`, with disposition `Completed`. Tests RW-C5 (the pins and negative fixtures, first), RW-C9 and **(r3)** RW-C17 (the product-SQL census for k). **(r2)** It needs nothing from J4a: it reports through its owner's own `LedgerDisposition`. Under item 3.3's fallback, J4c lands only RW-C5's negative controls. | J-RW, RW-S3 | S |
| **J4d** | **Trust.** RW-T1 and RW-T2 at `write_dependency`. **(r2)** RW-T3's C-TDIR at `parent_dir`, with the X4B-a acceptance-path directories. Tests RW-C14, RW-C15 and **(r4)** RW-C18 and RW-C19, the clocked path. | J4a, RW-S5 | S |
| **J4e** | **The rows.** X9 r17's section: RW-F00, RW-D1, RW-K1 to K10, RW-N1 to N12 and RW-B, transcribed; J4's census; the checker's limit list, conditionally (item 10); release absence for the `.repair` scope names. It joins every unit's typed completion result. Then **one serialized lead set** on both targets (item 10). | J4a to J4d, RW-S6 | the lead set |

- **Size.** M + M + S + S, plus the lead set. That is P5-1's "L plus one serialized lead set" (M3P:574). C-TDIR reuses J4a's C-ACL at one more step.
- **Critical path.** M3P gives J4 3 days, then 1 for its rows, from J-RW at or before day 0: rows by day 4, with slack against M3-X (M3P:311, :340).
  - J4a and J4c run in parallel from the start. J4b and J4d follow J4a.
  - RW-S1 to RW-S6 need not precede day 0. Each gates only its own sub-unit, and J4's slack absorbs their review.
- **J3d** keeps only J-C22. It reaches the completions through J1 item 3's entry (J1:756).

### 12. Successors

| # | Successor | Owner (law) | Content | Gates |
|---|---|---|---|---|
| RW-S0 | **This law** | lead | items 1 to 11 | J4a to J4e |
| RW-S1 | **X2 r10**, shared with J1's S7 (J1:727) | security | Item 4: the join classification, on the write gate only. New item **6c**, reservation completion (item 3.4), with **(r2)** its namespace-and-marker clause: a present marker of any form requires N complete. Item 8: no new row. The forbidden substitute "deleting or adopting a leftover reservation, namespace or marker" (X2:421) reads "deleting one; adopting one except through item 6c". "Not claimed: explicit recovery" (X2:433) excludes item 6c. | J4b |
| RW-S2 | **Registry owner selection v3** (record) | the registry owner (security) | J-RW is the operation owner that authorizes ordinary, random-kind reservation completion (REG:9, :74). Completing a strict-prefix marker in place is the reservation's own interrupted step, not an overwrite (REG:60). **(r2)** It is lawful only with the complete namespace present; REG:76's order covers every present-marker form, not only the exact one. Adoption, move and abandonment are unchanged. | J4b |
| RW-S3 | **X3c r9**, on X3c r8's accepted bytes (X3C:356) | storage | Item 1: C-ACL for the store directories. Item 2: the length-0 ACL-omitted file and **(r2)** L-UNC become resumable creation states, with L-UNC's schema-cookie clause, **(r3)** its bound k = 26 and its threat model as item 3.3 states them. **(r3)** A new forbidden substitute: schema-changing SQL on a ledger path, or a non-defensive ledger connection, without re-establishing k and L-UNC (RW-C17). Item 10: `LEDGER.CORRUPT` narrowed. The forbidden substitute "adopting a partial or schema-less ledger" (X3C:362) excludes L-UNC. Also item 12a's tests and item 13's units (J4a, J4c). r8's CL-3 constraint is kept (X3C:355). | J4a, J4c |
| RW-S4 | **X3b r11** | security, journal | Item 2: C-ACL for `trust/carrier-floors/` under the fence (X3B:52). Item 12: unit J4a. | J4a |
| RW-S5 | **(r4) X4T r13, the next X4T successor after the accepted r12,** plus a record note in **X4B r6** (shared with J1's S6, J1:726) | trust | **(r4)** It retains r12's clock and write-ahead rules unchanged: item 6's `EV-CLOCK`; item 7's write-ahead before a clocked refusal; item 9's refusal before every lease (X4T:170-175, :205). It records that C-TRUST and C-TDIR run on both ends of the read (item 2). X4T item 7's dependency rule gains:<br>- "complete a strict-prefix leaf at a name this publication writes" (item 3.5);<br>- **(r2)** "complete a `may_create` parent directory left without its allow" (item 3.6).<br>X4T item 10's incomplete row is narrowed. X4T items 12 and 13 gain the tests and unit J4d. X4B r6 records that the shared protocol completes such a leaf and such a directory, and deletes nothing (X4B:125-130). | J4d |
| RW-S6 | **X9 r17** (record and rows), shared with J1's S12 (J1:733) and X3c r8's RC section (X3C:354), as J-RW's own section | lead | item 10 | J4e |
| RW-S7 | **M3-PLAN's next revision** (record) | lead | P5-1's owner list gains X3b and REG. J4's sub-units J4a to J4e. J-RW's cross-law items. **(r4, record)** The owner list has landed: M3-PLAN r7 names "the X2, X3c, X4T, X3b and registry owners", accepted and current at r9 (`m3/M3-PLAN-r9.md:284`, `72bc7a13…`). | — |
| RW-S8 | **J1's next revision** (record) | lead | Item 11's recommendation is replaced by this law's decisions. Its "`repair recover` command is M5 (BP:973)" is corrected (item 14). J-C22 is defined in item 9. **(r4, record)** The correction has landed in J1 r4 and is carried in the accepted r5 (`m3/host-pipeline-j/PROPOSAL-r5.md:815`, `4ccb2320…`). Replacing item 11's recommendation is still owed. | — |

**Not successors:**
- L465. Its item 5 is the precedent C-ACL extends, by successors RW-S3, RW-S4 and RW-S5. 465's own creator rules are unchanged.
- OWN. §6 is kept: nothing is deleted, staging is never adopted, and "no … directory permission repair" stands, because C-ACL is not one (L465:25).
- IE. See X-RW-1.
- SOP2. `host.repair.completed` is an ordinary registration.

### 13. Cross-law items

- **X-RW-1. "Explicit recovery" (IE:47-50; REG:74). Law that must change: REG (record, RW-S2).**
  - REG:74's "independently authorized" is met by item 2's authorization. REG must record it.
  - **(r2)** Codex's r1 review found that IE:47-50 needs no passage successor for this design. Classification grants nothing, the separately specified completion chooses no competing identity, and the final writer admission still requires exact marker and ACTIVE agreement (Codex r1 review, request item 2). r1's conditional gate on an IE successor is withdrawn.
- **X-RW-2. The marker in place (REG:60; X2:247). Laws that must change: REG (RW-S2) and X2 (RW-S1).**
  - REG:60: "must not overwrite a … malformed … object". C-SUFFIX overwrites no byte: it writes only past the existing length, into the file the reservation's own step created.
  - **(r2)** It does so only when the complete N is present (item 3.4).
- **X-RW-3. The schema-less ledger (X3C:85, :216, :362). Law that must change: X3c (RW-S3).**
  - X3c item 2 treats only a length-0 file as "creation not begun", while X3b item 3a already reuses an empty database (X3B:86). r8 left item 2 unchanged (X3C:45, :357).
  - RW-S3 aligns X3c with X3b under L-UNC, which r2 makes stricter than X3b's rule by the schema cookie.
- **X-RW-4. The dependency rule (X4T:169; `floor_publication.rs:455-458`). Laws that must change: X4T (RW-S5), with an X4B record.**
  - X4B:125 rejects "writing records in place". That bullet concerns publishing new trust state by updating existing records. A strict-prefix completion changes no record's content. Codex found that X4T/X4B successors can authorize it without editing an admitted record (Codex r1 review, request item 3).
  - **(r2)** The parent-directory completion, C-TDIR, joins the same successor.
  - **(r4)** That successor is X4T r13, after the accepted r12 (RW-S5).
- **X-RW-5. Leftovers (X2:256, :421, :433; `first_registration.rs:18-21`). Law that must change: X2 (RW-S1).**
- **X-RW-6. L465 item 5's reach.** It was an owner decision for `OpenSIP` alone (L465:19). C-ACL applies the same rule, a lead decision, to more names in X3c, X3b, X2 and X4T:
  - nine fixed names;
  - **(r2)** the three `may_create` trust directories;
  - X4T dependency leaves.

  L465 itself does not change: the owners' successors carry the extension. It is flagged for the owner below.
- **X-RW-7. P5-1's owner list** (M3P:573) omits X3b and REG. **Law that must change:** M3-PLAN (record, RW-S7).
- **X-RW-8. J1 item 11's "`repair recover` command is M5 (BP:973)"** (J1:690). That command is the source-repair journal recovery (CINV:988; SL:673), not storage repair. **Law that must change:** J1 (record, RW-S8).
- **X-RW-9. X3c r8, the re-commit successor (P5-2), now accepted (X3C, `ba638efb…`). No conflict; J-RW's joins rechecked against it.**
  1. **Text.**
     - **Item 2 is untouched by r8.** r8 changes item 6, adds 6a, and changes item 10 and the forbidden substitutes only for re-commit, absorbing none of J-RW's X3c text (X3C:45, :356).
     - **Lead decision LD-11, now settled by r8's acceptance:** RW-S3 is X3c r9, written on r8's accepted bytes. It adds its text to items 1, 2, 10, 12a and 13 and to the partial-ledger forbidden substitute. It changes none of r8's re-commit clauses.
  2. **Semantics. Disjoint, with the guarantee item 3.3 actually establishes (r3).**
     - No completion here creates, reads or changes an attempt row, receipt, association, availability record, Run material or pin.
     - For every OpenSIP writer, a ledger C-LEDGER completes has never had a schema change committed (item 3.3, within the bound k = 26), so it holds the schema only. Histories written outside OpenSIP's writers are outside that guarantee, as they are outside X3c item 2's own check. r8's standing read (X3C:114-133) therefore finds no per-Run row, and the next commit of any Run there is a first commit.
     - That meets r8's CL-3 constraint, "never recreate, replace or empty a ledger that holds any committed row" (X3C:355), for every OpenSIP writer. Since r2 it is enforced by the schema cookie, and since r3 by the bound k, not by current emptiness alone.
     - If an identical Run commits again later, X3c r8's item 6a decides it; J-RW changes no outcome there.
  3. **Boundary.** r8 cites J-RW's out-of-scope list and keeps `admitted` attempts and undetermined commits with X6 (X3C:126, :345). So no state is claimed by both laws.
  4. **Matrix.** X3c r8's `RC-` section and J-RW's `RW-` section of X9 r17 are independent (X3C:354). Whichever of X3c-3 and J4 integrates second reruns both (X3C:261). J4's code does not depend on X3c-3.
- **X-RW-10. X9 r17 is shared.** J1's `S12-` rows, X3c r8's `RC-` rows and J-RW's `RW-` rows are separate sections of one record revision. Each section's rows are transcribed when its unit is ready. **Law that must change:** X9 (RW-S6).
- **X-RW-11. OWN:119** ("Present I missing … required trust dependency → no inferred pristine creation, reset or repair"). **No conflict.** C-TRUST and C-TDIR complete only a leaf or directory that the admitted closure does not name, so neither is a required dependency.
- **X-RW-13 (r4). X4T r12 and X4-F2, the clocked write-ahead (X4T:170-175, :205). No conflict, after r4's composition.** Accepted X4T r12 runs the mandatory floor write-ahead before a clocked continuation refusal, and integrated X4-F2 implements it (`floor_publication.rs:977-995` at `d2c00a9`).
  - **J-RW r3 assumed** that every publication follows an admitted view.
  - **r4 authorizes** C-TRUST and C-TDIR on that publication too (item 2, LD-16). The refusal that follows is unchanged, so X4T r12 needs no change.
  - **RW-S5's text** goes to the next X4T successor, r13, and keeps r12's clock and write-ahead rules.
- **X-RW-12 (r2). X9 r16's own note on directory occurrences** (X9:146-153: "A directory occurrence is not in X9-2's kill set at this census … A later census that puts one there transcribes it by the same reference, under X4T's parent-directory step"). **No conflict.** RW-D1 and RW-K10 name the directory occurrence explicitly, and C-TDIR is that parent-directory step's completion.

### 14. Record corrections (record only)

- **J1:690.** "A `repair recover` command is M5 (BP:973)." Storage repair has no command at M3, M4 or M5 in BP or CINV. `repair-recover` is source repair (X-RW-8).
- **M3P:573.** "amends X2 item 8, X3c item 10 and the X4T dependency-publication rule". It reads: X2 items 4, 6 and 8 (with REG's record); X3c items 1, 2 and 10; X3b item 2; and X4T item 7 (leaves and parent directories), with an X4B record.
- **M2C:349 and X9's limits.** L11's owner is J4 and its rows (item 10). M2C is a completion record and does not change. X9 r17 carries the change, conditionally.
- **(r2) r1's census example.** r1 said there were "39" `dependency/create.after` occurrences. The pinned EV storage census has seven. 39 is the count in security's own X9-1 self-census table (`crash_matrix_census.rs:826`), which is not the pinned evidence.

## Forbidden substitutes

- A completion on a read path: the read session, `doctor`, the recovery selector, the sweep or the ephemeral entry. A completion in the process that crashed, or a retry of a failed completion in the same process.
- **Deletion of any kind.** Also forbidden: truncation; renaming an existing object away; adopting a stage, a staging name or any temporary name; replacing a trust leaf or a marker by rename; rewriting any existing byte of a marker, a trust record or any evidence. C-LEDGER's selected schema transaction over an L-UNC file is the one stated exception (item 3).
- C-ACL on a non-empty directory, or on a file with bytes outside P-PREFIX. C-ACL on an object whose owner, mode, link count or filesystem is not the private shape, or whose ACL is present. Any mode change. Any ACE other than the one zero-rights owner allow. C-ACL on a trust directory at a name `may_create` does not permit.
- Completing a marker or leaf whose bytes are neither exactly equal to nor a strict prefix of the owner's own bytes. Completing a leaf at a name the publication does not write. Visiting an unreferenced leaf.
- Treating as L-UNC a ledger with any committed schema object, a freelist page, a second page, **or a schema cookie other than 0**. Migrating, truncating, renaming or deleting a ledger. Widening L-UNC to fit a run. Enabling C-LEDGER before J4c's positive and negative pins hold. **(r3)** Adding schema-changing SQL to a ledger path, or opening a ledger without defensive mode, without re-establishing k and L-UNC (RW-C17). That means a `VACUUM`, `DROP`, `ALTER`, `ANALYZE` or `REINDEX`, a migration, or a `CREATE` outside `selected_ddl()`.
- Completing an adopt-kind reservation. Converting a random row to an adopt row, or the reverse. Abandoning, moving or rewriting a RESERVED row except to its ACTIVE. **Completing, or taking any effect over, a present marker of any form while N is absent.** Admitting an incomplete or foreign N. Taking any completion effect before the join is decided.
- Inferring commitment, an attempt row, a receipt or a RunId from any completion. Settling an `admitted` attempt. Touching the journal, witness or carrier outside X3b's own reconciliation.
- Changing classification or rows on any path other than item 3.4's step.
- A new public code, class, exit, detail, subject, envelope member or remedy text. A new CLI word, flag or library entry for repair. Using logs or crash records as recovery input.
- A completion effect outside a `.repair` scope during a matrix run. A matrix expectation read back from a run. Retiring L11 before item 10's evidence holds.
- **(r4) On X4T r12's clocked path:**
  - completing anything but the mandatory write-ahead publication on the authenticated closure and pending write;
  - returning anything but X4T r12's unchanged clocked refusal after such a completion;
  - treating that refusal as a view, or granting a lease or later effect after it;
  - completing on a read refused before time admission, or on a report-only read;
  - a successful-view gate that leaves a repairable OpenSIP-owned leaf or directory blocking the mandatory write-ahead.

## Lead decisions

Each is dated 2026-10-04 and made under the owner's standing direction. The owner may reverse any of them.

| # | Decision | Rejected alternatives | Item |
|---|---|---|---|
| **LD-1** | Complete forward inside the next admitted durable write, at each owner's own step and under its lock | a separate repair command or entry; completion by the crashed process; completion on a read path or in `doctor`; abandonment and reallocation | 2 |
| **LD-2** | An `OrdinaryWriteAdmission` on the same root, with agreeing locator and incarnation, authorizes random-kind reservation completion | a consent flag (no CLI at M3); adopt rows completed alike (REG:76) | 2 |
| **LD-3** | C-ACL generalizes L465 item 5 to the L11 owners | quarantine-rename; a mode or ACL rewrite; completing non-empty objects | 3.1 |
| **LD-4** | C-SUFFIX: finish an interrupted write in place, suffix only | atomic replacement (temporary names in trust collections; X4B:125; the marker is no-replace); truncate and rewrite; completing non-prefixes | 3.2 |
| **LD-5 (r2; r3)** | C-LEDGER over L-UNC with the schema cookie 0 as its history discriminator, pinned by J4c, with a fallback to refusal. **(r3)** Its guarantee is scoped to OpenSIP's writers by the bound k = 26 and kept true by RW-C17. | r1's predicate without a history discriminator; the file change counter; the cookie alone; rename aside and recreate; deletion; **(r3)** withdrawing C-LEDGER because the cookie wraps; a 2³² stress run; a separate history record | 3.3 |
| **LD-6** | C-REG runs X2 item 6's remaining steps from the found state, never touching leftovers | a fresh registration over the reservation; abandonment | 3.4 |
| **LD-7** | No public disclosure; one operational-record event by ordinary registration | a new detail, subject or envelope member; no record at all | 7 |
| **LD-8** | Scope is L11's families exactly, by state and every census occurrence | a general repair of refused states | 1 |
| **LD-9** | `.repair` scope names for completion effects | reusing the first-act names | 10 |
| **LD-10 (r2)** | X9 r17: re-transcribe F00's L11 cells; add RW-D1, RW-K, RW-N and RW-B; retire L11 only on item 10's evidence | r1's unconditional retirement; keeping L11 as a limit whatever the rows show | 10 |
| **LD-11** | J-RW's X3c text is X3c r9 on r8's accepted bytes | editing r8 from here | 13 |
| **LD-12** | P5-1's owner list gains X3b and REG | leaving RW-P3 (installation-wide) and REG's authorization unowned | 1, 13 |
| **LD-13 (r2)** | The join requires a positively absent marker whenever N is absent, decided before any effect | r1's join, which admitted a non-exact marker with N absent | 3.4 |
| **LD-14 (r2)** | C-TDIR completes a `may_create` trust directory at `parent_dir` | a residual L11 limit for it; completing any parent directory; renaming it aside | 3.6 |
| **LD-16 (r4)** | C-TRUST and C-TDIR are authorized on X4T r12's clocked path. They rest on the authenticated closure and the pending write the admission carries, and the unchanged clocked refusal follows them. | **a successful-view gate**, which would leave repairable, OpenSIP-owned objects blocking the mandatory write-ahead X4T r12 requires before that refusal (JRW-R3-02) | 2, 3.5, 3.6 |
| **LD-15 (r3)** | N-T2 is split at the existing failure boundary. A native open failure keeps `HOST.IO_FAILURE`, a failed custody judgment keeps `installation-incomplete`, and C-ACL runs only on a retained, opened directory. | one row for every directory-shaped failure, which would change an existing public row (JRW-R2-02) | 3.6, 5 |

## Open questions

**No owner decision blocks J-RW.**

**Flagged for the owner (non-blocking lead decisions the owner may reverse):**
1. **LD-1 and LD-2.** A crash during a project's first registration is completed by the next durable analysis of that project, with no prompt and no public notice; only the operational record shows it. The alternative is a refused project until an explicit repair command exists, and none is planned through M5.
2. **LD-3, LD-14 (X-RW-6).** The owner's 2026-09-27 decision for `OpenSIP` (L465 item 5) is extended, in four laws, to:
   - nine more fixed names: X3c's four store directories and ledger file, X3b's `carrier-floors`, X2's `I/host` and `I/host/projects`, and the marker;
   - the three `may_create` trust directories;
   - X4T dependency leaves.
3. **LD-4 and LD-5.** An interrupted trust record and an interrupted ledger creation are completed in place, never replaced or deleted.

**For the reviewer (r4):**
- **R10 (r4).** Is the 7/1/18 breakdown now correct everywhere, with k = 26, RW-C5 and the fallback unchanged? Does RW-C17 enumerate the selected statements by name?
- **R11 (r4).** Does item 2's clocked-path authorization compose with X4T r12 exactly (X4T:170-175, :205; `floor_publication.rs:961-1000` and `current_trust_admission.rs:243-289`, `:1113-1125` at `d2c00a9`)? That means completion on the authenticated closure and pending write; then the unchanged clocked refusal at the same precedence; no view and no lease. Are the earlier refusals and report-only reads still effect-free? Do RW-C18 and RW-C19 cover the route?

**For the reviewer (r3, answered in r3's review):**
- **R1 (closed in r2).** IE needs no passage successor (X-RW-1).
- **R2 (r3).** Is the guarantee now stated exactly? It is scoped to OpenSIP's writers by the bound k = 26, with foreign SQL writers, wraparound and forgery under "Not established". Is k established by item 3.3's five steps and the bundled engine's source? Do RW-C5's pin of 26 and RW-C17's census, with its owner, keep k true? Are the stop rule and fallback unchanged?
- **R9 (r3).** Does the N-T2a/N-T2b split leave every existing row unchanged (X4T:216, :233)? Does C-TDIR run only on a retained, opened directory?
- **R3.** Is C-SUFFIX on a trust leaf consistent with X4T item 7, X4B:125 and X4B:130, and OWN §6 (X-RW-4, X-RW-11)? Is item 3.5's argument that the leaf cannot be referenced sound?
- **R4.** Is C-ACL a lawful generalization of L465 item 5 to non-creator owners under the writer lease and the fence (X-RW-6)? Is P-ACL's clause 4 (empty) the right bound?
- **R5.** Does C-REG's join, now closed by clause 3, meet REG:70-76 exactly, and is every non-join combination in item 5 with its actual row?
- **R6.** Is item 1's enumeration complete for both pinned censuses? Is RW-T3, with C-TDIR, reachable without relaxing trust admission?
- **R7.** Do RW-D1, RW-K10, the new RW-N rows and the conditional L11 retirement cover JRW-R1-03 under X9's rules (X9:146-153, :170, :920, :1079, :1236)?
- **R8.** Are the X3c joins sound against accepted r8 (X-RW-9)?

## Not claimed

- No code, test, build or matrix run for this law. No SQLite fixture was run for r2 or r3. Every SQLite claim is from the cited documentation or from the bundled engine's source (SQ-SRC), and J4c pins it against that engine before C-LEDGER is enabled.
- No CLI or library repair entry. No `doctor` change. No public code, class, exit, detail or subject.
- No recovery of power-loss variants (L1), migrations (L5), orphans (L6), `admitted` attempts, undetermined commits, quarantines, adopt-kind reservations, or moved or re-cloned roots.
- No defence against a same-uid actor who writes a ledger outside OpenSIP: by raw bytes, through a non-defensive connection, or with 2³² − k or more schema changes by ordinary SQL (item 3.3's threat model).
- No deletion or cleanup of stages, temporary files or unreferenced trust leaves.
- J-RW r4 was written from the product at `d2c00a9` and the snapshots named above. r4's X4-F2 cites (`floor_publication.rs:938-1001`, `current_trust_admission.rs:243-289`, `:1113-1125`, `floor_publication_tests.rs:801-852`) hold at `d2c00a9` only. Every other cited product line is the same at `cd5958b` and `d2c00a9`.
