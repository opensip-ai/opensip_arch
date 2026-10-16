// Law M3-J1 r5 item 10 (unit J2a): the M3 outcome matrix, included as
// outcomes.rs's cfg(test) module. Each row's termination is checked field
// by field and validated against the selected common-v4 `StepTermination`
// schema; the route registry, the deficiency bridge and the D9 goldens the
// M3 analysis path can reach are restated from their owners and compared.
use super::*;
use serde_json::{Value, json};

/// All 23 newly selected key/origin pairs reach a complete typed failure
/// envelope with this host's allocated RequestId. The source registry is
/// compared independently of the mapper's branch selection.
#[test]
fn native_input_failure_envelopes_match_all_selected_origins() {
    let registry: Value = serde_json::from_str(include_str!(
        "../../../schemas/sources/native-v2.schema.json"
    ))
    .unwrap();
    let rows = &registry["x-opensip-public-route-registry"]["keys"];
    let mut cases = Vec::new();
    for key in [
        ClosureProtocolKey::AnalyzerMismatch,
        ClosureProtocolKey::DeclarationMissing,
        ClosureProtocolKey::DescriptorMismatch,
        ClosureProtocolKey::Unsupported,
    ] {
        for (origin, name) in [
            (
                ClosureProtocolOrigin::AuthenticatedReleaseDeclaration,
                "authenticated-release-declaration",
            ),
            (
                ClosureProtocolOrigin::ExternallySuppliedSpec,
                "externally-supplied-spec",
            ),
            (
                ClosureProtocolOrigin::HostGeneratedInternalLayer,
                "host-generated-internal-layer",
            ),
        ] {
            cases.push((
                NativeRefusal::ClosureProtocol {
                    key,
                    origin,
                    suffix: Some("λ".repeat(4096)),
                },
                name,
            ));
        }
    }
    for key in [
        NativeImportKey::SelfReference,
        NativeImportKey::AcquisitionPath,
        NativeImportKey::JoinMissing,
        NativeImportKey::JoinAmbiguous,
    ] {
        for (origin, name) in [
            (
                NativeImportOrigin::ExternallySuppliedSpec,
                "externally-supplied-spec",
            ),
            (
                NativeImportOrigin::HostGeneratedInternalLayer,
                "host-generated-internal-layer",
            ),
        ] {
            cases.push((
                NativeRefusal::NativeImport {
                    key,
                    origin,
                    suffix: Some("λ".repeat(4096)),
                },
                name,
            ));
        }
    }
    for (origin, name) in [
        (SpecOrigin::ExternalConfiguration, "external-configuration"),
        (
            SpecOrigin::ExternallySuppliedSpec,
            "externally-supplied-spec",
        ),
        (
            SpecOrigin::HostGeneratedInternalLayer,
            "host-generated-internal-layer",
        ),
    ] {
        cases.push((
            NativeRefusal::ConfiguredNativeImport {
                origin,
                suffix: Some("λ".repeat(4096)),
            },
            name,
        ));
    }
    assert_eq!(cases.len(), 23);
    let mut host = MetadataHost::new();
    let context = host.begin().unwrap();
    let allocated = host.request_id(&context).unwrap();
    let schemas = crate::embedded_schema_registry().unwrap();
    for (refusal, origin) in cases {
        let row = &rows[refusal.key()]["byOriginatingBoundary"][origin];
        assert!(row.is_object(), "missing selected key/origin");
        let envelope = host
            .native_input_failure_projection(&context, &refusal)
            .unwrap();
        let value = serde_json::to_value(envelope).unwrap();
        assert_eq!(value["requestId"], allocated);
        assert_eq!(value["termination"]["class"], row["class"]);
        assert_eq!(value["termination"]["errorCode"], row["errorCode"]);
        let exit = if row["class"] == "request-rejected" {
            2
        } else {
            4
        };
        assert_eq!(value["exitCode"], exit);
        if let Some(fault) = row.get("faultCause") {
            assert_eq!(&value["termination"]["faultCause"], fault);
        } else {
            assert!(value["termination"].get("faultCause").is_none());
        }
        let errors = value["errors"].as_array().unwrap();
        assert_eq!(errors.len(), 1);
        assert_eq!(errors[0]["code"], row["envelopeDetail"]);
        if row["domainDetail"].is_null() {
            assert!(value["termination"].get("domainDetail").is_none());
        } else {
            assert_eq!(value["termination"]["domainDetail"], errors[0]);
        }
        let subject = errors[0]["subject"].as_str().unwrap();
        assert_eq!(subject.chars().count(), 1024);
        assert_eq!(subject, bounded_subject(&refusal.raw()));
        let expected_remedy = match row["envelopeDetail"].as_str().unwrap() {
            "native.closure-protocol-invalid" => {
                "Select a component release with a signed role-supported closure protocol declaration consistent with its required joins; for a retained descriptor mismatch, supply the descriptor projected from that signed body. Never patch retained signed bytes."
            }
            "native.input-import-invalid" => {
                "Supply an admitted inert native import with null payload self references and acquisitionSourcePath, selected through exactly one matching context identity join; remove native imports from configuration evidence.importIds. Never patch retained historical bytes."
            }
            "HOST.INVARIANT_VIOLATED" => {
                "the host produced an invalid internal record; report the defect with the retained diagnostic"
            }
            code => panic!("unexpected public detail {code}"),
        };
        assert_eq!(errors[0]["remedy"], expected_remedy);
        for key in ["planId", "runId", "executionId", "plan", "run"] {
            assert!(value.get(key).is_none());
        }
        schemas
            .schema(
                "urn:opensip:product-v1:workflows:evaluator3:command-envelope:7",
                "",
            )
            .unwrap()
            .admit_json(&serde_json::to_vec(&value).unwrap(), 1 << 20)
            .unwrap();
        assert_eq!(native(&refusal).operational, vec![refusal.raw()]);
    }
}

#[test]
fn native_input_failure_refuses_foreign_context_and_old_route() {
    let mut host = MetadataHost::new();
    let context = host.begin().unwrap();
    let mut foreign = MetadataHost::new();
    let foreign_context = foreign.begin().unwrap();
    let refusal = NativeRefusal::NativeImport {
        key: NativeImportKey::JoinMissing,
        origin: NativeImportOrigin::ExternallySuppliedSpec,
        suffix: None,
    };
    assert_eq!(
        host.native_input_failure_projection(&foreign_context, &refusal)
            .unwrap_err(),
        MetadataError::Projection
    );
    let old = NativeRefusal::ReleaseDeclaration {
        key: ReleaseDeclarationKey::Unregistered,
        suffix: None,
    };
    assert_eq!(
        host.native_input_failure_projection(&context, &old)
            .unwrap_err(),
        MetadataError::Projection
    );
    let value = serde_json::to_value(
        host.native_input_failure_projection(&context, &refusal)
            .unwrap(),
    )
    .unwrap();
    assert_eq!(
        value["errors"][0]["subject"],
        "native.input-import-join-missing"
    );
}

const COMMON4: &str = "urn:opensip:product-v1:workflows:evaluator3:common:4";
const RUN: &str = "run3:1111111111111111111111111111111111111111111111111111111111111111";
const EXEC: &str = "exec1_22222222222222222222222222222222";
const COVERAGE: &str = "coverage2:3333333333333333333333333333333333333333333333333333333333333333";
const NAMESPACE: &str = "ns1";
const DIGEST_A: &str = "0aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
const DIGEST_B: &str = "1bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb";

/// The termination as a `StepTermination` instance. Remedies other than the
/// three this projection selects are the envelope's (J3d), so a shape-only
/// placeholder stands in for them here.
fn step_termination(t: &Termination) -> Value {
    let mut value = json!({"class": t.class.to_string()});
    if let Some(code) = t.error_code {
        value["errorCode"] = json!(code.to_string());
    }
    if t.class == Class::OperationalFailed {
        value["faultCause"] = json!(t.fault_cause.to_string());
    }
    if !t.reason_codes.is_empty() {
        value["reasonCodes"] = json!(
            t.reason_codes
                .iter()
                .map(|r| r.to_string())
                .collect::<Vec<_>>()
        );
    }
    if let Some(run_id) = &t.run_id {
        value["runId"] = json!(run_id);
    }
    if let Some(execution_id) = &t.execution_id {
        value["executionId"] = json!(execution_id);
    }
    if let Some(coverage_id) = &t.coverage_id {
        value["coverageId"] = json!(coverage_id);
    }
    if let Some(signal) = t.signal {
        value["signal"] = json!(signal.to_string());
    }
    if let Some(authority) = t.authority {
        value["authority"] = json!(authority.to_string());
    }
    if let Some(detail) = t.detail {
        let mut d =
            json!({"code": detail.to_string(), "remedy": t.remedy.unwrap_or("placeholder")});
        if let Some(subject) = &t.subject {
            d["subject"] = json!(subject);
        }
        value["domainDetail"] = d;
    }
    value
}
fn schema_valid(t: &Termination) -> bool {
    crate::embedded_schema_registry()
        .unwrap()
        .schema(COMMON4, "/$defs/StepTermination")
        .unwrap()
        .admit_json(&serde_json::to_vec(&step_termination(t)).unwrap(), 1 << 20)
        .is_ok()
}
fn deficiencies(all: &[D9Deficiency]) -> Deficiencies {
    Deficiencies::new(all[0], &all[1..]).unwrap()
}
fn manifest(class: ManifestExcludedClass, digest: &str) -> ExcludedManifest {
    ExcludedManifest {
        class,
        manifest_digest: ManifestDigest::parse(digest).unwrap(),
    }
}

/// One expected row: class, exit, errorCode, faultCause, detail, subject,
/// runId, executionId.
struct Expect {
    row: u8,
    observation: Observation,
    class: &'static str,
    exit: u8,
    code: Option<&'static str>,
    fault: &'static str,
    detail: Option<&'static str>,
    subject: Option<&'static str>,
    run_id: Option<&'static str>,
    execution_id: Option<&'static str>,
}
#[allow(clippy::too_many_arguments)]
fn row(
    row: u8,
    observation: Observation,
    class: &'static str,
    exit: u8,
    code: Option<&'static str>,
    fault: &'static str,
    detail: Option<&'static str>,
    subject: Option<&'static str>,
) -> Expect {
    Expect {
        row,
        observation,
        class,
        exit,
        code,
        fault,
        detail,
        subject,
        run_id: None,
        execution_id: None,
    }
}
fn ids(
    mut expect: Expect,
    run_id: Option<&'static str>,
    execution_id: Option<&'static str>,
) -> Expect {
    expect.run_id = run_id;
    expect.execution_id = execution_id;
    expect
}

const RR: &str = "request-rejected";
const OF: &str = "operational-failed";

/// Item 10, one entry per row M3 code can reach or J1 fully specifies.
/// Rows 1 and 49 after admission are `request_identity_unallocated` and
/// `host_panic`; 41, 45, 48 and 50 are not terminations here; row 58 has
/// no observation yet.
fn matrix() -> Vec<Expect> {
    use Observation as O;
    let custody = |s: &'static str| Row::Custody { subject: s };
    vec![
        row(
            2,
            O::HostSpecInvalid {
                key: "WORKFLOW.DEPENDENCY_CYCLE:0".into(),
            },
            OF,
            4,
            Some("SYSTEM.OUTCOME.ILLEGAL_STATE"),
            "host-invariant",
            None,
            None,
        ),
        row(
            3,
            O::Installation(Row::NoEmbeddedRelease),
            RR,
            2,
            Some("REQUEST.PRECONDITION_FAILED"),
            "none",
            Some("CORE.NO_EMBEDDED_RELEASE"),
            None,
        ),
        row(
            4,
            O::Installation(Row::AccountRefused),
            RR,
            2,
            Some("REQUEST.PRECONDITION_FAILED"),
            "none",
            Some("INSTALLATION.ACCOUNT_REFUSED"),
            None,
        ),
        row(
            4,
            O::Installation(Row::PlatformUnqualified),
            RR,
            2,
            Some("EXTENSION.ADMISSION_REJECTED"),
            "none",
            Some("NT-TCB-PROFILE-UNQUALIFIED"),
            Some("platform"),
        ),
        row(
            5,
            O::Installation(custody("ancestor-acl-omitted")),
            RR,
            2,
            Some("CONFIG.INVALID"),
            "none",
            Some("CONFIG.CUSTODY_REFUSED"),
            Some("ancestor-acl-omitted"),
        ),
        row(
            6,
            O::Installation(Row::Incomplete),
            RR,
            2,
            Some("CONFIG.INVALID"),
            "none",
            Some("CONFIG.CUSTODY_REFUSED"),
            Some("installation-incomplete"),
        ),
        row(
            7,
            O::Installation(Row::NotInitialized),
            RR,
            2,
            Some("REQUEST.PRECONDITION_FAILED"),
            "none",
            Some("INSTALLATION.NOT_INITIALIZED"),
            None,
        ),
        row(
            8,
            O::Installation(Row::BackupChoiceRequired),
            RR,
            2,
            Some("REQUEST.PRECONDITION_FAILED"),
            "none",
            Some("storage.backup-choice-required"),
            None,
        ),
        row(
            9,
            O::Installation(Row::Busy),
            OF,
            4,
            Some("LEDGER.BUSY_TIMEOUT"),
            "ledger-busy",
            Some("PROJECT.BUSY"),
            None,
        ),
        row(
            10,
            O::Installation(Row::HostIo),
            OF,
            4,
            Some("HOST.IO_FAILURE"),
            "host-io",
            None,
            None,
        ),
        row(
            11,
            O::Installation(Row::BudgetExhausted),
            OF,
            4,
            Some("SYSTEM.OUTCOME.ILLEGAL_STATE"),
            "host-invariant",
            Some("WORK.BUDGET_EXHAUSTED"),
            None,
        ),
        row(
            12,
            O::CarrierCustody {
                subject: "local-carrier-mode".into(),
            },
            RR,
            2,
            Some("CONFIG.INVALID"),
            "none",
            Some("CONFIG.CUSTODY_REFUSED"),
            Some("local-carrier-mode"),
        ),
        row(
            12,
            O::ConfigurationInvalid { subject: None },
            RR,
            2,
            Some("CONFIG.INVALID"),
            "none",
            Some("CONFIG.INVALID"),
            None,
        ),
        row(
            13,
            O::HostInvariant {
                subject: Some("flags-layer".into()),
            },
            OF,
            4,
            Some("SYSTEM.OUTCOME.ILLEGAL_STATE"),
            "host-invariant",
            Some("HOST.INVARIANT_VIOLATED"),
            Some("flags-layer"),
        ),
        row(
            14,
            O::PolicySelection(PolicySelectionRefusal::Count(2)),
            RR,
            2,
            Some("CONFIG.INVALID"),
            "none",
            Some("CONFIG.INVALID"),
            Some("count:2"),
        ),
        row(
            15,
            O::Installation(Row::ProjectExplicitPath),
            RR,
            2,
            Some("CONFIG.INVALID"),
            "none",
            Some("PROJECT.EXPLICIT_PATH_INVALID"),
            None,
        ),
        row(
            15,
            O::Installation(Row::ProjectRootCustody {
                subject: "identity-contradiction",
            }),
            RR,
            2,
            Some("CONFIG.INVALID"),
            "none",
            Some("PROJECT.ROOT_CUSTODY_REFUSED"),
            Some("identity-contradiction"),
        ),
        row(
            16,
            O::Installation(Row::StateSchemaUnsupported),
            RR,
            2,
            Some("REQUEST.SCHEMA_MAJOR_UNSUPPORTED"),
            "none",
            Some("STATE.SCHEMA_UNSUPPORTED"),
            None,
        ),
        row(
            17,
            O::Installation(Row::TrustNoAdmittedTimeContext),
            RR,
            2,
            Some("REQUEST.PRECONDITION_FAILED"),
            "none",
            Some("TRUST.NO_ADMITTED_TIME_CONTEXT"),
            None,
        ),
        row(
            17,
            O::Installation(Row::TrustContinuation {
                subject: "index:expired".into(),
            }),
            RR,
            2,
            Some("EXTENSION.ADMISSION_REJECTED"),
            "none",
            Some("CONTINUE-CORE-NOT-TRUSTED"),
            Some("index:expired"),
        ),
        row(
            17,
            O::Installation(Row::TrustPayloadNotAdmissible { subject: "catalog" }),
            RR,
            2,
            Some("EXTENSION.ADMISSION_REJECTED"),
            "none",
            Some("PAYLOAD-NOT-ADMISSIBLE"),
            Some("catalog"),
        ),
        row(
            17,
            O::Installation(Row::ClockExcursionForward {
                subject: "beyond-horizon",
            }),
            RR,
            2,
            Some("REQUEST.PRECONDITION_FAILED"),
            "none",
            Some("CLOCK-EXCURSION-FORWARD"),
            Some("beyond-horizon"),
        ),
        row(
            18,
            O::Installation(Row::RevokedDuringOperation {
                subject: "trust-revoked",
            }),
            RR,
            2,
            Some("EXTENSION.ADMISSION_REJECTED"),
            "none",
            Some("TRUST.COMPONENT_REVOKED_DURING_OPERATION"),
            Some("trust-revoked"),
        ),
        row(
            19,
            O::Installation(Row::ObserverFailStop { subject: "stalled" }),
            OF,
            4,
            Some("HOST.IO_FAILURE"),
            "host-io",
            Some("OBSERVER.FAIL_STOP"),
            Some("stalled"),
        ),
        row(
            20,
            O::WorkspaceUnitLimit {
                subject: "WORKSPACE_UNIT_LIMIT:4097>4096".into(),
            },
            RR,
            2,
            Some("REQUEST.UNSATISFIABLE"),
            "none",
            Some("PROJECT.WORKSPACE_UNIT_LIMIT"),
            Some("WORKSPACE_UNIT_LIMIT:4097>4096"),
        ),
        row(
            21,
            O::WorkBudgetExhausted,
            OF,
            4,
            Some("SYSTEM.OUTCOME.ILLEGAL_STATE"),
            "host-invariant",
            Some("WORK.BUDGET_EXHAUSTED"),
            None,
        ),
        row(
            22,
            O::ScopeLimit {
                subject: "snapshotEntries:1048577>1048576".into(),
            },
            RR,
            2,
            Some("REQUEST.UNSATISFIABLE"),
            "none",
            Some("PROJECT.SCOPE_LIMIT"),
            Some("snapshotEntries:1048577>1048576"),
        ),
        row(
            23,
            O::HostIo,
            OF,
            4,
            Some("HOST.IO_FAILURE"),
            "host-io",
            None,
            None,
        ),
        row(
            24,
            O::ExplicitRootWithoutMarker { subject: None },
            RR,
            2,
            Some("CONFIG.INVALID"),
            "none",
            Some("native.explicit-root-without-marker"),
            None,
        ),
        row(
            24,
            O::ExplicitPathInvalid { subject: None },
            RR,
            2,
            Some("CONFIG.INVALID"),
            "none",
            Some("PROJECT.EXPLICIT_PATH_INVALID"),
            None,
        ),
        row(
            25,
            O::DiscoveryInventoryMismatch,
            RR,
            2,
            Some("REQUEST.PRECONDITION_FAILED"),
            "none",
            Some("PROJECT.DISCOVERY_INVENTORY_MISMATCH"),
            None,
        ),
        row(
            25,
            O::Stale(StaleRow::PreparedOutput),
            RR,
            2,
            Some("REQUEST.PRECONDITION_FAILED"),
            "none",
            Some("native.stale-prepared-output"),
            None,
        ),
        row(
            25,
            O::Stale(StaleRow::Import),
            RR,
            2,
            Some("REQUEST.PRECONDITION_FAILED"),
            "none",
            Some("native.stale-import"),
            None,
        ),
        row(
            25,
            O::Stale(StaleRow::PreparedOutputNotInert),
            RR,
            2,
            Some("REQUEST.PRECONDITION_FAILED"),
            "none",
            Some("native.prepared-output-not-inert"),
            None,
        ),
        row(
            26,
            O::Native(NativeRefusal::RequestedCapability {
                key: RequestedCapabilityKey::Unregistered,
                origin: SpecOrigin::ExternalConfiguration,
                suffix: Some("made-up".into()),
            }),
            RR,
            2,
            Some("CONFIG.INVALID"),
            "none",
            Some("CONFIG.INVALID"),
            Some("native.requested-capability-unregistered:made-up"),
        ),
        row(
            26,
            O::Native(NativeRefusal::RequestedCapability {
                key: RequestedCapabilityKey::DuplicateOwnershipTuple,
                origin: SpecOrigin::ExternallySuppliedSpec,
                suffix: None,
            }),
            RR,
            2,
            Some("REQUEST.PRECONDITION_FAILED"),
            "none",
            None,
            None,
        ),
        row(
            26,
            O::Native(NativeRefusal::RequestedCapability {
                key: RequestedCapabilityKey::ModeUnregistered,
                origin: SpecOrigin::HostGeneratedInternalLayer,
                suffix: None,
            }),
            OF,
            4,
            Some("SYSTEM.OUTCOME.ILLEGAL_STATE"),
            "host-invariant",
            None,
            None,
        ),
        row(
            26,
            O::Native(NativeRefusal::RequestedCapability {
                key: RequestedCapabilityKey::ModeNotSelected,
                origin: SpecOrigin::HostGeneratedInternalLayer,
                suffix: Some("calls@ts".into()),
            }),
            RR,
            2,
            Some("REQUEST.UNSATISFIABLE"),
            "none",
            Some("PROVIDER.NOT_SELECTED"),
            Some("native.requested-capability-mode-not-selected:calls@ts"),
        ),
        ids(
            row(
                27,
                O::Analysis(AnalysisOutcome::Committed {
                    run_id: RUN.into(),
                    verdict: Verdict::Indeterminate {
                        deficiencies: deficiencies(&[D9Deficiency::ProviderUnavailable]),
                        coverage_id: Some(COVERAGE.into()),
                        detail: Some(AnalysisDetail::RequiredClosureNotInstalled),
                    },
                }),
                "indeterminate",
                3,
                None,
                "none",
                Some("COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED"),
                None,
            ),
            Some(RUN),
            None,
        ),
        row(
            28,
            O::ClosureBytesCorrupt,
            OF,
            4,
            Some("HOST.IO_FAILURE"),
            "host-io",
            Some("DELIVERY.CLOSURE_BYTES_CORRUPT"),
            None,
        ),
        row(
            28,
            O::ClosureUnspawnable,
            OF,
            4,
            Some("HOST.IO_FAILURE"),
            "host-io",
            Some("DELIVERY.CLOSURE_UNSPAWNABLE"),
            None,
        ),
        row(
            29,
            O::HostInvariant {
                subject: Some("plan:check_plan_pack".into()),
            },
            OF,
            4,
            Some("SYSTEM.OUTCOME.ILLEGAL_STATE"),
            "host-invariant",
            Some("HOST.INVARIANT_VIOLATED"),
            Some("plan:check_plan_pack"),
        ),
        row(
            30,
            O::ProviderProtocol {
                key: "native.worker-fault".into(),
            },
            OF,
            4,
            Some("PROVIDER.PROTOCOL_VIOLATION"),
            "provider-protocol",
            None,
            None,
        ),
        ids(
            row(
                31,
                O::Analysis(AnalysisOutcome::Committed {
                    run_id: RUN.into(),
                    verdict: Verdict::Indeterminate {
                        deficiencies: deficiencies(&[native_deficiency_d9(
                            NativeDeficiency::InputClosureIncomplete,
                        )]),
                        coverage_id: Some(COVERAGE.into()),
                        detail: Some(AnalysisDetail::InputClosureIncomplete),
                    },
                }),
                "indeterminate",
                3,
                None,
                "none",
                Some("input-closure-incomplete"),
                None,
            ),
            Some(RUN),
            None,
        ),
        row(
            31,
            O::Analysis(AnalysisOutcome::Ephemeral(
                EphemeralVerdict::Indeterminate {
                    deficiencies: deficiencies(&[D9Deficiency::BudgetExhausted]),
                },
            )),
            "indeterminate",
            3,
            None,
            "none",
            None,
            None,
        ),
        row(
            32,
            O::Native(NativeRefusal::CoverageCause {
                key: CoverageCauseKey::NotForDeficiency,
                suffix: Some("input-closure-incomplete:capability-missing".into()),
            }),
            OF,
            4,
            Some("PROVIDER.PROTOCOL_VIOLATION"),
            "provider-protocol",
            None,
            None,
        ),
        row(
            32,
            O::ProviderProtocol {
                key: "native.coverage-bijection-mismatch".into(),
            },
            OF,
            4,
            Some("PROVIDER.PROTOCOL_VIOLATION"),
            "provider-protocol",
            None,
            None,
        ),
        ids(
            row(
                33,
                O::Analysis(AnalysisOutcome::Committed {
                    run_id: RUN.into(),
                    verdict: Verdict::Indeterminate {
                        deficiencies: deficiencies(&[D9Deficiency::BudgetExhausted]),
                        coverage_id: None,
                        detail: Some(AnalysisDetail::WorkBudgetExhausted),
                    },
                }),
                "indeterminate",
                3,
                None,
                "none",
                Some("EVALUATION.WORK_BUDGET_EXHAUSTED"),
                None,
            ),
            Some(RUN),
            None,
        ),
        row(
            34,
            O::OutputBoundExceeded,
            OF,
            4,
            Some("OUTPUT.SERIALIZATION_FAILED"),
            "output-serialization",
            Some("EVALUATION.OUTPUT_BOUND_EXCEEDED"),
            None,
        ),
        ids(
            row(
                35,
                O::Analysis(AnalysisOutcome::Committed {
                    run_id: RUN.into(),
                    verdict: Verdict::Pass,
                }),
                "success",
                0,
                None,
                "none",
                None,
                None,
            ),
            Some(RUN),
            None,
        ),
        ids(
            row(
                35,
                O::Analysis(AnalysisOutcome::Committed {
                    run_id: RUN.into(),
                    verdict: Verdict::Fail,
                }),
                "policy-failed",
                1,
                None,
                "none",
                None,
                None,
            ),
            Some(RUN),
            None,
        ),
        row(
            35,
            O::Analysis(AnalysisOutcome::Ephemeral(EphemeralVerdict::Fail)),
            "policy-failed",
            1,
            None,
            "none",
            None,
            None,
        ),
        row(
            35,
            O::Analysis(AnalysisOutcome::Ephemeral(EphemeralVerdict::Pass)),
            "success",
            0,
            None,
            "none",
            None,
            None,
        ),
        row(
            36,
            O::Replay(InstallationTerminationV1 {
                class: Class::OperationalFailed,
                exit: 4,
                error_code: Code::ProviderProtocolViolation,
                fault_cause: Fault::ProviderProtocol,
                detail: Some(Detail::EvaluationInputRefused),
                subject: None,
            }),
            OF,
            4,
            Some("PROVIDER.PROTOCOL_VIOLATION"),
            "provider-protocol",
            Some("EVALUATION.INPUT_REFUSED"),
            None,
        ),
        row(
            37,
            O::Installation(Row::LedgerCorrupt),
            OF,
            4,
            Some("LEDGER.CORRUPT"),
            "ledger-corrupt",
            None,
            None,
        ),
        row(
            37,
            O::Installation(Row::MigrationCorrupt),
            OF,
            4,
            Some("LEDGER.CORRUPT"),
            "ledger-corrupt",
            Some("MIGRATION.CORRUPT"),
            None,
        ),
        row(
            37,
            O::Installation(Row::Invariant),
            OF,
            4,
            Some("SYSTEM.OUTCOME.ILLEGAL_STATE"),
            "host-invariant",
            Some("HOST.INVARIANT_VIOLATED"),
            None,
        ),
        ids(
            row(
                38,
                O::CommitUndetermined {
                    execution_id: EXEC.into(),
                    namespace: NAMESPACE.into(),
                },
                OF,
                4,
                Some("DURABILITY.COMMIT_FAILED"),
                "durability-commit",
                None,
                Some(EXEC),
            ),
            None,
            Some(EXEC),
        ),
        ids(
            row(
                39,
                O::ExistingAttempt {
                    execution_id: EXEC.into(),
                    namespace: NAMESPACE.into(),
                },
                OF,
                4,
                Some("SYSTEM.OUTCOME.ILLEGAL_STATE"),
                "host-invariant",
                Some("HOST.INVARIANT_VIOLATED"),
                Some(EXEC),
            ),
            None,
            Some(EXEC),
        ),
        row(
            40,
            O::CarrierCapacityExhausted {
                namespace: NAMESPACE.into(),
            },
            OF,
            4,
            Some("LEDGER.BUSY_TIMEOUT"),
            "ledger-busy",
            Some("PROJECT.BUSY"),
            Some(NAMESPACE),
        ),
        ids(
            row(
                42,
                O::LatchedAfterAdmission { run_id: RUN.into() },
                OF,
                4,
                Some("DELIVERY.REQUIRED_FAILED"),
                "delivery-required",
                Some("DELIVERY.RENDERER_FAILED_AFTER_COMMIT"),
                None,
            ),
            Some(RUN),
            None,
        ),
        ids(
            row(
                43,
                O::RequiredDeliveryFailed {
                    committed_run: Some(RUN.into()),
                },
                OF,
                4,
                Some("DELIVERY.REQUIRED_FAILED"),
                "delivery-required",
                Some("DELIVERY.RENDERER_FAILED_AFTER_COMMIT"),
                None,
            ),
            Some(RUN),
            None,
        ),
        row(
            44,
            O::RequiredDeliveryFailed {
                committed_run: None,
            },
            OF,
            4,
            Some("DELIVERY.REQUIRED_FAILED"),
            "delivery-required",
            Some("DELIVERY.REQUIRED_PROJECTION_FAILED"),
            None,
        ),
        row(
            46,
            O::Interrupted {
                signal: Signal::Sigint,
                run_id: None,
            },
            "interrupted",
            130,
            None,
            "none",
            None,
            None,
        ),
        ids(
            row(
                47,
                O::Interrupted {
                    signal: Signal::Sigterm,
                    run_id: Some(RUN.into()),
                },
                "interrupted",
                130,
                None,
                "none",
                None,
                None,
            ),
            Some(RUN),
            None,
        ),
        row(
            49,
            O::HostPanicBeforeAdmission,
            OF,
            4,
            Some("SYSTEM.OUTCOME.ILLEGAL_STATE"),
            "host-invariant",
            None,
            None,
        ),
        row(
            51,
            O::EphemeralCannotSupplyAuthority,
            RR,
            2,
            Some("REQUEST.UNSATISFIABLE"),
            "none",
            Some("WORKFLOW.EPHEMERAL_CANNOT_SUPPLY_AUTHORITY"),
            None,
        ),
        row(
            52,
            O::NativeContextRefused {
                key: "native.native-context-closure-unretained:stdlib".into(),
            },
            RR,
            2,
            Some("REQUEST.PRECONDITION_FAILED"),
            "none",
            None,
            None,
        ),
        row(
            53,
            O::PrepareBoundExceeded,
            OF,
            4,
            Some("HOST.IO_FAILURE"),
            "host-io",
            Some("native.prepare-bound-exceeded"),
            None,
        ),
        row(
            54,
            O::AmbientCargoConfig,
            OF,
            4,
            Some("HOST.IO_FAILURE"),
            "host-io",
            Some("native.ambient-cargo-config"),
            None,
        ),
        row(
            55,
            O::Native(NativeRefusal::ReleaseDeclaration {
                key: ReleaseDeclarationKey::PreviewConstant,
                suffix: Some("preview-calls".into()),
            }),
            RR,
            2,
            Some("REQUEST.PRECONDITION_FAILED"),
            "none",
            None,
            None,
        ),
        row(
            56,
            O::ExcludedManifests {
                first: manifest(ManifestExcludedClass::Ee5a, DIGEST_B),
                rest: vec![
                    manifest(ManifestExcludedClass::Ee3b, DIGEST_A),
                    manifest(ManifestExcludedClass::Ee1, DIGEST_B),
                ],
            },
            RR,
            2,
            Some("EXTENSION.ADMISSION_REJECTED"),
            "none",
            Some("PAYLOAD-NOT-ADMISSIBLE"),
            Some(
                "excluded-form:EE-3b:0aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            ),
        ),
        row(
            57,
            O::ExcludedRequest {
                first: RequestExcludedClass::Ee6a,
                rest: vec![RequestExcludedClass::Ee4],
            },
            RR,
            2,
            Some("REQUEST.UNSATISFIABLE"),
            "none",
            Some("PROVIDER.NOT_SELECTED"),
            Some("excluded-form:EE-4"),
        ),
        // M3-J1 r7 row 59 (M3-B r8 item 14a; unit B2-c2).
        row(
            59,
            O::TypescriptConfigUnresolved(ConfigRefusal {
                key: crate::typescript_config::ConfigRefusalKey::ExtendsCycle,
                path: "packages/web/tsconfig.json".to_owned(),
            }),
            RR,
            2,
            Some("CONFIG.INVALID"),
            "none",
            Some("native.typescript-config-unresolved"),
            Some("native.typescript-config-extends-cycle:packages/web/tsconfig.json"),
        ),
    ]
}

/// Item 10 and J-C20: every row's termination, field by field, and schema
/// validity of each against the selected `StepTermination`.
#[test]
fn every_row_projects_to_its_item_10_termination() {
    let matrix = matrix();
    for expect in &matrix {
        let t = project(&expect.observation);
        let at = format!("row {} {:?}", expect.row, expect.observation);
        assert_eq!(t.class.to_string(), expect.class, "{at}");
        assert_eq!(t.exit(), expect.exit, "{at}");
        assert_eq!(
            t.error_code.map(|c| c.to_string()).as_deref(),
            expect.code,
            "{at}"
        );
        assert_eq!(t.fault_cause.to_string(), expect.fault, "{at}");
        assert_eq!(
            t.detail.map(|d| d.to_string()).as_deref(),
            expect.detail,
            "{at}"
        );
        assert_eq!(t.subject.as_deref(), expect.subject, "{at}");
        assert_eq!(t.run_id.as_deref(), expect.run_id, "{at}");
        assert_eq!(t.execution_id.as_deref(), expect.execution_id, "{at}");
        assert!(schema_valid(&t), "{at}: {}", step_termination(&t));
    }
    // Every numbered row of item 10 that has a termination here is covered.
    // Row 58, SYN-1's syntax backend fault, has no observation yet.
    let covered: std::collections::BTreeSet<u8> = matrix.iter().map(|e| e.row).collect();
    let expected: std::collections::BTreeSet<u8> = (2..=59)
        .filter(|row| ![41, 45, 48, 50, 58].contains(row))
        .collect();
    assert_eq!(covered, expected);
}

/// D9's class/exit pairing and the fault map, with the selected
/// `host-invariant` member (NES `hostInvariantSuccessor`).
#[test]
fn every_termination_pairs_exit_code_and_fault_as_d9_does() {
    for expect in matrix() {
        let t = project(&expect.observation);
        match t.class {
            Class::OperationalFailed => {
                let paired = match t.error_code.unwrap() {
                    Code::HostIoFailure => Fault::HostIo,
                    Code::LedgerBusyTimeout => Fault::LedgerBusy,
                    Code::LedgerCorrupt => Fault::LedgerCorrupt,
                    Code::ProviderProtocolViolation => Fault::ProviderProtocol,
                    Code::DurabilityCommitFailed => Fault::DurabilityCommit,
                    Code::DeliveryRequiredFailed => Fault::DeliveryRequired,
                    Code::OutputSerializationFailed => Fault::OutputSerialization,
                    Code::SystemOutcomeIllegalState => Fault::HostInvariant,
                    other => panic!("{other:?}"),
                };
                assert_eq!(t.fault_cause, paired, "{:?}", expect.observation);
            }
            Class::RequestRejected => {
                assert!(t.error_code.is_some());
                assert_eq!(t.fault_cause, Fault::None);
            }
            _ => {
                assert_eq!(t.error_code, None);
                assert_eq!(t.fault_cause, Fault::None);
            }
        }
        assert!(t.reason_codes.is_empty() || t.class == Class::Indeterminate);
        assert_eq!(t.signal.is_some(), t.class == Class::Interrupted);
    }
}

/// Item 10's internal keys: rows 2, 26 (non-configured origins), 30, 32, 52
/// and 55 carry no detail, and their key goes to the operational record.
#[test]
fn absent_details_put_their_key_in_the_operational_record() {
    for (observation, key) in [
        (
            Observation::HostSpecInvalid {
                key: "WORKFLOW.DEPENDENCY_CYCLE:0".into(),
            },
            "WORKFLOW.DEPENDENCY_CYCLE:0",
        ),
        (
            Observation::ProviderProtocol {
                key: "native.worker-fault".into(),
            },
            "native.worker-fault",
        ),
        (
            Observation::NativeContextRefused {
                key: "native.universe-context-binding-mismatch".into(),
            },
            "native.universe-context-binding-mismatch",
        ),
        (
            Observation::Native(NativeRefusal::ReleaseDeclaration {
                key: ReleaseDeclarationKey::Duplicate,
                suffix: Some("calls".into()),
            }),
            "native.release-capability-duplicate:calls",
        ),
        (
            Observation::Native(NativeRefusal::CoverageCause {
                key: CoverageCauseKey::Required,
                suffix: None,
            }),
            "native.coverage-cause-required",
        ),
    ] {
        let t = project(&observation);
        assert_eq!(t.detail, None, "{observation:?}");
        assert_eq!(t.operational, vec![key.to_owned()], "{observation:?}");
    }
    // Rows 53 and 54 carry the registered detail and keep the key.
    assert_eq!(
        project(&Observation::AmbientCargoConfig).operational,
        vec!["native.ambient-cargo-config"]
    );
    assert_eq!(
        project(&Observation::PrepareBoundExceeded).operational,
        vec!["native.prepare-bound-exceeded"]
    );
}

/// Rows 1 and 49: no envelope for an unallocated RequestId; nothing
/// manufactured for a panic after FinalGate admission.
#[test]
fn rows_without_a_termination() {
    assert_eq!(
        request_identity_unallocated(),
        (4, "HOST.IO_FAILURE: request identity allocation failed.")
    );
    assert_eq!(host_panic(true), None);
    assert_eq!(
        host_panic(false),
        Some(project(&Observation::HostPanicBeforeAdmission))
    );
}

/// Row 56 (SD-5, conformed by SD-7): the least manifestDigest, then its
/// first class in the order EE-1, EE-3b, EE-4, EE-5a; every refusal in the
/// operational record; the conformed remedy; no runId or executionId.
#[test]
fn the_excluded_manifest_row_names_the_least_digest_then_the_first_class() {
    let refusals = [
        manifest(ManifestExcludedClass::Ee5a, DIGEST_A),
        manifest(ManifestExcludedClass::Ee4, DIGEST_B),
        manifest(ManifestExcludedClass::Ee1, DIGEST_A),
        manifest(ManifestExcludedClass::Ee1, DIGEST_A),
    ];
    // Whatever the order of discovery, the same detail.
    for first in 0..refusals.len() {
        let rest: Vec<_> = refusals
            .iter()
            .enumerate()
            .filter(|(i, _)| *i != first)
            .map(|(_, r)| r.clone())
            .collect();
        let t = project(&Observation::ExcludedManifests {
            first: refusals[first].clone(),
            rest,
        });
        assert_eq!(
            t.subject.as_deref(),
            Some(format!("excluded-form:EE-1:{DIGEST_A}").as_str())
        );
        assert_eq!(
            t.operational,
            vec![
                format!("excluded-form:EE-1:{DIGEST_A}"),
                format!("excluded-form:EE-5a:{DIGEST_A}"),
                format!("excluded-form:EE-4:{DIGEST_B}"),
            ]
        );
        assert_eq!(t.remedy, Some(REMEDY_EXCLUDED_MANIFEST));
        assert_eq!(
            (t.run_id.as_deref(), t.execution_id.as_deref()),
            (None, None)
        );
    }
    // Every class spells as SD-5's row does; every subject is at most 84.
    for (class, spelled) in [
        (ManifestExcludedClass::Ee1, "EE-1"),
        (ManifestExcludedClass::Ee3b, "EE-3b"),
        (ManifestExcludedClass::Ee4, "EE-4"),
        (ManifestExcludedClass::Ee5a, "EE-5a"),
    ] {
        let t = project(&Observation::ExcludedManifests {
            first: manifest(class, DIGEST_B),
            rest: vec![],
        });
        assert_eq!(
            t.subject,
            Some(format!("excluded-form:{spelled}:{DIGEST_B}"))
        );
        assert!(t.subject.unwrap().len() <= 84);
        assert_eq!(
            (t.class, t.error_code, t.detail),
            (
                Class::RequestRejected,
                Some(Code::ExtensionAdmissionRejected),
                Some(Detail::PayloadNotAdmissible)
            )
        );
    }
    // SD-7's conformed remedy, word for word, within BoundedText.
    assert!(REMEDY_EXCLUDED_MANIFEST.ends_with("or claim a project hook, a reserved or additional root command, or a probe. Remove the component, or install its first-party release."));
    assert!(!REMEDY_EXCLUDED_MANIFEST.contains("declare a project hook"));
    assert!(REMEDY_EXCLUDED_MANIFEST.is_ascii() && REMEDY_EXCLUDED_MANIFEST.len() <= 1024);
}

/// Row 57 (M3-D r5 item 25; SD-7's NE:3539 row): the first class in the
/// order EE-2, EE-4, EE-6a, with `PROVIDER.NOT_SELECTED`'s widened remedy.
#[test]
fn the_request_class_row_names_the_first_class_with_the_widened_remedy() {
    let t = project(&Observation::ExcludedRequest {
        first: RequestExcludedClass::Ee6a,
        rest: vec![RequestExcludedClass::Ee2, RequestExcludedClass::Ee6a],
    });
    assert_eq!(t.subject.as_deref(), Some("excluded-form:EE-2"));
    assert_eq!(
        t.operational,
        vec!["excluded-form:EE-2", "excluded-form:EE-6a"]
    );
    assert_eq!(
        (t.class, t.exit(), t.error_code, t.detail),
        (
            Class::RequestRejected,
            2,
            Some(Code::RequestUnsatisfiable),
            Some(Detail::ProviderNotSelected)
        )
    );
    assert_eq!(t.remedy, Some(REMEDY_PROVIDER_NOT_SELECTED));
    assert_eq!((t.run_id, t.execution_id), (None, None));
    // The widened remedy keeps both of the original clauses (SD-7), and the
    // NOT-SELECTED cell carries the same code-keyed text.
    assert!(
        REMEDY_PROVIDER_NOT_SELECTED
            .starts_with("this capability is not selected for that language mode")
    );
    assert!(REMEDY_PROVIDER_NOT_SELECTED.contains("no promise is made for it"));
    assert_eq!(REMEDY_PROVIDER_NOT_SELECTED.len(), 254);
    let cell = project(&Observation::Native(NativeRefusal::RequestedCapability {
        key: RequestedCapabilityKey::ModeNotSelected,
        origin: SpecOrigin::ExternalConfiguration,
        suffix: None,
    }));
    assert_eq!(cell.remedy, Some(REMEDY_PROVIDER_NOT_SELECTED));
    for (class, spelled) in [
        (RequestExcludedClass::Ee2, "EE-2"),
        (RequestExcludedClass::Ee4, "EE-4"),
        (RequestExcludedClass::Ee6a, "EE-6a"),
    ] {
        assert_eq!(
            project(&Observation::ExcludedRequest {
                first: class,
                rest: vec![]
            })
            .subject,
            Some(format!("excluded-form:{spelled}"))
        );
    }
}

/// SD-5's boundary: an excluded form is never the not-installed golden, and
/// a required closure that is absent is never an excluded form.
#[test]
fn the_excluded_form_row_is_distinct_from_row_27() {
    let excluded = project(&Observation::ExcludedManifests {
        first: manifest(ManifestExcludedClass::Ee1, DIGEST_A),
        rest: vec![],
    });
    let absent = project(&Observation::Analysis(AnalysisOutcome::Committed {
        run_id: RUN.into(),
        verdict: Verdict::Indeterminate {
            deficiencies: deficiencies(&[D9Deficiency::ProviderUnavailable]),
            coverage_id: None,
            detail: Some(AnalysisDetail::RequiredClosureNotInstalled),
        },
    }));
    assert_eq!(
        (excluded.class, excluded.exit()),
        (Class::RequestRejected, 2)
    );
    assert_eq!((absent.class, absent.exit()), (Class::Indeterminate, 3));
    assert!(excluded.reason_codes.is_empty() && excluded.run_id.is_none());
    assert_eq!(
        absent.reason_codes,
        vec![Reason::CoverageProviderUnavailable]
    );
    assert_ne!(excluded.detail, absent.detail);
}

#[test]
fn a_manifest_digest_is_exactly_64_lowercase_hex() {
    assert!(ManifestDigest::parse(DIGEST_A).is_some());
    for bad in [
        "",
        &DIGEST_A[1..],
        &DIGEST_A.to_uppercase(),
        &format!("{DIGEST_A}0"),
        &format!("g{}", &DIGEST_A[1..]),
    ] {
        assert!(ManifestDigest::parse(bad).is_none(), "{bad}");
    }
}

/// NE section 10 (NE:3380-3394): the bridge restated from the native
/// reference model's `DEFICIENCY_TO_D9_DEFICIENCY`, and the reason codes
/// from D9 v1.14's `codeMaps.deficiencyToReasonCode`.
#[test]
fn the_deficiency_bridge_and_the_d9_reason_map_are_total_and_agree() {
    for (native, d9) in [
        ("language-tier-unsupported", "language-tier-unsupported"),
        ("provider-unavailable", "provider-unavailable"),
        ("input-closure-incomplete", "verdict-indeterminate"),
        ("budget-exhausted", "budget-exhausted"),
        ("confidence-floor-unmet", "confidence-floor-unmet"),
        ("derivation-policy-unmet", "verdict-indeterminate"),
        ("resolution-incomplete", "verdict-indeterminate"),
        ("external-consumers-unknown", "verdict-indeterminate"),
        ("required-relation-missing", "required-relation-missing"),
    ] {
        assert_eq!(
            native_deficiency_d9(native.parse().unwrap()).to_string(),
            d9,
            "{native}"
        );
    }
    for (d9, code) in [
        (
            "required-relation-missing",
            "COVERAGE.REQUIRED_RELATION_MISSING",
        ),
        ("provider-unavailable", "COVERAGE.PROVIDER_UNAVAILABLE"),
        (
            "language-tier-unsupported",
            "COVERAGE.LANGUAGE_TIER_UNSUPPORTED",
        ),
        ("budget-exhausted", "COVERAGE.BUDGET_EXHAUSTED"),
        ("convergence-exhausted", "SNAPSHOT.CONVERGENCE_EXHAUSTED"),
        ("baseline-recipe-unsupported", "BASELINE.RECIPE_UNSUPPORTED"),
        ("verdict-indeterminate", "VERDICT.INDETERMINATE"),
        ("query-completeness-unmet", "QUERY.COMPLETENESS_UNMET"),
        ("confidence-floor-unmet", "COVERAGE.CONFIDENCE_FLOOR_UNMET"),
    ] {
        assert_eq!(
            reason_code(d9.parse().unwrap())
                .map(|r| r.to_string())
                .as_deref(),
            Some(code),
            "{d9}"
        );
    }
    assert_eq!(reason_code(D9Deficiency::None), None);
}

/// Run-termination contract section 4: the reasons are the D9 map of the
/// ordered, distinct deficiencies, primary first.
#[test]
fn deficiencies_are_ordered_distinct_and_never_none() {
    let d = deficiencies(&[
        D9Deficiency::ProviderUnavailable,
        D9Deficiency::BudgetExhausted,
    ]);
    assert_eq!(d.primary(), D9Deficiency::ProviderUnavailable);
    assert_eq!(
        d.reason_codes(),
        vec![
            Reason::CoverageProviderUnavailable,
            Reason::CoverageBudgetExhausted
        ]
    );
    assert!(Deficiencies::new(D9Deficiency::None, &[]).is_none());
    assert!(Deficiencies::new(D9Deficiency::BudgetExhausted, &[D9Deficiency::None]).is_none());
    assert!(
        Deficiencies::new(
            D9Deficiency::BudgetExhausted,
            &[D9Deficiency::BudgetExhausted]
        )
        .is_none()
    );
}

/// NES `x-opensip-public-route-registry`, restated key by key: class, code,
/// fault, detail and envelope detail for every possible origin.
#[test]
fn the_route_registry_is_restated_key_by_key() {
    use RequestedCapabilityKey as Q;
    use SpecOrigin as S;
    let malformed = [
        (Q::Unregistered, "native.requested-capability-unregistered"),
        (
            Q::ModeUnregistered,
            "native.requested-capability-mode-unregistered",
        ),
        (
            Q::DuplicateOwnershipTuple,
            "native.requested-capability-duplicate-ownership-tuple",
        ),
    ];
    for (key, spelled) in malformed {
        for (origin, class, code, fault, detail, envelope) in [
            (
                S::ExternalConfiguration,
                RR,
                "CONFIG.INVALID",
                "none",
                Some("CONFIG.INVALID"),
                "CONFIG.INVALID",
            ),
            (
                S::ExternallySuppliedSpec,
                RR,
                "REQUEST.PRECONDITION_FAILED",
                "none",
                None,
                "native.capability-spec-invalid",
            ),
            (
                S::HostGeneratedInternalLayer,
                OF,
                "SYSTEM.OUTCOME.ILLEGAL_STATE",
                "host-invariant",
                None,
                "HOST.INVARIANT_VIOLATED",
            ),
        ] {
            let refusal = NativeRefusal::RequestedCapability {
                key,
                origin,
                suffix: None,
            };
            assert_eq!(refusal.key(), spelled);
            let t = project(&Observation::Native(refusal.clone()));
            assert_eq!(
                (
                    t.class.to_string().as_str(),
                    t.error_code.unwrap().to_string().as_str(),
                    t.fault_cause.to_string().as_str()
                ),
                (class, code, fault),
                "{spelled} {origin:?}"
            );
            assert_eq!(t.detail.map(|d| d.to_string()).as_deref(), detail);
            assert_eq!(refusal.envelope_detail().to_string(), envelope);
            assert!(schema_valid(&t));
        }
    }
    for origin in [
        S::ExternalConfiguration,
        S::ExternallySuppliedSpec,
        S::HostGeneratedInternalLayer,
    ] {
        let refusal = NativeRefusal::RequestedCapability {
            key: Q::ModeNotSelected,
            origin,
            suffix: None,
        };
        let t = project(&Observation::Native(refusal.clone()));
        assert_eq!(
            (t.class, t.error_code, t.detail),
            (
                Class::RequestRejected,
                Some(Code::RequestUnsatisfiable),
                Some(Detail::ProviderNotSelected)
            )
        );
        assert_eq!(
            t.subject.as_deref(),
            Some("native.requested-capability-mode-not-selected")
        );
        assert_eq!(refusal.envelope_detail(), Detail::ProviderNotSelected);
    }
    use ReleaseDeclarationKey as R;
    for (key, spelled) in [
        (R::Unregistered, "native.release-capability-unregistered"),
        (
            R::ModeUnregistered,
            "native.release-capability-mode-unregistered",
        ),
        (
            R::ModeNotSelected,
            "native.release-capability-mode-not-selected",
        ),
        (R::Duplicate, "native.release-capability-duplicate"),
        (
            R::PreviewConstant,
            "native.release-capability-preview-constant",
        ),
    ] {
        let refusal = NativeRefusal::ReleaseDeclaration { key, suffix: None };
        assert_eq!(refusal.key(), spelled);
        let t = project(&Observation::Native(refusal.clone()));
        assert_eq!(
            (t.class, t.error_code, t.detail),
            (
                Class::RequestRejected,
                Some(Code::RequestPreconditionFailed),
                None
            )
        );
        assert_eq!(
            refusal.envelope_detail(),
            Detail::NativeReleaseDeclarationInvalid
        );
    }
    use CoverageCauseKey as K;
    for (key, spelled) in [
        (K::Required, "native.coverage-cause-required"),
        (K::MustBeNull, "native.coverage-cause-must-be-null"),
        (
            K::NotForDeficiency,
            "native.coverage-cause-not-for-deficiency",
        ),
        (
            K::CarrierUnsupported,
            "native.coverage-cause-carrier-unsupported",
        ),
        (
            K::RelationNotInScope,
            "native.coverage-cause-relation-not-in-scope",
        ),
        (
            K::WithoutDeficiency,
            "native.coverage-cause-without-deficiency",
        ),
        (
            K::RegistryRowMissing,
            "native.coverage-cause-registry-row-missing",
        ),
    ] {
        let refusal = NativeRefusal::CoverageCause { key, suffix: None };
        assert_eq!(refusal.key(), spelled);
        let t = project(&Observation::Native(refusal.clone()));
        assert_eq!(
            (t.class, t.error_code, t.fault_cause, t.detail),
            (
                Class::OperationalFailed,
                Some(Code::ProviderProtocolViolation),
                Fault::ProviderProtocol,
                None
            )
        );
        assert_eq!(
            refusal.envelope_detail(),
            Detail::NativeCoverageCauseUnsupported
        );
    }
}

/// NES `subjectBoundLaw`: a subject over 1024 code points keeps the key,
/// a leading window and the SHA-256 of the whole subject's UTF-8 bytes,
/// exactly 1024 code points; distinct values stay distinct.
#[test]
fn a_long_subject_is_bounded_with_its_digest() {
    let short = "native.requested-capability-unregistered:x";
    assert_eq!(bounded_subject(short), short);
    let at_bound: String = "é".repeat(1024);
    assert_eq!(bounded_subject(&at_bound), at_bound);
    let long = format!(
        "native.requested-capability-mode-unregistered:{}",
        "é".repeat(4096)
    );
    let bounded = bounded_subject(&long);
    assert_eq!(bounded.chars().count(), 1024);
    assert!(bounded.starts_with("native.requested-capability-mode-unregistered:é"));
    let digest = opensip_identity::digest_hex(&opensip_identity::raw_sha256(long.as_bytes()));
    assert!(bounded.ends_with(&format!("...#sha256:{digest}")));
    let other = format!("{long}x");
    assert_ne!(bounded_subject(&other), bounded);
    let t = project(&Observation::Native(NativeRefusal::RequestedCapability {
        key: RequestedCapabilityKey::ModeUnregistered,
        origin: SpecOrigin::ExternalConfiguration,
        suffix: Some("é".repeat(4096)),
    }));
    assert_eq!(t.subject.as_deref(), Some(bounded.as_str()));
    assert!(schema_valid(&t));
}

/// (golden, observation, class, errorCode, reasonCodes).
type Golden = (
    &'static str,
    Observation,
    &'static str,
    Option<&'static str>,
    Vec<&'static str>,
);
/// The D9 v1.14 goldens the M3 analysis path can reach, restated (class,
/// error or reason codes), each from its J2a observation. Where a golden
/// lists an id that item 10 does not carry (`user-interrupt-finite`'s and
/// `analysis-provider-protocol-prevents-seal`'s executionId), only the
/// class and codes are compared: ENV7's interrupted branch and J1 rows 30
/// and 46 carry none.
#[test]
fn the_d9_goldens_of_the_analysis_path() {
    let committed = |verdict| {
        Observation::Analysis(AnalysisOutcome::Committed {
            run_id: RUN.into(),
            verdict,
        })
    };
    let indeterminate = |all: &[D9Deficiency]| Verdict::Indeterminate {
        deficiencies: deficiencies(all),
        coverage_id: None,
        detail: None,
    };
    let cases: Vec<Golden> = vec![
        (
            "analysis-pass",
            committed(Verdict::Pass),
            "success",
            None,
            vec![],
        ),
        (
            "analysis-policy-fail",
            committed(Verdict::Fail),
            "policy-failed",
            None,
            vec![],
        ),
        (
            "analysis-required-coverage-missing",
            committed(indeterminate(&[D9Deficiency::RequiredRelationMissing])),
            "indeterminate",
            None,
            vec!["COVERAGE.REQUIRED_RELATION_MISSING"],
        ),
        (
            "analysis-verdict-indeterminate",
            committed(indeterminate(&[D9Deficiency::VerdictIndeterminate])),
            "indeterminate",
            None,
            vec!["VERDICT.INDETERMINATE"],
        ),
        (
            "analysis-required-provider-unavailable",
            committed(indeterminate(&[D9Deficiency::ProviderUnavailable])),
            "indeterminate",
            None,
            vec!["COVERAGE.PROVIDER_UNAVAILABLE"],
        ),
        (
            "analysis-language-tier-unsupported",
            committed(indeterminate(&[D9Deficiency::LanguageTierUnsupported])),
            "indeterminate",
            None,
            vec!["COVERAGE.LANGUAGE_TIER_UNSUPPORTED"],
        ),
        (
            "analysis-budget-exhausted",
            committed(indeterminate(&[D9Deficiency::BudgetExhausted])),
            "indeterminate",
            None,
            vec!["COVERAGE.BUDGET_EXHAUSTED"],
        ),
        (
            "analysis-confidence-floor-unmet",
            committed(indeterminate(&[D9Deficiency::ConfidenceFloorUnmet])),
            "indeterminate",
            None,
            vec!["COVERAGE.CONFIDENCE_FLOOR_UNMET"],
        ),
        (
            "analysis-multiple-deficiencies",
            committed(indeterminate(&[
                D9Deficiency::ProviderUnavailable,
                D9Deficiency::BudgetExhausted,
            ])),
            "indeterminate",
            None,
            vec!["COVERAGE.PROVIDER_UNAVAILABLE", "COVERAGE.BUDGET_EXHAUSTED"],
        ),
        (
            "analysis-authorized-ephemeral",
            Observation::Analysis(AnalysisOutcome::Ephemeral(EphemeralVerdict::Pass)),
            "success",
            None,
            vec![],
        ),
        (
            "analysis-provider-protocol-prevents-seal",
            Observation::ProviderProtocol {
                key: "native.worker-fault".into(),
            },
            "operational-failed",
            Some("PROVIDER.PROTOCOL_VIOLATION"),
            vec![],
        ),
        (
            "analysis-durability-failed",
            Observation::CommitUndetermined {
                execution_id: EXEC.into(),
                namespace: NAMESPACE.into(),
            },
            "operational-failed",
            Some("DURABILITY.COMMIT_FAILED"),
            vec![],
        ),
        (
            "pre-admission-invalid-config",
            Observation::ConfigurationInvalid { subject: None },
            "request-rejected",
            Some("CONFIG.INVALID"),
            vec![],
        ),
        (
            "pre-admission-host-io-failure",
            Observation::HostIo,
            "operational-failed",
            Some("HOST.IO_FAILURE"),
            vec![],
        ),
        (
            "ledger-busy-timeout-exceeded",
            Observation::Installation(Row::Busy),
            "operational-failed",
            Some("LEDGER.BUSY_TIMEOUT"),
            vec![],
        ),
        (
            "extension-admission-rejected",
            Observation::ExcludedManifests {
                first: manifest(ManifestExcludedClass::Ee1, DIGEST_A),
                rest: vec![],
            },
            "request-rejected",
            Some("EXTENSION.ADMISSION_REJECTED"),
            vec![],
        ),
        (
            "required-delivery-failed",
            Observation::RequiredDeliveryFailed {
                committed_run: Some(RUN.into()),
            },
            "operational-failed",
            Some("DELIVERY.REQUIRED_FAILED"),
            vec![],
        ),
        (
            "user-interrupt-finite",
            Observation::Interrupted {
                signal: Signal::Sigint,
                run_id: None,
            },
            "interrupted",
            None,
            vec![],
        ),
    ];
    for (golden, observation, class, code, reasons) in cases {
        let t = project(&observation);
        assert_eq!(t.class.to_string(), class, "{golden}");
        assert_eq!(
            t.error_code.map(|c| c.to_string()).as_deref(),
            code,
            "{golden}"
        );
        assert_eq!(
            t.reason_codes
                .iter()
                .map(|r| r.to_string())
                .collect::<Vec<_>>(),
            reasons,
            "{golden}"
        );
        assert!(schema_valid(&t), "{golden}");
    }
}

/// Run-termination contract section 7.4: a committed Run carries its runId
/// and no authority; an ephemeral result carries `authority: ephemeral`,
/// never a runId, and no detail, on every verdict class.
#[test]
fn authority_follows_the_committed_run_or_the_ephemeral_attempt() {
    for verdict in [
        Verdict::Pass,
        Verdict::Fail,
        Verdict::Indeterminate {
            deficiencies: deficiencies(&[D9Deficiency::BudgetExhausted]),
            coverage_id: Some(COVERAGE.into()),
            detail: None,
        },
    ] {
        let t = project(&Observation::Analysis(AnalysisOutcome::Committed {
            run_id: RUN.into(),
            verdict,
        }));
        assert_eq!((t.run_id.as_deref(), t.authority), (Some(RUN), None));
        assert!(schema_valid(&t));
    }
    for verdict in [
        EphemeralVerdict::Pass,
        EphemeralVerdict::Fail,
        EphemeralVerdict::Indeterminate {
            deficiencies: deficiencies(&[D9Deficiency::ProviderUnavailable]),
        },
    ] {
        let t = project(&Observation::Analysis(AnalysisOutcome::Ephemeral(verdict)));
        assert_eq!(
            (
                t.run_id.as_deref(),
                t.authority,
                t.detail,
                t.coverage_id.as_deref()
            ),
            (None, Some(Authority::Ephemeral), None, None)
        );
        assert!(schema_valid(&t));
    }
}

/// The exit derives from the class by the fixed table only (WS:1355-1356).
#[test]
fn the_exit_table_is_fixed() {
    for (class, exit) in [
        (Class::Success, 0),
        (Class::PolicyFailed, 1),
        (Class::RequestRejected, 2),
        (Class::Indeterminate, 3),
        (Class::OperationalFailed, 4),
        (Class::Interrupted, 130),
    ] {
        assert_eq!(exit_code(class), exit);
    }
}

/// Contract successor S10 (M3-B r8 item 14a): the new public detail is a
/// member of the generated vocabulary, and its D9 row (request-rejected,
/// exit 2, `CONFIG.INVALID`) with its code-keyed remedy and a subject is an
/// admitted `StepTermination`. The remedy is the S10 model copies' string,
/// byte for byte.
#[test]
fn the_typescript_configuration_detail_is_admitted() {
    let detail: Detail = "native.typescript-config-unresolved".parse().unwrap();
    assert_eq!(detail, Detail::NativeTypescriptConfigUnresolved);
    assert_eq!(detail.to_string(), "native.typescript-config-unresolved");
    assert_eq!(REMEDY_TYPESCRIPT_CONFIG_UNRESOLVED.len(), 568);
    assert!(REMEDY_TYPESCRIPT_CONFIG_UNRESOLVED.is_ascii());
    assert_eq!(
        opensip_identity::digest_hex(&opensip_identity::raw_sha256(
            REMEDY_TYPESCRIPT_CONFIG_UNRESOLVED.as_bytes()
        )),
        "98fe066f2e22692647d5d6692bc876e711909496dd788eeaa5d05e3d3bd80903"
    );
    let t = Termination {
        remedy: Some(REMEDY_TYPESCRIPT_CONFIG_UNRESOLVED),
        ..Termination::rejected(
            Code::ConfigInvalid,
            Some(detail),
            Some("native.typescript-config-extends-cycle:packages/web/tsconfig.json".to_owned()),
        )
    };
    assert_eq!(exit_code(t.class), 2);
    assert!(schema_valid(&t));
    assert_eq!(
        step_termination(&t)["domainDetail"]["remedy"],
        REMEDY_TYPESCRIPT_CONFIG_UNRESOLVED
    );
}
