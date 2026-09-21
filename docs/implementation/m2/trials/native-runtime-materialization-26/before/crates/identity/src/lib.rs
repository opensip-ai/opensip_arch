//! Pure, bounded identity primitives over explicitly supplied bytes and values.
//!
//! Lexical admission and canonical encoding are distinct from schema validation,
//! descriptor admission and complete semantic replay. A digest proves none of
//! those later obligations by itself.
#![no_std]
#![forbid(unsafe_code)]

extern crate alloc;

mod canonical;
mod capability_codec;
mod closure;
mod descriptors;
mod digests;
mod relations;
mod schema;
mod schema_patterns;
mod schema_registry;
#[cfg(test)]
mod schema_tests;

pub use canonical::{
    Error as CanonicalError, Integer as JsonInteger, MAX_BYTES, MAX_DEPTH, MAX_INTEGER,
    MIN_INTEGER, Value as JsonValue, encode as canonical_bytes, parse as parse_json,
};
pub use descriptors::{
    ArrayOrder, ArrayOrderError, CandidateError, IdentityCandidate, IdentityDomain, LogicalPath,
    LogicalPathError,
};
pub use digests::{
    Error as DigestError, frame as hash_preimage, hex as digest_hex,
    identity as hash_canonical_value, raw_sha256, unframe as parse_hash_preimage,
};
pub use schema::Error as SchemaError;
pub use schema_registry::{
    AdmissionError as SchemaAdmissionError, RegisteredSchemas, SchemaHandle, ShapeValue, SourcePin,
};

#[cfg(test)]
mod canonical_tests;

pub use closure::{Error as RetainedInputError, ObjectInput, RetainedBlob, RetainedInputs};

pub use closure::{FramedCandidate, NativeFrameSet};
pub use closure::{
    GraphError, StructuralChecks, StructuralObligation, StructuralOwner, TraversalBudget,
};

pub use capability_codec::{Error as Cve1Error, decode as decode_cve1, encode as encode_cve1};

mod toml;
pub use toml::{TomlDocument, TomlError, TomlTableView, TomlValueView, parse_toml};

pub use closure::{CaptureError, CapturedEvidence};
