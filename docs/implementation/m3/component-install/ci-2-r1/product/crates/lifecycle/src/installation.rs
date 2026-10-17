//! Law CI r5 items 4 and 5, with amendments CI-A1 (accepted) and CI-A2
//! (proposed with this unit) (unit CI-2; component installation plan r3):
//! the component store and the installer transaction.
//!
//! One installation installs one admitted catalog release for the host's
//! platform, from an operator-supplied profile-1 archive, into
//! `<installRoot>/components/<closure2-hex>/`. The transaction:
//! 1. **Admit:** the release's artifact row, its profile and digests, the
//!    tree's capacities and `archiveLength` (CI-1's codec), the generation
//!    record's exact length `R`, and the admission bound, all before any
//!    acquisition. The bound is reserved (LD-CI2-3), and every later charge
//!    draws from that reservation. If `<closure2-hex>` exists, the
//!    re-install path verifies it instead (LD-CI-6).
//! 2. **Stage** directly in the store, and stream the archive through the
//!    codec into `tree/`, member by member, in member order (CI-A2-a).
//! 3. **V1:** the staged tree, its staging modes and every file's bytes,
//!    re-read.
//! 4. **Finalize** in a branch-local post-order (CI-A1): each file's final
//!    mode then its barrier, each directory's after its descendants, then
//!    `generation.json`, `pin.lock` and the stage's barrier.
//! 5. **V2:** the final modes, the record and `pin.lock`'s state.
//! 6. **Publish,** funded: the exclusive same-parent rename and the store's
//!    barrier inside one reservation.
//!
//! No step retries, repairs or cleans up (LD-CI-12): a failed act leaves an
//! inert stage, which only GC's census removes.
//!
//! Every charge is made before its operation, at the published prices of
//! item 4's recipes; `install_bound` computes the same recipe before
//! acquisition, and the controls enumerate both independently.
use crate::retained_tree::{self, PinRequest, TreeReadFailure};
use opensip_identity::JsonValue as V;
use opensip_platform::component_tree::{
    self as ct, Access, EntryKind, NATIVE_CALL, TreeFile, TreeOpenError,
};
use opensip_platform::{
    DirectoryRenameClass, ExclusiveDirectoryError, ExclusiveDirectoryOutcome,
    ExclusiveRegularError, ExclusiveRegularOutcome, RetainedDirectory, WorkBudgetError, WorkCost,
    WorkFailure, WorkScope, create_exclusive_directory_cost, create_exclusive_regular_cost,
    descriptor_acl_capture_cost, directory_barrier_cost, exclusive_publication_cost,
    private_directory_stage_cost,
};
use opensip_security::archive_profile::{
    self as ap, ArchiveEvent, ArchivePlan, ArchiveRefusal, ArchiveRows, RowKind, TreeRow,
};
use opensip_security::snapshot_source::{
    CustodyDirectoryRefusal, admit_custody_directory, owned_record,
};
use opensip_security::{AuthenticatedComponent, ClosureCandidate, SelectedPlatform};
use std::ffi::OsStr;
use std::fs::File;
use std::io::{self, Read};
use std::path::Path;

// ---- Prices (LAW item 4's shorthands) ----

/// The shared read buffer's size (SNAP's `READ_CHUNK`).
pub(crate) const READ_CHUNK: usize = 65_536;
/// The bounded reader's first growth (SNAP; `work_reader.rs`, `CHUNK`).
const FIRST_GROWTH: usize = 4096;
/// `rd`: one read attempt or one `readdir`.
pub(crate) const READ: WorkCost = NATIVE_CALL;
/// One comparison of a charged merge sort or binary search (CI-A1-b,
/// CI-A2), charged immediately before it.
pub(crate) const COMPARISON: WorkCost = NATIVE_CALL;
/// A generation's name: exactly 64 lowercase hex digits (LAW item 5).
pub(crate) const NAME_BYTES: usize = 64;
/// The generation record and the pin file (LAW item 5).
pub(crate) const RECORD: &str = "generation.json";
pub(crate) const PIN: &str = "pin.lock";
pub(crate) const TREE: &str = "tree";

/// `buf`: SNAP's `buffer_cost()` (`crates/host/src/snapshot.rs`), the same
/// expression; a source pin compares the two.
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

/// `env(x)`: the read-attempt envelope `2·⌈x / 64 KiB⌉ + 2` (SNAP).
pub(crate) fn envelope(size: u64) -> u64 {
    size.div_ceil(READ_CHUNK as u64)
        .saturating_mul(2)
        .saturating_add(2)
}

/// One traversal level: the stack slot `desc(k)` prices (LD-CI2-4).
pub(crate) struct Level {
    pub(crate) directory: RetainedDirectory,
    /// The directory's row, or `None` for `tree/` itself.
    pub(crate) row: Option<u32>,
    /// The children visited so far, compared with the listing at pop.
    pub(crate) children: usize,
}

/// `desc(k)`: entering one directory whose name is `k` bytes by a no-follow
/// `openat` from its parent: `{objects 3, edges 3, bytes k + 1 + 4·LEVEL}`,
/// D3a-0's descent formula over this traversal's own level type (LD-CI2-4).
pub(crate) fn descend_cost(name: usize) -> WorkCost {
    WorkCost {
        objects: 3,
        edges: 3,
        bytes: name
            .saturating_add(1)
            .saturating_add(4 * std::mem::size_of::<Level>()),
    }
}

/// `cust`: one directory's custody check, at its actual charge (LAW r5,
/// NBO-1).
pub(crate) fn custody_cost() -> WorkCost {
    descriptor_acl_capture_cost()
}

/// One merge sort's two `u32` index buffers, one each (CI-A1-b, CI-A2):
/// objects 1 and bytes `n·size_of::<u32>()`.
pub(crate) fn index_buffer_cost(n: usize) -> Option<WorkCost> {
    Some(WorkCost {
        objects: 1,
        edges: 0,
        bytes: n.checked_mul(size_of::<u32>())?,
    })
}

/// At most `n·⌈log₂ n⌉` comparisons; 0 for `n = 1`.
pub(crate) fn sort_comparisons(n: usize) -> Option<usize> {
    if n < 2 {
        return Some(0);
    }
    n.checked_mul((usize::BITS - (n - 1).leading_zeros()) as usize)
}

/// At most `⌈log₂ n⌉ + 1` comparisons for one binary search (CI-A2-b, -c).
pub(crate) fn search_comparisons(n: usize) -> usize {
    if n < 2 {
        1
    } else {
        (usize::BITS - (n - 1).leading_zeros()) as usize + 1
    }
}

/// Checked arithmetic over costs (LAW item 4): `sum` adds, `times` scales.
#[derive(Clone, Copy, Debug, Default, PartialEq, Eq)]
pub(crate) struct Bound(pub(crate) WorkCost);
impl Bound {
    pub(crate) fn add(self, cost: WorkCost) -> Option<Self> {
        Some(Self(self.0.checked_add(cost)?))
    }
    pub(crate) fn add_times(self, cost: WorkCost, count: usize) -> Option<Self> {
        self.add(times(cost, count)?)
    }
}
pub(crate) fn times(cost: WorkCost, count: usize) -> Option<WorkCost> {
    Some(WorkCost {
        objects: cost.objects.checked_mul(count)?,
        edges: cost.edges.checked_mul(count)?,
        bytes: cost.bytes.checked_mul(count)?,
    })
}
fn to_usize(n: u64) -> Option<usize> {
    usize::try_from(n).ok()
}

// ---- The tree, borrowed from the validated manifest ----

/// The selected platform's TreeCommitment rows, borrowed (LAW item 2).
/// Nothing is copied: each row is read from the manifest value on demand.
#[derive(Clone, Copy)]
pub(crate) struct Tree<'a> {
    entries: &'a [V],
    pub(crate) n: usize,
    pub(crate) files: usize,
    pub(crate) dirs: usize,
}

/// A row the validated manifest's shape cannot produce; the archive plan
/// refuses it (`Rows/Text`), so it can never admit anything.
const INVALID: TreeRow<'static> = TreeRow {
    path: "",
    mode: 0,
    kind: RowKind::Dir,
};

fn member<'v>(v: &'v V, key: &str) -> Option<&'v V> {
    match v {
        V::Object(m) => m.get(key),
        _ => None,
    }
}
fn text(v: &V) -> Option<&str> {
    match v {
        V::String(s) => Some(s),
        _ => None,
    }
}
fn items(v: &V) -> Option<&[V]> {
    match v {
        V::Array(a) => Some(a),
        _ => None,
    }
}
fn hex_digest(s: &str) -> Option<[u8; 32]> {
    let b = s.as_bytes();
    if b.len() != 64 {
        return None;
    }
    let nibble = |c: u8| match c {
        b'0'..=b'9' => Some(c - b'0'),
        b'a'..=b'f' => Some(c - b'a' + 10),
        _ => None,
    };
    let mut out = [0u8; 32];
    for (i, o) in out.iter_mut().enumerate() {
        *o = (nibble(b[2 * i])? << 4) | nibble(b[2 * i + 1])?;
    }
    Some(out)
}
fn parse_row(entry: &V) -> Option<TreeRow<'_>> {
    let path = text(member(entry, "path")?)?;
    let mode = text(member(entry, "mode")?)?;
    let mode = u32::from_str_radix(mode, 8).ok()?;
    let kind = match text(member(entry, "type")?)? {
        "file" => {
            let V::Integer(n) = member(entry, "length")? else {
                return None;
            };
            RowKind::File {
                length: u64::try_from(n.get()).ok()?,
                sha256: hex_digest(text(member(entry, "sha256")?)?)?,
            }
        }
        "dir" => RowKind::Dir,
        "symlink" => RowKind::Symlink {
            target: text(member(entry, "target")?)?,
        },
        _ => return None,
    };
    Some(TreeRow { path, mode, kind })
}

impl<'a> Tree<'a> {
    /// The selected platform row's entries, each checked to parse. The
    /// manifest's admission guarantees the shape; a failure here is the
    /// caller's bug (`Evidence`).
    pub(crate) fn of(manifest: &'a V, platform: SelectedPlatform<'_>) -> Option<Self> {
        let mut row = None;
        for candidate in items(member(manifest, "platforms")?)? {
            if text(member(candidate, "os")?)? == platform.os
                && text(member(candidate, "arch")?)? == platform.arch
            {
                row = Some(candidate);
            }
        }
        let entries = items(member(member(row?, "tree")?, "entries")?)?;
        let (mut files, mut dirs) = (0, 0);
        for entry in entries {
            match parse_row(entry)?.kind {
                RowKind::File { .. } => files += 1,
                RowKind::Dir => dirs += 1,
                RowKind::Symlink { .. } => {}
            }
        }
        if entries.is_empty() || entries.len() > ap::MAX_ENTRIES {
            return None;
        }
        Some(Self {
            entries,
            n: entries.len(),
            files,
            dirs,
        })
    }
    pub(crate) fn row(&self, index: u32) -> TreeRow<'a> {
        self.entries
            .get(index as usize)
            .and_then(parse_row)
            .unwrap_or(INVALID)
    }
    /// Every row, in manifest order.
    pub(crate) fn rows(&self) -> impl Iterator<Item = TreeRow<'a>> + '_ {
        (0..self.n as u32).map(|i| self.row(i))
    }
}

/// The rows in an index's order, for CI-1's codec (member order, CI-A2-a).
pub(crate) struct Ordered<'t, 'a> {
    pub(crate) tree: &'t Tree<'a>,
    pub(crate) order: &'t [u32],
}
impl ArchiveRows for Ordered<'_, '_> {
    fn count(&self) -> usize {
        self.order.len()
    }
    fn row(&self, position: usize) -> TreeRow<'_> {
        self.order
            .get(position)
            .map_or(INVALID, |&i| self.tree.row(i))
    }
}

/// A path's last component and its parent (`""` at the root).
pub(crate) fn split(path: &str) -> (&str, &str) {
    path.rsplit_once('/').unwrap_or(("", path))
}
/// `k(e)`: the number of `/`-separated components.
pub(crate) fn depth(path: &str) -> usize {
    path.bytes().filter(|&b| b == b'/').count() + 1
}

/// PKG-AP's member order: the path's UTF-8 bytes (CI-A2-a).
pub(crate) fn byte_less(a: &str, b: &str) -> bool {
    a.as_bytes() < b.as_bytes()
}
/// Path component sequence order (CI-A1-b): component-wise byte comparison,
/// so each directory's descendants follow it contiguously.
pub(crate) fn component_cmp(a: &str, b: &str) -> std::cmp::Ordering {
    let key = |c: u8| if c == b'/' { 0u16 } else { c as u16 + 1 };
    a.bytes().map(key).cmp(b.bytes().map(key))
}

/// A deterministic bottom-up merge sort of `0..n` (C2a r4's R3-RF-2 recipe
/// as CI-A1-b and CI-A2 price it): each of the two `u32` index buffers is
/// charged immediately before it is allocated, and one edge immediately
/// before each comparison, at most `n·⌈log₂ n⌉`. Returns the sorted index;
/// the other buffer is dropped.
pub(crate) fn charged_sort<E>(
    n: usize,
    work: &mut WorkScope<'_>,
    mut less: impl FnMut(u32, u32) -> bool,
) -> Result<Vec<u32>, WorkFailure<E>> {
    let buffer = index_buffer_cost(n).ok_or(WorkFailure::Budget(WorkBudgetError::Arithmetic))?;
    let count = u32::try_from(n).map_err(|_| WorkFailure::Budget(WorkBudgetError::Arithmetic))?;
    work.charge(buffer)?;
    let mut from = Vec::with_capacity(n);
    from.extend(0..count);
    work.charge(buffer)?;
    let mut to = Vec::with_capacity(n);
    to.extend(0..count);
    let mut width = 1;
    while width < n {
        let mut low = 0;
        while low < n {
            let mid = (low + width).min(n);
            let high = (low + 2 * width).min(n);
            let (mut i, mut j, mut k) = (low, mid, low);
            while i < mid && j < high {
                work.charge(COMPARISON)?;
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
        std::mem::swap(&mut from, &mut to);
        width *= 2;
    }
    Ok(from)
}

/// One charged binary search of `path` in a component-ordered index
/// (CI-A2-b, -c): at most `⌈log₂ n⌉ + 1` comparisons, one edge each.
pub(crate) fn charged_find<E>(
    tree: &Tree<'_>,
    order: &[u32],
    path: &str,
    work: &mut WorkScope<'_>,
) -> Result<Option<u32>, WorkFailure<E>> {
    let (mut low, mut high) = (0usize, order.len());
    while low < high {
        let mid = low + (high - low) / 2;
        work.charge(COMPARISON)?;
        match component_cmp(tree.row(order[mid]).path, path) {
            std::cmp::Ordering::Less => low = mid + 1,
            std::cmp::Ordering::Greater => high = mid,
            std::cmp::Ordering::Equal => return Ok(Some(order[mid])),
        }
    }
    Ok(None)
}

/// LD-CI-10: a file is `0500` if its authenticated mode has an execute bit,
/// else `0400`; a directory inside `tree/`, and `tree/` itself, `0500`.
pub(crate) fn installed_mode(row: &TreeRow<'_>) -> u32 {
    match row.kind {
        RowKind::File { .. } if row.mode & 0o111 != 0 => 0o500,
        RowKind::File { .. } => 0o400,
        RowKind::Dir | RowKind::Symlink { .. } => 0o500,
    }
}

// ---- The structural walk (V1, V2, and the retained tree's open) ----

/// What a walk checks: the staging modes and every byte (V1), the final
/// modes only (V2), or the final modes and every byte (the open).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum Phase {
    Staged,
    Final,
    Opened,
}

/// A walk's typed findings, which the installer and the reader each route.
#[derive(Debug)]
pub enum TreeFault {
    Absent {
        row: u32,
    },
    Extra {
        directory: Option<u32>,
    },
    Type {
        row: u32,
    },
    Mode {
        row: Option<u32>,
    },
    LinkTarget {
        row: u32,
    },
    Length {
        row: u32,
    },
    Digest {
        row: u32,
    },
    /// `generation.json` is not the owned expected record.
    Association,
    /// `pin.lock` is missing, or not a regular empty `0600` file.
    Pin,
    Io {
        call: &'static str,
        error: io::Error,
    },
}
type WalkFailure = WorkFailure<TreeFault>;

fn io_fault(call: &'static str) -> impl FnOnce(io::Error) -> WalkFailure {
    move |error| WorkFailure::Operation(TreeFault::Io { call, error })
}
fn open_fault(call: &'static str, row: u32, e: WorkFailure<TreeOpenError>) -> WalkFailure {
    match e {
        WorkFailure::Budget(b) => WorkFailure::Budget(b),
        WorkFailure::Operation(TreeOpenError::Absent) => {
            WorkFailure::Operation(TreeFault::Absent { row })
        }
        WorkFailure::Operation(TreeOpenError::NotRegular) => {
            WorkFailure::Operation(TreeFault::Type { row })
        }
        WorkFailure::Operation(TreeOpenError::Io(error)) => {
            WorkFailure::Operation(TreeFault::Io { call, error })
        }
        WorkFailure::Operation(TreeOpenError::Name | TreeOpenError::Unsupported) => {
            WorkFailure::Operation(TreeFault::Io {
                call,
                error: io::Error::new(
                    io::ErrorKind::Unsupported,
                    "component tree primitive refused",
                ),
            })
        }
    }
}

/// Enter one directory: `desc(len(name))`, charged before the no-follow open.
pub(crate) fn descend(
    parent: &RetainedDirectory,
    name: &str,
    row: Option<u32>,
    work: &mut WorkScope<'_>,
) -> Result<Level, WalkFailure> {
    work.charge(descend_cost(name.len()))?;
    let directory = parent
        .open_child_directory(OsStr::new(name))
        .map_err(|error| {
            WorkFailure::Operation(match row {
                Some(row) if error.kind() == io::ErrorKind::NotFound => TreeFault::Absent { row },
                Some(row) if ct::is_not_directory(&error) => TreeFault::Type { row },
                _ => TreeFault::Io {
                    call: "openat-directory",
                    error,
                },
            })
        })?;
    Ok(Level {
        directory,
        row,
        children: 0,
    })
}

/// A directory's listing, at its pop: its children plus `.`, `..` and the
/// end, charged before the listing; any entry beyond the children visited
/// is `Extra`. Every expected child was already found by its status read,
/// and names are unique, so an equal count means an equal set.
pub(crate) fn check_listing(level: &Level, work: &mut WorkScope<'_>) -> Result<(), WalkFailure> {
    check_listing_of(&level.directory, level.row, level.children, work)
}
pub(crate) fn check_listing_of(
    directory: &RetainedDirectory,
    row: Option<u32>,
    children: usize,
    work: &mut WorkScope<'_>,
) -> Result<(), WalkFailure> {
    work.charge(
        times(READ, children + 3).ok_or(WorkFailure::Budget(WorkBudgetError::Arithmetic))?,
    )?;
    let mut names = 0usize;
    let summary = directory.visit_entry_names::<()>(children + 2, 1024 * (children + 2), |name| {
        if name != b"." && name != b".." {
            names += 1;
        }
        Ok(())
    });
    let extra = || WorkFailure::Operation(TreeFault::Extra { directory: row });
    match summary {
        Ok(_) if names == children => Ok(()),
        Ok(_) | Err(opensip_platform::DirectoryVisitError::EntryLimit) => Err(extra()),
        Err(opensip_platform::DirectoryVisitError::NameByteLimit) => Err(extra()),
        Err(opensip_platform::DirectoryVisitError::Native(error)) => {
            Err(WorkFailure::Operation(TreeFault::Io {
                call: "readdir",
                error,
            }))
        }
        Err(_) => Err(WorkFailure::Operation(TreeFault::Io {
            call: "readdir",
            error: io::Error::new(io::ErrorKind::InvalidInput, "listing limits"),
        })),
    }
}

/// Read one open file through the shared buffer, at most `env(length)`
/// attempts, each charged first; its length and SHA-256 must be the row's.
/// `sink` sees each chunk (the retained tree's transfer).
pub(crate) fn read_verified(
    file: &TreeFile,
    row: u32,
    length: u64,
    sha256: [u8; 32],
    buffer: &mut [u8],
    work: &mut WorkScope<'_>,
    mut sink: impl FnMut(&[u8]),
) -> Result<(), WalkFailure> {
    let attempts = envelope(length);
    let mut digest = Some(opensip_identity::RawSha256::new());
    let mut total = 0u64;
    let mut made = 0u64;
    let mut reader = file.file();
    loop {
        if made == attempts {
            // The envelope is spent before the end was observed.
            return Err(WorkFailure::Operation(TreeFault::Length { row }));
        }
        work.charge(READ)?;
        made += 1;
        let n = reader.read(buffer).map_err(io_fault("read"))?;
        if n == 0 {
            break;
        }
        total = total.saturating_add(n as u64);
        if total > length {
            return Err(WorkFailure::Operation(TreeFault::Length { row }));
        }
        let d = digest
            .take()
            .ok_or(WorkFailure::Operation(TreeFault::Digest { row }))?;
        digest = Some(
            d.update(&buffer[..n])
                .map_err(|_| WorkFailure::Operation(TreeFault::Digest { row }))?,
        );
        sink(&buffer[..n]);
    }
    if total != length {
        return Err(WorkFailure::Operation(TreeFault::Length { row }));
    }
    let d = digest
        .take()
        .ok_or(WorkFailure::Operation(TreeFault::Digest { row }))?;
    if d.finish() != sha256 {
        return Err(WorkFailure::Operation(TreeFault::Digest { row }));
    }
    Ok(())
}

/// The structural walk over a component-ordered index from `tree/`'s handle
/// (CI-A1-c; LD-CIP-4): each directory is entered once, from its parent on
/// the current-branch stack, and listed at its pop; `tree/` is listed last.
/// No row is found by listing; every row is found by its own status read.
pub(crate) fn walk(
    root: &RetainedDirectory,
    tree: &Tree<'_>,
    order: &[u32],
    phase: Phase,
    buffer: &mut [u8],
    work: &mut WorkScope<'_>,
) -> Result<(), WalkFailure> {
    let mut stack: Vec<Level> = Vec::new();
    let mut root_children = 0usize;
    let staged = phase == Phase::Staged;
    for &index in order {
        let row = tree.row(index);
        let (parent, name) = split(row.path);
        pop_to(&mut stack, tree, parent, work, |level, work| {
            check_listing(&level, work)
        })?;
        let directory = match stack.last_mut() {
            Some(top) => {
                top.children += 1;
                &top.directory
            }
            None => {
                root_children += 1;
                root
            }
        };
        let status =
            ct::entry_status(directory, name, work).map_err(|e| open_fault("fstatat", index, e))?;
        match row.kind {
            RowKind::File { length, sha256 } => {
                if status.kind != EntryKind::File {
                    return Err(WorkFailure::Operation(TreeFault::Type { row: index }));
                }
                let mode = if staged { 0o600 } else { installed_mode(&row) };
                if status.mode != mode {
                    return Err(WorkFailure::Operation(TreeFault::Mode { row: Some(index) }));
                }
                if phase != Phase::Final {
                    let file = ct::open_regular_no_follow(directory, name, Access::ReadOnly, work)
                        .map_err(|e| open_fault("openat", index, e))?;
                    if file.mode() != mode {
                        return Err(WorkFailure::Operation(TreeFault::Mode { row: Some(index) }));
                    }
                    if file.length() != length {
                        return Err(WorkFailure::Operation(TreeFault::Length { row: index }));
                    }
                    read_verified(&file, index, length, sha256, buffer, work, |_| {})?;
                }
            }
            RowKind::Dir => {
                if status.kind != EntryKind::Directory {
                    return Err(WorkFailure::Operation(TreeFault::Type { row: index }));
                }
                let mode = if staged { 0o700 } else { installed_mode(&row) };
                if status.mode != mode {
                    return Err(WorkFailure::Operation(TreeFault::Mode { row: Some(index) }));
                }
                let level = descend(directory, name, Some(index), work)?;
                stack.push(level);
            }
            RowKind::Symlink { target } => {
                if status.kind != EntryKind::Symlink {
                    return Err(WorkFailure::Operation(TreeFault::Type { row: index }));
                }
                work.charge(owned_record(ct::LINK_BUFFER))?;
                let mut link = [0u8; ct::LINK_BUFFER];
                let n = ct::read_link(directory, name, &mut link, work)
                    .map_err(|e| open_fault("readlinkat", index, e))?;
                if &link[..n] != target.as_bytes() {
                    return Err(WorkFailure::Operation(TreeFault::LinkTarget { row: index }));
                }
            }
        }
    }
    while let Some(level) = stack.pop() {
        check_listing(&level, work)?;
    }
    check_listing_of(root, None, root_children, work)
}

/// Pop every level that is not `parent` or an ancestor of it, applying
/// `finish` to each popped level (a listing check, or finalization).
pub(crate) fn pop_to<E>(
    stack: &mut Vec<Level>,
    tree: &Tree<'_>,
    parent: &str,
    work: &mut WorkScope<'_>,
    mut finish: impl FnMut(Level, &mut WorkScope<'_>) -> Result<(), WorkFailure<E>>,
) -> Result<(), WorkFailure<E>> {
    while let Some(top) = stack.last() {
        let here = top.row.map_or("", |r| tree.row(r).path);
        if here == parent {
            break;
        }
        let Some(level) = stack.pop() else { break };
        finish(level, work)?;
    }
    Ok(())
}

// ---- The generation record (LAW item 5; LD-CIP-5) ----

/// The record's authenticated values, borrowed: the canonical JSON object
/// `{archiveDigest, archiveProfileId, catalogRelease: {envelopeDigest,
/// manifestDigest, stableId, version}, closureId, componentManifestDigest,
/// platform}`, keys in canonical order.
pub(crate) struct Record<'a> {
    pub(crate) archive_digest: &'a str,
    pub(crate) envelope_digest: &'a str,
    pub(crate) manifest_digest: &'a str,
    pub(crate) stable_id: &'a str,
    pub(crate) version: &'a str,
    pub(crate) closure_id: &'a str,
    pub(crate) component_manifest_digest: [u8; 64],
    pub(crate) platform: &'a str,
}

/// One string's canonical JSON length (the identity encoder's escapes).
fn string_len(s: &str) -> usize {
    2 + s
        .chars()
        .map(|c| match c {
            '"' | '\\' | '\u{8}' | '\u{c}' | '\n' | '\r' | '\t' => 2,
            '\0'..='\u{1f}' => 6,
            _ => c.len_utf8(),
        })
        .sum::<usize>()
}
fn push_string(out: &mut Vec<u8>, s: &str) {
    out.push(b'"');
    for c in s.chars() {
        match c {
            '"' => out.extend_from_slice(b"\\\""),
            '\\' => out.extend_from_slice(b"\\\\"),
            '\u{8}' => out.extend_from_slice(b"\\b"),
            '\u{c}' => out.extend_from_slice(b"\\f"),
            '\n' => out.extend_from_slice(b"\\n"),
            '\r' => out.extend_from_slice(b"\\r"),
            '\t' => out.extend_from_slice(b"\\t"),
            '\0'..='\u{1f}' => {
                const HEX: &[u8] = b"0123456789abcdef";
                let b = c as u8;
                out.extend_from_slice(&[
                    b'\\',
                    b'u',
                    b'0',
                    b'0',
                    HEX[(b >> 4) as usize],
                    HEX[(b & 15) as usize],
                ]);
            }
            _ => out.extend_from_slice(c.encode_utf8(&mut [0; 4]).as_bytes()),
        }
    }
    out.push(b'"');
}
impl Record<'_> {
    fn fields(&self) -> [(&'static str, Field<'_>); 7] {
        [
            ("archiveDigest", Field::Text(self.archive_digest)),
            ("archiveProfileId", Field::Text(ap::PROFILE_ID)),
            ("catalogRelease", Field::Release),
            ("closureId", Field::Text(self.closure_id)),
            (
                "componentManifestDigest",
                Field::Hex(&self.component_manifest_digest),
            ),
            ("platform", Field::Text(self.platform)),
            ("", Field::End),
        ]
    }
    fn release(&self) -> [(&'static str, &str); 4] {
        [
            ("envelopeDigest", self.envelope_digest),
            ("manifestDigest", self.manifest_digest),
            ("stableId", self.stable_id),
            ("version", self.version),
        ]
    }
    /// `R`, the exact canonical length, computed before anything is
    /// allocated.
    pub(crate) fn length(&self) -> usize {
        let mut len = 2; // { }
        let mut first = true;
        for (key, field) in self.fields() {
            let value = match field {
                Field::End => continue,
                Field::Text(s) => string_len(s),
                Field::Hex(h) => 2 + h.len(),
                Field::Release => {
                    2 + self
                        .release()
                        .iter()
                        .map(|(k, v)| string_len(k) + 1 + string_len(v))
                        .sum::<usize>()
                        + 3
                }
            };
            len += if first { 0 } else { 1 } + string_len(key) + 1 + value;
            first = false;
        }
        len
    }
    /// The record's bytes, hand-encoded into one buffer reserved at exactly
    /// `R` (LD-CIP-5); the caller charges `owned(R)` first.
    pub(crate) fn encode(&self) -> Vec<u8> {
        let mut out = Vec::with_capacity(self.length());
        out.push(b'{');
        let mut first = true;
        for (key, field) in self.fields() {
            if let Field::End = field {
                continue;
            }
            if !first {
                out.push(b',');
            }
            first = false;
            push_string(&mut out, key);
            out.push(b':');
            match field {
                Field::Text(s) => push_string(&mut out, s),
                Field::Hex(h) => {
                    out.push(b'"');
                    out.extend_from_slice(h);
                    out.push(b'"');
                }
                Field::Release => {
                    out.push(b'{');
                    for (i, (k, v)) in self.release().iter().enumerate() {
                        if i > 0 {
                            out.push(b',');
                        }
                        push_string(&mut out, k);
                        out.push(b':');
                        push_string(&mut out, v);
                    }
                    out.push(b'}');
                }
                Field::End => {}
            }
        }
        out.push(b'}');
        out
    }
}
enum Field<'a> {
    Text(&'a str),
    Hex(&'a [u8; 64]),
    Release,
    End,
}
pub(crate) fn hex64(bytes: &[u8; 32]) -> [u8; 64] {
    const HEX: &[u8] = b"0123456789abcdef";
    let mut out = [0u8; 64];
    for (i, b) in bytes.iter().enumerate() {
        out[2 * i] = HEX[(b >> 4) as usize];
        out[2 * i + 1] = HEX[(b & 15) as usize];
    }
    out
}

// ---- The evidence (LAW item 2) ----

/// One release's installation evidence, borrowed from C2a-1's bridge and
/// candidate: the selected tree, the artifact row's values and the record.
pub(crate) struct Evidence<'a> {
    pub(crate) tree: Tree<'a>,
    pub(crate) archive_digest: &'a str,
    pub(crate) record: Record<'a>,
    /// The generation's directory name: `closure2:`'s 64 hex digits.
    pub(crate) name: &'a str,
}

/// S8's closed four-row table: the host's `{os, arch}` to RC's artifact
/// token (LD-CI-2), used only to select the artifact.
pub(crate) fn platform_token(platform: SelectedPlatform<'_>) -> Option<&'static str> {
    match (platform.os, platform.arch) {
        ("macos", "arm64") => Some("macos-arm64"),
        ("macos", "x86_64") => Some("macos-x86_64"),
        ("linux", "arm64") => Some("linux-arm64"),
        ("linux", "x86_64") => Some("linux-x86_64"),
        _ => None,
    }
}

/// Item 8's admission refusals (request-rejected 2,
/// `EXTENSION.ADMISSION_REJECTED`).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum AdmissionRefusal {
    /// The host's platform has no S8 row, or no artifact of its token.
    PlatformUnsupported,
    /// `archiveProfileId` is not `opensip-archive-profile.1`.
    Profile,
    /// `archiveDigest` and `sha256` differ (`artifact-digest-split`).
    ArtifactDigestSplit,
    /// A profile capacity (`archive-capacity`), before any read.
    Capacity(ap::Capacity),
    /// The admission bound exceeds the ledger's allowance, or overflows
    /// (`install-budget`), before acquisition.
    InstallBudget,
    /// A profile admission check (item 3), including the length.
    Archive(ArchiveRefusal),
    /// The archive digest is not the signed `archiveDigest`.
    ArchiveDigest,
    /// The archive's identity changed during the read (`archive-changed`).
    ArchiveChanged,
    /// The read-attempt envelope was spent (`archive-read-attempts`).
    ArchiveReadAttempts,
    /// The archive path is not a regular file, or absent.
    ArchiveNotRegular,
    /// The evidence and candidate disagree (a caller's bug).
    Evidence,
}

pub(crate) fn evidence<'a>(
    component: &AuthenticatedComponent<'a>,
    candidate: &'a ClosureCandidate<'_>,
    platform: SelectedPlatform<'_>,
) -> Result<Evidence<'a>, AdmissionRefusal> {
    let token = platform_token(platform).ok_or(AdmissionRefusal::PlatformUnsupported)?;
    let release = component.release();
    let mut artifact = None;
    for a in items(member(release, "artifacts").ok_or(AdmissionRefusal::Evidence)?)
        .ok_or(AdmissionRefusal::Evidence)?
    {
        if member(a, "platform").and_then(text) == Some(token) {
            artifact = Some(a);
        }
    }
    let artifact = artifact.ok_or(AdmissionRefusal::PlatformUnsupported)?;
    let field = |v: &'a V, key: &str| {
        member(v, key)
            .and_then(text)
            .ok_or(AdmissionRefusal::Evidence)
    };
    if field(artifact, "archiveProfileId")? != ap::PROFILE_ID {
        return Err(AdmissionRefusal::Profile);
    }
    let archive_digest = field(artifact, "archiveDigest")?;
    if archive_digest != field(artifact, "sha256")? {
        return Err(AdmissionRefusal::ArtifactDigestSplit);
    }
    let tree = Tree::of(component.manifest(), platform).ok_or(AdmissionRefusal::Evidence)?;
    let name = candidate
        .closure()
        .strip_prefix("closure2:")
        .filter(|h| {
            h.len() == NAME_BYTES
                && h.bytes()
                    .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
        })
        .ok_or(AdmissionRefusal::Evidence)?;
    let record = Record {
        archive_digest,
        envelope_digest: field(release, "envelopeDigest")?,
        manifest_digest: field(release, "manifestDigest")?,
        stable_id: field(release, "stableId")?,
        version: field(release, "version")?,
        closure_id: candidate.closure(),
        component_manifest_digest: hex64(&candidate.manifest_digest()),
        platform: token,
    };
    if record.manifest_digest.as_bytes() != &record.component_manifest_digest[..] {
        return Err(AdmissionRefusal::Evidence);
    }
    Ok(Evidence {
        tree,
        archive_digest,
        record,
        name,
    })
}

// ---- The admission bound (LAW item 4's `B_install`, with CI-A1 and CI-A2) ----

/// `B_install` for a tree with archive length `length`, record length
/// `record` and archive path length `path`. Every sum and product is
/// checked; `None` is an overflow, refused `install-budget`.
pub(crate) fn install_bound(
    tree: &Tree<'_>,
    length: u64,
    record: usize,
    path: usize,
) -> Option<WorkCost> {
    let st = ct::status_read_cost();
    let fopen = ct::open_regular_no_follow_cost();
    let (n, d) = (tree.n, tree.dirs);
    let sorts = sort_comparisons(n)?;
    let mut b = Bound::default()
        // Step 1: the existence check, the store's custody, the archive's
        // open with its path record, and the identity samples.
        .add(owned_record(NAME_BYTES + 1))?
        .add(st)?
        .add(custody_cost())?
        .add(fopen)?
        .add(owned_record(path))?
        .add_times(st, 2)?
        // Step 2: the stage, its custody, `tree/`, the buffer, the read
        // attempts, the member order (CI-A2-a), and each member.
        .add(private_directory_stage_cost())?
        .add(opensip_platform::append_owner_zero_allow_cost())?
        .add(custody_cost())?
        .add(create_exclusive_directory_cost(TREE))?
        .add(buffer_cost())?
        .add_times(READ, to_usize(envelope(length))?)?
        .add_times(index_buffer_cost(n)?, 2)?
        .add_times(COMPARISON, sorts)?
        // The Blobs' association, one comparison per file row (CI-A2-a).
        .add_times(COMPARISON, tree.files)?
        // Step 3 (V1) and step 4 share CI-A1-b's index: computed once.
        .add_times(index_buffer_cost(n)?, 2)?
        .add_times(COMPARISON, sorts)?;
    for row in tree.rows() {
        let (_, name) = split(row.path);
        // Step 2: the member's parent chain from `tree/`.
        let mut rest = row.path;
        for _ in 1..depth(row.path) {
            let (segment, tail) = rest.split_once('/')?;
            b = b.add(descend_cost(segment.len()))?;
            rest = tail;
        }
        match row.kind {
            RowKind::File { length, .. } => {
                b = b
                    // Step 2: the exclusive create and the chunk writes.
                    .add(create_exclusive_regular_cost(name))?
                    .add_times(NATIVE_CALL, to_usize(length.div_ceil(READ_CHUNK as u64))?)?
                    // Step 3 (V1): the open and the read attempts.
                    .add(fopen)?
                    .add_times(READ, to_usize(envelope(length))?)?
                    // Step 4.1: the open, `fchmod` and the barrier.
                    .add(fopen)?
                    .add_times(NATIVE_CALL, 2)?;
            }
            RowKind::Dir => {
                b = b
                    // Step 2: the exclusive create.
                    .add(create_exclusive_directory_cost(name))?
                    // Steps 3, 4 and 5: one descent each.
                    .add_times(descend_cost(name.len()), 3)?
                    // Step 4.4: `fchmod` and the barrier.
                    .add(NATIVE_CALL)?
                    .add(directory_barrier_cost())?;
            }
            RowKind::Symlink { target } => {
                b = b
                    // Step 2: `symlinkat` and its target's record.
                    .add(NATIVE_CALL)?
                    .add(owned_record(target.len()))?
                    // Steps 3 and 5: `readlinkat` and its buffer.
                    .add_times(NATIVE_CALL, 2)?
                    .add_times(owned_record(ct::LINK_BUFFER), 2)?;
            }
        }
    }
    let listing = n.checked_add(3usize.checked_mul(d.checked_add(1)?)?)?;
    b = b
        // Step 3 (V1): into `tree/`, the listings and the status reads.
        .add(descend_cost(TREE.len()))?
        .add_times(READ, listing)?
        .add_times(st, n)?
        // Step 4: into `tree/`; `tree/`'s `fchmod` and barrier (4.4).
        .add(descend_cost(TREE.len()))?
        .add(NATIVE_CALL)?
        .add(directory_barrier_cost())?
        // 4.2: `generation.json`.
        .add(create_exclusive_regular_cost(RECORD))?
        .add(owned_record(record))?
        .add_times(NATIVE_CALL, record.div_ceil(READ_CHUNK))?
        .add_times(NATIVE_CALL, 2)?
        // 4.3: `pin.lock`, created and barriered.
        .add(create_exclusive_regular_cost(PIN))?
        .add(NATIVE_CALL)?
        // 4.5: the stage.
        .add(directory_barrier_cost())?
        // Step 5 (V2): into `tree/`, `tree/`'s status (CI-A2-d), the
        // listings, the status reads, the record and `pin.lock`.
        .add(descend_cost(TREE.len()))?
        .add(st)?
        .add_times(READ, listing)?
        .add_times(st, n)?
        .add(fopen)?
        .add_times(READ, to_usize(envelope(record as u64))?)?
        .add(fopen)?
        // Step 6: the reserved suffix.
        .add(exclusive_publication_cost())?
        .add(directory_barrier_cost())?;
    Some(b.0)
}

// ---- The store (LAW item 5) ----

/// `<installRoot>/components/`, retained, with the invoking user its
/// custody is judged against. Only its owner opens it: the host, from its
/// admitted installation root, or a fixture.
pub struct ComponentStore {
    pub(crate) directory: RetainedDirectory,
    pub(crate) invoking_uid: u32,
}
impl ComponentStore {
    /// The store, opened no-follow from its admitted installation root,
    /// whose custody is the host's. The store's own custody is checked by
    /// every use (items 4 and 6).
    pub fn open_in(install_root: &RetainedDirectory, invoking_uid: u32) -> io::Result<Self> {
        let directory =
            install_root.open_child_directory(OsStr::new(crate::locations::COMPONENT_STORE))?;
        Ok(Self {
            directory,
            invoking_uid,
        })
    }
    /// A fixture store over `directory` (LAW item 6's fixture path; plan r3
    /// LD-CIP-3), only under the joint fixture predicate.
    #[cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))]
    pub fn fixture(directory: RetainedDirectory, invoking_uid: u32) -> Self {
        Self {
            directory,
            invoking_uid,
        }
    }
    /// `cust`, at its actual charge.
    pub(crate) fn custody<E>(
        &self,
        directory: &File,
        work: &mut WorkScope<'_>,
    ) -> Result<Result<(), CustodyDirectoryRefusal>, WorkFailure<E>> {
        match admit_custody_directory(directory, self.invoking_uid, work) {
            Ok(()) => Ok(Ok(())),
            Err(WorkFailure::Budget(b)) => Err(WorkFailure::Budget(b)),
            Err(WorkFailure::Operation(refusal)) => Ok(Err(refusal)),
        }
    }
}

// ---- The installer ----

/// Test seams: named points of the transaction where a control injects a
/// failure or tampers with the stage (CI-T7, CI-T19, CI-T24, CI-T25), and a
/// cap on one archive read (CI-T6). Compiled only into this crate's tests.
#[cfg(test)]
pub(crate) mod seams {
    use std::cell::RefCell;
    use std::io;
    type Hook = Box<dyn FnMut(&'static str) -> io::Result<()>>;
    thread_local! {
        pub(crate) static HOOK: RefCell<Option<Hook>> = const { RefCell::new(None) };
        pub(crate) static READ_CAP: RefCell<Option<usize>> = const { RefCell::new(None) };
        pub(crate) static WRITES: RefCell<usize> = const { RefCell::new(0) };
    }
    pub(crate) fn at(step: &'static str) -> io::Result<()> {
        HOOK.with(|h| h.borrow_mut().as_mut().map_or(Ok(()), |f| f(step)))
    }
    pub(crate) fn room(room: usize) -> usize {
        READ_CAP.with(|c| c.borrow().map_or(room, |cap| room.min(cap)))
    }
}
#[cfg(test)]
fn seam(step: &'static str) -> Result<(), Failure> {
    seams::at(step).map_err(install_io("seam"))
}
#[cfg(not(test))]
fn seam(_: &'static str) -> Result<(), Failure> {
    Ok(())
}
#[cfg(test)]
fn read_room(room: usize) -> usize {
    seams::room(room)
}
#[cfg(not(test))]
fn read_room(room: usize) -> usize {
    room
}

/// Item 8's I/O failures (operational-failed 4, `EXTENSION.INSTALL_IO_FAILED`).
#[derive(Debug)]
pub enum InstallIo {
    /// A native call failed while staging, verifying or making durable.
    Call {
        call: &'static str,
        error: io::Error,
    },
    /// The store or the stage failed custody.
    Custody(CustodyDirectoryRefusal),
    /// The staged tree disagreed with what was written (V1 or V2).
    Verify(TreeFault),
    /// The exclusive rename's class: `LostRace` or `NotPerformed` ended the
    /// act with nothing published; `Indeterminate` is publication uncertain.
    Publication(DirectoryRenameClass),
    /// The funded parent barrier failed after the rename: publication
    /// uncertain. Nothing is retried, replaced or rolled back.
    Uncertain(io::Error),
}

/// Item 8's installation outcomes.
#[derive(Debug)]
pub enum InstallFailure {
    Admission(AdmissionRefusal),
    Io(InstallIo),
    /// Work exhausted during installation: law 468's route
    /// (`SYSTEM.OUTCOME.ILLEGAL_STATE`, detail `WORK.BUDGET_EXHAUSTED`).
    Budget(WorkBudgetError),
    /// An existing generation failed item 6's verification on re-install
    /// (`HOST.IO_FAILURE`, `DELIVERY.CLOSURE_BYTES_CORRUPT`). Nothing is
    /// replaced.
    Corrupt(TreeReadFailure),
}

/// A completed installation.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Installed {
    /// The generation was staged, verified and published.
    Published,
    /// The generation already existed and verified (LD-CI-6): nothing was
    /// staged.
    AlreadyInstalled,
}

type Failure = WorkFailure<InstallFailure>;
fn admission(r: AdmissionRefusal) -> Failure {
    WorkFailure::Operation(InstallFailure::Admission(r))
}
fn install_io(call: &'static str) -> impl FnOnce(io::Error) -> Failure {
    move |error| WorkFailure::Operation(InstallFailure::Io(InstallIo::Call { call, error }))
}
fn walk_failure(e: WalkFailure) -> Failure {
    match e {
        WorkFailure::Budget(b) => WorkFailure::Budget(b),
        WorkFailure::Operation(fault) => {
            WorkFailure::Operation(InstallFailure::Io(InstallIo::Verify(fault)))
        }
    }
}
/// A primitive's error, as the I/O route's `io::Error`.
trait ToIo {
    fn to_io(self) -> io::Error;
}
impl ToIo for io::Error {
    fn to_io(self) -> io::Error {
        self
    }
}
impl ToIo for TreeOpenError {
    fn to_io(self) -> io::Error {
        match self {
            TreeOpenError::Io(e) => e,
            TreeOpenError::Absent => io::Error::new(io::ErrorKind::NotFound, "absent"),
            TreeOpenError::NotRegular => {
                io::Error::new(io::ErrorKind::InvalidData, "not a regular file")
            }
            TreeOpenError::Name => io::Error::new(io::ErrorKind::InvalidInput, "not one component"),
            TreeOpenError::Unsupported => {
                io::Error::new(io::ErrorKind::Unsupported, "unsupported target")
            }
        }
    }
}
impl ToIo for ExclusiveDirectoryError {
    fn to_io(self) -> io::Error {
        match self {
            ExclusiveDirectoryError::Name(e)
            | ExclusiveDirectoryError::Create(e)
            | ExclusiveDirectoryError::AfterCreate(e) => e,
            ExclusiveDirectoryError::NotFresh => {
                io::Error::new(io::ErrorKind::InvalidData, "directory not fresh")
            }
        }
    }
}
impl ToIo for ExclusiveRegularError {
    fn to_io(self) -> io::Error {
        match self {
            ExclusiveRegularError::Name(e)
            | ExclusiveRegularError::Create(e)
            | ExclusiveRegularError::AfterCreate(e) => e,
        }
    }
}
impl ToIo for ct::ChunkWriteError {
    fn to_io(self) -> io::Error {
        match self {
            ct::ChunkWriteError::Io(e) => e,
            ct::ChunkWriteError::Short { .. } => {
                io::Error::new(io::ErrorKind::WriteZero, "short write")
            }
        }
    }
}
fn io_of<E: ToIo>(call: &'static str) -> impl FnOnce(WorkFailure<E>) -> Failure {
    move |e| match e {
        WorkFailure::Budget(b) => WorkFailure::Budget(b),
        WorkFailure::Operation(e) => WorkFailure::Operation(InstallFailure::Io(InstallIo::Call {
            call,
            error: e.to_io(),
        })),
    }
}
fn exists() -> io::Error {
    io::Error::new(
        io::ErrorKind::AlreadyExists,
        "an exclusive create found an entry",
    )
}

/// The re-install path's bound: step 1's existence check and the store's
/// custody, then item 6's `B_open` (LD-CI-6).
fn reinstall_bound(tree: &Tree<'_>, record: usize) -> Option<WorkCost> {
    Bound::default()
        .add(owned_record(NAME_BYTES + 1))?
        .add(ct::status_read_cost())?
        .add(retained_tree::open_bound(tree, record)?)
        .map(|b| b.0)
}
/// The admission bound reserved before acquisition: `B_install`, or the
/// re-install path's if that is larger in any component (LD-CI2-3).
pub(crate) fn admission_bound(
    tree: &Tree<'_>,
    length: u64,
    record: usize,
    path: usize,
) -> Option<WorkCost> {
    let a = install_bound(tree, length, record, path)?;
    let b = reinstall_bound(tree, record)?;
    Some(WorkCost {
        objects: a.objects.max(b.objects),
        edges: a.edges.max(b.edges),
        bytes: a.bytes.max(b.bytes),
    })
}

/// Install one admitted release for the host's platform from the archive at
/// `archive` (LAW item 4). The caller holds the lifecycle fence for the whole
/// act (CI-4's command acquires it), and supplies the ledger: the interim
/// policy is `WorkLedger::snapshot_profile()` (X-CI-1).
///
/// `component` and `candidate` are C2a-1's: the ordinary reader's verified
/// component and its unadmitted candidate for `platform`.
pub fn install(
    store: &ComponentStore,
    component: &AuthenticatedComponent<'_>,
    candidate: &ClosureCandidate<'_>,
    platform: SelectedPlatform<'_>,
    archive: &Path,
    work: &mut WorkScope<'_>,
) -> Result<Installed, InstallFailure> {
    let evidence = evidence(component, candidate, platform).map_err(InstallFailure::Admission)?;
    let tree = &evidence.tree;
    // Capacities and `archiveLength`, before any read (item 3).
    let length = archive_length(tree)?;
    let record = evidence.record.length();
    let path_len = archive.as_os_str().len();
    let bound = admission_bound(tree, length, record, path_len)
        .ok_or(InstallFailure::Admission(AdmissionRefusal::InstallBudget))?;
    // The admission bound, reserved before acquisition (LD-CI2-3): an excess
    // is `install-budget`; every later charge draws from this reservation.
    let reserved = work.effect(WorkCost::default(), bound, |post| {
        post.prepaid(bound, |work| {
            transaction(store, &evidence, candidate, archive, length, work)
        })
    });
    match reserved {
        Ok(outcome) => Ok(outcome),
        Err(WorkFailure::Operation(failure)) => Err(failure),
        Err(WorkFailure::Budget(b)) if is_reservation(&b) => {
            Err(InstallFailure::Admission(AdmissionRefusal::InstallBudget))
        }
        Err(WorkFailure::Budget(b)) => Err(InstallFailure::Budget(b)),
    }
}

/// The reservation's own refusal is one of the limit dimensions; a charge
/// beyond the prepaid credit inside it is `ReservedPostcheck` (law 468's
/// route), and so is any later exhaustion.
fn is_reservation(b: &WorkBudgetError) -> bool {
    matches!(
        b,
        WorkBudgetError::Objects | WorkBudgetError::Edges | WorkBudgetError::Bytes
    )
}

/// `archiveLength`, with every capacity checked (CI-1), before any read.
/// The member order's rows are not needed: length and capacities do not
/// depend on order, so manifest order with a sortedness-free check suffices.
fn archive_length(tree: &Tree<'_>) -> Result<u64, InstallFailure> {
    let mut length = 1024u64;
    for row in tree.rows() {
        if row.path.len() > ap::MAX_PATH_BYTES {
            return Err(InstallFailure::Admission(AdmissionRefusal::Capacity(
                ap::Capacity::PathExceedsUstarName,
            )));
        }
        if row.mode > ap::MAX_MODE {
            return Err(InstallFailure::Admission(AdmissionRefusal::Capacity(
                ap::Capacity::ModeExceedsUstarField,
            )));
        }
        let body = match row.kind {
            RowKind::File { length, .. } if length > ap::MAX_SIZE => {
                return Err(InstallFailure::Admission(AdmissionRefusal::Capacity(
                    ap::Capacity::SizeExceedsUstarField,
                )));
            }
            RowKind::File { length, .. } => length.div_ceil(512) * 512,
            RowKind::Symlink { target } if target.len() > ap::MAX_LINK_TARGET_BYTES => {
                return Err(InstallFailure::Admission(AdmissionRefusal::Capacity(
                    ap::Capacity::LinkTargetExceedsUstarLinkname,
                )));
            }
            _ => 0,
        };
        length = length
            .checked_add(512)
            .and_then(|l| l.checked_add(body))
            .ok_or(InstallFailure::Admission(AdmissionRefusal::InstallBudget))?;
    }
    Ok(length)
}

fn transaction(
    store: &ComponentStore,
    evidence: &Evidence<'_>,
    candidate: &ClosureCandidate<'_>,
    archive: &Path,
    length: u64,
    work: &mut WorkScope<'_>,
) -> Result<Installed, Failure> {
    let tree = &evidence.tree;
    // Step 1: does `<closure2-hex>` exist?
    work.charge(owned_record(NAME_BYTES + 1))?;
    match ct::entry_status(&store.directory, evidence.name, work) {
        Ok(_) => {
            // LD-CI-6: verify the existing generation; never replace it.
            return match retained_tree::open_with(
                store,
                evidence,
                candidate,
                PinRequest::UnderFence,
                work,
            ) {
                Ok(tree) => {
                    drop(tree);
                    Ok(Installed::AlreadyInstalled)
                }
                Err(TreeReadFailure::Budget(b)) => Err(WorkFailure::Budget(b)),
                Err(failure) => Err(WorkFailure::Operation(InstallFailure::Corrupt(failure))),
            };
        }
        Err(WorkFailure::Operation(TreeOpenError::Absent)) => {}
        Err(WorkFailure::Budget(b)) => return Err(WorkFailure::Budget(b)),
        Err(WorkFailure::Operation(e)) => {
            return Err(io_of::<TreeOpenError>("fstatat")(WorkFailure::Operation(e)));
        }
    }
    if let Err(refusal) = store.custody::<InstallFailure>(store.directory.as_file(), work)? {
        return Err(WorkFailure::Operation(InstallFailure::Io(
            InstallIo::Custody(refusal),
        )));
    }
    // The archive (P-5): the path's record, the open, and its first sample.
    work.charge(owned_record(archive.as_os_str().len()))?;
    let file = match ct::open_archive(archive, work) {
        Ok(file) => file,
        Err(WorkFailure::Budget(b)) => return Err(WorkFailure::Budget(b)),
        Err(WorkFailure::Operation(
            TreeOpenError::Absent | TreeOpenError::NotRegular | TreeOpenError::Name,
        )) => {
            return Err(admission(AdmissionRefusal::ArchiveNotRegular));
        }
        Err(WorkFailure::Operation(e)) => {
            return Err(io_of::<TreeOpenError>("open-archive")(
                WorkFailure::Operation(e),
            ));
        }
    };
    let before = ct::sample_identity(&file, work).map_err(io_of::<io::Error>("fstat"))?;
    // The length, judged before any byte is read (item 3; CI-T2).
    if before.size != length {
        return Err(admission(AdmissionRefusal::Archive(
            ArchiveRefusal::Length {
                expected: length,
                observed: before.size,
            },
        )));
    }
    // Step 2: the stage, directly in the store, and its custody.
    let stage = store
        .directory
        .create_private_directory_stage_accounted(work)
        .map_err(io_of::<io::Error>("stage"))?;
    // FS creates the stage with no ACL; the custody rule requires the
    // zero-rights owner allow every private directory carries (CI-A2-g).
    opensip_platform::append_owner_zero_allow_accounted(stage.directory().as_file(), work)
        .map_err(io_of::<io::Error>("acl-append"))?;
    if let Err(refusal) = store.custody::<InstallFailure>(stage.directory().as_file(), work)? {
        return Err(WorkFailure::Operation(InstallFailure::Io(
            InstallIo::Custody(refusal),
        )));
    }
    let root = match stage
        .directory()
        .create_exclusive_directory_accounted(TREE, work)
    {
        Ok(ExclusiveDirectoryOutcome::Created(root)) => root,
        Ok(ExclusiveDirectoryOutcome::EntryExists) => {
            return Err(install_io("mkdirat")(exists()));
        }
        Err(e) => return Err(io_of::<ExclusiveDirectoryError>("mkdirat")(e)),
    };
    seam("staged")?;
    work.charge(buffer_cost())?;
    let mut buffer = vec![0u8; READ_CHUNK];
    let member_order = charged_sort::<InstallFailure>(tree.n, work, |a, b| {
        byte_less(tree.row(a).path, tree.row(b).path)
    })?;
    associate(tree, &member_order, candidate, work)?;
    stream(
        &file,
        &root,
        tree,
        &member_order,
        length,
        evidence.archive_digest,
        &mut buffer,
        work,
    )?;
    drop(member_order);
    seam("streamed")?;
    let after = ct::sample_identity(&file, work).map_err(io_of::<io::Error>("fstat"))?;
    if after != before {
        return Err(admission(AdmissionRefusal::ArchiveChanged));
    }
    drop(root);
    // Step 3 (V1), on CI-A1-b's index, which step 4 and V2 reuse.
    let order = charged_sort::<InstallFailure>(tree.n, work, |a, b| {
        component_cmp(tree.row(a).path, tree.row(b).path).is_lt()
    })?;
    let root = descend(stage.directory(), TREE, None, work).map_err(walk_failure)?;
    walk(
        &root.directory,
        tree,
        &order,
        Phase::Staged,
        &mut buffer,
        work,
    )
    .map_err(walk_failure)?;
    drop(root);
    seam("verified")?;
    // Step 4: finalize, in the branch-local post-order.
    finalize(stage.directory(), tree, &order, work)?;
    let bytes = record_file(stage.directory(), &evidence.record, work)?;
    pin_file(stage.directory(), work)?;
    stage
        .directory()
        .confirm_directory_barrier_accounted(work)
        .map_err(io_of::<io::Error>("barrier-stage"))?;
    seam("finalized")?;
    // Step 5 (V2): the final prerequisites.
    let root = descend(stage.directory(), TREE, None, work).map_err(walk_failure)?;
    tree_root_mode(stage.directory(), work).map_err(walk_failure)?;
    walk(
        &root.directory,
        tree,
        &order,
        Phase::Final,
        &mut buffer,
        work,
    )
    .map_err(walk_failure)?;
    drop(root);
    check_record(stage.directory(), &bytes, &mut buffer, work).map_err(walk_failure)?;
    check_pin(stage.directory(), work).map_err(walk_failure)?;
    drop(order);
    seam("prerequisites")?;
    // Step 6: publish, funded.
    let name = OsStr::new(evidence.name);
    let postchecks = exclusive_publication_cost()
        .checked_add(directory_barrier_cost())
        .ok_or(WorkFailure::Budget(WorkBudgetError::Arithmetic))?;
    work.effect(WorkCost::default(), postchecks, |post| {
        let publication = match stage.publish_exclusive_reserved(name, post) {
            Ok(publication) => publication,
            Err(WorkFailure::Budget(b)) => return Err(WorkFailure::Budget(b)),
            Err(WorkFailure::Operation(failure)) => {
                return Err(WorkFailure::Operation(InstallFailure::Io(
                    InstallIo::Publication(failure.class()),
                )));
            }
        };
        seam("renamed")?;
        match publication
            .parent_directory()
            .confirm_directory_barrier_reserved(post)
        {
            Ok(_) => Ok(()),
            Err(WorkFailure::Budget(b)) => Err(WorkFailure::Budget(b)),
            Err(WorkFailure::Operation(error)) => Err(WorkFailure::Operation(InstallFailure::Io(
                InstallIo::Uncertain(error),
            ))),
        }
    })?;
    Ok(Installed::Published)
}

/// P-1, once per chunk. The controls count the calls (CI-T22).
fn chunk_write(
    file: &File,
    offset: u64,
    bytes: &[u8],
    work: &mut WorkScope<'_>,
) -> Result<(), Failure> {
    #[cfg(test)]
    seams::WRITES.with(|w| *w.borrow_mut() += 1);
    ct::write_chunk(file, offset, bytes, work).map_err(io_of::<ct::ChunkWriteError>("pwrite"))
}

/// Step 2: C2a-1's Blobs are exactly the file rows projected (LAW item 6's
/// association, at installation; CI-A2-a): both are in path-byte order, so
/// one pass compares each file row with the next Blob, one charged
/// comparison each. A candidate of another platform or release refuses.
fn associate(
    tree: &Tree<'_>,
    member_order: &[u32],
    candidate: &ClosureCandidate<'_>,
    work: &mut WorkScope<'_>,
) -> Result<(), Failure> {
    let mut blobs = candidate.blobs();
    for &index in member_order {
        let row = tree.row(index);
        let RowKind::File { length, sha256 } = row.kind else {
            continue;
        };
        work.charge(COMPARISON)?;
        let blob = blobs.next().ok_or(admission(AdmissionRefusal::Evidence))?;
        if blob.path() != row.path
            || blob.bytes() != length
            || blob.sha256().as_bytes() != &hex64(&sha256)[..]
        {
            return Err(admission(AdmissionRefusal::Evidence));
        }
    }
    if blobs.next().is_some() {
        return Err(admission(AdmissionRefusal::Evidence));
    }
    Ok(())
}

/// Create one exclusive regular file in `directory` (`mkf`).
fn create_file(
    directory: &RetainedDirectory,
    name: &str,
    work: &mut WorkScope<'_>,
) -> Result<File, Failure> {
    match directory.create_exclusive_regular_accounted(name, work) {
        Ok(ExclusiveRegularOutcome::Created(file)) => Ok(file),
        Ok(ExclusiveRegularOutcome::EntryExists) => Err(install_io("openat-create")(exists())),
        Err(e) => Err(io_of::<ExclusiveRegularError>("openat-create")(e)),
    }
}

/// The member being written: its file, its length, what is written, and
/// where its unwritten chunk's bytes begin in the buffer.
struct Writing {
    file: File,
    length: u64,
    written: u64,
}

/// Step 2: stream the archive through CI-1's codec into `tree/`, each member
/// created in its parent, reached by no-follow descent along its parent
/// chain (dropped after the member). File bodies are written in chunks at
/// 64 KiB file offsets, one P-1 attempt each: a chunk split across two
/// archive reads is kept at the buffer's start until the next read
/// completes it. At most `env(L)` read attempts and `L + 1` bytes are read.
#[allow(clippy::too_many_arguments)]
fn stream(
    archive: &TreeFile,
    root: &RetainedDirectory,
    tree: &Tree<'_>,
    member_order: &[u32],
    length: u64,
    archive_digest: &str,
    buffer: &mut [u8],
    work: &mut WorkScope<'_>,
) -> Result<(), Failure> {
    let rows = Ordered {
        tree,
        order: member_order,
    };
    let plan = ArchivePlan::new(&rows).map_err(|e| admission(capacity_or_archive(e)))?;
    plan.check_length(length)
        .map_err(|e| admission(AdmissionRefusal::Archive(e)))?;
    let mut verifier = Some(plan.verifier());
    let attempts = envelope(length);
    let limit = plan.read_limit();
    let (mut made, mut read) = (0u64, 0u64);
    // Valid data is `buffer[..end]`; `pending` bytes at its start belong to
    // the current file's unwritten chunk.
    let (mut end, mut pending) = (0usize, 0usize);
    let mut parent_chain: Vec<RetainedDirectory> = Vec::new();
    let mut writing: Option<Writing> = None;
    loop {
        // One read attempt into the free tail, charged first.
        if made == attempts {
            return Err(admission(AdmissionRefusal::ArchiveReadAttempts));
        }
        let room = read_room((READ_CHUNK - end).min(to_usize(limit - read).unwrap_or(READ_CHUNK)));
        work.charge(READ)?;
        made += 1;
        let n = (&mut archive.file())
            .read(&mut buffer[end..end + room])
            .map_err(install_io("read"))?;
        read += n as u64;
        if n == 0 {
            let v = verifier
                .take()
                .ok_or(admission(AdmissionRefusal::Evidence))?;
            v.finish()
                .map_err(|e| admission(AdmissionRefusal::Archive(e)))?;
            return Ok(());
        }
        let fed_from = end;
        end += n;
        let mut at = fed_from;
        while at < end {
            let v = verifier
                .take()
                .ok_or(admission(AdmissionRefusal::Evidence))?;
            let mut input = &buffer[at..end];
            let before = input.len();
            let (next, event) = v
                .step(&mut input)
                .map_err(|e| admission(AdmissionRefusal::Archive(e)))?;
            verifier = Some(next);
            let consumed = before - input.len();
            let start = at;
            at += consumed;
            match event {
                None => break,
                Some(ArchiveEvent::Header { position }) => {
                    let row = rows.row(position);
                    enter_parents(root, &row, &mut parent_chain, work)?;
                    let (_, name) = split(row.path);
                    let parent = parent_chain.last().unwrap_or(root);
                    match row.kind {
                        RowKind::File { length, .. } => {
                            let file = create_file(parent, name, work)?;
                            writing = Some(Writing {
                                file,
                                length,
                                written: 0,
                            });
                        }
                        RowKind::Dir => match parent
                            .create_exclusive_directory_accounted(name, work)
                        {
                            Ok(ExclusiveDirectoryOutcome::Created(created)) => drop(created),
                            Ok(ExclusiveDirectoryOutcome::EntryExists) => {
                                return Err(install_io("mkdirat")(exists()));
                            }
                            Err(e) => return Err(io_of::<ExclusiveDirectoryError>("mkdirat")(e)),
                        },
                        RowKind::Symlink { target } => {
                            work.charge(owned_record(target.len()))?;
                            ct::create_symlink(parent, name, target, work).map_err(io_of::<
                                io::Error,
                            >(
                                "symlinkat",
                            ))?;
                        }
                    }
                }
                Some(ArchiveEvent::FileBytes { bytes, .. }) => {
                    let w = writing
                        .as_mut()
                        .ok_or(admission(AdmissionRefusal::Evidence))?;
                    // The chunk's bytes are contiguous: the pending prefix,
                    // then this event's slice.
                    let chunk_start = start - pending;
                    let mut available = pending + bytes.len();
                    let mut from = chunk_start;
                    loop {
                        let remaining = w.length - w.written;
                        let chunk =
                            to_usize(remaining.min(READ_CHUNK as u64)).unwrap_or(READ_CHUNK);
                        if chunk == 0 || available < chunk {
                            break;
                        }
                        chunk_write(&w.file, w.written, &buffer[from..from + chunk], work)?;
                        w.written += chunk as u64;
                        from += chunk;
                        available -= chunk;
                    }
                    pending = available;
                }
                Some(ArchiveEvent::MemberEnd { .. }) => {
                    writing = None;
                    parent_chain.clear();
                    pending = 0;
                }
                Some(ArchiveEvent::End { sha256 }) => {
                    if &hex64(&sha256)[..] != archive_digest.as_bytes() {
                        return Err(admission(AdmissionRefusal::ArchiveDigest));
                    }
                }
            }
        }
        // Keep an unwritten chunk's bytes at the buffer's start.
        if pending > 0 {
            buffer.copy_within(end - pending..end, 0);
        }
        end = pending;
    }
}

fn capacity_or_archive(e: ArchiveRefusal) -> AdmissionRefusal {
    match e {
        ArchiveRefusal::Capacity { capacity, .. } => AdmissionRefusal::Capacity(capacity),
        other => AdmissionRefusal::Archive(other),
    }
}

/// Descend from `tree/` along a member's parent chain, one component at a
/// time (`desc(len(seg_i))` each), holding only that chain.
fn enter_parents(
    root: &RetainedDirectory,
    row: &TreeRow<'_>,
    chain: &mut Vec<RetainedDirectory>,
    work: &mut WorkScope<'_>,
) -> Result<(), Failure> {
    chain.clear();
    let (parent, _) = split(row.path);
    if parent.is_empty() {
        return Ok(());
    }
    for segment in parent.split('/') {
        let from = chain.last().unwrap_or(root);
        let level = descend(from, segment, None, work).map_err(walk_failure)?;
        chain.push(level.directory);
    }
    Ok(())
}

/// Step 4: finalize in the branch-local post-order (CI-A1-c): each file's
/// final mode then its barrier; each directory's `0500` then its barrier
/// after all its descendants, at its pop; `tree/` last.
fn finalize(
    stage: &RetainedDirectory,
    tree: &Tree<'_>,
    order: &[u32],
    work: &mut WorkScope<'_>,
) -> Result<(), Failure> {
    let finish = |level: Level, work: &mut WorkScope<'_>| -> Result<(), Failure> {
        ct::set_mode(level.directory.as_file(), 0o500, work)
            .map_err(io_of::<io::Error>("fchmod"))?;
        level
            .directory
            .confirm_directory_barrier_accounted(work)
            .map_err(io_of::<io::Error>("barrier-directory"))?;
        Ok(())
    };
    let root = descend(stage, TREE, None, work).map_err(walk_failure)?;
    let mut stack = vec![root];
    for &index in order {
        let row = tree.row(index);
        let (parent, name) = split(row.path);
        pop_to(&mut stack, tree, parent, work, finish)?;
        let top = stack.last().ok_or(admission(AdmissionRefusal::Evidence))?;
        match row.kind {
            RowKind::File { .. } => {
                let file = ct::open_regular_no_follow(&top.directory, name, FINALIZE_ACCESS, work)
                    .map_err(|e| walk_failure(open_fault("openat", index, e)))?;
                ct::set_mode(file.file(), installed_mode(&row), work)
                    .map_err(io_of::<io::Error>("fchmod"))?;
                ct::barrier_file(file.file(), work).map_err(io_of::<io::Error>("barrier-file"))?;
            }
            RowKind::Dir => {
                let level =
                    descend(&top.directory, name, Some(index), work).map_err(walk_failure)?;
                stack.push(level);
            }
            RowKind::Symlink { .. } => {}
        }
    }
    while let Some(level) = stack.pop() {
        finish(level, work)?;
    }
    Ok(())
}

/// LD-CIP-6: the finalization open's access mode, selected per platform
/// before the open and never retried in the other mode. On macOS a
/// read-only descriptor takes both `fchmod` and `F_FULLFSYNC`.
const FINALIZE_ACCESS: Access = Access::ReadOnly;

/// Step 4.2: `generation.json`, created exclusive at `0600`, written with
/// P-1, then `0400`, then its barrier. Returns the record's bytes, the
/// owned expected record V2 compares.
fn record_file(
    stage: &RetainedDirectory,
    record: &Record<'_>,
    work: &mut WorkScope<'_>,
) -> Result<Vec<u8>, Failure> {
    let file = create_file(stage, RECORD, work)?;
    work.charge(owned_record(record.length()))?;
    let bytes = record.encode();
    for (i, chunk) in bytes.chunks(READ_CHUNK).enumerate() {
        chunk_write(&file, (i * READ_CHUNK) as u64, chunk, work)?;
    }
    ct::set_mode(&file, 0o400, work).map_err(io_of::<io::Error>("fchmod"))?;
    ct::barrier_file(&file, work).map_err(io_of::<io::Error>("barrier-file"))?;
    Ok(bytes)
}

/// Step 4.3: `pin.lock`, created exclusive at `0600`, empty, then its
/// barrier.
fn pin_file(stage: &RetainedDirectory, work: &mut WorkScope<'_>) -> Result<(), Failure> {
    let file = create_file(stage, PIN, work)?;
    ct::barrier_file(&file, work).map_err(io_of::<io::Error>("barrier-file"))?;
    Ok(())
}

/// `tree/`'s own installed mode, `0500` (CI-A2-d): one status read.
pub(crate) fn tree_root_mode(
    parent: &RetainedDirectory,
    work: &mut WorkScope<'_>,
) -> Result<(), WalkFailure> {
    let status = ct::entry_status(parent, TREE, work).map_err(|e| open_fault("fstatat", 0, e))?;
    if status.kind != EntryKind::Directory || status.mode != 0o500 {
        return Err(WorkFailure::Operation(TreeFault::Mode { row: None }));
    }
    Ok(())
}

/// A missing or mistyped record is an association failure, not an absence.
fn association(e: WalkFailure) -> WalkFailure {
    match e {
        WorkFailure::Operation(TreeFault::Absent { .. } | TreeFault::Type { .. }) => {
            WorkFailure::Operation(TreeFault::Association)
        }
        other => other,
    }
}
/// A missing or mistyped `pin.lock` fails `Pin`; nothing recreates it.
pub(crate) fn pin_fault(e: WalkFailure) -> WalkFailure {
    match e {
        WorkFailure::Operation(TreeFault::Absent { .. } | TreeFault::Type { .. }) => {
            WorkFailure::Operation(TreeFault::Pin)
        }
        other => other,
    }
}

/// V2 and the open: `generation.json` is a regular `0400` file whose bytes
/// equal the owned expected record, compared byte for byte, with no parse.
pub(crate) fn check_record(
    generation: &RetainedDirectory,
    expected: &[u8],
    buffer: &mut [u8],
    work: &mut WorkScope<'_>,
) -> Result<(), WalkFailure> {
    let file = ct::open_regular_no_follow(generation, RECORD, Access::ReadOnly, work)
        .map_err(|e| association(open_fault("openat", 0, e)))?;
    if file.mode() != 0o400 || file.length() != expected.len() as u64 {
        return Err(WorkFailure::Operation(TreeFault::Association));
    }
    let attempts = envelope(expected.len() as u64);
    let (mut made, mut total) = (0u64, 0usize);
    let mut reader = file.file();
    loop {
        if made == attempts {
            return Err(WorkFailure::Operation(TreeFault::Association));
        }
        work.charge(READ)?;
        made += 1;
        let n = reader.read(buffer).map_err(io_fault("read"))?;
        if n == 0 {
            break;
        }
        if total + n > expected.len() || buffer[..n] != expected[total..total + n] {
            return Err(WorkFailure::Operation(TreeFault::Association));
        }
        total += n;
    }
    if total != expected.len() {
        return Err(WorkFailure::Operation(TreeFault::Association));
    }
    Ok(())
}

/// V2: `pin.lock` is a regular empty `0600` file.
pub(crate) fn check_pin(
    generation: &RetainedDirectory,
    work: &mut WorkScope<'_>,
) -> Result<(), WalkFailure> {
    let file = ct::open_regular_no_follow(generation, PIN, Access::ReadOnly, work)
        .map_err(|e| pin_fault(open_fault("openat", 0, e)))?;
    if file.mode() != 0o600 || file.length() != 0 {
        return Err(WorkFailure::Operation(TreeFault::Pin));
    }
    Ok(())
}

#[cfg(test)]
#[path = "installation_tests.rs"]
pub(crate) mod tests;
