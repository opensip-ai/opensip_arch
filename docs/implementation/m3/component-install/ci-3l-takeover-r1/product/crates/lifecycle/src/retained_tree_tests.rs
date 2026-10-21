// Unit CI-3's controls (component installation plan r3, section 4): CI-T9,
// CI-T10, CI-T12's construction half, CI-T15, CI-T17, CI-T20, CI-T21 and
// CI-T22's B_open and B_transfer halves. Every tree is installed by the same
// installer (LAW item 6's fixture path), from C2a-1's `TestComponent`.
use super::*;
use crate::installation::tests::{
    Fixture, MACOS, Spec, SpecKind, dir, file, file_only, link, make_writable, nested, within,
};
use opensip_platform::WorkLedger;
use std::os::unix::fs::PermissionsExt;
use std::path::Path;

/// Open `f`'s capability on `ledger` and hand it to `then`.
fn opened<T>(
    f: &Fixture,
    request: PinRequest,
    ledger: &mut WorkLedger,
    then: impl FnOnce(&mut RetainedTree<'_, '_>, &mut WorkScope<'_>) -> T,
) -> Result<T, TreeReadFailure> {
    let candidate = f.candidate();
    let component = f.component.authenticated();
    within(ledger, |work| {
        match open_retained_tree(&f.store, &component, &candidate, MACOS, request, work) {
            Ok(mut tree) => Ok(then(&mut tree, work)),
            Err(e) => Err(e),
        }
    })
}
fn open(f: &Fixture) -> Result<(), TreeReadFailure> {
    opened(
        f,
        PinRequest::UnderFence,
        &mut WorkLedger::snapshot_profile(),
        |_, _| (),
    )
}
fn installed(specs: Vec<Spec>) -> Fixture {
    let f = Fixture::new(specs);
    f.install().unwrap();
    f
}
/// Change an installed entry: its directory is made writable, `change`
/// runs, and the directory's mode is restored.
fn tamper(f: &Fixture, relative: &str, change: impl FnOnce(&Path)) {
    let path = f.generation().join(relative);
    let parent = path.parent().unwrap().to_path_buf();
    let mode = std::fs::metadata(&parent).unwrap().permissions().mode() & 0o7777;
    std::fs::set_permissions(&parent, std::fs::Permissions::from_mode(0o700)).unwrap();
    change(&path);
    std::fs::set_permissions(&parent, std::fs::Permissions::from_mode(mode)).unwrap();
}
fn rewrite(path: &Path, bytes: &[u8]) {
    let mode = std::fs::metadata(path).unwrap().permissions().mode() & 0o7777;
    std::fs::set_permissions(path, std::fs::Permissions::from_mode(0o600)).unwrap();
    std::fs::write(path, bytes).unwrap();
    std::fs::set_permissions(path, std::fs::Permissions::from_mode(mode)).unwrap();
}

/// A sink that commits only on a verified finish.
#[derive(Default)]
struct Sink {
    expected: Option<([u8; 32], u64)>,
    pending: Vec<u8>,
    committed: Option<Vec<u8>>,
    finished: Vec<bool>,
}
impl VerifiedSink for Sink {
    fn begin(&mut self, sha256: [u8; 32], length: u64) {
        self.expected = Some((sha256, length));
    }
    fn chunk(&mut self, bytes: &[u8]) {
        self.pending.extend_from_slice(bytes);
    }
    fn finish(&mut self, verified: bool) {
        self.finished.push(verified);
        if verified {
            self.committed = Some(std::mem::take(&mut self.pending));
        }
    }
}

// ---- CI-T10: the capability's typed results ----

#[test]
fn ci_t10_not_installed_differs_from_absent() {
    let f = Fixture::new(nested());
    assert!(matches!(open(&f), Err(TreeReadFailure::NotInstalled)));
    f.install().unwrap();
    open(&f).unwrap();
    tamper(&f, "tree/a/b/empty", |p| std::fs::remove_file(p).unwrap());
    assert!(matches!(open(&f), Err(TreeReadFailure::Absent { .. })));
}

#[test]
fn ci_t10_a_short_ledger_is_budget() {
    let f = installed(nested());
    let mut ledger = WorkLedger::with_limits(opensip_platform::WorkCost {
        objects: 10,
        edges: 50,
        bytes: 1 << 20,
    })
    .unwrap();
    assert!(matches!(
        opened(&f, PinRequest::UnderFence, &mut ledger, |_, _| ()),
        Err(TreeReadFailure::Budget(_))
    ));
}

// ---- CI-T9 and CI-T17: corruption keeps its own cause ----

#[test]
fn ci_t9_a_modified_truncated_removed_or_replaced_file_refuses() {
    let f = installed(nested());
    tamper(&f, "tree/a/z", |p| {
        let mut b = std::fs::read(p).unwrap();
        b[10] ^= 1;
        rewrite(p, &b);
    });
    assert!(matches!(open(&f), Err(TreeReadFailure::Digest { .. })));
    let f = installed(nested());
    tamper(&f, "tree/a/z", |p| rewrite(p, b"short"));
    assert!(matches!(open(&f), Err(TreeReadFailure::Length { .. })));
    let f = installed(nested());
    tamper(&f, "tree/a/z", |p| std::fs::remove_file(p).unwrap());
    assert!(matches!(open(&f), Err(TreeReadFailure::Absent { .. })));
    let f = installed(nested());
    tamper(&f, "tree/a/z", |p| {
        std::fs::remove_file(p).unwrap();
        std::os::unix::fs::symlink("../a-x", p).unwrap();
    });
    assert!(matches!(open(&f), Err(TreeReadFailure::Type { .. })));
    // Nothing rewrote any of them: the refusals repaired nothing.
}

#[test]
fn ci_t17_structure_extra_absent_link_type_and_association() {
    let f = installed(nested());
    tamper(&f, "tree/lib/extra", |p| std::fs::write(p, b"x").unwrap());
    assert!(matches!(open(&f), Err(TreeReadFailure::Extra { .. })));
    let f = installed(vec![dir("empty", 0o755), file("f", 0o644, b"f")]);
    tamper(&f, "tree/empty", |p| std::fs::remove_dir(p).unwrap());
    assert!(matches!(open(&f), Err(TreeReadFailure::Absent { .. })));
    let f = installed(nested());
    tamper(&f, "tree/latest", |p| {
        std::fs::remove_file(p).unwrap();
        std::os::unix::fs::symlink("bin/other", p).unwrap();
    });
    assert!(matches!(open(&f), Err(TreeReadFailure::LinkTarget { .. })));
    let f = installed(nested());
    tamper(&f, "tree/lib", |p| {
        make_writable(p);
        std::fs::remove_dir_all(p).unwrap();
        std::fs::write(p, b"not a dir").unwrap();
    });
    assert!(matches!(open(&f), Err(TreeReadFailure::Type { .. })));
    let f = installed(nested());
    tamper(&f, "generation.json", |p| {
        let mut b = std::fs::read(p).unwrap();
        let at = b.len() - 3;
        b[at] = b'X';
        rewrite(p, &b);
    });
    assert!(matches!(open(&f), Err(TreeReadFailure::Association)));
}

#[test]
fn ci_t18_an_installed_mode_differing_from_ld_ci_10_refuses_mode() {
    let f = installed(nested());
    tamper(&f, "tree/bin/entry", |p| {
        std::fs::set_permissions(p, std::fs::Permissions::from_mode(0o700)).unwrap();
    });
    assert!(matches!(open(&f), Err(TreeReadFailure::Mode { .. })));
    let f = installed(nested());
    std::fs::set_permissions(
        f.generation().join("tree"),
        std::fs::Permissions::from_mode(0o700),
    )
    .unwrap();
    assert!(matches!(open(&f), Err(TreeReadFailure::Mode { row: None })));
}

#[test]
fn a_candidate_of_another_release_fails_association() {
    let f = installed(nested());
    let g = Fixture::new(vec![file("entry", 0o755, b"other")]);
    let candidate = g.candidate();
    let component = f.component.authenticated();
    let mut ledger = WorkLedger::snapshot_profile();
    let r = within(&mut ledger, |work| {
        open_retained_tree(
            &f.store,
            &component,
            &candidate,
            MACOS,
            PinRequest::UnderFence,
            work,
        )
        .map(|_| ())
    });
    assert!(matches!(r, Err(TreeReadFailure::Association)));
}

// ---- The pin (CI-T20) and the ephemeral path (CI-T15) ----

#[test]
fn ci_t20_a_pinned_generation_is_busy_for_gc_and_free_after_release() {
    let f = installed(nested());
    let pin_path = f.generation().join(crate::installation::PIN);
    let probe = |work: &mut WorkScope<'_>| {
        let dir = opensip_platform::RetainedDirectory::from_retained_handle(
            std::fs::File::open(f.generation()).unwrap(),
        )
        .unwrap();
        let file = ct::open_regular_no_follow(&dir, "pin.lock", Access::ReadOnly, work).unwrap();
        ct::try_pin(file, PinMode::Exclusive, work).unwrap().is_ok()
    };
    let mut ledger = WorkLedger::snapshot_profile();
    let busy = opened(&f, PinRequest::UnderFence, &mut ledger, |tree, work| {
        assert_eq!(tree.pin_mode(), PinMode::Shared);
        probe(work)
    })
    .unwrap();
    assert!(
        !busy,
        "GC's exclusive probe is busy while a capability is live"
    );
    let mut ledger = WorkLedger::snapshot_profile();
    let free = within(&mut ledger, probe);
    assert!(free, "the pin is released when the capability drops");
    assert!(pin_path.exists());
}

#[test]
fn a_missing_or_invalid_pin_file_fails_pin_and_is_never_recreated() {
    let f = installed(nested());
    tamper(&f, "pin.lock", |p| std::fs::remove_file(p).unwrap());
    assert!(matches!(open(&f), Err(TreeReadFailure::Pin)));
    assert!(
        !f.generation().join("pin.lock").exists(),
        "nothing recreates it"
    );
    let f = installed(nested());
    tamper(&f, "pin.lock", |p| std::fs::write(p, b"x").unwrap());
    assert!(matches!(open(&f), Err(TreeReadFailure::Pin)));
    let f = installed(nested());
    std::fs::set_permissions(
        f.generation().join("pin.lock"),
        std::fs::Permissions::from_mode(0o644),
    )
    .unwrap();
    assert!(matches!(open(&f), Err(TreeReadFailure::Pin)));
}

/// Every path and its bytes and modification times, recursively.
fn snapshot(root: &Path) -> Vec<(String, Vec<u8>, std::time::SystemTime)> {
    let mut out = Vec::new();
    let mut stack = vec![root.to_path_buf()];
    while let Some(p) = stack.pop() {
        let meta = std::fs::symlink_metadata(&p).unwrap();
        let bytes = if meta.is_file() {
            std::fs::read(&p).unwrap()
        } else {
            Vec::new()
        };
        out.push((
            p.to_string_lossy().into_owned(),
            bytes,
            meta.modified().unwrap(),
        ));
        if meta.is_dir() {
            for e in std::fs::read_dir(&p).unwrap() {
                stack.push(e.unwrap().path());
            }
        }
    }
    out.sort();
    out
}

#[test]
fn ci_t15_the_ephemeral_path_writes_nothing() {
    let f = installed(nested());
    let before = snapshot(&f.store_path);
    let mut ledger = WorkLedger::snapshot_profile();
    let got = opened(&f, PinRequest::Ephemeral, &mut ledger, |tree, work| {
        assert_eq!(tree.request(), PinRequest::Ephemeral);
        let mut sink = Sink::default();
        tree.transfer("a/b/c/deep.txt", &mut sink, work).unwrap();
        sink.committed
    })
    .unwrap();
    assert!(got.is_some());
    assert_eq!(
        snapshot(&f.store_path),
        before,
        "no byte, entry or time changed"
    );
}

// ---- The transfer (CI-T21; CI-T22's B_transfer half) ----

#[test]
fn ci_t21_transfer_delivers_exact_verified_bytes() {
    let f = installed(nested());
    let mut ledger = WorkLedger::snapshot_profile();
    opened(&f, PinRequest::UnderFence, &mut ledger, |tree, work| {
        for s in &f.specs {
            let SpecKind::File(bytes) = &s.kind else {
                continue;
            };
            let mut sink = Sink::default();
            tree.transfer(&s.path, &mut sink, work).unwrap();
            assert_eq!(
                sink.committed.as_deref(),
                Some(bytes.as_slice()),
                "{}",
                s.path
            );
            assert_eq!(sink.expected.unwrap().1, bytes.len() as u64);
            assert_eq!(sink.finished, vec![true]);
        }
        // A directory or symlink row is not a Blob.
        let mut sink = Sink::default();
        assert!(matches!(
            tree.transfer("latest", &mut sink, work),
            Err(TreeReadFailure::Association)
        ));
        assert!(matches!(
            tree.transfer("nowhere", &mut sink, work),
            Err(TreeReadFailure::Association)
        ));
        assert!(sink.committed.is_none());
    })
    .unwrap();
}

#[test]
fn ci_t21_a_file_changed_mid_transfer_fails_the_sink_commit() {
    let f = installed(nested());
    let mut ledger = WorkLedger::snapshot_profile();
    opened(&f, PinRequest::UnderFence, &mut ledger, |tree, work| {
        tamper(&f, "tree/a/b/c/deep.txt", |p| {
            let mut b = std::fs::read(p).unwrap();
            b[100_000] ^= 1;
            rewrite(p, &b);
        });
        let mut sink = Sink::default();
        assert!(matches!(
            tree.transfer("a/b/c/deep.txt", &mut sink, work),
            Err(TreeReadFailure::Digest { .. })
        ));
        assert!(sink.committed.is_none(), "nothing committed");
        assert_eq!(sink.finished, vec![false]);
    })
    .unwrap();
}

#[test]
fn ci_t22_transfer_charges_are_within_b_transfer_root_level_and_nested() {
    let f = installed(nested());
    let mut ledger = WorkLedger::snapshot_profile();
    opened(&f, PinRequest::UnderFence, &mut ledger, |tree, work| {
        for (path, k) in [("a-x", 1usize), ("a/b/c/deep.txt", 4)] {
            let SpecKind::File(bytes) = &f.specs.iter().find(|s| s.path == path).unwrap().kind
            else {
                panic!()
            };
            let before = work.used();
            let mut sink = Sink::default();
            tree.transfer(path, &mut sink, work).unwrap();
            let used = work.used();
            let bound = transfer_bound(f.specs.len(), path, bytes.len() as u64).unwrap();
            let charged = opensip_platform::WorkCost {
                objects: used.objects - before.objects,
                edges: used.edges - before.edges,
                bytes: used.bytes - before.bytes,
            };
            assert!(
                charged.edges <= bound.edges
                    && charged.objects == bound.objects
                    && charged.bytes == bound.bytes,
                "{path}"
            );
            // Exactly `k − 1` descents, each `desc`'s three objects.
            assert_eq!(charged.objects, 3 * (k - 1), "{path}");
        }
    })
    .unwrap();
}

// ---- CI-T22's B_open half ----

#[test]
fn ci_t22_open_charges_are_within_b_open_with_exact_fixed_rows() {
    let metadata_heavy = vec![
        dir("x", 0o755),
        dir("x/y", 0o755),
        file("x/y/e0", 0o644, b""),
        file("e1", 0o644, b""),
        link("l1", "e1"),
        link("x/l2", "y/e0"),
    ];
    for specs in [nested(), metadata_heavy] {
        let f = installed(specs);
        let candidate = f.candidate();
        let component = f.component.authenticated();
        let e = crate::installation::evidence(&component, &candidate, MACOS).unwrap();
        let bound = open_bound(&e.tree, e.record.length()).unwrap();
        let mut ledger = WorkLedger::snapshot_profile();
        opened(&f, PinRequest::UnderFence, &mut ledger, |_, _| ()).unwrap();
        let used = ledger.used();
        assert!(
            used.objects <= bound.objects && used.edges <= bound.edges && used.bytes <= bound.bytes
        );
        // Objects and bytes have no variable rows: they are exact.
        assert_eq!((used.objects, used.bytes), (bound.objects, bound.bytes));
    }
}

#[test]
fn ci_t12_only_the_trust_owner_or_a_fixture_constructs_the_evidence() {
    // An `AuthenticatedComponent` has no public constructor: only the trust
    // owner's reader lends one, from an admitted, unrevoked release, and the
    // capability takes nothing else. The fixture's `TestComponent` exists
    // only under the joint fixture predicate (gate 7). Revocation at R10a is
    // the reader's (C2a-4 with C2a-2's signed fixtures).
    let source = include_str!("../../security/src/trust_admitted_components.rs");
    assert!(source.contains("    pub(in crate::trust) fn new("));
    let retained = include_str!("retained_tree.rs");
    assert!(retained.contains("component: &AuthenticatedComponent<'a>,"));
}

#[test]
fn ci_t14_a_foreign_acl_on_a_generation_refuses_custody() {
    let f = installed(nested());
    let status = std::process::Command::new("/bin/chmod")
        .args(["+a", "everyone allow list"])
        .arg(f.generation())
        .status()
        .unwrap();
    assert!(status.success());
    assert!(matches!(open(&f), Err(TreeReadFailure::Custody(_))));
}

#[test]
fn a_candidate_of_another_platform_fails_association_at_the_open() {
    let f = Fixture::two_platforms(nested(), vec![file("only", 0o755, b"x86")]);
    f.install().unwrap();
    let other = f.candidate_for(opensip_security::SelectedPlatform {
        os: "macos",
        arch: "x86_64",
    });
    let component = f.component.authenticated();
    let mut ledger = WorkLedger::snapshot_profile();
    let r = within(&mut ledger, |work| {
        open_retained_tree(
            &f.store,
            &component,
            &other,
            MACOS,
            PinRequest::UnderFence,
            work,
        )
        .map(|_| ())
    });
    assert!(matches!(r, Err(TreeReadFailure::Association)), "{r:?}");
}

// ---- CI2-R1-RF-3: B_open's and B_transfer's rows, enumerated independently ----

/// LAW item 6's `B_open` rows with CI-A2-b and CI-A2-d, written out here
/// from the law's table rather than from `open_bound`: every object and
/// byte exactly, and every edge but the variable classes (comparisons and
/// read attempts), whose worst cases are returned separately.
fn open_rows(f: &Fixture) -> (opensip_platform::WorkCost, usize) {
    use crate::installation::{
        buffer_cost, custody_cost, descend_cost, envelope, index_buffer_cost, search_comparisons,
        sort_comparisons, times,
    };
    use opensip_security::snapshot_source::owned_record;
    let st = reference_status();
    let fopen = reference_regular_open();
    let one = ct::NATIVE_CALL;
    let mut total = opensip_platform::WorkCost::default();
    let mut add = |c: opensip_platform::WorkCost, k: usize| {
        total = total.checked_add(times(c, k).unwrap()).unwrap()
    };
    let n = f.specs.len();
    let d = f
        .specs
        .iter()
        .filter(|s| matches!(s.kind, SpecKind::Dir))
        .count();
    let files = f
        .specs
        .iter()
        .filter(|s| matches!(s.kind, SpecKind::File(_)))
        .count();
    let candidate = f.candidate();
    let component = f.component.authenticated();
    let r = crate::installation::evidence(&component, &candidate, MACOS)
        .unwrap()
        .record
        .length();
    add(custody_cost(), 2);
    add(owned_record(65), 1);
    add(descend_cost(64), 1);
    add(fopen, 2);
    add(one, 1);
    add(owned_record(r), 1);
    add(buffer_cost(), 1);
    add(descend_cost(4), 1);
    add(st, 1);
    add(index_buffer_cost(n).unwrap(), 2);
    add(one, n + 3 * (d + 1));
    add(st, n);
    add(capability_cost(), 1);
    let mut variable =
        envelope(r as u64) as usize + sort_comparisons(n).unwrap() + files * search_comparisons(n);
    for s in &f.specs {
        let name = s.path.rsplit('/').next().unwrap();
        match &s.kind {
            SpecKind::File(b) => {
                add(fopen, 1);
                variable += envelope(b.len() as u64) as usize;
            }
            SpecKind::Dir => add(descend_cost(name.len()), 1),
            SpecKind::Link(_) => {
                add(one, 1);
                add(owned_record(101), 1);
            }
        }
    }
    (total, variable)
}

#[test]
fn ci_t22_open_charges_match_an_independent_enumeration() {
    for specs in [
        nested(),
        vec![dir("x", 0o755), file("x/e", 0o644, b""), link("l", "x/e")],
    ] {
        let f = installed(specs);
        let mut ledger = WorkLedger::snapshot_profile();
        opened(&f, PinRequest::UnderFence, &mut ledger, |_, _| ()).unwrap();
        let used = ledger.used();
        let (fixed, variable) = open_rows(&f);
        assert_eq!((used.objects, used.bytes), (fixed.objects, fixed.bytes));
        assert!(
            used.edges >= fixed.edges && used.edges <= fixed.edges + variable,
            "{used:?} {fixed:?} {variable}"
        );
    }
}

#[test]
fn ci_t22_transfer_charges_match_an_independent_enumeration() {
    use crate::installation::{descend_cost, envelope, search_comparisons};
    let f = installed(nested());
    let mut ledger = WorkLedger::snapshot_profile();
    opened(&f, PinRequest::UnderFence, &mut ledger, |tree, work| {
        for s in &f.specs {
            let SpecKind::File(bytes) = &s.kind else {
                continue;
            };
            let before = work.used();
            tree.transfer(&s.path, &mut Sink::default(), work).unwrap();
            let used = work.used();
            // B_transfer(f): `k − 1` descents, one open, and the variable
            // lookup comparisons and read attempts.
            let mut fixed = ct::open_regular_no_follow_cost();
            let segments: Vec<&str> = s.path.split('/').collect();
            for seg in &segments[..segments.len() - 1] {
                fixed = fixed.checked_add(descend_cost(seg.len())).unwrap();
            }
            let variable =
                search_comparisons(f.specs.len()) + envelope(bytes.len() as u64) as usize;
            let charged = (
                used.objects - before.objects,
                used.edges - before.edges,
                used.bytes - before.bytes,
            );
            assert_eq!(
                (charged.0, charged.2),
                (fixed.objects, fixed.bytes),
                "{}",
                s.path
            );
            assert!(
                charged.1 >= fixed.edges && charged.1 <= fixed.edges + variable,
                "{}",
                s.path
            );
        }
    })
    .unwrap();
}

#[test]
fn ci_t22_live_handles_stay_bounded_on_open_and_transfer() {
    crate::installation::tests::isolated(
        "retained_tree::tests::ci_t22_live_handles_stay_bounded_on_open_and_transfer",
        open_handles,
    );
}
fn open_handles() {
    let f = installed(nested());
    let baseline = std::fs::read_dir("/dev/fd").unwrap().count();
    let peak = std::rc::Rc::new(std::cell::Cell::new(0usize));
    let p = peak.clone();
    crate::installation::tests::with_seam(
        move |step| {
            if step == "row" {
                p.set(p.get().max(std::fs::read_dir("/dev/fd").unwrap().count()));
            }
            Ok(())
        },
        || open(&f).unwrap(),
    );
    assert!(
        peak.get() <= baseline + 12,
        "peak {} over baseline {baseline}",
        peak.get()
    );
}

#[test]
fn a_failed_transfer_latches_its_cause_for_every_later_transfer() {
    let f = installed(nested());
    let mut ledger = WorkLedger::snapshot_profile();
    opened(&f, PinRequest::UnderFence, &mut ledger, |tree, work| {
        tamper(&f, "tree/a-x", |p| {
            let mut b = std::fs::read(p).unwrap();
            b[0] ^= 1;
            rewrite(p, &b);
        });
        let mut sink = Sink::default();
        let first = tree.transfer("a-x", &mut sink, work);
        assert!(matches!(first, Err(TreeReadFailure::Digest { .. })));
        // An intact file now refuses with the same, latched cause, and its
        // sink is told only that the transfer failed.
        let mut sink = Sink::default();
        let later = tree.transfer("bin/entry", &mut sink, work);
        assert!(
            matches!(later, Err(TreeReadFailure::Digest { .. })),
            "{later:?}"
        );
        assert_eq!(sink.finished, vec![false]);
        assert!(sink.expected.is_none() && sink.committed.is_none());
    })
    .unwrap();
}

// ---- Unit CI-3L (amendment CI-A3): the launch member, CI-T27 and CI-T28 ----

use crate::installation::tests::with_seam;
use opensip_platform::WorkCost;
use std::cell::Cell;
use std::os::unix::ffi::OsStrExt;
use std::os::unix::fs::MetadataExt;
use std::path::PathBuf;
use std::rc::Rc;

/// One launch's result, owned.
#[derive(Debug, Clone, PartialEq, Eq)]
struct Launched {
    path: PathBuf,
    device: u64,
    inode: u64,
    sha256: Option<[u8; 32]>,
    row: Option<u32>,
}
fn launched(m: LaunchMember<'_>) -> Launched {
    Launched {
        path: m.path().to_path_buf(),
        device: m.device(),
        inode: m.inode(),
        sha256: m.sha256(),
        row: m.row(),
    }
}
fn minus(after: WorkCost, before: WorkCost) -> WorkCost {
    WorkCost {
        objects: after.objects - before.objects,
        edges: after.edges - before.edges,
        bytes: after.bytes - before.bytes,
    }
}
fn sum(costs: &[WorkCost]) -> WorkCost {
    costs
        .iter()
        .fold(WorkCost::default(), |a, c| a.checked_add(*c).unwrap())
}
fn le(a: WorkCost, b: WorkCost) -> bool {
    a.objects <= b.objects && a.edges <= b.edges && a.bytes <= b.bytes
}

/// The pinned capability of `f`, opened on its own ledger: a launch's
/// scope is always another one.
fn capability<'s, 'a>(
    f: &'s Fixture,
    component: &AuthenticatedComponent<'a>,
    candidate: &'a ClosureCandidate<'_>,
) -> RetainedTree<'s, 'a> {
    within(&mut WorkLedger::snapshot_profile(), |work| {
        open_retained_tree(
            &f.store,
            component,
            candidate,
            MACOS,
            PinRequest::UnderFence,
            work,
        )
    })
    .unwrap()
}

/// What one launch did: its result, its exact charge on a fresh scope of
/// `ledger`, and the observations it made (read attempts, binding reads).
struct Run {
    result: Result<Launched, TreeReadFailure>,
    charged: WorkCost,
    reads: usize,
    lstats: usize,
}
fn launch_on(
    tree: &mut RetainedTree<'_, '_>,
    request: MemberRequest<'_>,
    ledger: &mut WorkLedger,
) -> Run {
    let reads = Rc::new(Cell::new(0usize));
    let lstats = Rc::new(Cell::new(0usize));
    let (r, l) = (reads.clone(), lstats.clone());
    let (result, charged) = with_seam(
        move |step| {
            match step {
                "read" => r.set(r.get() + 1),
                "lstat" => l.set(l.get() + 1),
                _ => {}
            }
            Ok(())
        },
        || {
            within(ledger, |work| {
                let before = work.used();
                let result = tree.launch_member(request, work).map(launched);
                (result, minus(work.used(), before))
            })
        },
    );
    Run {
        result,
        charged,
        reads: reads.get(),
        lstats: lstats.get(),
    }
}
fn launch(tree: &mut RetainedTree<'_, '_>, request: MemberRequest<'_>) -> Run {
    launch_on(tree, request, &mut WorkLedger::snapshot_profile())
}
/// The spelled launch path: `<storePath>/<closure2-hex>/tree[/<member>]`.
fn spelled(f: &Fixture, member: &str) -> PathBuf {
    let mut s = f.store_path.as_os_str().as_bytes().to_vec();
    s.extend_from_slice(b"/");
    s.extend_from_slice(f.name().as_bytes());
    s.extend_from_slice(b"/tree");
    if !member.is_empty() {
        s.extend_from_slice(b"/");
        s.extend_from_slice(member.as_bytes());
    }
    PathBuf::from(std::ffi::OsString::from(
        std::str::from_utf8(&s).unwrap().to_owned(),
    ))
}
fn row_of(f: &Fixture, path: &str) -> u32 {
    f.specs.iter().position(|s| s.path == path).unwrap() as u32
}
fn digest_of(f: &Fixture, path: &str) -> [u8; 32] {
    let SpecKind::File(bytes) = &f.specs[row_of(f, path) as usize].kind else {
        panic!("{path}")
    };
    opensip_identity::raw_sha256(bytes)
}

// ---- The independent enumerator (CI-T28) ----

/// The component sequence order, written here as a lexicographic order of
/// the `/`-separated segment lists (not the module's byte key).
fn segments_cmp(a: &str, b: &str) -> std::cmp::Ordering {
    let (a, b): (Vec<&[u8]>, Vec<&[u8]>) = (
        a.split('/').map(str::as_bytes).collect(),
        b.split('/').map(str::as_bytes).collect(),
    );
    a.cmp(&b)
}
/// The retained index as this enumerator orders it.
fn index_of(specs: &[Spec]) -> Vec<usize> {
    let mut order: Vec<usize> = (0..specs.len()).collect();
    order.sort_by(|&x, &y| segments_cmp(&specs[x].path, &specs[y].path));
    order
}
/// One binary search over `order`: the row found and the comparisons made.
fn search(specs: &[Spec], order: &[usize], path: &str) -> (Option<usize>, usize) {
    let (mut low, mut high, mut made) = (0usize, order.len(), 0usize);
    while low < high {
        let mid = low + (high - low) / 2;
        made += 1;
        match segments_cmp(&specs[order[mid]].path, path) {
            std::cmp::Ordering::Less => low = mid + 1,
            std::cmp::Ordering::Greater => high = mid,
            std::cmp::Ordering::Equal => return (Some(order[mid]), made),
        }
    }
    (None, made)
}
fn edge() -> WorkCost {
    WorkCost {
        objects: 0,
        edges: 1,
        bytes: 0,
    }
}
fn owned(bytes: usize) -> WorkCost {
    WorkCost {
        objects: 1,
        edges: 0,
        bytes,
    }
}
// Published CI-A2/CI-A3 primitive expressions, enumerated independently.
// Type sizes are measured here; no production cost function supplies a price.
// Independent Darwin SDK C sizeof(struct stat), rechecked by the owning lane.
const REFERENCE_NATIVE_STAT_BYTES: usize = 144;
fn reference_status() -> WorkCost {
    WorkCost {
        objects: 0,
        edges: 1,
        bytes: REFERENCE_NATIVE_STAT_BYTES.max(size_of::<std::fs::Metadata>()),
    }
}
fn reference_regular_open() -> WorkCost {
    WorkCost {
        objects: 0,
        edges: 2,
        bytes: REFERENCE_NATIVE_STAT_BYTES.max(size_of::<std::fs::Metadata>()),
    }
}
fn descent(name: usize) -> WorkCost {
    WorkCost {
        objects: 3,
        edges: 3,
        bytes: name + 1 + 4 * size_of::<crate::installation::Level>(),
    }
}
/// `⌈log₂ n⌉ + 1`, counted here.
fn search_envelope(n: usize) -> usize {
    let mut bits = 0;
    while (1usize << bits) < n {
        bits += 1;
    }
    bits + 1
}
/// `env(c)`: `2·⌈c / 64 KiB⌉ + 2`.
fn read_envelope(c: usize) -> usize {
    2 * c.div_ceil(65_536) + 2
}

/// CI-A3-b's rows for `request`, from the TreeCommitment and the store path
/// themselves, in execution order: the executed charges (`E_launch`, with
/// the observed counts), the per-member bound (`B_launch`) and the request
/// pre-bound (`B̂_launch`).
struct Expected {
    charges: Vec<WorkCost>,
    reads: usize,
    bound: WorkCost,
    pre_bound: WorkCost,
    /// The final row, or `None` when no member resolved.
    row: Option<Option<usize>>,
    lookup_trace: Vec<(String, usize)>,
    hop_lengths: Vec<usize>,
}
fn expected(f: &Fixture, entry: &str, request: MemberRequest<'_>) -> Expected {
    expected_specs(&f.specs, f.store_path.as_os_str().len(), entry, request)
}
fn expected_specs(
    specs: &[Spec],
    store: usize,
    entry: &str,
    request: MemberRequest<'_>,
) -> Expected {
    let st = reference_status();
    let fopen = reference_regular_open();
    let lm = owned(size_of::<LaunchMember<'static>>());
    let launch_path = |p: usize| owned(store + 1 + 64 + 1 + 4 + if p > 0 { 1 + p } else { 0 } + 1);
    let is_file = |s: &Spec| matches!(s.kind, SpecKind::File(_));
    let is_dir = |s: &Spec| matches!(s.kind, SpecKind::Dir);
    let wants_file = !matches!(request, MemberRequest::Directory(_));
    let of_kind = |s: &Spec| if wants_file { is_file(s) } else { is_dir(s) };
    let links = specs
        .iter()
        .filter(|s| matches!(s.kind, SpecKind::Link(_)))
        .count();
    let joined = |link: &str, target: &str| match link.rsplit_once('/') {
        Some((parent, _)) => format!("{parent}/{target}"),
        None => target.to_owned(),
    };
    // B̂: maxima over the requested kind's rows, 0 over an empty set.
    let pre_bound = if request == MemberRequest::Directory("") {
        sum(&[st, launch_path(0), st, lm])
    } else if !specs.iter().any(of_kind) {
        edge()
    } else {
        let rows: Vec<&Spec> = specs.iter().filter(|s| of_kind(s)).collect();
        let p = rows.iter().map(|s| s.path.len()).max().unwrap();
        let k = rows
            .iter()
            .map(|s| s.path.split('/').count())
            .max()
            .unwrap();
        let seg = rows
            .iter()
            .flat_map(|s| s.path.split('/'))
            .map(str::len)
            .max()
            .unwrap();
        let c = rows
            .iter()
            .map(|s| match &s.kind {
                SpecKind::File(b) => b.len(),
                _ => 0,
            })
            .max()
            .unwrap();
        let q = specs
            .iter()
            .filter_map(|s| match &s.kind {
                SpecKind::Link(t) => Some(joined(&s.path, t).len()),
                _ => None,
            })
            .max()
            .unwrap_or(0);
        let mut b = vec![edge()];
        b.extend(std::iter::repeat_n(
            edge(),
            (links + 1) * search_envelope(specs.len()),
        ));
        b.extend(std::iter::repeat_n(owned(q), links));
        if wants_file {
            b.extend(std::iter::repeat_n(descent(seg), k - 1));
            b.push(fopen);
            b.extend(std::iter::repeat_n(edge(), read_envelope(c)));
        } else {
            b.extend(std::iter::repeat_n(descent(seg), k));
            b.push(st);
        }
        b.extend([launch_path(p), st, lm]);
        sum(&b)
    };
    let mut charges = Vec::new();
    let mut bound = Vec::new();
    let mut lookup_trace = Vec::new();
    let mut hop_lengths = Vec::new();
    fn both(c: WorkCost, charges: &mut Vec<WorkCost>, bound: &mut Vec<WorkCost>) {
        charges.push(c);
        bound.push(c);
    }
    let stop =
        |charges: Vec<WorkCost>, bound: Vec<WorkCost>, row, lookup_trace, hop_lengths| Expected {
            reads: 0,
            bound: sum(&bound),
            charges,
            pre_bound,
            row,
            lookup_trace,
            hop_lengths,
        };
    let final_row = if request == MemberRequest::Directory("") {
        None
    } else {
        both(edge(), &mut charges, &mut bound);
        if !specs.iter().any(of_kind) {
            return stop(charges, bound, None, lookup_trace, hop_lengths);
        }
        let order = index_of(specs);
        let mut path = match request {
            MemberRequest::Entrypoint => entry.to_owned(),
            MemberRequest::File(p) | MemberRequest::Directory(p) => p.to_owned(),
        };
        let mut lookups = 0;
        let mut search_bound = 0;
        let found = loop {
            if lookups == links + 1 {
                break None;
            }
            lookups += 1;
            let (row, made) = search(specs, &order, &path);
            lookup_trace.push((path.clone(), made));
            charges.extend(std::iter::repeat_n(edge(), made));
            search_bound += search_envelope(specs.len());
            let Some(row) = row else { break None };
            match &specs[row].kind {
                SpecKind::Link(target) => {
                    if lookups > links {
                        break None;
                    }
                    path = joined(&specs[row].path, target);
                    hop_lengths.push(path.len());
                    both(owned(path.len()), &mut charges, &mut bound);
                }
                _ if of_kind(&specs[row]) => break Some(row),
                _ => break None,
            }
        };
        bound.extend(std::iter::repeat_n(edge(), search_bound));
        let Some(row) = found else {
            return stop(charges, bound, None, lookup_trace, hop_lengths);
        };
        Some(row)
    };
    let member = final_row.map_or("", |r| specs[r].path.as_str());
    let segments: Vec<&str> = if member.is_empty() {
        vec![]
    } else {
        member.split('/').collect()
    };
    let mut reads = 0;
    if wants_file {
        for seg in &segments[..segments.len() - 1] {
            both(descent(seg.len()), &mut charges, &mut bound);
        }
        both(fopen, &mut charges, &mut bound);
        let SpecKind::File(bytes) = &specs[final_row.unwrap()].kind else {
            panic!()
        };
        // The recorded read returns: full chunks, the remainder, then the end.
        reads = bytes.len().div_ceil(65_536) + 1;
        charges.extend(std::iter::repeat_n(edge(), reads));
        bound.extend(std::iter::repeat_n(edge(), read_envelope(bytes.len())));
    } else {
        for seg in &segments {
            both(descent(seg.len()), &mut charges, &mut bound);
        }
        both(st, &mut charges, &mut bound);
    }
    for c in [launch_path(member.len()), st, lm] {
        both(c, &mut charges, &mut bound);
    }
    Expected {
        reads,
        bound: sum(&bound),
        charges,
        pre_bound,
        row: Some(final_row),
        lookup_trace,
        hop_lengths,
    }
}

/// A run's work equals the enumerated executed charge exactly, and
/// `E ≤ B ≤ B̂` holds with the module's pre-bound equal to the enumerated one.
fn check_work(f: &Fixture, entry: &str, request: MemberRequest<'_>) -> Run {
    let (candidate, component) = (f.candidate(), f.component.authenticated());
    let mut tree = capability(f, &component, &candidate);
    let want = expected(f, entry, request);
    let run = launch(&mut tree, request);
    let e = sum(&want.charges);
    assert_eq!(run.charged, e, "{request:?}: actual = E_launch");
    assert_eq!(run.reads, want.reads, "{request:?}: read attempts");
    assert!(le(e, want.bound), "{request:?}: E ≤ B");
    assert!(le(want.bound, want.pre_bound), "{request:?}: B ≤ B̂");
    assert_eq!(
        tree.launch_pre_bound(request),
        Some(want.pre_bound),
        "{request:?}: B̂"
    );
    match (&run.result, want.row) {
        (Ok(m), Some(row)) => assert_eq!(m.row, row.map(|r| r as u32)),
        (Err(TreeReadFailure::Association), None) => {}
        (r, row) => panic!("{request:?}: {r:?} against {row:?}"),
    }
    run
}

// ---- CI-T27: resolution, observation, binding, directories, lifetime, latching ----

#[test]
fn ci_t27_entrypoints_resolve_to_the_final_file_row_at_root_nested_and_through_links() {
    // Root-level, and nested.
    for (specs, entry) in [(file_only(), "entry"), (nested(), "bin/entry")] {
        let f = installed(specs);
        let (candidate, component) = (f.candidate(), f.component.authenticated());
        let mut tree = capability(&f, &component, &candidate);
        let m = launch(&mut tree, MemberRequest::Entrypoint).result.unwrap();
        assert_eq!(m.path, spelled(&f, entry));
        assert_eq!(m.row, Some(row_of(&f, entry)));
        assert_eq!(m.sha256, Some(digest_of(&f, entry)));
        let meta = std::fs::symlink_metadata(&m.path).unwrap();
        assert!(meta.is_file());
        assert_eq!((m.device, m.inode), (meta.dev(), meta.ino()));
    }
    // Through one link, and through two: the result is the final file row,
    // and the path holds no link.
    let mut two = nested();
    two.push(link("again", "latest"));
    // A validated toolchain's entrypoint names its file row directly, and C2a-1's
    // candidate admits no analyzer fixture, so the installed chains are
    // requested as `File` members, which follow links by the same rule; the
    // `Entrypoint` chain is resolved over a hand-built TreeCommitment below.
    for (specs, entry) in [(nested(), "latest"), (two, "again")] {
        let f = installed(specs);
        let (candidate, component) = (f.candidate(), f.component.authenticated());
        let mut tree = capability(&f, &component, &candidate);
        let m = launch(&mut tree, MemberRequest::File(entry))
            .result
            .unwrap();
        assert_eq!(m.path, spelled(&f, "bin/entry"), "{entry}");
        assert_eq!(m.row, Some(row_of(&f, "bin/entry")));
        assert_eq!(m.sha256, Some(digest_of(&f, "bin/entry")));
        // No component below the store is a link.
        let mut walked = f.store_path.clone();
        for part in m.path.strip_prefix(&f.store_path).unwrap().components() {
            walked.push(part);
            assert!(!std::fs::symlink_metadata(&walked).unwrap().is_symlink());
        }
    }
    let (r, charged) = resolve_over(
        &[
            ("l2", "symlink", Some("l1")),
            ("l1", "symlink", Some("f")),
            ("f", "file", None),
        ],
        MemberRequest::Entrypoint,
    );
    assert_eq!(
        r.unwrap(),
        2,
        "the entrypoint `l2` resolves to the file row"
    );
    assert_eq!(
        (charged.objects, charged.bytes),
        (2, 3),
        "the two joined paths are `l1` (two bytes) and `f` (one byte)"
    );
}

/// The capability's own tree over a hand-built TreeCommitment, for the
/// resolution rules a validated manifest cannot reach (a cycle).
fn manifest_over(entries: &[(&str, &str, Option<&str>)]) -> opensip_identity::JsonValue {
    use opensip_identity::JsonValue as V;
    use std::collections::BTreeMap;
    let s = |t: &str| V::String(t.to_owned());
    let rows: Vec<V> = entries
        .iter()
        .map(|(path, kind, target)| {
            let mut e = BTreeMap::new();
            e.insert("path".to_owned(), s(path));
            e.insert("mode".to_owned(), s("0755"));
            e.insert("type".to_owned(), s(kind));
            match *kind {
                "file" => {
                    e.insert(
                        "length".to_owned(),
                        V::Integer(opensip_identity::JsonInteger::new(0).unwrap()),
                    );
                    e.insert("sha256".to_owned(), s(&"0".repeat(64)));
                }
                "symlink" => {
                    e.insert("target".to_owned(), s(target.unwrap()));
                }
                _ => {}
            }
            V::Object(e)
        })
        .collect();
    let mut tree = BTreeMap::new();
    tree.insert("entries".to_owned(), V::Array(rows));
    let mut platform = BTreeMap::new();
    platform.insert("os".to_owned(), s("macos"));
    platform.insert("arch".to_owned(), s("arm64"));
    platform.insert("entrypoint".to_owned(), s(entries[0].0));
    platform.insert("tree".to_owned(), V::Object(tree));
    let mut manifest = BTreeMap::new();
    manifest.insert("platforms".to_owned(), V::Array(vec![V::Object(platform)]));
    V::Object(manifest)
}
fn resolve_over(
    entries: &[(&str, &str, Option<&str>)],
    request: MemberRequest<'_>,
) -> (Result<u32, TreeReadFailure>, WorkCost) {
    let manifest = manifest_over(entries);
    let tree = crate::installation::Tree::of(&manifest, MACOS).unwrap();
    let mut ledger = WorkLedger::snapshot_profile();
    within(&mut ledger, |work| {
        let order = crate::installation::charged_sort::<TreeFault>(tree.n, work, |a, b| {
            crate::installation::component_cmp(tree.row(a).path, tree.row(b).path).is_lt()
        })
        .unwrap();
        let before = work.used();
        let r = resolve(&tree, &order, request, work);
        (r, minus(work.used(), before))
    })
}

#[test]
fn ci_t27_a_chain_beyond_s_plus_one_lookups_or_of_the_wrong_kind_refuses_association() {
    // A cycle (S = 2): three lookups follow a, b, a; a fourth is never made.
    let (r, charged) = resolve_over(
        &[
            ("a", "symlink", Some("b")),
            ("b", "symlink", Some("a")),
            ("f", "file", None),
        ],
        MemberRequest::File("a"),
    );
    assert!(matches!(r, Err(TreeReadFailure::Association)), "{r:?}");
    // Three lookups (a, b, a), but only S = 2 joined temporaries.
    // A link found on the last permitted lookup must refuse before another
    // allocation: the refusal prefix stays within the S-hop pre-bound.
    assert_eq!(charged.objects, 2, "at most S hop temporaries");
    assert_eq!(charged.bytes, 2);
    // An acyclic chain resolves; a request of the wrong kind refuses.
    let entries = [
        ("f", "file", None),
        ("d", "dir", None),
        ("l", "symlink", Some("f")),
    ];
    assert_eq!(
        resolve_over(&entries, MemberRequest::File("l")).0.unwrap(),
        0
    );
    for request in [
        MemberRequest::File("d"),
        MemberRequest::Directory("f"),
        MemberRequest::Directory("l"),
        MemberRequest::File("none"),
    ] {
        assert!(matches!(
            resolve_over(&entries, request).0,
            Err(TreeReadFailure::Association)
        ));
    }
    let f = installed(nested());
    let (candidate, component) = (f.candidate(), f.component.authenticated());
    let mut tree = capability(&f, &component, &candidate);
    assert!(matches!(
        launch(&mut tree, MemberRequest::File("lib")).result,
        Err(TreeReadFailure::Association)
    ));
}

#[test]
fn ci_t27_the_member_is_observed_from_the_retained_base_and_keeps_its_cause() {
    type Change = fn(&Path);
    type MatchesFailure = fn(&TreeReadFailure) -> bool;
    let cases: [(Change, MatchesFailure); 5] = [
        (
            |p| {
                let mut b = std::fs::read(p).unwrap();
                b[100] ^= 1;
                rewrite(p, &b);
            },
            |e| matches!(e, TreeReadFailure::Digest { .. }),
        ),
        (
            |p| rewrite(p, b"short"),
            |e| matches!(e, TreeReadFailure::Length { .. }),
        ),
        (
            |p| std::fs::set_permissions(p, std::fs::Permissions::from_mode(0o700)).unwrap(),
            |e| matches!(e, TreeReadFailure::Mode { .. }),
        ),
        (
            |p| {
                std::fs::remove_file(p).unwrap();
                std::fs::create_dir(p).unwrap();
            },
            |e| matches!(e, TreeReadFailure::Type { .. }),
        ),
        (
            |p| std::fs::remove_file(p).unwrap(),
            |e| matches!(e, TreeReadFailure::Absent { .. }),
        ),
    ];
    for (change, expect) in cases {
        let f = installed(nested());
        let (candidate, component) = (f.candidate(), f.component.authenticated());
        let mut tree = capability(&f, &component, &candidate);
        tamper(&f, "tree/a/z", change);
        let run = launch(&mut tree, MemberRequest::File("a/z"));
        let e = run.result.unwrap_err();
        assert!(expect(&e), "{e:?}");
        assert_eq!(run.lstats, 0, "no binding without a verified member");
    }
}

#[test]
fn ci_t27_the_launch_reads_only_through_retained_single_component_handles() {
    // A source pin over the launch member's code: no path-based filesystem
    // call; each descent and open names one component from a retained handle.
    let source = include_str!("retained_tree.rs");
    let at = source
        .find("// ---- The launch member (CI-A3; unit CI-3L) ----")
        .unwrap();
    let end = at + source[at..].find("#[cfg(test)]\n#[path").unwrap();
    let code = &source[at..end];
    for forbidden in [
        "std::fs",
        "File::open",
        "OpenOptions",
        "open_child_directory",
        "canonicalize",
        "read_link",
        "metadata(",
        "Command",
        "spawn",
    ] {
        assert!(!code.contains(forbidden), "{forbidden}");
    }
    assert_eq!(code.matches("ct::path_status_no_follow(").count(), 1);
    assert!(code.contains("for segment in member.split('/').take(descents)"));
}

/// Move the generation's `tree/` aside, leaving the retained handles on it,
/// and put a fresh `tree/` at its spelling, built by `build`.
fn swap_tree(f: &Fixture, build: impl FnOnce(&Path, &Path)) {
    let generation = f.generation();
    let mode = std::fs::metadata(&generation).unwrap().permissions().mode() & 0o7777;
    std::fs::set_permissions(&generation, std::fs::Permissions::from_mode(0o700)).unwrap();
    let aside = generation.join("tree.aside");
    std::fs::rename(generation.join("tree"), &aside).unwrap();
    std::fs::create_dir(generation.join("tree")).unwrap();
    build(&aside, &generation.join("tree"));
    std::fs::set_permissions(&generation, std::fs::Permissions::from_mode(mode)).unwrap();
}

#[test]
fn ci_t27_a_path_not_naming_the_verified_member_refuses_binding() {
    // The final component a symlink to an identical copy.
    let f = installed(nested());
    let (candidate, component) = (f.candidate(), f.component.authenticated());
    let mut tree = capability(&f, &component, &candidate);
    swap_tree(&f, |aside, fresh| {
        std::fs::create_dir(fresh.join("bin")).unwrap();
        std::fs::copy(aside.join("bin/entry"), fresh.join("copy")).unwrap();
        std::os::unix::fs::symlink("../copy", fresh.join("bin/entry")).unwrap();
    });
    let run = launch(&mut tree, MemberRequest::Entrypoint);
    assert!(
        matches!(run.result, Err(TreeReadFailure::Binding)),
        "{:?}",
        run.result
    );
    // An identical regular copy at the spelling: same bytes, another inode.
    let f = installed(nested());
    let (candidate, component) = (f.candidate(), f.component.authenticated());
    let mut tree = capability(&f, &component, &candidate);
    swap_tree(&f, |aside, fresh| {
        std::fs::create_dir(fresh.join("bin")).unwrap();
        std::fs::copy(aside.join("bin/entry"), fresh.join("bin/entry")).unwrap();
    });
    let run = launch(&mut tree, MemberRequest::Entrypoint);
    assert!(matches!(run.result, Err(TreeReadFailure::Binding)));
    // A store path naming another directory: an identical copy elsewhere
    // (another inode), nothing there (ENOENT) and a regular file (ENOTDIR).
    let f = installed(nested());
    let elsewhere = f.store_path.with_file_name("elsewhere");
    let copy = elsewhere.join(f.name()).join("tree/bin");
    std::fs::create_dir_all(&copy).unwrap();
    std::fs::copy(f.generation().join("tree/bin/entry"), copy.join("entry")).unwrap();
    let plain = f.store_path.with_file_name("plain");
    std::fs::write(&plain, b"x").unwrap();
    for store_path in [elsewhere, f.store_path.with_file_name("nothing"), plain] {
        let handle = opensip_platform::RetainedDirectory::from_retained_handle(
            std::fs::File::open(&f.store_path).unwrap(),
        )
        .unwrap();
        let uid = std::fs::metadata(&f.store_path).unwrap().uid();
        let store = within(&mut WorkLedger::new(), |work| {
            ComponentStore::fixture(handle, &store_path, uid, work)
        })
        .unwrap();
        let (candidate, component) = (f.candidate(), f.component.authenticated());
        let mut tree = within(&mut WorkLedger::snapshot_profile(), |work| {
            open_retained_tree(
                &store,
                &component,
                &candidate,
                MACOS,
                PinRequest::UnderFence,
                work,
            )
        })
        .unwrap();
        let run = launch(&mut tree, MemberRequest::Entrypoint);
        assert!(
            matches!(run.result, Err(TreeReadFailure::Binding)),
            "{store_path:?}: {:?}",
            run.result
        );
        assert_eq!(run.lstats, 1);
    }
}

#[test]
fn ci_t27_directory_members_give_their_identity_and_mode_and_read_no_content() {
    let f = installed(nested());
    let (candidate, component) = (f.candidate(), f.component.authenticated());
    let mut tree = capability(&f, &component, &candidate);
    for (request, member) in [
        (MemberRequest::Directory(""), ""),
        (MemberRequest::Directory("a/b/c"), "a/b/c"),
        (MemberRequest::Directory("lib"), "lib"),
    ] {
        let run = launch(&mut tree, request);
        let m = run.result.unwrap();
        let meta = std::fs::symlink_metadata(spelled(&f, member)).unwrap();
        assert!(meta.is_dir());
        assert_eq!((m.device, m.inode), (meta.dev(), meta.ino()));
        assert_eq!(m.path, spelled(&f, member));
        assert_eq!(m.sha256, None);
        assert_eq!(m.row, (!member.is_empty()).then(|| row_of(&f, member)));
        assert_eq!(run.reads, 0, "no content read");
    }
    // A changed directory mode refuses `Mode`; `tree/`'s own, with no row.
    let f = installed(nested());
    let (candidate, component) = (f.candidate(), f.component.authenticated());
    let mut tree = capability(&f, &component, &candidate);
    std::fs::set_permissions(
        f.generation().join("tree/a/b/c"),
        std::fs::Permissions::from_mode(0o700),
    )
    .unwrap();
    assert!(matches!(
        launch(&mut tree, MemberRequest::Directory("a/b/c")).result,
        Err(TreeReadFailure::Mode { row: Some(_) })
    ));
    let f = installed(nested());
    let (candidate, component) = (f.candidate(), f.component.authenticated());
    let mut tree = capability(&f, &component, &candidate);
    std::fs::set_permissions(
        f.generation().join("tree"),
        std::fs::Permissions::from_mode(0o700),
    )
    .unwrap();
    assert!(matches!(
        launch(&mut tree, MemberRequest::Directory("")).result,
        Err(TreeReadFailure::Mode { row: None })
    ));
}

#[test]
fn ci_t27_the_pinned_generation_survives_gc_across_a_spawn_of_its_member() {
    let f = installed(nested());
    let probe = || {
        within(&mut WorkLedger::snapshot_profile(), |work| {
            let dir = opensip_platform::RetainedDirectory::from_retained_handle(
                std::fs::File::open(f.generation()).unwrap(),
            )
            .unwrap();
            let file =
                ct::open_regular_no_follow(&dir, "pin.lock", Access::ReadOnly, work).unwrap();
            ct::try_pin(file, PinMode::Exclusive, work).unwrap().is_ok()
        })
    };
    let (candidate, component) = (f.candidate(), f.component.authenticated());
    let mut tree = capability(&f, &component, &candidate);
    let m = launch(&mut tree, MemberRequest::Entrypoint).result.unwrap();
    assert!(!probe(), "GC's exclusive probe is busy before the spawn");
    let status = std::process::Command::new(&m.path).status().unwrap();
    assert!(status.success());
    assert!(
        !probe(),
        "and after the child settled, while the capability lives"
    );
    drop(tree);
    assert!(
        probe(),
        "the pin is released only when the capability drops"
    );
}

#[test]
fn ci_t27_every_failure_latches_across_launch_and_transfer() {
    // A launch after a failed transfer.
    let f = installed(nested());
    let (candidate, component) = (f.candidate(), f.component.authenticated());
    let mut tree = capability(&f, &component, &candidate);
    tamper(&f, "tree/a-x", |p| {
        let mut b = std::fs::read(p).unwrap();
        b[0] ^= 1;
        rewrite(p, &b);
    });
    let mut ledger = WorkLedger::snapshot_profile();
    let first = within(&mut ledger, |work| {
        tree.transfer("a-x", &mut Sink::default(), work)
    });
    assert!(matches!(first, Err(TreeReadFailure::Digest { .. })));
    let run = launch(&mut tree, MemberRequest::Entrypoint);
    assert!(
        matches!(run.result, Err(TreeReadFailure::Digest { .. })),
        "{:?}",
        run.result
    );
    assert_eq!(
        (run.charged, run.reads, run.lstats),
        (WorkCost::default(), 0, 0)
    );
    // A transfer after a failed launch, and a later launch.
    let f = installed(nested());
    let (candidate, component) = (f.candidate(), f.component.authenticated());
    let mut tree = capability(&f, &component, &candidate);
    assert!(matches!(
        launch(&mut tree, MemberRequest::File("nowhere")).result,
        Err(TreeReadFailure::Association)
    ));
    let mut sink = Sink::default();
    let mut ledger = WorkLedger::snapshot_profile();
    let (later, charged) = within(&mut ledger, |work| {
        let before = work.used();
        let r = tree.transfer("bin/entry", &mut sink, work);
        (r, minus(work.used(), before))
    });
    assert!(matches!(later, Err(TreeReadFailure::Association)));
    assert_eq!(charged, WorkCost::default());
    assert!(sink.expected.is_none() && sink.committed.is_none());
    // `Budget`: exhausted on one scope, then refused on a fresh funded one
    // with `Budget(Closed)`, no charge and no observation.
    let f = installed(nested());
    let (candidate, component) = (f.candidate(), f.component.authenticated());
    let mut tree = capability(&f, &component, &candidate);
    let mut starved = WorkLedger::with_limits(WorkCost {
        objects: 1 << 16,
        edges: 3,
        bytes: 1 << 28,
    })
    .unwrap();
    let run = launch_on(&mut tree, MemberRequest::Entrypoint, &mut starved);
    assert!(matches!(run.result, Err(TreeReadFailure::Budget(_))));
    let run = launch(&mut tree, MemberRequest::Entrypoint);
    assert!(
        matches!(
            run.result,
            Err(TreeReadFailure::Budget(WorkBudgetError::Closed))
        ),
        "{:?}",
        run.result
    );
    assert_eq!(
        (run.charged, run.reads, run.lstats),
        (WorkCost::default(), 0, 0)
    );
    let mut sink = Sink::default();
    let mut ledger = WorkLedger::snapshot_profile();
    let (later, charged) = with_seam(
        |step| {
            assert_ne!(step, "read", "no observation");
            Ok(())
        },
        || {
            within(&mut ledger, |work| {
                let before = work.used();
                let r = tree.transfer("bin/entry", &mut sink, work);
                (r, minus(work.used(), before))
            })
        },
    );
    assert!(matches!(
        later,
        Err(TreeReadFailure::Budget(WorkBudgetError::Closed))
    ));
    assert_eq!(charged, WorkCost::default());
}

// ---- CI-T28: exact executed work, bounds, exhaustion and the partition ----

/// A zero-length file under a long path, a large file under a short one,
/// two hops of different joined lengths to a nested member, nested
/// directories, and an empty and a one-chunk file (`nested`'s `a/b/empty`
/// and `a/z`).
fn shapes() -> Vec<Spec> {
    let mut specs = nested();
    let long = [
        "d0123456789abcdef",
        "e0123456789abcdef",
        "f0123456789abcdef",
        "g0123456789abcdef",
    ];
    let mut path = String::new();
    for seg in long {
        if !path.is_empty() {
            path.push('/');
        }
        path.push_str(seg);
        specs.push(dir(&path, 0o755));
    }
    specs.push(file(&format!("{path}/zero"), 0o644, b""));
    specs.push(file("big", 0o644, &vec![7u8; 300_000]));
    specs.push(link("hop", "a/second"));
    specs.push(link("a/second", "b/c/deep.txt"));
    specs
}

#[test]
fn ci_t28_actual_charges_equal_e_launch_and_e_le_b_le_b_hat_for_every_shape() {
    let f = installed(shapes());
    let deep = format!(
        "{}/zero",
        "d0123456789abcdef/e0123456789abcdef/f0123456789abcdef/g0123456789abcdef"
    );
    let requests = [
        MemberRequest::Entrypoint,
        MemberRequest::File(&deep),
        MemberRequest::File("big"),
        MemberRequest::File("hop"),
        MemberRequest::File("a/b/empty"),
        MemberRequest::File("a/z"),
        MemberRequest::File("a-x"),
        MemberRequest::File("lib/provider.js"),
        MemberRequest::File("nowhere"),
        MemberRequest::Directory("a/b/c"),
        MemberRequest::Directory(""),
    ];
    // The lookups' search depths differ: the first probe, an intermediate
    // one, the last, and a miss all occur among these requests.
    let order = index_of(&f.specs);
    let mut depths = std::collections::BTreeSet::new();
    for request in requests {
        let run = check_work(&f, "bin/entry", request);
        if let MemberRequest::File(p) | MemberRequest::Directory(p) = request
            && !p.is_empty()
        {
            depths.insert(search(&f.specs, &order, p).1);
        }
        if let Ok(m) = &run.result {
            assert!(m.path.starts_with(&f.store_path));
        }
    }
    assert!(depths.len() >= 3, "{depths:?}");
    // The empty file is one attempt, the one-chunk file two.
    assert_eq!(
        expected(&f, "bin/entry", MemberRequest::File("a/b/empty")).reads,
        1
    );
    assert_eq!(
        expected(&f, "bin/entry", MemberRequest::File("a/z")).reads,
        2
    );
    // The hops' joined paths differ from each other and from the request.
    assert_ne!("a/second".len(), "a/b/c/deep.txt".len());
    assert_ne!("hop".len(), "a/second".len());
}

#[test]
fn ci_t28_a_kind_with_no_rows_refuses_at_the_kind_check_after_one_edge() {
    let f = installed(vec![file("f", 0o755, b"x"), link("l", "f")]);
    let run = check_work(&f, "f", MemberRequest::Directory("l"));
    assert!(matches!(run.result, Err(TreeReadFailure::Association)));
    assert_eq!(run.charged, edge());
    assert_eq!((run.reads, run.lstats), (0, 0));
    let f = installed(file_only());
    let run = check_work(&f, "entry", MemberRequest::Directory("x"));
    assert_eq!(run.charged, edge());
}

#[test]
fn ci_t28_a_scope_one_unit_short_before_each_actual_charge_refuses_budget_there() {
    // A one-unit pad is charged first, so every limit is positive (`with_limits`
    // admits no zero); the other dimensions get `WorkLedger::new()`'s limits
    // (`work_ledger.rs`'s OBJECT_LIMIT, EDGE_LIMIT and BYTE_LIMIT).
    let pad = WorkCost {
        objects: 1,
        edges: 1,
        bytes: 1,
    };
    let (objects, edges, bytes) = (1 << 16, 1 << 17, 1 << 28);
    let f = installed(shapes());
    for request in [
        MemberRequest::File("hop"),
        MemberRequest::File("a/z"),
        MemberRequest::Directory("a/b/c"),
        MemberRequest::Directory(""),
    ] {
        let want = expected(&f, "bin/entry", request);
        for i in 0..want.charges.len() {
            let prefix = pad.checked_add(sum(&want.charges[..i])).unwrap();
            let next = want.charges[i];
            let limit = if next.edges > 0 {
                WorkCost {
                    objects,
                    edges: prefix.edges + next.edges - 1,
                    bytes,
                }
            } else {
                WorkCost {
                    objects,
                    edges,
                    bytes: prefix.bytes + next.bytes - 1,
                }
            };
            let (candidate, component) = (f.candidate(), f.component.authenticated());
            let mut tree = capability(&f, &component, &candidate);
            let mut ledger = WorkLedger::with_limits(limit).unwrap();
            let lstats = Rc::new(Cell::new(0usize));
            let l = lstats.clone();
            let result = with_seam(
                move |step| {
                    if step == "lstat" {
                        l.set(l.get() + 1);
                    }
                    Ok(())
                },
                || {
                    within(&mut ledger, |work| {
                        work.charge::<io::Error>(pad).unwrap();
                        tree.launch_member(request, work).map(launched)
                    })
                },
            );
            assert!(
                matches!(result, Err(TreeReadFailure::Budget(_))),
                "{request:?} at {i}: {result:?}"
            );
            assert_eq!(
                ledger.used(),
                prefix,
                "{request:?} at {i}: nothing past the stop"
            );
            let lstat_at = want.charges.len() - 2;
            assert_eq!(
                lstats.get(),
                usize::from(i > lstat_at),
                "{request:?} at {i}"
            );
        }
    }
}

#[test]
fn ci_t28_the_partition_keeps_io_apart_from_digest_and_binding() {
    let f = installed(nested());
    let (candidate, component) = (f.candidate(), f.component.authenticated());
    // An injected read failure is `Io`, not `Digest`.
    let mut tree = capability(&f, &component, &candidate);
    let r = with_seam(
        |step| match step {
            "read" => Err(io::Error::other("injected read failure")),
            _ => Ok(()),
        },
        || {
            within(&mut WorkLedger::snapshot_profile(), |work| {
                tree.launch_member(MemberRequest::File("a/z"), work)
                    .map(launched)
            })
        },
    );
    assert!(
        matches!(r, Err(TreeReadFailure::Io { call: "read", .. })),
        "{r:?}"
    );
    // An injected native error from the binding's observation is `Io`;
    // `ENOENT` and `ENOTDIR` are `Binding`.
    for (error, binding) in [
        (io::Error::other("injected native I/O failure"), false),
        (io::Error::from(io::ErrorKind::NotFound), true),
        (io::Error::from(io::ErrorKind::NotADirectory), true),
    ] {
        let mut tree = capability(&f, &component, &candidate);
        let mut error = Some(error);
        let r = with_seam(
            move |step| match step {
                "lstat" => error.take().map_or(Ok(()), Err),
                _ => Ok(()),
            },
            || {
                within(&mut WorkLedger::snapshot_profile(), |work| {
                    tree.launch_member(MemberRequest::Entrypoint, work)
                        .map(launched)
                })
            },
        );
        if binding {
            assert!(matches!(r, Err(TreeReadFailure::Binding)), "{r:?}");
        } else {
            assert!(
                matches!(r, Err(TreeReadFailure::Io { call: "lstat", .. })),
                "{r:?}"
            );
        }
    }
}

#[test]
fn ci_t28_charges_precede_their_operations_in_source_order() {
    let source = include_str!("retained_tree.rs");
    let at = source
        .find("// ---- The launch member (CI-A3; unit CI-3L) ----")
        .unwrap();
    let code = &source[at..];
    let before = |charge: &str, operation: &str| {
        let c = code.find(charge).unwrap_or_else(|| panic!("{charge}"));
        let o = code
            .find(operation)
            .unwrap_or_else(|| panic!("{operation}"));
        assert!(c < o, "{operation} precedes {charge}");
    };
    before(
        "work.charge(inst::COMPARISON)",
        "resolve(&self.tree, &self.order",
    );
    before("work.charge(heap(length))", "String::with_capacity(length)");
    // The launch-path buffer's charge is the last heap charge, before its
    // allocation.
    let last = code.rfind("work.charge(heap(length))").unwrap();
    let buffer = code.find("Vec::with_capacity(length)").unwrap();
    assert!(code.find("String::with_capacity(length)").unwrap() < last && last < buffer);
    before("work.charge(launch_member_cost())", "Ok(LaunchMember {");
}

#[test]
fn ci_a3_d_the_store_path_is_charged_once_at_the_opening() {
    let f = installed(nested());
    let root = f.store_path.parent().unwrap().to_path_buf();
    let handle = opensip_platform::RetainedDirectory::from_retained_handle(
        std::fs::File::open(&root).unwrap(),
    )
    .unwrap();
    let uid = std::fs::metadata(&root).unwrap().uid();
    let mut ledger = WorkLedger::new();
    let (store, charged) = within(&mut ledger, |work| {
        let before = work.used();
        let store = ComponentStore::open_in(&handle, &root, uid, work);
        (store, minus(work.used(), before))
    });
    let store = store.unwrap();
    assert_eq!(store.path, f.store_path);
    assert_eq!(charged, owned(f.store_path.as_os_str().len()));
    // A relative spelling is refused before any charge or copy.
    let mut ledger = WorkLedger::new();
    let (r, charged) = within(&mut ledger, |work| {
        let before = work.used();
        let r = ComponentStore::open_in(&handle, Path::new("relative"), uid, work).map(|_| ());
        (r, minus(work.used(), before))
    });
    assert!(matches!(r, Err(WorkFailure::Operation(_))));
    assert_eq!(charged, WorkCost::default());
}

#[test]
fn ci_t28_review_cyclic_refusal_has_exact_prefix_and_independent_bounds() {
    let f = installed(file_only());
    let specs = vec![link("a", "b"), link("b", "a"), file("f", 0o755, &[])];
    let request = MemberRequest::File("a");
    let want = expected_specs(&specs, f.store_path.as_os_str().len(), "a", request);
    assert_eq!(
        want.lookup_trace,
        vec![("a".into(), 2), ("b".into(), 1), ("a".into(), 2)]
    );
    assert_eq!(want.hop_lengths, vec![1, 1]);
    assert_eq!(want.row, None);
    let exact = WorkCost {
        objects: 2,
        edges: 6,
        bytes: 2,
    };
    assert_eq!(sum(&want.charges), exact);
    assert_eq!(
        want.bound,
        WorkCost {
            objects: 2,
            edges: 10,
            bytes: 2
        }
    );
    // An authenticated archive cannot contain a cycle. Replace only the test
    // model on a genuinely opened/pinned capability; resolution refuses before
    // any filesystem member, read or binding operation can occur.
    let manifest = manifest_over(&[
        ("a", "symlink", Some("b")),
        ("b", "symlink", Some("a")),
        ("f", "file", None),
    ]);
    let candidate = f.candidate();
    let component = f.component.authenticated();
    let mut tree = capability(&f, &component, &candidate);
    tree.tree = crate::installation::Tree::of(&manifest, MACOS).unwrap();
    tree.order = vec![0, 1, 2];
    assert_eq!(tree.launch_pre_bound(request), Some(want.pre_bound));
    let run = launch(&mut tree, request);
    assert!(matches!(run.result, Err(TreeReadFailure::Association)));
    assert_eq!(run.charged, exact);
    assert_eq!((run.reads, run.lstats), (0, 0));
    assert!(le(run.charged, want.bound));
    assert!(le(want.bound, want.pre_bound));
}

#[test]
fn ci_t28_review_hop_length_overflow_keeps_budget_arithmetic() {
    for (parent, target) in [(usize::MAX, 0), (usize::MAX - 1, 1)] {
        assert!(matches!(
            joined_length_parts(parent, target),
            Err(TreeReadFailure::Budget(WorkBudgetError::Arithmetic))
        ));
    }
    assert_eq!(joined_length_parts(0, usize::MAX).unwrap(), usize::MAX);
    assert_eq!(joined_length_parts(usize::MAX - 2, 1).unwrap(), usize::MAX);
    assert_eq!(joined_length_parts(2, 3).unwrap(), 6);
    assert!(matches!(
        Latched::of(&TreeReadFailure::Budget(WorkBudgetError::Arithmetic)).failure(),
        TreeReadFailure::Budget(WorkBudgetError::Closed)
    ));
    let source = include_str!("retained_tree.rs");
    let start = source.find("pub(crate) fn resolve(").unwrap();
    let end = source[start..].find("impl RetainedTree").unwrap() + start;
    assert!(
        source[start..end].contains("let length = joined_length(row.path, target)?;"),
        "resolution must propagate the checked arithmetic cause without relabelling it"
    );
}
