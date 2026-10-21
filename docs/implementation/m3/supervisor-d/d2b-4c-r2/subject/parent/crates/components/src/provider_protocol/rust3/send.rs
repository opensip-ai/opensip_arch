//! Rust3 host builders, exact send schedule and sender (D2b-4b).
//!
//! The schedule mechanism is private. The Plan constructor will supply its
//! checked host values and selected owner bounds; a schedule is not Plan or
//! source admission and does not authorize disclosure by itself.
mod dependency;
mod domain;
mod participant;
mod policy;
mod prepared;
mod request;
mod schedule;
mod sender;
mod snapshot;

pub use domain::{
    Scope as Rust3ScopeBinding, Stage as Rust3StagePlan, Universe as Rust3UniversePlan,
};
pub use participant::Rust3Participant;
pub use policy::Open as Rust3OpenPlan;
pub use request::{Plan as Rust3Plan, Refusal as Rust3PlanRefusal, Request as Rust3Request};
pub use schedule::{
    Chunk as Rust3Chunk, Entry as Rust3SourceEntry, Frame as Rust3SlotFrame,
    Refusal as Rust3ScheduleRefusal, Schedule as Rust3Schedule, Slot as Rust3Slot,
    Totals as Rust3RequestTotals,
};
pub use sender::{
    Refusal as Rust3SendRefusal, Sender as Rust3Sender, Sent as Rust3Sent, Source as Rust3Source,
};
pub use snapshot::Entry as Rust3SnapshotEntry;
