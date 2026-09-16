// N3: reuse a consumed CommitSession
use contracts::{ExecutionId, NamespaceId};
pub fn reuse() {
    let g = platform::WriterGuard::acquire().unwrap();
    let s = security::admit_commit_session(NamespaceId(1), 5, ExecutionId(9), g).unwrap();
    let _t1 = security::begin_journal_txn(s);
    let _t2 = security::begin_journal_txn(s);
}
