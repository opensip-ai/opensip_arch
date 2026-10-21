//! DT-MD1 digest over supplied observations, without source or transport admission.
//! The caller owes the complete admitted sequence and every independent set, Plan,
//! membership, frame, chunk, seal, immutable VFS and limit check. This helper never
//! sorts, deduplicates, truncates or repairs that sequence.
use opensip_identity::{JsonInteger, JsonValue as V, LogicalPath, digest_hex, raw_sha256};
use std::collections::BTreeMap;

pub(crate) struct Entry<'a> {
    pub(crate) package_key: &'a str,
    pub(crate) path: &'a LogicalPath,
    pub(crate) byte_length: u64,
    pub(crate) content_sha256: [u8; 32],
}

#[derive(Debug)]
pub(crate) struct ManifestDigest {
    pub(crate) canonical_entries: Vec<u8>,
    pub(crate) manifest_sha256: [u8; 32],
}

/// Hash only deterministic-CBOR(entries): no set ID, wrapper or H-domain frame.
/// Typed fields and successful encoding do not attest any entry's membership.
pub(crate) fn compute(
    entries: &[Entry<'_>],
) -> Result<ManifestDigest, super::rust_scope_data::ScopeError> {
    let mut rows = Vec::with_capacity(entries.len());
    for entry in entries {
        let length = JsonInteger::new(i128::from(entry.byte_length))
            .map_err(|_| super::rust_scope_data::ScopeError::Integer)?;
        let row = [
            ("packageKey", V::String(entry.package_key.to_owned())),
            ("path", V::String(entry.path.as_str().to_owned())),
            ("byteLength", V::Integer(length)),
            (
                "contentSha256",
                V::String(digest_hex(&entry.content_sha256)),
            ),
        ];
        rows.push(V::Object(
            row.into_iter()
                .map(|(key, value)| (key.to_owned(), value))
                .collect::<BTreeMap<_, _>>(),
        ));
    }
    let canonical_entries = super::rust_scope_data::cbor(&V::Array(rows))?;
    let manifest_sha256 = raw_sha256(&canonical_entries);
    Ok(ManifestDigest {
        canonical_entries,
        manifest_sha256,
    })
}

#[cfg(test)]
#[path = "dependency_transport_digest_tests.rs"]
mod tests;
