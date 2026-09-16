// N4: the rejected borrow-then-move sketch (E0505 shape)
use contracts::{ExecutionId, NamespaceId};
fn borrow_txn(_s: &security::CommitSession) -> u8 { 0 }
pub fn sketch() {
    let g = platform::WriterGuard::acquire().unwrap();
    let s = security::admit_commit_session(NamespaceId(1), 5, ExecutionId(9), g).unwrap();
    let borrowed = &s;
    let _t = security::begin_journal_txn(s);
    let _x = borrow_txn(borrowed);
}
