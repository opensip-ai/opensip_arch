use contracts::{ExecutionId, NamespaceId, RunCandidate, Refusal};

fn attempt(bytes: Vec<u8>, claimed: &str, prelatch: bool) -> Result<storage::PublishedCommit, Refusal> {
    let candidate = RunCandidate { closure_bytes: bytes, claimed_run_id: String::from(claimed) };
    let run = evaluator::replay(&candidate)?;
    let guard = platform::WriterGuard::acquire().ok_or(Refusal::Admission)?;
    let session = security::admit_commit_session(NamespaceId(1), 5, ExecutionId(9), guard)?;
    let prepared = storage::prepare_commit(run, session)?;
    let attempt = security::AttemptState::new();
    if prelatch { let _ = attempt.latch(); }
    let out = prepared.publish(&attempt);
    println!("   attempt_state_after={}", attempt.state());
    out
}

fn main() {
    let bytes = vec![1u8, 2, 3];
    let sum: u32 = bytes.iter().map(|b| *b as u32).sum();
    let claimed = format!("run3:{:08x}", sum);
    println!("S1 clean publish:");
    match attempt(bytes.clone(), &claimed, false) {
        Ok(pc) => println!("   PUBLISHED run={} seq={} seal={}", pc.receipt_run_id(), pc.commit_sequence(), pc.seal_seq()),
        Err(e) => println!("   REFUSED {:?}", e),
    }
    println!("S2 observer latched before the gate:");
    match attempt(bytes.clone(), &claimed, true) {
        Ok(_) => println!("   UNEXPECTED publish after latch"),
        Err(e) => println!("   REFUSED {:?}", e),
    }
    println!("S3 replay refuses a substituted claim:");
    match attempt(vec![9u8], "run3:00000000", false) {
        Ok(_) => println!("   UNEXPECTED publish on bad claim"),
        Err(e) => println!("   REFUSED {:?}", e),
    }
}
