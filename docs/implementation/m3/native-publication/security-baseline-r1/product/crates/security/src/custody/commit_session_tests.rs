// Law X3d r6 (unit X3d-1) through the real handoff, on scratch homes only:
// each test publishes a real P0 under a scratch H with X4T-0's signed
// accepted store, hands an operation off with a scripted monitor clock and
// observer ticks on request, and opens the one `CommitSession` on it. The
// evidence ledger is storage's (X3d-2): here a test adapter stands in for
// its staging and `COMMIT`, so these tests pin the security side only (the
// order, the latch, the stop order, the forfeit and the end path). Nothing
// sleeps; nothing opens the real account's I.
use crate::commit_authority::AttemptState;
use crate::custody::commit_session::end_path_for_tests as end_path;
use crate::custody::commit_session::{
    CommitAdapter, CommitSession, EvidenceCommit, RolloverDisclosure, SealOutcome, SealRefusal,
    SessionEnd, StagedCommit, StoppedSession, begin_journal_txn, seal_under_append_lock,
};
use crate::custody::installation_read_fixture::churned;
use crate::journal_store::{
    AppendStep, Fault, RecordDraft, end_path_append_bound, end_path_append_cost, fixtures,
    plant_committed_tail_for_tests,
};
use crate::trust::ObservationHook;

/// A started operation with its scripted clock and the writer's trees.
struct Started {
    operation: ProjectOperation,
    clock: scripted::Clock,
    _trees: ReadProducers,
}
fn start(fixture: &ReadFixture, project: &Path, tag: &str) -> Started {
    let (mut writer, trees) = new_writer(fixture, tag);
    let subject = admitted(&mut writer, project);
    let clock = scripted::Clock::new();
    let operation = writer
        .begin_operation_with(
            subject,
            WriterLease::AppendWrite,
            &inputs(),
            &scripted::invocation(),
            scripted::seam(&clock, ObservationHook::live()),
        )
        .unwrap();
    Started {
        operation,
        clock,
        _trees: trees,
    }
}
/// A fresh eligible project and an operation on it.
fn started(tag: &str) -> (ReadFixture, String, Started) {
    let (fixture, project, n) = eligible(tag);
    let started = start(&fixture, &project, tag);
    (fixture, n, started)
}
/// Item 3 steps 0 and 3 on a fresh session: the reserve, then capacity.
fn funded(operation: ProjectOperation) -> CommitSession {
    CommitSession::open(operation)
        .unwrap()
        .reserve_end_path()
        .unwrap()
        .capacity()
        .unwrap()
}

/// Every record of N's carrier: (type, seq, body).
fn records(fixture: &ReadFixture, n: &str) -> Vec<(String, i64, String)> {
    let path = namespace_path(fixture, n).join("grant-journal.sqlite");
    let c = rusqlite::Connection::open_with_flags(
        &path,
        rusqlite::OpenFlags::SQLITE_OPEN_READ_ONLY | rusqlite::OpenFlags::SQLITE_OPEN_NO_MUTEX,
    )
    .unwrap();
    let mut statement = c
        .prepare(
            "SELECT record_type, seq, body FROM grant_journal_v3 ORDER BY grantGeneration, seq",
        )
        .unwrap();
    statement
        .query_map([], |r| Ok((r.get(0)?, r.get(1)?, r.get(2)?)))
        .unwrap()
        .map(Result::unwrap)
        .collect()
}
fn kinds(fixture: &ReadFixture, n: &str) -> Vec<String> {
    records(fixture, n).into_iter().map(|(k, ..)| k).collect()
}
/// The floor did not move and nothing is locked: the end step took no fence.
fn no_end_step(fixture: &ReadFixture, n: &str, end: &SessionEnd, floor: (i64, i64, bool)) {
    assert!(!end.end_step_entered());
    assert!(matches!(end.end(), OperationEnd::NotEntered));
    assert_eq!(floor_of(fixture, n), floor);
    assert!(fence_free(fixture) && unlocked(fixture, n));
}

/// The test's stand-in for storage's private adapter (X3d-2).
#[derive(Clone, Copy, PartialEq, Eq)]
enum Stage {
    Staged,
    /// A staging I/O error, in the open evidence transaction.
    Io,
    /// The staging blocks past S6's bound before the final checkpoint.
    Stall,
}
struct Adapter {
    stage: Stage,
    commit: bool,
    clock: scripted::Clock,
}
struct Staged {
    commit: bool,
}
impl CommitAdapter for Adapter {
    type Staged = Staged;
    type Refusal = &'static str;
    fn stage(
        self,
        binding: &crate::custody::commit_session::JournalSealBinding,
        work: &mut WorkScope<'_>,
    ) -> Result<Staged, WorkFailure<&'static str>> {
        assert_eq!(binding.grant_generation(), 1);
        work.run(WorkCost::default(), |_| match self.stage {
            Stage::Staged => Ok(Staged {
                commit: self.commit,
            }),
            Stage::Io => Err(WorkFailure::Operation("staging-io")),
            Stage::Stall => {
                self.clock.advance(Duration::from_secs(11));
                Ok(Staged {
                    commit: self.commit,
                })
            }
        })
    }
}
impl StagedCommit for Staged {
    type Committed = &'static str;
    fn commit(self) -> EvidenceCommit<&'static str> {
        if self.commit {
            EvidenceCommit::Committed("receipt")
        } else {
            EvidenceCommit::Undetermined
        }
    }
}
fn adapter(started: &Started, stage: Stage, commit: bool) -> Adapter {
    Adapter {
        stage,
        commit,
        clock: started.clock.clone(),
    }
}
/// Item 4 on a funded session: the journal's level 3, then the SEAL path.
fn publish(
    started: Started,
    stage: Stage,
    commit: bool,
) -> (SealOutcome<&'static str, &'static str>, StoppedSession) {
    let adapter = adapter(&started, stage, commit);
    let txn = begin_journal_txn(funded(started.operation)).unwrap();
    seal_under_append_lock(txn, &fixtures::replay(), adapter)
}

// ------------------------------------------------------------- the session

#[test]
fn open_draws_an_execution_id_and_operation_ref_and_binds_the_operation() {
    churned(|| {
        let (fixture, n, started) = started("x3d1-open");
        let selected = started.operation.selected_core().0.to_owned();
        let session = CommitSession::open(started.operation).unwrap();
        let id = session.execution_id().to_owned();
        assert!(id.starts_with("exec1_") && id.len() == 38, "{id}");
        assert!(
            id[6..]
                .bytes()
                .all(|b| matches!(b, b'0'..=b'9' | b'a'..=b'f'))
        );
        let op = session.operation_ref();
        assert!(op.starts_with("op-") && op.len() == 35, "{op}");
        assert_eq!(session.namespace_id(), n);
        assert_eq!(session.store_instance(), fixture.store);
        assert_eq!(
            session.carrier_digest(),
            opensip_identity::digest_hex(&opensip_identity::raw_sha256(n.as_bytes()))
        );
        assert_eq!(session.core_closure(), selected);
        // A refusal before step 0 latches the gate, so a REV is owed, but no
        // reserve was taken: nothing is appended unfunded.
        let end = session.refused().finish();
        assert!(!end.revocation_appended());
        assert!(kinds(&fixture, &n).is_empty());
    });
}

/// Law X3d r9 S10.1 (J1 item 2; unit J3a), control J-C4b's session half:
/// `open` reserves its drawn ExecutionId in the process registry in the
/// drawing step, before the session exists, and the session and its stopped
/// session hold that reservation; two sessions hold two reservations.
#[test]
fn open_reserves_its_execution_id_in_the_process_registry() {
    churned(|| {
        let (_fixture, _n, started) = started("j3a-open-reserves");
        let session = CommitSession::open(started.operation).unwrap();
        let id = session.execution_id().to_owned();
        assert!(opensip_platform::execution_id_reserved(&id), "{id}");
        // The registry's own draw collides with nothing reserved, so a
        // further reservation is another id.
        let other = opensip_platform::reserve_execution_id().unwrap();
        assert_ne!(other.as_str(), id);
        let stopped = session.refused();
        assert_eq!(stopped.execution_id(), Some(id.as_str()));
        let _ = stopped.finish();
        // The reservation outlives the session: never released or reused.
        assert!(opensip_platform::execution_id_reserved(&id));
    });
    // In `open`, the one reservation is the draw point's own effect, and the
    // session is built only after it.
    let source = include_str!("commit_session.rs");
    let open = &source[source.find("    pub fn open(").unwrap()..];
    let open = &open[..open.find("\n    }\n").unwrap()];
    let draw = open.find("\"execution-draw\",").unwrap();
    let reserve = open
        .find("opensip_platform::reserve_execution_id()")
        .unwrap();
    assert!(draw < reserve && reserve < open.find("Ok(CommitSession {").unwrap());
    assert_eq!(open.matches("reserve_execution_id()").count(), 1);
    assert!(!open.contains("request_entropy().map(|bytes| render_id(\"exec1_\""));
    // The session's ExecutionId field is the reservation, not a string.
    let fields = &source[source.find("pub struct CommitSession {").unwrap()..];
    let fields = &fields[..fields.find('}').unwrap()];
    assert!(fields.contains("execution_id: ReservedExecutionId,"));
}

#[test]
fn a_lawful_commit_appends_one_seal_and_no_end_path_record() {
    churned(|| {
        let (fixture, n, started) = started("x3d1-lawful");
        let replayed = fixtures::replay();
        let adapter = adapter(&started, Stage::Staged, true);
        let session = funded(started.operation);
        let execution = session.execution_id().to_owned();
        let operation_ref = session.operation_ref().to_owned();
        let txn = begin_journal_txn(session).unwrap();
        assert_eq!(txn.execution_id(), execution);
        let (outcome, stopped) = seal_under_append_lock(txn, &replayed, adapter);
        match outcome {
            SealOutcome::Committed {
                committed,
                binding,
                latched_after_admission,
            } => {
                assert_eq!(committed, "receipt");
                assert!(!latched_after_admission);
                assert_eq!((binding.grant_generation(), binding.seal_seq()), (1, 1));
                assert_eq!(binding.run_id(), replayed.run_id());
                assert_eq!(binding.operation_ref(), operation_ref);
                assert_eq!(binding.body_sha256().len(), 64);
            }
            other => panic!("{other:?}"),
        }
        assert_eq!(stopped.execution_id(), Some(execution.as_str()));
        let end = stopped.finish();
        assert!(!end.revocation_appended() && !end.cleanup_appended());
        assert_eq!(end.settlement_failure(), None);
        assert_eq!(kinds(&fixture, &n), ["SEAL"]);
        assert_eq!(witness_of(&fixture, &n), (1, 1, "COMMITTED".into()));
        // The end step ran and copied the floor to the SEAL.
        assert!(end.end_step_entered());
        assert_eq!(floor_of(&fixture, &n), (1, 1, true));
        assert!(fence_free(&fixture) && unlocked(&fixture, &n));
    });
}

// ------------------------------------- certain refusals that close the ledger

#[test]
fn a_publication_reserve_overrun_appends_the_rev_and_takes_no_fence() {
    churned(|| {
        let (fixture, n, started) = started("x3d1-overrun");
        let floor = floor_of(&fixture, &n);
        let mut session = CommitSession::open(started.operation)
            .unwrap()
            .reserve_end_path()
            .unwrap();
        // Item 3 step 2 (X3d-2's publication reserve) overruns the attempt
        // ledger: the budget row, and the ledger is closed.
        let overrun = session.charge::<(), ()>(|work| {
            work.run(
                WorkCost {
                    bytes: usize::MAX / 2,
                    ..WorkCost::default()
                },
                |_| Ok(()),
            )
        });
        assert!(matches!(overrun, Err(WorkFailure::Budget(_))));
        let end = session.refused().finish();
        assert!(end.revocation_appended() && !end.cleanup_appended());
        assert_eq!(end.settlement_failure(), None);
        let records = records(&fixture, &n);
        assert_eq!(records.len(), 1);
        assert_eq!(records[0].0, "REV");
        assert!(records[0].2.contains(r#""reason":"operation-stopped""#));
        no_end_step(&fixture, &n, &end, floor);
    });
}

#[test]
fn busy_at_the_evidence_ledger_aborts_the_journal_then_appends_the_rev() {
    churned(|| {
        let (fixture, n, started) = started("x3d1-busy");
        let floor = floor_of(&fixture, &n);
        let mut txn = begin_journal_txn(funded(started.operation)).unwrap();
        // Item 4 step 2: storage's ledger BEGIN IMMEDIATE is busy, inside the
        // attempt ledger's charge; the ledger closes.
        let busy = txn.charge::<(), &str>(|_| Err(WorkFailure::Operation("ledger-busy")));
        assert!(matches!(busy, Err(WorkFailure::Operation("ledger-busy"))));
        // The consuming abort releases the journal's level 3 (F06): the REV's
        // fresh level 3 finds the carrier free.
        let end = txn.abort().finish();
        assert!(end.revocation_appended() && !end.cleanup_appended());
        assert_eq!(kinds(&fixture, &n), ["REV"]);
        no_end_step(&fixture, &n, &end, floor);
    });
}

#[test]
fn a_staging_io_error_rolls_back_then_appends_rev_and_cln() {
    churned(|| {
        let (fixture, n, started) = started("x3d1-staging");
        let floor = floor_of(&fixture, &n);
        let (outcome, stopped) = publish(started, Stage::Io, true);
        assert!(matches!(
            outcome,
            SealOutcome::Refused(SealRefusal::Staging("staging-io"))
        ));
        let end = stopped.finish();
        assert!(end.revocation_appended() && end.cleanup_appended());
        let records = records(&fixture, &n);
        let kinds: Vec<&str> = records.iter().map(|(k, ..)| k.as_str()).collect();
        assert_eq!(kinds, ["SEAL", "REV", "CLN"]);
        assert_eq!(
            records.iter().map(|(_, seq, _)| *seq).collect::<Vec<_>>(),
            [1, 2, 3]
        );
        assert!(records[2].2.contains(
            r#""residuals":["seal-without-evidence-commit","evidence-transaction-rolled-back"]"#
        ));
        assert_eq!(witness_of(&fixture, &n), (1, 3, "COMMITTED".into()));
        no_end_step(&fixture, &n, &end, floor);
    });
}

#[test]
fn a_failed_final_checkpoint_latches_and_the_rev_names_the_fail_stop() {
    churned(|| {
        let (fixture, n, started) = started("x3d1-stall");
        let floor = floor_of(&fixture, &n);
        let (outcome, stopped) = publish(started, Stage::Stall, true);
        match outcome {
            SealOutcome::Refused(SealRefusal::Session(refusal)) => {
                assert!(matches!(refusal.termination(), T::ObserverFailStop { .. }))
            }
            other => panic!("{other:?}"),
        }
        let end = stopped.finish();
        let records = records(&fixture, &n);
        let kinds: Vec<&str> = records.iter().map(|(k, ..)| k.as_str()).collect();
        assert_eq!(kinds, ["SEAL", "REV", "CLN"]);
        assert!(records[1].2.contains(r#""reason":"observer-fail-stop""#));
        assert!(end.revocation_appended() && end.cleanup_appended());
        no_end_step(&fixture, &n, &end, floor);
    });
}

#[test]
fn a_failed_rev_appends_no_cln_and_is_disclosed() {
    churned(|| {
        let (fixture, n, started) = started("x3d1-failed-rev");
        let floor = floor_of(&fixture, &n);
        let (outcome, stopped) = publish(started, Stage::Io, true);
        assert!(matches!(outcome, SealOutcome::Refused(_)));
        // Another holder has the carrier's level 3: the REV's BEGIN IMMEDIATE
        // is busy, the settlement ends, and no CLN follows.
        let holder =
            rusqlite::Connection::open(namespace_path(&fixture, &n).join("grant-journal.sqlite"))
                .unwrap();
        holder.execute_batch("BEGIN IMMEDIATE").unwrap();
        let end = stopped.finish();
        holder.execute_batch("ROLLBACK").unwrap();
        drop(holder);
        assert!(!end.revocation_appended() && !end.cleanup_appended());
        assert_eq!(end.settlement_failure(), Some(&T::Busy));
        assert_eq!(kinds(&fixture, &n), ["SEAL"]);
        no_end_step(&fixture, &n, &end, floor);
    });
}

#[test]
fn a_refused_step_zero_holds_no_reserve_and_appends_nothing() {
    churned(|| {
        let (fixture, n, started) = started("x3d1-step-zero");
        let floor = floor_of(&fixture, &n);
        let mut session = CommitSession::open(started.operation).unwrap();
        // The attempt ledger is closed before step 0: the reserve is refused on
        // the budget row, and the StoppedSession holds none.
        let _ = session.charge::<(), &str>(|_| Err(WorkFailure::Operation("closed")));
        let (refusal, stopped) = session.reserve_end_path().unwrap_err();
        assert_eq!(refusal.termination(), T::BudgetExhausted);
        // The gate is latched, so a REV would be owed; it is never unfunded.
        let end = stopped.finish();
        assert!(!end.revocation_appended());
        assert_eq!(end.settlement_failure(), None);
        assert!(kinds(&fixture, &n).is_empty());
        no_end_step(&fixture, &n, &end, floor);
    });
}

#[test]
fn the_journal_transaction_is_refused_without_the_end_path_reserve() {
    churned(|| {
        let (fixture, n, started) = started("x3d1-unfunded");
        let session = CommitSession::open(started.operation).unwrap();
        let (refusal, stopped) = begin_journal_txn(session).unwrap_err();
        assert_eq!(refusal.termination(), T::Invariant);
        let end = stopped.finish();
        assert!(!end.revocation_appended());
        assert!(kinds(&fixture, &n).is_empty());
        assert!(fence_free(&fixture) && unlocked(&fixture, &n));
    });
}

#[test]
fn a_second_reserve_is_the_invariant_row() {
    churned(|| {
        let (_fixture, _n, started) = started("x3d1-twice");
        let session = CommitSession::open(started.operation)
            .unwrap()
            .reserve_end_path()
            .unwrap();
        let (refusal, stopped) = session.reserve_end_path().unwrap_err();
        assert_eq!(refusal.termination(), T::Invariant);
        // The first reserve is kept: the latched gate's REV is funded.
        assert!(stopped.finish().revocation_appended());
    });
}

// --------------------------------------------------- uncertain outcomes

#[test]
fn an_uncertain_seal_commit_forfeits_the_reserve_and_nothing_follows() {
    churned(|| {
        let (fixture, n, mut started) = started("x3d1-uncertain-seal");
        let floor = floor_of(&fixture, &n);
        // The SEAL's COMMIT lands and reports failure: durability-undetermined.
        started
            .operation
            .carrier_mut()
            .lock_mut()
            .set_hook(|step| (step == AppendStep::Committed).then_some(Fault::Fail));
        let (outcome, stopped) = publish(started, Stage::Staged, true);
        let execution = stopped.execution_id().unwrap().to_owned();
        match outcome {
            SealOutcome::CommitUndetermined { execution_id } => assert_eq!(execution_id, execution),
            other => panic!("{other:?}"),
        }
        let end = stopped.finish();
        assert!(!end.revocation_appended() && !end.cleanup_appended());
        assert_eq!(end.settlement_failure(), None);
        assert_eq!(kinds(&fixture, &n), ["SEAL"]);
        // The witness stays as the uncertain append left it; the next writer
        // reconciles it.
        assert_eq!(witness_of(&fixture, &n).2, "PENDING");
        no_end_step(&fixture, &n, &end, floor);
    });
}

#[test]
fn an_undetermined_evidence_commit_forfeits_the_reserve_and_nothing_follows() {
    churned(|| {
        let (fixture, n, started) = started("x3d1-uncertain-commit");
        let floor = floor_of(&fixture, &n);
        let (outcome, stopped) = publish(started, Stage::Staged, false);
        assert!(matches!(outcome, SealOutcome::CommitUndetermined { .. }));
        let end = stopped.finish();
        // A certain stop here would owe the REV and the CLN.
        assert!(!end.revocation_appended() && !end.cleanup_appended());
        assert_eq!(kinds(&fixture, &n), ["SEAL"]);
        no_end_step(&fixture, &n, &end, floor);
    });
}

#[test]
fn an_undetermined_attempt_admission_forfeits_the_reserve_and_nothing_follows() {
    churned(|| {
        let (fixture, n, started) = started("x3d1-uncertain-attempt");
        let floor = floor_of(&fixture, &n);
        let session = CommitSession::open(started.operation)
            .unwrap()
            .reserve_end_path()
            .unwrap();
        let end = session.undetermined().finish();
        assert!(!end.revocation_appended());
        assert!(kinds(&fixture, &n).is_empty());
        no_end_step(&fixture, &n, &end, floor);
    });
}

// ------------------------------------------------------------- capacity

#[test]
fn an_exhausted_generation_is_returned_with_the_ledger_open() {
    churned(|| {
        // X3b r8 item 5a: no SEAL fits after 9007199254740987.
        const FULL: i64 = 9_007_199_254_740_988;
        let (fixture, project, n) = eligible("x3d1-full");
        let first = start(&fixture, &project, "x3d1-full");
        assert!(matches!(
            first.operation.end(JournalOutcome::Certain),
            OperationEnd::Ended(_)
        ));
        plant_committed_tail_for_tests(&namespace_path(&fixture, &n), &n, FULL);
        let next = start(&fixture, &project, "x3d1-fulm");
        let cancellation = next.operation.guard().cancellation_handle();
        let mut session = CommitSession::open(next.operation)
            .unwrap()
            .reserve_end_path()
            .unwrap();
        let token = session.take_cancellation_latch().unwrap();
        let (exhausted, stopped) = session.capacity().unwrap_err();
        assert!(!stopped.admitted_at_close());
        // The window never opened on this real path. Set only its open bit
        // in the fixture after return to prove that capacity set CLOSED;
        // merely testing a never-opened token would not prove the close.
        cancellation.open_window();
        assert_eq!(
            token.latch(crate::D9Signal::Sigterm),
            crate::LatchOutcome::OutsideWindow
        );
        assert_eq!(
            (exhausted.grant_generation(), exhausted.proven_tail_seq()),
            (1, FULL)
        );
        // Not a refusal: nothing is owed, and the end step rolls over.
        let end = stopped.finish();
        assert!(!end.revocation_appended());
        match end.end() {
            OperationEnd::RolledOver {
                rollover: RolloverOutcome::Rolled { opened: 2, .. },
                end: Ok(_),
            } => {}
            other => panic!("{other:?}"),
        }
        assert!(fence_free(&fixture) && unlocked(&fixture, &n));
    });
}

// ------------------------------- X7b: the rollover route, as disclosed

/// Law X7 r5 item 6 (unit X7b): a real generation filled to an exhausted
/// tail, a second operation whose session met the exhaustion at item 3 step
/// 3, and its stopped session, not yet finished. `hold` runs before the
/// second operation begins, and what it returns is held until the end.
struct Exhausted<H> {
    fixture: ReadFixture,
    n: String,
    stopped: StoppedSession,
    _held: H,
    _next: (scripted::Clock, ReadProducers),
}
fn exhausted_session<H>(
    tag: &str,
    next: &str,
    hold: impl FnOnce(&ReadFixture, &str) -> H,
) -> Exhausted<H> {
    const FULL: i64 = 9_007_199_254_740_988;
    let (fixture, project, n) = eligible(tag);
    let first = start(&fixture, &project, tag);
    assert!(matches!(
        first.operation.end(JournalOutcome::Certain),
        OperationEnd::Ended(_)
    ));
    plant_committed_tail_for_tests(&namespace_path(&fixture, &n), &n, FULL);
    let held = hold(&fixture, &n);
    let Started {
        operation,
        clock,
        _trees,
    } = start(&fixture, &project, next);
    let session = CommitSession::open(operation)
        .unwrap()
        .reserve_end_path()
        .unwrap();
    let (exhausted, stopped) = session.capacity().unwrap_err();
    assert_eq!(
        (exhausted.grant_generation(), exhausted.proven_tail_seq()),
        (1, FULL)
    );
    Exhausted {
        fixture,
        n,
        stopped,
        _held: held,
        _next: (clock, _trees),
    }
}
fn terminals(fixture: &ReadFixture, n: &str) -> usize {
    kinds(fixture, n)
        .iter()
        .filter(|k| *k == "TERMINAL")
        .count()
}

#[test]
fn an_exhausted_carrier_through_finish_discloses_the_rollover_as_rolled() {
    let e = exhausted_session("x7b-rolled", "x7b-rollee", |_, _| ());
    let end = e.stopped.finish();
    // Nothing was owed, the end step ran the rollover, and its floor copy
    // followed: no end-step failure, and no row for the rollover.
    assert!(!end.revocation_appended() && end.settlement_failure().is_none());
    assert_eq!(end.end_step_failure(), None);
    assert_eq!(
        end.rollover(),
        Some(RolloverDisclosure::Rolled {
            opened_generation: 2
        })
    );
    assert_eq!(terminals(&e.fixture, &e.n), 1);
    assert_eq!(floor_of(&e.fixture, &e.n), (2, 0, false));
    assert!(fence_free(&e.fixture) && unlocked(&e.fixture, &e.n));
}

#[test]
fn a_held_readers_lease_discloses_the_rollover_as_skipped() {
    // A reader holds N's readers.lease throughout: the rollover cannot take
    // EXCLUSIVE, writes nothing, and the end step continues.
    let e = exhausted_session("x7b-skipped", "x7b-skippee", |fixture, n| {
        hold(
            &namespace_path(fixture, n).join(READERS_LEASE),
            LockMode::Shared,
        )
    });
    let end = e.stopped.finish();
    assert_eq!(end.rollover(), Some(RolloverDisclosure::Skipped));
    assert_eq!(end.end_step_failure(), None);
    assert_eq!(terminals(&e.fixture, &e.n), 0);
    assert!(fence_free(&e.fixture));
}

#[test]
fn a_busy_journal_transaction_discloses_the_rollover_as_refused_busy() {
    // Another holder has the carrier's level 3: the TERMINAL's BEGIN
    // IMMEDIATE is busy, nothing is written, and the closed attempt ledger
    // runs no floor copy (X3b r10 item 4), which is not a failure.
    let e = exhausted_session("x7b-refused", "x7b-refusee", |_, _| ());
    let holder =
        rusqlite::Connection::open(namespace_path(&e.fixture, &e.n).join("grant-journal.sqlite"))
            .unwrap();
    holder.execute_batch("BEGIN IMMEDIATE").unwrap();
    let end = e.stopped.finish();
    holder.execute_batch("ROLLBACK").unwrap();
    drop(holder);
    assert_eq!(end.rollover(), Some(RolloverDisclosure::Refused(T::Busy)));
    assert_eq!(end.end_step_failure(), None);
    assert_eq!(terminals(&e.fixture, &e.n), 0);
    assert!(fence_free(&e.fixture) && unlocked(&e.fixture, &e.n));
}

#[test]
fn an_end_step_that_stops_before_the_rollover_discloses_its_failure_and_no_rollover() {
    // N is no longer bound by name when the end step rebinds it under the
    // fence: the end step refuses before the rollover, which is not
    // attempted and so not disclosed.
    let e = exhausted_session("x7b-moved", "x7b-movee", |_, _| ());
    let namespace = namespace_path(&e.fixture, &e.n);
    fs::rename(&namespace, namespace.with_file_name("moved")).unwrap();
    let end = e.stopped.finish();
    assert_eq!(end.rollover(), None);
    assert_eq!(
        end.end_step_failure(),
        Some(T::Custody {
            subject: "required-files-changed"
        })
    );
    assert!(fence_free(&e.fixture));
}

// The rollover outcomes no fault reaches through `finish` in production:
// the handoff's own end step at X3b-4's test points, as X2e's tests drive
// it, read back through `SessionEnd`'s accessors.

#[test]
fn an_undetermined_rollover_is_disclosed_as_undetermined_with_no_end_step_failure() {
    use crate::journal_store::{Fault, RolloverStep, TestPoints};
    let (fixture, n, operation, _trees) = exhausted_operation("x7b-und-a", None);
    let points = TestPoints {
        step: Some(std::sync::Arc::new(|step| {
            (step == RolloverStep::Opened).then_some(Fault::Fail)
        })),
        ..TestPoints::default()
    };
    let end = end_path::session_end(end_at(operation, &points));
    assert_eq!(end.rollover(), Some(RolloverDisclosure::Undetermined));
    // Nothing followed, and a copy not attempted is not a failure.
    assert_eq!(end.end_step_failure(), None);
    assert_eq!(floor_of(&fixture, &n), (1, EXHAUSTED, true));
}

#[test]
fn a_rollover_short_of_its_reservation_is_disclosed_on_the_budget_row() {
    let (_twin, _, measured, _trees) = exhausted_operation("x7b-rsv-a", None);
    let used = measured.attempt_used();
    drop(measured);
    let cap = WorkCost {
        objects: 65_536,
        edges: 131_072,
        bytes: used.bytes + (1 << 20),
    };
    let (fixture, n, operation, _trees) = exhausted_operation("x7b-rsv-b", Some(cap));
    let end = end_path::session_end(operation.end(exhausted()));
    assert_eq!(
        end.rollover(),
        Some(RolloverDisclosure::Refused(T::BudgetExhausted))
    );
    assert_eq!(end.end_step_failure(), None);
    not_rolled(&fixture, &n);
}

#[test]
fn an_io_refused_rollover_and_its_failed_copy_are_each_disclosed_on_their_rows() {
    let (fixture, n, operation, _trees) = exhausted_operation("x7b-iof-a", None);
    floor_file(&fixture, &n, 0o000);
    let end = end_path::session_end(operation.end(exhausted()));
    floor_file(&fixture, &n, 0o600);
    assert_eq!(end.rollover(), Some(RolloverDisclosure::Refused(T::HostIo)));
    assert_eq!(end.end_step_failure(), Some(T::HostIo));
    not_rolled(&fixture, &n);
}

#[test]
fn a_failed_copy_after_a_rollover_is_an_end_step_failure_beside_rolled() {
    use crate::journal_store::{RolloverStep, TestPoints};
    let (fixture, n, operation, _trees) = exhausted_operation("x7b-cpy-a", None);
    let floor = floor_path(&fixture, &n);
    let points = TestPoints {
        step: Some(std::sync::Arc::new(move |step| {
            if step == RolloverStep::WriterReleased {
                fs::set_permissions(&floor, fs::Permissions::from_mode(0o000)).unwrap();
            }
            None
        })),
        ..TestPoints::default()
    };
    let end = end_path::session_end(end_at(operation, &points));
    floor_file(&fixture, &n, 0o600);
    assert_eq!(
        end.rollover(),
        Some(RolloverDisclosure::Rolled {
            opened_generation: 2
        })
    );
    assert_eq!(end.end_step_failure(), Some(T::HostIo));
}

// --------------------------------------------------------- the end path

#[test]
fn the_reserve_is_one_bounded_rev_and_one_bounded_cln_at_their_exact_cost() {
    let n = "00000000-0000-4000-8000-000000000001";
    let op = format!("op-{}", "a".repeat(32));
    let rev = end_path::longest_rev();
    let cln = end_path::cleanup();
    let expected = end_path_append_bound(n, &op, &rev)
        .unwrap()
        .checked_add(end_path_append_bound(n, &op, &cln).unwrap())
        .unwrap();
    assert_eq!(end_path::reserve_cost(n, &op), Some(expected));
    // The bound is the largest generation at the last ordinary sequence.
    assert_eq!(
        end_path_append_bound(n, &op, &rev),
        end_path_append_cost(n, &op, &rev, i64::MAX, 9_007_199_254_740_990)
    );
    // The closed REV set, and the longest one bounds every other.
    assert_eq!(
        end_path::reasons(),
        [
            "trust-revoked",
            "policy",
            "observer-fail-stop",
            "stale-guard",
            "operation-stopped",
            "operator"
        ]
    );
    let mut longer = end_path::cleanup();
    if let RecordDraft::Cln { residuals } = &mut longer {
        residuals[1].push('x');
    }
    for (rev_kind, draft, admitted) in [
        (true, rev.clone(), true),
        (false, cln.clone(), true),
        (false, longer, false),
        (true, cln.clone(), false),
        (false, rev.clone(), false),
    ] {
        assert_eq!(end_path::admits(n, &op, rev_kind, &draft), admitted);
    }
    // One byte over the longest reason is refused before any effect.
    let RecordDraft::Rev { reason, .. } = &rev else {
        unreachable!()
    };
    let over = RecordDraft::Rev {
        reason: format!("{reason}x"),
        trust_epoch_observed: None,
    };
    assert!(!end_path::admits(n, &op, true, &over));
    // A trust epoch is never recorded by the end path: any one is over.
    let epoch = RecordDraft::Rev {
        reason: reason.clone(),
        trust_epoch_observed: Some(opensip_identity::JsonValue::Object(Default::default())),
    };
    assert!(!end_path::admits(n, &op, true, &epoch));
}

#[test]
fn a_real_rev_and_cln_charge_exactly_the_cost_function_at_the_last_slots() {
    churned(|| {
        // The REV takes 9007199254740989 and the CLN 9007199254740990, the two
        // slots X3b r8 item 5a reserves after the highest SEAL.
        const TAIL: i64 = 9_007_199_254_740_988;
        let (fixture, project, n) = eligible("x3d1-exact");
        let first = start(&fixture, &project, "x3d1-exact");
        assert!(matches!(
            first.operation.end(JournalOutcome::Certain),
            OperationEnd::Ended(_)
        ));
        plant_committed_tail_for_tests(&namespace_path(&fixture, &n), &n, TAIL);
        let mut next = start(&fixture, &project, "x3d1-exacu");
        let op = format!("op-{}", "e".repeat(32));
        for (draft, seq) in [
            (end_path::longest_rev(), TAIL + 1),
            (end_path::cleanup(), TAIL + 2),
        ] {
            let before = next.operation.attempt_used();
            next.operation
                .journal(|location, carrier, _checkpoint, work| {
                    let held = carrier.lock().begin(location, work)?.acquire()?;
                    held.append(&op, &draft, work).map_err(|error| match error {
                        crate::journal_store::AppendError::Refused(f)
                        | crate::journal_store::AppendError::Undetermined(f) => f,
                    })
                })
                .unwrap();
            let used = next.operation.attempt_used();
            let charged = WorkCost {
                objects: used.objects - before.objects,
                edges: used.edges - before.edges,
                bytes: used.bytes - before.bytes,
            };
            assert_eq!(
                charged,
                end_path_append_cost(&n, &op, &draft, 1, seq).unwrap()
            );
            // The bound covers it, and only the generation's width differs.
            let bound = end_path_append_bound(&n, &op, &draft).unwrap();
            assert_eq!(
                (charged.objects, charged.edges),
                (bound.objects, bound.edges)
            );
            assert!(charged.bytes < bound.bytes);
        }
        assert_eq!(
            kinds(&fixture, &n)[1..],
            ["REV".to_owned(), "CLN".to_owned()]
        );
        drop(next);
    });
}

#[test]
fn the_settlement_reserve_has_one_production_caller_each() {
    // Law X3d r6 item 8: in production code, the platform's
    // `reserve_settlement` and `settle` are reached only through the one
    // chain attempt -> receipt -> operation -> session, each link with one
    // caller: the session's end-path step and `StoppedSession::finish`.
    let root = Path::new(env!("CARGO_MANIFEST_DIR")).join("..");
    let mut sources = Vec::new();
    let mut stack = vec![root.clone()];
    while let Some(dir) = stack.pop() {
        for entry in fs::read_dir(&dir).unwrap() {
            let path = entry.unwrap().path();
            let text = path.to_string_lossy().into_owned();
            if path.is_dir() {
                if !text.ends_with("/target") && !text.contains("/tests") {
                    stack.push(path);
                }
            } else if text.contains("/src/")
                && text.ends_with(".rs")
                && !text.ends_with("_tests.rs")
            {
                sources.push(path);
            }
        }
    }
    let count = |needle: &str| -> BTreeMap<String, usize> {
        let mut found = BTreeMap::new();
        for path in &sources {
            let relative = path
                .strip_prefix(&root)
                .unwrap()
                .to_string_lossy()
                .into_owned();
            if relative == "platform/src/work_ledger.rs" {
                continue;
            }
            let n = fs::read_to_string(path)
                .unwrap()
                .lines()
                .filter(|l| !l.trim_start().starts_with("//"))
                .map(|l| l.matches(needle).count())
                .sum::<usize>();
            if n > 0 {
                found.insert(relative, n);
            }
        }
        found
    };
    let one = |file: &str| BTreeMap::from([(file.to_owned(), 1)]);
    assert_eq!(
        count(".reserve_settlement("),
        one("security/src/initial_installation.rs")
    );
    assert_eq!(
        count(".ledger.settle("),
        one("security/src/initial_installation.rs")
    );
    // Other owners have private state-machine helpers named `settle`.
    // Admit only their exact existing `self.settle` call counts and private
    // signatures, never a whole-file exemption for a ledger call.
    let mut settle = count(".settle(");
    settle.remove("security/src/initial_installation.rs");
    for (file, signature, calls, accepted_call) in [
        (
            "components/src/supervisor.rs",
            "    fn settle(&mut self) {",
            3,
            "self.settle();",
        ),
        (
            "host/src/archive_decoder/tar.rs",
            "    fn settle(&mut self) -> Result<(), DecodeError<C::Error>> {",
            2,
            "self.settle()?;",
        ),
    ] {
        let source = fs::read_to_string(root.join(file)).unwrap();
        assert!(source.contains(signature), "{file}: private helper changed");
        let helper_calls = |text: &str| {
            text.lines()
                .filter(|line| line.trim() == accepted_call)
                .count()
        };
        let own_calls = helper_calls(&source);
        // Preserve the total and the private signature while replacing exactly
        // one accepted receiver. Identifier suffixes must never inherit `self`.
        for receiver in ["myself", "not_self", "ledger", "éself"] {
            let mut planted = false;
            let changed = source
                .lines()
                .map(|line| {
                    if !planted && line.trim() == accepted_call {
                        planted = true;
                        line.replacen("self.settle(", &format!("{receiver}.settle("), 1)
                    } else {
                        line.to_owned()
                    }
                })
                .collect::<Vec<_>>()
                .join("\n");
            assert!(planted && changed.contains(signature));
            let total = changed
                .lines()
                .filter(|line| !line.trim_start().starts_with("//"))
                .map(|line| line.matches(".settle(").count())
                .sum::<usize>();
            assert_eq!(total, calls, "{file}: negative must preserve total");
            assert_eq!(
                helper_calls(&changed),
                calls - 1,
                "{file}: {receiver} must be refused as a helper receiver"
            );
        }
        assert_eq!(own_calls, calls, "{file}: private helper caller count");
        assert_eq!(
            settle.remove(file),
            Some(calls),
            "{file}: unexpected ledger or other settle call"
        );
    }
    assert_eq!(
        settle,
        BTreeMap::from([("security/src/custody/ordinary_writer.rs".to_owned(), 9)])
    );
    assert!(
        fs::read_to_string(root.join("security/src/custody/ordinary_writer.rs"))
            .unwrap()
            .contains("    fn settle<R>(")
    );
    for wrapper in [".reserve_end_path_settlement(", ".settle_end_path("] {
        assert_eq!(
            count(wrapper),
            BTreeMap::from([
                ("security/src/custody/commit_session.rs".to_owned(), 1),
                ("security/src/custody/operation_handoff.rs".to_owned(), 1),
                ("security/src/custody/read_premise.rs".to_owned(), 1),
            ]),
            "{wrapper}"
        );
    }
    let session = include_str!("commit_session.rs");
    assert_eq!(session.matches(".reserve_end_path_settlement(").count(), 1);
    assert!(
        session[session.find("pub fn reserve_end_path(").unwrap()..]
            .find(".reserve_end_path_settlement(")
            .unwrap()
            < session[session.find("pub fn reserve_end_path(").unwrap()..]
                .find("\n    }\n")
                .unwrap()
    );
    let finish = &session[session.find("pub fn finish(self)").unwrap()..];
    assert!(finish.find(".settle_end_path(").unwrap() < finish.find("\n    }\n").unwrap());
}

#[test]
fn the_crash_points_are_the_laws_names_in_registered_scopes() {
    // Law X9 r1 item 5's `x3d.*` scopes, placed by this unit (the
    // `x3d.publish.published` point is X3d-2's).
    let session = include_str!("commit_session.rs");
    let handoff = include_str!("operation_handoff.rs");
    for (source, point) in [
        (
            session,
            r#""x3d.session",
                    "execution-draw",
                    draw,"#,
        ),
        (
            session,
            r#"crash_barrier!("x3d.session", "settlement-reserved", step)"#,
        ),
        (
            session,
            r#"crash_barrier!("x3d.publish", "after-staging", step)"#,
        ),
        (
            session,
            r#"crash_barrier!("x3d.publish", "before-final-checkpoint", step)"#,
        ),
        (
            session,
            r#"crash_barrier!("x3d.publish", "commit-returned", step)"#,
        ),
        (
            session,
            r#"crash_barrier!("x3d.finish", "settle.before", step)"#,
        ),
        (
            session,
            r#"crash_barrier!("x3d.finish", "settle.after", step)"#,
        ),
        (
            handoff,
            r#"crash_barrier!("x3d.finish", "lease-release", step)"#,
        ),
        (
            handoff,
            r#"crash_barrier!("x3d.finish", "end-step.before", step)"#,
        ),
        (
            handoff,
            r#"crash_barrier!("x3d.finish", "end-step.after", step)"#,
        ),
    ] {
        assert!(source.contains(point), "{point}");
    }
}

// ------------------------------------------------------ unit X3d-2's hooks

/// Unit X3d-2: the session's target identity is the ACTIVE row's ProjectId,
/// and its store root is the endpoint's own `I/stores/S`: the same directory
/// by identity and spelling, holding the admitted marker. A store directory
/// replaced after the handoff is the custody row `required-files-changed`.
#[test]
fn the_store_root_is_the_endpoints_store_and_the_project_is_the_active_rows() {
    churned(|| {
        use std::os::unix::fs::MetadataExt;
        let (fixture, _, started) = started("x3d2-store-root");
        let project = started.operation.row().project_id().to_owned();
        let mut session = CommitSession::open(started.operation).unwrap();
        assert_eq!(session.project_id(), project);
        assert!(project.starts_with("prj1-"));
        let path = fixture.installation.join("stores").join(&fixture.store);
        let root = session.store_root().unwrap();
        assert!(root.path().ends_with(format!("stores/{}", fixture.store)));
        let named = fs::metadata(&path).unwrap();
        let spelled = fs::metadata(root.path()).unwrap();
        let held = root.directory().as_file().metadata().unwrap();
        assert_eq!((held.dev(), held.ino()), (named.dev(), named.ino()));
        assert_eq!((spelled.dev(), spelled.ino()), (named.dev(), named.ino()));
        assert_eq!(root.uid(), named.uid());
        drop(root);
        // Replace S with a private directory holding a copy of the marker.
        let moved = fixture.installation.join("stores").join("moved");
        fs::rename(&path, &moved).unwrap();
        fs::create_dir(&path).unwrap();
        fs::set_permissions(&path, fs::Permissions::from_mode(0o700)).unwrap();
        private(&path);
        fs::copy(
            moved.join("store-instance.v1"),
            path.join("store-instance.v1"),
        )
        .unwrap();
        let refused = session.store_root().unwrap_err();
        let WorkFailure::Operation(refusal) = refused else {
            panic!("expected the custody row")
        };
        assert_eq!(
            refusal.termination(),
            crate::InstallationTermination::Custody {
                subject: "required-files-changed"
            }
        );
        // The failure latched the attempt ledger: nothing further is charged.
        assert!(matches!(
            session.charge::<(), ()>(|work| work.charge(WorkCost::default())),
            Err(WorkFailure::Budget(
                opensip_platform::WorkBudgetError::Closed
            ))
        ));
        fs::remove_dir_all(&path).unwrap();
        fs::rename(&moved, &path).unwrap();
        let end = session.refused().finish();
        assert!(!end.end_step_entered());
    });
}

// ------------------------- law X4 r8 S11.6 (unit X4-F3): D8-1's schedules

/// The `REV` reason of the one end-path record `finish` appended.
fn one_rev(fixture: &ReadFixture, n: &str, reason: &str) {
    let records = records(fixture, n);
    assert_eq!(records.len(), 1, "{records:?}");
    assert_eq!(records[0].0, "REV");
    assert!(
        records[0].2.contains(&format!(r#""reason":"{reason}""#)),
        "{records:?}"
    );
}

#[test]
fn a_certain_refusal_then_an_observer_tick_keeps_operation_stopped() {
    // W-8 (a), D8-1's first schedule: a certain refusal with a settlement
    // reserve, then an observer tick, a signal after the closing return,
    // and `finish`. The late cancellation is OutsideWindow.
    churned(|| {
        let (fixture, n, started) = started("x4f3-w8a");
        let watch = started.operation.guard().watch();
        let cancellation = started.operation.guard().cancellation_handle();
        let session = CommitSession::open(started.operation)
            .unwrap()
            .reserve_end_path()
            .unwrap();
        let stopped = session.refused();
        assert_eq!(watch.cause(), Some(StopCause::CertainRefusal));
        assert_eq!(watch.state(), AttemptState::LatchedBeforeAdmission);
        // The tick's read finds the latch and reads the recorded cause: it
        // records nothing, and the observer stops.
        assert!(!watch.tick());
        assert_eq!(watch.cause(), Some(StopCause::CertainRefusal));
        assert_eq!(
            cancellation.cancel(crate::D9Signal::Sigint),
            crate::LatchOutcome::OutsideWindow
        );
        let end = stopped.finish();
        assert!(end.revocation_appended() && !end.cleanup_appended());
        one_rev(&fixture, &n, "operation-stopped");
    });
}

#[test]
fn a_stale_guard_held_after_its_section_keeps_its_row_and_stale_guard() {
    // W-8 (b), D8-1's second schedule: a stale guard before admission, held
    // after its stop transition's release (a seam outside the critical
    // section), then a cancellation, an observer tick and checkpoint return.
    // The cancellation is AlreadyStopped and records nothing.
    churned(|| {
        let (fixture, n, started) = started("x4f3-w8b");
        let watch = started.operation.guard().watch();
        let cancellation = started.operation.guard().cancellation_handle();
        cancellation.open_window();
        let seen = std::sync::Arc::new(std::sync::Mutex::new(None));
        {
            let seen = std::sync::Arc::clone(&seen);
            let tick = started.operation.guard().watch();
            watch.after_stop(move || {
                assert_eq!(
                    cancellation.cancel(crate::D9Signal::Sigterm),
                    crate::LatchOutcome::AlreadyStopped
                );
                let ticked = tick.tick();
                *seen.lock().unwrap() = Some((ticked, tick.cause()));
            });
        }
        let adapter = adapter(&started, Stage::Staged, true);
        let txn = begin_journal_txn(funded(started.operation)).unwrap();
        // A foreign store endpoint: the store marker replaced, a stale guard at
        // the checkpoint's step 1.
        let marker = fixture
            .installation
            .join(format!("stores/{}/store-instance.v1", fixture.store));
        let next = marker.with_file_name("store-instance.x4f3");
        fs::copy(&marker, &next).unwrap();
        private(&next);
        fs::rename(&next, &marker).unwrap();
        let (outcome, stopped) = seal_under_append_lock(txn, &fixtures::replay(), adapter);
        let changed = T::Custody {
            subject: "required-files-changed",
        };
        let stale = StopCause::Stale(OperationRow::Installation(changed.clone()));
        // The tick ran after the stale guard's section and before the
        // checkpoint returned: it read the stale guard and recorded nothing.
        assert_eq!(*seen.lock().unwrap(), Some((false, Some(stale.clone()))));
        match outcome {
            SealOutcome::Refused(SealRefusal::Session(refusal)) => {
                assert_eq!(refusal.termination(), changed)
            }
            other => panic!("{other:?}"),
        }
        assert_eq!(watch.cause(), Some(stale));
        let end = stopped.finish();
        assert!(end.revocation_appended() && !end.cleanup_appended());
        one_rev(&fixture, &n, "stale-guard");
    });
}

#[test]
fn an_observer_revocation_then_a_certain_refusal_keeps_trust_revoked() {
    // W-8 (d): an observer revocation, then a certain refusal, through
    // `refused()` and through `publish`, whose checkpoint reports the
    // revocation's row before its refusal arm stops the operation. The
    // signal between them is AlreadyStopped and records nothing.
    churned(|| {
        for through_publish in [false, true] {
            let tag = if through_publish {
                "x4f3-w8d-publish"
            } else {
                "x4f3-w8d"
            };
            let (fixture, n, started) = started(tag);
            let watch = started.operation.guard().watch();
            let cancellation = started.operation.guard().cancellation_handle();
            cancellation.open_window();
            let closure = started.operation.selected_core().0.to_owned();
            fixture.swap_trust(vec![("release", closure)], 2);
            assert!(!watch.tick());
            let revoked = StopCause::Revoked {
                subject: "trust-revoked",
            };
            assert_eq!(watch.cause(), Some(revoked.clone()));
            assert_eq!(
                cancellation.cancel(crate::D9Signal::Sighup),
                crate::LatchOutcome::AlreadyStopped
            );
            let stopped = if through_publish {
                let (outcome, stopped) = publish(started, Stage::Staged, true);
                match outcome {
                    SealOutcome::Refused(SealRefusal::Session(refusal)) => assert_eq!(
                        refusal.termination(),
                        T::RevokedDuringOperation {
                            subject: "trust-revoked"
                        }
                    ),
                    other => panic!("{other:?}"),
                }
                stopped
            } else {
                funded(started.operation).refused()
            };
            assert_eq!(watch.cause(), Some(revoked));
            assert_eq!(watch.state(), AttemptState::LatchedBeforeAdmission);
            let end = stopped.finish();
            assert!(end.revocation_appended() && !end.cleanup_appended());
            one_rev(&fixture, &n, "trust-revoked");
        }
    });
}

// X3d r9 S10 / J-C15: security-side window controls, scratch installation only.
#[test]
fn cancellation_token_is_minted_once_and_closed_session_cannot_be_stopped_again() {
    churned(|| {
        let (fixture, n, started) = started("j3b-one-token");
        let mut session = CommitSession::open(started.operation).unwrap();
        let token = session.take_cancellation_latch().unwrap();
        assert!(session.take_cancellation_latch().is_none());
        let stopped = session.refused();
        assert!(!stopped.admitted_at_close());
        assert_eq!(
            token.latch(crate::D9Signal::Sigint),
            crate::LatchOutcome::OutsideWindow
        );
        let end = stopped.finish();
        assert!(!end.revocation_appended());
        assert!(records(&fixture, &n).is_empty());
        assert!(fence_free(&fixture) && unlocked(&fixture, &n));
    });
}
#[test]
fn cancellation_outside_never_opened_window_consumes_no_stop_authority() {
    churned(|| {
        let (fixture, n, started) = started("j3b-outside-window");
        let mut session = CommitSession::open(started.operation).unwrap();
        let token = session.take_cancellation_latch().unwrap();
        assert_eq!(
            token.latch(crate::D9Signal::Sighup),
            crate::LatchOutcome::OutsideWindow
        );
        assert!(session.take_cancellation_latch().is_none());
        let stopped = session.refused();
        assert!(!stopped.admitted_at_close());
        assert!(!stopped.finish().revocation_appended());
        assert!(records(&fixture, &n).is_empty());
    });
}
struct OperatorAdapter {
    token: crate::CancellationLatch,
    after_admission: bool,
    committed: bool,
}
struct OperatorStaged {
    token: Option<crate::CancellationLatch>,
    committed: bool,
}
impl CommitAdapter for OperatorAdapter {
    type Staged = OperatorStaged;
    type Refusal = &'static str;
    fn stage(
        self,
        _: &crate::JournalSealBinding,
        work: &mut WorkScope<'_>,
    ) -> Result<OperatorStaged, WorkFailure<&'static str>> {
        work.run(WorkCost::default(), |_| {
            let token = if self.after_admission {
                Some(self.token)
            } else {
                assert_eq!(
                    self.token.latch(crate::D9Signal::Sigterm),
                    crate::LatchOutcome::BeforeAdmission
                );
                None
            };
            Ok(OperatorStaged {
                token,
                committed: self.committed,
            })
        })
    }
}
impl StagedCommit for OperatorStaged {
    type Committed = &'static str;
    fn commit(self) -> EvidenceCommit<&'static str> {
        if let Some(token) = self.token {
            assert_eq!(
                token.latch(crate::D9Signal::Sigterm),
                crate::LatchOutcome::AfterAdmission
            );
        }
        if self.committed {
            EvidenceCommit::Committed("operator-test-receipt")
        } else {
            EvidenceCommit::Undetermined
        }
    }
}
#[test]
fn operator_latch_before_admission_keeps_operator_row_and_funds_rev_cln() {
    churned(|| {
        let (fixture, n, started) = started("j3b-before-admission");
        let mut session = funded(started.operation);
        let token = session.take_cancellation_latch().unwrap();
        session
            .charge_attempt(|_, open| {
                open();
                Ok::<_, WorkFailure<()>>(())
            })
            .unwrap();
        let txn = begin_journal_txn(session).unwrap();
        let (outcome, stopped) = seal_under_append_lock(
            txn,
            &fixtures::replay(),
            OperatorAdapter {
                token,
                after_admission: false,
                committed: true,
            },
        );
        let SealOutcome::Refused(SealRefusal::Session(refusal)) = outcome else {
            panic!("operator refusal")
        };
        assert_eq!(
            refusal.termination(),
            T::Interrupted {
                signal: crate::D9Signal::Sigterm
            }
        );
        assert!(!stopped.admitted_at_close());
        let end = stopped.finish();
        assert!(end.revocation_appended() && end.cleanup_appended());
        assert_eq!(kinds(&fixture, &n), ["SEAL", "REV", "CLN"]);
        assert!(
            records(&fixture, &n)
                .iter()
                .any(|(kind, _, body)| kind == "REV" && body.contains("\"reason\":\"operator\""))
        );
        assert!(fence_free(&fixture) && unlocked(&fixture, &n));
    });
}
#[test]
fn operator_latch_after_admission_preserves_committed_and_undetermined_outcomes() {
    for committed in [true, false] {
        churned(|| {
            let (fixture, n, started) = started(if committed {
                "j3b-after-committed"
            } else {
                "j3b-after-undetermined"
            });
            let mut session = funded(started.operation);
            let token = session.take_cancellation_latch().unwrap();
            session
                .charge_attempt(|_, open| {
                    open();
                    Ok::<_, WorkFailure<()>>(())
                })
                .unwrap();
            let txn = begin_journal_txn(session).unwrap();
            let (outcome, stopped) = seal_under_append_lock(
                txn,
                &fixtures::replay(),
                OperatorAdapter {
                    token,
                    after_admission: true,
                    committed,
                },
            );
            assert!(stopped.admitted_at_close());
            match outcome {
                SealOutcome::Committed {
                    latched_after_admission,
                    committed: receipt,
                    ..
                } => {
                    assert!(committed && latched_after_admission);
                    assert_eq!(receipt, "operator-test-receipt");
                }
                SealOutcome::CommitUndetermined { .. } => assert!(!committed),
                SealOutcome::Refused(_) => panic!("post-admission outcome was relabelled"),
            }
            let end = stopped.finish();
            assert_eq!(end.revocation_appended(), committed);
            assert!(!end.cleanup_appended());
            assert_eq!(
                kinds(&fixture, &n),
                if committed {
                    vec!["SEAL", "REV"]
                } else {
                    vec!["SEAL"]
                }
            );
            assert!(fence_free(&fixture) && unlocked(&fixture, &n));
        });
    }
}

#[test]
fn certain_refusal_inside_the_window_keeps_its_reason_after_a_signal() {
    // W-8(c), with the synchronization at the guard level outside sections.
    churned(|| {
        let (fixture, n, started) = started("j3b-w8c");
        let cancellation = started.operation.guard().cancellation_handle();
        let watch = started.operation.guard().watch();
        let session = funded(started.operation);
        cancellation.open_window();
        let stopped = cancellation.stop(StopCause::CertainRefusal);
        assert!(stopped.first);
        assert_eq!(
            cancellation.cancel(crate::D9Signal::Sigint),
            crate::LatchOutcome::AlreadyStopped
        );
        assert_eq!(watch.cause(), Some(StopCause::CertainRefusal));
        let end = session.refused().finish();
        assert!(end.revocation_appended() && !end.cleanup_appended());
        one_rev(&fixture, &n, "operation-stopped");
    });
}

// J-C15 / W-3: compose both gate total orders with each stopped-session
// return family. Gate controls separately force read/exchange interference.
#[test]
fn closing_returns_keep_their_sample_or_refuse_the_late_signal() {
    #[derive(Clone, Copy, Debug)]
    enum Closing {
        Refused,
        Undetermined,
        ReserveRefused,
        PublishRefused,
        Committed,
        PublishUndetermined,
    }
    for closing in [
        Closing::Refused,
        Closing::Undetermined,
        Closing::ReserveRefused,
        Closing::PublishRefused,
        Closing::Committed,
        Closing::PublishUndetermined,
    ] {
        for signal_first in [true, false] {
            churned(|| {
                let (fixture, n, started) = started("j3b-closing-orders");
                let watch = started.operation.guard().watch();
                let staged = adapter(
                    &started,
                    if matches!(closing, Closing::PublishRefused) {
                        Stage::Io
                    } else {
                        Stage::Staged
                    },
                    !matches!(closing, Closing::PublishUndetermined),
                );
                let mut session = funded(started.operation);
                let mut token = Some(session.take_cancellation_latch().unwrap());
                // Security-side producer: storage's attempt COMMIT itself is
                // exercised by the storage prepared-window control.
                session
                    .charge_attempt(|_, open| {
                        open();
                        Ok::<_, WorkFailure<()>>(())
                    })
                    .unwrap();
                if signal_first {
                    assert_eq!(
                        token.take().unwrap().latch(crate::D9Signal::Sighup),
                        crate::LatchOutcome::BeforeAdmission
                    );
                }
                let stopped = match closing {
                    Closing::Refused => session.refused(),
                    Closing::Undetermined => session.undetermined(),
                    Closing::ReserveRefused => session.reserve_end_path().unwrap_err().1,
                    Closing::PublishRefused | Closing::Committed | Closing::PublishUndetermined => {
                        let txn = begin_journal_txn(session).unwrap();
                        let (outcome, stopped) =
                            seal_under_append_lock(txn, &fixtures::replay(), staged);
                        if signal_first || matches!(closing, Closing::PublishRefused) {
                            assert!(matches!(outcome, SealOutcome::Refused(_)));
                        } else if matches!(closing, Closing::Committed) {
                            assert!(matches!(
                                outcome,
                                SealOutcome::Committed {
                                    latched_after_admission: false,
                                    ..
                                }
                            ));
                        } else {
                            assert!(matches!(outcome, SealOutcome::CommitUndetermined { .. }));
                        }
                        stopped
                    }
                };
                let admitted = !signal_first
                    && matches!(closing, Closing::Committed | Closing::PublishUndetermined);
                assert_eq!(stopped.admitted_at_close(), admitted, "{closing:?}");
                if signal_first {
                    assert!(matches!(
                        watch.cause(),
                        Some(StopCause::Operator {
                            signal: crate::D9Signal::Sighup
                        })
                    ));
                } else {
                    let prior_cause = watch.cause();
                    assert_eq!(
                        token.take().unwrap().latch(crate::D9Signal::Sighup),
                        crate::LatchOutcome::OutsideWindow,
                        "{closing:?}"
                    );
                    assert_eq!(
                        watch.cause(),
                        prior_cause,
                        "late signal changed cause: {closing:?}"
                    );
                    assert_eq!(stopped.admitted_at_close(), admitted);
                }
                let end = stopped.finish();
                if matches!(closing, Closing::Undetermined)
                    || (!signal_first && matches!(closing, Closing::PublishUndetermined))
                {
                    assert!(!end.revocation_appended() && !end.cleanup_appended());
                }
                assert!(fence_free(&fixture) && unlocked(&fixture, &n));
            });
        }
    }
}
