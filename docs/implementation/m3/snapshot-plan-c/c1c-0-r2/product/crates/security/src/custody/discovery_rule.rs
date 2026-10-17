// M3-B r5 items 13 and 14 (unit B2-a): the shared discovery rule, NE §1.4
// U-4a and SL S3 as contract successor B-S1 states them, stated once for the
// security discovery instrument (B2-b) and the native unit instrument (B2-c).
// The reference is the B2-a refresh of discovery-defaults.py (contract
// successor 163): the corrected pruning copy plus SX-1 and the V3 boundary
// inventory. Pure functions over relative logical paths in internal form
// (`""` is the selected root): no filesystem, no environment, no platform
// type. Every output order is UTF-8 byte order. Records, public rows and
// membership are not decided here.
use std::collections::{BTreeMap, BTreeSet};

/// The identity contract's explicit-root sentinel and the internal root.
pub(crate) const ROOT_SENTINEL: &str = ".";
pub(crate) const INTERNAL_ROOT: &str = "";
/// Language markers: a directory holding one is a workspace unit.
pub(crate) const WORKSPACE_MARKERS: [&str; 4] = [
    "Cargo.toml",
    "package.json",
    "tsconfig.json",
    "jsconfig.json",
];
const DEPENDENCY_TREE_SEGMENT: &str = "node_modules";
const VCS_TREE_SEGMENTS: [&str; 4] = [".git", ".hg", ".svn", ".jj"];
const CARGO_BUILD_OUTPUT_SEGMENT: &str = "target";
/// The Cargo manifest's name; the read set observes it (unit C1c-0).
pub(crate) const CARGO_MARKER: &str = "Cargo.toml";
/// SX-1: OpenSIP custody state, an exact anchor at the root and at each
/// admitted D15 member root only.
pub(crate) const OPENSIP_CUSTODY_STATE: &str = ".opensip";
/// The first-party unit cap (SL:216-222; U-7).
pub(crate) const MAX_WORKSPACE_UNITS: usize = 4096;
const MARKER_CUSTODY_PREFIX: &str = "MARKER_CUSTODY:";

/// Why a tree is pruned (`PrunedTreeRowV3.reason`).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum PruneReason {
    DependencyTree,
    VcsTree,
    CargoBuildOutput,
    OpensipCustodyState,
}
impl PruneReason {
    pub(crate) fn as_str(self) -> &'static str {
        match self {
            Self::DependencyTree => "dependency-tree",
            Self::VcsTree => "vcs-tree",
            Self::CargoBuildOutput => "cargo-build-output",
            Self::OpensipCustodyState => "opensip-custody-state",
        }
    }
}

/// The outermost pruned segment a path lies at or below.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct PrunedAnchor {
    pub(crate) path: String,
    pub(crate) reason: PruneReason,
}
impl PrunedAnchor {
    fn new(parts: &[&str], index: usize, reason: PruneReason) -> Self {
        Self {
            path: parts[..=index].join("/"),
            reason,
        }
    }
    /// The anchor's depth: its segment index.
    fn depth(&self) -> usize {
        self.path.matches('/').count()
    }
}

/// An explicit root that is not the sentinel or a strict logical path.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) struct RootGrammar;

/// `.` alone is the selected root `""`. Otherwise a strict logical relative
/// directory with one trailing `/` dropped (a CLI value; Config2 refused it
/// earlier, SL:228-232). Absolute, backslash, NUL, empty, `.` or `..`
/// segments refuse.
pub(crate) fn normalize_explicit_root(spec: &str) -> Result<String, RootGrammar> {
    if spec.is_empty() {
        return Err(RootGrammar);
    }
    if spec == ROOT_SENTINEL {
        return Ok(INTERNAL_ROOT.to_owned());
    }
    if spec.starts_with('/') || spec.contains('\\') || spec.contains('\0') {
        return Err(RootGrammar);
    }
    let body = spec.strip_suffix('/').unwrap_or(spec);
    if body
        .split('/')
        .any(|segment| matches!(segment, "" | "." | ".."))
    {
        return Err(RootGrammar);
    }
    Ok(body.to_owned())
}

/// The inverse spelling for records whose grammar needs non-empty text.
pub(crate) fn spell_root(internal_root: &str) -> &str {
    if internal_root == INTERNAL_ROOT {
        ROOT_SENTINEL
    } else {
        internal_root
    }
}

fn dir_of(relpath: &str) -> &str {
    relpath
        .rsplit_once('/')
        .map_or(INTERNAL_ROOT, |(dir, _)| dir)
}
fn file_name(relpath: &str) -> &str {
    relpath.rsplit_once('/').map_or(relpath, |(_, name)| name)
}

/// Dependency and VCS pruning by exact segment: the outermost such segment.
fn segment_prune(parts: &[&str]) -> Option<PrunedAnchor> {
    parts.iter().enumerate().find_map(|(index, segment)| {
        if *segment == DEPENDENCY_TREE_SEGMENT {
            Some(PrunedAnchor::new(parts, index, PruneReason::DependencyTree))
        } else if VCS_TREE_SEGMENTS.contains(segment) {
            Some(PrunedAnchor::new(parts, index, PruneReason::VcsTree))
        } else {
            None
        }
    })
}

/// SX-1: the outermost `.opensip` directly under the root or an admitted
/// member root. Each member root's segments are compared in place and never
/// collected, so a classification allocates nothing per member (M3-C r9
/// item 2, remedy (b-prime); unit C1a4).
fn custody_state(parts: &[&str], member_roots: &BTreeSet<String>) -> Option<PrunedAnchor> {
    let mut best: Option<usize> = None;
    for base in std::iter::once(INTERNAL_ROOT).chain(member_roots.iter().map(String::as_str)) {
        let k = if base.is_empty() {
            0
        } else {
            base.split('/').count()
        };
        if parts.len() > k
            && (base.is_empty() || parts[..k].iter().copied().eq(base.split('/')))
            && parts[k] == OPENSIP_CUSTODY_STATE
            && best.is_none_or(|b| k < b)
        {
            best = Some(k);
        }
    }
    best.map(|k| PrunedAnchor::new(parts, k, PruneReason::OpensipCustodyState))
}

/// The pruned tree `relpath` (a file or directory) lies in, if any: the
/// outermost anchor across all four reasons. `cargo_roots` are the
/// directories holding `Cargo.toml` (`cargo_roots_from_markers`).
pub(crate) fn classify_path(
    relpath: &str,
    cargo_roots: &BTreeSet<String>,
    member_roots: &BTreeSet<String>,
) -> Option<PrunedAnchor> {
    let parts: Vec<&str> = relpath.split('/').collect();
    let mut hit = segment_prune(&parts);
    if let Some(index) = (0..parts.len()).find(|&i| {
        parts[i] == CARGO_BUILD_OUTPUT_SEGMENT && cargo_roots.contains(&parts[..i].join("/"))
    }) && hit.as_ref().is_none_or(|h| index < h.depth())
    {
        hit = Some(PrunedAnchor::new(
            &parts,
            index,
            PruneReason::CargoBuildOutput,
        ));
    }
    match custody_state(&parts, member_roots) {
        Some(state) if hit.as_ref().is_none_or(|h| state.depth() < h.depth()) => Some(state),
        _ => hit,
    }
}

/// Directories holding `Cargo.toml` outside every pruned tree, derived
/// parent-first so a marker in an already pruned tree never makes a root.
pub(crate) fn cargo_roots_from_markers<S: AsRef<str>>(
    marker_relpaths: &[S],
    member_roots: &BTreeSet<String>,
) -> BTreeSet<String> {
    let mut ordered: Vec<&str> = marker_relpaths.iter().map(AsRef::as_ref).collect();
    ordered.sort_by_key(|path| (path.matches('/').count(), *path));
    let mut roots = BTreeSet::new();
    for marker in ordered {
        if file_name(marker) == CARGO_MARKER
            && classify_path(marker, &roots, member_roots).is_none()
        {
            roots.insert(dir_of(marker).to_owned());
        }
    }
    roots
}

/// Every pruned anchor among the observed directories, without descent.
/// Absolute paths and the root itself are skipped.
pub(crate) fn pruned_anchors_from_directories<S: AsRef<str>>(
    dir_relpaths: &[S],
    cargo_roots: &BTreeSet<String>,
    member_roots: &BTreeSet<String>,
) -> Vec<PrunedAnchor> {
    let mut out = BTreeMap::new();
    for dir in dir_relpaths.iter().map(AsRef::as_ref) {
        if dir.starts_with('/') || dir == INTERNAL_ROOT {
            continue;
        }
        if let Some(anchor) = classify_path(dir, cargo_roots, member_roots) {
            out.insert((anchor.path.clone(), anchor.reason.as_str()), anchor);
        }
    }
    out.into_values().collect()
}

/// Whether a pruned-tree count is over the supplied inventory.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum MarkerCountBasis {
    NotEnumerated,
    ObservedInventory,
}
impl MarkerCountBasis {
    pub(crate) fn as_str(self) -> &'static str {
        match self {
            Self::NotEnumerated => "not-enumerated",
            Self::ObservedInventory => "observed-inventory",
        }
    }
}

/// A pruned-tree row: `markerCount` is `None` exactly when not enumerated.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct PrunedTreeRow {
    pub(crate) anchor: PrunedAnchor,
    pub(crate) marker_count: Option<u64>,
    pub(crate) basis: MarkerCountBasis,
}

/// More than 4096 first-party units: no unit is returned (no truncation).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) struct WorkspaceUnitLimit {
    pub(crate) unit_count: usize,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct UnitEnumeration {
    pub(crate) unit_dirs: Vec<String>,
    pub(crate) pruned_trees: Vec<PrunedTreeRow>,
    pub(crate) refusal: Option<WorkspaceUnitLimit>,
}

/// What `enumerate_units` is told about its inventory.
pub(crate) struct EnumerationInput<'a, S: AsRef<str>> {
    pub(crate) enforce_limit: bool,
    /// The admitted directory observation, or `None` for the algorithm lane.
    pub(crate) observed_directories: Option<&'a [S]>,
    pub(crate) basis: MarkerCountBasis,
    pub(crate) unreadable_anchors: &'a [S],
    pub(crate) member_roots: &'a BTreeSet<String>,
}

/// Zero-config units: the directories holding a marker outside every pruned
/// tree. Paths that are absolute or not markers are ignored.
pub(crate) fn enumerate_units<S: AsRef<str>>(
    marker_relpaths: &[S],
    input: &EnumerationInput<'_, S>,
) -> UnitEnumeration {
    let markers: BTreeSet<&str> = marker_relpaths
        .iter()
        .map(AsRef::as_ref)
        .filter(|path| !path.starts_with('/') && WORKSPACE_MARKERS.contains(&file_name(path)))
        .collect();
    let markers: Vec<&str> = markers.into_iter().collect();
    let cargo_roots = cargo_roots_from_markers(&markers, input.member_roots);
    let mut pruned: BTreeMap<(String, &'static str), (PrunedAnchor, u64)> = BTreeMap::new();
    let mut unit_dirs = BTreeSet::new();
    for marker in &markers {
        match classify_path(marker, &cargo_roots, input.member_roots) {
            Some(anchor) => {
                let key = (anchor.path.clone(), anchor.reason.as_str());
                pruned.entry(key).or_insert((anchor, 0)).1 += 1;
            }
            None => {
                unit_dirs.insert(dir_of(marker).to_owned());
            }
        }
    }
    if let Some(observed) = input.observed_directories {
        for anchor in pruned_anchors_from_directories(observed, &cargo_roots, input.member_roots) {
            let key = (anchor.path.clone(), anchor.reason.as_str());
            pruned.entry(key).or_insert((anchor, 0));
        }
    }
    let unreadable: BTreeSet<&str> = input.unreadable_anchors.iter().map(AsRef::as_ref).collect();
    let pruned_trees = pruned
        .into_values()
        .map(|(anchor, count)| {
            if unreadable.contains(anchor.path.as_str())
                || input.basis == MarkerCountBasis::NotEnumerated
            {
                PrunedTreeRow {
                    anchor,
                    marker_count: None,
                    basis: MarkerCountBasis::NotEnumerated,
                }
            } else {
                PrunedTreeRow {
                    anchor,
                    marker_count: Some(count),
                    basis: MarkerCountBasis::ObservedInventory,
                }
            }
        })
        .collect();
    if input.enforce_limit && unit_dirs.len() > MAX_WORKSPACE_UNITS {
        return UnitEnumeration {
            unit_dirs: Vec::new(),
            pruned_trees,
            refusal: Some(WorkspaceUnitLimit {
                unit_count: unit_dirs.len(),
            }),
        };
    }
    UnitEnumeration {
        unit_dirs: unit_dirs.into_iter().collect(),
        pruned_trees,
        refusal: None,
    }
}

/// A custody locator that cannot become a relative scope path.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum LocatorRefusal {
    OutsideRoot,
    Grammar,
}

/// An absolute custody locator at or below the selected root, in internal
/// relative form (`""` for the root itself).
pub(crate) fn relative_locator(
    selected_root: &str,
    absolute: &str,
) -> Result<String, LocatorRefusal> {
    if selected_root.is_empty() {
        return Err(LocatorRefusal::OutsideRoot);
    }
    if absolute == selected_root {
        return Ok(INTERNAL_ROOT.to_owned());
    }
    let base = format!("{}/", selected_root.trim_end_matches('/'));
    let Some(rel) = absolute.strip_prefix(&base) else {
        return Err(LocatorRefusal::OutsideRoot);
    };
    if rel.is_empty()
        || rel.contains('\\')
        || rel.contains('\0')
        || rel
            .split('/')
            .any(|segment| matches!(segment, "" | "." | ".."))
    {
        return Err(LocatorRefusal::Grammar);
    }
    Ok(rel.to_owned())
}

fn at_or_below(path: &str, anchor: &str) -> bool {
    path == anchor
        || path
            .strip_prefix(anchor.trim_end_matches('/'))
            .is_some_and(|rest| rest.starts_with('/'))
}

/// Why a path is outside this project's authority.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum BoundaryReason {
    NestedRepository,
    NestedProject,
}
impl BoundaryReason {
    pub(crate) fn as_str(self) -> &'static str {
        match self {
            Self::NestedRepository => "nested-repository",
            Self::NestedProject => "nested-project",
        }
    }
}

/// The nested boundary `path` lies at or below. Repositories are tested
/// first: a nested project inside a nested repository belongs to it.
pub(crate) fn classify_boundary<'a, S: AsRef<str>>(
    path: &str,
    nested_repositories: &'a [S],
    nested_projects: &'a [S],
) -> Option<(&'a str, BoundaryReason)> {
    let first = |anchors: &'a [S], reason| {
        anchors
            .iter()
            .map(AsRef::as_ref)
            .find(|anchor| at_or_below(path, anchor))
            .map(|anchor| (anchor, reason))
    };
    first(nested_repositories, BoundaryReason::NestedRepository)
        .or_else(|| first(nested_projects, BoundaryReason::NestedProject))
}

/// A security `excludedUnits` row the native instrument consumes.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct CustodyExcludedUnit {
    pub(crate) path: String,
    pub(crate) reason: String,
}

/// The custody exclusion covering `unit_dir`: a directory custody or depth
/// row at or above it, or a `MARKER_CUSTODY:<marker>` row for exactly this
/// directory and marker.
pub(crate) fn classify_custody_exclusion<'a>(
    unit_dir: &str,
    marker_name: Option<&str>,
    custody_excluded: &'a [CustodyExcludedUnit],
) -> Option<&'a str> {
    custody_excluded.iter().find_map(|row| {
        let covered = match row.reason.strip_prefix(MARKER_CUSTODY_PREFIX) {
            Some(detail) => {
                row.path == unit_dir
                    && marker_name.is_some_and(|m| detail.split(':').next() == Some(m))
            }
            None => at_or_below(unit_dir, &row.path),
        };
        covered.then_some(row.path.as_str())
    })
}

/// The anchors a scope descriptor lists for the admitted boundaries: every
/// nested repository and project, and every directory-custody exclusion
/// except the root. D15 members are not boundaries and add none (NE:940).
pub(crate) fn boundary_excluded_prefixes<S: AsRef<str>>(
    nested_repositories: &[S],
    nested_projects: &[S],
    custody_excluded: &[CustodyExcludedUnit],
) -> Vec<String> {
    let mut out: BTreeSet<String> = nested_repositories
        .iter()
        .chain(nested_projects)
        .map(|p| p.as_ref().to_owned())
        .collect();
    for row in custody_excluded {
        if !row.reason.starts_with(MARKER_CUSTODY_PREFIX) && row.path != INTERNAL_ROOT {
            out.insert(row.path.clone());
        }
    }
    out.into_iter().collect()
}

fn under(root: &str, segment: &str) -> String {
    if root.is_empty() {
        segment.to_owned()
    } else {
        format!("{root}/{segment}")
    }
}

/// The conventional prefixes: `.git` and `node_modules` under every unit
/// root, `target` under every Cargo root only, and `.opensip` at the root and
/// at each member root, always (B-S1 LD-3).
pub(crate) fn conventional_excluded_prefixes<S: AsRef<str>>(
    unit_roots: &[S],
    cargo_roots: &BTreeSet<String>,
    member_roots: &BTreeSet<String>,
) -> Vec<String> {
    let mut out = BTreeSet::new();
    for root in unit_roots.iter().map(AsRef::as_ref) {
        out.insert(under(root, DEPENDENCY_TREE_SEGMENT));
        out.insert(under(root, ".git"));
    }
    for root in cargo_roots {
        out.insert(under(root, CARGO_BUILD_OUTPUT_SEGMENT));
    }
    for root in std::iter::once(INTERNAL_ROOT).chain(member_roots.iter().map(String::as_str)) {
        out.insert(under(root, OPENSIP_CUSTODY_STATE));
    }
    out.into_iter().collect()
}

/// What a directory entry is, as its parent's listing reports it.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum EntryKind {
    Directory,
    File,
    Symlink,
    Other,
}

/// The walker's decision for one entry of a listed parent, made before any
/// open (SL:195): an entry in a pruned tree is never entered, never source
/// and never inventoried, whatever its kind; only an observed anchor
/// directory is recorded as a pruned-tree row.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) enum EntryDisposition {
    NeverEnter {
        anchor: PrunedAnchor,
        recorded: bool,
    },
    Ordinary,
}

pub(crate) fn classify_entry(
    relpath: &str,
    kind: EntryKind,
    cargo_roots: &BTreeSet<String>,
    member_roots: &BTreeSet<String>,
) -> EntryDisposition {
    match classify_path(relpath, cargo_roots, member_roots) {
        Some(anchor) => EntryDisposition::NeverEnter {
            recorded: kind == EntryKind::Directory && anchor.path == relpath,
            anchor,
        },
        None => EntryDisposition::Ordinary,
    }
}

/// Why the read set does not read a path below an authorized package
/// directory (M3-C r8 item 3; C1c plan r4, LD-C1C-5).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum ReadSetExclusion {
    /// A further exact `node_modules` segment below the authorized
    /// directory: a nested installed package, which needs its own row.
    NestedPackage,
    /// A VCS segment anywhere on the full path.
    VcsTree,
    /// A `target` directly under a Cargo root, first-party or in a
    /// dependency tree.
    CargoBuildOutput,
    /// The exact `.opensip` anchor at the root or an admitted member root.
    OpensipCustodyState,
}

impl ReadSetExclusion {
    pub(crate) fn as_str(self) -> &'static str {
        match self {
            Self::NestedPackage => "nested-package",
            Self::VcsTree => "vcs-tree",
            Self::CargoBuildOutput => "cargo-build-output",
            Self::OpensipCustodyState => "opensip-custody-state",
        }
    }
}

/// The read set's authorization of one path (unit C1c-0).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum ReadSetPath {
    Admitted,
    Excluded(ReadSetExclusion),
    /// The authorized directory lies in no dependency tree: no layout row
    /// can authorize a read there.
    Forbidden,
}

/// Read authorization below an authorized package directory (M3-C r8 item
/// 3; C1c plan r4, LD-C1C-5). `classify_path` answers which outermost
/// pruned tree holds a path, and discovery keeps that answer; this answers
/// whether the read set may read `relative` (`""` for the directory itself)
/// below `authorized`, a layout row's `realPath`. The check runs over the
/// full path, `authorized` then `relative`, never over `relative` alone:
/// - `authorized` must hold an exact `node_modules` segment;
/// - a VCS segment anywhere excludes;
/// - the exact `.opensip` anchor at the root or an admitted member root
///   excludes (`custody_state`); a `.opensip` anywhere else stays eligible;
/// - a further exact `node_modules` segment below `authorized` excludes;
/// - a `target` segment excludes when the directory before it is a Cargo
///   root: a first-party root (`first_party_cargo_roots`, the walk's own
///   derivation) or a dependency-tree root (`dependency_cargo_roots`,
///   observed by the read set). A `target` with no Cargo parent stays
///   eligible.
///
/// Its temporaries are one segment list and, per `target` segment, the
/// Cargo-root prefix it is tested as, and at most one custody anchor.
pub(crate) fn read_set_path(
    authorized: &str,
    relative: &str,
    first_party_cargo_roots: &BTreeSet<String>,
    dependency_cargo_roots: &BTreeSet<String>,
    member_roots: &BTreeSet<String>,
) -> ReadSetPath {
    let base = authorized.split('/').count();
    let below = if relative.is_empty() {
        0
    } else {
        relative.split('/').count()
    };
    let mut parts: Vec<&str> = Vec::with_capacity(base + below);
    parts.extend(authorized.split('/'));
    if !parts.contains(&DEPENDENCY_TREE_SEGMENT) {
        return ReadSetPath::Forbidden;
    }
    if below > 0 {
        parts.extend(relative.split('/'));
    }
    if parts
        .iter()
        .any(|segment| VCS_TREE_SEGMENTS.contains(segment))
    {
        return ReadSetPath::Excluded(ReadSetExclusion::VcsTree);
    }
    if custody_state(&parts, member_roots).is_some() {
        return ReadSetPath::Excluded(ReadSetExclusion::OpensipCustodyState);
    }
    if parts[base..].contains(&DEPENDENCY_TREE_SEGMENT) {
        return ReadSetPath::Excluded(ReadSetExclusion::NestedPackage);
    }
    for index in 0..parts.len() {
        if parts[index] == CARGO_BUILD_OUTPUT_SEGMENT {
            let prefix = parts[..index].join("/");
            if first_party_cargo_roots.contains(&prefix) || dependency_cargo_roots.contains(&prefix)
            {
                return ReadSetPath::Excluded(ReadSetExclusion::CargoBuildOutput);
            }
        }
    }
    ReadSetPath::Admitted
}

/// Whether a directory the read set holds is a dependency-tree Cargo root:
/// it lies in a dependency tree and holds a regular `Cargo.toml`. The read
/// set derives these parent first, as it reaches and descends (C1c plan r4,
/// LD-C1C-13), and never takes `cargo_roots_from_markers`'s first-party
/// skip of markers inside pruned trees.
pub(crate) fn is_dependency_cargo_root(dir: &str, holds_regular_marker: bool) -> bool {
    holds_regular_marker && dir.split('/').any(|s| s == DEPENDENCY_TREE_SEGMENT)
}

/// Where a pruned-tree capture's path stands (C1c plan r4, LD-C1C-2): the
/// index of its outermost dependency segment, before the leaf, when no VCS
/// segment and no custody anchor lies on it.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum PrunedCapture {
    Anchor(usize),
    /// No `node_modules` segment before the leaf: a first-party path, which
    /// `SnapshotRoot::open` captures.
    Outside,
    Excluded(ReadSetExclusion),
}
pub(crate) fn pruned_capture(path: &str, member_roots: &BTreeSet<String>) -> PrunedCapture {
    let parts: Vec<&str> = path.split('/').collect();
    let Some(anchor) = parts[..parts.len().saturating_sub(1)]
        .iter()
        .position(|s| *s == DEPENDENCY_TREE_SEGMENT)
    else {
        return PrunedCapture::Outside;
    };
    if parts
        .iter()
        .any(|segment| VCS_TREE_SEGMENTS.contains(segment))
    {
        return PrunedCapture::Excluded(ReadSetExclusion::VcsTree);
    }
    if custody_state(&parts, member_roots).is_some() {
        return PrunedCapture::Excluded(ReadSetExclusion::OpensipCustodyState);
    }
    PrunedCapture::Anchor(anchor)
}

#[cfg(test)]
mod tests {
    include!("discovery_rule_tests.rs");
}
