// Law X2 r8 item 7a (unit X2e), composed with law X3b r10 items 1, 3, 3a and
// 4 (unit X3b-3): the checked operation handoff. One owner, on one ordinary
// writer's gate, builds the operation context while the same installation
// fence is held:
// - the selected store endpoint is joined from the gate's one read (X3a r5
//   items 1 and 2);
// - the subject's namespace is admitted (X2d, item 7), with no lock taken;
// - at the lease-free point, with R current and no project lock held, the
//   operation's carrier place is confirmed (`I/trust` and the spelling SQLite
//   opens, which must name the retained N) and X3b's floor step runs, charged
//   to the write receipt's attempt ledger (X3b r10 item 9's operation
//   ledger). X4a's fenced trust admission runs first at this point (X4 r7
//   item 2, X4T r11 item 9), with X4B-b's bootstrap inside it on F absent;
// - the lease is taken (X2d), APPEND-WRITE or EXCLUSIVE;
// - item 7a step 1, the join: the subject, the namespace, the locked
//   carriers and the gate are rechecked, and owner §8's five-field binding
//   is derived from the owners about to move;
// - step 2, the transfer: the owners move out of the fenced gate, never
//   copied;
// - step 3, X3b's carrier start: item 3a's creation when the floor step
//   found INIT, item 4's start against the floor step's observation, and
//   item 6's append lock; then every owner is rechecked once more, with a
//   registered subject's namespace held to the started footprint (the
//   carrier and its witness now stand beside the leases);
// - step 4: only then is the fence released, and the gate's ledger ends.
// Law X4 r7 items 2 and 6 (unit X4a) fill this unit's seams: at the
// lease-free point, before anything else, the operation's one `FinalGate`
// and `FreshnessMonitor` are created and X4T's fenced admission (with its
// write-ahead) runs as the monitor's first read on the gate's ledger; the
// trust store's handles are retained and judged there too. After the
// carrier start, still under the fence, `OperationGuard` is built from them
// and moved into the operation, which starts its observer. `journal` lends
// each journal step X4's checkpoint over the operation's owners.
// The result is `ProjectOperation`. Its end path (X3b r10 item 4, end step)
// releases the lease, and after certain journal outcomes on an open attempt
// ledger retakes the fence by the shared charged walk and bounded wait on
// that ledger, runs X3b-4's rollover when the owner reports the carrier's
// capacity exhausted, copies the floor forward and releases the fence; after
// an uncertain outcome, or on a closed attempt ledger, it does nothing more.
// Every refusal names its row; the public projection is the composition
// owner's. Library only.
use super::first_registration::{
    Footprint, HOST, Owner, PROJECTS, ProjectInputs, ProjectWriteRefusal, ProjectWriteRow,
    RegistrationRefusal, Step, rebind,
};
use super::installation_admission::{
    Account, Chain, ChainPolicy, EndpointValues, GateRefusal, IoFailure, RequiredFile, Walked,
    open_fence, walk_chain,
};
use super::installation_root::{FINAL_NAME, FIXED_ANCESTORS};
use super::installation_routing::gate_refusal;
use super::installation_session::{OsClock, WaitClock, wait};
use super::namespace_lease::{
    self, Failure as NamespaceFailure, Held, HeldLease, LeaseMode, Namespace, NamespaceParts,
    NamespaceRefusal, NamespaceSubject, WriterLease, recheck_binding, recheck_directories,
    recheck_subject, required_directory,
};
use super::operation_guard::{
    Checkpoint, GuardSeam, GuardStart, LeaseFree, MonitorClock, OperationGuard, StopCause,
    trust_termination,
};
use super::ordinary_writer::{GateStep, OrdinaryWriteAdmission};
use super::read_premise::WritePlatformReceipt;
use super::store_endpoint::SelectedStoreEndpoint;
use crate::InstallationTermination as T;
use crate::journal_store::{
    CapacityExhaustion, CarrierLocation, CarrierRefusal, CarrierRefusalRow as CarrierRow,
    EndOutcome, ExhaustedEnd, OperationCarrier, OperationFloor, RolloverOutcome,
    operation_end_after_exhaustion, operation_end_copy, operation_floor_step, operation_start,
};
use crate::trust::{
    AdmittedCurrentTrust, RetainedTrustHandles, StateWriter, TrustInvocation, TrustRefusal,
    fenced_operation_read,
};
use opensip_identity::ProjectRegistryEntry;
use opensip_platform::{DescriptorFilesystem, RetainedDirectory, WorkCost, WorkFailure, WorkScope};
use std::io;
use std::os::unix::fs::MetadataExt;
use std::path::{Path, PathBuf};

/// The carrier floor's parent under I (law X3b item 2).
const TRUST: &str = "trust";
/// One status read of a path, no-follow at its last component.
const PATH_STATUS: WorkCost = WorkCost {
    objects: 1,
    edges: 1,
    bytes: 256,
};

// ------------------------------------------------------------- refusals

/// Why the handoff refused. Each has one row (`row`). Any refusal spends the
/// gate, releases every project lock already taken and then the fence.
#[derive(Debug)]
pub(crate) enum OperationRefusal {
    /// X3a's endpoint join (law X3a r5 item 5), as 468c maps it.
    Endpoint(T),
    /// X2's own steps on the gate: namespace admission, the lease, the
    /// rechecks, the gate's and the receipt's (law X2 item 8).
    Project(ProjectWriteRefusal),
    /// X3b's floor step, creation or start on the attempt ledger (X3b item
    /// 8's carrier rows; the budget row for a ledger failure).
    Carrier(WorkFailure<CarrierRefusal>),
    /// The fence's release failed after the carrier start: the host I/O row.
    Release(T),
    /// X4T's fenced admission at the lease-free point refused (law X4T r9
    /// item 10's rows, unit X4a).
    Trust(TrustRefusal),
    /// The operation's monitor stopped at its first read (law X4 r7 item 8's
    /// fail-stop row).
    Live(StopCause),
    /// The observer thread could not be started: the host I/O row.
    Observer(io::Error),
}
/// The row a handoff or end-path refusal names, for the composition owner.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) enum OperationRow {
    /// 468 item 6's row, through 468c's maps.
    Installation(T),
    /// Law X2 item 8's row, as X2c and X2d name it.
    Project(ProjectWriteRow),
    /// Law X3b item 8's row.
    Carrier(CarrierRow),
    /// `WORK.BUDGET_EXHAUSTED`.
    BudgetExhausted,
}
fn carrier_row(failure: &WorkFailure<CarrierRefusal>) -> OperationRow {
    match failure {
        WorkFailure::Budget(_) => OperationRow::BudgetExhausted,
        WorkFailure::Operation(refusal) => OperationRow::Carrier(refusal.row()),
    }
}
impl OperationRefusal {
    pub(crate) fn row(&self) -> OperationRow {
        match self {
            Self::Endpoint(row) | Self::Release(row) => OperationRow::Installation(row.clone()),
            Self::Project(refusal) => OperationRow::Project(refusal.row()),
            Self::Carrier(failure) => carrier_row(failure),
            Self::Trust(refusal) => OperationRow::Installation(trust_termination(&refusal.row)),
            Self::Live(cause) => cause.row(),
            Self::Observer(_) => OperationRow::Installation(T::HostIo),
        }
    }
}
fn released(error: io::Error) -> T {
    gate_refusal(&GateRefusal::Io(IoFailure::Lock(error)))
}

// ------------------------------------------------------------ the binding

/// Owner §8's five-field binding `{schemaVersion: 1, namespaceId: N,
/// storeInstanceId: S, storeGeneration: G, stateSchema: K}`, derived in the
/// handoff from the moved owners only (X3b r10 item 1): N from the current
/// registry owner's ACTIVE row, S from the opened endpoint's marker, G and K
/// from the admitted selection pair. Values only; not Clone, no serialized
/// form, and no digest (its consumers, X3c and X3d, own that).
#[derive(Debug, PartialEq, Eq)]
pub(crate) struct OperationBinding {
    namespace_id: String,
    store_instance: String,
    store_generation: i64,
    state_schema: u8,
}
impl OperationBinding {
    pub(crate) const SCHEMA_VERSION: u8 = 1;
    pub(crate) fn namespace_id(&self) -> &str {
        &self.namespace_id
    }
    pub(crate) fn store_instance(&self) -> &str {
        &self.store_instance
    }
    pub(crate) fn store_generation(&self) -> i64 {
        self.store_generation
    }
    pub(crate) fn state_schema(&self) -> u8 {
        self.state_schema
    }
}
/// The binding from N (the ACTIVE row's, which must name the confirmed
/// namespace) and the gate's admitted endpoint, charged as one small object.
fn derive_binding(
    row: &ProjectRegistryEntry,
    namespace: &Namespace,
    held: &Held<'_, '_>,
    work: &mut WorkScope<'_>,
) -> Result<OperationBinding, NamespaceFailure> {
    let Some(durable) = held.durable else {
        return Err(WorkFailure::Operation(NamespaceRefusal::Invariant(
            "binding-without-gate",
        )));
    };
    let endpoint = SelectedStoreEndpoint::new(durable.endpoint());
    let cost = WorkCost {
        objects: 1,
        edges: 4,
        bytes: row.namespace_id().len() + endpoint.store_instance().len() + 16,
    };
    work.run(cost, |_| {
        if row.namespace_id() != namespace.id {
            return Err(WorkFailure::Operation(NamespaceRefusal::Invariant(
                "binding-namespace",
            )));
        }
        Ok(OperationBinding {
            namespace_id: row.namespace_id().to_owned(),
            store_instance: endpoint.store_instance().to_owned(),
            store_generation: endpoint.store_generation(),
            state_schema: endpoint.state_schema(),
        })
    })
}

// ---------------------------------------------------------- carrier place

/// Where the operation's carrier and floor live (X3b item 2): `I/trust`
/// confirmed under the fence, the admitted N with the spelling SQLite opens
/// (confirmed to name that same N), N's id and the invoking user. Built only
/// here, from admitted owners; `CarrierLocation::admitted` is its one
/// consumer (X3b item 11's production constructor).
pub(crate) struct CarrierPlace<'a> {
    trust: &'a RetainedDirectory,
    namespace: &'a RetainedDirectory,
    namespace_path: &'a Path,
    namespace_id: &'a str,
    uid: u32,
}
impl<'a> CarrierPlace<'a> {
    pub(crate) fn trust(&self) -> &'a RetainedDirectory {
        self.trust
    }
    pub(crate) fn namespace(&self) -> &'a RetainedDirectory {
        self.namespace
    }
    pub(crate) fn namespace_path(&self) -> &'a Path {
        self.namespace_path
    }
    pub(crate) fn namespace_id(&self) -> &'a str {
        self.namespace_id
    }
    pub(crate) fn uid(&self) -> u32 {
        self.uid
    }
}
/// N's absolute spelling, from H's spelling exactly as the gate walked it:
/// `H/Library/Application Support/OpenSIP/<I>/host/projects/N`. It is
/// admitted only if a no-follow status of it finds the retained N (same
/// device and inode); SQLite's path opens confirm the file again by identity.
pub(super) fn namespace_spelling(
    home: &Path,
    id: &str,
    namespace: &RetainedDirectory,
    work: &mut WorkScope<'_>,
) -> Result<PathBuf, NamespaceFailure> {
    let path = FIXED_ANCESTORS
        .iter()
        .chain([FINAL_NAME, HOST, PROJECTS, id].iter())
        .fold(home.to_path_buf(), |path, name| path.join(name));
    let changed = || {
        WorkFailure::Operation(NamespaceRefusal::Owner(RegistrationRefusal::Changed(
            Owner::Namespace,
        )))
    };
    let io = |error| {
        WorkFailure::Operation(NamespaceRefusal::Owner(RegistrationRefusal::Io(
            Step::Handoff,
            Owner::Namespace,
            error,
        )))
    };
    let cost = WorkCost {
        bytes: path.as_os_str().len(),
        ..PATH_STATUS
    };
    work.run(cost, |_| {
        let named = match std::fs::symlink_metadata(&path) {
            Ok(named) => named,
            Err(error) if error.kind() == io::ErrorKind::NotFound => return Err(changed()),
            Err(error) => return Err(io(error)),
        };
        let retained = namespace.as_file().metadata().map_err(io)?;
        if !named.file_type().is_dir()
            || (named.dev(), named.ino()) != (retained.dev(), retained.ino())
        {
            return Err(changed());
        }
        Ok(path)
    })
}

// ------------------------------------------------------------ the operation

/// What an operation's journal ended with, as its owner (X3d's `finish`)
/// reports it. `Uncertain` is any durability-undetermined journal outcome of
/// the operation (X3b r10 item 5). `Exhausted` is a certain operation whose
/// outcome was X3d's `CarrierCapacityExhausted`, with the released
/// operation's `operationRef` (X3b r10 items 4 step 3 and 13).
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) enum JournalOutcome {
    Certain,
    Uncertain,
    Exhausted {
        exhaustion: CapacityExhaustion,
        operation_ref: String,
    },
}

/// Law X2 item 7a's operation context: private, not Clone, no serialized
/// form, built only by `begin` from owners moved out of one ordinary
/// writer's fenced gate. The fence is released; the lease is held until the
/// end path or a drop releases it. It holds:
/// - the started carrier with its append lock and start tail (X3b);
/// - the held lease and its mode (X2d);
/// - owner §8's binding, and the immutable ACTIVE row snapshot;
/// - the original project root, `.opensip`, marker and namespace owners, as
///   the subject's admission or registration retained them;
/// - the confirmed `I/trust` and N's spelling (the carrier place);
/// - the store endpoint's decoded values and the required files' full
///   samples (the endpoint and lineage owners, law X3a item 2), with the
///   retained chain to I and the account (no fence lock);
/// - the write receipt, whose attempt ledger is the operation ledger.
///
/// The registry and selection captures it carries are provenance after the
/// release (item 7a): nothing here rechecks them. It also holds X4's
/// `OperationGuard` (X4 r7 item 6): the monitor history, the gate, the start
/// view, the retained trust handles and the running observer. X3d's
/// `CommitSession` consumes this.
///
/// Law X3d r6 item 2 (unit X3d-1): exported, because the public
/// `CommitSession::open` takes it. Nothing outside security can build,
/// default, clone, serialize or read one (law X8 r3 groups D, E, F and G).
pub struct ProjectOperation {
    // Declaration order is drop order: the guard (its observer stops), the
    // append lock, then the lease (`readers.lease`, then `writer.lease`),
    // then the rest.
    guard: OperationGuard,
    carrier: OperationCarrier,
    lease: HeldLease,
    mode: LeaseMode,
    binding: OperationBinding,
    row: ProjectRegistryEntry,
    subject: NamespaceSubject,
    namespace: Namespace,
    namespace_path: PathBuf,
    trust: RetainedDirectory,
    endpoint: EndpointValues,
    required: Vec<RequiredFile>,
    chain: Chain,
    account: Account,
    receipt: WritePlatformReceipt,
}
impl std::fmt::Debug for ProjectOperation {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("ProjectOperation")
            .field("binding", &self.binding)
            .field("mode", &self.mode)
            .field("carrier", &self.carrier)
            .finish_non_exhaustive()
    }
}
impl ProjectOperation {
    /// Owner §8's binding.
    pub(crate) fn binding(&self) -> &OperationBinding {
        &self.binding
    }
    /// The ACTIVE row snapshot of the registry owner current at the handoff.
    pub(crate) fn row(&self) -> &ProjectRegistryEntry {
        &self.row
    }
    pub(crate) fn mode(&self) -> LeaseMode {
        self.mode
    }
    /// The root admission or the registered project, as moved.
    pub(crate) fn subject(&self) -> &NamespaceSubject {
        &self.subject
    }
    /// The discovery walk's view of the subject's root (M3-B r5 item 12;
    /// unit B2-b3a, LD-B2B3-1), after the handoff released the fence: the
    /// subject chain's retained root, and the write receipt's omission
    /// premise and check that a filesystem is H's. Nothing else.
    pub(crate) fn discovery_root(&self) -> super::project_chain::DiscoveryRoot<'_> {
        let chain = match &self.subject {
            NamespaceSubject::Eligible { admission, .. } => admission.chain(),
            NamespaceSubject::Registered(registered) => registered.chain(),
        };
        super::project_chain::DiscoveryRoot::lend_write(chain, self.receipt.qualification())
    }
    /// The selected store endpoint, from the gate's one read.
    pub(crate) fn endpoint(&self) -> SelectedStoreEndpoint<'_> {
        SelectedStoreEndpoint::new(&self.endpoint)
    }
    /// The endpoint and lineage owners' full samples (law X3a item 2).
    pub(crate) fn required(&self) -> &[RequiredFile] {
        &self.required
    }
    /// The write receipt's selected core closure and state writer.
    pub(crate) fn selected_core(&self) -> (&str, StateWriter) {
        self.receipt.selected_core()
    }
    /// Law X3d r8 item 13: the write receipt's core evaluator closure
    /// (contract successor EC1). A value only, beside `selected_core`.
    pub(crate) fn core_evaluator_closure(&self) -> &str {
        self.receipt.core_evaluator_closure()
    }
    /// Law X3d r8 item 13: the shared test-support read (`CommitSession`'s
    /// accessor) through the write receipt. On X8 r3 item 4b's site list.
    #[cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))]
    pub(crate) fn core_evaluator_closure_preimages(
        &self,
    ) -> (
        opensip_identity::JsonValue,
        Vec<u8>,
        std::collections::BTreeMap<String, Vec<u8>>,
    ) {
        self.receipt.core_evaluator_closure_preimages()
    }
    /// The started carrier: its start tail and append lock.
    pub(crate) fn carrier(&self) -> &OperationCarrier {
        &self.carrier
    }
    /// X4's live guard: the gate's state, the stop cause and the drift.
    pub(crate) fn guard(&self) -> &OperationGuard {
        &self.guard
    }
    #[cfg(test)]
    pub(super) fn lease_mut(&mut self) -> &mut HeldLease {
        &mut self.lease
    }
    /// Law X3d r6 item 8 (unit X3d-1): one charged step on the attempt
    /// ledger with no checkpoint, for the commit session's own work and the
    /// work storage does through it (draws, preflight, attempt admission,
    /// objects, the evidence ledger's level 3). Refused `Closed` once the
    /// ledger is latched; any failure latches it.
    pub(crate) fn charge<R, E>(
        &mut self,
        action: impl FnOnce(&mut WorkScope<'_>) -> Result<R, WorkFailure<E>>,
    ) -> Result<R, WorkFailure<E>> {
        self.receipt.charge(|_, work| action(work))
    }
    /// Law X3d r6 item 3 step 0 (unit X3d-1): the attempt ledger's one
    /// settlement reserve, on the commit session's end-path step's way only.
    pub(crate) fn reserve_end_path_settlement(
        &mut self,
        cost: WorkCost,
    ) -> Result<opensip_platform::SettlementReserve, opensip_platform::WorkBudgetError> {
        self.receipt.reserve_end_path_settlement(cost)
    }
    /// Law X3d r6 items 7 and 8 (unit X3d-1): spend the reserve once, on
    /// `StoppedSession::finish`'s way only, with the operation's carrier
    /// location and started carrier, as `journal` lends them but with no
    /// checkpoint (the end-path appends are neither a brokered effect nor a
    /// commit admission, X4 r7 item 3). Admitted on a closed attempt ledger.
    pub(crate) fn settle_end_path<R, E>(
        &mut self,
        reserve: opensip_platform::SettlementReserve,
        action: impl FnOnce(
            &CarrierLocation<'_>,
            &OperationCarrier,
            &mut WorkScope<'_>,
        ) -> Result<R, WorkFailure<E>>,
    ) -> Result<R, WorkFailure<E>> {
        let Self {
            carrier,
            namespace,
            namespace_path,
            trust,
            account,
            receipt,
            ..
        } = self;
        let place = CarrierPlace {
            trust,
            namespace: &namespace.directory,
            namespace_path,
            namespace_id: &namespace.id,
            uid: account.uid(),
        };
        let location = CarrierLocation::admitted(&place);
        let carrier = &*carrier;
        receipt.settle_end_path(reserve, |work| action(&location, carrier, work))
    }
    /// Test seam (unit X3d-1): the started carrier, to install an append
    /// hook on its lock.
    #[cfg(test)]
    pub(super) fn carrier_mut(&mut self) -> &mut OperationCarrier {
        &mut self.carrier
    }
    /// Whether the attempt ledger is closed (the end step is then not
    /// entered).
    pub(crate) fn attempt_closed(&self) -> bool {
        self.receipt.is_closed()
    }
    #[cfg(test)]
    fn attempt_used(&self) -> WorkCost {
        self.receipt.attempt_used()
    }
    /// One charged journal step on the attempt ledger, with the operation's
    /// carrier location, started carrier and X4's checkpoint (X3d's appends
    /// and admissions). The checkpoint borrows the guard and every owner of
    /// X4 r7 item 4's set, and runs on this same charge; it needs the
    /// action's level-4 borrow. The lease is held; the fence is not.
    pub(crate) fn journal<R, E>(
        &mut self,
        action: impl FnOnce(
            &CarrierLocation<'_>,
            &OperationCarrier,
            &Checkpoint<'_>,
            &mut WorkScope<'_>,
        ) -> Result<R, WorkFailure<E>>,
    ) -> Result<R, WorkFailure<E>> {
        let Self {
            guard,
            carrier,
            lease,
            binding,
            row,
            subject,
            namespace,
            namespace_path,
            trust,
            endpoint,
            required,
            chain,
            account,
            receipt,
            ..
        } = self;
        let uid = account.uid();
        let place = CarrierPlace {
            trust,
            namespace: &namespace.directory,
            namespace_path,
            namespace_id: &namespace.id,
            uid,
        };
        let location = CarrierLocation::admitted(&place);
        let carrier = &*carrier;
        receipt.charge_guarded(|qualification, recheck, work| {
            let checkpoint = Checkpoint {
                guard,
                receipt: recheck,
                qualification,
                lease,
                namespace,
                subject,
                binding,
                row,
                endpoint,
                required,
                chain,
                uid,
                carrier,
            };
            action(&location, carrier, &checkpoint, work)
        })
    }

    /// X3b r10 item 4's end step, as the operation's end path runs it:
    /// 1. the append lock is dropped, then the lease is released
    ///    (`readers.lease`, then `writer.lease`);
    /// 2. the end step is not entered (X3b r10 item 4; X3d r6 item 7) after
    ///    an uncertain journal outcome, as the operation's owner reports it,
    ///    or when the attempt ledger is closed (a certain refusal or a failed
    ///    settlement closed it; the walk's first charge would be refused):
    ///    no fence, no read, no copy, and nothing to disclose;
    /// 3. otherwise, on the attempt ledger: the fence is retaken by the
    ///    shared charged walk from H, the no-follow fence open and S7's
    ///    bounded wait; the walked I must be the retained I, and `trust`,
    ///    `host`, `projects` and N must still be bound by name under it;
    ///    then, after `Exhausted`, step 3's rollover (X3b-4), which takes and
    ///    releases its own `EXCLUSIVE` lease; then steps 4 and 5's probe, read
    ///    and floor copy; then the fence is released.
    ///
    /// A failure is returned as a value and never rewrites the operation's
    /// outcome; a rollover outcome is disclosed on its own row.
    pub(crate) fn end(self, outcome: JournalOutcome) -> OperationEnd {
        self.end_with(outcome, &mut OsClock, operation_end_after_exhaustion)
    }
    /// `end` over a given wait clock and rollover (the test seam; production
    /// passes the OS clock and X3b-4's `end_step_after_exhaustion`).
    pub(super) fn end_with(
        self,
        outcome: JournalOutcome,
        clock: &mut impl WaitClock,
        rollover: impl FnOnce(
            &CarrierLocation<'_>,
            CapacityExhaustion,
            &str,
            &mut WorkScope<'_>,
        ) -> ExhaustedEnd,
    ) -> OperationEnd {
        let Self {
            guard,
            carrier,
            lease,
            namespace,
            namespace_path,
            trust,
            chain,
            account,
            receipt,
            ..
        } = self;
        // The observer stops first; then the append lock and the lease.
        drop(guard);
        drop(carrier);
        drop(lease);
        // Law X9 r1 item 5 (unit X3d-1): `StoppedSession::finish`'s release
        // and end step, X3d item 7 steps 2 and 3.
        opensip_platform::crash_barrier!("x3d.finish", "lease-release", step);
        if outcome == JournalOutcome::Uncertain || receipt.is_closed() {
            return OperationEnd::NotEntered;
        }
        opensip_platform::crash_barrier!("x3d.finish", "end-step.before", step);
        let ended = end_entered(
            outcome,
            clock,
            rollover,
            trust,
            namespace,
            namespace_path,
            chain,
            account,
            receipt,
        );
        opensip_platform::crash_barrier!("x3d.finish", "end-step.after", step);
        ended
    }
}
// ------------------------------------------------------------ the store root

/// `I/stores`, the parent of every store directory.
pub(super) const STORES: &str = "stores";
/// The store's own marker, which the endpoint admitted (law X3a item 2).
pub(super) const STORE_MARKER: &str = "store-instance.v1";
/// macOS `ELOOP`: `O_NOFOLLOW` met a symbolic link at the marker's name.
const ELOOP: i32 = 62;

/// Law X3d r6 item 3 steps 4 to 6 (unit X3d-2): the selected store's
/// directory `I/stores/S`, for storage's per-(S, N) evidence ledger and
/// objects (law X3c r7 item 1), on the attempt ledger, under the held lease.
/// - It is opened no-follow from the retained I: `stores`, then S, each
///   present, private, exactly named and on I's device.
/// - It must hold the marker the endpoint admitted: `store-instance.v1`,
///   opened no-follow under it, has the device and inode of the endpoint's
///   retained marker sample (law X3a item 2). Otherwise, or if either
///   directory is gone, it is the custody row `required-files-changed`.
/// - Its absolute spelling, built from H as walked, must name that same
///   directory, as N's does (`namespace_spelling`).
///
/// Read-only: nothing is created or written, and no fence is taken. A free
/// function, so that `ProjectOperation` gains no inherent function.
pub(crate) fn open_store_root(
    operation: &mut ProjectOperation,
) -> Result<(RetainedDirectory, PathBuf, u32), WorkFailure<OperationRow>> {
    let ProjectOperation {
        binding,
        required,
        chain,
        account,
        receipt,
        ..
    } = operation;
    let uid = account.uid();
    let store = binding.store_instance().to_owned();
    let relative = format!("{STORES}/{store}/{STORE_MARKER}");
    let admitted = required
        .iter()
        .find(|file| file.relative() == relative)
        .map(RequiredFile::identity);
    let home = chain.home_spelling().to_path_buf();
    receipt.charge(|_, work| {
        let (root, path) = store_root_in(chain.installation(), &home, &store, admitted, uid, work)?;
        Ok((root, path, uid))
    })
}

/// `open_store_root`'s steps over a retained I, H's spelling, S and the
/// endpoint's admitted marker identity, on any caller's ledger: the write
/// operation's attempt ledger, or read-only recovery's own (law X6 r3 item 3,
/// unit X6b). Read-only.
pub(super) fn store_root_in(
    installation: &RetainedDirectory,
    home: &Path,
    store: &str,
    admitted: Option<(u64, u64)>,
    uid: u32,
    work: &mut WorkScope<'_>,
) -> Result<(RetainedDirectory, PathBuf), WorkFailure<OperationRow>> {
    let home = home.to_path_buf();
    let changed = || {
        WorkFailure::Operation(OperationRow::Installation(T::Custody {
            subject: "required-files-changed",
        }))
    };
    let host_io = || WorkFailure::Operation(OperationRow::Installation(T::HostIo));
    let directory = |failure: NamespaceFailure| match failure {
        WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
        WorkFailure::Operation(NamespaceRefusal::Missing(..)) => changed(),
        WorkFailure::Operation(refusal) => WorkFailure::Operation(OperationRow::Project(
            ProjectWriteRow::Project(refusal.row()),
        )),
    };
    let Some(admitted) = admitted else {
        return Err(WorkFailure::Operation(OperationRow::Installation(
            T::Invariant,
        )));
    };
    // `I/stores` and S are installation-private store data under I.
    let stores = required_directory(installation, STORES, Owner::Installation, uid, work)
        .map_err(directory)?;
    let root = required_directory(&stores, store, Owner::Installation, uid, work)
        .map_err(directory)?;
    let marker = work.run(RetainedDirectory::open_regular_cost(STORE_MARKER), |_| {
        root.open_regular(STORE_MARKER).map_err(|error| {
            if error.kind() == io::ErrorKind::NotFound || error.raw_os_error() == Some(ELOOP) {
                changed()
            } else {
                host_io()
            }
        })
    })?;
    let path = FIXED_ANCESTORS
        .iter()
        .chain([FINAL_NAME, STORES, store].iter())
        .fold(home, |path, name| path.join(name));
    let cost = WorkCost {
        bytes: path.as_os_str().len(),
        ..PATH_STATUS
    };
    work.run(cost, |_| {
        let held = marker.metadata().map_err(|_| host_io())?;
        if (held.dev(), held.ino()) != admitted {
            return Err(changed());
        }
        let named = match std::fs::symlink_metadata(&path) {
            Ok(named) => named,
            Err(error) if error.kind() == io::ErrorKind::NotFound => return Err(changed()),
            Err(_) => return Err(host_io()),
        };
        let retained = root.as_file().metadata().map_err(|_| host_io())?;
        if !named.file_type().is_dir()
            || (named.dev(), named.ino()) != (retained.dev(), retained.ino())
        {
            return Err(changed());
        }
        Ok(())
    })?;
    Ok((root, path))
}

/// The end step itself, once entered: on the attempt ledger, the fence
/// retaken, then the rollover after `Exhausted`, then the copy.
#[allow(clippy::too_many_arguments)]
fn end_entered(
    outcome: JournalOutcome,
    clock: &mut impl WaitClock,
    rollover: impl FnOnce(
        &CarrierLocation<'_>,
        CapacityExhaustion,
        &str,
        &mut WorkScope<'_>,
    ) -> ExhaustedEnd,
    trust: RetainedDirectory,
    namespace: Namespace,
    namespace_path: PathBuf,
    chain: Chain,
    account: Account,
    mut receipt: WritePlatformReceipt,
) -> OperationEnd {
    let exhausted = match &outcome {
        JournalOutcome::Exhausted {
            exhaustion,
            operation_ref,
        } => Some((*exhaustion, operation_ref.as_str())),
        _ => None,
    };
    let uid = account.uid();
    // Once the rollover has returned, its outcome and the unlock's are
    // kept here, outside the charge: a rollover that latched the attempt
    // ledger (a refusal, a failed reservation, an undetermined outcome, or
    // a failed copy after it) makes the charge itself return `Closed`,
    // and the rollover's outcome must still be disclosed on its own row.
    let mut rolled: Option<(ExhaustedEnd, io::Result<()>)> = None;
    let result = receipt.charge(|qualification, work| {
        let home_filesystem =
            |sample: &DescriptorFilesystem| qualification.is_home_filesystem(sample);
        let policy = ChainPolicy::new(qualification.omission_premise(), &home_filesystem);
        let gate = |failure: WorkFailure<GateRefusal>| lift(failure, EndRefusal::Gate);
        let fresh = match walk_chain(chain.home_spelling(), uid, &policy, work).map_err(gate)? {
            Walked::Present(fresh) => fresh,
            Walked::Absent(_) => {
                return Err(WorkFailure::Operation(EndRefusal::Gate(
                    GateRefusal::Absent,
                )));
            }
        };
        let (file, _) = open_fence(&fresh, uid, work).map_err(gate)?;
        // X9: the end path's fence is `x2.fence.end` (law X9 r1 item 5).
        let fence = opensip_platform::crash_scope!("x2.fence.end", { wait(file, clock, work) })
            .map_err(gate)?;
        // The fence is held from here, and released last whatever the
        // steps below return.
        let ended = end_under_fence(
            &fresh,
            &chain,
            &trust,
            &namespace,
            &namespace_path,
            uid,
            exhausted.map(|(exhaustion, released)| (exhaustion, released, rollover)),
            work,
        );
        let unlocked = opensip_platform::crash_scope!("x2.fence.end", { fence.release() });
        drop(fresh);
        match ended? {
            Ended::Copied(copied) => {
                unlocked.map_err(|error| WorkFailure::Operation(EndRefusal::Release(error)))?;
                Ok(Some(copied))
            }
            Ended::Rolled(exhausted) => {
                rolled = Some((exhausted, unlocked));
                Ok(None)
            }
        }
    });
    // The rollover ran: its outcome is returned whatever the charge
    // returned, with the copy's or the unlock's failure kept in `end`.
    if let Some((ExhaustedEnd { rollover, end }, unlocked)) = rolled {
        let end = match (end, unlocked) {
            (Err(failure), _) => Err(EndFailure(lift(failure, EndRefusal::Carrier))),
            (Ok(_), Err(error)) => Err(EndFailure(WorkFailure::Operation(EndRefusal::Release(
                error,
            )))),
            (Ok(copied), Ok(())) => Ok(copied),
        };
        return OperationEnd::RolledOver { rollover, end };
    }
    // No rollover ran: the walk, the fence, a rebind or the copy decides.
    match result {
        Ok(Some(copied)) => OperationEnd::Ended(copied),
        Ok(None) => OperationEnd::Failed(EndFailure(WorkFailure::Operation(EndRefusal::Carrier(
            CarrierRefusal::Unreadable,
        )))),
        Err(failure) => OperationEnd::Failed(EndFailure(failure)),
    }
}
fn lift<E>(failure: WorkFailure<E>, wrap: impl FnOnce(E) -> EndRefusal) -> WorkFailure<EndRefusal> {
    match failure {
        WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
        WorkFailure::Operation(error) => WorkFailure::Operation(wrap(error)),
    }
}
/// What the end step under the fence did.
enum Ended {
    Copied(EndOutcome),
    Rolled(ExhaustedEnd),
}
/// The end step under the retaken fence: the walked I is the retained one,
/// the location's directories are still bound by name, then the copy, or,
/// after an exhaustion, the rollover and then the copy.
#[allow(clippy::too_many_arguments)]
fn end_under_fence(
    fresh: &Chain,
    chain: &Chain,
    trust: &RetainedDirectory,
    namespace: &Namespace,
    namespace_path: &Path,
    uid: u32,
    exhausted: Option<(
        CapacityExhaustion,
        &str,
        impl FnOnce(&CarrierLocation<'_>, CapacityExhaustion, &str, &mut WorkScope<'_>) -> ExhaustedEnd,
    )>,
    work: &mut WorkScope<'_>,
) -> Result<Ended, WorkFailure<EndRefusal>> {
    let owner = |failure| lift(failure, EndRefusal::Owner);
    if fresh.installation_id() != chain.installation_id() {
        return Err(WorkFailure::Operation(EndRefusal::Owner(
            RegistrationRefusal::Changed(Owner::Installation),
        )));
    }
    let i = fresh.installation();
    let step = Step::Handoff;
    rebind(i, TRUST, trust, step, Owner::Trust, work).map_err(owner)?;
    rebind(i, HOST, &namespace.host, step, Owner::Host, work).map_err(owner)?;
    rebind(
        &namespace.host,
        PROJECTS,
        &namespace.projects,
        step,
        Owner::Projects,
        work,
    )
    .map_err(owner)?;
    rebind(
        &namespace.projects,
        &namespace.id,
        &namespace.directory,
        step,
        Owner::Namespace,
        work,
    )
    .map_err(owner)?;
    let place = CarrierPlace {
        trust,
        namespace: &namespace.directory,
        namespace_path,
        namespace_id: &namespace.id,
        uid,
    };
    let location = CarrierLocation::admitted(&place);
    match exhausted {
        Some((exhaustion, released, rollover)) => Ok(Ended::Rolled(rollover(
            &location, exhaustion, released, work,
        ))),
        None => operation_end_copy(&location, work)
            .map(Ended::Copied)
            .map_err(|failure| lift(failure, EndRefusal::Carrier)),
    }
}

/// The end path's result. None of it rewrites the operation's outcome.
#[derive(Debug)]
pub(crate) enum OperationEnd {
    /// An uncertain journal outcome, or a closed attempt ledger: the lease
    /// was released and the end step was not entered (X3b r10 item 4). Not
    /// a failure. The next writer's floor step copies the floor.
    NotEntered,
    /// The end step ran under the retaken fence, which is released again.
    Ended(EndOutcome),
    /// After `Exhausted`: X3b-4's rollover outcome (each disclosed on its
    /// own row, X7 r3 item 6) and the floor copy that followed it, or the
    /// copy's or the unlock's failure. The fence is released.
    RolledOver {
        rollover: RolloverOutcome,
        end: Result<EndOutcome, EndFailure>,
    },
    /// The end step stopped; the floor stays where it was, and the fence,
    /// if it was taken, is released. Disclosed by the caller.
    Failed(EndFailure),
}
impl OperationEnd {
    /// Whether the end step was entered (M3-B unit B2-b3c; Codex
    /// B2B3C-R1-RF-1). `NotEntered` is not a failure.
    pub(crate) fn entered(&self) -> bool {
        !matches!(self, Self::NotEntered)
    }
    /// The end-path failure the caller must disclose, if any: a stopped end
    /// step, or a failed copy or unlock after a rollover.
    pub(crate) fn failure(&self) -> Option<&EndFailure> {
        match self {
            Self::NotEntered | Self::Ended(_) | Self::RolledOver { end: Ok(_), .. } => None,
            Self::RolledOver { end: Err(failure), .. } | Self::Failed(failure) => Some(failure),
        }
    }
}
/// Why the end step stopped.
#[derive(Debug)]
pub(crate) enum EndRefusal {
    /// The walk, the fence open or the bounded wait (468's rows; busy is the
    /// installation busy row).
    Gate(GateRefusal),
    /// A changed I, or a carrier-place directory no longer bound by name.
    Owner(RegistrationRefusal),
    /// The end step's own refusal (X3b item 8).
    Carrier(CarrierRefusal),
    /// The fence's unlock failed after the copy.
    Release(io::Error),
}
/// An end-path failure on the attempt ledger, after the end step was
/// entered (a closed ledger never enters it).
#[derive(Debug)]
pub(crate) struct EndFailure(WorkFailure<EndRefusal>);
impl EndFailure {
    pub(crate) fn failure(&self) -> &WorkFailure<EndRefusal> {
        &self.0
    }
    pub(crate) fn row(&self) -> OperationRow {
        match &self.0 {
            WorkFailure::Budget(_) => OperationRow::BudgetExhausted,
            WorkFailure::Operation(EndRefusal::Gate(refusal)) => {
                OperationRow::Installation(gate_refusal(refusal))
            }
            WorkFailure::Operation(EndRefusal::Owner(refusal)) => {
                OperationRow::Project(ProjectWriteRow::Project(refusal.row()))
            }
            WorkFailure::Operation(EndRefusal::Carrier(refusal)) => {
                OperationRow::Carrier(refusal.row())
            }
            WorkFailure::Operation(EndRefusal::Release(_)) => OperationRow::Installation(T::HostIo),
        }
    }
}

// ------------------------------------------------------------- the handoff

/// What the lease-free point made for X4's guard (law X4 r7 item 2): the
/// gate and the monitor, created first, the view the monitor's first read
/// admitted, and the trust store's retained handles.
struct TrustStart {
    lease_free: LeaseFree,
    view: AdmittedCurrentTrust,
    handles: RetainedTrustHandles,
    core: String,
}
/// Why the lease-free trust step refused.
enum TrustStep {
    Trust(TrustRefusal),
    Monitor(crate::revocation::StopReason),
    Gate(GateRefusal),
}
/// Law X4 r7 item 2 with X4T r11 items 7 to 9 and X4B r5 item 1 (units
/// X4a and X4B-b), first at the lease-free point and before anything is
/// read: the operation's one `FinalGate` and `FreshnessMonitor` are
/// created; the monitor's first `read` runs X4T's fenced admission over the
/// gate's one read of `state.v1`, with the S4 observation projected from
/// that read's own opening sample. On F absent only, the same read accepts
/// the write receipt's embedded bootstrap payload on that observation and
/// runs the one confirming admission (X4B r5 item 1 step 2). Each confirmed
/// publication (the acceptance, then any floor write) advances the gate's
/// retained `state.v1` owner, in order; then the trust store's handles are
/// retained and judged. All on the gate's ledger with the fence held and no
/// project lock, then the gate's and the receipt's rechecks.
fn trust_start(
    holder: &mut OrdinaryWriteAdmission,
    invocation: &TrustInvocation,
    clock: MonitorClock,
) -> Result<TrustStart, OperationRefusal> {
    let mut lease_free = LeaseFree::create(clock);
    let core = holder.selected_closure();
    let refused = |step: TrustStep| WorkFailure::Operation(step);
    let stepped = holder.gate_step(|installation, qualification, bootstrap, work| {
        let (raw, sample) = {
            let read = installation.current_trust();
            let Some(file) = read.file else {
                return Err(refused(TrustStep::Gate(GateRefusal::Latched)));
            };
            (read.raw.to_vec(), file.metadata().clone())
        };
        let read = {
            let fence = installation.held_fence();
            lease_free.first_read(|opening| {
                let observation = crate::clock_observation::project_monitor_sample(
                    opening.wall_seconds,
                    opening.wall_nanos,
                    opening.before,
                    opening.after,
                    &opening.boot,
                )
                .map_err(|cause| TrustRefusal {
                    row: crate::trust::TrustRow::HostIo,
                    cause: cause.into(),
                })?;
                fenced_operation_read(
                    work,
                    &fence,
                    &raw,
                    &sample,
                    &observation,
                    &core,
                    invocation,
                    bootstrap,
                )
            })
        };
        let (view, confirmed) = read.map_err(|failure| {
            refused(match failure {
                super::operation_guard::FirstRead::Counter(refusal) => TrustStep::Trust(refusal),
                super::operation_guard::FirstRead::Monitor(reason) => TrustStep::Monitor(reason),
            })
        })?;
        // X4T-b judgment call 9: after each confirmed publication, in order.
        for confirmed in &confirmed {
            installation
                .advance_current(confirmed)
                .map_err(|refusal| refused(TrustStep::Gate(refusal)))?;
        }
        let store = opensip_identity::parse_json(installation.current_trust().raw)
            .ok()
            .and_then(|capsule| match capsule {
                opensip_identity::JsonValue::Object(mut members) => members.remove("store"),
                _ => None,
            })
            .ok_or_else(|| {
                refused(TrustStep::Gate(GateRefusal::Incomplete(
                    super::installation_admission::IncompleteRefusal::CurrentStore,
                )))
            })?;
        let home_filesystem =
            |sample: &DescriptorFilesystem| qualification.is_home_filesystem(sample);
        let handles = RetainedTrustHandles::open(
            installation.installation_directory(),
            installation.uid(),
            &store,
            &home_filesystem,
            work,
        )
        .map_err(|failure| match failure {
            WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
            WorkFailure::Operation(refusal) => refused(TrustStep::Trust(refusal)),
        })?;
        Ok((view, handles))
    });
    let (view, handles) = stepped.map_err(|failure| match failure {
        GateStep::Gate(refusal) => OperationRefusal::Project(refusal),
        GateStep::Step(WorkFailure::Budget(budget)) => {
            OperationRefusal::Project(ProjectWriteRefusal::Gate(GateRefusal::Budget(budget)))
        }
        GateStep::Step(WorkFailure::Operation(TrustStep::Trust(refusal))) => {
            OperationRefusal::Trust(refusal)
        }
        GateStep::Step(WorkFailure::Operation(TrustStep::Monitor(reason))) => {
            OperationRefusal::Live(StopCause::FailStop {
                subject: reason.subject(),
            })
        }
        GateStep::Step(WorkFailure::Operation(TrustStep::Gate(refusal))) => {
            OperationRefusal::Project(ProjectWriteRefusal::Gate(refusal))
        }
    })?;
    Ok(TrustStart {
        lease_free,
        view,
        handles,
        core,
    })
}

/// The lease-free point on the writer's held fence: `I/trust` confirmed and
/// N's spelling admitted on the gate's ledger with the gate's recheck, then
/// X3b's floor step on the attempt ledger with the gate's and the receipt's
/// rechecks. No project lock is held. X4's trust start (`trust_start`) runs
/// first, at this same point.
fn lease_free(
    holder: &mut &mut OrdinaryWriteAdmission,
    namespace: &RetainedDirectory,
    id: &str,
    inputs: &ProjectInputs<'_>,
) -> Result<(RetainedDirectory, PathBuf, OperationFloor), OperationRefusal> {
    use namespace_lease::FenceHolder;
    let (trust, path) = holder
        .fenced(inputs, |held, work| {
            let trust = required_directory(held.installation, TRUST, Owner::Trust, held.uid, work)?;
            let path = namespace_spelling(held.home, id, namespace, work)?;
            Ok((trust, path))
        })
        .map_err(OperationRefusal::Project)?;
    let floor = holder.attempt_step(|installation, work| {
        let place = CarrierPlace {
            trust: &trust,
            namespace,
            namespace_path: &path,
            namespace_id: id,
            uid: installation.uid(),
        };
        operation_floor_step(&CarrierLocation::admitted(&place), work)
    })?;
    Ok((trust, path, floor))
}
/// Item 7a's recheck of the moved owners under the held fence: the subject
/// (a registered subject's namespace to `footprint`), the namespace's
/// directories, and each locked carrier's name binding.
fn recheck_owners(
    parts: &NamespaceParts,
    held: &Held<'_, '_>,
    footprint: Footprint,
    work: &mut WorkScope<'_>,
) -> Result<(), NamespaceFailure> {
    recheck_subject(&parts.subject, held, footprint, work)?;
    recheck_directories(&parts.namespace, held, work)?;
    for (name, metadata) in parts.lease.carriers() {
        recheck_binding(&parts.namespace.directory, name, metadata, held.uid, work)?;
    }
    Ok(())
}

/// Law X2 item 7a with X3b-3, on one ordinary writer. See the module
/// comment for the order. On any refusal the values already built drop in
/// reverse order: the append lock, the lease, and last the writer, whose
/// installation releases the fence.
pub(super) fn begin(
    mut writer: OrdinaryWriteAdmission,
    subject: NamespaceSubject,
    lease: WriterLease,
    inputs: &ProjectInputs<'_>,
    invocation: &TrustInvocation,
    seam: GuardSeam,
) -> Result<ProjectOperation, OperationRefusal> {
    use namespace_lease::FenceHolder;
    // X3a's endpoint, from this gate's one read.
    writer
        .join_store_endpoint()
        .map_err(OperationRefusal::Endpoint)?;
    // Item 7 (X2d): the namespace, with no lock taken.
    let mut target =
        namespace_lease::admit(&mut writer, subject, inputs).map_err(OperationRefusal::Project)?;
    // The lease-free point: X4's gate, monitor and first read first, then
    // the carrier place and X3b's floor step.
    let GuardSeam {
        clock,
        cadence,
        hook,
    } = seam;
    let (start, trust, namespace_path, floor) = target.lease_free(|holder, namespace, id| {
        let start = trust_start(holder, invocation, clock)?;
        let (trust, path, floor) = lease_free(holder, namespace, id, inputs)?;
        Ok::<_, OperationRefusal>((start, trust, path, floor))
    })?;
    // Item 7 (X2d): the lease.
    let fenced = target
        .lease_writer(lease, inputs)
        .map_err(OperationRefusal::Project)?;
    // Item 7a step 2's move begins here: the lease and the subject leave the
    // fenced namespace, and the writer, still holding the fence, is free
    // again. Nothing is copied.
    let (_, parts) = fenced.into_parts();
    // Step 1, the join: every owner rechecked under the fence, and owner
    // §8's binding derived from the owners moving into the operation.
    let binding = (&mut writer)
        .fenced(inputs, |held, work| {
            recheck_owners(&parts, held, Footprint::Exact, work)?;
            derive_binding(&parts.row, &parts.namespace, held, work)
        })
        .map_err(OperationRefusal::Project)?;
    // Step 3: X3b's carrier start under the fence and the lease, then every
    // owner again, with N now holding the carrier.
    let carrier = writer.attempt_step(|installation, work| {
        let place = CarrierPlace {
            trust: &trust,
            namespace: &parts.namespace.directory,
            namespace_path: &namespace_path,
            namespace_id: &parts.namespace.id,
            uid: installation.uid(),
        };
        operation_start(&CarrierLocation::admitted(&place), floor, work)
    })?;
    (&mut writer)
        .fenced(inputs, |held, work| {
            recheck_owners(&parts, held, Footprint::Started, work)
        })
        .map_err(OperationRefusal::Project)?;
    // X4 r7 item 6: the guard, built under the held fence from what the
    // lease-free point made; its observer starts as it moves into the
    // operation. It runs no admission and writes no trust state here.
    let TrustStart {
        lease_free,
        view,
        handles,
        core,
    } = start;
    let guard = OperationGuard::start(
        lease_free,
        view,
        handles,
        core,
        inputs.trust_groups.clone(),
        cadence,
        hook,
    )
    .map_err(|refusal| match refusal {
        // Law X4 r8 LD8-10 (unit X4-F3): a gate latched before the guard's
        // entry is the fail-stop row a first read returning `AlreadyStopped`
        // takes, subject `latched`. No guard or observer exists.
        GuardStart::Latched => OperationRefusal::Live(StopCause::FailStop {
            subject: crate::revocation::StopReason::AlreadyStopped.subject(),
        }),
        GuardStart::Observer(error) => OperationRefusal::Observer(error),
    })?;
    // Steps 2 and 4: the writer's owners move into the operation, the gate
    // and its ledger end (the unbound `_`), and only then is the fence
    // released. A failed unlock closes the fence descriptor anyway; the
    // operation is then dropped, releasing the append lock and the lease.
    let (installation, receipt, _) = writer.into_parts();
    let (fence, chain, account, required, endpoint) = installation.into_handoff();
    let NamespaceParts {
        lease,
        mode,
        subject,
        row,
        namespace,
    } = parts;
    let operation = ProjectOperation {
        guard,
        carrier,
        lease,
        mode,
        binding,
        row,
        subject,
        namespace,
        namespace_path,
        trust,
        endpoint,
        required,
        chain,
        account,
        receipt,
    };
    // X9: the handoff's release is `x2.fence.release` (law X9 r1 item 5).
    match fence.release() {
        Ok(()) => Ok(operation),
        Err(error) => Err(OperationRefusal::Release(released(error))),
    }
}

#[cfg(test)]
mod tests {
    include!("operation_handoff_tests.rs");
}
