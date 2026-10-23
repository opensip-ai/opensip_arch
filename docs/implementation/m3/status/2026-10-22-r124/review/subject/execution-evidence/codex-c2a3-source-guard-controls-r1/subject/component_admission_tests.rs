use super::*;
use opensip_platform::WorkLedger;

const SHA: &str = "0000000000000000000000000000000000000000000000000000000000000000";
fn collector(length: usize) -> Collector<'static> {
    Collector {
        expected: length,
        sha256: SHA,
        bytes: Vec::with_capacity(length),
        begun: false,
        finished: false,
        fault: None,
    }
}

#[test]
fn collector_accepts_only_verified_complete_bytes_including_empty() {
    for bytes in [b"".as_slice(), b"abc".as_slice()] {
        let mut sink = collector(bytes.len());
        sink.begin([0; 32], bytes.len() as u64);
        for chunk in bytes.chunks(1) {
            sink.chunk(chunk);
        }
        sink.finish(true);
        assert_eq!(sink.into_verified().unwrap(), bytes);
    }
}

#[test]
fn collector_overflow_keeps_private_capacity_and_never_accepts_a_prefix() {
    let mut sink = collector(2);
    let capacity = sink.bytes.capacity();
    sink.begin([0; 32], 2);
    sink.chunk(b"ab");
    sink.chunk(b"extra");
    sink.finish(true);
    assert_eq!(sink.bytes.capacity(), capacity);
    assert_eq!(sink.bytes, b"ab");
    assert_eq!(sink.into_verified().unwrap_err(), CollectorFault::Length);
}

#[test]
fn collector_refuses_incomplete_unverified_or_repeated_completion() {
    let mut incomplete = collector(2);
    incomplete.begin([0; 32], 2);
    incomplete.chunk(b"a");
    incomplete.finish(true);
    assert!(incomplete.into_verified().is_err());
    let mut unverified = collector(0);
    unverified.begin([0; 32], 0);
    unverified.finish(false);
    assert!(unverified.into_verified().is_err());
    let mut repeated = collector(0);
    repeated.begin([0; 32], 0);
    repeated.finish(true);
    repeated.finish(true);
    assert!(repeated.into_verified().is_err());
}

#[test]
fn collector_rejects_out_of_order_and_mismatched_begin_without_copying() {
    let mut early = collector(1);
    early.chunk(b"a");
    early.begin([0; 32], 1);
    early.finish(true);
    assert!(early.bytes.is_empty());
    assert_eq!(early.into_verified().unwrap_err(), CollectorFault::Chunk);
    let mut digest = collector(1);
    digest.begin([1; 32], 1);
    digest.chunk(b"a");
    assert!(digest.bytes.is_empty());
    assert_eq!(digest.into_verified().unwrap_err(), CollectorFault::Begin);
    let mut length = collector(1);
    length.begin([0; 32], 2);
    assert_eq!(length.into_verified().unwrap_err(), CollectorFault::Begin);
    let mut repeated = collector(1);
    repeated.begin([0; 32], 1);
    repeated.begin([0; 32], 1);
    assert_eq!(repeated.into_verified().unwrap_err(), CollectorFault::Begin);
}

fn budgets() -> [WorkBudgetError; 8] {
    [WorkBudgetError::Closed, WorkBudgetError::Objects, WorkBudgetError::Edges,
     WorkBudgetError::Bytes, WorkBudgetError::Record, WorkBudgetError::Arithmetic,
     WorkBudgetError::ReservedPostcheck, WorkBudgetError::Profile]
}

#[test]
fn every_nested_tree_budget_latches_the_original_scope_and_returns_top_level_budget() {
    for budget in budgets() {
        let expected = format!("{budget:?}");
        let mut ledger = WorkLedger::new();
        let failure = ledger.scope::<(), Fault>(|_| Err(tree_input(TreeReadFailure::Budget(budget))));
        assert!(ledger.is_failed());
        match public_failure(failure.err().unwrap()) {
            ComponentAdmissionFailure::Budget(actual) => assert_eq!(format!("{actual:?}"), expected),
            other => panic!("nested Budget was misrouted: {other:?}"),
        }
        let mut executed = false;
        assert!(ledger.scope::<(), Fault>(|_| { executed = true; Ok(()) }).is_err());
        assert!(!executed);
    }
}

#[test]
fn every_direct_kernel_budget_has_the_same_top_level_route_and_latch() {
    for budget in budgets() {
        let expected = format!("{budget:?}");
        let mut ledger = WorkLedger::new();
        let failure = ledger.scope::<(), Fault>(|_| Err(closure_input(WorkFailure::Budget(budget))));
        assert!(ledger.is_failed());
        match public_failure(failure.err().unwrap()) {
            ComponentAdmissionFailure::Budget(actual) => assert_eq!(format!("{actual:?}"), expected),
            other => panic!("direct Budget was misrouted: {other:?}"),
        }
    }
}

#[test]
fn all_nonbudget_tree_causes_keep_their_original_payloads() {
    use opensip_security::snapshot_source::CustodyDirectoryRefusal;
    let causes = [TreeReadFailure::NotInstalled, TreeReadFailure::Absent { row: 3 },
        TreeReadFailure::Length { row: 5 }, TreeReadFailure::Digest { row: 7 },
        TreeReadFailure::Type { row: None }, TreeReadFailure::Mode { row: Some(11) },
        TreeReadFailure::LinkTarget { row: 13 }, TreeReadFailure::Extra { directory: Some(17) },
        TreeReadFailure::Association, TreeReadFailure::Pin,
        TreeReadFailure::Custody(CustodyDirectoryRefusal::ForeignAccess), TreeReadFailure::Binding,
        TreeReadFailure::Io { call: "retained-read", error: std::io::Error::from_raw_os_error(2) }];
    for cause in causes {
        let expected = format!("{cause:?}");
        match public_failure(tree_input(cause)) {
            ComponentAdmissionFailure::Tree(actual) => assert_eq!(format!("{actual:?}"), expected),
            other => panic!("tree cause was relabelled: {other:?}"),
        }
    }
}

#[test]
fn representation_overflow_is_budget_arithmetic_inside_the_original_ledger() {
    let mut ledger = WorkLedger::new();
    let result = ledger.scope::<(), Fault>(|_| { mul(usize::MAX, 2)?; Ok(()) });
    assert!(ledger.is_failed());
    assert!(matches!(public_failure(result.err().unwrap()),
        ComponentAdmissionFailure::Budget(WorkBudgetError::Arithmetic)));
}

#[test]
fn prepared_empty_slots_charge_nothing_and_mint_only_one_claim() {
    let components: [AuthenticatedComponent<'static>; 0] = [];
    let mut ledger = WorkLedger::snapshot_profile();
    let mut prepared = crate::installation::tests::within(&mut ledger, |work| {
        AdmittedSet::prepare_slots(&components, work)
    }).unwrap();
    assert!(prepared.slots.is_empty());
    assert_eq!(ledger.used(), WorkCost::default());
    drop(prepared.claim().unwrap());
    assert!(prepared.claim().is_none());
    assert_eq!(ledger.used(), WorkCost::default());
}

#[test]
fn prepared_slots_refuse_their_fee_before_minting_any_claim() {
    use crate::installation::tests::{Fixture, nested, within};
    let fixture = Fixture::new(nested());
    let components = [fixture.component.authenticated()];
    let mut ledger = WorkLedger::with_limits(WorkCost {
        objects: 1, edges: 131_072, bytes: 268_435_456,
    }).unwrap();
    // Zero limits are invalid profiles. Exhaust a valid original ledger's
    // remaining object credit before asking the paid constructor to run.
    let prior = WorkCost { objects: 1, edges: 0, bytes: 0 };
    assert!(ledger.charge::<Fault>(prior).is_ok());
    let result = within(&mut ledger, |work| AdmittedSet::prepare_slots(&components, work));
    assert!(matches!(result, Err(ComponentAdmissionFailure::Budget(WorkBudgetError::Objects))));
    assert!(ledger.is_failed());
    assert_eq!(ledger.used(), prior);
}

fn ordinary_store() -> (crate::installation::tests::Scratch, ComponentStore, std::path::PathBuf) {
    use crate::installation::tests::{scratch_dir, within};
    use std::os::unix::fs::{MetadataExt, PermissionsExt};
    let scratch = scratch_dir();
    let path = scratch.0.join("components");
    std::fs::create_dir(&path).unwrap();
    std::fs::set_permissions(&path, std::fs::Permissions::from_mode(0o700)).unwrap();
    let uid = std::fs::metadata(&path).unwrap().uid();
    let directory = opensip_platform::RetainedDirectory::from_retained_handle(
        std::fs::File::open(&path).unwrap(),
    ).unwrap();
    // Exactly CI's fixture provisioning predicate; never a production store.
    let mut provisioning = WorkLedger::new();
    within(&mut provisioning, |work| {
        opensip_platform::append_owner_zero_allow_accounted(directory.as_file(), work)
    }).unwrap();
    let store = within(&mut provisioning, |work| ComponentStore::fixture(directory, &path, uid, work)).unwrap();
    (scratch, store, path)
}

fn ordinary_pin_is_free(store: &std::path::Path, closure: &str) -> bool {
    use opensip_platform::component_tree::{self as tree, Access, PinMode};
    let generation = store.join(closure.strip_prefix("closure2:").unwrap());
    let directory = opensip_platform::RetainedDirectory::from_retained_handle(
        std::fs::File::open(generation).unwrap(),
    ).unwrap();
    let mut gc = WorkLedger::snapshot_profile();
    crate::installation::tests::within(&mut gc, |work| {
        let file = tree::open_regular_no_follow(&directory, "pin.lock", Access::ReadOnly, work).unwrap();
        tree::try_pin(file, PinMode::Exclusive, work).unwrap().is_ok()
    })
}

#[test]
fn signed_ordinary_reader_all_five_roles_install_and_admit_on_one_original_scope() {
    use crate::installation::{install, tests::{MACOS, registry, within}};
    use opensip_security::{fixture_analyzer_subprotocol, retention_fixture};
    const FILES: &[(&str, &[u8])] = &[
        ("bin/entry", b"#!/bin/sh\n# synthetic admission\n"),
        ("lib/empty", b""),
        ("nested/utf8/\u{8a9e}.txt", b"whole retained bytes"),
    ];
    retention_fixture::with_components(FILES, |components, core, archives| {
        assert_eq!(components.len(), 5);
        let (scratch, store, store_path) = ordinary_store();
        let analyzer = fixture_analyzer_subprotocol(1);
        let expected_core = core.core_closure().to_owned();
        let expected_lineage = core.lineage();
        let roles = [CoreRole::Evaluator, CoreRole::Detector, CoreRole::Provider, CoreRole::Adapter];
        let expected_roles: Vec<_> = roles.iter().map(|role| core.role(*role).closure().to_owned()).collect();
        for (index, component) in components.iter().enumerate() {
            // Independent installation operations, not component-admission
            // ledgers and never a retry of a refused admission.
            let path = scratch.0.join(format!("release-{index}.tar"));
            std::fs::write(&path, &archives[index]).unwrap();
            let mut installation = WorkLedger::snapshot_profile();
            let candidate = within(&mut installation, |work| {
                component_candidate(component, MACOS, Some(&analyzer), registry(), work)
            }).unwrap();
            within(&mut installation, |work| install(&store, component, &candidate, MACOS, &path, work)).unwrap();
        }
        let mut admission = WorkLedger::snapshot_profile();
        let mut prepared = within(&mut admission, |work| AdmittedSet::prepare_slots(components, work)).unwrap();
        let claim = prepared.claim().unwrap();
        let set = within(&mut admission, |work| {
            AdmittedSet::admit(&store, claim, core, MACOS, Some(&analyzer), registry(), PinRequest::UnderFence, work)
        }).unwrap();
        assert!(!admission.is_failed());
        assert_eq!(set.components().len(), components.len());
        let ids: Vec<_> = set.components().iter().zip(components).map(|(admitted, component)| {
            let descriptor = opensip_identity::parse_json(admitted.descriptor()).unwrap();
            let opensip_identity::JsonValue::Object(fields) = descriptor else { panic!("descriptor object") };
            assert_eq!(fields["kind"], opensip_identity::JsonValue::String(component.closure_kind().to_owned()));
            assert!(!ordinary_pin_is_free(&store_path, admitted.closure()));
            admitted.closure().to_owned()
        }).collect();
        for (role, expected) in roles.into_iter().zip(expected_roles) {
            let AdmittedClosure::Core(view) = set.core(role) else { panic!("core view") };
            assert_eq!(view.closure(), expected);
            assert_eq!(view.core_closure(), expected_core);
            assert_eq!(view.lineage(), expected_lineage);
        }
        drop(set);
        assert!(prepared.claim().is_none());
        assert!(ids.iter().all(|id| ordinary_pin_is_free(&store_path, id)));
    });
}

#[test]
fn first_component_retention_refusal_precedes_later_analyzer_candidate_refusal() {
    use crate::installation::tests::{MACOS, registry, within};
    use opensip_security::retention_fixture::{self, Role};
    retention_fixture::with_roles(&[Role::Toolchain, Role::Analyzer], &[("entry", b"synthetic")],
        |components, core, _archives| {
            let (_scratch, store, _path) = ordinary_store();
            let mut admission = WorkLedger::snapshot_profile();
            let mut prepared = within(&mut admission, |work| AdmittedSet::prepare_slots(components, work)).unwrap();
            let claim = prepared.claim().unwrap();
            // Nothing is installed. Toolchain's retention must refuse first;
            // eagerly constructing analyzer's unselected protocol would instead
            // produce Closure(Protocol), which is the wrong owning order.
            let result = within(&mut admission, |work| {
                AdmittedSet::admit(&store, claim, core, MACOS, None, registry(), PinRequest::UnderFence, work)
            });
            assert!(matches!(result, Err(ComponentAdmissionFailure::Tree(TreeReadFailure::NotInstalled))));
            assert!(admission.is_failed());
            assert!(prepared.claim().is_none());
        });
}

#[test]
fn failure_in_the_second_signed_component_releases_the_first_completed_pin() {
    use crate::installation::{install, tests::{MACOS, registry, within}};
    use opensip_security::retention_fixture::{self, Role};
    retention_fixture::with_roles(&[Role::Toolchain, Role::Stdlib], &[("entry", b"synthetic")],
        |components, core, archives| {
            let (scratch, store, path) = ordinary_store();
            let archive = scratch.0.join("first.tar");
            std::fs::write(&archive, &archives[0]).unwrap();
            let mut installation = WorkLedger::snapshot_profile();
            let candidate = within(&mut installation, |work| {
                component_candidate(&components[0], MACOS, None, registry(), work)
            }).unwrap();
            let first_id = candidate.closure().to_owned();
            within(&mut installation, |work| {
                install(&store, &components[0], &candidate, MACOS, &archive, work)
            }).unwrap();
            assert!(ordinary_pin_is_free(&path, &first_id));
            let mut admission = WorkLedger::snapshot_profile();
            let mut prepared = within(&mut admission, |work| AdmittedSet::prepare_slots(components, work)).unwrap();
            let claim = prepared.claim().unwrap();
            let result = within(&mut admission, |work| {
                AdmittedSet::admit(&store, claim, core, MACOS, None, registry(), PinRequest::UnderFence, work)
            });
            assert!(matches!(result, Err(ComponentAdmissionFailure::Tree(TreeReadFailure::NotInstalled))));
            assert!(admission.is_failed());
            assert!(prepared.claim().is_none());
            assert!(ordinary_pin_is_free(&path, &first_id));
            let mut entered = false;
            assert!(admission.scope::<(), ()>(|_| { entered = true; Ok(()) }).is_err());
            assert!(!entered);
        });
}

fn install_signed<'a>(
    scratch: &crate::installation::tests::Scratch,
    store: &ComponentStore,
    component: &AuthenticatedComponent<'a>,
    archive: &[u8],
) -> ClosureCandidate<'a> {
    use crate::installation::{install, tests::{MACOS, registry, within}};
    let path = scratch.0.join("negative-control.tar");
    std::fs::write(&path, archive).unwrap();
    let mut installation = WorkLedger::snapshot_profile();
    let candidate = within(&mut installation, |work| {
        component_candidate(component, MACOS, None, registry(), work)
    }).unwrap();
    within(&mut installation, |work| install(store, component, &candidate, MACOS, &path, work)).unwrap();
    candidate
}

#[test]
fn a_late_transfer_digest_failure_preserves_its_cause_and_exposes_no_copied_prefix() {
    use crate::installation::tests::{MACOS, within};
    use opensip_security::retention_fixture::{self, Role};
    use std::os::unix::fs::PermissionsExt;
    let bytes = vec![0x5a; 131_073];
    retention_fixture::with_roles(&[Role::Toolchain], &[("entry", bytes.as_slice())],
        |components, _core, archives| {
            let (scratch, store, path) = ordinary_store();
            let candidate = install_signed(&scratch, &store, &components[0], &archives[0]);
            let entry = path.join(candidate.closure().strip_prefix("closure2:").unwrap()).join("tree/entry");
            let guard = test_faults::arm_after_open(move || {
                let mode = std::fs::metadata(&entry).unwrap().permissions().mode() & 0o7777;
                std::fs::set_permissions(&entry, std::fs::Permissions::from_mode(0o600)).unwrap();
                let mut changed = std::fs::read(&entry).unwrap();
                changed[100_000] ^= 1;
                std::fs::write(&entry, changed).unwrap();
                std::fs::set_permissions(&entry, std::fs::Permissions::from_mode(mode)).unwrap();
            });
            let mut admission = WorkLedger::snapshot_profile();
            let result = within(&mut admission, |work| {
                admit_component(&store, &components[0], &candidate, MACOS, PinRequest::UnderFence, work)
            });
            assert!(matches!(result, Err(ComponentAdmissionFailure::Tree(TreeReadFailure::Digest { .. }))));
            let observed = test_faults::observation().unwrap();
            assert_eq!(observed.copied, 131_073);
            assert!(observed.finished && observed.collector_fault);
            assert!(admission.is_failed());
            assert!(ordinary_pin_is_free(&path, candidate.closure()));
            drop(guard);
        });
}

#[cfg(debug_assertions)]
#[test]
fn a_post_open_transfer_io_failure_wins_over_unverified_collector_completion() {
    use crate::installation::tests::{MACOS, within};
    use opensip_security::retention_fixture::{self, Role};
    use std::{cell::RefCell, rc::Rc};
    retention_fixture::with_roles(&[Role::Toolchain], &[("entry", b"synthetic")],
        |components, _core, archives| {
            let (scratch, store, path) = ordinary_store();
            let candidate = install_signed(&scratch, &store, &components[0], &archives[0]);
            let read_guard = Rc::new(RefCell::new(None));
            let captured = Rc::clone(&read_guard);
            let guard = test_faults::arm_after_open(move || {
                *captured.borrow_mut() = Some(crate::retained_tree::read_fixture::fail_next_read());
            });
            let mut admission = WorkLedger::snapshot_profile();
            let result = within(&mut admission, |work| {
                admit_component(&store, &components[0], &candidate, MACOS, PinRequest::UnderFence, work)
            });
            assert!(read_guard.borrow().as_ref().unwrap().was_triggered());
            assert!(matches!(result, Err(ComponentAdmissionFailure::Tree(TreeReadFailure::Io { call: "read", .. }))));
            let observed = test_faults::observation().unwrap();
            assert_eq!(observed.copied, 0);
            assert!(observed.finished && observed.collector_fault);
            assert!(admission.is_failed());
            assert!(ordinary_pin_is_free(&path, candidate.closure()));
            drop(guard);
        });
}

#[test]
fn the_actual_admission_kernel_refuses_each_corrupted_private_representation() {
    use crate::installation::tests::{MACOS, within};
    use opensip_security::{ClosureRetention, retention_fixture::{self, Role}};
    use test_faults::KernelFault;
    // Distinct injected operations, not retries of a failed production scope.
    for (fault, expected) in [(KernelFault::Missing, ClosureRetention::Missing),
        (KernelFault::Length, ClosureRetention::Length),
        (KernelFault::Digest, ClosureRetention::Digest),
        (KernelFault::BodyDigest, ClosureRetention::Digest)] {
        retention_fixture::with_roles(&[Role::Toolchain], &[("entry", b"synthetic")],
            |components, _core, archives| {
                let (scratch, store, path) = ordinary_store();
                let candidate = install_signed(&scratch, &store, &components[0], &archives[0]);
                let guard = test_faults::arm_kernel(fault);
                let mut admission = WorkLedger::snapshot_profile();
                let result = within(&mut admission, |work| {
                    admit_component(&store, &components[0], &candidate, MACOS, PinRequest::UnderFence, work)
                });
                match result {
                    Err(ComponentAdmissionFailure::Closure(ClosureRefusal::Retention(actual))) => assert_eq!(actual, expected),
                    _ => panic!("the actual kernel failed to retain its refusal cause"),
                }
                assert!(admission.is_failed());
                assert!(ordinary_pin_is_free(&path, candidate.closure()));
                drop(guard);
            });
    }
}

/// Independent oracle from M-BOUND's operation-category table, rather than
/// the implementation's reduced 237/23/10368 coefficient expression. Wide
/// arithmetic also keeps the test oracle independent of its checked helpers.
fn representation_contract_price(candidate: &ClosureCandidate<'_>) -> WorkCost {
    let mut count = 0u128;
    let mut bytes = 0u128;
    let mut longest_path = 0u128;
    let mut callbacks = 0u128;
    for blob in candidate.blobs() {
        count += 1;
        let length = u128::from(blob.bytes());
        bytes += length;
        longest_path = longest_path.max(blob.path().len() as u128);
        callbacks += 2 * length.div_ceil(65_536) + 2;
    }
    let mut height = 1u128;
    let mut remaining = count;
    while remaining != 0 {
        height += 1;
        remaining /= 2;
    }
    let nodes = 2 * count;
    let comparisons = 11 * count * height;
    // (occurrences, logical edges, bulk bytes); scalar metadata reserves64
    // bytes per edge. String comparisons have a separate two-path allowance.
    let categories = [
        (1, 128, 0), (count, 64, 0), (callbacks, 8, 0),
        (nodes, 2, 0), (count, 6, 768), (nodes, 8, 704),
        (2 * nodes, 22, 1024), (nodes, 20, 1024), (nodes, 8, 1024),
        (count + nodes, 1, 0), (count * height, 1, 0),
        (comparisons, 1, 0), // probe-loop metadata, not string-byte comparison
    ];
    let mut edges = comparisons;
    let mut priced_bytes = 2 * longest_path * comparisons;
    for (occurrences, visits, bulk) in categories {
        edges += occurrences * visits;
        priced_bytes += occurrences * (64 * visits + bulk);
    }
    assert_eq!(std::mem::size_of::<Vec<u8>>(), 24);
    let index = if count == 0 { 0 } else { 24 * count + 128 };
    priced_bytes += index + bytes + 128 * count + nodes * (512 + 128);
    priced_bytes += 2 * bytes + 48 * count;
    WorkCost {
        objects: usize::try_from(u128::from(count != 0) + count + nodes).unwrap(),
        edges: usize::try_from(edges).unwrap(),
        bytes: usize::try_from(priced_bytes).unwrap(),
    }
}

#[test]
fn representation_funding_matches_independent_categories_on_signed_metadata() {
    use crate::installation::tests::{MACOS, registry, within};
    use opensip_security::retention_fixture::{self, Role};
    let crossing = vec![b'x'; 65_537];
    let cases: Vec<Vec<(&str, &[u8])>> = vec![
        vec![("bin/entry", b"")],
        vec![("bin/entry", b"x"), ("nested/語語語語/empty", b"")],
        vec![("bin/entry", b"entry"), ("nested/chunks", &crossing),
             ("nested/語語語語/empty", b"")],
    ];
    for files in cases {
        retention_fixture::with_roles(&[Role::Toolchain], &files, |components, _, _| {
            let mut preparation = WorkLedger::snapshot_profile();
            let candidate = within(&mut preparation, |work| {
                component_candidate(&components[0], MACOS, None, registry(), work)
            }).unwrap();
            let expected = representation_contract_price(&candidate);
            // A direct private funding-unit control, not an admitted capability
            // or a replacement for the production CI-open prerequisite.
            let mut measured = WorkLedger::new();
            let result = measured.scope::<_, Fault>(|work| fund_representation(&candidate, work));
            assert_eq!(result.ok(), Some(files.len()));
            assert_eq!(measured.used(), expected);
            assert!(!measured.is_failed());
        });
    }
}

#[test]
fn each_actual_funding_phase_preserves_budget_cause_prefix_and_latch() {
    use crate::installation::tests::{MACOS, registry, within};
    use opensip_security::retention_fixture::{self, Role};
    const FILES: &[(&str, &[u8])] = &[("bin/entry", b"entry"), ("a/empty", b""),
                                    ("nested/語語語語/data", b"payload")];
    retention_fixture::with_roles(&[Role::Toolchain], FILES, |components, _, _| {
        let mut preparation = WorkLedger::snapshot_profile();
        let candidate = within(&mut preparation, |work| {
            component_candidate(&components[0], MACOS, None, registry(), work)
        }).unwrap();
        let full = representation_contract_price(&candidate);
        let fixed = WorkCost { objects: 0, edges: 128, bytes: 128 * 64 };
        let scans = 12 * FILES.len();
        let scanned = fixed.checked_add(WorkCost { objects: 0, edges: scans, bytes: 64 * scans }).unwrap();
        let cases = [
            ("fixed", WorkCost { bytes: fixed.bytes - 1, ..full }, WorkBudgetError::Bytes, WorkCost::default()),
            ("scan", WorkCost { bytes: scanned.bytes - 1, ..full }, WorkBudgetError::Bytes, fixed),
            ("remainder-objects", WorkCost { objects: full.objects - 1, ..full }, WorkBudgetError::Objects, scanned),
            ("remainder-edges", WorkCost { edges: full.edges - 1, ..full }, WorkBudgetError::Edges, scanned),
            ("remainder-bytes", WorkCost { bytes: full.bytes - 1, ..full }, WorkBudgetError::Bytes, scanned),
        ];
        for (name, limits, expected, prefix) in cases {
            // Independent negative scenarios; never replace a failed operation's ledger.
            let mut ledger = WorkLedger::with_limits(limits).unwrap();
            let result = ledger.scope::<_, Fault>(|work| fund_representation(&candidate, work));
            match public_failure(result.err().expect("funding must refuse")) {
                ComponentAdmissionFailure::Budget(actual) => assert_eq!(format!("{actual:?}"), format!("{expected:?}"), "{name}"),
                other => panic!("funding cause changed for {name}: {other:?}"),
            }
            assert!(ledger.is_failed(), "{name}");
            assert_eq!(ledger.used(), prefix, "{name}");
            let mut entered = false;
            let later = ledger.scope::<(), Fault>(|_| { entered = true; Ok(()) });
            assert!(matches!(later, Err(WorkFailure::Budget(WorkBudgetError::Closed))));
            assert!(!entered);
            assert_eq!(ledger.used(), prefix);
        }
    });
}

/// Reference CI/T sink. Its metadata work is covered by the independently
/// prepaid M allowance. It holds no scope, allocates no payload, and mints no
/// admitted authority; this is a control over existing owner's charged calls.
struct ChargeReferenceSink {
    expected: u64,
    received: u64,
    begun: bool,
    finished: bool,
}
impl VerifiedSink for ChargeReferenceSink {
    fn begin(&mut self, _sha256: [u8; 32], length: u64) {
        assert!(!self.begun);
        assert_eq!(length, self.expected);
        self.begun = true;
    }
    fn chunk(&mut self, bytes: &[u8]) {
        assert!(self.begun && !self.finished);
        self.received = self.received.checked_add(u64::try_from(bytes.len()).unwrap()).unwrap();
        assert!(self.received <= self.expected);
    }
    fn finish(&mut self, verified: bool) {
        assert!(self.begun && !self.finished && verified);
        assert_eq!(self.received, self.expected);
        self.finished = true;
    }
}
struct ChargeReference {
    total: WorkCost,
    after_candidate: WorkCost,
    after_representation: WorkCost,
    before_kernel: WorkCost,
    closure: String,
}
fn admission_charge_reference(
    store: &ComponentStore,
    component: &AuthenticatedComponent<'_>,
    files: &[(&str, &[u8])],
) -> ChargeReference {
    use crate::installation::tests::{MACOS, registry, within};
    // An independent positive reference operation, not a retry of an actual
    // admission. Measure original C2a-1/CI/T/K owners; fund only M from the
    // category-table oracle. Test-oracle/expected-data preparation is not a
    // production allocation or an all-input operation-count measurement.
    let mut reference = WorkLedger::snapshot_profile();
    let candidate = within(&mut reference, |work| {
        component_candidate(component, MACOS, None, registry(), work)
    }).unwrap();
    let after_candidate = reference.used();
    let price = representation_contract_price(&candidate);
    let closure = candidate.closure().to_owned();
    let mut retained = within(&mut reference, |work| {
        open_retained_tree(store, component, &candidate, MACOS, PinRequest::UnderFence, work)
    }).unwrap();
    within(&mut reference, |work| work.charge::<()>(price)).unwrap();
    let after_representation = reference.used();
    for blob in candidate.blobs() {
        let mut sink = ChargeReferenceSink { expected: blob.bytes(), received: 0, begun: false, finished: false };
        within(&mut reference, |work| retained.transfer(blob.path(), &mut sink, work)).unwrap();
        assert!(sink.finished);
    }
    let before_kernel = reference.used();
    let mut expected = BTreeMap::new();
    for (path, bytes) in files {
        expected.insert(*path, *bytes);
    }
    within(&mut reference, |work| {
        verify_retained_tree(&candidate, &expected, component.body(), work)
    }).unwrap();
    assert!(!reference.is_failed());
    let total = reference.used();
    drop(retained);
    ChargeReference { total, after_candidate, after_representation, before_kernel, closure }
}

#[test]
fn shared_storage_fee_and_actual_owner_charges_compose_once_on_one_scope() {
    use crate::installation::tests::{MACOS, registry, within};
    use opensip_security::retention_fixture::{self, Role};
    let crossing = vec![b'x'; 65_537];
    let files: &[(&str, &[u8])] = &[("bin/entry", b"entry"), ("nested/chunks", &crossing),
                                  ("nested/語語語語/empty", b"")];
    retention_fixture::with_roles(&[Role::Toolchain, Role::Stdlib], files, |components, core, archives| {
        let (scratch, store, path) = ordinary_store();
        for (component, archive) in components.iter().zip(archives) {
            drop(install_signed(&scratch, &store, component, archive));
        }
        let count = components.len();
        assert_eq!(count, 2);
        let candidate_slot = std::mem::size_of::<Option<ClosureCandidate<'static>>>();
        let admitted_slot = std::mem::size_of::<AdmittedComponent<'static, 'static, 'static>>();
        let prepared_fee = WorkCost { objects: 1, edges: 4 * count, bytes: 128 + 5 * count * candidate_slot };
        let result_fee = WorkCost { objects: 1, edges: 4 * count, bytes: 128 + 3 * count * admitted_slot };
        let mut expected = prepared_fee.checked_add(result_fee).unwrap();
        let mut expected_ids = Vec::new();
        for component in components {
            let reference = admission_charge_reference(&store, component, files);
            assert!(ordinary_pin_is_free(&path, &reference.closure));
            expected = expected.checked_add(reference.total).unwrap();
            expected_ids.push(reference.closure);
        }
        let mut admission = WorkLedger::snapshot_profile();
        let mut prepared = within(&mut admission, |work| AdmittedSet::prepare_slots(components, work)).unwrap();
        assert_eq!(admission.used(), prepared_fee);
        let actual = within(&mut admission, |work| {
            AdmittedSet::admit(&store, prepared.claim().unwrap(), core, MACOS, None, registry(), PinRequest::UnderFence, work)
        }).unwrap();
        assert_eq!(admission.used(), expected);
        assert!(!admission.is_failed());
        assert_eq!(actual.components().len(), count);
        for (component, id) in actual.components().iter().zip(&expected_ids) {
            assert_eq!(component.closure(), id.as_str());
            assert!(!ordinary_pin_is_free(&path, id));
        }
        drop(actual);
        assert!(prepared.claim().is_none());
        assert_eq!(admission.used(), expected);
        assert!(expected_ids.iter().all(|id| ordinary_pin_is_free(&path, id)));
        // A future exact native runner must retain this successful test's
        // output (e.g. --show-output); no native sizes exist until it runs.
        println!("C2A3_SHARED_STORAGE_ABI {{\"candidateSlotSize\":{candidate_slot},\"admittedSlotSize\":{admitted_slot},\"components\":{count},\"chargedObjects\":{},\"chargedEdges\":{},\"chargedBytes\":{},\"unitAcceptance\":false,\"productQualification\":false}}", expected.objects, expected.edges, expected.bytes);
    });
}

#[test]
fn kernel_budget_after_all_verified_transfers_drops_the_actual_pin() {
    use crate::installation::tests::{MACOS, registry, within};
    use opensip_security::retention_fixture::{self, Role};
    const FILES: &[(&str, &[u8])] = &[("bin/entry", b"entry"), ("nested/data", b"payload")];
    retention_fixture::with_roles(&[Role::Toolchain], FILES, |components, _, archives| {
        let (scratch, store, path) = ordinary_store();
        drop(install_signed(&scratch, &store, &components[0], &archives[0]));
        let reference = admission_charge_reference(&store, &components[0], FILES);
        assert!(reference.total.edges > reference.before_kernel.edges);
        let mut admission = WorkLedger::with_limits(WorkCost {
            edges: reference.before_kernel.edges, ..reference.total
        }).unwrap();
        let candidate = within(&mut admission, |work| {
            component_candidate(&components[0], MACOS, None, registry(), work)
        }).unwrap();
        let result = within(&mut admission, |work| {
            admit_component(&store, &components[0], &candidate, MACOS, PinRequest::UnderFence, work)
        });
        assert!(matches!(result, Err(ComponentAdmissionFailure::Budget(WorkBudgetError::Edges))));
        assert!(admission.is_failed());
        assert_eq!(admission.used(), reference.before_kernel);
        assert!(ordinary_pin_is_free(&path, &reference.closure));
        let mut entered = false;
        let later = admission.scope::<(), Fault>(|_| { entered = true; Ok(()) });
        assert!(matches!(later, Err(WorkFailure::Budget(WorkBudgetError::Closed))));
        assert!(!entered);
    });
}

#[test]
fn actual_transfer_budget_wins_over_the_collectors_unverified_completion() {
    use crate::installation::tests::{MACOS, registry, within};
    use opensip_security::retention_fixture::{self, Role};
    const FILES: &[(&str, &[u8])] = &[("bin/entry", b"entry"), ("nested/data", b"payload")];
    retention_fixture::with_roles(&[Role::Toolchain], FILES, |components, _, archives| {
        let (scratch, store, path) = ordinary_store();
        drop(install_signed(&scratch, &store, &components[0], &archives[0]));
        let reference = admission_charge_reference(&store, &components[0], FILES);
        assert!(reference.before_kernel.edges > reference.after_representation.edges);
        let mut admission = WorkLedger::with_limits(WorkCost {
            edges: reference.after_representation.edges, ..reference.total
        }).unwrap();
        let candidate = within(&mut admission, |work| {
            component_candidate(&components[0], MACOS, None, registry(), work)
        }).unwrap();
        let guard = test_faults::arm_after_open(|| {});
        let result = within(&mut admission, |work| {
            admit_component(&store, &components[0], &candidate, MACOS, PinRequest::UnderFence, work)
        });
        assert!(matches!(result, Err(ComponentAdmissionFailure::Budget(WorkBudgetError::Edges))));
        assert!(admission.is_failed());
        assert_eq!(admission.used(), reference.after_representation);
        let observed = test_faults::observation().expect("actual transfer error observation");
        assert_eq!(observed.copied, 0);
        assert!(observed.finished && observed.collector_fault);
        assert!(ordinary_pin_is_free(&path, &reference.closure));
        drop(guard);
        let mut entered = false;
        let later = admission.scope::<(), Fault>(|_| { entered = true; Ok(()) });
        assert!(matches!(later, Err(WorkFailure::Budget(WorkBudgetError::Closed))));
        assert!(!entered);
    });
}

#[test]
fn actual_ci_open_budget_normalizes_before_representation_or_transfer() {
    use crate::installation::tests::{MACOS, registry, within};
    use opensip_security::retention_fixture::{self, Role};
    use std::{cell::Cell, rc::Rc};
    const FILES: &[(&str, &[u8])] = &[("bin/entry", b"entry"), ("nested/data", b"payload")];
    retention_fixture::with_roles(&[Role::Toolchain], FILES, |components, _, archives| {
        let (scratch, store, path) = ordinary_store();
        drop(install_signed(&scratch, &store, &components[0], &archives[0]));
        let reference = admission_charge_reference(&store, &components[0], FILES);
        let mut admission = WorkLedger::with_limits(WorkCost {
            edges: reference.after_candidate.edges, ..reference.total
        }).unwrap();
        let candidate = within(&mut admission, |work| {
            component_candidate(&components[0], MACOS, None, registry(), work)
        }).unwrap();
        let opened = Rc::new(Cell::new(false));
        let hook = opened.clone();
        let guard = test_faults::arm_after_open(move || hook.set(true));
        let result = within(&mut admission, |work| {
            admit_component(&store, &components[0], &candidate, MACOS, PinRequest::UnderFence, work)
        });
        assert!(matches!(result, Err(ComponentAdmissionFailure::Budget(WorkBudgetError::Edges))));
        assert!(admission.is_failed());
        assert_eq!(admission.used().edges, reference.after_candidate.edges);
        assert!(!opened.get());
        assert!(test_faults::observation().is_none());
        assert!(ordinary_pin_is_free(&path, &reference.closure));
        drop(guard);
        let mut entered = false;
        let later = admission.scope::<(), Fault>(|_| { entered = true; Ok(()) });
        assert!(matches!(later, Err(WorkFailure::Budget(WorkBudgetError::Closed))));
        assert!(!entered);
    });
}

// Exact draft-source binding required by the representation plan. This test
// does not prove the M bound or grant acceptance. Rebind only with the exact
// independently reviewed source/model delta; comments and formatting also bind.
fn representation_source_matches_review_pin(source: &str) -> bool {
    const EXPECTED: [u8; 32] = [0x12, 0x33, 0xe3, 0x07, 0x6a, 0xb9, 0x4f, 0xa4, 0x17, 0x50, 0xf1, 0xcb, 0x08, 0x74, 0x69, 0x3a, 0x10, 0x60, 0x11, 0x48, 0xae, 0xa5, 0x96, 0x77, 0x4b, 0xc1, 0x6f, 0xad, 0x9e, 0xe3, 0x78, 0x11];
    opensip_identity::RawSha256::new()
        .update(source.as_bytes())
        .expect("bounded admission source")
        .finish() == EXPECTED
}

#[test]
fn representation_source_guard_binds_the_exact_draft_implementation() {
    assert!(representation_source_matches_review_pin(include_str!("component_admission.rs")));
}

#[test]
fn representation_source_guard_refuses_unreviewed_copy_growth_scan_and_callback_work() {
    let source = include_str!("component_admission.rs");
    for (before, after) in [
        ("payloads.push(bytes);", "payloads.push(bytes.clone());"),
        ("bytes: Vec::with_capacity(length),", "bytes: Vec::with_capacity(length.saturating_add(1)),"),
        ("let count = candidate.blob_count();", "let count = candidate.blobs().count();"),
        ("self.bytes.extend_from_slice(bytes);", "self.bytes.extend_from_slice(bytes); self.bytes.clone();"),
        ("mul(8, envelopes)?", "mul(1, envelopes)?"),
    ] {
        assert_eq!(source.matches(before).count(), 1, "mutation anchor must be unique");
        let changed = source.replacen(before, after, 1);
        assert_ne!(changed, source);
        assert!(!representation_source_matches_review_pin(&changed), "changed source requires review");
    }
}
