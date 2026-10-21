// Law X10 items 5 and 7, the binary layer. The real built `opensip doctor`
// runs with no override of any kind: a development build ends at F0 with
// `CORE.NO_EMBEDDED_RELEASE`, exit 2, before any installation path is
// opened. These tests assert exactly that shipped behaviour, the envelope's
// schema validity, and that the account's real installation is untouched.
// The source pins keep every home, profile and release selector out of the
// binary and the doctor ingress.
use serde_json::Value;
use std::path::{Path, PathBuf};
use std::process::Command;

const ENVELOPE: &str = "urn:opensip:product-v1:workflows:evaluator3:command-envelope:7";

fn real_installation() -> PathBuf {
    let home = std::env::var_os("HOME").expect("HOME for the test process");
    Path::new(&home).join("Library/Application Support/OpenSIP")
}
fn doctor(args: &[&str]) -> std::process::Output {
    // A scratch working directory: the command reads no project or
    // configuration, and HOME plays no part in finding the installation.
    let cwd = std::env::temp_dir();
    Command::new(env!("CARGO_BIN_EXE_opensip"))
        .args(args)
        .current_dir(cwd)
        .output()
        .unwrap()
}
fn schema_valid(raw: &[u8]) -> bool {
    opensip_host::embedded_schema_registry()
        .unwrap()
        .schema(ENVELOPE, "")
        .unwrap()
        .admit_json(raw, 64 * 1024 * 1024)
        .is_ok()
}

#[test]
fn a_development_build_doctor_ends_at_no_embedded_release_in_both_formats() {
    let existed = real_installation().exists();
    let out = doctor(&["doctor", "--format", "json"]);
    assert_eq!(out.status.code(), Some(2));
    assert!(out.stderr.is_empty());
    assert!(schema_valid(&out.stdout));
    let value: Value = serde_json::from_slice(&out.stdout).unwrap();
    assert_eq!(value["kind"], "failure");
    assert!(value.get("doctor").is_none());
    assert_eq!(value["exitCode"], 2);
    assert_eq!(value["termination"]["class"], "request-rejected");
    assert_eq!(
        value["termination"]["errorCode"],
        "REQUEST.PRECONDITION_FAILED"
    );
    assert_eq!(
        value["termination"]["domainDetail"]["code"],
        "CORE.NO_EMBEDDED_RELEASE"
    );
    assert_eq!(value["errors"][0], value["termination"]["domainDetail"]);
    let id = value["requestId"].as_str().unwrap();
    assert!(id.starts_with("req1_") && id.len() == 37);

    let human = doctor(&["doctor"]);
    assert_eq!(human.status.code(), Some(2));
    let text = String::from_utf8(human.stdout).unwrap();
    let remedy = value["errors"][0]["remedy"].as_str().unwrap();
    assert!(text.starts_with(&format!(
        "Termination: request-rejected\nError: REQUEST.PRECONDITION_FAILED\n\
         Detail: CORE.NO_EMBEDDED_RELEASE\nRemedy: {remedy}\nRequest: req1_"
    )));
    // Nothing was created: a development build cannot reach any path.
    assert_eq!(real_installation().exists(), existed);
}

#[test]
fn doctor_takes_no_flags_and_agent_format_is_not_applicable() {
    let out = doctor(&["doctor", "--checks", "platform", "--format=json"]);
    assert_eq!(out.status.code(), Some(2));
    let value: Value = serde_json::from_slice(&out.stdout).unwrap();
    assert_eq!(value["termination"]["errorCode"], "REQUEST.UNKNOWN_OPTION");
    let out = doctor(&["doctor", "extra", "--format=json"]);
    assert_eq!(out.status.code(), Some(2));
    let out = doctor(&["doctor", "--format=agent"]);
    assert_eq!(out.status.code(), Some(2));
    assert!(
        String::from_utf8(out.stdout)
            .unwrap()
            .contains("OUTPUT.FORMAT_NOT_APPLICABLE")
    );
}

#[test]
fn help_and_completion_list_doctor() {
    let out = doctor(&["help", "doctor", "--format=json"]);
    assert_eq!(out.status.code(), Some(0));
    let value: Value = serde_json::from_slice(&out.stdout).unwrap();
    assert_eq!(
        value["meta"]["commands"],
        serde_json::json!([{
            "name": "doctor",
            "usage": "opensip doctor [--format human|json]",
            "summary": "Report the health of this account's OpenSIP installation."
        }])
    );
    let text = String::from_utf8(doctor(&["completion", "bash"]).stdout).unwrap();
    assert!(text.contains("doctor"));
}

/// The exact accepted S-OP-2 logging test module, in the middle of
/// outcomes.rs. Removing this one known cfg(test) item must retain every
/// production byte on either side. Unknown changes remain visible and fail
/// the original source guard rather than being parsed as a new exception.
// Exact accepted production prefix: the exception is a top-level item at
// this one offset, never a copied block in a nested module or macro.
const KNOWN_LOGGING_PREFIX: &str = r#####"use crate::configuration::{PolicySelectionRefusal, policy_selection_termination};
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

"#####;

const KNOWN_LOGGING_TESTS: &str = r###"#[cfg(test)]
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
"###;

const KNOWN_TEST_TAILS: [&str; 3] = [
    r########"#[cfg(test)]
mod tests {
    include!("outcomes_tests.rs");
}
"########,
    r########"#[cfg(test)]
mod tests {
    include!("doctor_ingress_tests.rs");
}
"########,
    r########"#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn foreign_and_unreserved_contexts_cannot_project() {
        let mut a = RequestAuthority::default();
        let mut b = RequestAuthority::default();
        let x = a.allocate(|| Ok([1; 16])).unwrap();
        let y = b.allocate(|| Ok([1; 16])).unwrap();
        assert!(a.project(&y).is_none());
        assert!(b.project(&x).is_none());
        assert!(a.project(&RequestContext { _private: 1 }).is_none());
        assert_eq!(
            a.project(&x).unwrap(),
            "req1_01010101010101010101010101010101"
        );
        assert_eq!(a.reservations.len(), 1);
    }
    /// Law M3-J1 r6 item 2 (unit J3a), J-C2's host half: the identity the
    /// registry lends is the one its projection renders, so the envelope's
    /// `requestId` and P0's `invocation.requestId` (which the intent records
    /// from the lent identity) are one RequestId. A foreign context lends
    /// nothing.
    #[test]
    fn the_lent_identity_is_the_projected_request_id() {
        let mut a = RequestAuthority::default();
        let mut b = RequestAuthority::default();
        let x = a.begin().unwrap();
        let y = b.begin().unwrap();
        let lent = a.identity(&x).unwrap();
        let rendered = lent
            .bytes()
            .iter()
            .fold("req1_".to_owned(), |text, byte| format!("{text}{byte:02x}"));
        assert_eq!(a.project(&x).unwrap(), rendered);
        assert!(a.identity(&y).is_none());
        assert!(b.identity(&x).is_none());
        assert!(a.identity(&RequestContext { _private: 1 }).is_none());
        assert_ne!(b.identity(&y).unwrap().bytes(), lent.bytes());
        assert_eq!((a.reservations.len(), a.identities.len()), (1, 1));
        // A context reserved through a forced draw has no lent identity.
        let forced = a.allocate(|| Ok([9; 16])).unwrap();
        assert!(a.project(&forced).is_some() && a.identity(&forced).is_none());
    }
    #[test]
    fn logging_scopes_require_the_owned_platform_reservation() {
        let mut a = RequestAuthority::default();
        let mut b = RequestAuthority::default();
        let x = a.begin().unwrap();
        let y = b.begin().unwrap();
        let before = (a.reservations.len(), a.identities.len());
        assert!(a.logging_scope(&x).is_some());
        assert!(a.logging_scope(&x).is_some());
        assert!(a.logging_scope(&y).is_none());
        assert!(b.logging_scope(&x).is_none());
        assert!(a.logging_scope(&RequestContext { _private: 1 }).is_none());
        assert_eq!((a.reservations.len(), a.identities.len()), before);
        let forced = a.allocate(|| Ok([7; 16])).unwrap();
        assert!(a.project(&forced).is_some());
        assert!(a.logging_scope(&forced).is_none());
    }

    #[test]
    fn collision_budget_and_error_do_not_publish_or_replace() {
        let mut a = RequestAuthority::default();
        let first = a.allocate(|| Ok([0; 16])).unwrap();
        let mut draws = 0;
        assert!(matches!(
            a.allocate(|| {
                draws += 1;
                Ok([0; 16])
            }),
            Err(RequestAllocationError::CollisionExhausted)
        ));
        assert_eq!(draws, 8);
        assert_eq!(a.reservations.len(), 1);
        assert!(a.project(&first).is_some());
        assert!(matches!(
            a.allocate(|| Err(RequestAllocationError::EntropyUnavailable)),
            Err(RequestAllocationError::EntropyUnavailable)
        ));
        assert_eq!(a.reservations.len(), 1);
        let mut calls = 0;
        let second = a
            .allocate(|| {
                calls += 1;
                Ok([if calls < 3 { 0 } else { 2 }; 16])
            })
            .unwrap();
        assert_eq!(calls, 3);
        assert_ne!(a.project(&first), a.project(&second));
    }
    #[test]
    fn only_the_four_authoritative_default_commands_may_create() {
        use opensip_contracts::generated::invocation::Inventory3CommandName as C;
        let all: Vec<C> = serde_json::from_value(serde_json::json!([
            "default",
            "recommend",
            "analyze",
            "fit",
            "audit",
            "query",
            "import",
            "baseline-adopt",
            "baseline-export",
            "baseline-show",
            "baseline-upgrade",
            "policy-show",
            "policy-init",
            "policy-test",
            "waive",
            "candidates",
            "inspect",
            "review-brief",
            "review-join",
            "repair-preview",
            "repair-apply",
            "repair-verify",
            "repair-recover",
            "test-run",
            "install",
            "update",
            "doctor",
            "purge",
            "agent-serve",
            "help",
            "version",
            "completion",
            "trust-recovery-challenge",
            "trust-recovery-import",
            "trust-refresh",
            "trust-import",
            "trust-doctor",
            "store-migrate",
            "store-rollback",
            "store-gc",
            "store-status",
            "native-prepare",
            "core-update",
            "core-repair",
            "core-rollback"
        ]))
        .unwrap();
        assert_eq!(all.len(), 45);
        let named = |entry: InstallationEntry| -> Vec<String> {
            all.iter()
                .filter(|c| installation_entry(**c, false) == Ok(entry))
                .map(|c| c.to_string())
                .collect()
        };
        assert_eq!(
            named(InstallationEntry::Creator),
            ["default", "analyze", "fit", "audit"]
        );
        assert_eq!(
            named(InstallationEntry::NotInitializedWhenAbsent),
            [
                "import",
                "baseline-upgrade",
                "repair-apply",
                "repair-verify",
                "test-run",
                "native-prepare"
            ]
        );
        assert_eq!(
            named(InstallationEntry::Outside),
            [
                "install",
                "update",
                "doctor",
                "help",
                "version",
                "completion"
            ]
        );
        assert_eq!(
            named(InstallationEntry::CommandOwnerDecides).len(),
            45 - 4 - 6 - 6
        );
    }
    #[test]
    fn ephemeral_leaves_the_creator_only_where_accepted() {
        use opensip_contracts::generated::invocation::Inventory3CommandName as C;
        assert_eq!(
            installation_entry(C::Analyze, true),
            Ok(InstallationEntry::Outside)
        );
        assert_eq!(
            installation_entry(C::Fit, true),
            Ok(InstallationEntry::Outside)
        );
        for command in [C::Default, C::Audit, C::Import, C::Help, C::RepairVerify] {
            assert_eq!(
                installation_entry(command, true),
                Err(InstallationEntryError::EphemeralNotAccepted)
            );
        }
    }
    #[test]
    fn not_initialized_applies_only_to_non_creators_that_need_the_installation() {
        use InstallationEntry::*;
        for entry in [
            Creator,
            NotInitializedWhenAbsent,
            CommandOwnerDecides,
            Outside,
        ] {
            assert_eq!(installation_precondition(entry, false), None);
        }
        assert_eq!(
            installation_precondition(NotInitializedWhenAbsent, true).map(|d| d.to_string()),
            Some("INSTALLATION.NOT_INITIALIZED".to_string())
        );
        for entry in [Creator, CommandOwnerDecides, Outside] {
            assert_eq!(installation_precondition(entry, true), None);
        }
    }
}
"########,
];

fn strip_known_test_tail(text: &str) -> &str {
    for tail in KNOWN_TEST_TAILS {
        if let Some(before) = text.strip_suffix(tail) {
            return before;
        }
    }
    text
}

fn logging_block_is_pinned(text: &str) -> bool {
    text.strip_prefix(KNOWN_LOGGING_PREFIX)
        .is_some_and(|rest| rest.starts_with(KNOWN_LOGGING_TESTS))
        && text.matches(KNOWN_LOGGING_TESTS).count() == 1
}

fn production_source(text: &str, outcomes: bool) -> String {
    let text = if outcomes && logging_block_is_pinned(text) {
        text.replacen(KNOWN_LOGGING_TESTS, "", 1)
    } else {
        text.to_owned()
    };
    // Only an exact known cfg(test) tail at EOF is excluded. A selector
    // appended after a test module must remain visible to the source guard.
    let text = strip_known_test_tail(&text);
    text.lines()
        .filter(|line| !line.trim_start().starts_with("//"))
        .collect::<Vec<_>>()
        .join("\n")
}
fn production(path: &Path) -> String {
    let text = std::fs::read_to_string(path).unwrap();
    let outcomes = path.ends_with("crates/host/src/outcomes.rs");
    assert!(
        production_feature_sites_are_closed(&text, outcomes),
        "unapproved feature selector in {}",
        path.display()
    );
    production_source(&text, outcomes)
}

#[test]
fn production_projection_excludes_only_the_exact_logging_test_module() {
    let production = "fn production() {}\n";
    let accepted = format!("{KNOWN_LOGGING_PREFIX}{KNOWN_LOGGING_TESTS}{production}");
    let expected = format!("{KNOWN_LOGGING_PREFIX}{production}");
    assert_eq!(
        production_source(&accepted, true),
        production_source(&expected, true),
        "logging exclusion must preserve surrounding production"
    );
    for altered in [
        KNOWN_LOGGING_TESTS.replace("mod logging_tests", "mod unrelated_tests"),
        KNOWN_LOGGING_TESTS.replace("host.begin()", "unexpected_bridge()"),
        KNOWN_LOGGING_TESTS.replace("#[cfg(test)]", "# [cfg(test)]"),
        KNOWN_LOGGING_TESTS.repeat(2),
    ] {
        assert!(
            production_source(&format!("{KNOWN_LOGGING_PREFIX}{altered}"), true)
                .contains("cfg(test)"),
            "unknown logging test shape must remain visible"
        );
    }
    assert!(
        production_source(&accepted, false).contains("cfg(test)"),
        "other paths must not gain the logging exception"
    );
    for nested in [
        format!("mod bridge {{\n{accepted}\n}}"),
        format!("{KNOWN_LOGGING_PREFIX}mod bridge {{\n{KNOWN_LOGGING_TESTS}\n}}"),
    ] {
        assert!(
            production_source(&nested, true).contains("cfg(test)"),
            "nested logging module must remain visible"
        );
    }
    let debug = KNOWN_LOGGING_TESTS.replace("cfg(test)", "cfg(debug_assertions)");
    assert!(production_source(&debug, true).contains("cfg(debug_assertions)"));
    for tail in KNOWN_TEST_TAILS {
        let accepted_tail = format!("{production}{tail}");
        assert_eq!(
            production_source(&accepted_tail, false),
            production.trim_end()
        );
        let after = format!("{accepted_tail}\nfn selected() {{ std::env::var(\"HOME\"); }}");
        assert!(
            production_source(&after, false).contains("std::env::var"),
            "production after a final tests module must remain visible"
        );
    }
    // A new production selector on either side cannot disappear along with
    // the accepted test block, including the code after that middle block.
    for selector in [
        "std::env::var(\"HOME\")",
        "cfg(feature = \"bridge\")",
        "cfg(debug_assertions)",
    ] {
        for text in [
            format!("{selector}\n{accepted}"),
            format!("{accepted}\n{selector}"),
        ] {
            assert!(
                production_source(&text, true).contains(selector),
                "production before and after the logging block must remain visible"
            );
        }
    }
}

fn allowed_feature_declarations() -> [(&'static str, &'static str, Value); 8] {
    [
        (
            "opensip-cli",
            "apps/cli",
            serde_json::json!({
                "operability-dev-sinks": ["opensip-host/operability-dev-sinks"],
                "harness-instrumentation": ["opensip-host/harness-instrumentation"]
            }),
        ),
        (
            "opensip-reporting",
            "crates/reporting",
            serde_json::json!({}),
        ),
        (
            "opensip-host",
            "crates/host",
            serde_json::json!({
                "crash-matrix": ["opensip-storage/crash-matrix", "opensip-security/crash-matrix", "opensip-platform/crash-matrix"],
                "operability-dev-sinks": ["opensip-operability/operability-dev-sinks"],
                "harness-instrumentation": ["opensip-operability/harness-instrumentation"]
            }),
        ),
        (
            "opensip-security",
            "crates/security",
            serde_json::json!({
                "crash-matrix": ["opensip-platform/crash-matrix"], "scenario-fixtures": []
            }),
        ),
        (
            "opensip-storage",
            "crates/storage",
            serde_json::json!({
                "crash-matrix": ["opensip-security/crash-matrix", "opensip-platform/crash-matrix"],
                "scenario-fixtures": ["opensip-security/scenario-fixtures"]
            }),
        ),
        (
            "opensip-operability",
            "crates/operability",
            serde_json::json!({
                "operability-dev-sinks": [], "harness-instrumentation": [], "test-mints": []
            }),
        ),
        (
            "opensip-platform",
            "crates/platform",
            serde_json::json!({
                "crash-matrix": [], "test-fixture": []
            }),
        ),
        (
            "opensip-lifecycle",
            "crates/lifecycle",
            serde_json::json!({
                "crash-matrix": ["opensip-security/crash-matrix"],
                "scenario-fixtures": ["opensip-security/scenario-fixtures"]
            }),
        ),
    ]
}
fn guarded_feature(feature: &str) -> bool {
    matches!(
        feature,
        "operability-dev-sinks"
            | "harness-instrumentation"
            | "crash-matrix"
            | "scenario-fixtures"
            | "test-mints"
            | "test-fixture"
    )
}
fn resolve_node<'a>(doc: &'a Value, id: &Value) -> Option<&'a Value> {
    id.as_str()?;
    let mut nodes = doc["resolve"]["nodes"]
        .as_array()?
        .iter()
        .filter(|n| n["id"] == *id);
    let node = nodes.next()?;
    if nodes.next().is_some() {
        return None;
    }
    Some(node)
}
fn resolved_dependency<'a>(doc: &'a Value, package: &Value, alias: &str) -> Option<&'a Value> {
    let node = resolve_node(doc, &package["id"])?;
    let normalized = alias.replace('-', "_");
    let mut edges = node["deps"]
        .as_array()?
        .iter()
        .filter(|d| d["name"] == normalized);
    let edge = edges.next()?;
    edge["pkg"].as_str()?;
    if edges.next().is_some() {
        return None;
    }
    Some(edge)
}
fn dependency_alias(dep: &Value) -> Option<&str> {
    dep["rename"].as_str().or_else(|| dep["name"].as_str())
}
fn edge_has_declaration(edge: &Value, dep: &Value) -> bool {
    let (Some(kind), Some(target)) = (dep.get("kind"), dep.get("target")) else {
        return false;
    };
    edge["dep_kinds"].as_array().is_some_and(|kinds| {
        kinds
            .iter()
            .any(|k| k.get("kind") == Some(kind) && k.get("target") == Some(target))
    })
}
fn metadata_declared_features_are_closed(root: &Path, doc: &Value) -> bool {
    let Some(packages) = doc["packages"].as_array() else {
        return false;
    };
    let mut selected = std::collections::BTreeMap::new();
    for (name, directory, expected_features) in allowed_feature_declarations() {
        let Ok(expected_manifest) = root.join(directory).join("Cargo.toml").canonicalize() else {
            return false;
        };
        let matching: Vec<_> = packages
            .iter()
            .filter(|p| {
                p["name"] == name
                    && p["manifest_path"]
                        .as_str()
                        .and_then(|p| Path::new(p).canonicalize().ok())
                        .is_some_and(|actual| actual == expected_manifest)
            })
            .collect();
        if matching.len() != 1 || matching[0]["features"] != expected_features {
            return false;
        }
        let package = matching[0];
        let (kind, source) = if name == "opensip-cli" {
            ("bin", "src/main.rs")
        } else {
            ("lib", "src/lib.rs")
        };
        let Ok(expected_source) = root.join(directory).join(source).canonicalize() else {
            return false;
        };
        let Some(targets) = package["targets"].as_array() else {
            return false;
        };
        let targets: Vec<_> = targets
            .iter()
            .filter(|t| {
                t["kind"]
                    .as_array()
                    .is_some_and(|kinds| kinds.iter().any(|k| k == kind))
            })
            .collect();
        if targets.len() != 1
            || !targets[0]["src_path"]
                .as_str()
                .and_then(|p| Path::new(p).canonicalize().ok())
                .is_some_and(|actual| actual == expected_source)
        {
            return false;
        }
        if resolve_node(doc, &package["id"]).is_none() {
            return false;
        }
        selected.insert(name, package);
    }
    // Bind each allowed forwarding spelling to its actual resolved package,
    // not a same-spelling alias or a package row merely present elsewhere.
    for package in selected.values() {
        let Some(features) = package["features"].as_object() else {
            return false;
        };
        for items in features.values() {
            let Some(items) = items.as_array() else {
                return false;
            };
            for item in items {
                let Some(item) = item.as_str() else {
                    return false;
                };
                let Some((alias, _)) = item.split_once('/') else {
                    continue;
                };
                let Some(target) = selected.get(alias) else {
                    return false;
                };
                let Some(edge) = resolved_dependency(doc, package, alias) else {
                    return false;
                };
                if edge["pkg"] != target["id"] {
                    return false;
                }
                let Some(dependencies) = package["dependencies"].as_array() else {
                    return false;
                };
                if !dependencies.iter().any(|d| {
                    dependency_alias(d) == Some(alias)
                        && d.get("kind").is_some_and(Value::is_null)
                        && d.get("target").is_some_and(Value::is_null)
                        && edge_has_declaration(edge, d)
                }) {
                    return false;
                }
            }
        }
    }
    for package in packages {
        // An unapproved intermediate package cannot invent another feature
        // name/default which forwards into one of these guarded endpoints.
        let Some(features) = package["features"].as_object() else {
            return false;
        };
        for items in features.values() {
            let Some(items) = items.as_array() else {
                return false;
            };
            for item in items {
                let Some(item) = item.as_str() else {
                    return false;
                };
                let Some((alias, feature)) = item.split_once('/') else {
                    continue;
                };
                if !guarded_feature(feature) {
                    continue;
                }
                let alias = alias.strip_suffix('?').unwrap_or(alias);
                let Some(edge) = resolved_dependency(doc, package, alias) else {
                    return false;
                };
                if selected.values().any(|target| target["id"] == edge["pkg"])
                    && !selected
                        .values()
                        .any(|source| source["id"] == package["id"])
                {
                    return false;
                }
            }
        }
        let Some(dependencies) = package["dependencies"].as_array() else {
            return false;
        };
        for dep in dependencies {
            let Some(features) = dep["features"].as_array() else {
                return false;
            };
            for feature in features {
                let Some(feature) = feature.as_str() else {
                    return false;
                };
                if !guarded_feature(feature) {
                    continue;
                }
                let Some(alias) = dependency_alias(dep) else {
                    return false;
                };
                let Some(edge) = resolved_dependency(doc, package, alias) else {
                    return false;
                };
                if !selected.values().any(|p| p["id"] == edge["pkg"]) {
                    continue;
                }
                if !edge_has_declaration(edge, dep) {
                    return false;
                }
                let allowed_dev_feature = dep["kind"] == "dev"
                    && matches!(feature, "scenario-fixtures" | "test-mints" | "test-fixture");
                if !allowed_dev_feature {
                    return false;
                }
            }
        }
    }
    true
}
fn actual_declared_features_are_closed(root: &Path) -> bool {
    let Ok(output) = Command::new(env!("CARGO"))
        .args(["metadata", "--locked", "--offline", "--format-version", "1"])
        .current_dir(root)
        .output()
    else {
        return false;
    };
    if !output.status.success() {
        return false;
    }
    let Ok(doc) = serde_json::from_slice::<Value>(&output.stdout) else {
        return false;
    };
    metadata_declared_features_are_closed(root, &doc)
}
const KNOWN_CLI_MAIN_SOURCE: &str = r########"#![forbid(unsafe_code)]
mod arguments;
mod bootstrap;
mod terminal;
fn main() -> std::process::ExitCode {
    std::process::ExitCode::from(bootstrap::run(std::env::args_os().skip(1)))
}
"########;
const KNOWN_NONFEATURE_IMPORTS: &[&str] = &[
r########"use InstallationEntry::*;"########,
r########"use Observation as O;"########,
r########"use crate::arguments::{self, Request};"########,
r########"use crate::outcomes::{Format, MetadataError, RenderedResponse};"########,
r########"use crate::{DoctorOutcome, DoctorReportV1, InstallationTerminationV1};"########,
r########"use opensip_contracts::generated::evidence::{
    Common4D9Class as Class, Common4DomainDetailCode as Detail,
};"########,
r########"use opensip_contracts::generated::invocation::Inventory3CommandName as C;"########,
r########"use opensip_contracts::generated::output::Envelope7Root;"########,
r########"use opensip_host::{Format, MetadataRequest};"########,
r########"use opensip_host::{MetadataError, MetadataHost, finalize_invocation};"########,
r########"use serde_json::{Value, json};"########,
r########"use std::ffi::OsString;"########,
r########"use std::fmt::Write;"########,
r########"use std::io;"########,
r########"use std::os::fd::AsFd;"########,
r########"use std::{
    ffi::OsString,
    io::{self, Write},
};"########,
r########"use std::{collections::BTreeMap, sync::Arc};"########,
];
const KNOWN_EXPRESSION_MACROS: &[&str] = &["compile_error","format","json","matches","unreachable","vec","write","writeln"];

fn source_code_without_data(text: &str) -> Option<String> {
    let bytes = text.as_bytes();
    let mut code = bytes.to_vec();
    let mut i = 0;
    while i < bytes.len() {
        if bytes[i..].starts_with(b"//") {
            let end = bytes[i..].iter().position(|b| *b == b'\n').map_or(bytes.len(), |n| i + n);
            code[i..end].fill(b' ');
            i = end;
            continue;
        }
        if bytes[i..].starts_with(b"/*") {
            let mut depth = 1;
            let mut end = i + 2;
            while end < bytes.len() && depth != 0 {
                if bytes[end..].starts_with(b"/*") { depth += 1; end += 2; }
                else if bytes[end..].starts_with(b"*/") { depth -= 1; end += 2; }
                else { end += 1; }
            }
            if depth != 0 { return None; }
            code[i..end].fill(b' ');
            i = end;
            continue;
        }
        // Only the already selected package-version query is allowed; an
        // env!("HOME") or CARGO_FEATURE query is not a logging permission.
        let version = b"env!(\"CARGO_PKG_VERSION\")";
        if bytes[i..].starts_with(version) {
            code[i..i+version.len()].fill(b' ');
            i += version.len();
            continue;
        }
        let raw_prefix = if bytes[i..].starts_with(b"br") || bytes[i..].starts_with(b"cr") { 2 }
            else if bytes[i] == b'r' { 1 } else { 0 };
        if raw_prefix != 0 {
            let start = i + raw_prefix;
            let mut quote = start;
            while bytes.get(quote) == Some(&b'#') { quote += 1; }
            if bytes.get(quote) == Some(&b'"') {
                let hashes = &bytes[start..quote];
                let mut end = quote + 1;
                loop {
                    if end >= bytes.len() { return None; }
                    if bytes[end] == b'"' && bytes.get(end+1..end+1+hashes.len()) == Some(hashes) {
                        end += 1 + hashes.len();
                        break;
                    }
                    end += 1;
                }
                code[i..end].fill(b' ');
                i = end;
                continue;
            }
        }
        if bytes[i] == b'"' {
            let mut end = i + 1;
            loop {
                match bytes.get(end) {
                    None => return None,
                    Some(b'\\') => { if end + 1 >= bytes.len() { return None; } end += 2; }
                    Some(b'"') => { end += 1; break; }
                    Some(_) => end += 1,
                }
            }
            code[i..end].fill(b' ');
            i = end;
            continue;
        }
        if bytes[i] == b'\'' {
            let mut end = i + 1;
            if bytes.get(end) == Some(&b'\\') {
                end += 1;
                match bytes.get(end) {
                    Some(b'u') if bytes.get(end+1) == Some(&b'{') => {
                        end += 2;
                        while bytes.get(end).is_some_and(|b| b.is_ascii_hexdigit() || *b == b'_') { end += 1; }
                        if bytes.get(end) == Some(&b'}') { end += 1; }
                    }
                    Some(b'x') if bytes.get(end+1).is_some_and(u8::is_ascii_hexdigit)
                        && bytes.get(end+2).is_some_and(u8::is_ascii_hexdigit) => end += 3,
                    Some(_) => end += 1,
                    None => return None,
                }
            } else if let Some(c) = text.get(end..)?.chars().next() { end += c.len_utf8(); }
            if bytes.get(end) == Some(&b'\'') {
                end += 1;
                code[i..end].fill(b' ');
                i = end;
                continue;
            }
        }
        if bytes[i] == b'#' {
            let end = bytes[i..].iter().position(|b| *b == b'\n').map_or(bytes.len(), |n| i+n);
            let attribute = std::str::from_utf8(&bytes[i..end]).ok()?.trim_end();
            if [
                "#![forbid(unsafe_code)]", r#"#[cfg(target_os = "macos")]"#,
                r#"#[cfg(not(target_os = "macos"))]"#, "#[cfg(unix)]", "#[cfg(not(unix))]",
                "#[derive(Debug, Clone, Copy, PartialEq, Eq)]",
                "#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]",
                "#[derive(Debug, Clone, PartialEq, Eq)]",
                "#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord)]",
                "#[derive(Debug, PartialEq, Eq)]", "#[derive(Default)]",
            ].contains(&attribute) {
                code[i..end].fill(b' ');
                i = end;
                continue;
            }
        }
        if bytes[i].is_ascii_alphabetic() || bytes[i] == b'_' || bytes[i] >= 0x80 {
            i += 1;
            while i < bytes.len() && (bytes[i].is_ascii_alphanumeric() || bytes[i] == b'_' || bytes[i] >= 0x80) { i += 1; }
        } else { i += 1; }
    }
    String::from_utf8(code).ok()
}
fn expression_macros_are_closed(code: &str) -> bool {
    let bytes = code.as_bytes();
    for (i, b) in bytes.iter().enumerate() {
        if *b != b'!' { continue; }
        let mut next = i + 1;
        while bytes.get(next).is_some_and(u8::is_ascii_whitespace) { next += 1; }
        if !bytes.get(next).is_some_and(|b| matches!(b, b'(' | b'[' | b'{')) { continue; }
        let mut end = i;
        while end > 0 && bytes[end-1].is_ascii_whitespace() { end -= 1; }
        let mut start = end;
        while start > 0 && (bytes[start-1].is_ascii_alphanumeric() || matches!(bytes[start-1], b'_' | b':')) { start -= 1; }
        if start == end { continue; } // logical negation, such as !(a && b)
        let name = &code[start..end];
        if ["if", "while", "return", "break", "else", "match"].contains(&name) { continue; }
        if !KNOWN_EXPRESSION_MACROS.contains(&name) { return false; }
    }
    true
}

fn is_forbidden_selector_token(token: &str) -> bool {
    matches!(token, "cfg" | "cfg_attr" | "feature" | "macro_rules" | "macro" | "derive" | "forbid" | "allow" | "use" | "mod" | "extern")
}
fn production_feature_sites_are_closed(text: &str, outcomes: bool) -> bool {
    if !outcomes && text == KNOWN_CLI_MAIN_SOURCE { return true; }
    let text = if outcomes {
        let Some(rest) = text.strip_prefix(KNOWN_LOGGING_PREFIX)
            .and_then(|rest| rest.strip_prefix(KNOWN_LOGGING_TESTS)) else { return false; };
        rest
    } else { text };
    let Some(mut unaccounted) = source_code_without_data(strip_known_test_tail(text)) else { return false; };
    for import in KNOWN_NONFEATURE_IMPORTS {
        let Some(import) = source_code_without_data(import) else { return false; };
        unaccounted = unaccounted.replace(&import, "");
    }
    !unaccounted.contains('#') && expression_macros_are_closed(&unaccounted) && !unaccounted
        .split(|c: char| !(c.is_ascii_alphanumeric() || c == '_'))
        .any(is_forbidden_selector_token)
}
fn feature_metadata_fixture(root: &Path) -> Value {
    let declarations = allowed_feature_declarations();
    let mut packages = Vec::new();
    let mut nodes = Vec::new();
    for (name, directory, features) in &declarations {
        let mut aliases = std::collections::BTreeSet::new();
        for items in features.as_object().unwrap().values() {
            for item in items.as_array().unwrap() {
                if let Some((alias, _)) = item.as_str().unwrap().split_once('/') {
                    aliases.insert(alias);
                }
            }
        }
        let dependencies: Vec<_> = aliases
            .iter()
            .map(|alias| {
                let target = declarations.iter().find(|d| d.0 == *alias).unwrap();
                serde_json::json!({"name": alias, "rename": null, "kind": null, "target": null,
                "features": [], "path": root.join(target.1)})
            })
            .collect();
        let edges: Vec<_> = aliases
            .iter()
            .map(|alias| {
                serde_json::json!({
                    "name": alias.replace('-', "_"), "pkg": format!("pkg:{alias}"),
                    "dep_kinds": [{"kind": null, "target": null}]
                })
            })
            .collect();
        let (kind, source) = if *name == "opensip-cli" {
            ("bin", "src/main.rs")
        } else {
            ("lib", "src/lib.rs")
        };
        packages.push(serde_json::json!({"name": name, "id": format!("pkg:{name}"),
            "manifest_path": root.join(directory).join("Cargo.toml"), "features": features,
            "dependencies": dependencies, "targets": [{"kind": [kind], "src_path": root.join(directory).join(source)}]}));
        nodes.push(serde_json::json!({"id": format!("pkg:{name}"), "deps": edges, "features": []}));
    }
    serde_json::json!({"packages": packages, "resolve": {"nodes": nodes}})
}
#[test]
fn doctor_feature_declarations_keep_the_accepted_opt_in_graph() {
    let root = Path::new(env!("CARGO_MANIFEST_DIR")).join("../..");
    let valid = feature_metadata_fixture(&root);
    assert!(metadata_declared_features_are_closed(&root, &valid));
    for index in 0..8 {
        for (feature, value) in [
            ("default", serde_json::json!([])),
            ("default", serde_json::json!(["harness-instrumentation"])),
            ("home-test-bridge", serde_json::json!([])),
        ] {
            let mut changed = valid.clone();
            changed["packages"][index]["features"][feature] = value;
            assert!(
                !metadata_declared_features_are_closed(&root, &changed),
                "unknown or default features must remain refused"
            );
        }
        let mut foreign = valid.clone();
        foreign["packages"][index]["manifest_path"] =
            serde_json::json!(root.join("not-the-selected-manifest"));
        assert!(!metadata_declared_features_are_closed(&root, &foreign));
        let mut source = valid.clone();
        source["packages"][index]["targets"][0]["src_path"] =
            serde_json::json!(root.join("not-the-selected-source"));
        assert!(!metadata_declared_features_are_closed(&root, &source));
    }
    let mut retarget = valid.clone();
    retarget["packages"][0]["dependencies"][0]["name"] = serde_json::json!("doctor-bridge");
    retarget["packages"][0]["dependencies"][0]["rename"] = serde_json::json!("opensip-host");
    retarget["packages"][0]["dependencies"][0]["path"] =
        serde_json::json!(root.join("foreign/doctor-bridge"));
    retarget["resolve"]["nodes"][0]["deps"][0]["pkg"] = serde_json::json!("foreign:doctor-bridge");
    retarget["packages"].as_array_mut().unwrap().push(serde_json::json!({
        "id": "foreign:doctor-bridge", "name": "doctor-bridge", "manifest_path": root.join("foreign/doctor-bridge/Cargo.toml"),
        "features": {"harness-instrumentation": [], "operability-dev-sinks": []}, "dependencies": [], "targets": []}));
    retarget["resolve"]["nodes"]
        .as_array_mut()
        .unwrap()
        .push(serde_json::json!({"id":"foreign:doctor-bridge","deps":[],"features":[]}));
    assert!(
        !metadata_declared_features_are_closed(&root, &retarget),
        "forwarding alias must bind the intended resolved package"
    );
    for kind in [
        Value::Null,
        serde_json::json!("dev"),
        serde_json::json!("build"),
    ] {
        let mut activated = valid.clone();
        activated["packages"][0]["dependencies"][0]["kind"] = kind.clone();
        activated["packages"][0]["dependencies"][0]["features"] =
            serde_json::json!(["harness-instrumentation"]);
        activated["resolve"]["nodes"][0]["deps"][0]["dep_kinds"] =
            serde_json::json!([{"kind":null,"target":null},{"kind":kind,"target":null}]);
        assert!(
            !metadata_declared_features_are_closed(&root, &activated),
            "direct dependency activation must remain refused"
        );
    }
    let mut forwarding = valid.clone();
    forwarding["packages"][0]["features"]["harness-instrumentation"] =
        serde_json::json!(["opensip-host/crash-matrix"]);
    assert!(!metadata_declared_features_are_closed(&root, &forwarding));
    let mut duplicate = valid.clone();
    duplicate["packages"]
        .as_array_mut()
        .unwrap()
        .push(valid["packages"][0].clone());
    assert!(!metadata_declared_features_are_closed(&root, &duplicate));
    let mut missing = valid.clone();
    missing.as_object_mut().unwrap().remove("resolve");
    assert!(!metadata_declared_features_are_closed(&root, &missing));
    assert!(!metadata_declared_features_are_closed(
        &root,
        &serde_json::json!({})
    ));
}
#[test]
fn doctor_feature_sites_reject_other_cfg_spellings_and_copied_gates() {
    let trusted = format!("{KNOWN_LOGGING_PREFIX}{KNOWN_LOGGING_TESTS}fn ordinary() {{}}\n");
    assert!(production_feature_sites_are_closed(&trusted, true));
    assert!(production_feature_sites_are_closed(
        "#[cfg(unix)]\nfn ordinary() {}",
        false
    ));
    for data in [
        r#"let text = "feature cfg allow";"#,
        r###"let text = r#"cfg_attr # feature"#;"###,
        "let hash = '#'; let quote = '\\'';",
        "/* nested /* \" */ comment */ fn ordinary() {}",
    ] { assert!(production_feature_sites_are_closed(data, false), "literal/comment data is not selector syntax: {data}"); }
    for gate in [
        r#"#[cfg(any(feature = "harness-instrumentation"))]"#,
        r#"#[cfg_attr(feature = "operability-dev-sinks", path = "bridge.rs")]"#,
        r#"# [ cfg ( feature = "harness-instrumentation" ) ]"#,
        "#\n[cfg/*separator*/(any(feature = \"harness-instrumentation\"))]",
        r#"if cfg! ( feature = "harness-instrumentation" ) {}"#,
        r#"#[cfg(any(feature = "operability-dev-sinks", feature = "harness-instrumentation"))]"#,
        "#[unapproved_attribute]",
        r#"unapproved_generator!("#[cfg(feature = \"harness-instrumentation\")] fn alternate(){}")"#,
        r#"use bridge::format; format!("hidden feature generator")"#,
        "mod bridge;",
        r#"env!("HOME")"#,

    ] {
        for (text, outcomes) in [
            (format!("{gate}\nfn alternate() {{}}"), false),
            (format!("{trusted}\n{gate}\nfn alternate() {{}}"), true),
        ] {
            assert!(
                !production_feature_sites_are_closed(&text, outcomes),
                "unapproved feature selector syntax/site must remain refused: {gate}"
            );
        }
    }
}

#[test]
fn no_home_profile_or_release_selector_reaches_the_binary_or_the_ingress() {
    let root = Path::new(env!("CARGO_MANIFEST_DIR")).join("../..");
    let mut files: Vec<PathBuf> = std::fs::read_dir(root.join("apps/cli/src"))
        .unwrap()
        .map(|entry| entry.unwrap().path())
        .collect();
    files.push(root.join("crates/host/src/doctor_ingress.rs"));
    files.push(root.join("crates/host/src/outcomes.rs"));
    files.push(root.join("crates/host/src/request.rs"));
    files.sort();
    for file in &files {
        let text = production(file);
        for forbidden in [
            "std::env::var",
            "env::var",
            "var_os",
            "home_dir",
            "cfg(feature",
            "cfg(test)",
            "cfg(debug_assertions)",
        ] {
            // `main.rs` passes the process arguments, nothing else.
            assert!(
                !text.contains(forbidden),
                "{forbidden} in {}",
                file.display()
            );
        }
    }
    // The ingress's one producer call; no other producer or session entry.
    let ingress = production(&root.join("crates/host/src/doctor_ingress.rs"));
    assert_eq!(
        ingress.matches("observe_installation_for_doctor()").count(),
        1
    );
    for forbidden in [
        "produce_read_platform",
        "produce_on",
        "observe_with",
        "ObservationSession",
        "HomeSource",
        "read_producers",
    ] {
        assert!(!ingress.contains(forbidden), "{forbidden} in the ingress");
    }
    // X10's cross-crate test-bridge prohibition stands. Accepted M3-O1
    // explicitly adds only these opt-in logging/harness feature forwards;
    // no default, home/profile selector or further forwarding is admitted.
    assert!(
        actual_declared_features_are_closed(&root),
        "declared features must equal the accepted opt-in graph"
    );
}
