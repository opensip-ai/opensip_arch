//! RUST3-LIM subject recipes over supplied observations; plain data, not admission.
//! Complete manifest custody, stage/key selection, independent host/worker
//! reconstruction, negotiated wire checks and public failures remain owners' work.
use opensip_identity::{JsonInteger, JsonValue as V, LogicalPath, digest_hex, raw_sha256};
use std::collections::BTreeMap;

#[derive(Debug)]
pub(crate) enum ScopeError {
    SnapshotShape,
    MissingFileLength,
    MissingFileDigest,
    Empty,
    DuplicatePath,
    Integer,
    Text(opensip_identity::Cve1Error),
}

/// Inert observations. A kind spelling or LogicalPath does not attest membership.
pub(crate) struct Entry<'a> {
    pub(crate) kind: &'a str,
    pub(crate) path: &'a LogicalPath,
    pub(crate) byte_length: Option<u64>,
    pub(crate) content_sha256: Option<[u8; 32]>,
}

#[derive(Debug)]
pub(crate) struct ScopeData {
    pub(crate) subjects: V,
    pub(crate) subject_count: u64,
    pub(crate) canonical_subjects: Vec<u8>,
    pub(crate) subject_scope_commitment: String,
}

/// Rebuild the complete nonempty .rs array. No 256-subject inline cap is applied:
/// this is data for the selected by-reference recipe, never permission to spawn.
/// Upstream owners must supply the fully admitted manifest and selected snapshot.
pub(crate) fn rebuild(snapshot_id: &str, entries: &[Entry<'_>]) -> Result<ScopeData, ScopeError> {
    let Some(digest) = snapshot_id.strip_prefix("snapshot2:") else {
        return Err(ScopeError::SnapshotShape);
    };
    if digest.len() != 64
        || !digest
            .bytes()
            .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
    {
        return Err(ScopeError::SnapshotShape);
    }
    let mut selected = Vec::new();
    for entry in entries {
        if entry.kind != "file" || !entry.path.as_str().ends_with(".rs") {
            continue;
        }
        let length = entry.byte_length.ok_or(ScopeError::MissingFileLength)?;
        if length != 0 {
            selected.push((entry, length));
        }
    }
    selected.sort_by(|(a, _), (b, _)| a.path.as_str().as_bytes().cmp(b.path.as_str().as_bytes()));
    if selected.is_empty() {
        return Err(ScopeError::Empty);
    }
    if selected
        .windows(2)
        .any(|pair| pair[0].0.path == pair[1].0.path)
    {
        return Err(ScopeError::DuplicatePath);
    }
    let subject_count = u64::try_from(selected.len()).map_err(|_| ScopeError::Integer)?;
    let mut subjects = Vec::with_capacity(selected.len());
    for (ordinal, (entry, length)) in selected.into_iter().enumerate() {
        let digest = entry.content_sha256.ok_or(ScopeError::MissingFileDigest)?;
        let preimage = object([
            ("snapshotId", V::String(snapshot_id.to_owned())),
            ("path", V::String(entry.path.as_str().to_owned())),
            ("contentSha256", V::String(digest_hex(&digest))),
            ("byteLength", integer(length)?),
        ]);
        let subject_id = format!(
            "rust-file:{}",
            commitment("opensip.rust-provider.subject.v2", &preimage)?
        );
        subjects.push(object([
            (
                "subjectOrdinal",
                integer(u64::try_from(ordinal).map_err(|_| ScopeError::Integer)?)?,
            ),
            ("subjectId", V::String(subject_id)),
            ("path", V::String(entry.path.as_str().to_owned())),
            ("startByte", integer(0)?),
            ("endByte", integer(length)?),
        ]));
    }
    let subjects = V::Array(subjects);
    let canonical_subjects = cbor(&subjects)?;
    let subject_scope_commitment = hash_bytes(
        "opensip.rust-provider.subject-scope.v2",
        &canonical_subjects,
    );
    Ok(ScopeData {
        subjects,
        subject_count,
        canonical_subjects,
        subject_scope_commitment,
    })
}

/// Hash the exact supplied key array, preserving order and every field. This
/// neither derives nor validates C-2 keys, stage membership or provider identity.
/// Actual constructors owe those checks and independent domain recomputation.
pub(crate) fn domain_commitment(
    subjects: &ScopeData,
    requested_keys: &[V],
) -> Result<String, ScopeError> {
    commitment(
        "opensip.rust-provider.analysis-domain.v2",
        &object([
            ("subjects", subjects.subjects.clone()),
            ("requestedCoverageDomain", V::Array(requested_keys.to_vec())),
        ]),
    )
}

fn integer(n: u64) -> Result<V, ScopeError> {
    Ok(V::Integer(
        JsonInteger::new(i128::from(n)).map_err(|_| ScopeError::Integer)?,
    ))
}
fn object<const N: usize>(rows: [(&str, V); N]) -> V {
    V::Object(
        rows.into_iter()
            .map(|(k, v)| (k.to_owned(), v))
            .collect::<BTreeMap<_, _>>(),
    )
}
fn hash_bytes(domain: &str, bytes: &[u8]) -> String {
    let mut preimage = Vec::new();
    preimage.extend_from_slice(domain.as_bytes());
    preimage.push(0);
    preimage.extend_from_slice(bytes);
    format!("sha256:{}", digest_hex(&raw_sha256(&preimage)))
}
fn commitment(domain: &str, value: &V) -> Result<String, ScopeError> {
    Ok(hash_bytes(domain, &cbor(value)?))
}

// The inherited native uint64/JSON-shaped deterministic-CBOR subset. These
// preimages contain no byte-string member. This is not a wire decoder/schema.
fn head(out: &mut Vec<u8>, major: u8, n: u64) {
    let (additional, width) = match n {
        0..=23 => {
            out.push((major << 5) | n as u8);
            return;
        }
        24..=255 => (24, 1),
        256..=65535 => (25, 2),
        65536..=4294967295 => (26, 4),
        _ => (27, 8),
    };
    out.push((major << 5) | additional);
    out.extend_from_slice(&n.to_be_bytes()[8 - width..]);
}
fn text(out: &mut Vec<u8>, s: &str) -> Result<(), ScopeError> {
    // Reuse only the existing NFC/text-length check on a single inert string.
    // The emitted bytes below are native CBOR, never CVE1 framing.
    opensip_identity::encode_cve1(&V::String(s.to_owned())).map_err(ScopeError::Text)?;
    head(
        out,
        3,
        u64::try_from(s.len()).map_err(|_| ScopeError::Integer)?,
    );
    out.extend_from_slice(s.as_bytes());
    Ok(())
}
fn cbor(value: &V) -> Result<Vec<u8>, ScopeError> {
    let mut bytes = Vec::new();
    write(value, &mut bytes)?;
    Ok(bytes)
}
fn write(value: &V, out: &mut Vec<u8>) -> Result<(), ScopeError> {
    enum Task<'a> {
        Value(&'a V),
        Key(Vec<u8>),
    }
    let mut tasks = vec![Task::Value(value)];
    while let Some(task) = tasks.pop() {
        let value = match task {
            Task::Key(key) => {
                out.extend_from_slice(&key);
                continue;
            }
            Task::Value(value) => value,
        };
        match value {
            V::Null => out.push(0xf6),
            V::Bool(false) => out.push(0xf4),
            V::Bool(true) => out.push(0xf5),
            V::Integer(n) => head(
                out,
                0,
                u64::try_from(n.get()).map_err(|_| ScopeError::Integer)?,
            ),
            V::String(s) => text(out, s)?,
            V::Array(values) => {
                head(
                    out,
                    4,
                    u64::try_from(values.len()).map_err(|_| ScopeError::Integer)?,
                );
                tasks.extend(values.iter().rev().map(Task::Value));
            }
            V::Object(values) => {
                let mut keys = Vec::with_capacity(values.len());
                for (k, v) in values {
                    let mut encoded = Vec::new();
                    text(&mut encoded, k)?;
                    keys.push((encoded, v));
                }
                keys.sort_by(|(a, _), (b, _)| a.len().cmp(&b.len()).then_with(|| a.cmp(b)));
                head(
                    out,
                    5,
                    u64::try_from(keys.len()).map_err(|_| ScopeError::Integer)?,
                );
                for (key, v) in keys.into_iter().rev() {
                    tasks.push(Task::Value(v));
                    tasks.push(Task::Key(key));
                }
            }
        }
    }
    Ok(())
}

#[cfg(test)]
#[path = "rust_scope_data_tests.rs"]
mod tests;
