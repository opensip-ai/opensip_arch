//! Law CI r5 items 6 and 7, with amendment CI-A2 (proposed with this unit)
//! (unit CI-3; component installation plan r3): the retained-tree
//! capability C2a-3 binds, and its bounded verified-byte transfer.
//!
//! `open_retained_tree` re-verifies everything, every time: the store's and
//! the generation's custody, the association of the generation with the
//! authenticated evidence and C2a-1's candidate, the pin, and the whole
//! tree's structure, installed modes, link targets and bytes. It trusts
//! nothing by existence, and repairs nothing. The capability it returns is
//! pinned (a shared `flock` on `pin.lock`) and holds the retained handles
//! and the shared read buffer, so a transfer re-reads a file from the
//! retained `tree/` handle, component by component, and hands the sink its
//! bytes only as verified at the end.
use crate::installation::{
    self as inst, ComponentStore, Evidence, Phase, READ, READ_CHUNK, TREE, Tree, TreeFault,
    charged_find, charged_sort, component_cmp, custody_cost, descend, descend_cost, envelope,
    index_buffer_cost, read_verified, search_comparisons, sort_comparisons, split,
};
use opensip_platform::component_tree::{self as ct, Access, PinLock, PinMode, TreeOpenError};
use opensip_platform::{RetainedDirectory, WorkBudgetError, WorkCost, WorkFailure, WorkScope};
use opensip_security::archive_profile::RowKind;
use opensip_security::snapshot_source::{CustodyDirectoryRefusal, owned_record};
use opensip_security::{AuthenticatedComponent, ClosureCandidate, SelectedPlatform};
use std::io;

/// Which fence the caller holds while it pins (LAW item 7): the durable
/// path's lifecycle fence, ER10a's read-session fence, or none for an
/// ephemeral read. The pin itself is the same shared `flock` in each.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum PinRequest {
    UnderFence,
    UnderReadSession,
    Ephemeral,
}

/// LAW item 6's typed failures. `NotInstalled` is the only absence of the
/// generation; every other failure but `Budget` and `Io` is a promised
/// tree's own corruption and keeps its cause (LAW item 8).
#[derive(Debug)]
pub enum TreeReadFailure {
    NotInstalled,
    Absent {
        row: u32,
    },
    Length {
        row: u32,
    },
    Digest {
        row: u32,
    },
    /// A row of the wrong type, or (`None`) a generation name that is not a
    /// directory.
    Type {
        row: Option<u32>,
    },
    Mode {
        row: Option<u32>,
    },
    LinkTarget {
        row: u32,
    },
    Extra {
        directory: Option<u32>,
    },
    Association,
    Pin,
    Custody(CustodyDirectoryRefusal),
    Budget(WorkBudgetError),
    Io {
        call: &'static str,
        error: io::Error,
    },
}
impl TreeReadFailure {
    fn of(e: WorkFailure<TreeFault>) -> Self {
        match e {
            WorkFailure::Budget(b) => Self::Budget(b),
            WorkFailure::Operation(fault) => match fault {
                TreeFault::Absent { row } => Self::Absent { row },
                TreeFault::Extra { directory } => Self::Extra { directory },
                TreeFault::Type { row } => Self::Type { row: Some(row) },
                TreeFault::Mode { row } => Self::Mode { row },
                TreeFault::LinkTarget { row } => Self::LinkTarget { row },
                TreeFault::Length { row } => Self::Length { row },
                TreeFault::Digest { row } => Self::Digest { row },
                TreeFault::Association => Self::Association,
                TreeFault::Pin => Self::Pin,
                TreeFault::Io { call, error } => Self::Io { call, error },
            },
        }
    }
}

/// The sink of one verified transfer. It receives the expected digest and
/// length first, then the bytes, and is told only at the end whether the
/// stream verified; it must commit nothing unless `finish(true)` arrives.
/// Its own work is charged to its owner's ledger.
pub trait VerifiedSink {
    fn begin(&mut self, sha256: [u8; 32], length: u64);
    fn chunk(&mut self, bytes: &[u8]);
    fn finish(&mut self, verified: bool);
}

/// The opaque, pinned capability: the store's borrowed directory, the
/// generation's, `tree/`'s and `pin.lock`'s retained handles, the shared
/// read buffer, the borrowed TreeCommitment and its component-ordered index
/// (CI-A2-b). Only `open_retained_tree` constructs one; it never stands for
/// bytes present later on its own.
pub struct RetainedTree<'s, 'a> {
    #[allow(dead_code)]
    store: &'s ComponentStore,
    #[allow(dead_code)]
    generation: RetainedDirectory,
    tree_dir: RetainedDirectory,
    pin: PinLock,
    buffer: Vec<u8>,
    tree: Tree<'a>,
    order: Vec<u32>,
    /// The fence the caller declared it held while pinning (LAW item 7).
    request: PinRequest,
}

/// `CAP`: the capability record's size, a compile-time property of the
/// code.
pub(crate) fn capability_cost() -> WorkCost {
    WorkCost {
        objects: 1,
        edges: 0,
        bytes: size_of::<RetainedTree<'static, 'static>>(),
    }
}

/// `B_open` (LAW item 6, with CI-A2-b and CI-A2-d), with checked arithmetic.
pub(crate) fn open_bound(tree: &Tree<'_>, record: usize) -> Option<WorkCost> {
    let st = ct::status_read_cost();
    let fopen = ct::open_regular_no_follow_cost();
    let (n, d) = (tree.n, tree.dirs);
    let listing = n.checked_add(3usize.checked_mul(d.checked_add(1)?)?)?;
    let mut b = inst::Bound::default()
        .add(custody_cost())?
        .add(owned_record(inst::NAME_BYTES + 1))?
        .add(descend_cost(inst::NAME_BYTES))?
        .add(custody_cost())?
        .add(fopen)?
        .add(ct::NATIVE_CALL)?
        .add(owned_record(record))?
        .add(fopen)?
        .add_times(READ, usize::try_from(envelope(record as u64)).ok()?)?
        .add(inst::buffer_cost())?
        .add(descend_cost(TREE.len()))?
        .add(st)?
        // CI-A2-b: the component-ordered index, and the Blobs' association.
        .add_times(index_buffer_cost(n)?, 2)?
        .add_times(inst::COMPARISON, sort_comparisons(n)?)?
        .add_times(
            inst::COMPARISON,
            tree.files.checked_mul(search_comparisons(n))?,
        )?
        .add_times(READ, listing)?
        .add_times(st, n)?
        .add(capability_cost())?;
    for row in tree.rows() {
        let (_, name) = split(row.path);
        match row.kind {
            RowKind::File { length, .. } => {
                b = b
                    .add(fopen)?
                    .add_times(READ, usize::try_from(envelope(length)).ok()?)?;
            }
            RowKind::Dir => b = b.add(descend_cost(name.len()))?,
            RowKind::Symlink { .. } => {
                b = b.add(ct::NATIVE_CALL)?.add(owned_record(ct::LINK_BUFFER))?
            }
        }
    }
    Some(b.0)
}

/// `B_transfer(f)` (LAW item 6, with CI-A2-c): the path's lookup, the
/// parent chain's descents, the file's open and its read attempts.
pub fn transfer_bound(tree_rows: usize, path: &str, length: u64) -> Option<WorkCost> {
    let mut b = inst::Bound::default()
        .add_times(inst::COMPARISON, search_comparisons(tree_rows))?
        .add(ct::open_regular_no_follow_cost())?
        .add_times(READ, usize::try_from(envelope(length)).ok()?)?;
    let (parent, _) = split(path);
    if !parent.is_empty() {
        for segment in parent.split('/') {
            b = b.add(descend_cost(segment.len()))?;
        }
    }
    Some(b.0)
}

/// Open the pinned capability for C2a-1's candidate of `component` on
/// `platform` (LAW item 6). Every operation is charged before it is made,
/// at `B_open`'s prices; the work profile is the caller's.
pub fn open_retained_tree<'s, 'a>(
    store: &'s ComponentStore,
    component: &AuthenticatedComponent<'a>,
    candidate: &'a ClosureCandidate<'_>,
    platform: SelectedPlatform<'_>,
    pin: PinRequest,
    work: &mut WorkScope<'_>,
) -> Result<RetainedTree<'s, 'a>, TreeReadFailure> {
    let evidence =
        inst::evidence(component, candidate, platform).map_err(|_| TreeReadFailure::Association)?;
    open_with(store, &evidence, candidate, pin, work)
}

fn budget(e: WorkFailure<TreeFault>) -> TreeReadFailure {
    TreeReadFailure::of(e)
}

pub(crate) fn open_with<'s, 'a>(
    store: &'s ComponentStore,
    evidence: &Evidence<'a>,
    candidate: &ClosureCandidate<'_>,
    pin: PinRequest,
    work: &mut WorkScope<'_>,
) -> Result<RetainedTree<'s, 'a>, TreeReadFailure> {
    let request = pin;
    let tree = evidence.tree;
    // The store's custody.
    match store.custody::<TreeFault>(store.directory.as_file(), work) {
        Ok(Ok(())) => {}
        Ok(Err(refusal)) => return Err(TreeReadFailure::Custody(refusal)),
        Err(e) => return Err(budget(e)),
    }
    // Association: the candidate's Blobs are exactly the file rows
    // projected, found through the component-ordered index (CI-A2-b).
    let order = charged_sort::<TreeFault>(tree.n, work, |a, b| {
        component_cmp(tree.row(a).path, tree.row(b).path).is_lt()
    })
    .map_err(budget)?;
    let mut blobs = 0usize;
    for blob in candidate.blobs() {
        blobs += 1;
        let found = charged_find::<TreeFault>(&tree, &order, blob.path(), work).map_err(budget)?;
        let Some(index) = found else {
            return Err(TreeReadFailure::Association);
        };
        let RowKind::File { length, sha256 } = tree.row(index).kind else {
            return Err(TreeReadFailure::Association);
        };
        if length != blob.bytes() || &inst::hex64(&sha256)[..] != blob.sha256().as_bytes() {
            return Err(TreeReadFailure::Association);
        }
    }
    if blobs != tree.files {
        return Err(TreeReadFailure::Association);
    }
    // `<closure2-hex>`: its name's record and its descent, retained.
    work.charge(owned_record(inst::NAME_BYTES + 1))
        .map_err(budget)?;
    let generation = match descend(&store.directory, evidence.name, None, work) {
        Ok(level) => level.directory,
        Err(WorkFailure::Operation(TreeFault::Io { error, .. }))
            if error.kind() == io::ErrorKind::NotFound =>
        {
            return Err(TreeReadFailure::NotInstalled);
        }
        Err(WorkFailure::Operation(TreeFault::Io { error, .. }))
            if ct::is_not_directory(&error) =>
        {
            return Err(TreeReadFailure::Type { row: None });
        }
        Err(e) => return Err(budget(e)),
    };
    match store.custody::<TreeFault>(generation.as_file(), work) {
        Ok(Ok(())) => {}
        Ok(Err(refusal)) => return Err(TreeReadFailure::Custody(refusal)),
        Err(e) => return Err(budget(e)),
    }
    // The pin, before anything else of the generation is read: the existing
    // `pin.lock`, never created, a regular empty `0600` file, then one
    // shared `flock`. Busy (an exclusive GC probe) fails `Pin`, unretried.
    let pin_file = match ct::open_regular_no_follow(&generation, inst::PIN, Access::ReadOnly, work)
    {
        Ok(file) => file,
        Err(WorkFailure::Budget(b)) => return Err(TreeReadFailure::Budget(b)),
        Err(WorkFailure::Operation(TreeOpenError::Absent | TreeOpenError::NotRegular)) => {
            return Err(TreeReadFailure::Pin);
        }
        Err(WorkFailure::Operation(e)) => return Err(io_failure("openat", e)),
    };
    if pin_file.mode() != 0o600 || pin_file.length() != 0 {
        return Err(TreeReadFailure::Pin);
    }
    let pin = match ct::try_pin(pin_file, PinMode::Shared, work) {
        Ok(Ok(pin)) => pin,
        Ok(Err(_busy)) => return Err(TreeReadFailure::Pin),
        Err(WorkFailure::Budget(b)) => return Err(TreeReadFailure::Budget(b)),
        Err(WorkFailure::Operation(error)) => {
            return Err(TreeReadFailure::Io {
                call: "flock",
                error,
            });
        }
    };
    // `generation.json`: the owned expected record, compared byte for byte.
    work.charge(owned_record(evidence.record.length()))
        .map_err(budget)?;
    let expected = evidence.record.encode();
    work.charge(inst::buffer_cost()).map_err(budget)?;
    let mut buffer = vec![0u8; READ_CHUNK];
    inst::check_record(&generation, &expected, &mut buffer, work).map_err(TreeReadFailure::of)?;
    drop(expected);
    // `tree/`, retained as the capability's base, and its own mode.
    let tree_dir = descend(&generation, TREE, None, work)
        .map_err(TreeReadFailure::of)?
        .directory;
    inst::tree_root_mode(&generation, work).map_err(TreeReadFailure::of)?;
    // The structure, the installed modes, the link targets and every byte.
    inst::walk(&tree_dir, &tree, &order, Phase::Opened, &mut buffer, work)
        .map_err(TreeReadFailure::of)?;
    work.charge(capability_cost()).map_err(budget)?;
    Ok(RetainedTree {
        store,
        generation,
        tree_dir,
        pin,
        buffer,
        tree,
        order,
        request,
    })
}

fn io_failure(call: &'static str, e: TreeOpenError) -> TreeReadFailure {
    match e {
        TreeOpenError::Io(error) => TreeReadFailure::Io { call, error },
        TreeOpenError::Absent => TreeReadFailure::Io {
            call,
            error: io::Error::new(io::ErrorKind::NotFound, "absent"),
        },
        other => TreeReadFailure::Io {
            call,
            error: io::Error::new(io::ErrorKind::InvalidInput, format!("{other:?}")),
        },
    }
}

impl RetainedTree<'_, '_> {
    /// The pin's mode: always shared.
    pub fn pin_mode(&self) -> PinMode {
        self.pin.mode()
    }
    /// The fence the caller declared it held while pinning.
    pub fn request(&self) -> PinRequest {
        self.request
    }
    /// Transfer the regular file at `path` to `sink`, verified (LAW item 6):
    /// its row found through the retained index (CI-A2-c), its parent chain
    /// resolved one no-follow component at a time from the retained `tree/`
    /// handle, its type, mode and length re-checked, then its bytes streamed
    /// through the retained buffer in charged attempts, hashed as they go.
    /// The sink is told at the end whether the stream verified.
    pub fn transfer(
        &mut self,
        path: &str,
        sink: &mut impl VerifiedSink,
        work: &mut WorkScope<'_>,
    ) -> Result<(), TreeReadFailure> {
        let result = self.transfer_inner(path, sink, work);
        if result.is_err() {
            sink.finish(false);
        }
        result
    }
    fn transfer_inner(
        &mut self,
        path: &str,
        sink: &mut impl VerifiedSink,
        work: &mut WorkScope<'_>,
    ) -> Result<(), TreeReadFailure> {
        let found =
            charged_find::<TreeFault>(&self.tree, &self.order, path, work).map_err(budget)?;
        let index = found.ok_or(TreeReadFailure::Association)?;
        let row = self.tree.row(index);
        let RowKind::File { length, sha256 } = row.kind else {
            return Err(TreeReadFailure::Association);
        };
        let (parent, name) = split(row.path);
        let mut chain: Vec<RetainedDirectory> = Vec::new();
        if !parent.is_empty() {
            for segment in parent.split('/') {
                let from = chain.last().unwrap_or(&self.tree_dir);
                let level = descend(from, segment, None, work).map_err(|e| match e {
                    WorkFailure::Operation(TreeFault::Io { error, .. })
                        if error.kind() == io::ErrorKind::NotFound =>
                    {
                        TreeReadFailure::Absent { row: index }
                    }
                    WorkFailure::Operation(TreeFault::Io { error, .. })
                        if ct::is_not_directory(&error) =>
                    {
                        TreeReadFailure::Type { row: Some(index) }
                    }
                    other => TreeReadFailure::of(other),
                })?;
                chain.push(level.directory);
            }
        }
        let directory = chain.last().unwrap_or(&self.tree_dir);
        let file = match ct::open_regular_no_follow(directory, name, Access::ReadOnly, work) {
            Ok(file) => file,
            Err(WorkFailure::Budget(b)) => return Err(TreeReadFailure::Budget(b)),
            Err(WorkFailure::Operation(TreeOpenError::Absent)) => {
                return Err(TreeReadFailure::Absent { row: index });
            }
            Err(WorkFailure::Operation(TreeOpenError::NotRegular)) => {
                return Err(TreeReadFailure::Type { row: Some(index) });
            }
            Err(WorkFailure::Operation(e)) => return Err(io_failure("openat", e)),
        };
        if file.mode() != inst::installed_mode(&row) {
            return Err(TreeReadFailure::Mode { row: Some(index) });
        }
        if file.length() != length {
            return Err(TreeReadFailure::Length { row: index });
        }
        sink.begin(sha256, length);
        read_verified(
            &file,
            index,
            length,
            sha256,
            &mut self.buffer,
            work,
            |bytes| sink.chunk(bytes),
        )
        .map_err(TreeReadFailure::of)?;
        sink.finish(true);
        Ok(())
    }
}

#[cfg(test)]
#[path = "retained_tree_tests.rs"]
mod tests;
