use crate::request::{RequestAllocationError, RequestAuthority, RequestContext};
use opensip_contracts::generated::output::{Envelope4Root, Metadata1HelpCommand};
use serde_json::{Value, json};
use std::sync::Arc;

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

/// Explicit process-only ingress for metadata operations. It never admits an
/// analysis or mutation, and opens no project, durable store or provider session.
#[derive(Default)]
pub struct MetadataHost {
    authority: RequestAuthority,
}
impl MetadataHost {
    pub fn new() -> Self {
        Self::default()
    }
    /// Must precede argument parsing. No caller identifier is accepted.
    pub fn begin(&mut self) -> Result<Arc<RequestContext>, RequestAllocationError> {
        self.authority.begin()
    }
    /// Required delivery failure before any Run exists, preserving this request.
    pub fn delivery_failure(
        &self,
        context: &RequestContext,
        format: Format,
    ) -> Result<RenderedResponse, &'static str> {
        let request_id = self
            .authority
            .project(context)
            .ok_or("foreign request context")?;
        let detail = json!({"code":"DELIVERY.REQUIRED_PROJECTION_FAILED","remedy":"Retry after resolving the output or projection failure."});
        let projection:Envelope4Root=serde_json::from_value(json!({
            "schemaFamily":"opensip.product.envelope","schemaMajor":4,"kind":"failure","requestId":request_id,
            "termination":{"class":"operational-failed","errorCode":"DELIVERY.REQUIRED_FAILED","faultCause":"delivery-required","domainDetail":detail},
            "exitCode":4,"errors":[detail],"diagnostics":["Required output delivery failed."]
        })).map_err(|_|"delivery failure projection failed")?;
        let bytes = match format {
            Format::Json => opensip_reporting::render_json(&projection)
                .map_err(|_| "delivery failure encoding failed")?,
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
    ) -> Result<RenderedResponse, &'static str> {
        let request_id = self
            .authority
            .project(context)
            .ok_or("request context does not belong to selected host")?;
        if correlation.is_some_and(|x| !(1..=128).contains(&x.chars().count())) {
            return Err("invalid correlation projection");
        }
        let commands = catalogue()?;
        let mut envelope = json!({"schemaFamily":"opensip.product.envelope","schemaMajor":4,"kind":"meta","requestId":request_id,"termination":{"class":"success"},"exitCode":0});
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
        if let Some(bytes) = completion_bytes {
            return Ok(RenderedResponse {
                bytes,
                exit_code: 0,
            });
        }
        let exit_code = if envelope["kind"] == "failure" { 2 } else { 0 };
        // This is construction from host-owned fields, not admission of caller
        // JSON. Original-schema conformance is checked independently in tests.
        let projection: Envelope4Root =
            serde_json::from_value(envelope).map_err(|_| "host metadata projection failed")?;
        let bytes = match format {
            Format::Human => opensip_reporting::render_human(&projection)?,
            Format::Json => opensip_reporting::render_json(&projection)
                .map_err(|_| "host JSON projection failed")?,
        };
        Ok(RenderedResponse { bytes, exit_code })
    }
}
fn catalogue() -> Result<Vec<Metadata1HelpCommand>, &'static str> {
    serde_json::from_value(json!([
        {"name":"completion","usage":"opensip completion <bash|zsh|fish>","summary":"Print shell completion for implemented commands."},
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
