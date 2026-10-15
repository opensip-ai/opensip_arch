// Cooperative exclusive lock under a supplied retained installation path.
// The native wrapper retains OS-account/root provenance; the supplied factory
// remains conditional. Profile, invocation/group admission and scheduling are
// separate obligations. This is not trust authority or a complete admission.
use super::{
    DirectoryPathRefusal, NativeRefusal, Scope, check_descriptor_observation,
    inspect_directory_path, inspect_operational_file,
};
use opensip_platform::{
    DescriptorFilesystem, DescriptorObservationError, FileLock, LockMode, RetainedDirectory,
    RetainedDirectoryPath, descriptor_name_matches,
};
use std::{collections::BTreeSet, ffi::OsStr, io, sync::Arc};
pub(super) const CARRIER: &str = "lifecycle.fence";
#[derive(Debug)]
pub(crate) enum Error {
    Root(DirectoryPathRefusal),
    File(NativeRefusal),
    Observation(DescriptorObservationError),
    Native(io::Error),
    NameChanged,
    #[cfg(target_os = "macos")]
    Source(super::installation_root::Error),
    #[cfg(target_os = "macos")]
    RootAbsent,
    /// The read session holding I refused (law 458c item 8): a charged
    /// recheck or sample failed, and the session is latched.
    #[cfg(target_os = "macos")]
    Session(super::installation_session::SessionRefusal),
}

/// What a capture under the installation fence needs from whoever holds it:
/// the held I, the actor, a recheck of the held fence and a sample of the
/// fence carrier's filesystem. The read session (law 458c item 8) holds it
/// for production readers; the supplied fence remains for supplied-root
/// tests only. No descriptor escape, no creation and no authority.
pub(crate) trait HeldFence {
    fn directory(&self) -> &RetainedDirectory;
    fn supplied_actor(&self) -> (u32, &BTreeSet<u32>);
    fn recheck(&self) -> Result<(), Error>;
    fn observe_filesystem(&self) -> Result<DescriptorFilesystem, Error>;
}
impl HeldFence for SuppliedInstallationFence {
    fn directory(&self) -> &RetainedDirectory {
        self.root.directory()
    }
    fn supplied_actor(&self) -> (u32, &BTreeSet<u32>) {
        SuppliedInstallationFence::supplied_actor(self)
    }
    fn recheck(&self) -> Result<(), Error> {
        SuppliedInstallationFence::recheck(self)
    }
    fn observe_filesystem(&self) -> Result<DescriptorFilesystem, Error> {
        SuppliedInstallationFence::observe_filesystem(self)
    }
}
// Lock declared first: drop unlocks/closes it before releasing ancestor handles.
// No lock descriptor escape, duplicate, upgrade, implicit retry or creation.
pub(crate) struct SuppliedInstallationFence {
    lock: FileLock,
    root: Arc<RetainedDirectoryPath>,
    uid: u32,
    groups: BTreeSet<u32>,
    #[cfg(target_os = "macos")]
    native_source: Option<super::installation_root::NativeInstallationRoot>,
}
impl SuppliedInstallationFence {
    /// Exactly one nonblocking EXCLUSIVE attempt. None means native contention,
    /// never absent carrier. Five-second scheduling belongs to lifecycle.
    pub(crate) fn try_acquire(
        root: Arc<RetainedDirectoryPath>,
        uid: u32,
        groups: &BTreeSet<u32>,
    ) -> Result<Option<Self>, Error> {
        Self::try_acquire_with(root, uid, groups, || {})
    }
    fn try_acquire_with(
        root: Arc<RetainedDirectoryPath>,
        uid: u32,
        groups: &BTreeSet<u32>,
        after_lock: impl FnOnce(),
    ) -> Result<Option<Self>, Error> {
        inspect_directory_path(&root, uid, groups).map_err(Error::Root)?;
        let opened = root.directory().open_regular(CARRIER);
        inspect_directory_path(&root, uid, groups).map_err(Error::Root)?;
        let file = opened.map_err(Error::Native)?;
        inspect_operational_file(&file, uid, groups).map_err(Error::File)?;
        if !descriptor_name_matches(&file, OsStr::new(CARRIER)).map_err(Error::Native)? {
            return Err(Error::NameChanged);
        }
        let acquired = FileLock::try_acquire(file, LockMode::Exclusive);
        after_lock();
        // A failed/busy acquisition still does not bypass the root postcheck.
        inspect_directory_path(&root, uid, groups).map_err(Error::Root)?;
        let Some(lock) = acquired.map_err(Error::Native)? else {
            return Ok(None);
        };
        let held = Self {
            lock,
            root,
            uid,
            groups: groups.clone(),
            #[cfg(target_os = "macos")]
            native_source: None,
        };
        held.recheck()?;
        Ok(Some(held))
    }
    pub(crate) fn observe_filesystem(
        &self,
    ) -> Result<opensip_platform::DescriptorFilesystem, Error> {
        self.recheck()?;
        let sampled = self.lock.observe_filesystem().map_err(Error::Native)?;
        self.recheck()?;
        Ok(sampled)
    }
    pub(crate) fn root(&self) -> &RetainedDirectoryPath {
        &self.root
    }
    /// The policy retained by this guard. The native constructor supplies the
    /// observed OS UID; the supplied constructor retains conditional UID origin.
    /// Groups still require admitted invocation provenance in either case.
    pub(crate) fn supplied_actor(&self) -> (u32, &BTreeSet<u32>) {
        (self.uid, &self.groups)
    }

    /// Re-sample the exact still-locked file, relative identity and ancestors.
    /// Cooperative exclusion requires all first-party users to share this stable
    /// carrier; samples do not defeat noncooperating trusted code or ABA.
    pub(crate) fn recheck(&self) -> Result<(), Error> {
        self.recheck_with(|| {})
    }
    fn recheck_with(&self, after_held: impl FnOnce()) -> Result<(), Error> {
        #[cfg(target_os = "macos")]
        if let Some(source) = &self.native_source {
            source.recheck().map_err(Error::Source)?;
        }
        let checked = self.recheck_held();
        after_held();
        #[cfg(target_os = "macos")]
        if let Some(source) = &self.native_source {
            source.recheck().map_err(Error::Source)?;
        }
        checked
    }
    fn recheck_held(&self) -> Result<(), Error> {
        inspect_directory_path(&self.root, self.uid, &self.groups).map_err(Error::Root)?;
        let held = self.lock.observe_descriptor().map_err(Error::Observation)?;
        check_descriptor_observation(&held, Scope::OperationalFile, self.uid, &self.groups, false)
            .map_err(|e| Error::File(NativeRefusal::Predicate(e)))?;
        if !self
            .lock
            .name_matches(OsStr::new(CARRIER))
            .map_err(Error::Native)?
        {
            return Err(Error::NameChanged);
        }
        let current = self
            .root
            .directory()
            .open_regular(CARRIER)
            .map_err(Error::Native)?;
        let current =
            inspect_operational_file(&current, self.uid, &self.groups).map_err(Error::File)?;
        if held.metadata.device != current.metadata.device
            || held.metadata.inode != current.metadata.inode
        {
            return Err(Error::NameChanged);
        }
        inspect_directory_path(&self.root, self.uid, &self.groups).map_err(Error::Root)?;
        Ok(())
    }
    pub(crate) fn release(self) -> io::Result<()> {
        self.lock.release()
    }
}
// The distinct factory/type requires native OS-account root selection. Borrowing
// its inner fence preserves source checks: they live inside the held guard and
// are repeated by every existing consumer's SuppliedInstallationFence::recheck.
#[cfg(target_os = "macos")]
pub(crate) struct NativeInstallationFence(SuppliedInstallationFence);
#[cfg(target_os = "macos")]
impl NativeInstallationFence {
    pub(crate) fn try_acquire(supplied_groups: &BTreeSet<u32>) -> Result<Option<Self>, Error> {
        let source = super::installation_root::NativeInstallationRoot::capture(supplied_groups)
            .map_err(Error::Source)?;
        Self::try_from_source(source, || {})
    }
    fn try_from_source(
        source: super::installation_root::NativeInstallationRoot,
        after_attempt: impl FnOnce(),
    ) -> Result<Option<Self>, Error> {
        source.recheck().map_err(Error::Source)?;
        let path = match source.observation().map_err(Error::Source)? {
            super::installation_root::RootObservation::Existing(root) => {
                Arc::clone(root.retained_path())
            }
            super::installation_root::RootObservation::Missing(_) => return Err(Error::RootAbsent),
        };
        let (uid, groups) = source.supplied_actor();
        let attempted = SuppliedInstallationFence::try_acquire(path, uid, groups);
        after_attempt();
        source.recheck().map_err(Error::Source)?;
        let Some(mut held) = attempted? else {
            return Ok(None);
        };
        held.native_source = Some(source);
        held.recheck()?;
        Ok(Some(Self(held)))
    }
    // SYNTHETIC test-only home selection; production factory remains OS-only.
    #[cfg(test)]
    pub(crate) fn fixture_at(home: &std::path::Path) -> Result<Self, Error> {
        let source = super::installation_root::NativeInstallationRoot::fixture_observation_at(
            home,
            &BTreeSet::new(),
        )
        .map_err(Error::Source)?;
        Self::try_from_source(source, || {})?.ok_or_else(|| {
            Error::Native(io::Error::new(
                io::ErrorKind::WouldBlock,
                "fixture fence busy",
            ))
        })
    }
    pub(crate) fn as_supplied(&self) -> &SuppliedInstallationFence {
        &self.0
    }
    pub(crate) fn recheck(&self) -> Result<(), Error> {
        self.0.recheck()
    }
    pub(crate) fn release(self) -> io::Result<()> {
        self.0.release()
    }
}
#[cfg(all(test, target_os = "macos"))]
mod tests {
    use super::*;
    use std::{
        fs::{self, File, Permissions},
        os::unix::fs::{MetadataExt, PermissionsExt, symlink},
        path::PathBuf,
        process::Command,
    };
    struct Fixture {
        root: PathBuf,
        path: Arc<RetainedDirectoryPath>,
        uid: u32,
    }
    impl Fixture {
        fn new() -> Self {
            let id: String = opensip_platform::request_entropy()
                .unwrap()
                .iter()
                .map(|b| format!("{b:02x}"))
                .collect();
            let root =
                crate::test_scratch::acl_scratch().join(format!("opensip-installation-fence-{id}"));
            fs::create_dir(&root).unwrap();
            fs::set_permissions(&root, Permissions::from_mode(0o700)).unwrap();
            let root = fs::canonicalize(root).unwrap();
            let uid = fs::metadata(&root).unwrap().uid();
            fs::write(root.join(CARRIER), b"").unwrap();
            fs::set_permissions(root.join(CARRIER), Permissions::from_mode(0o600)).unwrap();
            let path = Arc::new(RetainedDirectoryPath::open(&root, 128).unwrap());
            Self { root, path, uid }
        }
        fn acquire(&self) -> Result<Option<SuppliedInstallationFence>, Error> {
            SuppliedInstallationFence::try_acquire(
                Arc::clone(&self.path),
                self.uid,
                &BTreeSet::new(),
            )
        }
        fn child(&self, busy: bool) {
            let r = Command::new(std::env::current_exe().unwrap())
                .args([
                    "--exact",
                    "custody::installation_fence::tests::installation_fence_child_probe",
                    "--nocapture",
                ])
                .env("OPENSIP_TEST_FENCE341_CARRIER", self.root.join(CARRIER))
                .env(
                    "OPENSIP_TEST_FENCE341_BUSY",
                    if busy { "yes" } else { "no" },
                )
                .output()
                .unwrap();
            assert!(
                r.status.success(),
                "{}\n{}",
                String::from_utf8_lossy(&r.stdout),
                String::from_utf8_lossy(&r.stderr)
            );
            assert!(String::from_utf8_lossy(&r.stdout).contains("1 passed"));
        }
    }
    impl Drop for Fixture {
        fn drop(&mut self) {
            let _ = fs::remove_dir_all(&self.root);
        }
    }
    #[test]
    #[allow(
        clippy::disallowed_methods,
        reason = "M3-B r5 item 9: the fence child markers, a re-executed child, test-only"
    )]
    fn installation_fence_child_probe() {
        let Some(path) = std::env::var_os("OPENSIP_TEST_FENCE341_CARRIER") else {
            return;
        };
        let got = FileLock::try_acquire(File::open(path).unwrap(), LockMode::Shared).unwrap();
        assert_eq!(
            got.is_none(),
            std::env::var("OPENSIP_TEST_FENCE341_BUSY").unwrap() == "yes"
        );
    }
    #[test]
    fn installation_fence_native_excludes_another_process_until_release_or_drop() {
        let f = Fixture::new();
        let guard = f.acquire().unwrap().unwrap();
        guard.recheck().unwrap();
        assert!(guard.root().recheck_exact_names().unwrap());
        f.child(true);
        assert!(f.acquire().unwrap().is_none());
        guard.release().unwrap();
        f.child(false);
        let guard = f.acquire().unwrap().unwrap();
        f.child(true);
        drop(guard);
        f.child(false);
        assert!(fs::read(f.root.join(CARRIER)).unwrap().is_empty());
    }
    #[test]
    fn installation_fence_missing_wrong_kind_and_unsafe_carrier_never_become_busy() {
        for kind in ["absent", "symlink", "directory", "mode", "hardlink", "case"] {
            let f = Fixture::new();
            let file = f.root.join(CARRIER);
            match kind {
                "absent" => fs::remove_file(&file).unwrap(),
                "symlink" => {
                    fs::remove_file(&file).unwrap();
                    symlink("missing", &file).unwrap();
                }
                "directory" => {
                    fs::remove_file(&file).unwrap();
                    fs::create_dir(&file).unwrap();
                }
                "mode" => fs::set_permissions(&file, Permissions::from_mode(0o666)).unwrap(),
                "hardlink" => fs::hard_link(&file, f.root.join("other")).unwrap(),
                "case" => fs::rename(&file, f.root.join("LIFECYCLE.FENCE")).unwrap(),
                _ => unreachable!(),
            }
            assert!(f.acquire().is_err(), "{kind}");
        }
    }
    #[test]
    fn installation_fence_post_acquisition_replacement_refuses_and_releases_original() {
        let f = Fixture::new();
        let old = f.root.join("original");
        let result = SuppliedInstallationFence::try_acquire_with(
            Arc::clone(&f.path),
            f.uid,
            &BTreeSet::new(),
            || {
                fs::rename(f.root.join(CARRIER), &old).unwrap();
                fs::write(f.root.join(CARRIER), b"").unwrap();
                fs::set_permissions(f.root.join(CARRIER), Permissions::from_mode(0o600)).unwrap();
            },
        );
        assert!(matches!(result, Err(Error::NameChanged)));
        assert!(
            FileLock::try_acquire(File::open(old).unwrap(), LockMode::Exclusive)
                .unwrap()
                .is_some()
        );
        f.child(false);
    }
    #[test]
    fn installation_fence_recheck_samples_actual_locked_file_and_root() {
        for change in ["mode", "case", "same-name-other-parent", "root"] {
            let f = Fixture::new();
            let guard = f.acquire().unwrap().unwrap();
            let file = f.root.join(CARRIER);
            match change {
                "mode" => fs::set_permissions(&file, Permissions::from_mode(0o666)).unwrap(),
                "case" => fs::rename(&file, f.root.join("LIFECYCLE.FENCE")).unwrap(),
                "same-name-other-parent" => {
                    fs::create_dir(f.root.join("old")).unwrap();
                    fs::rename(&file, f.root.join("old").join(CARRIER)).unwrap();
                    fs::write(&file, b"").unwrap();
                    fs::set_permissions(&file, Permissions::from_mode(0o600)).unwrap();
                }
                "root" => fs::set_permissions(&f.root, Permissions::from_mode(0o777)).unwrap(),
                _ => unreachable!(),
            }
            assert!(guard.recheck().is_err(), "{change}");
        }
    }
    #[test]
    fn installation_fence_busy_path_still_checks_changed_root() {
        let f = Fixture::new();
        let _held = f.acquire().unwrap().unwrap();
        let result = SuppliedInstallationFence::try_acquire_with(
            Arc::clone(&f.path),
            f.uid,
            &BTreeSet::new(),
            || {
                fs::set_permissions(&f.root, Permissions::from_mode(0o777)).unwrap();
            },
        );
        assert!(matches!(result, Err(Error::Root(_))));
    }
    struct NativeFixture {
        home: Fixture,
        root: PathBuf,
    }
    impl NativeFixture {
        fn new() -> Self {
            let home = Fixture::new();
            let mut root = home.root.clone();
            for c in ["Library", "Application Support", "OpenSIP", "preview-v1"] {
                root.push(c);
                fs::create_dir(&root).unwrap();
                fs::set_permissions(&root, Permissions::from_mode(0o700)).unwrap();
            }
            fs::write(root.join(CARRIER), b"").unwrap();
            fs::set_permissions(root.join(CARRIER), Permissions::from_mode(0o600)).unwrap();
            Self { home, root }
        }
        fn source(&self) -> super::super::installation_root::NativeInstallationRoot {
            super::super::installation_root::NativeInstallationRoot::fixture_observation_at(
                &self.home.root,
                &BTreeSet::new(),
            )
            .unwrap()
        }
        fn acquire(&self) -> Result<Option<NativeInstallationFence>, Error> {
            NativeInstallationFence::try_from_source(self.source(), || {})
        }
        fn probe_shared(&self) -> bool {
            FileLock::try_acquire(
                File::open(self.root.join(CARRIER)).unwrap(),
                LockMode::Shared,
            )
            .unwrap()
            .is_some()
        }
    }
    #[test]
    fn native_installation_fence_retains_source_and_actual_exclusion_through_inner_borrow() {
        let f = NativeFixture::new();
        let held = f.acquire().unwrap().unwrap();
        assert!(!f.probe_shared());
        assert!(f.acquire().unwrap().is_none());
        assert!(held.0.native_source.is_some());
        held.recheck().unwrap();
        held.as_supplied().recheck().unwrap();
        held.as_supplied().observe_filesystem().unwrap();
        assert!(held.as_supplied().root().recheck_exact_names().unwrap());
        assert_eq!(held.as_supplied().supplied_actor().0, f.home.uid);
        held.release().unwrap();
        assert!(f.probe_shared());
        let held = f.acquire().unwrap().unwrap();
        drop(held);
        assert!(f.probe_shared());
    }
    #[test]
    fn native_installation_fence_missing_root_and_carrier_never_become_busy_or_creation() {
        let f = NativeFixture::new();
        fs::remove_file(f.root.join(CARRIER)).unwrap();
        assert!(matches!(f.acquire(),Err(Error::Native(e))if e.kind()==io::ErrorKind::NotFound));
        fs::remove_dir(&f.root).unwrap();
        assert!(matches!(f.acquire(), Err(Error::RootAbsent)));
        assert!(!f.root.exists());
    }
    #[test]
    fn native_installation_fence_all_attempt_results_recheck_native_source_before_return() {
        for outcome in ["acquired", "busy", "failed"] {
            let f = NativeFixture::new();
            let _busy = if outcome == "busy" {
                Some(f.acquire().unwrap().unwrap())
            } else {
                None
            };
            if outcome == "failed" {
                fs::remove_file(f.root.join(CARRIER)).unwrap();
            }
            let source = f.source();
            let result = NativeInstallationFence::try_from_source(source, || {
                fs::set_permissions(&f.home.root, Permissions::from_mode(0o777)).unwrap();
            });
            assert!(matches!(result, Err(Error::Source(_))), "{outcome}");
            if outcome == "acquired" {
                assert!(f.probe_shared());
            }
        }
    }
    #[test]
    fn native_installation_fence_inner_consumers_refuse_changed_account_and_custody() {
        for change in ["account", "mode", "root", "carrier-replaced"] {
            let f = NativeFixture::new();
            let mut held = f.acquire().unwrap().unwrap();
            match change {
                "account" => held
                    .0
                    .native_source
                    .as_mut()
                    .unwrap()
                    .invalidate_fixture_account(),
                "mode" => fs::set_permissions(f.root.join(CARRIER), Permissions::from_mode(0o666))
                    .unwrap(),
                "root" => fs::set_permissions(&f.home.root, Permissions::from_mode(0o777)).unwrap(),
                "carrier-replaced" => {
                    fs::rename(f.root.join(CARRIER), f.root.join("old")).unwrap();
                    fs::write(f.root.join(CARRIER), b"").unwrap();
                }
                _ => unreachable!(),
            }
            assert!(held.as_supplied().recheck().is_err(), "{change}");
            assert!(held.as_supplied().observe_filesystem().is_err(), "{change}");
            if change == "account" {
                assert!(matches!(
                    held.recheck(),
                    Err(Error::Source(
                        super::super::installation_root::Error::AccountChanged
                    ))
                ));
            }
        }
    }
    #[test]
    fn native_installation_fence_actual_factory_is_read_only() {
        // No fixture path goes through this constructor. Actual I may be absent,
        // unsafe or busy: each has a distinct honest outcome, no initialization.
        match NativeInstallationFence::try_acquire(&BTreeSet::new()) {
            Ok(Some(held)) => {
                held.recheck().unwrap();
                held.release().unwrap();
            }
            Ok(None)
            | Err(Error::RootAbsent)
            | Err(Error::Native(_))
            | Err(Error::Source(_))
            | Err(Error::Root(_))
            | Err(Error::File(_))
            | Err(Error::Observation(_))
            | Err(Error::NameChanged)
            | Err(Error::Session(_)) => {}
        }
    }
    #[test]
    fn native_installation_fence_source_postcheck_covers_success_and_failed_held_check() {
        for bad_file in [false, true] {
            let f = NativeFixture::new();
            let held = f.acquire().unwrap().unwrap();
            if bad_file {
                fs::set_permissions(f.root.join(CARRIER), Permissions::from_mode(0o666)).unwrap();
            }
            let checked = held.0.recheck_with(|| {
                fs::set_permissions(&f.home.root, Permissions::from_mode(0o777)).unwrap();
            });
            assert!(matches!(checked, Err(Error::Source(_))), "{bad_file}");
        }
    }
}
