// M3-C r8 item 1 (unit C1a2; C1a plan r4 section C1a2): the invocation's
// candidate blob custody. Every source byte the snapshot reads goes here once,
// under its raw SHA-256, and every later consumer takes it from here.
//
// The custody directory is the caller's (LD-C1A-4: J1 chooses it, item
// 5.4(a); tests supply a private temporary directory), and it must be an
// empty directory private to the invoking user: 0700, the user's, and with a
// present ACL that grants no one else any right, inherit-only entries
// included (security's `admit_custody_directory`; r2, C1A2-R1-RF-1). So no
// other principal writes custody, which LD-C1A-9 rests on, and no custody
// file inherits a grant. The writer takes chunks
// (plan r2, RF-1), so it never holds or reads a source descriptor. A pending
// blob is a create-exclusive, no-follow temporary entry, mode 0600; its
// commit checks length and digest and places it under its digest hex by an
// exclusive rename. Custody is per invocation and starts empty, so a digest
// already committed is resolved from the in-memory set: the new temporary is
// unlinked and nothing is re-read (LD-C1A-9). `open` re-verifies kind, mode,
// length and digest by reading the custody file itself; this module reads
// nothing else. Every step is charged to the caller's ledger before it runs,
// and every native write is one charged attempt, never retried (r2,
// C1A2-R1-RF-2).
use opensip_identity::RawSha256;
use opensip_platform::{
    DirectoryVisitError, ExclusiveRegularError, ExclusiveRegularOutcome, ExclusiveRenameOutcome,
    RetainedDirectory, WorkCost, WorkFailure, WorkScope,
};
use opensip_security::snapshot_source::{
    CustodyDirectoryRefusal, STATUS_COST, admit_custody_directory, owned_record,
};
use std::collections::BTreeMap;
use std::fs::File;
use std::io::{self, Read, Seek, Write};

/// The read buffer `open`'s verification reads through, and the most one
/// verification read asks for.
pub(crate) const VERIFY_CHUNK: usize = 65_536;
/// One listing of the custody directory (the discovery walk's price).
const LISTING: WorkCost = WorkCost {
    objects: 2,
    edges: 3,
    bytes: 1024,
};
/// One entry visited in that listing.
const VISIT: WorkCost = WorkCost {
    objects: 0,
    edges: 1,
    bytes: 0,
};
/// One write attempt: one `write` call of one whole chunk. A short or
/// interrupted write refuses; nothing retries it.
const WRITE: WorkCost = WorkCost {
    objects: 0,
    edges: 1,
    bytes: 0,
};

/// Why custody refused. Every refusal is terminal for its blob.
#[derive(Debug)]
pub(crate) enum CustodyError {
    /// The directory is not private to the invoking user.
    Private(CustodyDirectoryRefusal),
    /// The directory is not empty, or could not be listed within its limits.
    Directory(&'static str),
    /// A pending entry could not be created.
    Create(io::Error),
    /// An entry was already at the pending name.
    PendingExists,
    /// The one write attempt failed, `Interrupted` included.
    Write(io::Error),
    /// The one write attempt wrote fewer bytes than the chunk.
    ShortWrite {
        chunk: usize,
        written: usize,
    },
    /// The bytes written are not the length the caller expected.
    LengthMismatch {
        expected: u64,
        written: u64,
    },
    /// The raw digest's bit-length domain was exceeded.
    Digest,
    /// An entry already holds the digest's name, though this invocation
    /// never committed it.
    Collision(String),
    Rename(io::Error),
    Unlink(io::Error),
    /// `open` of a digest this invocation never committed.
    NotCommitted,
    /// `open` found the custody file changed: its kind, mode, length or
    /// digest is not the committed one.
    Corrupted(&'static str),
    Io(io::Error),
}
pub(crate) type CustodyFailure = WorkFailure<CustodyError>;

fn io_failure(
    error: WorkFailure<io::Error>,
    wrap: fn(io::Error) -> CustodyError,
) -> CustodyFailure {
    match error {
        WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
        WorkFailure::Operation(error) => WorkFailure::Operation(wrap(error)),
    }
}
fn refuse<T>(error: CustodyError) -> Result<T, CustodyFailure> {
    Err(WorkFailure::Operation(error))
}

/// A committed blob: its raw SHA-256 and length. `duplicate` says the digest
/// was already in custody, so this commit stored nothing new.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) struct Custodied {
    pub(crate) sha256: [u8; 32],
    pub(crate) bytes: u64,
    pub(crate) duplicate: bool,
}

/// The digest's custody name: 64 lowercase hex characters.
pub(crate) fn digest_hex(sha256: &[u8; 32]) -> String {
    const HEX: &[u8; 16] = b"0123456789abcdef";
    let mut out = String::with_capacity(64);
    for byte in sha256 {
        out.push(HEX[(byte >> 4) as usize] as char);
        out.push(HEX[(byte & 15) as usize] as char);
    }
    out
}

/// The invocation's candidate blob custody.
pub(crate) struct CandidateCustody {
    dir: RetainedDirectory,
    uid: u32,
    committed: BTreeMap<[u8; 32], u64>,
    next: u64,
}
impl std::fmt::Debug for CandidateCustody {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("CandidateCustody")
            .field("committed", &self.committed.len())
            .finish_non_exhaustive()
    }
}

impl CandidateCustody {
    /// Custody over `dir`, which must be private to `uid` (judged from one
    /// charged ACL capture of its descriptor) and have no entry in it.
    pub(crate) fn new(
        dir: RetainedDirectory,
        uid: u32,
        work: &mut WorkScope<'_>,
    ) -> Result<Self, CustodyFailure> {
        admit_custody_directory(dir.as_file(), uid, work).map_err(|failure| match failure {
            WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
            WorkFailure::Operation(refusal) => {
                WorkFailure::Operation(CustodyError::Private(refusal))
            }
        })?;
        work.charge::<CustodyError>(LISTING)?;
        let mut names = 0usize;
        let visited = dir.visit_entry_names(4, 4096, |name| {
            work.charge::<CustodyError>(VISIT)?;
            if name != b"." && name != b".." {
                names += 1;
            }
            Ok(())
        });
        match visited {
            Ok(_) if names == 0 => {}
            Ok(_) | Err(DirectoryVisitError::EntryLimit | DirectoryVisitError::NameByteLimit) => {
                return refuse(CustodyError::Directory("not empty"));
            }
            Err(DirectoryVisitError::Visitor(failure)) => return Err(failure),
            Err(DirectoryVisitError::Native(error)) => return refuse(CustodyError::Io(error)),
            Err(DirectoryVisitError::InvalidLimits) => {
                return refuse(CustodyError::Directory("listing limits"));
            }
        }
        Ok(Self {
            dir,
            uid,
            committed: BTreeMap::new(),
            next: 0,
        })
    }

    /// Begin one blob of `expected` bytes: a new pending entry, created
    /// exclusively, never following a link.
    pub(crate) fn begin(
        &mut self,
        expected: u64,
        work: &mut WorkScope<'_>,
    ) -> Result<PendingBlob<'_>, CustodyFailure> {
        let name_bytes = "pending-".len() + decimal_len(self.next);
        work.charge::<CustodyError>(owned_record(name_bytes))?;
        let name = format!("pending-{}", self.next);
        self.next += 1;
        let file = match self
            .dir
            .create_exclusive_regular_accounted(&name, work)
            .map_err(|failure| match failure {
                WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
                WorkFailure::Operation(error) => {
                    WorkFailure::Operation(CustodyError::Create(match error {
                        ExclusiveRegularError::Name(e)
                        | ExclusiveRegularError::Create(e)
                        | ExclusiveRegularError::AfterCreate(e) => e,
                    }))
                }
            })? {
            ExclusiveRegularOutcome::Created(file) => file,
            ExclusiveRegularOutcome::EntryExists => return refuse(CustodyError::PendingExists),
        };
        Ok(PendingBlob {
            custody: self,
            name,
            file,
            digest: Some(RawSha256::new()),
            expected,
            written: 0,
        })
    }

    /// The committed blob `sha256`, opened and re-verified: a regular file,
    /// mode 0600, of the invoking user, of the committed length and digest.
    /// The returned descriptor is at offset zero.
    pub(crate) fn open(
        &self,
        sha256: &[u8; 32],
        buffer: &mut [u8],
        work: &mut WorkScope<'_>,
    ) -> Result<File, CustodyFailure> {
        let Some(&length) = self.committed.get(sha256) else {
            return refuse(CustodyError::NotCommitted);
        };
        work.charge::<CustodyError>(owned_record(64))?;
        let name = digest_hex(sha256);
        let mut file = work.run(RetainedDirectory::open_regular_cost(&name), |_| {
            self.dir
                .open_regular(&name)
                .map_err(|error| WorkFailure::Operation(CustodyError::Io(error)))
        })?;
        let sample = work.run(STATUS_COST, |_| {
            opensip_platform::observe_descriptor_metadata(&file)
                .map_err(|error| WorkFailure::Operation(CustodyError::Io(error)))
        })?;
        if sample.mode & 0o170_000 != 0o100_000
            || sample.mode & 0o7777 != 0o600
            || sample.uid != self.uid
        {
            return refuse(CustodyError::Corrupted("kind, mode or owner"));
        }
        if sample.size != length {
            return refuse(CustodyError::Corrupted("length"));
        }
        let chunk = buffer.len().min(VERIFY_CHUNK);
        let mut digest = RawSha256::new();
        let mut seen = 0u64;
        loop {
            work.charge::<CustodyError>(WorkCost {
                objects: 0,
                edges: 1,
                bytes: 0,
            })?;
            let n = match file.read(&mut buffer[..chunk]) {
                Ok(0) => break,
                Ok(n) => n,
                Err(error) if error.kind() == io::ErrorKind::Interrupted => continue,
                Err(error) => return refuse(CustodyError::Io(error)),
            };
            seen += n as u64;
            if seen > length {
                return refuse(CustodyError::Corrupted("length"));
            }
            digest = digest
                .update(&buffer[..n])
                .map_err(|_| WorkFailure::Operation(CustodyError::Digest))?;
        }
        // The associated form: host's structural pin keeps the method-call
        // spelling for finalization's commit alone.
        if seen != length || RawSha256::finish(digest) != *sha256 {
            return refuse(CustodyError::Corrupted("digest"));
        }
        work.charge::<CustodyError>(WorkCost {
            objects: 0,
            edges: 1,
            bytes: 0,
        })?;
        file.rewind()
            .map_err(|error| WorkFailure::Operation(CustodyError::Io(error)))?;
        Ok(file)
    }

    /// How many distinct blobs are committed.
    pub(crate) fn blob_count(&self) -> usize {
        self.committed.len()
    }
    /// Whether `sha256` is committed, and at what length.
    pub(crate) fn committed(&self, sha256: &[u8; 32]) -> Option<u64> {
        self.committed.get(sha256).copied()
    }
}

/// One blob being written: its pending entry, the running digest, and the
/// expected and written lengths.
pub(crate) struct PendingBlob<'c> {
    custody: &'c mut CandidateCustody,
    name: String,
    file: File,
    /// `None` only after a refused update, which ends the blob.
    digest: Option<RawSha256>,
    expected: u64,
    written: u64,
}
impl PendingBlob<'_> {
    /// Append one chunk in one charged write attempt: the whole chunk is
    /// written, then hashed. A short or failed write, `Interrupted`
    /// included, refuses and ends the blob; nothing retries it. Writing past
    /// the expected length refuses before the write.
    pub(crate) fn write(
        &mut self,
        chunk: &[u8],
        work: &mut WorkScope<'_>,
    ) -> Result<(), CustodyFailure> {
        work.charge::<CustodyError>(WRITE)?;
        let written = self.written + chunk.len() as u64;
        if written > self.expected {
            return refuse(CustodyError::LengthMismatch {
                expected: self.expected,
                written,
            });
        }
        let Some(digest) = self.digest.take() else {
            return refuse(CustodyError::Digest);
        };
        #[cfg(test)]
        let result = match write_hook(chunk.len()) {
            Some(WriteInjection::Fail(error)) => Err(error),
            Some(WriteInjection::Short(n)) => self.file.write(&chunk[..n]),
            None => self.file.write(chunk),
        };
        #[cfg(not(test))]
        let result = self.file.write(chunk);
        match result {
            Ok(n) if n == chunk.len() => {}
            Ok(n) => {
                return refuse(CustodyError::ShortWrite {
                    chunk: chunk.len(),
                    written: n,
                });
            }
            Err(error) => return refuse(CustodyError::Write(error)),
        }
        self.digest = Some(
            digest
                .update(chunk)
                .map_err(|_| WorkFailure::Operation(CustodyError::Digest))?,
        );
        self.written = written;
        Ok(())
    }

    /// Check the length, then place the blob under its digest hex by an
    /// exclusive rename; a digest already committed discards this one.
    pub(crate) fn commit(self, work: &mut WorkScope<'_>) -> Result<Custodied, CustodyFailure> {
        let Self {
            custody,
            name,
            file,
            digest,
            expected,
            written,
        } = self;
        if written != expected {
            return refuse(CustodyError::LengthMismatch { expected, written });
        }
        let Some(digest) = digest else {
            return refuse(CustodyError::Digest);
        };
        let sample = work.run(STATUS_COST, |_| {
            opensip_platform::observe_descriptor_metadata(&file)
                .map_err(|error| WorkFailure::Operation(CustodyError::Io(error)))
        })?;
        drop(file);
        if sample.size != expected {
            return refuse(CustodyError::LengthMismatch {
                expected,
                written: sample.size,
            });
        }
        let sha256 = RawSha256::finish(digest);
        if custody.committed.contains_key(&sha256) {
            custody
                .dir
                .unlink_entry_accounted(&name, work)
                .map_err(|e| io_failure(e, CustodyError::Unlink))?;
            return Ok(Custodied {
                sha256,
                bytes: expected,
                duplicate: true,
            });
        }
        work.charge::<CustodyError>(owned_record(64))?;
        let hex = digest_hex(&sha256);
        match custody
            .dir
            .rename_exclusive_accounted(&name, &hex, work)
            .map_err(|e| io_failure(e, CustodyError::Rename))?
        {
            ExclusiveRenameOutcome::Renamed => {}
            ExclusiveRenameOutcome::EntryExists => return refuse(CustodyError::Collision(hex)),
        }
        work.charge::<CustodyError>(owned_record(std::mem::size_of::<([u8; 32], u64)>()))?;
        custody.committed.insert(sha256, expected);
        Ok(Custodied {
            sha256,
            bytes: expected,
            duplicate: false,
        })
    }
}

/// A test's injected outcome for the next write attempt.
#[cfg(test)]
pub(crate) enum WriteInjection {
    Fail(io::Error),
    /// Write only this many of the chunk's bytes.
    Short(usize),
}
#[cfg(test)]
pub(crate) type WriteHook = Option<Box<dyn FnMut(usize) -> Option<WriteInjection>>>;
#[cfg(test)]
thread_local! {
    pub(crate) static WRITE_HOOK: std::cell::RefCell<WriteHook> =
        const { std::cell::RefCell::new(None) };
}
#[cfg(test)]
fn write_hook(chunk: usize) -> Option<WriteInjection> {
    WRITE_HOOK.with_borrow_mut(|h| h.as_mut().and_then(|h| h(chunk)))
}

fn decimal_len(mut n: u64) -> usize {
    let mut len = 1;
    while n >= 10 {
        n /= 10;
        len += 1;
    }
    len
}

#[cfg(test)]
#[path = "candidate_custody_tests.rs"]
pub(crate) mod tests;
