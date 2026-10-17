// Unit CI-3's controls (component installation plan r3, section 4): CI-T9,
// CI-T10, CI-T12's construction half, CI-T15, CI-T17, CI-T20, CI-T21 and
// CI-T22's B_open and B_transfer halves. Every tree is installed by the same
// installer (LAW item 6's fixture path), from C2a-1's `TestComponent`.
use super::*;
use crate::installation::tests::{
    Fixture, MACOS, Spec, SpecKind, dir, file, link, make_writable, nested, within,
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
    let st = ct::status_read_cost();
    let fopen = ct::open_regular_no_follow_cost();
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
