// Generated trial: named28 profile, typify0.8.0; inert carriers only.
#![allow(unused_imports)]
use super::evidence::error;
use super::evidence::*;
use super::invocation::*;
use super::output::*;
use super::protocol::*;
#[doc = "`Identity3AnalysisSpec`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3AnalysisSpec {
    pub parameters: ::std::vec::Vec<Identity3AnalysisSpecParametersItem>,
    #[serde(rename = "policyPackIds")]
    pub policy_pack_ids: ::std::vec::Vec<Identity3Text>,
    #[serde(rename = "requestedCapabilities")]
    pub requested_capabilities: ::std::vec::Vec<Identity3AnalysisSpecRequestedCapabilitiesItem>,
    #[serde(rename = "schemaVersion")]
    pub schema_version: ExactInteger,
}
#[doc = "`Identity3AnalysisSpecParametersItem`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3AnalysisSpecParametersItem {
    #[serde(rename = "payloadDigest")]
    pub payload_digest: ::std::string::String,
    #[serde(rename = "schemaDigest")]
    pub schema_digest: ::std::string::String,
}
#[doc = "`Identity3AnalysisSpecRequestedCapabilitiesItem`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3AnalysisSpecRequestedCapabilitiesItem {
    #[serde(rename = "capabilityId")]
    pub capability_id: Identity3AnalysisSpecRequestedCapabilitiesItemCapabilityId,
    #[serde(rename = "languageMode")]
    pub language_mode: Identity3Text,
    pub required: bool,
    #[serde(rename = "workspaceRoot")]
    pub workspace_root: Identity3Text,
}
#[doc = "`Identity3AnalysisSpecRequestedCapabilitiesItemCapabilityId`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Identity3AnalysisSpecRequestedCapabilitiesItemCapabilityId(::std::string::String);
impl ::std::ops::Deref for Identity3AnalysisSpecRequestedCapabilitiesItemCapabilityId {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Identity3AnalysisSpecRequestedCapabilitiesItemCapabilityId>
    for ::std::string::String
{
    fn from(value: Identity3AnalysisSpecRequestedCapabilitiesItemCapabilityId) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Identity3AnalysisSpecRequestedCapabilitiesItemCapabilityId {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 128usize {
            return Err("longer than 128 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Identity3AnalysisSpecRequestedCapabilitiesItemCapabilityId {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
    for Identity3AnalysisSpecRequestedCapabilitiesItemCapabilityId
{
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Identity3AnalysisSpecRequestedCapabilitiesItemCapabilityId {
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
#[doc = "`Identity3Availability`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3Availability {
    pub generation: u64,
    #[serde(rename = "missingRefs")]
    pub missing_refs: ::std::vec::Vec<Identity3Ref>,
    pub reason: Identity3AvailabilityReason,
    #[serde(rename = "runId")]
    pub run_id: ::std::string::String,
    #[serde(rename = "schemaVersion")]
    pub schema_version: ExactInteger,
    pub state: Identity3AvailabilityState,
}
#[doc = "`Identity3AvailabilityReason`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Identity3AvailabilityReason(::std::string::String);
impl ::std::ops::Deref for Identity3AvailabilityReason {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Identity3AvailabilityReason> for ::std::string::String {
    fn from(value: Identity3AvailabilityReason) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Identity3AvailabilityReason {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 4096usize {
            return Err("longer than 4096 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Identity3AvailabilityReason {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3AvailabilityReason {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Identity3AvailabilityReason {
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
#[doc = "`Identity3AvailabilityState`"]
#[derive(
    :: serde :: Deserialize,
    :: serde :: Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd,
)]
pub enum Identity3AvailabilityState {
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
impl ::std::fmt::Display for Identity3AvailabilityState {
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
impl ::std::str::FromStr for Identity3AvailabilityState {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
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
impl ::std::convert::TryFrom<&str> for Identity3AvailabilityState {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3AvailabilityState {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
#[doc = "`Identity3Blob`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3Blob {
    pub bytes: u64,
    pub path: Identity3LogicalPath,
    pub sha256: ::std::string::String,
}
#[doc = "The closed record whose raw SHA-256 is the languageVersion component of a FACT-IDENTITY body frame. Retention is DERIVED: no field of it is a free input, every field is copied from a named path in a record this Run already retains and the owning contract already admitted, and Run closure recomputes it rather than accepting it. Two conforming implementations build identical bytes from the same committed Run, which is what the inherited obligation \"canonical identity bytes supplied by ResolvedInputs/PlanId, not a human display string\" asks for. It is hashed, not embedded, because the inherited frame gives each component a u8 length and a component built by embedding per-crate data is not representable for valid inputs."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3BodyLanguageVersion {
    #[doc = "The exact build of that component: rustCommitHash for rust, compilerPackageDigest for typescript. Not a 64-hex field of this bundle and deliberately not annotated as one: it is an owner-admitted identity carried inside a derived record, joined by equality to the retained context and never re-hashed here. Its width differs by language by construction."]
    #[serde(rename = "compilerBuild")]
    pub compiler_build: Identity3BodyLanguageVersionCompilerBuild,
    #[doc = "The component that INTERPRETS the body span. Not the build tool and not the resolver."]
    #[serde(rename = "compilerName")]
    pub compiler_name: Identity3BodyLanguageVersionCompilerName,
    #[doc = "The release identity of that component, taken from the admitted native context. admit_native_context already refuses native.native-context-compiler-version-not-from-manifest unless it equals the admitted tool closure semanticVersion, for both languages, so this is joined to a retained closure manifest and is not a copied display string."]
    #[serde(rename = "compilerVersion")]
    pub compiler_version: Identity3BodyLanguageVersionCompilerVersion,
    #[doc = "The SELECTED source-language dialect of the body being identified: the edition of its owning compilation unit, the source variant its own suffix denotes, or - for a grammar-only interpretation - the grammar variant that suffix selects. Never a whole map and never null - a language with no declared dialect axis would be an unexamined default, and there is none. Including a map would make one body identity depend on unrelated crates and would not be representable inside the inherited u8 component length."]
    pub dialect: Identity3BodyLanguageVersionDialect,
    #[doc = "The language of the BODY, which is not always the language of the provider. Native section 6.3 puts languageId in the normalized-body preimage and closes it to {typescript, javascript, rust} so that a TypeScript body never groups with a JavaScript one even with identical bytes. One TypeScript engine universe produces bodies of BOTH: the engine is the provider, the source variant decides the body language, and section 6.4 keeps cross-TS/JS matching a separate candidate-only projection rather than a shared identity."]
    #[serde(rename = "languageId")]
    pub language_id: Identity3BodyLanguageVersionLanguageId,
    #[serde(rename = "schemaVersion")]
    pub schema_version: ExactInteger,
}
#[doc = "The exact build of that component: rustCommitHash for rust, compilerPackageDigest for typescript. Not a 64-hex field of this bundle and deliberately not annotated as one: it is an owner-admitted identity carried inside a derived record, joined by equality to the retained context and never re-hashed here. Its width differs by language by construction."]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Identity3BodyLanguageVersionCompilerBuild(::std::string::String);
impl ::std::ops::Deref for Identity3BodyLanguageVersionCompilerBuild {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Identity3BodyLanguageVersionCompilerBuild> for ::std::string::String {
    fn from(value: Identity3BodyLanguageVersionCompilerBuild) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Identity3BodyLanguageVersionCompilerBuild {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 512usize {
            return Err("longer than 512 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Identity3BodyLanguageVersionCompilerBuild {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3BodyLanguageVersionCompilerBuild {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Identity3BodyLanguageVersionCompilerBuild {
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
#[doc = "The component that INTERPRETS the body span. Not the build tool and not the resolver."]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Identity3BodyLanguageVersionCompilerName(::std::string::String);
impl ::std::ops::Deref for Identity3BodyLanguageVersionCompilerName {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Identity3BodyLanguageVersionCompilerName> for ::std::string::String {
    fn from(value: Identity3BodyLanguageVersionCompilerName) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Identity3BodyLanguageVersionCompilerName {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 256usize {
            return Err("longer than 256 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Identity3BodyLanguageVersionCompilerName {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3BodyLanguageVersionCompilerName {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Identity3BodyLanguageVersionCompilerName {
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
#[doc = "The release identity of that component, taken from the admitted native context. admit_native_context already refuses native.native-context-compiler-version-not-from-manifest unless it equals the admitted tool closure semanticVersion, for both languages, so this is joined to a retained closure manifest and is not a copied display string."]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Identity3BodyLanguageVersionCompilerVersion(::std::string::String);
impl ::std::ops::Deref for Identity3BodyLanguageVersionCompilerVersion {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Identity3BodyLanguageVersionCompilerVersion> for ::std::string::String {
    fn from(value: Identity3BodyLanguageVersionCompilerVersion) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Identity3BodyLanguageVersionCompilerVersion {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 256usize {
            return Err("longer than 256 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Identity3BodyLanguageVersionCompilerVersion {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
    for Identity3BodyLanguageVersionCompilerVersion
{
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Identity3BodyLanguageVersionCompilerVersion {
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
#[doc = "The SELECTED source-language dialect of the body being identified: the edition of its owning compilation unit, the source variant its own suffix denotes, or - for a grammar-only interpretation - the grammar variant that suffix selects. Never a whole map and never null - a language with no declared dialect axis would be an unexamined default, and there is none. Including a map would make one body identity depend on unrelated crates and would not be representable inside the inherited u8 component length."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
pub enum Identity3BodyLanguageVersionDialect {
    #[serde(rename = "edition")]
    Edition(ExactInteger),
    #[serde(rename = "sourceVariant")]
    SourceVariant(Identity3BodyLanguageVersionDialectSourceVariant),
    #[doc = "The dialect axis of a GRAMMAR-ONLY interpretation; used only by the syntax-only universe. A syntax-only analysis has no compilation unit, so it has no edition to select and no tsconfig program to join. Claiming an edition for a .rs body read without Cargo would fabricate compiler semantics, and reusing sourceVariant would let a grammar-parsed body carry the identical dialect token as a compiler-parsed one. The token is the variant the bundled grammar selects from the body's own suffix. Because this is a DIFFERENT branch, a syntax-only body identity can never collide with a compiler-derived identity over the same bytes - which is the intended distinction, not a defect: a grammar parse and a compiler parse are different interpretations of the span and equating them would be a false clone claim."]
    #[serde(rename = "grammarVariant")]
    GrammarVariant(Identity3BodyLanguageVersionDialectGrammarVariant),
}
impl ::std::convert::From<ExactInteger> for Identity3BodyLanguageVersionDialect {
    fn from(value: ExactInteger) -> Self {
        Self::Edition(value)
    }
}
impl ::std::convert::From<Identity3BodyLanguageVersionDialectSourceVariant>
    for Identity3BodyLanguageVersionDialect
{
    fn from(value: Identity3BodyLanguageVersionDialectSourceVariant) -> Self {
        Self::SourceVariant(value)
    }
}
impl ::std::convert::From<Identity3BodyLanguageVersionDialectGrammarVariant>
    for Identity3BodyLanguageVersionDialect
{
    fn from(value: Identity3BodyLanguageVersionDialectGrammarVariant) -> Self {
        Self::GrammarVariant(value)
    }
}
#[doc = "`Identity3BodyLanguageVersionDialectGrammarVariant`"]
#[derive(
    :: serde :: Deserialize,
    :: serde :: Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd,
)]
pub enum Identity3BodyLanguageVersionDialectGrammarVariant {
    #[serde(rename = "rs")]
    Rs,
    #[serde(rename = "ts")]
    Ts,
    #[serde(rename = "tsx")]
    Tsx,
    #[serde(rename = "ts-declaration")]
    TsDeclaration,
    #[serde(rename = "mts")]
    Mts,
    #[serde(rename = "cts")]
    Cts,
    #[serde(rename = "js")]
    Js,
    #[serde(rename = "jsx")]
    Jsx,
    #[serde(rename = "mjs")]
    Mjs,
    #[serde(rename = "cjs")]
    Cjs,
}
impl ::std::fmt::Display for Identity3BodyLanguageVersionDialectGrammarVariant {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Rs => f.write_str("rs"),
            Self::Ts => f.write_str("ts"),
            Self::Tsx => f.write_str("tsx"),
            Self::TsDeclaration => f.write_str("ts-declaration"),
            Self::Mts => f.write_str("mts"),
            Self::Cts => f.write_str("cts"),
            Self::Js => f.write_str("js"),
            Self::Jsx => f.write_str("jsx"),
            Self::Mjs => f.write_str("mjs"),
            Self::Cjs => f.write_str("cjs"),
        }
    }
}
impl ::std::str::FromStr for Identity3BodyLanguageVersionDialectGrammarVariant {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "rs" => Ok(Self::Rs),
            "ts" => Ok(Self::Ts),
            "tsx" => Ok(Self::Tsx),
            "ts-declaration" => Ok(Self::TsDeclaration),
            "mts" => Ok(Self::Mts),
            "cts" => Ok(Self::Cts),
            "js" => Ok(Self::Js),
            "jsx" => Ok(Self::Jsx),
            "mjs" => Ok(Self::Mjs),
            "cjs" => Ok(Self::Cjs),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Identity3BodyLanguageVersionDialectGrammarVariant {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
    for Identity3BodyLanguageVersionDialectGrammarVariant
{
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
#[doc = "`Identity3BodyLanguageVersionDialectSourceVariant`"]
#[derive(
    :: serde :: Deserialize,
    :: serde :: Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd,
)]
pub enum Identity3BodyLanguageVersionDialectSourceVariant {
    #[serde(rename = "ts")]
    Ts,
    #[serde(rename = "tsx")]
    Tsx,
    #[serde(rename = "ts-declaration")]
    TsDeclaration,
    #[serde(rename = "mts")]
    Mts,
    #[serde(rename = "cts")]
    Cts,
    #[serde(rename = "js")]
    Js,
    #[serde(rename = "jsx")]
    Jsx,
    #[serde(rename = "mjs")]
    Mjs,
    #[serde(rename = "cjs")]
    Cjs,
}
impl ::std::fmt::Display for Identity3BodyLanguageVersionDialectSourceVariant {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Ts => f.write_str("ts"),
            Self::Tsx => f.write_str("tsx"),
            Self::TsDeclaration => f.write_str("ts-declaration"),
            Self::Mts => f.write_str("mts"),
            Self::Cts => f.write_str("cts"),
            Self::Js => f.write_str("js"),
            Self::Jsx => f.write_str("jsx"),
            Self::Mjs => f.write_str("mjs"),
            Self::Cjs => f.write_str("cjs"),
        }
    }
}
impl ::std::str::FromStr for Identity3BodyLanguageVersionDialectSourceVariant {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "ts" => Ok(Self::Ts),
            "tsx" => Ok(Self::Tsx),
            "ts-declaration" => Ok(Self::TsDeclaration),
            "mts" => Ok(Self::Mts),
            "cts" => Ok(Self::Cts),
            "js" => Ok(Self::Js),
            "jsx" => Ok(Self::Jsx),
            "mjs" => Ok(Self::Mjs),
            "cjs" => Ok(Self::Cjs),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Identity3BodyLanguageVersionDialectSourceVariant {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
    for Identity3BodyLanguageVersionDialectSourceVariant
{
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
#[doc = "The language of the BODY, which is not always the language of the provider. Native section 6.3 puts languageId in the normalized-body preimage and closes it to {typescript, javascript, rust} so that a TypeScript body never groups with a JavaScript one even with identical bytes. One TypeScript engine universe produces bodies of BOTH: the engine is the provider, the source variant decides the body language, and section 6.4 keeps cross-TS/JS matching a separate candidate-only projection rather than a shared identity."]
#[derive(
    :: serde :: Deserialize,
    :: serde :: Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd,
)]
pub enum Identity3BodyLanguageVersionLanguageId {
    #[serde(rename = "typescript")]
    Typescript,
    #[serde(rename = "javascript")]
    Javascript,
    #[serde(rename = "rust")]
    Rust,
}
impl ::std::fmt::Display for Identity3BodyLanguageVersionLanguageId {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Typescript => f.write_str("typescript"),
            Self::Javascript => f.write_str("javascript"),
            Self::Rust => f.write_str("rust"),
        }
    }
}
impl ::std::str::FromStr for Identity3BodyLanguageVersionLanguageId {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "typescript" => Ok(Self::Typescript),
            "javascript" => Ok(Self::Javascript),
            "rust" => Ok(Self::Rust),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Identity3BodyLanguageVersionLanguageId {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3BodyLanguageVersionLanguageId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
#[doc = "`Identity3CacheKey`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3CacheKey {
    #[serde(rename = "inputRefs")]
    pub input_refs: ::std::vec::Vec<Identity3Ref>,
    #[serde(rename = "outputSchemaDigest")]
    pub output_schema_digest: ::std::string::String,
    #[serde(rename = "planId")]
    pub plan_id: ::std::string::String,
    #[serde(rename = "producerClosure")]
    pub producer_closure: ::std::string::String,
    #[serde(rename = "schemaVersion")]
    pub schema_version: ExactInteger,
    #[serde(rename = "scopeIds")]
    pub scope_ids: ::std::vec::Vec<::std::string::String>,
    #[serde(rename = "stageSpecDigest")]
    pub stage_spec_digest: ::std::string::String,
}
#[doc = "`Identity3Closure`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3Closure {
    pub kind: Identity3ClosureKind,
    #[serde(rename = "manifestDigest")]
    pub manifest_digest: ::std::string::String,
    pub platform: Identity3ClosurePlatform,
    #[serde(rename = "protocolMajor")]
    pub protocol_major: u64,
    #[serde(rename = "schemaVersion")]
    pub schema_version: ExactInteger,
    #[serde(rename = "semanticVersion")]
    pub semantic_version: Identity3ClosureSemanticVersion,
    pub tree: ::std::vec::Vec<Identity3Blob>,
}
#[doc = "`Identity3ClosureKind`"]
#[derive(
    :: serde :: Deserialize,
    :: serde :: Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd,
)]
pub enum Identity3ClosureKind {
    #[serde(rename = "provider")]
    Provider,
    #[serde(rename = "evaluator")]
    Evaluator,
    #[serde(rename = "detector")]
    Detector,
    #[serde(rename = "toolchain")]
    Toolchain,
    #[serde(rename = "stdlib")]
    Stdlib,
    #[serde(rename = "rust-dev-llvm")]
    RustDevLlvm,
    #[serde(rename = "grammar")]
    Grammar,
    #[serde(rename = "adapter")]
    Adapter,
}
impl ::std::fmt::Display for Identity3ClosureKind {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Provider => f.write_str("provider"),
            Self::Evaluator => f.write_str("evaluator"),
            Self::Detector => f.write_str("detector"),
            Self::Toolchain => f.write_str("toolchain"),
            Self::Stdlib => f.write_str("stdlib"),
            Self::RustDevLlvm => f.write_str("rust-dev-llvm"),
            Self::Grammar => f.write_str("grammar"),
            Self::Adapter => f.write_str("adapter"),
        }
    }
}
impl ::std::str::FromStr for Identity3ClosureKind {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "provider" => Ok(Self::Provider),
            "evaluator" => Ok(Self::Evaluator),
            "detector" => Ok(Self::Detector),
            "toolchain" => Ok(Self::Toolchain),
            "stdlib" => Ok(Self::Stdlib),
            "rust-dev-llvm" => Ok(Self::RustDevLlvm),
            "grammar" => Ok(Self::Grammar),
            "adapter" => Ok(Self::Adapter),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Identity3ClosureKind {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3ClosureKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
#[doc = "`Identity3ClosurePlatform`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Identity3ClosurePlatform(::std::string::String);
impl ::std::ops::Deref for Identity3ClosurePlatform {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Identity3ClosurePlatform> for ::std::string::String {
    fn from(value: Identity3ClosurePlatform) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Identity3ClosurePlatform {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 4096usize {
            return Err("longer than 4096 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Identity3ClosurePlatform {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3ClosurePlatform {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Identity3ClosurePlatform {
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
#[doc = "`Identity3ClosureSemanticVersion`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Identity3ClosureSemanticVersion(::std::string::String);
impl ::std::ops::Deref for Identity3ClosureSemanticVersion {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Identity3ClosureSemanticVersion> for ::std::string::String {
    fn from(value: Identity3ClosureSemanticVersion) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Identity3ClosureSemanticVersion {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 4096usize {
            return Err("longer than 4096 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Identity3ClosureSemanticVersion {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3ClosureSemanticVersion {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Identity3ClosureSemanticVersion {
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
#[doc = "The closed record digested by commit-receipt.inventoryDigest: the exact set of typed object identities and retained raw blob digests the commit published for this Run."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3CommitInventory {
    #[serde(rename = "blobDigests")]
    pub blob_digests: ::std::vec::Vec<::std::string::String>,
    pub objects: ::std::vec::Vec<Identity3Text>,
    #[serde(rename = "runId")]
    pub run_id: ::std::string::String,
    #[serde(rename = "schemaVersion")]
    pub schema_version: ExactInteger,
}
#[doc = "`Identity3CommitReceipt`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3CommitReceipt {
    #[serde(rename = "commitSequence")]
    pub commit_sequence: u64,
    #[serde(rename = "executionId")]
    pub execution_id: ::std::string::String,
    #[serde(rename = "inventoryDigest")]
    pub inventory_digest: ::std::string::String,
    #[serde(rename = "namespaceId")]
    pub namespace_id: Identity3CommitReceiptNamespaceId,
    #[serde(rename = "runId")]
    pub run_id: ::std::string::String,
    #[serde(rename = "schemaVersion")]
    pub schema_version: ExactInteger,
    #[serde(rename = "sealedAssurance")]
    pub sealed_assurance: Identity3CommitReceiptSealedAssurance,
    #[serde(rename = "signerKeyId")]
    pub signer_key_id: Identity3CommitReceiptSignerKeyId,
}
#[doc = "`Identity3CommitReceiptNamespaceId`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Identity3CommitReceiptNamespaceId(::std::string::String);
impl ::std::ops::Deref for Identity3CommitReceiptNamespaceId {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Identity3CommitReceiptNamespaceId> for ::std::string::String {
    fn from(value: Identity3CommitReceiptNamespaceId) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Identity3CommitReceiptNamespaceId {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 4096usize {
            return Err("longer than 4096 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Identity3CommitReceiptNamespaceId {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3CommitReceiptNamespaceId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Identity3CommitReceiptNamespaceId {
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
#[doc = "`Identity3CommitReceiptSealedAssurance`"]
#[derive(
    :: serde :: Deserialize,
    :: serde :: Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd,
)]
pub enum Identity3CommitReceiptSealedAssurance {
    #[serde(rename = "verified")]
    Verified,
    #[serde(rename = "verifiable")]
    Verifiable,
    #[serde(rename = "replayable")]
    Replayable,
}
impl ::std::fmt::Display for Identity3CommitReceiptSealedAssurance {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Verified => f.write_str("verified"),
            Self::Verifiable => f.write_str("verifiable"),
            Self::Replayable => f.write_str("replayable"),
        }
    }
}
impl ::std::str::FromStr for Identity3CommitReceiptSealedAssurance {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "verified" => Ok(Self::Verified),
            "verifiable" => Ok(Self::Verifiable),
            "replayable" => Ok(Self::Replayable),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Identity3CommitReceiptSealedAssurance {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3CommitReceiptSealedAssurance {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
#[doc = "`Identity3CommitReceiptSignerKeyId`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Identity3CommitReceiptSignerKeyId(::std::string::String);
impl ::std::ops::Deref for Identity3CommitReceiptSignerKeyId {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Identity3CommitReceiptSignerKeyId> for ::std::string::String {
    fn from(value: Identity3CommitReceiptSignerKeyId) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Identity3CommitReceiptSignerKeyId {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 4096usize {
            return Err("longer than 4096 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Identity3CommitReceiptSignerKeyId {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3CommitReceiptSignerKeyId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Identity3CommitReceiptSignerKeyId {
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
#[doc = "`Identity3Coverage`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3Coverage {
    #[serde(rename = "payloadDigest")]
    pub payload_digest: ::std::string::String,
    #[serde(rename = "payloadSchemaDigest")]
    pub payload_schema_digest: ::std::string::String,
    #[serde(rename = "schemaVersion")]
    pub schema_version: ExactInteger,
    #[serde(rename = "scopeId")]
    pub scope_id: ::std::string::String,
}
#[doc = "Registered digest-domain name. This enumeration and #/$defs/Ref/properties/domain are the same set, and both are the registered keys of x-opensip-digest-domains.byDomain."]
#[derive(
    :: serde :: Deserialize,
    :: serde :: Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd,
)]
pub enum Identity3Domain {
    #[serde(rename = "analysis-spec")]
    AnalysisSpec,
    #[serde(rename = "blob")]
    Blob,
    #[serde(rename = "cache-key")]
    CacheKey,
    #[serde(rename = "capability-manifest")]
    CapabilityManifest,
    #[serde(rename = "closure")]
    Closure,
    #[serde(rename = "configuration")]
    Configuration,
    #[serde(rename = "coverage")]
    Coverage,
    #[serde(rename = "coverage-payload")]
    CoveragePayload,
    #[serde(rename = "enumeration-plan")]
    EnumerationPlan,
    #[serde(rename = "evaluation-seal")]
    EvaluationSeal,
    #[serde(rename = "evaluation-subject")]
    EvaluationSubject,
    #[serde(rename = "evaluator-emission-plan")]
    EvaluatorEmissionPlan,
    #[serde(rename = "execution-plan")]
    ExecutionPlan,
    #[serde(rename = "fact")]
    Fact,
    #[serde(rename = "fact-payload")]
    FactPayload,
    #[serde(rename = "finding")]
    Finding,
    #[serde(rename = "finding-fingerprint")]
    FindingFingerprint,
    #[serde(rename = "finding-parameters")]
    FindingParameters,
    #[serde(rename = "import")]
    Import,
    #[serde(rename = "import-payload")]
    ImportPayload,
    #[serde(rename = "native-context")]
    NativeContext,
    #[serde(rename = "plan")]
    Plan,
    #[serde(rename = "policy")]
    Policy,
    #[serde(rename = "policy-derivation")]
    PolicyDerivation,
    #[serde(rename = "predicate-witness")]
    PredicateWitness,
    #[serde(rename = "proof-bundle")]
    ProofBundle,
    #[serde(rename = "regeneration-key")]
    RegenerationKey,
    #[serde(rename = "rule-program")]
    RuleProgram,
    #[serde(rename = "run")]
    Run,
    #[serde(rename = "schema")]
    Schema,
    #[serde(rename = "semantic-evidence")]
    SemanticEvidence,
    #[serde(rename = "snapshot")]
    Snapshot,
    #[serde(rename = "subject-inventory")]
    SubjectInventory,
    #[serde(rename = "subject-scope")]
    SubjectScope,
    #[serde(rename = "target-attribution")]
    TargetAttribution,
    #[serde(rename = "view")]
    View,
    #[serde(rename = "waiver")]
    Waiver,
    #[serde(rename = "incoming-search")]
    IncomingSearch,
    #[serde(rename = "execution-inputs")]
    ExecutionInputs,
    #[serde(rename = "candidate-producer-result")]
    CandidateProducerResult,
}
impl ::std::fmt::Display for Identity3Domain {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::AnalysisSpec => f.write_str("analysis-spec"),
            Self::Blob => f.write_str("blob"),
            Self::CacheKey => f.write_str("cache-key"),
            Self::CapabilityManifest => f.write_str("capability-manifest"),
            Self::Closure => f.write_str("closure"),
            Self::Configuration => f.write_str("configuration"),
            Self::Coverage => f.write_str("coverage"),
            Self::CoveragePayload => f.write_str("coverage-payload"),
            Self::EnumerationPlan => f.write_str("enumeration-plan"),
            Self::EvaluationSeal => f.write_str("evaluation-seal"),
            Self::EvaluationSubject => f.write_str("evaluation-subject"),
            Self::EvaluatorEmissionPlan => f.write_str("evaluator-emission-plan"),
            Self::ExecutionPlan => f.write_str("execution-plan"),
            Self::Fact => f.write_str("fact"),
            Self::FactPayload => f.write_str("fact-payload"),
            Self::Finding => f.write_str("finding"),
            Self::FindingFingerprint => f.write_str("finding-fingerprint"),
            Self::FindingParameters => f.write_str("finding-parameters"),
            Self::Import => f.write_str("import"),
            Self::ImportPayload => f.write_str("import-payload"),
            Self::NativeContext => f.write_str("native-context"),
            Self::Plan => f.write_str("plan"),
            Self::Policy => f.write_str("policy"),
            Self::PolicyDerivation => f.write_str("policy-derivation"),
            Self::PredicateWitness => f.write_str("predicate-witness"),
            Self::ProofBundle => f.write_str("proof-bundle"),
            Self::RegenerationKey => f.write_str("regeneration-key"),
            Self::RuleProgram => f.write_str("rule-program"),
            Self::Run => f.write_str("run"),
            Self::Schema => f.write_str("schema"),
            Self::SemanticEvidence => f.write_str("semantic-evidence"),
            Self::Snapshot => f.write_str("snapshot"),
            Self::SubjectInventory => f.write_str("subject-inventory"),
            Self::SubjectScope => f.write_str("subject-scope"),
            Self::TargetAttribution => f.write_str("target-attribution"),
            Self::View => f.write_str("view"),
            Self::Waiver => f.write_str("waiver"),
            Self::IncomingSearch => f.write_str("incoming-search"),
            Self::ExecutionInputs => f.write_str("execution-inputs"),
            Self::CandidateProducerResult => f.write_str("candidate-producer-result"),
        }
    }
}
impl ::std::str::FromStr for Identity3Domain {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "analysis-spec" => Ok(Self::AnalysisSpec),
            "blob" => Ok(Self::Blob),
            "cache-key" => Ok(Self::CacheKey),
            "capability-manifest" => Ok(Self::CapabilityManifest),
            "closure" => Ok(Self::Closure),
            "configuration" => Ok(Self::Configuration),
            "coverage" => Ok(Self::Coverage),
            "coverage-payload" => Ok(Self::CoveragePayload),
            "enumeration-plan" => Ok(Self::EnumerationPlan),
            "evaluation-seal" => Ok(Self::EvaluationSeal),
            "evaluation-subject" => Ok(Self::EvaluationSubject),
            "evaluator-emission-plan" => Ok(Self::EvaluatorEmissionPlan),
            "execution-plan" => Ok(Self::ExecutionPlan),
            "fact" => Ok(Self::Fact),
            "fact-payload" => Ok(Self::FactPayload),
            "finding" => Ok(Self::Finding),
            "finding-fingerprint" => Ok(Self::FindingFingerprint),
            "finding-parameters" => Ok(Self::FindingParameters),
            "import" => Ok(Self::Import),
            "import-payload" => Ok(Self::ImportPayload),
            "native-context" => Ok(Self::NativeContext),
            "plan" => Ok(Self::Plan),
            "policy" => Ok(Self::Policy),
            "policy-derivation" => Ok(Self::PolicyDerivation),
            "predicate-witness" => Ok(Self::PredicateWitness),
            "proof-bundle" => Ok(Self::ProofBundle),
            "regeneration-key" => Ok(Self::RegenerationKey),
            "rule-program" => Ok(Self::RuleProgram),
            "run" => Ok(Self::Run),
            "schema" => Ok(Self::Schema),
            "semantic-evidence" => Ok(Self::SemanticEvidence),
            "snapshot" => Ok(Self::Snapshot),
            "subject-inventory" => Ok(Self::SubjectInventory),
            "subject-scope" => Ok(Self::SubjectScope),
            "target-attribution" => Ok(Self::TargetAttribution),
            "view" => Ok(Self::View),
            "waiver" => Ok(Self::Waiver),
            "incoming-search" => Ok(Self::IncomingSearch),
            "execution-inputs" => Ok(Self::ExecutionInputs),
            "candidate-producer-result" => Ok(Self::CandidateProducerResult),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Identity3Domain {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3Domain {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
#[doc = "Closed replayed deficiency with explicit origin. evidenceKind is data provenance bound to the policy atom/declaration, not a gating flag. Native carrier, universe, subject, predicate and inputRefs are rederived from admitted inputs per composition §9.5–§9.6. Execution-assessment items use source=execution and inputRefs = ExecutionInputsV1 ref plus originating row refs. Atom items on a native/import plane copy evaluationInputRefs except Coverage-entry items which name that Coverage."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3EvaluationDeficiency {
    pub cause: Identity3EvaluationDeficiencyCause,
    #[serde(
        rename = "evidenceKind",
        deserialize_with = "::std::option::Option::deserialize"
    )]
    pub evidence_kind: ::std::option::Option<Identity3EvaluationDeficiencyEvidenceKind>,
    #[serde(rename = "inputRefs")]
    pub input_refs: ::std::vec::Vec<Identity3ProofInputRef>,
    #[serde(
        rename = "nativeCause",
        deserialize_with = "::std::option::Option::deserialize"
    )]
    pub native_cause: ::std::option::Option<Identity3EvaluationDeficiencyNativeCause>,
    #[serde(
        rename = "predicateId",
        deserialize_with = "::std::option::Option::deserialize"
    )]
    pub predicate_id: ::std::option::Option<Identity3Text>,
    pub source: Identity3EvaluationDeficiencySource,
    #[serde(
        rename = "subjectId",
        deserialize_with = "::std::option::Option::deserialize"
    )]
    pub subject_id: ::std::option::Option<::std::string::String>,
    #[serde(deserialize_with = "::std::option::Option::deserialize")]
    pub universe: ::std::option::Option<::std::string::String>,
}
#[doc = "`Identity3EvaluationDeficiencyCause`"]
#[derive(
    :: serde :: Deserialize,
    :: serde :: Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd,
)]
pub enum Identity3EvaluationDeficiencyCause {
    #[serde(rename = "anonymous-subject")]
    AnonymousSubject,
    #[serde(rename = "budget-exhausted")]
    BudgetExhausted,
    #[serde(rename = "confidence-floor-unmet")]
    ConfidenceFloorUnmet,
    #[serde(rename = "coverage-unknown")]
    CoverageUnknown,
    #[serde(rename = "cross-family-edge-not-owed")]
    CrossFamilyEdgeNotOwed,
    #[serde(rename = "derivation-policy-unmet")]
    DerivationPolicyUnmet,
    #[serde(rename = "enumeration-unknown")]
    EnumerationUnknown,
    #[serde(rename = "evidence-kind-unavailable")]
    EvidenceKindUnavailable,
    #[serde(rename = "external-consumers-unknown")]
    ExternalConsumersUnknown,
    #[serde(rename = "history-outside-collection-scope")]
    HistoryOutsideCollectionScope,
    #[serde(rename = "history-truncated")]
    HistoryTruncated,
    #[serde(rename = "import-unmapped-only")]
    ImportUnmappedOnly,
    #[serde(rename = "incomplete-inventory")]
    IncompleteInventory,
    #[serde(rename = "incomplete-observation")]
    IncompleteObservation,
    #[serde(rename = "input-closure-incomplete")]
    InputClosureIncomplete,
    #[serde(rename = "language-tier-unsupported")]
    LanguageTierUnsupported,
    #[serde(rename = "missing-relation-coverage")]
    MissingRelationCoverage,
    #[serde(rename = "no-consumable-row")]
    NoConsumableRow,
    #[serde(rename = "no-covering-program")]
    NoCoveringProgram,
    #[serde(rename = "null-exit-status")]
    NullExitStatus,
    #[serde(rename = "observation-window-insufficient")]
    ObservationWindowInsufficient,
    #[serde(rename = "overload-ambiguous")]
    OverloadAmbiguous,
    #[serde(rename = "population-incomplete")]
    PopulationIncomplete,
    #[serde(rename = "population-unknown")]
    PopulationUnknown,
    #[serde(rename = "projection-unavailable")]
    ProjectionUnavailable,
    #[serde(rename = "provider-unavailable")]
    ProviderUnavailable,
    #[serde(rename = "required-cell-unsatisfied")]
    RequiredCellUnsatisfied,
    #[serde(rename = "required-relation-missing")]
    RequiredRelationMissing,
    #[serde(rename = "resolution-incomplete")]
    ResolutionIncomplete,
    #[serde(rename = "scope-without-coverage")]
    ScopeWithoutCoverage,
    #[serde(rename = "selector-unbound")]
    SelectorUnbound,
    #[serde(rename = "signature-ambiguous")]
    SignatureAmbiguous,
    #[serde(rename = "source-syntax-invalid")]
    SourceSyntaxInvalid,
    #[serde(rename = "source-target-search-unattested")]
    SourceTargetSearchUnattested,
    #[serde(rename = "target-export-unknown")]
    TargetExportUnknown,
    #[serde(rename = "target-kind-unknown")]
    TargetKindUnknown,
    #[serde(rename = "target-metadata-unknown")]
    TargetMetadataUnknown,
    #[serde(rename = "test-completeness-not-established")]
    TestCompletenessNotEstablished,
    #[serde(rename = "unavailable-program-binding")]
    UnavailableProgramBinding,
    #[serde(rename = "uncovered-expected-source-subject")]
    UncoveredExpectedSourceSubject,
    #[serde(rename = "unknown-export-membership")]
    UnknownExportMembership,
    #[serde(rename = "unmapped-subject")]
    UnmappedSubject,
    #[serde(rename = "unobservable-subject")]
    UnobservableSubject,
    #[serde(rename = "unresolved-edge-target-unattributed")]
    UnresolvedEdgeTargetUnattributed,
    #[serde(rename = "work-budget-exhausted")]
    WorkBudgetExhausted,
    #[serde(rename = "wrapper-partial")]
    WrapperPartial,
    #[serde(rename = "zero-owed-wrappers")]
    ZeroOwedWrappers,
}
impl ::std::fmt::Display for Identity3EvaluationDeficiencyCause {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::AnonymousSubject => f.write_str("anonymous-subject"),
            Self::BudgetExhausted => f.write_str("budget-exhausted"),
            Self::ConfidenceFloorUnmet => f.write_str("confidence-floor-unmet"),
            Self::CoverageUnknown => f.write_str("coverage-unknown"),
            Self::CrossFamilyEdgeNotOwed => f.write_str("cross-family-edge-not-owed"),
            Self::DerivationPolicyUnmet => f.write_str("derivation-policy-unmet"),
            Self::EnumerationUnknown => f.write_str("enumeration-unknown"),
            Self::EvidenceKindUnavailable => f.write_str("evidence-kind-unavailable"),
            Self::ExternalConsumersUnknown => f.write_str("external-consumers-unknown"),
            Self::HistoryOutsideCollectionScope => f.write_str("history-outside-collection-scope"),
            Self::HistoryTruncated => f.write_str("history-truncated"),
            Self::ImportUnmappedOnly => f.write_str("import-unmapped-only"),
            Self::IncompleteInventory => f.write_str("incomplete-inventory"),
            Self::IncompleteObservation => f.write_str("incomplete-observation"),
            Self::InputClosureIncomplete => f.write_str("input-closure-incomplete"),
            Self::LanguageTierUnsupported => f.write_str("language-tier-unsupported"),
            Self::MissingRelationCoverage => f.write_str("missing-relation-coverage"),
            Self::NoConsumableRow => f.write_str("no-consumable-row"),
            Self::NoCoveringProgram => f.write_str("no-covering-program"),
            Self::NullExitStatus => f.write_str("null-exit-status"),
            Self::ObservationWindowInsufficient => f.write_str("observation-window-insufficient"),
            Self::OverloadAmbiguous => f.write_str("overload-ambiguous"),
            Self::PopulationIncomplete => f.write_str("population-incomplete"),
            Self::PopulationUnknown => f.write_str("population-unknown"),
            Self::ProjectionUnavailable => f.write_str("projection-unavailable"),
            Self::ProviderUnavailable => f.write_str("provider-unavailable"),
            Self::RequiredCellUnsatisfied => f.write_str("required-cell-unsatisfied"),
            Self::RequiredRelationMissing => f.write_str("required-relation-missing"),
            Self::ResolutionIncomplete => f.write_str("resolution-incomplete"),
            Self::ScopeWithoutCoverage => f.write_str("scope-without-coverage"),
            Self::SelectorUnbound => f.write_str("selector-unbound"),
            Self::SignatureAmbiguous => f.write_str("signature-ambiguous"),
            Self::SourceSyntaxInvalid => f.write_str("source-syntax-invalid"),
            Self::SourceTargetSearchUnattested => f.write_str("source-target-search-unattested"),
            Self::TargetExportUnknown => f.write_str("target-export-unknown"),
            Self::TargetKindUnknown => f.write_str("target-kind-unknown"),
            Self::TargetMetadataUnknown => f.write_str("target-metadata-unknown"),
            Self::TestCompletenessNotEstablished => {
                f.write_str("test-completeness-not-established")
            }
            Self::UnavailableProgramBinding => f.write_str("unavailable-program-binding"),
            Self::UncoveredExpectedSourceSubject => {
                f.write_str("uncovered-expected-source-subject")
            }
            Self::UnknownExportMembership => f.write_str("unknown-export-membership"),
            Self::UnmappedSubject => f.write_str("unmapped-subject"),
            Self::UnobservableSubject => f.write_str("unobservable-subject"),
            Self::UnresolvedEdgeTargetUnattributed => {
                f.write_str("unresolved-edge-target-unattributed")
            }
            Self::WorkBudgetExhausted => f.write_str("work-budget-exhausted"),
            Self::WrapperPartial => f.write_str("wrapper-partial"),
            Self::ZeroOwedWrappers => f.write_str("zero-owed-wrappers"),
        }
    }
}
impl ::std::str::FromStr for Identity3EvaluationDeficiencyCause {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "anonymous-subject" => Ok(Self::AnonymousSubject),
            "budget-exhausted" => Ok(Self::BudgetExhausted),
            "confidence-floor-unmet" => Ok(Self::ConfidenceFloorUnmet),
            "coverage-unknown" => Ok(Self::CoverageUnknown),
            "cross-family-edge-not-owed" => Ok(Self::CrossFamilyEdgeNotOwed),
            "derivation-policy-unmet" => Ok(Self::DerivationPolicyUnmet),
            "enumeration-unknown" => Ok(Self::EnumerationUnknown),
            "evidence-kind-unavailable" => Ok(Self::EvidenceKindUnavailable),
            "external-consumers-unknown" => Ok(Self::ExternalConsumersUnknown),
            "history-outside-collection-scope" => Ok(Self::HistoryOutsideCollectionScope),
            "history-truncated" => Ok(Self::HistoryTruncated),
            "import-unmapped-only" => Ok(Self::ImportUnmappedOnly),
            "incomplete-inventory" => Ok(Self::IncompleteInventory),
            "incomplete-observation" => Ok(Self::IncompleteObservation),
            "input-closure-incomplete" => Ok(Self::InputClosureIncomplete),
            "language-tier-unsupported" => Ok(Self::LanguageTierUnsupported),
            "missing-relation-coverage" => Ok(Self::MissingRelationCoverage),
            "no-consumable-row" => Ok(Self::NoConsumableRow),
            "no-covering-program" => Ok(Self::NoCoveringProgram),
            "null-exit-status" => Ok(Self::NullExitStatus),
            "observation-window-insufficient" => Ok(Self::ObservationWindowInsufficient),
            "overload-ambiguous" => Ok(Self::OverloadAmbiguous),
            "population-incomplete" => Ok(Self::PopulationIncomplete),
            "population-unknown" => Ok(Self::PopulationUnknown),
            "projection-unavailable" => Ok(Self::ProjectionUnavailable),
            "provider-unavailable" => Ok(Self::ProviderUnavailable),
            "required-cell-unsatisfied" => Ok(Self::RequiredCellUnsatisfied),
            "required-relation-missing" => Ok(Self::RequiredRelationMissing),
            "resolution-incomplete" => Ok(Self::ResolutionIncomplete),
            "scope-without-coverage" => Ok(Self::ScopeWithoutCoverage),
            "selector-unbound" => Ok(Self::SelectorUnbound),
            "signature-ambiguous" => Ok(Self::SignatureAmbiguous),
            "source-syntax-invalid" => Ok(Self::SourceSyntaxInvalid),
            "source-target-search-unattested" => Ok(Self::SourceTargetSearchUnattested),
            "target-export-unknown" => Ok(Self::TargetExportUnknown),
            "target-kind-unknown" => Ok(Self::TargetKindUnknown),
            "target-metadata-unknown" => Ok(Self::TargetMetadataUnknown),
            "test-completeness-not-established" => Ok(Self::TestCompletenessNotEstablished),
            "unavailable-program-binding" => Ok(Self::UnavailableProgramBinding),
            "uncovered-expected-source-subject" => Ok(Self::UncoveredExpectedSourceSubject),
            "unknown-export-membership" => Ok(Self::UnknownExportMembership),
            "unmapped-subject" => Ok(Self::UnmappedSubject),
            "unobservable-subject" => Ok(Self::UnobservableSubject),
            "unresolved-edge-target-unattributed" => Ok(Self::UnresolvedEdgeTargetUnattributed),
            "work-budget-exhausted" => Ok(Self::WorkBudgetExhausted),
            "wrapper-partial" => Ok(Self::WrapperPartial),
            "zero-owed-wrappers" => Ok(Self::ZeroOwedWrappers),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Identity3EvaluationDeficiencyCause {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3EvaluationDeficiencyCause {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
#[doc = "`Identity3EvaluationDeficiencyEvidenceKind`"]
#[derive(
    :: serde :: Deserialize,
    :: serde :: Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd,
)]
pub enum Identity3EvaluationDeficiencyEvidenceKind {
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
impl ::std::fmt::Display for Identity3EvaluationDeficiencyEvidenceKind {
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
impl ::std::str::FromStr for Identity3EvaluationDeficiencyEvidenceKind {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
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
impl ::std::convert::TryFrom<&str> for Identity3EvaluationDeficiencyEvidenceKind {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3EvaluationDeficiencyEvidenceKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
#[doc = "The typed cause carried beside a DeficiencyV2 in a Coverage entry. The three body-language-* members are the clones ownership states that identity-and-evidence and native-evidence section 11 require the clones Coverage to DISCLOSE: the contract mandates that such a scope mint no body identity, that its Coverage report the incompleteness, and that the predicate and seal be indeterminate rather than a false pass -- and until these members existed no value in this closed vocabulary could name why. A nullable nativeCause does not satisfy a mandated disclosure; a null there records that a disclosure was owed and not made. The other selectionLaw causes deliberately have NO member here: BODY_LANGUAGE_OWNER_NOT_COMPILED and BODY_LANGUAGE_OWNER_NOT_SELECTED are per-body refusals that section 11 states are compatible with coverage=complete (the host examined that subject and correctly produced no fact for it), and BODY_LANGUAGE_DIALECT_ABSENT/BODY_LANGUAGE_DIALECT_AMBIGUOUS are universe-level dialect faults that refuse before any Coverage entry is minted."]
#[derive(
    :: serde :: Deserialize,
    :: serde :: Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd,
)]
pub enum Identity3EvaluationDeficiencyNativeCause {
    #[serde(rename = "body-language-owner-ambiguous")]
    BodyLanguageOwnerAmbiguous,
    #[serde(rename = "body-language-owner-unenumerated")]
    BodyLanguageOwnerUnenumerated,
    #[serde(rename = "body-language-ownership-missing")]
    BodyLanguageOwnershipMissing,
    #[serde(rename = "capability-missing")]
    CapabilityMissing,
    #[serde(rename = "config-flag-stripped")]
    ConfigFlagStripped,
    #[serde(rename = "generated-file-missing")]
    GeneratedFileMissing,
    #[serde(rename = "generated-file-out-of-bounds")]
    GeneratedFileOutOfBounds,
    #[serde(rename = "generated-output-unavailable")]
    GeneratedOutputUnavailable,
    #[serde(rename = "linker-unavailable")]
    LinkerUnavailable,
    #[serde(rename = "lockfile-missing")]
    LockfileMissing,
    #[serde(rename = "missing-dependency-source")]
    MissingDependencySource,
    #[serde(rename = "no-program-unit")]
    NoProgramUnit,
    #[serde(rename = "node-modules-outside-read-set")]
    NodeModulesOutsideReadSet,
    #[serde(rename = "source-replacement-outside-snapshot")]
    SourceReplacementOutsideSnapshot,
}
impl ::std::fmt::Display for Identity3EvaluationDeficiencyNativeCause {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::BodyLanguageOwnerAmbiguous => f.write_str("body-language-owner-ambiguous"),
            Self::BodyLanguageOwnerUnenumerated => f.write_str("body-language-owner-unenumerated"),
            Self::BodyLanguageOwnershipMissing => f.write_str("body-language-ownership-missing"),
            Self::CapabilityMissing => f.write_str("capability-missing"),
            Self::ConfigFlagStripped => f.write_str("config-flag-stripped"),
            Self::GeneratedFileMissing => f.write_str("generated-file-missing"),
            Self::GeneratedFileOutOfBounds => f.write_str("generated-file-out-of-bounds"),
            Self::GeneratedOutputUnavailable => f.write_str("generated-output-unavailable"),
            Self::LinkerUnavailable => f.write_str("linker-unavailable"),
            Self::LockfileMissing => f.write_str("lockfile-missing"),
            Self::MissingDependencySource => f.write_str("missing-dependency-source"),
            Self::NoProgramUnit => f.write_str("no-program-unit"),
            Self::NodeModulesOutsideReadSet => f.write_str("node-modules-outside-read-set"),
            Self::SourceReplacementOutsideSnapshot => {
                f.write_str("source-replacement-outside-snapshot")
            }
        }
    }
}
impl ::std::str::FromStr for Identity3EvaluationDeficiencyNativeCause {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "body-language-owner-ambiguous" => Ok(Self::BodyLanguageOwnerAmbiguous),
            "body-language-owner-unenumerated" => Ok(Self::BodyLanguageOwnerUnenumerated),
            "body-language-ownership-missing" => Ok(Self::BodyLanguageOwnershipMissing),
            "capability-missing" => Ok(Self::CapabilityMissing),
            "config-flag-stripped" => Ok(Self::ConfigFlagStripped),
            "generated-file-missing" => Ok(Self::GeneratedFileMissing),
            "generated-file-out-of-bounds" => Ok(Self::GeneratedFileOutOfBounds),
            "generated-output-unavailable" => Ok(Self::GeneratedOutputUnavailable),
            "linker-unavailable" => Ok(Self::LinkerUnavailable),
            "lockfile-missing" => Ok(Self::LockfileMissing),
            "missing-dependency-source" => Ok(Self::MissingDependencySource),
            "no-program-unit" => Ok(Self::NoProgramUnit),
            "node-modules-outside-read-set" => Ok(Self::NodeModulesOutsideReadSet),
            "source-replacement-outside-snapshot" => Ok(Self::SourceReplacementOutsideSnapshot),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Identity3EvaluationDeficiencyNativeCause {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3EvaluationDeficiencyNativeCause {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
#[doc = "`Identity3EvaluationDeficiencySource`"]
#[derive(
    :: serde :: Deserialize,
    :: serde :: Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd,
)]
pub enum Identity3EvaluationDeficiencySource {
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
impl ::std::fmt::Display for Identity3EvaluationDeficiencySource {
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
impl ::std::str::FromStr for Identity3EvaluationDeficiencySource {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
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
impl ::std::convert::TryFrom<&str> for Identity3EvaluationDeficiencySource {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3EvaluationDeficiencySource {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
#[doc = "`Identity3EvaluationSeal`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3EvaluationSeal {
    #[serde(rename = "evaluatorClosure")]
    pub evaluator_closure: ::std::string::String,
    #[serde(rename = "evidenceId")]
    pub evidence_id: ::std::string::String,
    #[serde(rename = "executionPlanId")]
    pub execution_plan_id: ::std::string::String,
    #[serde(rename = "planId")]
    pub plan_id: ::std::string::String,
    #[serde(rename = "policyDigest")]
    pub policy_digest: ::std::string::String,
    #[serde(rename = "proofBundleId")]
    pub proof_bundle_id: ::std::string::String,
    #[serde(rename = "schemaVersion")]
    pub schema_version: ExactInteger,
    pub verdict: Identity3EvaluationSealVerdict,
}
#[doc = "`Identity3EvaluationSealVerdict`"]
#[derive(
    :: serde :: Deserialize,
    :: serde :: Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd,
)]
pub enum Identity3EvaluationSealVerdict {
    #[serde(rename = "pass")]
    Pass,
    #[serde(rename = "fail")]
    Fail,
    #[serde(rename = "indeterminate")]
    Indeterminate,
}
impl ::std::fmt::Display for Identity3EvaluationSealVerdict {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Pass => f.write_str("pass"),
            Self::Fail => f.write_str("fail"),
            Self::Indeterminate => f.write_str("indeterminate"),
        }
    }
}
impl ::std::str::FromStr for Identity3EvaluationSealVerdict {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "pass" => Ok(Self::Pass),
            "fail" => Ok(Self::Fail),
            "indeterminate" => Ok(Self::Indeterminate),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Identity3EvaluationSealVerdict {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3EvaluationSealVerdict {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
#[doc = "Configuration-qualified subject. File/symbol native IDs are unique in kind/universe. Package names can repeat at different first-party manifests, so packageManifestPath is a required package-only coordinate. No synthetic native package spelling or encounter-order suffix."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3EvaluationSubject {
    pub kind: Identity3EvaluationSubjectKind,
    #[serde(rename = "nativeSubjectId")]
    pub native_subject_id: Identity3Text,
    #[serde(
        rename = "packageManifestPath",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub package_manifest_path: FieldPresence<::std::option::Option<Identity3LogicalPath>>,
    #[serde(rename = "schemaVersion")]
    pub schema_version: ExactInteger,
    pub universe: ::std::string::String,
}
#[doc = "`Identity3EvaluationSubjectKind`"]
#[derive(
    :: serde :: Deserialize,
    :: serde :: Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd,
)]
pub enum Identity3EvaluationSubjectKind {
    #[serde(rename = "file")]
    File,
    #[serde(rename = "symbol")]
    Symbol,
    #[serde(rename = "package")]
    Package,
}
impl ::std::fmt::Display for Identity3EvaluationSubjectKind {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::File => f.write_str("file"),
            Self::Symbol => f.write_str("symbol"),
            Self::Package => f.write_str("package"),
        }
    }
}
impl ::std::str::FromStr for Identity3EvaluationSubjectKind {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "file" => Ok(Self::File),
            "symbol" => Ok(Self::Symbol),
            "package" => Ok(Self::Package),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Identity3EvaluationSubjectKind {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3EvaluationSubjectKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
#[doc = "`Identity3ExecutionPlan`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3ExecutionPlan {
    #[serde(rename = "planId")]
    pub plan_id: ::std::string::String,
    #[serde(rename = "schemaVersion")]
    pub schema_version: ExactInteger,
    pub stages: ::std::vec::Vec<Identity3ExecutionPlanStagesItem>,
}
#[doc = "`Identity3ExecutionPlanStagesItem`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3ExecutionPlanStagesItem {
    pub ordinal: u64,
    #[doc = "Declared output-domain set. Empty is permitted and asserts no output domains; it does not establish completeness or result authority. Stage and stage-spec sets must agree."]
    #[serde(rename = "outputDomains")]
    pub output_domains: ::std::vec::Vec<Identity3Domain>,
    pub requires: ::std::vec::Vec<u64>,
    #[serde(rename = "stageSpecDigest")]
    pub stage_spec_digest: ::std::string::String,
}
#[doc = "`Identity3Fact`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3Fact {
    pub anchors: ::std::vec::Vec<Identity3FactAnchorsItem>,
    #[serde(rename = "confidenceMillionths")]
    pub confidence_millionths: i64,
    #[serde(rename = "payloadDigest")]
    pub payload_digest: ::std::string::String,
    #[serde(rename = "payloadSchemaDigest")]
    pub payload_schema_digest: ::std::string::String,
    #[serde(rename = "producerClosure")]
    pub producer_closure: ::std::string::String,
    pub relation: Identity3FactRelation,
    pub resolution: Identity3FactResolution,
    #[serde(rename = "schemaVersion")]
    pub schema_version: ExactInteger,
    #[serde(rename = "snapshotId")]
    pub snapshot_id: ::std::string::String,
    #[serde(rename = "sourceUniverse")]
    pub source_universe: ::std::string::String,
    #[serde(rename = "targetUniverse")]
    pub target_universe: ::std::string::String,
}
#[doc = "`Identity3FactAnchorsItem`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3FactAnchorsItem {
    #[serde(rename = "blobDigest")]
    pub blob_digest: ::std::string::String,
    #[serde(rename = "endByte")]
    pub end_byte: u64,
    pub path: Identity3FactAnchorsItemPath,
    #[serde(rename = "startByte")]
    pub start_byte: u64,
}
#[doc = "`Identity3FactAnchorsItemPath`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Identity3FactAnchorsItemPath(::std::string::String);
impl ::std::ops::Deref for Identity3FactAnchorsItemPath {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Identity3FactAnchorsItemPath> for ::std::string::String {
    fn from(value: Identity3FactAnchorsItemPath) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Identity3FactAnchorsItemPath {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 4096usize {
            return Err("longer than 4096 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Identity3FactAnchorsItemPath {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3FactAnchorsItemPath {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Identity3FactAnchorsItemPath {
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
#[doc = "`Identity3FactRelation`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Identity3FactRelation(::std::string::String);
impl ::std::ops::Deref for Identity3FactRelation {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Identity3FactRelation> for ::std::string::String {
    fn from(value: Identity3FactRelation) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Identity3FactRelation {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 4096usize {
            return Err("longer than 4096 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Identity3FactRelation {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3FactRelation {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Identity3FactRelation {
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
#[doc = "`Identity3FactResolution`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Identity3FactResolution(::std::string::String);
impl ::std::ops::Deref for Identity3FactResolution {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Identity3FactResolution> for ::std::string::String {
    fn from(value: Identity3FactResolution) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Identity3FactResolution {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 4096usize {
            return Err("longer than 4096 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Identity3FactResolution {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3FactResolution {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Identity3FactResolution {
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
#[doc = "Version3 finding: one full configuration-qualified occurrence. subjectId is evaluation-subject; fingerprint is unchanged logical correspondence. Baseline projection groups only identical logical fingerprint descriptors and complete BaselineEntry fields."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3Finding {
    pub correspondence: Identity3FindingCorrespondence,
    #[doc = "Root predicate-witness digest; descendant known and uncertain facts; descendant witness coverageIds (consulted); descendant matching/uncertain observation importIds; and every evaluationInputRefs member with domain=import. Enumeration/execution inventory refs stay on the proof. composition §9.7."]
    #[serde(rename = "evidenceRefs")]
    pub evidence_refs: ::std::vec::Vec<Identity3FindingEvidenceRef>,
    #[serde(deserialize_with = "::std::option::Option::deserialize")]
    pub fingerprint: ::std::option::Option<::std::string::String>,
    #[serde(rename = "messageCode")]
    pub message_code: Identity3FindingMessageCode,
    #[serde(rename = "parameterDigest")]
    pub parameter_digest: ::std::string::String,
    #[serde(rename = "ruleClosure")]
    pub rule_closure: ::std::string::String,
    #[serde(rename = "ruleId")]
    pub rule_id: Identity3Text,
    #[serde(rename = "schemaVersion")]
    pub schema_version: ExactInteger,
    pub severity: Identity3FindingSeverity,
    pub subject: Identity3FindingSubject,
    #[serde(rename = "subjectId")]
    pub subject_id: ::std::string::String,
}
#[doc = "`Identity3FindingCorrespondence`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3FindingCorrespondence {
    #[serde(deserialize_with = "::std::option::Option::deserialize")]
    pub reason: ::std::option::Option<Identity3FindingCorrespondenceReason>,
    pub state: Identity3FindingCorrespondenceState,
}
#[doc = "`Identity3FindingCorrespondenceReason`"]
#[derive(
    :: serde :: Deserialize,
    :: serde :: Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd,
)]
pub enum Identity3FindingCorrespondenceReason {
    #[serde(rename = "projection-unavailable")]
    ProjectionUnavailable,
    #[serde(rename = "signature-ambiguous")]
    SignatureAmbiguous,
    #[serde(rename = "anonymous-subject")]
    AnonymousSubject,
    #[serde(rename = "population-incomplete")]
    PopulationIncomplete,
}
impl ::std::fmt::Display for Identity3FindingCorrespondenceReason {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::ProjectionUnavailable => f.write_str("projection-unavailable"),
            Self::SignatureAmbiguous => f.write_str("signature-ambiguous"),
            Self::AnonymousSubject => f.write_str("anonymous-subject"),
            Self::PopulationIncomplete => f.write_str("population-incomplete"),
        }
    }
}
impl ::std::str::FromStr for Identity3FindingCorrespondenceReason {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "projection-unavailable" => Ok(Self::ProjectionUnavailable),
            "signature-ambiguous" => Ok(Self::SignatureAmbiguous),
            "anonymous-subject" => Ok(Self::AnonymousSubject),
            "population-incomplete" => Ok(Self::PopulationIncomplete),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Identity3FindingCorrespondenceReason {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3FindingCorrespondenceReason {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
#[doc = "`Identity3FindingCorrespondenceState`"]
#[derive(
    :: serde :: Deserialize,
    :: serde :: Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd,
)]
pub enum Identity3FindingCorrespondenceState {
    #[serde(rename = "matched")]
    Matched,
    #[serde(rename = "unmatched")]
    Unmatched,
}
impl ::std::fmt::Display for Identity3FindingCorrespondenceState {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Matched => f.write_str("matched"),
            Self::Unmatched => f.write_str("unmatched"),
        }
    }
}
impl ::std::str::FromStr for Identity3FindingCorrespondenceState {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "matched" => Ok(Self::Matched),
            "unmatched" => Ok(Self::Unmatched),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Identity3FindingCorrespondenceState {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3FindingCorrespondenceState {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
#[doc = "`Identity3FindingEvidenceRef`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3FindingEvidenceRef {
    pub digest: ::std::string::String,
    pub domain: Identity3FindingEvidenceRefDomain,
}
#[doc = "`Identity3FindingEvidenceRefDomain`"]
#[derive(
    :: serde :: Deserialize,
    :: serde :: Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd,
)]
pub enum Identity3FindingEvidenceRefDomain {
    #[serde(rename = "fact")]
    Fact,
    #[serde(rename = "coverage")]
    Coverage,
    #[serde(rename = "import")]
    Import,
    #[serde(rename = "predicate-witness")]
    PredicateWitness,
    #[serde(rename = "blob")]
    Blob,
}
impl ::std::fmt::Display for Identity3FindingEvidenceRefDomain {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Fact => f.write_str("fact"),
            Self::Coverage => f.write_str("coverage"),
            Self::Import => f.write_str("import"),
            Self::PredicateWitness => f.write_str("predicate-witness"),
            Self::Blob => f.write_str("blob"),
        }
    }
}
impl ::std::str::FromStr for Identity3FindingEvidenceRefDomain {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "fact" => Ok(Self::Fact),
            "coverage" => Ok(Self::Coverage),
            "import" => Ok(Self::Import),
            "predicate-witness" => Ok(Self::PredicateWitness),
            "blob" => Ok(Self::Blob),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Identity3FindingEvidenceRefDomain {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3FindingEvidenceRefDomain {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
#[doc = "`Identity3FindingFingerprint`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3FindingFingerprint {
    #[serde(rename = "detectorSemanticsMajor")]
    pub detector_semantics_major: u64,
    #[serde(rename = "relatedSubjectKeys")]
    pub related_subject_keys: ::std::vec::Vec<Identity3FindingFingerprintRelatedSubjectKeysItem>,
    #[serde(rename = "ruleStableId")]
    pub rule_stable_id: Identity3FindingFingerprintRuleStableId,
    #[serde(rename = "schemaVersion")]
    pub schema_version: ExactInteger,
    #[serde(rename = "subjectKey")]
    pub subject_key: Identity3FindingFingerprintSubjectKey,
}
#[doc = "`Identity3FindingFingerprintRelatedSubjectKeysItem`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Identity3FindingFingerprintRelatedSubjectKeysItem(::std::string::String);
impl ::std::ops::Deref for Identity3FindingFingerprintRelatedSubjectKeysItem {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Identity3FindingFingerprintRelatedSubjectKeysItem>
    for ::std::string::String
{
    fn from(value: Identity3FindingFingerprintRelatedSubjectKeysItem) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Identity3FindingFingerprintRelatedSubjectKeysItem {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 4096usize {
            return Err("longer than 4096 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Identity3FindingFingerprintRelatedSubjectKeysItem {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
    for Identity3FindingFingerprintRelatedSubjectKeysItem
{
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Identity3FindingFingerprintRelatedSubjectKeysItem {
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
#[doc = "`Identity3FindingFingerprintRuleStableId`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Identity3FindingFingerprintRuleStableId(::std::string::String);
impl ::std::ops::Deref for Identity3FindingFingerprintRuleStableId {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Identity3FindingFingerprintRuleStableId> for ::std::string::String {
    fn from(value: Identity3FindingFingerprintRuleStableId) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Identity3FindingFingerprintRuleStableId {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 4096usize {
            return Err("longer than 4096 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Identity3FindingFingerprintRuleStableId {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3FindingFingerprintRuleStableId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Identity3FindingFingerprintRuleStableId {
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
#[doc = "`Identity3FindingFingerprintSubjectKey`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3FindingFingerprintSubjectKey {
    pub discriminator: Identity3FindingFingerprintSubjectKeyDiscriminator,
    pub kind: Identity3FindingFingerprintSubjectKeyKind,
    pub language: Identity3FindingFingerprintSubjectKeyLanguage,
    #[serde(rename = "logicalPath")]
    pub logical_path: Identity3FindingFingerprintSubjectKeyLogicalPath,
    #[serde(rename = "qualifiedName")]
    pub qualified_name: Identity3FindingFingerprintSubjectKeyQualifiedName,
}
#[doc = "`Identity3FindingFingerprintSubjectKeyDiscriminator`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Identity3FindingFingerprintSubjectKeyDiscriminator(::std::string::String);
impl ::std::ops::Deref for Identity3FindingFingerprintSubjectKeyDiscriminator {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Identity3FindingFingerprintSubjectKeyDiscriminator>
    for ::std::string::String
{
    fn from(value: Identity3FindingFingerprintSubjectKeyDiscriminator) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Identity3FindingFingerprintSubjectKeyDiscriminator {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 4096usize {
            return Err("longer than 4096 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Identity3FindingFingerprintSubjectKeyDiscriminator {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
    for Identity3FindingFingerprintSubjectKeyDiscriminator
{
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Identity3FindingFingerprintSubjectKeyDiscriminator {
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
#[doc = "`Identity3FindingFingerprintSubjectKeyKind`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Identity3FindingFingerprintSubjectKeyKind(::std::string::String);
impl ::std::ops::Deref for Identity3FindingFingerprintSubjectKeyKind {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Identity3FindingFingerprintSubjectKeyKind> for ::std::string::String {
    fn from(value: Identity3FindingFingerprintSubjectKeyKind) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Identity3FindingFingerprintSubjectKeyKind {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 4096usize {
            return Err("longer than 4096 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Identity3FindingFingerprintSubjectKeyKind {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3FindingFingerprintSubjectKeyKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Identity3FindingFingerprintSubjectKeyKind {
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
#[doc = "`Identity3FindingFingerprintSubjectKeyLanguage`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Identity3FindingFingerprintSubjectKeyLanguage(::std::string::String);
impl ::std::ops::Deref for Identity3FindingFingerprintSubjectKeyLanguage {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Identity3FindingFingerprintSubjectKeyLanguage> for ::std::string::String {
    fn from(value: Identity3FindingFingerprintSubjectKeyLanguage) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Identity3FindingFingerprintSubjectKeyLanguage {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 4096usize {
            return Err("longer than 4096 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Identity3FindingFingerprintSubjectKeyLanguage {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
    for Identity3FindingFingerprintSubjectKeyLanguage
{
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Identity3FindingFingerprintSubjectKeyLanguage {
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
#[doc = "`Identity3FindingFingerprintSubjectKeyLogicalPath`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Identity3FindingFingerprintSubjectKeyLogicalPath(::std::string::String);
impl ::std::ops::Deref for Identity3FindingFingerprintSubjectKeyLogicalPath {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Identity3FindingFingerprintSubjectKeyLogicalPath>
    for ::std::string::String
{
    fn from(value: Identity3FindingFingerprintSubjectKeyLogicalPath) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Identity3FindingFingerprintSubjectKeyLogicalPath {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 4096usize {
            return Err("longer than 4096 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Identity3FindingFingerprintSubjectKeyLogicalPath {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
    for Identity3FindingFingerprintSubjectKeyLogicalPath
{
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Identity3FindingFingerprintSubjectKeyLogicalPath {
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
#[doc = "`Identity3FindingFingerprintSubjectKeyQualifiedName`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Identity3FindingFingerprintSubjectKeyQualifiedName(::std::string::String);
impl ::std::ops::Deref for Identity3FindingFingerprintSubjectKeyQualifiedName {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Identity3FindingFingerprintSubjectKeyQualifiedName>
    for ::std::string::String
{
    fn from(value: Identity3FindingFingerprintSubjectKeyQualifiedName) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Identity3FindingFingerprintSubjectKeyQualifiedName {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 4096usize {
            return Err("longer than 4096 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Identity3FindingFingerprintSubjectKeyQualifiedName {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
    for Identity3FindingFingerprintSubjectKeyQualifiedName
{
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Identity3FindingFingerprintSubjectKeyQualifiedName {
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
#[doc = "`Identity3FindingMessageCode`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Identity3FindingMessageCode(::std::string::String);
impl ::std::ops::Deref for Identity3FindingMessageCode {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Identity3FindingMessageCode> for ::std::string::String {
    fn from(value: Identity3FindingMessageCode) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Identity3FindingMessageCode {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 4096usize {
            return Err("longer than 4096 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Identity3FindingMessageCode {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3FindingMessageCode {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Identity3FindingMessageCode {
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
#[doc = "The closed record digested by finding.parameterDigest. parameters is an object map so that parameter names are unique and ordered by the canonical encoder itself, with no ordering annotation to elect."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3FindingParameters {
    #[serde(rename = "messageCode")]
    pub message_code: Identity3Text,
    pub parameters: ::std::collections::BTreeMap<
        Identity3FindingParametersParametersKey,
        Identity3FindingParametersParametersValue,
    >,
    #[serde(rename = "schemaVersion")]
    pub schema_version: ExactInteger,
}
#[doc = "`Identity3FindingParametersParametersKey`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Identity3FindingParametersParametersKey(::std::string::String);
impl ::std::ops::Deref for Identity3FindingParametersParametersKey {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Identity3FindingParametersParametersKey> for ::std::string::String {
    fn from(value: Identity3FindingParametersParametersKey) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Identity3FindingParametersParametersKey {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 128usize {
            return Err("longer than 128 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Identity3FindingParametersParametersKey {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3FindingParametersParametersKey {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Identity3FindingParametersParametersKey {
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
#[doc = "`Identity3FindingParametersParametersValue`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(untagged)]
pub enum Identity3FindingParametersParametersValue {
    String(Identity3FindingParametersParametersValueString),
    Integer(ExactInteger),
    Boolean(bool),
}
impl ::std::fmt::Display for Identity3FindingParametersParametersValue {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match self {
            Self::String(x) => x.fmt(f),
            Self::Integer(x) => x.fmt(f),
            Self::Boolean(x) => x.fmt(f),
        }
    }
}
impl ::std::convert::From<Identity3FindingParametersParametersValueString>
    for Identity3FindingParametersParametersValue
{
    fn from(value: Identity3FindingParametersParametersValueString) -> Self {
        Self::String(value)
    }
}
impl ::std::convert::From<ExactInteger> for Identity3FindingParametersParametersValue {
    fn from(value: ExactInteger) -> Self {
        Self::Integer(value)
    }
}
impl ::std::convert::From<bool> for Identity3FindingParametersParametersValue {
    fn from(value: bool) -> Self {
        Self::Boolean(value)
    }
}
#[doc = "`Identity3FindingParametersParametersValueString`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Identity3FindingParametersParametersValueString(::std::string::String);
impl ::std::ops::Deref for Identity3FindingParametersParametersValueString {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Identity3FindingParametersParametersValueString>
    for ::std::string::String
{
    fn from(value: Identity3FindingParametersParametersValueString) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Identity3FindingParametersParametersValueString {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 4096usize {
            return Err("longer than 4096 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Identity3FindingParametersParametersValueString {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
    for Identity3FindingParametersParametersValueString
{
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Identity3FindingParametersParametersValueString {
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
#[doc = "`Identity3FindingSeverity`"]
#[derive(
    :: serde :: Deserialize,
    :: serde :: Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd,
)]
pub enum Identity3FindingSeverity {
    #[serde(rename = "note")]
    Note,
    #[serde(rename = "warning")]
    Warning,
    #[serde(rename = "error")]
    Error,
}
impl ::std::fmt::Display for Identity3FindingSeverity {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Note => f.write_str("note"),
            Self::Warning => f.write_str("warning"),
            Self::Error => f.write_str("error"),
        }
    }
}
impl ::std::str::FromStr for Identity3FindingSeverity {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "note" => Ok(Self::Note),
            "warning" => Ok(Self::Warning),
            "error" => Ok(Self::Error),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Identity3FindingSeverity {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3FindingSeverity {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
#[doc = "`Identity3FindingSubject`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3FindingSubject {
    pub kind: Identity3FindingSubjectKind,
    pub language: Identity3Text,
    #[serde(rename = "logicalPath")]
    pub logical_path: Identity3LogicalPath,
    #[serde(rename = "qualifiedName")]
    pub qualified_name: Identity3Text,
}
#[doc = "`Identity3FindingSubjectKind`"]
#[derive(
    :: serde :: Deserialize,
    :: serde :: Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd,
)]
pub enum Identity3FindingSubjectKind {
    #[serde(rename = "file")]
    File,
    #[serde(rename = "symbol")]
    Symbol,
    #[serde(rename = "package")]
    Package,
}
impl ::std::fmt::Display for Identity3FindingSubjectKind {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::File => f.write_str("file"),
            Self::Symbol => f.write_str("symbol"),
            Self::Package => f.write_str("package"),
        }
    }
}
impl ::std::str::FromStr for Identity3FindingSubjectKind {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "file" => Ok(Self::File),
            "symbol" => Ok(Self::Symbol),
            "package" => Ok(Self::Package),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Identity3FindingSubjectKind {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3FindingSubjectKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
#[doc = "`Identity3Hash`"]
#[derive(
    :: serde :: Deserialize,
    :: serde :: Serialize,
    Clone,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd,
)]
#[serde(transparent)]
pub struct Identity3Hash(pub ::std::string::String);
impl ::std::ops::Deref for Identity3Hash {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Identity3Hash> for ::std::string::String {
    fn from(value: Identity3Hash) -> Self {
        value.0
    }
}
impl ::std::convert::From<::std::string::String> for Identity3Hash {
    fn from(value: ::std::string::String) -> Self {
        Self(value)
    }
}
impl ::std::fmt::Display for Identity3Hash {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        self.0.fmt(f)
    }
}
impl ::std::str::FromStr for Identity3Hash {
    type Err = ::std::convert::Infallible;
    fn from_str(value: &str) -> ::std::result::Result<Self, Self::Err> {
        Ok(Self(value.to_string()))
    }
}
#[doc = "`Identity3Import`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3Import {
    #[serde(rename = "adapterClosure")]
    pub adapter_closure: ::std::string::String,
    #[doc = "The closed inventory of the import's retained AUXILIARY ASSET members. It is not the import's mandatory custody: the payload bytes and the exact registered schema DOCUMENT bytes are retained and re-hashed independently by registered_payload, and those obligations hold identically when this array is empty. An archive member outside this list is never read (native-evidence section 3 PO-4) - a restriction on READING, satisfied vacuously by an empty list, never a requirement that a member exist. minItems 0 is therefore the owning admissibility: a self-contained normalized payload may legitimately retain no auxiliary asset. An earlier revision of this description required minItems 1, arguing that adapterClosure asserts an adapter ran over the bytes named by the custody record's sourcePath; that argument was withdrawn because ImportedEvidenceRecordV1.sourcePath is a UserInputPath, which the workflow common schema defines as never entering any content identity and recorded in operational records only, and because no join anywhere binds sourcePath to a member of this array. Requiring one arbitrary blob would not establish original-input custody. maxItems 4096 and the item byte bound are the import unit's own published hostile-input bounds (workflows/schemas/imported-evidence.schema.json top-level description: at most 4096 blobs, artifact at most 268435456 bytes); the foundation record previously allowed 100000, and narrowing to the published bound is a stated compatibility change."]
    pub blobs: ::std::vec::Vec<Identity3ImportBlob>,
    #[serde(rename = "buildDigest")]
    pub build_digest: ::std::string::String,
    pub completeness: Identity3ImportCompleteness,
    pub kind: Identity3ImportKind,
    #[serde(rename = "observationDigest")]
    pub observation_digest: ::std::string::String,
    pub omissions: ::std::vec::Vec<Identity3ImportOmissionsItem>,
    #[serde(rename = "payloadDigest")]
    pub payload_digest: ::std::string::String,
    #[serde(rename = "payloadSchemaDigest")]
    pub payload_schema_digest: ::std::string::String,
    #[serde(rename = "producerClosure")]
    pub producer_closure: ::std::string::String,
    #[serde(rename = "schemaVersion")]
    pub schema_version: ExactInteger,
    #[serde(rename = "scopeDigest")]
    pub scope_digest: ::std::string::String,
    #[serde(rename = "sourceCorrespondenceDigest")]
    pub source_correspondence_digest: ::std::string::String,
}
#[doc = "A retained blob row of an import. Identical to Blob except for the import unit's own published hostile-input artifact bound (imported-evidence.schema.json: 'artifact at most 268435456 bytes'), which is an import bound and deliberately not imposed on source-inventory or closure tree rows. Exact mirror of workflows/schemas/common.schema.json#/$defs/Blob."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3ImportBlob {
    pub bytes: i64,
    pub path: Identity3LogicalPath,
    pub sha256: ::std::string::String,
}
#[doc = "`Identity3ImportCompleteness`"]
#[derive(
    :: serde :: Deserialize,
    :: serde :: Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd,
)]
pub enum Identity3ImportCompleteness {
    #[serde(rename = "complete")]
    Complete,
    #[serde(rename = "partial")]
    Partial,
    #[serde(rename = "unknown")]
    Unknown,
}
impl ::std::fmt::Display for Identity3ImportCompleteness {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Complete => f.write_str("complete"),
            Self::Partial => f.write_str("partial"),
            Self::Unknown => f.write_str("unknown"),
        }
    }
}
impl ::std::str::FromStr for Identity3ImportCompleteness {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "complete" => Ok(Self::Complete),
            "partial" => Ok(Self::Partial),
            "unknown" => Ok(Self::Unknown),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Identity3ImportCompleteness {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3ImportCompleteness {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
#[doc = "`Identity3ImportKind`"]
#[derive(
    :: serde :: Deserialize,
    :: serde :: Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd,
)]
pub enum Identity3ImportKind {
    #[serde(rename = "runtime")]
    Runtime,
    #[serde(rename = "test")]
    Test,
    #[serde(rename = "history")]
    History,
    #[serde(rename = "dependency")]
    Dependency,
    #[serde(rename = "prepared")]
    Prepared,
}
impl ::std::fmt::Display for Identity3ImportKind {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Runtime => f.write_str("runtime"),
            Self::Test => f.write_str("test"),
            Self::History => f.write_str("history"),
            Self::Dependency => f.write_str("dependency"),
            Self::Prepared => f.write_str("prepared"),
        }
    }
}
impl ::std::str::FromStr for Identity3ImportKind {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "runtime" => Ok(Self::Runtime),
            "test" => Ok(Self::Test),
            "history" => Ok(Self::History),
            "dependency" => Ok(Self::Dependency),
            "prepared" => Ok(Self::Prepared),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Identity3ImportKind {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3ImportKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
#[doc = "Exact row address within the payload selected by importId. execution selects the TestPayload as a whole; other selectors select subjects[ordinal] or tests[ordinal]. Owner admission checks kind/selector, bounds and explicit Plan/evaluation-input membership. This new descriptor is inline in its witness and is not assigned fragment retention."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3ImportObservationAddress {
    #[serde(rename = "importId")]
    pub import_id: ::std::string::String,
    #[serde(deserialize_with = "::std::option::Option::deserialize")]
    pub ordinal: ::std::option::Option<i64>,
    pub selector: Identity3ImportObservationAddressSelector,
}
#[doc = "`Identity3ImportObservationAddressSelector`"]
#[derive(
    :: serde :: Deserialize,
    :: serde :: Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd,
)]
pub enum Identity3ImportObservationAddressSelector {
    #[serde(rename = "runtime-subject")]
    RuntimeSubject,
    #[serde(rename = "history-subject")]
    HistorySubject,
    #[serde(rename = "test-case")]
    TestCase,
    #[serde(rename = "test-execution")]
    TestExecution,
}
impl ::std::fmt::Display for Identity3ImportObservationAddressSelector {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::RuntimeSubject => f.write_str("runtime-subject"),
            Self::HistorySubject => f.write_str("history-subject"),
            Self::TestCase => f.write_str("test-case"),
            Self::TestExecution => f.write_str("test-execution"),
        }
    }
}
impl ::std::str::FromStr for Identity3ImportObservationAddressSelector {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "runtime-subject" => Ok(Self::RuntimeSubject),
            "history-subject" => Ok(Self::HistorySubject),
            "test-case" => Ok(Self::TestCase),
            "test-execution" => Ok(Self::TestExecution),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Identity3ImportObservationAddressSelector {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3ImportObservationAddressSelector {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
#[doc = "`Identity3ImportOmissionsItem`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Identity3ImportOmissionsItem(::std::string::String);
impl ::std::ops::Deref for Identity3ImportOmissionsItem {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Identity3ImportOmissionsItem> for ::std::string::String {
    fn from(value: Identity3ImportOmissionsItem) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Identity3ImportOmissionsItem {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 4096usize {
            return Err("longer than 4096 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Identity3ImportOmissionsItem {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3ImportOmissionsItem {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Identity3ImportOmissionsItem {
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
#[doc = "The logical-path grammar identity-and-evidence section 3 already states: relative, slash-separated, no empty/dot/dot-dot/NUL/backslash segment, each segment at most 255 characters. THREE DIFFERENT ENFORCEMENTS EXIST AND THEY ARE NOT EQUIVALENT; this description states only where each applies and changes no accepted path set. (1) DIRECT $ref, exactly two fields: #/$defs/Blob/properties/path and #/$defs/import-blob/properties/path. Only these carry the full declarative grammar, INCLUDING the at-most-255-characters-per-segment bound. (2) fact/anchors[]/path: a plain bounded string here, additionally subject to the imperative recursive check in foundation/identity-model.py `ordered()` AND to a real snapshot JOIN - an anchor path must be an inventoried snapshot path, and inventory rows ARE Blob, so the declarative grammar reaches it through that join. (3) finding-fingerprint/subjectKey/logicalPath: a plain bounded string subject to the SAME imperative `ordered()` check and to NO snapshot join. `ordered()` refuses, for any string under a key named `path` or `logicalPath` at any depth, a leading slash, a backslash, a NUL and any empty/dot/dot-dot segment - and it does NOT enforce the per-segment 255 maximum. So (3) is not equivalently constrained to (1), and no snapshot join is claimed for it. The three scope-descriptor path arrays deliberately reference none of this, because `.` alone denotes the admitted project root and this grammar forbids a dot segment. Byte-identical in constraint to workflows/schemas/common.schema.json#/$defs/LogicalPath, which is what makes the import blob rows an exact mirror."]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Identity3LogicalPath(::std::string::String);
impl ::std::ops::Deref for Identity3LogicalPath {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Identity3LogicalPath> for ::std::string::String {
    fn from(value: Identity3LogicalPath) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Identity3LogicalPath {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 4096usize {
            return Err("longer than 4096 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Identity3LogicalPath {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3LogicalPath {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Identity3LogicalPath {
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
#[doc = "The per-level normalization specification map a body-interpreting closure publishes (x-opensip-digest-domains.normalizationSpecificationLaw). Its canonical bytes C(this) are the closure tree member at the law's closureTreePath; each row names the exact retained level-specification bytes for one normalisation level. levels is strictly ascending by the UTF-8 bytes of level, so one map has one spelling."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3NormalizationSpecificationMap {
    #[doc = "Strictly ascending by the UTF-8 bytes of level; enforced at Run closure (BODY_NORMALIZATION_MAP_INVALID)."]
    pub levels: ::std::vec::Vec<Identity3NormalizationSpecificationMapLevelsItem>,
    #[serde(rename = "normalizerId")]
    pub normalizer_id: Identity3Text,
    #[serde(rename = "schemaVersion")]
    pub schema_version: ExactInteger,
}
#[doc = "`Identity3NormalizationSpecificationMapLevelsItem`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3NormalizationSpecificationMapLevelsItem {
    pub level: Identity3NormalizationSpecificationMapLevelsItemLevel,
    #[serde(rename = "specificationDigest")]
    pub specification_digest: ::std::string::String,
}
#[doc = "`Identity3NormalizationSpecificationMapLevelsItemLevel`"]
#[derive(
    :: serde :: Deserialize,
    :: serde :: Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd,
)]
pub enum Identity3NormalizationSpecificationMapLevelsItemLevel {
    #[serde(rename = "L0-verbatim")]
    L0Verbatim,
    #[serde(rename = "L1-lexical")]
    L1Lexical,
    #[serde(rename = "L2-comment-insensitive")]
    L2CommentInsensitive,
    #[serde(rename = "L3-identifier-insensitive")]
    L3IdentifierInsensitive,
}
impl ::std::fmt::Display for Identity3NormalizationSpecificationMapLevelsItemLevel {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::L0Verbatim => f.write_str("L0-verbatim"),
            Self::L1Lexical => f.write_str("L1-lexical"),
            Self::L2CommentInsensitive => f.write_str("L2-comment-insensitive"),
            Self::L3IdentifierInsensitive => f.write_str("L3-identifier-insensitive"),
        }
    }
}
impl ::std::str::FromStr for Identity3NormalizationSpecificationMapLevelsItemLevel {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "L0-verbatim" => Ok(Self::L0Verbatim),
            "L1-lexical" => Ok(Self::L1Lexical),
            "L2-comment-insensitive" => Ok(Self::L2CommentInsensitive),
            "L3-identifier-insensitive" => Ok(Self::L3IdentifierInsensitive),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Identity3NormalizationSpecificationMapLevelsItemLevel {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
    for Identity3NormalizationSpecificationMapLevelsItemLevel
{
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
#[doc = "The closed record digested by semantic-grant.principals[].ownerSourceDigest: the security contract RepoExecutionGrantV2 owner projection, strictly ascending and unique by ownerKey UTF-8 bytes."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(transparent)]
pub struct Identity3OwnerSourceSet(pub ::std::vec::Vec<Identity3OwnerSourceSetItem>);
impl ::std::ops::Deref for Identity3OwnerSourceSet {
    type Target = ::std::vec::Vec<Identity3OwnerSourceSetItem>;
    fn deref(&self) -> &::std::vec::Vec<Identity3OwnerSourceSetItem> {
        &self.0
    }
}
impl ::std::convert::From<Identity3OwnerSourceSet>
    for ::std::vec::Vec<Identity3OwnerSourceSetItem>
{
    fn from(value: Identity3OwnerSourceSet) -> Self {
        value.0
    }
}
impl ::std::convert::From<::std::vec::Vec<Identity3OwnerSourceSetItem>>
    for Identity3OwnerSourceSet
{
    fn from(value: ::std::vec::Vec<Identity3OwnerSourceSetItem>) -> Self {
        Self(value)
    }
}
#[doc = "`Identity3OwnerSourceSetItem`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3OwnerSourceSetItem {
    #[serde(rename = "ownerFileManifestSha256")]
    pub owner_file_manifest_sha256: ::std::string::String,
    #[serde(rename = "ownerKey")]
    pub owner_key: Identity3Text,
    pub source: Identity3Text,
}
#[doc = "`Identity3Plan`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3Plan {
    #[serde(rename = "analysisSpecDigest")]
    pub analysis_spec_digest: ::std::string::String,
    pub budget: Identity3PlanBudget,
    #[serde(rename = "capabilityManifestBytesDigest")]
    pub capability_manifest_bytes_digest: Identity3Hash,
    #[serde(rename = "capabilityManifestId")]
    pub capability_manifest_id: Identity3Hash,
    #[serde(rename = "importIds")]
    pub import_ids: ::std::vec::Vec<::std::string::String>,
    #[serde(rename = "nativeContextDigests")]
    pub native_context_digests: ::std::vec::Vec<::std::string::String>,
    #[serde(rename = "policyDigest")]
    pub policy_digest: ::std::string::String,
    #[serde(rename = "resolvedConfigDigest")]
    pub resolved_config_digest: ::std::string::String,
    #[serde(rename = "schemaVersion")]
    pub schema_version: ExactInteger,
    #[serde(rename = "scopeDigest")]
    pub scope_digest: ::std::string::String,
    #[doc = "Explicit selection with required membership under x-opensip-digest-domains.closureMembership, not an exact minimal set. Extra admissible retained closures may be selected; their selection changes PlanId."]
    #[serde(rename = "semanticClosures")]
    pub semantic_closures: ::std::vec::Vec<::std::string::String>,
    #[serde(rename = "semanticGrantDigest")]
    pub semantic_grant_digest: ::std::string::String,
    #[serde(rename = "snapshotId")]
    pub snapshot_id: ::std::string::String,
    #[serde(rename = "waiverDigest")]
    pub waiver_digest: ::std::string::String,
}
#[doc = "Equal, exactly and by type, to the analysis.budget of the committed resolved semantic configuration this Plan names (identity-and-evidence section 3 closure list). A legitimate override enters the resolved configuration first; neither committed place silently wins."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3PlanBudget {
    pub limit: ::std::num::NonZeroU64,
    pub unit: ::serde_json::Value,
}
#[doc = "`Identity3PolicyDerivation`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3PolicyDerivation {
    #[serde(rename = "planId")]
    pub plan_id: ::std::string::String,
    #[serde(rename = "policyDigest")]
    pub policy_digest: ::std::string::String,
    #[serde(rename = "proofBundleId")]
    pub proof_bundle_id: ::std::string::String,
    #[serde(rename = "schemaVersion")]
    pub schema_version: ExactInteger,
    pub verdict: Identity3PolicyDerivationVerdict,
    #[serde(rename = "waiverDigest")]
    pub waiver_digest: ::std::string::String,
}
#[doc = "`Identity3PolicyDerivationVerdict`"]
#[derive(
    :: serde :: Deserialize,
    :: serde :: Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd,
)]
pub enum Identity3PolicyDerivationVerdict {
    #[serde(rename = "pass")]
    Pass,
    #[serde(rename = "fail")]
    Fail,
    #[serde(rename = "indeterminate")]
    Indeterminate,
}
impl ::std::fmt::Display for Identity3PolicyDerivationVerdict {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Pass => f.write_str("pass"),
            Self::Fail => f.write_str("fail"),
            Self::Indeterminate => f.write_str("indeterminate"),
        }
    }
}
impl ::std::str::FromStr for Identity3PolicyDerivationVerdict {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "pass" => Ok(Self::Pass),
            "fail" => Ok(Self::Fail),
            "indeterminate" => Ok(Self::Indeterminate),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Identity3PolicyDerivationVerdict {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3PolicyDerivationVerdict {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
#[doc = "Version3 witness. No inputRefs field: the complete admitted evaluation input selection is projected onto predicateProofs[].inputRefs (composition §9.2). Native atoms carry native matches/uncertain matches and Coverage; imported atoms carry observation addresses, never fact2; boolean nodes carry children and empty match/Coverage arrays. coverageIds and matching/uncertain sets are consulted evidence and may be narrower than evaluationInputRefs. Exact source-specific plane/operation constraints and complete replay are evaluator admission laws."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3PredicateWitness {
    #[serde(rename = "childPredicateIds")]
    pub child_predicate_ids: ::std::vec::Vec<Identity3Text>,
    #[serde(
        rename = "countLimit",
        deserialize_with = "::std::option::Option::deserialize"
    )]
    pub count_limit: ::std::option::Option<Identity3U64>,
    #[serde(rename = "coverageIds")]
    pub coverage_ids: ::std::vec::Vec<::std::string::String>,
    pub deficiencies: ::std::vec::Vec<Identity3EvaluationDeficiency>,
    pub kind: Identity3PredicateWitnessKind,
    #[serde(rename = "matchingFactIds")]
    pub matching_fact_ids: ::std::vec::Vec<::std::string::String>,
    #[serde(rename = "matchingImportRows")]
    pub matching_import_rows: ::std::vec::Vec<Identity3ImportObservationAddress>,
    #[serde(rename = "programPredicateDigest")]
    pub program_predicate_digest: Identity3Hash,
    #[serde(rename = "schemaVersion")]
    pub schema_version: ExactInteger,
    #[serde(rename = "uncertainFactIds")]
    pub uncertain_fact_ids: ::std::vec::Vec<::std::string::String>,
    #[serde(rename = "uncertainImportRows")]
    pub uncertain_import_rows: ::std::vec::Vec<Identity3ImportObservationAddress>,
}
#[doc = "`Identity3PredicateWitnessKind`"]
#[derive(
    :: serde :: Deserialize,
    :: serde :: Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd,
)]
pub enum Identity3PredicateWitnessKind {
    #[serde(rename = "native-atom")]
    NativeAtom,
    #[serde(rename = "imported-atom")]
    ImportedAtom,
    #[serde(rename = "boolean")]
    Boolean,
}
impl ::std::fmt::Display for Identity3PredicateWitnessKind {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::NativeAtom => f.write_str("native-atom"),
            Self::ImportedAtom => f.write_str("imported-atom"),
            Self::Boolean => f.write_str("boolean"),
        }
    }
}
impl ::std::str::FromStr for Identity3PredicateWitnessKind {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "native-atom" => Ok(Self::NativeAtom),
            "imported-atom" => Ok(Self::ImportedAtom),
            "boolean" => Ok(Self::Boolean),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Identity3PredicateWitnessKind {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3PredicateWitnessKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
#[doc = "The closed record digested by predicate-witness.programPredicateDigest. It addresses ONE predicate node of the admitted RuleProgramV2; it introduces no second policy language. predicateId is the node address: the rule root is \"p\", the i-th operand of an and/or node at address a is a+\".\"+i (zero-based, shortest decimal), and the operand of a not node at address a is a+\".0\"."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3ProgramPredicate {
    #[doc = "raw SHA-256 of the canonical bytes of the exact predicate node the rule program carries at rules[ruleId].emitWhen addressed by predicateId; its op equals operation"]
    #[serde(rename = "nodeDigest")]
    pub node_digest: ::std::string::String,
    pub operation: Identity3ProgramPredicateOperation,
    #[serde(rename = "predicateId")]
    pub predicate_id: Identity3Text,
    #[serde(rename = "ruleId")]
    pub rule_id: Identity3Text,
    #[doc = "equal to the proof bundle ruleProgramDigest this witness belongs to"]
    #[serde(rename = "ruleProgramDigest")]
    pub rule_program_digest: ::std::string::String,
    #[serde(rename = "schemaVersion")]
    pub schema_version: ExactInteger,
}
#[doc = "`Identity3ProgramPredicateOperation`"]
#[derive(
    :: serde :: Deserialize,
    :: serde :: Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd,
)]
pub enum Identity3ProgramPredicateOperation {
    #[serde(rename = "exists")]
    Exists,
    #[serde(rename = "none")]
    None,
    #[serde(rename = "count-at-most")]
    CountAtMost,
    #[serde(rename = "all-covered")]
    AllCovered,
    #[serde(rename = "and")]
    And,
    #[serde(rename = "or")]
    Or,
    #[serde(rename = "not")]
    Not,
}
impl ::std::fmt::Display for Identity3ProgramPredicateOperation {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Exists => f.write_str("exists"),
            Self::None => f.write_str("none"),
            Self::CountAtMost => f.write_str("count-at-most"),
            Self::AllCovered => f.write_str("all-covered"),
            Self::And => f.write_str("and"),
            Self::Or => f.write_str("or"),
            Self::Not => f.write_str("not"),
        }
    }
}
impl ::std::str::FromStr for Identity3ProgramPredicateOperation {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "exists" => Ok(Self::Exists),
            "none" => Ok(Self::None),
            "count-at-most" => Ok(Self::CountAtMost),
            "all-covered" => Ok(Self::AllCovered),
            "and" => Ok(Self::And),
            "or" => Ok(Self::Or),
            "not" => Ok(Self::Not),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Identity3ProgramPredicateOperation {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3ProgramPredicateOperation {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
#[doc = "`Identity3ProjectId`"]
#[derive(
    :: serde :: Deserialize,
    :: serde :: Serialize,
    Clone,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd,
)]
#[serde(transparent)]
pub struct Identity3ProjectId(pub ::std::string::String);
impl ::std::ops::Deref for Identity3ProjectId {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Identity3ProjectId> for ::std::string::String {
    fn from(value: Identity3ProjectId) -> Self {
        value.0
    }
}
impl ::std::convert::From<::std::string::String> for Identity3ProjectId {
    fn from(value: ::std::string::String) -> Self {
        Self(value)
    }
}
impl ::std::fmt::Display for Identity3ProjectId {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        self.0.fmt(f)
    }
}
impl ::std::str::FromStr for Identity3ProjectId {
    type Err = ::std::convert::Infallible;
    fn from_str(value: &str) -> ::std::result::Result<Self, Self::Err> {
        Ok(Self(value.to_string()))
    }
}
#[doc = "Version3 COMPLETE normalized evaluator output. Rule enumerations/results, all predicate proofs/witnesses, full findings and waiver membership, execution deficiencies and sealed verdict are independently recomputed. Count-only comparison is not replay. A deterministic preflight budget refusal is explicit and never an empty successful analysis."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3ProofBundle {
    #[doc = "Complete admitted selection: ExecutionInputsV1.selectedRefs plus the one execution-inputs ref. Not an evaluated subset. Atomic predicateProofs[].inputRefs copy this whole set (composition §9.2)."]
    #[serde(rename = "evaluationInputRefs")]
    pub evaluation_input_refs: ::std::vec::Vec<Identity3ProofInputRef>,
    #[serde(rename = "evaluationState")]
    pub evaluation_state: Identity3ProofBundleEvaluationState,
    #[serde(rename = "evaluatorClosure")]
    pub evaluator_closure: ::std::string::String,
    #[doc = "Required-execution assessment items even when all rules are disabled, plus work-budget-exhausted. source=execution is the assessment layer. cause is row.deficiency if it is an execution-registry member, else required-cell-unsatisfied for null/source-syntax-invalid. inputRefs are the ExecutionInputsV1 ref plus originating Coverage/inventory/candidate refs. subjectId and predicateId are null. composition §9.6. Internal requiredCellDeficiencies tokens native-work-incomplete/unsupported-typed are not proof causes."]
    #[serde(rename = "executionDeficiencies")]
    pub execution_deficiencies: ::std::vec::Vec<Identity3EvaluationDeficiency>,
    #[serde(rename = "executionInputsDigest")]
    pub execution_inputs_digest: ::std::string::String,
    #[serde(rename = "executionPlanId")]
    pub execution_plan_id: ::std::string::String,
    #[serde(rename = "findingIds")]
    pub finding_ids: ::std::vec::Vec<::std::string::String>,
    #[serde(rename = "planId")]
    pub plan_id: ::std::string::String,
    #[serde(rename = "predicateProofs")]
    pub predicate_proofs: ::std::vec::Vec<Identity3ProofBundlePredicateProofsItem>,
    #[serde(rename = "ruleProgramDigest")]
    pub rule_program_digest: ::std::string::String,
    #[serde(rename = "ruleResults")]
    pub rule_results: ::std::vec::Vec<Identity3RuleResult>,
    #[serde(rename = "schemaVersion")]
    pub schema_version: ExactInteger,
    pub verdict: Identity3ProofBundleVerdict,
    #[serde(rename = "waivedFindingIds")]
    pub waived_finding_ids: ::std::vec::Vec<::std::string::String>,
}
#[doc = "`Identity3ProofBundleEvaluationState`"]
#[derive(
    :: serde :: Deserialize,
    :: serde :: Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd,
)]
pub enum Identity3ProofBundleEvaluationState {
    #[serde(rename = "evaluated")]
    Evaluated,
    #[serde(rename = "budget-exhausted")]
    BudgetExhausted,
}
impl ::std::fmt::Display for Identity3ProofBundleEvaluationState {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Evaluated => f.write_str("evaluated"),
            Self::BudgetExhausted => f.write_str("budget-exhausted"),
        }
    }
}
impl ::std::str::FromStr for Identity3ProofBundleEvaluationState {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "evaluated" => Ok(Self::Evaluated),
            "budget-exhausted" => Ok(Self::BudgetExhausted),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Identity3ProofBundleEvaluationState {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3ProofBundleEvaluationState {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
#[doc = "`Identity3ProofBundlePredicateProofsItem`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3ProofBundlePredicateProofsItem {
    #[doc = "Atomic: equal to proof.evaluationInputRefs (whole admitted selection, including empty-population inputs). Boolean: canonical union of immediate children. Projection of the witness-binding sentence; witnesses have no inputRefs field. Not the atom internal consumed-ref subset. composition §9.2."]
    #[serde(rename = "inputRefs")]
    pub input_refs: ::std::vec::Vec<Identity3ProofInputRef>,
    pub operation: Identity3ProofBundlePredicateProofsItemOperation,
    #[serde(rename = "predicateId")]
    pub predicate_id: Identity3ProofBundlePredicateProofsItemPredicateId,
    #[serde(rename = "ruleId")]
    pub rule_id: Identity3ProofBundlePredicateProofsItemRuleId,
    #[serde(rename = "scopeIds")]
    pub scope_ids: ::std::vec::Vec<::std::string::String>,
    #[serde(rename = "subjectId")]
    pub subject_id: ::std::string::String,
    pub value: Identity3ProofBundlePredicateProofsItemValue,
    #[serde(rename = "witnessDigest")]
    pub witness_digest: ::std::string::String,
}
#[doc = "`Identity3ProofBundlePredicateProofsItemOperation`"]
#[derive(
    :: serde :: Deserialize,
    :: serde :: Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd,
)]
pub enum Identity3ProofBundlePredicateProofsItemOperation {
    #[serde(rename = "exists")]
    Exists,
    #[serde(rename = "none")]
    None,
    #[serde(rename = "count-at-most")]
    CountAtMost,
    #[serde(rename = "all-covered")]
    AllCovered,
    #[serde(rename = "and")]
    And,
    #[serde(rename = "or")]
    Or,
    #[serde(rename = "not")]
    Not,
}
impl ::std::fmt::Display for Identity3ProofBundlePredicateProofsItemOperation {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Exists => f.write_str("exists"),
            Self::None => f.write_str("none"),
            Self::CountAtMost => f.write_str("count-at-most"),
            Self::AllCovered => f.write_str("all-covered"),
            Self::And => f.write_str("and"),
            Self::Or => f.write_str("or"),
            Self::Not => f.write_str("not"),
        }
    }
}
impl ::std::str::FromStr for Identity3ProofBundlePredicateProofsItemOperation {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "exists" => Ok(Self::Exists),
            "none" => Ok(Self::None),
            "count-at-most" => Ok(Self::CountAtMost),
            "all-covered" => Ok(Self::AllCovered),
            "and" => Ok(Self::And),
            "or" => Ok(Self::Or),
            "not" => Ok(Self::Not),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Identity3ProofBundlePredicateProofsItemOperation {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
    for Identity3ProofBundlePredicateProofsItemOperation
{
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
#[doc = "`Identity3ProofBundlePredicateProofsItemPredicateId`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Identity3ProofBundlePredicateProofsItemPredicateId(::std::string::String);
impl ::std::ops::Deref for Identity3ProofBundlePredicateProofsItemPredicateId {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Identity3ProofBundlePredicateProofsItemPredicateId>
    for ::std::string::String
{
    fn from(value: Identity3ProofBundlePredicateProofsItemPredicateId) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Identity3ProofBundlePredicateProofsItemPredicateId {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 4096usize {
            return Err("longer than 4096 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Identity3ProofBundlePredicateProofsItemPredicateId {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
    for Identity3ProofBundlePredicateProofsItemPredicateId
{
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Identity3ProofBundlePredicateProofsItemPredicateId {
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
#[doc = "`Identity3ProofBundlePredicateProofsItemRuleId`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Identity3ProofBundlePredicateProofsItemRuleId(::std::string::String);
impl ::std::ops::Deref for Identity3ProofBundlePredicateProofsItemRuleId {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Identity3ProofBundlePredicateProofsItemRuleId> for ::std::string::String {
    fn from(value: Identity3ProofBundlePredicateProofsItemRuleId) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Identity3ProofBundlePredicateProofsItemRuleId {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 4096usize {
            return Err("longer than 4096 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Identity3ProofBundlePredicateProofsItemRuleId {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
    for Identity3ProofBundlePredicateProofsItemRuleId
{
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Identity3ProofBundlePredicateProofsItemRuleId {
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
#[doc = "`Identity3ProofBundlePredicateProofsItemValue`"]
#[derive(
    :: serde :: Deserialize,
    :: serde :: Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd,
)]
pub enum Identity3ProofBundlePredicateProofsItemValue {
    #[serde(rename = "true")]
    True,
    #[serde(rename = "false")]
    False,
    #[serde(rename = "indeterminate")]
    Indeterminate,
}
impl ::std::fmt::Display for Identity3ProofBundlePredicateProofsItemValue {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::True => f.write_str("true"),
            Self::False => f.write_str("false"),
            Self::Indeterminate => f.write_str("indeterminate"),
        }
    }
}
impl ::std::str::FromStr for Identity3ProofBundlePredicateProofsItemValue {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "true" => Ok(Self::True),
            "false" => Ok(Self::False),
            "indeterminate" => Ok(Self::Indeterminate),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Identity3ProofBundlePredicateProofsItemValue {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
    for Identity3ProofBundlePredicateProofsItemValue
{
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
#[doc = "`Identity3ProofBundleVerdict`"]
#[derive(
    :: serde :: Deserialize,
    :: serde :: Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd,
)]
pub enum Identity3ProofBundleVerdict {
    #[serde(rename = "pass")]
    Pass,
    #[serde(rename = "fail")]
    Fail,
    #[serde(rename = "indeterminate")]
    Indeterminate,
}
impl ::std::fmt::Display for Identity3ProofBundleVerdict {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Pass => f.write_str("pass"),
            Self::Fail => f.write_str("fail"),
            Self::Indeterminate => f.write_str("indeterminate"),
        }
    }
}
impl ::std::str::FromStr for Identity3ProofBundleVerdict {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "pass" => Ok(Self::Pass),
            "fail" => Ok(Self::Fail),
            "indeterminate" => Ok(Self::Indeterminate),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Identity3ProofBundleVerdict {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3ProofBundleVerdict {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
#[doc = "`Identity3ProofInputRef`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3ProofInputRef {
    pub digest: ::std::string::String,
    pub domain: Identity3ProofInputRefDomain,
}
#[doc = "`Identity3ProofInputRefDomain`"]
#[derive(
    :: serde :: Deserialize,
    :: serde :: Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd,
)]
pub enum Identity3ProofInputRefDomain {
    #[serde(rename = "view")]
    View,
    #[serde(rename = "import")]
    Import,
    #[serde(rename = "coverage")]
    Coverage,
    #[serde(rename = "rule-program")]
    RuleProgram,
    #[serde(rename = "policy")]
    Policy,
    #[serde(rename = "waiver")]
    Waiver,
    #[serde(rename = "schema")]
    Schema,
    #[serde(rename = "blob")]
    Blob,
    #[serde(rename = "configuration")]
    Configuration,
    #[serde(rename = "native-context")]
    NativeContext,
    #[serde(rename = "analysis-spec")]
    AnalysisSpec,
    #[serde(rename = "capability-manifest")]
    CapabilityManifest,
    #[serde(rename = "enumeration-plan")]
    EnumerationPlan,
    #[serde(rename = "subject-inventory")]
    SubjectInventory,
    #[serde(rename = "evaluator-emission-plan")]
    EvaluatorEmissionPlan,
    #[serde(rename = "target-attribution")]
    TargetAttribution,
    #[serde(rename = "incoming-search")]
    IncomingSearch,
    #[serde(rename = "execution-inputs")]
    ExecutionInputs,
    #[serde(rename = "candidate-producer-result")]
    CandidateProducerResult,
}
impl ::std::fmt::Display for Identity3ProofInputRefDomain {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::View => f.write_str("view"),
            Self::Import => f.write_str("import"),
            Self::Coverage => f.write_str("coverage"),
            Self::RuleProgram => f.write_str("rule-program"),
            Self::Policy => f.write_str("policy"),
            Self::Waiver => f.write_str("waiver"),
            Self::Schema => f.write_str("schema"),
            Self::Blob => f.write_str("blob"),
            Self::Configuration => f.write_str("configuration"),
            Self::NativeContext => f.write_str("native-context"),
            Self::AnalysisSpec => f.write_str("analysis-spec"),
            Self::CapabilityManifest => f.write_str("capability-manifest"),
            Self::EnumerationPlan => f.write_str("enumeration-plan"),
            Self::SubjectInventory => f.write_str("subject-inventory"),
            Self::EvaluatorEmissionPlan => f.write_str("evaluator-emission-plan"),
            Self::TargetAttribution => f.write_str("target-attribution"),
            Self::IncomingSearch => f.write_str("incoming-search"),
            Self::ExecutionInputs => f.write_str("execution-inputs"),
            Self::CandidateProducerResult => f.write_str("candidate-producer-result"),
        }
    }
}
impl ::std::str::FromStr for Identity3ProofInputRefDomain {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "view" => Ok(Self::View),
            "import" => Ok(Self::Import),
            "coverage" => Ok(Self::Coverage),
            "rule-program" => Ok(Self::RuleProgram),
            "policy" => Ok(Self::Policy),
            "waiver" => Ok(Self::Waiver),
            "schema" => Ok(Self::Schema),
            "blob" => Ok(Self::Blob),
            "configuration" => Ok(Self::Configuration),
            "native-context" => Ok(Self::NativeContext),
            "analysis-spec" => Ok(Self::AnalysisSpec),
            "capability-manifest" => Ok(Self::CapabilityManifest),
            "enumeration-plan" => Ok(Self::EnumerationPlan),
            "subject-inventory" => Ok(Self::SubjectInventory),
            "evaluator-emission-plan" => Ok(Self::EvaluatorEmissionPlan),
            "target-attribution" => Ok(Self::TargetAttribution),
            "incoming-search" => Ok(Self::IncomingSearch),
            "execution-inputs" => Ok(Self::ExecutionInputs),
            "candidate-producer-result" => Ok(Self::CandidateProducerResult),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Identity3ProofInputRefDomain {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3ProofInputRefDomain {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
#[doc = "`Identity3Ref`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3Ref {
    pub digest: ::std::string::String,
    pub domain: Identity3RefDomain,
}
#[doc = "`Identity3RefDomain`"]
#[derive(
    :: serde :: Deserialize,
    :: serde :: Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd,
)]
pub enum Identity3RefDomain {
    #[serde(rename = "analysis-spec")]
    AnalysisSpec,
    #[serde(rename = "blob")]
    Blob,
    #[serde(rename = "cache-key")]
    CacheKey,
    #[serde(rename = "capability-manifest")]
    CapabilityManifest,
    #[serde(rename = "closure")]
    Closure,
    #[serde(rename = "configuration")]
    Configuration,
    #[serde(rename = "coverage")]
    Coverage,
    #[serde(rename = "coverage-payload")]
    CoveragePayload,
    #[serde(rename = "enumeration-plan")]
    EnumerationPlan,
    #[serde(rename = "evaluation-seal")]
    EvaluationSeal,
    #[serde(rename = "evaluation-subject")]
    EvaluationSubject,
    #[serde(rename = "evaluator-emission-plan")]
    EvaluatorEmissionPlan,
    #[serde(rename = "execution-plan")]
    ExecutionPlan,
    #[serde(rename = "fact")]
    Fact,
    #[serde(rename = "fact-payload")]
    FactPayload,
    #[serde(rename = "finding")]
    Finding,
    #[serde(rename = "finding-fingerprint")]
    FindingFingerprint,
    #[serde(rename = "finding-parameters")]
    FindingParameters,
    #[serde(rename = "import")]
    Import,
    #[serde(rename = "import-payload")]
    ImportPayload,
    #[serde(rename = "native-context")]
    NativeContext,
    #[serde(rename = "plan")]
    Plan,
    #[serde(rename = "policy")]
    Policy,
    #[serde(rename = "policy-derivation")]
    PolicyDerivation,
    #[serde(rename = "predicate-witness")]
    PredicateWitness,
    #[serde(rename = "proof-bundle")]
    ProofBundle,
    #[serde(rename = "regeneration-key")]
    RegenerationKey,
    #[serde(rename = "rule-program")]
    RuleProgram,
    #[serde(rename = "run")]
    Run,
    #[serde(rename = "schema")]
    Schema,
    #[serde(rename = "semantic-evidence")]
    SemanticEvidence,
    #[serde(rename = "snapshot")]
    Snapshot,
    #[serde(rename = "subject-inventory")]
    SubjectInventory,
    #[serde(rename = "subject-scope")]
    SubjectScope,
    #[serde(rename = "target-attribution")]
    TargetAttribution,
    #[serde(rename = "view")]
    View,
    #[serde(rename = "waiver")]
    Waiver,
    #[serde(rename = "incoming-search")]
    IncomingSearch,
    #[serde(rename = "execution-inputs")]
    ExecutionInputs,
    #[serde(rename = "candidate-producer-result")]
    CandidateProducerResult,
}
impl ::std::fmt::Display for Identity3RefDomain {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::AnalysisSpec => f.write_str("analysis-spec"),
            Self::Blob => f.write_str("blob"),
            Self::CacheKey => f.write_str("cache-key"),
            Self::CapabilityManifest => f.write_str("capability-manifest"),
            Self::Closure => f.write_str("closure"),
            Self::Configuration => f.write_str("configuration"),
            Self::Coverage => f.write_str("coverage"),
            Self::CoveragePayload => f.write_str("coverage-payload"),
            Self::EnumerationPlan => f.write_str("enumeration-plan"),
            Self::EvaluationSeal => f.write_str("evaluation-seal"),
            Self::EvaluationSubject => f.write_str("evaluation-subject"),
            Self::EvaluatorEmissionPlan => f.write_str("evaluator-emission-plan"),
            Self::ExecutionPlan => f.write_str("execution-plan"),
            Self::Fact => f.write_str("fact"),
            Self::FactPayload => f.write_str("fact-payload"),
            Self::Finding => f.write_str("finding"),
            Self::FindingFingerprint => f.write_str("finding-fingerprint"),
            Self::FindingParameters => f.write_str("finding-parameters"),
            Self::Import => f.write_str("import"),
            Self::ImportPayload => f.write_str("import-payload"),
            Self::NativeContext => f.write_str("native-context"),
            Self::Plan => f.write_str("plan"),
            Self::Policy => f.write_str("policy"),
            Self::PolicyDerivation => f.write_str("policy-derivation"),
            Self::PredicateWitness => f.write_str("predicate-witness"),
            Self::ProofBundle => f.write_str("proof-bundle"),
            Self::RegenerationKey => f.write_str("regeneration-key"),
            Self::RuleProgram => f.write_str("rule-program"),
            Self::Run => f.write_str("run"),
            Self::Schema => f.write_str("schema"),
            Self::SemanticEvidence => f.write_str("semantic-evidence"),
            Self::Snapshot => f.write_str("snapshot"),
            Self::SubjectInventory => f.write_str("subject-inventory"),
            Self::SubjectScope => f.write_str("subject-scope"),
            Self::TargetAttribution => f.write_str("target-attribution"),
            Self::View => f.write_str("view"),
            Self::Waiver => f.write_str("waiver"),
            Self::IncomingSearch => f.write_str("incoming-search"),
            Self::ExecutionInputs => f.write_str("execution-inputs"),
            Self::CandidateProducerResult => f.write_str("candidate-producer-result"),
        }
    }
}
impl ::std::str::FromStr for Identity3RefDomain {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "analysis-spec" => Ok(Self::AnalysisSpec),
            "blob" => Ok(Self::Blob),
            "cache-key" => Ok(Self::CacheKey),
            "capability-manifest" => Ok(Self::CapabilityManifest),
            "closure" => Ok(Self::Closure),
            "configuration" => Ok(Self::Configuration),
            "coverage" => Ok(Self::Coverage),
            "coverage-payload" => Ok(Self::CoveragePayload),
            "enumeration-plan" => Ok(Self::EnumerationPlan),
            "evaluation-seal" => Ok(Self::EvaluationSeal),
            "evaluation-subject" => Ok(Self::EvaluationSubject),
            "evaluator-emission-plan" => Ok(Self::EvaluatorEmissionPlan),
            "execution-plan" => Ok(Self::ExecutionPlan),
            "fact" => Ok(Self::Fact),
            "fact-payload" => Ok(Self::FactPayload),
            "finding" => Ok(Self::Finding),
            "finding-fingerprint" => Ok(Self::FindingFingerprint),
            "finding-parameters" => Ok(Self::FindingParameters),
            "import" => Ok(Self::Import),
            "import-payload" => Ok(Self::ImportPayload),
            "native-context" => Ok(Self::NativeContext),
            "plan" => Ok(Self::Plan),
            "policy" => Ok(Self::Policy),
            "policy-derivation" => Ok(Self::PolicyDerivation),
            "predicate-witness" => Ok(Self::PredicateWitness),
            "proof-bundle" => Ok(Self::ProofBundle),
            "regeneration-key" => Ok(Self::RegenerationKey),
            "rule-program" => Ok(Self::RuleProgram),
            "run" => Ok(Self::Run),
            "schema" => Ok(Self::Schema),
            "semantic-evidence" => Ok(Self::SemanticEvidence),
            "snapshot" => Ok(Self::Snapshot),
            "subject-inventory" => Ok(Self::SubjectInventory),
            "subject-scope" => Ok(Self::SubjectScope),
            "target-attribution" => Ok(Self::TargetAttribution),
            "view" => Ok(Self::View),
            "waiver" => Ok(Self::Waiver),
            "incoming-search" => Ok(Self::IncomingSearch),
            "execution-inputs" => Ok(Self::ExecutionInputs),
            "candidate-producer-result" => Ok(Self::CandidateProducerResult),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Identity3RefDomain {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3RefDomain {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
#[doc = "`Identity3RegenerationKey`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(transparent)]
pub struct Identity3RegenerationKey(pub Identity3CacheKey);
impl ::std::ops::Deref for Identity3RegenerationKey {
    type Target = Identity3CacheKey;
    fn deref(&self) -> &Identity3CacheKey {
        &self.0
    }
}
impl ::std::convert::From<Identity3RegenerationKey> for Identity3CacheKey {
    fn from(value: Identity3RegenerationKey) -> Self {
        value.0
    }
}
impl ::std::convert::From<Identity3CacheKey> for Identity3RegenerationKey {
    fn from(value: Identity3CacheKey) -> Self {
        Self(value)
    }
}
#[doc = "`Identity3Root`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(transparent)]
pub struct Identity3Root(pub ::serde_json::Value);
impl ::std::ops::Deref for Identity3Root {
    type Target = ::serde_json::Value;
    fn deref(&self) -> &::serde_json::Value {
        &self.0
    }
}
impl ::std::convert::From<Identity3Root> for ::serde_json::Value {
    fn from(value: Identity3Root) -> Self {
        value.0
    }
}
impl ::std::convert::From<::serde_json::Value> for Identity3Root {
    fn from(value: ::serde_json::Value) -> Self {
        Self(value)
    }
}
#[doc = "Retained OUTPUT recomputed from Plan-bound expected inventories and rule selection. Incomplete includes unavailable and partial population or unknown export membership. Complete-empty is explicit. Disabled is all arrays empty. Inventory refs include all relevant expected outcomes, including unavailable records; unseen population never gets a fabricated subject id."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3RuleEnumeration {
    #[serde(rename = "incompleteInventoryRefs")]
    pub incomplete_inventory_refs: ::std::vec::Vec<Identity3SubjectInventoryRef>,
    #[serde(rename = "inventoryRefs")]
    pub inventory_refs: ::std::vec::Vec<Identity3SubjectInventoryRef>,
    #[serde(rename = "selectedSubjectIds")]
    pub selected_subject_ids: ::std::vec::Vec<::std::string::String>,
    pub state: Identity3RuleEnumerationState,
    #[serde(rename = "unresolvedSubjectIds")]
    pub unresolved_subject_ids: ::std::vec::Vec<::std::string::String>,
}
#[doc = "`Identity3RuleEnumerationState`"]
#[derive(
    :: serde :: Deserialize,
    :: serde :: Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd,
)]
pub enum Identity3RuleEnumerationState {
    #[serde(rename = "disabled")]
    Disabled,
    #[serde(rename = "complete")]
    Complete,
    #[serde(rename = "incomplete")]
    Incomplete,
}
impl ::std::fmt::Display for Identity3RuleEnumerationState {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Disabled => f.write_str("disabled"),
            Self::Complete => f.write_str("complete"),
            Self::Incomplete => f.write_str("incomplete"),
        }
    }
}
impl ::std::str::FromStr for Identity3RuleEnumerationState {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "disabled" => Ok(Self::Disabled),
            "complete" => Ok(Self::Complete),
            "incomplete" => Ok(Self::Incomplete),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Identity3RuleEnumerationState {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3RuleEnumerationState {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
#[doc = "One result for EVERY compiled policy rule, including disabled and zero-subject rules, strictly sorted by ruleId. Outcome is recomputed after explicit waiver resolution and effective gate selection; advisory matches remain findings with pass sealed rule outcome. Enumeration uncertainty survives waived known findings."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3RuleResult {
    pub deficiencies: ::std::vec::Vec<Identity3EvaluationDeficiency>,
    pub enumeration: Identity3RuleEnumeration,
    #[serde(rename = "findingIds")]
    pub finding_ids: ::std::vec::Vec<::std::string::String>,
    pub outcome: Identity3RuleResultOutcome,
    #[serde(rename = "ruleId")]
    pub rule_id: Identity3Text,
}
#[doc = "`Identity3RuleResultOutcome`"]
#[derive(
    :: serde :: Deserialize,
    :: serde :: Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd,
)]
pub enum Identity3RuleResultOutcome {
    #[serde(rename = "disabled")]
    Disabled,
    #[serde(rename = "pass")]
    Pass,
    #[serde(rename = "fail")]
    Fail,
    #[serde(rename = "indeterminate")]
    Indeterminate,
}
impl ::std::fmt::Display for Identity3RuleResultOutcome {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Disabled => f.write_str("disabled"),
            Self::Pass => f.write_str("pass"),
            Self::Fail => f.write_str("fail"),
            Self::Indeterminate => f.write_str("indeterminate"),
        }
    }
}
impl ::std::str::FromStr for Identity3RuleResultOutcome {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "disabled" => Ok(Self::Disabled),
            "pass" => Ok(Self::Pass),
            "fail" => Ok(Self::Fail),
            "indeterminate" => Ok(Self::Indeterminate),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Identity3RuleResultOutcome {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3RuleResultOutcome {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
#[doc = "`Identity3Run`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3Run {
    #[serde(rename = "capabilityManifestId")]
    pub capability_manifest_id: Identity3Hash,
    #[serde(rename = "evaluationSealId")]
    pub evaluation_seal_id: ::std::string::String,
    #[serde(rename = "evidenceId")]
    pub evidence_id: ::std::string::String,
    #[serde(rename = "planId")]
    pub plan_id: ::std::string::String,
    #[serde(rename = "projectId")]
    pub project_id: Identity3ProjectId,
    #[serde(rename = "schemaVersion")]
    pub schema_version: ExactInteger,
    #[serde(rename = "snapshotId")]
    pub snapshot_id: ::std::string::String,
}
#[doc = "`Identity3ScopeDescriptor`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3ScopeDescriptor {
    #[serde(rename = "excludedPathPrefixes")]
    pub excluded_path_prefixes: ::std::vec::Vec<Identity3Text>,
    #[serde(rename = "pathPrefixes")]
    pub path_prefixes: ::std::vec::Vec<Identity3Text>,
    #[serde(rename = "schemaVersion")]
    pub schema_version: ExactInteger,
    #[serde(rename = "workspaceRoots")]
    pub workspace_roots: ::std::vec::Vec<Identity3Text>,
}
#[doc = "`Identity3SemanticConfiguration`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3SemanticConfiguration {
    pub analysis: Identity3SemanticConfigurationAnalysis,
    pub components: Identity3SemanticConfigurationComponents,
    pub discovery: Identity3SemanticConfigurationDiscovery,
    pub evidence: Identity3SemanticConfigurationEvidence,
    pub policy: Identity3SemanticConfigurationPolicy,
}
#[doc = "`Identity3SemanticConfigurationAnalysis`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3SemanticConfigurationAnalysis {
    pub budget: Identity3SemanticConfigurationAnalysisBudget,
    pub capabilities: ::std::vec::Vec<Identity3SemanticConfigurationAnalysisCapabilitiesItem>,
    #[serde(rename = "profileId")]
    pub profile_id: Identity3SemanticConfigurationAnalysisProfileId,
}
#[doc = "The deterministic analysis budget. identity-and-evidence section 3 requires plan.budget to equal this value exactly and by type; an override is made here first so both committed places agree."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3SemanticConfigurationAnalysisBudget {
    pub limit: ::std::num::NonZeroU64,
    pub unit: ::serde_json::Value,
}
#[doc = "`Identity3SemanticConfigurationAnalysisCapabilitiesItem`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Identity3SemanticConfigurationAnalysisCapabilitiesItem(::std::string::String);
impl ::std::ops::Deref for Identity3SemanticConfigurationAnalysisCapabilitiesItem {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Identity3SemanticConfigurationAnalysisCapabilitiesItem>
    for ::std::string::String
{
    fn from(value: Identity3SemanticConfigurationAnalysisCapabilitiesItem) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Identity3SemanticConfigurationAnalysisCapabilitiesItem {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 128usize {
            return Err("longer than 128 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Identity3SemanticConfigurationAnalysisCapabilitiesItem {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
    for Identity3SemanticConfigurationAnalysisCapabilitiesItem
{
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Identity3SemanticConfigurationAnalysisCapabilitiesItem {
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
#[doc = "`Identity3SemanticConfigurationAnalysisProfileId`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Identity3SemanticConfigurationAnalysisProfileId(::std::string::String);
impl ::std::ops::Deref for Identity3SemanticConfigurationAnalysisProfileId {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Identity3SemanticConfigurationAnalysisProfileId>
    for ::std::string::String
{
    fn from(value: Identity3SemanticConfigurationAnalysisProfileId) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Identity3SemanticConfigurationAnalysisProfileId {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 128usize {
            return Err("longer than 128 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Identity3SemanticConfigurationAnalysisProfileId {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
    for Identity3SemanticConfigurationAnalysisProfileId
{
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Identity3SemanticConfigurationAnalysisProfileId {
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
#[doc = "`Identity3SemanticConfigurationComponents`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug, Default)]
#[serde(deny_unknown_fields)]
pub struct Identity3SemanticConfigurationComponents {
    #[serde(
        rename = "allowedScopes",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub allowed_scopes:
        FieldPresence<::std::option::Option<Identity3SemanticConfigurationComponentsAllowedScopes>>,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub holds: FieldPresence<
        ::std::option::Option<::std::vec::Vec<Identity3SemanticConfigurationComponentsHoldsItem>>,
    >,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub pins: FieldPresence<
        ::std::option::Option<::std::vec::Vec<Identity3SemanticConfigurationComponentsPinsItem>>,
    >,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub request:
        FieldPresence<::std::vec::Vec<Identity3SemanticConfigurationComponentsRequestItem>>,
}
#[doc = "`Identity3SemanticConfigurationComponentsAllowedScopes`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(untagged)]
pub enum Identity3SemanticConfigurationComponentsAllowedScopes {
    Variant0(::serde_json::Value),
    Variant1(::serde_json::Value),
}
#[doc = "`Identity3SemanticConfigurationComponentsHoldsItem`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3SemanticConfigurationComponentsHoldsItem {
    #[serde(rename = "stableId")]
    pub stable_id: ::std::string::String,
    pub version: ::std::string::String,
}
#[doc = "`Identity3SemanticConfigurationComponentsPinsItem`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3SemanticConfigurationComponentsPinsItem {
    #[serde(rename = "stableId")]
    pub stable_id: ::std::string::String,
    pub version: ::std::string::String,
}
#[doc = "`Identity3SemanticConfigurationComponentsRequestItem`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(untagged, deny_unknown_fields)]
pub enum Identity3SemanticConfigurationComponentsRequestItem {
    Variant0 {
        #[serde(rename = "stableId")]
        stable_id: ::std::string::String,
        version: ::std::string::String,
    },
    Variant1 {
        #[serde(rename = "stableId")]
        stable_id: ::std::string::String,
        #[serde(rename = "versionConstraint")]
        version_constraint:
            Identity3SemanticConfigurationComponentsRequestItemVariant1VersionConstraint,
    },
}
#[doc = "`Identity3SemanticConfigurationComponentsRequestItemVariant1VersionConstraint`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(untagged, deny_unknown_fields)]
pub enum Identity3SemanticConfigurationComponentsRequestItemVariant1VersionConstraint {
    String(::std::string::String),
    Object {
        #[serde(rename = "includeMax")]
        include_max: bool,
        #[serde(rename = "includeMin")]
        include_min: bool,
        max: ::std::string::String,
        min: ::std::string::String,
    },
}
#[doc = "`Identity3SemanticConfigurationDiscovery`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug, Default)]
#[serde(deny_unknown_fields)]
pub struct Identity3SemanticConfigurationDiscovery {
    #[serde(
        rename = "entryPoints",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub entry_points: FieldPresence<
        ::std::option::Option<
            ::std::vec::Vec<Identity3SemanticConfigurationDiscoveryEntryPointsItem>,
        >,
    >,
    #[serde(
        rename = "ignorePaths",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub ignore_paths: FieldPresence<
        ::std::option::Option<
            ::std::vec::Vec<Identity3SemanticConfigurationDiscoveryIgnorePathsItem>,
        >,
    >,
    #[serde(
        rename = "workspaceRoots",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub workspace_roots: FieldPresence<
        ::std::option::Option<
            ::std::vec::Vec<Identity3SemanticConfigurationDiscoveryWorkspaceRootsItem>,
        >,
    >,
}
#[doc = "`Identity3SemanticConfigurationDiscoveryEntryPointsItem`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Identity3SemanticConfigurationDiscoveryEntryPointsItem(::std::string::String);
impl ::std::ops::Deref for Identity3SemanticConfigurationDiscoveryEntryPointsItem {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Identity3SemanticConfigurationDiscoveryEntryPointsItem>
    for ::std::string::String
{
    fn from(value: Identity3SemanticConfigurationDiscoveryEntryPointsItem) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Identity3SemanticConfigurationDiscoveryEntryPointsItem {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 4096usize {
            return Err("longer than 4096 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Identity3SemanticConfigurationDiscoveryEntryPointsItem {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
    for Identity3SemanticConfigurationDiscoveryEntryPointsItem
{
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Identity3SemanticConfigurationDiscoveryEntryPointsItem {
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
#[doc = "`Identity3SemanticConfigurationDiscoveryIgnorePathsItem`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Identity3SemanticConfigurationDiscoveryIgnorePathsItem(::std::string::String);
impl ::std::ops::Deref for Identity3SemanticConfigurationDiscoveryIgnorePathsItem {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Identity3SemanticConfigurationDiscoveryIgnorePathsItem>
    for ::std::string::String
{
    fn from(value: Identity3SemanticConfigurationDiscoveryIgnorePathsItem) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Identity3SemanticConfigurationDiscoveryIgnorePathsItem {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 4096usize {
            return Err("longer than 4096 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Identity3SemanticConfigurationDiscoveryIgnorePathsItem {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
    for Identity3SemanticConfigurationDiscoveryIgnorePathsItem
{
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Identity3SemanticConfigurationDiscoveryIgnorePathsItem {
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
#[doc = "`Identity3SemanticConfigurationDiscoveryWorkspaceRootsItem`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Identity3SemanticConfigurationDiscoveryWorkspaceRootsItem(::std::string::String);
impl ::std::ops::Deref for Identity3SemanticConfigurationDiscoveryWorkspaceRootsItem {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Identity3SemanticConfigurationDiscoveryWorkspaceRootsItem>
    for ::std::string::String
{
    fn from(value: Identity3SemanticConfigurationDiscoveryWorkspaceRootsItem) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Identity3SemanticConfigurationDiscoveryWorkspaceRootsItem {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 4096usize {
            return Err("longer than 4096 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Identity3SemanticConfigurationDiscoveryWorkspaceRootsItem {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
    for Identity3SemanticConfigurationDiscoveryWorkspaceRootsItem
{
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Identity3SemanticConfigurationDiscoveryWorkspaceRootsItem {
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
#[doc = "`Identity3SemanticConfigurationEvidence`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug, Default)]
#[serde(deny_unknown_fields)]
pub struct Identity3SemanticConfigurationEvidence {
    #[serde(
        rename = "importIds",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub import_ids: FieldPresence<::std::option::Option<::std::vec::Vec<::std::string::String>>>,
}
#[doc = "`Identity3SemanticConfigurationPolicy`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug, Default)]
#[serde(deny_unknown_fields)]
pub struct Identity3SemanticConfigurationPolicy {
    #[serde(
        rename = "packIds",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub pack_ids: FieldPresence<
        ::std::option::Option<::std::vec::Vec<Identity3SemanticConfigurationPolicyPackIdsItem>>,
    >,
    #[serde(
        rename = "waiverIds",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub waiver_ids: FieldPresence<
        ::std::option::Option<::std::vec::Vec<Identity3SemanticConfigurationPolicyWaiverIdsItem>>,
    >,
}
#[doc = "`Identity3SemanticConfigurationPolicyPackIdsItem`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Identity3SemanticConfigurationPolicyPackIdsItem(::std::string::String);
impl ::std::ops::Deref for Identity3SemanticConfigurationPolicyPackIdsItem {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Identity3SemanticConfigurationPolicyPackIdsItem>
    for ::std::string::String
{
    fn from(value: Identity3SemanticConfigurationPolicyPackIdsItem) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Identity3SemanticConfigurationPolicyPackIdsItem {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 128usize {
            return Err("longer than 128 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Identity3SemanticConfigurationPolicyPackIdsItem {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
    for Identity3SemanticConfigurationPolicyPackIdsItem
{
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Identity3SemanticConfigurationPolicyPackIdsItem {
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
#[doc = "`Identity3SemanticConfigurationPolicyWaiverIdsItem`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Identity3SemanticConfigurationPolicyWaiverIdsItem(::std::string::String);
impl ::std::ops::Deref for Identity3SemanticConfigurationPolicyWaiverIdsItem {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Identity3SemanticConfigurationPolicyWaiverIdsItem>
    for ::std::string::String
{
    fn from(value: Identity3SemanticConfigurationPolicyWaiverIdsItem) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Identity3SemanticConfigurationPolicyWaiverIdsItem {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 128usize {
            return Err("longer than 128 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Identity3SemanticConfigurationPolicyWaiverIdsItem {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
    for Identity3SemanticConfigurationPolicyWaiverIdsItem
{
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Identity3SemanticConfigurationPolicyWaiverIdsItem {
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
#[doc = "`Identity3SemanticEvidence`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3SemanticEvidence {
    #[serde(rename = "coverageIds")]
    pub coverage_ids: ::std::vec::Vec<::std::string::String>,
    #[serde(rename = "findingIds")]
    pub finding_ids: ::std::vec::Vec<::std::string::String>,
    #[doc = "Exactly the Plan-selected import set of this Run's Plan, repeated: equal as a canonical set to plan.importIds (IMPORT_JOIN). A repetition of the selection, never a second selection. This array is not an evaluated subset and is not proof.evaluationInputRefs (that field is the complete selectedRefs plus the execution-inputs ref). A selected import that nothing evaluated is still resolved and retained by the Run closure, and being selected alone grants it no evidence authority. Matched and uncertain observation addresses live on predicate-witness matchingImportRows/uncertainImportRows. Atomic predicateProofs[].inputRefs copy the whole evaluationInputRefs under composition §9.2 and therefore may list every selected import without those imports being consulted observation evidence."]
    #[serde(rename = "importIds")]
    pub import_ids: ::std::vec::Vec<::std::string::String>,
    #[serde(rename = "planId")]
    pub plan_id: ::std::string::String,
    #[serde(rename = "proofBundleId")]
    pub proof_bundle_id: ::std::string::String,
    #[serde(rename = "schemaVersion")]
    pub schema_version: ExactInteger,
    #[serde(rename = "viewIds")]
    pub view_ids: ::std::vec::Vec<::std::string::String>,
}
#[doc = "`Identity3SemanticGrant`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3SemanticGrant {
    #[serde(rename = "analysisOperations")]
    pub analysis_operations: ::std::vec::Vec<Identity3SemanticGrantAnalysisOperationsItem>,
    pub principals: ::std::vec::Vec<Identity3SemanticGrantPrincipalsItem>,
    #[serde(rename = "projectId")]
    pub project_id: Identity3ProjectId,
    #[serde(rename = "schemaVersion")]
    pub schema_version: ExactInteger,
    #[serde(rename = "scopeDigest")]
    pub scope_digest: Identity3Hash,
}
#[doc = "`Identity3SemanticGrantAnalysisOperationsItem`"]
#[derive(
    :: serde :: Deserialize,
    :: serde :: Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd,
)]
pub enum Identity3SemanticGrantAnalysisOperationsItem {
    #[serde(rename = "read-source")]
    ReadSource,
    #[serde(rename = "read-import")]
    ReadImport,
    #[serde(rename = "native-analysis")]
    NativeAnalysis,
    #[serde(rename = "prepare-code")]
    PrepareCode,
}
impl ::std::fmt::Display for Identity3SemanticGrantAnalysisOperationsItem {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::ReadSource => f.write_str("read-source"),
            Self::ReadImport => f.write_str("read-import"),
            Self::NativeAnalysis => f.write_str("native-analysis"),
            Self::PrepareCode => f.write_str("prepare-code"),
        }
    }
}
impl ::std::str::FromStr for Identity3SemanticGrantAnalysisOperationsItem {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "read-source" => Ok(Self::ReadSource),
            "read-import" => Ok(Self::ReadImport),
            "native-analysis" => Ok(Self::NativeAnalysis),
            "prepare-code" => Ok(Self::PrepareCode),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Identity3SemanticGrantAnalysisOperationsItem {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
    for Identity3SemanticGrantAnalysisOperationsItem
{
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
#[doc = "`Identity3SemanticGrantPrincipalsItem`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3SemanticGrantPrincipalsItem {
    #[serde(rename = "closureId")]
    pub closure_id: ::std::string::String,
    pub kind: Identity3SemanticGrantPrincipalsItemKind,
    #[serde(
        rename = "ownerSourceDigest",
        deserialize_with = "::std::option::Option::deserialize"
    )]
    pub owner_source_digest: ::std::option::Option<Identity3Hash>,
}
#[doc = "`Identity3SemanticGrantPrincipalsItemKind`"]
#[derive(
    :: serde :: Deserialize,
    :: serde :: Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd,
)]
pub enum Identity3SemanticGrantPrincipalsItemKind {
    #[serde(rename = "first-party")]
    FirstParty,
    #[serde(rename = "trusted-repository-code")]
    TrustedRepositoryCode,
}
impl ::std::fmt::Display for Identity3SemanticGrantPrincipalsItemKind {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::FirstParty => f.write_str("first-party"),
            Self::TrustedRepositoryCode => f.write_str("trusted-repository-code"),
        }
    }
}
impl ::std::str::FromStr for Identity3SemanticGrantPrincipalsItemKind {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "first-party" => Ok(Self::FirstParty),
            "trusted-repository-code" => Ok(Self::TrustedRepositoryCode),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Identity3SemanticGrantPrincipalsItemKind {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3SemanticGrantPrincipalsItemKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
#[doc = "`Identity3Snapshot`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3Snapshot {
    #[serde(rename = "projectId")]
    pub project_id: Identity3ProjectId,
    #[serde(rename = "resolvedConfigDigest")]
    pub resolved_config_digest: ::std::string::String,
    #[serde(rename = "schemaVersion")]
    pub schema_version: ExactInteger,
    #[serde(rename = "scopeDigest")]
    pub scope_digest: ::std::string::String,
    #[serde(rename = "sourceInventory")]
    pub source_inventory: Identity3SourceInventory,
    #[serde(rename = "vcsDigest")]
    pub vcs_digest: ::std::string::String,
}
#[doc = "The snapshot source inventory as a registered record in its own right, so that vcs-observation.sourceInventoryDigest names a record rather than an unnamed canonical fragment."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(transparent)]
pub struct Identity3SourceInventory(pub ::std::vec::Vec<Identity3Blob>);
impl ::std::ops::Deref for Identity3SourceInventory {
    type Target = ::std::vec::Vec<Identity3Blob>;
    fn deref(&self) -> &::std::vec::Vec<Identity3Blob> {
        &self.0
    }
}
impl ::std::convert::From<Identity3SourceInventory> for ::std::vec::Vec<Identity3Blob> {
    fn from(value: Identity3SourceInventory) -> Self {
        value.0
    }
}
impl ::std::convert::From<::std::vec::Vec<Identity3Blob>> for Identity3SourceInventory {
    fn from(value: ::std::vec::Vec<Identity3Blob>) -> Self {
        Self(value)
    }
}
#[doc = "The closed record digested by stageSpecDigest. execution-plan.stages[].stageSpecDigest and cache-key.stageSpecDigest are the SAME field name because they are the same digest of the same record under the same recipe; there are not two recipes for one spelling."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3StageSpec {
    pub operation: Identity3Text,
    #[doc = "Declared output-domain set. Empty is permitted and asserts no output domains; it does not establish completeness or result authority. Stage and stage-spec sets must agree."]
    #[serde(rename = "outputDomains")]
    pub output_domains: ::std::vec::Vec<Identity3Domain>,
    #[serde(rename = "outputSchemaDigest")]
    pub output_schema_digest: ::std::string::String,
    #[doc = "every row must also be a row of the Plan analysis-spec parameters: a stage takes no hidden input"]
    pub parameters: ::std::vec::Vec<Identity3StageSpecParametersItem>,
    #[serde(rename = "planId")]
    pub plan_id: ::std::string::String,
    #[serde(rename = "producerClosure")]
    pub producer_closure: ::std::string::String,
    #[serde(rename = "schemaVersion")]
    pub schema_version: ExactInteger,
}
#[doc = "`Identity3StageSpecParametersItem`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3StageSpecParametersItem {
    #[serde(rename = "payloadDigest")]
    pub payload_digest: ::std::string::String,
    #[serde(rename = "schemaDigest")]
    pub schema_digest: ::std::string::String,
}
#[doc = "`Identity3SubjectInventoryRef`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3SubjectInventoryRef {
    pub digest: ::std::string::String,
    pub domain: ::serde_json::Value,
}
#[doc = "`Identity3SubjectScope`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3SubjectScope {
    #[doc = "The Plan-selected closure that enumerated this scope. Its kind must be 'provider': enumeration is a native provider act, and no 'enumerator' kind is minted for it. The closure must also be a member of plan.semanticClosures, so the enumerator is one the Plan selected."]
    #[serde(rename = "enumeratorClosure")]
    pub enumerator_closure: ::std::string::String,
    pub relation: Identity3SubjectScopeRelation,
    pub resolution: Identity3SubjectScopeResolution,
    #[serde(rename = "schemaVersion")]
    pub schema_version: ExactInteger,
    #[serde(rename = "snapshotId")]
    pub snapshot_id: ::std::string::String,
    #[serde(rename = "sourceUniverse")]
    pub source_universe: ::std::string::String,
    pub subjects: ::std::vec::Vec<Identity3SubjectScopeSubjectsItem>,
    #[serde(rename = "targetUniverse")]
    pub target_universe: ::std::string::String,
}
#[doc = "`Identity3SubjectScopeRelation`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Identity3SubjectScopeRelation(::std::string::String);
impl ::std::ops::Deref for Identity3SubjectScopeRelation {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Identity3SubjectScopeRelation> for ::std::string::String {
    fn from(value: Identity3SubjectScopeRelation) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Identity3SubjectScopeRelation {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 4096usize {
            return Err("longer than 4096 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Identity3SubjectScopeRelation {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3SubjectScopeRelation {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Identity3SubjectScopeRelation {
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
#[doc = "`Identity3SubjectScopeResolution`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Identity3SubjectScopeResolution(::std::string::String);
impl ::std::ops::Deref for Identity3SubjectScopeResolution {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Identity3SubjectScopeResolution> for ::std::string::String {
    fn from(value: Identity3SubjectScopeResolution) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Identity3SubjectScopeResolution {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 4096usize {
            return Err("longer than 4096 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Identity3SubjectScopeResolution {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3SubjectScopeResolution {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Identity3SubjectScopeResolution {
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
#[doc = "`Identity3SubjectScopeSubjectsItem`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Identity3SubjectScopeSubjectsItem(::std::string::String);
impl ::std::ops::Deref for Identity3SubjectScopeSubjectsItem {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Identity3SubjectScopeSubjectsItem> for ::std::string::String {
    fn from(value: Identity3SubjectScopeSubjectsItem) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Identity3SubjectScopeSubjectsItem {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 4096usize {
            return Err("longer than 4096 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Identity3SubjectScopeSubjectsItem {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3SubjectScopeSubjectsItem {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Identity3SubjectScopeSubjectsItem {
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
#[doc = "`Identity3Text`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Identity3Text(::std::string::String);
impl ::std::ops::Deref for Identity3Text {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Identity3Text> for ::std::string::String {
    fn from(value: Identity3Text) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Identity3Text {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 4096usize {
            return Err("longer than 4096 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Identity3Text {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3Text {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Identity3Text {
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
#[doc = "`Identity3U64`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(transparent)]
pub struct Identity3U64(pub u64);
impl ::std::ops::Deref for Identity3U64 {
    type Target = u64;
    fn deref(&self) -> &u64 {
        &self.0
    }
}
impl ::std::convert::From<Identity3U64> for u64 {
    fn from(value: Identity3U64) -> Self {
        value.0
    }
}
impl ::std::convert::From<u64> for Identity3U64 {
    fn from(value: u64) -> Self {
        Self(value)
    }
}
impl ::std::fmt::Display for Identity3U64 {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        self.0.fmt(f)
    }
}
impl ::std::str::FromStr for Identity3U64 {
    type Err = <u64 as ::std::str::FromStr>::Err;
    fn from_str(value: &str) -> ::std::result::Result<Self, Self::Err> {
        Ok(Self(value.parse()?))
    }
}
impl ::std::convert::TryFrom<&str> for Identity3U64 {
    type Error = <u64 as ::std::str::FromStr>::Err;
    fn try_from(value: &str) -> ::std::result::Result<Self, Self::Error> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<String> for Identity3U64 {
    type Error = <u64 as ::std::str::FromStr>::Err;
    fn try_from(value: String) -> ::std::result::Result<Self, Self::Error> {
        value.parse()
    }
}
#[doc = "`Identity3VcsObservation`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3VcsObservation {
    #[serde(
        rename = "commitId",
        deserialize_with = "::std::option::Option::deserialize"
    )]
    pub commit_id: ::std::option::Option<Identity3Text>,
    pub dirty: bool,
    pub kind: Identity3VcsObservationKind,
    #[serde(rename = "schemaVersion")]
    pub schema_version: ExactInteger,
    #[serde(rename = "sourceInventoryDigest")]
    pub source_inventory_digest: Identity3Hash,
}
#[doc = "`Identity3VcsObservationKind`"]
#[derive(
    :: serde :: Deserialize,
    :: serde :: Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd,
)]
pub enum Identity3VcsObservationKind {
    #[serde(rename = "none")]
    None,
    #[serde(rename = "git")]
    Git,
    #[serde(rename = "hg")]
    Hg,
    #[serde(rename = "svn")]
    Svn,
    #[serde(rename = "jj")]
    Jj,
}
impl ::std::fmt::Display for Identity3VcsObservationKind {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::None => f.write_str("none"),
            Self::Git => f.write_str("git"),
            Self::Hg => f.write_str("hg"),
            Self::Svn => f.write_str("svn"),
            Self::Jj => f.write_str("jj"),
        }
    }
}
impl ::std::str::FromStr for Identity3VcsObservationKind {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "none" => Ok(Self::None),
            "git" => Ok(Self::Git),
            "hg" => Ok(Self::Hg),
            "svn" => Ok(Self::Svn),
            "jj" => Ok(Self::Jj),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Identity3VcsObservationKind {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Identity3VcsObservationKind {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
#[doc = "`Identity3View`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Identity3View {
    #[serde(rename = "coverageIds")]
    pub coverage_ids: ::std::vec::Vec<::std::string::String>,
    pub facts: ::std::vec::Vec<::std::string::String>,
    #[serde(rename = "planId")]
    pub plan_id: ::std::string::String,
    #[serde(rename = "producerClosure")]
    pub producer_closure: ::std::string::String,
    #[serde(rename = "schemaDigests")]
    pub schema_digests: ::std::vec::Vec<::std::string::String>,
    #[serde(rename = "schemaVersion")]
    pub schema_version: ExactInteger,
    #[serde(rename = "scopeIds")]
    pub scope_ids: ::std::vec::Vec<::std::string::String>,
}
