//! Single-component, handle-relative directory opens. Selection, ownership,
//! ACL/mount admission, name stability and exclusion remain security concerns.
use super::{RetainedDirectory, STAGING_PREFIX};
use std::ffi::{CString, OsStr};
use std::fs::File;
use std::io;
use std::os::fd::{AsRawFd, FromRawFd};
use std::os::unix::ffi::OsStrExt;

// Bound our native-name allocation independently of a filesystem's smaller
// NAME_MAX. The kernel can impose a stricter limit; it is never bypassed.
const MAX_COMPONENT_BYTES: usize = 1023;
fn component(name: &OsStr) -> io::Result<CString> {
    let raw = name.as_bytes();
    if raw.is_empty()
        || raw.len() > MAX_COMPONENT_BYTES
        || matches!(raw, b"." | b"..")
        || raw.contains(&b'/')
        || raw.contains(&b'\\')
        || raw.contains(&0)
        || raw.starts_with(STAGING_PREFIX.as_bytes())
    {
        return Err(io::Error::new(
            io::ErrorKind::InvalidInput,
            "invalid child directory component",
        ));
    }
    CString::new(raw).map_err(|_| io::ErrorKind::InvalidInput.into())
}
/// One `openat` of a child directory and the kind-check status read on the
/// new handle: the handle, the NUL-terminated name and the status buffer.
pub fn open_child_directory_cost(name: &OsStr) -> crate::WorkCost {
    let status = super::path_binding::status_read_cost();
    crate::WorkCost {
        objects: 2,
        edges: 1 + status.edges,
        bytes: name
            .as_bytes()
            .len()
            .saturating_add(1)
            .saturating_add(status.bytes),
    }
}
/// One `fstatat` without following a final symlink: the name and the status buffer.
pub fn child_absence_observation_cost(name: &OsStr) -> crate::WorkCost {
    crate::WorkCost {
        objects: 1,
        edges: 1,
        bytes: name
            .as_bytes()
            .len()
            .saturating_add(1)
            .saturating_add(std::mem::size_of::<libc::stat>()),
    }
}
/// What one no-follow status read reports a child entry to be (unit B2-b1).
#[cfg(target_os = "macos")]
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum ChildKind {
    Directory,
    File,
    Symlink,
    Other,
}
#[cfg(target_os = "macos")]
impl ChildKind {
    fn of(mode: u32) -> Self {
        let format = mode & libc::S_IFMT as u32;
        if format == libc::S_IFDIR as u32 {
            Self::Directory
        } else if format == libc::S_IFREG as u32 {
            Self::File
        } else if format == libc::S_IFLNK as u32 {
            Self::Symlink
        } else {
            Self::Other
        }
    }
}
/// One by-name observation of a child entry, made from its parent without
/// opening the child (M3-B r5 items 12 and 13; unit B2-b1). It keeps the
/// entry's identity so that a later open can be compared with it. It is one
/// sample: it proves no binding, custody or exclusion.
#[cfg(target_os = "macos")]
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum ChildObservation {
    Absent,
    Present {
        kind: ChildKind,
        metadata: super::DescriptorMetadata,
    },
}
#[cfg(target_os = "macos")]
impl ChildObservation {
    /// Whether `opened` (the status of a descriptor opened from the same name)
    /// is the entry observed: same device, inode and kind. An absent
    /// observation matches nothing, so a change between observation and open
    /// is never mistaken for the original entry.
    pub fn matches(&self, opened: &super::DescriptorMetadata) -> bool {
        match self {
            Self::Absent => false,
            Self::Present { kind, metadata } => {
                metadata.device == opened.device
                    && metadata.inode == opened.inode
                    && *kind == ChildKind::of(opened.mode)
            }
        }
    }
}
#[cfg(target_os = "macos")]
impl RetainedDirectory {
    /// Observe `name` under this exact retained handle with one `fstatat` and
    /// `AT_SYMLINK_NOFOLLOW`. The child is never opened, created or followed.
    /// Only `ENOENT` is absence; every other error is returned.
    pub fn observe_child(&self, name: &OsStr) -> io::Result<ChildObservation> {
        let name = component(name)?;
        let mut stat = std::mem::MaybeUninit::<libc::stat>::uninit();
        // SAFETY: live retained parent fd, bounded NUL-terminated single
        // component, writable stat storage. No creation or following occurs.
        let result = unsafe {
            libc::fstatat(
                self.0.as_raw_fd(),
                name.as_ptr(),
                stat.as_mut_ptr(),
                libc::AT_SYMLINK_NOFOLLOW,
            )
        };
        if result != 0 {
            let error = io::Error::last_os_error();
            return if error.raw_os_error() == Some(libc::ENOENT) {
                Ok(ChildObservation::Absent)
            } else {
                Err(error)
            };
        }
        // SAFETY: fstatat succeeded and initialized the buffer.
        let stat = unsafe { stat.assume_init() };
        let metadata = super::DescriptorMetadata::from_stat(&stat);
        Ok(ChildObservation::Present {
            kind: ChildKind::of(metadata.mode),
            metadata,
        })
    }
    /// `observe_child`, charged to `work` first: the same single status read
    /// as `child_absence_observation_cost`.
    pub fn observe_child_accounted(
        &self,
        name: &OsStr,
        work: &mut crate::WorkScope<'_>,
    ) -> Result<ChildObservation, crate::WorkFailure<io::Error>> {
        work.run(child_absence_observation_cost(name), |_| {
            self.observe_child(name)
                .map_err(crate::WorkFailure::Operation)
        })
    }
}
impl RetainedDirectory {
    /// `open_child_directory`, charged to `work` first. A native NotFound is
    /// returned as `None`, an observation that does not fail the work scope;
    /// it is not authorized or fenced absence. Every other error fails the
    /// scope and keeps the charge.
    pub fn open_child_directory_if_present_accounted(
        &self,
        name: &OsStr,
        work: &mut crate::WorkScope<'_>,
    ) -> Result<Option<RetainedDirectory>, crate::WorkFailure<io::Error>> {
        work.run(open_child_directory_cost(name), |_| {
            match self.open_child_directory(name) {
                Ok(child) => Ok(Some(child)),
                Err(error) if error.kind() == io::ErrorKind::NotFound => Ok(None),
                Err(error) => Err(crate::WorkFailure::Operation(error)),
            }
        })
    }
    /// `open_child_directory`, spending `open_child_directory_cost` from an
    /// existing reservation first, with no second outer charge. Every error,
    /// NotFound included, closes the original operation and keeps the spend.
    pub fn open_child_directory_reserved(
        &self,
        name: &OsStr,
        post: &mut crate::ReservedPostchecks<'_>,
    ) -> Result<RetainedDirectory, crate::WorkFailure<io::Error>> {
        post.scope(|post| {
            post.spend(open_child_directory_cost(name))?;
            self.open_child_directory(name)
                .map_err(crate::WorkFailure::Operation)
        })
    }
    /// Observe whether `name` is absent under this exact retained handle, with
    /// `fstatat` and `AT_SYMLINK_NOFOLLOW`. Only `ENOENT` is absence (true). Any
    /// entry, including a dangling symlink, is presence (false). Every other
    /// error is returned. This is one sample through this handle; it is not
    /// exclusion, a parent/name binding, or permission to create.
    pub fn observe_child_absent(&self, name: &OsStr) -> io::Result<bool> {
        let name = component(name)?;
        let mut stat = std::mem::MaybeUninit::<libc::stat>::uninit();
        // SAFETY: live retained parent fd, bounded NUL-terminated single
        // component, writable stat storage. No creation or following occurs.
        let result = unsafe {
            libc::fstatat(
                self.0.as_raw_fd(),
                name.as_ptr(),
                stat.as_mut_ptr(),
                libc::AT_SYMLINK_NOFOLLOW,
            )
        };
        if result == 0 {
            return Ok(false);
        }
        let error = io::Error::last_os_error();
        if error.raw_os_error() == Some(libc::ENOENT) {
            Ok(true)
        } else {
            Err(error)
        }
    }
    /// `observe_child_absent`, charged to `work` first.
    pub fn observe_child_absent_accounted(
        &self,
        name: &OsStr,
        work: &mut crate::WorkScope<'_>,
    ) -> Result<bool, crate::WorkFailure<io::Error>> {
        work.run(child_absence_observation_cost(name), |_| {
            self.observe_child_absent(name)
                .map_err(crate::WorkFailure::Operation)
        })
    }
    /// Open one existing child directory under this exact retained handle.
    /// No pathname root is reselected, no intermediate components are walked,
    /// and no symlink fallback, creation, chmod, cleanup or retry occurs.
    /// Non-UTF8 OS bytes are preserved, not normalized into another name.
    /// A native NotFound is an observation, not authorized/fenced absence.
    /// The returned handle proves neither current parent/name attachment nor
    /// ownership, ACL policy, filesystem support, mount identity or durability.
    pub fn open_child_directory(&self, name: &OsStr) -> io::Result<RetainedDirectory> {
        let name = component(name)?;
        // SAFETY: live retained parent fd and bounded NUL-terminated single
        // component. No create flags; the new descriptor is independently owned.
        let fd = unsafe {
            libc::openat(
                self.0.as_raw_fd(),
                name.as_ptr(),
                libc::O_RDONLY
                    | libc::O_DIRECTORY
                    | libc::O_NOFOLLOW
                    | libc::O_CLOEXEC
                    | libc::O_NONBLOCK,
            )
        };
        if fd < 0 {
            return Err(io::Error::last_os_error());
        }
        // SAFETY: successful openat returns one new owned fd; File closes it on
        // constructor error and RetainedDirectory owns it on success.
        let file = unsafe { File::from_raw_fd(fd) };
        RetainedDirectory::from_retained_handle(file)
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    use std::os::unix::fs::{MetadataExt, symlink};
    use std::path::PathBuf;
    struct Fixture {
        root: PathBuf,
    }
    impl Fixture {
        fn new() -> Self {
            let mut random = [0u8; 16];
            getrandom::fill(&mut random).unwrap();
            let id: String = random.iter().map(|b| format!("{b:02x}")).collect();
            let root = std::env::temp_dir().join(format!("opensip-child-directory-{id}"));
            std::fs::create_dir(&root).unwrap();
            Self { root }
        }
        fn retained(&self) -> RetainedDirectory {
            RetainedDirectory::from_retained_handle(File::open(&self.root).unwrap()).unwrap()
        }
    }
    impl Drop for Fixture {
        fn drop(&mut self) {
            let _ = std::fs::remove_dir_all(&self.root);
        }
    }
    #[test]
    fn child_directory_component_is_bounded_and_preserves_os_bytes() {
        for raw in [
            b"".as_slice(),
            b".",
            b"..",
            b"/",
            b"a/b",
            b"a\\b",
            b"a\0b",
            b".opensip-stage-abc",
        ] {
            assert_eq!(
                component(OsStr::from_bytes(raw)).unwrap_err().kind(),
                io::ErrorKind::InvalidInput
            );
        }
        assert_eq!(
            component(OsStr::from_bytes(&vec![b'x'; 1024]))
                .unwrap_err()
                .kind(),
            io::ErrorKind::InvalidInput
        );
        assert_eq!(
            component(OsStr::from_bytes(&vec![b'x'; 1023]))
                .unwrap()
                .as_bytes(),
            vec![b'x'; 1023]
        );
        for raw in [b"sha256-name".as_slice(), b".other", &[0xff, 0xfe, b'a']] {
            assert_eq!(component(OsStr::from_bytes(raw)).unwrap().as_bytes(), raw);
        }
    }
    #[test]
    fn child_directory_native_retains_cloexec_readonly_directory_without_creating() {
        let f = Fixture::new();
        std::fs::create_dir(f.root.join("child")).unwrap();
        let parent = f.retained();
        let child = parent.open_child_directory(OsStr::new("child")).unwrap();
        assert!(child.0.metadata().unwrap().is_dir());
        // SAFETY: F_GETFD/F_GETFL only inspect this live owned descriptor.
        assert_ne!(
            unsafe { libc::fcntl(child.0.as_raw_fd(), libc::F_GETFD) } & libc::FD_CLOEXEC,
            0
        );
        // SAFETY: descriptor remains owned by child for this query.
        assert_eq!(
            unsafe { libc::fcntl(child.0.as_raw_fd(), libc::F_GETFL) } & libc::O_ACCMODE,
            libc::O_RDONLY
        );
        let expected = std::fs::metadata(f.root.join("child")).unwrap();
        let actual = child.0.metadata().unwrap();
        assert_eq!(
            (actual.dev(), actual.ino()),
            (expected.dev(), expected.ino())
        );
        assert_eq!(
            parent
                .open_child_directory(OsStr::new("absent"))
                .err()
                .unwrap()
                .kind(),
            io::ErrorKind::NotFound
        );
        assert!(!f.root.join("absent").exists());
        assert_eq!(std::fs::read_dir(&f.root).unwrap().count(), 1);
    }
    #[test]
    fn child_directory_native_refuses_links_non_directories_and_traversal() {
        let f = Fixture::new();
        std::fs::create_dir(f.root.join("actual")).unwrap();
        std::fs::create_dir(f.root.join("actual/nested")).unwrap();
        std::fs::write(f.root.join("regular"), b"unchanged").unwrap();
        symlink("actual", f.root.join("link")).unwrap();
        symlink("missing", f.root.join("dangling")).unwrap();
        let fifo = CString::new(f.root.join("fifo").as_os_str().as_bytes()).unwrap();
        // SAFETY: live bounded test path; creation is solely test fixture setup.
        assert_eq!(unsafe { libc::mkfifo(fifo.as_ptr(), 0o600) }, 0);
        let p = f.retained();
        for name in ["link", "dangling", "regular", "fifo"] {
            let error = p
                .open_child_directory(OsStr::new(name))
                .err()
                .expect("not a directory capability");
            assert_ne!(
                error.kind(),
                io::ErrorKind::NotFound,
                "{name} cannot become absence"
            );
        }
        for name in ["actual/nested", "../escape", ".", ".opensip-stage-x"] {
            assert_eq!(
                p.open_child_directory(OsStr::new(name))
                    .err()
                    .unwrap()
                    .kind(),
                io::ErrorKind::InvalidInput
            );
        }
        assert_eq!(std::fs::read(f.root.join("regular")).unwrap(), b"unchanged");
    }
    #[test]
    fn child_directory_native_follows_retained_parent_and_child_not_replaced_paths() {
        let f = Fixture::new();
        let selected = f.root.join("selected");
        std::fs::create_dir(&selected).unwrap();
        std::fs::create_dir(selected.join("child")).unwrap();
        std::fs::write(selected.join("child/old"), b"retained").unwrap();
        let p = RetainedDirectory::from_retained_handle(File::open(&selected).unwrap()).unwrap();
        std::fs::rename(&selected, f.root.join("moved")).unwrap();
        std::fs::create_dir(&selected).unwrap();
        std::fs::create_dir(selected.join("child")).unwrap();
        std::fs::write(selected.join("child/decoy"), b"wrong").unwrap();
        let c = p.open_child_directory(OsStr::new("child")).unwrap();
        let mut seen = Vec::new();
        c.visit_entry_names(20, 1000, |n| {
            seen.push(n.to_vec());
            Ok::<_, ()>(())
        })
        .unwrap();
        assert!(seen.contains(&b"old".to_vec()));
        assert!(!seen.contains(&b"decoy".to_vec()));
        std::fs::rename(
            f.root.join("moved/child"),
            f.root.join("moved/original-child"),
        )
        .unwrap();
        std::fs::create_dir(f.root.join("moved/child")).unwrap();
        std::fs::write(f.root.join("moved/child/replacement"), b"wrong").unwrap();
        seen.clear();
        c.visit_entry_names(20, 1000, |n| {
            seen.push(n.to_vec());
            Ok::<_, ()>(())
        })
        .unwrap();
        assert!(seen.contains(&b"old".to_vec()));
        assert!(!seen.contains(&b"replacement".to_vec()));
        let mut bytes = Vec::new();
        use std::io::Read;
        c.open_regular("old")
            .unwrap()
            .read_to_end(&mut bytes)
            .unwrap();
        assert_eq!(bytes, b"retained");
    }
    #[test]
    fn accounted_child_open_reports_absence_without_failing_the_scope() {
        let f = Fixture::new();
        std::fs::create_dir(f.root.join("present")).unwrap();
        std::fs::write(f.root.join("file"), b"x").unwrap();
        symlink("/nonexistent-opensip-target", f.root.join("dangling")).unwrap();
        let retained = f.retained();
        let mut ledger = crate::WorkLedger::new();
        let missing = ledger
            .scope(|work| {
                retained.open_child_directory_if_present_accounted(OsStr::new("missing"), work)
            })
            .unwrap();
        assert!(missing.is_none());
        assert!(!ledger.is_failed());
        // The openat and the kind-check status read on the new handle.
        let cost = open_child_directory_cost(OsStr::new("missing"));
        assert_eq!(cost.edges, 2);
        assert_eq!(
            cost.bytes,
            "missing".len() + 1 + super::super::path_binding::status_read_cost().bytes
        );
        assert_eq!(
            ledger.used(),
            open_child_directory_cost(OsStr::new("missing"))
        );
        assert!(
            ledger
                .scope(|work| {
                    retained.open_child_directory_if_present_accounted(OsStr::new("present"), work)
                })
                .unwrap()
                .is_some()
        );
        assert!(matches!(
            ledger.scope(|work| {
                retained.open_child_directory_if_present_accounted(OsStr::new("dangling"), work)
            }),
            Err(crate::WorkFailure::Operation(_))
        ));
        assert!(ledger.is_failed());
    }
    #[test]
    fn child_absence_is_only_enoent_and_never_follows_a_symlink() {
        let f = Fixture::new();
        std::fs::create_dir(f.root.join("present")).unwrap();
        std::fs::write(f.root.join("file"), b"x").unwrap();
        symlink("/nonexistent-opensip-target", f.root.join("dangling")).unwrap();
        let retained = f.retained();
        assert!(
            retained
                .observe_child_absent(OsStr::new("missing"))
                .unwrap()
        );
        for name in ["present", "file", "dangling"] {
            assert!(
                !retained.observe_child_absent(OsStr::new(name)).unwrap(),
                "{name}"
            );
        }
        for bad in ["", ".", "..", "a/b", ".opensip-stage-x"] {
            assert_eq!(
                retained
                    .observe_child_absent(OsStr::new(bad))
                    .unwrap_err()
                    .kind(),
                io::ErrorKind::InvalidInput
            );
        }
        let mut ledger = crate::WorkLedger::new();
        assert!(
            ledger
                .scope(|work| retained.observe_child_absent_accounted(OsStr::new("missing"), work))
                .unwrap()
        );
        assert_eq!(
            ledger.used(),
            child_absence_observation_cost(OsStr::new("missing"))
        );
    }
    #[cfg(target_os = "linux")]
    #[test]
    fn child_directory_native_linux_preserves_non_utf8_component() {
        let f = Fixture::new();
        let name = OsStr::from_bytes(&[0xff, 0xfe, b'd']);
        std::fs::create_dir(f.root.join(name)).unwrap();
        let d = f.retained().open_child_directory(name).unwrap();
        assert!(d.0.metadata().unwrap().is_dir());
    }
    // M3-B r5 items 12 and 13 (unit B2-b1): the by-name child observation.
    #[cfg(target_os = "macos")]
    fn present(o: &ChildObservation) -> (ChildKind, crate::DescriptorMetadata) {
        match o {
            ChildObservation::Present { kind, metadata } => (*kind, metadata.clone()),
            ChildObservation::Absent => panic!("absent"),
        }
    }
    #[cfg(target_os = "macos")]
    #[test]
    fn observe_child_reports_each_kind_and_absence_without_opening() {
        let f = Fixture::new();
        std::fs::create_dir(f.root.join("d")).unwrap();
        std::fs::write(f.root.join("f"), b"x").unwrap();
        symlink(f.root.join("d"), f.root.join("l")).unwrap();
        // A FIFO is the "other" kind (a socket path may exceed SUN_LEN here).
        let fifo = CString::new(f.root.join("s").as_os_str().as_bytes()).unwrap();
        // SAFETY: a valid NUL-terminated path inside the private fixture root.
        assert_eq!(unsafe { libc::mkfifo(fifo.as_ptr(), 0o600) }, 0);
        let parent = f.retained();
        for (name, kind) in [
            ("d", ChildKind::Directory),
            ("f", ChildKind::File),
            ("l", ChildKind::Symlink),
            ("s", ChildKind::Other),
        ] {
            let (got, metadata) = present(&parent.observe_child(OsStr::new(name)).unwrap());
            assert_eq!(got, kind, "{name}");
            let lstat = std::fs::symlink_metadata(f.root.join(name)).unwrap();
            assert_eq!(
                (metadata.device, metadata.inode),
                (lstat.dev(), lstat.ino()),
                "{name}"
            );
        }
        assert_eq!(
            parent.observe_child(OsStr::new("missing")).unwrap(),
            ChildObservation::Absent
        );
        for bad in ["..", "a/b", ""] {
            assert_eq!(
                parent.observe_child(OsStr::new(bad)).unwrap_err().kind(),
                io::ErrorKind::InvalidInput
            );
        }
    }
    #[cfg(target_os = "macos")]
    #[test]
    fn observe_child_changes_no_time_of_the_parent_or_the_child() {
        let f = Fixture::new();
        std::fs::create_dir(f.root.join("d")).unwrap();
        std::fs::write(f.root.join("d/inner"), b"x").unwrap();
        let times = |p: &std::path::Path| {
            let m = std::fs::symlink_metadata(p).unwrap();
            (
                m.atime(),
                m.atime_nsec(),
                m.mtime(),
                m.mtime_nsec(),
                m.ctime(),
                m.ctime_nsec(),
            )
        };
        let before = (times(&f.root), times(&f.root.join("d")));
        let parent = f.retained();
        assert_eq!(
            present(&parent.observe_child(OsStr::new("d")).unwrap()).0,
            ChildKind::Directory
        );
        assert_eq!((times(&f.root), times(&f.root.join("d"))), before);
    }
    #[cfg(target_os = "macos")]
    #[test]
    fn a_same_kind_replacement_between_observation_and_open_does_not_match() {
        let f = Fixture::new();
        std::fs::create_dir(f.root.join("d")).unwrap();
        std::fs::write(f.root.join("f"), b"original").unwrap();
        let parent = f.retained();
        let dir = parent.observe_child(OsStr::new("d")).unwrap();
        let file = parent.observe_child(OsStr::new("f")).unwrap();
        // Unchanged: the opened descriptors are the observed entries.
        let opened = parent.open_child_directory(OsStr::new("d")).unwrap();
        assert!(dir.matches(&crate::observe_descriptor_metadata(opened.as_file()).unwrap()));
        let opened = parent.open_regular("f").unwrap();
        assert!(file.matches(&crate::observe_descriptor_metadata(&opened).unwrap()));
        // Replaced by another entry of the same kind under the same name.
        std::fs::rename(f.root.join("d"), f.root.join("d-old")).unwrap();
        std::fs::create_dir(f.root.join("d")).unwrap();
        std::fs::write(f.root.join("f-new"), b"replacement").unwrap();
        std::fs::rename(f.root.join("f-new"), f.root.join("f")).unwrap();
        let opened = parent.open_child_directory(OsStr::new("d")).unwrap();
        let replaced_dir = crate::observe_descriptor_metadata(opened.as_file()).unwrap();
        assert!(!dir.matches(&replaced_dir));
        let opened = parent.open_regular("f").unwrap();
        assert!(!file.matches(&crate::observe_descriptor_metadata(&opened).unwrap()));
        // A kind mismatch or an absent observation never matches.
        let (_, file_metadata) = present(&file);
        assert!(!dir.matches(&file_metadata));
        assert!(!ChildObservation::Absent.matches(&replaced_dir));
    }
    #[cfg(target_os = "macos")]
    #[test]
    fn observe_child_accounted_charges_one_status_read() {
        let f = Fixture::new();
        std::fs::create_dir(f.root.join("d")).unwrap();
        let parent = f.retained();
        let mut ledger = crate::WorkLedger::new();
        let observed = ledger
            .scope::<_, io::Error>(|work| parent.observe_child_accounted(OsStr::new("d"), work))
            .unwrap();
        assert_eq!(present(&observed).0, ChildKind::Directory);
        assert_eq!(
            ledger.used(),
            child_absence_observation_cost(OsStr::new("d"))
        );
    }
}
