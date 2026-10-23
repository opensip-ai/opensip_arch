// M3-C r8 item 1 (unit C1a2; C1a plan r4 section C1a2): the snapshot's
// capture session, and the one source-read site (C1-T2).
//
// One session per request, opened after X2's handoff releases the fence and
// before the first source read. Every source read before sealing goes through
// it, keyed by logical path: a pre-walk capture (B2's marker and manifest
// reads, C2's layout reads) opens through `SnapshotRoot::open`, and the walk
// hands each regular file in its extent, open. Each file is read once, to
// EOF, through the session's one reused 64 KiB buffer, every chunk going to
// the pending custody blob (LD-C1A-3). The read's before and after samples
// must be equal and the length read must be the size, else
// `ChangedDuringRead`; each read call is one attempt, charged first, within
// the file's envelope `2·⌈size / 64 KiB⌉ + 2`. Nothing is retried.
//
// A captured path the walk reaches is never read again: the walk's
// observation through its enumerating parent is compared with the capture's
// (device, inode, size, mtime, ctime), and a difference refuses (C1-T24). A
// capture the walk never reaches stays a leftover, which sealing refuses if
// a resolved input depends on it (C1a3). Each reached path's origin is kept
// as an operational side record, outside identity (C1-T25).
use crate::candidate_custody::{CandidateCustody, CustodyError};
use opensip_platform::{DescriptorMetadata, WorkCost, WorkFailure, WorkScope};
use opensip_security::snapshot_read_set::open_pruned;
use opensip_security::snapshot_source::{
    STATUS_COST, SnapshotCustody, SnapshotRefusal, SnapshotRoot, SourceFile, owned_record,
};
use opensip_security::snapshot_walk::{
    SnapshotExtent, SnapshotStop, SnapshotWalkReport, WalkEvidence, walk_snapshot_retaining,
};
use std::collections::BTreeMap;
use std::io::{self, Read};

/// The session's one read buffer.
pub(crate) const READ_CHUNK: usize = 65_536;
/// The bounded reader's first growth (`work_reader.rs`, `CHUNK`).
const FIRST_GROWTH: usize = 4096;
/// One read attempt: its edge, charged before the call.
const ATTEMPT: WorkCost = WorkCost {
    objects: 0,
    edges: 1,
    bytes: 0,
};

/// The buffer's charge under item 2's pricing recipe: the bounded reader's
/// growth rule (`work_reader.rs`, `next_buffer`: 4 KiB, then doubling, to
/// the buffer's size), each requested growth charged in full and never
/// refunded, as one object. Charged once per session; the buffer itself is
/// allocated once, at its final size.
pub(crate) fn buffer_cost() -> WorkCost {
    let (mut current, mut bytes) = (0usize, 0usize);
    while current < READ_CHUNK {
        current = if current == 0 {
            FIRST_GROWTH
        } else {
            current * 2
        }
        .min(READ_CHUNK);
        bytes += current;
    }
    WorkCost {
        objects: 1,
        edges: 0,
        bytes,
    }
}

/// A file's read-attempt envelope (C1a plan r3): `2·⌈size / 64 KiB⌉ + 2`.
pub(crate) fn attempt_envelope(size: u64) -> u64 {
    size.div_ceil(READ_CHUNK as u64)
        .saturating_mul(2)
        .saturating_add(2)
}

/// A descriptor observation as the session compares it (item 1): device,
/// inode, size, mtime and ctime.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) struct Stamp {
    device: u64,
    inode: u64,
    size: u64,
    modified: (i64, i64),
    changed: (i64, i64),
}
impl Stamp {
    fn of(metadata: &DescriptorMetadata) -> Self {
        Self {
            device: metadata.device,
            inode: metadata.inode,
            size: metadata.size,
            modified: metadata.modified,
            changed: metadata.changed,
        }
    }
}

/// Where an inventory path's bytes came from (C1-T25): operational, outside
/// identity. `ReadSet` is C1c's.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum CaptureOrigin {
    Walk,
    ReadSet,
}

/// One kept capture: its custody digest and length, and the observation it
/// was read under. `origin` is set once the walk (or the read set) reaches
/// it; a capture never reached is a leftover.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct Capture {
    pub(crate) sha256: [u8; 32],
    pub(crate) bytes: u64,
    pub(crate) stamp: Stamp,
    pub(crate) origin: Option<CaptureOrigin>,
}

/// Why the session refused. None is retried, and none leaves a partial
/// capture.
#[derive(Debug)]
pub(crate) enum ReadError {
    /// The walk's or the opener's own refusal.
    Refused(SnapshotRefusal),
    Custody(CustodyError),
    /// The descriptor's sample at the read's start is not the observation
    /// it was opened under.
    ChangedBeforeRead(String),
    /// The samples before and after the read differ, or the length read is
    /// not the size.
    ChangedDuringRead(String),
    /// The file's read-attempt envelope ran out before EOF.
    ReadAttemptsExhausted(String),
    /// A captured path, reached by the walk, is no longer the captured
    /// object (C1-T24).
    ChangedSinceCapture(String),
    Read {
        path: String,
        error: io::Error,
    },
}
pub(crate) type ReadFailure = WorkFailure<ReadError>;

fn lift<E>(failure: WorkFailure<E>, wrap: impl FnOnce(E) -> ReadError) -> ReadFailure {
    match failure {
        WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
        WorkFailure::Operation(error) => WorkFailure::Operation(wrap(error)),
    }
}
fn refuse<T>(error: ReadError) -> Result<T, ReadFailure> {
    Err(WorkFailure::Operation(error))
}

/// The request's capture session: the custody, the one buffer, the kept
/// captures, by logical path, and the walk's evidence once it has walked
/// (the read set's, unit C1c-0).
pub(crate) struct CaptureSession {
    custody: CandidateCustody,
    buffer: Vec<u8>,
    captures: BTreeMap<String, Capture>,
    evidence: Option<WalkEvidence>,
}

// Unit tests only: the read-pass spy (C1A-T1), counting `read_once` passes
// per path on this thread, and a hook at two points of each read: before its
// first sample, and before each read call, where it may inject that call's
// error (the change, attempt and I/O controls).
#[cfg(test)]
pub(crate) enum ReadPoint {
    BeforeSample,
    BeforeCall(u64),
}
#[cfg(test)]
pub(crate) type ReadHook = Option<Box<dyn FnMut(&str, ReadPoint) -> Option<io::Error>>>;
#[cfg(test)]
thread_local! {
    pub(crate) static READ_PASSES: std::cell::RefCell<BTreeMap<String, u32>> =
        const { std::cell::RefCell::new(BTreeMap::new()) };
    pub(crate) static READ_HOOK: std::cell::RefCell<ReadHook> =
        const { std::cell::RefCell::new(None) };
}
#[cfg(test)]
fn hook(path: &str, point: ReadPoint) -> Option<io::Error> {
    READ_HOOK.with_borrow_mut(|h| h.as_mut().and_then(|h| h(path, point)))
}
impl std::fmt::Debug for CaptureSession {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("CaptureSession")
            .field("captures", &self.captures.len())
            .finish_non_exhaustive()
    }
}

impl CaptureSession {
    /// Open the session over `custody`, charging its buffer once.
    pub(crate) fn open(
        custody: CandidateCustody,
        work: &mut WorkScope<'_>,
    ) -> Result<Self, ReadFailure> {
        work.charge::<ReadError>(buffer_cost())?;
        Ok(Self {
            custody,
            buffer: vec![0; READ_CHUNK],
            captures: BTreeMap::new(),
            evidence: None,
        })
    }

    /// A pre-walk capture of `path` (B2's and C2's reads): the kept capture
    /// if there is one, never a second read; else `SnapshotRoot::open`, then
    /// the one read.
    pub(crate) fn capture(
        &mut self,
        root: &SnapshotRoot<'_>,
        path: &str,
        custody: SnapshotCustody<'_>,
        work: &mut WorkScope<'_>,
    ) -> Result<&Capture, ReadFailure> {
        if !self.captures.contains_key(path) {
            let source = root
                .open(path, custody, work)
                .map_err(|f| lift(f, ReadError::Refused))?;
            let (owned_path, capture) =
                read_once(&mut self.custody, &mut self.buffer, source, None, work)?;
            work.charge::<ReadError>(owned_record(std::mem::size_of::<Capture>()))?;
            self.captures.insert(owned_path, capture);
        }
        Ok(&self.captures[path])
    }

    /// A pre-walk capture of `path` in a dependency tree (C2's layout reads;
    /// M3-C r8 item 3, unit C1c-0): the kept capture if there is one, never
    /// a second read; else `open_pruned`, S3 custody above the dependency
    /// anchor and the descriptor discipline below it, then the one read.
    pub(crate) fn capture_pruned(
        &mut self,
        root: &SnapshotRoot<'_>,
        path: &str,
        extent: &SnapshotExtent<'_>,
        custody: SnapshotCustody<'_>,
        work: &mut WorkScope<'_>,
    ) -> Result<&Capture, ReadFailure> {
        if !self.captures.contains_key(path) {
            let source = open_pruned(root, path, extent, custody, work)
                .map_err(|f| lift(f, ReadError::Refused))?;
            let (owned_path, capture) =
                read_once(&mut self.custody, &mut self.buffer, source, None, work)?;
            work.charge::<ReadError>(owned_record(std::mem::size_of::<Capture>()))?;
            self.captures.insert(owned_path, capture);
        }
        Ok(&self.captures[path])
    }

    /// The extent walk (item 2), each handed regular file read once into
    /// custody, or, when already captured, compared and reused. The walk's
    /// evidence is kept for the read set (unit C1c-0).
    pub(crate) fn walk(
        &mut self,
        root: &SnapshotRoot<'_>,
        custody: SnapshotCustody<'_>,
        extent: &SnapshotExtent<'_>,
        work: &mut WorkScope<'_>,
    ) -> Result<SnapshotWalkReport, ReadFailure> {
        let Self {
            custody: store,
            buffer,
            captures,
            evidence,
        } = self;
        let mut visit = |source: SourceFile, work: &mut WorkScope<'_>| -> Result<(), ReadFailure> {
            if let Some(capture) = captures.get_mut(source.path()) {
                // No second read: the walk's observation through the
                // enumerating parent must be the capture's (C1-T24).
                if capture.stamp != Stamp::of(source.observation()) {
                    return refuse(ReadError::ChangedSinceCapture(source.into_parts().0));
                }
                capture.origin = Some(CaptureOrigin::Walk);
                return Ok(());
            }
            let (path, capture) =
                read_once(store, buffer, source, Some(CaptureOrigin::Walk), work)?;
            work.charge::<ReadError>(owned_record(std::mem::size_of::<Capture>()))?;
            captures.insert(path, capture);
            Ok(())
        };
        let (report, walked) = walk_snapshot_retaining(root, custody, extent, &mut visit, work)
            .map_err(|failure| match failure {
                WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
                WorkFailure::Operation(SnapshotStop::Refused(refusal)) => {
                    WorkFailure::Operation(ReadError::Refused(refusal))
                }
                WorkFailure::Operation(SnapshotStop::Visitor(failure)) => failure,
            })?;
        // The evidence moves into the session: no copy and no charge.
        *evidence = Some(walked);
        Ok(report)
    }

    /// The reached captures in path byte order: the inventory's rows and
    /// their side record.
    pub(crate) fn inventory(&self) -> impl Iterator<Item = (&str, &Capture)> {
        self.captures
            .iter()
            .filter(|(_, c)| c.origin.is_some())
            .map(|(p, c)| (p.as_str(), c))
    }
    /// The walk's evidence (unit C1c-0), once the session has walked.
    pub(crate) fn walk_evidence(&self) -> Option<&WalkEvidence> {
        self.evidence.as_ref()
    }
    /// The captures the walk never reached.
    pub(crate) fn leftovers(&self) -> impl Iterator<Item = &str> {
        self.captures
            .iter()
            .filter(|(_, c)| c.origin.is_none())
            .map(|(p, _)| p.as_str())
    }
    pub(crate) fn custody(&self) -> &CandidateCustody {
        &self.custody
    }
    /// The session's custody, for sealing's inventory blob (unit C1a3).
    pub(crate) fn custody_mut(&mut self) -> &mut CandidateCustody {
        &mut self.custody
    }
    /// The session's buffer, for `CandidateCustody::open`'s verification.
    pub(crate) fn custody_and_buffer(&mut self) -> (&CandidateCustody, &mut [u8]) {
        (&self.custody, &mut self.buffer)
    }
}

/// The one read of one source file: its sample at the start must be its
/// observation; each read call is one attempt within the envelope; every
/// chunk goes to the pending blob; the sample after EOF must equal the one
/// before and the length read must be the size. Then the blob is committed.
/// The source is consumed: its own path, already charged when it was made,
/// moves into the capture's key or into the refusal, so no refusal copies a
/// path (r2, C1A2-R1-RF-3).
fn read_once(
    custody: &mut CandidateCustody,
    buffer: &mut [u8],
    mut source: SourceFile,
    origin: Option<CaptureOrigin>,
    work: &mut WorkScope<'_>,
) -> Result<(String, Capture), ReadFailure> {
    #[cfg(test)]
    READ_PASSES.with_borrow_mut(|passes| *passes.entry(source.path().to_owned()).or_default() += 1);
    #[cfg(test)]
    hook(source.path(), ReadPoint::BeforeSample);
    let observed = Stamp::of(source.observation());
    let sample = |file: &std::fs::File, work: &mut WorkScope<'_>| {
        work.run(STATUS_COST, |_| {
            opensip_platform::observe_descriptor_metadata(file).map_err(|error| {
                WorkFailure::Operation(ReadError::Read {
                    path: String::new(),
                    error,
                })
            })
        })
    };
    let before = sample(source.file(), work)?;
    if Stamp::of(&before) != observed {
        return refuse(ReadError::ChangedBeforeRead(source.into_parts().0));
    }
    let size = before.size;
    let envelope = attempt_envelope(size);
    let mut pending = custody
        .begin(size, work)
        .map_err(|f| lift(f, ReadError::Custody))?;
    let (mut attempts, mut total) = (0u64, 0u64);
    loop {
        if attempts == envelope {
            return refuse(ReadError::ReadAttemptsExhausted(source.into_parts().0));
        }
        work.charge::<ReadError>(ATTEMPT)?;
        attempts += 1;
        #[cfg(test)]
        let injected = hook(source.path(), ReadPoint::BeforeCall(attempts));
        #[cfg(not(test))]
        let injected: Option<io::Error> = None;
        let result = match injected {
            Some(error) => Err(error),
            None => source.file().read(buffer),
        };
        let n = match result {
            Ok(0) => break,
            Ok(n) => n,
            Err(error) if error.kind() == io::ErrorKind::Interrupted => continue,
            Err(error) => {
                return refuse(ReadError::Read {
                    path: source.into_parts().0,
                    error,
                });
            }
        };
        total += n as u64;
        if total > size {
            return refuse(ReadError::ChangedDuringRead(source.into_parts().0));
        }
        pending
            .write(&buffer[..n], work)
            .map_err(|f| lift(f, ReadError::Custody))?;
    }
    let after = sample(source.file(), work)?;
    if after != before || total != size {
        return refuse(ReadError::ChangedDuringRead(source.into_parts().0));
    }
    let custodied = pending
        .commit(work)
        .map_err(|f| lift(f, ReadError::Custody))?;
    Ok((
        source.into_parts().0,
        Capture {
            sha256: custodied.sha256,
            bytes: custodied.bytes,
            stamp: observed,
            origin,
        },
    ))
}

#[cfg(test)]
#[path = "snapshot_tests.rs"]
pub(crate) mod tests;
