//! Private signed-metadata encoding primitives. Shape, signatures, signer
//! thresholds, custody, freshness and operational authority are separate owners.
#[cfg(target_os = "macos")]
pub(crate) use root_payload::AclOmissionPremise;
#[cfg(target_os = "macos")]
pub(crate) use root_payload::{
    InitialCore, InitialCoreRefusal, InitialPlatform, InitialPlatformRefusal, PrimitivePolicy,
    StateWriter, produce_initial_core, produce_initial_platform,
};
#[cfg(all(
    any(test, feature = "crash-matrix", feature = "scenario-fixtures"),
    target_os = "macos"
))]
#[cfg_attr(not(test), allow(unused_imports))]
pub(crate) use root_payload::{InitialReceipts, ReadProducers, read_producers, receipts_at};
#[cfg(target_os = "macos")]
pub use root_payload::{NativeTrustReadError, NativeTrustReadSession, ProvisionalSuccessorCounts};
#[path = "component_manifest.rs"]
mod component_manifest;
#[path = "trust_outcomes.rs"]
mod trust_outcomes;
#[path = "trust_record_reader.rs"]
mod trust_record_reader;
#[path = "trust_record_shapes.rs"]
mod trust_record_shapes;
// M3-C r8 item 7 (unit C2a-1): the read-only bridge to verified components.
#[path = "trust_admitted_components.rs"]
mod admitted_components;
pub(crate) use admitted_components::AuthenticatedComponent;
#[cfg(test)]
pub(crate) use admitted_components::TestComponent;
use metadata::MAX_DEPTH;
use opensip_identity::JsonValue;
#[cfg(target_os = "macos")]
pub(crate) use root_payload::ConfirmedCurrent;
#[cfg(all(test, target_os = "macos"))]
pub(crate) use root_payload::ObservationPoint;
#[cfg(test)]
pub(crate) use root_payload::write_accepted_trust;
#[cfg(test)]
pub(crate) use root_payload::write_accepted_trust_issued;
#[cfg(target_os = "macos")]
pub(crate) use root_payload::{
    AdmittedCurrentTrust, BootstrapSource, LiveObservation, ObservationHook, Observed,
    RetainedTrustHandles, TrustInvocation, TrustRefusal, TrustRow, fenced_operation_read,
};
pub(crate) use root_payload::{CURRENT_STATE_CAP, decode_current_store};
pub(crate) use root_payload::{
    CapturedImage, CapturedOrdinaryInput, ClockProjection, OrdinaryClockInput,
};
pub(crate) use root_payload::{
    InitialPublicationError, InitialPublicationInputs, TrustFile, build_initial_publication,
    verify_initial_publication_files,
};
#[cfg(all(test, target_os = "macos"))]
pub(crate) use root_payload::{RetainedCurrentTrust, publish_trust};
// Law X9 r1 item 6 / X8 r3 item 4b: the shared fenced publisher and X4T-0's
// store, on the shared fixture-gate site list.
#[cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))]
pub(crate) use root_payload::accepted_store_files;
#[cfg(all(
    any(test, feature = "crash-matrix", feature = "scenario-fixtures"),
    target_os = "macos"
))]
pub(crate) use root_payload::publish_store_fenced;

#[cfg(test)]
pub(crate) fn clock_fixture_projection(value: &JsonValue) -> Result<ClockProjection, String> {
    root_payload::clock_fixture_projection(value)
}

#[derive(Debug, PartialEq, Eq)]
enum MetadataError {
    NonNfc,
    IntegerRange,
    Limit,
    NfcKeyCollision,
    Canonical(metadata::Error),
}

/// Encode opensip-metadata-canonical.1 values: reject non-NFC strings without
/// normalizing, require signed i64 integers, then use metadata-specific JSON encoding with64-container nesting. This does not admit a signed document, and is
/// never used to interpret product evidence. Work is a local input-byte/node
/// bound, not a signature-verification or aggregate resource qualification.
fn metadata_bytes(value: &JsonValue, mut work: usize) -> Result<Vec<u8>, MetadataError> {
    check_value(value, 0, &mut work)?;
    metadata::encode(value).map_err(|error| match error {
        metadata::Error::NonNfc => MetadataError::NonNfc,
        metadata::Error::NfcKeyCollision => MetadataError::NfcKeyCollision,
        metadata::Error::IntegerRange => MetadataError::IntegerRange,
        _ => MetadataError::Canonical(error),
    })
}
// Count local traversal work before profile encoding. The input is
// already owned; this pass allocates no tree or pending-node queue. Recursion
// is bounded by the metadata profile's64-container limit.
fn check_value(value: &JsonValue, depth: usize, work: &mut usize) -> Result<(), MetadataError> {
    if depth > MAX_DEPTH {
        return Err(MetadataError::Limit);
    }
    *work = work.checked_sub(1).ok_or(MetadataError::Limit)?;
    match value {
        JsonValue::Integer(_) => {}
        JsonValue::String(s) => check_string(s, work)?,
        JsonValue::Array(a) => {
            for v in a {
                check_value(v, depth + 1, work)?;
            }
        }
        JsonValue::Object(o) => {
            for (k, v) in o {
                check_string(k, work)?;
                check_value(v, depth + 1, work)?;
            }
        }
        JsonValue::Null | JsonValue::Bool(_) => {}
    }
    Ok(())
}
fn check_string(s: &str, work: &mut usize) -> Result<(), MetadataError> {
    *work = work.checked_sub(s.len()).ok_or(MetadataError::Limit)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    include!("trust/metadata_tests.rs");
}

// Lexical mechanism adapted from the pinned product codec, with a separate
// metadata profile: i64,64 containers, -0 canonicalizes to0, NFC strings and
// NFC key-collision rejection. It never changes product JSON rules.
pub(super) mod metadata {
    include!("trust/metadata.rs");
}

#[cfg(test)]
mod codec_tests {
    include!("trust/codec_tests.rs");
}

// Retained v8 semantic rule kernel over bounded, structurally projected input.
// This is not the product RootV1/RootV2 schema gate, trust-chain admission,
// signature verification, or a trusted-root constructor.
mod retained_root_semantics {
    include!("trust/retained_root_semantics.rs");
}

// Metadata domains use SHA256(UTF8(domain) || 0 || canonical metadata),
// distinct from product identity frames. These helpers produce inert digests;
// they perform no envelope shape/routing/threshold/signature admission.
fn metadata_domain_digest(kind: &str, value: &JsonValue) -> Result<[u8; 32], &'static str> {
    let domain = match kind {
        "manifest" => "opensip.metadata.manifest.1",
        "catalog" => "opensip.metadata.catalog.1",
        "registry" => "opensip.metadata.registry.1",
        "lock" => "opensip.metadata.lock.1",
        "root" => "opensip.metadata.root.1",
        "revocation" => "opensip.metadata.revocation.1",
        "inventory" => "opensip.metadata.inventory.1",
        "payload" => "opensip.metadata.payload.1",
        "registry-view" => "opensip.metadata.registry-view.1",
        "envelope" => "opensip.metadata.envelope.2",
        "journal" => "opensip.metadata.journal.1",
        "policy" => "opensip.metadata.policy.1",
        "policy-effective" => "opensip.metadata.policy-effective.1",
        "test" => "opensip.metadata.test.1",
        _ => return Err("UNKNOWN_METADATA_DOMAIN"),
    };
    metadata_digest_for_domain(domain, value)
}
fn metadata_digest_for_domain(domain: &str, value: &JsonValue) -> Result<[u8; 32], &'static str> {
    let canonical = metadata_bytes(value, 5_000_000).map_err(|_| "METADATA")?;
    let mut bytes = Vec::with_capacity(domain.len() + 1 + canonical.len());
    bytes.extend_from_slice(domain.as_bytes());
    bytes.push(0);
    bytes.extend_from_slice(&canonical);
    Ok(opensip_identity::raw_sha256(&bytes))
}
fn envelope_message(env: &JsonValue) -> Result<[u8; 32], &'static str> {
    // Bound the supplied tree before cloning projected fields. This is a local
    // work bound, not envelope schema or signature admission.
    check_value(env, 0, &mut 5_000_000).map_err(|_| "METADATA")?;
    let JsonValue::Object(env) = env else {
        return Err("SHAPE");
    };
    let Some(JsonValue::Object(s)) = env.get("subject") else {
        return Err("SHAPE");
    };
    let mut out = std::collections::BTreeMap::new();
    for field in ["kind", "domain", "storedSha256", "preimageSha256"] {
        let Some(JsonValue::String(v)) = s.get(field) else {
            return Err("SHAPE");
        };
        out.insert(field.into(), JsonValue::String(v.clone()));
    }
    for field in ["role", "namespace"] {
        let Some(JsonValue::String(v)) = env.get(field) else {
            return Err("SHAPE");
        };
        out.insert(field.into(), JsonValue::String(v.clone()));
    }
    metadata_domain_digest("envelope", &JsonValue::Object(out))
}
#[cfg(test)]
mod digest_tests {
    include!("trust/digest_tests.rs");
}

// A verified signature is a private cryptographic fact over exactly32 metadata
// digest bytes, not a trusted signer/role/quorum/root or operational authority.
#[derive(Debug, PartialEq, Eq)]
struct VerifiedSignature {
    key_id: [u8; 32],
    message: [u8; 32],
}
#[derive(Debug, PartialEq, Eq)]
enum SignatureError {
    PublicKey,
    Invalid,
}
// Canonical compressed point admission shared by root keys and signatures.
// to_bytes() preserves presented bytes; re-encoding the Edwards point is required.
fn admitted_public_key(
    public_key: &[u8; 32],
) -> Result<ed25519_dalek::VerifyingKey, SignatureError> {
    let key = ed25519_dalek::VerifyingKey::from_bytes(public_key)
        .map_err(|_| SignatureError::PublicKey)?;
    if key.is_weak() || key.to_edwards().compress().to_bytes() != *public_key {
        return Err(SignatureError::PublicKey);
    }
    Ok(key)
}
fn verify_metadata_signature(
    public_key: &[u8; 32],
    message: &[u8; 32],
    signature: &[u8; 64],
) -> Result<VerifiedSignature, SignatureError> {
    let key = admitted_public_key(public_key)?;
    key.verify_strict(message, &ed25519_dalek::Signature::from_bytes(signature))
        .map_err(|_| SignatureError::Invalid)?;
    Ok(VerifiedSignature {
        key_id: opensip_identity::raw_sha256(public_key),
        message: *message,
    })
}
#[cfg(test)]
mod signature_tests {
    include!("trust/signature_tests.rs");
}

// Full document rules remain distinct from authenticated root-chain/current
// trust admission. This module is private while reference60 awaits review.
mod root_payload {
    include!("trust/root_payload.rs");
}

// Conditional per-role event kernel; durable admission/evidence remain host work.
mod role_machine;
