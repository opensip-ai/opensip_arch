//! Unix handle walk for the report-asset trial. No root-path discovery, trust
//! admission, installation, filesystem mutation, or network access.
#![deny(unsafe_op_in_unsafe_fn)]

use std::ffi::CString;
use std::fs::File;
use std::io;
use std::os::fd::{AsRawFd, FromRawFd};

pub struct ReleaseDirectory(File);

impl ReleaseDirectory {
    /// The host supplies an already selected, retained installation root handle.
    /// This checks its kind; it does not authenticate who selected that handle.
    pub fn from_retained_handle(directory: File) -> io::Result<Self> {
        if !directory.metadata()?.is_dir() {
            return Err(io::Error::new(
                io::ErrorKind::InvalidInput,
                "release root is not a directory",
            ));
        }
        Ok(Self(directory))
    }

    pub fn open_regular(&self, relative: &str) -> io::Result<File> {
        if relative.is_empty()
            || relative.contains(['\\', '\0'])
            || relative.split('/').any(|p| matches!(p, "" | "." | ".."))
        {
            return Err(io::Error::new(
                io::ErrorKind::InvalidInput,
                "invalid relative path",
            ));
        }
        let mut parts = relative.split('/').peekable();
        let mut parent = self.0.try_clone()?;
        while let Some(part) = parts.next() {
            let leaf = parts.peek().is_none();
            let name = CString::new(part).map_err(|_| io::ErrorKind::InvalidInput)?;
            let flags = libc::O_RDONLY
                | libc::O_CLOEXEC
                | libc::O_NOFOLLOW
                | libc::O_NONBLOCK
                | if leaf { 0 } else { libc::O_DIRECTORY };
            // SAFETY: parent owns a live descriptor; name is NUL-terminated and
            // contains exactly one nonempty path segment; openat retains its
            // own descriptor. No create flag is present, so no mode is required.
            let fd = unsafe { libc::openat(parent.as_raw_fd(), name.as_ptr(), flags) };
            if fd < 0 {
                return Err(io::Error::last_os_error());
            }
            // SAFETY: successful openat returns one new owned descriptor. File
            // closes it exactly once, including every error path below.
            let opened = unsafe { File::from_raw_fd(fd) };
            if leaf {
                if !opened.metadata()?.is_file() {
                    return Err(io::Error::new(
                        io::ErrorKind::InvalidInput,
                        "asset is not a regular file",
                    ));
                }
                return Ok(opened);
            }
            if !opened.metadata()?.is_dir() {
                return Err(io::Error::new(
                    io::ErrorKind::InvalidInput,
                    "asset parent is not a directory",
                ));
            }
            parent = opened;
        }
        Err(io::ErrorKind::InvalidInput.into())
    }
}
