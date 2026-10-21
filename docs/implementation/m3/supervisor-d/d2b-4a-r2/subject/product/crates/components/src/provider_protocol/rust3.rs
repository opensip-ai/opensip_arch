//! Rust3 receive codec (D2b-4a; selected D2b PLAN-r3/A2).
//!
//! Strict bounded acquisition, envelope and closed payload checks, immutable
//! contextual joins and response safety accounting precede P3T matching and
//! publication of generated payloads. Spool records are separate from the
//! retained received bytes used for commitments. This unit adds no production
//! session factory; send/participant and negotiated successors follow in4b/4c.
mod accounting;
mod build;
mod observations;
mod receive;
mod schema_work;
mod schemas;
pub use accounting::ResponseTotals;

// Only the Rust3 carrier profile uses this structured schema path.
pub(super) use schema_work::admit_extern;

pub use receive::{
    RELATION_PAYLOAD_MAX_DEPTH, RUST3_FRAME_MAX_DEPTH, Rust3Admitted, Rust3DispatchContext,
    Rust3HostFrame, Rust3Receiver, Rust3Refusal, Rust3StageBinding,
};
