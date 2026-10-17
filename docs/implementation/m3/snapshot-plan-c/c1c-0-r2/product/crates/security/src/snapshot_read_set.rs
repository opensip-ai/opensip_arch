// M3-C r8 item 3 (unit C1c-0; C1c plan r4 sections 2 and 3): the read set's
// security primitives, ahead of the read set itself (C1c-1).
//
// `open_pruned` is the pruned-tree capture opener that C2's layout reads use
// (LD-C1C-2): a path whose outermost dependency segment lies before its leaf
// is reached from the retained root by no-follow opens, each directory
// observed through its parent and compared. Directories above the
// dependency anchor are judged under S3 directory custody, as
// `SnapshotRoot::open` judges them. At and below it only the descriptor
// discipline applies (SL:266: a pruned tree is never custody-walked), and an
// installed manifest is never judged under config-file custody or its 4 MiB
// marker ceiling (the Q2 ruling). A VCS segment or a custody anchor on the
// path refuses.
//
// `authorize_read` is the read set's authorization (LD-C1C-5), the shared
// rule's `read_set_path` over the full path, with the walk's own evidence
// (LD-C1C-13). `observes_dependency_cargo_root` is the charged, no-follow
// `Cargo.toml` observation the read set derives dependency-tree Cargo roots
// from: an operational observation, never a source read. Nothing here reads
// content: `crates/host/src/snapshot.rs` is the only source-read site
// (C1-T2). Every step is charged to the caller's ledger before it is made.
use crate::custody::discovery_rule::{self as rule, PrunedCapture, ReadSetPath};
use crate::custody::discovery_walk::owned;
use crate::custody::project_chain::ProjectObject;
use crate::snapshot_source::{
    SnapshotCustody, SnapshotFailure, SnapshotRefusal, SnapshotRoot, SourceFile, io_failure,
    join_rel, judge_opened, judge_root, key_cost, open_directory, open_regular, refuse,
    source_file,
};
use crate::snapshot_walk::{SnapshotExtent, WalkEvidence};
use opensip_platform::{ChildKind, ChildObservation, RetainedDirectory, WorkCost, WorkScope};
use std::collections::BTreeSet;
use std::ffi::OsStr;

/// The record overhead the discovery walk prices every owned record with
/// (`discovery_walk.rs`, `RECORD`), as `snapshot_walk.rs` mirrors it.
const RECORD: usize = 128;

/// `rule::pruned_capture`'s temporaries for `path`, counted from the rule's
/// source: the segment list, and at most one custody anchor of at most the
/// path's length.
fn pruned_capture_cost(path: &str) -> WorkCost {
    let segments = path.split('/').count();
    WorkCost {
        objects: 2,
        edges: 0,
        bytes: segments
            .saturating_mul(2 * std::mem::size_of::<usize>())
            .saturating_add(path.len())
            .saturating_add(2 * RECORD),
    }
}

/// `rule::read_set_path`'s temporaries for `authorized` and `relative`,
/// counted from the rule's source: one segment list over the full path,
/// per `target` segment the Cargo-root prefix it is tested as, and at most
/// one custody anchor, each at most the full path's length.
pub fn read_set_path_cost(authorized: &str, relative: &str) -> WorkCost {
    let full = authorized
        .len()
        .saturating_add(1)
        .saturating_add(relative.len());
    let parts = authorized
        .split('/')
        .chain(relative.split('/').filter(|_| !relative.is_empty()));
    let (segments, targets) = parts.fold((0usize, 0usize), |(n, t), part| {
        (n + 1, t + (part == "target") as usize)
    });
    let objects = 2 + targets;
    WorkCost {
        objects,
        edges: 0,
        bytes: segments
            .saturating_mul(2 * std::mem::size_of::<usize>())
            .saturating_add(full.saturating_mul(1 + targets))
            .saturating_add(objects.saturating_mul(RECORD)),
    }
}

/// The read set's authorization of one path (C1c plan r4, LD-C1C-5): the
/// shared rule's answer, its exclusion spelled as the rule spells it
/// (`nested-package`, `vcs-tree`, `cargo-build-output` or
/// `opensip-custody-state`).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ReadAuthorization {
    Admitted,
    Excluded(&'static str),
    /// The authorized directory lies in no dependency tree.
    Forbidden,
}

/// The read set's authorization of `relative` below `authorized` (a layout
/// row's `realPath`), charged first (C1c plan r4, LD-C1C-5 and LD-C1C-13):
/// the shared rule's `read_set_path` over the full path, with the
/// first-party Cargo roots and member roots of the same session's own walk
/// (`evidence`), and the dependency-tree Cargo roots the read set observed.
pub fn authorize_read(
    authorized: &str,
    relative: &str,
    evidence: &WalkEvidence,
    dependency_cargo_roots: &BTreeSet<String>,
    work: &mut WorkScope<'_>,
) -> Result<ReadAuthorization, SnapshotFailure> {
    work.charge::<SnapshotRefusal>(read_set_path_cost(authorized, relative))?;
    Ok(
        match rule::read_set_path(
            authorized,
            relative,
            evidence.cargo_roots(),
            dependency_cargo_roots,
            evidence.member_roots(),
        ) {
            ReadSetPath::Admitted => ReadAuthorization::Admitted,
            ReadSetPath::Excluded(exclusion) => ReadAuthorization::Excluded(exclusion.as_str()),
            ReadSetPath::Forbidden => ReadAuthorization::Forbidden,
        },
    )
}

/// Whether `dir`, at `rel`, is a dependency-tree Cargo root (LD-C1C-13): its
/// `Cargo.toml` entry observed with `fstatat(AT_SYMLINK_NOFOLLOW)` relative
/// to the held descriptor, charged by the observation's owner, and a
/// regular file there, with `rel` in a dependency tree. No byte of the
/// manifest is read.
pub fn observes_dependency_cargo_root(
    dir: &RetainedDirectory,
    rel: &str,
    work: &mut WorkScope<'_>,
) -> Result<bool, SnapshotFailure> {
    let observation = dir
        .observe_child_accounted(OsStr::new(rule::CARGO_MARKER), work)
        .map_err(io_failure)?;
    let regular = matches!(
        observation,
        ChildObservation::Present {
            kind: ChildKind::File,
            ..
        }
    );
    Ok(rule::is_dependency_cargo_root(rel, regular))
}

/// The pruned-tree capture opener (LD-C1C-2), for C2's layout reads. The
/// shared grammar's validated copy, charged first, is kept as the source
/// file's path. Then the rule places the path (its dependency anchor, or a
/// refusal); the retained root is judged; each directory component is
/// observed through its parent with `fstatat(AT_SYMLINK_NOFOLLOW)`, opened
/// `O_NOFOLLOW` and compared, and judged under S3 directory custody only
/// above the dependency anchor; the leaf is observed, opened and compared,
/// with no config-file custody. A symlinked component or leaf refuses.
/// Charged to `work`, the ledger the caller passes.
pub fn open_pruned(
    root: &SnapshotRoot<'_>,
    path: &str,
    extent: &SnapshotExtent<'_>,
    custody: SnapshotCustody<'_>,
    work: &mut WorkScope<'_>,
) -> Result<SourceFile, SnapshotFailure> {
    work.charge::<SnapshotRefusal>(owned(path.len()))?;
    let Ok(validated) = opensip_identity::LogicalPath::parse(path) else {
        return refuse(SnapshotRefusal::Name {
            parent: String::new(),
            name: path.escape_default().to_string(),
        });
    };
    work.charge::<SnapshotRefusal>(pruned_capture_cost(path))?;
    let anchor = match rule::pruned_capture(path, extent.member_roots()) {
        PrunedCapture::Anchor(index) => index,
        PrunedCapture::Outside => {
            return refuse(SnapshotRefusal::PrunedPath {
                path: path.to_owned(),
                reason: "outside-dependency-tree",
            });
        }
        PrunedCapture::Excluded(exclusion) => {
            return refuse(SnapshotRefusal::PrunedPath {
                path: path.to_owned(),
                reason: exclusion.as_str(),
            });
        }
    };
    judge_root(root, custody, work)?;
    // The anchor lies before the leaf, so the path has a directory part.
    let (dirs, leaf) = path.rsplit_once('/').unwrap_or(("", path));
    let mut held: Option<RetainedDirectory> = None;
    let mut rel = String::new();
    for (index, part) in dirs.split('/').enumerate() {
        let parent = held.as_ref().unwrap_or(root.retained());
        work.charge::<SnapshotRefusal>(key_cost(&rel, part))?;
        let sub = join_rel(&rel, part);
        let observation = parent
            .observe_child_accounted(OsStr::new(part), work)
            .map_err(io_failure)?;
        if !matches!(
            observation,
            ChildObservation::Present {
                kind: ChildKind::Directory,
                ..
            }
        ) {
            return refuse(SnapshotRefusal::NotARegularFile(path.to_owned()));
        }
        let (next, sample) = open_directory(parent, part, &sub, &observation, work)?;
        // S3 custody above the dependency anchor only (SL:266).
        if index < anchor
            && let Err(reason) = judge_opened(
                root.lent(),
                custody,
                next.as_file(),
                &sample,
                &sub,
                ProjectObject::Directory,
                work,
            )?
        {
            return refuse(SnapshotRefusal::Custody { path: sub, reason });
        }
        held = Some(next);
        rel = sub;
    }
    let parent = held.as_ref().unwrap_or(root.retained());
    let observation = parent
        .observe_child_accounted(OsStr::new(leaf), work)
        .map_err(io_failure)?;
    let ChildObservation::Present {
        kind: ChildKind::File,
        metadata,
    } = observation
    else {
        return refuse(SnapshotRefusal::NotARegularFile(path.to_owned()));
    };
    let file = open_regular(parent, leaf, path, &metadata, work)?;
    // Below the anchor no file is judged as a marker.
    Ok(source_file(validated.into_string(), file, metadata, false))
}
