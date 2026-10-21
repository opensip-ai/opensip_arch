//! D2b-4a Rust3 receive mechanisms (accepted D2b PLAN-r3/A2).
//!
//! The response safety accounting below is one part of admission. It does
//! not validate a frame's schema/context, match P3T or admit facts. The full
//! receive side is still being implemented in this unaccepted worktree.
mod accounting;
mod observations;
mod schema_work;
mod schemas;
pub use accounting::{CandidateBatch, ResponseAccounting, ResponseBoundsRefusal, ResponseTotals};
pub use observations::ProviderFaultWindow;
pub use schemas::Rust3PayloadSchemas;

// Only the Rust3 carrier profile uses this structured schema path.
pub(super) use schema_work::admit_extern;
