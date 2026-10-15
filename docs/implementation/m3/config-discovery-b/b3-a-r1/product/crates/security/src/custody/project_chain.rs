// Law X2 r5 items 1 to 3, the custody half of item 4, and item 9 (unit X2a):
// the project chain walk. One retained, no-follow, charged walk from `/` to a
// selected project root, judged in three bands:
// - `/` through H, exactly as 468 r5 step 0 judges it (the external ancestor
//   predicate, with this invocation's omission premise under 465 item 4's
//   scope);
// - each directory strictly between H and the root, by the same external
//   ancestor predicate, with the same premise (item 1's widened scope);
// - the root, by S3's directory custody: owner is the invoking user or root,
//   no other-write, no group-write or ACL write grant except for an explicit
//   `--trust-group` gid, and an ACL that is readable or omitted under the
//   premise.
// From H down, every directory must be on H's own volume (item 1). The root
// must be strictly below H and outside `H/Library/Application Support/OpenSIP`
// (item 2), judged before any open. The root's native birth is sampled with
// the existing sampler, charged first, with no mtime or ctime substitute
// (item 4). Nothing is created or written. S3 selection, the registry read,
// `ProjectRootAdmission`, tracking and every public row are X2b's; this unit
// gives each refusal its item 8 row and subject for X2b to project. Library
// only.
use super::installation_root::{ParentRefusal, judge_ancestor};
use crate::grants::AuthorizedGroups;
use crate::trust::AclOmissionPremise;
use opensip_platform::{
    CapturedAclPrincipal, CapturedAclState, DescriptorAclCaptureError, DescriptorFilesystem,
    DirectoryBirthObservation, RetainedDirectory, RetainedDirectoryPath, WorkCost, WorkFailure,
    WorkScope,
};
use std::collections::BTreeSet;
use std::io;
use std::os::unix::ffi::OsStrExt;
use std::path::{Path, PathBuf};

/// Item 9: S3's selection walk is at most 256 levels; the retained chain from
/// `/` to the selected root is held to the same bound.
pub(crate) const MAX_PROJECT_COMPONENTS: usize = 256;

/// The fixed installation suffix below H that no project root may enter
/// (item 2). Compared ASCII-case-insensitively, as APFS resolves names.
const INSTALLATION_PARENT: [&str; 3] = ["Library", "Application Support", "OpenSIP"];

/// The placement judgment: a bounded byte comparison of the two paths. It
/// allocates nothing (component iterators over the borrowed bytes), so it
/// is one edge plus the bytes it reads.
fn placement_cost(home: &Path, root: &Path) -> WorkCost {
    WorkCost {
        objects: 0,
        edges: 1,
        bytes: home.as_os_str().len().saturating_add(root.as_os_str().len()),
    }
}
/// The retained spelling: one owned copy of the root's path bytes.
fn spelling_cost(root: &Path) -> WorkCost {
    WorkCost {
        objects: 1,
        edges: 0,
        bytes: root.as_os_str().len(),
    }
}
/// The birth identity (item 4): device, inode and native birth only. The
/// sample's other metadata (mtime, ctime, link count, size, mode) changes
/// lawfully, for example when `.opensip` is created, and is never part of it.
fn same_birth(a: &DirectoryBirthObservation, b: &DirectoryBirthObservation) -> bool {
    a.metadata().device == b.metadata().device
        && a.metadata().inode == b.metadata().inode
        && a.birth_seconds() == b.birth_seconds()
        && a.birth_nanoseconds() == b.birth_nanoseconds()
}
/// One native birth sample: a status read before and after, and the
/// `fgetattrlist` between them, each with its buffer.
const BIRTH_COST: WorkCost = WorkCost {
    objects: 0,
    edges: 3,
    bytes: 3 * 512,
};

/// What the walk borrows: this invocation's omission premise (from the read
/// or write receipt, never built by a caller), the check that a filesystem
/// is H's, and the explicit `--trust-group` set for the root's group and ACL
/// grants. It adds nothing to either receipt's lending.
pub(crate) struct ProjectChainPolicy<'a> {
    premise: Option<&'a AclOmissionPremise>,
    home_filesystem: &'a dyn Fn(&DescriptorFilesystem) -> bool,
    trust_groups: &'a BTreeSet<u32>,
}
impl<'a> ProjectChainPolicy<'a> {
    /// The check that a filesystem is H's.
    pub(crate) fn home_filesystem(&self) -> &'a dyn Fn(&DescriptorFilesystem) -> bool {
        self.home_filesystem
    }
    pub(crate) fn new(
        premise: Option<&'a AclOmissionPremise>,
        home_filesystem: &'a dyn Fn(&DescriptorFilesystem) -> bool,
        trust_groups: &'a BTreeSet<u32>,
    ) -> Self {
        Self {
            premise,
            home_filesystem,
            trust_groups,
        }
    }
    /// The same policy with the trust groups taken from the invocation's
    /// typed `--trust-group` record (M3-B r5 item 23).
    #[allow(dead_code)]
    pub(crate) fn from_grants(
        premise: Option<&'a AclOmissionPremise>,
        home_filesystem: &'a dyn Fn(&DescriptorFilesystem) -> bool,
        groups: &'a AuthorizedGroups,
    ) -> Self {
        Self::new(premise, home_filesystem, groups.as_set())
    }
}

/// Why the walk refused. Each variant has exactly one item 8 row (`row`).
#[derive(Debug)]
pub(crate) enum ProjectChainRefusal {
    /// The path is not an absolute raw POSIX spelling within the bound, or
    /// does not resolve to a directory.
    PathInvalid(io::Error),
    /// Item 2: not strictly below H, or inside the installation's parent.
    OutsideHome,
    /// A component is a symbolic link (`ELOOP`). macOS reports a no-follow
    /// directory open of a link as `ENOTDIR`, which is `PathInvalid`; both
    /// refuse.
    Symlink,
    /// `/` through the last directory above the root (the external ancestor
    /// band), as the shared 468 step 0 judgment reports it.
    Chain(ParentRefusal),
    /// The root failed S3's directory custody.
    Root(crate::custody::Refusal),
    /// The root's ACL was omitted and no premise admitted it.
    RootAclOmitted,
    RootCapture(DescriptorAclCaptureError),
    /// A directory from H down is not on H's own volume (`component` counts
    /// from `/` as 0).
    VolumeUnsupported { component: usize },
    /// The root's native birth is unsupported or unreliable.
    BirthUnsupported(io::Error),
    /// A retained name, identity or birth no longer matches.
    Changed,
    Io(io::Error),
}

/// Item 8's row for a refusal, for X2b to project through 468 item 6.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum ProjectChainRow {
    /// `PROJECT.ROOT_CUSTODY_REFUSED`, with this subject.
    RootCustody(&'static str),
    /// `PROJECT.EXPLICIT_PATH_INVALID` (S3).
    ExplicitPath,
    /// The host I/O row.
    HostIo,
}
fn refusal_subject(refusal: crate::custody::Refusal) -> &'static str {
    use crate::custody::Refusal as R;
    match refusal {
        R::ForeignOwner => "foreign-owner",
        R::OthersWrite | R::GroupWrite => "mode",
        R::AclUnreadable => "acl-unreadable",
        R::AclWrite => "acl-write",
        R::Symlink => "symlink",
        R::NotDirectory | R::NotRegular => "not-a-directory",
        R::Absent | R::HardLinked | R::Unlinked | R::TooLarge => "custody",
    }
}
fn capture_row(error: &DescriptorAclCaptureError) -> ProjectChainRow {
    match error {
        DescriptorAclCaptureError::Io(_) => ProjectChainRow::HostIo,
        DescriptorAclCaptureError::Unsupported
        | DescriptorAclCaptureError::Malformed(_)
        | DescriptorAclCaptureError::Changed => ProjectChainRow::RootCustody("acl-unreadable"),
    }
}
impl ProjectChainRefusal {
    pub(crate) fn row(&self) -> ProjectChainRow {
        use ProjectChainRow as Row;
        match self {
            Self::PathInvalid(_) => Row::ExplicitPath,
            Self::OutsideHome => Row::RootCustody("outside-home"),
            Self::Symlink => Row::RootCustody("symlink"),
            Self::Chain(parent) => match parent {
                ParentRefusal::Ancestor { refusal, .. } => Row::RootCustody(refusal_subject(*refusal)),
                ParentRefusal::AncestorAclOmitted { .. } => Row::RootCustody("acl-unreadable"),
                ParentRefusal::Capture { error, .. } => capture_row(error),
                ParentRefusal::NameChanged => Row::RootCustody("name-changed"),
                // The judgment reports only the variants above; any other is
                // an I/O sample failure (`Filesystem`, `NameObservation`).
                _ => Row::HostIo,
            },
            Self::Root(refusal) => Row::RootCustody(refusal_subject(*refusal)),
            Self::RootAclOmitted => Row::RootCustody("acl-unreadable"),
            Self::RootCapture(error) => capture_row(error),
            Self::VolumeUnsupported { .. } => Row::RootCustody("volume-unsupported"),
            Self::BirthUnsupported(_) => Row::RootCustody("birth-unsupported"),
            Self::Changed => Row::RootCustody("name-changed"),
            Self::Io(_) => Row::HostIo,
        }
    }
}
pub(super) type Failure = WorkFailure<ProjectChainRefusal>;
fn refuse<T>(refusal: ProjectChainRefusal) -> Result<T, Failure> {
    Err(WorkFailure::Operation(refusal))
}
fn lift<E>(
    wrap: impl FnOnce(E) -> ProjectChainRefusal,
) -> impl FnOnce(WorkFailure<E>) -> Failure {
    move |failure| match failure {
        WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
        WorkFailure::Operation(error) => WorkFailure::Operation(wrap(error)),
    }
}

/// The retained chain from `/` to an admitted project root. Private, not
/// Clone, not serializable. It holds the retained descriptors, the path
/// exactly as walked, H's position in it, and the root's native birth sample.
/// It grants nothing: X2b joins it with the registry and tracking.
pub(crate) struct ProjectChain {
    path: RetainedDirectoryPath,
    spelling: PathBuf,
    home_components: usize,
    birth: DirectoryBirthObservation,
}
impl std::fmt::Debug for ProjectChain {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("ProjectChain").finish_non_exhaustive()
    }
}
impl ProjectChain {
    /// The retained project root.
    pub(crate) fn root(&self) -> &RetainedDirectory {
        self.path.directory()
    }
    /// The canonical path bytes, exactly as walked (never normalized).
    pub(crate) fn spelling(&self) -> &Path {
        &self.spelling
    }
    /// The root's native birth, sampled from the retained root descriptor.
    pub(crate) fn birth(&self) -> &DirectoryBirthObservation {
        &self.birth
    }
    /// The retained chain from `/` to the root.
    pub(crate) fn path(&self) -> &RetainedDirectoryPath {
        &self.path
    }
    /// H's retained component index (0 is `/`).
    pub(crate) fn home_index(&self) -> usize {
        self.home_components
    }
    /// The number of directories strictly between H and the root.
    pub(crate) fn below_home(&self) -> usize {
        self.path.component_count() - self.home_components - 1
    }
    /// The chain's part of the held-fence recheck set (item 3): every name
    /// again, every custody judgment again, every volume check again, and the
    /// root's birth sampled again and compared. Charged to `work`.
    pub(crate) fn recheck(
        &self,
        uid: u32,
        policy: &ProjectChainPolicy<'_>,
        work: &mut WorkScope<'_>,
    ) -> Result<(), Failure> {
        names(&self.path, work)?;
        judge(&self.path, self.home_components, uid, policy, work)?;
        names(&self.path, work)?;
        let birth = sample_birth(self.root(), work)?;
        if !same_birth(&birth, &self.birth) {
            return refuse(ProjectChainRefusal::Changed);
        }
        Ok(())
    }
}

/// Item 2, lexically and before any open: the root is strictly below H by
/// exact component spelling, and its first components below H are not the
/// installation's parent suffix. Returns H's component count.
fn placement(home: &Path, root: &Path) -> Result<usize, ProjectChainRefusal> {
    // Components of an absolute spelling, borrowed; `None` marks a bad one.
    fn parts(path: &Path) -> Option<impl Iterator<Item = Option<&[u8]>> + Clone> {
        let raw = path.as_os_str().as_bytes();
        let rest = raw.strip_prefix(b"/")?;
        Some(
            rest.split(|b| *b == b'/')
                .filter(move |_| !rest.is_empty())
                .map(|part| (!part.is_empty() && part != b"." && part != b"..").then_some(part)),
        )
    }
    let invalid = || {
        ProjectChainRefusal::PathInvalid(io::Error::new(
            io::ErrorKind::InvalidInput,
            "project root is not an absolute raw POSIX path",
        ))
    };
    let home_parts = parts(home).ok_or_else(invalid)?;
    let root_parts = parts(root).ok_or_else(invalid)?;
    if home_parts.clone().any(|p| p.is_none()) || root_parts.clone().any(|p| p.is_none()) {
        return Err(invalid());
    }
    let home_count = home_parts.clone().count();
    let root_count = root_parts.clone().count();
    if root_count <= home_count || !home_parts.clone().zip(root_parts.clone()).all(|(h, r)| h == r) {
        return Err(ProjectChainRefusal::OutsideHome);
    }
    let below = root_count - home_count;
    let inside_installation_parent = below >= INSTALLATION_PARENT.len()
        && INSTALLATION_PARENT
            .iter()
            .zip(root_parts.skip(home_count))
            .all(|(fixed, part)| part.is_some_and(|p| p.eq_ignore_ascii_case(fixed.as_bytes())));
    if inside_installation_parent {
        return Err(ProjectChainRefusal::OutsideHome);
    }
    Ok(home_count)
}

/// Items 1 to 3: walk and judge the chain from `/` to `root`, where H is
/// `home`, the actor's admitted home. Charged to `work` before every step.
/// Nothing is created or written.
pub(crate) fn walk_project_chain(
    home: &Path,
    root: &Path,
    uid: u32,
    policy: &ProjectChainPolicy<'_>,
    work: &mut WorkScope<'_>,
) -> Result<ProjectChain, Failure> {
    let home_components = work.run(placement_cost(home, root), |_| {
        placement(home, root).map_err(WorkFailure::Operation)
    })?;
    let path = work.run(opensip_platform::retained_path_open_cost(root), |_| {
        RetainedDirectoryPath::open_project_root(root, MAX_PROJECT_COMPONENTS)
            .map_err(|error| WorkFailure::Operation(open_refusal(error)))
    })?;
    judge(&path, home_components, uid, policy, work)?;
    names(&path, work)?;
    let birth = sample_birth(path.directory(), work)?;
    let spelling = work.run(spelling_cost(root), |_| Ok(root.to_path_buf()))?;
    Ok(ProjectChain {
        path,
        spelling,
        home_components,
        birth,
    })
}

pub(super) fn open_refusal(error: io::Error) -> ProjectChainRefusal {
    // macOS `ELOOP`: O_NOFOLLOW met a symbolic link.
    const ELOOP: i32 = 62;
    if error.raw_os_error() == Some(ELOOP) {
        return ProjectChainRefusal::Symlink;
    }
    match error.kind() {
        io::ErrorKind::NotFound | io::ErrorKind::NotADirectory | io::ErrorKind::InvalidInput => {
            ProjectChainRefusal::PathInvalid(error)
        }
        _ => ProjectChainRefusal::Io(error),
    }
}

/// Every retained name still matches its descriptor, and the chain from `/`
/// still resolves to the same identities.
fn names(path: &RetainedDirectoryPath, work: &mut WorkScope<'_>) -> Result<(), Failure> {
    if path
        .recheck_exact_names_accounted(work)
        .map_err(lift(ProjectChainRefusal::Io))?
    {
        Ok(())
    } else {
        refuse(ProjectChainRefusal::Changed)
    }
}

/// The three bands of the module comment, root to leaf.
fn judge(
    path: &RetainedDirectoryPath,
    home_components: usize,
    uid: u32,
    policy: &ProjectChainPolicy<'_>,
    work: &mut WorkScope<'_>,
) -> Result<(), Failure> {
    let leaf = path.component_count();
    path.visit_directories(|component, directory| {
        if component < leaf {
            judge_ancestor(component, directory.as_file(), uid, policy.premise, work)
                .map_err(lift(ProjectChainRefusal::Chain))?;
        } else {
            judge_root(directory, uid, policy, work)?;
        }
        if component >= home_components {
            volume(component, directory, policy, work)?;
        }
        Ok(())
    })
}

/// From H down, the directory must be on H's own volume (item 1).
fn volume(
    component: usize,
    directory: &RetainedDirectory,
    policy: &ProjectChainPolicy<'_>,
    work: &mut WorkScope<'_>,
) -> Result<(), Failure> {
    let sample = opensip_platform::observe_filesystem_accounted(directory.as_file(), work)
        .map_err(lift(ProjectChainRefusal::Io))?;
    if (policy.home_filesystem)(&sample) {
        Ok(())
    } else {
        refuse(ProjectChainRefusal::VolumeUnsupported { component })
    }
}

/// S3's directory custody for the root, from one bounded ACL capture. An
/// omitted ACL is judged as a present empty ACL only when the premise admits
/// this descriptor (its own `fstatfs`).
fn judge_root(
    directory: &RetainedDirectory,
    uid: u32,
    policy: &ProjectChainPolicy<'_>,
    work: &mut WorkScope<'_>,
) -> Result<(), Failure> {
    judge_project_object(directory.as_file(), ProjectObject::Directory, uid, policy, work)
}

/// What a project object is judged as: S3 directory custody, or S3 config
/// file custody (a regular file, one link, at most 4 MiB). Item 1 puts both
/// in the premise's scope (`.opensip/` and the S3 config file, unit X2b).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum ProjectObject {
    Directory,
    ConfigurationFile,
}

/// S3 custody of one project object from one bounded ACL capture, with the
/// premise applied to an omitted ACL through the object's own `fstatfs`.
pub(crate) fn judge_project_object(
    file: &std::fs::File,
    object: ProjectObject,
    uid: u32,
    policy: &ProjectChainPolicy<'_>,
    work: &mut WorkScope<'_>,
) -> Result<(), Failure> {
    judge_project_object_sampled(file, object, uid, policy, work).map(|_| ())
}

/// `judge_project_object`, also returning the full metadata sample the
/// judgment passed on (M3-B unit B1-b: a carrier capture binds to it). The
/// same capture and checks, so the same charges.
pub(crate) fn judge_project_object_sampled(
    file: &std::fs::File,
    object: ProjectObject,
    uid: u32,
    policy: &ProjectChainPolicy<'_>,
    work: &mut WorkScope<'_>,
) -> Result<opensip_platform::DescriptorMetadata, Failure> {
    let sample = opensip_platform::capture_descriptor_acl_accounted(file, work)
        .map_err(lift(ProjectChainRefusal::RootCapture))?;
    let judged = check_project_object(
        sample.metadata(),
        sample.acl_state(),
        |index| sample.entry(index),
        uid,
        policy.trust_groups,
        object,
    );
    match judged {
        Err(crate::custody::Refusal::AclUnreadable)
            if sample.acl_state() == CapturedAclState::NotReturned =>
        {
            let admitted = match policy.premise {
                Some(premise) => premise
                    .admits(file, work)
                    .map_err(lift(ProjectChainRefusal::Chain))?,
                None => false,
            };
            if !admitted {
                return refuse(ProjectChainRefusal::RootAclOmitted);
            }
            check_project_object(
                sample.metadata(),
                CapturedAclState::Entries(0),
                |_| None,
                uid,
                policy.trust_groups,
                object,
            )
            .map(|()| sample.metadata().clone())
            .map_err(|refusal| WorkFailure::Operation(ProjectChainRefusal::Root(refusal)))
        }
        Err(refusal) => refuse(ProjectChainRefusal::Root(refusal)),
        Ok(()) => Ok(sample.metadata().clone()),
    }
}

/// S3 directory custody over a capture (pure): the shared `check` for the
/// kind, owner and mode bits with the trusted groups, then each ACL entry.
/// An allow that grants more than read-only rights must name the invoking
/// user, root or a trusted group. An entry this code cannot interpret, or a
/// state with no entries, is unreadable.
pub(crate) fn check_project_root(
    metadata: &opensip_platform::DescriptorMetadata,
    state: CapturedAclState,
    entry: impl Fn(usize) -> Option<opensip_platform::CapturedAclEntry>,
    invoking_uid: u32,
    trust_groups: &BTreeSet<u32>,
) -> Result<(), crate::custody::Refusal> {
    check_project_object(
        metadata,
        state,
        entry,
        invoking_uid,
        trust_groups,
        ProjectObject::Directory,
    )
}
/// `check_project_root` for either project object kind (pure).
pub(crate) fn check_project_object(
    metadata: &opensip_platform::DescriptorMetadata,
    state: CapturedAclState,
    entry: impl Fn(usize) -> Option<opensip_platform::CapturedAclEntry>,
    invoking_uid: u32,
    trust_groups: &BTreeSet<u32>,
    object: ProjectObject,
) -> Result<(), crate::custody::Refusal> {
    use super::{AclWrite, EntryKind, EntryObservation, Refusal, Scope};
    use crate::private_access::{ACE_DENY, ACE_KIND_MASK, ACE_PERMIT, KNOWN_ACE_FLAGS};
    let observed = EntryObservation {
        kind: match metadata.mode & 0o170000 {
            0o040000 => EntryKind::Directory,
            0o100000 => EntryKind::Regular,
            0o120000 => EntryKind::Symlink,
            _ => EntryKind::Other,
        },
        uid: metadata.uid,
        gid: metadata.gid,
        mode: metadata.mode,
        links: metadata.links,
        size: metadata.size,
        // The ACL is judged below from the capture. An empty list keeps the
        // shared refusal order: ACL after mode.
        acl: AclWrite::Known(Vec::new()),
    };
    super::check(
        Some(&observed),
        match object {
            ProjectObject::Directory => Scope::Directory,
            ProjectObject::ConfigurationFile => Scope::ConfigurationFile,
        },
        invoking_uid,
        trust_groups,
        false,
    )?;
    let CapturedAclState::Entries(count) = state else {
        return Err(Refusal::AclUnreadable);
    };
    for index in 0..count {
        let Some(e) = entry(index) else {
            return Err(Refusal::AclUnreadable);
        };
        if e.flags & !KNOWN_ACE_FLAGS != 0 {
            return Err(Refusal::AclUnreadable);
        }
        match e.flags & ACE_KIND_MASK {
            ACE_DENY => {}
            ACE_PERMIT if e.rights & !super::READ_ONLY_ACE_RIGHTS == 0 => {}
            ACE_PERMIT => match e.principal {
                CapturedAclPrincipal::User(id) if id == 0 || id == invoking_uid => {}
                CapturedAclPrincipal::Group(gid) if trust_groups.contains(&gid) => {}
                _ => return Err(Refusal::AclWrite),
            },
            _ => return Err(Refusal::AclUnreadable),
        }
    }
    Ok(())
}

/// The root's native birth, charged first. Unsupported or unreliable birth
/// data refuses; there is no ctime or mtime substitute (item 4).
fn sample_birth(
    root: &RetainedDirectory,
    work: &mut WorkScope<'_>,
) -> Result<DirectoryBirthObservation, Failure> {
    work.run(BIRTH_COST, |_| {
        root.observe_birth()
            .map_err(|error| WorkFailure::Operation(ProjectChainRefusal::BirthUnsupported(error)))
    })
}

#[cfg(test)]
mod tests {
    include!("project_chain_tests.rs");
}
