# Review: ordinary writer X1a r1

Verdict: ACCEPT-UNIT.

Worktree `/Users/sb/code/opensip-ai/opensip-x1a` is `fdbedf4acc7ef57fb71eed424c3b08fa2af7fe98` plus four files. `product.diff` is 27399 bytes, sha256 `7aa3b824d4c221a069f80fa591beff38ee31cc5e428541af28f36908f1464d81`. The four product pins match hashes.txt. The real OpenSIP support directory is absent. Law X1 r1 is the accepted proposal.

## Items 1 to 7

`PlatformReceipt<P: Purpose>` is the one private receipt. `Purpose` is sealed, and `Read` and `Write` are its only implementors. `ReadPremiseReceipt` is `PlatformReceipt<Read>`. `WritePlatformReceipt` is `PlatformReceipt<Write>`. `PhantomData<fn() -> P>` keeps the purposes distinct. There is no `Clone` and no serialized form. `produce_for::<P>` is the one composition: the attempt, `observe_actor`, `produce_initial_core` and `produce_initial_platform`, with the same lineage check 458c-a used. `produce_read_platform` and `produce_on` return `PlatformReceipt<Read>`. `produce_write_platform` returns `PlatformReceipt<Write>`. The attempt stays inside the receipt.

`qualification` is an inherent method on each concrete receipt. `PlatformReceipt<Read>` returns `&impl ReadPremiseQualification` and still has `split`. `PlatformReceipt<Write>` returns `&impl DurableBarrierQualification`. The generic impl has `recheck` only. `DurableBarrierQualification` is unchanged: barrier policy, the H-filesystem check, and the omission premise, implemented only by `InitialPlatform`. `ReadPremiseQualification` is the same sole implementor. The platform field is private, so a receipt exposes the platform only through its own opaque lending.

`admit_ordinary_writer` follows item 2. `produce_write_platform` runs first, so a development build ends at `CORE.NO_EMBEDDED_RELEASE` before a path is opened. `admit_with` then rechecks the receipt, calls `DurableWriteGate::begin` and `admit(receipt.qualification())`, and rechecks again. `begin` builds `WorkLedger::new()` on `GATE_ALLOCATED`. The receipt's rechecks charge the attempt. A step 2 error returns before `begin`. A step 4 error calls `installation.release()` and returns the recheck row, so the writer does not receive the admission. Success is `OrdinaryWriteAdmission { installation, receipt }` with `installation()`, `recheck()` and `release()`. `release` maps an unlock failure through `gate_refusal` of `IoFailure::Lock`, which is the host I/O row. There is no store, trust, project, id, grant or commit method, and no conversion into a read session.

Absent I is `GateRefusal::Absent`, mapped to `INSTALLATION.NOT_INITIALIZED`. The absent-home test leaves the scratch home empty. A file at `Library` is a different row, and the bytes stay. No command is wired: the only `custody.rs` change is the macOS module include. `run_initial_creator` is untouched. A second `begin` of the attempt or the gate is `AttemptError::AlreadyAllocated` or `GateRefusal::Latched`, both `Invariant`.

## Can a Read receipt reach the gate, or a Write receipt reach the session?

No. The separation is compiler-enforced.

`InstallationObservation::retain`, `observe_with`, `installation_read` and `installation_doctor` take `ReadPremiseReceipt`. `admit_with` takes `WritePlatformReceipt`. `DurableWriteGate::admit` takes `&impl DurableBarrierQualification`. That opaque type is the return of `PlatformReceipt<Write>::qualification` only. `PlatformReceipt<Read>::qualification` returns `&impl ReadPremiseQualification`, and that trait is not the barrier trait. The two marker traits are the probes: `LendsReadPremise` is implemented for `PlatformReceipt<Read>` and `LendsBarrier` for `PlatformReceipt<Write>`. They do not grant the lending. The lending methods are inherent on the concrete types, so implementing the wrong marker would not add the other `qualification`. The const probes fail if a marker is attached to the wrong receipt. The source pin requires exactly two `fn qualification(` in `read_premise.rs`, each naming only its own trait, no `qualification` on the generic impl, and no `From` or `Into` there, and it requires each sealed-trait impl in the three scanned files to name `InitialPlatform`. rustdoc cannot name these `pub(crate)` items, so this pin is the check the law allowed. I searched the security crate: the only implementors are the two `InitialPlatform` impls.

## Judgment calls

1. The marker probes plus the source pin match the types above. The compiler enforcement is the concrete receipts, the opaque lendings, and the session and gate signatures. Accepted.
2. On a failed second recheck, `let _ = installation.release()` drops the unlock error and returns the recheck row. `FileLock::release` unlocks and closes the descriptor. Item 2 requires the recheck's item 6 row to stay the cause. Accepted.
3. The step 2 and step 4 tests pass a scripted closure through `admit_with`, which is the production composition. Production `admit_ordinary_writer` passes `WritePlatformReceipt::recheck`. The step 4 test sees the fence held on the second call, gets `PlatformUnqualified` back, and finds the fence free afterward. A real recheck failure uses that same arm. Accepted.
4. `read_premise.rs`'s effective description is 461b's override, carried by value. It still says the receipt lends only `ReadPremiseQualification` and names no barrier policy. The file now also lends `DurableBarrierQualification` for `Write`. Law X1 item 8 is the description-only successor for that staleness, and the v81 README names X1b as that successor. Deferring it is what the accepted law says. Accepted.

## Inventory v81

v81 is 751 files: v80's 749 rows carried by value, plus `ordinary_writer.rs` and `ordinary_writer_tests.rs` inserted at indexes 250 and 251. Packages, pending decisions and the schema match v80. The standing sentence is the ordinary-writer proposal. `custody.rs` keeps its historical description, which still describes that file. The two new descriptions match the code: the admission order, the grant, the absence row, the 468c maps, and the scratch-home tests including the purpose pin.

The projection has 16 rows: the eight rows inherited through v80 and 461b's eight overrides. Parent pointers match v80. Candidate pointers match v81, shifted by two from `read_premise.rs` onward and unshifted before the insert. Each `before` equals the v80 description. I ran `verify_projection.py`: 16 rows, positive pass, 83 corruptions refused. I ran `evidence/verify_scratch.py`: passed, selected inventory v81, 16 inheritance rows, 56 inventory successors and 70 contract successors.

## What I ran

`cargo test --locked --offline -p opensip-security --lib ordinary_writer::` : 11 passed. `read_premise::` : 7 passed. `cargo clippy --locked --offline -p opensip-security --lib -- -D warnings` finished clean. I did not replay the workspace suite. No product cargo was run outside this worktree.
