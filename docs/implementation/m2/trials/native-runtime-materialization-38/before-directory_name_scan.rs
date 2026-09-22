// Bounded OS-returned names, NOT descriptor admission or a qualified census.
// This composes 330/332/333 with the SAME immutable-evidence work Budget.
use super::retained_metadata_index::{Budget, Error as BudgetError};
use crate::custody::{DirectoryPathRefusal, directory_policy};
use opensip_platform::{
    DescriptorObservation, DirectoryVisitError, DirectoryVisitSummary, RetainedChildDirectory,
};
use std::{collections::BTreeSet, sync::Arc};

#[derive(Debug)]
pub(super) enum EntryError {
    Budget(BudgetError),
    CanonicalLimit,
    Duplicate,
    Diagnostic,
}
#[derive(Debug)]
pub(super) enum Error {
    Budget(BudgetError),
    Policy(DirectoryPathRefusal),
    Changed,
    Visit(DirectoryVisitError<EntryError>),
}
impl From<BudgetError> for Error {
    fn from(e: BudgetError) -> Self {
        Self::Budget(e)
    }
}
pub(super) struct Names {
    directory: Arc<RetainedChildDirectory>,
    canonical: Vec<[u8; 32]>,
    summary: DirectoryVisitSummary,
    observation: DescriptorObservation,
}
impl Names {
    pub(super) fn recheck(&self, uid: u32, groups: &BTreeSet<u32>) -> Result<(), Error> {
        let [_, now] =
            directory_policy::inspect(&self.directory, uid, groups).map_err(Error::Policy)?;
        if now.metadata != self.observation.metadata
            || now.possible_acl_writers != self.observation.possible_acl_writers
        {
            return Err(Error::Changed);
        }
        Ok(())
    }

    pub(super) fn directory(&self) -> &RetainedChildDirectory {
        &self.directory
    }
    pub(super) fn canonical(&self) -> &[[u8; 32]] {
        &self.canonical
    }
    pub(super) fn summary(&self) -> DirectoryVisitSummary {
        self.summary
    }
}
// No lossy decoding, case folding, extension stripping, or type/inode hints.
fn canonical(name: &[u8]) -> Option<[u8; 32]> {
    if name.len() != 64 {
        return None;
    }
    fn digit(b: u8) -> Option<u8> {
        match b {
            b'0'..=b'9' => Some(b - b'0'),
            b'a'..=b'f' => Some(b - b'a' + 10),
            _ => None,
        }
    }
    let mut digest = [0; 32];
    for (i, pair) in name.chunks_exact(2).enumerate() {
        digest[i] = digit(pair[0])? * 16 + digit(pair[1])?;
    }
    Some(digest)
}
fn entry(
    budget: &mut Budget,
    names: &mut Vec<[u8; 32]>,
    name: &[u8],
    foreign: &mut impl FnMut(&[u8]) -> Result<(), ()>,
) -> Result<(), EntryError> {
    budget.entry(name).map_err(EntryError::Budget)?;
    if let Some(digest) = canonical(name) {
        if names.contains(&digest) {
            return Err(EntryError::Duplicate);
        }
        if names.len() == 64 {
            return Err(EntryError::CanonicalLimit);
        }
        names.push(digest);
    } else if name != b"." && name != b".." {
        // Callback sees a borrowed, already-charged name. It must not interpret
        // foreign content, mutate the directory or retain unbounded diagnostics.
        foreign(name).map_err(|_| EntryError::Diagnostic)?;
    }
    Ok(())
}
/// The supplied native edge was captured by the caller before this operation.
/// No retrospective pre-allocation/custody claim for that capture is made here.
/// Successful EOF and name/policy samples are not continuous exclusion, full
/// ancestor admission or selected-filesystem qualification. No file is opened
/// from these names, and no absence/orphan/successor decision is produced.
pub(super) fn scan(
    budget: &mut Budget,
    directory: Arc<RetainedChildDirectory>,
    uid: u32,
    groups: &BTreeSet<u32>,
    mut foreign: impl FnMut(&[u8]) -> Result<(), ()>,
) -> Result<Names, Error> {
    budget.scope(|b| {
        let [_, before] =
            directory_policy::inspect(&directory, uid, groups).map_err(Error::Policy)?;
        b.directory(Arc::clone(&directory))?;
        let mut names = Vec::new();
        let summary = directory
            .directory()
            .visit_entry_names(131_072, 268_435_456, |name| {
                entry(b, &mut names, name, &mut foreign)
            })
            .map_err(Error::Visit)?;
        let [_, after] =
            directory_policy::inspect(&directory, uid, groups).map_err(Error::Policy)?;
        if before.metadata != after.metadata
            || before.possible_acl_writers != after.possible_acl_writers
        {
            return Err(Error::Changed);
        }
        names.sort_unstable();
        Ok(Names {
            directory,
            canonical: names,
            summary,
            observation: after,
        })
    })
}

#[cfg(all(test, target_os = "macos"))]
mod tests {
    use super::super::retained_metadata_index::Collection;
    use super::*;
    use opensip_platform::RetainedDirectory;
    use std::{
        ffi::OsStr,
        fs::{self, File, Permissions},
        os::unix::fs::{MetadataExt, PermissionsExt, symlink},
        path::PathBuf,
    };
    struct Fixture {
        root: PathBuf,
        uid: u32,
    }
    impl Fixture {
        fn new() -> Self {
            let id: String = opensip_platform::request_entropy()
                .unwrap()
                .iter()
                .map(|b| format!("{b:02x}"))
                .collect();
            let root = std::env::temp_dir().join(format!("opensip-directory-budget-{id}"));
            fs::create_dir(&root).unwrap();
            fs::set_permissions(&root, Permissions::from_mode(0o700)).unwrap();
            let uid = fs::metadata(&root).unwrap().uid();
            Self { root, uid }
        }
        fn add(&self, name: &str) -> Arc<RetainedChildDirectory> {
            fs::create_dir(self.root.join(name)).unwrap();
            fs::set_permissions(self.root.join(name), Permissions::from_mode(0o700)).unwrap();
            self.bind(name)
        }
        fn bind(&self, name: &str) -> Arc<RetainedChildDirectory> {
            Arc::new(
                RetainedDirectory::from_retained_handle(File::open(&self.root).unwrap())
                    .unwrap()
                    .bind_child_directory(OsStr::new(name))
                    .unwrap(),
            )
        }
    }
    impl Drop for Fixture {
        fn drop(&mut self) {
            let _ = fs::remove_dir_all(&self.root);
        }
    }
    fn budget() -> Budget {
        Budget::new(65536, 131072, 268435456).unwrap()
    }
    fn run(b: &mut Budget, d: Arc<RetainedChildDirectory>, f: &Fixture) -> Result<Names, Error> {
        scan(b, d, f.uid, &BTreeSet::new(), |_| Ok(()))
    }
    #[test]
    fn directory_scan_exact_names_sorted_foreign_unread_and_repeated_work_charged() {
        let f = Fixture::new();
        let d = f.add("bucket");
        let path = f.root.join("bucket");
        fs::write(
            path.join("a".repeat(64)),
            b"malformed candidate not read by name scan",
        )
        .unwrap();
        fs::create_dir(path.join("0".repeat(64))).unwrap();
        symlink("absent", path.join("f".repeat(64))).unwrap();
        let upper = "B".repeat(64);
        fs::write(path.join(&upper), b"foreign").unwrap();
        symlink("absent", path.join("foreign")).unwrap();
        let mut b = budget();
        let mut foreign = Vec::new();
        let result = scan(&mut b, Arc::clone(&d), f.uid, &BTreeSet::new(), |n| {
            foreign.push(n.to_vec());
            Ok(())
        })
        .unwrap();
        assert_eq!(result.canonical(), &[[0; 32], [0xaa; 32], [0xff; 32]]);
        foreign.sort();
        let mut expected = vec![upper.into_bytes(), b"foreign".to_vec()];
        expected.sort();
        assert_eq!(foreign, expected);
        assert_eq!(result.summary().entries(), 7);
        assert_eq!(result.summary().name_bytes(), 266);
        assert_eq!(b.counters(), (1, 8, 266));
        let again = run(&mut b, f.bind("bucket"), &f).unwrap();
        assert_eq!(again.canonical(), result.canonical());
        assert_eq!(b.counters(), (1, 16, 532));
        drop(d);
        assert!(result.directory().recheck().unwrap());
        assert_eq!(
            fs::read(path.join("a".repeat(64))).unwrap(),
            b"malformed candidate not read by name scan"
        );
        assert!(
            fs::symlink_metadata(path.join("foreign"))
                .unwrap()
                .file_type()
                .is_symlink()
        );
    }
    #[test]
    fn directory_scan_sixty_four_capacity_and_overfull_latches_shared_budget() {
        let f = Fixture::new();
        let d = f.add("bucket");
        for i in 0..64 {
            fs::write(f.root.join("bucket").join(format!("{i:064x}")), b"x").unwrap();
        }
        let mut b = budget();
        let names = run(&mut b, Arc::clone(&d), &f).unwrap();
        assert_eq!(names.canonical().len(), 64);
        fs::write(f.root.join("bucket").join(format!("{:064x}", 64)), b"x").unwrap();
        assert!(matches!(
            run(&mut b, d, &f),
            Err(Error::Visit(DirectoryVisitError::Visitor(
                EntryError::CanonicalLimit
            )))
        ));
        assert_eq!(
            b.retain(Collection::Records, b"later"),
            Err(BudgetError::Closed)
        );
        assert_eq!(fs::read_dir(f.root.join("bucket")).unwrap().count(), 65);
    }
    #[test]
    fn directory_scan_shares_object_slots_with_evidence_in_both_orders() {
        let f = Fixture::new();
        let a = f.add("a");
        let z = f.add("z");
        let mut b = Budget::new(2, 100, 1000).unwrap();
        b.retain(Collection::Records, b"x").unwrap();
        run(&mut b, Arc::clone(&a), &f).unwrap();
        run(&mut b, Arc::clone(&a), &f).unwrap();
        assert_eq!(b.counters().0, 2);
        assert!(matches!(
            run(&mut b, z, &f),
            Err(Error::Budget(BudgetError::ObjectLimit))
        ));
        drop(b);
        let mut b = Budget::new(1, 100, 1000).unwrap();
        run(&mut b, Arc::clone(&a), &f).unwrap();
        let weak = Arc::downgrade(&a);
        drop(a);
        assert!(weak.upgrade().is_some());
        assert_eq!(
            b.retain(Collection::Records, b"x"),
            Err(BudgetError::ObjectLimit)
        );
        drop(b);
        assert!(weak.upgrade().is_none());
    }
    #[test]
    fn directory_scan_shared_edges_and_bytes_include_dots_foreign_before_diagnostics() {
        let f = Fixture::new();
        let d = f.add("bucket");
        fs::write(f.root.join("bucket/foreign"), b"untouched").unwrap();
        let mut b = Budget::new(10, 1, 1000).unwrap();
        let mut seen = 0;
        assert!(
            scan(&mut b, Arc::clone(&d), f.uid, &BTreeSet::new(), |_| {
                seen += 1;
                Ok(())
            })
            .is_err()
        );
        assert_eq!(seen, 0);
        assert_eq!(b.counters(), (1, 1, 0));
        let mut b = Budget::new(10, 100, 3).unwrap();
        let mut seen = 0;
        assert!(matches!(
            scan(&mut b, Arc::clone(&d), f.uid, &BTreeSet::new(), |_| {
                seen += 1;
                Ok(())
            }),
            Err(Error::Visit(DirectoryVisitError::Visitor(
                EntryError::Budget(BudgetError::ByteLimit)
            )))
        ));
        assert_eq!(seen, 0);
        assert_eq!(b.edge(1), Err(BudgetError::Closed));
        let mut b = Budget::new(10, 100, 11).unwrap();
        let names = run(&mut b, d, &f).unwrap();
        assert_eq!(names.summary().name_bytes(), 10);
        b.retain(Collection::Records, b"x").unwrap();
        assert_eq!(b.counters().2, 11);
        assert_eq!(
            b.retain(Collection::Records, b"y"),
            Err(BudgetError::ByteLimit)
        );
    }
    #[test]
    fn directory_scan_foreign_failure_and_post_name_policy_changes_latch() {
        for change in ["callback-error", "rename", "chmod"] {
            let f = Fixture::new();
            let d = f.add("bucket");
            fs::write(f.root.join("bucket/foreign"), b"keep").unwrap();
            let mut b = budget();
            let r = scan(&mut b, d, f.uid, &BTreeSet::new(), |_| {
                match change {
                    "callback-error" => return Err(()),
                    "rename" => {
                        fs::rename(f.root.join("bucket"), f.root.join("old")).unwrap();
                        fs::create_dir(f.root.join("bucket")).unwrap();
                    }
                    _ => fs::set_permissions(f.root.join("bucket"), Permissions::from_mode(0o777))
                        .unwrap(),
                }
                Ok(())
            });
            match change {
                "callback-error" => assert!(matches!(
                    r,
                    Err(Error::Visit(DirectoryVisitError::Visitor(
                        EntryError::Diagnostic
                    )))
                )),
                _ => assert!(matches!(r, Err(Error::Policy(_)))),
            }
            assert_eq!(b.edge(1), Err(BudgetError::Closed));
        }
    }
    #[test]
    fn directory_scan_classification_duplicate_and_before_materialization() {
        for name in [
            b"A".repeat(64),
            b"a".repeat(63),
            b"a".repeat(65),
            vec![0xff; 64],
            b"g".repeat(64),
        ] {
            assert_eq!(canonical(&name), None);
        }
        assert_eq!(canonical(&b"f".repeat(64)), Some([255; 32]));
        let mut b = Budget::new(1, 10, 63).unwrap();
        let mut names = vec![];
        assert!(matches!(
            entry(&mut b, &mut names, &b"a".repeat(64), &mut |_| panic!()),
            Err(EntryError::Budget(BudgetError::ByteLimit))
        ));
        assert!(names.is_empty());
        let mut b = budget();
        let mut names = vec![];
        entry(&mut b, &mut names, &b"a".repeat(64), &mut |_| panic!()).unwrap();
        assert!(matches!(
            entry(&mut b, &mut names, &b"a".repeat(64), &mut |_| panic!()),
            Err(EntryError::Duplicate)
        ));
        assert_eq!(names.len(), 1);
        assert_eq!(b.counters(), (0, 2, 128));
    }
    #[test]
    fn directory_scan_pre_policy_refuses_before_enumerating_or_accounting() {
        let f = Fixture::new();
        let d = f.add("bucket");
        fs::write(f.root.join("bucket/foreign"), b"keep").unwrap();
        fs::set_permissions(f.root.join("bucket"), Permissions::from_mode(0o702)).unwrap();
        let mut b = budget();
        assert!(matches!(
            scan(&mut b, d, f.uid, &BTreeSet::new(), |_| panic!(
                "unsafe input reached visitor"
            )),
            Err(Error::Policy(_))
        ));
        assert_eq!(b.counters(), (0, 0, 0));
        assert_eq!(b.edge(1), Err(BudgetError::Closed));
    }
}
