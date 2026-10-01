# Native current-trust admission — proposal X4T r1

2026-09-30. Claude Opus 5.5, implementation lead. Law for unit X4T, the prerequisite that X4 r2 item 1 (RF-1) created. It is written under the security contract's S4 (trust time), S5 (root chains) and S6 (live revocation), owner.md §5 and §7, and laws 463 (core, release and revocation), 466/467 (the P0 trust files), 458c r6, X1 r1, X2 r3, X3a r3, X3b r1 and X4 r2. Items 1, 2, 3, 6, 7, 8, 9 and 11 contain lead decisions made under the owner's standing direction of 2026-09-30 to proceed on the lead's recommendation; each names the alternative it rejects. Not code. It reads, authenticates and admits the installation's current trust; the only write it defines is the S4 write-ahead floor of item 7.

## Problem

At f7acb6d no code produces an authenticated view of the installation's current trust:
- `trust/native_current.rs` captures `state.v1` and its P2-local joins only as a provisional, supplied-path image ("does not select I/S … or grant authority");
- `captured_capsule_clock.rs` is "a captured retained capsule IMAGE, not admission of the live state.v1 head";
- the ordinary modules (`trust_ordinary_roots`, `trust_ordinary_bundle`, `trust_policy`, `trust_time`, `admitted_revocations`, `role_machine`) authenticate or evaluate only premises their caller supplies, and `trust_time::evaluate_retained_ordinary` "proposes writes only".

X4's operation guard, observer and authority checkpoint all need one admitted current-trust view, `AdmittedCurrentTrust`, produced from the installation's own trust store. X4T composes the existing owners into that admission. It adds no trust semantics of its own.

## Decisions

1. **What an admitted current-trust view is (lead decision).** `AdmittedCurrentTrust` is private, not Clone and not serializable, and is borrowed from the session or operation that produced it. It holds:
   - **The head:** the installation's `trust/stores/S/state.v1` capsule for X3a's admitted S, decoded, capped, and joined to X3a's `C.store`.
   - **The dependency closure:** every record the capsule names (its publication descriptor, the role member records `TR-BUNDLE`, `TR-COMPONENT`, `TR-CORE`, `TR-INDEX`, `TR-PROFILE`, `TR-REPAIR`, and the documents those roles accept: the accepted root, the accepted revocation, the accepted permission policy), each at its exact locator, decoded, capped and admitted by its existing shape and record owners (`trust_record_reader`, `trust_record_shapes`, `admitted_trust_records`, `retained_trust_graph`).
   - **The authentication result** of item 3, the revocation set of item 4 and the effective policy of item 5.
   - **The time admission** of item 6: tEval, F, L and the anchor, after item 7's write-ahead if one was needed.
   - **The S6 trust epoch** `{rootVersion, indexSnapshotVersion, revocationVersion, permissionPolicyDigest}` derived from the above, plus the role states from `role_machine`.

   It grants nothing by itself. It is the input X4's guard, observer and checkpoint consume, and the only one they may consume.

   - **Not admitted.** The view refuses (item 10) unless every role X4 requires is `Trusted` under the role machine. A creator-only installation (P0: every role `Unbootstrapped`) is not admitted. The embedded release's root (463) authenticates the release, never the installation's current trust; it is not a substitute for an accepted installation root.
   - **Rejected:** admitting a view from the P0 capsule plus the embedded root list. It would let a freshly created installation run operations on trust it never accepted, which X4 r2 forbids.

2. **The read set and its order (lead decision).** One view reads, in this order, each step charged before it runs:
   1. `state.v1`, by name through the retained `trust/stores/S` handle (item 8 says which capture);
   2. the publication descriptor the capsule names;
   3. each role member record the capsule names;
   4. each accepted document those records name: root, revocation, policy;
   5. `state.v1` again, by name, to confirm it is the same file with the same full sample.

   Dependencies come from the immutable collections under `trust/` (`records`, `publications`, `stores/S/events`), each opened through a retained directory handle with an exact-length cap at its owner's bound (at most 4 MiB, `retained_metadata_index::CAP`). The closure is closed: a reference outside it, a missing member, a duplicate disagreement or a cycle refuses as an incomplete installation. There is no directory scan; every file is reached through a reference.

   **Rejected:** a census of every trust record (`native_census`). The current view needs only the closure its head names; the census is the doctor's and recovery's.

3. **Authentication (lead decision).**
   - **Which roots.** The view is authenticated from the installation's accepted root, the document the `TR-CORE`/root role accepts, through `trust_ordinary_roots::authenticate_shared`. A root chain N+1..M recorded in the closure is evaluated link by link under S5 (continuity and possession thresholds, revoked keys excluded, final root unexpired at tEval).
   - **The embedded release's role.** 463 authenticates the running core against the embedded release root. X4T requires that the installation's accepted core closure equals the running core's, as X3a's endpoint join already checks, and that the embedded release's revocation (463) has not revoked it. The embedded root never stands in for the installation's root.
   - **Signatures.** Every accepted document's envelope is reverified against the accepted root's keys at their thresholds, with revoked keys excluded, by the existing envelope and quorum owners. A record whose envelope does not verify refuses; nothing is "accepted because it is in the store".
   - **Rejected:** trusting stored acceptance flags without reverifying signatures. A store rewritten by a local attacker would otherwise grant trust.

4. **Revocation admission.** The accepted revocation document is verified by `admitted_revocations::verify_revocation` against the accepted root, with the keys revoked before it. Its version is the epoch's `revocationVersion`. A revoked component in the closure (the running core, the release, the signing keys, the namespace's catalog snapshot) refuses at admission. A lower revocation version than the floor records is never accepted (item 7).

5. **Policy and grant admission.** The accepted permission policy is merged by `trust_policy::merge` in the installation context. Its canonical digest is the epoch's `permissionPolicyDigest`. X4T admits the effective policy; it does not decide whether a given operation is granted. That is X4's operation grant, which reads the effective policy from the view.

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

     The writer reuses 467's existing trust publication producers. It never changes a counter, a role state or an accepted document.
   - **Retained evidence advances.** The session and operation retain `state.v1` (468 item 3, X3a item 2). Only this confirmed publication may replace that retained owner, exactly as X2 r3's registry rule: the confirmed new `state.v1` becomes the retained file and its full sample, and every later recheck compares against it. Any other change still fails as `required-files-changed`.
   - **Rollback.** A capsule whose F, L, root version, revocation version or index snapshot version is lower than the carrier high-water floor (X3b item 2's `I/trust/carrier-floors/N.v1`, which records the trust epoch at the last operation boundary) refuses as a rollback. A lower counter never revokes (S6); it refuses admission.
   - **Report-only.** A read session (458c, doctor) runs the same evaluation and returns the proposed writes without performing them (S4's report-only mode).
   - **Rejected:** admitting a decision at tEval without the write-ahead. It lets a later evaluation run earlier than an earlier one, which S4 forbids.

8. **Reuse of the 458c and X3a capture.** The fenced first read does not read `state.v1` again. It takes the decoded, capped capsule and full sample that X3a item 2 already retains for the session, and the retained `trust/stores/S` handle. The dependency closure is new reading, because no earlier unit reads it. Observer rereads (item 9) do read `state.v1` again by name; that is their purpose.

   **Rejected:** a second fenced capture of `state.v1`. It would duplicate X3a's read and give two owners for one file.

9. **The fenced versus unfenced reread protocol (lead decision).**
   - **Fenced first read.** It runs inside X2 r3's handoff (item 7a), with the installation fence held, as X4 r2 item 2 orders: the monitor's first timed read. It performs items 2 to 7, including any write-ahead, and the view becomes the operation's start epoch.
   - **Unfenced observer reread.** It runs on X4's observer ticks and at X4's checkpoint, without the fence (S7's lock order forbids level 0 under level 1). It reads only through handles retained under the fence: `trust/stores/S` and the immutable collection directories. It performs items 2 to 5 (head, closure, authentication, revocation, policy), with no time re-admission (item 6) and no write (item 7).
     - **Consistency.** It opens `state.v1` by name at the start and again at the end, and requires the same file and full sample. If the pointer changed in between, it retries once from the new head; a second mixed read stops the operation (X4 r2 item RF-3).
     - **A later pointer.** A newer `state.v1` published by another writer is admitted like any other view; X4's S6 predicate decides whether it revokes, is drift, or is a rollback.
   - **Rejected:** taking the fence for rereads. It would invert S7's lock order and deadlock with the journal append lock.

10. **Refusal rows (no new codes).** Every refusal maps through 468c's `InstallationTermination` to an existing row; where S12 or the public detail registry fixes a class for a detail, that class prevails:
    - missing, undecodable, oversize or misbound trust records, an incomplete closure, a pointer that changes twice: the incomplete row (`CONFIG.CUSTODY_REFUSED`, subject `installation-incomplete`), and the `installation-incomplete:current-store` doctor subject for `state.v1` (X3a item 5);
    - a role not `Trusted`: `Unbootstrapped` → `TRUST.NO_ADMITTED_TIME_CONTEXT` (S4 step 2: no accepted bootstrap); `Revoked`, `StaleRevocation`, `QuorumLost`, `Recovery` → `CONTINUE-CORE-NOT-TRUSTED`, subject the role state; `Expired` → the S5 row the chain evaluation produces (`ROOT.EXPIRED_NO_CHAIN`, `ROOT.FINAL_EXPIRED`, and so on);
    - a root chain refusal: its S5 `ROOT.*` detail, naming the link;
    - a signature or quorum failure, or a future payload: `PAYLOAD-NOT-ADMISSIBLE`;
    - plausibility: `CLOCK-EXCURSION-FORWARD`;
    - a revoked component at admission: `CONTINUE-CORE-NOT-TRUSTED`, subject the revoked component (during an operation, X4 owns `TRUST.COMPONENT_REVOKED_DURING_OPERATION`);
    - a rollback below the carrier floor: `CONFIG.CUSTODY_REFUSED`, subject `trust-rollback`;
    - an unsupported schema: `ROOT.SCHEMA_UNSUPPORTED` or `STATE.SCHEMA_UNSUPPORTED`;
    - I/O, a failed write-ahead confirmation, budget: the host I/O and budget rows.

11. **Budget (lead decision).** One view's closed read set is bounded by the closure of item 2: one head, one descriptor, six role records, and at most three accepted documents per role chain, with a root chain bounded by its own counter range. X4T publishes a fixed ceiling per view, `TRUST_VIEW_COST`:
    - objects ≤ 1024, edges ≤ 8192, bytes ≤ 32 MiB.

    X4T-a measures the real cost of one view on its largest synthetic store (the full role set, a five-link root chain, a revocation and a policy), pins the measurement in a test, and pins that the measurement is at most the ceiling. A view that would exceed the ceiling refuses on the budget row; it is never truncated.
    - **Where it is charged.** The fenced first read charges the gate ledger while the fence is held (X4 r2 item 8); the write-ahead reserves its post-publication confirmation before its first effect. An unfenced reread charges X4's per-observation ledger, which X4 sizes at 2 × `TRUST_VIEW_COST` (16384 edges, 64 MiB), well inside the owner's caps.
    - **Rejected:** an unbounded "measured later" figure. X4 needs a fixed number to size its ledger now.

12. **Tests.** On scratch installations with synthetic signed trust (the 462 signed test trees and the existing trust signing fixtures), built by a test-only fixture in the security crate that writes an accepted trust store (every role `Trusted`, accepted root, revocation and policy) after the P0 publication. Cases:
    - a P0 creator-only installation refuses `TRUST.NO_ADMITTED_TIME_CONTEXT`;
    - an admitted view, with its epoch;
    - each role state's row;
    - a bad signature, a wrong-threshold quorum, a future payload;
    - a root chain through expired intermediates, and an expired final root;
    - a revoked core closure;
    - a rollback below the carrier floor;
    - time: a floor advance is written ahead and the retained `state.v1` owner advances; a W beyond A + 90 d writes nothing; report-only returns proposed writes and writes nothing;
    - rereads: a pointer change mid-read retries once; a second change stops; a newer pointer with an unrelated revocation is admitted as drift input;
    - budget: the measured cost on the largest store, and the ceiling refusal.

    There is no production seam: the fixture is `cfg(test)` in the security crate.

13. **Units.**
    - **X4T-a:** the read-only admission: items 1 to 6, 8, 9 (both reads), 10 and 11, with report-only time. Depends on X3a-1.
    - **X4T-b:** the write-ahead floor publication and the retained `state.v1` advance (item 7). Depends on X4T-a and reuses 467's trust publication producers.
    - **First trust acceptance (new follow-up, X4B).** Until an installation's roles are `Trusted`, no operation can be admitted. The first acceptance of the core's embedded bootstrap payload (S4 step 2) as an authenticated installation trust event is a separate law and unit. It is not needed for the M2 exit matrix, which runs on synthetic signed trust stores, but it is needed before any real installation can commit. EXIT-PLAN gains it before X11.

## Forbidden substitutes

A view built from the P0 capsule, the embedded root list or stored acceptance flags without reverifying signatures; a census in place of the head's closure; a second fenced capture of `state.v1`; a directory scan to find trust records; time re-admitted on an unfenced reread; a decision at tEval without the write-ahead floor; any write other than item 7's floor publication; a floor write without the fence; replacing the retained `state.v1` owner except through a confirmed publication; taking the fence on a reread; admitting a lower counter or floor; a truncated or partially read view; a new public code.

## Not claimed

The first trust acceptance (X4B); trust import, recovery challenge and recovery import (S4.5); X4's operation grant, observer, checkpoint and S6 predicate; rollback of effects; any doctor trust report; Linux; a qualified measured macOS 27 profile row. On this BASELINE-ATTESTED host a real installation never reaches X4T, because reads refuse at `/` without a premise.
