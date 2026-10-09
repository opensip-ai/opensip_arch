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

#[derive(Clone, Copy, Debug)]
pub(crate) enum SourceKind {
    Registry,
    Git,
    Path,
    Vendored,
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
