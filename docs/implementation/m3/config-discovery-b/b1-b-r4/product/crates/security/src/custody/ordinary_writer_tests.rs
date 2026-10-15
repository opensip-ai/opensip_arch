// Law X1 r1 items 1 to 7, on scratch account homes only. The write receipt
// is produced over 462's signed test trees for a scratch H, and the gate
// runs on that H with the real account's credentials. Nothing here opens
// the real account's I.
use super::super::installation_admission::{GateSeam, HomeSource};
use super::super::installation_read_fixture::{ReadFixture, churned};
use super::super::read_premise::{
    LendsBarrier, LendsReadPremise, ReadPremiseReceipt, Write, produce_for,
};
use super::*;
use crate::initial_installation::InitialInstallationAttempt;
use crate::trust::{ReadProducers, produce_initial_core, read_producers};
use opensip_platform::{FileLock, LockMode, WorkCost};
use std::cell::Cell;
use std::fs;
use std::marker::PhantomData;
use std::os::unix::fs::PermissionsExt;
use std::path::{Path, PathBuf};
use std::sync::atomic::AtomicBool;

struct Scratch(PathBuf);
impl Drop for Scratch {
    fn drop(&mut self) {
        let _ = fs::remove_dir_all(&self.0);
    }
}
/// A scratch root holding an empty 0700 `home`, on its canonical path.
fn scratch() -> (Scratch, PathBuf) {
    let nonce: String = opensip_platform::request_entropy()
        .unwrap()
        .iter()
        .map(|b| format!("{b:02x}"))
        .collect();
    let root = crate::test_scratch::temp_dir().join(format!("opensip-writerx1-{nonce}"));
    fs::create_dir(&root).unwrap();
    fs::set_permissions(&root, fs::Permissions::from_mode(0o700)).unwrap();
    let root = fs::canonicalize(&root).unwrap();
    let home = root.join("home");
    fs::create_dir(&home).unwrap();
    fs::set_permissions(&home, fs::Permissions::from_mode(0o700)).unwrap();
    (Scratch(root), home)
}
fn entries(dir: &Path) -> usize {
    fs::read_dir(dir).unwrap().count()
}
fn fence_free(i: &Path) -> bool {
    FileLock::try_acquire(
        fs::File::open(i.join("lifecycle.fence")).unwrap(),
        LockMode::Exclusive,
    )
    .unwrap()
    .is_some()
}

/// The write receipt over the signed test trees, on its own test attempt.
fn write_receipt(flag: &AtomicBool, producers: &ReadProducers) -> Result<WritePlatformReceipt, T> {
    produce_for::<Write>(
        InitialInstallationAttempt::for_tests(flag, None),
        InitialInstallationAttempt::observe_actor,
        |attempt| producers.core(attempt),
        |attempt, actor, core| producers.platform(attempt, actor, core),
    )
}
/// Item 2 on the I under `home`, with the receipt's own recheck, a gate on
/// `gate_flag` with `limits`, and the fixture H.
fn admit_at(
    receipt: WritePlatformReceipt,
    home: &Path,
    gate_flag: &AtomicBool,
    limits: Option<WorkCost>,
) -> Result<OrdinaryWriteAdmission, T> {
    admit_with(
        receipt,
        WritePlatformReceipt::recheck,
        || DurableWriteGate::for_tests(gate_flag, limits),
        |gate, receipt| {
            gate.admit_with(
                receipt.qualification(),
                HomeSource::Fixture(home),
                &GateSeam::live(),
            )
        },
    )
}

#[test]
fn an_ordinary_writer_is_admitted_with_the_fence_held_and_can_recheck() {
    churned(|| {
        let f = ReadFixture::new("x1-ok");
        let producers = read_producers("x1-ok-write", true, Some(&f.home));
        let receipt = write_receipt(&AtomicBool::new(false), &producers).unwrap();
        let mut admission = admit_at(receipt, &f.home, &AtomicBool::new(false), None).unwrap();
        // Item 4: the held fence and the gate's observations, nothing more.
        assert!(!fence_free(&f.installation));
        assert!(!admission.installation().required().is_empty());
        assert_eq!(
            format!("{admission:?}").split_once('{').unwrap().0.trim(),
            "OrdinaryWriteAdmission"
        );
        admission.recheck().unwrap();
        admission.release().unwrap();
        assert!(fence_free(&f.installation));
    });
}

#[test]
#[allow(clippy::disallowed_methods, reason = "M3-B r5 item 9: the real HOME, only to assert no real installation exists, test-only")]
fn a_development_build_ends_in_the_no_embedded_release_row() {
    // The live actor and the live InitialCore: F0 refuses before any path.
    let result = produce_for::<Write>(
        InitialInstallationAttempt::for_tests(&AtomicBool::new(false), None),
        InitialInstallationAttempt::observe_actor,
        produce_initial_core,
        |_, _, _| panic!("InitialPlatform must not run after F0 refuses"),
    );
    assert_eq!(result.unwrap_err(), T::NoEmbeddedRelease);
    let real = std::env::var_os("HOME").map(PathBuf::from).unwrap();
    assert!(!real.join("Library/Application Support/OpenSIP").exists());
}

#[test]
fn an_absent_installation_is_not_initialized_and_nothing_is_created() {
    churned(|| {
        let (_scratch, home) = scratch();
        let producers = read_producers("x1-absent", true, Some(&home));
        let receipt = write_receipt(&AtomicBool::new(false), &producers).unwrap();
        let result = admit_at(receipt, &home, &AtomicBool::new(false), None);
        assert_eq!(result.unwrap_err(), T::NotInitialized);
        // An ordinary writer never creates I, an ancestor or a stage.
        assert_eq!(entries(&home), 0);
    });
}

#[test]
fn a_non_directory_at_a_suffix_name_is_not_absence() {
    churned(|| {
        let (_scratch, home) = scratch();
        let library = home.join("Library");
        fs::write(&library, b"not a directory").unwrap();
        let producers = read_producers("x1-file", true, Some(&home));
        let receipt = write_receipt(&AtomicBool::new(false), &producers).unwrap();
        let result = admit_at(receipt, &home, &AtomicBool::new(false), None);
        let row = result.unwrap_err();
        assert_ne!(row, T::NotInitialized, "{row:?}");
        // Nothing was replaced or created.
        assert_eq!(fs::read(&library).unwrap(), b"not a directory");
        assert_eq!(entries(&home), 1);
    });
}

#[test]
fn a_first_recheck_refusal_never_enters_the_gate() {
    churned(|| {
        let f = ReadFixture::new("x1-first");
        let producers = read_producers("x1-first-write", true, Some(&f.home));
        let receipt = write_receipt(&AtomicBool::new(false), &producers).unwrap();
        let result = admit_with(
            receipt,
            |_| Err(T::AccountRefused),
            || panic!("the gate must not begin after a refused step 2 recheck"),
            |_, _| panic!("the gate must not admit after a refused step 2 recheck"),
        );
        assert_eq!(result.unwrap_err(), T::AccountRefused);
        assert!(fence_free(&f.installation));
    });
}

#[test]
fn a_second_recheck_refusal_releases_the_fence_and_returns_nothing() {
    churned(|| {
        let f = ReadFixture::new("x1-second");
        let producers = read_producers("x1-second-write", true, Some(&f.home));
        let receipt = write_receipt(&AtomicBool::new(false), &producers).unwrap();
        let calls = Cell::new(0);
        let held_at_second = Cell::new(false);
        let gate_flag = AtomicBool::new(false);
        let result = admit_with(
            receipt,
            |receipt| {
                calls.set(calls.get() + 1);
                if calls.get() == 1 {
                    receipt.recheck()
                } else {
                    // Step 4 runs while the gate's fence is still held.
                    held_at_second.set(!fence_free(&f.installation));
                    Err(T::PlatformUnqualified)
                }
            },
            || DurableWriteGate::for_tests(&gate_flag, None),
            |gate, receipt| {
                gate.admit_with(
                    receipt.qualification(),
                    HomeSource::Fixture(&f.home),
                    &GateSeam::live(),
                )
            },
        );
        assert_eq!(result.unwrap_err(), T::PlatformUnqualified);
        assert_eq!(calls.get(), 2);
        assert!(held_at_second.get());
        assert!(fence_free(&f.installation));
    });
}

#[test]
fn a_busy_installation_fence_ends_in_the_busy_row() {
    churned(|| {
        let f = ReadFixture::new("x1-busy");
        let _other = FileLock::try_acquire(
            fs::File::open(f.installation.join("lifecycle.fence")).unwrap(),
            LockMode::Exclusive,
        )
        .unwrap()
        .unwrap();
        let producers = read_producers("x1-busy-write", true, Some(&f.home));
        let receipt = write_receipt(&AtomicBool::new(false), &producers).unwrap();
        let result = admit_at(receipt, &f.home, &AtomicBool::new(false), None);
        assert_eq!(result.unwrap_err(), T::Busy);
    });
}

#[test]
fn a_gate_that_cannot_charge_ends_in_the_budget_row_with_the_fence_free() {
    churned(|| {
        let f = ReadFixture::new("x1-budget");
        let producers = read_producers("x1-budget-write", true, Some(&f.home));
        let receipt = write_receipt(&AtomicBool::new(false), &producers).unwrap();
        // Item 5: the gate's own ledger, separate from the receipt's attempt.
        let limits = WorkCost {
            objects: 64,
            edges: 64,
            bytes: 1 << 20,
        };
        let result = admit_at(receipt, &f.home, &AtomicBool::new(false), Some(limits));
        assert_eq!(result.unwrap_err(), T::BudgetExhausted);
        assert!(fence_free(&f.installation));
    });
}

#[test]
fn a_process_has_one_entry() {
    churned(|| {
        let (_scratch, home) = scratch();
        let producers = read_producers("x1-one", true, Some(&home));
        // One attempt: a second receipt on the same flag is a broken caller,
        // whichever purpose produced the first.
        let attempt = AtomicBool::new(false);
        drop(write_receipt(&attempt, &producers).unwrap());
        assert_eq!(write_receipt(&attempt, &producers).unwrap_err(), T::Invariant);
        // One gate: a second admission on the same gate flag never runs.
        let f = ReadFixture::new("x1-one-gate");
        let producers = read_producers("x1-one-gate-write", true, Some(&f.home));
        let gate = AtomicBool::new(false);
        let first = admit_at(
            write_receipt(&AtomicBool::new(false), &producers).unwrap(),
            &f.home,
            &gate,
            None,
        )
        .unwrap();
        first.release().unwrap();
        let second = admit_at(
            write_receipt(&AtomicBool::new(false), &producers).unwrap(),
            &f.home,
            &gate,
            None,
        );
        assert_eq!(second.unwrap_err(), T::Invariant);
    });
}

// Item 1: each purpose lends only its own sealed qualification. The inherent
// constants apply only when the bound holds; otherwise the trait's default
// is chosen.
trait Lacks {
    const BARRIER: bool = false;
    const READ_PREMISE: bool = false;
    const CLONE: bool = false;
}
struct Probe<R>(PhantomData<R>);
impl<R> Lacks for Probe<R> {}
#[allow(dead_code)]
impl<R: LendsBarrier> Probe<R> {
    const BARRIER: bool = true;
}
#[allow(dead_code)]
struct ReadProbe<R>(PhantomData<R>);
impl<R> Lacks for ReadProbe<R> {}
#[allow(dead_code)]
impl<R: LendsReadPremise> ReadProbe<R> {
    const READ_PREMISE: bool = true;
}
#[allow(dead_code)]
struct CloneProbe<R>(PhantomData<R>);
impl<R> Lacks for CloneProbe<R> {}
#[allow(dead_code)]
impl<R: Clone> CloneProbe<R> {
    const CLONE: bool = true;
}

#[test]
fn each_purpose_lends_only_its_own_sealed_qualification() {
    const {
        assert!(Probe::<WritePlatformReceipt>::BARRIER);
        assert!(!Probe::<ReadPremiseReceipt>::BARRIER);
        assert!(ReadProbe::<ReadPremiseReceipt>::READ_PREMISE);
        assert!(!ReadProbe::<WritePlatformReceipt>::READ_PREMISE);
        assert!(!CloneProbe::<WritePlatformReceipt>::CLONE);
        assert!(!CloneProbe::<OrdinaryWriteAdmission>::CLONE);
    };
    let (_scratch, home) = scratch();
    let producers = read_producers("x1-lend", true, Some(&home));
    let receipt = write_receipt(&AtomicBool::new(false), &producers).unwrap();
    assert_eq!(format!("{receipt:?}"), "WritePlatformReceipt { .. }");
    fn lent<Q: DurableBarrierQualificationProbe>(_: &Q) {}
    lent(receipt.qualification());
    // The live entries take nothing: no command, flag, writer or receipt.
    let _: fn() -> Result<WritePlatformReceipt, T> = produce_write_platform;
    let _: fn() -> Result<OrdinaryWriteAdmission, T> = admit_ordinary_writer;
}
use super::super::installation_admission::DurableBarrierQualification as DurableBarrierQualificationProbe;

#[test]
fn the_lendings_are_typed_by_purpose_in_the_source() {
    // Production text of the receipt, without its test module.
    let source = include_str!("read_premise.rs");
    let source = source.split("#[cfg(test)]").next().unwrap();
    // Exactly two lending methods, one per purpose's own impl block.
    assert_eq!(source.matches("fn qualification(").count(), 2);
    let read = source.split("impl PlatformReceipt<Read>").nth(1).unwrap();
    let read = read.split("impl PlatformReceipt<Write>").next().unwrap();
    assert!(read.contains("-> &impl ReadPremiseQualification"));
    assert!(!read.contains("DurableBarrierQualification"));
    let write = source.split("impl PlatformReceipt<Write>").nth(1).unwrap();
    assert!(write.contains("-> &impl DurableBarrierQualification"));
    assert!(!write.contains("ReadPremiseQualification"));
    // No generic lending and no conversion between purposes.
    let generic = source.split("impl<P: Purpose> PlatformReceipt<P>").nth(1).unwrap();
    let generic = generic.split("\n}\n").next().unwrap();
    assert!(!generic.contains("qualification"));
    assert!(!source.contains("impl From<") && !source.contains("impl Into<"));
    // Only InitialPlatform implements either sealed qualification.
    for (file, text) in [
        ("read_premise.rs", source),
        ("installation_admission.rs", include_str!("installation_admission.rs")),
        ("ordinary_writer.rs", include_str!("ordinary_writer.rs")),
    ] {
        for trait_name in ["ReadPremiseQualification for", "DurableBarrierQualification for"] {
            for line in text.lines().filter(|line| line.contains(trait_name)) {
                if line.trim_start().starts_with("impl") {
                    assert!(line.contains("for InitialPlatform"), "{file}: {line}");
                }
            }
        }
    }
}

// Law X3a r3 (unit X3a-1): the writer's selected store endpoint.

#[test]
fn an_ordinary_writer_admits_the_store_endpoint_of_the_gates_one_read() {
    churned(|| {
        let f = ReadFixture::new("x3a-writer");
        let producers = read_producers("x3a-writer-write", true, Some(&f.home));
        let receipt = write_receipt(&AtomicBool::new(false), &producers).unwrap();
        let admission = admit_at(receipt, &f.home, &AtomicBool::new(false), None).unwrap();
        let writer = admission.admit_store_endpoint().unwrap();
        let endpoint = writer.endpoint();
        assert_eq!(endpoint.store_instance(), f.store);
        assert_eq!(endpoint.store_generation(), 0);
        assert_eq!(endpoint.nodes().len(), 1);
        // Still under the held fence; release frees it.
        assert!(!fence_free(&f.installation));
        assert!(format!("{writer:?}").starts_with("StoreAdmittedWriter"));
        writer.release().unwrap();
        assert!(fence_free(&f.installation));
    });
}

#[test]
fn a_failed_endpoint_admission_releases_the_fence_with_its_own_row() {
    churned(|| {
        let f = ReadFixture::new("x3a-writer-changed");
        let producers = read_producers("x3a-writer-changed-write", true, Some(&f.home));
        let receipt = write_receipt(&AtomicBool::new(false), &producers).unwrap();
        let admission = admit_at(receipt, &f.home, &AtomicBool::new(false), None).unwrap();
        // An in-place rewrite after the gate's one read: the full recheck sees
        // the changed sample.
        let pair = f.installation.join("selection.pair");
        let bytes = fs::read(&pair).unwrap();
        std::thread::sleep(std::time::Duration::from_millis(5));
        fs::write(&pair, &bytes).unwrap();
        let refused = admission.admit_store_endpoint().unwrap_err();
        assert_eq!(
            refused,
            T::Custody {
                subject: "required-files-changed"
            }
        );
        assert!(fence_free(&f.installation));
    });
}
