//! Storage: contracts + evaluator + platform + security. Security never depends on storage.
use contracts::Refusal;
use evaluator::ReplayedRun;
use security::{abort_journal_txn, begin_journal_txn, seal_under_append_lock, AttemptState, CommitSession,
               CommitStaging, JournalSealBinding, PreparedLedgerCommit};

/// Private ledger connection/transaction: never escapes the crate.
struct LedgerTxn { staged: Option<(String, u128)>, committed: bool }
impl LedgerTxn {
    fn acquire_non_waiting() -> Result<LedgerTxn, Refusal> {
        Ok(LedgerTxn { staged: None, committed: false })
    }
}

/// Storage-private adapter implementation holding the already-open evidence txn.
struct LedgerStaging<T> { txn: T, expected_run: String, next_commit_seq: u128 }
struct PreparedLedger<T> { txn: T }

impl<T: AsMut<LedgerTxn>> CommitStaging for LedgerStaging<T> {
    type Prepared = PreparedLedger<T>;
    fn stage(mut self, b: &JournalSealBinding) -> Result<Self::Prepared, Refusal> {
        if b.run_id() != self.expected_run { return Err(Refusal::Ledger); }
        if b.journal_seq() > 9007199254740990 { return Err(Refusal::Carrier); }
        if b.grant_generation() <= 0 { return Err(Refusal::Carrier); }
        // storage owns receipt/association values; security manufactures neither
        let seq = self.next_commit_seq;
        self.txn.as_mut().staged = Some((String::from(b.run_id()), seq));
        Ok(PreparedLedger { txn: self.txn })
    }
}
impl<T: AsMut<LedgerTxn>> PreparedLedgerCommit for PreparedLedger<T> {
    fn commit(mut self) -> Result<(), Refusal> {
        if self.txn.as_mut().staged.is_none() { return Err(Refusal::Ledger); }
        self.txn.as_mut().committed = true;
        Ok(())
    }
}
struct TxnRef<T>(T);
impl<A> AsMut<LedgerTxn> for TxnRef<A> where A: AsMut<LedgerTxn> {
    fn as_mut(&mut self) -> &mut LedgerTxn { self.0.as_mut() }
}
struct Owned(LedgerTxn);
impl AsMut<LedgerTxn> for Owned { fn as_mut(&mut self) -> &mut LedgerTxn { &mut self.0 } }

/// Public opaque; returned only by prepare_commit; owns both prerequisites.
pub struct PreparedCommit { run: ReplayedRun, session: CommitSession }

/// Public opaque storage result; constructor private to durable commit validation.
pub struct PublishedCommit { receipt_run_id: String, commit_sequence: u128, seal_seq: i64 }
impl PublishedCommit {
    pub fn receipt_run_id(&self) -> &str { &self.receipt_run_id }
    pub fn commit_sequence(&self) -> u128 { self.commit_sequence }
    pub fn seal_seq(&self) -> i64 { self.seal_seq }
}

pub fn prepare_commit(run: ReplayedRun, session: CommitSession) -> Result<PreparedCommit, Refusal> {
    if session.store_generation() < 0 { return Err(Refusal::Admission); }
    if !session.guard_live() { return Err(Refusal::Admission); }
    Ok(PreparedCommit { run, session })
}

impl PreparedCommit {
    /// The only publication path; accepts no external adapter and no external SealOutcome.
    pub fn publish(self, attempt: &AttemptState) -> Result<PublishedCommit, Refusal> {
        let PreparedCommit { run, session } = self;
        let expected_run = String::from(run.run_id());
        // fixed order: grant-journal level 3, then evidence ledger level 3, both non-waiting
        let jtxn = begin_journal_txn(session)?;
        let mut ledger = match LedgerTxn::acquire_non_waiting() {
            Ok(l) => Owned(l),
            Err(e) => { let stopped = abort_journal_txn(jtxn); let _ = stopped.record_rev_cleanup(); return Err(e); }
        };
        let adapter = LedgerStaging { txn: TxnRef(&mut ledger), expected_run, next_commit_seq: 42 };
        let outcome = match seal_under_append_lock(jtxn, &run, attempt, adapter) {
            Ok((o, stopped)) => { let _ = stopped.record_rev_cleanup(); o }
            Err((e, stopped)) => { let _ = stopped.record_rev_cleanup(); return Err(e); }
        };
        if !ledger.0.committed { return Err(Refusal::Ledger); }
        let (rid, seq) = ledger.0.staged.take().ok_or(Refusal::Ledger)?;
        Ok(PublishedCommit { receipt_run_id: rid, commit_sequence: seq, seal_seq: outcome.durable_seal_seq() })
    }
}
