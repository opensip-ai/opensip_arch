//! Streaming OS entry names under a retained directory. This is not a stable
//! snapshot, path custody, file admission, or a complete trust successor census.
//! Callers must hold the appropriate exclusion and charge their shared operation
//! budget in the visitor BEFORE cloning a name or opening/materializing its file.
//! All returned names (including dot entries and non-UTF8 names) reach the visitor.
//! No d_type/inode hint is used to skip or authenticate a candidate.
use super::RetainedDirectory;
use std::fs::File;
use std::io;
use std::os::fd::{AsRawFd, FromRawFd};
use std::ptr::NonNull;

#[derive(Debug)]
pub enum DirectoryVisitError<E> {
    Native(io::Error),
    InvalidLimits,
    EntryLimit,
    NameByteLimit,
    Visitor(E),
}
/// Counts only this completed stream, including dot entries if the OS returned
/// them. EOF does not establish stability under concurrent directory mutation.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct DirectoryVisitSummary {
    entries: usize,
    name_bytes: usize,
}
impl DirectoryVisitSummary {
    pub fn entries(&self) -> usize {
        self.entries
    }
    pub fn name_bytes(&self) -> usize {
        self.name_bytes
    }
}
const MAX_ENTRIES: usize = 131_072;
const MAX_NAME_BYTES: usize = 268_435_456;
fn limits<E>(entries: usize, bytes: usize) -> Result<(), DirectoryVisitError<E>> {
    if entries > MAX_ENTRIES || bytes > MAX_NAME_BYTES {
        Err(DirectoryVisitError::InvalidLimits)
    } else {
        Ok(())
    }
}
trait Entries {
    fn next(&mut self) -> io::Result<Option<&[u8]>>;
}
fn visit<E>(
    stream: &mut impl Entries,
    max_entries: usize,
    max_name_bytes: usize,
    visitor: &mut impl FnMut(&[u8]) -> Result<(), E>,
) -> Result<DirectoryVisitSummary, DirectoryVisitError<E>> {
    let mut summary = DirectoryVisitSummary {
        entries: 0,
        name_bytes: 0,
    };
    while let Some(name) = stream.next().map_err(DirectoryVisitError::Native)? {
        // Borrowed libc/kernel record already exists in the bounded stream
        // buffer. No Rust name allocation or entry open precedes these checks.
        if summary.entries == max_entries {
            return Err(DirectoryVisitError::EntryLimit);
        }
        if name.len() > max_name_bytes - summary.name_bytes {
            return Err(DirectoryVisitError::NameByteLimit);
        }
        summary.entries += 1;
        summary.name_bytes += name.len();
        visitor(name).map_err(DirectoryVisitError::Visitor)?;
    }
    Ok(summary)
}
impl RetainedDirectory {
    /// Start an independent handle-relative stream and visit borrowed OS name
    /// bytes. Zero limits are allowed but refuse any returned entry. The local
    /// limits are hard ceilings, not a substitute for the shared caller budget.
    /// This does not sort, deduplicate, follow symlinks, open entries, or publish.
    /// Visitor error, native error, limits, and close failure cannot return a
    /// completed summary. On failure previously visited names must not be used
    /// as a complete census. No implicit retry or rewind occurs.
    pub fn visit_entry_names<E>(
        &self,
        max_entries: usize,
        max_name_bytes: usize,
        mut visitor: impl FnMut(&[u8]) -> Result<(), E>,
    ) -> Result<DirectoryVisitSummary, DirectoryVisitError<E>> {
        limits(max_entries, max_name_bytes)?;
        let mut stream = NativeEntries::open(&self.0).map_err(DirectoryVisitError::Native)?;
        let summary = visit(&mut stream, max_entries, max_name_bytes, &mut visitor)?;
        stream.close().map_err(DirectoryVisitError::Native)?;
        Ok(summary)
    }
}
struct NativeEntries {
    stream: Option<NonNull<libc::DIR>>,
}
impl NativeEntries {
    fn open(parent: &File) -> io::Result<Self> {
        // SAFETY: parent owns a live directory descriptor. The literal is one
        // NUL-terminated component; openat creates a NEW open file description,
        // unlike dup/try_clone which would share a mutable directory offset.
        let fd = unsafe {
            libc::openat(
                parent.as_raw_fd(),
                c".".as_ptr(),
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
        // SAFETY: successful openat returns a uniquely owned descriptor.
        let file = unsafe { File::from_raw_fd(fd) };
        check_stream_filesystem(&file)?;
        // SAFETY: file owns a fresh readable directory descriptor. fdopendir
        // takes ownership only on success; on failure File still closes it.
        let ptr = unsafe { libc::fdopendir(file.as_raw_fd()) };
        let stream = NonNull::new(ptr).ok_or_else(io::Error::last_os_error)?;
        std::mem::forget(file);
        Ok(Self {
            stream: Some(stream),
        })
    }
    fn close(&mut self) -> io::Result<()> {
        self.close_with(libc::closedir)
    }
    fn close_with(
        &mut self,
        close: unsafe extern "C" fn(*mut libc::DIR) -> libc::c_int,
    ) -> io::Result<()> {
        let Some(stream) = self.stream.take() else {
            return Ok(());
        };
        // SAFETY: this unique live stream has no outstanding borrowed name.
        // Consume it exactly once; never retry a close even after native error.
        if unsafe { close(stream.as_ptr()) } < 0 {
            Err(io::Error::last_os_error())
        } else {
            Ok(())
        }
    }
}
impl Drop for NativeEntries {
    fn drop(&mut self) {
        let _ = self.close();
    }
}
fn errno_ptr() -> *mut libc::c_int {
    #[cfg(target_os = "macos")]
    // SAFETY: libc returns the calling thread's valid errno cell.
    unsafe {
        libc::__error()
    }
    #[cfg(target_os = "linux")]
    // SAFETY: libc returns the calling thread's valid errno cell.
    unsafe {
        libc::__errno_location()
    }
}
fn check_stream_filesystem(file: &File) -> io::Result<()> {
    #[cfg(target_os = "macos")]
    {
        let stat = super::observe_filesystem(file)?;
        // Apple's fdopendir may materialize an entire union directory before
        // returning. Refuse that mode before entering libc's directory reader.
        check_mount_flags(stat.flags())?;
    }
    #[cfg(target_os = "linux")]
    let _ = file;
    Ok(())
}
#[cfg(target_os = "macos")]
fn check_mount_flags(flags: u32) -> io::Result<()> {
    if flags & libc::MNT_UNION as u32 != 0 {
        Err(io::Error::new(
            io::ErrorKind::Unsupported,
            "union directory streaming is not bounded",
        ))
    } else {
        Ok(())
    }
}
impl Entries for NativeEntries {
    fn next(&mut self) -> io::Result<Option<&[u8]>> {
        self.next_with(libc::readdir)
    }
}
impl NativeEntries {
    // Private fault seam; read must obey the same borrowed-record/null+errno
    // contract as libc::readdir. Production always passes libc::readdir.
    fn next_with(
        &mut self,
        read: unsafe extern "C" fn(*mut libc::DIR) -> *mut libc::dirent,
    ) -> io::Result<Option<&[u8]>> {
        let stream = self.stream.ok_or_else(|| {
            io::Error::new(io::ErrorKind::InvalidInput, "closed directory stream")
        })?;
        // SAFETY: thread-local errno cell; reset immediately before readdir to
        // distinguish EOF from failure, including after an errno-setting visitor.
        unsafe {
            *errno_ptr() = 0;
        }
        // SAFETY: exclusively borrowed, live stream. The returned record is
        // borrowed only until the next call on this stream or its close.
        let entry = unsafe { read(stream.as_ptr()) };
        if entry.is_null() {
            let error = io::Error::last_os_error();
            return if error.raw_os_error() == Some(0) {
                Ok(None)
            } else {
                Err(error)
            };
        }
        // SAFETY: readdir supplies a valid native dirent header. Read just the
        // fixed header field, not a reference spanning the variable-size record.
        let record_len = unsafe { (*entry).d_reclen as usize };
        let offset = std::mem::offset_of!(libc::dirent, d_name);
        let available = record_len.checked_sub(offset).ok_or_else(bad_name)?;
        #[cfg(target_os = "macos")]
        let cap = 1024;
        #[cfg(target_os = "linux")]
        let cap = 256;
        let len = available.min(cap);
        // SAFETY: readdir guarantees a live record of d_reclen bytes. The slice
        // stays within that record and the supported platform name bound. It
        // does not form a reference to the entire nominal libc::dirent struct.
        let bytes = unsafe {
            std::slice::from_raw_parts(std::ptr::addr_of!((*entry).d_name).cast::<u8>(), len)
        };
        let end = bytes.iter().position(|b| *b == 0).ok_or_else(bad_name)?;
        if end == 0 || bytes[..end].contains(&b'/') {
            return Err(bad_name());
        }
        #[cfg(target_os = "macos")]
        // SAFETY: d_namlen is in the valid fixed header supplied by readdir.
        if unsafe { (*entry).d_namlen as usize } != end {
            return Err(bad_name());
        }
        Ok(Some(&bytes[..end]))
    }
}
fn bad_name() -> io::Error {
    io::Error::new(
        io::ErrorKind::InvalidData,
        "invalid native directory entry name",
    )
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::collections::BTreeSet;
    use std::os::unix::fs::symlink;
    use std::path::PathBuf;
    struct Fixture {
        root: PathBuf,
    }
    impl Fixture {
        fn new() -> Self {
            let mut random = [0u8; 16];
            getrandom::fill(&mut random).unwrap();
            let name: String = random.iter().map(|b| format!("{b:02x}")).collect();
            let root = std::env::temp_dir().join(format!("opensip-directory-visit-{name}"));
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
    fn names(d: &RetainedDirectory) -> (DirectoryVisitSummary, BTreeSet<Vec<u8>>) {
        let mut names = BTreeSet::new();
        let summary = d
            .visit_entry_names(10_000, 1_000_000, |n| {
                assert!(names.insert(n.to_vec()));
                Ok::<_, ()>(())
            })
            .unwrap();
        assert_eq!(summary.entries(), names.len());
        assert_eq!(
            summary.name_bytes(),
            names.iter().map(Vec::len).sum::<usize>()
        );
        (summary, names)
    }
    struct Fake {
        rows: Vec<Result<Vec<u8>, io::ErrorKind>>,
        next: usize,
    }
    impl Entries for Fake {
        fn next(&mut self) -> io::Result<Option<&[u8]>> {
            let row = self.rows.get(self.next);
            self.next += 1;
            match row {
                None => Ok(None),
                Some(Ok(b)) => Ok(Some(b)),
                Some(Err(kind)) => Err(io::Error::from(*kind)),
            }
        }
    }
    fn fake() -> Fake {
        Fake {
            rows: vec![
                Ok(b".".to_vec()),
                Ok(b"..".to_vec()),
                Ok(vec![0xff, 0xfe]),
                Ok(b"foreign".to_vec()),
            ],
            next: 0,
        }
    }
    #[test]
    fn directory_visit_limits_charge_every_raw_name_before_visitor() {
        for max in 0..4 {
            let mut f = fake();
            let mut seen = Vec::new();
            assert!(matches!(
                visit(&mut f, max, 100, &mut |n| {
                    seen.push(n.to_vec());
                    Ok::<_, ()>(())
                }),
                Err(DirectoryVisitError::EntryLimit)
            ));
            assert_eq!(seen.len(), max);
            assert_eq!(f.next, max + 1);
        }
        for max in 0..12 {
            let mut f = fake();
            let mut used = 0;
            let result = visit(&mut f, 4, max, &mut |n| {
                used += n.len();
                Ok::<_, ()>(())
            });
            assert!(matches!(result, Err(DirectoryVisitError::NameByteLimit)));
            assert!(used <= max);
        }
        let mut f = fake();
        let mut seen = Vec::new();
        let summary = visit(&mut f, 4, 12, &mut |n| {
            seen.push(n.to_vec());
            Ok::<_, ()>(())
        })
        .unwrap();
        assert_eq!(
            summary,
            DirectoryVisitSummary {
                entries: 4,
                name_bytes: 12
            }
        );
        assert_eq!(seen[2], vec![0xff, 0xfe]);
        assert_eq!(f.next, 5);
    }
    #[test]
    fn directory_visit_errors_never_return_partial_completion() {
        let mut f = fake();
        let mut calls = 0;
        assert!(matches!(
            visit(&mut f, 4, 12, &mut |_| {
                calls += 1;
                Err::<(), _>("shared budget exhausted")
            }),
            Err(DirectoryVisitError::Visitor("shared budget exhausted"))
        ));
        assert_eq!(calls, 1);
        assert_eq!(f.next, 1);
        let mut f = Fake {
            rows: vec![
                Ok(b"valid".to_vec()),
                Err(io::ErrorKind::PermissionDenied),
                Ok(b"unseen".to_vec()),
            ],
            next: 0,
        };
        let mut seen = Vec::new();
        assert!(
            matches!(visit(&mut f,4,100,&mut|n|{seen.push(n.to_vec());Ok::<_,()>(())}),Err(DirectoryVisitError::Native(e))if e.kind()==io::ErrorKind::PermissionDenied)
        );
        assert_eq!(seen, vec![b"valid".to_vec()]);
        assert_eq!(f.next, 2);
        assert!(matches!(
            limits::<()>(MAX_ENTRIES + 1, 1),
            Err(DirectoryVisitError::InvalidLimits)
        ));
        assert!(matches!(
            limits::<()>(1, MAX_NAME_BYTES + 1),
            Err(DirectoryVisitError::InvalidLimits)
        ));
    }
    #[test]
    fn directory_visit_native_keeps_all_entry_kinds_and_independent_offsets() {
        let f = Fixture::new();
        std::fs::write(f.root.join("regular"), b"payload").unwrap();
        std::fs::create_dir(f.root.join("subdirectory")).unwrap();
        symlink("nonexistent-target", f.root.join("symlink")).unwrap();
        let fifo =
            std::ffi::CString::new(f.root.join("fifo").as_os_str().as_encoded_bytes()).unwrap();
        // SAFETY: live NUL-terminated test-owned path, mode-only FIFO creation.
        assert_eq!(unsafe { libc::mkfifo(fifo.as_ptr(), 0o600) }, 0);
        for i in 0..512 {
            std::fs::write(f.root.join(format!("{:064x}-entry-{i}", i)), b"").unwrap();
        }
        let d = f.retained();
        let (summary, expected) = names(&d);
        for n in ["regular", "subdirectory", "symlink", "fifo"] {
            assert!(expected.contains(n.as_bytes()));
        }
        assert!(expected.contains(b".".as_slice()));
        assert!(expected.contains(b"..".as_slice()));
        assert_eq!(summary.entries(), 518);
        let mut outer = BTreeSet::new();
        let mut nested = false;
        let got = d
            .visit_entry_names(1000, 100_000, |name| {
                assert!(outer.insert(name.to_vec()));
                if !nested {
                    nested = true;
                    assert_eq!(names(&d).1, expected);
                }
                // SAFETY: this thread owns its errno cell. Successful EOF must not
                // mistake a visitor's unrelated errno for a readdir error.
                unsafe {
                    *errno_ptr() = libc::EACCES;
                }
                Ok::<_, ()>(())
            })
            .unwrap();
        assert_eq!(got, summary);
        assert_eq!(outer, expected);
        assert_eq!(names(&d).1, expected);
        assert_eq!(std::fs::read(f.root.join("regular")).unwrap(), b"payload");
        assert!(
            std::fs::symlink_metadata(f.root.join("symlink"))
                .unwrap()
                .file_type()
                .is_symlink()
        );
    }
    #[test]
    fn directory_visit_native_limits_stop_before_extra_callback_and_allow_fresh_stream() {
        let f = Fixture::new();
        std::fs::write(f.root.join("first"), b"").unwrap();
        std::fs::write(f.root.join("second"), b"").unwrap();
        let d = f.retained();
        let (summary, expected) = names(&d);
        let mut callbacks = 0;
        assert!(matches!(
            d.visit_entry_names(1, 100, |_| {
                callbacks += 1;
                Ok::<_, ()>(())
            }),
            Err(DirectoryVisitError::EntryLimit)
        ));
        assert_eq!(callbacks, 1);
        assert!(matches!(
            d.visit_entry_names(100, 0, |_| panic!("zero-byte limit called visitor")),
            Err::<DirectoryVisitSummary, DirectoryVisitError<()>>(
                DirectoryVisitError::NameByteLimit
            )
        ));
        assert!(matches!(
            d.visit_entry_names(MAX_ENTRIES + 1, 1, |_| panic!(
                "invalid limit called visitor"
            )),
            Err::<DirectoryVisitSummary, DirectoryVisitError<()>>(
                DirectoryVisitError::InvalidLimits
            )
        ));
        let exact = d
            .visit_entry_names(summary.entries(), summary.name_bytes(), |_| Ok::<_, ()>(()))
            .unwrap();
        assert_eq!(exact, summary);
        assert_eq!(names(&d).1, expected);
    }
    #[test]
    fn directory_visit_native_uses_retained_directory_after_name_replacement() {
        let f = Fixture::new();
        let original = f.root.join("chosen");
        std::fs::create_dir(&original).unwrap();
        std::fs::write(original.join("old"), b"").unwrap();
        let d = RetainedDirectory::from_retained_handle(File::open(&original).unwrap()).unwrap();
        std::fs::rename(&original, f.root.join("renamed")).unwrap();
        std::fs::create_dir(&original).unwrap();
        std::fs::write(original.join("decoy"), b"").unwrap();
        let got = names(&d).1;
        assert!(got.contains(b"old".as_slice()));
        assert!(!got.contains(b"decoy".as_slice()));
    }
    #[test]
    fn directory_visit_native_visitor_error_and_panic_release_only_the_stream() {
        let f = Fixture::new();
        std::fs::write(f.root.join("entry"), b"").unwrap();
        let d = f.retained();
        let expected = names(&d).1;
        assert!(matches!(
            d.visit_entry_names(100, 1000, |_| Err::<(), _>(42)),
            Err(DirectoryVisitError::Visitor(42))
        ));
        assert_eq!(names(&d).1, expected);
        assert!(
            std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| {
                let _ = d.visit_entry_names::<()>(100, 1000, |_| panic!("test visitor panic"));
            }))
            .is_err()
        );
        assert_eq!(names(&d).1, expected);
        let mut stream = NativeEntries::open(&d.0).unwrap();
        stream.close().unwrap();
        stream.close().unwrap();
        assert!(stream.next().is_err());
        assert_eq!(names(&d).1, expected);
    }
    #[test]
    fn directory_visit_native_error_and_close_failure_are_not_eof_or_success() {
        #[cfg(target_os = "macos")]
        {
            assert!(check_mount_flags(0).is_ok());
            assert_eq!(
                check_mount_flags(libc::MNT_UNION as u32)
                    .unwrap_err()
                    .kind(),
                io::ErrorKind::Unsupported
            );
            assert_eq!(
                check_mount_flags((libc::MNT_UNION | libc::MNT_LOCAL) as u32)
                    .unwrap_err()
                    .kind(),
                io::ErrorKind::Unsupported
            );
        }
        unsafe extern "C" fn read_error(_: *mut libc::DIR) -> *mut libc::dirent {
            // SAFETY: calling thread owns this valid errno cell.
            unsafe {
                *errno_ptr() = libc::EIO;
            }
            std::ptr::null_mut()
        }
        unsafe extern "C" fn close_error(d: *mut libc::DIR) -> libc::c_int {
            // SAFETY: the test passes the unique live stream; close it once,
            // then simulate a reported native close failure without leaking it.
            assert_eq!(unsafe { libc::closedir(d) }, 0);
            // SAFETY: calling thread owns this valid errno cell.
            unsafe {
                *errno_ptr() = libc::EIO;
            }
            -1
        }
        let f = Fixture::new();
        let d = f.retained();
        let mut s = NativeEntries::open(&d.0).unwrap();
        assert_eq!(
            s.next_with(read_error).unwrap_err().raw_os_error(),
            Some(libc::EIO)
        );
        assert_eq!(
            s.close_with(close_error).unwrap_err().raw_os_error(),
            Some(libc::EIO)
        );
        // Taking ownership before the failing close prevents retry/double-close.
        assert!(s.stream.is_none());
        s.close().unwrap();
        assert!(s.next().is_err());
        assert_eq!(names(&d).0.entries(), 2);
    }
    #[cfg(target_os = "linux")]
    #[test]
    fn directory_visit_native_linux_preserves_non_utf8_names() {
        use std::os::unix::ffi::OsStrExt;
        let f = Fixture::new();
        let raw = [0xff, 0xfe, b'x'];
        std::fs::write(f.root.join(std::ffi::OsStr::from_bytes(&raw)), b"").unwrap();
        assert!(names(&f.retained()).1.contains(raw.as_slice()));
    }
}
