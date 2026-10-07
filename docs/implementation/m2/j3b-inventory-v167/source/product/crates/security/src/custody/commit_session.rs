// Law X3d r6 (unit X3d-1): the security side of the `CommitSession` storage
// facade. One `ProjectOperation` (X2e) opens at most one session:
// - `CommitSession::open` (item 2) consumes the operation, draws the
//   ExecutionId and the operationRef from the host CSPRNG on the attempt
//   ledger, and binds N, (S, G, K), the carrier digest, the receipt's
//   selected core closure and (law X3d r8) its core evaluator closure; (law
//   X3d r9 S10.1, unit J3a) the ExecutionId is reserved in the process's
//   `ExecutionIdReservations` in the same step, and the session holds the
//   `ReservedExecutionId`;
// - `reserve_end_path` is item 3 step 0: the attempt ledger's one settlement
//   reserve (X3d-0), sized exactly at one bounded `REV` and one bounded
//   `CLN` append (item 8), and held only by the session and then its
//   `StoppedSession`;
// - `capacity` is item 3 step 3 over X3b's `seal_fits`;
// - `begin_journal_txn` and `JournalWriteTxn::abort` are item 4 steps 1 and
//   2: the journal's level 3, and its consuming abort when storage's
//   evidence ledger refuses its own level 3;
// - `seal_under_append_lock` is item 4 step 3 with the security-owned
//   two-phase adapter (`CommitAdapter`, `StagedCommit`), whose
//   implementation is storage's (X3d-2): level 4, X4's checkpoint, the
//   `SEAL` bound through `PreparedJournalSeal`, the repeated checkpoint, the
//   adapter's staging, the final checkpoint ending in `FinalGate::admit`, the
//   evidence `COMMIT` through the one `AdmissionPermit`, then level 4's
//   release; every stop takes X3b's stop order exactly once;
// - `StoppedSession::finish` is item 7 with X4c merged: one `settle` of the
//   reserve for the `REV`, then the `CLN`, each a fresh level-3-then-level-4
//   append; then the lease's release and X3b's end step, which is not
//   entered after an uncertain outcome or on a closed attempt ledger.
// The reserve is forfeited where an uncertain outcome is classified (a
// journal commit or barrier, an undetermined attempt-admission `COMMIT`, an
// undetermined evidence `COMMIT`): the `StoppedSession` then holds none.
// Every certain refusal before admission latches the operation's one gate
// (X4 r7 item 7, 0 to 2), so the `REV` item 7 owes a latched gate follows.
// X9 r1 item 5's `x3d.session`, `x3d.publish` and `x3d.finish` points are
// placed here and in the end path; `x3d.publish.published` is X3d-2's.
// Library only: no command commits.
use super::first_registration::{ProjectWriteRow, RegistrationRow};
use super::operation_guard::StopHandle;
use super::operation_guard::{GuardRefusal, StopCause};
use super::operation_handoff::{
    JournalOutcome, OperationEnd, OperationRow, ProjectOperation, open_store_root,
};
use super::project_admission::ProjectAdmissionRow;
use crate::InstallationTermination as T;
use crate::commit_authority::{AttemptState, PreparedJournalSeal};
use crate::journal_store::{
    AppendError, CapacityExhaustion, CarrierRefusal, CarrierRefusalRow as CarrierRow,
    DetachedJournal, RecordDraft, RolloverOutcome, end_path_append_bound, end_path_body_bound,
    project_key_digest, seal_fits,
};
use crate::{D9Signal, LatchOutcome};
use opensip_evaluator::ReplayedRun;
use opensip_platform::{
    ReservedExecutionId, RetainedDirectory, SettlementReserve, WorkBudgetError, WorkCost,
    WorkFailure, WorkScope,
};
use std::path::{Path, PathBuf};

/// The two host-CSPRNG draws of `open` (item 2): 16 bytes each, for the
/// ExecutionId and the operationRef, rendered as fixed-length ids.
const DRAW_COST: WorkCost = WorkCost {
    objects: 2,
    edges: 2,
    bytes: 2 * (16 + 38),
};

// ------------------------------------------------------- end-path bodies

/// Law X3d r6 item 8: the closed end-path `REV` reasons. S6's own words where
/// they name the stop (`trust-revoked`, `policy`, `observer-fail-stop`), and
/// two for the other latches: a stale guard at a checkpoint, and any other
/// certain refusal or a durable `SEAL` without its evidence commit. The end
/// path records no `trustEpochObserved`.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum RevReason {
    Operator,
    TrustRevoked,
    Policy,
    ObserverFailStop,
    StaleGuard,
    OperationStopped,
}
impl RevReason {
    const ALL: [Self; 6] = [
        Self::TrustRevoked,
        Self::Policy,
        Self::ObserverFailStop,
        Self::StaleGuard,
        Self::OperationStopped,
        Self::Operator,
    ];
    fn spelling(self) -> &'static str {
        match self {
            Self::Operator => "operator",
            Self::TrustRevoked => "trust-revoked",
            Self::Policy => "policy",
            Self::ObserverFailStop => "observer-fail-stop",
            Self::StaleGuard => "stale-guard",
            Self::OperationStopped => "operation-stopped",
        }
    }
    /// The reason for the operation's first recorded stop, if any.
    fn of(cause: Option<&StopCause>) -> Self {
        match cause {
            Some(StopCause::Operator { .. }) => Self::Operator,
            Some(StopCause::Revoked { subject }) if *subject == "policy" => Self::Policy,
            Some(StopCause::Revoked { .. }) => Self::TrustRevoked,
            Some(StopCause::FailStop { .. }) => Self::ObserverFailStop,
            Some(StopCause::Stale(_)) => Self::StaleGuard,
            // Law X4 r8 LD8-7 (unit X4-F3): a certain refusal's recorded
            // cause keeps the reason it had with no cause.
            Some(StopCause::CertainRefusal) | None => Self::OperationStopped,
        }
    }
    fn draft(self) -> RecordDraft {
        RecordDraft::Rev {
            reason: self.spelling().to_owned(),
            trust_epoch_observed: None,
        }
    }
}
/// F38's fixed residual pair: the durable `SEAL` that has no evidence
/// commit, and the staged evidence that was rolled back (or never staged).
const CLEANUP_RESIDUALS: [&str; 2] = [
    "seal-without-evidence-commit",
    "evidence-transaction-rolled-back",
];
fn cleanup_draft() -> RecordDraft {
    RecordDraft::Cln {
        residuals: CLEANUP_RESIDUALS.iter().map(|r| (*r).to_owned()).collect(),
    }
}
/// The two end-path kinds and their bounds.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum EndRecord {
    Rev,
    Cln,
}
impl EndRecord {
    fn kind(self) -> &'static str {
        match self {
            Self::Rev => "REV",
            Self::Cln => "CLN",
        }
    }
    /// Every draft of this kind the end path can build.
    fn drafts(self) -> Vec<RecordDraft> {
        match self {
            Self::Rev => RevReason::ALL.iter().map(|r| r.draft()).collect(),
            Self::Cln => vec![cleanup_draft()],
        }
    }
}
/// The end path's body bound for `kind`: the longest canonical body any of
/// its drafts has at the largest generation and the last ordinary sequence.
fn body_bound(n: &str, operation_ref: &str, kind: EndRecord) -> Option<usize> {
    kind.drafts()
        .iter()
        .map(|draft| end_path_body_bound(n, operation_ref, draft).ok())
        .try_fold(0, |bound, len| len.map(|len| bound.max(len)))
}
/// Law X3d r6 item 8: a draft longer than its kind's bound is refused on the
/// invariant row before any effect. Only the end path's own closed drafts
/// fit; the check runs again before each append.
fn admit_end_draft(
    n: &str,
    operation_ref: &str,
    kind: EndRecord,
    draft: &RecordDraft,
) -> Result<(), EndStep> {
    let fits = matches!(
        (kind, draft),
        (EndRecord::Rev, RecordDraft::Rev { .. }) | (EndRecord::Cln, RecordDraft::Cln { .. })
    );
    let len = end_path_body_bound(n, operation_ref, draft).map_err(|_| EndStep::Bound)?;
    match body_bound(n, operation_ref, kind) {
        Some(bound) if fits && len <= bound => Ok(()),
        _ => Err(EndStep::Bound),
    }
}
/// Law X3d r6 item 8: the settlement reserve's exact size, one bounded `REV`
/// and one bounded `CLN` append, each by the append path's own cost
/// functions at its kind's longest draft.
fn end_path_reserve_cost(n: &str, operation_ref: &str) -> Option<WorkCost> {
    [EndRecord::Rev, EndRecord::Cln]
        .into_iter()
        .map(|kind| {
            kind.drafts()
                .iter()
                .filter_map(|draft| end_path_append_bound(n, operation_ref, draft).ok())
                .max_by_key(|cost| (cost.bytes, cost.edges, cost.objects))
        })
        .try_fold(WorkCost::default(), |total, cost| total.checked_add(cost?))
}

// --------------------------------------------------------------- refusals

/// A refusal of the session, with its item 9 row. Not authority.
#[derive(Debug)]
pub struct SessionRefusal(OperationRow);
impl SessionRefusal {
    /// The row, through 468c's `InstallationTermination` (item 9).
    pub fn termination(&self) -> T {
        operation_termination(&self.0)
    }
}
fn carrier_termination(row: CarrierRow) -> T {
    match row {
        CarrierRow::Busy => T::Busy,
        CarrierRow::LedgerCorrupt => T::LedgerCorrupt,
        CarrierRow::MigrationCorrupt => T::MigrationCorrupt,
        CarrierRow::InheritedCarrier | CarrierRow::HostIo => T::HostIo,
        CarrierRow::Invariant => T::Invariant,
        CarrierRow::DurabilityUndetermined => T::CommitUndetermined,
    }
}
pub(super) fn admission_termination(row: ProjectAdmissionRow) -> T {
    match row {
        ProjectAdmissionRow::RootCustody(subject) => T::ProjectRootCustody { subject },
        ProjectAdmissionRow::ConfigCustody(subject) => T::Custody { subject },
        ProjectAdmissionRow::ExplicitPath => T::ProjectExplicitPath,
        ProjectAdmissionRow::Incomplete => T::Incomplete,
        ProjectAdmissionRow::RequiredFilesChanged => T::Custody {
            subject: "required-files-changed",
        },
        ProjectAdmissionRow::HostIo => T::HostIo,
    }
}
pub(super) fn project_termination(row: &ProjectWriteRow) -> T {
    match row {
        ProjectWriteRow::Installation(row) => row.clone(),
        ProjectWriteRow::BudgetExhausted => T::BudgetExhausted,
        ProjectWriteRow::Project(row) => match row {
            RegistrationRow::Admission(row) => admission_termination(*row),
            RegistrationRow::RootCustody(subject) => T::ProjectRootCustody { subject },
            RegistrationRow::InstallationCustody(subject) => T::Custody { subject },
            RegistrationRow::Incomplete => T::Incomplete,
            RegistrationRow::ScopeLimit(subject) => T::ProjectScopeLimit {
                subject: subject.clone(),
            },
            RegistrationRow::HostIo => T::HostIo,
            RegistrationRow::Invariant => T::Invariant,
            RegistrationRow::Busy => T::Busy,
        },
    }
}
/// Item 9: every row of the composition, exhaustively, through 468c's
/// vocabulary.
pub(super) fn operation_termination(row: &OperationRow) -> T {
    match row {
        OperationRow::Installation(row) => row.clone(),
        OperationRow::Project(row) => project_termination(row),
        OperationRow::Carrier(row) => carrier_termination(*row),
        OperationRow::BudgetExhausted => T::BudgetExhausted,
    }
}
fn carrier_failure(failure: &WorkFailure<CarrierRefusal>) -> OperationRow {
    match failure {
        WorkFailure::Budget(_) => OperationRow::BudgetExhausted,
        WorkFailure::Operation(refusal) => OperationRow::Carrier(refusal.row()),
    }
}
fn invariant() -> OperationRow {
    OperationRow::Installation(T::Invariant)
}
fn budget(_: WorkBudgetError) -> OperationRow {
    OperationRow::BudgetExhausted
}

// ---------------------------------------------------------------- session

/// Item 8: the end-path settlement reserve, held by the session and then
/// its `StoppedSession` only. Private, not Clone; spent only by `finish`.
struct EndPath(SettlementReserve);

/// Item 8: the reserve is given up unspent: where an uncertain outcome is
/// classified, or when `finish` owes nothing. It is never refunded to the
/// attempt ledger's limits.
fn forfeit(_reserve: Option<EndPath>) {}

/// Item 1's `CommitSession`: the consumed `ProjectOperation` with its lease,
/// owners, endpoint, carrier, guard and gate, the drawn ExecutionId and
/// operationRef, the bound carrier digest, and from item 3 step 0 the
/// end-path settlement reserve. Private fields; not Clone, Default or
/// serializable; `open` is its only constructor. Law X3d r9 S10.1 (unit
/// J3a): the ExecutionId is the process registry's `ReservedExecutionId`,
/// and the session accepts no other.
/// Security-owned one-use cancellation token. Only a session mints it.
pub struct CancellationLatch(StopHandle);
impl CancellationLatch {
    pub fn latch(self, signal: D9Signal) -> LatchOutcome {
        self.0.cancel(signal)
    }
}
fn close_sample(operation: &ProjectOperation) -> AttemptState {
    operation.guard().cancellation_handle().close_window()
}
fn admitted(sample: AttemptState) -> bool {
    matches!(
        sample,
        AttemptState::Admitted | AttemptState::AdmittedThenLatched
    )
}
pub struct CommitSession {
    cancellation_taken: bool,
    operation: ProjectOperation,
    execution_id: ReservedExecutionId,
    operation_ref: String,
    carrier_digest: String,
    end_path: Option<EndPath>,
}
impl std::fmt::Debug for CommitSession {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("CommitSession")
            .field("execution_id", &self.execution_id)
            .field("operation_ref", &self.operation_ref)
            .field("reserved", &self.end_path.is_some())
            .finish_non_exhaustive()
    }
}

/// `exec1_` or `op-` and the lowercase hex of 16 CSPRNG bytes.
fn render_id(prefix: &str, bytes: [u8; 16]) -> String {
    let mut id = String::with_capacity(prefix.len() + 32);
    id.push_str(prefix);
    for byte in bytes {
        id.push_str(&format!("{byte:02x}"));
    }
    id
}
/// Identity §2's ExecutionId grammar: `exec1_` and 32 lowercase hex.
fn lawful_execution_id(id: &str) -> bool {
    id.strip_prefix("exec1_").is_some_and(|hex| {
        hex.len() == 32
            && hex
                .bytes()
                .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
    })
}
enum Draw {
    Entropy,
    Grammar,
}

impl CommitSession {
    /// X3d r9 S10.2: minted once for this operation, with no other grant.
    pub fn take_cancellation_latch(&mut self) -> Option<CancellationLatch> {
        if self.cancellation_taken {
            return None;
        }
        self.cancellation_taken = true;
        Some(CancellationLatch(
            self.operation.guard().cancellation_handle(),
        ))
    }
    /// The charged storage step receives the session's one opening callback.
    /// It calls it immediately after successful attempt-row COMMIT, before
    /// publishing the first object (X3d r9 LD9-1).
    pub fn charge_attempt<R, E>(
        &mut self,
        action: impl FnOnce(&mut WorkScope<'_>, Box<dyn FnOnce() + '_>) -> Result<R, WorkFailure<E>>,
    ) -> Result<R, WorkFailure<E>> {
        let handle = self.operation.guard().cancellation_handle();
        self.operation
            .charge(|work| action(work, Box::new(|| handle.open_window())))
    }
    /// Item 2: open the operation's one session. The ExecutionId and the
    /// operationRef are drawn from the host CSPRNG on the attempt ledger
    /// (`x3d.session.execution-draw`); the session binds N, the endpoint's
    /// (S, G, K), the carrier digest `SHA-256(N)` and the selected core
    /// closure the operation carries. A failed draw is the host I/O row, a
    /// binding that does not join is the invariant row; either latches the
    /// gate and returns the operation as a `StoppedSession` with no reserve.
    /// Law X3d r9 S10.1 (J1 item 2; unit J3a): the ExecutionId is reserved
    /// in the process registry in the drawing step, before the session
    /// exists and so before any provider frame; eight collisions are the
    /// host I/O row too. The reservation is never released or reused. The
    /// durable reservation is still the attempt row's (item 3 step 4).
    pub fn open(
        operation: ProjectOperation,
    ) -> Result<CommitSession, (SessionRefusal, StoppedSession)> {
        let mut operation = operation;
        let n = operation.binding().namespace_id().to_owned();
        let drawn = operation.charge(|work| {
            work.run(DRAW_COST, |_| {
                let entropy = || opensip_platform::request_entropy().map_err(|_| Draw::Entropy);
                // Law X3d r9 S10.1 (unit J3a): the draw is reserved in this
                // process's `ExecutionIdReservations` in the same step, before
                // the session exists; a failed draw or eight collisions are
                // the host I/O row. The point keeps its name, place and
                // payload. Under the crash matrix, an injected id is reserved
                // as a draw is: outside the grammar it is the grammar
                // refusal, and already reserved here it is the host I/O row.
                let execution: Result<ReservedExecutionId, Draw> = opensip_platform::crash_barrier!(
                    "x3d.session",
                    "execution-draw",
                    draw,
                    opensip_platform::reserve_execution_id().map_err(|_| Draw::Entropy),
                    |id: &str| {
                        use opensip_platform::crash_barrier::{
                            InjectedExecutionId as Injected, reserve_injected_execution_id,
                        };
                        reserve_injected_execution_id(id).map_err(|refusal| match refusal {
                            Injected::Grammar => Draw::Grammar,
                            Injected::Reserved => Draw::Entropy,
                        })
                    },
                    |value: &Result<ReservedExecutionId, Draw>| value
                        .as_ref()
                        .map_or(String::new(), |id| id.as_str().to_owned())
                );
                let execution = execution.map_err(WorkFailure::Operation)?;
                if !lawful_execution_id(execution.as_str()) {
                    return Err(WorkFailure::Operation(Draw::Grammar));
                }
                let operation_ref = render_id("op-", entropy().map_err(WorkFailure::Operation)?);
                Ok((execution, operation_ref))
            })
        });
        let (execution_id, operation_ref) = match drawn {
            Ok(ids) => ids,
            Err(failure) => {
                let row = match failure {
                    WorkFailure::Budget(_) => OperationRow::BudgetExhausted,
                    WorkFailure::Operation(Draw::Entropy) => OperationRow::Installation(T::HostIo),
                    WorkFailure::Operation(Draw::Grammar) => invariant(),
                };
                return Err(refused(operation, None, row));
            }
        };
        if operation.carrier().lock().namespace_id() != n || operation.row().namespace_id() != n {
            return Err(refused(
                operation,
                Some((execution_id, operation_ref)),
                invariant(),
            ));
        }
        Ok(CommitSession {
            cancellation_taken: false,
            carrier_digest: project_key_digest(&n),
            operation,
            execution_id,
            operation_ref,
            end_path: None,
        })
    }
    /// Law X8 r3 item 3d: the drawn ExecutionId. Read-only; it admits
    /// nothing. Law X3d r9 S10.1 (unit J3a): the reservation's read-only
    /// projection, which storage's binding reads.
    pub fn execution_id(&self) -> &str {
        self.execution_id.as_str()
    }
    /// The session's operationRef (`op-` and 32 hex), for the attempt row
    /// and every journal record of this operation.
    pub fn operation_ref(&self) -> &str {
        &self.operation_ref
    }
    /// N, the bound namespace.
    pub fn namespace_id(&self) -> &str {
        self.operation.binding().namespace_id()
    }
    /// S, the selected store instance.
    pub fn store_instance(&self) -> &str {
        self.operation.binding().store_instance()
    }
    /// G, the selected store generation.
    pub fn store_generation(&self) -> i64 {
        self.operation.binding().store_generation()
    }
    /// K, the selected state schema.
    pub fn state_schema(&self) -> u8 {
        self.operation.binding().state_schema()
    }
    /// The journal carrier's `projectKeyDigest`, lowercase hex of
    /// `SHA-256(N)`, which the start admitted.
    pub fn carrier_digest(&self) -> &str {
        &self.carrier_digest
    }
    /// The write receipt's selected core closure (`kind: "core"`): the store
    /// pair's, X4's closure subjects' and live revocation's. A Run never
    /// names it (law X3d r8; replay admits only `kind: "evaluator"`).
    pub fn core_closure(&self) -> &str {
        self.operation.selected_core().0
    }
    /// Law X3d r8 item 13: the receipt's core evaluator closure (contract
    /// successor EC1), which a `ReplayedRun`'s evaluator closure must equal
    /// (item 3 step 1). Security derives it from the receipt's authenticated
    /// core inventory, the same one as `core_closure`; it is never read from
    /// a Run. Read-only; it admits nothing.
    pub fn core_evaluator_closure(&self) -> &str {
        self.operation.core_evaluator_closure()
    }
    /// Law X3d r8 item 13 (unit X3d-3): the one shared test-support accessor
    /// for the synthetic run candidate. It returns the core evaluator
    /// closure's descriptor (`kind: "evaluator"`, EC1), the TR-CORE-signed
    /// inventory body its `manifestDigest` names, and each tree member's
    /// bytes by logical path, read through the core's retained handles. It
    /// is on X8 r3 item 4b's one site list under the joint predicate, absent
    /// from every release build, and no production path calls it. Values
    /// only: it grants nothing.
    #[doc(hidden)]
    #[cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))]
    pub fn core_evaluator_closure_preimages(
        &self,
    ) -> (
        opensip_identity::JsonValue,
        Vec<u8>,
        std::collections::BTreeMap<String, Vec<u8>>,
    ) {
        self.operation.core_evaluator_closure_preimages()
    }
    /// Unit X3d-2: the ProjectId of N's ACTIVE row, the session's target
    /// identity, which a `ReplayedRun`'s Run must name (item 3 step 1; X5's
    /// "target identity"). Read-only; it admits nothing.
    pub fn project_id(&self) -> &str {
        self.operation.row().project_id()
    }
    /// Unit X3d-2: the selected store's directory `I/stores/S`, for item 3
    /// steps 4 to 6's ledger and objects (law X3c r7 item 1), as one charged
    /// step on the attempt ledger. It is opened no-follow from the retained
    /// I and must hold the marker the endpoint admitted; its absolute
    /// spelling names the same directory. Read-only. Any failure latches the
    /// ledger, and the caller then stops the session with `refused`.
    pub fn store_root(&mut self) -> Result<StoreRoot, WorkFailure<SessionRefusal>> {
        match open_store_root(&mut self.operation) {
            Ok((directory, path, uid)) => Ok(StoreRoot {
                directory,
                path,
                uid,
            }),
            Err(WorkFailure::Budget(budget)) => Err(WorkFailure::Budget(budget)),
            Err(WorkFailure::Operation(row)) => Err(WorkFailure::Operation(SessionRefusal(row))),
        }
    }
    /// Item 3 step 0: take the end-path settlement reserve, first, before
    /// any check that can return a `StoppedSession` (X3d-2's
    /// `prepare_commit` calls this). Its size is item 8's exact cost of one
    /// bounded `REV` and one bounded `CLN` append. A refusal is the budget
    /// row and latches the attempt ledger; the returned `StoppedSession`
    /// holds no reserve. A second call is the invariant row.
    pub fn reserve_end_path(mut self) -> Result<CommitSession, (SessionRefusal, StoppedSession)> {
        if self.end_path.is_some() {
            return Err(refuse(self, invariant()));
        }
        let Some(cost) = end_path_reserve_cost(self.namespace_id(), &self.operation_ref) else {
            return Err(refuse(self, invariant()));
        };
        match self.operation.reserve_end_path_settlement(cost) {
            Ok(reserve) => {
                opensip_platform::crash_barrier!("x3d.session", "settlement-reserved", step);
                self.end_path = Some(EndPath(reserve));
                Ok(self)
            }
            Err(failure) => Err(refuse(self, budget(failure))),
        }
    }
    /// Item 3 step 3 (F32): whether a `SEAL` fits after the tail the
    /// carrier start proved, by X3b's `seal_fits` (no literal threshold). An
    /// exhausted generation is not a refusal: the attempt ledger stays open
    /// and the `StoppedSession` carries the exhaustion to `finish`'s end
    /// step and X3b's rollover.
    pub fn capacity(self) -> Result<CommitSession, (CarrierCapacityExhausted, StoppedSession)> {
        // The tail the start proved, as every certain append since keeps it
        // (no append precedes the SEAL path in M2).
        let carrier = self.operation.carrier();
        let start = carrier.start_tail();
        let (generation, tail) = carrier.lock().proven_tail().unwrap_or((start.0, start.1));
        if seal_fits(tail) {
            return Ok(self);
        }
        let exhausted = CarrierCapacityExhausted {
            grant_generation: generation,
            proven_tail_seq: tail,
        };
        let CommitSession {
            operation,
            execution_id,
            operation_ref,
            end_path,
            ..
        } = self;
        let stopped = StoppedSession {
            operation: Box::new(StoppedOperation {
                admitted_at_close: admitted(close_sample(&operation)),
                operation,
            }),
            ids: Some(Box::new((execution_id, operation_ref))),
            end_path,
            ended: Ended::Exhausted(CapacityExhaustion::new(generation, tail)),
        };
        Err((exhausted, stopped))
    }
    /// One charged step on the attempt ledger for storage's own work under
    /// the session (preflight, the publication reserve, attempt admission,
    /// objects). Any failure latches the ledger; the caller then stops the
    /// session with `refused` or `undetermined`.
    pub fn charge<R, E>(
        &mut self,
        action: impl FnOnce(&mut WorkScope<'_>) -> Result<R, WorkFailure<E>>,
    ) -> Result<R, WorkFailure<E>> {
        self.operation.charge(action)
    }
    /// Item 3: a certain refusal of `prepare_commit` (the caller's row). The
    /// operation stops before admission: the gate latches (X4 r7 item 7),
    /// the reserve is kept for `finish`'s `REV`.
    pub fn refused(self) -> StoppedSession {
        refuse(self, invariant()).1
    }
    /// Item 3 step 4: the attempt-admission `COMMIT` was undetermined. The
    /// reserve is forfeited here, where the outcome is classified (item 8):
    /// `finish` appends nothing and runs no end step.
    pub fn undetermined(self) -> StoppedSession {
        let CommitSession {
            operation,
            execution_id,
            operation_ref,
            end_path,
            ..
        } = self;
        let close = close_sample(&operation);
        forfeit(end_path);
        StoppedSession {
            operation: Box::new(StoppedOperation {
                admitted_at_close: admitted(close),
                operation,
            }),
            ids: Some(Box::new((execution_id, operation_ref))),
            end_path: None,
            ended: Ended::Uncertain,
        }
    }
}
/// A certain refusal of the session: the gate latches (X4 r7 item 7), and the
/// reserve, if taken, is kept for `finish`'s `REV`.
fn refuse(session: CommitSession, row: OperationRow) -> (SessionRefusal, StoppedSession) {
    let CommitSession {
        operation,
        execution_id,
        operation_ref,
        end_path,
        ..
    } = session;
    operation.guard().stop(StopCause::CertainRefusal);
    let stopped = StoppedSession {
        operation: Box::new(StoppedOperation {
            admitted_at_close: admitted(close_sample(&operation)),
            operation,
        }),
        ids: Some(Box::new((execution_id, operation_ref))),
        end_path,
        ended: Ended::Certain(Seal::Absent),
    };
    (SessionRefusal(row), stopped)
}
/// `open`'s refusal: the gate latches; no reserve exists yet.
fn refused(
    operation: ProjectOperation,
    ids: Option<(ReservedExecutionId, String)>,
    row: OperationRow,
) -> (SessionRefusal, StoppedSession) {
    operation.guard().stop(StopCause::CertainRefusal);
    (
        SessionRefusal(row),
        StoppedSession {
            operation: Box::new(StoppedOperation {
                admitted_at_close: admitted(close_sample(&operation)),
                operation,
            }),
            ids: ids.map(Box::new),
            end_path: None,
            ended: Ended::Certain(Seal::Absent),
        },
    )
}

/// Unit X3d-2: the selected store's directory `I/stores/S` as
/// `CommitSession::store_root` opened it, its absolute spelling and the
/// invoking user. A retained handle and values, not authority: it admits no
/// write and nothing accepts it in place of a session.
pub struct StoreRoot {
    directory: RetainedDirectory,
    path: PathBuf,
    uid: u32,
}
impl std::fmt::Debug for StoreRoot {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("StoreRoot")
            .field("path", &self.path)
            .finish_non_exhaustive()
    }
}
impl StoreRoot {
    pub fn directory(&self) -> &RetainedDirectory {
        &self.directory
    }
    pub fn path(&self) -> &Path {
        &self.path
    }
    pub fn uid(&self) -> u32 {
        self.uid
    }
}

/// Item 3 step 3's outcome: the generation an attempt proved full and the
/// tail it proved. A value, not authority.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct CarrierCapacityExhausted {
    grant_generation: i64,
    proven_tail_seq: i64,
}
impl CarrierCapacityExhausted {
    pub fn grant_generation(&self) -> i64 {
        self.grant_generation
    }
    pub fn proven_tail_seq(&self) -> i64 {
        self.proven_tail_seq
    }
}

// ------------------------------------------------------ journal transaction

/// Item 1's `JournalWriteTxn`: the live session and the open level-3
/// journal transaction. No SQL, write or checkpoint method. Private fields;
/// not Clone, Default or serializable; `begin_journal_txn` makes it.
pub struct JournalWriteTxn {
    // Declaration order is drop order: the journal's level 3 rolls back
    // before the operation's lease is released.
    open: DetachedJournal,
    session: CommitSession,
}
impl std::fmt::Debug for JournalWriteTxn {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("JournalWriteTxn")
            .field("session", &self.session)
            .finish_non_exhaustive()
    }
}
impl JournalWriteTxn {
    /// The session's ExecutionId.
    pub fn execution_id(&self) -> &str {
        self.session.execution_id.as_str()
    }
    /// Item 4 step 2: one charged step on the attempt ledger with the
    /// journal's level 3 held, for storage's evidence-ledger `BEGIN
    /// IMMEDIATE` (never waiting). Never under level 4.
    pub fn charge<R, E>(
        &mut self,
        action: impl FnOnce(&mut WorkScope<'_>) -> Result<R, WorkFailure<E>>,
    ) -> Result<R, WorkFailure<E>> {
        self.session.operation.charge(action)
    }
    /// Item 4 step 2's consuming abort (F06): the journal's level 3 rolls
    /// back, the gate latches, and the session stops holding its reserve.
    pub fn abort(self) -> StoppedSession {
        let JournalWriteTxn { open, session } = self;
        drop(open);
        refuse(session, invariant()).1
    }
}

/// Item 4 step 1: the journal's `BEGIN IMMEDIATE` (level 3), never waiting,
/// on the attempt ledger. Busy, I/O or a quarantine is its carrier row, with
/// a `StoppedSession`. A session without the end-path reserve (item 3 step
/// 0) is the invariant row: no `SEAL` path starts unfunded.
pub fn begin_journal_txn(
    session: CommitSession,
) -> Result<JournalWriteTxn, (SessionRefusal, StoppedSession)> {
    let mut session = session;
    if session.end_path.is_none() {
        return Err(refuse(session, invariant()));
    }
    let opened = session
        .operation
        .journal(|location, carrier, _checkpoint, work| {
            // X9: the SEAL append's protocol is `x3b.append.seal` (law X9 r1
            // item 5), from its level 3 on.
            opensip_platform::crash_scope!("x3b.append.seal", {
                carrier
                    .lock()
                    .begin(location, work)
                    .map(|transaction| transaction.detach())
            })
        });
    match opened {
        Ok(open) => Ok(JournalWriteTxn { open, session }),
        Err(failure) => Err(refuse(session, carrier_failure(&failure))),
    }
}

// ---------------------------------------------------------------- the SEAL

/// Item 1's `JournalSealBinding`: read-only evidence of one `SEAL` append,
/// never a grant: the carrier digest, the grant generation, the `SEAL`'s
/// sequence and body digest, the operationRef and the replayed RunId. Made
/// only by `seal_under_append_lock`. Private fields; not Clone, Default or
/// serializable.
#[derive(Debug)]
pub struct JournalSealBinding {
    carrier_digest: String,
    grant_generation: i64,
    seal_seq: i64,
    body_sha256: String,
    operation_ref: String,
    run_id: String,
}
impl JournalSealBinding {
    pub fn carrier_digest(&self) -> &str {
        &self.carrier_digest
    }
    pub fn grant_generation(&self) -> i64 {
        self.grant_generation
    }
    pub fn seal_seq(&self) -> i64 {
        self.seal_seq
    }
    pub fn body_sha256(&self) -> &str {
        &self.body_sha256
    }
    pub fn operation_ref(&self) -> &str {
        &self.operation_ref
    }
    pub fn run_id(&self) -> &str {
        &self.run_id
    }
}

/// Item 1's two-phase adapter, owned here and implemented by storage alone
/// (X3d-2): staging in the open evidence-ledger transaction with nothing
/// committed (item 4 step 3.8), returning the prepared commit.
pub trait CommitAdapter {
    type Staged: StagedCommit;
    type Refusal;
    fn stage(
        self,
        binding: &JournalSealBinding,
        work: &mut WorkScope<'_>,
    ) -> Result<Self::Staged, WorkFailure<Self::Refusal>>;
}
/// The adapter's second phase: the evidence `COMMIT` only (item 4 step
/// 3.10), run only inside the one `AdmissionPermit`'s `consume`.
pub trait StagedCommit {
    type Committed;
    fn commit(self) -> EvidenceCommit<Self::Committed>;
}
/// The evidence `COMMIT`'s durability classification (X3c item 7).
#[derive(Debug, PartialEq, Eq)]
pub enum EvidenceCommit<C> {
    /// `COMMIT` returned success: durable.
    Committed(C),
    /// `COMMIT` errored or the connection was lost: neither state is
    /// inferred.
    Undetermined,
}

/// What `seal_under_append_lock` returns beside the `StoppedSession`.
#[derive(Debug)]
pub enum SealOutcome<C, R> {
    /// The evidence `COMMIT` returned success through the permit.
    /// `latched_after_admission` is a latch that took the gate from 1 to 3
    /// (F39): the outcome stands.
    Committed {
        committed: C,
        binding: JournalSealBinding,
        latched_after_admission: bool,
    },
    /// An uncertain journal commit or barrier, or an undetermined evidence
    /// `COMMIT` (F12, F40): the ExecutionId is retained, there is no RunId,
    /// and nothing follows.
    CommitUndetermined { execution_id: String },
    /// A certain refusal before a permit was used.
    Refused(SealRefusal<R>),
}
/// A certain refusal of the `SEAL` path: the session's own row, or the
/// adapter's staging refusal (storage names its row).
#[derive(Debug)]
pub enum SealRefusal<R> {
    Session(SessionRefusal),
    Staging(R),
}

/// Why the `SEAL` path stopped, inside the attempt ledger's charge.
enum SealStep<R> {
    Carrier(CarrierRefusal),
    Guard(GuardRefusal),
    Staging(R),
    JournalUndetermined,
    EvidenceUndetermined,
    Invariant,
}
fn lifted<R>(failure: WorkFailure<CarrierRefusal>) -> WorkFailure<SealStep<R>> {
    match failure {
        WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
        WorkFailure::Operation(refusal) => WorkFailure::Operation(SealStep::Carrier(refusal)),
    }
}

/// Item 4 step 3, under the journal's level 3 and storage's evidence-ledger
/// level 3, on the attempt ledger:
/// 1. level 4 (`JournalAppendLock`);
/// 2. X4's checkpoint, admitting nothing yet;
/// 3. the `SEAL` built and validated, bound to `replayed` through
///    `PreparedJournalSeal::bind`;
/// 4. to 6. the `SEAL`'s `PENDING` witness, insert and commit (the journal
///    transaction closes), `COMMITTED` witness;
/// 7. X4's checkpoint again (F19);
/// 8. the adapter's staging (`x3d.publish.after-staging`);
/// 9. X4's checkpoint again (`x3d.publish.before-final-checkpoint`), ending
///    in `FinalGate::admit`, which mints the one `AdmissionPermit`;
/// 10. the evidence `COMMIT` through the permit
///     (`x3d.publish.commit-returned`);
/// 11. level 4's release.
///
/// A certain stop after step 1 rolls the evidence transaction back, then
/// releases level 4, then the journal's level 3 if still open, exactly once;
/// it appends nothing (the `REV` and `CLN` are `finish`'s) and latches the
/// gate. An uncertain journal outcome or an undetermined evidence `COMMIT`
/// forfeits the end-path reserve here, where it is classified.
pub fn seal_under_append_lock<A: CommitAdapter>(
    txn: JournalWriteTxn,
    replayed: &ReplayedRun,
    adapter: A,
) -> (
    SealOutcome<<A::Staged as StagedCommit>::Committed, A::Refusal>,
    StoppedSession,
) {
    let JournalWriteTxn { open, session } = txn;
    let CommitSession {
        mut operation,
        execution_id,
        operation_ref,
        carrier_digest,
        end_path,
        ..
    } = session;
    let mut seal_durable = false;
    let result = operation.journal(|location, carrier, checkpoint, work| {
        // X9: `x3b.append.seal` (law X9 r1 item 5) through level 4's
        // release; the X3d, X4 and X3c points inside name their own scopes.
        opensip_platform::crash_scope!("x3b.append.seal", {
            let mut adapter = Some(adapter);
            // Step 1: level 4 from the open journal transaction.
            let mut held = match open
                .attach(carrier.lock(), location)
                .and_then(|transaction| transaction.acquire())
            {
                Ok(held) => held,
                Err(failure) => {
                    drop(adapter.take());
                    return Err(lifted(failure));
                }
            };
            // Step 2: the checkpoint over the level-4 borrow.
            if let Err(refusal) = checkpoint.effect(&held, work) {
                drop(adapter.take());
                drop(held);
                return Err(WorkFailure::Operation(SealStep::Guard(refusal)));
            }
            // Step 3: the SEAL, built and bound to the replay.
            let bound = held
                .seal_record(&operation_ref, replayed.run_id())
                .ok()
                .and_then(|record| PreparedJournalSeal::bind(record, replayed).ok());
            let Some(bound) = bound else {
                drop(adapter.take());
                drop(held);
                return Err(WorkFailure::Operation(SealStep::Invariant));
            };
            // Steps 4 to 6.
            let appended = match held.append_seal(&operation_ref, bound.run_id(), work) {
                Ok(appended) => appended,
                Err(AppendError::Undetermined(_)) => {
                    drop(adapter.take());
                    drop(held);
                    return Err(WorkFailure::Operation(SealStep::JournalUndetermined));
                }
                Err(AppendError::Refused(failure)) => {
                    drop(adapter.take());
                    drop(held);
                    return Err(lifted(failure));
                }
            };
            seal_durable = true;
            let expected = opensip_identity::digest_hex(&bound.journal_body_sha256());
            if appended.body_sha256() != expected || appended.run_id() != Some(bound.run_id()) {
                drop(adapter.take());
                drop(held);
                return Err(WorkFailure::Operation(SealStep::Invariant));
            }
            let binding = JournalSealBinding {
                carrier_digest: carrier_digest.clone(),
                grant_generation: appended.generation(),
                seal_seq: appended.seq(),
                body_sha256: appended.body_sha256().to_owned(),
                operation_ref: appended.operation_ref().to_owned(),
                run_id: bound.run_id().to_owned(),
            };
            // Step 7: the repeated checkpoint after the blocking SEAL work.
            if let Err(refusal) = checkpoint.effect(&held, work) {
                drop(adapter.take());
                drop(held);
                return Err(WorkFailure::Operation(SealStep::Guard(refusal)));
            }
            // Step 8: staging, in the open evidence transaction.
            let staged = match adapter.take().expect("staged once").stage(&binding, work) {
                Ok(staged) => staged,
                Err(WorkFailure::Budget(budget)) => {
                    drop(held);
                    return Err(WorkFailure::Budget(budget));
                }
                Err(WorkFailure::Operation(refusal)) => {
                    drop(held);
                    return Err(WorkFailure::Operation(SealStep::Staging(refusal)));
                }
            };
            opensip_platform::crash_barrier!("x3d.publish", "after-staging", step);
            opensip_platform::crash_barrier!("x3d.publish", "before-final-checkpoint", step);
            // Step 9: the final checkpoint and the one permit.
            let permit = match checkpoint.admit(&held, staged, work) {
                Ok(permit) => permit,
                Err((refusal, staged)) => {
                    drop(staged);
                    drop(held);
                    return Err(WorkFailure::Operation(SealStep::Guard(refusal)));
                }
            };
            // Step 10: the evidence COMMIT, only through the permit.
            let committed = permit.consume(StagedCommit::commit);
            opensip_platform::crash_barrier!("x3d.publish", "commit-returned", step);
            // Step 11: level 4 is released once the COMMIT has returned.
            drop(held);
            match committed {
                EvidenceCommit::Committed(committed) => Ok((committed, binding)),
                EvidenceCommit::Undetermined => {
                    Err(WorkFailure::Operation(SealStep::EvidenceUndetermined))
                }
            }
        })
    });
    // The outcome discloses the reservation's projection; the stopped
    // session keeps the reservation itself.
    let undetermined_id = execution_id.as_str().to_owned();
    let ids = Some(Box::new((execution_id, operation_ref)));
    match result {
        Ok((committed, binding)) => {
            let close = close_sample(&operation);
            let latched_after_admission = close == AttemptState::AdmittedThenLatched;
            let stopped = StoppedSession {
                operation: Box::new(StoppedOperation {
                    admitted_at_close: admitted(close),
                    operation,
                }),
                ids,
                end_path,
                ended: Ended::Certain(Seal::Committed),
            };
            (
                SealOutcome::Committed {
                    committed,
                    binding,
                    latched_after_admission,
                },
                stopped,
            )
        }
        Err(WorkFailure::Operation(
            SealStep::JournalUndetermined | SealStep::EvidenceUndetermined,
        )) => {
            // Item 8: the reserve is forfeited where the outcome is
            // classified; nothing follows an uncertain outcome.
            let close = close_sample(&operation);
            forfeit(end_path);
            let stopped = StoppedSession {
                operation: Box::new(StoppedOperation {
                    admitted_at_close: admitted(close),
                    operation,
                }),
                ids,
                end_path: None,
                ended: Ended::Uncertain,
            };
            (
                SealOutcome::CommitUndetermined {
                    execution_id: undetermined_id,
                },
                stopped,
            )
        }
        Err(failure) => {
            operation.guard().stop(StopCause::CertainRefusal);
            let refusal = match failure {
                WorkFailure::Budget(_) => {
                    SealRefusal::Session(SessionRefusal(OperationRow::BudgetExhausted))
                }
                WorkFailure::Operation(SealStep::Carrier(refusal)) => {
                    SealRefusal::Session(SessionRefusal(OperationRow::Carrier(refusal.row())))
                }
                WorkFailure::Operation(SealStep::Guard(refusal)) => {
                    SealRefusal::Session(SessionRefusal(refusal.row()))
                }
                WorkFailure::Operation(SealStep::Staging(refusal)) => SealRefusal::Staging(refusal),
                WorkFailure::Operation(
                    SealStep::Invariant
                    | SealStep::JournalUndetermined
                    | SealStep::EvidenceUndetermined,
                ) => SealRefusal::Session(SessionRefusal(invariant())),
            };
            let stopped = StoppedSession {
                operation: Box::new(StoppedOperation {
                    admitted_at_close: admitted(close_sample(&operation)),
                    operation,
                }),
                ids,
                end_path,
                ended: Ended::Certain(if seal_durable {
                    Seal::WithoutEvidence
                } else {
                    Seal::Absent
                }),
            };
            (SealOutcome::Refused(refusal), stopped)
        }
    }
}

// ------------------------------------------------------------- the end path

/// Whether this operation's `SEAL` was made durable, and committed.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Seal {
    Absent,
    WithoutEvidence,
    Committed,
}
/// How the session ended. `Uncertain` never holds a reserve.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Ended {
    Certain(Seal),
    Exhausted(CapacityExhaustion),
    Uncertain,
}

// Keep the close sample in the existing operation allocation, so the
// stopped-session refusal stays small without a second allocation.
struct StoppedOperation {
    admitted_at_close: bool,
    operation: ProjectOperation,
}

/// Item 1's `StoppedSession`: the operation's lease and end-path owners,
/// admitting cleanup only, and the end-path reserve if item 3 step 0 took
/// it and no uncertain outcome forfeited it. Every end of the session makes
/// one; `finish` consumes it. Private fields; not Clone, Default or
/// serializable.
pub struct StoppedSession {
    // Boxed: the operation is large, and a stopped session travels in every
    // refusal beside its row.
    operation: Box<StoppedOperation>,
    // The ExecutionId and operationRef, if `open` drew them; boxed with the
    // operation, so that a refusal and its stopped session stay small. The
    // ExecutionId is the session's reservation (X3d r9 S10.1).
    ids: Option<Box<(ReservedExecutionId, String)>>,
    end_path: Option<EndPath>,
    ended: Ended,
}
impl std::fmt::Debug for StoppedSession {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("StoppedSession")
            .field("ids", &self.ids)
            .field("reserved", &self.end_path.is_some())
            .field("ended", &self.ended)
            .finish_non_exhaustive()
    }
}

/// Why the end path's settlement stopped.
enum EndStep {
    /// A draft beyond its kind's bound, before any effect.
    Bound,
    Carrier(CarrierRefusal),
    /// An end-path append ended durability-undetermined.
    Undetermined,
}
fn end_lifted(failure: WorkFailure<CarrierRefusal>) -> WorkFailure<EndStep> {
    match failure {
        WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
        WorkFailure::Operation(refusal) => WorkFailure::Operation(EndStep::Carrier(refusal)),
    }
}

impl StoppedSession {
    pub fn admitted_at_close(&self) -> bool {
        self.operation.admitted_at_close
    }
    /// The session's ExecutionId, if `open` drew one.
    pub fn execution_id(&self) -> Option<&str> {
        self.ids.as_ref().map(|ids| ids.0.as_str())
    }
    /// Item 7: the end path, with X4c merged.
    /// 1. While the lease is still held: a `REV` is owed if a durable `SEAL`
    ///    has no evidence commit, the gate is latched, or a revocation was
    ///    observed; a `CLN` is owed for F38's `SEAL` without its commit.
    ///    Owed records are appended in one `settle` of the reserve, the `REV`
    ///    first, each through a fresh level-3-then-level-4 append with no
    ///    checkpoint. A failure inside the settlement ends it (no `CLN` after
    ///    a failed `REV`, no retry). Nothing owed: the reserve is dropped
    ///    unspent. No reserve (step 0 refused, or an uncertain outcome
    ///    forfeited it): nothing is appended.
    /// 2. The lease is released.
    /// 3. X3b's end step runs, unless an outcome was uncertain or the attempt
    ///    ledger is closed.
    pub fn finish(self) -> SessionEnd {
        let StoppedSession {
            operation,
            ids,
            end_path,
            ended,
            ..
        } = self;
        let StoppedOperation { mut operation, .. } = *operation;
        let seal = match ended {
            Ended::Certain(seal) => seal,
            Ended::Exhausted(_) | Ended::Uncertain => Seal::Absent,
        };
        let guard = operation.guard();
        let latched = matches!(
            guard.state(),
            AttemptState::LatchedBeforeAdmission | AttemptState::AdmittedThenLatched
        );
        let cause = guard.cause();
        let revoked = matches!(cause, Some(StopCause::Revoked { .. }));
        let without_evidence = seal == Seal::WithoutEvidence;
        let mut owed = Vec::new();
        if without_evidence || latched || revoked {
            owed.push((EndRecord::Rev, RevReason::of(cause.as_ref()).draft()));
        }
        if without_evidence {
            owed.push((EndRecord::Cln, cleanup_draft()));
        }
        let mut appended = Vec::new();
        let mut undetermined = ended == Ended::Uncertain;
        let mut settlement = None;
        match (end_path, &ids) {
            (Some(EndPath(reserve)), Some(ids)) if !owed.is_empty() => {
                let operation_ref = &ids.1;
                let n = operation.binding().namespace_id().to_owned();
                opensip_platform::crash_barrier!("x3d.finish", "settle.before", step);
                let settled = operation.settle_end_path(reserve, |location, carrier, work| {
                    for (kind, draft) in &owed {
                        admit_end_draft(&n, operation_ref, *kind, draft)
                            .map_err(WorkFailure::Operation)?;
                        // X9: `x3b.append.rev` or `.cln` (law X9 r1 item 5).
                        let appended_record = opensip_platform::crash_scope!(
                            match kind {
                                EndRecord::Rev => "x3b.append.rev",
                                EndRecord::Cln => "x3b.append.cln",
                            },
                            {
                                carrier
                                    .lock()
                                    .begin(location, work)
                                    .and_then(|transaction| transaction.acquire())
                                    .map_err(end_lifted)
                                    .map(|held| held.append(operation_ref, draft, work))
                            }
                        )?;
                        match appended_record {
                            Ok(record) => appended.push(record.record_type()),
                            Err(AppendError::Undetermined(_)) => {
                                return Err(WorkFailure::Operation(EndStep::Undetermined));
                            }
                            Err(AppendError::Refused(failure)) => return Err(end_lifted(failure)),
                        }
                    }
                    Ok(())
                });
                opensip_platform::crash_barrier!("x3d.finish", "settle.after", step);
                if let Err(failure) = settled {
                    let row = match failure {
                        WorkFailure::Budget(_) => T::BudgetExhausted,
                        WorkFailure::Operation(EndStep::Bound) => T::Invariant,
                        WorkFailure::Operation(EndStep::Carrier(refusal)) => {
                            carrier_termination(refusal.row())
                        }
                        WorkFailure::Operation(EndStep::Undetermined) => {
                            undetermined = true;
                            T::CommitUndetermined
                        }
                    };
                    settlement = Some(row);
                }
            }
            // Nothing owed: dropped unspent, never refunded.
            (end_path, _) => forfeit(end_path),
        }
        let outcome = match (undetermined, ended, ids) {
            (true, ..) => JournalOutcome::Uncertain,
            (false, Ended::Exhausted(exhaustion), Some(ids)) => JournalOutcome::Exhausted {
                exhaustion,
                operation_ref: ids.1,
            },
            _ => JournalOutcome::Certain,
        };
        let end = operation.end(outcome);
        SessionEnd {
            appended,
            settlement,
            end,
        }
    }
}

/// What `finish` did. None of it rewrites the outcome the session returned:
/// a failed end-path append is an end failure on its existing row (item 9).
#[derive(Debug)]
pub struct SessionEnd {
    appended: Vec<&'static str>,
    settlement: Option<T>,
    end: OperationEnd,
}
impl SessionEnd {
    /// Whether the end path appended this operation's `REV`.
    pub fn revocation_appended(&self) -> bool {
        self.appended.contains(&"REV")
    }
    /// Whether the end path appended this operation's `CLN`.
    pub fn cleanup_appended(&self) -> bool {
        self.appended.contains(&"CLN")
    }
    /// The disclosed row of a failed end-path settlement, if it failed.
    pub fn settlement_failure(&self) -> Option<&T> {
        self.settlement.as_ref()
    }
    /// Whether X3b's end step was entered (it is not after an uncertain
    /// outcome or on a closed attempt ledger; not entering it is not a
    /// failure).
    pub fn end_step_entered(&self) -> bool {
        !matches!(self.end, OperationEnd::NotEntered)
    }
    /// Law X7 r5 item 6 (unit X7b): the disclosed row of X3b's end step, if
    /// it was entered and failed: the walk, the fence, a rebind, the floor
    /// copy (after a rollover too) or the fence's unlock (X3b r10 item 4).
    /// An end step not entered is not a failure and is not disclosed (X3d
    /// r6 item 9). Never rewrites the session's outcome.
    pub fn end_step_failure(&self) -> Option<T> {
        match &self.end {
            OperationEnd::NotEntered
            | OperationEnd::Ended(_)
            | OperationEnd::RolledOver { end: Ok(_), .. } => None,
            OperationEnd::RolledOver {
                end: Err(failure), ..
            }
            | OperationEnd::Failed(failure) => Some(operation_termination(&failure.row())),
        }
    }
    /// Law X7 r5 item 6 (unit X7b): the rollover's outcome, when the end
    /// step ran it after a `CarrierCapacityExhausted` attempt (X3b r10 item
    /// 13). `None` when no rollover was attempted: any other outcome, an end
    /// step not entered, or one that stopped before the rollover.
    pub fn rollover(&self) -> Option<RolloverDisclosure> {
        match &self.end {
            OperationEnd::RolledOver { rollover, .. } => Some(RolloverDisclosure::of(rollover)),
            OperationEnd::NotEntered | OperationEnd::Ended(_) | OperationEnd::Failed(_) => None,
        }
    }
}

/// Law X7 r5 item 6 (unit X7b): what the capacity rollover in `finish`'s end
/// step did, as X3b r10 item 13 returns it. A disclosure value only: it
/// carries no lease, lock, carrier, ledger or receipt, and building one
/// grants nothing. None of it rewrites the attempt's outcome, which stays
/// on X7 item 6a's busy row.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum RolloverDisclosure {
    /// G was closed by a `TERMINAL` (appended now, or already durable when
    /// only OPEN ran), and this generation was opened.
    Rolled { opened_generation: i64 },
    /// G was already closed and its successor open, or a later generation
    /// has rows. Nothing was written.
    AlreadyRolled,
    /// `writer.lease` or `readers.lease` was busy: nothing was written, and
    /// the next writer that reaches the exhaustion takes the route.
    Skipped,
    /// A certain refusal, on its own row (X3b item 8, or the budget row).
    Refused(T),
    /// The `TERMINAL` append or OPEN failed after visibility. Nothing
    /// followed; the next writer's floor step and start reconcile.
    Undetermined,
}
impl RolloverDisclosure {
    fn of(outcome: &RolloverOutcome) -> Self {
        match outcome {
            RolloverOutcome::Rolled { opened, .. } => Self::Rolled {
                opened_generation: *opened,
            },
            RolloverOutcome::AlreadyRolled => Self::AlreadyRolled,
            RolloverOutcome::Skipped => Self::Skipped,
            RolloverOutcome::Refused(failure) => {
                Self::Refused(operation_termination(&carrier_failure(failure)))
            }
            RolloverOutcome::Undetermined(_) => Self::Undetermined,
        }
    }
}
#[cfg(test)]
impl SessionEnd {
    pub(super) fn end(&self) -> &OperationEnd {
        &self.end
    }
}

#[cfg(test)]
pub(super) mod end_path_for_tests {
    //! The end path's closed drafts and bounds, for the unit's tests.
    use super::*;
    /// Unit X7b: a `SessionEnd` around a real end-step result, which the
    /// handoff's tests produce at X3b-4's test points (no production path
    /// reaches those faults through `finish`).
    pub(in super::super) fn session_end(end: OperationEnd) -> SessionEnd {
        SessionEnd {
            appended: Vec::new(),
            settlement: None,
            end,
        }
    }
    pub(in super::super) fn reserve_cost(n: &str, operation_ref: &str) -> Option<WorkCost> {
        end_path_reserve_cost(n, operation_ref)
    }
    pub(in super::super) fn longest_rev() -> RecordDraft {
        RevReason::ALL
            .iter()
            .max_by_key(|r| r.spelling().len())
            .expect("closed set")
            .draft()
    }
    pub(in super::super) fn cleanup() -> RecordDraft {
        cleanup_draft()
    }
    pub(in super::super) fn admits(
        n: &str,
        operation_ref: &str,
        rev: bool,
        draft: &RecordDraft,
    ) -> bool {
        let kind = if rev { EndRecord::Rev } else { EndRecord::Cln };
        admit_end_draft(n, operation_ref, kind, draft).is_ok()
    }
    pub(in super::super) fn reasons() -> Vec<&'static str> {
        RevReason::ALL.iter().map(|r| r.spelling()).collect()
    }
    /// Law X4 r8 W-6 (unit X4-F3): `finish`'s `REV` reason for a recorded
    /// first cause.
    pub(in super::super) fn reason(cause: Option<&StopCause>) -> &'static str {
        RevReason::of(cause).spelling()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::journal_store::CarrierRefusalRow as Row;

    /// Item 9: every carrier row, as S12 spells its termination.
    #[test]
    fn every_carrier_row_maps_to_its_existing_termination() {
        for (row, termination) in [
            (Row::Busy, T::Busy),
            (Row::LedgerCorrupt, T::LedgerCorrupt),
            (Row::MigrationCorrupt, T::MigrationCorrupt),
            (Row::InheritedCarrier, T::HostIo),
            (Row::HostIo, T::HostIo),
            (Row::Invariant, T::Invariant),
            (Row::DurabilityUndetermined, T::CommitUndetermined),
        ] {
            assert_eq!(carrier_termination(row), termination, "{row:?}");
            assert_eq!(
                SessionRefusal(OperationRow::Carrier(row)).termination(),
                termination
            );
        }
    }

    /// Item 9 with X4 r7 item 8: a stale owner keeps its own X2 row.
    #[test]
    fn every_project_row_maps_to_its_existing_termination() {
        use ProjectAdmissionRow as A;
        use RegistrationRow as R;
        for (row, termination) in [
            (
                R::Admission(A::RootCustody("walk-depth-exceeded")),
                T::ProjectRootCustody {
                    subject: "walk-depth-exceeded",
                },
            ),
            (
                R::Admission(A::ConfigCustody("symlink")),
                T::Custody { subject: "symlink" },
            ),
            (R::Admission(A::ExplicitPath), T::ProjectExplicitPath),
            (R::Admission(A::Incomplete), T::Incomplete),
            (
                R::Admission(A::RequiredFilesChanged),
                T::Custody {
                    subject: "required-files-changed",
                },
            ),
            (R::Admission(A::HostIo), T::HostIo),
            (
                R::RootCustody("identity-contradiction"),
                T::ProjectRootCustody {
                    subject: "identity-contradiction",
                },
            ),
            (
                R::InstallationCustody("private"),
                T::Custody { subject: "private" },
            ),
            (R::Incomplete, T::Incomplete),
            (
                R::ScopeLimit("pathPrefixes:65537>65536".into()),
                T::ProjectScopeLimit {
                    subject: "pathPrefixes:65537>65536".into(),
                },
            ),
            (R::HostIo, T::HostIo),
            (R::Invariant, T::Invariant),
            (R::Busy, T::Busy),
        ] {
            let row = OperationRow::Project(ProjectWriteRow::Project(row));
            assert_eq!(operation_termination(&row), termination, "{row:?}");
        }
        assert_eq!(
            operation_termination(&OperationRow::Project(ProjectWriteRow::BudgetExhausted)),
            T::BudgetExhausted
        );
        assert_eq!(
            operation_termination(&OperationRow::Project(ProjectWriteRow::Installation(
                T::Busy
            ))),
            T::Busy
        );
        assert_eq!(
            operation_termination(&OperationRow::BudgetExhausted),
            T::BudgetExhausted
        );
    }

    #[test]
    fn ids_render_as_their_grammars() {
        let id = render_id("exec1_", [0xab; 16]);
        assert!(lawful_execution_id(&id));
        assert_eq!(id, format!("exec1_{}", "ab".repeat(16)));
        assert!(!lawful_execution_id(&format!("exec1_{}", "AB".repeat(16))));
        assert!(!lawful_execution_id(&format!("exec1_{}", "ab".repeat(15))));
        assert!(!lawful_execution_id("exec1_"));
        assert_eq!(render_id("op-", [0; 16]), format!("op-{}", "0".repeat(32)));
    }

    // ---------------------------------------- X7b: the end-step disclosure

    use crate::journal_store::EndOutcome;

    /// A `SessionEnd` around an end-step result (unit X7b); the real routes
    /// are `commit_session_tests.rs`'s.
    fn ended(end: OperationEnd) -> SessionEnd {
        end_path_for_tests::session_end(end)
    }
    fn rolled_over(rollover: RolloverOutcome, end: EndOutcome) -> SessionEnd {
        ended(OperationEnd::RolledOver {
            rollover,
            end: Ok(end),
        })
    }

    /// Law X7 r5 item 6: each rollover outcome, as X3b r10 item 13 returns
    /// it, is disclosed as itself, and each certain refusal on its own row:
    /// busy, host I/O, quarantine, an invariant and budget. An uncertain one
    /// is `Undetermined`, which X7 discloses on `DURABILITY.COMMIT_FAILED`. A
    /// floor copy not run after a rollover that closed the attempt ledger is
    /// not an end-step failure.
    #[test]
    fn every_rollover_outcome_is_disclosed_as_itself() {
        use RolloverDisclosure as D;
        let refused = |refusal| RolloverOutcome::Refused(WorkFailure::Operation(refusal));
        for (outcome, end, disclosed) in [
            (
                RolloverOutcome::Rolled {
                    closed: (1, 9_007_199_254_740_991),
                    opened: 2,
                },
                EndOutcome::CopiedForward,
                D::Rolled {
                    opened_generation: 2,
                },
            ),
            (
                RolloverOutcome::AlreadyRolled,
                EndOutcome::Unchanged,
                D::AlreadyRolled,
            ),
            (RolloverOutcome::Skipped, EndOutcome::Skipped, D::Skipped),
            (
                refused(CarrierRefusal::Busy),
                EndOutcome::NotCopied,
                D::Refused(T::Busy),
            ),
            (
                refused(CarrierRefusal::Unreadable),
                EndOutcome::NotCopied,
                D::Refused(T::HostIo),
            ),
            (
                refused(CarrierRefusal::Binding),
                EndOutcome::NotCopied,
                D::Refused(T::LedgerCorrupt),
            ),
            (
                refused(CarrierRefusal::Footprint),
                EndOutcome::NotCopied,
                D::Refused(T::MigrationCorrupt),
            ),
            (
                refused(CarrierRefusal::NoSuccessor),
                EndOutcome::NotCopied,
                D::Refused(T::Invariant),
            ),
            (
                RolloverOutcome::Refused(WorkFailure::Budget(WorkBudgetError::Bytes)),
                EndOutcome::NotCopied,
                D::Refused(T::BudgetExhausted),
            ),
            (
                RolloverOutcome::Undetermined(WorkFailure::Operation(CarrierRefusal::Busy)),
                EndOutcome::NotCopied,
                D::Undetermined,
            ),
        ] {
            let end = rolled_over(outcome, end);
            assert!(end.end_step_entered());
            assert_eq!(end.end_step_failure(), None);
            assert_eq!(end.rollover(), Some(disclosed));
        }
    }

    /// X3d r6 item 9: an end step not entered is not disclosed, and a
    /// completed one discloses nothing. Neither is a rollover. (A failed one
    /// is `commit_session_tests.rs`'s, on real end steps.)
    #[test]
    fn an_end_step_not_entered_or_completed_discloses_nothing() {
        for end in [
            OperationEnd::NotEntered,
            OperationEnd::Ended(EndOutcome::CopiedForward),
            OperationEnd::Ended(EndOutcome::Unchanged),
            OperationEnd::Ended(EndOutcome::Skipped),
        ] {
            let end = ended(end);
            assert_eq!(end.end_step_failure(), None);
            assert_eq!(end.rollover(), None);
        }
    }
}
