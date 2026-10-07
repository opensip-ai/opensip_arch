// Law X4 r7 (unit X4a): the guard's own pieces, with scripted clocks only.
// The end-to-end cases run through the handoff (`operation_live_tests.rs`).
use super::scripted::{Clock, unwinding};
use super::*;
use crate::trust::TrustRow;

fn sample(at: Duration, boot: &str) -> Sample {
    Sample {
        before: at,
        after: at,
        boot: boot.into(),
        wall_seconds: scripted::WALL,
        wall_nanos: 0,
    }
}

#[test]
fn every_fenced_admission_row_takes_its_x4t_item_10_termination() {
    let cases = [
        (TrustRow::Incomplete, T::Incomplete),
        (
            TrustRow::NoAdmittedTimeContext,
            T::TrustNoAdmittedTimeContext,
        ),
        (
            TrustRow::Continuation("index:expired".into()),
            T::TrustContinuation {
                subject: "index:expired".into(),
            },
        ),
        (
            TrustRow::Root("ROOT.CHAIN_GAP", "link:2".into()),
            T::TrustRoot {
                detail: RootDetail::ChainGap,
                subject: "link:2".into(),
            },
        ),
        (
            TrustRow::Root("ROOT.SCHEMA_UNSUPPORTED", "anchor".into()),
            T::TrustRoot {
                detail: RootDetail::SchemaUnsupported,
                subject: "anchor".into(),
            },
        ),
        (
            TrustRow::PayloadNotAdmissible("revocation"),
            T::TrustPayloadNotAdmissible {
                subject: "revocation",
            },
        ),
        (
            TrustRow::ClockExcursion("in-session"),
            T::ClockExcursionForward {
                subject: "in-session",
            },
        ),
        (TrustRow::StateSchemaUnsupported, T::StateSchemaUnsupported),
        (TrustRow::HostIo, T::HostIo),
        (TrustRow::Budget, T::BudgetExhausted),
        (
            TrustRow::Rollback,
            T::Custody {
                subject: "trust-rollback",
            },
        ),
        (
            TrustRow::RequiredFilesChanged,
            T::Custody {
                subject: "required-files-changed",
            },
        ),
        // X4B r5 item 1 step 2.3 (unit X4B-b): a second F absent.
        (TrustRow::Invariant, T::Invariant),
    ];
    for (row, termination) in cases {
        assert_eq!(trust_termination(&row), termination, "{row:?}");
    }
    // Every chain detail the chain evaluation names is a registered one.
    for code in [
        "ROOT.CHAIN_GAP",
        "ROOT.CHAIN_BACKDATED",
        "ROOT.CHAIN_OLD_THRESHOLD",
        "ROOT.CHAIN_NEW_THRESHOLD",
        "ROOT.FINAL_EXPIRED",
        "ROOT.FINAL_FUTURE",
        "ROOT.EXPIRED_NO_CHAIN",
        "ROOT.STATE_INCONSISTENT",
        "ROOT.SCHEMA_UNSUPPORTED",
    ] {
        assert_ne!(
            trust_termination(&TrustRow::Root(code, String::new())),
            T::Invariant,
            "{code}"
        );
    }
}

#[test]
fn each_stop_names_x4_item_8s_row() {
    assert_eq!(
        StopCause::Revoked { subject: "policy" }.row(),
        OperationRow::Installation(T::RevokedDuringOperation { subject: "policy" })
    );
    assert_eq!(
        StopCause::FailStop { subject: "mixed" }.row(),
        OperationRow::Installation(T::ObserverFailStop { subject: "mixed" })
    );
    let stale = OperationRow::Installation(T::Custody {
        subject: "required-files-changed",
    });
    assert_eq!(StopCause::Stale(stale.clone()).row(), stale);
    assert_eq!(
        GuardRefusal::Invariant.row(),
        OperationRow::Installation(T::Invariant)
    );
}

#[test]
fn the_gate_and_monitor_come_first_and_the_first_read_is_bracketed() {
    // A read: its opening sample reaches the counter; the gate is open.
    let clock = Clock::new();
    let mut lease_free = LeaseFree::create(clock.monitor());
    assert_eq!(lease_free.state(), AttemptState::Preparing);
    let opening = lease_free
        .first_read(|sample| Ok::<_, ()>(sample.clone()))
        .unwrap();
    assert_eq!(opening.boot, scripted::BOOT);
    assert_eq!(opening.wall_seconds, scripted::WALL);
    assert_eq!(lease_free.state(), AttemptState::Preparing);

    // The counter's own refusal is returned as such, and latches.
    let mut lease_free = LeaseFree::create(Clock::new().monitor());
    assert!(matches!(
        lease_free.first_read(|_| Err::<(), _>("refused")),
        Err(FirstRead::Counter("refused"))
    ));
    assert_eq!(lease_free.state(), AttemptState::LatchedBeforeAdmission);

    // A long first read (an acceptance, a slow store) is inside the bracket:
    // over the bound it stalls and latches.
    let clock = Clock::new();
    let mut lease_free = LeaseFree::create(clock.monitor());
    let read = lease_free.first_read(|_| {
        clock.advance(Duration::from_secs(11));
        Ok::<_, ()>(())
    });
    assert!(matches!(
        read,
        Err(FirstRead::Monitor(StopReason::Stalled(_)))
    ));
    assert_eq!(lease_free.state(), AttemptState::LatchedBeforeAdmission);
}

#[test]
fn the_admission_boundary_admits_exactly_ten_seconds_and_refuses_one_nanosecond_more() {
    for (extra, admitted) in [(Duration::ZERO, true), (Duration::from_nanos(1), false)] {
        let (_gate, stop) = OperationGate::new();
        let mut monitor = FreshnessMonitor::new(stop.clone());
        let base = Duration::from_secs(100);
        let mut samples = vec![sample(base, "b"), sample(base, "b")].into_iter();
        monitor
            .read_sampled_with(
                || Ok(samples.next().unwrap()),
                |_| Ok::<_, ()>(()),
                StopReason::subject,
            )
            .unwrap();
        let now = base + Duration::from_secs(10) + extra;
        let result = monitor.boundary_with(|| Ok(sample(now, "b")), "admission-boundary");
        assert_eq!(result.is_ok(), admitted);
        assert_eq!(
            stop.observe(),
            if admitted {
                AttemptState::Preparing
            } else {
                AttemptState::LatchedBeforeAdmission
            }
        );
    }
    // A boot change, a sample before the read's end, or no read at all.
    for (now, boot, read) in [
        (Duration::from_secs(101), "c", true),
        (Duration::from_secs(99), "b", true),
        (Duration::from_secs(101), "b", false),
    ] {
        let (_gate, stop) = OperationGate::new();
        let mut monitor = FreshnessMonitor::new(stop.clone());
        if read {
            let mut samples = vec![
                sample(Duration::from_secs(100), "b"),
                sample(Duration::from_secs(100), "b"),
            ]
            .into_iter();
            monitor
                .read_sampled_with(
                    || Ok(samples.next().unwrap()),
                    |_| Ok::<_, ()>(()),
                    StopReason::subject,
                )
                .unwrap();
        }
        assert_eq!(
            monitor.boundary_with(|| Ok(sample(now, boot)), "admission-boundary"),
            Err(StopReason::MalformedClock)
        );
        assert_eq!(stop.observe(), AttemptState::LatchedBeforeAdmission);
    }
}

#[test]
fn one_gate_mints_one_permit_and_a_late_latch_keeps_its_result() {
    let (gate, stop) = OperationGate::new();
    let permit = gate.admit("prepared").unwrap();
    // No second permit; the prepared value comes back with the state.
    match gate.admit("again") {
        Err((prepared, state)) => {
            assert_eq!(prepared, "again");
            assert_eq!(state, AttemptState::Admitted);
        }
        Ok(_) => panic!("a second permit"),
    }
    assert_eq!(stop.latch(), AttemptState::AdmittedThenLatched);
    assert_eq!(permit.consume(|prepared| prepared), "prepared");
    assert_eq!(gate.observe(), AttemptState::AdmittedThenLatched);
    // Latched first: no permit at all.
    let (gate, stop) = OperationGate::new();
    stop.latch();
    assert!(matches!(
        gate.admit(()),
        Err(((), AttemptState::LatchedBeforeAdmission))
    ));
}

#[test]
fn the_observer_period_ticks_on_its_timeout_and_stops_on_its_signal() {
    // The production cadence's wait, with no sleep: a zero period times out
    // at once (a tick); a pending stop ends it whatever the period.
    let (signals, receiver) = mpsc::channel();
    assert!(matches!(
        wait(&receiver, &Cadence::Period(Duration::ZERO)),
        Wake::Tick
    ));
    signals.send(Signal::Stop).unwrap();
    assert!(matches!(
        wait(&receiver, &Cadence::Period(OBSERVER_PERIOD)),
        Wake::Stop
    ));
    drop(signals);
    assert!(matches!(
        wait(&receiver, &Cadence::Period(OBSERVER_PERIOD)),
        Wake::Stop
    ));
    assert_eq!(OBSERVER_PERIOD, Duration::from_secs(5));
    assert!(matches!(GuardSeam::live().cadence, Cadence::Period(p) if p == OBSERVER_PERIOD));
}

#[test]
fn the_crash_points_are_the_laws_names_in_registered_scopes() {
    // Law X9 r1 item 5's `x4.*` scopes and G4's points, placed by this unit.
    let guard = include_str!("operation_guard.rs");
    let gate = include_str!("../commit_authority.rs");
    for (source, point) in [
        (
            guard,
            r#"crash_barrier!(
            "x4.observer",
            "tick",
            gate,"#,
        ),
        (
            guard,
            r#"crash_barrier!("x4.observer", "after-observation", step)"#,
        ),
        (guard, r#"crash_scope!("x4.checkpoint""#),
        (
            guard,
            r#"crash_barrier!("x4.checkpoint", "before-observation", step)"#,
        ),
        (
            guard,
            r#"crash_barrier!("x4.checkpoint", "after-observation", step)"#,
        ),
        (
            guard,
            r#"crash_barrier!("x4.checkpoint", "before-admit", step)"#,
        ),
        (gate, r#"crash_barrier!("x4.gate", "admit.after", step)"#),
        (gate, r#"crash_barrier!("x4.gate", "latch.after", step)"#),
    ] {
        assert!(source.contains(point), "{point}");
    }
}

// ------------------------------------- law X4 r8 S11.6 (unit X4-F3)

#[test]
fn a_certain_refusal_is_the_invariant_row() {
    // LD8-7: `CertainRefusal`'s row is the invariant row; X3d's `REV` reason
    // for it stays `operation-stopped`, the reason it had with no cause.
    assert_eq!(
        StopCause::CertainRefusal.row(),
        OperationRow::Installation(T::Invariant)
    );
    use super::super::commit_session::end_path_for_tests::reason;
    assert_eq!(
        reason(Some(&StopCause::CertainRefusal)),
        "operation-stopped"
    );
    assert_eq!(reason(None), "operation-stopped");
}

/// W-11 and W-12: a first read that succeeded, and its start sample.
fn read_lease_free(clock: &Clock) -> (LeaseFree, Duration) {
    let mut lease_free = LeaseFree::create(clock.monitor());
    let before = lease_free
        .first_read(|sample| Ok::<_, ()>(sample.before))
        .unwrap();
    (lease_free, before)
}
/// The entry rule's refusal: no guard, the gate still latched, nothing
/// recorded, and the monitor's history the successful read's.
fn assert_refused_at_entry(lease_free: LeaseFree, before: Duration) {
    let refused = match enter(lease_free) {
        Err(refused) => refused,
        Ok(_) => panic!("a guard on a latched gate with no cause"),
    };
    assert_eq!(refused.stop.observe(), AttemptState::LatchedBeforeAdmission);
    assert_eq!(refused.gate.observe(), AttemptState::LatchedBeforeAdmission);
    assert_eq!(refused.stop.cause(), None);
    assert_eq!(refused.cell.monitor.last_before(), Some(before));
}

#[test]
fn a_successful_lease_free_read_during_unrelated_unwinding_gets_no_guard() {
    // W-11 (RF-X4R8-R2-1): inside a destructor during an unrelated unwind,
    // the first read succeeds, and `StopOnUnwind` latches the gate bare.
    let clock = Clock::new();
    let mut lease_free = LeaseFree::create(clock.monitor());
    let (panicking, read) =
        unwinding(|| lease_free.first_read(|sample| Ok::<_, ()>(sample.before)));
    assert!(panicking);
    let before = read.unwrap();
    assert_eq!(lease_free.state(), AttemptState::LatchedBeforeAdmission);
    // The entry rule refuses it: no guard, so no observer; the latch and the
    // history are kept; nothing is recorded (no `CertainRefusal`, no
    // invariant row). The handoff maps the refusal to `Live(FailStop
    // { latched })` (`operation_live_tests.rs`).
    assert_refused_at_entry(lease_free, before);
}

#[test]
fn the_same_read_after_the_guards_entry_records_its_fail_stop() {
    // W-11's second half, source 4: after the entry, the same read through
    // the rebound monitor latches through the stop handle and records
    // `FailStop { latched }`; a later reader gets it.
    let clock = Clock::new();
    let (lease_free, _) = read_lease_free(&clock);
    let Ok(mut entered) = enter(lease_free) else {
        panic!("a clear gate is refused")
    };
    assert_eq!(entered.stop.cause(), None);
    let MonitorCell { monitor, clock } = &mut entered.cell;
    let (panicking, read) = unwinding(|| {
        monitor.read_sampled_with(&mut *clock, |_| Ok::<_, ()>(()), StopReason::subject)
    });
    assert!(panicking);
    assert_eq!(read, Ok(()));
    let latched = StopCause::FailStop { subject: "latched" };
    assert_eq!(entered.stop.cause(), Some(latched.clone()));
    assert_eq!(entered.stop.observe(), AttemptState::LatchedBeforeAdmission);
    // The next read, an observer tick's or checkpoint step 2's, finds the
    // latch and reads that cause; it records nothing.
    let read = monitor.read_sampled_with(&mut *clock, |_| Ok::<_, ()>(()), StopReason::subject);
    assert_eq!(read, Err(StopReason::AlreadyStopped));
    assert_eq!(
        observed(
            &entered.stop,
            read.map(|()| Observed::Continue { drift: None })
        ),
        Err(GuardRefusal::Stopped(latched.clone()))
    );
    assert_eq!(entered.stop.cause(), Some(latched));
}

#[test]
fn a_bare_latch_on_any_lease_free_handle_before_the_entry_gets_no_guard() {
    // W-12: after a successful first read and just before `start`, a bare
    // latch on each lease-free handle in turn, through a test seam outside
    // any critical section. Each is W-11's refusal.
    for handle in [BareHandle::Gate, BareHandle::Stop, BareHandle::Monitor] {
        let clock = Clock::new();
        let (lease_free, before) = read_lease_free(&clock);
        assert_eq!(
            lease_free.latch_bare(handle),
            AttemptState::LatchedBeforeAdmission,
            "{handle:?}"
        );
        assert_refused_at_entry(lease_free, before);
    }
    // The control: with no latch, the entry installs the guard's parts in
    // state 0 with no cause recorded, and its first stop transition records
    // its cause.
    let clock = Clock::new();
    let (lease_free, before) = read_lease_free(&clock);
    let Ok(entered) = enter(lease_free) else {
        panic!("a clear gate is refused")
    };
    assert_eq!(entered.stop.observe(), AttemptState::Preparing);
    assert_eq!(entered.stop.cause(), None);
    assert_eq!(entered.cell.monitor.last_before(), Some(before));
    let stopped = entered.stop.stop(StopCause::CertainRefusal);
    assert_eq!(
        stopped,
        Transition {
            state: AttemptState::LatchedBeforeAdmission,
            first: true,
            cause: Some(StopCause::CertainRefusal),
        }
    );
}

/// The eight sources of law X4 r8 S11.6's table that unit X4-F3 carries.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum Source {
    /// 1: the observer's revoking observation.
    Revoked,
    /// 2: a monitor read's failure (here a stall).
    Read,
    /// 3: the admission-boundary check's own failure.
    Boundary,
    /// 4: `StopOnUnwind`: a read that ends while its thread unwinds.
    Unwind,
    /// 5: the shared monitor's mutex poisoned.
    Poisoned,
    /// 6: a stale guard at checkpoint step 1.
    Stale,
    /// 7: a level-4 borrow that is not this operation's lock.
    LockMismatch,
    /// 8: X3d's certain refusal (`OperationGuard::stop`).
    CertainRefusal,
}
const SOURCES: [Source; 8] = [
    Source::Revoked,
    Source::Read,
    Source::Boundary,
    Source::Unwind,
    Source::Poisoned,
    Source::Stale,
    Source::LockMismatch,
    Source::CertainRefusal,
];
#[test]
fn operator_stop_pairs_preserve_every_existing_sources_first_cause() {
    use super::super::commit_session::end_path_for_tests::reason;
    for source in SOURCES {
        for window in 0..3 {
            let rig = Rig::new();
            if window != 0 {
                rig.stop.open_window();
            }
            rig.drive(source, &mut || {});
            if window == 2 {
                rig.stop.close_window();
            }
            let expected = if window == 1 {
                LatchOutcome::AlreadyStopped
            } else {
                LatchOutcome::OutsideWindow
            };
            assert_eq!(rig.stop.cancel(D9Signal::Sigint), expected);
            assert_eq!(rig.stop.cause(), Some(source.cause()));
            assert_eq!(reason(rig.stop.cause().as_ref()), source.reason());
        }
        let rig = Rig::new();
        rig.stop.open_window();
        assert_eq!(
            rig.stop.cancel(D9Signal::Sigterm),
            LatchOutcome::BeforeAdmission
        );
        let operator = StopCause::Operator {
            signal: D9Signal::Sigterm,
        };
        assert_eq!(
            rig.drive(source, &mut || {}),
            reported(source, &operator, false)
        );
        assert_eq!(rig.stop.cause(), Some(operator.clone()));
        assert_eq!(reason(rig.stop.cause().as_ref()), "operator");
        assert_eq!(rig.stop.latched().row(), operator.row());
    }
}
fn stale_row() -> OperationRow {
    OperationRow::Installation(T::Custody {
        subject: "required-files-changed",
    })
}
impl Source {
    /// The cause the source records in its own stop transition.
    fn cause(self) -> StopCause {
        match self {
            Self::Revoked => StopCause::Revoked {
                subject: "trust-revoked",
            },
            Self::Read => StopCause::FailStop { subject: "stalled" },
            Self::Boundary => StopCause::FailStop {
                subject: "admission-boundary",
            },
            Self::Unwind | Self::Poisoned => StopCause::FailStop { subject: "latched" },
            Self::Stale => StopCause::Stale(stale_row()),
            Self::LockMismatch | Self::CertainRefusal => StopCause::CertainRefusal,
        }
    }
    /// `finish`'s `REV` reason when the source is the first stop.
    fn reason(self) -> &'static str {
        match self {
            Self::Revoked => "trust-revoked",
            Self::Read | Self::Boundary | Self::Unwind | Self::Poisoned => "observer-fail-stop",
            Self::Stale => "stale-guard",
            Self::LockMismatch | Self::CertainRefusal => "operation-stopped",
        }
    }
}
/// What a source's path reports: a checkpoint's refusal after its trailing
/// latch (sources 1 to 7; none if the path did not refuse), or the stop
/// transition `OperationGuard::stop` makes (8).
#[derive(Debug, PartialEq, Eq)]
enum Report {
    Refusal(Option<GuardRefusal>),
    Stop(Transition),
}
/// One operation at its guard's entry: its stop handle, the scripted clock,
/// a monitor on the stop handle for each of sources 2 to 4 (as the entry
/// rebinds it, each after one successful read, made here, so that no source
/// reads while another's destructor unwinds), and a poisoned mutex standing
/// for the shared monitor's.
struct Rig {
    stop: StopHandle,
    clock: Clock,
    monitors: [std::cell::RefCell<FreshnessMonitor<StopHandle>>; 3],
    poisoned: Mutex<()>,
}
impl Rig {
    fn new() -> Self {
        let clock = Clock::new();
        let (lease_free, _) = read_lease_free(&clock);
        let Ok(Entered { stop, .. }) = enter(lease_free) else {
            panic!("a clear gate is refused")
        };
        let monitors = [(); 3].map(|()| {
            let mut monitor = FreshnessMonitor::new(stop.clone());
            monitor
                .read_sampled_with(clock.monitor(), |_| Ok::<_, ()>(()), StopReason::subject)
                .unwrap();
            std::cell::RefCell::new(monitor)
        });
        let poisoned = Mutex::new(());
        let _ = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| {
            let _held = poisoned.lock();
            std::panic::resume_unwind(Box::new("poison"))
        }));
        assert!(poisoned.is_poisoned());
        assert_eq!(stop.observe(), AttemptState::Preparing);
        Self {
            stop,
            clock,
            monitors,
            poisoned,
        }
    }
    /// Drive `source` through the production path that makes its stop
    /// transition, with the scripted clock and counter seams. `first` runs at
    /// the path's last point before that transition: inside the read's
    /// counter (sources 2 and 4) or the boundary's clock (3), else just
    /// before the path. Never panics, since `first` may run in a destructor
    /// during unwinding.
    fn drive(&self, source: Source, first: &mut dyn FnMut()) -> Report {
        let stop = &self.stop;
        let continued = || Observed::Continue { drift: None };
        let refused = match source {
            Source::Revoked => {
                first();
                // The observer's tick and checkpoint step 2 alike.
                observed(
                    stop,
                    Ok(Observed::Revoke {
                        subject: "trust-revoked",
                    }),
                )
                .err()
            }
            Source::Read => {
                let mut monitor = self.monitors[0].borrow_mut();
                let read = monitor.read_sampled_with(
                    self.clock.monitor(),
                    |_| {
                        first();
                        self.clock.advance(Duration::from_secs(11));
                        Ok::<_, ()>(continued())
                    },
                    StopReason::subject,
                );
                observed(stop, read).err()
            }
            Source::Boundary => {
                let mut monitor = self.monitors[1].borrow_mut();
                let mut sampled = self.clock.monitor();
                let _ = monitor.boundary_with(
                    || {
                        first();
                        self.clock.advance(Duration::from_secs(11));
                        sampled()
                    },
                    "admission-boundary",
                );
                // Checkpoint step 4's refusal.
                Some(GuardRefusal::Stopped(StopCause::FailStop {
                    subject: "admission-boundary",
                }))
            }
            Source::Unwind => {
                let mut monitor = self.monitors[2].borrow_mut();
                let (_, read) = unwinding(|| {
                    monitor.read_sampled_with(
                        self.clock.monitor(),
                        |_| {
                            first();
                            Ok::<_, ()>(continued())
                        },
                        StopReason::subject,
                    )
                });
                // A successful read on a latched gate: step 3 reads the latch.
                match observed(stop, read) {
                    Ok(_) => Some(stop.latched()),
                    Err(refusal) => Some(refusal),
                }
            }
            Source::Poisoned => {
                first();
                lock_monitor(&self.poisoned, stop).err()
            }
            Source::Stale => {
                first();
                Some(stale(stop, stale_row()))
            }
            Source::LockMismatch => {
                first();
                Some(GuardRefusal::Invariant)
            }
            Source::CertainRefusal => {
                first();
                return Report::Stop(stop.stop(StopCause::CertainRefusal));
            }
        };
        // The checkpoint's trailing latch.
        Report::Refusal(refused.map(|refusal| refuse(stop, refusal)))
    }
}
/// What a source's own path reports when the cause `first` is recorded.
fn reported(source: Source, first: &StopCause, set: bool) -> Report {
    match source {
        Source::LockMismatch => Report::Refusal(Some(GuardRefusal::Invariant)),
        Source::CertainRefusal => Report::Stop(Transition {
            state: AttemptState::LatchedBeforeAdmission,
            first: set,
            cause: Some(first.clone()),
        }),
        _ => Report::Refusal(Some(GuardRefusal::Stopped(first.clone()))),
    }
}

#[test]
fn every_ordered_pair_of_sources_keeps_the_first_stops_cause() {
    // W-6 (RF-X4R8-1) over sources 1 to 8, at the guard level: A's stop
    // transition completes, then B's runs. B's pairs with source 9 are J3b's.
    for a in SOURCES {
        for b in SOURCES.into_iter().filter(|b| *b != a) {
            let rig = Rig::new();
            let mut first = None;
            let second = rig.drive(b, &mut || {
                let report = rig.drive(a, &mut || {});
                first = Some((report, rig.stop.cause(), rig.stop.observe()));
            });
            let (first, recorded, state) = first.expect("A ran");
            let cause = a.cause();
            // A was the first stop: its transition set `LATCHED` and recorded
            // its cause in the same critical section (I1).
            assert_eq!(recorded.as_ref(), Some(&cause), "{a:?} then {b:?}");
            assert_eq!(state, AttemptState::LatchedBeforeAdmission);
            assert_eq!(first, reported(a, &cause, true), "{a:?} then {b:?}");
            // B recorded nothing, and its call returned A's cause; a
            // checkpoint path reports A's cause's row, except the lock
            // mismatch, which reports `GuardRefusal::Invariant`.
            assert_eq!(rig.stop.cause(), Some(cause.clone()), "{a:?} then {b:?}");
            assert_eq!(second, reported(b, &cause, false), "{a:?} then {b:?}");
            if let Report::Refusal(Some(refusal)) = &second {
                let row = match b {
                    Source::LockMismatch => OperationRow::Installation(T::Invariant),
                    _ => cause.row(),
                };
                assert_eq!(refusal.row(), row, "{a:?} then {b:?}");
            }
            // `finish`'s `REV` reason is A's.
            use super::super::commit_session::end_path_for_tests::reason;
            assert_eq!(
                reason(rig.stop.cause().as_ref()),
                a.reason(),
                "{a:?} then {b:?}"
            );
            assert_eq!(rig.stop.observe(), AttemptState::LatchedBeforeAdmission);
        }
    }
}

/// Production text: everything before `end`, with comment lines dropped
/// (the X8 r3 source-pin convention).
fn production(source: &str, end: &str) -> String {
    source[..source.find(end).expect("the test boundary")]
        .lines()
        .filter(|line| !line.trim_start().starts_with("//"))
        .collect::<Vec<_>>()
        .join("\n")
}
/// The body of the first `fn` whose signature starts with `signature`, to its
/// closing brace at the same indentation.
fn body<'a>(code: &'a str, signature: &str) -> &'a str {
    let start = code
        .find(signature)
        .unwrap_or_else(|| panic!("{signature}"));
    let indent = code[..start].rsplit('\n').next().unwrap_or("");
    let close = format!("\n{indent}}}");
    let end = code[start..].find(&close).expect("the closing brace");
    &code[start..start + end + close.len()]
}

#[test]
fn the_stop_transition_is_the_only_latch_after_the_guards_entry() {
    // W-9 (round 2; round 3's entry order), over production code under
    // `crates/security/src`.
    let guard = production(
        include_str!("operation_guard.rs"),
        "#[cfg(test)]\npub(crate) mod scripted",
    );
    let gate = production(
        include_str!("../commit_authority.rs"),
        "#[cfg(test)]\nmod tests",
    );
    let monitor = production(include_str!("../revocation.rs"), "#[cfg(test)]\nmod tests");
    // The word: one fetch-OR of `LATCHED`, in the section's word operation;
    // nothing clears, stores or swaps the word.
    assert_eq!(gate.matches("fetch_or(").count(), 3);
    assert!(body(&gate, "fn open_window(").contains("fetch_or(WINDOW_OPEN, Ordering::SeqCst)"));
    assert!(body(&gate, "fn close_window(").contains("fetch_or(WINDOW_CLOSED, Ordering::SeqCst)"));
    assert!(body(&gate, "pub(super) fn fetch_latch(self)").contains("fetch_or(LATCHED,"));
    for forbidden in ["fetch_and(", ".store(", ".swap(", "Mutex", ".lock("] {
        assert!(!gate.contains(forbidden), "{forbidden}");
    }
    // `x4.gate.latch.after` follows the section's return (LD8-4), once.
    assert_eq!(
        gate.matches(r#"crash_barrier!("x4.gate", "latch.after", step)"#)
            .count(),
        1
    );
    assert!(body(&gate, "fn latch_within<R>").contains(
        "let result = section(Latching(self));\n        \
         opensip_platform::crash_barrier!(\"x4.gate\", \"latch.after\", step);"
    ));
    // Every latch of an operation's gate after the guard's entry is the stop
    // transition: `latch_within` is called in exactly one place, the stop
    // transition. The other latches are bare: the monitor's at the
    // lease-free point, and the gate's own, which is test code only.
    assert_eq!(guard.matches("latch_within(").count(), 1);
    assert!(
        body(
            &guard,
            "pub(crate) fn stop(&self, cause: StopCause) -> Transition"
        )
        .contains("latch_within(")
    );
    let bare = body(&guard, "pub(crate) fn latch_bare(");
    assert_eq!(
        guard.matches(".latch()").count(),
        bare.matches(".latch()").count()
    );
    assert!(guard.contains("    #[cfg(test)]\n    pub(crate) fn latch_bare("));
    assert!(gate.contains(
        "    #[cfg(test)]\n    pub(crate) fn latch(&self) -> AttemptState {\n        self.0.latch()"
    ));
    assert_eq!(monitor.matches(".latch()").count(), 2);
    assert_eq!(
        body(&monitor, "impl MonitorStop for StopObserver")
            .matches(".latch()")
            .count(),
        2
    );
    assert!(!monitor.contains("latch_within("));
    for (name, code) in [
        (
            "commit_session.rs",
            production(
                include_str!("commit_session.rs"),
                "#[cfg(test)]\nimpl SessionEnd",
            ),
        ),
        (
            "operation_handoff.rs",
            production(
                include_str!("operation_handoff.rs"),
                "#[cfg(test)]\nmod tests",
            ),
        ),
    ] {
        for forbidden in [".latch()", "latch_within(", "StopObserver", "OperationGate"] {
            assert!(!code.contains(forbidden), "{name}: {forbidden}");
        }
    }
    // The record's one insert is inside the stop transition, which records
    // only when its own fetch-OR set `LATCHED`. `Shared::record` is gone, and
    // a reader (`latched`) records nothing.
    assert!(!guard.contains("fn record("));
    assert_eq!(guard.matches("get_or_insert(").count(), 2);
    assert_eq!(guard.matches("insert(").count(), 3); // both stop sections and drift
    assert!(
        body(
            &guard,
            "fn observe(&self, cell: &mut MonitorCell<StopHandle>)"
        )
        .contains(".insert(drift)")
    );
    let reader = body(&guard, "fn latched(&self) -> GuardRefusal");
    for forbidden in ["insert", ".stop(", "latch"] {
        assert!(
            !reader.replace("fn latched", "").contains(forbidden),
            "{forbidden}"
        );
    }
    let cancel = body(&guard, "pub(crate) fn cancel(&self, signal: D9Signal)");
    let critical_start = cancel.find("let mut cause = slot(&self.0.cause);").unwrap();
    let critical_end = cancel[critical_start..].find("\n        };").unwrap() + critical_start;
    let critical = &cancel[critical_start..critical_end];
    assert!(critical.contains("let outcome = self.0.gate.cancel();"));
    assert!(critical.contains("cause.get_or_insert(StopCause::Operator { signal });"));
    for forbidden in [
        "crash_barrier!",
        "monitor",
        ".wait(",
        ".recv(",
        ".send(",
        "sleep(",
        "callback",
        "read(",
        "write(",
    ] {
        assert!(
            !critical.contains(forbidden),
            "cancellation cause section: {forbidden}"
        );
    }
    assert!(cancel[critical_end..].contains(r#"crash_barrier!("x4.gate", "latch.after", step)"#));
    assert_eq!(guard.matches("self.0.gate.cancel()").count(), 1);
    // The critical section holds only the word's operation and the record's
    // insert and read: no I/O, wait, callback, crash point or monitor.
    let stop = body(
        &guard,
        "pub(crate) fn stop(&self, cause: StopCause) -> Transition",
    );
    assert!(stop.contains(
        "        let transition = gate.latch_within(|latching| {
            let mut slot = slot(record);
            let latched = latching.fetch_latch();
            if latched.first {
                slot.get_or_insert(cause);
            }
            Transition {
                state: latched.state,
                first: latched.first,
                cause: slot.clone(),
            }
        });"
    ));
    assert!(!stop.contains("monitor"));
    assert!(
        body(&guard, "fn slot(").contains("cause.lock().unwrap_or_else(PoisonError::into_inner)")
    );
    // The cause lock is taken only by the transition, the reader, the entry
    // check and the test seam that holds it.
    assert_eq!(
        guard.matches("slot(&").count() + guard.matches("slot(record)").count(),
        5
    );
    // `admit`'s success path takes no stop-cause lock: the gate takes no lock
    // (above), and the checkpoint reads a cause only on admit's refusal.
    let admit = body(&guard, "pub(crate) fn admit<P>(");
    assert_eq!(admit.matches("latched()").count(), 1);
    assert!(admit.find(".map_err(|(value, _)|").unwrap() < admit.find("latched()").unwrap());
    assert!(body(&guard, "fn steps<R>(").contains("Ok(value) => Ok(value),"));
    // The entry order (round 3): the record, the monitor's rebind, the check
    // under the record's lock, then the observer's spawn. Nothing bare
    // survives into the guard but behind the stop handle.
    let enter = body(&guard, "fn enter(lease_free: LeaseFree)");
    let order = [
        "StopHandle::new(stop)",
        "monitor.rebind(stop.clone())",
        "stop.entry_latched()",
        "if latched { Err(entered) } else { Ok(entered) }",
    ]
    .map(|step| enter.find(step).unwrap_or_else(|| panic!("{step}")));
    assert!(order.is_sorted(), "{order:?}");
    let start = body(&guard, "pub(crate) fn start(");
    assert!(start.find("enter(lease_free)").unwrap() < start.find(".spawn(").unwrap());
    assert!(body(&guard, "fn entry_latched(&self)").contains("let _slot = slot(&self.0.cause);"));
    let shared = body(&guard, "struct Shared {");
    assert!(shared.contains("monitor: Mutex<MonitorCell<StopHandle>>,"));
    assert!(shared.contains("stop: StopHandle,"));
    assert!(!shared.contains("StopObserver"));
}

#[test]
fn operator_exchange_wins_before_each_readers_stop_section() {
    use super::super::commit_session::end_path_for_tests::reason;
    // The scripted seams run before the reader's stop section, while its
    // monitor may be held. Both the boundary's own failure and its later
    // AlreadyStopped read must preserve the recorded operator.
    for source in [
        Source::Read,
        Source::Boundary,
        Source::Unwind,
        Source::Revoked,
    ] {
        let rig = Rig::new();
        rig.stop.open_window();
        let result = rig.drive(source, &mut || {
            assert_eq!(
                rig.stop.cancel(D9Signal::Sigint),
                LatchOutcome::BeforeAdmission
            );
        });
        let operator = StopCause::Operator {
            signal: D9Signal::Sigint,
        };
        assert_eq!(result, reported(source, &operator, false));
        assert_eq!(rig.stop.latched().row(), operator.row());
        assert_eq!(rig.stop.cause(), Some(operator.clone()));
        assert_eq!(reason(rig.stop.cause().as_ref()), "operator");
        assert_eq!(
            rig.drive(source, &mut || {}),
            reported(source, &operator, false)
        );
    }
    // Admission refusal uses the same gate and reads the same cause;
    // cancellation never manufactures a second permit or a placeholder.
    let (gate, observer) = OperationGate::new();
    let stop = StopHandle::new(observer);
    stop.open_window();
    assert_eq!(
        stop.cancel(D9Signal::Sigterm),
        LatchOutcome::BeforeAdmission
    );
    assert!(matches!(
        gate.admit("prepared"),
        Err(("prepared", AttemptState::LatchedBeforeAdmission))
    ));
    let operator = StopCause::Operator {
        signal: D9Signal::Sigterm,
    };
    assert_eq!(stop.latched().row(), operator.row());
    assert_eq!(reason(stop.cause().as_ref()), "operator");
}
