// Unit CI-2's controls for the component store's primitives (plan r3,
// CI-PT-1, CI-PT-5 and CI-PT-6): each charges exactly its price before its
// one native call; the barrier receipt binds its exact handle; the pin is one
// flock, busy hands the file back, and release is the close alone; P-7's
// price equals the filesystem's own expression.
use super::*;
use crate::WorkLedger;
use std::os::unix::fs::PermissionsExt;
use std::path::PathBuf;

struct Scratch(PathBuf);
impl Drop for Scratch {
    fn drop(&mut self) {
        // The removal is checked unless the test is already failing.
        let removed = std::fs::remove_dir_all(&self.0);
        if !std::thread::panicking() {
            removed.unwrap();
        }
    }
}
fn scratch() -> (Scratch, RetainedDirectory) {
    let mut bytes = [0u8; 8];
    getrandom::fill(&mut bytes).unwrap();
    let hex: String = bytes.iter().map(|b| format!("{b:02x}")).collect();
    let dir = std::env::temp_dir().join(format!("opensip-component-tree-{hex}"));
    std::fs::create_dir(&dir).unwrap();
    std::fs::set_permissions(&dir, std::fs::Permissions::from_mode(0o700)).unwrap();
    let retained = RetainedDirectory::from_retained_handle(File::open(&dir).unwrap()).unwrap();
    (Scratch(dir), retained)
}
fn add(a: WorkCost, b: WorkCost) -> WorkCost {
    a.checked_add(b).unwrap()
}

#[test]
fn p7_status_price_equals_the_filesystem_expression() {
    // CI-PT-1: the two definitions are the identical expression.
    let ours = include_str!("component_tree.rs");
    let theirs = include_str!("filesystem/path_binding.rs");
    let body = |s: &str, head: &str| {
        let at = s.find(head).unwrap() + head.len();
        let end = at + s[at..].find("\n}\n").unwrap();
        s[at..end].split_whitespace().collect::<Vec<_>>().join(" ")
    };
    let ours = body(ours, "pub fn status_read_cost() -> crate::WorkCost {");
    let theirs = body(
        theirs,
        "pub(super) fn status_read_cost() -> crate::WorkCost {",
    );
    assert_eq!(ours, theirs);
    assert!(ours.contains("size_of::<libc::stat>().max(std::mem::size_of::<std::fs::Metadata>())"));
}

#[test]
fn the_no_follow_open_admits_regular_files_only_and_charges_first() {
    let (s, dir) = scratch();
    std::fs::write(s.0.join("f"), b"abc").unwrap();
    std::fs::set_permissions(s.0.join("f"), std::fs::Permissions::from_mode(0o640)).unwrap();
    std::os::unix::fs::symlink("f", s.0.join("l")).unwrap();
    std::fs::create_dir(s.0.join("d")).unwrap();
    let mut ledger = WorkLedger::new();
    ledger
        .scope(|work| {
            let before = work.used();
            let f = open_regular_no_follow(&dir, "f", Access::ReadOnly, work)?;
            assert_eq!(work.used(), add(before, open_regular_no_follow_cost()));
            assert_eq!((f.length(), f.mode()), (3, 0o640));
            for (name, access) in [
                ("l", Access::ReadOnly),
                ("d", Access::ReadOnly),
                ("d", Access::ReadWrite),
            ] {
                assert!(matches!(
                    open_regular_no_follow(&dir, name, access, work),
                    Err(WorkFailure::Operation(TreeOpenError::NotRegular))
                ));
            }
            assert!(matches!(
                open_regular_no_follow(&dir, "absent", Access::ReadOnly, work),
                Err(WorkFailure::Operation(TreeOpenError::Absent))
            ));
            for bad in ["", ".", "..", "a/b"] {
                let used = work.used();
                assert!(matches!(
                    open_regular_no_follow(&dir, bad, Access::ReadOnly, work),
                    Err(WorkFailure::Operation(TreeOpenError::Name))
                ));
                assert_eq!(work.used(), used, "a refused name charges nothing");
            }
            Ok::<_, WorkFailure<TreeOpenError>>(())
        })
        .unwrap();
}

#[test]
fn an_unfunded_open_refuses_before_its_call() {
    let (s, dir) = scratch();
    std::fs::write(s.0.join("f"), b"abc").unwrap();
    let mut ledger = WorkLedger::with_limits(WorkCost {
        objects: 1,
        edges: 1,
        bytes: 1 << 20,
    })
    .unwrap();
    let r =
        ledger.scope(|work| open_regular_no_follow(&dir, "f", Access::ReadOnly, work).map(|_| ()));
    assert!(matches!(
        r,
        Err(WorkFailure::Budget(crate::WorkBudgetError::Edges))
    ));
    assert!(ledger.is_failed());
}

#[test]
fn the_archive_open_is_no_follow_and_samples_identity() {
    let (s, _) = scratch();
    std::fs::write(s.0.join("a.tar"), b"0123456789").unwrap();
    std::os::unix::fs::symlink(s.0.join("a.tar"), s.0.join("link.tar")).unwrap();
    let mut ledger = WorkLedger::new();
    ledger
        .scope(|work| {
            let a = open_archive(&s.0.join("a.tar"), work)?;
            assert_eq!(a.length(), 10);
            let before = work.used();
            let sample = sample_identity(&a, work).map_err(|e| match e {
                WorkFailure::Budget(b) => WorkFailure::Budget(b),
                WorkFailure::Operation(e) => WorkFailure::Operation(TreeOpenError::Io(e)),
            })?;
            assert_eq!(work.used(), add(before, status_read_cost()));
            assert_eq!(sample, a.identity());
            assert!(matches!(
                open_archive(&s.0.join("link.tar"), work),
                Err(WorkFailure::Operation(TreeOpenError::NotRegular))
            ));
            Ok::<_, WorkFailure<TreeOpenError>>(())
        })
        .unwrap();
}

#[test]
fn chunks_modes_and_status_are_one_charged_call_each() {
    let (s, dir) = scratch();
    let mut ledger = WorkLedger::new();
    ledger
        .scope(|work| {
            let file = std::fs::File::create(s.0.join("w")).unwrap();
            let before = work.used();
            write_chunk(&file, 0, b"hello", work).map_err(|_| WorkFailure::Operation(()))?;
            write_chunk(&file, 5, b" world", work).map_err(|_| WorkFailure::Operation(()))?;
            assert_eq!(work.used(), add(add(before, NATIVE_CALL), NATIVE_CALL));
            let before = work.used();
            set_mode(&file, 0o400, work).map_err(|_| WorkFailure::Operation(()))?;
            assert_eq!(work.used(), add(before, NATIVE_CALL));
            let before = work.used();
            let st = entry_status(&dir, "w", work).map_err(|_| WorkFailure::Operation(()))?;
            assert_eq!(work.used(), add(before, status_read_cost()));
            assert_eq!(
                st,
                EntryStatus {
                    kind: EntryKind::File,
                    mode: 0o400,
                    length: 11
                }
            );
            Ok::<_, WorkFailure<()>>(())
        })
        .unwrap();
    assert_eq!(std::fs::read(s.0.join("w")).unwrap(), b"hello world");
}

#[test]
fn symlinks_are_created_and_read_never_followed() {
    let (s, dir) = scratch();
    let mut ledger = WorkLedger::new();
    ledger
        .scope(|work| {
            let before = work.used();
            create_symlink(&dir, "l", "../outside/target", work)
                .map_err(|_| WorkFailure::Operation(()))?;
            assert_eq!(work.used(), add(before, NATIVE_CALL));
            let mut buffer = [0u8; LINK_BUFFER];
            let before = work.used();
            let n =
                read_link(&dir, "l", &mut buffer, work).map_err(|_| WorkFailure::Operation(()))?;
            assert_eq!(work.used(), add(before, NATIVE_CALL));
            assert_eq!(&buffer[..n], b"../outside/target");
            let st = entry_status(&dir, "l", work).map_err(|_| WorkFailure::Operation(()))?;
            assert_eq!(st.kind, EntryKind::Symlink);
            let long = "t".repeat(150);
            create_symlink(&dir, "long", &long, work).map_err(|_| WorkFailure::Operation(()))?;
            assert_eq!(
                read_link(&dir, "long", &mut buffer, work)
                    .map_err(|_| WorkFailure::Operation(()))?,
                LINK_BUFFER
            );
            Ok::<_, WorkFailure<()>>(())
        })
        .unwrap();
    std::fs::write(s.0.join("plain"), b"").unwrap();
    let mut ledger = WorkLedger::new();
    let r = ledger.scope(|work| read_link(&dir, "plain", &mut [0u8; LINK_BUFFER], work));
    assert!(matches!(
        r,
        Err(WorkFailure::Operation(TreeOpenError::NotRegular))
    ));
}

#[test]
fn the_barrier_receipt_binds_its_exact_handle() {
    // CI-PT-6: `is_for` is handle identity; a failed barrier gives no receipt.
    let (s, dir) = scratch();
    std::fs::write(s.0.join("f"), b"x").unwrap();
    let mut ledger = WorkLedger::new();
    ledger
        .scope(|work| {
            let a = open_regular_no_follow(&dir, "f", Access::ReadOnly, work)
                .map_err(|_| WorkFailure::Operation(()))?;
            let b = open_regular_no_follow(&dir, "f", Access::ReadOnly, work)
                .map_err(|_| WorkFailure::Operation(()))?;
            let before = work.used();
            let receipt = barrier_file(a.file(), work).map_err(|_| WorkFailure::Operation(()))?;
            assert_eq!(work.used(), add(before, NATIVE_CALL));
            assert!(receipt.is_for(a.file()));
            assert!(
                !receipt.is_for(b.file()),
                "another handle to the same file is not this handle"
            );
            Ok::<_, WorkFailure<()>>(())
        })
        .unwrap();
    // A barrier on a pipe fails, and yields no receipt.
    let mut fds = [0; 2];
    // SAFETY: a valid two-slot output array.
    assert_eq!(unsafe { libc::pipe(fds.as_mut_ptr()) }, 0);
    // SAFETY: pipe returned two owned descriptors.
    let (r, w) = unsafe { (File::from_raw_fd(fds[0]), File::from_raw_fd(fds[1])) };
    let mut ledger = WorkLedger::new();
    assert!(matches!(
        ledger.scope(|work| barrier_file(&r, work).map(|_| ())),
        Err(WorkFailure::Operation(_))
    ));
    drop(w);
}

#[test]
fn a_pin_is_one_flock_and_releases_by_close() {
    // CI-PT-5: shared pins coexist; an exclusive probe is busy while any is
    // held and hands its file back; dropping the last pin releases.
    let (s, dir) = scratch();
    std::fs::write(s.0.join("pin.lock"), b"").unwrap();
    let mut ledger = WorkLedger::new();
    ledger
        .scope(|work| {
            let open = |work: &mut WorkScope<'_>| {
                open_regular_no_follow(&dir, "pin.lock", Access::ReadOnly, work)
                    .map_err(|_| WorkFailure::Operation(()))
            };
            let f = open(work)?;
            let before = work.used();
            let first = try_pin(f, PinMode::Shared, work)
                .map_err(|_| WorkFailure::Operation(()))?
                .unwrap();
            assert_eq!(work.used(), add(before, NATIVE_CALL));
            assert_eq!(first.mode(), PinMode::Shared);
            let second = try_pin(open(work)?, PinMode::Shared, work)
                .map_err(|_| WorkFailure::Operation(()))?
                .unwrap();
            let probe = open(work)?;
            let probe =
                try_pin(probe, PinMode::Exclusive, work).map_err(|_| WorkFailure::Operation(()))?;
            let probe = probe.expect_err("busy while pinned");
            drop(first);
            let probe =
                try_pin(probe, PinMode::Exclusive, work).map_err(|_| WorkFailure::Operation(()))?;
            let probe = probe.expect_err("still busy while one pin remains");
            drop(second);
            let held = try_pin(probe, PinMode::Exclusive, work)
                .map_err(|_| WorkFailure::Operation(()))?
                .unwrap();
            assert!(
                try_pin(open(work)?, PinMode::Shared, work)
                    .map_err(|_| WorkFailure::Operation(()))?
                    .is_err()
            );
            drop(held);
            assert!(
                try_pin(open(work)?, PinMode::Shared, work)
                    .map_err(|_| WorkFailure::Operation(()))?
                    .is_ok()
            );
            Ok::<_, WorkFailure<()>>(())
        })
        .unwrap();
}

#[test]
fn source_pins_one_call_per_primitive_and_no_unlock() {
    // CI-PT-5 and CI-PT-6 as source pins: one native call per primitive, no
    // unlock, no duplicate descriptor, no retry loop, no FileLock, no
    // FileBarrierReceipt, and no whole-buffer writer.
    let source = include_str!("component_tree.rs");
    let code: String = source
        .lines()
        .filter(|l| !l.trim_start().starts_with("//"))
        .collect::<Vec<_>>()
        .join("\n");
    for forbidden in [
        "LOCK_UN",
        "dup(",
        "dup2(",
        "loop {",
        "while ",
        "FileLock",
        "FileBarrierReceipt",
        "write_new_regular",
        "write_all",
    ] {
        assert!(!code.contains(forbidden), "{forbidden}");
    }
    for call in [
        "libc::flock(",
        "libc::pwrite(",
        "libc::fchmod(",
        "libc::symlinkat(",
        "libc::readlinkat(",
        "libc::F_FULLFSYNC",
    ] {
        assert_eq!(code.matches(call).count(), 1, "{call}");
    }
}

// ---- CI2-R1-RF-1: no primitive allocates (a counting allocator) ----

/// This test binary's allocator: the system's, counting each thread's
/// allocations (CI2-R1-RF-1's independent allocation oracle).
struct Counting;
thread_local! {
    static ALLOCATIONS: std::cell::Cell<usize> = const { std::cell::Cell::new(0) };
}
// SAFETY: every call forwards to the system allocator unchanged; the count is
// a thread-local `Cell` with a constant initializer, which never allocates.
unsafe impl std::alloc::GlobalAlloc for Counting {
    unsafe fn alloc(&self, layout: std::alloc::Layout) -> *mut u8 {
        ALLOCATIONS.try_with(|a| a.set(a.get() + 1)).ok();
        // SAFETY: the caller's layout contract is forwarded unchanged.
        unsafe { std::alloc::System.alloc(layout) }
    }
    unsafe fn dealloc(&self, ptr: *mut u8, layout: std::alloc::Layout) {
        // SAFETY: `ptr` came from this allocator's `alloc`, i.e. the system's.
        unsafe { std::alloc::System.dealloc(ptr, layout) }
    }
}
#[global_allocator]
static COUNTING: Counting = Counting;
fn allocations() -> usize {
    ALLOCATIONS.with(|a| a.get())
}
/// The allocations `f` makes on this thread.
fn allocated<T>(f: impl FnOnce() -> T) -> (T, usize) {
    let before = allocations();
    let out = f();
    (out, allocations() - before)
}

#[test]
fn every_primitive_copies_names_onto_the_stack_and_allocates_nothing() {
    let (s, dir) = scratch();
    std::fs::write(s.0.join("f"), b"abc").unwrap();
    let archive = s.0.join("f");
    let mut ledger = WorkLedger::new();
    ledger
        .scope(|work| {
            let (f, n) = allocated(|| open_regular_no_follow(&dir, "f", Access::ReadOnly, work));
            let f = f.map_err(|_| WorkFailure::Operation(()))?;
            assert_eq!(n, 0, "open");
            let (r, n) = allocated(|| entry_status(&dir, "f", work));
            r.map_err(|_| WorkFailure::Operation(()))?;
            assert_eq!(n, 0, "status");
            let (r, n) = allocated(|| create_symlink(&dir, "l", "f", work));
            r.map_err(|_| WorkFailure::Operation(()))?;
            assert_eq!(n, 0, "symlinkat");
            let mut buffer = [0u8; LINK_BUFFER];
            let (r, n) = allocated(|| read_link(&dir, "l", &mut buffer, work));
            r.map_err(|_| WorkFailure::Operation(()))?;
            assert_eq!(n, 0, "readlinkat");
            let (r, n) = allocated(|| open_archive(&archive, work));
            r.map_err(|_| WorkFailure::Operation(()))?;
            assert_eq!(n, 0, "archive open");
            let (r, n) = allocated(|| set_mode(f.file(), 0o600, work));
            r.map_err(|_| WorkFailure::Operation(()))?;
            assert_eq!(n, 0, "fchmod");
            let (r, n) = allocated(|| barrier_file(f.file(), work).map(|_| ()));
            r.map_err(|_| WorkFailure::Operation(()))?;
            assert_eq!(n, 0, "barrier");
            Ok::<_, WorkFailure<()>>(())
        })
        .unwrap();
}

#[test]
fn an_unfunded_or_overlong_name_refuses_before_any_copy_or_call() {
    let (s, dir) = scratch();
    std::fs::write(s.0.join("f"), b"abc").unwrap();
    // One edge short of the open: the budget refuses, with nothing allocated.
    let mut ledger = WorkLedger::with_limits(WorkCost {
        objects: 1,
        edges: 1,
        bytes: 1 << 20,
    })
    .unwrap();
    let (r, n) = allocated(|| {
        ledger.scope(|work| open_regular_no_follow(&dir, "f", Access::ReadOnly, work).map(|_| ()))
    });
    assert!(matches!(r, Err(WorkFailure::Budget(_))));
    assert_eq!(n, 0);
    // A name or path beyond the stack capacity refuses `Name` and charges nothing.
    let long = "n".repeat(NAME_CAPACITY + 1);
    let mut ledger = WorkLedger::new();
    ledger
        .scope(|work| {
            let used = work.used();
            assert!(matches!(
                open_regular_no_follow(&dir, &long, Access::ReadOnly, work),
                Err(WorkFailure::Operation(TreeOpenError::Name))
            ));
            assert!(matches!(
                open_archive(&s.0.join(&long), work),
                Err(WorkFailure::Operation(TreeOpenError::Name))
            ));
            assert_eq!(work.used(), used);
            Ok::<_, WorkFailure<()>>(())
        })
        .unwrap();
}

#[test]
fn every_primitive_charges_before_its_native_call() {
    // A source-order guard (the pre-submission checklist's item 1): in each
    // primitive's body the charge comes before the one native call it makes.
    let source = include_str!("component_tree.rs");
    for (function, call) in [
        ("pub fn open_regular_no_follow(", "libc::openat("),
        ("pub fn open_archive(", "libc::open("),
        ("pub fn sample_identity(", "fstat(&file.file)"),
        ("pub fn entry_status(", "libc::fstatat("),
        ("pub fn write_chunk(", "libc::pwrite("),
        ("pub fn set_mode(", "libc::fchmod("),
        ("pub fn barrier_file<'file>(", "full_flush(file)"),
        ("pub fn create_symlink(", "libc::symlinkat("),
        ("pub fn read_link(", "libc::readlinkat("),
        ("pub fn try_pin(", "libc::flock("),
    ] {
        let at = source
            .find(function)
            .unwrap_or_else(|| panic!("{function}"));
        let body = &source[at..at + source[at..].find("\n}\n").unwrap()];
        let charge = body
            .find("work.charge(")
            .unwrap_or_else(|| panic!("{function}: no charge"));
        let native = body
            .find(call)
            .unwrap_or_else(|| panic!("{function}: no {call}"));
        assert!(
            charge < native,
            "{function}: the native call precedes its charge"
        );
    }
}
