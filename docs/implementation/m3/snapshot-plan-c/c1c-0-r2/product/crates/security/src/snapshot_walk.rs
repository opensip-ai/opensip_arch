// M3-C r8 item 2 (unit C1a1, C1a plan r4 sections 1 and 2): the snapshot's
// extent walk. It descends from the snapshot root holding each directory's
// retained descriptor, lists each directory once (the discovery walk's
// listing conversion and pricing, unchanged), observes every child with
// `fstatat(AT_SYMLINK_NOFOLLOW)` relative to its enumerating parent, and
// opens each entry `O_NOFOLLOW` relative to that same descriptor, comparing
// it with the listing-time observation (RF-2 of the plan's round 2). The
// exact `.opensip/` anchors at the root and each admitted D15 member are
// dropped from their listing first: never stat'ed, opened or listed (item 1).
//
// The extent is the shared discovery rule's (IE:548-551), never a copy: the
// rule's pruned trees (with `.opensip/` at the root and each admitted D15
// member, SX-1), B2's admitted boundaries (nested repositories and projects,
// custody and depth exclusions, whatever their entries now are, and a
// marker-custody row's own marker), and Config2 `ignorePaths`. The root and
// every directory entered pass S3 directory custody
// and every marker config-file custody; a failure refuses, never skips.
// Symlinks and special files are counted and named in the walk report, never
// opened. Every regular file in the extent is handed, open, to the visitor:
// `crates/host/src/snapshot.rs` reads it (C1-T2). Charged to the snapshot
// ledger before every step; nothing is retried, created or written.
use crate::custody::discovery_rule::{self as rule};
use crate::custody::discovery_walk::{
    LISTING, ListingConversion, MAX_LISTED_ENTRIES, MAX_LISTED_NAME_BYTES, WalkRefusal, owned,
};
use crate::custody::project_chain::ProjectObject;
use crate::discovery_export::AdmittedBoundaries;
use crate::snapshot_source::{
    SnapshotCustody, SnapshotFailure, SnapshotRefusal, SnapshotRoot, SourceFile, is_marker_name,
    judge_opened, judge_root, key_cost, last_segment, open_directory, open_regular, refuse,
    source_file,
};
use opensip_platform::{
    ChildKind, ChildObservation, RetainedDirectory, WorkCost, WorkFailure, WorkScope,
};
use std::collections::BTreeSet;
use std::ffi::OsStr;

/// The record overhead the discovery walk prices every owned record with
/// (`discovery_walk.rs`, `RECORD`): mirrored here for the classification
/// temporaries.
const RECORD: usize = 128;

/// The shared rule's `classify_path` temporaries for `rel`, counted from its
/// source (`discovery_rule.rs`) rather than taken from the discovery walk's
/// `classify_cost` (unit C1a1 r2, Codex C1A1-R1-RF-4): the segment list; for
/// each `target` segment, the Cargo-root prefix it is tested as; and up to
/// three anchors (a dependency or VCS segment, a Cargo build output and the
/// custody state, each at most `rel`). The D15 member roots cost nothing:
/// `custody_state` compares them in place (M3-C r9 item 2, remedy
/// (b-prime); unit C1a4).
fn classify_cost(rel: &str) -> WorkCost {
    let segments = rel.split('/').count();
    let targets = rel.split('/').filter(|part| *part == "target").count();
    let objects = 4 + targets;
    WorkCost {
        objects,
        edges: 0,
        bytes: segments
            .saturating_mul(2 * std::mem::size_of::<usize>())
            .saturating_add(rel.len().saturating_mul(3 + targets))
            .saturating_add(objects.saturating_mul(RECORD)),
    }
}

/// What the walk excludes beyond the shared rule's pruned trees: B2's
/// admitted boundaries, the admitted D15 member roots (for `.opensip/` and
/// the `target` rule) and the resolved Config2 `ignorePaths`.
pub struct SnapshotExtent<'a> {
    boundaries: &'a AdmittedBoundaries,
    member_roots: &'a BTreeSet<String>,
    ignore_paths: &'a [String],
}
/// An `ignorePaths` entry that is not a logical path.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct IgnorePathInvalid(pub String);
impl<'a> SnapshotExtent<'a> {
    /// From B2's accepted outputs. The boundaries are an admitted
    /// `AdmittedBoundaryInventoryV3`, so no ignore list can stand in for them.
    /// Each `ignorePaths` entry is validated by the shared grammar, its
    /// validator's copy charged to `work` before it is made (unit C1a1 r3).
    pub fn new(
        boundaries: &'a AdmittedBoundaries,
        member_roots: &'a BTreeSet<String>,
        ignore_paths: &'a [String],
        work: &mut WorkScope<'_>,
    ) -> Result<Self, WorkFailure<IgnorePathInvalid>> {
        for path in ignore_paths {
            work.charge::<IgnorePathInvalid>(owned(path.len()))?;
            if opensip_identity::LogicalPath::parse(path).is_err() {
                return Err(WorkFailure::Operation(IgnorePathInvalid(path.clone())));
            }
        }
        Ok(Self {
            boundaries,
            member_roots,
            ignore_paths,
        })
    }
    /// The admitted D15 member roots (the pruned-tree opener's custody
    /// anchors; unit C1c-0).
    pub(crate) fn member_roots(&self) -> &BTreeSet<String> {
        self.member_roots
    }
    fn ignored(&self, rel: &str) -> bool {
        self.ignore_paths.iter().any(|p| {
            rel == p
                || (rel.len() > p.len()
                    && rel.starts_with(p.as_str())
                    && rel.as_bytes()[p.len()] == b'/')
        })
    }
}

/// The operational walk report (item 2): symlinks and special files are
/// counted and named (paths at P2 under S-OP-2), never opened or
/// inventoried. Outside identity.
#[derive(Debug, Default, Clone, PartialEq, Eq)]
pub struct SnapshotWalkReport {
    pub symlinks: Vec<String>,
    pub special: Vec<String>,
    pub directories: u64,
    pub files: u64,
    /// The root listing's `opensip.json`, as the walk saw it (unit C1a3;
    /// M3-C r8 item 1 rule 2, the project carrier's join).
    pub carrier: CarrierEntry,
}

/// The project carrier's path, at the root.
pub const PROJECT_CARRIER: &str = "opensip.json";

/// The root listing's `opensip.json` entry, as the walk classified it.
#[derive(Debug, Default, Clone, Copy, PartialEq, Eq)]
pub enum CarrierEntry {
    /// No entry of that name in the root's listing.
    #[default]
    Absent,
    /// A regular file, handed to the visitor (an inventory row).
    Regular,
    Directory,
    Symlink,
    Special,
    /// Excluded from the extent (by `ignorePaths`, a pruned tree or a
    /// boundary) before it was opened.
    Excluded,
}

/// What the walk derived that the read set needs (M3-C r8 item 3; unit
/// C1c-0, C1c plan r4 LD-C1C-13), retained by the host's capture session so
/// the read set uses the same session's own walk over the same root:
/// - the first-party Cargo roots the walk derived, by the shared rule. The
///   walk already charges each root's key once, as an owned record, when it
///   is derived (`key_cost`), and now keeps it rather than dropping it at
///   its frame's exit: a move, never a copy, and no new charge. A kept root
///   that is not an ancestor of a later path changes no classification:
///   `classify_path` tests only that path's own prefixes;
/// - the admitted D15 member roots, copied from the extent's borrow, each
///   copy charged first (`owned(len)`).
///
/// Its fields are private and it has no public constructor: only the walk
/// makes one.
#[derive(Debug)]
pub struct WalkEvidence {
    cargo_roots: BTreeSet<String>,
    member_roots: BTreeSet<String>,
}
impl WalkEvidence {
    pub(crate) fn cargo_roots(&self) -> &BTreeSet<String> {
        &self.cargo_roots
    }
    pub(crate) fn member_roots(&self) -> &BTreeSet<String> {
        &self.member_roots
    }
}

/// Why a walk stopped: the walk's own refusal, or the visitor's.
#[derive(Debug)]
pub enum SnapshotStop<E> {
    Refused(SnapshotRefusal),
    Visitor(E),
}
pub type SnapshotWalkFailure<E> = WorkFailure<SnapshotStop<E>>;

fn lift<E>(failure: SnapshotFailure) -> SnapshotWalkFailure<E> {
    match failure {
        WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
        WorkFailure::Operation(refusal) => WorkFailure::Operation(SnapshotStop::Refused(refusal)),
    }
}
fn from_listing<E>(failure: WorkFailure<WalkRefusal>) -> SnapshotWalkFailure<E> {
    match failure {
        WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
        WorkFailure::Operation(refusal) => {
            WorkFailure::Operation(SnapshotStop::Refused(match refusal {
                WalkRefusal::NameUnrepresentable { parent, name } => {
                    SnapshotRefusal::Name { parent, name }
                }
                WalkRefusal::ListingBound => SnapshotRefusal::ListingBound,
                WalkRefusal::HostIo(error) => SnapshotRefusal::HostIo(error),
                other => SnapshotRefusal::HostIo(std::io::Error::other(format!("{other:?}"))),
            }))
        }
    }
}

/// One directory on the current path: its retained descriptor (the root's
/// is lent), its listed children (less the exact
/// `.opensip/` anchors, never observed) with their listing-time
/// observations, the next child, and the anchor question's classification
/// of a listed `.opensip` that is not an anchor (its index and whether a
/// pruned tree holds it).
struct Level {
    dir: Option<RetainedDirectory>,
    paths: Vec<String>,
    observed: Vec<ChildObservation>,
    next: usize,
    opensip: Option<(usize, bool)>,
}

/// The extent walk (item 2). Each regular file in the extent is handed to
/// `visit` open, compared with its listing-time observation through its
/// enumerating parent, with the walk's own ledger scope, so the host's read
/// is charged to the same snapshot ledger (unit C1a2).
///
/// Every heap copy the walk itself makes is charged before it is made (unit
/// C1a1 r2, Codex C1A1-R1-RF-4): a frame's slot (`owned(0)`), its children's
/// observation slots, a Cargo root's key, a reported link's or special
/// file's slot, and the shared rule's classification temporaries
/// (`classify_cost`). A child's path moves out of its frame, never copied;
/// its parent and name are borrowed views of it; boundary lookups borrow
/// (`AdmittedBoundaries::boundary_anchor`); and the root's spelling is built
/// only for a terminal name refusal. The listing conversion, observations,
/// opens, status samples and ACL captures are charged by their owners at the
/// discovery walk's prices.
pub fn walk_snapshot<E>(
    root: &SnapshotRoot<'_>,
    custody: SnapshotCustody<'_>,
    extent: &SnapshotExtent<'_>,
    visit: &mut dyn FnMut(SourceFile, &mut WorkScope<'_>) -> Result<(), E>,
    work: &mut WorkScope<'_>,
) -> Result<SnapshotWalkReport, SnapshotWalkFailure<E>> {
    walk_snapshot_retaining(root, custody, extent, visit, work).map(|(report, _)| report)
}

/// [`walk_snapshot`], also returning its [`WalkEvidence`] (unit C1c-0): the
/// one walk, with the same charges, which the host's capture session keeps.
pub fn walk_snapshot_retaining<E>(
    root: &SnapshotRoot<'_>,
    custody: SnapshotCustody<'_>,
    extent: &SnapshotExtent<'_>,
    visit: &mut dyn FnMut(SourceFile, &mut WorkScope<'_>) -> Result<(), E>,
    work: &mut WorkScope<'_>,
) -> Result<(SnapshotWalkReport, WalkEvidence), SnapshotWalkFailure<E>> {
    let lent = root.retained();
    let mut report = SnapshotWalkReport::default();
    // The root: its own sample, then S3 directory custody.
    judge_root(root, custody, work).map_err(lift)?;
    let mut known: BTreeSet<String> = BTreeSet::new();
    let mut levels: Vec<Level> = Vec::new();
    // The root frame's own slot.
    work.charge::<SnapshotStop<E>>(owned(0))?;
    let first = enter(root, None, String::new(), extent, &mut known, work)?;
    levels.push(first);
    report.directories += 1;
    while let Some(top) = levels.last_mut() {
        if top.next == top.paths.len() {
            // A finished frame's Cargo root stays known: the read set's
            // evidence (unit C1c-0), and no later path's prefix.
            drop(levels.pop());
            continue;
        }
        let index = top.next;
        top.next += 1;
        let recorded = top.opensip.filter(|(at, _)| *at == index);
        // Each child is visited once: its path and observation move out of
        // the frame, never copied.
        let rel = std::mem::take(&mut top.paths[index]);
        let observation = std::mem::replace(&mut top.observed[index], ChildObservation::Absent);
        let ChildObservation::Present { kind, metadata } = &observation else {
            return Err(lift(
                refuse::<()>(SnapshotRefusal::Changed(rel)).unwrap_err(),
            ));
        };
        let (kind, metadata) = (*kind, metadata.clone());
        // The shared rule's pruned trees, before any open; then
        // `ignorePaths`; then an admitted boundary, which excludes
        // everything at or below it, whatever its entry is now (Codex
        // C1A1-R1-RF-2): a boundary replaced by a file, a link or a special
        // file is neither handed nor reported. A `.opensip` the anchor
        // question already classified is not classified again (M3-C r9 item
        // 2, remedy (a); unit C1a4): `known` has since gained only this
        // directory's own Cargo root and roots kept from finished sibling
        // subtrees (unit C1c-0), none of which a prefix of that path can be.
        let pruned = match recorded {
            Some((_, pruned)) => pruned,
            None => {
                work.charge::<SnapshotStop<E>>(classify_cost(&rel))?;
                rule::classify_path(&rel, &known, extent.member_roots).is_some()
            }
        };
        let excluded = pruned || extent.ignored(&rel) || extent.boundaries.is_boundary(&rel);
        // The root's carrier is classified as the walk saw it (C1a3).
        if rel == PROJECT_CARRIER {
            report.carrier = match (excluded, kind) {
                (true, _) => CarrierEntry::Excluded,
                (false, ChildKind::File) => CarrierEntry::Regular,
                (false, ChildKind::Directory) => CarrierEntry::Directory,
                (false, ChildKind::Symlink) => CarrierEntry::Symlink,
                (false, ChildKind::Other) => CarrierEntry::Special,
            };
        }
        if excluded {
            continue;
        }
        let parent_dir = levels
            .last()
            .expect("the stack has a top level")
            .dir
            .as_ref()
            .unwrap_or(lent);
        match kind {
            ChildKind::Directory => {
                let name = last_segment(&rel);
                let (child, sample) =
                    open_directory(parent_dir, name, &rel, &observation, work).map_err(lift)?;
                if let Err(reason) = judge_opened(
                    root.lent(),
                    custody,
                    child.as_file(),
                    &sample,
                    &rel,
                    ProjectObject::Directory,
                    work,
                )
                .map_err(lift)?
                {
                    return Err(lift(
                        refuse::<()>(SnapshotRefusal::Custody { path: rel, reason }).unwrap_err(),
                    ));
                }
                // The frame's own slot; its path moved in.
                work.charge::<SnapshotStop<E>>(owned(0))?;
                let level = enter(root, Some(child), rel, extent, &mut known, work)?;
                levels.push(level);
                report.directories += 1;
            }
            ChildKind::File => {
                let (parent_rel, name) = rel.rsplit_once('/').unwrap_or(("", rel.as_str()));
                let marker = is_marker_name(name);
                // A marker-custody row excludes exactly its marker file.
                if marker
                    && extent
                        .boundaries
                        .boundary_anchor(parent_rel, Some(name))
                        .is_some_and(|(anchor, _)| anchor == parent_rel)
                {
                    continue;
                }
                let file = open_regular(parent_dir, name, &rel, &metadata, work).map_err(lift)?;
                if marker
                    && let Err(reason) = judge_opened(
                        root.lent(),
                        custody,
                        &file,
                        &metadata,
                        &rel,
                        ProjectObject::ConfigurationFile,
                        work,
                    )
                    .map_err(lift)?
                {
                    return Err(lift(
                        refuse::<()>(SnapshotRefusal::MarkerCustody { path: rel, reason })
                            .unwrap_err(),
                    ));
                }
                report.files += 1;
                visit(source_file(rel, file, metadata, marker), work)
                    .map_err(|e| WorkFailure::Operation(SnapshotStop::Visitor(e)))?;
            }
            ChildKind::Symlink => {
                work.charge::<SnapshotStop<E>>(owned(rel.len()))?;
                report.symlinks.push(rel);
            }
            ChildKind::Other => {
                work.charge::<SnapshotStop<E>>(owned(rel.len()))?;
                report.special.push(rel);
            }
        }
    }
    // The admitted member roots, copied out of the extent's borrow, each
    // copy charged first (unit C1c-0); the Cargo roots move.
    let mut member_roots = BTreeSet::new();
    for member in extent.member_roots {
        work.charge::<SnapshotStop<E>>(owned(member.len()))?;
        member_roots.insert(member.clone());
    }
    Ok((
        report,
        WalkEvidence {
            cargo_roots: known,
            member_roots,
        },
    ))
}

/// A listed name, as the anchor question sees it.
enum OpensipName {
    /// Not `.opensip`: not asked, and not classified.
    Other,
    /// Exactly an OpenSIP custody-state anchor (the shared rule's `.opensip/`
    /// at the root or an admitted D15 member, SX-1).
    Anchor,
    /// A `.opensip` that is not an anchor, with whether a pruned tree holds
    /// it: the walk loop reuses this classification (M3-C r9 item 2, remedy
    /// (a); unit C1a4).
    Classified { pruned: bool },
}

/// The anchor question, asked only of a `.opensip` name and charged as one
/// classification.
fn opensip_name<E>(
    path: &str,
    known: &BTreeSet<String>,
    members: &BTreeSet<String>,
    work: &mut WorkScope<'_>,
) -> Result<OpensipName, SnapshotWalkFailure<E>> {
    if last_segment(path) != rule::OPENSIP_CUSTODY_STATE {
        return Ok(OpensipName::Other);
    }
    work.charge::<SnapshotStop<E>>(classify_cost(path))?;
    Ok(match rule::classify_path(path, known, members) {
        Some(anchor) if anchor.reason == rule::PruneReason::OpensipCustodyState => {
            OpensipName::Anchor
        }
        hit => OpensipName::Classified {
            pruned: hit.is_some(),
        },
    })
}

/// List one directory and observe its children through it (the listing
/// conversion is the discovery walk's, so names refuse exactly as there).
/// An exact `.opensip/` anchor is dropped from the listing before any child
/// is observed, so the walk never stats, opens or lists it (M3-C r8 item 1;
/// Codex C1A1-R1-RF-1).
fn enter<E>(
    root: &SnapshotRoot<'_>,
    dir: Option<RetainedDirectory>,
    rel: String,
    extent: &SnapshotExtent<'_>,
    known: &mut BTreeSet<String>,
    work: &mut WorkScope<'_>,
) -> Result<Level, SnapshotWalkFailure<E>> {
    let held = dir.as_ref().unwrap_or(root.retained());
    work.charge::<SnapshotStop<E>>(LISTING)?;
    let mut conversion = ListingConversion::new();
    let visited = held.visit_entry_names(MAX_LISTED_ENTRIES, MAX_LISTED_NAME_BYTES, |name| {
        conversion.accept(&rel, name, work)
    });
    let mut paths = conversion
        .finish(visited, || {
            // A terminal refusal's detail only.
            let root_abs = root.lent().spelling().to_string_lossy();
            if rel.is_empty() {
                root_abs.into_owned()
            } else {
                format!("{root_abs}/{rel}")
            }
        })
        .map_err(from_listing)?;
    // A listing holds at most one `.opensip`; its removal moves, never copies.
    // Kept, it keeps its index and its classification.
    let (mut anchor, mut opensip) = (None, None);
    for (index, path) in paths.iter().enumerate() {
        match opensip_name(path, known, extent.member_roots, work)? {
            OpensipName::Other => {}
            OpensipName::Anchor => anchor = Some(index),
            OpensipName::Classified { pruned } => opensip = Some((index, pruned)),
        }
    }
    if let Some(index) = anchor {
        drop(paths.remove(index));
    }
    work.charge::<SnapshotStop<E>>(owned(
        paths
            .len()
            .saturating_mul(std::mem::size_of::<ChildObservation>()),
    ))?;
    let mut observed = Vec::with_capacity(paths.len());
    for path in &paths {
        #[cfg(test)]
        before_observe(path);
        let observation = held
            .observe_child_accounted(OsStr::new(last_segment(path)), work)
            .map_err(|failure| match failure {
                WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
                WorkFailure::Operation(error) => {
                    WorkFailure::Operation(SnapshotStop::Refused(SnapshotRefusal::HostIo(error)))
                }
            })?;
        if observation == ChildObservation::Absent {
            return Err(lift(
                refuse::<()>(SnapshotRefusal::Changed(path.clone())).unwrap_err(),
            ));
        }
        observed.push(observation);
    }
    let regular_cargo = paths.iter().zip(&observed).any(|(p, o)| {
        last_segment(p) == "Cargo.toml"
            && matches!(
                o,
                ChildObservation::Present {
                    kind: ChildKind::File,
                    ..
                }
            )
    });
    if regular_cargo && !known.contains(&rel) {
        work.charge::<SnapshotStop<E>>(key_cost(&rel, ""))?;
        known.insert(rel.clone());
    }
    Ok(Level {
        dir,
        paths,
        observed,
        next: 0,
        opensip,
    })
}

// Unit tests only: a hook run just before each child observation, for the
// controls that the exact `.opensip/` anchors are never observed (Codex
// C1A1-R1-RF-1).
#[cfg(test)]
pub(crate) type ObserveHook = Option<Box<dyn FnMut(&str)>>;
#[cfg(test)]
thread_local! {
    static BEFORE_OBSERVE: std::cell::RefCell<ObserveHook> =
        const { std::cell::RefCell::new(None) };
}
#[cfg(test)]
pub(crate) fn set_before_observe(hook: ObserveHook) {
    BEFORE_OBSERVE.with_borrow_mut(|h| *h = hook);
}
#[cfg(test)]
fn before_observe(rel: &str) {
    BEFORE_OBSERVE.with_borrow_mut(|h| {
        if let Some(h) = h {
            h(rel);
        }
    });
}

#[cfg(test)]
#[path = "snapshot_walk_tests.rs"]
mod tests;
