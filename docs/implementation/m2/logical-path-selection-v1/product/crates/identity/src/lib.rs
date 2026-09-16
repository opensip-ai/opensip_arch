//! Pure, bounded identity primitives over explicitly supplied bytes and values.
//!
//! Lexical admission and canonical encoding are distinct from schema validation,
//! descriptor admission and complete semantic replay. A digest proves none of
//! those later obligations by itself.
#![no_std]
#![forbid(unsafe_code)]

extern crate alloc;

mod canonical;
mod descriptors;
mod digests;

pub use canonical::{
    Error as CanonicalError, Integer as JsonInteger, MAX_BYTES, MAX_DEPTH, MAX_INTEGER,
    MIN_INTEGER, Value as JsonValue, encode as canonical_bytes, parse as parse_json,
};
pub use descriptors::{LogicalPath, LogicalPathError};
pub use digests::{
    Error as DigestError, frame as hash_preimage, hex as digest_hex,
    identity as hash_canonical_value, raw_sha256, unframe as parse_hash_preimage,
};

#[cfg(test)]
mod canonical_tests;
