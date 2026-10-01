Grok review: X2e with X3b-3, the checked operation handoff (law X2 r8 item 7a) composed with the grant journal's floor step, carrier start and end step (law X3b r10 items 1, 3, 3a, 4 and 11), with inventory v111 (parent v112). Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-operation-handoff-x2e-r1. If you build or test, use a CARGO_TARGET_DIR under that directory. Run git only read-only, and only against the worktree below. Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent. Never read or print the private 413 UUID fixture.

## Law

All in arch `docs/implementation/m2/`, accepted:
- `project-root-x2/PROPOSAL.md` r8: item 7a (the handoff), item 7's ordering note (the floor step before the lease), items 8 and 9, and item 10's X2e row ("X3a's store binding and X3b depend on it").
- `journal-x3b/PROPOSAL.md` r10 (accepted 2026-10-01, after this unit started; r9 bytes are PROPOSAL-r9.md): items 1 (X2e composes both steps), 2, 3, 3a, 4 (start, end, r9's nothing-after-uncertain, r10's closed attempt ledger), 9, 11 (r10 tests) and 12's X3b-3 row.
- `store-admission-x3a/PROPOSAL.md` r5: items 1 and 2 (the endpoint from the gate's one read).
- `live-guards-x4/PROPOSAL.md` r7: items 2 and 6 (the monitor at the lease-free point; `OperationGuard` built inside X2e's handoff). X4a has not landed.
- `trust-admission-x4t/PROPOSAL.md` r9: item 7 (the write-ahead floor and the handoff rollback check) and item 9 (the fenced first read at the lease-free point, not inside 7a). X4T-b has not landed.
- `commit-session-x3d/PROPOSAL.md` r6 (accepted with X3b r10): items 1, 2, 7 and 8, for what X3d-1 receives (`CommitSession::open(ProjectOperation)`) and `finish`'s end path.
- Also: S7 "Leases and lock order" in `docs/v2/contracts/product-v1/security-and-lifecycle.md`; the X2d r1 review (`reviews/grok-namespace-lease-x2d-r1/REVIEW.md`), judgment call 5.

## Subject

Pins are in hashes.txt.
- **Product:** the worktree `/Users/sb/code/opensip-ai/opensip-x2e`, detached at f1b8321 (X2d at 9d51f33, F4 at 8bd0283, X3d-0 at f1b8321; inventory v112 selected). Save `git -C <worktree> diff` (the four new files are intent-to-add) as product.diff and report its sha256. Lead's value: `7992c1a0e603174ac75ee7daad27712bd4af8dffb2bbc51c49ecc813f242d2c6`, 95794 bytes; 14 files, 1948 insertions, 26 deletions.
- **Arch:** v111 (parent v112: `repository-file-inventory.v112.json`, 365881 bytes, sha256 `acfc4bc9cc896bab1f916d4a06eb6adc87bab89b2a1c809696dba09b13c7473a`), `operation-handoff-x2e-inventory-v111-subject.json` and `operation-handoff-x2e-inventory-v111/`. These files are untracked in arch until acceptance. v111 was numbered before X3d-0 took v112; the chain is linear by parent (v110 → v112 → v111).

## What it does

New code, all crate-private in `opensip-security`, library only:
- `custody/operation_handoff.rs` (X2e) and its tests;
- `journal_store/carrier_operation.rs` (X3b-3's journal half, declared as `carrier_floor`'s child module `operation`) and its tests.

**The handoff: `OrdinaryWriteAdmission::begin_operation(self, subject, WriterLease, inputs) -> Result<ProjectOperation, OperationRefusal>`.** One writer, one gate, one fence hold, in this order:
1. **Endpoint join (X3a).** `join_store_endpoint`: `validate_endpoint` over the gate's one read against the receipt's selected core, on the gate ledger, then the gate's and the receipt's rechecks. Unlike `admit_store_endpoint` it keeps the writer. It runs first, so a store mismatch refuses before any floor write.
2. **Namespace admission (X2d).** `namespace_lease::admit`, with no lock taken.
3. **Lease-free point.** `NamespaceTarget::lease_free` hands the step the holder and N:
   - on the gate ledger (`fenced`, then the gate's and receipt's rechecks): `I/trust` is confirmed by X2d's `required_directory` (present, private, exactly named, on I's device). N's absolute spelling is `H/Library/Application Support/OpenSIP/preview-v1/host/projects/N`, built from H's spelling as the gate walked it, and admitted only if a no-follow `lstat` of it finds the retained N's (device, inode);
   - on the attempt ledger (`attempt_step`, then the gate's and receipt's rechecks): X3b's floor step through `CarrierLocation::admitted`, keeping its observation (`OperationFloor`).
4. **Lease (X2d).** `lease_writer`, APPEND-WRITE or EXCLUSIVE.
5. **Item 7a.**
   - **Step 2, the move:** `FencedNamespace::into_parts` moves the lease, subject, row and namespace out and ends the borrow of the writer, which still holds the fence. Nothing is copied.
   - **Step 1, the join:** on the gate ledger, the subject (registered: X2c's exact footprint), the namespace directories and each locked carrier's binding are rechecked, and owner §8's binding `{1, N, S, G, K}` is derived from the ACTIVE row and the gate's endpoint. N must equal the confirmed namespace id.
   - **Step 3, the carrier start:** on the attempt ledger: `create_carrier` when the floor step found INIT (`InitFloorWritten` or `InitPending`), then `carrier_start` against the floor step's observation, then `JournalAppendLock::after_start`. Then every owner is rechecked again, with a registered subject's namespace held to `Footprint::Started`.
   - **Step 4, the release:** the writer and `DurableInstallation` are split (`into_parts`, `into_handoff`). The gate and its ledger end. `ProjectOperation` is assembled from the moved owners, and only then is the fence released.

   Any refusal spends the gate. Locals drop in reverse order: the append lock, then the lease, then the writer, which releases the fence.

**`ProjectOperation`** (private, not Clone). It holds:
- the started carrier (`OperationCarrier`: the append lock, the start tail, the reconciliation, the creation outcome);
- the `HeldLease` and its mode;
- `OperationBinding`;
- the ACTIVE row snapshot;
- the subject (`NamespaceSubject`, as X2b or X2c retained it);
- the namespace directories;
- N's spelling;
- `I/trust`;
- the endpoint values and the required files' full samples;
- the retained chain to I, with no lock;
- the account;
- the write receipt (whose attempt ledger is the operation ledger).

Accessors: `binding`, `row`, `mode`, `subject`, `endpoint`, `required`, `selected_core`, `carrier`, `attempt_closed`, and `journal(|location, carrier, work| …)`, which runs one step on the attempt ledger with the carrier location (X3d's appends).

**End path: `ProjectOperation::end(self, JournalOutcome) -> OperationEnd`.**
1. The append lock is dropped, then the lease is released (`readers.lease`, then `writer.lease`).
2. If the owner reports `Uncertain`, or the attempt ledger is closed, it returns `NotEntered`: no fence, no read, no copy, no disclosure (X3b r10 item 4, X3d r6 item 7).
3. Otherwise, on the attempt ledger:
   - the fence is retaken by `walk_chain` from the retained H spelling and uid, `open_fence`, and installation_session's bounded wait (now `pub(super)`, unchanged);
   - the walked I's identity must equal the retained I's;
   - `trust`, `host`, `projects` and N are rebound by name (`rebind`);
   - `operation_end_copy`, which is X3b-1b's `end_step(Certain)`, runs;
   - the fence is released last, whatever the copy returned.

   Results: `Ended(EndOutcome)` or `Failed(EndFailure)`, which carries a row. A failure never rewrites the operation's outcome.

**Journal half (`carrier_operation.rs`).**
- `CarrierLocation::admitted(&CarrierPlace)` is the only production constructor; `CarrierPlace` is built only in operation_handoff.rs.
- `operation_floor_step` returns the outcome plus the committed tail to confirm.
- `operation_start` runs creation when INIT, then start, then the append lock. A skipped floor step (busy `writer.lease`) has no observation, so if the lease was nevertheless taken it refuses on the busy row with nothing written.
- `operation_end_copy`.

It adds no carrier semantics. It re-exports only what custody names.

**Edits to existing files.**
- `namespace_lease.rs`: `lease_free`, `into_parts`/`NamespaceParts`, `pub(super)` helpers, and a `Footprint` argument to `recheck_subject`. X2d's own calls pass `Exact`.
- `first_registration.rs`: `Footprint { Exact, Started }`, `recheck_registered_with` (`recheck_registered` is unchanged and still `Exact`), `Owner::Trust`, `Step::Handoff`.
- `ordinary_writer.rs`: `begin_operation`, `join_store_endpoint`, `attempt_step`, `into_parts`.
- `read_premise.rs`: the write receipt's `charge` (attempt ledger, with the same qualification lent) and `is_closed`, plus a `cfg(test)` `attempt_used`.
- `installation_admission.rs`: `DurableInstallation::into_handoff`, `Chain::installation_id`.
- `installation_session.rs`: `wait` becomes `pub(super)`.
- `journal_store.rs`, `carrier_floor.rs`, `custody.rs`: module declarations and re-exports. carrier_floor's `CarrierRow` is re-exported as `CarrierRefusalRow`, because journal_store has its own `CarrierRow`.

carrier_start.rs and carrier_append.rs are not edited (X3b-4 is changing them).

## Judgment calls: please rule on each

1. **Ledgers.** X3b's carrier work goes on the write receipt's attempt ledger: the floor step, creation, start, journal steps, and the end step including its fence walk. X3b r10 item 9 (r7 text) names the operation ledger as X1 item 5's attempt ledger, and X3d r6 item 8 agrees. X2e's own fenced work (trust confirmation, spelling, rechecks, binding) is on the gate ledger, per X2 item 9 and X4 item 6 ("the gate ledger ends at the fence release"). Each attempt-ledger step under the fence is followed by the gate's and the receipt's rechecks, and a refusal spends the gate too. **Rejected:** carrier work on the gate ledger (that contradicts X3b's operation ledger), and the reverse.
2. **X2d judgment call 5, resolved.** `Footprint::Started` drops only X2c's closed entry scan. N must still be private, and both lease files present, private and empty. It is used only for the recheck after the carrier start. X2c's registration and every X2d step stay `Exact`. **Rejected:** skipping the subject recheck after the start (it leaves the release unchecked), and relaxing `Exact` everywhere (X2c's registration and lease must still prove the published footprint).
3. **Order and the move.** The endpoint join runs first, before any effect. Item 7a's step 2 destructure is plumbing: it ends the `&mut` borrow so the writer's fence and the moved owners can be used together. The join's recheck and binding then run under the same fence. `ProjectOperation` is assembled after the start, and the fence is released last. Step 2's semantic content (owners moved, never copied, out of the fenced gate) holds throughout.
4. **The binding is values only.** No digest: X3a r5 leaves the digest unclaimed, and X3c and X3d own its use. N comes from the ACTIVE row and must equal the confirmed namespace id. S comes from the opened marker; G and K from the pair (`SelectedStoreEndpoint`).
5. **The carrier place.** `I/trust` is confirmed under the fence on the gate ledger, because absent is 468's incomplete row and non-private is its custody row. N's spelling (needed by X3b's SQLite path opens) is admitted only by identity with the retained N. `CarrierLocation::admitted` takes only `CarrierPlace`, so no caller path reaches a location. A source pin guards the constructor.
6. **A skipped floor step, then a free lease.** X3b item 3 says "continue; X2d will then report the busy row". If the other writer released `writer.lease` in between, the start has no observation to confirm (item 4), so it refuses on the busy row with nothing written. **Rejected:** a second floor step under the lease (S7 forbids a floor write under a lease).
7. **End path.**
   - The decision whether to enter is taken from the owner's `JournalOutcome` (X3d's `finish` decides, X3d r5/r6 item 7) and from the attempt ledger's closure (X3b r10). The append lock's own undetermined latch is not consulted: that would need a new `try_lock` in carrier_append.rs, whose source pin counts them, and X3b-4 is changing that file.
   - Under the fence, the walked I must be the retained I, and the location's directories are rebound by name before the copy. **Rejected:** copying through possibly-moved retained handles.
   - The receipt is not rechecked at the end. The law names no such step, and the end is not an effect admission.
   - `NotEntered` covers both the uncertain and the closed-ledger cases and is never disclosed.
8. **Seams not built.**
   - X3b-4's rollover (`end_step_after_exhaustion`) and the `CarrierCapacityExhausted` thread into the end step's step 3: X3b-4 is not integrated, and its r12 order is X3b-4 then X3b-3. They join when this unit is rebased onto X3b-4.
   - X4a's monitor and X4T-b's fenced admission at the lease-free point (commented in `lease_free`).
   - `OperationGuard` inside the handoff (documented in `ProjectOperation`).
   - No placeholder types.
9. **Writer side only.** The read session's `FencedNamespace<&ReadSession>` stays drop-only. There is no reader consumer of a `ProjectOperation`: the carrier start and the floor write are writer steps, and X4's guard is for writers. Item 7a's "session or gate" is satisfied for the gate, and the read side waits for its first consumer.
10. **Eligible owners as retained.** An Eligible subject moves X2b's `ProjectRootAdmission` (chain, incarnation, marker observation, R0) and tracking. There is no extra `.opensip` handle. The registry and pair captures ride along as provenance and nothing rechecks them after the release (item 7a). X4a's guard set chooses its post-release rechecks.
11. **Rows.** `OperationRow` is one of: `Installation` (the endpoint's or release's 468c row), `Project(ProjectWriteRow)`, `Carrier(CarrierRow)` or `BudgetExhausted`. `Owner::Trust` maps to the installation custody row. A failed fence unlock after the start is host I/O, and the operation is dropped. No public code is added.
12. **Laws revised mid-unit.** The unit was assigned against X3b r9. X3b r10 and X3d r6 were accepted while it was built, and the code follows r10 (the end step is not entered on a closed ledger, with no disclosure). Under r9-literal it would have been an end failure disclosed as budget `Closed`. No contradiction was found in the accepted laws.
13. **Stale descriptions.** ordinary_writer.rs and read_premise.rs were already stale and are carried by value. first_registration_tests.rs gains one case its description does not list. All are deferred to the description-only successor named at inventory97, 101, 102, 105 and 110.

## Tests

16 new tests, on scratch homes with a creator-published P0, writers over 462's signed test trees, and other holders simulated by `flock`.

**operation_handoff_tests.rs (11):**
- **A fresh registration, APPEND-WRITE:** the fence is released and `writer.lease` is held while `readers.lease` stays SH-free. The INIT floor, the created carrier and its `COMMITTED 0` witness are present. The binding equals the row's N and the endpoint's S, G and K. Then `end` leaves the floor Unchanged and nothing locked.
- **An Eligible root, EXCLUSIVE:** an `RA` append leaves the floor until the end copies it forward to (1,1); the next writer starts at tail 1.
- **The floor step precedes the lease:** with `readers.lease` held, EXCLUSIVE refuses busy, the INIT floor is written, and there is no carrier.
- **A busy `writer.lease`:** busy, and nothing is written.
- **`floorLost`:** the LedgerCorrupt row before any lease, and nothing is written.
- **A budget cut at the last attempt charge, measured on a twin fixture:** the refusal comes after the start; the lease and the fence are freed; the next writer starts.
- **An uncertain outcome with the fence held elsewhere:** `NotEntered`, the floor untouched; the next writer's floor step copies to (1,1).
- **A busy fence at the end:** S7's bound runs out on a scripted clock and the result is the busy row, with the lease already released and no copy.
- **A closed attempt ledger:** `NotEntered` with no walk, while the fence is held elsewhere; the next writer copies forward.
- **A moved N at the end:** required-files-changed, and the fence is released.
- **The source pin** on the location constructor.

**carrier_operation_tests.rs (4):**
- an INIT step, then creation, start, the end copy before and after an append, and the next step and start;
- `InitPending` resuming creation;
- a skipped step with a then-free lease refusing busy, writing nothing;
- the end copy skipped under a held lease.

**first_registration_tests.rs (1):** `Exact` refuses a third entry while `Started` admits it; a non-empty or missing lease refuses under `Started`.

## Checks

- At f1b8321 plus this diff, two full workspace runs: 1435 passed, 0 failed, 3 ignored, both times.
- `cargo clippy --workspace --all-targets --offline --locked -- -D warnings` is clean, and so is `cargo fmt --all -- --check`.
- `rustfmt --check --edition 2024` (for the `include!`d custody files):
  - clean on operation_handoff.rs, operation_handoff_tests.rs, first_registration.rs, first_registration_tests.rs and namespace_lease.rs;
  - ordinary_writer.rs has the base's two import-order deltas and no more;
  - installation_admission.rs, installation_session.rs and read_premise.rs are unchanged from their base deltas.
- `check_package_edges --lane host` against v111 passes; security's edges stay evaluator, identity and platform.
- verify_scratch (v111 appended over the real lock at f1b8321) passes: 74 inventory successors, 72 contract successors, 16 inheritance rows, v111 selected.
- verify_projection against the real lock: 16 rows, 83 corruptions refused.
- `build_v111.py` reruns produce the same bytes.
- `~/Library/Application Support/OpenSIP` is absent.

## Decide

- Does X2e implement item 7a exactly?
  - the join with X3a's endpoint from the same gate;
  - owners moved, never copied;
  - X3b's carrier start after the transfer and before the release;
  - the fence released only then;
  - no promotion, reopening or backward fence;
  - the floor step at item 7's lease-free point, outside 7a, with no project lock.
- Does X3b-3 compose X3b r10 exactly?
  - the floor step's observation confirmed by the start;
  - INIT creation under the lease;
  - no floor write under any lease;
  - the end step after the lease's release, under a retaken fence, with nothing at all after an uncertain outcome or on a closed attempt ledger.
- Is the X2d judgment call 5 resolution sound?
- Is `ProjectOperation` what X3d-1 can consume (with X4a's guard to come)?
- Rule on the judgment calls, in particular 1, 2, 5, 6, 7 and 8.
- Is v111 right on v112?
- Is anything else wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": the sha256 of `operation-handoff-x2e-inventory-v111-subject.json` (lead's value `df4c25af4ee222d99af284c156a6ca37d8a34f432eb4a58b5f549df67486f7e9`);
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes and sha256 of v111, parent (the v112 pin), successorRecord (the pin of `operation-handoff-x2e-inventory-v111/successor.json`)}.

Write REVIEW.md and review.json. Do not commit.
