// Law CI r5 item 3 (unit CI-1; component installation plan r3, sub-unit
// CI-1): the one archive profile, `opensip-archive-profile.1`, adopted exactly
// as PKG-AP defines it, by reference to PKG at its pinned SHA-256
// (`PROFILE_SOURCE`, `PROFILE_SOURCE_SHA256`). Adopting it applies neither
// PKG nor DR-120.
//
// Admission is PKG-AP's `admissionChecks`, as hostile-input parsing. Every
// 512-byte header is recomputed from its TreeCommitment row and compared
// octet for octet; the members are in bijection with the rows, in the
// profile's order; every body has its row's length and SHA-256, every pad and
// both trailer blocks are NUL, and nothing follows them. The archive length
// is PKG-AP's `archiveLength`, computed from the rows before anything is
// read, and every capacity is checked then.
//
// The verifier is a streaming state machine over caller-supplied bytes. It
// allocates nothing: the expected header is a fixed array in its state, the
// digests are fixed-size accumulators, and file bytes are lent back as
// slices of the caller's own buffer. It executes, interprets and decompresses
// nothing, and a member's name is never used as a path: a header is only
// ever equal or unequal to its row's, and callers use the row.
//
// The emitter, PKG-AP's byte algorithm, exists only for fixtures, under the
// joint fixture predicate (plan LD-CIP-3).
use opensip_identity::RawSha256;

/// The one profile token (LAW item 2; PKG-AP `id`).
pub const PROFILE_ID: &str = "opensip-archive-profile.1";
/// The profile's definition, adopted by reference: PKG, whose `archiveProfile`
/// member is PKG-AP (LAW, short names).
pub const PROFILE_SOURCE: &str = "docs/coop/artifacts/component-packaging-contract.v14.json";
pub const PROFILE_SOURCE_SHA256: &str =
    "8321d527843c63592d8e4fd49c3df0ace690da0bcbcd1e268464e578fe30424c";

/// PKG-AP `headerLayout.blockSize`.
const BLOCK: usize = 512;
/// PKG-AP `trailer`: exactly two zero blocks.
const TRAILER: usize = 2 * BLOCK;
/// PKG-AP `pathBytes`: `name[0:100]`.
pub const MAX_PATH_BYTES: usize = 100;
/// PKG-AP `linkTargetBytes`: `linkname[0:100]`.
pub const MAX_LINK_TARGET_BYTES: usize = 100;
/// PKG-AP `numericCapacity.mode`: octal7nul encodes 0..=2,097,151.
pub const MAX_MODE: u32 = 0o7_777_777;
/// PKG-AP `numericCapacity.size`: octal11nul encodes 0..=8,589,934,591.
pub const MAX_SIZE: u64 = 0o77_777_777_777;
/// Entries per tree: 1 to 100,000, the admitted manifest shape
/// (`generated/component_manifest_shape.rs`, the tree's `entries`).
pub const MAX_ENTRIES: usize = 100_000;

/// One header field of PKG-AP's `headerLayout`, in layout order.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum HeaderField {
    Name,
    Mode,
    Uid,
    Gid,
    Size,
    Mtime,
    Chksum,
    Typeflag,
    Linkname,
    Magic,
    Version,
    Uname,
    Gname,
    Devmajor,
    Devminor,
    Prefix,
    Pad,
}

/// PKG-AP `headerLayout.fields`, exactly: field, name, offset and length. The
/// lane compares this table with PKG's own.
pub const LAYOUT: [(HeaderField, &str, usize, usize); 17] = [
    (HeaderField::Name, "name", 0, 100),
    (HeaderField::Mode, "mode", 100, 8),
    (HeaderField::Uid, "uid", 108, 8),
    (HeaderField::Gid, "gid", 116, 8),
    (HeaderField::Size, "size", 124, 12),
    (HeaderField::Mtime, "mtime", 136, 12),
    (HeaderField::Chksum, "chksum", 148, 8),
    (HeaderField::Typeflag, "typeflag", 156, 1),
    (HeaderField::Linkname, "linkname", 157, 100),
    (HeaderField::Magic, "magic", 257, 6),
    (HeaderField::Version, "version", 263, 2),
    (HeaderField::Uname, "uname", 265, 32),
    (HeaderField::Gname, "gname", 297, 32),
    (HeaderField::Devmajor, "devmajor", 329, 8),
    (HeaderField::Devminor, "devminor", 337, 8),
    (HeaderField::Prefix, "prefix", 345, 155),
    (HeaderField::Pad, "pad", 500, 12),
];
const CHKSUM: usize = 148;
const CHKSUM_END: usize = 156;

/// The field holding header offset `offset` (`0..512`).
pub fn field_at(offset: usize) -> HeaderField {
    let mut field = HeaderField::Name;
    for (f, _, start, _) in LAYOUT {
        if offset >= start {
            field = f;
        }
    }
    field
}

/// One TreeCommitment row, borrowed from the validated manifest. `mode` is the
/// integer value of the row's octal `mode` string; `sha256` is its digest's
/// raw bytes.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct TreeRow<'a> {
    pub path: &'a str,
    pub mode: u32,
    pub kind: RowKind<'a>,
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum RowKind<'a> {
    File { length: u64, sha256: [u8; 32] },
    Dir,
    Symlink { target: &'a str },
}

/// The rows of one tree, in the profile's member order (PKG-AP `ordering`:
/// Unicode code-point order of the NFC path, which is UTF-8 byte order).
/// `ArchivePlan::new` checks that order rather than trusting it, so a caller's
/// mis-ordered rows refuse instead of admitting a non-canonical archive.
pub trait ArchiveRows {
    fn count(&self) -> usize;
    /// The row at member position `position < count()`.
    fn row(&self, position: usize) -> TreeRow<'_>;
}
impl ArchiveRows for [TreeRow<'_>] {
    fn count(&self) -> usize {
        self.len()
    }
    fn row(&self, position: usize) -> TreeRow<'_> {
        self[position]
    }
}

/// PKG-AP's four profile-capacity refusals (`doesNotMintSchemaCaps`). A tree
/// that exceeds one is admissible metadata that profile 1 cannot deliver:
/// LAW item 8's `archive-capacity`.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Capacity {
    PathExceedsUstarName,
    LinkTargetExceedsUstarLinkname,
    ModeExceedsUstarField,
    SizeExceedsUstarField,
}
impl Capacity {
    /// PKG-AP's own token for the refusal.
    pub fn token(self) -> &'static str {
        match self {
            Self::PathExceedsUstarName => "PATH-EXCEEDS-USTAR-NAME",
            Self::LinkTargetExceedsUstarLinkname => "LINKTARGET-EXCEEDS-USTAR-LINKNAME",
            Self::ModeExceedsUstarField => "MODE-EXCEEDS-USTAR-FIELD",
            Self::SizeExceedsUstarField => "SIZE-EXCEEDS-USTAR-FIELD",
        }
    }
}

/// Row properties the manifest's admission already guarantees. Seeing one
/// here is the caller's bug, never the archive's.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum RowsInvariant {
    /// Not 1 to 100,000 rows.
    Count,
    /// Not strictly after the previous row's path, in byte order.
    Order,
    /// An empty path or link target, or one containing NUL.
    Text,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ArchiveRefusal {
    /// A profile capacity, before any read (`archive-capacity`).
    Capacity { position: usize, capacity: Capacity },
    /// The caller's rows broke an admitted-manifest property.
    Rows {
        position: usize,
        invariant: RowsInvariant,
    },
    /// The archive's length is not `archiveLength`; judged before any read.
    Length { expected: u64, observed: u64 },
    /// A header octet differs from the recomputed header. `field` is the first
    /// differing field other than `chksum`, or `chksum` when only it differs.
    Header { position: usize, field: HeaderField },
    /// A file body's SHA-256 is not its row's.
    FileDigest { position: usize },
    /// A body pad byte is not NUL.
    Pad { position: usize },
    /// A trailer byte is not NUL.
    Trailer,
    /// Bytes follow the trailer.
    TrailingBytes,
    /// The input ended before the trailer did.
    Truncated { consumed: u64 },
    /// SHA-256's message-length domain. Unreachable: `archiveLength` is at most
    /// about 2^50 bytes, far below it.
    DigestDomain,
}

/// One verified step of the stream.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ArchiveEvent<'a> {
    /// Member `position`'s header equals its row's.
    Header { position: usize },
    /// Body bytes of file member `position`, a slice of the caller's input.
    /// They are unverified until that member's `MemberEnd`.
    FileBytes { position: usize, bytes: &'a [u8] },
    /// Member `position` is complete: for a file, its length and SHA-256 equal
    /// the row's and its pad is NUL.
    MemberEnd { position: usize },
    /// The trailer is exact. `sha256` is the raw SHA-256 of every archive byte,
    /// to compare with the release's `archiveDigest`.
    End { sha256: [u8; 32] },
}

/// The rows of one tree, admitted against the profile's capacities, with its
/// `archiveLength`.
pub struct ArchivePlan<'r, R: ArchiveRows + ?Sized> {
    rows: &'r R,
    count: usize,
    length: u64,
}
impl<'r, R: ArchiveRows + ?Sized> ArchivePlan<'r, R> {
    /// Checks every row and computes PKG-AP's `archiveLength`:
    /// `512·N + Σ_files 512·⌈length/512⌉ + 1024`, with checked arithmetic.
    pub fn new(rows: &'r R) -> Result<Self, ArchiveRefusal> {
        let count = rows.count();
        if count == 0 || count > MAX_ENTRIES {
            return Err(ArchiveRefusal::Rows {
                position: 0,
                invariant: RowsInvariant::Count,
            });
        }
        let mut length = TRAILER as u64;
        for position in 0..count {
            let row = rows.row(position);
            let refuse = |capacity| ArchiveRefusal::Capacity { position, capacity };
            let invariant = |invariant| ArchiveRefusal::Rows {
                position,
                invariant,
            };
            if !text_ok(row.path) {
                return Err(invariant(RowsInvariant::Text));
            }
            if position > 0 && rows.row(position - 1).path.as_bytes() >= row.path.as_bytes() {
                return Err(invariant(RowsInvariant::Order));
            }
            if row.path.len() > MAX_PATH_BYTES {
                return Err(refuse(Capacity::PathExceedsUstarName));
            }
            if row.mode > MAX_MODE {
                return Err(refuse(Capacity::ModeExceedsUstarField));
            }
            let body = match row.kind {
                RowKind::File { length, .. } if length > MAX_SIZE => {
                    return Err(refuse(Capacity::SizeExceedsUstarField));
                }
                RowKind::File { length, .. } => padded(length),
                RowKind::Symlink { target } if !text_ok(target) => {
                    return Err(invariant(RowsInvariant::Text));
                }
                RowKind::Symlink { target } if target.len() > MAX_LINK_TARGET_BYTES => {
                    return Err(refuse(Capacity::LinkTargetExceedsUstarLinkname));
                }
                RowKind::Symlink { .. } | RowKind::Dir => 0,
            };
            length = length
                .checked_add(BLOCK as u64)
                .and_then(|l| l.checked_add(body))
                .ok_or(ArchiveRefusal::DigestDomain)?;
        }
        Ok(Self {
            rows,
            count,
            length,
        })
    }
    /// PKG-AP's `archiveLength` for these rows.
    pub fn length(&self) -> u64 {
        self.length
    }
    /// The most bytes a reader needs: the length plus one, to observe EOF.
    pub fn read_limit(&self) -> u64 {
        self.length + 1
    }
    /// The archive's observed size, judged before any byte is read.
    pub fn check_length(&self, observed: u64) -> Result<(), ArchiveRefusal> {
        if observed != self.length {
            return Err(ArchiveRefusal::Length {
                expected: self.length,
                observed,
            });
        }
        Ok(())
    }
    pub fn verifier(&self) -> ArchiveVerifier<'r, R> {
        ArchiveVerifier {
            rows: self.rows,
            count: self.count,
            position: 0,
            phase: Phase::Header,
            expected: header(&self.rows.row(0)),
            filled: 0,
            mismatch: None,
            chksum_differs: false,
            file: None,
            archive: Some(RawSha256::new()),
            consumed: 0,
        }
    }
}

fn text_ok(s: &str) -> bool {
    !s.is_empty() && !s.as_bytes().contains(&0)
}
fn padded(length: u64) -> u64 {
    length.div_ceil(BLOCK as u64) * BLOCK as u64
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Phase {
    Header,
    Body { remaining: u64 },
    Pad { remaining: usize },
    End,
    Trailer { seen: usize },
    Done,
}

/// The streaming verifier. Each step consumes it and, unless it refuses,
/// returns it: a refused stream leaves no verifier that could continue.
#[must_use]
pub struct ArchiveVerifier<'r, R: ArchiveRows + ?Sized> {
    rows: &'r R,
    count: usize,
    position: usize,
    phase: Phase,
    expected: [u8; BLOCK],
    filled: usize,
    mismatch: Option<usize>,
    chksum_differs: bool,
    file: Option<RawSha256>,
    archive: Option<RawSha256>,
    consumed: u64,
}
impl<'r, R: ArchiveRows + ?Sized> ArchiveVerifier<'r, R> {
    /// Consumes bytes from the front of `input` and returns the next event,
    /// or `None` once `input` is exhausted without completing one.
    pub fn step<'a>(
        mut self,
        input: &mut &'a [u8],
    ) -> Result<(Self, Option<ArchiveEvent<'a>>), ArchiveRefusal> {
        let position = self.position;
        match self.phase {
            Phase::Header => {
                let take = (BLOCK - self.filled).min(input.len());
                let (bytes, rest) = input.split_at(take);
                for (i, &b) in bytes.iter().enumerate() {
                    let offset = self.filled + i;
                    if b != self.expected[offset] {
                        if (CHKSUM..CHKSUM_END).contains(&offset) {
                            self.chksum_differs = true;
                        } else if self.mismatch.is_none() {
                            self.mismatch = Some(offset);
                        }
                    }
                }
                self.digest(bytes)?;
                *input = rest;
                self.filled += take;
                if self.filled < BLOCK {
                    return Ok((self, None));
                }
                if let Some(offset) = self.mismatch {
                    return Err(ArchiveRefusal::Header {
                        position,
                        field: field_at(offset),
                    });
                }
                if self.chksum_differs {
                    return Err(ArchiveRefusal::Header {
                        position,
                        field: HeaderField::Chksum,
                    });
                }
                self.phase = match self.rows.row(position).kind {
                    RowKind::File { length, .. } => {
                        self.file = Some(RawSha256::new());
                        Phase::Body { remaining: length }
                    }
                    RowKind::Dir | RowKind::Symlink { .. } => Phase::End,
                };
                Ok((self, Some(ArchiveEvent::Header { position })))
            }
            Phase::Body { remaining } => {
                if remaining > 0 && input.is_empty() {
                    return Ok((self, None));
                }
                let take = remaining.min(input.len() as u64) as usize;
                let (bytes, rest) = input.split_at(take);
                self.digest(bytes)?;
                let file = self.file.take().ok_or(ArchiveRefusal::DigestDomain)?;
                let file = file
                    .update(bytes)
                    .map_err(|_| ArchiveRefusal::DigestDomain)?;
                *input = rest;
                let remaining = remaining - take as u64;
                if remaining > 0 {
                    self.file = Some(file);
                    self.phase = Phase::Body { remaining };
                    return Ok((self, Some(ArchiveEvent::FileBytes { position, bytes })));
                }
                let RowKind::File { length, sha256 } = self.rows.row(position).kind else {
                    return Err(ArchiveRefusal::DigestDomain);
                };
                if file.finish() != sha256 {
                    return Err(ArchiveRefusal::FileDigest { position });
                }
                self.phase = Phase::Pad {
                    remaining: (padded(length) - length) as usize,
                };
                if bytes.is_empty() {
                    // An empty file has no body event.
                    return self.step(input);
                }
                Ok((self, Some(ArchiveEvent::FileBytes { position, bytes })))
            }
            Phase::Pad { remaining } => {
                let take = remaining.min(input.len());
                let (bytes, rest) = input.split_at(take);
                if bytes.iter().any(|&b| b != 0) {
                    return Err(ArchiveRefusal::Pad { position });
                }
                self.digest(bytes)?;
                *input = rest;
                if remaining > take {
                    self.phase = Phase::Pad {
                        remaining: remaining - take,
                    };
                    return Ok((self, None));
                }
                self.phase = Phase::End;
                self.step(input)
            }
            Phase::End => {
                self.position += 1;
                self.filled = 0;
                self.mismatch = None;
                self.chksum_differs = false;
                if self.position < self.count {
                    self.expected = header(&self.rows.row(self.position));
                    self.phase = Phase::Header;
                } else {
                    self.phase = Phase::Trailer { seen: 0 };
                }
                Ok((self, Some(ArchiveEvent::MemberEnd { position })))
            }
            Phase::Trailer { seen } => {
                let take = (TRAILER - seen).min(input.len());
                let (bytes, rest) = input.split_at(take);
                if bytes.iter().any(|&b| b != 0) {
                    return Err(ArchiveRefusal::Trailer);
                }
                self.digest(bytes)?;
                *input = rest;
                if seen + take < TRAILER {
                    self.phase = Phase::Trailer { seen: seen + take };
                    return Ok((self, None));
                }
                self.phase = Phase::Done;
                let sha256 = self
                    .archive
                    .take()
                    .ok_or(ArchiveRefusal::DigestDomain)?
                    .finish();
                Ok((self, Some(ArchiveEvent::End { sha256 })))
            }
            Phase::Done => {
                if !input.is_empty() {
                    return Err(ArchiveRefusal::TrailingBytes);
                }
                Ok((self, None))
            }
        }
    }
    /// At the input's end: the archive is complete only if its trailer was.
    pub fn finish(self) -> Result<(), ArchiveRefusal> {
        if self.phase != Phase::Done {
            return Err(ArchiveRefusal::Truncated {
                consumed: self.consumed,
            });
        }
        Ok(())
    }
    /// Bytes consumed so far.
    pub fn consumed(&self) -> u64 {
        self.consumed
    }
    fn digest(&mut self, bytes: &[u8]) -> Result<(), ArchiveRefusal> {
        let archive = self.archive.take().ok_or(ArchiveRefusal::DigestDomain)?;
        self.archive = Some(
            archive
                .update(bytes)
                .map_err(|_| ArchiveRefusal::DigestDomain)?,
        );
        self.consumed += bytes.len() as u64;
        Ok(())
    }
}

/// PKG-AP's `headerLayout` for one admitted row: the only byte representation.
fn header(row: &TreeRow<'_>) -> [u8; BLOCK] {
    let mut h = [0u8; BLOCK];
    h[..row.path.len()].copy_from_slice(row.path.as_bytes());
    octal(&mut h[100..108], row.mode as u64);
    octal(&mut h[108..116], 0);
    octal(&mut h[116..124], 0);
    let (size, typeflag) = match row.kind {
        RowKind::File { length, .. } => (length, b'0'),
        RowKind::Dir => (0, b'5'),
        RowKind::Symlink { target } => {
            h[157..157 + target.len()].copy_from_slice(target.as_bytes());
            (0, b'2')
        }
    };
    octal(&mut h[124..136], size);
    octal(&mut h[136..148], 0);
    h[156] = typeflag;
    h[257..263].copy_from_slice(b"ustar\0");
    h[263..265].copy_from_slice(b"00");
    octal(&mut h[329..337], 0);
    octal(&mut h[337..345], 0);
    // `checksumComputation`: the sum with the eight chksum octets as spaces,
    // stored as six octal digits, NUL, space. At most 512·255 < 8^6.
    h[CHKSUM..CHKSUM_END].fill(b' ');
    let sum = h.iter().map(|&b| b as u64).sum::<u64>();
    octal(&mut h[CHKSUM..CHKSUM + 7], sum);
    h
}
/// `octal7nul` / `octal11nul`: zero-padded octal digits, then NUL.
fn octal(field: &mut [u8], value: u64) {
    let digits = field.len() - 1;
    let mut v = value;
    for d in field[..digits].iter_mut().rev() {
        *d = b'0' + (v & 7) as u8;
        v >>= 3;
    }
    field[digits] = 0;
}

/// The emitter's refusals (PKG-AP `byteAlgorithm.inputs` and `bodyRules`).
#[cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))]
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum EmitRefusal {
    Plan(ArchiveRefusal),
    /// `SIZE-OR-DIGEST-MISMATCH`: a file's payload is missing, or its length
    /// or SHA-256 is not the row's.
    SizeOrDigestMismatch {
        path: String,
    },
    /// A payload keyed by a dir or symlink row, by no row, or twice.
    Payload {
        path: String,
    },
}

/// PKG-AP's byte algorithm, for fixtures only: `entries` in any order, and
/// `payloads` keyed by file path. Members are sorted by code point (step 1),
/// then each header, body and pad is written, then the trailer (steps 2-3).
#[cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))]
pub fn emit(entries: &[TreeRow<'_>], payloads: &[(&str, &[u8])]) -> Result<Vec<u8>, EmitRefusal> {
    let mut rows = entries.to_vec();
    rows.sort_by(|a, b| a.path.as_bytes().cmp(b.path.as_bytes()));
    let plan = ArchivePlan::new(&rows[..]).map_err(EmitRefusal::Plan)?;
    for (i, (path, _)) in payloads.iter().enumerate() {
        let file = rows
            .iter()
            .any(|r| r.path == *path && matches!(r.kind, RowKind::File { .. }));
        if !file || payloads[..i].iter().any(|(p, _)| p == path) {
            return Err(EmitRefusal::Payload {
                path: path.to_string(),
            });
        }
    }
    let mut out = Vec::with_capacity(plan.length() as usize);
    for row in &rows {
        out.extend_from_slice(&header(row));
        if let RowKind::File { length, sha256 } = row.kind {
            let body = payloads
                .iter()
                .find(|(p, _)| *p == row.path)
                .map(|(_, b)| *b)
                .filter(|b| b.len() as u64 == length && opensip_identity::raw_sha256(b) == sha256)
                .ok_or_else(|| EmitRefusal::SizeOrDigestMismatch {
                    path: row.path.to_string(),
                })?;
            out.extend_from_slice(body);
            out.resize(out.len() + (padded(length) - length) as usize, 0);
        }
    }
    out.resize(out.len() + TRAILER, 0);
    debug_assert_eq!(out.len() as u64, plan.length());
    Ok(out)
}

#[cfg(test)]
#[path = "archive_profile_tests.rs"]
mod tests;
