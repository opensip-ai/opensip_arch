//! Snapshot host frames from C1's immutable sealed manifest projection.
//! Greedy coordinates and wire bounds are checked here; the later sender
//! reads from custody and verifies each completed entry's content digest.
use super::super::super::{
    cbor::{self, Value},
    manifest_digest,
    ts2::carrier::Carriers,
};
use super::{policy::Policy, schedule};
use opensip_identity::parse_json;

#[derive(Debug)]
pub(super) enum Entry {
    File {
        path: String,
        byte_length: u64,
        content_sha256: String,
        executable: bool,
    },
    Symlink {
        path: String,
        target_bytes: Vec<u8>,
    },
}
impl Entry {
    pub(super) fn path(&self) -> &str {
        match self {
            Self::File { path, .. } | Self::Symlink { path, .. } => path,
        }
    }
    fn value(&self, copy_target: bool) -> Value {
        let (kind, length, digest, executable, target) = match self {
            Self::File {
                byte_length,
                content_sha256,
                executable,
                ..
            } => (
                "file",
                Value::Unsigned(*byte_length),
                t(content_sha256),
                Value::Bool(*executable),
                Value::Null,
            ),
            Self::Symlink { target_bytes, .. } => (
                "symlink",
                Value::Null,
                Value::Null,
                Value::Null,
                Value::Bytes(if copy_target {
                    target_bytes.clone()
                } else {
                    Vec::new()
                }),
            ),
        };
        map(vec![
            ("path", t(self.path())),
            ("kind", t(kind)),
            ("byteLength", length),
            ("contentSha256", digest),
            ("executable", executable),
            ("targetBytes", target),
        ])
    }
}
#[derive(Debug, PartialEq, Eq)]
pub(super) enum Refusal {
    Policy(super::policy::Refusal),
    Shape(String),
    Bound(&'static str),
    Join(&'static str),
    Arithmetic,
}
impl From<super::policy::Refusal> for Refusal {
    fn from(v: super::policy::Refusal) -> Self {
        Self::Policy(v)
    }
}
fn t(v: &str) -> Value {
    Value::Text(v.into())
}
fn map(v: Vec<(&str, Value)>) -> Value {
    Value::Map(v.into_iter().map(|(k, v)| (k.into(), v)).collect())
}
fn head(v: u64) -> u64 {
    match v {
        0..=23 => 1,
        24..=255 => 2,
        256..=65_535 => 3,
        65_536..=4_294_967_295 => 5,
        _ => 9,
    }
}
pub(super) struct Built {
    pub manifest: Value,
    pub seal: Value,
    pub chunks: u64,
    pub bytes: u64,
}

pub(super) fn build(
    policy: &Policy,
    snapshot_id: &str,
    entries: &[Entry],
    sequence: u64,
) -> Result<Built, Refusal> {
    let count = u64::try_from(entries.len()).map_err(|_| Refusal::Arithmetic)?;
    if count == 0 || count > policy.limit("maxSnapshotEntries")? {
        return Err(Refusal::Bound("snapshot entries"));
    }
    let carriers = Carriers::load("Rust3").map_err(Refusal::Shape)?;
    carriers
        .check(
            &parse_json(br#"{"t":"ref","ref":"Rust3SnapshotId2"}"#)
                .map_err(|e| Refusal::Shape(e.to_string()))?,
            &t(snapshot_id),
            "snapshotId",
        )
        .map_err(Refusal::Shape)?;
    let maximum = policy.limit("maxSnapshotChunkBytes")?;
    let mut lengths = head(count);
    let mut bytes = 0_u64;
    let mut chunks = 0_u64;
    for (index, entry) in entries.iter().enumerate() {
        carriers
            .check(
                &parse_json(br#"{"t":"ref","ref":"Rust3CanonicalPath"}"#)
                    .map_err(|e| Refusal::Shape(e.to_string()))?,
                &t(entry.path()),
                "path",
            )
            .map_err(Refusal::Shape)?;
        if index > 0 && entries[index - 1].path().as_bytes() >= entry.path().as_bytes() {
            return Err(Refusal::Join("snapshot path order"));
        }
        let probe = entry.value(false);
        let mut length = cbor::encoded_length(&probe).ok_or(Refusal::Arithmetic)?;
        match entry {
            Entry::File { byte_length, .. } => {
                carriers
                    .check_record("Rust3SnapshotEntryV2", &probe)
                    .map_err(Refusal::Shape)?;
                bytes = bytes.checked_add(*byte_length).ok_or(Refusal::Arithmetic)?;
                if bytes > policy.limit("maxSnapshotTotalFileBytes")? {
                    return Err(Refusal::Bound("snapshot file bytes"));
                }
                chunks = chunks
                    .checked_add(
                        schedule::chunk_count(*byte_length, maximum)
                            .map_err(|_| Refusal::Arithmetic)?,
                    )
                    .ok_or(Refusal::Arithmetic)?;
            }
            Entry::Symlink { target_bytes, .. } => {
                let n = u64::try_from(target_bytes.len()).map_err(|_| Refusal::Arithmetic)?;
                if n == 0 || n > policy.limit("maxFramePayloadBytes")? {
                    return Err(Refusal::Bound("snapshot symlink bytes"));
                }
                length = length
                    .checked_sub(1)
                    .and_then(|n0| n0.checked_add(head(n)))
                    .and_then(|n0| n0.checked_add(n))
                    .ok_or(Refusal::Arithmetic)?;
            }
        }
        lengths = lengths.checked_add(length).ok_or(Refusal::Arithmetic)?;
    }
    let probe = map(vec![
        ("snapshotId", t(snapshot_id)),
        ("manifestSha256", t(&"0".repeat(64))),
        ("entries", Value::Null),
    ]);
    let payload_length = cbor::encoded_length(&probe)
        .and_then(|n| n.checked_sub(1))
        .and_then(|n| n.checked_add(lengths))
        .ok_or(Refusal::Arithmetic)?;
    let envelope =
        schedule::envelope_length_for_payload(sequence, "SnapshotManifest", payload_length)
            .map_err(|_| Refusal::Arithmetic)?;
    if envelope > policy.limit("maxFramePayloadBytes")? {
        return Err(Refusal::Bound("snapshot manifest envelope"));
    }
    // Only now copy the symlink bytes into the new manifest value.
    let values = Value::Array(entries.iter().map(|e| e.value(true)).collect());
    let digest = manifest_digest(&values);
    let manifest = map(vec![
        ("snapshotId", t(snapshot_id)),
        ("manifestSha256", t(&digest)),
        ("entries", values),
    ]);
    carriers
        .check_record("Rust3SnapshotManifestV2", &manifest)
        .map_err(Refusal::Shape)?;
    let seal = map(vec![
        ("snapshotId", t(snapshot_id)),
        ("manifestSha256", t(&digest)),
        ("entryCount", Value::Unsigned(count)),
        ("totalFileBytes", Value::Unsigned(bytes)),
        ("totalChunkCount", Value::Unsigned(chunks)),
    ]);
    carriers
        .check_record("Rust3SnapshotSealV2", &seal)
        .map_err(Refusal::Shape)?;
    Ok(Built {
        manifest,
        seal,
        chunks,
        bytes,
    })
}

pub(super) fn chunk(
    policy: &Policy,
    snapshot_id: &str,
    entry: &Entry,
    index: u64,
    offset: u64,
    bytes: Vec<u8>,
) -> Result<Value, Refusal> {
    let Entry::File {
        path, byte_length, ..
    } = entry
    else {
        return Err(Refusal::Join("symlink has no chunks"));
    };
    let maximum = policy.limit("maxSnapshotChunkBytes")?;
    let start = index.checked_mul(maximum).ok_or(Refusal::Arithmetic)?;
    if start != offset || start >= *byte_length {
        return Err(Refusal::Join("snapshot chunk coordinates"));
    }
    let expected = (*byte_length - start).min(maximum);
    if u64::try_from(bytes.len()).map_err(|_| Refusal::Arithmetic)? != expected {
        return Err(Refusal::Join("snapshot greedy chunk length"));
    }
    let value = map(vec![
        ("snapshotId", t(snapshot_id)),
        ("path", t(path)),
        ("chunkIndex", Value::Unsigned(index)),
        ("byteOffset", Value::Unsigned(offset)),
        ("bytes", Value::Bytes(bytes)),
    ]);
    Carriers::load("Rust3")
        .map_err(Refusal::Shape)?
        .check_record("Rust3SnapshotFileChunkV2", &value)
        .map_err(Refusal::Shape)?;
    Ok(value)
}

#[cfg(test)]
#[path = "snapshot_tests.rs"]
mod tests;
