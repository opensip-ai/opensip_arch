# First trust acceptance from the embedded bootstrap payload — proposal X4B r2

2026-10-01. Claude Opus 5.5, implementation lead. Law for unit X4B of `EXIT-PLAN.md`, created by X4T r4 to r7 (item 13). It is written under:
- the security contract's S4 (trust time, step 2 "fresh install") and S4.5, S5 and S6;
- laws 463 (core, release and the embedded release values) and 466/467 (P0 and its producers);
- the accepted laws X1 r1, X2 r6, X3a r5, X4 r7 and X4T (r7 under review);
- the role machine `trust/role_machine.rs` at product fc7dce7.

Items 1 to 7 contain lead decisions made under the owner's standing direction to proceed on the lead's recommendation; each names the alternative it rejects. Not code. Library only: no CLI command is wired.

r2 answers Grok X4B r1:
- **RF-1.** Acceptance no longer sits inside `admit_ordinary_writer` or anywhere near X2e's lease. It runs at X4T's fenced first read: X3a's store is retained, R is fixed, the fence is held, and no project lease has been taken. The fenced admission then runs again on the confirmed retained `state.v1`, still before any lease. Items 1 and 11 are corrected.
- **RF-2.** Item 4 now names the `role_machine::decide` event sequence from `Unbootstrapped` for an expired, stale or revoked document. Every accepted event is recorded, and the test expectations follow the states that sequence stores. Items 9 and 10 are corrected to match.

r1 bytes are preserved in PROPOSAL-r1.md.

## Problem

A creator-only installation holds the P0 capsule:
- `heads` and `history` are null;
- the clock phase is unevaluated;
- every role is `ST-UNBOOTSTRAPPED`.

X4T admits it only as "F absent" (`TRUST.NO_ADMITTED_TIME_CONTEXT`, S4 step 2). So no operation can ever be admitted on a real installation.

S4 step 2 names the remedy: the core's embedded bootstrap payload. Law 463's release embedding already carries a bootstrap path in `EmbeddedCoreRelease` (`core_release_embedding.rs`), which is absent in development builds.

At 7e676a9, nothing in the product produces the retained-phase records:
- root and metadata admissions;
- revocation history;
- role events and changes;
- publication events;
- time evidence and the signed time source;
- the retained capsule.

X4T-0 builds them only under `cfg(test)`. X4B is their production producer.

## Decisions

1. **Trigger: X4T's fenced first read, lazily (lead decision; RF-1).** Acceptance runs at exactly the point where X4T item 9 runs its fenced first read. That is X2 item 7's ordering note:
   - X1's `admit_ordinary_writer` has already returned the `OrdinaryWriteAdmission`, with the installation fence held;
   - X3a has retained `trust/stores/S` and its `state.v1`, with the decoded, capped capsule and its full sample;
   - the current registry owner R is fixed;
   - no project lock is held, and X2 item 7 has taken no lease.

   The sequence is:
   1. **X4T's fenced first read** runs on X3a's retained capsule. If it returns a view or any refusal other than F absent (`TRUST.NO_ADMITTED_TIME_CONTEXT`, S4 step 2), X4B does nothing.
   2. **On F absent, and only then,** X4B runs items 2 to 6 under the same fence hold. The confirmed new `state.v1` replaces the retained owner (item 5).
   3. **The fenced admission runs again,** once, on that confirmed retained `state.v1` and its capsule, still under the fence and before any lease. It performs X4T items 2 to 7 as usual. Its view becomes the operation's start epoch, and X4's `FreshnessMonitor` is created immediately before it, so the monitor's clock brackets the admission that yields the view (X4T item 9). If this second read returns F absent again, that is the existing host invariant row (operational-failed, 4, `SYSTEM.OUTCOME.ILLEGAL_STATE`, `host-invariant`, detail `HOST.INVARIANT_VIOLATED`, as X3d item 9 uses it). No third read runs.
   4. **X3b's floor step and X2 item 7** then run as already ordered. X2e (item 7a) receives the resulting view and publishes no trust state.

   - **Read-only commands never bootstrap.** Doctor and query keep reporting F absent (458c, report-only).
   - **Why this point.** S7 writes trust state only under the fence and never under a lease. `admit_ordinary_writer` grants no store, no trust admission and no project admission, so the store acceptance writes to is not yet retained there.
   - **Rejected:**
     - inside `admit_ordinary_writer` (RF-1): no store is retained there;
     - at X2e or under any lease: S7, and X4T item 9;
     - the creator path: 468c's `route` drops `InitialCore` before the gate (468 r5 item 1), and X3a r5 gives a creator invocation no store;
     - a separate `trust bootstrap` command: it would add a mandatory user step with nothing to decide.
2. **What is accepted (lead decision).** Exactly the payload law 463 embeds, read from the running core's tree through the `InitialCore` that X1's write receipt retains.
   - **Authentication:** it is authenticated from the embedded root binding (schema, version, digest), against the signed root it carries, and through S5's chain within `ChainBudget{16 links, 16 MiB}`. Every signature is re-verified.
   - **No other source:** no network, import file or caller-supplied payload is consulted. A development build has no embedded bootstrap and refuses earlier, at `CORE.NO_EMBEDDED_RELEASE`.
   - **Rejected:** importing an ordinary payload here. That is S4.5 and later import units.
3. **Time (S4 step 2, exactly).**
   - A = max(the payload's root issue time, the newest verified document issue time), since L is absent.
   - An issue time later than W + 24 h refuses as `PAYLOAD-NOT-ADMISSIBLE`.
   - W > A + 90 d refuses as `CLOCK-EXCURSION-FORWARD` (`beyond-horizon`) and writes nothing.
   - Otherwise tEval = max(W, A); F := tEval; L := A; and the anchor := (B, M, W) from the same clock sample X4T uses.
   - Expiry is evaluated from the presented documents at tEval, never set to false.
   - The time evidence record carries this evaluation as its proof, and the signed time source carries the payload's own signer.
4. **Role transitions: the `decide` event sequence (RF-2).** Each role starts at `Unbootstrapped`. For each role whose document the payload carries, X4B dispatches the following events through `role_machine::decide` (product fc7dce7), in this order, and stops at the first refusal.
   1. **`PresentOrdinary { entry }`.** It runs with the entry observation for that role's document: authenticated, active and admissible under S5, judged at tEval. Only an admissible entry is accepted, which stores `Trusted`. This event takes no expiry, staleness or revocation input. An inactive or rejected entry is refused, and the role stays `Unbootstrapped` with no event recorded.
   2. **`Clock { expired, stale_revocation }`.** It is dispatched only when, at tEval, the document is expired or its revocation data is stale. From `Trusted` it stores `Expired` if `expired`, otherwise `StaleRevocation`. If both are true, `Expired` wins, as `decide` orders them. It is recorded as `EV-CLOCK`.
   3. **`Revoke { newer_and_byte_valid: true }`.** It is dispatched only when the payload's own verified revocation document, newer than any accepted for the role, revokes that role's document or key. From any state but `Unbootstrapped` it stores `Revoked`. It is recorded as `EV-REVOKE`, with `conditionEvidence.revokedBy` naming it.

   Every event `decide` accepts is recorded:
   - as a `TrustEventV1` with its `RoleChangeV1` (before and after) and `PublicationEventV1`;
   - chained on the role's history in dispatch order;
   - with the role's `accepted.by` naming that role's `EV-PRESENT-PAYLOAD` event, the event that accepted the document.

   These are the record shapes X4T-0's `accepted_store_fixture.rs` builds for the same states. No event is dispatched that `decide` would accept as a no-op: `Clock` is skipped when both inputs are false, and `Revoke` when nothing is revoked.
   - **The resulting stored states:**
     - fresh, unexpired and unrevoked at tEval: the single `PresentOrdinary`, ending at `ST-TRUSTED`;
     - expired: `PresentOrdinary` then `Clock`, ending at `ST-EXPIRED`;
     - stale revocation: `PresentOrdinary` then `Clock`, ending at `ST-STALE-REVOCATION`;
     - revoked: `PresentOrdinary` then `Revoke`, ending at `ST-REVOKED`;
     - expired and revoked: all three events, ending at `ST-REVOKED`.
   - **Roles the payload doesn't carry** stay `Unbootstrapped`, with no event recorded.
   - **Continuation.** X4T's re-admission (item 1 step 3) reads the stored `roles.*.state` and runs `continuation`. If core, index or component isn't continuable, it refuses on its continuation row, after the acceptance is durably recorded. The record is honest even when the result is unusable.
   - **Rejected:**
     - writing `Expired`, `StaleRevocation` or `Revoked` directly with one `PresentOrdinary` (RF-2): `decide` stores `Trusted` for that event;
     - dispatching `Clock` or `Revoke` from `Unbootstrapped`: `decide` stores `Unbootstrapped` or refuses;
     - `QuorumObserve` at acceptance: quorum loss needs a later observation that the payload doesn't supply.
5. **The writes: one publication, atomic at the pointer (lead decision).**
   - **The records:** under the held fence, X4B writes the payload closure and every record of item 4, plus:
     - `RootAdmissionNodeV1`, and the `MetadataAdmissionNodeV1`s for the catalog and revocation;
     - `RevocationHistoryNodeV1` (the list form, as X4T-0's shape);
     - `TimeEvidenceV1` and `SignedTimeSourceV1`;
     - the operation input;
     - the revision-2 `PublicationDescriptorV1` on the P0 predecessor;
     - the retained-phase `TrustCapsuleV1`.
   - **How they are written:** each record is canonically encoded and admitted by its closed shape before it is written. Each file goes through 467's private-file producer with its file barrier. The `state.v1` pointer goes last, by atomic replacement (exclusive temporary name, file barrier, rename, directory barrier, reopen and confirm), exactly as X4T item 7's floor write-ahead does.
   - **Retained evidence:** the confirmed new `state.v1` becomes X3a's retained owner while the fence is held, as X4T item 7 and X2's registry rule require. The decoded, capped capsule comes from the confirming reopen, not from X4B's own memory. Item 1 step 3's re-admission reads that retained owner.
   - **Rejected:** writing records in place, or a pointer before its dependencies.
6. **Crash states.**
   - **Before the pointer:** the store still points at P0. Any written records are unreferenced and harmless. The next first write runs X4B again with fresh names; records are content-addressed, so equal bytes are equal names.
   - **After a confirmed pointer:** accepted.
   - **An uncertain pointer replacement:** it refuses on the host I/O row and runs nothing further. The next invocation's X4T read decides from the pointer it finds.
   - **No deletion.** Nothing is ever deleted (owner §6).
7. **Rows (existing only).**
   - no embedded bootstrap: `CORE.NO_EMBEDDED_RELEASE`;
   - authentication: the `ROOT.*` and `PAYLOAD-NOT-ADMISSIBLE` rows X4T item 10 fixes;
   - time: `PAYLOAD-NOT-ADMISSIBLE` or `CLOCK-EXCURSION-FORWARD`;
   - a revoked core at acceptance: the continuation row;
   - I/O and an uncertain publication: host I/O;
   - budget: `WORK.BUDGET_EXHAUSTED`;
   - a changed retained file: `required-files-changed`.

   **Rejected:** a new bootstrap-specific code.
8. **Budget.** It is charged to the gate ledger at X4T's fenced first read, as X4T-b's write-ahead is. That covers the F-absent read, the acceptance and the one re-admission. Each record is charged before it's written, every post-effect confirmation is reserved first, and the root chain is within `ChainBudget`.
9. **Relation to X4T-0.** Once X4B's producer exists, X4T-0's test-only constructor is replaced by calls to it, wherever X4B can produce the requested role states: `Trusted`, `Expired`, `StaleRevocation` and `Revoked`, through item 4's sequences. X4T-0 keeps only the states acceptance can't reach, such as `QuorumLost` and `Recovery`, as test-only constructions. Its source pin stays.
10. **Tests.**
    - **Scratch installations,** with a test-only embedded release whose bootstrap payload is signed with the public quorum62 seeds (462/463's test trees). Covered cases:
      - P0 → accepted, after which X4T's re-admission admits the result with every carried, fresh role `ST-TRUSTED` from a single `EV-PRESENT-PAYLOAD`;
      - the future-dated payload, beyond-horizon and fresh-install time rules;
      - an expired document at acceptance: `EV-PRESENT-PAYLOAD` then `EV-CLOCK`, stored `ST-EXPIRED`, with `accepted.by` naming the first event. The core expired gives X4T's continuation row;
      - a stale revocation: `ST-STALE-REVOCATION`. A revoked document: `EV-PRESENT-PAYLOAD` then `EV-REVOKE`, stored `ST-REVOKED`, with `revokedBy` set. Expired and revoked: three events, stored `ST-REVOKED`;
      - an inactive or rejected entry: the role stays `ST-UNBOOTSTRAPPED` with no event;
      - ordering: acceptance runs only at the fenced first read and only on F absent, never under a lease; the re-admission runs once; a second F absent is the host invariant row;
      - a crash before the pointer, then a rerun;
      - an uncertain pointer replacement;
      - a dev build at `CORE.NO_EMBEDDED_RELEASE`;
      - read-only commands never bootstrapping.
    - **Round trip:** X4T-a's loaders (`capture_p2`, `bind`, `bind_retained_head`, `Budget::load` and the `accepted.by` check) accept what X4B writes.
11. **Units.**
    - **X4B-a:** the producer: the records and the publication of items 2 to 6. It depends on X4T-a and on X4T-b's publication protocol.
    - **X4B-b:** the wiring at X4T's fenced first read (item 1): the F-absent branch, the acceptance and the one re-admission on the confirmed retained `state.v1`. It depends on:
      - X4B-a;
      - X1's returned fence;
      - X3a's retained store;
      - X4T-b's fenced read.

      It does not depend on X2e, which only receives the view.
    - **X4B-c:** moving X4T-0 onto X4B's producer (item 9).

    All are required before X11. None is required for the M2 exit matrix, which runs on X4T-0's synthetic stores.

## Forbidden substitutes

- acceptance in the creator invocation, or from a read-only command;
- any payload other than the running core's embedded bootstrap;
- `Trusted`, or any stored role state, set by fiat or by an event sequence `decide` doesn't accept;
- acceptance inside `admit_ordinary_writer`, at X2e, or under any lease;
- more than one re-admission;
- a record written without its closed-shape admission;
- the pointer before its dependencies;
- deleting records after a failure;
- a new public code;
- X4T-0's test constructor reachable from production.

## Not claimed

- ordinary payload import and S4.5 recovery;
- later role events (install, recover, quorum);
- CLI enablement (X11);
- network acquisition of payloads;
- a qualified measured macOS 27 profile row. On this BASELINE-ATTESTED host, real reads refuse at `/` without a premise, so real acceptance is exercised only on scratch chains.
