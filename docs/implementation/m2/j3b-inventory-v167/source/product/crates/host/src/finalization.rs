//! Law X7 r5 (units X7a and X7b): host finalization, the one application
//! coordinator of a durable analysis (item 1). Read under the laws X3b r10,
//! X3d r6, X5 r3, X6 r3, X8 r3, X9 r1 and X12 r3.
//!
//! J3b follows X3d r9, X4 r8, X5 r4 and X7 r7's S9. The caller
//! obtains its one ProjectOperation at R12, then `open_finalization` opens
//! the session and keeps P1's one-use token. Analysis can end that session
//! through `end_before_commit`; a candidate goes through `finalize`:
//! 1. replay the candidate against REPLAY_LIMITS under existing custody;
//! 2. check P2, prepare, and transfer the token only at successful P3;
//! 3. publish, sample the close at P4, and finish on every return;
//! 4. project an unlatched committed Run after the writer lease is released;
//! 5. decide once at P5, run the operational hook, render, output and flush;
//! 6. settle at P6, then run optional effects only after success output.
//!
//! Finalization admits no pack and wires no Plan join into replay.
//!
//! Then it projects exactly one outcome (items 3 and 8) through exhaustive
//! matches with no wildcard arm. Only [`authoritative_run`], which takes
//! `&PublishedCommit` and nothing else, writes the authoritative label and
//! the RunId (item 2, DR-G27). An explicit ephemeral analysis has its own
//! projection, which can only write `ephemeral` and no RunId.
//!
//! Finalization charges no ledger itself (item 7), never calls recovery for
//! its own `CommitUndetermined` (item 5) or `ExistingAttempt` (item 3), never retries a commit, and takes
//! no admission, gate or fence of its own.
//!
//! The capacity rollover route (item 6, unit X7b). A
//! `CarrierCapacityExhausted` attempt is finished like any other: X3d's
//! `finish` carries the exhaustion into X3b's end step, which runs the
//! rollover under the fence it already holds, on this invocation's one
//! admission and attempt ledger (X3b r10 item 13). Finalization runs no
//! rollover. It projects the attempt on item 6a's busy row, and discloses
//! beside it, through `SessionEnd`'s accessors, the rollover's outcome
//! (rolled, already rolled, skipped, or a refusal or an uncertain append on
//! its own row) and any end-step failure. Neither rewrites the attempt's
//! row. Library only: no CLI command is wired.
use crate::fact_admission::{
    REPLAY_LIMITS, RunCandidateInputs, replay_candidate, replay_remedy, replay_termination,
};
use crate::{
    InstallationTerminationV1, RenderedResponse, deliver_required, installation_termination,
};
use opensip_contracts::generated::evidence::{
    Common4D9Class as Class, Common4D9ErrorCode as Code, Common4D9FaultCause as Fault,
    Common4DomainDetailCode as Detail,
};
use opensip_evaluator::EvaluationCandidate;
use opensip_security::{
    CancellationLatch, CommitSession, D9Signal, InstallationTermination as Row, ProjectOperation,
    RequestedBinding, RolloverDisclosure, SessionEnd,
};
use opensip_storage::{CommitOutcome, NotPrepared, PublishedCommit, prepare_commit};
use std::io::Write;
pub(crate) mod cancellation;

/// The after-commit required-delivery remedy, as the workflow projection's
/// reference model words it for `DELIVERY.RENDERER_FAILED_AFTER_COMMIT`.
pub(crate) const REMEDY_RENDERER_FAILED_AFTER_COMMIT: &str =
    "the Run is committed; rerun the renderer with this runId";
/// Item 5: an undetermined commit is settled by a later invocation's
/// read-only recovery of this ExecutionId (X6), never by a retry.
pub(crate) const REMEDY_COMMIT_UNDETERMINED: &str = "The commit's outcome is undetermined. Run OpenSIP's read-only recovery for this executionId in a later invocation; do not retry the attempt.";
/// Item 3 (r4): an existing attempt is recovered only by a later
/// invocation's read-only recovery with the disclosed binding (X6 r3 item
/// 6), never in this invocation and never by a retry.
pub(crate) const REMEDY_EXISTING_ATTEMPT: &str = "An attempt with this executionId already exists. Run OpenSIP's read-only recovery for this executionId and its requested binding in a later invocation; do not retry the attempt.";

// ------------------------------------------------------------- the labels

/// Item 2: the authoritative label of a committed Run. Private fields; not
/// Clone, Default or serializable; [`authoritative_run`] is its only
/// constructor.
#[derive(Debug, PartialEq, Eq)]
pub struct AuthoritativeRun {
    run_id: String,
}
impl AuthoritativeRun {
    /// `run.authority`: always `"authoritative"`.
    pub fn authority(&self) -> &'static str {
        "authoritative"
    }
    /// `run.runId`: the committed Run's identity.
    pub fn run_id(&self) -> &str {
        &self.run_id
    }
}

/// Item 2 (DR-G27): the one projection that writes `run.authority =
/// "authoritative"` and `run.runId`. It takes `&PublishedCommit`, which only
/// storage's commit path builds after a successful evidence `COMMIT`, and
/// nothing else. Exported so that its signature is pinned from outside the
/// crate (X8 r3 item 3c); it is inert.
pub fn authoritative_run(commit: &PublishedCommit) -> AuthoritativeRun {
    AuthoritativeRun {
        run_id: commit.run_id().to_owned(),
    }
}

/// Item 2: the label of an explicit ephemeral analysis. It carries no RunId
/// and can never be authoritative.
#[derive(Debug, PartialEq, Eq)]
pub(crate) struct EphemeralRun {
    proof_bundle_id: String,
}
impl EphemeralRun {
    /// `run.authority`: always `"ephemeral"`.
    pub(crate) fn authority(&self) -> &'static str {
        "ephemeral"
    }
    /// An ephemeral analysis has no Run (build plan line 161).
    pub(crate) fn run_id(&self) -> Option<&str> {
        None
    }
    /// The derived proof's identity, which a result may cite.
    pub(crate) fn proof_bundle_id(&self) -> &str {
        &self.proof_bundle_id
    }
}

/// Item 2: the separate projection of the evaluator's non-authoritative
/// result. It can only write `ephemeral`, with no RunId.
pub(crate) fn ephemeral_run(result: &EvaluationCandidate) -> EphemeralRun {
    EphemeralRun {
        proof_bundle_id: result.proof_bundle_id().to_owned(),
    }
}

// ---------------------------------------------------------- the outcome

/// One failure termination: the public row, the committed RunId it retains
/// (required delivery after commit only), the remedy finalization owns for
/// it, where it owns one, and the namespace disclosed beside it, where a
/// later recovery needs it as its selector (items 3 and 5, r4). For an
/// `ExistingAttempt` the whole requested binding is disclosed too (X6 r3
/// item 6, unit X6b): the store generation digest, the namespace, the
/// carrier digest and the operation reference a later recovery compares.
#[derive(Debug, PartialEq, Eq)]
pub(crate) struct Termination {
    pub(crate) row: InstallationTerminationV1,
    pub(crate) run_id: Option<String>,
    pub(crate) remedy: Option<&'static str>,
    pub(crate) namespace: Option<String>,
    pub(crate) requested: Option<RequestedBinding>,
}

/// Item 8: exactly one envelope per invocation.
#[derive(Debug, PartialEq, Eq)]
pub(crate) enum Outcome {
    /// Required delivery succeeded: the authoritative Run, and the exit the
    /// delivered response settled (0, or the evaluation class's 1 or 3).
    Authoritative { run: AuthoritativeRun, exit: u8 },
    /// Every other end, on its one row.
    Terminated(Termination),
    Interrupted {
        signal: D9Signal,
        run: Option<AuthoritativeRun>,
    },
}

/// What one invocation of `finalize` returns. The disclosures never rewrite
/// the outcome.
#[derive(Debug, PartialEq, Eq)]
pub(crate) struct Finalization {
    pub(crate) outcome: Outcome,
    /// A failed end-path settlement (X3d r6 item 9), on its own existing
    /// row.
    pub(crate) end_failure: Option<InstallationTerminationV1>,
    /// X3b's end step failed after it was entered (X3b r10 item 4), on its
    /// own existing row. An end step not entered is not disclosed (X3d r6
    /// item 9).
    pub(crate) end_step_failure: Option<InstallationTerminationV1>,
    /// Item 6 (X7b): the capacity rollover's outcome, where the end step
    /// ran one; `None` where none was attempted.
    pub(crate) rollover: Option<Rollover>,
    /// An optional effect that failed after required delivery succeeded
    /// (F17), disclosed on its own surface.
    pub(crate) optional_failure: Option<OptionalFailed>,
}

/// Item 6 (unit X7b): what the capacity rollover in `finish`'s end step did
/// (X3b r10 item 13), disclosed beside the attempt's item 6a busy row, which
/// it never rewrites.
#[derive(Debug, PartialEq, Eq)]
pub(crate) enum Rollover {
    /// The generation was closed and this one opened; the busy row's retry
    /// proceeds there (item 6a).
    Rolled { opened_generation: i64 },
    /// The generation was already closed; nothing was written.
    AlreadyRolled,
    /// Another operation held the namespace; nothing was written, and the
    /// next writer that reaches the exhaustion takes the route.
    Skipped,
    /// A certain refusal, on its own row: busy, host I/O, quarantine, an
    /// invariant or budget. The generation stays at capacity.
    Refused(InstallationTerminationV1),
    /// An uncertain append, on `DURABILITY.COMMIT_FAILED`; the next writer's
    /// start reconciles it.
    Undetermined(InstallationTerminationV1),
}

/// What `finish` disclosed, as values: the settlement's failure (X3d r6
/// item 9), the end step's (X3b r10 item 4) and the rollover's outcome
/// (item 6). None of it rewrites the outcome.
#[derive(Debug, Default)]
struct EndDisclosure {
    settlement: Option<Row>,
    end_step: Option<Row>,
    rollover: Option<RolloverDisclosure>,
}
impl From<SessionEnd> for EndDisclosure {
    fn from(end: SessionEnd) -> Self {
        Self {
            settlement: end.settlement_failure().cloned(),
            end_step: end.end_step_failure(),
            rollover: end.rollover(),
        }
    }
}

/// Item 6's rollover rows, exhaustively: a refusal keeps its own row, and an
/// uncertain append takes the durability row.
fn route(disclosure: &RolloverDisclosure) -> Rollover {
    match disclosure {
        RolloverDisclosure::Rolled { opened_generation } => Rollover::Rolled {
            opened_generation: *opened_generation,
        },
        RolloverDisclosure::AlreadyRolled => Rollover::AlreadyRolled,
        RolloverDisclosure::Skipped => Rollover::Skipped,
        RolloverDisclosure::Refused(row) => Rollover::Refused(installation_termination(row)),
        RolloverDisclosure::Undetermined => {
            Rollover::Undetermined(installation_termination(&Row::CommitUndetermined))
        }
    }
}

// ------------------------------------------------------- the delivery phase

/// The selected required renderer failed.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) struct RendererFailed;
/// An optional effect (browser launch, export) failed.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) struct OptionalFailed;
/// The required step failed: the renderer, the output or its flush.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
struct RequiredFailed;

/// Item 4 (r4): the delivery phase of a committed Run, supplied by the
/// caller. It reads nothing from the store: it projects and renders only
/// what the invocation already holds, the `PublishedCommit` lent here and
/// the evaluation result the phase itself holds, both in memory. It takes
/// no lease, receipt or read session (a writer's invocation has spent its
/// one receipt; X1 items 1 and 7). It runs only after `finish` consumed the
/// stopped session and released the writer lease, and it is handed nothing
/// that can open the store. `commit` is the committed Run, inert.
/// The envelope fixed at P5. Projection exists only for an unlatched commit.
pub(crate) struct DecidedEnvelope<'a, P> {
    pub(crate) outcome: &'a Outcome,
    pub(crate) projection: Option<&'a P>,
}
pub(crate) trait DeliveryPhase<C = PublishedCommit> {
    type Projection;
    fn project(&mut self, commit: &C) -> Result<(Self::Projection, u8), RendererFailed>;
    fn render(
        &mut self,
        envelope: DecidedEnvelope<'_, Self::Projection>,
    ) -> Result<RenderedResponse, RendererFailed>;
    fn finalize_operational(&mut self, finalization: &Finalization);
    fn output(&mut self) -> &mut dyn Write;
    fn error_output(&mut self) -> &mut dyn Write;
    fn optional(&mut self, commit: &C) -> Result<(), OptionalFailed>;
}
/// Caller-owned cancellation source. It receives a token only at P3, and
/// latches on the first signal while publication is running. P5 atomically
/// switches later signals to O; P6 switches them to E.
pub(crate) trait CancellationPort {
    fn observed(&mut self) -> Option<D9Signal>;
    fn arm(&mut self, token: CancellationLatch);
    fn returned(&mut self, admitted_at_close: bool, enters_delivery: bool);
    fn decide_output(&mut self) -> Option<D9Signal>;
    fn settled(&mut self);
}
/// Opened at R12, before provider work. Finalization retains the unused token.
pub(crate) struct OpenedFinalization {
    session: CommitSession,
    token: Option<CancellationLatch>,
}
#[cfg(test)]
impl OpenedFinalization {
    /// Build owned test data from this session; no production authority accessor.
    pub(crate) fn fixture<C>(&self, build: impl FnOnce(&CommitSession) -> C) -> C {
        build(&self.session)
    }
}

/// What the delivery phase did.
#[derive(Debug, PartialEq, Eq)]
enum Delivery {
    /// F39: latched after admission; no delivery phase was started.
    NotStarted,
    /// F16: the required step failed.
    Failed,
    /// The required response was delivered with this exit; any optional
    /// failure is disclosed beside it (F17).
    Delivered {
        exit: u8,
        optional: Option<OptionalFailed>,
    },
}

// ------------------------------------------------------------ the attempt

/// X3d's outcomes, joined: `publish`'s and `prepare_commit`'s.
#[derive(Debug)]
enum Joined {
    Committed(PublishedCommit),
    Undetermined {
        execution_id: String,
    },
    Refused(Row),
    ExistingAttempt {
        execution_id: String,
        requested: Box<RequestedBinding>,
    },
    Exhausted,
}
// X6 r3 item 6: `NotPrepared::ExistingAttempt` carries the requested
// binding, which item 3's row discloses (X6b, integrating second; X7 r5
// item 10).
impl From<CommitOutcome> for Joined {
    fn from(outcome: CommitOutcome) -> Self {
        match outcome {
            CommitOutcome::Committed(commit) => Self::Committed(commit),
            CommitOutcome::CommitUndetermined { execution_id } => {
                Self::Undetermined { execution_id }
            }
            CommitOutcome::Refused(row) => Self::Refused(row),
        }
    }
}
impl From<NotPrepared> for Joined {
    fn from(outcome: NotPrepared) -> Self {
        match outcome {
            NotPrepared::CarrierCapacityExhausted(_) => Self::Exhausted,
            NotPrepared::ExistingAttempt {
                execution_id,
                requested,
            } => Self::ExistingAttempt {
                execution_id,
                requested,
            },
            NotPrepared::CommitUndetermined { execution_id } => Self::Undetermined { execution_id },
            NotPrepared::Refused(row) => Self::Refused(row),
        }
    }
}

/// The attempt, after `finish` and the delivery phase: values only.
#[derive(Debug, PartialEq, Eq)]
enum Concluded {
    Committed {
        run: AuthoritativeRun,
        delivery: Delivery,
    },
    Undetermined {
        execution_id: String,
        namespace: String,
    },
    Refused(Row),
    ExistingAttempt {
        execution_id: String,
        requested: Box<RequestedBinding>,
    },
    Exhausted {
        namespace: String,
    },
}

// ------------------------------------------------------------- finalize

/// Item 1: finalize one durable analysis. `admit` is X1's write admission
/// and X2's project admission and handoff; it runs only after the replay
/// succeeded (X5 item 3), and its refusal is projected on its own row.
/// `phase` is the delivery phase of a committed Run.
pub(crate) fn open_finalization<D: DeliveryPhase>(
    operation: ProjectOperation,
    phase: &mut D,
    port: &mut impl CancellationPort,
) -> Result<OpenedFinalization, Box<Finalization>> {
    match CommitSession::open(operation) {
        Ok(mut session) => {
            let token = session.take_cancellation_latch();
            Ok(OpenedFinalization { session, token })
        }
        Err((refusal, stopped)) => {
            let end = stopped.finish();
            Err(Box::new(output_finalization::<D>(
                Concluded::Refused(refusal.termination()),
                end.into(),
                None,
                phase,
                port,
            )))
        }
    }
}
/// Analysis refusals after R12 use the same sole owner of refused/finish.
pub(crate) fn end_before_commit<D: DeliveryPhase>(
    opened: OpenedFinalization,
    row: Row,
    phase: &mut D,
    port: &mut impl CancellationPort,
) -> Finalization {
    let end = opened.session.refused().finish();
    output_finalization::<D>(Concluded::Refused(row), end.into(), None, phase, port)
}
pub(crate) fn finalize<D: DeliveryPhase>(
    opened: OpenedFinalization,
    candidate: &RunCandidateInputs<'_>,
    phase: &mut D,
    port: &mut impl CancellationPort,
) -> Finalization {
    let OpenedFinalization { session, token } = opened;
    let replayed = match replay_candidate(candidate, REPLAY_LIMITS) {
        Ok(replayed) => replayed,
        Err(refusal) => {
            let end = session.refused().finish();
            let result = Finalization {
                outcome: Outcome::Terminated(Termination {
                    row: replay_termination(&refusal),
                    run_id: None,
                    remedy: Some(replay_remedy(&refusal)),
                    namespace: None,
                    requested: None,
                }),
                end_failure: None,
                end_step_failure: None,
                rollover: None,
                optional_failure: None,
            };
            return output_decision(result, end.into(), None, None, phase, port);
        }
    };
    if let Some(signal) = port.observed() {
        let end = session.refused().finish();
        return output_finalization::<D>(
            Concluded::Refused(Row::Interrupted { signal }),
            end.into(),
            None,
            phase,
            port,
        );
    }
    let namespace = session.namespace_id().to_owned();
    let (attempt, stopped) = match prepare_commit(replayed, session) {
        Ok(prepared) => {
            // P3 alone transfers custody. Never arm on prepare's refusal paths.
            if let Some(token) = token {
                port.arm(token);
            }
            let (outcome, stopped) = prepared.publish();
            let enters_delivery = matches!(&outcome, CommitOutcome::Committed(commit) if !commit.latched_after_admission());
            port.returned(stopped.admitted_at_close(), enters_delivery);
            (Joined::from(outcome), stopped)
        }
        Err((outcome, stopped)) => (Joined::from(outcome), stopped),
    };
    let end = stopped.finish();
    match attempt {
        Joined::Committed(commit) => {
            if commit.latched_after_admission() {
                let concluded = Concluded::Committed {
                    run: authoritative_run(&commit),
                    delivery: Delivery::NotStarted,
                };
                output_finalization::<D>(concluded, end.into(), Some(&commit), phase, port)
            } else {
                let (projection, projected_exit) = match phase.project(&commit) {
                    Ok((projection, exit)) if matches!(exit, 0 | 1 | 3) => {
                        (Some(projection), Some(exit))
                    }
                    Ok(_) | Err(_) => (None, None),
                };
                let delivery =
                    projected_exit.map_or(Delivery::Failed, |exit| Delivery::Delivered {
                        exit,
                        optional: None,
                    });
                let result = finalization(
                    Concluded::Committed {
                        run: authoritative_run(&commit),
                        delivery,
                    },
                    EndDisclosure::default(),
                );
                output_decision(
                    result,
                    end.into(),
                    Some(&commit),
                    projection.as_ref(),
                    phase,
                    port,
                )
            }
        }
        Joined::Undetermined { execution_id } => output_finalization::<D>(
            Concluded::Undetermined {
                execution_id,
                namespace,
            },
            end.into(),
            None,
            phase,
            port,
        ),
        Joined::Refused(row) => {
            output_finalization::<D>(Concluded::Refused(row), end.into(), None, phase, port)
        }
        Joined::ExistingAttempt {
            execution_id,
            requested,
        } => output_finalization::<D>(
            Concluded::ExistingAttempt {
                execution_id,
                requested,
            },
            end.into(),
            None,
            phase,
            port,
        ),
        Joined::Exhausted => output_finalization::<D>(
            Concluded::Exhausted { namespace },
            end.into(),
            None,
            phase,
            port,
        ),
    }
}
fn output_finalization<D: DeliveryPhase>(
    concluded: Concluded,
    end: EndDisclosure,
    commit: Option<&PublishedCommit>,
    phase: &mut D,
    port: &mut impl CancellationPort,
) -> Finalization {
    output_decision(
        finalization(concluded, EndDisclosure::default()),
        end,
        commit,
        None,
        phase,
        port,
    )
}
fn output_decision<D: DeliveryPhase>(
    mut result: Finalization,
    end: EndDisclosure,
    commit: Option<&PublishedCommit>,
    projection: Option<&D::Projection>,
    phase: &mut D,
    port: &mut impl CancellationPort,
) -> Finalization {
    result.end_failure = end.settlement.as_ref().map(installation_termination);
    result.end_step_failure = end.end_step.as_ref().map(installation_termination);
    result.rollover = end.rollover.as_ref().map(route);
    // P5: one decision, returned outcome before signal, then O for all later signals.
    let signal = port.decide_output();
    let protected = matches!(&result.outcome, Outcome::Terminated(t) if t.row.error_code == Code::DurabilityCommitFailed)
        || commit.is_some_and(PublishedCommit::latched_after_admission);
    if !protected && let Some(signal) = signal {
        result.outcome = Outcome::Interrupted {
            signal,
            run: commit.map(authoritative_run),
        };
    }
    phase.finalize_operational(&result);
    let run_delivery = commit.is_some_and(|c| !c.latched_after_admission());
    let projection = if matches!(result.outcome, Outcome::Authoritative { .. }) {
        projection
    } else {
        None
    };
    let output = if run_delivery {
        opensip_platform::crash_barrier!(
            "x7.delivery",
            "required",
            fallible,
            emit_decided(&result.outcome, projection, phase),
            |_| RequiredOutputError::Projection
        )
    } else {
        emit_decided(&result.outcome, projection, phase)
    };
    match output {
        Ok(exit) => {
            if let Outcome::Authoritative { exit: settled, .. } = &mut result.outcome {
                *settled = exit;
            }
        }
        Err(RequiredOutputError::Projection) => {
            result.outcome = required_output_failure(commit, &result.outcome);
            match emit_decided(&result.outcome, None, phase) {
                Ok(_) => {}
                Err(RequiredOutputError::Projection) => {
                    let _ = writeln!(
                        phase.error_output(),
                        "DELIVERY.REQUIRED_FAILED: required metadata projection failed."
                    );
                }
                Err(RequiredOutputError::Emission) => {
                    result.outcome = emission_failure(commit, &result.outcome);
                    let _ = writeln!(
                        phase.error_output(),
                        "OUTPUT.SERIALIZATION_FAILED: required output emission failed."
                    );
                }
            }
        }
        Err(RequiredOutputError::Emission) => {
            result.outcome = emission_failure(commit, &result.outcome);
            let _ = writeln!(
                phase.error_output(),
                "OUTPUT.SERIALIZATION_FAILED: required output emission failed."
            );
        }
    }
    port.settled();
    if let (Outcome::Authoritative { .. }, Some(commit)) = (&result.outcome, commit) {
        let optional = opensip_platform::crash_barrier!(
            "x7.delivery",
            "optional",
            fallible,
            phase.optional(commit),
            |_| OptionalFailed
        );
        result.optional_failure = optional.err();
    }
    result
}
#[derive(Debug)]
enum RequiredOutputError {
    Projection,
    Emission,
}
fn decided_exit(outcome: &Outcome) -> u8 {
    match outcome {
        Outcome::Authoritative { exit, .. } => *exit,
        Outcome::Terminated(termination) => termination.row.exit,
        Outcome::Interrupted { .. } => 130,
    }
}
fn emit_decided<D: DeliveryPhase>(
    outcome: &Outcome,
    projection: Option<&D::Projection>,
    phase: &mut D,
) -> Result<u8, RequiredOutputError> {
    let response = phase
        .render(DecidedEnvelope {
            outcome,
            projection,
        })
        .map_err(|_| RequiredOutputError::Projection)?;
    if response.exit_code != decided_exit(outcome) {
        return Err(RequiredOutputError::Projection);
    }
    deliver_required(response, phase.output()).map_err(|_| RequiredOutputError::Emission)
}
fn emission_failure(commit: Option<&PublishedCommit>, previous: &Outcome) -> Outcome {
    let (namespace, subject) = match previous {
        Outcome::Terminated(t) => (t.namespace.clone(), t.row.subject.clone()),
        Outcome::Authoritative { .. } | Outcome::Interrupted { .. } => (None, None),
    };
    Outcome::Terminated(Termination {
        row: InstallationTerminationV1 {
            class: Class::OperationalFailed,
            exit: 4,
            error_code: Code::OutputSerializationFailed,
            fault_cause: Fault::OutputSerialization,
            detail: None,
            subject,
        },
        run_id: commit.map(|c| c.run_id().to_owned()),
        remedy: None,
        namespace,
        requested: None,
    })
}
fn required_output_failure(commit: Option<&PublishedCommit>, previous: &Outcome) -> Outcome {
    let (run_id, detail) = match commit {
        Some(c) => (
            Some(c.run_id().to_owned()),
            Detail::DeliveryRendererFailedAfterCommit,
        ),
        None => (None, Detail::DeliveryRequiredProjectionFailed),
    };
    let (namespace, subject) = match previous {
        Outcome::Terminated(t) if t.row.error_code == Code::DurabilityCommitFailed => {
            (t.namespace.clone(), t.row.subject.clone())
        }
        Outcome::Authoritative { .. } | Outcome::Terminated(_) | Outcome::Interrupted { .. } => {
            (None, None)
        }
    };
    Outcome::Terminated(Termination {
        row: InstallationTerminationV1 {
            class: Class::OperationalFailed,
            exit: 4,
            error_code: Code::DeliveryRequiredFailed,
            fault_cause: Fault::DeliveryRequired,
            detail: Some(detail),
            subject,
        },
        run_id,
        remedy: commit.map(|_| REMEDY_RENDERER_FAILED_AFTER_COMMIT),
        namespace,
        requested: None,
    })
}

/// Items 3, 6 and 8: the one envelope, and the end path's disclosures beside
/// it.
fn finalization(concluded: Concluded, end: EndDisclosure) -> Finalization {
    let (outcome, optional_failure) = project(concluded);
    Finalization {
        outcome,
        end_failure: end.settlement.as_ref().map(installation_termination),
        end_step_failure: end.end_step.as_ref().map(installation_termination),
        rollover: end.rollover.as_ref().map(route),
        optional_failure,
    }
}

/// Item 3's table, exhaustively, with no wildcard arm.
fn project(concluded: Concluded) -> (Outcome, Option<OptionalFailed>) {
    let terminated = |row, run_id, remedy, namespace| {
        Outcome::Terminated(Termination {
            row,
            run_id,
            remedy,
            namespace,
            requested: None,
        })
    };
    match concluded {
        Concluded::Committed { run, delivery } => match delivery {
            Delivery::Delivered { exit, optional } => {
                (Outcome::Authoritative { run, exit }, optional)
            }
            // F16, and F39's row: the RunId is retained.
            Delivery::Failed | Delivery::NotStarted => (
                terminated(
                    InstallationTerminationV1 {
                        class: Class::OperationalFailed,
                        exit: 4,
                        error_code: Code::DeliveryRequiredFailed,
                        fault_cause: Fault::DeliveryRequired,
                        detail: Some(Detail::DeliveryRendererFailedAfterCommit),
                        subject: None,
                    },
                    Some(run.run_id),
                    Some(REMEDY_RENDERER_FAILED_AFTER_COMMIT),
                    None,
                ),
                None,
            ),
        },
        // F12, F40: the durability row; the ExecutionId is the subject, the
        // namespace is disclosed beside it (item 5, r4), and no RunId exists.
        Concluded::Undetermined {
            execution_id,
            namespace,
        } => (
            terminated(
                InstallationTerminationV1 {
                    subject: Some(execution_id),
                    ..installation_termination(&Row::CommitUndetermined)
                },
                None,
                Some(REMEDY_COMMIT_UNDETERMINED),
                Some(namespace),
            ),
            None,
        ),
        // The row as X3d item 9 fixes it.
        Concluded::Refused(Row::Interrupted { signal }) => {
            (Outcome::Interrupted { signal, run: None }, None)
        }
        Concluded::Refused(row) => (
            terminated(installation_termination(&row), None, None, None),
            None,
        ),
        // Item 3 (r4, F34): X3d's invariant row, the ExecutionId as subject,
        // the binding's namespace and its other three members beside it (X6
        // r3 item 6), and the later-recovery remedy. No recovery runs in
        // this invocation.
        Concluded::ExistingAttempt {
            execution_id,
            requested,
        } => (
            Outcome::Terminated(Termination {
                row: InstallationTerminationV1 {
                    subject: Some(execution_id),
                    ..installation_termination(&Row::Invariant)
                },
                run_id: None,
                remedy: Some(REMEDY_EXISTING_ATTEMPT),
                namespace: Some(requested.namespace_id().to_owned()),
                requested: Some(*requested),
            }),
            None,
        ),
        // Item 6a: the existing busy row, naming the namespace, whatever the
        // rollover did (item 6); its outcome is disclosed beside the row.
        Concluded::Exhausted { namespace } => (
            terminated(
                InstallationTerminationV1 {
                    subject: Some(namespace),
                    ..installation_termination(&Row::Busy)
                },
                None,
                None,
                None,
            ),
            None,
        ),
    }
}

#[cfg(test)]
mod tests {
    include!("finalization_tests.rs");
}
