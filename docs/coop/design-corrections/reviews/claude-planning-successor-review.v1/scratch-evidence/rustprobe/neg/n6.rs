// N6: clone a CommitSession
use contracts::{ExecutionId, NamespaceId};
pub fn dup() {
    let g = platform::WriterGuard::acquire().unwrap();
    let s = security::admit_commit_session(NamespaceId(1), 5, ExecutionId(9), g).unwrap();
    let _c = s.clone();
}
