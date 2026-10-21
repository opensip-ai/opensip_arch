// Law X7 r5 item 10 (units X7a and X7b), host side. Every row of item 3's
// table through injected X3d outcomes; item 6's rollover outcomes and the
// end step's failure through injected `finish` disclosures (X7b; the real
// exhausted carrier through `finish` is security's
// `commit_session_tests.rs`); the delivery phase over a scripted renderer
// and sink; the order of replay, admission and the commit facade over the
// evaluator's synthetic replay corpus (`tests/fixtures/replay-fixtures.current.json`);
// the ephemeral label (DR-G27); and the source pins of items 1, 2, 5 and 8.
// Coordinator controls use ScenarioHome's owned synthetic installation under
// the private TMPDIR. They use real custody, replay and publish; they qualify
// neither a native provider nor native scheduling.
use super::*;
use opensip_identity::{
    IdentityDomain, JsonValue as V, ObjectInput, RegisteredSchemas, parse_json,
};
use std::collections::BTreeMap;
use std::io;
use std::sync::OnceLock;

const RUN: &str = "run3:0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef";
const EXEC: &str = "exec1_0123456789abcdef0123456789abcdef";
const N: &str = "6f1c2a4e-3b5d-4c7e-9f10-1a2b3c4d5e6f";
/// The corpus's lawful case, and its missing-evidence case.
const LAWFUL: &str = "packet-0-original";
const MISSING_BLOB: &str =
    "missing-blob-03cc96a8548e6d391a1b12c3bcf491ab13ef50f355e809819b2a1d7e53117bd0";

fn deliver<C>(commit: &C, latched: bool, phase: &mut impl DeliveryPhase<C>) -> Delivery {
    if latched {
        return Delivery::NotStarted;
    }
    let projected = phase.project(commit);
    let Ok((projection, exit)) = projected else {
        return Delivery::Failed;
    };
    if !matches!(exit, 0 | 1 | 3) {
        return Delivery::Failed;
    }
    let outcome = Outcome::Authoritative {
        run: AuthoritativeRun {
            run_id: "unit-test".into(),
        },
        exit,
    };
    let response = match phase.render(DecidedEnvelope {
        outcome: &outcome,
        projection: Some(&projection),
    }) {
        Ok(response) if matches!(response.exit_code, 0 | 1 | 3) => response,
        Ok(_) | Err(_) => return Delivery::Failed,
    };
    if deliver_required(response, phase.output()).is_err() {
        return Delivery::Failed;
    }
    Delivery::Delivered {
        exit,
        optional: phase.optional(commit).err(),
    }
}

// ---------------------------------------------------------------- helpers

/// An authoritative label for an injected outcome. Only this module's child
/// can write the literal; production has one, in `authoritative_run`.
fn run() -> AuthoritativeRun {
    AuthoritativeRun {
        run_id: RUN.to_owned(),
    }
}
fn spelled(t: &InstallationTerminationV1) -> (String, u8, String, String, Option<String>) {
    (
        t.class.to_string(),
        t.exit,
        t.error_code.to_string(),
        t.fault_cause.to_string(),
        t.detail.as_ref().map(ToString::to_string),
    )
}
fn terminated(outcome: Outcome) -> Termination {
    match outcome {
        Outcome::Terminated(t) => t,
        Outcome::Authoritative { .. } | Outcome::Interrupted { .. } => {
            panic!("expected a termination")
        }
    }
}
fn owned(
    class: &str,
    exit: u8,
    code: &str,
    fault: &str,
    detail: Option<&str>,
) -> (String, u8, String, String, Option<String>) {
    (
        class.into(),
        exit,
        code.into(),
        fault.into(),
        detail.map(Into::into),
    )
}

// ------------------------------------------------------------- the table

/// Item 3: a committed Run whose required delivery succeeded is the one
/// authoritative outcome, with the delivered response's exit; an optional
/// failure is disclosed beside it and changes nothing.
#[test]
fn a_delivered_commit_is_authoritative_with_its_settled_exit() {
    for exit in [0, 1, 3] {
        for optional in [None, Some(OptionalFailed)] {
            let (outcome, disclosed) = project(Concluded::Committed {
                run: run(),
                delivery: Delivery::Delivered { exit, optional },
            });
            let Outcome::Authoritative { run, exit: settled } = outcome else {
                panic!("authoritative")
            };
            assert_eq!(run.authority(), "authoritative");
            assert_eq!(run.run_id(), RUN);
            assert_eq!(settled, exit);
            assert_eq!(disclosed, optional);
        }
    }
}

/// Item 3, F16 and F39: a failed required delivery, and a latch after
/// admission that started no delivery, take the same row. The RunId is
/// retained, and the Run is never relabelled.
#[test]
fn a_failed_or_latched_delivery_keeps_the_run_id_and_exits_4() {
    for delivery in [Delivery::Failed, Delivery::NotStarted] {
        let (outcome, disclosed) = project(Concluded::Committed {
            run: run(),
            delivery,
        });
        assert_eq!(disclosed, None);
        let t = terminated(outcome);
        assert_eq!(
            spelled(&t.row),
            owned(
                "operational-failed",
                4,
                "DELIVERY.REQUIRED_FAILED",
                "delivery-required",
                Some("DELIVERY.RENDERER_FAILED_AFTER_COMMIT"),
            )
        );
        assert_eq!(t.row.subject, None);
        assert_eq!(t.run_id.as_deref(), Some(RUN));
        assert_eq!(t.remedy, Some(REMEDY_RENDERER_FAILED_AFTER_COMMIT));
        assert_eq!(t.namespace, None);
    }
}

/// Item 3 and item 5 (r4), F12 and F40: the durability row discloses the
/// ExecutionId as subject and the namespace beside it, carries no RunId,
/// and names read-only recovery.
#[test]
fn an_undetermined_commit_discloses_the_execution_id_namespace_and_no_run_id() {
    let (outcome, disclosed) = project(Concluded::Undetermined {
        execution_id: EXEC.into(),
        namespace: N.into(),
    });
    assert_eq!(disclosed, None);
    let t = terminated(outcome);
    assert_eq!(
        spelled(&t.row),
        owned(
            "operational-failed",
            4,
            "DURABILITY.COMMIT_FAILED",
            "durability-commit",
            None,
        )
    );
    assert_eq!(t.row.subject.as_deref(), Some(EXEC));
    assert_eq!(t.run_id, None);
    assert_eq!(t.remedy, Some(REMEDY_COMMIT_UNDETERMINED));
    assert_eq!(t.namespace.as_deref(), Some(N));
    assert!(REMEDY_COMMIT_UNDETERMINED.contains("read-only recovery"));
    assert!(REMEDY_COMMIT_UNDETERMINED.contains("executionId"));
}

/// Item 3: a refusal is its row exactly as X3d item 9 fixes it, with no
/// RunId and no remedy of finalization's.
#[test]
fn a_refusal_is_its_own_row_unchanged() {
    for row in [
        Row::Busy,
        Row::HostIo,
        Row::LedgerCorrupt,
        Row::MigrationCorrupt,
        Row::BudgetExhausted,
        Row::Invariant,
        Row::CommitUndetermined,
        Row::RevokedDuringOperation { subject: "core" },
        Row::ObserverFailStop { subject: "trust" },
        Row::Custody {
            subject: "required-files-changed",
        },
        Row::ProjectScopeLimit {
            subject: "pathPrefixes:65537>65536".into(),
        },
    ] {
        let expected = installation_termination(&row);
        let (outcome, disclosed) = project(Concluded::Refused(row));
        assert_eq!(disclosed, None);
        let t = terminated(outcome);
        assert_eq!(t.row, expected);
        assert_eq!(t.run_id, None);
        assert_eq!(t.remedy, None);
        assert_eq!(t.namespace, None);
    }
}

/// Item 3 (r4, F34): an existing attempt is X3d's invariant row, with its
/// ExecutionId as subject, the binding's namespace beside it and the remedy
/// of a later invocation's read-only recovery; no RunId.
#[test]
fn an_existing_attempt_is_the_invariant_row_disclosing_its_execution_id() {
    let (outcome, _) = project(Concluded::ExistingAttempt {
        execution_id: EXEC.into(),
        requested: Box::new(requested()),
    });
    let t = terminated(outcome);
    assert_eq!(t.row.subject.as_deref(), Some(EXEC));
    assert_eq!(
        InstallationTerminationV1 {
            subject: None,
            ..t.row.clone()
        },
        installation_termination(&Row::Invariant)
    );
    assert_eq!(
        spelled(&t.row),
        owned(
            "operational-failed",
            4,
            "SYSTEM.OUTCOME.ILLEGAL_STATE",
            "host-invariant",
            Some("HOST.INVARIANT_VIOLATED"),
        )
    );
    assert_eq!(t.run_id, None);
    assert_eq!(t.remedy, Some(REMEDY_EXISTING_ATTEMPT));
    assert!(REMEDY_EXISTING_ATTEMPT.contains("read-only recovery"));
    assert!(REMEDY_EXISTING_ATTEMPT.contains("requested binding"));
    assert_eq!(t.namespace.as_deref(), Some(N));
    // X6 r3 item 6 (unit X6b): the other three members beside it.
    let disclosed = t.requested.expect("the requested binding is disclosed");
    assert_eq!(disclosed, requested());
    assert_eq!(disclosed.store_generation_digest(), "a".repeat(64));
    assert_eq!(disclosed.journal_carrier_digest(), "b".repeat(64));
    assert_eq!(disclosed.operation_ref(), format!("op-{}", "c".repeat(32)));
}
/// The binding X3d discloses with an existing attempt (X6 r3 item 2).
fn requested() -> RequestedBinding {
    RequestedBinding::checked(
        &"a".repeat(64),
        N,
        &"b".repeat(64),
        &format!("op-{}", "c".repeat(32)),
    )
    .unwrap()
}

/// Item 6a: an exhausted generation is the existing busy row, unchanged,
/// with the namespace as its subject. No code, subject kind or remedy is
/// added.
#[test]
fn an_exhausted_generation_is_the_busy_row_naming_the_namespace() {
    let (outcome, _) = project(Concluded::Exhausted {
        namespace: N.into(),
    });
    let t = terminated(outcome);
    assert_eq!(
        spelled(&t.row),
        owned(
            "operational-failed",
            4,
            "LEDGER.BUSY_TIMEOUT",
            "ledger-busy",
            Some("PROJECT.BUSY"),
        )
    );
    assert_eq!(t.row.subject.as_deref(), Some(N));
    assert_eq!(
        InstallationTerminationV1 {
            subject: None,
            ..t.row
        },
        installation_termination(&Row::Busy)
    );
    assert_eq!(t.run_id, None);
    assert_eq!(t.remedy, None);
    assert_eq!(t.namespace, None);
}

/// Item 3: every X3d outcome a caller can hold joins exactly one attempt.
/// (`Committed` and `CarrierCapacityExhausted` carry values only storage
/// and security build.)
#[test]
fn every_x3d_outcome_joins_one_attempt() {
    assert!(matches!(
        Joined::from(CommitOutcome::CommitUndetermined {
            execution_id: EXEC.into()
        }),
        Joined::Undetermined { execution_id } if execution_id == EXEC
    ));
    assert!(matches!(
        Joined::from(CommitOutcome::Refused(Row::Busy)),
        Joined::Refused(Row::Busy)
    ));
    assert!(matches!(
        Joined::from(NotPrepared::ExistingAttempt {
            execution_id: EXEC.into(),
            requested: Box::new(requested()),
        }),
        Joined::ExistingAttempt { execution_id, requested: binding }
            if execution_id == EXEC && *binding == requested()
    ));
    assert!(matches!(
        Joined::from(NotPrepared::CommitUndetermined {
            execution_id: EXEC.into()
        }),
        Joined::Undetermined { execution_id } if execution_id == EXEC
    ));
    assert!(matches!(
        Joined::from(NotPrepared::Refused(Row::HostIo)),
        Joined::Refused(Row::HostIo)
    ));
}

/// X3d r6 item 9: a failed end-path settlement is disclosed on its own row
/// beside the outcome and never rewrites it.
#[test]
fn an_end_failure_is_disclosed_beside_the_outcome_never_in_it() {
    for settlement in [
        Row::Busy,
        Row::HostIo,
        Row::LedgerCorrupt,
        Row::BudgetExhausted,
        Row::CommitUndetermined,
    ] {
        let delivered = finalization(
            Concluded::Committed {
                run: run(),
                delivery: Delivery::Delivered {
                    exit: 0,
                    optional: None,
                },
            },
            settled(&settlement),
        );
        assert_eq!(
            delivered.outcome,
            Outcome::Authoritative {
                run: run(),
                exit: 0
            }
        );
        assert_eq!(
            delivered.end_failure,
            Some(installation_termination(&settlement))
        );
        let refused = finalization(Concluded::Refused(Row::HostIo), settled(&settlement));
        assert_eq!(
            terminated(refused.outcome).row,
            installation_termination(&Row::HostIo)
        );
        assert_eq!(
            refused.end_failure,
            Some(installation_termination(&settlement))
        );
    }
    let clean = finalization(
        Concluded::Undetermined {
            execution_id: EXEC.into(),
            namespace: N.into(),
        },
        EndDisclosure::default(),
    );
    assert_eq!(clean.end_failure, None);
    assert_eq!(clean.end_step_failure, None);
    assert_eq!(clean.rollover, None);
    assert_eq!(clean.optional_failure, None);
}
fn settled(row: &Row) -> EndDisclosure {
    EndDisclosure {
        settlement: Some(row.clone()),
        ..EndDisclosure::default()
    }
}

// ------------------------------------------- X7b: the capacity rollover

fn exhausted() -> Concluded {
    Concluded::Exhausted {
        namespace: N.into(),
    }
}
fn rolled_over(rollover: RolloverDisclosure) -> EndDisclosure {
    EndDisclosure {
        rollover: Some(rollover),
        ..EndDisclosure::default()
    }
}
/// The attempt's item 6a row, exactly as X7a projects it with no rollover.
fn busy_row() -> Outcome {
    project(exhausted()).0
}

/// Item 6: each rollover outcome security discloses is projected beside the
/// attempt, which stays on item 6a's busy row whatever the rollover did.
/// Rolled, already rolled and skipped carry no row.
#[test]
fn every_rollover_outcome_is_disclosed_beside_the_busy_row() {
    for (disclosed, projected) in [
        (
            RolloverDisclosure::Rolled {
                opened_generation: 2,
            },
            Rollover::Rolled {
                opened_generation: 2,
            },
        ),
        (RolloverDisclosure::AlreadyRolled, Rollover::AlreadyRolled),
        (RolloverDisclosure::Skipped, Rollover::Skipped),
    ] {
        let f = finalization(exhausted(), rolled_over(disclosed));
        assert_eq!(f.outcome, busy_row());
        assert_eq!(f.rollover, Some(projected));
        assert_eq!(f.end_failure, None);
        assert_eq!(f.end_step_failure, None);
        assert_eq!(f.optional_failure, None);
    }
}

/// Item 6's rollover-failure rows: busy at level 3, host I/O, quarantine,
/// an invariant and budget keep their own rows; an uncertain append is
/// `DURABILITY.COMMIT_FAILED`, with no ExecutionId and no remedy of
/// finalization's. None rewrites the attempt's busy row.
#[test]
fn a_rollover_failure_is_its_own_row_and_never_rewrites_the_attempt() {
    let refused = |row: Row| {
        let f = finalization(exhausted(), rolled_over(RolloverDisclosure::Refused(row)));
        assert_eq!(f.outcome, busy_row());
        match f.rollover {
            Some(Rollover::Refused(row)) => spelled(&row),
            other => panic!("{other:?}"),
        }
    };
    assert_eq!(
        refused(Row::Busy),
        owned(
            "operational-failed",
            4,
            "LEDGER.BUSY_TIMEOUT",
            "ledger-busy",
            Some("PROJECT.BUSY"),
        )
    );
    assert_eq!(
        refused(Row::HostIo),
        owned("operational-failed", 4, "HOST.IO_FAILURE", "host-io", None)
    );
    assert_eq!(
        refused(Row::LedgerCorrupt),
        spelled(&installation_termination(&Row::LedgerCorrupt))
    );
    assert_eq!(
        refused(Row::BudgetExhausted),
        owned(
            "operational-failed",
            4,
            "SYSTEM.OUTCOME.ILLEGAL_STATE",
            "host-invariant",
            Some("WORK.BUDGET_EXHAUSTED"),
        )
    );
    assert_eq!(
        refused(Row::Invariant),
        spelled(&installation_termination(&Row::Invariant))
    );
    let f = finalization(exhausted(), rolled_over(RolloverDisclosure::Undetermined));
    assert_eq!(f.outcome, busy_row());
    let Some(Rollover::Undetermined(row)) = f.rollover else {
        panic!("{:?}", f.rollover);
    };
    assert_eq!(
        spelled(&row),
        owned(
            "operational-failed",
            4,
            "DURABILITY.COMMIT_FAILED",
            "durability-commit",
            None,
        )
    );
    assert_eq!(row.subject, None);
    assert_eq!(f.end_step_failure, None);
}

/// X3b r10 item 4 and X3d r6 item 9: an end step that failed after it was
/// entered is disclosed on its own row, beside the outcome and beside any
/// rollover outcome, and rewrites neither. One that stopped before the
/// rollover discloses no rollover.
#[test]
fn an_end_step_failure_is_disclosed_beside_the_outcome_and_the_rollover() {
    let f = finalization(
        exhausted(),
        EndDisclosure {
            end_step: Some(Row::HostIo),
            rollover: Some(RolloverDisclosure::Rolled {
                opened_generation: 2,
            }),
            ..EndDisclosure::default()
        },
    );
    assert_eq!(f.outcome, busy_row());
    assert_eq!(
        f.rollover,
        Some(Rollover::Rolled {
            opened_generation: 2
        })
    );
    assert_eq!(
        f.end_step_failure,
        Some(installation_termination(&Row::HostIo))
    );
    let custody = Row::Custody {
        subject: "required-files-changed",
    };
    let f = finalization(
        exhausted(),
        EndDisclosure {
            end_step: Some(custody.clone()),
            ..EndDisclosure::default()
        },
    );
    assert_eq!(f.outcome, busy_row());
    assert_eq!(f.rollover, None);
    assert_eq!(f.end_step_failure, Some(installation_termination(&custody)));
    // Any other outcome keeps its own row beside an end-step failure.
    let f = finalization(
        Concluded::Refused(Row::Busy),
        EndDisclosure {
            end_step: Some(Row::BudgetExhausted),
            ..EndDisclosure::default()
        },
    );
    assert_eq!(
        terminated(f.outcome).row,
        installation_termination(&Row::Busy)
    );
    assert_eq!(
        f.end_step_failure,
        Some(installation_termination(&Row::BudgetExhausted))
    );
}

// ------------------------------------------------------ the delivery phase

/// A scripted delivery phase over any commit value. It counts every call.
struct Phase {
    rendered: Result<u8, RendererFailed>,
    optional: Result<(), OptionalFailed>,
    sink: Sink,
    renders: usize,
    optionals: usize,
}
#[derive(Default)]
struct Sink {
    bytes: Vec<u8>,
    flushes: usize,
    fail_write: bool,
    fail_flush: bool,
}
impl Write for Sink {
    fn write(&mut self, bytes: &[u8]) -> io::Result<usize> {
        if self.fail_write {
            return Err(io::ErrorKind::BrokenPipe.into());
        }
        self.bytes.extend_from_slice(bytes);
        Ok(bytes.len())
    }
    fn flush(&mut self) -> io::Result<()> {
        self.flushes += 1;
        if self.fail_flush {
            Err(io::ErrorKind::Other.into())
        } else {
            Ok(())
        }
    }
}
impl Phase {
    fn new(rendered: Result<u8, RendererFailed>) -> Self {
        Self {
            rendered,
            optional: Ok(()),
            sink: Sink::default(),
            renders: 0,
            optionals: 0,
        }
    }
}
impl<C> DeliveryPhase<C> for Phase {
    type Projection = u8;
    fn project(&mut self, _: &C) -> Result<(u8, u8), RendererFailed> {
        self.rendered.map(|exit| (exit, exit))
    }
    fn finalize_operational(&mut self, _: &Finalization) {}
    fn render(
        &mut self,
        envelope: DecidedEnvelope<'_, u8>,
    ) -> Result<RenderedResponse, RendererFailed> {
        self.renders += 1;
        self.rendered.map(|_| RenderedResponse {
            bytes: b"committed run\n".to_vec(),
            exit_code: decided_exit(envelope.outcome),
        })
    }
    fn output(&mut self) -> &mut dyn Write {
        &mut self.sink
    }
    fn error_output(&mut self) -> &mut dyn Write {
        &mut self.sink
    }
    fn optional(&mut self, _: &C) -> Result<(), OptionalFailed> {
        self.optionals += 1;
        self.optional
    }
}

/// Item 4, F39: a latch after admission starts no delivery phase: nothing
/// is rendered, written or flushed, and no optional effect runs.
#[test]
fn a_latched_commit_starts_no_delivery_phase() {
    let mut phase = Phase::new(Ok(0));
    assert_eq!(deliver(&(), true, &mut phase), Delivery::NotStarted);
    assert_eq!((phase.renders, phase.optionals), (0, 0));
    assert!(phase.sink.bytes.is_empty());
    assert_eq!(phase.sink.flushes, 0);
}

/// Item 4: the required response is delivered whole and flushed once; its
/// exit is the evaluation class's own, and the optional effects follow.
#[test]
fn a_delivered_response_settles_its_own_exit() {
    for exit in [0, 1, 3] {
        let mut phase = Phase::new(Ok(exit));
        assert_eq!(
            deliver(&(), false, &mut phase),
            Delivery::Delivered {
                exit,
                optional: None
            }
        );
        assert_eq!(phase.sink.bytes, b"committed run\n");
        assert_eq!(phase.sink.flushes, 1);
        assert_eq!((phase.renders, phase.optionals), (1, 1));
    }
}

/// F16: a renderer failure, a response that settles no success exit, a
/// write failure and a flush failure each fail the required step. Nothing
/// is retried and no optional effect runs.
#[test]
fn every_required_failure_is_one_failed_delivery_with_no_retry() {
    let mut renderer = Phase::new(Err(RendererFailed));
    assert_eq!(deliver(&(), false, &mut renderer), Delivery::Failed);
    assert!(renderer.sink.bytes.is_empty());
    assert_eq!((renderer.renders, renderer.optionals), (0, 0));
    for exit in [2, 4, 130] {
        let mut unlawful = Phase::new(Ok(exit));
        assert_eq!(deliver(&(), false, &mut unlawful), Delivery::Failed);
        assert!(unlawful.sink.bytes.is_empty(), "{exit}");
        assert_eq!(unlawful.sink.flushes, 0);
        assert_eq!(unlawful.optionals, 0);
    }
    let mut write = Phase::new(Ok(0));
    write.sink.fail_write = true;
    assert_eq!(deliver(&(), false, &mut write), Delivery::Failed);
    assert_eq!((write.renders, write.optionals), (1, 0));
    assert_eq!(write.sink.flushes, 0);
    let mut flush = Phase::new(Ok(1));
    flush.sink.fail_flush = true;
    assert_eq!(deliver(&(), false, &mut flush), Delivery::Failed);
    assert_eq!(flush.sink.bytes, b"committed run\n");
    assert_eq!(
        (flush.renders, flush.optionals, flush.sink.flushes),
        (1, 0, 1)
    );
}

/// F17: an optional effect that fails after required delivery is disclosed
/// beside it; the delivered exit is unchanged.
#[test]
fn an_optional_failure_never_changes_the_delivered_exit() {
    for exit in [0, 1, 3] {
        let mut phase = Phase::new(Ok(exit));
        phase.optional = Err(OptionalFailed);
        assert_eq!(
            deliver(&(), false, &mut phase),
            Delivery::Delivered {
                exit,
                optional: Some(OptionalFailed)
            }
        );
        assert_eq!(phase.sink.bytes, b"committed run\n");
    }
}

// ------------------------------------------------------------ the order

struct Candidate {
    run_id: String,
    objects: BTreeMap<String, ObjectInput>,
    blobs: BTreeMap<[u8; 32], Vec<u8>>,
}
fn object(v: &V) -> &BTreeMap<String, V> {
    match v {
        V::Object(o) => o,
        _ => panic!("fixture object"),
    }
}
fn array(v: &V) -> &[V] {
    match v {
        V::Array(a) => a,
        _ => panic!("fixture array"),
    }
}
fn string(v: &V) -> &str {
    match v {
        V::String(s) => s,
        _ => panic!("fixture string"),
    }
}
fn bytes(hex: &str) -> Vec<u8> {
    hex.as_bytes()
        .chunks_exact(2)
        .map(|p| u8::from_str_radix(std::str::from_utf8(p).unwrap(), 16).unwrap())
        .collect()
}
/// One labelled case of the evaluator's synthetic replay corpus.
fn candidate(label: &str) -> Candidate {
    let f = parse_json(include_bytes!(
        "../tests/fixtures/replay-fixtures.current.json"
    ))
    .unwrap();
    let f = object(&f);
    let q = array(&f["cases"])
        .iter()
        .map(object)
        .find(|q| string(&q["label"]) == label)
        .unwrap();
    let objects = array(&q["objects"])
        .iter()
        .map(|k| {
            let r = object(&object(&f["objectPool"])[string(k)]);
            (
                string(&r["id"]).to_owned(),
                ObjectInput {
                    domain: IdentityDomain::parse(string(&r["domain"])).unwrap(),
                    descriptor: r["descriptor"].clone(),
                },
            )
        })
        .collect();
    let blobs = array(&q["blobs"])
        .iter()
        .map(|k| {
            let r = object(&object(&f["blobPool"])[string(k)]);
            (
                bytes(string(&r["digest"])).try_into().unwrap(),
                bytes(string(&r["hex"])),
            )
        })
        .collect();
    Candidate {
        run_id: string(&q["runId"]).to_owned(),
        objects,
        blobs,
    }
}
fn registry() -> &'static RegisteredSchemas {
    static REGISTRY: OnceLock<RegisteredSchemas> = OnceLock::new();
    REGISTRY.get_or_init(|| crate::embedded_schema_registry().unwrap())
}
#[derive(Default)]
struct TestPort {
    first: Option<D9Signal>,
    decisions: usize,
    armed: usize,
    returns: Vec<(bool, bool)>,
    settled: usize,
}
impl CancellationPort for TestPort {
    fn observed(&mut self) -> Option<D9Signal> {
        self.first
    }
    fn arm(&mut self, token: CancellationLatch) {
        self.armed += 1;
        if let Some(signal) = self.first {
            let _ = token.latch(signal);
        }
    }
    fn returned(&mut self, admitted: bool, enters_delivery: bool) {
        self.returns.push((admitted, enters_delivery));
    }
    fn decide_output(&mut self) -> Option<D9Signal> {
        self.decisions += 1;
        self.first
    }
    fn settled(&mut self) {
        self.settled += 1;
    }
}
#[test]
fn replay_refusal_after_r12_finishes_once_and_outputs_its_own_row() {
    let c = candidate(MISSING_BLOB);
    let inputs = RunCandidateInputs {
        registry: registry(),
        objects: &c.objects,
        blobs: &c.blobs,
        run_id: &c.run_id,
    };
    let home = opensip_security::scenario::ScenarioHome::create(&std::env::temp_dir());
    let root = home.project("j3b-replay-refusal");
    let operation = home.operation(&root).unwrap();
    let mut phase = Phase::new(Ok(0));
    let mut port = TestPort::default();
    let opened = match open_finalization(operation, &mut phase, &mut port) {
        Ok(opened) => opened,
        Err(_) => panic!("session open"),
    };
    let namespace = opened.fixture(|session| session.namespace_id().to_owned());
    let finalized = finalize(opened, &inputs, &mut phase, &mut port);
    assert_eq!(
        terminated(finalized.outcome)
            .row
            .detail
            .map(|d| d.to_string()),
        Some("evidence.missing".to_owned())
    );
    assert_eq!((port.armed, port.decisions, port.settled), (0, 1, 1));
    let census = home.carrier_census(&namespace).unwrap();
    assert_eq!((census.seal, census.rev, census.cln), (0, 0, 0));
    assert!(port.returns.is_empty());
    assert_eq!(phase.optionals, 0);
    assert_eq!(phase.sink.flushes, 1);
    // The released lease permits the next operation; no attempt row was written.
    let operation = home.operation(&root).unwrap();
    let opened = match open_finalization(operation, &mut phase, &mut port) {
        Ok(opened) => opened,
        Err(_) => panic!("session reopen"),
    };
    let ended = end_before_commit(opened, Row::Busy, &mut phase, &mut port);
    assert_eq!(
        terminated(ended.outcome).row,
        installation_termination(&Row::Busy)
    );
    assert_eq!((port.decisions, port.settled), (2, 2));
}

/// Item 2 (DR-G27): an ephemeral analysis is labelled `ephemeral` and never
/// carries a RunId.
#[test]
fn an_ephemeral_analysis_is_never_authoritative_and_has_no_run_id() {
    let ephemeral = EphemeralRun {
        proof_bundle_id: "proof-bundle".into(),
    };
    assert_eq!(ephemeral.authority(), "ephemeral");
    assert_eq!(ephemeral.run_id(), None);
    assert_eq!(ephemeral.proof_bundle_id(), "proof-bundle");
    assert_ne!(ephemeral.authority(), run().authority());
}

// -------------------------------------------------------------- the pins

fn code_only(source: &str) -> String {
    source
        .lines()
        .filter(|line| !line.trim_start().starts_with("//"))
        .collect::<Vec<_>>()
        .join("\n")
}
fn production_source() -> String {
    let text = include_str!("finalization.rs");
    code_only(text.split("#[cfg(test)]\nmod tests").next().unwrap())
}
/// Every host production source but this module's own tests, by file name.
fn host_production_sources() -> Vec<(String, String)> {
    let root = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("src");
    let mut out = Vec::new();
    let mut stack = vec![root];
    while let Some(dir) = stack.pop() {
        for entry in std::fs::read_dir(&dir).unwrap() {
            let path = entry.unwrap().path();
            let name = path.file_name().unwrap().to_string_lossy().into_owned();
            if path.is_dir() {
                stack.push(path);
            } else if name.ends_with(".rs") && !name.ends_with("_tests.rs") && name != "tests.rs" {
                let text = std::fs::read_to_string(&path).unwrap();
                let text = text.split("#[cfg(test)]\nmod tests").next().unwrap();
                out.push((name, code_only(text)));
            }
        }
    }
    out
}

/// Item 1: finalization is the one commit coordinator. No other host
/// production module calls the replay join or the commit facade.
#[test]
fn no_other_host_module_coordinates_a_commit() {
    let sources = host_production_sources();
    assert!(sources.iter().any(|(name, _)| name == "finalization.rs"));
    for needle in [
        "replay_candidate(",
        "CommitSession::open(",
        "take_cancellation_latch(",
        ".refused()",
        ".undetermined()",
        "prepare_commit(",
        ".publish()",
        ".finish()",
        "authoritative_run(",
    ] {
        for (name, text) in &sources {
            let calls = text
                .match_indices(needle)
                .filter(|&(at, _)| !text[..at].ends_with("fn "))
                .count();
            if name != "finalization.rs" {
                assert_eq!(calls, 0, "{name} calls {needle}");
            }
        }
    }
}

/// S9.1/P1-P4: the opening entry alone creates a session, replay follows
/// the already-open session, and only P3 transfers the token to the port.
#[test]
fn finalize_uses_opened_session_then_replay_prepare_publish_finish_projection() {
    let source = production_source();
    let open = &source[source.find("pub(crate) fn open_finalization<").unwrap()
        ..source.find("pub(crate) fn end_before_commit<").unwrap()];
    assert_eq!(open.matches("CommitSession::open(").count(), 1);
    assert_eq!(open.matches("take_cancellation_latch()").count(), 1);
    let body = &source[source.find("pub(crate) fn finalize<").unwrap()
        ..source.find("fn output_finalization<").unwrap()];
    assert!(!body.contains("admit()"));
    assert!(!body.contains("CommitSession::open("));
    let order = [
        "replay_candidate(candidate, REPLAY_LIMITS)",
        "port.observed()",
        "prepare_commit(replayed, session)",
        "port.arm(token)",
        "prepared.publish()",
        "stopped.admitted_at_close()",
        "let end = stopped.finish();",
        "phase.project(&commit)",
    ];
    let mut last = 0;
    for needle in order {
        let at = body.rfind(needle).unwrap_or_else(|| panic!("{needle}"));
        assert!(at >= last, "{needle}");
        last = at;
    }
    let output = &source[source.find("fn output_decision<").unwrap()
        ..source.find("fn required_output_failure(").unwrap()];
    assert_eq!(output.matches("port.decide_output()").count(), 1);
    assert!(
        output.find("port.decide_output()").unwrap()
            < output.find("phase.finalize_operational(").unwrap()
    );
    assert!(
        output.find("phase.finalize_operational(").unwrap() < output.find("emit_decided(").unwrap()
    );
}

/// Items 4 to 8 and the forbidden substitutes: no recovery of its own
/// outcome, no read session or receipt (the delivery read's authority is X7
/// r4's), no admission, gate, fence or ledger of its own, no lifecycle, no
/// retry, and no wildcard arm.
#[test]
fn finalization_owns_no_recovery_admission_ledger_or_wildcard() {
    let source = production_source();
    for forbidden in [
        "recover(",
        "recovery::",
        "ReadReceipt",
        "read_receipt",
        "ReadSession",
        "SharedRead",
        "installation_read",
        "admit_ordinary_writer",
        "DurableWriteGate",
        "WorkLedger",
        "WorkScope",
        ".charge(",
        "settle(",
        "opensip_lifecycle",
        "fence",
        "loop {",
        "retry(",
        "_ =>",
        "unwrap(",
        "expect(",
    ] {
        assert!(!source.contains(forbidden), "{forbidden}");
    }
}

/// Item 4 (r4) and item 10's pin: the delivery phase reads nothing from
/// the store. `finalization.rs` names no 458c read entry, receipt or read
/// session, no X2 lease, and no storage reader: its only security and
/// storage names are the commit facade's (and the inert requested binding
/// it discloses), in two exact `use` lines.
#[test]
fn finalization_reaches_no_read_entry_lease_or_storage_reader() {
    let source = production_source();
    // X6b adds the inert `RequestedBinding` value it discloses (X6 r3 item 6).
    assert!(source.contains(
        "use opensip_security::{\n    CancellationLatch, CommitSession, D9Signal, InstallationTermination as Row, ProjectOperation,\n    RequestedBinding, RolloverDisclosure, SessionEnd,\n};"
    ));
    assert!(source.contains(
        "use opensip_storage::{CommitOutcome, NotPrepared, PublishedCommit, prepare_commit};"
    ));
    assert_eq!(source.matches("opensip_security").count(), 1);
    assert_eq!(source.matches("opensip_storage").count(), 1);
    for forbidden in [
        "Lease",
        "_lease",
        "lease::",
        "read_entry",
        "ReadEntry",
        "ReadReceipt",
        "read_receipt",
        "ReadSession",
        "read_session",
        "SharedRead",
        "installation_read",
        "doctor_report",
        "join_ledger",
        "RecoveredCommit",
        "open_store",
        "store_root",
        "std::fs",
        "File::",
    ] {
        assert!(!source.contains(forbidden), "{forbidden}");
    }
}

/// Item 2 (DR-G27): the one authoritative label is written in exactly one
/// place, `authoritative_run`, which takes `&PublishedCommit` and nothing
/// else; no other function returns one, and the ephemeral projection takes
/// only the evaluator's non-authoritative result.
#[test]
fn only_a_published_commit_writes_the_authoritative_label() {
    let source = production_source();
    assert_eq!(source.matches("-> AuthoritativeRun").count(), 1);
    assert!(
        source.contains(
            "pub fn authoritative_run(commit: &PublishedCommit) -> AuthoritativeRun {\n    AuthoritativeRun {\n        run_id: commit.run_id().to_owned(),\n    }\n}"
        )
    );
    let literals = source
        .lines()
        .filter(|line| line.trim() == "AuthoritativeRun {")
        .count();
    assert_eq!(literals, 1);
    assert_eq!(source.matches("\"authoritative\"").count(), 1);
    assert_eq!(source.matches("\"ephemeral\"").count(), 1);
    assert!(
        source.contains(
            "pub(crate) fn ephemeral_run(result: &EvaluationCandidate) -> EphemeralRun {"
        )
    );
    assert_eq!(source.matches("-> EphemeralRun").count(), 1);
    // No conversion between the labels, and no authority parameter.
    for forbidden in [
        "From<EphemeralRun>",
        "From<bool>",
        "authority: bool",
        "authoritative: bool",
        "impl Clone for AuthoritativeRun",
        "impl Default for AuthoritativeRun",
    ] {
        assert!(!source.contains(forbidden), "{forbidden}");
    }
    // The type derives nothing that copies, defaults or serializes it.
    let derive = source
        .lines()
        .take_while(|line| !line.contains("pub struct AuthoritativeRun"))
        .last()
        .unwrap();
    assert_eq!(derive.trim(), "#[derive(Debug, PartialEq, Eq)]");
}

/// X9 r1 item 5: X7a places its own `x7.delivery` points, `required` and
/// `optional`, each fallible.
#[test]
fn the_delivery_points_are_placed() {
    let source = production_source();
    for step in ["required", "optional"] {
        assert!(source.contains(&format!("\"{step}\"")), "{step}");
    }
    assert!(source.contains("emit_decided(&result.outcome, projection, phase)"));
    assert!(source.contains("phase.optional(commit)"));
    assert_eq!(source.matches("crash_barrier!(").count(), 2);
}

/// Item 6 (X7b): finalization runs no rollover. It reads the end path only
/// through `SessionEnd`'s three accessors, once each, in one place, and
/// names no rollover operation, end step, carrier record or lease.
#[test]
fn finalization_reads_the_rollover_only_through_session_end() {
    let source = production_source();
    let from = &source[source
        .find("impl From<SessionEnd> for EndDisclosure")
        .unwrap()..];
    let from = &from[..from.find("\n}\n").unwrap()];
    for accessor in [
        "end.settlement_failure()",
        "end.end_step_failure()",
        "end.rollover()",
    ] {
        assert_eq!(source.matches(accessor).count(), 1, "{accessor}");
        assert!(from.contains(accessor), "{accessor}");
    }
    assert_eq!(source.matches("rollover(").count(), 1);
    assert_eq!(source.matches("end_step_failure(").count(), 1);
    for forbidden in [
        "end_step_after_exhaustion",
        "RolloverOutcome",
        "OperationEnd",
        "EndFailure",
        "TERMINAL",
        "EXCLUSIVE",
        "Exclusive",
        "grant_generation",
    ] {
        assert!(!source.contains(forbidden), "{forbidden}");
    }
}
