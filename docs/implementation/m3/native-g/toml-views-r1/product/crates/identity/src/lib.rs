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
pub use toml::{
    TomlArrayView, TomlDocument, TomlError, TomlIntegerView, TomlTableView, TomlValueView,
    parse_toml,
};

pub use closure::{CaptureError, CapturedEvidence};

// Pure private-registry values. These decoders never establish native custody,
// registration, a held lease, or store/operation authority.
mod project_registry;
pub use project_registry::{
    AllocationKind as ProjectAllocationKind, Entry as ProjectRegistryEntry,
    Error as ProjectRegistryError, PROJECT_MARKER_SIZE, Platform as ProjectRootPlatform,
    ProjectMarker as ProjectIdMarker, REGISTRY_CAP as PROJECT_REGISTRY_CAP,
    REGISTRY_ROW_CAP as PROJECT_REGISTRY_ROW_CAP, Registry as ProjectRegistryDocument,
    Root as ProjectRegistryRoot, Status as ProjectRegistryStatus,
    VolumeIdentityKind as ProjectVolumeIdentityKind,
};
#[cfg(test)]
mod project_registry_tests;

// Shared syntactic store values only. No filesystem, lifecycle or storage edges.
mod store_identity;
mod store_lineage;
mod store_marker;
mod store_selection;
pub use store_identity::{Error as StoreInstanceIdError, StoreInstance as StoreInstanceId};
pub use store_lineage::{
    CAP as LINEAGE_NODE_CAP, DecodeError as LineageDecodeError, Key as LineageKey,
    Node as DecodedLineageNodeV1, SuppliedChain as SuppliedLineageChain,
    WalkError as LineageWalkError, inspect_supplied as inspect_supplied_lineage,
};
pub use store_marker::{
    Error as StoreMarkerDecodeError, MARKER_LIMIT as STORE_MARKER_CAP,
    Marker as DecodedStoreMarkerV1,
};
pub use store_selection::{
    CAP as SELECTION_PAIR_CAP, Error as SelectionDecodeError, LEAF as SELECTION_PAIR_LEAF,
    Selection as DecodedSelectionV1,
};
