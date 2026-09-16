// Generated trial: named28 profile, typify0.8.0; inert carriers only.
#![allow(unused_imports)]
use super::evidence::*;
use super::identity::*;
use super::output::*;
use super::protocol::*;
use super::evidence::error;
///Optional regular-file Blob at path .opensip/detector-compatibility.json on an already admitted same closure2 tree. Identity hashes closure.manifestDigest as the DR-103 component-manifest body (platforms/tree/role), never this three-field listing. Select the unique reserved path from closure.tree; compare exact retained blob SHA-256 and byte length. Path absent is no declaration. Empty compatibleClosures is a complete listing. A present malformed, unrecognized, wrong-digest, or missing listing refuses; it is never silently no declaration. This schema is not a signature envelope and this projector does not verify signatures. Current-trust receipt requires host.closures[closureId].trust=admitted and trustOrigin in retained-generation | installed-signed-release | signed-closure-bundle. Caller compatibleWith maps are never this listing.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Detector1Root {
    #[serde(rename = "compatibleClosures")]
    pub compatible_closures: ::std::vec::Vec<Detector1RootCompatibleClosuresItem>,
    #[serde(rename = "schemaFamily")]
    pub schema_family: ::serde_json::Value,
    #[serde(rename = "schemaMajor")]
    pub schema_major: ExactInteger,
}
///`Detector1RootCompatibleClosuresItem`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Detector1RootCompatibleClosuresItem {
    #[serde(rename = "closureId")]
    pub closure_id: Common3ClosureId,
    #[serde(rename = "semanticsMajor")]
    pub semantics_major: u16,
}
impl ::std::convert::From<Imported1TestPayloadV1> for TestExecution1TestPayloadV1 {
    fn from(value: Imported1TestPayloadV1) -> Self {
        value.0
    }
}
///`Inventory3AnalysisProfile`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Inventory3AnalysisProfile {
    #[serde(rename = "default")]
    Default,
    #[serde(rename = "fit")]
    Fit,
    #[serde(rename = "audit")]
    Audit,
    #[serde(rename = "verify")]
    Verify,
    #[serde(rename = "pivot")]
    Pivot,
    #[serde(rename = "policy-test-fixture")]
    PolicyTestFixture,
}
impl ::std::fmt::Display for Inventory3AnalysisProfile {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Default => f.write_str("default"),
            Self::Fit => f.write_str("fit"),
            Self::Audit => f.write_str("audit"),
            Self::Verify => f.write_str("verify"),
            Self::Pivot => f.write_str("pivot"),
            Self::PolicyTestFixture => f.write_str("policy-test-fixture"),
        }
    }
}
impl ::std::str::FromStr for Inventory3AnalysisProfile {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "default" => Ok(Self::Default),
            "fit" => Ok(Self::Fit),
            "audit" => Ok(Self::Audit),
            "verify" => Ok(Self::Verify),
            "pivot" => Ok(Self::Pivot),
            "policy-test-fixture" => Ok(Self::PolicyTestFixture),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Inventory3AnalysisProfile {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Inventory3AnalysisProfile {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Inventory3Command`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Inventory3Command {
    ///true: every output is Map-side and can never be a Control verdict or repair authorization
    pub advisory: bool,
    pub authority: Inventory3CommandAuthority,
    ///what authorizes the command's effect (distinct from advisory, which describes its OUTPUT standing). none: read-only or ordinary durable write under the project writer. user-consent: interactive confirmation or --yes-policy. policy-record-or-consent: CI needs a pre-existing policy record. security-grant: an admitted RepoExecutionGrantV2. recovery-authority-quorum: an epoch signed by recoveryAuthority keys at its threshold (S4.5); ordinary root keys do not count. exclusive-lease: EXCLUSIVE lease (S7) plus explicit invocation. core-transition-leases: installation fence plus the S7 affected namespace EXCLUSIVE set, derived from the admitted intent and installation registry; same-schema core update/repair require the fence alone.
    #[serde(rename = "authorizationClass")]
    pub authorization_class: Inventory3CommandAuthorizationClass,
    pub cli: Inventory3CommandCli,
    ///true when the command may perform the first source-derived write into the private store; such a command must carry the --allow-backup-custody join (identity §5 / TM V17)
    #[serde(
        rename = "firstSourceWrite",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub first_source_write: FieldPresence<::std::option::Option<bool>>,
    pub flags: ::std::vec::Vec<Inventory3CommandFlag>,
    pub formats: ::std::vec::Vec<Inventory3OutputFormat>,
    ///Candidate declared syntax; does not establish independent acceptance of the complete surface.
    #[serde(rename = "grammarStanding")]
    pub grammar_standing: ::serde_json::Value,
    pub name: Inventory3CommandName,
    ///the contract that owns the command's semantics; the workflow inventory only enumerates and joins
    pub owner: Inventory3CommandOwner,
    ///fields whose value must be semantically identical across every applicable renderer of this command
    #[serde(rename = "parityFields")]
    pub parity_fields: ::std::vec::Vec<Common3CanonicalIdentifier>,
    #[serde(
        rename = "queryDispatch",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub query_dispatch: FieldPresence<::std::option::Option<Inventory3QueryDispatch>>,
    #[serde(rename = "repositoryExecution")]
    pub repository_execution: Inventory3CommandRepositoryExecution,
    #[serde(rename = "requestClass")]
    pub request_class: Inventory3RequestClass,
    pub steps: ::std::vec::Vec<Invocation3StepKind>,
    ///true only for explicit policy-init/waive/baseline-adopt/baseline-export/baseline-upgrade; no other command writes a tracked file
    #[serde(rename = "writesTrackedIntent")]
    pub writes_tracked_intent: bool,
}
///`Inventory3CommandAuthority`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Inventory3CommandAuthority {
    #[serde(rename = "authoritative-default")]
    AuthoritativeDefault,
    #[serde(rename = "ephemeral-only")]
    EphemeralOnly,
    #[serde(rename = "ephemeral-optional")]
    EphemeralOptional,
    #[serde(rename = "none")]
    None,
}
impl ::std::fmt::Display for Inventory3CommandAuthority {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::AuthoritativeDefault => f.write_str("authoritative-default"),
            Self::EphemeralOnly => f.write_str("ephemeral-only"),
            Self::EphemeralOptional => f.write_str("ephemeral-optional"),
            Self::None => f.write_str("none"),
        }
    }
}
impl ::std::str::FromStr for Inventory3CommandAuthority {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "authoritative-default" => Ok(Self::AuthoritativeDefault),
            "ephemeral-only" => Ok(Self::EphemeralOnly),
            "ephemeral-optional" => Ok(Self::EphemeralOptional),
            "none" => Ok(Self::None),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Inventory3CommandAuthority {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Inventory3CommandAuthority {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///what authorizes the command's effect (distinct from advisory, which describes its OUTPUT standing). none: read-only or ordinary durable write under the project writer. user-consent: interactive confirmation or --yes-policy. policy-record-or-consent: CI needs a pre-existing policy record. security-grant: an admitted RepoExecutionGrantV2. recovery-authority-quorum: an epoch signed by recoveryAuthority keys at its threshold (S4.5); ordinary root keys do not count. exclusive-lease: EXCLUSIVE lease (S7) plus explicit invocation. core-transition-leases: installation fence plus the S7 affected namespace EXCLUSIVE set, derived from the admitted intent and installation registry; same-schema core update/repair require the fence alone.
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Inventory3CommandAuthorizationClass {
    #[serde(rename = "none")]
    None,
    #[serde(rename = "user-consent")]
    UserConsent,
    #[serde(rename = "policy-record-or-consent")]
    PolicyRecordOrConsent,
    #[serde(rename = "security-grant")]
    SecurityGrant,
    #[serde(rename = "recovery-authority-quorum")]
    RecoveryAuthorityQuorum,
    #[serde(rename = "exclusive-lease")]
    ExclusiveLease,
    #[serde(rename = "core-transition-leases")]
    CoreTransitionLeases,
}
impl ::std::fmt::Display for Inventory3CommandAuthorizationClass {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::None => f.write_str("none"),
            Self::UserConsent => f.write_str("user-consent"),
            Self::PolicyRecordOrConsent => f.write_str("policy-record-or-consent"),
            Self::SecurityGrant => f.write_str("security-grant"),
            Self::RecoveryAuthorityQuorum => f.write_str("recovery-authority-quorum"),
            Self::ExclusiveLease => f.write_str("exclusive-lease"),
            Self::CoreTransitionLeases => f.write_str("core-transition-leases"),
        }
    }
}
impl ::std::str::FromStr for Inventory3CommandAuthorizationClass {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "none" => Ok(Self::None),
            "user-consent" => Ok(Self::UserConsent),
            "policy-record-or-consent" => Ok(Self::PolicyRecordOrConsent),
            "security-grant" => Ok(Self::SecurityGrant),
            "recovery-authority-quorum" => Ok(Self::RecoveryAuthorityQuorum),
            "exclusive-lease" => Ok(Self::ExclusiveLease),
            "core-transition-leases" => Ok(Self::CoreTransitionLeases),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Inventory3CommandAuthorizationClass {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Inventory3CommandAuthorizationClass {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Inventory3CommandCli`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Inventory3CommandCli(::std::string::String);
impl ::std::ops::Deref for Inventory3CommandCli {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Inventory3CommandCli> for ::std::string::String {
    fn from(value: Inventory3CommandCli) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Inventory3CommandCli {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 256usize {
            return Err("longer than 256 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Inventory3CommandCli {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Inventory3CommandCli {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Inventory3CommandCli {
    fn deserialize<D>(deserializer: D) -> ::std::result::Result<Self, D::Error>
    where
        D: ::serde::Deserializer<'de>,
    {
        ::std::string::String::deserialize(deserializer)?
            .parse()
            .map_err(|e: self::error::ConversionError| {
                <D::Error as ::serde::de::Error>::custom(e.to_string())
            })
    }
}
///A cross-owner flag join. authorization flags grant or acknowledge an effect; advisory flags only shape output.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Inventory3CommandFlag {
    pub class: Inventory3CommandFlagClass,
    pub flag: Inventory3CommandFlagFlag,
    pub join: Common3BoundedText,
    pub owner: Inventory3CommandFlagOwner,
}
///`Inventory3CommandFlagClass`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Inventory3CommandFlagClass {
    #[serde(rename = "authorization")]
    Authorization,
    #[serde(rename = "advisory")]
    Advisory,
    #[serde(rename = "selection")]
    Selection,
}
impl ::std::fmt::Display for Inventory3CommandFlagClass {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Authorization => f.write_str("authorization"),
            Self::Advisory => f.write_str("advisory"),
            Self::Selection => f.write_str("selection"),
        }
    }
}
impl ::std::str::FromStr for Inventory3CommandFlagClass {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "authorization" => Ok(Self::Authorization),
            "advisory" => Ok(Self::Advisory),
            "selection" => Ok(Self::Selection),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Inventory3CommandFlagClass {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Inventory3CommandFlagClass {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Inventory3CommandFlagFlag`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Inventory3CommandFlagFlag(::std::string::String);
impl ::std::ops::Deref for Inventory3CommandFlagFlag {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Inventory3CommandFlagFlag> for ::std::string::String {
    fn from(value: Inventory3CommandFlagFlag) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Inventory3CommandFlagFlag {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 64usize {
            return Err("longer than 64 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Inventory3CommandFlagFlag {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Inventory3CommandFlagFlag {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Inventory3CommandFlagFlag {
    fn deserialize<D>(deserializer: D) -> ::std::result::Result<Self, D::Error>
    where
        D: ::serde::Deserializer<'de>,
    {
        ::std::string::String::deserialize(deserializer)?
            .parse()
            .map_err(|e: self::error::ConversionError| {
                <D::Error as ::serde::de::Error>::custom(e.to_string())
            })
    }
}
///`Inventory3CommandFlagOwner`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Inventory3CommandFlagOwner {
    #[serde(rename = "workflow")]
    Workflow,
    #[serde(rename = "security")]
    Security,
    #[serde(rename = "identity")]
    Identity,
    #[serde(rename = "native")]
    Native,
    #[serde(rename = "foundation")]
    Foundation,
}
impl ::std::fmt::Display for Inventory3CommandFlagOwner {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Workflow => f.write_str("workflow"),
            Self::Security => f.write_str("security"),
            Self::Identity => f.write_str("identity"),
            Self::Native => f.write_str("native"),
            Self::Foundation => f.write_str("foundation"),
        }
    }
}
impl ::std::str::FromStr for Inventory3CommandFlagOwner {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "workflow" => Ok(Self::Workflow),
            "security" => Ok(Self::Security),
            "identity" => Ok(Self::Identity),
            "native" => Ok(Self::Native),
            "foundation" => Ok(Self::Foundation),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Inventory3CommandFlagOwner {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Inventory3CommandFlagOwner {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Inventory3CommandName`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Inventory3CommandName {
    #[serde(rename = "default")]
    Default,
    #[serde(rename = "recommend")]
    Recommend,
    #[serde(rename = "analyze")]
    Analyze,
    #[serde(rename = "fit")]
    Fit,
    #[serde(rename = "audit")]
    Audit,
    #[serde(rename = "query")]
    Query,
    #[serde(rename = "import")]
    Import,
    #[serde(rename = "baseline-adopt")]
    BaselineAdopt,
    #[serde(rename = "baseline-export")]
    BaselineExport,
    #[serde(rename = "baseline-show")]
    BaselineShow,
    #[serde(rename = "baseline-upgrade")]
    BaselineUpgrade,
    #[serde(rename = "policy-show")]
    PolicyShow,
    #[serde(rename = "policy-init")]
    PolicyInit,
    #[serde(rename = "policy-test")]
    PolicyTest,
    #[serde(rename = "waive")]
    Waive,
    #[serde(rename = "candidates")]
    Candidates,
    #[serde(rename = "inspect")]
    Inspect,
    #[serde(rename = "review-brief")]
    ReviewBrief,
    #[serde(rename = "review-join")]
    ReviewJoin,
    #[serde(rename = "repair-preview")]
    RepairPreview,
    #[serde(rename = "repair-apply")]
    RepairApply,
    #[serde(rename = "repair-verify")]
    RepairVerify,
    #[serde(rename = "repair-recover")]
    RepairRecover,
    #[serde(rename = "test-run")]
    TestRun,
    #[serde(rename = "install")]
    Install,
    #[serde(rename = "update")]
    Update,
    #[serde(rename = "doctor")]
    Doctor,
    #[serde(rename = "purge")]
    Purge,
    #[serde(rename = "agent-serve")]
    AgentServe,
    #[serde(rename = "help")]
    Help,
    #[serde(rename = "version")]
    Version,
    #[serde(rename = "completion")]
    Completion,
    #[serde(rename = "trust-recovery-challenge")]
    TrustRecoveryChallenge,
    #[serde(rename = "trust-recovery-import")]
    TrustRecoveryImport,
    #[serde(rename = "trust-refresh")]
    TrustRefresh,
    #[serde(rename = "trust-import")]
    TrustImport,
    #[serde(rename = "trust-doctor")]
    TrustDoctor,
    #[serde(rename = "store-migrate")]
    StoreMigrate,
    #[serde(rename = "store-rollback")]
    StoreRollback,
    #[serde(rename = "store-gc")]
    StoreGc,
    #[serde(rename = "store-status")]
    StoreStatus,
    #[serde(rename = "native-prepare")]
    NativePrepare,
    #[serde(rename = "core-update")]
    CoreUpdate,
    #[serde(rename = "core-repair")]
    CoreRepair,
    #[serde(rename = "core-rollback")]
    CoreRollback,
}
impl ::std::fmt::Display for Inventory3CommandName {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Default => f.write_str("default"),
            Self::Recommend => f.write_str("recommend"),
            Self::Analyze => f.write_str("analyze"),
            Self::Fit => f.write_str("fit"),
            Self::Audit => f.write_str("audit"),
            Self::Query => f.write_str("query"),
            Self::Import => f.write_str("import"),
            Self::BaselineAdopt => f.write_str("baseline-adopt"),
            Self::BaselineExport => f.write_str("baseline-export"),
            Self::BaselineShow => f.write_str("baseline-show"),
            Self::BaselineUpgrade => f.write_str("baseline-upgrade"),
            Self::PolicyShow => f.write_str("policy-show"),
            Self::PolicyInit => f.write_str("policy-init"),
            Self::PolicyTest => f.write_str("policy-test"),
            Self::Waive => f.write_str("waive"),
            Self::Candidates => f.write_str("candidates"),
            Self::Inspect => f.write_str("inspect"),
            Self::ReviewBrief => f.write_str("review-brief"),
            Self::ReviewJoin => f.write_str("review-join"),
            Self::RepairPreview => f.write_str("repair-preview"),
            Self::RepairApply => f.write_str("repair-apply"),
            Self::RepairVerify => f.write_str("repair-verify"),
            Self::RepairRecover => f.write_str("repair-recover"),
            Self::TestRun => f.write_str("test-run"),
            Self::Install => f.write_str("install"),
            Self::Update => f.write_str("update"),
            Self::Doctor => f.write_str("doctor"),
            Self::Purge => f.write_str("purge"),
            Self::AgentServe => f.write_str("agent-serve"),
            Self::Help => f.write_str("help"),
            Self::Version => f.write_str("version"),
            Self::Completion => f.write_str("completion"),
            Self::TrustRecoveryChallenge => f.write_str("trust-recovery-challenge"),
            Self::TrustRecoveryImport => f.write_str("trust-recovery-import"),
            Self::TrustRefresh => f.write_str("trust-refresh"),
            Self::TrustImport => f.write_str("trust-import"),
            Self::TrustDoctor => f.write_str("trust-doctor"),
            Self::StoreMigrate => f.write_str("store-migrate"),
            Self::StoreRollback => f.write_str("store-rollback"),
            Self::StoreGc => f.write_str("store-gc"),
            Self::StoreStatus => f.write_str("store-status"),
            Self::NativePrepare => f.write_str("native-prepare"),
            Self::CoreUpdate => f.write_str("core-update"),
            Self::CoreRepair => f.write_str("core-repair"),
            Self::CoreRollback => f.write_str("core-rollback"),
        }
    }
}
impl ::std::str::FromStr for Inventory3CommandName {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "default" => Ok(Self::Default),
            "recommend" => Ok(Self::Recommend),
            "analyze" => Ok(Self::Analyze),
            "fit" => Ok(Self::Fit),
            "audit" => Ok(Self::Audit),
            "query" => Ok(Self::Query),
            "import" => Ok(Self::Import),
            "baseline-adopt" => Ok(Self::BaselineAdopt),
            "baseline-export" => Ok(Self::BaselineExport),
            "baseline-show" => Ok(Self::BaselineShow),
            "baseline-upgrade" => Ok(Self::BaselineUpgrade),
            "policy-show" => Ok(Self::PolicyShow),
            "policy-init" => Ok(Self::PolicyInit),
            "policy-test" => Ok(Self::PolicyTest),
            "waive" => Ok(Self::Waive),
            "candidates" => Ok(Self::Candidates),
            "inspect" => Ok(Self::Inspect),
            "review-brief" => Ok(Self::ReviewBrief),
            "review-join" => Ok(Self::ReviewJoin),
            "repair-preview" => Ok(Self::RepairPreview),
            "repair-apply" => Ok(Self::RepairApply),
            "repair-verify" => Ok(Self::RepairVerify),
            "repair-recover" => Ok(Self::RepairRecover),
            "test-run" => Ok(Self::TestRun),
            "install" => Ok(Self::Install),
            "update" => Ok(Self::Update),
            "doctor" => Ok(Self::Doctor),
            "purge" => Ok(Self::Purge),
            "agent-serve" => Ok(Self::AgentServe),
            "help" => Ok(Self::Help),
            "version" => Ok(Self::Version),
            "completion" => Ok(Self::Completion),
            "trust-recovery-challenge" => Ok(Self::TrustRecoveryChallenge),
            "trust-recovery-import" => Ok(Self::TrustRecoveryImport),
            "trust-refresh" => Ok(Self::TrustRefresh),
            "trust-import" => Ok(Self::TrustImport),
            "trust-doctor" => Ok(Self::TrustDoctor),
            "store-migrate" => Ok(Self::StoreMigrate),
            "store-rollback" => Ok(Self::StoreRollback),
            "store-gc" => Ok(Self::StoreGc),
            "store-status" => Ok(Self::StoreStatus),
            "native-prepare" => Ok(Self::NativePrepare),
            "core-update" => Ok(Self::CoreUpdate),
            "core-repair" => Ok(Self::CoreRepair),
            "core-rollback" => Ok(Self::CoreRollback),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Inventory3CommandName {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Inventory3CommandName {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///the contract that owns the command's semantics; the workflow inventory only enumerates and joins
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Inventory3CommandOwner {
    #[serde(rename = "workflow")]
    Workflow,
    #[serde(rename = "security")]
    Security,
    #[serde(rename = "identity")]
    Identity,
    #[serde(rename = "native")]
    Native,
}
impl ::std::fmt::Display for Inventory3CommandOwner {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Workflow => f.write_str("workflow"),
            Self::Security => f.write_str("security"),
            Self::Identity => f.write_str("identity"),
            Self::Native => f.write_str("native"),
        }
    }
}
impl ::std::str::FromStr for Inventory3CommandOwner {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "workflow" => Ok(Self::Workflow),
            "security" => Ok(Self::Security),
            "identity" => Ok(Self::Identity),
            "native" => Ok(Self::Native),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Inventory3CommandOwner {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Inventory3CommandOwner {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Inventory3CommandRepositoryExecution`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Inventory3CommandRepositoryExecution {
    #[serde(rename = "never")]
    Never,
    #[serde(rename = "explicit-authorized")]
    ExplicitAuthorized,
}
impl ::std::fmt::Display for Inventory3CommandRepositoryExecution {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Never => f.write_str("never"),
            Self::ExplicitAuthorized => f.write_str("explicit-authorized"),
        }
    }
}
impl ::std::str::FromStr for Inventory3CommandRepositoryExecution {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "never" => Ok(Self::Never),
            "explicit-authorized" => Ok(Self::ExplicitAuthorized),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Inventory3CommandRepositoryExecution {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Inventory3CommandRepositoryExecution {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///A failure golden (request-rejected or operational-failed) carries its actual domainDetail, unless detailSuppliedBy names the composition that supplies the failure envelope errors.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Inventory3Golden {
    pub class: Common3D9Class,
    pub command: Inventory3CommandName,
    ///workflows-and-surfaces §8: the native §10 route composition supplies errors from the route detail. Absent when domainDetail is present.
    #[serde(
        rename = "detailSuppliedBy",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub detail_supplied_by: FieldPresence<
        ::std::option::Option<Inventory3GoldenDetailSuppliedBy>,
    >,
    #[serde(
        rename = "domainDetail",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub domain_detail: FieldPresence<::std::option::Option<Common3DomainDetailCode>>,
    #[serde(
        rename = "errorCode",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub error_code: FieldPresence<::std::option::Option<Common3D9ErrorCode>>,
    #[serde(rename = "exitCode")]
    pub exit_code: ExactInteger,
    pub id: Common3CanonicalIdentifier,
    #[serde(
        rename = "reasonCode",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub reason_code: FieldPresence<::std::option::Option<Common3D9ReasonCode>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub remedy: FieldPresence<::std::option::Option<Common3BoundedText>>,
    pub situation: Common3BoundedText,
}
///workflows-and-surfaces §8: the native §10 route composition supplies errors from the route detail. Absent when domainDetail is present.
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Inventory3GoldenDetailSuppliedBy {
    #[serde(rename = "native-route-composition")]
    NativeRouteComposition,
}
impl ::std::fmt::Display for Inventory3GoldenDetailSuppliedBy {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::NativeRouteComposition => f.write_str("native-route-composition"),
        }
    }
}
impl ::std::str::FromStr for Inventory3GoldenDetailSuppliedBy {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "native-route-composition" => Ok(Self::NativeRouteComposition),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Inventory3GoldenDetailSuppliedBy {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Inventory3GoldenDetailSuppliedBy {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Inventory3OutputFormat`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Inventory3OutputFormat {
    #[serde(rename = "human")]
    Human,
    #[serde(rename = "json")]
    Json,
    #[serde(rename = "sarif")]
    Sarif,
    #[serde(rename = "html")]
    Html,
    #[serde(rename = "agent")]
    Agent,
}
impl ::std::fmt::Display for Inventory3OutputFormat {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Human => f.write_str("human"),
            Self::Json => f.write_str("json"),
            Self::Sarif => f.write_str("sarif"),
            Self::Html => f.write_str("html"),
            Self::Agent => f.write_str("agent"),
        }
    }
}
impl ::std::str::FromStr for Inventory3OutputFormat {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "human" => Ok(Self::Human),
            "json" => Ok(Self::Json),
            "sarif" => Ok(Self::Sarif),
            "html" => Ok(Self::Html),
            "agent" => Ok(Self::Agent),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Inventory3OutputFormat {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Inventory3OutputFormat {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Closed dispatch of a query-class command: the envelope surface it selects, the step that produces it, the query-step operations it may dispatch, and the exact JSON pointer into CommandEnvelope major 3 for every parity field.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Inventory3QueryDispatch {
    pub operations: ::std::vec::Vec<Inventory3QueryDispatchOperationsItem>,
    #[serde(rename = "parityPaths")]
    pub parity_paths: ::std::collections::BTreeMap<
        Common3CanonicalIdentifier,
        ::std::string::String,
    >,
    #[serde(rename = "stepKind")]
    pub step_kind: Inventory3QueryDispatchStepKind,
    pub surface: Envelope3PropertiesQuerySurface,
}
///`Inventory3QueryDispatchOperationsItem`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(untagged)]
pub enum Inventory3QueryDispatchOperationsItem {
    Graph3Operation(Graph3Operation),
    Invocation3HostQueryOperation(Invocation3HostQueryOperation),
}
impl ::std::fmt::Display for Inventory3QueryDispatchOperationsItem {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match self {
            Self::Graph3Operation(x) => x.fmt(f),
            Self::Invocation3HostQueryOperation(x) => x.fmt(f),
        }
    }
}
impl ::std::str::FromStr for Inventory3QueryDispatchOperationsItem {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if let Ok(v) = value.parse() {
            Ok(Self::Graph3Operation(v))
        } else if let Ok(v) = value.parse() {
            Ok(Self::Invocation3HostQueryOperation(v))
        } else {
            Err("string conversion failed for all variants".into())
        }
    }
}
impl ::std::convert::TryFrom<&str> for Inventory3QueryDispatchOperationsItem {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Inventory3QueryDispatchOperationsItem {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::From<Graph3Operation> for Inventory3QueryDispatchOperationsItem {
    fn from(value: Graph3Operation) -> Self {
        Self::Graph3Operation(value)
    }
}
impl ::std::convert::From<Invocation3HostQueryOperation>
for Inventory3QueryDispatchOperationsItem {
    fn from(value: Invocation3HostQueryOperation) -> Self {
        Self::Invocation3HostQueryOperation(value)
    }
}
///`Inventory3QueryDispatchStepKind`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Inventory3QueryDispatchStepKind {
    #[serde(rename = "query")]
    Query,
    #[serde(rename = "repair-preview")]
    RepairPreview,
}
impl ::std::fmt::Display for Inventory3QueryDispatchStepKind {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Query => f.write_str("query"),
            Self::RepairPreview => f.write_str("repair-preview"),
        }
    }
}
impl ::std::str::FromStr for Inventory3QueryDispatchStepKind {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "query" => Ok(Self::Query),
            "repair-preview" => Ok(Self::RepairPreview),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Inventory3QueryDispatchStepKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Inventory3QueryDispatchStepKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Inventory3Renderer`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Inventory3Renderer {
    pub applicability: ::std::vec::Vec<Inventory3RequestClass>,
    pub format: Inventory3OutputFormat,
    #[serde(rename = "parityRule")]
    pub parity_rule: Common3BoundedText,
    #[serde(rename = "requiredFailureClass")]
    pub required_failure_class: ::serde_json::Value,
    pub version: ::std::num::NonZeroU64,
}
///`Inventory3RequestClass`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Inventory3RequestClass {
    #[serde(rename = "analysis")]
    Analysis,
    #[serde(rename = "query")]
    Query,
    #[serde(rename = "mutation")]
    Mutation,
    #[serde(rename = "lifecycle")]
    Lifecycle,
    #[serde(rename = "execution")]
    Execution,
    #[serde(rename = "serve")]
    Serve,
    #[serde(rename = "meta")]
    Meta,
    #[serde(rename = "trust")]
    Trust,
}
impl ::std::fmt::Display for Inventory3RequestClass {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Analysis => f.write_str("analysis"),
            Self::Query => f.write_str("query"),
            Self::Mutation => f.write_str("mutation"),
            Self::Lifecycle => f.write_str("lifecycle"),
            Self::Execution => f.write_str("execution"),
            Self::Serve => f.write_str("serve"),
            Self::Meta => f.write_str("meta"),
            Self::Trust => f.write_str("trust"),
        }
    }
}
impl ::std::str::FromStr for Inventory3RequestClass {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "analysis" => Ok(Self::Analysis),
            "query" => Ok(Self::Query),
            "mutation" => Ok(Self::Mutation),
            "lifecycle" => Ok(Self::Lifecycle),
            "execution" => Ok(Self::Execution),
            "serve" => Ok(Self::Serve),
            "meta" => Ok(Self::Meta),
            "trust" => Ok(Self::Trust),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Inventory3RequestClass {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Inventory3RequestClass {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Isolated evaluator3 inventory schema. schemaMajor 3 because declared findings parity is FindingSurface (one result per finding3; partialFingerprints only when matched).
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Inventory3Root {
    pub commands: ::std::vec::Vec<Inventory3Command>,
    pub goldens: ::std::vec::Vec<Inventory3Golden>,
    pub renderers: [Inventory3Renderer; 5usize],
    #[serde(rename = "schemaFamily")]
    pub schema_family: ::serde_json::Value,
    #[serde(rename = "schemaMajor")]
    pub schema_major: ExactInteger,
    ///flags owned by other contracts that the host front end must accept on the listed commands; authorization flags never appear on advisory-only commands
    #[serde(
        rename = "sharedFlags",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub shared_flags: FieldPresence<
        ::std::option::Option<::std::vec::Vec<Inventory3CommandFlag>>,
    >,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub standing: FieldPresence<::std::option::Option<Inventory3RootStanding>>,
}
///`Inventory3RootStanding`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Inventory3RootStanding(::std::string::String);
impl ::std::ops::Deref for Inventory3RootStanding {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Inventory3RootStanding> for ::std::string::String {
    fn from(value: Inventory3RootStanding) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Inventory3RootStanding {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 2048usize {
            return Err("longer than 2048 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Inventory3RootStanding {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Inventory3RootStanding {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Inventory3RootStanding {
    fn deserialize<D>(deserializer: D) -> ::std::result::Result<Self, D::Error>
    where
        D: ::serde::Deserializer<'de>,
    {
        ::std::string::String::deserialize(deserializer)?
            .parse()
            .map_err(|e: self::error::ConversionError| {
                <D::Error as ::serde::de::Error>::custom(e.to_string())
            })
    }
}
///`Inventory4AnalysisProfile`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Inventory4AnalysisProfile {
    #[serde(rename = "default")]
    Default,
    #[serde(rename = "fit")]
    Fit,
    #[serde(rename = "audit")]
    Audit,
    #[serde(rename = "verify")]
    Verify,
    #[serde(rename = "pivot")]
    Pivot,
    #[serde(rename = "policy-test-fixture")]
    PolicyTestFixture,
}
impl ::std::fmt::Display for Inventory4AnalysisProfile {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Default => f.write_str("default"),
            Self::Fit => f.write_str("fit"),
            Self::Audit => f.write_str("audit"),
            Self::Verify => f.write_str("verify"),
            Self::Pivot => f.write_str("pivot"),
            Self::PolicyTestFixture => f.write_str("policy-test-fixture"),
        }
    }
}
impl ::std::str::FromStr for Inventory4AnalysisProfile {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "default" => Ok(Self::Default),
            "fit" => Ok(Self::Fit),
            "audit" => Ok(Self::Audit),
            "verify" => Ok(Self::Verify),
            "pivot" => Ok(Self::Pivot),
            "policy-test-fixture" => Ok(Self::PolicyTestFixture),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Inventory4AnalysisProfile {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Inventory4AnalysisProfile {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Inventory4Command`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Inventory4Command {
    ///true: every output is Map-side and can never be a Control verdict or repair authorization
    pub advisory: bool,
    pub authority: Inventory4CommandAuthority,
    ///what authorizes the command's effect (distinct from advisory, which describes its OUTPUT standing). none: read-only or ordinary durable write under the project writer. user-consent: interactive confirmation or --yes-policy. policy-record-or-consent: CI needs a pre-existing policy record. security-grant: an admitted RepoExecutionGrantV2. recovery-authority-quorum: an epoch signed by recoveryAuthority keys at its threshold (S4.5); ordinary root keys do not count. exclusive-lease: EXCLUSIVE lease (S7) plus explicit invocation. core-transition-leases: installation fence plus the S7 affected namespace EXCLUSIVE set, derived from the admitted intent and installation registry; same-schema core update/repair require the fence alone.
    #[serde(rename = "authorizationClass")]
    pub authorization_class: Inventory4CommandAuthorizationClass,
    pub cli: Inventory4CommandCli,
    ///true when the command may perform the first source-derived write into the private store; such a command must carry the --allow-backup-custody join (identity §5 / TM V17)
    #[serde(
        rename = "firstSourceWrite",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub first_source_write: FieldPresence<::std::option::Option<bool>>,
    pub flags: ::std::vec::Vec<Inventory4CommandFlag>,
    pub formats: ::std::vec::Vec<Inventory4OutputFormat>,
    ///Candidate declared syntax; does not establish independent acceptance of the complete surface.
    #[serde(rename = "grammarStanding")]
    pub grammar_standing: ::serde_json::Value,
    #[serde(
        rename = "metaDispatch",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub meta_dispatch: FieldPresence<
        ::std::option::Option<Inventory4CommandMetaDispatch>,
    >,
    pub name: Inventory4CommandName,
    ///the contract that owns the command's semantics; the workflow inventory only enumerates and joins
    pub owner: Inventory4CommandOwner,
    ///fields whose value must be semantically identical across every applicable renderer of this command
    #[serde(rename = "parityFields")]
    pub parity_fields: ::std::vec::Vec<Common3CanonicalIdentifier>,
    #[serde(
        rename = "queryDispatch",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub query_dispatch: FieldPresence<::std::option::Option<Inventory4QueryDispatch>>,
    #[serde(rename = "repositoryExecution")]
    pub repository_execution: Inventory4CommandRepositoryExecution,
    #[serde(rename = "requestClass")]
    pub request_class: Inventory4RequestClass,
    pub steps: ::std::vec::Vec<Invocation3StepKind>,
    ///true only for explicit policy-init/waive/baseline-adopt/baseline-export/baseline-upgrade; no other command writes a tracked file
    #[serde(rename = "writesTrackedIntent")]
    pub writes_tracked_intent: bool,
}
///`Inventory4CommandAuthority`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Inventory4CommandAuthority {
    #[serde(rename = "authoritative-default")]
    AuthoritativeDefault,
    #[serde(rename = "ephemeral-only")]
    EphemeralOnly,
    #[serde(rename = "ephemeral-optional")]
    EphemeralOptional,
    #[serde(rename = "none")]
    None,
}
impl ::std::fmt::Display for Inventory4CommandAuthority {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::AuthoritativeDefault => f.write_str("authoritative-default"),
            Self::EphemeralOnly => f.write_str("ephemeral-only"),
            Self::EphemeralOptional => f.write_str("ephemeral-optional"),
            Self::None => f.write_str("none"),
        }
    }
}
impl ::std::str::FromStr for Inventory4CommandAuthority {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "authoritative-default" => Ok(Self::AuthoritativeDefault),
            "ephemeral-only" => Ok(Self::EphemeralOnly),
            "ephemeral-optional" => Ok(Self::EphemeralOptional),
            "none" => Ok(Self::None),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Inventory4CommandAuthority {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Inventory4CommandAuthority {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///what authorizes the command's effect (distinct from advisory, which describes its OUTPUT standing). none: read-only or ordinary durable write under the project writer. user-consent: interactive confirmation or --yes-policy. policy-record-or-consent: CI needs a pre-existing policy record. security-grant: an admitted RepoExecutionGrantV2. recovery-authority-quorum: an epoch signed by recoveryAuthority keys at its threshold (S4.5); ordinary root keys do not count. exclusive-lease: EXCLUSIVE lease (S7) plus explicit invocation. core-transition-leases: installation fence plus the S7 affected namespace EXCLUSIVE set, derived from the admitted intent and installation registry; same-schema core update/repair require the fence alone.
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Inventory4CommandAuthorizationClass {
    #[serde(rename = "none")]
    None,
    #[serde(rename = "user-consent")]
    UserConsent,
    #[serde(rename = "policy-record-or-consent")]
    PolicyRecordOrConsent,
    #[serde(rename = "security-grant")]
    SecurityGrant,
    #[serde(rename = "recovery-authority-quorum")]
    RecoveryAuthorityQuorum,
    #[serde(rename = "exclusive-lease")]
    ExclusiveLease,
    #[serde(rename = "core-transition-leases")]
    CoreTransitionLeases,
}
impl ::std::fmt::Display for Inventory4CommandAuthorizationClass {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::None => f.write_str("none"),
            Self::UserConsent => f.write_str("user-consent"),
            Self::PolicyRecordOrConsent => f.write_str("policy-record-or-consent"),
            Self::SecurityGrant => f.write_str("security-grant"),
            Self::RecoveryAuthorityQuorum => f.write_str("recovery-authority-quorum"),
            Self::ExclusiveLease => f.write_str("exclusive-lease"),
            Self::CoreTransitionLeases => f.write_str("core-transition-leases"),
        }
    }
}
impl ::std::str::FromStr for Inventory4CommandAuthorizationClass {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "none" => Ok(Self::None),
            "user-consent" => Ok(Self::UserConsent),
            "policy-record-or-consent" => Ok(Self::PolicyRecordOrConsent),
            "security-grant" => Ok(Self::SecurityGrant),
            "recovery-authority-quorum" => Ok(Self::RecoveryAuthorityQuorum),
            "exclusive-lease" => Ok(Self::ExclusiveLease),
            "core-transition-leases" => Ok(Self::CoreTransitionLeases),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Inventory4CommandAuthorizationClass {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Inventory4CommandAuthorizationClass {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Inventory4CommandCli`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Inventory4CommandCli(::std::string::String);
impl ::std::ops::Deref for Inventory4CommandCli {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Inventory4CommandCli> for ::std::string::String {
    fn from(value: Inventory4CommandCli) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Inventory4CommandCli {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 256usize {
            return Err("longer than 256 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Inventory4CommandCli {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Inventory4CommandCli {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Inventory4CommandCli {
    fn deserialize<D>(deserializer: D) -> ::std::result::Result<Self, D::Error>
    where
        D: ::serde::Deserializer<'de>,
    {
        ::std::string::String::deserialize(deserializer)?
            .parse()
            .map_err(|e: self::error::ConversionError| {
                <D::Error as ::serde::de::Error>::custom(e.to_string())
            })
    }
}
///A cross-owner flag join. authorization flags grant or acknowledge an effect; advisory flags only shape output.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Inventory4CommandFlag {
    pub class: Inventory4CommandFlagClass,
    pub flag: Inventory4CommandFlagFlag,
    pub join: Common3BoundedText,
    pub owner: Inventory4CommandFlagOwner,
}
///`Inventory4CommandFlagClass`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Inventory4CommandFlagClass {
    #[serde(rename = "authorization")]
    Authorization,
    #[serde(rename = "advisory")]
    Advisory,
    #[serde(rename = "selection")]
    Selection,
}
impl ::std::fmt::Display for Inventory4CommandFlagClass {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Authorization => f.write_str("authorization"),
            Self::Advisory => f.write_str("advisory"),
            Self::Selection => f.write_str("selection"),
        }
    }
}
impl ::std::str::FromStr for Inventory4CommandFlagClass {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "authorization" => Ok(Self::Authorization),
            "advisory" => Ok(Self::Advisory),
            "selection" => Ok(Self::Selection),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Inventory4CommandFlagClass {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Inventory4CommandFlagClass {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Inventory4CommandFlagFlag`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Inventory4CommandFlagFlag(::std::string::String);
impl ::std::ops::Deref for Inventory4CommandFlagFlag {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Inventory4CommandFlagFlag> for ::std::string::String {
    fn from(value: Inventory4CommandFlagFlag) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Inventory4CommandFlagFlag {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 64usize {
            return Err("longer than 64 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Inventory4CommandFlagFlag {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Inventory4CommandFlagFlag {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Inventory4CommandFlagFlag {
    fn deserialize<D>(deserializer: D) -> ::std::result::Result<Self, D::Error>
    where
        D: ::serde::Deserializer<'de>,
    {
        ::std::string::String::deserialize(deserializer)?
            .parse()
            .map_err(|e: self::error::ConversionError| {
                <D::Error as ::serde::de::Error>::custom(e.to_string())
            })
    }
}
///`Inventory4CommandFlagOwner`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Inventory4CommandFlagOwner {
    #[serde(rename = "workflow")]
    Workflow,
    #[serde(rename = "security")]
    Security,
    #[serde(rename = "identity")]
    Identity,
    #[serde(rename = "native")]
    Native,
    #[serde(rename = "foundation")]
    Foundation,
}
impl ::std::fmt::Display for Inventory4CommandFlagOwner {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Workflow => f.write_str("workflow"),
            Self::Security => f.write_str("security"),
            Self::Identity => f.write_str("identity"),
            Self::Native => f.write_str("native"),
            Self::Foundation => f.write_str("foundation"),
        }
    }
}
impl ::std::str::FromStr for Inventory4CommandFlagOwner {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "workflow" => Ok(Self::Workflow),
            "security" => Ok(Self::Security),
            "identity" => Ok(Self::Identity),
            "native" => Ok(Self::Native),
            "foundation" => Ok(Self::Foundation),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Inventory4CommandFlagOwner {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Inventory4CommandFlagOwner {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Inventory4CommandMetaDispatch`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(tag = "command", content = "paritySelectors", deny_unknown_fields)]
pub enum Inventory4CommandMetaDispatch {
    #[serde(rename = "help")]
    Help { #[serde(rename = "command-names")] command_names: ::std::string::String },
    #[serde(rename = "version")]
    Version {
        #[serde(rename = "build-channel")]
        build_channel: ::std::string::String,
        #[serde(rename = "closure-ids")]
        closure_ids: ::std::string::String,
        #[serde(rename = "host-release")]
        host_release: ::std::string::String,
    },
}
///`Inventory4CommandName`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Inventory4CommandName {
    #[serde(rename = "default")]
    Default,
    #[serde(rename = "recommend")]
    Recommend,
    #[serde(rename = "analyze")]
    Analyze,
    #[serde(rename = "fit")]
    Fit,
    #[serde(rename = "audit")]
    Audit,
    #[serde(rename = "query")]
    Query,
    #[serde(rename = "import")]
    Import,
    #[serde(rename = "baseline-adopt")]
    BaselineAdopt,
    #[serde(rename = "baseline-export")]
    BaselineExport,
    #[serde(rename = "baseline-show")]
    BaselineShow,
    #[serde(rename = "baseline-upgrade")]
    BaselineUpgrade,
    #[serde(rename = "policy-show")]
    PolicyShow,
    #[serde(rename = "policy-init")]
    PolicyInit,
    #[serde(rename = "policy-test")]
    PolicyTest,
    #[serde(rename = "waive")]
    Waive,
    #[serde(rename = "candidates")]
    Candidates,
    #[serde(rename = "inspect")]
    Inspect,
    #[serde(rename = "review-brief")]
    ReviewBrief,
    #[serde(rename = "review-join")]
    ReviewJoin,
    #[serde(rename = "repair-preview")]
    RepairPreview,
    #[serde(rename = "repair-apply")]
    RepairApply,
    #[serde(rename = "repair-verify")]
    RepairVerify,
    #[serde(rename = "repair-recover")]
    RepairRecover,
    #[serde(rename = "test-run")]
    TestRun,
    #[serde(rename = "install")]
    Install,
    #[serde(rename = "update")]
    Update,
    #[serde(rename = "doctor")]
    Doctor,
    #[serde(rename = "purge")]
    Purge,
    #[serde(rename = "agent-serve")]
    AgentServe,
    #[serde(rename = "help")]
    Help,
    #[serde(rename = "version")]
    Version,
    #[serde(rename = "completion")]
    Completion,
    #[serde(rename = "trust-recovery-challenge")]
    TrustRecoveryChallenge,
    #[serde(rename = "trust-recovery-import")]
    TrustRecoveryImport,
    #[serde(rename = "trust-refresh")]
    TrustRefresh,
    #[serde(rename = "trust-import")]
    TrustImport,
    #[serde(rename = "trust-doctor")]
    TrustDoctor,
    #[serde(rename = "store-migrate")]
    StoreMigrate,
    #[serde(rename = "store-rollback")]
    StoreRollback,
    #[serde(rename = "store-gc")]
    StoreGc,
    #[serde(rename = "store-status")]
    StoreStatus,
    #[serde(rename = "native-prepare")]
    NativePrepare,
    #[serde(rename = "core-update")]
    CoreUpdate,
    #[serde(rename = "core-repair")]
    CoreRepair,
    #[serde(rename = "core-rollback")]
    CoreRollback,
}
impl ::std::fmt::Display for Inventory4CommandName {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Default => f.write_str("default"),
            Self::Recommend => f.write_str("recommend"),
            Self::Analyze => f.write_str("analyze"),
            Self::Fit => f.write_str("fit"),
            Self::Audit => f.write_str("audit"),
            Self::Query => f.write_str("query"),
            Self::Import => f.write_str("import"),
            Self::BaselineAdopt => f.write_str("baseline-adopt"),
            Self::BaselineExport => f.write_str("baseline-export"),
            Self::BaselineShow => f.write_str("baseline-show"),
            Self::BaselineUpgrade => f.write_str("baseline-upgrade"),
            Self::PolicyShow => f.write_str("policy-show"),
            Self::PolicyInit => f.write_str("policy-init"),
            Self::PolicyTest => f.write_str("policy-test"),
            Self::Waive => f.write_str("waive"),
            Self::Candidates => f.write_str("candidates"),
            Self::Inspect => f.write_str("inspect"),
            Self::ReviewBrief => f.write_str("review-brief"),
            Self::ReviewJoin => f.write_str("review-join"),
            Self::RepairPreview => f.write_str("repair-preview"),
            Self::RepairApply => f.write_str("repair-apply"),
            Self::RepairVerify => f.write_str("repair-verify"),
            Self::RepairRecover => f.write_str("repair-recover"),
            Self::TestRun => f.write_str("test-run"),
            Self::Install => f.write_str("install"),
            Self::Update => f.write_str("update"),
            Self::Doctor => f.write_str("doctor"),
            Self::Purge => f.write_str("purge"),
            Self::AgentServe => f.write_str("agent-serve"),
            Self::Help => f.write_str("help"),
            Self::Version => f.write_str("version"),
            Self::Completion => f.write_str("completion"),
            Self::TrustRecoveryChallenge => f.write_str("trust-recovery-challenge"),
            Self::TrustRecoveryImport => f.write_str("trust-recovery-import"),
            Self::TrustRefresh => f.write_str("trust-refresh"),
            Self::TrustImport => f.write_str("trust-import"),
            Self::TrustDoctor => f.write_str("trust-doctor"),
            Self::StoreMigrate => f.write_str("store-migrate"),
            Self::StoreRollback => f.write_str("store-rollback"),
            Self::StoreGc => f.write_str("store-gc"),
            Self::StoreStatus => f.write_str("store-status"),
            Self::NativePrepare => f.write_str("native-prepare"),
            Self::CoreUpdate => f.write_str("core-update"),
            Self::CoreRepair => f.write_str("core-repair"),
            Self::CoreRollback => f.write_str("core-rollback"),
        }
    }
}
impl ::std::str::FromStr for Inventory4CommandName {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "default" => Ok(Self::Default),
            "recommend" => Ok(Self::Recommend),
            "analyze" => Ok(Self::Analyze),
            "fit" => Ok(Self::Fit),
            "audit" => Ok(Self::Audit),
            "query" => Ok(Self::Query),
            "import" => Ok(Self::Import),
            "baseline-adopt" => Ok(Self::BaselineAdopt),
            "baseline-export" => Ok(Self::BaselineExport),
            "baseline-show" => Ok(Self::BaselineShow),
            "baseline-upgrade" => Ok(Self::BaselineUpgrade),
            "policy-show" => Ok(Self::PolicyShow),
            "policy-init" => Ok(Self::PolicyInit),
            "policy-test" => Ok(Self::PolicyTest),
            "waive" => Ok(Self::Waive),
            "candidates" => Ok(Self::Candidates),
            "inspect" => Ok(Self::Inspect),
            "review-brief" => Ok(Self::ReviewBrief),
            "review-join" => Ok(Self::ReviewJoin),
            "repair-preview" => Ok(Self::RepairPreview),
            "repair-apply" => Ok(Self::RepairApply),
            "repair-verify" => Ok(Self::RepairVerify),
            "repair-recover" => Ok(Self::RepairRecover),
            "test-run" => Ok(Self::TestRun),
            "install" => Ok(Self::Install),
            "update" => Ok(Self::Update),
            "doctor" => Ok(Self::Doctor),
            "purge" => Ok(Self::Purge),
            "agent-serve" => Ok(Self::AgentServe),
            "help" => Ok(Self::Help),
            "version" => Ok(Self::Version),
            "completion" => Ok(Self::Completion),
            "trust-recovery-challenge" => Ok(Self::TrustRecoveryChallenge),
            "trust-recovery-import" => Ok(Self::TrustRecoveryImport),
            "trust-refresh" => Ok(Self::TrustRefresh),
            "trust-import" => Ok(Self::TrustImport),
            "trust-doctor" => Ok(Self::TrustDoctor),
            "store-migrate" => Ok(Self::StoreMigrate),
            "store-rollback" => Ok(Self::StoreRollback),
            "store-gc" => Ok(Self::StoreGc),
            "store-status" => Ok(Self::StoreStatus),
            "native-prepare" => Ok(Self::NativePrepare),
            "core-update" => Ok(Self::CoreUpdate),
            "core-repair" => Ok(Self::CoreRepair),
            "core-rollback" => Ok(Self::CoreRollback),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Inventory4CommandName {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Inventory4CommandName {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///the contract that owns the command's semantics; the workflow inventory only enumerates and joins
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Inventory4CommandOwner {
    #[serde(rename = "workflow")]
    Workflow,
    #[serde(rename = "security")]
    Security,
    #[serde(rename = "identity")]
    Identity,
    #[serde(rename = "native")]
    Native,
}
impl ::std::fmt::Display for Inventory4CommandOwner {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Workflow => f.write_str("workflow"),
            Self::Security => f.write_str("security"),
            Self::Identity => f.write_str("identity"),
            Self::Native => f.write_str("native"),
        }
    }
}
impl ::std::str::FromStr for Inventory4CommandOwner {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "workflow" => Ok(Self::Workflow),
            "security" => Ok(Self::Security),
            "identity" => Ok(Self::Identity),
            "native" => Ok(Self::Native),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Inventory4CommandOwner {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Inventory4CommandOwner {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Inventory4CommandRepositoryExecution`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Inventory4CommandRepositoryExecution {
    #[serde(rename = "never")]
    Never,
    #[serde(rename = "explicit-authorized")]
    ExplicitAuthorized,
}
impl ::std::fmt::Display for Inventory4CommandRepositoryExecution {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Never => f.write_str("never"),
            Self::ExplicitAuthorized => f.write_str("explicit-authorized"),
        }
    }
}
impl ::std::str::FromStr for Inventory4CommandRepositoryExecution {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "never" => Ok(Self::Never),
            "explicit-authorized" => Ok(Self::ExplicitAuthorized),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Inventory4CommandRepositoryExecution {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Inventory4CommandRepositoryExecution {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///A failure golden (request-rejected or operational-failed) carries its actual domainDetail, unless detailSuppliedBy names the composition that supplies the failure envelope errors.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Inventory4Golden {
    pub class: Common3D9Class,
    pub command: Inventory4CommandName,
    ///workflows-and-surfaces §8: the native §10 route composition supplies errors from the route detail. Absent when domainDetail is present.
    #[serde(
        rename = "detailSuppliedBy",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub detail_supplied_by: FieldPresence<
        ::std::option::Option<Inventory4GoldenDetailSuppliedBy>,
    >,
    #[serde(
        rename = "domainDetail",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub domain_detail: FieldPresence<::std::option::Option<Common3DomainDetailCode>>,
    #[serde(
        rename = "errorCode",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub error_code: FieldPresence<::std::option::Option<Common3D9ErrorCode>>,
    #[serde(rename = "exitCode")]
    pub exit_code: ExactInteger,
    pub id: Common3CanonicalIdentifier,
    #[serde(
        rename = "reasonCode",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub reason_code: FieldPresence<::std::option::Option<Common3D9ReasonCode>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub remedy: FieldPresence<::std::option::Option<Common3BoundedText>>,
    pub situation: Common3BoundedText,
}
///workflows-and-surfaces §8: the native §10 route composition supplies errors from the route detail. Absent when domainDetail is present.
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Inventory4GoldenDetailSuppliedBy {
    #[serde(rename = "native-route-composition")]
    NativeRouteComposition,
}
impl ::std::fmt::Display for Inventory4GoldenDetailSuppliedBy {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::NativeRouteComposition => f.write_str("native-route-composition"),
        }
    }
}
impl ::std::str::FromStr for Inventory4GoldenDetailSuppliedBy {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "native-route-composition" => Ok(Self::NativeRouteComposition),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Inventory4GoldenDetailSuppliedBy {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Inventory4GoldenDetailSuppliedBy {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Inventory4OutputFormat`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Inventory4OutputFormat {
    #[serde(rename = "human")]
    Human,
    #[serde(rename = "json")]
    Json,
    #[serde(rename = "sarif")]
    Sarif,
    #[serde(rename = "html")]
    Html,
    #[serde(rename = "agent")]
    Agent,
}
impl ::std::fmt::Display for Inventory4OutputFormat {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Human => f.write_str("human"),
            Self::Json => f.write_str("json"),
            Self::Sarif => f.write_str("sarif"),
            Self::Html => f.write_str("html"),
            Self::Agent => f.write_str("agent"),
        }
    }
}
impl ::std::str::FromStr for Inventory4OutputFormat {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "human" => Ok(Self::Human),
            "json" => Ok(Self::Json),
            "sarif" => Ok(Self::Sarif),
            "html" => Ok(Self::Html),
            "agent" => Ok(Self::Agent),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Inventory4OutputFormat {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Inventory4OutputFormat {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Closed dispatch of a query-class command: the envelope surface it selects, the step that produces it, the query-step operations it may dispatch, and the exact JSON pointer into CommandEnvelope major 3 for every parity field.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Inventory4QueryDispatch {
    pub operations: ::std::vec::Vec<Inventory4QueryDispatchOperationsItem>,
    #[serde(rename = "parityPaths")]
    pub parity_paths: ::std::collections::BTreeMap<
        Common3CanonicalIdentifier,
        ::std::string::String,
    >,
    #[serde(rename = "stepKind")]
    pub step_kind: Inventory4QueryDispatchStepKind,
    pub surface: Envelope3PropertiesQuerySurface,
}
///`Inventory4QueryDispatchOperationsItem`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(untagged)]
pub enum Inventory4QueryDispatchOperationsItem {
    Graph3Operation(Graph3Operation),
    Invocation3HostQueryOperation(Invocation3HostQueryOperation),
}
impl ::std::fmt::Display for Inventory4QueryDispatchOperationsItem {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match self {
            Self::Graph3Operation(x) => x.fmt(f),
            Self::Invocation3HostQueryOperation(x) => x.fmt(f),
        }
    }
}
impl ::std::str::FromStr for Inventory4QueryDispatchOperationsItem {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if let Ok(v) = value.parse() {
            Ok(Self::Graph3Operation(v))
        } else if let Ok(v) = value.parse() {
            Ok(Self::Invocation3HostQueryOperation(v))
        } else {
            Err("string conversion failed for all variants".into())
        }
    }
}
impl ::std::convert::TryFrom<&str> for Inventory4QueryDispatchOperationsItem {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Inventory4QueryDispatchOperationsItem {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::From<Graph3Operation> for Inventory4QueryDispatchOperationsItem {
    fn from(value: Graph3Operation) -> Self {
        Self::Graph3Operation(value)
    }
}
impl ::std::convert::From<Invocation3HostQueryOperation>
for Inventory4QueryDispatchOperationsItem {
    fn from(value: Invocation3HostQueryOperation) -> Self {
        Self::Invocation3HostQueryOperation(value)
    }
}
///`Inventory4QueryDispatchStepKind`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Inventory4QueryDispatchStepKind {
    #[serde(rename = "query")]
    Query,
    #[serde(rename = "repair-preview")]
    RepairPreview,
}
impl ::std::fmt::Display for Inventory4QueryDispatchStepKind {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Query => f.write_str("query"),
            Self::RepairPreview => f.write_str("repair-preview"),
        }
    }
}
impl ::std::str::FromStr for Inventory4QueryDispatchStepKind {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "query" => Ok(Self::Query),
            "repair-preview" => Ok(Self::RepairPreview),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Inventory4QueryDispatchStepKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Inventory4QueryDispatchStepKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Inventory4Renderer`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Inventory4Renderer {
    pub applicability: ::std::vec::Vec<Inventory4RequestClass>,
    pub format: Inventory4OutputFormat,
    #[serde(rename = "parityRule")]
    pub parity_rule: Common3BoundedText,
    #[serde(rename = "requiredFailureClass")]
    pub required_failure_class: ::serde_json::Value,
    pub version: ::std::num::NonZeroU64,
}
///`Inventory4RequestClass`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Inventory4RequestClass {
    #[serde(rename = "analysis")]
    Analysis,
    #[serde(rename = "query")]
    Query,
    #[serde(rename = "mutation")]
    Mutation,
    #[serde(rename = "lifecycle")]
    Lifecycle,
    #[serde(rename = "execution")]
    Execution,
    #[serde(rename = "serve")]
    Serve,
    #[serde(rename = "meta")]
    Meta,
    #[serde(rename = "trust")]
    Trust,
}
impl ::std::fmt::Display for Inventory4RequestClass {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Analysis => f.write_str("analysis"),
            Self::Query => f.write_str("query"),
            Self::Mutation => f.write_str("mutation"),
            Self::Lifecycle => f.write_str("lifecycle"),
            Self::Execution => f.write_str("execution"),
            Self::Serve => f.write_str("serve"),
            Self::Meta => f.write_str("meta"),
            Self::Trust => f.write_str("trust"),
        }
    }
}
impl ::std::str::FromStr for Inventory4RequestClass {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "analysis" => Ok(Self::Analysis),
            "query" => Ok(Self::Query),
            "mutation" => Ok(Self::Mutation),
            "lifecycle" => Ok(Self::Lifecycle),
            "execution" => Ok(Self::Execution),
            "serve" => Ok(Self::Serve),
            "meta" => Ok(Self::Meta),
            "trust" => Ok(Self::Trust),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Inventory4RequestClass {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Inventory4RequestClass {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Isolated evaluator3 inventory schema. schemaMajor 3 because declared findings parity is FindingSurface (one result per finding3; partialFingerprints only when matched). Successor major4 adds metadata dispatch and selects envelope major4; command authorization and all existing query dispatch remain unchanged.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Inventory4Root {
    pub commands: ::std::vec::Vec<Inventory4Command>,
    pub goldens: ::std::vec::Vec<Inventory4Golden>,
    pub renderers: [Inventory4Renderer; 5usize],
    #[serde(rename = "schemaFamily")]
    pub schema_family: ::serde_json::Value,
    #[serde(rename = "schemaMajor")]
    pub schema_major: ExactInteger,
    ///flags owned by other contracts that the host front end must accept on the listed commands; authorization flags never appear on advisory-only commands
    #[serde(
        rename = "sharedFlags",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub shared_flags: FieldPresence<
        ::std::option::Option<::std::vec::Vec<Inventory4CommandFlag>>,
    >,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub standing: FieldPresence<::std::option::Option<Inventory4RootStanding>>,
}
///`Inventory4RootStanding`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Inventory4RootStanding(::std::string::String);
impl ::std::ops::Deref for Inventory4RootStanding {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Inventory4RootStanding> for ::std::string::String {
    fn from(value: Inventory4RootStanding) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Inventory4RootStanding {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 2048usize {
            return Err("longer than 2048 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Inventory4RootStanding {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Inventory4RootStanding {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Inventory4RootStanding {
    fn deserialize<D>(deserializer: D) -> ::std::result::Result<Self, D::Error>
    where
        D: ::serde::Deserializer<'de>,
    {
        ::std::string::String::deserialize(deserializer)?
            .parse()
            .map_err(|e: self::error::ConversionError| {
                <D::Error as ::serde::de::Error>::custom(e.to_string())
            })
    }
}
///`Inventory6AdvisoryDispatch`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Inventory6AdvisoryDispatch {
    pub operations: ::serde_json::Value,
    #[serde(rename = "parityPaths")]
    pub parity_paths: Inventory6AdvisoryDispatchParityPaths,
    pub request: Inventory6AdvisoryDispatchRequest,
    #[serde(rename = "sourceBinding")]
    pub source_binding: Inventory6AdvisoryDispatchSourceBinding,
    #[serde(rename = "stepKind")]
    pub step_kind: ::std::string::String,
    pub surface: ::std::string::String,
}
///`Inventory6AdvisoryDispatchParityPaths`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Inventory6AdvisoryDispatchParityPaths {
    pub candidates: ::std::string::String,
    #[serde(rename = "candidates-availability")]
    pub candidates_availability: ::std::string::String,
    #[serde(rename = "candidates-next-cursor")]
    pub candidates_next_cursor: ::std::string::String,
    #[serde(rename = "candidates-total-items")]
    pub candidates_total_items: ::std::string::String,
    #[serde(rename = "candidates-truncated")]
    pub candidates_truncated: ::std::string::String,
    #[serde(rename = "capability-availability")]
    pub capability_availability: ::std::string::String,
    #[serde(rename = "evidence-levels")]
    pub evidence_levels: ::std::string::String,
    #[serde(rename = "run-id")]
    pub run_id: ::std::string::String,
    #[serde(rename = "termination-class")]
    pub termination_class: ::std::string::String,
}
///`Inventory6AdvisoryDispatchRequest`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Inventory6AdvisoryDispatchRequest {
    pub completeness: ::std::string::String,
    pub cursor: ::std::string::String,
    pub operation: ::std::string::String,
    pub order: ::std::string::String,
    pub page: Inventory6AdvisoryDispatchRequestPage,
    pub params: Inventory6AdvisoryDispatchRequestParams,
    pub view: ::std::string::String,
}
///`Inventory6AdvisoryDispatchRequestPage`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Inventory6AdvisoryDispatchRequestPage {
    pub size: i64,
}
///`Inventory6AdvisoryDispatchRequestParams`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Inventory6AdvisoryDispatchRequestParams {
    #[serde(rename = "includeSuppressed")]
    pub include_suppressed: bool,
}
///`Inventory6AdvisoryDispatchSourceBinding`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Inventory6AdvisoryDispatchSourceBinding {
    #[serde(rename = "completedResponseCustody")]
    pub completed_response_custody: ::std::string::String,
    pub ephemeral: ::std::string::String,
    #[serde(rename = "noncompletedQuery")]
    pub noncompleted_query: ::std::string::String,
    #[serde(rename = "plannedParams")]
    pub planned_params: Inventory6AdvisoryDispatchSourceBindingPlannedParams,
    #[serde(rename = "requestSchemaMajor")]
    pub request_schema_major: i64,
    pub resolution: ::std::string::String,
}
///`Inventory6AdvisoryDispatchSourceBindingPlannedParams`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Inventory6AdvisoryDispatchSourceBindingPlannedParams {
    pub kind: ::std::string::String,
    pub operation: ::std::string::String,
    #[serde(rename = "sourceStep")]
    pub source_step: i64,
}
///`Inventory6AnalysisProfile`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Inventory6AnalysisProfile {
    #[serde(rename = "default")]
    Default,
    #[serde(rename = "fit")]
    Fit,
    #[serde(rename = "audit")]
    Audit,
    #[serde(rename = "verify")]
    Verify,
    #[serde(rename = "pivot")]
    Pivot,
    #[serde(rename = "policy-test-fixture")]
    PolicyTestFixture,
}
impl ::std::fmt::Display for Inventory6AnalysisProfile {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Default => f.write_str("default"),
            Self::Fit => f.write_str("fit"),
            Self::Audit => f.write_str("audit"),
            Self::Verify => f.write_str("verify"),
            Self::Pivot => f.write_str("pivot"),
            Self::PolicyTestFixture => f.write_str("policy-test-fixture"),
        }
    }
}
impl ::std::str::FromStr for Inventory6AnalysisProfile {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "default" => Ok(Self::Default),
            "fit" => Ok(Self::Fit),
            "audit" => Ok(Self::Audit),
            "verify" => Ok(Self::Verify),
            "pivot" => Ok(Self::Pivot),
            "policy-test-fixture" => Ok(Self::PolicyTestFixture),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Inventory6AnalysisProfile {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Inventory6AnalysisProfile {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Inventory6Command`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Inventory6Command {
    ///true: every output is Map-side and can never be a Control verdict or repair authorization
    pub advisory: bool,
    #[serde(
        rename = "advisoryDispatch",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub advisory_dispatch: FieldPresence<
        ::std::option::Option<Inventory6AdvisoryDispatch>,
    >,
    pub authority: Inventory6CommandAuthority,
    ///what authorizes the command's effect (distinct from advisory, which describes its OUTPUT standing). none: read-only or ordinary durable write under the project writer. user-consent: interactive confirmation or --yes-policy. policy-record-or-consent: CI needs a pre-existing policy record. security-grant: an admitted RepoExecutionGrantV2. recovery-authority-quorum: an epoch signed by recoveryAuthority keys at its threshold (S4.5); ordinary root keys do not count. exclusive-lease: EXCLUSIVE lease (S7) plus explicit invocation. core-transition-leases: installation fence plus the S7 affected namespace EXCLUSIVE set, derived from the admitted intent and installation registry; same-schema core update/repair require the fence alone.
    #[serde(rename = "authorizationClass")]
    pub authorization_class: Inventory6CommandAuthorizationClass,
    pub cli: Inventory6CommandCli,
    ///true when the command may perform the first source-derived write into the private store; such a command must carry the --allow-backup-custody join (identity §5 / TM V17)
    #[serde(
        rename = "firstSourceWrite",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub first_source_write: FieldPresence<::std::option::Option<bool>>,
    pub flags: ::std::vec::Vec<Inventory6CommandFlag>,
    pub formats: ::std::vec::Vec<Inventory6OutputFormat>,
    ///Candidate declared syntax; does not establish independent acceptance of the complete surface.
    #[serde(rename = "grammarStanding")]
    pub grammar_standing: ::serde_json::Value,
    #[serde(
        rename = "metaDispatch",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub meta_dispatch: FieldPresence<
        ::std::option::Option<Inventory6CommandMetaDispatch>,
    >,
    pub name: Inventory6CommandName,
    ///the contract that owns the command's semantics; the workflow inventory only enumerates and joins
    pub owner: Inventory6CommandOwner,
    ///fields whose value must be semantically identical across every applicable renderer of this command
    #[serde(rename = "parityFields")]
    pub parity_fields: ::std::vec::Vec<Common4CanonicalIdentifier>,
    #[serde(
        rename = "queryDispatch",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub query_dispatch: FieldPresence<::std::option::Option<Inventory6QueryDispatch>>,
    #[serde(rename = "repositoryExecution")]
    pub repository_execution: Inventory6CommandRepositoryExecution,
    #[serde(rename = "requestClass")]
    pub request_class: Inventory6RequestClass,
    ///Maximal step-kind summary of the builtin workflow in canonical order; not the exact planned expansion. For the eight html report commands the exact expansions (plan role, requirement, dependsOn, dependencyGate and their conditions) are bound by owner/builtin-step-planning.v1.json; a kind listed here that no admitted grammar can plan (analyze import) is recorded there as unresolved, never silently planned.
    pub steps: ::std::vec::Vec<Invocation5StepKind>,
    ///true only for explicit policy-init/waive/baseline-adopt/baseline-export/baseline-upgrade; no other command writes a tracked file
    #[serde(rename = "writesTrackedIntent")]
    pub writes_tracked_intent: bool,
}
///`Inventory6CommandAuthority`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Inventory6CommandAuthority {
    #[serde(rename = "authoritative-default")]
    AuthoritativeDefault,
    #[serde(rename = "ephemeral-only")]
    EphemeralOnly,
    #[serde(rename = "ephemeral-optional")]
    EphemeralOptional,
    #[serde(rename = "none")]
    None,
}
impl ::std::fmt::Display for Inventory6CommandAuthority {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::AuthoritativeDefault => f.write_str("authoritative-default"),
            Self::EphemeralOnly => f.write_str("ephemeral-only"),
            Self::EphemeralOptional => f.write_str("ephemeral-optional"),
            Self::None => f.write_str("none"),
        }
    }
}
impl ::std::str::FromStr for Inventory6CommandAuthority {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "authoritative-default" => Ok(Self::AuthoritativeDefault),
            "ephemeral-only" => Ok(Self::EphemeralOnly),
            "ephemeral-optional" => Ok(Self::EphemeralOptional),
            "none" => Ok(Self::None),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Inventory6CommandAuthority {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Inventory6CommandAuthority {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///what authorizes the command's effect (distinct from advisory, which describes its OUTPUT standing). none: read-only or ordinary durable write under the project writer. user-consent: interactive confirmation or --yes-policy. policy-record-or-consent: CI needs a pre-existing policy record. security-grant: an admitted RepoExecutionGrantV2. recovery-authority-quorum: an epoch signed by recoveryAuthority keys at its threshold (S4.5); ordinary root keys do not count. exclusive-lease: EXCLUSIVE lease (S7) plus explicit invocation. core-transition-leases: installation fence plus the S7 affected namespace EXCLUSIVE set, derived from the admitted intent and installation registry; same-schema core update/repair require the fence alone.
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Inventory6CommandAuthorizationClass {
    #[serde(rename = "none")]
    None,
    #[serde(rename = "user-consent")]
    UserConsent,
    #[serde(rename = "policy-record-or-consent")]
    PolicyRecordOrConsent,
    #[serde(rename = "security-grant")]
    SecurityGrant,
    #[serde(rename = "recovery-authority-quorum")]
    RecoveryAuthorityQuorum,
    #[serde(rename = "exclusive-lease")]
    ExclusiveLease,
    #[serde(rename = "core-transition-leases")]
    CoreTransitionLeases,
}
impl ::std::fmt::Display for Inventory6CommandAuthorizationClass {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::None => f.write_str("none"),
            Self::UserConsent => f.write_str("user-consent"),
            Self::PolicyRecordOrConsent => f.write_str("policy-record-or-consent"),
            Self::SecurityGrant => f.write_str("security-grant"),
            Self::RecoveryAuthorityQuorum => f.write_str("recovery-authority-quorum"),
            Self::ExclusiveLease => f.write_str("exclusive-lease"),
            Self::CoreTransitionLeases => f.write_str("core-transition-leases"),
        }
    }
}
impl ::std::str::FromStr for Inventory6CommandAuthorizationClass {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "none" => Ok(Self::None),
            "user-consent" => Ok(Self::UserConsent),
            "policy-record-or-consent" => Ok(Self::PolicyRecordOrConsent),
            "security-grant" => Ok(Self::SecurityGrant),
            "recovery-authority-quorum" => Ok(Self::RecoveryAuthorityQuorum),
            "exclusive-lease" => Ok(Self::ExclusiveLease),
            "core-transition-leases" => Ok(Self::CoreTransitionLeases),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Inventory6CommandAuthorizationClass {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Inventory6CommandAuthorizationClass {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Inventory6CommandCli`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Inventory6CommandCli(::std::string::String);
impl ::std::ops::Deref for Inventory6CommandCli {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Inventory6CommandCli> for ::std::string::String {
    fn from(value: Inventory6CommandCli) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Inventory6CommandCli {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 256usize {
            return Err("longer than 256 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Inventory6CommandCli {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Inventory6CommandCli {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Inventory6CommandCli {
    fn deserialize<D>(deserializer: D) -> ::std::result::Result<Self, D::Error>
    where
        D: ::serde::Deserializer<'de>,
    {
        ::std::string::String::deserialize(deserializer)?
            .parse()
            .map_err(|e: self::error::ConversionError| {
                <D::Error as ::serde::de::Error>::custom(e.to_string())
            })
    }
}
///A cross-owner flag join. authorization flags grant or acknowledge an effect; advisory flags only shape output.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Inventory6CommandFlag {
    pub class: Inventory6CommandFlagClass,
    pub flag: Inventory6CommandFlagFlag,
    pub join: Common4BoundedText,
    pub owner: Inventory6CommandFlagOwner,
}
///`Inventory6CommandFlagClass`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Inventory6CommandFlagClass {
    #[serde(rename = "authorization")]
    Authorization,
    #[serde(rename = "advisory")]
    Advisory,
    #[serde(rename = "selection")]
    Selection,
}
impl ::std::fmt::Display for Inventory6CommandFlagClass {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Authorization => f.write_str("authorization"),
            Self::Advisory => f.write_str("advisory"),
            Self::Selection => f.write_str("selection"),
        }
    }
}
impl ::std::str::FromStr for Inventory6CommandFlagClass {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "authorization" => Ok(Self::Authorization),
            "advisory" => Ok(Self::Advisory),
            "selection" => Ok(Self::Selection),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Inventory6CommandFlagClass {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Inventory6CommandFlagClass {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Inventory6CommandFlagFlag`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Inventory6CommandFlagFlag(::std::string::String);
impl ::std::ops::Deref for Inventory6CommandFlagFlag {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Inventory6CommandFlagFlag> for ::std::string::String {
    fn from(value: Inventory6CommandFlagFlag) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Inventory6CommandFlagFlag {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 64usize {
            return Err("longer than 64 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Inventory6CommandFlagFlag {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Inventory6CommandFlagFlag {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Inventory6CommandFlagFlag {
    fn deserialize<D>(deserializer: D) -> ::std::result::Result<Self, D::Error>
    where
        D: ::serde::Deserializer<'de>,
    {
        ::std::string::String::deserialize(deserializer)?
            .parse()
            .map_err(|e: self::error::ConversionError| {
                <D::Error as ::serde::de::Error>::custom(e.to_string())
            })
    }
}
///`Inventory6CommandFlagOwner`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Inventory6CommandFlagOwner {
    #[serde(rename = "workflow")]
    Workflow,
    #[serde(rename = "security")]
    Security,
    #[serde(rename = "identity")]
    Identity,
    #[serde(rename = "native")]
    Native,
    #[serde(rename = "foundation")]
    Foundation,
}
impl ::std::fmt::Display for Inventory6CommandFlagOwner {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Workflow => f.write_str("workflow"),
            Self::Security => f.write_str("security"),
            Self::Identity => f.write_str("identity"),
            Self::Native => f.write_str("native"),
            Self::Foundation => f.write_str("foundation"),
        }
    }
}
impl ::std::str::FromStr for Inventory6CommandFlagOwner {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "workflow" => Ok(Self::Workflow),
            "security" => Ok(Self::Security),
            "identity" => Ok(Self::Identity),
            "native" => Ok(Self::Native),
            "foundation" => Ok(Self::Foundation),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Inventory6CommandFlagOwner {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Inventory6CommandFlagOwner {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Inventory6CommandMetaDispatch`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(tag = "command", content = "paritySelectors", deny_unknown_fields)]
pub enum Inventory6CommandMetaDispatch {
    #[serde(rename = "help")]
    Help { #[serde(rename = "command-names")] command_names: ::std::string::String },
    #[serde(rename = "version")]
    Version {
        #[serde(rename = "build-channel")]
        build_channel: ::std::string::String,
        #[serde(rename = "closure-ids")]
        closure_ids: ::std::string::String,
        #[serde(rename = "host-release")]
        host_release: ::std::string::String,
    },
}
///`Inventory6CommandName`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Inventory6CommandName {
    #[serde(rename = "default")]
    Default,
    #[serde(rename = "recommend")]
    Recommend,
    #[serde(rename = "analyze")]
    Analyze,
    #[serde(rename = "fit")]
    Fit,
    #[serde(rename = "audit")]
    Audit,
    #[serde(rename = "query")]
    Query,
    #[serde(rename = "import")]
    Import,
    #[serde(rename = "baseline-adopt")]
    BaselineAdopt,
    #[serde(rename = "baseline-export")]
    BaselineExport,
    #[serde(rename = "baseline-show")]
    BaselineShow,
    #[serde(rename = "baseline-upgrade")]
    BaselineUpgrade,
    #[serde(rename = "policy-show")]
    PolicyShow,
    #[serde(rename = "policy-init")]
    PolicyInit,
    #[serde(rename = "policy-test")]
    PolicyTest,
    #[serde(rename = "waive")]
    Waive,
    #[serde(rename = "candidates")]
    Candidates,
    #[serde(rename = "inspect")]
    Inspect,
    #[serde(rename = "review-brief")]
    ReviewBrief,
    #[serde(rename = "review-join")]
    ReviewJoin,
    #[serde(rename = "repair-preview")]
    RepairPreview,
    #[serde(rename = "repair-apply")]
    RepairApply,
    #[serde(rename = "repair-verify")]
    RepairVerify,
    #[serde(rename = "repair-recover")]
    RepairRecover,
    #[serde(rename = "test-run")]
    TestRun,
    #[serde(rename = "install")]
    Install,
    #[serde(rename = "update")]
    Update,
    #[serde(rename = "doctor")]
    Doctor,
    #[serde(rename = "purge")]
    Purge,
    #[serde(rename = "agent-serve")]
    AgentServe,
    #[serde(rename = "help")]
    Help,
    #[serde(rename = "version")]
    Version,
    #[serde(rename = "completion")]
    Completion,
    #[serde(rename = "trust-recovery-challenge")]
    TrustRecoveryChallenge,
    #[serde(rename = "trust-recovery-import")]
    TrustRecoveryImport,
    #[serde(rename = "trust-refresh")]
    TrustRefresh,
    #[serde(rename = "trust-import")]
    TrustImport,
    #[serde(rename = "trust-doctor")]
    TrustDoctor,
    #[serde(rename = "store-migrate")]
    StoreMigrate,
    #[serde(rename = "store-rollback")]
    StoreRollback,
    #[serde(rename = "store-gc")]
    StoreGc,
    #[serde(rename = "store-status")]
    StoreStatus,
    #[serde(rename = "native-prepare")]
    NativePrepare,
    #[serde(rename = "core-update")]
    CoreUpdate,
    #[serde(rename = "core-repair")]
    CoreRepair,
    #[serde(rename = "core-rollback")]
    CoreRollback,
}
impl ::std::fmt::Display for Inventory6CommandName {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Default => f.write_str("default"),
            Self::Recommend => f.write_str("recommend"),
            Self::Analyze => f.write_str("analyze"),
            Self::Fit => f.write_str("fit"),
            Self::Audit => f.write_str("audit"),
            Self::Query => f.write_str("query"),
            Self::Import => f.write_str("import"),
            Self::BaselineAdopt => f.write_str("baseline-adopt"),
            Self::BaselineExport => f.write_str("baseline-export"),
            Self::BaselineShow => f.write_str("baseline-show"),
            Self::BaselineUpgrade => f.write_str("baseline-upgrade"),
            Self::PolicyShow => f.write_str("policy-show"),
            Self::PolicyInit => f.write_str("policy-init"),
            Self::PolicyTest => f.write_str("policy-test"),
            Self::Waive => f.write_str("waive"),
            Self::Candidates => f.write_str("candidates"),
            Self::Inspect => f.write_str("inspect"),
            Self::ReviewBrief => f.write_str("review-brief"),
            Self::ReviewJoin => f.write_str("review-join"),
            Self::RepairPreview => f.write_str("repair-preview"),
            Self::RepairApply => f.write_str("repair-apply"),
            Self::RepairVerify => f.write_str("repair-verify"),
            Self::RepairRecover => f.write_str("repair-recover"),
            Self::TestRun => f.write_str("test-run"),
            Self::Install => f.write_str("install"),
            Self::Update => f.write_str("update"),
            Self::Doctor => f.write_str("doctor"),
            Self::Purge => f.write_str("purge"),
            Self::AgentServe => f.write_str("agent-serve"),
            Self::Help => f.write_str("help"),
            Self::Version => f.write_str("version"),
            Self::Completion => f.write_str("completion"),
            Self::TrustRecoveryChallenge => f.write_str("trust-recovery-challenge"),
            Self::TrustRecoveryImport => f.write_str("trust-recovery-import"),
            Self::TrustRefresh => f.write_str("trust-refresh"),
            Self::TrustImport => f.write_str("trust-import"),
            Self::TrustDoctor => f.write_str("trust-doctor"),
            Self::StoreMigrate => f.write_str("store-migrate"),
            Self::StoreRollback => f.write_str("store-rollback"),
            Self::StoreGc => f.write_str("store-gc"),
            Self::StoreStatus => f.write_str("store-status"),
            Self::NativePrepare => f.write_str("native-prepare"),
            Self::CoreUpdate => f.write_str("core-update"),
            Self::CoreRepair => f.write_str("core-repair"),
            Self::CoreRollback => f.write_str("core-rollback"),
        }
    }
}
impl ::std::str::FromStr for Inventory6CommandName {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "default" => Ok(Self::Default),
            "recommend" => Ok(Self::Recommend),
            "analyze" => Ok(Self::Analyze),
            "fit" => Ok(Self::Fit),
            "audit" => Ok(Self::Audit),
            "query" => Ok(Self::Query),
            "import" => Ok(Self::Import),
            "baseline-adopt" => Ok(Self::BaselineAdopt),
            "baseline-export" => Ok(Self::BaselineExport),
            "baseline-show" => Ok(Self::BaselineShow),
            "baseline-upgrade" => Ok(Self::BaselineUpgrade),
            "policy-show" => Ok(Self::PolicyShow),
            "policy-init" => Ok(Self::PolicyInit),
            "policy-test" => Ok(Self::PolicyTest),
            "waive" => Ok(Self::Waive),
            "candidates" => Ok(Self::Candidates),
            "inspect" => Ok(Self::Inspect),
            "review-brief" => Ok(Self::ReviewBrief),
            "review-join" => Ok(Self::ReviewJoin),
            "repair-preview" => Ok(Self::RepairPreview),
            "repair-apply" => Ok(Self::RepairApply),
            "repair-verify" => Ok(Self::RepairVerify),
            "repair-recover" => Ok(Self::RepairRecover),
            "test-run" => Ok(Self::TestRun),
            "install" => Ok(Self::Install),
            "update" => Ok(Self::Update),
            "doctor" => Ok(Self::Doctor),
            "purge" => Ok(Self::Purge),
            "agent-serve" => Ok(Self::AgentServe),
            "help" => Ok(Self::Help),
            "version" => Ok(Self::Version),
            "completion" => Ok(Self::Completion),
            "trust-recovery-challenge" => Ok(Self::TrustRecoveryChallenge),
            "trust-recovery-import" => Ok(Self::TrustRecoveryImport),
            "trust-refresh" => Ok(Self::TrustRefresh),
            "trust-import" => Ok(Self::TrustImport),
            "trust-doctor" => Ok(Self::TrustDoctor),
            "store-migrate" => Ok(Self::StoreMigrate),
            "store-rollback" => Ok(Self::StoreRollback),
            "store-gc" => Ok(Self::StoreGc),
            "store-status" => Ok(Self::StoreStatus),
            "native-prepare" => Ok(Self::NativePrepare),
            "core-update" => Ok(Self::CoreUpdate),
            "core-repair" => Ok(Self::CoreRepair),
            "core-rollback" => Ok(Self::CoreRollback),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Inventory6CommandName {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Inventory6CommandName {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///the contract that owns the command's semantics; the workflow inventory only enumerates and joins
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Inventory6CommandOwner {
    #[serde(rename = "workflow")]
    Workflow,
    #[serde(rename = "security")]
    Security,
    #[serde(rename = "identity")]
    Identity,
    #[serde(rename = "native")]
    Native,
}
impl ::std::fmt::Display for Inventory6CommandOwner {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Workflow => f.write_str("workflow"),
            Self::Security => f.write_str("security"),
            Self::Identity => f.write_str("identity"),
            Self::Native => f.write_str("native"),
        }
    }
}
impl ::std::str::FromStr for Inventory6CommandOwner {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "workflow" => Ok(Self::Workflow),
            "security" => Ok(Self::Security),
            "identity" => Ok(Self::Identity),
            "native" => Ok(Self::Native),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Inventory6CommandOwner {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Inventory6CommandOwner {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Inventory6CommandRepositoryExecution`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Inventory6CommandRepositoryExecution {
    #[serde(rename = "never")]
    Never,
    #[serde(rename = "explicit-authorized")]
    ExplicitAuthorized,
}
impl ::std::fmt::Display for Inventory6CommandRepositoryExecution {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Never => f.write_str("never"),
            Self::ExplicitAuthorized => f.write_str("explicit-authorized"),
        }
    }
}
impl ::std::str::FromStr for Inventory6CommandRepositoryExecution {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "never" => Ok(Self::Never),
            "explicit-authorized" => Ok(Self::ExplicitAuthorized),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Inventory6CommandRepositoryExecution {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Inventory6CommandRepositoryExecution {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///A failure golden (request-rejected or operational-failed) carries its actual domainDetail, unless detailSuppliedBy names the composition that supplies the failure envelope errors.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Inventory6Golden {
    pub class: Common4D9Class,
    pub command: Inventory6CommandName,
    ///workflows-and-surfaces §8: the native §10 route composition supplies errors from the route detail. Absent when domainDetail is present.
    #[serde(
        rename = "detailSuppliedBy",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub detail_supplied_by: FieldPresence<
        ::std::option::Option<Inventory6GoldenDetailSuppliedBy>,
    >,
    #[serde(
        rename = "domainDetail",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub domain_detail: FieldPresence<::std::option::Option<Common4DomainDetailCode>>,
    #[serde(
        rename = "errorCode",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub error_code: FieldPresence<::std::option::Option<Common4D9ErrorCode>>,
    #[serde(rename = "exitCode")]
    pub exit_code: ExactInteger,
    pub id: Common4CanonicalIdentifier,
    #[serde(
        rename = "reasonCode",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub reason_code: FieldPresence<::std::option::Option<Common4D9ReasonCode>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub remedy: FieldPresence<::std::option::Option<Common4BoundedText>>,
    pub situation: Common4BoundedText,
}
///workflows-and-surfaces §8: the native §10 route composition supplies errors from the route detail. Absent when domainDetail is present.
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Inventory6GoldenDetailSuppliedBy {
    #[serde(rename = "native-route-composition")]
    NativeRouteComposition,
}
impl ::std::fmt::Display for Inventory6GoldenDetailSuppliedBy {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::NativeRouteComposition => f.write_str("native-route-composition"),
        }
    }
}
impl ::std::str::FromStr for Inventory6GoldenDetailSuppliedBy {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "native-route-composition" => Ok(Self::NativeRouteComposition),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Inventory6GoldenDetailSuppliedBy {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Inventory6GoldenDetailSuppliedBy {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Inventory6OutputFormat`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Inventory6OutputFormat {
    #[serde(rename = "human")]
    Human,
    #[serde(rename = "json")]
    Json,
    #[serde(rename = "sarif")]
    Sarif,
    #[serde(rename = "html")]
    Html,
    #[serde(rename = "agent")]
    Agent,
}
impl ::std::fmt::Display for Inventory6OutputFormat {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Human => f.write_str("human"),
            Self::Json => f.write_str("json"),
            Self::Sarif => f.write_str("sarif"),
            Self::Html => f.write_str("html"),
            Self::Agent => f.write_str("agent"),
        }
    }
}
impl ::std::str::FromStr for Inventory6OutputFormat {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "human" => Ok(Self::Human),
            "json" => Ok(Self::Json),
            "sarif" => Ok(Self::Sarif),
            "html" => Ok(Self::Html),
            "agent" => Ok(Self::Agent),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Inventory6OutputFormat {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Inventory6OutputFormat {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Closed dispatch of a query-class command: the envelope surface it selects, the step that produces it, the query-step operations it may dispatch, and the exact JSON pointer into CommandEnvelope major 3 for every parity field.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Inventory6QueryDispatch {
    pub operations: ::std::vec::Vec<Inventory6QueryDispatchOperationsItem>,
    #[serde(rename = "parityPaths")]
    pub parity_paths: ::std::collections::BTreeMap<
        Common4CanonicalIdentifier,
        ::std::string::String,
    >,
    #[serde(rename = "stepKind")]
    pub step_kind: Inventory6QueryDispatchStepKind,
    pub surface: Envelope7PropertiesQuerySurface,
}
///`Inventory6QueryDispatchOperationsItem`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(untagged)]
pub enum Inventory6QueryDispatchOperationsItem {
    Graph4Operation(Graph4Operation),
    Invocation5HostQueryOperation(Invocation5HostQueryOperation),
}
impl ::std::fmt::Display for Inventory6QueryDispatchOperationsItem {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match self {
            Self::Graph4Operation(x) => x.fmt(f),
            Self::Invocation5HostQueryOperation(x) => x.fmt(f),
        }
    }
}
impl ::std::str::FromStr for Inventory6QueryDispatchOperationsItem {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if let Ok(v) = value.parse() {
            Ok(Self::Graph4Operation(v))
        } else if let Ok(v) = value.parse() {
            Ok(Self::Invocation5HostQueryOperation(v))
        } else {
            Err("string conversion failed for all variants".into())
        }
    }
}
impl ::std::convert::TryFrom<&str> for Inventory6QueryDispatchOperationsItem {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Inventory6QueryDispatchOperationsItem {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::From<Graph4Operation> for Inventory6QueryDispatchOperationsItem {
    fn from(value: Graph4Operation) -> Self {
        Self::Graph4Operation(value)
    }
}
impl ::std::convert::From<Invocation5HostQueryOperation>
for Inventory6QueryDispatchOperationsItem {
    fn from(value: Invocation5HostQueryOperation) -> Self {
        Self::Invocation5HostQueryOperation(value)
    }
}
///`Inventory6QueryDispatchStepKind`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Inventory6QueryDispatchStepKind {
    #[serde(rename = "query")]
    Query,
    #[serde(rename = "repair-preview")]
    RepairPreview,
}
impl ::std::fmt::Display for Inventory6QueryDispatchStepKind {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Query => f.write_str("query"),
            Self::RepairPreview => f.write_str("repair-preview"),
        }
    }
}
impl ::std::str::FromStr for Inventory6QueryDispatchStepKind {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "query" => Ok(Self::Query),
            "repair-preview" => Ok(Self::RepairPreview),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Inventory6QueryDispatchStepKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Inventory6QueryDispatchStepKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Inventory6Renderer`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Inventory6Renderer {
    pub applicability: ::std::vec::Vec<Inventory6RequestClass>,
    pub format: Inventory6OutputFormat,
    #[serde(rename = "parityRule")]
    pub parity_rule: Common4BoundedText,
    #[serde(rename = "requiredFailureClass")]
    pub required_failure_class: ::serde_json::Value,
    pub version: ::std::num::NonZeroU64,
}
///`Inventory6RequestClass`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Inventory6RequestClass {
    #[serde(rename = "analysis")]
    Analysis,
    #[serde(rename = "query")]
    Query,
    #[serde(rename = "mutation")]
    Mutation,
    #[serde(rename = "lifecycle")]
    Lifecycle,
    #[serde(rename = "execution")]
    Execution,
    #[serde(rename = "serve")]
    Serve,
    #[serde(rename = "meta")]
    Meta,
    #[serde(rename = "trust")]
    Trust,
}
impl ::std::fmt::Display for Inventory6RequestClass {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Analysis => f.write_str("analysis"),
            Self::Query => f.write_str("query"),
            Self::Mutation => f.write_str("mutation"),
            Self::Lifecycle => f.write_str("lifecycle"),
            Self::Execution => f.write_str("execution"),
            Self::Serve => f.write_str("serve"),
            Self::Meta => f.write_str("meta"),
            Self::Trust => f.write_str("trust"),
        }
    }
}
impl ::std::str::FromStr for Inventory6RequestClass {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "analysis" => Ok(Self::Analysis),
            "query" => Ok(Self::Query),
            "mutation" => Ok(Self::Mutation),
            "lifecycle" => Ok(Self::Lifecycle),
            "execution" => Ok(Self::Execution),
            "serve" => Ok(Self::Serve),
            "meta" => Ok(Self::Meta),
            "trust" => Ok(Self::Trust),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Inventory6RequestClass {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Inventory6RequestClass {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Unaccepted successor of report08 inventory5. Existing authorization, format applicability and parity pointers remain unchanged. New query steps use invocation5 and query4; the complete envelope7 remains the parity reference.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Inventory6Root {
    pub commands: ::std::vec::Vec<Inventory6Command>,
    pub goldens: ::std::vec::Vec<Inventory6Golden>,
    pub renderers: [Inventory6Renderer; 5usize],
    #[serde(rename = "schemaFamily")]
    pub schema_family: ::serde_json::Value,
    #[serde(rename = "schemaMajor")]
    pub schema_major: ExactInteger,
    ///flags owned by other contracts that the host front end must accept on the listed commands; authorization flags never appear on advisory-only commands
    #[serde(
        rename = "sharedFlags",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub shared_flags: FieldPresence<
        ::std::option::Option<::std::vec::Vec<Inventory6CommandFlag>>,
    >,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub standing: FieldPresence<::std::option::Option<Inventory6RootStanding>>,
}
///`Inventory6RootStanding`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Inventory6RootStanding(::std::string::String);
impl ::std::ops::Deref for Inventory6RootStanding {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Inventory6RootStanding> for ::std::string::String {
    fn from(value: Inventory6RootStanding) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Inventory6RootStanding {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 2048usize {
            return Err("longer than 2048 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Inventory6RootStanding {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Inventory6RootStanding {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Inventory6RootStanding {
    fn deserialize<D>(deserializer: D) -> ::std::result::Result<Self, D::Error>
    where
        D: ::serde::Deserializer<'de>,
    {
        ::std::string::String::deserialize(deserializer)?
            .parse()
            .map_err(|e: self::error::ConversionError| {
                <D::Error as ::serde::de::Error>::custom(e.to_string())
            })
    }
}
///`Invocation3AnalysisParams`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation3AnalysisParams {
    #[serde(
        rename = "afterStep",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub after_step: FieldPresence<::std::option::Option<Common3StepId>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub baseline: FieldPresence<
        ::std::option::Option<Invocation3AnalysisParamsBaseline>,
    >,
    pub durability: Invocation3AnalysisParamsDurability,
    #[serde(
        rename = "importedEvidenceSteps",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub imported_evidence_steps: FieldPresence<
        ::std::option::Option<::std::vec::Vec<Common3StepId>>,
    >,
    pub kind: ::serde_json::Value,
    #[serde(
        rename = "pivotClosureIds",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub pivot_closure_ids: FieldPresence<
        ::std::option::Option<::std::vec::Vec<Common3ClosureId>>,
    >,
    #[serde(
        rename = "pivotOfStep",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub pivot_of_step: FieldPresence<::std::option::Option<Common3StepId>>,
    pub profile: Inventory3AnalysisProfile,
    ///pivot: the baseline's prior detector closure over current source, auto-planned before the primary analysis when a comparison needs the detector pivot and the closure is admitted
    pub role: Invocation3AnalysisParamsRole,
    ///fresh-after-step: a new snapshot is admitted after afterStep completed; never reuses a snapshot captured before a mutation
    #[serde(rename = "snapshotSource")]
    pub snapshot_source: Invocation3AnalysisParamsSnapshotSource,
    ///Step gate participation. self (default when absent): the Run verdict terminates this step (fail → policy-failed). delegated: this analysis supplies the current Run to exactly one later comparison step (which must name it as currentStep); its Run verdict does NOT terminate the step — completion, operational faults and requiredCoverage≠satisfied / verdict=indeterminate still do. A delegated analysis with no consuming comparison step is WORKFLOW.VERDICT_GATE_UNBOUND (request-rejected). A pivot analysis is always delegated.
    #[serde(
        rename = "verdictGate",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub verdict_gate: FieldPresence<
        ::std::option::Option<Invocation3AnalysisParamsVerdictGate>,
    >,
}
///`Invocation3AnalysisParamsBaseline`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation3AnalysisParamsBaseline {
    #[serde(
        rename = "acceptOriginProjectIds",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub accept_origin_project_ids: FieldPresence<
        ::std::option::Option<::std::vec::Vec<Common3ProjectId>>,
    >,
    #[serde(rename = "auditProfile")]
    pub audit_profile: Comparison2AuditProfileName,
    #[serde(
        rename = "closureBundlePath",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub closure_bundle_path: FieldPresence<::std::option::Option<Common3UserInputPath>>,
    pub path: Common3UserInputPath,
}
///`Invocation3AnalysisParamsDurability`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation3AnalysisParamsDurability {
    #[serde(rename = "authoritative")]
    Authoritative,
    #[serde(rename = "ephemeral")]
    Ephemeral,
}
impl ::std::fmt::Display for Invocation3AnalysisParamsDurability {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Authoritative => f.write_str("authoritative"),
            Self::Ephemeral => f.write_str("ephemeral"),
        }
    }
}
impl ::std::str::FromStr for Invocation3AnalysisParamsDurability {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "authoritative" => Ok(Self::Authoritative),
            "ephemeral" => Ok(Self::Ephemeral),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation3AnalysisParamsDurability {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Invocation3AnalysisParamsDurability {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///pivot: the baseline's prior detector closure over current source, auto-planned before the primary analysis when a comparison needs the detector pivot and the closure is admitted
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation3AnalysisParamsRole {
    #[serde(rename = "primary")]
    Primary,
    #[serde(rename = "pivot")]
    Pivot,
}
impl ::std::fmt::Display for Invocation3AnalysisParamsRole {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Primary => f.write_str("primary"),
            Self::Pivot => f.write_str("pivot"),
        }
    }
}
impl ::std::str::FromStr for Invocation3AnalysisParamsRole {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "primary" => Ok(Self::Primary),
            "pivot" => Ok(Self::Pivot),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation3AnalysisParamsRole {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Invocation3AnalysisParamsRole {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///fresh-after-step: a new snapshot is admitted after afterStep completed; never reuses a snapshot captured before a mutation
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation3AnalysisParamsSnapshotSource {
    #[serde(rename = "live-worktree")]
    LiveWorktree,
    #[serde(rename = "fresh-after-step")]
    FreshAfterStep,
}
impl ::std::fmt::Display for Invocation3AnalysisParamsSnapshotSource {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::LiveWorktree => f.write_str("live-worktree"),
            Self::FreshAfterStep => f.write_str("fresh-after-step"),
        }
    }
}
impl ::std::str::FromStr for Invocation3AnalysisParamsSnapshotSource {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "live-worktree" => Ok(Self::LiveWorktree),
            "fresh-after-step" => Ok(Self::FreshAfterStep),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation3AnalysisParamsSnapshotSource {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Invocation3AnalysisParamsSnapshotSource {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Step gate participation. self (default when absent): the Run verdict terminates this step (fail → policy-failed). delegated: this analysis supplies the current Run to exactly one later comparison step (which must name it as currentStep); its Run verdict does NOT terminate the step — completion, operational faults and requiredCoverage≠satisfied / verdict=indeterminate still do. A delegated analysis with no consuming comparison step is WORKFLOW.VERDICT_GATE_UNBOUND (request-rejected). A pivot analysis is always delegated.
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation3AnalysisParamsVerdictGate {
    #[serde(rename = "self")]
    Self_,
    #[serde(rename = "delegated")]
    Delegated,
}
impl ::std::fmt::Display for Invocation3AnalysisParamsVerdictGate {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Self_ => f.write_str("self"),
            Self::Delegated => f.write_str("delegated"),
        }
    }
}
impl ::std::str::FromStr for Invocation3AnalysisParamsVerdictGate {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "self" => Ok(Self::Self_),
            "delegated" => Ok(Self::Delegated),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation3AnalysisParamsVerdictGate {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Invocation3AnalysisParamsVerdictGate {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Closed union. authoritative: a committed Run with receipt. ephemeral: no Run, no receipt, no authority; carries only semantic plan/evidence identities so that a result can be cited, and can never satisfy baseline adoption, repair preconditions, or verify.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(tag = "authority", deny_unknown_fields)]
pub enum Invocation3AnalysisResult {
    #[serde(rename = "authoritative")]
    Authoritative {
        #[serde(
            rename = "comparisonResultId",
            default,
            skip_serializing_if = "FieldPresence::is_missing"
        )]
        comparison_result_id: FieldPresence<
            ::std::option::Option<Common3ComparisonResultId>,
        >,
        #[serde(
            rename = "coverageId",
            default,
            skip_serializing_if = "FieldPresence::is_missing"
        )]
        coverage_id: FieldPresence<::std::option::Option<Common3CoverageId>>,
        deficiency: Common3D9Deficiency,
        durability: ::serde_json::Value,
        kind: Invocation3AnalysisResultKind,
        #[serde(rename = "planId")]
        plan_id: Common3PlanId,
        #[serde(rename = "requiredCoverage")]
        required_coverage: Common3RequiredCoverage,
        #[serde(rename = "runId")]
        run_id: Common3RunId,
        #[serde(rename = "secondaryDeficiencies")]
        secondary_deficiencies: ::std::vec::Vec<Common3D9Deficiency>,
        verdict: Common3Verdict,
        #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
        verification: FieldPresence<
            ::std::option::Option<Invocation3VerificationOutcome>,
        >,
    },
    #[serde(rename = "ephemeral")]
    Ephemeral {
        #[serde(
            rename = "comparisonResultId",
            default,
            skip_serializing_if = "FieldPresence::is_missing"
        )]
        comparison_result_id: FieldPresence<
            ::std::option::Option<Common3ComparisonResultId>,
        >,
        #[serde(
            rename = "coverageId",
            default,
            skip_serializing_if = "FieldPresence::is_missing"
        )]
        coverage_id: FieldPresence<::std::option::Option<Common3CoverageId>>,
        deficiency: Common3D9Deficiency,
        durability: ::serde_json::Value,
        #[serde(rename = "evidenceId")]
        evidence_id: Common3EvidenceId,
        kind: ::serde_json::Value,
        #[serde(rename = "planId")]
        plan_id: Common3PlanId,
        #[serde(rename = "requiredCoverage")]
        required_coverage: Common3RequiredCoverage,
        #[serde(rename = "secondaryDeficiencies")]
        secondary_deficiencies: ::std::vec::Vec<Common3D9Deficiency>,
        verdict: Common3Verdict,
    },
}
///`Invocation3AnalysisResultKind`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation3AnalysisResultKind {
    #[serde(rename = "analysis")]
    Analysis,
    #[serde(rename = "verify")]
    Verify,
}
impl ::std::fmt::Display for Invocation3AnalysisResultKind {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Analysis => f.write_str("analysis"),
            Self::Verify => f.write_str("verify"),
        }
    }
}
impl ::std::str::FromStr for Invocation3AnalysisResultKind {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "analysis" => Ok(Self::Analysis),
            "verify" => Ok(Self::Verify),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation3AnalysisResultKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Invocation3AnalysisResultKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Invocation3Attempt`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation3Attempt {
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub derivation: FieldPresence<::std::option::Option<Invocation3DerivationBinding>>,
    #[serde(rename = "executionId")]
    pub execution_id: Common3ExecutionId,
    #[serde(
        rename = "faultCause",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub fault_cause: FieldPresence<::std::option::Option<Common3D9FaultCause>>,
    ///Installation mutation attempts only. Initial attempt: first LEASED after all locks, then durable revisions written in order. Recovery attempt: first is the observed installationRecoveryStartRef (any closed state), then revisions written by this attempt. Earlier attempt records remain unchanged. Required once a journal exists, including failed/abandoned attempts; absent before any journal. Operational custody, excluded from Run identity.
    #[serde(
        rename = "installationJournalRefs",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub installation_journal_refs: FieldPresence<
        ::std::option::Option<::std::vec::Vec<Common3InstallationTransitionJournalRef>>,
    >,
    ///Recovery attempt only: exact current durable revision read under the installation fence; equals installationJournalRefs[0]. It is host-observed, never accepted from request input.
    #[serde(
        rename = "installationRecoveryStartRef",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub installation_recovery_start_ref: FieldPresence<
        ::std::option::Option<Common3InstallationTransitionJournalRef>,
    >,
    pub outcome: Invocation3AttemptOutcome,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub retried: FieldPresence<::std::option::Option<bool>>,
}
///`Invocation3AttemptOutcome`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation3AttemptOutcome {
    #[serde(rename = "completed")]
    Completed,
    #[serde(rename = "rejected")]
    Rejected,
    #[serde(rename = "failed")]
    Failed,
    #[serde(rename = "cancelled")]
    Cancelled,
    #[serde(rename = "abandoned")]
    Abandoned,
}
impl ::std::fmt::Display for Invocation3AttemptOutcome {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Completed => f.write_str("completed"),
            Self::Rejected => f.write_str("rejected"),
            Self::Failed => f.write_str("failed"),
            Self::Cancelled => f.write_str("cancelled"),
            Self::Abandoned => f.write_str("abandoned"),
        }
    }
}
impl ::std::str::FromStr for Invocation3AttemptOutcome {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "completed" => Ok(Self::Completed),
            "rejected" => Ok(Self::Rejected),
            "failed" => Ok(Self::Failed),
            "cancelled" => Ok(Self::Cancelled),
            "abandoned" => Ok(Self::Abandoned),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation3AttemptOutcome {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Invocation3AttemptOutcome {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///baseline show [PATH]: the tracked baseline artifact path (default opensip.baseline.json resolved by the host).
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation3BaselineInspectRequestV1 {
    pub operation: ::serde_json::Value,
    pub path: Common3UserInputPath,
}
///`Invocation3Cancellation`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation3Cancellation {
    ///before-settle: at least one required step had not reached a terminal outcome; aggregate is interrupted (130). after-settle: every required step already reached a terminal outcome; the aggregate termination is not reclassified.
    pub phase: Invocation3CancellationPhase,
    pub requested: bool,
    pub signal: Common3D9Signal,
}
///before-settle: at least one required step had not reached a terminal outcome; aggregate is interrupted (130). after-settle: every required step already reached a terminal outcome; the aggregate termination is not reclassified.
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation3CancellationPhase {
    #[serde(rename = "none")]
    None,
    #[serde(rename = "before-settle")]
    BeforeSettle,
    #[serde(rename = "after-settle")]
    AfterSettle,
}
impl ::std::fmt::Display for Invocation3CancellationPhase {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::None => f.write_str("none"),
            Self::BeforeSettle => f.write_str("before-settle"),
            Self::AfterSettle => f.write_str("after-settle"),
        }
    }
}
impl ::std::str::FromStr for Invocation3CancellationPhase {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "none" => Ok(Self::None),
            "before-settle" => Ok(Self::BeforeSettle),
            "after-settle" => Ok(Self::AfterSettle),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation3CancellationPhase {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Invocation3CancellationPhase {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Invocation3ComparisonParams`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation3ComparisonParams {
    #[serde(
        rename = "acceptOriginProjectIds",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub accept_origin_project_ids: FieldPresence<
        ::std::option::Option<::std::vec::Vec<Common3ProjectId>>,
    >,
    #[serde(rename = "auditProfile")]
    pub audit_profile: Comparison2AuditProfileName,
    pub baseline: Common3UserInputPath,
    #[serde(
        rename = "closureBundlePath",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub closure_bundle_path: FieldPresence<::std::option::Option<Common3UserInputPath>>,
    ///the authoritative primary analysis whose Run is the current side; that step must carry verdictGate=delegated and must be in dependsOn
    #[serde(rename = "currentStep")]
    pub current_step: Common3StepId,
    pub kind: ::serde_json::Value,
    ///the role=pivot analysis step when E0 is needed; must be in dependsOn
    #[serde(
        rename = "pivotStep",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub pivot_step: FieldPresence<::std::option::Option<Common3StepId>>,
}
///Operational projection of a ComparisonResultV1. The step termination is derived from verdict: fail → policy-failed (runId = currentRunId); indeterminate → indeterminate with reasonCodes [VERDICT.INDETERMINATE] or [BASELINE.RECIPE_UNSUPPORTED] per d9Deficiency and the descriptor remedy as domainDetail; pass → success (runId = currentRunId). Never defaults to success.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation3ComparisonStepResult {
    #[serde(rename = "baselineId")]
    pub baseline_id: Common3BaselineId,
    #[serde(rename = "comparisonPerformed")]
    pub comparison_performed: bool,
    #[serde(rename = "comparisonResultId")]
    pub comparison_result_id: Common3ComparisonResultId,
    pub counts: Invocation3ComparisonStepResultCounts,
    #[serde(rename = "currentRunId")]
    pub current_run_id: Common3RunId,
    #[serde(
        rename = "d9Deficiency",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub d9_deficiency: FieldPresence<::std::option::Option<Common3D9Deficiency>>,
    pub kind: ::serde_json::Value,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub remedy: FieldPresence<::std::option::Option<Common3DomainDetail>>,
    pub verdict: Invocation3ComparisonStepResultVerdict,
}
///`Invocation3ComparisonStepResultCounts`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation3ComparisonStepResultCounts {
    pub entries: Common3Uint53,
    pub gating: Common3Uint53,
    pub indeterminate: Common3Uint53,
}
///`Invocation3ComparisonStepResultVerdict`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation3ComparisonStepResultVerdict {
    #[serde(rename = "pass")]
    Pass,
    #[serde(rename = "fail")]
    Fail,
    #[serde(rename = "indeterminate")]
    Indeterminate,
}
impl ::std::fmt::Display for Invocation3ComparisonStepResultVerdict {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Pass => f.write_str("pass"),
            Self::Fail => f.write_str("fail"),
            Self::Indeterminate => f.write_str("indeterminate"),
        }
    }
}
impl ::std::str::FromStr for Invocation3ComparisonStepResultVerdict {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "pass" => Ok(Self::Pass),
            "fail" => Ok(Self::Fail),
            "indeterminate" => Ok(Self::Indeterminate),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation3ComparisonStepResultVerdict {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Invocation3ComparisonStepResultVerdict {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///One closed installation intent for core update/repair/rollback and store migrate/rollback. Security S9.2 admits exact per-operation closure/schema/store/deadline semantics and journals the derived namespace lease set. Store operations keep the core closure; a same-schema core operation keeps the store. Target trust/profile/generation/time observations are host-admitted, never caller granted.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation3CoreTransitionIntentV1 {
    #[serde(rename = "fromCoreClosure")]
    pub from_core_closure: Common3ClosureId,
    #[serde(rename = "fromStateSchema")]
    pub from_state_schema: ExactInteger,
    #[serde(rename = "fromStoreGeneration")]
    pub from_store_generation: u64,
    pub operation: Invocation3CoreTransitionIntentV1Operation,
    #[serde(rename = "platformProfileSetBodyDigest")]
    pub platform_profile_set_body_digest: Common3Sha256Hex,
    #[serde(rename = "preconditionGeneration")]
    pub precondition_generation: u64,
    #[serde(
        rename = "rollbackDeadline",
        deserialize_with = "::std::option::Option::deserialize"
    )]
    pub rollback_deadline: ::std::option::Option<Common3UtcTimestamp>,
    #[serde(rename = "schemaVersion")]
    pub schema_version: ExactInteger,
    #[serde(rename = "toCoreClosure")]
    pub to_core_closure: Common3ClosureId,
    #[serde(rename = "toStateSchema")]
    pub to_state_schema: ExactInteger,
    #[serde(rename = "toStoreGeneration")]
    pub to_store_generation: u64,
}
///`Invocation3CoreTransitionIntentV1Operation`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation3CoreTransitionIntentV1Operation {
    #[serde(rename = "core-update")]
    CoreUpdate,
    #[serde(rename = "core-repair")]
    CoreRepair,
    #[serde(rename = "core-rollback")]
    CoreRollback,
    #[serde(rename = "store-migrate")]
    StoreMigrate,
    #[serde(rename = "store-rollback")]
    StoreRollback,
}
impl ::std::fmt::Display for Invocation3CoreTransitionIntentV1Operation {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::CoreUpdate => f.write_str("core-update"),
            Self::CoreRepair => f.write_str("core-repair"),
            Self::CoreRollback => f.write_str("core-rollback"),
            Self::StoreMigrate => f.write_str("store-migrate"),
            Self::StoreRollback => f.write_str("store-rollback"),
        }
    }
}
impl ::std::str::FromStr for Invocation3CoreTransitionIntentV1Operation {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "core-update" => Ok(Self::CoreUpdate),
            "core-repair" => Ok(Self::CoreRepair),
            "core-rollback" => Ok(Self::CoreRollback),
            "store-migrate" => Ok(Self::StoreMigrate),
            "store-rollback" => Ok(Self::StoreRollback),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation3CoreTransitionIntentV1Operation {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Invocation3CoreTransitionIntentV1Operation {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Explicit mapping from one analysis/verify attempt to its derivation DAG. The workflow step DAG (≤64 steps) and the derivation DAG (≤1024 stages) are distinct: a step never depends on a stage and a stage never references a step. One attempt owns exactly one execution plan; a retry attempt on identical admitted inputs may bind the same exec-plan2 and Run.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation3DerivationBinding {
    #[serde(rename = "executionPlanId")]
    pub execution_plan_id: Common3ExecutionPlanId,
    #[serde(
        rename = "firstFailedStage",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub first_failed_stage: FieldPresence<::std::option::Option<Common3StageOrdinal>>,
    #[serde(rename = "planId")]
    pub plan_id: Common3PlanId,
    #[serde(rename = "stageCount")]
    pub stage_count: ::std::num::NonZeroU64,
    #[serde(rename = "stagesCompleted")]
    pub stages_completed: i64,
}
///recommend [--emit-config-proposal PATH].
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation3DiscoveryRecommendRequestV1 {
    #[serde(
        rename = "emitConfigProposalPath",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub emit_config_proposal_path: FieldPresence<
        ::std::option::Option<Common3UserInputPath>,
    >,
    pub operation: ::serde_json::Value,
}
///`Invocation3DoctorParams`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation3DoctorParams {
    pub checks: ::std::vec::Vec<Invocation3DoctorParamsChecksItem>,
    pub kind: ::serde_json::Value,
}
///`Invocation3DoctorParamsChecksItem`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation3DoctorParamsChecksItem {
    #[serde(rename = "closures")]
    Closures,
    #[serde(rename = "trust")]
    Trust,
    #[serde(rename = "store")]
    Store,
    #[serde(rename = "platform")]
    Platform,
    #[serde(rename = "project-marker")]
    ProjectMarker,
    #[serde(rename = "offline-window")]
    OfflineWindow,
}
impl ::std::fmt::Display for Invocation3DoctorParamsChecksItem {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Closures => f.write_str("closures"),
            Self::Trust => f.write_str("trust"),
            Self::Store => f.write_str("store"),
            Self::Platform => f.write_str("platform"),
            Self::ProjectMarker => f.write_str("project-marker"),
            Self::OfflineWindow => f.write_str("offline-window"),
        }
    }
}
impl ::std::str::FromStr for Invocation3DoctorParamsChecksItem {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "closures" => Ok(Self::Closures),
            "trust" => Ok(Self::Trust),
            "store" => Ok(Self::Store),
            "platform" => Ok(Self::Platform),
            "project-marker" => Ok(Self::ProjectMarker),
            "offline-window" => Ok(Self::OfflineWindow),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation3DoctorParamsChecksItem {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Invocation3DoctorParamsChecksItem {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Invocation3DoctorResult`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation3DoctorResult {
    pub defects: ::std::vec::Vec<Common3DomainDetail>,
    #[serde(rename = "defectsFound")]
    pub defects_found: Common3Uint53,
    pub kind: ::serde_json::Value,
    #[serde(rename = "reportProduced")]
    pub report_produced: bool,
}
///`Invocation3ExportDeliveryParams`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation3ExportDeliveryParams {
    pub kind: ::serde_json::Value,
    ///optional egress failure never changes a local verdict (success); explicitly required delivery failure is operational-failed
    pub required: bool,
    pub sink: Common3CanonicalIdentifier,
    #[serde(rename = "sourceStep")]
    pub source_step: Common3StepId,
}
///`Invocation3ExportDeliveryResult`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation3ExportDeliveryResult {
    pub delivered: bool,
    pub kind: ::serde_json::Value,
}
///Closed host-only query-step operations for query-class CLI commands whose request has no member of the public graph-query:3 Operation/Params API. Never members of that public Operation enum and never public query operations.
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation3HostQueryOperation {
    #[serde(rename = "baseline.inspect")]
    BaselineInspect,
    #[serde(rename = "discovery.recommend")]
    DiscoveryRecommend,
    #[serde(rename = "policy.show")]
    PolicyShow,
    #[serde(rename = "policy.test")]
    PolicyTest,
    #[serde(rename = "review.produce-brief")]
    ReviewProduceBrief,
}
impl ::std::fmt::Display for Invocation3HostQueryOperation {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::BaselineInspect => f.write_str("baseline.inspect"),
            Self::DiscoveryRecommend => f.write_str("discovery.recommend"),
            Self::PolicyShow => f.write_str("policy.show"),
            Self::PolicyTest => f.write_str("policy.test"),
            Self::ReviewProduceBrief => f.write_str("review.produce-brief"),
        }
    }
}
impl ::std::str::FromStr for Invocation3HostQueryOperation {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "baseline.inspect" => Ok(Self::BaselineInspect),
            "discovery.recommend" => Ok(Self::DiscoveryRecommend),
            "policy.show" => Ok(Self::PolicyShow),
            "policy.test" => Ok(Self::PolicyTest),
            "review.produce-brief" => Ok(Self::ReviewProduceBrief),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation3HostQueryOperation {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Invocation3HostQueryOperation {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///A query step over one closed host-only operation; request is the closed record of exactly that operation.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation3HostQueryParams {
    pub kind: ::serde_json::Value,
    pub operation: Invocation3HostQueryOperation,
    pub request: Invocation3HostQueryParamsRequest,
}
///`Invocation3HostQueryParamsRequest`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(untagged)]
pub enum Invocation3HostQueryParamsRequest {
    BaselineInspectRequestV1(Invocation3BaselineInspectRequestV1),
    DiscoveryRecommendRequestV1(Invocation3DiscoveryRecommendRequestV1),
    PolicyShowRequestV1(Invocation3PolicyShowRequestV1),
    PolicyTestRequestV1(Invocation3PolicyTestRequestV1),
    ReviewBriefProduceRequestV1(Invocation3ReviewBriefProduceRequestV1),
}
impl ::std::convert::From<Invocation3BaselineInspectRequestV1>
for Invocation3HostQueryParamsRequest {
    fn from(value: Invocation3BaselineInspectRequestV1) -> Self {
        Self::BaselineInspectRequestV1(value)
    }
}
impl ::std::convert::From<Invocation3DiscoveryRecommendRequestV1>
for Invocation3HostQueryParamsRequest {
    fn from(value: Invocation3DiscoveryRecommendRequestV1) -> Self {
        Self::DiscoveryRecommendRequestV1(value)
    }
}
impl ::std::convert::From<Invocation3PolicyShowRequestV1>
for Invocation3HostQueryParamsRequest {
    fn from(value: Invocation3PolicyShowRequestV1) -> Self {
        Self::PolicyShowRequestV1(value)
    }
}
impl ::std::convert::From<Invocation3PolicyTestRequestV1>
for Invocation3HostQueryParamsRequest {
    fn from(value: Invocation3PolicyTestRequestV1) -> Self {
        Self::PolicyTestRequestV1(value)
    }
}
impl ::std::convert::From<Invocation3ReviewBriefProduceRequestV1>
for Invocation3HostQueryParamsRequest {
    fn from(value: Invocation3ReviewBriefProduceRequestV1) -> Self {
        Self::ReviewBriefProduceRequestV1(value)
    }
}
///`Invocation3ImportParams`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation3ImportParams {
    pub correspondence: Common3SourceCorrespondence,
    #[serde(rename = "evidenceKind")]
    pub evidence_kind: Imported1ImportKind,
    pub kind: ::serde_json::Value,
    pub path: Common3UserInputPath,
}
///`Invocation3ImportResult`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation3ImportResult {
    #[serde(rename = "importId")]
    pub import_id: Common3ImportId,
    pub kind: ::serde_json::Value,
    #[serde(rename = "payloadDigest")]
    pub payload_digest: Common3Sha256Hex,
    #[serde(rename = "receiptId")]
    pub receipt_id: Common3ReceiptId,
    pub staleness: Imported1Staleness,
}
///`Invocation3Mode`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation3Mode {
    pub ci: bool,
    ///true only with explicit --ephemeral; a non-authoritative invocation cannot supply baseline/repair prerequisites
    pub ephemeral: bool,
    pub interactive: bool,
}
///`Invocation3MutationParams`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation3MutationParams {
    ///Bare H("workflow.mutation-intent", MutationReplayScopeV1) binding this host-minted requestId, stepId, projectId and mutationClass as operation. The exact scope and admitted immutable step parameters are retained and checked before receipt lookup. Equal COMPLETED replay performs no second effect; separate fresh requests have different keys. Repair apply has a separate step/recipe.
    #[serde(rename = "idempotencyKey")]
    pub idempotency_key: Common3Sha256Hex,
    ///Retained closed operation-specific input: CoreTransitionIntentV1 for installation operations; RepairRecoveryIntentV1 for repair-recover.
    #[serde(
        rename = "inputDescriptorDigest",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub input_descriptor_digest: FieldPresence<::std::option::Option<Common3Sha256Hex>>,
    pub kind: ::serde_json::Value,
    #[serde(rename = "mutationClass")]
    pub mutation_class: Invocation3MutationParamsMutationClass,
    #[serde(
        rename = "sourceStep",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub source_step: FieldPresence<::std::option::Option<Common3StepId>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub target: FieldPresence<::std::option::Option<Common3UserInputPath>>,
}
///`Invocation3MutationParamsMutationClass`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation3MutationParamsMutationClass {
    #[serde(rename = "repair-apply")]
    RepairApply,
    #[serde(rename = "repair-recover")]
    RepairRecover,
    #[serde(rename = "baseline-adopt")]
    BaselineAdopt,
    #[serde(rename = "baseline-upgrade-apply")]
    BaselineUpgradeApply,
    #[serde(rename = "baseline-export")]
    BaselineExport,
    #[serde(rename = "waiver-change")]
    WaiverChange,
    #[serde(rename = "policy-write")]
    PolicyWrite,
    #[serde(rename = "config-write")]
    ConfigWrite,
    #[serde(rename = "purge")]
    Purge,
    #[serde(rename = "install")]
    Install,
    #[serde(rename = "update")]
    Update,
    #[serde(rename = "review-join")]
    ReviewJoin,
    #[serde(rename = "import")]
    Import,
    #[serde(rename = "trust-refresh")]
    TrustRefresh,
    #[serde(rename = "trust-import")]
    TrustImport,
    #[serde(rename = "trust-recovery-challenge")]
    TrustRecoveryChallenge,
    #[serde(rename = "trust-recovery-import")]
    TrustRecoveryImport,
    #[serde(rename = "store-migrate")]
    StoreMigrate,
    #[serde(rename = "store-rollback")]
    StoreRollback,
    #[serde(rename = "store-gc")]
    StoreGc,
    #[serde(rename = "core-update")]
    CoreUpdate,
    #[serde(rename = "core-repair")]
    CoreRepair,
    #[serde(rename = "core-rollback")]
    CoreRollback,
    #[serde(rename = "native-preparation")]
    NativePreparation,
}
impl ::std::fmt::Display for Invocation3MutationParamsMutationClass {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::RepairApply => f.write_str("repair-apply"),
            Self::RepairRecover => f.write_str("repair-recover"),
            Self::BaselineAdopt => f.write_str("baseline-adopt"),
            Self::BaselineUpgradeApply => f.write_str("baseline-upgrade-apply"),
            Self::BaselineExport => f.write_str("baseline-export"),
            Self::WaiverChange => f.write_str("waiver-change"),
            Self::PolicyWrite => f.write_str("policy-write"),
            Self::ConfigWrite => f.write_str("config-write"),
            Self::Purge => f.write_str("purge"),
            Self::Install => f.write_str("install"),
            Self::Update => f.write_str("update"),
            Self::ReviewJoin => f.write_str("review-join"),
            Self::Import => f.write_str("import"),
            Self::TrustRefresh => f.write_str("trust-refresh"),
            Self::TrustImport => f.write_str("trust-import"),
            Self::TrustRecoveryChallenge => f.write_str("trust-recovery-challenge"),
            Self::TrustRecoveryImport => f.write_str("trust-recovery-import"),
            Self::StoreMigrate => f.write_str("store-migrate"),
            Self::StoreRollback => f.write_str("store-rollback"),
            Self::StoreGc => f.write_str("store-gc"),
            Self::CoreUpdate => f.write_str("core-update"),
            Self::CoreRepair => f.write_str("core-repair"),
            Self::CoreRollback => f.write_str("core-rollback"),
            Self::NativePreparation => f.write_str("native-preparation"),
        }
    }
}
impl ::std::str::FromStr for Invocation3MutationParamsMutationClass {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "repair-apply" => Ok(Self::RepairApply),
            "repair-recover" => Ok(Self::RepairRecover),
            "baseline-adopt" => Ok(Self::BaselineAdopt),
            "baseline-upgrade-apply" => Ok(Self::BaselineUpgradeApply),
            "baseline-export" => Ok(Self::BaselineExport),
            "waiver-change" => Ok(Self::WaiverChange),
            "policy-write" => Ok(Self::PolicyWrite),
            "config-write" => Ok(Self::ConfigWrite),
            "purge" => Ok(Self::Purge),
            "install" => Ok(Self::Install),
            "update" => Ok(Self::Update),
            "review-join" => Ok(Self::ReviewJoin),
            "import" => Ok(Self::Import),
            "trust-refresh" => Ok(Self::TrustRefresh),
            "trust-import" => Ok(Self::TrustImport),
            "trust-recovery-challenge" => Ok(Self::TrustRecoveryChallenge),
            "trust-recovery-import" => Ok(Self::TrustRecoveryImport),
            "store-migrate" => Ok(Self::StoreMigrate),
            "store-rollback" => Ok(Self::StoreRollback),
            "store-gc" => Ok(Self::StoreGc),
            "core-update" => Ok(Self::CoreUpdate),
            "core-repair" => Ok(Self::CoreRepair),
            "core-rollback" => Ok(Self::CoreRollback),
            "native-preparation" => Ok(Self::NativePreparation),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation3MutationParamsMutationClass {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Invocation3MutationParamsMutationClass {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Retained operational replay namespace for a generic mutation. H(workflow.mutation-intent, this complete record) is its idempotencyKey. The admitted immutable invocation and step own effect inputs; a key grants no authority and never deduplicates different fresh requests. Repair apply uses its separate exact content-derived recipe.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation3MutationReplayScopeV1 {
    pub operation: Repair2MutationOperation,
    #[serde(rename = "projectId")]
    pub project_id: Common3ProjectId,
    #[serde(rename = "requestId")]
    pub request_id: Common3RequestId,
    #[serde(rename = "schemaVersion")]
    pub schema_version: ExactInteger,
    #[serde(rename = "stepId")]
    pub step_id: Common3StepId,
}
///`Invocation3MutationResult`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation3MutationResult {
    #[serde(rename = "effectOutcome")]
    pub effect_outcome: Invocation3MutationResultEffectOutcome,
    pub kind: ::serde_json::Value,
    #[serde(rename = "receiptId")]
    pub receipt_id: Common3ReceiptId,
    pub replayed: bool,
}
///`Invocation3MutationResultEffectOutcome`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation3MutationResultEffectOutcome {
    #[serde(rename = "COMPLETED")]
    Completed,
    #[serde(rename = "FAILED")]
    Failed,
    #[serde(rename = "INDETERMINATE")]
    Indeterminate,
}
impl ::std::fmt::Display for Invocation3MutationResultEffectOutcome {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Completed => f.write_str("COMPLETED"),
            Self::Failed => f.write_str("FAILED"),
            Self::Indeterminate => f.write_str("INDETERMINATE"),
        }
    }
}
impl ::std::str::FromStr for Invocation3MutationResultEffectOutcome {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "COMPLETED" => Ok(Self::Completed),
            "FAILED" => Ok(Self::Failed),
            "INDETERMINATE" => Ok(Self::Indeterminate),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation3MutationResultEffectOutcome {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Invocation3MutationResultEffectOutcome {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Digest is raw SHA-256 of canonical retained native AuthorizedExecutionV2. The host verifies that preimage and its grant-set reference, then composes security admission for every owner before spawning. No Run; no automatic retry.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation3NativePreparationParams {
    #[serde(rename = "authorizationDescriptorDigest")]
    pub authorization_descriptor_digest: Common3Sha256Hex,
    pub kind: ::serde_json::Value,
    #[serde(rename = "securityGrantSetRef")]
    pub security_grant_set_ref: ::std::string::String,
}
///Completed preparation only: explicit execution receipt and admitted prepared import. Faults use step termination/journal, never this success record.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation3NativePreparationResult {
    #[serde(rename = "importId")]
    pub import_id: Common3ImportId,
    pub kind: ::serde_json::Value,
    #[serde(rename = "ownerCount")]
    pub owner_count: i64,
    #[serde(rename = "receiptId")]
    pub receipt_id: Common3ReceiptId,
}
///policy show: tracked policy and waiver documents resolved at the admitted trust-clock date (host observation, not a request field).
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation3PolicyShowRequestV1 {
    pub operation: ::serde_json::Value,
}
///policy test SUITE: suitePath names an evaluator3 PolicyTestSuiteV2 document (urn:opensip:product-v1:workflows:evaluator3:policy-test:2); a suite or candidate policy of another major is refused before evaluation.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation3PolicyTestRequestV1 {
    pub operation: ::serde_json::Value,
    #[serde(rename = "suitePath")]
    pub suite_path: Common3UserInputPath,
}
///A query step over one of the twenty public graph-query:3 operations; request is the complete admitted GraphQueryRequestV1 whose operation, completeness and page equal the step fields (cross-field join).
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation3PublicQueryParams {
    pub completeness: Invocation3PublicQueryParamsCompleteness,
    pub kind: ::serde_json::Value,
    pub operation: Graph3Operation,
    pub page: Graph3Page,
    pub request: Graph3GraphQueryRequestV1,
}
///`Invocation3PublicQueryParamsCompleteness`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation3PublicQueryParamsCompleteness {
    #[serde(rename = "required")]
    Required,
    #[serde(rename = "best-effort")]
    BestEffort,
}
impl ::std::fmt::Display for Invocation3PublicQueryParamsCompleteness {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Required => f.write_str("required"),
            Self::BestEffort => f.write_str("best-effort"),
        }
    }
}
impl ::std::str::FromStr for Invocation3PublicQueryParamsCompleteness {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "required" => Ok(Self::Required),
            "best-effort" => Ok(Self::BestEffort),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation3PublicQueryParamsCompleteness {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Invocation3PublicQueryParamsCompleteness {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Closed query-step params: public graph-query:3 operations or the closed host-only extension. The command->operation mapping is command-inventory:3 queryDispatch.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(untagged)]
pub enum Invocation3QueryParams {
    PublicQueryParams(Invocation3PublicQueryParams),
    HostQueryParams(Invocation3HostQueryParams),
}
impl ::std::convert::From<Invocation3PublicQueryParams> for Invocation3QueryParams {
    fn from(value: Invocation3PublicQueryParams) -> Self {
        Self::PublicQueryParams(value)
    }
}
impl ::std::convert::From<Invocation3HostQueryParams> for Invocation3QueryParams {
    fn from(value: Invocation3HostQueryParams) -> Self {
        Self::HostQueryParams(value)
    }
}
///`Invocation3QueryResult`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation3QueryResult {
    pub advisory: bool,
    #[serde(rename = "completenessMet")]
    pub completeness_met: bool,
    pub items: Common3Uint53,
    pub kind: ::serde_json::Value,
    #[serde(
        rename = "nextCursor",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub next_cursor: FieldPresence<
        ::std::option::Option<Invocation3QueryResultNextCursor>,
    >,
    pub truncated: bool,
}
///`Invocation3QueryResultNextCursor`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Invocation3QueryResultNextCursor(::std::string::String);
impl ::std::ops::Deref for Invocation3QueryResultNextCursor {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Invocation3QueryResultNextCursor> for ::std::string::String {
    fn from(value: Invocation3QueryResultNextCursor) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Invocation3QueryResultNextCursor {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 256usize {
            return Err("longer than 256 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Invocation3QueryResultNextCursor {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Invocation3QueryResultNextCursor {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Invocation3QueryResultNextCursor {
    fn deserialize<D>(deserializer: D) -> ::std::result::Result<Self, D::Error>
    where
        D: ::serde::Deserializer<'de>,
    {
        ::std::string::String::deserialize(deserializer)?
            .parse()
            .map_err(|e: self::error::ConversionError| {
                <D::Error as ::serde::de::Error>::custom(e.to_string())
            })
    }
}
///`Invocation3RenderParams`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation3RenderParams {
    pub destination: Invocation3RenderParamsDestination,
    pub format: Inventory3OutputFormat,
    pub kind: ::serde_json::Value,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub path: FieldPresence<::std::option::Option<Common3UserInputPath>>,
    ///true for the selected primary renderer: its failure after a committed Run is DELIVERY.REQUIRED_FAILED (exit 4) and never rewrites the Run
    pub required: bool,
    #[serde(rename = "sourceSteps")]
    pub source_steps: ::std::vec::Vec<Common3StepId>,
}
///`Invocation3RenderParamsDestination`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation3RenderParamsDestination {
    #[serde(rename = "stdout")]
    Stdout,
    #[serde(rename = "file")]
    File,
}
impl ::std::fmt::Display for Invocation3RenderParamsDestination {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Stdout => f.write_str("stdout"),
            Self::File => f.write_str("file"),
        }
    }
}
impl ::std::str::FromStr for Invocation3RenderParamsDestination {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "stdout" => Ok(Self::Stdout),
            "file" => Ok(Self::File),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation3RenderParamsDestination {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Invocation3RenderParamsDestination {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Invocation3RenderResult`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation3RenderResult {
    pub bytes: Common3Uint53,
    pub format: Inventory3OutputFormat,
    pub kind: ::serde_json::Value,
    #[serde(rename = "rendererVersion")]
    pub renderer_version: ::std::num::NonZeroU64,
    pub truncation: bool,
    pub written: bool,
}
///`Invocation3RepairApplyParams`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation3RepairApplyParams {
    #[serde(rename = "authorizationRef")]
    pub authorization_ref: Common3RepairAuthorizationRef,
    #[serde(rename = "consentSource")]
    pub consent_source: Invocation3RepairApplyParamsConsentSource,
    pub kind: ::serde_json::Value,
    #[serde(rename = "planStep")]
    pub plan_step: Common3StepId,
    ///must equal the plan step's result; apply is bound to the exact plan identity, not to the step
    #[serde(rename = "repairPlanId")]
    pub repair_plan_id: Common3RepairPlanId,
}
///`Invocation3RepairApplyParamsConsentSource`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation3RepairApplyParamsConsentSource {
    #[serde(rename = "policy")]
    Policy,
    #[serde(rename = "interactive")]
    Interactive,
}
impl ::std::fmt::Display for Invocation3RepairApplyParamsConsentSource {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Policy => f.write_str("policy"),
            Self::Interactive => f.write_str("interactive"),
        }
    }
}
impl ::std::str::FromStr for Invocation3RepairApplyParamsConsentSource {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "policy" => Ok(Self::Policy),
            "interactive" => Ok(Self::Interactive),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation3RepairApplyParamsConsentSource {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Invocation3RepairApplyParamsConsentSource {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Invocation3RepairApplyResult`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation3RepairApplyResult {
    #[serde(
        rename = "appliedSnapshotId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub applied_snapshot_id: FieldPresence<::std::option::Option<Common3SnapshotId>>,
    #[serde(rename = "effectOutcome")]
    pub effect_outcome: Invocation3RepairApplyResultEffectOutcome,
    #[serde(rename = "journalState")]
    pub journal_state: Repair2JournalState,
    pub kind: ::serde_json::Value,
    #[serde(rename = "receiptId")]
    pub receipt_id: Common3ReceiptId,
    pub rollback: Invocation3RepairApplyResultRollback,
}
///`Invocation3RepairApplyResultEffectOutcome`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation3RepairApplyResultEffectOutcome {
    #[serde(rename = "COMPLETED")]
    Completed,
    #[serde(rename = "FAILED")]
    Failed,
    #[serde(rename = "INDETERMINATE")]
    Indeterminate,
}
impl ::std::fmt::Display for Invocation3RepairApplyResultEffectOutcome {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Completed => f.write_str("COMPLETED"),
            Self::Failed => f.write_str("FAILED"),
            Self::Indeterminate => f.write_str("INDETERMINATE"),
        }
    }
}
impl ::std::str::FromStr for Invocation3RepairApplyResultEffectOutcome {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "COMPLETED" => Ok(Self::Completed),
            "FAILED" => Ok(Self::Failed),
            "INDETERMINATE" => Ok(Self::Indeterminate),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation3RepairApplyResultEffectOutcome {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Invocation3RepairApplyResultEffectOutcome {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Invocation3RepairApplyResultRollback`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation3RepairApplyResultRollback {
    #[serde(rename = "not-needed")]
    NotNeeded,
    #[serde(rename = "completed")]
    Completed,
    #[serde(rename = "blocked")]
    Blocked,
    #[serde(rename = "not-attempted")]
    NotAttempted,
}
impl ::std::fmt::Display for Invocation3RepairApplyResultRollback {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::NotNeeded => f.write_str("not-needed"),
            Self::Completed => f.write_str("completed"),
            Self::Blocked => f.write_str("blocked"),
            Self::NotAttempted => f.write_str("not-attempted"),
        }
    }
}
impl ::std::str::FromStr for Invocation3RepairApplyResultRollback {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "not-needed" => Ok(Self::NotNeeded),
            "completed" => Ok(Self::Completed),
            "blocked" => Ok(Self::Blocked),
            "not-attempted" => Ok(Self::NotAttempted),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation3RepairApplyResultRollback {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Invocation3RepairApplyResultRollback {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Invocation3RepairPreviewParams`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation3RepairPreviewParams {
    #[serde(rename = "evidenceSource")]
    pub evidence_source: Invocation3RepairPreviewParamsEvidenceSource,
    pub kind: ::serde_json::Value,
    pub recipe: Repair2RecipeRef,
    pub targets: ::std::vec::Vec<Common3Fingerprint>,
}
///`Invocation3RepairPreviewParamsEvidenceSource`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
pub enum Invocation3RepairPreviewParamsEvidenceSource {
    #[serde(rename = "step")]
    Step(Common3StepId),
    #[serde(rename = "runId")]
    RunId(Common3RunId),
}
impl ::std::convert::From<Common3StepId>
for Invocation3RepairPreviewParamsEvidenceSource {
    fn from(value: Common3StepId) -> Self {
        Self::Step(value)
    }
}
impl ::std::convert::From<Common3RunId>
for Invocation3RepairPreviewParamsEvidenceSource {
    fn from(value: Common3RunId) -> Self {
        Self::RunId(value)
    }
}
///`Invocation3RepairPreviewResult`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation3RepairPreviewResult {
    pub applicable: bool,
    pub kind: ::serde_json::Value,
    #[serde(rename = "repairPlanId")]
    pub repair_plan_id: Common3RepairPlanId,
    #[serde(rename = "snapshotId")]
    pub snapshot_id: Common3SnapshotId,
    #[serde(rename = "unmetPreconditions")]
    pub unmet_preconditions: ::std::vec::Vec<Common3DomainDetail>,
}
///Host-created after reading the exact apply journal and obtaining fresh security recovery admission. It binds the mutation step inputDescriptorDigest. All fields join the admitted authorization; inspection uses the query step and needs no authorization.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation3RepairRecoveryIntentV1 {
    #[serde(rename = "authorizationRef")]
    pub authorization_ref: Common3RepairRecoveryAuthorizationRef,
    #[serde(rename = "journalRef")]
    pub journal_ref: Common3RepairJournalRef,
    pub kind: ::serde_json::Value,
    #[serde(rename = "recoveryAction")]
    pub recovery_action: Invocation3RepairRecoveryIntentV1RecoveryAction,
    #[serde(rename = "repairPlanId")]
    pub repair_plan_id: Common3RepairPlanId,
    #[serde(rename = "schemaVersion")]
    pub schema_version: ExactInteger,
}
///`Invocation3RepairRecoveryIntentV1RecoveryAction`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation3RepairRecoveryIntentV1RecoveryAction {
    #[serde(rename = "discard-temps")]
    DiscardTemps,
    #[serde(rename = "roll-back-renamed")]
    RollBackRenamed,
    #[serde(rename = "verify-postimages-and-commit")]
    VerifyPostimagesAndCommit,
}
impl ::std::fmt::Display for Invocation3RepairRecoveryIntentV1RecoveryAction {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::DiscardTemps => f.write_str("discard-temps"),
            Self::RollBackRenamed => f.write_str("roll-back-renamed"),
            Self::VerifyPostimagesAndCommit => {
                f.write_str("verify-postimages-and-commit")
            }
        }
    }
}
impl ::std::str::FromStr for Invocation3RepairRecoveryIntentV1RecoveryAction {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "discard-temps" => Ok(Self::DiscardTemps),
            "roll-back-renamed" => Ok(Self::RollBackRenamed),
            "verify-postimages-and-commit" => Ok(Self::VerifyPostimagesAndCommit),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation3RepairRecoveryIntentV1RecoveryAction {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Invocation3RepairRecoveryIntentV1RecoveryAction {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Invocation3RetentionDisclosure`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation3RetentionDisclosure {
    #[serde(rename = "firstUse")]
    pub first_use: bool,
    pub policy: Invocation3RetentionDisclosurePolicy,
    pub provenance: Invocation3RetentionDisclosureProvenance,
    #[serde(rename = "storageRoot")]
    pub storage_root: Common3UserInputPath,
}
///`Invocation3RetentionDisclosurePolicy`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation3RetentionDisclosurePolicy {
    #[serde(rename = "durable-unbounded")]
    DurableUnbounded,
    #[serde(rename = "durable-bounded")]
    DurableBounded,
    #[serde(rename = "ephemeral")]
    Ephemeral,
}
impl ::std::fmt::Display for Invocation3RetentionDisclosurePolicy {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::DurableUnbounded => f.write_str("durable-unbounded"),
            Self::DurableBounded => f.write_str("durable-bounded"),
            Self::Ephemeral => f.write_str("ephemeral"),
        }
    }
}
impl ::std::str::FromStr for Invocation3RetentionDisclosurePolicy {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "durable-unbounded" => Ok(Self::DurableUnbounded),
            "durable-bounded" => Ok(Self::DurableBounded),
            "ephemeral" => Ok(Self::Ephemeral),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation3RetentionDisclosurePolicy {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Invocation3RetentionDisclosurePolicy {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Invocation3RetentionDisclosureProvenance`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation3RetentionDisclosureProvenance {
    #[serde(rename = "DEFAULTED")]
    Defaulted,
    #[serde(rename = "CONFIGURED")]
    Configured,
    #[serde(rename = "EXPLICIT-FLAG")]
    ExplicitFlag,
}
impl ::std::fmt::Display for Invocation3RetentionDisclosureProvenance {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Defaulted => f.write_str("DEFAULTED"),
            Self::Configured => f.write_str("CONFIGURED"),
            Self::ExplicitFlag => f.write_str("EXPLICIT-FLAG"),
        }
    }
}
impl ::std::str::FromStr for Invocation3RetentionDisclosureProvenance {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "DEFAULTED" => Ok(Self::Defaulted),
            "CONFIGURED" => Ok(Self::Configured),
            "EXPLICIT-FLAG" => Ok(Self::ExplicitFlag),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation3RetentionDisclosureProvenance {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Invocation3RetentionDisclosureProvenance {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///review brief [--producer model|heuristic]: model selects a ReviewerPrincipal of kind model with its admitted modelClosureId; heuristic selects kind policy-rule with id opensip.review.heuristic.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation3ReviewBriefProduceRequestV1 {
    pub operation: ::serde_json::Value,
    pub producer: Review2ReviewerPrincipal,
    pub view: Graph3View,
}
///Operational identity remains RequestId. Analysis/verify attempts seal run3 (not run2). Derivation DAG remains exec-plan2. schemaMajor 3 because AnalysisResult.runId pattern changed. Mixed run2/run3 graphs refuse.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation3Root {
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub cancellation: FieldPresence<::std::option::Option<Invocation3Cancellation>>,
    #[serde(
        rename = "clientCorrelationId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub client_correlation_id: FieldPresence<
        ::std::option::Option<Invocation3RootClientCorrelationId>,
    >,
    pub mode: Invocation3Mode,
    #[serde(rename = "orderedSteps")]
    pub ordered_steps: ::std::vec::Vec<Invocation3StepSpec>,
    #[serde(
        rename = "projectId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub project_id: FieldPresence<::std::option::Option<Common3ProjectId>>,
    #[serde(rename = "requestId")]
    pub request_id: Common3RequestId,
    #[serde(
        rename = "retentionDisclosure",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub retention_disclosure: FieldPresence<
        ::std::option::Option<Invocation3RetentionDisclosure>,
    >,
    #[serde(rename = "schemaFamily")]
    pub schema_family: ::serde_json::Value,
    #[serde(rename = "schemaMajor")]
    pub schema_major: ExactInteger,
    #[serde(
        rename = "stepResults",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub step_results: FieldPresence<::std::vec::Vec<Invocation3StepResult>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub termination: FieldPresence<::std::option::Option<Common3StepTermination>>,
    #[serde(
        rename = "terminationEmitted",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub termination_emitted: FieldPresence<::std::option::Option<bool>>,
    pub workflow: Invocation3WorkflowRef,
}
///`Invocation3RootClientCorrelationId`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Invocation3RootClientCorrelationId(::std::string::String);
impl ::std::ops::Deref for Invocation3RootClientCorrelationId {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Invocation3RootClientCorrelationId> for ::std::string::String {
    fn from(value: Invocation3RootClientCorrelationId) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Invocation3RootClientCorrelationId {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 128usize {
            return Err("longer than 128 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Invocation3RootClientCorrelationId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Invocation3RootClientCorrelationId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Invocation3RootClientCorrelationId {
    fn deserialize<D>(deserializer: D) -> ::std::result::Result<Self, D::Error>
    where
        D: ::serde::Deserializer<'de>,
    {
        ::std::string::String::deserialize(deserializer)?
            .parse()
            .map_err(|e: self::error::ConversionError| {
                <D::Error as ::serde::de::Error>::custom(e.to_string())
            })
    }
}
///`Invocation3StepDomainResult`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(untagged)]
pub enum Invocation3StepDomainResult {
    AnalysisResult(Invocation3AnalysisResult),
    ComparisonStepResult(Invocation3ComparisonStepResult),
    QueryResult(Invocation3QueryResult),
    RenderResult(Invocation3RenderResult),
    ImportResult(Invocation3ImportResult),
    RepairPreviewResult(Invocation3RepairPreviewResult),
    RepairApplyResult(Invocation3RepairApplyResult),
    TestExecutionResult(Invocation3TestExecutionResult),
    MutationResult(Invocation3MutationResult),
    ExportDeliveryResult(Invocation3ExportDeliveryResult),
    DoctorResult(Invocation3DoctorResult),
    NativePreparationResult(Invocation3NativePreparationResult),
}
impl ::std::convert::From<Invocation3AnalysisResult> for Invocation3StepDomainResult {
    fn from(value: Invocation3AnalysisResult) -> Self {
        Self::AnalysisResult(value)
    }
}
impl ::std::convert::From<Invocation3ComparisonStepResult>
for Invocation3StepDomainResult {
    fn from(value: Invocation3ComparisonStepResult) -> Self {
        Self::ComparisonStepResult(value)
    }
}
impl ::std::convert::From<Invocation3QueryResult> for Invocation3StepDomainResult {
    fn from(value: Invocation3QueryResult) -> Self {
        Self::QueryResult(value)
    }
}
impl ::std::convert::From<Invocation3RenderResult> for Invocation3StepDomainResult {
    fn from(value: Invocation3RenderResult) -> Self {
        Self::RenderResult(value)
    }
}
impl ::std::convert::From<Invocation3ImportResult> for Invocation3StepDomainResult {
    fn from(value: Invocation3ImportResult) -> Self {
        Self::ImportResult(value)
    }
}
impl ::std::convert::From<Invocation3RepairPreviewResult>
for Invocation3StepDomainResult {
    fn from(value: Invocation3RepairPreviewResult) -> Self {
        Self::RepairPreviewResult(value)
    }
}
impl ::std::convert::From<Invocation3RepairApplyResult> for Invocation3StepDomainResult {
    fn from(value: Invocation3RepairApplyResult) -> Self {
        Self::RepairApplyResult(value)
    }
}
impl ::std::convert::From<Invocation3TestExecutionResult>
for Invocation3StepDomainResult {
    fn from(value: Invocation3TestExecutionResult) -> Self {
        Self::TestExecutionResult(value)
    }
}
impl ::std::convert::From<Invocation3MutationResult> for Invocation3StepDomainResult {
    fn from(value: Invocation3MutationResult) -> Self {
        Self::MutationResult(value)
    }
}
impl ::std::convert::From<Invocation3ExportDeliveryResult>
for Invocation3StepDomainResult {
    fn from(value: Invocation3ExportDeliveryResult) -> Self {
        Self::ExportDeliveryResult(value)
    }
}
impl ::std::convert::From<Invocation3DoctorResult> for Invocation3StepDomainResult {
    fn from(value: Invocation3DoctorResult) -> Self {
        Self::DoctorResult(value)
    }
}
impl ::std::convert::From<Invocation3NativePreparationResult>
for Invocation3StepDomainResult {
    fn from(value: Invocation3NativePreparationResult) -> Self {
        Self::NativePreparationResult(value)
    }
}
///comparison: the audit verdict step. It consumes the current analysis Run (currentStep) and a baseline artifact, mints no Run, and is the ONLY step whose verdict gates an audit; the analysis it consumes participates in the aggregate for completion, operational faults and required-coverage indeterminacy only (verdictGate=delegated).
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation3StepKind {
    #[serde(rename = "analysis")]
    Analysis,
    #[serde(rename = "verify")]
    Verify,
    #[serde(rename = "comparison")]
    Comparison,
    #[serde(rename = "query")]
    Query,
    #[serde(rename = "render")]
    Render,
    #[serde(rename = "import")]
    Import,
    #[serde(rename = "repair-preview")]
    RepairPreview,
    #[serde(rename = "repair-apply")]
    RepairApply,
    #[serde(rename = "test-execution")]
    TestExecution,
    #[serde(rename = "mutation")]
    Mutation,
    #[serde(rename = "export-delivery")]
    ExportDelivery,
    #[serde(rename = "doctor")]
    Doctor,
    #[serde(rename = "native-preparation")]
    NativePreparation,
}
impl ::std::fmt::Display for Invocation3StepKind {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Analysis => f.write_str("analysis"),
            Self::Verify => f.write_str("verify"),
            Self::Comparison => f.write_str("comparison"),
            Self::Query => f.write_str("query"),
            Self::Render => f.write_str("render"),
            Self::Import => f.write_str("import"),
            Self::RepairPreview => f.write_str("repair-preview"),
            Self::RepairApply => f.write_str("repair-apply"),
            Self::TestExecution => f.write_str("test-execution"),
            Self::Mutation => f.write_str("mutation"),
            Self::ExportDelivery => f.write_str("export-delivery"),
            Self::Doctor => f.write_str("doctor"),
            Self::NativePreparation => f.write_str("native-preparation"),
        }
    }
}
impl ::std::str::FromStr for Invocation3StepKind {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "analysis" => Ok(Self::Analysis),
            "verify" => Ok(Self::Verify),
            "comparison" => Ok(Self::Comparison),
            "query" => Ok(Self::Query),
            "render" => Ok(Self::Render),
            "import" => Ok(Self::Import),
            "repair-preview" => Ok(Self::RepairPreview),
            "repair-apply" => Ok(Self::RepairApply),
            "test-execution" => Ok(Self::TestExecution),
            "mutation" => Ok(Self::Mutation),
            "export-delivery" => Ok(Self::ExportDelivery),
            "doctor" => Ok(Self::Doctor),
            "native-preparation" => Ok(Self::NativePreparation),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation3StepKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Invocation3StepKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///completed: the step reached its own terminal domain result (an analysis verdict of fail or indeterminate is still completed). rejected: admission or precondition refusal. failed: operational fault. skipped: a dependency did not satisfy the gate. cancelled: cancellation arrived before a terminal result. abandoned: assigned only by crash recovery to a non-terminal step whose supervisor died.
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation3StepOutcome {
    #[serde(rename = "completed")]
    Completed,
    #[serde(rename = "rejected")]
    Rejected,
    #[serde(rename = "failed")]
    Failed,
    #[serde(rename = "skipped")]
    Skipped,
    #[serde(rename = "cancelled")]
    Cancelled,
    #[serde(rename = "abandoned")]
    Abandoned,
}
impl ::std::fmt::Display for Invocation3StepOutcome {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Completed => f.write_str("completed"),
            Self::Rejected => f.write_str("rejected"),
            Self::Failed => f.write_str("failed"),
            Self::Skipped => f.write_str("skipped"),
            Self::Cancelled => f.write_str("cancelled"),
            Self::Abandoned => f.write_str("abandoned"),
        }
    }
}
impl ::std::str::FromStr for Invocation3StepOutcome {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "completed" => Ok(Self::Completed),
            "rejected" => Ok(Self::Rejected),
            "failed" => Ok(Self::Failed),
            "skipped" => Ok(Self::Skipped),
            "cancelled" => Ok(Self::Cancelled),
            "abandoned" => Ok(Self::Abandoned),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation3StepOutcome {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Invocation3StepOutcome {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Invocation3StepParams`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(untagged)]
pub enum Invocation3StepParams {
    AnalysisParams(Invocation3AnalysisParams),
    VerifyParams(Invocation3VerifyParams),
    ComparisonParams(Invocation3ComparisonParams),
    QueryParams(Invocation3QueryParams),
    RenderParams(Invocation3RenderParams),
    ImportParams(Invocation3ImportParams),
    RepairPreviewParams(Invocation3RepairPreviewParams),
    RepairApplyParams(Invocation3RepairApplyParams),
    TestExecutionParams(Invocation3TestExecutionParams),
    MutationParams(Invocation3MutationParams),
    ExportDeliveryParams(Invocation3ExportDeliveryParams),
    DoctorParams(Invocation3DoctorParams),
    NativePreparationParams(Invocation3NativePreparationParams),
}
impl ::std::convert::From<Invocation3AnalysisParams> for Invocation3StepParams {
    fn from(value: Invocation3AnalysisParams) -> Self {
        Self::AnalysisParams(value)
    }
}
impl ::std::convert::From<Invocation3VerifyParams> for Invocation3StepParams {
    fn from(value: Invocation3VerifyParams) -> Self {
        Self::VerifyParams(value)
    }
}
impl ::std::convert::From<Invocation3ComparisonParams> for Invocation3StepParams {
    fn from(value: Invocation3ComparisonParams) -> Self {
        Self::ComparisonParams(value)
    }
}
impl ::std::convert::From<Invocation3QueryParams> for Invocation3StepParams {
    fn from(value: Invocation3QueryParams) -> Self {
        Self::QueryParams(value)
    }
}
impl ::std::convert::From<Invocation3RenderParams> for Invocation3StepParams {
    fn from(value: Invocation3RenderParams) -> Self {
        Self::RenderParams(value)
    }
}
impl ::std::convert::From<Invocation3ImportParams> for Invocation3StepParams {
    fn from(value: Invocation3ImportParams) -> Self {
        Self::ImportParams(value)
    }
}
impl ::std::convert::From<Invocation3RepairPreviewParams> for Invocation3StepParams {
    fn from(value: Invocation3RepairPreviewParams) -> Self {
        Self::RepairPreviewParams(value)
    }
}
impl ::std::convert::From<Invocation3RepairApplyParams> for Invocation3StepParams {
    fn from(value: Invocation3RepairApplyParams) -> Self {
        Self::RepairApplyParams(value)
    }
}
impl ::std::convert::From<Invocation3TestExecutionParams> for Invocation3StepParams {
    fn from(value: Invocation3TestExecutionParams) -> Self {
        Self::TestExecutionParams(value)
    }
}
impl ::std::convert::From<Invocation3MutationParams> for Invocation3StepParams {
    fn from(value: Invocation3MutationParams) -> Self {
        Self::MutationParams(value)
    }
}
impl ::std::convert::From<Invocation3ExportDeliveryParams> for Invocation3StepParams {
    fn from(value: Invocation3ExportDeliveryParams) -> Self {
        Self::ExportDeliveryParams(value)
    }
}
impl ::std::convert::From<Invocation3DoctorParams> for Invocation3StepParams {
    fn from(value: Invocation3DoctorParams) -> Self {
        Self::DoctorParams(value)
    }
}
impl ::std::convert::From<Invocation3NativePreparationParams> for Invocation3StepParams {
    fn from(value: Invocation3NativePreparationParams) -> Self {
        Self::NativePreparationParams(value)
    }
}
///`Invocation3StepResult`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation3StepResult {
    pub attempts: ::std::vec::Vec<Invocation3Attempt>,
    pub outcome: Invocation3StepOutcome,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub result: FieldPresence<::std::option::Option<Invocation3StepDomainResult>>,
    #[serde(
        rename = "skipReason",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub skip_reason: FieldPresence<
        ::std::option::Option<Invocation3StepResultSkipReason>,
    >,
    #[serde(rename = "stepId")]
    pub step_id: Common3StepId,
    pub termination: Common3StepTermination,
}
///`Invocation3StepResultSkipReason`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation3StepResultSkipReason {
    #[serde(rename = "dependency-not-completed")]
    DependencyNotCompleted,
    #[serde(rename = "dependency-not-terminal")]
    DependencyNotTerminal,
    #[serde(rename = "dependency-cancelled")]
    DependencyCancelled,
}
impl ::std::fmt::Display for Invocation3StepResultSkipReason {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::DependencyNotCompleted => f.write_str("dependency-not-completed"),
            Self::DependencyNotTerminal => f.write_str("dependency-not-terminal"),
            Self::DependencyCancelled => f.write_str("dependency-cancelled"),
        }
    }
}
impl ::std::str::FromStr for Invocation3StepResultSkipReason {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "dependency-not-completed" => Ok(Self::DependencyNotCompleted),
            "dependency-not-terminal" => Ok(Self::DependencyNotTerminal),
            "dependency-cancelled" => Ok(Self::DependencyCancelled),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation3StepResultSkipReason {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Invocation3StepResultSkipReason {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Invocation3StepSpec`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation3StepSpec {
    ///completed: every dependency outcome must be completed. terminal: every dependency must have reached any terminal outcome; used only by render/export-delivery steps that project whatever happened.
    #[serde(rename = "dependencyGate")]
    pub dependency_gate: Invocation3StepSpecDependencyGate,
    ///every entry is a lower stepId (acyclic by construction; a forward or self reference is WORKFLOW.DEPENDENCY_CYCLE)
    #[serde(rename = "dependsOn")]
    pub depends_on: ::std::vec::Vec<Common3StepId>,
    pub kind: Invocation3StepKind,
    pub params: Invocation3StepParams,
    ///required steps determine the aggregate termination; an optional step's rejection/failure never changes it. A required step may not depend on an optional step (WORKFLOW.REQUIRED_DEPENDS_ON_OPTIONAL, request-rejected).
    pub requirement: Invocation3StepSpecRequirement,
    ///idempotent-retry is lawful only for analysis, verify, query, render, doctor and export-delivery and only for faultCause ledger-busy; at most 3 attempts in total. Mutation, import, repair-preview, repair-apply and test-execution are never implicitly retried.
    #[serde(rename = "retryPolicy")]
    pub retry_policy: Invocation3StepSpecRetryPolicy,
    #[serde(rename = "stepId")]
    pub step_id: Common3StepId,
}
///completed: every dependency outcome must be completed. terminal: every dependency must have reached any terminal outcome; used only by render/export-delivery steps that project whatever happened.
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation3StepSpecDependencyGate {
    #[serde(rename = "completed")]
    Completed,
    #[serde(rename = "terminal")]
    Terminal,
}
impl ::std::fmt::Display for Invocation3StepSpecDependencyGate {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Completed => f.write_str("completed"),
            Self::Terminal => f.write_str("terminal"),
        }
    }
}
impl ::std::str::FromStr for Invocation3StepSpecDependencyGate {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "completed" => Ok(Self::Completed),
            "terminal" => Ok(Self::Terminal),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation3StepSpecDependencyGate {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Invocation3StepSpecDependencyGate {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///required steps determine the aggregate termination; an optional step's rejection/failure never changes it. A required step may not depend on an optional step (WORKFLOW.REQUIRED_DEPENDS_ON_OPTIONAL, request-rejected).
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation3StepSpecRequirement {
    #[serde(rename = "required")]
    Required,
    #[serde(rename = "optional")]
    Optional,
}
impl ::std::fmt::Display for Invocation3StepSpecRequirement {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Required => f.write_str("required"),
            Self::Optional => f.write_str("optional"),
        }
    }
}
impl ::std::str::FromStr for Invocation3StepSpecRequirement {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "required" => Ok(Self::Required),
            "optional" => Ok(Self::Optional),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation3StepSpecRequirement {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Invocation3StepSpecRequirement {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///idempotent-retry is lawful only for analysis, verify, query, render, doctor and export-delivery and only for faultCause ledger-busy; at most 3 attempts in total. Mutation, import, repair-preview, repair-apply and test-execution are never implicitly retried.
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation3StepSpecRetryPolicy {
    #[serde(rename = "idempotent-retry")]
    IdempotentRetry,
    #[serde(rename = "none")]
    None,
}
impl ::std::fmt::Display for Invocation3StepSpecRetryPolicy {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::IdempotentRetry => f.write_str("idempotent-retry"),
            Self::None => f.write_str("none"),
        }
    }
}
impl ::std::str::FromStr for Invocation3StepSpecRetryPolicy {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "idempotent-retry" => Ok(Self::IdempotentRetry),
            "none" => Ok(Self::None),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation3StepSpecRetryPolicy {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Invocation3StepSpecRetryPolicy {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Invocation3TestExecutionParams`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(transparent)]
pub struct Invocation3TestExecutionParams(pub TestExecution1TestExecutionStepParams);
impl ::std::ops::Deref for Invocation3TestExecutionParams {
    type Target = TestExecution1TestExecutionStepParams;
    fn deref(&self) -> &TestExecution1TestExecutionStepParams {
        &self.0
    }
}
impl ::std::convert::From<Invocation3TestExecutionParams>
for TestExecution1TestExecutionStepParams {
    fn from(value: Invocation3TestExecutionParams) -> Self {
        value.0
    }
}
impl ::std::convert::From<TestExecution1TestExecutionStepParams>
for Invocation3TestExecutionParams {
    fn from(value: TestExecution1TestExecutionStepParams) -> Self {
        Self(value)
    }
}
///`Invocation3TestExecutionResult`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(transparent)]
pub struct Invocation3TestExecutionResult(pub TestExecution1TestExecutionStepResult);
impl ::std::ops::Deref for Invocation3TestExecutionResult {
    type Target = TestExecution1TestExecutionStepResult;
    fn deref(&self) -> &TestExecution1TestExecutionStepResult {
        &self.0
    }
}
impl ::std::convert::From<Invocation3TestExecutionResult>
for TestExecution1TestExecutionStepResult {
    fn from(value: Invocation3TestExecutionResult) -> Self {
        value.0
    }
}
impl ::std::convert::From<TestExecution1TestExecutionStepResult>
for Invocation3TestExecutionResult {
    fn from(value: TestExecution1TestExecutionStepResult) -> Self {
        Self(value)
    }
}
///`Invocation3VerificationOutcome`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation3VerificationOutcome {
    #[serde(rename = "appliedSnapshotId")]
    pub applied_snapshot_id: Common3SnapshotId,
    #[serde(rename = "netNewFindings")]
    pub net_new_findings: Common3Uint53,
    #[serde(rename = "snapshotMatched")]
    pub snapshot_matched: bool,
    #[serde(rename = "targetsRemaining")]
    pub targets_remaining: Common3Uint53,
    #[serde(rename = "verifiedSnapshotId")]
    pub verified_snapshot_id: Common3SnapshotId,
}
///`Invocation3VerifyParams`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation3VerifyParams {
    ///the repair-apply step whose appliedSnapshotId the fresh snapshot must equal; verify always resnapshots and always seals a new authoritative Run
    #[serde(rename = "afterStep")]
    pub after_step: Common3StepId,
    #[serde(
        rename = "importedEvidenceSteps",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub imported_evidence_steps: FieldPresence<
        ::std::option::Option<::std::vec::Vec<Common3StepId>>,
    >,
    pub kind: ::serde_json::Value,
    pub profile: Inventory3AnalysisProfile,
}
///`Invocation3WorkflowRef`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(tag = "kind", deny_unknown_fields)]
pub enum Invocation3WorkflowRef {
    #[serde(rename = "builtin")]
    Builtin { name: Inventory3CommandName },
    #[serde(rename = "profile")]
    Profile {
        #[serde(rename = "activationId")]
        activation_id: Common3CanonicalIdentifier,
        #[serde(rename = "contributionId")]
        contribution_id: Common3ContributionId,
        #[serde(rename = "profileVersion")]
        profile_version: Common3SemanticVersion,
    },
}
///`Invocation5AnalysisParams`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation5AnalysisParams {
    #[serde(
        rename = "afterStep",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub after_step: FieldPresence<::std::option::Option<Common4StepId>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub baseline: FieldPresence<
        ::std::option::Option<Invocation5AnalysisParamsBaseline>,
    >,
    pub durability: Invocation5AnalysisParamsDurability,
    #[serde(
        rename = "importedEvidenceSteps",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub imported_evidence_steps: FieldPresence<
        ::std::option::Option<::std::vec::Vec<Common4StepId>>,
    >,
    pub kind: ::serde_json::Value,
    #[serde(
        rename = "pivotClosureIds",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub pivot_closure_ids: FieldPresence<
        ::std::option::Option<::std::vec::Vec<Common4ClosureId>>,
    >,
    #[serde(
        rename = "pivotOfStep",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub pivot_of_step: FieldPresence<::std::option::Option<Common4StepId>>,
    pub profile: Inventory3AnalysisProfile,
    ///pivot: the baseline's prior detector closure over current source, auto-planned before the primary analysis when a comparison needs the detector pivot and the closure is admitted
    pub role: Invocation5AnalysisParamsRole,
    ///fresh-after-step: a new snapshot is admitted after afterStep completed; never reuses a snapshot captured before a mutation
    #[serde(rename = "snapshotSource")]
    pub snapshot_source: Invocation5AnalysisParamsSnapshotSource,
    ///Step gate participation. self (default when absent): the Run verdict terminates this step (fail → policy-failed). delegated: this analysis supplies the current Run to exactly one later comparison step (which must name it as currentStep); its Run verdict does NOT terminate the step — completion, operational faults and requiredCoverage≠satisfied / verdict=indeterminate still do. A delegated analysis with no consuming comparison step is WORKFLOW.VERDICT_GATE_UNBOUND (request-rejected). A pivot analysis is always delegated.
    #[serde(
        rename = "verdictGate",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub verdict_gate: FieldPresence<
        ::std::option::Option<Invocation5AnalysisParamsVerdictGate>,
    >,
}
///`Invocation5AnalysisParamsBaseline`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation5AnalysisParamsBaseline {
    #[serde(
        rename = "acceptOriginProjectIds",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub accept_origin_project_ids: FieldPresence<
        ::std::option::Option<::std::vec::Vec<Common4ProjectId>>,
    >,
    #[serde(rename = "auditProfile")]
    pub audit_profile: Comparison2AuditProfileName,
    #[serde(
        rename = "closureBundlePath",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub closure_bundle_path: FieldPresence<::std::option::Option<Common4UserInputPath>>,
    pub path: Common4UserInputPath,
}
///`Invocation5AnalysisParamsDurability`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation5AnalysisParamsDurability {
    #[serde(rename = "authoritative")]
    Authoritative,
    #[serde(rename = "ephemeral")]
    Ephemeral,
}
impl ::std::fmt::Display for Invocation5AnalysisParamsDurability {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Authoritative => f.write_str("authoritative"),
            Self::Ephemeral => f.write_str("ephemeral"),
        }
    }
}
impl ::std::str::FromStr for Invocation5AnalysisParamsDurability {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "authoritative" => Ok(Self::Authoritative),
            "ephemeral" => Ok(Self::Ephemeral),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation5AnalysisParamsDurability {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Invocation5AnalysisParamsDurability {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///pivot: the baseline's prior detector closure over current source, auto-planned before the primary analysis when a comparison needs the detector pivot and the closure is admitted
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation5AnalysisParamsRole {
    #[serde(rename = "primary")]
    Primary,
    #[serde(rename = "pivot")]
    Pivot,
}
impl ::std::fmt::Display for Invocation5AnalysisParamsRole {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Primary => f.write_str("primary"),
            Self::Pivot => f.write_str("pivot"),
        }
    }
}
impl ::std::str::FromStr for Invocation5AnalysisParamsRole {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "primary" => Ok(Self::Primary),
            "pivot" => Ok(Self::Pivot),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation5AnalysisParamsRole {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Invocation5AnalysisParamsRole {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///fresh-after-step: a new snapshot is admitted after afterStep completed; never reuses a snapshot captured before a mutation
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation5AnalysisParamsSnapshotSource {
    #[serde(rename = "live-worktree")]
    LiveWorktree,
    #[serde(rename = "fresh-after-step")]
    FreshAfterStep,
}
impl ::std::fmt::Display for Invocation5AnalysisParamsSnapshotSource {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::LiveWorktree => f.write_str("live-worktree"),
            Self::FreshAfterStep => f.write_str("fresh-after-step"),
        }
    }
}
impl ::std::str::FromStr for Invocation5AnalysisParamsSnapshotSource {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "live-worktree" => Ok(Self::LiveWorktree),
            "fresh-after-step" => Ok(Self::FreshAfterStep),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation5AnalysisParamsSnapshotSource {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Invocation5AnalysisParamsSnapshotSource {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Step gate participation. self (default when absent): the Run verdict terminates this step (fail → policy-failed). delegated: this analysis supplies the current Run to exactly one later comparison step (which must name it as currentStep); its Run verdict does NOT terminate the step — completion, operational faults and requiredCoverage≠satisfied / verdict=indeterminate still do. A delegated analysis with no consuming comparison step is WORKFLOW.VERDICT_GATE_UNBOUND (request-rejected). A pivot analysis is always delegated.
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation5AnalysisParamsVerdictGate {
    #[serde(rename = "self")]
    Self_,
    #[serde(rename = "delegated")]
    Delegated,
}
impl ::std::fmt::Display for Invocation5AnalysisParamsVerdictGate {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Self_ => f.write_str("self"),
            Self::Delegated => f.write_str("delegated"),
        }
    }
}
impl ::std::str::FromStr for Invocation5AnalysisParamsVerdictGate {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "self" => Ok(Self::Self_),
            "delegated" => Ok(Self::Delegated),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation5AnalysisParamsVerdictGate {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Invocation5AnalysisParamsVerdictGate {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Closed union. authoritative: a committed Run with receipt. ephemeral: no Run, no receipt, no authority; carries only semantic plan/evidence identities so that a result can be cited, and can never satisfy baseline adoption, repair preconditions, or verify.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(tag = "authority", deny_unknown_fields)]
pub enum Invocation5AnalysisResult {
    #[serde(rename = "authoritative")]
    Authoritative {
        #[serde(
            rename = "comparisonResultId",
            default,
            skip_serializing_if = "FieldPresence::is_missing"
        )]
        comparison_result_id: FieldPresence<
            ::std::option::Option<Common4ComparisonResultId>,
        >,
        #[serde(
            rename = "coverageId",
            default,
            skip_serializing_if = "FieldPresence::is_missing"
        )]
        coverage_id: FieldPresence<::std::option::Option<Common4CoverageId>>,
        deficiency: Common4D9Deficiency,
        durability: ::serde_json::Value,
        kind: Invocation5AnalysisResultKind,
        #[serde(rename = "planId")]
        plan_id: Common4PlanId,
        #[serde(rename = "requiredCoverage")]
        required_coverage: Common4RequiredCoverage,
        #[serde(rename = "runId")]
        run_id: Common4RunId,
        #[serde(rename = "secondaryDeficiencies")]
        secondary_deficiencies: ::std::vec::Vec<Common4D9Deficiency>,
        verdict: Common4Verdict,
        #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
        verification: FieldPresence<
            ::std::option::Option<Invocation5VerificationOutcome>,
        >,
    },
    #[serde(rename = "ephemeral")]
    Ephemeral {
        #[serde(
            rename = "comparisonResultId",
            default,
            skip_serializing_if = "FieldPresence::is_missing"
        )]
        comparison_result_id: FieldPresence<
            ::std::option::Option<Common4ComparisonResultId>,
        >,
        #[serde(
            rename = "coverageId",
            default,
            skip_serializing_if = "FieldPresence::is_missing"
        )]
        coverage_id: FieldPresence<::std::option::Option<Common4CoverageId>>,
        deficiency: Common4D9Deficiency,
        durability: ::serde_json::Value,
        #[serde(rename = "evidenceId")]
        evidence_id: Common4EvidenceId,
        kind: ::serde_json::Value,
        #[serde(rename = "planId")]
        plan_id: Common4PlanId,
        #[serde(rename = "requiredCoverage")]
        required_coverage: Common4RequiredCoverage,
        #[serde(rename = "secondaryDeficiencies")]
        secondary_deficiencies: ::std::vec::Vec<Common4D9Deficiency>,
        verdict: Common4Verdict,
    },
}
///`Invocation5AnalysisResultKind`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation5AnalysisResultKind {
    #[serde(rename = "analysis")]
    Analysis,
    #[serde(rename = "verify")]
    Verify,
}
impl ::std::fmt::Display for Invocation5AnalysisResultKind {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Analysis => f.write_str("analysis"),
            Self::Verify => f.write_str("verify"),
        }
    }
}
impl ::std::str::FromStr for Invocation5AnalysisResultKind {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "analysis" => Ok(Self::Analysis),
            "verify" => Ok(Self::Verify),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation5AnalysisResultKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Invocation5AnalysisResultKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Invocation5Attempt`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation5Attempt {
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub derivation: FieldPresence<::std::option::Option<Invocation5DerivationBinding>>,
    #[serde(rename = "executionId")]
    pub execution_id: Common4ExecutionId,
    #[serde(
        rename = "faultCause",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub fault_cause: FieldPresence<::std::option::Option<Common4D9FaultCause>>,
    ///Installation mutation attempts only. Initial attempt: first LEASED after all locks, then durable revisions written in order. Recovery attempt: first is the observed installationRecoveryStartRef (any closed state), then revisions written by this attempt. Earlier attempt records remain unchanged. Required once a journal exists, including failed/abandoned attempts; absent before any journal. Operational custody, excluded from Run identity.
    #[serde(
        rename = "installationJournalRefs",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub installation_journal_refs: FieldPresence<
        ::std::option::Option<::std::vec::Vec<Common4InstallationTransitionJournalRef>>,
    >,
    ///Recovery attempt only: exact current durable revision read under the installation fence; equals installationJournalRefs[0]. It is host-observed, never accepted from request input.
    #[serde(
        rename = "installationRecoveryStartRef",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub installation_recovery_start_ref: FieldPresence<
        ::std::option::Option<Common4InstallationTransitionJournalRef>,
    >,
    #[serde(rename = "observedDuration")]
    pub observed_duration: Invocation5AttemptDurationV1,
    pub outcome: Invocation5AttemptOutcome,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub retried: FieldPresence<::std::option::Option<bool>>,
}
///Host monotonic observation of this attempt only, with explicit inability to measure. Milliseconds are truncated from the elapsed monotonic nanoseconds; zero is a valid measured duration. Source custody and lifecycle rules are semantic admission duties.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(tag = "state", deny_unknown_fields)]
pub enum Invocation5AttemptDurationV1 {
    #[serde(rename = "measured")]
    Measured { milliseconds: u64 },
    #[serde(rename = "unavailable")]
    Unavailable { reason: Invocation5AttemptDurationV1Reason },
}
///`Invocation5AttemptDurationV1Reason`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation5AttemptDurationV1Reason {
    #[serde(rename = "supervisor-lost")]
    SupervisorLost,
    #[serde(rename = "clock-unavailable")]
    ClockUnavailable,
    #[serde(rename = "clock-regressed")]
    ClockRegressed,
    #[serde(rename = "duration-overflow")]
    DurationOverflow,
}
impl ::std::fmt::Display for Invocation5AttemptDurationV1Reason {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::SupervisorLost => f.write_str("supervisor-lost"),
            Self::ClockUnavailable => f.write_str("clock-unavailable"),
            Self::ClockRegressed => f.write_str("clock-regressed"),
            Self::DurationOverflow => f.write_str("duration-overflow"),
        }
    }
}
impl ::std::str::FromStr for Invocation5AttemptDurationV1Reason {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "supervisor-lost" => Ok(Self::SupervisorLost),
            "clock-unavailable" => Ok(Self::ClockUnavailable),
            "clock-regressed" => Ok(Self::ClockRegressed),
            "duration-overflow" => Ok(Self::DurationOverflow),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation5AttemptDurationV1Reason {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Invocation5AttemptDurationV1Reason {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Invocation5AttemptOutcome`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation5AttemptOutcome {
    #[serde(rename = "completed")]
    Completed,
    #[serde(rename = "rejected")]
    Rejected,
    #[serde(rename = "failed")]
    Failed,
    #[serde(rename = "cancelled")]
    Cancelled,
    #[serde(rename = "abandoned")]
    Abandoned,
}
impl ::std::fmt::Display for Invocation5AttemptOutcome {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Completed => f.write_str("completed"),
            Self::Rejected => f.write_str("rejected"),
            Self::Failed => f.write_str("failed"),
            Self::Cancelled => f.write_str("cancelled"),
            Self::Abandoned => f.write_str("abandoned"),
        }
    }
}
impl ::std::str::FromStr for Invocation5AttemptOutcome {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "completed" => Ok(Self::Completed),
            "rejected" => Ok(Self::Rejected),
            "failed" => Ok(Self::Failed),
            "cancelled" => Ok(Self::Cancelled),
            "abandoned" => Ok(Self::Abandoned),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation5AttemptOutcome {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Invocation5AttemptOutcome {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Invocation5AttemptPropertiesExecutionId`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(transparent)]
pub struct Invocation5AttemptPropertiesExecutionId(pub Common4ExecutionId);
impl ::std::ops::Deref for Invocation5AttemptPropertiesExecutionId {
    type Target = Common4ExecutionId;
    fn deref(&self) -> &Common4ExecutionId {
        &self.0
    }
}
impl ::std::convert::From<Common4ExecutionId>
for Invocation5AttemptPropertiesExecutionId {
    fn from(value: Common4ExecutionId) -> Self {
        Self(value)
    }
}
impl ::std::fmt::Display for Invocation5AttemptPropertiesExecutionId {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        self.0.fmt(f)
    }
}
impl ::std::str::FromStr for Invocation5AttemptPropertiesExecutionId {
    type Err = <Common4ExecutionId as ::std::str::FromStr>::Err;
    fn from_str(value: &str) -> ::std::result::Result<Self, Self::Err> {
        Ok(Self(value.parse()?))
    }
}
impl ::std::convert::TryFrom<&str> for Invocation5AttemptPropertiesExecutionId {
    type Error = <Common4ExecutionId as ::std::str::FromStr>::Err;
    fn try_from(value: &str) -> ::std::result::Result<Self, Self::Error> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<String> for Invocation5AttemptPropertiesExecutionId {
    type Error = <Common4ExecutionId as ::std::str::FromStr>::Err;
    fn try_from(value: String) -> ::std::result::Result<Self, Self::Error> {
        value.parse()
    }
}
///`Invocation5AttemptPropertiesFaultCause`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(transparent)]
pub struct Invocation5AttemptPropertiesFaultCause(pub Common4D9FaultCause);
impl ::std::ops::Deref for Invocation5AttemptPropertiesFaultCause {
    type Target = Common4D9FaultCause;
    fn deref(&self) -> &Common4D9FaultCause {
        &self.0
    }
}
impl ::std::convert::From<Common4D9FaultCause>
for Invocation5AttemptPropertiesFaultCause {
    fn from(value: Common4D9FaultCause) -> Self {
        Self(value)
    }
}
impl ::std::fmt::Display for Invocation5AttemptPropertiesFaultCause {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        self.0.fmt(f)
    }
}
impl ::std::str::FromStr for Invocation5AttemptPropertiesFaultCause {
    type Err = <Common4D9FaultCause as ::std::str::FromStr>::Err;
    fn from_str(value: &str) -> ::std::result::Result<Self, Self::Err> {
        Ok(Self(value.parse()?))
    }
}
impl ::std::convert::TryFrom<&str> for Invocation5AttemptPropertiesFaultCause {
    type Error = <Common4D9FaultCause as ::std::str::FromStr>::Err;
    fn try_from(value: &str) -> ::std::result::Result<Self, Self::Error> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<String> for Invocation5AttemptPropertiesFaultCause {
    type Error = <Common4D9FaultCause as ::std::str::FromStr>::Err;
    fn try_from(value: String) -> ::std::result::Result<Self, Self::Error> {
        value.parse()
    }
}
///`Invocation5AttemptPropertiesOutcome`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation5AttemptPropertiesOutcome {
    #[serde(rename = "completed")]
    Completed,
    #[serde(rename = "rejected")]
    Rejected,
    #[serde(rename = "failed")]
    Failed,
    #[serde(rename = "cancelled")]
    Cancelled,
    #[serde(rename = "abandoned")]
    Abandoned,
}
impl ::std::fmt::Display for Invocation5AttemptPropertiesOutcome {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Completed => f.write_str("completed"),
            Self::Rejected => f.write_str("rejected"),
            Self::Failed => f.write_str("failed"),
            Self::Cancelled => f.write_str("cancelled"),
            Self::Abandoned => f.write_str("abandoned"),
        }
    }
}
impl ::std::str::FromStr for Invocation5AttemptPropertiesOutcome {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "completed" => Ok(Self::Completed),
            "rejected" => Ok(Self::Rejected),
            "failed" => Ok(Self::Failed),
            "cancelled" => Ok(Self::Cancelled),
            "abandoned" => Ok(Self::Abandoned),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation5AttemptPropertiesOutcome {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Invocation5AttemptPropertiesOutcome {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Invocation5AttemptPropertiesRetried`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(transparent)]
pub struct Invocation5AttemptPropertiesRetried(pub bool);
impl ::std::ops::Deref for Invocation5AttemptPropertiesRetried {
    type Target = bool;
    fn deref(&self) -> &bool {
        &self.0
    }
}
impl ::std::convert::From<Invocation5AttemptPropertiesRetried> for bool {
    fn from(value: Invocation5AttemptPropertiesRetried) -> Self {
        value.0
    }
}
impl ::std::convert::From<bool> for Invocation5AttemptPropertiesRetried {
    fn from(value: bool) -> Self {
        Self(value)
    }
}
impl ::std::fmt::Display for Invocation5AttemptPropertiesRetried {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        self.0.fmt(f)
    }
}
impl ::std::str::FromStr for Invocation5AttemptPropertiesRetried {
    type Err = <bool as ::std::str::FromStr>::Err;
    fn from_str(value: &str) -> ::std::result::Result<Self, Self::Err> {
        Ok(Self(value.parse()?))
    }
}
impl ::std::convert::TryFrom<&str> for Invocation5AttemptPropertiesRetried {
    type Error = <bool as ::std::str::FromStr>::Err;
    fn try_from(value: &str) -> ::std::result::Result<Self, Self::Error> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<String> for Invocation5AttemptPropertiesRetried {
    type Error = <bool as ::std::str::FromStr>::Err;
    fn try_from(value: String) -> ::std::result::Result<Self, Self::Error> {
        value.parse()
    }
}
///baseline show [PATH]: the tracked baseline artifact path (default opensip.baseline.json resolved by the host).
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation5BaselineInspectRequestV1 {
    pub operation: ::serde_json::Value,
    pub path: Common4UserInputPath,
}
///`Invocation5Cancellation`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation5Cancellation {
    ///before-settle: at least one required step had not reached a terminal outcome; aggregate is interrupted (130). after-settle: every required step already reached a terminal outcome; the aggregate termination is not reclassified.
    pub phase: Invocation5CancellationPhase,
    pub requested: bool,
    pub signal: Common4D9Signal,
}
///before-settle: at least one required step had not reached a terminal outcome; aggregate is interrupted (130). after-settle: every required step already reached a terminal outcome; the aggregate termination is not reclassified.
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation5CancellationPhase {
    #[serde(rename = "none")]
    None,
    #[serde(rename = "before-settle")]
    BeforeSettle,
    #[serde(rename = "after-settle")]
    AfterSettle,
}
impl ::std::fmt::Display for Invocation5CancellationPhase {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::None => f.write_str("none"),
            Self::BeforeSettle => f.write_str("before-settle"),
            Self::AfterSettle => f.write_str("after-settle"),
        }
    }
}
impl ::std::str::FromStr for Invocation5CancellationPhase {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "none" => Ok(Self::None),
            "before-settle" => Ok(Self::BeforeSettle),
            "after-settle" => Ok(Self::AfterSettle),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation5CancellationPhase {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Invocation5CancellationPhase {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Invocation5ComparisonParams`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation5ComparisonParams {
    #[serde(
        rename = "acceptOriginProjectIds",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub accept_origin_project_ids: FieldPresence<
        ::std::option::Option<::std::vec::Vec<Common4ProjectId>>,
    >,
    #[serde(rename = "auditProfile")]
    pub audit_profile: Comparison2AuditProfileName,
    pub baseline: Common4UserInputPath,
    #[serde(
        rename = "closureBundlePath",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub closure_bundle_path: FieldPresence<::std::option::Option<Common4UserInputPath>>,
    ///the authoritative primary analysis whose Run is the current side; that step must carry verdictGate=delegated and must be in dependsOn
    #[serde(rename = "currentStep")]
    pub current_step: Common4StepId,
    pub kind: ::serde_json::Value,
    ///the role=pivot analysis step when E0 is needed; must be in dependsOn
    #[serde(
        rename = "pivotStep",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub pivot_step: FieldPresence<::std::option::Option<Common4StepId>>,
}
///Operational projection of a ComparisonResultV1. The step termination is derived from verdict: fail → policy-failed (runId = currentRunId); indeterminate → indeterminate with reasonCodes [VERDICT.INDETERMINATE] or [BASELINE.RECIPE_UNSUPPORTED] per d9Deficiency and the descriptor remedy as domainDetail; pass → success (runId = currentRunId). Never defaults to success.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation5ComparisonStepResult {
    #[serde(rename = "baselineId")]
    pub baseline_id: Common4BaselineId,
    #[serde(rename = "comparisonPerformed")]
    pub comparison_performed: bool,
    #[serde(rename = "comparisonResultId")]
    pub comparison_result_id: Common4ComparisonResultId,
    pub counts: Invocation5ComparisonStepResultCounts,
    #[serde(rename = "currentRunId")]
    pub current_run_id: Common4RunId,
    #[serde(
        rename = "d9Deficiency",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub d9_deficiency: FieldPresence<::std::option::Option<Common4D9Deficiency>>,
    pub kind: ::serde_json::Value,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub remedy: FieldPresence<::std::option::Option<Common4DomainDetail>>,
    pub verdict: Invocation5ComparisonStepResultVerdict,
}
///`Invocation5ComparisonStepResultCounts`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation5ComparisonStepResultCounts {
    pub entries: Common4Uint53,
    pub gating: Common4Uint53,
    pub indeterminate: Common4Uint53,
}
///`Invocation5ComparisonStepResultVerdict`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation5ComparisonStepResultVerdict {
    #[serde(rename = "pass")]
    Pass,
    #[serde(rename = "fail")]
    Fail,
    #[serde(rename = "indeterminate")]
    Indeterminate,
}
impl ::std::fmt::Display for Invocation5ComparisonStepResultVerdict {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Pass => f.write_str("pass"),
            Self::Fail => f.write_str("fail"),
            Self::Indeterminate => f.write_str("indeterminate"),
        }
    }
}
impl ::std::str::FromStr for Invocation5ComparisonStepResultVerdict {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "pass" => Ok(Self::Pass),
            "fail" => Ok(Self::Fail),
            "indeterminate" => Ok(Self::Indeterminate),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation5ComparisonStepResultVerdict {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Invocation5ComparisonStepResultVerdict {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///One closed installation intent for core update/repair/rollback and store migrate/rollback. Security S9.2 admits exact per-operation closure/schema/store/deadline semantics and journals the derived namespace lease set. Store operations keep the core closure; a same-schema core operation keeps the store. Target trust/profile/generation/time observations are host-admitted, never caller granted.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation5CoreTransitionIntentV1 {
    #[serde(rename = "fromCoreClosure")]
    pub from_core_closure: Common4ClosureId,
    #[serde(rename = "fromStateSchema")]
    pub from_state_schema: ExactInteger,
    #[serde(rename = "fromStoreGeneration")]
    pub from_store_generation: u64,
    pub operation: Invocation5CoreTransitionIntentV1Operation,
    #[serde(rename = "platformProfileSetBodyDigest")]
    pub platform_profile_set_body_digest: Common4Sha256Hex,
    #[serde(rename = "preconditionGeneration")]
    pub precondition_generation: u64,
    #[serde(
        rename = "rollbackDeadline",
        deserialize_with = "::std::option::Option::deserialize"
    )]
    pub rollback_deadline: ::std::option::Option<Common4UtcTimestamp>,
    #[serde(rename = "schemaVersion")]
    pub schema_version: ExactInteger,
    #[serde(rename = "toCoreClosure")]
    pub to_core_closure: Common4ClosureId,
    #[serde(rename = "toStateSchema")]
    pub to_state_schema: ExactInteger,
    #[serde(rename = "toStoreGeneration")]
    pub to_store_generation: u64,
}
///`Invocation5CoreTransitionIntentV1Operation`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation5CoreTransitionIntentV1Operation {
    #[serde(rename = "core-update")]
    CoreUpdate,
    #[serde(rename = "core-repair")]
    CoreRepair,
    #[serde(rename = "core-rollback")]
    CoreRollback,
    #[serde(rename = "store-migrate")]
    StoreMigrate,
    #[serde(rename = "store-rollback")]
    StoreRollback,
}
impl ::std::fmt::Display for Invocation5CoreTransitionIntentV1Operation {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::CoreUpdate => f.write_str("core-update"),
            Self::CoreRepair => f.write_str("core-repair"),
            Self::CoreRollback => f.write_str("core-rollback"),
            Self::StoreMigrate => f.write_str("store-migrate"),
            Self::StoreRollback => f.write_str("store-rollback"),
        }
    }
}
impl ::std::str::FromStr for Invocation5CoreTransitionIntentV1Operation {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "core-update" => Ok(Self::CoreUpdate),
            "core-repair" => Ok(Self::CoreRepair),
            "core-rollback" => Ok(Self::CoreRollback),
            "store-migrate" => Ok(Self::StoreMigrate),
            "store-rollback" => Ok(Self::StoreRollback),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation5CoreTransitionIntentV1Operation {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Invocation5CoreTransitionIntentV1Operation {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Explicit mapping from one analysis/verify attempt to its derivation DAG. The workflow step DAG (≤64 steps) and the derivation DAG (≤1024 stages) are distinct: a step never depends on a stage and a stage never references a step. One attempt owns exactly one execution plan; a retry attempt on identical admitted inputs may bind the same exec-plan2 and Run.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation5DerivationBinding {
    #[serde(rename = "executionPlanId")]
    pub execution_plan_id: Common4ExecutionPlanId,
    #[serde(
        rename = "firstFailedStage",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub first_failed_stage: FieldPresence<::std::option::Option<Common4StageOrdinal>>,
    #[serde(rename = "planId")]
    pub plan_id: Common4PlanId,
    #[serde(rename = "stageCount")]
    pub stage_count: ::std::num::NonZeroU64,
    #[serde(rename = "stagesCompleted")]
    pub stages_completed: i64,
}
///recommend [--emit-config-proposal PATH].
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation5DiscoveryRecommendRequestV1 {
    #[serde(
        rename = "emitConfigProposalPath",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub emit_config_proposal_path: FieldPresence<
        ::std::option::Option<Common4UserInputPath>,
    >,
    pub operation: ::serde_json::Value,
}
///`Invocation5DoctorParams`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation5DoctorParams {
    pub checks: ::std::vec::Vec<Invocation5DoctorParamsChecksItem>,
    pub kind: ::serde_json::Value,
}
///`Invocation5DoctorParamsChecksItem`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation5DoctorParamsChecksItem {
    #[serde(rename = "closures")]
    Closures,
    #[serde(rename = "trust")]
    Trust,
    #[serde(rename = "store")]
    Store,
    #[serde(rename = "platform")]
    Platform,
    #[serde(rename = "project-marker")]
    ProjectMarker,
    #[serde(rename = "offline-window")]
    OfflineWindow,
}
impl ::std::fmt::Display for Invocation5DoctorParamsChecksItem {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Closures => f.write_str("closures"),
            Self::Trust => f.write_str("trust"),
            Self::Store => f.write_str("store"),
            Self::Platform => f.write_str("platform"),
            Self::ProjectMarker => f.write_str("project-marker"),
            Self::OfflineWindow => f.write_str("offline-window"),
        }
    }
}
impl ::std::str::FromStr for Invocation5DoctorParamsChecksItem {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "closures" => Ok(Self::Closures),
            "trust" => Ok(Self::Trust),
            "store" => Ok(Self::Store),
            "platform" => Ok(Self::Platform),
            "project-marker" => Ok(Self::ProjectMarker),
            "offline-window" => Ok(Self::OfflineWindow),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation5DoctorParamsChecksItem {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Invocation5DoctorParamsChecksItem {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Invocation5DoctorResult`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation5DoctorResult {
    pub defects: ::std::vec::Vec<Common4DomainDetail>,
    #[serde(rename = "defectsFound")]
    pub defects_found: Common4Uint53,
    pub kind: ::serde_json::Value,
    #[serde(rename = "reportProduced")]
    pub report_produced: bool,
}
///`Invocation5ExportDeliveryParams`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation5ExportDeliveryParams {
    pub kind: ::serde_json::Value,
    ///optional egress failure never changes a local verdict (success); explicitly required delivery failure is operational-failed
    pub required: bool,
    pub sink: Common4CanonicalIdentifier,
    #[serde(rename = "sourceStep")]
    pub source_step: Common4StepId,
}
///`Invocation5ExportDeliveryResult`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation5ExportDeliveryResult {
    pub delivered: bool,
    pub kind: ::serde_json::Value,
}
///`Invocation5FitQueryFromAnalysisParams`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation5FitQueryFromAnalysisParams {
    pub kind: ::serde_json::Value,
    pub operation: ::serde_json::Value,
    #[serde(rename = "sourceStep")]
    pub source_step: i64,
}
///Closed host-only query-step operations for query-class CLI commands whose request has no member of the public graph-query:3 Operation/Params API. Never members of that public Operation enum and never public query operations.
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation5HostQueryOperation {
    #[serde(rename = "baseline.inspect")]
    BaselineInspect,
    #[serde(rename = "discovery.recommend")]
    DiscoveryRecommend,
    #[serde(rename = "policy.show")]
    PolicyShow,
    #[serde(rename = "policy.test")]
    PolicyTest,
    #[serde(rename = "review.produce-brief")]
    ReviewProduceBrief,
}
impl ::std::fmt::Display for Invocation5HostQueryOperation {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::BaselineInspect => f.write_str("baseline.inspect"),
            Self::DiscoveryRecommend => f.write_str("discovery.recommend"),
            Self::PolicyShow => f.write_str("policy.show"),
            Self::PolicyTest => f.write_str("policy.test"),
            Self::ReviewProduceBrief => f.write_str("review.produce-brief"),
        }
    }
}
impl ::std::str::FromStr for Invocation5HostQueryOperation {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "baseline.inspect" => Ok(Self::BaselineInspect),
            "discovery.recommend" => Ok(Self::DiscoveryRecommend),
            "policy.show" => Ok(Self::PolicyShow),
            "policy.test" => Ok(Self::PolicyTest),
            "review.produce-brief" => Ok(Self::ReviewProduceBrief),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation5HostQueryOperation {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Invocation5HostQueryOperation {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///A query step over one closed host-only operation; request is the closed record of exactly that operation.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation5HostQueryParams {
    pub kind: ::serde_json::Value,
    pub operation: Invocation5HostQueryOperation,
    pub request: Invocation5HostQueryParamsRequest,
}
///`Invocation5HostQueryParamsRequest`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(untagged)]
pub enum Invocation5HostQueryParamsRequest {
    BaselineInspectRequestV1(Invocation5BaselineInspectRequestV1),
    DiscoveryRecommendRequestV1(Invocation5DiscoveryRecommendRequestV1),
    PolicyShowRequestV1(Invocation5PolicyShowRequestV1),
    PolicyTestRequestV1(Invocation5PolicyTestRequestV1),
    ReviewBriefProduceRequestV1(Invocation5ReviewBriefProduceRequestV1),
}
impl ::std::convert::From<Invocation5BaselineInspectRequestV1>
for Invocation5HostQueryParamsRequest {
    fn from(value: Invocation5BaselineInspectRequestV1) -> Self {
        Self::BaselineInspectRequestV1(value)
    }
}
impl ::std::convert::From<Invocation5DiscoveryRecommendRequestV1>
for Invocation5HostQueryParamsRequest {
    fn from(value: Invocation5DiscoveryRecommendRequestV1) -> Self {
        Self::DiscoveryRecommendRequestV1(value)
    }
}
impl ::std::convert::From<Invocation5PolicyShowRequestV1>
for Invocation5HostQueryParamsRequest {
    fn from(value: Invocation5PolicyShowRequestV1) -> Self {
        Self::PolicyShowRequestV1(value)
    }
}
impl ::std::convert::From<Invocation5PolicyTestRequestV1>
for Invocation5HostQueryParamsRequest {
    fn from(value: Invocation5PolicyTestRequestV1) -> Self {
        Self::PolicyTestRequestV1(value)
    }
}
impl ::std::convert::From<Invocation5ReviewBriefProduceRequestV1>
for Invocation5HostQueryParamsRequest {
    fn from(value: Invocation5ReviewBriefProduceRequestV1) -> Self {
        Self::ReviewBriefProduceRequestV1(value)
    }
}
///`Invocation5ImportParams`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation5ImportParams {
    pub correspondence: Common4SourceCorrespondence,
    #[serde(rename = "evidenceKind")]
    pub evidence_kind: Imported1ImportKind,
    pub kind: ::serde_json::Value,
    pub path: Common4UserInputPath,
}
///`Invocation5ImportResult`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation5ImportResult {
    #[serde(rename = "importId")]
    pub import_id: Common4ImportId,
    pub kind: ::serde_json::Value,
    #[serde(rename = "payloadDigest")]
    pub payload_digest: Common4Sha256Hex,
    #[serde(rename = "receiptId")]
    pub receipt_id: Common4ReceiptId,
    pub staleness: Imported1Staleness,
}
///`Invocation5Mode`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation5Mode {
    pub ci: bool,
    ///true only with explicit --ephemeral; a non-authoritative invocation cannot supply baseline/repair prerequisites
    pub ephemeral: bool,
    pub interactive: bool,
}
///`Invocation5MutationParams`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation5MutationParams {
    ///Bare H("workflow.mutation-intent", MutationReplayScopeV1) binding this host-minted requestId, stepId, projectId and mutationClass as operation. The exact scope and admitted immutable step parameters are retained and checked before receipt lookup. Equal COMPLETED replay performs no second effect; separate fresh requests have different keys. Repair apply has a separate step/recipe.
    #[serde(rename = "idempotencyKey")]
    pub idempotency_key: Common4Sha256Hex,
    ///Retained closed operation-specific input: CoreTransitionIntentV1 for installation operations; RepairRecoveryIntentV1 for repair-recover.
    #[serde(
        rename = "inputDescriptorDigest",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub input_descriptor_digest: FieldPresence<::std::option::Option<Common4Sha256Hex>>,
    pub kind: ::serde_json::Value,
    #[serde(rename = "mutationClass")]
    pub mutation_class: Invocation5MutationParamsMutationClass,
    #[serde(
        rename = "sourceStep",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub source_step: FieldPresence<::std::option::Option<Common4StepId>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub target: FieldPresence<::std::option::Option<Common4UserInputPath>>,
}
///`Invocation5MutationParamsMutationClass`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation5MutationParamsMutationClass {
    #[serde(rename = "repair-apply")]
    RepairApply,
    #[serde(rename = "repair-recover")]
    RepairRecover,
    #[serde(rename = "baseline-adopt")]
    BaselineAdopt,
    #[serde(rename = "baseline-upgrade-apply")]
    BaselineUpgradeApply,
    #[serde(rename = "baseline-export")]
    BaselineExport,
    #[serde(rename = "waiver-change")]
    WaiverChange,
    #[serde(rename = "policy-write")]
    PolicyWrite,
    #[serde(rename = "config-write")]
    ConfigWrite,
    #[serde(rename = "purge")]
    Purge,
    #[serde(rename = "install")]
    Install,
    #[serde(rename = "update")]
    Update,
    #[serde(rename = "review-join")]
    ReviewJoin,
    #[serde(rename = "import")]
    Import,
    #[serde(rename = "trust-refresh")]
    TrustRefresh,
    #[serde(rename = "trust-import")]
    TrustImport,
    #[serde(rename = "trust-recovery-challenge")]
    TrustRecoveryChallenge,
    #[serde(rename = "trust-recovery-import")]
    TrustRecoveryImport,
    #[serde(rename = "store-migrate")]
    StoreMigrate,
    #[serde(rename = "store-rollback")]
    StoreRollback,
    #[serde(rename = "store-gc")]
    StoreGc,
    #[serde(rename = "core-update")]
    CoreUpdate,
    #[serde(rename = "core-repair")]
    CoreRepair,
    #[serde(rename = "core-rollback")]
    CoreRollback,
    #[serde(rename = "native-preparation")]
    NativePreparation,
}
impl ::std::fmt::Display for Invocation5MutationParamsMutationClass {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::RepairApply => f.write_str("repair-apply"),
            Self::RepairRecover => f.write_str("repair-recover"),
            Self::BaselineAdopt => f.write_str("baseline-adopt"),
            Self::BaselineUpgradeApply => f.write_str("baseline-upgrade-apply"),
            Self::BaselineExport => f.write_str("baseline-export"),
            Self::WaiverChange => f.write_str("waiver-change"),
            Self::PolicyWrite => f.write_str("policy-write"),
            Self::ConfigWrite => f.write_str("config-write"),
            Self::Purge => f.write_str("purge"),
            Self::Install => f.write_str("install"),
            Self::Update => f.write_str("update"),
            Self::ReviewJoin => f.write_str("review-join"),
            Self::Import => f.write_str("import"),
            Self::TrustRefresh => f.write_str("trust-refresh"),
            Self::TrustImport => f.write_str("trust-import"),
            Self::TrustRecoveryChallenge => f.write_str("trust-recovery-challenge"),
            Self::TrustRecoveryImport => f.write_str("trust-recovery-import"),
            Self::StoreMigrate => f.write_str("store-migrate"),
            Self::StoreRollback => f.write_str("store-rollback"),
            Self::StoreGc => f.write_str("store-gc"),
            Self::CoreUpdate => f.write_str("core-update"),
            Self::CoreRepair => f.write_str("core-repair"),
            Self::CoreRollback => f.write_str("core-rollback"),
            Self::NativePreparation => f.write_str("native-preparation"),
        }
    }
}
impl ::std::str::FromStr for Invocation5MutationParamsMutationClass {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "repair-apply" => Ok(Self::RepairApply),
            "repair-recover" => Ok(Self::RepairRecover),
            "baseline-adopt" => Ok(Self::BaselineAdopt),
            "baseline-upgrade-apply" => Ok(Self::BaselineUpgradeApply),
            "baseline-export" => Ok(Self::BaselineExport),
            "waiver-change" => Ok(Self::WaiverChange),
            "policy-write" => Ok(Self::PolicyWrite),
            "config-write" => Ok(Self::ConfigWrite),
            "purge" => Ok(Self::Purge),
            "install" => Ok(Self::Install),
            "update" => Ok(Self::Update),
            "review-join" => Ok(Self::ReviewJoin),
            "import" => Ok(Self::Import),
            "trust-refresh" => Ok(Self::TrustRefresh),
            "trust-import" => Ok(Self::TrustImport),
            "trust-recovery-challenge" => Ok(Self::TrustRecoveryChallenge),
            "trust-recovery-import" => Ok(Self::TrustRecoveryImport),
            "store-migrate" => Ok(Self::StoreMigrate),
            "store-rollback" => Ok(Self::StoreRollback),
            "store-gc" => Ok(Self::StoreGc),
            "core-update" => Ok(Self::CoreUpdate),
            "core-repair" => Ok(Self::CoreRepair),
            "core-rollback" => Ok(Self::CoreRollback),
            "native-preparation" => Ok(Self::NativePreparation),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation5MutationParamsMutationClass {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Invocation5MutationParamsMutationClass {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Retained operational replay namespace for a generic mutation. H(workflow.mutation-intent, this complete record) is its idempotencyKey. The admitted immutable invocation and step own effect inputs; a key grants no authority and never deduplicates different fresh requests. Repair apply uses its separate exact content-derived recipe.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation5MutationReplayScopeV1 {
    pub operation: Repair2MutationOperation,
    #[serde(rename = "projectId")]
    pub project_id: Common4ProjectId,
    #[serde(rename = "requestId")]
    pub request_id: Common4RequestId,
    #[serde(rename = "schemaVersion")]
    pub schema_version: ExactInteger,
    #[serde(rename = "stepId")]
    pub step_id: Common4StepId,
}
///`Invocation5MutationResult`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation5MutationResult {
    #[serde(rename = "effectOutcome")]
    pub effect_outcome: Invocation5MutationResultEffectOutcome,
    pub kind: ::serde_json::Value,
    #[serde(rename = "receiptId")]
    pub receipt_id: Common4ReceiptId,
    pub replayed: bool,
}
///`Invocation5MutationResultEffectOutcome`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation5MutationResultEffectOutcome {
    #[serde(rename = "COMPLETED")]
    Completed,
    #[serde(rename = "FAILED")]
    Failed,
    #[serde(rename = "INDETERMINATE")]
    Indeterminate,
}
impl ::std::fmt::Display for Invocation5MutationResultEffectOutcome {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Completed => f.write_str("COMPLETED"),
            Self::Failed => f.write_str("FAILED"),
            Self::Indeterminate => f.write_str("INDETERMINATE"),
        }
    }
}
impl ::std::str::FromStr for Invocation5MutationResultEffectOutcome {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "COMPLETED" => Ok(Self::Completed),
            "FAILED" => Ok(Self::Failed),
            "INDETERMINATE" => Ok(Self::Indeterminate),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation5MutationResultEffectOutcome {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Invocation5MutationResultEffectOutcome {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Digest is raw SHA-256 of canonical retained native AuthorizedExecutionV2. The host verifies that preimage and its grant-set reference, then composes security admission for every owner before spawning. No Run; no automatic retry.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation5NativePreparationParams {
    #[serde(rename = "authorizationDescriptorDigest")]
    pub authorization_descriptor_digest: Common4Sha256Hex,
    pub kind: ::serde_json::Value,
    #[serde(rename = "securityGrantSetRef")]
    pub security_grant_set_ref: ::std::string::String,
}
///Completed preparation only: explicit execution receipt and admitted prepared import. Faults use step termination/journal, never this success record.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation5NativePreparationResult {
    #[serde(rename = "importId")]
    pub import_id: Common4ImportId,
    pub kind: ::serde_json::Value,
    #[serde(rename = "ownerCount")]
    pub owner_count: i64,
    #[serde(rename = "receiptId")]
    pub receipt_id: Common4ReceiptId,
}
///policy show: tracked policy and waiver documents resolved at the admitted trust-clock date (host observation, not a request field).
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation5PolicyShowRequestV1 {
    pub operation: ::serde_json::Value,
}
///policy test SUITE: suitePath names an evaluator3 PolicyTestSuiteV2 document (urn:opensip:product-v1:workflows:evaluator3:policy-test:2); a suite or candidate policy of another major is refused before evaluation.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation5PolicyTestRequestV1 {
    pub operation: ::serde_json::Value,
    #[serde(rename = "suitePath")]
    pub suite_path: Common4UserInputPath,
}
///A query step over one of the twenty public graph-query:3 operations; request is the complete admitted GraphQueryRequestV1 whose operation, completeness and page equal the step fields (cross-field join).
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation5PublicQueryParams {
    pub completeness: Invocation5PublicQueryParamsCompleteness,
    pub kind: ::serde_json::Value,
    pub operation: Graph4Operation,
    pub page: Graph4Page,
    pub request: Graph4GraphQueryRequestV1,
}
///`Invocation5PublicQueryParamsCompleteness`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation5PublicQueryParamsCompleteness {
    #[serde(rename = "required")]
    Required,
    #[serde(rename = "best-effort")]
    BestEffort,
}
impl ::std::fmt::Display for Invocation5PublicQueryParamsCompleteness {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Required => f.write_str("required"),
            Self::BestEffort => f.write_str("best-effort"),
        }
    }
}
impl ::std::str::FromStr for Invocation5PublicQueryParamsCompleteness {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "required" => Ok(Self::Required),
            "best-effort" => Ok(Self::BestEffort),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation5PublicQueryParamsCompleteness {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Invocation5PublicQueryParamsCompleteness {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Closed query-step params: public graph-query:3 operations or the closed host-only extension. The command->operation mapping is command-inventory:3 queryDispatch.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(untagged)]
pub enum Invocation5QueryParams {
    PublicQueryParams(Invocation5PublicQueryParams),
    HostQueryParams(Invocation5HostQueryParams),
    FitQueryFromAnalysisParams(Invocation5FitQueryFromAnalysisParams),
}
impl ::std::convert::From<Invocation5PublicQueryParams> for Invocation5QueryParams {
    fn from(value: Invocation5PublicQueryParams) -> Self {
        Self::PublicQueryParams(value)
    }
}
impl ::std::convert::From<Invocation5HostQueryParams> for Invocation5QueryParams {
    fn from(value: Invocation5HostQueryParams) -> Self {
        Self::HostQueryParams(value)
    }
}
impl ::std::convert::From<Invocation5FitQueryFromAnalysisParams>
for Invocation5QueryParams {
    fn from(value: Invocation5FitQueryFromAnalysisParams) -> Self {
        Self::FitQueryFromAnalysisParams(value)
    }
}
///`Invocation5QueryResult`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation5QueryResult {
    pub advisory: bool,
    #[serde(rename = "completenessMet")]
    pub completeness_met: bool,
    pub items: Common4Uint53,
    pub kind: ::serde_json::Value,
    #[serde(
        rename = "nextCursor",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub next_cursor: FieldPresence<
        ::std::option::Option<Invocation5QueryResultNextCursor>,
    >,
    pub truncated: bool,
}
///`Invocation5QueryResultNextCursor`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Invocation5QueryResultNextCursor(::std::string::String);
impl ::std::ops::Deref for Invocation5QueryResultNextCursor {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Invocation5QueryResultNextCursor> for ::std::string::String {
    fn from(value: Invocation5QueryResultNextCursor) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Invocation5QueryResultNextCursor {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 256usize {
            return Err("longer than 256 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Invocation5QueryResultNextCursor {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Invocation5QueryResultNextCursor {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Invocation5QueryResultNextCursor {
    fn deserialize<D>(deserializer: D) -> ::std::result::Result<Self, D::Error>
    where
        D: ::serde::Deserializer<'de>,
    {
        ::std::string::String::deserialize(deserializer)?
            .parse()
            .map_err(|e: self::error::ConversionError| {
                <D::Error as ::serde::de::Error>::custom(e.to_string())
            })
    }
}
///`Invocation5RenderParams`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation5RenderParams {
    pub destination: Invocation5RenderParamsDestination,
    pub format: Inventory3OutputFormat,
    pub kind: ::serde_json::Value,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub path: FieldPresence<::std::option::Option<Common4UserInputPath>>,
    ///true for the selected primary renderer: its failure after a committed Run is DELIVERY.REQUIRED_FAILED (exit 4) and never rewrites the Run
    pub required: bool,
    #[serde(rename = "sourceSteps")]
    pub source_steps: ::std::vec::Vec<Common4StepId>,
}
///`Invocation5RenderParamsDestination`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation5RenderParamsDestination {
    #[serde(rename = "stdout")]
    Stdout,
    #[serde(rename = "file")]
    File,
}
impl ::std::fmt::Display for Invocation5RenderParamsDestination {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Stdout => f.write_str("stdout"),
            Self::File => f.write_str("file"),
        }
    }
}
impl ::std::str::FromStr for Invocation5RenderParamsDestination {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "stdout" => Ok(Self::Stdout),
            "file" => Ok(Self::File),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation5RenderParamsDestination {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Invocation5RenderParamsDestination {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Invocation5RenderResult`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation5RenderResult {
    pub bytes: Common4Uint53,
    pub format: Inventory3OutputFormat,
    pub kind: ::serde_json::Value,
    #[serde(rename = "rendererVersion")]
    pub renderer_version: ::std::num::NonZeroU64,
    pub truncation: bool,
    pub written: bool,
}
///`Invocation5RepairApplyParams`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation5RepairApplyParams {
    #[serde(rename = "authorizationRef")]
    pub authorization_ref: Common4RepairAuthorizationRef,
    #[serde(rename = "consentSource")]
    pub consent_source: Invocation5RepairApplyParamsConsentSource,
    pub kind: ::serde_json::Value,
    #[serde(rename = "planStep")]
    pub plan_step: Common4StepId,
    ///must equal the plan step's result; apply is bound to the exact plan identity, not to the step
    #[serde(rename = "repairPlanId")]
    pub repair_plan_id: Common4RepairPlanId,
}
///`Invocation5RepairApplyParamsConsentSource`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation5RepairApplyParamsConsentSource {
    #[serde(rename = "policy")]
    Policy,
    #[serde(rename = "interactive")]
    Interactive,
}
impl ::std::fmt::Display for Invocation5RepairApplyParamsConsentSource {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Policy => f.write_str("policy"),
            Self::Interactive => f.write_str("interactive"),
        }
    }
}
impl ::std::str::FromStr for Invocation5RepairApplyParamsConsentSource {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "policy" => Ok(Self::Policy),
            "interactive" => Ok(Self::Interactive),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation5RepairApplyParamsConsentSource {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Invocation5RepairApplyParamsConsentSource {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Invocation5RepairApplyResult`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation5RepairApplyResult {
    #[serde(
        rename = "appliedSnapshotId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub applied_snapshot_id: FieldPresence<::std::option::Option<Common4SnapshotId>>,
    #[serde(rename = "effectOutcome")]
    pub effect_outcome: Invocation5RepairApplyResultEffectOutcome,
    #[serde(rename = "journalState")]
    pub journal_state: Repair2JournalState,
    pub kind: ::serde_json::Value,
    #[serde(rename = "receiptId")]
    pub receipt_id: Common4ReceiptId,
    pub rollback: Invocation5RepairApplyResultRollback,
}
///`Invocation5RepairApplyResultEffectOutcome`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation5RepairApplyResultEffectOutcome {
    #[serde(rename = "COMPLETED")]
    Completed,
    #[serde(rename = "FAILED")]
    Failed,
    #[serde(rename = "INDETERMINATE")]
    Indeterminate,
}
impl ::std::fmt::Display for Invocation5RepairApplyResultEffectOutcome {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Completed => f.write_str("COMPLETED"),
            Self::Failed => f.write_str("FAILED"),
            Self::Indeterminate => f.write_str("INDETERMINATE"),
        }
    }
}
impl ::std::str::FromStr for Invocation5RepairApplyResultEffectOutcome {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "COMPLETED" => Ok(Self::Completed),
            "FAILED" => Ok(Self::Failed),
            "INDETERMINATE" => Ok(Self::Indeterminate),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation5RepairApplyResultEffectOutcome {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Invocation5RepairApplyResultEffectOutcome {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Invocation5RepairApplyResultRollback`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation5RepairApplyResultRollback {
    #[serde(rename = "not-needed")]
    NotNeeded,
    #[serde(rename = "completed")]
    Completed,
    #[serde(rename = "blocked")]
    Blocked,
    #[serde(rename = "not-attempted")]
    NotAttempted,
}
impl ::std::fmt::Display for Invocation5RepairApplyResultRollback {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::NotNeeded => f.write_str("not-needed"),
            Self::Completed => f.write_str("completed"),
            Self::Blocked => f.write_str("blocked"),
            Self::NotAttempted => f.write_str("not-attempted"),
        }
    }
}
impl ::std::str::FromStr for Invocation5RepairApplyResultRollback {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "not-needed" => Ok(Self::NotNeeded),
            "completed" => Ok(Self::Completed),
            "blocked" => Ok(Self::Blocked),
            "not-attempted" => Ok(Self::NotAttempted),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation5RepairApplyResultRollback {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Invocation5RepairApplyResultRollback {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Invocation5RepairPreviewParams`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation5RepairPreviewParams {
    #[serde(rename = "evidenceSource")]
    pub evidence_source: Invocation5RepairPreviewParamsEvidenceSource,
    pub kind: ::serde_json::Value,
    pub recipe: Repair2RecipeRef,
    pub targets: ::std::vec::Vec<Common4Fingerprint>,
}
///`Invocation5RepairPreviewParamsEvidenceSource`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
pub enum Invocation5RepairPreviewParamsEvidenceSource {
    #[serde(rename = "step")]
    Step(Common4StepId),
    #[serde(rename = "runId")]
    RunId(Common4RunId),
}
impl ::std::convert::From<Common4StepId>
for Invocation5RepairPreviewParamsEvidenceSource {
    fn from(value: Common4StepId) -> Self {
        Self::Step(value)
    }
}
impl ::std::convert::From<Common4RunId>
for Invocation5RepairPreviewParamsEvidenceSource {
    fn from(value: Common4RunId) -> Self {
        Self::RunId(value)
    }
}
///`Invocation5RepairPreviewResult`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation5RepairPreviewResult {
    pub applicable: bool,
    pub kind: ::serde_json::Value,
    #[serde(rename = "repairPlanId")]
    pub repair_plan_id: Common4RepairPlanId,
    #[serde(rename = "snapshotId")]
    pub snapshot_id: Common4SnapshotId,
    #[serde(rename = "unmetPreconditions")]
    pub unmet_preconditions: ::std::vec::Vec<Common4DomainDetail>,
}
///Host-created after reading the exact apply journal and obtaining fresh security recovery admission. It binds the mutation step inputDescriptorDigest. All fields join the admitted authorization; inspection uses the query step and needs no authorization.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation5RepairRecoveryIntentV1 {
    #[serde(rename = "authorizationRef")]
    pub authorization_ref: Common4RepairRecoveryAuthorizationRef,
    #[serde(rename = "journalRef")]
    pub journal_ref: Common4RepairJournalRef,
    pub kind: ::serde_json::Value,
    #[serde(rename = "recoveryAction")]
    pub recovery_action: Invocation5RepairRecoveryIntentV1RecoveryAction,
    #[serde(rename = "repairPlanId")]
    pub repair_plan_id: Common4RepairPlanId,
    #[serde(rename = "schemaVersion")]
    pub schema_version: ExactInteger,
}
///`Invocation5RepairRecoveryIntentV1RecoveryAction`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation5RepairRecoveryIntentV1RecoveryAction {
    #[serde(rename = "discard-temps")]
    DiscardTemps,
    #[serde(rename = "roll-back-renamed")]
    RollBackRenamed,
    #[serde(rename = "verify-postimages-and-commit")]
    VerifyPostimagesAndCommit,
}
impl ::std::fmt::Display for Invocation5RepairRecoveryIntentV1RecoveryAction {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::DiscardTemps => f.write_str("discard-temps"),
            Self::RollBackRenamed => f.write_str("roll-back-renamed"),
            Self::VerifyPostimagesAndCommit => {
                f.write_str("verify-postimages-and-commit")
            }
        }
    }
}
impl ::std::str::FromStr for Invocation5RepairRecoveryIntentV1RecoveryAction {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "discard-temps" => Ok(Self::DiscardTemps),
            "roll-back-renamed" => Ok(Self::RollBackRenamed),
            "verify-postimages-and-commit" => Ok(Self::VerifyPostimagesAndCommit),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation5RepairRecoveryIntentV1RecoveryAction {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Invocation5RepairRecoveryIntentV1RecoveryAction {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Invocation5RetentionDisclosure`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation5RetentionDisclosure {
    #[serde(rename = "firstUse")]
    pub first_use: bool,
    pub policy: Invocation5RetentionDisclosurePolicy,
    pub provenance: Invocation5RetentionDisclosureProvenance,
    #[serde(rename = "storageRoot")]
    pub storage_root: Common4UserInputPath,
}
///`Invocation5RetentionDisclosurePolicy`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation5RetentionDisclosurePolicy {
    #[serde(rename = "durable-unbounded")]
    DurableUnbounded,
    #[serde(rename = "durable-bounded")]
    DurableBounded,
    #[serde(rename = "ephemeral")]
    Ephemeral,
}
impl ::std::fmt::Display for Invocation5RetentionDisclosurePolicy {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::DurableUnbounded => f.write_str("durable-unbounded"),
            Self::DurableBounded => f.write_str("durable-bounded"),
            Self::Ephemeral => f.write_str("ephemeral"),
        }
    }
}
impl ::std::str::FromStr for Invocation5RetentionDisclosurePolicy {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "durable-unbounded" => Ok(Self::DurableUnbounded),
            "durable-bounded" => Ok(Self::DurableBounded),
            "ephemeral" => Ok(Self::Ephemeral),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation5RetentionDisclosurePolicy {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Invocation5RetentionDisclosurePolicy {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Invocation5RetentionDisclosureProvenance`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation5RetentionDisclosureProvenance {
    #[serde(rename = "DEFAULTED")]
    Defaulted,
    #[serde(rename = "CONFIGURED")]
    Configured,
    #[serde(rename = "EXPLICIT-FLAG")]
    ExplicitFlag,
}
impl ::std::fmt::Display for Invocation5RetentionDisclosureProvenance {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Defaulted => f.write_str("DEFAULTED"),
            Self::Configured => f.write_str("CONFIGURED"),
            Self::ExplicitFlag => f.write_str("EXPLICIT-FLAG"),
        }
    }
}
impl ::std::str::FromStr for Invocation5RetentionDisclosureProvenance {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "DEFAULTED" => Ok(Self::Defaulted),
            "CONFIGURED" => Ok(Self::Configured),
            "EXPLICIT-FLAG" => Ok(Self::ExplicitFlag),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation5RetentionDisclosureProvenance {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Invocation5RetentionDisclosureProvenance {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///review brief [--producer model|heuristic]: model selects a ReviewerPrincipal of kind model with its admitted modelClosureId; heuristic selects kind policy-rule with id opensip.review.heuristic.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation5ReviewBriefProduceRequestV1 {
    pub operation: ::serde_json::Value,
    pub producer: Review2ReviewerPrincipal,
    pub view: Graph4View,
}
///Successor of invocation:3 adding required operational duration observations to terminal Attempt records. Timing has no Run identity, verdict, gating, retry, authority or D9 effect. Historical v3 is retained under its own schema and cannot be silently reclassified as v4. Joint unaccepted successor5 adds only the closed FitQueryFromAnalysisParams alternative. Host source-step, completion and private response joins are separate mandatory laws.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation5Root {
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub cancellation: FieldPresence<::std::option::Option<Invocation5Cancellation>>,
    #[serde(
        rename = "clientCorrelationId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub client_correlation_id: FieldPresence<
        ::std::option::Option<Invocation5RootClientCorrelationId>,
    >,
    pub mode: Invocation5Mode,
    #[serde(rename = "orderedSteps")]
    pub ordered_steps: ::std::vec::Vec<Invocation5StepSpec>,
    #[serde(
        rename = "projectId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub project_id: FieldPresence<::std::option::Option<Common4ProjectId>>,
    #[serde(rename = "requestId")]
    pub request_id: Common4RequestId,
    #[serde(
        rename = "retentionDisclosure",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub retention_disclosure: FieldPresence<
        ::std::option::Option<Invocation5RetentionDisclosure>,
    >,
    #[serde(rename = "schemaFamily")]
    pub schema_family: ::serde_json::Value,
    #[serde(rename = "schemaMajor")]
    pub schema_major: ExactInteger,
    #[serde(
        rename = "stepResults",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub step_results: FieldPresence<::std::vec::Vec<Invocation5StepResult>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub termination: FieldPresence<::std::option::Option<Common4StepTermination>>,
    #[serde(
        rename = "terminationEmitted",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub termination_emitted: FieldPresence<::std::option::Option<bool>>,
    pub workflow: Invocation5WorkflowRef,
}
///`Invocation5RootClientCorrelationId`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Invocation5RootClientCorrelationId(::std::string::String);
impl ::std::ops::Deref for Invocation5RootClientCorrelationId {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Invocation5RootClientCorrelationId> for ::std::string::String {
    fn from(value: Invocation5RootClientCorrelationId) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Invocation5RootClientCorrelationId {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 128usize {
            return Err("longer than 128 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Invocation5RootClientCorrelationId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Invocation5RootClientCorrelationId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Invocation5RootClientCorrelationId {
    fn deserialize<D>(deserializer: D) -> ::std::result::Result<Self, D::Error>
    where
        D: ::serde::Deserializer<'de>,
    {
        ::std::string::String::deserialize(deserializer)?
            .parse()
            .map_err(|e: self::error::ConversionError| {
                <D::Error as ::serde::de::Error>::custom(e.to_string())
            })
    }
}
///`Invocation5StepDomainResult`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(untagged)]
pub enum Invocation5StepDomainResult {
    AnalysisResult(Invocation5AnalysisResult),
    ComparisonStepResult(Invocation5ComparisonStepResult),
    QueryResult(Invocation5QueryResult),
    RenderResult(Invocation5RenderResult),
    ImportResult(Invocation5ImportResult),
    RepairPreviewResult(Invocation5RepairPreviewResult),
    RepairApplyResult(Invocation5RepairApplyResult),
    TestExecutionResult(Invocation5TestExecutionResult),
    MutationResult(Invocation5MutationResult),
    ExportDeliveryResult(Invocation5ExportDeliveryResult),
    DoctorResult(Invocation5DoctorResult),
    NativePreparationResult(Invocation5NativePreparationResult),
}
impl ::std::convert::From<Invocation5AnalysisResult> for Invocation5StepDomainResult {
    fn from(value: Invocation5AnalysisResult) -> Self {
        Self::AnalysisResult(value)
    }
}
impl ::std::convert::From<Invocation5ComparisonStepResult>
for Invocation5StepDomainResult {
    fn from(value: Invocation5ComparisonStepResult) -> Self {
        Self::ComparisonStepResult(value)
    }
}
impl ::std::convert::From<Invocation5QueryResult> for Invocation5StepDomainResult {
    fn from(value: Invocation5QueryResult) -> Self {
        Self::QueryResult(value)
    }
}
impl ::std::convert::From<Invocation5RenderResult> for Invocation5StepDomainResult {
    fn from(value: Invocation5RenderResult) -> Self {
        Self::RenderResult(value)
    }
}
impl ::std::convert::From<Invocation5ImportResult> for Invocation5StepDomainResult {
    fn from(value: Invocation5ImportResult) -> Self {
        Self::ImportResult(value)
    }
}
impl ::std::convert::From<Invocation5RepairPreviewResult>
for Invocation5StepDomainResult {
    fn from(value: Invocation5RepairPreviewResult) -> Self {
        Self::RepairPreviewResult(value)
    }
}
impl ::std::convert::From<Invocation5RepairApplyResult> for Invocation5StepDomainResult {
    fn from(value: Invocation5RepairApplyResult) -> Self {
        Self::RepairApplyResult(value)
    }
}
impl ::std::convert::From<Invocation5TestExecutionResult>
for Invocation5StepDomainResult {
    fn from(value: Invocation5TestExecutionResult) -> Self {
        Self::TestExecutionResult(value)
    }
}
impl ::std::convert::From<Invocation5MutationResult> for Invocation5StepDomainResult {
    fn from(value: Invocation5MutationResult) -> Self {
        Self::MutationResult(value)
    }
}
impl ::std::convert::From<Invocation5ExportDeliveryResult>
for Invocation5StepDomainResult {
    fn from(value: Invocation5ExportDeliveryResult) -> Self {
        Self::ExportDeliveryResult(value)
    }
}
impl ::std::convert::From<Invocation5DoctorResult> for Invocation5StepDomainResult {
    fn from(value: Invocation5DoctorResult) -> Self {
        Self::DoctorResult(value)
    }
}
impl ::std::convert::From<Invocation5NativePreparationResult>
for Invocation5StepDomainResult {
    fn from(value: Invocation5NativePreparationResult) -> Self {
        Self::NativePreparationResult(value)
    }
}
///comparison: the audit verdict step. It consumes the current analysis Run (currentStep) and a baseline artifact, mints no Run, and is the ONLY step whose verdict gates an audit; the analysis it consumes participates in the aggregate for completion, operational faults and required-coverage indeterminacy only (verdictGate=delegated).
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation5StepKind {
    #[serde(rename = "analysis")]
    Analysis,
    #[serde(rename = "verify")]
    Verify,
    #[serde(rename = "comparison")]
    Comparison,
    #[serde(rename = "query")]
    Query,
    #[serde(rename = "render")]
    Render,
    #[serde(rename = "import")]
    Import,
    #[serde(rename = "repair-preview")]
    RepairPreview,
    #[serde(rename = "repair-apply")]
    RepairApply,
    #[serde(rename = "test-execution")]
    TestExecution,
    #[serde(rename = "mutation")]
    Mutation,
    #[serde(rename = "export-delivery")]
    ExportDelivery,
    #[serde(rename = "doctor")]
    Doctor,
    #[serde(rename = "native-preparation")]
    NativePreparation,
}
impl ::std::fmt::Display for Invocation5StepKind {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Analysis => f.write_str("analysis"),
            Self::Verify => f.write_str("verify"),
            Self::Comparison => f.write_str("comparison"),
            Self::Query => f.write_str("query"),
            Self::Render => f.write_str("render"),
            Self::Import => f.write_str("import"),
            Self::RepairPreview => f.write_str("repair-preview"),
            Self::RepairApply => f.write_str("repair-apply"),
            Self::TestExecution => f.write_str("test-execution"),
            Self::Mutation => f.write_str("mutation"),
            Self::ExportDelivery => f.write_str("export-delivery"),
            Self::Doctor => f.write_str("doctor"),
            Self::NativePreparation => f.write_str("native-preparation"),
        }
    }
}
impl ::std::str::FromStr for Invocation5StepKind {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "analysis" => Ok(Self::Analysis),
            "verify" => Ok(Self::Verify),
            "comparison" => Ok(Self::Comparison),
            "query" => Ok(Self::Query),
            "render" => Ok(Self::Render),
            "import" => Ok(Self::Import),
            "repair-preview" => Ok(Self::RepairPreview),
            "repair-apply" => Ok(Self::RepairApply),
            "test-execution" => Ok(Self::TestExecution),
            "mutation" => Ok(Self::Mutation),
            "export-delivery" => Ok(Self::ExportDelivery),
            "doctor" => Ok(Self::Doctor),
            "native-preparation" => Ok(Self::NativePreparation),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation5StepKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Invocation5StepKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///completed: the step reached its own terminal domain result (an analysis verdict of fail or indeterminate is still completed). rejected: admission or precondition refusal. failed: operational fault. skipped: a dependency did not satisfy the gate. cancelled: cancellation arrived before a terminal result. abandoned: assigned only by crash recovery to a non-terminal step whose supervisor died.
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation5StepOutcome {
    #[serde(rename = "completed")]
    Completed,
    #[serde(rename = "rejected")]
    Rejected,
    #[serde(rename = "failed")]
    Failed,
    #[serde(rename = "skipped")]
    Skipped,
    #[serde(rename = "cancelled")]
    Cancelled,
    #[serde(rename = "abandoned")]
    Abandoned,
}
impl ::std::fmt::Display for Invocation5StepOutcome {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Completed => f.write_str("completed"),
            Self::Rejected => f.write_str("rejected"),
            Self::Failed => f.write_str("failed"),
            Self::Skipped => f.write_str("skipped"),
            Self::Cancelled => f.write_str("cancelled"),
            Self::Abandoned => f.write_str("abandoned"),
        }
    }
}
impl ::std::str::FromStr for Invocation5StepOutcome {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "completed" => Ok(Self::Completed),
            "rejected" => Ok(Self::Rejected),
            "failed" => Ok(Self::Failed),
            "skipped" => Ok(Self::Skipped),
            "cancelled" => Ok(Self::Cancelled),
            "abandoned" => Ok(Self::Abandoned),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation5StepOutcome {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Invocation5StepOutcome {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Invocation5StepParams`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(untagged)]
pub enum Invocation5StepParams {
    AnalysisParams(Invocation5AnalysisParams),
    VerifyParams(Invocation5VerifyParams),
    ComparisonParams(Invocation5ComparisonParams),
    QueryParams(Invocation5QueryParams),
    RenderParams(Invocation5RenderParams),
    ImportParams(Invocation5ImportParams),
    RepairPreviewParams(Invocation5RepairPreviewParams),
    RepairApplyParams(Invocation5RepairApplyParams),
    TestExecutionParams(Invocation5TestExecutionParams),
    MutationParams(Invocation5MutationParams),
    ExportDeliveryParams(Invocation5ExportDeliveryParams),
    DoctorParams(Invocation5DoctorParams),
    NativePreparationParams(Invocation5NativePreparationParams),
}
impl ::std::convert::From<Invocation5AnalysisParams> for Invocation5StepParams {
    fn from(value: Invocation5AnalysisParams) -> Self {
        Self::AnalysisParams(value)
    }
}
impl ::std::convert::From<Invocation5VerifyParams> for Invocation5StepParams {
    fn from(value: Invocation5VerifyParams) -> Self {
        Self::VerifyParams(value)
    }
}
impl ::std::convert::From<Invocation5ComparisonParams> for Invocation5StepParams {
    fn from(value: Invocation5ComparisonParams) -> Self {
        Self::ComparisonParams(value)
    }
}
impl ::std::convert::From<Invocation5QueryParams> for Invocation5StepParams {
    fn from(value: Invocation5QueryParams) -> Self {
        Self::QueryParams(value)
    }
}
impl ::std::convert::From<Invocation5RenderParams> for Invocation5StepParams {
    fn from(value: Invocation5RenderParams) -> Self {
        Self::RenderParams(value)
    }
}
impl ::std::convert::From<Invocation5ImportParams> for Invocation5StepParams {
    fn from(value: Invocation5ImportParams) -> Self {
        Self::ImportParams(value)
    }
}
impl ::std::convert::From<Invocation5RepairPreviewParams> for Invocation5StepParams {
    fn from(value: Invocation5RepairPreviewParams) -> Self {
        Self::RepairPreviewParams(value)
    }
}
impl ::std::convert::From<Invocation5RepairApplyParams> for Invocation5StepParams {
    fn from(value: Invocation5RepairApplyParams) -> Self {
        Self::RepairApplyParams(value)
    }
}
impl ::std::convert::From<Invocation5TestExecutionParams> for Invocation5StepParams {
    fn from(value: Invocation5TestExecutionParams) -> Self {
        Self::TestExecutionParams(value)
    }
}
impl ::std::convert::From<Invocation5MutationParams> for Invocation5StepParams {
    fn from(value: Invocation5MutationParams) -> Self {
        Self::MutationParams(value)
    }
}
impl ::std::convert::From<Invocation5ExportDeliveryParams> for Invocation5StepParams {
    fn from(value: Invocation5ExportDeliveryParams) -> Self {
        Self::ExportDeliveryParams(value)
    }
}
impl ::std::convert::From<Invocation5DoctorParams> for Invocation5StepParams {
    fn from(value: Invocation5DoctorParams) -> Self {
        Self::DoctorParams(value)
    }
}
impl ::std::convert::From<Invocation5NativePreparationParams> for Invocation5StepParams {
    fn from(value: Invocation5NativePreparationParams) -> Self {
        Self::NativePreparationParams(value)
    }
}
///`Invocation5StepResult`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation5StepResult {
    pub attempts: ::std::vec::Vec<Invocation5Attempt>,
    pub outcome: Invocation5StepOutcome,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub result: FieldPresence<::std::option::Option<Invocation5StepDomainResult>>,
    #[serde(
        rename = "skipReason",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub skip_reason: FieldPresence<
        ::std::option::Option<Invocation5StepResultSkipReason>,
    >,
    #[serde(rename = "stepId")]
    pub step_id: Common4StepId,
    pub termination: Common4StepTermination,
}
///`Invocation5StepResultPropertiesSkipReason`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation5StepResultPropertiesSkipReason {
    #[serde(rename = "dependency-not-completed")]
    DependencyNotCompleted,
    #[serde(rename = "dependency-not-terminal")]
    DependencyNotTerminal,
    #[serde(rename = "dependency-cancelled")]
    DependencyCancelled,
}
impl ::std::fmt::Display for Invocation5StepResultPropertiesSkipReason {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::DependencyNotCompleted => f.write_str("dependency-not-completed"),
            Self::DependencyNotTerminal => f.write_str("dependency-not-terminal"),
            Self::DependencyCancelled => f.write_str("dependency-cancelled"),
        }
    }
}
impl ::std::str::FromStr for Invocation5StepResultPropertiesSkipReason {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "dependency-not-completed" => Ok(Self::DependencyNotCompleted),
            "dependency-not-terminal" => Ok(Self::DependencyNotTerminal),
            "dependency-cancelled" => Ok(Self::DependencyCancelled),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation5StepResultPropertiesSkipReason {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Invocation5StepResultPropertiesSkipReason {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Invocation5StepResultSkipReason`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation5StepResultSkipReason {
    #[serde(rename = "dependency-not-completed")]
    DependencyNotCompleted,
    #[serde(rename = "dependency-not-terminal")]
    DependencyNotTerminal,
    #[serde(rename = "dependency-cancelled")]
    DependencyCancelled,
}
impl ::std::fmt::Display for Invocation5StepResultSkipReason {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::DependencyNotCompleted => f.write_str("dependency-not-completed"),
            Self::DependencyNotTerminal => f.write_str("dependency-not-terminal"),
            Self::DependencyCancelled => f.write_str("dependency-cancelled"),
        }
    }
}
impl ::std::str::FromStr for Invocation5StepResultSkipReason {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "dependency-not-completed" => Ok(Self::DependencyNotCompleted),
            "dependency-not-terminal" => Ok(Self::DependencyNotTerminal),
            "dependency-cancelled" => Ok(Self::DependencyCancelled),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation5StepResultSkipReason {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Invocation5StepResultSkipReason {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Invocation5StepSpec`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation5StepSpec {
    ///completed: every dependency outcome must be completed. terminal: every dependency must have reached any terminal outcome; used only by render/export-delivery steps that project whatever happened.
    #[serde(rename = "dependencyGate")]
    pub dependency_gate: Invocation5StepSpecDependencyGate,
    ///every entry is a lower stepId (acyclic by construction; a forward or self reference is WORKFLOW.DEPENDENCY_CYCLE)
    #[serde(rename = "dependsOn")]
    pub depends_on: ::std::vec::Vec<Common4StepId>,
    pub kind: Invocation5StepKind,
    pub params: Invocation5StepParams,
    ///required steps determine the aggregate termination; an optional step's rejection/failure never changes it. A required step may not depend on an optional step (WORKFLOW.REQUIRED_DEPENDS_ON_OPTIONAL, request-rejected).
    pub requirement: Invocation5StepSpecRequirement,
    ///idempotent-retry is lawful only for analysis, verify, query, render, doctor and export-delivery and only for faultCause ledger-busy; at most 3 attempts in total. Mutation, import, repair-preview, repair-apply and test-execution are never implicitly retried.
    #[serde(rename = "retryPolicy")]
    pub retry_policy: Invocation5StepSpecRetryPolicy,
    #[serde(rename = "stepId")]
    pub step_id: Common4StepId,
}
///completed: every dependency outcome must be completed. terminal: every dependency must have reached any terminal outcome; used only by render/export-delivery steps that project whatever happened.
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation5StepSpecDependencyGate {
    #[serde(rename = "completed")]
    Completed,
    #[serde(rename = "terminal")]
    Terminal,
}
impl ::std::fmt::Display for Invocation5StepSpecDependencyGate {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Completed => f.write_str("completed"),
            Self::Terminal => f.write_str("terminal"),
        }
    }
}
impl ::std::str::FromStr for Invocation5StepSpecDependencyGate {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "completed" => Ok(Self::Completed),
            "terminal" => Ok(Self::Terminal),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation5StepSpecDependencyGate {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Invocation5StepSpecDependencyGate {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///completed: every dependency outcome must be completed. terminal: every dependency must have reached any terminal outcome; used only by render/export-delivery steps that project whatever happened.
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation5StepSpecPropertiesDependencyGate {
    #[serde(rename = "completed")]
    Completed,
    #[serde(rename = "terminal")]
    Terminal,
}
impl ::std::fmt::Display for Invocation5StepSpecPropertiesDependencyGate {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Completed => f.write_str("completed"),
            Self::Terminal => f.write_str("terminal"),
        }
    }
}
impl ::std::str::FromStr for Invocation5StepSpecPropertiesDependencyGate {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "completed" => Ok(Self::Completed),
            "terminal" => Ok(Self::Terminal),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation5StepSpecPropertiesDependencyGate {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Invocation5StepSpecPropertiesDependencyGate {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///every entry is a lower stepId (acyclic by construction; a forward or self reference is WORKFLOW.DEPENDENCY_CYCLE)
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(transparent)]
pub struct Invocation5StepSpecPropertiesDependsOn(pub ::std::vec::Vec<Common4StepId>);
impl ::std::ops::Deref for Invocation5StepSpecPropertiesDependsOn {
    type Target = ::std::vec::Vec<Common4StepId>;
    fn deref(&self) -> &::std::vec::Vec<Common4StepId> {
        &self.0
    }
}
impl ::std::convert::From<::std::vec::Vec<Common4StepId>>
for Invocation5StepSpecPropertiesDependsOn {
    fn from(value: ::std::vec::Vec<Common4StepId>) -> Self {
        Self(value)
    }
}
///required steps determine the aggregate termination; an optional step's rejection/failure never changes it. A required step may not depend on an optional step (WORKFLOW.REQUIRED_DEPENDS_ON_OPTIONAL, request-rejected).
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation5StepSpecPropertiesRequirement {
    #[serde(rename = "required")]
    Required,
    #[serde(rename = "optional")]
    Optional,
}
impl ::std::fmt::Display for Invocation5StepSpecPropertiesRequirement {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Required => f.write_str("required"),
            Self::Optional => f.write_str("optional"),
        }
    }
}
impl ::std::str::FromStr for Invocation5StepSpecPropertiesRequirement {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "required" => Ok(Self::Required),
            "optional" => Ok(Self::Optional),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation5StepSpecPropertiesRequirement {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Invocation5StepSpecPropertiesRequirement {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///required steps determine the aggregate termination; an optional step's rejection/failure never changes it. A required step may not depend on an optional step (WORKFLOW.REQUIRED_DEPENDS_ON_OPTIONAL, request-rejected).
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation5StepSpecRequirement {
    #[serde(rename = "required")]
    Required,
    #[serde(rename = "optional")]
    Optional,
}
impl ::std::fmt::Display for Invocation5StepSpecRequirement {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Required => f.write_str("required"),
            Self::Optional => f.write_str("optional"),
        }
    }
}
impl ::std::str::FromStr for Invocation5StepSpecRequirement {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "required" => Ok(Self::Required),
            "optional" => Ok(Self::Optional),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation5StepSpecRequirement {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Invocation5StepSpecRequirement {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///idempotent-retry is lawful only for analysis, verify, query, render, doctor and export-delivery and only for faultCause ledger-busy; at most 3 attempts in total. Mutation, import, repair-preview, repair-apply and test-execution are never implicitly retried.
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Invocation5StepSpecRetryPolicy {
    #[serde(rename = "idempotent-retry")]
    IdempotentRetry,
    #[serde(rename = "none")]
    None,
}
impl ::std::fmt::Display for Invocation5StepSpecRetryPolicy {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::IdempotentRetry => f.write_str("idempotent-retry"),
            Self::None => f.write_str("none"),
        }
    }
}
impl ::std::str::FromStr for Invocation5StepSpecRetryPolicy {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "idempotent-retry" => Ok(Self::IdempotentRetry),
            "none" => Ok(Self::None),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Invocation5StepSpecRetryPolicy {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Invocation5StepSpecRetryPolicy {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Invocation5TestExecutionParams`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(transparent)]
pub struct Invocation5TestExecutionParams(pub TestExecution1TestExecutionStepParams);
impl ::std::ops::Deref for Invocation5TestExecutionParams {
    type Target = TestExecution1TestExecutionStepParams;
    fn deref(&self) -> &TestExecution1TestExecutionStepParams {
        &self.0
    }
}
impl ::std::convert::From<Invocation5TestExecutionParams>
for TestExecution1TestExecutionStepParams {
    fn from(value: Invocation5TestExecutionParams) -> Self {
        value.0
    }
}
impl ::std::convert::From<TestExecution1TestExecutionStepParams>
for Invocation5TestExecutionParams {
    fn from(value: TestExecution1TestExecutionStepParams) -> Self {
        Self(value)
    }
}
///`Invocation5TestExecutionResult`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(transparent)]
pub struct Invocation5TestExecutionResult(pub TestExecution1TestExecutionStepResult);
impl ::std::ops::Deref for Invocation5TestExecutionResult {
    type Target = TestExecution1TestExecutionStepResult;
    fn deref(&self) -> &TestExecution1TestExecutionStepResult {
        &self.0
    }
}
impl ::std::convert::From<Invocation5TestExecutionResult>
for TestExecution1TestExecutionStepResult {
    fn from(value: Invocation5TestExecutionResult) -> Self {
        value.0
    }
}
impl ::std::convert::From<TestExecution1TestExecutionStepResult>
for Invocation5TestExecutionResult {
    fn from(value: TestExecution1TestExecutionStepResult) -> Self {
        Self(value)
    }
}
///`Invocation5VerificationOutcome`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation5VerificationOutcome {
    #[serde(rename = "appliedSnapshotId")]
    pub applied_snapshot_id: Common4SnapshotId,
    #[serde(rename = "netNewFindings")]
    pub net_new_findings: Common4Uint53,
    #[serde(rename = "snapshotMatched")]
    pub snapshot_matched: bool,
    #[serde(rename = "targetsRemaining")]
    pub targets_remaining: Common4Uint53,
    #[serde(rename = "verifiedSnapshotId")]
    pub verified_snapshot_id: Common4SnapshotId,
}
///`Invocation5VerifyParams`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Invocation5VerifyParams {
    ///the repair-apply step whose appliedSnapshotId the fresh snapshot must equal; verify always resnapshots and always seals a new authoritative Run
    #[serde(rename = "afterStep")]
    pub after_step: Common4StepId,
    #[serde(
        rename = "importedEvidenceSteps",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub imported_evidence_steps: FieldPresence<
        ::std::option::Option<::std::vec::Vec<Common4StepId>>,
    >,
    pub kind: ::serde_json::Value,
    pub profile: Inventory3AnalysisProfile,
}
///`Invocation5WorkflowRef`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(tag = "kind", deny_unknown_fields)]
pub enum Invocation5WorkflowRef {
    #[serde(rename = "builtin")]
    Builtin { name: Inventory3CommandName },
    #[serde(rename = "profile")]
    Profile {
        #[serde(rename = "activationId")]
        activation_id: Common4CanonicalIdentifier,
        #[serde(rename = "contributionId")]
        contribution_id: Common4ContributionId,
        #[serde(rename = "profileVersion")]
        profile_version: Common4SemanticVersion,
    },
}
///Closed current test-execution vocabulary. Membership is necessary, not sufficient: each effect value must equal the selected security permission truth-table profile row for the platform (permission-truth-tables.v9 through security-and-lifecycle S10, child-process execution mode), otherwise TEST.CONFINEMENT_CLAIM_REFUSED. That profile has no measured platform-primitive row, so ENFORCED-PLATFORM:<primitiveId> cannot be claimed and is not a member. Security EnforcementV1 retains that future vocabulary; admitting it here requires a successor truth-table profile with a measured primitive and a successor of this schema.
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum TestExecution1EnforcementValue {
    #[serde(rename = "DISCLOSURE-ONLY")]
    DisclosureOnly,
    #[serde(rename = "ENFORCED-BY-CONSTRUCTION")]
    EnforcedByConstruction,
    #[serde(rename = "ENFORCED-AT-HOST-BROKER")]
    EnforcedAtHostBroker,
}
impl ::std::fmt::Display for TestExecution1EnforcementValue {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::DisclosureOnly => f.write_str("DISCLOSURE-ONLY"),
            Self::EnforcedByConstruction => f.write_str("ENFORCED-BY-CONSTRUCTION"),
            Self::EnforcedAtHostBroker => f.write_str("ENFORCED-AT-HOST-BROKER"),
        }
    }
}
impl ::std::str::FromStr for TestExecution1EnforcementValue {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "DISCLOSURE-ONLY" => Ok(Self::DisclosureOnly),
            "ENFORCED-BY-CONSTRUCTION" => Ok(Self::EnforcedByConstruction),
            "ENFORCED-AT-HOST-BROKER" => Ok(Self::EnforcedAtHostBroker),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for TestExecution1EnforcementValue {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for TestExecution1EnforcementValue {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Repository code execution is disabled by default. A test-execution step is admitted only when selected explicitly, the security unit admits a RepoExecutionGrantV2 with principal P-TRUSTED-REPO and executionClass test-runner bound to this projectId, snapshot digest and the exact argv digest (expiry operation-end, never inherited), and CI mode uses a pre-existing policy record rather than interactive consent. The host spawns the exact argv with no shell: argv[0] is either a LogicalPath member of the sealed snapshot or a member of the declared toolchain closure2; the environment is constructed from the allowlist only; cwd is a LogicalPath inside the project root. The host DISCLOSES network and process reach (copied from the security unit's platform truth table); it does not confine them and refuses any step that claims it does. The outcome is evidence (an import2 wrapper with kind=test), never Coverage and never a verdict.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(transparent)]
pub struct TestExecution1Root(pub ::serde_json::Value);
impl ::std::ops::Deref for TestExecution1Root {
    type Target = ::serde_json::Value;
    fn deref(&self) -> &::serde_json::Value {
        &self.0
    }
}
impl ::std::convert::From<TestExecution1Root> for ::serde_json::Value {
    fn from(value: TestExecution1Root) -> Self {
        value.0
    }
}
impl ::std::convert::From<::serde_json::Value> for TestExecution1Root {
    fn from(value: ::serde_json::Value) -> Self {
        Self(value)
    }
}
///`TestExecution1TestExecutionStepParams`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct TestExecution1TestExecutionStepParams {
    ///the analysis, verify or repair-apply step whose (applied) snapshot the tests run against; the live tree must still equal that snapshot at spawn
    #[serde(rename = "afterStep")]
    pub after_step: Common1StepId,
    ///exact argument vector; no shell, no interpolation, no PATH search
    pub argv: ::std::vec::Vec<TestExecution1TestExecutionStepParamsArgvItem>,
    #[serde(rename = "argv0Source")]
    pub argv0_source: TestExecution1TestExecutionStepParamsArgv0Source,
    ///Exact host-admitted v2 grant reference; must equal the admitted projection reference as well as binding argv, project, snapshot, class and platform.
    #[serde(rename = "authorizationRef")]
    pub authorization_ref: ::std::string::String,
    ///CI mode requires pre-existing-policy; interactive consent in CI is TEST.INTERACTIVE_CONSENT_IN_CI (request-rejected)
    #[serde(rename = "consentSource")]
    pub consent_source: TestExecution1TestExecutionStepParamsConsentSource,
    ///project-relative working directory inside the sealed root; present exactly when cwdIsRoot is false
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub cwd: FieldPresence<::std::option::Option<Common1LogicalPath>>,
    ///true: the working directory is the project root itself and cwd is absent ('.' is not a LogicalPath)
    #[serde(rename = "cwdIsRoot")]
    pub cwd_is_root: bool,
    pub effects: TestExecution1TestExecutionStepParamsEffects,
    ///variables copied from the invoking environment; everything else is absent; PATH is never copied and is set to the declared toolchain closure only
    #[serde(rename = "environmentAllowlist")]
    pub environment_allowlist: ::std::vec::Vec<
        TestExecution1TestExecutionStepParamsEnvironmentAllowlistItem,
    >,
    #[serde(rename = "executionClass")]
    pub execution_class: ::serde_json::Value,
    pub kind: ::serde_json::Value,
    #[serde(rename = "maxOutputBytes")]
    pub max_output_bytes: ::std::num::NonZeroU64,
    ///security S8 platform; every effects value must EQUAL the security owner's truth-table row for this platform (S10), copied verbatim
    #[serde(rename = "platformId")]
    pub platform_id: TestExecution1TestExecutionStepParamsPlatformId,
    ///display label only. It maps to security principalClass 'repository-code' (RepoExecutionGrantV2) and to the foundation semantic-grant principal kind 'trusted-repository-code'; the grant record, not this label, is the authority
    pub principal: ::serde_json::Value,
    #[serde(rename = "timeoutMilliseconds")]
    pub timeout_milliseconds: ::std::num::NonZeroU64,
}
///`TestExecution1TestExecutionStepParamsArgv0Source`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(tag = "kind", deny_unknown_fields)]
pub enum TestExecution1TestExecutionStepParamsArgv0Source {
    #[serde(rename = "snapshot-member")]
    SnapshotMember { path: Common1LogicalPath },
    ///argv[0] must be byte-equal to member, member must be an inventoried tree entry of the admitted closure2, and the closure must be the declared toolchain of the grant; an alias, a PATH lookup, a symlink or a member of another closure is TEST.ARGV_NOT_IN_CLOSURE
    #[serde(rename = "toolchain-closure")]
    ToolchainClosure {
        #[serde(rename = "closureId")]
        closure_id: Common1ClosureId,
        member: Common1LogicalPath,
    },
}
///`TestExecution1TestExecutionStepParamsArgvItem`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct TestExecution1TestExecutionStepParamsArgvItem(::std::string::String);
impl ::std::ops::Deref for TestExecution1TestExecutionStepParamsArgvItem {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<TestExecution1TestExecutionStepParamsArgvItem>
for ::std::string::String {
    fn from(value: TestExecution1TestExecutionStepParamsArgvItem) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for TestExecution1TestExecutionStepParamsArgvItem {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 4096usize {
            return Err("longer than 4096 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for TestExecution1TestExecutionStepParamsArgvItem {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for TestExecution1TestExecutionStepParamsArgvItem {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for TestExecution1TestExecutionStepParamsArgvItem {
    fn deserialize<D>(deserializer: D) -> ::std::result::Result<Self, D::Error>
    where
        D: ::serde::Deserializer<'de>,
    {
        ::std::string::String::deserialize(deserializer)?
            .parse()
            .map_err(|e: self::error::ConversionError| {
                <D::Error as ::serde::de::Error>::custom(e.to_string())
            })
    }
}
///CI mode requires pre-existing-policy; interactive consent in CI is TEST.INTERACTIVE_CONSENT_IN_CI (request-rejected)
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum TestExecution1TestExecutionStepParamsConsentSource {
    #[serde(rename = "pre-existing-policy")]
    PreExistingPolicy,
    #[serde(rename = "interactive-consent")]
    InteractiveConsent,
}
impl ::std::fmt::Display for TestExecution1TestExecutionStepParamsConsentSource {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::PreExistingPolicy => f.write_str("pre-existing-policy"),
            Self::InteractiveConsent => f.write_str("interactive-consent"),
        }
    }
}
impl ::std::str::FromStr for TestExecution1TestExecutionStepParamsConsentSource {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "pre-existing-policy" => Ok(Self::PreExistingPolicy),
            "interactive-consent" => Ok(Self::InteractiveConsent),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str>
for TestExecution1TestExecutionStepParamsConsentSource {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for TestExecution1TestExecutionStepParamsConsentSource {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`TestExecution1TestExecutionStepParamsEffects`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct TestExecution1TestExecutionStepParamsEffects {
    pub environment: TestExecution1EnforcementValue,
    #[serde(rename = "filesystemWrite")]
    pub filesystem_write: TestExecution1EnforcementValue,
    pub network: TestExecution1EnforcementValue,
    pub subprocess: TestExecution1EnforcementValue,
}
///`TestExecution1TestExecutionStepParamsEnvironmentAllowlistItem`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct TestExecution1TestExecutionStepParamsEnvironmentAllowlistItem(
    ::std::string::String,
);
impl ::std::ops::Deref
for TestExecution1TestExecutionStepParamsEnvironmentAllowlistItem {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<TestExecution1TestExecutionStepParamsEnvironmentAllowlistItem>
for ::std::string::String {
    fn from(
        value: TestExecution1TestExecutionStepParamsEnvironmentAllowlistItem,
    ) -> Self {
        value.0
    }
}
impl ::std::str::FromStr
for TestExecution1TestExecutionStepParamsEnvironmentAllowlistItem {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 128usize {
            return Err("longer than 128 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str>
for TestExecution1TestExecutionStepParamsEnvironmentAllowlistItem {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for TestExecution1TestExecutionStepParamsEnvironmentAllowlistItem {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de>
for TestExecution1TestExecutionStepParamsEnvironmentAllowlistItem {
    fn deserialize<D>(deserializer: D) -> ::std::result::Result<Self, D::Error>
    where
        D: ::serde::Deserializer<'de>,
    {
        ::std::string::String::deserialize(deserializer)?
            .parse()
            .map_err(|e: self::error::ConversionError| {
                <D::Error as ::serde::de::Error>::custom(e.to_string())
            })
    }
}
///security S8 platform; every effects value must EQUAL the security owner's truth-table row for this platform (S10), copied verbatim
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum TestExecution1TestExecutionStepParamsPlatformId {
    #[serde(rename = "macos-aarch64")]
    MacosAarch64,
    #[serde(rename = "macos-x86_64")]
    MacosX8664,
    #[serde(rename = "linux-x86_64-gnu")]
    LinuxX8664Gnu,
    #[serde(rename = "linux-aarch64-gnu")]
    LinuxAarch64Gnu,
}
impl ::std::fmt::Display for TestExecution1TestExecutionStepParamsPlatformId {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::MacosAarch64 => f.write_str("macos-aarch64"),
            Self::MacosX8664 => f.write_str("macos-x86_64"),
            Self::LinuxX8664Gnu => f.write_str("linux-x86_64-gnu"),
            Self::LinuxAarch64Gnu => f.write_str("linux-aarch64-gnu"),
        }
    }
}
impl ::std::str::FromStr for TestExecution1TestExecutionStepParamsPlatformId {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "macos-aarch64" => Ok(Self::MacosAarch64),
            "macos-x86_64" => Ok(Self::MacosX8664),
            "linux-x86_64-gnu" => Ok(Self::LinuxX8664Gnu),
            "linux-aarch64-gnu" => Ok(Self::LinuxAarch64Gnu),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for TestExecution1TestExecutionStepParamsPlatformId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for TestExecution1TestExecutionStepParamsPlatformId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`TestExecution1TestExecutionStepResult`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct TestExecution1TestExecutionStepResult {
    #[serde(rename = "disclosureEmitted")]
    pub disclosure_emitted: ::serde_json::Value,
    #[serde(
        rename = "exitStatus",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub exit_status: FieldPresence<::std::option::Option<u8>>,
    #[serde(rename = "importId")]
    pub import_id: Common1ImportId,
    pub kind: ::serde_json::Value,
    #[serde(rename = "outputTruncated")]
    pub output_truncated: bool,
    #[serde(rename = "payloadDigest")]
    pub payload_digest: Common1Sha256Hex,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub signal: FieldPresence<
        ::std::option::Option<TestExecution1TestExecutionStepResultSignal>,
    >,
    ///passed: exit 0; failed: nonzero exit; error: signal, timeout or spawn failure
    #[serde(rename = "testResult")]
    pub test_result: TestExecution1TestExecutionStepResultTestResult,
    #[serde(rename = "timedOut")]
    pub timed_out: bool,
}
///`TestExecution1TestExecutionStepResultSignal`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct TestExecution1TestExecutionStepResultSignal(::std::string::String);
impl ::std::ops::Deref for TestExecution1TestExecutionStepResultSignal {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<TestExecution1TestExecutionStepResultSignal>
for ::std::string::String {
    fn from(value: TestExecution1TestExecutionStepResultSignal) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for TestExecution1TestExecutionStepResultSignal {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 32usize {
            return Err("longer than 32 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for TestExecution1TestExecutionStepResultSignal {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for TestExecution1TestExecutionStepResultSignal {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for TestExecution1TestExecutionStepResultSignal {
    fn deserialize<D>(deserializer: D) -> ::std::result::Result<Self, D::Error>
    where
        D: ::serde::Deserializer<'de>,
    {
        ::std::string::String::deserialize(deserializer)?
            .parse()
            .map_err(|e: self::error::ConversionError| {
                <D::Error as ::serde::de::Error>::custom(e.to_string())
            })
    }
}
///passed: exit 0; failed: nonzero exit; error: signal, timeout or spawn failure
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum TestExecution1TestExecutionStepResultTestResult {
    #[serde(rename = "passed")]
    Passed,
    #[serde(rename = "failed")]
    Failed,
    #[serde(rename = "error")]
    Error,
}
impl ::std::fmt::Display for TestExecution1TestExecutionStepResultTestResult {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Passed => f.write_str("passed"),
            Self::Failed => f.write_str("failed"),
            Self::Error => f.write_str("error"),
        }
    }
}
impl ::std::str::FromStr for TestExecution1TestExecutionStepResultTestResult {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "passed" => Ok(Self::Passed),
            "failed" => Ok(Self::Failed),
            "error" => Ok(Self::Error),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for TestExecution1TestExecutionStepResultTestResult {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for TestExecution1TestExecutionStepResultTestResult {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Payload domain workflow.import-payload.test.v1; wrapped by the foundation import descriptor with kind=test. Produced by the host test-execution step or imported from an independently prepared run.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct TestExecution1TestPayloadV1 {
    #[serde(rename = "argvDigest")]
    pub argv_digest: Common1Sha256Hex,
    #[serde(
        rename = "exitStatus",
        deserialize_with = "::std::option::Option::deserialize"
    )]
    pub exit_status: ::std::option::Option<u8>,
    #[serde(rename = "outputTruncated")]
    pub output_truncated: bool,
    #[serde(rename = "payloadDomain")]
    pub payload_domain: ::serde_json::Value,
    pub producer: TestExecution1TestPayloadV1Producer,
    pub selection: TestExecution1TestPayloadV1Selection,
    #[serde(deserialize_with = "::std::option::Option::deserialize")]
    pub signal: ::std::option::Option<TestExecution1TestPayloadV1Signal>,
    #[serde(rename = "stderrBytes")]
    pub stderr_bytes: i64,
    #[serde(rename = "stderrDigest")]
    pub stderr_digest: Common1Sha256Hex,
    #[serde(rename = "stdoutBytes")]
    pub stdout_bytes: i64,
    #[serde(rename = "stdoutDigest")]
    pub stdout_digest: Common1Sha256Hex,
    pub tests: ::std::vec::Vec<TestExecution1TestPayloadV1TestsItem>,
    #[serde(rename = "timedOut")]
    pub timed_out: bool,
    #[serde(
        rename = "toolClosureId",
        deserialize_with = "::std::option::Option::deserialize"
    )]
    pub tool_closure_id: ::std::option::Option<Common1ClosureId>,
}
///`TestExecution1TestPayloadV1Producer`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum TestExecution1TestPayloadV1Producer {
    #[serde(rename = "host-test-execution")]
    HostTestExecution,
    #[serde(rename = "independent-prepared")]
    IndependentPrepared,
}
impl ::std::fmt::Display for TestExecution1TestPayloadV1Producer {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::HostTestExecution => f.write_str("host-test-execution"),
            Self::IndependentPrepared => f.write_str("independent-prepared"),
        }
    }
}
impl ::std::str::FromStr for TestExecution1TestPayloadV1Producer {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "host-test-execution" => Ok(Self::HostTestExecution),
            "independent-prepared" => Ok(Self::IndependentPrepared),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for TestExecution1TestPayloadV1Producer {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for TestExecution1TestPayloadV1Producer {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`TestExecution1TestPayloadV1Selection`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct TestExecution1TestPayloadV1Selection {
    #[serde(rename = "completenessEstablished")]
    pub completeness_established: bool,
    pub mode: TestExecution1TestPayloadV1SelectionMode,
}
///`TestExecution1TestPayloadV1SelectionMode`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum TestExecution1TestPayloadV1SelectionMode {
    #[serde(rename = "full")]
    Full,
    #[serde(rename = "impact-selected")]
    ImpactSelected,
    #[serde(rename = "explicit")]
    Explicit,
}
impl ::std::fmt::Display for TestExecution1TestPayloadV1SelectionMode {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Full => f.write_str("full"),
            Self::ImpactSelected => f.write_str("impact-selected"),
            Self::Explicit => f.write_str("explicit"),
        }
    }
}
impl ::std::str::FromStr for TestExecution1TestPayloadV1SelectionMode {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "full" => Ok(Self::Full),
            "impact-selected" => Ok(Self::ImpactSelected),
            "explicit" => Ok(Self::Explicit),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for TestExecution1TestPayloadV1SelectionMode {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for TestExecution1TestPayloadV1SelectionMode {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`TestExecution1TestPayloadV1Signal`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct TestExecution1TestPayloadV1Signal(::std::string::String);
impl ::std::ops::Deref for TestExecution1TestPayloadV1Signal {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<TestExecution1TestPayloadV1Signal> for ::std::string::String {
    fn from(value: TestExecution1TestPayloadV1Signal) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for TestExecution1TestPayloadV1Signal {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 32usize {
            return Err("longer than 32 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for TestExecution1TestPayloadV1Signal {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for TestExecution1TestPayloadV1Signal {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for TestExecution1TestPayloadV1Signal {
    fn deserialize<D>(deserializer: D) -> ::std::result::Result<Self, D::Error>
    where
        D: ::serde::Deserializer<'de>,
    {
        ::std::string::String::deserialize(deserializer)?
            .parse()
            .map_err(|e: self::error::ConversionError| {
                <D::Error as ::serde::de::Error>::custom(e.to_string())
            })
    }
}
///`TestExecution1TestPayloadV1TestsItem`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct TestExecution1TestPayloadV1TestsItem {
    #[serde(
        rename = "durationMillis",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub duration_millis: FieldPresence<::std::option::Option<Common1Uint53>>,
    pub outcome: TestExecution1TestPayloadV1TestsItemOutcome,
    #[serde(
        rename = "subjectPath",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub subject_path: FieldPresence<::std::option::Option<Common1LogicalPath>>,
    #[serde(rename = "testId")]
    pub test_id: TestExecution1TestPayloadV1TestsItemTestId,
}
///`TestExecution1TestPayloadV1TestsItemOutcome`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum TestExecution1TestPayloadV1TestsItemOutcome {
    #[serde(rename = "pass")]
    Pass,
    #[serde(rename = "fail")]
    Fail,
    #[serde(rename = "skip")]
    Skip,
    #[serde(rename = "error")]
    Error,
}
impl ::std::fmt::Display for TestExecution1TestPayloadV1TestsItemOutcome {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Pass => f.write_str("pass"),
            Self::Fail => f.write_str("fail"),
            Self::Skip => f.write_str("skip"),
            Self::Error => f.write_str("error"),
        }
    }
}
impl ::std::str::FromStr for TestExecution1TestPayloadV1TestsItemOutcome {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "pass" => Ok(Self::Pass),
            "fail" => Ok(Self::Fail),
            "skip" => Ok(Self::Skip),
            "error" => Ok(Self::Error),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for TestExecution1TestPayloadV1TestsItemOutcome {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for TestExecution1TestPayloadV1TestsItemOutcome {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`TestExecution1TestPayloadV1TestsItemTestId`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct TestExecution1TestPayloadV1TestsItemTestId(::std::string::String);
impl ::std::ops::Deref for TestExecution1TestPayloadV1TestsItemTestId {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<TestExecution1TestPayloadV1TestsItemTestId>
for ::std::string::String {
    fn from(value: TestExecution1TestPayloadV1TestsItemTestId) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for TestExecution1TestPayloadV1TestsItemTestId {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 1024usize {
            return Err("longer than 1024 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for TestExecution1TestPayloadV1TestsItemTestId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for TestExecution1TestPayloadV1TestsItemTestId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for TestExecution1TestPayloadV1TestsItemTestId {
    fn deserialize<D>(deserializer: D) -> ::std::result::Result<Self, D::Error>
    where
        D: ::serde::Deserializer<'de>,
    {
        ::std::string::String::deserialize(deserializer)?
            .parse()
            .map_err(|e: self::error::ConversionError| {
                <D::Error as ::serde::de::Error>::custom(e.to_string())
            })
    }
}
