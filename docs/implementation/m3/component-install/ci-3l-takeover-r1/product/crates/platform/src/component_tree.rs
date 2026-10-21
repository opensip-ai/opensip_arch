//! Charged native primitives for the component store (law CI r5 item 4, P-1
//! to P-7, with amendment CI-A1; component installation plan r3, LD-CIP-1,
//! -2, -6, -10 and -11; unit CI-2): a positioned chunk write, `fchmod`, a
//! standalone file barrier, `symlinkat`, `readlinkat`, a no-follow regular
//! open from a retained directory or of an operator path, a no-follow entry
//! status read, and a one-call pin lock; and, for the launch member (unit
//! CI-3L, amendment CI-A3), a no-follow-final `lstat` of an absolute spelling
//! and an `fstat` of a retained directory. Mechanisms only: which directory,
//! which names and what a result means belong to the installer.
//!
//! Each primitive charges its price before its native call, and makes that
//! call once: no retry and no fallback. A price is one edge per native call;
//! a status read is `status_read_cost()`. Names, paths and link targets are
//! copied NUL-terminated into a fixed stack buffer (`StackName`), never onto
//! the heap, so no primitive allocates; LAW's owned records for the archive
//! path, a link target and the link buffer stay the caller's charges, as its
//! recipes price them. Descriptor closes are not counted, as
//! everywhere in the filesystem primitives (`directory_publication.rs`).
//!
//! Only macOS is implemented and qualified (plan r3's Q2 ruling). On every
//! other target each primitive refuses `Unsupported` before charging or
//! making any native call; nothing falls back.
//!
//! This module sits outside the census closure (LD-CIP-1): it uses the
//! public `RetainedDirectory::as_file` only.
#![deny(unsafe_op_in_unsafe_fn)]
use crate::{RetainedDirectory, WorkCost, WorkFailure, WorkScope};
use std::ffi::CStr;
use std::fs::File;
use std::io;
use std::os::fd::{AsRawFd, FromRawFd};
use std::path::Path;

/// P-7 (LD-CIP-2): a published price equal to the filesystem's internal
/// `status_read_cost()` (`filesystem/path_binding.rs`). A source pin keeps the
/// two expressions identical.
pub fn status_read_cost() -> crate::WorkCost {
    crate::WorkCost {
        objects: 0,
        edges: 1,
        bytes: std::mem::size_of::<libc::stat>().max(std::mem::size_of::<std::fs::Metadata>()),
    }
}

/// One native call: one edge (P-1, P-2, P-3, P-4's `symlinkat` and
/// `readlinkat`, P-6).
pub const NATIVE_CALL: WorkCost = WorkCost {
    objects: 0,
    edges: 1,
    bytes: 0,
};

/// `fopen` and P-5: one no-follow open plus its kind-check status read.
pub fn open_regular_no_follow_cost() -> WorkCost {
    let status = status_read_cost();
    WorkCost {
        objects: 0,
        edges: 1 + status.edges,
        bytes: status.bytes,
    }
}

/// The access a no-follow open asks for (LD-CIP-6): chosen per platform
/// before the open, never retried in the other mode.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Access {
    ReadOnly,
    ReadWrite,
}

/// Why a no-follow open or status read did not yield a regular file.
#[derive(Debug)]
pub enum TreeOpenError {
    /// The name is not present (`ENOENT`).
    Absent,
    /// It is present but not a regular file: a symlink (`ELOOP` under
    /// `O_NOFOLLOW`), a directory, or another kind.
    NotRegular,
    /// The name is not one lawful component.
    Name,
    /// The target does not implement the primitive (only macOS does).
    Unsupported,
    Io(io::Error),
}

/// A regular file this module opened no-follow and close-on-exec, and
/// kind-checked. Only this module constructs one, so a pin (P-6) can rely on
/// both without another call (LD-CIP-11).
#[derive(Debug)]
pub struct TreeFile {
    file: File,
    length: u64,
    mode: u32,
    identity: Identity,
}
impl TreeFile {
    pub fn file(&self) -> &File {
        &self.file
    }
    /// The length its kind-check status read observed.
    pub fn length(&self) -> u64 {
        self.length
    }
    /// The permission bits (`0o7777`) its kind-check status read observed.
    pub fn mode(&self) -> u32 {
        self.mode
    }
    /// The identity its kind-check status read observed.
    pub fn identity(&self) -> Identity {
        self.identity
    }
}

/// `(device, inode, size, mtime, ctime)`, the archive's identity sample
/// (LAW item 4, LD-CI-4).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Identity {
    pub device: u64,
    pub inode: u64,
    pub size: u64,
    pub mtime: (i64, i64),
    pub ctime: (i64, i64),
}

/// An entry's no-follow status (`fstatat` with `AT_SYMLINK_NOFOLLOW`).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct EntryStatus {
    pub kind: EntryKind,
    /// The permission bits, `0o7777`.
    pub mode: u32,
    pub length: u64,
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum EntryKind {
    File,
    Directory,
    Symlink,
    Other,
}

fn invalid_input() -> io::Error {
    io::Error::new(
        io::ErrorKind::InvalidInput,
        "invalid component tree argument",
    )
}
fn supported() -> Result<(), TreeOpenError> {
    if cfg!(target_os = "macos") {
        Ok(())
    } else {
        Err(TreeOpenError::Unsupported)
    }
}
fn supported_io() -> io::Result<()> {
    if cfg!(target_os = "macos") {
        Ok(())
    } else {
        Err(io::Error::new(
            io::ErrorKind::Unsupported,
            "component tree primitives are implemented on macOS only",
        ))
    }
}

/// A no-follow directory open met a non-directory: `ENOTDIR`, or `ELOOP`
/// for a symlink.
pub fn is_not_directory(error: &io::Error) -> bool {
    matches!(
        error.raw_os_error(),
        Some(libc::ENOTDIR) | Some(libc::ELOOP)
    )
}

/// The longest name or path a primitive copies: macOS's `PATH_MAX`, so every
/// component (at most `NAME_MAX`, 255 bytes) and every path a no-follow open
/// accepts fits.
pub const NAME_CAPACITY: usize = 1024;

/// A NUL-terminated copy of a name or path in a fixed stack buffer (CI2-R1-RF-1;
/// CI-A2-h): `NAME_CAPACITY` bytes at most, then one NUL. No heap allocation
/// is made, so a copy is not an owned record and carries no charge. A longer
/// input, or one holding NUL, is refused before any charge or call.
struct StackName {
    bytes: [u8; NAME_CAPACITY + 1],
}
impl StackName {
    fn of(raw: &[u8]) -> Option<Self> {
        if raw.len() > NAME_CAPACITY || raw.contains(&0) {
            return None;
        }
        let mut bytes = [0u8; NAME_CAPACITY + 1];
        bytes[..raw.len()].copy_from_slice(raw);
        Some(Self { bytes })
    }
    fn as_ptr(&self) -> *const libc::c_char {
        self.bytes.as_ptr().cast()
    }
}

/// One component: not empty, `.` or `..`, and holding no `/` or NUL.
fn component(name: &str) -> Option<StackName> {
    if name.is_empty() || name == "." || name == ".." || name.contains('/') {
        return None;
    }
    StackName::of(name.as_bytes())
}

// The `stat` field types differ across targets; the casts are portable.
#[allow(clippy::unnecessary_cast)]
fn status_of(st: &libc::stat) -> (EntryKind, u32, u64, Identity) {
    let kind = match st.st_mode & libc::S_IFMT {
        libc::S_IFREG => EntryKind::File,
        libc::S_IFDIR => EntryKind::Directory,
        libc::S_IFLNK => EntryKind::Symlink,
        _ => EntryKind::Other,
    };
    let identity = Identity {
        device: st.st_dev as u64,
        inode: st.st_ino as u64,
        size: st.st_size as u64,
        mtime: (st.st_mtime as i64, st.st_mtime_nsec as i64),
        ctime: (st.st_ctime as i64, st.st_ctime_nsec as i64),
    };
    (
        kind,
        (st.st_mode as u32) & 0o7777,
        st.st_size as u64,
        identity,
    )
}

fn fstat(file: &File) -> io::Result<libc::stat> {
    // SAFETY: an all-zero `stat` is a valid output buffer for fstat.
    let mut st: libc::stat = unsafe { std::mem::zeroed() };
    // SAFETY: file owns a live descriptor and st is a valid out pointer.
    if unsafe { libc::fstat(file.as_raw_fd(), &mut st) } != 0 {
        return Err(io::Error::last_os_error());
    }
    Ok(st)
}

/// Wrap a fresh descriptor and kind-check it: a regular file, or refused.
fn admit_regular(fd: libc::c_int) -> Result<TreeFile, TreeOpenError> {
    if fd < 0 {
        let error = io::Error::last_os_error();
        return Err(match error.raw_os_error() {
            Some(libc::ENOENT) => TreeOpenError::Absent,
            Some(libc::ELOOP) | Some(libc::EISDIR) => TreeOpenError::NotRegular,
            _ => TreeOpenError::Io(error),
        });
    }
    // SAFETY: a successful open returns one new owned descriptor.
    let file = unsafe { File::from_raw_fd(fd) };
    let st = fstat(&file).map_err(TreeOpenError::Io)?;
    let (kind, mode, length, identity) = status_of(&st);
    if kind != EntryKind::File {
        return Err(TreeOpenError::NotRegular);
    }
    Ok(TreeFile {
        file,
        length,
        mode,
        identity,
    })
}

fn flags(access: Access) -> libc::c_int {
    let base = libc::O_NOFOLLOW | libc::O_CLOEXEC | libc::O_NONBLOCK;
    match access {
        Access::ReadOnly => base | libc::O_RDONLY,
        Access::ReadWrite => base | libc::O_RDWR,
    }
}

/// P-4's `fopen`: open `name` in `directory` no-follow and close-on-exec,
/// then kind-check it. One open and one status read, charged first
/// (`open_regular_no_follow_cost`).
pub fn open_regular_no_follow(
    directory: &RetainedDirectory,
    name: &str,
    access: Access,
    work: &mut WorkScope<'_>,
) -> Result<TreeFile, WorkFailure<TreeOpenError>> {
    supported().map_err(WorkFailure::Operation)?;
    let name = component(name).ok_or(WorkFailure::Operation(TreeOpenError::Name))?;
    work.charge(open_regular_no_follow_cost())?;
    // SAFETY: a live retained directory descriptor and one NUL-terminated
    // component; no create flags.
    let fd = unsafe {
        libc::openat(
            directory.as_file().as_raw_fd(),
            name.as_ptr(),
            flags(access),
        )
    };
    admit_regular(fd).map_err(WorkFailure::Operation)
}

/// P-5: open the operator-supplied archive path read-only, no-follow and
/// close-on-exec, then kind-check it (`open_regular_no_follow_cost`). The
/// path is copied onto the stack; LAW's owned record for it is the caller's.
pub fn open_archive(
    path: &Path,
    work: &mut WorkScope<'_>,
) -> Result<TreeFile, WorkFailure<TreeOpenError>> {
    use std::os::unix::ffi::OsStrExt;
    supported().map_err(WorkFailure::Operation)?;
    let path = StackName::of(path.as_os_str().as_bytes())
        .ok_or(WorkFailure::Operation(TreeOpenError::Name))?;
    work.charge(open_regular_no_follow_cost())?;
    // SAFETY: one NUL-terminated path; no create flags.
    let fd = unsafe { libc::open(path.as_ptr(), flags(Access::ReadOnly)) };
    admit_regular(fd).map_err(WorkFailure::Operation)
}

/// One identity sample of an open file (`status_read_cost`).
pub fn sample_identity(
    file: &TreeFile,
    work: &mut WorkScope<'_>,
) -> Result<Identity, WorkFailure<io::Error>> {
    supported_io().map_err(WorkFailure::Operation)?;
    work.charge(status_read_cost())?;
    let st = fstat(&file.file).map_err(WorkFailure::Operation)?;
    Ok(status_of(&st).3)
}

/// One no-follow status read of `name` in `directory` (`status_read_cost`).
pub fn entry_status(
    directory: &RetainedDirectory,
    name: &str,
    work: &mut WorkScope<'_>,
) -> Result<EntryStatus, WorkFailure<TreeOpenError>> {
    supported().map_err(WorkFailure::Operation)?;
    let name = component(name).ok_or(WorkFailure::Operation(TreeOpenError::Name))?;
    work.charge(status_read_cost())?;
    // SAFETY: an all-zero `stat` is a valid output buffer.
    let mut st: libc::stat = unsafe { std::mem::zeroed() };
    // SAFETY: a live directory descriptor, one component, a valid out pointer.
    let r = unsafe {
        libc::fstatat(
            directory.as_file().as_raw_fd(),
            name.as_ptr(),
            &mut st,
            libc::AT_SYMLINK_NOFOLLOW,
        )
    };
    if r != 0 {
        let error = io::Error::last_os_error();
        return Err(WorkFailure::Operation(match error.raw_os_error() {
            Some(libc::ENOENT) => TreeOpenError::Absent,
            _ => TreeOpenError::Io(error),
        }));
    }
    let (kind, mode, length, _) = status_of(&st);
    Ok(EntryStatus { kind, mode, length })
}

/// One no-follow status of an absolute spelling, or of a retained
/// directory handle (CI-A3; unit CI-3L): its kind, permission bits and
/// identity.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct PathStatus {
    pub kind: EntryKind,
    /// The permission bits, `0o7777`.
    pub mode: u32,
    pub device: u64,
    pub inode: u64,
}

/// Why `path_status_no_follow` observed no status: the spelling names
/// nothing (`ENOENT`), a non-directory stands along it (`ENOTDIR`), or any
/// other native error.
#[derive(Debug)]
pub enum PathStatusError {
    Absent,
    NotDirectory,
    Io(io::Error),
}

fn path_status_of(st: &libc::stat) -> PathStatus {
    let (kind, mode, _, identity) = status_of(st);
    PathStatus {
        kind,
        mode,
        device: identity.device,
        inode: identity.inode,
    }
}

/// CI-A3's path observation: one `lstat` of an absolute spelling, which does
/// not follow its final component (`status_read_cost`, charged before the
/// call). The caller owns and charges the spelling; nothing is copied.
pub fn path_status_no_follow(
    path: &CStr,
    work: &mut WorkScope<'_>,
) -> Result<PathStatus, WorkFailure<PathStatusError>> {
    supported_io().map_err(|e| WorkFailure::Operation(PathStatusError::Io(e)))?;
    work.charge(status_read_cost())?;
    // SAFETY: an all-zero `stat` is a valid output buffer.
    let mut st: libc::stat = unsafe { std::mem::zeroed() };
    // SAFETY: one NUL-terminated spelling the caller borrows, and a valid out
    // pointer.
    if unsafe { libc::lstat(path.as_ptr(), &mut st) } != 0 {
        let error = io::Error::last_os_error();
        return Err(WorkFailure::Operation(match error.raw_os_error() {
            Some(libc::ENOENT) => PathStatusError::Absent,
            Some(libc::ENOTDIR) => PathStatusError::NotDirectory,
            _ => PathStatusError::Io(error),
        }));
    }
    Ok(path_status_of(&st))
}

/// CI-A3's directory observation: one `fstat` of a retained directory
/// handle (`status_read_cost`, charged before the call).
pub fn directory_identity(
    directory: &RetainedDirectory,
    work: &mut WorkScope<'_>,
) -> Result<PathStatus, WorkFailure<io::Error>> {
    supported_io().map_err(WorkFailure::Operation)?;
    work.charge(status_read_cost())?;
    let st = fstat(directory.as_file()).map_err(WorkFailure::Operation)?;
    Ok(path_status_of(&st))
}

/// Why a positioned chunk write refused.
#[derive(Debug)]
pub enum ChunkWriteError {
    Io(io::Error),
    /// Fewer bytes were written than supplied (C1a2's candidate-custody
    /// rule): refused, never continued.
    Short {
        written: usize,
    },
}

/// P-1: one positioned write of `bytes` at `offset`, one charged attempt,
/// never retried. A short write refuses.
pub fn write_chunk(
    file: &File,
    offset: u64,
    bytes: &[u8],
    work: &mut WorkScope<'_>,
) -> Result<(), WorkFailure<ChunkWriteError>> {
    supported_io().map_err(|e| WorkFailure::Operation(ChunkWriteError::Io(e)))?;
    let offset = libc::off_t::try_from(offset)
        .map_err(|_| WorkFailure::Operation(ChunkWriteError::Io(invalid_input())))?;
    work.charge(NATIVE_CALL)?;
    // SAFETY: a live descriptor and a valid buffer of bytes.len() bytes.
    let n = unsafe { libc::pwrite(file.as_raw_fd(), bytes.as_ptr().cast(), bytes.len(), offset) };
    if n < 0 {
        return Err(WorkFailure::Operation(ChunkWriteError::Io(
            io::Error::last_os_error(),
        )));
    }
    if n as usize != bytes.len() {
        return Err(WorkFailure::Operation(ChunkWriteError::Short {
            written: n as usize,
        }));
    }
    Ok(())
}

/// P-2: one `fchmod` of a retained file or directory handle.
pub fn set_mode(
    file: &File,
    mode: u32,
    work: &mut WorkScope<'_>,
) -> Result<(), WorkFailure<io::Error>> {
    supported_io().map_err(WorkFailure::Operation)?;
    let mode = libc::mode_t::try_from(mode & 0o7777)
        .map_err(|_| WorkFailure::Operation(invalid_input()))?;
    work.charge(NATIVE_CALL)?;
    // SAFETY: a live descriptor and plain permission bits.
    if unsafe { libc::fchmod(file.as_raw_fd(), mode) } != 0 {
        return Err(WorkFailure::Operation(io::Error::last_os_error()));
    }
    Ok(())
}

/// A completed standalone barrier on one exact handle (LD-CIP-10;
/// amendment CI-A1-a). It witnesses only that one barrier completed on that
/// handle object: it claims nothing about bytes or read-back. Its fields are
/// private and only `barrier_file` constructs one.
#[derive(Debug)]
pub struct StandaloneBarrierReceipt<'file> {
    file: &'file File,
}
impl StandaloneBarrierReceipt<'_> {
    /// Exact borrowed handle-object identity, not inode or path equality.
    pub fn is_for(&self, file: &File) -> bool {
        std::ptr::eq(self.file, file)
    }
}

/// P-3: one standalone file barrier, `F_FULLFSYNC` on macOS, charged first,
/// with no fallback and no retry.
pub fn barrier_file<'file>(
    file: &'file File,
    work: &mut WorkScope<'_>,
) -> Result<StandaloneBarrierReceipt<'file>, WorkFailure<io::Error>> {
    supported_io().map_err(WorkFailure::Operation)?;
    work.charge(NATIVE_CALL)?;
    full_flush(file).map_err(WorkFailure::Operation)?;
    Ok(StandaloneBarrierReceipt { file })
}
#[cfg(target_os = "macos")]
fn full_flush(file: &File) -> io::Result<()> {
    // SAFETY: a live descriptor; F_FULLFSYNC takes no further argument.
    if unsafe { libc::fcntl(file.as_raw_fd(), libc::F_FULLFSYNC) } != 0 {
        return Err(io::Error::last_os_error());
    }
    Ok(())
}
#[cfg(not(target_os = "macos"))]
fn full_flush(_: &File) -> io::Result<()> {
    supported_io()
}

/// P-4: one `symlinkat` of `target` at `name` in `directory`. Both are
/// copied onto the stack; LAW's owned record for the target is the caller's.
pub fn create_symlink(
    directory: &RetainedDirectory,
    name: &str,
    target: &str,
    work: &mut WorkScope<'_>,
) -> Result<(), WorkFailure<io::Error>> {
    supported_io().map_err(WorkFailure::Operation)?;
    let invalid = || WorkFailure::Operation(invalid_input());
    let name = component(name).ok_or_else(invalid)?;
    let target = StackName::of(target.as_bytes()).ok_or_else(invalid)?;
    work.charge(NATIVE_CALL)?;
    // SAFETY: a live directory descriptor and two NUL-terminated strings.
    if unsafe {
        libc::symlinkat(
            target.as_ptr(),
            directory.as_file().as_raw_fd(),
            name.as_ptr(),
        )
    } != 0
    {
        return Err(WorkFailure::Operation(io::Error::last_os_error()));
    }
    Ok(())
}

/// The largest link target the profile admits, plus one byte to observe a
/// longer target.
pub const LINK_BUFFER: usize = 101;

/// P-4: one `readlinkat` of `name` in `directory` into the caller's owned
/// 101-byte buffer. Returns the target's length; a result of 101 means the
/// target is longer than any admitted one.
pub fn read_link(
    directory: &RetainedDirectory,
    name: &str,
    buffer: &mut [u8; LINK_BUFFER],
    work: &mut WorkScope<'_>,
) -> Result<usize, WorkFailure<TreeOpenError>> {
    supported().map_err(WorkFailure::Operation)?;
    let name = component(name).ok_or(WorkFailure::Operation(TreeOpenError::Name))?;
    work.charge(NATIVE_CALL)?;
    // SAFETY: a live directory descriptor, one component, and a buffer of
    // LINK_BUFFER writable bytes.
    let n = unsafe {
        libc::readlinkat(
            directory.as_file().as_raw_fd(),
            name.as_ptr(),
            buffer.as_mut_ptr().cast(),
            LINK_BUFFER,
        )
    };
    if n < 0 {
        let error = io::Error::last_os_error();
        return Err(WorkFailure::Operation(match error.raw_os_error() {
            Some(libc::ENOENT) => TreeOpenError::Absent,
            // Not a symlink: the entry is of another kind.
            Some(libc::EINVAL) => TreeOpenError::NotRegular,
            _ => TreeOpenError::Io(error),
        }));
    }
    Ok(n as usize)
}

/// A pin's lock mode (LAW item 7): shared for a pin, exclusive for GC's
/// probe. Both are non-blocking.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum PinMode {
    Shared,
    Exclusive,
}

/// A held pin (LD-CIP-11). It owns the descriptor, never duplicates it, and
/// releases the lock by closing it on drop: no `LOCK_UN` call.
#[derive(Debug)]
pub struct PinLock {
    file: TreeFile,
    mode: PinMode,
}
impl PinLock {
    pub fn mode(&self) -> PinMode {
        self.mode
    }
    pub fn file(&self) -> &TreeFile {
        &self.file
    }
}

/// P-6: one charged `flock(LOCK_NB)` on a file this module opened
/// (no-follow, close-on-exec, kind-checked). Busy (`EWOULDBLOCK`) hands the
/// file back with no retry; any other failure is `Io`.
pub fn try_pin(
    file: TreeFile,
    mode: PinMode,
    work: &mut WorkScope<'_>,
) -> Result<Result<PinLock, TreeFile>, WorkFailure<io::Error>> {
    supported_io().map_err(WorkFailure::Operation)?;
    work.charge(NATIVE_CALL)?;
    let operation = match mode {
        PinMode::Shared => libc::LOCK_SH,
        PinMode::Exclusive => libc::LOCK_EX,
    } | libc::LOCK_NB;
    // SAFETY: a live owned descriptor and a fixed flock selector.
    if unsafe { libc::flock(file.file.as_raw_fd(), operation) } != 0 {
        let error = io::Error::last_os_error();
        if error
            .raw_os_error()
            .is_some_and(|code| code == libc::EWOULDBLOCK || code == libc::EAGAIN)
        {
            return Ok(Err(file));
        }
        return Err(WorkFailure::Operation(error));
    }
    Ok(Ok(PinLock { file, mode }))
}

#[cfg(test)]
#[path = "component_tree_tests.rs"]
mod tests;
