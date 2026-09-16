struct CommitSession;
struct JournalWriteTxn { session: CommitSession }
fn begin_journal_txn(session: CommitSession) -> JournalWriteTxn { JournalWriteTxn{session} }
fn seal_under_append_lock(txn: JournalWriteTxn) { let _session=txn.session; }
fn main() { let session=CommitSession; let txn=begin_journal_txn(session); seal_under_append_lock(txn); }
