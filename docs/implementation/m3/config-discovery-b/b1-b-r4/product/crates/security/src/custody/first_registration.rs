// Law X2 r8 item 6 (unit X2c): first registration on the durable write
// gate, with the registry replacement primitive and the create-or-admit of
// `I/host`, `I/host/projects` and the project's `.opensip`. It follows the
// registry owner's ordinary first-use sequence exactly, inside the held
// fence, on the gate's one ledger:
// - preconditions before any effect: a FirstUseCandidate with the marker
//   absent, the admission's own recheck (chain, incarnation, marker, R0,
//   v1 absence), item 6a's tracking observation rechecked, no transition
//   state beside the lineage, capacity, collisions against all history,
//   occupancy of the candidate namespace path and the private custody of a
//   present `host` or `projects`;
// - RESERVED through the replacement primitive (R0 to R1);
// - the namespace `I/host/projects/N` with exactly `writer.lease` and
//   `readers.lease`, by a staged no-replace directory publication;
// - `.opensip`, created or admitted, then the 92-byte marker no-replace;
// - every current owner rechecked, then ACTIVE through the replacement
//   primitive (R1 to R2).
// Each effect reserves its own confirmation work before it runs. Any failed
// or uncertain step closes the gate's ledger: no later step, no retry and
// no deletion. Each leftover is the registry owner's explicit-recovery case,
// which is not implemented here. The write-gate entries for project
// admission and tracking (X2b's, read side only until now) are here too.
// Every refusal names its item 8 row; the public projection is the
// composition owner's. Namespace admission and leases are X2d's
// (`namespace_lease`, which reuses this unit's owner checks and rows); the
// operation handoff (X2e) is a later unit. Library only.
use super::git_tracking::{
    Failure as TrackingFailure, TrackingInputs, TrackingObservation, TrackingRefusal, TrackingRow,
    observe_tracking, recheck_tracking,
};
use super::installation_admission::{
    DurableBarrierQualification, DurableInstallation, DurableWriteGate, GateRefusal, plus, times,
};
use super::installation_routing::gate_refusal;
use super::project_admission::{
    CarrierAdmission, Classification, Failure as AdmissionFailure, Incarnation, LocalCarrierPolicy,
    MARKER_DIRECTORY, MARKER_FILE, MarkerObservation, ProjectAdmissionRefusal, ProjectAdmissionRow,
    ProjectRootAdmission, REGISTRY, Selected, admit_project_root, admit_project_root_for_analysis,
    classify, judged_registry, old_name_absent, sample_incarnation,
};
use super::project_chain::{
    ProjectChain, ProjectChainPolicy, ProjectChainRefusal, ProjectChainRow, ProjectObject,
    judge_project_object,
};
use crate::InstallationTermination as T;
use crate::private_access::{
    PreparePrivateError, PrivateObjectKind, assess_private_descendant_capture,
    observe_private_directory, prepare_fresh_private_sample,
};
use crate::trust::PrimitivePolicy;
use opensip_identity::{
    JsonInteger, JsonValue as V, PROJECT_MARKER_SIZE, PROJECT_REGISTRY_CAP,
    PROJECT_REGISTRY_ROW_CAP, ProjectAllocationKind, ProjectIdMarker, ProjectRegistryDocument,
    ProjectRegistryEntry, ProjectRegistryError, ProjectRegistryStatus, canonical_bytes,
};
use opensip_platform::{
    DescriptorAclCapture, DescriptorAclCaptureError, DescriptorFilesystem, DescriptorMetadata,
    DirectoryBarrier, DirectoryRenameClass, DirectoryVisitError, ExclusiveDirectoryError,
    ExclusiveDirectoryOutcome, ExclusiveRegularError, ExclusiveRegularOutcome,
    NamedDirectoryPublication, NewRegularWriteError, RenameReplaceError, RetainedDirectory,
    WorkCost, WorkFailure, WorkScope,
};
use std::collections::{BTreeMap, BTreeSet};
use std::ffi::{OsStr, OsString};
use std::fs::File;
use std::io::{self, Read};
use std::os::unix::ffi::OsStrExt;
use std::os::unix::fs::MetadataExt;
use std::path::{Path, PathBuf};

/// The installation's project parents (item 6 step 3) and the namespace's
/// two lease carriers (the registry owner's initial namespace profile).
pub(super) const HOST: &str = "host";
pub(super) const PROJECTS: &str = "projects";
pub(super) const WRITER_LEASE: &str = "writer.lease";
pub(super) const READERS_LEASE: &str = "readers.lease";
/// The installation's transition directory and the one entry P0 gives it.
const TRANSITIONS: &str = "transitions";
const LINEAGE: &[u8] = b"lineage";
/// The registry owner: at most eight candidates of each kind.
const CANDIDATES: usize = 8;
/// The marker's fixed prefix (identity §2).
const MARKER_PREFIX: &[u8] = b"opensip-project-id-v1\n";
/// Directory scans: `.`, `..` and the admitted names, with one more entry
/// to see an extra name, and a name-byte ceiling far above any of them.
const SCAN_ENTRIES: usize = 5;
const SCAN_NAME_BYTES: usize = 4 * 256;
/// One status read with a buffer no smaller than the native `stat`.
pub(super) const STATUS: WorkCost = WorkCost {
    objects: 0,
    edges: 1,
    bytes: 512,
};
/// One bounded directory scan: the stream, its entries, names and a dirent.
const SCAN: WorkCost = WorkCost {
    objects: 2,
    edges: 3 + SCAN_ENTRIES,
    bytes: SCAN_NAME_BYTES + 1024,
};
/// One OS entropy draw into its buffer and its hex spelling.
const DRAW: WorkCost = WorkCost {
    objects: 2,
    edges: 1,
    bytes: 32 + 64 + 5,
};
/// The publication's exact-name recheck: two binding rechecks (an open and
/// four status reads each) around one native name sample.
const EXACT_NAME: WorkCost = WorkCost {
    objects: 2,
    edges: 10,
    bytes: 8 * 512,
};
/// A canonical root path is at most 4096 bytes (8192 hex digits); with every
/// other member at its widest a row is below this many bytes.
const ROW_BOUND: usize = 8192 + 1024;

// ------------------------------------------------------------- refusals

/// The registration step a refusal stopped (item 6's steps 2 to 6, with the
/// preconditions before them and the final confirmation after ACTIVE).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum Step {
    Preconditions,
    Reserved,
    Namespace,
    MarkerDirectory,
    Marker,
    Active,
    Confirmed,
    /// Law X2 item 7 (unit X2d): namespace admission and its lease.
    Lease,
    /// Law X2 item 7a (unit X2e): the operation handoff, from the
    /// lease-free point to the fence's release.
    Handoff,
}
/// The owner a refusal concerns.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum Owner {
    Installation,
    Registry,
    Transitions,
    Host,
    Projects,
    Namespace,
    Root,
    MarkerDirectory,
    Marker,
    /// `I/trust`, the carrier floor's parent (law X3b item 2), confirmed by
    /// the operation handoff (unit X2e with X3b-3).
    Trust,
}
impl Owner {
    /// Project objects are judged by S3; the rest are installation-private.
    fn in_project(self) -> bool {
        matches!(self, Self::Root | Self::MarkerDirectory | Self::Marker)
    }
}

/// Why first registration refused. Each variant has one item 8 row (`row`).
#[derive(Debug)]
pub(crate) enum RegistrationRefusal {
    /// Item 4: only a FirstUseCandidate with the marker positively absent
    /// registers.
    NotFirstUse(Classification),
    /// The admission's own recheck (chain, incarnation, marker, R0, v1).
    Admission(ProjectAdmissionRefusal),
    /// Item 6a's tracking observation, rechecked before any effect and
    /// before ACTIVE.
    Tracking(TrackingRefusal),
    /// The registry owner's active-transition-recovery gate: `transitions`
    /// holds an entry other than P0's `lineage`.
    TransitionActive,
    /// An owner failed its custody (subject as item 8 or 468 spell it).
    Custody(Owner, &'static str),
    /// Item 8's scope-limit row: `field:count>limit`.
    ScopeLimit { field: &'static str, count: usize },
    /// The OS CSPRNG returned no complete draw.
    Entropy,
    /// Eight candidates of this kind all collided.
    Exhausted(&'static str),
    /// A constructed replacement failed the decoder (a broken composition).
    Document(ProjectRegistryError),
    /// A retained owner, its name binding or its bytes changed.
    Changed(Owner),
    /// Native I/O, including a failed barrier, at this step on this owner.
    Io(Step, Owner, io::Error),
    /// A barrier receipt for another handle, at this step on this owner.
    BarrierReceipt(Step, Owner),
    /// A composition that cannot arise from the admitted inputs.
    Invariant(&'static str),
}
/// Item 8's rows, named for the composition owner's projection.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) enum RegistrationRow {
    /// An admission row (X2b-1's), unchanged.
    Admission(ProjectAdmissionRow),
    /// `PROJECT.ROOT_CUSTODY_REFUSED`, with this subject.
    RootCustody(&'static str),
    /// 468 item 6's custody row for an installation-private owner.
    InstallationCustody(&'static str),
    /// 468 item 6's incomplete-installation row (unavailable).
    Incomplete,
    /// `PROJECT.SCOPE_LIMIT`, request-rejected, with this S12 subject.
    ScopeLimit(String),
    /// The host I/O row (entropy, exhaustion, I/O and barriers).
    HostIo,
    /// The host invariant row: a broken composition.
    Invariant,
    /// The busy row (`LEDGER.BUSY_TIMEOUT` / `PROJECT.BUSY`): a project
    /// lease is held elsewhere (item 7, unit X2d).
    Busy,
}
impl RegistrationRefusal {
    pub(crate) fn row(&self) -> RegistrationRow {
        use RegistrationRow as Row;
        match self {
            Self::NotFirstUse(Classification::RecoveryNeeded { .. } | Classification::OneSided) => {
                Row::RootCustody("identity-recovery-required")
            }
            Self::NotFirstUse(Classification::Contradiction) => {
                Row::RootCustody("identity-contradiction")
            }
            Self::NotFirstUse(
                Classification::Eligible { .. } | Classification::FirstUseCandidate,
            ) => Row::Invariant,
            Self::Admission(refusal) => Row::Admission(refusal.row()),
            Self::Tracking(refusal) => match refusal.row() {
                TrackingRow::RootCustody(subject) => Row::RootCustody(subject),
                TrackingRow::HostIo => Row::HostIo,
            },
            Self::TransitionActive => Row::Incomplete,
            Self::Custody(owner, subject) if owner.in_project() => Row::RootCustody(subject),
            Self::Custody(_, subject) => Row::InstallationCustody(subject),
            Self::ScopeLimit { field, count } => {
                let limit = if *field == "registry-bytes" {
                    PROJECT_REGISTRY_CAP
                } else {
                    PROJECT_REGISTRY_ROW_CAP
                };
                Row::ScopeLimit(format!("{field}:{count}>{limit}"))
            }
            Self::Entropy | Self::Exhausted(_) | Self::Io(..) => Row::HostIo,
            Self::Changed(_) => Row::Admission(ProjectAdmissionRow::RequiredFilesChanged),
            Self::Document(_) | Self::BarrierReceipt(..) | Self::Invariant(_) => Row::Invariant,
        }
    }
}
pub(crate) type Failure = WorkFailure<RegistrationRefusal>;
fn refuse<T>(refusal: RegistrationRefusal) -> Result<T, Failure> {
    Err(WorkFailure::Operation(refusal))
}
fn lift<E>(wrap: impl FnOnce(E) -> RegistrationRefusal) -> impl FnOnce(WorkFailure<E>) -> Failure {
    move |failure| match failure {
        WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
        WorkFailure::Operation(error) => WorkFailure::Operation(wrap(error)),
    }
}
fn io_at(step: Step, owner: Owner) -> impl FnOnce(WorkFailure<io::Error>) -> Failure {
    lift(move |error| RegistrationRefusal::Io(step, owner, error))
}
pub(super) fn admission(failure: AdmissionFailure) -> Failure {
    lift(RegistrationRefusal::Admission)(failure)
}
pub(super) fn tracking(failure: TrackingFailure) -> Failure {
    lift(RegistrationRefusal::Tracking)(failure)
}
fn chain(failure: WorkFailure<ProjectChainRefusal>) -> Failure {
    lift(|refusal| RegistrationRefusal::Admission(ProjectAdmissionRefusal::Chain(refusal)))(failure)
}
/// A private-access failure: capture I/O and append I/O are the host I/O
/// row; an unreadable capture or a refused predicate is custody.
pub(super) fn private(
    step: Step,
    owner: Owner,
) -> impl FnOnce(WorkFailure<PreparePrivateError>) -> Failure {
    use RegistrationRefusal as R;
    move |failure| {
        let error = match failure {
            WorkFailure::Budget(budget) => return WorkFailure::Budget(budget),
            WorkFailure::Operation(error) => error,
        };
        WorkFailure::Operation(match error {
            PreparePrivateError::Capture(WorkFailure::Budget(budget))
            | PreparePrivateError::Append(WorkFailure::Budget(budget)) => {
                return WorkFailure::Budget(budget);
            }
            PreparePrivateError::Capture(WorkFailure::Operation(
                DescriptorAclCaptureError::Io(error),
            )) => R::Io(step, owner, error),
            PreparePrivateError::Capture(WorkFailure::Operation(_)) => {
                R::Custody(owner, "acl-unreadable")
            }
            PreparePrivateError::Append(WorkFailure::Operation(error))
            | PreparePrivateError::Create(error) => R::Io(step, owner, error),
            PreparePrivateError::Access(_) => R::Custody(owner, "private"),
            PreparePrivateError::Name => R::Invariant("private-name"),
        })
    }
}
/// A refused exclusive directory creation.
fn exclusive_directory(
    step: Step,
    owner: Owner,
) -> impl FnOnce(WorkFailure<ExclusiveDirectoryError>) -> Failure {
    lift(move |error| match error {
        ExclusiveDirectoryError::Name(_) => RegistrationRefusal::Invariant("directory-name"),
        ExclusiveDirectoryError::NotFresh => RegistrationRefusal::Changed(owner),
        ExclusiveDirectoryError::Create(error) | ExclusiveDirectoryError::AfterCreate(error) => {
            RegistrationRefusal::Io(step, owner, error)
        }
    })
}
/// A refused exclusive regular-file creation.
fn exclusive_regular(
    step: Step,
    owner: Owner,
) -> impl FnOnce(WorkFailure<ExclusiveRegularError>) -> Failure {
    lift(move |error| match error {
        ExclusiveRegularError::Name(_) => RegistrationRefusal::Invariant("file-name"),
        ExclusiveRegularError::Create(error) | ExclusiveRegularError::AfterCreate(error) => {
            RegistrationRefusal::Io(step, owner, error)
        }
    })
}
/// A refused write: a failed barrier or read-back is I/O at that step.
fn write(step: Step, owner: Owner) -> impl FnOnce(WorkFailure<NewRegularWriteError>) -> Failure {
    lift(move |error| {
        RegistrationRefusal::Io(
            step,
            owner,
            match error {
                NewRegularWriteError::Write(error)
                | NewRegularWriteError::Status(error)
                | NewRegularWriteError::ReadBack(error)
                | NewRegularWriteError::Barrier(error) => error,
                NewRegularWriteError::Length { .. } | NewRegularWriteError::Mismatch => {
                    io::Error::new(io::ErrorKind::InvalidData, "written bytes differ")
                }
            },
        )
    })
}
/// macOS `ELOOP` and `ENOTDIR`: a link or a non-directory at a name.
pub(super) const ELOOP: i32 = 62;
const ENOTDIR: i32 = 20;
fn kind_or_io(step: Step, owner: Owner) -> impl FnOnce(WorkFailure<io::Error>) -> Failure {
    lift(move |error: io::Error| match error.raw_os_error() {
        Some(ELOOP) => RegistrationRefusal::Custody(owner, "symlink"),
        Some(ENOTDIR) => RegistrationRefusal::Custody(owner, "not-a-directory"),
        _ => RegistrationRefusal::Io(step, owner, error),
    })
}

// ----------------------------------------------------------- test seam

/// The points item 6's steps pass, in order. Tests stop a registration at
/// any of them; production passes none.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum Point {
    /// RESERVED's temporary file is written, barriered and confirmed.
    ReservedWritten,
    /// RESERVED is renamed over the registry, before I's barrier.
    ReservedRenamed,
    /// RESERVED is confirmed (R1), before the namespace step.
    ReservedConfirmed,
    /// `I/host` and `I/host/projects` are created or admitted.
    ParentsReady,
    /// The namespace stage is complete and barriered, before its rename.
    NamespaceStaged,
    /// The namespace is renamed to N, before `projects`' barrier.
    NamespacePublished,
    /// `.opensip` is created or admitted, before its barriers.
    MarkerDirectoryReady,
    /// The marker file is created empty, before its bytes.
    MarkerCreated,
    /// The marker's bytes are written and barriered, before `.opensip`'s.
    MarkerWritten,
    /// ACTIVE's temporary file is written, barriered and confirmed.
    ActiveWritten,
    /// ACTIVE is renamed over the registry, before I's barrier.
    ActiveRenamed,
}
/// A scripted candidate draw (tests only): fills the buffer, or fails.
#[cfg(test)]
pub(crate) type Draw<'a> = dyn Fn(&mut [u8]) -> bool + 'a;
/// Test seams: a hook at each point (it may change the filesystem; `true`
/// injects an I/O failure there), and scripted candidate draws. Production
/// passes `Seam::live()`.
pub(crate) struct Seam<'a> {
    #[cfg(test)]
    pub(crate) fault: Option<&'a dyn Fn(Point) -> bool>,
    #[cfg(test)]
    pub(crate) draw: Option<&'a Draw<'a>>,
    live: std::marker::PhantomData<&'a ()>,
}
impl Seam<'_> {
    pub(crate) fn live() -> Self {
        Self {
            #[cfg(test)]
            fault: None,
            #[cfg(test)]
            draw: None,
            live: std::marker::PhantomData,
        }
    }
    fn at(&self, point: Point, step: Step, owner: Owner) -> Result<(), Failure> {
        #[cfg(test)]
        if let Some(fault) = self.fault
            && fault(point)
        {
            return refuse(RegistrationRefusal::Io(
                step,
                owner,
                io::Error::other(format!("injected at {point:?}")),
            ));
        }
        let _ = (point, step, owner, self.live);
        Ok(())
    }
    /// One ProjectId candidate: a complete independent 32-byte draw.
    fn project_draw(&self) -> Option<[u8; 32]> {
        #[cfg(test)]
        if let Some(draw) = self.draw {
            let mut out = [0; 32];
            return draw(&mut out).then_some(out);
        }
        opensip_platform::project_id_draw().ok()
    }
    /// One namespace candidate: its own independent 16-byte draw.
    fn namespace_draw(&self) -> Option<[u8; 16]> {
        #[cfg(test)]
        if let Some(draw) = self.draw {
            let mut out = [0; 16];
            return draw(&mut out).then_some(out);
        }
        opensip_platform::request_entropy().ok()
    }
}

/// What a project step needs besides the gate: the explicit `--trust-group`
/// set, and the environment and fixed system sources item 6a reads only to
/// refuse. Production passes the process environment and `SYSTEM_SOURCES`.
pub(crate) struct ProjectInputs<'a> {
    pub(crate) trust_groups: &'a BTreeSet<u32>,
    pub(crate) environment: &'a [(OsString, OsString)],
    pub(crate) system_sources: &'a [&'a Path],
}

// ------------------------------------------------------------- the costs

pub(super) fn capture_cost() -> WorkCost {
    opensip_platform::descriptor_acl_capture_cost()
}
/// `prepare_fresh_private_sample`: a sample, the append and a sample.
fn prepare_cost() -> WorkCost {
    plus(&[
        capture_cost(),
        opensip_platform::append_owner_zero_allow_cost(),
        capture_cost(),
    ])
}
fn filesystem_cost() -> WorkCost {
    opensip_platform::descriptor_filesystem_observation_cost()
}
fn barrier_cost() -> WorkCost {
    opensip_platform::directory_barrier_cost()
}
pub(super) fn name_cost() -> WorkCost {
    opensip_platform::descriptor_name_observation_cost()
}
/// One reopened file's confirmation: the open, both samples and the read.
fn confirm_cost(name: &str, len: usize) -> WorkCost {
    plus(&[
        RetainedDirectory::open_regular_cost(name),
        capture_cost(),
        capture_cost(),
        read_cost(len),
    ])
}
fn read_cost(len: usize) -> WorkCost {
    WorkCost {
        objects: 1,
        edges: 2,
        bytes: len.saturating_add(1),
    }
}
/// The temporary file of the replacement primitive (steps 3).
fn temporary_cost(temporary: &str, len: usize) -> WorkCost {
    plus(&[
        opensip_platform::create_exclusive_regular_cost(temporary),
        prepare_cost(),
        opensip_platform::write_new_regular_cost(len),
        confirm_cost(temporary, len),
    ])
}
/// The rename, I's barrier and the name recheck (steps 4 and 5).
fn publish_cost(temporary: &str) -> WorkCost {
    plus(&[
        opensip_platform::rename_replace_cost(temporary, REGISTRY),
        barrier_cost(),
        capture_cost(),
        RetainedDirectory::open_regular_cost(REGISTRY),
        capture_cost(),
    ])
}
/// 465 item 3's create-or-admit of one private directory, either branch.
fn parent_cost(name: &str) -> WorkCost {
    plus(&[
        opensip_platform::create_exclusive_directory_cost(name),
        prepare_cost(),
        opensip_platform::open_child_directory_cost(OsStr::new(name)),
        capture_cost(),
        name_cost(),
        filesystem_cost(),
        times(STATUS, 2),
        times(barrier_cost(), 2),
    ])
}
/// The namespace's confirmation: its custody, its scan and both leases.
fn footprint_cost() -> WorkCost {
    let lease = plus(&[
        RetainedDirectory::open_regular_cost(WRITER_LEASE),
        capture_cost(),
    ]);
    plus(&[capture_cost(), SCAN, times(lease, 2)])
}
/// The staged namespace: the stage, its allow, both leases written empty
/// with their barriers, the stage barrier, the exclusive rename, the
/// parent barrier, the exact name and the footprint.
fn namespace_cost() -> WorkCost {
    let lease = plus(&[
        opensip_platform::create_exclusive_regular_cost(READERS_LEASE),
        prepare_cost(),
        opensip_platform::write_new_regular_cost(0),
    ]);
    plus(&[
        opensip_platform::private_directory_stage_cost(),
        prepare_cost(),
        times(lease, 2),
        barrier_cost(),
        opensip_platform::exclusive_publication_cost(),
        barrier_cost(),
        EXACT_NAME,
        name_cost(),
        footprint_cost(),
    ])
}
/// `.opensip`'s create-or-admit with S3 custody under the premise.
fn marker_directory_cost() -> WorkCost {
    plus(&[
        opensip_platform::create_exclusive_directory_cost(MARKER_DIRECTORY),
        prepare_cost(),
        opensip_platform::open_child_directory_cost(OsStr::new(MARKER_DIRECTORY)),
        capture_cost(),
        filesystem_cost(),
        name_cost(),
        filesystem_cost(),
        times(barrier_cost(), 2),
    ])
}
/// The marker: the exclusive create, its allow, its bytes and barrier,
/// `.opensip`'s barrier and the confirmation.
fn marker_cost() -> WorkCost {
    plus(&[
        opensip_platform::create_exclusive_regular_cost(MARKER_FILE),
        prepare_cost(),
        opensip_platform::write_new_regular_cost(PROJECT_MARKER_SIZE),
        barrier_cost(),
        confirm_cost(MARKER_FILE, PROJECT_MARKER_SIZE),
    ])
}

// --------------------------------------------------------- native helpers

/// One charged ACL capture of `file`.
fn capture(
    file: &File,
    step: Step,
    owner: Owner,
    work: &mut WorkScope<'_>,
) -> Result<DescriptorAclCapture, Failure> {
    opensip_platform::capture_descriptor_acl_accounted(file, work).map_err(lift(move |error| {
        match error {
            DescriptorAclCaptureError::Io(error) => RegistrationRefusal::Io(step, owner, error),
            _ => RegistrationRefusal::Custody(owner, "acl-unreadable"),
        }
    }))
}
/// A private regular file's full metadata sample, judged private.
pub(super) fn private_file(
    file: &File,
    step: Step,
    owner: Owner,
    uid: u32,
    work: &mut WorkScope<'_>,
) -> Result<DescriptorMetadata, Failure> {
    let sample = capture(file, step, owner, work)?;
    judge_private(&sample, owner, uid)?;
    Ok(sample.metadata().clone())
}
fn judge_private(sample: &DescriptorAclCapture, owner: Owner, uid: u32) -> Result<(), Failure> {
    assess_private_descendant_capture(PrivateObjectKind::RegularFile, uid, sample)
        .map_err(|_| WorkFailure::Operation(RegistrationRefusal::Custody(owner, "private")))
}
/// A retained file still carries `expected` as its full sample (any
/// difference, an unlinked or replaced file included, is a change), and is
/// still private.
pub(super) fn same_private(
    file: &File,
    expected: &DescriptorMetadata,
    step: Step,
    owner: Owner,
    uid: u32,
    work: &mut WorkScope<'_>,
) -> Result<(), Failure> {
    let sample = capture(file, step, owner, work)?;
    if sample.metadata() != expected {
        return refuse(RegistrationRefusal::Changed(owner));
    }
    judge_private(&sample, owner, uid)
}
/// A no-follow open by name. A missing, linked or non-regular entry under a
/// held fence is a change.
fn open_named(
    directory: &RetainedDirectory,
    name: &str,
    step: Step,
    owner: Owner,
    work: &mut WorkScope<'_>,
) -> Result<File, Failure> {
    work.run(RetainedDirectory::open_regular_cost(name), |_| {
        directory.open_regular(name).map_err(|error| {
            WorkFailure::Operation(
                if error.kind() == io::ErrorKind::NotFound
                    || error.kind() == io::ErrorKind::InvalidInput
                    || error.raw_os_error() == Some(ELOOP)
                {
                    RegistrationRefusal::Changed(owner)
                } else {
                    RegistrationRefusal::Io(step, owner, error)
                },
            )
        })
    })
}
/// Read a reopened file whole (one byte past `len` shows a longer file).
fn read_back(
    file: &File,
    len: usize,
    step: Step,
    owner: Owner,
    work: &mut WorkScope<'_>,
) -> Result<Vec<u8>, Failure> {
    work.run(read_cost(len), |_| {
        let mut bytes = Vec::with_capacity(len.saturating_add(1));
        file.take(len as u64 + 1)
            .read_to_end(&mut bytes)
            .map_err(|error| WorkFailure::Operation(RegistrationRefusal::Io(step, owner, error)))?;
        Ok(bytes)
    })
}
/// Confirm a written file by identity and exact bytes: reopened by name
/// no-follow, the same full sample as its own descriptor's, private, and
/// holding exactly `bytes`. Returns that sample.
#[allow(clippy::too_many_arguments)]
fn confirm_file(
    directory: &RetainedDirectory,
    name: &str,
    file: &File,
    bytes: &[u8],
    uid: u32,
    step: Step,
    owner: Owner,
    work: &mut WorkScope<'_>,
) -> Result<DescriptorMetadata, Failure> {
    let reopened = open_named(directory, name, step, owner, work)?;
    let held = capture(file, step, owner, work)?;
    let named = capture(&reopened, step, owner, work)?;
    if held.metadata() != named.metadata() {
        return refuse(RegistrationRefusal::Changed(owner));
    }
    judge_private(&held, owner, uid)?;
    if read_back(&reopened, bytes.len(), step, owner, work)? != bytes {
        return refuse(RegistrationRefusal::Changed(owner));
    }
    Ok(held.metadata().clone())
}
/// One directory barrier on this exact handle: its receipt must be for the
/// handle, and the receipt's policy must accept the kind (as the gate's).
fn barrier(
    directory: &RetainedDirectory,
    policy: PrimitivePolicy,
    step: Step,
    owner: Owner,
    work: &mut WorkScope<'_>,
) -> Result<(), Failure> {
    let receipt = directory
        .confirm_directory_barrier_accounted(work)
        .map_err(io_at(step, owner))?;
    if !receipt.is_for(directory) {
        return refuse(RegistrationRefusal::BarrierReceipt(step, owner));
    }
    match (policy, receipt.barrier()) {
        (PrimitivePolicy::Apfs, DirectoryBarrier::FullFlush | DirectoryBarrier::Fsync) => Ok(()),
    }
}
/// The retained directory still has its exact name.
fn named(
    directory: &RetainedDirectory,
    name: &str,
    step: Step,
    owner: Owner,
    work: &mut WorkScope<'_>,
) -> Result<(), Failure> {
    if opensip_platform::descriptor_name_matches_accounted(
        directory.as_file(),
        OsStr::new(name),
        work,
    )
    .map_err(io_at(step, owner))?
    {
        Ok(())
    } else {
        refuse(RegistrationRefusal::Changed(owner))
    }
}
pub(super) fn identity(
    file: &File,
    step: Step,
    owner: Owner,
    work: &mut WorkScope<'_>,
) -> Result<(u64, u64), Failure> {
    work.run(STATUS, |_| {
        file.metadata()
            .map(|m| (m.dev(), m.ino()))
            .map_err(|error| WorkFailure::Operation(RegistrationRefusal::Io(step, owner, error)))
    })
}
/// The retained `child` is still the directory a no-follow reopen of `name`
/// under `parent` finds, and still has its exact name.
pub(super) fn rebind(
    parent: &RetainedDirectory,
    name: &str,
    child: &RetainedDirectory,
    step: Step,
    owner: Owner,
    work: &mut WorkScope<'_>,
) -> Result<(), Failure> {
    let reopened = parent
        .open_child_directory_if_present_accounted(OsStr::new(name), work)
        .map_err(lift(move |_| RegistrationRefusal::Changed(owner)))?;
    let Some(reopened) = reopened else {
        return refuse(RegistrationRefusal::Changed(owner));
    };
    if identity(reopened.as_file(), step, owner, work)?
        != identity(child.as_file(), step, owner, work)?
    {
        return refuse(RegistrationRefusal::Changed(owner));
    }
    named(child, name, step, owner, work)
}
/// An installation-private child directory if present: opened no-follow,
/// judged private (0700, owned, an ACL with no foreign grant) and named.
pub(super) fn private_child(
    parent: &RetainedDirectory,
    name: &str,
    uid: u32,
    step: Step,
    owner: Owner,
    work: &mut WorkScope<'_>,
) -> Result<Option<RetainedDirectory>, Failure> {
    let child = parent
        .open_child_directory_if_present_accounted(OsStr::new(name), work)
        .map_err(kind_or_io(step, owner))?;
    let Some(child) = child else {
        return Ok(None);
    };
    observe_private_directory(child.as_file(), uid, work).map_err(private(step, owner))?;
    named(&child, name, step, owner, work)?;
    Ok(Some(child))
}
/// Item 1: an object the premise admits must also be on H's volume.
fn home_volume(
    file: &File,
    home_filesystem: &dyn Fn(&DescriptorFilesystem) -> bool,
    step: Step,
    owner: Owner,
    work: &mut WorkScope<'_>,
) -> Result<(), Failure> {
    let sample =
        opensip_platform::observe_filesystem_accounted(file, work).map_err(io_at(step, owner))?;
    if home_filesystem(&sample) {
        Ok(())
    } else {
        refuse(RegistrationRefusal::Custody(owner, "volume-unsupported"))
    }
}
/// A project object's S3 custody judgment: host I/O stays I/O; every other
/// refusal is that object's custody subject.
fn project_object(
    directory: &RetainedDirectory,
    uid: u32,
    policy: &ProjectChainPolicy<'_>,
    owner: Owner,
    subject: &'static str,
    work: &mut WorkScope<'_>,
) -> Result<(), Failure> {
    match judge_project_object(
        directory.as_file(),
        ProjectObject::Directory,
        uid,
        policy,
        work,
    ) {
        Ok(()) => Ok(()),
        Err(WorkFailure::Budget(budget)) => Err(WorkFailure::Budget(budget)),
        Err(WorkFailure::Operation(refusal)) if refusal.row() == ProjectChainRow::HostIo => refuse(
            RegistrationRefusal::Admission(ProjectAdmissionRefusal::Chain(refusal)),
        ),
        Err(WorkFailure::Operation(_)) => refuse(RegistrationRefusal::Custody(owner, subject)),
    }
}
/// Run `action` as one effect whose whole work, the effect and its
/// confirmations, is reserved before it starts (467 item 6). A shortfall
/// fails closed before the work it would cover.
fn effect<R>(
    work: &mut WorkScope<'_>,
    reserve: WorkCost,
    action: impl FnOnce(&mut WorkScope<'_>) -> Result<R, Failure>,
) -> Result<R, Failure> {
    work.effect(WorkCost::default(), reserve, |post| {
        post.prepaid(reserve, action)
    })
}
fn hex(bytes: &[u8]) -> String {
    const DIGITS: &[u8; 16] = b"0123456789abcdef";
    let mut out = String::with_capacity(bytes.len() * 2);
    for b in bytes {
        out.push(DIGITS[usize::from(b >> 4)] as char);
        out.push(DIGITS[usize::from(b & 15)] as char);
    }
    out
}
/// The canonical lowercase UUIDv4 of one 16-byte draw: version 4 and the
/// RFC variant set, the other 122 bits from the draw.
pub(crate) fn namespace_text(mut draw: [u8; 16]) -> String {
    draw[6] = (draw[6] & 0x0f) | 0x40;
    draw[8] = (draw[8] & 0x3f) | 0x80;
    let h = hex(&draw);
    format!(
        "{}-{}-{}-{}-{}",
        &h[0..8],
        &h[8..12],
        &h[12..16],
        &h[16..20],
        &h[20..32]
    )
}
/// The 92-byte marker frame for a ProjectId.
fn marker_bytes(project: &str) -> Vec<u8> {
    let mut bytes = Vec::with_capacity(PROJECT_MARKER_SIZE);
    bytes.extend_from_slice(MARKER_PREFIX);
    bytes.extend_from_slice(project.as_bytes());
    bytes.push(b'\n');
    bytes
}

// ------------------------------------------------------ the document

fn status_text(status: ProjectRegistryStatus) -> &'static str {
    match status {
        ProjectRegistryStatus::Reserved => "RESERVED",
        ProjectRegistryStatus::Active => "ACTIVE",
        ProjectRegistryStatus::Retired => "RETIRED",
        ProjectRegistryStatus::Abandoned => "ABANDONED",
    }
}
/// The longest status a row can lawfully reach later: RESERVED may end
/// ABANDONED, ACTIVE may end RETIRED; terminal rows never change.
fn worst_status(status: ProjectRegistryStatus) -> ProjectRegistryStatus {
    match status {
        ProjectRegistryStatus::Reserved => ProjectRegistryStatus::Abandoned,
        ProjectRegistryStatus::Active => ProjectRegistryStatus::Retired,
        terminal => terminal,
    }
}
fn text(s: &str) -> V {
    V::String(s.to_owned())
}
fn integer(n: i128) -> Result<V, RegistrationRefusal> {
    JsonInteger::new(n)
        .map(V::Integer)
        .map_err(|_| RegistrationRefusal::Invariant("integer"))
}
/// The closed NativeProjectRootV2 of one row.
struct RootValues<'a> {
    path: &'a [u8],
    volume: &'a [u8; 16],
    inode: u64,
    seconds: i64,
    nanoseconds: u32,
}
fn root_value(root: &RootValues<'_>) -> Result<V, RegistrationRefusal> {
    Ok(V::Object(BTreeMap::from([
        ("platform".to_owned(), text("macos")),
        ("canonicalPathBytesHex".to_owned(), text(&hex(root.path))),
        (
            "volumeIdentity".to_owned(),
            V::Object(BTreeMap::from([
                ("kind".to_owned(), text("macos-apfs-volume-uuid-v1")),
                ("value".to_owned(), text(&hex(root.volume))),
            ])),
        ),
        ("inodeId".to_owned(), text(&root.inode.to_string())),
        (
            "birthSeconds".to_owned(),
            integer(i128::from(root.seconds))?,
        ),
        (
            "birthNanoseconds".to_owned(),
            integer(i128::from(root.nanoseconds))?,
        ),
    ])))
}
fn row_value(
    project: &str,
    namespace: &str,
    root: V,
    status: ProjectRegistryStatus,
    allocation: ProjectAllocationKind,
) -> V {
    V::Object(BTreeMap::from([
        ("projectId".to_owned(), text(project)),
        ("namespaceId".to_owned(), text(namespace)),
        ("root".to_owned(), root),
        ("status".to_owned(), text(status_text(status))),
        (
            "allocationKind".to_owned(),
            text(match allocation {
                ProjectAllocationKind::Random => "random",
                ProjectAllocationKind::Adopt => "adopt",
            }),
        ),
    ]))
}
/// An admitted row re-encoded from its decoded members, at `status`.
fn existing_row(
    entry: &ProjectRegistryEntry,
    status: ProjectRegistryStatus,
) -> Result<V, RegistrationRefusal> {
    let root = entry.root();
    let values = RootValues {
        path: root.path_bytes(),
        volume: root.volume_uuid_bytes(),
        inode: root.inode(),
        seconds: root.birth_seconds(),
        nanoseconds: root.birth_nanoseconds(),
    };
    Ok(row_value(
        entry.project_id(),
        entry.namespace_id(),
        root_value(&values)?,
        status,
        entry.allocation_kind(),
    ))
}
fn document_value(rows: Vec<V>) -> Result<V, RegistrationRefusal> {
    Ok(V::Object(BTreeMap::from([
        ("entries".to_owned(), V::Array(rows)),
        ("schemaVersion".to_owned(), integer(2)?),
    ])))
}
fn encoded(value: &V) -> Result<Vec<u8>, RegistrationRefusal> {
    canonical_bytes(value).map_err(|_| RegistrationRefusal::Invariant("canonical-encoding"))
}
/// The canonical length of a document whose rows have these canonical
/// lengths: the empty envelope, every row, and the commas between them.
fn document_length(empty: usize, rows: impl Iterator<Item = usize>) -> usize {
    let (count, sum) = rows.fold((0usize, 0usize), |(n, s), len| {
        (n + 1, s.saturating_add(len))
    });
    empty
        .saturating_add(sum)
        .saturating_add(count.saturating_sub(1))
}
/// A complete replacement document, built canonically and validated by the
/// same decoder as the capture (item 6 step 2). Only `build` makes one.
pub(crate) struct Built {
    bytes: Vec<u8>,
    document: ProjectRegistryDocument,
}
fn build(rows: Vec<V>, work: &mut WorkScope<'_>) -> Result<Built, Failure> {
    let value = document_value(rows).map_err(WorkFailure::Operation)?;
    let bytes = work.run(
        WorkCost {
            objects: 1,
            edges: 1,
            bytes: PROJECT_REGISTRY_CAP,
        },
        |_| encoded(&value).map_err(WorkFailure::Operation),
    )?;
    let decode = WorkCost {
        objects: 1,
        edges: 1,
        bytes: bytes.len(),
    };
    let document = work.run(decode, |_| {
        ProjectRegistryDocument::decode(&bytes)
            .map_err(|error| WorkFailure::Operation(RegistrationRefusal::Document(error)))
    })?;
    Ok(Built { bytes, document })
}

/// The new row's members.
struct NewRow<'a> {
    project: &'a str,
    namespace: &'a str,
    path: &'a [u8],
    incarnation: &'a Incarnation,
}
impl NewRow<'_> {
    fn value(&self, status: ProjectRegistryStatus) -> Result<V, RegistrationRefusal> {
        let root = RootValues {
            path: self.path,
            volume: &self.incarnation.volume,
            inode: self.incarnation.inode,
            seconds: self.incarnation.birth_seconds,
            nanoseconds: self.incarnation.birth_nanoseconds,
        };
        Ok(row_value(
            self.project,
            self.namespace,
            root_value(&root)?,
            status,
            ProjectAllocationKind::Random,
        ))
    }
}

/// Item 6's capacity, before any effect: the resulting rows, the canonical
/// bytes of the RESERVED and ACTIVE documents and of the worst later
/// terminal spelling, and the worst all-registered transition wrapper, all
/// within the 4096-row profile. Then RESERVED is built and validated.
/// R0's rows are re-encoded once; they must reproduce R0's exact bytes.
fn plan_reserved(
    document: &ProjectRegistryDocument,
    new: &NewRow<'_>,
    work: &mut WorkScope<'_>,
) -> Result<Built, Failure> {
    let entries = document.entries();
    let count = entries.len() + 1;
    if count > PROJECT_REGISTRY_ROW_CAP {
        return refuse(RegistrationRefusal::ScopeLimit {
            field: "registry-rows",
            count,
        });
    }
    // Every row encoded once, the new row three times, then R0's bytes.
    let serialize = WorkCost {
        objects: count.saturating_add(3),
        edges: count.saturating_add(3),
        bytes: document
            .raw()
            .len()
            .saturating_add(3 * ROW_BOUND)
            .saturating_add(document.raw().len()),
    };
    let (rows, lengths, worst, reserved_len, active_len, abandoned_len) =
        work.run(serialize, |_| {
            let mut rows = Vec::with_capacity(count);
            let mut lengths = Vec::with_capacity(count);
            let mut worst = Vec::with_capacity(count);
            for entry in entries {
                let row = existing_row(entry, entry.status()).map_err(WorkFailure::Operation)?;
                let len = encoded(&row).map_err(WorkFailure::Operation)?.len();
                // RESERVED to ABANDONED and ACTIVE to RETIRED each add one byte.
                let later = len + usize::from(worst_status(entry.status()) != entry.status());
                rows.push(row);
                lengths.push(len);
                worst.push(later);
            }
            let reserved = new
                .value(ProjectRegistryStatus::Reserved)
                .map_err(WorkFailure::Operation)?;
            let reserved_len = encoded(&reserved).map_err(WorkFailure::Operation)?.len();
            let active = new
                .value(ProjectRegistryStatus::Active)
                .map_err(WorkFailure::Operation)?;
            let active_len = encoded(&active).map_err(WorkFailure::Operation)?.len();
            let abandoned = new
                .value(ProjectRegistryStatus::Abandoned)
                .map_err(WorkFailure::Operation)?;
            let abandoned_len = encoded(&abandoned).map_err(WorkFailure::Operation)?.len();
            let again = encoded(&document_value(rows.clone()).map_err(WorkFailure::Operation)?)
                .map_err(WorkFailure::Operation)?;
            if again != document.raw() {
                return refuse(RegistrationRefusal::Invariant("r0-reencoding"));
            }
            let at =
                entries.partition_point(|e| e.namespace_id().as_bytes() < new.namespace.as_bytes());
            rows.insert(at, reserved);
            Ok((
                rows,
                lengths,
                worst,
                reserved_len,
                active_len,
                abandoned_len,
            ))
        })?;
    let empty = encoded(&document_value(Vec::new()).map_err(WorkFailure::Operation)?)
        .map_err(WorkFailure::Operation)?
        .len();
    let reserved = document_length(empty, lengths.iter().copied().chain([reserved_len]));
    let active = document_length(empty, lengths.iter().copied().chain([active_len]));
    let terminal = document_length(empty, worst.iter().copied().chain([abandoned_len]));
    for n in [reserved, active, terminal] {
        if n > PROJECT_REGISTRY_CAP {
            return refuse(RegistrationRefusal::ScopeLimit {
                field: "registry-bytes",
                count: n,
            });
        }
    }
    // The worst legal all-registered wrapper: every row that can still be
    // registered (RESERVED, ACTIVE, RETIRED; never ABANDONED), and this one.
    let registered = entries
        .iter()
        .filter(|e| e.status() != ProjectRegistryStatus::Abandoned)
        .count()
        + 1;
    if registered > PROJECT_REGISTRY_ROW_CAP {
        return refuse(RegistrationRefusal::ScopeLimit {
            field: "registry-transition-rows",
            count: registered,
        });
    }
    let built = build(rows, work)?;
    if built.bytes.len() != reserved {
        return refuse(RegistrationRefusal::Invariant("reserved-length"));
    }
    Ok(built)
}
/// ACTIVE from R1's validated document, never from the candidate IDs
/// alone: the one RESERVED random row at N becomes ACTIVE, every other row
/// is carried by value.
fn plan_active(
    document: &ProjectRegistryDocument,
    namespace: &str,
    work: &mut WorkScope<'_>,
) -> Result<Built, Failure> {
    let entries = document.entries();
    let serialize = WorkCost {
        objects: entries.len().saturating_add(1),
        edges: entries.len().saturating_add(1),
        bytes: document.raw().len().saturating_add(ROW_BOUND),
    };
    let rows = work.run(serialize, |_| {
        let mut found = 0;
        let mut rows = Vec::with_capacity(entries.len());
        for entry in entries {
            let status = if entry.namespace_id() == namespace {
                found += 1;
                if entry.status() != ProjectRegistryStatus::Reserved
                    || entry.allocation_kind() != ProjectAllocationKind::Random
                {
                    return refuse(RegistrationRefusal::Invariant("reserved-row"));
                }
                ProjectRegistryStatus::Active
            } else {
                entry.status()
            };
            rows.push(existing_row(entry, status).map_err(WorkFailure::Operation)?);
        }
        if found != 1 {
            return refuse(RegistrationRefusal::Invariant("reserved-row"));
        }
        Ok(rows)
    })?;
    build(rows, work)
}

// ------------------------------------------- the replacement primitive

/// The current registry owner R (item 6): the retained descriptor of the
/// file now named `project-registry.v2`, its full sample, and its
/// validated document. R0 is item 5's capture; R1 and R2 are the
/// temporary files' own descriptors carried across their renames.
pub(crate) struct RegistryOwner {
    file: File,
    metadata: DescriptorMetadata,
    document: ProjectRegistryDocument,
}
impl RegistryOwner {
    pub(crate) fn document(&self) -> &ProjectRegistryDocument {
        &self.document
    }
}
/// Step 1: R by its retained descriptor and full sample (private, the same
/// sample), the name binding under I (a no-follow reopen with the same
/// sample), and the old name still positively absent. I itself is the
/// gate's, rechecked by the gate.
fn reconfirm(
    i: &RetainedDirectory,
    owner: &RegistryOwner,
    step: Step,
    uid: u32,
    work: &mut WorkScope<'_>,
) -> Result<(), Failure> {
    same_private(
        &owner.file,
        &owner.metadata,
        step,
        Owner::Registry,
        uid,
        work,
    )?;
    let named = open_named(i, REGISTRY, step, Owner::Registry, work)?;
    same_private(&named, &owner.metadata, step, Owner::Registry, uid, work)?;
    old_name_absent(i, work).map_err(admission)
}
/// Item 6's registry replacement primitive, used for RESERVED and ACTIVE;
/// never a no-replace publication. Step 1 reconfirms R; step 2 is `next`,
/// already built and validated; step 3 writes a fresh exclusive temporary
/// name in I, private, with `F_FULLFSYNC`, confirmed by identity and exact
/// bytes; step 4 renames it over the registry; step 5 takes I's barrier and
/// rechecks that the name holds the new file by identity. Returns the new
/// owner. The temporary file is never removed.
#[allow(clippy::too_many_arguments)]
fn replace(
    i: &RetainedDirectory,
    owner: &RegistryOwner,
    next: Built,
    step: Step,
    uid: u32,
    policy: PrimitivePolicy,
    seam: &Seam<'_>,
    work: &mut WorkScope<'_>,
) -> Result<RegistryOwner, Failure> {
    let (written, renamed) = match step {
        Step::Reserved => (Point::ReservedWritten, Point::ReservedRenamed),
        _ => (Point::ActiveWritten, Point::ActiveRenamed),
    };
    reconfirm(i, owner, step, uid, work)?;
    let nonce = work.run(DRAW, |_| {
        opensip_platform::request_entropy()
            .map_err(|_| WorkFailure::Operation(RegistrationRefusal::Entropy))
    })?;
    let temporary = format!("{REGISTRY}.{}", hex(&nonce));
    let Built { bytes, document } = next;
    let file = effect(work, temporary_cost(&temporary, bytes.len()), |work| {
        let file = match i
            .create_exclusive_regular_accounted(&temporary, work)
            .map_err(exclusive_regular(step, Owner::Registry))?
        {
            ExclusiveRegularOutcome::Created(file) => file,
            ExclusiveRegularOutcome::EntryExists => {
                return refuse(RegistrationRefusal::Changed(Owner::Registry));
            }
        };
        prepare_fresh_private_sample(PrivateObjectKind::RegularFile, uid, &file, work)
            .map_err(private(step, Owner::Registry))?;
        let receipt = opensip_platform::write_new_regular_accounted(&file, &bytes, work)
            .map_err(write(step, Owner::Registry))?;
        if !receipt.is_for(&file) {
            return refuse(RegistrationRefusal::BarrierReceipt(step, Owner::Registry));
        }
        seam.at(written, step, Owner::Registry)?;
        confirm_file(
            i,
            &temporary,
            &file,
            &bytes,
            uid,
            step,
            Owner::Registry,
            work,
        )?;
        Ok(file)
    })?;
    effect(work, publish_cost(&temporary), |work| {
        i.rename_replace_accounted(&temporary, REGISTRY, work)
            .map_err(lift(|error| match error {
                RenameReplaceError::TargetNotRegular => {
                    RegistrationRefusal::Changed(Owner::Registry)
                }
                RenameReplaceError::Name(_) => RegistrationRefusal::Invariant("rename-name"),
                RenameReplaceError::TargetStatus(error) | RenameReplaceError::Rename(error) => {
                    RegistrationRefusal::Io(step, Owner::Registry, error)
                }
            }))?;
        seam.at(renamed, step, Owner::Installation)?;
        barrier(i, policy, step, Owner::Installation, work)?;
        let metadata = private_file(&file, step, Owner::Registry, uid, work)?;
        let named = open_named(i, REGISTRY, step, Owner::Registry, work)?;
        same_private(&named, &metadata, step, Owner::Registry, uid, work)?;
        Ok(RegistryOwner {
            file,
            metadata,
            document,
        })
    })
}

// --------------------------------------------------------- preconditions

/// The registry owner's active-transition-recovery gate. No transition
/// carrier is implemented: P0's `transitions` holds only `lineage`, so any
/// other entry may be a transition slot and refuses (unavailable).
fn transitions_quiet(
    i: &RetainedDirectory,
    uid: u32,
    step: Step,
    work: &mut WorkScope<'_>,
) -> Result<(), Failure> {
    let Some(directory) = private_child(i, TRANSITIONS, uid, step, Owner::Transitions, work)?
    else {
        return Ok(());
    };
    work.run(SCAN, |_| {
        directory
            .visit_entry_names(SCAN_ENTRIES, SCAN_NAME_BYTES, |name| {
                if matches!(name, b"." | b"..") || name == LINEAGE {
                    Ok(())
                } else {
                    Err(())
                }
            })
            .map(drop)
            .map_err(|error| {
                WorkFailure::Operation(match error {
                    DirectoryVisitError::Native(error) => {
                        RegistrationRefusal::Io(step, Owner::Transitions, error)
                    }
                    _ => RegistrationRefusal::TransitionActive,
                })
            })
    })
}
/// A present `host` and `projects`, judged private before any effect, so a
/// foreign parent refuses before RESERVED. Returns `projects` if present.
fn observe_parents(
    i: &RetainedDirectory,
    uid: u32,
    work: &mut WorkScope<'_>,
) -> Result<Option<RetainedDirectory>, Failure> {
    let step = Step::Preconditions;
    let Some(host) = private_child(i, HOST, uid, step, Owner::Host, work)? else {
        return Ok(None);
    };
    private_child(&host, PROJECTS, uid, step, Owner::Projects, work)
}
/// Up to eight independent ProjectId candidates; a collision with any row
/// of the whole history draws again.
fn allocate_project(
    entries: &[ProjectRegistryEntry],
    seam: &Seam<'_>,
    work: &mut WorkScope<'_>,
) -> Result<String, Failure> {
    for _ in 0..CANDIDATES {
        let draw = work.run(DRAW, |_| {
            seam.project_draw()
                .ok_or(WorkFailure::Operation(RegistrationRefusal::Entropy))
        })?;
        let project = format!("prj1-{}", hex(&draw));
        let scan = WorkCost {
            objects: 0,
            edges: entries.len().max(1),
            bytes: entries.len().saturating_mul(project.len()),
        };
        let recorded = work.run(scan, |_| {
            Ok(entries.iter().any(|e| e.project_id() == project))
        })?;
        if !recorded {
            return Ok(project);
        }
    }
    refuse(RegistrationRefusal::Exhausted("project-id"))
}
/// Up to eight independent UUIDv4 namespace candidates; a recorded N or an
/// occupied `I/host/projects/N` (any entry, by a no-follow lookup) draws
/// again. Absent parents make every target path positively absent.
fn allocate_namespace(
    entries: &[ProjectRegistryEntry],
    projects: Option<&RetainedDirectory>,
    seam: &Seam<'_>,
    work: &mut WorkScope<'_>,
) -> Result<String, Failure> {
    for _ in 0..CANDIDATES {
        let draw = work.run(DRAW, |_| {
            seam.namespace_draw()
                .ok_or(WorkFailure::Operation(RegistrationRefusal::Entropy))
        })?;
        let namespace = namespace_text(draw);
        let scan = WorkCost {
            objects: 0,
            edges: entries.len().max(1),
            bytes: entries.len().saturating_mul(namespace.len()),
        };
        let recorded = work.run(scan, |_| {
            Ok(entries.iter().any(|e| e.namespace_id() == namespace))
        })?;
        let occupied = match projects {
            Some(projects) => !projects
                .observe_child_absent_accounted(OsStr::new(&namespace), work)
                .map_err(io_at(Step::Preconditions, Owner::Projects))?,
            None => false,
        };
        if !recorded && !occupied {
            return Ok(namespace);
        }
    }
    refuse(RegistrationRefusal::Exhausted("namespace"))
}

/// Everything item 6 fixes before the first effect.
struct Plan {
    project: String,
    namespace: String,
    reserved: Built,
}
/// The preconditions, in order, all before any effect.
#[allow(clippy::too_many_arguments)]
fn preconditions(
    admission: &ProjectRootAdmission,
    observed: &TrackingObservation,
    installation: &DurableInstallation,
    policy: &ProjectChainPolicy<'_>,
    inputs: &ProjectInputs<'_>,
    seam: &Seam<'_>,
    work: &mut WorkScope<'_>,
) -> Result<Plan, Failure> {
    match (admission.classification(), admission.marker()) {
        (Classification::FirstUseCandidate, MarkerObservation::Absent) => {}
        (classification, _) => {
            return refuse(RegistrationRefusal::NotFirstUse(classification.clone()));
        }
    }
    let uid = installation.uid();
    let i = installation.installation_directory();
    let judged = judged_registry(installation.required()).ok_or(WorkFailure::Operation(
        RegistrationRefusal::Invariant("no-registry"),
    ))?;
    admission
        .recheck(uid, i, judged, policy, work)
        .map_err(admission_failure)?;
    let inputs = TrackingInputs {
        chain: admission.chain(),
        uid,
        policy,
        home: installation.home_spelling(),
        environment: inputs.environment,
        system_sources: inputs.system_sources,
    };
    recheck_tracking(observed, &inputs, work).map_err(tracking)?;
    transitions_quiet(i, uid, Step::Preconditions, work)?;
    let projects = observe_parents(i, uid, work)?;
    let document = admission.registry().document();
    let project = allocate_project(document.entries(), seam, work)?;
    let namespace = allocate_namespace(document.entries(), projects.as_ref(), seam, work)?;
    let new = NewRow {
        project: &project,
        namespace: &namespace,
        path: admission.chain().spelling().as_os_str().as_bytes(),
        incarnation: admission.incarnation(),
    };
    let reserved = plan_reserved(document, &new, work)?;
    Ok(Plan {
        project,
        namespace,
        reserved,
    })
}
fn admission_failure(failure: AdmissionFailure) -> Failure {
    admission(failure)
}

// ----------------------------------------------------- steps 3 to 5

/// 465 item 3 for one installation-private directory: an exclusive `0700`
/// create with the zero-rights owner allow, or, only on a raw `EEXIST`, a
/// fresh no-follow admission judged private (never changed). Either way
/// the exact name, H's volume and the parent's device, the directory's own
/// barrier and then the parent's. The whole step is reserved first.
#[allow(clippy::too_many_arguments)]
fn create_or_admit(
    parent: &RetainedDirectory,
    name: &str,
    owner: Owner,
    uid: u32,
    home_filesystem: &dyn Fn(&DescriptorFilesystem) -> bool,
    policy: PrimitivePolicy,
    step: Step,
    work: &mut WorkScope<'_>,
) -> Result<RetainedDirectory, Failure> {
    effect(work, parent_cost(name), |work| {
        let child = match parent
            .create_exclusive_directory_accounted(name, work)
            .map_err(exclusive_directory(step, owner))?
        {
            ExclusiveDirectoryOutcome::Created(child) => {
                prepare_fresh_private_sample(
                    PrivateObjectKind::Directory,
                    uid,
                    child.as_file(),
                    work,
                )
                .map_err(private(step, owner))?;
                child
            }
            ExclusiveDirectoryOutcome::EntryExists => {
                let Some(child) = parent
                    .open_child_directory_if_present_accounted(OsStr::new(name), work)
                    .map_err(kind_or_io(step, owner))?
                else {
                    return refuse(RegistrationRefusal::Changed(owner));
                };
                observe_private_directory(child.as_file(), uid, work)
                    .map_err(private(step, owner))?;
                child
            }
        };
        named(&child, name, step, owner, work)?;
        home_volume(child.as_file(), home_filesystem, step, owner, work)?;
        if identity(child.as_file(), step, owner, work)?.0
            != identity(parent.as_file(), step, owner, work)?.0
        {
            return refuse(RegistrationRefusal::Custody(owner, "volume-unsupported"));
        }
        barrier(&child, policy, step, owner, work)?;
        barrier(parent, policy, step, owner, work)?;
        Ok(child)
    })
}
/// Which namespace footprint a registered project's recheck requires.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum Footprint {
    /// Item 6's published footprint, exactly: the namespace holds only
    /// `writer.lease` and `readers.lease`. Registration and item 7 (X2c,
    /// X2d) recheck this.
    Exact,
    /// After X3b's carrier start may have populated N (unit X2e with
    /// X3b-3): the carrier, its WAL and shm sidecars, the witness and a
    /// leftover temporary file may stand beside the leases. N must still be
    /// private and both lease files present, private and empty; only the
    /// closed entry scan is not made.
    Started,
}
/// The namespace's complete footprint: a private directory holding exactly
/// `writer.lease` and `readers.lease`, each an empty private regular file.
fn confirm_footprint(
    directory: &RetainedDirectory,
    uid: u32,
    step: Step,
    work: &mut WorkScope<'_>,
) -> Result<(), Failure> {
    confirm_namespace_files(directory, uid, Footprint::Exact, step, work)
}
/// The namespace under `footprint`: private, both lease files present,
/// private and empty, and under `Exact` nothing else.
fn confirm_namespace_files(
    directory: &RetainedDirectory,
    uid: u32,
    footprint: Footprint,
    step: Step,
    work: &mut WorkScope<'_>,
) -> Result<(), Failure> {
    let owner = Owner::Namespace;
    observe_private_directory(directory.as_file(), uid, work).map_err(private(step, owner))?;
    if footprint == Footprint::Started {
        return lease_files(directory, uid, step, work);
    }
    let mut seen = [false; 2];
    work.run(SCAN, |_| {
        directory
            .visit_entry_names(SCAN_ENTRIES, SCAN_NAME_BYTES, |name| {
                match name {
                    b"." | b".." => {}
                    b"writer.lease" if !seen[0] => seen[0] = true,
                    b"readers.lease" if !seen[1] => seen[1] = true,
                    _ => return Err(()),
                }
                Ok(())
            })
            .map(drop)
            .map_err(|error| {
                WorkFailure::Operation(match error {
                    DirectoryVisitError::Native(error) => {
                        RegistrationRefusal::Io(step, owner, error)
                    }
                    _ => RegistrationRefusal::Changed(owner),
                })
            })
    })?;
    if seen != [true, true] {
        return refuse(RegistrationRefusal::Changed(owner));
    }
    lease_files(directory, uid, step, work)
}
/// Both lease files under N: present, private and empty.
fn lease_files(
    directory: &RetainedDirectory,
    uid: u32,
    step: Step,
    work: &mut WorkScope<'_>,
) -> Result<(), Failure> {
    let owner = Owner::Namespace;
    for lease in [WRITER_LEASE, READERS_LEASE] {
        let file = open_named(directory, lease, step, owner, work)?;
        if private_file(&file, step, owner, uid, work)?.size != 0 {
            return refuse(RegistrationRefusal::Changed(owner));
        }
    }
    Ok(())
}
/// Item 6 step 3: `I/host` and `I/host/projects` created or admitted, then
/// `I/host/projects/N` published whole: a private same-parent stage holding
/// exactly the two empty lease files, each written with its file barrier,
/// the stage's barrier, one exclusive rename to N, `projects`' barrier, the
/// exact name and the footprint confirmed. The positively absent N becomes
/// the published namespace's owner here.
#[allow(clippy::too_many_arguments)]
fn publish_namespace(
    i: &RetainedDirectory,
    namespace: &str,
    uid: u32,
    home_filesystem: &dyn Fn(&DescriptorFilesystem) -> bool,
    policy: PrimitivePolicy,
    seam: &Seam<'_>,
    work: &mut WorkScope<'_>,
) -> Result<
    (
        RetainedDirectory,
        RetainedDirectory,
        NamedDirectoryPublication,
    ),
    Failure,
> {
    let step = Step::Namespace;
    seam.at(Point::ReservedConfirmed, step, Owner::Registry)?;
    let host = create_or_admit(
        i,
        HOST,
        Owner::Host,
        uid,
        home_filesystem,
        policy,
        step,
        work,
    )?;
    let projects = create_or_admit(
        &host,
        PROJECTS,
        Owner::Projects,
        uid,
        home_filesystem,
        policy,
        step,
        work,
    )?;
    seam.at(Point::ParentsReady, step, Owner::Projects)?;
    let owner = Owner::Namespace;
    let publication = effect(work, namespace_cost(), |work| {
        let stage = projects
            .create_private_directory_stage_accounted(work)
            .map_err(io_at(step, owner))?;
        prepare_fresh_private_sample(
            PrivateObjectKind::Directory,
            uid,
            stage.directory().as_file(),
            work,
        )
        .map_err(private(step, owner))?;
        for lease in [WRITER_LEASE, READERS_LEASE] {
            let file = match stage
                .directory()
                .create_exclusive_regular_accounted(lease, work)
                .map_err(exclusive_regular(step, owner))?
            {
                ExclusiveRegularOutcome::Created(file) => file,
                ExclusiveRegularOutcome::EntryExists => {
                    return refuse(RegistrationRefusal::Changed(owner));
                }
            };
            prepare_fresh_private_sample(PrivateObjectKind::RegularFile, uid, &file, work)
                .map_err(private(step, owner))?;
            let receipt = opensip_platform::write_new_regular_accounted(&file, b"", work)
                .map_err(write(step, owner))?;
            if !receipt.is_for(&file) {
                return refuse(RegistrationRefusal::BarrierReceipt(step, owner));
            }
        }
        barrier(stage.directory(), policy, step, owner, work)?;
        seam.at(Point::NamespaceStaged, step, owner)?;
        let publication = stage
            .publish_exclusive_accounted(OsStr::new(namespace), work)
            .map_err(lift(
                |failure: opensip_platform::DirectoryRenameFailure| match failure.class() {
                    DirectoryRenameClass::LostRace => RegistrationRefusal::Changed(owner),
                    DirectoryRenameClass::NotPerformed | DirectoryRenameClass::Indeterminate => {
                        RegistrationRefusal::Io(
                            step,
                            owner,
                            io::Error::new(failure.error().kind(), failure.error().to_string()),
                        )
                    }
                },
            ))?;
        seam.at(Point::NamespacePublished, step, owner)?;
        barrier(
            publication.parent_directory(),
            policy,
            step,
            Owner::Projects,
            work,
        )?;
        let exact = work.run(plus(&[EXACT_NAME, name_cost()]), |_| {
            publication.recheck_exact_name().map_err(|error| {
                WorkFailure::Operation(RegistrationRefusal::Io(step, owner, error))
            })
        })?;
        if !exact {
            return refuse(RegistrationRefusal::Changed(owner));
        }
        confirm_footprint(publication.directory(), uid, step, work)?;
        Ok(publication)
    })?;
    Ok((host, projects, publication))
}
/// Item 6 step 4: `.opensip` created or admitted under the retained root,
/// as 465 item 3 does: the exact name, S3 directory custody with item 1's
/// premise and H's volume, the zero-rights owner allow on creation, then
/// `.opensip`'s barrier and the root's. A reused `.opensip` takes both
/// barriers too: existence is not a durability receipt.
fn marker_directory(
    chain: &ProjectChain,
    uid: u32,
    policy: &ProjectChainPolicy<'_>,
    barrier_policy: PrimitivePolicy,
    seam: &Seam<'_>,
    work: &mut WorkScope<'_>,
) -> Result<RetainedDirectory, Failure> {
    let step = Step::MarkerDirectory;
    let owner = Owner::MarkerDirectory;
    let root = chain.root();
    effect(work, marker_directory_cost(), |work| {
        let directory = match root
            .create_exclusive_directory_accounted(MARKER_DIRECTORY, work)
            .map_err(exclusive_directory(step, owner))?
        {
            ExclusiveDirectoryOutcome::Created(directory) => {
                prepare_fresh_private_sample(
                    PrivateObjectKind::Directory,
                    uid,
                    directory.as_file(),
                    work,
                )
                .map_err(private(step, owner))?;
                directory
            }
            ExclusiveDirectoryOutcome::EntryExists => {
                let Some(directory) = root
                    .open_child_directory_if_present_accounted(OsStr::new(MARKER_DIRECTORY), work)
                    .map_err(lift(move |error: io::Error| match error.raw_os_error() {
                        Some(ELOOP) | Some(ENOTDIR) => {
                            RegistrationRefusal::Custody(owner, "marker-directory-custody")
                        }
                        _ => RegistrationRefusal::Io(step, owner, error),
                    }))?
                else {
                    return refuse(RegistrationRefusal::Changed(owner));
                };
                directory
            }
        };
        project_object(
            &directory,
            uid,
            policy,
            owner,
            "marker-directory-custody",
            work,
        )?;
        named(&directory, MARKER_DIRECTORY, step, owner, work)?;
        home_volume(
            directory.as_file(),
            policy.home_filesystem(),
            step,
            owner,
            work,
        )?;
        seam.at(Point::MarkerDirectoryReady, step, owner)?;
        barrier(&directory, barrier_policy, step, owner, work)?;
        barrier(root, barrier_policy, step, Owner::Root, work)?;
        Ok(directory)
    })
}
/// Item 6 step 5: the 92-byte marker created no-replace under the retained
/// `.opensip`, with the zero-rights owner allow, written with its file
/// barrier, then `.opensip`'s barrier, and confirmed by identity and bytes.
fn create_marker(
    directory: &RetainedDirectory,
    project: &str,
    uid: u32,
    policy: PrimitivePolicy,
    seam: &Seam<'_>,
    work: &mut WorkScope<'_>,
) -> Result<(File, DescriptorMetadata), Failure> {
    let step = Step::Marker;
    let owner = Owner::Marker;
    let bytes = marker_bytes(project);
    if bytes.len() != PROJECT_MARKER_SIZE || ProjectIdMarker::decode(&bytes).is_err() {
        return refuse(RegistrationRefusal::Invariant("marker-frame"));
    }
    effect(work, marker_cost(), |work| {
        let file = match directory
            .create_exclusive_regular_accounted(MARKER_FILE, work)
            .map_err(exclusive_regular(step, owner))?
        {
            ExclusiveRegularOutcome::Created(file) => file,
            ExclusiveRegularOutcome::EntryExists => {
                return refuse(RegistrationRefusal::Changed(owner));
            }
        };
        prepare_fresh_private_sample(PrivateObjectKind::RegularFile, uid, &file, work)
            .map_err(private(step, owner))?;
        seam.at(Point::MarkerCreated, step, owner)?;
        let receipt = opensip_platform::write_new_regular_accounted(&file, &bytes, work)
            .map_err(write(step, owner))?;
        if !receipt.is_for(&file) {
            return refuse(RegistrationRefusal::BarrierReceipt(step, owner));
        }
        seam.at(Point::MarkerWritten, step, owner)?;
        barrier(directory, policy, step, Owner::MarkerDirectory, work)?;
        let metadata = confirm_file(
            directory,
            MARKER_FILE,
            &file,
            &bytes,
            uid,
            step,
            owner,
            work,
        )?;
        Ok((file, metadata))
    })
}

// ------------------------------------------------- the registered project

/// A project this admission has just registered (item 6, R2). Private, not
/// Clone, not serializable. It holds the root admission's chain, the
/// `.opensip`, marker, `host`, `projects` and namespace owners published or
/// admitted by steps 3 to 5, the current registry owner R2 with its exact
/// ACTIVE row, and the tracking observation. R0 and R1 are provenance. It
/// grants exactly what Eligible grants (item 4): namespace admission, which
/// is X2d's; it takes no lease and holds no lock of its own.
pub(crate) struct RegisteredProject {
    chain: ProjectChain,
    selected: Selected,
    incarnation: Incarnation,
    marker_directory: RetainedDirectory,
    marker: File,
    marker_metadata: DescriptorMetadata,
    host: RetainedDirectory,
    projects: RetainedDirectory,
    namespace: NamedDirectoryPublication,
    registry: RegistryOwner,
    row: ProjectRegistryEntry,
    tracking: TrackingObservation,
}
impl std::fmt::Debug for RegisteredProject {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("RegisteredProject")
            .field("namespace", &self.row.namespace_id())
            .field("project", &self.row.project_id())
            .finish_non_exhaustive()
    }
}
impl RegisteredProject {
    /// N, from R2's ACTIVE row only.
    pub(crate) fn namespace_id(&self) -> &str {
        self.row.namespace_id()
    }
    pub(crate) fn project_id(&self) -> &str {
        self.row.project_id()
    }
    /// R2's exact ACTIVE row.
    pub(crate) fn row(&self) -> &ProjectRegistryEntry {
        &self.row
    }
    /// The current registry owner, R2.
    pub(crate) fn registry(&self) -> &RegistryOwner {
        &self.registry
    }
    pub(crate) fn selected(&self) -> &Selected {
        &self.selected
    }
    pub(crate) fn chain(&self) -> &ProjectChain {
        &self.chain
    }
    pub(crate) fn tracking(&self) -> &TrackingObservation {
        &self.tracking
    }
    /// The published namespace directory, `I/host/projects/N`.
    pub(crate) fn namespace(&self) -> &RetainedDirectory {
        self.namespace.directory()
    }
    /// The classification R2 gives this root with its marker: Eligible.
    pub(crate) fn classification(&self) -> Classification {
        classify(
            self.registry.document.entries(),
            self.chain.spelling().as_os_str().as_bytes(),
            &self.incarnation,
            &MarkerObservation::Present {
                project: self.row.project_id().to_owned(),
                metadata: self.marker_metadata.clone(),
            },
        )
    }
}
/// The current owners step 6 rechecks, and the registered project's
/// recheck: the chain with the root's birth and incarnation, `.opensip`
/// and the marker, `host`, `projects` and the namespace footprint, the
/// registry owner R with the old name absent, and the tracking observation,
/// each through its own retained descriptor. R's predecessors are not
/// rechecked.
struct Current<'a> {
    chain: &'a ProjectChain,
    incarnation: &'a Incarnation,
    marker_directory: &'a RetainedDirectory,
    marker: &'a File,
    marker_metadata: &'a DescriptorMetadata,
    host: &'a RetainedDirectory,
    projects: &'a RetainedDirectory,
    namespace: &'a RetainedDirectory,
    namespace_id: &'a str,
    registry: &'a RegistryOwner,
    tracking: &'a TrackingObservation,
}
#[allow(clippy::too_many_arguments)]
fn recheck_current(
    current: &Current<'_>,
    installation: &DurableInstallation,
    policy: &ProjectChainPolicy<'_>,
    inputs: &ProjectInputs<'_>,
    footprint: Footprint,
    step: Step,
    work: &mut WorkScope<'_>,
) -> Result<(), Failure> {
    let uid = installation.uid();
    let i = installation.installation_directory();
    current.chain.recheck(uid, policy, work).map_err(chain)?;
    if &sample_incarnation(current.chain, work).map_err(admission_failure)? != current.incarnation {
        return refuse(RegistrationRefusal::Changed(Owner::Root));
    }
    rebind(
        current.chain.root(),
        MARKER_DIRECTORY,
        current.marker_directory,
        step,
        Owner::MarkerDirectory,
        work,
    )?;
    project_object(
        current.marker_directory,
        uid,
        policy,
        Owner::MarkerDirectory,
        "marker-directory-custody",
        work,
    )?;
    same_private(
        current.marker,
        current.marker_metadata,
        step,
        Owner::Marker,
        uid,
        work,
    )?;
    let named_marker = open_named(
        current.marker_directory,
        MARKER_FILE,
        step,
        Owner::Marker,
        work,
    )?;
    same_private(
        &named_marker,
        current.marker_metadata,
        step,
        Owner::Marker,
        uid,
        work,
    )?;
    rebind(i, HOST, current.host, step, Owner::Host, work)?;
    observe_private_directory(current.host.as_file(), uid, work)
        .map_err(private(step, Owner::Host))?;
    rebind(
        current.host,
        PROJECTS,
        current.projects,
        step,
        Owner::Projects,
        work,
    )?;
    observe_private_directory(current.projects.as_file(), uid, work)
        .map_err(private(step, Owner::Projects))?;
    rebind(
        current.projects,
        current.namespace_id,
        current.namespace,
        step,
        Owner::Namespace,
        work,
    )?;
    confirm_namespace_files(current.namespace, uid, footprint, step, work)?;
    reconfirm(i, current.registry, step, uid, work)?;
    let tracking_inputs = TrackingInputs {
        chain: current.chain,
        uid,
        policy,
        home: installation.home_spelling(),
        environment: inputs.environment,
        system_sources: inputs.system_sources,
    };
    recheck_tracking(current.tracking, &tracking_inputs, work).map_err(tracking)
}

// --------------------------------------------------- write-gate entries

/// A project step's refusal on the write gate: the gate's own (its latch or
/// recheck), the write receipt's recheck, or the step's own (law X2 item
/// 8). Any of them spends the gate.
#[derive(Debug)]
pub(crate) enum ProjectWriteRefusal {
    /// An earlier refusal spent this writer's gate.
    Latched,
    Gate(GateRefusal),
    Receipt(T),
    Project(AdmissionFailure),
    Tracking(TrackingFailure),
    Registration(Failure),
    /// Item 7's namespace admission or lease (unit X2d).
    Namespace(super::namespace_lease::Failure),
}
/// The row a write-gate project refusal names, for the composition owner.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) enum ProjectWriteRow {
    /// 468 item 6's row, through 468c's map.
    Installation(T),
    /// Law X2 item 8's row.
    Project(RegistrationRow),
    /// `WORK.BUDGET_EXHAUSTED`.
    BudgetExhausted,
}
impl ProjectWriteRefusal {
    pub(crate) fn row(&self) -> ProjectWriteRow {
        use ProjectWriteRow as Row;
        fn work<E>(
            failure: &WorkFailure<E>,
            row: impl FnOnce(&E) -> RegistrationRow,
        ) -> ProjectWriteRow {
            match failure {
                WorkFailure::Budget(_) => ProjectWriteRow::BudgetExhausted,
                WorkFailure::Operation(refusal) => ProjectWriteRow::Project(row(refusal)),
            }
        }
        match self {
            Self::Latched => Row::Installation(T::Invariant),
            Self::Gate(refusal) => Row::Installation(gate_refusal(refusal)),
            Self::Receipt(row) => Row::Installation(row.clone()),
            Self::Project(failure) => work(failure, |r| RegistrationRow::Admission(r.row())),
            Self::Tracking(failure) => work(failure, |r| match r.row() {
                TrackingRow::RootCustody(subject) => RegistrationRow::RootCustody(subject),
                TrackingRow::HostIo => RegistrationRow::HostIo,
            }),
            Self::Registration(failure) => work(failure, RegistrationRefusal::row),
            Self::Namespace(failure) => {
                work(failure, super::namespace_lease::NamespaceRefusal::row)
            }
        }
    }
}

/// Law X2 items 2 to 5 on the write gate (X2b's entry, which X2b-1 left to
/// this unit): S3 selection, the chain walk, the incarnation, the marker,
/// the one registry capture (R0) and the classification, on the gate's own
/// ledger under its held fence, with the write receipt's premise; then the
/// admission's recheck and the gate's full recheck.
pub(super) fn admit_on_gate(
    gate: &mut DurableWriteGate,
    installation: &DurableInstallation,
    qualification: &impl DurableBarrierQualification,
    launch: &Path,
    explicit: Option<&Path>,
    trust_groups: &BTreeSet<u32>,
) -> Result<ProjectRootAdmission, ProjectWriteRefusal> {
    if gate.is_spent() {
        return Err(ProjectWriteRefusal::Latched);
    }
    let home_filesystem = |sample: &DescriptorFilesystem| qualification.is_home_filesystem(sample);
    let policy = ProjectChainPolicy::new(
        qualification.omission_premise(),
        &home_filesystem,
        trust_groups,
    );
    let uid = installation.uid();
    let i = installation.installation_directory();
    // The gate judged the registry among the required files (468 item 5).
    let Some(judged) = judged_registry(installation.required()).cloned() else {
        gate.spend();
        return Err(ProjectWriteRefusal::Registration(WorkFailure::Operation(
            RegistrationRefusal::Invariant("no-registry"),
        )));
    };
    let admission = gate
        .scope(|work| {
            let admission = admit_project_root(
                installation.home_spelling(),
                uid,
                launch,
                explicit,
                i,
                &judged,
                &policy,
                work,
            )?;
            admission.recheck(uid, i, &judged, &policy, work)?;
            Ok(admission)
        })
        .map_err(ProjectWriteRefusal::Project)?;
    gate.recheck(installation, qualification)
        .map_err(ProjectWriteRefusal::Gate)?;
    Ok(admission)
}

/// M3-B unit B1-b, the analysis path's first phase on the write gate:
/// selection retaining the judged `opensip.json`, the chain, incarnation,
/// marker and carriers, on the gate's ledger, then the gate's recheck. No
/// registry is read (X2 r9 item 3a's order).
pub(super) fn admit_carriers_on_gate(
    gate: &mut DurableWriteGate,
    installation: &DurableInstallation,
    qualification: &impl DurableBarrierQualification,
    launch: &Path,
    explicit: Option<&Path>,
    trust_groups: &BTreeSet<u32>,
    local: LocalCarrierPolicy,
) -> Result<CarrierAdmission, ProjectWriteRefusal> {
    if gate.is_spent() {
        return Err(ProjectWriteRefusal::Latched);
    }
    let home_filesystem = |sample: &DescriptorFilesystem| qualification.is_home_filesystem(sample);
    let policy = ProjectChainPolicy::new(
        qualification.omission_premise(),
        &home_filesystem,
        trust_groups,
    );
    let uid = installation.uid();
    let admission = gate
        .scope(|work| {
            admit_project_root_for_analysis(
                installation.home_spelling(),
                uid,
                launch,
                explicit,
                local,
                &policy,
                work,
            )
        })
        .map_err(ProjectWriteRefusal::Project)?;
    gate.recheck(installation, qualification)
        .map_err(ProjectWriteRefusal::Gate)?;
    Ok(admission)
}

/// The analysis path's second phase on the write gate (X2 item 5): the
/// registry capture and classification, the admission's recheck with the
/// carriers, then the gate's recheck.
pub(super) fn complete_on_gate(
    gate: &mut DurableWriteGate,
    installation: &DurableInstallation,
    qualification: &impl DurableBarrierQualification,
    carriers: CarrierAdmission,
    trust_groups: &BTreeSet<u32>,
) -> Result<ProjectRootAdmission, ProjectWriteRefusal> {
    if gate.is_spent() {
        return Err(ProjectWriteRefusal::Latched);
    }
    let home_filesystem = |sample: &DescriptorFilesystem| qualification.is_home_filesystem(sample);
    let policy = ProjectChainPolicy::new(
        qualification.omission_premise(),
        &home_filesystem,
        trust_groups,
    );
    let uid = installation.uid();
    let i = installation.installation_directory();
    let Some(judged) = judged_registry(installation.required()).cloned() else {
        gate.spend();
        return Err(ProjectWriteRefusal::Registration(WorkFailure::Operation(
            RegistrationRefusal::Invariant("no-registry"),
        )));
    };
    let admission = gate
        .scope(|work| {
            let admission = carriers.capture_registry(i, &judged, work)?;
            admission.recheck(uid, i, &judged, &policy, work)?;
            Ok(admission)
        })
        .map_err(ProjectWriteRefusal::Project)?;
    gate.recheck(installation, qualification)
        .map_err(ProjectWriteRefusal::Gate)?;
    Ok(admission)
}

/// Item 6a on the write gate: the tracking observation for an admitted
/// root and its recheck, on the gate's ledger, then the gate's recheck.
pub(super) fn observe_tracking_on_gate(
    gate: &mut DurableWriteGate,
    installation: &DurableInstallation,
    qualification: &impl DurableBarrierQualification,
    admission: &ProjectRootAdmission,
    inputs: &ProjectInputs<'_>,
) -> Result<TrackingObservation, ProjectWriteRefusal> {
    if gate.is_spent() {
        return Err(ProjectWriteRefusal::Latched);
    }
    let home_filesystem = |sample: &DescriptorFilesystem| qualification.is_home_filesystem(sample);
    let policy = ProjectChainPolicy::new(
        qualification.omission_premise(),
        &home_filesystem,
        inputs.trust_groups,
    );
    let tracking_inputs = TrackingInputs {
        chain: admission.chain(),
        uid: installation.uid(),
        policy: &policy,
        home: installation.home_spelling(),
        environment: inputs.environment,
        system_sources: inputs.system_sources,
    };
    let observed = gate
        .scope(|work| {
            let observed = observe_tracking(&tracking_inputs, work)?;
            recheck_tracking(&observed, &tracking_inputs, work)?;
            Ok(observed)
        })
        .map_err(ProjectWriteRefusal::Tracking)?;
    gate.recheck(installation, qualification)
        .map_err(ProjectWriteRefusal::Gate)?;
    Ok(observed)
}

/// Item 6: first registration under the write gate's held fence, on its one
/// ledger. The preconditions run before any effect, then the gate's full
/// recheck; RESERVED (R0 to R1), the namespace, `.opensip` and the marker;
/// every current owner rechecked and ACTIVE (R1 to R2). The gate's retained
/// registry sample advances only with each confirmed publication. Then R2
/// must classify this root Eligible, the registered project is rechecked,
/// and the gate's full recheck runs. Any refusal spends the gate.
pub(super) fn register_on_gate(
    gate: &mut DurableWriteGate,
    installation: &mut DurableInstallation,
    qualification: &impl DurableBarrierQualification,
    admission: ProjectRootAdmission,
    observed: TrackingObservation,
    inputs: &ProjectInputs<'_>,
    seam: &Seam<'_>,
) -> Result<RegisteredProject, ProjectWriteRefusal> {
    use ProjectWriteRefusal::{Gate, Registration};
    if gate.is_spent() {
        return Err(ProjectWriteRefusal::Latched);
    }
    let home_filesystem = |sample: &DescriptorFilesystem| qualification.is_home_filesystem(sample);
    let policy = ProjectChainPolicy::new(
        qualification.omission_premise(),
        &home_filesystem,
        inputs.trust_groups,
    );
    let barrier_policy = qualification.barrier_policy();
    let uid = installation.uid();

    // Preconditions, all before any effect, then the gate's recheck.
    let plan = gate
        .scope(|work| {
            preconditions(
                &admission,
                &observed,
                installation,
                &policy,
                inputs,
                seam,
                work,
            )
        })
        .map_err(Registration)?;
    gate.recheck(installation, qualification).map_err(Gate)?;

    let parts = admission.into_parts();
    let (file, metadata, document) = parts.registry.into_parts();
    let r0 = RegistryOwner {
        file,
        metadata,
        document,
    };

    // Step 2: RESERVED (R0 to R1).
    let Plan {
        project,
        namespace,
        reserved,
    } = plan;
    // X9: X2c's effects run under the held fence, as `x2.fence.register.*`
    // (law X9 r1 item 5).
    let r1 = gate
        .scope(|work| {
            opensip_platform::crash_scope!("x2.fence.register.reserved", {
                replace(
                    installation.installation_directory(),
                    &r0,
                    reserved,
                    Step::Reserved,
                    uid,
                    barrier_policy,
                    seam,
                    work,
                )
            })
        })
        .map_err(Registration)?;
    if !installation.advance_registry(&r0.metadata, r1.metadata.clone()) {
        gate.spend();
        return Err(Registration(WorkFailure::Operation(
            RegistrationRefusal::Invariant("registry-advance"),
        )));
    }
    drop(r0);

    // Step 3: the namespace and its parents.
    let (host, projects, publication) = gate
        .scope(|work| {
            opensip_platform::crash_scope!("x2.fence.register.namespace", {
                publish_namespace(
                    installation.installation_directory(),
                    &namespace,
                    uid,
                    &home_filesystem,
                    barrier_policy,
                    seam,
                    work,
                )
            })
        })
        .map_err(Registration)?;

    // Step 4: `.opensip`.
    let opensip = gate
        .scope(|work| {
            opensip_platform::crash_scope!("x2.fence.register.marker-directory", {
                marker_directory(&parts.chain, uid, &policy, barrier_policy, seam, work)
            })
        })
        .map_err(Registration)?;

    // Step 5: the marker.
    let (marker, marker_metadata) = gate
        .scope(|work| {
            opensip_platform::crash_scope!("x2.fence.register.marker", {
                create_marker(&opensip, &project, uid, barrier_policy, seam, work)
            })
        })
        .map_err(Registration)?;

    // Step 6: every current owner, then ACTIVE (R1 to R2).
    let r2 = gate
        .scope(|work| {
            let current = Current {
                chain: &parts.chain,
                incarnation: &parts.incarnation,
                marker_directory: &opensip,
                marker: &marker,
                marker_metadata: &marker_metadata,
                host: &host,
                projects: &projects,
                namespace: publication.directory(),
                namespace_id: &namespace,
                registry: &r1,
                tracking: &observed,
            };
            recheck_current(
                &current,
                installation,
                &policy,
                inputs,
                Footprint::Exact,
                Step::Active,
                work,
            )?;
            transitions_quiet(
                installation.installation_directory(),
                uid,
                Step::Active,
                work,
            )?;
            let active = plan_active(r1.document(), &namespace, work)?;
            opensip_platform::crash_scope!("x2.fence.register.active", {
                replace(
                    installation.installation_directory(),
                    &r1,
                    active,
                    Step::Active,
                    uid,
                    barrier_policy,
                    seam,
                    work,
                )
            })
        })
        .map_err(Registration)?;
    if !installation.advance_registry(&r1.metadata, r2.metadata.clone()) {
        gate.spend();
        return Err(Registration(WorkFailure::Operation(
            RegistrationRefusal::Invariant("registry-advance"),
        )));
    }
    drop(r1);

    // R2 is the only source of the ACTIVE row and of Eligible.
    let row = r2
        .document
        .entries()
        .iter()
        .find(|entry| entry.namespace_id() == namespace)
        .cloned();
    let Some(row) = row else {
        gate.spend();
        return Err(Registration(WorkFailure::Operation(
            RegistrationRefusal::Invariant("active-row"),
        )));
    };
    let registered = RegisteredProject {
        chain: parts.chain,
        selected: parts.selected,
        incarnation: parts.incarnation,
        marker_directory: opensip,
        marker,
        marker_metadata,
        host,
        projects,
        namespace: publication,
        registry: r2,
        row,
        tracking: observed,
    };
    gate.scope(|work| {
        let eligible = work.run(
            WorkCost {
                objects: 1,
                edges: registered.registry.document.entries().len().max(1),
                bytes: registered.registry.document.raw().len(),
            },
            |_| Ok(registered.classification()),
        )?;
        let expected = Classification::Eligible {
            namespace: namespace.clone(),
            project: project.clone(),
        };
        if eligible != expected || registered.row.status() != ProjectRegistryStatus::Active {
            return refuse(RegistrationRefusal::Invariant("not-eligible"));
        }
        recheck_registered(
            &registered,
            installation,
            &policy,
            inputs,
            Step::Confirmed,
            work,
        )
    })
    .map_err(Registration)?;
    gate.recheck(installation, qualification).map_err(Gate)?;
    Ok(registered)
}

/// Law X4 r7 item 4 (unit X4a): a registered project's original owners
/// only, after the fence is released: the chain, the root's incarnation,
/// `.opensip` (bound by name and still the project's) and the marker (the
/// same private file, by descriptor and by name). The registry, the
/// tracking observation and `host` and `projects` are not rechecked here;
/// N is the operation's own namespace guard.
pub(super) fn recheck_registered_owners(
    registered: &RegisteredProject,
    uid: u32,
    policy: &ProjectChainPolicy<'_>,
    work: &mut WorkScope<'_>,
) -> Result<(), Failure> {
    let step = Step::Handoff;
    registered.chain.recheck(uid, policy, work).map_err(chain)?;
    if sample_incarnation(&registered.chain, work).map_err(admission_failure)?
        != registered.incarnation
    {
        return refuse(RegistrationRefusal::Changed(Owner::Root));
    }
    rebind(
        registered.chain.root(),
        MARKER_DIRECTORY,
        &registered.marker_directory,
        step,
        Owner::MarkerDirectory,
        work,
    )?;
    project_object(
        &registered.marker_directory,
        uid,
        policy,
        Owner::MarkerDirectory,
        "marker-directory-custody",
        work,
    )?;
    same_private(
        &registered.marker,
        &registered.marker_metadata,
        step,
        Owner::Marker,
        uid,
        work,
    )?;
    let named = open_named(
        &registered.marker_directory,
        MARKER_FILE,
        step,
        Owner::Marker,
        work,
    )?;
    same_private(
        &named,
        &registered.marker_metadata,
        step,
        Owner::Marker,
        uid,
        work,
    )
}

/// The registered project's recheck set (item 3's, with the owners item 6
/// published), on the given ledger, with item 6's exact namespace
/// footprint.
pub(super) fn recheck_registered(
    registered: &RegisteredProject,
    installation: &DurableInstallation,
    policy: &ProjectChainPolicy<'_>,
    inputs: &ProjectInputs<'_>,
    step: Step,
    work: &mut WorkScope<'_>,
) -> Result<(), Failure> {
    recheck_registered_with(
        registered,
        installation,
        policy,
        inputs,
        Footprint::Exact,
        step,
        work,
    )
}
/// The registered project's recheck set under `footprint`. Every owner is
/// rechecked as `recheck_registered` rechecks it; only the namespace's
/// closed entry scan depends on `footprint` (unit X2e: after X3b's carrier
/// start, N also holds the carrier and its witness).
pub(super) fn recheck_registered_with(
    registered: &RegisteredProject,
    installation: &DurableInstallation,
    policy: &ProjectChainPolicy<'_>,
    inputs: &ProjectInputs<'_>,
    footprint: Footprint,
    step: Step,
    work: &mut WorkScope<'_>,
) -> Result<(), Failure> {
    let current = Current {
        chain: &registered.chain,
        incarnation: &registered.incarnation,
        marker_directory: &registered.marker_directory,
        marker: &registered.marker,
        marker_metadata: &registered.marker_metadata,
        host: &registered.host,
        projects: &registered.projects,
        namespace: registered.namespace.directory(),
        namespace_id: registered.row.namespace_id(),
        registry: &registered.registry,
        tracking: &registered.tracking,
    };
    recheck_current(
        &current,
        installation,
        policy,
        inputs,
        footprint,
        step,
        work,
    )
}

/// The registered project's recheck on the write gate, then the gate's.
pub(super) fn recheck_registered_on_gate(
    gate: &mut DurableWriteGate,
    installation: &DurableInstallation,
    qualification: &impl DurableBarrierQualification,
    registered: &RegisteredProject,
    inputs: &ProjectInputs<'_>,
) -> Result<(), ProjectWriteRefusal> {
    if gate.is_spent() {
        return Err(ProjectWriteRefusal::Latched);
    }
    let home_filesystem = |sample: &DescriptorFilesystem| qualification.is_home_filesystem(sample);
    let policy = ProjectChainPolicy::new(
        qualification.omission_premise(),
        &home_filesystem,
        inputs.trust_groups,
    );
    gate.scope(|work| {
        recheck_registered(
            registered,
            installation,
            &policy,
            inputs,
            Step::Confirmed,
            work,
        )
    })
    .map_err(ProjectWriteRefusal::Registration)?;
    gate.recheck(installation, qualification)
        .map_err(ProjectWriteRefusal::Gate)
}

/// The process environment and the fixed system sources, for the
/// production entries (item 6a reads them only to refuse).
pub(crate) fn production_sources() -> (Vec<(OsString, OsString)>, Vec<PathBuf>) {
    (
        super::git_tracking::process_environment(),
        super::git_tracking::SYSTEM_SOURCES
            .iter()
            .map(PathBuf::from)
            .collect(),
    )
}

#[cfg(test)]
mod tests {
    include!("first_registration_tests.rs");
}
