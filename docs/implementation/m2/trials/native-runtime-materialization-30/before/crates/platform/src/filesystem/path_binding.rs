//! Retained root-to-leaf directory names, not continuous namespace exclusion.
use super::{RetainedDirectory, STAGING_PREFIX};
use std::{
    ffi::{CStr, CString},
    fs::{File, OpenOptions},
    io,
    os::{
        fd::{AsRawFd, FromRawFd},
        unix::{
            ffi::OsStrExt,
            fs::{MetadataExt, OpenOptionsExt},
        },
    },
    path::Path,
};

struct Edge {
    name: CString,
    directory: RetainedDirectory,
}
/// Owns every directory descriptor from the process root to an absolute path.
/// It observes named identity only. The caller still owes admitted local-filesystem
/// ownership/ACL policy, mount assumptions and exclusion through consumption.
/// A-to-B-to-A changes and mutations after a successful check remain possible.
/// All ancestors must permit O_RDONLY directory opens; search-only ancestors are
/// unsupported. Spelling is retained, but OS case/normalization aliases may bind
/// the same identity. This public mechanism grants no security authority.
pub struct RetainedDirectoryPath {
    root: RetainedDirectory,
    edges: Vec<Edge>,
}
fn flags() -> i32 {
    libc::O_DIRECTORY | libc::O_NOFOLLOW | libc::O_CLOEXEC | libc::O_NONBLOCK
}
fn root() -> io::Result<RetainedDirectory> {
    RetainedDirectory::from_retained_handle(
        OpenOptions::new()
            .read(true)
            .custom_flags(flags())
            .open("/")?,
    )
}
fn child(parent: &RetainedDirectory, name: &CStr) -> io::Result<RetainedDirectory> {
    // SAFETY: parent retains a live directory descriptor; name is a validated
    // single NUL-terminated component. No creation flag or borrowed descriptor is
    // returned. A successful openat returns one newly owned descriptor.
    let fd = unsafe {
        libc::openat(
            parent.0.as_raw_fd(),
            name.as_ptr(),
            libc::O_RDONLY | flags(),
        )
    };
    if fd < 0 {
        return Err(io::Error::last_os_error());
    }
    // SAFETY: this successful openat descriptor is owned exactly once and is
    // closed by File on every success/error path after this point.
    RetainedDirectory::from_retained_handle(unsafe { File::from_raw_fd(fd) })
}
fn same(a: &RetainedDirectory, b: &RetainedDirectory) -> io::Result<bool> {
    let a = a.0.metadata()?;
    let b = b.0.metadata()?;
    Ok(a.is_dir()
        && b.is_dir()
        && a.nlink() != 0
        && b.nlink() != 0
        && a.dev() == b.dev()
        && a.ino() == b.ino())
}
impl RetainedDirectoryPath {
    /// Require each saved child component to match its retained descriptor's
    /// native name in addition to bracketing full root-to-leaf inode checks.
    /// The filesystem root has no child component. This is still sampled,
    /// macOS-only name evidence; no exclusion or filesystem profile is granted.
    pub fn recheck_exact_names(&self) -> io::Result<bool> {
        if !self.recheck()? {
            return Ok(false);
        }
        for edge in &self.edges {
            if !super::directory_names::matches(
                &edge.directory.0,
                std::ffi::OsStr::from_bytes(edge.name.to_bytes()),
            )? {
                return Ok(false);
            }
        }
        self.recheck()
    }
    /// No canonicalization, symlinks, dot segments, empty components or staging
    /// names. Native path bytes reach the OS unchanged; filesystem refusals propagate.
    /// The supplied bound counts child
    /// components, excluding root; it bounds retained descriptors, not path memory.
    pub fn open(path: &Path, max_components: usize) -> io::Result<Self> {
        Self::open_inner(path, max_components, || {})
    }
    // Private sequencing seam; cannot supply or replace a retained descriptor.
    fn open_inner(
        path: &Path,
        max_components: usize,
        after_retention: impl FnOnce(),
    ) -> io::Result<Self> {
        let raw = path.as_os_str().as_bytes();
        if !raw.starts_with(b"/") || raw.contains(&0) || raw.contains(&b'\\') {
            return Err(io::Error::new(
                io::ErrorKind::InvalidInput,
                "invalid absolute directory path",
            ));
        }
        let parts: Vec<&[u8]> = if raw == b"/" {
            Vec::new()
        } else {
            raw[1..].split(|b| *b == b'/').collect()
        };
        if parts.len() > max_components
            || parts.iter().any(|p| {
                p.is_empty()
                    || *p == b"."
                    || *p == b".."
                    || p.starts_with(STAGING_PREFIX.as_bytes())
            })
        {
            return Err(io::Error::new(
                io::ErrorKind::InvalidInput,
                "invalid or over-bound directory components",
            ));
        }
        let root = root()?;
        let mut edges: Vec<Edge> = Vec::with_capacity(parts.len());
        for part in parts {
            let name = CString::new(part).map_err(|_| io::ErrorKind::InvalidInput)?;
            let parent = edges.last().map_or(&root, |e| &e.directory);
            let directory = child(parent, &name)?;
            edges.push(Edge { name, directory });
        }
        let retained = Self { root, edges };
        after_retention();
        if !retained.recheck()? {
            return Err(io::Error::new(
                io::ErrorKind::InvalidData,
                "directory name changed during retention",
            ));
        }
        Ok(retained)
    }
    /// The retained leaf may remain usable after relocation; callers must not
    /// interpret a successful descriptor-relative read as a successful name check.
    pub fn directory(&self) -> &RetainedDirectory {
        self.edges.last().map_or(&self.root, |e| &e.directory)
    }
    /// Sequential filesystem observations for every retained root-to-leaf handle.
    /// No partial result, name re-resolution, coherent snapshot or admission.
    pub fn observe_filesystems(&self) -> io::Result<Vec<super::DescriptorFilesystem>> {
        std::iter::once(&self.root)
            .chain(self.edges.iter().map(|edge| &edge.directory))
            .map(super::RetainedDirectory::observe_filesystem)
            .collect()
    }
    /// Observe every retained descriptor in root-to-leaf order. No descriptor is
    /// exported. Failure returns no partial vector; unsupported ACL observation
    /// stays unsupported. The component bound supplied to open bounds the count.
    /// These are sequential metadata/ACL samples, not a coherent permission
    /// snapshot, a name check, filesystem qualification or lasting custody.
    pub fn observe_directories(
        &self,
    ) -> Result<Vec<super::DescriptorObservation>, super::DescriptorObservationError> {
        std::iter::once(&self.root)
            .chain(self.edges.iter().map(|edge| &edge.directory))
            .map(|directory| super::observe_descriptor(&directory.0))
            .collect()
    }
    /// Re-resolve each edge from its retained parent and compare device/inode.
    /// Missing/substituted directories (including files and symlinks) return false; observation errors remain
    /// errors, never absence of an operational file within the directory.
    /// This is a sequence of samples, not an atomic check or a lasting capability.
    pub fn recheck(&self) -> io::Result<bool> {
        if !same(&self.root, &root()?)? {
            return Ok(false);
        }
        let mut parent = &self.root;
        for edge in &self.edges {
            let reopened = match child(parent, &edge.name) {
                Ok(directory) => directory,
                Err(error)
                    if error.kind() == io::ErrorKind::NotFound
                        || matches!(error.raw_os_error(), Some(libc::ENOTDIR | libc::ELOOP)) =>
                {
                    return Ok(false);
                }
                Err(error) => return Err(error),
            };
            if !same(&edge.directory, &reopened)? {
                return Ok(false);
            }
            parent = &edge.directory;
        }
        Ok(true)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::{
        fs,
        io::Read,
        os::unix::{
            ffi::OsStringExt,
            fs::{PermissionsExt, symlink},
        },
        path::PathBuf,
    };
    struct Fixture(PathBuf);
    impl Fixture {
        fn new() -> Self {
            let tag = crate::request_entropy()
                .unwrap()
                .iter()
                .map(|n| format!("{n:02x}"))
                .collect::<String>();
            let path = std::env::temp_dir().join(format!("opensip-binding161-{tag}"));
            fs::create_dir(&path).unwrap();
            let path = fs::canonicalize(path).unwrap();
            fs::create_dir_all(path.join("outer/inner")).unwrap();
            fs::write(path.join("outer/inner/witness"), b"old").unwrap();
            Self(path)
        }
        fn target(&self) -> PathBuf {
            self.0.join("outer/inner")
        }
        fn capture(&self) -> RetainedDirectoryPath {
            RetainedDirectoryPath::open(&self.target(), 128).unwrap()
        }
    }
    impl Drop for Fixture {
        fn drop(&mut self) {
            let _ = fs::remove_dir_all(&self.0);
        }
    }
    fn read_witness(path: &RetainedDirectoryPath) -> Vec<u8> {
        let mut bytes = Vec::new();
        path.directory()
            .open_regular("witness")
            .unwrap()
            .read_to_end(&mut bytes)
            .unwrap();
        bytes
    }
    #[test]
    fn stable_path_retains_native_names_and_exact_component_bound() {
        let f = Fixture::new();
        let path = f.target();
        let count = path.as_os_str().as_bytes()[1..]
            .split(|b| *b == b'/')
            .count();
        assert!(RetainedDirectoryPath::open(&path, count - 1).is_err());
        let retained = RetainedDirectoryPath::open(&path, count).unwrap();
        assert!(retained.recheck().unwrap());
        assert_eq!(read_witness(&retained), b"old");
        assert_eq!(
            retained
                .directory()
                .open_regular("floor")
                .unwrap_err()
                .kind(),
            io::ErrorKind::NotFound
        );
        let root = RetainedDirectoryPath::open(Path::new("/"), 0).unwrap();
        assert!(root.recheck().unwrap());
        let native =
            f.0.join(std::ffi::OsString::from_vec(b"native-\xff-name".to_vec()));
        match fs::create_dir(&native) {
            Ok(()) => {
                let native = RetainedDirectoryPath::open(&native, 128).unwrap();
                assert!(native.recheck().unwrap());
            }
            Err(error) => {
                // This APFS host refuses non-UTF8 names. Preserve that OS refusal;
                // do not reinterpret its bytes or fabricate a retained directory.
                assert_eq!(error.raw_os_error(), Some(libc::EILSEQ));
                assert!(RetainedDirectoryPath::open(&native, 128).is_err());
            }
        }
    }
    #[test]
    fn leaf_relocation_and_replacement_do_not_inherit_a_name_binding() {
        let f = Fixture::new();
        let retained = f.capture();
        let moved = f.0.join("moved");
        fs::rename(f.target(), &moved).unwrap();
        assert!(!retained.recheck().unwrap());
        assert_eq!(read_witness(&retained), b"old");
        fs::create_dir(f.target()).unwrap();
        fs::write(f.target().join("witness"), b"new").unwrap();
        assert!(!retained.recheck().unwrap());
        assert_eq!(read_witness(&retained), b"old");
        let replacement = f.capture();
        assert!(replacement.recheck().unwrap());
        assert_eq!(read_witness(&replacement), b"new");
    }
    #[test]
    fn moved_ancestor_is_detected_even_when_its_retained_leaf_edge_is_unchanged() {
        let f = Fixture::new();
        let retained = f.capture();
        fs::rename(f.0.join("outer"), f.0.join("moved")).unwrap();
        fs::create_dir_all(f.target()).unwrap();
        fs::write(f.target().join("witness"), b"replacement").unwrap();
        assert!(!retained.recheck().unwrap());
        assert_eq!(read_witness(&retained), b"old");
        // Last-edge-only validation would still pass inside the moved ancestor.
        let n = retained.edges.len();
        let parent = &retained.edges[n - 2].directory;
        let leaf = &retained.edges[n - 1];
        assert!(same(&leaf.directory, &child(parent, &leaf.name).unwrap()).unwrap());
    }
    #[test]
    fn removal_files_and_symlinks_never_become_successful_rechecks() {
        for replacement in ["absent", "directory", "file", "symlink"] {
            let f = Fixture::new();
            let retained = f.capture();
            fs::remove_dir_all(f.target()).unwrap();
            match replacement {
                "directory" => fs::create_dir(f.target()).unwrap(),
                "file" => fs::write(f.target(), b"file").unwrap(),
                "symlink" => symlink(&f.0, f.target()).unwrap(),
                _ => {}
            }
            assert!(!retained.recheck().unwrap(), "{replacement}");
        }
        let f = Fixture::new();
        fs::rename(f.0.join("outer"), f.0.join("moved")).unwrap();
        symlink(f.0.join("moved"), f.0.join("outer")).unwrap();
        assert!(RetainedDirectoryPath::open(&f.target(), 128).is_err());
        assert!(RetainedDirectoryPath::open(&f.0.join("missing"), 128).is_err());
    }
    #[test]
    fn strict_absolute_path_shape_refuses_normalization_and_reserved_components() {
        for path in [
            "",
            "relative",
            "//",
            "/./",
            "/../",
            "/a//b",
            "/a/./b",
            "/a/../b",
            "/a/",
            "/a\\b",
            "/a\0b",
            "/.opensip-stage-x",
        ] {
            assert_eq!(
                RetainedDirectoryPath::open(Path::new(path), 128)
                    .err()
                    .unwrap()
                    .kind(),
                io::ErrorKind::InvalidInput,
                "{path:?}"
            );
        }
    }
    #[test]
    fn recheck_is_an_observation_and_does_not_claim_to_exclude_aba() {
        let f = Fixture::new();
        let retained = f.capture();
        let moved = f.0.join("moved");
        fs::rename(f.target(), &moved).unwrap();
        assert!(!retained.recheck().unwrap());
        fs::rename(&moved, f.target()).unwrap();
        assert!(retained.recheck().unwrap());
    }
    #[test]
    fn permission_failure_is_an_error_not_a_successful_binding() {
        let f = Fixture::new();
        if fs::metadata(&f.0).unwrap().uid() == 0 {
            return;
        }
        let retained = f.capture();
        let outer = f.0.join("outer");
        fs::set_permissions(&outer, fs::Permissions::from_mode(0o0)).unwrap();
        let result = retained.recheck();
        fs::set_permissions(&outer, fs::Permissions::from_mode(0o700)).unwrap();
        assert_eq!(
            result.err().unwrap().kind(),
            io::ErrorKind::PermissionDenied
        );
    }
    #[test]
    fn relocation_before_construction_returns_never_creates_a_successful_binding() {
        let f = Fixture::new();
        let result = RetainedDirectoryPath::open_inner(&f.target(), 128, || {
            fs::rename(f.0.join("outer"), f.0.join("moved")).unwrap();
            fs::create_dir_all(f.target()).unwrap();
        });
        assert_eq!(result.err().unwrap().kind(), io::ErrorKind::InvalidData);
    }
    #[test]
    fn retained_chain_descriptors_are_readonly_nonblocking_and_close_on_exec() {
        let f = Fixture::new();
        let retained = f.capture();
        for directory in
            std::iter::once(&retained.root).chain(retained.edges.iter().map(|e| &e.directory))
        {
            // SAFETY: both fcntl queries take a live retained descriptor and no
            // pointer argument; they neither transfer ownership nor mutate it.
            let descriptor_flags = unsafe { libc::fcntl(directory.0.as_raw_fd(), libc::F_GETFD) };
            let status_flags = unsafe { libc::fcntl(directory.0.as_raw_fd(), libc::F_GETFL) };
            assert!(descriptor_flags >= 0 && status_flags >= 0);
            assert_ne!(descriptor_flags & libc::FD_CLOEXEC, 0);
            assert_ne!(status_flags & libc::O_NONBLOCK, 0);
            assert_eq!(status_flags & libc::O_ACCMODE, libc::O_RDONLY);
        }
    }
    #[cfg(target_os = "macos")]
    #[test]
    fn actual_observations_include_root_and_every_retained_ancestor_in_order() {
        // Test-only retries: parallel tests legitimately change shared ancestor
        // metadata. Production remains one attempt with ChangedDuringRead.
        let observe = |path: &RetainedDirectoryPath| {
            for _ in 0..256 {
                match path.observe_directories() {
                    Err(super::super::DescriptorObservationError::ChangedDuringRead) => {
                        std::thread::sleep(std::time::Duration::from_millis(1))
                    }
                    result => return result.unwrap(),
                }
            }
            panic!("no stable test observation of shared ancestors");
        };
        let f = Fixture::new();
        let retained = f.capture();
        fs::set_permissions(f.0.join("outer"), fs::Permissions::from_mode(0o702)).unwrap();
        let observed = observe(&retained);
        assert_eq!(observed.len(), retained.edges.len() + 1);
        for (sample, directory) in observed
            .iter()
            .zip(std::iter::once(&retained.root).chain(retained.edges.iter().map(|e| &e.directory)))
        {
            let m = directory.0.metadata().unwrap();
            assert_eq!(
                (
                    sample.metadata.device,
                    sample.metadata.inode,
                    sample.metadata.mode
                ),
                (m.dev(), m.ino(), m.mode())
            );
        }
        assert_eq!(observed[observed.len() - 2].metadata.mode & 0o777, 0o702);
        let moved = f.0.join("moved");
        fs::rename(f.0.join("outer"), &moved).unwrap();
        fs::create_dir_all(f.target()).unwrap();
        assert!(!retained.recheck().unwrap());
        // Observing the retained old descriptors must not silently follow new names.
        let after = observe(&retained);
        assert_eq!(
            after
                .iter()
                .map(|o| (o.metadata.device, o.metadata.inode))
                .collect::<Vec<_>>(),
            observed
                .iter()
                .map(|o| (o.metadata.device, o.metadata.inode))
                .collect::<Vec<_>>()
        );
        let root = RetainedDirectoryPath::open(Path::new("/"), 0).unwrap();
        assert_eq!(observe(&root).len(), 1);
    }
    #[cfg(target_os = "linux")]
    #[test]
    fn unsupported_acl_observation_never_returns_an_empty_success() {
        let root = RetainedDirectoryPath::open(Path::new("/"), 0).unwrap();
        assert!(matches!(
            root.observe_directories(),
            Err(super::super::DescriptorObservationError::UnsupportedPlatform)
        ));
    }
    #[cfg(target_os = "macos")]
    #[test]
    fn exact_path_names_reject_ancestor_and_leaf_case_changes() {
        for part in ["outer", "outer/inner"] {
            let f = Fixture::new();
            let retained = f.capture();
            assert!(retained.recheck_exact_names().unwrap());
            let old = f.0.join(part);
            let new = old.with_file_name(old.file_name().unwrap().to_str().unwrap().to_uppercase());
            fs::rename(&old, &new).unwrap();
            assert!(!retained.recheck_exact_names().unwrap());
            fs::rename(&new, &old).unwrap();
            // Restoration is observable; no claim to exclude an ABA history.
            assert!(retained.recheck_exact_names().unwrap());
        }
        assert!(
            RetainedDirectoryPath::open(Path::new("/"), 0)
                .unwrap()
                .recheck_exact_names()
                .unwrap()
        );
    }
    #[cfg(target_os = "macos")]
    #[test]
    fn exact_path_names_keep_inode_binding_after_equal_basename_relocation() {
        let f = Fixture::new();
        let retained = f.capture();
        fs::create_dir(f.0.join("old")).unwrap();
        fs::rename(f.0.join("outer"), f.0.join("old/outer")).unwrap();
        fs::create_dir_all(f.0.join("outer/inner")).unwrap();
        assert!(!retained.recheck_exact_names().unwrap());
    }
}
