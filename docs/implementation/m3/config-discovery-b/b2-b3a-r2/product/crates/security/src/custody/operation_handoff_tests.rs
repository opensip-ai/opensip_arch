// Law X2 r8 item 7a (unit X2e) with law X3b r10 items 1, 3, 3a and 4 (unit
// X3b-3), on scratch homes only. Each test publishes a real P0 under a
// scratch H (`installation_read_fixture`), registers a scratch project with
// an ordinary writer over 462's signed test trees (X2c), and runs the
// handoff on a writer's gate: endpoint join, namespace admission (X2d), the
// floor step at the lease-free point, the lease, the join, the transfer,
// the carrier start and the fence's release; then the end path. Other
// holders are simulated by nonblocking `flock`s on separate descriptors,
// which conflict exactly as another process's would. Tracking reads an
// empty environment and no system sources. Nothing here opens the real
// account's I or runs Git.
use super::super::first_registration::{
    ProjectWriteRefusal, ProjectWriteRow, READERS_LEASE, RegisteredProject, RegistrationRow, Seam,
    WRITER_LEASE,
};
use super::super::installation_admission::{DurableWriteGate, GateSeam, HomeSource};
use super::super::installation_read_fixture::{ReadFixture, churned, private};
use super::super::operation_guard::scripted;
use super::super::ordinary_writer::admit_with;
use super::super::project_admission::ProjectAdmissionRow;
use super::super::read_premise::{Write, produce_for};
use super::*;
use crate::initial_installation::InitialInstallationAttempt;
use crate::trust::{ReadProducers, read_producers};
use opensip_identity::JsonValue as V;
use opensip_platform::{FileLock, LockMode};
use std::collections::{BTreeMap, BTreeSet};
use std::fs::{self, File};
use std::os::unix::fs::{MetadataExt, PermissionsExt};
use std::sync::atomic::AtomicBool;
use std::time::Duration;

// ---------------------------------------------------------------- helpers

/// Unit X4a: a fixture whose P0 trust store is replaced by X4T-0's signed
/// accepted store for its S and K, so the lease-free point's fenced first
/// read admits a view.
fn trusted(tag: &str) -> ReadFixture {
    let fixture = ReadFixture::new(tag);
    fixture.accept_trust();
    fixture
}
/// The handoff on a scripted guard seam: a scripted monitor clock, observer
/// ticks only on request, and a fixed floor-publication invocation.
trait BeginTest {
    fn begin_test(
        self,
        subject: NamespaceSubject,
        lease: WriterLease,
        inputs: &ProjectInputs<'_>,
    ) -> Result<ProjectOperation, OperationRefusal>;
}
impl BeginTest for OrdinaryWriteAdmission {
    fn begin_test(
        self,
        subject: NamespaceSubject,
        lease: WriterLease,
        inputs: &ProjectInputs<'_>,
    ) -> Result<ProjectOperation, OperationRefusal> {
        let clock = scripted::Clock::new();
        self.begin_operation_with(
            subject,
            lease,
            inputs,
            &scripted::invocation(),
            scripted::seam(&clock, crate::trust::ObservationHook::live()),
        )
    }
}

fn directory(path: &Path, mode: u32) {
    fs::create_dir(path).unwrap();
    fs::set_permissions(path, fs::Permissions::from_mode(mode)).unwrap();
}
/// A project under the fixture's H, 0755 with no ACL, as on a stock Mac.
fn fixture_project(fixture: &ReadFixture) -> PathBuf {
    let code = fixture.home.join("code");
    directory(&code, 0o755);
    let project = code.join("project");
    directory(&project, 0o755);
    project
}
/// An ordinary writer on the fixture's I, its attempt ledger capped at
/// `limits` when given, and the signed trees it needs.
fn writer_with(
    fixture: &ReadFixture,
    tag: &str,
    limits: Option<WorkCost>,
) -> (OrdinaryWriteAdmission, ReadProducers) {
    let producers = read_producers(&format!("{tag}-write"), true, Some(&fixture.home));
    let receipt = produce_for::<Write>(
        InitialInstallationAttempt::for_tests(&AtomicBool::new(false), limits),
        InitialInstallationAttempt::observe_actor,
        |attempt| producers.core(attempt),
        |attempt, actor, core| producers.platform(attempt, actor, core),
    )
    .unwrap();
    let admission = admit_with(
        receipt,
        WritePlatformReceipt::recheck,
        || DurableWriteGate::for_tests(&AtomicBool::new(false), None),
        |gate, receipt| {
            gate.admit_with(
                receipt.qualification(),
                HomeSource::Fixture(&fixture.home),
                &GateSeam::live(),
            )
        },
    )
    .unwrap();
    (admission, producers)
}
fn new_writer(fixture: &ReadFixture, tag: &str) -> (OrdinaryWriteAdmission, ReadProducers) {
    writer_with(fixture, tag, None)
}
const NO_GROUPS: &BTreeSet<u32> = &BTreeSet::new();
fn inputs() -> ProjectInputs<'static> {
    ProjectInputs {
        trust_groups: NO_GROUPS,
        environment: &[],
        system_sources: &[],
    }
}
/// The root admission and its tracking observation on the writer's gate.
fn admitted(writer: &mut OrdinaryWriteAdmission, project: &Path) -> NamespaceSubject {
    let admission = writer.admit_project_root(project, None, NO_GROUPS).unwrap();
    let tracking = writer
        .observe_project_tracking_with(&admission, &inputs())
        .unwrap();
    NamespaceSubject::Eligible {
        admission,
        tracking,
    }
}
/// A first registration of `project` on the writer's gate (unit X2c).
fn register(writer: &mut OrdinaryWriteAdmission, project: &Path) -> RegisteredProject {
    let NamespaceSubject::Eligible {
        admission,
        tracking,
    } = admitted(writer, project)
    else {
        unreachable!()
    };
    writer
        .register_first_use_with(admission, tracking, &inputs(), &Seam::live())
        .unwrap()
}
/// A fixture whose project is registered by a writer that has since
/// released its fence: the project is Eligible, and N holds only the leases.
fn eligible(tag: &str) -> (ReadFixture, PathBuf, String) {
    eligible_on(trusted(tag), tag)
}
/// The same, on a fixture whose trust store the caller has already written.
fn eligible_on(fixture: ReadFixture, tag: &str) -> (ReadFixture, PathBuf, String) {
    let project = fixture_project(&fixture);
    let (mut writer, _trees) = new_writer(&fixture, &format!("{tag}-register"));
    let registered = register(&mut writer, &project);
    let n = registered.namespace_id().to_owned();
    drop(registered);
    writer.release().unwrap();
    (fixture, project, n)
}
fn namespace_path(fixture: &ReadFixture, n: &str) -> PathBuf {
    fixture.installation.join(HOST).join(PROJECTS).join(n)
}
fn floor_path(fixture: &ReadFixture, n: &str) -> PathBuf {
    fixture
        .installation
        .join("trust/carrier-floors")
        .join(format!("{n}.v1"))
}
/// Whether another holder could take `mode` on the file at `path` now.
fn free(path: &Path, mode: LockMode) -> bool {
    FileLock::try_acquire(File::open(path).unwrap(), mode)
        .unwrap()
        .is_some()
}
/// Another holder's lock on the file at `path`.
fn hold(path: &Path, mode: LockMode) -> FileLock {
    FileLock::try_acquire(File::open(path).unwrap(), mode)
        .unwrap()
        .unwrap()
}
fn fence_path(fixture: &ReadFixture) -> PathBuf {
    fixture.installation.join("lifecycle.fence")
}
fn fence_free(fixture: &ReadFixture) -> bool {
    free(&fence_path(fixture), LockMode::Exclusive)
}
/// Neither lease carrier of N is locked by anyone.
fn unlocked(fixture: &ReadFixture, n: &str) -> bool {
    let namespace = namespace_path(fixture, n);
    free(&namespace.join(WRITER_LEASE), LockMode::Exclusive)
        && free(&namespace.join(READERS_LEASE), LockMode::Exclusive)
}
/// A closed operational JSON file's members (floor or witness).
fn members(path: &Path) -> BTreeMap<String, V> {
    let raw = fs::read(path).unwrap();
    let end = raw
        .iter()
        .rposition(|b| !b.is_ascii_whitespace())
        .map_or(0, |i| i + 1);
    match crate::trust::metadata::parse(&raw[..end]).unwrap() {
        V::Object(members) => members,
        other => panic!("{other:?}"),
    }
}
fn integer(value: &V) -> i64 {
    match value {
        V::Integer(n) => i64::try_from(n.get()).unwrap(),
        other => panic!("{other:?}"),
    }
}
/// The floor for N: (grant generation, last sequence, tail hash present).
fn floor_of(fixture: &ReadFixture, n: &str) -> (i64, i64, bool) {
    let floor = members(&floor_path(fixture, n));
    (
        integer(&floor["grantGeneration"]),
        integer(&floor["lastSeq"]),
        floor["tailSha256"] != V::Null,
    )
}
/// The witness in N: (generation, sequence, state).
fn witness_of(fixture: &ReadFixture, n: &str) -> (i64, i64, String) {
    let witness = members(&namespace_path(fixture, n).join("grant-journal.witness.json"));
    let V::String(state) = &witness["state"] else {
        panic!("{witness:?}")
    };
    (
        integer(&witness["grantGeneration"]),
        integer(&witness["seq"]),
        state.clone(),
    )
}
fn refusal_row<T: std::fmt::Debug>(result: Result<T, OperationRefusal>) -> OperationRow {
    match result {
        Err(refusal) => refusal.row(),
        Ok(value) => panic!("expected a refusal, got {value:?}"),
    }
}
/// One certain `RA` through the operation's carrier, on the attempt ledger.
fn append_ra(operation: &mut ProjectOperation) {
    use crate::journal_store::{AppendError, RecordDraft};
    operation
        .journal(|location, carrier, _checkpoint, work| {
            let held = carrier.lock().begin(location, work)?.acquire()?;
            held.append(
                &format!("op-{}", "b".repeat(32)),
                &RecordDraft::Ra {
                    request_ref: "request-1".into(),
                },
                work,
            )
            .map_err(|error| match error {
                AppendError::Refused(failure) | AppendError::Undetermined(failure) => failure,
            })
        })
        .unwrap();
}
/// A scripted monotonic clock: each sample is one second after the last,
/// and sleeping takes no time, so S7's 5 s bound runs out at once.
struct Scripted(Duration);
impl WaitClock for Scripted {
    fn now(&mut self) -> io::Result<Duration> {
        self.0 += Duration::from_secs(1);
        Ok(self.0)
    }
    fn sleep(&mut self, _: Duration) {}
}

// ------------------------------------------------------------ the handoff

#[test]
fn a_fresh_registration_hands_off_with_the_carrier_started_and_the_fence_released() {
    churned(|| {
        let fixture = trusted("x2e-fresh");
        let project = fixture_project(&fixture);
        let (mut writer, _trees) = new_writer(&fixture, "x2e-fresh");
        let registered = register(&mut writer, &project);
        let n = registered.namespace_id().to_owned();
        let operation = writer
            .begin_test(
                NamespaceSubject::Registered(registered),
                WriterLease::AppendWrite,
                &inputs(),
            )
            .unwrap();
        // Step 4: the fence is released; the APPEND-WRITE lease is held.
        assert!(fence_free(&fixture));
        let namespace = namespace_path(&fixture, &n);
        assert!(!free(&namespace.join(WRITER_LEASE), LockMode::Exclusive));
        assert!(free(&namespace.join(READERS_LEASE), LockMode::Shared));
        assert_eq!(operation.mode(), LeaseMode::AppendWrite);
        // The floor step wrote the INIT floor; the start created the carrier
        // and its witness `COMMITTED 0` in N.
        assert_eq!(floor_of(&fixture, &n), (1, 0, false));
        assert_eq!(witness_of(&fixture, &n), (1, 0, "COMMITTED".into()));
        assert!(namespace.join("grant-journal.sqlite").exists());
        assert_eq!(operation.carrier().start_tail(), (1, 0, None));
        assert_eq!(
            operation.carrier().created(),
            Some(crate::journal_store::CreationOutcome::Created)
        );
        // Owner §8's binding: N from R2's ACTIVE row, (S, G, K) from the
        // endpoint the gate read once.
        let binding = operation.binding();
        assert_eq!(OperationBinding::SCHEMA_VERSION, 1);
        assert_eq!(binding.namespace_id(), n);
        assert_eq!(operation.row().namespace_id(), n);
        assert_eq!(binding.store_instance(), fixture.store);
        let endpoint = operation.endpoint();
        assert_eq!(binding.store_instance(), endpoint.store_instance());
        assert_eq!(binding.store_generation(), endpoint.store_generation());
        assert_eq!(binding.state_schema(), endpoint.state_schema());
        assert_eq!(
            binding.state_schema(),
            match operation.selected_core().1 {
                StateWriter::Stage1 => 1,
                StateWriter::Stage2 => 2,
            }
        );
        assert!(matches!(
            operation.subject(),
            NamespaceSubject::Registered(_)
        ));
        assert!(!operation.required().is_empty());
        // The end path: the lease, then the fence retaken and released again.
        match operation.end(JournalOutcome::Certain) {
            OperationEnd::Ended(EndOutcome::Unchanged) => {}
            other => panic!("{other:?}"),
        }
        assert!(fence_free(&fixture) && unlocked(&fixture, &n));
        assert_eq!(floor_of(&fixture, &n), (1, 0, false));
    });
}

#[test]
fn the_operation_lends_the_discovery_root_after_the_fence_is_released() {
    // M3-B unit B2-b3a (LD-B2B3-1): the write path's lending, for an
    // eligible root and for a fresh registration.
    churned(|| {
        let (fixture, project, _n) = eligible("b2b3a-root-eligible");
        let (mut writer, _trees) = new_writer(&fixture, "b2b3a-root-eligible");
        let subject = admitted(&mut writer, &project);
        let operation = writer
            .begin_test(subject, WriterLease::AppendWrite, &inputs())
            .unwrap();
        assert!(fence_free(&fixture));
        let root = operation.discovery_root();
        assert_eq!(root.spelling(), project);
        assert_eq!(
            root.root().as_file().metadata().unwrap().ino(),
            fs::metadata(&project).unwrap().ino()
        );
        assert!(root.premise().is_some());
        match operation.end(JournalOutcome::Certain) {
            OperationEnd::Ended(_) => {}
            other => panic!("{other:?}"),
        }
        let fixture = trusted("b2b3a-root-fresh");
        let project = fixture_project(&fixture);
        let (mut writer, _trees) = new_writer(&fixture, "b2b3a-root-fresh");
        let registered = register(&mut writer, &project);
        let operation = writer
            .begin_test(
                NamespaceSubject::Registered(registered),
                WriterLease::AppendWrite,
                &inputs(),
            )
            .unwrap();
        assert!(fence_free(&fixture));
        assert_eq!(operation.discovery_root().spelling(), project);
        match operation.end(JournalOutcome::Certain) {
            OperationEnd::Ended(_) => {}
            other => panic!("{other:?}"),
        }
    });
}

#[test]
fn an_eligible_root_hands_off_and_the_end_copies_the_floor_after_an_append() {
    churned(|| {
        let (fixture, project, n) = eligible("x2e-eligible");
        let (mut writer, _trees) = new_writer(&fixture, "x2e-eligible");
        let subject = admitted(&mut writer, &project);
        let mut operation = writer
            .begin_test(subject, WriterLease::Exclusive, &inputs())
            .unwrap();
        assert!(fence_free(&fixture));
        let namespace = namespace_path(&fixture, &n);
        assert!(!free(&namespace.join(WRITER_LEASE), LockMode::Shared));
        assert!(!free(&namespace.join(READERS_LEASE), LockMode::Shared));
        assert!(matches!(
            operation.subject(),
            NamespaceSubject::Eligible { .. }
        ));
        append_ra(&mut operation);
        // The floor moves only at the end step, never under the lease.
        assert_eq!(floor_of(&fixture, &n), (1, 0, false));
        assert_eq!(witness_of(&fixture, &n), (1, 1, "COMMITTED".into()));
        match operation.end(JournalOutcome::Certain) {
            OperationEnd::Ended(EndOutcome::CopiedForward) => {}
            other => panic!("{other:?}"),
        }
        assert_eq!(floor_of(&fixture, &n), (1, 1, true));
        assert!(fence_free(&fixture) && unlocked(&fixture, &n));

        // The next writer's operation finds the floor at the tail and starts.
        let (mut next, _trees) = new_writer(&fixture, "x2e-eligiblf");
        let subject = admitted(&mut next, &project);
        let operation = next
            .begin_test(subject, WriterLease::AppendWrite, &inputs())
            .unwrap();
        assert_eq!(operation.carrier().start_tail().1, 1);
        assert_eq!(operation.carrier().created(), None);
        assert!(matches!(
            operation.end(JournalOutcome::Certain),
            OperationEnd::Ended(EndOutcome::Unchanged)
        ));
    });
}

#[test]
fn the_floor_step_runs_at_the_lease_free_point_before_the_lease() {
    churned(|| {
        let (fixture, project, n) = eligible("x2e-order");
        // A reader holds `readers.lease`: EXCLUSIVE is busy at its second lock,
        // but the floor step, which runs before any lease, has written the INIT
        // floor with no project lock held. Creation, under the lease, never ran.
        let reader = hold(
            &namespace_path(&fixture, &n).join(READERS_LEASE),
            LockMode::Shared,
        );
        let (mut writer, _trees) = new_writer(&fixture, "x2e-order");
        let subject = admitted(&mut writer, &project);
        let row = refusal_row(writer.begin_test(subject, WriterLease::Exclusive, &inputs()));
        assert_eq!(
            row,
            OperationRow::Project(ProjectWriteRow::Project(RegistrationRow::Busy))
        );
        assert_eq!(floor_of(&fixture, &n), (1, 0, false));
        let namespace = namespace_path(&fixture, &n);
        assert!(!namespace.join("grant-journal.sqlite").exists());
        assert!(!namespace.join("grant-journal.witness.json").exists());
        assert!(fence_free(&fixture));
        assert!(free(&namespace.join(WRITER_LEASE), LockMode::Exclusive));
        drop(reader);
    });
}

#[test]
fn a_busy_writer_lease_skips_the_floor_step_and_the_lease_is_busy() {
    churned(|| {
        let (fixture, project, n) = eligible("x2e-skip");
        let other = hold(
            &namespace_path(&fixture, &n).join(WRITER_LEASE),
            LockMode::Exclusive,
        );
        let (mut writer, _trees) = new_writer(&fixture, "x2e-skip");
        let subject = admitted(&mut writer, &project);
        let row = refusal_row(writer.begin_test(subject, WriterLease::AppendWrite, &inputs()));
        assert_eq!(
            row,
            OperationRow::Project(ProjectWriteRow::Project(RegistrationRow::Busy))
        );
        // The skip wrote nothing: no floor directory, no carrier.
        assert!(!fixture.installation.join("trust/carrier-floors").exists());
        assert!(
            !namespace_path(&fixture, &n)
                .join("grant-journal.sqlite")
                .exists()
        );
        assert!(fence_free(&fixture));
        drop(other);
    });
}

#[test]
fn a_floor_step_quarantine_refuses_before_the_lease_and_writes_nothing() {
    churned(|| {
        let (fixture, project, n) = eligible("x2e-floorlost");
        // A witness in N with no floor: `floorLost` (X3b item 3 step 4).
        let witness = namespace_path(&fixture, &n).join("grant-journal.witness.json");
        fs::write(&witness, b"{}\n").unwrap();
        fs::set_permissions(&witness, fs::Permissions::from_mode(0o600)).unwrap();
        private(&witness);
        let (mut writer, _trees) = new_writer(&fixture, "x2e-floorlost");
        let subject = admitted(&mut writer, &project);
        let row = refusal_row(writer.begin_test(subject, WriterLease::AppendWrite, &inputs()));
        assert_eq!(row, OperationRow::Carrier(CarrierRow::LedgerCorrupt));
        assert!(!fixture.installation.join("trust/carrier-floors").exists());
        assert_eq!(fs::read(&witness).unwrap(), b"{}\n");
        assert!(fence_free(&fixture) && unlocked(&fixture, &n));
    });
}

#[test]
fn a_refusal_after_the_carrier_start_releases_the_lease_then_the_fence() {
    churned(|| {
        // Measure one whole handoff's attempt-ledger use on a twin fixture...
        let (twin, twin_project, _) = eligible("x2e-cut-a");
        let (mut measured, _trees) = new_writer(&twin, "x2e-cut-a");
        let subject = admitted(&mut measured, &twin_project);
        let operation = measured
            .begin_test(subject, WriterLease::AppendWrite, &inputs())
            .unwrap();
        let total = operation.attempt_used();
        drop(operation);
        // ...then cap this writer's attempt ledger one byte short of it. The
        // handoff's last attempt charge (the receipt's recheck after the
        // post-start recheck) is refused after the carrier started.
        let (fixture, project, n) = eligible("x2e-cut-b");
        let cut = WorkCost {
            bytes: total.bytes - 1,
            ..total
        };
        let (mut writer, _trees) = writer_with(&fixture, "x2e-cut-b", Some(cut));
        let subject = admitted(&mut writer, &project);
        let result = writer.begin_test(subject, WriterLease::AppendWrite, &inputs());
        match &result {
            Err(OperationRefusal::Project(ProjectWriteRefusal::Receipt(row))) => {
                assert_eq!(row, &T::BudgetExhausted);
            }
            other => panic!("{other:?}"),
        }
        // The carrier started, then the lock, the lease and the fence went.
        assert_eq!(witness_of(&fixture, &n), (1, 0, "COMMITTED".into()));
        assert!(fence_free(&fixture) && unlocked(&fixture, &n));
        // The next writer reconciles and starts on what the refused one left.
        let (mut next, _trees) = new_writer(&fixture, "x2e-cut-c");
        let subject = admitted(&mut next, &project);
        let operation = next
            .begin_test(subject, WriterLease::AppendWrite, &inputs())
            .unwrap();
        assert_eq!(operation.carrier().created(), None);
        assert_eq!(operation.carrier().start_tail(), (1, 0, None));
    });
}

// ------------------------------------------------------------ the end path

#[test]
fn an_uncertain_outcome_releases_the_lease_and_takes_no_fence() {
    churned(|| {
        let (fixture, project, n) = eligible("x2e-uncertain");
        let (mut writer, _trees) = new_writer(&fixture, "x2e-uncertain");
        let subject = admitted(&mut writer, &project);
        let mut operation = writer
            .begin_test(subject, WriterLease::AppendWrite, &inputs())
            .unwrap();
        append_ra(&mut operation);
        // Another invocation holds the fence: a fence wait would block, and a
        // copy would move the floor. Neither happens.
        let fence = hold(&fence_path(&fixture), LockMode::Exclusive);
        match operation.end_with(
            JournalOutcome::Uncertain,
            &mut Scripted(Duration::ZERO),
            operation_end_after_exhaustion,
        ) {
            OperationEnd::NotEntered => {}
            other => panic!("{other:?}"),
        }
        assert!(unlocked(&fixture, &n));
        assert_eq!(floor_of(&fixture, &n), (1, 0, false));
        drop(fence);
        // The next writer's floor step copies it forward.
        let (mut next, _trees) = new_writer(&fixture, "x2e-uncertaio");
        let subject = admitted(&mut next, &project);
        let operation = next
            .begin_test(subject, WriterLease::AppendWrite, &inputs())
            .unwrap();
        assert_eq!(floor_of(&fixture, &n), (1, 1, true));
        assert_eq!(operation.carrier().start_tail().1, 1);
    });
}

#[test]
fn a_busy_fence_at_the_end_is_waited_for_within_the_bound_then_disclosed() {
    churned(|| {
        let (fixture, project, n) = eligible("x2e-endbusy");
        let (mut writer, _trees) = new_writer(&fixture, "x2e-endbusy");
        let subject = admitted(&mut writer, &project);
        let mut operation = writer
            .begin_test(subject, WriterLease::AppendWrite, &inputs())
            .unwrap();
        append_ra(&mut operation);
        let fence = hold(&fence_path(&fixture), LockMode::Exclusive);
        let failure = match operation.end_with(
            JournalOutcome::Certain,
            &mut Scripted(Duration::ZERO),
            operation_end_after_exhaustion,
        ) {
            OperationEnd::Failed(failure) => failure,
            other => panic!("{other:?}"),
        };
        assert_eq!(failure.row(), OperationRow::Installation(T::Busy));
        // The lease went first; nothing was copied.
        assert!(unlocked(&fixture, &n));
        assert_eq!(floor_of(&fixture, &n), (1, 0, false));
        drop(fence);
    });
}

#[test]
fn a_closed_attempt_ledger_does_not_enter_the_end_step() {
    churned(|| {
        let (fixture, project, n) = eligible("x2e-closed");
        let (mut writer, _trees) = new_writer(&fixture, "x2e-closed");
        let subject = admitted(&mut writer, &project);
        let mut operation = writer
            .begin_test(subject, WriterLease::AppendWrite, &inputs())
            .unwrap();
        append_ra(&mut operation);
        // A certain refusal on the attempt ledger closes it for good.
        assert!(
            operation
                .journal::<(), ()>(|_, _, _, _| Err(WorkFailure::Operation(())))
                .is_err()
        );
        assert!(operation.attempt_closed());
        // X3b r10 item 4: the end step is not entered. The fence is held
        // elsewhere, so a walk would wait; none is attempted, nothing is read
        // or copied, and nothing is disclosed.
        let fence = hold(&fence_path(&fixture), LockMode::Exclusive);
        match operation.end_with(
            JournalOutcome::Certain,
            &mut Scripted(Duration::ZERO),
            operation_end_after_exhaustion,
        ) {
            OperationEnd::NotEntered => {}
            other => panic!("{other:?}"),
        }
        assert!(unlocked(&fixture, &n));
        assert_eq!(floor_of(&fixture, &n), (1, 0, false));
        drop(fence);
        // The next writer's floor step copies it forward.
        let (mut next, _trees) = new_writer(&fixture, "x2e-closee");
        let subject = admitted(&mut next, &project);
        let operation = next
            .begin_test(subject, WriterLease::AppendWrite, &inputs())
            .unwrap();
        assert_eq!(floor_of(&fixture, &n), (1, 1, true));
        assert_eq!(operation.carrier().start_tail().1, 1);
    });
}

#[test]
fn a_moved_namespace_at_the_end_refuses_the_copy_and_releases_the_fence() {
    churned(|| {
        let (fixture, project, n) = eligible("x2e-moved");
        let (mut writer, _trees) = new_writer(&fixture, "x2e-moved");
        let subject = admitted(&mut writer, &project);
        let mut operation = writer
            .begin_test(subject, WriterLease::AppendWrite, &inputs())
            .unwrap();
        append_ra(&mut operation);
        let namespace = namespace_path(&fixture, &n);
        let moved = namespace.with_file_name("moved");
        fs::rename(&namespace, &moved).unwrap();
        let failure = match operation.end(JournalOutcome::Certain) {
            OperationEnd::Failed(failure) => failure,
            other => panic!("{other:?}"),
        };
        assert_eq!(
            failure.row(),
            OperationRow::Project(ProjectWriteRow::Project(RegistrationRow::Admission(
                ProjectAdmissionRow::RequiredFilesChanged
            )))
        );
        assert!(fence_free(&fixture));
        assert_eq!(floor_of(&fixture, &n), (1, 0, false));
    });
}

#[test]
fn an_exhausted_generation_rolls_over_under_the_retaken_fence_then_copies_the_floor() {
    churned(|| {
        use crate::journal_store::plant_committed_tail_for_tests;
        // X3b r10 item 5a: no SEAL fits after 9007199254740987.
        const EXHAUSTED: i64 = 9_007_199_254_740_990;
        let (fixture, project, n) = eligible("x2e-rollover");
        // A first operation creates the carrier; then the generation is filled
        // to an exhausted tail with X3b-2's reserved-slot technique.
        let (mut writer, _trees) = new_writer(&fixture, "x2e-rollover");
        let subject = admitted(&mut writer, &project);
        let operation = writer
            .begin_test(subject, WriterLease::AppendWrite, &inputs())
            .unwrap();
        assert!(matches!(
            operation.end(JournalOutcome::Certain),
            OperationEnd::Ended(EndOutcome::Unchanged)
        ));
        plant_committed_tail_for_tests(&namespace_path(&fixture, &n), &n, EXHAUSTED);
        // The next operation's floor step copies the floor to that tail.
        let (mut next, _trees) = new_writer(&fixture, "x2e-rollovfr");
        let subject = admitted(&mut next, &project);
        let operation = next
            .begin_test(subject, WriterLease::AppendWrite, &inputs())
            .unwrap();
        assert_eq!(operation.carrier().start_tail().1, EXHAUSTED);
        assert_eq!(floor_of(&fixture, &n), (1, EXHAUSTED, true));
        // X3d reports `CarrierCapacityExhausted`: the end step rolls over under
        // the retaken fence, then copies the floor to G+1's empty tail.
        let ended = operation.end(JournalOutcome::Exhausted {
            exhaustion: CapacityExhaustion::new(1, EXHAUSTED),
            operation_ref: format!("op-{}", "d".repeat(32)),
        });
        match ended {
            OperationEnd::RolledOver {
                rollover: RolloverOutcome::Rolled { closed, opened: 2 },
                end: Ok(EndOutcome::CopiedForward),
            } => assert_eq!(closed, (1, EXHAUSTED + 1)),
            other => panic!("{other:?}"),
        }
        assert_eq!(witness_of(&fixture, &n), (2, 0, "COMMITTED".into()));
        assert_eq!(floor_of(&fixture, &n), (2, 0, false));
        assert!(fence_free(&fixture) && unlocked(&fixture, &n));
        // The next writer starts in generation 2.
        let (mut third, _trees) = new_writer(&fixture, "x2e-rollovgr");
        let subject = admitted(&mut third, &project);
        let operation = third
            .begin_test(subject, WriterLease::AppendWrite, &inputs())
            .unwrap();
        assert_eq!(operation.carrier().start_tail(), (2, 0, None));
    });
}

// ------------------------------------- the rollover's outcome is kept

/// An exhausted tail: no `SEAL` fits after 9007199254740987 (X3b r10 5a).
const EXHAUSTED: i64 = 9_007_199_254_740_990;
fn exhausted() -> JournalOutcome {
    JournalOutcome::Exhausted {
        exhaustion: CapacityExhaustion::new(1, EXHAUSTED),
        operation_ref: format!("op-{}", "d".repeat(32)),
    }
}
/// A project whose generation 1 is exhausted at `EXHAUSTED` (a first
/// operation creates the carrier, then X3b-2's reserved-slot technique
/// fills it), and an operation begun on it by a writer whose attempt ledger
/// is capped at `limits`. Twins must use tags of equal length.
fn exhausted_operation(
    tag: &str,
    limits: Option<WorkCost>,
) -> (ReadFixture, String, ProjectOperation, [ReadProducers; 2]) {
    use crate::journal_store::plant_committed_tail_for_tests;
    let (fixture, project, n) = eligible(tag);
    let (mut first, first_trees) = new_writer(&fixture, tag);
    let subject = admitted(&mut first, &project);
    let operation = first
        .begin_test(subject, WriterLease::AppendWrite, &inputs())
        .unwrap();
    assert!(matches!(
        operation.end(JournalOutcome::Certain),
        OperationEnd::Ended(EndOutcome::Unchanged)
    ));
    plant_committed_tail_for_tests(&namespace_path(&fixture, &n), &n, EXHAUSTED);
    let (mut writer, trees) = writer_with(&fixture, &format!("{tag}-x"), limits);
    let subject = admitted(&mut writer, &project);
    let operation = writer
        .begin_test(subject, WriterLease::AppendWrite, &inputs())
        .unwrap();
    assert_eq!(operation.carrier().start_tail().1, EXHAUSTED);
    (fixture, n, operation, [first_trees, trees])
}
/// Nothing of generation 2 exists, the floor is still at the exhausted
/// tail, and nothing is locked.
fn not_rolled(fixture: &ReadFixture, n: &str) {
    assert_eq!(witness_of(fixture, n), (1, EXHAUSTED, "COMMITTED".into()));
    assert_eq!(floor_of(fixture, n), (1, EXHAUSTED, true));
    assert!(fence_free(fixture) && unlocked(fixture, n));
}
fn end_at(operation: ProjectOperation, points: &crate::journal_store::TestPoints) -> OperationEnd {
    operation.end_with(
        exhausted(),
        &mut Scripted(Duration::ZERO),
        |location, exhaustion, released, work| {
            crate::journal_store::end_step_after_exhaustion_at(
                location, exhaustion, released, points, work,
            )
        },
    )
}
fn floor_file(fixture: &ReadFixture, n: &str, mode: u32) {
    fs::set_permissions(floor_path(fixture, n), fs::Permissions::from_mode(mode)).unwrap();
}

#[test]
fn a_failed_rollover_reservation_is_returned_with_no_copy() {
    churned(|| {
        // Measure a twin's attempt ledger after the handoff, then leave this
        // writer room for the end walk and rebinds (well under 1 MiB) but not
        // for the rollover's reservation (several MiB, X3b r10 item 9).
        let (_twin, _, measured, _trees) = exhausted_operation("x2e-rsv-a", None);
        let used = measured.attempt_used();
        drop(measured);
        // Objects and edges stay at the platform's maxima; bytes bind.
        let cap = WorkCost {
            objects: 65_536,
            edges: 131_072,
            bytes: used.bytes + (1 << 20),
        };
        let (fixture, n, operation, _trees) = exhausted_operation("x2e-rsv-b", Some(cap));
        match operation.end(exhausted()) {
            OperationEnd::RolledOver {
                rollover: RolloverOutcome::Refused(WorkFailure::Budget(_)),
                end: Ok(EndOutcome::NotCopied),
            } => {}
            other => panic!("{other:?}"),
        }
        not_rolled(&fixture, &n);
    });
}

#[test]
fn a_busy_writer_lease_skips_the_rollover_and_the_copy() {
    churned(|| {
        use crate::journal_store::{RolloverStep, TestPoints};
        let (fixture, n, operation, _trees) = exhausted_operation("x2e-skp-a", None);
        // Another writer takes `writer.lease` after this operation released it
        // and before the rollover's EXCLUSIVE (at X3b-4's `Reserved` point).
        let carrier = namespace_path(&fixture, &n).join(WRITER_LEASE);
        let other = std::sync::Arc::new(std::sync::Mutex::new(None));
        let taken = std::sync::Arc::clone(&other);
        let points = TestPoints {
            step: Some(std::sync::Arc::new(move |step| {
                if step == RolloverStep::Reserved {
                    *taken.lock().unwrap() = Some(hold(&carrier, LockMode::Exclusive));
                }
                None
            })),
            ..TestPoints::default()
        };
        match end_at(operation, &points) {
            OperationEnd::RolledOver {
                rollover: RolloverOutcome::Skipped,
                end: Ok(EndOutcome::Skipped),
            } => {}
            other => panic!("{other:?}"),
        }
        assert!(other.lock().unwrap().is_some());
        drop(other.lock().unwrap().take());
        not_rolled(&fixture, &n);
    });
}

#[test]
fn an_io_refusal_inside_the_rollover_is_returned_on_its_own_row() {
    churned(|| {
        let (fixture, n, operation, _trees) = exhausted_operation("x2e-iof-a", None);
        // The rollover's observation reads the floor (item 13 step 3), and so
        // does the copy after it: both refuse on the host I/O row, and both
        // are returned.
        floor_file(&fixture, &n, 0o000);
        let ended = operation.end(exhausted());
        floor_file(&fixture, &n, 0o600);
        match ended {
            OperationEnd::RolledOver {
                rollover: rollover @ RolloverOutcome::Refused(WorkFailure::Operation(_)),
                end: Err(failure),
            } => {
                assert_eq!(rollover.row(), Some(CarrierRow::HostIo));
                assert_eq!(failure.row(), OperationRow::Carrier(CarrierRow::HostIo));
            }
            other => panic!("{other:?}"),
        }
        not_rolled(&fixture, &n);
    });
}

#[test]
fn an_undetermined_rollover_is_returned_for_its_durability_row() {
    churned(|| {
        use crate::journal_store::{Fault, RolloverStep, TestPoints};
        let (fixture, n, operation, _trees) = exhausted_operation("x2e-und-a", None);
        // OPEN's witness publication fails after visibility (X3b-4's point).
        let points = TestPoints {
            step: Some(std::sync::Arc::new(|step| {
                (step == RolloverStep::Opened).then_some(Fault::Fail)
            })),
            ..TestPoints::default()
        };
        match end_at(operation, &points) {
            OperationEnd::RolledOver {
                rollover: rollover @ RolloverOutcome::Undetermined(_),
                end: Ok(EndOutcome::NotCopied),
            } => assert_eq!(rollover.row(), Some(CarrierRow::DurabilityUndetermined)),
            other => panic!("{other:?}"),
        }
        // Nothing followed: the floor was not copied; the next writer's floor
        // step and start take it from the durable state.
        assert_eq!(floor_of(&fixture, &n), (1, EXHAUSTED, true));
        assert!(fence_free(&fixture) && unlocked(&fixture, &n));
    });
}

#[test]
fn a_failed_copy_after_a_rollover_keeps_the_rolled_outcome() {
    churned(|| {
        use crate::journal_store::TestPoints;
        let (fixture, n, operation, _trees) = exhausted_operation("x2e-cpy-a", None);
        // After the rollover released its lease, the floor becomes unreadable,
        // so the end step's copy (steps 4 and 5) fails.
        let floor = floor_path(&fixture, &n);
        let points = TestPoints {
            step: Some(std::sync::Arc::new(move |step| {
                if step == crate::journal_store::RolloverStep::WriterReleased {
                    fs::set_permissions(&floor, fs::Permissions::from_mode(0o000)).unwrap();
                }
                None
            })),
            ..TestPoints::default()
        };
        let ended = end_at(operation, &points);
        floor_file(&fixture, &n, 0o600);
        match ended {
            OperationEnd::RolledOver {
                rollover: RolloverOutcome::Rolled { closed, opened: 2 },
                end: Err(failure),
            } => {
                assert_eq!(closed, (1, EXHAUSTED + 1));
                assert_eq!(failure.row(), OperationRow::Carrier(CarrierRow::HostIo));
            }
            other => panic!("{other:?}"),
        }
        // Generation 2 is open; the floor is still in generation 1.
        assert_eq!(witness_of(&fixture, &n), (2, 0, "COMMITTED".into()));
        assert_eq!(floor_of(&fixture, &n), (1, EXHAUSTED, true));
        assert!(fence_free(&fixture) && unlocked(&fixture, &n));
    });
}

// ------------------------------------------------------------ the seams

#[test]
fn the_carrier_location_has_no_production_constructor_but_the_admitted_place() {
    let floor = include_str!("../journal_store/carrier_floor.rs");
    let operation = include_str!("../journal_store/carrier_operation.rs");
    let handoff = include_str!("operation_handoff.rs");
    // carrier_floor builds a location only in its `cfg(test)` constructor.
    let for_tests = floor.find("pub(crate) fn for_tests(").unwrap();
    assert!(floor[..for_tests].trim_end().ends_with("#[cfg(test)]"));
    assert_eq!(floor.matches("CarrierLocation {").count(), 0);
    // The one production constructor takes X2e's place, and only this
    // module builds a place.
    assert!(operation.contains("pub(crate) fn admitted(place: &CarrierPlace<'a>) -> Self"));
    assert!(!handoff.contains("for_tests("));
    assert!(handoff.contains("pub(crate) struct CarrierPlace<'a> {\n    trust:"));
}

// Law X4 r7 (unit X4a): the live guards through this handoff.
mod live {
    use super::*;
    include!("operation_live_tests.rs");
}
mod session {
    use super::*;
    include!("commit_session_tests.rs");
}
