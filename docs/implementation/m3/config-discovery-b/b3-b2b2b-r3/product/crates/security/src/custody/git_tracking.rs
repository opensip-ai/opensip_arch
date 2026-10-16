// Law X2 r7 item 6a and item 1's Git premise scope (unit X2b-2): the
// tracking observation. One bounded, charged, custody-checked observation
// over the admitted project root's retained chain that decides whether the
// project marker `.opensip/project-id.v1` is tracked by any enclosing Git
// repository. M2 admits one closed, conventional Git layout and refuses
// every other layout as `vcs-unsupported`; nothing is modelled.
//
// Pure parts: the closed configuration parse and its refusals, the process
// environment refusal, the exact index decoder (versions 2, 3 and 4, with
// the trailing SHA-1 checked) and the marker-path match. Native parts: the
// upward walk for VCS markers, each enclosing repository's layout evidence,
// and the fixed global and system configuration sources. Every native step
// is charged before it runs, and the whole evidence set is re-observed and
// compared for the held-fence recheck.
//
// The system configuration sources are refusal-only evidence (r7): read by
// their fixed paths, following links, with no custody judged; they can only
// refuse. Library only; nothing is created or written.
use super::project_chain::{
    ChainIdentity, CustodyOrder, Failure as ChainFailure, ProjectChain, ProjectChainPolicy, ProjectChainRefusal,
    ProjectObject, check_project_object_ordered,
};
use crate::trust::AclOmissionPremise;
use opensip_platform::{CapturedAclState, DescriptorAclCaptureError};
use std::collections::BTreeSet;
use opensip_platform::{
    DescriptorFilesystem, DescriptorMetadata, RetainedDirectory, WorkCost, WorkFailure, WorkReadFailure, WorkScope,
};
use std::ffi::{OsStr, OsString};
use std::fs::File;
use std::io;
use std::os::unix::ffi::OsStrExt;
use std::path::Path;

/// Item 6a: a Git configuration source is capped at 64 KiB.
pub(crate) const CONFIG_CAP: usize = 64 * 1024;
/// Item 9: a Git index is held to the 4 MiB per-record ceiling.
pub(crate) const INDEX_CAP: usize = 4 * 1024 * 1024;
/// The fixed system configuration sources (item 6a).
pub(crate) const SYSTEM_SOURCES: [&str; 5] = [
    "/etc/gitconfig",
    "/Library/Developer/CommandLineTools/usr/share/git-core/gitconfig",
    "/Applications/Xcode.app/Contents/Developer/usr/share/git-core/gitconfig",
    "/opt/homebrew/etc/gitconfig",
    "/usr/local/etc/gitconfig",
];
/// The VCS markers looked up at every directory of the chain.
const VCS_MARKERS: [&str; 4] = [".git", ".hg", ".svn", ".jj"];
/// The marker's path below a project root.
const MARKER_SUFFIX: &[u8] = b".opensip/project-id.v1";
/// A gitlink (submodule) entry's mode.
const GITLINK: u32 = 0o160000;

// ------------------------------------------------------------- refusals

/// Why the tracking observation refused. Item 8: a tracked marker is
/// `marker-tracked`; every unsupported, unreadable, oversized or malformed
/// VCS, config or index observation is `vcs-unsupported`; native I/O is the
/// host I/O row.
#[derive(Debug)]
pub(crate) enum TrackingRefusal {
    MarkerTracked,
    VcsUnsupported(&'static str),
    Io(io::Error),
}
/// Item 8's row.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum TrackingRow {
    /// `PROJECT.ROOT_CUSTODY_REFUSED`, with this subject.
    RootCustody(&'static str),
    /// The host I/O row.
    HostIo,
}
impl TrackingRefusal {
    pub(crate) fn row(&self) -> TrackingRow {
        match self {
            Self::MarkerTracked => TrackingRow::RootCustody("marker-tracked"),
            Self::VcsUnsupported(_) => TrackingRow::RootCustody("vcs-unsupported"),
            Self::Io(_) => TrackingRow::HostIo,
        }
    }
}
pub(crate) type Failure = WorkFailure<TrackingRefusal>;
fn unsupported<T>(reason: &'static str) -> Result<T, Failure> {
    Err(WorkFailure::Operation(TrackingRefusal::VcsUnsupported(reason)))
}
fn io_failure(failure: WorkFailure<io::Error>) -> Failure {
    match failure {
        WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
        WorkFailure::Operation(error) => WorkFailure::Operation(TrackingRefusal::Io(error)),
    }
}
/// A custody judgment that did not pass: I/O is host I/O; anything else is
/// inadmissible VCS evidence.
fn chain_failure(failure: ChainFailure, reason: &'static str) -> Failure {
    match failure {
        WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
        WorkFailure::Operation(refusal) => match refusal {
            ProjectChainRefusal::Io(error) => WorkFailure::Operation(TrackingRefusal::Io(error)),
            ProjectChainRefusal::RootCapture(opensip_platform::DescriptorAclCaptureError::Io(
                error,
            )) => WorkFailure::Operation(TrackingRefusal::Io(error)),
            _ => WorkFailure::Operation(TrackingRefusal::VcsUnsupported(reason)),
        },
    }
}

// ------------------------------------------------- the closed config parse

/// One `key = value` line of a Git configuration source. Section and key
/// are ASCII-lowercased (Git compares them case-insensitively); the
/// subsection is kept exactly. A key with no `=` is a boolean true
/// (`value` is `None`).
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct ConfigEntry {
    pub(crate) section: String,
    pub(crate) subsection: Option<Vec<u8>>,
    pub(crate) key: String,
    pub(crate) value: Option<Vec<u8>>,
}

fn is_space(b: u8) -> bool {
    b == b' ' || b == b'\t'
}
/// Item 6a's closed subset of Git's configuration syntax: `[section]` and
/// `[section "subsection"]` headers, `key = value` and bare `key` lines,
/// `#` and `;` comments, and values with `"` quoting and the escapes `\\`,
/// `\"`, `\n`, `\t` and `\b`. A line continuation, a carriage return, a
/// legacy `[section.sub]` header, a key before any section, or any other
/// byte the subset does not name refuses.
pub(crate) fn parse_config(raw: &[u8]) -> Result<Vec<ConfigEntry>, &'static str> {
    if raw.len() > CONFIG_CAP {
        return Err("config-oversized");
    }
    let mut entries = Vec::new();
    let mut section: Option<(String, Option<Vec<u8>>)> = None;
    for line in raw.split(|b| *b == b'\n') {
        if line.contains(&b'\r') || line.contains(&0) {
            return Err("config-syntax");
        }
        let start = line.iter().position(|b| !is_space(*b)).unwrap_or(line.len());
        let line = &line[start..];
        match line.first() {
            None | Some(b'#') | Some(b';') => continue,
            Some(b'[') => section = Some(parse_header(line)?),
            Some(_) => {
                let (current, sub) = section.as_ref().ok_or("config-syntax")?;
                let (key, value) = parse_key_value(line)?;
                entries.push(ConfigEntry {
                    section: current.clone(),
                    subsection: sub.clone(),
                    key,
                    value,
                });
            }
        }
    }
    Ok(entries)
}
fn parse_header(line: &[u8]) -> Result<(String, Option<Vec<u8>>), &'static str> {
    let mut i = 1;
    let start = i;
    while i < line.len() && (line[i].is_ascii_alphanumeric() || line[i] == b'-') {
        i += 1;
    }
    if i == start {
        return Err("config-syntax");
    }
    let name = String::from_utf8(line[start..i].to_ascii_lowercase()).map_err(|_| "config-syntax")?;
    let mut subsection = None;
    if line.get(i) == Some(&b' ') {
        while line.get(i).is_some_and(|b| is_space(*b)) {
            i += 1;
        }
        if line.get(i) != Some(&b'"') {
            return Err("config-syntax");
        }
        i += 1;
        let mut sub = Vec::new();
        loop {
            match line.get(i) {
                None => return Err("config-syntax"),
                Some(b'"') => {
                    i += 1;
                    break;
                }
                Some(b'\\') => {
                    match line.get(i + 1) {
                        Some(b'"') => sub.push(b'"'),
                        Some(b'\\') => sub.push(b'\\'),
                        _ => return Err("config-syntax"),
                    }
                    i += 2;
                }
                Some(b) => {
                    sub.push(*b);
                    i += 1;
                }
            }
        }
        subsection = Some(sub);
    }
    if line.get(i) != Some(&b']') {
        return Err("config-syntax");
    }
    i += 1;
    while line.get(i).is_some_and(|b| is_space(*b)) {
        i += 1;
    }
    match line.get(i) {
        None | Some(b'#') | Some(b';') => Ok((name, subsection)),
        Some(_) => Err("config-syntax"),
    }
}
fn parse_key_value(line: &[u8]) -> Result<(String, Option<Vec<u8>>), &'static str> {
    if !line[0].is_ascii_alphabetic() {
        return Err("config-syntax");
    }
    let mut i = 0;
    while i < line.len() && (line[i].is_ascii_alphanumeric() || line[i] == b'-') {
        i += 1;
    }
    let key = String::from_utf8(line[..i].to_ascii_lowercase()).map_err(|_| "config-syntax")?;
    while line.get(i).is_some_and(|b| is_space(*b)) {
        i += 1;
    }
    match line.get(i) {
        None | Some(b'#') | Some(b';') => return Ok((key, None)),
        Some(b'=') => i += 1,
        Some(_) => return Err("config-syntax"),
    }
    let mut value = Vec::new();
    // Trailing whitespace outside quotes is dropped; `pending` holds it
    // until a later non-space byte shows it was interior.
    let mut pending = Vec::new();
    let mut quoted = false;
    let mut leading = true;
    while i < line.len() {
        let b = line[i];
        match b {
            b'"' => {
                value.append(&mut pending);
                quoted = !quoted;
                leading = false;
                i += 1;
            }
            b'\\' => {
                let escaped = match line.get(i + 1) {
                    Some(b'\\') => b'\\',
                    Some(b'"') => b'"',
                    Some(b'n') => b'\n',
                    Some(b't') => b'\t',
                    Some(b'b') => 0x08,
                    // A continuation (backslash at end of line) or any
                    // other escape is outside the subset.
                    _ => return Err("config-syntax"),
                };
                value.append(&mut pending);
                value.push(escaped);
                leading = false;
                i += 2;
            }
            b'#' | b';' if !quoted => break,
            b if is_space(b) && !quoted => {
                if !leading {
                    pending.push(b);
                }
                i += 1;
            }
            b => {
                value.append(&mut pending);
                value.push(b);
                leading = false;
                i += 1;
            }
        }
    }
    if quoted {
        return Err("config-syntax");
    }
    Ok((key, Some(value)))
}
/// Git's false spellings (case-insensitive): `false`, `no`, `off`, `0`, and
/// the empty value. A bare key (no `=`) is true.
fn is_false(value: &Option<Vec<u8>>) -> bool {
    match value {
        None => false,
        Some(v) => {
            v.is_empty()
                || [&b"false"[..], b"no", b"off", b"0"]
                    .iter()
                    .any(|f| v.eq_ignore_ascii_case(f))
        }
    }
}
/// Item 6a's refusals over one source's entries. The union of the sources
/// is checked by checking each source, since every refusal is per entry.
pub(crate) fn check_config(entries: &[ConfigEntry]) -> Result<(), &'static str> {
    for e in entries {
        if e.section == "include" || e.section == "includeif" {
            return Err("config-include");
        }
        if e.section == "extensions" {
            return Err("config-extensions");
        }
        if e.section != "core" || e.subsection.is_some() {
            continue;
        }
        match e.key.as_str() {
            "worktree" => return Err("config-worktree"),
            "bare" if !is_false(&e.value) => return Err("config-bare"),
            "repositoryformatversion" if e.value.as_deref() != Some(b"0") => {
                return Err("config-format-version");
            }
            "precomposeunicode" if is_false(&e.value) => return Err("config-precompose"),
            _ => {}
        }
    }
    Ok(())
}

// -------------------------------------------------------- the environment

/// Item 6a: the process environment is read only to refuse. Any variable
/// whose name starts with `GIT_`, or `XDG_CONFIG_HOME`, or a `HOME` that is
/// not H's exact spelling, refuses.
pub(crate) fn check_environment(
    variables: &[(OsString, OsString)],
    home: &Path,
) -> Result<(), &'static str> {
    for (name, value) in variables {
        let name = name.as_bytes();
        if name.starts_with(b"GIT_") {
            return Err("environment-git");
        }
        if name == b"XDG_CONFIG_HOME" {
            return Err("environment-xdg");
        }
        if name == b"HOME" && value.as_bytes() != home.as_os_str().as_bytes() {
            return Err("environment-home");
        }
    }
    Ok(())
}
/// The process environment, for the production entry. Only refusals are
/// derived from it.
#[allow(clippy::disallowed_methods, reason = "M3-B r5 item 9: the one production read, X2's refusal-only Git check")]
pub(crate) fn process_environment() -> Vec<(OsString, OsString)> {
    std::env::vars_os().collect()
}

// ------------------------------------------------------------------ SHA-1

/// SHA-1 (FIPS 180-4), for the index's trailing checksum only. It is an
/// integrity check of a file the index's own writer computed, never an
/// authentication.
pub(crate) fn sha1(data: &[u8]) -> [u8; 20] {
    let mut h: [u32; 5] = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0];
    let bit_len = (data.len() as u64).wrapping_mul(8);
    let mut message = data.to_vec();
    message.push(0x80);
    while message.len() % 64 != 56 {
        message.push(0);
    }
    message.extend_from_slice(&bit_len.to_be_bytes());
    for block in message.chunks_exact(64) {
        let mut w = [0u32; 80];
        for (i, word) in block.chunks_exact(4).enumerate() {
            w[i] = u32::from_be_bytes([word[0], word[1], word[2], word[3]]);
        }
        for i in 16..80 {
            w[i] = (w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16]).rotate_left(1);
        }
        let [mut a, mut b, mut c, mut d, mut e] = h;
        for (i, wi) in w.iter().enumerate() {
            let (f, k) = match i {
                0..=19 => ((b & c) | (!b & d), 0x5A827999),
                20..=39 => (b ^ c ^ d, 0x6ED9EBA1),
                40..=59 => ((b & c) | (b & d) | (c & d), 0x8F1BBCDC),
                _ => (b ^ c ^ d, 0xCA62C1D6),
            };
            let t = a
                .rotate_left(5)
                .wrapping_add(f)
                .wrapping_add(e)
                .wrapping_add(k)
                .wrapping_add(*wi);
            e = d;
            d = c;
            c = b.rotate_left(30);
            b = a;
            a = t;
        }
        for (slot, v) in h.iter_mut().zip([a, b, c, d, e]) {
            *slot = slot.wrapping_add(v);
        }
    }
    let mut out = [0u8; 20];
    for (chunk, v) in out.chunks_exact_mut(4).zip(h) {
        chunk.copy_from_slice(&v.to_be_bytes());
    }
    out
}

// ------------------------------------------------------- the index decoder

/// One decoded index entry: its full path and mode.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct IndexEntry {
    pub(crate) path: Vec<u8>,
    pub(crate) mode: u32,
}
/// The fixed part of an entry: ten 32-bit stat fields, the 20-byte object
/// name and the 16-bit flags.
const FIXED: usize = 62;
fn u32_at(raw: &[u8], at: usize) -> Option<u32> {
    raw.get(at..at + 4).map(|b| u32::from_be_bytes([b[0], b[1], b[2], b[3]]))
}
fn u16_at(raw: &[u8], at: usize) -> Option<u16> {
    raw.get(at..at + 2).map(|b| u16::from_be_bytes([b[0], b[1]]))
}
/// Decode a complete index exactly as Git's index-format documentation
/// specifies (item 6a): the trailing SHA-1 over every preceding byte,
/// `DIRC`, version 2, 3 or 4, exactly the counted entries, then extensions
/// to the checksum with every byte consumed. Version 3 and later carry a
/// 16-bit extended-flags field when flag 0x4000 is set; version 2 with it
/// refuses. Versions 2 and 3 pad each entry with 1 to 8 NULs to a multiple
/// of 8; version 4 strips a prefix of the previous path (Git's offset
/// varint) and has no padding. The 12-bit name length must equal the path
/// length, or 0xFFF for paths that long or longer. A `link` or `sdir`
/// extension, or any extension whose signature starts with a lowercase
/// letter (Git's "required"), refuses.
pub(crate) fn decode_index(raw: &[u8]) -> Result<Vec<IndexEntry>, &'static str> {
    if raw.len() > INDEX_CAP {
        return Err("index-oversized");
    }
    if raw.len() < 12 + 20 {
        return Err("index-malformed");
    }
    let body = raw.len() - 20;
    if sha1(&raw[..body]) != raw[body..] {
        return Err("index-checksum");
    }
    if &raw[..4] != b"DIRC" {
        return Err("index-malformed");
    }
    let version = u32_at(raw, 4).ok_or("index-malformed")?;
    if !(2..=4).contains(&version) {
        return Err("index-version");
    }
    let count = u32_at(raw, 8).ok_or("index-malformed")? as usize;
    let mut at = 12;
    let mut entries: Vec<IndexEntry> = Vec::new();
    let mut previous: Vec<u8> = Vec::new();
    for _ in 0..count {
        let start = at;
        if at + FIXED > body {
            return Err("index-malformed");
        }
        let mode = u32_at(raw, at + 24).ok_or("index-malformed")?;
        let flags = u16_at(raw, at + 60).ok_or("index-malformed")?;
        at += FIXED;
        if flags & 0x4000 != 0 {
            if version < 3 {
                return Err("index-extended-flags");
            }
            if at + 2 > body {
                return Err("index-malformed");
            }
            at += 2;
        }
        let path = if version == 4 {
            let (strip, used) = varint(&raw[at..body]).ok_or("index-malformed")?;
            at += used;
            if strip > previous.len() {
                return Err("index-prefix");
            }
            let nul = raw[at..body]
                .iter()
                .position(|b| *b == 0)
                .ok_or("index-malformed")?;
            let mut path = previous[..previous.len() - strip].to_vec();
            path.extend_from_slice(&raw[at..at + nul]);
            at += nul + 1;
            path
        } else {
            let nul = raw[at..body]
                .iter()
                .position(|b| *b == 0)
                .ok_or("index-malformed")?;
            let path = raw[at..at + nul].to_vec();
            at += nul;
            // 1 to 8 NULs, to a multiple of eight from the entry's start.
            let pad = 8 - ((at - start) % 8);
            if at + pad > body || raw[at..at + pad].iter().any(|b| *b != 0) {
                return Err("index-malformed");
            }
            at += pad;
            path
        };
        if path.is_empty() {
            return Err("index-malformed");
        }
        let named = usize::from(flags & 0x0FFF);
        if named != path.len().min(0xFFF) {
            return Err("index-name-length");
        }
        previous.clone_from(&path);
        entries.push(IndexEntry { path, mode });
    }
    while at < body {
        if at + 8 > body {
            return Err("index-malformed");
        }
        let signature = &raw[at..at + 4];
        let size = u32_at(raw, at + 4).ok_or("index-malformed")? as usize;
        if signature == b"link" || signature == b"sdir" {
            return Err("index-split-or-sparse");
        }
        if signature[0].is_ascii_lowercase() {
            return Err("index-required-extension");
        }
        at = at
            .checked_add(8)
            .and_then(|a| a.checked_add(size))
            .ok_or("index-malformed")?;
        if at > body {
            return Err("index-malformed");
        }
    }
    Ok(entries)
}
/// Git's offset varint (item 6a): `value = b & 0x7f`, then while the high
/// bit is set, `value = ((value + 1) << 7) | (next & 0x7f)`. Overflow
/// refuses.
fn varint(raw: &[u8]) -> Option<(usize, usize)> {
    let mut used = 0;
    let mut b = *raw.first()?;
    used += 1;
    let mut value = usize::from(b & 0x7f);
    while b & 0x80 != 0 {
        b = *raw.get(used)?;
        used += 1;
        value = value.checked_add(1)?.checked_mul(128)? | usize::from(b & 0x7f);
    }
    Some((value, used))
}

/// The marker's path relative to a repository's worktree root, from the
/// root's components below the `.git` parent (item 6a). The relative part
/// must be ASCII.
pub(crate) fn marker_path(relative: &[&[u8]]) -> Result<Vec<u8>, &'static str> {
    let mut path = Vec::new();
    for component in relative {
        if !component.is_ascii() {
            return Err("path-non-ascii");
        }
        path.extend_from_slice(component);
        path.push(b'/');
    }
    path.extend_from_slice(MARKER_SUFFIX);
    Ok(path)
}
/// Whether any decoded entry is at the marker's path, compared
/// ASCII-case-insensitively (APFS is case-insensitive here). A gitlink
/// entry is never a match.
pub(crate) fn tracks(entries: &[IndexEntry], marker: &[u8]) -> bool {
    entries
        .iter()
        .any(|e| e.mode & 0o170000 != GITLINK && e.path.eq_ignore_ascii_case(marker))
}

// ------------------------------------------------------- native evidence

/// One piece of evidence the recheck compares, each by a stable label: a
/// name observed absent, an object's full metadata sample, or a system
/// source's bytes.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) enum Sample {
    Absent(Vec<u8>),
    Present(Vec<u8>, DescriptorMetadata),
    /// A system source's bytes (refusal-only evidence, rechecked by
    /// re-reading).
    Read(Vec<u8>, Vec<u8>),
}
/// The tracking decision.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum Tracking {
    /// No VCS marker on any directory of the chain, each looked up
    /// positively.
    NoRepository,
    /// Every enclosing repository was examined and none tracks the marker.
    Untracked { repositories: usize },
}
/// Item 6a's observation: the decision and the evidence it rests on, and
/// the identity of the retained chain it walked (B3-b2b2a). Equality, which
/// the held-fence recheck compares, is the decision and the evidence only:
/// item 6a is unchanged.
#[derive(Debug, Clone)]
pub(crate) struct TrackingObservation {
    tracking: Tracking,
    evidence: Vec<Sample>,
    root: ChainIdentity,
}
impl PartialEq for TrackingObservation {
    fn eq(&self, other: &Self) -> bool {
        self.tracking == other.tracking && self.evidence == other.evidence
    }
}
impl Eq for TrackingObservation {}
impl TrackingObservation {
    pub(crate) fn tracking(&self) -> Tracking {
        self.tracking
    }
    pub(crate) fn evidence(&self) -> &[Sample] {
        &self.evidence
    }
}

/// One status read.
const STATUS: WorkCost = WorkCost {
    objects: 0,
    edges: 1,
    bytes: 512,
};
fn label(parts: &[&[u8]]) -> Vec<u8> {
    parts.join(&b'/')
}
fn metadata(file: &File, work: &mut WorkScope<'_>) -> Result<DescriptorMetadata, Failure> {
    work.run(STATUS, |_| {
        opensip_platform::observe_descriptor_metadata(file)
            .map_err(|error| WorkFailure::Operation(TrackingRefusal::Io(error)))
    })
}
fn filesystem(file: &File, work: &mut WorkScope<'_>) -> Result<DescriptorFilesystem, Failure> {
    opensip_platform::observe_filesystem_accounted(file, work).map_err(io_failure)
}
/// macOS `ELOOP`.
const ELOOP: i32 = 62;
fn is_link_or_not_directory(error: &io::Error) -> bool {
    error.raw_os_error() == Some(ELOOP)
        || error.kind() == io::ErrorKind::NotADirectory
        || error.kind() == io::ErrorKind::InvalidInput
}
fn absent(
    directory: &RetainedDirectory,
    name: &str,
    work: &mut WorkScope<'_>,
) -> Result<bool, Failure> {
    directory
        .observe_child_absent_accounted(OsStr::new(name), work)
        .map_err(io_failure)
}
fn open_directory(
    directory: &RetainedDirectory,
    name: &str,
    work: &mut WorkScope<'_>,
) -> Result<io::Result<RetainedDirectory>, Failure> {
    work.run(
        opensip_platform::open_child_directory_cost(OsStr::new(name)),
        |_| Ok::<_, Failure>(directory.open_child_directory(OsStr::new(name))),
    )
}
fn open_file(
    directory: &RetainedDirectory,
    name: &str,
    work: &mut WorkScope<'_>,
) -> Result<io::Result<File>, Failure> {
    work.run(RetainedDirectory::open_regular_cost(name), |_| {
        Ok::<_, Failure>(directory.open_regular(name))
    })
}
fn read(file: &File, cap: usize, reason: &'static str, work: &mut WorkScope<'_>) -> Result<Vec<u8>, Failure> {
    match opensip_platform::read_bounded_observed(file, cap, work)? {
        Ok(raw) => Ok(raw),
        Err(WorkReadFailure::Bound) => unsupported(reason),
        Err(WorkReadFailure::Io(error)) => Err(WorkFailure::Operation(TrackingRefusal::Io(error))),
        Err(_) => unsupported(reason),
    }
}
/// Parse and check one configuration source, charged over its bytes.
fn config(raw: &[u8], work: &mut WorkScope<'_>) -> Result<(), Failure> {
    let cost = WorkCost {
        objects: 1,
        edges: 1,
        bytes: raw.len(),
    };
    work.run(cost, |_| {
        let entries = parse_config(raw).map_err(|r| WorkFailure::Operation(TrackingRefusal::VcsUnsupported(r)))?;
        check_config(&entries).map_err(|r| WorkFailure::Operation(TrackingRefusal::VcsUnsupported(r)))
    })
}

/// `config` for item 6b: the same charge and the same parse and refusals,
/// but the refusal is decided after the charged step returns, so one
/// member's refusal does not latch the discovery ledger that the rest of
/// the pass continues on (`work_ledger.rs`: an error inside a scope closes
/// the ledger).
fn config_decided(raw: &[u8], work: &mut WorkScope<'_>) -> Result<(), Failure> {
    let cost = WorkCost {
        objects: 1,
        edges: 1,
        bytes: raw.len(),
    };
    let verdict = work.run(cost, |_| Ok::<_, Failure>(parse_config(raw).and_then(|entries| check_config(&entries))))?;
    verdict.map_err(|r| WorkFailure::Operation(TrackingRefusal::VcsUnsupported(r)))
}
/// The pass the shared steps run in: item 6a's tracking pass, whose first
/// refusal ends the pass, or item 6b's member pass, whose per-member
/// refusals are decided after each charged step returns, so that they do not
/// latch the discovery ledger the rest of the pass continues on
/// (`work_ledger.rs`: an error inside a scope closes the ledger). The charges
/// and the refusal subjects are the same in both.
#[derive(Clone, Copy)]
enum Pass<'a> {
    Tracking,
    Members(&'a MemberCustody<'a>),
}
impl Pass<'_> {
    fn config(self, raw: &[u8], work: &mut WorkScope<'_>) -> Result<(), Failure> {
        match self {
            Self::Tracking => config(raw, work),
            Self::Members(_) => config_decided(raw, work),
        }
    }
    /// S3 custody of one Git or configuration object.
    fn judge(
        self,
        file: &File,
        object: ProjectObject,
        inputs: &TrackingInputs<'_>,
        reason: &'static str,
        work: &mut WorkScope<'_>,
    ) -> Result<(), Failure> {
        match self {
            Self::Tracking => super::project_chain::judge_project_object(file, object, inputs.uid, inputs.policy, work)
                .map_err(|f| chain_failure(f, reason)),
            Self::Members(custody) => judge_decided(file, object, inputs.uid, custody, reason, work),
        }
    }
}

/// What one evidence pass needs.
pub(crate) struct TrackingInputs<'a> {
    pub(crate) chain: &'a ProjectChain,
    pub(crate) uid: u32,
    pub(crate) policy: &'a ProjectChainPolicy<'a>,
    /// H's spelling (the account database's home, as walked).
    pub(crate) home: &'a Path,
    pub(crate) environment: &'a [(OsString, OsString)],
    /// The fixed system sources; `SYSTEM_SOURCES` in production.
    pub(crate) system_sources: &'a [&'a Path],
}

/// Item 6a: one evidence pass. The order is: the environment; the walk
/// from the root up to `/` (positive no-follow lookups of every VCS marker
/// at every directory); each enclosing repository's layout, config and
/// index; then the global and system configuration sources. Any refusal
/// stops the pass.
pub(crate) fn observe_tracking(
    inputs: &TrackingInputs<'_>,
    work: &mut WorkScope<'_>,
) -> Result<TrackingObservation, Failure> {
    let environment = WorkCost {
        objects: 0,
        edges: inputs.environment.len().max(1),
        bytes: inputs
            .environment
            .iter()
            .map(|(n, v)| n.len() + v.len())
            .sum(),
    };
    work.run(environment, |_| {
        check_environment(inputs.environment, inputs.home)
            .map_err(|r| WorkFailure::Operation(TrackingRefusal::VcsUnsupported(r)))
    })?;
    let mut evidence = Vec::new();
    let repositories = repositories(inputs, &mut evidence, work)?;
    global_sources(inputs, &mut evidence, Pass::Tracking, work)?;
    for source in inputs.system_sources {
        system_source(source, &mut evidence, Pass::Tracking, work)?;
    }
    let tracking = if repositories == 0 {
        Tracking::NoRepository
    } else {
        Tracking::Untracked { repositories }
    };
    Ok(TrackingObservation {
        tracking,
        evidence,
        root: inputs.chain.identity(),
    })
}

/// The held-fence recheck: a fresh evidence pass whose result must equal
/// the retained one (every sample and every absence). Charged to `work`.
pub(crate) fn recheck_tracking(
    observed: &TrackingObservation,
    inputs: &TrackingInputs<'_>,
    work: &mut WorkScope<'_>,
) -> Result<(), Failure> {
    let again = observe_tracking(inputs, work)?;
    if &again == observed {
        Ok(())
    } else {
        unsupported("evidence-changed")
    }
}

/// The upward walk and every enclosing repository. Returns how many
/// repositories were examined; a tracked marker refuses.
fn repositories(
    inputs: &TrackingInputs<'_>,
    evidence: &mut Vec<Sample>,
    work: &mut WorkScope<'_>,
) -> Result<usize, Failure> {
    let chain = inputs.chain;
    let path = chain.path();
    let leaf = path.component_count();
    let spelling = chain.spelling().as_os_str().as_bytes();
    let components: Vec<&[u8]> = spelling[1..].split(|b| *b == b'/').collect();
    let mut found = 0;
    for index in (0..=leaf).rev() {
        let directory = path.directory_at(index).expect("retained index");
        let here = label(&components[..index]);
        for marker in VCS_MARKERS {
            let name = label(&[&here, marker.as_bytes()]);
            if absent(directory, marker, work)? {
                evidence.push(Sample::Absent(name));
                continue;
            }
            if marker != ".git" {
                return unsupported("vcs-other");
            }
            if index <= chain.home_index() {
                return unsupported("repository-at-or-above-home");
            }
            repository(directory, &components[index..], &name, inputs, evidence, work)?;
            found += 1;
        }
    }
    Ok(found)
}

/// One enclosing repository at `directory/.git`: the admitted layout, its
/// config and its index (item 6a), with `relative` the root's components
/// below the `.git` parent.
fn repository(
    directory: &RetainedDirectory,
    relative: &[&[u8]],
    name: &[u8],
    inputs: &TrackingInputs<'_>,
    evidence: &mut Vec<Sample>,
    work: &mut WorkScope<'_>,
) -> Result<(), Failure> {
    let Some(raw) = layout(directory, name, inputs, evidence, Pass::Tracking, work)? else {
        return Ok(());
    };
    let decode = WorkCost {
        objects: 1,
        edges: 1,
        bytes: raw.len().saturating_mul(2),
    };
    let marker = marker_path(relative).map_err(|r| WorkFailure::Operation(TrackingRefusal::VcsUnsupported(r)))?;
    work.run(decode, |_| {
        let entries =
            decode_index(&raw).map_err(|r| WorkFailure::Operation(TrackingRefusal::VcsUnsupported(r)))?;
        if tracks(&entries, &marker) {
            Err(WorkFailure::Operation(TrackingRefusal::MarkerTracked))
        } else {
            Ok(())
        }
    })
}

/// Item 6a's admitted layout of `directory/.git`, shared unchanged by item
/// 6b (X2 r9): the `.git` directory on H's volume under directory custody,
/// no linked worktree, the required configuration (custody-checked, capped
/// and parsed with item 6a's refusals), and the index's bytes when it is
/// present (custody-checked and capped), `None` when it is absent.
fn layout(
    directory: &RetainedDirectory,
    name: &[u8],
    inputs: &TrackingInputs<'_>,
    evidence: &mut Vec<Sample>,
    pass: Pass<'_>,
    work: &mut WorkScope<'_>,
) -> Result<Option<Vec<u8>>, Failure> {
    let git = match open_directory(directory, ".git", work)? {
        Ok(git) => git,
        Err(error) if is_link_or_not_directory(&error) => return unsupported("git-not-directory"),
        Err(error) if error.kind() == io::ErrorKind::NotFound => return unsupported("evidence-changed"),
        Err(error) => return Err(WorkFailure::Operation(TrackingRefusal::Io(error))),
    };
    if !(inputs.policy.home_filesystem())(&filesystem(git.as_file(), work)?) {
        return unsupported("repository-off-home-volume");
    }
    pass.judge(git.as_file(), ProjectObject::Directory, inputs, "git-custody", work)?;
    evidence.push(Sample::Present(name.to_vec(), metadata(git.as_file(), work)?));
    for linked in ["commondir", "config.worktree"] {
        if !absent(&git, linked, work)? {
            return unsupported("linked-worktree");
        }
        evidence.push(Sample::Absent(label(&[name, linked.as_bytes()])));
    }
    // The repository config: required, custody-checked, capped, parsed.
    let file = match open_file(&git, "config", work)? {
        Ok(file) => file,
        Err(error) if error.kind() == io::ErrorKind::NotFound => return unsupported("config-missing"),
        Err(error) if is_link_or_not_directory(&error) => return unsupported("config-not-file"),
        Err(error) => return Err(WorkFailure::Operation(TrackingRefusal::Io(error))),
    };
    let sample = judge_file(&file, inputs, pass, "config-custody", work)?;
    evidence.push(Sample::Present(label(&[name, b"config"]), sample));
    let raw = read(&file, CONFIG_CAP, "config-oversized", work)?;
    pass.config(&raw, work)?;
    // The index: absent means no tracked paths here.
    let file = match open_file(&git, "index", work)? {
        Ok(file) => file,
        Err(error) if error.kind() == io::ErrorKind::NotFound => {
            evidence.push(Sample::Absent(label(&[name, b"index"])));
            return Ok(None);
        }
        Err(error) if is_link_or_not_directory(&error) => return unsupported("index-not-file"),
        Err(error) => return Err(WorkFailure::Operation(TrackingRefusal::Io(error))),
    };
    let sample = judge_file(&file, inputs, pass, "index-custody", work)?;
    evidence.push(Sample::Present(label(&[name, b"index"]), sample));
    read(&file, INDEX_CAP, "index-oversized", work).map(Some)
}

/// A file under item 1's scope: S3 config-file custody (owner the invoking
/// user or root, no group or other write, one link, at most 4 MiB, ACL
/// readable or omitted under the premise), on H's volume. Returns its full
/// metadata sample.
fn judge_file(
    file: &File,
    inputs: &TrackingInputs<'_>,
    pass: Pass<'_>,
    reason: &'static str,
    work: &mut WorkScope<'_>,
) -> Result<DescriptorMetadata, Failure> {
    if !(inputs.policy.home_filesystem())(&filesystem(file, work)?) {
        return unsupported("evidence-off-home-volume");
    }
    pass.judge(file, ProjectObject::ConfigurationFile, inputs, reason, work)?;
    metadata(file, work)
}

/// The global sources under H: `H/.gitconfig` and `H/.config/git/config`
/// (item 6a), through H's retained handle. Each object present must be
/// owned by the invoking user, with no group or other write and one link
/// for files, ACL readable or omitted under the premise, on H's volume
/// (item 1). Each is positively absent or admitted and parsed.
fn global_sources(
    inputs: &TrackingInputs<'_>,
    evidence: &mut Vec<Sample>,
    pass: Pass<'_>,
    work: &mut WorkScope<'_>,
) -> Result<(), Failure> {
    let home = inputs
        .chain
        .path()
        .directory_at(inputs.chain.home_index())
        .expect("H is retained");
    global_file(home, ".gitconfig", b"~/.gitconfig", inputs, evidence, pass, work)?;
    let config = match open_directory(home, ".config", work)? {
        Ok(directory) => directory,
        Err(error) if error.kind() == io::ErrorKind::NotFound => {
            evidence.push(Sample::Absent(b"~/.config".to_vec()));
            return Ok(());
        }
        Err(error) if is_link_or_not_directory(&error) => return unsupported("global-not-directory"),
        Err(error) => return Err(WorkFailure::Operation(TrackingRefusal::Io(error))),
    };
    let sample = judge_owned(config.as_file(), ProjectObject::Directory, inputs, pass, work)?;
    evidence.push(Sample::Present(b"~/.config".to_vec(), sample));
    let git = match open_directory(&config, "git", work)? {
        Ok(directory) => directory,
        Err(error) if error.kind() == io::ErrorKind::NotFound => {
            evidence.push(Sample::Absent(b"~/.config/git".to_vec()));
            return Ok(());
        }
        Err(error) if is_link_or_not_directory(&error) => return unsupported("global-not-directory"),
        Err(error) => return Err(WorkFailure::Operation(TrackingRefusal::Io(error))),
    };
    let sample = judge_owned(git.as_file(), ProjectObject::Directory, inputs, pass, work)?;
    evidence.push(Sample::Present(b"~/.config/git".to_vec(), sample));
    global_file(&git, "config", b"~/.config/git/config", inputs, evidence, pass, work)
}
fn global_file(
    directory: &RetainedDirectory,
    name: &str,
    shown: &[u8],
    inputs: &TrackingInputs<'_>,
    evidence: &mut Vec<Sample>,
    pass: Pass<'_>,
    work: &mut WorkScope<'_>,
) -> Result<(), Failure> {
    let file = match open_file(directory, name, work)? {
        Ok(file) => file,
        Err(error) if error.kind() == io::ErrorKind::NotFound => {
            evidence.push(Sample::Absent(shown.to_vec()));
            return Ok(());
        }
        Err(error) if is_link_or_not_directory(&error) => return unsupported("global-not-file"),
        Err(error) => return Err(WorkFailure::Operation(TrackingRefusal::Io(error))),
    };
    let sample = judge_owned(&file, ProjectObject::ConfigurationFile, inputs, pass, work)?;
    evidence.push(Sample::Present(shown.to_vec(), sample));
    let raw = read(&file, CONFIG_CAP, "config-oversized", work)?;
    pass.config(&raw, work)
}
/// A global object: item 1's custody, owned by the invoking user exactly.
fn judge_owned(
    file: &File,
    object: ProjectObject,
    inputs: &TrackingInputs<'_>,
    pass: Pass<'_>,
    work: &mut WorkScope<'_>,
) -> Result<DescriptorMetadata, Failure> {
    if !(inputs.policy.home_filesystem())(&filesystem(file, work)?) {
        return unsupported("global-off-home-volume");
    }
    pass.judge(file, object, inputs, "global-custody", work)?;
    let sample = metadata(file, work)?;
    if sample.uid != inputs.uid {
        return unsupported("global-custody");
    }
    Ok(sample)
}

/// One fixed system source, as refusal-only evidence (r7): opened by its
/// fixed path, following symbolic links, charged and capped. `ENOENT`
/// anywhere on the path is absence. No custody is judged; the source can
/// only refuse. Anything else that stops the read (permission, I/O, a
/// non-regular file, over the cap) is `vcs-unsupported`. The evidence is
/// the bytes read, so the recheck is a re-read.
fn system_source(
    source: &Path,
    evidence: &mut Vec<Sample>,
    pass: Pass<'_>,
    work: &mut WorkScope<'_>,
) -> Result<(), Failure> {
    let shown = source.as_os_str().as_bytes().to_vec();
    let opened = work.run(
        opensip_platform::open_fixed_regular_following_cost(source),
        |_| Ok::<_, Failure>(opensip_platform::open_fixed_regular_following(source)),
    )?;
    let file = match opened {
        Ok(file) => file,
        Err(error) if error.kind() == io::ErrorKind::NotFound => {
            evidence.push(Sample::Absent(shown));
            return Ok(());
        }
        Err(error) if error.kind() == io::ErrorKind::InvalidInput => {
            return unsupported("system-source-not-regular");
        }
        Err(_) => return unsupported("system-source-unreadable"),
    };
    let raw = match opensip_platform::read_bounded_observed(&file, CONFIG_CAP, work)? {
        Ok(raw) => raw,
        Err(WorkReadFailure::Bound) => return unsupported("config-oversized"),
        Err(_) => return unsupported("system-source-unreadable"),
    };
    pass.config(&raw, work)?;
    evidence.push(Sample::Read(shown, raw));
    Ok(())
}

// ------------------------------------------- item 6b: the member observation

/// Item 6a's observation of one root, bound to the retained chain it walked
/// (r3, Codex B3B1-R2-RF-1). Only `observe_root` constructs it, from the
/// chain of the inputs it observed, so the binding is the borrow itself: no
/// label, spelling or birth comparison stands in for it.
#[derive(Debug)]
pub(crate) struct RootObservation<'a> {
    chain: &'a ProjectChain,
    observation: TrackingObservation,
}
impl<'a> RootObservation<'a> {
    pub(crate) fn observation(&self) -> &TrackingObservation {
        &self.observation
    }
    pub(crate) fn into_observation(self) -> TrackingObservation {
        self.observation
    }
    /// The precondition of item 6b, when the observation is `NoRepository`.
    pub(crate) fn no_repository(&self) -> Option<NoRepository<'a>> {
        (self.observation.tracking == Tracking::NoRepository).then_some(NoRepository(self.chain))
    }
}

/// Item 6a over `inputs`, bound to `inputs.chain` (r3). The evidence pass is
/// `observe_tracking` unchanged.
pub(crate) fn observe_root<'a>(
    inputs: &TrackingInputs<'a>,
    work: &mut WorkScope<'_>,
) -> Result<RootObservation<'a>, Failure> {
    let observation = observe_tracking(inputs, work)?;
    Ok(RootObservation {
        chain: inputs.chain,
        observation,
    })
}

/// Proof that item 6a observed W as `NoRepository` (W2), the precondition of
/// item 6b (X2 r9; law M3-B item 21). It holds the retained chain item 6a
/// walked, and item 6b takes W from it (r3, Codex B3B1-R2-RF-1): there is no
/// second chain to substitute. Only `RootObservation::no_repository`
/// constructs it, so 6b cannot run without W2.
#[derive(Debug, Clone, Copy)]
pub(crate) struct NoRepository<'a>(&'a ProjectChain);
impl<'a> NoRepository<'a> {
    /// The proof for `chain` from an observation stored apart from it (M3-B
    /// unit B3-b2b2a, the operation handoff): only when `observed` is
    /// `NoRepository` and was observed over this very chain, by its
    /// never-reused identity. Another chain, at any spelling, gets none.
    pub(crate) fn retained(chain: &'a ProjectChain, observed: &TrackingObservation) -> Option<Self> {
        (observed.tracking == Tracking::NoRepository && observed.root == chain.identity()).then_some(Self(chain))
    }
}

/// The custody facts item 6b judges member Git evidence with: the trusted
/// groups and the ACL-omission premise of this invocation. They also build
/// the pass's `ProjectChainPolicy`, so there is one source (r2, Codex
/// B3B1-R1-RF-1). No owner waiver: `--trust-project-owner` never reaches
/// member Git evidence (law M3-B item 23).
pub(crate) struct MemberCustody<'a> {
    pub(crate) trust_groups: &'a BTreeSet<u32>,
    pub(crate) premise: Option<&'a AclOmissionPremise>,
}

/// What one item-6b pass needs (r2): the invoking user, H, the check that a
/// filesystem is H's, the environment and system sources of item 6a, and the
/// custody facts. W's retained chain is the proof's (r3).
pub(crate) struct MemberInputs<'a> {
    pub(crate) uid: u32,
    pub(crate) home: &'a Path,
    pub(crate) home_filesystem: &'a dyn Fn(&DescriptorFilesystem) -> bool,
    pub(crate) environment: &'a [(OsString, OsString)],
    pub(crate) system_sources: &'a [&'a Path],
    pub(crate) custody: MemberCustody<'a>,
}

/// Item 6b's S3 custody judgment of one object (r2, Codex B3B1-R1-RF-1):
/// `judge_project_object`'s capture, charge, pure check (the shared order)
/// and premise, but the capture is `capture_descriptor_acl_observed`, so a
/// native capture refusal returns as a value and is decided after the
/// charged step, never latching the ledger. A capture refusal and a custody
/// refusal are this object's `reason`, as in item 6a. Host I/O, including
/// the premise's own filesystem sample, fails the pass (LD-B3B1-2).
fn judge_decided(
    file: &File,
    object: ProjectObject,
    uid: u32,
    custody: &MemberCustody<'_>,
    reason: &'static str,
    work: &mut WorkScope<'_>,
) -> Result<(), Failure> {
    let captured = opensip_platform::capture_descriptor_acl_observed::<TrackingRefusal>(file, work)?;
    #[cfg(test)]
    let captured = tests::injected_capture(captured);
    let sample = match captured {
        Ok(sample) => sample,
        Err(DescriptorAclCaptureError::Io(error)) => {
            return Err(WorkFailure::Operation(TrackingRefusal::Io(error)));
        }
        Err(_) => return unsupported(reason),
    };
    let judged = check_project_object_ordered(
        sample.metadata(),
        sample.acl_state(),
        |index| sample.entry(index),
        uid,
        custody.trust_groups,
        object,
        None,
        CustodyOrder::Shared,
    );
    match judged {
        Ok(()) => Ok(()),
        Err(crate::custody::Refusal::AclUnreadable) if sample.acl_state() == CapturedAclState::NotReturned => {
            let admitted = match custody.premise {
                Some(premise) => premise.admits(file, work).map_err(|failure| match failure {
                    WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
                    WorkFailure::Operation(refusal) => WorkFailure::Operation(TrackingRefusal::Io(io::Error::other(format!("{refusal:?}")))),
                })?,
                None => false,
            };
            if !admitted {
                return unsupported(reason);
            }
            check_project_object_ordered(
                sample.metadata(),
                CapturedAclState::Entries(0),
                |_| None,
                uid,
                custody.trust_groups,
                object,
                None,
                CustodyOrder::Shared,
            )
            .or_else(|_| unsupported(reason))
        }
        Err(_) => unsupported(reason),
    }
}

/// The deepest member below W (law M3-B item 19, M1).
pub(crate) const MAX_MEMBER_DEPTH: usize = 256;

/// A declared member's path below W: canonical, relative and at most 256
/// segments (no empty, `.` or `..` segment, no NUL), as placement admitted
/// it.
#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord)]
pub(crate) struct MemberPath(Vec<Vec<u8>>);
impl MemberPath {
    pub(crate) fn new(relative: &[u8]) -> Option<Self> {
        let segments: Vec<Vec<u8>> = relative.split(|b| *b == b'/').map(<[u8]>::to_vec).collect();
        let canonical = !relative.is_empty()
            && segments.len() <= MAX_MEMBER_DEPTH
            && segments
                .iter()
                .all(|s| !s.is_empty() && s != b"." && s != b".." && !s.contains(&0));
        canonical.then_some(Self(segments))
    }
    fn spelling(&self) -> Vec<u8> {
        self.0.join(&b'/')
    }
}

/// Why item 6b did not admit a declared member. Item 8's subjects under
/// `PROJECT.ROOT_CUSTODY_REFUSED` (X2 r9): a branch-A member refuses with
/// it, and a branch-B member is excluded and disclosed with it (item 24).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum MemberRefusal {
    /// Placement, layout, configuration or index outside item 6a's closed
    /// layout, with 6a's reason.
    VcsUnsupported(&'static str),
    /// A device change on the way from W to the member (M1).
    OutsideVolume,
}
impl MemberRefusal {
    pub(crate) fn subject(self) -> String {
        match self {
            Self::VcsUnsupported(reason) => format!("member-vcs-unsupported:{reason}"),
            Self::OutsideVolume => "member-outside-volume".to_owned(),
        }
    }
}

/// Item 6b's verdict on one declared member.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) enum MemberVerdict {
    /// Admitted. The member index's gitlink paths are nested repositories
    /// inside the member; they stay boundaries.
    Admitted { gitlinks: Vec<Vec<u8>> },
    Refused(MemberRefusal),
}

/// Item 6b (X2 r9; law M3-B item 21): the member observation, after the
/// fence is released, on the caller's discovery ledger. The environment, the
/// global sources and the system sources are checked once for the pass (a
/// refusal there refuses every member with its reason); then each member, in
/// the order given (ascending path order), is reached from W's retained
/// descriptor by no-follow opens, with positive lookups of every VCS marker
/// at every directory strictly between W and M and at M, on W's device, and
/// passes item 6a's admitted layout unchanged (`layout`): `M/.git`,
/// `M/.git/config` and `M/.git/index` only. Nothing is written; no evidence
/// is retained for a recheck (C1's per-read custody covers the snapshot).
/// Host I/O and ledger exhaustion fail the pass.
pub(crate) fn observe_members(
    member_inputs: &MemberInputs<'_>,
    root: NoRepository<'_>,
    members: &[MemberPath],
    work: &mut WorkScope<'_>,
) -> Result<Vec<MemberVerdict>, Failure> {
    let session = MemberSession::begin(member_inputs, root, work)?;
    members.iter().map(|member| session.observe(member, work)).collect()
}

/// Item 6b as a session (M3-B unit B3-b2b2a): the environment, the global
/// sources and the system sources are checked once, at `begin`; then
/// `observe` gives one member's verdict, with exactly `observe_members`'
/// steps and charges for it. The decision core asks one candidate at a time
/// (B3-b2b1, Codex B3B2B1-R1-RF-2), and pays the pass-level check once.
pub(crate) struct MemberSession<'a> {
    inputs: &'a MemberInputs<'a>,
    chain: &'a ProjectChain,
    policy: ProjectChainPolicy<'a>,
    /// A pass-level refusal: every member's verdict, with its reason.
    refused: Option<&'static str>,
    /// W's device, sampled once the pass-level sources pass.
    device: u64,
}
impl<'a> MemberSession<'a> {
    pub(crate) fn begin(
        member_inputs: &'a MemberInputs<'a>,
        root: NoRepository<'a>,
        work: &mut WorkScope<'_>,
    ) -> Result<Self, Failure> {
        // r3 (B3B1-R2-RF-1): W is the retained chain item 6a walked.
        let NoRepository(chain) = root;
        let mut session = Self {
            inputs: member_inputs,
            chain,
            policy: ProjectChainPolicy::new(
                member_inputs.custody.premise,
                member_inputs.home_filesystem,
                member_inputs.custody.trust_groups,
            ),
            refused: None,
            device: 0,
        };
        let inputs = &session.tracking_inputs();
        let pass = Pass::Members(&member_inputs.custody);
        let environment = WorkCost {
            objects: 0,
            edges: inputs.environment.len().max(1),
            bytes: inputs.environment.iter().map(|(n, v)| n.len() + v.len()).sum(),
        };
        let mut ignored = Vec::new();
        let sources = work
            .run(environment, |_| Ok::<_, Failure>(check_environment(inputs.environment, inputs.home)))
            .and_then(|verdict| verdict.map_err(|r| WorkFailure::Operation(TrackingRefusal::VcsUnsupported(r))))
            .and_then(|()| global_sources(inputs, &mut ignored, pass, work))
            .and_then(|()| {
                inputs
                    .system_sources
                    .iter()
                    .try_for_each(|source| system_source(source, &mut ignored, pass, work))
            });
        match sources {
            Ok(()) => {}
            Err(WorkFailure::Operation(TrackingRefusal::VcsUnsupported(reason))) => {
                session.refused = Some(reason);
                return Ok(session);
            }
            Err(other) => return Err(other),
        }
        session.device = metadata(session.w().as_file(), work)?.device;
        Ok(session)
    }
    fn tracking_inputs(&self) -> TrackingInputs<'_> {
        TrackingInputs {
            chain: self.chain,
            uid: self.inputs.uid,
            policy: &self.policy,
            home: self.inputs.home,
            environment: self.inputs.environment,
            system_sources: self.inputs.system_sources,
        }
    }
    fn w(&self) -> &'a RetainedDirectory {
        self.chain
            .path()
            .directory_at(self.chain.path().component_count())
            .expect("W is retained")
    }
    /// One member's verdict. Host I/O and ledger exhaustion fail the pass.
    pub(crate) fn observe(&self, member: &MemberPath, work: &mut WorkScope<'_>) -> Result<MemberVerdict, Failure> {
        self.observe_identified(member, work).map(|(verdict, _)| verdict)
    }
    /// `observe`, with the status of every object item 6b opened for the
    /// verdict, W-relative: each directory from W's child to M, `M/.git`,
    /// and its config and index (unit B3-b2b2b r3, Codex B3B2B2B-R2-RF-2).
    /// The caller binds each to the object its own observations bound. The
    /// statuses are the ones item 6b already samples: no new charge.
    pub(crate) fn observe_identified(
        &self,
        member: &MemberPath,
        work: &mut WorkScope<'_>,
    ) -> Result<(MemberVerdict, MemberIdentities), Failure> {
        if let Some(reason) = self.refused {
            return Ok((MemberVerdict::Refused(MemberRefusal::VcsUnsupported(reason)), Vec::new()));
        }
        let inputs = &self.tracking_inputs();
        let pass = Pass::Members(&self.inputs.custody);
        let mut identities = Vec::new();
        let verdict = match member_layout(self.w(), self.device, member, inputs, pass, &mut identities, work) {
            Ok(gitlinks) => MemberVerdict::Admitted { gitlinks },
            Err(WorkFailure::Operation(MemberFailure::Refused(refusal))) => MemberVerdict::Refused(refusal),
            Err(WorkFailure::Operation(MemberFailure::Pass(failure))) => return Err(failure),
            Err(WorkFailure::Budget(budget)) => return Err(WorkFailure::Budget(budget)),
        };
        Ok((verdict, identities))
    }
}

/// One member's refusal, or a failure of the whole pass.
enum MemberFailure {
    Refused(MemberRefusal),
    Pass(Failure),
}
fn member_failure(failure: Failure) -> WorkFailure<MemberFailure> {
    match failure {
        WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
        WorkFailure::Operation(TrackingRefusal::VcsUnsupported(reason)) => {
            WorkFailure::Operation(MemberFailure::Refused(MemberRefusal::VcsUnsupported(reason)))
        }
        other => WorkFailure::Operation(MemberFailure::Pass(other)),
    }
}
fn member_refused<T>(refusal: MemberRefusal) -> Result<T, WorkFailure<MemberFailure>> {
    Err(WorkFailure::Operation(MemberFailure::Refused(refusal)))
}

/// The objects item 6b opened for one verdict, W-relative, each with its
/// status (unit B3-b2b2b r3).
pub(crate) type MemberIdentities = Vec<(Vec<u8>, DescriptorMetadata)>;

/// `M/.git` (an empty `rest`) or `M/.git/<rest>`.
fn label_in_git(member: &[u8], rest: &[u8]) -> Vec<u8> {
    let mut path = member.to_vec();
    path.extend_from_slice(b"/.git");
    if !rest.is_empty() {
        path.push(b'/');
        path.extend_from_slice(rest);
    }
    path
}

/// Placement (M1, M2) and item 6a's layout for one member; returns its
/// index's gitlink paths.
fn member_layout(
    root: &RetainedDirectory,
    device: u64,
    member: &MemberPath,
    inputs: &TrackingInputs<'_>,
    pass: Pass<'_>,
    identities: &mut MemberIdentities,
    work: &mut WorkScope<'_>,
) -> Result<Vec<Vec<u8>>, WorkFailure<MemberFailure>> {
    let mut opened: Vec<RetainedDirectory> = Vec::with_capacity(member.0.len());
    for (index, segment) in member.0.iter().enumerate() {
        let parent = opened.last().unwrap_or(root);
        let name = OsStr::from_bytes(segment);
        let child = match work
            .run(opensip_platform::open_child_directory_cost(name), |_| {
                Ok::<_, Failure>(parent.open_child_directory(name))
            })
            .map_err(member_failure)?
        {
            Ok(child) => child,
            // The placement the declaration was counted under no longer holds.
            Err(error) if is_link_or_not_directory(&error) || error.kind() == io::ErrorKind::NotFound => {
                return member_refused(MemberRefusal::VcsUnsupported("evidence-changed"));
            }
            Err(error) => return Err(member_failure(WorkFailure::Operation(TrackingRefusal::Io(error)))),
        };
        let sample = metadata(child.as_file(), work).map_err(member_failure)?;
        // Every directory item 6b opens, with the status its device check
        // already charged (unit B3-b2b2b r3, Codex B3B2B2B-R2-RF-2).
        identities.push((member.0[..=index].join(&b'/'), sample.clone()));
        if sample.device != device {
            return member_refused(MemberRefusal::OutsideVolume);
        }
        let at_member = index + 1 == member.0.len();
        for marker in VCS_MARKERS {
            let missing = absent(&child, marker, work).map_err(member_failure)?;
            match (at_member, marker == ".git", missing) {
                // At M, `.git` must be there; every other marker must not.
                (true, true, true) => return member_refused(MemberRefusal::VcsUnsupported("evidence-changed")),
                (true, false, false) => return member_refused(MemberRefusal::VcsUnsupported("vcs-other")),
                // Strictly between W and M, no marker at all (M2). Another
                // VCS is `vcs-other`; a `.git` means the counted candidate
                // was not the first repository on the path any more.
                (false, false, false) => return member_refused(MemberRefusal::VcsUnsupported("vcs-other")),
                (false, true, false) => return member_refused(MemberRefusal::VcsUnsupported("evidence-changed")),
                _ => {}
            }
        }
        opened.push(child);
    }
    let directory = opened.last().expect("a member has at least one segment");
    let spelling = member.spelling();
    let mut evidence = Vec::new();
    let laid = layout(directory, &spelling, inputs, &mut evidence, pass, work);
    // Item 6a's layout samples, which it already charged: `M/.git`,
    // `M/.git/config` and `M/.git/index` (unit B3-b2b2b r3).
    for sample in evidence {
        if let Sample::Present(label, md) = sample {
            let path = match label.strip_prefix(spelling.as_slice()) {
                Some(b"") => label_in_git(&spelling, b""),
                Some(rest) => label_in_git(&spelling, rest.strip_prefix(b"/").unwrap_or(rest)),
                None => continue,
            };
            identities.push((path, md));
        }
    }
    let Some(raw) = laid.map_err(member_failure)? else {
        return Ok(Vec::new());
    };
    let decode = WorkCost {
        objects: 1,
        edges: 1,
        bytes: raw.len().saturating_mul(2),
    };
    // Decided after the charged step returns (`config_decided`).
    let decoded = work.run(decode, |_| Ok::<_, Failure>(decode_index(&raw))).map_err(member_failure)?;
    match decoded {
        Ok(entries) => Ok(entries
            .into_iter()
            .filter(|e| e.mode & 0o170000 == GITLINK)
            .map(|e| e.path)
            .collect()),
        Err(reason) => member_refused(MemberRefusal::VcsUnsupported(reason)),
    }
}

#[cfg(test)]
mod tests {
    include!("git_tracking_tests.rs");
    include!("git_tracking_member_tests.rs");
}
