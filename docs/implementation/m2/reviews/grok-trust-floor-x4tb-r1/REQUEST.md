Grok review: X4T-a2 and X4T-b, implemented together as one unit: the `accepted.by` load by reference, the fenced first read's S4 write-ahead floor publication, the retained `state.v1` owner and its advance, and the handoff rollback check (law X4T r9 items 1, 2, 7, 8, 11 and 12), with inventory v106. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-trust-floor-x4tb-r1. If you build or test, use a CARGO_TARGET_DIR under that directory. Run git only read-only, and only against the worktree below.

Law: `docs/implementation/m2/trust-admission-x4t/PROPOSAL.md` r9 (accepted; the file adds only the "r9 ACCEPTED" note to the reviewed bytes). X4T-a (items 1 to 6, 8 to 11) is integrated at product fc7dce7, and X4T-0 at 5b5f04c. Also read X4B r4 (`trust-bootstrap-x4b/PROPOSAL.md`, accepted), whose X4B-a uses this unit's publication protocol (its items 5 and 6), and X2 r5's registry replacement rule (item 6), which item 7 follows for the retained owner.

## Subject

Pins are in hashes.txt.
- **Product:** the worktree `/Users/sb/code/opensip-ai/opensip-x4tb`, based on b642c45 (X12a integrated, inventory v104 selected). Save `git -C <worktree> diff` (the two new files are intent-to-add) as product.diff and report its sha256. Lead's value: 37263cd87d47fc8fd2127ca7a7ee354a28b8e5a935819a9dd46d03d830cfc891, 99728 bytes, 13 files, 1943 insertions and 84 deletions.
- **Arch:** v106 (parent v104): `trust-floor-x4tb-inventory-v106-subject.json` and `trust-floor-x4tb-inventory-v106/`. X2c's v105 is in flight on the same parent, v104.

## What it does

### X4T-a2: `accepted.by` by reference (items 1, 2 and 11)

`current_trust_admission.rs` `check_accepted_by` now takes the budget, the descriptor and the store.
- An `accepted.by` that names an event `bind_trace` loaded is checked there, with no read.
- Otherwise exactly that event is opened by reference: `Budget::load_at(Collection::Events, by, None, store)`, then admitted as `TrustEventV1`. It must be:
  - a `role-event` of that role, with outcome `accepted`;
  - in this store: the event's `store` and the reference's `storeInstanceId` are both S;
  - at the reference's sequence, and lower than the sequence of the current descriptor's first listed event (for an empty list: no higher than `eventHead`'s).
- The read is counted (`MAX_ACCEPTED_BY_READS = 6`). The event's own `previous` is never followed, and `history` is never walked.
- A missing event, another role's, a refused or non-role event, another store's, or one that is not earlier than the current publication is the incomplete row. A ledger limit is the budget row.

### Rollback checks 1 and 2 (item 7, r8 and r9)

The view now carries the capsule's `Floors`: F, L, root, revocation and index snapshot versions. F and L are seconds, and a field is `None` where the clock phase has none.
- `open_heads` keeps the time-evidence value it already loads.
- `check_evidence_floors` runs on every read, and only for an `s4-evaluation` input; an S4.5 epoch input is not compared.
  - **Check 1:** against the evidence's `beforeClock`. A retained clock compares all five floors, an evaluated clock compares F and L, and an unevaluated clock compares nothing.
  - **Check 2:** F must be at least the evidence's `observation.wall`.
- A fenced refusal is the new `TrustRow::Rollback` (`CONFIG.CUSTODY_REFUSED`, subject `trust-rollback`). On a reread, the same `TrustRefusal` goes back to X4's callback (item 9).

### X4T-b (`trust/floor_publication.rs`, a macOS child of `current_trust_admission`)

**The retained owner (items 7 and 8, r8).**
- `RetainedCurrentTrust::bind(i, uid, expected_store, raw, sample, work)` takes the session's one read: its bytes and its custody sample.
  - The gate now keeps those bytes: `CurrentStore.raw`, from the same read, with no new read. `DurableInstallation::current_trust()` lends I, the uid, the bytes and the `RequiredFile`.
  - `bind` decodes the capsule from those bytes. It opens `trust/stores/S` through I, judging each directory private. It then rechecks `state.v1` under it by custody's own `private_file` judgment (`observe_private_file`), against the sample.
- `recheck` compares the full sample. Any change is the new `TrustRow::RequiredFilesChanged` (`CONFIG.CUSTODY_REFUSED`, subject `required-files-changed`).

**`fenced_first_read(work, fence, owner, inputs, invocation)`.** It runs only in fenced mode, with a fence recheck and an owner recheck first. Then:
1. X4T-a's `admit_current_trust` runs over the owner's capsule, with a `NativeStore` on the held fence, charged to the gate ledger through a borrowed budget.
2. **Check 3 (r9):** the view's floors must not be below any floors in `owner.prior`. A predecessor's floors are pushed there on each advance only when its clock is evaluated or retained, so X4B's acceptance over P0 passes.
3. Unless the read is report-only, `needs_write` decides whether to publish: F rises, L advances, or the anchor is rewritten to a different value. If so, it builds the floor publication, verifies it and publishes it.

**`build_floor_publication`.** It writes, in dependency order:
- the before image (the owner's exact bytes, as a record);
- the `S4EvaluationInputV2` from `proposed_time_input::assemble` (judgment call 3);
- a `TrustAdmissionInputV1` (`continue`, `installed-component`, the running core closure) and its `host-trust-admission` `OperationInputV1`;
- the `ClockWriteEventV1` (retained to retained, source `s4`, at the next sequence after `eventHead`);
- the descriptor in `by-predecessor/<sha256(before)>`, with `nativeBefore` the direct predecessor;
- the successor capsule.

In the capsule, only F (:= tEval), the anchor (when S4 rewrote it), L and the time evidence (only when L advances) change in the clock, along with the revision, `previous`, `eventHead` and `publication`. Every role, head, history, counter and expiry field is unchanged. Before any effect, `successor_record_bindings::bind` (against the actual before) and `current_record_bindings::bind` (which runs `bind_trace`) check exactly these bytes in memory.

**`publish(fence, owner, files, capsule_raw, work)`.** This is the shared protocol, used by item 7 and, later, X4B-a.
1. Fence recheck and owner recheck.
2. One `work.effect` reserves every write and the post-publication confirmation before the first effect. Inside, two `prepaid` allowances are drawn:
   - **Writes.** For each dependency:
     - its parents are opened and judged private, and only `publications/by-predecessor` and its bucket may be created (private create with both barriers);
     - an absence probe follows;
     - an absent name gets a private create, `write_new_regular_accounted` (`F_FULLFSYNC`) and the directory barrier;
     - a present name is admitted only if it is private and its capped reread equals the bytes. A foreign file is the incomplete row.

     Then `state.v1` goes through X3b's `publish_private_file` (exclusive temporary name, write and `F_FULLFSYNC`, rename, directory barrier, reopen and confirm).
   - **Confirmation.** The new `state.v1` is judged and sampled, reread through an exact-length cap, and sampled again. Both samples must be equal and the bytes must match.
3. The owner advances: bytes and capsule from the reread, the post-rename sample, the predecessor's floors added to `prior`, and a `ConfirmedCurrent` minted (only `publish` can mint one).
4. A fence recheck and an owner recheck close the protocol.

Failure rows:
- before the rename: host I/O, with the pointer unchanged and the records unreferenced;
- from the rename on: host I/O, durability-undetermined (the cause names the protocol step);
- ledger limits: the budget row;
- a missing parent or foreign record: incomplete.

Nothing is retried or deleted.

**The gate's advance.** `DurableInstallation::advance_current(&ConfirmedCurrent)` is the only change of `state.v1`'s `RequiredFile`. It requires the same path, and that the reread bytes decode to the same (S, G, K). It replaces the sample and the endpoint's bytes.

**Supporting edits.**
- `journal_store.rs` re-exports `carrier_floor::publish_private_file` (judgment call 2).
- `installation_session.rs`: `decode_current` takes the read's bytes by value.
- Re-exports in `ordinary_targets.rs`, `root_payload.rs` and `trust.rs`: `ConfirmedCurrent` crate-wide, and the owner and `publish` only under `cfg(all(test, macos))`, for the gate's test.
- `accepted_store_fixture_tests.rs`: its source pin admits `floor_publication_tests.rs` under the same `cfg(test)` include check as X4T-a's tests.

## Judgment calls: please rule on each

1. **The floor publication's operation (gap 2).** It is `host-trust-admission` with `TrustAdmissionInputV1 {purpose: continue, surface: installed-component, closure: the running core closure}`. Of the fourteen existing actions, this is the one that names an operation's own trust admission. `refresh`, `ordinary-import` and `bootstrap` require a payload closure the floor write doesn't have. No definition is added, and `trust_input_bindings::descriptor` accepts it. The admission binder's install/continue contract (owned role events plus `EV-CLOCK`, each citing a clock-write by this operation) is untouched: this publication has no role event.
2. **Reuse of X3b's file protocol (gap 4).** `publish_private_file`'s shape is the same at 9dbefb9 and b642c45, and X3b-2 only added rows to `carrier_floor.rs`. A one-line `pub(crate) use` in `journal_store.rs` reuses it rather than copying it, so the pointer and the carrier floor share one protocol. Its leftover `state.v1.<32 hex>` temporary file is never adopted or deleted (X4B item 6, owner §6). The census scans no `trust/stores/S` names.
3. **The S4 evaluation input.** `proposed_time_input::prepare`'s body moves unchanged into `assemble(proposal, capsule, before, invocation)`, which `prepare` now calls, so one producer assembles every write's input. Its values:
   - authority: `heads.root.admission`;
   - `beforeClock`: the capsule's clock;
   - `beforeImage`: the owner's bytes, written as a record so the reference resolves, as X4T-0 does for P0's image;
   - source: `ordinary` with the closure the evaluation actually used.
4. **Kept or new time evidence.** The event's `timeEvidence` is `{kind: kept}`, with the capsule's `clock.timeEvidence` unchanged, unless L advances. If it does, the evidence is `{kind: new, proof: the evaluation}` and the capsule's evidence is that evaluation. These are `ClockWriteEventV1`'s crossfield and S4's `ProofRetention`. `writes` always lists `evalHighWater`; it lists `anchor` when S4 rewrote the anchor and `lastAccepted` when L advances.
5. **When to write.** Item 7 says "tEval exceeds F, or L or the anchor advance". The anchor test is a value change. S4 step 5 rewrites the anchor whenever continuity allows, so in practice every fenced first read on a new clock sample publishes. A confirming admission on the same sample writes nothing, as X4B item 1 requires.
6. **Verifiers before any effect.** As with 467's P0 builder, the existing successor and current binders check the exact bytes in memory, charged to the gate ledger.
7. **Existing records and directories.** A content-addressed name that is already present is admitted when it is private and its bytes are equal (X4B item 6). An absence probe comes first, because a failed exclusive create would latch the ledger. Only the `by-predecessor` bucket and its parent may be created. Every other missing collection directory means an incomplete installation.
8. **Rows.** Two new `TrustRow` variants for subjects item 7 already names, on the existing `CONFIG.CUSTODY_REFUSED` row: `trust-rollback` and `required-files-changed`. No new code.
9. **The retained bytes live in `CurrentStore`.** Both the gate and the read session keep the bytes of their one read. Only the gate has `advance_current`; the read session never publishes.
10. **No production wiring.** `fenced_first_read` and `publish` take `&dyn HeldFence`. No adapter over the gate's `DurableInstallation` is built here, and the gate test uses a test-only one. Wiring is X4a and X4B-b, which is why the owner and `publish` leave their module only under `cfg(test)`.
11. **Costs.** The reservation is the sum of per-file upper bounds from the platform's published cost functions:
    - each parent opened, judged and created;
    - the create path and the existing-record path both counted;
    - the pointer's protocol and the confirmation (two judged samples and the capped reread).

    It is charged in one effect before the first write, and an overrun fails closed (`prepaid`). X4T-a's `MEASURED` and `NATIVE_MEASURED` are unchanged: in X4T-0's store, every acceptance event is in the current chain, so no event is opened by reference. A new pin, `NATIVE_AFTER_FLOOR = (31, 253, 32103)`, measures the native reread after a floor publication, with four events opened by reference, and checks it against `TRUST_VIEW_COST`. Item 13's "constants move by the counted events" applies only when events are out of chain.
12. **A stricter in-chain check.** An in-chain `accepted.by` must now also be an accepted `role-event`, as item 1 r8 states ("an accepted role event of that role"). X4T-0's stores pass.
13. **Stale descriptions.** These go to the D1 description-only successor, as with X3c-2's rows:
    - `current_trust_admission.rs` ("checks each accepted role's accepted.by against the loaded events … writes nothing; the write-ahead floor is X4T-b's");
    - `installation_admission.rs`;
    - `installation_admission_tests.rs`.

    See the v106 README.

## Tests

On ACL-scratch installations (`test_scratch::acl_scratch`, under `<temp>/opensip-test/<pid>-<nanos>`) with X4T-0's signed store under a supplied fence, and on scratch account homes for the gate. No real home is touched; `~/Library/Application Support/OpenSIP` is absent.

**`floor_publication_tests.rs`: 12 tests.**
- **A floor advance.** It is written ahead: F := tEval and the anchor rewritten; L, the time evidence, every counter, expiry, role, head and history field unchanged; revision 3; the before image recorded; one descriptor in the predecessor's bucket; the next event sequence; the owner advanced to the confirmed file, with one prior floor set and the recheck passing.
- **The next invocation.** Its fenced read and the native reread admit the store, with `accepted.by` opened by reference. The pinned cost is within the ceiling.
- **Out-of-chain `accepted.by`.** Four reads for four roles. Each of these refuses as incomplete: another role's event, a missing event, another store's reference, the P0 creation event (earlier but not a role event), and the current chain's clock-write.
- **A confirming admission on the same sample** writes nothing.
- **Report-only and beyond-horizon** reads write nothing, with the same inode and file count.
- **An in-place rewrite** of `state.v1` is `required-files-changed`.
- **Check 3** refuses below this hold's floors. An unevaluated (P0) predecessor has no floors.
- **Checks 1 and 2** over retained, evaluated and unevaluated before-clocks, the evaluation wall, and an S4.5 epoch input (not compared).
- **A whole-file restore** of the older `state.v1` is admitted, and publishes a second descriptor into the same bucket. This pins the stated limit.
- **The protocol** refuses a foreign record before the pointer (same inode), and admits an equal one, then replaces the pointer.
- **A ledger short of the reservation** fails with nothing written.
- **A reread mode** is not a fenced first read.

**`installation_admission_tests.rs`: 1 new test.** On a real scratch P0 through the gate, `publish` with no dependencies gives a new confirmed file. With `advance_current`, the gate's recheck passes and holds the new sample and bytes. Without it, the recheck is `required-files-changed`.

**`current_trust_admission_tests.rs`: 19 tests**, adapted to the new signature, including the stricter in-chain case. **`accepted_store_fixture_tests.rs`: 7 tests**, including the widened source pin.

## Checks

- Full workspace, two runs on b642c45 plus this diff: 1379 passed, 0 failed, 3 ignored each.
- Clippy `--workspace --all-targets -D warnings` and `fmt --check` are clean.
- `check_package_edges --lane host` against v106 passes; no edge is added.
- verify_scratch (v106 appended over the worktree's lock at b642c45) passes: 70 inventory successors, 71 contract successors, 16 inheritance rows, v106 selected.
- verify_projection against the real lock: 16 rows, 83 corruptions refused.
- `build_v106.py` reruns produce the same bytes.

## Decide

- Does the unit implement X4T r9 items 1, 2, 7, 8, 11 and 12 exactly? In particular:
  - the `accepted.by` read bound and its refusals;
  - checks 1 to 3 exactly as stated, with S4.5 and unevaluated predecessors excluded;
  - the write-ahead before the view is returned, under the fence and outside any lease;
  - dependencies before the pointer;
  - the owner advancing only through a confirmed publication, from the reread;
  - nothing else in the capsule changing;
  - no retry or deletion.
- Is the publication protocol fit for X4B-a's use (X4B items 5 and 6)?
- Rule on the judgment calls, in particular 1, 2, 5, 9, 10 and 11.
- Is v106 right on v104?
- Is anything else wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": the sha256 of `trust-floor-x4tb-inventory-v106-subject.json`;
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes, sha256 of v106, parent (the v104 pin), successorRecord}.

Write REVIEW.md and review.json. Do not commit.

**Lead note on ordering.** X2c's inventory105 is in flight on the same parent, v104. If X2c integrates first, `build_v106.py` gets a parent-only rebuild on v105 (one more PRIOR entry), and the rebuilt v106 gets a quick rebase-only recheck. This review judges v106 on v104 as submitted.
