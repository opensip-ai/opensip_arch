//! Admission of inherited harness descriptor 3.
//! Law M3-O1 item 2 and S-OP-2b item 4. This is the mechanism only:
//! the host decides when to call it.

use std::fs::File;
use std::io;
use std::os::fd::FromRawFd;

/// Descriptor the harness driver inherits to the host.
pub const HARNESS_DESCRIPTOR: i32 = 3;

/// The inherited descriptor is not a writable FIFO or regular file.
#[derive(Debug)]
pub enum HarnessDescriptorError {
    /// `fstat` failed. A closed descriptor is `EBADF`.
    Unavailable(io::Error),
    /// Not a FIFO and not a regular file. A directory is this refusal.
    WrongType,
    /// Open, but `O_ACCMODE` is not write-only or read-write.
    NotWritable,
    /// `fcntl` failed while reading or setting the status flags.
    Flag(io::Error),
}
impl std::fmt::Display for HarnessDescriptorError {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::Unavailable(source) => write!(formatter, "harness descriptor: {source}"),
            Self::WrongType => {
                write!(
                    formatter,
                    "harness descriptor is not a fifo or a regular file"
                )
            }
            Self::NotWritable => write!(formatter, "harness descriptor is not writable"),
            Self::Flag(source) => write!(formatter, "harness descriptor flags: {source}"),
        }
    }
}
impl std::error::Error for HarnessDescriptorError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            Self::Unavailable(source) | Self::Flag(source) => Some(source),
            Self::WrongType | Self::NotWritable => None,
        }
    }
}

/// Admit descriptor 3 when it is an open writable FIFO or regular file.
/// Sets close-on-exec on that descriptor and returns a new close-on-exec
/// duplicate. The file owns only the duplicate, so another call cannot alias
/// it. Failure leaves descriptor 3 unowned.
pub fn admit_harness_descriptor() -> Result<File, HarnessDescriptorError> {
    // SAFETY: stat is a plain integer struct. Zero is a value fstat overwrites.
    let mut info: libc::stat = unsafe { std::mem::zeroed() };
    // SAFETY: info is a live writable stat, and the descriptor number is the fixed harness channel.
    let stated = unsafe { libc::fstat(HARNESS_DESCRIPTOR, &mut info) };
    if stated != 0 {
        return Err(HarnessDescriptorError::Unavailable(
            io::Error::last_os_error(),
        ));
    }
    let kind = info.st_mode & libc::S_IFMT;
    if kind != libc::S_IFIFO && kind != libc::S_IFREG {
        return Err(HarnessDescriptorError::WrongType);
    }
    // SAFETY: F_GETFL reads the status flags of the fixed descriptor.
    let flags = unsafe { libc::fcntl(HARNESS_DESCRIPTOR, libc::F_GETFL) };
    if flags < 0 {
        return Err(HarnessDescriptorError::Flag(io::Error::last_os_error()));
    }
    let access = flags & libc::O_ACCMODE;
    if access != libc::O_WRONLY && access != libc::O_RDWR {
        return Err(HarnessDescriptorError::NotWritable);
    }
    // SAFETY: F_SETFD replaces the descriptor flags of the inherited channel with close-on-exec.
    let set = unsafe { libc::fcntl(HARNESS_DESCRIPTOR, libc::F_SETFD, libc::FD_CLOEXEC) };
    if set < 0 {
        return Err(HarnessDescriptorError::Flag(io::Error::last_os_error()));
    }
    // SAFETY: F_DUPFD_CLOEXEC returns a new descriptor. No other owner holds it,
    // and descriptor 3 stays open as the inherited channel.
    let owned = unsafe { libc::fcntl(HARNESS_DESCRIPTOR, libc::F_DUPFD_CLOEXEC, 0) };
    if owned < 0 {
        return Err(HarnessDescriptorError::Flag(io::Error::last_os_error()));
    }
    // SAFETY: `owned` is a fresh descriptor from the call above.
    Ok(unsafe { File::from_raw_fd(owned) })
}

#[cfg(test)]
mod tests {
    use std::fs::{self, File, OpenOptions};
    use std::io::Write;
    use std::os::fd::{AsRawFd, FromRawFd, OwnedFd};
    use std::os::unix::ffi::OsStrExt;
    use std::path::PathBuf;
    use std::sync::atomic::{AtomicU64, Ordering};

    use super::{HarnessDescriptorError, admit_harness_descriptor};

    use std::os::unix::fs::MetadataExt;
    use std::os::unix::process::CommandExt;

    const FD3_CASE: &str = "harness_descriptor::tests::admit_harness_descriptor_refuses_closed_readonly_and_directory_and_sets_cloexec";
    const FD3_PROBE: &str = "harness_descriptor::tests::an_ordinary_owned_descriptor_survives_fd3_checks";
    const FD3_CHILD: &str = "opensip-internal-fd3-child-only";

    // Descriptor 3 belongs to the entire process. Mutating it in a normal
    // test worker can close another parallel worker's owned File. Reexecute
    // the actual kernel checks in a separate program image, with one exact
    // test selected; do not serialize or weaken the ordinary platform suite.
    fn isolated_fd3_case(case: &str, inherited: Option<i32>) -> bool {
        let args: Vec<_> = std::env::args_os().collect();
        if args.windows(2).any(|a| a[0] == "--exact" && a[1] == case)
            && args.windows(2).any(|a| a[0] == "--skip" && a[1] == FD3_CHILD)
            && args.iter().any(|a| a == "--test-threads=1")
        {
            return false;
        }
        let mut command = std::process::Command::new(std::env::current_exe().unwrap());
        command.args(["--exact", case, "--test-threads=1", "--nocapture", "--skip", FD3_CHILD]);
        if let Some(source) = inherited {
            // SAFETY: only the child's fd table is changed after fork; the
            // source stays alive in the parent through output(). The calls
            // below are async-signal-safe. Exec discards the old Rust owners.
            unsafe {
                command.pre_exec(move || {
                    if libc::dup2(source, 3) < 0 {
                        return Err(std::io::Error::last_os_error());
                    }
                    let flags = libc::fcntl(3, libc::F_GETFD);
                    if flags < 0 || libc::fcntl(3, libc::F_SETFD, flags & !libc::FD_CLOEXEC) < 0 {
                        return Err(std::io::Error::last_os_error());
                    }
                    Ok(())
                });
            }
        }
        let out = command.output().expect("isolated descriptor test process");
        assert!(out.status.success() && String::from_utf8_lossy(&out.stdout).contains("1 passed; 0 failed"),
            "isolated fd3 case {case} failed: {:?}\n{}\n{}", out.status,
            String::from_utf8_lossy(&out.stdout), String::from_utf8_lossy(&out.stderr));
        true
    }

    #[test]
    fn an_ordinary_owned_descriptor_survives_fd3_checks() {
        let dir = scratch();
        let path = dir.join("held-parent");
        let mut fixture = OpenOptions::new().read(true).write(true).create_new(true).open(&path).unwrap();
        fixture.write_all(b"held").unwrap();
        if isolated_fd3_case(FD3_PROBE, Some(fixture.as_raw_fd())) {
            assert_eq!(fs::read(&path).unwrap(), b"held-retained");
            drop(fixture);
            fs::remove_dir_all(&dir).unwrap();
            return;
        }
        drop(fixture);
        let flags = unsafe { libc::fcntl(3, libc::F_GETFD) };
        assert!(flags >= 0, "isolated probe inherits its parent's temporary file");
        assert_eq!(unsafe { libc::fcntl(3, libc::F_SETFD, flags | libc::FD_CLOEXEC) }, 0);
        // SAFETY: after exec this inherited descriptor has no Rust owner;
        // this single selected test takes its ownership exactly once.
        let mut held = unsafe { File::from_raw_fd(3) };
        let before = held.metadata().unwrap();
        let flags = unsafe { libc::fcntl(3, libc::F_GETFD) };
        admit_harness_descriptor_refuses_closed_readonly_and_directory_and_sets_cloexec();
        let after = held.metadata().unwrap();
        assert_eq!((before.dev(), before.ino()), (after.dev(), after.ino()));
        assert_eq!(unsafe { libc::fcntl(3, libc::F_GETFD) }, flags,
            "an unrelated owned fd3 must retain its flags across descriptor checks");
        held.write_all(b"-retained").unwrap();
        drop(held);
        fs::remove_dir_all(&dir).unwrap();
    }

    struct RestoredFd3 {
        saved: Option<OwnedFd>,
    }
    impl RestoredFd3 {
        fn install(source: std::os::fd::RawFd) -> Self {
            let saved = duplicate_current();
            let installed = unsafe { libc::dup2(source, 3) };
            assert_eq!(installed, 3, "dup2 onto descriptor 3");
            Self { saved }
        }
        fn close_descriptor() -> Self {
            let saved = duplicate_current();
            if saved.is_some() {
                let closed = unsafe { libc::close(3) };
                assert_eq!(closed, 0, "close descriptor 3");
            }
            Self { saved }
        }
    }
    impl Drop for RestoredFd3 {
        fn drop(&mut self) {
            match self.saved.take() {
                Some(saved) => {
                    let restored = unsafe { libc::dup2(saved.as_raw_fd(), 3) };
                    assert_eq!(restored, 3, "restore descriptor 3");
                }
                None => {
                    let closed = unsafe { libc::close(3) };
                    assert!(closed == 0 || closed == -1);
                }
            }
        }
    }
    fn duplicate_current() -> Option<OwnedFd> {
        let existing = unsafe { libc::fcntl(3, libc::F_GETFD) };
        if existing < 0 {
            return None;
        }
        let duplicated = unsafe { libc::dup(3) };
        assert!(duplicated >= 0, "dup of descriptor 3");
        Some(unsafe { OwnedFd::from_raw_fd(duplicated) })
    }
    fn scratch() -> PathBuf {
        static N: AtomicU64 = AtomicU64::new(0);
        let n = N.fetch_add(1, Ordering::Relaxed);
        let path = std::env::temp_dir().join(format!("opensip-o1p-{}-{n}", std::process::id()));
        fs::create_dir_all(&path).unwrap();
        path
    }
    fn flags_are_close_on_exec(file: &File) -> bool {
        raw_is_close_on_exec(file.as_raw_fd())
    }
    fn raw_is_close_on_exec(fd: i32) -> bool {
        let flags = unsafe { libc::fcntl(fd, libc::F_GETFD) };
        flags >= 0 && flags & libc::FD_CLOEXEC != 0
    }

    #[test]
    fn admit_harness_descriptor_refuses_closed_readonly_and_directory_and_sets_cloexec() {
        if isolated_fd3_case(FD3_CASE, None) {
            return;
        }
        let dir = scratch();
        let closed = RestoredFd3::close_descriptor();
        match admit_harness_descriptor() {
            Err(HarnessDescriptorError::Unavailable(source)) => {
                assert_eq!(source.raw_os_error(), Some(libc::EBADF));
            }
            other => panic!("expected a closed descriptor, got {other:?}"),
        }
        drop(closed);

        let read_only_path = dir.join("read-only");
        fs::write(&read_only_path, b"x").unwrap();
        let read_only = File::open(&read_only_path).unwrap();
        let guard = RestoredFd3::install(read_only.as_raw_fd());
        assert!(matches!(
            admit_harness_descriptor(),
            Err(HarnessDescriptorError::NotWritable)
        ));
        drop(guard);
        drop(read_only);

        let directory = File::open(&dir).unwrap();
        let guard = RestoredFd3::install(directory.as_raw_fd());
        assert!(matches!(
            admit_harness_descriptor(),
            Err(HarnessDescriptorError::WrongType)
        ));
        drop(guard);
        drop(directory);

        let regular_path = dir.join("regular");
        let mut regular = OpenOptions::new()
            .write(true)
            .create(true)
            .truncate(true)
            .open(&regular_path)
            .unwrap();
        regular.write_all(b"w").unwrap();
        let guard = RestoredFd3::install(regular.as_raw_fd());
        let mut first = admit_harness_descriptor().unwrap();
        let mut second = admit_harness_descriptor().unwrap();
        assert_ne!(first.as_raw_fd(), 3);
        assert_ne!(second.as_raw_fd(), 3);
        assert_ne!(first.as_raw_fd(), second.as_raw_fd());
        assert!(flags_are_close_on_exec(&first));
        assert!(flags_are_close_on_exec(&second));
        assert!(raw_is_close_on_exec(3));
        first.write_all(b"one").unwrap();
        drop(first);
        let unrelated_path = dir.join("unrelated");
        let unrelated = OpenOptions::new()
            .write(true)
            .create(true)
            .truncate(true)
            .open(&unrelated_path)
            .unwrap();
        second.write_all(b"two").unwrap();
        drop(second);
        drop(unrelated);
        assert_eq!(fs::read(&unrelated_path).unwrap(), b"");
        assert_eq!(fs::read(&regular_path).unwrap(), b"wonetwo");
        assert!(raw_is_close_on_exec(3));
        drop(guard);
        drop(regular);

        let fifo_path = dir.join("fifo");
        let fifo_bytes = std::ffi::CString::new(fifo_path.as_os_str().as_bytes()).unwrap();
        let created = unsafe { libc::mkfifo(fifo_bytes.as_ptr(), 0o600) };
        assert_eq!(created, 0, "mkfifo");
        let opened = unsafe {
            libc::open(
                fifo_bytes.as_ptr(),
                libc::O_RDWR | libc::O_NONBLOCK | libc::O_CLOEXEC,
            )
        };
        assert!(opened >= 0, "open fifo");
        let fifo = unsafe { File::from_raw_fd(opened) };
        let guard = RestoredFd3::install(fifo.as_raw_fd());
        let admitted = admit_harness_descriptor().unwrap();
        assert_ne!(admitted.as_raw_fd(), 3);
        assert!(flags_are_close_on_exec(&admitted));
        assert!(raw_is_close_on_exec(3));
        drop(admitted);
        drop(guard);
        drop(fifo);

        fs::remove_dir_all(&dir).unwrap();
    }
}
