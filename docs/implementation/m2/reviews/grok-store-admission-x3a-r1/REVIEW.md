# Review: store admission X3a r1

Verdict: REQUIRED-FINDINGS.

Subject `docs/implementation/m2/store-admission-x3a/PROPOSAL.md` is 11034 bytes, sha256 `60288d02aece9f5dfd136c72de17206aa894bc37027904d7c5459bdeb98d2651`, matching hashes.txt. Product HEAD is `fdbedf4acc7ef57fb71eed424c3b08fa2af7fe98`, and the tree is clean. The real OpenSIP support directory is absent. No product cargo.

## Item 1

Admitting the endpoint without a namespace is sound. Owner §1 and §8 form the five-field value only after an actual registry namespace is admitted, and that N is a UUIDv4 taken from the selected registry. P0 has an empty registry, so no five-field binding exists before X2. `SelectedStoreEndpoint` is private, not Clone and not serializable, and it is borrowed from one held session. Holding the decoded pair, S from the physically opened marker, the node at exact (S, G, K) and that node's admitted ancestry gives the later binding its base. The value grants no namespace, project, lease, journal, ledger, blob or commit authority. Rejecting a placeholder or test N follows §8. Placing the five-field value in the first unit after X2 that has a registered project follows the exit plan.

The lookup owner §7 requires also compares C.store's three fields with the admitted triple. Item 1 does not. See RF-1.

## Item 2

The single read and the full sample are sound. `DescriptorMetadata` carries `device`, `inode`, `mode`, `uid`, `gid`, `links`, `size`, `modified`, `changed` and `flags`, and `changed` is `(ctime, ctime_nsec)`. Retaining that sample and the decoded value from the session's own read, then comparing the full sample on every session recheck, catches an in-place rewrite that updates `changed`, `size` or `modified`. That is owner §8's rule that a fenced session retains originals and rechecks its contributing owners, with any observed failure latching the session. Rejecting a second per-node capture is right.

The subject item 2 gives that recheck is wrong. See RF-2.

## Item 3

The 64-node bound is sound for M2. Each node is charged before its own read, as 458c item 5 step 3 already requires, and the per-node charge is unchanged. A chain past 64 is the existing budget row: `SYSTEM.OUTCOME.ILLEGAL_STATE`, `WORK.BUDGET_EXHAUSTED`, fault `host-invariant`. That row is unavailability, which is owner §8's rule that a limit failure is never "no ancestor" and never permission to repair. Dropping the second capture and the per-node full recheck is what removes the old edge pile-up. X3a-1's pin of the measured cost of a 64-node chain, on a deep scratch home, for both the gate and the observation session, within the owner caps and the session's other reservations, is the right closure. I did not replay that measurement.

## Item 4

The read-side switch is sound. `host::installation_lineage`, `installation_records`, `installation_selection` and `storage::store_root::native_marker::ProvisionalStoreMarker::read_existing` take the pair, the marker and the chain from the session's `SelectedStoreEndpoint`. The extended 458c-b2 source pin, scoped to a second capture of a required endpoint file, leaves `capture_descendant` for files the session has not already read. The public behavior change is the one the law discloses: those readers inherit the full-sample recheck and the 64 bound. X3a-2's reviewed description override for `installation_lineage.rs` is the override owner §9 requires, and it keeps the historical inventory bytes. The inherited effective sentence already names the physically opened selected endpoint store marker; the override is still the successor §9 asks for.

## Item 5

`STATE.SCHEMA_UNSUPPORTED` is the right existing detail for a store `stateSchema` K the selected core does not support. The public-detail registry lists that code, owner security, selector "security model D9 mapping". Its S12 row is class `request-rejected`, exit 2, error code `REQUEST.SCHEMA_MAJOR_UNSUPPORTED`. Deferring the class and error code to that row is 468's rule that the registry prevails. The K named on 468's core row is InitialCore's `StateWriter`, which `core_refusal` already publishes as subject `state-writer`. The store schema and that writer are different refusals.

The incomplete subjects and the coreClosure row do not match the 468 item 6 pairing. See RF-3 and RF-4.

## Items 6 to 8

F00 holds: a writer that fails endpoint admission receives no `SelectedStoreEndpoint`, has no commit call, and the session owner releases the fence. F24's refusal of a failed read or a wrong generation satisfies "never interpret as no commit" once the subject in RF-3 is the incomplete row. The core-mismatch arm is RF-4. F27's namespace, operation and execution joins belong with X3b, X3c and X5, after a registered project can supply N. The C.store join is the comparison in RF-1; items 6 and 8 do not assign it to a later unit. One ledger per session, with the endpoint's in-memory checks charged on that same `WorkScope` and no branch-local reset, matches owner §8 and X1 item 5. X3a-1 is the sample, the bound, the endpoint, the remaining node-law checks, the refusal mapping, the tests and an inventory successor. X3a-2 is the read-side adoption, the extended source pin and the description overrides, including `installation_lineage.rs`. X3b's law then places the N-bound binding after X2.

The header still says X1 r1 is under review. X1 r1 is accepted. The decisions use `OrdinaryWriteAdmission` and the two ledgers as that law left them, so the stamp is stale and is not a finding.

## Required findings

### RF-1 — Endpoint admission omits the C.store comparison

Owner §7's lookup compares C.store's three fields with the admitted triple, and that sentence says the comparison is necessary and is separate from original-time and current-authority admission. Item 1 compares the pair's `coreClosure` with the receipt's selected core and compares K with the core's supported schemas. It retains the trust current record as a required-file identity and puts trust admission under "Not claimed". The three C.store fields are never compared, and no later unit is given that comparison.

Failure scenario: the marker and the node admit (S, G, K), and C.store on the trust current record holds a different S, G or K. `SelectedStoreEndpoint` is still granted. A later binder treats that triple as the store §7 admitted. F27's join against C.store is never made.

### RF-2 — The rewrite recheck names subject `changed`

`gate_refusal` maps `CustodyRefusal::Changed` to `CONFIG.CUSTODY_REFUSED` subject `required-files-changed`. The neighbouring subjects are `name-changed`, `fence-changed` and `identity-changed`. No arm publishes `changed`. Item 2 says an in-place rewrite fails on subject `changed`, "already 468c's for `CustodyRefusal::Changed`". Item 5 then says a recheck failure keeps its 468 item 6 row, which is the `required-files-changed` subject.

Failure scenario: an in-place rewrite of a retained endpoint file updates ctime. The full-sample recheck returns `CustodyRefusal::Changed`. An implementer who follows item 2 emits subject `changed`. The accepted routing and the host custody row emit `required-files-changed`. The same rewrite is pinned to two subjects.

### RF-3 — Structural refusals use the doctor finding subjects

468 item 6's incomplete row is `CONFIG.INVALID` / `CONFIG.CUSTODY_REFUSED`, subject `installation-incomplete`. `gate_refusal` maps every `IncompleteRefusal` variant (`Missing`, `Pair`, `Marker`, `Store`, `Node`, `Chain`) to `InstallationTermination::Incomplete`, and the host projection emits that unsuffixed subject. 458c item 7 ends every non-doctor read of an incomplete or contradictory I on that same subject. 458c item 12's colon subjects (`installation-incomplete:pair`, `:marker`, `:store`, `:node`, `:chain`, `:missing:<path>`) are doctor report entries. Doctor does not terminate on them, and a writer produces no report. Item 5 says the structural endpoint failures, including the node-law rules the session does not already check, keep the 468 incomplete row with those item 12 subjects.

Failure scenario: a broken chain or a duplicate-key disagreement becomes `GateRefusal::Incomplete`. Following item 5 publishes subject `installation-incomplete:chain`. The host row for `Incomplete` publishes `installation-incomplete`. A host left on the accepted subject fails the law's tests. A host changed to the colon subject moves every non-doctor incomplete read off 458c item 7, and a writer termination carries a doctor finding subject.

### RF-4 — A coreClosure mismatch is routed as a core refusal

468 item 6 routes a present but contradictory installation, including wrong owner-chain linkage, to `CONFIG.CUSTODY_REFUSED` subject `installation-incomplete`. 458c item 7 ends other read commands on that row. The 468 core row is the InitialCore family (release authentication, revocation, entrypoint, code-signing flags, `StateWriter`, core-tree custody), published as `EXTENSION.ADMISSION_REJECTED` / `NT-TCB-IDENTITY` with that refusal as subject. `core_refusal` already publishes `StateWriter` as subject `state-writer`. Item 5 routes a pair whose `coreClosure` differs from the session receipt's selected core to that core row, subject `selected-core-mismatch`, and calls the case F24.

Failure scenario: the receipt's core admitted, and the selection pair names another closure. The law publishes `NT-TCB-IDENTITY`. Callers and tests treat that detail as a failed core admission. The contradictory installation leaves the incomplete row that 468 item 6 and 458c item 7 already assign to it.
