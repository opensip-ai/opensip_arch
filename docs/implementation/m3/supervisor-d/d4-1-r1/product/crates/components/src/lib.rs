//! Common component negotiation and supervision.
//!
//! Law M3-D assigns the modules: `control_protocol.rs` to D2a and
//! `provider_protocol.rs` to D2b (both here), `supervisor.rs` to D3a and D3b, and
//! `manifest.rs` with `session_factory.rs` to D4. Only the supervisor spawns,
//! and only a `VerifiedLaunch` through the platform's spawner. `manifest.rs`
//! judges the manifest-class excluded forms over a host-built projection; its
//! `Cleared` authorizes nothing, so nothing here admits a manifest on its own.

// M3-D r5 item 9 (unit D2a): the common control codec, CC v5 exactly.
pub mod control_protocol;

// M3-D r5 items 10 and 11 (unit D2b): the provider codecs. D2b-1 lands the
// strict CBOR profiles, the framing, the sequences and the commitments.
pub mod provider_protocol;

// M3-D r5 items 12 to 15, 17 and 19's normal end (unit D3a-1): one supervised
// provider child, to exactly one settlement.
pub mod supervisor;

// Unit D2b-3a: the embedded schema sources the provider codecs admit by.
mod schema_sources;

// M3-D r5 item 24 (unit D4-1): the manifest-class excluded forms at R10a.
pub mod manifest;
