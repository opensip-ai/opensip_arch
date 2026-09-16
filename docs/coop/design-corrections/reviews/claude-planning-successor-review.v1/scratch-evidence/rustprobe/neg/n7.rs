// N7: any crate depending on security can implement the public staging trait
use contracts::{ExecutionId, NamespaceId, Refusal};
use security::{CommitStaging, JournalSealBinding, PreparedLedgerCommit};
struct HostAdapter;
struct HostPrepared;
impl CommitStaging for HostAdapter {
    type Prepared = HostPrepared;
    fn stage(self, _b: &JournalSealBinding) -> Result<HostPrepared, Refusal> { Ok(HostPrepared) }
}
impl PreparedLedgerCommit for HostPrepared {
    fn commit(self) -> Result<(), Refusal> { Ok(()) }
}
pub fn drive_seal_without_storage() -> bool {
    let g = platform::WriterGuard::acquire().unwrap();
    let s = security::admit_commit_session(NamespaceId(1), 5, ExecutionId(9), g).unwrap();
    let t = security::begin_journal_txn(s).unwrap();
    let c = contracts::RunCandidate { closure_bytes: vec![1u8,2,3], claimed_run_id: String::from("run3:00000006") };
    let run = evaluator::replay(&c).unwrap();
    let att = security::AttemptState::new();
    security::seal_under_append_lock(t, &run, &att, HostAdapter).is_ok()
}
