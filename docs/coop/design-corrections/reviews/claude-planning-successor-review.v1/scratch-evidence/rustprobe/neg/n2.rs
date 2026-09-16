// N2: forge PublishedCommit in host
pub fn forge() -> storage::PublishedCommit {
    storage::PublishedCommit { receipt_run_id: String::from("r"), commit_sequence: 1, seal_seq: 1 }
}
