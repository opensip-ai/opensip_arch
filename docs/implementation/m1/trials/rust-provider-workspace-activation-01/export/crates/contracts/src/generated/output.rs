// Generated trial: named28 profile, typify0.8.0; inert carriers only.
#![allow(unused_imports)]
use super::evidence::*;
use super::identity::*;
use super::invocation::*;
use super::protocol::*;
use super::evidence::error;
///Identity-bearing: H('workflow.baseline', descriptor). Excludes RequestId, ExecutionId, clocks, receipts, host release and signatures.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Baseline2BaselineDescriptor {
    pub context: Comparison2EvaluationContext,
    #[serde(rename = "contextDocuments")]
    pub context_documents: Baseline2BaselineDescriptorContextDocuments,
    #[serde(rename = "detectorClosure")]
    pub detector_closure: ::std::vec::Vec<Baseline2DetectorClosureEntry>,
    ///sorted strictly ascending by fingerprint UTF-8 bytes; duplicates rejected
    pub entries: ::std::vec::Vec<Baseline2BaselineEntry>,
    #[serde(rename = "fingerprintRecipe")]
    pub fingerprint_recipe: Baseline2BaselineDescriptorFingerprintRecipe,
    #[serde(rename = "originProjectId")]
    pub origin_project_id: Common3ProjectId,
    ///Complete executable closure required to run E0: every detector, the evaluator, stdlib/toolchain closures and registered schema digests. Fact dual-emission (legacy fingerprints) is fingerprint migration only and never appears here.
    #[serde(rename = "pivotClosure")]
    pub pivot_closure: ::std::vec::Vec<Baseline2PivotClosureEntry>,
    #[serde(rename = "planId")]
    pub plan_id: Common3PlanId,
    #[serde(rename = "ruleCoverage")]
    pub rule_coverage: ::std::vec::Vec<Comparison2RuleCoverage>,
    #[serde(rename = "runId")]
    pub run_id: Common3RunId,
    #[serde(rename = "schemaFamily")]
    pub schema_family: ::serde_json::Value,
    #[serde(rename = "schemaMajor")]
    pub schema_major: ExactInteger,
    pub source: Baseline2BaselineDescriptorSource,
    ///Every unmatched finding3 of the origin Run. Empty is an explicit complete-correspondence assertion for unmatched, not an implicit default for schemaMajor 1.
    #[serde(rename = "unmatchedOccurrences")]
    pub unmatched_occurrences: ::std::vec::Vec<Common3UnmatchedOccurrence>,
}
///Embedded typed documents whose digests equal context.*Digest. They make E1..E3 computable on a fresh CI host.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Baseline2BaselineDescriptorContextDocuments {
    pub policy: Policy2PolicyDocumentV2,
    pub scope: Policy1ScopeDocumentV1,
    pub waivers: Policy1WaiverSetV1,
}
///`Baseline2BaselineDescriptorFingerprintRecipe`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Baseline2BaselineDescriptorFingerprintRecipe {
    pub domain: ::serde_json::Value,
    #[serde(rename = "recipeMajor")]
    pub recipe_major: i64,
}
///`Baseline2BaselineDescriptorSource`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Baseline2BaselineDescriptorSource {
    #[serde(rename = "snapshotId")]
    pub snapshot_id: Common3SnapshotId,
    #[serde(
        rename = "vcsRevision",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub vcs_revision: FieldPresence<::std::option::Option<Common3VcsRevision>>,
}
///`Baseline2BaselineEntry`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Baseline2BaselineEntry {
    ///the entry rule's emission-binding contributionId; a member of detectorClosure detectorId
    #[serde(rename = "detectorId")]
    pub detector_id: Common3CanonicalIdentifier,
    pub fingerprint: Common3Fingerprint,
    ///present only inside a fingerprint dual-emission window; supplies identity migration, never a prior executable algorithm
    #[serde(
        rename = "legacyFingerprint",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub legacy_fingerprint: FieldPresence<
        ::std::option::Option<Baseline2BaselineEntryLegacyFingerprint>,
    >,
    #[serde(rename = "ruleId")]
    pub rule_id: Common3CanonicalIdentifier,
    #[serde(rename = "stabilityClass")]
    pub stability_class: Baseline2BaselineEntryStabilityClass,
    #[serde(rename = "subjectPath")]
    pub subject_path: Common3LogicalPath,
    pub waived: bool,
}
///present only inside a fingerprint dual-emission window; supplies identity migration, never a prior executable algorithm
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Baseline2BaselineEntryLegacyFingerprint(::std::string::String);
impl ::std::ops::Deref for Baseline2BaselineEntryLegacyFingerprint {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Baseline2BaselineEntryLegacyFingerprint>
for ::std::string::String {
    fn from(value: Baseline2BaselineEntryLegacyFingerprint) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Baseline2BaselineEntryLegacyFingerprint {
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
impl ::std::convert::TryFrom<&str> for Baseline2BaselineEntryLegacyFingerprint {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Baseline2BaselineEntryLegacyFingerprint {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Baseline2BaselineEntryLegacyFingerprint {
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
///`Baseline2BaselineEntryStabilityClass`
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
pub enum Baseline2BaselineEntryStabilityClass {
    #[serde(rename = "rename-stable")]
    RenameStable,
    #[serde(rename = "path-stable")]
    PathStable,
    #[serde(rename = "span-fallback")]
    SpanFallback,
}
impl ::std::fmt::Display for Baseline2BaselineEntryStabilityClass {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::RenameStable => f.write_str("rename-stable"),
            Self::PathStable => f.write_str("path-stable"),
            Self::SpanFallback => f.write_str("span-fallback"),
        }
    }
}
impl ::std::str::FromStr for Baseline2BaselineEntryStabilityClass {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "rename-stable" => Ok(Self::RenameStable),
            "path-stable" => Ok(Self::PathStable),
            "span-fallback" => Ok(Self::SpanFallback),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Baseline2BaselineEntryStabilityClass {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Baseline2BaselineEntryStabilityClass {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Non-identity custody envelope. Time and host release are disclosure only; they never enter baselineId.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Baseline2Custody {
    #[serde(
        rename = "closureBundle",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub closure_bundle: FieldPresence<
        ::std::option::Option<Baseline2CustodyClosureBundle>,
    >,
    #[serde(rename = "exportedAtUtc")]
    pub exported_at_utc: Common3UtcTimestamp,
    #[serde(rename = "exportedByHostRelease")]
    pub exported_by_host_release: Common3SemanticVersion,
    ///retention roots the origin host pinned at adoption: the Run and every pivot closure; loss of a pin is disclosed as availability partial, never as a silent two-way fallback
    #[serde(rename = "retentionPins")]
    pub retention_pins: ::std::vec::Vec<::std::string::String>,
    #[serde(rename = "runRetainedAtExport")]
    pub run_retained_at_export: bool,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub signature: FieldPresence<::std::option::Option<Baseline2CustodySignature>>,
}
///optional signed portable bundle carrying the pivot closure bytes for a fresh CI host; its signature/trust admission is the security unit's contract
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Baseline2CustodyClosureBundle {
    pub bytes: ::std::num::NonZeroU64,
    pub path: Common3UserInputPath,
    pub sha256: Common3Sha256Hex,
}
///`Baseline2CustodySignature`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Baseline2CustodySignature {
    #[serde(rename = "keyId")]
    pub key_id: Common3Sha256Hex,
    pub scheme: ::serde_json::Value,
    pub value: ::std::string::String,
}
///Exactly one row per distinct contributionId of the origin EvaluatorEmissionPlanV1 rule rows (disabled rules included): detectorId equals contributionId; closureId and semanticsMajor are that contribution row detectorClosure and semanticsMajor. Rows sharing a contributionId with a different closure or major refuse (CONFIG.INVALID / EVALUATION.FINDING_JOIN_REFUSED).
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Baseline2DetectorClosureEntry {
    #[serde(rename = "closureId")]
    pub closure_id: Common3ClosureId,
    #[serde(rename = "contributionId")]
    pub contribution_id: Common3ContributionId,
    ///equals contributionId
    #[serde(rename = "detectorId")]
    pub detector_id: Common3CanonicalIdentifier,
    #[serde(rename = "manifestDigest")]
    pub manifest_digest: Common3Sha256Hex,
    #[serde(rename = "semanticVersion")]
    pub semantic_version: Common3SemanticVersion,
    #[serde(rename = "semanticsMajor")]
    pub semantics_major: u16,
}
///`Baseline2PivotClosureEntry`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Baseline2PivotClosureEntry {
    #[serde(rename = "closureId")]
    pub closure_id: Common3ClosureId,
    pub kind: Baseline2PivotClosureEntryKind,
    #[serde(rename = "manifestDigest")]
    pub manifest_digest: Common3Sha256Hex,
    pub platform: Baseline2PivotClosureEntryPlatform,
    #[serde(rename = "protocolMajor")]
    pub protocol_major: u16,
}
///`Baseline2PivotClosureEntryKind`
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
pub enum Baseline2PivotClosureEntryKind {
    #[serde(rename = "detector")]
    Detector,
    #[serde(rename = "evaluator")]
    Evaluator,
    #[serde(rename = "provider")]
    Provider,
    #[serde(rename = "toolchain")]
    Toolchain,
    #[serde(rename = "stdlib")]
    Stdlib,
    #[serde(rename = "schema-set")]
    SchemaSet,
}
impl ::std::fmt::Display for Baseline2PivotClosureEntryKind {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Detector => f.write_str("detector"),
            Self::Evaluator => f.write_str("evaluator"),
            Self::Provider => f.write_str("provider"),
            Self::Toolchain => f.write_str("toolchain"),
            Self::Stdlib => f.write_str("stdlib"),
            Self::SchemaSet => f.write_str("schema-set"),
        }
    }
}
impl ::std::str::FromStr for Baseline2PivotClosureEntryKind {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "detector" => Ok(Self::Detector),
            "evaluator" => Ok(Self::Evaluator),
            "provider" => Ok(Self::Provider),
            "toolchain" => Ok(Self::Toolchain),
            "stdlib" => Ok(Self::Stdlib),
            "schema-set" => Ok(Self::SchemaSet),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Baseline2PivotClosureEntryKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Baseline2PivotClosureEntryKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Baseline2PivotClosureEntryPlatform`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Baseline2PivotClosureEntryPlatform(::std::string::String);
impl ::std::ops::Deref for Baseline2PivotClosureEntryPlatform {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Baseline2PivotClosureEntryPlatform> for ::std::string::String {
    fn from(value: Baseline2PivotClosureEntryPlatform) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Baseline2PivotClosureEntryPlatform {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 64usize {
            return Err("longer than 64 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Baseline2PivotClosureEntryPlatform {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Baseline2PivotClosureEntryPlatform {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Baseline2PivotClosureEntryPlatform {
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
///`Baseline2PivotClosureEntryPropertiesKind`
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
pub enum Baseline2PivotClosureEntryPropertiesKind {
    #[serde(rename = "detector")]
    Detector,
    #[serde(rename = "evaluator")]
    Evaluator,
    #[serde(rename = "provider")]
    Provider,
    #[serde(rename = "toolchain")]
    Toolchain,
    #[serde(rename = "stdlib")]
    Stdlib,
    #[serde(rename = "schema-set")]
    SchemaSet,
}
impl ::std::fmt::Display for Baseline2PivotClosureEntryPropertiesKind {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Detector => f.write_str("detector"),
            Self::Evaluator => f.write_str("evaluator"),
            Self::Provider => f.write_str("provider"),
            Self::Toolchain => f.write_str("toolchain"),
            Self::Stdlib => f.write_str("stdlib"),
            Self::SchemaSet => f.write_str("schema-set"),
        }
    }
}
impl ::std::str::FromStr for Baseline2PivotClosureEntryPropertiesKind {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "detector" => Ok(Self::Detector),
            "evaluator" => Ok(Self::Evaluator),
            "provider" => Ok(Self::Provider),
            "toolchain" => Ok(Self::Toolchain),
            "stdlib" => Ok(Self::Stdlib),
            "schema-set" => Ok(Self::SchemaSet),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Baseline2PivotClosureEntryPropertiesKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Baseline2PivotClosureEntryPropertiesKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Identity-bearing descriptor schemaMajor is 2 because unmatchedOccurrences is a required member of the H('workflow.baseline', descriptor) preimage. Historical schemaMajor 1 artifacts are refused (BASELINE.SCHEMA_MAJOR_UNSUPPORTED / REQUEST.SCHEMA_MAJOR_UNSUPPORTED). They MUST NOT be admitted by treating a missing unmatched array as []. RunId is run3. Fingerprint recipe remains finding-fingerprint / finding-key2. Policy embed is PolicyDocumentV2; Scope/Waiver remain V1 on the original owner document.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Baseline2Root {
    #[serde(rename = "baselineId")]
    pub baseline_id: Common3BaselineId,
    pub custody: Baseline2Custody,
    pub descriptor: Baseline2BaselineDescriptor,
}
///Explicit, visible gate semantics. code-regression (default for audit): gates CODE-NET-NEW on rules gating under baseline OR current policy; a new waiver added in the same change does not suppress it. policy-change: additionally gates findings newly live through POLICY/SCOPE/WAIVER deltas (used to review a policy change; code regressions still gate). full-current: every live unwaived gating finding on the current side gates, whatever its axis. report-only: nothing gates; verdict is pass or indeterminate only.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Comparison2AuditProfile {
    #[serde(rename = "gateAllCurrentLive")]
    pub gate_all_current_live: bool,
    #[serde(rename = "gateCodeNetNew")]
    pub gate_code_net_new: bool,
    #[serde(rename = "gateNewlyLiveByPolicyAxes")]
    pub gate_newly_live_by_policy_axes: bool,
    #[serde(rename = "gateRuleUnder")]
    pub gate_rule_under: Comparison2AuditProfileGateRuleUnder,
    pub name: Comparison2AuditProfileName,
    #[serde(rename = "newWaiverSuppressesCodeNetNew")]
    pub new_waiver_suppresses_code_net_new: bool,
}
///`Comparison2AuditProfileGateRuleUnder`
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
pub enum Comparison2AuditProfileGateRuleUnder {
    #[serde(rename = "baseline-or-current")]
    BaselineOrCurrent,
    #[serde(rename = "current-only")]
    CurrentOnly,
}
impl ::std::fmt::Display for Comparison2AuditProfileGateRuleUnder {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::BaselineOrCurrent => f.write_str("baseline-or-current"),
            Self::CurrentOnly => f.write_str("current-only"),
        }
    }
}
impl ::std::str::FromStr for Comparison2AuditProfileGateRuleUnder {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "baseline-or-current" => Ok(Self::BaselineOrCurrent),
            "current-only" => Ok(Self::CurrentOnly),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Comparison2AuditProfileGateRuleUnder {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Comparison2AuditProfileGateRuleUnder {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Comparison2AuditProfileName`
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
pub enum Comparison2AuditProfileName {
    #[serde(rename = "code-regression")]
    CodeRegression,
    #[serde(rename = "policy-change")]
    PolicyChange,
    #[serde(rename = "full-current")]
    FullCurrent,
    #[serde(rename = "report-only")]
    ReportOnly,
}
impl ::std::fmt::Display for Comparison2AuditProfileName {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::CodeRegression => f.write_str("code-regression"),
            Self::PolicyChange => f.write_str("policy-change"),
            Self::FullCurrent => f.write_str("full-current"),
            Self::ReportOnly => f.write_str("report-only"),
        }
    }
}
impl ::std::str::FromStr for Comparison2AuditProfileName {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "code-regression" => Ok(Self::CodeRegression),
            "policy-change" => Ok(Self::PolicyChange),
            "full-current" => Ok(Self::FullCurrent),
            "report-only" => Ok(Self::ReportOnly),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Comparison2AuditProfileName {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Comparison2AuditProfileName {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Comparison2Axis`
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
pub enum Comparison2Axis {
    #[serde(rename = "code")]
    Code,
    #[serde(rename = "detection")]
    Detection,
    #[serde(rename = "policy")]
    Policy,
    #[serde(rename = "scope")]
    Scope,
    #[serde(rename = "waiver")]
    Waiver,
    #[serde(rename = "evidence")]
    Evidence,
}
impl ::std::fmt::Display for Comparison2Axis {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Code => f.write_str("code"),
            Self::Detection => f.write_str("detection"),
            Self::Policy => f.write_str("policy"),
            Self::Scope => f.write_str("scope"),
            Self::Waiver => f.write_str("waiver"),
            Self::Evidence => f.write_str("evidence"),
        }
    }
}
impl ::std::str::FromStr for Comparison2Axis {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "code" => Ok(Self::Code),
            "detection" => Ok(Self::Detection),
            "policy" => Ok(Self::Policy),
            "scope" => Ok(Self::Scope),
            "waiver" => Ok(Self::Waiver),
            "evidence" => Ok(Self::Evidence),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Comparison2Axis {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Comparison2Axis {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Comparison2BoundImport`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Comparison2BoundImport {
    #[serde(rename = "importId")]
    pub import_id: Common3ImportId,
    pub kind: Imported1ImportKind,
    #[serde(rename = "observationDigest")]
    pub observation_digest: Common3Sha256Hex,
    #[serde(rename = "payloadDigest")]
    pub payload_digest: Common3Sha256Hex,
    #[serde(rename = "scopeDigest")]
    pub scope_digest: Common3Sha256Hex,
    #[serde(rename = "sourceCorrespondenceDigest")]
    pub source_correspondence_digest: Common3Sha256Hex,
}
///`Comparison2Classification`
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
pub enum Comparison2Classification {
    #[serde(rename = "UNCHANGED")]
    Unchanged,
    #[serde(rename = "CODE-NET-NEW")]
    CodeNetNew,
    #[serde(rename = "CODE-FIXED")]
    CodeFixed,
    #[serde(rename = "DETECTION-DELTA")]
    DetectionDelta,
    #[serde(rename = "POLICY-DELTA")]
    PolicyDelta,
    #[serde(rename = "SCOPE-DELTA")]
    ScopeDelta,
    #[serde(rename = "WAIVER-DELTA")]
    WaiverDelta,
    #[serde(rename = "EVIDENCE-DELTA")]
    EvidenceDelta,
    #[serde(rename = "INDETERMINATE")]
    Indeterminate,
}
impl ::std::fmt::Display for Comparison2Classification {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Unchanged => f.write_str("UNCHANGED"),
            Self::CodeNetNew => f.write_str("CODE-NET-NEW"),
            Self::CodeFixed => f.write_str("CODE-FIXED"),
            Self::DetectionDelta => f.write_str("DETECTION-DELTA"),
            Self::PolicyDelta => f.write_str("POLICY-DELTA"),
            Self::ScopeDelta => f.write_str("SCOPE-DELTA"),
            Self::WaiverDelta => f.write_str("WAIVER-DELTA"),
            Self::EvidenceDelta => f.write_str("EVIDENCE-DELTA"),
            Self::Indeterminate => f.write_str("INDETERMINATE"),
        }
    }
}
impl ::std::str::FromStr for Comparison2Classification {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "UNCHANGED" => Ok(Self::Unchanged),
            "CODE-NET-NEW" => Ok(Self::CodeNetNew),
            "CODE-FIXED" => Ok(Self::CodeFixed),
            "DETECTION-DELTA" => Ok(Self::DetectionDelta),
            "POLICY-DELTA" => Ok(Self::PolicyDelta),
            "SCOPE-DELTA" => Ok(Self::ScopeDelta),
            "WAIVER-DELTA" => Ok(Self::WaiverDelta),
            "EVIDENCE-DELTA" => Ok(Self::EvidenceDelta),
            "INDETERMINATE" => Ok(Self::Indeterminate),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Comparison2Classification {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Comparison2Classification {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Identity-bearing: H('workflow.comparison', descriptor). Excludes RequestId/ExecutionId/clocks/receipts.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Comparison2ComparisonDescriptor {
    #[serde(rename = "auditProfile")]
    pub audit_profile: Comparison2AuditProfile,
    #[serde(rename = "baselineContext")]
    pub baseline_context: Comparison2EvaluationContext,
    #[serde(rename = "baselineId")]
    pub baseline_id: Common3BaselineId,
    #[serde(rename = "comparisonPerformed")]
    pub comparison_performed: bool,
    #[serde(rename = "contextDelta")]
    pub context_delta: Comparison2ComparisonDescriptorContextDelta,
    #[serde(rename = "correspondenceCoverage")]
    pub correspondence_coverage: ::std::vec::Vec<Common3CorrespondenceCoverage>,
    pub counts: Comparison2ComparisonDescriptorCounts,
    #[serde(rename = "currentContext")]
    pub current_context: Comparison2EvaluationContext,
    ///Admitted current proof evaluationState. Independent of rule gating.
    #[serde(rename = "currentEvaluationState")]
    pub current_evaluation_state: Comparison2ComparisonDescriptorCurrentEvaluationState,
    ///Exact current proof executionDeficiencies (source-specific causes). Not collapsed into ruleDeficiencies. Execution unknown is independent of policy gating; matched CODE-NET-NEW fail still dominates.
    #[serde(rename = "currentExecutionDeficiencies")]
    pub current_execution_deficiencies: ::std::vec::Vec<Comparison2ExecutionDeficiency>,
    #[serde(rename = "currentRunId")]
    pub current_run_id: Common3RunId,
    #[serde(rename = "currentSnapshotId")]
    pub current_snapshot_id: Common3SnapshotId,
    #[serde(
        rename = "d9Deficiency",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub d9_deficiency: FieldPresence<::std::option::Option<Common3D9Deficiency>>,
    pub detectors: ::std::vec::Vec<Comparison2DetectorDisposition>,
    ///sorted strictly ascending by fingerprint UTF-8 bytes
    pub entries: ::std::vec::Vec<Comparison2Entry>,
    #[serde(rename = "pivotsAvailable")]
    pub pivots_available: Comparison2ComparisonDescriptorPivotsAvailable,
    #[serde(rename = "projectCorrespondence")]
    pub project_correspondence: Comparison2ComparisonDescriptorProjectCorrespondence,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub remedy: FieldPresence<::std::option::Option<Common3DomainDetail>>,
    ///sorted by ruleId; a gating deficiency yields verdict indeterminate even with zero entries
    #[serde(rename = "ruleDeficiencies")]
    pub rule_deficiencies: ::std::vec::Vec<Comparison2RuleDeficiency>,
    #[serde(rename = "schemaFamily")]
    pub schema_family: ::serde_json::Value,
    #[serde(rename = "schemaMajor")]
    pub schema_major: ExactInteger,
    ///Union of baseline and current unmatched findings. Not comparison entries and not classified as UNCHANGED, CODE-NET-NEW, or CODE-FIXED.
    #[serde(rename = "unmatchedOccurrences")]
    pub unmatched_occurrences: ::std::vec::Vec<Common3UnmatchedOccurrence>,
    pub verdict: Comparison2ComparisonDescriptorVerdict,
    #[serde(
        rename = "wholeIndeterminateReason",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub whole_indeterminate_reason: FieldPresence<
        ::std::option::Option<Comparison2IndeterminateReason>,
    >,
}
///`Comparison2ComparisonDescriptorContextDelta`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Comparison2ComparisonDescriptorContextDelta {
    #[serde(rename = "codeChanged")]
    pub code_changed: bool,
    #[serde(rename = "detectorChanged")]
    pub detector_changed: bool,
    #[serde(rename = "evidenceAvailabilityChanged")]
    pub evidence_availability_changed: bool,
    #[serde(rename = "policyChanged")]
    pub policy_changed: bool,
    #[serde(rename = "scopeChanged")]
    pub scope_changed: bool,
    #[serde(rename = "waiversChanged")]
    pub waivers_changed: bool,
}
///`Comparison2ComparisonDescriptorCounts`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Comparison2ComparisonDescriptorCounts {
    #[serde(rename = "CODE-FIXED")]
    pub code_fixed: Common3Uint53,
    #[serde(rename = "CODE-NET-NEW")]
    pub code_net_new: Common3Uint53,
    #[serde(rename = "DETECTION-DELTA")]
    pub detection_delta: Common3Uint53,
    #[serde(rename = "EVIDENCE-DELTA")]
    pub evidence_delta: Common3Uint53,
    pub gating: Common3Uint53,
    #[serde(rename = "INDETERMINATE")]
    pub indeterminate: Common3Uint53,
    #[serde(rename = "POLICY-DELTA")]
    pub policy_delta: Common3Uint53,
    #[serde(rename = "SCOPE-DELTA")]
    pub scope_delta: Common3Uint53,
    #[serde(rename = "UNCHANGED")]
    pub unchanged: Common3Uint53,
    #[serde(rename = "WAIVER-DELTA")]
    pub waiver_delta: Common3Uint53,
}
///Admitted current proof evaluationState. Independent of rule gating.
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
pub enum Comparison2ComparisonDescriptorCurrentEvaluationState {
    #[serde(rename = "evaluated")]
    Evaluated,
    #[serde(rename = "budget-exhausted")]
    BudgetExhausted,
}
impl ::std::fmt::Display for Comparison2ComparisonDescriptorCurrentEvaluationState {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Evaluated => f.write_str("evaluated"),
            Self::BudgetExhausted => f.write_str("budget-exhausted"),
        }
    }
}
impl ::std::str::FromStr for Comparison2ComparisonDescriptorCurrentEvaluationState {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "evaluated" => Ok(Self::Evaluated),
            "budget-exhausted" => Ok(Self::BudgetExhausted),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str>
for Comparison2ComparisonDescriptorCurrentEvaluationState {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Comparison2ComparisonDescriptorCurrentEvaluationState {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Derived from what was actually bound, never assumed: E0 from the detector dispositions; E1..E3 are 'available' only when the current side supplied a bound re-evaluation result for that pivot (boundPivots), 'not-needed' when that axis is unchanged, else 'unavailable' (every entry INDETERMINATE pivot-reevaluation-unavailable).
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Comparison2ComparisonDescriptorPivotsAvailable {
    #[serde(rename = "E0")]
    pub e0: Comparison2ComparisonDescriptorPivotsAvailableE0,
    #[serde(rename = "E1")]
    pub e1: Comparison2ComparisonDescriptorPivotsAvailableE1,
    #[serde(rename = "E2")]
    pub e2: Comparison2ComparisonDescriptorPivotsAvailableE2,
    #[serde(rename = "E3")]
    pub e3: Comparison2ComparisonDescriptorPivotsAvailableE3,
}
///`Comparison2ComparisonDescriptorPivotsAvailableE0`
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
pub enum Comparison2ComparisonDescriptorPivotsAvailableE0 {
    #[serde(rename = "available")]
    Available,
    #[serde(rename = "not-needed")]
    NotNeeded,
    #[serde(rename = "unavailable")]
    Unavailable,
}
impl ::std::fmt::Display for Comparison2ComparisonDescriptorPivotsAvailableE0 {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Available => f.write_str("available"),
            Self::NotNeeded => f.write_str("not-needed"),
            Self::Unavailable => f.write_str("unavailable"),
        }
    }
}
impl ::std::str::FromStr for Comparison2ComparisonDescriptorPivotsAvailableE0 {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "available" => Ok(Self::Available),
            "not-needed" => Ok(Self::NotNeeded),
            "unavailable" => Ok(Self::Unavailable),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Comparison2ComparisonDescriptorPivotsAvailableE0 {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Comparison2ComparisonDescriptorPivotsAvailableE0 {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Comparison2ComparisonDescriptorPivotsAvailableE1`
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
pub enum Comparison2ComparisonDescriptorPivotsAvailableE1 {
    #[serde(rename = "available")]
    Available,
    #[serde(rename = "not-needed")]
    NotNeeded,
    #[serde(rename = "unavailable")]
    Unavailable,
}
impl ::std::fmt::Display for Comparison2ComparisonDescriptorPivotsAvailableE1 {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Available => f.write_str("available"),
            Self::NotNeeded => f.write_str("not-needed"),
            Self::Unavailable => f.write_str("unavailable"),
        }
    }
}
impl ::std::str::FromStr for Comparison2ComparisonDescriptorPivotsAvailableE1 {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "available" => Ok(Self::Available),
            "not-needed" => Ok(Self::NotNeeded),
            "unavailable" => Ok(Self::Unavailable),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Comparison2ComparisonDescriptorPivotsAvailableE1 {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Comparison2ComparisonDescriptorPivotsAvailableE1 {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Comparison2ComparisonDescriptorPivotsAvailableE2`
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
pub enum Comparison2ComparisonDescriptorPivotsAvailableE2 {
    #[serde(rename = "available")]
    Available,
    #[serde(rename = "not-needed")]
    NotNeeded,
    #[serde(rename = "unavailable")]
    Unavailable,
}
impl ::std::fmt::Display for Comparison2ComparisonDescriptorPivotsAvailableE2 {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Available => f.write_str("available"),
            Self::NotNeeded => f.write_str("not-needed"),
            Self::Unavailable => f.write_str("unavailable"),
        }
    }
}
impl ::std::str::FromStr for Comparison2ComparisonDescriptorPivotsAvailableE2 {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "available" => Ok(Self::Available),
            "not-needed" => Ok(Self::NotNeeded),
            "unavailable" => Ok(Self::Unavailable),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Comparison2ComparisonDescriptorPivotsAvailableE2 {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Comparison2ComparisonDescriptorPivotsAvailableE2 {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Comparison2ComparisonDescriptorPivotsAvailableE3`
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
pub enum Comparison2ComparisonDescriptorPivotsAvailableE3 {
    #[serde(rename = "available")]
    Available,
    #[serde(rename = "not-needed")]
    NotNeeded,
    #[serde(rename = "unavailable")]
    Unavailable,
}
impl ::std::fmt::Display for Comparison2ComparisonDescriptorPivotsAvailableE3 {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Available => f.write_str("available"),
            Self::NotNeeded => f.write_str("not-needed"),
            Self::Unavailable => f.write_str("unavailable"),
        }
    }
}
impl ::std::str::FromStr for Comparison2ComparisonDescriptorPivotsAvailableE3 {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "available" => Ok(Self::Available),
            "not-needed" => Ok(Self::NotNeeded),
            "unavailable" => Ok(Self::Unavailable),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Comparison2ComparisonDescriptorPivotsAvailableE3 {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Comparison2ComparisonDescriptorPivotsAvailableE3 {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Comparison2ComparisonDescriptorProjectCorrespondence`
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
pub enum Comparison2ComparisonDescriptorProjectCorrespondence {
    #[serde(rename = "same-project")]
    SameProject,
    #[serde(rename = "declared")]
    Declared,
    #[serde(rename = "unmapped")]
    Unmapped,
}
impl ::std::fmt::Display for Comparison2ComparisonDescriptorProjectCorrespondence {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::SameProject => f.write_str("same-project"),
            Self::Declared => f.write_str("declared"),
            Self::Unmapped => f.write_str("unmapped"),
        }
    }
}
impl ::std::str::FromStr for Comparison2ComparisonDescriptorProjectCorrespondence {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "same-project" => Ok(Self::SameProject),
            "declared" => Ok(Self::Declared),
            "unmapped" => Ok(Self::Unmapped),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str>
for Comparison2ComparisonDescriptorProjectCorrespondence {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Comparison2ComparisonDescriptorProjectCorrespondence {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Comparison2ComparisonDescriptorVerdict`
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
pub enum Comparison2ComparisonDescriptorVerdict {
    #[serde(rename = "pass")]
    Pass,
    #[serde(rename = "fail")]
    Fail,
    #[serde(rename = "indeterminate")]
    Indeterminate,
}
impl ::std::fmt::Display for Comparison2ComparisonDescriptorVerdict {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Pass => f.write_str("pass"),
            Self::Fail => f.write_str("fail"),
            Self::Indeterminate => f.write_str("indeterminate"),
        }
    }
}
impl ::std::str::FromStr for Comparison2ComparisonDescriptorVerdict {
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
impl ::std::convert::TryFrom<&str> for Comparison2ComparisonDescriptorVerdict {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Comparison2ComparisonDescriptorVerdict {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Comparison2DetectorDisposition`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Comparison2DetectorDisposition {
    ///null only for method=detector-added
    #[serde(
        rename = "baselineClosureId",
        deserialize_with = "::std::option::Option::deserialize"
    )]
    pub baseline_closure_id: ::std::option::Option<Common3ClosureId>,
    #[serde(
        rename = "baselineSemanticsMajor",
        deserialize_with = "::std::option::Option::deserialize"
    )]
    pub baseline_semantics_major: ::std::option::Option<u16>,
    ///null when the current detector was removed, including indeterminate removal without an admitted pivot.
    #[serde(
        rename = "currentClosureId",
        deserialize_with = "::std::option::Option::deserialize"
    )]
    pub current_closure_id: ::std::option::Option<Common3ClosureId>,
    #[serde(
        rename = "currentSemanticsMajor",
        deserialize_with = "::std::option::Option::deserialize"
    )]
    pub current_semantics_major: ::std::option::Option<u16>,
    #[serde(rename = "detectorId")]
    pub detector_id: Common3CanonicalIdentifier,
    #[serde(
        rename = "indeterminateReason",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub indeterminate_reason: FieldPresence<
        ::std::option::Option<Comparison2IndeterminateReason>,
    >,
    ///Identical or explicitly compatible closures permit two-way comparison. Changed or removed baseline detectors require a committed current-trusted E0 pivot over current source; removal sets E1..E4 false but preserves measured E0. New detectors set E0 false. Missing pivot is indeterminate; removal cannot hide code regressions.
    pub method: Comparison2DetectorDispositionMethod,
    #[serde(
        rename = "pivotRunId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub pivot_run_id: FieldPresence<::std::option::Option<Common3RunId>>,
}
///Identical or explicitly compatible closures permit two-way comparison. Changed or removed baseline detectors require a committed current-trusted E0 pivot over current source; removal sets E1..E4 false but preserves measured E0. New detectors set E0 false. Missing pivot is indeterminate; removal cannot hide code regressions.
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
pub enum Comparison2DetectorDispositionMethod {
    #[serde(rename = "identical-closure")]
    IdenticalClosure,
    #[serde(rename = "declared-compatible")]
    DeclaredCompatible,
    #[serde(rename = "three-way-pivot")]
    ThreeWayPivot,
    #[serde(rename = "detector-added")]
    DetectorAdded,
    #[serde(rename = "detector-removed")]
    DetectorRemoved,
    #[serde(rename = "indeterminate")]
    Indeterminate,
}
impl ::std::fmt::Display for Comparison2DetectorDispositionMethod {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::IdenticalClosure => f.write_str("identical-closure"),
            Self::DeclaredCompatible => f.write_str("declared-compatible"),
            Self::ThreeWayPivot => f.write_str("three-way-pivot"),
            Self::DetectorAdded => f.write_str("detector-added"),
            Self::DetectorRemoved => f.write_str("detector-removed"),
            Self::Indeterminate => f.write_str("indeterminate"),
        }
    }
}
impl ::std::str::FromStr for Comparison2DetectorDispositionMethod {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "identical-closure" => Ok(Self::IdenticalClosure),
            "declared-compatible" => Ok(Self::DeclaredCompatible),
            "three-way-pivot" => Ok(Self::ThreeWayPivot),
            "detector-added" => Ok(Self::DetectorAdded),
            "detector-removed" => Ok(Self::DetectorRemoved),
            "indeterminate" => Ok(Self::Indeterminate),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Comparison2DetectorDispositionMethod {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Comparison2DetectorDispositionMethod {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Comparison2Entry`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Comparison2Entry {
    pub classification: Comparison2Classification,
    #[serde(rename = "detectorId")]
    pub detector_id: Common3CanonicalIdentifier,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub direction: FieldPresence<::std::option::Option<Comparison2EntryDirection>>,
    pub fingerprint: Common3Fingerprint,
    ///code-net-new-policy-hidden: a gating CODE-NET-NEW entry that is not live in current because a later axis hid it (a detector, policy or scope change, or a waiver added in the same change); subsequentDeltas names the later axes.
    #[serde(
        rename = "gateReason",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub gate_reason: FieldPresence<::std::option::Option<Comparison2EntryGateReason>>,
    pub gates: bool,
    #[serde(
        rename = "indeterminateReason",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub indeterminate_reason: FieldPresence<
        ::std::option::Option<Comparison2IndeterminateReason>,
    >,
    ///true only when E4 is a known hit and the current occurrence is not waived
    #[serde(rename = "liveInCurrent")]
    pub live_in_current: bool,
    pub presence: Comparison2PivotPresence,
    #[serde(rename = "ruleId")]
    pub rule_id: Common3CanonicalIdentifier,
    ///axes after the classifying axis at which presence/waiver status changed again; a CODE-NET-NEW entry with subsequentDeltas [policy] is a code regression hidden by a policy change and still gates
    #[serde(rename = "subsequentDeltas")]
    pub subsequent_deltas: ::std::vec::Vec<Comparison2Axis>,
}
///`Comparison2EntryDirection`
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
pub enum Comparison2EntryDirection {
    #[serde(rename = "appeared")]
    Appeared,
    #[serde(rename = "vanished")]
    Vanished,
    #[serde(rename = "waiver-added")]
    WaiverAdded,
    #[serde(rename = "waiver-removed")]
    WaiverRemoved,
}
impl ::std::fmt::Display for Comparison2EntryDirection {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Appeared => f.write_str("appeared"),
            Self::Vanished => f.write_str("vanished"),
            Self::WaiverAdded => f.write_str("waiver-added"),
            Self::WaiverRemoved => f.write_str("waiver-removed"),
        }
    }
}
impl ::std::str::FromStr for Comparison2EntryDirection {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "appeared" => Ok(Self::Appeared),
            "vanished" => Ok(Self::Vanished),
            "waiver-added" => Ok(Self::WaiverAdded),
            "waiver-removed" => Ok(Self::WaiverRemoved),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Comparison2EntryDirection {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Comparison2EntryDirection {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///code-net-new-policy-hidden: a gating CODE-NET-NEW entry that is not live in current because a later axis hid it (a detector, policy or scope change, or a waiver added in the same change); subsequentDeltas names the later axes.
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
pub enum Comparison2EntryGateReason {
    #[serde(rename = "code-net-new")]
    CodeNetNew,
    #[serde(rename = "code-net-new-policy-hidden")]
    CodeNetNewPolicyHidden,
    #[serde(rename = "newly-live-policy-axis")]
    NewlyLivePolicyAxis,
    #[serde(rename = "current-live")]
    CurrentLive,
    #[serde(rename = "indeterminate-gating-rule")]
    IndeterminateGatingRule,
}
impl ::std::fmt::Display for Comparison2EntryGateReason {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::CodeNetNew => f.write_str("code-net-new"),
            Self::CodeNetNewPolicyHidden => f.write_str("code-net-new-policy-hidden"),
            Self::NewlyLivePolicyAxis => f.write_str("newly-live-policy-axis"),
            Self::CurrentLive => f.write_str("current-live"),
            Self::IndeterminateGatingRule => f.write_str("indeterminate-gating-rule"),
        }
    }
}
impl ::std::str::FromStr for Comparison2EntryGateReason {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "code-net-new" => Ok(Self::CodeNetNew),
            "code-net-new-policy-hidden" => Ok(Self::CodeNetNewPolicyHidden),
            "newly-live-policy-axis" => Ok(Self::NewlyLivePolicyAxis),
            "current-live" => Ok(Self::CurrentLive),
            "indeterminate-gating-rule" => Ok(Self::IndeterminateGatingRule),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Comparison2EntryGateReason {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Comparison2EntryGateReason {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Digests of the evaluation context on one side. policyDigest = raw SHA-256 of the canonical PolicyDocumentV1 bytes (equals plan.policyDigest); waiverSetDigest = raw SHA-256 of the canonical RESOLVED WaiverSetV1 bytes (equals plan.waiverDigest); scopeDigest = raw SHA-256 of the canonical ScopeDocumentV1 bytes (the workflow glob scope-policy document, bound as an analysis-spec parameter; distinct from plan.scopeDigest, which is the foundation scope-descriptor). All three are retained blobs. detectorClosureIds are closure2 identities. evidenceAvailability lists the exact imports, kinds and required relations actually bound on that side.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Comparison2EvaluationContext {
    #[serde(rename = "detectorClosureIds")]
    pub detector_closure_ids: ::std::vec::Vec<Common3ClosureId>,
    #[serde(rename = "evidenceAvailability")]
    pub evidence_availability: Comparison2EvidenceAvailability,
    #[serde(rename = "policyDigest")]
    pub policy_digest: Common3Sha256Hex,
    #[serde(rename = "scopeDigest")]
    pub scope_digest: Common3Sha256Hex,
    #[serde(rename = "waiverSetDigest")]
    pub waiver_set_digest: Common3Sha256Hex,
}
///Evidence actually bound on one side. imports lists the exact import2 identities (each already binds payload content, correspondence, scope and observation digests) so that the evidence axis compares identities, not kind presence: the same kind with different payload/correspondence/scope/window is a changed axis. importKinds is derived from imports and retained for the rule evidenceUse join.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Comparison2EvidenceAvailability {
    #[serde(rename = "importKinds")]
    pub import_kinds: ::std::vec::Vec<Imported1ImportKind>,
    ///sorted ascending by importId
    pub imports: ::std::vec::Vec<Comparison2BoundImport>,
    pub relations: ::std::vec::Vec<Common3CanonicalIdentifier>,
}
///Drift-checked copy of foundation3 evaluation-deficiency required fields. Full Run replay is a prerequisite. Not a Comparison RuleDeficiency cause key.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Comparison2ExecutionDeficiency {
    pub cause: Comparison2ExecutionDeficiencyCause,
    #[serde(
        rename = "evidenceKind",
        deserialize_with = "::std::option::Option::deserialize"
    )]
    pub evidence_kind: ::std::option::Option<Comparison2ExecutionDeficiencyEvidenceKind>,
    #[serde(rename = "inputRefs")]
    pub input_refs: ::std::vec::Vec<Comparison2ExecutionDeficiencyInputRefsItem>,
    #[serde(
        rename = "nativeCause",
        deserialize_with = "::std::option::Option::deserialize"
    )]
    pub native_cause: ::std::option::Option<Comparison2ExecutionDeficiencyNativeCause>,
    #[serde(
        rename = "predicateId",
        deserialize_with = "::std::option::Option::deserialize"
    )]
    pub predicate_id: ::std::option::Option<Comparison2ExecutionDeficiencyPredicateId>,
    pub source: Comparison2ExecutionDeficiencySource,
    #[serde(
        rename = "subjectId",
        deserialize_with = "::std::option::Option::deserialize"
    )]
    pub subject_id: ::std::option::Option<Common3SubjectId>,
    #[serde(deserialize_with = "::std::option::Option::deserialize")]
    pub universe: ::std::option::Option<Comparison2ExecutionDeficiencyUniverse>,
}
///`Comparison2ExecutionDeficiencyCause`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Comparison2ExecutionDeficiencyCause(::std::string::String);
impl ::std::ops::Deref for Comparison2ExecutionDeficiencyCause {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Comparison2ExecutionDeficiencyCause>
for ::std::string::String {
    fn from(value: Comparison2ExecutionDeficiencyCause) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Comparison2ExecutionDeficiencyCause {
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
impl ::std::convert::TryFrom<&str> for Comparison2ExecutionDeficiencyCause {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Comparison2ExecutionDeficiencyCause {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Comparison2ExecutionDeficiencyCause {
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
///`Comparison2ExecutionDeficiencyEvidenceKind`
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
pub enum Comparison2ExecutionDeficiencyEvidenceKind {
    #[serde(rename = "test")]
    Test,
    #[serde(rename = "runtime")]
    Runtime,
    #[serde(rename = "history")]
    History,
    #[serde(rename = "dependency")]
    Dependency,
    #[serde(rename = "prepared")]
    Prepared,
}
impl ::std::fmt::Display for Comparison2ExecutionDeficiencyEvidenceKind {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Test => f.write_str("test"),
            Self::Runtime => f.write_str("runtime"),
            Self::History => f.write_str("history"),
            Self::Dependency => f.write_str("dependency"),
            Self::Prepared => f.write_str("prepared"),
        }
    }
}
impl ::std::str::FromStr for Comparison2ExecutionDeficiencyEvidenceKind {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "test" => Ok(Self::Test),
            "runtime" => Ok(Self::Runtime),
            "history" => Ok(Self::History),
            "dependency" => Ok(Self::Dependency),
            "prepared" => Ok(Self::Prepared),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Comparison2ExecutionDeficiencyEvidenceKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Comparison2ExecutionDeficiencyEvidenceKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Comparison2ExecutionDeficiencyInputRefsItem`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Comparison2ExecutionDeficiencyInputRefsItem {
    pub digest: Common3Sha256Hex,
    pub domain: Comparison2ExecutionDeficiencyInputRefsItemDomain,
}
///`Comparison2ExecutionDeficiencyInputRefsItemDomain`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Comparison2ExecutionDeficiencyInputRefsItemDomain(::std::string::String);
impl ::std::ops::Deref for Comparison2ExecutionDeficiencyInputRefsItemDomain {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Comparison2ExecutionDeficiencyInputRefsItemDomain>
for ::std::string::String {
    fn from(value: Comparison2ExecutionDeficiencyInputRefsItemDomain) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Comparison2ExecutionDeficiencyInputRefsItemDomain {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 64usize {
            return Err("longer than 64 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str>
for Comparison2ExecutionDeficiencyInputRefsItemDomain {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Comparison2ExecutionDeficiencyInputRefsItemDomain {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de>
for Comparison2ExecutionDeficiencyInputRefsItemDomain {
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
///`Comparison2ExecutionDeficiencyNativeCause`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Comparison2ExecutionDeficiencyNativeCause(::std::string::String);
impl ::std::ops::Deref for Comparison2ExecutionDeficiencyNativeCause {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Comparison2ExecutionDeficiencyNativeCause>
for ::std::string::String {
    fn from(value: Comparison2ExecutionDeficiencyNativeCause) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Comparison2ExecutionDeficiencyNativeCause {
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
impl ::std::convert::TryFrom<&str> for Comparison2ExecutionDeficiencyNativeCause {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Comparison2ExecutionDeficiencyNativeCause {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Comparison2ExecutionDeficiencyNativeCause {
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
///`Comparison2ExecutionDeficiencyPredicateId`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Comparison2ExecutionDeficiencyPredicateId(::std::string::String);
impl ::std::ops::Deref for Comparison2ExecutionDeficiencyPredicateId {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Comparison2ExecutionDeficiencyPredicateId>
for ::std::string::String {
    fn from(value: Comparison2ExecutionDeficiencyPredicateId) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Comparison2ExecutionDeficiencyPredicateId {
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
impl ::std::convert::TryFrom<&str> for Comparison2ExecutionDeficiencyPredicateId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Comparison2ExecutionDeficiencyPredicateId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Comparison2ExecutionDeficiencyPredicateId {
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
///`Comparison2ExecutionDeficiencySource`
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
pub enum Comparison2ExecutionDeficiencySource {
    #[serde(rename = "enumeration")]
    Enumeration,
    #[serde(rename = "native")]
    Native,
    #[serde(rename = "import")]
    Import,
    #[serde(rename = "execution")]
    Execution,
    #[serde(rename = "correspondence")]
    Correspondence,
}
impl ::std::fmt::Display for Comparison2ExecutionDeficiencySource {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Enumeration => f.write_str("enumeration"),
            Self::Native => f.write_str("native"),
            Self::Import => f.write_str("import"),
            Self::Execution => f.write_str("execution"),
            Self::Correspondence => f.write_str("correspondence"),
        }
    }
}
impl ::std::str::FromStr for Comparison2ExecutionDeficiencySource {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "enumeration" => Ok(Self::Enumeration),
            "native" => Ok(Self::Native),
            "import" => Ok(Self::Import),
            "execution" => Ok(Self::Execution),
            "correspondence" => Ok(Self::Correspondence),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Comparison2ExecutionDeficiencySource {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Comparison2ExecutionDeficiencySource {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Comparison2ExecutionDeficiencyUniverse`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Comparison2ExecutionDeficiencyUniverse(::std::string::String);
impl ::std::ops::Deref for Comparison2ExecutionDeficiencyUniverse {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Comparison2ExecutionDeficiencyUniverse>
for ::std::string::String {
    fn from(value: Comparison2ExecutionDeficiencyUniverse) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Comparison2ExecutionDeficiencyUniverse {
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
impl ::std::convert::TryFrom<&str> for Comparison2ExecutionDeficiencyUniverse {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Comparison2ExecutionDeficiencyUniverse {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Comparison2ExecutionDeficiencyUniverse {
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
///`Comparison2IndeterminateReason`
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
pub enum Comparison2IndeterminateReason {
    #[serde(rename = "pivot-detector-unavailable")]
    PivotDetectorUnavailable,
    #[serde(rename = "pivot-closure-revoked")]
    PivotClosureRevoked,
    #[serde(rename = "pivot-closure-incompatible")]
    PivotClosureIncompatible,
    #[serde(rename = "pivot-run-not-committed")]
    PivotRunNotCommitted,
    #[serde(rename = "pivot-detector-nondeterministic")]
    PivotDetectorNondeterministic,
    #[serde(rename = "pivot-reevaluation-unavailable")]
    PivotReevaluationUnavailable,
    #[serde(rename = "baseline-recipe-unsupported")]
    BaselineRecipeUnsupported,
    #[serde(rename = "baseline-project-unmapped")]
    BaselineProjectUnmapped,
    #[serde(rename = "baseline-context-document-missing")]
    BaselineContextDocumentMissing,
    #[serde(rename = "baseline-schema-major-unsupported")]
    BaselineSchemaMajorUnsupported,
    #[serde(rename = "required-evidence-unavailable")]
    RequiredEvidenceUnavailable,
    #[serde(rename = "evidence-availability-changed")]
    EvidenceAvailabilityChanged,
    #[serde(rename = "evidence-content-changed")]
    EvidenceContentChanged,
    #[serde(rename = "fingerprint-migration-only")]
    FingerprintMigrationOnly,
    #[serde(rename = "baseline-absence-unknown")]
    BaselineAbsenceUnknown,
    #[serde(rename = "current-absence-unknown")]
    CurrentAbsenceUnknown,
}
impl ::std::fmt::Display for Comparison2IndeterminateReason {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::PivotDetectorUnavailable => f.write_str("pivot-detector-unavailable"),
            Self::PivotClosureRevoked => f.write_str("pivot-closure-revoked"),
            Self::PivotClosureIncompatible => f.write_str("pivot-closure-incompatible"),
            Self::PivotRunNotCommitted => f.write_str("pivot-run-not-committed"),
            Self::PivotDetectorNondeterministic => {
                f.write_str("pivot-detector-nondeterministic")
            }
            Self::PivotReevaluationUnavailable => {
                f.write_str("pivot-reevaluation-unavailable")
            }
            Self::BaselineRecipeUnsupported => f.write_str("baseline-recipe-unsupported"),
            Self::BaselineProjectUnmapped => f.write_str("baseline-project-unmapped"),
            Self::BaselineContextDocumentMissing => {
                f.write_str("baseline-context-document-missing")
            }
            Self::BaselineSchemaMajorUnsupported => {
                f.write_str("baseline-schema-major-unsupported")
            }
            Self::RequiredEvidenceUnavailable => {
                f.write_str("required-evidence-unavailable")
            }
            Self::EvidenceAvailabilityChanged => {
                f.write_str("evidence-availability-changed")
            }
            Self::EvidenceContentChanged => f.write_str("evidence-content-changed"),
            Self::FingerprintMigrationOnly => f.write_str("fingerprint-migration-only"),
            Self::BaselineAbsenceUnknown => f.write_str("baseline-absence-unknown"),
            Self::CurrentAbsenceUnknown => f.write_str("current-absence-unknown"),
        }
    }
}
impl ::std::str::FromStr for Comparison2IndeterminateReason {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "pivot-detector-unavailable" => Ok(Self::PivotDetectorUnavailable),
            "pivot-closure-revoked" => Ok(Self::PivotClosureRevoked),
            "pivot-closure-incompatible" => Ok(Self::PivotClosureIncompatible),
            "pivot-run-not-committed" => Ok(Self::PivotRunNotCommitted),
            "pivot-detector-nondeterministic" => Ok(Self::PivotDetectorNondeterministic),
            "pivot-reevaluation-unavailable" => Ok(Self::PivotReevaluationUnavailable),
            "baseline-recipe-unsupported" => Ok(Self::BaselineRecipeUnsupported),
            "baseline-project-unmapped" => Ok(Self::BaselineProjectUnmapped),
            "baseline-context-document-missing" => {
                Ok(Self::BaselineContextDocumentMissing)
            }
            "baseline-schema-major-unsupported" => {
                Ok(Self::BaselineSchemaMajorUnsupported)
            }
            "required-evidence-unavailable" => Ok(Self::RequiredEvidenceUnavailable),
            "evidence-availability-changed" => Ok(Self::EvidenceAvailabilityChanged),
            "evidence-content-changed" => Ok(Self::EvidenceContentChanged),
            "fingerprint-migration-only" => Ok(Self::FingerprintMigrationOnly),
            "baseline-absence-unknown" => Ok(Self::BaselineAbsenceUnknown),
            "current-absence-unknown" => Ok(Self::CurrentAbsenceUnknown),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Comparison2IndeterminateReason {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Comparison2IndeterminateReason {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Presence knowledge of the fingerprint at each pivot. true = a known matched occurrence (waived included). false = non-selection (that side's policy does not enable the rule or its ScopeDocument does not select the path; attributed to the policy or scope axis, never CODE-FIXED) or evaluated absence proved by that side's rule under the complete-hit-set law (enabled rule, evaluated, complete enumeration, every selected emitWhen root determinate, fingerprint absent from the emitted matched set, path inside the attested extent, no unmatched occurrence at that side that might be the fingerprint). null = not known. No fingerprint is minted for an unmatched occurrence. B is evaluated-absent only when the baseline RuleCoverage absenceKnowledge is complete-hit-set. waivedB/waivedC record waiver status on the two real sides.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Comparison2PivotPresence {
    #[serde(rename = "B", deserialize_with = "::std::option::Option::deserialize")]
    pub b: ::std::option::Option<bool>,
    #[serde(rename = "E0", deserialize_with = "::std::option::Option::deserialize")]
    pub e0: ::std::option::Option<bool>,
    #[serde(rename = "E1", deserialize_with = "::std::option::Option::deserialize")]
    pub e1: ::std::option::Option<bool>,
    #[serde(rename = "E2", deserialize_with = "::std::option::Option::deserialize")]
    pub e2: ::std::option::Option<bool>,
    #[serde(rename = "E3", deserialize_with = "::std::option::Option::deserialize")]
    pub e3: ::std::option::Option<bool>,
    #[serde(rename = "E4", deserialize_with = "::std::option::Option::deserialize")]
    pub e4: ::std::option::Option<bool>,
    #[serde(rename = "waivedB")]
    pub waived_b: bool,
    #[serde(rename = "waivedC")]
    pub waived_c: bool,
}
///Explicit successor to versioning-policy.v8.json#comparisonSchema.ComparisonResult. Attribution follows a fixed pivot chain over CURRENT source: E0 = (prior detector, prior policy, prior scope, prior waivers); E1 = (current detector, prior policy/scope/waivers); E2 = (current detector, current policy, prior scope/waivers); E3 = (current detector/policy/scope, prior waivers); E4 = current Run. Baseline B is the artifact's entry set. Each entry's classification is the FIRST axis in the order code→detection→policy→scope→waiver at which its presence (or waived status, for the waiver axis) changes, and later axes are recorded in subsequentDeltas, so a code regression cannot be hidden under a simultaneous policy, scope, waiver or evidence change. E1..E3 are pure re-evaluations of retained current facts under the baseline's embedded context documents (fresh CI needs no origin store). E0 requires a runnable admitted prior detector closure; when it is unavailable and the detector changed without a declared exact semantic compatibility, every entry of that detector is INDETERMINATE with a typed reason. Gate semantics are selected by the named audit profile, never by enum precedence. Whole-comparison indeterminacy performs no comparison and emits zero entries. Evaluator3: schemaMajor 2 because unmatchedOccurrences and correspondenceCoverage are identity-bearing. Unmatched records are not classified as UNCHANGED, CODE-NET-NEW, CODE-FIXED or resolved. Known matched CODE-NET-NEW still fails even when gating correspondence deficiencies exist. Historical schemaMajor 1 is refused, never coerced to empty unmatched.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Comparison2Root {
    #[serde(rename = "comparisonResultId")]
    pub comparison_result_id: Common3ComparisonResultId,
    pub descriptor: Comparison2ComparisonDescriptor,
}
///`Comparison2RuleCoverage`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Comparison2RuleCoverage {
    ///complete-hit-set when this side can prove absence of a non-emitted fingerprint of the rule: enabled, not budget-exhausted, outcome not indeterminate, complete enumeration and every selected emitWhen root determinate. Otherwise unknown (including disabled rules). Independent of requiredCoverage.
    #[serde(rename = "absenceKnowledge")]
    pub absence_knowledge: Comparison2RuleCoverageAbsenceKnowledge,
    pub enabled: bool,
    #[serde(rename = "evidenceUse")]
    pub evidence_use: ::std::vec::Vec<Policy1EvidenceUse>,
    ///true when the rule's effective severity under this side's policy fails the gate
    pub gating: bool,
    #[serde(rename = "requiredCoverage")]
    pub required_coverage: Common3RequiredCoverage,
    #[serde(rename = "ruleId")]
    pub rule_id: Common3CanonicalIdentifier,
}
///complete-hit-set when this side can prove absence of a non-emitted fingerprint of the rule: enabled, not budget-exhausted, outcome not indeterminate, complete enumeration and every selected emitWhen root determinate. Otherwise unknown (including disabled rules). Independent of requiredCoverage.
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
pub enum Comparison2RuleCoverageAbsenceKnowledge {
    #[serde(rename = "complete-hit-set")]
    CompleteHitSet,
    #[serde(rename = "unknown")]
    Unknown,
}
impl ::std::fmt::Display for Comparison2RuleCoverageAbsenceKnowledge {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::CompleteHitSet => f.write_str("complete-hit-set"),
            Self::Unknown => f.write_str("unknown"),
        }
    }
}
impl ::std::str::FromStr for Comparison2RuleCoverageAbsenceKnowledge {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "complete-hit-set" => Ok(Self::CompleteHitSet),
            "unknown" => Ok(Self::Unknown),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Comparison2RuleCoverageAbsenceKnowledge {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Comparison2RuleCoverageAbsenceKnowledge {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Current-side rule deficiency independent of classified matched entries. correspondence-incomplete covers unmatched findings and semantic population unknown (unavailable inventory record or no-covering-program) including zero-finding rules. A missing expected inventory POINTER is not this cause: that is structural admission refusal.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Comparison2RuleDeficiency {
    pub cause: Comparison2RuleDeficiencyCause,
    pub gating: bool,
    #[serde(rename = "ruleId")]
    pub rule_id: Common3CanonicalIdentifier,
}
///`Comparison2RuleDeficiencyCause`
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
pub enum Comparison2RuleDeficiencyCause {
    #[serde(rename = "required-coverage-unsatisfied")]
    RequiredCoverageUnsatisfied,
    #[serde(rename = "required-coverage-unknown")]
    RequiredCoverageUnknown,
    #[serde(rename = "required-evidence-unavailable")]
    RequiredEvidenceUnavailable,
    #[serde(rename = "correspondence-incomplete")]
    CorrespondenceIncomplete,
}
impl ::std::fmt::Display for Comparison2RuleDeficiencyCause {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::RequiredCoverageUnsatisfied => {
                f.write_str("required-coverage-unsatisfied")
            }
            Self::RequiredCoverageUnknown => f.write_str("required-coverage-unknown"),
            Self::RequiredEvidenceUnavailable => {
                f.write_str("required-evidence-unavailable")
            }
            Self::CorrespondenceIncomplete => f.write_str("correspondence-incomplete"),
        }
    }
}
impl ::std::str::FromStr for Comparison2RuleDeficiencyCause {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "required-coverage-unsatisfied" => Ok(Self::RequiredCoverageUnsatisfied),
            "required-coverage-unknown" => Ok(Self::RequiredCoverageUnknown),
            "required-evidence-unavailable" => Ok(Self::RequiredEvidenceUnavailable),
            "correspondence-incomplete" => Ok(Self::CorrespondenceIncomplete),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Comparison2RuleDeficiencyCause {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Comparison2RuleDeficiencyCause {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`ConfigurationDisclosure1Root`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct ConfigurationDisclosure1Root {
    pub fields: ConfigurationDisclosure1RootFields,
    pub limitations: ::serde_json::Value,
    pub policy: ::serde_json::Value,
    pub provenance: ConfigurationDisclosure1RootProvenance,
    #[serde(rename = "schemaFamily")]
    pub schema_family: ::serde_json::Value,
    #[serde(rename = "schemaMajor")]
    pub schema_major: ExactInteger,
    pub source: ConfigurationDisclosure1RootSource,
}
///`ConfigurationDisclosure1RootFields`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct ConfigurationDisclosure1RootFields {
    #[serde(rename = "analysis.budget")]
    pub analysis_budget: ConfigurationDisclosure1RootFieldsAnalysisBudget,
    #[serde(rename = "analysis.capabilities")]
    pub analysis_capabilities: ConfigurationDisclosure1RootFieldsAnalysisCapabilities,
    #[serde(rename = "analysis.profileId")]
    pub analysis_profile_id: ConfigurationDisclosure1RootFieldsAnalysisProfileId,
    #[serde(rename = "components.allowedScopes")]
    pub components_allowed_scopes: ConfigurationDisclosure1RootFieldsComponentsAllowedScopes,
    #[serde(rename = "components.holds")]
    pub components_holds: ConfigurationDisclosure1RootFieldsComponentsHolds,
    #[serde(rename = "components.pins")]
    pub components_pins: ConfigurationDisclosure1RootFieldsComponentsPins,
    #[serde(rename = "components.request")]
    pub components_request: ConfigurationDisclosure1RootFieldsComponentsRequest,
    #[serde(rename = "discovery.entryPoints")]
    pub discovery_entry_points: ConfigurationDisclosure1RootFieldsDiscoveryEntryPoints,
    #[serde(rename = "discovery.ignorePaths")]
    pub discovery_ignore_paths: ConfigurationDisclosure1RootFieldsDiscoveryIgnorePaths,
    #[serde(rename = "discovery.workspaceRoots")]
    pub discovery_workspace_roots: ConfigurationDisclosure1RootFieldsDiscoveryWorkspaceRoots,
    #[serde(rename = "evidence.importIds")]
    pub evidence_import_ids: ConfigurationDisclosure1RootFieldsEvidenceImportIds,
    #[serde(rename = "policy.packIds")]
    pub policy_pack_ids: ConfigurationDisclosure1RootFieldsPolicyPackIds,
    #[serde(rename = "policy.waiverIds")]
    pub policy_waiver_ids: ConfigurationDisclosure1RootFieldsPolicyWaiverIds,
}
///`ConfigurationDisclosure1RootFieldsAnalysisBudget`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct ConfigurationDisclosure1RootFieldsAnalysisBudget {
    pub field: ::serde_json::Value,
    pub state: ::serde_json::Value,
    pub value: ConfigurationDisclosure1RootFieldsAnalysisBudgetValue,
}
///The deterministic analysis budget. identity-and-evidence section 3 requires plan.budget to equal this value exactly and by type; an override is made here first so both committed places agree.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct ConfigurationDisclosure1RootFieldsAnalysisBudgetValue {
    pub limit: ::std::num::NonZeroU64,
    pub unit: ::serde_json::Value,
}
///`ConfigurationDisclosure1RootFieldsAnalysisCapabilities`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct ConfigurationDisclosure1RootFieldsAnalysisCapabilities {
    pub field: ::serde_json::Value,
    #[serde(rename = "itemCount")]
    pub item_count: i64,
    pub reason: ::serde_json::Value,
    pub state: ::serde_json::Value,
}
///`ConfigurationDisclosure1RootFieldsAnalysisProfileId`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct ConfigurationDisclosure1RootFieldsAnalysisProfileId {
    pub field: ::serde_json::Value,
    pub reason: ::serde_json::Value,
    pub state: ::serde_json::Value,
}
///`ConfigurationDisclosure1RootFieldsComponentsAllowedScopes`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(tag = "state", deny_unknown_fields)]
pub enum ConfigurationDisclosure1RootFieldsComponentsAllowedScopes {
    #[serde(rename = "disclosed")]
    Disclosed {
        field: ::serde_json::Value,
        value: ConfigurationDisclosure1RootFieldsComponentsAllowedScopesValue,
    },
    #[serde(rename = "not-present")]
    NotPresent { field: ::serde_json::Value },
}
///`ConfigurationDisclosure1RootFieldsComponentsAllowedScopesValue`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(untagged)]
pub enum ConfigurationDisclosure1RootFieldsComponentsAllowedScopesValue {
    Variant0(::serde_json::Value),
    Variant1(::serde_json::Value),
}
///`ConfigurationDisclosure1RootFieldsComponentsHolds`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(tag = "state", deny_unknown_fields)]
pub enum ConfigurationDisclosure1RootFieldsComponentsHolds {
    #[serde(rename = "redacted")]
    Redacted {
        field: ::serde_json::Value,
        #[serde(rename = "itemCount")]
        item_count: i64,
        reason: ::serde_json::Value,
    },
    #[serde(rename = "not-present")]
    NotPresent { field: ::serde_json::Value },
}
///`ConfigurationDisclosure1RootFieldsComponentsPins`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(tag = "state", deny_unknown_fields)]
pub enum ConfigurationDisclosure1RootFieldsComponentsPins {
    #[serde(rename = "redacted")]
    Redacted {
        field: ::serde_json::Value,
        #[serde(rename = "itemCount")]
        item_count: i64,
        reason: ::serde_json::Value,
    },
    #[serde(rename = "not-present")]
    NotPresent { field: ::serde_json::Value },
}
///`ConfigurationDisclosure1RootFieldsComponentsRequest`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(tag = "state", deny_unknown_fields)]
pub enum ConfigurationDisclosure1RootFieldsComponentsRequest {
    #[serde(rename = "redacted")]
    Redacted {
        field: ::serde_json::Value,
        #[serde(rename = "itemCount")]
        item_count: ::std::num::NonZeroU64,
        reason: ::serde_json::Value,
    },
    #[serde(rename = "not-present")]
    NotPresent { field: ::serde_json::Value },
}
///`ConfigurationDisclosure1RootFieldsDiscoveryEntryPoints`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(tag = "state", deny_unknown_fields)]
pub enum ConfigurationDisclosure1RootFieldsDiscoveryEntryPoints {
    #[serde(rename = "redacted")]
    Redacted {
        field: ::serde_json::Value,
        #[serde(rename = "itemCount")]
        item_count: i64,
        reason: ::serde_json::Value,
    },
    #[serde(rename = "not-present")]
    NotPresent { field: ::serde_json::Value },
}
///`ConfigurationDisclosure1RootFieldsDiscoveryIgnorePaths`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(tag = "state", deny_unknown_fields)]
pub enum ConfigurationDisclosure1RootFieldsDiscoveryIgnorePaths {
    #[serde(rename = "redacted")]
    Redacted {
        field: ::serde_json::Value,
        #[serde(rename = "itemCount")]
        item_count: i64,
        reason: ::serde_json::Value,
    },
    #[serde(rename = "not-present")]
    NotPresent { field: ::serde_json::Value },
}
///`ConfigurationDisclosure1RootFieldsDiscoveryWorkspaceRoots`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(tag = "state", deny_unknown_fields)]
pub enum ConfigurationDisclosure1RootFieldsDiscoveryWorkspaceRoots {
    #[serde(rename = "redacted")]
    Redacted {
        field: ::serde_json::Value,
        #[serde(rename = "itemCount")]
        item_count: i64,
        reason: ::serde_json::Value,
    },
    #[serde(rename = "not-present")]
    NotPresent { field: ::serde_json::Value },
}
///`ConfigurationDisclosure1RootFieldsEvidenceImportIds`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(tag = "state", deny_unknown_fields)]
pub enum ConfigurationDisclosure1RootFieldsEvidenceImportIds {
    #[serde(rename = "redacted")]
    Redacted {
        field: ::serde_json::Value,
        #[serde(rename = "itemCount")]
        item_count: i64,
        reason: ::serde_json::Value,
    },
    #[serde(rename = "not-present")]
    NotPresent { field: ::serde_json::Value },
}
///`ConfigurationDisclosure1RootFieldsPolicyPackIds`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(tag = "state", deny_unknown_fields)]
pub enum ConfigurationDisclosure1RootFieldsPolicyPackIds {
    #[serde(rename = "redacted")]
    Redacted {
        field: ::serde_json::Value,
        #[serde(rename = "itemCount")]
        item_count: i64,
        reason: ::serde_json::Value,
    },
    #[serde(rename = "not-present")]
    NotPresent { field: ::serde_json::Value },
}
///`ConfigurationDisclosure1RootFieldsPolicyWaiverIds`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(tag = "state", deny_unknown_fields)]
pub enum ConfigurationDisclosure1RootFieldsPolicyWaiverIds {
    #[serde(rename = "redacted")]
    Redacted {
        field: ::serde_json::Value,
        #[serde(rename = "itemCount")]
        item_count: i64,
        reason: ::serde_json::Value,
    },
    #[serde(rename = "not-present")]
    NotPresent { field: ::serde_json::Value },
}
///`ConfigurationDisclosure1RootProvenance`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct ConfigurationDisclosure1RootProvenance {
    #[serde(rename = "hostAsserted")]
    pub host_asserted: ::serde_json::Value,
    #[serde(rename = "verifiedInDocument")]
    pub verified_in_document: ::serde_json::Value,
}
///`ConfigurationDisclosure1RootSource`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct ConfigurationDisclosure1RootSource {
    pub kind: ::serde_json::Value,
    #[serde(rename = "planId")]
    pub plan_id: ::std::string::String,
    #[serde(rename = "resolvedConfigDigest")]
    pub resolved_config_digest: ::std::string::String,
}
///baseline show: the admitted baseline:2 artifact and one availability row per descriptor pivotClosure entry, in descriptor order.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope3BaselineInspectionRecordV1 {
    pub baseline: Baseline2Root,
    #[serde(rename = "pivotClosureAvailability")]
    pub pivot_closure_availability: ::std::vec::Vec<Envelope3PivotClosureAvailabilityV1>,
    pub surface: ::serde_json::Value,
}
///inspect: the review:2 InspectionBundle of one candidate of an admitted Run.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope3CandidateInspectionRecordV1 {
    pub context: Graph3GraphQueryResponseContext,
    pub inspection: Review2InspectionBundle,
    pub surface: ::serde_json::Value,
}
///candidates: review:2 Candidate records of one admitted Run with the owner non-graph context.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope3CandidateListRecordV1 {
    pub candidates: ::std::vec::Vec<Review2Candidate>,
    pub context: Graph3GraphQueryResponseContext,
    #[serde(rename = "evidenceLevels")]
    pub evidence_levels: Envelope3EvidenceLevelCountsV1,
    #[serde(rename = "includeSuppressed")]
    pub include_suppressed: bool,
    #[serde(rename = "suppressedCount")]
    pub suppressed_count: Common3Uint53,
    pub surface: ::serde_json::Value,
}
///The only config2 proposal this surface emits: explicit discovery.workspaceRoots (native explicit-root spelling) pinning discovered units. Every root normalizes to a discovered unit rootPath and unitOrdinals are exactly those units. Other config2 keys have no published config2 document schema and are not proposed.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope3Config2WorkspaceRootsProposalV1 {
    pub key: ::serde_json::Value,
    #[serde(rename = "unitOrdinals")]
    pub unit_ordinals: ::std::vec::Vec<i64>,
    #[serde(rename = "workspaceRoots")]
    pub workspace_roots: ::std::vec::Vec<
        Envelope3Config2WorkspaceRootsProposalV1WorkspaceRootsItem,
    >,
}
///`Envelope3Config2WorkspaceRootsProposalV1WorkspaceRootsItem`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Envelope3Config2WorkspaceRootsProposalV1WorkspaceRootsItem(
    ::std::string::String,
);
impl ::std::ops::Deref for Envelope3Config2WorkspaceRootsProposalV1WorkspaceRootsItem {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Envelope3Config2WorkspaceRootsProposalV1WorkspaceRootsItem>
for ::std::string::String {
    fn from(value: Envelope3Config2WorkspaceRootsProposalV1WorkspaceRootsItem) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Envelope3Config2WorkspaceRootsProposalV1WorkspaceRootsItem {
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
impl ::std::convert::TryFrom<&str>
for Envelope3Config2WorkspaceRootsProposalV1WorkspaceRootsItem {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Envelope3Config2WorkspaceRootsProposalV1WorkspaceRootsItem {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de>
for Envelope3Config2WorkspaceRootsProposalV1WorkspaceRootsItem {
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
///recommend: native UnitDiscoveryV2 admitted under the security boundary inventory, registered advisory details, and config2 proposals. Advisory only.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope3DiscoveryRecommendationRecordV1 {
    pub advisory: ::serde_json::Value,
    #[serde(rename = "config2Proposals")]
    pub config2_proposals: ::std::vec::Vec<Envelope3Config2WorkspaceRootsProposalV1>,
    pub discovery: Native2UnitDiscoveryV2,
    ///Zero rows in this profile: no recommendation detail is registered. The only advisory next step is the explicit discovery.workspaceRoots config2 proposal. A recommendation vocabulary requires registered details and a successor of this record.
    pub recommendations: ::std::vec::Vec<Common3DomainDetail>,
    pub surface: ::serde_json::Value,
}
///policy show: the admitted tracked policy, the resolved effective waiver set and its resolution disclosure, with their document digests.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope3EffectivePolicyRecordV1 {
    #[serde(rename = "effectiveWaivers")]
    pub effective_waivers: Policy1WaiverSetV1,
    pub policy: Policy2PolicyDocumentV2,
    #[serde(rename = "policyDigest")]
    pub policy_digest: Common3Sha256Hex,
    pub surface: ::serde_json::Value,
    #[serde(rename = "waiverResolution")]
    pub waiver_resolution: Policy1WaiverResolutionV1,
    #[serde(rename = "waiverSetDigest")]
    pub waiver_set_digest: Common3Sha256Hex,
}
///Count of listed candidates per review:2 EvidenceLevel.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope3EvidenceLevelCountsV1 {
    #[serde(rename = "advisory-only")]
    pub advisory_only: Common3Uint53,
    #[serde(rename = "partial-coverage")]
    pub partial_coverage: Common3Uint53,
    #[serde(rename = "proof-backed")]
    pub proof_backed: Common3Uint53,
}
///`Envelope3MutationReceiptProjection`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope3MutationReceiptProjection {
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub after: FieldPresence<::std::option::Option<Common3Sha256Hex>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub before: FieldPresence<::std::option::Option<Common3Sha256Hex>>,
    #[serde(rename = "commitClass")]
    pub commit_class: Envelope3MutationReceiptProjectionCommitClass,
    #[serde(rename = "effectOutcome")]
    pub effect_outcome: Envelope3MutationReceiptProjectionEffectOutcome,
    pub operation: Repair2MutationOperation,
    #[serde(rename = "receiptId")]
    pub receipt_id: Common3ReceiptId,
    pub replayed: bool,
    #[serde(
        rename = "verificationRunId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub verification_run_id: FieldPresence<::std::option::Option<Common3RunId>>,
}
///`Envelope3MutationReceiptProjectionCommitClass`
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
pub enum Envelope3MutationReceiptProjectionCommitClass {
    #[serde(rename = "REVERSIBLE")]
    Reversible,
    #[serde(rename = "IRREVERSIBLE")]
    Irreversible,
}
impl ::std::fmt::Display for Envelope3MutationReceiptProjectionCommitClass {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Reversible => f.write_str("REVERSIBLE"),
            Self::Irreversible => f.write_str("IRREVERSIBLE"),
        }
    }
}
impl ::std::str::FromStr for Envelope3MutationReceiptProjectionCommitClass {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "REVERSIBLE" => Ok(Self::Reversible),
            "IRREVERSIBLE" => Ok(Self::Irreversible),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Envelope3MutationReceiptProjectionCommitClass {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Envelope3MutationReceiptProjectionCommitClass {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Envelope3MutationReceiptProjectionEffectOutcome`
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
pub enum Envelope3MutationReceiptProjectionEffectOutcome {
    #[serde(rename = "COMPLETED")]
    Completed,
    #[serde(rename = "FAILED")]
    Failed,
    #[serde(rename = "INDETERMINATE")]
    Indeterminate,
}
impl ::std::fmt::Display for Envelope3MutationReceiptProjectionEffectOutcome {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Completed => f.write_str("COMPLETED"),
            Self::Failed => f.write_str("FAILED"),
            Self::Indeterminate => f.write_str("INDETERMINATE"),
        }
    }
}
impl ::std::str::FromStr for Envelope3MutationReceiptProjectionEffectOutcome {
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
impl ::std::convert::TryFrom<&str> for Envelope3MutationReceiptProjectionEffectOutcome {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Envelope3MutationReceiptProjectionEffectOutcome {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Current-trust resolution of one pivot closure: missing (BASELINE.PIVOT_DETECTOR_UNAVAILABLE), revoked (BASELINE.PIVOT_CLOSURE_REVOKED), incompatible protocol major or platform (BASELINE.PIVOT_CLOSURE_INCOMPATIBLE), or available with its trust origin.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope3PivotClosureAvailabilityV1 {
    #[serde(rename = "closureId")]
    pub closure_id: Common3ClosureId,
    pub kind: Baseline2PivotClosureEntryPropertiesKind,
    pub state: Envelope3PivotClosureAvailabilityV1State,
    #[serde(
        rename = "trustOrigin",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub trust_origin: FieldPresence<
        ::std::option::Option<Envelope3PivotClosureAvailabilityV1TrustOrigin>,
    >,
}
///`Envelope3PivotClosureAvailabilityV1State`
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
pub enum Envelope3PivotClosureAvailabilityV1State {
    #[serde(rename = "available")]
    Available,
    #[serde(rename = "missing")]
    Missing,
    #[serde(rename = "revoked")]
    Revoked,
    #[serde(rename = "incompatible")]
    Incompatible,
}
impl ::std::fmt::Display for Envelope3PivotClosureAvailabilityV1State {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Available => f.write_str("available"),
            Self::Missing => f.write_str("missing"),
            Self::Revoked => f.write_str("revoked"),
            Self::Incompatible => f.write_str("incompatible"),
        }
    }
}
impl ::std::str::FromStr for Envelope3PivotClosureAvailabilityV1State {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "available" => Ok(Self::Available),
            "missing" => Ok(Self::Missing),
            "revoked" => Ok(Self::Revoked),
            "incompatible" => Ok(Self::Incompatible),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Envelope3PivotClosureAvailabilityV1State {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Envelope3PivotClosureAvailabilityV1State {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Envelope3PivotClosureAvailabilityV1TrustOrigin`
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
pub enum Envelope3PivotClosureAvailabilityV1TrustOrigin {
    #[serde(rename = "retained-generation")]
    RetainedGeneration,
    #[serde(rename = "installed-signed-release")]
    InstalledSignedRelease,
    #[serde(rename = "signed-closure-bundle")]
    SignedClosureBundle,
}
impl ::std::fmt::Display for Envelope3PivotClosureAvailabilityV1TrustOrigin {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::RetainedGeneration => f.write_str("retained-generation"),
            Self::InstalledSignedRelease => f.write_str("installed-signed-release"),
            Self::SignedClosureBundle => f.write_str("signed-closure-bundle"),
        }
    }
}
impl ::std::str::FromStr for Envelope3PivotClosureAvailabilityV1TrustOrigin {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "retained-generation" => Ok(Self::RetainedGeneration),
            "installed-signed-release" => Ok(Self::InstalledSignedRelease),
            "signed-closure-bundle" => Ok(Self::SignedClosureBundle),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Envelope3PivotClosureAvailabilityV1TrustOrigin {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Envelope3PivotClosureAvailabilityV1TrustOrigin {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///policy test: the complete PolicyTestResultV1 of a resolver-accepted evaluator3 PolicyTestSuiteV2 (urn:opensip:product-v1:workflows:evaluator3:policy-test:2). A suite or candidate policy of another major terminates request-rejected REQUEST.SCHEMA_MAJOR_UNSUPPORTED with EVALUATION.MIXED_OUTPUT_MAJOR (golden policy-test-suite-major-unsupported); any other suite admission or resolver refusal terminates request-rejected CONFIG.INVALID with its detail (workflows-and-surfaces section 5; goldens policy-test-duplicate-waiver, policy-test-imperative-key, policy-test-suite-inadmissible). No refusal is carried here.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope3PolicyTestResultRecordV1 {
    pub result: Envelope3PolicyTestResultRecordV1Result,
    pub surface: ::serde_json::Value,
}
///`Envelope3PolicyTestResultRecordV1Result`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope3PolicyTestResultRecordV1Result {
    #[serde(rename = "candidatePolicyDigest")]
    pub candidate_policy_digest: Common1Sha256Hex,
    ///digest of the candidate after overrides; equals candidatePolicyDigest when no override applied
    #[serde(rename = "effectivePolicyDigest")]
    pub effective_policy_digest: Common1Sha256Hex,
    #[serde(rename = "enforcementUnchanged")]
    pub enforcement_unchanged: ::serde_json::Value,
    #[serde(rename = "overridesApplied")]
    pub overrides_applied: ::std::vec::Vec<PolicyTest1Override>,
    #[serde(rename = "policyTestResultId")]
    pub policy_test_result_id: Common1PolicyTestResultId,
    #[serde(rename = "resolverAccepted")]
    pub resolver_accepted: bool,
    #[serde(rename = "resolverRefusals")]
    pub resolver_refusals: ::std::vec::Vec<Common1DomainDetail>,
    pub results: ::std::vec::Vec<PolicyTest1CaseResult>,
    #[serde(rename = "schemaFamily")]
    pub schema_family: ::serde_json::Value,
    #[serde(rename = "schemaMajor")]
    pub schema_major: ExactInteger,
    ///Bare H("workflow.policy-test-suite", the complete admitted PolicyTestSuiteV1 before overrides), under identity section 3. Retain the suite preimage; not raw SHA-256 of canonical suite bytes.
    #[serde(rename = "suiteDigest")]
    pub suite_digest: Common1Sha256Hex,
    pub summary: Envelope3PolicyTestResultRecordV1ResultSummary,
    #[serde(rename = "waiverResolution")]
    pub waiver_resolution: Policy1WaiverResolutionV1,
}
///`Envelope3PolicyTestResultRecordV1ResultSummary`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope3PolicyTestResultRecordV1ResultSummary {
    pub failed: Common1Uint53,
    pub indeterminate: Common1Uint53,
    #[serde(rename = "notExecutable")]
    pub not_executable: Common1Uint53,
    pub passed: Common1Uint53,
}
///Required exactly on kind=query and equal to the command inventory queryDispatch.surface. graph-query-response carries queryResponse; every other value carries queryRecord of exactly its record type.
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
pub enum Envelope3PropertiesQuerySurface {
    #[serde(rename = "graph-query-response")]
    GraphQueryResponse,
    #[serde(rename = "discovery-recommendation")]
    DiscoveryRecommendation,
    #[serde(rename = "baseline-inspection")]
    BaselineInspection,
    #[serde(rename = "effective-policy")]
    EffectivePolicy,
    #[serde(rename = "policy-test-result")]
    PolicyTestResult,
    #[serde(rename = "candidate-list")]
    CandidateList,
    #[serde(rename = "candidate-inspection")]
    CandidateInspection,
    #[serde(rename = "review-brief")]
    ReviewBrief,
    #[serde(rename = "repair-preview")]
    RepairPreview,
}
impl ::std::fmt::Display for Envelope3PropertiesQuerySurface {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::GraphQueryResponse => f.write_str("graph-query-response"),
            Self::DiscoveryRecommendation => f.write_str("discovery-recommendation"),
            Self::BaselineInspection => f.write_str("baseline-inspection"),
            Self::EffectivePolicy => f.write_str("effective-policy"),
            Self::PolicyTestResult => f.write_str("policy-test-result"),
            Self::CandidateList => f.write_str("candidate-list"),
            Self::CandidateInspection => f.write_str("candidate-inspection"),
            Self::ReviewBrief => f.write_str("review-brief"),
            Self::RepairPreview => f.write_str("repair-preview"),
        }
    }
}
impl ::std::str::FromStr for Envelope3PropertiesQuerySurface {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "graph-query-response" => Ok(Self::GraphQueryResponse),
            "discovery-recommendation" => Ok(Self::DiscoveryRecommendation),
            "baseline-inspection" => Ok(Self::BaselineInspection),
            "effective-policy" => Ok(Self::EffectivePolicy),
            "policy-test-result" => Ok(Self::PolicyTestResult),
            "candidate-list" => Ok(Self::CandidateList),
            "candidate-inspection" => Ok(Self::CandidateInspection),
            "review-brief" => Ok(Self::ReviewBrief),
            "repair-preview" => Ok(Self::RepairPreview),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Envelope3PropertiesQuerySurface {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Envelope3PropertiesQuerySurface {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///repair preview: the invocation:3 RepairPreviewResult and the repair:2 RepairPlanV1 it names.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope3RepairPreviewRecordV1 {
    pub plan: Repair2RepairPlanV1,
    pub preview: Invocation3RepairPreviewResult,
    pub surface: ::serde_json::Value,
}
///review brief: the review:2 ReviewBrief of one admitted Run.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope3ReviewBriefRecordV1 {
    pub brief: Review2ReviewBrief,
    pub context: Graph3GraphQueryResponseContext,
    pub surface: ::serde_json::Value,
}
///Evaluator3 envelope. schemaMajor 3 because AnalysisResult.runId is run3 and the intermediate findings projection is FindingSurface (finding3, nullable fingerprint; not a SARIF result). SARIF 2.1.0 output is urn:opensip:product-v1:workflows:evaluator3:sarif-adapter:2. Consumers pin this major; major 2 envelopes are REQUEST.SCHEMA_MAJOR_UNSUPPORTED, never reshaped. Output serialization overflow uses OUTPUT.SERIALIZATION_FAILED / faultCause output-serialization. Query carrier: kind=query requires querySurface. The query command (the twenty graph-query:3 operations) selects graph-query-response and carries the complete owner-admitted GraphQueryResponseV1 in queryResponse, which is its query-response parity field; every other query-class command selects its own surface and carries queryRecord of that closed record type. Unsupported envelope majors terminate REQUEST.SCHEMA_MAJOR_UNSUPPORTED with detail OUTPUT.ENVELOPE_MAJOR_UNSUPPORTED.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope3Root {
    ///present only in the agent rendering; advisory text that never changes any parity field
    #[serde(
        rename = "agentHints",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub agent_hints: FieldPresence<::std::vec::Vec<Common3BoundedText>>,
    ///Optional. The bounded capability-availability collection of THIS invocation: every capability the selected product required that this release did not declare available, with its full ownership tuple. Present on the invocation that selected them - it is not deferred to a separate doctor report, which is a different invocation and cannot deliver these absences. Advisory only.
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub availability: FieldPresence<
        ::std::option::Option<Common3CapabilityAvailabilityV1>,
    >,
    #[serde(
        rename = "clientCorrelationId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub client_correlation_id: FieldPresence<
        ::std::option::Option<Envelope3RootClientCorrelationId>,
    >,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub diagnostics: FieldPresence<::std::vec::Vec<Common3BoundedText>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub doctor: FieldPresence<::std::option::Option<Invocation3DoctorResult>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub errors: FieldPresence<::std::vec::Vec<Common3DomainDetail>>,
    #[serde(rename = "exitCode")]
    pub exit_code: ExactInteger,
    ///Optional direct findings projection for analysis envelopes. One row per finding3. Not keyed by fingerprint.
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub findings: FieldPresence<
        ::std::option::Option<::std::vec::Vec<Common3FindingSurface>>,
    >,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub invocation: FieldPresence<::std::option::Option<Invocation3Root>>,
    pub kind: Envelope3RootKind,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub mutation: FieldPresence<
        ::std::option::Option<Envelope3MutationReceiptProjection>,
    >,
    #[serde(
        rename = "projectId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub project_id: FieldPresence<::std::option::Option<Common3ProjectId>>,
    #[serde(
        rename = "projectRoot",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub project_root: FieldPresence<::std::option::Option<Common3UserInputPath>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub query: FieldPresence<::std::option::Option<Invocation3QueryResult>>,
    ///Closed typed result of a non-graph query-class command, discriminated by surface; no untyped payload is admitted.
    #[serde(
        rename = "queryRecord",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub query_record: FieldPresence<::std::option::Option<Envelope3RootQueryRecord>>,
    ///The complete owner-admitted query response, required exactly when querySurface=graph-query-response. Cross-record joins beyond JSON Schema: context.projectId equals projectId; a present response termination equals termination; for graph.* the query summary is the owner projection of this response.
    #[serde(
        rename = "queryResponse",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub query_response: FieldPresence<::std::option::Option<Graph3GraphQueryResponseV1>>,
    ///Required exactly on kind=query and equal to the command inventory queryDispatch.surface. graph-query-response carries queryResponse; every other value carries queryRecord of exactly its record type.
    #[serde(
        rename = "querySurface",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub query_surface: FieldPresence<::std::option::Option<Envelope3RootQuerySurface>>,
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
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub run: FieldPresence<::std::option::Option<Invocation3AnalysisResult>>,
    #[serde(rename = "schemaFamily")]
    pub schema_family: ::serde_json::Value,
    #[serde(rename = "schemaMajor")]
    pub schema_major: ExactInteger,
    pub termination: Common3StepTermination,
}
///`Envelope3RootClientCorrelationId`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Envelope3RootClientCorrelationId(::std::string::String);
impl ::std::ops::Deref for Envelope3RootClientCorrelationId {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Envelope3RootClientCorrelationId> for ::std::string::String {
    fn from(value: Envelope3RootClientCorrelationId) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Envelope3RootClientCorrelationId {
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
impl ::std::convert::TryFrom<&str> for Envelope3RootClientCorrelationId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Envelope3RootClientCorrelationId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Envelope3RootClientCorrelationId {
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
///`Envelope3RootKind`
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
pub enum Envelope3RootKind {
    #[serde(rename = "run")]
    Run,
    #[serde(rename = "query")]
    Query,
    #[serde(rename = "mutation")]
    Mutation,
    #[serde(rename = "failure")]
    Failure,
    #[serde(rename = "invocation")]
    Invocation,
    #[serde(rename = "doctor")]
    Doctor,
}
impl ::std::fmt::Display for Envelope3RootKind {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Run => f.write_str("run"),
            Self::Query => f.write_str("query"),
            Self::Mutation => f.write_str("mutation"),
            Self::Failure => f.write_str("failure"),
            Self::Invocation => f.write_str("invocation"),
            Self::Doctor => f.write_str("doctor"),
        }
    }
}
impl ::std::str::FromStr for Envelope3RootKind {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "run" => Ok(Self::Run),
            "query" => Ok(Self::Query),
            "mutation" => Ok(Self::Mutation),
            "failure" => Ok(Self::Failure),
            "invocation" => Ok(Self::Invocation),
            "doctor" => Ok(Self::Doctor),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Envelope3RootKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Envelope3RootKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Closed typed result of a non-graph query-class command, discriminated by surface; no untyped payload is admitted.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(untagged)]
pub enum Envelope3RootQueryRecord {
    DiscoveryRecommendationRecordV1(Envelope3DiscoveryRecommendationRecordV1),
    BaselineInspectionRecordV1(Envelope3BaselineInspectionRecordV1),
    EffectivePolicyRecordV1(Envelope3EffectivePolicyRecordV1),
    PolicyTestResultRecordV1(Envelope3PolicyTestResultRecordV1),
    CandidateListRecordV1(Envelope3CandidateListRecordV1),
    CandidateInspectionRecordV1(Envelope3CandidateInspectionRecordV1),
    ReviewBriefRecordV1(Envelope3ReviewBriefRecordV1),
    RepairPreviewRecordV1(Envelope3RepairPreviewRecordV1),
}
impl ::std::convert::From<Envelope3DiscoveryRecommendationRecordV1>
for Envelope3RootQueryRecord {
    fn from(value: Envelope3DiscoveryRecommendationRecordV1) -> Self {
        Self::DiscoveryRecommendationRecordV1(value)
    }
}
impl ::std::convert::From<Envelope3BaselineInspectionRecordV1>
for Envelope3RootQueryRecord {
    fn from(value: Envelope3BaselineInspectionRecordV1) -> Self {
        Self::BaselineInspectionRecordV1(value)
    }
}
impl ::std::convert::From<Envelope3EffectivePolicyRecordV1>
for Envelope3RootQueryRecord {
    fn from(value: Envelope3EffectivePolicyRecordV1) -> Self {
        Self::EffectivePolicyRecordV1(value)
    }
}
impl ::std::convert::From<Envelope3PolicyTestResultRecordV1>
for Envelope3RootQueryRecord {
    fn from(value: Envelope3PolicyTestResultRecordV1) -> Self {
        Self::PolicyTestResultRecordV1(value)
    }
}
impl ::std::convert::From<Envelope3CandidateListRecordV1> for Envelope3RootQueryRecord {
    fn from(value: Envelope3CandidateListRecordV1) -> Self {
        Self::CandidateListRecordV1(value)
    }
}
impl ::std::convert::From<Envelope3CandidateInspectionRecordV1>
for Envelope3RootQueryRecord {
    fn from(value: Envelope3CandidateInspectionRecordV1) -> Self {
        Self::CandidateInspectionRecordV1(value)
    }
}
impl ::std::convert::From<Envelope3ReviewBriefRecordV1> for Envelope3RootQueryRecord {
    fn from(value: Envelope3ReviewBriefRecordV1) -> Self {
        Self::ReviewBriefRecordV1(value)
    }
}
impl ::std::convert::From<Envelope3RepairPreviewRecordV1> for Envelope3RootQueryRecord {
    fn from(value: Envelope3RepairPreviewRecordV1) -> Self {
        Self::RepairPreviewRecordV1(value)
    }
}
///Required exactly on kind=query and equal to the command inventory queryDispatch.surface. graph-query-response carries queryResponse; every other value carries queryRecord of exactly its record type.
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
pub enum Envelope3RootQuerySurface {
    #[serde(rename = "graph-query-response")]
    GraphQueryResponse,
    #[serde(rename = "discovery-recommendation")]
    DiscoveryRecommendation,
    #[serde(rename = "baseline-inspection")]
    BaselineInspection,
    #[serde(rename = "effective-policy")]
    EffectivePolicy,
    #[serde(rename = "policy-test-result")]
    PolicyTestResult,
    #[serde(rename = "candidate-list")]
    CandidateList,
    #[serde(rename = "candidate-inspection")]
    CandidateInspection,
    #[serde(rename = "review-brief")]
    ReviewBrief,
    #[serde(rename = "repair-preview")]
    RepairPreview,
}
impl ::std::fmt::Display for Envelope3RootQuerySurface {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::GraphQueryResponse => f.write_str("graph-query-response"),
            Self::DiscoveryRecommendation => f.write_str("discovery-recommendation"),
            Self::BaselineInspection => f.write_str("baseline-inspection"),
            Self::EffectivePolicy => f.write_str("effective-policy"),
            Self::PolicyTestResult => f.write_str("policy-test-result"),
            Self::CandidateList => f.write_str("candidate-list"),
            Self::CandidateInspection => f.write_str("candidate-inspection"),
            Self::ReviewBrief => f.write_str("review-brief"),
            Self::RepairPreview => f.write_str("repair-preview"),
        }
    }
}
impl ::std::str::FromStr for Envelope3RootQuerySurface {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "graph-query-response" => Ok(Self::GraphQueryResponse),
            "discovery-recommendation" => Ok(Self::DiscoveryRecommendation),
            "baseline-inspection" => Ok(Self::BaselineInspection),
            "effective-policy" => Ok(Self::EffectivePolicy),
            "policy-test-result" => Ok(Self::PolicyTestResult),
            "candidate-list" => Ok(Self::CandidateList),
            "candidate-inspection" => Ok(Self::CandidateInspection),
            "review-brief" => Ok(Self::ReviewBrief),
            "repair-preview" => Ok(Self::RepairPreview),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Envelope3RootQuerySurface {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Envelope3RootQuerySurface {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///baseline show: the admitted baseline:2 artifact and one availability row per descriptor pivotClosure entry, in descriptor order.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope4BaselineInspectionRecordV1 {
    pub baseline: Baseline2Root,
    #[serde(rename = "pivotClosureAvailability")]
    pub pivot_closure_availability: ::std::vec::Vec<Envelope4PivotClosureAvailabilityV1>,
    pub surface: ::serde_json::Value,
}
///inspect: the review:2 InspectionBundle of one candidate of an admitted Run.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope4CandidateInspectionRecordV1 {
    pub context: Graph3GraphQueryResponseContext,
    pub inspection: Review2InspectionBundle,
    pub surface: ::serde_json::Value,
}
///candidates: review:2 Candidate records of one admitted Run with the owner non-graph context.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope4CandidateListRecordV1 {
    pub candidates: ::std::vec::Vec<Review2Candidate>,
    pub context: Graph3GraphQueryResponseContext,
    #[serde(rename = "evidenceLevels")]
    pub evidence_levels: Envelope4EvidenceLevelCountsV1,
    #[serde(rename = "includeSuppressed")]
    pub include_suppressed: bool,
    #[serde(rename = "suppressedCount")]
    pub suppressed_count: Common3Uint53,
    pub surface: ::serde_json::Value,
}
///The only config2 proposal this surface emits: explicit discovery.workspaceRoots (native explicit-root spelling) pinning discovered units. Every root normalizes to a discovered unit rootPath and unitOrdinals are exactly those units. Other config2 keys have no published config2 document schema and are not proposed.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope4Config2WorkspaceRootsProposalV1 {
    pub key: ::serde_json::Value,
    #[serde(rename = "unitOrdinals")]
    pub unit_ordinals: ::std::vec::Vec<i64>,
    #[serde(rename = "workspaceRoots")]
    pub workspace_roots: ::std::vec::Vec<
        Envelope4Config2WorkspaceRootsProposalV1WorkspaceRootsItem,
    >,
}
///`Envelope4Config2WorkspaceRootsProposalV1WorkspaceRootsItem`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Envelope4Config2WorkspaceRootsProposalV1WorkspaceRootsItem(
    ::std::string::String,
);
impl ::std::ops::Deref for Envelope4Config2WorkspaceRootsProposalV1WorkspaceRootsItem {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Envelope4Config2WorkspaceRootsProposalV1WorkspaceRootsItem>
for ::std::string::String {
    fn from(value: Envelope4Config2WorkspaceRootsProposalV1WorkspaceRootsItem) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Envelope4Config2WorkspaceRootsProposalV1WorkspaceRootsItem {
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
impl ::std::convert::TryFrom<&str>
for Envelope4Config2WorkspaceRootsProposalV1WorkspaceRootsItem {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Envelope4Config2WorkspaceRootsProposalV1WorkspaceRootsItem {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de>
for Envelope4Config2WorkspaceRootsProposalV1WorkspaceRootsItem {
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
///recommend: native UnitDiscoveryV2 admitted under the security boundary inventory, registered advisory details, and config2 proposals. Advisory only.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope4DiscoveryRecommendationRecordV1 {
    pub advisory: ::serde_json::Value,
    #[serde(rename = "config2Proposals")]
    pub config2_proposals: ::std::vec::Vec<Envelope4Config2WorkspaceRootsProposalV1>,
    pub discovery: Native2UnitDiscoveryV2,
    ///Zero rows in this profile: no recommendation detail is registered. The only advisory next step is the explicit discovery.workspaceRoots config2 proposal. A recommendation vocabulary requires registered details and a successor of this record.
    pub recommendations: ::std::vec::Vec<Common3DomainDetail>,
    pub surface: ::serde_json::Value,
}
///policy show: the admitted tracked policy, the resolved effective waiver set and its resolution disclosure, with their document digests.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope4EffectivePolicyRecordV1 {
    #[serde(rename = "effectiveWaivers")]
    pub effective_waivers: Policy1WaiverSetV1,
    pub policy: Policy2PolicyDocumentV2,
    #[serde(rename = "policyDigest")]
    pub policy_digest: Common3Sha256Hex,
    pub surface: ::serde_json::Value,
    #[serde(rename = "waiverResolution")]
    pub waiver_resolution: Policy1WaiverResolutionV1,
    #[serde(rename = "waiverSetDigest")]
    pub waiver_set_digest: Common3Sha256Hex,
}
///Count of listed candidates per review:2 EvidenceLevel.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope4EvidenceLevelCountsV1 {
    #[serde(rename = "advisory-only")]
    pub advisory_only: Common3Uint53,
    #[serde(rename = "partial-coverage")]
    pub partial_coverage: Common3Uint53,
    #[serde(rename = "proof-backed")]
    pub proof_backed: Common3Uint53,
}
///`Envelope4MutationReceiptProjection`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope4MutationReceiptProjection {
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub after: FieldPresence<::std::option::Option<Common3Sha256Hex>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub before: FieldPresence<::std::option::Option<Common3Sha256Hex>>,
    #[serde(rename = "commitClass")]
    pub commit_class: Envelope4MutationReceiptProjectionCommitClass,
    #[serde(rename = "effectOutcome")]
    pub effect_outcome: Envelope4MutationReceiptProjectionEffectOutcome,
    pub operation: Repair2MutationOperation,
    #[serde(rename = "receiptId")]
    pub receipt_id: Common3ReceiptId,
    pub replayed: bool,
    #[serde(
        rename = "verificationRunId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub verification_run_id: FieldPresence<::std::option::Option<Common3RunId>>,
}
///`Envelope4MutationReceiptProjectionCommitClass`
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
pub enum Envelope4MutationReceiptProjectionCommitClass {
    #[serde(rename = "REVERSIBLE")]
    Reversible,
    #[serde(rename = "IRREVERSIBLE")]
    Irreversible,
}
impl ::std::fmt::Display for Envelope4MutationReceiptProjectionCommitClass {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Reversible => f.write_str("REVERSIBLE"),
            Self::Irreversible => f.write_str("IRREVERSIBLE"),
        }
    }
}
impl ::std::str::FromStr for Envelope4MutationReceiptProjectionCommitClass {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "REVERSIBLE" => Ok(Self::Reversible),
            "IRREVERSIBLE" => Ok(Self::Irreversible),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Envelope4MutationReceiptProjectionCommitClass {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Envelope4MutationReceiptProjectionCommitClass {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Envelope4MutationReceiptProjectionEffectOutcome`
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
pub enum Envelope4MutationReceiptProjectionEffectOutcome {
    #[serde(rename = "COMPLETED")]
    Completed,
    #[serde(rename = "FAILED")]
    Failed,
    #[serde(rename = "INDETERMINATE")]
    Indeterminate,
}
impl ::std::fmt::Display for Envelope4MutationReceiptProjectionEffectOutcome {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Completed => f.write_str("COMPLETED"),
            Self::Failed => f.write_str("FAILED"),
            Self::Indeterminate => f.write_str("INDETERMINATE"),
        }
    }
}
impl ::std::str::FromStr for Envelope4MutationReceiptProjectionEffectOutcome {
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
impl ::std::convert::TryFrom<&str> for Envelope4MutationReceiptProjectionEffectOutcome {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Envelope4MutationReceiptProjectionEffectOutcome {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Current-trust resolution of one pivot closure: missing (BASELINE.PIVOT_DETECTOR_UNAVAILABLE), revoked (BASELINE.PIVOT_CLOSURE_REVOKED), incompatible protocol major or platform (BASELINE.PIVOT_CLOSURE_INCOMPATIBLE), or available with its trust origin.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope4PivotClosureAvailabilityV1 {
    #[serde(rename = "closureId")]
    pub closure_id: Common3ClosureId,
    pub kind: Baseline2PivotClosureEntryPropertiesKind,
    pub state: Envelope4PivotClosureAvailabilityV1State,
    #[serde(
        rename = "trustOrigin",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub trust_origin: FieldPresence<
        ::std::option::Option<Envelope4PivotClosureAvailabilityV1TrustOrigin>,
    >,
}
///`Envelope4PivotClosureAvailabilityV1State`
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
pub enum Envelope4PivotClosureAvailabilityV1State {
    #[serde(rename = "available")]
    Available,
    #[serde(rename = "missing")]
    Missing,
    #[serde(rename = "revoked")]
    Revoked,
    #[serde(rename = "incompatible")]
    Incompatible,
}
impl ::std::fmt::Display for Envelope4PivotClosureAvailabilityV1State {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Available => f.write_str("available"),
            Self::Missing => f.write_str("missing"),
            Self::Revoked => f.write_str("revoked"),
            Self::Incompatible => f.write_str("incompatible"),
        }
    }
}
impl ::std::str::FromStr for Envelope4PivotClosureAvailabilityV1State {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "available" => Ok(Self::Available),
            "missing" => Ok(Self::Missing),
            "revoked" => Ok(Self::Revoked),
            "incompatible" => Ok(Self::Incompatible),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Envelope4PivotClosureAvailabilityV1State {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Envelope4PivotClosureAvailabilityV1State {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Envelope4PivotClosureAvailabilityV1TrustOrigin`
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
pub enum Envelope4PivotClosureAvailabilityV1TrustOrigin {
    #[serde(rename = "retained-generation")]
    RetainedGeneration,
    #[serde(rename = "installed-signed-release")]
    InstalledSignedRelease,
    #[serde(rename = "signed-closure-bundle")]
    SignedClosureBundle,
}
impl ::std::fmt::Display for Envelope4PivotClosureAvailabilityV1TrustOrigin {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::RetainedGeneration => f.write_str("retained-generation"),
            Self::InstalledSignedRelease => f.write_str("installed-signed-release"),
            Self::SignedClosureBundle => f.write_str("signed-closure-bundle"),
        }
    }
}
impl ::std::str::FromStr for Envelope4PivotClosureAvailabilityV1TrustOrigin {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "retained-generation" => Ok(Self::RetainedGeneration),
            "installed-signed-release" => Ok(Self::InstalledSignedRelease),
            "signed-closure-bundle" => Ok(Self::SignedClosureBundle),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Envelope4PivotClosureAvailabilityV1TrustOrigin {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Envelope4PivotClosureAvailabilityV1TrustOrigin {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///policy test: the complete PolicyTestResultV1 of a resolver-accepted evaluator3 PolicyTestSuiteV2 (urn:opensip:product-v1:workflows:evaluator3:policy-test:2). A suite or candidate policy of another major terminates request-rejected REQUEST.SCHEMA_MAJOR_UNSUPPORTED with EVALUATION.MIXED_OUTPUT_MAJOR (golden policy-test-suite-major-unsupported); any other suite admission or resolver refusal terminates request-rejected CONFIG.INVALID with its detail (workflows-and-surfaces section 5; goldens policy-test-duplicate-waiver, policy-test-imperative-key, policy-test-suite-inadmissible). No refusal is carried here.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope4PolicyTestResultRecordV1 {
    pub result: Envelope4PolicyTestResultRecordV1Result,
    pub surface: ::serde_json::Value,
}
///`Envelope4PolicyTestResultRecordV1Result`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope4PolicyTestResultRecordV1Result {
    #[serde(rename = "candidatePolicyDigest")]
    pub candidate_policy_digest: Common1Sha256Hex,
    ///digest of the candidate after overrides; equals candidatePolicyDigest when no override applied
    #[serde(rename = "effectivePolicyDigest")]
    pub effective_policy_digest: Common1Sha256Hex,
    #[serde(rename = "enforcementUnchanged")]
    pub enforcement_unchanged: ::serde_json::Value,
    #[serde(rename = "overridesApplied")]
    pub overrides_applied: ::std::vec::Vec<PolicyTest1Override>,
    #[serde(rename = "policyTestResultId")]
    pub policy_test_result_id: Common1PolicyTestResultId,
    #[serde(rename = "resolverAccepted")]
    pub resolver_accepted: bool,
    #[serde(rename = "resolverRefusals")]
    pub resolver_refusals: ::std::vec::Vec<Common1DomainDetail>,
    pub results: ::std::vec::Vec<PolicyTest1CaseResult>,
    #[serde(rename = "schemaFamily")]
    pub schema_family: ::serde_json::Value,
    #[serde(rename = "schemaMajor")]
    pub schema_major: ExactInteger,
    ///Bare H("workflow.policy-test-suite", the complete admitted PolicyTestSuiteV1 before overrides), under identity section 3. Retain the suite preimage; not raw SHA-256 of canonical suite bytes.
    #[serde(rename = "suiteDigest")]
    pub suite_digest: Common1Sha256Hex,
    pub summary: Envelope4PolicyTestResultRecordV1ResultSummary,
    #[serde(rename = "waiverResolution")]
    pub waiver_resolution: Policy1WaiverResolutionV1,
}
///`Envelope4PolicyTestResultRecordV1ResultSummary`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope4PolicyTestResultRecordV1ResultSummary {
    pub failed: Common1Uint53,
    pub indeterminate: Common1Uint53,
    #[serde(rename = "notExecutable")]
    pub not_executable: Common1Uint53,
    pub passed: Common1Uint53,
}
///repair preview: the invocation:3 RepairPreviewResult and the repair:2 RepairPlanV1 it names.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope4RepairPreviewRecordV1 {
    pub plan: Repair2RepairPlanV1,
    pub preview: Invocation3RepairPreviewResult,
    pub surface: ::serde_json::Value,
}
///review brief: the review:2 ReviewBrief of one admitted Run.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope4ReviewBriefRecordV1 {
    pub brief: Review2ReviewBrief,
    pub context: Graph3GraphQueryResponseContext,
    pub surface: ::serde_json::Value,
}
///Evaluator3 envelope. schemaMajor 3 because AnalysisResult.runId is run3 and the intermediate findings projection is FindingSurface (finding3, nullable fingerprint; not a SARIF result). SARIF 2.1.0 output is urn:opensip:product-v1:workflows:evaluator3:sarif-adapter:2. Consumers pin this major; major 2 envelopes are REQUEST.SCHEMA_MAJOR_UNSUPPORTED, never reshaped. Output serialization overflow uses OUTPUT.SERIALIZATION_FAILED / faultCause output-serialization. Query carrier: kind=query requires querySurface. The query command (the twenty graph-query:3 operations) selects graph-query-response and carries the complete owner-admitted GraphQueryResponseV1 in queryResponse, which is its query-response parity field; every other query-class command selects its own surface and carries queryRecord of that closed record type. Unsupported envelope majors terminate REQUEST.SCHEMA_MAJOR_UNSUPPORTED with detail OUTPUT.ENVELOPE_MAJOR_UNSUPPORTED. Successor major4 adds only the metadata success branch. All pre-existing evaluator3 payload constraints and semantic owners remain. Metadata failures use the existing failure branch. Metadata semantic admission also checks catalogue and compiled build selection.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope4Root {
    ///present only in the agent rendering; advisory text that never changes any parity field
    #[serde(
        rename = "agentHints",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub agent_hints: FieldPresence<::std::vec::Vec<Common3BoundedText>>,
    ///Optional. The bounded capability-availability collection of THIS invocation: every capability the selected product required that this release did not declare available, with its full ownership tuple. Present on the invocation that selected them - it is not deferred to a separate doctor report, which is a different invocation and cannot deliver these absences. Advisory only.
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub availability: FieldPresence<
        ::std::option::Option<Common3CapabilityAvailabilityV1>,
    >,
    #[serde(
        rename = "clientCorrelationId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub client_correlation_id: FieldPresence<
        ::std::option::Option<Envelope4RootClientCorrelationId>,
    >,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub diagnostics: FieldPresence<::std::vec::Vec<Common3BoundedText>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub doctor: FieldPresence<::std::option::Option<Invocation3DoctorResult>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub errors: FieldPresence<::std::vec::Vec<Common3DomainDetail>>,
    #[serde(rename = "exitCode")]
    pub exit_code: ExactInteger,
    ///Optional direct findings projection for analysis envelopes. One row per finding3. Not keyed by fingerprint.
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub findings: FieldPresence<
        ::std::option::Option<::std::vec::Vec<Common3FindingSurface>>,
    >,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub invocation: FieldPresence<::std::option::Option<Invocation3Root>>,
    pub kind: Envelope4RootKind,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub meta: FieldPresence<::std::option::Option<Metadata1Root>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub mutation: FieldPresence<
        ::std::option::Option<Envelope4MutationReceiptProjection>,
    >,
    #[serde(
        rename = "projectId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub project_id: FieldPresence<::std::option::Option<Common3ProjectId>>,
    #[serde(
        rename = "projectRoot",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub project_root: FieldPresence<::std::option::Option<Common3UserInputPath>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub query: FieldPresence<::std::option::Option<Invocation3QueryResult>>,
    ///Closed typed result of a non-graph query-class command, discriminated by surface; no untyped payload is admitted.
    #[serde(
        rename = "queryRecord",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub query_record: FieldPresence<::std::option::Option<Envelope4RootQueryRecord>>,
    ///The complete owner-admitted query response, required exactly when querySurface=graph-query-response. Cross-record joins beyond JSON Schema: context.projectId equals projectId; a present response termination equals termination; for graph.* the query summary is the owner projection of this response.
    #[serde(
        rename = "queryResponse",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub query_response: FieldPresence<::std::option::Option<Graph3GraphQueryResponseV1>>,
    ///Required exactly on kind=query and equal to the command inventory queryDispatch.surface. graph-query-response carries queryResponse; every other value carries queryRecord of exactly its record type.
    #[serde(
        rename = "querySurface",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub query_surface: FieldPresence<::std::option::Option<Envelope4RootQuerySurface>>,
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
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub run: FieldPresence<::std::option::Option<Invocation3AnalysisResult>>,
    #[serde(rename = "schemaFamily")]
    pub schema_family: ::serde_json::Value,
    #[serde(rename = "schemaMajor")]
    pub schema_major: ExactInteger,
    pub termination: Common3StepTermination,
}
///`Envelope4RootClientCorrelationId`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Envelope4RootClientCorrelationId(::std::string::String);
impl ::std::ops::Deref for Envelope4RootClientCorrelationId {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Envelope4RootClientCorrelationId> for ::std::string::String {
    fn from(value: Envelope4RootClientCorrelationId) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Envelope4RootClientCorrelationId {
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
impl ::std::convert::TryFrom<&str> for Envelope4RootClientCorrelationId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Envelope4RootClientCorrelationId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Envelope4RootClientCorrelationId {
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
///`Envelope4RootKind`
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
pub enum Envelope4RootKind {
    #[serde(rename = "run")]
    Run,
    #[serde(rename = "query")]
    Query,
    #[serde(rename = "mutation")]
    Mutation,
    #[serde(rename = "failure")]
    Failure,
    #[serde(rename = "invocation")]
    Invocation,
    #[serde(rename = "doctor")]
    Doctor,
    #[serde(rename = "meta")]
    Meta,
}
impl ::std::fmt::Display for Envelope4RootKind {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Run => f.write_str("run"),
            Self::Query => f.write_str("query"),
            Self::Mutation => f.write_str("mutation"),
            Self::Failure => f.write_str("failure"),
            Self::Invocation => f.write_str("invocation"),
            Self::Doctor => f.write_str("doctor"),
            Self::Meta => f.write_str("meta"),
        }
    }
}
impl ::std::str::FromStr for Envelope4RootKind {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "run" => Ok(Self::Run),
            "query" => Ok(Self::Query),
            "mutation" => Ok(Self::Mutation),
            "failure" => Ok(Self::Failure),
            "invocation" => Ok(Self::Invocation),
            "doctor" => Ok(Self::Doctor),
            "meta" => Ok(Self::Meta),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Envelope4RootKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Envelope4RootKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Closed typed result of a non-graph query-class command, discriminated by surface; no untyped payload is admitted.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(untagged)]
pub enum Envelope4RootQueryRecord {
    DiscoveryRecommendationRecordV1(Envelope4DiscoveryRecommendationRecordV1),
    BaselineInspectionRecordV1(Envelope4BaselineInspectionRecordV1),
    EffectivePolicyRecordV1(Envelope4EffectivePolicyRecordV1),
    PolicyTestResultRecordV1(Envelope4PolicyTestResultRecordV1),
    CandidateListRecordV1(Envelope4CandidateListRecordV1),
    CandidateInspectionRecordV1(Envelope4CandidateInspectionRecordV1),
    ReviewBriefRecordV1(Envelope4ReviewBriefRecordV1),
    RepairPreviewRecordV1(Envelope4RepairPreviewRecordV1),
}
impl ::std::convert::From<Envelope4DiscoveryRecommendationRecordV1>
for Envelope4RootQueryRecord {
    fn from(value: Envelope4DiscoveryRecommendationRecordV1) -> Self {
        Self::DiscoveryRecommendationRecordV1(value)
    }
}
impl ::std::convert::From<Envelope4BaselineInspectionRecordV1>
for Envelope4RootQueryRecord {
    fn from(value: Envelope4BaselineInspectionRecordV1) -> Self {
        Self::BaselineInspectionRecordV1(value)
    }
}
impl ::std::convert::From<Envelope4EffectivePolicyRecordV1>
for Envelope4RootQueryRecord {
    fn from(value: Envelope4EffectivePolicyRecordV1) -> Self {
        Self::EffectivePolicyRecordV1(value)
    }
}
impl ::std::convert::From<Envelope4PolicyTestResultRecordV1>
for Envelope4RootQueryRecord {
    fn from(value: Envelope4PolicyTestResultRecordV1) -> Self {
        Self::PolicyTestResultRecordV1(value)
    }
}
impl ::std::convert::From<Envelope4CandidateListRecordV1> for Envelope4RootQueryRecord {
    fn from(value: Envelope4CandidateListRecordV1) -> Self {
        Self::CandidateListRecordV1(value)
    }
}
impl ::std::convert::From<Envelope4CandidateInspectionRecordV1>
for Envelope4RootQueryRecord {
    fn from(value: Envelope4CandidateInspectionRecordV1) -> Self {
        Self::CandidateInspectionRecordV1(value)
    }
}
impl ::std::convert::From<Envelope4ReviewBriefRecordV1> for Envelope4RootQueryRecord {
    fn from(value: Envelope4ReviewBriefRecordV1) -> Self {
        Self::ReviewBriefRecordV1(value)
    }
}
impl ::std::convert::From<Envelope4RepairPreviewRecordV1> for Envelope4RootQueryRecord {
    fn from(value: Envelope4RepairPreviewRecordV1) -> Self {
        Self::RepairPreviewRecordV1(value)
    }
}
///Required exactly on kind=query and equal to the command inventory queryDispatch.surface. graph-query-response carries queryResponse; every other value carries queryRecord of exactly its record type.
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
pub enum Envelope4RootQuerySurface {
    #[serde(rename = "graph-query-response")]
    GraphQueryResponse,
    #[serde(rename = "discovery-recommendation")]
    DiscoveryRecommendation,
    #[serde(rename = "baseline-inspection")]
    BaselineInspection,
    #[serde(rename = "effective-policy")]
    EffectivePolicy,
    #[serde(rename = "policy-test-result")]
    PolicyTestResult,
    #[serde(rename = "candidate-list")]
    CandidateList,
    #[serde(rename = "candidate-inspection")]
    CandidateInspection,
    #[serde(rename = "review-brief")]
    ReviewBrief,
    #[serde(rename = "repair-preview")]
    RepairPreview,
}
impl ::std::fmt::Display for Envelope4RootQuerySurface {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::GraphQueryResponse => f.write_str("graph-query-response"),
            Self::DiscoveryRecommendation => f.write_str("discovery-recommendation"),
            Self::BaselineInspection => f.write_str("baseline-inspection"),
            Self::EffectivePolicy => f.write_str("effective-policy"),
            Self::PolicyTestResult => f.write_str("policy-test-result"),
            Self::CandidateList => f.write_str("candidate-list"),
            Self::CandidateInspection => f.write_str("candidate-inspection"),
            Self::ReviewBrief => f.write_str("review-brief"),
            Self::RepairPreview => f.write_str("repair-preview"),
        }
    }
}
impl ::std::str::FromStr for Envelope4RootQuerySurface {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "graph-query-response" => Ok(Self::GraphQueryResponse),
            "discovery-recommendation" => Ok(Self::DiscoveryRecommendation),
            "baseline-inspection" => Ok(Self::BaselineInspection),
            "effective-policy" => Ok(Self::EffectivePolicy),
            "policy-test-result" => Ok(Self::PolicyTestResult),
            "candidate-list" => Ok(Self::CandidateList),
            "candidate-inspection" => Ok(Self::CandidateInspection),
            "review-brief" => Ok(Self::ReviewBrief),
            "repair-preview" => Ok(Self::RepairPreview),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Envelope4RootQuerySurface {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Envelope4RootQuerySurface {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///baseline show: the admitted baseline:2 artifact and one availability row per descriptor pivotClosure entry, in descriptor order.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope7BaselineInspectionRecordV1 {
    pub baseline: Baseline2Root,
    #[serde(rename = "pivotClosureAvailability")]
    pub pivot_closure_availability: ::std::vec::Vec<Envelope7PivotClosureAvailabilityV1>,
    pub surface: ::serde_json::Value,
}
///inspect: the review:2 InspectionBundle of one candidate of an admitted Run.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope7CandidateInspectionRecordV1 {
    pub context: Graph4GraphQueryResponseContext,
    pub inspection: Review2InspectionBundle,
    pub surface: ::serde_json::Value,
}
///candidates: review:2 Candidate records of one admitted Run with the owner non-graph context.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope7CandidateListRecordV1 {
    pub candidates: ::std::vec::Vec<Review2Candidate>,
    pub context: Graph4GraphQueryResponseContext,
    #[serde(rename = "evidenceLevels")]
    pub evidence_levels: Envelope7EvidenceLevelCountsV1,
    #[serde(rename = "includeSuppressed")]
    pub include_suppressed: bool,
    #[serde(rename = "suppressedCount")]
    pub suppressed_count: Common4Uint53,
    pub surface: ::serde_json::Value,
}
///The only config2 proposal this surface emits: explicit discovery.workspaceRoots (native explicit-root spelling) pinning discovered units. Every root normalizes to a discovered unit rootPath and unitOrdinals are exactly those units. Other config2 keys have no published config2 document schema and are not proposed.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope7Config2WorkspaceRootsProposalV1 {
    pub key: ::serde_json::Value,
    #[serde(rename = "unitOrdinals")]
    pub unit_ordinals: ::std::vec::Vec<i64>,
    #[serde(rename = "workspaceRoots")]
    pub workspace_roots: ::std::vec::Vec<
        Envelope7Config2WorkspaceRootsProposalV1WorkspaceRootsItem,
    >,
}
///`Envelope7Config2WorkspaceRootsProposalV1WorkspaceRootsItem`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Envelope7Config2WorkspaceRootsProposalV1WorkspaceRootsItem(
    ::std::string::String,
);
impl ::std::ops::Deref for Envelope7Config2WorkspaceRootsProposalV1WorkspaceRootsItem {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Envelope7Config2WorkspaceRootsProposalV1WorkspaceRootsItem>
for ::std::string::String {
    fn from(value: Envelope7Config2WorkspaceRootsProposalV1WorkspaceRootsItem) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Envelope7Config2WorkspaceRootsProposalV1WorkspaceRootsItem {
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
impl ::std::convert::TryFrom<&str>
for Envelope7Config2WorkspaceRootsProposalV1WorkspaceRootsItem {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Envelope7Config2WorkspaceRootsProposalV1WorkspaceRootsItem {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de>
for Envelope7Config2WorkspaceRootsProposalV1WorkspaceRootsItem {
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
///recommend: native UnitDiscoveryV2 admitted under the security boundary inventory, registered advisory details, and config2 proposals. Advisory only.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope7DiscoveryRecommendationRecordV1 {
    pub advisory: ::serde_json::Value,
    #[serde(rename = "config2Proposals")]
    pub config2_proposals: ::std::vec::Vec<Envelope7Config2WorkspaceRootsProposalV1>,
    pub discovery: Native2UnitDiscoveryV2,
    ///Zero rows in this profile: no recommendation detail is registered. The only advisory next step is the explicit discovery.workspaceRoots config2 proposal. A recommendation vocabulary requires registered details and a successor of this record.
    pub recommendations: ::std::vec::Vec<Common4DomainDetail>,
    pub surface: ::serde_json::Value,
}
///policy show: the admitted tracked policy, the resolved effective waiver set and its resolution disclosure, with their document digests.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope7EffectivePolicyRecordV1 {
    #[serde(rename = "effectiveWaivers")]
    pub effective_waivers: Policy1WaiverSetV1,
    pub policy: Policy2PolicyDocumentV2,
    #[serde(rename = "policyDigest")]
    pub policy_digest: Common4Sha256Hex,
    pub surface: ::serde_json::Value,
    #[serde(rename = "waiverResolution")]
    pub waiver_resolution: Policy1WaiverResolutionV1,
    #[serde(rename = "waiverSetDigest")]
    pub waiver_set_digest: Common4Sha256Hex,
}
///Count of listed candidates per review:2 EvidenceLevel.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope7EvidenceLevelCountsV1 {
    #[serde(rename = "advisory-only")]
    pub advisory_only: Common4Uint53,
    #[serde(rename = "partial-coverage")]
    pub partial_coverage: Common4Uint53,
    #[serde(rename = "proof-backed")]
    pub proof_backed: Common4Uint53,
}
///fit query step result. sealed-run-first-page: the exact first candidate.list page of the Run this invocation sealed. unavailable-ephemeral-analysis: --ephemeral, no sealed Run.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(tag = "state", deny_unknown_fields)]
pub enum Envelope7FitAdvisoryReportV1 {
    #[serde(rename = "sealed-run-first-page")]
    SealedRunFirstPage {
        #[serde(rename = "candidateList")]
        candidate_list: Envelope7FitAdvisoryReportV1CandidateList,
        parity: Envelope7FitSealedParityV1,
        request: Envelope7FitAdvisoryReportV1Request,
    },
    #[serde(rename = "unavailable-ephemeral-analysis")]
    UnavailableEphemeralAnalysis { parity: Envelope7FitEphemeralParityV1 },
    #[serde(rename = "unavailable-query-result")]
    UnavailableQueryResult {
        parity: Envelope7FitAdvisoryReportV1Parity,
        #[serde(rename = "queryOutcome")]
        query_outcome: Envelope7FitAdvisoryReportV1QueryOutcome,
    },
}
///`Envelope7FitAdvisoryReportV1CandidateList`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope7FitAdvisoryReportV1CandidateList {
    pub candidates: ::std::vec::Vec<Review2Candidate>,
    pub context: Graph4GraphQueryResponseContext,
    #[serde(rename = "evidenceLevels")]
    pub evidence_levels: Envelope7EvidenceLevelCountsV1,
    #[serde(rename = "includeSuppressed")]
    pub include_suppressed: bool,
    #[serde(rename = "suppressedCount")]
    pub suppressed_count: Common4Uint53,
    pub surface: ::serde_json::Value,
}
///`Envelope7FitAdvisoryReportV1Parity`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope7FitAdvisoryReportV1Parity {
    pub candidates: (),
    #[serde(rename = "candidatesAvailability")]
    pub candidates_availability: ::serde_json::Value,
    #[serde(rename = "candidatesNextCursor")]
    pub candidates_next_cursor: (),
    #[serde(rename = "candidatesTotalItems")]
    pub candidates_total_items: (),
    #[serde(rename = "candidatesTruncated")]
    pub candidates_truncated: (),
    #[serde(rename = "evidenceLevels")]
    pub evidence_levels: (),
    #[serde(rename = "runId")]
    pub run_id: ::std::string::String,
}
///`Envelope7FitAdvisoryReportV1QueryOutcome`
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
pub enum Envelope7FitAdvisoryReportV1QueryOutcome {
    #[serde(rename = "cancelled")]
    Cancelled,
    #[serde(rename = "skipped")]
    Skipped,
    #[serde(rename = "failed")]
    Failed,
    #[serde(rename = "rejected")]
    Rejected,
}
impl ::std::fmt::Display for Envelope7FitAdvisoryReportV1QueryOutcome {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Cancelled => f.write_str("cancelled"),
            Self::Skipped => f.write_str("skipped"),
            Self::Failed => f.write_str("failed"),
            Self::Rejected => f.write_str("rejected"),
        }
    }
}
impl ::std::str::FromStr for Envelope7FitAdvisoryReportV1QueryOutcome {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "cancelled" => Ok(Self::Cancelled),
            "skipped" => Ok(Self::Skipped),
            "failed" => Ok(Self::Failed),
            "rejected" => Ok(Self::Rejected),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Envelope7FitAdvisoryReportV1QueryOutcome {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Envelope7FitAdvisoryReportV1QueryOutcome {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Envelope7FitAdvisoryReportV1Request`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope7FitAdvisoryReportV1Request {
    pub completeness: Envelope7FitAdvisoryReportV1RequestCompleteness,
    pub operation: Envelope7FitAdvisoryReportV1RequestOperation,
    pub page: Envelope7FitAdvisoryReportV1RequestPage,
    pub params: Envelope7FitAdvisoryReportV1RequestParams,
    #[serde(rename = "projectId")]
    pub project_id: Common4ProjectId,
    #[serde(rename = "schemaFamily")]
    pub schema_family: ::serde_json::Value,
    #[serde(rename = "schemaMajor")]
    pub schema_major: ExactInteger,
    pub view: Graph4ResolvedView,
}
///`Envelope7FitAdvisoryReportV1RequestCompleteness`
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
pub enum Envelope7FitAdvisoryReportV1RequestCompleteness {
    #[serde(rename = "best-effort")]
    BestEffort,
}
impl ::std::fmt::Display for Envelope7FitAdvisoryReportV1RequestCompleteness {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::BestEffort => f.write_str("best-effort"),
        }
    }
}
impl ::std::str::FromStr for Envelope7FitAdvisoryReportV1RequestCompleteness {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "best-effort" => Ok(Self::BestEffort),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Envelope7FitAdvisoryReportV1RequestCompleteness {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Envelope7FitAdvisoryReportV1RequestCompleteness {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Envelope7FitAdvisoryReportV1RequestOperation`
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
pub enum Envelope7FitAdvisoryReportV1RequestOperation {
    #[serde(rename = "candidate.list")]
    CandidateList,
}
impl ::std::fmt::Display for Envelope7FitAdvisoryReportV1RequestOperation {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::CandidateList => f.write_str("candidate.list"),
        }
    }
}
impl ::std::str::FromStr for Envelope7FitAdvisoryReportV1RequestOperation {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "candidate.list" => Ok(Self::CandidateList),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Envelope7FitAdvisoryReportV1RequestOperation {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Envelope7FitAdvisoryReportV1RequestOperation {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Envelope7FitAdvisoryReportV1RequestPage`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope7FitAdvisoryReportV1RequestPage {
    pub size: Envelope7FitAdvisoryReportV1RequestPageSize,
}
///`Envelope7FitAdvisoryReportV1RequestPageSize`
#[derive(::serde::Serialize, Clone, Debug)]
#[serde(transparent)]
pub struct Envelope7FitAdvisoryReportV1RequestPageSize(::std::num::NonZeroU64);
impl ::std::ops::Deref for Envelope7FitAdvisoryReportV1RequestPageSize {
    type Target = ::std::num::NonZeroU64;
    fn deref(&self) -> &::std::num::NonZeroU64 {
        &self.0
    }
}
impl ::std::convert::From<Envelope7FitAdvisoryReportV1RequestPageSize>
for ::std::num::NonZeroU64 {
    fn from(value: Envelope7FitAdvisoryReportV1RequestPageSize) -> Self {
        value.0
    }
}
impl ::std::convert::TryFrom<::std::num::NonZeroU64>
for Envelope7FitAdvisoryReportV1RequestPageSize {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::num::NonZeroU64,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if ![::std::num::NonZeroU64::new(100).unwrap()].contains(&value) {
            Err("invalid value".into())
        } else {
            Ok(Self(value))
        }
    }
}
impl<'de> ::serde::Deserialize<'de> for Envelope7FitAdvisoryReportV1RequestPageSize {
    fn deserialize<D>(deserializer: D) -> ::std::result::Result<Self, D::Error>
    where
        D: ::serde::Deserializer<'de>,
    {
        Self::try_from(<::std::num::NonZeroU64>::deserialize(deserializer)?)
            .map_err(|e| { <D::Error as ::serde::de::Error>::custom(e.to_string()) })
    }
}
///`Envelope7FitAdvisoryReportV1RequestParams`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope7FitAdvisoryReportV1RequestParams {
    #[serde(rename = "includeSuppressed")]
    pub include_suppressed: bool,
}
///Non-authoritative law (workflows section 8): run-id is explicitly null and no authoritative candidate parity exists; nothing is fabricated.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope7FitEphemeralParityV1 {
    pub candidates: (),
    #[serde(rename = "candidatesAvailability")]
    pub candidates_availability: ::serde_json::Value,
    #[serde(rename = "candidatesNextCursor")]
    pub candidates_next_cursor: (),
    #[serde(rename = "candidatesTotalItems")]
    pub candidates_total_items: (),
    #[serde(rename = "candidatesTruncated")]
    pub candidates_truncated: (),
    #[serde(rename = "evidenceLevels")]
    pub evidence_levels: (),
    #[serde(rename = "runId")]
    pub run_id: (),
}
///Total fit parity of the first canonical page. Not the complete candidate set: candidatesTruncated, candidatesTotalItems and candidatesNextCursor disclose the remainder.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope7FitSealedParityV1 {
    pub candidates: ::std::vec::Vec<Review2Candidate>,
    #[serde(rename = "candidatesAvailability")]
    pub candidates_availability: ::serde_json::Value,
    #[serde(
        rename = "candidatesNextCursor",
        deserialize_with = "::std::option::Option::deserialize"
    )]
    pub candidates_next_cursor: ::std::option::Option<
        Envelope7FitSealedParityV1CandidatesNextCursor,
    >,
    #[serde(rename = "candidatesTotalItems")]
    pub candidates_total_items: Common4Uint53,
    #[serde(rename = "candidatesTruncated")]
    pub candidates_truncated: bool,
    #[serde(rename = "evidenceLevels")]
    pub evidence_levels: Envelope7EvidenceLevelCountsV1,
    #[serde(rename = "runId")]
    pub run_id: Common4RunId,
}
///`Envelope7FitSealedParityV1CandidatesNextCursor`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Envelope7FitSealedParityV1CandidatesNextCursor(::std::string::String);
impl ::std::ops::Deref for Envelope7FitSealedParityV1CandidatesNextCursor {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Envelope7FitSealedParityV1CandidatesNextCursor>
for ::std::string::String {
    fn from(value: Envelope7FitSealedParityV1CandidatesNextCursor) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Envelope7FitSealedParityV1CandidatesNextCursor {
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
impl ::std::convert::TryFrom<&str> for Envelope7FitSealedParityV1CandidatesNextCursor {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Envelope7FitSealedParityV1CandidatesNextCursor {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Envelope7FitSealedParityV1CandidatesNextCursor {
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
///`Envelope7MutationReceiptProjection`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope7MutationReceiptProjection {
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub after: FieldPresence<::std::option::Option<Common4Sha256Hex>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub before: FieldPresence<::std::option::Option<Common4Sha256Hex>>,
    #[serde(rename = "commitClass")]
    pub commit_class: Envelope7MutationReceiptProjectionCommitClass,
    #[serde(rename = "effectOutcome")]
    pub effect_outcome: Envelope7MutationReceiptProjectionEffectOutcome,
    pub operation: Repair2MutationOperation,
    #[serde(rename = "receiptId")]
    pub receipt_id: Common4ReceiptId,
    pub replayed: bool,
    #[serde(
        rename = "verificationRunId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub verification_run_id: FieldPresence<::std::option::Option<Common4RunId>>,
}
///`Envelope7MutationReceiptProjectionCommitClass`
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
pub enum Envelope7MutationReceiptProjectionCommitClass {
    #[serde(rename = "REVERSIBLE")]
    Reversible,
    #[serde(rename = "IRREVERSIBLE")]
    Irreversible,
}
impl ::std::fmt::Display for Envelope7MutationReceiptProjectionCommitClass {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Reversible => f.write_str("REVERSIBLE"),
            Self::Irreversible => f.write_str("IRREVERSIBLE"),
        }
    }
}
impl ::std::str::FromStr for Envelope7MutationReceiptProjectionCommitClass {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "REVERSIBLE" => Ok(Self::Reversible),
            "IRREVERSIBLE" => Ok(Self::Irreversible),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Envelope7MutationReceiptProjectionCommitClass {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Envelope7MutationReceiptProjectionCommitClass {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Envelope7MutationReceiptProjectionEffectOutcome`
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
pub enum Envelope7MutationReceiptProjectionEffectOutcome {
    #[serde(rename = "COMPLETED")]
    Completed,
    #[serde(rename = "FAILED")]
    Failed,
    #[serde(rename = "INDETERMINATE")]
    Indeterminate,
}
impl ::std::fmt::Display for Envelope7MutationReceiptProjectionEffectOutcome {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Completed => f.write_str("COMPLETED"),
            Self::Failed => f.write_str("FAILED"),
            Self::Indeterminate => f.write_str("INDETERMINATE"),
        }
    }
}
impl ::std::str::FromStr for Envelope7MutationReceiptProjectionEffectOutcome {
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
impl ::std::convert::TryFrom<&str> for Envelope7MutationReceiptProjectionEffectOutcome {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Envelope7MutationReceiptProjectionEffectOutcome {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Current-trust resolution of one pivot closure: missing (BASELINE.PIVOT_DETECTOR_UNAVAILABLE), revoked (BASELINE.PIVOT_CLOSURE_REVOKED), incompatible protocol major or platform (BASELINE.PIVOT_CLOSURE_INCOMPATIBLE), or available with its trust origin.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope7PivotClosureAvailabilityV1 {
    #[serde(rename = "closureId")]
    pub closure_id: Common4ClosureId,
    pub kind: Baseline2PivotClosureEntryPropertiesKind,
    pub state: Envelope7PivotClosureAvailabilityV1State,
    #[serde(
        rename = "trustOrigin",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub trust_origin: FieldPresence<
        ::std::option::Option<Envelope7PivotClosureAvailabilityV1TrustOrigin>,
    >,
}
///`Envelope7PivotClosureAvailabilityV1State`
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
pub enum Envelope7PivotClosureAvailabilityV1State {
    #[serde(rename = "available")]
    Available,
    #[serde(rename = "missing")]
    Missing,
    #[serde(rename = "revoked")]
    Revoked,
    #[serde(rename = "incompatible")]
    Incompatible,
}
impl ::std::fmt::Display for Envelope7PivotClosureAvailabilityV1State {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Available => f.write_str("available"),
            Self::Missing => f.write_str("missing"),
            Self::Revoked => f.write_str("revoked"),
            Self::Incompatible => f.write_str("incompatible"),
        }
    }
}
impl ::std::str::FromStr for Envelope7PivotClosureAvailabilityV1State {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "available" => Ok(Self::Available),
            "missing" => Ok(Self::Missing),
            "revoked" => Ok(Self::Revoked),
            "incompatible" => Ok(Self::Incompatible),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Envelope7PivotClosureAvailabilityV1State {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Envelope7PivotClosureAvailabilityV1State {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Envelope7PivotClosureAvailabilityV1TrustOrigin`
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
pub enum Envelope7PivotClosureAvailabilityV1TrustOrigin {
    #[serde(rename = "retained-generation")]
    RetainedGeneration,
    #[serde(rename = "installed-signed-release")]
    InstalledSignedRelease,
    #[serde(rename = "signed-closure-bundle")]
    SignedClosureBundle,
}
impl ::std::fmt::Display for Envelope7PivotClosureAvailabilityV1TrustOrigin {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::RetainedGeneration => f.write_str("retained-generation"),
            Self::InstalledSignedRelease => f.write_str("installed-signed-release"),
            Self::SignedClosureBundle => f.write_str("signed-closure-bundle"),
        }
    }
}
impl ::std::str::FromStr for Envelope7PivotClosureAvailabilityV1TrustOrigin {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "retained-generation" => Ok(Self::RetainedGeneration),
            "installed-signed-release" => Ok(Self::InstalledSignedRelease),
            "signed-closure-bundle" => Ok(Self::SignedClosureBundle),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Envelope7PivotClosureAvailabilityV1TrustOrigin {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Envelope7PivotClosureAvailabilityV1TrustOrigin {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///policy test: the complete PolicyTestResultV1 of a resolver-accepted evaluator3 PolicyTestSuiteV2 (urn:opensip:product-v1:workflows:evaluator3:policy-test:2). A suite or candidate policy of another major terminates request-rejected REQUEST.SCHEMA_MAJOR_UNSUPPORTED with EVALUATION.MIXED_OUTPUT_MAJOR (golden policy-test-suite-major-unsupported); any other suite admission or resolver refusal terminates request-rejected CONFIG.INVALID with its detail (workflows-and-surfaces section 5; goldens policy-test-duplicate-waiver, policy-test-imperative-key, policy-test-suite-inadmissible). No refusal is carried here.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope7PolicyTestResultRecordV1 {
    pub result: Envelope7PolicyTestResultRecordV1Result,
    pub surface: ::serde_json::Value,
}
///`Envelope7PolicyTestResultRecordV1Result`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope7PolicyTestResultRecordV1Result {
    #[serde(rename = "candidatePolicyDigest")]
    pub candidate_policy_digest: Common1Sha256Hex,
    ///digest of the candidate after overrides; equals candidatePolicyDigest when no override applied
    #[serde(rename = "effectivePolicyDigest")]
    pub effective_policy_digest: Common1Sha256Hex,
    #[serde(rename = "enforcementUnchanged")]
    pub enforcement_unchanged: ::serde_json::Value,
    #[serde(rename = "overridesApplied")]
    pub overrides_applied: ::std::vec::Vec<PolicyTest1Override>,
    #[serde(rename = "policyTestResultId")]
    pub policy_test_result_id: Common1PolicyTestResultId,
    #[serde(rename = "resolverAccepted")]
    pub resolver_accepted: bool,
    #[serde(rename = "resolverRefusals")]
    pub resolver_refusals: ::std::vec::Vec<Common1DomainDetail>,
    pub results: ::std::vec::Vec<PolicyTest1CaseResult>,
    #[serde(rename = "schemaFamily")]
    pub schema_family: ::serde_json::Value,
    #[serde(rename = "schemaMajor")]
    pub schema_major: ExactInteger,
    ///Bare H("workflow.policy-test-suite", the complete admitted PolicyTestSuiteV1 before overrides), under identity section 3. Retain the suite preimage; not raw SHA-256 of canonical suite bytes.
    #[serde(rename = "suiteDigest")]
    pub suite_digest: Common1Sha256Hex,
    pub summary: Envelope7PolicyTestResultRecordV1ResultSummary,
    #[serde(rename = "waiverResolution")]
    pub waiver_resolution: Policy1WaiverResolutionV1,
}
///`Envelope7PolicyTestResultRecordV1ResultSummary`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope7PolicyTestResultRecordV1ResultSummary {
    pub failed: Common1Uint53,
    pub indeterminate: Common1Uint53,
    #[serde(rename = "notExecutable")]
    pub not_executable: Common1Uint53,
    pub passed: Common1Uint53,
}
///Required exactly on kind=query and equal to the command inventory queryDispatch.surface. graph-query-response carries queryResponse; every other value carries queryRecord of exactly its record type.
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
pub enum Envelope7PropertiesQuerySurface {
    #[serde(rename = "graph-query-response")]
    GraphQueryResponse,
    #[serde(rename = "discovery-recommendation")]
    DiscoveryRecommendation,
    #[serde(rename = "baseline-inspection")]
    BaselineInspection,
    #[serde(rename = "effective-policy")]
    EffectivePolicy,
    #[serde(rename = "policy-test-result")]
    PolicyTestResult,
    #[serde(rename = "candidate-list")]
    CandidateList,
    #[serde(rename = "candidate-inspection")]
    CandidateInspection,
    #[serde(rename = "review-brief")]
    ReviewBrief,
    #[serde(rename = "repair-preview")]
    RepairPreview,
}
impl ::std::fmt::Display for Envelope7PropertiesQuerySurface {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::GraphQueryResponse => f.write_str("graph-query-response"),
            Self::DiscoveryRecommendation => f.write_str("discovery-recommendation"),
            Self::BaselineInspection => f.write_str("baseline-inspection"),
            Self::EffectivePolicy => f.write_str("effective-policy"),
            Self::PolicyTestResult => f.write_str("policy-test-result"),
            Self::CandidateList => f.write_str("candidate-list"),
            Self::CandidateInspection => f.write_str("candidate-inspection"),
            Self::ReviewBrief => f.write_str("review-brief"),
            Self::RepairPreview => f.write_str("repair-preview"),
        }
    }
}
impl ::std::str::FromStr for Envelope7PropertiesQuerySurface {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "graph-query-response" => Ok(Self::GraphQueryResponse),
            "discovery-recommendation" => Ok(Self::DiscoveryRecommendation),
            "baseline-inspection" => Ok(Self::BaselineInspection),
            "effective-policy" => Ok(Self::EffectivePolicy),
            "policy-test-result" => Ok(Self::PolicyTestResult),
            "candidate-list" => Ok(Self::CandidateList),
            "candidate-inspection" => Ok(Self::CandidateInspection),
            "review-brief" => Ok(Self::ReviewBrief),
            "repair-preview" => Ok(Self::RepairPreview),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Envelope7PropertiesQuerySurface {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Envelope7PropertiesQuerySurface {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///repair preview: the invocation:3 RepairPreviewResult and the repair:2 RepairPlanV1 it names.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope7RepairPreviewRecordV1 {
    pub plan: Repair2RepairPlanV1,
    pub preview: Invocation5RepairPreviewResult,
    pub surface: ::serde_json::Value,
}
///review brief: the review:2 ReviewBrief of one admitted Run.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope7ReviewBriefRecordV1 {
    pub brief: Review2ReviewBrief,
    pub context: Graph4GraphQueryResponseContext,
    pub surface: ::serde_json::Value,
}
///Evaluator3 envelope. schemaMajor 3 because AnalysisResult.runId is run3 and the intermediate findings projection is FindingSurface (finding3, nullable fingerprint; not a SARIF result). SARIF 2.1.0 output is urn:opensip:product-v1:workflows:evaluator3:sarif-adapter:2. Consumers pin this major; major 2 envelopes are REQUEST.SCHEMA_MAJOR_UNSUPPORTED, never reshaped. Output serialization overflow uses OUTPUT.SERIALIZATION_FAILED / faultCause output-serialization. Query carrier: kind=query requires querySurface. The query command (the twenty graph-query:3 operations) selects graph-query-response and carries the complete owner-admitted GraphQueryResponseV1 in queryResponse, which is its query-response parity field; every other query-class command selects its own surface and carries queryRecord of that closed record type. Unsupported envelope majors terminate REQUEST.SCHEMA_MAJOR_UNSUPPORTED with detail OUTPUT.ENVELOPE_MAJOR_UNSUPPORTED. Successor major4 adds only the metadata success branch. All pre-existing evaluator3 payload constraints and semantic owners remain. Metadata failures use the existing failure branch. Metadata semantic admission also checks catalogue and compiled build selection. Successor major5 adds only advisoryReport, the fit advisory carrier on kind=run: either the first canonical candidate.list page of the sealed authoritative Run (exact request, CandidateListRecordV1, total parity) or the non-authoritative ephemeral form with run-id and candidate parity explicitly null. Presence is command-specific host admission through command-inventory:5 advisoryDispatch. Every major4 constraint, identity and semantic owner remains. A major4 reader rejects 5 and a major5 reader rejects 4. Successor major6 allows kind=failure/errors=[] for the existing interrupted termination before any committed Run, with an owned signal and exit130. It creates no error code or DomainDetail. The existing empty-errors REQUEST.UNKNOWN_OPTION diagnostic branch remains unchanged. A major5 reader rejects6; explicit major selection is required. Joint unaccepted successor7 adds explicit unavailable-query-result parity for an interrupted authoritative fit carrier. Completed query responses are preserved by private host completion custody.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Envelope7Root {
    ///Required exactly on the fit command's kind=run envelope (inventory5 advisoryDispatch). Never alters run, findings, verdict or termination.
    #[serde(
        rename = "advisoryReport",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub advisory_report: FieldPresence<
        ::std::option::Option<Envelope7FitAdvisoryReportV1>,
    >,
    ///present only in the agent rendering; advisory text that never changes any parity field
    #[serde(
        rename = "agentHints",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub agent_hints: FieldPresence<::std::vec::Vec<Common4BoundedText>>,
    ///Optional. The bounded capability-availability collection of THIS invocation: every capability the selected product required that this release did not declare available, with its full ownership tuple. Present on the invocation that selected them - it is not deferred to a separate doctor report, which is a different invocation and cannot deliver these absences. Advisory only.
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub availability: FieldPresence<
        ::std::option::Option<Common4CapabilityAvailabilityV1>,
    >,
    #[serde(
        rename = "clientCorrelationId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub client_correlation_id: FieldPresence<
        ::std::option::Option<Envelope7RootClientCorrelationId>,
    >,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub diagnostics: FieldPresence<::std::vec::Vec<Common4BoundedText>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub doctor: FieldPresence<::std::option::Option<Invocation5DoctorResult>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub errors: FieldPresence<::std::vec::Vec<Common4DomainDetail>>,
    #[serde(rename = "exitCode")]
    pub exit_code: ExactInteger,
    ///Optional direct findings projection for analysis envelopes. One row per finding3. Not keyed by fingerprint.
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub findings: FieldPresence<
        ::std::option::Option<::std::vec::Vec<Common4FindingSurface>>,
    >,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub invocation: FieldPresence<::std::option::Option<Invocation5Root>>,
    pub kind: Envelope7RootKind,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub meta: FieldPresence<::std::option::Option<Metadata1Root>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub mutation: FieldPresence<
        ::std::option::Option<Envelope7MutationReceiptProjection>,
    >,
    #[serde(
        rename = "projectId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub project_id: FieldPresence<::std::option::Option<Common4ProjectId>>,
    #[serde(
        rename = "projectRoot",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub project_root: FieldPresence<::std::option::Option<Common4UserInputPath>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub query: FieldPresence<::std::option::Option<Invocation5QueryResult>>,
    ///Closed typed result of a non-graph query-class command, discriminated by surface; no untyped payload is admitted.
    #[serde(
        rename = "queryRecord",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub query_record: FieldPresence<::std::option::Option<Envelope7RootQueryRecord>>,
    ///The complete owner-admitted query response, required exactly when querySurface=graph-query-response. Cross-record joins beyond JSON Schema: context.projectId equals projectId; a present response termination equals termination; for graph.* the query summary is the owner projection of this response.
    #[serde(
        rename = "queryResponse",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub query_response: FieldPresence<::std::option::Option<Graph4GraphQueryResponseV1>>,
    ///Required exactly on kind=query and equal to the command inventory queryDispatch.surface. graph-query-response carries queryResponse; every other value carries queryRecord of exactly its record type.
    #[serde(
        rename = "querySurface",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub query_surface: FieldPresence<::std::option::Option<Envelope7RootQuerySurface>>,
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
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub run: FieldPresence<::std::option::Option<Invocation5AnalysisResult>>,
    #[serde(rename = "schemaFamily")]
    pub schema_family: ::serde_json::Value,
    #[serde(rename = "schemaMajor")]
    pub schema_major: ExactInteger,
    pub termination: Common4StepTermination,
}
///`Envelope7RootClientCorrelationId`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Envelope7RootClientCorrelationId(::std::string::String);
impl ::std::ops::Deref for Envelope7RootClientCorrelationId {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Envelope7RootClientCorrelationId> for ::std::string::String {
    fn from(value: Envelope7RootClientCorrelationId) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Envelope7RootClientCorrelationId {
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
impl ::std::convert::TryFrom<&str> for Envelope7RootClientCorrelationId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Envelope7RootClientCorrelationId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Envelope7RootClientCorrelationId {
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
///`Envelope7RootKind`
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
pub enum Envelope7RootKind {
    #[serde(rename = "run")]
    Run,
    #[serde(rename = "query")]
    Query,
    #[serde(rename = "mutation")]
    Mutation,
    #[serde(rename = "failure")]
    Failure,
    #[serde(rename = "invocation")]
    Invocation,
    #[serde(rename = "doctor")]
    Doctor,
    #[serde(rename = "meta")]
    Meta,
}
impl ::std::fmt::Display for Envelope7RootKind {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Run => f.write_str("run"),
            Self::Query => f.write_str("query"),
            Self::Mutation => f.write_str("mutation"),
            Self::Failure => f.write_str("failure"),
            Self::Invocation => f.write_str("invocation"),
            Self::Doctor => f.write_str("doctor"),
            Self::Meta => f.write_str("meta"),
        }
    }
}
impl ::std::str::FromStr for Envelope7RootKind {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "run" => Ok(Self::Run),
            "query" => Ok(Self::Query),
            "mutation" => Ok(Self::Mutation),
            "failure" => Ok(Self::Failure),
            "invocation" => Ok(Self::Invocation),
            "doctor" => Ok(Self::Doctor),
            "meta" => Ok(Self::Meta),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Envelope7RootKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Envelope7RootKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Closed typed result of a non-graph query-class command, discriminated by surface; no untyped payload is admitted.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(untagged)]
pub enum Envelope7RootQueryRecord {
    DiscoveryRecommendationRecordV1(Envelope7DiscoveryRecommendationRecordV1),
    BaselineInspectionRecordV1(Envelope7BaselineInspectionRecordV1),
    EffectivePolicyRecordV1(Envelope7EffectivePolicyRecordV1),
    PolicyTestResultRecordV1(Envelope7PolicyTestResultRecordV1),
    CandidateListRecordV1(Envelope7CandidateListRecordV1),
    CandidateInspectionRecordV1(Envelope7CandidateInspectionRecordV1),
    ReviewBriefRecordV1(Envelope7ReviewBriefRecordV1),
    RepairPreviewRecordV1(Envelope7RepairPreviewRecordV1),
}
impl ::std::convert::From<Envelope7DiscoveryRecommendationRecordV1>
for Envelope7RootQueryRecord {
    fn from(value: Envelope7DiscoveryRecommendationRecordV1) -> Self {
        Self::DiscoveryRecommendationRecordV1(value)
    }
}
impl ::std::convert::From<Envelope7BaselineInspectionRecordV1>
for Envelope7RootQueryRecord {
    fn from(value: Envelope7BaselineInspectionRecordV1) -> Self {
        Self::BaselineInspectionRecordV1(value)
    }
}
impl ::std::convert::From<Envelope7EffectivePolicyRecordV1>
for Envelope7RootQueryRecord {
    fn from(value: Envelope7EffectivePolicyRecordV1) -> Self {
        Self::EffectivePolicyRecordV1(value)
    }
}
impl ::std::convert::From<Envelope7PolicyTestResultRecordV1>
for Envelope7RootQueryRecord {
    fn from(value: Envelope7PolicyTestResultRecordV1) -> Self {
        Self::PolicyTestResultRecordV1(value)
    }
}
impl ::std::convert::From<Envelope7CandidateListRecordV1> for Envelope7RootQueryRecord {
    fn from(value: Envelope7CandidateListRecordV1) -> Self {
        Self::CandidateListRecordV1(value)
    }
}
impl ::std::convert::From<Envelope7CandidateInspectionRecordV1>
for Envelope7RootQueryRecord {
    fn from(value: Envelope7CandidateInspectionRecordV1) -> Self {
        Self::CandidateInspectionRecordV1(value)
    }
}
impl ::std::convert::From<Envelope7ReviewBriefRecordV1> for Envelope7RootQueryRecord {
    fn from(value: Envelope7ReviewBriefRecordV1) -> Self {
        Self::ReviewBriefRecordV1(value)
    }
}
impl ::std::convert::From<Envelope7RepairPreviewRecordV1> for Envelope7RootQueryRecord {
    fn from(value: Envelope7RepairPreviewRecordV1) -> Self {
        Self::RepairPreviewRecordV1(value)
    }
}
///Required exactly on kind=query and equal to the command inventory queryDispatch.surface. graph-query-response carries queryResponse; every other value carries queryRecord of exactly its record type.
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
pub enum Envelope7RootQuerySurface {
    #[serde(rename = "graph-query-response")]
    GraphQueryResponse,
    #[serde(rename = "discovery-recommendation")]
    DiscoveryRecommendation,
    #[serde(rename = "baseline-inspection")]
    BaselineInspection,
    #[serde(rename = "effective-policy")]
    EffectivePolicy,
    #[serde(rename = "policy-test-result")]
    PolicyTestResult,
    #[serde(rename = "candidate-list")]
    CandidateList,
    #[serde(rename = "candidate-inspection")]
    CandidateInspection,
    #[serde(rename = "review-brief")]
    ReviewBrief,
    #[serde(rename = "repair-preview")]
    RepairPreview,
}
impl ::std::fmt::Display for Envelope7RootQuerySurface {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::GraphQueryResponse => f.write_str("graph-query-response"),
            Self::DiscoveryRecommendation => f.write_str("discovery-recommendation"),
            Self::BaselineInspection => f.write_str("baseline-inspection"),
            Self::EffectivePolicy => f.write_str("effective-policy"),
            Self::PolicyTestResult => f.write_str("policy-test-result"),
            Self::CandidateList => f.write_str("candidate-list"),
            Self::CandidateInspection => f.write_str("candidate-inspection"),
            Self::ReviewBrief => f.write_str("review-brief"),
            Self::RepairPreview => f.write_str("repair-preview"),
        }
    }
}
impl ::std::str::FromStr for Envelope7RootQuerySurface {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "graph-query-response" => Ok(Self::GraphQueryResponse),
            "discovery-recommendation" => Ok(Self::DiscoveryRecommendation),
            "baseline-inspection" => Ok(Self::BaselineInspection),
            "effective-policy" => Ok(Self::EffectivePolicy),
            "policy-test-result" => Ok(Self::PolicyTestResult),
            "candidate-list" => Ok(Self::CandidateList),
            "candidate-inspection" => Ok(Self::CandidateInspection),
            "review-brief" => Ok(Self::ReviewBrief),
            "repair-preview" => Ok(Self::RepairPreview),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Envelope7RootQuerySurface {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Envelope7RootQuerySurface {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`ExplicitHistory1Request`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct ExplicitHistory1Request {
    pub mode: ::serde_json::Value,
    #[serde(rename = "runIds")]
    pub run_ids: ::std::vec::Vec<::std::string::String>,
}
///`ExplicitHistory1Root`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct ExplicitHistory1Root {
    #[serde(
        rename = "currentRunId",
        deserialize_with = "::std::option::Option::deserialize"
    )]
    pub current_run_id: ::std::option::Option<::std::string::String>,
    pub policy: ::serde_json::Value,
    #[serde(rename = "requestedRunIds")]
    pub requested_run_ids: ::std::vec::Vec<::std::string::String>,
    pub slots: ::std::vec::Vec<ExplicitHistory1RootSlotsItem>,
}
///`ExplicitHistory1RootSlotsItem`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct ExplicitHistory1RootSlotsItem {
    #[serde(rename = "runId")]
    pub run_id: ::std::string::String,
    pub source: ExplicitHistory1RootSlotsItemSource,
}
///`ExplicitHistory1RootSlotsItemSource`
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
pub enum ExplicitHistory1RootSlotsItemSource {
    #[serde(rename = "current-run")]
    CurrentRun,
    #[serde(rename = "exact-retained-lookup")]
    ExactRetainedLookup,
}
impl ::std::fmt::Display for ExplicitHistory1RootSlotsItemSource {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::CurrentRun => f.write_str("current-run"),
            Self::ExactRetainedLookup => f.write_str("exact-retained-lookup"),
        }
    }
}
impl ::std::str::FromStr for ExplicitHistory1RootSlotsItemSource {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "current-run" => Ok(Self::CurrentRun),
            "exact-retained-lookup" => Ok(Self::ExactRetainedLookup),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for ExplicitHistory1RootSlotsItemSource {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for ExplicitHistory1RootSlotsItemSource {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`ExplicitHistoryPanel1RetainedHistorySlotV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(transparent)]
pub struct ExplicitHistoryPanel1RetainedHistorySlotV1(pub Report1HistoryRunV1);
impl ::std::ops::Deref for ExplicitHistoryPanel1RetainedHistorySlotV1 {
    type Target = Report1HistoryRunV1;
    fn deref(&self) -> &Report1HistoryRunV1 {
        &self.0
    }
}
impl ::std::convert::From<ExplicitHistoryPanel1RetainedHistorySlotV1>
for Report1HistoryRunV1 {
    fn from(value: ExplicitHistoryPanel1RetainedHistorySlotV1) -> Self {
        value.0
    }
}
impl ::std::convert::From<Report1HistoryRunV1>
for ExplicitHistoryPanel1RetainedHistorySlotV1 {
    fn from(value: Report1HistoryRunV1) -> Self {
        Self(value)
    }
}
///`ExplicitHistoryPanel1Root`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct ExplicitHistoryPanel1Root {
    pub provenance: ExplicitHistoryPanel1RootProvenance,
    pub runs: ::std::vec::Vec<ExplicitHistoryPanel1RootRunsItem>,
    pub selection: ExplicitHistory1Root,
}
///`ExplicitHistoryPanel1RootProvenance`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct ExplicitHistoryPanel1RootProvenance {
    #[serde(rename = "hostAsserted")]
    pub host_asserted: ::serde_json::Value,
    #[serde(rename = "verifiedInDocument")]
    pub verified_in_document: ::serde_json::Value,
}
///`ExplicitHistoryPanel1RootRunsItem`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(untagged, deny_unknown_fields)]
pub enum ExplicitHistoryPanel1RootRunsItem {
    Object {
        #[serde(rename = "runId")]
        run_id: Common4RunId,
        state: ::serde_json::Value,
    },
    ExplicitHistoryPanel1RetainedHistorySlotV1(
        ExplicitHistoryPanel1RetainedHistorySlotV1,
    ),
}
impl ::std::convert::From<ExplicitHistoryPanel1RetainedHistorySlotV1>
for ExplicitHistoryPanel1RootRunsItem {
    fn from(value: ExplicitHistoryPanel1RetainedHistorySlotV1) -> Self {
        Self::ExplicitHistoryPanel1RetainedHistorySlotV1(value)
    }
}
///`Graph3AdvisoryOperation`
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
pub enum Graph3AdvisoryOperation {
    #[serde(rename = "comparison.diff")]
    ComparisonDiff,
    #[serde(rename = "candidate.list")]
    CandidateList,
    #[serde(rename = "inspection.show")]
    InspectionShow,
    #[serde(rename = "review.brief")]
    ReviewBrief,
}
impl ::std::fmt::Display for Graph3AdvisoryOperation {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::ComparisonDiff => f.write_str("comparison.diff"),
            Self::CandidateList => f.write_str("candidate.list"),
            Self::InspectionShow => f.write_str("inspection.show"),
            Self::ReviewBrief => f.write_str("review.brief"),
        }
    }
}
impl ::std::str::FromStr for Graph3AdvisoryOperation {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "comparison.diff" => Ok(Self::ComparisonDiff),
            "candidate.list" => Ok(Self::CandidateList),
            "inspection.show" => Ok(Self::InspectionShow),
            "review.brief" => Ok(Self::ReviewBrief),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Graph3AdvisoryOperation {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Graph3AdvisoryOperation {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Graph3Bounds`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Graph3Bounds {
    #[serde(rename = "defaultPageSize")]
    pub default_page_size: ExactInteger,
    #[serde(rename = "maxItemsPerOperation")]
    pub max_items_per_operation: ExactInteger,
    #[serde(rename = "maxPageSize")]
    pub max_page_size: ExactInteger,
    #[serde(rename = "maxTraversalDepth")]
    pub max_traversal_depth: ExactInteger,
    #[serde(rename = "maxVisitedNodes")]
    pub max_visited_nodes: ExactInteger,
}
///Qualifies totalItems. exact: totalItems is the cardinality of the declared selection within semantic maxDepth. lower-bound: totalItems is a produced prefix, not a claimed universe cardinality. An empty nextCursor does not by itself make the count exact.
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
pub enum Graph3CountBasis {
    #[serde(rename = "exact")]
    Exact,
    #[serde(rename = "lower-bound")]
    LowerBound,
}
impl ::std::fmt::Display for Graph3CountBasis {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Exact => f.write_str("exact"),
            Self::LowerBound => f.write_str("lower-bound"),
        }
    }
}
impl ::std::str::FromStr for Graph3CountBasis {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "exact" => Ok(Self::Exact),
            "lower-bound" => Ok(Self::LowerBound),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Graph3CountBasis {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Graph3CountBasis {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Graph3FactId`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
#[serde(transparent)]
pub struct Graph3FactId(pub ::std::string::String);
impl ::std::ops::Deref for Graph3FactId {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Graph3FactId> for ::std::string::String {
    fn from(value: Graph3FactId) -> Self {
        value.0
    }
}
impl ::std::convert::From<::std::string::String> for Graph3FactId {
    fn from(value: ::std::string::String) -> Self {
        Self(value)
    }
}
impl ::std::fmt::Display for Graph3FactId {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        self.0.fmt(f)
    }
}
impl ::std::str::FromStr for Graph3FactId {
    type Err = ::std::convert::Infallible;
    fn from_str(value: &str) -> ::std::result::Result<Self, Self::Err> {
        Ok(Self(value.to_string()))
    }
}
///Explicit admitted view2 set. Omitted means all admitted views of the resolved Run whose scopes match relation@minResolution. Silent newest-provider is forbidden.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(transparent)]
pub struct Graph3FactViewDigests(pub ::std::vec::Vec<Graph3ViewDigest>);
impl ::std::ops::Deref for Graph3FactViewDigests {
    type Target = ::std::vec::Vec<Graph3ViewDigest>;
    fn deref(&self) -> &::std::vec::Vec<Graph3ViewDigest> {
        &self.0
    }
}
impl ::std::convert::From<Graph3FactViewDigests> for ::std::vec::Vec<Graph3ViewDigest> {
    fn from(value: Graph3FactViewDigests) -> Self {
        value.0
    }
}
impl ::std::convert::From<::std::vec::Vec<Graph3ViewDigest>> for Graph3FactViewDigests {
    fn from(value: ::std::vec::Vec<Graph3ViewDigest>) -> Self {
        Self(value)
    }
}
///`Graph3GraphDirection`
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
pub enum Graph3GraphDirection {
    #[serde(rename = "outgoing")]
    Outgoing,
    #[serde(rename = "incoming")]
    Incoming,
    #[serde(rename = "both")]
    Both,
}
impl ::std::fmt::Display for Graph3GraphDirection {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Outgoing => f.write_str("outgoing"),
            Self::Incoming => f.write_str("incoming"),
            Self::Both => f.write_str("both"),
        }
    }
}
impl ::std::str::FromStr for Graph3GraphDirection {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "outgoing" => Ok(Self::Outgoing),
            "incoming" => Ok(Self::Incoming),
            "both" => Ok(Self::Both),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Graph3GraphDirection {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Graph3GraphDirection {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Graph3GraphEndpoint`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Graph3GraphEndpoint {
    pub kind: Graph3StoredKind,
    #[serde(rename = "nativeSubjectId")]
    pub native_subject_id: Graph3NativeSubjectId,
    #[serde(
        rename = "packageManifestPath",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub package_manifest_path: FieldPresence<::std::option::Option<Common3LogicalPath>>,
    ///H-identity of the native semantic universe (fact sourceUniverse/targetUniverse). Required so two program universes with the same path cannot silently union.
    pub universe: Common3Sha256Hex,
}
///Mandatory Q3 disclosure for graph.*. Cites existing native Coverage, scopes, evaluation deficiencies and resolution limitations. Does not mint negative proof or run a parallel absence evaluator.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Graph3GraphEvidenceDisclosure {
    #[serde(rename = "coverageIds")]
    pub coverage_ids: ::std::vec::Vec<Common3CoverageId>,
    #[serde(rename = "deficiencyCitations")]
    pub deficiency_citations: ::std::vec::Vec<
        Graph3GraphEvidenceDisclosureDeficiencyCitationsItem,
    >,
    #[serde(rename = "resolutionLimitations")]
    pub resolution_limitations: ::std::vec::Vec<
        Graph3GraphEvidenceDisclosureResolutionLimitationsItem,
    >,
    #[serde(rename = "scopeIds")]
    pub scope_ids: ::std::vec::Vec<Graph3ScopeId>,
}
///`Graph3GraphEvidenceDisclosureDeficiencyCitationsItem`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Graph3GraphEvidenceDisclosureDeficiencyCitationsItem {
    pub cause: Graph3GraphEvidenceDisclosureDeficiencyCitationsItemCause,
    #[serde(
        rename = "coverageId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub coverage_id: FieldPresence<::std::option::Option<Common3CoverageId>>,
    #[serde(rename = "inputRefs")]
    pub input_refs: ::std::vec::Vec<
        Graph3GraphEvidenceDisclosureDeficiencyCitationsItemInputRefsItem,
    >,
    #[serde(
        rename = "nativeCause",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub native_cause: FieldPresence<
        ::std::option::Option<
            Graph3GraphEvidenceDisclosureDeficiencyCitationsItemNativeCause,
        >,
    >,
    #[serde(
        rename = "predicateId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub predicate_id: FieldPresence<
        ::std::option::Option<
            Graph3GraphEvidenceDisclosureDeficiencyCitationsItemPredicateId,
        >,
    >,
    pub source: Graph3GraphEvidenceDisclosureDeficiencyCitationsItemSource,
    #[serde(
        rename = "subjectId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub subject_id: FieldPresence<::std::option::Option<Common3SubjectId>>,
}
///`Graph3GraphEvidenceDisclosureDeficiencyCitationsItemCause`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Graph3GraphEvidenceDisclosureDeficiencyCitationsItemCause(
    ::std::string::String,
);
impl ::std::ops::Deref for Graph3GraphEvidenceDisclosureDeficiencyCitationsItemCause {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Graph3GraphEvidenceDisclosureDeficiencyCitationsItemCause>
for ::std::string::String {
    fn from(value: Graph3GraphEvidenceDisclosureDeficiencyCitationsItemCause) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Graph3GraphEvidenceDisclosureDeficiencyCitationsItemCause {
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
impl ::std::convert::TryFrom<&str>
for Graph3GraphEvidenceDisclosureDeficiencyCitationsItemCause {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Graph3GraphEvidenceDisclosureDeficiencyCitationsItemCause {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de>
for Graph3GraphEvidenceDisclosureDeficiencyCitationsItemCause {
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
///`Graph3GraphEvidenceDisclosureDeficiencyCitationsItemInputRefsItem`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Graph3GraphEvidenceDisclosureDeficiencyCitationsItemInputRefsItem {
    pub digest: Common3Sha256Hex,
    pub domain: Graph3GraphEvidenceDisclosureDeficiencyCitationsItemInputRefsItemDomain,
}
///`Graph3GraphEvidenceDisclosureDeficiencyCitationsItemInputRefsItemDomain`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Graph3GraphEvidenceDisclosureDeficiencyCitationsItemInputRefsItemDomain(
    ::std::string::String,
);
impl ::std::ops::Deref
for Graph3GraphEvidenceDisclosureDeficiencyCitationsItemInputRefsItemDomain {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<
    Graph3GraphEvidenceDisclosureDeficiencyCitationsItemInputRefsItemDomain,
> for ::std::string::String {
    fn from(
        value: Graph3GraphEvidenceDisclosureDeficiencyCitationsItemInputRefsItemDomain,
    ) -> Self {
        value.0
    }
}
impl ::std::str::FromStr
for Graph3GraphEvidenceDisclosureDeficiencyCitationsItemInputRefsItemDomain {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 64usize {
            return Err("longer than 64 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str>
for Graph3GraphEvidenceDisclosureDeficiencyCitationsItemInputRefsItemDomain {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Graph3GraphEvidenceDisclosureDeficiencyCitationsItemInputRefsItemDomain {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de>
for Graph3GraphEvidenceDisclosureDeficiencyCitationsItemInputRefsItemDomain {
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
///`Graph3GraphEvidenceDisclosureDeficiencyCitationsItemNativeCause`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Graph3GraphEvidenceDisclosureDeficiencyCitationsItemNativeCause(
    ::std::string::String,
);
impl ::std::ops::Deref
for Graph3GraphEvidenceDisclosureDeficiencyCitationsItemNativeCause {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<
    Graph3GraphEvidenceDisclosureDeficiencyCitationsItemNativeCause,
> for ::std::string::String {
    fn from(
        value: Graph3GraphEvidenceDisclosureDeficiencyCitationsItemNativeCause,
    ) -> Self {
        value.0
    }
}
impl ::std::str::FromStr
for Graph3GraphEvidenceDisclosureDeficiencyCitationsItemNativeCause {
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
impl ::std::convert::TryFrom<&str>
for Graph3GraphEvidenceDisclosureDeficiencyCitationsItemNativeCause {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Graph3GraphEvidenceDisclosureDeficiencyCitationsItemNativeCause {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de>
for Graph3GraphEvidenceDisclosureDeficiencyCitationsItemNativeCause {
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
///`Graph3GraphEvidenceDisclosureDeficiencyCitationsItemPredicateId`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Graph3GraphEvidenceDisclosureDeficiencyCitationsItemPredicateId(
    ::std::string::String,
);
impl ::std::ops::Deref
for Graph3GraphEvidenceDisclosureDeficiencyCitationsItemPredicateId {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<
    Graph3GraphEvidenceDisclosureDeficiencyCitationsItemPredicateId,
> for ::std::string::String {
    fn from(
        value: Graph3GraphEvidenceDisclosureDeficiencyCitationsItemPredicateId,
    ) -> Self {
        value.0
    }
}
impl ::std::str::FromStr
for Graph3GraphEvidenceDisclosureDeficiencyCitationsItemPredicateId {
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
impl ::std::convert::TryFrom<&str>
for Graph3GraphEvidenceDisclosureDeficiencyCitationsItemPredicateId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Graph3GraphEvidenceDisclosureDeficiencyCitationsItemPredicateId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de>
for Graph3GraphEvidenceDisclosureDeficiencyCitationsItemPredicateId {
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
///`Graph3GraphEvidenceDisclosureDeficiencyCitationsItemSource`
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
pub enum Graph3GraphEvidenceDisclosureDeficiencyCitationsItemSource {
    #[serde(rename = "enumeration")]
    Enumeration,
    #[serde(rename = "native")]
    Native,
    #[serde(rename = "import")]
    Import,
    #[serde(rename = "execution")]
    Execution,
    #[serde(rename = "correspondence")]
    Correspondence,
}
impl ::std::fmt::Display for Graph3GraphEvidenceDisclosureDeficiencyCitationsItemSource {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Enumeration => f.write_str("enumeration"),
            Self::Native => f.write_str("native"),
            Self::Import => f.write_str("import"),
            Self::Execution => f.write_str("execution"),
            Self::Correspondence => f.write_str("correspondence"),
        }
    }
}
impl ::std::str::FromStr for Graph3GraphEvidenceDisclosureDeficiencyCitationsItemSource {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "enumeration" => Ok(Self::Enumeration),
            "native" => Ok(Self::Native),
            "import" => Ok(Self::Import),
            "execution" => Ok(Self::Execution),
            "correspondence" => Ok(Self::Correspondence),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str>
for Graph3GraphEvidenceDisclosureDeficiencyCitationsItemSource {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Graph3GraphEvidenceDisclosureDeficiencyCitationsItemSource {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Graph3GraphEvidenceDisclosureResolutionLimitationsItem`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Graph3GraphEvidenceDisclosureResolutionLimitationsItem {
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub attempted: FieldPresence<::std::option::Option<bool>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub coverage: FieldPresence<
        ::std::option::Option<
            Graph3GraphEvidenceDisclosureResolutionLimitationsItemCoverage,
        >,
    >,
    #[serde(
        rename = "coverageId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub coverage_id: FieldPresence<::std::option::Option<Common3CoverageId>>,
    #[serde(
        rename = "examinedExhaustive",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub examined_exhaustive: FieldPresence<::std::option::Option<bool>>,
    #[serde(
        rename = "factId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub fact_id: FieldPresence<::std::option::Option<Graph3FactId>>,
    #[serde(
        rename = "incomingSearchDigest",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub incoming_search_digest: FieldPresence<::std::option::Option<Common3Sha256Hex>>,
    pub kind: Graph3GraphEvidenceDisclosureResolutionLimitationsItemKind,
    #[serde(
        rename = "minResolution",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub min_resolution: FieldPresence<::std::option::Option<Common3CanonicalIdentifier>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub note: FieldPresence<::std::option::Option<Common3BoundedText>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub relation: FieldPresence<::std::option::Option<Common3CanonicalIdentifier>>,
    #[serde(
        rename = "resolutionState",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub resolution_state: FieldPresence<
        ::std::option::Option<
            Graph3GraphEvidenceDisclosureResolutionLimitationsItemResolutionState,
        >,
    >,
    #[serde(
        rename = "unresolvedEdgeCount",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub unresolved_edge_count: FieldPresence<::std::option::Option<Common3Uint53>>,
}
///`Graph3GraphEvidenceDisclosureResolutionLimitationsItemCoverage`
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
pub enum Graph3GraphEvidenceDisclosureResolutionLimitationsItemCoverage {
    #[serde(rename = "complete")]
    Complete,
    #[serde(rename = "partial")]
    Partial,
    #[serde(rename = "unknown")]
    Unknown,
}
impl ::std::fmt::Display
for Graph3GraphEvidenceDisclosureResolutionLimitationsItemCoverage {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Complete => f.write_str("complete"),
            Self::Partial => f.write_str("partial"),
            Self::Unknown => f.write_str("unknown"),
        }
    }
}
impl ::std::str::FromStr
for Graph3GraphEvidenceDisclosureResolutionLimitationsItemCoverage {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "complete" => Ok(Self::Complete),
            "partial" => Ok(Self::Partial),
            "unknown" => Ok(Self::Unknown),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str>
for Graph3GraphEvidenceDisclosureResolutionLimitationsItemCoverage {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Graph3GraphEvidenceDisclosureResolutionLimitationsItemCoverage {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Graph3GraphEvidenceDisclosureResolutionLimitationsItemKind`
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
pub enum Graph3GraphEvidenceDisclosureResolutionLimitationsItemKind {
    #[serde(rename = "unexamined-work-bound")]
    UnexaminedWorkBound,
    #[serde(rename = "unprojectable-fact")]
    UnprojectableFact,
    #[serde(rename = "resolution-incomplete")]
    ResolutionIncomplete,
    #[serde(rename = "resolution-partial")]
    ResolutionPartial,
    #[serde(rename = "resolution-not-attempted")]
    ResolutionNotAttempted,
    #[serde(rename = "coverage-unknown")]
    CoverageUnknown,
    #[serde(rename = "coverage-partial")]
    CoveragePartial,
    #[serde(rename = "unresolved-edge-present")]
    UnresolvedEdgePresent,
    #[serde(rename = "examined-not-exhaustive")]
    ExaminedNotExhaustive,
    #[serde(rename = "unsupported-rung-omitted")]
    UnsupportedRungOmitted,
    #[serde(rename = "incoming-search-incomplete")]
    IncomingSearchIncomplete,
    #[serde(rename = "native-evidence-unavailable")]
    NativeEvidenceUnavailable,
}
impl ::std::fmt::Display for Graph3GraphEvidenceDisclosureResolutionLimitationsItemKind {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::UnexaminedWorkBound => f.write_str("unexamined-work-bound"),
            Self::UnprojectableFact => f.write_str("unprojectable-fact"),
            Self::ResolutionIncomplete => f.write_str("resolution-incomplete"),
            Self::ResolutionPartial => f.write_str("resolution-partial"),
            Self::ResolutionNotAttempted => f.write_str("resolution-not-attempted"),
            Self::CoverageUnknown => f.write_str("coverage-unknown"),
            Self::CoveragePartial => f.write_str("coverage-partial"),
            Self::UnresolvedEdgePresent => f.write_str("unresolved-edge-present"),
            Self::ExaminedNotExhaustive => f.write_str("examined-not-exhaustive"),
            Self::UnsupportedRungOmitted => f.write_str("unsupported-rung-omitted"),
            Self::IncomingSearchIncomplete => f.write_str("incoming-search-incomplete"),
            Self::NativeEvidenceUnavailable => f.write_str("native-evidence-unavailable"),
        }
    }
}
impl ::std::str::FromStr for Graph3GraphEvidenceDisclosureResolutionLimitationsItemKind {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "unexamined-work-bound" => Ok(Self::UnexaminedWorkBound),
            "unprojectable-fact" => Ok(Self::UnprojectableFact),
            "resolution-incomplete" => Ok(Self::ResolutionIncomplete),
            "resolution-partial" => Ok(Self::ResolutionPartial),
            "resolution-not-attempted" => Ok(Self::ResolutionNotAttempted),
            "coverage-unknown" => Ok(Self::CoverageUnknown),
            "coverage-partial" => Ok(Self::CoveragePartial),
            "unresolved-edge-present" => Ok(Self::UnresolvedEdgePresent),
            "examined-not-exhaustive" => Ok(Self::ExaminedNotExhaustive),
            "unsupported-rung-omitted" => Ok(Self::UnsupportedRungOmitted),
            "incoming-search-incomplete" => Ok(Self::IncomingSearchIncomplete),
            "native-evidence-unavailable" => Ok(Self::NativeEvidenceUnavailable),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str>
for Graph3GraphEvidenceDisclosureResolutionLimitationsItemKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Graph3GraphEvidenceDisclosureResolutionLimitationsItemKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Graph3GraphEvidenceDisclosureResolutionLimitationsItemResolutionState`
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
pub enum Graph3GraphEvidenceDisclosureResolutionLimitationsItemResolutionState {
    #[serde(rename = "not-attempted")]
    NotAttempted,
    #[serde(rename = "partial")]
    Partial,
    #[serde(rename = "complete")]
    Complete,
    #[serde(rename = "not-applicable")]
    NotApplicable,
    #[serde(rename = "incomplete")]
    Incomplete,
}
impl ::std::fmt::Display
for Graph3GraphEvidenceDisclosureResolutionLimitationsItemResolutionState {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::NotAttempted => f.write_str("not-attempted"),
            Self::Partial => f.write_str("partial"),
            Self::Complete => f.write_str("complete"),
            Self::NotApplicable => f.write_str("not-applicable"),
            Self::Incomplete => f.write_str("incomplete"),
        }
    }
}
impl ::std::str::FromStr
for Graph3GraphEvidenceDisclosureResolutionLimitationsItemResolutionState {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "not-attempted" => Ok(Self::NotAttempted),
            "partial" => Ok(Self::Partial),
            "complete" => Ok(Self::Complete),
            "not-applicable" => Ok(Self::NotApplicable),
            "incomplete" => Ok(Self::Incomplete),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str>
for Graph3GraphEvidenceDisclosureResolutionLimitationsItemResolutionState {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Graph3GraphEvidenceDisclosureResolutionLimitationsItemResolutionState {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Graph3GraphNeighborRow`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Graph3GraphNeighborRow {
    #[serde(
        rename = "confidenceMillionths",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub confidence_millionths: FieldPresence<::std::option::Option<Common3Uint53>>,
    #[serde(rename = "factId")]
    pub fact_id: Graph3FactId,
    #[serde(
        rename = "producerClosure",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub producer_closure: FieldPresence<::std::option::Option<Common3ClosureId>>,
    pub relation: Common3CanonicalIdentifier,
    pub resolution: Common3CanonicalIdentifier,
    pub source: Graph3GraphEndpoint,
    pub target: Graph3GraphEndpoint,
}
///`Graph3GraphNeighborsParams`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Graph3GraphNeighborsParams {
    pub direction: Graph3GraphDirection,
    pub endpoint: Graph3GraphEndpoint,
    #[serde(
        rename = "factViewDigests",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub fact_view_digests: FieldPresence<::std::option::Option<Graph3FactViewDigests>>,
    #[serde(rename = "minResolution")]
    pub min_resolution: Common3CanonicalIdentifier,
    pub relation: Common3CanonicalIdentifier,
}
///`Graph3GraphOperation`
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
pub enum Graph3GraphOperation {
    #[serde(rename = "graph.neighbors")]
    GraphNeighbors,
    #[serde(rename = "graph.path")]
    GraphPath,
    #[serde(rename = "graph.reach")]
    GraphReach,
}
impl ::std::fmt::Display for Graph3GraphOperation {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::GraphNeighbors => f.write_str("graph.neighbors"),
            Self::GraphPath => f.write_str("graph.path"),
            Self::GraphReach => f.write_str("graph.reach"),
        }
    }
}
impl ::std::str::FromStr for Graph3GraphOperation {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "graph.neighbors" => Ok(Self::GraphNeighbors),
            "graph.path" => Ok(Self::GraphPath),
            "graph.reach" => Ok(Self::GraphReach),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Graph3GraphOperation {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Graph3GraphOperation {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Mandatory graph.* response context. resolvedView is run3 only. traversalCoverage is not native CoverageResult. totalItems is qualified by countBasis. evidence is required. advisory is const false.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Graph3GraphOperationResponseContext {
    pub advisory: ::serde_json::Value,
    pub availability: Graph3GraphOperationResponseContextAvailability,
    #[serde(rename = "countBasis")]
    pub count_basis: Graph3CountBasis,
    pub evidence: Graph3GraphEvidenceDisclosure,
    #[serde(rename = "factViewDigests")]
    pub fact_view_digests: ::std::vec::Vec<Graph3ViewDigest>,
    #[serde(
        rename = "nextCursor",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub next_cursor: FieldPresence<
        ::std::option::Option<Graph3GraphOperationResponseContextNextCursor>,
    >,
    #[serde(rename = "producedItems")]
    pub produced_items: Common3Uint53,
    #[serde(rename = "projectId")]
    pub project_id: Common3ProjectId,
    #[serde(rename = "resolvedView")]
    pub resolved_view: Graph3ResolvedView,
    #[serde(rename = "totalItems")]
    pub total_items: Common3Uint53,
    #[serde(rename = "traversalCoverage")]
    pub traversal_coverage: Graph3TraversalCoverage,
    ///true iff traversalCoverage is truncated-bound (operation-level). Full page is not truncated.
    pub truncated: bool,
    #[serde(rename = "visitedNodes")]
    pub visited_nodes: Common3Uint53,
}
///`Graph3GraphOperationResponseContextAvailability`
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
pub enum Graph3GraphOperationResponseContextAvailability {
    #[serde(rename = "retained")]
    Retained,
    #[serde(rename = "partial")]
    Partial,
    #[serde(rename = "expired")]
    Expired,
    #[serde(rename = "purged")]
    Purged,
    #[serde(rename = "corrupt")]
    Corrupt,
    #[serde(rename = "unavailable")]
    Unavailable,
}
impl ::std::fmt::Display for Graph3GraphOperationResponseContextAvailability {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Retained => f.write_str("retained"),
            Self::Partial => f.write_str("partial"),
            Self::Expired => f.write_str("expired"),
            Self::Purged => f.write_str("purged"),
            Self::Corrupt => f.write_str("corrupt"),
            Self::Unavailable => f.write_str("unavailable"),
        }
    }
}
impl ::std::str::FromStr for Graph3GraphOperationResponseContextAvailability {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "retained" => Ok(Self::Retained),
            "partial" => Ok(Self::Partial),
            "expired" => Ok(Self::Expired),
            "purged" => Ok(Self::Purged),
            "corrupt" => Ok(Self::Corrupt),
            "unavailable" => Ok(Self::Unavailable),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Graph3GraphOperationResponseContextAvailability {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Graph3GraphOperationResponseContextAvailability {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Graph3GraphOperationResponseContextNextCursor`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Graph3GraphOperationResponseContextNextCursor(::std::string::String);
impl ::std::ops::Deref for Graph3GraphOperationResponseContextNextCursor {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Graph3GraphOperationResponseContextNextCursor>
for ::std::string::String {
    fn from(value: Graph3GraphOperationResponseContextNextCursor) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Graph3GraphOperationResponseContextNextCursor {
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
impl ::std::convert::TryFrom<&str> for Graph3GraphOperationResponseContextNextCursor {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Graph3GraphOperationResponseContextNextCursor {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Graph3GraphOperationResponseContextNextCursor {
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
///`Graph3GraphPathEdge`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Graph3GraphPathEdge {
    #[serde(rename = "factId")]
    pub fact_id: Graph3FactId,
    pub source: Graph3GraphEndpoint,
    pub target: Graph3GraphEndpoint,
}
///`Graph3GraphPathParams`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Graph3GraphPathParams {
    pub direction: Graph3GraphDirection,
    #[serde(
        rename = "factViewDigests",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub fact_view_digests: FieldPresence<::std::option::Option<Graph3FactViewDigests>>,
    ///Semantic hop bound (GX-01), not a free work cutoff. Required completion means complete within this declared depth.
    #[serde(rename = "maxDepth")]
    pub max_depth: ::std::num::NonZeroU64,
    #[serde(rename = "minResolution")]
    pub min_resolution: Common3CanonicalIdentifier,
    pub relation: Common3CanonicalIdentifier,
    pub start: Graph3GraphEndpoint,
    pub target: Graph3GraphEndpoint,
}
///One simple path. start==target yields hopCount 0, nodes [start], edges []. Otherwise shortest hop count with canonical fact2-id-sequence tie-break. No optional closing cycle.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Graph3GraphPathRow {
    pub edges: ::std::vec::Vec<Graph3GraphPathEdge>,
    #[serde(rename = "hopCount")]
    pub hop_count: Common3Uint53,
    pub nodes: ::std::vec::Vec<Graph3GraphEndpoint>,
    pub start: Graph3GraphEndpoint,
    pub target: Graph3GraphEndpoint,
}
///`Graph3GraphQueryRequestV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Graph3GraphQueryRequestV1 {
    pub completeness: Graph3GraphQueryRequestV1Completeness,
    #[serde(
        rename = "fieldSelection",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub field_selection: FieldPresence<
        ::std::option::Option<::std::vec::Vec<Common3CanonicalIdentifier>>,
    >,
    pub operation: Graph3Operation,
    pub page: Graph3Page,
    ///Closed per operation by the allOf joins below. Graph ops use GraphNeighborsParams/GraphPathParams/GraphReachParams. Other 17 operations keep Params.
    pub params: ::serde_json::Map<::std::string::String, ::serde_json::Value>,
    #[serde(rename = "projectId")]
    pub project_id: Common3ProjectId,
    #[serde(rename = "schemaFamily")]
    pub schema_family: ::serde_json::Value,
    #[serde(rename = "schemaMajor")]
    pub schema_major: ExactInteger,
    pub view: Graph3View,
}
///`Graph3GraphQueryRequestV1Completeness`
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
pub enum Graph3GraphQueryRequestV1Completeness {
    #[serde(rename = "required")]
    Required,
    #[serde(rename = "best-effort")]
    BestEffort,
}
impl ::std::fmt::Display for Graph3GraphQueryRequestV1Completeness {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Required => f.write_str("required"),
            Self::BestEffort => f.write_str("best-effort"),
        }
    }
}
impl ::std::str::FromStr for Graph3GraphQueryRequestV1Completeness {
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
impl ::std::convert::TryFrom<&str> for Graph3GraphQueryRequestV1Completeness {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Graph3GraphQueryRequestV1Completeness {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Response context for the 17 non-graph operations. resolvedView remains request View so snapshot metadata operations are not forced to run-only. Graph operations MUST use GraphOperationResponseContext instead.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Graph3GraphQueryResponseContext {
    ///true exactly for AdvisoryOperation members
    pub advisory: bool,
    pub availability: Graph3GraphQueryResponseContextAvailability,
    pub coverage: Graph3GraphQueryResponseContextCoverage,
    #[serde(
        rename = "nextCursor",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub next_cursor: FieldPresence<
        ::std::option::Option<Graph3GraphQueryResponseContextNextCursor>,
    >,
    #[serde(rename = "projectId")]
    pub project_id: Common3ProjectId,
    #[serde(rename = "resolvedView")]
    pub resolved_view: Graph3View,
    #[serde(rename = "totalItems")]
    pub total_items: Common3Uint53,
    pub truncated: bool,
}
///`Graph3GraphQueryResponseContextAvailability`
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
pub enum Graph3GraphQueryResponseContextAvailability {
    #[serde(rename = "retained")]
    Retained,
    #[serde(rename = "partial")]
    Partial,
    #[serde(rename = "expired")]
    Expired,
    #[serde(rename = "purged")]
    Purged,
    #[serde(rename = "corrupt")]
    Corrupt,
    #[serde(rename = "unavailable")]
    Unavailable,
}
impl ::std::fmt::Display for Graph3GraphQueryResponseContextAvailability {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Retained => f.write_str("retained"),
            Self::Partial => f.write_str("partial"),
            Self::Expired => f.write_str("expired"),
            Self::Purged => f.write_str("purged"),
            Self::Corrupt => f.write_str("corrupt"),
            Self::Unavailable => f.write_str("unavailable"),
        }
    }
}
impl ::std::str::FromStr for Graph3GraphQueryResponseContextAvailability {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "retained" => Ok(Self::Retained),
            "partial" => Ok(Self::Partial),
            "expired" => Ok(Self::Expired),
            "purged" => Ok(Self::Purged),
            "corrupt" => Ok(Self::Corrupt),
            "unavailable" => Ok(Self::Unavailable),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Graph3GraphQueryResponseContextAvailability {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Graph3GraphQueryResponseContextAvailability {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Graph3GraphQueryResponseContextCoverage`
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
pub enum Graph3GraphQueryResponseContextCoverage {
    #[serde(rename = "complete")]
    Complete,
    #[serde(rename = "partial")]
    Partial,
    #[serde(rename = "unavailable")]
    Unavailable,
}
impl ::std::fmt::Display for Graph3GraphQueryResponseContextCoverage {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Complete => f.write_str("complete"),
            Self::Partial => f.write_str("partial"),
            Self::Unavailable => f.write_str("unavailable"),
        }
    }
}
impl ::std::str::FromStr for Graph3GraphQueryResponseContextCoverage {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "complete" => Ok(Self::Complete),
            "partial" => Ok(Self::Partial),
            "unavailable" => Ok(Self::Unavailable),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Graph3GraphQueryResponseContextCoverage {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Graph3GraphQueryResponseContextCoverage {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Graph3GraphQueryResponseContextNextCursor`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Graph3GraphQueryResponseContextNextCursor(::std::string::String);
impl ::std::ops::Deref for Graph3GraphQueryResponseContextNextCursor {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Graph3GraphQueryResponseContextNextCursor>
for ::std::string::String {
    fn from(value: Graph3GraphQueryResponseContextNextCursor) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Graph3GraphQueryResponseContextNextCursor {
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
impl ::std::convert::TryFrom<&str> for Graph3GraphQueryResponseContextNextCursor {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Graph3GraphQueryResponseContextNextCursor {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Graph3GraphQueryResponseContextNextCursor {
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
///`Graph3GraphQueryResponseV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Graph3GraphQueryResponseV1 {
    pub context: ::serde_json::Map<::std::string::String, ::serde_json::Value>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub items: FieldPresence<::std::vec::Vec<::serde_json::Value>>,
    pub operation: Graph3Operation,
    #[serde(rename = "schemaFamily")]
    pub schema_family: ::serde_json::Value,
    #[serde(rename = "schemaMajor")]
    pub schema_major: ExactInteger,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub termination: FieldPresence<::std::option::Option<Common3StepTermination>>,
}
///`Graph3GraphReachParams`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Graph3GraphReachParams {
    pub direction: Graph3GraphDirection,
    #[serde(
        rename = "factViewDigests",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub fact_view_digests: FieldPresence<::std::option::Option<Graph3FactViewDigests>>,
    ///Closed reach field. Admission default false when omitted. Start is excluded unless true. Not an optional closing cycle.
    #[serde(
        rename = "includeStart",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub include_start: FieldPresence<::std::option::Option<bool>>,
    ///Semantic hop bound (GX-01).
    #[serde(rename = "maxDepth")]
    pub max_depth: ::std::num::NonZeroU64,
    #[serde(rename = "minResolution")]
    pub min_resolution: Common3CanonicalIdentifier,
    pub relation: Common3CanonicalIdentifier,
    pub start: Graph3GraphEndpoint,
}
///`Graph3GraphReachRow`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Graph3GraphReachRow {
    pub depth: Common3Uint53,
    pub endpoint: Graph3GraphEndpoint,
    ///Fact that first reached this endpoint on the canonical walk. Omitted for the start row when includeStart is true.
    #[serde(
        rename = "viaFactId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub via_fact_id: FieldPresence<::std::option::Option<Graph3FactId>>,
}
///Native evaluation-subject id as stored on inventory/fact payload. Not a backend numeric id.
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Graph3NativeSubjectId(::std::string::String);
impl ::std::ops::Deref for Graph3NativeSubjectId {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Graph3NativeSubjectId> for ::std::string::String {
    fn from(value: Graph3NativeSubjectId) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Graph3NativeSubjectId {
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
impl ::std::convert::TryFrom<&str> for Graph3NativeSubjectId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Graph3NativeSubjectId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Graph3NativeSubjectId {
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
///`Graph3Operation`
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
pub enum Graph3Operation {
    #[serde(rename = "run.show")]
    RunShow,
    #[serde(rename = "run.list")]
    RunList,
    #[serde(rename = "finding.list")]
    FindingList,
    #[serde(rename = "finding.show")]
    FindingShow,
    #[serde(rename = "fact.list")]
    FactList,
    #[serde(rename = "coverage.show")]
    CoverageShow,
    #[serde(rename = "artifact.get")]
    ArtifactGet,
    #[serde(rename = "graph.neighbors")]
    GraphNeighbors,
    #[serde(rename = "graph.path")]
    GraphPath,
    #[serde(rename = "graph.reach")]
    GraphReach,
    #[serde(rename = "baseline.show")]
    BaselineShow,
    #[serde(rename = "comparison.show")]
    ComparisonShow,
    #[serde(rename = "comparison.diff")]
    ComparisonDiff,
    #[serde(rename = "candidate.list")]
    CandidateList,
    #[serde(rename = "inspection.show")]
    InspectionShow,
    #[serde(rename = "review.brief")]
    ReviewBrief,
    #[serde(rename = "policy.effective")]
    PolicyEffective,
    #[serde(rename = "import.show")]
    ImportShow,
    #[serde(rename = "receipt.show")]
    ReceiptShow,
    #[serde(rename = "availability.show")]
    AvailabilityShow,
}
impl ::std::fmt::Display for Graph3Operation {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::RunShow => f.write_str("run.show"),
            Self::RunList => f.write_str("run.list"),
            Self::FindingList => f.write_str("finding.list"),
            Self::FindingShow => f.write_str("finding.show"),
            Self::FactList => f.write_str("fact.list"),
            Self::CoverageShow => f.write_str("coverage.show"),
            Self::ArtifactGet => f.write_str("artifact.get"),
            Self::GraphNeighbors => f.write_str("graph.neighbors"),
            Self::GraphPath => f.write_str("graph.path"),
            Self::GraphReach => f.write_str("graph.reach"),
            Self::BaselineShow => f.write_str("baseline.show"),
            Self::ComparisonShow => f.write_str("comparison.show"),
            Self::ComparisonDiff => f.write_str("comparison.diff"),
            Self::CandidateList => f.write_str("candidate.list"),
            Self::InspectionShow => f.write_str("inspection.show"),
            Self::ReviewBrief => f.write_str("review.brief"),
            Self::PolicyEffective => f.write_str("policy.effective"),
            Self::ImportShow => f.write_str("import.show"),
            Self::ReceiptShow => f.write_str("receipt.show"),
            Self::AvailabilityShow => f.write_str("availability.show"),
        }
    }
}
impl ::std::str::FromStr for Graph3Operation {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "run.show" => Ok(Self::RunShow),
            "run.list" => Ok(Self::RunList),
            "finding.list" => Ok(Self::FindingList),
            "finding.show" => Ok(Self::FindingShow),
            "fact.list" => Ok(Self::FactList),
            "coverage.show" => Ok(Self::CoverageShow),
            "artifact.get" => Ok(Self::ArtifactGet),
            "graph.neighbors" => Ok(Self::GraphNeighbors),
            "graph.path" => Ok(Self::GraphPath),
            "graph.reach" => Ok(Self::GraphReach),
            "baseline.show" => Ok(Self::BaselineShow),
            "comparison.show" => Ok(Self::ComparisonShow),
            "comparison.diff" => Ok(Self::ComparisonDiff),
            "candidate.list" => Ok(Self::CandidateList),
            "inspection.show" => Ok(Self::InspectionShow),
            "review.brief" => Ok(Self::ReviewBrief),
            "policy.effective" => Ok(Self::PolicyEffective),
            "import.show" => Ok(Self::ImportShow),
            "receipt.show" => Ok(Self::ReceiptShow),
            "availability.show" => Ok(Self::AvailabilityShow),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Graph3Operation {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Graph3Operation {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Graph3Page`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Graph3Page {
    ///Opaque host token bound to projectId+runId+factViewDigests+operation+effective params/order+page position. Continuation never re-resolves latest. Reference form q3.<runId-64hex>.<selectionHash64>.<position>.
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub cursor: FieldPresence<::std::option::Option<Graph3PageCursor>>,
    pub size: ::std::num::NonZeroU64,
}
///Opaque host token bound to projectId+runId+factViewDigests+operation+effective params/order+page position. Continuation never re-resolves latest. Reference form q3.<runId-64hex>.<selectionHash64>.<position>.
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Graph3PageCursor(::std::string::String);
impl ::std::ops::Deref for Graph3PageCursor {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Graph3PageCursor> for ::std::string::String {
    fn from(value: Graph3PageCursor) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Graph3PageCursor {
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
impl ::std::convert::TryFrom<&str> for Graph3PageCursor {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Graph3PageCursor {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Graph3PageCursor {
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
///Closed optional bag for the 17 non-graph operations only. Graph operations must not use this shape.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug, Default)]
#[serde(deny_unknown_fields)]
pub struct Graph3Params {
    #[serde(
        rename = "artifactRef",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub artifact_ref: FieldPresence<::std::option::Option<Graph3ParamsArtifactRef>>,
    #[serde(
        rename = "baselineId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub baseline_id: FieldPresence<::std::option::Option<Common3BaselineId>>,
    #[serde(
        rename = "candidateId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub candidate_id: FieldPresence<::std::option::Option<Common3CandidateId>>,
    #[serde(
        rename = "comparisonResultId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub comparison_result_id: FieldPresence<
        ::std::option::Option<Common3ComparisonResultId>,
    >,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub direction: FieldPresence<::std::option::Option<Graph3ParamsDirection>>,
    #[serde(
        rename = "findingId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub finding_id: FieldPresence<::std::option::Option<Common3FindingId>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub fingerprint: FieldPresence<::std::option::Option<Common3Fingerprint>>,
    #[serde(
        rename = "importId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub import_id: FieldPresence<::std::option::Option<Common3ImportId>>,
    #[serde(
        rename = "includeSuppressed",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub include_suppressed: FieldPresence<::std::option::Option<bool>>,
    #[serde(
        rename = "maxDepth",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub max_depth: FieldPresence<::std::option::Option<::std::num::NonZeroU64>>,
    #[serde(
        rename = "otherRunId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub other_run_id: FieldPresence<::std::option::Option<Common3RunId>>,
    #[serde(
        rename = "receiptId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub receipt_id: FieldPresence<::std::option::Option<Common3ReceiptId>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub relation: FieldPresence<::std::option::Option<Common3CanonicalIdentifier>>,
    #[serde(
        rename = "ruleId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub rule_id: FieldPresence<::std::option::Option<Common3CanonicalIdentifier>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub subject: FieldPresence<::std::option::Option<Common3LogicalPath>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub target: FieldPresence<::std::option::Option<Common3LogicalPath>>,
}
///`Graph3ParamsArtifactRef`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Graph3ParamsArtifactRef {
    pub digest: Common3Sha256Hex,
    pub domain: Graph3ParamsArtifactRefDomain,
}
///`Graph3ParamsArtifactRefDomain`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Graph3ParamsArtifactRefDomain(::std::string::String);
impl ::std::ops::Deref for Graph3ParamsArtifactRefDomain {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Graph3ParamsArtifactRefDomain> for ::std::string::String {
    fn from(value: Graph3ParamsArtifactRefDomain) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Graph3ParamsArtifactRefDomain {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 64usize {
            return Err("longer than 64 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Graph3ParamsArtifactRefDomain {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Graph3ParamsArtifactRefDomain {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Graph3ParamsArtifactRefDomain {
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
///`Graph3ParamsDirection`
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
pub enum Graph3ParamsDirection {
    #[serde(rename = "outgoing")]
    Outgoing,
    #[serde(rename = "incoming")]
    Incoming,
    #[serde(rename = "both")]
    Both,
}
impl ::std::fmt::Display for Graph3ParamsDirection {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Outgoing => f.write_str("outgoing"),
            Self::Incoming => f.write_str("incoming"),
            Self::Both => f.write_str("both"),
        }
    }
}
impl ::std::str::FromStr for Graph3ParamsDirection {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "outgoing" => Ok(Self::Outgoing),
            "incoming" => Ok(Self::Incoming),
            "both" => Ok(Self::Both),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Graph3ParamsDirection {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Graph3ParamsDirection {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Graph-operation response view. Concrete run3 only. latest and snapshotId are forbidden here so a page cannot re-resolve.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Graph3ResolvedView {
    #[serde(rename = "runId")]
    pub run_id: Common3RunId,
}
///Every query names one ProjectId and exactly one view selector. The 20 operation names are unchanged. Parameters are closed per operation. Graph operations (graph.neighbors|path|reach) select an admitted Run plus fact-view set and native endpoints {universe,kind,nativeSubjectId,(packageManifestPath)}. They do not accept LogicalPath-only subject/target. Response ResolvedView for graph.* is {runId} only; request View may still name snapshotId or latest as a resolver that must yield a unique Run. Non-graph snapshot metadata operations keep request View on the response and MUST NOT be forced to run-only. Bounds (schema constants, not request fields): page size 1..1000 (default 100); at most 100000 items per logical operation; traversal depth at most 64; at most 1000000 visited nodes. Work bounds apply across the logical operation and do not reset per page. A bound reached under completeness=required is QUERY.COMPLETENESS_UNMET (indeterminate); under best-effort it is truncated-bound with no continuation past the cap. Queries never materialise facts, invoke a provider, allocate an attempt, seal a Run, derive policy or choose termination. Advisory is cross-joined: true exactly for AdvisoryOperation members, false for graph.* and the remaining non-advisory operations. Evaluator3 schemaMajor 3. params.findingId locates unmatched and matched findings on finding ops. params.fingerprint locates matched occurrences only. RunId is run3. Native/input prefixes stay snapshot2/plan2/closure2/import2/fact2/view2. No global database id and no FactViewId recipe.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(transparent)]
pub struct Graph3Root(pub ::serde_json::Value);
impl ::std::ops::Deref for Graph3Root {
    type Target = ::serde_json::Value;
    fn deref(&self) -> &::serde_json::Value {
        &self.0
    }
}
impl ::std::convert::From<Graph3Root> for ::serde_json::Value {
    fn from(value: Graph3Root) -> Self {
        value.0
    }
}
impl ::std::convert::From<::serde_json::Value> for Graph3Root {
    fn from(value: ::serde_json::Value) -> Self {
        Self(value)
    }
}
///`Graph3ScopeId`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
#[serde(transparent)]
pub struct Graph3ScopeId(pub ::std::string::String);
impl ::std::ops::Deref for Graph3ScopeId {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Graph3ScopeId> for ::std::string::String {
    fn from(value: Graph3ScopeId) -> Self {
        value.0
    }
}
impl ::std::convert::From<::std::string::String> for Graph3ScopeId {
    fn from(value: ::std::string::String) -> Self {
        Self(value)
    }
}
impl ::std::fmt::Display for Graph3ScopeId {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        self.0.fmt(f)
    }
}
impl ::std::str::FromStr for Graph3ScopeId {
    type Err = ::std::convert::Infallible;
    fn from_str(value: &str) -> ::std::result::Result<Self, Self::Err> {
        Ok(Self(value.to_string()))
    }
}
///`Graph3StoredKind`
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
pub enum Graph3StoredKind {
    #[serde(rename = "file")]
    File,
    #[serde(rename = "symbol")]
    Symbol,
    #[serde(rename = "package")]
    Package,
}
impl ::std::fmt::Display for Graph3StoredKind {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::File => f.write_str("file"),
            Self::Symbol => f.write_str("symbol"),
            Self::Package => f.write_str("package"),
        }
    }
}
impl ::std::str::FromStr for Graph3StoredKind {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "file" => Ok(Self::File),
            "symbol" => Ok(Self::Symbol),
            "package" => Ok(Self::Package),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Graph3StoredKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Graph3StoredKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Graph traversal completion for the declared semantic depth. complete: no owed unexamined work remains within maxDepth (exactly-at-cap is complete when the queue is empty). truncated-page: this page is full and more result units exist in the produced selection; page fullness is not operation truncation. truncated-bound: a work bound stopped the logical operation and owed unexamined work remains. Not native CoverageResult.
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
pub enum Graph3TraversalCoverage {
    #[serde(rename = "complete")]
    Complete,
    #[serde(rename = "truncated-page")]
    TruncatedPage,
    #[serde(rename = "truncated-bound")]
    TruncatedBound,
}
impl ::std::fmt::Display for Graph3TraversalCoverage {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Complete => f.write_str("complete"),
            Self::TruncatedPage => f.write_str("truncated-page"),
            Self::TruncatedBound => f.write_str("truncated-bound"),
        }
    }
}
impl ::std::str::FromStr for Graph3TraversalCoverage {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "complete" => Ok(Self::Complete),
            "truncated-page" => Ok(Self::TruncatedPage),
            "truncated-bound" => Ok(Self::TruncatedBound),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Graph3TraversalCoverage {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Graph3TraversalCoverage {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Request selector. latest is an explicitly trusted host observation of current run identity; it is never derived from static Run bytes. snapshotId is joined to the admitted Run's snapshotId; a host index is not authority. Empty domain is IDENTITY.UNKNOWN with QUERY.VIEW_UNKNOWN. Two candidate Runs for one snapshot is QUERY.VIEW_AMBIGUOUS, not untyped IDENTITY.UNKNOWN-by-count.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
pub enum Graph3View {
    #[serde(rename = "runId")]
    RunId(Common3RunId),
    #[serde(rename = "snapshotId")]
    SnapshotId(Common3SnapshotId),
    ///a resolver, never an authority: graph responses must carry ResolvedView {runId}; empty domain is request-rejected
    #[serde(rename = "latest")]
    Latest(::serde_json::Value),
}
impl ::std::convert::From<Common3RunId> for Graph3View {
    fn from(value: Common3RunId) -> Self {
        Self::RunId(value)
    }
}
impl ::std::convert::From<Common3SnapshotId> for Graph3View {
    fn from(value: Common3SnapshotId) -> Self {
        Self::SnapshotId(value)
    }
}
impl ::std::convert::From<::serde_json::Value> for Graph3View {
    fn from(value: ::serde_json::Value) -> Self {
        Self::Latest(value)
    }
}
///Existing view2 identity of an admitted fact-view. Not a new FactViewId recipe.
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
#[serde(transparent)]
pub struct Graph3ViewDigest(pub ::std::string::String);
impl ::std::ops::Deref for Graph3ViewDigest {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Graph3ViewDigest> for ::std::string::String {
    fn from(value: Graph3ViewDigest) -> Self {
        value.0
    }
}
impl ::std::convert::From<::std::string::String> for Graph3ViewDigest {
    fn from(value: ::std::string::String) -> Self {
        Self(value)
    }
}
impl ::std::fmt::Display for Graph3ViewDigest {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        self.0.fmt(f)
    }
}
impl ::std::str::FromStr for Graph3ViewDigest {
    type Err = ::std::convert::Infallible;
    fn from_str(value: &str) -> ::std::result::Result<Self, Self::Err> {
        Ok(Self(value.to_string()))
    }
}
///`Graph4AdvisoryOperation`
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
pub enum Graph4AdvisoryOperation {
    #[serde(rename = "comparison.diff")]
    ComparisonDiff,
    #[serde(rename = "candidate.list")]
    CandidateList,
    #[serde(rename = "inspection.show")]
    InspectionShow,
    #[serde(rename = "review.brief")]
    ReviewBrief,
}
impl ::std::fmt::Display for Graph4AdvisoryOperation {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::ComparisonDiff => f.write_str("comparison.diff"),
            Self::CandidateList => f.write_str("candidate.list"),
            Self::InspectionShow => f.write_str("inspection.show"),
            Self::ReviewBrief => f.write_str("review.brief"),
        }
    }
}
impl ::std::str::FromStr for Graph4AdvisoryOperation {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "comparison.diff" => Ok(Self::ComparisonDiff),
            "candidate.list" => Ok(Self::CandidateList),
            "inspection.show" => Ok(Self::InspectionShow),
            "review.brief" => Ok(Self::ReviewBrief),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Graph4AdvisoryOperation {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Graph4AdvisoryOperation {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Graph4Bounds`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Graph4Bounds {
    #[serde(rename = "defaultPageSize")]
    pub default_page_size: ExactInteger,
    #[serde(rename = "maxItemsPerOperation")]
    pub max_items_per_operation: ExactInteger,
    #[serde(rename = "maxPageSize")]
    pub max_page_size: ExactInteger,
    #[serde(rename = "maxTraversalDepth")]
    pub max_traversal_depth: ExactInteger,
    #[serde(rename = "maxVisitedNodes")]
    pub max_visited_nodes: ExactInteger,
}
///Qualifies totalItems. exact: totalItems is the cardinality of the declared selection within semantic maxDepth. lower-bound: totalItems is a produced prefix, not a claimed universe cardinality. An empty nextCursor does not by itself make the count exact.
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
pub enum Graph4CountBasis {
    #[serde(rename = "exact")]
    Exact,
    #[serde(rename = "lower-bound")]
    LowerBound,
}
impl ::std::fmt::Display for Graph4CountBasis {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Exact => f.write_str("exact"),
            Self::LowerBound => f.write_str("lower-bound"),
        }
    }
}
impl ::std::str::FromStr for Graph4CountBasis {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "exact" => Ok(Self::Exact),
            "lower-bound" => Ok(Self::LowerBound),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Graph4CountBasis {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Graph4CountBasis {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Graph4FactId`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
#[serde(transparent)]
pub struct Graph4FactId(pub ::std::string::String);
impl ::std::ops::Deref for Graph4FactId {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Graph4FactId> for ::std::string::String {
    fn from(value: Graph4FactId) -> Self {
        value.0
    }
}
impl ::std::convert::From<::std::string::String> for Graph4FactId {
    fn from(value: ::std::string::String) -> Self {
        Self(value)
    }
}
impl ::std::fmt::Display for Graph4FactId {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        self.0.fmt(f)
    }
}
impl ::std::str::FromStr for Graph4FactId {
    type Err = ::std::convert::Infallible;
    fn from_str(value: &str) -> ::std::result::Result<Self, Self::Err> {
        Ok(Self(value.to_string()))
    }
}
///Explicit admitted view2 set. Omitted means all admitted views of the resolved Run whose scopes match relation@minResolution. Silent newest-provider is forbidden.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(transparent)]
pub struct Graph4FactViewDigests(pub ::std::vec::Vec<Graph4ViewDigest>);
impl ::std::ops::Deref for Graph4FactViewDigests {
    type Target = ::std::vec::Vec<Graph4ViewDigest>;
    fn deref(&self) -> &::std::vec::Vec<Graph4ViewDigest> {
        &self.0
    }
}
impl ::std::convert::From<Graph4FactViewDigests> for ::std::vec::Vec<Graph4ViewDigest> {
    fn from(value: Graph4FactViewDigests) -> Self {
        value.0
    }
}
impl ::std::convert::From<::std::vec::Vec<Graph4ViewDigest>> for Graph4FactViewDigests {
    fn from(value: ::std::vec::Vec<Graph4ViewDigest>) -> Self {
        Self(value)
    }
}
///`Graph4GraphDirection`
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
pub enum Graph4GraphDirection {
    #[serde(rename = "outgoing")]
    Outgoing,
    #[serde(rename = "incoming")]
    Incoming,
    #[serde(rename = "both")]
    Both,
}
impl ::std::fmt::Display for Graph4GraphDirection {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Outgoing => f.write_str("outgoing"),
            Self::Incoming => f.write_str("incoming"),
            Self::Both => f.write_str("both"),
        }
    }
}
impl ::std::str::FromStr for Graph4GraphDirection {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "outgoing" => Ok(Self::Outgoing),
            "incoming" => Ok(Self::Incoming),
            "both" => Ok(Self::Both),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Graph4GraphDirection {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Graph4GraphDirection {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Graph4GraphEndpoint`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Graph4GraphEndpoint {
    pub kind: Graph4StoredKind,
    #[serde(rename = "nativeSubjectId")]
    pub native_subject_id: Graph4NativeSubjectId,
    #[serde(
        rename = "packageManifestPath",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub package_manifest_path: FieldPresence<::std::option::Option<Common4LogicalPath>>,
    ///H-identity of the native semantic universe (fact sourceUniverse/targetUniverse). Required so two program universes with the same path cannot silently union.
    pub universe: Common4Sha256Hex,
}
///Mandatory Q3 disclosure for graph.*. Cites existing native Coverage, scopes, evaluation deficiencies and resolution limitations. Does not mint negative proof or run a parallel absence evaluator.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Graph4GraphEvidenceDisclosure {
    #[serde(rename = "coverageIds")]
    pub coverage_ids: ::std::vec::Vec<Common4CoverageId>,
    #[serde(rename = "deficiencyCitations")]
    pub deficiency_citations: ::std::vec::Vec<
        Graph4GraphEvidenceDisclosureDeficiencyCitationsItem,
    >,
    #[serde(rename = "resolutionLimitations")]
    pub resolution_limitations: ::std::vec::Vec<
        Graph4GraphEvidenceDisclosureResolutionLimitationsItem,
    >,
    #[serde(rename = "scopeIds")]
    pub scope_ids: ::std::vec::Vec<Graph4ScopeId>,
}
///`Graph4GraphEvidenceDisclosureDeficiencyCitationsItem`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Graph4GraphEvidenceDisclosureDeficiencyCitationsItem {
    pub cause: Graph4GraphEvidenceDisclosureDeficiencyCitationsItemCause,
    #[serde(
        rename = "coverageId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub coverage_id: FieldPresence<::std::option::Option<Common4CoverageId>>,
    #[serde(rename = "inputRefs")]
    pub input_refs: ::std::vec::Vec<
        Graph4GraphEvidenceDisclosureDeficiencyCitationsItemInputRefsItem,
    >,
    #[serde(
        rename = "nativeCause",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub native_cause: FieldPresence<
        ::std::option::Option<
            Graph4GraphEvidenceDisclosureDeficiencyCitationsItemNativeCause,
        >,
    >,
    #[serde(
        rename = "predicateId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub predicate_id: FieldPresence<
        ::std::option::Option<
            Graph4GraphEvidenceDisclosureDeficiencyCitationsItemPredicateId,
        >,
    >,
    pub source: Graph4GraphEvidenceDisclosureDeficiencyCitationsItemSource,
    #[serde(
        rename = "subjectId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub subject_id: FieldPresence<::std::option::Option<Common4SubjectId>>,
}
///`Graph4GraphEvidenceDisclosureDeficiencyCitationsItemCause`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Graph4GraphEvidenceDisclosureDeficiencyCitationsItemCause(
    ::std::string::String,
);
impl ::std::ops::Deref for Graph4GraphEvidenceDisclosureDeficiencyCitationsItemCause {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Graph4GraphEvidenceDisclosureDeficiencyCitationsItemCause>
for ::std::string::String {
    fn from(value: Graph4GraphEvidenceDisclosureDeficiencyCitationsItemCause) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Graph4GraphEvidenceDisclosureDeficiencyCitationsItemCause {
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
impl ::std::convert::TryFrom<&str>
for Graph4GraphEvidenceDisclosureDeficiencyCitationsItemCause {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Graph4GraphEvidenceDisclosureDeficiencyCitationsItemCause {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de>
for Graph4GraphEvidenceDisclosureDeficiencyCitationsItemCause {
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
///`Graph4GraphEvidenceDisclosureDeficiencyCitationsItemInputRefsItem`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Graph4GraphEvidenceDisclosureDeficiencyCitationsItemInputRefsItem {
    pub digest: Common4Sha256Hex,
    pub domain: Graph4GraphEvidenceDisclosureDeficiencyCitationsItemInputRefsItemDomain,
}
///`Graph4GraphEvidenceDisclosureDeficiencyCitationsItemInputRefsItemDomain`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Graph4GraphEvidenceDisclosureDeficiencyCitationsItemInputRefsItemDomain(
    ::std::string::String,
);
impl ::std::ops::Deref
for Graph4GraphEvidenceDisclosureDeficiencyCitationsItemInputRefsItemDomain {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<
    Graph4GraphEvidenceDisclosureDeficiencyCitationsItemInputRefsItemDomain,
> for ::std::string::String {
    fn from(
        value: Graph4GraphEvidenceDisclosureDeficiencyCitationsItemInputRefsItemDomain,
    ) -> Self {
        value.0
    }
}
impl ::std::str::FromStr
for Graph4GraphEvidenceDisclosureDeficiencyCitationsItemInputRefsItemDomain {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 64usize {
            return Err("longer than 64 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str>
for Graph4GraphEvidenceDisclosureDeficiencyCitationsItemInputRefsItemDomain {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Graph4GraphEvidenceDisclosureDeficiencyCitationsItemInputRefsItemDomain {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de>
for Graph4GraphEvidenceDisclosureDeficiencyCitationsItemInputRefsItemDomain {
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
///`Graph4GraphEvidenceDisclosureDeficiencyCitationsItemNativeCause`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Graph4GraphEvidenceDisclosureDeficiencyCitationsItemNativeCause(
    ::std::string::String,
);
impl ::std::ops::Deref
for Graph4GraphEvidenceDisclosureDeficiencyCitationsItemNativeCause {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<
    Graph4GraphEvidenceDisclosureDeficiencyCitationsItemNativeCause,
> for ::std::string::String {
    fn from(
        value: Graph4GraphEvidenceDisclosureDeficiencyCitationsItemNativeCause,
    ) -> Self {
        value.0
    }
}
impl ::std::str::FromStr
for Graph4GraphEvidenceDisclosureDeficiencyCitationsItemNativeCause {
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
impl ::std::convert::TryFrom<&str>
for Graph4GraphEvidenceDisclosureDeficiencyCitationsItemNativeCause {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Graph4GraphEvidenceDisclosureDeficiencyCitationsItemNativeCause {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de>
for Graph4GraphEvidenceDisclosureDeficiencyCitationsItemNativeCause {
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
///`Graph4GraphEvidenceDisclosureDeficiencyCitationsItemPredicateId`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Graph4GraphEvidenceDisclosureDeficiencyCitationsItemPredicateId(
    ::std::string::String,
);
impl ::std::ops::Deref
for Graph4GraphEvidenceDisclosureDeficiencyCitationsItemPredicateId {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<
    Graph4GraphEvidenceDisclosureDeficiencyCitationsItemPredicateId,
> for ::std::string::String {
    fn from(
        value: Graph4GraphEvidenceDisclosureDeficiencyCitationsItemPredicateId,
    ) -> Self {
        value.0
    }
}
impl ::std::str::FromStr
for Graph4GraphEvidenceDisclosureDeficiencyCitationsItemPredicateId {
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
impl ::std::convert::TryFrom<&str>
for Graph4GraphEvidenceDisclosureDeficiencyCitationsItemPredicateId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Graph4GraphEvidenceDisclosureDeficiencyCitationsItemPredicateId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de>
for Graph4GraphEvidenceDisclosureDeficiencyCitationsItemPredicateId {
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
///`Graph4GraphEvidenceDisclosureDeficiencyCitationsItemSource`
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
pub enum Graph4GraphEvidenceDisclosureDeficiencyCitationsItemSource {
    #[serde(rename = "enumeration")]
    Enumeration,
    #[serde(rename = "native")]
    Native,
    #[serde(rename = "import")]
    Import,
    #[serde(rename = "execution")]
    Execution,
    #[serde(rename = "correspondence")]
    Correspondence,
}
impl ::std::fmt::Display for Graph4GraphEvidenceDisclosureDeficiencyCitationsItemSource {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Enumeration => f.write_str("enumeration"),
            Self::Native => f.write_str("native"),
            Self::Import => f.write_str("import"),
            Self::Execution => f.write_str("execution"),
            Self::Correspondence => f.write_str("correspondence"),
        }
    }
}
impl ::std::str::FromStr for Graph4GraphEvidenceDisclosureDeficiencyCitationsItemSource {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "enumeration" => Ok(Self::Enumeration),
            "native" => Ok(Self::Native),
            "import" => Ok(Self::Import),
            "execution" => Ok(Self::Execution),
            "correspondence" => Ok(Self::Correspondence),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str>
for Graph4GraphEvidenceDisclosureDeficiencyCitationsItemSource {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Graph4GraphEvidenceDisclosureDeficiencyCitationsItemSource {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Graph4GraphEvidenceDisclosurePropertiesResolutionLimitationsItemsPropertiesKind`
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
pub enum Graph4GraphEvidenceDisclosurePropertiesResolutionLimitationsItemsPropertiesKind {
    #[serde(rename = "unexamined-work-bound")]
    UnexaminedWorkBound,
    #[serde(rename = "unprojectable-fact")]
    UnprojectableFact,
    #[serde(rename = "resolution-incomplete")]
    ResolutionIncomplete,
    #[serde(rename = "resolution-partial")]
    ResolutionPartial,
    #[serde(rename = "resolution-not-attempted")]
    ResolutionNotAttempted,
    #[serde(rename = "coverage-unknown")]
    CoverageUnknown,
    #[serde(rename = "coverage-partial")]
    CoveragePartial,
    #[serde(rename = "unresolved-edge-present")]
    UnresolvedEdgePresent,
    #[serde(rename = "examined-not-exhaustive")]
    ExaminedNotExhaustive,
    #[serde(rename = "unsupported-rung-omitted")]
    UnsupportedRungOmitted,
    #[serde(rename = "incoming-search-incomplete")]
    IncomingSearchIncomplete,
    #[serde(rename = "native-evidence-unavailable")]
    NativeEvidenceUnavailable,
}
impl ::std::fmt::Display
for Graph4GraphEvidenceDisclosurePropertiesResolutionLimitationsItemsPropertiesKind {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::UnexaminedWorkBound => f.write_str("unexamined-work-bound"),
            Self::UnprojectableFact => f.write_str("unprojectable-fact"),
            Self::ResolutionIncomplete => f.write_str("resolution-incomplete"),
            Self::ResolutionPartial => f.write_str("resolution-partial"),
            Self::ResolutionNotAttempted => f.write_str("resolution-not-attempted"),
            Self::CoverageUnknown => f.write_str("coverage-unknown"),
            Self::CoveragePartial => f.write_str("coverage-partial"),
            Self::UnresolvedEdgePresent => f.write_str("unresolved-edge-present"),
            Self::ExaminedNotExhaustive => f.write_str("examined-not-exhaustive"),
            Self::UnsupportedRungOmitted => f.write_str("unsupported-rung-omitted"),
            Self::IncomingSearchIncomplete => f.write_str("incoming-search-incomplete"),
            Self::NativeEvidenceUnavailable => f.write_str("native-evidence-unavailable"),
        }
    }
}
impl ::std::str::FromStr
for Graph4GraphEvidenceDisclosurePropertiesResolutionLimitationsItemsPropertiesKind {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "unexamined-work-bound" => Ok(Self::UnexaminedWorkBound),
            "unprojectable-fact" => Ok(Self::UnprojectableFact),
            "resolution-incomplete" => Ok(Self::ResolutionIncomplete),
            "resolution-partial" => Ok(Self::ResolutionPartial),
            "resolution-not-attempted" => Ok(Self::ResolutionNotAttempted),
            "coverage-unknown" => Ok(Self::CoverageUnknown),
            "coverage-partial" => Ok(Self::CoveragePartial),
            "unresolved-edge-present" => Ok(Self::UnresolvedEdgePresent),
            "examined-not-exhaustive" => Ok(Self::ExaminedNotExhaustive),
            "unsupported-rung-omitted" => Ok(Self::UnsupportedRungOmitted),
            "incoming-search-incomplete" => Ok(Self::IncomingSearchIncomplete),
            "native-evidence-unavailable" => Ok(Self::NativeEvidenceUnavailable),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str>
for Graph4GraphEvidenceDisclosurePropertiesResolutionLimitationsItemsPropertiesKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Graph4GraphEvidenceDisclosurePropertiesResolutionLimitationsItemsPropertiesKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Graph4GraphEvidenceDisclosureResolutionLimitationsItem`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Graph4GraphEvidenceDisclosureResolutionLimitationsItem {
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub attempted: FieldPresence<::std::option::Option<bool>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub coverage: FieldPresence<
        ::std::option::Option<
            Graph4GraphEvidenceDisclosureResolutionLimitationsItemCoverage,
        >,
    >,
    #[serde(
        rename = "coverageId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub coverage_id: FieldPresence<::std::option::Option<Common4CoverageId>>,
    #[serde(
        rename = "examinedExhaustive",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub examined_exhaustive: FieldPresence<::std::option::Option<bool>>,
    #[serde(
        rename = "factId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub fact_id: FieldPresence<::std::option::Option<Graph4FactId>>,
    #[serde(
        rename = "incomingSearchDigest",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub incoming_search_digest: FieldPresence<::std::option::Option<Common4Sha256Hex>>,
    pub kind: Graph4GraphEvidenceDisclosureResolutionLimitationsItemKind,
    #[serde(
        rename = "minResolution",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub min_resolution: FieldPresence<::std::option::Option<Common4CanonicalIdentifier>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub note: FieldPresence<::std::option::Option<Common4BoundedText>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub relation: FieldPresence<::std::option::Option<Common4CanonicalIdentifier>>,
    #[serde(
        rename = "resolutionState",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub resolution_state: FieldPresence<
        ::std::option::Option<
            Graph4GraphEvidenceDisclosureResolutionLimitationsItemResolutionState,
        >,
    >,
    #[serde(
        rename = "unresolvedEdgeCount",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub unresolved_edge_count: FieldPresence<::std::option::Option<Common4Uint53>>,
}
///`Graph4GraphEvidenceDisclosureResolutionLimitationsItemCoverage`
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
pub enum Graph4GraphEvidenceDisclosureResolutionLimitationsItemCoverage {
    #[serde(rename = "complete")]
    Complete,
    #[serde(rename = "partial")]
    Partial,
    #[serde(rename = "unknown")]
    Unknown,
}
impl ::std::fmt::Display
for Graph4GraphEvidenceDisclosureResolutionLimitationsItemCoverage {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Complete => f.write_str("complete"),
            Self::Partial => f.write_str("partial"),
            Self::Unknown => f.write_str("unknown"),
        }
    }
}
impl ::std::str::FromStr
for Graph4GraphEvidenceDisclosureResolutionLimitationsItemCoverage {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "complete" => Ok(Self::Complete),
            "partial" => Ok(Self::Partial),
            "unknown" => Ok(Self::Unknown),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str>
for Graph4GraphEvidenceDisclosureResolutionLimitationsItemCoverage {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Graph4GraphEvidenceDisclosureResolutionLimitationsItemCoverage {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Graph4GraphEvidenceDisclosureResolutionLimitationsItemKind`
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
pub enum Graph4GraphEvidenceDisclosureResolutionLimitationsItemKind {
    #[serde(rename = "unexamined-work-bound")]
    UnexaminedWorkBound,
    #[serde(rename = "unprojectable-fact")]
    UnprojectableFact,
    #[serde(rename = "resolution-incomplete")]
    ResolutionIncomplete,
    #[serde(rename = "resolution-partial")]
    ResolutionPartial,
    #[serde(rename = "resolution-not-attempted")]
    ResolutionNotAttempted,
    #[serde(rename = "coverage-unknown")]
    CoverageUnknown,
    #[serde(rename = "coverage-partial")]
    CoveragePartial,
    #[serde(rename = "unresolved-edge-present")]
    UnresolvedEdgePresent,
    #[serde(rename = "examined-not-exhaustive")]
    ExaminedNotExhaustive,
    #[serde(rename = "unsupported-rung-omitted")]
    UnsupportedRungOmitted,
    #[serde(rename = "incoming-search-incomplete")]
    IncomingSearchIncomplete,
    #[serde(rename = "native-evidence-unavailable")]
    NativeEvidenceUnavailable,
}
impl ::std::fmt::Display for Graph4GraphEvidenceDisclosureResolutionLimitationsItemKind {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::UnexaminedWorkBound => f.write_str("unexamined-work-bound"),
            Self::UnprojectableFact => f.write_str("unprojectable-fact"),
            Self::ResolutionIncomplete => f.write_str("resolution-incomplete"),
            Self::ResolutionPartial => f.write_str("resolution-partial"),
            Self::ResolutionNotAttempted => f.write_str("resolution-not-attempted"),
            Self::CoverageUnknown => f.write_str("coverage-unknown"),
            Self::CoveragePartial => f.write_str("coverage-partial"),
            Self::UnresolvedEdgePresent => f.write_str("unresolved-edge-present"),
            Self::ExaminedNotExhaustive => f.write_str("examined-not-exhaustive"),
            Self::UnsupportedRungOmitted => f.write_str("unsupported-rung-omitted"),
            Self::IncomingSearchIncomplete => f.write_str("incoming-search-incomplete"),
            Self::NativeEvidenceUnavailable => f.write_str("native-evidence-unavailable"),
        }
    }
}
impl ::std::str::FromStr for Graph4GraphEvidenceDisclosureResolutionLimitationsItemKind {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "unexamined-work-bound" => Ok(Self::UnexaminedWorkBound),
            "unprojectable-fact" => Ok(Self::UnprojectableFact),
            "resolution-incomplete" => Ok(Self::ResolutionIncomplete),
            "resolution-partial" => Ok(Self::ResolutionPartial),
            "resolution-not-attempted" => Ok(Self::ResolutionNotAttempted),
            "coverage-unknown" => Ok(Self::CoverageUnknown),
            "coverage-partial" => Ok(Self::CoveragePartial),
            "unresolved-edge-present" => Ok(Self::UnresolvedEdgePresent),
            "examined-not-exhaustive" => Ok(Self::ExaminedNotExhaustive),
            "unsupported-rung-omitted" => Ok(Self::UnsupportedRungOmitted),
            "incoming-search-incomplete" => Ok(Self::IncomingSearchIncomplete),
            "native-evidence-unavailable" => Ok(Self::NativeEvidenceUnavailable),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str>
for Graph4GraphEvidenceDisclosureResolutionLimitationsItemKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Graph4GraphEvidenceDisclosureResolutionLimitationsItemKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Graph4GraphEvidenceDisclosureResolutionLimitationsItemResolutionState`
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
pub enum Graph4GraphEvidenceDisclosureResolutionLimitationsItemResolutionState {
    #[serde(rename = "not-attempted")]
    NotAttempted,
    #[serde(rename = "partial")]
    Partial,
    #[serde(rename = "complete")]
    Complete,
    #[serde(rename = "not-applicable")]
    NotApplicable,
    #[serde(rename = "incomplete")]
    Incomplete,
}
impl ::std::fmt::Display
for Graph4GraphEvidenceDisclosureResolutionLimitationsItemResolutionState {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::NotAttempted => f.write_str("not-attempted"),
            Self::Partial => f.write_str("partial"),
            Self::Complete => f.write_str("complete"),
            Self::NotApplicable => f.write_str("not-applicable"),
            Self::Incomplete => f.write_str("incomplete"),
        }
    }
}
impl ::std::str::FromStr
for Graph4GraphEvidenceDisclosureResolutionLimitationsItemResolutionState {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "not-attempted" => Ok(Self::NotAttempted),
            "partial" => Ok(Self::Partial),
            "complete" => Ok(Self::Complete),
            "not-applicable" => Ok(Self::NotApplicable),
            "incomplete" => Ok(Self::Incomplete),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str>
for Graph4GraphEvidenceDisclosureResolutionLimitationsItemResolutionState {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Graph4GraphEvidenceDisclosureResolutionLimitationsItemResolutionState {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Graph4GraphNeighborRow`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Graph4GraphNeighborRow {
    #[serde(
        rename = "confidenceMillionths",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub confidence_millionths: FieldPresence<::std::option::Option<Common4Uint53>>,
    #[serde(rename = "factId")]
    pub fact_id: Graph4FactId,
    #[serde(
        rename = "producerClosure",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub producer_closure: FieldPresence<::std::option::Option<Common4ClosureId>>,
    pub relation: Common4CanonicalIdentifier,
    pub resolution: Common4CanonicalIdentifier,
    pub source: Graph4GraphEndpoint,
    pub target: Graph4GraphEndpoint,
}
///`Graph4GraphNeighborsParams`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Graph4GraphNeighborsParams {
    pub direction: Graph4GraphDirection,
    pub endpoint: Graph4GraphEndpoint,
    #[serde(
        rename = "factViewDigests",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub fact_view_digests: FieldPresence<::std::option::Option<Graph4FactViewDigests>>,
    #[serde(rename = "minResolution")]
    pub min_resolution: Common4CanonicalIdentifier,
    pub relation: Common4CanonicalIdentifier,
}
///`Graph4GraphOperation`
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
pub enum Graph4GraphOperation {
    #[serde(rename = "graph.neighbors")]
    GraphNeighbors,
    #[serde(rename = "graph.path")]
    GraphPath,
    #[serde(rename = "graph.reach")]
    GraphReach,
}
impl ::std::fmt::Display for Graph4GraphOperation {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::GraphNeighbors => f.write_str("graph.neighbors"),
            Self::GraphPath => f.write_str("graph.path"),
            Self::GraphReach => f.write_str("graph.reach"),
        }
    }
}
impl ::std::str::FromStr for Graph4GraphOperation {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "graph.neighbors" => Ok(Self::GraphNeighbors),
            "graph.path" => Ok(Self::GraphPath),
            "graph.reach" => Ok(Self::GraphReach),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Graph4GraphOperation {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Graph4GraphOperation {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Mandatory graph.* response context. resolvedView is run3 only. traversalCoverage is not native CoverageResult. totalItems is qualified by countBasis. evidence is required. advisory is const false.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Graph4GraphOperationResponseContext {
    pub advisory: ::serde_json::Value,
    pub availability: Graph4GraphOperationResponseContextAvailability,
    #[serde(rename = "countBasis")]
    pub count_basis: Graph4CountBasis,
    pub evidence: Graph4GraphEvidenceDisclosure,
    #[serde(rename = "factViewDigests")]
    pub fact_view_digests: ::std::vec::Vec<Graph4ViewDigest>,
    #[serde(
        rename = "nextCursor",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub next_cursor: FieldPresence<
        ::std::option::Option<Graph4GraphOperationResponseContextNextCursor>,
    >,
    #[serde(rename = "producedItems")]
    pub produced_items: Common4Uint53,
    #[serde(rename = "projectId")]
    pub project_id: Common4ProjectId,
    #[serde(rename = "resolvedView")]
    pub resolved_view: Graph4ResolvedView,
    #[serde(rename = "totalItems")]
    pub total_items: Common4Uint53,
    #[serde(rename = "traversalCoverage")]
    pub traversal_coverage: Graph4TraversalCoverage,
    ///true iff traversalCoverage is truncated-bound (operation-level). Full page is not truncated.
    pub truncated: bool,
    #[serde(rename = "visitedNodes")]
    pub visited_nodes: Common4Uint53,
}
///`Graph4GraphOperationResponseContextAvailability`
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
pub enum Graph4GraphOperationResponseContextAvailability {
    #[serde(rename = "retained")]
    Retained,
    #[serde(rename = "partial")]
    Partial,
    #[serde(rename = "expired")]
    Expired,
    #[serde(rename = "purged")]
    Purged,
    #[serde(rename = "corrupt")]
    Corrupt,
    #[serde(rename = "unavailable")]
    Unavailable,
}
impl ::std::fmt::Display for Graph4GraphOperationResponseContextAvailability {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Retained => f.write_str("retained"),
            Self::Partial => f.write_str("partial"),
            Self::Expired => f.write_str("expired"),
            Self::Purged => f.write_str("purged"),
            Self::Corrupt => f.write_str("corrupt"),
            Self::Unavailable => f.write_str("unavailable"),
        }
    }
}
impl ::std::str::FromStr for Graph4GraphOperationResponseContextAvailability {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "retained" => Ok(Self::Retained),
            "partial" => Ok(Self::Partial),
            "expired" => Ok(Self::Expired),
            "purged" => Ok(Self::Purged),
            "corrupt" => Ok(Self::Corrupt),
            "unavailable" => Ok(Self::Unavailable),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Graph4GraphOperationResponseContextAvailability {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Graph4GraphOperationResponseContextAvailability {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Graph4GraphOperationResponseContextNextCursor`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Graph4GraphOperationResponseContextNextCursor(::std::string::String);
impl ::std::ops::Deref for Graph4GraphOperationResponseContextNextCursor {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Graph4GraphOperationResponseContextNextCursor>
for ::std::string::String {
    fn from(value: Graph4GraphOperationResponseContextNextCursor) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Graph4GraphOperationResponseContextNextCursor {
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
impl ::std::convert::TryFrom<&str> for Graph4GraphOperationResponseContextNextCursor {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Graph4GraphOperationResponseContextNextCursor {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Graph4GraphOperationResponseContextNextCursor {
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
///`Graph4GraphPathEdge`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Graph4GraphPathEdge {
    #[serde(rename = "factId")]
    pub fact_id: Graph4FactId,
    pub source: Graph4GraphEndpoint,
    pub target: Graph4GraphEndpoint,
}
///`Graph4GraphPathParams`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Graph4GraphPathParams {
    pub direction: Graph4GraphDirection,
    #[serde(
        rename = "factViewDigests",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub fact_view_digests: FieldPresence<::std::option::Option<Graph4FactViewDigests>>,
    ///Semantic hop bound (GX-01), not a free work cutoff. Required completion means complete within this declared depth.
    #[serde(rename = "maxDepth")]
    pub max_depth: ::std::num::NonZeroU64,
    #[serde(rename = "minResolution")]
    pub min_resolution: Common4CanonicalIdentifier,
    pub relation: Common4CanonicalIdentifier,
    pub start: Graph4GraphEndpoint,
    pub target: Graph4GraphEndpoint,
}
///One simple path. start==target yields hopCount 0, nodes [start], edges []. Otherwise shortest hop count with canonical fact2-id-sequence tie-break. No optional closing cycle.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Graph4GraphPathRow {
    pub edges: ::std::vec::Vec<Graph4GraphPathEdge>,
    #[serde(rename = "hopCount")]
    pub hop_count: Common4Uint53,
    pub nodes: ::std::vec::Vec<Graph4GraphEndpoint>,
    pub start: Graph4GraphEndpoint,
    pub target: Graph4GraphEndpoint,
}
///`Graph4GraphQueryRequestV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Graph4GraphQueryRequestV1 {
    pub completeness: Graph4GraphQueryRequestV1Completeness,
    #[serde(
        rename = "fieldSelection",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub field_selection: FieldPresence<
        ::std::option::Option<::std::vec::Vec<Common4CanonicalIdentifier>>,
    >,
    pub operation: Graph4Operation,
    pub page: Graph4Page,
    ///Closed per operation by the allOf joins below. Graph ops use GraphNeighborsParams/GraphPathParams/GraphReachParams. Other 17 operations keep Params.
    pub params: ::serde_json::Map<::std::string::String, ::serde_json::Value>,
    #[serde(rename = "projectId")]
    pub project_id: Common4ProjectId,
    #[serde(rename = "schemaFamily")]
    pub schema_family: ::serde_json::Value,
    #[serde(rename = "schemaMajor")]
    pub schema_major: ExactInteger,
    pub view: Graph4View,
}
///`Graph4GraphQueryRequestV1Completeness`
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
pub enum Graph4GraphQueryRequestV1Completeness {
    #[serde(rename = "required")]
    Required,
    #[serde(rename = "best-effort")]
    BestEffort,
}
impl ::std::fmt::Display for Graph4GraphQueryRequestV1Completeness {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Required => f.write_str("required"),
            Self::BestEffort => f.write_str("best-effort"),
        }
    }
}
impl ::std::str::FromStr for Graph4GraphQueryRequestV1Completeness {
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
impl ::std::convert::TryFrom<&str> for Graph4GraphQueryRequestV1Completeness {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Graph4GraphQueryRequestV1Completeness {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Response context for the 17 non-graph operations. resolvedView remains request View so snapshot metadata operations are not forced to run-only. Graph operations MUST use GraphOperationResponseContext instead.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Graph4GraphQueryResponseContext {
    ///true exactly for AdvisoryOperation members
    pub advisory: bool,
    pub availability: Graph4GraphQueryResponseContextAvailability,
    pub coverage: Graph4GraphQueryResponseContextCoverage,
    #[serde(
        rename = "nextCursor",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub next_cursor: FieldPresence<
        ::std::option::Option<Graph4GraphQueryResponseContextNextCursor>,
    >,
    #[serde(rename = "projectId")]
    pub project_id: Common4ProjectId,
    #[serde(rename = "resolvedView")]
    pub resolved_view: Graph4View,
    #[serde(rename = "totalItems")]
    pub total_items: Common4Uint53,
    pub truncated: bool,
}
///`Graph4GraphQueryResponseContextAvailability`
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
pub enum Graph4GraphQueryResponseContextAvailability {
    #[serde(rename = "retained")]
    Retained,
    #[serde(rename = "partial")]
    Partial,
    #[serde(rename = "expired")]
    Expired,
    #[serde(rename = "purged")]
    Purged,
    #[serde(rename = "corrupt")]
    Corrupt,
    #[serde(rename = "unavailable")]
    Unavailable,
}
impl ::std::fmt::Display for Graph4GraphQueryResponseContextAvailability {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Retained => f.write_str("retained"),
            Self::Partial => f.write_str("partial"),
            Self::Expired => f.write_str("expired"),
            Self::Purged => f.write_str("purged"),
            Self::Corrupt => f.write_str("corrupt"),
            Self::Unavailable => f.write_str("unavailable"),
        }
    }
}
impl ::std::str::FromStr for Graph4GraphQueryResponseContextAvailability {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "retained" => Ok(Self::Retained),
            "partial" => Ok(Self::Partial),
            "expired" => Ok(Self::Expired),
            "purged" => Ok(Self::Purged),
            "corrupt" => Ok(Self::Corrupt),
            "unavailable" => Ok(Self::Unavailable),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Graph4GraphQueryResponseContextAvailability {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Graph4GraphQueryResponseContextAvailability {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Graph4GraphQueryResponseContextCoverage`
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
pub enum Graph4GraphQueryResponseContextCoverage {
    #[serde(rename = "complete")]
    Complete,
    #[serde(rename = "partial")]
    Partial,
    #[serde(rename = "unavailable")]
    Unavailable,
}
impl ::std::fmt::Display for Graph4GraphQueryResponseContextCoverage {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Complete => f.write_str("complete"),
            Self::Partial => f.write_str("partial"),
            Self::Unavailable => f.write_str("unavailable"),
        }
    }
}
impl ::std::str::FromStr for Graph4GraphQueryResponseContextCoverage {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "complete" => Ok(Self::Complete),
            "partial" => Ok(Self::Partial),
            "unavailable" => Ok(Self::Unavailable),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Graph4GraphQueryResponseContextCoverage {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Graph4GraphQueryResponseContextCoverage {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Graph4GraphQueryResponseContextNextCursor`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Graph4GraphQueryResponseContextNextCursor(::std::string::String);
impl ::std::ops::Deref for Graph4GraphQueryResponseContextNextCursor {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Graph4GraphQueryResponseContextNextCursor>
for ::std::string::String {
    fn from(value: Graph4GraphQueryResponseContextNextCursor) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Graph4GraphQueryResponseContextNextCursor {
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
impl ::std::convert::TryFrom<&str> for Graph4GraphQueryResponseContextNextCursor {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Graph4GraphQueryResponseContextNextCursor {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Graph4GraphQueryResponseContextNextCursor {
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
///`Graph4GraphQueryResponseV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Graph4GraphQueryResponseV1 {
    pub context: ::serde_json::Map<::std::string::String, ::serde_json::Value>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub items: FieldPresence<::std::vec::Vec<::serde_json::Value>>,
    pub operation: Graph4Operation,
    #[serde(rename = "schemaFamily")]
    pub schema_family: ::serde_json::Value,
    #[serde(rename = "schemaMajor")]
    pub schema_major: ExactInteger,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub termination: FieldPresence<::std::option::Option<Common4StepTermination>>,
}
///`Graph4GraphReachParams`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Graph4GraphReachParams {
    pub direction: Graph4GraphDirection,
    #[serde(
        rename = "factViewDigests",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub fact_view_digests: FieldPresence<::std::option::Option<Graph4FactViewDigests>>,
    ///Closed reach field. Admission default false when omitted. Start is excluded unless true. Not an optional closing cycle.
    #[serde(
        rename = "includeStart",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub include_start: FieldPresence<::std::option::Option<bool>>,
    ///Semantic hop bound (GX-01).
    #[serde(rename = "maxDepth")]
    pub max_depth: ::std::num::NonZeroU64,
    #[serde(rename = "minResolution")]
    pub min_resolution: Common4CanonicalIdentifier,
    pub relation: Common4CanonicalIdentifier,
    pub start: Graph4GraphEndpoint,
}
///`Graph4GraphReachRow`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Graph4GraphReachRow {
    pub depth: Common4Uint53,
    pub endpoint: Graph4GraphEndpoint,
    ///Fact that first reached this endpoint on the canonical walk. Omitted for the start row when includeStart is true.
    #[serde(
        rename = "viaFactId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub via_fact_id: FieldPresence<::std::option::Option<Graph4FactId>>,
}
///Native evaluation-subject id as stored on inventory/fact payload. Not a backend numeric id.
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Graph4NativeSubjectId(::std::string::String);
impl ::std::ops::Deref for Graph4NativeSubjectId {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Graph4NativeSubjectId> for ::std::string::String {
    fn from(value: Graph4NativeSubjectId) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Graph4NativeSubjectId {
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
impl ::std::convert::TryFrom<&str> for Graph4NativeSubjectId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Graph4NativeSubjectId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Graph4NativeSubjectId {
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
///`Graph4Operation`
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
pub enum Graph4Operation {
    #[serde(rename = "run.show")]
    RunShow,
    #[serde(rename = "run.list")]
    RunList,
    #[serde(rename = "finding.list")]
    FindingList,
    #[serde(rename = "finding.show")]
    FindingShow,
    #[serde(rename = "fact.list")]
    FactList,
    #[serde(rename = "coverage.show")]
    CoverageShow,
    #[serde(rename = "artifact.get")]
    ArtifactGet,
    #[serde(rename = "graph.neighbors")]
    GraphNeighbors,
    #[serde(rename = "graph.path")]
    GraphPath,
    #[serde(rename = "graph.reach")]
    GraphReach,
    #[serde(rename = "baseline.show")]
    BaselineShow,
    #[serde(rename = "comparison.show")]
    ComparisonShow,
    #[serde(rename = "comparison.diff")]
    ComparisonDiff,
    #[serde(rename = "candidate.list")]
    CandidateList,
    #[serde(rename = "inspection.show")]
    InspectionShow,
    #[serde(rename = "review.brief")]
    ReviewBrief,
    #[serde(rename = "policy.effective")]
    PolicyEffective,
    #[serde(rename = "import.show")]
    ImportShow,
    #[serde(rename = "receipt.show")]
    ReceiptShow,
    #[serde(rename = "availability.show")]
    AvailabilityShow,
}
impl ::std::fmt::Display for Graph4Operation {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::RunShow => f.write_str("run.show"),
            Self::RunList => f.write_str("run.list"),
            Self::FindingList => f.write_str("finding.list"),
            Self::FindingShow => f.write_str("finding.show"),
            Self::FactList => f.write_str("fact.list"),
            Self::CoverageShow => f.write_str("coverage.show"),
            Self::ArtifactGet => f.write_str("artifact.get"),
            Self::GraphNeighbors => f.write_str("graph.neighbors"),
            Self::GraphPath => f.write_str("graph.path"),
            Self::GraphReach => f.write_str("graph.reach"),
            Self::BaselineShow => f.write_str("baseline.show"),
            Self::ComparisonShow => f.write_str("comparison.show"),
            Self::ComparisonDiff => f.write_str("comparison.diff"),
            Self::CandidateList => f.write_str("candidate.list"),
            Self::InspectionShow => f.write_str("inspection.show"),
            Self::ReviewBrief => f.write_str("review.brief"),
            Self::PolicyEffective => f.write_str("policy.effective"),
            Self::ImportShow => f.write_str("import.show"),
            Self::ReceiptShow => f.write_str("receipt.show"),
            Self::AvailabilityShow => f.write_str("availability.show"),
        }
    }
}
impl ::std::str::FromStr for Graph4Operation {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "run.show" => Ok(Self::RunShow),
            "run.list" => Ok(Self::RunList),
            "finding.list" => Ok(Self::FindingList),
            "finding.show" => Ok(Self::FindingShow),
            "fact.list" => Ok(Self::FactList),
            "coverage.show" => Ok(Self::CoverageShow),
            "artifact.get" => Ok(Self::ArtifactGet),
            "graph.neighbors" => Ok(Self::GraphNeighbors),
            "graph.path" => Ok(Self::GraphPath),
            "graph.reach" => Ok(Self::GraphReach),
            "baseline.show" => Ok(Self::BaselineShow),
            "comparison.show" => Ok(Self::ComparisonShow),
            "comparison.diff" => Ok(Self::ComparisonDiff),
            "candidate.list" => Ok(Self::CandidateList),
            "inspection.show" => Ok(Self::InspectionShow),
            "review.brief" => Ok(Self::ReviewBrief),
            "policy.effective" => Ok(Self::PolicyEffective),
            "import.show" => Ok(Self::ImportShow),
            "receipt.show" => Ok(Self::ReceiptShow),
            "availability.show" => Ok(Self::AvailabilityShow),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Graph4Operation {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Graph4Operation {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Graph4Page`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Graph4Page {
    ///Opaque host token bound to projectId+runId+factViewDigests+operation+effective params/order+page position. Continuation never re-resolves latest. Reference form q3.<runId-64hex>.<selectionHash64>.<position>.
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub cursor: FieldPresence<::std::option::Option<Graph4PageCursor>>,
    pub size: ::std::num::NonZeroU64,
}
///Opaque host token bound to projectId+runId+factViewDigests+operation+effective params/order+page position. Continuation never re-resolves latest. Reference form q3.<runId-64hex>.<selectionHash64>.<position>.
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Graph4PageCursor(::std::string::String);
impl ::std::ops::Deref for Graph4PageCursor {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Graph4PageCursor> for ::std::string::String {
    fn from(value: Graph4PageCursor) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Graph4PageCursor {
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
impl ::std::convert::TryFrom<&str> for Graph4PageCursor {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Graph4PageCursor {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Graph4PageCursor {
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
///Closed optional bag for the 17 non-graph operations only. Graph operations must not use this shape.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug, Default)]
#[serde(deny_unknown_fields)]
pub struct Graph4Params {
    #[serde(
        rename = "artifactRef",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub artifact_ref: FieldPresence<::std::option::Option<Graph4ParamsArtifactRef>>,
    #[serde(
        rename = "baselineId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub baseline_id: FieldPresence<::std::option::Option<Common4BaselineId>>,
    #[serde(
        rename = "candidateId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub candidate_id: FieldPresence<::std::option::Option<Common4CandidateId>>,
    #[serde(
        rename = "comparisonResultId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub comparison_result_id: FieldPresence<
        ::std::option::Option<Common4ComparisonResultId>,
    >,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub direction: FieldPresence<::std::option::Option<Graph4ParamsDirection>>,
    #[serde(
        rename = "findingId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub finding_id: FieldPresence<::std::option::Option<Common4FindingId>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub fingerprint: FieldPresence<::std::option::Option<Common4Fingerprint>>,
    #[serde(
        rename = "importId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub import_id: FieldPresence<::std::option::Option<Common4ImportId>>,
    #[serde(
        rename = "includeSuppressed",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub include_suppressed: FieldPresence<::std::option::Option<bool>>,
    #[serde(
        rename = "maxDepth",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub max_depth: FieldPresence<::std::option::Option<::std::num::NonZeroU64>>,
    #[serde(
        rename = "otherRunId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub other_run_id: FieldPresence<::std::option::Option<Common4RunId>>,
    #[serde(
        rename = "receiptId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub receipt_id: FieldPresence<::std::option::Option<Common4ReceiptId>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub relation: FieldPresence<::std::option::Option<Common4CanonicalIdentifier>>,
    #[serde(
        rename = "ruleId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub rule_id: FieldPresence<::std::option::Option<Common4CanonicalIdentifier>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub subject: FieldPresence<::std::option::Option<Common4LogicalPath>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub target: FieldPresence<::std::option::Option<Common4LogicalPath>>,
}
///`Graph4ParamsArtifactRef`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Graph4ParamsArtifactRef {
    pub digest: Common4Sha256Hex,
    pub domain: Graph4ParamsArtifactRefDomain,
}
///`Graph4ParamsArtifactRefDomain`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Graph4ParamsArtifactRefDomain(::std::string::String);
impl ::std::ops::Deref for Graph4ParamsArtifactRefDomain {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Graph4ParamsArtifactRefDomain> for ::std::string::String {
    fn from(value: Graph4ParamsArtifactRefDomain) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Graph4ParamsArtifactRefDomain {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 64usize {
            return Err("longer than 64 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Graph4ParamsArtifactRefDomain {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Graph4ParamsArtifactRefDomain {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Graph4ParamsArtifactRefDomain {
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
///`Graph4ParamsDirection`
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
pub enum Graph4ParamsDirection {
    #[serde(rename = "outgoing")]
    Outgoing,
    #[serde(rename = "incoming")]
    Incoming,
    #[serde(rename = "both")]
    Both,
}
impl ::std::fmt::Display for Graph4ParamsDirection {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Outgoing => f.write_str("outgoing"),
            Self::Incoming => f.write_str("incoming"),
            Self::Both => f.write_str("both"),
        }
    }
}
impl ::std::str::FromStr for Graph4ParamsDirection {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "outgoing" => Ok(Self::Outgoing),
            "incoming" => Ok(Self::Incoming),
            "both" => Ok(Self::Both),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Graph4ParamsDirection {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Graph4ParamsDirection {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Graph-operation response view. Concrete run3 only. latest and snapshotId are forbidden here so a page cannot re-resolve.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Graph4ResolvedView {
    #[serde(rename = "runId")]
    pub run_id: Common4RunId,
}
///`Graph4RunShowItemV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Graph4RunShowItemV1 {
    #[serde(rename = "projectId")]
    pub project_id: Common4ProjectId,
    pub result: Graph4RunShowItemV1Result,
    #[serde(rename = "runId")]
    pub run_id: Common4RunId,
    #[serde(rename = "sealedRun")]
    pub sealed_run: Identity3Run,
}
///`Graph4RunShowItemV1Result`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Graph4RunShowItemV1Result {
    pub authority: Graph4RunShowItemV1ResultAuthority,
    #[serde(
        rename = "comparisonResultId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub comparison_result_id: FieldPresence<
        ::std::option::Option<Common4ComparisonResultId>,
    >,
    #[serde(
        rename = "coverageId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub coverage_id: FieldPresence<::std::option::Option<Common4CoverageId>>,
    pub deficiency: Common4D9Deficiency,
    pub durability: ::serde_json::Value,
    pub kind: Graph4RunShowItemV1ResultKind,
    #[serde(rename = "planId")]
    pub plan_id: Common4PlanId,
    #[serde(rename = "requiredCoverage")]
    pub required_coverage: Common4RequiredCoverage,
    #[serde(rename = "runId")]
    pub run_id: Common4RunId,
    #[serde(rename = "secondaryDeficiencies")]
    pub secondary_deficiencies: ::std::vec::Vec<Common4D9Deficiency>,
    pub verdict: Common4Verdict,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub verification: FieldPresence<
        ::std::option::Option<Invocation5VerificationOutcome>,
    >,
}
///`Graph4RunShowItemV1ResultAuthority`
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
pub enum Graph4RunShowItemV1ResultAuthority {
    #[serde(rename = "authoritative")]
    Authoritative,
}
impl ::std::fmt::Display for Graph4RunShowItemV1ResultAuthority {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Authoritative => f.write_str("authoritative"),
        }
    }
}
impl ::std::str::FromStr for Graph4RunShowItemV1ResultAuthority {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "authoritative" => Ok(Self::Authoritative),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Graph4RunShowItemV1ResultAuthority {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Graph4RunShowItemV1ResultAuthority {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Graph4RunShowItemV1ResultKind`
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
pub enum Graph4RunShowItemV1ResultKind {
    #[serde(rename = "analysis")]
    Analysis,
    #[serde(rename = "verify")]
    Verify,
}
impl ::std::fmt::Display for Graph4RunShowItemV1ResultKind {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Analysis => f.write_str("analysis"),
            Self::Verify => f.write_str("verify"),
        }
    }
}
impl ::std::str::FromStr for Graph4RunShowItemV1ResultKind {
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
impl ::std::convert::TryFrom<&str> for Graph4RunShowItemV1ResultKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Graph4RunShowItemV1ResultKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Graph4RunShowResponseV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug, Default)]
pub struct Graph4RunShowResponseV1 {
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub context: FieldPresence<::std::option::Option<Graph4RunShowResponseV1Context>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub operation: FieldPresence<::std::option::Option<::serde_json::Value>>,
}
///`Graph4RunShowResponseV1Context`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug, Default)]
pub struct Graph4RunShowResponseV1Context {
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub advisory: FieldPresence<::std::option::Option<::serde_json::Value>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub availability: FieldPresence<
        ::std::option::Option<Graph4RunShowResponseV1ContextAvailability>,
    >,
    #[serde(
        rename = "resolvedView",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub resolved_view: FieldPresence<::std::option::Option<Graph4ResolvedView>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub truncated: FieldPresence<::std::option::Option<::serde_json::Value>>,
}
///`Graph4RunShowResponseV1ContextAvailability`
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
pub enum Graph4RunShowResponseV1ContextAvailability {
    #[serde(rename = "retained")]
    Retained,
    #[serde(rename = "expired")]
    Expired,
    #[serde(rename = "purged")]
    Purged,
    #[serde(rename = "corrupt")]
    Corrupt,
    #[serde(rename = "unavailable")]
    Unavailable,
}
impl ::std::fmt::Display for Graph4RunShowResponseV1ContextAvailability {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Retained => f.write_str("retained"),
            Self::Expired => f.write_str("expired"),
            Self::Purged => f.write_str("purged"),
            Self::Corrupt => f.write_str("corrupt"),
            Self::Unavailable => f.write_str("unavailable"),
        }
    }
}
impl ::std::str::FromStr for Graph4RunShowResponseV1ContextAvailability {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "retained" => Ok(Self::Retained),
            "expired" => Ok(Self::Expired),
            "purged" => Ok(Self::Purged),
            "corrupt" => Ok(Self::Corrupt),
            "unavailable" => Ok(Self::Unavailable),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Graph4RunShowResponseV1ContextAvailability {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Graph4RunShowResponseV1ContextAvailability {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Graph4ScopeId`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
#[serde(transparent)]
pub struct Graph4ScopeId(pub ::std::string::String);
impl ::std::ops::Deref for Graph4ScopeId {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Graph4ScopeId> for ::std::string::String {
    fn from(value: Graph4ScopeId) -> Self {
        value.0
    }
}
impl ::std::convert::From<::std::string::String> for Graph4ScopeId {
    fn from(value: ::std::string::String) -> Self {
        Self(value)
    }
}
impl ::std::fmt::Display for Graph4ScopeId {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        self.0.fmt(f)
    }
}
impl ::std::str::FromStr for Graph4ScopeId {
    type Err = ::std::convert::Infallible;
    fn from_str(value: &str) -> ::std::result::Result<Self, Self::Err> {
        Ok(Self(value.to_string()))
    }
}
///`Graph4StoredKind`
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
pub enum Graph4StoredKind {
    #[serde(rename = "file")]
    File,
    #[serde(rename = "symbol")]
    Symbol,
    #[serde(rename = "package")]
    Package,
}
impl ::std::fmt::Display for Graph4StoredKind {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::File => f.write_str("file"),
            Self::Symbol => f.write_str("symbol"),
            Self::Package => f.write_str("package"),
        }
    }
}
impl ::std::str::FromStr for Graph4StoredKind {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "file" => Ok(Self::File),
            "symbol" => Ok(Self::Symbol),
            "package" => Ok(Self::Package),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Graph4StoredKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Graph4StoredKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Graph traversal completion for the declared semantic depth. complete: no owed unexamined work remains within maxDepth (exactly-at-cap is complete when the queue is empty). truncated-page: this page is full and more result units exist in the produced selection; page fullness is not operation truncation. truncated-bound: a work bound stopped the logical operation and owed unexamined work remains. Not native CoverageResult.
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
pub enum Graph4TraversalCoverage {
    #[serde(rename = "complete")]
    Complete,
    #[serde(rename = "truncated-page")]
    TruncatedPage,
    #[serde(rename = "truncated-bound")]
    TruncatedBound,
}
impl ::std::fmt::Display for Graph4TraversalCoverage {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Complete => f.write_str("complete"),
            Self::TruncatedPage => f.write_str("truncated-page"),
            Self::TruncatedBound => f.write_str("truncated-bound"),
        }
    }
}
impl ::std::str::FromStr for Graph4TraversalCoverage {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "complete" => Ok(Self::Complete),
            "truncated-page" => Ok(Self::TruncatedPage),
            "truncated-bound" => Ok(Self::TruncatedBound),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Graph4TraversalCoverage {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Graph4TraversalCoverage {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Request selector. latest is an explicitly trusted host observation of current run identity; it is never derived from static Run bytes. snapshotId is joined to the admitted Run's snapshotId; a host index is not authority. Empty domain is IDENTITY.UNKNOWN with QUERY.VIEW_UNKNOWN. Two candidate Runs for one snapshot is QUERY.VIEW_AMBIGUOUS, not untyped IDENTITY.UNKNOWN-by-count.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
pub enum Graph4View {
    #[serde(rename = "runId")]
    RunId(Common4RunId),
    #[serde(rename = "snapshotId")]
    SnapshotId(Common4SnapshotId),
    ///a resolver, never an authority: graph responses must carry ResolvedView {runId}; empty domain is request-rejected
    #[serde(rename = "latest")]
    Latest(::serde_json::Value),
}
impl ::std::convert::From<Common4RunId> for Graph4View {
    fn from(value: Common4RunId) -> Self {
        Self::RunId(value)
    }
}
impl ::std::convert::From<Common4SnapshotId> for Graph4View {
    fn from(value: Common4SnapshotId) -> Self {
        Self::SnapshotId(value)
    }
}
impl ::std::convert::From<::serde_json::Value> for Graph4View {
    fn from(value: ::serde_json::Value) -> Self {
        Self::Latest(value)
    }
}
///Existing view2 identity of an admitted fact-view. Not a new FactViewId recipe.
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
#[serde(transparent)]
pub struct Graph4ViewDigest(pub ::std::string::String);
impl ::std::ops::Deref for Graph4ViewDigest {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Graph4ViewDigest> for ::std::string::String {
    fn from(value: Graph4ViewDigest) -> Self {
        value.0
    }
}
impl ::std::convert::From<::std::string::String> for Graph4ViewDigest {
    fn from(value: ::std::string::String) -> Self {
        Self(value)
    }
}
impl ::std::fmt::Display for Graph4ViewDigest {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        self.0.fmt(f)
    }
}
impl ::std::str::FromStr for Graph4ViewDigest {
    type Err = ::std::convert::Infallible;
    fn from_str(value: &str) -> ::std::result::Result<Self, Self::Err> {
        Ok(Self(value.to_string()))
    }
}
///`Metadata1BuildMetadataV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Metadata1BuildMetadataV1 {
    #[serde(rename = "buildChannel")]
    pub build_channel: Metadata1BuildMetadataV1BuildChannel,
    #[serde(rename = "closureIds")]
    pub closure_ids: ::std::vec::Vec<Common3ClosureId>,
    #[serde(rename = "hostRelease")]
    pub host_release: Metadata1HostRelease,
    #[serde(rename = "schemaVersion")]
    pub schema_version: ExactInteger,
}
///`Metadata1BuildMetadataV1BuildChannel`
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
pub enum Metadata1BuildMetadataV1BuildChannel {
    #[serde(rename = "development")]
    Development,
    #[serde(rename = "release")]
    Release,
}
impl ::std::fmt::Display for Metadata1BuildMetadataV1BuildChannel {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Development => f.write_str("development"),
            Self::Release => f.write_str("release"),
        }
    }
}
impl ::std::str::FromStr for Metadata1BuildMetadataV1BuildChannel {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "development" => Ok(Self::Development),
            "release" => Ok(Self::Release),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Metadata1BuildMetadataV1BuildChannel {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Metadata1BuildMetadataV1BuildChannel {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Metadata1CommandName`
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
pub enum Metadata1CommandName {
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
impl ::std::fmt::Display for Metadata1CommandName {
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
impl ::std::str::FromStr for Metadata1CommandName {
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
impl ::std::convert::TryFrom<&str> for Metadata1CommandName {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Metadata1CommandName {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Metadata1HelpCommand`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Metadata1HelpCommand {
    pub name: Metadata1CommandName,
    pub summary: Metadata1HelpCommandSummary,
    pub usage: Metadata1HelpCommandUsage,
}
///`Metadata1HelpCommandSummary`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Metadata1HelpCommandSummary(::std::string::String);
impl ::std::ops::Deref for Metadata1HelpCommandSummary {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Metadata1HelpCommandSummary> for ::std::string::String {
    fn from(value: Metadata1HelpCommandSummary) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Metadata1HelpCommandSummary {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 2048usize {
            return Err("longer than 2048 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Metadata1HelpCommandSummary {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Metadata1HelpCommandSummary {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Metadata1HelpCommandSummary {
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
///`Metadata1HelpCommandUsage`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Metadata1HelpCommandUsage(::std::string::String);
impl ::std::ops::Deref for Metadata1HelpCommandUsage {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Metadata1HelpCommandUsage> for ::std::string::String {
    fn from(value: Metadata1HelpCommandUsage) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Metadata1HelpCommandUsage {
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
impl ::std::convert::TryFrom<&str> for Metadata1HelpCommandUsage {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Metadata1HelpCommandUsage {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Metadata1HelpCommandUsage {
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
///`Metadata1HelpMetadataV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Metadata1HelpMetadataV1 {
    pub command: ::serde_json::Value,
    pub commands: ::std::vec::Vec<Metadata1HelpCommand>,
    #[serde(deserialize_with = "::std::option::Option::deserialize")]
    pub topic: ::std::option::Option<Metadata1CommandName>,
}
///`Metadata1HostRelease`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Metadata1HostRelease(::std::string::String);
impl ::std::ops::Deref for Metadata1HostRelease {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Metadata1HostRelease> for ::std::string::String {
    fn from(value: Metadata1HostRelease) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Metadata1HostRelease {
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
impl ::std::convert::TryFrom<&str> for Metadata1HostRelease {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Metadata1HostRelease {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Metadata1HostRelease {
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
///`Metadata1Root`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(untagged)]
pub enum Metadata1Root {
    HelpMetadataV1(Metadata1HelpMetadataV1),
    VersionMetadataV1(Metadata1VersionMetadataV1),
}
impl ::std::convert::From<Metadata1HelpMetadataV1> for Metadata1Root {
    fn from(value: Metadata1HelpMetadataV1) -> Self {
        Self::HelpMetadataV1(value)
    }
}
impl ::std::convert::From<Metadata1VersionMetadataV1> for Metadata1Root {
    fn from(value: Metadata1VersionMetadataV1) -> Self {
        Self::VersionMetadataV1(value)
    }
}
///`Metadata1VersionMetadataV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Metadata1VersionMetadataV1 {
    #[serde(rename = "buildChannel")]
    pub build_channel: Metadata1VersionMetadataV1BuildChannel,
    #[serde(rename = "closureIds")]
    pub closure_ids: ::std::vec::Vec<Common3ClosureId>,
    pub command: ::serde_json::Value,
    #[serde(rename = "hostRelease")]
    pub host_release: Metadata1HostRelease,
}
///`Metadata1VersionMetadataV1BuildChannel`
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
pub enum Metadata1VersionMetadataV1BuildChannel {
    #[serde(rename = "development")]
    Development,
    #[serde(rename = "release")]
    Release,
}
impl ::std::fmt::Display for Metadata1VersionMetadataV1BuildChannel {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Development => f.write_str("development"),
            Self::Release => f.write_str("release"),
        }
    }
}
impl ::std::str::FromStr for Metadata1VersionMetadataV1BuildChannel {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "development" => Ok(Self::Development),
            "release" => Ok(Self::Release),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Metadata1VersionMetadataV1BuildChannel {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Metadata1VersionMetadataV1BuildChannel {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`PolicyTest1Case`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct PolicyTest1Case {
    pub expectations: ::std::vec::Vec<PolicyTest1Expectation>,
    pub id: Common1CanonicalIdentifier,
    pub subject: PolicyTest1Subject,
}
///`PolicyTest1CaseResult`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct PolicyTest1CaseResult {
    #[serde(rename = "expectationOutcomes")]
    pub expectation_outcomes: ::std::vec::Vec<
        PolicyTest1CaseResultExpectationOutcomesItem,
    >,
    pub findings: ::std::vec::Vec<PolicyTest1CaseResultFindingsItem>,
    pub id: Common1CanonicalIdentifier,
    #[serde(rename = "indeterminateRules")]
    pub indeterminate_rules: ::std::vec::Vec<Common1CanonicalIdentifier>,
    #[serde(rename = "observedVerdict")]
    pub observed_verdict: Common1Verdict,
    ///indeterminate: the fixture's declared Coverage was insufficient for an expectation that asserts a definite result. not-executable: a sources fixture without a bundled provider closure in the test host.
    pub outcome: PolicyTest1CaseResultOutcome,
}
///`PolicyTest1CaseResultExpectationOutcomesItem`
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
pub enum PolicyTest1CaseResultExpectationOutcomesItem {
    #[serde(rename = "met")]
    Met,
    #[serde(rename = "unmet")]
    Unmet,
    #[serde(rename = "indeterminate")]
    Indeterminate,
}
impl ::std::fmt::Display for PolicyTest1CaseResultExpectationOutcomesItem {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Met => f.write_str("met"),
            Self::Unmet => f.write_str("unmet"),
            Self::Indeterminate => f.write_str("indeterminate"),
        }
    }
}
impl ::std::str::FromStr for PolicyTest1CaseResultExpectationOutcomesItem {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "met" => Ok(Self::Met),
            "unmet" => Ok(Self::Unmet),
            "indeterminate" => Ok(Self::Indeterminate),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for PolicyTest1CaseResultExpectationOutcomesItem {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for PolicyTest1CaseResultExpectationOutcomesItem {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`PolicyTest1CaseResultFindingsItem`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct PolicyTest1CaseResultFindingsItem {
    #[serde(rename = "ruleId")]
    pub rule_id: Common1CanonicalIdentifier,
    pub subject: Common1LogicalPath,
    pub waived: bool,
}
///indeterminate: the fixture's declared Coverage was insufficient for an expectation that asserts a definite result. not-executable: a sources fixture without a bundled provider closure in the test host.
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
pub enum PolicyTest1CaseResultOutcome {
    #[serde(rename = "passed")]
    Passed,
    #[serde(rename = "failed")]
    Failed,
    #[serde(rename = "indeterminate")]
    Indeterminate,
    #[serde(rename = "not-executable")]
    NotExecutable,
}
impl ::std::fmt::Display for PolicyTest1CaseResultOutcome {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Passed => f.write_str("passed"),
            Self::Failed => f.write_str("failed"),
            Self::Indeterminate => f.write_str("indeterminate"),
            Self::NotExecutable => f.write_str("not-executable"),
        }
    }
}
impl ::std::str::FromStr for PolicyTest1CaseResultOutcome {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "passed" => Ok(Self::Passed),
            "failed" => Ok(Self::Failed),
            "indeterminate" => Ok(Self::Indeterminate),
            "not-executable" => Ok(Self::NotExecutable),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for PolicyTest1CaseResultOutcome {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for PolicyTest1CaseResultOutcome {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`PolicyTest1Expectation`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(tag = "kind", deny_unknown_fields)]
pub enum PolicyTest1Expectation {
    #[serde(rename = "finding")]
    Finding {
        #[serde(
            rename = "maxCount",
            default,
            skip_serializing_if = "FieldPresence::is_missing"
        )]
        max_count: FieldPresence<::std::option::Option<::std::num::NonZeroU64>>,
        #[serde(rename = "minCount")]
        min_count: ::std::num::NonZeroU64,
        #[serde(rename = "ruleId")]
        rule_id: Common1CanonicalIdentifier,
        #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
        subjects: FieldPresence<
            ::std::option::Option<::std::vec::Vec<Common1LogicalPath>>,
        >,
    },
    #[serde(rename = "no-finding")]
    NoFinding { #[serde(rename = "ruleId")] rule_id: Common1CanonicalIdentifier },
    #[serde(rename = "verdict")]
    Verdict { verdict: Common1Verdict },
    #[serde(rename = "indeterminate")]
    Indeterminate { #[serde(rename = "ruleId")] rule_id: Common1CanonicalIdentifier },
}
///A host-schema fact supplied as test input. The suite cannot mint fact2 identities; the verifier computes them.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct PolicyTest1FactRecordCandidate {
    #[serde(rename = "confidenceMillionths")]
    pub confidence_millionths: i64,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub observability: FieldPresence<
        ::std::option::Option<PolicyTest1FactRecordCandidateObservability>,
    >,
    pub relation: Common1CanonicalIdentifier,
    pub resolution: Policy1Rung,
    pub subject: Common1LogicalPath,
    #[serde(
        rename = "subjectKind",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub subject_kind: FieldPresence<
        ::std::option::Option<PolicyTest1FactRecordCandidateSubjectKind>,
    >,
    pub target: Common1LogicalPath,
    #[serde(
        rename = "targetKind",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub target_kind: FieldPresence<
        ::std::option::Option<PolicyTest1FactRecordCandidateTargetKind>,
    >,
    pub universe: Common1CanonicalIdentifier,
}
///`PolicyTest1FactRecordCandidateObservability`
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
pub enum PolicyTest1FactRecordCandidateObservability {
    #[serde(rename = "observed-hit")]
    ObservedHit,
    #[serde(rename = "observable-unhit")]
    ObservableUnhit,
    #[serde(rename = "unobservable")]
    Unobservable,
    #[serde(rename = "unmapped")]
    Unmapped,
}
impl ::std::fmt::Display for PolicyTest1FactRecordCandidateObservability {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::ObservedHit => f.write_str("observed-hit"),
            Self::ObservableUnhit => f.write_str("observable-unhit"),
            Self::Unobservable => f.write_str("unobservable"),
            Self::Unmapped => f.write_str("unmapped"),
        }
    }
}
impl ::std::str::FromStr for PolicyTest1FactRecordCandidateObservability {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "observed-hit" => Ok(Self::ObservedHit),
            "observable-unhit" => Ok(Self::ObservableUnhit),
            "unobservable" => Ok(Self::Unobservable),
            "unmapped" => Ok(Self::Unmapped),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for PolicyTest1FactRecordCandidateObservability {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for PolicyTest1FactRecordCandidateObservability {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`PolicyTest1FactRecordCandidateSubjectKind`
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
pub enum PolicyTest1FactRecordCandidateSubjectKind {
    #[serde(rename = "file")]
    File,
    #[serde(rename = "symbol")]
    Symbol,
    #[serde(rename = "export")]
    Export,
    #[serde(rename = "package")]
    Package,
}
impl ::std::fmt::Display for PolicyTest1FactRecordCandidateSubjectKind {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::File => f.write_str("file"),
            Self::Symbol => f.write_str("symbol"),
            Self::Export => f.write_str("export"),
            Self::Package => f.write_str("package"),
        }
    }
}
impl ::std::str::FromStr for PolicyTest1FactRecordCandidateSubjectKind {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "file" => Ok(Self::File),
            "symbol" => Ok(Self::Symbol),
            "export" => Ok(Self::Export),
            "package" => Ok(Self::Package),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for PolicyTest1FactRecordCandidateSubjectKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for PolicyTest1FactRecordCandidateSubjectKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`PolicyTest1FactRecordCandidateTargetKind`
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
pub enum PolicyTest1FactRecordCandidateTargetKind {
    #[serde(rename = "file")]
    File,
    #[serde(rename = "symbol")]
    Symbol,
    #[serde(rename = "export")]
    Export,
    #[serde(rename = "package")]
    Package,
    #[serde(rename = "external")]
    External,
}
impl ::std::fmt::Display for PolicyTest1FactRecordCandidateTargetKind {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::File => f.write_str("file"),
            Self::Symbol => f.write_str("symbol"),
            Self::Export => f.write_str("export"),
            Self::Package => f.write_str("package"),
            Self::External => f.write_str("external"),
        }
    }
}
impl ::std::str::FromStr for PolicyTest1FactRecordCandidateTargetKind {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "file" => Ok(Self::File),
            "symbol" => Ok(Self::Symbol),
            "export" => Ok(Self::Export),
            "package" => Ok(Self::Package),
            "external" => Ok(Self::External),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for PolicyTest1FactRecordCandidateTargetKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for PolicyTest1FactRecordCandidateTargetKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Test-only override of effective policy for this invocation. Disclosed in the result; never written.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct PolicyTest1Override {
    pub field: PolicyTest1OverrideField,
    #[serde(rename = "ruleId")]
    pub rule_id: Common1CanonicalIdentifier,
    pub value: PolicyTest1OverrideValue,
}
///`PolicyTest1OverrideField`
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
pub enum PolicyTest1OverrideField {
    #[serde(rename = "enabled")]
    Enabled,
    #[serde(rename = "severity")]
    Severity,
    #[serde(rename = "gate")]
    Gate,
}
impl ::std::fmt::Display for PolicyTest1OverrideField {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Enabled => f.write_str("enabled"),
            Self::Severity => f.write_str("severity"),
            Self::Gate => f.write_str("gate"),
        }
    }
}
impl ::std::str::FromStr for PolicyTest1OverrideField {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "enabled" => Ok(Self::Enabled),
            "severity" => Ok(Self::Severity),
            "gate" => Ok(Self::Gate),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for PolicyTest1OverrideField {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for PolicyTest1OverrideField {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`PolicyTest1OverrideValue`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(untagged)]
pub enum PolicyTest1OverrideValue {
    Boolean(bool),
    Policy1Severity(Policy1Severity),
}
impl ::std::fmt::Display for PolicyTest1OverrideValue {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match self {
            Self::Boolean(x) => x.fmt(f),
            Self::Policy1Severity(x) => x.fmt(f),
        }
    }
}
impl ::std::str::FromStr for PolicyTest1OverrideValue {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if let Ok(v) = value.parse() {
            Ok(Self::Boolean(v))
        } else if let Ok(v) = value.parse() {
            Ok(Self::Policy1Severity(v))
        } else {
            Err("string conversion failed for all variants".into())
        }
    }
}
impl ::std::convert::TryFrom<&str> for PolicyTest1OverrideValue {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for PolicyTest1OverrideValue {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::From<bool> for PolicyTest1OverrideValue {
    fn from(value: bool) -> Self {
        Self::Boolean(value)
    }
}
impl ::std::convert::From<Policy1Severity> for PolicyTest1OverrideValue {
    fn from(value: Policy1Severity) -> Self {
        Self::Policy1Severity(value)
    }
}
///`PolicyTest1PolicyTestResultV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct PolicyTest1PolicyTestResultV1 {
    #[serde(rename = "candidatePolicyDigest")]
    pub candidate_policy_digest: Common1Sha256Hex,
    ///digest of the candidate after overrides; equals candidatePolicyDigest when no override applied
    #[serde(rename = "effectivePolicyDigest")]
    pub effective_policy_digest: Common1Sha256Hex,
    #[serde(rename = "enforcementUnchanged")]
    pub enforcement_unchanged: ::serde_json::Value,
    #[serde(rename = "overridesApplied")]
    pub overrides_applied: ::std::vec::Vec<PolicyTest1Override>,
    #[serde(rename = "policyTestResultId")]
    pub policy_test_result_id: Common1PolicyTestResultId,
    #[serde(rename = "resolverAccepted")]
    pub resolver_accepted: bool,
    #[serde(rename = "resolverRefusals")]
    pub resolver_refusals: ::std::vec::Vec<Common1DomainDetail>,
    pub results: ::std::vec::Vec<PolicyTest1CaseResult>,
    #[serde(rename = "schemaFamily")]
    pub schema_family: ::serde_json::Value,
    #[serde(rename = "schemaMajor")]
    pub schema_major: ExactInteger,
    ///Bare H("workflow.policy-test-suite", the complete admitted PolicyTestSuiteV1 before overrides), under identity section 3. Retain the suite preimage; not raw SHA-256 of canonical suite bytes.
    #[serde(rename = "suiteDigest")]
    pub suite_digest: Common1Sha256Hex,
    pub summary: PolicyTest1PolicyTestResultV1Summary,
    #[serde(rename = "waiverResolution")]
    pub waiver_resolution: Policy1WaiverResolutionV1,
}
///`PolicyTest1PolicyTestResultV1Summary`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct PolicyTest1PolicyTestResultV1Summary {
    pub failed: Common1Uint53,
    pub indeterminate: Common1Uint53,
    #[serde(rename = "notExecutable")]
    pub not_executable: Common1Uint53,
    pub passed: Common1Uint53,
}
///`PolicyTest1PolicyTestSuiteV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct PolicyTest1PolicyTestSuiteV1 {
    ///date used for waiver expiry resolution in the fixture; defaults to no expiry resolution (all non-expired) when absent
    #[serde(
        rename = "asOfDate",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub as_of_date: FieldPresence<::std::option::Option<Common1UtcDate>>,
    #[serde(rename = "candidatePolicy")]
    pub candidate_policy: Policy1PolicyDocumentV1,
    pub cases: ::std::vec::Vec<PolicyTest1Case>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub overrides: FieldPresence<::std::vec::Vec<PolicyTest1Override>>,
    #[serde(rename = "schemaFamily")]
    pub schema_family: ::serde_json::Value,
    #[serde(rename = "schemaMajor")]
    pub schema_major: ExactInteger,
    pub waivers: Policy1WaiverSetV1,
}
///A suite tests a candidate PolicyDocumentV1 before enforcement. Every case supplies typed fact records with a declared Coverage state and is evaluated by the deterministic fixture verifier (the pure evaluator over a finite fact view; no provider, no repository code). Optionally a case names a bounded source fixture analyzed under an ephemeral non-authoritative Plan by the bundled trusted providers; that path is disclosed and never authoritative. The operation is Query class: it never writes tracked intent, never promotes severity, and discloses every override it applied. Bounds: at most 1024 cases per suite; at most 100000 fact records per case; at most 4194304 source bytes and 256 files per case.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(transparent)]
pub struct PolicyTest1Root(pub ::serde_json::Value);
impl ::std::ops::Deref for PolicyTest1Root {
    type Target = ::serde_json::Value;
    fn deref(&self) -> &::serde_json::Value {
        &self.0
    }
}
impl ::std::convert::From<PolicyTest1Root> for ::serde_json::Value {
    fn from(value: PolicyTest1Root) -> Self {
        value.0
    }
}
impl ::std::convert::From<::serde_json::Value> for PolicyTest1Root {
    fn from(value: ::serde_json::Value) -> Self {
        Self(value)
    }
}
///`PolicyTest1SourceFile`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct PolicyTest1SourceFile {
    pub bytes: i64,
    pub path: Common1LogicalPath,
    pub sha256: Common1Sha256Hex,
}
///`PolicyTest1Subject`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(tag = "kind", deny_unknown_fields)]
pub enum PolicyTest1Subject {
    #[serde(rename = "facts")]
    Facts {
        ///declared Coverage of the supplied fact view; partial/unknown lets a case assert indeterminate behavior
        coverage: PolicyTest1SubjectCoverage,
        #[serde(rename = "evidenceAvailable")]
        evidence_available: ::std::vec::Vec<Imported1ImportKind>,
        facts: ::std::vec::Vec<PolicyTest1FactRecordCandidate>,
        ///the complete enumerated subject inventory for the fixture; a rule's subjectEnumeration selects from it
        subjects: ::std::vec::Vec<Common1LogicalPath>,
    },
    #[serde(rename = "sources")]
    Sources { files: ::std::vec::Vec<PolicyTest1SourceFile> },
}
///declared Coverage of the supplied fact view; partial/unknown lets a case assert indeterminate behavior
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
pub enum PolicyTest1SubjectCoverage {
    #[serde(rename = "complete")]
    Complete,
    #[serde(rename = "partial")]
    Partial,
    #[serde(rename = "unknown")]
    Unknown,
}
impl ::std::fmt::Display for PolicyTest1SubjectCoverage {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Complete => f.write_str("complete"),
            Self::Partial => f.write_str("partial"),
            Self::Unknown => f.write_str("unknown"),
        }
    }
}
impl ::std::str::FromStr for PolicyTest1SubjectCoverage {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "complete" => Ok(Self::Complete),
            "partial" => Ok(Self::Partial),
            "unknown" => Ok(Self::Unknown),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for PolicyTest1SubjectCoverage {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for PolicyTest1SubjectCoverage {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`PolicyTest2PolicyTestSuiteV2`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct PolicyTest2PolicyTestSuiteV2 {
    ///date used for waiver expiry resolution in the fixture; defaults to no expiry resolution (all non-expired) when absent
    #[serde(
        rename = "asOfDate",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub as_of_date: FieldPresence<::std::option::Option<Common1UtcDate>>,
    #[serde(rename = "candidatePolicy")]
    pub candidate_policy: Policy2PolicyDocumentV2,
    ///Facts cases are evaluated under x-opensip-fixture-representation. Sources cases are not-executable in this reference.
    pub cases: ::std::vec::Vec<PolicyTest1Case>,
    ///Test-only overrides of the effective policy, disclosed in the result and never written. Each names a candidate rule and carries the value type of its field (boolean for enabled and gate, Severity for severity).
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub overrides: FieldPresence<::std::vec::Vec<PolicyTest1Override>>,
    #[serde(rename = "schemaFamily")]
    pub schema_family: ::serde_json::Value,
    #[serde(rename = "schemaMajor")]
    pub schema_major: ExactInteger,
    pub waivers: Policy1WaiverSetV1,
}
///The current evaluator3 `opensip policy test SUITE` input. A suite tests a candidate PolicyDocumentV2 before enforcement. schemaMajor 2 because the admitted candidate policy is PolicyDocumentV2 and the whole admitted suite, including this major and the candidate's own major, is the H("workflow.policy-test-suite", PolicyTestSuiteV2) preimage of PolicyTestResultV1.suiteDigest. Waivers (WaiverSetV1), cases (Case) and test-only overrides (Override) keep their retained owner definitions. The deterministic result stays urn:opensip:product-v1:workflows:policy-test#/$defs/PolicyTestResultV1 with prefix policytest2; its candidate and effective policy digests are raw SHA-256 of PolicyDocumentV2 canonical bytes. The retained PolicyTestSuiteV1 (candidate PolicyDocumentV1) is the historical workflow1 input and is not an alternative parser here: a suite or candidate policy of another major is refused before schema validation (REQUEST.SCHEMA_MAJOR_UNSUPPORTED / EVALUATION.MIXED_OUTPUT_MAJOR) and is never relabelled or coerced. Bounds are those of the retained definitions: at most 1024 cases, at most 64 overrides.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(transparent)]
pub struct PolicyTest2Root(pub ::serde_json::Value);
impl ::std::ops::Deref for PolicyTest2Root {
    type Target = ::serde_json::Value;
    fn deref(&self) -> &::serde_json::Value {
        &self.0
    }
}
impl ::std::convert::From<PolicyTest2Root> for ::serde_json::Value {
    fn from(value: PolicyTest2Root) -> Self {
        value.0
    }
}
impl ::std::convert::From<::serde_json::Value> for PolicyTest2Root {
    fn from(value: ::serde_json::Value) -> Self {
        Self(value)
    }
}
///`PresentationCatalog1CapabilityDescriptionV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct PresentationCatalog1CapabilityDescriptionV1 {
    #[serde(rename = "capabilityId")]
    pub capability_id: Common4CanonicalIdentifier,
    pub description: PresentationCatalog1CapabilityDescriptionV1Description,
    pub name: PresentationCatalog1CapabilityDescriptionV1Name,
    pub tags: ::std::vec::Vec<Common4CanonicalIdentifier>,
}
///`PresentationCatalog1CapabilityDescriptionV1Description`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct PresentationCatalog1CapabilityDescriptionV1Description(::std::string::String);
impl ::std::ops::Deref for PresentationCatalog1CapabilityDescriptionV1Description {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<PresentationCatalog1CapabilityDescriptionV1Description>
for ::std::string::String {
    fn from(value: PresentationCatalog1CapabilityDescriptionV1Description) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for PresentationCatalog1CapabilityDescriptionV1Description {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 8192usize {
            return Err("longer than 8192 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str>
for PresentationCatalog1CapabilityDescriptionV1Description {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for PresentationCatalog1CapabilityDescriptionV1Description {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de>
for PresentationCatalog1CapabilityDescriptionV1Description {
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
///`PresentationCatalog1CapabilityDescriptionV1Name`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct PresentationCatalog1CapabilityDescriptionV1Name(::std::string::String);
impl ::std::ops::Deref for PresentationCatalog1CapabilityDescriptionV1Name {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<PresentationCatalog1CapabilityDescriptionV1Name>
for ::std::string::String {
    fn from(value: PresentationCatalog1CapabilityDescriptionV1Name) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for PresentationCatalog1CapabilityDescriptionV1Name {
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
impl ::std::convert::TryFrom<&str> for PresentationCatalog1CapabilityDescriptionV1Name {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for PresentationCatalog1CapabilityDescriptionV1Name {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for PresentationCatalog1CapabilityDescriptionV1Name {
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
///`PresentationCatalog1RecipeDescriptionV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct PresentationCatalog1RecipeDescriptionV1 {
    pub description: PresentationCatalog1RecipeDescriptionV1Description,
    pub name: PresentationCatalog1RecipeDescriptionV1Name,
    #[serde(rename = "parameterDescriptions")]
    pub parameter_descriptions: PresentationCatalog1RecipeDescriptionV1ParameterDescriptions,
    #[serde(rename = "recipeKey")]
    pub recipe_key: PresentationCatalog1RecipeDescriptionV1RecipeKey,
    pub tags: ::std::vec::Vec<Common4CanonicalIdentifier>,
    #[serde(rename = "targetBounds")]
    pub target_bounds: PresentationCatalog1RecipeDescriptionV1TargetBounds,
}
///`PresentationCatalog1RecipeDescriptionV1Description`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct PresentationCatalog1RecipeDescriptionV1Description(::std::string::String);
impl ::std::ops::Deref for PresentationCatalog1RecipeDescriptionV1Description {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<PresentationCatalog1RecipeDescriptionV1Description>
for ::std::string::String {
    fn from(value: PresentationCatalog1RecipeDescriptionV1Description) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for PresentationCatalog1RecipeDescriptionV1Description {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 8192usize {
            return Err("longer than 8192 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str>
for PresentationCatalog1RecipeDescriptionV1Description {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for PresentationCatalog1RecipeDescriptionV1Description {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de>
for PresentationCatalog1RecipeDescriptionV1Description {
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
///`PresentationCatalog1RecipeDescriptionV1Name`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct PresentationCatalog1RecipeDescriptionV1Name(::std::string::String);
impl ::std::ops::Deref for PresentationCatalog1RecipeDescriptionV1Name {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<PresentationCatalog1RecipeDescriptionV1Name>
for ::std::string::String {
    fn from(value: PresentationCatalog1RecipeDescriptionV1Name) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for PresentationCatalog1RecipeDescriptionV1Name {
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
impl ::std::convert::TryFrom<&str> for PresentationCatalog1RecipeDescriptionV1Name {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for PresentationCatalog1RecipeDescriptionV1Name {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for PresentationCatalog1RecipeDescriptionV1Name {
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
///`PresentationCatalog1RecipeDescriptionV1ParameterDescriptions`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct PresentationCatalog1RecipeDescriptionV1ParameterDescriptions {
    #[serde(rename = "evidenceSource")]
    pub evidence_source: PresentationCatalog1RecipeDescriptionV1ParameterDescriptionsEvidenceSource,
    pub targets: PresentationCatalog1RecipeDescriptionV1ParameterDescriptionsTargets,
}
///`PresentationCatalog1RecipeDescriptionV1ParameterDescriptionsEvidenceSource`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct PresentationCatalog1RecipeDescriptionV1ParameterDescriptionsEvidenceSource(
    ::std::string::String,
);
impl ::std::ops::Deref
for PresentationCatalog1RecipeDescriptionV1ParameterDescriptionsEvidenceSource {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<
    PresentationCatalog1RecipeDescriptionV1ParameterDescriptionsEvidenceSource,
> for ::std::string::String {
    fn from(
        value: PresentationCatalog1RecipeDescriptionV1ParameterDescriptionsEvidenceSource,
    ) -> Self {
        value.0
    }
}
impl ::std::str::FromStr
for PresentationCatalog1RecipeDescriptionV1ParameterDescriptionsEvidenceSource {
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
impl ::std::convert::TryFrom<&str>
for PresentationCatalog1RecipeDescriptionV1ParameterDescriptionsEvidenceSource {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for PresentationCatalog1RecipeDescriptionV1ParameterDescriptionsEvidenceSource {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de>
for PresentationCatalog1RecipeDescriptionV1ParameterDescriptionsEvidenceSource {
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
///`PresentationCatalog1RecipeDescriptionV1ParameterDescriptionsTargets`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct PresentationCatalog1RecipeDescriptionV1ParameterDescriptionsTargets(
    ::std::string::String,
);
impl ::std::ops::Deref
for PresentationCatalog1RecipeDescriptionV1ParameterDescriptionsTargets {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<
    PresentationCatalog1RecipeDescriptionV1ParameterDescriptionsTargets,
> for ::std::string::String {
    fn from(
        value: PresentationCatalog1RecipeDescriptionV1ParameterDescriptionsTargets,
    ) -> Self {
        value.0
    }
}
impl ::std::str::FromStr
for PresentationCatalog1RecipeDescriptionV1ParameterDescriptionsTargets {
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
impl ::std::convert::TryFrom<&str>
for PresentationCatalog1RecipeDescriptionV1ParameterDescriptionsTargets {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for PresentationCatalog1RecipeDescriptionV1ParameterDescriptionsTargets {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de>
for PresentationCatalog1RecipeDescriptionV1ParameterDescriptionsTargets {
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
///`PresentationCatalog1RecipeDescriptionV1RecipeKey`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct PresentationCatalog1RecipeDescriptionV1RecipeKey {
    #[serde(rename = "contributionId")]
    pub contribution_id: Common4ContributionId,
    #[serde(rename = "recipeId")]
    pub recipe_id: Common4CanonicalIdentifier,
    #[serde(rename = "recipeVersion")]
    pub recipe_version: Common4SemanticVersion,
}
///`PresentationCatalog1RecipeDescriptionV1TargetBounds`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct PresentationCatalog1RecipeDescriptionV1TargetBounds {
    pub kind: ::serde_json::Value,
    #[serde(rename = "maximumTargets")]
    pub maximum_targets: ExactInteger,
    #[serde(rename = "minimumTargets")]
    pub minimum_targets: ExactInteger,
}
///`PresentationCatalog1Root`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct PresentationCatalog1Root {
    pub capabilities: ::std::vec::Vec<PresentationCatalog1CapabilityDescriptionV1>,
    pub recipes: ::std::vec::Vec<PresentationCatalog1RecipeDescriptionV1>,
    pub rules: ::std::vec::Vec<PresentationCatalog1RuleDescriptionV1>,
    #[serde(rename = "schemaFamily")]
    pub schema_family: ::serde_json::Value,
    #[serde(rename = "schemaMajor")]
    pub schema_major: ExactInteger,
}
///`PresentationCatalog1RuleDescriptionV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct PresentationCatalog1RuleDescriptionV1 {
    pub description: PresentationCatalog1RuleDescriptionV1Description,
    pub name: PresentationCatalog1RuleDescriptionV1Name,
    #[serde(rename = "ruleProgramRef")]
    pub rule_program_ref: PresentationCatalog1RuleDescriptionV1RuleProgramRef,
    pub tags: ::std::vec::Vec<Common4CanonicalIdentifier>,
}
///`PresentationCatalog1RuleDescriptionV1Description`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct PresentationCatalog1RuleDescriptionV1Description(::std::string::String);
impl ::std::ops::Deref for PresentationCatalog1RuleDescriptionV1Description {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<PresentationCatalog1RuleDescriptionV1Description>
for ::std::string::String {
    fn from(value: PresentationCatalog1RuleDescriptionV1Description) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for PresentationCatalog1RuleDescriptionV1Description {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 8192usize {
            return Err("longer than 8192 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for PresentationCatalog1RuleDescriptionV1Description {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for PresentationCatalog1RuleDescriptionV1Description {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de>
for PresentationCatalog1RuleDescriptionV1Description {
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
///`PresentationCatalog1RuleDescriptionV1Name`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct PresentationCatalog1RuleDescriptionV1Name(::std::string::String);
impl ::std::ops::Deref for PresentationCatalog1RuleDescriptionV1Name {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<PresentationCatalog1RuleDescriptionV1Name>
for ::std::string::String {
    fn from(value: PresentationCatalog1RuleDescriptionV1Name) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for PresentationCatalog1RuleDescriptionV1Name {
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
impl ::std::convert::TryFrom<&str> for PresentationCatalog1RuleDescriptionV1Name {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for PresentationCatalog1RuleDescriptionV1Name {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for PresentationCatalog1RuleDescriptionV1Name {
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
///`PresentationCatalog1RuleDescriptionV1RuleProgramRef`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct PresentationCatalog1RuleDescriptionV1RuleProgramRef {
    #[serde(rename = "contributionId")]
    pub contribution_id: Common1ContributionId,
    #[serde(rename = "programDigest")]
    pub program_digest: Common1Sha256Hex,
    #[serde(rename = "ruleStableId")]
    pub rule_stable_id: Common1CanonicalIdentifier,
    #[serde(rename = "semanticsMajor")]
    pub semantics_major: u16,
}
///`Repair2EvidenceRequirement`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Repair2EvidenceRequirement {
    pub completeness: Repair2EvidenceRequirementCompleteness,
    ///The reason THIS requirement is unsatisfied, in the vocabulary of THIS requirement's evidence PLANE. Repair admits a requirement over either plane, so the field carries either vocabulary and the plane is decided AT ADMISSION from the relation's registry membership - never guessed from the value and never left to the reader. NATIVE plane (the thirteen relations of foundation/relation-payload-schemas.v2.json): the value is a DeficiencyV2 member produced by native-evidence.md section 4.6 `sufficiency_v2` for this requirement against the evidence Run named by evidenceRunId. IMPORTED plane (`runtime-observation`, `history-change`): the value is an ImportedRequirementDeficiency produced under imported-evidence.schema.json#/x-opensip-imported-requirement-law, because those relations mint no fact2 and have no Coverage entry, so sufficiency_v2 has nothing to range over and is not asked. A cross-plane value is REFUSED at admission: the two vocabularies are disjoint in meaning as well as in membership. THIS SCHEMA DELIBERATELY LEAVES THE AUTHORITATIVE REGISTRY LOOKUP TO ADMISSION: the oneOf admits either vocabulary on either relation, and admission decides the plane AND the imported KIND from registry membership. That is a choice about where the authority lives, not a limitation of JSON Schema - a schema can branch on a property's const/enum even where the base type is a broader string - and duplicating a registry as schema conditionals would create the drift this contract set avoids elsewhere. The schema also cannot fetch registry rows. WHAT THIS FIELD CARRIES: it is the satisfaction/deficiency PROJECTION of its producer's full result, not that result. `sufficiency_v2` also returns `causes` on both branches and may return `disclosures` on a failing branch. Those are PRODUCER RESULT ARRAYS, not fields of any retained record - not of CoverageResultV3, and some could not be, since the confidence floor lives in RequirementV2 and `required-relation-missing` has no Coverage entry. What is retained is the EVIDENCE the evaluation read - the coverage2 record with its own deficiency and nativeCause carrier, and the rest of the Run's closure - so nothing retained is dropped, and re-deriving the full result means re-running the evaluation over that evidence rather than reading a stored field. PRESENCE IS TYPED, NOT OPTIONAL: `deficiency` is REQUIRED exactly when `satisfied` is false and FORBIDDEN when it is true, enforced by the allOf below. `additionalProperties: false` plus that law means an explicit `null` is refused in BOTH branches - a present key with a null value is not an absent key - and `satisfied` must be an actual boolean. WHY NOT D9Deficiency, which this field named before: four of the nine native outcomes are not members of it, so the field could not express its own producer's result, and its D9-mapped value is the same `verdict-indeterminate` for all four - conflating `resolution-incomplete`, the outcome that decides a destructive unused-code repair, with three unrelated causes. D9Deficiency is unchanged and still carries every whole-Run and comparison-step termination. THIS FIELD IS NOT AN AUTHORIZATION: the sealed Run named by evidenceRunId remains the authority, `applicable` is false whenever any requirement is unsatisfied, EVERY delete and EVERY replace is decided against that Run's own native ClosedWorldV2 before any descriptor exists - which no imported requirement can change - and apply requires a security authorization bound to the exact repairPlanId, which every edit to this value moves.
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub deficiency: FieldPresence<
        ::std::option::Option<Repair2EvidenceRequirementDeficiency>,
    >,
    #[serde(rename = "minResolution")]
    pub min_resolution: Policy1Rung,
    pub relation: Common3CanonicalIdentifier,
    pub satisfied: bool,
}
///`Repair2EvidenceRequirementCompleteness`
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
pub enum Repair2EvidenceRequirementCompleteness {
    #[serde(rename = "complete")]
    Complete,
    #[serde(rename = "partial-acceptable")]
    PartialAcceptable,
}
impl ::std::fmt::Display for Repair2EvidenceRequirementCompleteness {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Complete => f.write_str("complete"),
            Self::PartialAcceptable => f.write_str("partial-acceptable"),
        }
    }
}
impl ::std::str::FromStr for Repair2EvidenceRequirementCompleteness {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "complete" => Ok(Self::Complete),
            "partial-acceptable" => Ok(Self::PartialAcceptable),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Repair2EvidenceRequirementCompleteness {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Repair2EvidenceRequirementCompleteness {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///The reason THIS requirement is unsatisfied, in the vocabulary of THIS requirement's evidence PLANE. Repair admits a requirement over either plane, so the field carries either vocabulary and the plane is decided AT ADMISSION from the relation's registry membership - never guessed from the value and never left to the reader. NATIVE plane (the thirteen relations of foundation/relation-payload-schemas.v2.json): the value is a DeficiencyV2 member produced by native-evidence.md section 4.6 `sufficiency_v2` for this requirement against the evidence Run named by evidenceRunId. IMPORTED plane (`runtime-observation`, `history-change`): the value is an ImportedRequirementDeficiency produced under imported-evidence.schema.json#/x-opensip-imported-requirement-law, because those relations mint no fact2 and have no Coverage entry, so sufficiency_v2 has nothing to range over and is not asked. A cross-plane value is REFUSED at admission: the two vocabularies are disjoint in meaning as well as in membership. THIS SCHEMA DELIBERATELY LEAVES THE AUTHORITATIVE REGISTRY LOOKUP TO ADMISSION: the oneOf admits either vocabulary on either relation, and admission decides the plane AND the imported KIND from registry membership. That is a choice about where the authority lives, not a limitation of JSON Schema - a schema can branch on a property's const/enum even where the base type is a broader string - and duplicating a registry as schema conditionals would create the drift this contract set avoids elsewhere. The schema also cannot fetch registry rows. WHAT THIS FIELD CARRIES: it is the satisfaction/deficiency PROJECTION of its producer's full result, not that result. `sufficiency_v2` also returns `causes` on both branches and may return `disclosures` on a failing branch. Those are PRODUCER RESULT ARRAYS, not fields of any retained record - not of CoverageResultV3, and some could not be, since the confidence floor lives in RequirementV2 and `required-relation-missing` has no Coverage entry. What is retained is the EVIDENCE the evaluation read - the coverage2 record with its own deficiency and nativeCause carrier, and the rest of the Run's closure - so nothing retained is dropped, and re-deriving the full result means re-running the evaluation over that evidence rather than reading a stored field. PRESENCE IS TYPED, NOT OPTIONAL: `deficiency` is REQUIRED exactly when `satisfied` is false and FORBIDDEN when it is true, enforced by the allOf below. `additionalProperties: false` plus that law means an explicit `null` is refused in BOTH branches - a present key with a null value is not an absent key - and `satisfied` must be an actual boolean. WHY NOT D9Deficiency, which this field named before: four of the nine native outcomes are not members of it, so the field could not express its own producer's result, and its D9-mapped value is the same `verdict-indeterminate` for all four - conflating `resolution-incomplete`, the outcome that decides a destructive unused-code repair, with three unrelated causes. D9Deficiency is unchanged and still carries every whole-Run and comparison-step termination. THIS FIELD IS NOT AN AUTHORIZATION: the sealed Run named by evidenceRunId remains the authority, `applicable` is false whenever any requirement is unsatisfied, EVERY delete and EVERY replace is decided against that Run's own native ClosedWorldV2 before any descriptor exists - which no imported requirement can change - and apply requires a security authorization bound to the exact repairPlanId, which every edit to this value moves.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(untagged)]
pub enum Repair2EvidenceRequirementDeficiency {
    NativeSufficiencyDeficiency(Common3NativeSufficiencyDeficiency),
    ImportedRequirementDeficiency(Common3ImportedRequirementDeficiency),
}
impl ::std::fmt::Display for Repair2EvidenceRequirementDeficiency {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match self {
            Self::NativeSufficiencyDeficiency(x) => x.fmt(f),
            Self::ImportedRequirementDeficiency(x) => x.fmt(f),
        }
    }
}
impl ::std::str::FromStr for Repair2EvidenceRequirementDeficiency {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if let Ok(v) = value.parse() {
            Ok(Self::NativeSufficiencyDeficiency(v))
        } else if let Ok(v) = value.parse() {
            Ok(Self::ImportedRequirementDeficiency(v))
        } else {
            Err("string conversion failed for all variants".into())
        }
    }
}
impl ::std::convert::TryFrom<&str> for Repair2EvidenceRequirementDeficiency {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Repair2EvidenceRequirementDeficiency {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::From<Common3NativeSufficiencyDeficiency>
for Repair2EvidenceRequirementDeficiency {
    fn from(value: Common3NativeSufficiencyDeficiency) -> Self {
        Self::NativeSufficiencyDeficiency(value)
    }
}
impl ::std::convert::From<Common3ImportedRequirementDeficiency>
for Repair2EvidenceRequirementDeficiency {
    fn from(value: Common3ImportedRequirementDeficiency) -> Self {
        Self::ImportedRequirementDeficiency(value)
    }
}
///`Repair2FileEdit`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Repair2FileEdit {
    pub action: Repair2FileEditAction,
    pub path: Common3LogicalPath,
    #[serde(rename = "postimageBytes")]
    pub postimage_bytes: i64,
    ///null only for action=delete
    #[serde(
        rename = "postimageDigest",
        deserialize_with = "::std::option::Option::deserialize"
    )]
    pub postimage_digest: ::std::option::Option<Common3Sha256Hex>,
    ///null only for action=create; otherwise must equal the snapshot inventory digest for path
    #[serde(
        rename = "preimageDigest",
        deserialize_with = "::std::option::Option::deserialize"
    )]
    pub preimage_digest: ::std::option::Option<Common3Sha256Hex>,
}
///`Repair2FileEditAction`
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
pub enum Repair2FileEditAction {
    #[serde(rename = "replace")]
    Replace,
    #[serde(rename = "delete")]
    Delete,
    #[serde(rename = "create")]
    Create,
}
impl ::std::fmt::Display for Repair2FileEditAction {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Replace => f.write_str("replace"),
            Self::Delete => f.write_str("delete"),
            Self::Create => f.write_str("create"),
        }
    }
}
impl ::std::str::FromStr for Repair2FileEditAction {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "replace" => Ok(Self::Replace),
            "delete" => Ok(Self::Delete),
            "create" => Ok(Self::Create),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Repair2FileEditAction {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Repair2FileEditAction {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Repair2FileOutcome`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Repair2FileOutcome {
    #[serde(deserialize_with = "::std::option::Option::deserialize")]
    pub after: ::std::option::Option<Common3Sha256Hex>,
    #[serde(deserialize_with = "::std::option::Option::deserialize")]
    pub before: ::std::option::Option<Common3Sha256Hex>,
    pub path: Common3LogicalPath,
    pub state: Repair2FileOutcomeState,
}
///`Repair2FileOutcomeState`
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
pub enum Repair2FileOutcomeState {
    #[serde(rename = "applied")]
    Applied,
    #[serde(rename = "restored")]
    Restored,
    #[serde(rename = "untouched")]
    Untouched,
    #[serde(rename = "blocked")]
    Blocked,
}
impl ::std::fmt::Display for Repair2FileOutcomeState {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Applied => f.write_str("applied"),
            Self::Restored => f.write_str("restored"),
            Self::Untouched => f.write_str("untouched"),
            Self::Blocked => f.write_str("blocked"),
        }
    }
}
impl ::std::str::FromStr for Repair2FileOutcomeState {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "applied" => Ok(Self::Applied),
            "restored" => Ok(Self::Restored),
            "untouched" => Ok(Self::Untouched),
            "blocked" => Ok(Self::Blocked),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Repair2FileOutcomeState {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Repair2FileOutcomeState {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///PREPARING: intent journaled, no temp written. STAGED: every postimage written to a same-directory temp, digest-verified, and every preimage re-verified against the live file. APPLYING: renames in progress in ascending UTF-8 path order; appliedPaths lists completed renames. APPLIED: every rename done, snapshot not yet recaptured. COMMITTED: appliedSnapshotId recorded and receipt written. FAILED_CLEAN: no target byte changed. FAILED_ROLLED_BACK: every renamed target restored to its preimage. RECOVERY_BLOCKED: a renamed target is neither preimage nor postimage; no automatic action. INDETERMINATE: applied but post-apply tree identity could not be established.
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
pub enum Repair2JournalState {
    #[serde(rename = "PREPARING")]
    Preparing,
    #[serde(rename = "STAGED")]
    Staged,
    #[serde(rename = "APPLYING")]
    Applying,
    #[serde(rename = "APPLIED")]
    Applied,
    #[serde(rename = "COMMITTED")]
    Committed,
    #[serde(rename = "FAILED_CLEAN")]
    FailedClean,
    #[serde(rename = "FAILED_ROLLED_BACK")]
    FailedRolledBack,
    #[serde(rename = "RECOVERY_BLOCKED")]
    RecoveryBlocked,
    #[serde(rename = "INDETERMINATE")]
    Indeterminate,
}
impl ::std::fmt::Display for Repair2JournalState {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Preparing => f.write_str("PREPARING"),
            Self::Staged => f.write_str("STAGED"),
            Self::Applying => f.write_str("APPLYING"),
            Self::Applied => f.write_str("APPLIED"),
            Self::Committed => f.write_str("COMMITTED"),
            Self::FailedClean => f.write_str("FAILED_CLEAN"),
            Self::FailedRolledBack => f.write_str("FAILED_ROLLED_BACK"),
            Self::RecoveryBlocked => f.write_str("RECOVERY_BLOCKED"),
            Self::Indeterminate => f.write_str("INDETERMINATE"),
        }
    }
}
impl ::std::str::FromStr for Repair2JournalState {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "PREPARING" => Ok(Self::Preparing),
            "STAGED" => Ok(Self::Staged),
            "APPLYING" => Ok(Self::Applying),
            "APPLIED" => Ok(Self::Applied),
            "COMMITTED" => Ok(Self::Committed),
            "FAILED_CLEAN" => Ok(Self::FailedClean),
            "FAILED_ROLLED_BACK" => Ok(Self::FailedRolledBack),
            "RECOVERY_BLOCKED" => Ok(Self::RecoveryBlocked),
            "INDETERMINATE" => Ok(Self::Indeterminate),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Repair2JournalState {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Repair2JournalState {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///The closed effect-class vocabulary of a mutating step. Which operation each STEP KIND writes to its required receipt is published beside this enum at #/x-opensip-mutation-operation-map/byStepKindReceiptOperation, and which operation each current command's generic `mutation` step emits is at #/x-opensip-mutation-operation-map/byCommandGenericMutationStep; four commands do NOT share their operation's name, so name matching is not the derivation, and `import` is emitted by two commands, so the map is not invertible. Neither map is the admissible domain of the generic operation field: #/x-opensip-mutation-operation-map/admissibleGenericFieldDomain is, and it is every member here except `repair-apply`. `config-write` is the one member no step kind binds.
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
pub enum Repair2MutationOperation {
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
impl ::std::fmt::Display for Repair2MutationOperation {
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
impl ::std::str::FromStr for Repair2MutationOperation {
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
impl ::std::convert::TryFrom<&str> for Repair2MutationOperation {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Repair2MutationOperation {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Retained record of an attempted host mutation. Retained even when the effect FAILED or a later verification failed. receiptId = 'receipt2:' + H('workflow.mutation-receipt', this object without receiptId).
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Repair2MutationReceiptV1 {
    #[serde(
        rename = "appliedSnapshotId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub applied_snapshot_id: FieldPresence<::std::option::Option<Common3SnapshotId>>,
    #[serde(
        rename = "baseSnapshotId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub base_snapshot_id: FieldPresence<::std::option::Option<Common3SnapshotId>>,
    #[serde(rename = "commitClass")]
    pub commit_class: Repair2MutationReceiptV1CommitClass,
    #[serde(
        rename = "domainDetail",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub domain_detail: FieldPresence<::std::option::Option<Common3DomainDetail>>,
    #[serde(rename = "effectOutcome")]
    pub effect_outcome: Repair2MutationReceiptV1EffectOutcome,
    #[serde(rename = "executionId")]
    pub execution_id: Common3ExecutionId,
    #[serde(
        rename = "fileOutcomes",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub file_outcomes: FieldPresence<::std::vec::Vec<Repair2FileOutcome>>,
    #[serde(rename = "idempotencyKey")]
    pub idempotency_key: Common3Sha256Hex,
    pub operation: Repair2MutationOperation,
    #[serde(rename = "receiptId")]
    pub receipt_id: Common3ReceiptId,
    #[serde(
        rename = "repairPlanId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub repair_plan_id: FieldPresence<::std::option::Option<Common3RepairPlanId>>,
    ///true when an equal idempotencyKey already had a COMPLETED receipt and no second effect was performed
    pub replayed: bool,
    #[serde(rename = "requestId")]
    pub request_id: Common3RequestId,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub rollback: FieldPresence<::std::option::Option<Repair2MutationReceiptV1Rollback>>,
    #[serde(rename = "schemaFamily")]
    pub schema_family: ::serde_json::Value,
    #[serde(rename = "schemaMajor")]
    pub schema_major: ExactInteger,
    #[serde(rename = "stepId")]
    pub step_id: Common3StepId,
}
///`Repair2MutationReceiptV1CommitClass`
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
pub enum Repair2MutationReceiptV1CommitClass {
    #[serde(rename = "REVERSIBLE")]
    Reversible,
    #[serde(rename = "IRREVERSIBLE")]
    Irreversible,
}
impl ::std::fmt::Display for Repair2MutationReceiptV1CommitClass {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Reversible => f.write_str("REVERSIBLE"),
            Self::Irreversible => f.write_str("IRREVERSIBLE"),
        }
    }
}
impl ::std::str::FromStr for Repair2MutationReceiptV1CommitClass {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "REVERSIBLE" => Ok(Self::Reversible),
            "IRREVERSIBLE" => Ok(Self::Irreversible),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Repair2MutationReceiptV1CommitClass {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Repair2MutationReceiptV1CommitClass {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Repair2MutationReceiptV1EffectOutcome`
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
pub enum Repair2MutationReceiptV1EffectOutcome {
    #[serde(rename = "COMPLETED")]
    Completed,
    #[serde(rename = "FAILED")]
    Failed,
    #[serde(rename = "INDETERMINATE")]
    Indeterminate,
}
impl ::std::fmt::Display for Repair2MutationReceiptV1EffectOutcome {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Completed => f.write_str("COMPLETED"),
            Self::Failed => f.write_str("FAILED"),
            Self::Indeterminate => f.write_str("INDETERMINATE"),
        }
    }
}
impl ::std::str::FromStr for Repair2MutationReceiptV1EffectOutcome {
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
impl ::std::convert::TryFrom<&str> for Repair2MutationReceiptV1EffectOutcome {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Repair2MutationReceiptV1EffectOutcome {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Repair2MutationReceiptV1Rollback`
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
pub enum Repair2MutationReceiptV1Rollback {
    #[serde(rename = "not-needed")]
    NotNeeded,
    #[serde(rename = "completed")]
    Completed,
    #[serde(rename = "blocked")]
    Blocked,
    #[serde(rename = "not-attempted")]
    NotAttempted,
}
impl ::std::fmt::Display for Repair2MutationReceiptV1Rollback {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::NotNeeded => f.write_str("not-needed"),
            Self::Completed => f.write_str("completed"),
            Self::Blocked => f.write_str("blocked"),
            Self::NotAttempted => f.write_str("not-attempted"),
        }
    }
}
impl ::std::str::FromStr for Repair2MutationReceiptV1Rollback {
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
impl ::std::convert::TryFrom<&str> for Repair2MutationReceiptV1Rollback {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Repair2MutationReceiptV1Rollback {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Repair2RecipeRef`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Repair2RecipeRef {
    ///exact signed contribution closure that supplied the recipe; revocation of this closure under current trust invalidates apply (REPAIR.RECIPE_TRUST_REVOKED)
    #[serde(rename = "closureId")]
    pub closure_id: Common3ClosureId,
    #[serde(rename = "contributionId")]
    pub contribution_id: Common3ContributionId,
    #[serde(rename = "recipeId")]
    pub recipe_id: Common3CanonicalIdentifier,
    #[serde(rename = "recipeVersion")]
    pub recipe_version: Common3SemanticVersion,
}
///Closed decision-table row for repair-recover given a journal state and the observed live digests. Inspection (state, journal integrity, per-path digest comparison) is read-only and needs no authorization. Any action other than none/refuse is a separately authorized mutation within the ORIGINAL plan's authority (same repairPlanId, same base snapshot, same project); it never re-applies an edit and never touches a path outside the plan. roll-back-renamed: for every applied path the current digest must equal the plan postimage (or be absent for create) before the retained preimage blob is restored; any other digest is RECOVERY_BLOCKED. verify-postimages-and-commit (APPLIED/INDETERMINATE): every intended edit's current digest must equal its plan postimage (absent for delete) AND appliedPaths must equal the plan's edit paths; only then is the tree re-snapshotted and committed — an unexpected user edit is RECOVERY_BLOCKED, never silently committed. requires-broker: the retained preimage blob is unavailable to this process; the model returns the exact restore intent and changes nothing.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Repair2RecoveryAction {
    pub action: Repair2RecoveryActionAction,
    #[serde(rename = "receiptOutcome")]
    pub receipt_outcome: Repair2RecoveryActionReceiptOutcome,
    #[serde(rename = "resultState")]
    pub result_state: Repair2JournalState,
    pub state: Repair2JournalState,
}
///`Repair2RecoveryActionAction`
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
pub enum Repair2RecoveryActionAction {
    #[serde(rename = "discard-temps")]
    DiscardTemps,
    #[serde(rename = "roll-back-renamed")]
    RollBackRenamed,
    #[serde(rename = "verify-postimages-and-commit")]
    VerifyPostimagesAndCommit,
    #[serde(rename = "none")]
    None,
    #[serde(rename = "refuse")]
    Refuse,
    #[serde(rename = "requires-broker")]
    RequiresBroker,
}
impl ::std::fmt::Display for Repair2RecoveryActionAction {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::DiscardTemps => f.write_str("discard-temps"),
            Self::RollBackRenamed => f.write_str("roll-back-renamed"),
            Self::VerifyPostimagesAndCommit => {
                f.write_str("verify-postimages-and-commit")
            }
            Self::None => f.write_str("none"),
            Self::Refuse => f.write_str("refuse"),
            Self::RequiresBroker => f.write_str("requires-broker"),
        }
    }
}
impl ::std::str::FromStr for Repair2RecoveryActionAction {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "discard-temps" => Ok(Self::DiscardTemps),
            "roll-back-renamed" => Ok(Self::RollBackRenamed),
            "verify-postimages-and-commit" => Ok(Self::VerifyPostimagesAndCommit),
            "none" => Ok(Self::None),
            "refuse" => Ok(Self::Refuse),
            "requires-broker" => Ok(Self::RequiresBroker),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Repair2RecoveryActionAction {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Repair2RecoveryActionAction {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Repair2RecoveryActionReceiptOutcome`
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
pub enum Repair2RecoveryActionReceiptOutcome {
    #[serde(rename = "COMPLETED")]
    Completed,
    #[serde(rename = "FAILED")]
    Failed,
    #[serde(rename = "INDETERMINATE")]
    Indeterminate,
}
impl ::std::fmt::Display for Repair2RecoveryActionReceiptOutcome {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Completed => f.write_str("COMPLETED"),
            Self::Failed => f.write_str("FAILED"),
            Self::Indeterminate => f.write_str("INDETERMINATE"),
        }
    }
}
impl ::std::str::FromStr for Repair2RecoveryActionReceiptOutcome {
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
impl ::std::convert::TryFrom<&str> for Repair2RecoveryActionReceiptOutcome {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Repair2RecoveryActionReceiptOutcome {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///SC-OPS journal under projects/<namespaceId>/repair/<requestId>-<stepId>.json; operational, never in any content identity.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Repair2RepairApplyJournalV1 {
    #[serde(rename = "appliedPaths")]
    pub applied_paths: ::std::vec::Vec<Common3LogicalPath>,
    #[serde(
        rename = "appliedSnapshotId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub applied_snapshot_id: FieldPresence<::std::option::Option<Common3SnapshotId>>,
    #[serde(rename = "authorizationRef")]
    pub authorization_ref: Common3RepairAuthorizationRef,
    #[serde(rename = "baseSnapshotId")]
    pub base_snapshot_id: Common3SnapshotId,
    #[serde(
        rename = "blockedPaths",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub blocked_paths: FieldPresence<
        ::std::option::Option<::std::vec::Vec<Common3LogicalPath>>,
    >,
    #[serde(rename = "executionId")]
    pub execution_id: Common3ExecutionId,
    #[serde(
        rename = "faultCause",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub fault_cause: FieldPresence<::std::option::Option<Common3D9FaultCause>>,
    ///retained preimage bytes (digest-addressed, written before STAGED) for every replace/delete edit; rollback restores from these blobs, never from memory
    #[serde(
        rename = "preimageBlobs",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub preimage_blobs: FieldPresence<
        ::std::option::Option<::std::vec::Vec<Common3Blob>>,
    >,
    ///Full actual security-admitted fresh recovery authorization; identity and observed state are bound to the original journal.
    #[serde(
        rename = "recoveryAuthorizationRef",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub recovery_authorization_ref: FieldPresence<
        ::std::option::Option<Common3RepairRecoveryAuthorizationRef>,
    >,
    #[serde(rename = "repairPlanId")]
    pub repair_plan_id: Common3RepairPlanId,
    #[serde(rename = "requestId")]
    pub request_id: Common3RequestId,
    #[serde(
        rename = "restoreIntent",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub restore_intent: FieldPresence<
        ::std::vec::Vec<Repair2RepairApplyJournalV1RestoreIntentItem>,
    >,
    #[serde(rename = "schemaFamily")]
    pub schema_family: ::serde_json::Value,
    #[serde(rename = "schemaMajor")]
    pub schema_major: ExactInteger,
    #[serde(rename = "stagedPaths")]
    pub staged_paths: ::std::vec::Vec<Common3LogicalPath>,
    pub state: Repair2JournalState,
    #[serde(rename = "stepId")]
    pub step_id: Common3StepId,
}
///`Repair2RepairApplyJournalV1RestoreIntentItem`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Repair2RepairApplyJournalV1RestoreIntentItem {
    pub path: Common3LogicalPath,
    #[serde(
        rename = "restoreDigest",
        deserialize_with = "::std::option::Option::deserialize"
    )]
    pub restore_digest: ::std::option::Option<Common3Sha256Hex>,
}
///Identity-bearing descriptor for H('workflow.repair-plan', descriptor). No operational field is admitted here. Evaluator3: schemaMajor 2 because evidenceRunId is run3 (identity-bearing). Targets remain finding-key2 fingerprints. Unmatched findings are not lawful targets (REPAIR.TARGET_CORRESPONDENCE_UNAVAILABLE). Multiple configurations sharing one fingerprint must have compatible metadata or refuse REPAIR.TARGET_METADATA_AMBIGUOUS; parameter bytes are not collapsed. No automatic source edit.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Repair2RepairPlanDescriptor {
    ///true only when every evidenceRequirement is satisfied and unmetPreconditions is empty
    pub applicable: bool,
    #[serde(rename = "closedWorld")]
    pub closed_world: Repair2RepairPlanDescriptorClosedWorld,
    ///sorted ascending by path UTF-8 bytes; path unique
    pub edits: ::std::vec::Vec<Repair2FileEdit>,
    ///how the evidence Run's facts for the target relations were produced. imported-prepared-declared (a declared proc-macro/build expansion imported without verified provenance) is never authority for an unsafe (delete/replace) repair.
    #[serde(rename = "evidenceOrigin")]
    pub evidence_origin: Repair2RepairPlanDescriptorEvidenceOrigin,
    #[serde(rename = "evidenceRequirements")]
    pub evidence_requirements: ::std::vec::Vec<Repair2EvidenceRequirement>,
    #[serde(rename = "evidenceRunId")]
    pub evidence_run_id: Common3RunId,
    pub limitations: ::std::vec::Vec<Common3BoundedText>,
    #[serde(rename = "permittedEditScope")]
    pub permitted_edit_scope: ::std::vec::Vec<Common3GlobPattern>,
    #[serde(rename = "planId")]
    pub plan_id: Common3PlanId,
    #[serde(rename = "projectId")]
    pub project_id: Common3ProjectId,
    pub recipe: Repair2RecipeRef,
    ///positive current-trust disposition of recipe.closureId at preview: only 'admitted' (present in the current admitted closure set) is applicable; 'not-admitted' (absent) is REPAIR.RECIPE_TRUST_NOT_ADMITTED, 'revoked' is REPAIR.RECIPE_TRUST_REVOKED. Absence of a revocation is never admission.
    #[serde(rename = "recipeTrust")]
    pub recipe_trust: Repair2RepairPlanDescriptorRecipeTrust,
    #[serde(rename = "schemaFamily")]
    pub schema_family: ::serde_json::Value,
    #[serde(rename = "schemaMajor")]
    pub schema_major: ExactInteger,
    #[serde(rename = "snapshotId")]
    pub snapshot_id: Common3SnapshotId,
    pub targets: ::std::vec::Vec<Common3Fingerprint>,
    #[serde(rename = "totalPostimageBytes")]
    pub total_postimage_bytes: i64,
    #[serde(rename = "unmetPreconditions")]
    pub unmet_preconditions: ::std::vec::Vec<Common3DomainDetail>,
}
///AUTHOR_PENDING_REVIEW. The deterministic five-field DISPLAY SUMMARY of the native ClosedWorldV2 records that the workflows-and-surfaces section 6 SELECTION LAW selected from the evidence Run - NOT a copy, NOT a projection of one record, and NOT itself a native producer record. WHY A SUMMARY AND NOT A COPY: ClosedWorldV2 is a required member of ViewEntryV3 (native-evidence.md section 4.3), so a Run retains ONE PER COVERAGE ENTRY keyed by CoverageKeyV2, and identity-and-evidence.md section 3 makes several differing entries lawful in one Run. There is no Run-level ClosedWorldV2 to copy. ClosedWorldV2 is closed at SEVEN required members and a literal copy is REFUSED here (dynamicDispatch and reasons are not properties of this record). RELEVANT UNIVERSES: every universe reached by ALL matching occurrences of EVERY target fingerprint (finding3.subjectId -> subject3.universe) UNION every universe that owns an unsafe edited path in the RETAINED SELECTED-PROGRAM CENSUS of this Run's EnumerationPlanV1. That parameter is REQUIRED for evaluator3 (absent it refuses EVALUATOR_REQUIRED_PARAMETER_MISSING and full replay re-admits it), so the join is guaranteed and retained - never a caller-selected or optional unsigned map, never filename parsing. For each binding whose enumerator.status is `selected`, its applicable path census is its own extents[] per kind plus, on a candidate-only cell, candidateSourcePaths. A binding with a NON-NULL universe whose census contains the path contributes that universe. A SELECTED but UNAVAILABLE binding (universe=null, extents still populated from host membership) contributes TYPED UNRESOLVED OWNERSHIP: REPAIR.CLOSED_WORLD_NOT_ESTABLISHED that does NOT vanish because another owner of the same path is closed. An UNSELECTED binding is never inferred as an owner. Each extent kind is read as itself: file and package are host membership extents, symbol is the selected program's CODE scope, so all snapshot files are NOT treated as every compiler's programRootFiles and a selected program whose own census lacks the edit stays UNRELATED. Multiple ownership is preserved (one path under two Rust targets or editions is two bindings and both must be eligible). Retained source-path subject scopes (file, clones, vcs-change, all universeRule same-only) are an ADDITIONAL retained witness only: their subjectKindLaw proves those scopes NAME paths, not that they ENUMERATE every selected program owning one, and a universe bound only to a symbol-kind cell - owning a path through its retained symbol extent, with no file inventory and no lawful file@enumerated scope - is admitted. No path is reconstructed from an opaque native symbol ID; the census publishes the program's path extent directly. SELECTED RECORDS: EVERY retained native coverage2 whose scope sourceUniverse is relevant - independent of evidenceRequirements, so a recipe can neither pick a favourable relation or rung nor drop a conflicting record - deduplicated by retained coverage2 identity and ORDERED ON UTF-8 ENCODED BYTES by relation, resolution, sourceUniverse, targetUniverse, subjectScopeCommitment, then the coverage2 identity, which makes the order total even between two records agreeing on all five coordinates. GATE: eligibility for EVERY delete and EVERY replace in the plan is the NON-VACUOUS CONJUNCTION of deadCodeRepairEligible over those selected records, decided BEFORE this record is built. A relevant universe with no retained native Coverage, an unsafe path with no reconstructable owner, and an unresolved unavailable-binding ownership are each REPAIR.CLOSED_WORLD_NOT_ESTABLISHED - an empty evidence subset is not truth and no evidence is guessed. Each dissent remedy names ALL SIX ordering members UNABBREVIATED, including the exact retained coverage2 identity, because two lawfully distinct records can differ only in targetUniverse, only in subjectScopeCommitment, or only in the identity. Imported observations neither establish nor improve this gate; only native coverage2 records are selected. dynamicDispatch is NOT read by this gate and is NOT a global veto: native section 4.5 affected_targets and section 4.6 sufficiency_v2 keep dynamic-edge effects target-relative and per-requirement, and those judgements stay separate from this boolean. REDUCTION: deadCodeRepairEligible is the conjunction; each other member takes the LEAST-CLOSED value present (closed<open<unknown, all<partial<none, none<present, none-declared<possible<unknown); and ABSENCE IS FOLDED IN, so a relevant universe with no Coverage or an unresolved ownership also opens the summary instead of hiding behind the records that do exist. With nothing selected the same rule yields the FIVE-FIELD LEAST-CLOSED DISPLAY SENTINEL {deadCodeRepairEligible:false, exportsClosed:unknown, entryPointsRecognized:none, nonliteralLoading:present, externalConsumers:unknown}. That is NOT an all-unknown record: only two members are unknown, the other three being a false boolean and the least-closed pole of each enum that cannot spell absence. A create-only plan activates no gate and an ineligible closed world alone adds NO unmet precondition to it, but it still READS the selection and still BUILDS this required member, so the descriptor and therefore repairPlanId stay deterministic. AUTHORITY: this record has NONE, and NO MEMBER OF IT IS AUTHORITATIVE, the boolean included. It is a descriptor member carried for display and for the repairPlanId preimage, and it is never the input to the gate, which reads the full selected records including the two members this one does not carry. Editing a field here cannot bypass anything: a missing required member is schema-invalid, any edit mints a different repairPlanId, and apply requires a security authorization bound to the exact repairPlanId, base snapshot and project. Recipe trust, policy consent and current-snapshot equality remain separately required, and preview is a Query-class step that authorizes nothing. IDENTITY: this member's SHAPE and the repairPlanId RECIPE are unchanged; its VALUE may differ from an implementation that used a caller-selected record, so the minted repairPlanId may differ. NO repairPlanId equality is claimed across different evidenceRunIds - evidenceRunId is in the preimage, so a different Run is a different plan identity however similar its evidence.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Repair2RepairPlanDescriptorClosedWorld {
    #[serde(rename = "deadCodeRepairEligible")]
    pub dead_code_repair_eligible: bool,
    #[serde(rename = "entryPointsRecognized")]
    pub entry_points_recognized: Repair2RepairPlanDescriptorClosedWorldEntryPointsRecognized,
    #[serde(rename = "exportsClosed")]
    pub exports_closed: Repair2RepairPlanDescriptorClosedWorldExportsClosed,
    #[serde(rename = "externalConsumers")]
    pub external_consumers: Repair2RepairPlanDescriptorClosedWorldExternalConsumers,
    #[serde(rename = "nonliteralLoading")]
    pub nonliteral_loading: Repair2RepairPlanDescriptorClosedWorldNonliteralLoading,
}
///`Repair2RepairPlanDescriptorClosedWorldEntryPointsRecognized`
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
pub enum Repair2RepairPlanDescriptorClosedWorldEntryPointsRecognized {
    #[serde(rename = "all")]
    All,
    #[serde(rename = "partial")]
    Partial,
    #[serde(rename = "none")]
    None,
}
impl ::std::fmt::Display
for Repair2RepairPlanDescriptorClosedWorldEntryPointsRecognized {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::All => f.write_str("all"),
            Self::Partial => f.write_str("partial"),
            Self::None => f.write_str("none"),
        }
    }
}
impl ::std::str::FromStr
for Repair2RepairPlanDescriptorClosedWorldEntryPointsRecognized {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "all" => Ok(Self::All),
            "partial" => Ok(Self::Partial),
            "none" => Ok(Self::None),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str>
for Repair2RepairPlanDescriptorClosedWorldEntryPointsRecognized {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Repair2RepairPlanDescriptorClosedWorldEntryPointsRecognized {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Repair2RepairPlanDescriptorClosedWorldExportsClosed`
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
pub enum Repair2RepairPlanDescriptorClosedWorldExportsClosed {
    #[serde(rename = "closed")]
    Closed,
    #[serde(rename = "open")]
    Open,
    #[serde(rename = "unknown")]
    Unknown,
}
impl ::std::fmt::Display for Repair2RepairPlanDescriptorClosedWorldExportsClosed {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Closed => f.write_str("closed"),
            Self::Open => f.write_str("open"),
            Self::Unknown => f.write_str("unknown"),
        }
    }
}
impl ::std::str::FromStr for Repair2RepairPlanDescriptorClosedWorldExportsClosed {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "closed" => Ok(Self::Closed),
            "open" => Ok(Self::Open),
            "unknown" => Ok(Self::Unknown),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str>
for Repair2RepairPlanDescriptorClosedWorldExportsClosed {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Repair2RepairPlanDescriptorClosedWorldExportsClosed {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Repair2RepairPlanDescriptorClosedWorldExternalConsumers`
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
pub enum Repair2RepairPlanDescriptorClosedWorldExternalConsumers {
    #[serde(rename = "none-declared")]
    NoneDeclared,
    #[serde(rename = "possible")]
    Possible,
    #[serde(rename = "unknown")]
    Unknown,
}
impl ::std::fmt::Display for Repair2RepairPlanDescriptorClosedWorldExternalConsumers {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::NoneDeclared => f.write_str("none-declared"),
            Self::Possible => f.write_str("possible"),
            Self::Unknown => f.write_str("unknown"),
        }
    }
}
impl ::std::str::FromStr for Repair2RepairPlanDescriptorClosedWorldExternalConsumers {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "none-declared" => Ok(Self::NoneDeclared),
            "possible" => Ok(Self::Possible),
            "unknown" => Ok(Self::Unknown),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str>
for Repair2RepairPlanDescriptorClosedWorldExternalConsumers {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Repair2RepairPlanDescriptorClosedWorldExternalConsumers {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Repair2RepairPlanDescriptorClosedWorldNonliteralLoading`
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
pub enum Repair2RepairPlanDescriptorClosedWorldNonliteralLoading {
    #[serde(rename = "none")]
    None,
    #[serde(rename = "present")]
    Present,
}
impl ::std::fmt::Display for Repair2RepairPlanDescriptorClosedWorldNonliteralLoading {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::None => f.write_str("none"),
            Self::Present => f.write_str("present"),
        }
    }
}
impl ::std::str::FromStr for Repair2RepairPlanDescriptorClosedWorldNonliteralLoading {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "none" => Ok(Self::None),
            "present" => Ok(Self::Present),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str>
for Repair2RepairPlanDescriptorClosedWorldNonliteralLoading {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Repair2RepairPlanDescriptorClosedWorldNonliteralLoading {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///how the evidence Run's facts for the target relations were produced. imported-prepared-declared (a declared proc-macro/build expansion imported without verified provenance) is never authority for an unsafe (delete/replace) repair.
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
pub enum Repair2RepairPlanDescriptorEvidenceOrigin {
    #[serde(rename = "native-analysis")]
    NativeAnalysis,
    #[serde(rename = "imported-prepared-verified")]
    ImportedPreparedVerified,
    #[serde(rename = "imported-prepared-declared")]
    ImportedPreparedDeclared,
}
impl ::std::fmt::Display for Repair2RepairPlanDescriptorEvidenceOrigin {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::NativeAnalysis => f.write_str("native-analysis"),
            Self::ImportedPreparedVerified => f.write_str("imported-prepared-verified"),
            Self::ImportedPreparedDeclared => f.write_str("imported-prepared-declared"),
        }
    }
}
impl ::std::str::FromStr for Repair2RepairPlanDescriptorEvidenceOrigin {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "native-analysis" => Ok(Self::NativeAnalysis),
            "imported-prepared-verified" => Ok(Self::ImportedPreparedVerified),
            "imported-prepared-declared" => Ok(Self::ImportedPreparedDeclared),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Repair2RepairPlanDescriptorEvidenceOrigin {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Repair2RepairPlanDescriptorEvidenceOrigin {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///positive current-trust disposition of recipe.closureId at preview: only 'admitted' (present in the current admitted closure set) is applicable; 'not-admitted' (absent) is REPAIR.RECIPE_TRUST_NOT_ADMITTED, 'revoked' is REPAIR.RECIPE_TRUST_REVOKED. Absence of a revocation is never admission.
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
pub enum Repair2RepairPlanDescriptorRecipeTrust {
    #[serde(rename = "admitted")]
    Admitted,
    #[serde(rename = "not-admitted")]
    NotAdmitted,
    #[serde(rename = "revoked")]
    Revoked,
}
impl ::std::fmt::Display for Repair2RepairPlanDescriptorRecipeTrust {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Admitted => f.write_str("admitted"),
            Self::NotAdmitted => f.write_str("not-admitted"),
            Self::Revoked => f.write_str("revoked"),
        }
    }
}
impl ::std::str::FromStr for Repair2RepairPlanDescriptorRecipeTrust {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "admitted" => Ok(Self::Admitted),
            "not-admitted" => Ok(Self::NotAdmitted),
            "revoked" => Ok(Self::Revoked),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Repair2RepairPlanDescriptorRecipeTrust {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Repair2RepairPlanDescriptorRecipeTrust {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Repair2RepairPlanV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Repair2RepairPlanV1 {
    pub descriptor: Repair2RepairPlanDescriptor,
    #[serde(rename = "repairPlanId")]
    pub repair_plan_id: Common3RepairPlanId,
}
///Preview, apply and verify are three separately authorized steps. A RepairPlan is a content-identified, snapshot-bound, non-applying artifact (H('workflow.repair-plan', descriptor)); it requires an AUTHORITATIVE evidence Run whose availability is retained and whose sealed assurance is replayable. Apply is a host-owned mutation bound to the exact repairPlanId and snapshotId with a journaled same-directory-temp/rename protocol, per-file preimage verification and rollback. Verify always admits a fresh snapshot after apply and seals a new authoritative Run; it never reuses the pre-apply Run. Identity descriptors exclude RequestId, ExecutionId, clocks and receipts. Bounds: at most 4096 target files, at most 16 MiB per postimage, at most 64 MiB total postimage bytes per plan.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(transparent)]
pub struct Repair2Root(pub ::serde_json::Value);
impl ::std::ops::Deref for Repair2Root {
    type Target = ::serde_json::Value;
    fn deref(&self) -> &::serde_json::Value {
        &self.0
    }
}
impl ::std::convert::From<Repair2Root> for ::serde_json::Value {
    fn from(value: Repair2Root) -> Self {
        value.0
    }
}
impl ::std::convert::From<::serde_json::Value> for Repair2Root {
    fn from(value: ::serde_json::Value) -> Self {
        Self(value)
    }
}
///Append-only link from an immutable apply receipt to a later verification Run. A MutationReceiptV1 is content-identified and can never be edited to add a verificationRunId; the link is a separate retained record. linkId = 'receipt2:' + H('workflow.verification-link', this object without linkId).
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Repair2VerificationLinkV1 {
    #[serde(rename = "appliedSnapshotId")]
    pub applied_snapshot_id: Common3SnapshotId,
    #[serde(rename = "linkId")]
    pub link_id: Common3ReceiptId,
    #[serde(rename = "receiptId")]
    pub receipt_id: Common3ReceiptId,
    #[serde(rename = "requestId")]
    pub request_id: Common3RequestId,
    #[serde(rename = "schemaFamily")]
    pub schema_family: ::serde_json::Value,
    #[serde(rename = "schemaMajor")]
    pub schema_major: ExactInteger,
    #[serde(rename = "stepId")]
    pub step_id: Common3StepId,
    #[serde(rename = "verificationRunId")]
    pub verification_run_id: Common3RunId,
    #[serde(rename = "verifiedSnapshotId")]
    pub verified_snapshot_id: Common3SnapshotId,
}
///Sum of terminal attempt service observations, never step wall time. Exact source/ExecutionId/summary and unrecorded reason joins are mandatory.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(untagged, deny_unknown_fields)]
pub enum Report1AttemptServiceTimeV1 {
    Variant0 {
        #[serde(rename = "attemptCount")]
        attempt_count: ExactInteger,
        state: ::serde_json::Value,
    },
    Variant1 {
        #[serde(rename = "attemptCount")]
        attempt_count: ::std::num::NonZeroU64,
        milliseconds: u64,
        state: ::serde_json::Value,
    },
    Variant2 {
        #[serde(rename = "attemptCount")]
        attempt_count: ::std::num::NonZeroU64,
        reason: ::serde_json::Value,
        state: ::serde_json::Value,
        #[serde(rename = "unavailableAttemptCount")]
        unavailable_attempt_count: ::std::num::NonZeroU64,
    },
    Variant3 {
        #[serde(rename = "attemptCount")]
        attempt_count: ::std::num::NonZeroU64,
        reason: ::serde_json::Value,
        state: ::serde_json::Value,
        #[serde(rename = "unavailableAttemptCount")]
        unavailable_attempt_count: ExactInteger,
    },
    Variant4 {
        reason: Report1AttemptServiceTimeV1Variant4Reason,
        state: ::serde_json::Value,
    },
}
///`Report1AttemptServiceTimeV1Variant4Reason`
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
pub enum Report1AttemptServiceTimeV1Variant4Reason {
    #[serde(rename = "render-in-progress")]
    RenderInProgress,
    #[serde(rename = "step-result-not-recorded")]
    StepResultNotRecorded,
}
impl ::std::fmt::Display for Report1AttemptServiceTimeV1Variant4Reason {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::RenderInProgress => f.write_str("render-in-progress"),
            Self::StepResultNotRecorded => f.write_str("step-result-not-recorded"),
        }
    }
}
impl ::std::str::FromStr for Report1AttemptServiceTimeV1Variant4Reason {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "render-in-progress" => Ok(Self::RenderInProgress),
            "step-result-not-recorded" => Ok(Self::StepResultNotRecorded),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1AttemptServiceTimeV1Variant4Reason {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Report1AttemptServiceTimeV1Variant4Reason {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Report1AutomaticHistoryPanelV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1AutomaticHistoryPanelV1 {
    pub provenance: Report1AutomaticHistoryPanelV1Provenance,
    pub runs: ::std::vec::Vec<Report1HistoryRunV1>,
    pub selection: Report1AutomaticHistoryPanelV1Selection,
}
///`Report1AutomaticHistoryPanelV1Provenance`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1AutomaticHistoryPanelV1Provenance {
    #[serde(rename = "hostAsserted")]
    pub host_asserted: ::serde_json::Value,
    #[serde(rename = "verifiedInDocument")]
    pub verified_in_document: ::serde_json::Value,
}
///`Report1AutomaticHistoryPanelV1Selection`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1AutomaticHistoryPanelV1Selection {
    #[serde(
        rename = "baselineId",
        deserialize_with = "::std::option::Option::deserialize"
    )]
    pub baseline_id: ::std::option::Option<Common4BaselineId>,
    #[serde(
        rename = "baselineSourceRunId",
        deserialize_with = "::std::option::Option::deserialize"
    )]
    pub baseline_source_run_id: ::std::option::Option<Common4RunId>,
    #[serde(rename = "currentCommitSequence")]
    pub current_commit_sequence: u64,
    pub policy: ::serde_json::Value,
    #[serde(rename = "priorRuns")]
    pub prior_runs: ::std::vec::Vec<
        Report1AutomaticHistoryPanelV1SelectionPriorRunsItem,
    >,
    #[serde(rename = "priorRunsInSnapshot")]
    pub prior_runs_in_snapshot: Common4Uint53,
    #[serde(rename = "requestedRunIds")]
    pub requested_run_ids: ::std::vec::Vec<Common4RunId>,
}
///`Report1AutomaticHistoryPanelV1SelectionPriorRunsItem`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1AutomaticHistoryPanelV1SelectionPriorRunsItem {
    #[serde(rename = "commitSequence")]
    pub commit_sequence: u64,
    #[serde(rename = "runId")]
    pub run_id: Common4RunId,
}
///Development caps derived from owner schemas, the exact codec and per-command ledger step counts (contract section 9). Not measured performance or release qualification.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1BudgetProfileV1 {
    #[serde(rename = "browserLimits")]
    pub browser_limits: Report1BudgetProfileV1BrowserLimits,
    #[serde(rename = "documentMaxBytes")]
    pub document_max_bytes: ExactInteger,
    #[serde(rename = "embeddedPanelOwnerMaxCanonicalBytes")]
    pub embedded_panel_owner_max_canonical_bytes: ExactInteger,
    #[serde(rename = "envelopeMaxCanonicalBytes")]
    pub envelope_max_canonical_bytes: ExactInteger,
    #[serde(rename = "explorationMaxCanonicalBytes")]
    pub exploration_max_canonical_bytes: ExactInteger,
    #[serde(rename = "graphPageSizeLadder")]
    pub graph_page_size_ladder: ::serde_json::Value,
    #[serde(rename = "graphPublicBounds")]
    pub graph_public_bounds: Report1BudgetProfileV1GraphPublicBounds,
    #[serde(rename = "ledgerMaxBytes")]
    pub ledger_max_bytes: ExactInteger,
    #[serde(rename = "maxCapabilityDeclarations")]
    pub max_capability_declarations: ExactInteger,
    #[serde(rename = "maxCatalogRules")]
    pub max_catalog_rules: ExactInteger,
    #[serde(rename = "maxEvidenceEntries")]
    pub max_evidence_entries: ExactInteger,
    #[serde(rename = "maxGraphItemsPerSlot")]
    pub max_graph_items_per_slot: ExactInteger,
    #[serde(rename = "maxGraphSlots")]
    pub max_graph_slots: ExactInteger,
    #[serde(rename = "maxHistoryFindingsPerRun")]
    pub max_history_findings_per_run: ExactInteger,
    #[serde(rename = "maxHistoryRuns")]
    pub max_history_runs: ExactInteger,
    #[serde(rename = "maxJsonDepth")]
    pub max_json_depth: ExactInteger,
    #[serde(rename = "maxPlannedSubjects")]
    pub max_planned_subjects: ExactInteger,
    #[serde(rename = "maxSubjectIndexRows")]
    pub max_subject_index_rows: ExactInteger,
    #[serde(rename = "ownerCodecDepth")]
    pub owner_codec_depth: ExactInteger,
    #[serde(rename = "profileId")]
    pub profile_id: ::serde_json::Value,
    #[serde(rename = "projectionPriority")]
    pub projection_priority: ::serde_json::Value,
    #[serde(rename = "rootMemberMaxBytes")]
    pub root_member_max_bytes: ExactInteger,
    pub standing: ::serde_json::Value,
}
///`Report1BudgetProfileV1BrowserLimits`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1BudgetProfileV1BrowserLimits {
    #[serde(rename = "maxLaidOutGraphEdges")]
    pub max_laid_out_graph_edges: i64,
    #[serde(rename = "maxLaidOutGraphNodes")]
    pub max_laid_out_graph_nodes: i64,
    #[serde(rename = "maxRenderedTableRows")]
    pub max_rendered_table_rows: i64,
}
///`Report1BudgetProfileV1GraphPublicBounds`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1BudgetProfileV1GraphPublicBounds {
    #[serde(rename = "maxItemsPerOperation")]
    pub max_items_per_operation: i64,
    #[serde(rename = "maxVisitedNodes")]
    pub max_visited_nodes: i64,
}
///`Report1CapabilityCatalogV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1CapabilityCatalogV1 {
    pub declarations: Native2ReleaseCapabilityRegistryV1,
    pub provenance: Report1CapabilityCatalogV1Provenance,
    pub source: Report1CapabilityCatalogV1Source,
}
///`Report1CapabilityCatalogV1Provenance`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1CapabilityCatalogV1Provenance {
    #[serde(rename = "hostAsserted")]
    pub host_asserted: ::serde_json::Value,
    #[serde(rename = "verifiedInDocument")]
    pub verified_in_document: ::serde_json::Value,
}
///`Report1CapabilityCatalogV1Source`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1CapabilityCatalogV1Source {
    pub kind: ::serde_json::Value,
    #[serde(rename = "registrySha256")]
    pub registry_sha256: Common4Sha256Hex,
}
///`Report1CargoEntryTargetV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1CargoEntryTargetV1 {
    #[serde(
        rename = "crateRootPath",
        deserialize_with = "::std::option::Option::deserialize"
    )]
    pub crate_root_path: ::std::option::Option<Common4LogicalPath>,
    #[serde(rename = "markerPath")]
    pub marker_path: Common4LogicalPath,
    #[serde(rename = "targetKind")]
    pub target_kind: Report1CargoEntryTargetV1TargetKind,
    #[serde(rename = "targetName")]
    pub target_name: Native2UnitIdentityV1PropertiesTargetName,
    #[serde(rename = "unitId")]
    pub unit_id: ::std::string::String,
}
///`Report1CargoEntryTargetV1TargetKind`
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
pub enum Report1CargoEntryTargetV1TargetKind {
    #[serde(rename = "bin")]
    Bin,
    #[serde(rename = "lib")]
    Lib,
}
impl ::std::fmt::Display for Report1CargoEntryTargetV1TargetKind {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Bin => f.write_str("bin"),
            Self::Lib => f.write_str("lib"),
        }
    }
}
impl ::std::str::FromStr for Report1CargoEntryTargetV1TargetKind {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "bin" => Ok(Self::Bin),
            "lib" => Ok(Self::Lib),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1CargoEntryTargetV1TargetKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Report1CargoEntryTargetV1TargetKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Every SELECTED bin/lib target of a Rust universe with its unique owned crate root (SourceUnitOwnershipV1 x RustUniverseV2ResolvedInputs.crateRootPaths). all only when every such target root is resolved from complete ownership.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(untagged, deny_unknown_fields)]
pub enum Report1CargoTargetEntriesV1 {
    Variant0 {
        #[serde(rename = "missingCoverage")]
        missing_coverage: ::std::vec::Vec<
            Report1CargoTargetEntriesV1Variant0Property0Item,
        >,
        #[serde(rename = "sourceUnitOwnershipId")]
        source_unit_ownership_id: ::std::string::String,
        state: Report1CargoTargetEntriesV1Variant0State,
        targets: ::std::vec::Vec<Report1CargoEntryTargetV1>,
        universe: Common4Sha256Hex,
    },
    Variant1 {
        #[serde(rename = "missingCoverage")]
        missing_coverage: ::std::vec::Vec<
            Report1CargoTargetEntriesV1Variant1Property0Item,
        >,
        #[serde(rename = "sourceUnitOwnershipId")]
        source_unit_ownership_id: (),
        state: ::serde_json::Value,
        targets: ::std::vec::Vec<Report1CargoEntryTargetV1>,
        universe: Common4Sha256Hex,
    },
}
///`Report1CargoTargetEntriesV1Variant0Property0Item`
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
pub enum Report1CargoTargetEntriesV1Variant0Property0Item {
    #[serde(rename = "ownership-enumeration-partial")]
    OwnershipEnumerationPartial,
    #[serde(rename = "target-crate-root-ambiguous")]
    TargetCrateRootAmbiguous,
    #[serde(rename = "target-crate-root-unresolved")]
    TargetCrateRootUnresolved,
}
impl ::std::fmt::Display for Report1CargoTargetEntriesV1Variant0Property0Item {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::OwnershipEnumerationPartial => {
                f.write_str("ownership-enumeration-partial")
            }
            Self::TargetCrateRootAmbiguous => f.write_str("target-crate-root-ambiguous"),
            Self::TargetCrateRootUnresolved => {
                f.write_str("target-crate-root-unresolved")
            }
        }
    }
}
impl ::std::str::FromStr for Report1CargoTargetEntriesV1Variant0Property0Item {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "ownership-enumeration-partial" => Ok(Self::OwnershipEnumerationPartial),
            "target-crate-root-ambiguous" => Ok(Self::TargetCrateRootAmbiguous),
            "target-crate-root-unresolved" => Ok(Self::TargetCrateRootUnresolved),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1CargoTargetEntriesV1Variant0Property0Item {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Report1CargoTargetEntriesV1Variant0Property0Item {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Report1CargoTargetEntriesV1Variant0State`
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
pub enum Report1CargoTargetEntriesV1Variant0State {
    #[serde(rename = "all")]
    All,
    #[serde(rename = "none")]
    None,
    #[serde(rename = "partial")]
    Partial,
}
impl ::std::fmt::Display for Report1CargoTargetEntriesV1Variant0State {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::All => f.write_str("all"),
            Self::None => f.write_str("none"),
            Self::Partial => f.write_str("partial"),
        }
    }
}
impl ::std::str::FromStr for Report1CargoTargetEntriesV1Variant0State {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "all" => Ok(Self::All),
            "none" => Ok(Self::None),
            "partial" => Ok(Self::Partial),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1CargoTargetEntriesV1Variant0State {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Report1CargoTargetEntriesV1Variant0State {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Report1CargoTargetEntriesV1Variant1Property0Item`
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
pub enum Report1CargoTargetEntriesV1Variant1Property0Item {
    #[serde(rename = "ownership-enumeration-partial")]
    OwnershipEnumerationPartial,
    #[serde(rename = "target-crate-root-ambiguous")]
    TargetCrateRootAmbiguous,
    #[serde(rename = "target-crate-root-unresolved")]
    TargetCrateRootUnresolved,
}
impl ::std::fmt::Display for Report1CargoTargetEntriesV1Variant1Property0Item {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::OwnershipEnumerationPartial => {
                f.write_str("ownership-enumeration-partial")
            }
            Self::TargetCrateRootAmbiguous => f.write_str("target-crate-root-ambiguous"),
            Self::TargetCrateRootUnresolved => {
                f.write_str("target-crate-root-unresolved")
            }
        }
    }
}
impl ::std::str::FromStr for Report1CargoTargetEntriesV1Variant1Property0Item {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "ownership-enumeration-partial" => Ok(Self::OwnershipEnumerationPartial),
            "target-crate-root-ambiguous" => Ok(Self::TargetCrateRootAmbiguous),
            "target-crate-root-unresolved" => Ok(Self::TargetCrateRootUnresolved),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1CargoTargetEntriesV1Variant1Property0Item {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Report1CargoTargetEntriesV1Variant1Property0Item {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Report1CargoTargetRefV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1CargoTargetRefV1 {
    #[serde(rename = "markerPath")]
    pub marker_path: Common4LogicalPath,
    #[serde(rename = "targetKind")]
    pub target_kind: Native2UnitIdentityV1PropertiesTargetKind,
    #[serde(rename = "targetName")]
    pub target_name: Native2UnitIdentityV1PropertiesTargetName,
    #[serde(rename = "unitId")]
    pub unit_id: ::std::string::String,
}
///`Report1CatalogPanelStateV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(untagged, deny_unknown_fields)]
pub enum Report1CatalogPanelStateV1 {
    Object { data: Report1CatalogPanelV1, state: ::serde_json::Value },
    Report1PanelNotPresentV1(Report1PanelNotPresentV1),
}
impl ::std::convert::From<Report1PanelNotPresentV1> for Report1CatalogPanelStateV1 {
    fn from(value: Report1PanelNotPresentV1) -> Self {
        Self::Report1PanelNotPresentV1(value)
    }
}
///`Report1CatalogPanelV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1CatalogPanelV1 {
    pub capabilities: Report1CatalogPanelV1Capabilities,
    pub rules: Report1CatalogPanelV1Rules,
}
///`Report1CatalogPanelV1Capabilities`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(untagged, deny_unknown_fields)]
pub enum Report1CatalogPanelV1Capabilities {
    Object { data: Report1CapabilityCatalogV1, state: ::serde_json::Value },
    Report1PanelNotPresentV1(Report1PanelNotPresentV1),
}
impl ::std::convert::From<Report1PanelNotPresentV1>
for Report1CatalogPanelV1Capabilities {
    fn from(value: Report1PanelNotPresentV1) -> Self {
        Self::Report1PanelNotPresentV1(value)
    }
}
///`Report1CatalogPanelV1Rules`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(untagged, deny_unknown_fields)]
pub enum Report1CatalogPanelV1Rules {
    Object { data: Report1RuleCatalogV1, state: ::serde_json::Value },
    Report1PanelNotPresentV1(Report1PanelNotPresentV1),
}
impl ::std::convert::From<Report1PanelNotPresentV1> for Report1CatalogPanelV1Rules {
    fn from(value: Report1PanelNotPresentV1) -> Self {
        Self::Report1PanelNotPresentV1(value)
    }
}
///`Report1ComparisonPanelStateV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(untagged, deny_unknown_fields)]
pub enum Report1ComparisonPanelStateV1 {
    Object { data: Report1ComparisonPanelV1, state: ::serde_json::Value },
    Report1PanelNotPresentV1(Report1PanelNotPresentV1),
}
impl ::std::convert::From<Report1PanelNotPresentV1> for Report1ComparisonPanelStateV1 {
    fn from(value: Report1PanelNotPresentV1) -> Self {
        Self::Report1PanelNotPresentV1(value)
    }
}
///`Report1ComparisonPanelV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1ComparisonPanelV1 {
    pub comparison: Comparison2Root,
    pub provenance: Report1ComparisonPanelV1Provenance,
}
///`Report1ComparisonPanelV1Provenance`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1ComparisonPanelV1Provenance {
    #[serde(rename = "hostAsserted")]
    pub host_asserted: ::serde_json::Value,
    #[serde(rename = "verifiedInDocument")]
    pub verified_in_document: ::serde_json::Value,
}
///`Report1ConfigurationPanelStateV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(untagged, deny_unknown_fields)]
pub enum Report1ConfigurationPanelStateV1 {
    Object { data: ConfigurationDisclosure1Root, state: ::serde_json::Value },
    Report1PanelNotPresentV1(Report1PanelNotPresentV1),
}
impl ::std::convert::From<Report1PanelNotPresentV1>
for Report1ConfigurationPanelStateV1 {
    fn from(value: Report1PanelNotPresentV1) -> Self {
        Self::Report1PanelNotPresentV1(value)
    }
}
///facts = distinct fact2 observations; programEdges = distinct importer/target endpoint pairs (per universe); sourceDependencies = distinct (importer anchor paths, universe-independent target identity): the same source import observed by two programs is 2 facts and 1 source dependency.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1CouplingCellV1 {
    pub facts: Common4Uint53,
    #[serde(rename = "fromOwnerKey")]
    pub from_owner_key: ::std::string::String,
    #[serde(rename = "importerSymbols")]
    pub importer_symbols: Common4Uint53,
    #[serde(rename = "importerUniverses")]
    pub importer_universes: ::std::vec::Vec<Common4Sha256Hex>,
    pub internal: bool,
    #[serde(rename = "programEdges")]
    pub program_edges: Common4Uint53,
    #[serde(rename = "sharedImporterFacts")]
    pub shared_importer_facts: Common4Uint53,
    #[serde(rename = "sharedTargetFacts")]
    pub shared_target_facts: Common4Uint53,
    #[serde(rename = "sourceDependencies")]
    pub source_dependencies: Common4Uint53,
    #[serde(rename = "toOwnerKey")]
    pub to_owner_key: ::std::string::String,
}
///`Report1CouplingDrilldownRowV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1CouplingDrilldownRowV1 {
    #[serde(rename = "factId")]
    pub fact_id: Graph4FactId,
    #[serde(rename = "fromOwnerKey")]
    pub from_owner_key: ::std::string::String,
    pub importer: Graph4GraphEndpoint,
    #[serde(rename = "importerAnchorPaths")]
    pub importer_anchor_paths: ::std::vec::Vec<Common4LogicalPath>,
    #[serde(rename = "importerTestOrigin")]
    pub importer_test_origin: Report1CouplingDrilldownRowV1ImporterTestOrigin,
    pub target: Graph4GraphEndpoint,
    #[serde(rename = "toOwnerKey")]
    pub to_owner_key: ::std::string::String,
}
///`Report1CouplingDrilldownRowV1ImporterTestOrigin`
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
pub enum Report1CouplingDrilldownRowV1ImporterTestOrigin {
    #[serde(rename = "no-test-origin-identity")]
    NoTestOriginIdentity,
    #[serde(rename = "not-identified-as-test-origin")]
    NotIdentifiedAsTestOrigin,
    #[serde(rename = "test-origin")]
    TestOrigin,
}
impl ::std::fmt::Display for Report1CouplingDrilldownRowV1ImporterTestOrigin {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::NoTestOriginIdentity => f.write_str("no-test-origin-identity"),
            Self::NotIdentifiedAsTestOrigin => {
                f.write_str("not-identified-as-test-origin")
            }
            Self::TestOrigin => f.write_str("test-origin"),
        }
    }
}
impl ::std::str::FromStr for Report1CouplingDrilldownRowV1ImporterTestOrigin {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "no-test-origin-identity" => Ok(Self::NoTestOriginIdentity),
            "not-identified-as-test-origin" => Ok(Self::NotIdentifiedAsTestOrigin),
            "test-origin" => Ok(Self::TestOrigin),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1CouplingDrilldownRowV1ImporterTestOrigin {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Report1CouplingDrilldownRowV1ImporterTestOrigin {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Report1CouplingOwnerV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(tag = "keyKind", deny_unknown_fields)]
pub enum Report1CouplingOwnerV1 {
    #[serde(rename = "first-party-package")]
    FirstPartyPackage {
        #[serde(rename = "cargoTargets")]
        cargo_targets: ::std::vec::Vec<Report1CargoTargetRefV1>,
        #[serde(rename = "ownerKey")]
        owner_key: ::std::string::String,
        #[serde(rename = "packageManifestPath")]
        package_manifest_path: Common4LogicalPath,
        #[serde(rename = "packageName")]
        package_name: Report1CouplingOwnerV1PackageName,
        #[serde(
            rename = "workspaceUnit",
            deserialize_with = "::std::option::Option::deserialize"
        )]
        workspace_unit: ::std::option::Option<Report1WorkspaceUnitRefV1>,
    },
    #[serde(rename = "workspace-unit")]
    WorkspaceUnit {
        #[serde(rename = "ownerKey")]
        owner_key: ::std::string::String,
        #[serde(rename = "workspaceUnit")]
        workspace_unit: Report1WorkspaceUnitRefV1,
    },
    #[serde(rename = "external-package")]
    ExternalPackage {
        #[serde(rename = "ownerKey")]
        owner_key: ::std::string::String,
        #[serde(rename = "packageManifestPath")]
        package_manifest_path: Common4LogicalPath,
        #[serde(rename = "packageName")]
        package_name: Report1CouplingOwnerV1PackageName,
        universe: Common4Sha256Hex,
    },
}
///`Report1CouplingOwnerV1PackageName`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Report1CouplingOwnerV1PackageName(::std::string::String);
impl ::std::ops::Deref for Report1CouplingOwnerV1PackageName {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Report1CouplingOwnerV1PackageName> for ::std::string::String {
    fn from(value: Report1CouplingOwnerV1PackageName) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Report1CouplingOwnerV1PackageName {
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
impl ::std::convert::TryFrom<&str> for Report1CouplingOwnerV1PackageName {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Report1CouplingOwnerV1PackageName {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Report1CouplingOwnerV1PackageName {
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
///`Report1CouplingPanelStateV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(untagged, deny_unknown_fields)]
pub enum Report1CouplingPanelStateV1 {
    Object { data: Report1CouplingPanelV1, state: ::serde_json::Value },
    Report1PanelNotPresentV1(Report1PanelNotPresentV1),
}
impl ::std::convert::From<Report1PanelNotPresentV1> for Report1CouplingPanelStateV1 {
    fn from(value: Report1PanelNotPresentV1) -> Self {
        Self::Report1PanelNotPresentV1(value)
    }
}
///R08 coupling over the whole admitted imports@resolved-target view. Cells are listed in priority order (facts descending, then keys) and byte-bounded under the report-wide remaining exploration budget; omitted cells make a blank cell not-determined.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1CouplingPanelV1 {
    pub absence: Report1CouplingPanelV1Absence,
    pub cells: ::std::vec::Vec<Report1CouplingCellV1>,
    #[serde(rename = "cellsProjection")]
    pub cells_projection: Report1ItemProjectionV1,
    #[serde(rename = "countUnits")]
    pub count_units: Report1CouplingPanelV1CountUnits,
    pub drilldown: ::std::vec::Vec<Report1CouplingDrilldownRowV1>,
    #[serde(rename = "drilldownProjection")]
    pub drilldown_projection: Report1ItemProjectionV1,
    #[serde(rename = "importerBuckets")]
    pub importer_buckets: ::std::vec::Vec<Report1CouplingPanelV1ImporterBucketsItem>,
    #[serde(rename = "minResolution")]
    pub min_resolution: ::serde_json::Value,
    #[serde(rename = "ownerClosure")]
    pub owner_closure: Report1CouplingPanelV1OwnerClosure,
    pub owners: ::std::vec::Vec<Report1CouplingOwnerV1>,
    pub policy: ::serde_json::Value,
    pub projection: Report1CouplingPanelV1Projection,
    pub provenance: Report1CouplingPanelV1Provenance,
    pub relation: ::serde_json::Value,
    #[serde(rename = "runId")]
    pub run_id: Common4RunId,
    #[serde(rename = "targetBuckets")]
    pub target_buckets: ::std::vec::Vec<Report1CouplingPanelV1TargetBucketsItem>,
    #[serde(rename = "targetBucketsProjection")]
    pub target_buckets_projection: Report1ItemProjectionV1,
    pub totals: Report1CouplingPanelV1Totals,
}
///`Report1CouplingPanelV1Absence`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1CouplingPanelV1Absence {
    #[serde(rename = "absenceSupported")]
    pub absence_supported: bool,
    #[serde(rename = "blankCellMeans")]
    pub blank_cell_means: Report1CouplingPanelV1AbsenceBlankCellMeans,
    pub blockers: ::std::vec::Vec<Report1CouplingPanelV1AbsenceBlockersItem>,
}
///`Report1CouplingPanelV1AbsenceBlankCellMeans`
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
pub enum Report1CouplingPanelV1AbsenceBlankCellMeans {
    #[serde(rename = "no-projected-fact")]
    NoProjectedFact,
    #[serde(rename = "not-determined-cells-omitted")]
    NotDeterminedCellsOmitted,
}
impl ::std::fmt::Display for Report1CouplingPanelV1AbsenceBlankCellMeans {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::NoProjectedFact => f.write_str("no-projected-fact"),
            Self::NotDeterminedCellsOmitted => {
                f.write_str("not-determined-cells-omitted")
            }
        }
    }
}
impl ::std::str::FromStr for Report1CouplingPanelV1AbsenceBlankCellMeans {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "no-projected-fact" => Ok(Self::NoProjectedFact),
            "not-determined-cells-omitted" => Ok(Self::NotDeterminedCellsOmitted),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1CouplingPanelV1AbsenceBlankCellMeans {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Report1CouplingPanelV1AbsenceBlankCellMeans {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Report1CouplingPanelV1AbsenceBlockersItem`
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
pub enum Report1CouplingPanelV1AbsenceBlockersItem {
    #[serde(rename = "cells-omitted")]
    CellsOmitted,
    #[serde(rename = "evidence-limitations")]
    EvidenceLimitations,
    #[serde(rename = "projection-lower-bound")]
    ProjectionLowerBound,
    #[serde(rename = "target-buckets-omitted")]
    TargetBucketsOmitted,
    #[serde(rename = "unattributed-importers")]
    UnattributedImporters,
    #[serde(rename = "unattributed-targets")]
    UnattributedTargets,
}
impl ::std::fmt::Display for Report1CouplingPanelV1AbsenceBlockersItem {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::CellsOmitted => f.write_str("cells-omitted"),
            Self::EvidenceLimitations => f.write_str("evidence-limitations"),
            Self::ProjectionLowerBound => f.write_str("projection-lower-bound"),
            Self::TargetBucketsOmitted => f.write_str("target-buckets-omitted"),
            Self::UnattributedImporters => f.write_str("unattributed-importers"),
            Self::UnattributedTargets => f.write_str("unattributed-targets"),
        }
    }
}
impl ::std::str::FromStr for Report1CouplingPanelV1AbsenceBlockersItem {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "cells-omitted" => Ok(Self::CellsOmitted),
            "evidence-limitations" => Ok(Self::EvidenceLimitations),
            "projection-lower-bound" => Ok(Self::ProjectionLowerBound),
            "target-buckets-omitted" => Ok(Self::TargetBucketsOmitted),
            "unattributed-importers" => Ok(Self::UnattributedImporters),
            "unattributed-targets" => Ok(Self::UnattributedTargets),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1CouplingPanelV1AbsenceBlockersItem {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Report1CouplingPanelV1AbsenceBlockersItem {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Report1CouplingPanelV1CountUnits`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1CouplingPanelV1CountUnits {
    pub facts: ::std::string::String,
    #[serde(rename = "programEdges")]
    pub program_edges: ::std::string::String,
    #[serde(rename = "sourceDependencies")]
    pub source_dependencies: ::std::string::String,
}
///`Report1CouplingPanelV1ImporterBucketsItem`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1CouplingPanelV1ImporterBucketsItem {
    pub cause: Report1CouplingPanelV1ImporterBucketsItemCause,
    pub facts: Common4Uint53,
}
///`Report1CouplingPanelV1ImporterBucketsItemCause`
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
pub enum Report1CouplingPanelV1ImporterBucketsItemCause {
    #[serde(rename = "importer-anchor-missing")]
    ImporterAnchorMissing,
    #[serde(rename = "importer-anchor-owners-disagree")]
    ImporterAnchorOwnersDisagree,
    #[serde(rename = "membership-row-missing")]
    MembershipRowMissing,
    #[serde(rename = "no-program-unit")]
    NoProgramUnit,
    #[serde(rename = "not-compiled-by-selected-targets")]
    NotCompiledBySelectedTargets,
    #[serde(rename = "owned-only-by-unselected-targets")]
    OwnedOnlyByUnselectedTargets,
    #[serde(rename = "owner-manifest-not-package-inventoried")]
    OwnerManifestNotPackageInventoried,
    #[serde(rename = "ownership-enumeration-partial")]
    OwnershipEnumerationPartial,
    #[serde(rename = "ownership-missing")]
    OwnershipMissing,
    #[serde(rename = "package-inventory-conflict")]
    PackageInventoryConflict,
    #[serde(rename = "package-inventory-incomplete")]
    PackageInventoryIncomplete,
    #[serde(rename = "universe-not-plan-bound")]
    UniverseNotPlanBound,
}
impl ::std::fmt::Display for Report1CouplingPanelV1ImporterBucketsItemCause {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::ImporterAnchorMissing => f.write_str("importer-anchor-missing"),
            Self::ImporterAnchorOwnersDisagree => {
                f.write_str("importer-anchor-owners-disagree")
            }
            Self::MembershipRowMissing => f.write_str("membership-row-missing"),
            Self::NoProgramUnit => f.write_str("no-program-unit"),
            Self::NotCompiledBySelectedTargets => {
                f.write_str("not-compiled-by-selected-targets")
            }
            Self::OwnedOnlyByUnselectedTargets => {
                f.write_str("owned-only-by-unselected-targets")
            }
            Self::OwnerManifestNotPackageInventoried => {
                f.write_str("owner-manifest-not-package-inventoried")
            }
            Self::OwnershipEnumerationPartial => {
                f.write_str("ownership-enumeration-partial")
            }
            Self::OwnershipMissing => f.write_str("ownership-missing"),
            Self::PackageInventoryConflict => f.write_str("package-inventory-conflict"),
            Self::PackageInventoryIncomplete => {
                f.write_str("package-inventory-incomplete")
            }
            Self::UniverseNotPlanBound => f.write_str("universe-not-plan-bound"),
        }
    }
}
impl ::std::str::FromStr for Report1CouplingPanelV1ImporterBucketsItemCause {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "importer-anchor-missing" => Ok(Self::ImporterAnchorMissing),
            "importer-anchor-owners-disagree" => Ok(Self::ImporterAnchorOwnersDisagree),
            "membership-row-missing" => Ok(Self::MembershipRowMissing),
            "no-program-unit" => Ok(Self::NoProgramUnit),
            "not-compiled-by-selected-targets" => Ok(Self::NotCompiledBySelectedTargets),
            "owned-only-by-unselected-targets" => Ok(Self::OwnedOnlyByUnselectedTargets),
            "owner-manifest-not-package-inventoried" => {
                Ok(Self::OwnerManifestNotPackageInventoried)
            }
            "ownership-enumeration-partial" => Ok(Self::OwnershipEnumerationPartial),
            "ownership-missing" => Ok(Self::OwnershipMissing),
            "package-inventory-conflict" => Ok(Self::PackageInventoryConflict),
            "package-inventory-incomplete" => Ok(Self::PackageInventoryIncomplete),
            "universe-not-plan-bound" => Ok(Self::UniverseNotPlanBound),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1CouplingPanelV1ImporterBucketsItemCause {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Report1CouplingPanelV1ImporterBucketsItemCause {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Report1CouplingPanelV1OwnerClosure`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1CouplingPanelV1OwnerClosure {
    pub listed: Common4Uint53,
    pub rule: ::serde_json::Value,
    pub total: Common4Uint53,
}
///`Report1CouplingPanelV1Projection`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1CouplingPanelV1Projection {
    #[serde(rename = "countBasis")]
    pub count_basis: Graph4CountBasis,
    #[serde(rename = "coverageIds")]
    pub coverage_ids: ::std::vec::Vec<Common4CoverageId>,
    #[serde(rename = "deficiencyCitationCount")]
    pub deficiency_citation_count: Common4Uint53,
    #[serde(rename = "factViewDigests")]
    pub fact_view_digests: ::std::vec::Vec<Graph4ViewDigest>,
    #[serde(rename = "limitationKinds")]
    pub limitation_kinds: ::std::vec::Vec<
        Graph4GraphEvidenceDisclosurePropertiesResolutionLimitationsItemsPropertiesKind,
    >,
}
///`Report1CouplingPanelV1Provenance`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1CouplingPanelV1Provenance {
    #[serde(rename = "hostAsserted")]
    pub host_asserted: ::serde_json::Value,
    #[serde(rename = "verifiedInDocument")]
    pub verified_in_document: ::serde_json::Value,
}
///`Report1CouplingPanelV1TargetBucketsItem`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1CouplingPanelV1TargetBucketsItem {
    pub cause: Report1CouplingPanelV1TargetBucketsItemCause,
    pub facts: Common4Uint53,
    #[serde(rename = "fromOwnerKey")]
    pub from_owner_key: ::std::string::String,
}
///`Report1CouplingPanelV1TargetBucketsItemCause`
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
pub enum Report1CouplingPanelV1TargetBucketsItemCause {
    #[serde(rename = "external-non-package-target")]
    ExternalNonPackageTarget,
    #[serde(rename = "file-not-inventoried")]
    FileNotInventoried,
    #[serde(rename = "membership-row-missing")]
    MembershipRowMissing,
    #[serde(rename = "no-program-unit")]
    NoProgramUnit,
    #[serde(rename = "not-compiled-by-selected-targets")]
    NotCompiledBySelectedTargets,
    #[serde(rename = "owned-only-by-unselected-targets")]
    OwnedOnlyByUnselectedTargets,
    #[serde(rename = "owner-manifest-not-package-inventoried")]
    OwnerManifestNotPackageInventoried,
    #[serde(rename = "ownership-enumeration-partial")]
    OwnershipEnumerationPartial,
    #[serde(rename = "ownership-missing")]
    OwnershipMissing,
    #[serde(rename = "package-endpoint-inventory-mismatch")]
    PackageEndpointInventoryMismatch,
    #[serde(rename = "package-inventory-conflict")]
    PackageInventoryConflict,
    #[serde(rename = "package-inventory-incomplete")]
    PackageInventoryIncomplete,
    #[serde(rename = "symbol-attribution-conflict")]
    SymbolAttributionConflict,
    #[serde(rename = "symbol-inventory-incomplete")]
    SymbolInventoryIncomplete,
    #[serde(rename = "symbol-inventory-missing")]
    SymbolInventoryMissing,
    #[serde(rename = "symbol-not-inventoried")]
    SymbolNotInventoried,
    #[serde(rename = "universe-not-plan-bound")]
    UniverseNotPlanBound,
    #[serde(rename = "unknown-occupancy")]
    UnknownOccupancy,
}
impl ::std::fmt::Display for Report1CouplingPanelV1TargetBucketsItemCause {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::ExternalNonPackageTarget => f.write_str("external-non-package-target"),
            Self::FileNotInventoried => f.write_str("file-not-inventoried"),
            Self::MembershipRowMissing => f.write_str("membership-row-missing"),
            Self::NoProgramUnit => f.write_str("no-program-unit"),
            Self::NotCompiledBySelectedTargets => {
                f.write_str("not-compiled-by-selected-targets")
            }
            Self::OwnedOnlyByUnselectedTargets => {
                f.write_str("owned-only-by-unselected-targets")
            }
            Self::OwnerManifestNotPackageInventoried => {
                f.write_str("owner-manifest-not-package-inventoried")
            }
            Self::OwnershipEnumerationPartial => {
                f.write_str("ownership-enumeration-partial")
            }
            Self::OwnershipMissing => f.write_str("ownership-missing"),
            Self::PackageEndpointInventoryMismatch => {
                f.write_str("package-endpoint-inventory-mismatch")
            }
            Self::PackageInventoryConflict => f.write_str("package-inventory-conflict"),
            Self::PackageInventoryIncomplete => {
                f.write_str("package-inventory-incomplete")
            }
            Self::SymbolAttributionConflict => f.write_str("symbol-attribution-conflict"),
            Self::SymbolInventoryIncomplete => f.write_str("symbol-inventory-incomplete"),
            Self::SymbolInventoryMissing => f.write_str("symbol-inventory-missing"),
            Self::SymbolNotInventoried => f.write_str("symbol-not-inventoried"),
            Self::UniverseNotPlanBound => f.write_str("universe-not-plan-bound"),
            Self::UnknownOccupancy => f.write_str("unknown-occupancy"),
        }
    }
}
impl ::std::str::FromStr for Report1CouplingPanelV1TargetBucketsItemCause {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "external-non-package-target" => Ok(Self::ExternalNonPackageTarget),
            "file-not-inventoried" => Ok(Self::FileNotInventoried),
            "membership-row-missing" => Ok(Self::MembershipRowMissing),
            "no-program-unit" => Ok(Self::NoProgramUnit),
            "not-compiled-by-selected-targets" => Ok(Self::NotCompiledBySelectedTargets),
            "owned-only-by-unselected-targets" => Ok(Self::OwnedOnlyByUnselectedTargets),
            "owner-manifest-not-package-inventoried" => {
                Ok(Self::OwnerManifestNotPackageInventoried)
            }
            "ownership-enumeration-partial" => Ok(Self::OwnershipEnumerationPartial),
            "ownership-missing" => Ok(Self::OwnershipMissing),
            "package-endpoint-inventory-mismatch" => {
                Ok(Self::PackageEndpointInventoryMismatch)
            }
            "package-inventory-conflict" => Ok(Self::PackageInventoryConflict),
            "package-inventory-incomplete" => Ok(Self::PackageInventoryIncomplete),
            "symbol-attribution-conflict" => Ok(Self::SymbolAttributionConflict),
            "symbol-inventory-incomplete" => Ok(Self::SymbolInventoryIncomplete),
            "symbol-inventory-missing" => Ok(Self::SymbolInventoryMissing),
            "symbol-not-inventoried" => Ok(Self::SymbolNotInventoried),
            "universe-not-plan-bound" => Ok(Self::UniverseNotPlanBound),
            "unknown-occupancy" => Ok(Self::UnknownOccupancy),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1CouplingPanelV1TargetBucketsItemCause {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Report1CouplingPanelV1TargetBucketsItemCause {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Report1CouplingPanelV1Totals`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1CouplingPanelV1Totals {
    #[serde(rename = "attributedFacts")]
    pub attributed_facts: Common4Uint53,
    #[serde(rename = "cellCount")]
    pub cell_count: Common4Uint53,
    #[serde(rename = "cellFactSum")]
    pub cell_fact_sum: Common4Uint53,
    #[serde(rename = "distinctFacts")]
    pub distinct_facts: Common4Uint53,
    #[serde(rename = "importerSymbolPathOutsideAnchors")]
    pub importer_symbol_path_outside_anchors: Common4Uint53,
    #[serde(rename = "importerUnattributedFacts")]
    pub importer_unattributed_facts: Common4Uint53,
    #[serde(rename = "ownerCount")]
    pub owner_count: Common4Uint53,
    #[serde(rename = "targetBucketCount")]
    pub target_bucket_count: Common4Uint53,
    #[serde(rename = "targetUnattributedFacts")]
    pub target_unattributed_facts: Common4Uint53,
}
///Projection from the catalogue owner after private closure/release/declaration admission. Carries the complete tree, not a new proof of its authentication.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(tag = "state", deny_unknown_fields)]
pub enum Report1DescriptionReceiptV1 {
    #[serde(rename = "unavailable")]
    Unavailable {
        #[serde(rename = "closureId")]
        closure_id: Common4ClosureId,
        reason: Report1DescriptionReceiptV1Reason,
    },
    #[serde(rename = "no-catalogue-declared")]
    NoCatalogueDeclared {
        #[serde(
            rename = "capabilityAuthority",
            deserialize_with = "::std::option::Option::deserialize"
        )]
        capability_authority: ::std::option::Option<
            Report1DescriptionReceiptV1CapabilityAuthority,
        >,
        #[serde(rename = "closureId")]
        closure_id: Common4ClosureId,
        #[serde(rename = "componentManifestDigest")]
        component_manifest_digest: Common4Sha256Hex,
        platform: Identity3ClosurePropertiesPlatform,
        #[serde(rename = "protocolMajor")]
        protocol_major: Identity3ClosurePropertiesProtocolMajor,
        tree: Identity3ClosurePropertiesTree,
        #[serde(rename = "trustOrigin")]
        trust_origin: Report1DescriptionReceiptV1TrustOrigin,
    },
    #[serde(rename = "present")]
    Present {
        capabilities: ::std::vec::Vec<Report1DescriptionReceiptV1CapabilitiesItem>,
        #[serde(
            rename = "capabilityAuthority",
            deserialize_with = "::std::option::Option::deserialize"
        )]
        capability_authority: ::std::option::Option<
            Report1DescriptionReceiptV1CapabilityAuthority,
        >,
        #[serde(rename = "closureId")]
        closure_id: Common4ClosureId,
        #[serde(rename = "componentManifestDigest")]
        component_manifest_digest: Common4Sha256Hex,
        listing: Report1DescriptionReceiptV1Listing,
        platform: Identity3ClosurePropertiesPlatform,
        #[serde(rename = "protocolMajor")]
        protocol_major: Identity3ClosurePropertiesProtocolMajor,
        recipes: ::std::vec::Vec<Report1DescriptionReceiptV1RecipesItem>,
        rules: ::std::vec::Vec<Report1DescriptionReceiptV1RulesItem>,
        tree: Identity3ClosurePropertiesTree,
        #[serde(rename = "trustOrigin")]
        trust_origin: Report1DescriptionReceiptV1TrustOrigin,
    },
}
///`Report1DescriptionReceiptV1CapabilitiesItem`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(tag = "state", deny_unknown_fields)]
pub enum Report1DescriptionReceiptV1CapabilitiesItem {
    #[serde(rename = "present")]
    Present { descriptor: PresentationCatalog1CapabilityDescriptionV1 },
    #[serde(rename = "unavailable")]
    Unavailable { key: (Common4CanonicalIdentifier,), reason: ::serde_json::Value },
}
///`Report1DescriptionReceiptV1CapabilityAuthority`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1DescriptionReceiptV1CapabilityAuthority {
    #[serde(rename = "closureId")]
    pub closure_id: Common4ClosureId,
    pub platform: Identity3ClosurePropertiesPlatform,
    #[serde(rename = "registrySha256")]
    pub registry_sha256: Common4Sha256Hex,
}
///`Report1DescriptionReceiptV1Listing`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1DescriptionReceiptV1Listing {
    pub bytes: u64,
    pub path: Report1DescriptionReceiptV1ListingPath,
    pub sha256: ::std::string::String,
}
///`Report1DescriptionReceiptV1ListingPath`
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
pub enum Report1DescriptionReceiptV1ListingPath {
    #[serde(rename = ".opensip/presentation-catalog.v1.json")]
    OpensipPresentationCatalogV1Json,
}
impl ::std::fmt::Display for Report1DescriptionReceiptV1ListingPath {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::OpensipPresentationCatalogV1Json => {
                f.write_str(".opensip/presentation-catalog.v1.json")
            }
        }
    }
}
impl ::std::str::FromStr for Report1DescriptionReceiptV1ListingPath {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            ".opensip/presentation-catalog.v1.json" => {
                Ok(Self::OpensipPresentationCatalogV1Json)
            }
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1DescriptionReceiptV1ListingPath {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Report1DescriptionReceiptV1ListingPath {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Report1DescriptionReceiptV1Reason`
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
pub enum Report1DescriptionReceiptV1Reason {
    #[serde(rename = "catalog-not-retained")]
    CatalogNotRetained,
    #[serde(rename = "catalog-corrupt")]
    CatalogCorrupt,
}
impl ::std::fmt::Display for Report1DescriptionReceiptV1Reason {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::CatalogNotRetained => f.write_str("catalog-not-retained"),
            Self::CatalogCorrupt => f.write_str("catalog-corrupt"),
        }
    }
}
impl ::std::str::FromStr for Report1DescriptionReceiptV1Reason {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "catalog-not-retained" => Ok(Self::CatalogNotRetained),
            "catalog-corrupt" => Ok(Self::CatalogCorrupt),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1DescriptionReceiptV1Reason {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Report1DescriptionReceiptV1Reason {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Report1DescriptionReceiptV1RecipesItem`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(tag = "state", deny_unknown_fields)]
pub enum Report1DescriptionReceiptV1RecipesItem {
    #[serde(rename = "present")]
    Present { descriptor: PresentationCatalog1RecipeDescriptionV1 },
    #[serde(rename = "unavailable")]
    Unavailable {
        key: (Common4ContributionId, Common4CanonicalIdentifier, Common4SemanticVersion),
        reason: ::serde_json::Value,
    },
}
///`Report1DescriptionReceiptV1RulesItem`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(tag = "state", deny_unknown_fields)]
pub enum Report1DescriptionReceiptV1RulesItem {
    #[serde(rename = "present")]
    Present { descriptor: PresentationCatalog1RuleDescriptionV1 },
    #[serde(rename = "unavailable")]
    Unavailable {
        key: (Common1ContributionId, Common1CanonicalIdentifier, u16, Common1Sha256Hex),
        reason: ::serde_json::Value,
    },
}
///`Report1DescriptionReceiptV1TrustOrigin`
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
pub enum Report1DescriptionReceiptV1TrustOrigin {
    #[serde(rename = "retained-generation")]
    RetainedGeneration,
    #[serde(rename = "installed-signed-release")]
    InstalledSignedRelease,
    #[serde(rename = "signed-closure-bundle")]
    SignedClosureBundle,
}
impl ::std::fmt::Display for Report1DescriptionReceiptV1TrustOrigin {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::RetainedGeneration => f.write_str("retained-generation"),
            Self::InstalledSignedRelease => f.write_str("installed-signed-release"),
            Self::SignedClosureBundle => f.write_str("signed-closure-bundle"),
        }
    }
}
impl ::std::str::FromStr for Report1DescriptionReceiptV1TrustOrigin {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "retained-generation" => Ok(Self::RetainedGeneration),
            "installed-signed-release" => Ok(Self::InstalledSignedRelease),
            "signed-closure-bundle" => Ok(Self::SignedClosureBundle),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1DescriptionReceiptV1TrustOrigin {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Report1DescriptionReceiptV1TrustOrigin {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Report1DescriptionsPanelStateV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(untagged, deny_unknown_fields)]
pub enum Report1DescriptionsPanelStateV1 {
    Object { data: Report1DescriptionsPanelV1, state: ::serde_json::Value },
    Report1PanelNotPresentV1(Report1PanelNotPresentV1),
}
impl ::std::convert::From<Report1PanelNotPresentV1> for Report1DescriptionsPanelStateV1 {
    fn from(value: Report1PanelNotPresentV1) -> Self {
        Self::Report1PanelNotPresentV1(value)
    }
}
///`Report1DescriptionsPanelV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1DescriptionsPanelV1 {
    pub provenance: Report1DescriptionsPanelV1Provenance,
    pub recipe: Report1DescriptionsPanelV1Recipe,
    pub run: Report1DescriptionsPanelV1Run,
}
///`Report1DescriptionsPanelV1Provenance`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1DescriptionsPanelV1Provenance {
    #[serde(rename = "hostAsserted")]
    pub host_asserted: ::serde_json::Value,
    pub limits: ::serde_json::Value,
    #[serde(rename = "verifiedInDocument")]
    pub verified_in_document: ::serde_json::Value,
}
///`Report1DescriptionsPanelV1Recipe`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(untagged, deny_unknown_fields)]
pub enum Report1DescriptionsPanelV1Recipe {
    Object { data: Report1RecipeDescriptionsV1, state: ::serde_json::Value },
    Report1PanelNotPresentV1(Report1PanelNotPresentV1),
}
impl ::std::convert::From<Report1PanelNotPresentV1>
for Report1DescriptionsPanelV1Recipe {
    fn from(value: Report1PanelNotPresentV1) -> Self {
        Self::Report1PanelNotPresentV1(value)
    }
}
///`Report1DescriptionsPanelV1Run`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(untagged, deny_unknown_fields)]
pub enum Report1DescriptionsPanelV1Run {
    Object { data: Report1RunDescriptionsV1, state: ::serde_json::Value },
    Report1PanelNotPresentV1(Report1PanelNotPresentV1),
}
impl ::std::convert::From<Report1PanelNotPresentV1> for Report1DescriptionsPanelV1Run {
    fn from(value: Report1PanelNotPresentV1) -> Self {
        Self::Report1PanelNotPresentV1(value)
    }
}
///Counts shown in the static section. The descriptor-not-retained count and the snapshot count are host assertions, named as such; admission recomputes the counts from the document but cannot prove host retention. Browser admission is shape, codec and internal joins only and must not present verifiedInDocument labels as semantic proof.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1DisclosuresV1 {
    ///Mandatory exact explicit history selection, or null in automatic mode. Never removed with an omitted/unavailable history panel; echoed by the script-independent disclosure section.
    #[serde(
        rename = "explicitHistorySelection",
        deserialize_with = "::std::option::Option::deserialize"
    )]
    pub explicit_history_selection: ::std::option::Option<ExplicitHistory1Root>,
    #[serde(
        rename = "graphDescriptorNotRetainedSubjectsHostAsserted",
        deserialize_with = "::std::option::Option::deserialize"
    )]
    pub graph_descriptor_not_retained_subjects_host_asserted: ::std::option::Option<
        Common4Uint53,
    >,
    #[serde(
        rename = "graphPlannedSubjects",
        deserialize_with = "::std::option::Option::deserialize"
    )]
    pub graph_planned_subjects: ::std::option::Option<Common4Uint53>,
    #[serde(
        rename = "historyPriorRunsInSnapshotHostAsserted",
        deserialize_with = "::std::option::Option::deserialize"
    )]
    pub history_prior_runs_in_snapshot_host_asserted: ::std::option::Option<
        Common4Uint53,
    >,
}
///`Report1EntryProvenanceV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(tag = "source", deny_unknown_fields)]
pub enum Report1EntryProvenanceV1 {
    #[serde(rename = "explicit")]
    Explicit,
    #[serde(rename = "cargo-target")]
    CargoTarget {
        #[serde(rename = "markerPath")]
        marker_path: Common4LogicalPath,
        #[serde(rename = "targetKind")]
        target_kind: Report1EntryProvenanceV1TargetKind,
        #[serde(rename = "targetName")]
        target_name: Native2UnitIdentityV1PropertiesTargetName,
        #[serde(rename = "unitId")]
        unit_id: ::std::string::String,
    },
    #[serde(rename = "recognized")]
    Recognized {
        assurance: Native2FrameworkRecognitionResultV1PropertiesAssurance,
        evidence: Native2FrameworkRecognitionResultV1PropertiesEvidence,
        #[serde(rename = "recognizerId")]
        recognizer_id: Native2FrameworkRecognitionResultV1PropertiesRecognizerId,
        #[serde(rename = "recognizerVersion")]
        recognizer_version: ExactInteger,
        #[serde(rename = "unitOrdinal")]
        unit_ordinal: Common4Uint53,
        #[serde(rename = "unresolvedChoices")]
        unresolved_choices: Native2FrameworkRecognitionResultV1PropertiesUnresolvedChoices,
    },
}
///`Report1EntryProvenanceV1TargetKind`
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
pub enum Report1EntryProvenanceV1TargetKind {
    #[serde(rename = "bin")]
    Bin,
    #[serde(rename = "lib")]
    Lib,
}
impl ::std::fmt::Display for Report1EntryProvenanceV1TargetKind {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Bin => f.write_str("bin"),
            Self::Lib => f.write_str("lib"),
        }
    }
}
impl ::std::str::FromStr for Report1EntryProvenanceV1TargetKind {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "bin" => Ok(Self::Bin),
            "lib" => Ok(Self::Lib),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1EntryProvenanceV1TargetKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Report1EntryProvenanceV1TargetKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Report1EntryRecognitionStateV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(tag = "state", deny_unknown_fields)]
pub enum Report1EntryRecognitionStateV1 {
    #[serde(rename = "not-plan-bound")]
    NotPlanBound,
    #[serde(rename = "unavailable")]
    Unavailable {
        availability: Report1EntryRecognitionStateV1Variant1Property0,
        #[serde(rename = "parameterDigest")]
        parameter_digest: ::std::string::String,
    },
    #[serde(rename = "plan-bound")]
    PlanBound {
        availability: Report1EntryRecognitionStateV1Variant2Property0,
        #[serde(rename = "cargoTargetEntries")]
        cargo_target_entries: ::std::vec::Vec<Report1CargoTargetEntriesV1>,
        #[serde(rename = "explicitEntryPointCount")]
        explicit_entry_point_count: Common4Uint53,
        #[serde(rename = "parameterDigest")]
        parameter_digest: ::std::string::String,
        units: ::std::vec::Vec<Report1EntryRecognitionUnitV1>,
    },
}
///`Report1EntryRecognitionStateV1Variant1Property0`
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
pub enum Report1EntryRecognitionStateV1Variant1Property0 {
    #[serde(rename = "corrupt")]
    Corrupt,
    #[serde(rename = "expired")]
    Expired,
    #[serde(rename = "partial")]
    Partial,
    #[serde(rename = "purged")]
    Purged,
    #[serde(rename = "unavailable")]
    Unavailable,
}
impl ::std::fmt::Display for Report1EntryRecognitionStateV1Variant1Property0 {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Corrupt => f.write_str("corrupt"),
            Self::Expired => f.write_str("expired"),
            Self::Partial => f.write_str("partial"),
            Self::Purged => f.write_str("purged"),
            Self::Unavailable => f.write_str("unavailable"),
        }
    }
}
impl ::std::str::FromStr for Report1EntryRecognitionStateV1Variant1Property0 {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "corrupt" => Ok(Self::Corrupt),
            "expired" => Ok(Self::Expired),
            "partial" => Ok(Self::Partial),
            "purged" => Ok(Self::Purged),
            "unavailable" => Ok(Self::Unavailable),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1EntryRecognitionStateV1Variant1Property0 {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Report1EntryRecognitionStateV1Variant1Property0 {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Report1EntryRecognitionStateV1Variant2Property0`
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
pub enum Report1EntryRecognitionStateV1Variant2Property0 {
    #[serde(rename = "partial")]
    Partial,
    #[serde(rename = "retained")]
    Retained,
}
impl ::std::fmt::Display for Report1EntryRecognitionStateV1Variant2Property0 {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Partial => f.write_str("partial"),
            Self::Retained => f.write_str("retained"),
        }
    }
}
impl ::std::str::FromStr for Report1EntryRecognitionStateV1Variant2Property0 {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "partial" => Ok(Self::Partial),
            "retained" => Ok(Self::Retained),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1EntryRecognitionStateV1Variant2Property0 {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Report1EntryRecognitionStateV1Variant2Property0 {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Report1EntryRecognitionUnitV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1EntryRecognitionUnitV1 {
    #[serde(rename = "effectiveEntryPointCount")]
    pub effective_entry_point_count: Common4Uint53,
    #[serde(rename = "effectiveSource")]
    pub effective_source: Report1EntryRecognitionUnitV1EffectiveSource,
    #[serde(rename = "entryPoints")]
    pub entry_points: Native2EntryPointRecognitionV1,
    #[serde(rename = "markerPath")]
    pub marker_path: Report1EntryRecognitionUnitV1MarkerPath,
    #[serde(rename = "recognitionId")]
    pub recognition_id: ::std::string::String,
    pub recognizers: ::std::vec::Vec<Report1RecognizerSummaryV1>,
    #[serde(rename = "rootPath")]
    pub root_path: Native2InternalUnitRootV1,
    #[serde(rename = "unitOrdinal")]
    pub unit_ordinal: Common4Uint53,
}
///`Report1EntryRecognitionUnitV1EffectiveSource`
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
pub enum Report1EntryRecognitionUnitV1EffectiveSource {
    #[serde(rename = "explicit")]
    Explicit,
    #[serde(rename = "none")]
    None,
    #[serde(rename = "recognized")]
    Recognized,
}
impl ::std::fmt::Display for Report1EntryRecognitionUnitV1EffectiveSource {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Explicit => f.write_str("explicit"),
            Self::None => f.write_str("none"),
            Self::Recognized => f.write_str("recognized"),
        }
    }
}
impl ::std::str::FromStr for Report1EntryRecognitionUnitV1EffectiveSource {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "explicit" => Ok(Self::Explicit),
            "none" => Ok(Self::None),
            "recognized" => Ok(Self::Recognized),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1EntryRecognitionUnitV1EffectiveSource {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Report1EntryRecognitionUnitV1EffectiveSource {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Report1EntryRecognitionUnitV1MarkerPath`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Report1EntryRecognitionUnitV1MarkerPath(::std::string::String);
impl ::std::ops::Deref for Report1EntryRecognitionUnitV1MarkerPath {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Report1EntryRecognitionUnitV1MarkerPath>
for ::std::string::String {
    fn from(value: Report1EntryRecognitionUnitV1MarkerPath) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Report1EntryRecognitionUnitV1MarkerPath {
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
impl ::std::convert::TryFrom<&str> for Report1EntryRecognitionUnitV1MarkerPath {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Report1EntryRecognitionUnitV1MarkerPath {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Report1EntryRecognitionUnitV1MarkerPath {
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
///`Report1EntryTraceV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(untagged, deny_unknown_fields)]
pub enum Report1EntryTraceV1 {
    Variant0 {
        cause: Report1EntryTraceV1Variant0Property0,
        state: ::serde_json::Value,
        #[serde(rename = "subjectId")]
        subject_id: Common4SubjectId,
    },
    Variant1 {
        cause: Report1EntryTraceV1Variant1Property0,
        #[serde(rename = "originQuery")]
        origin_query: Report1ReportGraphExchangeV1,
        #[serde(
            rename = "scopeUnitOrdinal",
            deserialize_with = "::std::option::Option::deserialize"
        )]
        scope_unit_ordinal: ::std::option::Option<Common4Uint53>,
        #[serde(rename = "scopeUniverse")]
        scope_universe: Common4Sha256Hex,
        state: ::serde_json::Value,
        #[serde(rename = "subjectId")]
        subject_id: Common4SubjectId,
    },
    Variant2 {
        blockers: ::std::vec::Vec<Report1EntryTraceV1Variant2BlockersItem>,
        interpretation: ::serde_json::Value,
        #[serde(rename = "originQuery")]
        origin_query: Report1ReportGraphExchangeV1,
        #[serde(rename = "originUniverses")]
        origin_universes: ::std::vec::Vec<Common4Sha256Hex>,
        #[serde(rename = "originsExamined")]
        origins_examined: Common4Uint53,
        #[serde(rename = "originsOutsideEntrySet")]
        origins_outside_entry_set: Common4Uint53,
        #[serde(rename = "originsUnattributed")]
        origins_unattributed: Common4Uint53,
        #[serde(
            rename = "scopeUnitOrdinal",
            deserialize_with = "::std::option::Option::deserialize"
        )]
        scope_unit_ordinal: ::std::option::Option<Common4Uint53>,
        #[serde(rename = "scopeUniverse")]
        scope_universe: Common4Sha256Hex,
        state: ::serde_json::Value,
        #[serde(rename = "subjectId")]
        subject_id: Common4SubjectId,
    },
    Variant3 {
        #[serde(rename = "originQuery")]
        origin_query: Report1ReportGraphExchangeV1,
        path: Report1ReportGraphExchangeV1,
        #[serde(
            rename = "scopeUnitOrdinal",
            deserialize_with = "::std::option::Option::deserialize"
        )]
        scope_unit_ordinal: ::std::option::Option<Common4Uint53>,
        #[serde(rename = "scopeUniverse")]
        scope_universe: Common4Sha256Hex,
        start: Report1EntryTraceV1Variant3Start,
        state: Report1EntryTraceV1Variant3State,
        #[serde(rename = "subjectId")]
        subject_id: Common4SubjectId,
    },
}
///`Report1EntryTraceV1Variant0Property0`
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
pub enum Report1EntryTraceV1Variant0Property0 {
    #[serde(rename = "recognition-not-plan-bound")]
    RecognitionNotPlanBound,
    #[serde(rename = "recognition-unavailable")]
    RecognitionUnavailable,
    #[serde(rename = "subject-descriptor-not-retained")]
    SubjectDescriptorNotRetained,
}
impl ::std::fmt::Display for Report1EntryTraceV1Variant0Property0 {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::RecognitionNotPlanBound => f.write_str("recognition-not-plan-bound"),
            Self::RecognitionUnavailable => f.write_str("recognition-unavailable"),
            Self::SubjectDescriptorNotRetained => {
                f.write_str("subject-descriptor-not-retained")
            }
        }
    }
}
impl ::std::str::FromStr for Report1EntryTraceV1Variant0Property0 {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "recognition-not-plan-bound" => Ok(Self::RecognitionNotPlanBound),
            "recognition-unavailable" => Ok(Self::RecognitionUnavailable),
            "subject-descriptor-not-retained" => Ok(Self::SubjectDescriptorNotRetained),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1EntryTraceV1Variant0Property0 {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Report1EntryTraceV1Variant0Property0 {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Report1EntryTraceV1Variant1Property0`
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
pub enum Report1EntryTraceV1Variant1Property0 {
    #[serde(rename = "origin-page-set-not-embedded")]
    OriginPageSetNotEmbedded,
    #[serde(rename = "reachability-evidence-unavailable")]
    ReachabilityEvidenceUnavailable,
}
impl ::std::fmt::Display for Report1EntryTraceV1Variant1Property0 {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::OriginPageSetNotEmbedded => f.write_str("origin-page-set-not-embedded"),
            Self::ReachabilityEvidenceUnavailable => {
                f.write_str("reachability-evidence-unavailable")
            }
        }
    }
}
impl ::std::str::FromStr for Report1EntryTraceV1Variant1Property0 {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "origin-page-set-not-embedded" => Ok(Self::OriginPageSetNotEmbedded),
            "reachability-evidence-unavailable" => {
                Ok(Self::ReachabilityEvidenceUnavailable)
            }
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1EntryTraceV1Variant1Property0 {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Report1EntryTraceV1Variant1Property0 {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Report1EntryTraceV1Variant2BlockersItem`
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
pub enum Report1EntryTraceV1Variant2BlockersItem {
    #[serde(rename = "entry-recognition-not-all")]
    EntryRecognitionNotAll,
    #[serde(rename = "evidence-limitations")]
    EvidenceLimitations,
    #[serde(rename = "origin-attribution-unavailable")]
    OriginAttributionUnavailable,
}
impl ::std::fmt::Display for Report1EntryTraceV1Variant2BlockersItem {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::EntryRecognitionNotAll => f.write_str("entry-recognition-not-all"),
            Self::EvidenceLimitations => f.write_str("evidence-limitations"),
            Self::OriginAttributionUnavailable => {
                f.write_str("origin-attribution-unavailable")
            }
        }
    }
}
impl ::std::str::FromStr for Report1EntryTraceV1Variant2BlockersItem {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "entry-recognition-not-all" => Ok(Self::EntryRecognitionNotAll),
            "evidence-limitations" => Ok(Self::EvidenceLimitations),
            "origin-attribution-unavailable" => Ok(Self::OriginAttributionUnavailable),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1EntryTraceV1Variant2BlockersItem {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Report1EntryTraceV1Variant2BlockersItem {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Report1EntryTraceV1Variant3Start`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1EntryTraceV1Variant3Start {
    #[serde(rename = "attributionPath")]
    pub attribution_path: Common4LogicalPath,
    pub endpoint: Graph4GraphEndpoint,
    pub entry: Report1EntryTraceV1Variant3StartEntry,
    #[serde(rename = "viaReachabilityFactId")]
    pub via_reachability_fact_id: Graph4FactId,
}
///`Report1EntryTraceV1Variant3StartEntry`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1EntryTraceV1Variant3StartEntry {
    pub path: Common4LogicalPath,
    pub provenance: ::std::vec::Vec<Report1EntryProvenanceV1>,
}
///`Report1EntryTraceV1Variant3State`
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
pub enum Report1EntryTraceV1Variant3State {
    #[serde(rename = "path-found")]
    PathFound,
    #[serde(rename = "path-not-within-bound")]
    PathNotWithinBound,
}
impl ::std::fmt::Display for Report1EntryTraceV1Variant3State {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::PathFound => f.write_str("path-found"),
            Self::PathNotWithinBound => f.write_str("path-not-within-bound"),
        }
    }
}
impl ::std::str::FromStr for Report1EntryTraceV1Variant3State {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "path-found" => Ok(Self::PathFound),
            "path-not-within-bound" => Ok(Self::PathNotWithinBound),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1EntryTraceV1Variant3State {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Report1EntryTraceV1Variant3State {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Report1EvidencePanelStateV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(untagged, deny_unknown_fields)]
pub enum Report1EvidencePanelStateV1 {
    Object { data: Report1EvidencePanelV1, state: ::serde_json::Value },
    Report1PanelNotPresentV1(Report1PanelNotPresentV1),
}
impl ::std::convert::From<Report1PanelNotPresentV1> for Report1EvidencePanelStateV1 {
    fn from(value: Report1PanelNotPresentV1) -> Self {
        Self::Report1PanelNotPresentV1(value)
    }
}
///`Report1EvidencePanelV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1EvidencePanelV1 {
    pub entries: ::std::vec::Vec<Report1EvidencePanelV1EntriesItem>,
    #[serde(rename = "entriesProjection")]
    pub entries_projection: Report1ItemProjectionV1,
    pub provenance: Report1EvidencePanelV1Provenance,
    ///Exact retained Run/evidence or ephemeral Plan/evidence binding. Ephemeral evidence has no Run identity or retained-history authority.
    pub source: Report1EvidencePanelV1Source,
}
///`Report1EvidencePanelV1EntriesItem`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1EvidencePanelV1EntriesItem {
    #[serde(rename = "coverageId")]
    pub coverage_id: ::std::string::String,
    pub descriptor: Identity3Coverage,
    pub result: Native2CoverageResultV3,
}
///`Report1EvidencePanelV1Provenance`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1EvidencePanelV1Provenance {
    #[serde(rename = "hostAsserted")]
    pub host_asserted: ::serde_json::Value,
    #[serde(rename = "verifiedInDocument")]
    pub verified_in_document: ::serde_json::Value,
}
///Exact retained Run/evidence or ephemeral Plan/evidence binding. Ephemeral evidence has no Run identity or retained-history authority.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(untagged, deny_unknown_fields)]
pub enum Report1EvidencePanelV1Source {
    Variant0 {
        #[serde(rename = "evidenceId")]
        evidence_id: ::std::string::String,
        #[serde(rename = "runId")]
        run_id: ::std::string::String,
    },
    Variant1 {
        #[serde(rename = "evidenceId")]
        evidence_id: ::std::string::String,
        #[serde(rename = "planId")]
        plan_id: ::std::string::String,
    },
}
///`Report1FeatureId`
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
pub enum Report1FeatureId {
    #[serde(rename = "catalog-run-statistics")]
    CatalogRunStatistics,
}
impl ::std::fmt::Display for Report1FeatureId {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::CatalogRunStatistics => f.write_str("catalog-run-statistics"),
        }
    }
}
impl ::std::str::FromStr for Report1FeatureId {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "catalog-run-statistics" => Ok(Self::CatalogRunStatistics),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1FeatureId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Report1FeatureId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Required inventory feature not delivered by this carrier, with its precise cause and design obligation (owner/design-obligations.v1.json). Disclosure only: it never satisfies delivery of the feature.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1FeatureStateV1 {
    #[serde(rename = "featureId")]
    pub feature_id: Report1FeatureId,
    #[serde(rename = "obligationId")]
    pub obligation_id: ::std::string::String,
    pub reason: Report1FeatureStateV1Reason,
    pub state: ::serde_json::Value,
    pub view: Report1ReportViewId,
}
///`Report1FeatureStateV1Reason`
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
pub enum Report1FeatureStateV1Reason {
    #[serde(rename = "no-admitted-owner")]
    NoAdmittedOwner,
    #[serde(rename = "no-query-carrier")]
    NoQueryCarrier,
    #[serde(rename = "no-redaction-owner")]
    NoRedactionOwner,
    #[serde(rename = "no-selection-interface")]
    NoSelectionInterface,
    #[serde(rename = "owner-carrier-field-absent")]
    OwnerCarrierFieldAbsent,
    #[serde(rename = "owner-data-not-retained")]
    OwnerDataNotRetained,
}
impl ::std::fmt::Display for Report1FeatureStateV1Reason {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::NoAdmittedOwner => f.write_str("no-admitted-owner"),
            Self::NoQueryCarrier => f.write_str("no-query-carrier"),
            Self::NoRedactionOwner => f.write_str("no-redaction-owner"),
            Self::NoSelectionInterface => f.write_str("no-selection-interface"),
            Self::OwnerCarrierFieldAbsent => f.write_str("owner-carrier-field-absent"),
            Self::OwnerDataNotRetained => f.write_str("owner-data-not-retained"),
        }
    }
}
impl ::std::str::FromStr for Report1FeatureStateV1Reason {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "no-admitted-owner" => Ok(Self::NoAdmittedOwner),
            "no-query-carrier" => Ok(Self::NoQueryCarrier),
            "no-redaction-owner" => Ok(Self::NoRedactionOwner),
            "no-selection-interface" => Ok(Self::NoSelectionInterface),
            "owner-carrier-field-absent" => Ok(Self::OwnerCarrierFieldAbsent),
            "owner-data-not-retained" => Ok(Self::OwnerDataNotRetained),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1FeatureStateV1Reason {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Report1FeatureStateV1Reason {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Report1GraphPanelStateV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(untagged, deny_unknown_fields)]
pub enum Report1GraphPanelStateV1 {
    Object { data: Report1GraphPanelV1, state: ::serde_json::Value },
    Report1PanelNotPresentV1(Report1PanelNotPresentV1),
}
impl ::std::convert::From<Report1PanelNotPresentV1> for Report1GraphPanelStateV1 {
    fn from(value: Report1PanelNotPresentV1) -> Self {
        Self::Report1PanelNotPresentV1(value)
    }
}
///`Report1GraphPanelV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1GraphPanelV1 {
    pub policy: ::serde_json::Value,
    pub provenance: Report1GraphPanelV1Provenance,
    pub slots: ::std::vec::Vec<Report1GraphSlotV1>,
    #[serde(rename = "slotsProjection")]
    pub slots_projection: Report1ItemProjectionV1,
    #[serde(rename = "subjectIndex")]
    pub subject_index: ::std::vec::Vec<Report1GraphPanelV1SubjectIndexItem>,
    #[serde(rename = "subjectResolution")]
    pub subject_resolution: ::std::vec::Vec<Report1SubjectResolutionV1>,
}
///`Report1GraphPanelV1Provenance`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1GraphPanelV1Provenance {
    #[serde(rename = "hostAsserted")]
    pub host_asserted: ::serde_json::Value,
    #[serde(rename = "verifiedInDocument")]
    pub verified_in_document: ::serde_json::Value,
}
///`Report1GraphPanelV1SubjectIndexItem`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1GraphPanelV1SubjectIndexItem {
    pub endpoint: Graph4GraphEndpoint,
    #[serde(rename = "subjectId")]
    pub subject_id: Common4SubjectId,
}
///`Report1GraphSlotV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1GraphSlotV1 {
    #[serde(rename = "anchorSubjectIds")]
    pub anchor_subject_ids: ::std::vec::Vec<Common4SubjectId>,
    #[serde(rename = "hostProjection")]
    pub host_projection: Report1GraphSlotV1HostProjection,
    pub ordinal: i64,
    pub purpose: Report1GraphSlotV1Purpose,
    pub request: Report1GraphSlotV1Request,
    pub response: Report1GraphSlotV1Response,
}
///`Report1GraphSlotV1HostProjection`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1GraphSlotV1HostProjection {
    pub continuation: Report1GraphSlotV1HostProjectionContinuation,
    #[serde(rename = "pageSizeCause")]
    pub page_size_cause: Report1GraphSlotV1HostProjectionPageSizeCause,
    #[serde(
        rename = "rejectedByteDelta",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub rejected_byte_delta: FieldPresence<::std::option::Option<Common4Uint53>>,
}
///`Report1GraphSlotV1HostProjectionContinuation`
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
pub enum Report1GraphSlotV1HostProjectionContinuation {
    #[serde(rename = "complete-page-set")]
    CompletePageSet,
    #[serde(rename = "not-embedded")]
    NotEmbedded,
    #[serde(rename = "operation-truncated-no-continuation")]
    OperationTruncatedNoContinuation,
}
impl ::std::fmt::Display for Report1GraphSlotV1HostProjectionContinuation {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::CompletePageSet => f.write_str("complete-page-set"),
            Self::NotEmbedded => f.write_str("not-embedded"),
            Self::OperationTruncatedNoContinuation => {
                f.write_str("operation-truncated-no-continuation")
            }
        }
    }
}
impl ::std::str::FromStr for Report1GraphSlotV1HostProjectionContinuation {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "complete-page-set" => Ok(Self::CompletePageSet),
            "not-embedded" => Ok(Self::NotEmbedded),
            "operation-truncated-no-continuation" => {
                Ok(Self::OperationTruncatedNoContinuation)
            }
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1GraphSlotV1HostProjectionContinuation {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Report1GraphSlotV1HostProjectionContinuation {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Report1GraphSlotV1HostProjectionPageSizeCause`
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
pub enum Report1GraphSlotV1HostProjectionPageSizeCause {
    #[serde(rename = "ladder-first")]
    LadderFirst,
    #[serde(rename = "byte-budget-reduced")]
    ByteBudgetReduced,
}
impl ::std::fmt::Display for Report1GraphSlotV1HostProjectionPageSizeCause {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::LadderFirst => f.write_str("ladder-first"),
            Self::ByteBudgetReduced => f.write_str("byte-budget-reduced"),
        }
    }
}
impl ::std::str::FromStr for Report1GraphSlotV1HostProjectionPageSizeCause {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "ladder-first" => Ok(Self::LadderFirst),
            "byte-budget-reduced" => Ok(Self::ByteBudgetReduced),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1GraphSlotV1HostProjectionPageSizeCause {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Report1GraphSlotV1HostProjectionPageSizeCause {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Report1GraphSlotV1Purpose`
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
pub enum Report1GraphSlotV1Purpose {
    #[serde(rename = "neighborhood")]
    Neighborhood,
    #[serde(rename = "package-coupling")]
    PackageCoupling,
    #[serde(rename = "reach")]
    Reach,
    #[serde(rename = "path")]
    Path,
}
impl ::std::fmt::Display for Report1GraphSlotV1Purpose {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Neighborhood => f.write_str("neighborhood"),
            Self::PackageCoupling => f.write_str("package-coupling"),
            Self::Reach => f.write_str("reach"),
            Self::Path => f.write_str("path"),
        }
    }
}
impl ::std::str::FromStr for Report1GraphSlotV1Purpose {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "neighborhood" => Ok(Self::Neighborhood),
            "package-coupling" => Ok(Self::PackageCoupling),
            "reach" => Ok(Self::Reach),
            "path" => Ok(Self::Path),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1GraphSlotV1Purpose {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Report1GraphSlotV1Purpose {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Report1GraphSlotV1Request`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1GraphSlotV1Request {
    pub completeness: Report1GraphSlotV1RequestCompleteness,
    pub operation: Graph4GraphOperation,
    pub page: Report1GraphSlotV1RequestPage,
    ///Closed per operation by the allOf joins below. Graph ops use GraphNeighborsParams/GraphPathParams/GraphReachParams. Other 17 operations keep Params.
    pub params: ::serde_json::Map<::std::string::String, ::serde_json::Value>,
    #[serde(rename = "projectId")]
    pub project_id: Common4ProjectId,
    #[serde(rename = "schemaFamily")]
    pub schema_family: ::serde_json::Value,
    #[serde(rename = "schemaMajor")]
    pub schema_major: ExactInteger,
    pub view: Graph4ResolvedView,
}
///`Report1GraphSlotV1RequestCompleteness`
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
pub enum Report1GraphSlotV1RequestCompleteness {
    #[serde(rename = "best-effort")]
    BestEffort,
}
impl ::std::fmt::Display for Report1GraphSlotV1RequestCompleteness {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::BestEffort => f.write_str("best-effort"),
        }
    }
}
impl ::std::str::FromStr for Report1GraphSlotV1RequestCompleteness {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "best-effort" => Ok(Self::BestEffort),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1GraphSlotV1RequestCompleteness {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Report1GraphSlotV1RequestCompleteness {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Report1GraphSlotV1RequestPage`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1GraphSlotV1RequestPage {
    pub size: ::std::num::NonZeroU64,
}
///`Report1GraphSlotV1Response`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1GraphSlotV1Response {
    pub context: ::serde_json::Map<::std::string::String, ::serde_json::Value>,
    pub items: ::std::vec::Vec<::serde_json::Value>,
    pub operation: Graph4GraphOperation,
    #[serde(rename = "schemaFamily")]
    pub schema_family: ::serde_json::Value,
    #[serde(rename = "schemaMajor")]
    pub schema_major: ExactInteger,
}
///`Report1HistoryPanelStateV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(untagged, deny_unknown_fields)]
pub enum Report1HistoryPanelStateV1 {
    Object { data: Report1HistoryPanelV1, state: ::serde_json::Value },
    Report1PanelNotPresentV1(Report1PanelNotPresentV1),
}
impl ::std::convert::From<Report1PanelNotPresentV1> for Report1HistoryPanelStateV1 {
    fn from(value: Report1PanelNotPresentV1) -> Self {
        Self::Report1PanelNotPresentV1(value)
    }
}
///`Report1HistoryPanelV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(untagged)]
pub enum Report1HistoryPanelV1 {
    Report1AutomaticHistoryPanelV1(Report1AutomaticHistoryPanelV1),
    ExplicitHistoryPanel1Root(ExplicitHistoryPanel1Root),
}
impl ::std::convert::From<Report1AutomaticHistoryPanelV1> for Report1HistoryPanelV1 {
    fn from(value: Report1AutomaticHistoryPanelV1) -> Self {
        Self::Report1AutomaticHistoryPanelV1(value)
    }
}
impl ::std::convert::From<ExplicitHistoryPanel1Root> for Report1HistoryPanelV1 {
    fn from(value: ExplicitHistoryPanel1Root) -> Self {
        Self::ExplicitHistoryPanel1Root(value)
    }
}
///`Report1HistoryRunV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(tag = "state", deny_unknown_fields)]
pub enum Report1HistoryRunV1 {
    #[serde(rename = "present")]
    Present {
        #[serde(
            rename = "commitSequence",
            deserialize_with = "::std::option::Option::deserialize"
        )]
        commit_sequence: ::std::option::Option<u64>,
        findings: ::std::vec::Vec<Common4FindingSurface>,
        #[serde(rename = "findingsProjection")]
        findings_projection: Report1ItemProjectionV1,
        run: Report1HistoryRunV1Run,
        #[serde(rename = "runId")]
        run_id: Common4RunId,
    },
    #[serde(rename = "unavailable")]
    Unavailable {
        availability: Report1HistoryRunV1Availability,
        #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
        detail: FieldPresence<::std::option::Option<Common4DomainDetail>>,
        #[serde(rename = "runId")]
        run_id: Common4RunId,
    },
}
///`Report1HistoryRunV1Availability`
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
pub enum Report1HistoryRunV1Availability {
    #[serde(rename = "expired")]
    Expired,
    #[serde(rename = "purged")]
    Purged,
    #[serde(rename = "corrupt")]
    Corrupt,
    #[serde(rename = "unavailable")]
    Unavailable,
}
impl ::std::fmt::Display for Report1HistoryRunV1Availability {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Expired => f.write_str("expired"),
            Self::Purged => f.write_str("purged"),
            Self::Corrupt => f.write_str("corrupt"),
            Self::Unavailable => f.write_str("unavailable"),
        }
    }
}
impl ::std::str::FromStr for Report1HistoryRunV1Availability {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "expired" => Ok(Self::Expired),
            "purged" => Ok(Self::Purged),
            "corrupt" => Ok(Self::Corrupt),
            "unavailable" => Ok(Self::Unavailable),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1HistoryRunV1Availability {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Report1HistoryRunV1Availability {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Report1HistoryRunV1Run`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1HistoryRunV1Run {
    pub authority: Report1HistoryRunV1RunAuthority,
    #[serde(
        rename = "comparisonResultId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub comparison_result_id: FieldPresence<
        ::std::option::Option<Common4ComparisonResultId>,
    >,
    #[serde(
        rename = "coverageId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub coverage_id: FieldPresence<::std::option::Option<Common4CoverageId>>,
    pub deficiency: Common4D9Deficiency,
    pub durability: ::serde_json::Value,
    pub kind: Report1HistoryRunV1RunKind,
    #[serde(rename = "planId")]
    pub plan_id: Common4PlanId,
    #[serde(rename = "requiredCoverage")]
    pub required_coverage: Common4RequiredCoverage,
    #[serde(rename = "runId")]
    pub run_id: Common4RunId,
    #[serde(rename = "secondaryDeficiencies")]
    pub secondary_deficiencies: ::std::vec::Vec<Common4D9Deficiency>,
    pub verdict: Common4Verdict,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub verification: FieldPresence<
        ::std::option::Option<Invocation5VerificationOutcome>,
    >,
}
///`Report1HistoryRunV1RunAuthority`
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
pub enum Report1HistoryRunV1RunAuthority {
    #[serde(rename = "authoritative")]
    Authoritative,
}
impl ::std::fmt::Display for Report1HistoryRunV1RunAuthority {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Authoritative => f.write_str("authoritative"),
        }
    }
}
impl ::std::str::FromStr for Report1HistoryRunV1RunAuthority {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "authoritative" => Ok(Self::Authoritative),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1HistoryRunV1RunAuthority {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Report1HistoryRunV1RunAuthority {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Report1HistoryRunV1RunKind`
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
pub enum Report1HistoryRunV1RunKind {
    #[serde(rename = "analysis")]
    Analysis,
    #[serde(rename = "verify")]
    Verify,
}
impl ::std::fmt::Display for Report1HistoryRunV1RunKind {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Analysis => f.write_str("analysis"),
            Self::Verify => f.write_str("verify"),
        }
    }
}
impl ::std::str::FromStr for Report1HistoryRunV1RunKind {
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
impl ::std::convert::TryFrom<&str> for Report1HistoryRunV1RunKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Report1HistoryRunV1RunKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Report-at-render projection of the selected invocation owner. Current producers use invocation5; legacy attempt observation majors remain explicit. This projection does not select a codec or retention policy for the full InvocationRecord (L01).
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1InvocationLedgerV1 {
    ///No observed cancellation has no signal value. A requested cancellation carries the invocation owner signal/phase. Absence of the optional InvocationRecord.cancellation projects to the explicit none state.
    pub cancellation: Report1InvocationLedgerV1Cancellation,
    #[serde(rename = "missingChildren")]
    pub missing_children: ::std::vec::Vec<Report1InvocationLedgerV1MissingChildrenItem>,
    pub mode: Invocation5Mode,
    ///The owner/builtin-step-planning.v1.json variant this invocation planned; its planning condition is a host assertion.
    #[serde(rename = "planVariant")]
    pub plan_variant: Report1InvocationLedgerV1PlanVariant,
    pub provenance: Report1InvocationLedgerV1Provenance,
    #[serde(rename = "requestId")]
    pub request_id: Common4RequestId,
    pub steps: ::std::vec::Vec<Report1LedgerStepV1>,
    pub workflow: Invocation5WorkflowRef,
}
///No observed cancellation has no signal value. A requested cancellation carries the invocation owner signal/phase. Absence of the optional InvocationRecord.cancellation projects to the explicit none state.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(untagged, deny_unknown_fields)]
pub enum Report1InvocationLedgerV1Cancellation {
    Variant0 { phase: ::std::string::String, requested: bool },
    Variant1 {
        ///before-settle: at least one required step had not reached a terminal outcome; aggregate is interrupted (130). after-settle: every required step already reached a terminal outcome; the aggregate termination is not reclassified.
        phase: Report1InvocationLedgerV1CancellationVariant1Phase,
        requested: bool,
        signal: Common4D9Signal,
    },
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
pub enum Report1InvocationLedgerV1CancellationVariant1Phase {
    #[serde(rename = "none")]
    None,
    #[serde(rename = "before-settle")]
    BeforeSettle,
    #[serde(rename = "after-settle")]
    AfterSettle,
}
impl ::std::fmt::Display for Report1InvocationLedgerV1CancellationVariant1Phase {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::None => f.write_str("none"),
            Self::BeforeSettle => f.write_str("before-settle"),
            Self::AfterSettle => f.write_str("after-settle"),
        }
    }
}
impl ::std::str::FromStr for Report1InvocationLedgerV1CancellationVariant1Phase {
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
impl ::std::convert::TryFrom<&str>
for Report1InvocationLedgerV1CancellationVariant1Phase {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Report1InvocationLedgerV1CancellationVariant1Phase {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Report1InvocationLedgerV1MissingChildrenItem`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1InvocationLedgerV1MissingChildrenItem {
    pub missing: Report1InvocationLedgerV1MissingChildrenItemMissing,
    #[serde(rename = "stepId")]
    pub step_id: Common4StepId,
}
///`Report1InvocationLedgerV1MissingChildrenItemMissing`
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
pub enum Report1InvocationLedgerV1MissingChildrenItemMissing {
    #[serde(rename = "render-in-progress")]
    RenderInProgress,
    #[serde(rename = "step-result-not-recorded")]
    StepResultNotRecorded,
    #[serde(rename = "attempts-not-recorded")]
    AttemptsNotRecorded,
}
impl ::std::fmt::Display for Report1InvocationLedgerV1MissingChildrenItemMissing {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::RenderInProgress => f.write_str("render-in-progress"),
            Self::StepResultNotRecorded => f.write_str("step-result-not-recorded"),
            Self::AttemptsNotRecorded => f.write_str("attempts-not-recorded"),
        }
    }
}
impl ::std::str::FromStr for Report1InvocationLedgerV1MissingChildrenItemMissing {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "render-in-progress" => Ok(Self::RenderInProgress),
            "step-result-not-recorded" => Ok(Self::StepResultNotRecorded),
            "attempts-not-recorded" => Ok(Self::AttemptsNotRecorded),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str>
for Report1InvocationLedgerV1MissingChildrenItemMissing {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Report1InvocationLedgerV1MissingChildrenItemMissing {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///The owner/builtin-step-planning.v1.json variant this invocation planned; its planning condition is a host assertion.
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
pub enum Report1InvocationLedgerV1PlanVariant {
    #[serde(rename = "baseline-no-pivot")]
    BaselineNoPivot,
    #[serde(rename = "baseline-with-pivot")]
    BaselineWithPivot,
    #[serde(rename = "no-pivot")]
    NoPivot,
    #[serde(rename = "primary")]
    Primary,
    #[serde(rename = "primary-with-optional-export")]
    PrimaryWithOptionalExport,
    #[serde(rename = "with-pivot")]
    WithPivot,
}
impl ::std::fmt::Display for Report1InvocationLedgerV1PlanVariant {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::BaselineNoPivot => f.write_str("baseline-no-pivot"),
            Self::BaselineWithPivot => f.write_str("baseline-with-pivot"),
            Self::NoPivot => f.write_str("no-pivot"),
            Self::Primary => f.write_str("primary"),
            Self::PrimaryWithOptionalExport => {
                f.write_str("primary-with-optional-export")
            }
            Self::WithPivot => f.write_str("with-pivot"),
        }
    }
}
impl ::std::str::FromStr for Report1InvocationLedgerV1PlanVariant {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "baseline-no-pivot" => Ok(Self::BaselineNoPivot),
            "baseline-with-pivot" => Ok(Self::BaselineWithPivot),
            "no-pivot" => Ok(Self::NoPivot),
            "primary" => Ok(Self::Primary),
            "primary-with-optional-export" => Ok(Self::PrimaryWithOptionalExport),
            "with-pivot" => Ok(Self::WithPivot),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1InvocationLedgerV1PlanVariant {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Report1InvocationLedgerV1PlanVariant {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Report1InvocationLedgerV1Provenance`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1InvocationLedgerV1Provenance {
    #[serde(rename = "hostAsserted")]
    pub host_asserted: ::serde_json::Value,
    #[serde(rename = "verifiedInDocument")]
    pub verified_in_document: ::serde_json::Value,
}
///`Report1ItemProjectionV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1ItemProjectionV1 {
    #[serde(rename = "omissionCause")]
    pub omission_cause: Report1ItemProjectionV1OmissionCause,
    pub omitted: Common4Uint53,
    #[serde(
        rename = "rejectedByteDelta",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub rejected_byte_delta: FieldPresence<::std::option::Option<Common4Uint53>>,
    pub total: Common4Uint53,
}
///`Report1ItemProjectionV1OmissionCause`
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
pub enum Report1ItemProjectionV1OmissionCause {
    #[serde(rename = "none")]
    None,
    #[serde(rename = "item-cap")]
    ItemCap,
    #[serde(rename = "byte-budget")]
    ByteBudget,
}
impl ::std::fmt::Display for Report1ItemProjectionV1OmissionCause {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::None => f.write_str("none"),
            Self::ItemCap => f.write_str("item-cap"),
            Self::ByteBudget => f.write_str("byte-budget"),
        }
    }
}
impl ::std::str::FromStr for Report1ItemProjectionV1OmissionCause {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "none" => Ok(Self::None),
            "item-cap" => Ok(Self::ItemCap),
            "byte-budget" => Ok(Self::ByteBudget),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1ItemProjectionV1OmissionCause {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Report1ItemProjectionV1OmissionCause {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Report1LedgerStepV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1LedgerStepV1 {
    #[serde(
        rename = "analysisRunId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub analysis_run_id: FieldPresence<::std::option::Option<Common4RunId>>,
    #[serde(rename = "attemptServiceTime")]
    pub attempt_service_time: Report1AttemptServiceTimeV1,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub attempts: FieldPresence<::std::vec::Vec<Report1LedgerStepV1AttemptsItem>>,
    #[serde(rename = "dependencyGate")]
    pub dependency_gate: Invocation5StepSpecPropertiesDependencyGate,
    #[serde(rename = "dependsOn")]
    pub depends_on: Invocation5StepSpecPropertiesDependsOn,
    pub kind: Invocation5StepKind,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub outcome: FieldPresence<::std::option::Option<Invocation5StepOutcome>>,
    #[serde(rename = "planRole")]
    pub plan_role: Report1LedgerStepV1PlanRole,
    pub recorded: bool,
    pub requirement: Invocation5StepSpecPropertiesRequirement,
    #[serde(
        rename = "skipReason",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub skip_reason: FieldPresence<
        ::std::option::Option<Invocation5StepResultPropertiesSkipReason>,
    >,
    #[serde(rename = "stepId")]
    pub step_id: Common4StepId,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub termination: FieldPresence<::std::option::Option<Common4StepTermination>>,
}
///`Report1LedgerStepV1AttemptsItem`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1LedgerStepV1AttemptsItem {
    pub duration: Report1LedgerStepV1AttemptsItemDuration,
    #[serde(rename = "executionId")]
    pub execution_id: Invocation5AttemptPropertiesExecutionId,
    #[serde(
        rename = "faultCause",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub fault_cause: FieldPresence<
        ::std::option::Option<Invocation5AttemptPropertiesFaultCause>,
    >,
    pub outcome: Invocation5AttemptPropertiesOutcome,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub retried: FieldPresence<
        ::std::option::Option<Invocation5AttemptPropertiesRetried>,
    >,
    #[serde(rename = "sourceSchemaMajor")]
    pub source_schema_major: ExactInteger,
}
///`Report1LedgerStepV1AttemptsItemDuration`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(untagged, deny_unknown_fields)]
pub enum Report1LedgerStepV1AttemptsItemDuration {
    Invocation5AttemptDurationV1(Invocation5AttemptDurationV1),
    Object { reason: ::std::string::String, state: ::std::string::String },
}
impl ::std::convert::From<Invocation5AttemptDurationV1>
for Report1LedgerStepV1AttemptsItemDuration {
    fn from(value: Invocation5AttemptDurationV1) -> Self {
        Self::Invocation5AttemptDurationV1(value)
    }
}
///`Report1LedgerStepV1PlanRole`
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
pub enum Report1LedgerStepV1PlanRole {
    #[serde(rename = "primary-analysis")]
    PrimaryAnalysis,
    #[serde(rename = "pivot-analysis")]
    PivotAnalysis,
    #[serde(rename = "comparison")]
    Comparison,
    #[serde(rename = "query")]
    Query,
    #[serde(rename = "repair-preview")]
    RepairPreview,
    #[serde(rename = "import")]
    Import,
    #[serde(rename = "render")]
    Render,
    #[serde(rename = "export-delivery")]
    ExportDelivery,
}
impl ::std::fmt::Display for Report1LedgerStepV1PlanRole {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::PrimaryAnalysis => f.write_str("primary-analysis"),
            Self::PivotAnalysis => f.write_str("pivot-analysis"),
            Self::Comparison => f.write_str("comparison"),
            Self::Query => f.write_str("query"),
            Self::RepairPreview => f.write_str("repair-preview"),
            Self::Import => f.write_str("import"),
            Self::Render => f.write_str("render"),
            Self::ExportDelivery => f.write_str("export-delivery"),
        }
    }
}
impl ::std::str::FromStr for Report1LedgerStepV1PlanRole {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "primary-analysis" => Ok(Self::PrimaryAnalysis),
            "pivot-analysis" => Ok(Self::PivotAnalysis),
            "comparison" => Ok(Self::Comparison),
            "query" => Ok(Self::Query),
            "repair-preview" => Ok(Self::RepairPreview),
            "import" => Ok(Self::Import),
            "render" => Ok(Self::Render),
            "export-delivery" => Ok(Self::ExportDelivery),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1LedgerStepV1PlanRole {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Report1LedgerStepV1PlanRole {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Report1PanelNotPresentV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(tag = "state", deny_unknown_fields)]
pub enum Report1PanelNotPresentV1 {
    #[serde(rename = "omitted")]
    Omitted { reason: Report1PanelNotPresentV1Variant0Property0 },
    #[serde(rename = "unavailable")]
    Unavailable {
        #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
        detail: FieldPresence<::std::option::Option<Common4DomainDetail>>,
        reason: Report1PanelNotPresentV1Variant1Property1,
    },
    #[serde(rename = "corrupt")]
    Corrupt {
        #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
        detail: FieldPresence<::std::option::Option<Common4DomainDetail>>,
        reason: ::serde_json::Value,
    },
    #[serde(rename = "incompatible")]
    Incompatible {
        #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
        detail: FieldPresence<::std::option::Option<Common4DomainDetail>>,
        reason: ::serde_json::Value,
    },
}
///`Report1PanelNotPresentV1Variant0Property0`
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
pub enum Report1PanelNotPresentV1Variant0Property0 {
    #[serde(rename = "not-selected")]
    NotSelected,
    #[serde(rename = "exploration-budget-exceeded")]
    ExplorationBudgetExceeded,
}
impl ::std::fmt::Display for Report1PanelNotPresentV1Variant0Property0 {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::NotSelected => f.write_str("not-selected"),
            Self::ExplorationBudgetExceeded => f.write_str("exploration-budget-exceeded"),
        }
    }
}
impl ::std::str::FromStr for Report1PanelNotPresentV1Variant0Property0 {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "not-selected" => Ok(Self::NotSelected),
            "exploration-budget-exceeded" => Ok(Self::ExplorationBudgetExceeded),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1PanelNotPresentV1Variant0Property0 {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Report1PanelNotPresentV1Variant0Property0 {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Report1PanelNotPresentV1Variant1Property1`
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
pub enum Report1PanelNotPresentV1Variant1Property1 {
    #[serde(rename = "no-admitted-result")]
    NoAdmittedResult,
    #[serde(rename = "no-run-identity")]
    NoRunIdentity,
    #[serde(rename = "evidence-expired")]
    EvidenceExpired,
    #[serde(rename = "evidence-purged")]
    EvidencePurged,
    #[serde(rename = "evidence-missing")]
    EvidenceMissing,
    #[serde(rename = "source-refused")]
    SourceRefused,
    #[serde(rename = "prerequisite-panel-not-present")]
    PrerequisitePanelNotPresent,
}
impl ::std::fmt::Display for Report1PanelNotPresentV1Variant1Property1 {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::NoAdmittedResult => f.write_str("no-admitted-result"),
            Self::NoRunIdentity => f.write_str("no-run-identity"),
            Self::EvidenceExpired => f.write_str("evidence-expired"),
            Self::EvidencePurged => f.write_str("evidence-purged"),
            Self::EvidenceMissing => f.write_str("evidence-missing"),
            Self::SourceRefused => f.write_str("source-refused"),
            Self::PrerequisitePanelNotPresent => {
                f.write_str("prerequisite-panel-not-present")
            }
        }
    }
}
impl ::std::str::FromStr for Report1PanelNotPresentV1Variant1Property1 {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "no-admitted-result" => Ok(Self::NoAdmittedResult),
            "no-run-identity" => Ok(Self::NoRunIdentity),
            "evidence-expired" => Ok(Self::EvidenceExpired),
            "evidence-purged" => Ok(Self::EvidencePurged),
            "evidence-missing" => Ok(Self::EvidenceMissing),
            "source-refused" => Ok(Self::SourceRefused),
            "prerequisite-panel-not-present" => Ok(Self::PrerequisitePanelNotPresent),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1PanelNotPresentV1Variant1Property1 {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Report1PanelNotPresentV1Variant1Property1 {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Report1PanelsV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug, Default)]
#[serde(deny_unknown_fields)]
pub struct Report1PanelsV1 {
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub catalog: FieldPresence<::std::option::Option<Report1CatalogPanelStateV1>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub comparison: FieldPresence<::std::option::Option<Report1ComparisonPanelStateV1>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub configuration: FieldPresence<
        ::std::option::Option<Report1ConfigurationPanelStateV1>,
    >,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub coupling: FieldPresence<::std::option::Option<Report1CouplingPanelStateV1>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub descriptions: FieldPresence<
        ::std::option::Option<Report1DescriptionsPanelStateV1>,
    >,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub evidence: FieldPresence<::std::option::Option<Report1EvidencePanelStateV1>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub graph: FieldPresence<::std::option::Option<Report1GraphPanelStateV1>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub history: FieldPresence<::std::option::Option<Report1HistoryPanelStateV1>>,
    #[serde(
        rename = "symbolEvidence",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub symbol_evidence: FieldPresence<
        ::std::option::Option<Report1SymbolEvidencePanelStateV1>,
    >,
}
///`Report1PathDisclosureV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(tag = "mode", content = "editorScheme")]
pub enum Report1PathDisclosureV1 {
    #[serde(rename = "relative-only")]
    RelativeOnly,
    #[serde(rename = "local-editor-links")]
    LocalEditorLinks(Report1PathDisclosureV1EditorScheme),
}
impl ::std::convert::From<Report1PathDisclosureV1EditorScheme>
for Report1PathDisclosureV1 {
    fn from(value: Report1PathDisclosureV1EditorScheme) -> Self {
        Self::LocalEditorLinks(value)
    }
}
///`Report1PathDisclosureV1EditorScheme`
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
pub enum Report1PathDisclosureV1EditorScheme {
    #[serde(rename = "vscode")]
    Vscode,
    #[serde(rename = "vscode-insiders")]
    VscodeInsiders,
    #[serde(rename = "idea")]
    Idea,
}
impl ::std::fmt::Display for Report1PathDisclosureV1EditorScheme {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Vscode => f.write_str("vscode"),
            Self::VscodeInsiders => f.write_str("vscode-insiders"),
            Self::Idea => f.write_str("idea"),
        }
    }
}
impl ::std::str::FromStr for Report1PathDisclosureV1EditorScheme {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "vscode" => Ok(Self::Vscode),
            "vscode-insiders" => Ok(Self::VscodeInsiders),
            "idea" => Ok(Self::Idea),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1PathDisclosureV1EditorScheme {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Report1PathDisclosureV1EditorScheme {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Exactly the selected preview RecipeRef; capability/rule keys are empty and recipe keys contain exactly this one recipe. Actual evidence source, targets and applicability remain the existing envelope RepairPlanDescriptor.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1RecipeDescriptionsV1 {
    pub receipt: Report1DescriptionReceiptV1,
    pub recipe: Repair2RecipeRef,
    #[serde(rename = "repairPlanId")]
    pub repair_plan_id: Common4RepairPlanId,
    pub selection: Report1RecipeDescriptionsV1Selection,
}
///`Report1RecipeDescriptionsV1Selection`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1RecipeDescriptionsV1Selection {
    pub capabilities: ::std::vec::Vec<(Common4CanonicalIdentifier,)>,
    #[serde(rename = "closureId")]
    pub closure_id: Common4ClosureId,
    pub recipes: ::std::vec::Vec<
        (Common4ContributionId, Common4CanonicalIdentifier, Common4SemanticVersion),
    >,
    pub rules: ::std::vec::Vec<
        (Common1ContributionId, Common1CanonicalIdentifier, u16, Common1Sha256Hex),
    >,
}
///`Report1RecognizerSummaryV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1RecognizerSummaryV1 {
    pub assurance: Native2FrameworkRecognitionResultV1PropertiesAssurance,
    #[serde(rename = "entryPointCount")]
    pub entry_point_count: i64,
    pub evidence: Native2FrameworkRecognitionResultV1PropertiesEvidence,
    #[serde(rename = "recognizerId")]
    pub recognizer_id: Native2FrameworkRecognitionResultV1PropertiesRecognizerId,
    #[serde(rename = "recognizerVersion")]
    pub recognizer_version: ExactInteger,
    #[serde(rename = "testGlobs")]
    pub test_globs: Native2FrameworkRecognitionResultV1PropertiesEffectsPropertiesTestGlobs,
    #[serde(rename = "unresolvedChoices")]
    pub unresolved_choices: Native2FrameworkRecognitionResultV1PropertiesUnresolvedChoices,
}
///Exactly the command-inventory:5 commands whose formats contain html.
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
pub enum Report1ReportCommand {
    #[serde(rename = "default")]
    Default,
    #[serde(rename = "analyze")]
    Analyze,
    #[serde(rename = "fit")]
    Fit,
    #[serde(rename = "audit")]
    Audit,
    #[serde(rename = "candidates")]
    Candidates,
    #[serde(rename = "inspect")]
    Inspect,
    #[serde(rename = "review-brief")]
    ReviewBrief,
    #[serde(rename = "repair-preview")]
    RepairPreview,
}
impl ::std::fmt::Display for Report1ReportCommand {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Default => f.write_str("default"),
            Self::Analyze => f.write_str("analyze"),
            Self::Fit => f.write_str("fit"),
            Self::Audit => f.write_str("audit"),
            Self::Candidates => f.write_str("candidates"),
            Self::Inspect => f.write_str("inspect"),
            Self::ReviewBrief => f.write_str("review-brief"),
            Self::RepairPreview => f.write_str("repair-preview"),
        }
    }
}
impl ::std::str::FromStr for Report1ReportCommand {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "default" => Ok(Self::Default),
            "analyze" => Ok(Self::Analyze),
            "fit" => Ok(Self::Fit),
            "audit" => Ok(Self::Audit),
            "candidates" => Ok(Self::Candidates),
            "inspect" => Ok(Self::Inspect),
            "review-brief" => Ok(Self::ReviewBrief),
            "repair-preview" => Ok(Self::RepairPreview),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1ReportCommand {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Report1ReportCommand {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Report1ReportGraphExchangeV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1ReportGraphExchangeV1 {
    pub request: Graph4GraphQueryRequestV1,
    pub response: Graph4GraphQueryResponseV1,
}
///`Report1ReportReachContextV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1ReportReachContextV1 {
    pub request: Graph4GraphQueryRequestV1,
    #[serde(rename = "responseContext")]
    pub response_context: Graph4GraphOperationResponseContext,
}
///`Report1ReportViewId`
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
pub enum Report1ReportViewId {
    #[serde(rename = "overview")]
    Overview,
    #[serde(rename = "findings")]
    Findings,
    #[serde(rename = "candidate-list")]
    CandidateList,
    #[serde(rename = "candidate-inspection")]
    CandidateInspection,
    #[serde(rename = "review-brief")]
    ReviewBrief,
    #[serde(rename = "repair-preview")]
    RepairPreview,
    #[serde(rename = "evidence")]
    Evidence,
    #[serde(rename = "comparison")]
    Comparison,
    #[serde(rename = "history")]
    History,
    #[serde(rename = "catalog")]
    Catalog,
    #[serde(rename = "graph")]
    Graph,
    #[serde(rename = "symbol-detail")]
    SymbolDetail,
}
impl ::std::fmt::Display for Report1ReportViewId {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Overview => f.write_str("overview"),
            Self::Findings => f.write_str("findings"),
            Self::CandidateList => f.write_str("candidate-list"),
            Self::CandidateInspection => f.write_str("candidate-inspection"),
            Self::ReviewBrief => f.write_str("review-brief"),
            Self::RepairPreview => f.write_str("repair-preview"),
            Self::Evidence => f.write_str("evidence"),
            Self::Comparison => f.write_str("comparison"),
            Self::History => f.write_str("history"),
            Self::Catalog => f.write_str("catalog"),
            Self::Graph => f.write_str("graph"),
            Self::SymbolDetail => f.write_str("symbol-detail"),
        }
    }
}
impl ::std::str::FromStr for Report1ReportViewId {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "overview" => Ok(Self::Overview),
            "findings" => Ok(Self::Findings),
            "candidate-list" => Ok(Self::CandidateList),
            "candidate-inspection" => Ok(Self::CandidateInspection),
            "review-brief" => Ok(Self::ReviewBrief),
            "repair-preview" => Ok(Self::RepairPreview),
            "evidence" => Ok(Self::Evidence),
            "comparison" => Ok(Self::Comparison),
            "history" => Ok(Self::History),
            "catalog" => Ok(Self::Catalog),
            "graph" => Ok(Self::Graph),
            "symbol-detail" => Ok(Self::SymbolDetail),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1ReportViewId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Report1ReportViewId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Data document embedded in html v1 output of the eight command-inventory:5 html commands. envelope (command-envelope:6, jointly selected with its envelope5 parent) is the only parity source. invocationLedger projects this invocation's invocation:3 record including cancellation. Panels carry typed optional exploration data with explicit states, separated limit layers and provenance distinguishing checked joins from host assertions. featureStates disclose undelivered required features with precise causes and design obligations; they never satisfy delivery. Report codec, envelope5 host admission, ledger and cancellation joins, slot and history policies, owner page law, subject-index recomputation, derived root bounds and the byte law against the remaining document budget are admission rules of contract.md enforced by check.py. Joint candidate adds configuration, explicit history selection and attempt service observations. Present data requires its owner joins; complete composed budget derivation and actual fixture integration remain pending.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1Root {
    #[serde(rename = "budgetProfile")]
    pub budget_profile: Report1BudgetProfileV1,
    pub command: Report1ReportCommand,
    pub disclosures: Report1DisclosuresV1,
    #[serde(rename = "documentProvenance")]
    pub document_provenance: Report1RootDocumentProvenance,
    pub envelope: Report1RootEnvelope,
    #[serde(rename = "featureStates")]
    pub feature_states: ::std::vec::Vec<Report1FeatureStateV1>,
    #[serde(rename = "invocationLedger")]
    pub invocation_ledger: Report1InvocationLedgerV1,
    pub panels: Report1PanelsV1,
    #[serde(rename = "pathDisclosure")]
    pub path_disclosure: Report1PathDisclosureV1,
    pub renderer: Report1RootRenderer,
    #[serde(rename = "reportObservedAt")]
    pub report_observed_at: Common4UtcTimestamp,
    #[serde(rename = "schemaFamily")]
    pub schema_family: ::serde_json::Value,
    #[serde(rename = "schemaMajor")]
    pub schema_major: ExactInteger,
    #[serde(rename = "staticParity")]
    pub static_parity: Report1StaticParityV1,
    #[serde(rename = "supportedReportViews")]
    pub supported_report_views: ::std::vec::Vec<Report1ReportViewId>,
}
///`Report1RootDocumentProvenance`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1RootDocumentProvenance {
    #[serde(rename = "hostAsserted")]
    pub host_asserted: ::serde_json::Value,
    #[serde(rename = "verifiedInDocument")]
    pub verified_in_document: ::serde_json::Value,
}
///`Report1RootEnvelope`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1RootEnvelope {
    ///Required exactly on the fit command's kind=run envelope (inventory5 advisoryDispatch). Never alters run, findings, verdict or termination.
    #[serde(
        rename = "advisoryReport",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub advisory_report: FieldPresence<
        ::std::option::Option<Envelope7FitAdvisoryReportV1>,
    >,
    ///Optional. The bounded capability-availability collection of THIS invocation: every capability the selected product required that this release did not declare available, with its full ownership tuple. Present on the invocation that selected them - it is not deferred to a separate doctor report, which is a different invocation and cannot deliver these absences. Advisory only.
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub availability: FieldPresence<
        ::std::option::Option<Common4CapabilityAvailabilityV1>,
    >,
    #[serde(
        rename = "clientCorrelationId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub client_correlation_id: FieldPresence<
        ::std::option::Option<Report1RootEnvelopeClientCorrelationId>,
    >,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub diagnostics: FieldPresence<::std::vec::Vec<Common4BoundedText>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub doctor: FieldPresence<::std::option::Option<Invocation5DoctorResult>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub errors: FieldPresence<::std::vec::Vec<Common4DomainDetail>>,
    #[serde(rename = "exitCode")]
    pub exit_code: ExactInteger,
    ///Optional direct findings projection for analysis envelopes. One row per finding3. Not keyed by fingerprint.
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub findings: FieldPresence<
        ::std::option::Option<::std::vec::Vec<Common4FindingSurface>>,
    >,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub invocation: FieldPresence<::std::option::Option<Invocation5Root>>,
    pub kind: Report1RootEnvelopeKind,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub meta: FieldPresence<::std::option::Option<Metadata1Root>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub mutation: FieldPresence<
        ::std::option::Option<Envelope7MutationReceiptProjection>,
    >,
    #[serde(
        rename = "projectId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub project_id: FieldPresence<::std::option::Option<Common4ProjectId>>,
    #[serde(
        rename = "projectRoot",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub project_root: FieldPresence<::std::option::Option<Common4UserInputPath>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub query: FieldPresence<::std::option::Option<Invocation5QueryResult>>,
    ///Closed typed result of a non-graph query-class command, discriminated by surface; no untyped payload is admitted.
    #[serde(
        rename = "queryRecord",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub query_record: FieldPresence<
        ::std::option::Option<Report1RootEnvelopeQueryRecord>,
    >,
    ///The complete owner-admitted query response, required exactly when querySurface=graph-query-response. Cross-record joins beyond JSON Schema: context.projectId equals projectId; a present response termination equals termination; for graph.* the query summary is the owner projection of this response.
    #[serde(
        rename = "queryResponse",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub query_response: FieldPresence<::std::option::Option<Graph4GraphQueryResponseV1>>,
    ///Required exactly on kind=query and equal to the command inventory queryDispatch.surface. graph-query-response carries queryResponse; every other value carries queryRecord of exactly its record type.
    #[serde(
        rename = "querySurface",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub query_surface: FieldPresence<
        ::std::option::Option<Report1RootEnvelopeQuerySurface>,
    >,
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
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub run: FieldPresence<::std::option::Option<Invocation5AnalysisResult>>,
    #[serde(rename = "schemaFamily")]
    pub schema_family: ::serde_json::Value,
    #[serde(rename = "schemaMajor")]
    pub schema_major: ExactInteger,
    pub termination: Common4StepTermination,
}
///`Report1RootEnvelopeClientCorrelationId`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Report1RootEnvelopeClientCorrelationId(::std::string::String);
impl ::std::ops::Deref for Report1RootEnvelopeClientCorrelationId {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Report1RootEnvelopeClientCorrelationId>
for ::std::string::String {
    fn from(value: Report1RootEnvelopeClientCorrelationId) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Report1RootEnvelopeClientCorrelationId {
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
impl ::std::convert::TryFrom<&str> for Report1RootEnvelopeClientCorrelationId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Report1RootEnvelopeClientCorrelationId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Report1RootEnvelopeClientCorrelationId {
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
///`Report1RootEnvelopeKind`
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
pub enum Report1RootEnvelopeKind {
    #[serde(rename = "run")]
    Run,
    #[serde(rename = "query")]
    Query,
    #[serde(rename = "failure")]
    Failure,
}
impl ::std::fmt::Display for Report1RootEnvelopeKind {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Run => f.write_str("run"),
            Self::Query => f.write_str("query"),
            Self::Failure => f.write_str("failure"),
        }
    }
}
impl ::std::str::FromStr for Report1RootEnvelopeKind {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "run" => Ok(Self::Run),
            "query" => Ok(Self::Query),
            "failure" => Ok(Self::Failure),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1RootEnvelopeKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Report1RootEnvelopeKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Closed typed result of a non-graph query-class command, discriminated by surface; no untyped payload is admitted.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(untagged)]
pub enum Report1RootEnvelopeQueryRecord {
    DiscoveryRecommendationRecordV1(Envelope7DiscoveryRecommendationRecordV1),
    BaselineInspectionRecordV1(Envelope7BaselineInspectionRecordV1),
    EffectivePolicyRecordV1(Envelope7EffectivePolicyRecordV1),
    PolicyTestResultRecordV1(Envelope7PolicyTestResultRecordV1),
    CandidateListRecordV1(Envelope7CandidateListRecordV1),
    CandidateInspectionRecordV1(Envelope7CandidateInspectionRecordV1),
    ReviewBriefRecordV1(Envelope7ReviewBriefRecordV1),
    RepairPreviewRecordV1(Envelope7RepairPreviewRecordV1),
}
impl ::std::convert::From<Envelope7DiscoveryRecommendationRecordV1>
for Report1RootEnvelopeQueryRecord {
    fn from(value: Envelope7DiscoveryRecommendationRecordV1) -> Self {
        Self::DiscoveryRecommendationRecordV1(value)
    }
}
impl ::std::convert::From<Envelope7BaselineInspectionRecordV1>
for Report1RootEnvelopeQueryRecord {
    fn from(value: Envelope7BaselineInspectionRecordV1) -> Self {
        Self::BaselineInspectionRecordV1(value)
    }
}
impl ::std::convert::From<Envelope7EffectivePolicyRecordV1>
for Report1RootEnvelopeQueryRecord {
    fn from(value: Envelope7EffectivePolicyRecordV1) -> Self {
        Self::EffectivePolicyRecordV1(value)
    }
}
impl ::std::convert::From<Envelope7PolicyTestResultRecordV1>
for Report1RootEnvelopeQueryRecord {
    fn from(value: Envelope7PolicyTestResultRecordV1) -> Self {
        Self::PolicyTestResultRecordV1(value)
    }
}
impl ::std::convert::From<Envelope7CandidateListRecordV1>
for Report1RootEnvelopeQueryRecord {
    fn from(value: Envelope7CandidateListRecordV1) -> Self {
        Self::CandidateListRecordV1(value)
    }
}
impl ::std::convert::From<Envelope7CandidateInspectionRecordV1>
for Report1RootEnvelopeQueryRecord {
    fn from(value: Envelope7CandidateInspectionRecordV1) -> Self {
        Self::CandidateInspectionRecordV1(value)
    }
}
impl ::std::convert::From<Envelope7ReviewBriefRecordV1>
for Report1RootEnvelopeQueryRecord {
    fn from(value: Envelope7ReviewBriefRecordV1) -> Self {
        Self::ReviewBriefRecordV1(value)
    }
}
impl ::std::convert::From<Envelope7RepairPreviewRecordV1>
for Report1RootEnvelopeQueryRecord {
    fn from(value: Envelope7RepairPreviewRecordV1) -> Self {
        Self::RepairPreviewRecordV1(value)
    }
}
///Required exactly on kind=query and equal to the command inventory queryDispatch.surface. graph-query-response carries queryResponse; every other value carries queryRecord of exactly its record type.
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
pub enum Report1RootEnvelopeQuerySurface {
    #[serde(rename = "graph-query-response")]
    GraphQueryResponse,
    #[serde(rename = "discovery-recommendation")]
    DiscoveryRecommendation,
    #[serde(rename = "baseline-inspection")]
    BaselineInspection,
    #[serde(rename = "effective-policy")]
    EffectivePolicy,
    #[serde(rename = "policy-test-result")]
    PolicyTestResult,
    #[serde(rename = "candidate-list")]
    CandidateList,
    #[serde(rename = "candidate-inspection")]
    CandidateInspection,
    #[serde(rename = "review-brief")]
    ReviewBrief,
    #[serde(rename = "repair-preview")]
    RepairPreview,
}
impl ::std::fmt::Display for Report1RootEnvelopeQuerySurface {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::GraphQueryResponse => f.write_str("graph-query-response"),
            Self::DiscoveryRecommendation => f.write_str("discovery-recommendation"),
            Self::BaselineInspection => f.write_str("baseline-inspection"),
            Self::EffectivePolicy => f.write_str("effective-policy"),
            Self::PolicyTestResult => f.write_str("policy-test-result"),
            Self::CandidateList => f.write_str("candidate-list"),
            Self::CandidateInspection => f.write_str("candidate-inspection"),
            Self::ReviewBrief => f.write_str("review-brief"),
            Self::RepairPreview => f.write_str("repair-preview"),
        }
    }
}
impl ::std::str::FromStr for Report1RootEnvelopeQuerySurface {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "graph-query-response" => Ok(Self::GraphQueryResponse),
            "discovery-recommendation" => Ok(Self::DiscoveryRecommendation),
            "baseline-inspection" => Ok(Self::BaselineInspection),
            "effective-policy" => Ok(Self::EffectivePolicy),
            "policy-test-result" => Ok(Self::PolicyTestResult),
            "candidate-list" => Ok(Self::CandidateList),
            "candidate-inspection" => Ok(Self::CandidateInspection),
            "review-brief" => Ok(Self::ReviewBrief),
            "repair-preview" => Ok(Self::RepairPreview),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1RootEnvelopeQuerySurface {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Report1RootEnvelopeQuerySurface {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Report1RootRenderer`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1RootRenderer {
    pub format: ::serde_json::Value,
    pub version: ExactInteger,
}
///`Report1RuleCatalogV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1RuleCatalogV1 {
    #[serde(rename = "gateSeverityAtLeast")]
    pub gate_severity_at_least: Policy2Severity,
    pub provenance: Report1RuleCatalogV1Provenance,
    pub rules: ::std::vec::Vec<Policy2Rule>,
    pub source: Report1RuleCatalogV1Source,
}
///`Report1RuleCatalogV1Provenance`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1RuleCatalogV1Provenance {
    #[serde(rename = "hostAsserted")]
    pub host_asserted: ::serde_json::Value,
    #[serde(rename = "verifiedInDocument")]
    pub verified_in_document: ::serde_json::Value,
}
///`Report1RuleCatalogV1Source`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1RuleCatalogV1Source {
    pub kind: ::serde_json::Value,
    #[serde(rename = "planId")]
    pub plan_id: Common4PlanId,
    #[serde(rename = "policyDigest")]
    pub policy_digest: Common4Sha256Hex,
}
///Capabilities/rules only: recipe selection keys are empty. Closures and keys derive from this exact Run Plan, policy and native release; document indices are not authority.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1RunDescriptionsV1 {
    #[serde(rename = "planId")]
    pub plan_id: Common4PlanId,
    pub receipts: ::std::vec::Vec<Report1DescriptionReceiptV1>,
    #[serde(rename = "runId")]
    pub run_id: Common4RunId,
    pub selection: ::std::vec::Vec<Report1RunDescriptionsV1SelectionItem>,
}
///`Report1RunDescriptionsV1SelectionItem`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1RunDescriptionsV1SelectionItem {
    pub capabilities: ::std::vec::Vec<(Common4CanonicalIdentifier,)>,
    #[serde(rename = "closureId")]
    pub closure_id: Common4ClosureId,
    pub recipes: ::std::vec::Vec<
        (Common4ContributionId, Common4CanonicalIdentifier, Common4SemanticVersion),
    >,
    pub rules: ::std::vec::Vec<
        (Common1ContributionId, Common1CanonicalIdentifier, u16, Common1Sha256Hex),
    >,
}
///Digest of the script-independent static parity section: declared parity pointer lines, disclosure count lines, then the canonical envelope. Admission recomputes it.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1StaticParityV1 {
    pub format: ::serde_json::Value,
    #[serde(rename = "textBytes")]
    pub text_bytes: Common4Uint53,
    #[serde(rename = "textSha256")]
    pub text_sha256: Common4Sha256Hex,
}
///`Report1SubjectResolutionV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(tag = "state", deny_unknown_fields)]
pub enum Report1SubjectResolutionV1 {
    #[serde(rename = "resolved")]
    Resolved {
        endpoint: Graph4GraphEndpoint,
        #[serde(rename = "subjectId")]
        subject_id: Common4SubjectId,
    },
    #[serde(rename = "descriptor-not-retained")]
    DescriptorNotRetained {
        #[serde(rename = "subjectId")]
        subject_id: Common4SubjectId,
    },
}
///`Report1SymbolEvidencePanelStateV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(untagged, deny_unknown_fields)]
pub enum Report1SymbolEvidencePanelStateV1 {
    Object { data: Report1SymbolEvidencePanelV1, state: ::serde_json::Value },
    Report1PanelNotPresentV1(Report1PanelNotPresentV1),
}
impl ::std::convert::From<Report1PanelNotPresentV1>
for Report1SymbolEvidencePanelStateV1 {
    fn from(value: Report1PanelNotPresentV1) -> Self {
        Self::Report1PanelNotPresentV1(value)
    }
}
///`Report1SymbolEvidencePanelV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1SymbolEvidencePanelV1 {
    #[serde(rename = "entryRecognition")]
    pub entry_recognition: Report1EntryRecognitionStateV1,
    #[serde(rename = "metricCatalog")]
    pub metric_catalog: ::serde_json::Value,
    pub metrics: ::std::vec::Vec<Report1SymbolMetricV1>,
    #[serde(rename = "metricsProjection")]
    pub metrics_projection: Report1ItemProjectionV1,
    pub policy: ::serde_json::Value,
    pub provenance: Report1SymbolEvidencePanelV1Provenance,
    #[serde(rename = "runId")]
    pub run_id: Common4RunId,
    #[serde(rename = "testOrigins")]
    pub test_origins: ::std::vec::Vec<Report1TestOriginSetV1>,
    #[serde(rename = "testOriginsProjection")]
    pub test_origins_projection: Report1ItemProjectionV1,
    #[serde(rename = "testReachability")]
    pub test_reachability: ::std::vec::Vec<Report1TestReachabilityV1>,
    #[serde(rename = "testReachabilityProjection")]
    pub test_reachability_projection: Report1ItemProjectionV1,
    pub traces: ::std::vec::Vec<Report1EntryTraceV1>,
    #[serde(rename = "tracesProjection")]
    pub traces_projection: Report1ItemProjectionV1,
}
///`Report1SymbolEvidencePanelV1Provenance`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1SymbolEvidencePanelV1Provenance {
    #[serde(rename = "hostAsserted")]
    pub host_asserted: ::serde_json::Value,
    #[serde(rename = "verifiedInDocument")]
    pub verified_in_document: ::serde_json::Value,
}
///`Report1SymbolMetricV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(untagged, deny_unknown_fields)]
pub enum Report1SymbolMetricV1 {
    Variant0 {
        #[serde(rename = "countState")]
        count_state: Report1SymbolMetricV1Variant0CountState,
        interpretation: ::serde_json::Value,
        #[serde(rename = "limitationKinds")]
        limitation_kinds: ::std::vec::Vec<
            Graph4GraphEvidenceDisclosurePropertiesResolutionLimitationsItemsPropertiesKind,
        >,
        #[serde(rename = "metricId")]
        metric_id: Report1SymbolMetricV1Variant0MetricId,
        request: Graph4GraphQueryRequestV1,
        response: Graph4GraphQueryResponseV1,
        #[serde(rename = "subjectId")]
        subject_id: Common4SubjectId,
        value: Common4Uint53,
        #[serde(rename = "zeroSupportsAbsence")]
        zero_supports_absence: bool,
    },
    Variant1 {
        cause: ::serde_json::Value,
        #[serde(rename = "countState")]
        count_state: ::serde_json::Value,
        interpretation: ::serde_json::Value,
        #[serde(rename = "metricId")]
        metric_id: Report1SymbolMetricV1Variant1MetricId,
        request: Graph4GraphQueryRequestV1,
        response: Graph4GraphQueryResponseV1,
        #[serde(rename = "subjectId")]
        subject_id: Common4SubjectId,
    },
    Variant2 {
        cause: ::serde_json::Value,
        #[serde(rename = "countState")]
        count_state: ::serde_json::Value,
        #[serde(rename = "metricId")]
        metric_id: Report1SymbolMetricV1Variant2MetricId,
        #[serde(rename = "subjectId")]
        subject_id: Common4SubjectId,
    },
}
///`Report1SymbolMetricV1Variant0CountState`
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
pub enum Report1SymbolMetricV1Variant0CountState {
    #[serde(rename = "exact")]
    Exact,
    #[serde(rename = "lower-bound")]
    LowerBound,
}
impl ::std::fmt::Display for Report1SymbolMetricV1Variant0CountState {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Exact => f.write_str("exact"),
            Self::LowerBound => f.write_str("lower-bound"),
        }
    }
}
impl ::std::str::FromStr for Report1SymbolMetricV1Variant0CountState {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "exact" => Ok(Self::Exact),
            "lower-bound" => Ok(Self::LowerBound),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1SymbolMetricV1Variant0CountState {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Report1SymbolMetricV1Variant0CountState {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Report1SymbolMetricV1Variant0MetricId`
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
pub enum Report1SymbolMetricV1Variant0MetricId {
    #[serde(rename = "distinct-resolved-callees-within-1-hop")]
    DistinctResolvedCalleesWithin1Hop,
    #[serde(rename = "distinct-resolved-callers-within-1-hop")]
    DistinctResolvedCallersWithin1Hop,
    #[serde(rename = "resolved-call-facts-incoming")]
    ResolvedCallFactsIncoming,
    #[serde(rename = "resolved-call-facts-outgoing")]
    ResolvedCallFactsOutgoing,
    #[serde(rename = "resolved-reference-facts-incoming")]
    ResolvedReferenceFactsIncoming,
}
impl ::std::fmt::Display for Report1SymbolMetricV1Variant0MetricId {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::DistinctResolvedCalleesWithin1Hop => {
                f.write_str("distinct-resolved-callees-within-1-hop")
            }
            Self::DistinctResolvedCallersWithin1Hop => {
                f.write_str("distinct-resolved-callers-within-1-hop")
            }
            Self::ResolvedCallFactsIncoming => {
                f.write_str("resolved-call-facts-incoming")
            }
            Self::ResolvedCallFactsOutgoing => {
                f.write_str("resolved-call-facts-outgoing")
            }
            Self::ResolvedReferenceFactsIncoming => {
                f.write_str("resolved-reference-facts-incoming")
            }
        }
    }
}
impl ::std::str::FromStr for Report1SymbolMetricV1Variant0MetricId {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "distinct-resolved-callees-within-1-hop" => {
                Ok(Self::DistinctResolvedCalleesWithin1Hop)
            }
            "distinct-resolved-callers-within-1-hop" => {
                Ok(Self::DistinctResolvedCallersWithin1Hop)
            }
            "resolved-call-facts-incoming" => Ok(Self::ResolvedCallFactsIncoming),
            "resolved-call-facts-outgoing" => Ok(Self::ResolvedCallFactsOutgoing),
            "resolved-reference-facts-incoming" => {
                Ok(Self::ResolvedReferenceFactsIncoming)
            }
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1SymbolMetricV1Variant0MetricId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Report1SymbolMetricV1Variant0MetricId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Report1SymbolMetricV1Variant1MetricId`
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
pub enum Report1SymbolMetricV1Variant1MetricId {
    #[serde(rename = "distinct-resolved-callees-within-1-hop")]
    DistinctResolvedCalleesWithin1Hop,
    #[serde(rename = "distinct-resolved-callers-within-1-hop")]
    DistinctResolvedCallersWithin1Hop,
    #[serde(rename = "resolved-call-facts-incoming")]
    ResolvedCallFactsIncoming,
    #[serde(rename = "resolved-call-facts-outgoing")]
    ResolvedCallFactsOutgoing,
    #[serde(rename = "resolved-reference-facts-incoming")]
    ResolvedReferenceFactsIncoming,
}
impl ::std::fmt::Display for Report1SymbolMetricV1Variant1MetricId {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::DistinctResolvedCalleesWithin1Hop => {
                f.write_str("distinct-resolved-callees-within-1-hop")
            }
            Self::DistinctResolvedCallersWithin1Hop => {
                f.write_str("distinct-resolved-callers-within-1-hop")
            }
            Self::ResolvedCallFactsIncoming => {
                f.write_str("resolved-call-facts-incoming")
            }
            Self::ResolvedCallFactsOutgoing => {
                f.write_str("resolved-call-facts-outgoing")
            }
            Self::ResolvedReferenceFactsIncoming => {
                f.write_str("resolved-reference-facts-incoming")
            }
        }
    }
}
impl ::std::str::FromStr for Report1SymbolMetricV1Variant1MetricId {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "distinct-resolved-callees-within-1-hop" => {
                Ok(Self::DistinctResolvedCalleesWithin1Hop)
            }
            "distinct-resolved-callers-within-1-hop" => {
                Ok(Self::DistinctResolvedCallersWithin1Hop)
            }
            "resolved-call-facts-incoming" => Ok(Self::ResolvedCallFactsIncoming),
            "resolved-call-facts-outgoing" => Ok(Self::ResolvedCallFactsOutgoing),
            "resolved-reference-facts-incoming" => {
                Ok(Self::ResolvedReferenceFactsIncoming)
            }
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1SymbolMetricV1Variant1MetricId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Report1SymbolMetricV1Variant1MetricId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Report1SymbolMetricV1Variant2MetricId`
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
pub enum Report1SymbolMetricV1Variant2MetricId {
    #[serde(rename = "distinct-resolved-callees-within-1-hop")]
    DistinctResolvedCalleesWithin1Hop,
    #[serde(rename = "distinct-resolved-callers-within-1-hop")]
    DistinctResolvedCallersWithin1Hop,
    #[serde(rename = "resolved-call-facts-incoming")]
    ResolvedCallFactsIncoming,
    #[serde(rename = "resolved-call-facts-outgoing")]
    ResolvedCallFactsOutgoing,
    #[serde(rename = "resolved-reference-facts-incoming")]
    ResolvedReferenceFactsIncoming,
}
impl ::std::fmt::Display for Report1SymbolMetricV1Variant2MetricId {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::DistinctResolvedCalleesWithin1Hop => {
                f.write_str("distinct-resolved-callees-within-1-hop")
            }
            Self::DistinctResolvedCallersWithin1Hop => {
                f.write_str("distinct-resolved-callers-within-1-hop")
            }
            Self::ResolvedCallFactsIncoming => {
                f.write_str("resolved-call-facts-incoming")
            }
            Self::ResolvedCallFactsOutgoing => {
                f.write_str("resolved-call-facts-outgoing")
            }
            Self::ResolvedReferenceFactsIncoming => {
                f.write_str("resolved-reference-facts-incoming")
            }
        }
    }
}
impl ::std::str::FromStr for Report1SymbolMetricV1Variant2MetricId {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "distinct-resolved-callees-within-1-hop" => {
                Ok(Self::DistinctResolvedCalleesWithin1Hop)
            }
            "distinct-resolved-callers-within-1-hop" => {
                Ok(Self::DistinctResolvedCallersWithin1Hop)
            }
            "resolved-call-facts-incoming" => Ok(Self::ResolvedCallFactsIncoming),
            "resolved-call-facts-outgoing" => Ok(Self::ResolvedCallFactsOutgoing),
            "resolved-reference-facts-incoming" => {
                Ok(Self::ResolvedReferenceFactsIncoming)
            }
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1SymbolMetricV1Variant2MetricId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Report1SymbolMetricV1Variant2MetricId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Report1TestOriginEvidenceV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(tag = "kind", deny_unknown_fields)]
pub enum Report1TestOriginEvidenceV1 {
    #[serde(rename = "rust-test-target")]
    RustTestTarget {
        #[serde(rename = "unitIds")]
        unit_ids: ::std::vec::Vec<::std::string::String>,
    },
    #[serde(rename = "recognized-test-glob")]
    RecognizedTestGlob {
        glob: Report1TestOriginEvidenceV1Glob,
        #[serde(rename = "recognizerId")]
        recognizer_id: ::serde_json::Value,
        #[serde(rename = "relativePath")]
        relative_path: Common4LogicalPath,
        #[serde(rename = "unitOrdinal")]
        unit_ordinal: Common4Uint53,
    },
}
///`Report1TestOriginEvidenceV1Glob`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Report1TestOriginEvidenceV1Glob(::std::string::String);
impl ::std::ops::Deref for Report1TestOriginEvidenceV1Glob {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Report1TestOriginEvidenceV1Glob> for ::std::string::String {
    fn from(value: Report1TestOriginEvidenceV1Glob) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Report1TestOriginEvidenceV1Glob {
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
impl ::std::convert::TryFrom<&str> for Report1TestOriginEvidenceV1Glob {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Report1TestOriginEvidenceV1Glob {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Report1TestOriginEvidenceV1Glob {
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
///Exact static test origin identity of one program universe. No origin set is ever complete: recognizer globs are defaults, Rust in-target tests are not target facts, and imported TestPayloadV1 execution observations never identify origins.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(tag = "source", deny_unknown_fields)]
pub enum Report1TestOriginSetV1 {
    #[serde(rename = "none")]
    None {
        cause: Report1TestOriginSetV1Cause,
        completeness: ::serde_json::Value,
        interpretation: ::serde_json::Value,
        limitations: ::std::vec::Vec<Report1TestOriginSetV1Variant0Property3Item>,
        #[serde(rename = "originCount")]
        origin_count: ExactInteger,
        universe: Common4Sha256Hex,
    },
    #[serde(rename = "rust-test-targets")]
    RustTestTargets {
        completeness: ::serde_json::Value,
        evidence: Report1TestOriginSetV1Variant1Property1,
        interpretation: ::serde_json::Value,
        limitations: ::std::vec::Vec<Report1TestOriginSetV1Variant1Property3Item>,
        #[serde(rename = "originCount")]
        origin_count: Common4Uint53,
        universe: Common4Sha256Hex,
    },
    #[serde(rename = "recognized-test-globs")]
    RecognizedTestGlobs {
        completeness: ::serde_json::Value,
        evidence: Report1TestOriginSetV1Variant2Property1,
        interpretation: ::serde_json::Value,
        limitations: ::std::vec::Vec<Report1TestOriginSetV1Variant2Property3Item>,
        #[serde(rename = "originCount")]
        origin_count: Common4Uint53,
        universe: Common4Sha256Hex,
    },
}
///`Report1TestOriginSetV1Cause`
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
pub enum Report1TestOriginSetV1Cause {
    #[serde(rename = "no-test-recognizer")]
    NoTestRecognizer,
    #[serde(rename = "ownership-missing")]
    OwnershipMissing,
    #[serde(rename = "recognition-not-plan-bound")]
    RecognitionNotPlanBound,
    #[serde(rename = "recognition-unavailable")]
    RecognitionUnavailable,
    #[serde(rename = "unsupported-language-family")]
    UnsupportedLanguageFamily,
    #[serde(rename = "universe-not-plan-bound")]
    UniverseNotPlanBound,
}
impl ::std::fmt::Display for Report1TestOriginSetV1Cause {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::NoTestRecognizer => f.write_str("no-test-recognizer"),
            Self::OwnershipMissing => f.write_str("ownership-missing"),
            Self::RecognitionNotPlanBound => f.write_str("recognition-not-plan-bound"),
            Self::RecognitionUnavailable => f.write_str("recognition-unavailable"),
            Self::UnsupportedLanguageFamily => f.write_str("unsupported-language-family"),
            Self::UniverseNotPlanBound => f.write_str("universe-not-plan-bound"),
        }
    }
}
impl ::std::str::FromStr for Report1TestOriginSetV1Cause {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "no-test-recognizer" => Ok(Self::NoTestRecognizer),
            "ownership-missing" => Ok(Self::OwnershipMissing),
            "recognition-not-plan-bound" => Ok(Self::RecognitionNotPlanBound),
            "recognition-unavailable" => Ok(Self::RecognitionUnavailable),
            "unsupported-language-family" => Ok(Self::UnsupportedLanguageFamily),
            "universe-not-plan-bound" => Ok(Self::UniverseNotPlanBound),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1TestOriginSetV1Cause {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Report1TestOriginSetV1Cause {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Report1TestOriginSetV1Variant0Property3Item`
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
pub enum Report1TestOriginSetV1Variant0Property3Item {
    #[serde(rename = "foreign-unit-paths-not-matched")]
    ForeignUnitPathsNotMatched,
    #[serde(rename = "in-target-unit-tests-not-identified")]
    InTargetUnitTestsNotIdentified,
    #[serde(rename = "no-selected-test-targets")]
    NoSelectedTestTargets,
    #[serde(rename = "ownership-enumeration-partial")]
    OwnershipEnumerationPartial,
    #[serde(rename = "recognizer-globs-not-test-population")]
    RecognizerGlobsNotTestPopulation,
    #[serde(rename = "recognizer-unresolved-choices")]
    RecognizerUnresolvedChoices,
    #[serde(rename = "shared-test-and-non-test-target-path")]
    SharedTestAndNonTestTargetPath,
    #[serde(rename = "symbol-attribution-conflict")]
    SymbolAttributionConflict,
    #[serde(rename = "symbol-inventory-incomplete")]
    SymbolInventoryIncomplete,
    #[serde(rename = "test-selection-configured")]
    TestSelectionConfigured,
}
impl ::std::fmt::Display for Report1TestOriginSetV1Variant0Property3Item {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::ForeignUnitPathsNotMatched => {
                f.write_str("foreign-unit-paths-not-matched")
            }
            Self::InTargetUnitTestsNotIdentified => {
                f.write_str("in-target-unit-tests-not-identified")
            }
            Self::NoSelectedTestTargets => f.write_str("no-selected-test-targets"),
            Self::OwnershipEnumerationPartial => {
                f.write_str("ownership-enumeration-partial")
            }
            Self::RecognizerGlobsNotTestPopulation => {
                f.write_str("recognizer-globs-not-test-population")
            }
            Self::RecognizerUnresolvedChoices => {
                f.write_str("recognizer-unresolved-choices")
            }
            Self::SharedTestAndNonTestTargetPath => {
                f.write_str("shared-test-and-non-test-target-path")
            }
            Self::SymbolAttributionConflict => f.write_str("symbol-attribution-conflict"),
            Self::SymbolInventoryIncomplete => f.write_str("symbol-inventory-incomplete"),
            Self::TestSelectionConfigured => f.write_str("test-selection-configured"),
        }
    }
}
impl ::std::str::FromStr for Report1TestOriginSetV1Variant0Property3Item {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "foreign-unit-paths-not-matched" => Ok(Self::ForeignUnitPathsNotMatched),
            "in-target-unit-tests-not-identified" => {
                Ok(Self::InTargetUnitTestsNotIdentified)
            }
            "no-selected-test-targets" => Ok(Self::NoSelectedTestTargets),
            "ownership-enumeration-partial" => Ok(Self::OwnershipEnumerationPartial),
            "recognizer-globs-not-test-population" => {
                Ok(Self::RecognizerGlobsNotTestPopulation)
            }
            "recognizer-unresolved-choices" => Ok(Self::RecognizerUnresolvedChoices),
            "shared-test-and-non-test-target-path" => {
                Ok(Self::SharedTestAndNonTestTargetPath)
            }
            "symbol-attribution-conflict" => Ok(Self::SymbolAttributionConflict),
            "symbol-inventory-incomplete" => Ok(Self::SymbolInventoryIncomplete),
            "test-selection-configured" => Ok(Self::TestSelectionConfigured),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1TestOriginSetV1Variant0Property3Item {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Report1TestOriginSetV1Variant0Property3Item {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Report1TestOriginSetV1Variant1Property1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1TestOriginSetV1Variant1Property1 {
    #[serde(rename = "testTargets")]
    pub test_targets: ::std::vec::Vec<Report1CargoTargetRefV1>,
}
///`Report1TestOriginSetV1Variant1Property3Item`
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
pub enum Report1TestOriginSetV1Variant1Property3Item {
    #[serde(rename = "foreign-unit-paths-not-matched")]
    ForeignUnitPathsNotMatched,
    #[serde(rename = "in-target-unit-tests-not-identified")]
    InTargetUnitTestsNotIdentified,
    #[serde(rename = "no-selected-test-targets")]
    NoSelectedTestTargets,
    #[serde(rename = "ownership-enumeration-partial")]
    OwnershipEnumerationPartial,
    #[serde(rename = "recognizer-globs-not-test-population")]
    RecognizerGlobsNotTestPopulation,
    #[serde(rename = "recognizer-unresolved-choices")]
    RecognizerUnresolvedChoices,
    #[serde(rename = "shared-test-and-non-test-target-path")]
    SharedTestAndNonTestTargetPath,
    #[serde(rename = "symbol-attribution-conflict")]
    SymbolAttributionConflict,
    #[serde(rename = "symbol-inventory-incomplete")]
    SymbolInventoryIncomplete,
    #[serde(rename = "test-selection-configured")]
    TestSelectionConfigured,
}
impl ::std::fmt::Display for Report1TestOriginSetV1Variant1Property3Item {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::ForeignUnitPathsNotMatched => {
                f.write_str("foreign-unit-paths-not-matched")
            }
            Self::InTargetUnitTestsNotIdentified => {
                f.write_str("in-target-unit-tests-not-identified")
            }
            Self::NoSelectedTestTargets => f.write_str("no-selected-test-targets"),
            Self::OwnershipEnumerationPartial => {
                f.write_str("ownership-enumeration-partial")
            }
            Self::RecognizerGlobsNotTestPopulation => {
                f.write_str("recognizer-globs-not-test-population")
            }
            Self::RecognizerUnresolvedChoices => {
                f.write_str("recognizer-unresolved-choices")
            }
            Self::SharedTestAndNonTestTargetPath => {
                f.write_str("shared-test-and-non-test-target-path")
            }
            Self::SymbolAttributionConflict => f.write_str("symbol-attribution-conflict"),
            Self::SymbolInventoryIncomplete => f.write_str("symbol-inventory-incomplete"),
            Self::TestSelectionConfigured => f.write_str("test-selection-configured"),
        }
    }
}
impl ::std::str::FromStr for Report1TestOriginSetV1Variant1Property3Item {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "foreign-unit-paths-not-matched" => Ok(Self::ForeignUnitPathsNotMatched),
            "in-target-unit-tests-not-identified" => {
                Ok(Self::InTargetUnitTestsNotIdentified)
            }
            "no-selected-test-targets" => Ok(Self::NoSelectedTestTargets),
            "ownership-enumeration-partial" => Ok(Self::OwnershipEnumerationPartial),
            "recognizer-globs-not-test-population" => {
                Ok(Self::RecognizerGlobsNotTestPopulation)
            }
            "recognizer-unresolved-choices" => Ok(Self::RecognizerUnresolvedChoices),
            "shared-test-and-non-test-target-path" => {
                Ok(Self::SharedTestAndNonTestTargetPath)
            }
            "symbol-attribution-conflict" => Ok(Self::SymbolAttributionConflict),
            "symbol-inventory-incomplete" => Ok(Self::SymbolInventoryIncomplete),
            "test-selection-configured" => Ok(Self::TestSelectionConfigured),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1TestOriginSetV1Variant1Property3Item {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Report1TestOriginSetV1Variant1Property3Item {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Report1TestOriginSetV1Variant2Property1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1TestOriginSetV1Variant2Property1 {
    #[serde(rename = "markerPath")]
    pub marker_path: Report1TestOriginSetV1Variant2Property1MarkerPath,
    #[serde(rename = "recognitionId")]
    pub recognition_id: ::std::string::String,
    pub recognizers: ::std::vec::Vec<
        Report1TestOriginSetV1Variant2Property1RecognizersItem,
    >,
    #[serde(rename = "rootPath")]
    pub root_path: Native2InternalUnitRootV1,
    #[serde(rename = "unitOrdinal")]
    pub unit_ordinal: Common4Uint53,
}
///`Report1TestOriginSetV1Variant2Property1MarkerPath`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Report1TestOriginSetV1Variant2Property1MarkerPath(::std::string::String);
impl ::std::ops::Deref for Report1TestOriginSetV1Variant2Property1MarkerPath {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Report1TestOriginSetV1Variant2Property1MarkerPath>
for ::std::string::String {
    fn from(value: Report1TestOriginSetV1Variant2Property1MarkerPath) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Report1TestOriginSetV1Variant2Property1MarkerPath {
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
impl ::std::convert::TryFrom<&str>
for Report1TestOriginSetV1Variant2Property1MarkerPath {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Report1TestOriginSetV1Variant2Property1MarkerPath {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de>
for Report1TestOriginSetV1Variant2Property1MarkerPath {
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
///`Report1TestOriginSetV1Variant2Property1RecognizersItem`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1TestOriginSetV1Variant2Property1RecognizersItem {
    pub evidence: Native2FrameworkRecognitionResultV1PropertiesEvidence,
    #[serde(rename = "recognizerId")]
    pub recognizer_id: ::serde_json::Value,
    #[serde(rename = "testGlobs")]
    pub test_globs: Native2FrameworkRecognitionResultV1PropertiesEffectsPropertiesTestGlobs,
    #[serde(rename = "unresolvedChoices")]
    pub unresolved_choices: Native2FrameworkRecognitionResultV1PropertiesUnresolvedChoices,
}
///`Report1TestOriginSetV1Variant2Property3Item`
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
pub enum Report1TestOriginSetV1Variant2Property3Item {
    #[serde(rename = "foreign-unit-paths-not-matched")]
    ForeignUnitPathsNotMatched,
    #[serde(rename = "in-target-unit-tests-not-identified")]
    InTargetUnitTestsNotIdentified,
    #[serde(rename = "no-selected-test-targets")]
    NoSelectedTestTargets,
    #[serde(rename = "ownership-enumeration-partial")]
    OwnershipEnumerationPartial,
    #[serde(rename = "recognizer-globs-not-test-population")]
    RecognizerGlobsNotTestPopulation,
    #[serde(rename = "recognizer-unresolved-choices")]
    RecognizerUnresolvedChoices,
    #[serde(rename = "shared-test-and-non-test-target-path")]
    SharedTestAndNonTestTargetPath,
    #[serde(rename = "symbol-attribution-conflict")]
    SymbolAttributionConflict,
    #[serde(rename = "symbol-inventory-incomplete")]
    SymbolInventoryIncomplete,
    #[serde(rename = "test-selection-configured")]
    TestSelectionConfigured,
}
impl ::std::fmt::Display for Report1TestOriginSetV1Variant2Property3Item {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::ForeignUnitPathsNotMatched => {
                f.write_str("foreign-unit-paths-not-matched")
            }
            Self::InTargetUnitTestsNotIdentified => {
                f.write_str("in-target-unit-tests-not-identified")
            }
            Self::NoSelectedTestTargets => f.write_str("no-selected-test-targets"),
            Self::OwnershipEnumerationPartial => {
                f.write_str("ownership-enumeration-partial")
            }
            Self::RecognizerGlobsNotTestPopulation => {
                f.write_str("recognizer-globs-not-test-population")
            }
            Self::RecognizerUnresolvedChoices => {
                f.write_str("recognizer-unresolved-choices")
            }
            Self::SharedTestAndNonTestTargetPath => {
                f.write_str("shared-test-and-non-test-target-path")
            }
            Self::SymbolAttributionConflict => f.write_str("symbol-attribution-conflict"),
            Self::SymbolInventoryIncomplete => f.write_str("symbol-inventory-incomplete"),
            Self::TestSelectionConfigured => f.write_str("test-selection-configured"),
        }
    }
}
impl ::std::str::FromStr for Report1TestOriginSetV1Variant2Property3Item {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "foreign-unit-paths-not-matched" => Ok(Self::ForeignUnitPathsNotMatched),
            "in-target-unit-tests-not-identified" => {
                Ok(Self::InTargetUnitTestsNotIdentified)
            }
            "no-selected-test-targets" => Ok(Self::NoSelectedTestTargets),
            "ownership-enumeration-partial" => Ok(Self::OwnershipEnumerationPartial),
            "recognizer-globs-not-test-population" => {
                Ok(Self::RecognizerGlobsNotTestPopulation)
            }
            "recognizer-unresolved-choices" => Ok(Self::RecognizerUnresolvedChoices),
            "shared-test-and-non-test-target-path" => {
                Ok(Self::SharedTestAndNonTestTargetPath)
            }
            "symbol-attribution-conflict" => Ok(Self::SymbolAttributionConflict),
            "symbol-inventory-incomplete" => Ok(Self::SymbolInventoryIncomplete),
            "test-selection-configured" => Ok(Self::TestSelectionConfigured),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1TestOriginSetV1Variant2Property3Item {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Report1TestOriginSetV1Variant2Property3Item {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///R07 test reachability. There is deliberately no absence-style state: no retained evidence establishes a complete test origin set.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(untagged, deny_unknown_fields)]
pub enum Report1TestReachabilityV1 {
    Variant0 {
        cause: Report1TestReachabilityV1Variant0Cause,
        state: ::serde_json::Value,
        #[serde(rename = "subjectId")]
        subject_id: Common4SubjectId,
    },
    Variant1 {
        cause: ::serde_json::Value,
        reach: Report1ReportReachContextV1,
        #[serde(rename = "reachedUniverses")]
        reached_universes: ::std::vec::Vec<Common4Sha256Hex>,
        state: ::serde_json::Value,
        #[serde(rename = "subjectId")]
        subject_id: Common4SubjectId,
    },
    Variant2 {
        #[serde(rename = "attributionPath")]
        attribution_path: Common4LogicalPath,
        #[serde(rename = "originEvidence")]
        origin_evidence: Report1TestOriginEvidenceV1,
        state: ::serde_json::Value,
        #[serde(rename = "subjectId")]
        subject_id: Common4SubjectId,
    },
    Variant3 {
        interpretation: ::serde_json::Value,
        origin: Report1TestReachabilityV1Variant3Origin,
        reach: Report1ReportReachContextV1,
        state: ::serde_json::Value,
        #[serde(rename = "subjectId")]
        subject_id: Common4SubjectId,
        witness: Report1ReportGraphExchangeV1,
    },
    Variant4 {
        blockers: ::std::vec::Vec<Report1TestReachabilityV1Variant4BlockersItem>,
        interpretation: ::serde_json::Value,
        reach: Report1ReportReachContextV1,
        #[serde(rename = "reachedUniverses")]
        reached_universes: ::std::vec::Vec<Common4Sha256Hex>,
        state: ::serde_json::Value,
        #[serde(rename = "subjectId")]
        subject_id: Common4SubjectId,
    },
}
///`Report1TestReachabilityV1Variant0Cause`
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
pub enum Report1TestReachabilityV1Variant0Cause {
    #[serde(rename = "calls-evidence-unavailable")]
    CallsEvidenceUnavailable,
    #[serde(rename = "subject-descriptor-not-retained")]
    SubjectDescriptorNotRetained,
}
impl ::std::fmt::Display for Report1TestReachabilityV1Variant0Cause {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::CallsEvidenceUnavailable => f.write_str("calls-evidence-unavailable"),
            Self::SubjectDescriptorNotRetained => {
                f.write_str("subject-descriptor-not-retained")
            }
        }
    }
}
impl ::std::str::FromStr for Report1TestReachabilityV1Variant0Cause {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "calls-evidence-unavailable" => Ok(Self::CallsEvidenceUnavailable),
            "subject-descriptor-not-retained" => Ok(Self::SubjectDescriptorNotRetained),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1TestReachabilityV1Variant0Cause {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Report1TestReachabilityV1Variant0Cause {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Report1TestReachabilityV1Variant3Origin`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1TestReachabilityV1Variant3Origin {
    #[serde(rename = "attributionPath")]
    pub attribution_path: Common4LogicalPath,
    pub endpoint: Graph4GraphEndpoint,
    #[serde(rename = "originEvidence")]
    pub origin_evidence: Report1TestOriginEvidenceV1,
}
///`Report1TestReachabilityV1Variant4BlockersItem`
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
pub enum Report1TestReachabilityV1Variant4BlockersItem {
    #[serde(rename = "evidence-limitations")]
    EvidenceLimitations,
    #[serde(rename = "origin-sets-not-embedded")]
    OriginSetsNotEmbedded,
    #[serde(rename = "reach-lower-bound")]
    ReachLowerBound,
    #[serde(rename = "reached-universe-without-test-origin-identity")]
    ReachedUniverseWithoutTestOriginIdentity,
    #[serde(rename = "test-origin-set-partial")]
    TestOriginSetPartial,
}
impl ::std::fmt::Display for Report1TestReachabilityV1Variant4BlockersItem {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::EvidenceLimitations => f.write_str("evidence-limitations"),
            Self::OriginSetsNotEmbedded => f.write_str("origin-sets-not-embedded"),
            Self::ReachLowerBound => f.write_str("reach-lower-bound"),
            Self::ReachedUniverseWithoutTestOriginIdentity => {
                f.write_str("reached-universe-without-test-origin-identity")
            }
            Self::TestOriginSetPartial => f.write_str("test-origin-set-partial"),
        }
    }
}
impl ::std::str::FromStr for Report1TestReachabilityV1Variant4BlockersItem {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "evidence-limitations" => Ok(Self::EvidenceLimitations),
            "origin-sets-not-embedded" => Ok(Self::OriginSetsNotEmbedded),
            "reach-lower-bound" => Ok(Self::ReachLowerBound),
            "reached-universe-without-test-origin-identity" => {
                Ok(Self::ReachedUniverseWithoutTestOriginIdentity)
            }
            "test-origin-set-partial" => Ok(Self::TestOriginSetPartial),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1TestReachabilityV1Variant4BlockersItem {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Report1TestReachabilityV1Variant4BlockersItem {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Report1WorkspaceUnitRefV1`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Report1WorkspaceUnitRefV1 {
    #[serde(rename = "languageFamily")]
    pub language_family: ::serde_json::Value,
    #[serde(rename = "markerPath")]
    pub marker_path: Report1WorkspaceUnitRefV1MarkerPath,
    #[serde(rename = "rootPath")]
    pub root_path: Native2InternalUnitRootV1,
    #[serde(rename = "unitKind")]
    pub unit_kind: Report1WorkspaceUnitRefV1UnitKind,
    #[serde(rename = "unitOrdinal")]
    pub unit_ordinal: Common4Uint53,
}
///`Report1WorkspaceUnitRefV1MarkerPath`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Report1WorkspaceUnitRefV1MarkerPath(::std::string::String);
impl ::std::ops::Deref for Report1WorkspaceUnitRefV1MarkerPath {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Report1WorkspaceUnitRefV1MarkerPath>
for ::std::string::String {
    fn from(value: Report1WorkspaceUnitRefV1MarkerPath) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Report1WorkspaceUnitRefV1MarkerPath {
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
impl ::std::convert::TryFrom<&str> for Report1WorkspaceUnitRefV1MarkerPath {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Report1WorkspaceUnitRefV1MarkerPath {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Report1WorkspaceUnitRefV1MarkerPath {
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
///`Report1WorkspaceUnitRefV1UnitKind`
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
pub enum Report1WorkspaceUnitRefV1UnitKind {
    #[serde(rename = "js-program")]
    JsProgram,
    #[serde(rename = "ts-program")]
    TsProgram,
}
impl ::std::fmt::Display for Report1WorkspaceUnitRefV1UnitKind {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::JsProgram => f.write_str("js-program"),
            Self::TsProgram => f.write_str("ts-program"),
        }
    }
}
impl ::std::str::FromStr for Report1WorkspaceUnitRefV1UnitKind {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "js-program" => Ok(Self::JsProgram),
            "ts-program" => Ok(Self::TsProgram),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Report1WorkspaceUnitRefV1UnitKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Report1WorkspaceUnitRefV1UnitKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Matched finding candidates group by fingerprint after BaselineEntry-field agreement; unmatched stay one candidate per findingId. candidateId = candidate2: + H(workflow.candidate, {projectId,kind,key}) with key=fingerprint or findingId. No representative findingId may drop other configuration evidence.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Review2Candidate {
    #[serde(rename = "candidateId")]
    pub candidate_id: Common3CandidateId,
    ///true only for kind=finding on a gating rule with at least one live unwaived occurrence
    #[serde(rename = "controlBearing")]
    pub control_bearing: bool,
    #[serde(rename = "evidenceLevel")]
    pub evidence_level: Review2EvidenceLevel,
    #[serde(
        rename = "findingIds",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub finding_ids: FieldPresence<
        ::std::option::Option<::std::vec::Vec<Common3FindingId>>,
    >,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub fingerprint: FieldPresence<::std::option::Option<Common3NullableFingerprint>>,
    pub kind: Review2CandidateKind,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub occurrences: FieldPresence<::std::vec::Vec<Review2CandidateOccurrence>>,
    #[serde(
        rename = "previouslyReviewed",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub previously_reviewed: FieldPresence<::std::option::Option<bool>>,
    #[serde(
        rename = "ruleId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub rule_id: FieldPresence<::std::option::Option<Common3CanonicalIdentifier>>,
    #[serde(rename = "runId")]
    pub run_id: Common3RunId,
    #[serde(rename = "subjectPath")]
    pub subject_path: Common3LogicalPath,
    pub suppressed: bool,
    #[serde(
        rename = "suppressedBy",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub suppressed_by: FieldPresence<::std::option::Option<Common3ReceiptId>>,
}
///`Review2CandidateKind`
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
pub enum Review2CandidateKind {
    #[serde(rename = "finding")]
    Finding,
    #[serde(rename = "clone-candidate")]
    CloneCandidate,
    #[serde(rename = "low-confidence-unused")]
    LowConfidenceUnused,
    #[serde(rename = "runtime-unhit")]
    RuntimeUnhit,
    #[serde(rename = "history-stale")]
    HistoryStale,
}
impl ::std::fmt::Display for Review2CandidateKind {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Finding => f.write_str("finding"),
            Self::CloneCandidate => f.write_str("clone-candidate"),
            Self::LowConfidenceUnused => f.write_str("low-confidence-unused"),
            Self::RuntimeUnhit => f.write_str("runtime-unhit"),
            Self::HistoryStale => f.write_str("history-stale"),
        }
    }
}
impl ::std::str::FromStr for Review2CandidateKind {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "finding" => Ok(Self::Finding),
            "clone-candidate" => Ok(Self::CloneCandidate),
            "low-confidence-unused" => Ok(Self::LowConfidenceUnused),
            "runtime-unhit" => Ok(Self::RuntimeUnhit),
            "history-stale" => Ok(Self::HistoryStale),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Review2CandidateKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Review2CandidateKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///One configuration-qualified finding3 inside a logical candidate. Parameters stay per occurrence.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Review2CandidateOccurrence {
    pub correspondence: Common3Correspondence,
    #[serde(rename = "findingId")]
    pub finding_id: Common3FindingId,
    #[serde(rename = "parameterDigest")]
    pub parameter_digest: Common3Sha256Hex,
    #[serde(rename = "subjectId")]
    pub subject_id: Common3SubjectId,
    #[serde(rename = "subjectPath")]
    pub subject_path: Common3LogicalPath,
    pub waived: bool,
}
///`Review2EvidenceLevel`
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
pub enum Review2EvidenceLevel {
    #[serde(rename = "proof-backed")]
    ProofBacked,
    #[serde(rename = "partial-coverage")]
    PartialCoverage,
    #[serde(rename = "advisory-only")]
    AdvisoryOnly,
}
impl ::std::fmt::Display for Review2EvidenceLevel {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::ProofBacked => f.write_str("proof-backed"),
            Self::PartialCoverage => f.write_str("partial-coverage"),
            Self::AdvisoryOnly => f.write_str("advisory-only"),
        }
    }
}
impl ::std::str::FromStr for Review2EvidenceLevel {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "proof-backed" => Ok(Self::ProofBacked),
            "partial-coverage" => Ok(Self::PartialCoverage),
            "advisory-only" => Ok(Self::AdvisoryOnly),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Review2EvidenceLevel {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Review2EvidenceLevel {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Review2InspectionBundle`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Review2InspectionBundle {
    pub advisory: ::serde_json::Value,
    #[serde(rename = "candidateId")]
    pub candidate_id: Common3CandidateId,
    #[serde(rename = "coverageIds")]
    pub coverage_ids: ::std::vec::Vec<Common3CoverageId>,
    pub facts: ::std::vec::Vec<::std::string::String>,
    #[serde(rename = "importIds")]
    pub import_ids: ::std::vec::Vec<Common3ImportId>,
    pub limitations: ::std::vec::Vec<Common3BoundedText>,
    #[serde(rename = "runId")]
    pub run_id: Common3RunId,
}
///Output of review-brief: an ordered, bounded, advisory list. Model-produced ordering or text is labelled with the model closure and never alters candidates.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Review2ReviewBrief {
    pub advisory: ::serde_json::Value,
    pub candidates: ::std::vec::Vec<Common3CandidateId>,
    pub producer: Review2ReviewerPrincipal,
    #[serde(rename = "runId")]
    pub run_id: Common3RunId,
    pub truncated: bool,
}
///The effect of a review-join mutation. Advisory by construction: it has no verdict, run, baseline or authorization field, and the schema admits none.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Review2ReviewDisposition {
    pub advisory: ::serde_json::Value,
    #[serde(rename = "candidateId")]
    pub candidate_id: Common3CandidateId,
    pub disposition: Review2ReviewDispositionDisposition,
    pub note: Review2ReviewDispositionNote,
    pub reviewer: Review2ReviewerPrincipal,
    ///at most 365 days after the disposition date; null for accept
    #[serde(
        rename = "suppressUntil",
        deserialize_with = "::std::option::Option::deserialize"
    )]
    pub suppress_until: ::std::option::Option<Common3UtcDate>,
}
///`Review2ReviewDispositionDisposition`
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
pub enum Review2ReviewDispositionDisposition {
    #[serde(rename = "accept")]
    Accept,
    #[serde(rename = "reject")]
    Reject,
    #[serde(rename = "defer")]
    Defer,
}
impl ::std::fmt::Display for Review2ReviewDispositionDisposition {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Accept => f.write_str("accept"),
            Self::Reject => f.write_str("reject"),
            Self::Defer => f.write_str("defer"),
        }
    }
}
impl ::std::str::FromStr for Review2ReviewDispositionDisposition {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "accept" => Ok(Self::Accept),
            "reject" => Ok(Self::Reject),
            "defer" => Ok(Self::Defer),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Review2ReviewDispositionDisposition {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Review2ReviewDispositionDisposition {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Review2ReviewDispositionNote`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Review2ReviewDispositionNote(::std::string::String);
impl ::std::ops::Deref for Review2ReviewDispositionNote {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Review2ReviewDispositionNote> for ::std::string::String {
    fn from(value: Review2ReviewDispositionNote) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Review2ReviewDispositionNote {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 4096usize {
            return Err("longer than 4096 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Review2ReviewDispositionNote {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Review2ReviewDispositionNote {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Review2ReviewDispositionNote {
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
///`Review2ReviewerPrincipal`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Review2ReviewerPrincipal {
    pub id: Review2ReviewerPrincipalId,
    pub kind: Review2ReviewerPrincipalKind,
    #[serde(
        rename = "modelClosureId",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub model_closure_id: FieldPresence<::std::option::Option<Common3ClosureId>>,
}
///`Review2ReviewerPrincipalId`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Review2ReviewerPrincipalId(::std::string::String);
impl ::std::ops::Deref for Review2ReviewerPrincipalId {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Review2ReviewerPrincipalId> for ::std::string::String {
    fn from(value: Review2ReviewerPrincipalId) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Review2ReviewerPrincipalId {
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
impl ::std::convert::TryFrom<&str> for Review2ReviewerPrincipalId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Review2ReviewerPrincipalId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Review2ReviewerPrincipalId {
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
///`Review2ReviewerPrincipalKind`
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
pub enum Review2ReviewerPrincipalKind {
    #[serde(rename = "human")]
    Human,
    #[serde(rename = "model")]
    Model,
    #[serde(rename = "policy-rule")]
    PolicyRule,
}
impl ::std::fmt::Display for Review2ReviewerPrincipalKind {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Human => f.write_str("human"),
            Self::Model => f.write_str("model"),
            Self::PolicyRule => f.write_str("policy-rule"),
        }
    }
}
impl ::std::str::FromStr for Review2ReviewerPrincipalKind {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "human" => Ok(Self::Human),
            "model" => Ok(Self::Model),
            "policy-rule" => Ok(Self::PolicyRule),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Review2ReviewerPrincipalKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Review2ReviewerPrincipalKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Evaluator3 candidates. Matched findings group by fingerprint only after BaselineEntry-field agreement (including optional legacyFingerprint presence/value); the logical candidate carries every findingId and per-occurrence parameters. Unmatched findings are one candidate per findingId and MUST NOT mint a surrogate fingerprint. candidateId hashes {projectId,kind,key} where key is fingerprint for matched and findingId for unmatched. Reviewed-clone suppression is keyed by that candidateId so fingerprint-grouped clones share one logical target and unmatched findingIds stay distinct. RunId is run3.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(transparent)]
pub struct Review2Root(pub ::serde_json::Value);
impl ::std::ops::Deref for Review2Root {
    type Target = ::serde_json::Value;
    fn deref(&self) -> &::serde_json::Value {
        &self.0
    }
}
impl ::std::convert::From<Review2Root> for ::serde_json::Value {
    fn from(value: Review2Root) -> Self {
        value.0
    }
}
impl ::std::convert::From<::serde_json::Value> for Review2Root {
    fn from(value: ::serde_json::Value) -> Self {
        Self(value)
    }
}
///`Sarif2Result`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Sarif2Result {
    pub level: Sarif2ResultLevel,
    pub locations: [Sarif2ResultLocationsItem; 1usize],
    pub message: Sarif2ResultMessage,
    #[serde(
        rename = "partialFingerprints",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub partial_fingerprints: FieldPresence<
        ::std::option::Option<Sarif2ResultPartialFingerprints>,
    >,
    pub properties: Sarif2ResultProperties,
    #[serde(rename = "ruleId")]
    pub rule_id: Sarif2ResultRuleId,
    ///SARIF 2.1 suppressions. Present iff the finding is waived. kind=external (policy waiver), status=accepted.
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub suppressions: FieldPresence<::std::vec::Vec<Sarif2ResultSuppressionsItem>>,
}
///`Sarif2ResultLevel`
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
pub enum Sarif2ResultLevel {
    #[serde(rename = "note")]
    Note,
    #[serde(rename = "warning")]
    Warning,
    #[serde(rename = "error")]
    Error,
}
impl ::std::fmt::Display for Sarif2ResultLevel {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Note => f.write_str("note"),
            Self::Warning => f.write_str("warning"),
            Self::Error => f.write_str("error"),
        }
    }
}
impl ::std::str::FromStr for Sarif2ResultLevel {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "note" => Ok(Self::Note),
            "warning" => Ok(Self::Warning),
            "error" => Ok(Self::Error),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Sarif2ResultLevel {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Sarif2ResultLevel {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Sarif2ResultLocationsItem`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Sarif2ResultLocationsItem {
    #[serde(rename = "physicalLocation")]
    pub physical_location: Sarif2ResultLocationsItemPhysicalLocation,
}
///`Sarif2ResultLocationsItemPhysicalLocation`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Sarif2ResultLocationsItemPhysicalLocation {
    #[serde(rename = "artifactLocation")]
    pub artifact_location: Sarif2ResultLocationsItemPhysicalLocationArtifactLocation,
}
///`Sarif2ResultLocationsItemPhysicalLocationArtifactLocation`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Sarif2ResultLocationsItemPhysicalLocationArtifactLocation {
    ///Percent-encoded logical path (RFC 3986). Not a raw LogicalPath.
    pub uri: Sarif2ResultLocationsItemPhysicalLocationArtifactLocationUri,
}
///Percent-encoded logical path (RFC 3986). Not a raw LogicalPath.
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Sarif2ResultLocationsItemPhysicalLocationArtifactLocationUri(
    ::std::string::String,
);
impl ::std::ops::Deref for Sarif2ResultLocationsItemPhysicalLocationArtifactLocationUri {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Sarif2ResultLocationsItemPhysicalLocationArtifactLocationUri>
for ::std::string::String {
    fn from(
        value: Sarif2ResultLocationsItemPhysicalLocationArtifactLocationUri,
    ) -> Self {
        value.0
    }
}
impl ::std::str::FromStr
for Sarif2ResultLocationsItemPhysicalLocationArtifactLocationUri {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 8192usize {
            return Err("longer than 8192 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str>
for Sarif2ResultLocationsItemPhysicalLocationArtifactLocationUri {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Sarif2ResultLocationsItemPhysicalLocationArtifactLocationUri {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de>
for Sarif2ResultLocationsItemPhysicalLocationArtifactLocationUri {
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
///`Sarif2ResultMessage`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Sarif2ResultMessage {
    pub id: Sarif2ResultMessageId,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub properties: FieldPresence<
        ::std::collections::BTreeMap<
            ::std::string::String,
            Sarif2ResultMessagePropertiesValue,
        >,
    >,
    pub text: Sarif2ResultMessageText,
}
///`Sarif2ResultMessageId`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Sarif2ResultMessageId(::std::string::String);
impl ::std::ops::Deref for Sarif2ResultMessageId {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Sarif2ResultMessageId> for ::std::string::String {
    fn from(value: Sarif2ResultMessageId) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Sarif2ResultMessageId {
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
impl ::std::convert::TryFrom<&str> for Sarif2ResultMessageId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Sarif2ResultMessageId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Sarif2ResultMessageId {
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
///`Sarif2ResultMessagePropertiesValue`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(untagged)]
pub enum Sarif2ResultMessagePropertiesValue {
    Boolean(bool),
    Integer(ExactInteger),
    String(::std::string::String),
}
impl ::std::fmt::Display for Sarif2ResultMessagePropertiesValue {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match self {
            Self::Boolean(x) => x.fmt(f),
            Self::Integer(x) => x.fmt(f),
            Self::String(x) => x.fmt(f),
        }
    }
}
impl ::std::convert::From<bool> for Sarif2ResultMessagePropertiesValue {
    fn from(value: bool) -> Self {
        Self::Boolean(value)
    }
}
impl ::std::convert::From<ExactInteger> for Sarif2ResultMessagePropertiesValue {
    fn from(value: ExactInteger) -> Self {
        Self::Integer(value)
    }
}
///`Sarif2ResultMessageText`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Sarif2ResultMessageText(::std::string::String);
impl ::std::ops::Deref for Sarif2ResultMessageText {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Sarif2ResultMessageText> for ::std::string::String {
    fn from(value: Sarif2ResultMessageText) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Sarif2ResultMessageText {
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
impl ::std::convert::TryFrom<&str> for Sarif2ResultMessageText {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Sarif2ResultMessageText {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Sarif2ResultMessageText {
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
///`Sarif2ResultPartialFingerprints`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Sarif2ResultPartialFingerprints {
    #[serde(rename = "opensip/finding-key2")]
    pub opensip_finding_key2: Common3Fingerprint,
}
///`Sarif2ResultProperties`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Sarif2ResultProperties {
    pub citations: ::std::vec::Vec<Sarif2ResultPropertiesCitationsItem>,
    pub correspondence: Common3Correspondence,
    #[serde(rename = "findingId")]
    pub finding_id: Common3FindingId,
    #[serde(rename = "subjectId")]
    pub subject_id: Common3SubjectId,
    pub waived: bool,
}
///`Sarif2ResultPropertiesCitationsItem`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Sarif2ResultPropertiesCitationsItem {
    pub digest: Common3Sha256Hex,
    pub domain: Sarif2ResultPropertiesCitationsItemDomain,
}
///`Sarif2ResultPropertiesCitationsItemDomain`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Sarif2ResultPropertiesCitationsItemDomain(::std::string::String);
impl ::std::ops::Deref for Sarif2ResultPropertiesCitationsItemDomain {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Sarif2ResultPropertiesCitationsItemDomain>
for ::std::string::String {
    fn from(value: Sarif2ResultPropertiesCitationsItemDomain) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Sarif2ResultPropertiesCitationsItemDomain {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 64usize {
            return Err("longer than 64 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Sarif2ResultPropertiesCitationsItemDomain {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Sarif2ResultPropertiesCitationsItemDomain {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Sarif2ResultPropertiesCitationsItemDomain {
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
///`Sarif2ResultRuleId`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Sarif2ResultRuleId(::std::string::String);
impl ::std::ops::Deref for Sarif2ResultRuleId {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Sarif2ResultRuleId> for ::std::string::String {
    fn from(value: Sarif2ResultRuleId) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Sarif2ResultRuleId {
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
impl ::std::convert::TryFrom<&str> for Sarif2ResultRuleId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Sarif2ResultRuleId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Sarif2ResultRuleId {
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
///`Sarif2ResultSuppressionsItem`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Sarif2ResultSuppressionsItem {
    pub kind: Sarif2ResultSuppressionsItemKind,
    pub status: Sarif2ResultSuppressionsItemStatus,
}
///`Sarif2ResultSuppressionsItemKind`
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
pub enum Sarif2ResultSuppressionsItemKind {
    #[serde(rename = "external")]
    External,
}
impl ::std::fmt::Display for Sarif2ResultSuppressionsItemKind {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::External => f.write_str("external"),
        }
    }
}
impl ::std::str::FromStr for Sarif2ResultSuppressionsItemKind {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "external" => Ok(Self::External),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Sarif2ResultSuppressionsItemKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Sarif2ResultSuppressionsItemKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Sarif2ResultSuppressionsItemStatus`
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
pub enum Sarif2ResultSuppressionsItemStatus {
    #[serde(rename = "accepted")]
    Accepted,
}
impl ::std::fmt::Display for Sarif2ResultSuppressionsItemStatus {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Accepted => f.write_str("accepted"),
        }
    }
}
impl ::std::str::FromStr for Sarif2ResultSuppressionsItemStatus {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "accepted" => Ok(Self::Accepted),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Sarif2ResultSuppressionsItemStatus {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Sarif2ResultSuppressionsItemStatus {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///A SARIF 2.1.0 log subset produced from FindingSurface rows. One result per finding3. partialFingerprints only when matched. This is the SARIF document, not the intermediate FindingSurface.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Sarif2Root {
    pub runs: [Sarif2Run; 1usize],
    pub version: ::serde_json::Value,
}
///`Sarif2Run`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Sarif2Run {
    pub properties: Sarif2RunProperties,
    pub results: ::std::vec::Vec<Sarif2Result>,
    pub tool: Sarif2RunTool,
}
///`Sarif2RunProperties`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Sarif2RunProperties {
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub deficiency: FieldPresence<::std::option::Option<Sarif2RunPropertiesDeficiency>>,
    pub verdict: Sarif2RunPropertiesVerdict,
}
///`Sarif2RunPropertiesDeficiency`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Sarif2RunPropertiesDeficiency(::std::string::String);
impl ::std::ops::Deref for Sarif2RunPropertiesDeficiency {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Sarif2RunPropertiesDeficiency> for ::std::string::String {
    fn from(value: Sarif2RunPropertiesDeficiency) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Sarif2RunPropertiesDeficiency {
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
impl ::std::convert::TryFrom<&str> for Sarif2RunPropertiesDeficiency {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Sarif2RunPropertiesDeficiency {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Sarif2RunPropertiesDeficiency {
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
///`Sarif2RunPropertiesVerdict`
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
pub enum Sarif2RunPropertiesVerdict {
    #[serde(rename = "pass")]
    Pass,
    #[serde(rename = "fail")]
    Fail,
    #[serde(rename = "indeterminate")]
    Indeterminate,
}
impl ::std::fmt::Display for Sarif2RunPropertiesVerdict {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Pass => f.write_str("pass"),
            Self::Fail => f.write_str("fail"),
            Self::Indeterminate => f.write_str("indeterminate"),
        }
    }
}
impl ::std::str::FromStr for Sarif2RunPropertiesVerdict {
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
impl ::std::convert::TryFrom<&str> for Sarif2RunPropertiesVerdict {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Sarif2RunPropertiesVerdict {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Sarif2RunTool`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Sarif2RunTool {
    pub driver: Sarif2RunToolDriver,
}
///`Sarif2RunToolDriver`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Sarif2RunToolDriver {
    pub name: ::serde_json::Value,
    pub rules: ::std::vec::Vec<Sarif2RunToolDriverRulesItem>,
}
///`Sarif2RunToolDriverRulesItem`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Sarif2RunToolDriverRulesItem {
    pub id: Sarif2RunToolDriverRulesItemId,
    ///Required for every message.id referenced by a result of this rule.
    #[serde(
        rename = "messageStrings",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub message_strings: FieldPresence<
        ::std::collections::BTreeMap<
            ::std::string::String,
            Sarif2RunToolDriverRulesItemMessageStringsValue,
        >,
    >,
    #[serde(
        rename = "shortDescription",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub short_description: FieldPresence<
        ::std::option::Option<Sarif2RunToolDriverRulesItemShortDescription>,
    >,
}
///`Sarif2RunToolDriverRulesItemId`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Sarif2RunToolDriverRulesItemId(::std::string::String);
impl ::std::ops::Deref for Sarif2RunToolDriverRulesItemId {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Sarif2RunToolDriverRulesItemId> for ::std::string::String {
    fn from(value: Sarif2RunToolDriverRulesItemId) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Sarif2RunToolDriverRulesItemId {
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
impl ::std::convert::TryFrom<&str> for Sarif2RunToolDriverRulesItemId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Sarif2RunToolDriverRulesItemId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Sarif2RunToolDriverRulesItemId {
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
///`Sarif2RunToolDriverRulesItemMessageStringsValue`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Sarif2RunToolDriverRulesItemMessageStringsValue {
    pub text: Sarif2RunToolDriverRulesItemMessageStringsValueText,
}
///`Sarif2RunToolDriverRulesItemMessageStringsValueText`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Sarif2RunToolDriverRulesItemMessageStringsValueText(::std::string::String);
impl ::std::ops::Deref for Sarif2RunToolDriverRulesItemMessageStringsValueText {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Sarif2RunToolDriverRulesItemMessageStringsValueText>
for ::std::string::String {
    fn from(value: Sarif2RunToolDriverRulesItemMessageStringsValueText) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Sarif2RunToolDriverRulesItemMessageStringsValueText {
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
impl ::std::convert::TryFrom<&str>
for Sarif2RunToolDriverRulesItemMessageStringsValueText {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Sarif2RunToolDriverRulesItemMessageStringsValueText {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de>
for Sarif2RunToolDriverRulesItemMessageStringsValueText {
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
///`Sarif2RunToolDriverRulesItemShortDescription`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Sarif2RunToolDriverRulesItemShortDescription {
    pub text: Sarif2RunToolDriverRulesItemShortDescriptionText,
}
///`Sarif2RunToolDriverRulesItemShortDescriptionText`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Sarif2RunToolDriverRulesItemShortDescriptionText(::std::string::String);
impl ::std::ops::Deref for Sarif2RunToolDriverRulesItemShortDescriptionText {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Sarif2RunToolDriverRulesItemShortDescriptionText>
for ::std::string::String {
    fn from(value: Sarif2RunToolDriverRulesItemShortDescriptionText) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Sarif2RunToolDriverRulesItemShortDescriptionText {
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
impl ::std::convert::TryFrom<&str> for Sarif2RunToolDriverRulesItemShortDescriptionText {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Sarif2RunToolDriverRulesItemShortDescriptionText {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de>
for Sarif2RunToolDriverRulesItemShortDescriptionText {
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
