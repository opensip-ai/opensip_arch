//! Exact NKC-1 key data recipes; supplied tuples and paths confer no admission.
use opensip_identity::{JsonValue, LogicalPath, canonical_bytes, digest_hex, raw_sha256};

#[derive(Debug)]
pub(crate) enum KeyError {
    NameLength,
    VersionLength,
    SourceIdLength,
    OwnerShape,
    Canonical(opensip_identity::CanonicalError),
}

#[derive(Debug)]
pub(crate) struct KeyData {
    pub(crate) canonical_preimage: Vec<u8>,
    pub(crate) key: String,
}

#[derive(Clone, Copy, Debug)]
pub(crate) enum SourceClass {
    SnapshotMember,
    DependencyClosureMember,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub(crate) enum SourceKind {
    Registry,
    Git,
    Path,
    Vendored,
}

/// Supplied original-family data only, not parsed or admitted source evidence.
#[derive(Clone, Copy, Debug)]
pub(crate) enum OriginalSourceFamily {
    Registry,
    SparseRegistry,
    Git,
    Path,
}

/// Supplied acquisition data only, not a verified owned acquisition witness.
#[derive(Clone, Copy, Debug)]
pub(crate) enum AcquisitionMode {
    ImportedDescriptor,
    InSnapshotVendored,
    InSnapshotPath,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub(crate) enum SourceKindDataError {
    MissingFamily,
    MissingAcquisition,
    MissingAdvertisedKind,
    InvalidCombination,
    ConflictingAdvertisedKind,
}

/// Apply the selected NSK-1 table to supplied data; no source-string parser,
/// prefix fallback, sourceId substitution or acquisition authorization occurs.
/// The caller owes exact pinned Cargo parsing and actual same owned source,
/// acquisition, manifest, carrier, activation, custody and profile admission.
/// Registry and sparse share the existing native registry family. Vendoring
/// does not change the original family, raw tuple, checksum or provenance.
pub(crate) fn classify_source_kind_data(
    family: Option<OriginalSourceFamily>,
    acquisition: Option<AcquisitionMode>,
    advertised: Option<SourceKind>,
) -> Result<SourceKind, SourceKindDataError> {
    use AcquisitionMode as A;
    use OriginalSourceFamily as F;
    let family = family.ok_or(SourceKindDataError::MissingFamily)?;
    let acquisition = acquisition.ok_or(SourceKindDataError::MissingAcquisition)?;
    let advertised = advertised.ok_or(SourceKindDataError::MissingAdvertisedKind)?;
    let selected = match (family, acquisition) {
        (F::Registry | F::SparseRegistry, A::ImportedDescriptor) => SourceKind::Registry,
        (F::Registry | F::SparseRegistry | F::Git, A::InSnapshotVendored) => SourceKind::Vendored,
        (F::Git, A::ImportedDescriptor) => SourceKind::Git,
        (F::Path, A::InSnapshotPath) => SourceKind::Path,
        _ => return Err(SourceKindDataError::InvalidCombination),
    };
    if advertised != selected {
        return Err(SourceKindDataError::ConflictingAdvertisedKind);
    }
    Ok(selected)
}

/// Raw Cargo.lock tuple values, with the selected Unicode scalar bounds only.
/// No normalization, source parsing, semantic version or context identity enters.
pub(crate) fn package(name: &str, version: &str, source_id: &str) -> Result<KeyData, KeyError> {
    if !(1..=256).contains(&name.chars().take(257).count()) {
        return Err(KeyError::NameLength);
    }
    if !(1..=256).contains(&version.chars().take(257).count()) {
        return Err(KeyError::VersionLength);
    }
    if source_id.chars().take(4097).count() > 4096 {
        return Err(KeyError::SourceIdLength);
    }
    key_data(
        "pkg1-",
        JsonValue::Array(vec![
            JsonValue::String(name.to_owned()),
            JsonValue::String(version.to_owned()),
            JsonValue::String(source_id.to_owned()),
        ]),
    )
}

/// Recompute package data first; never accept a caller's alleged package key.
/// Shape checks do not prove snapshot membership, actual package mapping, source
/// class, producer observation, activation, custody or prepared-owner admission.
pub(crate) fn owner(
    name: &str,
    version: &str,
    source_id: &str,
    source: SourceClass,
    source_kind: SourceKind,
    snapshot_manifest_path: Option<&LogicalPath>,
) -> Result<(KeyData, KeyData), KeyError> {
    let package_data = package(name, version, source_id)?;
    if matches!(source, SourceClass::SnapshotMember) && !matches!(source_kind, SourceKind::Path) {
        return Err(KeyError::OwnerShape);
    }
    let locator = match (source_kind, snapshot_manifest_path) {
        (SourceKind::Path, Some(path))
            if source_id.is_empty() && path.as_str().rsplit('/').next() == Some("Cargo.toml") =>
        {
            JsonValue::String(path.as_str().to_owned())
        }
        (SourceKind::Registry | SourceKind::Git | SourceKind::Vendored, None) => JsonValue::Null,
        _ => return Err(KeyError::OwnerShape),
    };
    let class = match source {
        SourceClass::SnapshotMember => "snapshot-member",
        SourceClass::DependencyClosureMember => "dependency-closure-member",
    };
    let owner_data = key_data(
        "own2-",
        JsonValue::Array(vec![
            JsonValue::String(class.to_owned()),
            JsonValue::String(package_data.key.clone()),
            locator,
        ]),
    )?;
    Ok((package_data, owner_data))
}

fn key_data(prefix: &str, value: JsonValue) -> Result<KeyData, KeyError> {
    let canonical_preimage = canonical_bytes(&value).map_err(KeyError::Canonical)?;
    let key = format!("{prefix}{}", digest_hex(&raw_sha256(&canonical_preimage)));
    Ok(KeyData {
        canonical_preimage,
        key,
    })
}

#[cfg(test)]
#[path = "native_key_data_tests.rs"]
mod tests;
