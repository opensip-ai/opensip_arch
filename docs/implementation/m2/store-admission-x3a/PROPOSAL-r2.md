# Selected store endpoint admission under the held fence — proposal X3a r2

2026-09-30. Claude Opus 5.5, implementation lead. Law for unit X3a of EXIT-PLAN.md, under owner.md §7 and §8, laws 468 r5, 458c r6, 461 r3 and X1 r1 (under review), and the build plan's F00, F24 and F27. Items 1, 2, 3, 5 and 6 contain lead decisions, made under the owner's standing direction of 2026-09-30 to proceed on the lead's recommendation and record it. r2 answers Grok X3a r1 RF-1 (the C.store join), RF-2 (the rewrite subject), RF-3 (structural subjects outside doctor) and RF-4 (the core mismatch row). r1 bytes are preserved in PROPOSAL-r1.md. Not code. Library only: no CLI command is wired.

## Problem

Owner §7 binds an ordinary operation to its selected store: capture the selection pair, open its physical endpoint, take S from that endpoint's immutable marker, locate the node at exact (S, G, K), admit the node's complete ancestry under §7's node law, and compare the pair's core closure and the admitted triple with the selected core. §8 then derives the five-field binding `{schemaVersion, namespaceId N, S, G, K}`. N comes only from the selected project registry's ACTIVE row, after project-root, marker and namespace admission.

Two facts at product fdbedf4 shape this unit.
- **The sessions already read the endpoint once.** 468b's gate step 2 and 458c's observation step 3 both read `selection.pair`, the endpoint marker and the whole node chain (decoding each to find the next file) through the held fence's retained handles, charged to the session ledger. `DurableInstallation` and `InstallationObservation` retain each file only as `RequiredFile { relative, identity: (device, inode) }`. The bytes are discarded, so the identity-only recheck cannot detect an in-place rewrite of a retained file.
- **The host readers read it again.** `host::installation_lineage::ProvisionalInstallationLineage` re-captures the pair, the marker and every node through `InstallationReadFence::capture_descendant`, each paying a full session recheck (about 3.4k edges per node on a deep scratch home, 458c-b2). That bounds the readable chain at roughly 35 nodes, and it is the 458c-b2 budget follow-up.

P0 has an empty project registry. No N exists until project registration (X2), so no five-field binding can exist before X2.

## Decisions

1. **What X3a admits: the selected store endpoint, not the binding (lead decision).** X3a produces `SelectedStoreEndpoint`, which is private, not Clone and not serializable, and is borrowed from one held session. It holds:
   - the decoded selection pair and its retained file;
   - S, taken from the physically opened endpoint's marker (owner §7; the pair only locates);
   - the node at exact (S, G, K), with its actual closed fields equal to its physical key;
   - the node's complete admitted ancestry under owner §7's node law: schema, canonical and cap correctness at each lookup; full triple equals path key; predecessor and origin both null or both nonnull; no self predecessor; every predecessor at its exact key; duplicate-key disagreement refuses; iterative acyclic traversal ending at exactly one root;
   - the comparison of the pair's `coreClosure` with the session receipt's selected core closure, and of K with the core's supported state schemas;
   - the comparison of the trust current record's `C.store` (S, G, K) with the admitted triple. All three fields must be equal. This is F27's endpoint join against `C.store`, and X3a makes it; no later unit repeats it.

   It grants exactly one thing: the base that the N-bound binding of owner §8 is later derived from. It grants no namespace, project, lease, journal, ledger, blob or commit authority, and no trust admission. The trust current record stays a required-file owner of the session (468 item 5), not a trust admission.

   **Rejected:** deriving a binding now with a placeholder or test N. Owner §8 forbids any N not obtained from the selected registry. The N-bound binding is produced in the first unit after X2 that has a registered project (X3b's law decides where), and EXIT-PLAN's X3b/X3c rows gain X2 as a dependency for their real paths.
2. **One read of each endpoint file per session (lead decision).** The endpoint is admitted from the session's own single read; nothing re-captures a file the session already read.
   - **Producers.** It is produced from `DurableInstallation`, reached through X1's `OrdinaryWriteAdmission` or 468c's `AdmittedInstallation`, and from `InstallationObservation`, reached through `ReadSession` (458c-b2). Both sessions already read the pair, the marker and every node in gate step 2 or observation step 3.
   - **Retention.** `RequiredFile` grows to retain, from that single read, the full `DescriptorMetadata` sample (including `size`, `modified` and `changed`) and the decoded value of each endpoint file (pair, marker, nodes).
   - **Rechecks.** Every session recheck (468 item 3; 458c item 5 steps 2 and 4) compares that full sample, not only (device, inode). An in-place rewrite of a retained file, which changes `changed`, therefore fails the recheck on the custody row: `CONFIG.CUSTODY_REFUSED` with exactly the subject 468c's `gate_refusal` gives `CustodyRefusal::Changed`, which at fdbedf4 is `required-files-changed`. No second subject exists for the same rewrite.
   - **Admission.** The endpoint admission adds no file read: it validates the retained decoded values under owner §7's node law, then runs one session recheck. Any failure latches the session.

   **Rejected:** keeping per-node captures with cheaper rechecks. That still reads every node twice per session and leaves the identity-only recheck gap.
3. **The chain bound (lead decision).** The node chain is read once per session, charged before each node's read (458c item 5 step 3), and at most `MAX_LINEAGE_NODES = 64` nodes are read.
   - **Over the bound.** A chain longer than 64 is a limit failure: the budget row (`SYSTEM.OUTCOME.ILLEGAL_STATE`, `WORK.BUDGET_EXHAUSTED`, `host-invariant`), unavailability, never "no ancestor" or permission to repair (owner §8).
   - **Why 64.** A generation advances only at an explicit store transition (selection, migration or restore), each its own owner act, so 64 is far beyond any M2 installation. A later compaction or retention law may revisit it.
   - **Charging.** The gate and the observation session reserve their step 2 or step 3 reads before they run, as today. The per-node charge is unchanged. What changes is that no second per-node capture or per-node full recheck exists.
   - **Pin.** 461a-style tests pin the measured cost of a 64-node chain on a deep scratch home, for both the gate and the observation session, as within the owner's caps with the session's other reservations.
4. **The read side adopts it now.** The read side gets the same endpoint admission in this unit, from `ReadSession`'s observation.
   - `host::installation_lineage`, `installation_records` and `installation_selection` take the pair, the marker and the chain from the session's `SelectedStoreEndpoint` instead of re-capturing them through `capture_descendant`.
   - `storage::store_root::native_marker::ProvisionalStoreMarker::read_existing` takes the marker the same way.
   - Their public behavior is unchanged except that they now inherit item 2's full-sample recheck and item 3's bound. The 458c-b2 source pin is extended so that none of them captures a required endpoint file a second time.
5. **Refusal rows (lead decision).** There are no new public codes. Every refusal is an existing row:
   - **A missing, undecodable or misbound endpoint file or node; a broken chain; a key mismatch; duplicate-key disagreement.** The session already reports these as structural findings (458c item 7). They keep 468 item 6's incomplete row exactly: `CONFIG.CUSTODY_REFUSED`, subject `installation-incomplete` (458c item 7), for every non-doctor reader and writer. The per-finding subjects of 458c r6 item 12 (`installation-incomplete:pair`, `:chain` and so on) appear only as doctor report entries, never in a termination.
   - **A rule of owner §7's node law that the session does not already check** (predecessor and origin both null or both nonnull, self predecessor, more than one root, a cycle). These are structural findings of kind `Chain`: the incomplete row in a termination, and `installation-incomplete:chain` only as a doctor entry.
   - **The pair's `coreClosure` differs from the session receipt's selected core, or `C.store` differs from the admitted (S, G, K).** This is F24 or F27 at the endpoint: the installation's owner chain is contradictory, while the core itself was admitted. It is the incomplete row (468 item 6 and 458c item 7: wrong owner-chain linkage). Each is a new `IncompleteRefusal` kind. In doctor each is a structural finding, so this law extends 458c r6 item 12's closed list of doctor entry subjects with exactly two: `installation-incomplete:core` (pair `coreClosure` mismatch) and `installation-incomplete:current-store` (`C.store` mismatch). Each has one fixed remedy in the same form. They are doctor entries only, never a termination subject. No code or schema changes. Rejected: `NT-TCB-IDENTITY`, which callers read as a failed core admission.
   - **K not supported by the selected core.** The existing detail `STATE.SCHEMA_UNSUPPORTED`, with the class and error code its S12 row fixes. Where that registry row already fixes a class, it prevails.
   - **A recheck failure** keeps its 468 item 6 row. **A limit failure** (item 3) is the budget row.
6. **Failure cases.**
   - **F00 (before project/store admission).** A writer that fails endpoint admission holds no store authority and has no commit call. Its fence is released by the session's owner.
   - **F24.** A failed read, wrong generation, or core-mismatched pair is never "no commit": it refuses as above.
   - **F27 (lead decision on the split).** X3a makes the endpoint joins: the pair's core closure, and `C.store`'s (S, G, K) against the marker and node. The namespace, operation and execution joins of F27 belong to X3b, X3c and X5.

   No other F-case is in X3a's scope.
7. **Budget.** There is one ledger per session, as today: the gate's own ledger on the write side (X1 item 5) and the observation session's on the read side (458c item 6). The endpoint admission's validation is in-memory and is charged as object and edge work proportional to the chain, through the same `WorkScope`. There is no branch-local reset (owner §8).
8. **Units after the law.**
   - **X3a-1:** `RequiredFile`'s retained sample and decoded values, the full-sample recheck, `MAX_LINEAGE_NODES`, `SelectedStoreEndpoint` from `DurableInstallation` and `InstallationObservation`, owner §7's remaining node-law checks, the refusal mapping, and tests (including the 64-node cost pin and an in-place-rewrite recheck failure). Plus an inventory successor.
   - **X3a-2:** read-side adoption (item 4), the extended source pin, and description overrides for the changed host and storage readers, including `installation_lineage.rs`, whose description owner §9 requires to stop promising per-node markers. Plus an inventory successor.
   - X3b's law then decides where the N-bound binding is produced, after X2.

## Forbidden substitutes

A binding with an N not read from the selected registry; a placeholder or test N in production; S taken from the pair or a node rather than the physically opened endpoint's marker; a second capture of a required endpoint file in one session; an identity-only recheck of a retained file whose decoded value is used; a per-node full session recheck; an intermediate store's marker read during traversal (owner §7); treating a missing node, a limit failure or a failed read as absence, "no ancestor" or "no commit"; repairing, reselecting or creating a store or node; a new public code.

## Not claimed

The N-bound five-field binding and its digest (after X2); project registration, project-root admission and the S7 lease; journal, ledger, blob and commit (X3b to X3d); trust current admission; store transitions (selection, migration, restore) and compaction of long chains; carrier formats (F46 to F51); CLI enablement. This macOS 27 host stays BASELINE-ATTESTED, so real sessions refuse at `/` and every test uses scratch homes with synthetic signed profiles.
