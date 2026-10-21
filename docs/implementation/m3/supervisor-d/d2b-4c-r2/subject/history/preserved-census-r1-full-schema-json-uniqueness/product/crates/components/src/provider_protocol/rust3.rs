//! Rust3 codecs (D2b-4a/4b; selected D2b PLAN-r3/A2).
//!
//! Strict bounded acquisition, envelope and closed payload checks, immutable
//! contextual joins and response safety accounting precede P3T matching and
//! publication of generated payloads. Spool records are separate from the
//! retained received bytes used for commitments. This unit adds no production
//! session factory. Host builders, the exact sender and the D3a participant
//! consume supplied admitted projections; negotiated successor admission
//! follows in4c, and the base participant preserves that explicit gate.
mod accounting;
mod build;
mod census;
mod observations;
mod receive;
mod schema_work;
mod schemas;
mod send;
pub use accounting::ResponseTotals;
pub use send::{
    Rust3Chunk, Rust3OpenPlan, Rust3Participant, Rust3Plan, Rust3PlanRefusal, Rust3Request,
    Rust3RequestTotals, Rust3Schedule, Rust3ScheduleRefusal, Rust3ScopeBinding, Rust3SendRefusal,
    Rust3Sender, Rust3Sent, Rust3Slot, Rust3SlotFrame, Rust3SnapshotEntry, Rust3Source,
    Rust3SourceEntry, Rust3StagePlan, Rust3UniversePlan,
};

// Only the Rust3 carrier profile uses this structured schema path.
pub(super) use schema_work::admit_extern;

pub use receive::{
    RELATION_PAYLOAD_MAX_DEPTH, RUST3_FRAME_MAX_DEPTH, Rust3Admitted, Rust3DispatchContext,
    Rust3HostFrame, Rust3Receiver, Rust3Refusal, Rust3StageBinding,
};
