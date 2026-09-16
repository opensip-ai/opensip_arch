//! Host coordinator: cannot manufacture either prerequisite from booleans or DTOs.
use contracts::{ExecutionId, NamespaceId, RunCandidate, Refusal};

pub fn finalize(bytes: Vec<u8>, claimed: &str) -> Result<storage::PublishedCommit, Refusal> {
    let candidate = RunCandidate { closure_bytes: bytes, claimed_run_id: String::from(claimed) };
    let run = evaluator::replay(&candidate)?;
    let guard = platform::WriterGuard::acquire().ok_or(Refusal::Admission)?;
    let session = security::admit_commit_session(NamespaceId(1), 5, ExecutionId(9), guard)?;
    let prepared = storage::prepare_commit(run, session)?;
    let attempt = security::AttemptState::new();
    prepared.publish(&attempt)
}

pub fn main_probe() {
    let bytes = vec![1u8, 2, 3];
    let sum: u32 = bytes.iter().map(|b| *b as u32).sum();
    let claimed = format!("run3:{:08x}", sum);
    match finalize(bytes.clone(), &claimed) {
        Ok(pc) => println!("PUBLISHED run={} seq={} seal={}", pc.receipt_run_id(), pc.commit_sequence(), pc.seal_seq()),
        Err(e) => println!("REFUSED {:?}", e),
    }
    match finalize(vec![9u8], "run3:00000000") {
        Ok(_) => println!("UNEXPECTED publish on bad claim"),
        Err(e) => println!("REFUSED-bad-claim {:?}", e),
    }
}

fn main() { main_probe(); }
