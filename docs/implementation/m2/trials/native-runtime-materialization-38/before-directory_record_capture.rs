// Actual bounded reads of ALL canonical names returned by334. These retained
// files/raw bytes are not admitted D records, a qualified census or authority.
use super::{
    directory_name_scan::{self, Names},
    retained_metadata_index::{Budget, Collection, Error as BudgetError},
};
use crate::{
    custody::{DirectoryPathRefusal, NativeRefusal, directory_policy, inspect_operational_file},
    journal_store::{
        OperationalBytesObservation, OperationalReadFailure, read_bounded_operational,
    },
};
use opensip_platform::{DescriptorObservation, RetainedChildDirectory};
use std::{collections::BTreeSet, fs::File, io, os::unix::fs::MetadataExt, sync::Arc};

#[derive(Debug)]
pub(super) enum Error {
    Budget(BudgetError),
    Scan(directory_name_scan::Error),
    Directory(DirectoryPathRefusal),
    File(NativeRefusal),
    Read(OperationalReadFailure),
    Open(io::Error),
    NameChanged,
    Changed,
}
impl From<BudgetError> for Error {
    fn from(e: BudgetError) -> Self {
        Self::Budget(e)
    }
}
pub(super) struct Record {
    digest: [u8; 32],
    file: File,
    raw: Arc<[u8]>,
    observation: DescriptorObservation,
}
impl Record {
    pub(super) fn digest(&self) -> [u8; 32] {
        self.digest
    }
    pub(super) fn file(&self) -> &File {
        &self.file
    }
    pub(super) fn raw(&self) -> &[u8] {
        &self.raw
    }
    pub(super) fn observation(&self) -> &DescriptorObservation {
        &self.observation
    }
}
pub(super) struct Captured {
    names: Names,
    records: Vec<Record>,
}
impl Captured {
    pub(super) fn visit_filesystems(
        &self,
        uid: u32,
        groups: &BTreeSet<u32>,
        visit: &mut impl FnMut(&opensip_platform::DescriptorFilesystem) -> std::io::Result<()>,
    ) -> Result<(), Error> {
        self.recheck(uid, groups)?;
        for fs in self
            .names
            .directory()
            .observe_filesystems()
            .map_err(Error::Open)?
        {
            visit(&fs).map_err(Error::Open)?;
        }
        for record in &self.records {
            visit(&opensip_platform::observe_filesystem(&record.file).map_err(Error::Open)?)
                .map_err(Error::Open)?;
        }
        self.recheck(uid, groups)
    }
    pub(super) fn recheck(&self, uid: u32, groups: &BTreeSet<u32>) -> Result<(), Error> {
        self.names.recheck(uid, groups).map_err(Error::Scan)?;
        for record in &self.records {
            let now = inspect_operational_file(&record.file, uid, groups).map_err(Error::File)?;
            check_name(
                self.names.directory(),
                &opensip_identity::digest_hex(&record.digest),
                &record.file,
            )?;
            if now.metadata != record.observation.metadata
                || now.possible_acl_writers != record.observation.possible_acl_writers
            {
                return Err(Error::Changed);
            }
        }
        self.names.recheck(uid, groups).map_err(Error::Scan)
    }

    pub(super) fn names(&self) -> &Names {
        &self.names
    }
    pub(super) fn records(&self) -> &[Record] {
        &self.records
    }
}
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub(super) enum Phase {
    BeforeRead,
    AfterRead,
}
// New independent open is solely a relative-name observation. Content is read
// ONLY from the original retained descriptor, never from this reopened handle.
pub(super) fn check_name(
    directory: &RetainedChildDirectory,
    leaf: &str,
    file: &File,
) -> Result<(), Error> {
    let current = directory
        .directory()
        .open_regular(leaf)
        .map_err(Error::Open)?;
    let current = current.metadata().map_err(Error::Open)?;
    let original = file.metadata().map_err(Error::Open)?;
    if !opensip_platform::descriptor_name_matches(file, std::ffi::OsStr::new(leaf))
        .map_err(Error::Open)?
        || !current.is_file()
        || !original.is_file()
        || current.nlink() != 1
        || original.nlink() != 1
        || current.dev() != original.dev()
        || current.ino() != original.ino()
    {
        return Err(Error::NameChanged);
    }
    Ok(())
}
pub(super) fn read_one(
    directory: &RetainedChildDirectory,
    leaf: &str,
    cap: usize,
    uid: u32,
    groups: &BTreeSet<u32>,
    mut interpose: impl FnMut(Phase),
) -> Result<(File, Vec<u8>, DescriptorObservation), Error> {
    directory_policy::inspect(directory, uid, groups).map_err(Error::Directory)?;
    let opened = directory.directory().open_regular(leaf);
    // Even failed opens must not bypass relative directory checks.
    directory_policy::inspect(directory, uid, groups).map_err(Error::Directory)?;
    let mut file = opened.map_err(Error::Open)?;
    let before = inspect_operational_file(&file, uid, groups).map_err(Error::File)?;
    if before.metadata.size > cap as u64 {
        return Err(Error::Read(OperationalReadFailure::Bound));
    }
    check_name(directory, leaf, &file)?;
    interpose(Phase::BeforeRead);
    let read = read_bounded_operational(&mut file, cap);
    interpose(Phase::AfterRead);
    let after = inspect_operational_file(&file, uid, groups).map_err(Error::File)?;
    directory_policy::inspect(directory, uid, groups).map_err(Error::Directory)?;
    check_name(directory, leaf, &file)?;
    if before.metadata != after.metadata
        || before.possible_acl_writers != after.possible_acl_writers
    {
        return Err(Error::Changed);
    }
    match read {
        OperationalBytesObservation::Present(raw) => Ok((file, raw, after)),
        OperationalBytesObservation::Unreadable(e) => Err(Error::Read(e)),
        OperationalBytesObservation::Absent => Err(Error::Read(OperationalReadFailure::Context)),
    }
}
/// Scan and capture share one Budget, with no public handoff that could reset
/// enumeration work before reading content. Every named path is freshly opened
/// even when its Publications digest is already cached. No NotFound is absence.
pub(super) fn capture(
    budget: &mut Budget,
    directory: Arc<RetainedChildDirectory>,
    uid: u32,
    groups: &BTreeSet<u32>,
    foreign: impl FnMut(&[u8]) -> Result<(), ()>,
) -> Result<Captured, Error> {
    capture_with(budget, directory, uid, groups, foreign, || {})
}
// The private seam schedules actual mutations AFTER completed enumeration;
// it cannot inject names/handles/bytes and avoids filesystem-order assumptions.
fn capture_with(
    budget: &mut Budget,
    directory: Arc<RetainedChildDirectory>,
    uid: u32,
    groups: &BTreeSet<u32>,
    foreign: impl FnMut(&[u8]) -> Result<(), ()>,
    after_scan: impl FnOnce(),
) -> Result<Captured, Error> {
    budget.scope(|b| {
        let names =
            directory_name_scan::scan(b, directory, uid, groups, foreign).map_err(Error::Scan)?;
        after_scan();
        let mut records = Vec::new();
        for digest in names.canonical() {
            b.edge(1)?;
            let leaf = opensip_identity::digest_hex(digest);
            let mut retained = None;
            let mut failure = None;
            // available() bounds object/bytes BEFORE invoking this native reader;
            // true forces current path presence independently of the raw cache.
            let result = b.capture(
                Collection::Publications,
                *digest,
                true,
                |cap| match read_one(names.directory(), &leaf, cap, uid, groups, |_| {}) {
                    Ok((file, raw, observation)) => {
                        retained = Some((file, observation));
                        Ok(raw)
                    }
                    Err(e) => {
                        failure = Some(e);
                        Err(())
                    }
                },
            );
            let raw = match result {
                Ok(raw) => raw,
                Err(e) => return Err(failure.unwrap_or(Error::Budget(e))),
            };
            let (file, observation) = retained.ok_or(Error::Budget(BudgetError::Capture))?;
            records.push(Record {
                digest: *digest,
                file,
                raw,
                observation,
            });
        }
        // Per-file postchecks do not replace the final directory sample when
        // the scan is empty or multiple candidate captures have occurred.
        directory_policy::inspect(names.directory(), uid, groups).map_err(Error::Directory)?;
        Ok(Captured { names, records })
    })
}

#[cfg(all(test, target_os = "macos"))]
mod tests {
    use super::*;
    use opensip_platform::RetainedDirectory;
    use std::{
        ffi::OsStr,
        fs::{self, Permissions},
        os::unix::fs::{FileExt, PermissionsExt, symlink},
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
            let root = std::env::temp_dir().join(format!("opensip-directory-capture-{id}"));
            fs::create_dir(&root).unwrap();
            fs::set_permissions(&root, Permissions::from_mode(0o700)).unwrap();
            let uid = fs::metadata(&root).unwrap().uid();
            Self { root, uid }
        }
        fn dir(&self, name: &str) -> Arc<RetainedChildDirectory> {
            fs::create_dir(self.root.join(name)).unwrap();
            fs::set_permissions(self.root.join(name), Permissions::from_mode(0o700)).unwrap();
            Arc::new(
                RetainedDirectory::from_retained_handle(File::open(&self.root).unwrap())
                    .unwrap()
                    .bind_child_directory(OsStr::new(name))
                    .unwrap(),
            )
        }
        fn write(&self, dir: &str, raw: &[u8]) -> ([u8; 32], PathBuf) {
            let hash = opensip_identity::raw_sha256(raw);
            let path = self
                .root
                .join(dir)
                .join(opensip_identity::digest_hex(&hash));
            fs::write(&path, raw).unwrap();
            fs::set_permissions(&path, Permissions::from_mode(0o600)).unwrap();
            (hash, path)
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
    fn run(b: &mut Budget, d: Arc<RetainedChildDirectory>, f: &Fixture) -> Result<Captured, Error> {
        capture(b, d, f.uid, &BTreeSet::new(), |_| Ok(()))
    }
    #[test]
    fn directory_capture_owns_exact_bytes_and_original_files_after_inputs_drop() {
        let f = Fixture::new();
        let d = f.dir("a");
        let (h1, _) = f.write("a", b"one");
        let (h2, _) = f.write("a", b"two");
        fs::write(f.root.join("a/foreign"), b"keep").unwrap();
        let mut b = budget();
        let captured = run(&mut b, d, &f).unwrap();
        assert_eq!(captured.records().len(), 2);
        let mut expected = vec![h1, h2];
        expected.sort();
        assert_eq!(
            captured
                .records()
                .iter()
                .map(Record::digest)
                .collect::<Vec<_>>(),
            expected
        );
        assert_eq!(b.counters(), (3, 8, 144));
        drop(b);
        fs::rename(f.root.join("a"), f.root.join("moved")).unwrap();
        fs::create_dir(f.root.join("a")).unwrap();
        for r in captured.records() {
            assert_eq!(opensip_identity::raw_sha256(r.raw()), r.digest());
            assert_eq!(
                r.file().metadata().unwrap().ino(),
                r.observation().metadata.inode
            );
            let mut raw = [0; 3];
            r.file().read_exact_at(&mut raw, 0).unwrap();
            assert_eq!(raw.as_slice(), r.raw());
        }
        assert!(!captured.names().directory().recheck().unwrap());
        assert_eq!(fs::read(f.root.join("moved/foreign")).unwrap(), b"keep");
    }
    #[test]
    fn directory_capture_rejects_wrong_kind_links_permissions_empty_and_digest_mismatch() {
        for kind in [
            "directory",
            "symlink",
            "hardlink",
            "mode",
            "empty",
            "digest",
        ] {
            let f = Fixture::new();
            let d = f.dir("a");
            let (_, path) = f.write("a", if kind == "empty" { b"" } else { b"expected" });
            match kind {
                "directory" => {
                    fs::remove_file(&path).unwrap();
                    fs::create_dir(&path).unwrap();
                }
                "symlink" => {
                    fs::remove_file(&path).unwrap();
                    symlink("absent", &path).unwrap();
                }
                "hardlink" => fs::hard_link(&path, f.root.join("extra")).unwrap(),
                "mode" => fs::set_permissions(&path, Permissions::from_mode(0o666)).unwrap(),
                "digest" => fs::write(&path, b"wrong digest").unwrap(),
                _ => {}
            }
            let mut b = budget();
            assert!(run(&mut b, d, &f).is_err(), "{kind}");
            assert_eq!(b.edge(1), Err(BudgetError::Closed));
            assert!(fs::symlink_metadata(&path).is_ok());
        }
    }
    #[test]
    fn directory_capture_cache_never_substitutes_for_missing_or_wrong_kind_new_path() {
        for replacement in ["missing", "symlink"] {
            let f = Fixture::new();
            let a = f.dir("a");
            let z = f.dir("z");
            let (h, _) = f.write("a", b"same");
            let (_, zp) = f.write("z", b"same");
            fs::write(f.root.join("z/foreign"), b"keep").unwrap();
            let mut b = budget();
            let first = run(&mut b, a, &f).unwrap();
            assert_eq!(first.records()[0].digest(), h);
            let result = capture_with(
                &mut b,
                z,
                f.uid,
                &BTreeSet::new(),
                |_| Ok(()),
                || {
                    fs::remove_file(&zp).unwrap();
                    if replacement == "symlink" {
                        symlink("absent", &zp).unwrap();
                    }
                },
            );
            assert!(result.is_err(), "{replacement}");
            assert_eq!(b.edge(1), Err(BudgetError::Closed));
        }
    }
    #[test]
    fn directory_capture_exact_remaining_bytes_and_objects_do_not_reset_scan_budget() {
        let f = Fixture::new();
        let d = f.dir("a");
        f.write("a", b"raw");
        let mut b = Budget::new(2, 5, 70).unwrap();
        let result = run(&mut b, Arc::clone(&d), &f).unwrap();
        assert_eq!(result.records()[0].raw(), b"raw");
        assert_eq!(b.counters(), (2, 5, 70));
        for (o, e, n) in [(1, 5, 70), (2, 4, 70), (2, 5, 69)] {
            let mut b = Budget::new(o, e, n).unwrap();
            assert!(run(&mut b, Arc::clone(&d), &f).is_err());
            assert_eq!(b.edge(1), Err(BudgetError::Closed));
        }
    }
    #[test]
    fn directory_capture_late_bad_candidate_cannot_return_partial_success() {
        let f = Fixture::new();
        let d = f.dir("a");
        f.write("a", b"good");
        let bad = f.root.join("a").join("f".repeat(64));
        fs::write(&bad, b"bad hash").unwrap();
        fs::set_permissions(&bad, Permissions::from_mode(0o600)).unwrap();
        let mut b = budget();
        assert!(matches!(
            run(&mut b, d, &f),
            Err(Error::Budget(BudgetError::Digest))
        ));
        assert_eq!(b.counters().0, 2);
        assert_eq!(b.edge(1), Err(BudgetError::Closed));
        assert_eq!(fs::read(&bad).unwrap(), b"bad hash");
    }
    #[test]
    fn directory_capture_native_interposition_never_returns_changed_file_as_stable() {
        for at in [Phase::BeforeRead, Phase::AfterRead] {
            for change in ["rename-file", "rename-directory", "chmod", "in-place"] {
                let f = Fixture::new();
                let d = f.dir("a");
                let (h, path) = f.write("a", b"old");
                let leaf = opensip_identity::digest_hex(&h);
                let result = read_one(&d, &leaf, 100, f.uid, &BTreeSet::new(), |phase| {
                    if phase != at {
                        return;
                    }
                    match change {
                        "rename-file" => {
                            fs::rename(&path, f.root.join("old")).unwrap();
                            fs::write(&path, b"old").unwrap();
                            fs::set_permissions(&path, Permissions::from_mode(0o600)).unwrap();
                        }
                        "rename-directory" => {
                            fs::rename(f.root.join("a"), f.root.join("old")).unwrap();
                            fs::create_dir(f.root.join("a")).unwrap();
                        }
                        "chmod" => {
                            fs::set_permissions(&path, Permissions::from_mode(0o666)).unwrap()
                        }
                        _ => fs::write(&path, b"changed length").unwrap(),
                    }
                });
                assert!(result.is_err(), "{at:?} {change}");
            }
        }
    }
    #[test]
    fn directory_capture_identical_cached_bytes_still_own_each_actual_path_file() {
        let f = Fixture::new();
        let a = f.dir("a");
        let z = f.dir("z");
        f.write("a", b"same");
        f.write("z", b"same");
        let mut b = budget();
        let first = run(&mut b, a, &f).unwrap();
        let second = run(&mut b, z, &f).unwrap();
        assert!(Arc::ptr_eq(&first.records[0].raw, &second.records[0].raw));
        assert_ne!(
            first.records[0].observation.metadata.inode,
            second.records[0].observation.metadata.inode
        );
        let cached = b.retain(Collection::Publications, b"same").unwrap();
        assert!(Arc::ptr_eq(&cached, &first.records[0].raw));
        assert_eq!(b.counters(), (3, 10, 138));
    }
    #[test]
    fn directory_capture_empty_scan_still_checks_directory_after_capture_boundary() {
        for change in ["mode", "rename"] {
            let f = Fixture::new();
            let d = f.dir("a");
            let mut b = budget();
            let r = capture_with(
                &mut b,
                d,
                f.uid,
                &BTreeSet::new(),
                |_| Ok(()),
                || {
                    if change == "mode" {
                        fs::set_permissions(f.root.join("a"), Permissions::from_mode(0o777))
                            .unwrap();
                    } else {
                        fs::rename(f.root.join("a"), f.root.join("old")).unwrap();
                        fs::create_dir(f.root.join("a")).unwrap();
                    }
                },
            );
            assert!(matches!(r, Err(Error::Directory(_))));
            assert_eq!(b.edge(1), Err(BudgetError::Closed));
        }
    }
    #[test]
    fn directory_capture_name_check_distinguishes_same_bytes_in_another_inode() {
        let f = Fixture::new();
        let d = f.dir("a");
        let (h, path) = f.write("a", b"same");
        let leaf = opensip_identity::digest_hex(&h);
        let retained = d.directory().open_regular(&leaf).unwrap();
        fs::rename(&path, f.root.join("old")).unwrap();
        fs::write(&path, b"same").unwrap();
        assert!(matches!(
            check_name(&d, &leaf, &retained),
            Err(Error::NameChanged)
        ));
        fs::remove_file(&path).unwrap();
        assert!(matches!(
            check_name(&d, &leaf, &retained),
            Err(Error::Open(_))
        ));
    }
    #[test]
    fn directory_capture_observed_oversize_refuses_before_read_boundary() {
        let f = Fixture::new();
        let d = f.dir("a");
        let (h, _) = f.write("a", b"oversize");
        let leaf = opensip_identity::digest_hex(&h);
        assert!(matches!(
            read_one(&d, &leaf, 2, f.uid, &BTreeSet::new(), |_| panic!(
                "oversize reached read boundary"
            )),
            Err(Error::Read(OperationalReadFailure::Bound))
        ));
    }
    #[test]
    fn directory_capture_exact_file_name_rejects_case_alias_after_completed_scan() {
        let f = Fixture::new();
        let d = f.dir("a");
        let (hash, path) = f.write("a", b"name-case");
        let leaf = opensip_identity::digest_hex(&hash);
        let upper = path.with_file_name(leaf.to_uppercase());
        assert_ne!(path, upper);
        let mut b = budget();
        let result = capture_with(
            &mut b,
            d,
            f.uid,
            &BTreeSet::new(),
            |_| Ok(()),
            || {
                fs::rename(&path, &upper).unwrap();
            },
        );
        assert!(matches!(
            result,
            Err(Error::NameChanged) | Err(Error::Open(_))
        ));
        assert_eq!(b.edge(1), Err(BudgetError::Closed));
        assert_eq!(fs::read(&upper).unwrap(), b"name-case");
    }
    #[test]
    fn directory_capture_foreign_uppercase_is_reported_unread_and_not_adopted() {
        let f = Fixture::new();
        let d = f.dir("a");
        let (hash, path) = f.write("a", b"foreign");
        let upper = opensip_identity::digest_hex(&hash).to_uppercase();
        fs::rename(&path, path.with_file_name(&upper)).unwrap();
        let mut seen = Vec::new();
        let mut b = budget();
        let got = capture(&mut b, d, f.uid, &BTreeSet::new(), |n| {
            seen.push(n.to_vec());
            Ok(())
        })
        .unwrap();
        assert!(got.records().is_empty());
        assert_eq!(seen, vec![upper.as_bytes()]);
        assert_eq!(b.counters(), (1, 4, 67));
    }
    #[test]
    fn directory_capture_exact_file_name_checks_retained_original_after_case_rename() {
        let f = Fixture::new();
        let d = f.dir("a");
        let (hash, path) = f.write("a", b"retained-name");
        let leaf = opensip_identity::digest_hex(&hash);
        let file = d.directory().open_regular(&leaf).unwrap();
        assert!(check_name(&d, &leaf, &file).is_ok());
        fs::rename(&path, path.with_file_name(leaf.to_uppercase())).unwrap();
        assert!(matches!(
            check_name(&d, &leaf, &file),
            Err(Error::NameChanged) | Err(Error::Open(_))
        ));
    }
}
