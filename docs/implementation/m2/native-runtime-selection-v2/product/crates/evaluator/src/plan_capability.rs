//! Join one admitted Plan descriptor to its retained capability bytes.
use crate::{CapabilityManifest, CapabilityRefusal, admit_capability_manifest};
use alloc::vec::Vec;
use opensip_identity::{
    IdentityDomain, JsonValue, RetainedInputError, RetainedInputs, digest_hex, raw_sha256,
};

#[derive(Debug, PartialEq, Eq)]
pub enum PlanCapabilityError {
    Input(RetainedInputError),
    Descriptor,
    BytesJoin,
    Manifest(CapabilityRefusal),
    ManifestIdentity,
}

fn text<'a>(value: &'a JsonValue, field: &str) -> Result<&'a str, PlanCapabilityError> {
    match value {
        JsonValue::Object(o) => match o.get(field) {
            Some(JsonValue::String(s)) => Ok(s),
            _ => Err(PlanCapabilityError::Descriptor),
        },
        _ => Err(PlanCapabilityError::Descriptor),
    }
}
fn digest(s: &str) -> Result<[u8; 32], PlanCapabilityError> {
    if s.len() != 64
        || !s
            .bytes()
            .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
    {
        return Err(PlanCapabilityError::Descriptor);
    }
    let mut out = [0; 32];
    for (i, byte) in out.iter_mut().enumerate() {
        *byte = u8::from_str_radix(&s[i * 2..i * 2 + 2], 16)
            .map_err(|_| PlanCapabilityError::Descriptor)?;
    }
    Ok(out)
}

/// Recompute the Plan identity, rehash retained bytes, check the committed
/// capability identity, and rerun the encoding owner's gates for this Plan.
/// This does not admit the Plan's other references, a Run, or release custody.
pub fn admit_plan_capability(
    inputs: &RetainedInputs<'_>,
    plan_id: &str,
    descriptor_work: usize,
) -> Result<CapabilityManifest, PlanCapabilityError> {
    let plan = inputs
        .object(plan_id, IdentityDomain::Plan, descriptor_work)
        .map_err(PlanCapabilityError::Input)?;
    let expected = text(plan.descriptor(), "capabilityManifestId")?;
    let blob = inputs
        .blob(digest(text(
            plan.descriptor(),
            "capabilityManifestBytesDigest",
        )?)?)
        .map_err(PlanCapabilityError::Input)?;
    // Match open_run_closure: bytes identity is checked BEFORE manifest gates,
    // so malformed bytes plus a mismatched ID cannot hide the failed join.
    let mut preimage = Vec::from(&b"opensip.capability-manifest.v1\0"[..]);
    preimage.extend_from_slice(blob.bytes());
    if digest_hex(&raw_sha256(&preimage)) != expected {
        return Err(PlanCapabilityError::BytesJoin);
    }
    let capability =
        admit_capability_manifest(blob.bytes()).map_err(PlanCapabilityError::Manifest)?;
    if digest_hex(&capability.identity()) != expected {
        return Err(PlanCapabilityError::ManifestIdentity);
    }
    Ok(capability)
}
