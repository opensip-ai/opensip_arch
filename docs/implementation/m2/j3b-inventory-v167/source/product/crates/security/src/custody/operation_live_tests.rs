// Law X4 r7 (unit X4a) through the real handoff, on scratch homes only:
// each test publishes a real P0 under a scratch H, replaces its trust store
// with X4T-0's signed accepted store for the same S and K, and runs the
// handoff with a scripted monitor clock and observer ticks on request.
// Nothing sleeps; nothing here qualifies native scheduling. Nothing opens
// the real account's I.
use super::super::super::installation_read_fixture::churned;
use super::super::super::operation_guard::{GuardRefusal, StopCause};
use crate::commit_authority::AttemptState;
use crate::journal_store::{AppendError, RecordDraft};
use crate::trust::{ObservationHook, ObservationPoint};
use std::sync::Arc;

/// A started operation on `fixture` with its own clock.
struct Live {
    operation: ProjectOperation,
    clock: scripted::Clock,
    /// The writer's signed trees: the receipt's core recheck reads them.
    _trees: ReadProducers,
}
fn begin_live(
    fixture: &ReadFixture,
    project: &Path,
    tag: &str,
    registered: bool,
    hook: ObservationHook,
) -> Result<Live, OperationRefusal> {
    let (mut writer, trees) = new_writer(fixture, tag);
    let subject = if registered {
        NamespaceSubject::Registered(register(&mut writer, project))
    } else {
        admitted(&mut writer, project)
    };
    let clock = scripted::Clock::new();
    let operation = writer.begin_operation_with(
        subject,
        WriterLease::AppendWrite,
        &inputs(),
        &scripted::invocation(),
        scripted::seam(&clock, hook),
    )?;
    Ok(Live {
        operation,
        clock,
        _trees: trees,
    })
}
fn eligible_live(tag: &str) -> (ReadFixture, PathBuf, String, Live) {
    let (fixture, project, n) = eligible(tag);
    let live = begin_live(&fixture, &project, tag, false, ObservationHook::live()).unwrap();
    (fixture, project, n, live)
}
fn current_path(fixture: &ReadFixture) -> PathBuf {
    fixture
        .installation
        .join(format!("trust/stores/{}/state.v1", fixture.store))
}

/// What a checkpoint inside one journal step returned.
#[derive(Debug)]
enum Checked {
    Effect,
    Permit(&'static str),
}
/// X3d's shape: level 3, then level 4, then X4's checkpoint over the
/// level-4 borrow (an effect check, or the final admission binding a
/// prepared value), then an `RA` for an effect.
fn checkpoint(operation: &mut ProjectOperation, admit: bool) -> Result<Checked, GuardRefusal> {
    let mut refused = None;
    let result = operation.journal::<Checked, ()>(|location, carrier, checkpoint, work| {
        let held = carrier
            .lock()
            .begin(location, work)
            .and_then(|transaction| transaction.acquire())
            .map_err(|_| WorkFailure::Operation(()))?;
        if admit {
            return match checkpoint.admit(&held, "prepared-commit", work) {
                Ok(permit) => Ok(Checked::Permit(permit.consume(|prepared| prepared))),
                Err((refusal, prepared)) => {
                    assert_eq!(prepared, "prepared-commit");
                    refused = Some(refusal);
                    Err(WorkFailure::Operation(()))
                }
            };
        }
        match checkpoint.effect(&held, work) {
            Ok(_) => {
                held.append(
                    &format!("op-{}", "c".repeat(32)),
                    &RecordDraft::Ra {
                        request_ref: "request-x4a".into(),
                    },
                    work,
                )
                .map_err(|error| match error {
                    AppendError::Refused(_) | AppendError::Undetermined(_) => {
                        WorkFailure::Operation(())
                    }
                })?;
                Ok(Checked::Effect)
            }
            Err(refusal) => {
                refused = Some(refusal);
                Err(WorkFailure::Operation(()))
            }
        }
    });
    match (result, refused) {
        (Ok(checked), _) => Ok(checked),
        (Err(_), Some(refusal)) => Err(refusal),
        (Err(failure), None) => panic!("{failure:?}"),
    }
}
fn stopped(refusal: Result<Checked, GuardRefusal>) -> StopCause {
    match refusal {
        Err(GuardRefusal::Stopped(cause)) => cause,
        other => panic!("{other:?}"),
    }
}
fn fail_stop(subject: &'static str) -> StopCause {
    StopCause::FailStop { subject }
}

// ----------------------------------------------- the lease-free point

#[test]
fn the_first_read_admits_the_start_view_before_any_lease_and_the_guard_carries_it() {
    churned(|| {
        let (fixture, project, n) = eligible("x4a-first");
        let before = fs::read(current_path(&fixture)).unwrap();
        let live = begin_live(
            &fixture,
            &project,
            "x4a-first",
            false,
            ObservationHook::live(),
        )
        .unwrap();
        let guard = live.operation.guard();
        assert_eq!(guard.state(), AttemptState::Preparing);
        assert_eq!(guard.cause(), None);
        let epoch = guard.start_view().epoch();
        assert_eq!(
            (
                epoch.root_version,
                epoch.index_snapshot_version,
                epoch.revocation_version
            ),
            (1, 1, 1)
        );
        // The S4 write-ahead published a new `state.v1` under the fence, and the
        // gate's own recheck set followed it (the handoff completed).
        assert_ne!(fs::read(current_path(&fixture)).unwrap(), before);
        assert!(fence_free(&fixture));
        // One observer tick: the same store, no drift, nothing latched.
        assert!(guard.tick());
        assert_eq!(guard.state(), AttemptState::Preparing);
        assert!(guard.drift().is_empty());
        drop(live);
        assert!(fence_free(&fixture) && unlocked(&fixture, &n));
    });
}

/// What the probe saw at each monitor clock sample of the handoff.
#[derive(Clone, Debug)]
struct Probed {
    sample: crate::revocation::Sample,
    state: Vec<u8>,
    fence_held: bool,
    leases_free: bool,
}
#[test]
fn a_p0_installation_is_accepted_inside_the_first_read_before_any_lease() {
    churned(|| {
        // Law X4B r5 item 1 (unit X4B-b): the P0 capsule is F absent (X4T item
        // 1). The monitor's one first read accepts the write receipt's embedded
        // bootstrap payload on its own opening sample and returns the one
        // confirming admission's view; the gate follows the confirmed `state.v1`.
        use super::super::super::operation_guard::{Cadence, GuardSeam};
        let fixture = ReadFixture::new("x4bb-p0");
        let project = fixture_project(&fixture);
        let (mut writer, _trees) = new_writer(&fixture, "x4bb-p0-register");
        let registered = register(&mut writer, &project);
        let n = registered.namespace_id().to_owned();
        drop(registered);
        writer.release().unwrap();
        let p0 = fs::read(current_path(&fixture)).unwrap();
        // A scripted clock that records, at every sample, the pointer and the
        // locks: the first read's bracket is samples 1 and 2.
        let clock = scripted::Clock::new();
        let probed = Arc::new(std::sync::Mutex::new(Vec::<Probed>::new()));
        let seam = {
            let (clock, probed) = (clock.clone(), Arc::clone(&probed));
            let (path, fence, namespace) = (
                current_path(&fixture),
                fence_path(&fixture),
                namespace_path(&fixture, &n),
            );
            GuardSeam {
                clock: Box::new(move || {
                    let sample = clock.sample()?;
                    let lock_free = |path: &Path, mode| {
                        FileLock::try_acquire(File::open(path).unwrap(), mode)
                            .unwrap()
                            .is_some()
                    };
                    probed.lock().unwrap().push(Probed {
                        sample: sample.clone(),
                        state: fs::read(&path).unwrap(),
                        fence_held: !lock_free(&fence, LockMode::Exclusive),
                        leases_free: lock_free(&namespace.join(WRITER_LEASE), LockMode::Exclusive)
                            && lock_free(&namespace.join(READERS_LEASE), LockMode::Exclusive),
                    });
                    Ok(sample)
                }),
                cadence: Cadence::Manual,
                hook: ObservationHook::live(),
            }
        };
        let (mut writer, _trees) = new_writer(&fixture, "x4bb-p0");
        let subject = admitted(&mut writer, &project);
        let operation = writer
            .begin_operation_with(
                subject,
                WriterLease::AppendWrite,
                &inputs(),
                &scripted::invocation(),
                seam,
            )
            .unwrap();
        let probed = probed.lock().unwrap().clone();
        let (opening, closing) = (&probed[0], &probed[1]);
        // The bracket opened on P0, under the fence and before any lease, and
        // closed on the accepted state.v1, still before any lease: the F-absent
        // admission, the acceptance and the confirming admission all ran inside
        // the monitor's one first read.
        assert_eq!(opening.state, p0);
        assert!(opening.fence_held && opening.leases_free);
        let accepted = fs::read(current_path(&fixture)).unwrap();
        assert_ne!(accepted, p0);
        assert_eq!(closing.state, accepted);
        assert!(closing.fence_held && closing.leases_free);
        // Item 3: the anchor is the opening sample's projection, and F is
        // max(W, A) on that sample's wall clock (W is past A here).
        let capsule = opensip_identity::parse_json(&accepted).unwrap();
        let field = |v: &V, k: &str| match v {
            V::Object(o) => o[k].clone(),
            _ => panic!("{k}"),
        };
        let record = field(&field(&capsule, "clock"), "record");
        let observation = crate::clock_observation::project_monitor_sample(
            opening.sample.wall_seconds,
            opening.sample.wall_nanos,
            opening.sample.before,
            opening.sample.after,
            &opening.sample.boot,
        )
        .unwrap();
        assert_eq!(field(&record, "anchor"), observation);
        assert_eq!(
            field(&record, "evalHighWater"),
            V::String(crate::trust_time::format_timestamp(opening.sample.wall_seconds).unwrap())
        );
        // The returned view is the confirming admission's: the carried roles
        // are trusted, and the confirming admission wrote nothing (revision 2).
        let guard = operation.guard();
        assert_eq!(
            format!("{:?}", guard.start_view().standing()),
            "InstallGateRequiredForNewProcess"
        );
        assert_eq!(
            field(&capsule, "revision"),
            V::Integer(opensip_identity::JsonInteger::new(2).unwrap())
        );
        for name in ["TR-BUNDLE", "TR-COMPONENT", "TR-CORE", "TR-INDEX"] {
            let role = field(&field(&capsule, "roles"), name);
            assert_eq!(
                field(&role, "state"),
                V::String("ST-TRUSTED".into()),
                "{name}"
            );
        }
        // The handoff completed, so the gate's recheck set followed the
        // confirmed publication; one observer tick reads the same store.
        assert!(guard.tick());
        assert_eq!(guard.state(), AttemptState::Preparing);
        drop(operation);
        assert!(fence_free(&fixture) && unlocked(&fixture, &n));
        // The next operation finds F present and accepts nothing again: on the
        // same sample, nothing is written.
        let live = begin_live(
            &fixture,
            &project,
            "x4bb-p0-next",
            false,
            ObservationHook::live(),
        )
        .unwrap();
        assert_eq!(fs::read(current_path(&fixture)).unwrap(), accepted);
        drop(live);
    });
}

// ------------------------------------------------------- the checkpoint

#[test]
fn the_final_admission_mints_one_permit_and_a_late_latch_keeps_its_outcome() {
    churned(|| {
        let (fixture, _project, n, mut live) = eligible_live("x4a-admit");
        // An effect checkpoint, then its RA; then the commit admission.
        assert!(matches!(
            checkpoint(&mut live.operation, false),
            Ok(Checked::Effect)
        ));
        assert_eq!(witness_of(&fixture, &n), (1, 1, "COMMITTED".into()));
        match checkpoint(&mut live.operation, true) {
            Ok(Checked::Permit(prepared)) => assert_eq!(prepared, "prepared-commit"),
            other => panic!("{other:?}"),
        }
        assert_eq!(live.operation.guard().state(), AttemptState::Admitted);
        // F39's gate half: a revoking observation after admission takes 1 to 3;
        // the admitted outcome above is not relabelled.
        let closure = live.operation.selected_core().0.to_owned();
        fixture.swap_trust(vec![("release", closure)], 2);
        assert!(!live.operation.guard().tick());
        assert_eq!(
            live.operation.guard().state(),
            AttemptState::AdmittedThenLatched
        );
        // No further effect or admission: it names the first cause.
        let revoked = StopCause::Revoked {
            subject: "trust-revoked",
        };
        assert_eq!(stopped(checkpoint(&mut live.operation, true)), revoked);

        // F41: a second admission finds the gate at 1. There is no second
        // permit; the refusal latches 1 to 3.
        let (_fixture, _project, _n, mut live) = eligible_live("x4a-admit-twice");
        assert!(matches!(
            checkpoint(&mut live.operation, true),
            Ok(Checked::Permit(_))
        ));
        assert_eq!(
            stopped(checkpoint(&mut live.operation, true)),
            fail_stop("latched")
        );
        assert_eq!(
            live.operation.guard().state(),
            AttemptState::AdmittedThenLatched
        );
    });
}

#[test]
fn a_pause_beyond_the_bound_after_the_first_read_fail_stops_before_any_effect() {
    churned(|| {
        let (fixture, _project, n, mut live) = eligible_live("x4a-pause");
        // The lease-free capture's earliest instant bounds the first checkpoint's
        // read: 10 s plus the read's own span is past the bound.
        live.clock.advance(Duration::from_secs(10));
        let cause = stopped(checkpoint(&mut live.operation, false));
        assert_eq!(cause, fail_stop("stalled"));
        assert_eq!(
            cause.row(),
            OperationRow::Installation(T::ObserverFailStop { subject: "stalled" })
        );
        assert_eq!(
            live.operation.guard().state(),
            AttemptState::LatchedBeforeAdmission
        );
        // No effect: the carrier holds no RA (F18). The certain refusal closed
        // the attempt ledger, so nothing further is charged or admitted.
        assert_eq!(witness_of(&fixture, &n), (1, 0, "COMMITTED".into()));
        assert!(live.operation.attempt_closed());
        assert_eq!(live.operation.guard().cause(), Some(cause));
    });
}

#[test]
fn ticks_and_checkpoints_share_one_monitor_history() {
    churned(|| {
        let (_fixture, _project, _n, mut live) = eligible_live("x4a-shared");
        // 9 s after the first read, a tick reads; 9 s after that a checkpoint
        // admits, bounded from the tick's earliest instant, not the first read's.
        live.clock.advance(Duration::from_secs(9));
        assert!(live.operation.guard().tick());
        live.clock.advance(Duration::from_secs(9));
        assert!(matches!(
            checkpoint(&mut live.operation, false),
            Ok(Checked::Effect)
        ));
        // And the checkpoint's read bounds the next tick in turn.
        live.clock.advance(Duration::from_secs(9));
        assert!(live.operation.guard().tick());
        assert_eq!(live.operation.guard().state(), AttemptState::Preparing);
    });
}

#[test]
fn a_pause_after_the_final_observation_fails_the_admission_boundary() {
    churned(|| {
        let (_fixture, _project, _n, mut live) = eligible_live("x4a-boundary");
        assert!(live.operation.guard().tick());
        // Each later sample is 6 s after the last: the final observation's read
        // is within the bound from the tick, but the boundary sample is 12 s
        // after that read's earliest instant (item 3 step 4).
        live.clock.step_by(Duration::from_secs(6));
        let cause = stopped(checkpoint(&mut live.operation, true));
        assert_eq!(cause, fail_stop("admission-boundary"));
        assert_eq!(
            live.operation.guard().state(),
            AttemptState::LatchedBeforeAdmission
        );
    });
}

#[test]
fn a_boot_change_fail_stops_the_next_read() {
    churned(|| {
        let (_fixture, _project, _n, mut live) = eligible_live("x4a-boot");
        live.clock.reboot("00000000-0000-4000-8000-000000000002");
        let cause = stopped(checkpoint(&mut live.operation, false));
        assert_eq!(cause, fail_stop("clock"));
    });
}

/// A started operation on `fixture` whose scripted monitor clock reads its
/// wall clock `shift` seconds from `scripted::WALL`. Its monotonic readings
/// and boot are the script's own.
fn begin_live_shifted(fixture: &ReadFixture, project: &Path, tag: &str, shift: i64) -> Live {
    try_begin_shifted(fixture, project, tag, shift, |_| {}).unwrap()
}
/// The same handoff, which may refuse; `probe` sees each monitor clock
/// sample before it is returned.
fn try_begin_shifted(
    fixture: &ReadFixture,
    project: &Path,
    tag: &str,
    shift: i64,
    probe: impl Fn(&crate::revocation::Sample) + Send + 'static,
) -> Result<Live, OperationRefusal> {
    use super::super::super::operation_guard::{Cadence, GuardSeam};
    let (mut writer, trees) = new_writer(fixture, tag);
    let subject = admitted(&mut writer, project);
    let clock = scripted::Clock::new();
    let seam = {
        let clock = clock.clone();
        GuardSeam {
            clock: Box::new(move || {
                let mut sample = clock.sample()?;
                sample.wall_seconds += shift;
                probe(&sample);
                Ok(sample)
            }),
            cadence: Cadence::Manual,
            hook: ObservationHook::live(),
        }
    };
    let operation = writer.begin_operation_with(
        subject,
        WriterLease::AppendWrite,
        &inputs(),
        &scripted::invocation(),
        seam,
    )?;
    Ok(Live {
        operation,
        clock,
        _trees: trees,
    })
}

#[test]
fn a_list_going_stale_during_the_operation_fail_stops_before_any_further_effect() {
    // Law X4T r11 item 6 (unit X4-F1). The store's list was issued
    // 2026-10-01, so it is stale strictly after 2026-12-30T00:00:00Z; its L
    // is 2026-10-01 too, so a first read is plausible up to that instant. The
    // first read's wall clock is two seconds before it, and so is its tEval.
    churned(|| {
        let (fixture, project, n) = eligible("x4f1-stale");
        let first_wall = 1_798_588_798; // 2026-12-29T23:59:58Z
        let mut live = begin_live_shifted(
            &fixture,
            &project,
            "x4f1-stale",
            first_wall - scripted::WALL,
        );
        assert_eq!(
            live.operation
                .guard()
                .start_view()
                .time()
                .unwrap()
                .evaluation,
            Some(first_wall)
        );
        // One monotonic second later: tEval + 1 is before the boundary. A
        // tick continues and an effect is admitted.
        live.clock.advance(Duration::from_secs(1));
        assert!(live.operation.guard().tick());
        assert!(matches!(
            checkpoint(&mut live.operation, false),
            Ok(Checked::Effect)
        ));
        assert_eq!(witness_of(&fixture, &n), (1, 1, "COMMITTED".into()));
        // Two more: tEval + 3 is past it. The core role is stale at the
        // observation's instant, so the observer fail-stops on the standing.
        live.clock.advance(Duration::from_secs(2));
        assert!(!live.operation.guard().tick());
        assert_eq!(live.operation.guard().cause(), Some(fail_stop("standing")));
        assert_eq!(
            live.operation.guard().state(),
            AttemptState::LatchedBeforeAdmission
        );
        // No further effect or admission: the checkpoint names the first cause.
        assert_eq!(
            stopped(checkpoint(&mut live.operation, true)),
            fail_stop("standing")
        );
        assert_eq!(witness_of(&fixture, &n), (1, 1, "COMMITTED".into()));
    });
}

#[test]
fn a_list_already_stale_at_the_first_reads_t_eval_refuses_at_the_lease_free_point() {
    // Law X4T r12 items 6, 7, 9 and 10 (unit X4-F2). The store's bootstrap
    // manifest is issued 2026-10-03 (X4T-0's knob), so its L is too and S4's
    // plausibility bound reaches 2027-01-01T00:00:00Z. Its list, issued
    // 2026-10-01, is stale strictly after 2026-12-30T00:00:00Z. The first
    // read's wall clock, and so its tEval, is one second past that.
    churned(|| {
        let fixture = ReadFixture::new("x4f2-stale");
        fixture.accept_trust_issued("2026-10-03T00:00:00Z");
        let (fixture, project, n) = eligible_on(fixture, "x4f2-stale");
        let accepted = fs::read(current_path(&fixture)).unwrap();
        let first_wall = 1_798_588_801; // 2026-12-30T00:00:01Z
        // At each monitor clock sample: the fence held, and no lease taken.
        let probed = Arc::new(std::sync::Mutex::new(Vec::<(bool, bool)>::new()));
        let probe = {
            let probed = Arc::clone(&probed);
            let (fence, namespace) = (fence_path(&fixture), namespace_path(&fixture, &n));
            move |_: &crate::revocation::Sample| {
                let lock_free = |path: &Path, mode| {
                    FileLock::try_acquire(File::open(path).unwrap(), mode)
                        .unwrap()
                        .is_some()
                };
                probed.lock().unwrap().push((
                    !lock_free(&fence, LockMode::Exclusive),
                    lock_free(&namespace.join(WRITER_LEASE), LockMode::Exclusive)
                        && lock_free(&namespace.join(READERS_LEASE), LockMode::Exclusive),
                ));
            }
        };
        let refusal = match try_begin_shifted(
            &fixture,
            &project,
            "x4f2-stale",
            first_wall - scripted::WALL,
            probe,
        ) {
            Err(refusal) => refusal,
            Ok(_) => panic!("the first read admitted a stale store"),
        };
        // X4T's own continuation row at the lease-free point: never
        // `OBSERVER.FAIL_STOP`, never `required-files-changed`.
        let OperationRefusal::Trust(trust) = &refusal else {
            panic!("{refusal:?}")
        };
        assert_eq!(
            trust.row,
            crate::trust::TrustRow::Continuation("core:stale-revocation".into()),
            "{}",
            trust.cause
        );
        assert_eq!(
            refusal.row(),
            OperationRow::Installation(T::TrustContinuation {
                subject: "core:stale-revocation".into()
            })
        );
        // The monitor's first read ran under the fence before any lease.
        let probed = probed.lock().unwrap().clone();
        assert!(!probed.is_empty());
        assert!(
            probed.iter().all(|(fence, free)| *fence && *free),
            "{probed:?}"
        );
        // The floor publication was confirmed first: F = tEval, and every
        // stored role state is as accepted.
        let published = fs::read(current_path(&fixture)).unwrap();
        assert_ne!(published, accepted);
        let field = |v: &V, k: &str| match v {
            V::Object(o) => o[k].clone(),
            _ => panic!("{k}"),
        };
        let (new, old) = (
            opensip_identity::parse_json(&published).unwrap(),
            opensip_identity::parse_json(&accepted).unwrap(),
        );
        assert_eq!(
            field(&field(&field(&new, "clock"), "record"), "evalHighWater"),
            V::String(crate::trust_time::format_timestamp(first_wall).unwrap())
        );
        assert_eq!(field(&new, "roles"), field(&old, "roles"));
        // No X3b floor, carrier or journal record; the fence and N are free.
        assert!(!fixture.installation.join("trust/carrier-floors").exists());
        let namespace = namespace_path(&fixture, &n);
        assert!(!namespace.join("grant-journal.sqlite").exists());
        assert!(!namespace.join("grant-journal.witness.json").exists());
        assert!(fence_free(&fixture) && unlocked(&fixture, &n));
    });
}

#[test]
fn a_checkpoint_needs_this_operations_own_level_four() {
    churned(|| {
        let (_fixture, _project, _n, mut live) = eligible_live("x4a-foreign-a");
        let (other_fixture, other_project, _) = eligible("x4a-foreign-b");
        let mut other = begin_live(
            &other_fixture,
            &other_project,
            "x4a-foreign-b",
            false,
            ObservationHook::live(),
        )
        .unwrap();
        // Another operation's held level 4 lent to this checkpoint: refused as
        // a broken caller, and this gate latches.
        let mut refused = None;
        let _ = other
            .operation
            .journal::<(), ()>(|location, carrier, _, work| {
                let held = carrier
                    .lock()
                    .begin(location, work)
                    .and_then(|transaction| transaction.acquire())
                    .map_err(|_| WorkFailure::Operation(()))?;
                let _ = live.operation.journal::<(), ()>(|_, _, checkpoint, work| {
                    refused = checkpoint.effect(&held, work).err();
                    Ok(())
                });
                Ok(())
            });
        assert_eq!(refused, Some(GuardRefusal::Invariant));
        assert_eq!(
            live.operation.guard().state(),
            AttemptState::LatchedBeforeAdmission
        );
        assert_eq!(other.operation.guard().state(), AttemptState::Preparing);
        drop(other);
    });
}

// ----------------------------------------------- the observer and drift

#[test]
fn an_unrelated_revocation_update_continues_as_drift_without_the_fence() {
    churned(|| {
        let (fixture, _project, _n, mut live) = eligible_live("x4a-drift");
        // Another writer's publication: a newer, authenticated list naming no
        // closure component, by atomic replacement of `state.v1`.
        fixture.swap_trust(vec![("release", format!("closure2:{}", "0".repeat(64)))], 2);
        // The observer never takes the fence: another holder keeps it.
        let fence = hold(&fence_path(&fixture), LockMode::Exclusive);
        assert!(live.operation.guard().tick());
        drop(fence);
        assert_eq!(live.operation.guard().drift(), vec!["revocation-unrelated"]);
        assert_eq!(live.operation.guard().state(), AttemptState::Preparing);
        // The start epoch is not replaced; the operation goes on.
        assert_eq!(
            live.operation
                .guard()
                .start_view()
                .epoch()
                .revocation_version,
            1
        );
        assert!(matches!(
            checkpoint(&mut live.operation, true),
            Ok(Checked::Permit(_))
        ));
    });
}

#[test]
fn a_revoking_update_latches_through_the_observer_and_refuses_the_checkpoint() {
    churned(|| {
        let (fixture, _project, n, mut live) = eligible_live("x4a-revoke");
        let closure = live.operation.selected_core().0.to_owned();
        fixture.swap_trust(vec![("release", closure)], 2);
        // The observer's tick sees the revocation and stops (F18's gate half).
        assert!(!live.operation.guard().tick());
        let revoked = StopCause::Revoked {
            subject: "trust-revoked",
        };
        assert_eq!(live.operation.guard().cause(), Some(revoked.clone()));
        assert_eq!(
            live.operation.guard().state(),
            AttemptState::LatchedBeforeAdmission
        );
        assert_eq!(
            revoked.row(),
            OperationRow::Installation(T::RevokedDuringOperation {
                subject: "trust-revoked"
            })
        );
        // No effect is admitted after it: the checkpoint names the first cause.
        assert_eq!(stopped(checkpoint(&mut live.operation, false)), revoked);
        assert_eq!(witness_of(&fixture, &n), (1, 0, "COMMITTED".into()));
    });
}

#[test]
fn a_revoking_update_is_seen_by_the_checkpoints_own_final_observation() {
    // F5: a run refused only by shared-ancestor churn starts over (`churned`).
    churned(|| {
        let (fixture, _project, _n, mut live) = eligible_live("x4a-revoke-cp");
        let closure = live.operation.selected_core().0.to_owned();
        fixture.swap_trust(vec![("release", closure)], 2);
        let cause = stopped(checkpoint(&mut live.operation, true));
        assert_eq!(
            cause,
            StopCause::Revoked {
                subject: "trust-revoked"
            }
        );
    });
}

#[test]
fn an_unreadable_newer_view_fail_stops_and_a_lower_one_is_a_rollback() {
    churned(|| {
        // A newer pointer whose revocation list is missing: the newly named
        // record is actually opened, never assumed.
        let (fixture, _project, _n, live) = eligible_live("x4a-unreadable");
        fixture.swap_trust(vec![("release", format!("closure2:{}", "1".repeat(64)))], 2);
        let objects = fixture.installation.join("trust/objects");
        let revocation = fs::read_dir(&objects)
            .unwrap()
            .map(|e| e.unwrap().path())
            .find(|path| {
                let needle = b"\"revocationVersion\":2,";
                fs::read(path).is_ok_and(|raw| raw.windows(needle.len()).any(|w| w == needle))
            })
            .expect("the new revocation body");
        fs::remove_file(&revocation).unwrap();
        assert!(!live.operation.guard().tick());
        assert_eq!(
            live.operation.guard().cause(),
            Some(fail_stop("unreadable"))
        );

        // A pointer back below the start view's counters: never revocation, and
        // never admitted as the current view.
        let (fixture, project, _) = eligible("x4a-rollback");
        fixture.write_trust(Vec::new(), 2);
        let live = begin_live(
            &fixture,
            &project,
            "x4a-rollback",
            false,
            ObservationHook::live(),
        )
        .unwrap();
        assert_eq!(
            live.operation
                .guard()
                .start_view()
                .epoch()
                .revocation_version,
            2
        );
        fixture.swap_trust(Vec::new(), 1);
        assert!(!live.operation.guard().tick());
        assert_eq!(live.operation.guard().cause(), Some(fail_stop("rollback")));
    });
}

#[test]
fn a_replacement_during_the_first_attempt_is_absorbed_and_a_second_is_mixed() {
    churned(|| {
        for twice in [false, true] {
            let tag = if twice { "x4a-mixed" } else { "x4a-absorb" };
            let (fixture, project, _) = eligible(tag);
            let current = current_path(&fixture);
            let renames = Arc::new(std::sync::atomic::AtomicUsize::new(0));
            let hook = {
                let current = current.clone();
                let renames = Arc::clone(&renames);
                ObservationHook {
                    at: Some(Arc::new(move |point| {
                        let replace = match point {
                            ObservationPoint::Admitted(1) => true,
                            ObservationPoint::Admitted(2) => twice,
                            _ => false,
                        };
                        if replace {
                            // The same bytes under a new file: the identity changes.
                            let next = current.with_file_name("state.v1.x4a");
                            fs::copy(&current, &next).unwrap();
                            private(&next);
                            fs::rename(&next, &current).unwrap();
                            renames.fetch_add(1, std::sync::atomic::Ordering::SeqCst);
                        }
                    })),
                }
            };
            let live = begin_live(&fixture, &project, tag, false, hook).unwrap();
            let ticked = live.operation.guard().tick();
            if twice {
                assert!(!ticked);
                assert_eq!(live.operation.guard().cause(), Some(fail_stop("mixed")));
                assert_eq!(renames.load(std::sync::atomic::Ordering::SeqCst), 2);
            } else {
                // One monitor read covered both attempts; nothing latched.
                assert!(ticked, "{:?}", live.operation.guard().cause());
                assert_eq!(live.operation.guard().state(), AttemptState::Preparing);
                assert_eq!(renames.load(std::sync::atomic::Ordering::SeqCst), 1);
            }
        }
    });
}

// --------------------------------------------------------- stale guards

#[test]
fn each_stale_guard_refuses_on_its_own_row_before_any_effect() {
    churned(|| {
        let changed = OperationRow::Project(ProjectWriteRow::Project(RegistrationRow::Admission(
            ProjectAdmissionRow::RequiredFilesChanged,
        )));
        // A lease whose descriptor is unchanged but whose lock was lost: S7's
        // busy row, never `required-files-changed`.
        let (fixture, _project, n, mut live) = eligible_live("x4a-lost");
        live.operation.lease_mut().lose_locks();
        let cause = stopped(checkpoint(&mut live.operation, false));
        assert_eq!(
            cause.row(),
            OperationRow::Project(ProjectWriteRow::Project(RegistrationRow::Busy))
        );
        assert_eq!(witness_of(&fixture, &n), (1, 0, "COMMITTED".into()));

        // A replaced lease file: the same name, another file.
        let (fixture, _project, n, mut live) = eligible_live("x4a-lease-file");
        let lease = namespace_path(&fixture, &n).join(WRITER_LEASE);
        let next = lease.with_file_name("writer.lease.x4a");
        fs::copy(&lease, &next).unwrap();
        private(&next);
        fs::rename(&next, &lease).unwrap();
        let cause = stopped(checkpoint(&mut live.operation, false));
        assert_eq!(cause.row(), changed);

        // A substituted marker of a registered project.
        let fixture = trusted("x4a-marker");
        let project = fixture_project(&fixture);
        let mut live = begin_live(
            &fixture,
            &project,
            "x4a-marker",
            true,
            ObservationHook::live(),
        )
        .unwrap();
        let marker = project.join(".opensip").join("project-id.v1");
        let next = marker.with_file_name("project-id.x4a");
        fs::copy(&marker, &next).unwrap();
        private(&next);
        fs::rename(&next, &marker).unwrap();
        let cause = stopped(checkpoint(&mut live.operation, false));
        assert_eq!(
            cause.row(),
            OperationRow::Project(ProjectWriteRow::Project(RegistrationRow::Admission(
                ProjectAdmissionRow::RequiredFilesChanged
            )))
        );

        // A foreign store endpoint: the store marker replaced.
        let (fixture, _project, _n, mut live) = eligible_live("x4a-endpoint");
        let marker = fixture
            .installation
            .join(format!("stores/{}/store-instance.v1", fixture.store));
        let next = marker.with_file_name("store-instance.x4a");
        fs::copy(&marker, &next).unwrap();
        private(&next);
        fs::rename(&next, &marker).unwrap();
        let cause = stopped(checkpoint(&mut live.operation, false));
        assert_eq!(
            cause.row(),
            OperationRow::Installation(T::Custody {
                subject: "required-files-changed"
            })
        );

        // The namespace no longer private (group-writable). (A namespace moved
        // away is refused earlier, by the journal's own level-3 open by path.)
        let (fixture, _project, n, mut live) = eligible_live("x4a-namespace");
        let namespace = namespace_path(&fixture, &n);
        fs::set_permissions(&namespace, fs::Permissions::from_mode(0o770)).unwrap();
        let cause = stopped(checkpoint(&mut live.operation, false));
        fs::set_permissions(&namespace, fs::Permissions::from_mode(0o700)).unwrap();
        assert!(matches!(cause, StopCause::Stale(_)), "{cause:?}");
        assert_eq!(
            live.operation.guard().state(),
            AttemptState::LatchedBeforeAdmission
        );
    });
}

#[test]
fn an_unrelated_registration_does_not_invalidate_the_operation() {
    churned(|| {
        let (fixture, _project, _n, mut live) = eligible_live("x4a-unrelated");
        // Another writer registers another project: R and the pair's capture
        // are provenance, never live obligations.
        let other = fixture.home.join("code").join("other");
        fs::create_dir(&other).unwrap();
        fs::set_permissions(&other, fs::Permissions::from_mode(0o755)).unwrap();
        let (mut writer, _trees) = new_writer(&fixture, "x4a-unrelates");
        let registered = register(&mut writer, &other);
        drop(registered);
        writer.release().unwrap();
        assert!(matches!(
            checkpoint(&mut live.operation, false),
            Ok(Checked::Effect)
        ));
        assert!(matches!(
            checkpoint(&mut live.operation, true),
            Ok(Checked::Permit(_))
        ));
    });
}

#[test]
fn a_repeated_checkpoint_after_journal_work_rechecks_everything_again() {
    churned(|| {
        // F19's shape: blocking journal work, then the repeated checkpoint. A
        // guard that went stale meanwhile latches; the RA already appended stays.
        let (fixture, _project, n, mut live) = eligible_live("x4a-repeat");
        assert!(matches!(
            checkpoint(&mut live.operation, false),
            Ok(Checked::Effect)
        ));
        assert_eq!(witness_of(&fixture, &n), (1, 1, "COMMITTED".into()));
        live.operation.lease_mut().lose_locks();
        let cause = stopped(checkpoint(&mut live.operation, true));
        assert_eq!(
            cause.row(),
            OperationRow::Project(ProjectWriteRow::Project(RegistrationRow::Busy))
        );
        assert_eq!(witness_of(&fixture, &n), (1, 1, "COMMITTED".into()));
    });
}

#[test]
fn the_end_path_stops_the_observer_and_releases_everything() {
    churned(|| {
        let (fixture, _project, n, live) = eligible_live("x4a-end");
        assert!(live.operation.guard().tick());
        match live.operation.end(JournalOutcome::Certain) {
            OperationEnd::Ended(_) => {}
            other => panic!("{other:?}"),
        }
        assert!(fence_free(&fixture) && unlocked(&fixture, &n));
    });
}

#[test]
fn a_substituted_root_or_a_missing_endpoint_file_is_stale_before_any_effect() {
    churned(|| {
        // The project root replaced by another directory at the same path.
        let (fixture, project, n, mut live) = eligible_live("x4a-root");
        fs::rename(&project, project.with_file_name("project-moved")).unwrap();
        fs::create_dir(&project).unwrap();
        fs::set_permissions(&project, fs::Permissions::from_mode(0o755)).unwrap();
        let cause = stopped(checkpoint(&mut live.operation, false));
        assert!(
            matches!(cause, StopCause::Stale(OperationRow::Project(_))),
            "{cause:?}"
        );
        assert_eq!(witness_of(&fixture, &n), (1, 0, "COMMITTED".into()));

        // The store endpoint's marker gone.
        let (fixture, _project, _n, mut live) = eligible_live("x4a-endpoint-gone");
        fs::remove_file(
            fixture
                .installation
                .join(format!("stores/{}/store-instance.v1", fixture.store)),
        )
        .unwrap();
        let cause = stopped(checkpoint(&mut live.operation, false));
        assert_eq!(cause.row(), OperationRow::Installation(T::Incomplete));
    });
}

#[test]
fn a_read_waiting_on_the_shared_monitor_counts_its_wait() {
    churned(|| {
        let (_fixture, _project, _n, live) = eligible_live("x4a-wait");
        let guard = live.operation.guard();
        std::thread::scope(|scope| {
            // A checkpoint holds the monitor (steps 2 to 4) while a tick waits.
            let held = guard.hold_monitor();
            let tick = scope.spawn(|| guard.tick());
            // The time spent waiting is inside the waiting read's bound: it is
            // measured from the earliest instant of the read before it.
            live.clock.advance(Duration::from_secs(11));
            drop(held);
            assert!(!tick.join().unwrap());
        });
        assert_eq!(live.operation.guard().cause(), Some(fail_stop("stalled")));
    });
}

// ------------------------------------- law X4 r8 S11.6 (unit X4-F3)

#[test]
fn a_first_read_succeeding_during_unrelated_unwinding_is_refused_at_the_guards_entry() {
    // W-11 (RF-X4R8-R2-1) through the real handoff: inside a destructor
    // during an unrelated unwind, the lease-free first read succeeds, with a
    // scripted clock, and `StopOnUnwind` latches the gate bare. The guard's
    // entry refuses it on the existing fail-stop row, subject `latched`, as
    // a first read returning `AlreadyStopped` is refused; no guard exists,
    // so no observer runs, and the handoff releases what it held.
    churned(|| {
        let (fixture, project, n) = eligible("x4f3-unwind");
        let (mut writer, _trees) = new_writer(&fixture, "x4f3-unwind");
        let subject = admitted(&mut writer, &project);
        let clock = scripted::Clock::new();
        let seam = scripted::seam(&clock, ObservationHook::live());
        // Only the handoff runs in the destructor; nothing there can panic.
        let mut parts = Some((writer, subject, seam));
        let (panicking, begun) = scripted::unwinding(|| {
            parts.take().map(|(writer, subject, seam)| {
                writer.begin_operation_with(
                    subject,
                    WriterLease::AppendWrite,
                    &inputs(),
                    &scripted::invocation(),
                    seam,
                )
            })
        });
        assert!(panicking);
        let refusal = match begun.expect("the handoff ran") {
            Err(refusal) => refusal,
            Ok(operation) => panic!("a guard on a latched gate: {:?}", operation.guard()),
        };
        assert!(
            matches!(
                refusal,
                OperationRefusal::Live(StopCause::FailStop { subject: "latched" })
            ),
            "{refusal:?}"
        );
        assert_eq!(
            refusal.row(),
            OperationRow::Installation(T::ObserverFailStop { subject: "latched" })
        );
        assert!(fence_free(&fixture) && unlocked(&fixture, &n));
    });
}

#[test]
fn a_certain_refusal_completes_while_an_observation_holds_the_monitor() {
    // W-10 (a), the certain refusal's half: its stop transition never takes
    // the monitor's mutex. (No timing bound is asserted.)
    churned(|| {
        let (_fixture, _project, _n, live) = eligible_live("x4f3-no-wait");
        let guard = live.operation.guard();
        std::thread::scope(|scope| {
            let held = guard.hold_monitor();
            let stopped = scope
                .spawn(|| guard.stop(StopCause::CertainRefusal))
                .join()
                .unwrap();
            assert_eq!(stopped, AttemptState::LatchedBeforeAdmission);
            assert_eq!(guard.cause(), Some(StopCause::CertainRefusal));
            drop(held);
        });
    });
}

#[test]
fn a_successful_admission_takes_no_stop_cause_lock() {
    // W-10 (c): a test thread holds the stop-cause lock, outside any stop
    // transition, while the final admission succeeds.
    churned(|| {
        let (_fixture, _project, _n, mut live) = eligible_live("x4f3-admit-free");
        let held = live.operation.guard().hold_cause();
        assert!(matches!(
            checkpoint(&mut live.operation, true),
            Ok(Checked::Permit("prepared-commit"))
        ));
        drop(held);
        assert_eq!(live.operation.guard().state(), AttemptState::Admitted);
        assert_eq!(live.operation.guard().cause(), None);
    });
}

#[test]
fn cancellation_completes_while_an_observation_holds_the_monitor() {
    // W-10(a): the cancellation half, with no native timing assertion.
    churned(|| {
        let (_fixture, _project, _n, live) = eligible_live("j3b-cancel-no-wait");
        let guard = live.operation.guard();
        let cancellation = guard.cancellation_handle();
        cancellation.open_window();
        std::thread::scope(|scope| {
            let held = guard.hold_monitor();
            let result = scope
                .spawn(|| cancellation.cancel(crate::D9Signal::Sighup))
                .join()
                .unwrap();
            assert_eq!(result, crate::LatchOutcome::BeforeAdmission);
            assert_eq!(
                guard.cause(),
                Some(StopCause::Operator {
                    signal: crate::D9Signal::Sighup
                })
            );
            drop(held);
        });
        assert_eq!(
            cancellation.close_window(),
            AttemptState::LatchedBeforeAdmission
        );
    });
}
