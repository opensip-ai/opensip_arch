//! Law 468 r5 item 6: the D9 projection of every creator and existing-root
//! admission row. Class, exit, error code, fault cause and domain detail are
//! exactly the rows published by the 468a diagnostic successor
//! (`existing-root-diagnostics-468a/diagnostic-routes.json`), plus law 468
//! r5's incomplete-installation row. Law X4 r7 item 8 (unit X4a) adds the
//! fenced trust admission's rows (law X4T r9 item 10) and the live guards'
//! two rows, each on an existing detail with the class S12 fixes for it. Law
//! X3d r6 item 9 (unit X3d-1) adds the commit facade's quarantine,
//! durability and project-owner rows, the same way. The
//! match is exhaustive, so a new row cannot compile without its termination.
//! Nothing emits this yet: no CLI command is wired (464 item 7).
use opensip_contracts::generated::evidence::{
    Common4D9Class as Class, Common4D9ErrorCode as Code, Common4D9FaultCause as Fault,
    Common4DomainDetailCode as Detail,
};
use opensip_security::{InstallationTermination as Row, RootDetail, TcbDetail};

/// One public termination. `detail` is absent only where the route names
/// none (the host I/O row); `subject` only where the route names one.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct InstallationTerminationV1 {
    pub class: Class,
    pub exit: u8,
    pub error_code: Code,
    pub fault_cause: Fault,
    pub detail: Option<Detail>,
    pub subject: Option<String>,
}

fn rejected(
    error_code: Code,
    detail: Detail,
    subject: Option<String>,
) -> InstallationTerminationV1 {
    InstallationTerminationV1 {
        class: Class::RequestRejected,
        exit: 2,
        error_code,
        fault_cause: Fault::None,
        detail: Some(detail),
        subject,
    }
}
fn failed(
    error_code: Code,
    fault_cause: Fault,
    detail: Option<Detail>,
) -> InstallationTerminationV1 {
    InstallationTerminationV1 {
        class: Class::OperationalFailed,
        exit: 4,
        error_code,
        fault_cause,
        detail,
        subject: None,
    }
}

/// The one termination for a row of law 468 item 6.
pub fn installation_termination(row: &Row) -> InstallationTerminationV1 {
    let admission = |detail, subject: &str| {
        rejected(
            Code::ExtensionAdmissionRejected,
            detail,
            Some(subject.to_owned()),
        )
    };
    match row {
        Row::NoEmbeddedRelease => rejected(
            Code::RequestPreconditionFailed,
            Detail::CoreNoEmbeddedRelease,
            None,
        ),
        Row::AccountRefused => rejected(
            Code::RequestPreconditionFailed,
            Detail::InstallationAccountRefused,
            None,
        ),
        Row::BackupChoiceRequired => rejected(
            Code::RequestPreconditionFailed,
            Detail::StorageBackupChoiceRequired,
            None,
        ),
        Row::NotInitialized => rejected(
            Code::RequestPreconditionFailed,
            Detail::InstallationNotInitialized,
            None,
        ),
        Row::CoreRefused { subject } => admission(Detail::NtTcbIdentity, subject),
        Row::PlatformDecision { detail, subject } => admission(
            match detail {
                TcbDetail::Boot => Detail::NtTcbBoot,
                TcbDetail::Identity => Detail::NtTcbIdentity,
                TcbDetail::ProfileUnqualified => Detail::NtTcbProfileUnqualified,
            },
            subject,
        ),
        Row::PlatformUnqualified => admission(Detail::NtTcbProfileUnqualified, "platform"),
        Row::InstallRootFilesystem => admission(Detail::NtTcbBoot, "INSTALL_ROOT_FS"),
        Row::Custody { subject } => rejected(
            Code::ConfigInvalid,
            Detail::ConfigCustodyRefused,
            Some((*subject).to_owned()),
        ),
        Row::Incomplete => rejected(
            Code::ConfigInvalid,
            Detail::ConfigCustodyRefused,
            Some("installation-incomplete".to_owned()),
        ),
        // Law X3a item 5: the existing detail, with the class and error code
        // its S12 row fixes (security-and-lifecycle.md, the schema rows).
        Row::StateSchemaUnsupported => rejected(
            Code::RequestSchemaMajorUnsupported,
            Detail::StateSchemaUnsupported,
            None,
        ),
        Row::Busy => failed(
            Code::LedgerBusyTimeout,
            Fault::LedgerBusy,
            Some(Detail::ProjectBusy),
        ),
        Row::HostIo => failed(Code::HostIoFailure, Fault::HostIo, None),
        Row::BudgetExhausted => failed(
            Code::SystemOutcomeIllegalState,
            Fault::HostInvariant,
            Some(Detail::WorkBudgetExhausted),
        ),
        // Law X4T r9 item 10, with S12's classes: F absent and the clock
        // excursion are precondition failures; the continuation row, every
        // `ROOT.*` chain detail but the schema-major one, and
        // `PAYLOAD-NOT-ADMISSIBLE` are admission rejections.
        Row::TrustNoAdmittedTimeContext => rejected(
            Code::RequestPreconditionFailed,
            Detail::TrustNoAdmittedTimeContext,
            None,
        ),
        Row::TrustContinuation { subject } => admission(Detail::ContinueCoreNotTrusted, subject),
        Row::TrustIndexContinuation { subject } => {
            admission(Detail::ContinueIndexNotTrusted, subject)
        }
        Row::TrustComponentContinuation { subject } => {
            admission(Detail::ContinueComponentNotTrusted, subject)
        }
        Row::TrustRoot { detail, subject } => {
            let code = match detail {
                RootDetail::SchemaUnsupported => Code::RequestSchemaMajorUnsupported,
                _ => Code::ExtensionAdmissionRejected,
            };
            let detail = match detail {
                RootDetail::ChainGap => Detail::RootChainGap,
                RootDetail::ChainBackdated => Detail::RootChainBackdated,
                RootDetail::ChainOldThreshold => Detail::RootChainOldThreshold,
                RootDetail::ChainNewThreshold => Detail::RootChainNewThreshold,
                RootDetail::FinalExpired => Detail::RootFinalExpired,
                RootDetail::FinalFuture => Detail::RootFinalFuture,
                RootDetail::ExpiredNoChain => Detail::RootExpiredNoChain,
                RootDetail::StateInconsistent => Detail::RootStateInconsistent,
                RootDetail::SchemaUnsupported => Detail::RootSchemaUnsupported,
            };
            rejected(code, detail, Some(subject.clone()))
        }
        Row::TrustPayloadNotAdmissible { subject } => {
            admission(Detail::PayloadNotAdmissible, subject)
        }
        Row::ClockExcursionForward { subject } => rejected(
            Code::RequestPreconditionFailed,
            Detail::ClockExcursionForward,
            Some((*subject).to_owned()),
        ),
        // Law X4 r7 item 8: S12's revoked-during-operation and
        // `OBSERVER.FAIL_STOP` rows.
        Row::RevokedDuringOperation { subject } => {
            admission(Detail::TrustComponentRevokedDuringOperation, subject)
        }
        Row::ObserverFailStop { subject } => InstallationTerminationV1 {
            subject: Some((*subject).to_owned()),
            ..failed(
                Code::HostIoFailure,
                Fault::HostIo,
                Some(Detail::ObserverFailStop),
            )
        },
        // Law X3d r6 item 9, with S12's rows: a journal or ledger
        // quarantine publishes no detail; a carrier migration footprint at a
        // writer open is `MIGRATION.CORRUPT`; an undetermined `COMMIT` is the
        // durability row.
        Row::LedgerCorrupt => failed(Code::LedgerCorrupt, Fault::LedgerCorrupt, None),
        Row::MigrationCorrupt => failed(
            Code::LedgerCorrupt,
            Fault::LedgerCorrupt,
            Some(Detail::MigrationCorrupt),
        ),
        Row::CommitUndetermined => {
            failed(Code::DurabilityCommitFailed, Fault::DurabilityCommit, None)
        }
        // Law X2 item 8's project rows, with S12's classes.
        Row::ProjectRootCustody { subject } => rejected(
            Code::ConfigInvalid,
            Detail::ProjectRootCustodyRefused,
            Some((*subject).to_owned()),
        ),
        Row::ProjectExplicitPath => rejected(
            Code::ConfigInvalid,
            Detail::ProjectExplicitPathInvalid,
            None,
        ),
        Row::ProjectScopeLimit { subject } => rejected(
            Code::RequestUnsatisfiable,
            Detail::ProjectScopeLimit,
            Some(subject.clone()),
        ),
        // Not a row of item 6: a broken caller. The existing host-invariant
        // pairing, with the existing HOST.INVARIANT_VIOLATED detail.
        Row::Interrupted { .. } => installation_termination(&Row::Invariant),
        Row::Invariant => failed(
            Code::SystemOutcomeIllegalState,
            Fault::HostInvariant,
            Some(Detail::HostInvariantViolated),
        ),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    /// (row, class, exit, errorCode, faultCause, detail, subject), spelled as
    /// `diagnostic-routes.json` of 468a spells them (the incomplete row from
    /// law 468 r5 item 6).
    #[allow(clippy::type_complexity)]
    fn table() -> Vec<(
        Row,
        &'static str,
        u8,
        &'static str,
        &'static str,
        Option<&'static str>,
        Option<&'static str>,
    )> {
        vec![
            (
                Row::NoEmbeddedRelease,
                "request-rejected",
                2,
                "REQUEST.PRECONDITION_FAILED",
                "none",
                Some("CORE.NO_EMBEDDED_RELEASE"),
                None,
            ),
            (
                Row::AccountRefused,
                "request-rejected",
                2,
                "REQUEST.PRECONDITION_FAILED",
                "none",
                Some("INSTALLATION.ACCOUNT_REFUSED"),
                None,
            ),
            (
                Row::BackupChoiceRequired,
                "request-rejected",
                2,
                "REQUEST.PRECONDITION_FAILED",
                "none",
                Some("storage.backup-choice-required"),
                None,
            ),
            (
                Row::NotInitialized,
                "request-rejected",
                2,
                "REQUEST.PRECONDITION_FAILED",
                "none",
                Some("INSTALLATION.NOT_INITIALIZED"),
                None,
            ),
            (
                Row::CoreRefused {
                    subject: "release-revoked",
                },
                "request-rejected",
                2,
                "EXTENSION.ADMISSION_REJECTED",
                "none",
                Some("NT-TCB-IDENTITY"),
                Some("release-revoked"),
            ),
            (
                Row::PlatformDecision {
                    detail: TcbDetail::Boot,
                    subject: "SIP_DISABLED".into(),
                },
                "request-rejected",
                2,
                "EXTENSION.ADMISSION_REJECTED",
                "none",
                Some("NT-TCB-BOOT"),
                Some("SIP_DISABLED"),
            ),
            (
                Row::PlatformDecision {
                    detail: TcbDetail::Identity,
                    subject: "BUILD_GRAMMAR".into(),
                },
                "request-rejected",
                2,
                "EXTENSION.ADMISSION_REJECTED",
                "none",
                Some("NT-TCB-IDENTITY"),
                Some("BUILD_GRAMMAR"),
            ),
            (
                Row::PlatformDecision {
                    detail: TcbDetail::ProfileUnqualified,
                    subject: "MACOS_MAJOR_28".into(),
                },
                "request-rejected",
                2,
                "EXTENSION.ADMISSION_REJECTED",
                "none",
                Some("NT-TCB-PROFILE-UNQUALIFIED"),
                Some("MACOS_MAJOR_28"),
            ),
            (
                Row::PlatformUnqualified,
                "request-rejected",
                2,
                "EXTENSION.ADMISSION_REJECTED",
                "none",
                Some("NT-TCB-PROFILE-UNQUALIFIED"),
                Some("platform"),
            ),
            (
                Row::InstallRootFilesystem,
                "request-rejected",
                2,
                "EXTENSION.ADMISSION_REJECTED",
                "none",
                Some("NT-TCB-BOOT"),
                Some("INSTALL_ROOT_FS"),
            ),
            (
                Row::Custody {
                    subject: "ancestor-acl-omitted",
                },
                "request-rejected",
                2,
                "CONFIG.INVALID",
                "none",
                Some("CONFIG.CUSTODY_REFUSED"),
                Some("ancestor-acl-omitted"),
            ),
            (
                Row::Incomplete,
                "request-rejected",
                2,
                "CONFIG.INVALID",
                "none",
                Some("CONFIG.CUSTODY_REFUSED"),
                Some("installation-incomplete"),
            ),
            (
                Row::StateSchemaUnsupported,
                "request-rejected",
                2,
                "REQUEST.SCHEMA_MAJOR_UNSUPPORTED",
                "none",
                Some("STATE.SCHEMA_UNSUPPORTED"),
                None,
            ),
            (
                Row::Busy,
                "operational-failed",
                4,
                "LEDGER.BUSY_TIMEOUT",
                "ledger-busy",
                Some("PROJECT.BUSY"),
                None,
            ),
            (
                Row::HostIo,
                "operational-failed",
                4,
                "HOST.IO_FAILURE",
                "host-io",
                None,
                None,
            ),
            (
                Row::BudgetExhausted,
                "operational-failed",
                4,
                "SYSTEM.OUTCOME.ILLEGAL_STATE",
                "host-invariant",
                Some("WORK.BUDGET_EXHAUSTED"),
                None,
            ),
            (
                Row::TrustNoAdmittedTimeContext,
                "request-rejected",
                2,
                "REQUEST.PRECONDITION_FAILED",
                "none",
                Some("TRUST.NO_ADMITTED_TIME_CONTEXT"),
                None,
            ),
            (
                Row::TrustContinuation {
                    subject: "index:expired".into(),
                },
                "request-rejected",
                2,
                "EXTENSION.ADMISSION_REJECTED",
                "none",
                Some("CONTINUE-CORE-NOT-TRUSTED"),
                Some("index:expired"),
            ),
            (
                Row::TrustRoot {
                    detail: RootDetail::ChainGap,
                    subject: "link:1".into(),
                },
                "request-rejected",
                2,
                "EXTENSION.ADMISSION_REJECTED",
                "none",
                Some("ROOT.CHAIN_GAP"),
                Some("link:1"),
            ),
            (
                Row::TrustRoot {
                    detail: RootDetail::SchemaUnsupported,
                    subject: "anchor".into(),
                },
                "request-rejected",
                2,
                "REQUEST.SCHEMA_MAJOR_UNSUPPORTED",
                "none",
                Some("ROOT.SCHEMA_UNSUPPORTED"),
                Some("anchor"),
            ),
            (
                Row::TrustPayloadNotAdmissible { subject: "catalog" },
                "request-rejected",
                2,
                "EXTENSION.ADMISSION_REJECTED",
                "none",
                Some("PAYLOAD-NOT-ADMISSIBLE"),
                Some("catalog"),
            ),
            (
                Row::ClockExcursionForward {
                    subject: "beyond-horizon",
                },
                "request-rejected",
                2,
                "REQUEST.PRECONDITION_FAILED",
                "none",
                Some("CLOCK-EXCURSION-FORWARD"),
                Some("beyond-horizon"),
            ),
            (
                Row::RevokedDuringOperation {
                    subject: "trust-revoked",
                },
                "request-rejected",
                2,
                "EXTENSION.ADMISSION_REJECTED",
                "none",
                Some("TRUST.COMPONENT_REVOKED_DURING_OPERATION"),
                Some("trust-revoked"),
            ),
            (
                Row::ObserverFailStop { subject: "stalled" },
                "operational-failed",
                4,
                "HOST.IO_FAILURE",
                "host-io",
                Some("OBSERVER.FAIL_STOP"),
                Some("stalled"),
            ),
            (
                Row::Invariant,
                "operational-failed",
                4,
                "SYSTEM.OUTCOME.ILLEGAL_STATE",
                "host-invariant",
                Some("HOST.INVARIANT_VIOLATED"),
                None,
            ),
            // Law X3d r6 item 9 (unit X3d-1), as S12 spells them.
            (
                Row::LedgerCorrupt,
                "operational-failed",
                4,
                "LEDGER.CORRUPT",
                "ledger-corrupt",
                None,
                None,
            ),
            (
                Row::MigrationCorrupt,
                "operational-failed",
                4,
                "LEDGER.CORRUPT",
                "ledger-corrupt",
                Some("MIGRATION.CORRUPT"),
                None,
            ),
            (
                Row::CommitUndetermined,
                "operational-failed",
                4,
                "DURABILITY.COMMIT_FAILED",
                "durability-commit",
                None,
                None,
            ),
            (
                Row::ProjectRootCustody {
                    subject: "identity-contradiction",
                },
                "request-rejected",
                2,
                "CONFIG.INVALID",
                "none",
                Some("PROJECT.ROOT_CUSTODY_REFUSED"),
                Some("identity-contradiction"),
            ),
            (
                Row::ProjectExplicitPath,
                "request-rejected",
                2,
                "CONFIG.INVALID",
                "none",
                Some("PROJECT.EXPLICIT_PATH_INVALID"),
                None,
            ),
            (
                Row::ProjectScopeLimit {
                    subject: "workspaceRoots:1025>1024".into(),
                },
                "request-rejected",
                2,
                "REQUEST.UNSATISFIABLE",
                "none",
                Some("PROJECT.SCOPE_LIMIT"),
                Some("workspaceRoots:1025>1024"),
            ),
        ]
    }

    #[test]
    fn every_row_projects_to_its_published_route() {
        for (row, class, exit, code, fault, detail, subject) in table() {
            let t = installation_termination(&row);
            assert_eq!(t.class.to_string(), class, "{row:?}");
            assert_eq!(t.exit, exit, "{row:?}");
            assert_eq!(t.error_code.to_string(), code, "{row:?}");
            assert_eq!(t.fault_cause.to_string(), fault, "{row:?}");
            assert_eq!(
                t.detail.map(|d| d.to_string()).as_deref(),
                detail,
                "{row:?}"
            );
            assert_eq!(t.subject.as_deref(), subject, "{row:?}");
        }
    }

    #[test]
    fn classes_pair_exits_and_fault_causes_as_d9_does() {
        for (row, ..) in table() {
            let t = installation_termination(&row);
            match t.class {
                Class::RequestRejected => {
                    assert_eq!((t.exit, t.fault_cause), (2, Fault::None), "{row:?}")
                }
                Class::OperationalFailed => {
                    assert_eq!(t.exit, 4, "{row:?}");
                    let paired = match t.error_code {
                        Code::HostIoFailure => Fault::HostIo,
                        Code::LedgerBusyTimeout => Fault::LedgerBusy,
                        Code::SystemOutcomeIllegalState => Fault::HostInvariant,
                        Code::LedgerCorrupt => Fault::LedgerCorrupt,
                        Code::DurabilityCommitFailed => Fault::DurabilityCommit,
                        other => panic!("{other:?}"),
                    };
                    assert_eq!(t.fault_cause, paired, "{row:?}");
                }
                other => panic!("{other:?}"),
            }
        }
    }

    #[test]
    fn the_three_468a_details_are_used_and_admitted_by_common4() {
        let mut used = std::collections::BTreeSet::new();
        for (row, ..) in table() {
            if let Some(detail) = installation_termination(&row).detail {
                used.insert(detail.to_string());
            }
        }
        for code in [
            "CORE.NO_EMBEDDED_RELEASE",
            "INSTALLATION.ACCOUNT_REFUSED",
            "WORK.BUDGET_EXHAUSTED",
        ] {
            assert!(used.contains(code), "{code}");
            assert!(code.parse::<Detail>().is_ok(), "{code}");
        }
    }

    /// Law X4 r7 item 8: each chain detail projects to its own registered
    /// code, and only the schema-major one leaves the admission class.
    #[test]
    fn every_root_chain_detail_projects_to_its_registered_code() {
        for detail in [
            RootDetail::ChainGap,
            RootDetail::ChainBackdated,
            RootDetail::ChainOldThreshold,
            RootDetail::ChainNewThreshold,
            RootDetail::FinalExpired,
            RootDetail::FinalFuture,
            RootDetail::ExpiredNoChain,
            RootDetail::StateInconsistent,
            RootDetail::SchemaUnsupported,
        ] {
            assert_eq!(RootDetail::parse(detail.code()), Some(detail));
            let t = installation_termination(&Row::TrustRoot {
                detail,
                subject: "final".into(),
            });
            assert_eq!(
                t.detail.map(|d| d.to_string()).as_deref(),
                Some(detail.code())
            );
            assert_eq!(
                t.error_code,
                if detail == RootDetail::SchemaUnsupported {
                    Code::RequestSchemaMajorUnsupported
                } else {
                    Code::ExtensionAdmissionRejected
                }
            );
            assert_eq!((t.class, t.exit), (Class::RequestRejected, 2));
        }
        assert_eq!(RootDetail::parse("ROOT.SHAPE"), None);
    }
    #[test]
    fn role_specific_continuation_details_preserve_the_d9_route() {
        for (row, detail, subject) in [
            (
                Row::TrustIndexContinuation {
                    subject: "index:revoked".into(),
                },
                "CONTINUE-INDEX-NOT-TRUSTED",
                "index:revoked",
            ),
            (
                Row::TrustComponentContinuation {
                    subject: "component:unbootstrapped".into(),
                },
                "CONTINUE-COMPONENT-NOT-TRUSTED",
                "component:unbootstrapped",
            ),
        ] {
            let t = installation_termination(&row);
            assert_eq!(t.class, Class::RequestRejected);
            assert_eq!(t.exit, 2);
            assert_eq!(t.error_code, Code::ExtensionAdmissionRejected);
            assert_eq!(t.fault_cause, Fault::None);
            assert_eq!(t.detail.unwrap().to_string(), detail);
            assert_eq!(t.subject.as_deref(), Some(subject));
        }
    }
}
