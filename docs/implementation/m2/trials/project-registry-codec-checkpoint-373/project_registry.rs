//! Pure syntax and complete-document invariants for the private project registry.
//! Decoded values are NOT native custody, registration, leases or authority.
//! No filesystem, entropy, allocation reservation, mutation or recovery is done here.
use crate::{CanonicalError, JsonValue as V, canonical_bytes, parse_json};
use alloc::{
    collections::{BTreeMap, BTreeSet},
    string::String,
    vec::Vec,
};

pub const REGISTRY_CAP: usize = 4_194_304;
pub const REGISTRY_ROW_CAP: usize = 4096;
pub const PROJECT_MARKER_SIZE: usize = 92;
const MARKER_PREFIX: &[u8] = b"opensip-project-id-v1\n";

#[derive(Debug, PartialEq, Eq)]
pub enum Error {
    Bound,
    Canonical(CanonicalError),
    Shape,
    Version,
    ProjectId,
    Namespace,
    Platform,
    RootPath,
    UnsignedDecimal,
    BirthTime,
    Status,
    AllocationKind,
    NamespaceOrder,
    DuplicateLiveProject,
    DuplicateLiveLocator,
    DuplicateLiveIncarnation,
    NonCanonical,
    Marker,
}

fn hex_byte(b: u8) -> Option<u8> {
    match b {
        b'0'..=b'9' => Some(b - b'0'),
        b'a'..=b'f' => Some(b - b'a' + 10),
        _ => None,
    }
}
fn project_id(s: &str) -> bool {
    s.strip_prefix("prj1-")
        .is_some_and(|h| h.len() == 64 && h.bytes().all(|b| hex_byte(b).is_some()))
}
fn namespace(s: &str) -> bool {
    let b = s.as_bytes();
    b.len() == 36
        && b[14] == b'4'
        && matches!(b[19], b'8' | b'9' | b'a' | b'b')
        && b.iter().enumerate().all(|(i, b)| {
            if [8, 13, 18, 23].contains(&i) {
                *b == b'-'
            } else {
                hex_byte(*b).is_some()
            }
        })
}
fn object<'a>(v: &'a V, fields: &[&str]) -> Result<&'a BTreeMap<String, V>, Error> {
    let V::Object(o) = v else {
        return Err(Error::Shape);
    };
    if o.len() != fields.len() || !fields.iter().all(|f| o.contains_key(*f)) {
        return Err(Error::Shape);
    }
    Ok(o)
}
fn text(v: &V) -> Result<&str, Error> {
    if let V::String(s) = v {
        Ok(s)
    } else {
        Err(Error::Shape)
    }
}
fn integer(v: &V) -> Result<i128, Error> {
    if let V::Integer(n) = v {
        Ok(n.get())
    } else {
        Err(Error::Shape)
    }
}
fn decimal(v: &V) -> Result<u64, Error> {
    let s = text(v)?;
    if s.is_empty()
        || s.len() > 20
        || (s.len() > 1 && s.starts_with('0'))
        || !s.bytes().all(|b| b.is_ascii_digit())
    {
        return Err(Error::UnsignedDecimal);
    }
    s.parse().map_err(|_| Error::UnsignedDecimal)
}
fn path(v: &V) -> Result<Vec<u8>, Error> {
    let s = text(v)?;
    if s.is_empty() || s.len() > 8192 || s.len() % 2 != 0 {
        return Err(Error::RootPath);
    }
    let mut bytes = Vec::with_capacity(s.len() / 2);
    for pair in s.as_bytes().chunks_exact(2) {
        let high = hex_byte(pair[0]).ok_or(Error::RootPath)?;
        let low = hex_byte(pair[1]).ok_or(Error::RootPath)?;
        bytes.push(high * 16 + low);
    }
    if bytes[0] != b'/'
        || bytes.contains(&0)
        || bytes.windows(2).any(|p| p == b"//")
        || (bytes.len() > 1 && bytes.ends_with(b"/"))
        || bytes.split(|b| *b == b'/').any(|p| p == b"." || p == b"..")
    {
        return Err(Error::RootPath);
    }
    Ok(bytes)
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum Platform {
    Macos,
    Linux,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Root {
    platform: Platform,
    path: Vec<u8>,
    device: u64,
    inode: u64,
    birth_seconds: i64,
    birth_nanoseconds: u32,
}
impl Root {
    fn decode(v: &V) -> Result<Self, Error> {
        let o = object(
            v,
            &[
                "platform",
                "canonicalPathBytesHex",
                "deviceId",
                "inodeId",
                "birthSeconds",
                "birthNanoseconds",
            ],
        )?;
        let platform = match text(&o["platform"])? {
            "macos" => Platform::Macos,
            "linux" => Platform::Linux,
            _ => return Err(Error::Platform),
        };
        let seconds = i64::try_from(integer(&o["birthSeconds"])?).map_err(|_| Error::BirthTime)?;
        let nanos =
            u32::try_from(integer(&o["birthNanoseconds"])?).map_err(|_| Error::BirthTime)?;
        if nanos >= 1_000_000_000 {
            return Err(Error::BirthTime);
        }
        Ok(Self {
            platform,
            path: path(&o["canonicalPathBytesHex"])?,
            device: decimal(&o["deviceId"])?,
            inode: decimal(&o["inodeId"])?,
            birth_seconds: seconds,
            birth_nanoseconds: nanos,
        })
    }
    pub fn platform(&self) -> Platform {
        self.platform
    }
    /// Supplied native path bytes only; never an opened root or custody proof.
    pub fn path_bytes(&self) -> &[u8] {
        &self.path
    }
    pub fn device(&self) -> u64 {
        self.device
    }
    pub fn inode(&self) -> u64 {
        self.inode
    }
    pub fn birth_seconds(&self) -> i64 {
        self.birth_seconds
    }
    pub fn birth_nanoseconds(&self) -> u32 {
        self.birth_nanoseconds
    }
    fn incarnation(&self) -> (Platform, u64, u64, i64, u32) {
        (
            self.platform,
            self.device,
            self.inode,
            self.birth_seconds,
            self.birth_nanoseconds,
        )
    }
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Status {
    Reserved,
    Active,
    Retired,
    Abandoned,
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum AllocationKind {
    Random,
    Adopt,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Entry {
    project: String,
    namespace: String,
    root: Root,
    status: Status,
    allocation: AllocationKind,
}
impl Entry {
    fn decode(v: &V) -> Result<Self, Error> {
        let o = object(
            v,
            &[
                "projectId",
                "namespaceId",
                "root",
                "status",
                "allocationKind",
            ],
        )?;
        let project = text(&o["projectId"])?;
        if !project_id(project) {
            return Err(Error::ProjectId);
        }
        let n = text(&o["namespaceId"])?;
        if !namespace(n) {
            return Err(Error::Namespace);
        }
        let status = match text(&o["status"])? {
            "RESERVED" => Status::Reserved,
            "ACTIVE" => Status::Active,
            "RETIRED" => Status::Retired,
            "ABANDONED" => Status::Abandoned,
            _ => return Err(Error::Status),
        };
        let allocation = match text(&o["allocationKind"])? {
            "random" => AllocationKind::Random,
            "adopt" => AllocationKind::Adopt,
            _ => return Err(Error::AllocationKind),
        };
        Ok(Self {
            project: project.into(),
            namespace: n.into(),
            root: Root::decode(&o["root"])?,
            status,
            allocation,
        })
    }
    pub fn project_id(&self) -> &str {
        &self.project
    }
    pub fn namespace_id(&self) -> &str {
        &self.namespace
    }
    pub fn root(&self) -> &Root {
        &self.root
    }
    pub fn status(&self) -> Status {
        self.status
    }
    pub fn allocation_kind(&self) -> AllocationKind {
        self.allocation
    }
}
#[derive(Debug)]
pub struct Registry {
    raw: Vec<u8>,
    entries: Vec<Entry>,
}
impl Registry {
    /// Decode a COMPLETE canonical bounded document. No entry can be obtained
    /// until every row, ordering and live uniqueness rule has passed.
    pub fn decode(raw: &[u8]) -> Result<Self, Error> {
        if raw.len() > REGISTRY_CAP {
            return Err(Error::Bound);
        }
        let v = parse_json(raw).map_err(Error::Canonical)?;
        let o = object(&v, &["schemaVersion", "entries"])?;
        if integer(&o["schemaVersion"])? != 1 {
            return Err(Error::Version);
        }
        let V::Array(rows) = &o["entries"] else {
            return Err(Error::Shape);
        };
        if rows.len() > REGISTRY_ROW_CAP {
            return Err(Error::Bound);
        }
        let mut entries: Vec<Entry> = Vec::with_capacity(rows.len());
        let mut projects = BTreeSet::new();
        let mut locators = BTreeSet::new();
        let mut incarnations = BTreeSet::new();
        for v in rows {
            let e = Entry::decode(v)?;
            if entries
                .last()
                .is_some_and(|prev| prev.namespace >= e.namespace)
            {
                return Err(Error::NamespaceOrder);
            }
            if matches!(e.status, Status::Reserved | Status::Active) {
                if !projects.insert(e.project.clone()) {
                    return Err(Error::DuplicateLiveProject);
                }
                if !locators.insert((e.root.platform, e.root.path.clone())) {
                    return Err(Error::DuplicateLiveLocator);
                }
                if !incarnations.insert(e.root.incarnation()) {
                    return Err(Error::DuplicateLiveIncarnation);
                }
            }
            entries.push(e);
        }
        if canonical_bytes(&v).map_err(Error::Canonical)? != raw {
            return Err(Error::NonCanonical);
        }
        Ok(Self {
            raw: raw.into(),
            entries,
        })
    }
    pub fn raw(&self) -> &[u8] {
        &self.raw
    }
    /// Syntax/whole-document invariant results only; not registered authority.
    pub fn entries(&self) -> &[Entry] {
        &self.entries
    }
    /// Pure projection only. The S9 start gate, transition slot, native carriers,
    /// exact lease set, custody and authorization must be admitted separately.
    pub fn registered_namespace_values(&self) -> impl Iterator<Item = &str> {
        self.entries
            .iter()
            .filter(|e| matches!(e.status, Status::Active | Status::Retired))
            .map(|e| e.namespace.as_str())
    }
    pub fn has_reservations(&self) -> bool {
        self.entries.iter().any(|e| e.status == Status::Reserved)
    }
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ProjectMarker {
    project: String,
}
impl ProjectMarker {
    /// The PROJECT-ID-V1 ASCII frame; this does not inspect VCS tracking, native
    /// custody, the root or registry and cannot mint a verified ProjectId.
    pub fn decode(raw: &[u8]) -> Result<Self, Error> {
        if raw.len() != PROJECT_MARKER_SIZE
            || !raw.starts_with(MARKER_PREFIX)
            || !raw.ends_with(b"\n")
        {
            return Err(Error::Marker);
        }
        let project = core::str::from_utf8(&raw[MARKER_PREFIX.len()..raw.len() - 1])
            .map_err(|_| Error::Marker)?;
        if !project_id(project) {
            return Err(Error::ProjectId);
        }
        Ok(Self {
            project: project.into(),
        })
    }
    pub fn project_id(&self) -> &str {
        &self.project
    }
}
