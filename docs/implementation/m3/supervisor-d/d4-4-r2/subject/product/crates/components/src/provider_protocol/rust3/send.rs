//! Rust3 host builders, exact send schedule and sender (D2b-4b/4c).
//!
//! The schedule mechanism is private. The Plan constructor will supply its
//! checked host values and selected owner bounds; a schedule is not Plan or
//! source admission and does not authorize disclosure by itself.
mod dependency;
pub(super) mod domain;
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

#[cfg(test)]
pub(super) fn census_context_for_test(mask: u8) -> super::Rust3DispatchContext {
    request::Request::build(request::tests::census_plan(mask))
        .unwrap()
        .context
}

#[cfg(test)]
pub(super) fn factory_fixture_for_test(
    mask: u8,
) -> (Rust3Sender, super::super::cbor::Value, Vec<String>) {
    // Distinct synthetic authority and codec input instances: controls can
    // change one while retaining the other, without copying sender output.
    let authority = request::tests::census_plan(mask);
    let request = request::Request::build(request::tests::census_plan(mask)).unwrap();
    (
        sender::Sender::new(request).unwrap(),
        authority.expected_identity,
        authority.capabilities,
    )
}
