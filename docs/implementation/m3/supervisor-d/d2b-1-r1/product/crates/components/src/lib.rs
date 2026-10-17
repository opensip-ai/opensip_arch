//! Common component negotiation and supervision.
//!
//! Law M3-D assigns the modules: `control_protocol.rs` to D2a and
//! `provider_protocol.rs` to D2b (both here), `supervisor.rs` to D3a and D3b, and
//! `manifest.rs` with `session_factory.rs` to D4. Nothing here spawns a
//! process, launches a component or admits a manifest.

// M3-D r5 item 9 (unit D2a): the common control codec, CC v5 exactly.
pub mod control_protocol;

// M3-D r5 items 10 and 11 (unit D2b): the provider codecs. D2b-1 lands the
// strict CBOR profiles, the framing, the sequences and the commitments.
pub mod provider_protocol;
