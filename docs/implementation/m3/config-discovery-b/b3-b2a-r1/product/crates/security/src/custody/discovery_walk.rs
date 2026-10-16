// M3-B r5 items 12 and 13 (unit B2-b3b; B2-b3 plan r2 section 3, LD-B2B3-2
// to LD-B2B3-6 and LD-B2B3-13): the S3 downward walker. It runs after the
// fence is released, on a lent `DiscoveryRoot`, and charges the caller's one
// discovery ledger before every step. It observes exactly the B2-b0
// reference's walker population, then hands it to B2-b2's core:
// - the unit source is chosen before traversal (plan r4 LD-B2B-8);
// - automatic mode lists the root and every ordinary directory down to 256
//   segments, depth first; a pruned anchor is its own entry only and is never
//   opened; a directory holding a VCS marker or `opensip.json` is a boundary,
//   probed by name and never listed; a 257-segment directory is opened only
//   to observe its four marker names;
// - explicit and config modes walk each named root's chain parent-first,
//   observing its markers by name at each level, then list that root's
//   subtree by the automatic rule;
// - every listed name is charged, `.` and `..` are discarded, and every other
//   name must form a logical path, or the whole discovery refuses;
// - only objects whose judgment reaches their ACL are captured: the walker
//   judges with the core's own `judge_entry`, in the core's order, so a
//   metadata-only rejection or a failing ancestor stops the captures there
//   (r2, Codex B2B3B-R1-RF-1); each capture is compared with its observation,
//   never reopened or retried; a non-regular marker is never opened;
// - a path observed twice must be the same object both times (r2, RF-2);
// - every owned record (spellings, scope entries, set and vector slots) is
//   charged before it is allocated (r2, RF-3).
// Peak descriptors (R2-NBO-1; r2 NBO-3): in a subtree, the retained frames on
// the current path (the root and depths 1 to 256); on a named chain, one per
// chain segment (the logical-path grammar allows up to 2,048), dropped before
// the named root's subtree; plus one temporary descriptor for a 257-segment
// directory, a marker or a `.git` file, and the listing stream, which closes
// before any child is observed. Running out refuses as host I/O. Nothing is
// created, written, followed or executed. Library only.
use super::discovery_rule::{self as rule, EntryDisposition, EntryKind, WORKSPACE_MARKERS};
use super::discovery_scan::{
    DiscoveryInvocation, DiscoveryRefusal, DiscoveryResultPending, EntryJudgment, ObservedAcl,
    ObservedEntry, ObservedScope, ObservedVcs, UnitSourceRequest, UnobservedAcl, UpwardProvenance,
    discover_observed, judge_entry,
};
use super::installation_root::ParentRefusal;
use super::project_admission::{
    CONFIG_FILE, ProjectAdmissionRefusal, VCS_MARKERS, gitdir_target, vcs_evidence,
};
use super::project_chain::{DiscoveryRoot, ProjectChainPolicy, ProjectObject};
use crate::grants::ProjectOwnerWaiver;
use crate::trust::AclOmissionPremise;
use opensip_identity::LogicalPath;
use opensip_platform::{
    CapturedAclState, ChildKind, ChildObservation, DescriptorAclCaptureError, DescriptorFilesystem,
    DescriptorMetadata, DirectoryVisitError, RetainedDirectory, WorkCost, WorkFailure, WorkScope,
};
use std::collections::{BTreeMap, BTreeSet};
use std::ffi::OsStr;
use std::fs::File;
use std::io;
use std::path::Path;

/// S3's listing depth: directories of at most 256 segments are listed.
const MAX_LISTED_DEPTH: usize = 256;
/// One directory listing, before any name (LD-B2B3-5): the stream, its
/// descriptor and one entry buffer (`first_registration.rs` SCAN).
const LISTING: WorkCost = WorkCost {
    objects: 2,
    edges: 3,
    bytes: 1024,
};
/// One listing entry visited, before any copy (unit B2-b3d): its edge.
const VISIT: WorkCost = WorkCost {
    objects: 0,
    edges: 1,
    bytes: 0,
};
/// The platform's per-directory ceilings (`directory_entries.rs`); reaching
/// either refuses as a bound, never truncation.
const MAX_LISTED_ENTRIES: usize = 131_072;
const MAX_LISTED_NAME_BYTES: usize = 268_435_456;
/// The platform's single-component grammar bound and staging prefix.
const MAX_COMPONENT_BYTES: usize = 1023;
const STAGING_PREFIX: &str = ".opensip-stage-";
/// One status read on a retained descriptor.
const STATUS: WorkCost = WorkCost {
    objects: 0,
    edges: 1,
    bytes: 512,
};
/// The storage of one owned record beyond its bytes: a conservative
/// allowance for the allocation header, a map or set node's links, and a
/// vector slot (r2, Codex B2B3B-R1-RF-3).
const RECORD: usize = 128;
/// One owned record of `bytes`, charged before it is allocated.
fn owned(bytes: usize) -> WorkCost {
    WorkCost {
        objects: 1,
        edges: 0,
        bytes: bytes.saturating_add(RECORD),
    }
}
/// The shared rule's temporaries for classifying `rel` (r3, Codex
/// B2B3B-R2-RF-2): its segment list, one prefix copy for each `target`
/// segment it tests against the Cargo roots, and the anchor's path.
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

/// Why a walk refused. None is a partial result.
#[derive(Debug)]
pub(crate) enum WalkRefusal {
    /// LD-B2B3-2: a listed name, or the root's spelling, that does not form
    /// a logical path (`PROJECT.ROOT_CUSTODY_REFUSED`).
    NameUnrepresentable { parent: String, name: String },
    /// LD-B2B3-5: a listed directory reached the platform's entry or name
    /// byte ceiling (`WORK.BUDGET_EXHAUSTED`, a bound).
    ListingBound,
    /// An object vanished, changed identity or is another kind between its
    /// observation and its open or capture. Never retried.
    Changed(String),
    /// The VCS evidence probe refused (change or host I/O).
    Evidence(ProjectAdmissionRefusal),
    /// An ACL capture failed.
    Capture(DescriptorAclCaptureError),
    /// The omission premise could not sample a filesystem.
    Premise(ParentRefusal),
    /// A host I/O failure, a union mount or descriptor exhaustion.
    HostIo(io::Error),
    /// The core's judgment reached an ACL the walk never captured: an
    /// instrument fault (LD-B2B3-3).
    Unobserved(UnobservedAcl),
}
impl WalkRefusal {
    /// The discovery result's refusal and detail, for the refusals that are
    /// discovery's (LD-B2B3-2). Bounds, changes, host I/O and instrument
    /// faults keep their own rows.
    pub(crate) fn discovery_refusal(&self) -> Option<(DiscoveryRefusal, String)> {
        match self {
            Self::NameUnrepresentable { parent, name } => Some((
                DiscoveryRefusal::RootCustodyRefused,
                format!("NAME_UNREPRESENTABLE:{parent}:{name}"),
            )),
            _ => None,
        }
    }
}
pub(crate) type Failure = WorkFailure<WalkRefusal>;
fn refuse<T>(refusal: WalkRefusal) -> Result<T, Failure> {
    Err(WorkFailure::Operation(refusal))
}
fn io_failure(failure: WorkFailure<io::Error>) -> Failure {
    match failure {
        WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
        WorkFailure::Operation(error) => WorkFailure::Operation(WalkRefusal::HostIo(error)),
    }
}
fn evidence_failure(failure: WorkFailure<ProjectAdmissionRefusal>) -> Failure {
    match failure {
        WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
        WorkFailure::Operation(refusal) => WorkFailure::Operation(WalkRefusal::Evidence(refusal)),
    }
}

// LD-B2B3-13: the test-only trace of every observe, open, list, probe and
// capture the walker makes, in order. Production carries nothing: each call
// passes a closure that spells the path, and the production stubs never call
// it (M3-B r6 item 12, unit B2-b3d LD-B2B3D-2; plan r2, Codex NBO-1).
#[cfg(test)]
thread_local! {
    static TRACE: std::cell::RefCell<Vec<(&'static str, String)>> =
        const { std::cell::RefCell::new(Vec::new()) };
    /// The walk's root spelling, for `trace_child`'s relative `at`.
    static TRACE_ROOT: std::cell::RefCell<String> = const { std::cell::RefCell::new(String::new()) };
}
#[cfg(test)]
fn trace(op: &'static str, path: impl FnOnce() -> String) {
    let path = path();
    TRACE.with_borrow_mut(|t| t.push((op, path)));
}
#[cfg(not(test))]
fn trace(_: &'static str, _: impl FnOnce() -> String) {}
#[cfg(test)]
fn set_trace_root(root: &str) {
    TRACE_ROOT.with_borrow_mut(|r| root.clone_into(r));
}
#[cfg(not(test))]
fn set_trace_root(_: &str) {}
/// The trace for an operation on `name` under the directory `dir`, for
/// B2-b3a's evidence probe (r2, Codex B2B3B-R1-NBO-2). The walker passes its
/// root-relative path, which the test-only trace spells under the walk's
/// root; upward selection passes an absolute one. It builds nothing outside
/// tests.
#[cfg(test)]
pub(super) fn trace_child(op: &'static str, dir: &Path, name: &str) {
    let dir = if dir.is_relative() {
        TRACE_ROOT.with_borrow(|root| {
            let root = Path::new(root.as_str());
            if dir.as_os_str().is_empty() {
                root.to_path_buf()
            } else {
                root.join(dir)
            }
        })
    } else {
        dir.to_path_buf()
    };
    trace(op, || dir.join(name).to_string_lossy().into_owned());
}
#[cfg(not(test))]
pub(super) fn trace_child(_: &'static str, _: &Path, _: &str) {}
#[cfg(test)]
pub(crate) fn take_trace() -> Vec<(&'static str, String)> {
    TRACE.with_borrow_mut(std::mem::take)
}
// Unit tests only: a hook run just before the walker opens an observed
// object, for the swap controls.
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
fn before_open(path: impl FnOnce() -> String) {
    let path = path();
    BEFORE_OPEN.with_borrow_mut(|h| {
        if let Some(h) = h {
            h(&path);
        }
    });
}
#[cfg(not(test))]
fn before_open(_: impl FnOnce() -> String) {}

/// A byte string as printable ASCII: graphic bytes but `%` and `:` stay;
/// every other byte is `%XX`.
fn escaped(bytes: &[u8]) -> String {
    let mut out = String::new();
    for &b in bytes {
        if b.is_ascii_graphic() && b != b'%' && b != b':' {
            out.push(b as char);
        } else {
            out.push_str(&format!("%{b:02X}"));
        }
    }
    out
}
fn join(dir: &str, name: &str) -> String {
    if dir == "/" {
        format!("/{name}")
    } else {
        format!("{dir}/{name}")
    }
}
fn join_rel(rel: &str, name: &str) -> String {
    if rel.is_empty() {
        name.to_owned()
    } else {
        format!("{rel}/{name}")
    }
}
/// A root-relative path's absolute spelling under `root`: built only for a
/// terminal refusal or the test-only trace (unit B2-b3d, LD-B2B3D-2/3).
fn spelled(root: &str, rel: &str) -> String {
    if rel.is_empty() {
        root.to_owned()
    } else {
        join(root, rel)
    }
}
/// A root-relative path's last segment: a child's name, borrowed.
fn last_segment(rel: &str) -> &str {
    rel.rsplit('/').next().unwrap_or(rel)
}
fn same_object(a: &DescriptorMetadata, b: &DescriptorMetadata) -> bool {
    a.device == b.device && a.inode == b.inode && a.mode & 0o170000 == b.mode & 0o170000
}

/// LD-B2B3-2 (r2): a listed name, not `.` or `..`, is one platform
/// component and its root-relative path is a logical path (segments of at
/// most 255 scalars, at most 4096 in all). Returns that path, or `None`.
fn listed_path(parent_rel: &str, raw: &[u8]) -> Option<String> {
    let name = std::str::from_utf8(raw).ok()?;
    if name.len() > MAX_COMPONENT_BYTES
        || name.contains(['/', '\\', '\0'])
        || name.starts_with(STAGING_PREFIX)
    {
        return None;
    }
    let rel = join_rel(parent_rel, name);
    LogicalPath::parse(&rel).is_ok().then_some(rel)
}

/// Unit tests only: `listed_path` with the refusal a listing raises for a
/// name that is not a logical path (the closed name controls).
#[cfg(test)]
fn listed_name(parent_abs: &str, parent_rel: &str, raw: &[u8]) -> Result<String, Failure> {
    listed_path(parent_rel, raw).map_or_else(
        || {
            refuse(WalkRefusal::NameUnrepresentable {
                parent: parent_abs.to_owned(),
                name: escaped(raw),
            })
        },
        Ok,
    )
}

/// One directory listing converted in one pass (unit B2-b3d, LD-B2B3D-4;
/// plan r2, Codex B2B3DPLAN-R1-RF-2). The visitor charges each raw entry's
/// visit, discards `.` and `..`, and converts every other name to its one
/// owned root-relative path, charged before it is built (with the
/// validator's copy). At the first name that is not a logical path it keeps
/// that name's bytes, charged, and converts no more, but the listing still
/// runs to completion: a listing failure refuses first, and only a complete
/// listing turns the kept name into `NAME_UNREPRESENTABLE`.
pub(crate) struct ListingConversion {
    pub(crate) paths: Vec<String>,
    invalid: Option<Vec<u8>>,
}
impl ListingConversion {
    pub(crate) fn new() -> Self {
        Self {
            paths: Vec::new(),
            invalid: None,
        }
    }
    /// One raw name from the listing visitor.
    pub(crate) fn accept(
        &mut self,
        parent_rel: &str,
        raw: &[u8],
        work: &mut WorkScope<'_>,
    ) -> Result<(), Failure> {
        work.charge::<WalkRefusal>(VISIT)?;
        if raw == b"." || raw == b".." || self.invalid.is_some() {
            return Ok(());
        }
        // The owned root-relative path and the validator's copy of it, with
        // their slots, charged before they are built.
        work.charge::<WalkRefusal>(WorkCost {
            objects: 2,
            edges: 0,
            bytes: 2 * (parent_rel.len() + 1 + raw.len()) + 2 * RECORD,
        })?;
        match listed_path(parent_rel, raw) {
            Some(rel) => self.paths.push(rel),
            None => {
                work.charge::<WalkRefusal>(owned(raw.len()))?;
                self.invalid = Some(raw.to_vec());
            }
        }
        Ok(())
    }
    /// The listing's outcome, in today's order: the listing's own failure,
    /// then a kept name that is not a logical path (its parent spelled only
    /// now, a terminal refusal), then the sorted paths.
    pub(crate) fn finish(
        mut self,
        visited: Result<opensip_platform::DirectoryVisitSummary, DirectoryVisitError<Failure>>,
        parent_abs: impl FnOnce() -> String,
    ) -> Result<Vec<String>, Failure> {
        match visited {
            Ok(_) => {}
            Err(DirectoryVisitError::Visitor(failure)) => return Err(failure),
            Err(DirectoryVisitError::EntryLimit | DirectoryVisitError::NameByteLimit) => {
                return refuse(WalkRefusal::ListingBound);
            }
            Err(DirectoryVisitError::Native(error)) => return refuse(WalkRefusal::HostIo(error)),
            Err(DirectoryVisitError::InvalidLimits) => {
                return refuse(WalkRefusal::HostIo(io::Error::new(
                    io::ErrorKind::InvalidInput,
                    "invalid listing limits",
                )));
            }
        }
        if let Some(raw) = self.invalid {
            return refuse(WalkRefusal::NameUnrepresentable {
                parent: parent_abs(),
                name: escaped(&raw),
            });
        }
        self.paths.sort();
        Ok(self.paths)
    }
}

/// What the walk observes and how; one per walk.
struct Walk<'r, 'a> {
    root: &'r DiscoveryRoot<'a>,
    /// The root's spelling, kept once: the core's handoff, terminal refusal
    /// details and the test-only trace.
    root_abs: String,
    uid: u32,
    groups: &'r BTreeSet<u32>,
    waiver: Option<&'r ProjectOwnerWaiver>,
    policy: &'r ProjectChainPolicy<'r>,
    automatic: bool,
    /// Keyed by root-relative path (unit B2-b3d).
    scope: ObservedScope,
    listed: BTreeSet<String>,
    /// Directory custody verdicts reached, by root-relative path (true
    /// passes).
    verdicts: BTreeMap<String, bool>,
    /// The admitted D15 member roots (M3-B r9 item 22; unit B3-b2a): not
    /// boundaries, entered as ordinary directories, with SX-1's `.opensip`
    /// anchor at each and their own `opensip.json` not a project boundary.
    members: &'r BTreeSet<String>,
}

/// One directory on the current path: its descriptor (the root's is lent)
/// and its root-relative path. No absolute spelling (unit B2-b3d).
struct Frame {
    dir: Option<RetainedDirectory>,
    rel: String,
}

/// A frame's descriptor: its own, or the lent root's.
fn dir_of<'f>(root: &'f RetainedDirectory, frame: &'f Frame) -> &'f RetainedDirectory {
    frame.dir.as_ref().unwrap_or(root)
}

/// One listed directory on the subtree stack: its frame, its depth below
/// the root, its children's root-relative paths with their observations
/// alongside, and the next child to visit.
struct Level {
    frame: Frame,
    depth: usize,
    paths: Vec<String>,
    observed: Vec<ChildObservation>,
    next: usize,
    pushed_cargo: bool,
}

/// How a named root's chain ended.
enum Chain {
    /// The named root, reached.
    Reached,
    /// A component that is not a directory (or is absent): the core's unit
    /// custody reports it.
    NotDirectory,
    /// A pruned prefix or a boundary: the core refuses the join before any
    /// custody.
    Refused,
}

fn is_file(observation: &ChildObservation) -> bool {
    matches!(
        observation,
        ChildObservation::Present {
            kind: ChildKind::File,
            ..
        }
    )
}

impl<'a> Walk<'_, 'a> {
    fn lent(&self) -> &'a RetainedDirectory {
        self.root.root()
    }
    fn premise(&self) -> Option<&AclOmissionPremise> {
        self.root.premise()
    }
    /// A root-relative path's absolute spelling: terminal refusals and the
    /// test-only trace only.
    fn spelled(&self, rel: &str) -> String {
        spelled(&self.root_abs, rel)
    }
    fn changed(&self, rel: &str) -> Failure {
        WorkFailure::Operation(WalkRefusal::Changed(self.spelled(rel)))
    }

    /// A child's root-relative key, charged as one owned record first.
    fn key(&self, dir: &str, name: &str, work: &mut WorkScope<'_>) -> Result<String, Failure> {
        work.charge::<WalkRefusal>(owned(dir.len() + 1 + name.len()))?;
        Ok(join_rel(dir, name))
    }

    /// One charged by-name observation of `rel` (named `name` in `parent`).
    /// A present entry joins the scope, its record and key charged first. A
    /// path already in the scope must be the same object (device, inode,
    /// kind), and still present: a path seen twice is never two objects (r2,
    /// Codex B2B3B-R1-RF-2).
    fn observe(
        &mut self,
        parent: &RetainedDirectory,
        name: &str,
        rel: &str,
        work: &mut WorkScope<'_>,
    ) -> Result<ChildObservation, Failure> {
        trace("observe", || self.spelled(rel));
        let observation = parent
            .observe_child_accounted(OsStr::new(name), work)
            .map_err(io_failure)?;
        match (self.scope.entries.get(rel), &observation) {
            (Some(seen), ChildObservation::Present { metadata, .. }) => {
                if !same_object(&seen.metadata, metadata) {
                    return Err(self.changed(rel));
                }
            }
            (Some(_), ChildObservation::Absent) => {
                return Err(self.changed(rel));
            }
            (None, ChildObservation::Present { metadata, .. }) => {
                work.charge::<WalkRefusal>(owned(
                    rel.len() + std::mem::size_of::<ObservedEntry>(),
                ))?;
                self.scope.entries.insert(
                    rel.to_owned(),
                    ObservedEntry {
                        metadata: metadata.clone(),
                        acl: ObservedAcl::NotObserved,
                        vcs: None,
                    },
                );
            }
            (None, ChildObservation::Absent) => {}
        }
        Ok(observation)
    }

    /// Open a child observed as a directory and compare it with that
    /// observation. Gone, a link or another kind now is a change.
    fn open_directory(
        &self,
        parent: &RetainedDirectory,
        name: &str,
        rel: &str,
        observation: &ChildObservation,
        work: &mut WorkScope<'_>,
    ) -> Result<RetainedDirectory, Failure> {
        trace("open", || self.spelled(rel));
        before_open(|| self.spelled(rel));
        let opened = work.run(
            opensip_platform::open_child_directory_cost(OsStr::new(name)),
            |_| Ok::<_, Failure>(parent.open_child_directory(OsStr::new(name))),
        )?;
        let directory = match opened {
            Ok(directory) => directory,
            Err(error)
                if matches!(
                    error.kind(),
                    io::ErrorKind::NotFound | io::ErrorKind::NotADirectory
                ) || error.raw_os_error() == Some(62) =>
            {
                return Err(self.changed(rel));
            }
            Err(error) => return refuse(WalkRefusal::HostIo(error)),
        };
        let sample = work.run(STATUS, |_| {
            opensip_platform::observe_descriptor_metadata(directory.as_file())
                .map_err(|error| WorkFailure::Operation(WalkRefusal::HostIo(error)))
        })?;
        if !observation.matches(&sample) {
            return Err(self.changed(rel));
        }
        Ok(directory)
    }

    /// One premise-applied ACL capture of an opened object, normalized
    /// (LD-B2B3-3): readable entries, an omission the premise admits as an
    /// empty list, or unreadable. The capture must be the object observed;
    /// its sample replaces the entry's metadata, so custody judges the
    /// metadata and ACL of one capture.
    fn capture(&mut self, file: &File, rel: &str, work: &mut WorkScope<'_>) -> Result<(), Failure> {
        trace("capture", || self.spelled(rel));
        let sample = opensip_platform::capture_descriptor_acl_accounted(file, work).map_err(
            |f| match f {
                WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
                WorkFailure::Operation(error) => {
                    WorkFailure::Operation(WalkRefusal::Capture(error))
                }
            },
        )?;
        let acl = match sample.acl_state() {
            CapturedAclState::Entries(count) => {
                work.charge::<WalkRefusal>(owned(
                    count.saturating_mul(std::mem::size_of::<opensip_platform::CapturedAclEntry>()),
                ))?;
                (0..count)
                    .map(|index| sample.entry(index))
                    .collect::<Option<Vec<_>>>()
                    .map_or(ObservedAcl::Unreadable, ObservedAcl::Entries)
            }
            CapturedAclState::NotReturned => {
                let admitted = match self.premise() {
                    Some(premise) => premise.admits(file, work).map_err(|f| match f {
                        WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
                        WorkFailure::Operation(error) => {
                            WorkFailure::Operation(WalkRefusal::Premise(error))
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
        let Some(entry) = self.scope.entries.get_mut(rel) else {
            return Err(self.changed(rel));
        };
        if !same_object(&entry.metadata, sample.metadata()) {
            return Err(self.changed(rel));
        }
        entry.metadata = sample.metadata().clone();
        entry.acl = acl;
        Ok(())
    }

    fn judged(
        &self,
        rel: &str,
        object: ProjectObject,
        waiver: Option<&ProjectOwnerWaiver>,
    ) -> EntryJudgment {
        judge_entry(
            self.scope.entries.get(rel),
            object,
            self.uid,
            self.groups,
            waiver,
        )
    }

    /// A directory's custody as the core judges it on a unit chain (with the
    /// waiver), memoized: the ACL is captured only when the metadata-only
    /// rejection passes (r2, Codex B2B3B-R1-RF-1).
    fn directory_passes(
        &mut self,
        dir: &RetainedDirectory,
        rel: &str,
        work: &mut WorkScope<'_>,
    ) -> Result<bool, Failure> {
        if let Some(&verdict) = self.verdicts.get(rel) {
            return Ok(verdict);
        }
        let mut judged = self.judged(rel, ProjectObject::Directory, self.waiver);
        if judged == EntryJudgment::NeedsAcl {
            self.capture(dir.as_file(), rel, work)?;
            judged = self.judged(rel, ProjectObject::Directory, self.waiver);
        }
        let verdict = judged == EntryJudgment::Passed;
        work.charge::<WalkRefusal>(owned(rel.len()))?;
        self.verdicts.insert(rel.to_owned(), verdict);
        Ok(verdict)
    }

    /// The markers of a unit whose chain passed (LD-B2B3-6): a marker is
    /// opened no-follow from its parent, compared with its observation and
    /// captured only when its metadata-only rejection passes, never waived.
    /// A FIFO, socket, device or link named as a marker, or a marker its
    /// owner or mode already refuses, is never opened and keeps
    /// `NotObserved`.
    fn capture_markers(
        &mut self,
        dir: &RetainedDirectory,
        rel: &str,
        work: &mut WorkScope<'_>,
    ) -> Result<(), Failure> {
        for marker in WORKSPACE_MARKERS {
            let path = self.key(rel, marker, work)?;
            if self.judged(&path, ProjectObject::ConfigurationFile, None) != EntryJudgment::NeedsAcl
            {
                continue;
            }
            trace("open", || self.spelled(&path));
            before_open(|| self.spelled(&path));
            let opened = work.run(RetainedDirectory::open_regular_cost(marker), |_| {
                Ok::<_, Failure>(dir.open_regular(marker))
            })?;
            let file = match opened {
                Ok(file) => file,
                Err(error)
                    if matches!(
                        error.kind(),
                        io::ErrorKind::NotFound | io::ErrorKind::InvalidInput
                    ) || error.raw_os_error() == Some(62) =>
                {
                    return Err(self.changed(&path));
                }
                Err(error) => return refuse(WalkRefusal::HostIo(error)),
            };
            let sample = work.run(STATUS, |_| {
                opensip_platform::observe_descriptor_metadata(&file)
                    .map_err(|error| WorkFailure::Operation(WalkRefusal::HostIo(error)))
            })?;
            let observed = self.scope.entries.get(&path).map(|e| &e.metadata);
            if !observed.is_some_and(|m| same_object(m, &sample)) {
                return Err(self.changed(&path));
            }
            self.capture(&file, &path, work)?;
        }
        Ok(())
    }

    /// The VCS evidence of a listed directory, from its listed children: the
    /// first present of `.git`, `.hg`, `.svn` and `.jj`, as B2-b3a records it
    /// upward (a `gitdir:` value only under S3 file custody).
    fn listed_vcs(
        &self,
        dir: &RetainedDirectory,
        rel: &str,
        paths: &[String],
        observed: &[ChildObservation],
        work: &mut WorkScope<'_>,
    ) -> Result<Option<ObservedVcs>, Failure> {
        for marker in VCS_MARKERS {
            let Some(index) = paths.iter().position(|p| last_segment(p) == marker) else {
                continue;
            };
            let ChildObservation::Present { kind, .. } = &observed[index] else {
                continue;
            };
            return Ok(Some(match kind {
                ChildKind::Directory => ObservedVcs::Directory,
                ChildKind::File if marker == ".git" => ObservedVcs::Indirection {
                    target: gitdir_target(
                        dir,
                        Path::new(rel),
                        &observed[index],
                        self.uid,
                        self.policy,
                        work,
                    )
                    .map_err(evidence_failure)?,
                },
                _ => ObservedVcs::Indirection { target: None },
            }));
        }
        Ok(None)
    }

    /// List one directory (LD-B2B3-5, LD-B2B3-2) in one pass (unit B2-b3d):
    /// charge the listing, then convert each name in the visitor; the stream
    /// is closed before any child is observed. Returns the children's
    /// root-relative paths, sorted.
    fn list(
        &mut self,
        dir: &RetainedDirectory,
        rel: &str,
        work: &mut WorkScope<'_>,
    ) -> Result<Vec<String>, Failure> {
        trace("list", || self.spelled(rel));
        work.charge::<WalkRefusal>(LISTING)?;
        let mut conversion = ListingConversion::new();
        let visited = dir.visit_entry_names(MAX_LISTED_ENTRIES, MAX_LISTED_NAME_BYTES, |name| {
            conversion.accept(rel, name, work)
        });
        conversion.finish(visited, || self.spelled(rel))
    }

    /// List one directory of a subtree and observe its children (the
    /// reference's `subtree` step): returns its level, or `None` when it was
    /// already listed. `ancestors` are the levels above it (the root's
    /// first, in automatic mode). In automatic mode a directory holding a
    /// regular marker is a unit: the core judges its chain below the root,
    /// in order, stopping at the first refusal, then its markers.
    fn enter(
        &mut self,
        ancestors: &[Level],
        start: Frame,
        known: &mut BTreeSet<String>,
        work: &mut WorkScope<'_>,
    ) -> Result<Option<Level>, Failure> {
        if self.listed.contains(&start.rel) {
            return Ok(None);
        }
        work.charge::<WalkRefusal>(owned(start.rel.len()))?;
        self.listed.insert(start.rel.clone());
        let lent = self.lent();
        let paths = self.list(dir_of(lent, &start), &start.rel, work)?;
        // The observations beside the paths, one slot per child: the whole
        // array is charged before it is reserved (r2, Codex B2B3D-R1-RF-1),
        // and the name is never copied again (unit B2-b3d, LD-B2B3D-4).
        work.charge::<WalkRefusal>(owned(
            paths
                .len()
                .saturating_mul(std::mem::size_of::<ChildObservation>()),
        ))?;
        let mut observed = Vec::with_capacity(paths.len());
        for path in &paths {
            let observation = self.observe(dir_of(lent, &start), last_segment(path), path, work)?;
            if observation == ChildObservation::Absent {
                return Err(self.changed(path));
            }
            observed.push(observation);
        }
        // Only the root can be listed while holding VCS evidence.
        if start.rel.is_empty() {
            let vcs = self.listed_vcs(dir_of(lent, &start), "", &paths, &observed, work)?;
            if let Some(entry) = self.scope.entries.get_mut("") {
                entry.vcs = vcs;
            }
        }
        let regular = |name: &str| {
            paths
                .iter()
                .zip(&observed)
                .any(|(p, o)| last_segment(p) == name && is_file(o))
        };
        let pushed_cargo = regular("Cargo.toml") && !known.contains(&start.rel);
        if pushed_cargo {
            work.charge::<WalkRefusal>(owned(start.rel.len()))?;
            known.insert(start.rel.clone());
        }
        if self.automatic && WORKSPACE_MARKERS.iter().any(|m| regular(m)) {
            let mut passes = true;
            for level in ancestors.iter().skip(1) {
                if !self.directory_passes(dir_of(lent, &level.frame), &level.frame.rel, work)? {
                    passes = false;
                    break;
                }
            }
            if passes && !start.rel.is_empty() {
                passes = self.directory_passes(dir_of(lent, &start), &start.rel, work)?;
            }
            if passes {
                self.capture_markers(dir_of(lent, &start), &start.rel, work)?;
            }
        }
        let depth = if start.rel.is_empty() {
            0
        } else {
            start.rel.split('/').count()
        };
        Ok(Some(Level {
            frame: start,
            depth,
            paths,
            observed,
            next: 0,
            pushed_cargo,
        }))
    }

    /// The four marker names of a directory past the depth policy, observed
    /// by name only.
    fn observe_markers(
        &mut self,
        dir: &RetainedDirectory,
        rel: &str,
        work: &mut WorkScope<'_>,
    ) -> Result<(), Failure> {
        for marker in WORKSPACE_MARKERS {
            let path = self.key(rel, marker, work)?;
            self.observe(dir, marker, &path, work)?;
        }
        Ok(())
    }

    /// The automatic rule from `start`, an ordinary directory already in the
    /// scope (the reference's `subtree`), depth first with the ancestors'
    /// descriptors retained on an explicit stack of levels (no recursion).
    /// `known` holds the Cargo roots on the current path.
    fn subtree(
        &mut self,
        start: Frame,
        known: &mut BTreeSet<String>,
        work: &mut WorkScope<'_>,
    ) -> Result<(), Failure> {
        let lent = self.lent();
        // The depth policy applies to the start too (r3, Codex
        // B2B3B-R2-RF-3): a named root of more than 256 segments is never
        // listed; only its four marker names are observed.
        if !start.rel.is_empty() && start.rel.split('/').count() > MAX_LISTED_DEPTH {
            return self.observe_markers(dir_of(lent, &start), &start.rel, work);
        }
        let mut levels: Vec<Level> = Vec::new();
        if let Some(level) = self.enter(&levels, start, known, work)? {
            levels.push(level);
        }
        while let Some(top) = levels.last_mut() {
            if top.next == top.paths.len() {
                let done = levels.pop().expect("the stack has a top level");
                if done.pushed_cargo {
                    known.remove(&done.frame.rel);
                }
                continue;
            }
            let index = top.next;
            top.next += 1;
            let ChildObservation::Present {
                kind: ChildKind::Directory,
                ..
            } = top.observed[index]
            else {
                continue;
            };
            // Each child is visited once: its owned path moves out of the
            // level, never copied (r3, Codex B2B3B-R2-RF-2).
            let rel = std::mem::take(&mut top.paths[index]);
            let observation = top.observed[index].clone();
            let depth = top.depth;
            work.charge::<WalkRefusal>(classify_cost(&rel))?;
            if let EntryDisposition::NeverEnter { .. } =
                rule::classify_entry(&rel, EntryKind::Directory, known, self.members)
            {
                // A pruned anchor: its own entry only, never opened.
                continue;
            }
            let parent = &levels.last().expect("the stack has a top level").frame;
            let name = last_segment(&rel);
            let child =
                self.open_directory(dir_of(lent, parent), name, &rel, &observation, work)?;
            if depth + 1 > MAX_LISTED_DEPTH {
                // A 257-segment directory: only its four marker names.
                self.observe_markers(&child, &rel, work)?;
                continue;
            }
            trace("probe", || self.spelled(&rel));
            let vcs = vcs_evidence(&child, Path::new(&rel), self.uid, self.policy, work)
                .map_err(evidence_failure)?;
            let config_path = self.key(&rel, CONFIG_FILE, work)?;
            let config = self.observe(&child, CONFIG_FILE, &config_path, work)?;
            // A member's VCS evidence and its own `opensip.json` make it
            // neither a repository nor a project boundary (item 22).
            let boundary = !self.members.contains(&rel) && (vcs.is_some() || is_file(&config));
            if let Some(entry) = self.scope.entries.get_mut(&rel) {
                entry.vcs = vcs;
            }
            if boundary {
                continue;
            }
            // The frame's own slot; its path moved in.
            work.charge::<WalkRefusal>(owned(0))?;
            let frame = Frame {
                dir: Some(child),
                rel,
            };
            if let Some(level) = self.enter(&levels, frame, known, work)? {
                levels.push(level);
            }
        }
        Ok(())
    }

    /// Explicit and config modes: one named root's chain, parent-first (the
    /// reference's chain walk), observing each chain directory's `Cargo.toml`,
    /// `opensip.json` and VCS evidence by name. A non-directory, a pruned
    /// prefix or a boundary stops it. With `judge`, the core's judgment of
    /// this join runs on the retained chain, in its order (r2, Codex
    /// B2B3B-R1-RF-1): a pruned prefix or a boundary refuses before any
    /// custody; otherwise each chain directory is judged from the root down,
    /// captured only past its metadata-only rejection, stopping at the first
    /// refusal; a reached root whose chain passed has its markers judged and
    /// captured. A reached root's subtree is then listed, its chain dropped
    /// first. Returns whether the core's judgment of the joins continues.
    fn named_root(
        &mut self,
        rel: &str,
        judge: bool,
        work: &mut WorkScope<'_>,
    ) -> Result<bool, Failure> {
        let lent = self.lent();
        // The root frame's own slot.
        work.charge::<WalkRefusal>(owned(0))?;
        let mut known = BTreeSet::new();
        let cargo_path = self.key("", "Cargo.toml", work)?;
        let cargo = self.observe(lent, "Cargo.toml", &cargo_path, work)?;
        let config_path = self.key("", CONFIG_FILE, work)?;
        self.observe(lent, CONFIG_FILE, &config_path, work)?;
        if is_file(&cargo) {
            work.charge::<WalkRefusal>(owned(0))?;
            known.insert(String::new());
        }
        let mut chain = vec![Frame {
            dir: None,
            rel: String::new(),
        }];
        let mut ended = Chain::Reached;
        if !rel.is_empty() {
            for part in rel.split('/') {
                let parent = chain.last().expect("the chain holds the root");
                let sub = self.key(&parent.rel, part, work)?;
                let observation = self.observe(dir_of(lent, parent), part, &sub, work)?;
                if !matches!(
                    observation,
                    ChildObservation::Present {
                        kind: ChildKind::Directory,
                        ..
                    }
                ) {
                    ended = Chain::NotDirectory;
                    break;
                }
                work.charge::<WalkRefusal>(classify_cost(&sub))?;
                if rule::classify_path(&sub, &known, self.members).is_some() {
                    ended = Chain::Refused;
                    break;
                }
                let next =
                    self.open_directory(dir_of(lent, parent), part, &sub, &observation, work)?;
                let cargo_path = self.key(&sub, "Cargo.toml", work)?;
                let cargo = self.observe(&next, "Cargo.toml", &cargo_path, work)?;
                let config_path = self.key(&sub, CONFIG_FILE, work)?;
                let config = self.observe(&next, CONFIG_FILE, &config_path, work)?;
                trace("probe", || self.spelled(&sub));
                let vcs = vcs_evidence(&next, Path::new(&sub), self.uid, self.policy, work)
                    .map_err(evidence_failure)?;
                let boundary = !self.members.contains(&sub) && (vcs.is_some() || is_file(&config));
                if let Some(entry) = self.scope.entries.get_mut(&sub) {
                    entry.vcs = vcs;
                }
                if boundary {
                    ended = Chain::Refused;
                    break;
                }
                if is_file(&cargo) {
                    work.charge::<WalkRefusal>(owned(sub.len()))?;
                    known.insert(sub.clone());
                }
                chain.push(Frame {
                    dir: Some(next),
                    rel: sub,
                });
            }
        }
        // The core refuses a join inside a pruned tree before any custody,
        // whether or not the pruned prefix is a directory, or present (r3,
        // Codex B2B3B-R2-RF-1).
        if judge && !rel.is_empty() && !matches!(ended, Chain::Refused) {
            work.charge::<WalkRefusal>(classify_cost(rel))?;
            if rule::classify_path(rel, &known, self.members).is_some() {
                ended = Chain::Refused;
            }
        }
        let mut continues = judge;
        if judge {
            continues = match ended {
                Chain::Refused => false,
                Chain::NotDirectory | Chain::Reached => {
                    // Unit custody: the root for `.`; otherwise each chain
                    // directory below it, then (for a stopped chain) the
                    // component that is not a directory, which refuses.
                    let mut passes = true;
                    let judged: Vec<usize> = if rel.is_empty() {
                        vec![0]
                    } else {
                        (1..chain.len()).collect()
                    };
                    for index in judged {
                        let frame = &chain[index];
                        if !self.directory_passes(dir_of(lent, frame), &frame.rel, work)? {
                            passes = false;
                            break;
                        }
                    }
                    if passes && matches!(ended, Chain::Reached) {
                        let start = chain.last().expect("the chain holds the named root");
                        self.observe_markers(dir_of(lent, start), &start.rel, work)?;
                        self.capture_markers(dir_of(lent, start), &start.rel, work)?;
                    }
                    passes && matches!(ended, Chain::Reached)
                }
            };
        }
        if matches!(ended, Chain::Reached) {
            let start = chain.pop().expect("the chain holds the named root");
            drop(chain);
            let mut known = known;
            self.subtree(start, &mut known, work)?;
        }
        Ok(continues)
    }
}

/// What the walk needs beyond the lent root: the unit source chosen before
/// traversal, the invoking user, the authorized groups and the typed owner
/// waiver (which the core applies to unit chains).
pub(crate) struct WalkRequest<'a> {
    pub(crate) source: &'a UnitSourceRequest,
    pub(crate) invoking_uid: u32,
    pub(crate) groups: &'a crate::grants::AuthorizedGroups,
    pub(crate) waiver: Option<&'a ProjectOwnerWaiver>,
    /// Admitted D15 member roots, root-relative (unit B3-b2a).
    pub(crate) member_roots: &'a BTreeSet<String>,
}

/// The S3 downward walk over a lent root: the observed scope the core
/// needs, keyed by root-relative path (unit B2-b3d). Charged to `work`
/// before every step.
pub(crate) fn walk(
    root: &DiscoveryRoot<'_>,
    request: &WalkRequest<'_>,
    work: &mut WorkScope<'_>,
) -> Result<ObservedScope, Failure> {
    let spelling = root.spelling();
    let Some(root_abs) = spelling.to_str() else {
        use std::os::unix::ffi::OsStrExt;
        return refuse(WalkRefusal::NameUnrepresentable {
            parent: String::new(),
            name: escaped(spelling.as_os_str().as_bytes()),
        });
    };
    // The root's spelling, kept once.
    work.charge::<WalkRefusal>(owned(root_abs.len()))?;
    let root_abs = root_abs.to_owned();
    set_trace_root(&root_abs);
    let home = |sample: &DescriptorFilesystem| root.is_home_filesystem(sample);
    let groups = request.groups.as_set();
    let policy = ProjectChainPolicy::new(root.premise(), &home, groups);
    let mut walk = Walk {
        root,
        root_abs,
        uid: request.invoking_uid,
        groups,
        waiver: request.waiver,
        policy: &policy,
        automatic: matches!(request.source, UnitSourceRequest::Automatic),
        scope: ObservedScope::default(),
        listed: BTreeSet::new(),
        verdicts: BTreeMap::new(),
        members: request.member_roots,
    };
    trace("observe", || walk.root_abs.clone());
    let sample = work.run(STATUS, |_| {
        opensip_platform::observe_descriptor_metadata(root.root().as_file())
            .map_err(|error| WorkFailure::Operation(WalkRefusal::HostIo(error)))
    })?;
    // The root's scope entry, keyed by the empty path.
    work.charge::<WalkRefusal>(owned(std::mem::size_of::<ObservedEntry>()))?;
    walk.scope.entries.insert(
        String::new(),
        ObservedEntry {
            metadata: sample,
            acl: ObservedAcl::NotObserved,
            vcs: None,
        },
    );
    match request.source {
        UnitSourceRequest::Automatic => {
            // The root frame's own slot.
            work.charge::<WalkRefusal>(owned(0))?;
            let start = Frame {
                dir: None,
                rel: String::new(),
            };
            walk.subtree(start, &mut BTreeSet::new(), work)?;
        }
        UnitSourceRequest::ExplicitJoins(paths)
        | UnitSourceRequest::ConfigWorkspaceRoots(paths) => {
            // The core judges the joins in order and stops at the first
            // refusal: over the cap, nothing is judged; a spec the grammar
            // refuses is not walked and ends the judgment.
            let mut judge = paths.len() <= rule::MAX_WORKSPACE_UNITS;
            let mut seen = BTreeSet::new();
            for spec in paths {
                work.charge::<WalkRefusal>(owned(spec.len()))?;
                let Ok(rel) = rule::normalize_explicit_root(spec) else {
                    judge = false;
                    continue;
                };
                if seen.contains(&rel) {
                    continue;
                }
                work.charge::<WalkRefusal>(owned(rel.len()))?;
                seen.insert(rel.clone());
                judge = walk.named_root(&rel, judge, work)?;
            }
        }
    }
    Ok(walk.scope)
}

/// The walk, then B2-b2's core over its scope (M3-B r5 item 13). An
/// uncaptured ACL the core reaches is the instrument fault, never a result.
pub(crate) fn discover_downward(
    root: &DiscoveryRoot<'_>,
    upward: UpwardProvenance,
    invocation: &DiscoveryInvocation<'_>,
    work: &mut WorkScope<'_>,
) -> Result<DiscoveryResultPending, Failure> {
    let request = WalkRequest {
        source: &invocation.source,
        invoking_uid: invocation.invoking_uid,
        groups: invocation.groups,
        waiver: invocation.waiver,
        member_roots: invocation.member_roots,
    };
    let scope = walk(root, &request, work)?;
    let root_abs = root
        .spelling()
        .to_str()
        .expect("the walk refused a root that is not UTF-8");
    discover_observed(&scope, root_abs, upward, invocation)
        .map_err(|fault| WorkFailure::Operation(WalkRefusal::Unobserved(fault)))
}

#[cfg(test)]
mod tests {
    include!("discovery_walk_tests.rs");
}
