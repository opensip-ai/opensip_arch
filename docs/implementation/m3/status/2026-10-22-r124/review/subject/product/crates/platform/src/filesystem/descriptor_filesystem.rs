//! Native samples of the filesystem containing an already retained descriptor.
//! No path lookup, profile admission, stable mount identity, or authority.
use std::{fs::File, io};

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct DescriptorFilesystem {
    name: [u8; 16],
    name_len: usize,
    device: u64,
    native_id: [i32; 2],
    type_code: u32,
    subtype: u32,
    flags: u32,
    local: bool,
    union: bool,
    read_only: bool,
}
impl DescriptorFilesystem {
    /// Exact bounded kernel type-name bytes, without its terminating NUL.
    pub fn name(&self) -> &[u8] {
        &self.name[..self.name_len]
    }
    /// Descriptor metadata device number; not a filesystem UUID/mount generation.
    pub fn device(&self) -> u64 {
        self.device
    }
    /// Native mounted-filesystem ID, sampled from fstatfs. Not a persistent UUID
    /// or mount generation; equality is scoped to held descriptors/this operation.
    /// APFS volume groups may share st_dev while these native IDs differ.
    pub fn native_id(&self) -> [i32; 2] {
        self.native_id
    }

    pub fn type_code(&self) -> u32 {
        self.type_code
    }
    pub fn subtype(&self) -> u32 {
        self.subtype
    }
    /// Native macOS mount flags, preserved without assigning authority.
    pub fn flags(&self) -> u32 {
        self.flags
    }
    pub fn is_local(&self) -> bool {
        self.local
    }
    pub fn is_union(&self) -> bool {
        self.union
    }
    pub fn is_read_only(&self) -> bool {
        self.read_only
    }
}
/// Sample the original open File. No duplication, pathname fallback, retry,
/// barrier or mutation. The result is a sample, not a coherent mount snapshot.
/// One status read and one `fstatfs`: the status and statfs output buffers.
pub fn descriptor_filesystem_observation_cost() -> crate::WorkCost {
    #[cfg(target_os = "macos")]
    let statfs = std::mem::size_of::<libc::statfs>();
    #[cfg(not(target_os = "macos"))]
    let statfs = 0;
    crate::WorkCost {
        objects: 1,
        edges: 2,
        bytes: statfs
            .saturating_add(super::path_binding::status_read_cost().bytes)
            .saturating_add(std::mem::size_of::<DescriptorFilesystem>()),
    }
}
/// `observe_filesystem`, charged to `work` first. A refusal keeps the charge.
pub fn observe_filesystem_accounted(
    file: &File,
    work: &mut crate::WorkScope<'_>,
) -> Result<DescriptorFilesystem, crate::WorkFailure<io::Error>> {
    work.run(descriptor_filesystem_observation_cost(), |_| {
        observe_filesystem(file).map_err(crate::WorkFailure::Operation)
    })
}
/// `observe_filesystem`, spending `descriptor_filesystem_observation_cost`
/// from an existing reservation first, with no second outer charge. A shortfall
/// or refusal closes the original operation.
pub fn observe_filesystem_reserved(
    file: &File,
    post: &mut crate::ReservedPostchecks<'_>,
) -> Result<DescriptorFilesystem, crate::WorkFailure<io::Error>> {
    post.scope(|post| {
        post.spend(descriptor_filesystem_observation_cost())?;
        observe_filesystem(file).map_err(crate::WorkFailure::Operation)
    })
}
pub fn observe_filesystem(file: &File) -> io::Result<DescriptorFilesystem> {
    #[cfg(target_os = "macos")]
    {
        observe_with(file, libc::fstatfs)
    }
    #[cfg(not(target_os = "macos"))]
    {
        let _ = file;
        Err(io::Error::new(
            io::ErrorKind::Unsupported,
            "native filesystem observer not implemented",
        ))
    }
}
#[cfg(target_os = "macos")]
fn observe_with(
    file: &File,
    call: unsafe extern "C" fn(libc::c_int, *mut libc::statfs) -> libc::c_int,
) -> io::Result<DescriptorFilesystem> {
    use std::os::{fd::AsRawFd, unix::fs::MetadataExt};
    let device = file.metadata()?.dev();
    let mut stat = std::mem::MaybeUninit::<libc::statfs>::uninit();
    // SAFETY: live original descriptor; correctly sized writable ABI storage.
    // Production uses fstatfs. Private test seam obeys the same pointer contract.
    if unsafe { call(file.as_raw_fd(), stat.as_mut_ptr()) } < 0 {
        return Err(io::Error::last_os_error());
    }
    // SAFETY: successful native call initialized its output struct.
    let stat = unsafe { stat.assume_init() };
    decode(&stat, device)
}
#[cfg(target_os = "macos")]
fn decode(stat: &libc::statfs, device: u64) -> io::Result<DescriptorFilesystem> {
    let mut name = [0; 16];
    let end = stat
        .f_fstypename
        .iter()
        .position(|b| *b == 0)
        .filter(|n| *n > 0)
        .ok_or_else(|| {
            io::Error::new(io::ErrorKind::InvalidData, "invalid filesystem type name")
        })?;
    for (out, input) in name[..end].iter_mut().zip(&stat.f_fstypename[..end]) {
        *out = *input as u8;
    }
    Ok(DescriptorFilesystem {
        name,
        name_len: end,
        device,
        // SAFETY: pinned macOS SDK fsid_t is exactly two int32_t values, and
        // libc's repr(C) fsid_t is exactly [i32;2] behind private fields. Both
        // types have identical size/alignment, no padding or invalid bit patterns;
        // successful fstatfs initialized the source. transmute checks the size.
        native_id: unsafe { std::mem::transmute::<libc::fsid_t, [i32; 2]>(stat.f_fsid) },
        type_code: stat.f_type,
        subtype: stat.f_fssubtype,
        flags: stat.f_flags,
        local: stat.f_flags & libc::MNT_LOCAL as u32 != 0,
        union: stat.f_flags & libc::MNT_UNION as u32 != 0,
        read_only: stat.f_flags & libc::MNT_RDONLY as u32 != 0,
    })
}
#[cfg(all(test, target_os = "macos"))]
mod tests {
    use super::*;
    #[test]
    fn observation_cost_counts_the_status_read_and_both_buffers() {
        let cost = descriptor_filesystem_observation_cost();
        assert_eq!(cost.edges, 2);
        assert!(
            cost.bytes
                >= std::mem::size_of::<libc::statfs>()
                    + std::mem::size_of::<libc::stat>()
                    + std::mem::size_of::<DescriptorFilesystem>()
        );
    }
    use crate::{FileLock, LockMode, RetainedDirectory, RetainedDirectoryPath};
    use std::{
        ffi::OsStr,
        fs,
        os::unix::fs::{MetadataExt, PermissionsExt},
        path::PathBuf,
    };
    fn stat(name: &[u8], flags: u32) -> libc::statfs {
        // SAFETY: statfs contains only integers and integer arrays; zero is valid.
        let mut s: libc::statfs = unsafe { std::mem::zeroed() };
        for (out, b) in s.f_fstypename.iter_mut().zip(name) {
            *out = *b as libc::c_char;
        }
        s.f_flags = flags;
        s.f_type = 23;
        s.f_fssubtype = 42;
        s
    }
    #[test]
    fn native_filesystem_bounded_name_flags_and_identity_are_observations() {
        let s = stat(b"apfs", (libc::MNT_LOCAL | libc::MNT_RDONLY) as u32);
        let got = decode(&s, 123).unwrap();
        assert_eq!(got.name(), b"apfs");
        assert_eq!(got.device(), 123);
        assert_eq!(got.type_code(), 23);
        assert_eq!(got.subtype(), 42);
        assert_eq!(got.flags(), (libc::MNT_LOCAL | libc::MNT_RDONLY) as u32);
        assert!(got.is_local());
        assert!(got.is_read_only());
        assert!(!got.is_union());
        for flags in [
            0,
            libc::MNT_UNION as u32,
            (libc::MNT_LOCAL | libc::MNT_UNION) as u32,
            0x80000000,
        ] {
            let got = decode(&stat(b"OtherFS", flags), 0).unwrap();
            assert_eq!(got.name(), b"OtherFS");
            assert_eq!(got.flags(), flags);
            assert_eq!(got.is_local(), flags & libc::MNT_LOCAL as u32 != 0);
            assert_eq!(got.is_union(), flags & libc::MNT_UNION as u32 != 0);
            assert!(!got.is_read_only());
        }
    }
    #[test]
    fn native_filesystem_name_decoder_rejects_empty_and_unterminated_without_normalizing() {
        assert_eq!(
            decode(&stat(b"", 0), 0).unwrap_err().kind(),
            io::ErrorKind::InvalidData
        );
        assert_eq!(
            decode(&stat(&[b'x'; 16], 0), 0).unwrap_err().kind(),
            io::ErrorKind::InvalidData
        );
        assert_eq!(
            decode(&stat(&[b'x'; 15], 0), 0).unwrap().name(),
            &[b'x'; 15]
        );
        assert_eq!(decode(&stat(b"APFS", 0), 0).unwrap().name(), b"APFS");
        assert_eq!(
            decode(&stat(&[0xff, b'x'], 0), 0).unwrap().name(),
            &[0xff, b'x']
        );
        let mut s = stat(b"apfs\0ignored", 0);
        let a = decode(&s, 1).unwrap();
        s.f_blocks = 1234;
        s.f_bfree = 456;
        s.f_files = 987;
        assert_eq!(a, decode(&s, 1).unwrap());
        assert_ne!(a, decode(&s, 2).unwrap());
    }
    #[test]
    fn native_filesystem_actual_root_child_and_full_path_observe_cross_mount_descriptors() {
        let root = RetainedDirectory::from_retained_handle(File::open("/").unwrap()).unwrap();
        let edge = root.bind_child_directory(OsStr::new("dev")).unwrap();
        let pair = edge.observe_filesystems().unwrap();
        assert_eq!(pair[0], root.observe_filesystem().unwrap());
        assert_eq!(pair[1], edge.directory().observe_filesystem().unwrap());
        assert_eq!(pair[1].name(), b"devfs");
        assert_ne!(pair[0].device(), pair[1].device());
        let path = RetainedDirectoryPath::open(std::path::Path::new("/dev"), 128).unwrap();
        assert_eq!(path.observe_filesystems().unwrap(), pair.to_vec());
        assert_eq!(pair[0].device(), fs::metadata("/").unwrap().dev());
        assert_eq!(pair[1].device(), fs::metadata("/dev").unwrap().dev());
    }
    #[test]
    fn native_filesystem_native_error_never_admits_even_initialized_output() {
        unsafe extern "C" fn failure(_: libc::c_int, out: *mut libc::statfs) -> libc::c_int {
            // SAFETY: private observer supplies valid aligned storage; initialize
            // plausible output before reporting failure to prove it is ignored.
            unsafe {
                out.write(stat(b"apfs", libc::MNT_LOCAL as u32));
                *libc::__error() = libc::EIO;
            }
            -1
        }
        let file = File::open("/dev").unwrap();
        assert_eq!(
            observe_with(&file, failure).unwrap_err().raw_os_error(),
            Some(libc::EIO)
        );
        assert_eq!(observe_filesystem(&file).unwrap().name(), b"devfs");
    }
    struct Fixture(PathBuf);
    impl Fixture {
        fn new() -> Self {
            let id: String = crate::request_entropy()
                .unwrap()
                .iter()
                .map(|b| format!("{b:02x}"))
                .collect();
            let p = std::env::temp_dir().join(format!("opensip-filesystem346-{id}"));
            fs::create_dir(&p).unwrap();
            fs::set_permissions(&p, fs::Permissions::from_mode(0o700)).unwrap();
            Self(fs::canonicalize(p).unwrap())
        }
    }
    impl Drop for Fixture {
        fn drop(&mut self) {
            let _ = fs::remove_dir_all(&self.0);
        }
    }
    #[test]
    fn native_filesystem_original_file_lock_and_all_path_components_stay_owned() {
        let f = Fixture::new();
        let leaf = f.0.join("carrier");
        fs::write(&leaf, b"original").unwrap();
        let file = File::open(&leaf).unwrap();
        let observed = observe_filesystem(&file).unwrap();
        assert_eq!(observed.device(), file.metadata().unwrap().dev());
        let lock = FileLock::try_acquire(file, LockMode::Exclusive)
            .unwrap()
            .unwrap();
        assert_eq!(lock.observe_filesystem().unwrap(), observed);
        assert!(
            FileLock::try_acquire(File::open(&leaf).unwrap(), LockMode::Exclusive)
                .unwrap()
                .is_none()
        );
        fs::rename(&leaf, f.0.join("moved")).unwrap();
        assert_eq!(lock.observe_filesystem().unwrap(), observed);
        let path = RetainedDirectoryPath::open(&f.0, 128).unwrap();
        let samples = path.observe_filesystems().unwrap();
        // The shared temp directory is an ancestor, and parallel tests change
        // it; a sample it changed under is refused, so retry only that case.
        let metadata = (0..8)
            .find_map(|_| match path.observe_directories() {
                Err(crate::DescriptorObservationError::ChangedDuringRead) => None,
                other => Some(other),
            })
            .expect("ancestors stayed unchanged for one sample")
            .unwrap();
        assert_eq!(samples.len(), metadata.len());
        assert!(samples.len() > 2);
        for (s, m) in samples.iter().zip(metadata) {
            assert_eq!(s.device(), m.metadata.device);
        }
        assert_eq!(samples.last().unwrap(), &observed);
        lock.release().unwrap();
        assert_eq!(fs::read(f.0.join("moved")).unwrap(), b"original");
    }
    #[test]
    fn native_filesystem_fsid_preserves_both_signed_words() {
        assert_eq!(std::mem::size_of::<libc::fsid_t>(), 8);
        assert_eq!(
            std::mem::align_of::<libc::fsid_t>(),
            std::mem::align_of::<[i32; 2]>()
        );
        for words in [[0, 0], [i32::MIN, i32::MAX], [-1, 26], [12345, -6789]] {
            let mut sample = stat(b"apfs", libc::MNT_LOCAL as u32);
            // SAFETY: same pinned two-int32 repr as the decode operation.
            sample.f_fsid = unsafe { std::mem::transmute::<[i32; 2], libc::fsid_t>(words) };
            let got = decode(&sample, 17).unwrap();
            assert_eq!(got.device(), 17);
            assert_eq!(got.native_id(), words);
        }
    }
    #[test]
    fn native_filesystem_actual_system_and_data_ids_are_observed_separately() {
        let system = RetainedDirectoryPath::open(std::path::Path::new("/"), 128)
            .unwrap()
            .directory()
            .observe_filesystem()
            .unwrap();
        let data = RetainedDirectoryPath::open(std::path::Path::new("/System/Volumes/Data"), 128)
            .unwrap()
            .directory()
            .observe_filesystem()
            .unwrap();
        assert_eq!(system.name(), b"apfs");
        assert_eq!(data.name(), b"apfs");
        assert_ne!(system.native_id(), data.native_id());
        println!(
            "system dev={} fsid={:?}; data dev={} fsid={:?}",
            system.device(),
            system.native_id(),
            data.device(),
            data.native_id()
        );
    }
}
