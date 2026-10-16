// The native workspace observation (M3-B r9 items 19 to 24; unit B3-b2b2b,
// B3-b plan r2 amendment A3): what the D15 decision core
// (`workspace_declarations.rs`) observes below W, read from the lent
// discovery root on the discovery ledger, after the fence is released.
//
// Every directory is reached from W's retained descriptor by no-follow
// opens, segment by segment; a component that is absent, a link or not a
// directory reaches nothing. Every object seen is bound, by path, to one
// identity in the decision's binding table, which the walk and item 6b
// share (r2, Codex B3B2B2B-R1-RF-2 and RF-3): a later open, observation,
// capture or member walk of that path must be the same object, or the
// discovery fails with a change. A custody judgment's ACL is captured from
// the bound descriptor itself, exactly where the metadata-only judgment
// passes (as the walker captures, LD-B3B2B1-6); a capture refusal other than
// a change is the object's unreadable ACL, a custody verdict, never a latch.
// A carrier or manifest is read from the very descriptor its custody capture
// judged, bounded at 4 MiB, and its status and ACL are sampled again after
// the read and must equal the capture (RF-4). VCS markers are positive
// lookups; listings are converted as the walker converts them. Item 6b is one
// session per decision, begun at the first counted candidate under the
// handoff's proof; the member it admits must be the bound object, and its
// index gitlinks are returned as nested repositories (RF-1). Host I/O, a
// change and ledger exhaustion fail the discovery.
use super::discovery_scan::{EntryJudgment, ObservedAcl, ObservedEntry, judge_entry};
use super::discovery_walk::{
    LISTING, ListingConversion, MAX_LISTED_ENTRIES, MAX_LISTED_NAME_BYTES, STATUS, WalkRefusal,
    owned, same_object,
};
use super::git_tracking::{
    MemberInputs, MemberPath, MemberSession, MemberVerdict, NoRepository, TrackingRefusal,
};
use super::project_chain::{DiscoveryRoot, ProjectObject};
use super::workspace_declarations::{CARRIER_CAP, FileBytes, MemberOutcome, WorkspaceObservation};
use crate::grants::ProjectOwnerWaiver;
use opensip_platform::{
    CapturedAclState, ChildKind, ChildObservation, DescriptorAclCaptureError, DescriptorMetadata,
    RetainedDirectory, WorkFailure, WorkReadFailure, WorkScope,
};
use std::cell::RefCell;
use std::collections::{BTreeMap, BTreeSet};
use std::ffi::OsStr;
use std::fs::File;
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

/// The decision's object identities, by W-relative path (`""` is W), shared
/// by the native observation of each phase, the walk and item 6b.
pub(crate) type Bindings = RefCell<BTreeMap<String, DescriptorMetadata>>;

fn walk_failure(refusal: WalkRefusal) -> Failure {
    WorkFailure::Operation(WorkspaceRefusal::Walk(refusal))
}
fn changed(rel: &str) -> Failure {
    walk_failure(WalkRefusal::Changed(rel.to_owned()))
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
fn join(dir: &str, name: &str) -> String {
    if dir.is_empty() {
        name.to_owned()
    } else {
        format!("{dir}/{name}")
    }
}

// The test-only trace of every request the decision core makes and every
// platform operation this observation makes for it, with its W-relative
// path, and the test-only hook a race control uses to change the tree at a
// named point (unit B3-b2b2b's access and binding controls). Production
// carries nothing.
/// A race control's hook (test only).
#[cfg(test)]
pub(crate) type RaceHook = Box<dyn FnMut(&str, &str)>;
#[cfg(test)]
thread_local! {
    static TRACE: RefCell<Vec<(&'static str, String)>> = const { RefCell::new(Vec::new()) };
    static HOOK: RefCell<Option<RaceHook>> = const { RefCell::new(None) };
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
#[cfg(test)]
pub(crate) fn hook(point: &str, path: &str) {
    let taken = HOOK.with(|h| h.borrow_mut().take());
    if let Some(mut f) = taken {
        f(point, path);
        HOOK.with(|h| *h.borrow_mut() = Some(f));
    }
}
#[cfg(not(test))]
pub(crate) fn hook(_: &str, _: &str) {}
#[cfg(test)]
pub(crate) fn set_hook(f: Option<RaceHook>) {
    HOOK.with(|h| *h.borrow_mut() = f);
}

/// A component that is absent, a link (`ELOOP`) or not a directory.
fn unreachable(error: &io::Error) -> bool {
    matches!(
        error.kind(),
        io::ErrorKind::NotFound | io::ErrorKind::NotADirectory
    ) || error.raw_os_error() == Some(62)
}

/// Bind `rel` to `metadata`'s object, or check it is the object already
/// bound; a new binding is charged as one owned record.
pub(crate) fn bind(
    bound: &Bindings,
    work: &mut WorkScope<'_>,
    rel: &str,
    metadata: &DescriptorMetadata,
) -> Result<(), Failure> {
    let known = bound.borrow().get(rel).cloned();
    match known {
        Some(seen) if !same_object(&seen, metadata) => Err(changed(rel)),
        Some(_) => Ok(()),
        None => {
            work.charge::<WorkspaceRefusal>(owned(
                rel.len() + std::mem::size_of::<DescriptorMetadata>(),
            ))?;
            bound.borrow_mut().insert(rel.to_owned(), metadata.clone());
            Ok(())
        }
    }
}

/// The directory at `rel` (W for `""`), opened no-follow from W through the
/// reused `stack`, or `None` when a component is unreachable. Every directory
/// opened is bound (r2, Codex B3B2B2B-R1-RF-2); a retained one stays bound to
/// the object it is, so every later sighting of its path is checked against
/// it. A free function over the observation's fields, so the directory and
/// the ledger are borrowed apart.
fn directory<'d>(
    root: &'d RetainedDirectory,
    stack: &'d mut Vec<(String, RetainedDirectory)>,
    bound: &Bindings,
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
            Err(error) if unreachable(&error) => {
                if bound.borrow().contains_key(&path) {
                    return Err(changed(&path));
                }
                return Ok(None);
            }
            Err(error) => return Err(walk_failure(WalkRefusal::HostIo(error))),
        };
        let sample = work.run(STATUS, |_| {
            opensip_platform::observe_descriptor_metadata(child.as_file())
                .map_err(|error| walk_failure(WalkRefusal::HostIo(error)))
        })?;
        bind(bound, work, &path, &sample)?;
        stack.push((path, child));
    }
    Ok(stack.last().map(|(_, d)| d))
}

/// One premise-applied ACL capture of a bound object's descriptor, normalized
/// as the walker normalizes it: the entry with the capture's status and ACL.
/// A change fails; any other capture refusal is an unreadable ACL.
fn capture(
    root: &DiscoveryRoot<'_>,
    work: &mut WorkScope<'_>,
    file: &File,
    rel: &str,
    entry: &ObservedEntry,
) -> Result<ObservedEntry, Failure> {
    let captured =
        opensip_platform::capture_descriptor_acl_observed::<WorkspaceRefusal>(file, work)?;
    let sample = match captured {
        Ok(sample) => sample,
        Err(DescriptorAclCaptureError::Io(error)) => {
            return Err(walk_failure(WalkRefusal::HostIo(error)));
        }
        Err(DescriptorAclCaptureError::Changed) => return Err(changed(rel)),
        Err(_) => {
            return Ok(ObservedEntry {
                acl: ObservedAcl::Unreadable,
                ..entry.clone()
            });
        }
    };
    if !same_object(&entry.metadata, sample.metadata()) {
        return Err(changed(rel));
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
    Ok(ObservedEntry {
        metadata: sample.metadata().clone(),
        acl,
        vcs: None,
    })
}

/// Whether the core's judgment of `entry` as `object` would need its ACL.
fn needs_acl(
    uid: u32,
    groups: &BTreeSet<u32>,
    waiver: Option<&ProjectOwnerWaiver>,
    entry: &ObservedEntry,
    object: ProjectObject,
) -> bool {
    let waiver = if matches!(object, ProjectObject::Directory) {
        waiver
    } else {
        None
    };
    judge_entry(Some(entry), object, uid, groups, waiver) == EntryJudgment::NeedsAcl
}

/// Item 6b's inputs, under the handoff's proof (B3-b2b2a).
pub(crate) struct MemberObservation<'a> {
    pub(crate) inputs: &'a MemberInputs<'a>,
    pub(crate) proof: NoRepository<'a>,
}

/// The native observation of one decision phase.
pub(crate) struct NativeObservation<'r, 'w, 's> {
    root: &'r DiscoveryRoot<'r>,
    uid: u32,
    groups: &'r BTreeSet<u32>,
    waiver: Option<&'r ProjectOwnerWaiver>,
    members: Option<&'r MemberObservation<'r>>,
    session: Option<MemberSession<'r>>,
    work: &'w mut WorkScope<'s>,
    bound: &'r Bindings,
    /// Metadata-only entries, by W-relative path.
    seen: BTreeMap<String, Option<ObservedEntry>>,
    /// Custody entries, with their capture, by W-relative path.
    custodied: BTreeMap<String, Option<ObservedEntry>>,
    /// The regular files whose capture judged their custody, retained for
    /// their read (RF-4).
    files: BTreeMap<String, File>,
    /// Each file's validated read, for the core's repeated requests (r3,
    /// Codex B3B2B2B-R2-RF-3): charged once when kept, and each copy handed
    /// out charged again.
    read: BTreeMap<String, FileBytes>,
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
        bound: &'r Bindings,
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
            bound,
            seen: BTreeMap::new(),
            custodied: BTreeMap::new(),
            files: BTreeMap::new(),
            read: BTreeMap::new(),
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
            bind(self.bound, self.work, rel, &metadata)?;
            return Ok(Some(ObservedEntry {
                metadata,
                acl: ObservedAcl::NotObserved,
                vcs: None,
            }));
        }
        let (parent_rel, name) = rel.rsplit_once('/').unwrap_or(("", rel));
        let Some(parent) = directory(
            self.root.root(),
            &mut self.stack,
            self.bound,
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
        let metadata = match observation {
            ChildObservation::Absent => {
                if self.bound.borrow().contains_key(rel) {
                    return Err(changed(rel));
                }
                return Ok(None);
            }
            ChildObservation::Present { metadata, .. } => metadata,
        };
        bind(self.bound, self.work, rel, &metadata)?;
        self.work
            .charge::<WorkspaceRefusal>(owned(rel.len() + std::mem::size_of::<ObservedEntry>()))?;
        Ok(Some(ObservedEntry {
            metadata,
            acl: ObservedAcl::NotObserved,
            vcs: None,
        }))
    }

    /// The custody entry: the metadata-only entry, with its ACL captured
    /// from the bound descriptor where the judgment of `object` needs it.
    fn judged(
        &mut self,
        rel: &str,
        object: ProjectObject,
    ) -> Result<Option<ObservedEntry>, Failure> {
        hook("before-custody", rel);
        let Some(entry) = self.entry(rel)? else {
            return Ok(None);
        };
        if !needs_acl(self.uid, self.groups, self.waiver, &entry, object) {
            return Ok(Some(entry));
        }
        trace("open-capture", rel);
        let root = self.root;
        if entry.metadata.mode & 0o170000 == 0o040000 {
            let held = directory(root.root(), &mut self.stack, self.bound, self.work, rel)?
                .ok_or_else(|| changed(rel))?;
            let captured = capture(root, self.work, held.as_file(), rel, &entry)?;
            return Ok(Some(captured));
        }
        let (parent_rel, name) = rel.rsplit_once('/').unwrap_or(("", rel));
        let parent = directory(
            root.root(),
            &mut self.stack,
            self.bound,
            self.work,
            parent_rel,
        )?
        .ok_or_else(|| changed(rel))?;
        let opened = self
            .work
            .run(RetainedDirectory::open_regular_cost(name), |_| {
                Ok::<_, Failure>(parent.open_regular(name))
            })?;
        let file = match opened {
            Ok(file) => file,
            Err(error) if unreachable(&error) || error.kind() == io::ErrorKind::InvalidInput => {
                return Err(changed(rel));
            }
            Err(error) => return Err(walk_failure(WalkRefusal::HostIo(error))),
        };
        let captured = capture(root, self.work, &file, rel, &entry)?;
        self.files.insert(rel.to_owned(), file);
        Ok(Some(captured))
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
    fn custody_entry(
        &mut self,
        rel: &str,
        object: ProjectObject,
    ) -> Result<Option<ObservedEntry>, Failure> {
        trace("request-custody", rel);
        if let Some(entry) = self.custodied.get(rel) {
            return Ok(entry.clone());
        }
        let entry = self.judged(rel, object)?;
        self.custodied.insert(rel.to_owned(), entry.clone());
        Ok(entry)
    }
    fn markers(&mut self, rel: &str) -> Result<Vec<(&'static str, bool)>, Failure> {
        trace("request-markers", rel);
        let Some(held) = directory(
            self.root.root(),
            &mut self.stack,
            self.bound,
            self.work,
            rel,
        )?
        else {
            return Ok(Vec::new());
        };
        let mut found = Vec::new();
        for marker in super::project_admission::VCS_MARKERS {
            let path = join(rel, marker);
            trace("lookup-marker", &path);
            match held
                .observe_child_accounted(OsStr::new(marker), self.work)
                .map_err(host_io)?
            {
                ChildObservation::Absent => {}
                ChildObservation::Present { kind, metadata } => {
                    bind(self.bound, self.work, &path, &metadata)?;
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
            self.bound,
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
    /// The bytes of a file whose custody entry captured it, read from that
    /// very descriptor; its status and ACL are sampled again after the read
    /// and must equal the capture, or the discovery fails with a change
    /// (r2, Codex B3B2B2B-R1-RF-4). The read's outcome is a value until the
    /// checks finish.
    fn bytes(&mut self, rel: &str) -> Result<FileBytes, Failure> {
        trace("request-bytes", rel);
        if let Some(kept) = self.read.get(rel) {
            return copy_kept(kept, self.work);
        }
        let outcome = self.read_once(rel)?;
        if let FileBytes::Read(raw) = &outcome {
            self.work
                .charge::<WorkspaceRefusal>(owned(rel.len() + raw.len()))?;
        }
        self.read.insert(rel.to_owned(), outcome.clone());
        Ok(outcome)
    }
    fn member_verdict(&mut self, candidate: &str) -> Result<MemberOutcome, Failure> {
        trace("request-verdict", candidate);
        hook("before-verdict", candidate);
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
        let (verdict, identities) = session
            .observe_identified(&path, self.work)
            .map_err(tracking)?;
        // Every object item 6b opened is the object the decision bound at
        // that path, its ancestors and `M/.git` included; the others are
        // bound for every later observer (r3, Codex B3B2B2B-R2-RF-2).
        for (rel, metadata) in &identities {
            bind(
                self.bound,
                self.work,
                &String::from_utf8_lossy(rel),
                metadata,
            )?;
        }
        Ok(match verdict {
            MemberVerdict::Admitted { gitlinks } => MemberOutcome::Admitted {
                gitlinks: gitlinks
                    .into_iter()
                    .map(|g| String::from_utf8_lossy(&g).into_owned())
                    .collect(),
            },
            MemberVerdict::Refused(refusal) => MemberOutcome::Refused(refusal.subject()),
        })
    }
}

/// A kept read's copy for a repeated request, charged on the discovery
/// ledger before it is made (Codex B3B2B2B-R3-RF-1).
pub(super) fn copy_kept(kept: &FileBytes, work: &mut WorkScope<'_>) -> Result<FileBytes, Failure> {
    if let FileBytes::Read(raw) = kept {
        work.charge::<WorkspaceRefusal>(owned(raw.len()))?;
    }
    trace("copy-kept", "");
    Ok(kept.clone())
}

impl NativeObservation<'_, '_, '_> {
    fn read_once(&mut self, rel: &str) -> Result<FileBytes, Failure> {
        let judged = self
            .custodied
            .get(rel)
            .cloned()
            .flatten()
            .ok_or(WorkFailure::Operation(WorkspaceRefusal::Invariant(
                "bytes-before-custody",
            )))?;
        let file =
            self.files
                .remove(rel)
                .ok_or(WorkFailure::Operation(WorkspaceRefusal::Invariant(
                    "bytes-without-descriptor",
                )))?;
        hook("before-read", rel);
        trace("read", rel);
        let read = opensip_platform::read_bounded_observed::<WorkspaceRefusal>(
            &file,
            CARRIER_CAP,
            self.work,
        )?;
        hook("after-read", rel);
        let sample = self.work.run(STATUS, |_| {
            opensip_platform::observe_descriptor_metadata(&file)
                .map_err(|error| walk_failure(WalkRefusal::HostIo(error)))
        })?;
        let again = capture(self.root, self.work, &file, rel, &judged)?;
        if sample != judged.metadata || again.metadata != judged.metadata || again.acl != judged.acl
        {
            return Err(changed(rel));
        }
        match read {
            Ok(raw) => Ok(FileBytes::Read(raw)),
            Err(WorkReadFailure::Bound) => Ok(FileBytes::TooLarge),
            Err(WorkReadFailure::Io(error)) => Err(walk_failure(WalkRefusal::HostIo(error))),
            Err(other) => Err(walk_failure(WalkRefusal::HostIo(io::Error::other(
                format!("{other:?}"),
            )))),
        }
    }
}
