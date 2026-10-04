# Native current-trust admission — proposal X4T r13

2026-09-30. Claude Opus 5.5, implementation lead. Law for unit X4T, the prerequisite that X4 r2 item 1 (RF-1) created. It is written under the security contract's S4 (trust time), S5 (root chains) and S6 (live revocation), owner.md §5 and §7, and laws 463 (core, release and revocation), 466/467 (the P0 trust files), 458c r6, X1 r1, X2 r5, X3a r3, X3b r2 and X4 r3. Items 1, 2, 3, 6, 7, 8, 9 and 11 contain lead decisions made under the owner's standing direction of 2026-09-30 to proceed on the lead's recommendation; each names the alternative it rejects. r1 carried one pre-review correction: rollback is judged against SC-TRUST's own retained floors, never the journal carrier floor (item 7). r2 answers Grok X4T r1 RF-1 to RF-6, aligned with X2 r5, X3b r2 and X4 r3. r1 bytes are preserved in PROPOSAL-r1.md. r3 answers Grok X4T r2 RF-1 (a root chain beyond ChainBudget takes the budget row). r2 bytes are preserved in PROPOSAL-r2.md. r3 ACCEPTED by Grok on 2026-09-30. r4 is an amendment from implementing X4T-a: the r3 read set did not match the product's trust store at 99f1c35. Items 1, 2, 5, 11, 12 and 13 are restated against the real capsule; r3 bytes are preserved in PROPOSAL-r3.md. r5 answers Grok X4T r4's finding that the named binders do not load what r4 assigned to them. The binders' real reach and checks are now stated as of product 8bfc78a, and the members no binder opens are opened by X4T-a itself. r4 bytes are preserved in PROPOSAL-r4.md. r5 was ACCEPTED by Grok on 2026-10-01. r6 is an amendment from implementing X4T-a: the cost pin is a linear-charge pin plus measured and boundary tests, because no lawful generated store reaches the 40 MiB closure. r5 bytes are preserved in PROPOSAL-r5.md. r7 answers Grok r6 RF-1: item 12's budget case now follows item 11's r6 pin. r6 bytes are preserved in PROPOSAL-r6.md. r7 ACCEPTED by Grok on 2026-10-01. r8 (2026-10-01) is an amendment from starting X4T-b, made as lead decisions under the owner's standing direction. As r7 stood, item 7 and item 1 contradicted each other: a floor publication lists only its clock-write event, so on the next admission every accepted role's `accepted.by` named no loaded event and the store refused as incomplete after its first operation. r8 changes items 1, 2, 11, 12 and 13 so that X4T-a loads each such event by reference (unit X4T-a2). It also settles two gaps that r7 left open: what the handoff rollback check compares against (item 7), and what the retained `state.v1` owner is and how it advances (items 7 and 8). r7 bytes are preserved in PROPOSAL-r7.md. r9 answers Grok X4T r8 RF-1: item 7 check 3 compares only predecessors with an evaluated or retained clock; an unevaluated predecessor has nothing to compare. r8 bytes are preserved in PROPOSAL-r8.md. r9 ACCEPTED by Grok on 2026-10-01. r10 (2026-10-01) is an amendment from Grok's X4B-a r1 judgment call 12, made as lead decisions under the owner's standing direction. As r9 stood, item 3 named `heads.root` as the accepted root, and X4T-a passes it to `authenticate_shared` as both the accepted root and the signing root. `verify_captured_core` requires the closure's first `rootChain` body to equal the accepted root and its last to equal the signing root. So a recorded rotation (root 1 to root 2, which X4B-a writes with `heads.root` and `clock.record.rootVersion` at root 2, as S5 requires) refused `FirstIdentity` before any link was evaluated. r10 changes item 3: `heads.root` stays the signing (final) root M that document signatures use; the accepted root N is the first body of the closure's `rootChain`; the links after it are S5's N+1..M. The knock-on edits are in items 1 (the epoch's `rootVersion`), 2 (the read set), 7 (one confirming sentence; no comparison changes), 10, 11 (the chain count), 12 (tests) and 13 (unit X4T-a3), plus the forbidden substitutes and an r10 note for X4B. r9 bytes are preserved in PROPOSAL-r9.md. r11 answers Grok X4T r10 RF-1: item 4 verifies `heads.revocation` against the signing root, `heads.root`, not the accepted root. r10 bytes are preserved in PROPOSAL-r10.md. r11 ACCEPTED by Grok on 2026-10-01 (arch `846071458`; the acceptance note in the live r11 file said 2026-10-03, which was a slip). r12 (2026-10-04) is the law for unit X4-F2, the follow-up that X4-F1 found and that M2-COMPLETE r3 §5 row 23 records: "the fenced read computes the expiry flags but never applies them". Its lead decisions are made under the owner's standing direction. As r11 stood, item 6's expiry and staleness reached the role states only on observer rereads (unit X4-F1, integrated at product `15c0779`). The fenced first read carried S4's three expiry states on its time admission and joined only the stored role states, as X4T-a r1 judgment call 6 accepted. So a store already expired or stale at the handoff's tEval was admitted at the lease-free point, took its lease, and fail-stopped as `OBSERVER.FAIL_STOP` at its first tick or checkpoint (GROK2's X4-F1 r1 review, judgment call 6). r12 applies `EV-CLOCK` at tEval on the fenced read. A refusal from that clock is published on item 10's continuation row at the lease-free point, after item 7's write-ahead. r12 also states how the fenced read's clock composes with the reread's. The edits are in items 1, 6, 7, 9, 10, 12 and 13, the forbidden substitutes, Not claimed, and a new r12 note; the "r12 changes" table lists them. r11 bytes are preserved in PROPOSAL-r11.md. r12 ACCEPTED 2026-10-04 by Codex (`cf566db7…`; `reviews/grok2-x4t-f2-r1/`), with no required findings. r13 (2026-10-04) is J-RW r4's successor RW-S5, its X4T part: item 7's publication protocol completes two interrupted steps, a torn leaf at a name the publication writes and a parent directory left without its owner allow, on both ends of the fenced read. J-RW r4 is the accepted resume/repair writer law, cited as JRW (`docs/implementation/m3/resume-repair-jrw/PROPOSAL-r4.md`, sha256 `9c53bce7…`; accepted by Codex, `m3/reviews/codex-resume-repair-jrw-r4`); its row RW-S5 is JRW:683. In JRW, X4T:NNN is r12's line, preserved in PROPOSAL-r12.md. r13 keeps r12's clock and write-ahead rules unchanged. Its lead decision is made under the owner's standing direction. The edits are in items 7, 10, 12 and 13, the forbidden substitutes and a new r13 note; the "r13 changes" table lists them. **Draft r13, not accepted.** Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the autonomous run. r12 bytes, as accepted (sha256 `cf566db7…`, without the acceptance note), are preserved in PROPOSAL-r12.md. Not code. It reads, authenticates and admits the installation's current trust; the only write it defines is the S4 write-ahead floor of item 7.

## r13 changes

| Where | Change | Source |
|---|---|---|
| Header | r12's acceptance, and what r13 changes | JRW:683; `reviews/grok2-x4t-f2-r1` |
| Item 7 | The dependency rule gains two completions: C-TDIR completes a `may_create` parent directory left without its allow, and C-TRUST completes a strict-prefix leaf at a name this publication writes. They run on both ends of the fenced read. r12's clock and write-ahead rules are unchanged. | JRW:683; JRW items 2, 3.5 and 3.6 (JRW:177-188, :373-415) |
| Item 10 | The incomplete row no longer arises from the three completed states. No new row, and every other state keeps its row. | JRW:460-462, :510-511 |
| Item 12 | J4d's tests: RW-C14, RW-C15, RW-C18 and RW-C19 | JRW:544-575 |
| Item 13 | Unit J4d | JRW:665 |
| Forbidden substitutes | The completions' bars. P-ACL's emptiness check is not a scan to find trust records (LD13-1). | JRW:747-749, :756-761 |
| r13 note | RW-S5's other part, X4B r6's record note, has landed. X4 and X9 need no amendment from r13. | JRW:683; X4B r6:151, :157-161 |

**LD13-1. P-ACL's emptiness check is not "a directory scan to find trust records" (lead decision).** C-TDIR's predicate needs the directory to hold no entry but `.` and `..`, by one bounded scan (JRW:220-224, :398-403). This law forbids "a directory scan to find trust records", because its read set is reference-directed (item 2).
- **Decision.** They compose. The check runs only at the parent step of a publication, on a directory the admitted closure does not name. It reads no record and selects nothing, and any entry it finds refuses on today's row (JRW N-T2b).
- **Rejected:** treating the check as that forbidden scan, which would make C-TDIR impossible as JRW states it; and probing a fixed list of names instead, which cannot prove that a directory is empty.

## r12 changes

| Where | Change | Source |
|---|---|---|
| Header | The r12 note, and r11's acceptance date corrected to 2026-10-01 | M2-COMPLETE r3 §5 row 23; arch `846071458` |
| Item 1 | Each read joins the role machine twice: over the stored states before authentication, as in r11, and over the states clocked at its instant after item 6. The view carries the clocked states and standing. | GROK2 X4-F1 r1 call 6 |
| Item 6 | New: expiry at the fenced read (lead decision). `EV-CLOCK` at tEval over S4's three states, by X4B r5 item 4's mapping; the join; nothing recorded; report-only; how it composes with the reread, with no double application; rejected alternatives. | S4 step 5 and "Consequences"; X4B r5 item 4; X4-F1 |
| Item 7 | New: the write-ahead also precedes a clocked refusal (lead decision); the hold after that refusal; refusing before the write is rejected. | S4 step 5 |
| Item 9 | The fenced first read clocks at tEval and may publish the continuation row before any lease. The unfenced reread is unchanged. | X4 r7 item 8 and its r5 note |
| Item 10 | The clocked continuation row: `core:expired` and `core:stale-revocation`, after the write-ahead. A final root expired at tEval is never `ROOT.FINAL_EXPIRED`. | X4T-a r1 call 6; S5 |
| Item 12 | The r12 tests, and the existing tests that must not move | — |
| Item 13 | Unit X4-F2: scope, dependencies, X4T-0's test-only knobs, the controls, and the X9 regression subset | M3-PLAN r9 P5-4 |
| Forbidden substitutes | Seven r12 entries | — |
| Not claimed | Expiry between reads, native scheduling, recorded `EV-CLOCK` transitions, F9 | GROK2 X4-F1 r1, "Not in this unit" |
| r12 note | X4, X4B and X9 need no amendment; record items for integration | — |

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
   - **The S6 trust epoch** `{rootVersion, indexSnapshotVersion, revocationVersion, permissionPolicyDigest}` derived from the above, plus the role states from `role_machine`. (r10) `rootVersion` is the signing root's, `heads.root`'s, which is M after a recorded chain (S5: success advances the root counter to M). It is never the accepted root N's.

   It grants nothing by itself. It is the input X4's guard, observer and checkpoint consume, and the only one they may consume.

   - **Role standing (RF-4; lead decision).** The view runs `role_machine::continuation(core, index, component)` over the admitted role states, exactly as the role machine defines it:
     - **F absent** (no accepted bootstrap, S4 step 2): refuses before the role join, as `TRUST.NO_ADMITTED_TIME_CONTEXT`. This is the P0 creator-only installation, and X4B's precondition.
     - **`Refuse(ContinueCoreNotTrusted | ContinueIndexNotTrusted | ContinueComponentNotTrusted)`:** refuses on item 10's continuation row.
     - **`ExistingOnly`** (core and component `Trusted`, index `Expired` or `StaleRevocation`): the view is admitted and carries `ExistingOnly`. An existing verified process may continue; nothing that starts a new process is granted from this view. X4's grant consults this standing; X4T does not refuse it.
     - **`InstallGateRequiredForNewProcess`:** admitted, carried the same way.
     - **(r12) Two joins per read.** Every read runs the join twice:
       - over the stored states (`roles.*.state`), before authentication, as above;
       - after item 6, over the states `EV-CLOCK` gives at that read's instant: tEval on the fenced first read (item 6, r12), or the advanced instant on a reread (item 6, X4-F1).

       The view carries the clocked states (`role_states`) and the standing of the second join. The stored states stay the capsule's, and no X4T write changes them (item 7).
     - **Rejected:** requiring every role `Trusted` (stricter than the role machine), and routing role states to `TRUST.NO_ADMITTED_TIME_CONTEXT` or S5 `ROOT.*` codes (wrong remedies). The embedded release's root (463) authenticates the release, never the installation's current trust; it is not a substitute for an accepted installation root.
   - **Rejected:** admitting a view from the P0 capsule plus the embedded root list. It would let a freshly created installation run operations on trust it never accepted, which X4 r2 forbids.

2. **The read set and its order (lead decision).** One view reads, in this order, each step charged before it runs:
   1. `state.v1`, by name through the retained `trust/stores/S` handle (item 8 says which capture);
   2. the publication descriptor, the inline `clock.record` and the event chain: `native_current::capture_p2`, which calls `current_record_bindings::bind`, whose event loader is `current_event_trace::bind_trace`;
   3. `heads.root`'s body and envelope (`trust_ordinary_roots::bind_retained_head`); then the root admission record, `heads.catalog`'s and `heads.revocation`'s body, envelope and admission record, each opened by X4T-a with `Budget::load` (item 1). (r10) Item 3's accepted root is read from the root admission's `parent`, the `PayloadMetadataClosureV1` that the existing authentication composition (`ordinary_inventory::prepare`) already loads from `records`: its first `rootChain` document's body, from `objects`. Both are loads by reference through the same `Budget`, which keys retained bytes by collection and digest, so a member already retained is not charged as a second object;
   4. `history` and `timeEvidence`, each opened by X4T-a with `Budget::load` in the collection its reference names (item 1);
   5. `state.v1` again, by name, to confirm it is the same file with the same full sample. On the fenced first read this is item 8's metadata recheck against the retained owner, not a content read.

   Role states are read from the capsule itself in step 1. After step 2, X4T-a checks each accepted role's `accepted.by` against the events `bind_trace` loaded, and opens by reference each `accepted.by` event that is not among them, at most six (item 1, r8). No role file is read. Dependencies come from the four immutable collections under `trust/` (`objects`, `records`, `publications`, `events`), each opened through a retained directory handle with an exact-length cap at its owner's bound (at most 4 MiB, `retained_metadata_index::CAP`). The closure is closed: a reference outside it, a missing member, a duplicate disagreement or a cycle refuses as an incomplete installation. There is no directory scan; every file is reached through a reference.

   **Rejected:** a census of every trust record (`native_census`). The current view needs only the closure its head names; the census is the doctor's and recovery's.

3. **Authentication (lead decision).**
   - **Which roots (r10; lead decision).** The view names two roots, which are the same document when the recorded chain has one root:
     - **The signing root** is `heads.root`, root M, bound by `trust_ordinary_roots::bind_retained_head`. It is the final root of the recorded chain. Every accepted document's envelope is reverified against it (Signatures, below). Its version is the epoch's `rootVersion` and the capsule's `clock.record.rootVersion` (item 1, and `check_capsule_projection`'s head counter identity); its expiry is `clock.record.rootExpiresAt`, which S5 requires unexpired at tEval (item 6).
     - **The accepted root** is root N, the first document of the closure's `rootChain`. The closure is the `PayloadMetadataClosureV1` named by `parent` of `heads.root`'s root admission record. It is the root the installation held when the recorded chain was accepted: the root X4B authenticated against the embedded binding, or an earlier head for a later accepted payload.
     - **The chain.** The `rootChain` documents after the first are the links N+1..M. They are evaluated link by link under S5: continuity and possession thresholds, revoked keys excluded, contiguity from N's `rootVersion`, intermediate expiry never consulted.
     - **The calls.** X4T passes the accepted root (its document reference and its validated payload) to `trust_ordinary_roots::authenticate_shared` as the accepted root, and `heads.root` as the signing root. `verify_captured_core` then checks the first `rootChain` body against N and the last against M, verifies N's own envelope at its threshold with revoked keys excluded, and authenticates the links after the first from N. `verify_captured_core` is not changed.
     - **The closure join.** The last `rootChain` document must equal `heads.root.document` exactly, both body and envelope references, as the root admission's `root` already must. A `rootChain` that is empty or ends elsewhere refuses as an incomplete installation. A value-only match is not enough: the head's envelope and the chain's last envelope would then be different stored bytes for one root.
     - **One root.** When `rootChain` has one document, the accepted root and the signing root are both `heads.root`, there are no links, and the result is r9's.
     - **Rejected:**
       - `heads.root` as both roots (r9 as implemented): every recorded rotation refuses `FirstIdentity`, including X4B's default release;
       - recording the first root as `heads.root`: documents are signed by the final root, and S5 and the head counter identity put the counter at M;
       - recording only the final root in the closure: the inventory's `RootCount` join requires the closure chain to match the payload manifest, and N+1..M would never be evaluated;
       - the embedded release's root as the accepted root: it never stands in for the installation's root (below), and a later accepted payload starts from an earlier head, not from it;
       - relaxing `verify_captured_core`'s first-identity check: it is shared with the ordinary-root owners and their oracle tests (`originalAcceptedRef`, `projectedAcceptedRef`).
   - **The embedded release's role.** 463 authenticates the running core against the embedded release root. X4T requires that the installation's accepted core closure equals the running core's, as X3a's endpoint join already checks, and that the embedded release's revocation (463) has not revoked it. The embedded root never stands in for the installation's root.
   - **Signatures.** Every accepted document's envelope is reverified against the signing root's keys (r10: `heads.root`, root M; r9 said "the accepted root's", which is the same root when the chain has one) at their thresholds, with revoked keys excluded, by the existing envelope and quorum owners. A record whose envelope does not verify refuses; nothing is "accepted because it is in the store".
   - **Rejected:** trusting stored acceptance flags without reverifying signatures. A store rewritten by a local attacker would otherwise grant trust.

4. **Revocation admission.** The accepted revocation document, `heads.revocation`, is opened by X4T-a (item 1). `admitted_revocations::verify_revocation`, which verifies only the bytes it is given, then verifies exactly the stored body and envelope that load supplied against the signing root, `heads.root` (root M), with the keys revoked before it (r11; r9 and r10 said "the accepted root", which r10 redefined as root N; a list signed by M need not meet N's quorum). Its version is the epoch's `revocationVersion`. A revoked component in the closure (the running core, the release, the signing keys, the namespace's catalog snapshot) refuses at admission. A lower revocation version than the floor records is never accepted (item 7).

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

   **Expiry at the fenced read (r12; lead decision).** S4 says expiry and staleness "fail closed at tEval". The fenced first read now applies them to the role states at tEval itself, not first at the operation's first reread.
   - **The instant.** The instant is tEval: the instant S4 step 5 has just admitted (`TimeAdmission.evaluation`), and the floor that item 7 writes. It is never W, never the stored F, and never a later monitor sample.
   - **The states.** They are S4's own three, which `finish` computes at tEval over the authenticated documents (`TimeAdmission.expired`):
     - root expiry: the signing root's `expiresAt` (`clock.record.rootExpiresAt`, root M), expired iff tEval ≥ it;
     - catalog expiry: the catalog's `expiresAt`, expired iff tEval ≥ it;
     - staleness: the revocation list's `issuedAt` plus 90 days, stale iff tEval > it.

     These are the same three fields and the same rule (`expiry_states`) as a reread uses (X4-F1). Every admitted evaluation carries them. If they are absent, the read refuses on the host I/O row, as X4B-a treats the same absence; they are never taken as false (S4 step 2).
   - **The mapping (X4B r5 item 4, unchanged).** `EV-CLOCK` runs through `role_machine::decide` (`role_machine::clock`) on each stored state:
     - root expiry goes to TR-BUNDLE, TR-COMPONENT and TR-CORE;
     - root or catalog expiry goes to TR-INDEX;
     - staleness goes to all four;
     - TR-PROFILE and TR-REPAIR keep their stored states.

     `decide`'s transition applies as it stands:
     - from `Trusted` or `StaleRevocation`, expiry gives `Expired`;
     - from `Trusted`, staleness alone gives `StaleRevocation`;
     - every other state is kept. `Expired`, `QuorumLost`, `Revoked`, `Recovery` and `Unbootstrapped` never move.
   - **The join (item 1).** The second join runs over the clocked core, index and component:
     - root expiry refuses `core:expired`; staleness refuses `core:stale-revocation`; with both, expiry wins, as `decide` orders them;
     - a catalog expiry alone makes the index `Expired` and the standing `ExistingOnly`, which is admitted and carried (X4 r7, r5 note);
     - with no state true, the clocked states equal the stored ones, and so does the standing.
   - **Where it runs.** It is the admission's last decision. It runs after every refusal of items 2 to 5 and after S4's own refusals, steps 1 to 4: a future payload or time range, no admitted time context, in-session, and beyond the horizon. Those write nothing and keep their precedence.
   - **What it publishes.** A clocked refusal is item 10's continuation row, published after item 7's write-ahead (item 7, r12) at the lease-free point (item 9). An admitted view carries:
     - the clocked states and standing;
     - the unchanged `TimeAdmission`, which still carries S4's three states;
     - the handoff clock (X4-F1).
   - **Nothing is recorded.** The clock is an evaluation in the view. No `EV-CLOCK` event is written and no stored role state is rewritten; item 7's writer never changes a role state. Every later read evaluates again from the same stored states.
   - **Report-only (item 7).** A report-only read computes the same states, the same join and the same refusal, and writes nothing. S4: report-only "computes the same decision, states and findings".
   - **Composition with the reread (X4-F1): each read clocks once.** A read clocks the stored states of the capsule it admitted, once, at its own instant:
     - the fenced read at tEval;
     - a reread at T = tEval + (M − M_handoff), on the same boot, over its own capsule's stored states. It never clocks the start view's clocked states.

     The start view's roles and standing are not inputs to a reread, nor to X4's S6 predicate, which compares the epoch, the floors and the closure.
     - **No double application.** T ≥ tEval, and each of S4's three states, for the same documents, can only turn from false to true as the instant rises. So a reread never finds the same documents in better standing than the fenced read did. A store refused at the fenced read would, with the same documents, also have been refused by its first reread, and r12 moves that refusal ahead of the lease. A store admitted `ExistingOnly` stays `ExistingOnly` or is refused later.
     - **Why the rule still holds.** `decide`'s `Clock` is monotone and idempotent, so clocking at tEval and then again at T would give the same state as clocking once at T. r12 still forbids it (Forbidden substitutes), so that a reread's result never depends on the start view.
     - **A newer pointer** is a new view with its own stored states and documents (item 9). It is clocked at the same advanced instant T.
   - **Rejected:**
     - **Leaving the fenced read unclocked** (r11, as X4T-a r1 call 6 accepted). An operation that is expired at its own decision instant would start. It takes its lease, runs X3b's floor step and the carrier start, and stops only at its first tick or checkpoint, as `OBSERVER.FAIL_STOP` (operational-failed, exit 4, `HOST.IO_FAILURE`) with subject `standing`. That is the wrong class and the wrong remedy for an expired trust store, which is request-rejected (exit 2) on the continuation row. It also misses S4's "fail closed at tEval" at the one read that evaluates at tEval.
     - **Refusing on any expiry state.** A catalog expiry alone gives `ExistingOnly`, which the role machine admits (X4-F1 judgment call 3; X4T-a r1 call 6).
     - **Recording `EV-CLOCK` in the trust store,** in item 7's floor publication or in a new one:
       - item 7's writer never changes a role state;
       - each read's states would depend on which process wrote last;
       - recorded clock transitions are trust updates with their own producers (X4B at acceptance, and a later trust-update unit), not this reader's.
     - **Clocking at W, at F, or at the monitor's opening instant.** S4 evaluates at tEval = max(F, W, A), and that is the instant whose floor item 7 writes.

7. **The floor write-ahead and rollback (lead decision).**
   - **Write-ahead.** S4 step 5 requires the floor written to equal tEval before any decision evaluated at tEval is used. When the fenced admission's tEval exceeds the stored F, or L or the anchor advance, X4T's writer publishes the new trust state under the held fence before the view is returned:
     - a new capsule record carrying F := tEval, L and the anchor, with every other field unchanged;
     - its publication event and descriptor;
     - the `state.v1` pointer last, replaced atomically (exclusive temporary name, file barrier, rename, directory barrier, reopen and confirm), as 467 orders dependencies before the pointer.

     The writer reuses 467's existing trust publication producers. It never changes a counter, a role state or an accepted document. It runs only at item 9's fenced, lease-free point: under the installation fence with no project lock held. S7 writes trust state only under the fence and never under a lease. This publication protocol (dependencies through the private-file producer with file and directory barriers, then the pointer by atomic replacement, reopen and confirm, then the owner advance below) has one owner. X4B-a's acceptance publication uses the same protocol (X4B item 5).
   - **(r12) Before a clocked refusal too (lead decision).** S4 step 5 requires the floor equal to tEval to be written before any decision evaluated at tEval is used. A refusal on item 6's clocked states is such a decision: it is made at the admitted tEval (step 5). S4's own refusals (steps 1 to 4) write nothing because they come before any instant is admitted.
     - **What the fenced read does.** When item 6's clock refuses, the fenced read performs this write-ahead exactly as it would for an admitted view: the same producers, the same publication and the same owner advance, and only when S4 proposes a change. Then it publishes the continuation row, and no view is returned.
     - **What is unchanged.** Check 3 (below) and the read's closing rechecks run where they run today, and a refusal either raises is published instead. A report-only read writes nothing. A refusal raised before time is admitted (items 2 to 5 and the stored-state join of item 1) writes nothing, as in r11.
     - **The hold after the refusal.** The confirmed publication is durable, and the retained owner has advanced inside the read, as after X4B item 4's refusal following a recorded acceptance (X4B-b). The write gate's step then fails and the gate is spent, so no later recheck compares the predecessor's sample. The refusal is never relabelled `required-files-changed`.
     - **Why.** The floor makes the refusal sticky. Every later evaluation of the store runs at tEval′ = max(F, W′, A) ≥ tEval, so it refuses again whatever the wall clock reads, until a newer accepted document or S4.5's recovery. r11 already wrote this floor for such a store, because r11's fenced read admitted it.
     - **Rejected:** refusing before the write-ahead. A later read with the wall clock set back below the expiry would then evaluate at a lower tEval and admit the store. A later evaluation would run earlier than an earlier one, which S4 forbids. It would also be weaker than r11 as built.
   - **(r13, JRW RW-S5) The dependency rule, and two completions of an interrupted step.** The protocol writes each dependency only at a content-addressed name that is absent. It admits an existing name only when that file is private and holds exactly the dependency's bytes (`floor_publication.rs:455-488` at product `d2c00a9`). A publication creates a missing parent directory only where `may_create` permits it (`:406-415`): the `trust/publications/by-predecessor` bucket; its predecessor directory `by-predecessor/<P>`, where P names the publication's predecessor; and `trust/objects`, which X4B-a's first acceptance creates. Every other parent must already exist. r13 adds two completions to this rule. Each finishes the step a crash interrupted, on the same object, by the protocol's own primitive (JRW item 3).
     - **C-TDIR: complete a `may_create` parent directory left without its allow (JRW item 3.6, state RW-T3).** At the parent step (`parent_dir`, `:416-451`), before any dependency is written.
       - **The state.** `create_private_directory` makes the directory by `mkdirat 0700`, then appends the zero-rights owner allow (`private_access.rs:209-238`). A kill between the two leaves it empty, `0700`, with its ACL omitted. The pointer was never replaced, so `state.v1` and its admitted closure are unchanged. Today `open_private` judges the directory and refuses `installation-incomplete` at every later publication from that pointer (`:158-172`), installation-wide.
       - **The predicate.** All of these hold: the name is one that `may_create` permits at that depth; `open_private`'s native open has succeeded and returned the retained directory (`:164-166`); and P-ACL holds on that handle. P-ACL means: owned by the invoking user; mode exactly `0700`; ACL omitted (`CapturedAclState::NotReturned`; a NOACL sentinel, an inconsistent capture or a present ACL is not omission); on its parent's filesystem; and no entry but `.` and `..`, by one bounded scan (LD13-1).
       - **Action.** Append exactly one zero-rights owner allow and sample again, through the fresh path's own step (`prepare_fresh_private_sample`). The new sample must judge private, or the step refuses on today's row; the allow stays. Then the creation path's own barrier and its parent's (`:439-446`). The publication then continues to its dependencies and the pointer.
       - **Never completed.** A native open failure keeps the host I/O row: a symlink (`O_NOFOLLOW`) or a non-directory (`O_DIRECTORY`) at the name (JRW N-T2a). An opened directory that fails the custody judgment other than by P-ACL keeps `installation-incomplete` (JRW N-T2b): one that holds any entry, has the wrong owner or mode, or has a present non-private ACL, or an ACL-omitted directory at a name `may_create` does not permit. A parent outside `may_create` is never completed.
     - **C-TRUST: complete a strict-prefix leaf at a name this publication writes (JRW item 3.5, states RW-T1 and RW-T2).** At the dependency step (`write_dependency`, `:459-488`), when the name is present.
       - **The states.** A kill after the exclusive create leaves the leaf zero-length, with its ACL omitted (RW-T1). A kill during the write leaves it private and torn, a strict prefix of its bytes (RW-T2). Today both refuse `installation-incomplete` when a later publication writes that same name (`:470`, `:479`), installation-wide.
       - **The predicate, P-PREFIX.** The leaf is a regular file, owned by the invoking user, with mode exactly `0600` and one link, on its parent's filesystem. Its ACL is omitted or judged private. Its bytes, read with a bound of the dependency's length plus one, are a strict prefix (the empty prefix included) of the bytes this publication writes at that name, whose digest the name addresses (`:253-261`).
       - **Action.** First C-ACL, as above, if the ACL is omitted. Then write only the missing suffix, at an offset equal to the existing length. Then the file barrier (`F_FULLFSYNC`), the directory barrier, and an exact-length capped read-back that must equal the dependency's bytes, on the same device and inode. No existing byte is rewritten, so the leaf only ever holds a prefix of its own bytes, or all of them.
       - **Never completed.** A leaf whose bytes are neither exactly equal to nor a strict prefix of the publication's bytes, a non-regular leaf, or one with the wrong owner, mode or link count keeps `installation-incomplete` (JRW N-T1). An exactly equal private leaf is today's ordinary admission. A torn leaf at a name no later publication writes is never visited. It stays unreferenced and harmless (X4B item 6).
     - **Why no trust admission is relaxed.** The fenced first read admitted a closure that does not name the leaf or the directory. A named, torn member would have refused that read as incomplete (item 10). The closure is read and authenticated by items 1 to 5, before item 6's clock, so this holds on both ends of the read. The publication writes only its own determined list of names. The predecessor directory is the current capsule's successor bucket, which the rollback check never probes and item 2's reference-directed read never opens. So the read admits and refuses exactly what it does in r12, and skips no trust check.
     - **Both ends of the fenced read (JRW item 2, LD-16).** The completions run inside this item's write-ahead, wherever it runs: before an admitted view is returned, and before r12's clocked continuation refusal (the r12 bullet above). On the clocked path they rest on the same authority as the publication itself: the closure the read authenticated, and the pending write its admission carries (`current_trust_admission.rs:243-289`, `:1113-1125` at `d2c00a9`). They manufacture no view and grant no lease. After the publication confirms and the owner advances, the read returns exactly r12's clocked refusal, at the same precedence (items 9 and 10).
     - **What r13 keeps from r12, unchanged.** Item 6's `EV-CLOCK` at tEval. This item's write-ahead before a clocked refusal. Item 9's refusal before every lease and later operation effect. A refusal raised before time is admitted (items 2 to 5, the stored-state join of item 1, and S4's steps 1 to 4) writes nothing and completes nothing, and so does a report-only read. A completion or publication failure on the clocked path ends on its own row, which `publish` returns before `into_view` runs (`floor_publication.rs:993`, `:995`): the host I/O row, `installation-incomplete` or the budget row. It never becomes the clocked refusal.
     - **What never happens.** No deletion, truncation, rename away, or temporary name in a trust collection. No rewrite of an existing byte of any record. No mode change, and no ACE but the one zero-rights owner allow. No completion on a read path, and none in the process that crashed. The protocol keeps its one owner, and X4B's acceptance publication gains both completions unchanged (X4B item 5).
     - **Budget.** Each completion is charged to the gate ledger before it runs, and reserves its post-effect confirmations, as the write-ahead does (item 11). The prefix read is bounded by the dependency's length plus one.
   - **The retained `state.v1` owner (r8; lead decision).** At product 66bdd05, X3a-1's single read of `state.v1` keeps only `state.v1`'s `RequiredFile` (its path and full metadata sample) and the decoded `C.store` (S, G, K). It drops the bytes, so the decoded capsule item 8 relies on is not retained anywhere. r8 fixes the owner as follows:
     - **What it is.** The trust current owner is X3a's one read of `state.v1`: the exact bytes of that read, within `CURRENT_STATE_CAP` (4 MiB); the capsule decoded from those bytes by the trust current record's own decoder; and that read's full metadata sample, which is X3a's `RequiredFile` for `trust/stores/S/state.v1`. X4T-b makes X3a's endpoint values keep the bytes of that same read. No new read is made.
     - **The store directory.** Under the fence, X4T-b opens `trust/stores/S` through the fence's retained I and judges it private. It binds the directory to the owner by a no-follow metadata recheck of `state.v1` under it against the owner's sample: same device and inode, same full sample. That is a recheck, not a content read. The pointer replacement renames under this handle.
     - **How it advances.** After a confirmed publication, by this item's protocol or X4B item 5's, the owner becomes the new `state.v1`. The temporary file's identity must be confirmed at the name, its bytes are reread through an exact-length cap and must equal the written bytes, and the capsule is decoded from that reread, never from the writer's memory (X4B item 5). Its post-rename full metadata sample replaces the `RequiredFile` sample in the gate's recheck set. The predecessor owner becomes provenance, and its absence is expected.
     - **What may change it.** Only that transition. Any other change to the name, the file or its sample before the fence is released fails the recheck as `required-files-changed`.
     - **Rejected:** a second fenced content capture of `state.v1` (item 8: two owners for one file); keeping only the sample and rereading the bytes at the fenced read, which is also a second owner; and advancing the owner from the written bytes in memory without the reopen.
   - **After the fence is released, the capture is provenance (RF-2; X4 r3 item 4).** No recheck compares the live `state.v1` with it. A newer pointer published by another writer is admitted as a new view (item 9), and X4's S6 predicate decides whether it revokes, is drift or is a rollback.
   - **Rollback at the handoff (r8 states the comparison exactly; lead decision).** On the fenced first read, the admitted capsule's floors are its `clock.record` values F (`evalHighWater`), L (`lastAccepted`), `rootVersion`, `revocationVersion` and `indexSnapshotVersion`. They are compared with SC-TRUST's own retained floors, using only what the view has already read. (r10) The `rootVersion` floor is `clock.record`'s, which equals `heads.root`'s, the signing root M. Item 3's accepted root N is never a floor and is never compared, so r10 changes none of these checks:
     Checks 1 and 2 apply only when `clock.timeEvidence` is an `s4-evaluation` input. An S4.5 epoch input records S4.5's recovery, the only lawful act that lowers a floor, so it is not compared.
     1. **The time evidence's before-clock.** `clock.timeEvidence` is a closure member that X4T-a already opens (item 1). Its `beforeClock` is the clock of the trust state that evaluation was made on, which is a retained predecessor. If that clock is `retained`, each of the five capsule floors must be at least the same field of its `record`. If it is `evaluated`, F and L must be at least its projection's. If it is `unevaluated`, there is nothing to compare.
     2. **The time evidence's observation.** F must be at least the `wall` of the evidence's `observation`. S4 step 5 wrote F ≥ tEval ≥ W at that evaluation, and F only rises.
     3. **This fence hold's own floors.** If the retained owner was advanced in this fence hold (a floor publication, or X4B's acceptance), each capsule floor must be at least the same floor of every capsule the hold retained before it whose clock is evaluated or retained. A predecessor whose clock is unevaluated (the P0 `state.v1` before X4B's acceptance) has no floors and nothing to compare, as in check 1, so check 3 admits X4B's acceptance.

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
     - **(r12) Its item 6 includes `EV-CLOCK` at tEval.** A clocked continuation refusal is published here, after item 7's write-ahead and before any lease. No view is returned and item 7a never runs, so no lease, X3b floor step, carrier start or effect follows. This is X4 r7 item 8's "no admitted current trust" route (X4T's own rows) and X4 r7's r5 note: `Continuation::Refuse` stays X4T's admission refusal at the lease-free point. X4B's confirming admission runs the same item 6 (below, r12 note).
     - **Rejected:** running the admission inside item 7a. The lease is held there, and S7 forbids the floor write under a lease; skipping the write would return a view at a tEval whose floor was not written ahead.
   - **Unfenced reread: one attempt (RF-3).** X4T supplies one attempt: given the retained `trust/stores/S` and collection handles and an opened `state.v1`, it captures the head and its closure and performs items 2 to 5 (head, closure, authentication, revocation, policy), with no time re-admission (item 6) and no write (item 7). It never retries, and never calls `FreshnessMonitor::read`.
     - **The only retry is X4's.** X4 r3 item 5's single `read` callback opens `state.v1`, calls this attempt, reopens `state.v1`, and, if the identity differs, does all of it once more. So at most two views are charged per observation, which is what X4's ledger is sized for (item 11).
     - **Its errors are X4's.** An unreadable record, a failed authentication, a rollback below the retained floors, or a second mixed view is returned to X4's callback as an error. X4 latches it as `OBSERVER.FAIL_STOP` (exit 4, `HOST.IO_FAILURE`). None of them is published on item 10's rows.
     - **A later pointer.** A newer `state.v1` is admitted like any other view; X4's S6 predicate decides whether it revokes, is drift, or is a rollback.
     - **(r12) Unchanged.** The reread clocks its own stored states at its instant (item 6, X4-F1). Its continuation refusal remains an error of X4's callback, `OBSERVER.FAIL_STOP` with subject `standing`, never item 10's row.
   - **Rejected:** taking the fence for rereads. It would invert S7's lock order and deadlock with the journal append lock. Also rejected: a retry inside X4T, which would nest inside X4's and charge four views to a two-view ledger.

10. **Refusal rows (no new codes).** Every refusal maps through 468c's `InstallationTermination` to an existing row; where S12 or the public detail registry fixes a class for a detail, that class prevails:
    These rows are the fenced admission's only. Unfenced reread errors are X4's `OBSERVER.FAIL_STOP` (item 9).
    - missing, undecodable, oversize or misbound trust records, an incomplete closure, (r10) a closure `rootChain` that is empty or whose last document is not `heads.root.document` (item 3): the incomplete row (`CONFIG.CUSTODY_REFUSED`, subject `installation-incomplete`), and the `installation-incomplete:current-store` doctor subject for `state.v1` (X3a item 5);
    - F absent (no accepted bootstrap, S4 step 2): `TRUST.NO_ADMITTED_TIME_CONTEXT`, class request-rejected, exit 2, `REQUEST.PRECONDITION_FAILED`. It is used for nothing else;
    - a continuation refusal (item 1): request-rejected, exit 2, `EXTENSION.ADMISSION_REJECTED`, the continuation row, with a subject naming the role and its state (`core:revoked`, `index:quorum-lost`, `component:unbootstrapped`, and so on):
      - `ContinueCoreNotTrusted`: detail `CONTINUE-CORE-NOT-TRUSTED`, its registered code;
      - `ContinueIndexNotTrusted` and `ContinueComponentNotTrusted`: the security contract names them `CONTINUE-INDEX-NOT-TRUSTED` and `CONTINUE-COMPONENT-NOT-TRUSTED`, but neither is a registered public code, and new public codes are the owner's (468 item 6). Until the owner decides, they publish the registered continuation detail `CONTINUE-CORE-NOT-TRUSTED`, with the role-naming subject (`index:…`, `component:…`) as the only distinction. This is an interim lead decision; adding the two codes is listed for the owner below;
    - an `Expired` core: the continuation row above (`core:expired`). An index or component `Expired` by the clock is never an S5 `ROOT.*` row;
    - (r12; lead decision) a core made `Expired` or `StaleRevocation` by item 6's clock at tEval: the continuation row above. The subject is `core:expired` or `core:stale-revocation`; with both states, expiry wins. The row is published after item 7's write-ahead.
      - **No new subject.** Both subjects are already published for stored states, which X4B's acceptance records.
      - **A final root expired at tEval** takes this row, never `ROOT.FINAL_EXPIRED`. The view authenticates the root chain without time (`authenticate_shared`, through `authenticate_root_chain`), so the root's expiry reaches the view only as S4's first state. `ROOT.FINAL_EXPIRED` stays the timed chain evaluation's (`verify_root_chain`), which the view does not call. S5's "the final root must be unexpired at tEval" is met: the fenced read refuses such a root at tEval, on this row.
      - **A catalog alone.** An index `Expired` or `StaleRevocation` by the clock alone is `ExistingOnly`: admitted, with no row.
      - **Rejected:** `ROOT.FINAL_EXPIRED` for the root's expiry, which would be a second evaluation of one instant with a second row (and X4T-a r1 call 6 rules that clock expiry is never an S5 row); `TRUST.NO_ADMITTED_TIME_CONTEXT`, which is F absent's only; and a new code or subject;
    - a root chain refusal: its S5 `ROOT.*` detail, naming the link. Only the chain evaluation produces these;
    - a signature or quorum failure, or a future payload: `PAYLOAD-NOT-ADMISSIBLE`;
    - plausibility or continuity: `CLOCK-EXCURSION-FORWARD`, with its S4 subject `beyond-horizon` or `in-session`;
    - a revoked component at admission: `CONTINUE-CORE-NOT-TRUSTED`, subject the revoked component (during an operation, X4 owns `TRUST.COMPONENT_REVOKED_DURING_OPERATION`);
    - a rollback below SC-TRUST's own retained floors: `CONFIG.CUSTODY_REFUSED`, subject `trust-rollback`;
    - an unsupported schema: `ROOT.SCHEMA_UNSUPPORTED` or `STATE.SCHEMA_UNSUPPORTED`;
    - I/O, a failed write-ahead confirmation, budget (including a root chain beyond `ChainBudget`, item 11): the host I/O and budget rows.
    - (r13, JRW RW-S5) **No new row.** The incomplete row no longer arises from the three states that item 7's completions finish: a leaf at a name the publication writes that is zero-length with its ACL omitted (RW-T1), or private and a strict prefix of its bytes (RW-T2); and a `may_create` parent directory left empty, `0700`, with its ACL omitted (RW-T3). Every other state keeps its row: N-T1 and N-T2b keep `installation-incomplete`, N-T2a keeps the host I/O row, and a budget failure keeps the budget row (JRW:460-462, :510-511). In the product these are `TrustRow::Incomplete`, `HostIo` and `Budget`, whose code and subject mapping is at `current_trust_admission.rs:89-114` at `d2c00a9`: `HOST.IO_FAILURE` at `:100`, `WORK.BUDGET_EXHAUSTED` at `:101`, and `installation-incomplete` at `:107`.

11. **Budget (lead decision; RF-5).**
    - **The closure is closed and counted (r4).** One view reads at most:
      - one head and one publication descriptor;
      - three heads (root, catalog, revocation), each a body, an envelope and an admission record: nine objects;
      - `history`, `clock.record`'s record and `timeEvidence`: three;
      - the event chain: `eventHead` and the current descriptor's `events`, at most `MAX_VIEW_EVENTS = 32`;
      - the `accepted.by` events outside that chain, at most one per role: six (r8, item 1);
      - the root chain N+1..M, and (r10) the accepted root N's body and envelope when N is not the head.

      That is at most 53 files plus the chain. `ChainBudget`'s stored bytes already count N's bytes as the chain's anchor, and the two files are inside the objects ceiling's margin, so no figure changes.
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
    - (r10) a recorded rotation (root 1 to root 2, then 1 to 3): admitted, with root 1 as the accepted root, `heads.root` as the signing root, and epoch `rootVersion` and the `rootVersion` floor at the final root's; a one-root store is unchanged; a closure whose last `rootChain` document is not `heads.root.document`, or whose `rootChain` is empty, refuses on the incomplete row; a first root whose own envelope misses its threshold after revoked keys are excluded refuses; a link failing continuity or possession refuses on its S5 row naming the link; a floor publication on a rotated store is followed by an admitted next read;
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
    - (r12) expiry at the fenced read, on stores whose stored roles are `Trusted` and whose expiry or staleness instant can be reached by a fenced read's tEval within S4's plausibility bound (item 13's X4T-0 knobs). In memory, through `admit_current_trust`:
      - **Staleness.** A tEval exactly at the list's `issuedAt` plus 90 days is admitted, `InstallGateRequiredForNewProcess`, with every role `trusted` (S4's strict `>`). One second later the read refuses `core:stale-revocation`, `CONTINUE-CORE-NOT-TRUSTED`.
      - **Root expiry.** One second before the signing root's `expiresAt` the read is admitted. At `expiresAt` it refuses `core:expired` (S4's `>=`), never `ROOT.FINAL_EXPIRED`. Both states true gives `core:expired`.
      - **Catalog expiry alone.** The read is admitted `ExistingOnly`. `role_states` shows TR-INDEX `expired`, and core, component and bundle `trusted`. `time()` still carries S4's three states, and the handoff clock is set.
      - **The mapping and the transition** are X4-F1's `a_rereads_clock_follows_x4b_item_4_and_the_role_machine` cases, now on the fenced read.
      - **Report-only** gives the same states, the same standing and the same refusal.
    - (r12) on native files, through X4T-b's `fenced_first_read` and X4B-b's `bootstrapping_first_read`:
      - **Write-ahead, then refusal.** A clocked refusal comes after a confirmed floor publication: the new `state.v1` has F = tEval, the owner holds one confirmation, and the stored `roles.*.state` are unchanged.
      - **The refusal is sticky.** A second fenced read with the wall clock set back below the boundary evaluates at tEval′ = F, refuses the same way, and writes nothing.
      - **Report-only** writes nothing and refuses the same way.
      - **Precedence.** A wall beyond the horizon refuses `beyond-horizon` and writes nothing, before any clock, even when the documents are expired at that wall.
    - (r12) through the real handoff (`operation_live_tests.rs`, or the handoff's own tests) with a scripted monitor clock whose first read's tEval is past the list's staleness:
      - the writer refuses at the lease-free point, as `TrustContinuation` with subject `core:stale-revocation` (request-rejected, exit 2, `EXTENSION.ADMISSION_REJECTED`);
      - the floor publication is confirmed;
      - no lease, X3b floor record, carrier or journal record exists, and no observer starts;
      - it is never `OBSERVER.FAIL_STOP` and never `required-files-changed`.
    - (r12) composition: after a fenced read admitted `ExistingOnly` (catalog expired), a reread at T = tEval returns the same clocked states and standing. A reread at a later T past staleness refuses `core:stale-revocation` from its own stored states (X4-F1).
    - (r12) existing tests whose behaviour must not move:
      - X4-F1's tests, among them `a_list_going_stale_during_the_operation_fail_stops_before_any_further_effect`, whose first read's tEval is two seconds before staleness;
      - X4B-a's and X4B-b's tests, where stored `Expired` and `StaleRevocation` states still refuse at the stored-state join, before time;
      - X4T-b's floor-publication tests, the `time_refusals_take_their_rows` rows, and the S4 reference fixtures.
    - (r13, JRW RW-S5; unit J4d) the completions, on scratch stores from X4T-0's generator (JRW:544-575):
      - **RW-C14, trust names.** C-TRUST and C-TDIR create no new name in any trust collection. After a killed C-TRUST, the structural name scan sees only canonical names. A leaf the admitted closure names is never a strict prefix at publication time, on either end of the read.
      - **RW-C15, trust directories.** C-TDIR completes each of the three `may_create` directories: the bucket, the predecessor directory, and `trust/objects` on an X4B-a acceptance. The fenced read before it ends as in r12: a view, or the clocked refusal. N-T2a (a symlink or a regular file at the name) keeps `HOST.IO_FAILURE`; N-T2b's opened directories keep `installation-incomplete`; a budget failure keeps `WORK.BUDGET_EXHAUSTED`. C-ACL never runs after a native open failure.
      - **RW-C18, completion before the clocked refusal.** Each of RW-T1, RW-T2 and RW-T3 is built in a store where S4 proposes a floor advance and `EV-CLOCK` at tEval refuses (`core:expired` or `core:stale-revocation`). The completion runs, the publication confirms and the owner advances. The read then returns r12's clocked refusal unchanged. No view, lease, X3b floor step, carrier start or later effect follows, and a second fenced read refuses again at tEval′ ≥ tEval. This mirrors `a_clocked_refusal_comes_after_its_confirmed_write_ahead_and_is_sticky` (`floor_publication_tests.rs:801-852` at `d2c00a9`).
      - **RW-C19, the clocked path's failures and its effect-free reads.** On the same route, N-T2a, N-T2b, N-T1 and an unreservable step each keep their own row and complete nothing. A refusal raised before time is admitted, and a report-only read, write nothing and complete nothing.
      - The shared C-ACL and C-SUFFIX predicates are J4a's tests (RW-C6, RW-C7; JRW:536-537, :662).

    There is no production seam: the fixture is `cfg(test)` in the security crate.

13. **Units.**
    - **X4T-0 (new in r4; test-only).** A signed accepted-store generator in the security crate, `cfg(test)`. It produces:
      - a real signed root, catalog and revocation, with envelopes, from test keys;
      - consistent admission records, `history`, the event chain, the clock record and time evidence;
      - roles in the requested states, each with `accepted.by` naming one of the current descriptor's events for that role, so X4T-a's check (item 1) passes;
      - the retained-phase capsule and `state.v1`.

      It drives every item 12 case. (r10) At product c2352ae it writes one-root chains only (`rootChain` holds the head's document, `rootVersion` 1); X4T-a3 extends it.

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
    - **X4T-a3 (r10; reader successor to X4T-a).** Item 3's two roots in `current_trust_admission::authenticate`: the accepted root read from the root admission's closure `rootChain`, `heads.root` as the signing root, and the closure join. Item 12's r10 tests. X4T-0 gains a test-only knob for a recorded rotation of n roots, each signed with the public test quorum seeds, with the head at the last. Depends on X4T-a2 and X4T-b. X4B-b depends on X4T-a3: its confirming admission must admit X4B-a's rotated default release.
      - **Rejected:** building X4T-a3's tests on X4B-a's producer or test release, which couples the reader to acceptance (as item 13 already rejects).
    - **X4T-b:** the write-ahead floor publication, the publication protocol it shares with X4B-a, the retained `state.v1` owner and its advance, and the handoff rollback comparison (items 7 and 8, r8). Depends on X4T-a2 and reuses 467's trust publication producers. X4T-a2 and X4T-b may be implemented and reviewed as one unit.
    - **First trust acceptance (new follow-up, X4B).** Until an installation's roles are `Trusted`, no operation can be admitted. The first acceptance of the core's embedded bootstrap payload (S4 step 2) as an authenticated installation trust event is a separate law and unit. It is not needed for the M2 exit matrix, which runs on synthetic signed trust stores, but it is needed before any real installation can commit. EXIT-PLAN gains it before X11.
    - **X4-F2 (r12; code successor to X4T-a, X4T-b and X4-F1).** It implements item 6's expiry at the fenced read, item 7's write-ahead before a clocked refusal, and items 9 and 10's rows, with item 12's r12 tests. It depends on X4-F1, integrated at product `15c0779`. It must land before J2b (M3-PLAN r9 P5-4) and is sized M plus one lead set (M3-PLAN r9).
      - **The changes.**
        - In `current_trust_admission::admit_bound`, the fenced branch clocks the stored states at tEval, with the same `clock_roles` and `standing_of` the reread uses, after S4's refusals.
        - A clocked refusal travels with the fenced read's pending write, and is never published as a view.
        - In `floor_publication::fenced_first_read`, the refusal is published at the point where r11 returns the view: after check 3, then after the write-ahead or the closing rechecks.
        - `live_observation`, the reread and every row and code are unchanged.
      - **X4T-0's test-only knobs (lead decision).** X4T-0's default store cannot reach an expiry at a fenced read. Its A is the list's issue time, so S4's plausibility bound stops W at the staleness boundary (the X4-F1 r1 request, judgment call 6). X4T-0 therefore gains three knobs, `cfg(test)` like X4T-a3's rotation knob:
        - a later issue time for one signed document, which raises A above the list's issue time;
        - the signing root's `expiresAt`;
        - the catalog's `expiresAt`.

        Each value lies inside S4's window for some lawful W. The stored roles stay `Trusted` because acceptance is judged earlier. **Rejected:** editing capsule or document bytes in a test, which breaks the closure's digests and signatures and so tests a different refusal.
      - **No file, no inventory.** If, as planned, the unit adds no file, it has no inventory successor and no design selection, as for X4-F1.
      - **The controls** are X4-F1's lanes:
        - `cargo fmt --all --check`;
        - the workspace build;
        - the crash-matrix and scenario-fixtures feature builds;
        - `cargo clippy` on the workspace and both feature lanes, with `-D warnings`;
        - the new and changed tests, single-threaded;
        - `cargo test --workspace` twice;
        - the crash-matrix feature test lane;
        - `verify_design.py`, and `check_package_edges.py --lane host`;
        - the crash-matrix checker's unittest;
        - release absence;
        - the X9 regression below.

        Every lane runs serially, with nothing else running, a private 0700 TMPDIR, `--locked --offline`, and the real home absent.
      - **The X9 regression (lead decision).** The method is X4-F1's.
        - **Source pins first.** The X9 harness sources are byte-identical at the unit's base and at X9-6's C, `3d2d5b5`, and the diff touches none of them. They are:
          - `tools/check_crash_matrix.py` and its test;
          - `crates/platform/src/crash_barrier.rs`;
          - storage's `commit_tests.rs` and host's `commit_matrix_tests.rs`;
          - both `required-runs.v1.json` files;
          - security's `crash_matrix_sites.rs`.

          At product main `218465f` they are, and `crates/security`, `storage`, `host` and `platform` are unchanged since `15c0779`. The checker's suite, X9-0's `no_manifest_enables_the_crash_matrix_feature`, and X9-1's `every_test_feature_site_is_on_the_pinned_list` pass.
        - **The selection.** A script computes it from the two required-runs files, and checks that the harness's own `OPENSIP_X9_ROWS` prefix rule selects exactly those rows. It takes the rows whose kill lies inside the code the unit changes or at the first durable point after it. In X2 item 7's lease-free order, the trust start comes first, then X3b's floor step (`operation_handoff::begin`).
          - **Storage, 54 rows, all F00.** 34 kill inside item 7's write-ahead (every `x4t.floor-publication` point: `dependency` and `pointer`, `create`, `write`, `file-barrier`, `rename` and `directory-barrier`, before and after). 20 kill at the `x3b.floor` points, the first durable points after the fenced read returns.
          - **Host: no row.** No host required run arms a point in, or right after, the fenced read. The host census alone is run, with a filter that matches no row, which the script asserts.
          - **Both censuses,** which pin every point of the writer's trace, the fenced read's included.
        - **The runs.** Two sets, one after the other, through X9-6's run-set entry `x9_6_matrix`: storage, then host, each with its census.
        - **The comparison.** X4-F1's `compare.py` fields (verdict, `postState.normalizedSha256`, the ladder, `notApplicable`, every child's role, ordinal, exit, `lastHeld`, outcome and trace; whether `timingGuard` is present), against the accepted X9-6 evidence. The expected result is identical, with 0 differences:
          - storage census: 259 points, trace 1379 records, `e9add21e…`, kill set 321;
          - host census: 218 points, trace 1195 records, `93d0922a…`, kill set 271.

          X4-F1 was integrated without rerunning these 54 rows. So if any difference appears, the same selection is run on the unit's base without the diff, to attribute it.
        - **Why these rows.** Every committing child runs the fenced read, and the selection covers the code the unit changes. X9 r16 item 3's scripted wall stays inside every validity window of the matrix's stores: the nearest boundary is the list's staleness, 2026-12-30T00:00:00Z, and the scripted wall is 2026-10-04T00:00:00Z plus 3600 s per child ordinal. So no fenced read in a required run reaches a clocked state, the clocked states equal the stored ones, and no outcome, crash point, scope, read, write or clock sample moves.
        - **Excluded:** X4-F1's 43 tick-armed rows and its checkpoint kills. The reread, the handoff clock, the epoch, the floors and the closure that X4's S6 predicate reads are all unchanged.
        - **No X9 row moves and no row is added (lead decision).** A kill inside a write-ahead that precedes a refusal leaves the crash states of the 34 existing rows. The next fenced read finds the old pointer, and refuses again at its own tEval, or the new one, and refuses at F. **Rejected:** a new matrix row with a scripted wall past a boundary. It needs a new matrix store and a new row family, to pin crash states the existing rows already pin.
    - **J4d (r13; J-RW r4's unit, JRW:665).** It implements item 7's two completions: C-TRUST at `write_dependency` (RW-T1, RW-T2) and C-TDIR at `parent_dir` (RW-T3), with the X4B-a acceptance-path directories, on both ends of the fenced read. It adds item 12's r13 tests. It depends on this revision and on J4a, which owns the shared C-ACL and C-SUFFIX primitives.
      - **Scope names.** Its completion effects run in the scope `x4t.floor-publication.dependency.repair/…` (JRW:643).
      - **The matrix.** Its X9 rows (RW-D1, RW-K8 to RW-K10, RW-N9 and RW-N12) are J-RW's section of X9 r17, transcribed by J4e (JRW item 10). X4-F2's regression subset above is unchanged.

## Forbidden substitutes

The floor write or fenced admission under a project lease; a retry inside X4T's reread; comparing the live `state.v1` with the start capture after the fence is released; storing any digest but `Effective::digest()` as `permissionPolicyDigest`; a chain budget beyond 16 links or 16 MiB; a view built from the P0 capsule, the embedded root list or stored acceptance flags without reverifying signatures; a census in place of the head's closure; a second fenced capture of `state.v1`; a directory scan to find trust records; time re-admitted on an unfenced reread; a decision at tEval without the write-ahead floor; any write other than item 7's floor publication; a floor write without the fence; replacing the retained `state.v1` owner while the fence is held, except through a confirmed publication; taking the fence on a reread; admitting a lower counter or floor; a truncated or partially read view; (r8) an `accepted.by` outside the loaded chain accepted without loading it, or following that event's `previous`; a rollback check that reads beyond the closure, probes a successor bucket or uses the journal carrier floor; advancing the retained owner from the written bytes without the reopen; a new public code (item 10 publishes the two unregistered continuation reasons under the registered detail until the owner decides); (r10) `heads.root` as the accepted root of a closure whose `rootChain` has more than one root, an accepted root taken from anywhere but the closure's first `rootChain` document, or a closure join by root value alone; (r12) a fenced view whose role states or standing were not clocked at tEval; a fenced clock at any instant but tEval; a clocked refusal published before item 7's write-ahead, or a write-ahead skipped because the read will refuse; an `EV-CLOCK` recorded in the trust store, or a role state rewritten by any X4T write; a reread clocked from the start view's clocked states rather than its own stored states; `ROOT.FINAL_EXPIRED`, `TRUST.NO_ADMITTED_TIME_CONTEXT`, or any new code or subject, for a clocked expiry; a refusal on a catalog expiry alone; (r13) a completion other than item 7's two, C-TRUST at a name this publication writes and C-TDIR at a `may_create` parent; a completion that deletes, truncates, renames away, rewrites an existing byte, uses a temporary name in a trust collection, changes a mode bit or appends any ACE but the one zero-rights owner allow; C-ACL after a native open failure, or at a parent `may_create` does not permit; completing a leaf whose bytes are neither exactly equal to nor a strict prefix of the publication's bytes, or visiting an unreferenced leaf; on the clocked path, completing anything but the mandatory write-ahead publication on the authenticated closure and pending write, or returning anything but r12's unchanged clocked refusal after it; a completion on a read refused before time is admitted, or on a report-only read; a successful-view gate that leaves a repairable, OpenSIP-owned leaf or directory blocking the mandatory write-ahead. P-ACL's one bounded emptiness check at the parent step is not a directory scan to find trust records (LD13-1).

## Not claimed

A global permission policy file under I and its custody owner (a later unit; item 5); the first trust acceptance (X4B); trust import, recovery challenge and recovery import (S4.5); X4's operation grant, observer, checkpoint and S6 predicate; rollback of effects; any doctor trust report; (r8) detecting a whole-file restore of an older, self-consistent `state.v1` and its closure, which is item 7's stated limit; Linux; a qualified measured macOS 27 profile row. On this BASELINE-ATTESTED host a real installation never reaches X4T, because reads refuse at `/` without a premise.

(r12) Also not claimed:
- **Expiry detected between reads.** A process that stops between reads is caught by S6's 10 s bound at its next read, which then clocks at its own instant (X4-F1).
- **Native scheduling of the 5 s and 10 s bounds (L3).**
- **Recording `EV-CLOCK` transitions in the trust store.** That is a later trust-update or doctor unit's.
- **F9's fixture date refresh.** r12 does not move F9's date. For X4T-0's self-constructed stores (L 2026-10-02), a fenced read on the native clock now refuses `core:stale-revocation` from 2026-12-30T00:00:01Z; r11 admitted it until 2026-12-31T00:00:00Z. That is the second X4-F1 already moved rereads to, and the default (X4B-produced) stores refuse `beyond-horizon` from that second anyway. F9's 2026-12-01 deadline (M3-PLAN r9 P5-5) covers both.

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

## r10 note: the matching X4B correction

X4B r5's text needs these changes to match r10. They are X4B's own amendment, not this law's:
1. **Units.** Item 11's X4B-b depends also on X4T-a3.
2. **Tests.** Item 10's first case and round trip run on the default release, which rotates root 1 to root 2. X4B-a's `a_multi_link_root_chain_is_authenticated_and_recorded_in_full` pins the confirming admission's `FirstIdentity` refusal. Once X4T-a3 is on main, that test expects the confirming admission to admit, with epoch `rootVersion` 2.
3. **What X4B writes is unchanged.** `heads.root` is the final root, `clock.record.rootVersion` is its version, and the closure's `rootChain` lists the whole chain with the final root last, exactly as X4B-a writes it.

## r12 note: other laws and the record

r12 needs no other law's amendment:
1. **X4 r7.** Item 8's "no admitted current trust" row already gives X4T's own rows at the lease-free point. Its r5 note already says `Continuation::Refuse` stays X4T's admission refusal there, and that `ExistingOnly` admits every M2 writer effect. The S6 predicate reads the start view's epoch, floors and closure, none of which r12 changes.
2. **X4B r5.** Item 4's mapping is the one r12 applies. Item 4 says the confirming admission "reads the stored `roles.*.state` and runs `continuation`", and that stays true: r12 adds a clock at the confirming admission's tEval, which equals the acceptance's. That tEval is max(F, W, A), with F the acceptance's tEval, the same clock sample and the same documents. So it gives exactly the states the acceptance recorded, and changes no X4B outcome. A store that the acceptance recorded as `Expired` or `StaleRevocation` still refuses at the stored-state join, before time.
3. **X9 r16.** No row, census or kill set moves (item 13). The regression subset is item 13's.

**Record items, for the lead at integration (not law):**
- M2-COMPLETE §5 row 23 and M3-PLAN's carry-in row for X4-F2 move to "integrated" once X4-F2 lands;
- EXIT-PLAN's "Follow-ups found by X4-F1" X4-F2 bullet is closed then.

## r13 note: other laws and the record

1. **X4B r6.** RW-S5's other part, a record note in X4B r6 shared with J1's S6 (JRW:683), has landed. Codex accepted X4B r6 on 2026-10-04 (`docs/implementation/m2/trust-bootstrap-x4b/PROPOSAL-r6.md`, sha256 `c8c54154…`; `reviews/codex-j1-successors-s2-s6-r1`). Its items 5 and 6 record that the shared protocol completes such a leaf and such a directory, and deletes nothing (X4B r6:151, :157-161). r13 does not repeat that note. X4B decides nothing: the rule is item 7's.
2. **X4 r7.** No amendment. The completions run inside item 7's write-ahead, before the view or the clocked refusal is returned, so the start epoch, the floors and the closure that X4's S6 predicate reads are r12's.
3. **X9.** No amendment from r13. J-RW's `RW-` section of X9 r17 carries the rows for these states, as its successor RW-S6, a separate record.
4. **465.** Item 5's rule is the precedent C-ACL extends. 465 itself does not change (JRW:689).
