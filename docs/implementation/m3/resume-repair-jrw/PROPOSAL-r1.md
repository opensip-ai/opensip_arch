# The resume/repair writer — proposal J-RW r1

2026-10-04. Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the overnight autonomous run. Law **J-RW** of the accepted M3 unit plan, owned by M3-J under lead decision P5-1 (M3P:217, :236, :572-575).

**Draft r1, not accepted. Not code.** It must be accepted before M3 day 0, which is M3-L's acceptance (M3P:236, :259). Its code unit J4 follows it and does not wait for J3 (M3P:251, :311, :574).

**What this law is.** P5-1 asks for "the resume/repair writer's successor to X2 item 8, X3c item 10 and the X4T dependency-publication rule, with its X9 coverage rows" (M3P:217, :573). M2 leaves three families of crash states permanently refused: an interrupted first registration, a created owner not yet sampled private, and a partial ledger WAL (EXIT:186-191; M2C:349-356, limit L11; X9:163-168). This law:
1. enumerates every such state by owner and census window (item 1, item 4);
2. fixes where, under which lock and on whose authority the writer completes each one (item 2);
3. fixes each completion as the owner's own interrupted step, finished in place (item 3);
4. fixes the states it must keep refusing (item 5), its idempotence and crash-during-repair rules (item 6), its disclosure (item 7) and its rows (item 8);
5. names its controls, its X9 r17 rows, J4's sub-units and the successors the owners must write (items 9 to 12);
6. records the cross-law items, X3c r8's included (item 13).

**Standing direction.** Every item that says "lead decision" is made under the owner's standing direction of 2026-09-30 to proceed on the lead's recommendation. Each names the alternatives it rejects. The owner may reverse any of them. No item blocks on an owner decision ("Open questions").

**The owners' assent.** The laws this one amends are the lead's: X2 r9, X3c r7, X3b r10, X4T r11 and X4B r5, and the registry owner selection v2. Their amendments are written here as successors RW-S1 to RW-S5 (item 12), as lead decisions under the standing direction. None of them changes before J-RW is accepted, and each is reviewed with J-RW or right after it. **X3c r8 is being drafted tonight by another agent. This law neither reads, cites nor edits it**; item 13 records how the two meet.

## Short names

Arch paths are under `docs/`. The sha256 prefixes are of the bytes read for this draft.

| Name | Document | sha256 |
|---|---|---|
| **M3P** | `implementation/m3/M3-PLAN-r6.md`, the accepted r6 bytes. The live `M3-PLAN.md` adds the acceptance note, so its lines are these plus 2. | `a6956e88…` |
| **J1** | `implementation/m3/host-pipeline-j/PROPOSAL-r3.md`, the r3 bytes CODEX2 accepted (live file: these lines plus 2) | `ad887c90…` |
| **M2C** | `implementation/m2/M2-COMPLETE.md` (r2, COMPLETE) | `b8d6053a…` |
| **EXIT** | `implementation/m2/EXIT-PLAN.md` | `fee07b44…` |
| **X2** | `implementation/m2/project-root-x2/PROPOSAL-r9.md`, the r9 bytes Grok accepted | `0d68e3a5…` |
| **X3C** | `implementation/m2/ledger-blob-x3c/PROPOSAL.md` (r7, accepted) | `838916f1…` |
| **X3B** | `implementation/m2/journal-x3b/PROPOSAL.md` (r10, accepted) | `c7d5e944…` |
| **X4T** | `implementation/m2/trust-admission-x4t/PROPOSAL.md` (r11, accepted) | `8116f487…` |
| **X4B** | `implementation/m2/trust-bootstrap-x4b/PROPOSAL.md` (r5, accepted) | `77b9ab1e…` |
| **X3D** | `implementation/m2/commit-session-x3d/PROPOSAL.md` (r8) | `9f3712a0…` |
| **X6** | `implementation/m2/carrier-recovery-x6/PROPOSAL.md` (r4) | `1b891802…` |
| **X1** | `implementation/m2/ordinary-platform-x1/PROPOSAL.md` (r1) | `d747adf0…` |
| **X9** | `implementation/m2/crash-matrix-x9/PROPOSAL-r16.md`, the accepted r16 bytes | `f08efe95…` |
| **EV** | X9's evidence record at C = `3d2d5b5`: `crash-matrix-x9/evidence/3d2d5b5a…/storage/matrix.json` (its `hashes.txt` is `97f8367e…`) | `5585bc42…` |
| **L465** | `implementation/m2/initial-parent-preparation-465/PROPOSAL.md` | `b34eae39…` |
| **REG** | `implementation/m2/project-registry-owner-selection-v2/owner.md`, the selected registry owner | `2d4b65c9…` |
| **OWN** | `implementation/m2/initial-root-binding-owner-selection-v1/owner.md` | `35953d09…` |
| **OPP** | `implementation/m3/operability/PLAN.md` (r3 accepted) | `4eca344b…` |
| **SOP2** | `implementation/m3/operability/s-op-2/PROPOSAL-r6.md`, the r6 bytes Codex accepted | `ce8d3a4b…` |
| **SL, IE** | `v2/contracts/product-v1/{security-and-lifecycle, identity-and-evidence}.md` | `a319da39…`, `c82404f3…` |
| **BP** | `v2/architecture/implementation-boundaries-and-build-plan.md` | `8e6e8bab…` |
| **CINV** | `coop/design-corrections/workflows/command-inventory.v3.json` | `d303cc64…` |

Product paths are under `opensip/` at main `3e64266`. They were read, not run. Main has since advanced to `e093e90` (F8b); `git diff --name-only 3e64266 e093e90 -- crates/` is empty, so every cited product line is unchanged there.

## Problem

**What exists at `3e64266`.** Each owner fails closed on its own interrupted act, and nothing completes it.
- **First registration** (X2 item 6). The RESERVED row is durable before the namespace, `.opensip` and marker exist, and ACTIVE comes last (X2:236-248). Admission classifies a matching RESERVED row as `RecoveryNeeded` and grants nothing (X2:177, :184; `crates/security/src/custody/project_admission.rs:678-719`). The row is `PROJECT.ROOT_CUSTODY_REFUSED` / `identity-recovery-required` (X2:366; `custody/first_registration.rs:214-222`). A marker that exists but is not judged private refuses earlier, as `marker-custody` (`project_admission.rs:602-603`). An empty private marker is `Malformed`, so `Contradiction` (`project_admission.rs:616`, `:684-685`). The writer itself says that "each leftover is the registry owner's explicit-recovery case, which is not implemented here" (`first_registration.rs:18-21`; X2:256).
- **Private creation.** A new private directory or file is made by `mkdirat 0700` or an exclusive `0600` create, and only then does it get its zero-rights owner allow (`private_access.rs:120-126`; `store_custody.rs:105-154`). The private predicate refuses an omitted ACL (`private_access.rs:55`). An existing object is judged as it stands and is never changed (`store_custody.rs:110`; L465:17). So a kill between the create and the allow refuses on every later admission:
  - X3c's store directories and ledger file: custody `private` (`ledger_store/project_ledger.rs:260`);
  - X3b's `trust/carrier-floors/`: X3b's host I/O row (`journal_store/carrier_floor.rs:237`, `:841-844`). This one blocks **every project of the installation**, not one;
  - X2's `I/host` and `I/host/projects`: inside registration, behind `identity-recovery-required`;
  - the marker: `marker-custody`, above;
  - an X4T dependency leaf, below.
- **The ledger WAL** (X3c item 2). WAL is selected, then one DDL transaction commits (`project_ledger.rs:452-509`; barriers `wal` at `:491` and `ddl.commit.before` at `:499`). On the next open, only an empty file with no `-wal` resumes (`project_ledger.rs:540-552`). Any other stored state is `LEDGER.CORRUPT` (`:425-432`, `:438-449`; X3C:28, :70).
- **An X4T dependency leaf** (X4T item 7). Each dependency is created only when its content-addressed name is absent. An existing name is admitted only when it is private and holds exactly the bytes (`trust/floor_publication.rs:455-488`). A leaf left empty, or torn, is never named by the unchanged pointer, so it is harmless until a later publication writes **that same name**. Then it refuses `CONFIG.CUSTODY_REFUSED` / `installation-incomplete` (X4T:141; `floor_publication.rs:470`, `:479`), installation-wide.

**What X9 measured.** In X9-2's kill set, 57 F00 kill points leave the next writer refused on these rows (X9:136-161; EV, F00 runs). They are tabulated in item 4. The census holds more occurrences of the same windows than the sampled kill set (X9:920; for example 39 `x4t.floor-publication.dependency/create.after` occurrences). This law covers states, not only the sampled points.

**Why it matters.** The owner uses OpenSIP daily. A crash in the first analysis of a project, or in the installation's first carrier floor, leaves the project, or every project, refused with no remedy OpenSIP can name. X9 deliberately added no writer for these states (X9:157). Writing one is M3's work.

## Decisions

### 1. Scope: exactly L11's three families, by owner (lead decision)

| Family | States (item 4) | Owner law and item | Product owner | Census windows |
|---|---|---|---|---|
| **R** interrupted first registration | RW-R1 to RW-R7 | X2 item 6, under REG's explicit reservation recovery (REG:72-78) | `custody/first_registration.rs`, `custody/project_admission.rs` | `x2.fence.register.reserved/rename.after` through `x2.fence.register.active/rename.before` |
| **P** created, not yet private | RW-P1 to RW-P3; also inside R (RW-R2, RW-R5) and T (RW-T1) | X3c items 1 and 2; X3b item 2 (X3B:52); X2 item 6 step 3 | `store_custody.rs`, `ledger_store/project_ledger.rs`, `journal_store/carrier_floor.rs` | every `…/create.after` of a private create, before its allow |
| **L** partial ledger WAL | RW-L1 | X3c item 2 (X3C:21-28) | `ledger_store/project_ledger.rs` | `x3c.ledger-create.wal` and `x3c.ledger-create.ddl.commit.before` |
| **T** X4T dependency at a re-written name | RW-T1, RW-T2 | X4T item 7 (X4T:97-102), shared with X4B item 5 | `trust/floor_publication.rs` | `x4t.floor-publication.dependency/create.after` and `/write.before`, where the next publication writes that name |

- **Owner list (cross-law item X-RW-7).** P5-1 names X2, X3c and X4T (M3P:573). Family P also has X3b's floor directory (X3B:52), and family R has REG as the recovery owner. Both are added here; M3P's next revision records it (RW-S7).
- **Out of scope**, each with its existing owner, unchanged:
  - `admitted` attempt rows and orphan SEALs: X6's sweep (X6 item 7; X3D:213). Its CLI is `store-gc` at M5.
  - Any `CommitUndetermined`: X3c item 7 and X6.
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
  | T | R10, X4T's floor write-ahead, or X4B's acceptance publication (same protocol) | fence, no project lock (X4T:102) | the gate's ledger |
  | RW-P1, RW-P2, RW-L1 | inside `prepare_commit`, at `admit_layout` (`crates/storage/src/commit.rs:370-375`), before the attempt row, so J1's phase A | namespace writer lease (X3C:19, :51) | the operation's attempt ledger (X3C item 9) |

  - **Who.** The writer is an X1 ordinary writer reached through J1 item 3's durable entry, never the creator act (J1:689). Matrix children and tests reach the same owners through their existing drivers.
  - **Never** on a read path: not the 458c read session, `doctor`, the read-only recovery selector (X2:336), the sweep, or the ephemeral entry (J1 item 6). These keep today's refusals byte for byte.
  - **Never in the crashed process.** A failed or uncertain step still latches its owner's ledger, with no later step and no retry (X2:212; X3C item 7). Completion is a later, separately admitted operation.
- **Authorization for family R (lead decision).** REG requires that "existing operation owners must supply authorization for … explicit recovery" (REG:9), and that recovery be "an independently authorized local operation, not the constructor's fallback" (REG:74). This law is that operation owner. **An `OrdinaryWriteAdmission` (X1 item 2) for a durable request on the same root, whose locator and incarnation agree with the row, authorizes completion of an `allocationKind: random` reservation.** That is the same authorization class, on the same root, that created the reservation (OWN:21, the durable commands' first-write effect). The completion runs as its own classified step in a later operation, never as the constructor's in-process fallback. Adopt-kind rows still need REG:76's fresh adoption context, and refuse.
- **Basis:**
  - J1's constraints and recommendation (J1:689-690);
  - SL's precedent: transition crash recovery "runs as the first act under the next fence acquisition, before any admission" (SL:648-651, :939-950);
  - L465 item 5, an owner decision: "the creator may add exactly that zero-rights owner allow … It completes the interrupted creation step and is not a permission repair" (L465:19-25);
  - X3b already resumes its own interrupted creation: "an empty database left by a crash is reused only if it holds no schema objects" (X3B:86; `carrier_floor_tests.rs:401-410`).
- **Rejected:**
  - **A separate repair command or library entry.** No analysis word is wired at M3 (J1 item 1), and CINV has no storage-repair command. `repair-recover` is the source-repair journal command, "`opensip repair recover REQUEST-ID [--apply-recovery]`" (CINV:988; BP:973; SL:673), not storage repair. A new command needs a CINV successor and its renderer milestone (BP:895). Meanwhile the daily user stays refused until M4 or M5.
  - **Completion by the crashed process,** as a retry. That is the latched-ledger rule's opposite (X2:212), and it is REG:74's "constructor's fallback".
  - **Completion on a read path or in `doctor`.** Read receipts never write (X2:406; OPP:216-218; OWN:95).
  - **Abandoning the reservation and allocating afresh.** Abandonment leaves an exact marker one-sided, refused for good (REG:78). It also needs proof that no ACTIVE binding was ever admitted, which is more than completion needs.
  - **A consent flag for completion.** There is no CLI at M3. Completion grants nothing the original request did not already ask for.

### 3. Each completion is the owner's own interrupted step, finished in place (lead decision)

**The principle.** A completion finishes the step the crash interrupted, on the same object, by the owner's own primitive:
- **Never deletes,** never truncates, never renames an existing object away, never adopts a staging or temporary name.
- **Never creates a name** the owner's step would not create.
- **Never changes a mode bit,** and appends no ACE but the one zero-rights owner allow a fresh creation appends.
- **Never rewrites an existing byte.**

It acts only when the object satisfies its predicate below. Anything else keeps today's row (item 5). Each predicate is judged under the owner's lock, through the owner's retained parent, no-follow, charged before it runs.

**3.1 C-ACL: completing a private creation (predicate P-ACL).** This is L465 item 5, applied to the L11 owners.
- **P-ACL.** All of these hold:
  1. The object is at the owner's fixed name, at the step where the owner creates or admits that name, on its parent's filesystem.
  2. It is owned by the invoking user. Its mode is exactly `0700` for a directory and `0600` for a file, and a file has one link.
  3. Its ACL attribute is **omitted** (`CapturedAclState::NotReturned`). A NOACL sentinel, an inconsistent capture or a present ACL is not omission. A present ACL is judged as it stands, as today.
  4. **A directory** holds no entry except `.` and `..`, by one bounded scan. **A file** has length 0, or, for item 3.2's targets, satisfies P-PREFIX.
- **Action.** Append exactly one zero-rights owner allow and sample again, through the fresh path's own step (`prepare_fresh_private_sample`, `private_access.rs:120-126`). The new sample must judge private, or the object refuses on today's row; the allow stays, as on the fresh path (`private_access.rs:121-124`). Then the owner's remaining steps run unchanged: exact name, filesystem, the object's own barrier and its parent's.
- **Where.** X3c's `projects/`, `projects/N/`, `objects/` and `objects/sha256/`, and `ledger.sqlite` at length 0 (then X3c item 2's existing resumable-empty path). X3b's `trust/carrier-floors/`. X2's `I/host` and `I/host/projects`. The marker. An X4T dependency leaf.
- **Why it is safe.** The allow grants nothing (L465:25). Every clause is the fresh path's own precondition, so the completed object is indistinguishable from a fresh creation. An empty object carries no content to adopt.
- **Rejected:**
  - quarantine-renaming the object and creating it afresh, which needs new names and has crash states of its own;
  - setting the mode or replacing the ACL, which would be a permission repair (OWN:120);
  - completing a non-empty directory, which this law cannot attribute to the owner's own crash.

**3.2 C-SUFFIX: completing an interrupted file write (predicate P-PREFIX).** For the marker (X2 item 6 step 5) and an X4T dependency leaf (X4T item 7).
- **P-PREFIX.** The object is a regular file that satisfies P-ACL clauses 1 and 2, and whose ACL is either omitted (then C-ACL runs first) or judged private. Its bytes, read through a bounded read of at most the expected length plus one, are a **strict prefix** (the empty prefix included) of the exact bytes the owner's step writes at that name:
  - the marker frame of the RESERVED row's ProjectId (`first_registration.rs:860`);
  - the dependency's canonical bytes, whose digest the leaf's name addresses (`floor_publication.rs:253-261`).
- **Action.** Write the missing suffix at offset = the existing length. Then the file barrier (`F_FULLFSYNC`), the directory barrier, and an exact-length capped read-back that must equal the expected bytes, on the same device and inode. No existing byte is rewritten. The file only ever holds a prefix of its own content, or all of it.
- **Rejected:**
  - **an atomic replacement** (a temporary name, then a rename over the leaf). It would leave temporary names in the trust collections on a crash. The structural trust scan reads every name returned (`trust/directory_name_scan.rs`, `trust/directory_record_capture.rs:183-193`), and X4B rejects replacing records (X4B:125). The marker is no-replace by law (X2:247; REG:60);
  - **truncating and rewriting**, which destroys bytes before the new ones are durable;
  - **completing a non-prefix**, which is foreign or corrupt content.

**3.3 C-LEDGER: completing a ledger whose schema transaction never committed (predicate L-UNC).**
- **L-UNC.** `ledger.sqlite` passes `open_store_file` (private, `store_custody.rs:251-274`) and is the retained, judged file (`same_file`). The engine opens it with item 2's flags, which runs SQLite's own WAL recovery. Then all of these hold:
  - the main schema holds **no object** (`whole_schema` is empty, `project_ledger.rs:377-386`);
  - `page_count` is 1 and `freelist_count` is 0: no committed page beyond the header page;
  - `journal_mode` is `wal`, `encoding` is `UTF-8`, and `user_version` and `application_id` are 0.
- **What it is.** This is the committed view at `x3c.ledger-create.wal`: `PRAGMA journal_mode=WAL` has written the header page, and no transaction has committed since. It is also the view at `ddl.commit.before`, because WAL recovery ignores frames with no commit record. Such a file has never held a table, so it has never held an attempt row, a receipt or any evidence.
- **Action.** X3c item 2 steps 2 to 5 on that file: `write_schema` from its `BEGIN IMMEDIATE` (`project_ledger.rs:452-509`; selecting WAL again is a no-op), then the namespace barrier and `open_verified`. The disposition is a new value, `Completed`, beside `Resumed` (`project_ledger.rs:348-356`).
- **Stop rule.** J4c pins these observables by test at both census points (control RW-C5). If the product shows a different committed view at either point, J4c stops and reports. The predicate is never widened to fit a run.
- **Basis.** X3b's carrier already resumes "an empty database … only if it holds no schema objects" (X3B:86; `carrier_floor.rs:405-425`; `carrier_dispatch.rs:153-163`). L-UNC is stricter: no schema object of **any** name, and no freelist page.
- **Rejected:**
  - **renaming the file aside and creating afresh.** It leaves an unadmitted file in the namespace and adds a rename to the store;
  - **any empty-schema database.** The `CREATE TABLE t; DROP TABLE t` fixture (`project_ledger_tests.rs:305-311`) has committed history, so it stays `LEDGER.CORRUPT`;
  - **deleting the file.**

**3.4 C-REG: completing an ordinary reservation (the reservation join).** Under the write gate, after X2 item 5's one capture and whole-document validation (no early match):
- **The join.** All of these hold:
  1. Exactly one relevant live row, by item 4's relevance rule (`project_admission.rs:688-704`). Its status is RESERVED and its `allocationKind` is `random`.
  2. The row's locator (platform, path bytes) and incarnation (volume UUID, inode, birth) agree with the admitted root.
  3. **The marker** is absent; or exact with the row's ProjectId; or a file satisfying P-PREFIX against the row's marker frame.
  4. **`I/host/projects/N`** (N the row's `namespaceId`) is positively absent, or present with exactly X2 item 6's complete footprint: a private directory with exactly two empty private lease files (`first_registration.rs:1551-1621`; REG:70).
  5. N absent with an exact marker is **not** the join. It is not a lawful crash prefix (REG:76).
  6. `I/host` and `I/host/projects` are each absent, private, or P-ACL.
  7. X2 item 6's preconditions hold: the active-transition gate (`first_registration.rs:1310`), capacity for the ACTIVE document, item 6a's tracking observation (the marker path untracked), and the recheck set.
- **Action.** Run X2 item 6's remaining steps from the first incomplete one, with the registry owner R taken from item 5's capture, which already holds the RESERVED row:
  - **step 3:** parents created or admitted, with C-ACL where P-ACL holds. Then N is published from positive absence through a **fresh** stage, or the complete N is admitted and its own and `projects`' barriers are reconfirmed (REG:70);
  - **step 4:** `.opensip` created or admitted;
  - **step 5:** the marker is created; or completed by C-ACL and C-SUFFIX; or, when exact, its file barrier and `.opensip`'s and the root's barriers are reconfirmed;
  - **step 6:** every current owner is rechecked, then RESERVED becomes ACTIVE through X2's replacement primitive, with a fresh temporary file.

  Item 7's namespace admission and the handoff then follow, as after a fresh registration.
- **What it never does.** It never touches an unpublished stage or a temporary file left by the crash (REG:70; `first_registration.rs:1228`). It never moves, abandons or rewrites the row except to its ACTIVE. It never converts a random row to an adopt row, or the reverse.
- **On every path other than this step,** admission's classification and its row are exactly today's. A zero-length marker therefore still reads `marker-custody` or `identity-contradiction` to `doctor` and to read sessions (control RW-C4).

**3.5 C-TRUST: completing a dependency leaf at a re-written name.** At `write_dependency` (`floor_publication.rs:459-488`), when the name is present:
- **The predicate.** The leaf satisfies P-PREFIX against `bytes`, and its ACL is omitted or private.
- **Action.** C-ACL if the ACL is omitted, then C-SUFFIX.
- **Why the leaf cannot be referenced.** The fenced first read admitted a closure that does not name it: a named, torn leaf would have refused that read as incomplete (X4T:141). The publication writes only its own determined list of names (X9:146-153). J4d asserts this and adds no read (control RW-C14).
- **What is never visited.** A torn leaf at a name no later publication writes stays unreferenced and harmless, as today (X4B:127; `floor_publication.rs:513-517`).
- **The shared protocol.** X4B's acceptance publication uses the same protocol, with one owner (X4T:102), and gains the same completion. Nothing is deleted, so X4B:130's "no deletion" holds unchanged.

### 4. The crash states, the writer's action and the terminal state

The counts are of X9-2's sampled F00 kill set (EV), 57 in all. Each state covers every census occurrence in its window, not only the sampled ones. "Today" is the next writer's row at `3e64266`. "Terminal" is what the next admitted durable write reaches.

| State | Window and the object it leaves | Kill points in the kill set | Today | Writer action | Terminal |
|---|---|---|---|---|---|
| **RW-R1** | RESERVED visible; N absent (a stage may be left); no marker. From `x2.fence.register.reserved/rename.after` through the namespace step before its publication | 25 for RW-R1 to RW-R3 together: `reserved/rename.after`, `reserved/directory-barrier.*`, and the `namespace/*` points. X9 r17's transcription assigns each one by its object (item 10). | `identity-recovery-required` | C-REG from step 3: parents, a fresh stage published to N, `.opensip`, marker, ACTIVE | ACTIVE (R2), Eligible, then Committed |
| **RW-R2** | As RW-R1, with `I/host` or `I/host/projects` created but not private | within the 25, at `namespace/create.after` of a parent | `identity-recovery-required` | C-ACL on that parent inside C-REG, then as RW-R1 | as RW-R1 |
| **RW-R3** | RESERVED; N published with its complete footprint; its barriers possibly pending. From `namespace/link.after` | within the 25 | `identity-recovery-required` | C-REG: admit N, reconfirm its and `projects`' barriers, then step 4 | as RW-R1 |
| **RW-R4** | RESERVED; N complete; `.opensip` created or admitted (under the S3 premise); marker absent. `marker-directory/*`, `marker/create.before` | 7 | `identity-recovery-required` | C-REG from step 5 | as RW-R1 |
| **RW-R5** | RESERVED; N complete; marker zero-length, ACL omitted. `marker/create.after` | 1 | `marker-custody` | C-ACL, then C-SUFFIX on the marker; step 6 | as RW-R1 |
| **RW-R6** | RESERVED; N complete; marker private, empty (or a strict prefix). `marker/write.before` | 1 | `identity-contradiction` | C-SUFFIX on the marker; step 6 | as RW-R1 |
| **RW-R7** | RESERVED; marker exact; ACTIVE not visible (an ACTIVE temporary may be left in I). `marker/write.after` through `active/rename.before` | 12 (5 `marker/*`, 7 `active/*`) | `identity-recovery-required` | C-REG: reconfirm the marker's and parents' barriers, recheck, ACTIVE with a fresh temporary | as RW-R1 |
| **RW-P1** | An X3c store directory (`projects`, `projects/N`, `objects`, `objects/sha256`) created, empty, ACL omitted | 4: `x3c.ledger-create.projects/create.after`, `.namespace/create.after`, `x3c.object.objects/create.after`, `x3c.object.sha256/create.after` | `Custody { subject: "private" }` | C-ACL, then create-or-admit's remaining checks and barriers | layout admitted; Committed |
| **RW-P2** | `ledger.sqlite` created, length 0, ACL omitted, no `-wal` | 1: `x3c.ledger-create/create.after` | custody `private` | C-ACL, then X3c item 2's resumable-empty path | ledger created; Committed |
| **RW-P3** | `I/trust/carrier-floors/` created, empty, ACL omitted. Installation-wide. | 1: `x3b.floor.directory/create.after` | X3b's host I/O row | C-ACL under the fence, then the floor write | floor written; Committed |
| **RW-L1** | `ledger.sqlite` private, WAL header only, no committed schema; at `ddl.commit.before`, uncommitted frames in `-wal` | 2: `x3c.ledger-create.wal`, `x3c.ledger-create.ddl.commit.before` | `LEDGER.CORRUPT` | C-LEDGER | ledger with the selected schema; Committed |
| **RW-T1** | A dependency leaf at a name the next publication writes: zero-length, ACL omitted | 1: `x4t.floor-publication.dependency/create.after#1` | `installation-incomplete` | C-ACL, then C-SUFFIX | publication confirmed; Committed |
| **RW-T2** | The same leaf private and torn (a strict prefix) | 2: `dependency/write.before#1`, `#3` | `installation-incomplete` | C-SUFFIX | as RW-T1 |

46 R + 6 P + 2 L + 3 T = 57. Leaves at names the next publication does not write (for example `dependency/write.before#6`) are already Committed and are not visited.

### 5. States the writer keeps refusing (the safety bias)

When a state is not exactly one of item 4's, the writer does nothing, and the request ends on today's row with today's subject. The row is the disclosure.

| Neighbour | Today's row, unchanged | Why it is not completed |
|---|---|---|
| **N-R1** An adopt-kind RESERVED row | `identity-recovery-required` | REG:76 requires a fresh admitted adoption context |
| **N-R2** RESERVED, an exact marker, N absent | `identity-recovery-required` | not a lawful crash prefix (REG:76) |
| **N-R3** RESERVED, N present but not exactly the complete footprint (an extra entry, a missing or non-empty lease, not private, a symlink) | `identity-recovery-required` | "an occupied incomplete or foreign namespace is unavailable" (REG:70) |
| **N-R4** RESERVED, a marker that is not a strict prefix of the row's frame | `identity-contradiction` | foreign or corrupt content |
| **N-R5** A RESERVED row whose locator or incarnation disagrees with the root (moved, re-cloned) | `identity-contradiction` | REG's move or abandonment, which needs user authorization |
| **N-R6** More than one relevant live row; ACTIVE with no marker; a marker with no row | `identity-contradiction` / `identity-recovery-required` | not a crash state of one registration (REG:41-43) |
| **N-R7** A zero-length or prefix marker with no matching RESERVED row | `marker-custody` / `identity-contradiction` | nothing proves it is OpenSIP's |
| **N-R8** A tracked marker path | `marker-tracked` | X2 item 6a |
| **N-P1** A P-ACL candidate that is non-empty, has the wrong owner, mode or link count, is on another filesystem, is a symlink, or has a present non-private ACL | today's custody row for its owner | not the fresh path's own prefix |
| **N-P2** `ledger.sqlite` at length 0 with a `-wal` beside it | `LEDGER.CORRUPT` | X3c item 2, unchanged (`project_ledger_tests.rs:294-298`) |
| **N-L1** Any committed schema object; a freelist page; more than one page; another journal mode or encoding; a nonzero `user_version` or `application_id`; not a database | `LEDGER.CORRUPT` | committed history, or not OpenSIP's creation (`project_ledger_tests.rs:292-340`) |
| **N-T1** A leaf whose bytes are not a strict prefix of the publication's bytes; a non-regular leaf; the wrong owner, mode or links | `installation-incomplete` | foreign or corrupt content (X4T:141) |
| **N-X1** An active transition slot | the incomplete row | S9.2's transition recovery |

### 6. Idempotence, crash during repair, cancellation and concurrency (law)

The X9 rows of item 10 cover each rule.
- **CR-1. A crash inside a completion stays in its family.** Each completion effect is one of the owner's own steps on the same object. A kill inside it leaves either the same state, the next state of the same family, or the completed object:
  - C-ACL killed after the append leaves a private object;
  - C-SUFFIX killed mid-write leaves a longer prefix;
  - C-LEDGER killed before `COMMIT` leaves L-UNC again;
  - C-REG killed in step 3 leaves RW-R1, RW-R2 or RW-R3. Killed in step 4 or 5, it leaves one of RW-R4 to RW-R7. Killed at its ACTIVE rename, it leaves RW-R7, or ACTIVE.

  The next admitted write completes it.
- **CR-2. Monotone, so it terminates.** Every completion moves its object forward along the owner's step order, and never back:
  - the registry row: RESERVED to ACTIVE;
  - the ACL: omitted to private;
  - file bytes: a prefix to a longer prefix to complete;
  - the schema: empty to selected.

  No state recurs after a later one. A run of crashes cannot cycle, and each completion that returns leaves strictly less to do.
- **CR-3. Idempotent.** A completion over an already completed object is the owner's ordinary admit path: no effect, and only the observation is charged. A second request after a completion performs no completion for that object.
- **CR-4. No retry inside a process.** A completion's failed or uncertain step latches its owner's ledger, as any of that owner's steps does (X2:212; X3C item 7). The request ends on that owner's row, and a later request resumes.
- **CR-5. Cancellation.** Every completion runs in J1's phase A, before attempt admission (J1:500). A signal during a completion lets the native effect in flight finish. The request then ends `interrupted` 130 with no runId (J1:661), and the state is resumable by CR-1.
- **CR-6. Concurrency.** Completions run only under the fence (R, RW-P3, T) or the namespace writer lease (RW-P1, RW-P2, RW-L1), so a competing writer gets its busy row. A fence-free `recover(ExecutionId)` reading a ledger during C-LEDGER sees one of two lawful views: before the commit, `ledger-unreadable` (UC); after it, no attempt row (UAU) (X6 item 4).
- **CR-7. Stacking.** Several families can be pending after successive crashes. One request completes them in J1's order (R9, then R10, then `admit_layout`). Each completion touches only its own owner's objects.

### 7. Disclosure, `doctor` and the operational record (lead decision)

- **No public surface changes.** There is no new code, class, exit, detail, subject, envelope member or remedy text (J1:689). A completed request's envelope is an ordinary one.
  - Completing a registration is not installation creation, so J1's `firstUse` stays false (J1:588).
  - A refusal keeps its existing row and subject, which is the disclosure the safety bias asks for.
- **The operational record.** Each completion emits one event, `host.repair.completed`, with:
  - `kind`, from a closed code table: `registration`, `store-directory`, `ledger-file`, `ledger-schema`, `carrier-floors`, `trust-dependency`;
  - `state`, the item 4 state ID.

  It carries no path, ProjectId or bytes. It is an ordinary registration under SOP2 (SOP2:226-231), reviewed in J4's units. Until S-OP-1 the sink is nonpersistent (OPP:211-218).
  - **No new edge.** S-OP-2's registry lands with O1 (M3P:314, day 4). A J4 unit that integrates before O1 returns the completion in its typed result only. The first J4 unit after O1, or O1 itself, adds the event. J4 gains no edge on O1.
- **Recovery never reads logs or crash records** (OPP:211, :313). Every predicate is a fresh observation of the owner's own objects.
- **`doctor` is unchanged.** It writes nothing (OPP:216), and it reports today's rows for these states. The next admitted durable request completes them. This is a stated limit, not a defect.
- **Rejected:**
  - **a new detail, subject or envelope member** ("repaired"): it would be a new public code, and it gives the user nothing to act on;
  - **no record at all:** support then could not tell a resumed project from a fresh one.

### 8. Rows and budget (law)

- **No new row.** Every refusal is an owner's existing row (X2 item 8; X3C item 10; X3B item 8; X4T item 10), now with narrower reach:
  - `identity-recovery-required`, `marker-custody` and `identity-contradiction` no longer arise from RW-R1 to RW-R7 on the write gate;
  - custody `private` no longer arises from RW-P1 or RW-P2;
  - X3b's host I/O row no longer arises from RW-P3;
  - `LEDGER.CORRUPT` no longer arises from RW-L1;
  - `installation-incomplete` no longer arises from RW-T1 or RW-T2.

  Each row's text, class and exit are unchanged.
- **Budget.** Each completion is charged to its owner's ledger before it runs, and reserves its post-effect confirmations, as the owner's own step does (X2 item 9; X3C item 9; X4T item 11). Its read of an existing prefix is bounded by the expected length plus one. If the reservation cannot be taken, the request refuses `WORK.BUDGET_EXHAUSTED` before the completion's first effect.

### 9. Controls

All of these run on scratch installations with labelled synthetic signed profiles and fixtures, as X2c's, X3c-1's, X3b's and X4T's tests do. No production seam is added.
- **RW-C1, each state.** Build each item 4 state, by the owner's crate-private step hooks or a matrix child, then run the owner's step. It completes to the terminal state. The test asserts that the only effects are the owner's own step effects on the named objects: nothing is deleted, and no name is created beyond the owner's own step (the fresh stage, the ACTIVE temporary).
- **RW-C2, each neighbour.** Each item 5 neighbour gives today's row and subject byte for byte. It writes nothing beyond the request's earlier lawful effects.
- **RW-C3, idempotence.** A completion over a completed object performs no effect. A second request performs no completion. CR-3.
- **RW-C4, read paths.** Run the 458c read session, `doctor` (core and project modes), `recover(ExecutionId)`, the sweep and the ephemeral entry over every item 4 state. Each one writes nothing and gives today's outcome byte for byte.
- **RW-C5, L-UNC pins.** The committed views at `x3c.ledger-create.wal` and `ddl.commit.before` satisfy L-UNC. Every fixture of `every_other_creation_footprint_is_ledger_corrupt` (`project_ledger_tests.rs:292-340`) fails it, CREATE-then-DROP included, and stays `LEDGER.CORRUPT`. Item 3.3's stop rule applies.
- **RW-C6, P-ACL.** Negating each clause in turn refuses on today's row. Metadata before and after shows exactly one zero-rights owner allow appended, and no mode bit changed.
- **RW-C7, P-PREFIX.** The prefix's inode and bytes are unchanged and only the suffix is written. A non-prefix refuses.
- **RW-C8, authorization.** Adopt-kind and identity-changed reservations refuse. C-REG compiles only against the write gate's `OrdinaryWriteAdmission` path: a compile-fail fixture shows that no read receipt reaches it.
- **RW-C9, no Run manufactured.** After every completion the ledger holds only what the request's own commit wrote. `recover` of a killed child's ExecutionId never reports committed.
- **RW-C10, census.** The lawful first commit's census (X9-0's) is unchanged by J4. Every new durability point lies under a `.repair` scope (item 10). Release absence covers the new scope names.
- **RW-C11, cancellation.** A phase-A signal during each completion ends `interrupted`, and the next request completes the state. CR-5.
- **RW-C12, budget.** An unreservable completion refuses on the budget row before its first effect.
- **RW-C13, the record.** Each completion emits exactly one `host.repair.completed`, with no path or identity in it.
- **RW-C14, trust names.** C-TRUST creates no new name in any trust collection. After a killed C-TRUST, the structural name scan sees only canonical names. A leaf the admitted closure names is never a strict prefix at publication time.
- **J-C22 (J3d's, answering J1:691).** One host durable request over an RW-R5 fixture ends Committed, with one receipt and an ordinary envelope (`firstUse: false`). One over an N-R2 fixture ends on `identity-recovery-required`, with nothing written.

### 10. X9 r17 rows (record)

These are the rows X9 r17 carries for J-RW, beside J1's S12 rows (J1:708-714, :733), as a named section. Each is transcribed into `required-runs.v1.json` before any run, and none is ever read back from a run (X9:1089, :1233). All are storage-target rows, driven by the existing `commit` driver. No fourth driver entry is added (X9:1236).
- **RW-F00, F00 re-transcribed.** F00's 57 L11 kill points (item 4), killed as F00 kills them:
  - **R2** becomes Committed. R2's run record names the completions it performed, taken from the product's typed completion results, never from a filesystem diff;
  - **R3** as F00's Committed cells;
  - **R1** as F00 r5;
  - **R4** returns to F00 r5's UAU at the seven `x3c.*` points (RW-P1, RW-P2, RW-L1), where R2 now creates the ledger. X9 r8's "R4 stays UC" clause is withdrawn.

  The other F00 cells stand. Each point's state is assigned by its object, from the same unarmed reference run X9 r9 uses for dependency occurrences (X9:146-153).
- **RW-K1 to RW-K9, crash during repair.** A three-child ladder:
  1. child 1 is killed at a start point;
  2. child 2, the repairing writer, is held, then killed at every durability point of its `.repair` scopes;
  3. child 3 commits.

  Start points:
  - RW-K1: `x2.fence.register.reserved/rename.after#1`;
  - RW-K2: `namespace/create.after#1`;
  - RW-K3: `marker/create.after#1`;
  - RW-K4: `x3c.ledger-create.projects/create.after#1`;
  - RW-K5: `x3c.ledger-create/create.after#1`;
  - RW-K6: `x3c.ledger-create.ddl.commit.before#1`;
  - RW-K7: `x3b.floor.directory/create.after#1`;
  - RW-K8: `x4t.floor-publication.dependency/create.after#1`;
  - RW-K9: `dependency/write.before#1`.

  **Expected:** child 3 is Committed, and the completions it names are exactly those whose final effect child 2 had not passed. A kill at a completion's last `.after` point is CR-3's cross-process idempotence row: child 3 names no completion for that object. R1 and R4 run for each killed child that drew an ExecutionId.
- **RW-N1 to RW-N9, refused neighbours** (exec (mut), labelled `mutation`; R1 and R2 only, X9:1079). The parent builds the neighbour on a fresh fixture, then one commit child runs:
  - N-R1, adopt kind;
  - N-R2, exact marker with N absent;
  - N-R3, N with an extra entry;
  - N-R4, a non-prefix marker;
  - N-R7, a zero-length marker with no row;
  - N-P1, a non-empty ACL-omitted `objects/`;
  - N-P2, length 0 with a `-wal`;
  - N-L1, CREATE-then-DROP;
  - N-T1, a non-prefix leaf at a name the publication writes.

  **Expected:** today's row and subject, no completion named, and nothing written past the request's earlier lawful effects.
- **RW-B, contention during repair.**
  - Writer A is held inside C-REG at `x2.fence.register.repair.marker/write.before#1`, with the fence held.
  - Process B, a competing writer of the same root, gets the busy row with no state change.
  - The sweep, C, skips and retains.
  - A is resumed and ends Committed.
- **The census for these rows (law for X9 r17).** J4's census is the census of its own driver runs (X9:170): the unarmed reference run of each RW-K start state, from child 1's kill. RW-K's kill set is every durability point in those traces whose scope carries the `.repair` component, at `#1`, and at the first, a middle and the last occurrence of a repeated protocol (X9:920).
- **Scope names (lead decision).** Each completion's effects run in a scope named after its owner's, with the component `repair` inserted. Examples:
  - `x2.fence.register.repair.namespace/…`, `x2.fence.register.repair.marker/…`, `x2.fence.register.repair.active/…`;
  - `x3c.ledger-create.repair/…`, `x3c.object.repair/…`;
  - `x3b.floor.directory.repair/…`;
  - `x4t.floor-publication.dependency.repair/…`.

  X9-1's site list and X9 r17's scope table gain them.
  - **Rejected:** reusing the first-registration names. A trace could not then tell a completion from a first act, and F00's transcription by window would misattribute points.
- **L11 is retired.** `limits` becomes L1 to L10. The checker's list follows, in `check` and `check-unit`. The power-loss variants stay L1. The neighbours are executed as RW-N rows, not recorded as limits.
- **The lead set.** One serialized lead set on J4e's integration commit, with both targets: storage, F00 to F53 plus the RW rows, and host. It is serialized with every other lead set because of the 5000 ms timing guard (M3P:421).
  - X3c-3's storage-row rerun and J4's lead set are independent. Whichever integrates second reruns both units' rows.
  - J4's rows commit each Run once per namespace, so J4 gains no edge on X3c-3 (P5-1's DAG is kept; M3P:311).

### 11. Units: J4's sub-units

Each is reviewed on its own, with an inventory successor numbered at build time under the linear-chain rule.

| Unit | Content | Depends on | Size |
|---|---|---|---|
| **J4a** | **The shared primitives:** C-ACL over P-ACL in `security::private_access`, used through `store_custody`, and C-SUFFIX over P-PREFIX. **Their X3c and X3b uses:** the store directories (RW-P1), the length-0 ledger file (RW-P2), and `trust/carrier-floors/` (RW-P3). The typed completion result every J4 unit returns, and `host.repair.completed` once O1 has landed (item 7). Tests RW-C1, C2, C3, C6, C7, C10 and C12 for these states. | J-RW, RW-S3, RW-S4 | M |
| **J4b** | **Registration.** `project_admission`'s marker observation and the join classification, on the write gate only. `first_registration`'s C-REG (item 3.4), steps 3 to 6 from the found state. Tests RW-C1 to C4 and RW-C8 for RW-R1 to RW-R7 and N-R1 to N-R8. | J4a, RW-S1, RW-S2 | M |
| **J4c** | **The ledger.** L-UNC and C-LEDGER in `project_ledger`, with disposition `Completed`. Tests RW-C5 and RW-C9. | J-RW, RW-S3 | S |
| **J4d** | **Trust.** RW-T1 and RW-T2 at `write_dependency`. Tests RW-C14. | J4a, RW-S5 | S |
| **J4e** | **The rows.** X9 r17's section: RW-F00, RW-K1 to K9, RW-N1 to N9 and RW-B, transcribed; J4's census; the checker's limit list; release absence for the `.repair` scope names. Then **one serialized lead set** on both targets (item 10). | J4a to J4d, RW-S6 | the lead set |

- **Size.** M + M + S + S, plus the lead set. That is P5-1's "L plus one serialized lead set" (M3P:574).
- **Critical path.** M3P gives J4 3 days, then 1 for its rows, from J-RW at or before day 0: rows by day 4, with slack against M3-X (M3P:311, :340). J4a and J4c run in parallel. J4b and J4d follow J4a. RW-S1 to RW-S6 need not precede day 0. Each gates only its own sub-unit, and J4's slack absorbs their review.
- **J3d** keeps only J-C22. It reaches the completions through J1 item 3's entry (J1:756).

### 12. Successors

| # | Successor | Owner (law) | Content | Gates |
|---|---|---|---|---|
| RW-S0 | **This law** | lead | items 1 to 11 | J4a to J4e |
| RW-S1 | **X2 r10**, shared with J1's S7 (J1:727) | security | Item 4: the join classification, on the write gate only. New item **6c**, reservation completion (item 3.4). Item 8: no new row. The forbidden substitute "deleting or adopting a leftover reservation, namespace or marker" (X2:421) reads "deleting one; adopting one except through item 6c". "Not claimed: explicit recovery" (X2:433) excludes item 6c. | J4b |
| RW-S2 | **Registry owner selection v3** (record) | the registry owner (security) | J-RW is the operation owner that authorizes ordinary, random-kind reservation completion (REG:9, :74). Completing a strict-prefix marker in place is the reservation's own interrupted step, not an overwrite (REG:60). Adoption, move and abandonment are unchanged. | J4b |
| RW-S3 | **X3c r9**, on X3c r8's accepted text. If r8 is still in review when J-RW is accepted, it may instead be folded into r8's next round as its own marked section (item 13). | storage | Item 1: C-ACL for the store directories. Item 2: the length-0 ACL-omitted file and L-UNC become resumable creation states. Item 10: `LEDGER.CORRUPT` narrowed. The forbidden substitute "adopting a partial or schema-less ledger" (X3C:89) excludes L-UNC. Also item 12a's tests and item 13's units (J4a, J4c). | J4a, J4c |
| RW-S4 | **X3b r11** | security, journal | Item 2: C-ACL for `trust/carrier-floors/` under the fence (X3B:52). Item 12: unit J4a. | J4a |
| RW-S5 | **X4T r12**, plus a record note in **X4B r6** (shared with J1's S6, J1:726) | trust | X4T item 7's dependency rule: "create when absent; admit equal bytes; refuse unequal bytes" gains "complete a strict-prefix leaf at a name this publication writes" (item 3.5). X4T item 10's incomplete row is narrowed. X4T items 12 and 13 gain the tests and unit J4d. X4B r6 records that the shared protocol completes such a leaf and deletes nothing (X4B:125-130). | J4d |
| RW-S6 | **X9 r17** (record and rows), shared with J1's S12 (J1:733), as J-RW's own section | lead | item 10 | J4e |
| RW-S7 | **M3-PLAN's next revision** (record) | lead | P5-1's owner list gains X3b and REG. J4's sub-units J4a to J4e. J-RW's cross-law items. | — |
| RW-S8 | **J1's next revision** (record) | lead | Item 11's recommendation is replaced by this law's decisions. Its "`repair recover` command is M5 (BP:973)" is corrected (item 14). J-C22 is defined in item 9. | — |

**Not successors:**
- L465. Its item 5 is the precedent C-ACL extends, by successors RW-S3 and RW-S4. 465's own creator rules are unchanged.
- OWN. §6 is kept: nothing is deleted, staging is never adopted, and "no … directory permission repair" stands, because C-ACL is not one (L465:25).
- IE. See X-RW-1.
- SOP2. `host.repair.completed` is an ordinary registration.

### 13. Cross-law items

- **X-RW-1. "Explicit recovery" (IE:47-50; REG:74). Law that must change: REG (record, RW-S2).**
  - IE: "either unilateral or contradictory presence is an admission refusal requiring explicit recovery/adoption. It never silently chooses one identity."
  - This law keeps the admission refusal: the classification still grants nothing. Its recovery is explicit in IE's sense: a separately specified act with closed predicates, its own classification and its own record. It chooses no identity, because the RESERVED row is the only one, and the marker is absent, a prefix of it, or equal to it.
  - REG:74's "independently authorized" is met by item 2's authorization. REG must record it (RW-S2).
  - If the reviewer reads "explicit" as "user-invoked", IE needs a passage successor. This law then gates J4b on it (review question R1).
- **X-RW-2. The marker in place (REG:60; X2:247). Laws that must change: REG (RW-S2) and X2 (RW-S1).**
  - REG:60: "must not overwrite a … malformed … object". C-SUFFIX overwrites no byte: it writes only past the existing length, into the file the reservation's own step created.
- **X-RW-3. The schema-less ledger (X3C:28, :70, :89). Law that must change: X3c (RW-S3).**
  - X3c item 2 treats only a length-0 file as "creation not begun", while X3b item 3a already reuses an empty database (X3B:86).
  - RW-S3 aligns X3c with X3b, under the stricter L-UNC.
- **X-RW-4. The dependency rule (X4T:102; `floor_publication.rs:455-458`). Laws that must change: X4T (RW-S5), with an X4B record.**
  - X4B:125 rejects "writing records in place". That bullet concerns publishing new trust state by updating existing records. A strict-prefix completion changes no record's content.
  - The reviewer is asked to confirm this reading (review question R3).
- **X-RW-5. Leftovers (X2:256, :421, :433; `first_registration.rs:18-21`). Law that must change: X2 (RW-S1).**
- **X-RW-6. L465 item 5's reach.** It was an owner decision for `OpenSIP` alone (L465:19). C-ACL applies the same rule, a lead decision, to nine more fixed names and to X4T dependency leaves, in X3c, X3b, X2 and X4T.
  - L465 itself does not change. The owners' successors carry the extension.
  - It is flagged for the owner below.
- **X-RW-7. P5-1's owner list** (M3P:573) omits X3b and REG. **Law that must change:** M3-PLAN (record, RW-S7).
- **X-RW-8. J1 item 11's "`repair recover` command is M5 (BP:973)"** (J1:690). That command is the source-repair journal recovery (CINV:988; SL:673), not storage repair. **Law that must change:** J1 (record, RW-S8).
- **X-RW-9. X3c r8, the re-commit successor (P5-2), in draft tonight. No conflict today; a sequencing item and a boundary.**
  1. **Text.** Both successors amend X3c, and both may touch item 10 and the forbidden-substitutes paragraph.
     - **Lead decision:** J-RW's X3c text is RW-S3. It is X3c r9, written on r8's accepted text, or it is folded into r8's next round as a separate marked section if r8 is still in review. Neither waits for the other.
     - **Rejected:** editing r8's draft from here, which would take another agent's subject out from under its review.
  2. **Semantics. Disjoint by construction.**
     - No completion here creates, reads or changes an attempt row, receipt, association, availability record, run material or pin. A ledger completed by C-LEDGER holds the schema only.
     - So nothing J-RW writes can satisfy re-commit's "already committed in the same store and namespace" condition (EXIT:171). Conversely, re-commit cannot find a committed Run in any L11 state, because none holds a receipt.
     - The first commit after a completion is a first commit. If an identical Run commits later, its outcome is X3c's alone: r7 refuses at staging (EXIT:171), and P5-2 intends r8 and X3c-3 to commit it (M3P:576). J-RW changes neither outcome.
  3. **Boundary.** This law leaves `admitted` attempts and every `CommitUndetermined` to X6 (item 1). If X3c r8 lets a re-commit proceed over either, it must cite this boundary, so that the two laws never both claim one state. That is a review point for r8's reviewer, not a change here.
  4. **Matrix.** X3c-3's rows run on day 3 and J4's on day 4 (M3P:421). Whichever integrates second reruns both. RW-F00's Committed cells take X3c-3's postState if X3c-3 has landed. J4's code does not depend on X3c-3.
- **X-RW-10. X9 r17 is shared.** J1's S12 rows and J-RW's RW rows are separate sections of one record revision, with distinct prefixes (`S12-`, `RW-`). Each section's rows are transcribed when its unit is ready. **Law that must change:** X9 (RW-S6).
- **X-RW-11. OWN:119** ("Present I missing … required trust dependency → no inferred pristine creation, reset or repair"). **No conflict.** C-TRUST completes only a leaf that the admitted closure does not name, so it is not a required dependency.

### 14. Record corrections (record only)

- **J1:690.** "A `repair recover` command is M5 (BP:973)." Storage repair has no command at M3, M4 or M5 in BP or CINV. `repair-recover` is source repair (X-RW-8).
- **M3P:573.** "amends X2 item 8, X3c item 10 and the X4T dependency-publication rule". It reads: X2 items 4, 6 and 8 (with REG's record); X3c items 1, 2 and 10; X3b item 2; and X4T item 7, with an X4B record.
- **M2C:349 and X9's limits.** L11's owner is closed by J4's rows (item 10). M2C is a completion record and does not change. X9 r17 carries the change.

## Forbidden substitutes

- A completion on a read path: the read session, `doctor`, the recovery selector, the sweep or the ephemeral entry. A completion in the process that crashed, or a retry of a failed completion in the same process.
- **Deletion of any kind.** Also forbidden: truncation; renaming an existing object away; adopting a stage, a staging name or any temporary name; replacing a trust leaf or a marker by rename; rewriting any existing byte.
- C-ACL on a non-empty directory, or on a file with bytes outside P-PREFIX. C-ACL on an object whose owner, mode, link count or filesystem is not the private shape, or whose ACL is present. Any mode change. Any ACE other than the one zero-rights owner allow.
- Completing a marker or leaf whose bytes are not a strict prefix of the owner's own bytes. Completing a leaf at a name the publication does not write. Visiting an unreferenced leaf.
- Treating a ledger with any committed schema object, a freelist page or a second page as L-UNC. Migrating, truncating, renaming or deleting a ledger. Widening L-UNC to fit a run.
- Completing an adopt-kind reservation. Converting a random row to an adopt row, or the reverse. Abandoning, moving or rewriting a RESERVED row except to its ACTIVE. Completing over an exact marker with N absent. Admitting an incomplete or foreign N.
- Inferring commitment, an attempt row, a receipt or a RunId from any completion. Settling an `admitted` attempt. Touching the journal, witness or carrier outside X3b's own reconciliation.
- Changing classification or rows on any path other than item 3.4's step.
- A new public code, class, exit, detail, subject, envelope member or remedy text. A new CLI word, flag or library entry for repair. Using logs or crash records as recovery input.
- A completion effect outside a `.repair` scope during a matrix run. A matrix expectation read back from a run.

## Lead decisions

Each is dated 2026-10-04 and made under the owner's standing direction. The owner may reverse any of them.

| # | Decision | Rejected alternatives | Item |
|---|---|---|---|
| **LD-1** | Complete forward inside the next admitted durable write, at each owner's own step and under its lock | a separate repair command or entry; completion by the crashed process; completion on a read path or in `doctor`; abandonment and reallocation | 2 |
| **LD-2** | An `OrdinaryWriteAdmission` on the same root, with agreeing locator and incarnation, authorizes random-kind reservation completion | a consent flag (no CLI at M3); adopt rows completed alike (REG:76) | 2 |
| **LD-3** | C-ACL generalizes L465 item 5 to the L11 owners | quarantine-rename; a mode or ACL rewrite; completing non-empty objects | 3.1 |
| **LD-4** | C-SUFFIX: finish an interrupted write in place, suffix only | atomic replacement (temporary names in trust collections; X4B:125; the marker is no-replace); truncate and rewrite; completing non-prefixes | 3.2 |
| **LD-5** | C-LEDGER over L-UNC, stricter than X3b's empty-database rule | rename aside and recreate; any empty-schema database (the CREATE-then-DROP fixture); deletion | 3.3 |
| **LD-6** | C-REG runs X2 item 6's remaining steps from the found state, never touching leftovers | a fresh registration over the reservation; abandonment | 3.4 |
| **LD-7** | No public disclosure; one operational-record event by ordinary registration | a new detail, subject or envelope member; no record at all | 7 |
| **LD-8** | Scope is L11's families exactly, by state and every census occurrence | a general repair of refused states | 1 |
| **LD-9** | `.repair` scope names for completion effects | reusing the first-act names | 10 |
| **LD-10** | X9 r17: re-transcribe F00's L11 cells, add RW-K, RW-N and RW-B, retire L11 | keeping L11 as a limit, which would leave J4 untested | 10 |
| **LD-11** | J-RW's X3c text is X3c r9 on r8, or folded into r8's next round | editing r8's draft from here | 13 |
| **LD-12** | P5-1's owner list gains X3b and REG | leaving RW-P3 (installation-wide) and REG's authorization unowned | 1, 13 |

## Open questions

**No owner decision blocks J-RW.**

**Flagged for the owner (non-blocking lead decisions the owner may reverse):**
1. **LD-1 and LD-2.** A crash during a project's first registration is completed by the next durable analysis of that project, with no prompt and no public notice; only the operational record shows it. The alternative is a refused project until an explicit repair command exists, and none is planned through M5.
2. **LD-3 (X-RW-6).** The owner's 2026-09-27 decision for `OpenSIP` (L465 item 5) is extended to nine more fixed names (X3c's four store directories and ledger file, X3b's `carrier-floors`, X2's `I/host` and `I/host/projects`, and the marker) and to X4T dependency leaves, in four laws.
3. **LD-4 and LD-5.** An interrupted trust record and an interrupted ledger creation are completed in place, never replaced or deleted.

**For the reviewer:**
- **R1.** Does item 2's authorization meet REG:9 and REG:74? Is IE:47-50's "explicit recovery" satisfied without a passage successor (X-RW-1)?
- **R2.** Is L-UNC exactly the committed view at `x3c.ledger-create.wal` and `ddl.commit.before`, and nothing that held evidence? Is item 3.3's stop rule enough?
- **R3.** Is C-SUFFIX on a trust leaf consistent with X4T item 7, X4B:125 and X4B:130, and OWN §6 (X-RW-4, X-RW-11)? Is item 3.5's argument that the leaf cannot be referenced sound?
- **R4.** Is C-ACL a lawful generalization of L465 item 5 to non-creator owners under the writer lease and the fence (X-RW-6)? Is P-ACL's clause 4 (empty) the right bound?
- **R5.** Does C-REG's join meet REG:70-76 exactly: complete footprint, absent namespace, marker order, random kind only?
- **R6.** Is item 4's table complete for L11? Does any census occurrence in these windows leave a state that is neither in item 4 nor in item 5?
- **R7.** Do RW-K's three-child ladder and its census rule cover CR-1 to CR-3 under X9's driver and evidence rules (X9:170, :920, :1079, :1236)?
- **R8.** Is X-RW-9's sequencing with X3c r8 sufficient, given that neither text has been read against the other?

## Not claimed

- No code, test, build or matrix run for this law.
- No CLI or library repair entry. No `doctor` change. No public code, class, exit, detail or subject.
- No recovery of power-loss variants (L1), migrations (L5), orphans (L6), `admitted` attempts, undetermined commits, quarantines, adopt-kind reservations, or moved or re-cloned roots.
- No deletion or cleanup of stages, temporary files or unreferenced trust leaves.
- No reading of X3c r8. Item 13 states only how the two laws must meet.
- J-RW was written from the product at `3e64266` and the laws named above. Every cited product line is unchanged at `e093e90`.
