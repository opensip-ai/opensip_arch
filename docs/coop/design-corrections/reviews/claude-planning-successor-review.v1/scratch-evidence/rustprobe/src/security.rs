//! Security: depends on contracts, evaluator, platform. NO storage dependency.
use std::sync::atomic::{AtomicU8, Ordering};
use contracts::{ExecutionId, NamespaceId, Refusal};
use evaluator::ReplayedRun;
use platform::WriterGuard;

/// Public opaque security type; only security admission mints it.
pub struct CommitSession {
    namespace: NamespaceId,
    store_generation: i64,
    execution: ExecutionId,
    operation_ref: String,
    guard: WriterGuard,
}
impl CommitSession {
    pub fn namespace(&self) -> NamespaceId { self.namespace }
    pub fn store_generation(&self) -> i64 { self.store_generation }
    pub fn execution(&self) -> ExecutionId { self.execution }
    pub fn operation_ref(&self) -> &str { &self.operation_ref }
    pub fn guard_live(&self) -> bool { self.guard.is_live() }
}

pub fn admit_commit_session(namespace: NamespaceId, store_generation: i64,
                            execution: ExecutionId, guard: WriterGuard)
                            -> Result<CommitSession, Refusal> {
    if store_generation < 0 { return Err(Refusal::Admission); }
    Ok(CommitSession { namespace, store_generation, execution,
        operation_ref: format!("op-{:032x}", execution.0), guard })
}

/// Opaque security-owned txn; consumes the session, no public SQL/write method.
pub struct JournalWriteTxn { session: CommitSession, journal_seq: i64 }

pub fn begin_journal_txn(session: CommitSession) -> Result<JournalWriteTxn, Refusal> {
    Ok(JournalWriteTxn { session, journal_seq: 41 })
}

/// Security-owned, privately constructed evidence of the durable append.
pub struct JournalSealBinding {
    carrier_digest: String, grant_generation: i64, journal_seq: i64,
    body_sha256: String, operation_ref: String, run_id: String,
    namespace: NamespaceId, execution: ExecutionId, store_generation: i64,
}
impl JournalSealBinding {
    pub fn carrier_digest(&self) -> &str { &self.carrier_digest }
    pub fn grant_generation(&self) -> i64 { self.grant_generation }
    pub fn journal_seq(&self) -> i64 { self.journal_seq }
    pub fn body_sha256(&self) -> &str { &self.body_sha256 }
    pub fn operation_ref(&self) -> &str { &self.operation_ref }
    pub fn run_id(&self) -> &str { &self.run_id }
    pub fn namespace(&self) -> NamespaceId { self.namespace }
    pub fn execution(&self) -> ExecutionId { self.execution }
    pub fn store_generation(&self) -> i64 { self.store_generation }
}

/// Two-phase adapter trait OWNED BY SECURITY; implementation private to storage.
pub trait CommitStaging {
    type Prepared: PreparedLedgerCommit;
    fn stage(self, binding: &JournalSealBinding) -> Result<Self::Prepared, Refusal>;
}
pub trait PreparedLedgerCommit {
    fn commit(self) -> Result<(), Refusal>;
}

pub struct SealOutcome { durable_seal_seq: i64 }
impl SealOutcome { pub fn durable_seal_seq(&self) -> i64 { self.durable_seal_seq } }

/// Cleanup-only session that still owns the operation lease.
pub struct StoppedSession { session: CommitSession }
impl StoppedSession {
    pub fn operation_ref(&self) -> &str { self.session.operation_ref() }
    pub fn record_rev_cleanup(self) -> Result<(), Refusal> { Ok(()) }
}

/// Single atomic attempt state arbitrating observer latch vs commit admission.
pub const ATT_PREPARING: u8 = 0;
pub const ATT_COMMIT_ADMITTED: u8 = 1;
pub const ATT_LATCHED: u8 = 2;

pub struct AttemptState(AtomicU8);
impl AttemptState {
    pub fn new() -> Self { AttemptState(AtomicU8::new(ATT_PREPARING)) }
    /// Observer fail-stop latch, taken outside the append mutex.
    pub fn latch(&self) -> bool {
        self.0.compare_exchange(ATT_PREPARING, ATT_LATCHED, Ordering::SeqCst, Ordering::SeqCst).is_ok()
    }
    /// Commit admission; wins before the commit syscall.
    pub fn admit_commit(&self) -> bool {
        self.0.compare_exchange(ATT_PREPARING, ATT_COMMIT_ADMITTED, Ordering::SeqCst, Ordering::SeqCst).is_ok()
    }
    pub fn state(&self) -> u8 { self.0.load(Ordering::SeqCst) }
}

/// Security owns the checkpoint/witness sequence: consumes the txn, borrows the run.
pub fn seal_under_append_lock<A: CommitStaging>(txn: JournalWriteTxn, run: &ReplayedRun,
                                                attempt: &AttemptState, adapter: A)
                                                -> Result<(SealOutcome, StoppedSession), (Refusal, StoppedSession)> {
    let JournalWriteTxn { session, journal_seq } = txn;
    // durable SEAL + PENDING -> COMMITTED witness happen here (elided)
    let binding = JournalSealBinding {
        carrier_digest: String::from("c0ffee"), grant_generation: 7, journal_seq,
        body_sha256: String::from("b0dy"), operation_ref: String::from(session.operation_ref()),
        run_id: String::from(run.run_id()), namespace: session.namespace(),
        execution: session.execution(), store_generation: session.store_generation(),
    };
    // Phase 1: at-most-once staging; may fail without issuing an evidence commit.
    let prepared = match adapter.stage(&binding) {
        Ok(p) => p,
        Err(e) => return Err((e, StoppedSession { session })),
    };
    // Phase 2: atomically arbitrate latch vs commit admission, then consume the one method.
    if !attempt.admit_commit() {
        return Err((Refusal::Latched, StoppedSession { session }));
    }
    match prepared.commit() {
        Ok(()) => Ok((SealOutcome { durable_seal_seq: journal_seq }, StoppedSession { session })),
        Err(e) => Err((e, StoppedSession { session })),
    }
}

/// Consuming abort path for a failed second (evidence) level-3 acquisition.
/// Returns the stopped session so the host can still record REV/cleanup.
pub fn abort_journal_txn(txn: JournalWriteTxn) -> StoppedSession {
    let JournalWriteTxn { session, journal_seq } = txn;
    let _ = journal_seq;
    StoppedSession { session }
}
