//! Rust3 host builders, exact send schedule and sender (D2b-4b).
//!
//! The schedule mechanism is private. The Plan constructor will supply its
//! checked host values and selected owner bounds; a schedule is not Plan or
//! source admission and does not authorize disclosure by itself.
mod dependency;
mod domain;
mod policy;
mod prepared;
mod schedule;
mod snapshot;
