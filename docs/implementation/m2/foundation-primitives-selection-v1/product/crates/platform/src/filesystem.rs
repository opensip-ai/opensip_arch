//! Handle-relative regular-file reads under an already selected directory.
//!
//! Root selection, path admission and custody policy belong to callers. This
//! primitive neither authenticates the root nor supplies immutable-tree custody.
//! It refuses symlinks at every walked component and never creates files.
//! Hard links, mounts and concurrent mutations inside the selected directory
//! remain caller custody concerns. O_NONBLOCK avoids waiting on FIFOs; opening
//! an unexpected device can have effects before metadata rejects it, so callers
//! must supply a trusted installation root (or enforce stronger custody).
#![deny(unsafe_op_in_unsafe_fn)]

use std::ffi::CString;
use std::fs::File;
use std::io;
use std::os::fd::{AsRawFd, FromRawFd};

pub struct RetainedDirectory(File);

impl RetainedDirectory {
    /// The host supplies an already selected, retained installation root handle.
    /// This checks its kind; it does not authenticate who selected that handle.
    pub fn from_retained_handle(directory: File) -> io::Result<Self> {
        if !directory.metadata()?.is_dir() {
            return Err(io::Error::new(
                io::ErrorKind::InvalidInput,
                "retained root is not a directory",
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
                        "entry is not a regular file",
                    ));
                }
                return Ok(opened);
            }
            if !opened.metadata()?.is_dir() {
                return Err(io::Error::new(
                    io::ErrorKind::InvalidInput,
                    "parent is not a directory",
                ));
            }
            parent = opened;
        }
        Err(io::ErrorKind::InvalidInput.into())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs;
    use std::io::Read;
    use std::os::unix::fs::{DirBuilderExt, symlink};
    use std::path::PathBuf;
    use std::sync::atomic::{AtomicU64, Ordering};

    static NEXT: AtomicU64 = AtomicU64::new(0);
    struct Tree(PathBuf);
    impl Tree {
        fn new() -> Self {
            for _ in 0..64 {
                let path = std::env::temp_dir().join(format!(
                    "opensip-handles-{}-{}",
                    std::process::id(),
                    NEXT.fetch_add(1, Ordering::Relaxed)
                ));
                match fs::DirBuilder::new().mode(0o700).create(&path) {
                    Ok(()) => return Self(path),
                    Err(e) if e.kind() == io::ErrorKind::AlreadyExists => continue,
                    Err(e) => panic!("create private test tree: {e}"),
                }
            }
            panic!("test directory collision budget exhausted");
        }
        fn handle(&self) -> RetainedDirectory {
            RetainedDirectory::from_retained_handle(File::open(&self.0).unwrap()).unwrap()
        }
    }
    impl Drop for Tree {
        fn drop(&mut self) {
            let _ = fs::remove_dir_all(&self.0);
        }
    }

    #[test]
    fn regular_file_is_read_only_and_close_on_exec() {
        let tree = Tree::new();
        fs::create_dir(tree.0.join("d")).unwrap();
        fs::write(tree.0.join("d/f"), b"selected bytes").unwrap();
        let mut f = tree.handle().open_regular("d/f").unwrap();
        let mut bytes = Vec::new();
        f.read_to_end(&mut bytes).unwrap();
        assert_eq!(bytes, b"selected bytes");
        // SAFETY: f owns a live descriptor for both read-only flag queries.
        let status = unsafe { libc::fcntl(f.as_raw_fd(), libc::F_GETFL) };
        let flags = unsafe { libc::fcntl(f.as_raw_fd(), libc::F_GETFD) };
        assert!(status >= 0 && flags >= 0);
        assert_eq!(status & libc::O_ACCMODE, libc::O_RDONLY);
        assert_ne!(flags & libc::FD_CLOEXEC, 0);
        assert_ne!(status & libc::O_NONBLOCK, 0);
    }

    #[test]
    fn refuses_traversal_links_and_nonregular_entries() {
        let tree = Tree::new();
        fs::create_dir(tree.0.join("inside")).unwrap();
        fs::write(tree.0.join("inside/file"), b"valid").unwrap();
        symlink("inside", tree.0.join("linked-parent")).unwrap();
        symlink("inside/file", tree.0.join("linked-leaf")).unwrap();
        let handle = tree.handle();
        for name in [
            "",
            "linked-parent/file",
            "linked-leaf",
            "inside",
            "inside/../inside/file",
            "./inside/file",
            "/inside/file",
            "inside//file",
            "inside/file/",
            "inside\\file",
            "inside/\0file",
            "x\n/../../inside/file",
            "missing",
        ] {
            assert!(handle.open_regular(name).is_err(), "{name:?}");
        }
        assert!(!tree.0.join("missing").exists());
        let _socket = std::os::unix::net::UnixListener::bind(tree.0.join("socket")).unwrap();
        assert!(handle.open_regular("socket").is_err());
        let fifo = CString::new(tree.0.join("fifo").as_os_str().as_encoded_bytes()).unwrap();
        // SAFETY: fifo is a live NUL-terminated name in this test's owned tree.
        assert_eq!(unsafe { libc::mkfifo(fifo.as_ptr(), 0o600) }, 0);
        assert!(handle.open_regular("fifo").is_err());
        assert!(
            RetainedDirectory::from_retained_handle(
                File::open(tree.0.join("inside/file")).unwrap()
            )
            .is_err()
        );
    }

    #[test]
    fn retained_root_and_opened_file_do_not_retarget_after_rename() {
        let tree = Tree::new();
        fs::create_dir(tree.0.join("root")).unwrap();
        fs::create_dir(tree.0.join("outside")).unwrap();
        fs::write(tree.0.join("root/file"), b"pinned").unwrap();
        fs::write(tree.0.join("outside/file"), b"replacement").unwrap();
        let handle =
            RetainedDirectory::from_retained_handle(File::open(tree.0.join("root")).unwrap())
                .unwrap();
        fs::rename(tree.0.join("root"), tree.0.join("retained")).unwrap();
        symlink("outside", tree.0.join("root")).unwrap();
        let mut opened = handle.open_regular("file").unwrap();
        fs::rename(tree.0.join("retained/file"), tree.0.join("retained/old")).unwrap();
        symlink("../outside/file", tree.0.join("retained/file")).unwrap();
        assert!(handle.open_regular("file").is_err());
        let mut text = String::new();
        opened.read_to_string(&mut text).unwrap();
        assert_eq!(text, "pinned");
    }
}
