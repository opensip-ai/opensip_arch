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
// Internal operational paths reserve staging spellings. Native project roots
// have their own raw POSIX grammar; neither spelling profile grants custody.
#[derive(Clone, Copy)]
enum PathUse {
    Internal,
    ProjectRoot,
}
fn components(raw: &[u8], max_components: usize, usage: PathUse) -> io::Result<Vec<&[u8]>> {
    let internal = matches!(usage, PathUse::Internal);
    if !raw.starts_with(b"/")
        || raw.contains(&0)
        || (internal && raw.contains(&b'\\'))
        || (!internal && raw.len() > 4096)
    {
        return Err(io::Error::new(
            io::ErrorKind::InvalidInput,
            "invalid absolute directory path",
        ));
    }
    let mut parts = Vec::new();
    if raw != b"/" {
        for part in raw[1..].split(|b| *b == b'/') {
            if parts.len() == max_components
                || part.is_empty()
                || part == b"."
                || part == b".."
                || (internal && part.starts_with(STAGING_PREFIX.as_bytes()))
            {
                return Err(io::Error::new(
                    io::ErrorKind::InvalidInput,
                    "invalid or over-bound directory components",
                ));
            }
            parts.push(part);
        }
    }
    Ok(parts)
}
/// Upper bound on the child components of `raw`, counted without allocation:
/// each component follows one slash. The parser still refuses bad spellings.
fn component_bound(raw: &[u8]) -> usize {
    if raw == b"/" {
        0
    } else {
        raw.iter().filter(|byte| **byte == b'/').count()
    }
}
/// One status read: an edge and a buffer the size of the larger of the native
/// `stat` and `std::fs::Metadata`. Every kind check and identity comparison in
/// this module is one.
pub(super) fn status_read_cost() -> crate::WorkCost {
    crate::WorkCost {
        objects: 0,
        edges: 1,
        bytes: std::mem::size_of::<libc::stat>().max(std::mem::size_of::<std::fs::Metadata>()),
    }
}
/// `count` status reads.
fn status_reads(count: usize) -> crate::WorkCost {
    let one = status_read_cost();
    crate::WorkCost {
        objects: 0,
        edges: count,
        bytes: one.bytes.saturating_mul(count),
    }
}
fn sum(a: crate::WorkCost, b: crate::WorkCost) -> crate::WorkCost {
    crate::WorkCost {
        objects: a.objects.saturating_add(b.objects),
        edges: a.edges.saturating_add(b.edges),
        bytes: a.bytes.saturating_add(b.bytes),
    }
}
/// One `recheck` over `components` child edges: reopen the root and each child
/// (one temporary handle and one open each), a kind-check status read on each
/// reopened handle, and two status reads per identity comparison.
fn recheck_cost_for(components: usize) -> crate::WorkCost {
    let directories = components.saturating_add(1);
    sum(
        crate::WorkCost {
            objects: directories,
            edges: directories,
            bytes: 0,
        },
        status_reads(directories.saturating_mul(3)),
    )
}
/// Conservative caller-owned work for `open` on `path`, computed from the raw
/// bytes before any allocation or open. Objects: the root handle, one handle
/// per component, the component list, the edge vector and the closing
/// recheck's temporary handles. Edges: the root open and one open per
/// component, a kind-check status read on each retained handle, and the
/// closing recheck. Bytes: the component list, the edge vector, each
/// NUL-terminated name, and every status buffer. Opaque kernel work and
/// latency are not counted. Arithmetic saturates, so an absurd path is refused
/// by the ledger. No custody or authority.
pub fn retained_path_open_cost(path: &Path) -> crate::WorkCost {
    let raw = path.as_os_str().as_bytes();
    let components = component_bound(raw);
    let directories = components.saturating_add(1);
    let opened = crate::WorkCost {
        objects: directories.saturating_add(2),
        edges: directories,
        bytes: components
            .saturating_mul(std::mem::size_of::<&[u8]>() + std::mem::size_of::<Edge>() + 1)
            .saturating_add(raw.len()),
    };
    sum(
        sum(opened, status_reads(directories)),
        recheck_cost_for(components),
    )
}
/// `recheck_exact_names_cost` for a path of `components` child edges, known
/// before the path is opened: two rechecks and one native name sample per edge.
pub(crate) fn recheck_exact_names_cost_for(components: usize) -> crate::WorkCost {
    let recheck = recheck_cost_for(components);
    let name = super::directory_names::observation_cost();
    let names = crate::WorkCost {
        objects: name.objects.saturating_mul(components),
        edges: name.edges.saturating_mul(components),
        bytes: name.bytes.saturating_mul(components),
    };
    sum(sum(recheck, recheck), names)
}
impl RetainedDirectoryPath {
    /// `open`, charged to `work` for `retained_path_open_cost` before any
    /// allocation or open. A refusal keeps the charge.
    pub fn open_accounted(
        path: &Path,
        max_components: usize,
        work: &mut crate::WorkScope<'_>,
    ) -> Result<Self, crate::WorkFailure<io::Error>> {
        work.run(retained_path_open_cost(path), |_| {
            Self::open(path, max_components).map_err(crate::WorkFailure::Operation)
        })
    }
    /// Child components below the filesystem root.
    pub fn component_count(&self) -> usize {
        self.edges.len()
    }
    /// Visit every retained handle in root-to-leaf order with its index (0 is
    /// the filesystem root). No descriptor escapes the borrow; the first error
    /// stops the visit.
    pub fn visit_directories<E>(
        &self,
        mut visit: impl FnMut(usize, &RetainedDirectory) -> Result<(), E>,
    ) -> Result<(), E> {
        visit(0, &self.root)?;
        for (index, edge) in self.edges.iter().enumerate() {
            visit(index + 1, &edge.directory)?;
        }
        Ok(())
    }
    /// Visit every retained handle in leaf-to-root order with its index (0 is
    /// the filesystem root), for walks that run upward from a launch
    /// directory. No descriptor escapes the borrow; the first error, or a
    /// `false` from `visit`, stops the visit, and later handles are not seen.
    pub fn visit_directories_upward<E>(
        &self,
        mut visit: impl FnMut(usize, &RetainedDirectory) -> Result<bool, E>,
    ) -> Result<(), E> {
        for (index, edge) in self.edges.iter().enumerate().rev() {
            if !visit(index + 1, &edge.directory)? {
                return Ok(());
            }
        }
        visit(0, &self.root).map(|_| ())
    }
    /// The retained handle at `index` (0 is the filesystem root), if any.
    /// The borrow cannot outlive this path.
    pub fn directory_at(&self, index: usize) -> Option<&RetainedDirectory> {
        if index == 0 {
            Some(&self.root)
        } else {
            self.edges.get(index - 1).map(|edge| &edge.directory)
        }
    }
    /// Two rechecks and one native name sample per child edge.
    pub fn recheck_exact_names_cost(&self) -> crate::WorkCost {
        recheck_exact_names_cost_for(self.edges.len())
    }
    /// `recheck_exact_names`, charged to `work` first. False is a changed or
    /// missing name, not a policy decision.
    pub fn recheck_exact_names_accounted(
        &self,
        work: &mut crate::WorkScope<'_>,
    ) -> Result<bool, crate::WorkFailure<io::Error>> {
        work.run(self.recheck_exact_names_cost(), |_| {
            self.recheck_exact_names()
                .map_err(crate::WorkFailure::Operation)
        })
    }
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
    /// Retain a native project root using raw POSIX spelling: absolute, at most
    /// 4096 bytes, no NUL, empty/dot components or trailing slash except root.
    /// Backslashes and internal staging-like names are ordinary project names.
    /// The bytes are never normalized and every open still refuses symlinks.
    /// This is sampled name/descriptor evidence only. The caller still owes
    /// shared-budget precharging, exact-name/filesystem/custody admission and
    /// operation exclusion; syntax does not promise the OS accepts every path.
    pub fn open_project_root(path: &Path, max_components: usize) -> io::Result<Self> {
        Self::open_for(path, max_components, PathUse::ProjectRoot, || {})
    }
    // Private sequencing seam; cannot supply or replace a retained descriptor.
    fn open_inner(
        path: &Path,
        max_components: usize,
        after_retention: impl FnOnce(),
    ) -> io::Result<Self> {
        Self::open_for(path, max_components, PathUse::Internal, after_retention)
    }
    fn open_for(
        path: &Path,
        max_components: usize,
        usage: PathUse,
        after_retention: impl FnOnce(),
    ) -> io::Result<Self> {
        let parts = components(path.as_os_str().as_bytes(), max_components, usage)?;
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
    #[test]
    fn accounted_open_and_name_recheck_charge_their_published_cost() {
        let f = Fixture::new();
        let target = f.target();
        let open = retained_path_open_cost(&target);
        let components = target
            .as_os_str()
            .as_bytes()
            .iter()
            .filter(|b| **b == b'/')
            .count();
        assert_eq!(open.edges, 6 * components + 6);
        let mut ledger = crate::WorkLedger::new();
        let path = ledger
            .scope(|work| RetainedDirectoryPath::open_accounted(&target, 128, work))
            .unwrap();
        assert_eq!(ledger.used(), open);
        assert_eq!(path.component_count(), components);
        let mut seen = Vec::new();
        path.visit_directories(|index, _| {
            seen.push(index);
            Ok::<_, ()>(())
        })
        .unwrap();
        assert_eq!(seen, (0..=components).collect::<Vec<_>>());
        let recheck = path.recheck_exact_names_cost();
        #[cfg(target_os = "macos")]
        {
            assert!(
                ledger
                    .scope(|work| path.recheck_exact_names_accounted(work))
                    .unwrap()
            );
            assert_eq!(ledger.used(), open.checked_add(recheck).unwrap());
        }
        let mut tight = crate::WorkLedger::with_limits(crate::WorkCost {
            edges: open.edges - 1,
            ..open
        })
        .unwrap();
        assert!(matches!(
            tight.scope(|work| RetainedDirectoryPath::open_accounted(&target, 128, work)),
            Err(crate::WorkFailure::Budget(_))
        ));
        let root = retained_path_open_cost(Path::new("/"));
        // The root open, its kind check, the recheck reopen, its kind check, and
        // two comparison reads.
        assert_eq!((root.objects, root.edges), (4, 6));
        // Four status buffers and the one raw path byte.
        assert_eq!(root.bytes, 4 * status_read_cost().bytes + 1);
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
    fn project_root_keeps_raw_names_without_relaxing_internal_staging_rules() {
        let f = Fixture::new();
        for name in ["literal\\backslash", ".opensip-stage-project"] {
            let path = f.0.join(name);
            fs::create_dir(&path).unwrap();
            fs::write(path.join("witness"), b"old").unwrap();
            assert_eq!(
                RetainedDirectoryPath::open(&path, 128)
                    .err()
                    .unwrap()
                    .kind(),
                io::ErrorKind::InvalidInput
            );
            let held = RetainedDirectoryPath::open_project_root(&path, 128).unwrap();
            assert!(held.recheck().unwrap());
            #[cfg(target_os = "macos")]
            assert!(held.recheck_exact_names().unwrap());
            assert_eq!(read_witness(&held), b"old");
            fs::rename(&path, f.0.join("moved-project")).unwrap();
            assert!(!held.recheck().unwrap());
            fs::create_dir(&path).unwrap();
            fs::write(path.join("witness"), b"new").unwrap();
            assert!(!held.recheck().unwrap());
            assert_eq!(read_witness(&held), b"old");
            fs::remove_dir_all(f.0.join("moved-project")).unwrap();
        }
    }
    #[test]
    fn project_root_grammar_is_byte_bounded_and_does_not_normalize() {
        for raw in [
            b"" as &[u8],
            b"relative",
            b"//",
            b"/a//b",
            b"/a/./b",
            b"/a/../b",
            b"/a/",
            b"/a\0b",
        ] {
            assert_eq!(
                components(raw, 128, PathUse::ProjectRoot)
                    .err()
                    .unwrap()
                    .kind(),
                io::ErrorKind::InvalidInput
            );
        }
        assert_eq!(components(b"/", 0, PathUse::ProjectRoot).unwrap().len(), 0);
        let exact = [b"/" as &[u8], &vec![b'x'; 4095]].concat();
        assert_eq!(
            components(&exact, 1, PathUse::ProjectRoot).unwrap(),
            [&exact[1..]]
        );
        let mut over = exact;
        over.push(b'x');
        assert!(components(&over, 1, PathUse::ProjectRoot).is_err());
        let raw = b"/raw-\xff/literal\\name";
        assert_eq!(
            components(raw, 2, PathUse::ProjectRoot).unwrap(),
            [&raw[1..6], &raw[7..]]
        );
        assert!(components(raw, 1, PathUse::ProjectRoot).is_err());
    }
    #[test]
    fn project_root_retention_keeps_symlink_and_mid_capture_relocation_refusals() {
        let f = Fixture::new();
        let held = RetainedDirectoryPath::open_project_root(&f.target(), 128).unwrap();
        fs::rename(f.0.join("outer"), f.0.join("moved")).unwrap();
        symlink(f.0.join("moved"), f.0.join("outer")).unwrap();
        assert!(!held.recheck().unwrap());
        assert!(RetainedDirectoryPath::open_project_root(&f.target(), 128).is_err());
        fs::remove_file(f.0.join("outer")).unwrap();
        fs::rename(f.0.join("moved"), f.0.join("outer")).unwrap();
        let result =
            RetainedDirectoryPath::open_for(&f.target(), 128, PathUse::ProjectRoot, || {
                fs::rename(f.0.join("outer"), f.0.join("moved")).unwrap();
                fs::create_dir_all(f.target()).unwrap();
            });
        assert_eq!(result.err().unwrap().kind(), io::ErrorKind::InvalidData);
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
