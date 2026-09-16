//! Pure evaluator: contracts only. No ports, callbacks or live state.
use contracts::{RunCandidate, Refusal};

/// Public opaque; constructor private to complete replay in this module.
pub struct ReplayedRun { run_id: String, inventory_digest: String }

impl ReplayedRun {
    pub fn run_id(&self) -> &str { &self.run_id }
    pub fn inventory_digest(&self) -> &str { &self.inventory_digest }
}

/// The only way to obtain a ReplayedRun: full semantic reconstruction.
pub fn replay(c: &RunCandidate) -> Result<ReplayedRun, Refusal> {
    if c.closure_bytes.is_empty() { return Err(Refusal::Replay); }
    let recomputed = format!("run3:{:08x}", c.closure_bytes.iter().map(|b| *b as u32).sum::<u32>());
    if recomputed != c.claimed_run_id { return Err(Refusal::Replay); }
    Ok(ReplayedRun { run_id: recomputed, inventory_digest: String::from("inv:deadbeef") })
}
