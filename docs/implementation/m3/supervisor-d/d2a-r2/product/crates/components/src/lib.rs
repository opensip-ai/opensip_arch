//! Common component negotiation and supervision.
//!
//! Law M3-D assigns the modules: `control_protocol.rs` to D2a (here),
//! `provider_protocol.rs` to D2b, `supervisor.rs` to D3a and D3b, and
//! `manifest.rs` with `session_factory.rs` to D4. Nothing here spawns a
//! process, launches a component or admits a manifest.

// M3-D r5 item 9 (unit D2a): the common control codec, CC v5 exactly.
pub mod control_protocol;
