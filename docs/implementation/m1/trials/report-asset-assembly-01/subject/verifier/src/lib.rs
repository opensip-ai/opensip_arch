//! Report asset integrity algorithm. Platform handle safety and compiled bundle
//! selection are separate integration duties; this trial grants no authority.
#![forbid(unsafe_code)]

use opensip_identity::{JsonValue, parse_json, raw_sha256};
use std::collections::BTreeMap;
use std::io::{self, Read};

const MAX_LENGTH: u64 = 9_007_199_254_740_990;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum AssetError {
    Io,
    Length,
    Digest,
    Shape,
    Path,
    Order,
    SelfListed,
    Incompatible,
    Unlisted,
    Allocation,
}

/// Private to the reporting owner in product integration. It must be compiled
/// into the trusted host, never deserialized from a request or runtime file.
#[derive(Clone, Debug)]
pub struct FixturePin {
    pub root: String,
    pub manifest_path: String,
    pub manifest_sha256: [u8; 32],
    pub manifest_bytes: u64,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Role {
    Script,
    Style,
    Font,
    Image,
    Notice,
}

#[derive(Clone, Debug, PartialEq, Eq)]
struct Member {
    path: String,
    sha256: [u8; 32],
    bytes: u64,
    role: Role,
}

/// No public constructor or mutable byte access. Contents were checked against
/// the independently pinned manifest, not a digest supplied alongside each file.
#[derive(Debug)]
pub struct VerifiedAsset {
    path: String,
    role: Role,
    bytes: Vec<u8>,
}

impl VerifiedAsset {
    pub fn path(&self) -> &str {
        &self.path
    }
    pub fn role(&self) -> Role {
        self.role
    }
    pub fn bytes(&self) -> &[u8] {
        &self.bytes
    }
}

/// Keeps the checked manifest's identity and asset root with its verified bytes.
/// A caller cannot substitute another pin when checking inventory completeness.
#[derive(Debug)]
pub struct VerifiedBundle {
    root: String,
    manifest_path: String,
    manifest_sha256: [u8; 32],
    projection_sha256: [u8; 32],
    assets: Vec<VerifiedAsset>,
}
impl VerifiedBundle {
    pub fn assets(&self) -> &[VerifiedAsset] {
        &self.assets
    }
    pub fn projection_sha256(&self) -> &[u8; 32] {
        &self.projection_sha256
    }
    pub fn manifest_sha256(&self) -> &[u8; 32] {
        &self.manifest_sha256
    }
}

/// Platform-owned adapter obligation: walk from a retained trusted release
/// directory handle, reject symlinks at every segment and nonregular endpoints,
/// and return the same opened file handle used for reading. No path reopening.
/// This trait is an explicit trusted-host boundary, not a sandbox/capability.
pub trait AssetSource {
    type Reader: Read;
    fn open_regular(&mut self, release_relative: &str) -> io::Result<Self::Reader>;
}

fn canonical_path(path: &str) -> bool {
    let scheme = path
        .split('/')
        .next()
        .unwrap_or("")
        .split_once(':')
        .is_some();
    !path.is_empty()
        && path.chars().count() <= 4096
        && !scheme
        && !path.contains(['\\', '\0'])
        && path.split('/').all(|p| !matches!(p, "" | "." | ".."))
}

fn under(path: &str, root: &str) -> bool {
    path.strip_prefix(root)
        .is_some_and(|tail| tail.starts_with('/') && tail.len() > 1)
}

fn object<'a>(
    value: &'a JsonValue,
    keys: &[&str],
) -> Result<&'a BTreeMap<String, JsonValue>, AssetError> {
    let JsonValue::Object(map) = value else {
        return Err(AssetError::Shape);
    };
    if map.len() != keys.len() || !keys.iter().all(|key| map.contains_key(*key)) {
        return Err(AssetError::Shape);
    }
    Ok(map)
}

fn text(value: &JsonValue) -> Result<&str, AssetError> {
    match value {
        JsonValue::String(s) => Ok(s),
        _ => Err(AssetError::Shape),
    }
}

fn array(value: &JsonValue) -> Result<&[JsonValue], AssetError> {
    match value {
        JsonValue::Array(a) => Ok(a),
        _ => Err(AssetError::Shape),
    }
}

fn length(value: &JsonValue) -> Result<u64, AssetError> {
    let JsonValue::Integer(n) = value else {
        return Err(AssetError::Shape);
    };
    u64::try_from(n.get())
        .ok()
        .filter(|n| *n <= MAX_LENGTH)
        .ok_or(AssetError::Shape)
}

fn digest(value: &JsonValue) -> Result<[u8; 32], AssetError> {
    let s = text(value)?.as_bytes();
    if s.len() != 64
        || !s
            .iter()
            .all(|x| x.is_ascii_digit() || (b'a'..=b'f').contains(x))
    {
        return Err(AssetError::Shape);
    }
    let digit = |v: u8| if v <= b'9' { v - b'0' } else { v - b'a' + 10 };
    Ok(std::array::from_fn(|i| {
        digit(s[i * 2]) * 16 + digit(s[i * 2 + 1])
    }))
}

/// Reads at most expected + 1 bytes even from a growing file. Allocation grows
/// only with bytes actually supplied; declared lengths never reserve huge memory.
fn checked_read(
    mut reader: impl Read,
    expected: u64,
    sha256: &[u8; 32],
) -> Result<Vec<u8>, AssetError> {
    if expected > MAX_LENGTH {
        return Err(AssetError::Length);
    }
    let mut left = expected + 1;
    let mut data = Vec::new();
    let mut buffer = [0; 16 * 1024];
    while left > 0 {
        let cap = left.min(buffer.len() as u64) as usize;
        let count = match reader.read(&mut buffer[..cap]) {
            Ok(n) => n,
            Err(e) if e.kind() == io::ErrorKind::Interrupted => continue,
            Err(_) => return Err(AssetError::Io),
        };
        if count == 0 {
            break;
        }
        if count > cap {
            return Err(AssetError::Io);
        }
        data.try_reserve(count)
            .map_err(|_| AssetError::Allocation)?;
        data.extend_from_slice(&buffer[..count]);
        left -= count as u64;
    }
    if data.len() as u64 != expected {
        return Err(AssetError::Length);
    }
    if raw_sha256(&data) != *sha256 {
        return Err(AssetError::Digest);
    }
    Ok(data)
}

fn manifest(
    raw: &[u8],
    pin: &FixturePin,
    projection: &[u8; 32],
) -> Result<Vec<Member>, AssetError> {
    let value = parse_json(raw).map_err(|_| AssetError::Shape)?;
    let doc = object(
        &value,
        &["schemaVersion", "projectionSchemaSha256s", "assets"],
    )?;
    if length(&doc["schemaVersion"])? != 1 {
        return Err(AssetError::Shape);
    }
    let schemas = array(&doc["projectionSchemaSha256s"])?;
    if schemas.is_empty() {
        return Err(AssetError::Shape);
    }
    let mut previous = None;
    let mut compatible = false;
    for item in schemas {
        let current = digest(item)?;
        if previous.is_some_and(|p| p >= current) {
            return Err(AssetError::Order);
        }
        compatible |= current == *projection;
        previous = Some(current);
    }
    if !compatible {
        return Err(AssetError::Incompatible);
    }
    let rows = array(&doc["assets"])?;
    if rows.is_empty() {
        return Err(AssetError::Shape);
    }
    let mut members: Vec<Member> = Vec::new();
    for row in rows {
        let fields = object(row, &["path", "sha256", "bytes", "role"])?;
        let path = text(&fields["path"])?;
        if !canonical_path(path) || !under(path, &pin.root) {
            return Err(AssetError::Path);
        }
        if path == pin.manifest_path {
            return Err(AssetError::SelfListed);
        }
        if members
            .last()
            .is_some_and(|old| old.path.as_bytes() >= path.as_bytes())
        {
            return Err(AssetError::Order);
        }
        let role = match text(&fields["role"])? {
            "script" => Role::Script,
            "style" => Role::Style,
            "font" => Role::Font,
            "image" => Role::Image,
            "notice" => Role::Notice,
            _ => return Err(AssetError::Shape),
        };
        members.push(Member {
            path: path.into(),
            sha256: digest(&fields["sha256"])?,
            bytes: length(&fields["bytes"])?,
            role,
        });
    }
    Ok(members)
}

/// Development algorithm trial entry point. Product integration must replace
/// FixturePin with a private compiled constant and the projection with the
/// selected renderer's compiled schema digest. This function is NOT that API.
pub fn verify_fixture_assets(
    source: &mut impl AssetSource,
    pin: &FixturePin,
    projection: &[u8; 32],
) -> Result<VerifiedBundle, AssetError> {
    if !canonical_path(&pin.root)
        || !canonical_path(&pin.manifest_path)
        || !under(&pin.manifest_path, &pin.root)
    {
        return Err(AssetError::Path);
    }
    // The current exact-JSON parser has a 4 MiB profile. This is a declared trial
    // limit, checked before opening; final build must prove its actual manifest
    // fits or select a separately reviewed bounded private-manifest profile.
    if pin.manifest_bytes == 0 || pin.manifest_bytes > opensip_identity::MAX_BYTES as u64 {
        return Err(AssetError::Length);
    }
    let raw = checked_read(
        source
            .open_regular(&pin.manifest_path)
            .map_err(|_| AssetError::Io)?,
        pin.manifest_bytes,
        &pin.manifest_sha256,
    )?;
    let members = manifest(&raw, pin, projection)?;
    let mut verified = Vec::new();
    for member in members {
        let bytes = checked_read(
            source
                .open_regular(&member.path)
                .map_err(|_| AssetError::Io)?,
            member.bytes,
            &member.sha256,
        )?;
        verified.push(VerifiedAsset {
            path: member.path,
            role: member.role,
            bytes,
        });
    }
    // No partial verified collection is returned on any failure.
    Ok(VerifiedBundle {
        root: pin.root.clone(),
        manifest_path: pin.manifest_path.clone(),
        manifest_sha256: pin.manifest_sha256,
        projection_sha256: *projection,
        assets: verified,
    })
}

/// Build assembly supplies its complete no-symlink regular-file enumeration.
/// It must verify all bytes independently; this check only establishes set
/// completeness and the exact single manifest exclusion.
pub fn fixture_completeness(
    verified: &VerifiedBundle,
    regular_paths: &[String],
) -> Result<(), AssetError> {
    let mut expected: Vec<_> = verified.assets.iter().map(|a| a.path.as_str()).collect();
    expected.push(&verified.manifest_path);
    expected.sort_unstable();
    if regular_paths
        .iter()
        .any(|p| !canonical_path(p) || !under(p, &verified.root))
    {
        return Err(AssetError::Path);
    }
    let mut actual: Vec<_> = regular_paths.iter().map(String::as_str).collect();
    actual.sort_unstable();
    if expected != actual {
        return Err(AssetError::Unlisted);
    }
    Ok(())
}

#[cfg(test)]
mod tests;

#[cfg(test)]
mod asset_tests;
