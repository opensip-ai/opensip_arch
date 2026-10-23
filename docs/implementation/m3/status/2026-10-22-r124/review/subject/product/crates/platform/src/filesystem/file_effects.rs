//! Charged private regular-file creation and write for law 467 (decisions 1.6
//! and 4): exclusive `O_EXCL` creation that distinguishes a raw `EEXIST`, and
//! a bounded write, length and read-back verification, then `F_FULLFSYNC` with
//! no fallback, returning a receipt bound to the exact file handle. Mechanisms
//! only: which names, modes, ACLs, owners or decoders a caller accepts, and
//! what a raw `EEXIST` means, belong to the caller. Every cost is charged or
//! spent before the first native call or allocation it covers. Opaque kernel
//! and libc work and latency are not counted. No custody or authority.
use super::path_binding::status_read_cost;
use super::{NATIVE_PUBLICATION, PublicationOps, RetainedDirectory};
use crate::{ReservedPostchecks, WorkCost, WorkFailure, WorkScope};
use std::fs::File;
use std::io;
use std::os::fd::{AsRawFd, FromRawFd};
use std::os::unix::fs::FileExt;

/// Bytes per write call and per read-back call, and the verify buffer size.
const VERIFY_BUFFER: usize = 65_536;

/// Published work of one `create_exclusive_regular_accounted` or `_reserved`
/// of `name`, computed without allocation. Objects: the NUL-terminated name
/// copy and the new file descriptor. Edges: the `O_CREAT | O_EXCL` `openat`
/// and the `fchmod` to `0600`. Bytes: the name and its NUL.
pub fn create_exclusive_regular_cost(name: &str) -> WorkCost {
    WorkCost {
        objects: 2,
        edges: 2,
        bytes: name.len().saturating_add(1),
    }
}

/// Published work of one `write_new_regular_accounted` or `_reserved` of `len`
/// bytes, with `n = ceil(len / 64 KiB)`: `n` positioned writes of at most
/// 64 KiB each, one status read for the length check, `n + 1` positioned
/// reads into the 64 KiB verify buffer (the last must find the end), and one
/// file barrier (`F_FULLFSYNC` on macOS, `fsync` on Linux), never a fallback.
/// Bytes: the verify buffer and the status buffer. The caller's bytes are
/// borrowed, not copied. The receipt is a borrowed value with no allocation.
pub fn write_new_regular_cost(len: usize) -> WorkCost {
    let chunks = len.div_ceil(VERIFY_BUFFER);
    let status = status_read_cost();
    WorkCost {
        objects: 0,
        edges: chunks
            .saturating_mul(2)
            .saturating_add(1)
            .saturating_add(status.edges)
            .saturating_add(1),
        bytes: VERIFY_BUFFER.saturating_add(status.bytes),
    }
}

/// A successful charged exclusive regular-file creation. `EntryExists` is
/// only a raw `EEXIST` from `openat`: some entry, of any kind (a symlink
/// included), was already at the name and this call made nothing. It leaves
/// the work scope open and is not admission of that entry.
#[derive(Debug)]
pub enum ExclusiveRegularOutcome {
    /// `openat(O_CREAT | O_EXCL | O_NOFOLLOW)` made the file, now mode `0600`.
    Created(File),
    EntryExists,
}

/// A refused charged exclusive regular-file creation. Every variant fails
/// the work scope.
#[derive(Debug)]
pub enum ExclusiveRegularError {
    /// The name is not one component. No native call was made.
    Name(io::Error),
    /// `openat` failed with an error other than `EEXIST`; this call made nothing.
    Create(io::Error),
    /// `openat` created the file, then `fchmod` failed. The file may remain.
    AfterCreate(io::Error),
}

/// Records that the bytes written through one exact file handle were read
/// back equal and its file barrier completed. The borrow keeps that handle
/// alive. It proves no name binding, directory durability, custody or authority.
#[derive(Debug)]
pub struct FileBarrierReceipt<'file> {
    file: &'file File,
    byte_len: usize,
}
impl FileBarrierReceipt<'_> {
    pub fn byte_len(&self) -> usize {
        self.byte_len
    }
    /// Exact borrowed handle-object identity, not inode or path equality. A
    /// separately opened handle to the same file does not match.
    pub fn is_for(&self, file: &File) -> bool {
        std::ptr::eq(self.file, file)
    }
}

/// A refused charged write. Every variant fails the work scope. Bytes may
/// have reached the file before any of them; nothing is truncated or removed.
#[derive(Debug)]
pub enum NewRegularWriteError {
    /// A positioned write failed or wrote short.
    Write(io::Error),
    /// The status read after the writes failed.
    Status(io::Error),
    /// The handle is not a regular file of exactly the written length.
    Length { observed: u64 },
    /// A positioned read-back call failed or returned short.
    ReadBack(io::Error),
    /// The bytes read back differ, or content follows the written length.
    Mismatch,
    /// The file barrier failed. There is no fallback and no retry.
    Barrier(io::Error),
}

impl RetainedDirectory {
    /// `create_exclusive_regular`, charged to `work` for
    /// `create_exclusive_regular_cost` before the name is copied or any native
    /// call is made. The steps are unchanged: no-follow `O_CREAT | O_EXCL |
    /// O_CLOEXEC` `openat` at mode `0600`, then `fchmod` to `0600`. A raw
    /// `EEXIST` is `Ok(EntryExists)` and leaves the scope open; every other
    /// outcome is a typed [`ExclusiveRegularError`] that fails the scope. No
    /// ACL is added and an existing entry is never changed.
    pub fn create_exclusive_regular_accounted(
        &self,
        name: &str,
        work: &mut WorkScope<'_>,
    ) -> Result<ExclusiveRegularOutcome, WorkFailure<ExclusiveRegularError>> {
        work.run(create_exclusive_regular_cost(name), |_| {
            self.create_exclusive_regular_charged(name)
                .map_err(WorkFailure::Operation)
        })
    }
    /// `create_exclusive_regular_accounted`, spending its cost from an
    /// existing reservation instead, with no second outer charge. A ledger
    /// that cannot reserve it stops before the name copy and `openat`.
    pub fn create_exclusive_regular_reserved(
        &self,
        name: &str,
        post: &mut ReservedPostchecks<'_>,
    ) -> Result<ExclusiveRegularOutcome, WorkFailure<ExclusiveRegularError>> {
        post.scope(|post| {
            post.spend(create_exclusive_regular_cost(name))?;
            self.create_exclusive_regular_charged(name)
                .map_err(WorkFailure::Operation)
        })
    }
    fn create_exclusive_regular_charged(
        &self,
        name: &str,
    ) -> Result<ExclusiveRegularOutcome, ExclusiveRegularError> {
        use std::os::unix::fs::PermissionsExt;
        let name = super::single_component(name).map_err(ExclusiveRegularError::Name)?;
        let created = crate::crash_barrier!(primitive, "create", step, {
            // SAFETY: the parent descriptor and the single-component name are
            // live. O_EXCL creates the entry without following a symlink.
            let fd = unsafe {
                libc::openat(
                    self.0.as_raw_fd(),
                    name.as_ptr(),
                    libc::O_RDWR
                        | libc::O_CREAT
                        | libc::O_EXCL
                        | libc::O_NOFOLLOW
                        | libc::O_CLOEXEC,
                    0o600,
                )
            };
            if fd < 0 {
                Err(io::Error::last_os_error())
            } else {
                // SAFETY: openat returned one newly owned descriptor.
                Ok(unsafe { File::from_raw_fd(fd) })
            }
        });
        let file = match created {
            Ok(file) => file,
            Err(error) if error.raw_os_error() == Some(libc::EEXIST) => {
                return Ok(ExclusiveRegularOutcome::EntryExists);
            }
            Err(error) => return Err(ExclusiveRegularError::Create(error)),
        };
        file.set_permissions(std::fs::Permissions::from_mode(0o600))
            .map_err(ExclusiveRegularError::AfterCreate)?;
        Ok(ExclusiveRegularOutcome::Created(file))
    }
}

/// Write `bytes` at offset zero of a new regular file, charged to `work` for
/// `write_new_regular_cost(bytes.len())` before the first write. Then check
/// the length by `fstat`, read every byte back in bounded chunks and compare,
/// confirm the end, and take the file barrier with no fallback. The receipt
/// names `file`. Any failure fails the scope and keeps the charge.
pub fn write_new_regular_accounted<'file>(
    file: &'file File,
    bytes: &[u8],
    work: &mut WorkScope<'_>,
) -> Result<FileBarrierReceipt<'file>, WorkFailure<NewRegularWriteError>> {
    work.run(write_new_regular_cost(bytes.len()), |_| {
        write_new_regular_charged(file, bytes, native_file_barrier).map_err(WorkFailure::Operation)
    })
}

/// `write_new_regular_accounted`, spending its cost from an existing
/// reservation before the first write, with no second outer charge.
pub fn write_new_regular_reserved<'file>(
    file: &'file File,
    bytes: &[u8],
    post: &mut ReservedPostchecks<'_>,
) -> Result<FileBarrierReceipt<'file>, WorkFailure<NewRegularWriteError>> {
    write_new_regular_reserved_with(file, bytes, post, native_file_barrier)
}

fn write_new_regular_reserved_with<'file>(
    file: &'file File,
    bytes: &[u8],
    post: &mut ReservedPostchecks<'_>,
    barrier: impl FnOnce(&File) -> io::Result<()>,
) -> Result<FileBarrierReceipt<'file>, WorkFailure<NewRegularWriteError>> {
    post.scope(|post| {
        post.spend(write_new_regular_cost(bytes.len()))?;
        write_new_regular_charged(file, bytes, barrier).map_err(WorkFailure::Operation)
    })
}

// Private seam: `barrier` is the native file barrier in production; tests
// inject its failure. There is no fallback path to select.
fn write_new_regular_charged<'file>(
    file: &'file File,
    bytes: &[u8],
    barrier: impl FnOnce(&File) -> io::Result<()>,
) -> Result<FileBarrierReceipt<'file>, NewRegularWriteError> {
    use NewRegularWriteError as E;
    crate::crash_barrier!(primitive, "write", write, bytes, |part| write_at_zero(
        file, part
    ))
    .map_err(E::Write)?;
    let status = file.metadata().map_err(E::Status)?;
    if !status.is_file() || status.len() != bytes.len() as u64 {
        return Err(E::Length {
            observed: status.len(),
        });
    }
    let mut buffer = [0u8; VERIFY_BUFFER];
    for (index, part) in bytes.chunks(VERIFY_BUFFER).enumerate() {
        let read = file
            .read_at(&mut buffer[..part.len()], (index * VERIFY_BUFFER) as u64)
            .map_err(E::ReadBack)?;
        if read != part.len() {
            return Err(E::ReadBack(io::Error::new(
                io::ErrorKind::UnexpectedEof,
                "short positioned read-back",
            )));
        }
        if &buffer[..read] != part {
            return Err(E::Mismatch);
        }
    }
    if file
        .read_at(&mut buffer[..1], bytes.len() as u64)
        .map_err(E::ReadBack)?
        != 0
    {
        return Err(E::Mismatch);
    }
    barrier(file).map_err(E::Barrier)?;
    Ok(FileBarrierReceipt {
        file,
        byte_len: bytes.len(),
    })
}

// The positioned writes from offset zero, in bounded chunks.
fn write_at_zero(file: &File, bytes: &[u8]) -> io::Result<()> {
    for (index, part) in bytes.chunks(VERIFY_BUFFER).enumerate() {
        let written = file.write_at(part, (index * VERIFY_BUFFER) as u64)?;
        if written != part.len() {
            return Err(io::Error::new(
                io::ErrorKind::WriteZero,
                "short positioned write",
            ));
        }
    }
    Ok(())
}

/// The existing file barrier: `F_FULLFSYNC` on macOS with no fallback (law 467
/// item 4), `fsync` on Linux.
fn native_file_barrier(file: &File) -> io::Result<()> {
    NATIVE_PUBLICATION.sync_file(file)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::{WorkBudgetError, WorkLedger};
    use std::cell::Cell;
    use std::fs;
    use std::os::unix::fs::{MetadataExt, PermissionsExt, symlink};
    use std::path::PathBuf;

    struct Fixture(PathBuf);
    impl Fixture {
        fn new() -> Self {
            let nonce = crate::request_entropy()
                .unwrap()
                .iter()
                .map(|b| format!("{b:02x}"))
                .collect::<String>();
            // On macOS, stay outside the per-user temporary directory: other
            // tests sample its metadata as a path component and would see
            // these fixtures come and go. /tmp is not one of its ancestors.
            #[cfg(target_os = "macos")]
            let base = PathBuf::from("/tmp");
            #[cfg(not(target_os = "macos"))]
            let base = std::env::temp_dir();
            let path = base.join(format!("opensip-file-effects467-{nonce}"));
            fs::create_dir(&path).unwrap();
            fs::set_permissions(&path, fs::Permissions::from_mode(0o700)).unwrap();
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
    fn short_edge(cost: WorkCost) -> WorkCost {
        WorkCost {
            objects: cost.objects.max(1),
            edges: cost.edges - 1,
            bytes: cost.bytes,
        }
    }
    fn short_byte(cost: WorkCost) -> WorkCost {
        WorkCost {
            objects: cost.objects.max(1),
            edges: cost.edges,
            bytes: cost.bytes - 1,
        }
    }
    fn created(outcome: ExclusiveRegularOutcome) -> File {
        match outcome {
            ExclusiveRegularOutcome::Created(file) => file,
            other => panic!("expected creation, got {other:?}"),
        }
    }
    fn pattern(len: usize) -> Vec<u8> {
        (0..len).map(|i| (i * 31 + 7) as u8).collect()
    }

    #[test]
    fn create_and_write_costs_are_pinned() {
        let create = create_exclusive_regular_cost("lifecycle.fence");
        assert_eq!(
            create,
            WorkCost {
                objects: 2,
                edges: 2,
                bytes: 16
            }
        );
        let status = status_read_cost();
        // (len, writes, reads): ceil(len / 64 KiB) writes and that plus one reads.
        for (len, writes, reads) in [
            (0, 0, 1),
            (1, 1, 2),
            (65_536, 1, 2),
            (65_537, 2, 3),
            (200_000, 4, 5),
        ] {
            let cost = write_new_regular_cost(len);
            assert_eq!(cost.objects, 0, "{len}");
            assert_eq!(cost.edges, writes + 1 + reads + 1, "{len}");
            assert_eq!(cost.bytes, 65_536 + status.bytes, "{len}");
        }
        // Saturating arithmetic: the largest length prices without overflow.
        assert!(write_new_regular_cost(usize::MAX).edges > usize::MAX / 65_536);
    }

    #[test]
    fn charged_create_makes_a_private_regular_file_and_charges_exactly() {
        let f = Fixture::new();
        let dir = f.held();
        let mut ledger = WorkLedger::new();
        let file = created(
            ledger
                .effect(
                    WorkCost::default(),
                    create_exclusive_regular_cost("state.v1"),
                    |post| dir.create_exclusive_regular_reserved("state.v1", post),
                )
                .unwrap(),
        );
        assert_eq!(ledger.used(), create_exclusive_regular_cost("state.v1"));
        assert!(!ledger.is_failed());
        let held = file.metadata().unwrap();
        let named = fs::symlink_metadata(f.0.join("state.v1")).unwrap();
        assert!(held.is_file());
        assert_eq!((held.dev(), held.ino()), (named.dev(), named.ino()));
        assert_eq!(named.mode() & 0o777, 0o600);
        assert_eq!((named.len(), named.nlink()), (0, 1));
        let mut ledger = WorkLedger::new();
        created(
            ledger
                .scope(|work| dir.create_exclusive_regular_accounted("other", work))
                .unwrap(),
        );
        assert_eq!(ledger.used(), create_exclusive_regular_cost("other"));
    }

    #[test]
    fn charged_create_raw_eexist_is_an_open_scope_observation() {
        let f = Fixture::new();
        fs::write(f.0.join("file"), b"keep").unwrap();
        fs::set_permissions(f.0.join("file"), fs::Permissions::from_mode(0o644)).unwrap();
        fs::create_dir(f.0.join("dir")).unwrap();
        symlink("missing-target", f.0.join("dangling")).unwrap();
        let dir = f.held();
        let mut ledger = WorkLedger::new();
        let mut expected = WorkCost::default();
        for name in ["file", "dir", "dangling"] {
            let outcome = ledger
                .scope(|work| dir.create_exclusive_regular_accounted(name, work))
                .unwrap();
            assert!(
                matches!(outcome, ExclusiveRegularOutcome::EntryExists),
                "{name}"
            );
            expected = expected
                .checked_add(create_exclusive_regular_cost(name))
                .unwrap();
            assert_eq!(ledger.used(), expected);
            assert!(!ledger.is_failed());
        }
        assert_eq!(fs::read(f.0.join("file")).unwrap(), b"keep");
        assert_eq!(
            fs::metadata(f.0.join("file")).unwrap().mode() & 0o777,
            0o644
        );
        assert!(!f.0.join("missing-target").exists());
        // The unaccounted API still reports the same raw EEXIST as an io::Error.
        let raw = dir.create_exclusive_regular("file").unwrap_err();
        assert_eq!(raw.raw_os_error(), Some(libc::EEXIST));
    }

    #[test]
    fn charged_create_other_failures_are_typed_and_close_the_scope() {
        let f = Fixture::new();
        let dir = f.held();
        let mut ledger = WorkLedger::new();
        let result = ledger.scope(|work| dir.create_exclusive_regular_accounted("a/b", work));
        assert!(matches!(
            result,
            Err(WorkFailure::Operation(ExclusiveRegularError::Name(_)))
        ));
        assert!(ledger.is_failed());
        let gone = f.0.join("gone");
        fs::create_dir(&gone).unwrap();
        let orphan = RetainedDirectory::from_retained_handle(File::open(&gone).unwrap()).unwrap();
        fs::remove_dir(&gone).unwrap();
        let mut ledger = WorkLedger::new();
        let result = ledger.scope(|work| orphan.create_exclusive_regular_accounted("child", work));
        assert!(matches!(
            result,
            Err(WorkFailure::Operation(ExclusiveRegularError::Create(ref e)))
                if e.raw_os_error() != Some(libc::EEXIST)
        ));
        assert!(ledger.is_failed());
    }

    #[test]
    fn charged_create_one_edge_or_byte_short_refuses_before_openat() {
        let f = Fixture::new();
        let dir = f.held();
        let cost = create_exclusive_regular_cost("never");
        for (limits, expected) in [
            (short_edge(cost), WorkBudgetError::Edges),
            (short_byte(cost), WorkBudgetError::Bytes),
        ] {
            let mut ledger = WorkLedger::with_limits(limits).unwrap();
            let result = ledger.scope(|work| dir.create_exclusive_regular_accounted("never", work));
            assert!(matches!(result, Err(WorkFailure::Budget(ref e)) if *e == expected));
            assert_eq!(ledger.used(), WorkCost::default());
        }
        let mut ledger = WorkLedger::new();
        let result = ledger.effect(WorkCost::default(), short_edge(cost), |post| {
            dir.create_exclusive_regular_reserved("never", post)
        });
        assert!(matches!(
            result,
            Err(WorkFailure::Budget(WorkBudgetError::ReservedPostcheck))
        ));
        assert!(fs::symlink_metadata(f.0.join("never")).is_err());
    }

    #[test]
    fn charged_write_verifies_flushes_and_binds_the_receipt_to_its_file() {
        let f = Fixture::new();
        let dir = f.held();
        for (name, len) in [
            ("empty", 0),
            ("small", 11),
            ("edge", 65_536),
            ("large", 150_000),
        ] {
            let file = dir.create_exclusive_regular(name).unwrap();
            let bytes = pattern(len);
            let cost = write_new_regular_cost(len);
            let mut ledger = WorkLedger::new();
            let byte_len = ledger
                .effect(WorkCost::default(), cost, |post| {
                    let receipt = write_new_regular_reserved(&file, &bytes, post)?;
                    assert!(receipt.is_for(&file));
                    let other = File::open(f.0.join(name)).unwrap();
                    assert!(!receipt.is_for(&other));
                    Ok(receipt.byte_len())
                })
                .unwrap();
            assert_eq!(byte_len, len);
            assert_eq!(ledger.used(), cost);
            assert!(!ledger.is_failed());
            assert_eq!(fs::read(f.0.join(name)).unwrap(), bytes);
        }
        let file = dir.create_exclusive_regular("accounted").unwrap();
        let mut ledger = WorkLedger::new();
        ledger
            .scope(|work| write_new_regular_accounted(&file, b"x", work).map(|r| r.byte_len()))
            .unwrap();
        assert_eq!(ledger.used(), write_new_regular_cost(1));
    }

    #[test]
    fn charged_write_short_ledger_refuses_before_the_write() {
        let f = Fixture::new();
        let dir = f.held();
        let file = dir.create_exclusive_regular("never").unwrap();
        let cost = write_new_regular_cost(5);
        for (limits, expected) in [
            (short_edge(cost), WorkBudgetError::Edges),
            (short_byte(cost), WorkBudgetError::Bytes),
        ] {
            let mut ledger = WorkLedger::with_limits(limits).unwrap();
            let result = ledger.scope(|work| {
                write_new_regular_accounted(&file, b"never", work).map(|r| r.byte_len())
            });
            assert!(matches!(result, Err(WorkFailure::Budget(ref e)) if *e == expected));
        }
        let mut ledger = WorkLedger::new();
        let flushed = Cell::new(false);
        let result = ledger.effect(WorkCost::default(), short_edge(cost), |post| {
            write_new_regular_reserved_with(&file, b"never", post, |_| {
                flushed.set(true);
                Ok(())
            })
            .map(|r| r.byte_len())
        });
        assert!(matches!(
            result,
            Err(WorkFailure::Budget(WorkBudgetError::ReservedPostcheck))
        ));
        assert!(!flushed.get());
        assert!(ledger.is_failed());
        assert_eq!(fs::metadata(f.0.join("never")).unwrap().len(), 0);
    }

    #[test]
    fn charged_write_barrier_failure_is_an_error_with_no_fallback() {
        let f = Fixture::new();
        let dir = f.held();
        // Including the errors the directory barrier would treat as a named
        // unsupported F_FULLFSYNC: a file barrier has no fallback (law 467 item 4).
        for errno in [libc::EINVAL, libc::ENOTSUP, libc::ENOTTY, libc::EIO] {
            let name = format!("fail-{errno}");
            let file = dir.create_exclusive_regular(&name).unwrap();
            let calls = Cell::new(0);
            let mut ledger = WorkLedger::new();
            let result = ledger.effect(WorkCost::default(), write_new_regular_cost(3), |post| {
                write_new_regular_reserved_with(&file, b"abc", post, |_| {
                    calls.set(calls.get() + 1);
                    Err(io::Error::from_raw_os_error(errno))
                })
                .map(|r| r.byte_len())
            });
            assert!(
                matches!(result, Err(WorkFailure::Operation(NewRegularWriteError::Barrier(ref e)))
                    if e.raw_os_error() == Some(errno)),
                "{errno}: {result:?}"
            );
            assert_eq!(calls.get(), 1);
            assert_eq!(ledger.used(), write_new_regular_cost(3));
            assert!(ledger.is_failed());
            // Nothing is removed or truncated.
            assert_eq!(fs::read(f.0.join(&name)).unwrap(), b"abc");
        }
    }

    #[test]
    fn charged_write_refuses_a_length_or_content_it_did_not_write() {
        let f = Fixture::new();
        let dir = f.held();
        // Longer existing content: the length check refuses.
        fs::write(f.0.join("longer"), b"0123456789").unwrap();
        let file = fs::OpenOptions::new()
            .read(true)
            .write(true)
            .open(f.0.join("longer"))
            .unwrap();
        let mut ledger = WorkLedger::new();
        let result = ledger
            .scope(|work| write_new_regular_accounted(&file, b"abc", work).map(|r| r.byte_len()));
        assert!(matches!(
            result,
            Err(WorkFailure::Operation(NewRegularWriteError::Length {
                observed: 10
            }))
        ));
        // A write-only handle cannot read back: no barrier and no receipt.
        let _ = dir.create_exclusive_regular("write-only").unwrap();
        let file = fs::OpenOptions::new()
            .write(true)
            .open(f.0.join("write-only"))
            .unwrap();
        let mut ledger = WorkLedger::new();
        let result = ledger.effect(WorkCost::default(), write_new_regular_cost(3), |post| {
            write_new_regular_reserved_with(&file, b"abc", post, |_| panic!("barrier ran"))
                .map(|r| r.byte_len())
        });
        assert!(matches!(
            result,
            Err(WorkFailure::Operation(NewRegularWriteError::ReadBack(_)))
        ));
    }
}
