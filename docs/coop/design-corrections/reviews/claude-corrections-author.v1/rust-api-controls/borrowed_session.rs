use std::marker::PhantomData;
struct CommitSession;
struct JournalWriteTxn<'s>(PhantomData<&'s CommitSession>);
fn begin_journal_txn<'s>(_: &'s CommitSession) -> JournalWriteTxn<'s> { JournalWriteTxn(PhantomData) }
fn seal_under_append_lock(_: JournalWriteTxn<'_>, _: CommitSession) {}
fn main() { let session=CommitSession; let txn=begin_journal_txn(&session); seal_under_append_lock(txn,session); }
