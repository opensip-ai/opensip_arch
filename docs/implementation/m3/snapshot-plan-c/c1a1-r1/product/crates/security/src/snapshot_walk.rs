// M3-C r8 item 2 (unit C1a1, C1a plan r4 sections 1 and 2): the snapshot's
// extent walk. It descends from the snapshot root holding each directory's
// retained descriptor, lists each directory once (the discovery walk's
// listing conversion and pricing, unchanged), observes every child with
// `fstatat(AT_SYMLINK_NOFOLLOW)` relative to its enumerating parent, and
// opens each entry `O_NOFOLLOW` relative to that same descriptor, comparing
// it with the listing-time observation (RF-2 of the plan's round 2).
//
// The extent is the shared discovery rule's (IE:548-551), never a copy: the
// rule's pruned trees (with `.opensip/` at the root and each admitted D15
// member, SX-1), B2's admitted boundaries (nested repositories and projects,
// custody and depth exclusions, and a marker-custody row's own marker), and
// Config2 `ignorePaths`. Every directory entered passes S3 directory custody
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
    judge_opened, key_cost, last_segment, open_directory, open_regular, refuse, source_file,
};
use opensip_platform::{
    ChildKind, ChildObservation, RetainedDirectory, WorkCost, WorkFailure, WorkScope,
};
use std::collections::BTreeSet;
use std::ffi::OsStr;

/// The record overhead the discovery walk prices every owned record with
/// (`discovery_walk.rs`, `RECORD`): mirrored here for the classification
/// temporaries, whose form follows `classify_cost`.
const RECORD: usize = 128;

/// The shared rule's classification temporaries for `rel` (the form of the
/// discovery walk's `classify_cost`): its segment list, one prefix copy per
/// `target` segment, and the anchor's path.
fn classify_cost(rel: &str) -> WorkCost {
    let segments = rel.split('/').count();
    let targets = rel.split('/').filter(|part| *part == "target").count();
    WorkCost {
        objects: 2 + targets,
        edges: 0,
        bytes: segments
            .saturating_mul(2 * std::mem::size_of::<usize>())
            .saturating_add(rel.len().saturating_mul(1 + targets))
            .saturating_add((2 + targets).saturating_mul(RECORD)),
    }
}

/// What the walk excludes beyond the shared rule's pruned trees: B2's
/// admitted boundaries, the admitted D15 member roots (for `.opensip/` and
/// the `target` rule) and the resolved Config2 `ignorePaths`.
pub struct SnapshotExtent<'a> {
    boundaries: &'a AdmittedBoundaries,
    member_roots: &'a BTreeSet<String>,
    ignore_paths: Vec<String>,
}
/// An `ignorePaths` entry that is not a logical path.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct IgnorePathInvalid(pub String);
impl<'a> SnapshotExtent<'a> {
    /// From B2's accepted outputs. The boundaries are an admitted
    /// `AdmittedBoundaryInventoryV3`, so no ignore list can stand in for them.
    pub fn new(
        boundaries: &'a AdmittedBoundaries,
        member_roots: &'a BTreeSet<String>,
        ignore_paths: &[String],
    ) -> Result<Self, IgnorePathInvalid> {
        for path in ignore_paths {
            if opensip_identity::LogicalPath::parse(path).is_err() {
                return Err(IgnorePathInvalid(path.clone()));
            }
        }
        Ok(Self {
            boundaries,
            member_roots,
            ignore_paths: ignore_paths.to_vec(),
        })
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
/// is lent), its root-relative path, its listed children with their
/// listing-time observations, the next child, and whether it pushed a Cargo
/// root.
struct Level {
    dir: Option<RetainedDirectory>,
    rel: String,
    paths: Vec<String>,
    observed: Vec<ChildObservation>,
    next: usize,
    pushed_cargo: bool,
}

/// The extent walk (item 2). Each regular file in the extent is handed to
/// `visit` open, compared with its listing-time observation through its
/// enumerating parent.
pub fn walk_snapshot<E>(
    root: &SnapshotRoot<'_>,
    custody: SnapshotCustody<'_>,
    extent: &SnapshotExtent<'_>,
    visit: &mut dyn FnMut(SourceFile) -> Result<(), E>,
    work: &mut WorkScope<'_>,
) -> Result<SnapshotWalkReport, SnapshotWalkFailure<E>> {
    let lent = root.retained();
    let mut report = SnapshotWalkReport::default();
    let root_abs = root.lent().spelling().to_string_lossy().into_owned();
    // The root: its own sample, then S3 directory custody.
    let sample = work
        .run(crate::custody::discovery_walk::STATUS, |_| {
            opensip_platform::observe_descriptor_metadata(lent.as_file())
                .map_err(|error| WorkFailure::Operation(SnapshotRefusal::HostIo(error)))
        })
        .map_err(lift)?;
    if let Err(reason) = judge_opened(
        root.lent(),
        custody,
        lent.as_file(),
        &sample,
        "",
        ProjectObject::Directory,
        work,
    )
    .map_err(lift)?
    {
        return Err(lift(
            refuse::<()>(SnapshotRefusal::Custody {
                path: String::new(),
                reason,
            })
            .unwrap_err(),
        ));
    }
    let mut known: BTreeSet<String> = BTreeSet::new();
    let mut levels: Vec<Level> = Vec::new();
    let first = enter(lent, None, String::new(), &root_abs, &mut known, work)?;
    levels.push(first);
    report.directories += 1;
    while let Some(top) = levels.last_mut() {
        if top.next == top.paths.len() {
            let done = levels.pop().expect("the stack has a top level");
            if done.pushed_cargo {
                known.remove(&done.rel);
            }
            continue;
        }
        let index = top.next;
        top.next += 1;
        let rel = std::mem::take(&mut top.paths[index]);
        let observation = top.observed[index].clone();
        let parent_rel = top.rel.clone();
        let ChildObservation::Present { kind, metadata } = observation.clone() else {
            return Err(lift(
                refuse::<()>(SnapshotRefusal::Changed(rel)).unwrap_err(),
            ));
        };
        let name = last_segment(&rel).to_owned();
        // The shared rule's pruned trees, before any open.
        work.charge::<SnapshotStop<E>>(classify_cost(&rel))?;
        if rule::classify_path(&rel, &known, extent.member_roots).is_some() {
            continue;
        }
        if extent.ignored(&rel) {
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
                if extent.boundaries.is_boundary(&rel) {
                    continue;
                }
                let (child, sample) =
                    open_directory(parent_dir, &name, &rel, &observation, work).map_err(lift)?;
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
                let level = enter(lent, Some(child), rel, &root_abs, &mut known, work)?;
                levels.push(level);
                report.directories += 1;
            }
            ChildKind::File => {
                // A marker-custody row excludes exactly its marker file.
                if extent
                    .boundaries
                    .boundary_hit(&parent_rel, Some(&name))
                    .is_some_and(|(anchor, _)| anchor == parent_rel)
                    && is_marker_name(&name)
                {
                    continue;
                }
                let file = open_regular(parent_dir, &name, &rel, &metadata, work).map_err(lift)?;
                let marker = is_marker_name(&name);
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
                visit(source_file(rel, file, metadata, marker))
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
    Ok(report)
}

/// List one directory and observe its children through it (the listing
/// conversion is the discovery walk's, so names refuse exactly as there).
fn enter<E>(
    lent: &RetainedDirectory,
    dir: Option<RetainedDirectory>,
    rel: String,
    root_abs: &str,
    known: &mut BTreeSet<String>,
    work: &mut WorkScope<'_>,
) -> Result<Level, SnapshotWalkFailure<E>> {
    let held = dir.as_ref().unwrap_or(lent);
    work.charge::<SnapshotStop<E>>(LISTING)?;
    let mut conversion = ListingConversion::new();
    let visited = held.visit_entry_names(MAX_LISTED_ENTRIES, MAX_LISTED_NAME_BYTES, |name| {
        conversion.accept(&rel, name, work)
    });
    let paths = conversion
        .finish(visited, || {
            if rel.is_empty() {
                root_abs.to_owned()
            } else {
                format!("{root_abs}/{rel}")
            }
        })
        .map_err(from_listing)?;
    work.charge::<SnapshotStop<E>>(owned(
        paths
            .len()
            .saturating_mul(std::mem::size_of::<ChildObservation>()),
    ))?;
    let mut observed = Vec::with_capacity(paths.len());
    for path in &paths {
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
    let pushed_cargo = regular_cargo && !known.contains(&rel);
    if pushed_cargo {
        work.charge::<SnapshotStop<E>>(key_cost(&rel, ""))?;
        known.insert(rel.clone());
    }
    Ok(Level {
        dir,
        rel,
        paths,
        observed,
        next: 0,
        pushed_cargo,
    })
}

#[cfg(test)]
#[path = "snapshot_walk_tests.rs"]
mod tests;
