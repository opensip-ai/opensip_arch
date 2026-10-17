//! Private security groundwork. No operational grant, custody or commit authority.
#![forbid(unsafe_code)]

// Law X9 r1 item 2, guard 1: the crash barrier never reaches a build without
// debug assertions, so a release-profile build with the feature fails here.
#[cfg(all(feature = "crash-matrix", not(debug_assertions)))]
compile_error!(
    "the crash-matrix feature is test-only (law X9 r1 item 2) and refuses every build without debug assertions"
);
#[allow(dead_code)]
mod clock_observation;
#[allow(dead_code)]
mod trust_time;

#[allow(dead_code)]
mod trust;

extern crate alloc;
mod metadata_casefold15;
mod metadata_unicode15;
#[allow(dead_code)]
mod metadata_versions;

#[allow(dead_code)]
mod custody;
/// Law X3d r6 (unit X3d-1): the security side of the commit facade. The
/// session types are exported for storage's `prepare_commit` and `publish`
/// (X3d-2) and the host; none has a public constructor but the facade's own,
/// and none is Clone, Default or serializable (law X8 r3 groups D to G).
/// `RolloverDisclosure` (law X7 r5 item 6, unit X7b) is not a session type:
/// it is the value `SessionEnd::rollover` discloses, and carries no
/// authority.
#[cfg(target_os = "macos")]
pub use custody::commit_session::{
    CarrierCapacityExhausted, CommitAdapter, CommitSession, EvidenceCommit, JournalSealBinding,
    JournalWriteTxn, RolloverDisclosure, SealOutcome, SealRefusal, SessionEnd, SessionRefusal,
    StagedCommit, StoppedSession, StoreRoot, begin_journal_txn, seal_under_append_lock,
};
/// Law X2 r8 item 7a's operation, exported because `CommitSession::open`
/// takes it (law X3d r6 item 2, unit X3d-1). Only security makes one.
#[cfg(target_os = "macos")]
pub use custody::operation_handoff::ProjectOperation;
/// Law X6 r3 items 1 to 3 (unit X6b): read-only recovery's request and its
/// admission, the custody half storage's `recover` consumes, and the public
/// view of X6a's carrier standing. No public constructor makes an
/// admission or an observation but the read entry's own.
#[cfg(target_os = "macos")]
pub use custody::recovery_admission::{
    CarrierCaptureFailure, RecoveryAdmission, RecoveryRefusal, RecoveryRequest, RequestShape,
    RequestedBinding,
};
/// Law X6 r3 item 7 (unit X6c): the custody half of the authorized
/// settlement sweep, which storage's settle write and the host's `store-gc`
/// step consume. No public constructor makes either but the sweep's own
/// entry (X1's ordinary writer admission) and its EXCLUSIVE lease.
#[cfg(target_os = "macos")]
pub use custody::settlement_sweep::{SettlementSweep, SweepLease, SweepLeaseRefusal};
#[cfg(target_os = "macos")]
pub use journal_store::{CarrierKind, CarrierObservation};

mod installation_termination;
/// Law 468 item 6: the closed public rows of creator and existing-root
/// admission refusals, for the host's D9 projection. Not authority.
pub use installation_termination::{D9Signal, InstallationTermination, RootDetail, TcbDetail};
pub use commit_authority::LatchOutcome;
#[cfg(target_os = "macos")]
pub use custody::commit_session::CancellationLatch;

/// Tests that create entries in the shared temporary directory, or walk
/// through it, run one at a time. Those walks compare directory metadata
/// before, during and after each read, so a parallel test adding a sibling
/// makes them report `ChangedDuringRead`. The first call on a test thread
/// takes one process-wide lock and keeps it until that thread exits, after the
/// test's own fixtures are dropped. Calls on the same thread reuse the lock.
#[cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))]
#[cfg_attr(not(test), allow(dead_code, unused_imports))]
mod test_scratch {
    use std::{
        cell::RefCell,
        sync::{Mutex, MutexGuard},
    };
    static TREE: Mutex<()> = Mutex::new(());
    thread_local! {
        static HELD: RefCell<Option<MutexGuard<'static, ()>>> = const { RefCell::new(None) };
    }
    pub(crate) fn temp_dir() -> std::path::PathBuf {
        HELD.with(|held| {
            let mut held = held.borrow_mut();
            if held.is_none() {
                *held = Some(TREE.lock().unwrap_or_else(|poisoned| poisoned.into_inner()));
            }
        });
        private_dir()
    }

    static PRIVATE: std::sync::OnceLock<std::path::PathBuf> = std::sync::OnceLock::new();
    /// F3: this process's private scratch parent, `<temp>/opensip-test/<pid>-<draw>`.
    /// Test walkers compare the metadata of every ancestor of a fixture, so a
    /// fixture created directly in the shared system temp directory sees that
    /// directory change whenever any other process (another test binary, another
    /// worktree's tests) creates or removes an entry there. Keeping every fixture
    /// below one long-lived `opensip-test` directory and a per-process child
    /// confines OpenSIP's own churn: `opensip-test` changes only when a test
    /// process starts, and this process's child changes only under the `TREE`
    /// lock above. Residual churn is absorbed by `settled`.
    fn private_dir() -> std::path::PathBuf {
        PRIVATE
            .get_or_init(|| {
                use std::os::unix::fs::DirBuilderExt;
                let shared = std::env::temp_dir().join("opensip-test");
                match std::fs::DirBuilder::new().mode(0o700).create(&shared) {
                    Ok(()) => {}
                    Err(e) if e.kind() == std::io::ErrorKind::AlreadyExists => {}
                    Err(e) => panic!("opensip-test scratch parent: {e}"),
                }
                // Law X9 r2 item 3: no wall reading names it (a matrix
                // child takes none from the OS); a fresh draw does.
                let draw: String = opensip_platform::request_entropy()
                    .expect("entropy")
                    .iter()
                    .map(|b| format!("{b:02x}"))
                    .collect();
                let private = shared.join(format!("{}-{draw}", std::process::id()));
                std::fs::DirBuilder::new()
                    .mode(0o700)
                    .create(&private)
                    .unwrap_or_else(|e| panic!("private scratch parent: {e}"));
                private
            })
            .clone()
    }

    /// F3: re-run a whole test, with fresh fixtures, only when it failed because
    /// a native observation saw a directory change during its read
    /// (`ChangedDuringRead`), which shared ancestors outside the test's control
    /// cause. Every assertion stays strict, any other failure is final, and the
    /// last attempt's failure is reported.
    pub(crate) fn settled(test: impl Fn() + std::panic::RefUnwindSafe) {
        const ATTEMPTS: u32 = 8;
        for attempt in 1..=ATTEMPTS {
            match std::panic::catch_unwind(&test) {
                Ok(()) => return,
                Err(panic) => {
                    let message = panic
                        .downcast_ref::<String>()
                        .map(String::as_str)
                        .or_else(|| panic.downcast_ref::<&str>().copied())
                        .unwrap_or("");
                    if attempt == ATTEMPTS || !message.contains("ChangedDuringRead") {
                        std::panic::resume_unwind(panic);
                    }
                    std::thread::sleep(std::time::Duration::from_millis(25 * u64::from(attempt)));
                }
            }
        }
    }

    thread_local! {
        /// The identities of the real system directories above this thread's
        /// ACL scratch base (`/` through the temp directory). See `acl_scratch`.
        static ABOVE_BASE: RefCell<Vec<(u64, u64)>> = const { RefCell::new(Vec::new()) };
    }
    static BASE: std::sync::OnceLock<std::path::PathBuf> = std::sync::OnceLock::new();

    /// Law 461: an omitted ACL is unreadable. The real ancestors of the temp
    /// directory (`/`, `/private`, `/var/folders/...`) omit their ACLs on a
    /// stock Mac and a test cannot give them one, so the test-only walkers that
    /// judge a whole path from `/` (`inspect_directory_path` under the supplied
    /// fence and `NativeInstallationRoot`) refuse at `/`. A test that calls
    /// this opts its thread in: it gets a per-process scratch base whose
    /// inheritable owner entry grants no write, so every directory and file it
    /// creates below carries a present ACL, and the chain judgment skips only
    /// those real ancestors, by identity, on this thread. The judgment of the
    /// base and everything below it is unchanged. Production is unaffected.
    pub(crate) fn acl_scratch() -> std::path::PathBuf {
        use std::os::unix::fs::{DirBuilderExt, MetadataExt};
        let parent = temp_dir();
        let base = BASE
            .get_or_init(|| {
                let base = parent.join(format!("opensip-acl461-{}", std::process::id()));
                match std::fs::DirBuilder::new().mode(0o700).create(&base) {
                    Ok(()) => {}
                    Err(e) if e.kind() == std::io::ErrorKind::AlreadyExists => {}
                    Err(e) => panic!("ACL scratch base: {e}"),
                }
                let user = std::process::Command::new("/usr/bin/id")
                    .arg("-un")
                    .output()
                    .unwrap();
                let user = String::from_utf8(user.stdout).unwrap();
                // readattr is not a mutation right, so the entry and its
                // inherited copies name no ACL writer.
                let entry = format!(
                    "user:{} allow readattr,file_inherit,directory_inherit",
                    user.trim()
                );
                let _ = std::process::Command::new("/bin/chmod")
                    .args(["-N"])
                    .arg(&base)
                    .status();
                let status = std::process::Command::new("/bin/chmod")
                    .args(["+a", &entry])
                    .arg(&base)
                    .status()
                    .unwrap();
                assert!(status.success(), "ACL scratch base entry");
                base
            })
            .clone();
        // The walkers retain the canonical chain (`/private/var/...`).
        let canonical = std::fs::canonicalize(&base).unwrap();
        let mut above = Vec::new();
        let mut at = canonical.parent();
        while let Some(dir) = at {
            let m = std::fs::metadata(dir).unwrap();
            above.push((m.dev(), m.ino()));
            at = dir.parent();
        }
        ABOVE_BASE.with(|cell| *cell.borrow_mut() = above);
        base
    }

    /// Whether this thread opted in and the identity is a real ancestor of
    /// its ACL scratch base.
    pub(crate) fn above_acl_scratch(device: u64, inode: u64) -> bool {
        ABOVE_BASE.with(|cell| cell.borrow().contains(&(device, inode)))
    }
}

#[allow(dead_code)]
mod initial_installation;

// M3-B r5 item 23 (unit B3-a): the invocation's authorization records and
// S3.1's choice. No M3 consumer yet.
#[allow(dead_code)]
mod grants;

#[allow(dead_code)]
mod private_access;

// Store-data custody for storage's per-project directories and files (X3c).
#[cfg(target_os = "macos")]
mod store_custody;
#[cfg(target_os = "macos")]
pub use store_custody::{
    StoreCustodyRefusal, StoreDirectoryDisposition, StoreFileCreation,
    admit_existing_store_directory, create_or_admit_store_directory, create_store_file,
    open_store_file,
};

#[allow(dead_code)]
mod commit_authority;

#[allow(dead_code)]
mod revocation;

#[allow(dead_code)]
mod journal_store;
// Law X9 r1 item 6 (unit X9-1): the crash matrix's synthetic support
// surface, only under the test-only feature.
#[cfg(all(feature = "crash-matrix", target_os = "macos"))]
#[doc(hidden)]
pub mod crash_matrix_support;
// M3-B r7 item 14 (unit B2-c1): the shared discovery rule and the admitted
// boundary inventory, for the host's native unit instrument.
pub mod discovery_export;
// M3-C r8 items 1 and 2 (unit C1a1): the snapshot's lawful root, its
// pre-walk opener and its extent walk. Neither reads content (C1-T2).
#[cfg(target_os = "macos")]
pub mod snapshot_source;
#[cfg(target_os = "macos")]
pub mod snapshot_walk;
// Law X8 r3 item 4 (unit X8b): the refusal suite's test seam, only under the
// test-only feature that storage's and host's `[dev-dependencies]` enable.
#[cfg(all(feature = "scenario-fixtures", target_os = "macos"))]
#[doc(hidden)]
pub mod scenario;
// Unit X9-1's pin of the shared fixture-gate site list and its tests of the
// shared producers, in every test build.
#[cfg(all(test, target_os = "macos"))]
mod crash_matrix_sites;
// Law X9 r1 items 5 and 12 (unit X9-1): the census of the integrated path,
// run in matrix children.
#[cfg(all(test, feature = "crash-matrix", target_os = "macos"))]
mod crash_matrix_census;

// Workspace observation mechanism, not admitted custody or a security grant.
pub use journal_store::OperationalReadFailure as OperationalFileReadFailure;
/// Exact bytes read from the retained file. No reopen by pathname is needed for
/// a later descriptor policy check. The handle alone does not establish current
/// linkage, name binding, exclusion, local-filesystem qualification or a lease.
#[derive(Debug)]
pub struct ObservedOperationalFile {
    file: std::fs::File,
    bytes: Vec<u8>,
}
impl ObservedOperationalFile {
    /// For descriptor metadata/policy checks on the object that supplied bytes.
    /// `bytes()` is the captured evidence. Reading or seeking this shared-offset
    /// handle does not repeat the capture's checks; a later read is unbracketed.
    pub fn file(&self) -> &std::fs::File {
        &self.file
    }
    pub fn bytes(&self) -> &[u8] {
        &self.bytes
    }
    pub fn into_parts(self) -> (std::fs::File, Vec<u8>) {
        (self.file, self.bytes)
    }
}
#[derive(Debug)]
pub enum OperationalFileObservation {
    Absent,
    Present(ObservedOperationalFile),
    Unreadable(OperationalFileReadFailure),
}
/// Sample an operational file under a supplied retained directory chain. Checks
/// named identity before/after open and after the bounded read; success retains
/// that exact open descriptor alongside the bytes. Does not admit owner/ACL/local
/// filesystem policy, actor provenance or a consuming lease. Callers must apply
/// descriptor policy and retain admitted exclusion/custody through consumption;
/// success and absence remain conditional observations, not current authority.
/// No creation/repair/retry; I/O and bound failures keep their causes.
pub fn observe_bound_operational_file(
    parent: &opensip_platform::RetainedDirectoryPath,
    leaf: &str,
    max_bytes: usize,
) -> OperationalFileObservation {
    match journal_store::bound_operational::capture_bound_operational_file(parent, leaf, max_bytes)
    {
        Ok(Some((file, bytes))) => {
            OperationalFileObservation::Present(ObservedOperationalFile { file, bytes })
        }
        Ok(None) => OperationalFileObservation::Absent,
        Err(error) => OperationalFileObservation::Unreadable(error),
    }
}

/// Observe metadata and ACLs on this exact retained descriptor and apply S7 file
/// predicates. Supplied uid/groups must come from an admitted actor context; do
/// not derive the invoking uid from the file being checked. This mechanism does
/// not authenticate that context, a pathname, ancestors, filesystem or lease.
/// It samples current descriptor policy; success is neither lasting exclusion
/// nor admission of previously captured bytes. No reopen, creation or retry.
pub use custody::inspect_operational_file as inspect_operational_file_policy;
/// Workspace diagnostic causes, not public report codes or authority. The shared
/// predicate enum includes causes for other private scopes; the operational-file
/// function never applies a configuration size limit or owner waiver.
pub use custody::{
    NativeRefusal as OperationalFilePolicyFailure, Refusal as CustodyPredicateFailure,
};

/// Full retained-directory observation causes. These are workspace diagnostics,
/// not public report codes, and include both failed reads and predicate failures.
pub use custody::DirectoryPathRefusal as DirectoryPathPolicyFailure;
#[derive(Debug)]
pub enum PolicyCaptureFailure {
    Directory(DirectoryPathPolicyFailure),
    Read(OperationalFileReadFailure),
    File(OperationalFilePolicyFailure),
}
/// Exact captured bytes plus the file-policy sample performed after that read.
/// It does not establish file policy DURING the read; only caller-held exclusion
/// can provide that guarantee. Directory samples are checked and discarded, not
/// retained in this value. This is historical evidence, not a lease or grant.
#[derive(Debug)]
pub struct PolicyObservedOperationalFile {
    captured: ObservedOperationalFile,
    descriptor: opensip_platform::DescriptorObservation,
}
impl PolicyObservedOperationalFile {
    pub fn captured(&self) -> &ObservedOperationalFile {
        &self.captured
    }
    pub fn descriptor(&self) -> &opensip_platform::DescriptorObservation {
        &self.descriptor
    }
}
#[derive(Debug)]
pub enum PolicyOperationalFileObservation {
    Absent,
    Present(PolicyObservedOperationalFile),
    Unavailable(PolicyCaptureFailure),
}
/// Sample full root-to-parent operational directory policy before and after the
/// bounded capture, and descriptor policy on the exact file that supplied bytes.
/// The final directory sample follows even a file-policy refusal. Failed directory
/// observation/policy cannot establish absence or authorize interpretation of a
/// lower-layer result. A directory failure takes precedence even if the file
/// independently failed. This never creates, repairs or retries.
///
/// UID/groups are asserted actor inputs. The caller still owes their provenance,
/// filesystem qualification, file/name joins and exclusion through consumption.
/// Samples cannot exclude ABA or a permission change between observations. This
/// is not the S3 discovery walk and has no explicit-project owner waiver.
pub fn observe_bound_operational_file_with_policy(
    parent: &opensip_platform::RetainedDirectoryPath,
    leaf: &str,
    max_bytes: usize,
    invoking_uid: u32,
    authorized_groups: &std::collections::BTreeSet<u32>,
) -> PolicyOperationalFileObservation {
    policy_capture_sequence(
        || custody::inspect_directory_path(parent, invoking_uid, authorized_groups).map(|_| ()),
        || observe_bound_operational_file(parent, leaf, max_bytes),
        |file| inspect_operational_file_policy(file, invoking_uid, authorized_groups),
    )
}
// Private sequencing seam: the public function fixes all three mechanisms.
// Test callbacks verify order/failure propagation; they are not OS qualification.
fn policy_capture_sequence(
    mut directories: impl FnMut() -> Result<(), DirectoryPathPolicyFailure>,
    read: impl FnOnce() -> OperationalFileObservation,
    inspect_file: impl FnOnce(
        &std::fs::File,
    ) -> Result<
        opensip_platform::DescriptorObservation,
        OperationalFilePolicyFailure,
    >,
) -> PolicyOperationalFileObservation {
    use PolicyOperationalFileObservation as O;
    if let Err(e) = directories() {
        return O::Unavailable(PolicyCaptureFailure::Directory(e));
    }
    let captured = read();
    if let Err(e) = directories() {
        return O::Unavailable(PolicyCaptureFailure::Directory(e));
    }
    match captured {
        OperationalFileObservation::Absent => O::Absent,
        OperationalFileObservation::Unreadable(e) => O::Unavailable(PolicyCaptureFailure::Read(e)),
        OperationalFileObservation::Present(captured) => {
            let sampled = inspect_file(captured.file());
            if let Err(e) = directories() {
                return O::Unavailable(PolicyCaptureFailure::Directory(e));
            }
            match sampled {
                Ok(descriptor) => O::Present(PolicyObservedOperationalFile {
                    captured,
                    descriptor,
                }),
                Err(e) => O::Unavailable(PolicyCaptureFailure::File(e)),
            }
        }
    }
}

#[cfg(all(test, target_os = "macos"))]
mod policy_capture_tests {
    use super::*;
    use std::{
        collections::BTreeSet,
        fs,
        os::unix::fs::{MetadataExt, PermissionsExt},
        path::Path,
    };
    #[test]
    fn policy_checked_absence_is_read_only_and_requires_full_parent_policy() {
        // Read-only root observation: no system file is created or modified.
        let root = opensip_platform::RetainedDirectoryPath::open(Path::new("/"), 0).unwrap();
        let leaf = format!(
            "opensip-absent-{}",
            opensip_identity::digest_hex(&opensip_identity::raw_sha256(
                &opensip_platform::request_entropy().unwrap()
            ))
        );
        // Law 461: the real `/` omits its ACL, so the whole-path walk refuses
        // there as unreadable, never "no writers", and absence is not reported.
        assert!(matches!(
            observe_bound_operational_file_with_policy(&root, &leaf, 128, 0, &BTreeSet::new()),
            PolicyOperationalFileObservation::Unavailable(PolicyCaptureFailure::Directory(
                DirectoryPathPolicyFailure::Predicate {
                    component: 0,
                    refusal: CustodyPredicateFailure::AclUnreadable
                }
            ))
        ));
        assert!(!Path::new("/").join(&leaf).exists());
        // Below an ACL-carrying scratch base the same absence is observed.
        let base = crate::test_scratch::acl_scratch();
        let present =
            opensip_platform::RetainedDirectoryPath::open(&fs::canonicalize(&base).unwrap(), 128)
                .unwrap();
        let base_uid = fs::metadata(&base).unwrap().uid();
        assert!(matches!(
            observe_bound_operational_file_with_policy(
                &present,
                &leaf,
                128,
                base_uid,
                &BTreeSet::new()
            ),
            PolicyOperationalFileObservation::Absent
        ));
        assert!(!base.join(&leaf).exists());
        // A private absent leaf beneath a writable ancestor cannot be absence.
        let path = crate::test_scratch::acl_scratch().join(&leaf);
        fs::create_dir(&path).unwrap();
        struct Cleanup(std::path::PathBuf);
        impl Drop for Cleanup {
            fn drop(&mut self) {
                let _ = fs::remove_dir_all(&self.0);
            }
        }
        let f = Cleanup(path);
        fs::create_dir(f.0.join("private")).unwrap();
        fs::set_permissions(&f.0, fs::Permissions::from_mode(0o777)).unwrap();
        fs::set_permissions(f.0.join("private"), fs::Permissions::from_mode(0o700)).unwrap();
        let bound = opensip_platform::RetainedDirectoryPath::open(
            &fs::canonicalize(f.0.join("private")).unwrap(),
            128,
        )
        .unwrap();
        let uid = fs::metadata(&f.0).unwrap().uid();
        assert!(matches!(
            observe_bound_operational_file_with_policy(
                &bound,
                "absent",
                128,
                uid,
                &BTreeSet::new()
            ),
            PolicyOperationalFileObservation::Unavailable(PolicyCaptureFailure::Directory(_))
        ));
        assert!(!f.0.join("private/absent").exists());
    }
    #[test]
    fn policy_checked_read_retains_the_descriptor_and_exact_bytes() {
        // Law 461: an existing macOS system file under `/`, read-only, now
        // refuses at the real `/`, which omits its ACL. The test creates nothing
        // there and does not print its contents.
        let system = fs::canonicalize("/etc/hosts").unwrap();
        let system_parent =
            opensip_platform::RetainedDirectoryPath::open(system.parent().unwrap(), 128).unwrap();
        assert!(matches!(
            observe_bound_operational_file_with_policy(
                &system_parent,
                system.file_name().unwrap().to_str().unwrap(),
                4_194_304,
                0,
                &BTreeSet::new(),
            ),
            PolicyOperationalFileObservation::Unavailable(PolicyCaptureFailure::Directory(
                DirectoryPathPolicyFailure::Predicate {
                    component: 0,
                    refusal: CustodyPredicateFailure::AclUnreadable
                }
            ))
        ));
        // The retention and exact-byte behaviour, on an owned scratch file
        // below an ACL-carrying base.
        let tag = opensip_identity::digest_hex(&opensip_identity::raw_sha256(
            &opensip_platform::request_entropy().unwrap(),
        ));
        let dir = crate::test_scratch::acl_scratch().join(format!("opensip-retain461-{tag}"));
        fs::create_dir(&dir).unwrap();
        struct Cleanup(std::path::PathBuf);
        impl Drop for Cleanup {
            fn drop(&mut self) {
                let _ = fs::remove_dir_all(&self.0);
            }
        }
        let dir = Cleanup(fs::canonicalize(dir).unwrap());
        fs::set_permissions(&dir.0, fs::Permissions::from_mode(0o700)).unwrap();
        fs::write(dir.0.join("hosts"), b"retained exact bytes").unwrap();
        fs::set_permissions(dir.0.join("hosts"), fs::Permissions::from_mode(0o600)).unwrap();
        let uid = fs::metadata(&dir.0).unwrap().uid();
        let parent = opensip_platform::RetainedDirectoryPath::open(&dir.0, 128).unwrap();
        let leaf = "hosts";
        let PolicyOperationalFileObservation::Present(observed) =
            observe_bound_operational_file_with_policy(
                &parent,
                leaf,
                4_194_304,
                uid,
                &BTreeSet::new(),
            )
        else {
            panic!("expected the owned scratch file");
        };
        use std::io::Seek;
        let captured = observed.captured();
        assert_eq!(
            (&captured.file).stream_position().unwrap(),
            captured.bytes().len() as u64
        );
        let metadata = captured.file().metadata().unwrap();
        assert_eq!(
            (
                observed.descriptor().metadata.device,
                observed.descriptor().metadata.inode
            ),
            (metadata.dev(), metadata.ino())
        );
        assert_eq!(captured.bytes(), b"retained exact bytes");
        assert!(matches!(
            observe_bound_operational_file_with_policy(&parent, leaf, 1, uid, &BTreeSet::new()),
            PolicyOperationalFileObservation::Unavailable(PolicyCaptureFailure::Read(
                OperationalFileReadFailure::Bound
            ))
        ));
    }
    #[test]
    fn policy_sequence_checks_directories_before_read_and_after_absence_or_error() {
        use std::cell::{Cell, RefCell};
        for fail_at in [0, 1, 2] {
            for absent in [false, true] {
                let count = Cell::new(0);
                let steps = RefCell::new(Vec::new());
                let observed = policy_capture_sequence(
                    || {
                        steps.borrow_mut().push("directory");
                        count.set(count.get() + 1);
                        if count.get() == fail_at {
                            Err(DirectoryPathPolicyFailure::NameChanged)
                        } else {
                            Ok(())
                        }
                    },
                    || {
                        steps.borrow_mut().push("read");
                        if absent {
                            OperationalFileObservation::Absent
                        } else {
                            OperationalFileObservation::Unreadable(
                                OperationalFileReadFailure::Bound,
                            )
                        }
                    },
                    |_| panic!("no descriptor after absent or failed read"),
                );
                if fail_at != 0 {
                    assert!(matches!(
                        observed,
                        PolicyOperationalFileObservation::Unavailable(
                            PolicyCaptureFailure::Directory(
                                DirectoryPathPolicyFailure::NameChanged
                            )
                        )
                    ));
                } else if absent {
                    assert!(matches!(observed, PolicyOperationalFileObservation::Absent));
                } else {
                    assert!(matches!(
                        observed,
                        PolicyOperationalFileObservation::Unavailable(PolicyCaptureFailure::Read(
                            OperationalFileReadFailure::Bound
                        ))
                    ));
                }
                assert_eq!(
                    *steps.borrow(),
                    if fail_at == 1 {
                        vec!["directory"]
                    } else {
                        vec!["directory", "read", "directory"]
                    }
                );
            }
        }
    }
    #[test]
    fn policy_sequence_brackets_descriptor_refusal_and_keeps_its_cause() {
        use std::{
            cell::{Cell, RefCell},
            io::Read,
        };
        for final_directory_fails in [false, true] {
            let count = Cell::new(0);
            let steps = RefCell::new(Vec::new());
            let mut file = fs::File::open("/etc/hosts").unwrap();
            let mut bytes = Vec::new();
            file.read_to_end(&mut bytes).unwrap();
            let observed = policy_capture_sequence(
                || {
                    steps.borrow_mut().push("directory");
                    count.set(count.get() + 1);
                    if final_directory_fails && count.get() == 3 {
                        Err(DirectoryPathPolicyFailure::NameChanged)
                    } else {
                        Ok(())
                    }
                },
                || {
                    steps.borrow_mut().push("read");
                    OperationalFileObservation::Present(ObservedOperationalFile { file, bytes })
                },
                |_| {
                    steps.borrow_mut().push("file");
                    Err(OperationalFilePolicyFailure::Predicate(
                        CustodyPredicateFailure::OthersWrite,
                    ))
                },
            );
            assert_eq!(
                *steps.borrow(),
                vec!["directory", "read", "directory", "file", "directory"]
            );
            if final_directory_fails {
                assert!(matches!(
                    observed,
                    PolicyOperationalFileObservation::Unavailable(PolicyCaptureFailure::Directory(
                        DirectoryPathPolicyFailure::NameChanged
                    ))
                ));
            } else {
                assert!(matches!(
                    observed,
                    PolicyOperationalFileObservation::Unavailable(PolicyCaptureFailure::File(
                        OperationalFilePolicyFailure::Predicate(
                            CustodyPredicateFailure::OthersWrite
                        )
                    ))
                ));
            }
        }
    }
    #[test]
    fn public_policy_wiring_checks_real_file_and_directory_permissions_and_actor() {
        // Law 461: below the account temporary directory, on an ACL-carrying
        // scratch base, since the real ancestors omit their ACLs.
        let parent = crate::test_scratch::acl_scratch();
        let tag = opensip_identity::digest_hex(&opensip_identity::raw_sha256(
            &opensip_platform::request_entropy().unwrap(),
        ));
        let path = parent.join(format!("opensip-policy216-{tag}"));
        fs::create_dir(&path).unwrap();
        struct Cleanup(std::path::PathBuf);
        impl Drop for Cleanup {
            fn drop(&mut self) {
                let _ = fs::remove_dir_all(&self.0);
            }
        }
        let f = Cleanup(fs::canonicalize(path).unwrap());
        fs::set_permissions(&f.0, fs::Permissions::from_mode(0o700)).unwrap();
        let file = f.0.join("observed");
        fs::write(&file, b"owned policy data").unwrap();
        fs::set_permissions(&file, fs::Permissions::from_mode(0o600)).unwrap();
        let metadata = fs::metadata(&file).unwrap();
        let uid = metadata.uid();
        let gid = metadata.gid();
        assert_ne!(uid, 0);
        // Fixture uid/gid only; production actor inputs have separate provenance.
        let bound = opensip_platform::RetainedDirectoryPath::open(&f.0, 128).unwrap();
        let groups = BTreeSet::new();
        let observe = |uid, groups: &BTreeSet<u32>| {
            observe_bound_operational_file_with_policy(&bound, "observed", 128, uid, groups)
        };
        let PolicyOperationalFileObservation::Present(captured) = observe(uid, &groups) else {
            panic!("owned protected file must pass");
        };
        assert_eq!(captured.captured().bytes(), b"owned policy data");
        assert!(matches!(
            observe(uid.checked_add(1).unwrap(), &groups),
            PolicyOperationalFileObservation::Unavailable(PolicyCaptureFailure::Directory(
                DirectoryPathPolicyFailure::Predicate {
                    refusal: CustodyPredicateFailure::ForeignOwner,
                    ..
                }
            ))
        ));
        fs::set_permissions(&file, fs::Permissions::from_mode(0o602)).unwrap();
        assert!(matches!(
            observe(uid, &groups),
            PolicyOperationalFileObservation::Unavailable(PolicyCaptureFailure::File(
                OperationalFilePolicyFailure::Predicate(CustodyPredicateFailure::OthersWrite)
            ))
        ));
        fs::set_permissions(&file, fs::Permissions::from_mode(0o620)).unwrap();
        assert!(matches!(
            observe(uid, &groups),
            PolicyOperationalFileObservation::Unavailable(PolicyCaptureFailure::File(
                OperationalFilePolicyFailure::Predicate(CustodyPredicateFailure::GroupWrite)
            ))
        ));
        assert!(matches!(
            observe(uid, &BTreeSet::from([gid])),
            PolicyOperationalFileObservation::Present(_)
        ));
        fs::set_permissions(&file, fs::Permissions::from_mode(0o600)).unwrap();
        let directory_gid = fs::metadata(&f.0).unwrap().gid();
        fs::set_permissions(&f.0, fs::Permissions::from_mode(0o770)).unwrap();
        assert!(matches!(
            observe(uid, &groups),
            PolicyOperationalFileObservation::Unavailable(PolicyCaptureFailure::Directory(
                DirectoryPathPolicyFailure::Predicate {
                    refusal: CustodyPredicateFailure::GroupWrite,
                    ..
                }
            ))
        ));
        assert!(matches!(
            observe(uid, &BTreeSet::from([directory_gid])),
            PolicyOperationalFileObservation::Present(_)
        ));
        fs::set_permissions(&f.0, fs::Permissions::from_mode(0o700)).unwrap();
        assert!(matches!(
            observe_bound_operational_file_with_policy(&bound, "absent", 128, uid, &groups),
            PolicyOperationalFileObservation::Absent
        ));
    }
}

#[cfg(target_os = "macos")]
pub mod installation_observation;

/// Law X3a r5 item 4 (unit X3a-2): the read session's selected store
/// endpoint, lent to the installation readers. Not authority.
#[cfg(target_os = "macos")]
pub mod installation_endpoint;

/// Law 458c r6 items 7 and 12: doctor's installation check, for the host's
/// doctor report.
#[cfg(target_os = "macos")]
pub use custody::installation_doctor::{
    DoctorInstallation, InstallationFinding, observe_installation_for_doctor,
};

#[cfg(target_os = "macos")]
pub use trust::{NativeTrustReadError, NativeTrustReadSession, ProvisionalSuccessorCounts};

// M3-C r8 item 3 (unit C1c-0): the pruned-tree opener for C2's layout reads
// and the read set's authorization and Cargo-marker primitives. It reads no
// content (C1-T2).
#[cfg(target_os = "macos")]
pub mod snapshot_read_set;
