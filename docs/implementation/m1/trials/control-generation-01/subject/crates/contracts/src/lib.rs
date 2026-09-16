#![forbid(unsafe_code)]
// Typify emits sequential bounds checks on one line and intentionally large
// inert wire unions. Their layout is measured separately from correctness.
// FieldPresence keeps a bound-free manual Default implementation.
#[allow(clippy::possible_missing_else, clippy::derivable_impls, clippy::large_enum_variant)]
#[rustfmt::skip]
pub mod generated;
