// Read-only native account-derived operational I. This observes an existing root
// or a missing suffix, never authorizes initialization or grants current authority.
// Explicit trust-group invocation provenance and elevated-process admission remain
// separate. No HOME/XDG/PATH/argv/project-root override or filesystem mutation.
use super::{DirectoryPathRefusal, inspect_directory_path};
use opensip_platform::{
    AccountObservation, AccountObservationError, RetainedDirectoryPath, observe_account,
};
use std::{
    collections::BTreeSet,
    io,
    path::{Path, PathBuf},
    sync::Arc,
};
pub(super) const SUFFIX: [&str; 4] = ["Library", "Application Support", "OpenSIP", "preview-v1"];
// Engineering descriptor bound, not the project-discovery depth contract or a
// wall-clock guarantee. The four fixed children count against the same limit.
pub(super) const MAX_COMPONENTS: usize = 256;
#[derive(Debug)]
pub(crate) enum Error {
    Account(AccountObservationError),
    DifferentCredentials,
    AccountChanged,
    Custody(DirectoryPathRefusal),
    Native(io::Error),
    Appeared,
}
struct AccountKey {
    real: u32,
    effective: u32,
    home: PathBuf,
}
impl AccountKey {
    fn from_native(a: AccountObservation) -> Result<Self, Error> {
        let key = Self {
            real: a.real_uid(),
            effective: a.effective_uid(),
            home: a.home().to_owned(),
        };
        key.check_credentials()?;
        Ok(key)
    }
    fn check_credentials(&self) -> Result<(), Error> {
        if self.real != self.effective {
            return Err(Error::DifferentCredentials);
        }
        Ok(())
    }
    fn matches(&self, other: &Self) -> Result<(), Error> {
        other.check_credentials()?;
        if self.real != other.real
            || self.effective != other.effective
            || self.home.as_os_str() != other.home.as_os_str()
        {
            return Err(Error::AccountChanged);
        }
        Ok(())
    }
}
pub(crate) struct ExistingRoot {
    path: Arc<RetainedDirectoryPath>,
}
pub(crate) struct MissingRoot {
    prefix: Arc<RetainedDirectoryPath>,
    next_path: PathBuf,
    missing_index: usize,
}
pub(crate) enum RootObservation {
    Existing(ExistingRoot),
    Missing(MissingRoot),
}
impl RootObservation {
    fn capture(home: &Path, uid: u32, groups: &BTreeSet<u32>) -> Result<Self, Error> {
        Self::capture_with(home, uid, groups, |_| {})
    }
    // Sequencing seam only; cannot substitute descriptors or fabricated results.
    fn capture_with(
        home: &Path,
        uid: u32,
        groups: &BTreeSet<u32>,
        mut after_open: impl FnMut(usize),
    ) -> Result<Self, Error> {
        let mut path = home.to_owned();
        let mut retained =
            Arc::new(RetainedDirectoryPath::open(home, MAX_COMPONENTS).map_err(Error::Native)?);
        inspect_directory_path(&retained, uid, groups).map_err(Error::Custody)?;
        for (index, component) in SUFFIX.iter().enumerate() {
            inspect_directory_path(&retained, uid, groups).map_err(Error::Custody)?;
            path.push(component);
            let opened = RetainedDirectoryPath::open(&path, MAX_COMPONENTS);
            after_open(index);
            // A failed open must not turn a moved/unsafe parent into absence.
            inspect_directory_path(&retained, uid, groups).map_err(Error::Custody)?;
            match opened {
                Ok(next) => {
                    inspect_directory_path(&next, uid, groups).map_err(Error::Custody)?;
                    retained = Arc::new(next);
                }
                Err(e) if e.kind() == io::ErrorKind::NotFound => {
                    let result = Self::Missing(MissingRoot {
                        prefix: retained,
                        next_path: path,
                        missing_index: index,
                    });
                    result.recheck(uid, groups)?;
                    return Ok(result);
                }
                Err(e) => return Err(Error::Native(e)),
            }
        }
        let result = Self::Existing(ExistingRoot { path: retained });
        result.recheck(uid, groups)?;
        Ok(result)
    }
    fn recheck(&self, uid: u32, groups: &BTreeSet<u32>) -> Result<(), Error> {
        match self {
            Self::Existing(root) => {
                inspect_directory_path(&root.path, uid, groups).map_err(Error::Custody)?;
            }
            Self::Missing(root) => {
                inspect_directory_path(&root.prefix, uid, groups).map_err(Error::Custody)?;
                let opened = RetainedDirectoryPath::open(&root.next_path, MAX_COMPONENTS);
                inspect_directory_path(&root.prefix, uid, groups).map_err(Error::Custody)?;
                match opened {
                    Err(e) if e.kind() == io::ErrorKind::NotFound => {}
                    Err(e) => return Err(Error::Native(e)),
                    Ok(_) => return Err(Error::Appeared),
                }
            }
        }
        Ok(())
    }
}
impl ExistingRoot {
    pub(crate) fn retained_path(&self) -> &Arc<RetainedDirectoryPath> {
        &self.path
    }
}
impl MissingRoot {
    // Only the fixed remaining components; does not grant mkdir/initialization.
    pub(crate) fn remaining_components(&self) -> &[&'static str] {
        &SUFFIX[self.missing_index..]
    }
}
// Account/home provenance stays owned through every later observation recheck.
// No Debug representation discloses the native home path or account identifiers.
pub(crate) struct NativeInstallationRoot {
    account: AccountKey,
    supplied_groups: BTreeSet<u32>,
    observation: RootObservation,
}
impl NativeInstallationRoot {
    pub(crate) fn capture(supplied_groups: &BTreeSet<u32>) -> Result<Self, Error> {
        Self::capture_observing(supplied_groups, Self::native_account)
    }
    fn native_account() -> Result<AccountKey, Error> {
        AccountKey::from_native(observe_account().map_err(Error::Account)?)
    }
    // Private sequencing seam; the only production caller uses native_account.
    // Synthetic test sources never enter a public/native-authority constructor.
    fn capture_observing(
        supplied_groups: &BTreeSet<u32>,
        mut sample: impl FnMut() -> Result<AccountKey, Error>,
    ) -> Result<Self, Error> {
        let account = sample()?;
        account.check_credentials()?;
        let observed = RootObservation::capture(&account.home, account.effective, supplied_groups);
        account.matches(&sample()?)?;
        let result = Self {
            account,
            supplied_groups: supplied_groups.clone(),
            observation: observed?,
        };
        result.recheck_observing(sample)?;
        Ok(result)
    }
    pub(crate) fn recheck(&self) -> Result<(), Error> {
        self.recheck_observing(Self::native_account)
    }
    fn recheck_observing(
        &self,
        mut sample: impl FnMut() -> Result<AccountKey, Error>,
    ) -> Result<(), Error> {
        self.account.matches(&sample()?)?;
        let checked = self
            .observation
            .recheck(self.account.effective, &self.supplied_groups);
        self.account.matches(&sample()?)?;
        checked
    }
    pub(crate) fn observation(&self) -> Result<&RootObservation, Error> {
        self.recheck()?;
        Ok(&self.observation)
    }
    // This is OS-observed UID plus SUPPLIED groups, not admitted invocation grants.
    pub(crate) fn supplied_actor(&self) -> (u32, &BTreeSet<u32>) {
        (self.account.effective, &self.supplied_groups)
    }
}

// Creator-side observation for owner §1a step 5, read half. It uses the
// bounded ACL capture and the attempt's one ledger, and it never creates.
use crate::initial_installation::{ActorRefusal, InitialActor, InitialInstallationAttempt};
use opensip_platform::WorkFailure;

/// Evidence B (law 458) is minted only by `InitialPlatform` (law 462 item 6).
use crate::trust::AclOmissionPremise;

/// The three fixed ancestors below H, in order. Final I is `FINAL_NAME`.
pub(super) const FIXED_ANCESTORS: [&str; 3] = ["Library", "Application Support", "OpenSIP"];
pub(super) const FINAL_NAME: &str = "preview-v1";

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum InstallationParent {
    /// Fixed ancestor `index` (0 `Library`, 1 `Application Support`, 2
    /// `OpenSIP`) does not exist under its retained, admitted parent.
    MissingAncestor { index: usize },
    /// All fixed ancestors exist and were admitted, and `preview-v1` was
    /// positively observed absent through the retained `OpenSIP` handle.
    FinalNameAbsent,
    /// `preview-v1` exists, as any kind of entry. It is never a pristine
    /// creation target.
    FinalNamePresent,
}

#[derive(Debug)]
pub(crate) enum ParentRefusal {
    Latched,
    WrongAttempt,
    /// The root-to-H chain could not be retained, including a symlink or a
    /// missing component.
    Open(std::io::Error),
    Capture {
        component: usize,
        error: opensip_platform::DescriptorAclCaptureError,
    },
    /// `component` counts from the filesystem root (0) through H and then
    /// the fixed ancestors.
    Ancestor {
        component: usize,
        refusal: crate::custody::Refusal,
    },
    /// The ACL was omitted and no premise admitted this descriptor.
    AncestorAclOmitted {
        component: usize,
    },
    Filesystem(std::io::Error),
    ChildOpen {
        index: usize,
        error: std::io::Error,
    },
    Private(crate::private_access::PreparePrivateError),
    Absence(std::io::Error),
    NameObservation(std::io::Error),
    /// A retained name no longer matched its descriptor.
    NameChanged,
    Actor(ActorRefusal),
}

/// Root to H retained and judged, the existing fixed ancestors retained and
/// judged, and the state of the final name. A sample, not exclusion: the
/// creator must recheck before every effect. It grants no creation.
pub(crate) struct InstallationParentObservation {
    lineage: [u8; 16],
    home: opensip_platform::RetainedDirectoryPath,
    ancestors: [Option<opensip_platform::RetainedDirectory>; 3],
    outcome: InstallationParent,
}
impl std::fmt::Debug for InstallationParentObservation {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("InstallationParentObservation")
            .field("outcome", &self.outcome)
            .finish_non_exhaustive()
    }
}
impl InstallationParentObservation {
    pub(crate) fn outcome(&self) -> InstallationParent {
        self.outcome
    }
    pub(crate) fn home(&self) -> &opensip_platform::RetainedDirectoryPath {
        &self.home
    }
    /// The retained fixed ancestor at `index`, when it exists.
    pub(crate) fn ancestor(&self, index: usize) -> Option<&opensip_platform::RetainedDirectory> {
        self.ancestors.get(index).and_then(Option::as_ref)
    }
    /// Consume the observation into its lineage, H's retained chain, the
    /// retained fixed ancestors and the final-name state (law 465 A2).
    pub(super) fn into_parts(
        self,
    ) -> (
        [u8; 16],
        opensip_platform::RetainedDirectoryPath,
        [Option<opensip_platform::RetainedDirectory>; 3],
        InstallationParent,
    ) {
        (self.lineage, self.home, self.ancestors, self.outcome)
    }
}

/// How the walk treats an existing `OpenSIP`.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(super) enum OpenSipJudgment {
    /// Law 460: `OpenSIP` must observe as private.
    Private,
    /// Law 465: retain `OpenSIP` by exact name only; the preparation judges
    /// it next, before any effect, including item 5's interrupted state.
    Retain,
}

pub(super) fn lift<E>(
    wrap: impl FnOnce(E) -> ParentRefusal,
) -> impl FnOnce(WorkFailure<E>) -> WorkFailure<ParentRefusal> {
    move |failure| match failure {
        WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
        WorkFailure::Operation(error) => WorkFailure::Operation(wrap(error)),
    }
}

/// Retain and judge root to H, then each existing fixed ancestor, then
/// observe the final name, all charged to `attempt`. Every directory from the
/// root through `Application Support` must pass the external ancestor check
/// (owner §1b); an omitted ACL passes only through `premise`. `OpenSIP` must be
/// private. Names and the actor are rechecked at the end. Any refusal latches
/// the attempt. Nothing is created.
pub(crate) fn observe_installation_parent(
    attempt: &mut InitialInstallationAttempt,
    actor: &InitialActor,
    premise: Option<&AclOmissionPremise>,
) -> Result<InstallationParentObservation, WorkFailure<ParentRefusal>> {
    observe_installation_parent_at(attempt, actor, actor.home(), premise)
}

fn observe_installation_parent_at(
    attempt: &mut InitialInstallationAttempt,
    actor: &InitialActor,
    home: &std::path::Path,
    premise: Option<&AclOmissionPremise>,
) -> Result<InstallationParentObservation, WorkFailure<ParentRefusal>> {
    if attempt.is_latched() {
        return Err(WorkFailure::Operation(ParentRefusal::Latched));
    }
    let premise_owned = premise.is_none_or(|premise| attempt.require_lineage(premise.lineage()));
    if !attempt.require_lineage(actor.lineage()) || !premise_owned {
        return Err(WorkFailure::Operation(ParentRefusal::WrongAttempt));
    }
    let uid = actor.uid();
    let lineage = attempt.lineage();
    let observed = attempt.run(|work| {
        observe_parent(lineage, home, uid, premise, OpenSipJudgment::Private, work)
    })?;
    attempt
        .recheck_actor(actor)
        .map_err(lift(ParentRefusal::Actor))?;
    Ok(observed)
}

pub(super) fn observe_parent(
    lineage: [u8; 16],
    home_path: &std::path::Path,
    uid: u32,
    premise: Option<&AclOmissionPremise>,
    opensip: OpenSipJudgment,
    work: &mut opensip_platform::WorkScope<'_>,
) -> Result<InstallationParentObservation, WorkFailure<ParentRefusal>> {
    use std::ffi::OsStr;
    let home = opensip_platform::RetainedDirectoryPath::open_accounted(
        home_path,
        MAX_COMPONENTS - SUFFIX.len(),
        work,
    )
    .map_err(lift(ParentRefusal::Open))?;
    home.visit_directories(|component, directory| {
        judge_ancestor(component, directory.as_file(), uid, premise, work)
    })?;
    let chain = home.component_count() + 1;
    let mut ancestors: [Option<opensip_platform::RetainedDirectory>; 3] = [None, None, None];
    let mut outcome = None;
    for (index, name) in FIXED_ANCESTORS.iter().enumerate() {
        let parent = match index {
            0 => home.directory(),
            _ => ancestors[index - 1]
                .as_ref()
                .expect("previous fixed ancestor retained"),
        };
        let Some(child) = parent
            .open_child_directory_if_present_accounted(OsStr::new(name), work)
            .map_err(lift(|error| ParentRefusal::ChildOpen { index, error }))?
        else {
            outcome = Some(InstallationParent::MissingAncestor { index });
            break;
        };
        require_name(&child, name, work)?;
        if index < 2 {
            judge_ancestor(chain + index, child.as_file(), uid, premise, work)?;
        } else if opensip == OpenSipJudgment::Private {
            crate::private_access::observe_private_directory(child.as_file(), uid, work)
                .map_err(lift(ParentRefusal::Private))?;
        }
        ancestors[index] = Some(child);
    }
    let outcome = match outcome {
        Some(outcome) => outcome,
        None => {
            let opensip = ancestors[2].as_ref().expect("OpenSIP retained");
            if opensip
                .observe_child_absent_accounted(OsStr::new(FINAL_NAME), work)
                .map_err(lift(ParentRefusal::Absence))?
            {
                InstallationParent::FinalNameAbsent
            } else {
                InstallationParent::FinalNamePresent
            }
        }
    };
    for (index, ancestor) in ancestors.iter().enumerate() {
        if let Some(ancestor) = ancestor {
            require_name(ancestor, FIXED_ANCESTORS[index], work)?;
        }
    }
    if !home
        .recheck_exact_names_accounted(work)
        .map_err(lift(ParentRefusal::NameObservation))?
    {
        return Err(WorkFailure::Operation(ParentRefusal::NameChanged));
    }
    Ok(InstallationParentObservation {
        lineage,
        home,
        ancestors,
        outcome,
    })
}

pub(super) fn require_name(
    directory: &opensip_platform::RetainedDirectory,
    name: &str,
    work: &mut opensip_platform::WorkScope<'_>,
) -> Result<(), WorkFailure<ParentRefusal>> {
    if opensip_platform::descriptor_name_matches_accounted(
        directory.as_file(),
        std::ffi::OsStr::new(name),
        work,
    )
    .map_err(lift(ParentRefusal::NameObservation))?
    {
        Ok(())
    } else {
        Err(WorkFailure::Operation(ParentRefusal::NameChanged))
    }
}

#[cfg(test)]
thread_local! {
    /// F5, test builds only: the walk component of every capture that
    /// `judge_ancestor` refused on this thread because the directory changed
    /// while it was sampled (`DescriptorAclCaptureError::Changed`). The rows
    /// that refusal reaches drop the component; the test classifier
    /// `installation_read_fixture::churned` drains this. Nothing else reads it.
    pub(crate) static CHANGED_CAPTURES: std::cell::RefCell<Vec<usize>> =
        const { std::cell::RefCell::new(Vec::new()) };
}

/// Capture once and judge with `check_external_ancestor`. An omitted ACL is
/// judged as a present empty ACL only when the premise admits this descriptor.
pub(super) fn judge_ancestor(
    component: usize,
    directory: &std::fs::File,
    uid: u32,
    premise: Option<&AclOmissionPremise>,
    work: &mut opensip_platform::WorkScope<'_>,
) -> Result<(), WorkFailure<ParentRefusal>> {
    let sample = opensip_platform::capture_descriptor_acl_accounted(directory, work)
        .map_err(lift(|error| {
            #[cfg(test)]
            if matches!(error, opensip_platform::DescriptorAclCaptureError::Changed) {
                CHANGED_CAPTURES.with_borrow_mut(|changed| changed.push(component));
            }
            ParentRefusal::Capture { component, error }
        }))?;
    judge_captured_ancestor(component, &sample, uid, premise.is_some(), || {
        premise.map_or(Ok(false), |premise| premise.admits(directory, work))
    })
}

/// The external ancestor judgment of one capture (owner §1b, law 458 §5).
/// `admit_omitted` runs only for an omitted ACL when a premise exists, and
/// must be the premise's own `fstatfs` on the captured descriptor.
pub(super) fn judge_captured_ancestor(
    component: usize,
    sample: &opensip_platform::DescriptorAclCapture,
    uid: u32,
    has_premise: bool,
    admit_omitted: impl FnOnce() -> Result<bool, WorkFailure<ParentRefusal>>,
) -> Result<(), WorkFailure<ParentRefusal>> {
    use opensip_platform::CapturedAclState;
    let judged = crate::custody::check_external_ancestor(
        sample.metadata(),
        sample.acl_state(),
        |index| sample.entry(index),
        uid,
    );
    match judged {
        Err(crate::custody::Refusal::AclUnreadable)
            if sample.acl_state() == CapturedAclState::NotReturned =>
        {
            if !has_premise || !admit_omitted()? {
                return Err(WorkFailure::Operation(ParentRefusal::AncestorAclOmitted {
                    component,
                }));
            }
            crate::custody::check_external_ancestor(
                sample.metadata(),
                CapturedAclState::Entries(0),
                |_| None,
                uid,
            )
            .map_err(|refusal| {
                WorkFailure::Operation(ParentRefusal::Ancestor { component, refusal })
            })
        }
        Err(refusal) => Err(WorkFailure::Operation(ParentRefusal::Ancestor {
            component,
            refusal,
        })),
        Ok(()) => Ok(()),
    }
}

#[cfg(test)]
impl NativeInstallationRoot {
    /// Synthetic path-selection bypass for native-fence sequencing tests ONLY.
    /// Account snapshots and filesystem descriptors remain actual, but this is
    /// expressly not evidence of native account-home-to-I selection.
    pub(super) fn fixture_observation_at(
        home: &Path,
        groups: &BTreeSet<u32>,
    ) -> Result<Self, Error> {
        let account = Self::native_account()?;
        let observation = RootObservation::capture(home, account.effective, groups)?;
        let result = Self {
            account,
            observation,
            supplied_groups: groups.clone(),
        };
        result.recheck()?;
        Ok(result)
    }
    pub(super) fn invalidate_fixture_account(&mut self) {
        self.account.home.push("synthetic-account-change");
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::{
        fs,
        os::unix::fs::{MetadataExt, PermissionsExt, symlink},
        process::Command,
    };
    struct Fixture {
        home: PathBuf,
        uid: u32,
    }
    impl Fixture {
        fn new() -> Self {
            let id: String = opensip_platform::request_entropy()
                .unwrap()
                .iter()
                .map(|b| format!("{b:02x}"))
                .collect();
            let home =
                crate::test_scratch::acl_scratch().join(format!("opensip-installation-root351-{id}"));
            fs::create_dir(&home).unwrap();
            fs::set_permissions(&home, fs::Permissions::from_mode(0o700)).unwrap();
            let home = fs::canonicalize(home).unwrap();
            let uid = fs::metadata(&home).unwrap().uid();
            Self { home, uid }
        }
        fn at(&self, depth: usize) -> PathBuf {
            let mut p = self.home.clone();
            for c in &SUFFIX[..depth] {
                p.push(c);
            }
            p
        }
        fn create(&self, depth: usize) {
            for n in 1..=depth {
                fs::create_dir(self.at(n)).unwrap();
                fs::set_permissions(self.at(n), fs::Permissions::from_mode(0o700)).unwrap();
            }
        }
        fn capture(&self) -> Result<RootObservation, Error> {
            RootObservation::capture(&self.home, self.uid, &BTreeSet::new())
        }
    }
    impl Drop for Fixture {
        fn drop(&mut self) {
            let _ = fs::remove_dir_all(&self.home);
        }
    }
    #[test]
    fn installation_root_missing_each_suffix_retains_only_existing_prefix_without_creation() {
        for depth in 0..4 {
            let f = Fixture::new();
            f.create(depth);
            let observed = f.capture().unwrap();
            let RootObservation::Missing(ref missing) = observed else {
                panic!("expected missing suffix")
            };
            assert_eq!(missing.remaining_components(), &SUFFIX[depth..]);
            assert!(missing.prefix.recheck_exact_names().unwrap());
            observed.recheck(f.uid, &BTreeSet::new()).unwrap();
            assert!(!f.at(depth + 1).exists());
            assert_eq!(fs::read_dir(f.at(depth)).unwrap().count(), 0);
            fs::create_dir(f.at(depth + 1)).unwrap();
            assert!(matches!(
                observed.recheck(f.uid, &BTreeSet::new()),
                Err(Error::Appeared)
            ));
        }
    }
    #[test]
    fn installation_root_existing_retains_actual_identity_and_refuses_later_replacement() {
        for change in ["replace", "mode", "case", "ancestor"] {
            let f = Fixture::new();
            f.create(4);
            let observed = f.capture().unwrap();
            let RootObservation::Existing(ref root) = observed else {
                panic!("expected existing")
            };
            assert!(root.retained_path().recheck_exact_names().unwrap());
            assert_eq!(
                root.retained_path()
                    .directory()
                    .observe_filesystem()
                    .unwrap()
                    .device(),
                fs::metadata(f.at(4)).unwrap().dev()
            );
            match change {
                "replace" => {
                    fs::rename(f.at(4), f.at(3).join("old")).unwrap();
                    fs::create_dir(f.at(4)).unwrap();
                }
                "mode" => fs::set_permissions(f.at(4), fs::Permissions::from_mode(0o777)).unwrap(),
                "case" => fs::rename(f.at(4), f.at(3).join("PREVIEW-V1")).unwrap(),
                "ancestor" => {
                    fs::set_permissions(f.at(1), fs::Permissions::from_mode(0o777)).unwrap()
                }
                _ => unreachable!(),
            }
            assert!(
                observed.recheck(f.uid, &BTreeSet::new()).is_err(),
                "{change}"
            );
        }
    }
    #[test]
    fn installation_root_wrong_kind_alias_symlink_and_unsafe_ancestor_never_become_absence() {
        for (depth, component) in SUFFIX.iter().enumerate() {
            for kind in ["file", "dangling", "symlink", "mode", "case"] {
                let f = Fixture::new();
                f.create(depth);
                let p = f.at(depth + 1);
                match kind {
                    "file" => fs::write(&p, b"").unwrap(),
                    "dangling" => symlink("absent", &p).unwrap(),
                    "symlink" => symlink(&f.home, &p).unwrap(),
                    "mode" => {
                        fs::create_dir(&p).unwrap();
                        fs::set_permissions(&p, fs::Permissions::from_mode(0o777)).unwrap();
                    }
                    "case" => fs::create_dir(f.at(depth).join(component.to_uppercase())).unwrap(),
                    _ => unreachable!(),
                }
                assert!(f.capture().is_err(), "{depth}/{kind}");
            }
        }
        let f = Fixture::new();
        fs::set_permissions(&f.home, fs::Permissions::from_mode(0o777)).unwrap();
        assert!(matches!(f.capture(), Err(Error::Custody(_))));
        assert!(
            RootObservation::capture(&f.home.join("no-home"), f.uid, &BTreeSet::new()).is_err()
        );
    }
    #[test]
    fn installation_root_failed_open_still_checks_parent_and_success_still_checks_child() {
        for existing in [false, true] {
            let f = Fixture::new();
            if existing {
                f.create(1);
            }
            let result = RootObservation::capture_with(&f.home, f.uid, &BTreeSet::new(), |index| {
                if index == 0 {
                    fs::set_permissions(&f.home, fs::Permissions::from_mode(0o777)).unwrap();
                }
            });
            assert!(matches!(result, Err(Error::Custody(_))));
        }
        let f = Fixture::new();
        f.create(1);
        let result = RootObservation::capture_with(&f.home, f.uid, &BTreeSet::new(), |index| {
            if index == 0 {
                fs::set_permissions(f.at(1), fs::Permissions::from_mode(0o777)).unwrap();
            }
        });
        assert!(matches!(result, Err(Error::Custody(_))));
    }
    #[test]
    fn installation_root_missing_recheck_refuses_wrong_kind_and_changed_prefix() {
        for change in ["file", "dangling", "prefix-replace", "prefix-mode"] {
            let f = Fixture::new();
            f.create(2);
            let observed = f.capture().unwrap();
            match change {
                "file" => fs::write(f.at(3), b"").unwrap(),
                "dangling" => symlink("absent", f.at(3)).unwrap(),
                "prefix-replace" => {
                    fs::rename(f.at(2), f.at(1).join("old")).unwrap();
                    fs::create_dir(f.at(2)).unwrap();
                }
                "prefix-mode" => {
                    fs::set_permissions(f.at(2), fs::Permissions::from_mode(0o777)).unwrap()
                }
                _ => unreachable!(),
            }
            assert!(
                observed.recheck(f.uid, &BTreeSet::new()).is_err(),
                "{change}"
            );
        }
    }
    #[test]
    fn installation_root_account_identity_is_exact_and_mixed_credentials_refuse() {
        let original = AccountKey {
            real: 42,
            effective: 42,
            home: PathBuf::from("/Users/person"),
        };
        for (real, effective, home) in [
            (43, 43, "/Users/person"),
            (42, 43, "/Users/person"),
            (42, 42, "/Users/other"),
            (42, 42, "/Users//person"),
        ] {
            assert!(
                original
                    .matches(&AccountKey {
                        real,
                        effective,
                        home: PathBuf::from(home)
                    })
                    .is_err()
            );
        }
        assert!(
            AccountKey {
                real: 42,
                effective: 0,
                home: PathBuf::from("/Users/person")
            }
            .check_credentials()
            .is_err()
        );
        assert!(
            original
                .matches(&AccountKey {
                    real: 42,
                    effective: 42,
                    home: PathBuf::from("/Users/person")
                })
                .is_ok()
        );
    }
    #[test]
    #[allow(clippy::disallowed_methods, reason = "M3-B r5 item 9: the root child marker, and the real HOME compared against the account-derived home, test-only")]
    fn installation_root_native_source_ignores_environment_child() {
        if std::env::var_os("OPENSIP_TEST_ROOT351_CHILD").is_none() {
            return;
        }
        let actual = AccountKey::from_native(observe_account().unwrap()).unwrap();
        assert_eq!(
            SUFFIX,
            ["Library", "Application Support", "OpenSIP", "preview-v1"]
        );
        assert!(actual.home.as_os_str() != std::env::var_os("HOME").unwrap());
        // A preexisting unsafe/absent-home installation may refuse. No state is
        // initialized and no policy failure is relabeled as an accepted absence.
        match NativeInstallationRoot::capture(&BTreeSet::new()) {
            Ok(root) => {
                actual.matches(&root.account).unwrap();
                assert_eq!(root.supplied_actor().0, actual.effective);
                assert!(root.supplied_actor().1.is_empty());
                match root.observation().unwrap() {
                    RootObservation::Existing(r) => {
                        let expected = fs::metadata(
                            actual
                                .home
                                .join("Library/Application Support/OpenSIP/preview-v1"),
                        )
                        .unwrap();
                        let got = r.retained_path().observe_directories().unwrap();
                        let leaf = &got.last().unwrap().metadata;
                        assert_eq!((leaf.device, leaf.inode), (expected.dev(), expected.ino()));
                    }
                    RootObservation::Missing(m) => {
                        assert!(!m.remaining_components().is_empty());
                        let mut expected = actual.home.clone();
                        for c in ["Library", "Application Support", "OpenSIP", "preview-v1"]
                            .iter()
                            .take(m.missing_index + 1)
                        {
                            expected.push(c);
                        }
                        assert!(m.next_path.as_os_str() == expected.as_os_str());
                    }
                }
            }
            Err(Error::Custody(_)) | Err(Error::Native(_)) => {}
            Err(other) => panic!("unexpected native source refusal: {other:?}"),
        }
    }
    #[test]
    fn installation_root_native_source_ignores_environment() {
        let f = Fixture::new();
        let result=Command::new(std::env::current_exe().unwrap()).args(["--exact","custody::installation_root::tests::installation_root_native_source_ignores_environment_child","--nocapture"]).env("OPENSIP_TEST_ROOT351_CHILD","1").env("HOME",&f.home).env("XDG_STATE_HOME",&f.home).env("USER","untrusted").env("SUDO_UID","0").output().unwrap();
        assert!(
            result.status.success(),
            "{}\n{}",
            String::from_utf8_lossy(&result.stdout),
            String::from_utf8_lossy(&result.stderr)
        );
        assert!(String::from_utf8_lossy(&result.stdout).contains("1 passed"));
        assert_eq!(fs::read_dir(&f.home).unwrap().count(), 0);
    }
    #[test]
    fn installation_root_source_rechecked_after_success_failure_and_later_consumption() {
        // The account keys in this sequencing test are explicitly synthetic;
        // actual Files/paths/ACLs remain native fixture observations.
        let f = Fixture::new();
        let key = || AccountKey {
            real: f.uid,
            effective: f.uid,
            home: f.home.clone(),
        };
        for changed_at in [1, 2, 3] {
            let mut calls = 0;
            let result = NativeInstallationRoot::capture_observing(&BTreeSet::new(), || {
                let mut k = key();
                if calls == changed_at {
                    k.home.push("changed");
                }
                calls += 1;
                Ok(k)
            });
            assert!(matches!(result, Err(Error::AccountChanged)), "{changed_at}");
            assert_eq!(calls, changed_at + 1);
        }
        let mut calls = 0;
        let native = NativeInstallationRoot::capture_observing(&BTreeSet::new(), || {
            calls += 1;
            Ok(key())
        })
        .unwrap();
        assert_eq!(calls, 4);
        for changed_at in [0, 1] {
            let mut calls = 0;
            let result = native.recheck_observing(|| {
                let mut k = key();
                if calls == changed_at {
                    k.home.push("changed");
                }
                calls += 1;
                Ok(k)
            });
            assert!(matches!(result, Err(Error::AccountChanged)));
            assert_eq!(calls, changed_at + 1);
        }
        fs::set_permissions(&f.home, fs::Permissions::from_mode(0o777)).unwrap();
        let mut calls = 0;
        assert!(matches!(
            native.recheck_observing(|| {
                calls += 1;
                Ok(key())
            }),
            Err(Error::Custody(_))
        ));
        assert_eq!(
            calls, 2,
            "failed filesystem recheck still samples account afterward"
        );
        let mut calls = 0;
        assert!(matches!(
            NativeInstallationRoot::capture_observing(&BTreeSet::new(), || {
                calls += 1;
                Ok(key())
            }),
            Err(Error::Custody(_))
        ));
        assert_eq!(
            calls, 2,
            "failed filesystem capture still samples account afterward"
        );
    }
}

#[cfg(all(test, target_os = "macos"))]
mod creator_parent_tests {
    use super::*;
    use crate::custody::installation_read_fixture::churned;
    use crate::initial_installation::{InitialActor, InitialInstallationAttempt};
    use opensip_platform::{WorkCost, WorkLedger};
    use std::os::unix::fs::PermissionsExt;
    use std::sync::atomic::AtomicBool;
    struct Scratch(std::path::PathBuf);
    impl Drop for Scratch {
        fn drop(&mut self) {
            let _ = std::process::Command::new("/bin/chmod")
                .args(["-R", "-N"])
                .arg(&self.0)
                .status();
            let _ = std::fs::remove_dir_all(&self.0);
        }
    }
    fn scratch() -> (Scratch, std::path::PathBuf) {
        let nonce = opensip_platform::request_entropy().unwrap();
        let name: String = nonce.iter().map(|b| format!("{b:02x}")).collect();
        let root = crate::test_scratch::acl_scratch().join(format!("opensip-parent460-{name}"));
        std::fs::create_dir(&root).unwrap();
        std::fs::set_permissions(&root, std::fs::Permissions::from_mode(0o700)).unwrap();
        // The walk refuses symlinks, and `/var` is one; use the real path.
        let root = std::fs::canonicalize(&root).unwrap();
        let home = root.join("home");
        directory(&home, 0o700);
        (Scratch(root), home)
    }
    fn directory(path: &std::path::Path, mode: u32) {
        std::fs::create_dir(path).unwrap();
        std::fs::set_permissions(path, std::fs::Permissions::from_mode(mode)).unwrap();
    }
    fn acl(path: &std::path::Path, entry: &str) {
        assert!(
            std::process::Command::new("/bin/chmod")
                .args(["+a", entry, path.to_str().unwrap()])
                .status()
                .unwrap()
                .success()
        );
    }
    fn private_opensip(parent: &std::path::Path, uid: u32) {
        let retained = opensip_platform::RetainedDirectory::from_retained_handle(
            std::fs::File::open(parent).unwrap(),
        )
        .unwrap();
        let mut ledger = WorkLedger::new();
        ledger
            .scope(|work| {
                crate::private_access::create_private_directory(&retained, "OpenSIP", uid, work)
            })
            .unwrap();
    }
    fn attempt() -> (InitialInstallationAttempt, InitialActor) {
        let flag = Box::leak(Box::new(AtomicBool::new(false)));
        let mut attempt = InitialInstallationAttempt::for_tests(flag, None).unwrap();
        let actor = attempt.observe_actor().unwrap();
        (attempt, actor)
    }
    const APFS: &[&[u8]] = &[b"apfs"];
    fn observe(
        home: &std::path::Path,
        premise: bool,
    ) -> Result<InstallationParent, WorkFailure<ParentRefusal>> {
        let (mut attempt, actor) = attempt();
        let premise = premise.then(|| AclOmissionPremise::for_tests(&attempt, APFS));
        let before = attempt.used();
        let result = observe_installation_parent_at(&mut attempt, &actor, home, premise.as_ref())
            .map(|observed| observed.outcome());
        assert!(attempt.used().edges > before.edges);
        assert_eq!(attempt.is_latched(), result.is_err());
        result
    }

    #[test]
    fn missing_ancestors_are_reported_in_order_and_nothing_is_created() {
        churned(|| {
            let (_scratch, home) = scratch();
            assert_eq!(
                observe(&home, true).unwrap(),
                InstallationParent::MissingAncestor { index: 0 }
            );
            directory(&home.join("Library"), 0o700);
            assert_eq!(
                observe(&home, true).unwrap(),
                InstallationParent::MissingAncestor { index: 1 }
            );
            directory(&home.join("Library/Application Support"), 0o755);
            assert_eq!(
                observe(&home, true).unwrap(),
                InstallationParent::MissingAncestor { index: 2 }
            );
            assert_eq!(
                std::fs::read_dir(home.join("Library/Application Support"))
                    .unwrap()
                    .count(),
                0
            );
        });
    }

    #[test]
    fn private_opensip_yields_a_positive_final_absence_and_any_entry_is_presence() {
        churned(|| {
            let (_scratch, home) = scratch();
            directory(&home.join("Library"), 0o700);
            acl(&home.join("Library"), "group:everyone deny delete");
            directory(&home.join("Library/Application Support"), 0o755);
            let (_attempt, actor) = attempt();
            private_opensip(&home.join("Library/Application Support"), actor.uid());
            assert_eq!(
                observe(&home, true).unwrap(),
                InstallationParent::FinalNameAbsent
            );
            let final_path = home.join("Library/Application Support/OpenSIP/preview-v1");
            std::os::unix::fs::symlink("/nonexistent-opensip-target", &final_path).unwrap();
            assert_eq!(
                observe(&home, true).unwrap(),
                InstallationParent::FinalNamePresent
            );
            std::fs::remove_file(&final_path).unwrap();
            directory(&final_path, 0o700);
            assert_eq!(
                observe(&home, true).unwrap(),
                InstallationParent::FinalNamePresent
            );
        });
    }

    #[test]
    fn omitted_ancestors_refuse_without_an_admitting_premise() {
        churned(|| {
            let (_scratch, home) = scratch();
            assert!(matches!(
                observe(&home, false),
                Err(WorkFailure::Operation(ParentRefusal::AncestorAclOmitted {
                    component: 0
                }))
            ));
            let (mut attempt, actor) = attempt();
            let other = AclOmissionPremise::for_tests(&attempt, &[b"hfs"]);
            assert!(matches!(
                observe_installation_parent_at(&mut attempt, &actor, &home, Some(&other)),
                Err(WorkFailure::Operation(ParentRefusal::AncestorAclOmitted {
                    component: 0
                }))
            ));
        });
    }

    #[test]
    fn unsafe_fixed_ancestors_refuse() {
        churned(|| {
            let (_scratch, home) = scratch();
            let library = home.join("Library");
            directory(&library, 0o700);
            acl(&library, "group:everyone allow add_file");
            let chain = home.components().count();
            assert!(matches!(
                observe(&home, true),
                Err(WorkFailure::Operation(ParentRefusal::Ancestor {
                    component,
                    refusal: crate::custody::Refusal::AclWrite,
                })) if component == chain
            ));
            let _ = std::process::Command::new("/bin/chmod")
                .args(["-N"])
                .arg(&library)
                .status();
            std::fs::remove_dir(&library).unwrap();
            std::os::unix::fs::symlink(home.parent().unwrap(), &library).unwrap();
            assert!(matches!(
                observe(&home, true),
                Err(WorkFailure::Operation(ParentRefusal::ChildOpen {
                    index: 0,
                    ..
                }))
            ));
            std::fs::remove_file(&library).unwrap();
            directory(&library, 0o700);
            directory(&library.join("Application Support"), 0o700);
            directory(&library.join("Application Support/OpenSIP"), 0o755);
            assert!(matches!(
                observe(&home, true),
                Err(WorkFailure::Operation(ParentRefusal::Private(_)))
            ));
            std::fs::set_permissions(&home, std::fs::Permissions::from_mode(0o770)).unwrap();
            assert!(matches!(
                observe(&home, true),
                Err(WorkFailure::Operation(ParentRefusal::Ancestor {
                    refusal: crate::custody::Refusal::GroupWrite,
                    ..
                }))
            ));
        });
    }

    #[test]
    fn wrong_attempt_and_unpaid_walk_refuse_and_latch() {
        let (_scratch, home) = scratch();
        let (_first, actor) = attempt();
        let flag = AtomicBool::new(false);
        let mut other = InitialInstallationAttempt::for_tests(&flag, None).unwrap();
        let before = other.used();
        assert!(matches!(
            observe_installation_parent_at(&mut other, &actor, &home, None),
            Err(WorkFailure::Operation(ParentRefusal::WrongAttempt))
        ));
        assert_eq!(other.used(), before);
        assert!(other.is_latched());

        let flag = AtomicBool::new(false);
        let open = opensip_platform::retained_path_open_cost(&home);
        let lineage = WorkCost {
            objects: 0,
            edges: 1,
            bytes: 16,
        };
        let limits = lineage
            .checked_add(opensip_platform::account_observation_cost())
            .unwrap()
            .checked_add(WorkCost {
                objects: open.objects,
                edges: open.edges - 1,
                bytes: open.bytes,
            })
            .unwrap();
        let mut tight = InitialInstallationAttempt::for_tests(&flag, Some(limits)).unwrap();
        let actor = tight.observe_actor().unwrap();
        let premise = AclOmissionPremise::for_tests(&tight, APFS);
        assert!(matches!(
            observe_installation_parent_at(&mut tight, &actor, &home, Some(&premise)),
            Err(WorkFailure::Budget(_))
        ));
        assert!(tight.is_latched());
    }
}
