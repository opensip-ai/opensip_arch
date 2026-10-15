// Law X2 r5 items 1 to 3 (unit X2a), on scratch homes only. The scratch H
// sits under the per-user temp directory, whose real ancestors (`/`,
// `/private`, `/var/folders/...`) omit their ACLs on a stock Mac; the test
// premise (apfs) admits them exactly as a qualified row would. Nothing here
// judges the real home's project folders.
use super::*;
use crate::custody::installation_read_fixture::churned;
use crate::initial_installation::InitialInstallationAttempt;
use opensip_platform::{WorkBudgetError, WorkLedger};
use std::os::unix::fs::MetadataExt;
use std::fs;
use std::os::unix::fs::PermissionsExt;
use std::sync::atomic::AtomicBool;

struct Scratch(PathBuf);
impl Drop for Scratch {
    fn drop(&mut self) {
        let _ = std::process::Command::new("/bin/chmod")
            .args(["-R", "-N"])
            .arg(&self.0)
            .status();
        let _ = fs::remove_dir_all(&self.0);
    }
}
/// A scratch root holding a 0700 `home`, on its canonical path.
fn scratch() -> (Scratch, PathBuf) {
    let nonce: String = opensip_platform::request_entropy()
        .unwrap()
        .iter()
        .map(|b| format!("{b:02x}"))
        .collect();
    let root = crate::test_scratch::temp_dir().join(format!("opensip-x2a-{nonce}"));
    fs::create_dir(&root).unwrap();
    fs::set_permissions(&root, fs::Permissions::from_mode(0o700)).unwrap();
    let root = fs::canonicalize(&root).unwrap();
    let home = root.join("home");
    directory(&home, 0o700);
    (Scratch(root), home)
}
fn directory(path: &Path, mode: u32) {
    fs::create_dir(path).unwrap();
    fs::set_permissions(path, fs::Permissions::from_mode(mode)).unwrap();
}
fn chmod(path: &Path, mode: u32) {
    fs::set_permissions(path, fs::Permissions::from_mode(mode)).unwrap();
}
fn acl(path: &Path, entry: &str) {
    assert!(
        std::process::Command::new("/bin/chmod")
            .args(["+a", entry])
            .arg(path)
            .status()
            .unwrap()
            .success()
    );
}
/// `home/code/project`, both 0755, with no ACL (as on a stock Mac).
fn project(home: &Path) -> PathBuf {
    directory(&home.join("code"), 0o755);
    let root = home.join("code/project");
    directory(&root, 0o755);
    root
}
/// The invoking account's ids, read from a directory this test created.
fn uid() -> u32 {
    fs::metadata(crate::test_scratch::temp_dir()).unwrap().uid()
}
fn gid() -> u32 {
    let probe = crate::test_scratch::temp_dir().join(format!("opensip-x2a-gid-{}", std::process::id()));
    let _ = fs::create_dir(&probe);
    let gid = fs::metadata(&probe).unwrap().gid();
    let _ = fs::remove_dir(&probe);
    gid
}
fn premise() -> AclOmissionPremise {
    let flag = Box::leak(Box::new(AtomicBool::new(false)));
    let attempt = InitialInstallationAttempt::for_tests(flag, None).unwrap();
    AclOmissionPremise::for_tests(&attempt, &[b"apfs"])
}
fn any_volume(_: &DescriptorFilesystem) -> bool {
    true
}
fn no_volume(_: &DescriptorFilesystem) -> bool {
    false
}

struct Run {
    premise: Option<AclOmissionPremise>,
    groups: BTreeSet<u32>,
    home_volume: fn(&DescriptorFilesystem) -> bool,
}
impl Run {
    fn with_premise() -> Self {
        Self {
            premise: Some(premise()),
            groups: BTreeSet::new(),
            home_volume: any_volume,
        }
    }
    fn walk(&self, home: &Path, root: &Path) -> Result<ProjectChain, Failure> {
        let mut ledger = WorkLedger::new();
        self.walk_on(&mut ledger, home, root)
    }
    fn walk_on(
        &self,
        ledger: &mut WorkLedger,
        home: &Path,
        root: &Path,
    ) -> Result<ProjectChain, Failure> {
        let volume = self.home_volume;
        let policy = ProjectChainPolicy::new(self.premise.as_ref(), &volume, &self.groups);
        ledger.scope(|work| walk_project_chain(home, root, uid(), &policy, work))
    }
    fn recheck(&self, chain: &ProjectChain) -> Result<(), Failure> {
        let volume = self.home_volume;
        let policy = ProjectChainPolicy::new(self.premise.as_ref(), &volume, &self.groups);
        let mut ledger = WorkLedger::new();
        ledger.scope(|work| chain.recheck(uid(), &policy, work))
    }
}
fn row(result: Result<ProjectChain, Failure>) -> ProjectChainRow {
    match result {
        Err(WorkFailure::Operation(refusal)) => refusal.row(),
        Err(WorkFailure::Budget(budget)) => panic!("budget: {budget:?}"),
        Ok(_) => panic!("admitted"),
    }
}
fn custody(subject: &'static str) -> ProjectChainRow {
    ProjectChainRow::RootCustody(subject)
}

#[test]
fn an_ordinary_project_below_h_is_admitted_under_the_premise_and_charged() {
    churned(|| {
        let (_scratch, home) = scratch();
        let root = project(&home);
        let mut ledger = WorkLedger::new();
        let chain = Run::with_premise()
            .walk_on(&mut ledger, &home, &root)
            .unwrap();
        assert!(ledger.used().edges > 0);
        assert_eq!(chain.spelling(), root.as_path());
        assert_eq!(chain.below_home(), 1);
        let meta = fs::metadata(&root).unwrap();
        let held = chain.root().as_file().metadata().unwrap();
        assert_eq!((held.dev(), held.ino()), (meta.dev(), meta.ino()));
        assert_eq!(chain.birth().metadata().inode, meta.ino());
        assert!(chain.birth().birth_seconds() > 0);
        // Nothing was created or changed.
        assert_eq!(fs::read_dir(&root).unwrap().count(), 0);
    });
}

#[test]
fn without_a_premise_the_omitted_acl_at_the_root_of_the_filesystem_refuses() {
    churned(|| {
        let (_scratch, home) = scratch();
        let root = project(&home);
        let run = Run {
            premise: None,
            ..Run::with_premise()
        };
        let result = run.walk(&home, &root);
        assert!(matches!(
            result,
            Err(WorkFailure::Operation(ProjectChainRefusal::Chain(
                ParentRefusal::AncestorAclOmitted { component: 0 }
            )))
        ));
        assert_eq!(row(run.walk(&home, &root)), custody("acl-unreadable"));
    });
}

#[test]
fn h_itself_and_roots_outside_h_are_outside_home_before_any_open() {
    let (scratch, home) = scratch();
    let elsewhere = scratch.0.join("elsewhere");
    directory(&elsewhere, 0o755);
    let run = Run::with_premise();
    for root in [
        home.clone(),
        scratch.0.clone(),
        elsewhere.clone(),
        PathBuf::from("/tmp"),
    ] {
        assert_eq!(row(run.walk(&home, &root)), custody("outside-home"));
    }
    // A sibling whose name extends H's last component is not below H.
    let sibling = PathBuf::from(format!("{}-other", home.display()));
    directory(&sibling, 0o755);
    assert_eq!(row(run.walk(&home, &sibling)), custody("outside-home"));
}

#[test]
fn a_root_inside_the_installation_parent_is_outside_home_in_any_case() {
    churned(|| {
        let (_scratch, home) = scratch();
        let run = Run::with_premise();
        for spelling in [
            "Library/Application Support/OpenSIP",
            "Library/Application Support/OpenSIP/preview-v1",
            "library/application support/opensip/x",
        ] {
            // Judged lexically, before any open: nothing needs to exist.
            assert_eq!(
                row(run.walk(&home, &home.join(spelling))),
                custody("outside-home")
            );
        }
        // Library and Application Support themselves, and siblings of OpenSIP,
        // are ordinary below-H paths (they still face custody).
        directory(&home.join("Library"), 0o700);
        directory(&home.join("Library/Application Support"), 0o755);
        directory(&home.join("Library/Application Support/Other"), 0o755);
        assert!(
            run.walk(&home, &home.join("Library/Application Support/Other"))
                .is_ok()
        );
    });
}

#[test]
fn bad_spellings_and_missing_roots_are_explicit_path_rows() {
    churned(|| {
        let (_scratch, home) = scratch();
        let root = project(&home);
        let run = Run::with_premise();
        let dotted = PathBuf::from(format!("{}/code/./project", home.display()));
        let parent = PathBuf::from(format!("{}/code/../code/project", home.display()));
        let relative = PathBuf::from("code/project");
        let missing = home.join("code/absent");
        let file = home.join("code/file");
        fs::write(&file, b"").unwrap();
        for path in [dotted, parent, relative, missing, file] {
            assert_eq!(
                row(run.walk(&home, &path)),
                ProjectChainRow::ExplicitPath,
                "{path:?}"
            );
        }
        assert!(run.walk(&home, &root).is_ok());
    });
}

#[test]
fn a_symlinked_component_refuses() {
    churned(|| {
        let (_scratch, home) = scratch();
        let root = project(&home);
        std::os::unix::fs::symlink(home.join("code"), home.join("link")).unwrap();
        let run = Run::with_premise();
        // macOS reports a no-follow directory open of a link as ENOTDIR (and
        // ELOOP elsewhere): either way it never resolves and is refused.
        let refused = row(run.walk(&home, &home.join("link/project")));
        assert!(
            refused == ProjectChainRow::ExplicitPath || refused == custody("symlink"),
            "{refused:?}"
        );
        // A link as the root itself refuses the same way.
        std::os::unix::fs::symlink(&root, home.join("code/alias")).unwrap();
        assert!(run.walk(&home, &home.join("code/alias")).is_err());
        assert!(run.walk(&home, &root).is_ok());
    });
}

#[test]
fn a_writable_directory_between_h_and_the_root_refuses_under_the_ancestor_predicate() {
    churned(|| {
        let (_scratch, home) = scratch();
        let root = project(&home);
        let run = Run::with_premise();
        chmod(&home.join("code"), 0o775);
        assert_eq!(row(run.walk(&home, &root)), custody("mode"));
        chmod(&home.join("code"), 0o757);
        assert_eq!(row(run.walk(&home, &root)), custody("mode"));
        chmod(&home.join("code"), 0o755);
        // An ACL write grant to another principal on an ancestor refuses, even
        // to a trusted group: trust groups are the root's, not its ancestors'.
        acl(&home.join("code"), "group:staff allow write");
        let trusting = Run {
            groups: BTreeSet::from([gid()]),
            ..Run::with_premise()
        };
        assert!(trusting.walk(&home, &root).is_err());
        assert!(run.walk(&home, &root).is_err());
    });
}

#[test]
fn the_root_follows_s3_custody_with_explicit_trust_groups() {
    churned(|| {
        let (_scratch, home) = scratch();
        let root = project(&home);
        let run = Run::with_premise();
        chmod(&root, 0o757);
        assert_eq!(row(run.walk(&home, &root)), custody("mode"));
        chmod(&root, 0o775);
        assert_eq!(row(run.walk(&home, &root)), custody("mode"));
        let trusting = Run {
            groups: BTreeSet::from([gid()]),
            ..Run::with_premise()
        };
        assert!(trusting.walk(&home, &root).is_ok());
        chmod(&root, 0o755);
        acl(&root, "group:everyone allow write");
        assert_eq!(row(run.walk(&home, &root)), custody("acl-write"));
        // A read-only allow and a deny are no writers.
        let _ = std::process::Command::new("/bin/chmod")
            .args(["-N"])
            .arg(&root)
            .status();
        acl(&root, "group:everyone allow list,search,readattr");
        acl(&root, "group:everyone deny delete");
        assert!(run.walk(&home, &root).is_ok());
    });
}

#[test]
fn an_omitted_root_acl_passes_only_through_the_premise() {
    churned(|| {
        let (_scratch, home) = scratch();
        let root = project(&home);
        // Give every directory from H down a present ACL so only the root, and
        // the system ancestors above H, omit theirs.
        acl(&home, "group:everyone deny delete");
        acl(&home.join("code"), "group:everyone deny delete");
        let run = Run::with_premise();
        assert!(run.walk(&home, &root).is_ok());
        // The pure root judgment refuses an omitted ACL on its own.
        let mut ledger = WorkLedger::new();
        let sample = ledger
            .scope::<_, ()>(|work| {
                opensip_platform::capture_descriptor_acl_accounted(
                    &fs::File::open(&root).unwrap(),
                    work,
                )
                .map_err(|_| WorkFailure::Operation(()))
            })
            .unwrap();
        assert_eq!(sample.acl_state(), CapturedAclState::NotReturned);
        assert_eq!(
            check_project_root(
                sample.metadata(),
                sample.acl_state(),
                |i| sample.entry(i),
                uid(),
                &BTreeSet::new(),
            ),
            Err(crate::custody::Refusal::AclUnreadable)
        );
    });
}

#[test]
fn a_directory_from_h_down_on_another_volume_is_volume_unsupported() {
    churned(|| {
        let (_scratch, home) = scratch();
        let root = project(&home);
        let run = Run {
            home_volume: no_volume,
            ..Run::with_premise()
        };
        let result = run.walk(&home, &root);
        // H itself is the first directory judged against H's volume.
        let depth = home.components().count() - 1;
        assert!(matches!(
            result,
            Err(WorkFailure::Operation(ProjectChainRefusal::VolumeUnsupported { component }))
                if component == depth
        ));
        assert_eq!(row(run.walk(&home, &root)), custody("volume-unsupported"));
    });
}

#[test]
fn the_recheck_sees_custody_name_and_identity_changes() {
    churned(|| {
        let (_scratch, home) = scratch();
        let root = project(&home);
        let run = Run::with_premise();
        let chain = run.walk(&home, &root).unwrap();
        run.recheck(&chain).unwrap();
        // A mode change on an ancestor.
        chmod(&home.join("code"), 0o775);
        assert!(matches!(
            run.recheck(&chain),
            Err(WorkFailure::Operation(ProjectChainRefusal::Chain(
                ParentRefusal::Ancestor { .. }
            )))
        ));
        chmod(&home.join("code"), 0o755);
        run.recheck(&chain).unwrap();
        // A rename of the root.
        fs::rename(&root, home.join("code/renamed")).unwrap();
        assert!(matches!(
            run.recheck(&chain),
            Err(WorkFailure::Operation(ProjectChainRefusal::Changed))
        ));
        // The same name now bound to a different directory.
        directory(&root, 0o755);
        assert!(matches!(
            run.recheck(&chain),
            Err(WorkFailure::Operation(ProjectChainRefusal::Changed))
        ));
    });
}

#[test]
fn a_short_ledger_refuses_on_the_budget_and_stays_closed() {
    churned(|| {
        let (_scratch, home) = scratch();
        let root = project(&home);
        let run = Run::with_premise();
        let mut full = WorkLedger::new();
        run.walk_on(&mut full, &home, &root).unwrap();
        let used = full.used();
        let mut short = WorkLedger::with_limits(WorkCost {
            objects: used.objects,
            edges: used.edges - 1,
            bytes: used.bytes,
        })
        .unwrap();
        assert!(matches!(
            run.walk_on(&mut short, &home, &root),
            Err(WorkFailure::Budget(WorkBudgetError::Edges))
        ));
        assert!(short.is_failed());
    });
}

#[test]
fn a_deep_project_fits_well_inside_the_owner_budget() {
    churned(|| {
        let (_scratch, home) = scratch();
        let mut root = home.clone();
        for level in 0..64 {
            root = root.join(format!("d{level}"));
            directory(&root, 0o755);
        }
        let mut ledger = WorkLedger::new();
        let chain = Run::with_premise()
            .walk_on(&mut ledger, &home, &root)
            .unwrap();
        assert_eq!(chain.below_home(), 63);
        let used = ledger.used();
        eprintln!("x2a 64-level project chain: {used:?}");
        assert!(used.objects < 65_536 / 2);
        assert!(used.edges < 131_072 / 2);
        assert!(used.bytes < (256 << 20) / 2);
    });
}

#[test]
fn the_walk_creates_nothing_and_the_policy_takes_no_caller_premise() {
    churned(|| {
        // The premise type has no public constructor: production values come only
        // from the read or write receipt (`omission_premise()`), and the policy
        // borrows it. This pins the policy's inputs.
        fn pinned<'a>(
            premise: Option<&'a AclOmissionPremise>,
            home_filesystem: &'a dyn Fn(&DescriptorFilesystem) -> bool,
            trust_groups: &'a BTreeSet<u32>,
        ) -> ProjectChainPolicy<'a> {
            ProjectChainPolicy::new(premise, home_filesystem, trust_groups)
        }
        let _ = pinned;
        let (_scratch, home) = scratch();
        let root = project(&home);
        let before: Vec<_> = fs::read_dir(&home).unwrap().map(|e| e.unwrap().path()).collect();
        Run::with_premise().walk(&home, &root).unwrap();
        let after: Vec<_> = fs::read_dir(&home).unwrap().map(|e| e.unwrap().path()).collect();
        assert_eq!(before, after);
    });
}

#[test]
fn lawful_changes_inside_the_root_keep_the_birth_identity() {
    churned(|| {
        let (_scratch, home) = scratch();
        let root = project(&home);
        let run = Run::with_premise();
        let chain = run.walk(&home, &root).unwrap();
        // A file created in the root changes its mtime and ctime.
        fs::write(root.join("source.rs"), b"fn main() {}").unwrap();
        run.recheck(&chain).unwrap();
        // `.opensip` created in the root also changes its link count.
        directory(&root.join(".opensip"), 0o700);
        run.recheck(&chain).unwrap();
        // A replaced root (a new directory at the same name) fails.
        fs::rename(&root, home.join("code/old")).unwrap();
        directory(&root, 0o755);
        assert!(run.recheck(&chain).is_err());
    });
}

#[test]
fn the_birth_identity_is_device_inode_and_native_birth_only() {
    churned(|| {
        let (_scratch, home) = scratch();
        let root = project(&home);
        let other = home.join("code/other");
        directory(&other, 0o755);
        let run = Run::with_premise();
        let a = run.walk(&home, &root).unwrap();
        let b = run.walk(&home, &other).unwrap();
        assert!(same_birth(a.birth(), a.birth()));
        // A different directory: a different inode.
        assert!(!same_birth(a.birth(), b.birth()));
        // The same directory after lawful changes: same identity, other metadata.
        fs::write(root.join("f"), b"x").unwrap();
        directory(&root.join(".opensip"), 0o700);
        let again = run.walk(&home, &root).unwrap();
        assert_ne!(a.birth().metadata(), again.birth().metadata());
        assert!(same_birth(a.birth(), again.birth()));
    });
}

#[test]
fn placement_allocates_nothing_and_the_spelling_copy_is_charged() {
    churned(|| {
        let (_scratch, home) = scratch();
        let root = project(&home);
        let used = |r: &Path| {
            let mut ledger = WorkLedger::new();
            let _ = ledger.scope(|work| work.run(placement_cost(&home, r), |_| placement(&home, r).map_err(WorkFailure::Operation)));
            ledger.used()
        };
        // Placement charges no object, whatever the depth.
        assert_eq!(used(&root).objects, 0);
        // The full walk includes the spelling's object and bytes.
        let mut ledger = WorkLedger::new();
        Run::with_premise().walk_on(&mut ledger, &home, &root).unwrap();
        let spelling = spelling_cost(&root);
        assert!(ledger.used().objects >= spelling.objects);
        // A ledger that can pay everything but the spelling refuses before the copy.
        let mut short = WorkLedger::with_limits(WorkCost {
            objects: ledger.used().objects - 1,
            edges: ledger.used().edges,
            bytes: ledger.used().bytes,
        })
        .unwrap();
        assert!(matches!(
            Run::with_premise().walk_on(&mut short, &home, &root),
            Err(WorkFailure::Budget(WorkBudgetError::Objects))
        ));
    });
}

// M3-B r5 item 23 (unit B3-a): the typed source lends exactly the
// invocation's authorized set.
#[test]
fn from_grants_lends_the_invocation_groups() {
    let groups = crate::grants::AuthorizedGroups::from_invocation(&[20, 20, 30]).unwrap();
    let home = |_: &DescriptorFilesystem| true;
    let policy = ProjectChainPolicy::from_grants(None, &home, &groups);
    assert!(std::ptr::eq(policy.trust_groups, groups.as_set()));
    assert!(policy.premise.is_none());
}
