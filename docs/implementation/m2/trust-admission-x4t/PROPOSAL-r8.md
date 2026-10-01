# Native current-trust admission — proposal X4T r8

2026-09-30. Claude Opus 5.5, implementation lead. Law for unit X4T, the prerequisite that X4 r2 item 1 (RF-1) created. It is written under the security contract's S4 (trust time), S5 (root chains) and S6 (live revocation), owner.md §5 and §7, and laws 463 (core, release and revocation), 466/467 (the P0 trust files), 458c r6, X1 r1, X2 r5, X3a r3, X3b r2 and X4 r3. Items 1, 2, 3, 6, 7, 8, 9 and 11 contain lead decisions made under the owner's standing direction of 2026-09-30 to proceed on the lead's recommendation; each names the alternative it rejects. r1 carried one pre-review correction: rollback is judged against SC-TRUST's own retained floors, never the journal carrier floor (item 7). r2 answers Grok X4T r1 RF-1 to RF-6, aligned with X2 r5, X3b r2 and X4 r3. r1 bytes are preserved in PROPOSAL-r1.md. r3 answers Grok X4T r2 RF-1 (a root chain beyond ChainBudget takes the budget row). r2 bytes are preserved in PROPOSAL-r2.md. r3 ACCEPTED by Grok on 2026-09-30. r4 is an amendment from implementing X4T-a: the r3 read set did not match the product's trust store at 99f1c35. Items 1, 2, 5, 11, 12 and 13 are restated against the real capsule; r3 bytes are preserved in PROPOSAL-r3.md. r5 answers Grok X4T r4's finding that the named binders do not load what r4 assigned to them. The binders' real reach and checks are now stated as of product 8bfc78a, and the members no binder opens are opened by X4T-a itself. r4 bytes are preserved in PROPOSAL-r4.md. r5 was ACCEPTED by Grok on 2026-10-01. r6 is an amendment from implementing X4T-a: the cost pin is a linear-charge pin plus measured and boundary tests, because no lawful generated store reaches the 40 MiB closure. r5 bytes are preserved in PROPOSAL-r5.md. r7 answers Grok r6 RF-1: item 12's budget case now follows item 11's r6 pin. r6 bytes are preserved in PROPOSAL-r6.md. r7 ACCEPTED by Grok on 2026-10-01. r8 (2026-10-01) is an amendment from starting X4T-b, made as lead decisions under the owner's standing direction. As r7 stood, item 7 and item 1 contradicted each other: a floor publication lists only its clock-write event, so on the next admission every accepted role's `accepted.by` named no loaded event and the store refused as incomplete after its first operation. r8 changes items 1, 2, 11, 12 and 13 so that X4T-a loads each such event by reference (unit X4T-a2). It also settles two gaps that r7 left open: what the handoff rollback check compares against (item 7), and what the retained `state.v1` owner is and how it advances (items 7 and 8). r7 bytes are preserved in PROPOSAL-r7.md. Not code. It reads, authenticates and admits the installation's current trust; the only write it defines is the S4 write-ahead floor of item 7.

## Problem

At f7acb6d no code produces an authenticated view of the installation's current trust:
- `trust/native_current.rs` captures `state.v1` and its P2-local joins only as a provisional, supplied-path image ("does not select I/S … or grant authority");
- `captured_capsule_clock.rs` is "a captured retained capsule IMAGE, not admission of the live state.v1 head";
- the ordinary modules (`trust_ordinary_roots`, `trust_ordinary_bundle`, `trust_policy`, `trust_time`, `admitted_revocations`, `role_machine`) authenticate or evaluate only premises their caller supplies, and `trust_time::evaluate_retained_ordinary` "proposes writes only".

X4's operation guard, observer and authority checkpoint all need one admitted current-trust view, `AdmittedCurrentTrust`, produced from the installation's own trust store. X4T composes the existing owners into that admission. It adds no trust semantics of its own.

## Decisions

1. **What an admitted current-trust view is (lead decision).** `AdmittedCurrentTrust` is private, not Clone and not serializable, and is borrowed from the session or operation that produced it. It holds:
   - **The head:** the installation's `trust/stores/S/state.v1` capsule for X3a's admitted S, decoded, capped, and joined to X3a's `C.store`.
   - **The roles (r4).** Roles are not separate files. They are inline objects of the capsule, `roles.TR-BUNDLE`, `TR-COMPONENT`, `TR-CORE`, `TR-INDEX`, `TR-PROFILE` and `TR-REPAIR`, each `{state, accepted{root, rootAdmission, namespaces, catalog, by}, conditionEvidence, reset, ceremony}` (`initial_publication::blank_roles`; `trust_input_bindings::check_capsule_projection`). A role's state is `roles.*.state`.
     - **What the existing checks do (8bfc78a).** `check_capsule_projection` requires `accepted` to be non-null for `ST-TRUSTED` and `ST-REVOKED`, and checks the head counter identity. `current_event_trace::bind_trace` loads the descriptor's events and requires `eventHead` to equal the last listed event. Neither it nor `publication_events::bind_events` reads `accepted.by`.
     - **The `accepted.by` join is X4T-a's own check (r5; r8 lead decision).** For every role whose `accepted` is non-null, `accepted.by` must name an accepted role event of that role:
       - **In the loaded chain.** If `accepted.by` names an event `bind_trace` loaded, that event must be the role's. No further read is made.
       - **Before the current publication (r8).** Otherwise X4T-a opens exactly that one event by its reference: `Budget::load_at` in `Collection::Events`, decoded and admitted as `TrustEventV1`. The loaded event must be a `role-event` of that role, with outcome `accepted`, in this store: its `store`, and the reference's `storeInstanceId`, equal S. Its sequence must be lower than the sequence of the current descriptor's first listed event (or, for a descriptor that lists none, no higher than `eventHead`'s). This is at most one read per role, so at most six. Each is charged and capped in the view's budget like every other member.
       - **Refusals.** A missing, unreadable or mis-shaped event, another role's event, a refused event, another store's event, or one that is not earlier than the current publication refuses as an incomplete installation. The loaded event's own `previous` is never followed, and `history` is never walked (item 11's bound).
       - **Why (r8).** Item 7's floor publication lists only its clock-write event, and so do later floor publications. If `accepted.by` had to be in the current chain, every store would refuse as incomplete after its first floor write.
       - **Rejected:** accepting an `accepted.by` outside the loaded chain without loading it, which would admit a dangling or forged reference; re-listing acceptance events in a floor publication, which `bind_events`' chain rule (`previous` equals the head) forbids; rewriting `accepted.by` in a floor publication, which item 7 forbids; and walking `history` or the event chain back to the acceptance, which is unbounded.
   - **The dependency closure (r4)** of a retained-phase capsule: the publication descriptor; `heads.root`, `heads.catalog` and `heads.revocation`, each a signed body and its envelope in the `objects` collection with its admission record; `history`; the event chain, which is `eventHead` and the current descriptor's `events`; each accepted role's `accepted.by` event that the chain does not contain (r8, at most six); and `clock.record` with its `timeEvidence`. Each member is reached by reference and decoded, capped and admitted. The opener of each member, at 8bfc78a:
     - **`native_current::capture_p2`** loads `state.v1` and the descriptor, then calls `current_record_bindings::bind`.
     - **`current_record_bindings::bind`** admits the inline `clock.record` (`clock::admit`; an inline object, not a separate open) and loads the events through `current_event_trace::bind_trace`. It does not open `history` or `timeEvidence`.
     - **`trust_ordinary_roots::bind_retained_head`** loads the root body and envelope from `objects` (`Budget::load(Collection::Objects, …)`). It keeps the root admission as a reference and does not open it.
     - **No existing binder opens** the root admission record, `heads.catalog` (body, envelope, admission), `heads.revocation` (body, envelope, admission), `history` or `timeEvidence`. X4T-a opens each of them with the same retained-object load `bind_retained_head` uses: `retained_metadata_index::Budget::load` (or `load_at` for a typed native reference), in `Collection::Objects` for signed bodies and envelopes, and in the collection its typed reference names for admission records, `history` and `timeEvidence`. Each is charged, capped and kept in the same budget as the other members.

     The head counter identity (`clock.record`'s `rootVersion`, `indexSnapshotVersion` and `revocationVersion` equal to the heads') is `check_capsule_projection`'s existing check. **Rejected:** a second parser for the capsule. Two parsers of one record could disagree about what was admitted.
   - **The phase.** Only a `retained`-phase capsule has heads and history. A pre-acceptance capsule (`heads` and `history` null, every role `ST-UNBOOTSTRAPPED`) is the P0 case, and refuses as item 10's F-absent row.
   - **The authentication result** of item 3, the revocation set of item 4 and the effective policy of item 5.
   - **The time admission** of item 6: tEval, F, L and the anchor, after item 7's write-ahead if one was needed.
   - **The S6 trust epoch** `{rootVersion, indexSnapshotVersion, revocationVersion, permissionPolicyDigest}` derived from the above, plus the role states from `role_machine`.

   It grants nothing by itself. It is the input X4's guard, observer and checkpoint consume, and the only one they may consume.

   - **Role standing (RF-4; lead decision).** The view runs `role_machine::continuation(core, index, component)` over the admitted role states, exactly as the role machine defines it:
     - **F absent** (no accepted bootstrap, S4 step 2): refuses before the role join, as `TRUST.NO_ADMITTED_TIME_CONTEXT`. This is the P0 creator-only installation, and X4B's precondition.
     - **`Refuse(ContinueCoreNotTrusted | ContinueIndexNotTrusted | ContinueComponentNotTrusted)`:** refuses on item 10's continuation row.
     - **`ExistingOnly`** (core and component `Trusted`, index `Expired` or `StaleRevocation`): the view is admitted and carries `ExistingOnly`. An existing verified process may continue; nothing that starts a new process is granted from this view. X4's grant consults this standing; X4T does not refuse it.
     - **`InstallGateRequiredForNewProcess`:** admitted, carried the same way.
     - **Rejected:** requiring every role `Trusted` (stricter than the role machine), and routing role states to `TRUST.NO_ADMITTED_TIME_CONTEXT` or S5 `ROOT.*` codes (wrong remedies). The embedded release's root (463) authenticates the release, never the installation's current trust; it is not a substitute for an accepted installation root.
   - **Rejected:** admitting a view from the P0 capsule plus the embedded root list. It would let a freshly created installation run operations on trust it never accepted, which X4 r2 forbids.

2. **The read set and its order (lead decision).** One view reads, in this order, each step charged before it runs:
   1. `state.v1`, by name through the retained `trust/stores/S` handle (item 8 says which capture);
   2. the publication descriptor, the inline `clock.record` and the event chain: `native_current::capture_p2`, which calls `current_record_bindings::bind`, whose event loader is `current_event_trace::bind_trace`;
   3. `heads.root`'s body and envelope (`trust_ordinary_roots::bind_retained_head`); then the root admission record, `heads.catalog`'s and `heads.revocation`'s body, envelope and admission record, each opened by X4T-a with `Budget::load` (item 1);
   4. `history` and `timeEvidence`, each opened by X4T-a with `Budget::load` in the collection its reference names (item 1);
   5. `state.v1` again, by name, to confirm it is the same file with the same full sample. On the fenced first read this is item 8's metadata recheck against the retained owner, not a content read.

   Role states are read from the capsule itself in step 1. After step 2, X4T-a checks each accepted role's `accepted.by` against the events `bind_trace` loaded, and opens by reference each `accepted.by` event that is not among them, at most six (item 1, r8). No role file is read. Dependencies come from the four immutable collections under `trust/` (`objects`, `records`, `publications`, `events`), each opened through a retained directory handle with an exact-length cap at its owner's bound (at most 4 MiB, `retained_metadata_index::CAP`). The closure is closed: a reference outside it, a missing member, a duplicate disagreement or a cycle refuses as an incomplete installation. There is no directory scan; every file is reached through a reference.

   **Rejected:** a census of every trust record (`native_census`). The current view needs only the closure its head names; the census is the doctor's and recovery's.

3. **Authentication (lead decision).**
   - **Which roots.** The view is authenticated from the installation's accepted root, `heads.root`, bound by `trust_ordinary_roots::bind_retained_head` and authenticated through `trust_ordinary_roots::authenticate_shared`. A root chain N+1..M recorded in the closure is evaluated link by link under S5 (continuity and possession thresholds, revoked keys excluded, final root unexpired at tEval).
   - **The embedded release's role.** 463 authenticates the running core against the embedded release root. X4T requires that the installation's accepted core closure equals the running core's, as X3a's endpoint join already checks, and that the embedded release's revocation (463) has not revoked it. The embedded root never stands in for the installation's root.
   - **Signatures.** Every accepted document's envelope is reverified against the accepted root's keys at their thresholds, with revoked keys excluded, by the existing envelope and quorum owners. A record whose envelope does not verify refuses; nothing is "accepted because it is in the store".
   - **Rejected:** trusting stored acceptance flags without reverifying signatures. A store rewritten by a local attacker would otherwise grant trust.

4. **Revocation admission.** The accepted revocation document, `heads.revocation`, is opened by X4T-a (item 1). `admitted_revocations::verify_revocation`, which verifies only the bytes it is given, then verifies exactly the stored body and envelope that load supplied against the accepted root, with the keys revoked before it. Its version is the epoch's `revocationVersion`. A revoked component in the closure (the running core, the release, the signing keys, the namespace's catalog snapshot) refuses at admission. A lower revocation version than the floor records is never accepted (item 7).

5. **Policy and grant admission (r4; lead decision).** The trust store carries no permission policy. `trust_policy::merge` takes unsigned local sources, and `Source::Missing` is the empty policy.
   - **Global policy in M2:** `Source::Missing`, the empty policy.
   - **Project policy:** the project owner's (X2), when one exists; otherwise `Source::Missing`.
   - **The digest.** The epoch's `permissionPolicyDigest` is exactly the digest `merge` returns, `Effective::digest()`: the domain-separated hash `opensip.metadata.policy-effective.1` over the merged policy's canonical bytes. The same function produces it on the fenced first read and on every reread, so an unchanged policy always compares equal. In M2, with no global policy file, it is the digest of the empty or project-only merge. The raw SHA-256 of the canonical bytes is never stored in the epoch.
   - X4T admits the effective policy; it does not decide whether a given operation is granted. That is X4's operation grant, which reads the effective policy from the view.
   - **Later unit:** a global policy file under I, with its own custody owner, is a separate later unit (Not claimed).
   - **Rejected:** inventing a signed policy head in the trust store, which no owner defines; and the raw SHA-256 as the digest.

6. **Time admission (lead decision).** X4T applies S4 exactly, through `trust_time::evaluate_retained_ordinary` over the admitted capsule's clock projection:
   - the payload future check, the plausibility check (W > A + 90 d refuses), and in-session continuity;
   - tEval = max(F, W, A);
   - `CLOCK-REGRESSION` and `TRUST.FLOOR_AHEAD_OF_WALL` are findings carried in the view, not refusals.

   **Only the fenced first read admits time** (item 9). Observer rereads do not re-admit time. They evaluate expiry and staleness at the handoff's tEval advanced by the elapsed sleep-inclusive monotonic time on the same boot, and a boot change is a stop (X4 r2 item 5).

   **Rejected:** re-admitting time on every observer tick. It would require a floor write on every tick (item 7), under no fence.

7. **The floor write-ahead and rollback (lead decision).**
   - **Write-ahead.** S4 step 5 requires the floor written to equal tEval before any decision evaluated at tEval is used. When the fenced admission's tEval exceeds the stored F, or L or the anchor advance, X4T's writer publishes the new trust state under the held fence before the view is returned:
     - a new capsule record carrying F := tEval, L and the anchor, with every other field unchanged;
     - its publication event and descriptor;
     - the `state.v1` pointer last, replaced atomically (exclusive temporary name, file barrier, rename, directory barrier, reopen and confirm), as 467 orders dependencies before the pointer.

     The writer reuses 467's existing trust publication producers. It never changes a counter, a role state or an accepted document. It runs only at item 9's fenced, lease-free point: under the installation fence with no project lock held. S7 writes trust state only under the fence and never under a lease. This publication protocol (dependencies through the private-file producer with file and directory barriers, then the pointer by atomic replacement, reopen and confirm, then the owner advance below) has one owner. X4B-a's acceptance publication uses the same protocol (X4B item 5).
   - **The retained `state.v1` owner (r8; lead decision).** At product 66bdd05, X3a-1's single read of `state.v1` keeps only `state.v1`'s `RequiredFile` (its path and full metadata sample) and the decoded `C.store` (S, G, K). It drops the bytes, so the decoded capsule item 8 relies on is not retained anywhere. r8 fixes the owner as follows:
     - **What it is.** The trust current owner is X3a's one read of `state.v1`: the exact bytes of that read, within `CURRENT_STATE_CAP` (4 MiB); the capsule decoded from those bytes by the trust current record's own decoder; and that read's full metadata sample, which is X3a's `RequiredFile` for `trust/stores/S/state.v1`. X4T-b makes X3a's endpoint values keep the bytes of that same read. No new read is made.
     - **The store directory.** Under the fence, X4T-b opens `trust/stores/S` through the fence's retained I and judges it private. It binds the directory to the owner by a no-follow metadata recheck of `state.v1` under it against the owner's sample: same device and inode, same full sample. That is a recheck, not a content read. The pointer replacement renames under this handle.
     - **How it advances.** After a confirmed publication, by this item's protocol or X4B item 5's, the owner becomes the new `state.v1`. The temporary file's identity must be confirmed at the name, its bytes are reread through an exact-length cap and must equal the written bytes, and the capsule is decoded from that reread, never from the writer's memory (X4B item 5). Its post-rename full metadata sample replaces the `RequiredFile` sample in the gate's recheck set. The predecessor owner becomes provenance, and its absence is expected.
     - **What may change it.** Only that transition. Any other change to the name, the file or its sample before the fence is released fails the recheck as `required-files-changed`.
     - **Rejected:** a second fenced content capture of `state.v1` (item 8: two owners for one file); keeping only the sample and rereading the bytes at the fenced read, which is also a second owner; and advancing the owner from the written bytes in memory without the reopen.
   - **After the fence is released, the capture is provenance (RF-2; X4 r3 item 4).** No recheck compares the live `state.v1` with it. A newer pointer published by another writer is admitted as a new view (item 9), and X4's S6 predicate decides whether it revokes, is drift or is a rollback.
   - **Rollback at the handoff (r8 states the comparison exactly; lead decision).** On the fenced first read, the admitted capsule's floors are its `clock.record` values F (`evalHighWater`), L (`lastAccepted`), `rootVersion`, `revocationVersion` and `indexSnapshotVersion`. They are compared with SC-TRUST's own retained floors, using only what the view has already read:
     Checks 1 and 2 apply only when `clock.timeEvidence` is an `s4-evaluation` input. An S4.5 epoch input records S4.5's recovery, the only lawful act that lowers a floor, so it is not compared.
     1. **The time evidence's before-clock.** `clock.timeEvidence` is a closure member that X4T-a already opens (item 1). Its `beforeClock` is the clock of the trust state that evaluation was made on, which is a retained predecessor. If that clock is `retained`, each of the five capsule floors must be at least the same field of its `record`. If it is `evaluated`, F and L must be at least its projection's. If it is `unevaluated`, there is nothing to compare.
     2. **The time evidence's observation.** F must be at least the `wall` of the evidence's `observation`. S4 step 5 wrote F ≥ tEval ≥ W at that evaluation, and F only rises.
     3. **This fence hold's own floors.** If the retained owner was advanced in this fence hold (a floor publication, or X4B's acceptance), each capsule floor must be at least the same floor of every capsule the hold retained before it.

     A capsule below any of these refuses as `trust-rollback`. A lower counter never revokes (S6). The journal carrier floor is never used: X3b r2 item 7 fixes it as a closed journal high-water, `{highWaterSchema, projectKeyDigest, grantGeneration, lastSeq, tailSha256}`, that records no trust epoch. On an unfenced reread, the same comparison (1 and 2 only) is an error of X4's callback, which X4 latches as `OBSERVER.FAIL_STOP` (item 9), never this custody row.
     - **Stated limit: a whole-file restore is not detectable.** If an older `state.v1` is restored together with its whole closure, the capsule is self-consistent, and every comparison above passes: its evidence and its predecessors are older still. Every member of SC-TRUST lives under I, and a restore of I or of `trust/` rolls all of them back together. Detecting it needs an anchor outside the restored unit, which no accepted law defines. This is a selected limit, not an open defect, in the same form as S6's carrier anchor bound. No M2 unit closes it. X9's matrix records it as a stated limit and does not test it as a refusal. The owner of a later closure is S9.3's authorized restore lineage (a restored store gets its own `storeInstanceId`) or a future anchor outside I. Neither is claimed here.
     - **Rejected:**
       - Reading the predecessor capsule named by `previous` or `nativeBefore`. It is an extra read outside item 2's closed closure, and no law requires that image to be kept in `trust/records`, so it could refuse lawful stores.
       - Probing the successor bucket `trust/publications/by-predecessor/<sha256 of this state.v1>`. A successor written before a crash, with the pointer never replaced, is a lawful and harmless state (item 7; X4B item 6), so the probe would call that state a rollback. A whole restore removes the bucket anyway.
       - The journal carrier floor (X3b r2 item 7). It is closed and records no trust epoch, and it lives under I too.
       - A new floor file outside I. That would be a new custody owner that no law defines.
   - **Report-only.** A read session (458c, doctor) runs the same evaluation and returns the proposed writes without performing them (S4's report-only mode).
   - **Rejected:** admitting a decision at tEval without the write-ahead. It lets a later evaluation run earlier than an earlier one, which S4 forbids.

8. **Reuse of the 458c and X3a capture.** The fenced first read does not read `state.v1` again. It takes the retained trust current owner of item 7 (r8): X3a's one read, meaning its bytes, the capsule decoded from them, and its full sample. It also takes the `trust/stores/S` handle that X4T-b opens and binds to that owner by a metadata recheck. The dependency closure is new reading, because no earlier unit reads it. Observer rereads (item 9) do read `state.v1` again by name; that is their purpose.

   **Rejected:** a second fenced capture of `state.v1`. It would duplicate X3a's read and give two owners for one file.

9. **The fenced versus unfenced reread protocol (lead decision).**
   - **Fenced first read: before any lease (RF-1).** It runs under the installation fence with no project lock held, at the same point as X3b's floor step: X2 r5 item 7's ordering note, after the current registry owner R is fixed and before item 7 takes any lease. It is not part of item 7a. It performs items 2 to 7, including any write-ahead, and its view becomes the operation's start epoch. The operation's `FreshnessMonitor` is created at this point and this admission is its first `read` call, so the monitor's clock brackets it (X4 r3 item 2). Item 7a then moves the view and the monitor into `ProjectOperation`; item 7a publishes no trust state.
     - **Rejected:** running the admission inside item 7a. The lease is held there, and S7 forbids the floor write under a lease; skipping the write would return a view at a tEval whose floor was not written ahead.
   - **Unfenced reread: one attempt (RF-3).** X4T supplies one attempt: given the retained `trust/stores/S` and collection handles and an opened `state.v1`, it captures the head and its closure and performs items 2 to 5 (head, closure, authentication, revocation, policy), with no time re-admission (item 6) and no write (item 7). It never retries, and never calls `FreshnessMonitor::read`.
     - **The only retry is X4's.** X4 r3 item 5's single `read` callback opens `state.v1`, calls this attempt, reopens `state.v1`, and, if the identity differs, does all of it once more. So at most two views are charged per observation, which is what X4's ledger is sized for (item 11).
     - **Its errors are X4's.** An unreadable record, a failed authentication, a rollback below the retained floors, or a second mixed view is returned to X4's callback as an error. X4 latches it as `OBSERVER.FAIL_STOP` (exit 4, `HOST.IO_FAILURE`). None of them is published on item 10's rows.
     - **A later pointer.** A newer `state.v1` is admitted like any other view; X4's S6 predicate decides whether it revokes, is drift, or is a rollback.
   - **Rejected:** taking the fence for rereads. It would invert S7's lock order and deadlock with the journal append lock. Also rejected: a retry inside X4T, which would nest inside X4's and charge four views to a two-view ledger.

10. **Refusal rows (no new codes).** Every refusal maps through 468c's `InstallationTermination` to an existing row; where S12 or the public detail registry fixes a class for a detail, that class prevails:
    These rows are the fenced admission's only. Unfenced reread errors are X4's `OBSERVER.FAIL_STOP` (item 9).
    - missing, undecodable, oversize or misbound trust records, an incomplete closure: the incomplete row (`CONFIG.CUSTODY_REFUSED`, subject `installation-incomplete`), and the `installation-incomplete:current-store` doctor subject for `state.v1` (X3a item 5);
    - F absent (no accepted bootstrap, S4 step 2): `TRUST.NO_ADMITTED_TIME_CONTEXT`, class request-rejected, exit 2, `REQUEST.PRECONDITION_FAILED`. It is used for nothing else;
    - a continuation refusal (item 1): request-rejected, exit 2, `EXTENSION.ADMISSION_REJECTED`, the continuation row, with a subject naming the role and its state (`core:revoked`, `index:quorum-lost`, `component:unbootstrapped`, and so on):
      - `ContinueCoreNotTrusted`: detail `CONTINUE-CORE-NOT-TRUSTED`, its registered code;
      - `ContinueIndexNotTrusted` and `ContinueComponentNotTrusted`: the security contract names them `CONTINUE-INDEX-NOT-TRUSTED` and `CONTINUE-COMPONENT-NOT-TRUSTED`, but neither is a registered public code, and new public codes are the owner's (468 item 6). Until the owner decides, they publish the registered continuation detail `CONTINUE-CORE-NOT-TRUSTED`, with the role-naming subject (`index:…`, `component:…`) as the only distinction. This is an interim lead decision; adding the two codes is listed for the owner below;
    - an `Expired` core: the continuation row above (`core:expired`). An index or component `Expired` by the clock is never an S5 `ROOT.*` row;
    - a root chain refusal: its S5 `ROOT.*` detail, naming the link. Only the chain evaluation produces these;
    - a signature or quorum failure, or a future payload: `PAYLOAD-NOT-ADMISSIBLE`;
    - plausibility or continuity: `CLOCK-EXCURSION-FORWARD`, with its S4 subject `beyond-horizon` or `in-session`;
    - a revoked component at admission: `CONTINUE-CORE-NOT-TRUSTED`, subject the revoked component (during an operation, X4 owns `TRUST.COMPONENT_REVOKED_DURING_OPERATION`);
    - a rollback below SC-TRUST's own retained floors: `CONFIG.CUSTODY_REFUSED`, subject `trust-rollback`;
    - an unsupported schema: `ROOT.SCHEMA_UNSUPPORTED` or `STATE.SCHEMA_UNSUPPORTED`;
    - I/O, a failed write-ahead confirmation, budget (including a root chain beyond `ChainBudget`, item 11): the host I/O and budget rows.

11. **Budget (lead decision; RF-5).**
    - **The closure is closed and counted (r4).** One view reads at most:
      - one head and one publication descriptor;
      - three heads (root, catalog, revocation), each a body, an envelope and an admission record: nine objects;
      - `history`, `clock.record`'s record and `timeEvidence`: three;
      - the event chain: `eventHead` and the current descriptor's `events`, at most `MAX_VIEW_EVENTS = 32`;
      - the `accepted.by` events outside that chain, at most one per role: six (r8, item 1);
      - the root chain N+1..M.

      That is at most 53 files plus the chain.
    - **The event-chain bound (r4; lead decision).** The view binds only the current publication's events: the descriptor's `events` list, ending at `eventHead`. It never walks earlier publications. Earlier publications are `history`'s, which is bound by reference, not walked. `MAX_VIEW_EVENTS = 32`: one publication records one trust transaction, which touches at most the six roles, each with at most four events (accept, condition, reset, ceremony), so 24 at most, with margin. A descriptor whose `events` list is longer refuses on the budget row; it is never truncated. **Rejected:** the record shape's own bound of 65536 events, which no per-view ceiling can cover; and walking every publication back to genesis, which is unbounded.
    - **The chain budget.** The root verifier is called with `ChainBudget { max_links: 16, max_stored_bytes: 16 MiB }`. A recorded chain beyond either refuses on the existing budget row: `WORK.BUDGET_EXHAUSTED`, operational-failed, exit 4, `SYSTEM.OUTCOME.ILLEGAL_STATE`, `host-invariant`. A limit failure is unavailability (owner §7), and `ChainError::Limit` has no public detail of its own. The chain is never truncated. **Rejected:** the `max_links: 131072`, 256 MiB budget some test owners pass, which no per-view ceiling can cover.
    - **The per-file cap stays the owners', with a closure total (r4; lead decision).** Every file keeps its owner's 4 MiB cap (`trust::metadata::MAX_BYTES`, `retained_metadata_index::CAP`). The closure's files together are also bounded by a stored-bytes total of 40 MiB, in the same way `ChainBudget` bounds the chain. A real store's closure is kilobytes (the P0 set is about 4 KiB). **Rejected:** per-file caps alone. At 53 × 4 MiB, doubled for two views, the cost exceeds the owner's 256 MiB cap. Also rejected: lowering the per-file caps, which would refuse lawful records.
    - **The ceiling covers that closure at its bounds.** `TRUST_VIEW_COST` is:
      - objects ≤ 128 (53 files and 16 links, with margin; r8 adds six files and leaves the ceiling unchanged);
      - edges ≤ 2048;
      - bytes ≤ 112 MiB. That is 2 × (40 MiB + 16 MiB): each byte read is charged once on retention and once for its counted decoded tree, which `check_value` bounds by the same byte count.
    - **Pinned by test (lead decision, r6).** A lawful generated store cannot reach the 40 MiB closure total. A revocation list, for example, holds at most 4096 entries of 256 characters, about 1.3 MiB, and reaching 40 MiB would need many component manifests. So X4T-a pins three things instead of one full-size measurement:
      1. **The linear charge:** an in-memory view charges exactly one object and its stored bytes per distinct record read, so (objects, bytes) equals (records read, their total size). At the bounds that gives 56 MiB against the 112 MiB ceiling.
      2. **A measured native read** of a generated store, within `TRUST_VIEW_COST`.
      3. **Boundary tests of the closure check:** 40 MiB plus a full chain admits, and just over 40 MiB with a small chain refuses.

      Rejected: extending X4T-0 into a padded, chained 40 MiB generator, a large fixture that tests the same linear rule. If a later measurement shows a factor above two, the ceiling is raised, never the bounds lowered. A view over the ceiling refuses on the budget row; it is never truncated.
    - **Where it is charged.** The fenced first read charges the gate ledger while the fence is held; the write-ahead reserves its post-publication confirmation before its first effect. An unfenced reread charges X4's per-observation ledger. At 2 × `TRUST_VIEW_COST` that ledger is 256 objects, 4096 edges and 224 MiB, inside the owner's 256 MiB byte cap. X4 must adopt these figures in place of the ones it states today (r4 note, below).

12. **Tests.** On scratch installations with real signed trust from X4T-0's generator (item 13). No signed end-to-end accepted store exists today: the existing trust corpora use placeholder hashes. The generator writes an accepted, retained-phase store after the P0 publication. Cases:
    - a P0 creator-only installation refuses `TRUST.NO_ADMITTED_TIME_CONTEXT`;
    - an admitted view, with its epoch;
    - each role state's row;
    - a bad signature, a wrong-threshold quorum, a future payload;
    - a root chain through expired intermediates, and an expired final root;
    - a revoked core closure;
    - a rollback below SC-TRUST's own retained floors;
    - time: a floor advance is written ahead and the retained `state.v1` owner advances; a W beyond A + 90 d writes nothing; report-only returns proposed writes and writes nothing;
    - rereads: one attempt per call, with no retry inside X4T; through X4's callback, a pointer change mid-read retries once and a second change is `OBSERVER.FAIL_STOP`; a newer pointer with an unrelated revocation is admitted as drift input; the start-epoch capture is not compared with the live pointer after release;
    - role standing: F absent gives `TRUST.NO_ADMITTED_TIME_CONTEXT`; each continuation refusal gives its role-naming subject; `ExistingOnly` is admitted and carried; an index `Expired` by the clock is never an S5 row;
    - the policy digest is `Effective::digest()` on both reads, and an unchanged policy compares equal;
    - the fenced admission and its write-ahead run with the fence held and no project lock;
    - floor publication (r8): after a floor publication, the next admission of the store is admitted, with `accepted.by` reached by reference; the advanced owner's capsule comes from the reopen, and its sample replaces the `RequiredFile` sample; any other change before the release is `required-files-changed`; rollback refuses as `trust-rollback` for each of item 7's three comparisons, and an S4.5 epoch input is not compared; a whole-file restore of an older self-consistent store is admitted, which pins the stated limit;
    - budget: item 11's r6 pin, which is the linear charge (one object and its stored bytes per distinct record read), a measured native read within `TRUST_VIEW_COST`, and the closure-check boundary (40 MiB plus a full chain admits; just over 40 MiB with a small chain refuses); a 33-event descriptor refuses; a 17-link chain refuses; a closure over 40 MiB refuses; the ceiling refusal;
    - closure: roles read from the capsule; X4T-a's `accepted.by` check refuses a role whose `accepted.by` names another role's event; (r8) an `accepted.by` outside the current chain is opened by reference and admitted when it is an earlier accepted role event of that role in this store, and refused when it is missing, another role's, refused, another store's, or not earlier than the current publication; at most six such reads, and the event's own `previous` is never followed; each member item 1 assigns to X4T-a is opened by `Budget::load` and a missing one refuses; a head counter mismatch refuses; a pre-acceptance capsule refuses as F absent; the existing binders are the only parsers.

    There is no production seam: the fixture is `cfg(test)` in the security crate.

13. **Units.**
    - **X4T-0 (new in r4; test-only).** A signed accepted-store generator in the security crate, `cfg(test)`. It produces:
      - a real signed root, catalog and revocation, with envelopes, from test keys;
      - consistent admission records, `history`, the event chain, the clock record and time evidence;
      - roles in the requested states, each with `accepted.by` naming one of the current descriptor's events for that role, so X4T-a's check (item 1) passes;
      - the retained-phase capsule and `state.v1`.

      It drives every item 12 case.

      **Test-only record constructor (lead decision, pre-review correction).** At 99f1c35 the product has no producer for most retained-phase kinds. Only P0 creation (`initial_publication.rs`) and test-only signing helpers exist. The kinds with no producer are:
      - `RootAdmissionNodeV1` and `MetadataAdmissionNodeV1`;
      - `RevocationHistoryNodeV1`;
      - `RoleEventV1` and `RoleChangeV1`;
      - `PublicationEventV1`;
      - `TimeEvidenceV1` and `SignedTimeSourceV1`;
      - a retained-phase `TrustCapsuleV1` (non-null heads and history, roles past unbootstrapped).

      Their real producer is trust acceptance (X4B, S4) and S4.5. So X4T-0 constructs exactly these kinds itself, `cfg(test)` in the security crate. Each is canonically encoded against its closed shape, signed with the public test quorum seeds, and accepted by the existing binders.

      The round-trip test requires `capture_p2` (with `bind_trace` as its event loader), `current_record_bindings::bind`, `bind_retained_head`, X4T-a's own loads and `accepted.by` check, and, as an additional acceptor, `publication_events::bind_events`, to accept the written store. The constructor is never compiled into a release build. No production path can reach it (a source pin guards this). It grants no standing outside tests.

      Rejected:
      - moving X4B before X4T-a, which would lengthen the critical trust chain and couple the reader to acceptance;
      - using the placeholder-digest corpora, which are not signed stores.

      X4B remains the only production producer and is required before X11. It is reviewed on its own, before X4T-a.
    - **X4T-a:** the read-only admission (depends on X4T-0): items 1 to 6, 8, 9 (the fenced read and the one-attempt reread), 10 and 11, with report-only time. Depends on X3a-1.
    - **X4T-a2 (r8; code successor to X4T-a).** Item 1's `accepted.by` load by reference (at most six reads) in `check_accepted_by`, its item 12 tests, and item 11's measured cost constants (`MEASURED` and `NATIVE_MEASURED` move by the counted events). Depends on X4T-a. The fixture already names events in the current descriptor, so it needs no change. The out-of-chain case is tested on a store after a floor publication, or on a fixture successor that X4T-a2's tests build.
    - **X4T-b:** the write-ahead floor publication, the publication protocol it shares with X4B-a, the retained `state.v1` owner and its advance, and the handoff rollback comparison (items 7 and 8, r8). Depends on X4T-a2 and reuses 467's trust publication producers. X4T-a2 and X4T-b may be implemented and reviewed as one unit.
    - **First trust acceptance (new follow-up, X4B).** Until an installation's roles are `Trusted`, no operation can be admitted. The first acceptance of the core's embedded bootstrap payload (S4 step 2) as an authenticated installation trust event is a separate law and unit. It is not needed for the M2 exit matrix, which runs on synthetic signed trust stores, but it is needed before any real installation can commit. EXIT-PLAN gains it before X11.

## Forbidden substitutes

The floor write or fenced admission under a project lease; a retry inside X4T's reread; comparing the live `state.v1` with the start capture after the fence is released; storing any digest but `Effective::digest()` as `permissionPolicyDigest`; a chain budget beyond 16 links or 16 MiB; a view built from the P0 capsule, the embedded root list or stored acceptance flags without reverifying signatures; a census in place of the head's closure; a second fenced capture of `state.v1`; a directory scan to find trust records; time re-admitted on an unfenced reread; a decision at tEval without the write-ahead floor; any write other than item 7's floor publication; a floor write without the fence; replacing the retained `state.v1` owner while the fence is held, except through a confirmed publication; taking the fence on a reread; admitting a lower counter or floor; a truncated or partially read view; (r8) an `accepted.by` outside the loaded chain accepted without loading it, or following that event's `previous`; a rollback check that reads beyond the closure, probes a successor bucket or uses the journal carrier floor; advancing the retained owner from the written bytes without the reopen; a new public code (item 10 publishes the two unregistered continuation reasons under the registered detail until the owner decides).

## Not claimed

A global permission policy file under I and its custody owner (a later unit; item 5); the first trust acceptance (X4B); trust import, recovery challenge and recovery import (S4.5); X4's operation grant, observer, checkpoint and S6 predicate; rollback of effects; any doctor trust report; (r8) detecting a whole-file restore of an older, self-consistent `state.v1` and its closure, which is item 7's stated limit; Linux; a qualified measured macOS 27 profile row. On this BASELINE-ATTESTED host a real installation never reaches X4T, because reads refuse at `/` without a premise.

## Lead decision: two continuation codes (2026-09-30, under the owner's standing direction)

The security contract's role machine refuses a non-trusted index or component as `CONTINUE-INDEX-NOT-TRUSTED` or `CONTINUE-COMPONENT-NOT-TRUSTED`. Neither is a registered public code.
- **Decision.** Add exactly these two codes in a contract successor (unit X4T-c), as 468a added three: common4 append, public detail registry rows, D9 routes, generation and drift check. They carry the continuation row's class: request-rejected, exit 2, `EXTENSION.ADMISSION_REJECTED`.
- **Until X4T-c lands,** item 10 publishes them under the registered `CONTINUE-CORE-NOT-TRUSTED`, with a subject naming the role.
- **Rejected:** permanently folding the index and component cases into the core code. The public detail would then name the wrong role.

## r4 note: the matching X4 correction

X4's current text needs these changes to match r4. They are X4's own amendment, not this law's:
1. **Ledger.** Item 5's per-observation ledger becomes 2 × `TRUST_VIEW_COST`: 256 objects, 4096 edges and 224 MiB.
2. **Retained handles.** Item 5's reading path retains `trust/stores/S` and the four collection directories (`objects`, `records`, `publications`, `events`), not only `trust/records`. Its step 2 captures in item 2's order through item 2's loaders: `capture_p2` (with `current_record_bindings::bind` and `bind_trace`), `bind_retained_head`, and X4T-a's `Budget::load` of the root admission, the catalog and revocation heads, `history` and `timeEvidence`, followed by X4T-a's `accepted.by` check.
3. **Policy drift.** In M2 the global policy is `Source::Missing`, so a policy change can come only from the project owner's policy. X4's "policy removing a required grant" and `policy-unrelated` drift remain correct and can fire only then.
4. **Role standing.** X4's grant consults the view's continuation standing (item 1), including `ExistingOnly`.
