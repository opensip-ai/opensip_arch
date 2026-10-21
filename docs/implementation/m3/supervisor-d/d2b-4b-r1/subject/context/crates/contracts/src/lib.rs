//! Inert generated carriers and exact representation helpers.
//! Deserialization validates representation only. Host admission, semantic
//! evidence validation and retained-source custody belong to their owners.
#![forbid(unsafe_code)]
// Generated bounds checks, wire unions and bound-free FieldPresence defaults
// retain the reviewed generator layout, including infallible string TryFrom
// implementations. These allowances apply only to the generated module.
#[allow(clippy::possible_missing_else, clippy::derivable_impls, clippy::large_enum_variant, clippy::infallible_try_from)]
#[rustfmt::skip]
pub mod generated;

/// The JSON value the generated carriers use for open or constant schema
/// members (`serde_json::Value`), named here so that a hand-written
/// conversion can build those members without a serde edge of its own
/// (unit D2b-3a, LD-D2B3-3). It decodes nothing.
pub use serde_json::Value as GeneratedJson;
