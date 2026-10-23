// M3-C r8 items 1, 4, 5 and 6 (unit C1a3; C1a plan r4 as amended by r5 and
// r6, section C1a3): sealing the walked snapshot into `snapshot2`.
//
// Item 6's order: (1) the walk, which the caller ran through the session;
// (2) the read set, empty until C1c (LD-C1A-6); (3) sort and uniqueness: the
// session's inventory is in path byte order and unique by construction, and
// sealing checks it; then the leftover captures and the project carrier's
// join; (4) the VCS observation (unit C1b-2; C1b plan r6): the lending's
// own subject, observed by C1b-1's Git reads on this ledger, sealed as
// schema 2 `none` or `git`, or schema 3 for admitted D15 members, with
// `dirty` a constant (LD-C1B-10); (5) the bounds,
// rows, descriptor and total bytes, each refusing `SnapshotBound`; (6)
// `H("snapshot", ..)` through `IdentityCandidate::from_json`, which admits
// against identity-v3's `$defs/snapshot` and checks the order.
//
// The canonical inventory and descriptor are written here byte for byte as
// the identity crate's canonical encoder writes them (a test compares them),
// so their exact lengths are known, and charged, before anything is
// allocated, and an over-bound descriptor is never built. The inventory is
// retained in candidate custody under its raw SHA-256, which is
// `sourceInventoryDigest` (item 4). No operational value enters a field.
use crate::candidate_custody::{Custodied, CustodyError};
use crate::configuration::ResolverInputV1;
use crate::snapshot::{CaptureSession, READ_CHUNK};
use opensip_identity::{
    CandidateError, IdentityCandidate, IdentityDomain, MAX_BYTES, RegisteredSchemas, raw_sha256,
};
use opensip_platform::{WorkFailure, WorkScope};
use opensip_security::discovery_export::AdmittedBoundaries;
use opensip_security::snapshot_source::{SnapshotCustody, SnapshotRoot, owned_record};
use opensip_security::snapshot_vcs::{
    COMMIT_HEX, CommitId, MemberCommit, VcsObservation, VcsRefusal, observe_vcs,
};
use opensip_security::snapshot_walk::{CarrierEntry, PROJECT_CARRIER, SnapshotWalkReport};

/// Item 5's row bound (IDS:2739; identity-v3 `source-inventory` `maxItems`).
pub(crate) const MAX_ROWS: u64 = 100_000;
/// Item 5's total-bytes bound: Rust3's retained `maxSnapshotTotalFileBytes`
/// (RPP:100; NE:2934), 8 GiB.
pub(crate) const MAX_TOTAL_BYTES: u64 = 8_589_934_592;
/// The schema evaluator's work bound for the one descriptor, as B1's
/// configuration admission bounds its own (`configuration.rs`).
const SCHEMA_BUDGET: usize = 64 * 1024 * 1024;

/// What B1 hands C1 of the project carrier (item 1 rule 2): absent, or
/// present with the SHA-256 of the exact captured bytes.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum ProjectCarrierObservation {
    Absent,
    Present { sha256: [u8; 32] },
}
impl ProjectCarrierObservation {
    /// The observation of B1's resolver input's project carrier.
    pub(crate) fn of(input: &ResolverInputV1) -> Self {
        match &input.project {
            None => Self::Absent,
            Some(carrier) => Self::Present {
                sha256: raw_sha256(&carrier.bytes),
            },
        }
    }
}

/// The carrier join's refusing transitions (item 1 rule 2's table).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum CarrierTransition {
    Digest,
    PresentAbsent,
    AbsentPresent,
    Type,
    Excluded,
}

/// Item 5's bounded fields.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum BoundField {
    Rows,
    Descriptor,
    TotalBytes,
}

/// Why sealing refused. Each is internal; their public projections are
/// J1's. None retries, and none mints a snapshot, a Plan or a Run.
#[derive(Debug)]
pub(crate) enum SealError {
    /// A capture the walk never reached (item 1): every capture is a
    /// resolved input's, so no leftover may stay uninventoried.
    LeftoverCapture(String),
    /// `SnapshotCarrierChanged {transition}` (item 1 rule 2).
    CarrierChanged(CarrierTransition),
    /// `SnapshotVcsPending` (LD-C1A-5, narrowed by C1b-2): the lending
    /// carries no tracking observation, the ephemeral route until J2c.
    VcsPending,
    /// The VCS observation refused (LD-C1B-8): C1b-1's typed refusal, whose
    /// route is J2's.
    Vcs(VcsRefusal),
    /// `SnapshotBound {field, observed, limit}` (item 5).
    Bound {
        field: BoundField,
        observed: u64,
        limit: u64,
    },
    /// The inventory blob could not be retained.
    Custody(CustodyError),
    /// The descriptor did not admit as identity-v3's snapshot.
    Identity(CandidateError),
    /// A sealing invariant failed: the session's inventory out of order, or
    /// an encoding longer than counted. Unreachable by construction.
    Internal(&'static str),
}
pub(crate) type SealFailure = WorkFailure<SealError>;
fn refuse<T>(error: SealError) -> Result<T, SealFailure> {
    Err(WorkFailure::Operation(error))
}

/// Sealing's bound inputs (item 6), none of them an operational value.
#[derive(Debug, Clone, Copy)]
pub(crate) struct SealInputs<'a> {
    /// X2's ProjectId, or J2c's fresh ephemeral draw.
    pub(crate) project_id: &'a str,
    /// B1's `resolvedConfigDigest`.
    pub(crate) resolved_config_digest: &'a str,
    /// B2's `scopeDigest` (`unit_scope_descriptor`).
    pub(crate) scope_digest: &'a str,
    pub(crate) carrier: ProjectCarrierObservation,
    /// Discovery's own record for this root (LD-C1B-3): its admitted D15
    /// member repositories, read as `member_repositories()`. Schema 3 applies
    /// exactly when that list is non-empty.
    pub(crate) boundaries: Option<&'a AdmittedBoundaries>,
}

/// A sealed snapshot: its id, the exact canonical descriptor, the inventory
/// digest and its custody blob, and the bounded counts.
#[derive(Debug)]
pub(crate) struct SealedSnapshot {
    pub(crate) snapshot2: String,
    pub(crate) descriptor: Vec<u8>,
    pub(crate) source_inventory_digest: [u8; 32],
    /// The canonical `vcs-observation` record `vcsDigest` names.
    pub(crate) vcs_record: Vec<u8>,
    pub(crate) inventory_blob: Custodied,
    pub(crate) rows: u64,
    pub(crate) total_bytes: u64,
}

/// The canonical encoder's length of one string (`canonical.rs` `string`).
fn string_len(text: &str) -> usize {
    2 + text
        .chars()
        .map(|c| match c {
            '"' | '\\' | '\u{8}' | '\u{c}' | '\n' | '\r' | '\t' => 2,
            '\0'..='\u{1f}' => 6,
            c => c.len_utf8(),
        })
        .sum::<usize>()
}
fn push_string(out: &mut Vec<u8>, text: &str) {
    const HEX: &[u8] = b"0123456789abcdef";
    out.push(b'"');
    for c in text.chars() {
        match c {
            '"' => out.extend_from_slice(b"\\\""),
            '\\' => out.extend_from_slice(b"\\\\"),
            '\u{8}' => out.extend_from_slice(b"\\b"),
            '\u{c}' => out.extend_from_slice(b"\\f"),
            '\n' => out.extend_from_slice(b"\\n"),
            '\r' => out.extend_from_slice(b"\\r"),
            '\t' => out.extend_from_slice(b"\\t"),
            '\0'..='\u{1f}' => {
                let b = c as u8;
                out.extend_from_slice(b"\\u00");
                out.push(HEX[(b >> 4) as usize]);
                out.push(HEX[(b & 15) as usize]);
            }
            c => out.extend_from_slice(c.encode_utf8(&mut [0; 4]).as_bytes()),
        }
    }
    out.push(b'"');
}
fn decimal_len(mut n: u64) -> usize {
    let mut len = 1;
    while n >= 10 {
        n /= 10;
        len += 1;
    }
    len
}
fn push_decimal(out: &mut Vec<u8>, n: u64) {
    let mut digits = [0u8; 20];
    let mut at = digits.len();
    let mut n = n;
    loop {
        at -= 1;
        digits[at] = b'0' + (n % 10) as u8;
        n /= 10;
        if n == 0 {
            break;
        }
    }
    out.extend_from_slice(&digits[at..]);
}

/// One inventory row's canonical length: `{"bytes":N,"path":P,"sha256":H}`,
/// its members in canonical key order.
fn row_len(path: &str, bytes: u64) -> usize {
    br#"{"bytes":"#.len()
        + decimal_len(bytes)
        + br#","path":"#.len()
        + string_len(path)
        + br#","sha256":"#.len()
        + 66
        + 1
}
/// Lowercase hex digits, written in place: sealing makes no digest-hex
/// temporary, so every byte it encodes lands in a buffer already charged.
const HEX: &[u8; 16] = b"0123456789abcdef";
fn hex_digits(digest: &[u8; 32]) -> [u8; 64] {
    let mut digits = [0u8; 64];
    for (at, byte) in digest.iter().enumerate() {
        digits[2 * at] = HEX[(byte >> 4) as usize];
        digits[2 * at + 1] = HEX[(byte & 0x0f) as usize];
    }
    digits
}
fn push_row(out: &mut Vec<u8>, path: &str, sha256: &[u8; 32], bytes: u64) {
    out.extend_from_slice(br#"{"bytes":"#);
    push_decimal(out, bytes);
    out.extend_from_slice(br#","path":"#);
    push_string(out, path);
    out.extend_from_slice(br#","sha256":""#);
    out.extend_from_slice(&hex_digits(sha256));
    out.extend_from_slice(br#""}"#);
}

/// The descriptor's canonical length around an inventory of `inventory`
/// bytes: `{"projectId":..,"resolvedConfigDigest":..,"schemaVersion":2,
/// "scopeDigest":..,"sourceInventory":[..],"vcsDigest":H}`.
fn descriptor_len(inputs: &SealInputs<'_>, inventory: usize) -> usize {
    br#"{"projectId":"#.len()
        + string_len(inputs.project_id)
        + br#","resolvedConfigDigest":"#.len()
        + string_len(inputs.resolved_config_digest)
        + br#","schemaVersion":2,"scopeDigest":"#.len()
        + string_len(inputs.scope_digest)
        + br#","sourceInventory":"#.len()
        + inventory
        + br#","vcsDigest":"#.len()
        + 66
        + 1
}
fn push_descriptor(out: &mut Vec<u8>, inputs: &SealInputs<'_>, inventory: &[u8], vcs: &[u8; 64]) {
    out.extend_from_slice(br#"{"projectId":"#);
    push_string(out, inputs.project_id);
    out.extend_from_slice(br#","resolvedConfigDigest":"#);
    push_string(out, inputs.resolved_config_digest);
    out.extend_from_slice(br#","schemaVersion":2,"scopeDigest":"#);
    push_string(out, inputs.scope_digest);
    out.extend_from_slice(br#","sourceInventory":"#);
    out.extend_from_slice(inventory);
    out.extend_from_slice(br#","vcsDigest":""#);
    out.extend_from_slice(vcs);
    out.extend_from_slice(br#""}"#);
}

/// The `vcs-observation` record's shapes (item 4; B-S2): schema 2 `none`,
/// schema 2 `git` with its commit, and schema 3 with its members in path
/// order, borrowed.
enum VcsRecord<'r, M> {
    None,
    Git([u8; COMMIT_HEX]),
    Members(&'r [M]),
}
/// A schema-3 member as the record writes it: its path, borrowed from
/// discovery's record, and its commit's 40 digits.
trait VcsMember {
    fn path(&self) -> &str;
    fn commit(&self) -> [u8; COMMIT_HEX];
}
impl VcsMember for MemberCommit<'_> {
    fn path(&self) -> &str {
        MemberCommit::path(self)
    }
    fn commit(&self) -> [u8; COMMIT_HEX] {
        commit_digits(MemberCommit::commit(self))
    }
}
const NONE_HEAD: &[u8] =
    br#"{"commitId":null,"dirty":false,"kind":"none","schemaVersion":2,"sourceInventoryDigest":""#;
const GIT_HEAD: &[u8] = br#"{"commitId":""#;
const GIT_TAIL: &[u8] =
    br#"","dirty":true,"kind":"git","schemaVersion":2,"sourceInventoryDigest":""#;
const MEMBERS_HEAD: &[u8] = br#"{"commitId":null,"dirty":false,"kind":"none","members":["#;
const MEMBER_HEAD: &[u8] = br#"{"commitId":""#;
const MEMBER_TAIL: &[u8] = br#"","dirty":true,"kind":"git","path":"#;
const MEMBERS_TAIL: &[u8] = br#"],"schemaVersion":3,"sourceInventoryDigest":""#;
/// The record's exact canonical length, counted before anything is
/// allocated: each shape's fixed syntax, the 64-digit inventory digest and
/// its closing `"}`, and for schema 3 each member's syntax, escaped path
/// and the commas between members.
fn vcs_record_len<M: VcsMember>(record: &VcsRecord<'_, M>) -> usize {
    let digest = 64 + br#""}"#.len();
    match record {
        VcsRecord::None => NONE_HEAD.len() + digest,
        VcsRecord::Git(_) => GIT_HEAD.len() + COMMIT_HEX + GIT_TAIL.len() + digest,
        VcsRecord::Members(members) => members
            .iter()
            .enumerate()
            .fold(MEMBERS_HEAD.len(), |len, (index, member)| {
                len.saturating_add((index > 0) as usize)
                    .saturating_add(MEMBER_HEAD.len() + COMMIT_HEX + MEMBER_TAIL.len() + 1)
                    .saturating_add(string_len(member.path()))
            })
            .saturating_add(MEMBERS_TAIL.len() + digest),
    }
}
/// The record's canonical bytes (identity-v3's `canonical-record`: keys in
/// byte order), charged at its exact length `len` first, then written into
/// one buffer of that length: the record's only allocation (C1b plan r6,
/// R4-RF-1). `dirty` is a constant by law (LD-C1B-10): `true` for every Git
/// observation, enclosing or member, and `false` only for the `none` top
/// level. The digest is the inventory's (C1-T17), once.
fn charged_vcs_record<M: VcsMember>(
    record: VcsRecord<'_, M>,
    len: usize,
    inventory_digest: &[u8; 32],
    work: &mut WorkScope<'_>,
) -> Result<Vec<u8>, SealFailure> {
    work.charge::<SealError>(owned_record(len))?;
    let mut out = Vec::with_capacity(len);
    match record {
        VcsRecord::None => out.extend_from_slice(NONE_HEAD),
        VcsRecord::Git(commit) => {
            out.extend_from_slice(GIT_HEAD);
            out.extend_from_slice(&commit);
            out.extend_from_slice(GIT_TAIL);
        }
        VcsRecord::Members(members) => {
            out.extend_from_slice(MEMBERS_HEAD);
            for (index, member) in members.iter().enumerate() {
                if index > 0 {
                    out.push(b',');
                }
                out.extend_from_slice(MEMBER_HEAD);
                out.extend_from_slice(&member.commit());
                out.extend_from_slice(MEMBER_TAIL);
                push_string(&mut out, member.path());
                out.push(b'}');
            }
            out.extend_from_slice(MEMBERS_TAIL);
        }
    }
    out.extend_from_slice(&hex_digits(inventory_digest));
    out.extend_from_slice(br#""}"#);
    Ok(out)
}
/// A commit's 40 digits, from C1b-1's observation (no allocation).
fn commit_digits(commit: CommitId) -> [u8; COMMIT_HEX] {
    let mut digits = [0u8; COMMIT_HEX];
    digits.copy_from_slice(commit.as_str().as_bytes());
    digits
}
/// Seal the walked session (item 6). `report` is the walk's own report over
/// `root`, whose lending supplies the tracking observation: no caller can
/// assert it. `custody` is the invocation's judgment, as the walk's.
pub(crate) fn seal(
    session: &mut CaptureSession,
    root: &SnapshotRoot<'_>,
    custody: SnapshotCustody<'_>,
    report: &SnapshotWalkReport,
    inputs: &SealInputs<'_>,
    registry: &RegisteredSchemas,
    work: &mut WorkScope<'_>,
) -> Result<SealedSnapshot, SealFailure> {
    // (2) The read set is C1c's, and empty here (LD-C1A-6).
    // (3) Sort and uniqueness: the inventory must be strictly ascending by
    // path bytes. Rows, total bytes and the inventory's exact canonical
    // length are counted here, without allocating.
    let (mut rows, mut total, mut inventory_len) = (0u64, 0u64, 2usize);
    let mut previous: Option<&str> = None;
    let mut carrier_row = None;
    for (path, capture) in session.inventory() {
        if previous.is_some_and(|p| p.as_bytes() >= path.as_bytes()) {
            return refuse(SealError::Internal("inventory order"));
        }
        previous = Some(path);
        if path == PROJECT_CARRIER {
            carrier_row = Some(capture.sha256);
        }
        rows += 1;
        total = total.saturating_add(capture.bytes);
        inventory_len = inventory_len
            .saturating_add(row_len(path, capture.bytes))
            .saturating_add((rows > 1) as usize);
    }
    // A capture the walk never reached is a resolved input's byte outside
    // the inventory (item 1).
    if let Some(leftover) = session.leftovers().next() {
        work.charge::<SealError>(owned_record(leftover.len()))?;
        return refuse(SealError::LeftoverCapture(leftover.to_owned()));
    }
    // The project carrier's join (item 1 rule 2).
    use CarrierEntry as E;
    use CarrierTransition as T;
    let joined = match (inputs.carrier, report.carrier) {
        (ProjectCarrierObservation::Present { sha256 }, E::Regular) => match carrier_row {
            Some(row) if row == sha256 => Ok(()),
            Some(_) => Err(T::Digest),
            None => Err(T::PresentAbsent),
        },
        (ProjectCarrierObservation::Present { .. }, E::Absent) => Err(T::PresentAbsent),
        (ProjectCarrierObservation::Present { .. }, E::Directory | E::Symlink | E::Special) => {
            Err(T::Type)
        }
        (ProjectCarrierObservation::Present { .. }, E::Excluded) => Err(T::Excluded),
        (ProjectCarrierObservation::Absent, E::Absent) => Ok(()),
        (ProjectCarrierObservation::Absent, _) => Err(T::AbsentPresent),
    };
    if let Err(transition) = joined {
        return refuse(SealError::CarrierChanged(transition));
    }
    // (4) The VCS observation (item 4; unit C1b-1's reads): the lending's own
    // subject and discovery's own member record, on this ledger. Only an
    // unobserved lending is still pending.
    let observation = observe_vcs(root, custody, inputs.boundaries, work).map_err(lift_vcs)?;
    let Some(priced_len) = observation.encoded_len() else {
        return refuse(SealError::VcsPending);
    };
    // Schema 3's members in path order (B-S2 LD-4), as discovery's record holds them.
    if let VcsObservation::Members(members) = &observation
        && members
            .windows(2)
            .any(|pair| pair[0].path().as_bytes() >= pair[1].path().as_bytes())
    {
        return refuse(SealError::Internal("member order"));
    }
    let record_shape = match &observation {
        VcsObservation::Git(commit) => VcsRecord::Git(commit_digits(*commit)),
        VcsObservation::Members(members) => VcsRecord::Members(members.as_slice()),
        VcsObservation::None | VcsObservation::Unobserved => VcsRecord::None,
    };
    // The record's length, counted here, is the length C1b-1's term priced
    // (`encoded_len`, C1b plan r6 LD-C1B-6): the charge below is that one.
    let record_len = vcs_record_len(&record_shape);
    if record_len != priced_len {
        return refuse(SealError::Internal("vcs record length"));
    }
    // (5) The bounds, in item 5's order. The descriptor's exact length is
    // known before it is built.
    if rows > MAX_ROWS {
        return refuse(SealError::Bound {
            field: BoundField::Rows,
            observed: rows,
            limit: MAX_ROWS,
        });
    }
    let descriptor_bytes = descriptor_len(inputs, inventory_len);
    if descriptor_bytes > MAX_BYTES {
        return refuse(SealError::Bound {
            field: BoundField::Descriptor,
            observed: descriptor_bytes as u64,
            limit: MAX_BYTES as u64,
        });
    }
    if total > MAX_TOTAL_BYTES {
        return refuse(SealError::Bound {
            field: BoundField::TotalBytes,
            observed: total,
            limit: MAX_TOTAL_BYTES,
        });
    }
    // The canonical inventory, charged at its exact length first; then its
    // digest, the VCS record and the descriptor, each charged first.
    work.charge::<SealError>(owned_record(inventory_len))?;
    let mut inventory = Vec::with_capacity(inventory_len);
    inventory.push(b'[');
    for (index, (path, capture)) in session.inventory().enumerate() {
        if index > 0 {
            inventory.push(b',');
        }
        push_row(&mut inventory, path, &capture.sha256, capture.bytes);
    }
    inventory.push(b']');
    if inventory.len() != inventory_len {
        return refuse(SealError::Internal("inventory length"));
    }
    let inventory_digest = raw_sha256(&inventory);
    let vcs_record = charged_vcs_record(record_shape, record_len, &inventory_digest, work)?;
    if vcs_record.len() != record_len {
        return refuse(SealError::Internal("vcs record length"));
    }
    let vcs = hex_digits(&raw_sha256(&vcs_record));
    // The inventory, retained in custody under its raw SHA-256 (item 4).
    let inventory_blob = {
        let custody = session.custody_mut();
        let mut pending = custody
            .begin(inventory.len() as u64, work)
            .map_err(lift_custody)?;
        for chunk in inventory.chunks(READ_CHUNK) {
            pending.write(chunk, work).map_err(lift_custody)?;
        }
        pending.commit(work).map_err(lift_custody)?
    };
    if inventory_blob.sha256 != inventory_digest {
        return refuse(SealError::Internal("inventory blob digest"));
    }
    work.charge::<SealError>(owned_record(descriptor_bytes))?;
    let mut descriptor = Vec::with_capacity(descriptor_bytes);
    push_descriptor(&mut descriptor, inputs, &inventory, &vcs);
    if descriptor.len() != descriptor_bytes {
        return refuse(SealError::Internal("descriptor length"));
    }
    // (6) `snapshot2`: admitted against identity-v3's `$defs/snapshot`, with
    // the inventory's order checked, then hashed.
    work.charge::<SealError>(owned_record("snapshot2:".len() + 64))?;
    let candidate = IdentityCandidate::from_json(
        registry,
        IdentityDomain::Snapshot,
        &descriptor,
        SCHEMA_BUDGET,
    )
    .map_err(|error| WorkFailure::Operation(SealError::Identity(error)))?;
    Ok(SealedSnapshot {
        snapshot2: candidate.identifier().to_owned(),
        descriptor,
        source_inventory_digest: inventory_digest,
        vcs_record,
        inventory_blob,
        rows,
        total_bytes: total,
    })
}

fn lift_vcs(failure: WorkFailure<VcsRefusal>) -> SealFailure {
    match failure {
        WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
        WorkFailure::Operation(refusal) => WorkFailure::Operation(SealError::Vcs(refusal)),
    }
}

fn lift_custody(failure: WorkFailure<CustodyError>) -> SealFailure {
    match failure {
        WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
        WorkFailure::Operation(error) => WorkFailure::Operation(SealError::Custody(error)),
    }
}

#[cfg(test)]
#[path = "snapshot_seal_tests.rs"]
pub(crate) mod tests;
