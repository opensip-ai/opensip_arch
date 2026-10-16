// M3-B r8 item 14a, as r9 amends its reading grammar and r10 its bounds
// (units B2-c2 and B2-c2b, B2-c plan r2 section 2.2): the pre-Plan
// TypeScript configuration graph and effective `allowJs`. For a `tsjs`
// marker whose first present marker is `tsconfig.json` or `jsconfig.json`
// (U-1), the host reads the marker and every base it `extends`, as JSONC
// data (`jsonc.rs`), through a custody source, and derives NE:527-545's
// effective `allowJs`. C2's `TypeScriptConfigGraphV1` is this graph.
//
// Pure: the only reads are the caller's `ConfigSource`; no I/O, process,
// socket, write or environment read here (FW-01). A graph that cannot be read
// refuses with one of item 14a's four internal keys, aliased at the host
// boundary to the public record `native.typescript-config-unresolved`
// (contract successor S10; M3-J1 r7 item 10 row 59).
//
// No production caller yet: J1 composes this with C1's snapshot custody.
use crate::discovery::{Family, InternalFault, MarkerFact, UnitDiscovery};
use crate::jsonc::{self, Document, Node};
use opensip_identity::{digest_hex, raw_sha256};
use std::collections::BTreeMap;

/// Item 14a's per-file bound, in bytes.
pub(crate) const MAX_CONFIG_FILE_BYTES: usize = 64 * 1024;
/// Item 14a's graph bound, in nodes.
pub(crate) const MAX_CONFIG_NODES: usize = 32;
/// M3-B r10: at most 64 entries in one file's `extends` array, repetitions
/// included (`TypeScriptConfigGraphV1`'s `extendsResolved` bound).
pub(crate) const MAX_EXTENDS_ENTRIES: usize = 64;
/// M3-B r10: at most 4,096 characters in a node's canonical path
/// (`CanonicalPath`'s `maxLength`, which counts characters, not bytes).
pub(crate) const MAX_NODE_PATH_CHARS: usize = 4096;
/// npm's bound on a package name (item 14a's name grammar).
const MAX_PACKAGE_NAME_CHARS: usize = 214;

// ------------------------------------------------------------------ the source

/// What the custody source finds at one project-relative path.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) enum ConfigEntry {
    /// A regular file: its bytes, at most `limit + 1` of them.
    File(Vec<u8>),
    /// Nothing, a directory, or anything else that is not a regular file.
    NotAFile,
    /// The path, or a directory on it, is a symbolic link the custody does
    /// not admit. Before C1's composition every link is one.
    Link,
}

/// The snapshot custody the reader reads through (C1's; a test tree until
/// then). `path` is canonical and project-relative: no leading `/`, and no
/// `.`, `..` or empty segment.
pub(crate) trait ConfigSource {
    fn read(&self, path: &str, limit: usize) -> ConfigEntry;
}

// ------------------------------------------------------------------ refusals

/// Item 14a's internal decision keys.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub(crate) enum ConfigRefusalKey {
    Bound,
    ExtendsCycle,
    ExtendsUnresolved,
    Malformed,
}
impl ConfigRefusalKey {
    pub(crate) fn key(self) -> &'static str {
        match self {
            Self::Bound => "native.typescript-config-bound",
            Self::ExtendsCycle => "native.typescript-config-extends-cycle",
            Self::ExtendsUnresolved => "native.typescript-config-extends-unresolved",
            Self::Malformed => "native.typescript-config-malformed",
        }
    }
}

/// A refusal: the internal class and the project-relative path of the
/// configuration file that refused (item 14a, "The subject").
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct ConfigRefusal {
    pub(crate) key: ConfigRefusalKey,
    pub(crate) path: String,
}
impl ConfigRefusal {
    fn at(key: ConfigRefusalKey, path: &str) -> Self {
        Self {
            key,
            path: path.to_owned(),
        }
    }
    /// The raw subject, `<internal key>:<path>`; the termination bounds it.
    pub(crate) fn subject(&self) -> String {
        format!("{}:{}", self.key.key(), self.path)
    }
}

/// A refusal, or a composition fault with no public detail: an entry the
/// marker inventory names that the source does not hold as a regular file,
/// or an entry path that is not canonical.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) enum ConfigFault {
    Refused(ConfigRefusal),
    Internal(InternalFault),
}

/// The registry's `internalAliases` rows for item 14a's keys
/// (S10's `public-detail-registry.v1.json`), pinned by the tests.
pub(crate) const TYPESCRIPT_CONFIG_ALIASES: [(&str, &str); 4] = [
    (
        "native.typescript-config-bound",
        "native.typescript-config-unresolved",
    ),
    (
        "native.typescript-config-extends-cycle",
        "native.typescript-config-unresolved",
    ),
    (
        "native.typescript-config-extends-unresolved",
        "native.typescript-config-unresolved",
    ),
    (
        "native.typescript-config-malformed",
        "native.typescript-config-unresolved",
    ),
];

/// The public `DomainDetailCode` of one of item 14a's internal keys. An
/// unknown key refuses: the alias map is closed.
pub(crate) fn public_detail(internal: &str) -> Result<&'static str, InternalFault> {
    TYPESCRIPT_CONFIG_ALIASES
        .iter()
        .find(|(key, _)| *key == internal)
        .map(|(_, public)| *public)
        .ok_or_else(|| InternalFault(format!("unknown internal detail key: {internal}")))
}

// ------------------------------------------------------------------ the graph

/// `TypeScriptConfigGraphV1.nodes[].kind`, from the exact basename.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum NodeKind {
    Tsconfig,
    Jsconfig,
    Other,
}
impl NodeKind {
    fn of(path: &str) -> Self {
        match path.rsplit('/').next() {
            Some("tsconfig.json") => Self::Tsconfig,
            Some("jsconfig.json") => Self::Jsconfig,
            _ => Self::Other,
        }
    }
    pub(crate) fn as_str(self) -> &'static str {
        match self {
            Self::Tsconfig => "tsconfig",
            Self::Jsconfig => "jsconfig",
            Self::Other => "other",
        }
    }
}

/// One node of `TypeScriptConfigGraphV1`.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct ConfigNode {
    pub(crate) path: String,
    pub(crate) content_sha256: String,
    pub(crate) kind: NodeKind,
    /// Every `extends` edge in declaration order, repetitions kept.
    pub(crate) extends_resolved: Vec<String>,
}

/// `TypeScriptConfigGraphV1`: the entry and every file read, by path.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct ConfigGraph {
    pub(crate) entry_config_path: String,
    pub(crate) nodes: Vec<ConfigNode>,
}

/// The marker's effective options and the graph they were derived over.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct EffectiveOptions {
    pub(crate) allow_js: bool,
    pub(crate) check_js: bool,
    pub(crate) graph: ConfigGraph,
    pub(crate) work: Work,
}

/// The derivation's work: each node's inherited options are computed once,
/// in postorder, and each edge is merged once (repetitions included), so the
/// work is linear in the graph however its bases repeat or are shared.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) struct Work {
    pub(crate) node_evaluations: usize,
    pub(crate) edge_merges: usize,
}

/// The fields item 14a reads from one file.
struct ConfigFile {
    allow_js: Option<bool>,
    check_js: Option<bool>,
    extends: Vec<String>,
}

/// One file's fields, or `malformed`. An empty document (whitespace and
/// comments only) is an empty object, and the root and `compilerOptions`
/// must be objects (M3-B r9).
fn read_fields(bytes: &[u8]) -> Option<ConfigFile> {
    let document = jsonc::parse(bytes).ok()?;
    let mut file = ConfigFile {
        allow_js: None,
        check_js: None,
        extends: Vec::new(),
    };
    let Some(root) = document.root() else {
        return Some(file);
    };
    if !matches!(root, Node::Object(_)) {
        return None;
    }
    if let Some(options) = document.member(root, "compilerOptions") {
        if !matches!(options, Node::Object(_)) {
            return None;
        }
        file.allow_js = flag(&document, options, "allowJs")?;
        file.check_js = flag(&document, options, "checkJs")?;
    }
    match document.member(root, "extends") {
        None => {}
        Some(Node::String(specifier)) => file.extends.push(specifier.clone()),
        Some(Node::Array(items)) => {
            for index in items {
                match document.node(*index) {
                    Node::String(specifier) => file.extends.push(specifier.clone()),
                    _ => return None,
                }
            }
        }
        Some(_) => return None,
    }
    Some(file)
}

/// An optional boolean member: `Some(None)` absent, `None` the wrong type.
fn flag(document: &Document, options: &Node, key: &str) -> Option<Option<bool>> {
    match document.member(options, key) {
        None => Some(None),
        Some(Node::Bool(value)) => Some(Some(*value)),
        Some(_) => None,
    }
}

// ------------------------------------------------------------------ the specifier grammar

/// A specifier, classified in item 14a's order.
#[derive(Debug, Clone, PartialEq, Eq)]
enum Specifier<'s> {
    /// `./` or `../`: every `/`-separated segment, the first included.
    Path(Vec<&'s str>),
    Absolute,
    Package {
        name: &'s str,
        subpath: Vec<&'s str>,
    },
}

fn name_first(byte: u8) -> bool {
    byte.is_ascii_lowercase() || byte.is_ascii_digit() || byte == b'~' || byte == b'-'
}
fn name_rest(byte: u8) -> bool {
    name_first(byte) || byte == b'.' || byte == b'_'
}
/// The length of the name prefix matching
/// `^(@[a-z0-9~-][a-z0-9._~-]*/)?[a-z0-9~-][a-z0-9._~-]*`, if any.
fn package_name_len(text: &str) -> Option<usize> {
    let bytes = text.as_bytes();
    let mut at = 0;
    if bytes.first() == Some(&b'@') {
        at = 1;
        if !bytes.get(at).is_some_and(|b| name_first(*b)) {
            return None;
        }
        at += 1;
        while bytes.get(at).is_some_and(|b| name_rest(*b)) {
            at += 1;
        }
        if bytes.get(at) != Some(&b'/') {
            return None;
        }
        at += 1;
    }
    if !bytes.get(at).is_some_and(|b| name_first(*b)) {
        return None;
    }
    at += 1;
    while bytes.get(at).is_some_and(|b| name_rest(*b)) {
        at += 1;
    }
    Some(at)
}

/// Item 14a's closed grammar; `None` is malformed.
fn classify(specifier: &str) -> Option<Specifier<'_>> {
    if specifier.is_empty()
        || specifier.contains('\\')
        || specifier.chars().any(|c| c < '\u{20}')
        || specifier.ends_with('/')
        || specifier.contains("//")
    {
        return None;
    }
    if specifier.starts_with("./") || specifier.starts_with("../") {
        return Some(Specifier::Path(specifier.split('/').collect()));
    }
    if specifier.starts_with('/') {
        return Some(Specifier::Absolute);
    }
    let len = package_name_len(specifier)?;
    let name = &specifier[..len];
    if name.chars().count() > MAX_PACKAGE_NAME_CHARS {
        return None;
    }
    let rest = &specifier[len..];
    let subpath: Vec<&str> = if rest.is_empty() {
        Vec::new()
    } else {
        let segments: Vec<&str> = rest.strip_prefix('/')?.split('/').collect();
        if segments
            .iter()
            .any(|s| s.is_empty() || *s == "." || *s == "..")
        {
            return None;
        }
        segments
    };
    Some(Specifier::Package { name, subpath })
}

/// `dir` joined with `segments`, normalized lexically: `.` dropped, `..`
/// removing the preceding segment. `None` when a `..` rises above the root.
fn normalize(dir: &str, segments: &[&str]) -> Option<String> {
    let mut out: Vec<&str> = dir.split('/').filter(|s| !s.is_empty()).collect();
    for segment in segments {
        match *segment {
            "." => {}
            ".." => {
                out.pop()?;
            }
            other => out.push(other),
        }
    }
    Some(out.join("/"))
}

fn parent(path: &str) -> &str {
    path.rfind('/').map_or("", |at| &path[..at])
}

fn join(dir: &str, tail: &str) -> String {
    if dir.is_empty() {
        tail.to_owned()
    } else {
        format!("{dir}/{tail}")
    }
}

/// The candidates of one specifier from a file in directory `dir`, or the
/// refusal its grammar or containment decides before any file is consulted.
fn candidates(dir: &str, specifier: &str) -> Result<Vec<String>, ConfigRefusalKey> {
    match classify(specifier).ok_or(ConfigRefusalKey::Malformed)? {
        Specifier::Absolute => Err(ConfigRefusalKey::ExtendsUnresolved),
        Specifier::Path(segments) => {
            // The candidate spellings: `S`, then `S.json` unless S's last
            // segment ends in `.json`. Each candidate's containment is
            // decided on its own normalized spelling, before any file is
            // consulted.
            let mut spellings: Vec<Vec<String>> =
                vec![segments.iter().map(|s| (*s).to_owned()).collect()];
            let last = segments.len() - 1;
            if !segments[last].ends_with(".json") {
                let mut with_json = spellings[0].clone();
                with_json[last].push_str(".json");
                spellings.push(with_json);
            }
            spellings
                .iter()
                .map(|spelling| {
                    let refs: Vec<&str> = spelling.iter().map(String::as_str).collect();
                    normalize(dir, &refs).ok_or(ConfigRefusalKey::ExtendsUnresolved)
                })
                .collect()
        }
        Specifier::Package { name, subpath } => {
            let sub = subpath.join("/");
            let mut out = Vec::new();
            let mut at = Some(dir);
            while let Some(e) = at {
                let base = join(e, &format!("node_modules/{name}"));
                if sub.is_empty() {
                    out.push(base.clone());
                    out.push(format!("{base}.json"));
                    out.push(format!("{base}/tsconfig.json"));
                } else {
                    out.push(format!("{base}/{sub}"));
                    out.push(format!("{base}/{sub}.json"));
                }
                at = (!e.is_empty()).then(|| parent(e));
            }
            Ok(out)
        }
    }
}

// ------------------------------------------------------------------ the walk

#[derive(Clone, Copy, PartialEq, Eq)]
enum Visit {
    OnPath,
    Done,
}

struct Read {
    sha256: String,
    kind: NodeKind,
    /// The node's inherited `allowJs` and `checkJs`, before defaults.
    inherited: (Option<bool>, Option<bool>),
    edges: Vec<String>,
}

struct Walk<'s> {
    source: &'s dyn ConfigSource,
    state: BTreeMap<String, Visit>,
    reads: BTreeMap<String, Read>,
    work: Work,
}
impl Walk<'_> {
    /// The file a specifier names: the first candidate that is a regular
    /// file. A link on any candidate's path refuses (before C1).
    fn resolve(&self, from: &str, specifier: &str) -> Result<(String, Vec<u8>), ConfigRefusal> {
        let list =
            candidates(parent(from), specifier).map_err(|key| ConfigRefusal::at(key, from))?;
        for candidate in list {
            if candidate.is_empty() {
                // The project root is a directory, never a file.
                continue;
            }
            match self.source.read(&candidate, MAX_CONFIG_FILE_BYTES) {
                ConfigEntry::File(bytes) => return Ok((candidate, bytes)),
                ConfigEntry::NotAFile => {}
                ConfigEntry::Link => {
                    return Err(ConfigRefusal::at(ConfigRefusalKey::ExtendsUnresolved, from));
                }
            }
        }
        Err(ConfigRefusal::at(ConfigRefusalKey::ExtendsUnresolved, from))
    }
    /// Read node `path` from `bytes` and walk its bases in order. Cycle and
    /// node bounds are checked on node identities as the graph is built.
    /// M3-B r10: the path length comes before the bytes are judged, and the
    /// `extends` count after the JSONC and types, before any entry resolves.
    fn visit(&mut self, path: String, bytes: Vec<u8>) -> Result<(), ConfigRefusal> {
        if path.chars().count() > MAX_NODE_PATH_CHARS || bytes.len() > MAX_CONFIG_FILE_BYTES {
            return Err(ConfigRefusal::at(ConfigRefusalKey::Bound, &path));
        }
        let file = read_fields(&bytes)
            .ok_or_else(|| ConfigRefusal::at(ConfigRefusalKey::Malformed, &path))?;
        if file.extends.len() > MAX_EXTENDS_ENTRIES {
            return Err(ConfigRefusal::at(ConfigRefusalKey::Bound, &path));
        }
        self.state.insert(path.clone(), Visit::OnPath);
        let mut edges = Vec::new();
        for specifier in &file.extends {
            let (target, target_bytes) = self.resolve(&path, specifier)?;
            match self.state.get(&target) {
                Some(Visit::OnPath) => {
                    return Err(ConfigRefusal::at(ConfigRefusalKey::ExtendsCycle, &path));
                }
                Some(Visit::Done) => {}
                None => {
                    if self.state.len() == MAX_CONFIG_NODES {
                        return Err(ConfigRefusal::at(ConfigRefusalKey::Bound, &path));
                    }
                    self.visit(target.clone(), target_bytes)?;
                }
            }
            edges.push(target);
        }
        // NE:527-545, in postorder: every base is already done, so its
        // inherited options are read once, never recomputed. A `jsconfig`
        // node supplies `allowJs: true` unless it writes `allowJs`; a later
        // base beats an earlier one; a node's own options beat its bases.
        let kind = NodeKind::of(&path);
        let (mut allow_js, mut check_js) = (None, None);
        for edge in &edges {
            let (a, c) = self.reads[edge].inherited;
            allow_js = a.or(allow_js);
            check_js = c.or(check_js);
            self.work.edge_merges += 1;
        }
        let own_allow_js = match (kind, file.allow_js) {
            (NodeKind::Jsconfig, None) => Some(true),
            (_, written) => written,
        };
        self.work.node_evaluations += 1;
        self.state.insert(path.clone(), Visit::Done);
        self.reads.insert(
            path,
            Read {
                sha256: digest_hex(&raw_sha256(&bytes)),
                kind,
                inherited: (own_allow_js.or(allow_js), file.check_js.or(check_js)),
                edges,
            },
        );
        Ok(())
    }
}

fn canonical_path(path: &str) -> bool {
    !path.is_empty()
        && path
            .split('/')
            .all(|s| !s.is_empty() && s != "." && s != "..")
}

/// Item 14a: the effective `allowJs` (and `checkJs`) of the configuration
/// file at project-relative `entry`, over its `extends` graph.
pub(crate) fn effective_allow_js(
    entry: &str,
    source: &dyn ConfigSource,
) -> Result<EffectiveOptions, ConfigFault> {
    if !canonical_path(entry) {
        return Err(ConfigFault::Internal(InternalFault(format!(
            "NATIVE_TYPESCRIPT_CONFIG_ENTRY_NOT_CANONICAL:{entry}"
        ))));
    }
    let bytes = match source.read(entry, MAX_CONFIG_FILE_BYTES) {
        ConfigEntry::File(bytes) => bytes,
        ConfigEntry::Link => {
            return Err(ConfigFault::Refused(ConfigRefusal::at(
                ConfigRefusalKey::ExtendsUnresolved,
                entry,
            )));
        }
        ConfigEntry::NotAFile => {
            return Err(ConfigFault::Internal(InternalFault(format!(
                "NATIVE_TYPESCRIPT_CONFIG_ENTRY_NOT_A_FILE:{entry}"
            ))));
        }
    };
    let mut walk = Walk {
        source,
        state: BTreeMap::new(),
        reads: BTreeMap::new(),
        work: Work {
            node_evaluations: 0,
            edge_merges: 0,
        },
    };
    walk.visit(entry.to_owned(), bytes)
        .map_err(ConfigFault::Refused)?;
    let (allow_js, check_js) = walk.reads[entry].inherited;
    let check_js = check_js.unwrap_or(false);
    let nodes = walk
        .reads
        .iter()
        .map(|(path, read)| ConfigNode {
            path: path.clone(),
            content_sha256: read.sha256.clone(),
            kind: read.kind,
            extends_resolved: read.edges.clone(),
        })
        .collect();
    Ok(EffectiveOptions {
        allow_js: allow_js.unwrap_or(check_js),
        check_js,
        graph: ConfigGraph {
            entry_config_path: entry.to_owned(),
            nodes,
        },
        work: walk.work,
    })
}

/// Item 14a's composition with U-1: for every `tsjs` unit of `discovery`
/// whose marker is `tsconfig.json` or `jsconfig.json`, the marker
/// observation's `allowJs` becomes the effective value read from bytes.
/// Discovery decides which marker directories survive, and U-1's mode is
/// the only thing `allowJs` changes, so a second discovery over the
/// returned markers gives the same units with their modes decided. A
/// refused discovery reads nothing. The first refusal, in unit order, wins.
pub(crate) fn observe_effective_allow_js(
    markers: &BTreeMap<String, MarkerFact>,
    discovery: &UnitDiscovery,
    source: &dyn ConfigSource,
) -> Result<BTreeMap<String, MarkerFact>, ConfigFault> {
    let mut observed = markers.clone();
    if discovery.refused.is_some() {
        return Ok(observed);
    }
    for unit in &discovery.units {
        let config = matches!(
            unit.marker_path.rsplit('/').next(),
            Some("tsconfig.json" | "jsconfig.json")
        );
        if unit.language_family != Family::Tsjs || !config {
            continue;
        }
        let effective = effective_allow_js(&unit.marker_path, source)?;
        match observed.get_mut(&unit.marker_path) {
            Some(fact) => fact.allow_js = Some(effective.allow_js),
            None => {
                return Err(ConfigFault::Internal(InternalFault(format!(
                    "NATIVE_TYPESCRIPT_CONFIG_MARKER_NOT_OBSERVED:{}",
                    unit.marker_path
                ))));
            }
        }
    }
    Ok(observed)
}
