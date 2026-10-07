// Law 468 r5 item 6: the public rows every creator and existing-root
// admission refusal ends in. One variant per row of the item 6 table, plus
// `Invariant` for the refusals that only a broken caller can reach; law X4
// r7 item 8 (unit X4a) adds the fenced trust admission's rows (law X4T r9
// item 10) and the live guards' two rows, all on existing details. Law X3d
// r6 item 9 (unit X3d-1) adds the commit facade's rows that 468c lacked: the
// journal and ledger quarantine rows, the durability row, and the project
// owners' own rows a stale guard keeps (X4 r7 item 8), each on an existing
// detail with the class S12 fixes for it. This is
// a closed vocabulary, not a termination: the host projects each row onto
// its D9 class, exit, error code, domain detail and fault cause. Workspace
// diagnostics never become authority.

/// COMMON4 D9Signal's closed signal vocabulary, carried without wire authority.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum D9Signal {
    Sigint,
    Sigterm,
    Sighup,
}
impl D9Signal {
    pub fn as_str(self) -> &'static str {
        match self {
            Self::Sigint => "SIGINT",
            Self::Sigterm => "SIGTERM",
            Self::Sighup => "SIGHUP",
        }
    }
}
/// The `NT-TCB-*` detail a platform decision refused with (item 6, the
/// platform-decision row).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TcbDetail {
    Boot,
    Identity,
    ProfileUnqualified,
}

/// The S5 `ROOT.*` detail a root chain refusal names (law X4T r9 item 10).
/// Only the chain evaluation produces these.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum RootDetail {
    ChainGap,
    ChainBackdated,
    ChainOldThreshold,
    ChainNewThreshold,
    FinalExpired,
    FinalFuture,
    ExpiredNoChain,
    StateInconsistent,
    SchemaUnsupported,
}
impl RootDetail {
    /// The registered spelling.
    pub fn code(self) -> &'static str {
        match self {
            Self::ChainGap => "ROOT.CHAIN_GAP",
            Self::ChainBackdated => "ROOT.CHAIN_BACKDATED",
            Self::ChainOldThreshold => "ROOT.CHAIN_OLD_THRESHOLD",
            Self::ChainNewThreshold => "ROOT.CHAIN_NEW_THRESHOLD",
            Self::FinalExpired => "ROOT.FINAL_EXPIRED",
            Self::FinalFuture => "ROOT.FINAL_FUTURE",
            Self::ExpiredNoChain => "ROOT.EXPIRED_NO_CHAIN",
            Self::StateInconsistent => "ROOT.STATE_INCONSISTENT",
            Self::SchemaUnsupported => "ROOT.SCHEMA_UNSUPPORTED",
        }
    }
    /// The detail for a registered spelling, if it is one of these.
    pub fn parse(code: &str) -> Option<Self> {
        [
            Self::ChainGap,
            Self::ChainBackdated,
            Self::ChainOldThreshold,
            Self::ChainNewThreshold,
            Self::FinalExpired,
            Self::FinalFuture,
            Self::ExpiredNoChain,
            Self::StateInconsistent,
            Self::SchemaUnsupported,
        ]
        .into_iter()
        .find(|detail| detail.code() == code)
    }
}

/// One row of law 468 item 6. `subject` strings are fixed workspace
/// spellings or the platform decision's own refusal suffix.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum InstallationTermination {
    /// X3d r9 S10.5: operator stop, D9 interrupted/130 without error details.
    Interrupted { signal: D9Signal },
    /// InitialCore F0: this build embeds no release.
    NoEmbeddedRelease,
    /// Unequal UIDs, home spelling or bounds, or the account changed.
    AccountRefused,
    /// The first creator's storage needs the invocation's backup choice.
    BackupChoiceRequired,
    /// The command needs the installation and I is absent.
    NotInitialized,
    /// Any other core refusal, with the refusal as subject.
    CoreRefused { subject: &'static str },
    /// The platform decision refused with its own `NT-TCB-*` detail.
    PlatformDecision { detail: TcbDetail, subject: String },
    /// Platform mismatch, translated process, loader filesystem, or a
    /// platform that cannot be observed or profiled (subject `platform`).
    PlatformUnqualified,
    /// H, or a fixed ancestor, is not a qualified install filesystem.
    InstallRootFilesystem,
    /// A custody refusal, with the sub-detail as subject.
    Custody { subject: &'static str },
    /// I is present but incomplete or contradictory (item 5).
    Incomplete,
    /// Law X3a item 5: the selected store's K is not a state schema the
    /// selected core supports (the existing `STATE.SCHEMA_UNSUPPORTED`).
    StateSchemaUnsupported,
    /// The installation fence is held by another invocation.
    Busy,
    /// A rename, barrier, filesystem, read or disclosure I/O failure, or any
    /// failure after the rename.
    HostIo,
    /// The attempt's or the admission's ledger refused a charge.
    BudgetExhausted,
    /// Law X4T r9 item 10: F absent, no accepted bootstrap (S4 step 2),
    /// `TRUST.NO_ADMITTED_TIME_CONTEXT`.
    TrustNoAdmittedTimeContext,
    /// Law X4T r9 item 10: the continuation row, `CONTINUE-CORE-NOT-TRUSTED`,
    /// with a subject naming the role and its state or the revoked component.
    TrustContinuation { subject: String },
    /// X4T-c: registered index-role continuation detail; class and subject unchanged.
    TrustIndexContinuation { subject: String },
    /// X4T-c: registered component-role continuation detail; class and subject unchanged.
    TrustComponentContinuation { subject: String },
    /// Law X4T r9 item 10: a root chain refusal, its S5 detail naming the link.
    TrustRoot { detail: RootDetail, subject: String },
    /// Law X4T r9 item 10: a signature, quorum or future-payload refusal,
    /// `PAYLOAD-NOT-ADMISSIBLE`.
    TrustPayloadNotAdmissible { subject: &'static str },
    /// Law X4T r9 item 10: plausibility or continuity,
    /// `CLOCK-EXCURSION-FORWARD` (`in-session` or `beyond-horizon`).
    ClockExcursionForward { subject: &'static str },
    /// Law X4 r7 item 8: a revoking observation during an operation,
    /// `TRUST.COMPONENT_REVOKED_DURING_OPERATION`, subject `trust-revoked`
    /// or `policy`.
    RevokedDuringOperation { subject: &'static str },
    /// Law X4 r7 item 8: an observer or monitor fail-stop,
    /// `OBSERVER.FAIL_STOP`, subject the stop reason.
    ObserverFailStop { subject: &'static str },
    /// Law X3d r6 item 9: a journal or ledger quarantine, `LEDGER.CORRUPT`,
    /// `ledger-corrupt`, with `domainDetail` omitted (S12; X3b r6 item 8).
    LedgerCorrupt,
    /// Law X3d r6 item 9: a carrierFormat 3 footprint that is not a lawful
    /// durable prefix at a writer open, `LEDGER.CORRUPT` with the detail
    /// `MIGRATION.CORRUPT` (S12).
    MigrationCorrupt,
    /// Law X3d r6 item 9: a durability-undetermined `COMMIT` or barrier,
    /// `DURABILITY.COMMIT_FAILED`, `durability-commit`. The ExecutionId the
    /// outcome retains is not part of the row.
    CommitUndetermined,
    /// Law X2 item 8's row a stale project owner keeps (X4 r7 item 8):
    /// `PROJECT.ROOT_CUSTODY_REFUSED`, with its subject.
    ProjectRootCustody { subject: &'static str },
    /// Law X2 item 8's `PROJECT.EXPLICIT_PATH_INVALID` (S3).
    ProjectExplicitPath,
    /// Law X2 item 8's `PROJECT.SCOPE_LIMIT`, with its `field:count>limit`
    /// subject (S12).
    ProjectScopeLimit { subject: String },
    /// A refusal only a broken caller reaches: a latched or foreign attempt
    /// or gate, a second allocation in one process, or a receipt that is not
    /// for its own handle. Not a row of item 6.
    Invariant,
}
