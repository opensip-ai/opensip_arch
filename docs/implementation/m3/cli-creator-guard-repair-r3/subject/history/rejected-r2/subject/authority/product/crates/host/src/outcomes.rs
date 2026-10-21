use crate::configuration::{PolicySelectionRefusal, policy_selection_termination};
use crate::invocation::Requirement;
use crate::request::{RequestAllocationError, RequestAuthority, RequestContext};
use crate::typescript_config::ConfigRefusal;
use crate::{InstallationTerminationV1, installation_termination};
use opensip_contracts::generated::evidence::{
    Common4D9Class as Class, Common4D9Deficiency as D9Deficiency, Common4D9ErrorCode as Code,
    Common4D9FaultCause as Fault, Common4D9ReasonCode as Reason, Common4D9Signal as Signal,
    Common4DomainDetailCode as Detail, Common4NativeSufficiencyDeficiency as NativeDeficiency,
    Common4StepTerminationAuthority as Authority,
};
use opensip_contracts::generated::invocation::Invocation5StepOutcome as StepOutcome;
use opensip_contracts::generated::output::{Envelope7Root, Metadata1HelpCommand};
use opensip_security::InstallationTermination as Row;
use serde_json::{Value, json};
use std::sync::Arc;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum MetadataError {
    Projection,
    Serialization,
}
impl From<&'static str> for MetadataError {
    fn from(_: &'static str) -> Self {
        Self::Projection
    }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Format {
    Human,
    Json,
}
#[derive(Debug)]
pub enum MetadataRequest {
    Help { topic: Option<String> },
    Version,
    Completion { shell: String },
    Rejected { diagnostic: &'static str },
    FormatNotApplicable,
}
pub struct RenderedResponse {
    pub bytes: Vec<u8>,
    pub exit_code: u8,
}

/// Explicit process-only ingress for metadata operations and, beside it, the
/// read-only `doctor` ingress (law X10; `doctor_ingress.rs`). Neither admits
/// an analysis or mutation, and neither opens a project, writes durably or
/// starts a provider session. Doctor reads the account installation through
/// the 458c read receipt and observation session only.
#[derive(Default)]
pub struct MetadataHost {
    authority: RequestAuthority,
    /// The process start capability set, held only by its owning host.
    capabilities: Option<opensip_operability::CapabilitySet>,
    /// Set when logging start fails. No summary is frozen in that case (item 12).
    logging_unavailable: Option<opensip_operability::LoggingUnavailable>,
    #[cfg(any(feature = "operability-dev-sinks", feature = "harness-instrumentation"))]
    request_span: std::sync::Mutex<Option<opensip_operability::RequestSpan>>,
    #[cfg(any(feature = "operability-dev-sinks", feature = "harness-instrumentation"))]
    phase_error: std::sync::Mutex<Option<opensip_operability::PhaseError>>,
}
impl MetadataHost {
    pub fn new() -> Self {
        Self::default()
    }
    /// Must precede argument parsing. No caller identifier is accepted.
    pub fn begin(&mut self) -> Result<Arc<RequestContext>, RequestAllocationError> {
        let context = self.authority.begin()?;
        // The RequestId is already allocated. An entropy failure here disables logging only.
        let scope = self
            .authority
            .logging_scope(&context)
            .expect("the authority owns the request it just reserved");
        match opensip_operability::start_for_request(scope) {
            Some(Ok(set)) => {
                self.capabilities = Some(set);
                #[cfg(any(feature = "operability-dev-sinks", feature = "harness-instrumentation"))]
                match opensip_operability::RequestSpan::begin(scope) {
                    Ok(span) => {
                        *self.request_span.lock().unwrap_or_else(|e| e.into_inner()) = Some(span)
                    }
                    Err(error) => self.record_phase_error(error),
                }
            }
            Some(Err(error)) => self.logging_unavailable = Some(error),
            None => {}
        }
        Ok(context)
    }
    #[cfg(any(feature = "operability-dev-sinks", feature = "harness-instrumentation"))]
    fn record_phase_error(&self, error: opensip_operability::PhaseError) {
        let mut first = self.phase_error.lock().unwrap_or_else(|e| e.into_inner());
        if first.is_none() {
            *first = Some(error);
        }
    }
    /// Observe the metadata delivery preparation actually owned by this ingress.
    /// Required final envelope projection and physical output remain after the freeze.
    pub(crate) fn prepare_delivery<T>(
        &self,
        context: &RequestContext,
        action: impl FnOnce() -> Result<T, MetadataError>,
    ) -> Result<T, MetadataError> {
        self.request_id(context)?;
        #[cfg(any(feature = "operability-dev-sinks", feature = "harness-instrumentation"))]
        let held = self.request_span.lock().unwrap_or_else(|e| e.into_inner());
        #[cfg(any(feature = "operability-dev-sinks", feature = "harness-instrumentation"))]
        let delivery =
            held.as_ref().and_then(
                |root| match root.start(opensip_operability::Phase::Delivery) {
                    Ok(span) => Some(span),
                    Err(error) => {
                        self.record_phase_error(error);
                        None
                    }
                },
            );
        let result = action();
        #[cfg(any(feature = "operability-dev-sinks", feature = "harness-instrumentation"))]
        if let Some(delivery) = delivery {
            let outcome = if result.is_ok() {
                opensip_operability::PhaseOutcome::Completed
            } else {
                opensip_operability::PhaseOutcome::Failed
            };
            if let Err(error) = delivery.finish(outcome) {
                self.record_phase_error(error);
            }
        }
        result
    }
    pub(crate) fn finish_logging(&self, failed: bool) {
        #[cfg(any(feature = "operability-dev-sinks", feature = "harness-instrumentation"))]
        {
            let root = self
                .request_span
                .lock()
                .unwrap_or_else(|e| e.into_inner())
                .take();
            if let Some(root) = root {
                let outcome = if failed {
                    opensip_operability::PhaseOutcome::Failed
                } else {
                    opensip_operability::PhaseOutcome::Completed
                };
                if let Err(error) = root.finish(outcome) {
                    self.record_phase_error(error);
                }
            }
        }
        #[cfg(not(any(feature = "operability-dev-sinks", feature = "harness-instrumentation")))]
        let _failed = failed;
        crate::finalize_invocation(false);
    }
    /// `true` when logging start failed and S-OP-6 will be the disclosure.
    pub fn logging_unavailable(&self) -> bool {
        self.logging_unavailable.is_some()
    }
    /// `true` when this host holds the capability set from the process's one `start`.
    pub fn holds_capability_set(&self) -> bool {
        self.capabilities.is_some()
    }
    /// J3a-o: the operational scope of this host's reserved request.
    /// No scope is lent when logging did not start for this host.
    pub fn logging_scope(
        &self,
        context: &RequestContext,
    ) -> Option<opensip_operability::RequestScope> {
        self.capabilities.as_ref()?;
        self.authority.logging_scope(context)
    }
    /// The projected request id of a context this host allocated.
    pub(crate) fn request_id(&self, context: &RequestContext) -> Result<String, MetadataError> {
        Ok(self
            .authority
            .project(context)
            .ok_or("request context does not belong to selected host")?)
    }
    /// C2PM-1/NIJ-1: project a new native input refusal before any Plan or Run.
    /// The owning admission boundary supplies the private, provenance-specific
    /// variant; this projection accepts neither caller identifiers nor origins.
    pub(crate) fn native_input_failure_projection(
        &self,
        context: &RequestContext,
        refusal: &NativeRefusal,
    ) -> Result<Envelope7Root, MetadataError> {
        let request_id = self.request_id(context)?;
        let remedy = refusal.input_remedy().ok_or(MetadataError::Projection)?;
        let termination = native(refusal);
        let exit_code = match termination.class {
            Class::RequestRejected => 2,
            Class::OperationalFailed => 4,
            _ => return Err(MetadataError::Projection),
        };
        let detail = json!({"code":refusal.envelope_detail().to_string(),
            "remedy":remedy,"subject":bounded_subject(&refusal.raw())});
        let mut step = json!({"class":termination.class.to_string(),
            "errorCode":termination.error_code.ok_or(MetadataError::Projection)?.to_string()});
        if termination.class == Class::OperationalFailed {
            step["faultCause"] = json!(termination.fault_cause.to_string());
        }
        if termination.detail.is_some() {
            step["domainDetail"] = detail.clone();
        }
        serde_json::from_value(json!({
            "schemaFamily":"opensip.product.envelope","schemaMajor":7,
            "kind":"failure","requestId":request_id,"termination":step,
            "exitCode":exit_code,"errors":[detail]
        }))
        .map_err(|_| MetadataError::Projection)
    }
    /// Required delivery failure before any Run exists, preserving this request.
    pub fn delivery_failure(
        &self,
        context: &RequestContext,
        format: Format,
    ) -> Result<RenderedResponse, MetadataError> {
        let request_id = self
            .authority
            .project(context)
            .ok_or("foreign request context")?;
        let detail = self.prepare_delivery(context, || Ok(json!({"code":"DELIVERY.REQUIRED_PROJECTION_FAILED","remedy":"Retry after resolving the output or projection failure."})))?;
        self.finish_logging(true);
        let projection:Envelope7Root=serde_json::from_value(json!({
            "schemaFamily":"opensip.product.envelope","schemaMajor":7,"kind":"failure","requestId":request_id,
            "termination":{"class":"operational-failed","errorCode":"DELIVERY.REQUIRED_FAILED","faultCause":"delivery-required","domainDetail":detail},
            "exitCode":4,"errors":[detail],"diagnostics":["Required output delivery failed."]
        })).map_err(|_|"delivery failure projection failed")?;
        let bytes = match format {
            Format::Json => opensip_reporting::render_json(&projection)
                .map_err(|_| MetadataError::Serialization)?,
            Format::Human => opensip_reporting::render_human(&projection)?,
        };
        Ok(RenderedResponse {
            bytes,
            exit_code: 4,
        })
    }
    pub fn execute(
        &self,
        context: &RequestContext,
        request: MetadataRequest,
        format: Format,
        correlation: Option<&str>,
        host_release: &'static str,
    ) -> Result<RenderedResponse, MetadataError> {
        let (envelope, completion_bytes) = self.prepare_delivery(context, || {
        let request_id = self
            .authority
            .project(context)
            .ok_or("request context does not belong to selected host")?;
        if correlation.is_some_and(|x| !(1..=128).contains(&x.chars().count())) {
            return Err(MetadataError::Projection);
        }
        let commands = catalogue()?;
        let mut envelope = json!({"schemaFamily":"opensip.product.envelope","schemaMajor":7,"kind":"meta","requestId":request_id,"termination":{"class":"success"},"exitCode":0});
        if let Some(value) = correlation {
            envelope["clientCorrelationId"] = json!(value);
        }
        let mut completion_bytes = None;
        match request {
            MetadataRequest::Help { topic } => {
                let selected = match &topic {
                    None => commands.clone(),
                    Some(name) => commands
                        .iter()
                        .filter(|row| row.name.to_string() == *name)
                        .cloned()
                        .collect(),
                };
                if selected.is_empty() {
                    reject(&mut envelope, "Unknown or unimplemented help topic.", false);
                } else {
                    envelope["meta"] = json!({"command":"help","topic":topic,"commands":selected});
                }
            }
            MetadataRequest::Version => {
                let build = opensip_reporting::development_metadata(host_release)?;
                envelope["meta"] = json!({"command":"version","hostRelease":build.host_release,"buildChannel":build.build_channel,"closureIds":build.closure_ids});
            }
            MetadataRequest::Completion { shell } => {
                if format == Format::Json {
                    reject(
                        &mut envelope,
                        "Completion supports human output only.",
                        true,
                    );
                } else if let Some(bytes) = opensip_reporting::completion(&shell, &commands) {
                    completion_bytes = Some(bytes);
                } else {
                    reject(
                        &mut envelope,
                        "Completion requires bash, zsh, or fish.",
                        false,
                    );
                }
            }
            MetadataRequest::Rejected { diagnostic } => reject(&mut envelope, diagnostic, false),
            MetadataRequest::FormatNotApplicable => reject(
                &mut envelope,
                "The selected format is not applicable to this command.",
                true,
            ),
        }
            Ok((envelope, completion_bytes))
        })?;
        self.finish_logging(false);
        if let Some(bytes) = completion_bytes {
            return Ok(RenderedResponse {
                bytes,
                exit_code: 0,
            });
        }
        let exit_code = if envelope["kind"] == "failure" { 2 } else { 0 };
        // This is construction from host-owned fields, not admission of caller
        // JSON. Original-schema conformance is checked independently in tests.
        let projection: Envelope7Root =
            serde_json::from_value(envelope).map_err(|_| "host metadata projection failed")?;
        let bytes = match format {
            Format::Human => opensip_reporting::render_human(&projection)?,
            Format::Json => opensip_reporting::render_json(&projection)
                .map_err(|_| MetadataError::Serialization)?,
        };
        Ok(RenderedResponse { bytes, exit_code })
    }
}
fn catalogue() -> Result<Vec<Metadata1HelpCommand>, &'static str> {
    serde_json::from_value(json!([
        {"name":"completion","usage":"opensip completion <bash|zsh|fish>","summary":"Print shell completion for implemented commands."},
        {"name":"doctor","usage":"opensip doctor [--format human|json]","summary":"Report the health of this account's OpenSIP installation."},
        {"name":"help","usage":"opensip help [command] [--format human|json]","summary":"Show help for implemented commands."},
        {"name":"version","usage":"opensip version [--format human|json]","summary":"Show the compiled host version and component selection."}
    ])).map_err(|_|"invalid compiled command catalogue")
}
fn reject(envelope: &mut Value, diagnostic: &str, format_detail: bool) {
    envelope["kind"] = json!("failure");
    envelope["exitCode"] = json!(2);
    envelope["termination"] =
        json!({"class":"request-rejected","errorCode":"REQUEST.UNKNOWN_OPTION"});
    envelope["diagnostics"] = json!([diagnostic]);
    envelope["errors"] = if format_detail {
        json!([{"code":"OUTPUT.FORMAT_NOT_APPLICABLE","remedy":"Choose an applicable output format."}])
    } else {
        json!([])
    };
}

#[cfg(test)]
mod logging_tests {
    use super::{Format, MetadataHost, MetadataRequest};

    fn contains(bytes: &[u8], needle: &[u8]) -> bool {
        bytes.windows(needle.len()).any(|window| window == needle)
    }

    #[test]
    fn help_envelope_has_no_logging_summary() {
        let mut host = MetadataHost::new();
        let context = host.begin().expect("request identity");
        assert!(!host.logging_unavailable());
        assert!(host.holds_capability_set());
        assert!(host.logging_scope(&context).is_some());
        let rendered = host
            .execute(
                &context,
                MetadataRequest::Help { topic: None },
                Format::Json,
                None,
                "0.0.0-test",
            )
            .expect("help");
        assert_eq!(rendered.exit_code, 0);
        assert!(
            contains(&rendered.bytes, b"\"kind\":\"meta\"")
                || contains(&rendered.bytes, b"\"kind\": \"meta\"")
        );
        assert!(!contains(&rendered.bytes, b"unpersisted"));
        assert!(!contains(&rendered.bytes, b"operability"));
        let mut second = MetadataHost::new();
        let second_context = second.begin().expect("second request");
        assert!(!second.holds_capability_set());
        assert!(second.logging_scope(&second_context).is_none());
        assert!(host.logging_scope(&second_context).is_none());
        assert!(second.logging_scope(&context).is_none());
        assert!(!second.logging_unavailable());
        let rejected = second
            .execute(
                &second_context,
                MetadataRequest::Rejected {
                    diagnostic: "no such command",
                },
                Format::Json,
                None,
                "0.0.0-test",
            )
            .expect("rejected");
        assert_eq!(rejected.exit_code, 2);
        assert!(!contains(&rejected.bytes, b"unpersisted"));
    }
}

// ===================================================================
// Law M3-J1 r5 item 10 (unit J2a): the M3 outcome matrix.
// ===================================================================
//
// NE section 10's deficiency-to-D9 bridge (NE:3364-3394), its route and
// origin tables (NE:3523-3575, with the bound successors SD-5 and SD-7 on
// NE:3539-3540) and item 10's total projection. Everything here is pure:
// no I/O, no lock, no ledger and no clock. Every row uses an existing D9
// class, error code, fault cause and detail; nothing is added (item 10).
// The projection is one exhaustive match with no wildcard arm (item 10,
// "Totality"; X7 item 8), so an observation without a row cannot compile.
//
// What is not here: the envelope's `errors` composition (WS:1340-1344) and
// every remedy but the two successor-selected ones below are the
// envelope's (J3d, J2c); rows 41 (S-OP-8), 45 (a disclosure beside the
// outcome), 48 (the settlement model in `invocation.rs`) and 50 (never a
// termination) have no observation; SD-5b's four refusals
// (`MemoryBudgetBelowCeiling`, `ToolOutputBound`, `ToolScratchBound`,
// `confinement-refused`) have no row yet (J1 S20; M3-D r5 item 29).

/// WS:1355-1356: the exit derives from the class by the fixed table only.
pub(crate) fn exit_code(class: Class) -> u8 {
    match class {
        Class::Success => 0,
        Class::PolicyFailed => 1,
        Class::RequestRejected => 2,
        Class::Indeterminate => 3,
        Class::OperationalFailed => 4,
        Class::Interrupted => 130,
    }
}

/// One public termination: item 10's columns. `fault_cause` is
/// `Fault::None` off the operational-failed class. `subject` is the
/// detail's, except on rows 38 and 39, where it is the ExecutionId as X7
/// item 3 projects it. `remedy` is set only where a bound successor makes
/// this projection select it (SD-5 LD-S5; SD-7). `namespace` is disclosed
/// beside the termination (rows 38 to 40). `operational` holds the internal
/// keys retained in the operational record, never in the envelope
/// (NE:3546-3555).
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct Termination {
    pub(crate) class: Class,
    pub(crate) error_code: Option<Code>,
    pub(crate) fault_cause: Fault,
    pub(crate) reason_codes: Vec<Reason>,
    pub(crate) detail: Option<Detail>,
    pub(crate) subject: Option<String>,
    pub(crate) remedy: Option<&'static str>,
    pub(crate) signal: Option<Signal>,
    pub(crate) run_id: Option<String>,
    pub(crate) execution_id: Option<String>,
    pub(crate) authority: Option<Authority>,
    pub(crate) coverage_id: Option<String>,
    pub(crate) namespace: Option<String>,
    pub(crate) operational: Vec<String>,
}
impl Termination {
    fn of(class: Class) -> Self {
        Self {
            class,
            error_code: None,
            fault_cause: Fault::None,
            reason_codes: Vec::new(),
            detail: None,
            subject: None,
            remedy: None,
            signal: None,
            run_id: None,
            execution_id: None,
            authority: None,
            coverage_id: None,
            namespace: None,
            operational: Vec::new(),
        }
    }
    fn rejected(code: Code, detail: Option<Detail>, subject: Option<String>) -> Self {
        Self {
            error_code: Some(code),
            detail,
            subject,
            ..Self::of(Class::RequestRejected)
        }
    }
    fn failed(code: Code, fault: Fault, detail: Option<Detail>) -> Self {
        Self {
            error_code: Some(code),
            fault_cause: fault,
            detail,
            ..Self::of(Class::OperationalFailed)
        }
    }
    fn keyed(mut self, key: String) -> Self {
        self.operational.push(key);
        self
    }
    /// `success`, carrying nothing.
    pub(crate) fn success() -> Self {
        Self::of(Class::Success)
    }
    /// The exit, from the class by the fixed table only.
    pub(crate) fn exit(&self) -> u8 {
        exit_code(self.class)
    }
    /// `interrupted` 130 with its signal (rows 46 and 47). A runId only
    /// where a Run was committed before the interrupt (WS:224-227).
    pub(crate) fn interrupted(signal: Signal, run_id: Option<String>) -> Self {
        Self {
            signal: Some(signal),
            run_id,
            ..Self::of(Class::Interrupted)
        }
    }
}
/// An owner's row, lifted unchanged: the exit of `InstallationTerminationV1`
/// already derives from its class by the same table.
impl From<InstallationTerminationV1> for Termination {
    fn from(row: InstallationTerminationV1) -> Self {
        Self {
            error_code: Some(row.error_code),
            fault_cause: row.fault_cause,
            detail: row.detail,
            subject: row.subject,
            ..Self::of(row.class)
        }
    }
}

// ------------------------------------------------- the deficiency bridge

/// NE section 10 (NE:3380-3394): native owns only the bridge into the D9
/// deficiency vocabulary. The five `DeficiencyV2` members that are also
/// D9 members map to themselves; the other four map to
/// `verdict-indeterminate`. Total over the nine members.
pub(crate) fn native_deficiency_d9(deficiency: NativeDeficiency) -> D9Deficiency {
    match deficiency {
        NativeDeficiency::LanguageTierUnsupported => D9Deficiency::LanguageTierUnsupported,
        NativeDeficiency::ProviderUnavailable => D9Deficiency::ProviderUnavailable,
        NativeDeficiency::BudgetExhausted => D9Deficiency::BudgetExhausted,
        NativeDeficiency::ConfidenceFloorUnmet => D9Deficiency::ConfidenceFloorUnmet,
        NativeDeficiency::RequiredRelationMissing => D9Deficiency::RequiredRelationMissing,
        NativeDeficiency::InputClosureIncomplete
        | NativeDeficiency::DerivationPolicyUnmet
        | NativeDeficiency::ResolutionIncomplete
        | NativeDeficiency::ExternalConsumersUnknown => D9Deficiency::VerdictIndeterminate,
    }
}

/// D9's `codeMaps.deficiencyToReasonCode`, total and injective over the
/// deficiencies that terminate; `none` names nothing deficient.
pub(crate) fn reason_code(deficiency: D9Deficiency) -> Option<Reason> {
    Some(match deficiency {
        D9Deficiency::None => return None,
        D9Deficiency::RequiredRelationMissing => Reason::CoverageRequiredRelationMissing,
        D9Deficiency::ProviderUnavailable => Reason::CoverageProviderUnavailable,
        D9Deficiency::LanguageTierUnsupported => Reason::CoverageLanguageTierUnsupported,
        D9Deficiency::BudgetExhausted => Reason::CoverageBudgetExhausted,
        D9Deficiency::ConfidenceFloorUnmet => Reason::CoverageConfidenceFloorUnmet,
        D9Deficiency::ConvergenceExhausted => Reason::SnapshotConvergenceExhausted,
        D9Deficiency::BaselineRecipeUnsupported => Reason::BaselineRecipeUnsupported,
        D9Deficiency::VerdictIndeterminate => Reason::VerdictIndeterminate,
        D9Deficiency::QueryCompletenessUnmet => Reason::QueryCompletenessUnmet,
    })
}

/// A Run's ordered D9 deficiencies: the primary, then the secondaries in
/// rank order, all distinct and none `none` (run-termination contract §4,
/// which owns the order). Its reason codes are the D9 map of that sequence.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct Deficiencies(Vec<D9Deficiency>);
impl Deficiencies {
    /// `None` for `none` or a repeated deficiency: neither has a lawful
    /// reason sequence (`reasonCodes` is unique and names a deficiency).
    pub(crate) fn new(primary: D9Deficiency, secondary: &[D9Deficiency]) -> Option<Self> {
        let mut all = vec![primary];
        for deficiency in secondary {
            if all.contains(deficiency) {
                return None;
            }
            all.push(*deficiency);
        }
        all.iter()
            .all(|deficiency| reason_code(*deficiency).is_some())
            .then_some(Self(all))
    }
    pub(crate) fn primary(&self) -> D9Deficiency {
        self.0[0]
    }
    fn reason_codes(&self) -> Vec<Reason> {
        self.0.iter().filter_map(|d| reason_code(*d)).collect()
    }
}

// ---------------------------------------------- the analysis projection

/// Run-termination contract §7.5's closed analysis detail allowlist, as the
/// composition selects it for a committed indeterminate Run. Only that
/// composition chooses the member; this projection carries it.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum AnalysisDetail {
    /// Row 1: `EVALUATION.WORK_BUDGET_EXHAUSTED` (J1 row 33).
    WorkBudgetExhausted,
    /// Row 2: `COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED` (J1 row 27).
    RequiredClosureNotInstalled,
    /// Row 3: the named record's own entry deficiency.
    BudgetExhaustedEntry,
    DerivationPolicyUnmet,
    ExternalConsumersUnknown,
    InputClosureIncomplete,
    ResolutionIncomplete,
}
impl AnalysisDetail {
    fn code(self) -> Detail {
        match self {
            Self::WorkBudgetExhausted => Detail::EvaluationWorkBudgetExhausted,
            Self::RequiredClosureNotInstalled => Detail::ComponentRequiredClosureNotInstalled,
            Self::BudgetExhaustedEntry => Detail::BudgetExhausted,
            Self::DerivationPolicyUnmet => Detail::DerivationPolicyUnmet,
            Self::ExternalConsumersUnknown => Detail::ExternalConsumersUnknown,
            Self::InputClosureIncomplete => Detail::InputClosureIncomplete,
            Self::ResolutionIncomplete => Detail::ResolutionIncomplete,
        }
    }
}

/// A committed Run's sealed verdict (rows 27, 31, 33 and 35).
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) enum Verdict {
    Pass,
    Fail,
    Indeterminate {
        deficiencies: Deficiencies,
        coverage_id: Option<String>,
        detail: Option<AnalysisDetail>,
    },
}
/// An ephemeral attempt's verdict. It carries no detail, coverage record
/// or Run (run-termination contract §7.4).
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) enum EphemeralVerdict {
    Pass,
    Fail,
    Indeterminate { deficiencies: Deficiencies },
}
/// What the analysis step's attempt produced when it ended with a verdict.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) enum AnalysisOutcome {
    /// A committed Run: its runId, and no authority (§7.4).
    Committed { run_id: String, verdict: Verdict },
    /// An ephemeral result: `authority: ephemeral`, never a runId (WS:242-248).
    Ephemeral(EphemeralVerdict),
}
impl AnalysisOutcome {
    /// The committed Run, if one exists.
    pub(crate) fn run_id(&self) -> Option<&str> {
        match self {
            Self::Committed { run_id, .. } => Some(run_id),
            Self::Ephemeral(_) => None,
        }
    }
}
fn analysis(outcome: &AnalysisOutcome) -> Termination {
    match outcome {
        AnalysisOutcome::Committed { run_id, verdict } => {
            let mut t = match verdict {
                Verdict::Pass => Termination::of(Class::Success),
                Verdict::Fail => Termination::of(Class::PolicyFailed),
                Verdict::Indeterminate {
                    deficiencies,
                    coverage_id,
                    detail,
                } => Termination {
                    reason_codes: deficiencies.reason_codes(),
                    coverage_id: coverage_id.clone(),
                    detail: detail.map(AnalysisDetail::code),
                    ..Termination::of(Class::Indeterminate)
                },
            };
            t.run_id = Some(run_id.clone());
            t
        }
        AnalysisOutcome::Ephemeral(verdict) => {
            let mut t = match verdict {
                EphemeralVerdict::Pass => Termination::of(Class::Success),
                EphemeralVerdict::Fail => Termination::of(Class::PolicyFailed),
                EphemeralVerdict::Indeterminate { deficiencies } => Termination {
                    reason_codes: deficiencies.reason_codes(),
                    ..Termination::of(Class::Indeterminate)
                },
            };
            t.authority = Some(Authority::Ephemeral);
            t
        }
    }
}

// ------------------------------------------- the route and origin tables

/// The originating boundary of a capability-request key (NE:3557-3575;
/// NES `x-opensip-public-route-registry`): who supplied the bad value.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum SpecOrigin {
    /// A capability the user configured (Config2 or CLI): `CONFIG.INVALID`.
    ExternalConfiguration,
    /// An externally supplied or retained spec of known external origin.
    ExternallySuppliedSpec,
    /// A host bug minting its own invalid internal layer.
    HostGeneratedInternalLayer,
}

/// The analysis spec's capability-request keys (row 26). Each may arise at
/// every `SpecOrigin`, so no impossible origin is representable.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum RequestedCapabilityKey {
    Unregistered,
    ModeUnregistered,
    DuplicateOwnershipTuple,
    /// The well-formed request for a `NOT-SELECTED` cell: origin-independent.
    ModeNotSelected,
}
/// The authenticated release declaration's keys (row 55). Their only
/// possible origin is the authenticated release declaration.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum ReleaseDeclarationKey {
    Unregistered,
    ModeUnregistered,
    ModeNotSelected,
    Duplicate,
    PreviewConstant,
}
/// The producer boundary's Coverage cause and carrier keys (row 32). Their
/// only possible origin is the producer boundary.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum CoverageCauseKey {
    Required,
    MustBeNull,
    NotForDeficiency,
    CarrierUnsupported,
    RelationNotInScope,
    WithoutDeficiency,
    RegistryRowMissing,
}

/// One refusal of the closed public route registry: its key, the origin the
/// host holds (only where the key can arise at more than one), and the
/// guard's colon suffix, which names the refused value.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum ClosureProtocolKey {
    AnalyzerMismatch,
    DeclarationMissing,
    DescriptorMismatch,
    Unsupported,
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum ClosureProtocolOrigin {
    AuthenticatedReleaseDeclaration,
    ExternallySuppliedSpec,
    HostGeneratedInternalLayer,
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum NativeImportKey {
    SelfReference,
    AcquisitionPath,
    JoinMissing,
    JoinAmbiguous,
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum NativeImportOrigin {
    ExternallySuppliedSpec,
    HostGeneratedInternalLayer,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) enum NativeRefusal {
    ClosureProtocol {
        key: ClosureProtocolKey,
        origin: ClosureProtocolOrigin,
        suffix: Option<String>,
    },
    NativeImport {
        key: NativeImportKey,
        origin: NativeImportOrigin,
        suffix: Option<String>,
    },
    /// Only this NIJ-1 key may originate at external configuration.
    ConfiguredNativeImport {
        origin: SpecOrigin,
        suffix: Option<String>,
    },
    RequestedCapability {
        key: RequestedCapabilityKey,
        origin: SpecOrigin,
        suffix: Option<String>,
    },
    ReleaseDeclaration {
        key: ReleaseDeclarationKey,
        suffix: Option<String>,
    },
    CoverageCause {
        key: CoverageCauseKey,
        suffix: Option<String>,
    },
}
impl NativeRefusal {
    /// The registered internal key, spelled as the registry spells it.
    pub(crate) fn key(&self) -> &'static str {
        match self {
            Self::ClosureProtocol { key, .. } => match key {
                ClosureProtocolKey::AnalyzerMismatch => "native.closure-protocol-analyzer-mismatch",
                ClosureProtocolKey::DeclarationMissing => {
                    "native.closure-protocol-declaration-missing"
                }
                ClosureProtocolKey::DescriptorMismatch => {
                    "native.closure-protocol-descriptor-mismatch"
                }
                ClosureProtocolKey::Unsupported => "native.closure-protocol-unsupported",
            },
            Self::NativeImport { key, .. } => match key {
                NativeImportKey::SelfReference => "native.input-import-self-reference",
                NativeImportKey::AcquisitionPath => "native.input-import-acquisition-path",
                NativeImportKey::JoinMissing => "native.input-import-join-missing",
                NativeImportKey::JoinAmbiguous => "native.input-import-join-ambiguous",
            },
            Self::ConfiguredNativeImport { .. } => "native.input-import-configured",
            Self::RequestedCapability { key, .. } => match key {
                RequestedCapabilityKey::Unregistered => "native.requested-capability-unregistered",
                RequestedCapabilityKey::ModeUnregistered => {
                    "native.requested-capability-mode-unregistered"
                }
                RequestedCapabilityKey::DuplicateOwnershipTuple => {
                    "native.requested-capability-duplicate-ownership-tuple"
                }
                RequestedCapabilityKey::ModeNotSelected => {
                    "native.requested-capability-mode-not-selected"
                }
            },
            Self::ReleaseDeclaration { key, .. } => match key {
                ReleaseDeclarationKey::Unregistered => "native.release-capability-unregistered",
                ReleaseDeclarationKey::ModeUnregistered => {
                    "native.release-capability-mode-unregistered"
                }
                ReleaseDeclarationKey::ModeNotSelected => {
                    "native.release-capability-mode-not-selected"
                }
                ReleaseDeclarationKey::Duplicate => "native.release-capability-duplicate",
                ReleaseDeclarationKey::PreviewConstant => {
                    "native.release-capability-preview-constant"
                }
            },
            Self::CoverageCause { key, .. } => match key {
                CoverageCauseKey::Required => "native.coverage-cause-required",
                CoverageCauseKey::MustBeNull => "native.coverage-cause-must-be-null",
                CoverageCauseKey::NotForDeficiency => "native.coverage-cause-not-for-deficiency",
                CoverageCauseKey::CarrierUnsupported => "native.coverage-cause-carrier-unsupported",
                CoverageCauseKey::RelationNotInScope => {
                    "native.coverage-cause-relation-not-in-scope"
                }
                CoverageCauseKey::WithoutDeficiency => "native.coverage-cause-without-deficiency",
                CoverageCauseKey::RegistryRowMissing => {
                    "native.coverage-cause-registry-row-missing"
                }
            },
        }
    }
    fn suffix(&self) -> Option<&str> {
        match self {
            Self::ClosureProtocol { suffix, .. }
            | Self::NativeImport { suffix, .. }
            | Self::ConfiguredNativeImport { suffix, .. }
            | Self::RequestedCapability { suffix, .. }
            | Self::ReleaseDeclaration { suffix, .. }
            | Self::CoverageCause { suffix, .. } => suffix.as_deref(),
        }
    }
    /// The raw guard string: the key, then `:` and the suffix where one is.
    fn raw(&self) -> String {
        match self.suffix() {
            Some(suffix) => format!("{}:{suffix}", self.key()),
            None => self.key().to_owned(),
        }
    }
    /// The registry's `envelopeDetail`: the detail the failure envelope's
    /// `errors` carries where the termination carries none (NES
    /// `envelopeErrorsComposition`). Where the termination carries a detail
    /// it is that detail.
    pub(crate) fn envelope_detail(&self) -> Detail {
        match self {
            Self::ClosureProtocol { origin, .. } => match origin {
                ClosureProtocolOrigin::HostGeneratedInternalLayer => Detail::HostInvariantViolated,
                _ => Detail::NativeClosureProtocolInvalid,
            },
            Self::NativeImport { origin, .. } => match origin {
                NativeImportOrigin::HostGeneratedInternalLayer => Detail::HostInvariantViolated,
                NativeImportOrigin::ExternallySuppliedSpec => Detail::NativeInputImportInvalid,
            },
            Self::ConfiguredNativeImport { origin, .. } => match origin {
                SpecOrigin::HostGeneratedInternalLayer => Detail::HostInvariantViolated,
                _ => Detail::NativeInputImportInvalid,
            },
            Self::RequestedCapability { key, origin, .. } => match (key, origin) {
                (RequestedCapabilityKey::ModeNotSelected, _) => Detail::ProviderNotSelected,
                (_, SpecOrigin::ExternalConfiguration) => Detail::ConfigInvalid,
                (_, SpecOrigin::ExternallySuppliedSpec) => Detail::NativeCapabilitySpecInvalid,
                (_, SpecOrigin::HostGeneratedInternalLayer) => Detail::HostInvariantViolated,
            },
            Self::ReleaseDeclaration { .. } => Detail::NativeReleaseDeclarationInvalid,
            Self::CoverageCause { .. } => Detail::NativeCoverageCauseUnsupported,
        }
    }
    fn input_remedy(&self) -> Option<&'static str> {
        match self {
            Self::ClosureProtocol { .. }
            | Self::NativeImport { .. }
            | Self::ConfiguredNativeImport { .. } => Some(match self.envelope_detail() {
                Detail::NativeClosureProtocolInvalid => {
                    "Select a component release with a signed role-supported closure protocol declaration consistent with its required joins; for a retained descriptor mismatch, supply the descriptor projected from that signed body. Never patch retained signed bytes."
                }
                Detail::NativeInputImportInvalid => {
                    "Supply an admitted inert native import with null payload self references and acquisitionSourcePath, selected through exactly one matching context identity join; remove native imports from configuration evidence.importIds. Never patch retained historical bytes."
                }
                Detail::HostInvariantViolated => {
                    "the host produced an invalid internal record; report the defect with the retained diagnostic"
                }
                _ => unreachable!("closed native input route"),
            }),
            _ => None,
        }
    }
}

/// NES `subjectBoundLaw`: `DomainDetail.subject` is BoundedText (1024 code
/// points). A longer subject keeps a leading window, the ASCII marker and
/// the SHA-256 of the whole subject's UTF-8 bytes, exactly 1024 code points.
pub(crate) fn bounded_subject(raw: &str) -> String {
    const MAX: usize = 1024;
    const MARKER: &str = "...#sha256:";
    if raw.chars().count() <= MAX {
        return raw.to_owned();
    }
    let digest = opensip_identity::digest_hex(&opensip_identity::raw_sha256(raw.as_bytes()));
    let keep = MAX - MARKER.len() - digest.len();
    let mut subject: String = raw.chars().take(keep).collect();
    subject.push_str(MARKER);
    subject.push_str(&digest);
    subject
}

/// NE section 10's route of one registry refusal (`public_termination_for`):
/// a detail only where an existing member names the condition, its subject
/// the bounded raw guard string; otherwise no detail, and the raw string
/// goes to the operational record.
fn native(refusal: &NativeRefusal) -> Termination {
    let raw = refusal.raw();
    let with_detail =
        |code, detail| Termination::rejected(code, Some(detail), Some(bounded_subject(&raw)));
    match refusal {
        NativeRefusal::ClosureProtocol { origin, .. } => match origin {
            ClosureProtocolOrigin::HostGeneratedInternalLayer => {
                Termination::failed(Code::SystemOutcomeIllegalState, Fault::HostInvariant, None)
                    .keyed(raw)
            }
            _ => Termination::rejected(Code::RequestPreconditionFailed, None, None).keyed(raw),
        },
        NativeRefusal::NativeImport { origin, .. } => match origin {
            NativeImportOrigin::HostGeneratedInternalLayer => {
                Termination::failed(Code::SystemOutcomeIllegalState, Fault::HostInvariant, None)
                    .keyed(raw)
            }
            NativeImportOrigin::ExternallySuppliedSpec => {
                Termination::rejected(Code::RequestPreconditionFailed, None, None).keyed(raw)
            }
        },
        NativeRefusal::ConfiguredNativeImport { origin, .. } => match origin {
            SpecOrigin::ExternalConfiguration => Termination {
                remedy: refusal.input_remedy(),
                ..with_detail(Code::ConfigInvalid, Detail::NativeInputImportInvalid)
            }
            .keyed(raw),
            SpecOrigin::ExternallySuppliedSpec => {
                Termination::rejected(Code::RequestPreconditionFailed, None, None).keyed(raw)
            }
            SpecOrigin::HostGeneratedInternalLayer => {
                Termination::failed(Code::SystemOutcomeIllegalState, Fault::HostInvariant, None)
                    .keyed(raw)
            }
        },
        NativeRefusal::RequestedCapability { key, origin, .. } => match (key, origin) {
            (RequestedCapabilityKey::ModeNotSelected, _) => Termination {
                remedy: Some(REMEDY_PROVIDER_NOT_SELECTED),
                ..with_detail(Code::RequestUnsatisfiable, Detail::ProviderNotSelected)
            },
            (_, SpecOrigin::ExternalConfiguration) => {
                with_detail(Code::ConfigInvalid, Detail::ConfigInvalid)
            }
            (_, SpecOrigin::ExternallySuppliedSpec) => {
                Termination::rejected(Code::RequestPreconditionFailed, None, None).keyed(raw)
            }
            (_, SpecOrigin::HostGeneratedInternalLayer) => {
                Termination::failed(Code::SystemOutcomeIllegalState, Fault::HostInvariant, None)
                    .keyed(raw)
            }
        },
        NativeRefusal::ReleaseDeclaration { .. } => {
            Termination::rejected(Code::RequestPreconditionFailed, None, None).keyed(raw)
        }
        NativeRefusal::CoverageCause { .. } => Termination::failed(
            Code::ProviderProtocolViolation,
            Fault::ProviderProtocol,
            None,
        )
        .keyed(raw),
    }
}

/// `PROVIDER.NOT_SELECTED`'s code-keyed remedy, as contract successor SD-7
/// widened it (both native-model copies, line 1159): true for the
/// `NOT-SELECTED` cell and for the three request-class excluded forms.
pub(crate) const REMEDY_PROVIDER_NOT_SELECTED: &str = "this capability is not selected for that language mode, or the request asks for an external discovery or public-lifecycle endpoint, untrusted native or WASM admission, or network-granted analysis; no promise is made for it; restate the request without it";
/// NE section 10's excluded-form row (SD-5, conformed by SD-7): the one
/// remedy this projection selects by the `excluded-form:` subject (SD-5
/// LD-S5).
pub(crate) const REMEDY_EXCLUDED_MANIFEST: &str = "This installed component is a form OpenSIP never admits. Only first-party or explicitly trusted components are admitted, and none may claim policy, persistence, rendering, termination or host-lifecycle authority, run untrusted native or WASM code, or claim a project hook, a reserved or additional root command, or a probe. Remove the component, or install its first-party release.";
/// `native.typescript-config-unresolved`'s remedy, keyed by that public
/// detail (M3-B r8 item 14a; contract successor S10, as S10b rewrites its
/// bounds clause for M3-B r10: the `PUBLIC_ROUTE_REMEDIES` entry of both
/// S10b native-model copies). One
/// string is true for its four internal keys: an unresolved `extends`
/// base, a cycle, a bound and a malformed file. Its D9 code is
/// `CONFIG.INVALID`, whose own remedy does not apply. B2-c2's refusal
/// carries it (row 59, `Observation::TypescriptConfigUnresolved`).
pub(crate) const REMEDY_TYPESCRIPT_CONFIG_UNRESOLVED: &str = "the TypeScript configuration could not be read before the Plan: make every extends base of the named configuration file present as a regular file inside the project, named by a well-formed ./ or ../ relative path or a lower-case package name, with no symbolic link the snapshot does not admit on its path, installing its package outside OpenSIP if needed; break any extends cycle; keep each file within 64 KiB and 64 extends entries, each configuration file path within 4,096 characters, and the graph within 32 files; or correct the file's syntax, so that it is JSONC with extends a string or an array of strings and allowJs and checkJs booleans";
/// Row 1's one fixed standard-error line (`bootstrap.rs:17-23`).
pub(crate) const LINE_REQUEST_IDENTITY: &str =
    "HOST.IO_FAILURE: request identity allocation failed.";

// --------------------------------------------------- the excluded forms

/// DR-117's manifest-class excluded forms (M3-D r5 item 24), in the order
/// SD-5's row names them.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub(crate) enum ManifestExcludedClass {
    Ee1,
    Ee3b,
    Ee4,
    Ee5a,
}
/// DR-117's request-class excluded forms (M3-D r5 item 25), in the order
/// SD-7's row names them.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub(crate) enum RequestExcludedClass {
    Ee2,
    /// EE-4's request part.
    Ee4,
    Ee6a,
}
impl ManifestExcludedClass {
    fn spelling(self) -> &'static str {
        match self {
            Self::Ee1 => "EE-1",
            Self::Ee3b => "EE-3b",
            Self::Ee4 => "EE-4",
            Self::Ee5a => "EE-5a",
        }
    }
}
impl RequestExcludedClass {
    fn spelling(self) -> &'static str {
        match self {
            Self::Ee2 => "EE-2",
            Self::Ee4 => "EE-4",
            Self::Ee6a => "EE-6a",
        }
    }
}
/// A component manifest's identity, `closure.manifestDigest`: exactly 64
/// lowercase hex, so the subject is at most 84 characters (SD-5 LD-S4).
#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord)]
pub(crate) struct ManifestDigest(String);
impl ManifestDigest {
    pub(crate) fn parse(text: &str) -> Option<Self> {
        (text.len() == 64
            && text
                .bytes()
                .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b)))
        .then(|| Self(text.to_owned()))
    }
}
/// One manifest-class `ExcludedForm {class, subject}` from R10a or ER10a.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct ExcludedManifest {
    pub(crate) class: ManifestExcludedClass,
    pub(crate) manifest_digest: ManifestDigest,
}
impl ExcludedManifest {
    fn subject(&self) -> String {
        format!(
            "excluded-form:{}:{}",
            self.class.spelling(),
            self.manifest_digest.0
        )
    }
}

/// Row 56 (SD-5, conformed by SD-7): the least `manifestDigest`, then its
/// first class in table order, names the one detail; every refusal goes to
/// the operational record. No runId or executionId.
fn excluded_manifests(first: &ExcludedManifest, rest: &[ExcludedManifest]) -> Termination {
    let mut all: Vec<&ExcludedManifest> = std::iter::once(first).chain(rest).collect();
    all.sort_by(|a, b| (&a.manifest_digest, a.class).cmp(&(&b.manifest_digest, b.class)));
    all.dedup();
    Termination {
        remedy: Some(REMEDY_EXCLUDED_MANIFEST),
        operational: all.iter().map(|refusal| refusal.subject()).collect(),
        ..Termination::rejected(
            Code::ExtensionAdmissionRejected,
            Some(Detail::PayloadNotAdmissible),
            Some(all[0].subject()),
        )
    }
}
/// Row 57 (M3-D r5 item 25; SD-7's NE:3539 row): the first class in table
/// order names the one detail, with `PROVIDER.NOT_SELECTED`'s widened
/// remedy; every refusal goes to the operational record.
fn excluded_requests(first: RequestExcludedClass, rest: &[RequestExcludedClass]) -> Termination {
    let mut all: Vec<RequestExcludedClass> =
        std::iter::once(first).chain(rest.iter().copied()).collect();
    all.sort();
    all.dedup();
    let subject = |class: &RequestExcludedClass| format!("excluded-form:{}", class.spelling());
    Termination {
        remedy: Some(REMEDY_PROVIDER_NOT_SELECTED),
        operational: all.iter().map(subject).collect(),
        ..Termination::rejected(
            Code::RequestUnsatisfiable,
            Some(Detail::ProviderNotSelected),
            Some(subject(&all[0])),
        )
    }
}

// ------------------------------------------------------ the observations

/// The stale or non-inert selected rows of row 25 (NE:3525).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum StaleRow {
    PreparedOutput,
    Import,
    PreparedOutputNotInert,
}

/// One typed boundary observation, a row family of item 10. Each variant
/// names its rows; owners that already project their rows exhaustively are
/// lifted unchanged (`installation_termination`, X12's and X5's routes).
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) enum Observation {
    /// Row 2: a malformed host-built request or step list, NE:3573's
    /// host-generated internal layer. The key goes to the operational
    /// record. M3-D r5 item 22's `session-spec-inconsistent` takes it too.
    HostSpecInvalid { key: String },
    /// Rows 3 to 11, 15 to 19 and 37: 468's item 6 rows, X2's, X3a's,
    /// X4T's, X4's and X3d's, through their exhaustive projection.
    Installation(Row),
    /// Row 12: project or local carrier custody (M3B:97, :151-152).
    CarrierCustody { subject: String },
    /// Row 12: invalid external configuration.
    ConfigurationInvalid { subject: Option<String> },
    /// Rows 13 and 29: an invalid compiled default or host-built flags
    /// layer; a Plan that fails `check_plan_pack` or the structural
    /// enumeration admission.
    HostInvariant { subject: Option<String> },
    /// Row 14: X12's pack rows, through X12's projection.
    PolicySelection(PolicySelectionRefusal),
    /// Row 20: workspace-unit excess.
    WorkspaceUnitLimit { subject: String },
    /// Row 21: the discovery or snapshot ledger exhausted.
    WorkBudgetExhausted,
    /// Row 22: a bound of 5.4c or a selection array, `field:count>limit`.
    ScopeLimit { subject: String },
    /// Row 23: host I/O during capture or discovery; M3-D r5 item 22's
    /// `host-fault` on a channel, scratch or exit source.
    HostIo,
    /// Row 24: an explicit root without a marker.
    ExplicitRootWithoutMarker { subject: Option<String> },
    /// Row 24: an explicit root path that is invalid.
    ExplicitPathInvalid { subject: Option<String> },
    /// Row 25: the discovery inventory mismatch.
    DiscoveryInventoryMismatch,
    /// Row 25: a stale or non-inert import or prepared row.
    Stale(StaleRow),
    /// Rows 26, 32 (cause and carrier) and 55: the route registry.
    Native(NativeRefusal),
    /// Row 28: installed closure bytes corrupt; M3-D r5 item 22's
    /// `closure-recheck-failed`.
    ClosureBytesCorrupt,
    /// Row 28: the closure is unspawnable; item 22's `spawn-failed`.
    ClosureUnspawnable,
    /// Rows 30 and 32 (contradictory completeness): a worker or protocol
    /// fault, and M3-D r5 item 22's provider-spoken or process settlements
    /// (`provider-protocol` to `handshake-deadline`). The key goes to the
    /// operational record.
    ProviderProtocol { key: String },
    /// Rows 27, 31, 33 and 35: the attempt's verdict.
    Analysis(AnalysisOutcome),
    /// Row 34: the evaluation output bound. Evaluation precedes the commit,
    /// so no Run exists.
    OutputBoundExceeded,
    /// Row 36: a replay refusal, as X5's `replay_termination` projects it.
    Replay(InstallationTerminationV1),
    /// Row 38: `CommitUndetermined` in any phase. The ExecutionId is the
    /// subject and the namespace is disclosed beside.
    CommitUndetermined {
        execution_id: String,
        namespace: String,
    },
    /// Row 39: `ExistingAttempt`, lawfully impossible.
    ExistingAttempt {
        execution_id: String,
        namespace: String,
    },
    /// Row 40: carrier capacity exhausted.
    CarrierCapacityExhausted { namespace: String },
    /// Row 42: `Committed(PublishedCommit)` with `latchedAfterAdmission`,
    /// selected by the returned outcome (8.3, rule 2).
    LatchedAfterAdmission { run_id: String },
    /// Rows 43 and 44: the required projection, renderer or output failed.
    /// The route follows the committed evidence: with a `PublishedCommit`,
    /// F16 and its runId; without one, WS:1377's row and no runId.
    RequiredDeliveryFailed { committed_run: Option<String> },
    /// Rows 46 and 47: a signal before settlement, phase A, B or D.
    Interrupted {
        signal: Signal,
        run_id: Option<String>,
    },
    /// Row 49 before FinalGate admission (`host_panic`).
    HostPanicBeforeAdmission,
    /// Row 51: `--ephemeral` with an authority prerequisite.
    EphemeralCannotSupplyAuthority,
    /// Row 52: a native context or universe binding refused, before the
    /// PlanId. The key goes to the operational record.
    NativeContextRefused { key: String },
    /// Row 53: the preparation bound (M5's).
    PrepareBoundExceeded,
    /// Row 54: ambient Cargo configuration or an environment override.
    AmbientCargoConfig,
    /// Row 56: manifest-class excluded forms from R10a or ER10a.
    ExcludedManifests {
        first: ExcludedManifest,
        rest: Vec<ExcludedManifest>,
    },
    /// Row 57: request-class excluded forms from R1.
    ExcludedRequest {
        first: RequestExcludedClass,
        rest: Vec<RequestExcludedClass>,
    },
    /// Row 59 (M3-J1 r7; M3-B r8 item 14a): the pre-Plan TypeScript
    /// configuration graph could not be read. The subject is the internal
    /// key and the configuration file's project-relative path.
    TypescriptConfigUnresolved(ConfigRefusal),
}

/// Row 1: RequestId allocation failed. There is no envelope: exit 4 and
/// one fixed standard-error line (`bootstrap.rs:17-23`).
pub(crate) fn request_identity_unallocated() -> (u8, &'static str) {
    (4, LINE_REQUEST_IDENTITY)
}
/// Row 49: a host panic. Before FinalGate admission, where the
/// termination layer is reachable after unwinding, it is the host-invariant
/// row; after it, no outcome is manufactured and the recovery evidence
/// stands (OPP:296-297; X3D:213).
pub(crate) fn host_panic(after_final_gate_admission: bool) -> Option<Termination> {
    (!after_final_gate_admission).then(|| project(&Observation::HostPanicBeforeAdmission))
}

/// Item 10's total projection: one exhaustive match, no wildcard arm.
/// Rows 1 and 49 after admission have no termination
/// (`request_identity_unallocated`, `host_panic`).
pub(crate) fn project(observation: &Observation) -> Termination {
    use Observation as O;
    let host_invariant = |subject: Option<String>| Termination {
        subject,
        ..Termination::failed(
            Code::SystemOutcomeIllegalState,
            Fault::HostInvariant,
            Some(Detail::HostInvariantViolated),
        )
    };
    match observation {
        O::HostSpecInvalid { key } => {
            Termination::failed(Code::SystemOutcomeIllegalState, Fault::HostInvariant, None)
                .keyed(key.clone())
        }
        O::Installation(row) => installation_termination(row).into(),
        O::CarrierCustody { subject } => Termination::rejected(
            Code::ConfigInvalid,
            Some(Detail::ConfigCustodyRefused),
            Some(subject.clone()),
        ),
        O::ConfigurationInvalid { subject } => Termination::rejected(
            Code::ConfigInvalid,
            Some(Detail::ConfigInvalid),
            subject.clone(),
        ),
        O::HostInvariant { subject } => host_invariant(subject.clone()),
        O::PolicySelection(refusal) => policy_selection_termination(refusal).into(),
        O::WorkspaceUnitLimit { subject } => Termination::rejected(
            Code::RequestUnsatisfiable,
            Some(Detail::ProjectWorkspaceUnitLimit),
            Some(subject.clone()),
        ),
        O::WorkBudgetExhausted => Termination::failed(
            Code::SystemOutcomeIllegalState,
            Fault::HostInvariant,
            Some(Detail::WorkBudgetExhausted),
        ),
        O::ScopeLimit { subject } => Termination::rejected(
            Code::RequestUnsatisfiable,
            Some(Detail::ProjectScopeLimit),
            Some(subject.clone()),
        ),
        O::HostIo => Termination::failed(Code::HostIoFailure, Fault::HostIo, None),
        O::ExplicitRootWithoutMarker { subject } => Termination::rejected(
            Code::ConfigInvalid,
            Some(Detail::NativeExplicitRootWithoutMarker),
            subject.clone(),
        ),
        O::ExplicitPathInvalid { subject } => Termination::rejected(
            Code::ConfigInvalid,
            Some(Detail::ProjectExplicitPathInvalid),
            subject.clone(),
        ),
        O::DiscoveryInventoryMismatch => Termination::rejected(
            Code::RequestPreconditionFailed,
            Some(Detail::ProjectDiscoveryInventoryMismatch),
            None,
        ),
        O::Stale(row) => Termination::rejected(
            Code::RequestPreconditionFailed,
            Some(match row {
                StaleRow::PreparedOutput => Detail::NativeStalePreparedOutput,
                StaleRow::Import => Detail::NativeStaleImport,
                StaleRow::PreparedOutputNotInert => Detail::NativePreparedOutputNotInert,
            }),
            None,
        ),
        O::Native(refusal) => native(refusal),
        O::ClosureBytesCorrupt => Termination::failed(
            Code::HostIoFailure,
            Fault::HostIo,
            Some(Detail::DeliveryClosureBytesCorrupt),
        ),
        O::ClosureUnspawnable => Termination::failed(
            Code::HostIoFailure,
            Fault::HostIo,
            Some(Detail::DeliveryClosureUnspawnable),
        ),
        O::ProviderProtocol { key } => Termination::failed(
            Code::ProviderProtocolViolation,
            Fault::ProviderProtocol,
            None,
        )
        .keyed(key.clone()),
        O::Analysis(outcome) => analysis(outcome),
        O::OutputBoundExceeded => Termination::failed(
            Code::OutputSerializationFailed,
            Fault::OutputSerialization,
            Some(Detail::EvaluationOutputBoundExceeded),
        ),
        O::Replay(row) => row.clone().into(),
        O::CommitUndetermined {
            execution_id,
            namespace,
        } => Termination {
            subject: Some(execution_id.clone()),
            execution_id: Some(execution_id.clone()),
            namespace: Some(namespace.clone()),
            ..Termination::failed(Code::DurabilityCommitFailed, Fault::DurabilityCommit, None)
        },
        O::ExistingAttempt {
            execution_id,
            namespace,
        } => Termination {
            execution_id: Some(execution_id.clone()),
            namespace: Some(namespace.clone()),
            ..host_invariant(Some(execution_id.clone()))
        },
        O::CarrierCapacityExhausted { namespace } => Termination {
            subject: Some(namespace.clone()),
            namespace: Some(namespace.clone()),
            ..Termination::failed(
                Code::LedgerBusyTimeout,
                Fault::LedgerBusy,
                Some(Detail::ProjectBusy),
            )
        },
        O::LatchedAfterAdmission { run_id } => delivery_failed(Some(run_id)),
        O::RequiredDeliveryFailed { committed_run } => delivery_failed(committed_run.as_ref()),
        O::Interrupted { signal, run_id } => Termination::interrupted(*signal, run_id.clone()),
        O::HostPanicBeforeAdmission => {
            Termination::failed(Code::SystemOutcomeIllegalState, Fault::HostInvariant, None)
        }
        O::EphemeralCannotSupplyAuthority => Termination::rejected(
            Code::RequestUnsatisfiable,
            Some(Detail::WorkflowEphemeralCannotSupplyAuthority),
            None,
        ),
        O::NativeContextRefused { key } => {
            Termination::rejected(Code::RequestPreconditionFailed, None, None).keyed(key.clone())
        }
        O::PrepareBoundExceeded => Termination::failed(
            Code::HostIoFailure,
            Fault::HostIo,
            Some(Detail::NativePrepareBoundExceeded),
        )
        .keyed("native.prepare-bound-exceeded".to_owned()),
        O::AmbientCargoConfig => Termination::failed(
            Code::HostIoFailure,
            Fault::HostIo,
            Some(Detail::NativeAmbientCargoConfig),
        )
        .keyed("native.ambient-cargo-config".to_owned()),
        O::ExcludedManifests { first, rest } => excluded_manifests(first, rest),
        O::ExcludedRequest { first, rest } => excluded_requests(*first, rest),
        O::TypescriptConfigUnresolved(refusal) => Termination {
            remedy: Some(REMEDY_TYPESCRIPT_CONFIG_UNRESOLVED),
            ..Termination::rejected(
                Code::ConfigInvalid,
                Some(Detail::NativeTypescriptConfigUnresolved),
                Some(bounded_subject(&refusal.subject())),
            )
        },
    }
}

/// Rows 42 to 44: `DELIVERY.REQUIRED_FAILED`, `delivery-required`. With a
/// committed Run, `DELIVERY.RENDERER_FAILED_AFTER_COMMIT` and its runId;
/// without one, `DELIVERY.REQUIRED_PROJECTION_FAILED` and no runId (the
/// StepTermination schema's required-delivery detail law).
fn delivery_failed(committed_run: Option<&String>) -> Termination {
    let detail = match committed_run {
        Some(_) => Detail::DeliveryRendererFailedAfterCommit,
        None => Detail::DeliveryRequiredProjectionFailed,
    };
    Termination {
        run_id: committed_run.cloned(),
        ..Termination::failed(
            Code::DeliveryRequiredFailed,
            Fault::DeliveryRequired,
            Some(detail),
        )
    }
}

// ------------------------------------------- WS:233-240: the aggregate

/// One step's terminal outcome and termination.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct StepResult {
    pub(crate) outcome: StepOutcome,
    pub(crate) termination: Termination,
}
impl StepResult {
    /// A required output that returned: `completed`, `success`.
    pub(crate) fn completed() -> Self {
        Self {
            outcome: StepOutcome::Completed,
            termination: Termination::success(),
        }
    }
    /// A step that ended on a termination: rejected, failed, cancelled, or
    /// completed with a verdict class.
    pub(crate) fn ended(termination: Termination) -> Self {
        let outcome = match termination.class {
            Class::RequestRejected => StepOutcome::Rejected,
            Class::OperationalFailed => StepOutcome::Failed,
            Class::Interrupted => StepOutcome::Cancelled,
            Class::Success | Class::PolicyFailed | Class::Indeterminate => StepOutcome::Completed,
        };
        Self {
            outcome,
            termination,
        }
    }
}

/// WS:233-240, over required steps only: `operational-failed` >
/// `request-rejected` > `policy-failed` > `indeterminate` > `success`. Ties
/// keep the first termination carrying a detail in step order, or the
/// first. A skipped step and an optional step never decide. With no
/// candidate, the first interrupted termination stands, else success.
pub(crate) fn aggregate(steps: &[(Requirement, &StepResult)]) -> Termination {
    const ORDER: [Class; 5] = [
        Class::OperationalFailed,
        Class::RequestRejected,
        Class::PolicyFailed,
        Class::Indeterminate,
        Class::Success,
    ];
    let required: Vec<&StepResult> = steps
        .iter()
        .filter(|(requirement, step)| {
            *requirement == Requirement::Required && step.outcome != StepOutcome::Skipped
        })
        .map(|(_, step)| *step)
        .collect();
    for class in ORDER {
        let matching: Vec<&StepResult> = required
            .iter()
            .copied()
            .filter(|step| step.termination.class == class)
            .collect();
        if let Some(first) = matching.first() {
            let chosen = matching
                .iter()
                .find(|step| step.termination.detail.is_some())
                .unwrap_or(first);
            return chosen.termination.clone();
        }
    }
    required
        .iter()
        .find(|step| step.termination.class == Class::Interrupted)
        .map(|step| step.termination.clone())
        .unwrap_or_else(Termination::success)
}
#[cfg(test)]
mod tests {
    include!("outcomes_tests.rs");
}
