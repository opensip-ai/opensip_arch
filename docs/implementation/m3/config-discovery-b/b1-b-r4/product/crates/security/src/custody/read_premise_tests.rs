// Law 458c r5 items 1 to 4 on scratch account homes only: the read side's
// receipt is the creator's InitialCore and InitialPlatform on the process's
// one attempt, with no intent, effect or fence, and every refusal ends in
// its law 468 item 6 row. InitialCore and InitialPlatform come from 462's
// signed on-disk test trees. Nothing here opens the real account's I; the
// one live core refuses at F0 before any installation path is touched.
use super::super::installation_admission::DurableBarrierQualification;
use super::*;
use crate::trust::{ReadProducers, read_producers, receipts_at};
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
    let root = crate::test_scratch::temp_dir().join(format!("opensip-read458c-{nonce}"));
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

/// The composition on a test attempt with its own allocation flag, over the
/// signed test tree's producers.
fn produce(
    flag: &AtomicBool,
    producers: &ReadProducers,
) -> Result<ReadPremiseReceipt, T> {
    produce_on(
        InitialInstallationAttempt::for_tests(flag, None),
        InitialInstallationAttempt::observe_actor,
        |attempt| producers.core(attempt),
        |attempt, actor, core| producers.platform(attempt, actor, core),
    )
}

#[test]
fn a_premise_is_lent_when_the_platform_mints_one_and_its_absence_is_not_a_refusal() {
    let (_scratch, home) = scratch();
    let with = read_producers("read-premise", true, Some(&home));
    let receipt = produce(&AtomicBool::new(false), &with).unwrap();
    assert!(receipt.qualification().omission_premise().is_some());
    // The lending is the same judgment the write gate borrows.
    let sample = receipt.platform.home_filesystem();
    assert!(receipt.qualification().is_home_filesystem(sample));
    assert_eq!(
        receipt.qualification().is_home_filesystem(sample),
        DurableBarrierQualification::is_home_filesystem(&receipt.platform, sample)
    );
    // BASELINE-ATTESTED: admitted, with no premise. Item 5's walk refuses
    // later; minting does not.
    let without = read_producers("read-no-premise", false, Some(&home));
    let receipt = produce(&AtomicBool::new(false), &without).unwrap();
    assert!(receipt.qualification().omission_premise().is_none());
}

#[test]
fn producing_the_receipt_mints_no_intent_and_has_no_effect() {
    let (_scratch, home) = scratch();
    let producers = read_producers("read-no-effect", true, Some(&home));
    let mut receipt = produce(&AtomicBool::new(false), &producers).unwrap();
    // No stage, ancestor, disclosure or fence: H is untouched.
    assert_eq!(entries(&home), 0);
    // The receipt's work stayed on its own attempt, which is still open.
    assert!(!receipt.attempt.is_latched());
    let before = receipt.attempt.used();
    receipt.recheck().unwrap();
    assert!(receipt.attempt.used().edges > before.edges);
    assert_eq!(entries(&home), 0);
    // The live composition takes no command, flag or disclosure writer, so
    // it has nothing to mint an intent from.
    let _: fn() -> Result<ReadPremiseReceipt, T> = produce_read_platform;
}

#[test]
#[allow(clippy::disallowed_methods, reason = "M3-B r5 item 9: the real HOME, only to assert no real installation exists, test-only")]
fn a_development_build_ends_in_the_no_embedded_release_row() {
    // The live actor and the live InitialCore: F0 refuses before any path.
    let result = produce_on(
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
fn a_process_gets_one_attempt() {
    let (_scratch, home) = scratch();
    let producers = read_producers("read-one-attempt", true, Some(&home));
    let flag = AtomicBool::new(false);
    let first = produce(&flag, &producers);
    assert!(first.is_ok());
    drop(first);
    // Even after the first receipt is dropped.
    assert_eq!(produce(&flag, &producers).unwrap_err(), T::Invariant);
}

#[test]
fn account_and_platform_refusals_choose_their_rows() {
    let (_scratch, home) = scratch();
    // An actor refusal ends before InitialCore runs.
    let result = produce_on(
        InitialInstallationAttempt::for_tests(&AtomicBool::new(false), None),
        |_| Err(WorkFailure::Operation(ActorRefusal::HomeSpelling)),
        |_| panic!("InitialCore must not run after the actor refuses"),
        |_, _, _| panic!("InitialPlatform must not run after the actor refuses"),
    );
    assert_eq!(result.unwrap_err(), T::AccountRefused);
    // H on devfs: local, but not a type in installRootFilesystems.
    let devfs = read_producers("read-devfs", true, Some(Path::new("/dev")));
    assert_eq!(
        produce(&AtomicBool::new(false), &devfs).unwrap_err(),
        T::InstallRootFilesystem
    );
    // A ledger refusal is the budget row.
    let result = produce_on(
        InitialInstallationAttempt::for_tests(&AtomicBool::new(false), None),
        |_| {
            Err(WorkFailure::Budget(
                opensip_platform::WorkBudgetError::Edges,
            ))
        },
        |_| panic!("InitialCore must not run after the budget refuses"),
        |_, _, _| panic!("InitialPlatform must not run after the budget refuses"),
    );
    assert_eq!(result.unwrap_err(), T::BudgetExhausted);
    // Sanity: the same scratch H admits with the premise.
    let ok = read_producers("read-ok", true, Some(&home));
    assert!(produce(&AtomicBool::new(false), &ok).is_ok());
}

#[test]
fn a_receipt_of_another_attempt_is_refused() {
    let (_scratch, home) = scratch();
    let other = receipts_at("read-other", true, Some(&home), None);
    let foreign = other.platform;
    let producers = read_producers("read-foreign", true, Some(&home));
    let result = produce_on(
        InitialInstallationAttempt::for_tests(&AtomicBool::new(false), None),
        InitialInstallationAttempt::observe_actor,
        |attempt| producers.core(attempt),
        move |_, _, _| Ok(foreign),
    );
    assert_eq!(result.unwrap_err(), T::Invariant);
}

// Item 1: not Clone. The inherent constant applies only when `R: Clone`;
// otherwise the trait's default is chosen.
trait NotClone {
    const CLONE: bool = false;
}
struct Probe<R>(PhantomData<R>);
impl<R> NotClone for Probe<R> {}
impl<R: Clone> Probe<R> {
    #[allow(dead_code)]
    const CLONE: bool = true;
}

#[test]
fn the_receipt_is_private_opaque_and_lends_only_the_sealed_qualification() {
    const { assert!(!Probe::<ReadPremiseReceipt>::CLONE) };
    let (_scratch, home) = scratch();
    let producers = read_producers("read-opaque", true, Some(&home));
    let receipt = produce(&AtomicBool::new(false), &producers).unwrap();
    assert_eq!(format!("{receipt:?}"), "ReadPremiseReceipt { .. }");
    // The only lending: a sealed qualification that InitialPlatform alone
    // implements.
    fn lent<Q: ReadPremiseQualification>(_: &Q) {}
    lent(receipt.qualification());
}
