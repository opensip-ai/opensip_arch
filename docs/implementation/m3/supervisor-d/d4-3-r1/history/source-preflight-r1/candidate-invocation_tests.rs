// Law M3-J1 r5 (unit J2a): the pure invocation model, included as
// invocation.rs's cfg(test) module. The WFC invocation cases M3's step
// lists can express are restated in M3's terms, with the case they come
// from named on each test.
use super::*;
use crate::outcomes::{Deficiencies, Verdict};
use opensip_contracts::generated::evidence::{
    Common4D9Class as Class, Common4D9Deficiency as D9Deficiency, Common4D9ErrorCode as Code,
    Common4D9ReasonCode as Reason, Common4StepTerminationAuthority as Authority,
};
use opensip_contracts::generated::invocation::Invocation5StepOutcome as StepOutcome;
use opensip_security::InstallationTermination as Row;

const RUN: &str = "run3:1111111111111111111111111111111111111111111111111111111111111111";
const EXEC: &str = "exec1_22222222222222222222222222222222";
const NAMESPACE: &str = "ns1";

fn committed(verdict: Verdict) -> Observation {
    Observation::Analysis(AnalysisOutcome::Committed {
        run_id: RUN.into(),
        verdict,
    })
}
fn undetermined() -> Observation {
    Observation::CommitUndetermined {
        execution_id: EXEC.into(),
        namespace: NAMESPACE.into(),
    }
}
fn spec(
    kind: StepKind,
    requirement: Requirement,
    depends_on: &[usize],
    gate: Gate,
    retry: Retry,
) -> StepSpec {
    StepSpec {
        kind,
        requirement,
        depends_on: depends_on.to_vec(),
        gate,
        retry,
    }
}
fn outcomes(settled: &Settled) -> [StepOutcome; 2] {
    [settled.steps[0].outcome, settled.steps[1].outcome]
}
/// Drive a durable chain from J-alpha to J-iota and end it on `outcome`.
fn durable_attempt(outcome: Observation) -> AnalysisEnd {
    Join::durable()
        .entered()
        .admitted()
        .opened()
        .captured()
        .planned()
        .provided()
        .admitted_facts()
        .evaluated()
        .finished(outcome)
}

// ---------------------------------------------------------- R1 and 5.1

/// Item 5.1: `[analysis, render]` for each of the three requests, with
/// retry `none`, and R2's entry through `request.rs`.
#[test]
fn the_three_requests_build_their_step_lists_and_entries() {
    for (request, command, durability, entry) in [
        (
            AnalysisRequest::Default,
            Command::Default,
            Durability::Authoritative,
            InstallationEntry::Creator,
        ),
        (
            AnalysisRequest::Analyze,
            Command::Analyze,
            Durability::Authoritative,
            InstallationEntry::Creator,
        ),
        (
            AnalysisRequest::AnalyzeEphemeral,
            Command::Analyze,
            Durability::Ephemeral,
            InstallationEntry::Outside,
        ),
    ] {
        let flags = RequestFlags {
            project: Some(PathBuf::from("/work/p")),
            workspace_roots: vec![PathBuf::from("crates/a")],
            trust_groups: vec![20],
            trust_project_owner: true,
            allow_backup_custody: true,
        };
        let mode = InvocationModeV1 { interactive: false };
        let admitted = AdmittedRequest::admit(request, flags.clone(), mode).unwrap();
        assert_eq!(admitted.request().command(), command);
        assert_eq!(
            (admitted.flags(), admitted.mode(), admitted.format()),
            (&flags, mode, OutputFormat::Json)
        );
        assert_eq!(admitted.installation_entry(), Ok(entry));
        let steps = admitted.steps();
        assert_eq!(
            steps.specs(),
            [
                spec(
                    StepKind::Analysis,
                    Requirement::Required,
                    &[],
                    Gate::Completed,
                    Retry::None
                ),
                spec(
                    StepKind::Render,
                    Requirement::Required,
                    &[0],
                    Gate::Terminal,
                    Retry::None
                ),
            ]
        );
        assert_eq!(
            steps.analysis(),
            AnalysisParams {
                durability,
                snapshot_source: SnapshotSource::LiveWorktree
            }
        );
        assert_eq!(
            steps.render(),
            RenderParams {
                format: OutputFormat::Json,
                required: true
            }
        );
        assert_eq!(check_step_list(steps.specs()), Ok(()));
    }
}

/// WS section 1's step-list rules, on the WFC refusal cases. For the
/// host-built list every refusal is row 2, with the workflow key in the
/// operational record.
#[test]
fn the_wfc_step_list_refusals_are_row_2_for_a_host_built_list() {
    use Requirement::{Optional, Required};
    let analysis = |deps: &[usize]| {
        spec(
            StepKind::Analysis,
            Required,
            deps,
            Gate::Completed,
            Retry::None,
        )
    };
    let render = |deps: &[usize]| {
        spec(
            StepKind::Render,
            Required,
            deps,
            Gate::Terminal,
            Retry::None,
        )
    };
    let query = spec(StepKind::Query, Optional, &[], Gate::Completed, Retry::None);
    let cases: Vec<(&str, Vec<StepSpec>, StepListFault, &str)> = vec![
        (
            "forward-dependency-refused",
            vec![analysis(&[1]), render(&[])],
            StepListFault::DependencyCycle { step: 0 },
            "WORKFLOW.DEPENDENCY_CYCLE:0",
        ),
        (
            "duplicate-depends-on-refused",
            vec![analysis(&[]), render(&[0, 0])],
            StepListFault::DependencyInvalid { step: 1 },
            "WORKFLOW.DEPENDENCY_INVALID:1",
        ),
        (
            "sixty-five-steps-refused",
            std::iter::once(analysis(&[]))
                .chain(std::iter::repeat_n(query.clone(), 64))
                .collect(),
            StepListFault::StepBound,
            "WORKFLOW.STEP_BOUND_EXCEEDED",
        ),
        (
            "terminal-gate-on-analysis-refused",
            vec![spec(
                StepKind::Analysis,
                Required,
                &[],
                Gate::Terminal,
                Retry::None,
            )],
            StepListFault::GateNotApplicable { step: 0 },
            "WORKFLOW.GATE_NOT_APPLICABLE:0",
        ),
        (
            "required-depends-on-optional-refused",
            vec![
                spec(
                    StepKind::Import,
                    Optional,
                    &[],
                    Gate::Completed,
                    Retry::None,
                ),
                analysis(&[0]),
            ],
            StepListFault::RequiredDependsOnOptional { step: 1 },
            "WORKFLOW.REQUIRED_DEPENDS_ON_OPTIONAL:1",
        ),
        (
            "mutation-never-retried-schema",
            vec![spec(
                StepKind::Mutation,
                Required,
                &[],
                Gate::Completed,
                Retry::IdempotentRetry,
            )],
            StepListFault::RetryNotApplicable { step: 0 },
            "WORKFLOW.RETRY_BUDGET_EXHAUSTED:0",
        ),
        (
            "no steps",
            vec![],
            StepListFault::StepBound,
            "WORKFLOW.STEP_BOUND_EXCEEDED",
        ),
        (
            "a self reference",
            vec![analysis(&[0])],
            StepListFault::DependencyCycle { step: 0 },
            "WORKFLOW.DEPENDENCY_CYCLE:0",
        ),
        (
            "an unknown step",
            vec![analysis(&[]), render(&[2])],
            StepListFault::DependencyInvalid { step: 1 },
            "WORKFLOW.DEPENDENCY_INVALID:1",
        ),
        (
            "nine dependencies",
            std::iter::repeat_n(analysis(&[]), 9)
                .chain(std::iter::once(render(&[0, 1, 2, 3, 4, 5, 6, 7, 8])))
                .collect(),
            StepListFault::DependencyInvalid { step: 9 },
            "WORKFLOW.DEPENDENCY_INVALID:9",
        ),
    ];
    for (case, steps, fault, key) in cases {
        assert_eq!(check_step_list(&steps), Err(fault), "{case}");
        assert_eq!(fault.key(), key, "{case}");
        let t = project(&fault.observation());
        assert_eq!(
            (t.class, t.exit(), t.error_code, t.detail),
            (
                Class::OperationalFailed,
                4,
                Some(Code::SystemOutcomeIllegalState),
                None
            ),
            "{case}"
        );
        assert_eq!(t.operational, vec![key.to_owned()], "{case}");
    }
    // Lawful lists from the same corpus pass: 64 steps, an optional chain
    // that a terminal render ends, and an optional export.
    let sixty_four: Vec<StepSpec> = std::iter::once(analysis(&[]))
        .chain(std::iter::repeat_n(query, 63))
        .collect();
    assert_eq!(check_step_list(&sixty_four), Ok(()));
    let optional_chain = vec![
        spec(
            StepKind::Import,
            Optional,
            &[],
            Gate::Completed,
            Retry::None,
        ),
        spec(
            StepKind::Analysis,
            Optional,
            &[0],
            Gate::Completed,
            Retry::None,
        ),
        spec(
            StepKind::Render,
            Optional,
            &[1],
            Gate::Terminal,
            Retry::None,
        ),
    ];
    assert_eq!(check_step_list(&optional_chain), Ok(()));
    let export = vec![
        analysis(&[]),
        spec(
            StepKind::ExportDelivery,
            Optional,
            &[0],
            Gate::Terminal,
            Retry::IdempotentRetry,
        ),
    ];
    assert_eq!(check_step_list(&export), Ok(()));
}

// ------------------------------------------------------------ 5.2 joins

/// Item 5.2: the durable chain runs J-alpha to J-iota and the ephemeral
/// chain skips J-gamma and J-iota; a refusal at any join ends step 0 on its
/// row. Re-entering or skipping a join does not compile: each step consumes
/// the previous token.
#[test]
fn the_join_chains_end_step_0_at_any_join() {
    let alpha = Join::durable();
    assert_eq!(alpha.name(), JoinName::Alpha);
    let beta = alpha.entered();
    assert_eq!(beta.name(), JoinName::Beta);
    let gamma = beta.admitted();
    assert_eq!(gamma.name(), JoinName::Gamma);
    let delta = gamma.opened();
    assert_eq!(delta.name(), JoinName::Delta);
    let refused = delta.refused(Observation::HostIo);
    assert_eq!(refused, AnalysisEnd::Ended(Observation::HostIo));
    assert_eq!(
        durable_attempt(undetermined()),
        AnalysisEnd::Ended(undetermined())
    );

    let ephemeral = Join::ephemeral().entered();
    assert_eq!(ephemeral.name(), JoinName::Beta);
    let delta = ephemeral.admitted();
    assert_eq!(delta.name(), JoinName::Delta);
    let theta = delta.captured().planned().provided().admitted_facts();
    assert_eq!(theta.name(), JoinName::Theta);
    assert_eq!(
        theta.evaluated(EphemeralVerdict::Pass),
        AnalysisEnd::Ended(Observation::Analysis(AnalysisOutcome::Ephemeral(
            EphemeralVerdict::Pass
        )))
    );
    // R10a's refusal at J-beta ends step 0 before any session (row 56).
    let deciding = Deciding {
        signal: Signal::Sigint,
        phase: CancelPhase::A,
    };
    assert_eq!(
        Join::durable().entered().cancelled(deciding),
        AnalysisEnd::Cancelled(deciding)
    );
}

// ---------------------------------------------------- 8.2 phases, LD-r5-1

#[test]
fn every_operation_point_has_its_phase() {
    for (point, phase) in [
        (OperationPoint::BeforeAttemptAdmission, CancelPhase::A),
        (OperationPoint::AttemptAdmitted, CancelPhase::B),
        (OperationPoint::FinalGateAdmitted, CancelPhase::C),
        // LD-r5-1: the window close's own sample decides.
        (
            OperationPoint::PublishReturned { admitted: false },
            CancelPhase::B,
        ),
        (
            OperationPoint::PublishReturned { admitted: true },
            CancelPhase::C,
        ),
        (OperationPoint::CommittedUnlatched, CancelPhase::D),
        (OperationPoint::FinalOutput, CancelPhase::O),
        (OperationPoint::Settled, CancelPhase::E),
    ] {
        assert_eq!(point.phase(), phase, "{point:?}");
    }
}

/// The cancellation source: the first signal before the decision point
/// decides and takes its phase's effect; later ones force the second
/// stage; O defers and E records. Every signal is recorded with its
/// ordinal and arrival phase, in memory.
#[test]
fn the_cancellation_source_classifies_every_signal() {
    for (point, effect) in [
        (
            OperationPoint::BeforeAttemptAdmission,
            SignalEffect::Cooperate,
        ),
        (OperationPoint::AttemptAdmitted, SignalEffect::Latch),
        (OperationPoint::FinalGateAdmitted, SignalEffect::Latch),
        (
            OperationPoint::PublishReturned { admitted: true },
            SignalEffect::Latch,
        ),
        (
            OperationPoint::CommittedUnlatched,
            SignalEffect::CancelAtDecisionPoint,
        ),
    ] {
        let mut source = CancellationSource::new();
        let (record, first) = source.observe(Signal::Sigterm, point);
        assert_eq!(first, effect, "{point:?}");
        assert_eq!(
            record,
            SignalRecord {
                signal: Signal::Sigterm,
                ordinal: 1,
                phase: point.phase()
            }
        );
        assert_eq!(
            source.deciding(),
            Some(Deciding {
                signal: Signal::Sigterm,
                phase: point.phase()
            })
        );
        let (record, second) = source.observe(Signal::Sigint, point);
        assert_eq!(
            (record.ordinal, second),
            (2, SignalEffect::Force),
            "{point:?}"
        );
        // The first signal still decides.
        assert_eq!(source.deciding().unwrap().signal, Signal::Sigterm);
    }
    let mut source = CancellationSource::new();
    assert_eq!(
        source
            .observe(Signal::Sighup, OperationPoint::FinalOutput)
            .1,
        SignalEffect::Defer
    );
    assert_eq!(
        source.observe(Signal::Sighup, OperationPoint::Settled),
        (
            SignalRecord {
                signal: Signal::Sighup,
                ordinal: 2,
                phase: CancelPhase::E
            },
            SignalEffect::Record
        )
    );
    assert_eq!(source.deciding(), None);
}

// ------------------------------------------ 5.3 and 8.4: WFC and CINV cases

/// WFC `default-analyze-render-success` (retry `none`, 5.1) and
/// `policy-failed-with-run`.
#[test]
fn a_committed_run_settles_on_its_verdict() {
    for (verdict, class, exit) in [
        (Verdict::Pass, Class::Success, 0),
        (Verdict::Fail, Class::PolicyFailed, 1),
    ] {
        let decision = Decision::decide(durable_attempt(committed(verdict)), None);
        assert_eq!(decision.step1_terminal(), None);
        let settled = decision.output_returned();
        assert_eq!((settled.termination.class, settled.exit()), (class, exit));
        assert_eq!(settled.termination.run_id.as_deref(), Some(RUN));
        assert_eq!(
            outcomes(&settled),
            [StepOutcome::Completed, StepOutcome::Completed]
        );
    }
}

/// WFC `ephemeral-result-has-no-run-and-no-authority`.
#[test]
fn an_ephemeral_failing_verdict_is_policy_failed_with_no_run() {
    let end = Join::ephemeral()
        .entered()
        .admitted()
        .captured()
        .planned()
        .provided()
        .admitted_facts()
        .evaluated(EphemeralVerdict::Fail);
    let settled = Decision::decide(end, None).output_returned();
    assert_eq!(
        (settled.termination.class, settled.exit()),
        (Class::PolicyFailed, 1)
    );
    assert_eq!(
        (settled.termination.run_id, settled.termination.authority),
        (None, Some(Authority::Ephemeral))
    );
}

/// WFC `indeterminate-provider-unavailable`.
#[test]
fn a_required_provider_unavailable_is_indeterminate() {
    use crate::outcomes::AnalysisDetail;
    let verdict = Verdict::Indeterminate {
        deficiencies: Deficiencies::new(D9Deficiency::ProviderUnavailable, &[]).unwrap(),
        coverage_id: None,
        detail: Some(AnalysisDetail::RequiredClosureNotInstalled),
    };
    let settled = Decision::decide(durable_attempt(committed(verdict)), None).output_returned();
    assert_eq!(
        (settled.termination.class, settled.exit()),
        (Class::Indeterminate, 3)
    );
    assert_eq!(
        settled.termination.reason_codes,
        vec![Reason::CoverageProviderUnavailable]
    );
    assert_eq!(
        settled.termination.detail,
        Some(Detail::ComponentRequiredClosureNotInstalled)
    );
}

/// WFC `operational-fault-dominates-committed-policy-failure` and CINV
/// `analyze-renderer-failed-after-commit` (rows 43; F16): a renderer
/// failure before any byte of a committed Run's envelope.
#[test]
fn a_renderer_failure_after_commit_dominates_and_keeps_the_run() {
    let decision = Decision::decide(durable_attempt(committed(Verdict::Fail)), None);
    let replaced = decision.renderer_failed().unwrap();
    let settled = replaced.output_returned();
    assert_eq!(
        (settled.termination.class, settled.exit()),
        (Class::OperationalFailed, 4)
    );
    assert_eq!(
        settled.termination.error_code,
        Some(Code::DeliveryRequiredFailed)
    );
    assert_eq!(
        settled.termination.detail,
        Some(Detail::DeliveryRendererFailedAfterCommit)
    );
    assert_eq!(settled.termination.run_id.as_deref(), Some(RUN));
    assert_eq!(
        outcomes(&settled),
        [StepOutcome::Completed, StepOutcome::Failed]
    );
}

/// WFC `cancel-before-settle-is-interrupted` and CINV
/// `interrupted-before-settle`: a signal before step 0 ends.
#[test]
fn a_signal_before_settle_is_interrupted_with_no_run() {
    let mut source = CancellationSource::new();
    let (_, effect) = source.observe(Signal::Sigint, OperationPoint::BeforeAttemptAdmission);
    assert_eq!(effect, SignalEffect::Cooperate);
    let end = Join::durable()
        .entered()
        .admitted()
        .opened()
        .captured()
        .cancelled(source.deciding().unwrap());
    let decision = Decision::decide(end, source.deciding());
    assert_eq!(
        decision.step1_terminal().unwrap().outcome,
        StepOutcome::Cancelled
    );
    let settled = decision.output_returned();
    assert_eq!(
        (settled.termination.class, settled.exit()),
        (Class::Interrupted, 130)
    );
    assert_eq!(
        (
            settled.termination.signal,
            settled.termination.run_id.as_deref()
        ),
        (Some(Signal::Sigint), None)
    );
    assert_eq!(
        outcomes(&settled),
        [StepOutcome::Cancelled, StepOutcome::Cancelled]
    );
}

/// WFC `cancel-after-settle-not-reclassified` and CINV
/// `interrupted-after-settle`: a signal after settlement is recorded only.
#[test]
fn a_signal_after_settle_is_recorded_and_reclassifies_nothing() {
    let mut source = CancellationSource::new();
    let settled = Decision::decide(durable_attempt(committed(Verdict::Fail)), source.deciding())
        .output_returned();
    assert_eq!(
        source.observe(Signal::Sigint, OperationPoint::Settled).1,
        SignalEffect::Record
    );
    assert_eq!(
        (settled.termination.class, settled.exit()),
        (Class::PolicyFailed, 1)
    );
    assert_eq!(source.deciding(), None);
}

/// WFC `cancel-mid-invocation-with-committed-run`, in M3's terms (8.3 rule
/// 3; row 47; S12-D): a signal in phase D gives `interrupted` with the
/// committed Run's id, step 0 completed and step 1 cancelled.
#[test]
fn a_signal_in_phase_d_is_interrupted_with_the_run() {
    let mut source = CancellationSource::new();
    let end = durable_attempt(committed(Verdict::Pass));
    assert_eq!(
        source
            .observe(Signal::Sigterm, OperationPoint::CommittedUnlatched)
            .1,
        SignalEffect::CancelAtDecisionPoint
    );
    let settled = Decision::decide(end, source.deciding()).output_returned();
    assert_eq!(
        (settled.termination.class, settled.exit()),
        (Class::Interrupted, 130)
    );
    assert_eq!(settled.termination.run_id.as_deref(), Some(RUN));
    assert_eq!(settled.termination.signal, Some(Signal::Sigterm));
    assert_eq!(
        outcomes(&settled),
        [StepOutcome::Completed, StepOutcome::Cancelled]
    );
}

/// WFC `host-io-not-retried`: a host I/O failure ends step 0 on its row in
/// one attempt; nothing in the model retries.
#[test]
fn a_host_io_failure_ends_on_its_row() {
    let end = Join::durable()
        .entered()
        .refused(Observation::Installation(Row::HostIo));
    let settled = Decision::decide(end, None).output_returned();
    assert_eq!(
        (
            settled.termination.class,
            settled.exit(),
            settled.termination.error_code
        ),
        (Class::OperationalFailed, 4, Some(Code::HostIoFailure))
    );
    assert_eq!(
        outcomes(&settled),
        [StepOutcome::Failed, StepOutcome::Completed]
    );
}

// ----------------------------------------------- 8.3: the precedence rules

/// Rule 1 (row 38; J-C14; S12-U): any `CommitUndetermined`, whatever the
/// gate's state, takes the durability row with the ExecutionId, never F39
/// or a runId, including a latch 1 to 3 followed by an undetermined
/// evidence `COMMIT` (LD-r5-1 labels it C).
#[test]
fn rule_1_any_undetermined_commit_takes_the_durability_row() {
    for point in [
        OperationPoint::BeforeAttemptAdmission,
        OperationPoint::AttemptAdmitted,
        OperationPoint::FinalGateAdmitted,
        OperationPoint::PublishReturned { admitted: true },
        OperationPoint::PublishReturned { admitted: false },
    ] {
        let mut source = CancellationSource::new();
        source.observe(Signal::Sigint, point);
        let decision = Decision::decide(durable_attempt(undetermined()), source.deciding());
        let envelope = decision.envelope();
        assert_eq!(
            (envelope.class, envelope.exit(), envelope.error_code),
            (
                Class::OperationalFailed,
                4,
                Some(Code::DurabilityCommitFailed)
            ),
            "{point:?}"
        );
        assert_eq!(
            (envelope.run_id.as_deref(), envelope.execution_id.as_deref()),
            (None, Some(EXEC))
        );
        assert_ne!(
            envelope.detail,
            Some(Detail::DeliveryRendererFailedAfterCommit)
        );
        assert_eq!(
            decision.uncertain(),
            Some(&Uncertain {
                execution_id: EXEC.into(),
                namespace: NAMESPACE.into()
            })
        );
        // The remaining step is cancelled; the commit outcome governs (S21).
        assert_eq!(
            decision.step1_terminal().unwrap().outcome,
            StepOutcome::Cancelled
        );
    }
    // Security's bare undetermined row takes rule 1 too, with no disclosure.
    let decision = Decision::decide(
        durable_attempt(Observation::Installation(Row::CommitUndetermined)),
        Some(Deciding {
            signal: Signal::Sigint,
            phase: CancelPhase::C,
        }),
    );
    assert_eq!(
        decision.envelope().error_code,
        Some(Code::DurabilityCommitFailed)
    );
    assert_eq!(decision.uncertain(), None);
    // With no signal the same row stands.
    let envelope = Decision::decide(durable_attempt(undetermined()), None)
        .envelope()
        .clone();
    assert_eq!(envelope.error_code, Some(Code::DurabilityCommitFailed));
}

/// Rule 2 (row 42; X7's F39; S12-C): a `Committed` latched after admission
/// takes `DELIVERY.REQUIRED_FAILED` with its runId, whether a signal or the
/// observer latched it.
#[test]
fn rule_2_a_latched_commit_takes_f39_with_the_run() {
    for signal in [
        None,
        Some(Deciding {
            signal: Signal::Sigint,
            phase: CancelPhase::C,
        }),
    ] {
        let decision = Decision::decide(
            durable_attempt(Observation::LatchedAfterAdmission { run_id: RUN.into() }),
            signal,
        );
        let envelope = decision.envelope();
        assert_eq!(
            (envelope.class, envelope.error_code, envelope.detail),
            (
                Class::OperationalFailed,
                Some(Code::DeliveryRequiredFailed),
                Some(Detail::DeliveryRendererFailedAfterCommit)
            )
        );
        assert_eq!(envelope.run_id.as_deref(), Some(RUN));
        assert_ne!(envelope.class, Class::Interrupted);
    }
}

/// Rule 4 (row 46): a certain refusal before the signal, or a `publish`
/// `Refused` (LD-r5-1: B), gives `interrupted` with no runId; the refused
/// attempt's own row stays with step 0, outside the envelope.
#[test]
fn rule_4_otherwise_interrupted_with_no_run() {
    let mut source = CancellationSource::new();
    source.observe(
        Signal::Sigterm,
        OperationPoint::PublishReturned { admitted: false },
    );
    assert_eq!(source.deciding().unwrap().phase, CancelPhase::B);
    let decision = Decision::decide(
        durable_attempt(Observation::Installation(Row::Busy)),
        source.deciding(),
    );
    assert_eq!(
        (
            decision.envelope().class,
            decision.envelope().run_id.as_deref()
        ),
        (Class::Interrupted, None)
    );
    assert_eq!(decision.step0().outcome, StepOutcome::Failed);
    assert_eq!(
        decision.step0().termination.error_code,
        Some(Code::LedgerBusyTimeout)
    );
    // A committed Run whose signal was not observed in D keeps rule 4.
    let decision = Decision::decide(
        durable_attempt(committed(Verdict::Pass)),
        Some(Deciding {
            signal: Signal::Sigint,
            phase: CancelPhase::A,
        }),
    );
    assert_eq!(
        (
            decision.envelope().class,
            decision.envelope().run_id.as_deref()
        ),
        (Class::Interrupted, None)
    );
}

// ------------------------------------------- 8.2's phase O and settlement

/// Phase O (S18; J-C14 "a signal in O"): a signal after the decision point
/// is deferred and the decided envelope and its exit stand.
#[test]
fn a_signal_in_the_final_output_section_is_deferred() {
    let mut source = CancellationSource::new();
    let decision = Decision::decide(durable_attempt(committed(Verdict::Pass)), source.deciding());
    assert_eq!(
        source.observe(Signal::Sigint, OperationPoint::FinalOutput),
        (
            SignalRecord {
                signal: Signal::Sigint,
                ordinal: 1,
                phase: CancelPhase::O
            },
            SignalEffect::Defer
        )
    );
    let settled = decision.output_returned();
    assert_eq!(
        (settled.termination.class, settled.exit()),
        (Class::Success, 0)
    );
    assert_eq!(settled.termination.run_id.as_deref(), Some(RUN));
}

/// J-C14b: the failure envelope of a renderer failure in O is chosen by the
/// committed evidence (row 43 or 44), and an uncertain step 0 keeps its
/// ExecutionId and namespace disclosed beside the primary termination,
/// never as the render attempt's or a Run's.
#[test]
fn a_renderer_failure_in_o_is_routed_by_committed_evidence() {
    let ephemeral = AnalysisEnd::Ended(Observation::Analysis(AnalysisOutcome::Ephemeral(
        EphemeralVerdict::Pass,
    )));
    let refusal = AnalysisEnd::Ended(Observation::Installation(Row::NotInitialized));
    for (end, detail, run_id) in [
        (
            durable_attempt(committed(Verdict::Pass)),
            Detail::DeliveryRendererFailedAfterCommit,
            Some(RUN),
        ),
        (
            durable_attempt(Observation::LatchedAfterAdmission { run_id: RUN.into() }),
            Detail::DeliveryRendererFailedAfterCommit,
            Some(RUN),
        ),
        (ephemeral, Detail::DeliveryRequiredProjectionFailed, None),
        (refusal, Detail::DeliveryRequiredProjectionFailed, None),
        (
            durable_attempt(undetermined()),
            Detail::DeliveryRequiredProjectionFailed,
            None,
        ),
    ] {
        let failed = Decision::decide(end, None).renderer_failed().unwrap();
        let settled = failed.output_returned();
        assert_eq!(settled.steps[1].termination.detail, Some(detail));
        assert_eq!(settled.steps[1].termination.run_id.as_deref(), run_id);
        assert_eq!(settled.exit(), 4);
    }
    // The uncertain attempt: WS:233-240's tie keeps step 1's detailed row
    // as primary; the ExecutionId and namespace stay disclosed separately.
    let settled = Decision::decide(durable_attempt(undetermined()), None)
        .renderer_failed()
        .unwrap()
        .output_returned();
    assert_eq!(
        settled.termination.detail,
        Some(Detail::DeliveryRequiredProjectionFailed)
    );
    assert_eq!(
        (
            settled.termination.run_id.as_deref(),
            settled.termination.execution_id.as_deref()
        ),
        (None, None)
    );
    assert_eq!(
        settled.uncertain,
        Some(Uncertain {
            execution_id: EXEC.into(),
            namespace: NAMESPACE.into()
        })
    );
    assert_eq!(
        settled.steps[0].termination.execution_id.as_deref(),
        Some(EXEC)
    );
}

/// S18: a renderer failure of a termination output (step 1 cancelled at
/// the decision point) still fails step 1, and the failure envelope
/// replaces `interrupted`.
#[test]
fn a_renderer_failure_of_a_termination_output_replaces_it() {
    let decided = Decision::decide(
        durable_attempt(committed(Verdict::Pass)),
        Some(Deciding {
            signal: Signal::Sigint,
            phase: CancelPhase::D,
        }),
    );
    assert_eq!(decided.envelope().class, Class::Interrupted);
    let settled = decided.renderer_failed().unwrap().output_returned();
    assert_eq!(
        (settled.termination.class, settled.termination.detail),
        (
            Class::OperationalFailed,
            Some(Detail::DeliveryRendererFailedAfterCommit)
        )
    );
    assert_eq!(settled.termination.run_id.as_deref(), Some(RUN));
    assert_eq!(
        outcomes(&settled),
        [StepOutcome::Completed, StepOutcome::Failed]
    );
}

/// S18: an unrenderable failure envelope, and a failed write or flush
/// whether or not a byte was written, end with exit 4 and no replacement.
#[test]
fn an_undeliverable_envelope_ends_exit_4_with_no_replacement() {
    let decision = Decision::decide(durable_attempt(committed(Verdict::Pass)), None);
    assert_eq!(decision.clone().output_failed().exit(), 4);
    let replaced = decision.renderer_failed().unwrap();
    assert_eq!(replaced.clone().output_failed().exit(), 4);
    assert_eq!(replaced.renderer_failed().map(|_| ()), Err(Undelivered));
}

/// J-C14c: an ephemeral signal before the decision point is `interrupted`
/// on the empty-errors branch, with no runId and no durable effect.
#[test]
fn an_ephemeral_signal_before_the_decision_point_is_interrupted() {
    let mut source = CancellationSource::new();
    let theta = Join::ephemeral()
        .entered()
        .admitted()
        .captured()
        .planned()
        .provided()
        .admitted_facts();
    assert_eq!(
        source
            .observe(Signal::Sigint, OperationPoint::BeforeAttemptAdmission)
            .1,
        SignalEffect::Cooperate
    );
    let settled = Decision::decide(theta.evaluated(EphemeralVerdict::Pass), source.deciding())
        .output_returned();
    assert_eq!(
        (
            settled.termination.class,
            settled.exit(),
            settled.termination.run_id.as_deref()
        ),
        (Class::Interrupted, 130, None)
    );
    assert_eq!(settled.termination.detail, None);
}

// ------------------------------------------------------- WS:233-240

/// WFC `policy-fail-dominates-indeterminate-across-steps`,
/// `optional-export-failure-keeps-success` and
/// `optional-import-rejected-then-analysis-skipped-but-render-runs`, with
/// the tie rule.
#[test]
fn the_aggregate_follows_the_d9_order_over_required_steps() {
    let ended = |o: Observation| StepResult::ended(project(&o));
    let fail = ended(committed(Verdict::Fail));
    let query_indeterminate = ended(committed(Verdict::Indeterminate {
        deficiencies: Deficiencies::new(D9Deficiency::QueryCompletenessUnmet, &[]).unwrap(),
        coverage_id: None,
        detail: None,
    }));
    let t = aggregate(&[
        (Requirement::Required, &fail),
        (Requirement::Required, &query_indeterminate),
    ]);
    assert_eq!((t.class, t.exit()), (Class::PolicyFailed, 1));

    let pass = ended(committed(Verdict::Pass));
    let export_failed = ended(Observation::HostIo);
    let t = aggregate(&[
        (Requirement::Required, &pass),
        (Requirement::Optional, &export_failed),
    ]);
    assert_eq!((t.class, t.exit()), (Class::Success, 0));

    let rejected = ended(Observation::ConfigurationInvalid { subject: None });
    let skipped = StepResult {
        outcome: StepOutcome::Skipped,
        termination: project(&Observation::HostIo),
    };
    let rendered = StepResult::completed();
    let t = aggregate(&[
        (Requirement::Optional, &rejected),
        (Requirement::Optional, &skipped),
        (Requirement::Optional, &rendered),
    ]);
    assert_eq!((t.class, t.exit()), (Class::Success, 0));

    // Ties keep the first termination carrying a detail, else the first.
    let io = ended(Observation::HostIo);
    let busy = ended(Observation::Installation(Row::Busy));
    let t = aggregate(&[(Requirement::Required, &io), (Requirement::Required, &busy)]);
    assert_eq!(t.detail, Some(Detail::ProjectBusy));
    let t = aggregate(&[
        (Requirement::Required, &io),
        (
            Requirement::Required,
            &ended(Observation::HostPanicBeforeAdmission),
        ),
    ]);
    assert_eq!(t.error_code, Some(Code::HostIoFailure));
}

/// D4-T2 has no carrier at M3. All three requests, both typed modes and
/// every presence/boolean combination of the five flags classify None.
#[test]
fn every_m3_request_is_classified_without_an_excluded_form() {
    for request in [
        AnalysisRequest::Default,
        AnalysisRequest::Analyze,
        AnalysisRequest::AnalyzeEphemeral,
    ] {
        for interactive in [false, true] {
            for mask in 0..32 {
                let flags = RequestFlags {
                    project: (mask & 1 != 0).then(|| PathBuf::from("/work/project")),
                    workspace_roots: if mask & 2 != 0 {
                        vec![PathBuf::from("/work/member")]
                    } else {
                        Vec::new()
                    },
                    trust_groups: if mask & 4 != 0 { vec![20] } else { Vec::new() },
                    trust_project_owner: mask & 8 != 0,
                    allow_backup_custody: mask & 16 != 0,
                };
                let mode = InvocationModeV1 { interactive };
                let admitted = AdmittedRequest::admit(request, flags.clone(), mode).unwrap();
                assert_eq!(request_excluded_form(&admitted), None);
                assert_eq!(admitted.request(), request);
                assert_eq!(admitted.flags(), &flags);
                assert_eq!(admitted.mode(), mode);
            }
        }
    }
}

/// LD-D4-7: preserve the exhaustive request classifier and the one opaque
/// construction-to-classification-to-return path, before any effect owner.
#[test]
fn request_classification_is_exhaustive_and_precedes_token_handover() {
    let source = include_str!("invocation.rs");
    let classifier = source
        .split("pub(crate) fn request_excluded_form(")
        .nth(1)
        .unwrap()
        .split("// ------------------------------------------------ item 5.1")
        .next()
        .unwrap();
    assert!(source.contains("#[deny(unreachable_patterns)]"));
    assert!(!classifier.contains("_ =>"));
    assert!(!classifier.contains(".."));
    for arm in [
        "AnalysisRequest::Default => None",
        "AnalysisRequest::Analyze => None",
        "AnalysisRequest::AnalyzeEphemeral => None",
    ] {
        assert_eq!(
            classifier.matches(arm).count(),
            1,
            "new request requires item25 review"
        );
    }
    let admission = source
        .split("pub(crate) fn admit(")
        .nth(1)
        .unwrap()
        .split("pub(crate) fn request(&self)")
        .next()
        .unwrap();
    let checked = admission.find("check_step_list(steps.specs())").unwrap();
    let constructed = admission.find("let admitted = Self {").unwrap();
    let classified = admission.find("request_excluded_form(&admitted)").unwrap();
    let handover = admission.find("Ok(admitted)").unwrap();
    assert!(checked < constructed && constructed < classified && classified < handover);
    assert_eq!(
        admission
            .matches("request_excluded_form(&admitted)")
            .count(),
        1
    );
    assert!(!admission.contains("Ok(Self {"));
    assert!(!admission.contains("RequestIdentity::draw"));
    assert!(!admission.contains(".begin("));
    assert_eq!(
        source.matches("AdmittedRequest {").count(),
        3,
        "only the private type, impl and closed destructure; review every new constructor"
    );
}
