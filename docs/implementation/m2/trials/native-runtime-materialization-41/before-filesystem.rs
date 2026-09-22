//! Handle-relative regular-file reads and replacement under a selected directory.
//!
//! Root selection, path admission and custody policy belong to callers. Callers
//! must bind this handle to an admitted local POSIX filesystem: a non-EIO error
//! from a remote filesystem does not establish unchanged visibility. This
//! primitive neither authenticates the root nor supplies immutable-tree custody.
//! Reads refuse symlinks at every walked component. Replacement creates a private
//! staging file, applies file/directory barriers, and reports uncertain visibility.
//! Hard links, mounts and concurrent mutations inside the selected directory
//! remain caller custody concerns. O_NONBLOCK avoids waiting on FIFOs; opening
//! an unexpected device can have effects before metadata rejects it, so callers
//! must supply a trusted installation root (or enforce stronger custody).
//! Publication creates a new inode with requested mode0600 (subject to creation
//! rules/umask). It does not copy the old inode's owner, ACL, xattrs or flags;
//! parent defaults may still be inherited, so callers must admit resulting custody.
//! Read-back checks cached bytes before barriers, not media integrity. Barriers
//! are never retried after failure. Staging names are reserved internal state;
//! crash-leftover cleanup belongs to fenced managed-state maintenance, not reads.
//! This primitive performs only cleanup of staging it created in this call.
#![deny(unsafe_op_in_unsafe_fn)]

use std::ffi::CString;
use std::fs::File;
use std::io;
use std::os::fd::{AsRawFd, FromRawFd};

const STAGING_PREFIX: &str = ".opensip-stage-";

mod directory_publication;
pub use directory_publication::{
    DirectoryRenameFailure, NamedDirectoryPublication, PrivateDirectoryStage,
};

mod directory_binding;
pub use directory_binding::RetainedChildDirectory;

mod descriptor_filesystem;
mod directory_entries;
mod directory_names;
pub use descriptor_filesystem::{DescriptorFilesystem, observe_filesystem};
mod directory_open;
pub use directory_entries::{DirectoryVisitError, DirectoryVisitSummary};

mod path_binding;
pub use path_binding::RetainedDirectoryPath;

pub struct RetainedDirectory(File);

/// Records the barrier primitive completed on one exact retained directory.
/// The borrow keeps that handle alive. It proves neither a parent/name binding,
/// recursive child/file durability, custody, profile qualification nor authority.
/// Consumers must separately admit whether this primitive meets their profile.
/// Multiple receipts can coexist for one handle; they provide no exclusion,
/// single-use permission or enduring namespace guarantee.
pub struct DirectoryBarrierReceipt<'directory> {
    directory: &'directory RetainedDirectory,
    barrier: DirectoryBarrier,
}
impl DirectoryBarrierReceipt<'_> {
    pub fn barrier(&self) -> DirectoryBarrier {
        self.barrier
    }
    /// Exact borrowed handle-object identity, not directory-inode or path equality.
    /// A separately opened handle to the same inode does not match.
    pub fn is_for(&self, directory: &RetainedDirectory) -> bool {
        std::ptr::eq(self.directory, directory)
    }
}
impl RetainedDirectory {
    /// Apply the existing native directory barrier to this original handle.
    /// On macOS, F_FULLFSYNC is tried once; only named unsupported errors allow
    /// the existing fsync fallback. The receipt exposes which completed. Linux
    /// uses fsync. No unsupported profile is upgraded by a successful syscall.
    ///
    /// This does not flush file contents, confirm this directory's name in its
    /// parent, recurse, re-resolve a path or create installation authority. The
    /// caller owes original name/custody/filesystem checks before and after,
    /// including on error, and exclusion through consumption. A failure returns
    /// no receipt and is never retried here; semantic owners must stop the act.
    ///
    /// The link-count guard is only a descriptor check, not portable attachment
    /// evidence: macOS can keep a positive count after rmdir and successfully
    /// flush that unlinked directory. [`Self::is_reachable`] is a separate
    /// available reachability observation. Even that observation does not replace
    /// the caller's original parent/name checks or exclusion through consumption;
    /// this primitive deliberately performs no reachability/path lookup.
    ///
    /// Post-barrier descriptor observation has error precedence: if metadata()
    /// fails or its checks fail, that error replaces any barrier error. Otherwise
    /// the original barrier error is returned. This prioritizes inability to
    /// confirm the retained descriptor; it does not preserve both causes. A post
    /// error therefore cannot prove whether the barrier succeeded or even what
    /// error it returned. All such errors require the owner to stop the act,
    /// without inferring unchanged durability or retry permission.
    pub fn confirm_directory_barrier(&self) -> io::Result<DirectoryBarrierReceipt<'_>> {
        self.confirm_directory_with(|directory| NATIVE_PUBLICATION.sync_directory(directory))
    }
    fn confirm_directory_with(
        &self,
        flush: impl FnOnce(&File) -> io::Result<DirectoryBarrier>,
    ) -> io::Result<DirectoryBarrierReceipt<'_>> {
        use std::os::unix::fs::MetadataExt;
        let before = self.0.metadata()?;
        if !before.is_dir() || before.nlink() == 0 {
            return Err(io::Error::new(
                io::ErrorKind::InvalidData,
                "invalid retained directory",
            ));
        }
        let attempted = flush(&self.0);
        // Sample the original even after a failed barrier. This remains only a
        // descriptor observation: macOS can retain nlink>0 on an unlinked dir.
        let after = self.0.metadata()?;
        if !after.is_dir()
            || after.nlink() == 0
            || before.dev() != after.dev()
            || before.ino() != after.ino()
        {
            return Err(io::Error::new(
                io::ErrorKind::InvalidData,
                "retained directory changed",
            ));
        }
        Ok(DirectoryBarrierReceipt {
            directory: self,
            barrier: attempted?,
        })
    }
}

/// Compare a retained descriptor's native name with exact expected bytes.
/// A sampled name only: no kind, parent/inode binding, custody or authority.
/// macOS bounded name observer; other platforms return Unsupported.
pub fn descriptor_name_matches(file: &File, expected: &std::ffi::OsStr) -> io::Result<bool> {
    directory_names::matches(file, expected)
}

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

    /// Observe whether the retained directory is still reachable on the admitted
    /// local filesystem. A positive observation is not custody or a promise of
    /// future linkage; callers bracket the operation they are classifying.
    /// macOS may retain a positive link count AND a stale F_GETPATH after unlink,
    /// so it additionally reopens that bounded kernel-reported path and compares
    /// device/inode. Failure to observe the path is an error, never leaf absence.
    /// macOS requires a path within PATH_MAX and permission to re-traverse its
    /// ancestors, even when descriptor-relative reads would otherwise succeed.
    /// A path-buffer limit is InvalidInput, not a storage-capacity failure.
    pub fn is_reachable(&self) -> io::Result<bool> {
        use std::os::unix::fs::MetadataExt;
        let retained = self.0.metadata()?;
        if retained.nlink() == 0 {
            return Ok(false);
        }
        #[cfg(target_os = "macos")]
        {
            use std::os::unix::{ffi::OsStrExt, fs::OpenOptionsExt};
            let mut path = [0u8; libc::PATH_MAX as usize];
            // SAFETY: the descriptor is live; F_GETPATH writes at most PATH_MAX
            // bytes into this live mutable buffer. No returned pointer is kept.
            if unsafe { libc::fcntl(self.0.as_raw_fd(), libc::F_GETPATH, path.as_mut_ptr()) } < 0 {
                let error = io::Error::last_os_error();
                // F_GETPATH uses ENOSPC for its fixed pathname buffer, not disk
                // capacity. This is an unavailable retained-path context.
                return Err(if error.raw_os_error() == Some(libc::ENOSPC) {
                    io::Error::new(
                        io::ErrorKind::InvalidInput,
                        "retained directory path exceeds host observation limit",
                    )
                } else {
                    error
                });
            }
            let end = path.iter().position(|b| *b == 0).ok_or_else(|| {
                io::Error::new(
                    io::ErrorKind::InvalidData,
                    "unterminated retained directory path",
                )
            })?;
            if end == 0 || path[0] != b'/' {
                return Err(io::Error::new(
                    io::ErrorKind::InvalidData,
                    "nonabsolute retained directory path",
                ));
            }
            let reopened = match std::fs::OpenOptions::new()
                .read(true)
                .custom_flags(
                    libc::O_DIRECTORY | libc::O_NOFOLLOW | libc::O_CLOEXEC | libc::O_NONBLOCK,
                )
                .open(std::ffi::OsStr::from_bytes(&path[..end]))
            {
                Ok(file) => file,
                Err(error) if error.kind() == io::ErrorKind::NotFound => return Ok(false),
                Err(error) => return Err(error),
            };
            let current = reopened.metadata()?;
            Ok(current.is_dir()
                && current.dev() == retained.dev()
                && current.ino() == retained.ino())
        }
        #[cfg(target_os = "linux")]
        Ok(true)
    }

    pub fn open_regular(&self, relative: &str) -> io::Result<File> {
        if relative.is_empty()
            || relative.contains(['\\', '\0'])
            || relative
                .split('/')
                .any(|p| matches!(p, "" | "." | "..") || p.starts_with(STAGING_PREFIX))
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

/// Mechanism receipt for a newly published file only. It does not prove content
/// addressing, retained custody, a ledger commit or semantic authority.
#[derive(Debug)]
pub struct NewFileReceipt(ReplacementReceipt);
impl NewFileReceipt {
    pub fn byte_len(&self) -> usize {
        self.0.byte_len()
    }
    pub fn directory_barrier(&self) -> DirectoryBarrier {
        self.0.directory_barrier()
    }
}
struct NativeNewPublication {
    // Private injection seam changes the write only; the native verification,
    // rename and barrier path is identical in production and adversarial tests.
    write_staging: fn(&mut File, &[u8]) -> io::Result<()>,
}
const NATIVE_NEW_PUBLICATION: NativeNewPublication = NativeNewPublication {
    write_staging: native_staging_write,
};
fn native_staging_write(file: &mut File, bytes: &[u8]) -> io::Result<()> {
    NATIVE_PUBLICATION.write(file, bytes)
}
impl PublicationOps for NativeNewPublication {
    fn write(&self, file: &mut File, bytes: &[u8]) -> io::Result<()> {
        (self.write_staging)(file, bytes)?;
        verify_staged_bytes(file, bytes)
    }
    fn sync_file(&self, file: &File) -> io::Result<()> {
        NATIVE_PUBLICATION.sync_file(file)
    }
    fn rename(&self, parent: &File, from: &CString, to: &CString) -> io::Result<()> {
        // SAFETY: both names are live single-component C strings under the same
        // retained directory. Exclusive rename must be supported: no overwrite
        // fallback is ever used on ENOTSUP/EINVAL/ENOSYS or any other failure.
        #[cfg(target_os = "macos")]
        let result = unsafe {
            libc::renameatx_np(
                parent.as_raw_fd(),
                from.as_ptr(),
                parent.as_raw_fd(),
                to.as_ptr(),
                libc::RENAME_EXCL,
            )
        };
        #[cfg(target_os = "linux")]
        let result = unsafe {
            libc::renameat2(
                parent.as_raw_fd(),
                from.as_ptr(),
                parent.as_raw_fd(),
                to.as_ptr(),
                libc::RENAME_NOREPLACE,
            )
        };
        if result != 0 {
            return Err(io::Error::last_os_error());
        }
        Ok(())
    }
    fn sync_directory(&self, parent: &File) -> io::Result<DirectoryBarrier> {
        NATIVE_PUBLICATION.sync_directory(parent)
    }
}
fn verify_staged_bytes(file: &mut File, expected: &[u8]) -> io::Result<()> {
    if file.metadata()?.len() != expected.len() as u64 {
        return Err(io::Error::new(
            io::ErrorKind::InvalidData,
            "staging length differs from input",
        ));
    }
    verify_file_contents(file, expected)
}
// Contents after the length precheck. Kept separate to test growth between that
// sample and reading without timing races; production always calls both checks.
fn verify_file_contents(mut file: &File, expected: &[u8]) -> io::Result<()> {
    use std::io::{Read, Seek, SeekFrom};
    file.seek(SeekFrom::Start(0))?;
    let mut buffer = [0u8; 65536];
    for part in expected.chunks(buffer.len()) {
        file.read_exact(&mut buffer[..part.len()])?;
        if &buffer[..part.len()] != part {
            return Err(io::Error::new(
                io::ErrorKind::InvalidData,
                "staging bytes differ from input",
            ));
        }
    }
    let mut extra = [0];
    if file.read(&mut extra)? != 0 {
        return Err(io::Error::new(
            io::ErrorKind::InvalidData,
            "staging length changed during verification",
        ));
    }
    Ok(())
}
impl RetainedDirectory {
    /// Verify staged bytes, apply the file barrier, atomically publish without
    /// replacing an existing entry, then apply the directory barrier. EEXIST
    /// reports no publication by this attempt; it is not a duplicate-content or
    /// durability receipt. Unsupported exclusive rename fails without fallback.
    /// Caller owns directory custody, stable naming and semantic digest checks.
    pub fn publish_new_regular(
        &self,
        name: &str,
        bytes: &[u8],
    ) -> Result<NewFileReceipt, PublicationFailure> {
        self.replace_with(name, bytes, &NATIVE_NEW_PUBLICATION)
            .map(NewFileReceipt)
    }
}

/// Successful byte verification, barriers and post-barrier name/descriptor match.
/// This is an observation under caller-held stable directory/name custody, not
/// permanent availability or a semantic commit. The caller must exclude purge,
/// GC, unlink, replacement and in-place writers through its consuming operation;
/// a post-check alone cannot exclude a mutation immediately after the check.
#[derive(Debug)]
pub struct ExistingFileReceipt(ReplacementReceipt);
impl ExistingFileReceipt {
    pub fn byte_len(&self) -> usize {
        self.0.byte_len()
    }
    pub fn directory_barrier(&self) -> DirectoryBarrier {
        self.0.directory_barrier()
    }
}
impl RetainedDirectory {
    /// Existing shared-writable blobs are refused without replacement. A legacy
    /// blob with permissive mode needs separate admitted maintenance; confirmation
    /// does not silently change permissions or repair existing content.
    pub fn confirm_existing_regular(
        &self,
        name: &str,
        expected: &[u8],
    ) -> io::Result<ExistingFileReceipt> {
        self.confirm_existing_with(name, expected, &NATIVE_PUBLICATION)
    }
    fn confirm_existing_with(
        &self,
        name: &str,
        expected: &[u8],
        ops: &impl PublicationOps,
    ) -> io::Result<ExistingFileReceipt> {
        use std::os::unix::fs::MetadataExt;
        if name.is_empty()
            || matches!(name, "." | "..")
            || name.starts_with(STAGING_PREFIX)
            || name.contains(['/', '\\', '\0'])
        {
            return Err(io::Error::new(
                io::ErrorKind::InvalidInput,
                "invalid confirmation basename",
            ));
        }
        // Linkage checks are defensive; the post-barrier reopened name and
        // identity comparison below establish the receipt name binding.
        if !self.is_reachable()? {
            return Err(io::Error::new(
                io::ErrorKind::InvalidInput,
                "confirmation parent is unreachable",
            ));
        }
        let mut file = self.open_regular(name)?;
        let before = confirmation_metadata(&file)?;
        verify_staged_bytes(&mut file, expected)?;
        ops.sync_file(&file)?;
        let directory_barrier = ops.sync_directory(&self.0)?;
        if !self.is_reachable()? {
            return Err(io::Error::new(
                io::ErrorKind::InvalidInput,
                "confirmation parent became unreachable",
            ));
        }
        let reopened = self.open_regular(name)?;
        let after = confirmation_metadata(&reopened)?;
        if before.dev() != after.dev() || before.ino() != after.ino() {
            return Err(io::Error::new(
                io::ErrorKind::InvalidData,
                "confirmed name no longer identifies verified file",
            ));
        }
        Ok(ExistingFileReceipt(ReplacementReceipt {
            byte_len: expected.len(),
            directory_barrier,
        }))
    }
}

fn confirmation_metadata(file: &File) -> io::Result<std::fs::Metadata> {
    use std::os::unix::fs::MetadataExt;
    let metadata = file.metadata()?;
    if !metadata.is_file() || metadata.nlink() != 1 || metadata.mode() & 0o022 != 0 {
        return Err(io::Error::new(
            io::ErrorKind::InvalidData,
            "existing file has shared links or write permissions",
        ));
    }
    Ok(metadata)
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs;
    use std::io::Read;
    use std::os::unix::fs::{DirBuilderExt, symlink};
    use std::path::{Path, PathBuf};
    use std::sync::atomic::{AtomicU64, Ordering};

    static NEXT: AtomicU64 = AtomicU64::new(0);
    struct Tree(PathBuf);
    impl Tree {
        fn new() -> Self {
            Self::new_in(&std::env::temp_dir())
        }
        fn new_in(base: &Path) -> Self {
            for _ in 0..64 {
                let path = base.join(format!(
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
        // AF_UNIX pathname limits can be shorter than an ordinary TMPDIR.
        // Keep this private socket fixture under the supported Unix /tmp root;
        // do not shorten the remaining filesystem tests or change global cwd.
        let socket_tree = Tree::new_in(Path::new("/tmp"));
        let _socket = std::os::unix::net::UnixListener::bind(socket_tree.0.join("s")).unwrap();
        assert!(socket_tree.handle().open_regular("s").is_err());
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

// Replacement primitive only. Caller owns stable directory/target custody and
// lifecycle fencing. A completed barrier is not a semantic commit or grant.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum PublicationStage {
    Prepare,
    WriteTemporary,
    SyncTemporary,
    Rename,
    SyncDirectory,
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TargetVisibility {
    Unchanged,
    Indeterminate,
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DirectoryBarrier {
    FullFlush,
    Fsync,
}
#[derive(Debug)]
pub struct ReplacementReceipt {
    byte_len: usize,
    directory_barrier: DirectoryBarrier,
}
impl ReplacementReceipt {
    pub fn byte_len(&self) -> usize {
        self.byte_len
    }
    pub fn directory_barrier(&self) -> DirectoryBarrier {
        self.directory_barrier
    }
}
#[derive(Debug)]
pub struct PublicationFailure {
    stage: PublicationStage,
    visibility: TargetVisibility,
    source: io::Error,
    cleanup_error: Option<io::Error>,
}
impl PublicationFailure {
    pub fn stage(&self) -> PublicationStage {
        self.stage
    }
    pub fn visibility(&self) -> TargetVisibility {
        self.visibility
    }
    pub fn source_error(&self) -> &io::Error {
        &self.source
    }
    pub fn cleanup_error(&self) -> Option<&io::Error> {
        self.cleanup_error.as_ref()
    }
}
impl std::fmt::Display for PublicationFailure {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "publication {:?} ({:?}): {}",
            self.stage, self.visibility, self.source
        )
    }
}
impl std::error::Error for PublicationFailure {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        Some(&self.source)
    }
}
fn publication_failure(stage: PublicationStage, error: io::Error) -> PublicationFailure {
    let known_non_io = error
        .raw_os_error()
        .is_some_and(|n| n > 0 && n != libc::EIO);
    let visibility = if stage == PublicationStage::SyncDirectory
        || stage == PublicationStage::Rename && !known_non_io
    {
        TargetVisibility::Indeterminate
    } else {
        TargetVisibility::Unchanged
    };
    PublicationFailure {
        stage,
        visibility,
        source: error,
        cleanup_error: None,
    }
}
trait PublicationOps {
    fn staging_nonce(&self) -> io::Result<[u8; 16]> {
        crate::request_entropy().map_err(|_| io::Error::other("OS staging entropy unavailable"))
    }
    fn cleanup(&self, staging: &mut StagingEntry<'_>) -> io::Result<()> {
        staging.cleanup()
    }
    fn write(&self, file: &mut File, bytes: &[u8]) -> io::Result<()>;
    fn sync_file(&self, file: &File) -> io::Result<()>;
    fn rename(&self, parent: &File, from: &CString, to: &CString) -> io::Result<()>;
    fn sync_directory(&self, parent: &File) -> io::Result<DirectoryBarrier>;
}
struct NativePublication {
    // Only the first syscall is injectable. Production fallback wiring is tested
    // through this exact PublicationOps implementation, not a parallel wrapper.
    #[cfg(target_os = "macos")]
    full_flush: fn(&File) -> io::Result<()>,
}
const NATIVE_PUBLICATION: NativePublication = NativePublication {
    #[cfg(target_os = "macos")]
    full_flush: full_flush_directory,
};
impl PublicationOps for NativePublication {
    fn write(&self, file: &mut File, bytes: &[u8]) -> io::Result<()> {
        use std::io::Write;
        file.write_all(bytes)
    }
    fn sync_file(&self, file: &File) -> io::Result<()> {
        #[cfg(target_os = "macos")]
        {
            // SAFETY: file owns a live fd; F_FULLFSYNC has no extra argument.
            if unsafe { libc::fcntl(file.as_raw_fd(), libc::F_FULLFSYNC) } != 0 {
                return Err(io::Error::last_os_error());
            }
            Ok(())
        }
        #[cfg(target_os = "linux")]
        {
            file.sync_all()
        }
    }
    fn rename(&self, parent: &File, from: &CString, to: &CString) -> io::Result<()> {
        // SAFETY: both pathnames are live single-component C strings and parent
        // owns the retained directory fd. No ambient path traversal occurs.
        if unsafe {
            libc::renameat(
                parent.as_raw_fd(),
                from.as_ptr(),
                parent.as_raw_fd(),
                to.as_ptr(),
            )
        } != 0
        {
            return Err(io::Error::last_os_error());
        }
        Ok(())
    }
    fn sync_directory(&self, parent: &File) -> io::Result<DirectoryBarrier> {
        #[cfg(target_os = "macos")]
        {
            directory_barrier_with(parent, self.full_flush, fsync_directory)
        }
        #[cfg(target_os = "linux")]
        {
            fsync_directory(parent)?;
            Ok(DirectoryBarrier::Fsync)
        }
    }
}
// Direct syscall: File::sync_all on Apple is F_FULLFSYNC, not this fallback.
fn fsync_directory(parent: &File) -> io::Result<()> {
    // SAFETY: parent owns the live descriptor; fsync takes no pointer arguments.
    if unsafe { libc::fsync(parent.as_raw_fd()) } != 0 {
        return Err(io::Error::last_os_error());
    }
    Ok(())
}
#[cfg(target_os = "macos")]
fn full_flush_directory(parent: &File) -> io::Result<()> {
    // SAFETY: parent owns a live descriptor; F_FULLFSYNC takes no extra argument.
    if unsafe { libc::fcntl(parent.as_raw_fd(), libc::F_FULLFSYNC) } != 0 {
        return Err(io::Error::last_os_error());
    }
    Ok(())
}
#[cfg(target_os = "macos")]
fn unsupported_directory_full_flush(error: &io::Error) -> bool {
    error
        .raw_os_error()
        .is_some_and(|n| n == libc::EINVAL || n == libc::ENOTSUP || n == libc::ENOTTY)
}
#[cfg(target_os = "macos")]
fn directory_barrier_with(
    parent: &File,
    full_flush: impl FnOnce(&File) -> io::Result<()>,
    fsync: impl FnOnce(&File) -> io::Result<()>,
) -> io::Result<DirectoryBarrier> {
    match full_flush(parent) {
        Ok(()) => Ok(DirectoryBarrier::FullFlush),
        Err(error) if unsupported_directory_full_flush(&error) => {
            fsync(parent)?;
            Ok(DirectoryBarrier::Fsync)
        }
        Err(error) => Err(error),
    }
}
struct StagingEntry<'a> {
    parent: &'a File,
    name: CString,
    linked: bool,
}
impl StagingEntry<'_> {
    fn cleanup(&mut self) -> io::Result<()> {
        if !self.linked {
            return Ok(());
        }
        // SAFETY: parent owns its fd and name is our exclusive-created child.
        if unsafe { libc::unlinkat(self.parent.as_raw_fd(), self.name.as_ptr(), 0) } != 0 {
            let e = io::Error::last_os_error();
            if e.raw_os_error() != Some(libc::ENOENT) {
                return Err(e);
            }
        }
        self.linked = false;
        Ok(())
    }
}
impl Drop for StagingEntry<'_> {
    fn drop(&mut self) {
        let _ = self.cleanup();
    }
}
impl RetainedDirectory {
    /// Replace one regular target under retained directory custody. Refuses
    /// symlink/nonregular targets; a missing target is allowed. The caller must
    /// exclude competing namespace writers and must never use this on live lock
    /// carriers. On any indeterminate outcome reopen/reconcile before further use.
    pub fn replace_regular(
        &self,
        name: &str,
        bytes: &[u8],
    ) -> Result<ReplacementReceipt, PublicationFailure> {
        self.replace_with(name, bytes, &NATIVE_PUBLICATION)
    }
    fn replace_with(
        &self,
        name: &str,
        bytes: &[u8],
        ops: &impl PublicationOps,
    ) -> Result<ReplacementReceipt, PublicationFailure> {
        let prepare = |e| publication_failure(PublicationStage::Prepare, e);
        if name.is_empty()
            || matches!(name, "." | "..")
            || name.starts_with(STAGING_PREFIX)
            || name.contains(['/', '\\', '\0'])
        {
            return Err(prepare(io::Error::new(
                io::ErrorKind::InvalidInput,
                "invalid publication basename",
            )));
        }
        let destination =
            CString::new(name).map_err(|_| prepare(io::ErrorKind::InvalidInput.into()))?;
        let mut stat = core::mem::MaybeUninit::<libc::stat>::uninit();
        // SAFETY: stat points to writable storage; the name is a single live
        // component; AT_SYMLINK_NOFOLLOW avoids opening or following its target.
        if unsafe {
            libc::fstatat(
                self.0.as_raw_fd(),
                destination.as_ptr(),
                stat.as_mut_ptr(),
                libc::AT_SYMLINK_NOFOLLOW,
            )
        } == 0
        {
            // SAFETY: successful fstatat initialized the entire stat structure.
            if unsafe { stat.assume_init() }.st_mode & libc::S_IFMT != libc::S_IFREG {
                return Err(prepare(io::Error::new(
                    io::ErrorKind::InvalidInput,
                    "publication target is not regular",
                )));
            }
        } else {
            let e = io::Error::last_os_error();
            if e.raw_os_error() != Some(libc::ENOENT) {
                return Err(prepare(e));
            }
        }
        let nonce = ops.staging_nonce().map_err(prepare)?;
        let tag = nonce.iter().map(|b| format!("{b:02x}")).collect::<String>();
        let name = CString::new(format!("{STAGING_PREFIX}{tag}")).unwrap();
        // SAFETY: parent fd/name are live. O_EXCL creates our private staging
        // entry without following links; the mode argument is supplied for CREATE.
        let fd = unsafe {
            libc::openat(
                self.0.as_raw_fd(),
                name.as_ptr(),
                libc::O_RDWR | libc::O_CREAT | libc::O_EXCL | libc::O_NOFOLLOW | libc::O_CLOEXEC,
                0o600 as libc::c_uint,
            )
        };
        if fd < 0 {
            return Err(prepare(io::Error::last_os_error()));
        }
        // SAFETY: successful openat returned one newly owned descriptor.
        let mut file = unsafe { File::from_raw_fd(fd) };
        let mut staging = StagingEntry {
            parent: &self.0,
            name,
            linked: true,
        };
        let result: Result<ReplacementReceipt, PublicationFailure> = (|| {
            ops.write(&mut file, bytes)
                .map_err(|e| publication_failure(PublicationStage::WriteTemporary, e))?;
            ops.sync_file(&file)
                .map_err(|e| publication_failure(PublicationStage::SyncTemporary, e))?;
            ops.rename(&self.0, &staging.name, &destination)
                .map_err(|e| publication_failure(PublicationStage::Rename, e))?;
            staging.linked = false;
            let directory_barrier = ops
                .sync_directory(&self.0)
                .map_err(|e| publication_failure(PublicationStage::SyncDirectory, e))?;
            Ok(ReplacementReceipt {
                byte_len: bytes.len(),
                directory_barrier,
            })
        })();
        drop(file);
        result.map_err(|mut e| {
            e.cleanup_error = ops.cleanup(&mut staging).err();
            e
        })
    }
}

#[cfg(test)]
mod publication_tests {
    use super::*;
    use std::{
        cell::RefCell,
        io::Write,
        os::unix::fs::{PermissionsExt, symlink},
        path::PathBuf,
    };
    struct Fixture {
        root: PathBuf,
        handle: RetainedDirectory,
    }
    impl Fixture {
        fn new() -> Self {
            let tag = crate::request_entropy()
                .unwrap()
                .iter()
                .map(|b| format!("{b:02x}"))
                .collect::<String>();
            let root = std::env::temp_dir().join(format!("opensip-publication79-{tag}"));
            std::fs::create_dir(&root).unwrap();
            let handle =
                RetainedDirectory::from_retained_handle(File::open(&root).unwrap()).unwrap();
            Self { root, handle }
        }
    }
    impl Drop for Fixture {
        fn drop(&mut self) {
            let _ = std::fs::remove_dir_all(&self.root);
        }
    }
    #[derive(Debug, Clone, Copy)]
    enum Fault {
        PartialWrite,
        FileSync,
        RenameBeforeIo,
        RenameAfterIo,
        RenameKnown,
        DirectorySync,
    }
    struct Injected {
        fault: Fault,
        calls: RefCell<Vec<&'static str>>,
    }
    impl PublicationOps for Injected {
        fn write(&self, f: &mut File, b: &[u8]) -> io::Result<()> {
            self.calls.borrow_mut().push("write");
            if matches!(self.fault, Fault::PartialWrite) {
                f.write_all(&b[..b.len() / 2])?;
                Err(io::Error::from_raw_os_error(libc::ENOSPC))
            } else {
                NATIVE_PUBLICATION.write(f, b)
            }
        }
        fn sync_file(&self, f: &File) -> io::Result<()> {
            self.calls.borrow_mut().push("file-sync");
            NATIVE_PUBLICATION.sync_file(f)?;
            if matches!(self.fault, Fault::FileSync) {
                Err(io::Error::from_raw_os_error(libc::EIO))
            } else {
                Ok(())
            }
        }
        fn rename(&self, p: &File, f: &CString, t: &CString) -> io::Result<()> {
            self.calls.borrow_mut().push("rename");
            if matches!(self.fault, Fault::RenameBeforeIo) {
                return Err(io::Error::from_raw_os_error(libc::EIO));
            }
            if matches!(self.fault, Fault::RenameKnown) {
                return Err(io::Error::from_raw_os_error(libc::EACCES));
            }
            NATIVE_PUBLICATION.rename(p, f, t)?;
            if matches!(self.fault, Fault::RenameAfterIo) {
                Err(io::Error::from_raw_os_error(libc::EIO))
            } else {
                Ok(())
            }
        }
        fn sync_directory(&self, p: &File) -> io::Result<DirectoryBarrier> {
            self.calls.borrow_mut().push("directory-sync");
            if matches!(self.fault, Fault::DirectorySync) {
                Err(io::Error::from_raw_os_error(libc::EIO))
            } else {
                NATIVE_PUBLICATION.sync_directory(p)
            }
        }
    }
    #[cfg(target_os = "macos")]
    #[test]
    fn native_directory_fallback_wiring_uses_fsync_after_unsupported_fullflush() {
        use std::os::fd::OwnedFd;
        use std::os::unix::net::UnixStream;
        // A socket is deliberately not an admitted publication directory. On
        // this supported Mac test lane fsync(socket) gives EINVAL, whereas
        // F_FULLFSYNC(socket) gives EBADF. This safely distinguishes the actual
        // fallback syscall without claiming a real filesystem rejected fullflush.
        let (left, _right) = UnixStream::pair().unwrap();
        let fd: OwnedFd = left.into();
        let file = File::from(fd);
        assert_eq!(
            fsync_directory(&file).unwrap_err().raw_os_error(),
            Some(libc::EINVAL)
        );
        assert_eq!(
            full_flush_directory(&file).unwrap_err().raw_os_error(),
            Some(libc::EBADF)
        );
        // Pin the production constant's first syscall as well as its fallback.
        assert_eq!(
            NATIVE_PUBLICATION
                .sync_directory(&file)
                .unwrap_err()
                .raw_os_error(),
            Some(libc::EBADF)
        );
        let native = NativePublication {
            full_flush: |_| Err(io::Error::from_raw_os_error(libc::ENOTSUP)),
        };
        let error = native.sync_directory(&file).unwrap_err();
        assert_eq!(error.raw_os_error(), Some(libc::EINVAL));
        let fixture = Fixture::new();
        assert_eq!(
            native.sync_directory(&fixture.handle.0).unwrap(),
            DirectoryBarrier::Fsync
        );
    }
    #[test]
    fn native_new_write_refuses_corruption_truncation_and_extra_bytes() {
        use std::io::{Seek, SeekFrom};
        fn corrupt(f: &mut File, b: &[u8]) -> io::Result<()> {
            native_staging_write(f, b)?;
            f.seek(SeekFrom::Start(0))?;
            f.write_all(b"X")
        }
        fn truncate(f: &mut File, b: &[u8]) -> io::Result<()> {
            native_staging_write(f, b)?;
            f.set_len(b.len().saturating_sub(1) as u64)
        }
        fn append(f: &mut File, b: &[u8]) -> io::Result<()> {
            native_staging_write(f, b)?;
            f.write_all(b"extra")
        }
        for write_staging in [
            corrupt as fn(&mut File, &[u8]) -> io::Result<()>,
            truncate,
            append,
        ] {
            let f = Fixture::new();
            let ops = NativeNewPublication { write_staging };
            let e = f.handle.replace_with("new", b"expected", &ops).unwrap_err();
            assert_eq!(e.stage(), PublicationStage::WriteTemporary);
            assert_eq!(e.visibility(), TargetVisibility::Unchanged);
            assert!(matches!(
                e.source_error().kind(),
                io::ErrorKind::InvalidData | io::ErrorKind::UnexpectedEof
            ));
            assert!(!f.root.join("new").exists());
            assert_eq!(std::fs::read_dir(&f.root).unwrap().count(), 0);
        }
    }
    #[cfg(target_os = "macos")]
    #[test]
    fn directory_fallback_accepts_only_named_unsupported_errors() {
        use std::cell::Cell;
        let f = Fixture::new();
        for errno in [
            libc::EINVAL,
            libc::ENOTSUP,
            libc::ENOTTY,
            libc::EIO,
            libc::ENOSPC,
            libc::EINTR,
            libc::EBADF,
        ] {
            let calls = Cell::new(0);
            let result = directory_barrier_with(
                &f.handle.0,
                |_| Err(io::Error::from_raw_os_error(errno)),
                |p| {
                    calls.set(calls.get() + 1);
                    fsync_directory(p)
                },
            );
            let allowed = [libc::EINVAL, libc::ENOTSUP, libc::ENOTTY].contains(&errno);
            assert_eq!(calls.get(), usize::from(allowed));
            if allowed {
                assert_eq!(result.unwrap(), DirectoryBarrier::Fsync);
            } else {
                assert_eq!(result.unwrap_err().raw_os_error(), Some(errno));
            }
        }
        assert!(!unsupported_directory_full_flush(&io::Error::other(
            "lost errno"
        )));
        let result =
            directory_barrier_with(&f.handle.0, |_| Ok(()), |_| panic!("unneeded fallback"));
        assert_eq!(result.unwrap(), DirectoryBarrier::FullFlush);
    }
    #[cfg(target_os = "macos")]
    #[test]
    fn failed_directory_fallback_is_not_retried_or_reported_successful() {
        use std::cell::Cell;
        let f = Fixture::new();
        let calls = Cell::new(0);
        let result = directory_barrier_with(
            &f.handle.0,
            |_| Err(io::Error::from_raw_os_error(libc::ENOTSUP)),
            |_| {
                calls.set(calls.get() + 1);
                Err(io::Error::from_raw_os_error(libc::EIO))
            },
        );
        assert_eq!(calls.get(), 1);
        assert_eq!(result.unwrap_err().raw_os_error(), Some(libc::EIO));
    }
    struct CollisionOrCleanup {
        fail_cleanup: bool,
    }
    impl PublicationOps for CollisionOrCleanup {
        fn staging_nonce(&self) -> io::Result<[u8; 16]> {
            Ok([0x42; 16])
        }
        fn write(&self, f: &mut File, b: &[u8]) -> io::Result<()> {
            NATIVE_PUBLICATION.write(f, b)?;
            if self.fail_cleanup {
                Err(io::Error::from_raw_os_error(libc::ENOSPC))
            } else {
                Ok(())
            }
        }
        fn sync_file(&self, f: &File) -> io::Result<()> {
            NATIVE_PUBLICATION.sync_file(f)
        }
        fn rename(&self, p: &File, f: &CString, t: &CString) -> io::Result<()> {
            NATIVE_PUBLICATION.rename(p, f, t)
        }
        fn sync_directory(&self, p: &File) -> io::Result<DirectoryBarrier> {
            NATIVE_PUBLICATION.sync_directory(p)
        }
        fn cleanup(&self, staging: &mut StagingEntry<'_>) -> io::Result<()> {
            if self.fail_cleanup {
                Err(io::Error::from_raw_os_error(libc::EIO))
            } else {
                staging.cleanup()
            }
        }
    }
    #[test]
    fn staging_collision_never_opens_or_replaces_an_existing_entry() {
        let f = Fixture::new();
        let staging = f.root.join(format!("{STAGING_PREFIX}{}", "42".repeat(16)));
        std::fs::write(&staging, b"other attempt").unwrap();
        let e = f
            .handle
            .replace_with(
                "new",
                b"replacement",
                &CollisionOrCleanup {
                    fail_cleanup: false,
                },
            )
            .unwrap_err();
        assert_eq!(e.stage(), PublicationStage::Prepare);
        assert_eq!(e.source_error().raw_os_error(), Some(libc::EEXIST));
        assert_eq!(std::fs::read(staging).unwrap(), b"other attempt");
        assert!(!f.root.join("new").exists());
    }
    #[test]
    fn cleanup_failure_remains_separate_from_publication_failure() {
        let f = Fixture::new();
        let e = f
            .handle
            .replace_with(
                "new",
                b"replacement",
                &CollisionOrCleanup { fail_cleanup: true },
            )
            .unwrap_err();
        assert_eq!(e.stage(), PublicationStage::WriteTemporary);
        assert_eq!(e.source_error().raw_os_error(), Some(libc::ENOSPC));
        assert_eq!(e.cleanup_error().unwrap().raw_os_error(), Some(libc::EIO));
        assert_eq!(e.visibility(), TargetVisibility::Unchanged);
        assert!(!f.root.join("new").exists());
        // Drop makes a separate best-effort cleanup; this is not a retry of a barrier.
        assert_eq!(std::fs::read_dir(&f.root).unwrap().count(), 0);
    }
    #[test]
    fn staging_prefix_cannot_name_publication_confirmation_or_read_targets() {
        let f = Fixture::new();
        let name = format!("{STAGING_PREFIX}{}", "ab".repeat(16));
        std::fs::write(f.root.join(&name), b"private stage").unwrap();
        assert_eq!(
            f.handle.replace_regular(&name, b"x").unwrap_err().stage(),
            PublicationStage::Prepare
        );
        assert_eq!(
            f.handle
                .publish_new_regular(&name, b"x")
                .unwrap_err()
                .stage(),
            PublicationStage::Prepare
        );
        assert!(f.handle.open_regular(&name).is_err());
        assert!(
            f.handle
                .confirm_existing_regular(&name, b"private stage")
                .is_err()
        );
        assert_eq!(std::fs::read(f.root.join(&name)).unwrap(), b"private stage");
    }

    #[test]
    fn actual_replacement_barriers_preserve_old_open_handle_and_retain_parent_identity() {
        use std::io::Read;
        let mut f = Fixture::new();
        let old = f.root.join("state");
        std::fs::write(&old, b"old").unwrap();
        let mut retained = File::open(&old).unwrap();
        let receipt = f.handle.replace_regular("state", b"new-state").unwrap();
        assert_eq!(receipt.byte_len(), 9);
        assert!(matches!(
            receipt.directory_barrier(),
            DirectoryBarrier::FullFlush | DirectoryBarrier::Fsync
        ));
        assert_eq!(std::fs::read(&old).unwrap(), b"new-state");
        let mut b = Vec::new();
        retained.read_to_end(&mut b).unwrap();
        assert_eq!(b, b"old");
        assert_eq!(
            std::fs::metadata(&old).unwrap().permissions().mode() & 0o777,
            0o600
        );
        f.handle.replace_regular("new-file", b"created").unwrap();
        assert_eq!(std::fs::read(f.root.join("new-file")).unwrap(), b"created");
        let previous = f.root.clone();
        let moved = f.root.with_extension("moved");
        std::fs::rename(&previous, &moved).unwrap();
        f.root = moved;
        std::fs::create_dir(&previous).unwrap();
        std::fs::write(previous.join("state"), b"unrelated").unwrap();
        f.handle
            .replace_regular("state", b"retained-parent")
            .unwrap();
        assert_eq!(
            std::fs::read(f.root.join("state")).unwrap(),
            b"retained-parent"
        );
        assert_eq!(std::fs::read(previous.join("state")).unwrap(), b"unrelated");
        std::fs::remove_dir_all(previous).unwrap();
    }
    #[test]
    fn injected_failure_stage_controls_visibility_and_never_returns_a_receipt() {
        for fault in [
            Fault::PartialWrite,
            Fault::FileSync,
            Fault::RenameBeforeIo,
            Fault::RenameAfterIo,
            Fault::RenameKnown,
            Fault::DirectorySync,
        ] {
            let f = Fixture::new();
            std::fs::write(f.root.join("state"), b"old").unwrap();
            let ops = Injected {
                fault,
                calls: RefCell::new(Vec::new()),
            };
            let failure = f
                .handle
                .replace_with("state", b"new-value", &ops)
                .unwrap_err();
            let (stage, visibility, visible, calls) = match fault {
                Fault::PartialWrite => (
                    PublicationStage::WriteTemporary,
                    TargetVisibility::Unchanged,
                    b"old".as_slice(),
                    1,
                ),
                Fault::FileSync => (
                    PublicationStage::SyncTemporary,
                    TargetVisibility::Unchanged,
                    b"old".as_slice(),
                    2,
                ),
                Fault::RenameBeforeIo => (
                    PublicationStage::Rename,
                    TargetVisibility::Indeterminate,
                    b"old".as_slice(),
                    3,
                ),
                Fault::RenameAfterIo => (
                    PublicationStage::Rename,
                    TargetVisibility::Indeterminate,
                    b"new-value".as_slice(),
                    3,
                ),
                Fault::RenameKnown => (
                    PublicationStage::Rename,
                    TargetVisibility::Unchanged,
                    b"old".as_slice(),
                    3,
                ),
                Fault::DirectorySync => (
                    PublicationStage::SyncDirectory,
                    TargetVisibility::Indeterminate,
                    b"new-value".as_slice(),
                    4,
                ),
            };
            assert_eq!(failure.stage(), stage, "{fault:?}");
            assert_eq!(failure.visibility(), visibility, "{fault:?}");
            assert!(failure.cleanup_error().is_none());
            assert!(failure.source_error().raw_os_error().is_some());
            assert_eq!(std::fs::read(f.root.join("state")).unwrap(), visible);
            assert_eq!(
                ops.calls.borrow().as_slice(),
                &["write", "file-sync", "rename", "directory-sync"][..calls]
            );
            assert!(std::fs::read_dir(&f.root).unwrap().all(|e| {
                !e.unwrap()
                    .file_name()
                    .to_string_lossy()
                    .starts_with(".opensip-stage-")
            }));
        }
    }
    #[test]
    fn malformed_names_and_nonregular_targets_refuse_before_publication() {
        let f = Fixture::new();
        std::fs::write(f.root.join("victim"), b"untouched").unwrap();
        symlink("victim", f.root.join("link")).unwrap();
        std::fs::create_dir(f.root.join("directory")).unwrap();
        for name in [
            "",
            ".",
            "..",
            "../escape",
            "nested/child",
            "back\\slash",
            "nul\0tail",
            "link",
            "directory",
        ] {
            let e = f.handle.replace_regular(name, b"bad").unwrap_err();
            assert_eq!(e.stage(), PublicationStage::Prepare);
            assert_eq!(e.visibility(), TargetVisibility::Unchanged);
        }
        assert_eq!(std::fs::read(f.root.join("victim")).unwrap(), b"untouched");
    }
    #[test]
    fn target_visibility_matches_stage_aware_reference_not_errno_alone() {
        let mut n = 0;
        for line in include_str!("../tests/fixtures/publication-failure-cases.tsv").lines() {
            let q = line.split('\t').collect::<Vec<_>>();
            assert_eq!(q.len(), 5);
            let stage = match q[1] {
                "prepare" => PublicationStage::Prepare,
                "write-temp" => PublicationStage::WriteTemporary,
                "sync-temp" => PublicationStage::SyncTemporary,
                "rename" => PublicationStage::Rename,
                "sync-directory" => PublicationStage::SyncDirectory,
                _ => panic!("stage"),
            };
            let code = match q[2] {
                "ENOSPC" => Some(libc::ENOSPC),
                "EDQUOT" => Some(libc::EDQUOT),
                "EIO" => Some(libc::EIO),
                "EROFS" => Some(libc::EROFS),
                "OTHER_NON_EIO" => Some(libc::EACCES),
                _ => None,
            };
            let error = code
                .map(io::Error::from_raw_os_error)
                .unwrap_or_else(|| io::Error::other("lost OS errno"));
            let result = publication_failure(stage, error);
            assert_eq!(
                if result.visibility == TargetVisibility::Unchanged {
                    "unchanged"
                } else {
                    "indeterminate"
                },
                q[3]
            );
            assert_eq!(
                result.visibility == TargetVisibility::Indeterminate,
                q[4] == "1"
            );
            n += 1;
        }
        assert_eq!(n, 315);
    }
}

/// Potential ACL writer, not an effective-access or custody decision.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum AclWriter {
    User(u32),
    Group(u32),
    Unresolved,
}

/// Selected descriptor metadata used to detect changes during observation.
/// Matching samples do not prove absence of intervening changes or future writes.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DescriptorMetadata {
    pub device: u64,
    pub inode: u64,
    pub mode: u32,
    pub uid: u32,
    pub gid: u32,
    pub links: u64,
    pub size: u64,
    pub modified: (i64, i64),
    pub changed: (i64, i64),
    pub flags: u32,
}
#[cfg(target_os = "macos")]
impl DescriptorMetadata {
    pub(crate) fn from_metadata(m: &std::fs::Metadata) -> Self {
        use std::os::unix::fs::MetadataExt;
        Self {
            device: m.dev(),
            inode: m.ino(),
            mode: m.mode(),
            uid: m.uid(),
            gid: m.gid(),
            links: m.nlink(),
            size: m.size(),
            modified: (m.mtime(), m.mtime_nsec()),
            changed: (m.ctime(), m.ctime_nsec()),
            #[cfg(target_os = "macos")]
            flags: {
                use std::os::macos::fs::MetadataExt;
                m.st_flags()
            },
            #[cfg(not(target_os = "macos"))]
            flags: 0,
        }
    }
}
#[derive(Debug)]
pub struct DescriptorObservation {
    pub metadata: DescriptorMetadata,
    /// Conservatively includes write ALLOW entries even if DENY or inheritance
    /// rules could prevent their effective use. Empty only after a successful read.
    pub possible_acl_writers: Vec<AclWriter>,
}
#[derive(Debug)]
pub enum DescriptorObservationError {
    Metadata(io::Error),
    Acl(io::Error),
    ChangedDuringRead,
    UnsupportedPlatform,
}

/// Observe an already retained descriptor. This does not authenticate its root,
/// path, owner or parent chain, and conveys no permission to write or execute.
/// The macOS adapter samples descriptor metadata before, during and after the ACL
/// read. Linux support is explicitly unavailable until separately implemented.
pub fn observe_descriptor(
    file: &File,
) -> Result<DescriptorObservation, DescriptorObservationError> {
    #[cfg(target_os = "macos")]
    {
        observe_descriptor_with(file, crate::macos::descriptor_acl)
    }
    #[cfg(not(target_os = "macos"))]
    {
        let _ = file;
        Err(DescriptorObservationError::UnsupportedPlatform)
    }
}
#[cfg(target_os = "macos")]
fn observe_descriptor_with(
    file: &File,
    reader: impl FnOnce(&File) -> io::Result<(DescriptorMetadata, Vec<AclWriter>)>,
) -> Result<DescriptorObservation, DescriptorObservationError> {
    let before = DescriptorMetadata::from_metadata(
        &file
            .metadata()
            .map_err(DescriptorObservationError::Metadata)?,
    );
    if before.mode & libc::S_IFMT as u32 != libc::S_IFREG as u32
        && before.mode & libc::S_IFMT as u32 != libc::S_IFDIR as u32
    {
        return Err(DescriptorObservationError::Metadata(io::Error::new(
            io::ErrorKind::InvalidInput,
            "descriptor must refer to regular file or directory",
        )));
    }
    let (during, writers) = reader(file).map_err(DescriptorObservationError::Acl)?;
    let after = DescriptorMetadata::from_metadata(
        &file
            .metadata()
            .map_err(DescriptorObservationError::Metadata)?,
    );
    if before != during || during != after {
        return Err(DescriptorObservationError::ChangedDuringRead);
    }
    Ok(DescriptorObservation {
        metadata: during,
        possible_acl_writers: writers,
    })
}

#[cfg(all(test, target_os = "macos"))]
mod observation_tests {
    use super::*;
    use std::fs;
    use std::os::unix::fs::{OpenOptionsExt, PermissionsExt};
    use std::sync::atomic::{AtomicU64, Ordering};
    static NEXT: AtomicU64 = AtomicU64::new(0);
    struct Scratch {
        path: std::path::PathBuf,
        file: File,
    }
    impl Scratch {
        fn new() -> Self {
            for _ in 0..64 {
                let path = std::env::temp_dir().join(format!(
                    "opensip-acl83-{}-{}",
                    std::process::id(),
                    NEXT.fetch_add(1, Ordering::Relaxed)
                ));
                match fs::OpenOptions::new()
                    .read(true)
                    .write(true)
                    .create_new(true)
                    .mode(0o600)
                    .open(&path)
                {
                    Ok(file) => return Self { path, file },
                    Err(e) if e.kind() == io::ErrorKind::AlreadyExists => continue,
                    Err(e) => panic!("scratch file: {e}"),
                }
            }
            panic!("scratch collision budget");
        }
    }
    impl Drop for Scratch {
        fn drop(&mut self) {
            let _ = fs::remove_file(&self.path);
        }
    }
    #[test]
    fn native_acl_read_has_explicit_absence_allow_deny_and_group_results() {
        let scratch = Scratch::new();
        assert!(
            observe_descriptor(&scratch.file)
                .unwrap()
                .possible_acl_writers
                .is_empty()
        );
        // SAFETY: pure OS identity queries, no pointer parameters.
        let uid = unsafe { libc::getuid() };
        let gid = unsafe { libc::getgid() };
        for (is_group, id, tag, mask, expected) in [
            (false, uid, 1, 1 << 2, vec![AclWriter::User(uid)]),
            (
                false,
                if uid == 1001 { 1002 } else { 1001 },
                1,
                1 << 12,
                vec![AclWriter::User(if uid == 1001 { 1002 } else { 1001 })],
            ),
            (true, gid, 1, 1 << 13, vec![AclWriter::Group(gid)]),
            (false, uid, 2, 1 << 2, vec![]),
            (false, uid, 1, 1 << 1, vec![]),
        ] {
            crate::macos::set_probe_acl(&scratch.file, is_group, id, tag, mask).unwrap();
            assert_eq!(
                observe_descriptor(&scratch.file)
                    .unwrap()
                    .possible_acl_writers,
                expected
            );
        }
    }
    #[test]
    fn descriptor_observation_survives_unlink_without_reading_replacement_path() {
        let scratch = Scratch::new();
        let before = observe_descriptor(&scratch.file).unwrap();
        fs::remove_file(&scratch.path).unwrap();
        fs::write(&scratch.path, b"replacement").unwrap();
        let held = observe_descriptor(&scratch.file).unwrap();
        let replaced = observe_descriptor(&File::open(&scratch.path).unwrap()).unwrap();
        assert_eq!(before.metadata.inode, held.metadata.inode);
        assert_eq!(held.metadata.links, 0);
        assert_ne!(held.metadata.inode, replaced.metadata.inode);
    }
    #[test]
    fn changes_during_acl_read_and_failed_acl_read_never_become_empty_evidence() {
        let scratch = Scratch::new();
        let result = observe_descriptor_with(&scratch.file, |file| {
            file.set_permissions(fs::Permissions::from_mode(0o640))?;
            crate::macos::descriptor_acl(file)
        });
        assert!(matches!(
            result,
            Err(DescriptorObservationError::ChangedDuringRead)
        ));
        let result = observe_descriptor_with(&scratch.file, |_| {
            Err(io::Error::from_raw_os_error(libc::EIO))
        });
        assert!(
            matches!(result,Err(DescriptorObservationError::Acl(e)) if e.raw_os_error()==Some(libc::EIO))
        );
        // A stale metadata sample followed by a mutation is refused too.
        let result = observe_descriptor_with(&scratch.file, |file| {
            let observed = crate::macos::descriptor_acl(file)?;
            file.set_permissions(fs::Permissions::from_mode(0o600))?;
            Ok(observed)
        });
        assert!(matches!(
            result,
            Err(DescriptorObservationError::ChangedDuringRead)
        ));
    }
    #[test]
    fn nonregular_descriptor_refuses_before_acl_observation() {
        let (stream, _peer) = std::os::unix::net::UnixStream::pair().unwrap();
        let owned: std::os::fd::OwnedFd = stream.into();
        let file = File::from(owned);
        assert!(matches!(
            observe_descriptor_with(&file, |_| panic!("must not read ACL")),
            Err(DescriptorObservationError::Metadata(_))
        ));
    }
}

#[cfg(test)]
mod new_publication_tests {
    use super::*;
    use std::{fs, io::Write, os::unix::fs::symlink, path::PathBuf};
    struct Fixture {
        root: PathBuf,
        dir: RetainedDirectory,
    }
    impl Fixture {
        fn new() -> Self {
            let tag = crate::request_entropy()
                .unwrap()
                .iter()
                .map(|b| format!("{b:02x}"))
                .collect::<String>();
            let root = std::env::temp_dir().join(format!("opensip-new88-{tag}"));
            fs::create_dir(&root).unwrap();
            let dir = RetainedDirectory::from_retained_handle(File::open(&root).unwrap()).unwrap();
            Self { root, dir }
        }
    }
    impl Drop for Fixture {
        fn drop(&mut self) {
            let _ = fs::remove_dir_all(&self.root);
        }
    }
    #[test]
    fn exclusive_publication_preserves_existing_bytes_and_cleans_staging() {
        let f = Fixture::new();
        let bytes = vec![0xa5; 200_000];
        let receipt = f.dir.publish_new_regular("object", &bytes).unwrap();
        assert_eq!(receipt.byte_len(), bytes.len());
        assert!(matches!(
            receipt.directory_barrier(),
            DirectoryBarrier::FullFlush | DirectoryBarrier::Fsync
        ));
        let err = f
            .dir
            .publish_new_regular("object", b"replacement")
            .unwrap_err();
        assert_eq!(err.stage(), PublicationStage::Rename);
        assert_eq!(err.source_error().raw_os_error(), Some(libc::EEXIST));
        assert_eq!(err.visibility(), TargetVisibility::Unchanged);
        assert!(err.cleanup_error().is_none());
        assert_eq!(fs::read(f.root.join("object")).unwrap(), bytes);
        assert_eq!(fs::read_dir(&f.root).unwrap().count(), 1);
        assert_eq!(
            f.dir.publish_new_regular("empty", b"").unwrap().byte_len(),
            0
        );
    }
    #[test]
    fn concurrent_new_publishers_have_one_winner_and_no_mixed_or_replaced_object() {
        let f = Fixture::new();
        let barrier = std::sync::Barrier::new(4);
        let results = std::thread::scope(|scope| {
            let jobs = (0..4u8)
                .map(|i| {
                    let f = &f;
                    let barrier = &barrier;
                    scope.spawn(move || {
                        let bytes = vec![i; 131_073];
                        barrier.wait();
                        (i, f.dir.publish_new_regular("object", &bytes))
                    })
                })
                .collect::<Vec<_>>();
            jobs.into_iter()
                .map(|j| j.join().unwrap())
                .collect::<Vec<_>>()
        });
        let winners = results
            .iter()
            .filter(|(_, r)| r.is_ok())
            .collect::<Vec<_>>();
        assert_eq!(winners.len(), 1);
        let winner = winners[0].0;
        for (_, r) in &results {
            if let Err(e) = r {
                assert_eq!(e.source_error().raw_os_error(), Some(libc::EEXIST));
                assert_eq!(e.visibility(), TargetVisibility::Unchanged);
                assert!(e.cleanup_error().is_none());
            }
        }
        assert_eq!(
            fs::read(f.root.join("object")).unwrap(),
            vec![winner; 131_073]
        );
        assert_eq!(fs::read_dir(&f.root).unwrap().count(), 1);
    }
    #[test]
    fn symlink_directory_and_invalid_names_are_not_replaced() {
        let f = Fixture::new();
        fs::write(f.root.join("outside"), b"original").unwrap();
        symlink("outside", f.root.join("link")).unwrap();
        fs::create_dir(f.root.join("dir")).unwrap();
        for name in ["link", "dir", "", "../outside", "a/b", "a\\b"] {
            assert!(f.dir.publish_new_regular(name, b"replacement").is_err());
        }
        assert_eq!(fs::read(f.root.join("outside")).unwrap(), b"original");
        assert!(
            fs::symlink_metadata(f.root.join("link"))
                .unwrap()
                .is_symlink()
        );
        assert!(f.root.join("dir").is_dir());
    }
    enum Fault {
        WrongBytes,
        ShortBytes,
        UnsupportedRename,
        AfterRenameIo,
    }
    struct FaultOps(Fault);
    impl PublicationOps for FaultOps {
        fn write(&self, f: &mut File, b: &[u8]) -> io::Result<()> {
            match self.0 {
                Fault::WrongBytes => {
                    f.write_all(&vec![0; b.len()])?;
                    verify_staged_bytes(f, b)
                }
                Fault::ShortBytes => {
                    f.write_all(&b[..b.len() - 1])?;
                    verify_staged_bytes(f, b)
                }
                _ => NATIVE_NEW_PUBLICATION.write(f, b),
            }
        }
        fn sync_file(&self, f: &File) -> io::Result<()> {
            NATIVE_NEW_PUBLICATION.sync_file(f)
        }
        fn rename(&self, p: &File, f: &CString, t: &CString) -> io::Result<()> {
            if matches!(self.0, Fault::UnsupportedRename) {
                return Err(io::Error::from_raw_os_error(libc::ENOTSUP));
            }
            NATIVE_NEW_PUBLICATION.rename(p, f, t)?;
            if matches!(self.0, Fault::AfterRenameIo) {
                return Err(io::Error::from_raw_os_error(libc::EIO));
            }
            Ok(())
        }
        fn sync_directory(&self, p: &File) -> io::Result<DirectoryBarrier> {
            NATIVE_NEW_PUBLICATION.sync_directory(p)
        }
    }
    #[test]
    fn staged_mismatch_and_unsupported_exclusive_rename_never_publish_or_fall_back() {
        for fault in [
            Fault::WrongBytes,
            Fault::ShortBytes,
            Fault::UnsupportedRename,
        ] {
            let f = Fixture::new();
            let e = f
                .dir
                .replace_with("object", b"expected-bytes", &FaultOps(fault))
                .unwrap_err();
            assert_eq!(e.visibility(), TargetVisibility::Unchanged);
            assert!(!f.root.join("object").exists());
            assert_eq!(fs::read_dir(&f.root).unwrap().count(), 0);
        }
        let f = Fixture::new();
        fs::write(f.root.join("object"), b"old").unwrap();
        let e = f
            .dir
            .replace_with(
                "object",
                b"expected-bytes",
                &FaultOps(Fault::UnsupportedRename),
            )
            .unwrap_err();
        assert_eq!(e.source_error().raw_os_error(), Some(libc::ENOTSUP));
        assert_eq!(fs::read(f.root.join("object")).unwrap(), b"old");
    }
    #[test]
    fn error_after_actual_exclusive_rename_stays_indeterminate_without_receipt() {
        let f = Fixture::new();
        let e = f
            .dir
            .replace_with("object", b"new", &FaultOps(Fault::AfterRenameIo))
            .unwrap_err();
        assert_eq!(e.stage(), PublicationStage::Rename);
        assert_eq!(e.visibility(), TargetVisibility::Indeterminate);
        assert_eq!(fs::read(f.root.join("object")).unwrap(), b"new");
        assert!(e.cleanup_error().is_none());
    }
}

#[cfg(test)]
mod confirmation_tests {
    use super::*;
    use std::{
        cell::RefCell,
        fs,
        io::Write,
        os::unix::fs::{PermissionsExt, symlink},
        path::PathBuf,
    };
    struct Fixture(PathBuf);
    impl Fixture {
        fn new() -> Self {
            let name = crate::request_entropy()
                .unwrap()
                .iter()
                .map(|b| format!("{b:02x}"))
                .collect::<String>();
            let path = std::env::temp_dir().join(format!("opensip-confirm126-{name}"));
            fs::create_dir(&path).unwrap();
            Self(path)
        }
        fn parent(&self) -> RetainedDirectory {
            RetainedDirectory::from_retained_handle(File::open(&self.0).unwrap()).unwrap()
        }
        fn put(&self, name: &str, bytes: &[u8]) {
            let p = self.0.join(name);
            fs::write(&p, bytes).unwrap();
            fs::set_permissions(p, fs::Permissions::from_mode(0o600)).unwrap();
        }
    }
    impl Drop for Fixture {
        fn drop(&mut self) {
            let _ = fs::remove_dir_all(&self.0);
        }
    }
    #[derive(Default)]
    struct Ops<'a> {
        calls: RefCell<Vec<&'static str>>,
        file_fail: bool,
        directory_fail: bool,
        after_directory: RefCell<Option<Box<dyn FnOnce() + 'a>>>,
    }
    impl PublicationOps for Ops<'_> {
        fn write(&self, _: &mut File, _: &[u8]) -> io::Result<()> {
            panic!("confirmation must not write")
        }
        fn rename(&self, _: &File, _: &CString, _: &CString) -> io::Result<()> {
            panic!("confirmation must not rename")
        }
        fn sync_file(&self, _: &File) -> io::Result<()> {
            self.calls.borrow_mut().push("file");
            if self.file_fail {
                Err(io::Error::other("injected file barrier"))
            } else {
                Ok(())
            }
        }
        fn sync_directory(&self, _: &File) -> io::Result<DirectoryBarrier> {
            self.calls.borrow_mut().push("directory");
            if self.directory_fail {
                return Err(io::Error::other("injected directory barrier"));
            }
            if let Some(action) = self.after_directory.borrow_mut().take() {
                action();
            }
            Ok(DirectoryBarrier::FullFlush)
        }
    }
    #[test]
    fn confirmation_verification_and_barriers_are_ordered_and_fail_closed() {
        let f = Fixture::new();
        f.put("blob", b"good");
        let parent = f.parent();
        for (file_fail, directory_fail, expected) in [
            (false, false, vec!["file", "directory"]),
            (true, false, vec!["file"]),
            (false, true, vec!["file", "directory"]),
        ] {
            let ops = Ops {
                file_fail,
                directory_fail,
                ..Ops::default()
            };
            let result = parent.confirm_existing_with("blob", b"good", &ops);
            assert_eq!(result.is_ok(), !file_fail && !directory_fail);
            assert_eq!(*ops.calls.borrow(), expected);
            if let Ok(receipt) = result {
                assert_eq!(receipt.byte_len(), 4);
                assert_eq!(receipt.directory_barrier(), DirectoryBarrier::FullFlush);
            }
        }
        for bytes in [b"evil".as_slice(), b"g", b"good-extra"] {
            f.put("blob", bytes);
            let ops = Ops::default();
            let result = parent.confirm_existing_with("blob", b"good", &ops);
            assert!(matches!(result,Err(e)if e.kind()==io::ErrorKind::InvalidData));
            assert!(ops.calls.borrow().is_empty());
            assert_eq!(fs::read(f.0.join("blob")).unwrap(), bytes);
        }
    }
    #[test]
    fn confirmation_rebinds_the_name_after_barriers() {
        for change in [
            "remove",
            "replace-other",
            "replace-same",
            "symlink",
            "hardlink",
            "writable",
            "parent-removed",
        ] {
            let f = Fixture::new();
            f.put("blob", b"good");
            let parent = f.parent();
            let ops = Ops {
                after_directory: RefCell::new(Some(Box::new(|| {
                    let path = f.0.join("blob");
                    match change {
                        "remove" => fs::remove_file(&path).unwrap(),
                        "replace-other" | "replace-same" => {
                            f.put(
                                "other",
                                if change == "replace-same" {
                                    b"good"
                                } else {
                                    b"evil"
                                },
                            );
                            fs::rename(f.0.join("other"), path).unwrap();
                        }
                        "symlink" => {
                            fs::remove_file(&path).unwrap();
                            f.put("other", b"good");
                            symlink("other", path).unwrap();
                        }
                        "hardlink" => fs::hard_link(path, f.0.join("other")).unwrap(),
                        "writable" => {
                            fs::set_permissions(path, fs::Permissions::from_mode(0o666)).unwrap()
                        }
                        "parent-removed" => {
                            fs::remove_file(path).unwrap();
                            fs::remove_dir(&f.0).unwrap();
                            fs::create_dir(&f.0).unwrap();
                            f.put("blob", b"good");
                        }
                        _ => unreachable!(),
                    }
                }))),
                ..Ops::default()
            };
            assert!(
                parent.confirm_existing_with("blob", b"good", &ops).is_err(),
                "{change}"
            );
            assert_eq!(*ops.calls.borrow(), ["file", "directory"]);
        }
    }
    #[test]
    fn confirmation_rejects_existing_shared_links_and_write_permissions() {
        let f = Fixture::new();
        let parent = f.parent();
        f.put("blob", b"good");
        fs::hard_link(f.0.join("blob"), f.0.join("other")).unwrap();
        let ops = Ops::default();
        assert!(parent.confirm_existing_with("blob", b"good", &ops).is_err());
        assert!(ops.calls.borrow().is_empty());
        fs::remove_file(f.0.join("other")).unwrap();
        for mode in [0o620, 0o602, 0o666] {
            fs::set_permissions(f.0.join("blob"), fs::Permissions::from_mode(mode)).unwrap();
            let ops = Ops::default();
            assert!(parent.confirm_existing_with("blob", b"good", &ops).is_err());
            assert!(ops.calls.borrow().is_empty());
        }
    }
    #[test]
    fn content_verification_detects_growth_after_the_length_sample() {
        let f = Fixture::new();
        f.put("blob", b"good");
        let file = File::open(f.0.join("blob")).unwrap();
        assert_eq!(file.metadata().unwrap().len(), 4);
        fs::OpenOptions::new()
            .append(true)
            .open(f.0.join("blob"))
            .unwrap()
            .write_all(b"extra")
            .unwrap();
        assert!(
            matches!(verify_file_contents(&file,b"good"),Err(e)if e.kind()==io::ErrorKind::InvalidData)
        );
    }
}

mod directory_birth;
pub use directory_birth::{DirectoryBirthObservation, observe_directory_birth};

mod directory_volume;
pub use directory_volume::{DirectoryVolumeObservation, observe_directory_volume};

#[cfg(test)]
mod directory_barrier_receipt_tests {
    use super::*;
    use std::{fs, os::unix::fs::MetadataExt, path::PathBuf};
    struct Fixture(PathBuf);
    impl Fixture {
        fn new() -> Self {
            let nonce = crate::request_entropy()
                .unwrap()
                .iter()
                .map(|b| format!("{b:02x}"))
                .collect::<String>();
            let path = std::env::temp_dir().join(format!("opensip-directory-barrier393-{nonce}"));
            fs::create_dir(&path).unwrap();
            Self(path)
        }
        fn held(&self) -> RetainedDirectory {
            RetainedDirectory::from_retained_handle(File::open(&self.0).unwrap()).unwrap()
        }
    }
    impl Drop for Fixture {
        fn drop(&mut self) {
            let _ = fs::remove_dir_all(&self.0);
        }
    }
    #[test]
    fn directory_barrier_receipt_binds_original_handle_owner() {
        let f = Fixture::new();
        let a = f.held();
        let b = f.held();
        let receipt = a.confirm_directory_barrier().unwrap();
        assert!(receipt.is_for(&a));
        assert!(!receipt.is_for(&b));
        #[cfg(target_os = "linux")]
        assert_eq!(receipt.barrier(), DirectoryBarrier::Fsync);
    }
    #[test]
    fn directory_barrier_failure_is_once_and_never_a_receipt() {
        let f = Fixture::new();
        let a = f.held();
        for code in [libc::EIO, libc::EINTR, libc::EACCES] {
            let mut calls = 0;
            let result = a.confirm_directory_with(|_| {
                calls += 1;
                Err(io::Error::from_raw_os_error(code))
            });
            assert_eq!(calls, 1);
            assert_eq!(result.err().unwrap().raw_os_error(), Some(code));
        }
    }
    #[test]
    fn directory_barrier_is_on_retained_inode_without_claiming_current_name() {
        let f = Fixture::new();
        let nested = f.0.join("original");
        fs::create_dir(&nested).unwrap();
        let a = RetainedDirectory::from_retained_handle(File::open(&nested).unwrap()).unwrap();
        let original = a.0.metadata().unwrap().ino();
        let receipt = a
            .confirm_directory_with(|fd| {
                fs::rename(&nested, f.0.join("moved")).unwrap();
                fs::create_dir(&nested).unwrap();
                assert_eq!(fd.metadata().unwrap().ino(), original);
                NATIVE_PUBLICATION.sync_directory(fd)
            })
            .unwrap();
        assert!(receipt.is_for(&a));
        assert_ne!(fs::metadata(&nested).unwrap().ino(), original);
        assert_eq!(fs::metadata(f.0.join("moved")).unwrap().ino(), original);
    }
    #[test]
    fn directory_barrier_receipt_preserves_the_primitive_not_a_stronger_promise() {
        let f = Fixture::new();
        let a = f.held();
        for primitive in [DirectoryBarrier::Fsync, DirectoryBarrier::FullFlush] {
            let receipt = a.confirm_directory_with(|_| Ok(primitive)).unwrap();
            assert_eq!(receipt.barrier(), primitive);
            assert!(receipt.is_for(&a));
        }
    }
    #[test]
    fn directory_barrier_defends_kind_before_any_flush() {
        let f = Fixture::new();
        let path = f.0.join("file");
        fs::write(&path, b"x").unwrap();
        // Private construction violates the public constructor's kind check.
        let invalid = RetainedDirectory(File::open(&path).unwrap());
        let mut called = false;
        assert!(
            invalid
                .confirm_directory_with(|_| {
                    called = true;
                    Ok(DirectoryBarrier::Fsync)
                })
                .is_err()
        );
        assert!(!called);
    }
}
