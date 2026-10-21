//! Law X10 r3: the `opensip doctor` ingress. It sits beside the metadata
//! ingress under the same process-custody `RequestAuthority`; doctor writes
//! nothing durable (owner §5), so no durable audit ingress is involved.
//!
//! Item 2: the ingress makes exactly one producer call,
//! `observe_installation_for_doctor()`, which is the process's one attempt,
//! one read receipt and one observation session (458c). Its only inputs are
//! the native account and the authenticated release and profile producers.
//! There is no producer-injection seam and no override of the installation,
//! profile or release (owner §1a).
//!
//! Item 3: a produced report and a report that cannot be produced are
//! `kind: doctor`, with the assembled `Invocation5DoctorResult` passed
//! through unchanged; an unreachable installation is `kind: failure` with
//! its law 468 item 6 row. Exit codes derive from the class only. Doctor's
//! only check is the installation check, so `other` is always empty.
use crate::outcomes::{Format, MetadataError, RenderedResponse};
use crate::{DoctorOutcome, DoctorReportV1, InstallationTerminationV1};
use opensip_contracts::generated::evidence::{
    Common4D9Class as Class, Common4DomainDetailCode as Detail,
};
use opensip_contracts::generated::output::Envelope7Root;
use serde_json::{Value, json};

impl crate::MetadataHost {
    /// Run `opensip doctor` for this request. The installation check is the
    /// only check (item 1); its result is projected by item 3.
    #[cfg(target_os = "macos")]
    pub fn doctor(
        &self,
        context: &crate::RequestContext,
        format: Format,
        correlation: Option<&str>,
    ) -> Result<RenderedResponse, MetadataError> {
        let request_id = self.request_id(context)?;
        if correlation.is_some_and(|x| !(1..=128).contains(&x.chars().count())) {
            return Err(MetadataError::Projection);
        }
        let observed = opensip_security::observe_installation_for_doctor();
        let outcome = crate::doctor_installation(
            &mut crate::DoctorReportSession::new(),
            observed,
            Vec::new(),
        );
        self.finish_logging(false);
        doctor_response(&request_id, correlation, &outcome, format)
    }
}

/// Item 3's envelope, rendered in the requested format, with its exit code.
pub(crate) fn doctor_response(
    request_id: &str,
    correlation: Option<&str>,
    outcome: &DoctorOutcome,
    format: Format,
) -> Result<RenderedResponse, MetadataError> {
    let (envelope, exit_code) = doctor_envelope(request_id, correlation, outcome)?;
    let bytes = match format {
        Format::Human => opensip_reporting::render_human(&envelope)?,
        Format::Json => {
            opensip_reporting::render_json(&envelope).map_err(|_| MetadataError::Serialization)?
        }
    };
    Ok(RenderedResponse { bytes, exit_code })
}

/// Item 3: the command-envelope v7 projection of doctor's outcome and its
/// exit code, derived from the termination class by the fixed table.
pub(crate) fn doctor_envelope(
    request_id: &str,
    correlation: Option<&str>,
    outcome: &DoctorOutcome,
) -> Result<(Envelope7Root, u8), MetadataError> {
    match outcome {
        DoctorOutcome::Report(report) => {
            let (envelope, class) = report_envelope(request_id, report)?;
            project(envelope, class, correlation)
        }
        DoctorOutcome::Refused(row) => failure_envelope(request_id, correlation, row),
    }
}

/// The `kind: failure` envelope of one public termination row and its exit
/// code: a law 468 item 6 row, or a law X12 r3 item 7 policy-selection row.
pub(crate) fn failure_envelope(
    request_id: &str,
    correlation: Option<&str>,
    row: &InstallationTerminationV1,
) -> Result<(Envelope7Root, u8), MetadataError> {
    let (envelope, class) = refused_envelope(request_id, row)?;
    project(envelope, class, correlation)
}

fn project(
    mut envelope: Value,
    class: Class,
    correlation: Option<&str>,
) -> Result<(Envelope7Root, u8), MetadataError> {
    let exit_code = exit(&class)?;
    envelope["exitCode"] = json!(exit_code);
    if let Some(value) = correlation {
        envelope["clientCorrelationId"] = json!(value);
    }
    // Construction from host-owned fields, not admission of caller JSON.
    // Source-schema conformance is checked independently in tests (item 7).
    let projection: Envelope7Root =
        serde_json::from_value(envelope).map_err(|_| "doctor envelope projection failed")?;
    Ok((projection, exit_code))
}

fn exit(class: &Class) -> Result<u8, MetadataError> {
    match class {
        Class::Success => Ok(0),
        Class::RequestRejected => Ok(2),
        Class::OperationalFailed => Ok(4),
        _ => Err(MetadataError::Projection),
    }
}

fn detail_json(code: &Detail, subject: Option<&str>, remedy: &str) -> Value {
    let mut detail = json!({"code": code.to_string(), "remedy": remedy});
    if let Some(subject) = subject {
        detail["subject"] = json!(subject);
    }
    detail
}

fn report_envelope(
    request_id: &str,
    report: &DoctorReportV1,
) -> Result<(Value, Class), MetadataError> {
    let t = &report.termination;
    let mut termination = json!({"class": t.class.to_string()});
    if let Some(code) = &t.error_code {
        termination["errorCode"] = json!(code.to_string());
    }
    if let Some(fault) = &t.fault_cause {
        termination["faultCause"] = json!(fault.to_string());
    }
    match (&t.detail, t.remedy) {
        (Some(detail), Some(remedy)) => {
            termination["domainDetail"] = detail_json(detail, None, remedy);
        }
        (None, None) => {}
        _ => return Err(MetadataError::Projection),
    }
    let doctor =
        serde_json::to_value(&report.result).map_err(|_| "doctor result projection failed")?;
    Ok((
        json!({
            "schemaFamily": "opensip.product.envelope", "schemaMajor": 7, "kind": "doctor",
            "requestId": request_id, "termination": termination, "doctor": doctor,
        }),
        t.class,
    ))
}

fn refused_envelope(
    request_id: &str,
    row: &InstallationTerminationV1,
) -> Result<(Value, Class), MetadataError> {
    let mut termination = json!({
        "class": row.class.to_string(),
        "errorCode": row.error_code.to_string(),
    });
    if matches!(row.class, Class::OperationalFailed) {
        termination["faultCause"] = json!(row.fault_cause.to_string());
    }
    let errors = match &row.detail {
        Some(code) => {
            let detail = detail_json(code, row.subject.as_deref(), row_remedy(code, row)?);
            termination["domainDetail"] = detail.clone();
            json!([detail])
        }
        // 468c's host I/O row names no domain detail. The schema requires a
        // non-empty `errors`, so it carries the existing HOST.IO_FAILURE detail.
        None => json!([detail_json(&Detail::HostIoFailure, None, HOST_IO_REMEDY)]),
    };
    Ok((
        json!({
            "schemaFamily": "opensip.product.envelope", "schemaMajor": 7, "kind": "failure",
            "requestId": request_id, "termination": termination, "errors": errors,
        }),
        row.class,
    ))
}

/// Item 3: one fixed remedy per row. The registered or selected-golden remedy
/// is used where one exists; otherwise the row's fixed text.
fn row_remedy(
    code: &Detail,
    row: &InstallationTerminationV1,
) -> Result<&'static str, MetadataError> {
    Ok(match code {
        Detail::CoreNoEmbeddedRelease => REMEDY_NO_EMBEDDED_RELEASE,
        Detail::InstallationAccountRefused => REMEDY_ACCOUNT_REFUSED,
        // The selected golden's remedy, as 468a's override words it.
        Detail::StorageBackupChoiceRequired => "pass --allow-backup-custody or choose --ephemeral",
        Detail::InstallationNotInitialized => REMEDY_NOT_INITIALIZED,
        Detail::NtTcbIdentity => REMEDY_TCB_IDENTITY,
        Detail::NtTcbBoot => REMEDY_TCB_BOOT,
        Detail::NtTcbProfileUnqualified => REMEDY_TCB_PROFILE,
        Detail::ConfigCustodyRefused => {
            if row.subject.as_deref() == Some("installation-incomplete") {
                REMEDY_INCOMPLETE
            } else {
                REMEDY_CUSTODY
            }
        }
        // Law X3a item 5: no remedy is registered, so the row's fixed text.
        Detail::StateSchemaUnsupported => REMEDY_STATE_SCHEMA,
        Detail::ProjectBusy => REMEDY_BUSY,
        Detail::WorkBudgetExhausted => REMEDY_BUDGET,
        Detail::HostInvariantViolated => REMEDY_INVARIANT,
        // Law X12 r3 item 7 rows 1, 2 and 3a: the published route remedy,
        // keyed by the public code, as contract successor X12-0 widened it.
        Detail::ConfigInvalid => crate::configuration::REMEDY_CONFIG_INVALID,
        // Row 3: the command inventory's remedy for this detail.
        Detail::PolicyImperativeKeyRefused => crate::configuration::REMEDY_IMPERATIVE_KEY,
        // Law X5 r3 items 5 and 5d: the replay join's three routes, each with
        // its fault-contract route remedy (the identity carriers' verbatim
        // for the first two).
        Detail::EvidenceMissing => crate::fact_admission::REMEDY_EVIDENCE_MISSING,
        Detail::EvidenceRegenerationMismatch => crate::fact_admission::REMEDY_REGENERATION_MISMATCH,
        Detail::EvaluationInputRefused => crate::fact_admission::REMEDY_INPUT_REFUSED,
        // 468c's, X12's and X5's projections name no other detail.
        _ => return Err(MetadataError::Projection),
    })
}

pub(crate) const REMEDY_NO_EMBEDDED_RELEASE: &str =
    "This build carries no embedded signed release. Run a signed OpenSIP release.";
pub(crate) const REMEDY_ACCOUNT_REFUSED: &str = "Run OpenSIP as the account that owns its home directory, with a supported home directory path.";
pub(crate) const REMEDY_NOT_INITIALIZED: &str = "No installation exists for this account. Run an admitted durable analysis (opensip, analyze, fit or audit) first.";
pub(crate) const REMEDY_TCB_IDENTITY: &str = "The OpenSIP release or its core could not be authenticated. Reinstall a signed OpenSIP release.";
pub(crate) const REMEDY_TCB_BOOT: &str =
    "This platform's boot or install-root state is not admitted by the signed platform profile.";
pub(crate) const REMEDY_TCB_PROFILE: &str =
    "This platform is not qualified by the signed platform profile. Use a supported platform.";
pub(crate) const REMEDY_CUSTODY: &str = "A directory or file on the installation path failed its owner, mode or ACL check. Correct its custody and run doctor again.";
pub(crate) const REMEDY_INCOMPLETE: &str =
    "The installation is incomplete. OpenSIP does not repair an incomplete installation.";
pub(crate) const REMEDY_STATE_SCHEMA: &str = "The selected store's state schema is not one this OpenSIP release supports. Run a release that supports it.";
pub(crate) const REMEDY_BUSY: &str =
    "Another OpenSIP process holds the installation. Retry when it finishes.";
pub(crate) const REMEDY_BUDGET: &str =
    "The installation exceeds the bounded work of one invocation and cannot be read.";
pub(crate) const REMEDY_INVARIANT: &str =
    "OpenSIP reached an internal invariant failure. Report this failure.";
pub(crate) const HOST_IO_REMEDY: &str =
    "A filesystem operation on the installation failed. Check the installation path and retry.";

#[cfg(test)]
mod tests {
    include!("doctor_ingress_tests.rs");
}
