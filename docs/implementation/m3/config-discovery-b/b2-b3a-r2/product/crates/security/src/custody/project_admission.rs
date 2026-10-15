// Law X2 r5 (unit X2b-1): S3 root selection, the item 5 registry capture
// producer, and `ProjectRootAdmission` with the registry owner's
// classification (item 4). Built on X2a's project chain walk. Everything is
// charged to the held session's one ledger before it runs, and nothing is
// created or written.
//
// Not in this unit: item 6a's tracking observation (X2b-2). Until it exists,
// an admission carries its classification but grants nothing; item 4 makes
// every grant (Eligible's namespace admission, FirstUseCandidate's
// registration) require the untracked observation, and those grants are
// X2c's and X2d's. The write-gate entry is X2c's; this unit wires the read
// session only. Library only.
use super::installation_admission::{RequiredFile, judge_capture, missing};
use super::discovery_scan::{DiscoveryRefusal, ObservedVcs, UpwardProvenance, VcsRecord, WalkRow};
use super::project_chain::{
    CustodyOrder, Failure as ChainFailure, ProjectChain, ProjectChainPolicy, ProjectChainRefusal,
    ProjectChainRow, ProjectObject, applicable_waiver, judge_project_object,
    judge_project_object_ordered, judge_project_object_sampled, open_refusal, walk_project_chain,
    walk_project_chain_waived,
};
use crate::grants::ProjectOwnerWaiver;
use opensip_identity::{
    PROJECT_MARKER_SIZE, PROJECT_REGISTRY_CAP, ProjectIdMarker, ProjectRegistryDocument,
    ProjectRegistryEntry, ProjectRegistryError, ProjectRegistryStatus, ProjectRootPlatform,
};
use opensip_platform::{
    ChildKind, ChildObservation, DescriptorMetadata, RetainedDirectory, RetainedDirectoryPath,
    WorkCost, WorkFailure, WorkScope,
};
use std::ffi::OsStr;
use std::fs::File;
use std::io;
use std::os::unix::ffi::OsStrExt;
use std::path::{Path, PathBuf};
use opensip_platform::WorkReadFailure as ReadFailure;

/// S3's config file at a candidate directory.
pub(crate) const CONFIG_FILE: &str = "opensip.json";
/// S3's VCS boundary markers. Any one is the boundary; the analysis path's
/// evidence is the first present in this order (M3-B unit B2-b3a).
const VCS_MARKERS: [&str; 4] = [".git", ".hg", ".svn", ".jj"];
/// The project marker, below the root (identity §2).
pub(crate) const MARKER_DIRECTORY: &str = ".opensip";
pub(crate) const MARKER_FILE: &str = "project-id.v1";
/// The registry under I, and the old name that must be positively absent.
pub(super) const REGISTRY: &str = "project-registry.v2";
pub(super) const REGISTRY_V1: &str = "project-registry.v1";
/// S3: the selection walk examines at most 256 levels (item 9).
const MAX_WALK_LEVELS: usize = 256;

/// One status read on a retained descriptor (device for the mount boundary).
const STATUS: WorkCost = WorkCost {
    objects: 0,
    edges: 1,
    bytes: 512,
};

/// How S3 selected the root.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum SelectionMode {
    /// `--project`: the given path, examined exactly once.
    Explicit,
    /// A directory holding `opensip.json`.
    Config,
    /// A VCS marker's directory: the repository root, not the launch.
    VcsDefault,
    /// No candidate before a home, root, mount or custody boundary.
    CwdDefault,
}
/// Why the upward walk stopped.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum StopReason {
    Explicit,
    Candidate,
    Vcs,
    Home,
    FsRoot,
    Mount,
    Custody,
}
/// S3's selection result: the selected root's spelling and how it was found.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct Selected {
    root: PathBuf,
    mode: SelectionMode,
    stop: StopReason,
    config: bool,
}
impl Selected {
    pub(crate) fn root(&self) -> &Path {
        &self.root
    }
    pub(crate) fn mode(&self) -> SelectionMode {
        self.mode
    }
    pub(crate) fn stop(&self) -> StopReason {
        self.stop
    }
    /// The selected root holds a custody-checked `opensip.json`.
    pub(crate) fn config(&self) -> bool {
        self.config
    }
}

/// What an upward row's directory decided about its `opensip.json` (SLM
/// `walked[].candidate`; M3-B unit B2-b3a, LD-B2B3-7).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum Candidate {
    Absent,
    Present,
    Refused,
    NotExamined,
}
/// Why the walk stopped at a row (SLM `walked[].boundary`). A custody
/// boundary is the bare custody reason. A mount is the child's boundary.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum RowBoundary {
    Explicit,
    Vcs,
    Home,
    FsRoot,
    Mount,
    Custody(super::Refusal),
}
/// One examined directory, as selection recorded it (SLM `walked`).
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct UpwardRow {
    pub(crate) path: PathBuf,
    /// `None` passed S3 directory custody; otherwise its reason.
    pub(crate) custody: Option<super::Refusal>,
    pub(crate) candidate: Candidate,
    pub(crate) boundary: Option<RowBoundary>,
}
/// The analysis path's upward provenance (M3-B r5 item 13; unit B2-b3a,
/// LD-B2B3-7): selection's rows as SLM's walk records them, and the
/// selected root's VCS evidence. It fills as the walk runs, so a refusal
/// keeps the rows before it and names its object. The legacy selection
/// records nothing.
#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub(crate) struct UpwardRecord {
    pub(crate) walked: Vec<UpwardRow>,
    /// The first present VCS marker at the selected root (explicit, config
    /// or VCS stop), observed by name and never followed.
    pub(crate) vcs: Option<ObservedVcs>,
    /// The object a selection refusal names (SLM's refusal `path`).
    pub(crate) refused: Option<PathBuf>,
}
fn spelled(path: &Path) -> Option<String> {
    path.to_str().map(str::to_owned)
}
impl UpwardRecord {
    /// The rows as `DiscoveryProvenanceV3.walked`; `None` when a spelling is
    /// not UTF-8, which the caller refuses (its walk has no such record).
    pub(crate) fn rows(&self) -> Option<Vec<WalkRow>> {
        self.walked
            .iter()
            .map(|row| {
                Some(WalkRow {
                    path: spelled(&row.path)?,
                    custody: row.custody.map_or("PASS", super::Refusal::code).to_owned(),
                    candidate: match row.candidate {
                        Candidate::Absent => "ABSENT",
                        Candidate::Present => "PRESENT",
                        Candidate::Refused => "REFUSED",
                        Candidate::NotExamined => "NOT_EXAMINED",
                    }
                    .to_owned(),
                    boundary: row.boundary.map(|boundary| {
                        match boundary {
                            RowBoundary::Explicit => "EXPLICIT",
                            RowBoundary::Vcs => "VCS",
                            RowBoundary::Home => "HOME",
                            RowBoundary::FsRoot => "FS_ROOT",
                            RowBoundary::Mount => "MOUNT",
                            RowBoundary::Custody(why) => why.code(),
                        }
                        .to_owned()
                    }),
                })
            })
            .collect()
    }
    /// The discovery result's refusal, detail and named object for an
    /// admission refusal, only when selection itself refused (r2, Codex
    /// B2B3A-R1-NBO-2): selection names the object of every refusal it
    /// makes and of nothing else, so a later step's refusal (the chain walk,
    /// the marker, the carriers) has no named object here and maps to
    /// `None`, even where its variant is one selection also uses.
    pub(crate) fn discovery_refusal(
        &self,
        refusal: &ProjectAdmissionRefusal,
        explicit: bool,
    ) -> Option<(DiscoveryRefusal, &'static str, &Path)> {
        let path = self.refused.as_deref()?;
        let (code, detail) = refusal.selection_refusal(explicit)?;
        Some((code, detail, path))
    }
    /// The upward half of an accepted selection's provenance. The explicit
    /// path is never resolved through a link (a link in its spelling
    /// refuses), so `explicitPathWasSymlink` is false whenever it applies.
    pub(crate) fn provenance(&self, selected: &Selected) -> Option<UpwardProvenance> {
        let stop = match selected.stop {
            StopReason::Explicit => "EXPLICIT".to_owned(),
            StopReason::Candidate => "CANDIDATE".to_owned(),
            StopReason::Vcs => "VCS".to_owned(),
            StopReason::Home => "HOME".to_owned(),
            StopReason::FsRoot => "FS_ROOT".to_owned(),
            StopReason::Mount => "MOUNT".to_owned(),
            StopReason::Custody => match self.walked.last()?.boundary? {
                RowBoundary::Custody(why) => format!("CUSTODY:{}", why.code()),
                _ => return None,
            },
        };
        let explicit = selected.mode == SelectionMode::Explicit;
        Some(UpwardProvenance {
            mode: match selected.mode {
                SelectionMode::Explicit => "explicit",
                SelectionMode::Config => "config",
                SelectionMode::VcsDefault => "vcs-default",
                SelectionMode::CwdDefault => "cwd-default",
            }
            .to_owned(),
            config_path: if selected.config {
                Some(spelled(&selected.root.join(CONFIG_FILE))?)
            } else {
                None
            },
            walked: self.rows()?,
            stop_reason: stop,
            vcs: self.vcs.as_ref().map(|vcs| match vcs {
                ObservedVcs::Directory => VcsRecord {
                    kind: "directory",
                    target: None,
                },
                ObservedVcs::Indirection { target } => VcsRecord {
                    kind: "indirection",
                    target: target.clone(),
                },
            }),
            explicit_path_was_symlink: explicit.then_some(false),
        })
    }
}

/// Why project admission refused. Each variant has one item 8 row (`row`).
#[derive(Debug)]
pub(crate) enum ProjectAdmissionRefusal {
    /// X2a's chain walk, or a custody judgment it owns.
    Chain(ProjectChainRefusal),
    /// S3: the launch directory (or the explicit path) failed custody.
    LaunchCustody(ProjectChainRefusal),
    /// S3: more than 256 levels.
    WalkDepthExceeded,
    /// S3: a present `opensip.json` failed config custody, or is not a file.
    ConfigCustody(ConfigRefusal),
    /// Item 4: the root's volume identity is unsupported or unavailable.
    VolumeUnsupported(io::Error),
    /// `.opensip` or the marker is not a private object of the kind expected.
    MarkerCustody(&'static str),
    /// Item 5: the registry is missing, oversized or malformed, or
    /// `project-registry.v1` is present. Unavailable, never empty.
    Registry(RegistryRefusal),
    /// A retained registry, marker or volume observation changed.
    Changed,
    /// M3-B unit B1-b (X2 r9 item 3a): a configuration carrier refused, or
    /// one observed absent appeared. `CONFIG.CUSTODY_REFUSED`, this subject.
    Carrier(&'static str),
    Io(io::Error),
}
/// Config custody failures, S3's `CONFIG.CUSTODY_REFUSED` causes.
#[derive(Debug)]
pub(crate) enum ConfigRefusal {
    Symlink,
    NotRegular,
    Custody(ProjectChainRefusal),
}
/// Item 5's unavailable registry states.
#[derive(Debug)]
pub(crate) enum RegistryRefusal {
    Missing,
    Oversized,
    Malformed(ProjectRegistryError),
    OldNamePresent,
}
/// Item 8's row for a refusal, for the host projection (X2c and later).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum ProjectAdmissionRow {
    /// `PROJECT.ROOT_CUSTODY_REFUSED`, with this subject.
    RootCustody(&'static str),
    /// `CONFIG.CUSTODY_REFUSED`, with this subject.
    ConfigCustody(&'static str),
    /// `PROJECT.EXPLICIT_PATH_INVALID` (S3).
    ExplicitPath,
    /// 468 item 6's incomplete-installation row (item 5: unavailable).
    Incomplete,
    /// The custody row with subject `required-files-changed`.
    RequiredFilesChanged,
    /// The host I/O row.
    HostIo,
}
fn chain_row(row: ProjectChainRow) -> ProjectAdmissionRow {
    match row {
        ProjectChainRow::RootCustody(subject) => ProjectAdmissionRow::RootCustody(subject),
        ProjectChainRow::ExplicitPath => ProjectAdmissionRow::ExplicitPath,
        ProjectChainRow::HostIo => ProjectAdmissionRow::HostIo,
    }
}
impl ProjectAdmissionRefusal {
    pub(crate) fn row(&self) -> ProjectAdmissionRow {
        use ProjectAdmissionRow as Row;
        match self {
            Self::Chain(refusal) | Self::LaunchCustody(refusal) => chain_row(refusal.row()),
            Self::WalkDepthExceeded => Row::RootCustody("walk-depth-exceeded"),
            Self::ConfigCustody(refusal) => Row::ConfigCustody(match refusal {
                ConfigRefusal::Symlink => "symlink",
                ConfigRefusal::NotRegular => "not-a-regular-file",
                ConfigRefusal::Custody(inner) => match inner.row() {
                    ProjectChainRow::RootCustody(subject) => subject,
                    // `examine` routes host I/O to `Chain`; nothing else
                    // reaches here.
                    ProjectChainRow::ExplicitPath | ProjectChainRow::HostIo => "custody",
                },
            }),
            Self::VolumeUnsupported(_) => Row::RootCustody("volume-unsupported"),
            Self::MarkerCustody(subject) => Row::RootCustody(subject),
            Self::Registry(_) => Row::Incomplete,
            Self::Changed => Row::RequiredFilesChanged,
            Self::Carrier(subject) => Row::ConfigCustody(subject),
            Self::Io(_) => Row::HostIo,
        }
    }
    /// The discovery result's refusal and detail for a refusal selection
    /// made (SLM `discovery`'s upward refusals; M3-B unit B2-b3a), with
    /// `explicit` saying whether `--project` was given. `None` for a
    /// refusal that is not discovery's (host I/O, budget). Only
    /// `UpwardRecord::discovery_refusal` calls it, which also requires that
    /// selection named the refusal's object: the chain walk can refuse with
    /// the same variants.
    fn selection_refusal(&self, explicit: bool) -> Option<(DiscoveryRefusal, &'static str)> {
        use super::Refusal as R;
        let custody = |refusal: &ProjectChainRefusal| match refusal {
            ProjectChainRefusal::Root(why) => Some(*why),
            ProjectChainRefusal::RootAclOmitted => Some(R::AclUnreadable),
            _ => None,
        };
        match self {
            Self::Chain(ProjectChainRefusal::PathInvalid(error)) => {
                let why = match error.kind() {
                    io::ErrorKind::NotFound => R::Absent,
                    io::ErrorKind::NotADirectory => R::NotDirectory,
                    _ => return None,
                };
                let refusal = if explicit {
                    DiscoveryRefusal::ExplicitPathInvalid
                } else {
                    DiscoveryRefusal::RootCustodyRefused
                };
                Some((refusal, why.code()))
            }
            Self::Chain(ProjectChainRefusal::Symlink) => {
                Some((DiscoveryRefusal::RootCustodyRefused, R::Symlink.code()))
            }
            Self::LaunchCustody(refusal) => {
                Some((DiscoveryRefusal::RootCustodyRefused, custody(refusal)?.code()))
            }
            Self::WalkDepthExceeded => {
                Some((DiscoveryRefusal::RootCustodyRefused, "WALK_DEPTH_EXCEEDED"))
            }
            Self::ConfigCustody(refusal) => Some((
                DiscoveryRefusal::ConfigCustodyRefused,
                match refusal {
                    ConfigRefusal::Symlink => R::Symlink.code(),
                    ConfigRefusal::NotRegular => R::NotRegular.code(),
                    ConfigRefusal::Custody(inner) => custody(inner)?.code(),
                },
            )),
            _ => None,
        }
    }
}
pub(crate) type Failure = WorkFailure<ProjectAdmissionRefusal>;
fn refuse<T>(refusal: ProjectAdmissionRefusal) -> Result<T, Failure> {
    Err(WorkFailure::Operation(refusal))
}
fn chain(failure: ChainFailure) -> Failure {
    match failure {
        WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
        WorkFailure::Operation(refusal) => WorkFailure::Operation(ProjectAdmissionRefusal::Chain(refusal)),
    }
}
fn io_failure(failure: WorkFailure<io::Error>) -> Failure {
    match failure {
        WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
        WorkFailure::Operation(error) => WorkFailure::Operation(ProjectAdmissionRefusal::Io(error)),
    }
}
/// macOS `ELOOP`: O_NOFOLLOW met a symbolic link.
const ELOOP: i32 = 62;

/// One no-follow open of a regular file under `directory`, charged first.
/// The outcome is a value, so a missing or wrong-kind object is the
/// caller's observation, not a failed scope.
fn open_file(
    directory: &RetainedDirectory,
    name: &str,
    work: &mut WorkScope<'_>,
) -> Result<io::Result<File>, Failure> {
    work.run(RetainedDirectory::open_regular_cost(name), |_| {
        Ok::<_, Failure>(directory.open_regular(name))
    })
}

/// A charged status read for the mount boundary.
fn device(directory: &RetainedDirectory, work: &mut WorkScope<'_>) -> Result<u64, Failure> {
    use std::os::unix::fs::MetadataExt;
    work.run(STATUS, |_| {
        directory
            .as_file()
            .metadata()
            .map(|m| m.dev())
            .map_err(|error| WorkFailure::Operation(ProjectAdmissionRefusal::Io(error)))
    })
}

/// What one examined directory decided.
enum Examined {
    /// It holds a custody-checked `opensip.json`; its judged descriptor and
    /// the full sample the judgment passed on, when the caller retains them
    /// (M3-B unit B1-b, the analysis path only).
    Config(Option<(File, DescriptorMetadata)>),
    /// It holds a VCS marker.
    Vcs,
    /// Neither.
    Nothing,
}
/// S3's examination of one directory that passed custody: the config file,
/// custody-checked if present (a failure refuses; it is never skipped), then
/// the VCS markers by positive no-follow lookups. With `recorded` (the
/// analysis path, M3-B unit B2-b3a) the config is judged with the waiver in
/// SLM's refusal order, and the directory's VCS evidence is returned: after
/// a config too, since SLM records the config directory's `vcs`. Without it,
/// this is exactly the legacy examination.
#[allow(clippy::too_many_arguments)]
fn examine(
    directory: &RetainedDirectory,
    uid: u32,
    policy: &ProjectChainPolicy<'_>,
    retain: bool,
    waiver: Option<&ProjectOwnerWaiver>,
    recorded: bool,
    work: &mut WorkScope<'_>,
) -> Result<(Examined, Option<ObservedVcs>), Failure> {
    let order = if recorded {
        CustodyOrder::Reference
    } else {
        CustodyOrder::Shared
    };
    match open_file(directory, CONFIG_FILE, work)? {
        Ok(file) => {
            let judged = match judge_project_object_ordered(
                &file,
                ProjectObject::ConfigurationFile,
                uid,
                policy,
                waiver,
                order,
                work,
            ) {
                Ok(judged) => judged,
                Err(WorkFailure::Operation(refusal)) => return refuse(config_refusal(refusal)),
                Err(WorkFailure::Budget(budget)) => return Err(WorkFailure::Budget(budget)),
            };
            let vcs = if recorded {
                vcs_evidence(directory, uid, policy, work)?
            } else {
                None
            };
            return Ok((Examined::Config(retain.then_some((file, judged))), vcs));
        }
        Err(error) if error.kind() == io::ErrorKind::NotFound => {}
        Err(error) if error.raw_os_error() == Some(ELOOP) => {
            return refuse(ProjectAdmissionRefusal::ConfigCustody(ConfigRefusal::Symlink));
        }
        Err(error) if error.kind() == io::ErrorKind::InvalidInput => {
            return refuse(ProjectAdmissionRefusal::ConfigCustody(ConfigRefusal::NotRegular));
        }
        Err(error) => return refuse(ProjectAdmissionRefusal::Io(error)),
    }
    if recorded {
        let vcs = vcs_evidence(directory, uid, policy, work)?;
        let examined = if vcs.is_some() {
            Examined::Vcs
        } else {
            Examined::Nothing
        };
        return Ok((examined, vcs));
    }
    for marker in VCS_MARKERS {
        let absent = directory
            .observe_child_absent_accounted(OsStr::new(marker), work)
            .map_err(io_failure)?;
        if !absent {
            return Ok((Examined::Vcs, None));
        }
    }
    Ok((Examined::Nothing, None))
}

/// The analysis path's VCS evidence at one directory (M3-B unit B2-b3a,
/// LD-B2B3-7): the first present marker in `VCS_MARKERS` order, each by one
/// charged no-follow status read (the legacy absence probe's cost). A marker
/// directory is `directory`. A regular `.git` file is `indirection` with its
/// `gitdir:` value when S3 file custody admits it. Any other `.git`, or a
/// non-directory `.hg`, `.svn` or `.jj`, is `indirection` with no target: it
/// is never opened or followed.
fn vcs_evidence(
    directory: &RetainedDirectory,
    uid: u32,
    policy: &ProjectChainPolicy<'_>,
    work: &mut WorkScope<'_>,
) -> Result<Option<ObservedVcs>, Failure> {
    for marker in VCS_MARKERS {
        let observation = directory
            .observe_child_accounted(OsStr::new(marker), work)
            .map_err(io_failure)?;
        let ChildObservation::Present { kind, .. } = &observation else {
            continue;
        };
        return Ok(Some(match kind {
            ChildKind::Directory => ObservedVcs::Directory,
            ChildKind::File if marker == ".git" => ObservedVcs::Indirection {
                target: gitdir_target(directory, &observation, uid, policy, work)?,
            },
            _ => ObservedVcs::Indirection { target: None },
        }));
    }
    Ok(None)
}

/// A regular `.git` file's `gitdir:` value, read as data and never followed
/// (LD-B2B3-7; r2, Codex B2B3A-R1-RF-1). The file is opened no-follow from
/// its parent and must be the entry observed. It is then judged by S3 file
/// custody, exactly as a configuration file is (owner, other and group
/// write, the ACL with this invocation's premise and trusted groups, one
/// link, at most 4 MiB, in SLM's order), with no owner waiver. A file that
/// custody refuses keeps its boundary and has no target. Otherwise its
/// bytes are read once from the judged descriptor, whose status must be
/// unchanged before and after the read, and one `gitdir:` line is the
/// target. A change between the observation, the judgment and the read
/// refuses the whole operation, as do exhaustion and host I/O.
fn gitdir_target(
    directory: &RetainedDirectory,
    observation: &ChildObservation,
    uid: u32,
    policy: &ProjectChainPolicy<'_>,
    work: &mut WorkScope<'_>,
) -> Result<Option<String>, Failure> {
    let file = match open_file(directory, ".git", work)? {
        Ok(file) => file,
        // Observed as a regular file: gone, a link or another kind now is a
        // change.
        Err(error)
            if error.kind() == io::ErrorKind::NotFound
                || error.kind() == io::ErrorKind::InvalidInput
                || error.raw_os_error() == Some(ELOOP) =>
        {
            return refuse(ProjectAdmissionRefusal::Changed);
        }
        Err(error) => return refuse(ProjectAdmissionRefusal::Io(error)),
    };
    let sample = |file: &File, work: &mut WorkScope<'_>| {
        work.run(STATUS, |_| {
            opensip_platform::observe_descriptor_metadata(file)
                .map_err(|error| WorkFailure::Operation(ProjectAdmissionRefusal::Io(error)))
        })
    };
    let opened = sample(&file, work)?;
    if !observation.matches(&opened) {
        return refuse(ProjectAdmissionRefusal::Changed);
    }
    let judged = match judge_project_object_ordered(
        &file,
        ProjectObject::ConfigurationFile,
        uid,
        policy,
        None,
        CustodyOrder::Reference,
        work,
    ) {
        Ok(judged) => judged,
        Err(WorkFailure::Operation(
            ProjectChainRefusal::Root(_) | ProjectChainRefusal::RootAclOmitted,
        )) => return Ok(None),
        Err(WorkFailure::Operation(refusal)) => {
            return refuse(ProjectAdmissionRefusal::Chain(refusal));
        }
        Err(WorkFailure::Budget(budget)) => return Err(WorkFailure::Budget(budget)),
    };
    if judged != opened {
        return refuse(ProjectAdmissionRefusal::Changed);
    }
    let limit = usize::try_from(super::MAX_CONFIG_BYTES).unwrap_or(usize::MAX);
    let bytes = match opensip_platform::read_bounded_observed(&file, limit, work)? {
        Ok(bytes) => bytes,
        // Judged within 4 MiB, so a longer read means the file changed.
        Err(ReadFailure::Bound) => return refuse(ProjectAdmissionRefusal::Changed),
        Err(error) => {
            return refuse(ProjectAdmissionRefusal::Io(io::Error::other(format!("{error:?}"))));
        }
    };
    if sample(&file, work)? != judged {
        return refuse(ProjectAdmissionRefusal::Changed);
    }
    let Some(target) = gitdir_value(&bytes) else {
        return Ok(None);
    };
    work.run(
        WorkCost {
            objects: 1,
            edges: 0,
            bytes: target.len(),
        },
        |_| Ok(Some(target.to_owned())),
    )
}
/// Git's `.git` file form, `gitdir: <path>`, with an optional `\n` or
/// `\r\n` line end (r2, Codex B2B3A-R1-NBO-1: a bare `\r` is not one): one
/// nonempty UTF-8 line. Anything else has no value.
fn gitdir_value(bytes: &[u8]) -> Option<&str> {
    let line = std::str::from_utf8(bytes).ok()?.strip_prefix("gitdir: ")?;
    let value = line
        .strip_suffix("\r\n")
        .or_else(|| line.strip_suffix('\n'))
        .unwrap_or(line);
    (!value.is_empty() && !value.contains(['\n', '\r', '\0'])).then_some(value)
}

/// A config custody judgment that did not pass: a capture or filesystem I/O
/// failure is the host I/O row (item 8), never config custody; every other
/// refusal is `CONFIG.CUSTODY_REFUSED`.
fn config_refusal(refusal: ProjectChainRefusal) -> ProjectAdmissionRefusal {
    if refusal.row() == ProjectChainRow::HostIo {
        ProjectAdmissionRefusal::Chain(refusal)
    } else {
        ProjectAdmissionRefusal::ConfigCustody(ConfigRefusal::Custody(refusal))
    }
}

/// S3 directory custody of one examined directory as a value: `Ok(true)`
/// passes, `Ok(false)` is a custody failure (a boundary above the launch).
/// Budget and I/O failures still fail the scope.
fn passes(
    directory: &RetainedDirectory,
    uid: u32,
    policy: &ProjectChainPolicy<'_>,
    waiver: Option<&ProjectOwnerWaiver>,
    work: &mut WorkScope<'_>,
) -> Result<Result<(), ProjectChainRefusal>, Failure> {
    match judge_project_object_ordered(
        directory.as_file(),
        ProjectObject::Directory,
        uid,
        policy,
        waiver,
        CustodyOrder::Shared,
        work,
    ) {
        Ok(_) => Ok(Ok(())),
        Err(WorkFailure::Operation(
            refusal @ (ProjectChainRefusal::Root(_) | ProjectChainRefusal::RootAclOmitted),
        )) => Ok(Err(refusal)),
        Err(failure) => Err(chain(failure)),
    }
}

/// S3's selection (item 3: "selection stays S3's"), charged on the session's
/// ledger. With `explicit`, that path is examined exactly once: its custody
/// (absent or not a directory is the explicit-path row), then its config.
/// Otherwise the walk runs upward from `launch`, at most 256 levels: a
/// custody failure at the launch refuses, one at an ancestor is a boundary;
/// a passing directory's config, if present, is custody-checked and selects
/// it; then, in precedence, a VCS marker selects that repository root, and
/// the account home, the filesystem root and a mount change are boundaries
/// that select the launch. Raw spellings are never normalized: a symlink
/// anywhere in the spelling refuses (no-follow opens).
pub(crate) fn select_project_root(
    launch: &Path,
    explicit: Option<&Path>,
    home: &Path,
    uid: u32,
    policy: &ProjectChainPolicy<'_>,
    work: &mut WorkScope<'_>,
) -> Result<Selected, Failure> {
    select(launch, explicit, home, uid, policy, false, None, None, work).map(|(selected, _)| selected)
}
/// Name the object a recorded selection refusal is about (SLM's refusal
/// `path`), charged as one owned copy. A failed open closes the scope, so
/// the path an open may refuse is named before it, and cleared after.
fn refused_at(
    record: &mut Option<&mut UpwardRecord>,
    path: &Path,
    work: &mut WorkScope<'_>,
) -> Result<(), Failure> {
    if let Some(record) = record.as_deref_mut() {
        record.refused = Some(owned(path, work)?);
    }
    Ok(())
}
/// Append one row to a recorded selection, its spelling charged as one
/// owned copy.
fn push_row(
    record: &mut Option<&mut UpwardRecord>,
    path: &Path,
    custody: Option<super::Refusal>,
    candidate: Candidate,
    boundary: Option<RowBoundary>,
    work: &mut WorkScope<'_>,
) -> Result<(), Failure> {
    if let Some(record) = record.as_deref_mut() {
        record.walked.push(UpwardRow {
            path: owned(path, work)?,
            custody,
            candidate,
            boundary,
        });
    }
    Ok(())
}
/// Set the last recorded row's boundary (or candidate).
fn last_row(record: &mut Option<&mut UpwardRecord>, update: impl FnOnce(&mut UpwardRow)) {
    if let Some(row) = record.as_deref_mut().and_then(|record| record.walked.last_mut()) {
        update(row);
    }
}
/// `examine` for a recorded row: the row's candidate follows the config
/// (PRESENT when it passes, REFUSED when its custody refuses, which names
/// the config), and the evidence is kept for the caller.
#[allow(clippy::too_many_arguments)]
fn examine_row(
    directory: &RetainedDirectory,
    path: &Path,
    uid: u32,
    policy: &ProjectChainPolicy<'_>,
    retain: bool,
    waiver: Option<&ProjectOwnerWaiver>,
    record: &mut Option<&mut UpwardRecord>,
    work: &mut WorkScope<'_>,
) -> Result<(Examined, Option<ObservedVcs>), Failure> {
    let result = examine(directory, uid, policy, retain, waiver, record.is_some(), work);
    match &result {
        Ok((Examined::Config(_), _)) => last_row(record, |row| row.candidate = Candidate::Present),
        Err(WorkFailure::Operation(ProjectAdmissionRefusal::ConfigCustody(_))) => {
            last_row(record, |row| row.candidate = Candidate::Refused);
            refused_at(record, &path.join(CONFIG_FILE), work)?;
        }
        _ => {}
    }
    result
}
/// S3's selection, also returning the selected `opensip.json`'s judged
/// descriptor when `retain` (M3-B unit B1-b; X2 r9 item 3a). Without
/// `retain`, `waiver` or `record` it is exactly the legacy selection: the
/// same opens, charges and refusals, and the descriptor is dropped where it
/// always was.
///
/// With `record` (the analysis path, M3-B unit B2-b3a, LD-B2B3-7) it also
/// records SLM's rows and the selected root's VCS evidence, and follows
/// SLM's walk where the legacy order differs: the config is judged in SLM's
/// refusal order, and a mount is the child's boundary, decided before the
/// parent's depth. `waiver` (LD-B2B3-9) reaches only the explicit root and
/// its `opensip.json`, and only when it names that root.
#[allow(clippy::too_many_arguments)]
fn select(
    launch: &Path,
    explicit: Option<&Path>,
    home: &Path,
    uid: u32,
    policy: &ProjectChainPolicy<'_>,
    retain: bool,
    waiver: Option<&ProjectOwnerWaiver>,
    mut record: Option<&mut UpwardRecord>,
    work: &mut WorkScope<'_>,
) -> Result<(Selected, Option<(File, DescriptorMetadata)>), Failure> {
    if let Some(explicit) = explicit {
        let waiver = applicable_waiver(waiver, explicit);
        refused_at(&mut record, explicit, work)?;
        let path = open_path(explicit, work)?;
        if let Some(record) = record.as_deref_mut() {
            record.refused = None;
        }
        if let Err(refusal) = passes(path.directory(), uid, policy, waiver, work)? {
            refused_at(&mut record, explicit, work)?;
            return refuse(ProjectAdmissionRefusal::LaunchCustody(refusal));
        }
        push_row(
            &mut record,
            explicit,
            None,
            Candidate::Absent,
            Some(RowBoundary::Explicit),
            work,
        )?;
        let (examined, vcs) = examine_row(
            path.directory(),
            explicit,
            uid,
            policy,
            retain,
            waiver,
            &mut record,
            work,
        )?;
        let (config, file) = match examined {
            Examined::Config(file) => (true, file),
            Examined::Vcs | Examined::Nothing => (false, None),
        };
        if let Some(record) = record.as_deref_mut() {
            record.vcs = vcs;
        }
        return Ok((
            Selected {
                root: owned(explicit, work)?,
                mode: SelectionMode::Explicit,
                stop: StopReason::Explicit,
                config,
            },
            file,
        ));
    }
    refused_at(&mut record, launch, work)?;
    let path = open_path(launch, work)?;
    if let Some(record) = record.as_deref_mut() {
        record.refused = None;
    }
    let leaf = path.component_count();
    let home_index = launch
        .starts_with(home)
        .then(|| home.components().count() - 1);
    let mut outcome: Option<(usize, SelectionMode, StopReason, bool)> = None;
    let mut retained: Option<(File, DescriptorMetadata)> = None;
    let mut child_device: Option<u64> = None;
    let mut levels = 0usize;
    let recorded = record.is_some();
    path.visit_directories_upward(|index, directory| -> Result<bool, Failure> {
        levels += 1;
        let here_path = launch
            .ancestors()
            .nth(leaf - index)
            .expect("the retained walk has this many components");
        // SLM: a mount is the child's boundary, so the analysis path reads
        // this directory's device before it judges the walk's depth here.
        let early = if recorded {
            Some(device(directory, work)?)
        } else {
            None
        };
        let mount = |here: u64| child_device.is_some_and(|child| child != here);
        if early.is_some_and(mount) {
            last_row(&mut record, |row| row.boundary = Some(RowBoundary::Mount));
            outcome = Some((leaf, SelectionMode::CwdDefault, StopReason::Mount, false));
            return Ok(false);
        }
        if levels > MAX_WALK_LEVELS {
            refused_at(&mut record, here_path, work)?;
            return refuse(ProjectAdmissionRefusal::WalkDepthExceeded);
        }
        let here = match early {
            Some(here) => here,
            None => device(directory, work)?,
        };
        if mount(here) {
            outcome = Some((leaf, SelectionMode::CwdDefault, StopReason::Mount, false));
            return Ok(false);
        }
        if let Err(refusal) = passes(directory, uid, policy, None, work)? {
            if index == leaf {
                refused_at(&mut record, here_path, work)?;
                return refuse(ProjectAdmissionRefusal::LaunchCustody(refusal));
            }
            let why = match &refusal {
                ProjectChainRefusal::Root(why) => *why,
                // `passes` returns only a custody judgment or an omitted ACL
                // no premise admitted, which custody cannot establish.
                _ => super::Refusal::AclUnreadable,
            };
            push_row(
                &mut record,
                here_path,
                Some(why),
                Candidate::NotExamined,
                Some(RowBoundary::Custody(why)),
                work,
            )?;
            outcome = Some((leaf, SelectionMode::CwdDefault, StopReason::Custody, false));
            return Ok(false);
        }
        push_row(&mut record, here_path, None, Candidate::Absent, None, work)?;
        let (examined, vcs) = examine_row(
            directory,
            here_path,
            uid,
            policy,
            retain,
            None,
            &mut record,
            work,
        )?;
        match examined {
            Examined::Config(file) => {
                retained = file;
                if let Some(record) = record.as_deref_mut() {
                    record.vcs = vcs;
                }
                outcome = Some((index, SelectionMode::Config, StopReason::Candidate, true));
                return Ok(false);
            }
            Examined::Vcs => {
                last_row(&mut record, |row| row.boundary = Some(RowBoundary::Vcs));
                if let Some(record) = record.as_deref_mut() {
                    record.vcs = vcs;
                }
                outcome = Some((index, SelectionMode::VcsDefault, StopReason::Vcs, false));
                return Ok(false);
            }
            Examined::Nothing => {}
        }
        if home_index == Some(index) {
            last_row(&mut record, |row| row.boundary = Some(RowBoundary::Home));
            outcome = Some((leaf, SelectionMode::CwdDefault, StopReason::Home, false));
            return Ok(false);
        }
        if index == 0 {
            last_row(&mut record, |row| row.boundary = Some(RowBoundary::FsRoot));
            outcome = Some((leaf, SelectionMode::CwdDefault, StopReason::FsRoot, false));
            return Ok(false);
        }
        child_device = Some(here);
        Ok(true)
    })?;
    let (index, mode, stop, config) =
        outcome.unwrap_or((leaf, SelectionMode::CwdDefault, StopReason::FsRoot, false));
    let selected = launch
        .ancestors()
        .nth(leaf - index)
        .expect("the retained walk has this many components");
    Ok((
        Selected {
            root: owned(selected, work)?,
            mode,
            stop,
            config,
        },
        retained,
    ))
}
fn open_path(path: &Path, work: &mut WorkScope<'_>) -> Result<RetainedDirectoryPath, Failure> {
    work.run(opensip_platform::retained_path_open_cost(path), |_| {
        RetainedDirectoryPath::open_project_root(path, super::project_chain::MAX_PROJECT_COMPONENTS)
            .map_err(|error| WorkFailure::Operation(ProjectAdmissionRefusal::Chain(open_refusal(error))))
    })
}
/// One owned copy of a spelling, charged first.
fn owned(path: &Path, work: &mut WorkScope<'_>) -> Result<PathBuf, Failure> {
    work.run(
        WorkCost {
            objects: 1,
            edges: 0,
            bytes: path.as_os_str().len(),
        },
        |_| Ok(path.to_path_buf()),
    )
}

/// Item 5's one capture of the complete registry under the held fence:
/// opened no-follow through the retained I by the name whose custody the
/// session already judged, its full metadata sample required to equal that
/// judgment's (so it is the same file, unchanged), read once within 4 MiB,
/// and decoded whole before any classification. `project-registry.v1` is
/// observed positively absent. Unavailable, never empty. The descriptor
/// that was read is retained (item 5): it is R0, the predecessor first
/// registration reconfirms (item 6, unit X2c).
pub(crate) struct RegistryCapture {
    file: File,
    metadata: DescriptorMetadata,
    document: ProjectRegistryDocument,
}
impl std::fmt::Debug for RegistryCapture {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("RegistryCapture")
            .field("entries", &self.document.entries().len())
            .finish_non_exhaustive()
    }
}
impl RegistryCapture {
    /// The validated document (R0).
    pub(crate) fn document(&self) -> &ProjectRegistryDocument {
        &self.document
    }
    /// The full metadata sample of the file that was read.
    pub(super) fn metadata(&self) -> &DescriptorMetadata {
        &self.metadata
    }
    /// R0 as its parts: the retained descriptor, its sample and the
    /// validated document (item 6's replacement primitive, unit X2c).
    pub(super) fn into_parts(self) -> (File, DescriptorMetadata, ProjectRegistryDocument) {
        (self.file, self.metadata, self.document)
    }
}
pub(crate) fn capture_registry(
    installation: &RetainedDirectory,
    judged: &RequiredFile,
    work: &mut WorkScope<'_>,
) -> Result<RegistryCapture, Failure> {
    let metadata = registry_sample(installation, judged, work)?;
    let file = match open_file(installation, REGISTRY, work)? {
        Ok(file) => file,
        Err(error) if missing(&error) => {
            return refuse(ProjectAdmissionRefusal::Registry(RegistryRefusal::Missing));
        }
        Err(error) => return refuse(ProjectAdmissionRefusal::Io(error)),
    };
    let raw = match opensip_platform::read_bounded_observed(&file, PROJECT_REGISTRY_CAP, work)? {
        Ok(raw) => raw,
        Err(ReadFailure::Bound) => {
            return refuse(ProjectAdmissionRefusal::Registry(RegistryRefusal::Oversized));
        }
        Err(error) => {
            return refuse(ProjectAdmissionRefusal::Io(io::Error::other(format!("{error:?}"))));
        }
    };
    // Whole-document validation, charged as one step over the decoded size.
    let decode = WorkCost {
        objects: 1,
        edges: 1,
        bytes: raw.len(),
    };
    let document = work.run(decode, |_| {
        ProjectRegistryDocument::decode(&raw).map_err(|error| {
            WorkFailure::Operation(ProjectAdmissionRefusal::Registry(RegistryRefusal::Malformed(
                error,
            )))
        })
    })?;
    // The read file is the judged one, unchanged since the judgment.
    if registry_sample(installation, judged, work)? != metadata {
        return refuse(ProjectAdmissionRefusal::Changed);
    }
    old_name_absent(installation, work)?;
    Ok(RegistryCapture {
        file,
        metadata,
        document,
    })
}
/// The registry's full metadata sample now, required to equal the session's
/// judgment of it.
fn registry_sample(
    installation: &RetainedDirectory,
    judged: &RequiredFile,
    work: &mut WorkScope<'_>,
) -> Result<DescriptorMetadata, Failure> {
    let file = match open_file(installation, REGISTRY, work)? {
        Ok(file) => file,
        Err(error) if missing(&error) => {
            return refuse(ProjectAdmissionRefusal::Registry(RegistryRefusal::Missing));
        }
        Err(error) => return refuse(ProjectAdmissionRefusal::Io(error)),
    };
    let sample = opensip_platform::capture_descriptor_acl_accounted(&file, work).map_err(
        |failure| match failure {
            WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
            WorkFailure::Operation(error) => WorkFailure::Operation(ProjectAdmissionRefusal::Io(
                io::Error::other(format!("{error:?}")),
            )),
        },
    )?;
    if sample.metadata() != judged.metadata() {
        return refuse(ProjectAdmissionRefusal::Changed);
    }
    Ok(sample.metadata().clone())
}
pub(super) fn old_name_absent(
    installation: &RetainedDirectory,
    work: &mut WorkScope<'_>,
) -> Result<(), Failure> {
    let absent = installation
        .observe_child_absent_accounted(OsStr::new(REGISTRY_V1), work)
        .map_err(io_failure)?;
    if absent {
        Ok(())
    } else {
        refuse(ProjectAdmissionRefusal::Registry(RegistryRefusal::OldNamePresent))
    }
}

/// The marker observation at `.opensip/project-id.v1` (item 4).
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) enum MarkerObservation {
    /// `.opensip` or the marker is positively absent (native NotFound).
    Absent,
    /// The exact 92-byte marker, read once, with its file's metadata.
    Present {
        project: String,
        metadata: DescriptorMetadata,
    },
    /// An object is there that is not an exact marker: not a regular file,
    /// a symlink, the wrong size, or the wrong frame. Never a marker.
    Malformed,
}
impl MarkerObservation {
    fn project(&self) -> Option<&str> {
        match self {
            Self::Present { project, .. } => Some(project),
            _ => None,
        }
    }
}
/// Observe the marker under the retained root. `.opensip` is judged by S3
/// directory custody (item 1 puts it in the premise's scope). The marker is
/// OpenSIP's own operational file, outside the premise: it is judged private
/// (owned by the invoking user, 0600, one link, the zero-rights owner allow
/// of a private creation), as X2c will create it.
fn observe_marker(
    root: &RetainedDirectory,
    uid: u32,
    policy: &ProjectChainPolicy<'_>,
    work: &mut WorkScope<'_>,
) -> Result<MarkerObservation, Failure> {
    let directory = match work.run(
        opensip_platform::open_child_directory_cost(OsStr::new(MARKER_DIRECTORY)),
        |_| Ok::<_, Failure>(root.open_child_directory(OsStr::new(MARKER_DIRECTORY))),
    )? {
        Ok(directory) => directory,
        Err(error) if error.kind() == io::ErrorKind::NotFound => return Ok(MarkerObservation::Absent),
        Err(error)
            if error.raw_os_error() == Some(ELOOP)
                || error.kind() == io::ErrorKind::NotADirectory
                || error.kind() == io::ErrorKind::InvalidInput =>
        {
            return Ok(MarkerObservation::Malformed);
        }
        Err(error) => return refuse(ProjectAdmissionRefusal::Io(error)),
    };
    match judge_project_object(directory.as_file(), ProjectObject::Directory, uid, policy, work) {
        Ok(()) => {}
        Err(WorkFailure::Operation(refusal)) => return refuse(marker_directory_refusal(refusal)),
        Err(WorkFailure::Budget(budget)) => return Err(WorkFailure::Budget(budget)),
    }
    let file = match open_file(&directory, MARKER_FILE, work)? {
        Ok(file) => file,
        Err(error) if error.kind() == io::ErrorKind::NotFound => return Ok(MarkerObservation::Absent),
        Err(error)
            if error.raw_os_error() == Some(ELOOP) || error.kind() == io::ErrorKind::InvalidInput =>
        {
            return Ok(MarkerObservation::Malformed);
        }
        Err(error) => return refuse(ProjectAdmissionRefusal::Io(error)),
    };
    let capture = opensip_platform::capture_descriptor_acl_accounted(&file, work)
        .map_err(|failure| match failure {
            WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
            WorkFailure::Operation(error) => WorkFailure::Operation(marker_capture_refusal(error)),
        })?;
    let metadata = judge_capture(&capture, MARKER_FILE, uid)
        .map_err(|_| WorkFailure::Operation(ProjectAdmissionRefusal::MarkerCustody("marker-custody")))?;
    let raw = match opensip_platform::read_bounded_observed(&file, PROJECT_MARKER_SIZE, work)? {
        Ok(raw) => raw,
        Err(ReadFailure::Bound) => return Ok(MarkerObservation::Malformed),
        Err(error) => {
            return refuse(ProjectAdmissionRefusal::Io(io::Error::other(format!("{error:?}"))));
        }
    };
    Ok(match ProjectIdMarker::decode(&raw) {
        Ok(marker) => MarkerObservation::Present {
            project: marker.project_id().to_owned(),
            metadata,
        },
        Err(_) => MarkerObservation::Malformed,
    })
}

/// `.opensip`'s custody judgment that did not pass: I/O is the host I/O row
/// (item 8); every other refusal is `marker-directory-custody`.
fn marker_directory_refusal(refusal: ProjectChainRefusal) -> ProjectAdmissionRefusal {
    if refusal.row() == ProjectChainRow::HostIo {
        ProjectAdmissionRefusal::Chain(refusal)
    } else {
        ProjectAdmissionRefusal::MarkerCustody("marker-directory-custody")
    }
}
/// A failed ACL capture of the marker: I/O is the host I/O row (item 8);
/// an unsupported, malformed or changed capture is a custody judgment that
/// could not pass, so it stays marker custody.
fn marker_capture_refusal(error: opensip_platform::DescriptorAclCaptureError) -> ProjectAdmissionRefusal {
    match error {
        opensip_platform::DescriptorAclCaptureError::Io(error) => ProjectAdmissionRefusal::Io(error),
        _ => ProjectAdmissionRefusal::MarkerCustody("marker-custody"),
    }
}

/// The root's native incarnation (item 4): APFS volume UUID, inode, birth.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) struct Incarnation {
    pub(crate) volume: [u8; 16],
    pub(crate) inode: u64,
    pub(crate) birth_seconds: i64,
    pub(crate) birth_nanoseconds: u32,
}
fn same_incarnation(entry: &ProjectRegistryEntry, incarnation: &Incarnation) -> bool {
    let root = entry.root();
    root.volume_uuid_bytes() == &incarnation.volume
        && root.inode() == incarnation.inode
        && root.birth_seconds() == incarnation.birth_seconds
        && root.birth_nanoseconds() == incarnation.birth_nanoseconds
}

/// The registry owner's classification (registry draft r4, the table under
/// "classify observations without writing").
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) enum Classification {
    /// The exact marker and exactly one matching ACTIVE row: same ProjectId,
    /// root path and incarnation, and no competing live row.
    Eligible { namespace: String, project: String },
    /// The marker positively absent and no live row binds this locator or
    /// incarnation.
    FirstUseCandidate,
    /// A matching RESERVED row, with the marker absent or exact.
    RecoveryNeeded { namespace: String, project: String },
    /// A marker without a matching live row, or a matching ACTIVE row with
    /// the marker missing.
    OneSided,
    /// Positive disagreement, a duplicate live identity, or a malformed
    /// marker.
    Contradiction,
}
/// Classify (pure). Live rows are RESERVED and ACTIVE; terminal history is
/// never live admission. A live row is relevant when it binds this
/// locator (platform and exact path bytes), this incarnation, or the
/// marker's ProjectId.
pub(crate) fn classify(
    entries: &[ProjectRegistryEntry],
    path: &[u8],
    incarnation: &Incarnation,
    marker: &MarkerObservation,
) -> Classification {
    if matches!(marker, MarkerObservation::Malformed) {
        return Classification::Contradiction;
    }
    let marked = marker.project();
    let mut relevant = entries.iter().filter(|entry| {
        matches!(
            entry.status(),
            ProjectRegistryStatus::Reserved | ProjectRegistryStatus::Active
        ) && (entry.root().platform() == ProjectRootPlatform::Macos
            && entry.root().path_bytes() == path
            || same_incarnation(entry, incarnation)
            || marked == Some(entry.project_id()))
    });
    let Some(row) = relevant.next() else {
        return match marker {
            MarkerObservation::Absent => Classification::FirstUseCandidate,
            _ => Classification::OneSided,
        };
    };
    if relevant.next().is_some() {
        return Classification::Contradiction;
    }
    let agrees = row.root().platform() == ProjectRootPlatform::Macos
        && row.root().path_bytes() == path
        && same_incarnation(row, incarnation)
        && marked.is_none_or(|project| project == row.project_id());
    if !agrees {
        return Classification::Contradiction;
    }
    let namespace = row.namespace_id().to_owned();
    let project = row.project_id().to_owned();
    match (row.status(), marked) {
        (ProjectRegistryStatus::Active, Some(_)) => Classification::Eligible { namespace, project },
        (ProjectRegistryStatus::Active, None) => Classification::OneSided,
        (_, _) => Classification::RecoveryNeeded { namespace, project },
    }
}

/// Item 4: a project root admission. Private, not Clone, not serializable,
/// produced only under a held installation fence. It holds the X2a chain,
/// S3's selection, the root's incarnation, the marker observation, the
/// registry capture (R0) and the classification. It grants nothing in this
/// unit: every grant also requires item 6a's tracking observation (X2b-2).
pub(crate) struct ProjectRootAdmission {
    chain: ProjectChain,
    selected: Selected,
    incarnation: Incarnation,
    marker: MarkerObservation,
    registry: RegistryCapture,
    classification: Classification,
    /// The analysis path's configuration carriers (M3-B unit B1-b); `None`
    /// on the legacy path, which captures none.
    carriers: Option<ConfigCarriers>,
}
/// A `ProjectRootAdmission` moved apart into its owners (unit X2c).
pub(super) struct AdmissionParts {
    pub(super) chain: ProjectChain,
    pub(super) selected: Selected,
    pub(super) incarnation: Incarnation,
    pub(super) marker: MarkerObservation,
    pub(super) registry: RegistryCapture,
    pub(super) classification: Classification,
}
impl std::fmt::Debug for ProjectRootAdmission {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("ProjectRootAdmission")
            .field("selected", &self.selected)
            .field("classification", &self.classification)
            .finish_non_exhaustive()
    }
}
impl ProjectRootAdmission {
    pub(crate) fn selected(&self) -> &Selected {
        &self.selected
    }
    pub(crate) fn classification(&self) -> &Classification {
        &self.classification
    }
    pub(crate) fn incarnation(&self) -> &Incarnation {
        &self.incarnation
    }
    pub(crate) fn marker(&self) -> &MarkerObservation {
        &self.marker
    }
    pub(crate) fn registry(&self) -> &RegistryCapture {
        &self.registry
    }
    pub(crate) fn chain(&self) -> &ProjectChain {
        &self.chain
    }
    /// The analysis path's configuration carriers; `None` on the legacy path.
    pub(crate) fn carriers(&self) -> Option<&ConfigCarriers> {
        self.carriers.as_ref()
    }
    /// The admission as its owners, for first registration (unit X2c),
    /// which moves them into the registered project.
    pub(super) fn into_parts(self) -> AdmissionParts {
        AdmissionParts {
            chain: self.chain,
            selected: self.selected,
            incarnation: self.incarnation,
            marker: self.marker,
            registry: self.registry,
            classification: self.classification,
        }
    }
    /// Law X4 r7 item 4 (unit X4a): the original owners only, after the fence
    /// is released: the chain (names, custody, volume, birth), the root's
    /// incarnation and the marker (still absent, or the same file
    /// unchanged). The registry is provenance and is not rechecked.
    pub(crate) fn recheck_owners(
        &self,
        uid: u32,
        policy: &ProjectChainPolicy<'_>,
        work: &mut WorkScope<'_>,
    ) -> Result<(), Failure> {
        self.chain.recheck(uid, policy, work).map_err(chain)?;
        if sample_incarnation(&self.chain, work)? != self.incarnation {
            return refuse(ProjectAdmissionRefusal::Changed);
        }
        if observe_marker(self.chain.root(), uid, policy, work)? != self.marker {
            return refuse(ProjectAdmissionRefusal::Changed);
        }
        Ok(())
    }
    /// Item 3's recheck set with the project chain added: the chain (names,
    /// custody, volume, birth), the root's volume UUID, the marker (still
    /// absent, or the same file unchanged), and the registry (the same
    /// judged file unchanged, and `v1` still absent). Charged to `work`.
    pub(crate) fn recheck(
        &self,
        uid: u32,
        installation: &RetainedDirectory,
        judged: &RequiredFile,
        policy: &ProjectChainPolicy<'_>,
        work: &mut WorkScope<'_>,
    ) -> Result<(), Failure> {
        self.recheck_waived(uid, installation, judged, policy, None, work)
    }
    /// `recheck` with the invocation's owner waiver (M3-B unit B2-b3a,
    /// LD-B2B3-9), which reaches the chain's root judgment again only when
    /// the walk waived it.
    pub(crate) fn recheck_waived(
        &self,
        uid: u32,
        installation: &RetainedDirectory,
        judged: &RequiredFile,
        policy: &ProjectChainPolicy<'_>,
        waiver: Option<&ProjectOwnerWaiver>,
        work: &mut WorkScope<'_>,
    ) -> Result<(), Failure> {
        self.chain.recheck_waived(uid, policy, waiver, work).map_err(chain)?;
        if sample_incarnation(&self.chain, work)? != self.incarnation {
            return refuse(ProjectAdmissionRefusal::Changed);
        }
        let marker = observe_marker(self.chain.root(), uid, policy, work)?;
        if marker != self.marker {
            return refuse(ProjectAdmissionRefusal::Changed);
        }
        if registry_sample(installation, judged, work)? != self.registry.metadata {
            return refuse(ProjectAdmissionRefusal::Changed);
        }
        old_name_absent(installation, work)?;
        // X2 r9 item 3a: the carriers' samples and absences join this set
        // on the analysis path only.
        match &self.carriers {
            Some(carriers) => carriers.recheck(self.chain.root(), uid, policy, work),
            None => Ok(()),
        }
    }
}

/// The root's incarnation from the retained root descriptor: the APFS
/// volume UUID (charged first; unsupported refuses, with no device or fsid
/// substitute) on the same device as the X2a birth sample.
pub(super) fn sample_incarnation(
    chain: &ProjectChain,
    work: &mut WorkScope<'_>,
) -> Result<Incarnation, Failure> {
    let volume = work.run(opensip_platform::directory_volume_observation_cost(), |_| {
        chain
            .root()
            .observe_volume()
            .map_err(|error| WorkFailure::Operation(ProjectAdmissionRefusal::VolumeUnsupported(error)))
    })?;
    let birth = chain.birth();
    if volume.metadata().device != birth.metadata().device || volume.metadata().inode != birth.metadata().inode {
        return refuse(ProjectAdmissionRefusal::Changed);
    }
    Ok(Incarnation {
        volume: *volume.uuid_bytes(),
        inode: birth.metadata().inode,
        birth_seconds: birth.birth_seconds(),
        birth_nanoseconds: birth.birth_nanoseconds(),
    })
}

/// Items 2 to 5 under a held fence, in law order: S3 selection; item 2's
/// placement and X2a's chain walk (placement runs before any open, so an
/// outside-home root refuses before any registry read); the incarnation;
/// the marker; then the one registry capture; then the classification.
#[allow(clippy::too_many_arguments)]
pub(crate) fn admit_project_root(
    home: &Path,
    uid: u32,
    launch: &Path,
    explicit: Option<&Path>,
    installation: &RetainedDirectory,
    judged: &RequiredFile,
    policy: &ProjectChainPolicy<'_>,
    work: &mut WorkScope<'_>,
) -> Result<ProjectRootAdmission, Failure> {
    let selected = select_project_root(launch, explicit, home, uid, policy, work)?;
    let chain = walk_project_chain(home, selected.root(), uid, policy, work).map_err(chain)?;
    let incarnation = sample_incarnation(&chain, work)?;
    let marker = observe_marker(chain.root(), uid, policy, work)?;
    let registry = capture_registry(installation, judged, work)?;
    let classification = classify(
        registry.document().entries(),
        chain.spelling().as_os_str().as_bytes(),
        &incarnation,
        &marker,
    );
    Ok(ProjectRootAdmission {
        chain,
        selected,
        incarnation,
        marker,
        registry,
        classification,
        carriers: None,
    })
}

// ---------------------------------------------------------------------------
// M3-B unit B1-b (X2 r9 item 3a): the configuration carriers, the analysis
// path only. The legacy admission above captures none.
// ---------------------------------------------------------------------------

/// The interactive local carrier's file under `.opensip`.
pub(crate) const LOCAL_CONFIG_FILE: &str = "local.json";

// Test-only count of local-carrier lookups (Codex B1B-R2-RF-02): CI must make
// none, which an aggregate charge comparison cannot show.
#[cfg(test)]
thread_local! {
    static LOCAL_LOOKUPS: std::cell::Cell<usize> = const { std::cell::Cell::new(0) };
}

/// Whether the interactive local carrier is read (M3-B item 3). The host
/// computes it once from the invocation mode; in CI the local carrier is
/// never looked up at all.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum LocalCarrierPolicy {
    Interactive,
    NonInteractive,
}

/// One captured configuration carrier: its path relative to the root, the
/// full metadata sample of the judged file and its exact bytes, read once
/// from the judged descriptor within the 4 MiB custody bound.
#[derive(Clone, PartialEq, Eq)]
pub(crate) struct ConfigCarrier {
    relative: &'static str,
    metadata: DescriptorMetadata,
    bytes: Vec<u8>,
}
impl std::fmt::Debug for ConfigCarrier {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("ConfigCarrier")
            .field("relative", &self.relative)
            .field("bytes", &self.bytes.len())
            .finish_non_exhaustive()
    }
}
impl ConfigCarrier {
    pub(crate) fn relative(&self) -> &'static str {
        self.relative
    }
    pub(crate) fn bytes(&self) -> &[u8] {
        &self.bytes
    }
}

/// `opensip.json`: captured, or positively absent (and rechecked absent).
#[derive(Debug, Clone, PartialEq, Eq)]
enum ProjectCarrier {
    Captured(ConfigCarrier),
    Absent,
}
/// The interactive local carrier: `.opensip` absent, `local.json` absent
/// under the judged `.opensip`, or captured. Each is rechecked.
#[derive(Debug, Clone, PartialEq, Eq)]
enum LocalCarrier {
    DirectoryAbsent,
    Absent,
    Captured(ConfigCarrier),
}

/// The analysis path's carriers and absence observations. `local` is
/// `None` in CI: nothing about `.opensip/local.json` was observed.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct ConfigCarriers {
    project: ProjectCarrier,
    local: Option<LocalCarrier>,
}
impl ConfigCarriers {
    /// The captured `opensip.json`, if present.
    pub(crate) fn project(&self) -> Option<&ConfigCarrier> {
        match &self.project {
            ProjectCarrier::Captured(carrier) => Some(carrier),
            ProjectCarrier::Absent => None,
        }
    }
    /// The captured `.opensip/local.json`, if read and present.
    pub(crate) fn local(&self) -> Option<&ConfigCarrier> {
        match &self.local {
            Some(LocalCarrier::Captured(carrier)) => Some(carrier),
            Some(LocalCarrier::DirectoryAbsent | LocalCarrier::Absent) | None => None,
        }
    }
    /// Item 3's recheck under the held fence: each captured carrier is the
    /// same file, unchanged (full sample), and each observed absence holds.
    fn recheck(
        &self,
        root: &RetainedDirectory,
        uid: u32,
        policy: &ProjectChainPolicy<'_>,
        work: &mut WorkScope<'_>,
    ) -> Result<(), Failure> {
        match &self.project {
            ProjectCarrier::Captured(carrier) => same_carrier(root, carrier, work)?,
            ProjectCarrier::Absent => still_absent(root, CONFIG_FILE, "opensip.json:appeared", work)?,
        }
        match &self.local {
            None => {}
            Some(LocalCarrier::DirectoryAbsent) => {
                still_absent(root, MARKER_DIRECTORY, ".opensip:appeared", work)?;
            }
            Some(LocalCarrier::Absent) => {
                let directory = local_directory(root, uid, policy, work)?
                    .ok_or(WorkFailure::Operation(ProjectAdmissionRefusal::Changed))?;
                still_absent(&directory, LOCAL_CONFIG_FILE, "local.json:appeared", work)?;
            }
            Some(LocalCarrier::Captured(carrier)) => {
                let directory = local_directory(root, uid, policy, work)?
                    .ok_or(WorkFailure::Operation(ProjectAdmissionRefusal::Changed))?;
                same_carrier(&directory, carrier, work)?;
            }
        }
        Ok(())
    }
}

/// A charged positive-absence observation that must still hold.
fn still_absent(
    directory: &RetainedDirectory,
    name: &str,
    appeared: &'static str,
    work: &mut WorkScope<'_>,
) -> Result<(), Failure> {
    let absent = directory
        .observe_child_absent_accounted(OsStr::new(name), work)
        .map_err(io_failure)?;
    if absent {
        Ok(())
    } else {
        refuse(ProjectAdmissionRefusal::Carrier(appeared))
    }
}

/// The recheck of one captured carrier: reopened no-follow by its name in
/// its directory, its full metadata sample equal to the captured one.
fn same_carrier(
    directory: &RetainedDirectory,
    carrier: &ConfigCarrier,
    work: &mut WorkScope<'_>,
) -> Result<(), Failure> {
    let name = carrier.relative.rsplit('/').next().unwrap_or(carrier.relative);
    let file = match open_file(directory, name, work)? {
        Ok(file) => file,
        Err(error) if error.kind() == io::ErrorKind::NotFound => {
            return refuse(ProjectAdmissionRefusal::Changed);
        }
        Err(error) if error.raw_os_error() == Some(ELOOP) || error.kind() == io::ErrorKind::InvalidInput => {
            return refuse(ProjectAdmissionRefusal::Changed);
        }
        Err(error) => return refuse(ProjectAdmissionRefusal::Io(error)),
    };
    if carrier_sample(&file, work)? != carrier.metadata {
        return refuse(ProjectAdmissionRefusal::Changed);
    }
    Ok(())
}

/// One charged full metadata sample of a carrier descriptor.
fn carrier_sample(file: &File, work: &mut WorkScope<'_>) -> Result<DescriptorMetadata, Failure> {
    opensip_platform::capture_descriptor_acl_accounted(file, work)
        .map(|sample| sample.metadata().clone())
        .map_err(|failure| match failure {
            WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
            WorkFailure::Operation(error) => WorkFailure::Operation(ProjectAdmissionRefusal::Io(
                io::Error::other(format!("{error:?}")),
            )),
        })
}

/// X2 r9 item 3a's read of a judged carrier from its retained descriptor,
/// bound to its custody judgment (Codex B1B-R1-RF-01): a sample that must
/// equal the one the judgment passed on, one read within 4 MiB charged to
/// the ledger, and a second sample that must equal it too. The full sample
/// includes the change time, so any write, mode, owner or ACL change since
/// the judgment refuses; the judgment is never re-baselined.
fn capture_carrier(
    file: &File,
    judged: &DescriptorMetadata,
    relative: &'static str,
    work: &mut WorkScope<'_>,
) -> Result<ConfigCarrier, Failure> {
    if carrier_sample(file, work)? != *judged {
        return refuse(ProjectAdmissionRefusal::Changed);
    }
    let metadata = judged.clone();
    let limit = usize::try_from(super::MAX_CONFIG_BYTES).unwrap_or(usize::MAX);
    let bytes = match opensip_platform::read_bounded_observed(file, limit, work)? {
        Ok(bytes) => bytes,
        // Judged within 4 MiB, so a longer read means the file changed.
        Err(ReadFailure::Bound) => return refuse(ProjectAdmissionRefusal::Changed),
        Err(error) => {
            return refuse(ProjectAdmissionRefusal::Io(io::Error::other(format!("{error:?}"))));
        }
    };
    if carrier_sample(file, work)? != metadata {
        return refuse(ProjectAdmissionRefusal::Changed);
    }
    Ok(ConfigCarrier {
        relative,
        metadata,
        bytes,
    })
}

/// `.opensip` under the root, judged by S3 directory custody as the marker
/// observation judges it; `None` when positively absent. A malformed or
/// refused directory refuses the local carrier.
fn local_directory(
    root: &RetainedDirectory,
    uid: u32,
    policy: &ProjectChainPolicy<'_>,
    work: &mut WorkScope<'_>,
) -> Result<Option<RetainedDirectory>, Failure> {
    #[cfg(test)]
    LOCAL_LOOKUPS.with(|count| count.set(count.get() + 1));
    let directory = match work.run(
        opensip_platform::open_child_directory_cost(OsStr::new(MARKER_DIRECTORY)),
        |_| Ok::<_, Failure>(root.open_child_directory(OsStr::new(MARKER_DIRECTORY))),
    )? {
        Ok(directory) => directory,
        Err(error) if error.kind() == io::ErrorKind::NotFound => return Ok(None),
        Err(error)
            if error.raw_os_error() == Some(ELOOP)
                || error.kind() == io::ErrorKind::NotADirectory
                || error.kind() == io::ErrorKind::InvalidInput =>
        {
            return refuse(ProjectAdmissionRefusal::Carrier("local-directory-custody"));
        }
        Err(error) => return refuse(ProjectAdmissionRefusal::Io(error)),
    };
    match judge_project_object(directory.as_file(), ProjectObject::Directory, uid, policy, work) {
        Ok(()) => Ok(Some(directory)),
        Err(WorkFailure::Operation(refusal)) if refusal.row() == ProjectChainRow::HostIo => {
            refuse(ProjectAdmissionRefusal::Chain(refusal))
        }
        Err(WorkFailure::Operation(_)) => refuse(ProjectAdmissionRefusal::Carrier("local-directory-custody")),
        Err(WorkFailure::Budget(budget)) => Err(WorkFailure::Budget(budget)),
    }
}

/// Item 3a's captures after the chain walk, the incarnation and the marker:
/// `opensip.json` from the descriptor selection judged (or its absence, by a
/// charged lookup), and, when interactive only, `.opensip/local.json` judged
/// as configuration custody (or the absence of either).
/// `.opensip/local.json` under the judged `.opensip`, judged by configuration
/// custody: its descriptor and the sample the judgment passed on, or `None`
/// when positively absent.
fn judge_local(
    directory: &RetainedDirectory,
    uid: u32,
    policy: &ProjectChainPolicy<'_>,
    work: &mut WorkScope<'_>,
) -> Result<Option<(File, DescriptorMetadata)>, Failure> {
    let file = match open_file(directory, LOCAL_CONFIG_FILE, work)? {
        Ok(file) => file,
        Err(error) if error.kind() == io::ErrorKind::NotFound => return Ok(None),
        Err(error) if error.raw_os_error() == Some(ELOOP) => {
            return refuse(ProjectAdmissionRefusal::Carrier("local-symlink"));
        }
        Err(error) if error.kind() == io::ErrorKind::InvalidInput => {
            return refuse(ProjectAdmissionRefusal::Carrier("local-not-a-regular-file"));
        }
        Err(error) => return refuse(ProjectAdmissionRefusal::Io(error)),
    };
    match judge_project_object_sampled(&file, ProjectObject::ConfigurationFile, uid, policy, work) {
        Ok(judged) => Ok(Some((file, judged))),
        Err(WorkFailure::Operation(refusal)) if refusal.row() == ProjectChainRow::HostIo => {
            refuse(ProjectAdmissionRefusal::Chain(refusal))
        }
        Err(WorkFailure::Operation(_)) => refuse(ProjectAdmissionRefusal::Carrier("local-custody")),
        Err(WorkFailure::Budget(budget)) => Err(WorkFailure::Budget(budget)),
    }
}

fn capture_carriers(
    root: &RetainedDirectory,
    selected_config: Option<(File, DescriptorMetadata)>,
    local: LocalCarrierPolicy,
    uid: u32,
    policy: &ProjectChainPolicy<'_>,
    work: &mut WorkScope<'_>,
) -> Result<ConfigCarriers, Failure> {
    let project = match selected_config {
        Some((file, judged)) => ProjectCarrier::Captured(capture_carrier(&file, &judged, CONFIG_FILE, work)?),
        None => {
            still_absent(root, CONFIG_FILE, "opensip.json:appeared", work)?;
            ProjectCarrier::Absent
        }
    };
    let local = match local {
        LocalCarrierPolicy::NonInteractive => None,
        LocalCarrierPolicy::Interactive => Some(match local_directory(root, uid, policy, work)? {
            None => LocalCarrier::DirectoryAbsent,
            Some(directory) => match judge_local(&directory, uid, policy, work)? {
                None => LocalCarrier::Absent,
                Some((file, judged)) => {
                    LocalCarrier::Captured(capture_carrier(&file, &judged, ".opensip/local.json", work)?)
                }
            },
        }),
    };
    Ok(ConfigCarriers { project, local })
}

/// The analysis path's first phase (M3-B unit B1-b; X2 r9 item 3a's order):
/// S3 selection retaining the judged `opensip.json`, the chain walk, the
/// incarnation, the marker, then the carriers. It has no registry capture:
/// configuration resolution and pack admission (X12 r4) run on it before
/// `capture_registry`, item 5. Not Clone; produced under a held fence.
pub(crate) struct CarrierAdmission {
    chain: ProjectChain,
    selected: Selected,
    incarnation: Incarnation,
    marker: MarkerObservation,
    carriers: ConfigCarriers,
}
impl std::fmt::Debug for CarrierAdmission {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("CarrierAdmission")
            .field("selected", &self.selected)
            .field("carriers", &self.carriers)
            .finish_non_exhaustive()
    }
}
impl CarrierAdmission {
    pub(crate) fn selected(&self) -> &Selected {
        &self.selected
    }
    pub(crate) fn carriers(&self) -> &ConfigCarriers {
        &self.carriers
    }
    /// Item 5, after configuration resolution and pack admission: the one
    /// registry capture, then the classification. The carriers stay in the
    /// admission and join its recheck.
    pub(crate) fn capture_registry(
        self,
        installation: &RetainedDirectory,
        judged: &RequiredFile,
        work: &mut WorkScope<'_>,
    ) -> Result<ProjectRootAdmission, Failure> {
        let registry = capture_registry(installation, judged, work)?;
        let classification = classify(
            registry.document().entries(),
            self.chain.spelling().as_os_str().as_bytes(),
            &self.incarnation,
            &self.marker,
        );
        Ok(ProjectRootAdmission {
            chain: self.chain,
            selected: self.selected,
            incarnation: self.incarnation,
            marker: self.marker,
            registry,
            classification,
            carriers: Some(self.carriers),
        })
    }
}

/// The analysis path's first phase under a held fence, in law order: S3
/// selection (retaining the judged `opensip.json`), item 2's placement and
/// the chain walk, the incarnation, the marker, then X2 r9 item 3a's
/// carriers. No registry is read. Selection records its upward provenance
/// into `upward` as it runs, so a refusal keeps its rows (M3-B unit B2-b3a),
/// and `waiver` reaches the explicit root's custody, its `opensip.json` and
/// the chain walk's root judgment (LD-B2B3-9).
#[allow(clippy::too_many_arguments)]
pub(crate) fn admit_project_root_for_analysis(
    home: &Path,
    uid: u32,
    launch: &Path,
    explicit: Option<&Path>,
    waiver: Option<&ProjectOwnerWaiver>,
    local: LocalCarrierPolicy,
    policy: &ProjectChainPolicy<'_>,
    upward: &mut UpwardRecord,
    work: &mut WorkScope<'_>,
) -> Result<CarrierAdmission, Failure> {
    let (selected, config) = select(
        launch,
        explicit,
        home,
        uid,
        policy,
        true,
        waiver,
        Some(upward),
        work,
    )?;
    let chain = walk_project_chain_waived(home, selected.root(), uid, policy, waiver, work)
        .map_err(chain)?;
    let incarnation = sample_incarnation(&chain, work)?;
    let marker = observe_marker(chain.root(), uid, policy, work)?;
    let carriers = capture_carriers(chain.root(), config, local, uid, policy, work)?;
    Ok(CarrierAdmission {
        chain,
        selected,
        incarnation,
        marker,
        carriers,
    })
}

/// The registry's judged required file among a session's required files.
pub(crate) fn judged_registry(required: &[RequiredFile]) -> Option<&RequiredFile> {
    required.iter().find(|file| file.relative() == REGISTRY)
}

#[cfg(test)]
mod tests {
    include!("project_admission_tests.rs");
    include!("project_admission_carrier_tests.rs");
    include!("project_admission_legacy_probe_tests.rs");
    include!("project_admission_upward_tests.rs");
}
