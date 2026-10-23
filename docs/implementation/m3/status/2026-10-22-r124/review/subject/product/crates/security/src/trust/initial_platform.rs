// Law 462 (items 1-9): the platform receipt of the initial creator, owner
// §1a step 4. The profile is authenticated under InitialCore's release context
// only, every native observation is charged to the attempt's one ledger, and
// Evidence B (law 458) is minted here and nowhere else. No probe, no effect.
use super::admitted_profiles::{InitialProfile, verify_initial_core_pinned, verify_initial_signed};
use super::initial_core::{InitialCore, InitialCoreRefusal, ReleaseFile};
use super::native_platform::{machine, usable_filesystem_id};
use super::*;
use crate::custody::installation_root::ParentRefusal;
use crate::initial_installation::{ActorRefusal, InitialActor, InitialInstallationAttempt};
use opensip_platform::{
    DescriptorFilesystem, MacosBootError, MacosBootObservation, MacosLoaderError,
    MacosLoaderObservation, MacosProcessError, MacosProcessObservation, RetainedDirectoryPath,
    WorkCost, WorkFailure, WorkScope,
};
use std::{io, path::Path};

/// Item 1: the two fixed names below the core tree root.
const PROFILE: [&str; 2] = ["platform", "profile-set.json"];
const ENVELOPE: [&str; 2] = ["platform", "profile-set.sig.json"];
/// Owner §2: 256 components to I, less the four fixed suffix components.
const MAX_HOME_COMPONENTS: usize = 252;
/// The observed identity object: the map, its seven keys and bounded values.
const OBSERVED: WorkCost = WorkCost {
    objects: 15,
    edges: 1,
    bytes: 1024,
};
/// `same_home`'s two status reads, each with a buffer no smaller than `stat`.
const HOME_IDENTITY: WorkCost = WorkCost {
    objects: 0,
    edges: 2,
    bytes: 1024,
};
/// One owned name or citation string, at most a filesystem type name or a
/// bounded build, lane or UUID.
const NAME: WorkCost = WorkCost {
    objects: 1,
    edges: 0,
    bytes: 64,
};

#[derive(Debug)]
pub(crate) enum InitialPlatformRefusal {
    WrongAttempt,
    Process(MacosProcessError),
    Translated,
    Boot(MacosBootError),
    Loader(MacosLoaderError),
    /// The process and loader name no supported machine.
    UnsupportedPopulation,
    /// The observed machine is not InitialCore's compiled platform (item 3).
    PlatformMismatch,
    LoaderFilesystem,
    /// Opening or rechecking a profile file under the core tree.
    Core(InitialCoreRefusal),
    /// The inventory has no `platformProfileSetBodyDigest`.
    ProfilePin,
    /// A profile file is not the platform row's tree file of that name.
    ProfileRow,
    Profile(ProfileError),
    Home(io::Error),
    /// H is not local, is a union mount, is read-only, or its type is not in
    /// `installRootFilesystems` (item 4).
    HomeFilesystem,
    Decision(PlatformError),
    /// The decision refused, has no tier, or names another platform.
    Unadmitted(Vec<String>),
    Changed,
    Actor(ActorRefusal),
}
type Failure = WorkFailure<InitialPlatformRefusal>;
use InitialPlatformRefusal as R;

/// Item 5: the primitive policy H's filesystem selects. Recorded, never probed;
/// the typed receipts are taken at effect time (465, 467).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum PrimitivePolicy {
    /// Exclusive same-parent `renameatx_np(RENAME_EXCL)` and `F_FULLFSYNC`,
    /// with the §5.6 `Fsync` fallback only for its named unsupported errors.
    Apfs,
}

#[derive(Clone, Copy)]
enum Source {
    Live,
    /// A given process sample, charged as the live one.
    #[cfg(test)]
    Process(MacosProcessObservation),
}
impl Source {
    fn process(self, work: &mut WorkScope<'_>) -> Result<MacosProcessObservation, Failure> {
        match self {
            Self::Live => opensip_platform::observe_macos_process_accounted(work)
                .map_err(lift(R::Process)),
            #[cfg(test)]
            Self::Process(process) => {
                work.run(opensip_platform::macos_process_observation_cost(), |_| {
                    Ok(process)
                })
            }
        }
    }
}

/// The matched measured row Evidence B cites (item 6). In memory only.
#[derive(Debug, PartialEq, Eq)]
struct RowCitation {
    profile_digest: [u8; 32],
    platform: &'static str,
    lane: String,
    build: String,
    kern_uuid: String,
    dyld_cdhash: [u8; 20],
}

/// Evidence B of law 458: an omitted ACL on an external ancestor counts as a
/// present empty ACL only when this premise admits that descriptor's own
/// filesystem sample, taken here. Minted only by `InitialPlatform` from a V2
/// matched measured row carrying `installAclOmission`. Private, not Clone,
/// bound to the attempt. Its scope is law 458 §5's, enforced by 460.
pub(crate) struct AclOmissionPremise {
    lineage: [u8; 16],
    filesystems: Vec<Box<[u8]>>,
    citation: RowCitation,
}
impl std::fmt::Debug for AclOmissionPremise {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("AclOmissionPremise").finish_non_exhaustive()
    }
}
impl AclOmissionPremise {
    #[cfg(test)]
    pub(crate) fn for_tests(
        attempt: &InitialInstallationAttempt,
        filesystems: &'static [&'static [u8]],
    ) -> Self {
        Self {
            lineage: attempt.lineage(),
            filesystems: filesystems.iter().map(|n| Box::from(*n)).collect(),
            citation: RowCitation {
                profile_digest: [0; 32],
                platform: "",
                lane: String::new(),
                build: String::new(),
                kern_uuid: String::new(),
                dyld_cdhash: [0; 20],
            },
        }
    }
    pub(crate) fn lineage(&self) -> [u8; 16] {
        self.lineage
    }
    /// Sample this descriptor's filesystem and admit it only when it is local,
    /// not a union mount, and its type name is qualified by the premise.
    pub(crate) fn admits(
        &self,
        directory: &std::fs::File,
        work: &mut WorkScope<'_>,
    ) -> Result<bool, WorkFailure<ParentRefusal>> {
        let sample =
            opensip_platform::observe_filesystem_accounted(directory, work).map_err(|f| match f {
                WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
                WorkFailure::Operation(e) => WorkFailure::Operation(ParentRefusal::Filesystem(e)),
            })?;
        Ok(self.qualifies(&sample))
    }
    /// `admits`, spending the same sample from an existing reservation (law
    /// 465 item 6). The premise still takes its own `fstatfs`.
    pub(crate) fn admits_reserved(
        &self,
        directory: &std::fs::File,
        post: &mut opensip_platform::ReservedPostchecks<'_>,
    ) -> Result<bool, WorkFailure<ParentRefusal>> {
        let sample =
            opensip_platform::observe_filesystem_reserved(directory, post).map_err(|f| match f {
                WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
                WorkFailure::Operation(e) => WorkFailure::Operation(ParentRefusal::Filesystem(e)),
            })?;
        Ok(self.qualifies(&sample))
    }
    fn qualifies(&self, sample: &DescriptorFilesystem) -> bool {
        sample.is_local()
            && !sample.is_union()
            && self.filesystems.iter().any(|n| **n == *sample.name())
    }
}

/// Owner §1a step 4's receipt. Private, not Clone, bound to one attempt.
pub(crate) struct InitialPlatform {
    lineage: [u8; 16],
    source: Source,
    platform: &'static str,
    process: MacosProcessObservation,
    boot: MacosBootObservation,
    loader: MacosLoaderObservation,
    loader_fs: DescriptorFilesystem,
    profile: InitialProfile,
    profile_file: ReleaseFile,
    envelope_file: Option<ReleaseFile>,
    home: RetainedDirectoryPath,
    home_fs: DescriptorFilesystem,
    install_filesystems: Vec<Box<[u8]>>,
    observed: V,
    decision: PlatformDecision,
    policy: PrimitivePolicy,
    premise: Option<AclOmissionPremise>,
}
impl std::fmt::Debug for InitialPlatform {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("InitialPlatform").finish_non_exhaustive()
    }
}
impl InitialPlatform {
    pub(crate) fn lineage(&self) -> [u8; 16] {
        self.lineage
    }
    pub(crate) fn platform(&self) -> &'static str {
        self.platform
    }
    pub(crate) fn tier(&self) -> &PlatformTier {
        self.decision.tier.as_ref().expect("admitted at a tier")
    }
    pub(crate) fn home_filesystem(&self) -> &DescriptorFilesystem {
        &self.home_fs
    }
    pub(crate) fn policy(&self) -> PrimitivePolicy {
        self.policy
    }
    /// Item 4: `fs` is a sample of H's own mounted filesystem.
    pub(crate) fn qualifies_installation_filesystem(&self, fs: &DescriptorFilesystem) -> bool {
        fs.is_local()
            && !fs.is_union()
            && usable_filesystem_id(fs.native_id())
            && fs.native_id() == self.home_fs.native_id()
            && fs.device() == self.home_fs.device()
            && fs.name() == self.home_fs.name()
    }
    pub(crate) fn acl_omission_premise(&self) -> Option<&AclOmissionPremise> {
        self.premise.as_ref()
    }
    /// Law 465 item 7: `directory` is this receipt's retained H, by device
    /// and inode. Two charged status reads; a sample, not exclusion.
    pub(crate) fn same_home(
        &self,
        directory: &opensip_platform::RetainedDirectory,
        work: &mut WorkScope<'_>,
    ) -> Result<bool, WorkFailure<io::Error>> {
        use std::os::unix::fs::MetadataExt;
        work.run(HOME_IDENTITY, |_| {
            let ours = self.home.directory().as_file().metadata();
            let theirs = directory.as_file().metadata();
            match (ours, theirs) {
                (Ok(ours), Ok(theirs)) => {
                    Ok((ours.dev(), ours.ino()) == (theirs.dev(), theirs.ino()))
                }
                (Err(e), _) | (_, Err(e)) => Err(WorkFailure::Operation(e)),
            }
        })
    }
    /// Item 9: re-sample everything on the attempt's ledger and require
    /// equality. A sample, not exclusion. Any refusal latches.
    pub(crate) fn recheck(&self, attempt: &mut InitialInstallationAttempt) -> Result<(), Failure> {
        if !attempt.require_lineage(self.lineage) {
            return Err(WorkFailure::Operation(R::WrongAttempt));
        }
        attempt.run(|work| self.recheck_in(work))
    }
    /// The same recheck on a borrowed scope, for a caller that has already
    /// checked the lineage (law 467 item 6: inside the rename's reservation).
    pub(crate) fn recheck_in(&self, work: &mut WorkScope<'_>) -> Result<(), Failure> {
        let process = self.source.process(work)?;
        let boot = opensip_platform::observe_macos_boot_accounted(work).map_err(lift(R::Boot))?;
        self.loader
            .recheck_accounted(work)
            .map_err(lift(R::Loader))?;
        let loader_fs = self
            .loader
            .filesystem_accounted(work)
            .map_err(lift(R::Loader))?;
        let names = self
            .home
            .recheck_exact_names_accounted(work)
            .map_err(lift(R::Home))?;
        let home_fs =
            opensip_platform::observe_filesystem_accounted(self.home.directory().as_file(), work)
                .map_err(lift(R::Home))?;
        for file in [Some(&self.profile_file), self.envelope_file.as_ref()]
            .into_iter()
            .flatten()
        {
            file.recheck(work).map_err(lift(R::Core))?;
        }
        operation(
            names
                && machine(process, self.loader.cpu()).ok() == Some(self.platform)
                && process == self.process
                && boot == self.boot
                && loader_fs == self.loader_fs
                && home_fs == self.home_fs,
            (),
            R::Changed,
        )
    }
}

fn lift<E>(
    wrap: impl FnOnce(E) -> InitialPlatformRefusal,
) -> impl FnOnce(WorkFailure<E>) -> Failure {
    move |failure| match failure {
        WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
        WorkFailure::Operation(error) => WorkFailure::Operation(wrap(error)),
    }
}
fn operation<T>(ok: bool, value: T, refusal: InitialPlatformRefusal) -> Result<T, Failure> {
    if ok {
        Ok(value)
    } else {
        Err(WorkFailure::Operation(refusal))
    }
}
/// A charged allowance for one parse or verification over `bytes` of source.
fn parse_cost(bytes: usize) -> WorkCost {
    WorkCost {
        objects: 1,
        edges: 1,
        bytes: bytes.saturating_mul(4),
    }
}
/// Item 7: a SYNTHETIC profile set never mints Evidence B outside tests.
fn standing_admits(standing: Option<&str>, tests: bool) -> bool {
    standing.is_some_and(|s| s != "SYNTHETIC" || tests)
}
/// Item 1: open one fixed file and join its bytes to the platform row.
fn open_profile_file(
    core: &InitialCore,
    path: [&str; 2],
    work: &mut WorkScope<'_>,
) -> Result<(ReleaseFile, Vec<u8>), Failure> {
    let (file, raw) = core
        .open_release_file(&path, work)
        .map_err(lift(R::Core))?;
    let joined = work.run(NAME, |_| Ok(path.join("/")))?;
    let row = core.tree_file(&joined);
    operation(
        row == Some((file.sha256(), i64::try_from(file.length()).unwrap_or(-1))),
        (file, raw),
        R::ProfileRow,
    )
}
/// Item 2: the final root decides the path; an envelope's presence never does.
fn profile_role_active(root: &ValidatedRootPayload) -> bool {
    root.schema() == 2
        && object(root.value())
            .and_then(|o| o.get("roles"))
            .and_then(object)
            .and_then(|r| r.get("TR-PROFILE"))
            .and_then(object)
            .and_then(|r| r.get("standing"))
            .and_then(string)
            == Some("active")
}

/// Owner §1a step 4 for this attempt. Every step runs on the attempt's one
/// ledger; any refusal latches the attempt.
pub(crate) fn produce_initial_platform(
    attempt: &mut InitialInstallationAttempt,
    actor: &InitialActor,
    core: &InitialCore,
) -> Result<InitialPlatform, Failure> {
    produce_with(attempt, actor, actor.home(), core, Source::Live)
}
fn produce_with(
    attempt: &mut InitialInstallationAttempt,
    actor: &InitialActor,
    home: &Path,
    core: &InitialCore,
    source: Source,
) -> Result<InitialPlatform, Failure> {
    // P0: both receipts belong to this attempt.
    if !attempt.require_lineage(core.lineage()) || !attempt.require_lineage(actor.lineage()) {
        return Err(WorkFailure::Operation(R::WrongAttempt));
    }
    let lineage = attempt.lineage();
    let platform = attempt.run(|work| produce_in(work, lineage, home, core, source))?;
    // P12: the actor, after the closing recheck.
    attempt.recheck_actor(actor).map_err(lift(R::Actor))?;
    Ok(platform)
}

fn produce_in(
    work: &mut WorkScope<'_>,
    lineage: [u8; 16],
    home_path: &Path,
    core: &InitialCore,
    source: Source,
) -> Result<InitialPlatform, Failure> {
    // P1-P3: process, boot and the system loader (348a), each charged first.
    let process = source.process(work)?;
    operation(
        process != MacosProcessObservation::Translated,
        (),
        R::Translated,
    )?;
    let boot = opensip_platform::observe_macos_boot_accounted(work).map_err(lift(R::Boot))?;
    let loader =
        opensip_platform::capture_system_loader_accounted(work).map_err(lift(R::Loader))?;
    // P4: the machine is InitialCore's compiled platform (item 3).
    let platform = machine(process, loader.cpu())
        .map_err(|_| WorkFailure::Operation(R::UnsupportedPopulation))?;
    operation(platform == core.platform(), (), R::PlatformMismatch)?;
    // P5: the loader's own filesystem sample.
    let loader_fs = loader.filesystem_accounted(work).map_err(lift(R::Loader))?;
    operation(
        loader_fs.is_local()
            && !loader_fs.is_union()
            && loader_fs.is_read_only()
            && loader_fs.name() == b"apfs",
        (),
        R::LoaderFilesystem,
    )?;
    // P6, P7: the profile bytes, then the path the final root selects.
    let pin = core
        .profile_pin()
        .ok_or(WorkFailure::Operation(R::ProfilePin))?;
    let (profile_file, stored) = open_profile_file(core, PROFILE, work)?;
    let root = core.final_root();
    let (envelope_file, profile) = if profile_role_active(root) {
        let (file, raw) = open_profile_file(core, ENVELOPE, work)?;
        let profile = work.run(parse_cost(stored.len() + raw.len()), |_| {
            let envelope = super::super::metadata::parse(&raw)
                .map_err(|_| WorkFailure::Operation(R::Profile(ProfileError::Envelope)))?;
            verify_initial_signed(root, &stored, &envelope, pin, core.revoked())
                .map_err(|e| WorkFailure::Operation(R::Profile(e)))
        })?;
        (Some(file), profile)
    } else {
        let profile = work.run(parse_cost(stored.len()), |_| {
            verify_initial_core_pinned(&stored, pin)
                .map_err(|e| WorkFailure::Operation(R::Profile(e)))
        })?;
        (None, profile)
    };
    drop(stored);
    // P8: H, retained no-follow, and its own filesystem sample (item 4).
    let home = RetainedDirectoryPath::open_accounted(home_path, MAX_HOME_COMPONENTS, work)
        .map_err(lift(R::Home))?;
    let home_fs = opensip_platform::observe_filesystem_accounted(home.directory().as_file(), work)
        .map_err(lift(R::Home))?;
    let listed = object(profile.payload())
        .and_then(|p| p.get("platforms"))
        .and_then(object)
        .and_then(|p| p.get(platform))
        .and_then(object)
        .and_then(|p| p.get("installRootFilesystems"))
        .and_then(array)
        .unwrap_or(&[]);
    let mut install_filesystems: Vec<Box<[u8]>> = Vec::new();
    for name in listed.iter().filter_map(string) {
        install_filesystems.push(work.run(NAME, |_| Ok(Box::from(name.as_bytes())))?);
    }
    operation(
        home_fs.is_local()
            && !home_fs.is_union()
            && !home_fs.is_read_only()
            && install_filesystems.iter().any(|n| **n == *home_fs.name()),
        (),
        R::HomeFilesystem,
    )?;
    // P11: the recorded policy (item 5).
    let policy = operation(home_fs.name() == b"apfs", PrimitivePolicy::Apfs, R::HomeFilesystem)?;
    // P9: the full observed identity, with H's type; an admitted decision.
    let fs_type = std::str::from_utf8(home_fs.name())
        .map_err(|_| WorkFailure::Operation(R::HomeFilesystem))?;
    let observed = work.run(OBSERVED, |_| {
        Ok(V::Object(BTreeMap::from([
            ("platform".into(), V::String(platform.into())),
            ("fsType".into(), V::String(fs_type.into())),
            (
                "authenticatedRoot".into(),
                V::String(
                    if boot.unauthenticated_root_allowed() {
                        "disabled"
                    } else {
                        "enabled"
                    }
                    .into(),
                ),
            ),
            (
                "sip".into(),
                V::Bool(!boot.unrestricted_filesystem_allowed()),
            ),
            ("osversion".into(), V::String(boot.os_build().into())),
            ("kernUuid".into(), V::String(boot.kernel_uuid().into())),
            (
                "dyldCdhash".into(),
                V::String(loader.cdhash().iter().map(|b| format!("{b:02x}")).collect()),
            ),
        ])))
    })?;
    let decision = work.run(parse_cost(OBSERVED.bytes), |_| {
        platform_decision(
            platform_profile::AdmittedProfile::from_initial(&profile),
            &observed,
        )
        .map_err(|e| WorkFailure::Operation(R::Decision(e)))
    })?;
    if !decision.refusals.is_empty()
        || decision.tier.is_none()
        || decision.platform.as_deref() != Some(core.platform())
    {
        return Err(WorkFailure::Operation(R::Unadmitted(decision.refusals)));
    }
    // P10: Evidence B (items 6, 7).
    let premise = if profile.is_v2()
        && decision.install_acl_omission()
        && standing_admits(
            profile.standing(),
            cfg!(any(test, feature = "crash-matrix", feature = "scenario-fixtures")),
        )
    {
        let mut filesystems = Vec::new();
        for name in &install_filesystems {
            filesystems.push(work.run(NAME, |_| Ok(name.clone()))?);
        }
        let citation = work.run(
            WorkCost {
                objects: 3,
                edges: 0,
                bytes: 3 * NAME.bytes,
            },
            |_| {
                Ok(RowCitation {
                    profile_digest: profile.digest(),
                    platform,
                    lane: decision.lane.clone().expect("a lane is required"),
                    build: boot.os_build().into(),
                    kern_uuid: boot.kernel_uuid().into(),
                    dyld_cdhash: loader.cdhash(),
                })
            },
        )?;
        Some(AclOmissionPremise {
            lineage,
            filesystems,
            citation,
        })
    } else {
        None
    };
    // P12: the closing recheck.
    let receipt = InitialPlatform {
        lineage,
        source,
        platform,
        process,
        boot,
        loader,
        loader_fs,
        profile,
        profile_file,
        envelope_file,
        home,
        home_fs,
        install_filesystems,
        observed,
        decision,
        policy,
        premise,
    };
    receipt.recheck_in(work)?;
    Ok(receipt)
}

#[cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))]
#[cfg_attr(not(test), allow(dead_code, unused_imports))]
pub(super) mod tests {
    include!("initial_platform_tests.rs");
}
