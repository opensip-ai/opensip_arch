// The native workspace observation (M3-B r9 items 19 to 24; unit B3-b2b2b,
// B3-b plan r2 amendment A3): what the D15 decision core
// (`workspace_declarations.rs`) observes below W, read from the lent
// discovery root on the discovery ledger, after the fence is released.
//
// Every directory is reached from W's retained descriptor by no-follow
// opens, segment by segment; a component that is absent, a link or not a
// directory reaches nothing. Each entry is one accounted by-name
// observation, memoized, so a path is one object for the whole decision: a
// later open of it must match. Its ACL is captured, with the omission
// premise, exactly where the metadata-only judgment passes (as the walker
// captures, LD-B3B2B1-6). A capture refusal other than a change is the
// object's unreadable ACL, a custody verdict, never a latch. VCS markers are
// positive lookups; listings are converted as the walker converts them; a
// carrier or manifest is read bounded at 4 MiB. Item 6b is one session per
// decision, begun at the first counted candidate under the handoff's proof.
// Host I/O, a change and ledger exhaustion fail the discovery.
use super::discovery_scan::{EntryJudgment, ObservedAcl, ObservedEntry, judge_entry};
use super::discovery_walk::{
    LISTING, ListingConversion, MAX_LISTED_ENTRIES, MAX_LISTED_NAME_BYTES, STATUS, WalkRefusal,
    owned, same_object,
};
use super::git_tracking::{
    MemberInputs, MemberPath, MemberSession, MemberVerdict, NoRepository, TrackingRefusal,
};
use super::project_chain::{DiscoveryRoot, ProjectObject};
use super::workspace_declarations::{CARRIER_CAP, FileBytes, WorkspaceObservation};
use crate::grants::ProjectOwnerWaiver;
use opensip_platform::{
    CapturedAclState, ChildKind, ChildObservation, DescriptorAclCaptureError, RetainedDirectory,
    WorkFailure, WorkReadFailure, WorkScope,
};
use std::collections::{BTreeMap, BTreeSet};
use std::ffi::OsStr;
use std::io;

/// Why the workspace observation failed the discovery.
#[derive(Debug)]
pub(crate) enum WorkspaceRefusal {
    /// The walker's refusals: host I/O, a change, a capture or premise
    /// failure, a listing bound or an unrepresentable listed name.
    Walk(WalkRefusal),
    /// Item 6b's pass failure (host I/O).
    Tracking(TrackingRefusal),
    /// The core asked for something it never asks for: an instrument fault.
    Invariant(&'static str),
}
impl WorkspaceRefusal {
    /// The discovery result's refusal and detail, for the walker's refusals
    /// that are discovery's; every other failure keeps its own row.
    pub(crate) fn discovery_refusal(
        &self,
    ) -> Option<(super::discovery_scan::DiscoveryRefusal, String)> {
        match self {
            Self::Walk(refusal) => refusal.discovery_refusal(),
            _ => None,
        }
    }
}
pub(crate) type Failure = WorkFailure<WorkspaceRefusal>;
fn walk_failure(refusal: WalkRefusal) -> Failure {
    WorkFailure::Operation(WorkspaceRefusal::Walk(refusal))
}
fn host_io(failure: WorkFailure<io::Error>) -> Failure {
    match failure {
        WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
        WorkFailure::Operation(error) => walk_failure(WalkRefusal::HostIo(error)),
    }
}
fn from_walk(failure: super::discovery_walk::Failure) -> Failure {
    match failure {
        WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
        WorkFailure::Operation(refusal) => walk_failure(refusal),
    }
}
// The test-only trace of every request the decision core makes and every
// platform operation this observation makes for it, with its W-relative path
// (unit B3-b2b2b's access control). Production carries nothing.
#[cfg(test)]
thread_local! {
    static TRACE: std::cell::RefCell<Vec<(&'static str, String)>> = const { std::cell::RefCell::new(Vec::new()) };
}
#[cfg(test)]
fn trace(op: &'static str, path: &str) {
    TRACE.with(|t| t.borrow_mut().push((op, path.to_owned())));
}
#[cfg(not(test))]
fn trace(_: &'static str, _: &str) {}
#[cfg(test)]
pub(crate) fn take_trace() -> Vec<(&'static str, String)> {
    TRACE.with(|t| std::mem::take(&mut *t.borrow_mut()))
}

/// A component that is absent, a link (`ELOOP`) or not a directory.
fn unreachable(error: &io::Error) -> bool {
    matches!(
        error.kind(),
        io::ErrorKind::NotFound | io::ErrorKind::NotADirectory
    ) || error.raw_os_error() == Some(62)
}

/// The directory at `rel` (W for `""`), opened no-follow from W through the
/// reused `stack`, or `None` when a component is unreachable. An opened
/// directory already observed must be that object. A free function over the
/// observation's fields, so the directory and the ledger are borrowed apart.
fn directory<'d>(
    root: &'d RetainedDirectory,
    stack: &'d mut Vec<(String, RetainedDirectory)>,
    seen: &BTreeMap<String, Option<ObservedEntry>>,
    work: &mut WorkScope<'_>,
    rel: &str,
) -> Result<Option<&'d RetainedDirectory>, Failure> {
    if rel.is_empty() {
        return Ok(Some(root));
    }
    let parts: Vec<&str> = rel.split('/').collect();
    let keep = stack
        .iter()
        .enumerate()
        .take_while(|(depth, (path, _))| {
            *depth < parts.len() && *path == parts[..=*depth].join("/")
        })
        .count();
    stack.truncate(keep);
    for depth in keep..parts.len() {
        let path = parts[..=depth].join("/");
        trace("open-directory", &path);
        let name = OsStr::new(parts[depth]);
        let parent = stack.last().map_or(root, |(_, d)| d);
        let opened = work.run(opensip_platform::open_child_directory_cost(name), |_| {
            Ok::<_, Failure>(parent.open_child_directory(name))
        })?;
        let child = match opened {
            Ok(child) => child,
            Err(error) if unreachable(&error) => return Ok(None),
            Err(error) => return Err(walk_failure(WalkRefusal::HostIo(error))),
        };
        let sample = work.run(STATUS, |_| {
            opensip_platform::observe_descriptor_metadata(child.as_file())
                .map_err(|error| walk_failure(WalkRefusal::HostIo(error)))
        })?;
        if let Some(Some(observed)) = seen.get(&path)
            && !same_object(&observed.metadata, &sample)
        {
            return Err(walk_failure(WalkRefusal::Changed(path)));
        }
        stack.push((path, child));
    }
    Ok(stack.last().map(|(_, d)| d))
}

/// One premise-applied ACL capture of an opened object (the walker's
/// normalization). A change fails; any other capture refusal is the
/// object's unreadable ACL.
fn capture(
    root: &DiscoveryRoot<'_>,
    work: &mut WorkScope<'_>,
    file: &std::fs::File,
    rel: &str,
    entry: &mut ObservedEntry,
) -> Result<(), Failure> {
    let captured =
        opensip_platform::capture_descriptor_acl_observed::<WorkspaceRefusal>(file, work)?;
    let sample = match captured {
        Ok(sample) => sample,
        Err(DescriptorAclCaptureError::Io(error)) => {
            return Err(walk_failure(WalkRefusal::HostIo(error)));
        }
        Err(DescriptorAclCaptureError::Changed) => {
            return Err(walk_failure(WalkRefusal::Changed(rel.to_owned())));
        }
        Err(_) => {
            entry.acl = ObservedAcl::Unreadable;
            return Ok(());
        }
    };
    if !same_object(&entry.metadata, sample.metadata()) {
        return Err(walk_failure(WalkRefusal::Changed(rel.to_owned())));
    }
    let acl = match sample.acl_state() {
        CapturedAclState::Entries(count) => {
            work.charge::<WorkspaceRefusal>(owned(
                count.saturating_mul(std::mem::size_of::<opensip_platform::CapturedAclEntry>()),
            ))?;
            (0..count)
                .map(|index| sample.entry(index))
                .collect::<Option<Vec<_>>>()
                .map_or(ObservedAcl::Unreadable, ObservedAcl::Entries)
        }
        CapturedAclState::NotReturned => {
            let admitted = match root.premise() {
                Some(premise) => premise
                    .admits(file, work)
                    .map_err(|failure| match failure {
                        WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
                        WorkFailure::Operation(error) => walk_failure(WalkRefusal::Premise(error)),
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
    Ok(())
}

/// Whether a judgment the core makes of `entry` would need its ACL: a
/// directory with or without the owner waiver, a regular file without.
fn needs_acl(
    uid: u32,
    groups: &BTreeSet<u32>,
    waiver: Option<&ProjectOwnerWaiver>,
    entry: &ObservedEntry,
) -> bool {
    let judged = |object, waiver| {
        judge_entry(Some(entry), object, uid, groups, waiver) == EntryJudgment::NeedsAcl
    };
    match entry.metadata.mode & 0o170000 {
        0o040000 => {
            judged(ProjectObject::Directory, None) || judged(ProjectObject::Directory, waiver)
        }
        0o100000 => judged(ProjectObject::ConfigurationFile, None),
        _ => false,
    }
}

/// Item 6b's inputs, under the handoff's proof (B3-b2b2a).
pub(crate) struct MemberObservation<'a> {
    pub(crate) inputs: &'a MemberInputs<'a>,
    pub(crate) proof: NoRepository<'a>,
}

/// The native observation of one decision.
pub(crate) struct NativeObservation<'r, 'w, 's> {
    root: &'r DiscoveryRoot<'r>,
    uid: u32,
    groups: &'r BTreeSet<u32>,
    waiver: Option<&'r ProjectOwnerWaiver>,
    members: Option<&'r MemberObservation<'r>>,
    session: Option<MemberSession<'r>>,
    work: &'w mut WorkScope<'s>,
    /// Every entry observed, by W-relative path: one object per path.
    seen: BTreeMap<String, Option<ObservedEntry>>,
    /// The directories last opened from W, in order (`""` is W, not kept).
    stack: Vec<(String, RetainedDirectory)>,
}
impl<'r, 'w, 's> NativeObservation<'r, 'w, 's> {
    pub(crate) fn new(
        root: &'r DiscoveryRoot<'r>,
        uid: u32,
        groups: &'r BTreeSet<u32>,
        waiver: Option<&'r ProjectOwnerWaiver>,
        members: Option<&'r MemberObservation<'r>>,
        work: &'w mut WorkScope<'s>,
    ) -> Self {
        Self {
            root,
            uid,
            groups,
            waiver,
            members,
            session: None,
            work,
            seen: BTreeMap::new(),
            stack: Vec::new(),
        }
    }

    fn observe(&mut self, rel: &str) -> Result<Option<ObservedEntry>, Failure> {
        if rel.is_empty() {
            let file = self.root.root().as_file();
            let metadata = self.work.run(STATUS, |_| {
                opensip_platform::observe_descriptor_metadata(file)
                    .map_err(|error| walk_failure(WalkRefusal::HostIo(error)))
            })?;
            let mut entry = ObservedEntry {
                metadata,
                acl: ObservedAcl::NotObserved,
                vcs: None,
            };
            if needs_acl(self.uid, self.groups, self.waiver, &entry) {
                capture(
                    self.root,
                    self.work,
                    self.root.root().as_file(),
                    rel,
                    &mut entry,
                )?;
            }
            return Ok(Some(entry));
        }
        let (parent_rel, name) = rel.rsplit_once('/').unwrap_or(("", rel));
        let Some(parent) = directory(
            self.root.root(),
            &mut self.stack,
            &self.seen,
            self.work,
            parent_rel,
        )?
        else {
            return Ok(None);
        };
        trace("observe", rel);
        let observation = parent
            .observe_child_accounted(OsStr::new(name), self.work)
            .map_err(host_io)?;
        let (kind, metadata) = match observation {
            ChildObservation::Absent => return Ok(None),
            ChildObservation::Present { kind, metadata } => (kind, metadata),
        };
        self.work
            .charge::<WorkspaceRefusal>(owned(rel.len() + std::mem::size_of::<ObservedEntry>()))?;
        let mut entry = ObservedEntry {
            metadata,
            acl: ObservedAcl::NotObserved,
            vcs: None,
        };
        if !needs_acl(self.uid, self.groups, self.waiver, &entry) {
            return Ok(Some(entry));
        }
        trace("open-capture", rel);
        let changed = || walk_failure(WalkRefusal::Changed(rel.to_owned()));
        if kind == ChildKind::Directory {
            let opened = self.work.run(
                opensip_platform::open_child_directory_cost(OsStr::new(name)),
                |_| Ok::<_, Failure>(parent.open_child_directory(OsStr::new(name))),
            )?;
            let child = match opened {
                Ok(child) => child,
                Err(error) if unreachable(&error) => return Err(changed()),
                Err(error) => return Err(walk_failure(WalkRefusal::HostIo(error))),
            };
            let captured = capture(self.root, self.work, child.as_file(), rel, &mut entry);
            captured?;
        } else {
            let opened = self
                .work
                .run(RetainedDirectory::open_regular_cost(name), |_| {
                    Ok::<_, Failure>(parent.open_regular(name))
                })?;
            let file = match opened {
                Ok(file) => file,
                Err(error)
                    if unreachable(&error) || error.kind() == io::ErrorKind::InvalidInput =>
                {
                    return Err(changed());
                }
                Err(error) => return Err(walk_failure(WalkRefusal::HostIo(error))),
            };
            capture(self.root, self.work, &file, rel, &mut entry)?;
        }
        Ok(Some(entry))
    }
}

impl WorkspaceObservation for NativeObservation<'_, '_, '_> {
    type Error = Failure;
    fn entry(&mut self, rel: &str) -> Result<Option<ObservedEntry>, Failure> {
        trace("request-entry", rel);
        if let Some(entry) = self.seen.get(rel) {
            return Ok(entry.clone());
        }
        let entry = self.observe(rel)?;
        self.seen.insert(rel.to_owned(), entry.clone());
        Ok(entry)
    }
    fn markers(&mut self, rel: &str) -> Result<Vec<(&'static str, bool)>, Failure> {
        trace("request-markers", rel);
        let Some(directory) = directory(
            self.root.root(),
            &mut self.stack,
            &self.seen,
            self.work,
            rel,
        )?
        else {
            return Ok(Vec::new());
        };
        let mut found = Vec::new();
        for marker in super::project_admission::VCS_MARKERS {
            trace(
                "lookup-marker",
                &if rel.is_empty() {
                    marker.to_owned()
                } else {
                    format!("{rel}/{marker}")
                },
            );
            match directory
                .observe_child_accounted(OsStr::new(marker), self.work)
                .map_err(host_io)?
            {
                ChildObservation::Absent => {}
                ChildObservation::Present { kind, .. } => {
                    found.push((marker, kind == ChildKind::Directory))
                }
            }
        }
        Ok(found)
    }
    fn children(&mut self, rel: &str) -> Result<Vec<String>, Failure> {
        trace("request-children", rel);
        self.work.charge::<WorkspaceRefusal>(LISTING)?;
        let spelled = self.root.spelling().to_string_lossy().into_owned();
        let Some(listed) = directory(
            self.root.root(),
            &mut self.stack,
            &self.seen,
            self.work,
            rel,
        )?
        else {
            return Ok(Vec::new());
        };
        trace("list", rel);
        let mut conversion = ListingConversion::new();
        let work = &mut *self.work;
        let visited = listed.visit_entry_names(MAX_LISTED_ENTRIES, MAX_LISTED_NAME_BYTES, |name| {
            conversion.accept(rel, name, work)
        });
        let paths = conversion
            .finish(visited, || format!("{spelled}/{rel}"))
            .map_err(from_walk)?;
        Ok(paths
            .into_iter()
            .map(|p| p.rsplit('/').next().unwrap_or_default().to_owned())
            .collect())
    }
    fn bytes(&mut self, rel: &str) -> Result<FileBytes, Failure> {
        trace("request-bytes", rel);
        let seen = self
            .seen
            .get(rel)
            .cloned()
            .flatten()
            .ok_or(WorkFailure::Operation(WorkspaceRefusal::Invariant(
                "bytes-before-entry",
            )))?;
        let (parent_rel, name) = rel.rsplit_once('/').unwrap_or(("", rel));
        let Some(parent) = directory(
            self.root.root(),
            &mut self.stack,
            &self.seen,
            self.work,
            parent_rel,
        )?
        else {
            return Err(walk_failure(WalkRefusal::Changed(rel.to_owned())));
        };
        trace("read", rel);
        let opened = self
            .work
            .run(RetainedDirectory::open_regular_cost(name), |_| {
                Ok::<_, Failure>(parent.open_regular(name))
            })?;
        let file = match opened {
            Ok(file) => file,
            Err(error) if unreachable(&error) || error.kind() == io::ErrorKind::InvalidInput => {
                return Err(walk_failure(WalkRefusal::Changed(rel.to_owned())));
            }
            Err(error) => return Err(walk_failure(WalkRefusal::HostIo(error))),
        };
        let sample = self.work.run(STATUS, |_| {
            opensip_platform::observe_descriptor_metadata(&file)
                .map_err(|error| walk_failure(WalkRefusal::HostIo(error)))
        })?;
        if !same_object(&seen.metadata, &sample) {
            return Err(walk_failure(WalkRefusal::Changed(rel.to_owned())));
        }
        match opensip_platform::read_bounded_observed::<WorkspaceRefusal>(
            &file,
            CARRIER_CAP,
            self.work,
        )? {
            Ok(raw) => Ok(FileBytes::Read(raw)),
            Err(WorkReadFailure::Bound) => Ok(FileBytes::TooLarge),
            Err(WorkReadFailure::Io(error)) => Err(walk_failure(WalkRefusal::HostIo(error))),
            Err(other) => Err(walk_failure(WalkRefusal::HostIo(io::Error::other(
                format!("{other:?}"),
            )))),
        }
    }
    fn member_verdict(&mut self, candidate: &str) -> Result<Option<String>, Failure> {
        trace("request-verdict", candidate);
        let members = self
            .members
            .ok_or(WorkFailure::Operation(WorkspaceRefusal::Invariant(
                "member-verdict-without-precondition",
            )))?;
        let path = MemberPath::new(candidate.as_bytes()).ok_or(WorkFailure::Operation(
            WorkspaceRefusal::Invariant("member-path"),
        ))?;
        let tracking = |failure: super::git_tracking::Failure| match failure {
            WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
            WorkFailure::Operation(refusal) => {
                WorkFailure::Operation(WorkspaceRefusal::Tracking(refusal))
            }
        };
        if self.session.is_none() {
            self.session = Some(
                MemberSession::begin(members.inputs, members.proof, self.work).map_err(tracking)?,
            );
        }
        let session = self.session.as_ref().expect("begun above");
        Ok(match session.observe(&path, self.work).map_err(tracking)? {
            MemberVerdict::Admitted { .. } => None,
            MemberVerdict::Refused(refusal) => Some(refusal.subject()),
        })
    }
}
