//! Inert contracts crate: no authority-bearing type, no cross-crate constructor hole.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct RunCandidate { pub closure_bytes: Vec<u8>, pub claimed_run_id: String }
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct NamespaceId(pub u32);
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct ExecutionId(pub u64);
#[derive(Debug)]
pub enum Refusal { Replay, Admission, Latched, Carrier, Ledger }
