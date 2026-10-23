// M3-C r8 items 7 and 8 (unit C2a-1; C2a plan r4, LD-C2A-2 to -4 and LD-C2A-9
// to -12): one verified component's unadmitted closure candidate.
//
// The order, after the trust, parse, shape and body-semantic prerequisites
// the ordinary reader owns: (1) the platform join (LD-C2A-3); (2) CR-1's
// kind (LD-C2A-2); (3) the regular-file projection, its charged merge sort
// and the duplicate pass; (4) C2PM-1's guards 1 and 2 over the authenticated
// declaration; (5) the descriptor, its length predicted and bounded before
// anything is allocated, hand-encoded at exactly that length and admitted
// against identity-v3's `$defs/closure`; (6) C2PM-1's guards 3 and 4 over the
// admitted descriptor (LD-C2A-11). The first refusal mints nothing.
//
// The descriptor is written here byte for byte as the identity crate's
// canonical encoder writes it (`canonical.rs`:286-312; a test compares them),
// following C1a3's sealing encoders (`snapshot_seal.rs`). So its exact length
// D is known, and charged, before its one buffer is reserved, and no string,
// integer or digest temporary is made (R3-RF-1).
//
// A candidate authorizes nothing (LD-C2A-12): no context, Plan, worker or
// selection accepts it. Admission is C2a-3's, after whole retention.
//
// C2a-3k's pure verification kernel (`verify_retained_tree`; C2a plan r4,
// Q6) checks a candidate's Blobs and manifest body against bytes the caller
// already holds in memory. It reads no file, holds no custody and constructs
// nothing admitted: a verified candidate is still only a candidate.
use crate::trust::AuthenticatedComponent;
use opensip_identity::{
    IdentityCandidate, IdentityDomain, JsonValue as V, MAX_BYTES, RegisteredSchemas, raw_sha256,
};
use opensip_platform::{WorkCost, WorkFailure, WorkScope};
use std::cmp::Ordering;
use std::collections::BTreeMap;

/// The schema evaluator's work bound for the one descriptor, as C1a3's
/// sealing bounds its own (`snapshot_seal.rs`; LD-C1A3-4's scoped exception).
const SCHEMA_BUDGET: usize = 64 * 1024 * 1024;
/// The four platform tokens the catalog's artifact shape admits
/// (`recovery_catalog.rs`, `artifact`; a test pins the two lists equal).
const PLATFORMS: [&str; 4] = ["macos-arm64", "macos-x86_64", "linux-arm64", "linux-x86_64"];
/// The candidate id's prefix (`core_inventory.rs`, `closure_id`).
const PREFIX: &str = "closure2:";

/// C2PM-1's four internal keys (`outcomes.rs`, `ClosureProtocolKey`).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ProtocolKey {
    DeclarationMissing,
    AnalyzerMismatch,
    DescriptorMismatch,
    Unsupported,
}
/// Where the failing declaration or descriptor came from, carried by the
/// projection and never asserted by a caller (LD-C2A-11). C2a-1 sees only an
/// authenticated release declaration and its own recomputed descriptor.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ProtocolOrigin {
    /// `request-rejected` / `REQUEST.PRECONDITION_FAILED`, public detail
    /// `native.closure-protocol-invalid`.
    AuthenticatedReleaseDeclaration,
    /// A host bug: `HOST.INVARIANT_VIOLATED`.
    HostGeneratedInternalLayer,
}
/// LD-C2A-9's refusals: C2a-1's, and `Retention` from C2a-3k's verifier.
/// Work exhaustion stays the ledger's `Budget`.
#[derive(Debug, PartialEq, Eq)]
pub enum ClosureRefusal {
    Platform,
    Tree,
    Field,
    Encoding,
    Protocol {
        key: ProtocolKey,
        origin: ProtocolOrigin,
    },
    /// A promised retained tree or body disagrees with the candidate. It
    /// keeps this cause, and is never relabelled as not installed (LD-C2A-5).
    Retention(Retention),
    /// Defence in depth: the encoder disagreed with its own prediction, or
    /// the validated manifest lacked a member its shape guarantees.
    Internal(&'static str),
}
pub type ClosureFailure = WorkFailure<ClosureRefusal>;
/// C2a-3k's typed retention failures (LD-C2A-5, LD-C2A-9).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Retention {
    /// A Blob has no retained slice at its path.
    Missing,
    /// A retained slice's length is not its Blob's `bytes` (`BLOB_LENGTH`).
    Length,
    /// A retained slice's SHA-256 is not its Blob's `sha256`, or the
    /// retained body's raw SHA-256 is not the candidate's `manifestDigest`.
    Digest,
}

/// The `{os, arch}` row the caller selected in the manifest's `platforms[]`.
#[derive(Debug, Clone, Copy)]
pub struct SelectedPlatform<'a> {
    pub os: &'a str,
    pub arch: &'a str,
}

/// The analyzer role's already-selected named subprotocol, the only way an
/// analyzer major is supported (C2PM-1 CONTRACT.md, "Role interface meanings
/// and supported resource declarations"). Selecting it is its owner's: until
/// that owner lands there is no production constructor, so no analyzer
/// obtains a new projection in production.
pub struct AnalyzerSubprotocol {
    major: u64,
}
impl AnalyzerSubprotocol {
    #[cfg(test)]
    pub(crate) fn selected_for_tests(major: u64) -> Self {
        Self { major }
    }
}

/// Synthetic protocol selection for the shared component fixtures only.
/// This is not the production analyzer protocol-selection owner.
#[cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))]
pub fn fixture_analyzer_subprotocol(major: u64) -> AnalyzerSubprotocol {
    AnalyzerSubprotocol { major }
}

/// One Blob of the projection, borrowed from the validated manifest's
/// `type=file` entry: its path, its lowercase hex SHA-256 and its length.
#[derive(Debug, PartialEq, Eq)]
pub struct BlobRef<'a> {
    path: &'a str,
    sha256: &'a str,
    bytes: u64,
}
impl<'a> BlobRef<'a> {
    pub fn path(&self) -> &'a str {
        self.path
    }
    pub fn sha256(&self) -> &'a str {
        self.sha256
    }
    pub fn bytes(&self) -> u64 {
        self.bytes
    }
}

/// C2a-1's output: unadmitted (LD-C2A-12). It has no constructor outside
/// this module and is not Clone, Default or serializable.
pub struct ClosureCandidate<'a> {
    closure: String,
    descriptor: Vec<u8>,
    manifest_digest: [u8; 32],
    blobs: Vec<BlobRef<'a>>,
    order: Vec<u32>,
}
impl<'a> ClosureCandidate<'a> {
    /// The candidate id, `closure2:` + H("closure", D).
    pub fn closure(&self) -> &str {
        &self.closure
    }
    /// D, the canonical descriptor bytes.
    pub fn descriptor(&self) -> &[u8] {
        &self.descriptor
    }
    /// The raw SHA-256 of the authenticated body (`manifestDigest`).
    pub fn manifest_digest(&self) -> [u8; 32] {
        self.manifest_digest
    }
    /// The bounded projection count, without walking or copying its Blobs.
    /// Like every candidate observation, this grants no admitted authority.
    pub fn blob_count(&self) -> usize {
        self.order.len()
    }
    /// The Blobs in the descriptor's order, path bytes ascending.
    pub fn blobs(&self) -> impl Iterator<Item = &BlobRef<'a>> {
        self.order.iter().map(|&at| &self.blobs[at as usize])
    }
}

// The published prices (LD-C2A-10). Each is charged before the work or
// allocation it prices; nothing else is allocated.

/// One visit of each of a platform row's `entries`. The projection visits
/// the row twice, to count its regular files and then to project them.
pub(crate) const fn visit_cost(entries: usize) -> WorkCost {
    WorkCost {
        objects: 0,
        edges: entries,
        bytes: 0,
    }
}
/// The projection's one `Vec<BlobRef<'_>>`, reserved for exactly `files`.
pub(crate) const fn projection_cost(files: usize) -> WorkCost {
    WorkCost {
        objects: 1,
        edges: 0,
        bytes: files.saturating_mul(size_of::<BlobRef<'_>>()),
    }
}
/// The merge sort's two `u32` index buffers.
pub(crate) const fn sort_buffers_cost(n: usize) -> WorkCost {
    WorkCost {
        objects: 2,
        edges: 0,
        bytes: n.saturating_mul(2 * size_of::<u32>()),
    }
}
/// One comparison of the merge sort, charged immediately before it.
pub(crate) const COMPARISON_COST: WorkCost = WorkCost {
    objects: 0,
    edges: 1,
    bytes: 0,
};
/// The sort's published reference price: at most n·⌈log₂ n⌉ comparisons.
pub(crate) const fn sort_reference_comparisons(n: usize) -> usize {
    if n < 2 {
        0
    } else {
        n.saturating_mul((usize::BITS - (n - 1).leading_zeros()) as usize)
    }
}
/// The adjacent-duplicate pass over n sorted Blobs.
pub(crate) const fn duplicate_pass_cost(n: usize) -> WorkCost {
    WorkCost {
        objects: 0,
        edges: n.saturating_sub(1),
        bytes: 0,
    }
}
/// One SHA-256 over `len` bytes: a conservative block bound.
pub(crate) const fn digest_cost(len: usize) -> WorkCost {
    WorkCost {
        objects: 0,
        edges: len.div_ceil(64).saturating_add(1),
        bytes: 0,
    }
}
/// The descriptor's one buffer, `Vec::with_capacity(D)`.
pub(crate) const fn encoding_cost(d: usize) -> WorkCost {
    WorkCost {
        objects: 1,
        edges: 0,
        bytes: d,
    }
}
/// The candidate id, an owned record of `"closure2:".len() + 64` bytes.
pub(crate) const ID_COST: WorkCost = WorkCost {
    objects: 1,
    edges: 0,
    bytes: PREFIX.len() + 64,
};

/// The descriptor's fields other than its tree (LD-C2A-4).
struct Fields<'a> {
    kind: &'static str,
    manifest_digest: [u8; 64],
    platform: &'static str,
    protocol_major: u64,
    semantic_version: &'a str,
}

/// One verified component's candidate for `platform` (LD-C2A-3, -4, -11).
/// `analyzer` is the analyzer role's selected subprotocol, if any. The work
/// is the caller's borrowed scope (Q5): C2a-1 selects no profile.
pub fn component_candidate<'a>(
    component: &AuthenticatedComponent<'a>,
    platform: SelectedPlatform<'_>,
    analyzer: Option<&AnalyzerSubprotocol>,
    registry: &RegisteredSchemas,
    work: &mut WorkScope<'_>,
) -> Result<ClosureCandidate<'a>, ClosureFailure> {
    let manifest = component.manifest();
    let (row, token) = join_platform(manifest, component.release(), platform)?;
    let kind = component.closure_kind();
    let entries = items(member(member(row, "tree")?, "entries")?)?;
    let blobs = project(entries, work)?;
    let order = ordered(&blobs, work)?;
    let role = text(member(manifest, "role")?)?;
    let declaration = match object(manifest)?.get("closureProtocolMajor") {
        None => None,
        Some(major) => Some(integer(major)?),
    };
    let provider_protocol = integer(member(
        member(manifest, "compatibility")?,
        "providerProtocol",
    )?)?;
    let major = declared_major(role, declaration, provider_protocol)?;
    work.charge(digest_cost(component.body().len()))?;
    let manifest_digest = raw_sha256(component.body());
    let fields = Fields {
        kind,
        manifest_digest: hex_digits(&manifest_digest),
        platform: token,
        protocol_major: major,
        semantic_version: text(member(manifest, "version")?)?,
    };
    let (descriptor, candidate) = admit_descriptor(&fields, &blobs, &order, registry, work)?;
    let admitted = match object(candidate.descriptor())?.get("protocolMajor") {
        None => None,
        Some(major) => Some(integer(major)?),
    };
    admitted_major(role, major, admitted, analyzer)?;
    work.charge(ID_COST)?;
    let closure = candidate.identifier().to_owned();
    Ok(ClosureCandidate {
        closure,
        descriptor,
        manifest_digest,
        blobs,
        order,
    })
}

/// LD-C2A-3's join: the selected `{os, arch}` row, its token among the
/// catalog's four, and an artifact of that token in the same release row.
fn join_platform<'m>(
    manifest: &'m V,
    release: &V,
    platform: SelectedPlatform<'_>,
) -> Result<(&'m V, &'static str), ClosureFailure> {
    let mut row = None;
    for candidate in items(member(manifest, "platforms")?)? {
        if text(member(candidate, "os")?)? == platform.os
            && text(member(candidate, "arch")?)? == platform.arch
        {
            row = Some(candidate);
        }
    }
    let row = row.ok_or(WorkFailure::Operation(ClosureRefusal::Platform))?;
    let token = PLATFORMS
        .into_iter()
        .find(|token| {
            token.len() == platform.os.len() + 1 + platform.arch.len()
                && token.starts_with(platform.os)
                && token.as_bytes()[platform.os.len()] == b'-'
                && token.ends_with(platform.arch)
        })
        .ok_or(WorkFailure::Operation(ClosureRefusal::Platform))?;
    let mut joined = false;
    for artifact in items(member(release, "artifacts")?)? {
        joined |= text(member(artifact, "platform")?)? == token;
    }
    if !joined {
        return Err(WorkFailure::Operation(ClosureRefusal::Platform));
    }
    Ok((row, token))
}

/// The regular-file projection (SL:41-48): each `type=file` entry becomes a
/// Blob with the same path; `dir` and `symlink` rows are not members.
fn project<'m>(
    entries: &'m [V],
    work: &mut WorkScope<'_>,
) -> Result<Vec<BlobRef<'m>>, ClosureFailure> {
    work.charge(visit_cost(entries.len()))?;
    let mut files = 0;
    for entry in entries {
        if text(member(entry, "type")?)? == "file" {
            files += 1;
        }
    }
    work.charge(projection_cost(files))?;
    let mut blobs = Vec::with_capacity(files);
    work.charge(visit_cost(entries.len()))?;
    for entry in entries {
        if text(member(entry, "type")?)? != "file" {
            continue;
        }
        let bytes = u64::try_from(integer(member(entry, "length")?)?)
            .map_err(|_| WorkFailure::Operation(ClosureRefusal::Field))?;
        blobs.push(BlobRef {
            path: text(member(entry, "path")?)?,
            sha256: text(member(entry, "sha256")?)?,
            bytes,
        });
    }
    Ok(blobs)
}

/// The Blob order by path bytes, which `x-opensip-order` requires and the
/// body reader does not guarantee; then the duplicate pass (`Tree`).
fn ordered(blobs: &[BlobRef<'_>], work: &mut WorkScope<'_>) -> Result<Vec<u32>, ClosureFailure> {
    let n = u32::try_from(blobs.len()).map_err(|_| WorkFailure::Operation(ClosureRefusal::Tree))?;
    let order = merge_sort(n, work, |a, b| {
        blobs[a as usize].path.as_bytes() < blobs[b as usize].path.as_bytes()
    })?;
    work.charge(duplicate_pass_cost(order.len()))?;
    for pair in order.windows(2) {
        if blobs[pair[0] as usize].path == blobs[pair[1] as usize].path {
            return Err(WorkFailure::Operation(ClosureRefusal::Tree));
        }
    }
    Ok(order)
}

/// A stable bottom-up merge sort of the indices `0..n` by `less` (R3-RF-2).
/// One edge is charged immediately before each comparison, and `Budget`
/// propagates out before an unfunded comparison is made. At most
/// n·⌈log₂ n⌉ comparisons are made.
pub(crate) fn merge_sort<E>(
    n: u32,
    work: &mut WorkScope<'_>,
    mut less: impl FnMut(u32, u32) -> bool,
) -> Result<Vec<u32>, WorkFailure<E>> {
    let len = n as usize;
    work.charge(sort_buffers_cost(len))?;
    let mut from = Vec::with_capacity(len);
    from.extend(0..n);
    let mut to = Vec::with_capacity(len);
    to.extend(0..n);
    let mut width = 1;
    while width < len {
        let mut low = 0;
        while low < len {
            let mid = (low + width).min(len);
            let high = (low + 2 * width).min(len);
            let (mut i, mut j, mut k) = (low, mid, low);
            while i < mid && j < high {
                work.charge(COMPARISON_COST)?;
                if less(from[j], from[i]) {
                    to[k] = from[j];
                    j += 1;
                } else {
                    to[k] = from[i];
                    i += 1;
                }
                k += 1;
            }
            to[k..k + mid - i].copy_from_slice(&from[i..mid]);
            k += mid - i;
            to[k..high].copy_from_slice(&from[j..high]);
            low = high;
        }
        core::mem::swap(&mut from, &mut to);
        width *= 2;
    }
    Ok(from)
}

/// C2PM-1's guards 1 and 2 over the authenticated declaration (LD-C2A-11):
/// the exact integer copied into `protocolMajor`, never inferred from
/// `compatibility.providerProtocol` when absent.
fn declared_major(
    role: &str,
    declaration: Option<i128>,
    provider_protocol: i128,
) -> Result<u64, ClosureFailure> {
    let Some(declaration) = declaration else {
        return Err(protocol(
            ProtocolKey::DeclarationMissing,
            ProtocolOrigin::AuthenticatedReleaseDeclaration,
        ));
    };
    if role == "analyzer" && declaration != provider_protocol {
        return Err(protocol(
            ProtocolKey::AnalyzerMismatch,
            ProtocolOrigin::AuthenticatedReleaseDeclaration,
        ));
    }
    u64::try_from(declaration)
        .map_err(|_| WorkFailure::Operation(ClosureRefusal::Internal("declaration range")))
}

/// C2PM-1's guards 3 and 4 over the admitted descriptor (LD-C2A-11). The
/// descriptor is the host's own, so a mismatch is a host bug; support is
/// the role table, with no numeric union and no cross-role equivalence.
fn admitted_major(
    role: &str,
    declared: u64,
    descriptor: Option<i128>,
    analyzer: Option<&AnalyzerSubprotocol>,
) -> Result<(), ClosureFailure> {
    if descriptor != Some(declared as i128) {
        return Err(protocol(
            ProtocolKey::DescriptorMismatch,
            ProtocolOrigin::HostGeneratedInternalLayer,
        ));
    }
    let supported = match role {
        "toolchain" | "stdlib" | "rust-dev-llvm" | "grammar" => declared == 1,
        "analyzer" => analyzer.is_some_and(|selected| selected.major == declared),
        _ => false,
    };
    if !supported {
        return Err(protocol(
            ProtocolKey::Unsupported,
            ProtocolOrigin::AuthenticatedReleaseDeclaration,
        ));
    }
    Ok(())
}
fn protocol(key: ProtocolKey, origin: ProtocolOrigin) -> ClosureFailure {
    WorkFailure::Operation(ClosureRefusal::Protocol { key, origin })
}

/// C2a-3k (C2a plan r4, Q6; LD-C2A-5, -10): `candidate`'s Blobs against
/// `retained`, the caller's in-memory slices by path, and `body` against the
/// candidate's `manifestDigest`. Each Blob, in path order, must have a slice,
/// of exactly its `bytes` (`BLOB_LENGTH`) and of its `sha256`; then the
/// body's raw SHA-256 must be `manifestDigest`. The first failure returns.
///
/// Presence is one ordered walk of `retained` beside the Blobs, both in path
/// byte order. A retained slice that is no Blob's is not a member and is
/// passed over. Every comparison is charged `COMPARISON_COST` immediately
/// before it is made, and every SHA-256 `digest_cost` immediately before it,
/// in the caller's borrowed scope. No slice is copied and nothing is
/// allocated.
pub fn verify_retained_tree(
    candidate: &ClosureCandidate<'_>,
    retained: &BTreeMap<&str, &[u8]>,
    body: &[u8],
    work: &mut WorkScope<'_>,
) -> Result<(), ClosureFailure> {
    let mut slices = retained.iter();
    let mut next = slices.next();
    for blob in candidate.blobs() {
        let slice = loop {
            let Some((&path, &slice)) = next else {
                return Err(retention(Retention::Missing));
            };
            work.charge(COMPARISON_COST)?;
            match path.as_bytes().cmp(blob.path().as_bytes()) {
                Ordering::Less => next = slices.next(),
                Ordering::Equal => {
                    next = slices.next();
                    break slice;
                }
                Ordering::Greater => return Err(retention(Retention::Missing)),
            }
        };
        work.charge(COMPARISON_COST)?;
        if u64::try_from(slice.len()) != Ok(blob.bytes()) {
            return Err(retention(Retention::Length));
        }
        work.charge(digest_cost(slice.len()))?;
        let digest = raw_sha256(slice);
        work.charge(COMPARISON_COST)?;
        if blob.sha256().as_bytes() != hex_digits(&digest) {
            return Err(retention(Retention::Digest));
        }
    }
    work.charge(digest_cost(body.len()))?;
    let digest = raw_sha256(body);
    work.charge(COMPARISON_COST)?;
    if digest != candidate.manifest_digest {
        return Err(retention(Retention::Digest));
    }
    Ok(())
}
fn retention(failure: Retention) -> ClosureFailure {
    WorkFailure::Operation(ClosureRefusal::Retention(failure))
}

/// D: predicted, bounded (`Encoding` before anything is allocated), charged,
/// hand-encoded at exactly its length and admitted against `$defs/closure`.
fn admit_descriptor<'r>(
    fields: &Fields<'_>,
    blobs: &[BlobRef<'_>],
    order: &[u32],
    registry: &'r RegisteredSchemas,
    work: &mut WorkScope<'_>,
) -> Result<(Vec<u8>, IdentityCandidate<'r>), ClosureFailure> {
    let length = descriptor_len(fields, blobs);
    if length > MAX_BYTES {
        return Err(WorkFailure::Operation(ClosureRefusal::Encoding));
    }
    work.charge(encoding_cost(length))?;
    let mut descriptor = Vec::with_capacity(length);
    push_descriptor(&mut descriptor, fields, blobs, order);
    if descriptor.len() != length || descriptor.capacity() != length {
        return Err(WorkFailure::Operation(ClosureRefusal::Internal(
            "descriptor length",
        )));
    }
    let candidate = IdentityCandidate::from_json(
        registry,
        IdentityDomain::Closure,
        &descriptor,
        SCHEMA_BUDGET,
    )
    .map_err(|_| WorkFailure::Operation(ClosureRefusal::Field))?;
    Ok((descriptor, candidate))
}

/// e(x): one string's encoded payload, its canonical encoding without the
/// two quotes (`canonical.rs`:286-312).
fn payload_len(text: &str) -> usize {
    let mut len = 0usize;
    for c in text.chars() {
        len = len.saturating_add(match c {
            '"' | '\\' | '\u{8}' | '\u{c}' | '\n' | '\r' | '\t' => 2,
            '\0'..='\u{1f}' => 6,
            c => c.len_utf8(),
        });
    }
    len
}
/// d(n): an integer's decimal digits.
fn decimal_len(mut n: u64) -> usize {
    let mut len = 1;
    while n >= 10 {
        n /= 10;
        len += 1;
    }
    len
}
/// LD-C2A-3's formula: 175 + e(kind) + e(platform) + d(protocolMajor) +
/// e(semanticVersion) + Σ(96 + d(Nᵢ) + e(Pᵢ)) + max(n − 1, 0).
fn descriptor_len(fields: &Fields<'_>, blobs: &[BlobRef<'_>]) -> usize {
    let mut len = 175usize
        .saturating_add(payload_len(fields.kind))
        .saturating_add(payload_len(fields.platform))
        .saturating_add(decimal_len(fields.protocol_major))
        .saturating_add(payload_len(fields.semantic_version))
        .saturating_add(blobs.len().saturating_sub(1));
    for blob in blobs {
        len = len
            .saturating_add(96)
            .saturating_add(decimal_len(blob.bytes))
            .saturating_add(payload_len(blob.path));
    }
    len
}
fn push_string(out: &mut Vec<u8>, text: &str) {
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
/// An integer's decimal digits, from a 39-byte stack buffer.
fn push_decimal(out: &mut Vec<u8>, n: u64) {
    let mut digits = [0u8; 39];
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
/// Lowercase hex digits, written in place.
const HEX: &[u8; 16] = b"0123456789abcdef";
fn hex_digits(digest: &[u8; 32]) -> [u8; 64] {
    let mut digits = [0u8; 64];
    for (at, byte) in digest.iter().enumerate() {
        digits[2 * at] = HEX[(byte >> 4) as usize];
        digits[2 * at + 1] = HEX[(byte & 0x0f) as usize];
    }
    digits
}
/// `{"kind":..,"manifestDigest":..,"platform":..,"protocolMajor":..,
/// "schemaVersion":2,"semanticVersion":..,"tree":[..]}`, keys in byte order;
/// each Blob `{"bytes":N,"path":P,"sha256":H}`.
fn push_descriptor(out: &mut Vec<u8>, fields: &Fields<'_>, blobs: &[BlobRef<'_>], order: &[u32]) {
    out.extend_from_slice(br#"{"kind":"#);
    push_string(out, fields.kind);
    out.extend_from_slice(br#","manifestDigest":""#);
    out.extend_from_slice(&fields.manifest_digest);
    out.extend_from_slice(br#"","platform":"#);
    push_string(out, fields.platform);
    out.extend_from_slice(br#","protocolMajor":"#);
    push_decimal(out, fields.protocol_major);
    out.extend_from_slice(br#","schemaVersion":2,"semanticVersion":"#);
    push_string(out, fields.semantic_version);
    out.extend_from_slice(br#","tree":["#);
    for (index, &at) in order.iter().enumerate() {
        let blob = &blobs[at as usize];
        if index > 0 {
            out.push(b',');
        }
        out.extend_from_slice(br#"{"bytes":"#);
        push_decimal(out, blob.bytes);
        out.extend_from_slice(br#","path":"#);
        push_string(out, blob.path);
        out.extend_from_slice(br#","sha256":""#);
        out.extend_from_slice(blob.sha256.as_bytes());
        out.extend_from_slice(br#""}"#);
    }
    out.extend_from_slice(b"]}");
}

// The validated manifest's and release row's shapes are the reader's; a
// missing member is a defect here, never a new refusal class.
fn object(v: &V) -> Result<&BTreeMap<String, V>, ClosureFailure> {
    match v {
        V::Object(o) => Ok(o),
        _ => Err(WorkFailure::Operation(ClosureRefusal::Internal("shape"))),
    }
}
fn member<'v>(v: &'v V, key: &str) -> Result<&'v V, ClosureFailure> {
    object(v)?
        .get(key)
        .ok_or(WorkFailure::Operation(ClosureRefusal::Internal("shape")))
}
fn items(v: &V) -> Result<&[V], ClosureFailure> {
    match v {
        V::Array(a) => Ok(a),
        _ => Err(WorkFailure::Operation(ClosureRefusal::Internal("shape"))),
    }
}
fn text(v: &V) -> Result<&str, ClosureFailure> {
    match v {
        V::String(s) => Ok(s),
        _ => Err(WorkFailure::Operation(ClosureRefusal::Internal("shape"))),
    }
}
fn integer(v: &V) -> Result<i128, ClosureFailure> {
    match v {
        V::Integer(n) => Ok(n.get()),
        _ => Err(WorkFailure::Operation(ClosureRefusal::Internal("shape"))),
    }
}

#[cfg(test)]
#[path = "component_closure_tests.rs"]
pub(crate) mod tests;
