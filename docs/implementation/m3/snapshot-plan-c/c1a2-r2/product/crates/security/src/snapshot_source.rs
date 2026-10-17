// M3-C r8 items 1 and 2 (unit C1a1, C1a plan r4 section 1): the snapshot's
// lawful root and its one opening rule. `SnapshotRoot` wraps the existing
// discovery lendings: `from_operation`, the durable writer handoff after the
// fence is released (under the lease), and `from_released_read`, the
// ephemeral read session's equivalent release (I complete; no lease, no
// fence). The I-absent root is join E-1 (M3-J1 item 6), added when it lands.
//
// `SnapshotRoot::open` is the pre-walk capture opener only: it walks a
// logical path's components from the retained root, judging S3 directory
// custody on each directory and config-file custody on a marker, and opens
// the final regular file `O_NOFOLLOW`, comparing it with its observation.
// The extent walk (`snapshot_walk.rs`) opens from its enumerating parent
// instead. Nothing here reads content: `crates/host/src/snapshot.rs` is the
// only source-read site (C1-T2). No census-closure file is changed; every
// shared rule is called, never copied.
use crate::custody::discovery_rule::WORKSPACE_MARKERS;
use crate::custody::discovery_scan::{EntryJudgment, ObservedAcl, ObservedEntry, judge_entry};
use crate::custody::discovery_walk::{STATUS, owned, same_object};
use crate::custody::project_chain::{DiscoveryRoot, ProjectObject};
use crate::grants::ProjectOwnerWaiver;
use opensip_platform::{
    CapturedAclState, ChildKind, ChildObservation, DescriptorAclCaptureError, DescriptorMetadata,
    RetainedDirectory, WorkCost, WorkFailure, WorkScope,
};
use std::collections::BTreeSet;
use std::ffi::OsStr;
use std::fs::File;
use std::io;

/// The snapshot's root: one of the lawful lendings, nothing else.
pub struct SnapshotRoot<'a> {
    root: DiscoveryRoot<'a>,
}
impl std::fmt::Debug for SnapshotRoot<'_> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("SnapshotRoot").finish_non_exhaustive()
    }
}
impl<'a> SnapshotRoot<'a> {
    /// Durable: the writer handoff's root, after the fence is released.
    pub fn from_operation(operation: &'a crate::ProjectOperation) -> Self {
        Self {
            root: operation.discovery_root(),
        }
    }
    /// Ephemeral, I complete: the released read session's root.
    /// Crate-internal until J2c exposes the read entry.
    #[allow(dead_code)]
    pub(crate) fn from_released_read(
        read: &'a crate::custody::installation_read::ReleasedRead,
        admission: &'a crate::custody::project_admission::ProjectRootAdmission,
    ) -> Self {
        Self {
            root: read.discovery_root(admission),
        }
    }
    /// Unit tests only: a scratch root with a test premise.
    #[cfg(test)]
    pub(crate) fn for_tests(root: DiscoveryRoot<'a>) -> Self {
        Self { root }
    }
    pub(crate) fn lent(&self) -> &DiscoveryRoot<'a> {
        &self.root
    }
    pub(crate) fn retained(&self) -> &'a RetainedDirectory {
        self.root.root()
    }
}

/// Who is judging custody: the invoking user, the authorized groups and the
/// typed owner waiver (which applies to directories, never to markers).
#[derive(Clone, Copy)]
pub struct SnapshotCustody<'a> {
    pub(crate) uid: u32,
    pub(crate) groups: &'a BTreeSet<u32>,
    pub(crate) waiver: Option<&'a ProjectOwnerWaiver>,
}
impl<'a> SnapshotCustody<'a> {
    #[allow(dead_code)]
    pub(crate) fn new(
        uid: u32,
        groups: &'a BTreeSet<u32>,
        waiver: Option<&'a ProjectOwnerWaiver>,
    ) -> Self {
        Self {
            uid,
            groups,
            waiver,
        }
    }
}

/// One regular file of the snapshot, opened `O_NOFOLLOW` and compared with
/// its observation; never read here.
#[derive(Debug)]
pub struct SourceFile {
    path: String,
    file: File,
    observation: DescriptorMetadata,
    marker: bool,
}
impl SourceFile {
    /// The logical path, root-relative.
    pub fn path(&self) -> &str {
        &self.path
    }
    /// The opened descriptor (the host's `snapshot.rs` reads it once).
    pub fn file(&mut self) -> &mut File {
        &mut self.file
    }
    /// The observation made through the enumerating parent, before the open.
    pub fn observation(&self) -> &DescriptorMetadata {
        &self.observation
    }
    pub fn is_marker(&self) -> bool {
        self.marker
    }
    pub fn into_parts(self) -> (String, File, DescriptorMetadata) {
        (self.path, self.file, self.observation)
    }
}

/// Why opening or walking refused. Never a partial result, never retried.
#[derive(Debug)]
pub enum SnapshotRefusal {
    /// A name that is not a logical path (item 2), with its parent and the
    /// escaped name bytes (the remedy is renaming it, or `ignorePaths`).
    Name { parent: String, name: String },
    /// A listing reached the platform's entry or name-byte ceiling.
    ListingBound,
    /// An object vanished, changed identity or kind between its observation
    /// and its open, or between two observations of one path. Never retried.
    Changed(String),
    /// A directory failed S3 directory custody.
    Custody { path: String, reason: String },
    /// A marker failed config-file custody.
    MarkerCustody { path: String, reason: String },
    /// The path names something that is not a regular file, or is absent.
    NotARegularFile(String),
    /// An ACL capture failed.
    Capture(String),
    /// The omission premise could not sample a filesystem.
    Premise(String),
    /// A host I/O failure or descriptor exhaustion.
    HostIo(io::Error),
}
pub type SnapshotFailure = WorkFailure<SnapshotRefusal>;
pub(crate) fn refuse<T>(refusal: SnapshotRefusal) -> Result<T, SnapshotFailure> {
    Err(WorkFailure::Operation(refusal))
}
pub(crate) fn io_failure(failure: WorkFailure<io::Error>) -> SnapshotFailure {
    match failure {
        WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
        WorkFailure::Operation(error) => WorkFailure::Operation(SnapshotRefusal::HostIo(error)),
    }
}
fn capture_failure(failure: WorkFailure<DescriptorAclCaptureError>) -> SnapshotFailure {
    match failure {
        WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
        WorkFailure::Operation(error) => {
            WorkFailure::Operation(SnapshotRefusal::Capture(format!("{error:?}")))
        }
    }
}

pub(crate) fn join_rel(rel: &str, name: &str) -> String {
    if rel.is_empty() {
        name.to_owned()
    } else {
        format!("{rel}/{name}")
    }
}
pub(crate) fn last_segment(rel: &str) -> &str {
    rel.rsplit('/').next().unwrap_or(rel)
}
pub(crate) fn is_marker_name(name: &str) -> bool {
    WORKSPACE_MARKERS.contains(&name)
}

/// One opened object's custody judgment (S3): the metadata-only rejection
/// first; when it passes, one premise-applied ACL capture of the same object,
/// charged by its owner, then the full judgment.
pub(crate) fn judge_opened(
    root: &DiscoveryRoot<'_>,
    custody: SnapshotCustody<'_>,
    file: &File,
    observed: &DescriptorMetadata,
    rel: &str,
    object: ProjectObject,
    work: &mut WorkScope<'_>,
) -> Result<Result<(), String>, SnapshotFailure> {
    let waiver = match object {
        ProjectObject::Directory => custody.waiver,
        ProjectObject::ConfigurationFile => None,
    };
    let mut entry = ObservedEntry {
        metadata: observed.clone(),
        acl: ObservedAcl::NotObserved,
        vcs: None,
    };
    match judge_entry(Some(&entry), object, custody.uid, custody.groups, waiver) {
        EntryJudgment::Passed => return Ok(Ok(())),
        EntryJudgment::Refused(refusal) => return Ok(Err(format!("{refusal:?}"))),
        EntryJudgment::NeedsAcl => {}
    }
    let sample =
        opensip_platform::capture_descriptor_acl_accounted(file, work).map_err(capture_failure)?;
    if !same_object(observed, sample.metadata()) {
        return refuse(SnapshotRefusal::Changed(rel.to_owned()));
    }
    let acl = match sample.acl_state() {
        CapturedAclState::Entries(count) => {
            work.charge::<SnapshotRefusal>(owned(
                count.saturating_mul(std::mem::size_of::<opensip_platform::CapturedAclEntry>()),
            ))?;
            (0..count)
                .map(|index| sample.entry(index))
                .collect::<Option<Vec<_>>>()
                .map_or(ObservedAcl::Unreadable, ObservedAcl::Entries)
        }
        CapturedAclState::NotReturned => {
            let admitted = match root.premise() {
                Some(premise) => premise.admits(file, work).map_err(|f| match f {
                    WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
                    WorkFailure::Operation(error) => {
                        WorkFailure::Operation(SnapshotRefusal::Premise(format!("{error:?}")))
                    }
                })?,
                None => false,
            };
            if admitted {
                ObservedAcl::Entries(Vec::new())
            } else {
                ObservedAcl::Unreadable
            }
        }
        CapturedAclState::NoAclSentinel => ObservedAcl::Unreadable,
    };
    entry.metadata = sample.metadata().clone();
    entry.acl = acl;
    Ok(
        match judge_entry(Some(&entry), object, custody.uid, custody.groups, waiver) {
            EntryJudgment::Passed => Ok(()),
            EntryJudgment::Refused(refusal) => Err(format!("{refusal:?}")),
            EntryJudgment::NeedsAcl => Err("AclUnreadable".to_owned()),
        },
    )
}

/// The retained root's own custody (S3 directory custody, the waiver
/// applying): one status sample of the lent descriptor, then
/// `judge_opened`. Both the walk and the pre-walk opener judge it first, so
/// no capture rests on an admission-time judgment alone (unit C1a1 r2, Codex
/// C1A1-R1-RF-3). A failure refuses `Custody` at the root, terminally.
pub(crate) fn judge_root(
    root: &SnapshotRoot<'_>,
    custody: SnapshotCustody<'_>,
    work: &mut WorkScope<'_>,
) -> Result<(), SnapshotFailure> {
    let lent = root.retained();
    let sample = work.run(STATUS, |_| {
        opensip_platform::observe_descriptor_metadata(lent.as_file())
            .map_err(|error| WorkFailure::Operation(SnapshotRefusal::HostIo(error)))
    })?;
    match judge_opened(
        root.lent(),
        custody,
        lent.as_file(),
        &sample,
        "",
        ProjectObject::Directory,
        work,
    )? {
        Ok(()) => Ok(()),
        Err(reason) => refuse(SnapshotRefusal::Custody {
            path: String::new(),
            reason,
        }),
    }
}

// Unit tests only: a hook run just before an observed object is opened, for
// the swap and ancestor-replacement controls (C1-T4, C1A-T5).
#[cfg(test)]
pub(crate) type OpenHook = Option<Box<dyn FnMut(&str)>>;
#[cfg(test)]
thread_local! {
    static BEFORE_OPEN: std::cell::RefCell<OpenHook> = const { std::cell::RefCell::new(None) };
}
#[cfg(test)]
pub(crate) fn set_before_open(hook: OpenHook) {
    BEFORE_OPEN.with_borrow_mut(|h| *h = hook);
}
#[cfg(test)]
fn before_open(rel: &str) {
    BEFORE_OPEN.with_borrow_mut(|h| {
        if let Some(h) = h {
            h(rel);
        }
    });
}
#[cfg(not(test))]
fn before_open(_: &str) {}

/// Open a child observed as a directory, relative to its parent, and compare
/// it with that observation. Gone, a link or another kind now is a change.
pub(crate) fn open_directory(
    parent: &RetainedDirectory,
    name: &str,
    rel: &str,
    observation: &ChildObservation,
    work: &mut WorkScope<'_>,
) -> Result<(RetainedDirectory, DescriptorMetadata), SnapshotFailure> {
    before_open(rel);
    let opened = work.run(
        opensip_platform::open_child_directory_cost(OsStr::new(name)),
        |_| Ok::<_, SnapshotFailure>(parent.open_child_directory(OsStr::new(name))),
    )?;
    let directory = match opened {
        Ok(directory) => directory,
        Err(error)
            if matches!(
                error.kind(),
                io::ErrorKind::NotFound | io::ErrorKind::NotADirectory
            ) || error.raw_os_error() == Some(libc_eloop()) =>
        {
            return refuse(SnapshotRefusal::Changed(rel.to_owned()));
        }
        Err(error) => return refuse(SnapshotRefusal::HostIo(error)),
    };
    let sample = work.run(STATUS, |_| {
        opensip_platform::observe_descriptor_metadata(directory.as_file())
            .map_err(|error| WorkFailure::Operation(SnapshotRefusal::HostIo(error)))
    })?;
    if !observation.matches(&sample) {
        return refuse(SnapshotRefusal::Changed(rel.to_owned()));
    }
    Ok((directory, sample))
}

/// Open a child observed as a regular file `O_NOFOLLOW`, relative to its
/// parent, and compare it with that observation.
pub(crate) fn open_regular(
    parent: &RetainedDirectory,
    name: &str,
    rel: &str,
    observed: &DescriptorMetadata,
    work: &mut WorkScope<'_>,
) -> Result<File, SnapshotFailure> {
    before_open(rel);
    let opened = work.run(RetainedDirectory::open_regular_cost(name), |_| {
        Ok::<_, SnapshotFailure>(parent.open_regular(name))
    })?;
    let file = match opened {
        Ok(file) => file,
        Err(error)
            if matches!(
                error.kind(),
                io::ErrorKind::NotFound | io::ErrorKind::InvalidInput
            ) || error.raw_os_error() == Some(libc_eloop()) =>
        {
            return refuse(SnapshotRefusal::Changed(rel.to_owned()));
        }
        Err(error) => return refuse(SnapshotRefusal::HostIo(error)),
    };
    let sample = work.run(STATUS, |_| {
        opensip_platform::observe_descriptor_metadata(&file)
            .map_err(|error| WorkFailure::Operation(SnapshotRefusal::HostIo(error)))
    })?;
    if !same_object(observed, &sample) {
        return refuse(SnapshotRefusal::Changed(rel.to_owned()));
    }
    Ok(file)
}

/// `ELOOP`: a symbolic link met by an `O_NOFOLLOW` open.
const fn libc_eloop() -> i32 {
    62
}

/// The discovery walk's prices, exported for the host's capture session and
/// candidate custody (unit C1a2), so the snapshot has one price list: one
/// status read of a retained descriptor, and one owned record of `bytes`.
pub const STATUS_COST: WorkCost = STATUS;
pub fn owned_record(bytes: usize) -> WorkCost {
    owned(bytes)
}

/// Why a candidate custody directory is not private to the invoking user.
#[derive(Debug)]
pub enum CustodyDirectoryRefusal {
    /// The ACL sample itself failed.
    Capture(DescriptorAclCaptureError),
    /// The sample omitted the ACL or carried the NOACL sentinel. That is
    /// unavailable evidence, never an absence of other writers (law 461).
    AclUnavailable,
    /// Not a 0700 directory owned by the invoking user.
    NotPrivate,
    /// An ACL entry grants a right to another principal (an inherit-only
    /// entry included, which would pass it to every new custody file), or
    /// cannot be interpreted.
    ForeignAccess,
}

/// Judge the candidate custody directory private (unit C1a2 r2, Codex
/// C1A2-R1-RF-1), bound to its retained descriptor: one charged ACL capture,
/// then the private-descendant predicate of `private_access`: a 0700
/// directory of `invoking_uid` whose present ACL grants no right to anyone
/// else, inherit-only entries included. So no other principal can traverse,
/// add, remove or rename a custody entry, and no custody file inherits a
/// grant. The invoking user's own processes and root are outside what any
/// custody check excludes. Contents and the path to the directory are not
/// judged.
#[cfg(target_os = "macos")]
pub fn admit_custody_directory(
    directory: &File,
    invoking_uid: u32,
    work: &mut WorkScope<'_>,
) -> Result<(), WorkFailure<CustodyDirectoryRefusal>> {
    use crate::private_access::{PreparePrivateError, PrivateAccessRefusal as A};
    crate::private_access::observe_private_directory(directory, invoking_uid, work)
        .map(|_| ())
        .map_err(|failure| match failure {
            WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
            WorkFailure::Operation(error) => WorkFailure::Operation(match error {
                PreparePrivateError::Capture(WorkFailure::Operation(error)) => {
                    CustodyDirectoryRefusal::Capture(error)
                }
                PreparePrivateError::Access(A::AclNotReturned | A::AclSentinelUnqualified) => {
                    CustodyDirectoryRefusal::AclUnavailable
                }
                PreparePrivateError::Access(A::ForeignOwner | A::ModeShape | A::LinkCount) => {
                    CustodyDirectoryRefusal::NotPrivate
                }
                PreparePrivateError::Access(
                    A::ForeignAclAccess
                    | A::UnknownAceKind
                    | A::UnknownAceFlags
                    | A::InconsistentCapture,
                ) => CustodyDirectoryRefusal::ForeignAccess,
                // `observe_private_directory` neither appends, creates nor
                // names, and its capture lifts a budget failure outward.
                PreparePrivateError::Capture(WorkFailure::Budget(_))
                | PreparePrivateError::Append(_)
                | PreparePrivateError::Create(_)
                | PreparePrivateError::Name => {
                    unreachable!("observe_private_directory only captures and judges")
                }
            }),
        })
}

/// The cost of one owned root-relative key.
pub(crate) fn key_cost(dir: &str, name: &str) -> WorkCost {
    owned(dir.len() + 1 + name.len())
}

impl SnapshotRoot<'_> {
    /// The pre-walk capture opener (item 1; C1a plan r4 RF-1): the retained
    /// root judged first (`judge_root`), then `path`'s components walked
    /// from it, each directory observed
    /// with `fstatat(AT_SYMLINK_NOFOLLOW)`, opened `O_NOFOLLOW`, compared and
    /// judged under S3 directory custody; the final regular file judged under
    /// config-file custody when it is a marker, opened and compared. Charged
    /// to `work` (the discovery ledger for B2's and C2's captures).
    pub fn open(
        &self,
        path: &str,
        custody: SnapshotCustody<'_>,
        work: &mut WorkScope<'_>,
    ) -> Result<SourceFile, SnapshotFailure> {
        // The shared grammar's validated copy, charged before it is made, is
        // kept as the source file's path: no second copy (Codex
        // C1A1-R2-RF-1).
        work.charge::<SnapshotRefusal>(owned(path.len()))?;
        let Ok(validated) = opensip_identity::LogicalPath::parse(path) else {
            return refuse(SnapshotRefusal::Name {
                parent: String::new(),
                name: path.escape_default().to_string(),
            });
        };
        judge_root(self, custody, work)?;
        // The components are borrowed views of `path`; only `rel`, charged,
        // is built (Codex C1A1-R1-RF-4).
        let (dirs, leaf) = path.rsplit_once('/').unwrap_or(("", path));
        let mut held: Option<RetainedDirectory> = None;
        let mut rel = String::new();
        for part in dirs.split('/').filter(|_| !dirs.is_empty()) {
            let parent = held.as_ref().unwrap_or(self.retained());
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
            if let Err(reason) = judge_opened(
                &self.root,
                custody,
                next.as_file(),
                &sample,
                &sub,
                ProjectObject::Directory,
                work,
            )? {
                return refuse(SnapshotRefusal::Custody { path: sub, reason });
            }
            held = Some(next);
            rel = sub;
        }
        let parent = held.as_ref().unwrap_or(self.retained());
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
        let marker = is_marker_name(leaf);
        if marker
            && let Err(reason) = judge_opened(
                &self.root,
                custody,
                &file,
                &metadata,
                path,
                ProjectObject::ConfigurationFile,
                work,
            )?
        {
            return refuse(SnapshotRefusal::MarkerCustody {
                path: path.to_owned(),
                reason,
            });
        }
        Ok(SourceFile {
            path: validated.into_string(),
            file,
            observation: metadata,
            marker,
        })
    }
}

/// A `SourceFile` from the walk (crate-internal constructor).
pub(crate) fn source_file(
    path: String,
    file: File,
    observation: DescriptorMetadata,
    marker: bool,
) -> SourceFile {
    SourceFile {
        path,
        file,
        observation,
        marker,
    }
}

// Unit C1a2's route controls (C1A-T2, C1A-T3).
#[cfg(test)]
#[path = "snapshot_route_tests.rs"]
mod route_tests;
