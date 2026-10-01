# First trust acceptance from the embedded bootstrap payload — proposal X4B r1

2026-10-01. Claude Opus 5.5, implementation lead. Law for unit X4B of `EXIT-PLAN.md`, created by X4T r4 to r7 (item 13). It is written under:
- the security contract's S4 (trust time, step 2 "fresh install") and S4.5, S5 and S6;
- laws 463 (core, release and the embedded release values) and 466/467 (P0 and its producers);
- the accepted laws X1 r1, X2 r5, X3a r5, X4 r7 and X4T (r7 under review).

Items 1 to 7 contain lead decisions made under the owner's standing direction to proceed on the lead's recommendation; each names the alternative it rejects. Not code. Library only: no CLI command is wired.

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

1. **Trigger: the first ordinary write, lazily (lead decision).** Acceptance runs inside X1's `admit_ordinary_writer` path, at X2 r5 item 7's lease-free point: under the installation fence, with no project lock, at the same point as X4T's fenced admission. When X4T's fenced first read returns F absent, and only then, the ordinary-writer admission runs X4B and then re-runs X4T's fenced admission on the new state, still under the same fence.
   - **Read-only commands never bootstrap.** Doctor and query keep reporting F absent (458c, report-only).
   - **Rejected:** the creator path. 468c's `route` drops `InitialCore` before the gate (468 r5 item 1), so the embedded payload's authority is gone. X3a r5 already rules that a creator invocation gets no store, for the same reason.
   - **Rejected:** a separate `trust bootstrap` command. It would add a mandatory user step with nothing to decide.
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
4. **Role transitions.** For each role whose accepted document the payload carries, the role machine's `PresentOrdinary` event moves `Unbootstrapped` to `Trusted`. It is recorded as one `EV-PRESENT-PAYLOAD` trust event with its `RoleChangeV1` and `PublicationEventV1`, and `accepted.by` names that event.
   - Roles the payload doesn't carry stay `Unbootstrapped`.
   - An expired, stale or revoked document gives the state `role_machine::decide` returns, never `Trusted` by fiat.
   - If core, index or component ends anything but continuable, X4T's re-admission refuses on its continuation row, after the acceptance is durably recorded. The record is honest even when the result is unusable.
5. **The writes: one publication, atomic at the pointer (lead decision).**
   - **The records:** under the held fence, X4B writes the payload closure and every record of item 4, plus:
     - `RootAdmissionNodeV1`, and the `MetadataAdmissionNodeV1`s for the catalog and revocation;
     - `RevocationHistoryNodeV1` (the list form, as X4T-0's shape);
     - `TimeEvidenceV1` and `SignedTimeSourceV1`;
     - the operation input;
     - the revision-2 `PublicationDescriptorV1` on the P0 predecessor;
     - the retained-phase `TrustCapsuleV1`.
   - **How they are written:** each record is canonically encoded and admitted by its closed shape before it is written. Each file goes through 467's private-file producer with its file barrier. The `state.v1` pointer goes last, by atomic replacement (exclusive temporary name, file barrier, rename, directory barrier, reopen and confirm), exactly as X4T item 7's floor write-ahead does.
   - **Retained evidence:** the confirmed new `state.v1` becomes the session's retained owner, as X4T item 7 and X2 r5's registry rule require.
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
8. **Budget.** It is charged to the gate ledger at the lease-free point, as X4T-b's write-ahead is. Each record is charged before it's written, every post-effect confirmation is reserved first, and the root chain is within `ChainBudget`.
9. **Relation to X4T-0.** Once X4B's producer exists, X4T-0's test-only constructor is replaced by calls to it, wherever X4B can produce the requested role states. X4T-0 keeps only the states acceptance can't reach, for example Revoked or QuorumLost, as test-only constructions. Its source pin stays.
10. **Tests.**
    - **Scratch installations,** with a test-only embedded release whose bootstrap payload is signed with the public quorum62 seeds (462/463's test trees). Covered cases:
      - P0 → accepted, after which X4T admits the result with every carried role `Trusted`;
      - the future-dated payload, beyond-horizon and fresh-install time rules;
      - an expired document at acceptance;
      - a crash before the pointer, then a rerun;
      - an uncertain pointer replacement;
      - a dev build at `CORE.NO_EMBEDDED_RELEASE`;
      - read-only commands never bootstrapping.
    - **Round trip:** X4T-a's loaders (`capture_p2`, `bind`, `bind_retained_head`, `Budget::load` and the `accepted.by` check) accept what X4B writes.
11. **Units.**
    - **X4B-a:** the producer: the records and the publication of items 2 to 6. It depends on X4T-a and on X4T-b's publication protocol.
    - **X4B-b:** the wiring into X1's ordinary-writer path at the lease-free point, with the X4T re-admission. It depends on X4B-a, X1 and X2e.
    - **X4B-c:** moving X4T-0 onto X4B's producer (item 9).

    All are required before X11. None is required for the M2 exit matrix, which runs on X4T-0's synthetic stores.

## Forbidden substitutes

- acceptance in the creator invocation, or from a read-only command;
- any payload other than the running core's embedded bootstrap;
- `Trusted` set by fiat;
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
