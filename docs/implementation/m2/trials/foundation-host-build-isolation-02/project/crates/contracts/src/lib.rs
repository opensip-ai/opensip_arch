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
