//! Complete sorted native file-manifest recipes over supplied file observations.
//! Plain array/frame bytes and digests never establish retained source custody.
use crate::archive_decoder::FileRecord;
use opensip_identity::{
    JsonInteger, JsonValue, canonical_bytes, digest_hex, hash_preimage, raw_sha256,
};
use std::collections::BTreeMap;

#[derive(Debug)]
pub(crate) enum ManifestError {
    DuplicatePath,
    CountOverflow,
    TotalOverflow,
    Canonical(opensip_identity::CanonicalError),
    Frame(opensip_identity::DigestError),
}

#[derive(Debug)]
pub(crate) struct ManifestData {
    pub(crate) canonical_array: Vec<u8>,
    pub(crate) raw_array_sha256: [u8; 32],
    pub(crate) native_frame: Vec<u8>,
    pub(crate) native_manifest_sha256: [u8; 32],
    pub(crate) file_count: u64,
    pub(crate) total_bytes: u128,
}

/// Every supplied record is included; no partitioning, truncation or salvage.
/// Caller owns actual full tree membership, byte/descriptor retention and joins.
/// Schema, source admission, activation, final counters and public error mapping
/// follow separately. Array bytes keep the existing complete CAN 4MiB limit.
pub(crate) fn build(files: &[FileRecord]) -> Result<ManifestData, ManifestError> {
    let file_count = u64::try_from(files.len()).map_err(|_| ManifestError::CountOverflow)?;
    let mut ordered: Vec<&FileRecord> = files.iter().collect();
    ordered.sort_by(|left, right| {
        left.path
            .as_str()
            .as_bytes()
            .cmp(right.path.as_str().as_bytes())
    });
    if ordered.windows(2).any(|pair| pair[0].path == pair[1].path) {
        return Err(ManifestError::DuplicatePath);
    }
    let mut total_bytes = 0_u128;
    let mut rows = Vec::with_capacity(ordered.len());
    for file in ordered {
        total_bytes = total_bytes
            .checked_add(u128::from(file.byte_length))
            .ok_or(ManifestError::TotalOverflow)?;
        let integer =
            JsonInteger::new(i128::from(file.byte_length)).map_err(ManifestError::Canonical)?;
        rows.push(JsonValue::Object(BTreeMap::from([
            ("byteLength".to_owned(), JsonValue::Integer(integer)),
            (
                "contentSha256".to_owned(),
                JsonValue::String(digest_hex(&file.content_sha256)),
            ),
            (
                "path".to_owned(),
                JsonValue::String(file.path.as_str().to_owned()),
            ),
        ])));
    }
    let value = JsonValue::Array(rows);
    let canonical_array = canonical_bytes(&value).map_err(ManifestError::Canonical)?;
    let raw_array_sha256 = raw_sha256(&canonical_array);
    let native_frame = hash_preimage("native.dependency-file-manifest.v1", &value)
        .map_err(ManifestError::Frame)?;
    let native_manifest_sha256 = raw_sha256(&native_frame);
    Ok(ManifestData {
        canonical_array,
        raw_array_sha256,
        native_frame,
        native_manifest_sha256,
        file_count,
        total_bytes,
    })
}

#[cfg(test)]
#[path = "native_file_manifest_tests.rs"]
mod tests;
