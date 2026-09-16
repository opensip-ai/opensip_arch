// Generated trial: named28 profile, typify0.8.0; inert carriers only.
#![allow(unused_imports)]
use super::evidence::*;
use super::identity::*;
use super::invocation::*;
use super::output::*;
use super::evidence::error;
///`Control3Root`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(tag = "type", deny_unknown_fields)]
pub enum Control3Root {
    #[serde(rename = "hello")]
    Hello {
        body: Control3RootVariant0Property0,
        #[serde(rename = "controlMajor")]
        control_major: ::std::num::NonZeroU64,
        seq: ::std::num::NonZeroU64,
    },
    #[serde(rename = "helloAck")]
    HelloAck {
        body: Control3RootVariant1Property0,
        #[serde(rename = "controlMajor")]
        control_major: ::std::num::NonZeroU64,
        seq: ::std::num::NonZeroU64,
    },
    #[serde(rename = "select")]
    Select {
        body: Control3RootVariant2Property0,
        #[serde(rename = "controlMajor")]
        control_major: ::std::num::NonZeroU64,
        seq: ::std::num::NonZeroU64,
    },
    #[serde(rename = "selectAck")]
    SelectAck {
        body: Control3RootVariant3Property0,
        #[serde(rename = "controlMajor")]
        control_major: ::std::num::NonZeroU64,
        seq: ::std::num::NonZeroU64,
    },
    #[serde(rename = "refusal")]
    Refusal {
        body: Control3RootVariant4Property0,
        #[serde(rename = "controlMajor")]
        control_major: ::std::num::NonZeroU64,
        seq: ::std::num::NonZeroU64,
    },
    #[serde(rename = "ping")]
    Ping {
        body: Control3RootVariant5Property0,
        #[serde(rename = "controlMajor")]
        control_major: ::std::num::NonZeroU64,
        seq: ::std::num::NonZeroU64,
    },
    #[serde(rename = "pong")]
    Pong {
        body: Control3RootVariant6Property0,
        #[serde(rename = "controlMajor")]
        control_major: ::std::num::NonZeroU64,
        seq: ::std::num::NonZeroU64,
    },
    #[serde(rename = "cancel")]
    Cancel {
        body: Control3RootVariant7Property0,
        #[serde(rename = "controlMajor")]
        control_major: ::std::num::NonZeroU64,
        seq: ::std::num::NonZeroU64,
    },
    #[serde(rename = "health")]
    Health {
        body: Control3RootVariant8Property0,
        #[serde(rename = "controlMajor")]
        control_major: ::std::num::NonZeroU64,
        seq: ::std::num::NonZeroU64,
    },
    #[serde(rename = "healthReport")]
    HealthReport {
        body: Control3RootVariant9Property0,
        #[serde(rename = "controlMajor")]
        control_major: ::std::num::NonZeroU64,
        seq: ::std::num::NonZeroU64,
    },
    #[serde(rename = "resourceReport")]
    ResourceReport {
        body: Control3RootVariant10Property0,
        #[serde(rename = "controlMajor")]
        control_major: ::std::num::NonZeroU64,
        seq: ::std::num::NonZeroU64,
    },
    #[serde(rename = "fault")]
    Fault {
        body: Control3RootVariant11Property0,
        #[serde(rename = "controlMajor")]
        control_major: ::std::num::NonZeroU64,
        seq: ::std::num::NonZeroU64,
    },
    #[serde(rename = "effectRequest")]
    EffectRequest {
        body: Control3RootVariant12Property0,
        #[serde(rename = "controlMajor")]
        control_major: ::std::num::NonZeroU64,
        seq: ::std::num::NonZeroU64,
    },
    #[serde(rename = "effectResult")]
    EffectResult {
        body: Control3RootVariant13Property0,
        #[serde(rename = "controlMajor")]
        control_major: ::std::num::NonZeroU64,
        seq: ::std::num::NonZeroU64,
    },
    #[serde(rename = "shutdown")]
    Shutdown {
        body: Control3RootVariant14Property0,
        #[serde(rename = "controlMajor")]
        control_major: ::std::num::NonZeroU64,
        seq: ::std::num::NonZeroU64,
    },
    #[serde(rename = "shutdownAck")]
    ShutdownAck {
        body: Control3RootVariant15Property0,
        #[serde(rename = "controlMajor")]
        control_major: ::std::num::NonZeroU64,
        seq: ::std::num::NonZeroU64,
    },
}
///`Control3RootVariant0Property0`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Control3RootVariant0Property0 {
    #[serde(rename = "admittedManifestDigest")]
    pub admitted_manifest_digest: ::std::string::String,
    #[serde(rename = "controlMajor")]
    pub control_major: ::std::num::NonZeroU64,
    #[serde(rename = "expectedStableId")]
    pub expected_stable_id: ::std::string::String,
    #[serde(rename = "maxControlFrameBytesOffer")]
    pub max_control_frame_bytes_offer: i64,
    pub platform: Control3RootVariant0Property0Platform,
    #[serde(rename = "subprotocolOffers")]
    pub subprotocol_offers: ::std::vec::Vec<
        Control3RootVariant0Property0SubprotocolOffersItem,
    >,
}
///`Control3RootVariant0Property0Platform`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Control3RootVariant0Property0Platform {
    pub arch: Control3RootVariant0Property0PlatformArch,
    pub os: Control3RootVariant0Property0PlatformOs,
}
///`Control3RootVariant0Property0PlatformArch`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Control3RootVariant0Property0PlatformArch {
    #[serde(rename = "arm64")]
    Arm64,
    #[serde(rename = "x86_64")]
    X8664,
}
impl ::std::fmt::Display for Control3RootVariant0Property0PlatformArch {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Arm64 => f.write_str("arm64"),
            Self::X8664 => f.write_str("x86_64"),
        }
    }
}
impl ::std::str::FromStr for Control3RootVariant0Property0PlatformArch {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "arm64" => Ok(Self::Arm64),
            "x86_64" => Ok(Self::X8664),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Control3RootVariant0Property0PlatformArch {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Control3RootVariant0Property0PlatformArch {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Control3RootVariant0Property0PlatformOs`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Control3RootVariant0Property0PlatformOs {
    #[serde(rename = "macos")]
    Macos,
    #[serde(rename = "linux")]
    Linux,
}
impl ::std::fmt::Display for Control3RootVariant0Property0PlatformOs {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Macos => f.write_str("macos"),
            Self::Linux => f.write_str("linux"),
        }
    }
}
impl ::std::str::FromStr for Control3RootVariant0Property0PlatformOs {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "macos" => Ok(Self::Macos),
            "linux" => Ok(Self::Linux),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Control3RootVariant0Property0PlatformOs {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Control3RootVariant0Property0PlatformOs {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Control3RootVariant0Property0SubprotocolOffersItem`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Control3RootVariant0Property0SubprotocolOffersItem {
    pub role: Control3RootVariant0Property0SubprotocolOffersItemRole,
    #[serde(rename = "roleSubprotocol")]
    pub role_subprotocol: Control3RootVariant0Property0SubprotocolOffersItemRoleSubprotocol,
    #[serde(rename = "subprotocolVersion")]
    pub subprotocol_version: ::std::num::NonZeroU64,
}
///`Control3RootVariant0Property0SubprotocolOffersItemRole`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Control3RootVariant0Property0SubprotocolOffersItemRole(::std::string::String);
impl ::std::ops::Deref for Control3RootVariant0Property0SubprotocolOffersItemRole {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Control3RootVariant0Property0SubprotocolOffersItemRole>
for ::std::string::String {
    fn from(value: Control3RootVariant0Property0SubprotocolOffersItemRole) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Control3RootVariant0Property0SubprotocolOffersItemRole {
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
for Control3RootVariant0Property0SubprotocolOffersItemRole {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Control3RootVariant0Property0SubprotocolOffersItemRole {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de>
for Control3RootVariant0Property0SubprotocolOffersItemRole {
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
///`Control3RootVariant0Property0SubprotocolOffersItemRoleSubprotocol`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Control3RootVariant0Property0SubprotocolOffersItemRoleSubprotocol(
    ::std::string::String,
);
impl ::std::ops::Deref
for Control3RootVariant0Property0SubprotocolOffersItemRoleSubprotocol {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<
    Control3RootVariant0Property0SubprotocolOffersItemRoleSubprotocol,
> for ::std::string::String {
    fn from(
        value: Control3RootVariant0Property0SubprotocolOffersItemRoleSubprotocol,
    ) -> Self {
        value.0
    }
}
impl ::std::str::FromStr
for Control3RootVariant0Property0SubprotocolOffersItemRoleSubprotocol {
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
for Control3RootVariant0Property0SubprotocolOffersItemRoleSubprotocol {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Control3RootVariant0Property0SubprotocolOffersItemRoleSubprotocol {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de>
for Control3RootVariant0Property0SubprotocolOffersItemRoleSubprotocol {
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
///`Control3RootVariant10Property0`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Control3RootVariant10Property0 {
    #[serde(rename = "cpuNanoseconds")]
    pub cpu_nanoseconds: i64,
    #[serde(rename = "openHandles")]
    pub open_handles: i64,
    #[serde(rename = "residentBytes")]
    pub resident_bytes: i64,
}
///`Control3RootVariant11Property0`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Control3RootVariant11Property0 {
    pub detail: Control3RootVariant11Property0Detail,
}
///`Control3RootVariant11Property0Detail`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Control3RootVariant11Property0Detail(::std::string::String);
impl ::std::ops::Deref for Control3RootVariant11Property0Detail {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Control3RootVariant11Property0Detail>
for ::std::string::String {
    fn from(value: Control3RootVariant11Property0Detail) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Control3RootVariant11Property0Detail {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 1024usize {
            return Err("longer than 1024 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Control3RootVariant11Property0Detail {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Control3RootVariant11Property0Detail {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Control3RootVariant11Property0Detail {
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
///`Control3RootVariant12Property0`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Control3RootVariant12Property0 {
    #[serde(rename = "authorizationRef")]
    pub authorization_ref: Control3RootVariant12Property0AuthorizationRef,
    #[serde(rename = "effectClass")]
    pub effect_class: Control3RootVariant12Property0EffectClass,
    #[serde(rename = "operationRef")]
    pub operation_ref: Control3RootVariant12Property0OperationRef,
}
///`Control3RootVariant12Property0AuthorizationRef`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Control3RootVariant12Property0AuthorizationRef(::std::string::String);
impl ::std::ops::Deref for Control3RootVariant12Property0AuthorizationRef {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Control3RootVariant12Property0AuthorizationRef>
for ::std::string::String {
    fn from(value: Control3RootVariant12Property0AuthorizationRef) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Control3RootVariant12Property0AuthorizationRef {
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
impl ::std::convert::TryFrom<&str> for Control3RootVariant12Property0AuthorizationRef {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Control3RootVariant12Property0AuthorizationRef {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Control3RootVariant12Property0AuthorizationRef {
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
///`Control3RootVariant12Property0EffectClass`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Control3RootVariant12Property0EffectClass {
    #[serde(rename = "HE-1")]
    He1,
    #[serde(rename = "HE-2")]
    He2,
}
impl ::std::fmt::Display for Control3RootVariant12Property0EffectClass {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::He1 => f.write_str("HE-1"),
            Self::He2 => f.write_str("HE-2"),
        }
    }
}
impl ::std::str::FromStr for Control3RootVariant12Property0EffectClass {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "HE-1" => Ok(Self::He1),
            "HE-2" => Ok(Self::He2),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Control3RootVariant12Property0EffectClass {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Control3RootVariant12Property0EffectClass {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Control3RootVariant12Property0OperationRef`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Control3RootVariant12Property0OperationRef(::std::string::String);
impl ::std::ops::Deref for Control3RootVariant12Property0OperationRef {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Control3RootVariant12Property0OperationRef>
for ::std::string::String {
    fn from(value: Control3RootVariant12Property0OperationRef) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Control3RootVariant12Property0OperationRef {
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
impl ::std::convert::TryFrom<&str> for Control3RootVariant12Property0OperationRef {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Control3RootVariant12Property0OperationRef {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Control3RootVariant12Property0OperationRef {
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
///`Control3RootVariant13Property0`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Control3RootVariant13Property0 {
    #[serde(rename = "commitClass")]
    pub commit_class: Control3RootVariant13Property0CommitClass,
    #[serde(rename = "decisionSeq")]
    pub decision_seq: ::std::num::NonZeroU64,
    #[serde(rename = "effectOutcome")]
    pub effect_outcome: Control3RootVariant13Property0EffectOutcome,
    #[serde(rename = "outcomeSeq")]
    pub outcome_seq: ::std::num::NonZeroU64,
    #[serde(rename = "requestSeq")]
    pub request_seq: ::std::num::NonZeroU64,
    #[serde(
        rename = "resultRef",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub result_ref: FieldPresence<
        ::std::option::Option<Control3RootVariant13Property0ResultRef>,
    >,
}
///`Control3RootVariant13Property0CommitClass`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Control3RootVariant13Property0CommitClass {
    #[serde(rename = "REVERSIBLE")]
    Reversible,
    #[serde(rename = "IRREVERSIBLE")]
    Irreversible,
}
impl ::std::fmt::Display for Control3RootVariant13Property0CommitClass {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Reversible => f.write_str("REVERSIBLE"),
            Self::Irreversible => f.write_str("IRREVERSIBLE"),
        }
    }
}
impl ::std::str::FromStr for Control3RootVariant13Property0CommitClass {
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
impl ::std::convert::TryFrom<&str> for Control3RootVariant13Property0CommitClass {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Control3RootVariant13Property0CommitClass {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Control3RootVariant13Property0EffectOutcome`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Control3RootVariant13Property0EffectOutcome {
    #[serde(rename = "COMPLETED")]
    Completed,
    #[serde(rename = "FAILED")]
    Failed,
    #[serde(rename = "INDETERMINATE")]
    Indeterminate,
}
impl ::std::fmt::Display for Control3RootVariant13Property0EffectOutcome {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Completed => f.write_str("COMPLETED"),
            Self::Failed => f.write_str("FAILED"),
            Self::Indeterminate => f.write_str("INDETERMINATE"),
        }
    }
}
impl ::std::str::FromStr for Control3RootVariant13Property0EffectOutcome {
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
impl ::std::convert::TryFrom<&str> for Control3RootVariant13Property0EffectOutcome {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Control3RootVariant13Property0EffectOutcome {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Control3RootVariant13Property0ResultRef`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Control3RootVariant13Property0ResultRef(::std::string::String);
impl ::std::ops::Deref for Control3RootVariant13Property0ResultRef {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Control3RootVariant13Property0ResultRef>
for ::std::string::String {
    fn from(value: Control3RootVariant13Property0ResultRef) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Control3RootVariant13Property0ResultRef {
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
impl ::std::convert::TryFrom<&str> for Control3RootVariant13Property0ResultRef {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Control3RootVariant13Property0ResultRef {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Control3RootVariant13Property0ResultRef {
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
///`Control3RootVariant14Property0`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Control3RootVariant14Property0 {
    pub reason: Control3RootVariant14Property0Reason,
}
///`Control3RootVariant14Property0Reason`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Control3RootVariant14Property0Reason {
    #[serde(rename = "normal")]
    Normal,
    #[serde(rename = "cancelled")]
    Cancelled,
    #[serde(rename = "refused")]
    Refused,
    #[serde(rename = "fault")]
    Fault,
}
impl ::std::fmt::Display for Control3RootVariant14Property0Reason {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Normal => f.write_str("normal"),
            Self::Cancelled => f.write_str("cancelled"),
            Self::Refused => f.write_str("refused"),
            Self::Fault => f.write_str("fault"),
        }
    }
}
impl ::std::str::FromStr for Control3RootVariant14Property0Reason {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "normal" => Ok(Self::Normal),
            "cancelled" => Ok(Self::Cancelled),
            "refused" => Ok(Self::Refused),
            "fault" => Ok(Self::Fault),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Control3RootVariant14Property0Reason {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Control3RootVariant14Property0Reason {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Control3RootVariant15Property0`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug, Default)]
#[serde(deny_unknown_fields)]
pub struct Control3RootVariant15Property0 {}
///`Control3RootVariant1Property0`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Control3RootVariant1Property0 {
    #[serde(rename = "admittedManifestDigest")]
    pub admitted_manifest_digest: ::std::string::String,
    #[serde(rename = "controlMajor")]
    pub control_major: ::std::num::NonZeroU64,
    #[serde(rename = "maxControlFrameBytes")]
    pub max_control_frame_bytes: i64,
    #[serde(rename = "stableId")]
    pub stable_id: ::std::string::String,
    #[serde(rename = "subprotocolConfirms")]
    pub subprotocol_confirms: ::std::vec::Vec<
        Control3RootVariant1Property0SubprotocolConfirmsItem,
    >,
}
///`Control3RootVariant1Property0SubprotocolConfirmsItem`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Control3RootVariant1Property0SubprotocolConfirmsItem {
    pub role: Control3RootVariant1Property0SubprotocolConfirmsItemRole,
    #[serde(rename = "roleSubprotocol")]
    pub role_subprotocol: Control3RootVariant1Property0SubprotocolConfirmsItemRoleSubprotocol,
    #[serde(rename = "subprotocolVersion")]
    pub subprotocol_version: ::std::num::NonZeroU64,
}
///`Control3RootVariant1Property0SubprotocolConfirmsItemRole`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Control3RootVariant1Property0SubprotocolConfirmsItemRole(
    ::std::string::String,
);
impl ::std::ops::Deref for Control3RootVariant1Property0SubprotocolConfirmsItemRole {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Control3RootVariant1Property0SubprotocolConfirmsItemRole>
for ::std::string::String {
    fn from(value: Control3RootVariant1Property0SubprotocolConfirmsItemRole) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Control3RootVariant1Property0SubprotocolConfirmsItemRole {
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
for Control3RootVariant1Property0SubprotocolConfirmsItemRole {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Control3RootVariant1Property0SubprotocolConfirmsItemRole {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de>
for Control3RootVariant1Property0SubprotocolConfirmsItemRole {
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
///`Control3RootVariant1Property0SubprotocolConfirmsItemRoleSubprotocol`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Control3RootVariant1Property0SubprotocolConfirmsItemRoleSubprotocol(
    ::std::string::String,
);
impl ::std::ops::Deref
for Control3RootVariant1Property0SubprotocolConfirmsItemRoleSubprotocol {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<
    Control3RootVariant1Property0SubprotocolConfirmsItemRoleSubprotocol,
> for ::std::string::String {
    fn from(
        value: Control3RootVariant1Property0SubprotocolConfirmsItemRoleSubprotocol,
    ) -> Self {
        value.0
    }
}
impl ::std::str::FromStr
for Control3RootVariant1Property0SubprotocolConfirmsItemRoleSubprotocol {
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
for Control3RootVariant1Property0SubprotocolConfirmsItemRoleSubprotocol {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Control3RootVariant1Property0SubprotocolConfirmsItemRoleSubprotocol {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de>
for Control3RootVariant1Property0SubprotocolConfirmsItemRoleSubprotocol {
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
///`Control3RootVariant2Property0`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Control3RootVariant2Property0 {
    pub role: Control3RootVariant2Property0Role,
    #[serde(rename = "roleSubprotocol")]
    pub role_subprotocol: Control3RootVariant2Property0RoleSubprotocol,
    #[serde(rename = "subprotocolVersion")]
    pub subprotocol_version: ::std::num::NonZeroU64,
}
///`Control3RootVariant2Property0Role`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Control3RootVariant2Property0Role(::std::string::String);
impl ::std::ops::Deref for Control3RootVariant2Property0Role {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Control3RootVariant2Property0Role> for ::std::string::String {
    fn from(value: Control3RootVariant2Property0Role) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Control3RootVariant2Property0Role {
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
impl ::std::convert::TryFrom<&str> for Control3RootVariant2Property0Role {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Control3RootVariant2Property0Role {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Control3RootVariant2Property0Role {
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
///`Control3RootVariant2Property0RoleSubprotocol`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Control3RootVariant2Property0RoleSubprotocol(::std::string::String);
impl ::std::ops::Deref for Control3RootVariant2Property0RoleSubprotocol {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Control3RootVariant2Property0RoleSubprotocol>
for ::std::string::String {
    fn from(value: Control3RootVariant2Property0RoleSubprotocol) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Control3RootVariant2Property0RoleSubprotocol {
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
impl ::std::convert::TryFrom<&str> for Control3RootVariant2Property0RoleSubprotocol {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Control3RootVariant2Property0RoleSubprotocol {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Control3RootVariant2Property0RoleSubprotocol {
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
///`Control3RootVariant3Property0`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Control3RootVariant3Property0 {
    pub role: Control3RootVariant3Property0Role,
    #[serde(rename = "roleSubprotocol")]
    pub role_subprotocol: Control3RootVariant3Property0RoleSubprotocol,
    #[serde(rename = "subprotocolVersion")]
    pub subprotocol_version: ::std::num::NonZeroU64,
}
///`Control3RootVariant3Property0Role`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Control3RootVariant3Property0Role(::std::string::String);
impl ::std::ops::Deref for Control3RootVariant3Property0Role {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Control3RootVariant3Property0Role> for ::std::string::String {
    fn from(value: Control3RootVariant3Property0Role) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Control3RootVariant3Property0Role {
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
impl ::std::convert::TryFrom<&str> for Control3RootVariant3Property0Role {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Control3RootVariant3Property0Role {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Control3RootVariant3Property0Role {
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
///`Control3RootVariant3Property0RoleSubprotocol`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Control3RootVariant3Property0RoleSubprotocol(::std::string::String);
impl ::std::ops::Deref for Control3RootVariant3Property0RoleSubprotocol {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Control3RootVariant3Property0RoleSubprotocol>
for ::std::string::String {
    fn from(value: Control3RootVariant3Property0RoleSubprotocol) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Control3RootVariant3Property0RoleSubprotocol {
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
impl ::std::convert::TryFrom<&str> for Control3RootVariant3Property0RoleSubprotocol {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Control3RootVariant3Property0RoleSubprotocol {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Control3RootVariant3Property0RoleSubprotocol {
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
///`Control3RootVariant4Property0`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Control3RootVariant4Property0 {
    #[serde(
        rename = "decisionClass",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub decision_class: FieldPresence<
        ::std::option::Option<Control3RootVariant4Property0DecisionClass>,
    >,
    #[serde(default, skip_serializing_if = "FieldPresence::is_missing")]
    pub detail: FieldPresence<
        ::std::option::Option<Control3RootVariant4Property0Detail>,
    >,
    pub family: Control3RootVariant4Property0Family,
    #[serde(
        rename = "supportedControlMajors",
        default,
        skip_serializing_if = "FieldPresence::is_missing"
    )]
    pub supported_control_majors: FieldPresence<
        ::std::option::Option<::std::vec::Vec<::std::num::NonZeroU64>>,
    >,
}
///`Control3RootVariant4Property0DecisionClass`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Control3RootVariant4Property0DecisionClass {
    #[serde(rename = "PR-1")]
    Pr1,
    #[serde(rename = "PR-2")]
    Pr2,
    #[serde(rename = "PR-3")]
    Pr3,
    #[serde(rename = "PR-4")]
    Pr4,
    #[serde(rename = "PR-5")]
    Pr5,
    #[serde(rename = "PR-6")]
    Pr6,
    #[serde(rename = "PR-7")]
    Pr7,
    #[serde(rename = "PR-8")]
    Pr8,
    #[serde(rename = "PR-9")]
    Pr9,
}
impl ::std::fmt::Display for Control3RootVariant4Property0DecisionClass {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Pr1 => f.write_str("PR-1"),
            Self::Pr2 => f.write_str("PR-2"),
            Self::Pr3 => f.write_str("PR-3"),
            Self::Pr4 => f.write_str("PR-4"),
            Self::Pr5 => f.write_str("PR-5"),
            Self::Pr6 => f.write_str("PR-6"),
            Self::Pr7 => f.write_str("PR-7"),
            Self::Pr8 => f.write_str("PR-8"),
            Self::Pr9 => f.write_str("PR-9"),
        }
    }
}
impl ::std::str::FromStr for Control3RootVariant4Property0DecisionClass {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "PR-1" => Ok(Self::Pr1),
            "PR-2" => Ok(Self::Pr2),
            "PR-3" => Ok(Self::Pr3),
            "PR-4" => Ok(Self::Pr4),
            "PR-5" => Ok(Self::Pr5),
            "PR-6" => Ok(Self::Pr6),
            "PR-7" => Ok(Self::Pr7),
            "PR-8" => Ok(Self::Pr8),
            "PR-9" => Ok(Self::Pr9),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Control3RootVariant4Property0DecisionClass {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Control3RootVariant4Property0DecisionClass {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Control3RootVariant4Property0Detail`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Control3RootVariant4Property0Detail(::std::string::String);
impl ::std::ops::Deref for Control3RootVariant4Property0Detail {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Control3RootVariant4Property0Detail>
for ::std::string::String {
    fn from(value: Control3RootVariant4Property0Detail) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Control3RootVariant4Property0Detail {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 1024usize {
            return Err("longer than 1024 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Control3RootVariant4Property0Detail {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Control3RootVariant4Property0Detail {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Control3RootVariant4Property0Detail {
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
///`Control3RootVariant4Property0Family`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Control3RootVariant4Property0Family {
    #[serde(rename = "RF-1")]
    Rf1,
    #[serde(rename = "RF-2")]
    Rf2,
    #[serde(rename = "RF-3")]
    Rf3,
    #[serde(rename = "RF-4")]
    Rf4,
    #[serde(rename = "RF-5")]
    Rf5,
    #[serde(rename = "RF-6")]
    Rf6,
    #[serde(rename = "RF-7")]
    Rf7,
    #[serde(rename = "RF-8")]
    Rf8,
}
impl ::std::fmt::Display for Control3RootVariant4Property0Family {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Rf1 => f.write_str("RF-1"),
            Self::Rf2 => f.write_str("RF-2"),
            Self::Rf3 => f.write_str("RF-3"),
            Self::Rf4 => f.write_str("RF-4"),
            Self::Rf5 => f.write_str("RF-5"),
            Self::Rf6 => f.write_str("RF-6"),
            Self::Rf7 => f.write_str("RF-7"),
            Self::Rf8 => f.write_str("RF-8"),
        }
    }
}
impl ::std::str::FromStr for Control3RootVariant4Property0Family {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "RF-1" => Ok(Self::Rf1),
            "RF-2" => Ok(Self::Rf2),
            "RF-3" => Ok(Self::Rf3),
            "RF-4" => Ok(Self::Rf4),
            "RF-5" => Ok(Self::Rf5),
            "RF-6" => Ok(Self::Rf6),
            "RF-7" => Ok(Self::Rf7),
            "RF-8" => Ok(Self::Rf8),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Control3RootVariant4Property0Family {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Control3RootVariant4Property0Family {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Control3RootVariant5Property0`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Control3RootVariant5Property0 {
    pub nonce: Control3RootVariant5Property0Nonce,
}
///`Control3RootVariant5Property0Nonce`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Control3RootVariant5Property0Nonce(::std::string::String);
impl ::std::ops::Deref for Control3RootVariant5Property0Nonce {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Control3RootVariant5Property0Nonce> for ::std::string::String {
    fn from(value: Control3RootVariant5Property0Nonce) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Control3RootVariant5Property0Nonce {
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
impl ::std::convert::TryFrom<&str> for Control3RootVariant5Property0Nonce {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Control3RootVariant5Property0Nonce {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Control3RootVariant5Property0Nonce {
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
///`Control3RootVariant6Property0`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Control3RootVariant6Property0 {
    pub nonce: Control3RootVariant6Property0Nonce,
}
///`Control3RootVariant6Property0Nonce`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Control3RootVariant6Property0Nonce(::std::string::String);
impl ::std::ops::Deref for Control3RootVariant6Property0Nonce {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Control3RootVariant6Property0Nonce> for ::std::string::String {
    fn from(value: Control3RootVariant6Property0Nonce) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Control3RootVariant6Property0Nonce {
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
impl ::std::convert::TryFrom<&str> for Control3RootVariant6Property0Nonce {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Control3RootVariant6Property0Nonce {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Control3RootVariant6Property0Nonce {
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
///`Control3RootVariant7Property0`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Control3RootVariant7Property0 {
    pub reason: Control3RootVariant7Property0Reason,
}
///`Control3RootVariant7Property0Reason`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Control3RootVariant7Property0Reason {
    #[serde(rename = "user")]
    User,
    #[serde(rename = "deadline")]
    Deadline,
    #[serde(rename = "supervisor-fault")]
    SupervisorFault,
}
impl ::std::fmt::Display for Control3RootVariant7Property0Reason {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::User => f.write_str("user"),
            Self::Deadline => f.write_str("deadline"),
            Self::SupervisorFault => f.write_str("supervisor-fault"),
        }
    }
}
impl ::std::str::FromStr for Control3RootVariant7Property0Reason {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "user" => Ok(Self::User),
            "deadline" => Ok(Self::Deadline),
            "supervisor-fault" => Ok(Self::SupervisorFault),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Control3RootVariant7Property0Reason {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Control3RootVariant7Property0Reason {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///`Control3RootVariant8Property0`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Control3RootVariant8Property0 {
    pub nonce: Control3RootVariant8Property0Nonce,
}
///`Control3RootVariant8Property0Nonce`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Control3RootVariant8Property0Nonce(::std::string::String);
impl ::std::ops::Deref for Control3RootVariant8Property0Nonce {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Control3RootVariant8Property0Nonce> for ::std::string::String {
    fn from(value: Control3RootVariant8Property0Nonce) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Control3RootVariant8Property0Nonce {
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
impl ::std::convert::TryFrom<&str> for Control3RootVariant8Property0Nonce {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Control3RootVariant8Property0Nonce {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Control3RootVariant8Property0Nonce {
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
///`Control3RootVariant9Property0`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Control3RootVariant9Property0 {
    pub nonce: Control3RootVariant9Property0Nonce,
    pub status: Control3RootVariant9Property0Status,
}
///`Control3RootVariant9Property0Nonce`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Control3RootVariant9Property0Nonce(::std::string::String);
impl ::std::ops::Deref for Control3RootVariant9Property0Nonce {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Control3RootVariant9Property0Nonce> for ::std::string::String {
    fn from(value: Control3RootVariant9Property0Nonce) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Control3RootVariant9Property0Nonce {
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
impl ::std::convert::TryFrom<&str> for Control3RootVariant9Property0Nonce {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Control3RootVariant9Property0Nonce {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Control3RootVariant9Property0Nonce {
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
///`Control3RootVariant9Property0Status`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Control3RootVariant9Property0Status {
    #[serde(rename = "ready")]
    Ready,
    #[serde(rename = "busy")]
    Busy,
    #[serde(rename = "stopping")]
    Stopping,
}
impl ::std::fmt::Display for Control3RootVariant9Property0Status {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::Ready => f.write_str("ready"),
            Self::Busy => f.write_str("busy"),
            Self::Stopping => f.write_str("stopping"),
        }
    }
}
impl ::std::str::FromStr for Control3RootVariant9Property0Status {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "ready" => Ok(Self::Ready),
            "busy" => Ok(Self::Busy),
            "stopping" => Ok(Self::Stopping),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Control3RootVariant9Property0Status {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Control3RootVariant9Property0Status {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///Host operational binding derived by dispatch from the actual Plan stage selected into THIS Analyze request. Not a protocol3 frame, not a worker field, not a new channel. FactBatch.stageId remains C-2 TEXT. Analyze may be a subset of execution-plan stages, so analyzeRequestOrdinal (contiguous in THIS Analyze) MUST NOT be equated with retainedStageOrdinal (execution-plan.stages[].ordinal). Host bind looks up the execution-plan row by retainedStageOrdinal and correlates the worker batch against expectedStageId / expectedAnalysisOrdinal / expectedBatchIndex / expectedFirstCandidateOrdinal.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Dispatch1Root {
    ///StageRequestV1.stageOrdinal / StageRequestV2.stageOrdinal: contiguous 0..n-1 in THIS Analyze request order. Provider Analyze may omit Plan stages, so this MAY differ from retainedStageOrdinal. Not echoed as FactBatch.stageId.
    #[serde(rename = "analyzeRequestOrdinal")]
    pub analyze_request_ordinal: u64,
    ///AnalyzeV1/AnalyzeV2.analysisOrdinal for this Analyze. Worker FactBatch.analysisOrdinal must equal this integer. Omitting this observation cannot be replaced by a caller scalar on the batch.
    #[serde(rename = "expectedAnalysisOrdinal")]
    pub expected_analysis_ordinal: u64,
    ///Contiguous batchIndex the host expects for this stage's next FactBatch (0..n-1 per requested stage).
    #[serde(rename = "expectedBatchIndex")]
    pub expected_batch_index: u64,
    ///candidateOrdinal of the first candidate in this batch. Batch 0 of a stage is 0. Later batches continue the per-stage candidate stream. Unique-increasing inside the batch is the candidateOrdinal array-order annotation; contiguous 0..n-1 across batches of one stage is a separate candidate-stream law.
    #[serde(rename = "expectedFirstCandidateOrdinal")]
    pub expected_first_candidate_ordinal: u64,
    ///Exact C-2 stageId text of the selected Plan stage (StageRequestV1.stageId; StageRequestV2.planStage.stageId). Worker FactBatch.stageId must byte-equal this text.
    #[serde(rename = "expectedStageId")]
    pub expected_stage_id: Dispatch1RootExpectedStageId,
    ///Retained Plan locator. Must equal execution-plan.planId and the stage-spec planId.
    #[serde(rename = "planId")]
    pub plan_id: ::std::string::String,
    ///Stage-spec producerClosure of the retained stage. Occupancy joins this producer, not EnumerationPlan enumerator.closureId.
    #[serde(rename = "producerClosure")]
    pub producer_closure: ::std::string::String,
    ///execution-plan.stages[].ordinal of the Plan stage this Analyze request selected. Host looks up the execution-plan row by this integer. Not FactBatch.stageId. Not analyzeRequestOrdinal.
    #[serde(rename = "retainedStageOrdinal")]
    pub retained_stage_ordinal: u64,
    #[serde(rename = "schemaVersion")]
    pub schema_version: ExactInteger,
    ///execution-plan.stages[retainedStageOrdinal].stageSpecDigest. Host re-derives producerClosure from the stage spec at this digest.
    #[serde(rename = "stageSpecDigest")]
    pub stage_spec_digest: ::std::string::String,
}
///Exact C-2 stageId text of the selected Plan stage (StageRequestV1.stageId; StageRequestV2.planStage.stageId). Worker FactBatch.stageId must byte-equal this text.
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Dispatch1RootExpectedStageId(::std::string::String);
impl ::std::ops::Deref for Dispatch1RootExpectedStageId {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Dispatch1RootExpectedStageId> for ::std::string::String {
    fn from(value: Dispatch1RootExpectedStageId) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Dispatch1RootExpectedStageId {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 255usize {
            return Err("longer than 255 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Dispatch1RootExpectedStageId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Dispatch1RootExpectedStageId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Dispatch1RootExpectedStageId {
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
///`FactBatch3PropertiesCandidatesItems`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct FactBatch3PropertiesCandidatesItems {
    pub anchors: ::std::vec::Vec<
        ::serde_json::Map<::std::string::String, ::serde_json::Value>,
    >,
    #[serde(rename = "candidateOrdinal")]
    pub candidate_ordinal: u64,
    ///JSON-vector transcription of FactCandidateV1.canonicalRelationPayload. Those wire bytes are deterministic-CBOR of the closed relation payload (fact-plane.v1 candidateSchema.transportRepresentation). The hex encodes those SAME CBOR bytes, not canonical JSON UTF-8. Admission requires hex == deterministic_cbor(decodedRelationPayload).hex().
    #[serde(rename = "canonicalRelationPayloadHex")]
    pub canonical_relation_payload_hex: FactBatch3PropertiesCandidatesItemsCanonicalRelationPayloadHex,
    #[serde(rename = "confidenceMillionths")]
    pub confidence_millionths: i64,
    ///Verified TCB observation of one decode of the CBOR payload bytes. Not a wire field. Must round-trip to canonicalRelationPayloadHex via fact-plane _deterministic_cbor.
    #[serde(rename = "decodedRelationPayload")]
    pub decoded_relation_payload: ::serde_json::Map<
        ::std::string::String,
        ::serde_json::Value,
    >,
    pub language: FactBatch3PropertiesCandidatesItemsLanguage,
    pub layer: FactBatch3PropertiesCandidatesItemsLayer,
    pub producer: FactBatch3PropertiesCandidatesItemsProducer,
    #[serde(rename = "producerVersion")]
    pub producer_version: FactBatch3PropertiesCandidatesItemsProducerVersion,
    pub relation: FactBatch3PropertiesCandidatesItemsRelation,
    #[serde(rename = "relationSchemaId")]
    pub relation_schema_id: FactBatch3PropertiesCandidatesItemsRelationSchemaId,
    pub resolution: FactBatch3PropertiesCandidatesItemsResolution,
    #[serde(rename = "schemaVersion")]
    pub schema_version: u64,
    #[serde(rename = "sourceUniverseId")]
    pub source_universe_id: FactBatch3PropertiesCandidatesItemsSourceUniverseId,
    #[serde(rename = "targetUniverseId")]
    pub target_universe_id: FactBatch3PropertiesCandidatesItemsTargetUniverseId,
}
///JSON-vector transcription of FactCandidateV1.canonicalRelationPayload. Those wire bytes are deterministic-CBOR of the closed relation payload (fact-plane.v1 candidateSchema.transportRepresentation). The hex encodes those SAME CBOR bytes, not canonical JSON UTF-8. Admission requires hex == deterministic_cbor(decodedRelationPayload).hex().
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct FactBatch3PropertiesCandidatesItemsCanonicalRelationPayloadHex(
    ::std::string::String,
);
impl ::std::ops::Deref
for FactBatch3PropertiesCandidatesItemsCanonicalRelationPayloadHex {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<FactBatch3PropertiesCandidatesItemsCanonicalRelationPayloadHex>
for ::std::string::String {
    fn from(
        value: FactBatch3PropertiesCandidatesItemsCanonicalRelationPayloadHex,
    ) -> Self {
        value.0
    }
}
impl ::std::str::FromStr
for FactBatch3PropertiesCandidatesItemsCanonicalRelationPayloadHex {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() < 2usize {
            return Err("shorter than 2 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str>
for FactBatch3PropertiesCandidatesItemsCanonicalRelationPayloadHex {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for FactBatch3PropertiesCandidatesItemsCanonicalRelationPayloadHex {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de>
for FactBatch3PropertiesCandidatesItemsCanonicalRelationPayloadHex {
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
///`FactBatch3PropertiesCandidatesItemsLanguage`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct FactBatch3PropertiesCandidatesItemsLanguage(::std::string::String);
impl ::std::ops::Deref for FactBatch3PropertiesCandidatesItemsLanguage {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<FactBatch3PropertiesCandidatesItemsLanguage>
for ::std::string::String {
    fn from(value: FactBatch3PropertiesCandidatesItemsLanguage) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for FactBatch3PropertiesCandidatesItemsLanguage {
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
impl ::std::convert::TryFrom<&str> for FactBatch3PropertiesCandidatesItemsLanguage {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for FactBatch3PropertiesCandidatesItemsLanguage {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for FactBatch3PropertiesCandidatesItemsLanguage {
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
///`FactBatch3PropertiesCandidatesItemsLayer`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct FactBatch3PropertiesCandidatesItemsLayer(::std::string::String);
impl ::std::ops::Deref for FactBatch3PropertiesCandidatesItemsLayer {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<FactBatch3PropertiesCandidatesItemsLayer>
for ::std::string::String {
    fn from(value: FactBatch3PropertiesCandidatesItemsLayer) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for FactBatch3PropertiesCandidatesItemsLayer {
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
impl ::std::convert::TryFrom<&str> for FactBatch3PropertiesCandidatesItemsLayer {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for FactBatch3PropertiesCandidatesItemsLayer {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for FactBatch3PropertiesCandidatesItemsLayer {
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
///`FactBatch3PropertiesCandidatesItemsProducer`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct FactBatch3PropertiesCandidatesItemsProducer(::std::string::String);
impl ::std::ops::Deref for FactBatch3PropertiesCandidatesItemsProducer {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<FactBatch3PropertiesCandidatesItemsProducer>
for ::std::string::String {
    fn from(value: FactBatch3PropertiesCandidatesItemsProducer) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for FactBatch3PropertiesCandidatesItemsProducer {
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
impl ::std::convert::TryFrom<&str> for FactBatch3PropertiesCandidatesItemsProducer {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for FactBatch3PropertiesCandidatesItemsProducer {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for FactBatch3PropertiesCandidatesItemsProducer {
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
///`FactBatch3PropertiesCandidatesItemsProducerVersion`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct FactBatch3PropertiesCandidatesItemsProducerVersion(::std::string::String);
impl ::std::ops::Deref for FactBatch3PropertiesCandidatesItemsProducerVersion {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<FactBatch3PropertiesCandidatesItemsProducerVersion>
for ::std::string::String {
    fn from(value: FactBatch3PropertiesCandidatesItemsProducerVersion) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for FactBatch3PropertiesCandidatesItemsProducerVersion {
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
impl ::std::convert::TryFrom<&str>
for FactBatch3PropertiesCandidatesItemsProducerVersion {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for FactBatch3PropertiesCandidatesItemsProducerVersion {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de>
for FactBatch3PropertiesCandidatesItemsProducerVersion {
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
///`FactBatch3PropertiesCandidatesItemsRelation`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct FactBatch3PropertiesCandidatesItemsRelation(::std::string::String);
impl ::std::ops::Deref for FactBatch3PropertiesCandidatesItemsRelation {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<FactBatch3PropertiesCandidatesItemsRelation>
for ::std::string::String {
    fn from(value: FactBatch3PropertiesCandidatesItemsRelation) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for FactBatch3PropertiesCandidatesItemsRelation {
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
impl ::std::convert::TryFrom<&str> for FactBatch3PropertiesCandidatesItemsRelation {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for FactBatch3PropertiesCandidatesItemsRelation {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for FactBatch3PropertiesCandidatesItemsRelation {
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
///`FactBatch3PropertiesCandidatesItemsRelationSchemaId`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct FactBatch3PropertiesCandidatesItemsRelationSchemaId(::std::string::String);
impl ::std::ops::Deref for FactBatch3PropertiesCandidatesItemsRelationSchemaId {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<FactBatch3PropertiesCandidatesItemsRelationSchemaId>
for ::std::string::String {
    fn from(value: FactBatch3PropertiesCandidatesItemsRelationSchemaId) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for FactBatch3PropertiesCandidatesItemsRelationSchemaId {
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
impl ::std::convert::TryFrom<&str>
for FactBatch3PropertiesCandidatesItemsRelationSchemaId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for FactBatch3PropertiesCandidatesItemsRelationSchemaId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de>
for FactBatch3PropertiesCandidatesItemsRelationSchemaId {
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
///`FactBatch3PropertiesCandidatesItemsResolution`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct FactBatch3PropertiesCandidatesItemsResolution(::std::string::String);
impl ::std::ops::Deref for FactBatch3PropertiesCandidatesItemsResolution {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<FactBatch3PropertiesCandidatesItemsResolution>
for ::std::string::String {
    fn from(value: FactBatch3PropertiesCandidatesItemsResolution) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for FactBatch3PropertiesCandidatesItemsResolution {
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
impl ::std::convert::TryFrom<&str> for FactBatch3PropertiesCandidatesItemsResolution {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for FactBatch3PropertiesCandidatesItemsResolution {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for FactBatch3PropertiesCandidatesItemsResolution {
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
///`FactBatch3PropertiesCandidatesItemsSourceUniverseId`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct FactBatch3PropertiesCandidatesItemsSourceUniverseId(::std::string::String);
impl ::std::ops::Deref for FactBatch3PropertiesCandidatesItemsSourceUniverseId {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<FactBatch3PropertiesCandidatesItemsSourceUniverseId>
for ::std::string::String {
    fn from(value: FactBatch3PropertiesCandidatesItemsSourceUniverseId) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for FactBatch3PropertiesCandidatesItemsSourceUniverseId {
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
for FactBatch3PropertiesCandidatesItemsSourceUniverseId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for FactBatch3PropertiesCandidatesItemsSourceUniverseId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de>
for FactBatch3PropertiesCandidatesItemsSourceUniverseId {
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
///`FactBatch3PropertiesCandidatesItemsTargetUniverseId`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct FactBatch3PropertiesCandidatesItemsTargetUniverseId(::std::string::String);
impl ::std::ops::Deref for FactBatch3PropertiesCandidatesItemsTargetUniverseId {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<FactBatch3PropertiesCandidatesItemsTargetUniverseId>
for ::std::string::String {
    fn from(value: FactBatch3PropertiesCandidatesItemsTargetUniverseId) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for FactBatch3PropertiesCandidatesItemsTargetUniverseId {
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
for FactBatch3PropertiesCandidatesItemsTargetUniverseId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for FactBatch3PropertiesCandidatesItemsTargetUniverseId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de>
for FactBatch3PropertiesCandidatesItemsTargetUniverseId {
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
///CURRENT selected FactBatch payload iff Hello/HelloAck negotiated target-attribution-v2. Preserves the historical rust-semantic FactBatchV2 field names analysisOrdinal, stageId, batchIndex, candidates (the typescript-semantic historical FactBatchV1 names its array facts and carries batchCommitment). Occupancy is a PARALLEL occupancyCompanions array, not a FactCandidateV1 field. stageId is TEXT: the worker echo of the current requested C-2 stageId (StageRequestV1.stageId; StageRequestV2.planStage.stageId). It is NOT Analyze stageOrdinal and NOT execution-plan.stages[].ordinal. Provider Analyze may be a subset of Plan stages; host DispatchBindingV1 carries retainedStageOrdinal separately. When the token is absent the historical per-language payload remains: typescript-semantic delivery.v2 FactBatchV1 {analysisOrdinal, stageId, batchIndex, facts, batchCommitment}; rust-semantic rust-provider-protocol.v2 FactBatchV2 {analysisOrdinal, stageId, batchIndex, candidates}. A V3 payload without the token, or that language's historical payload with the token, is PROVIDER.PROTOCOL_VIOLATION.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct FactBatch3Root {
    ///Exact echo of AnalyzeV1/AnalyzeV2.analysisOrdinal for this Analyze. Host correlates against DispatchBindingV1.expectedAnalysisOrdinal.
    #[serde(rename = "analysisOrdinal")]
    pub analysis_ordinal: u64,
    ///Contiguous from 0 for this requested stage, same as FactBatchV2. Host correlates against DispatchBindingV1.expectedBatchIndex.
    #[serde(rename = "batchIndex")]
    pub batch_index: u64,
    ///Non-empty closed FactCandidateV1 membership as a JSON vector. No occupancy field. Array-order token candidateOrdinal (published in occupancy-companion.schema.v1.json x-opensip-order-vocabulary and implemented by canonical.py): integer unique strictly increasing by candidateOrdinal; gaps lawful at this annotation. Contiguous 0..n-1 across batches of one requested stage is a separate candidate-stream law, joined to DispatchBindingV1.expectedFirstCandidateOrdinal. Arrays are not silently sorted.
    pub candidates: ::std::vec::Vec<FactBatch3RootCandidatesItem>,
    ///Zero or more OccupancyCompanionV1, each admitting as native/occupancy-companion.schema.v1.json including its allOf branches. Length <= candidates. Every candidateOrdinal names a candidate in this batch. Empty is lawful unknown except exact-id ephemeral. Same candidateOrdinal array-order token as candidates. Not silently sorted. This schema is independently complete via registered $ref; validators MUST resolve opensip.product.occupancy-companion.1 without mutating this dictionary at import time.
    #[serde(rename = "occupancyCompanions")]
    pub occupancy_companions: ::std::vec::Vec<Occupancy1Root>,
    #[serde(rename = "schemaVersion")]
    pub schema_version: ExactInteger,
    ///Historical FactBatchV1/V2.stageId preserved as C-2 TEXT. Worker echo of the current requested stage's C-2 stageId (delivery.v2 StageRequestV1.stageId; rust-provider-protocol StageRequestV2.planStage.stageId). Host correlates batch.stageId == DispatchBindingV1.expectedStageId. Do not treat this string as execution-plan.stages[].ordinal or as Analyze request stageOrdinal.
    #[serde(rename = "stageId")]
    pub stage_id: FactBatch3RootStageId,
}
///`FactBatch3RootCandidatesItem`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct FactBatch3RootCandidatesItem {
    pub anchors: ::std::vec::Vec<
        ::serde_json::Map<::std::string::String, ::serde_json::Value>,
    >,
    #[serde(rename = "candidateOrdinal")]
    pub candidate_ordinal: u64,
    ///JSON-vector transcription of FactCandidateV1.canonicalRelationPayload. Those wire bytes are deterministic-CBOR of the closed relation payload (fact-plane.v1 candidateSchema.transportRepresentation). The hex encodes those SAME CBOR bytes, not canonical JSON UTF-8. Admission requires hex == deterministic_cbor(decodedRelationPayload).hex().
    #[serde(rename = "canonicalRelationPayloadHex")]
    pub canonical_relation_payload_hex: FactBatch3RootCandidatesItemCanonicalRelationPayloadHex,
    #[serde(rename = "confidenceMillionths")]
    pub confidence_millionths: i64,
    ///Verified TCB observation of one decode of the CBOR payload bytes. Not a wire field. Must round-trip to canonicalRelationPayloadHex via fact-plane _deterministic_cbor.
    #[serde(rename = "decodedRelationPayload")]
    pub decoded_relation_payload: ::serde_json::Map<
        ::std::string::String,
        ::serde_json::Value,
    >,
    pub language: FactBatch3RootCandidatesItemLanguage,
    pub layer: FactBatch3RootCandidatesItemLayer,
    pub producer: FactBatch3RootCandidatesItemProducer,
    #[serde(rename = "producerVersion")]
    pub producer_version: FactBatch3RootCandidatesItemProducerVersion,
    pub relation: FactBatch3RootCandidatesItemRelation,
    #[serde(rename = "relationSchemaId")]
    pub relation_schema_id: FactBatch3RootCandidatesItemRelationSchemaId,
    pub resolution: FactBatch3RootCandidatesItemResolution,
    #[serde(rename = "schemaVersion")]
    pub schema_version: u64,
    #[serde(rename = "sourceUniverseId")]
    pub source_universe_id: FactBatch3RootCandidatesItemSourceUniverseId,
    #[serde(rename = "targetUniverseId")]
    pub target_universe_id: FactBatch3RootCandidatesItemTargetUniverseId,
}
///JSON-vector transcription of FactCandidateV1.canonicalRelationPayload. Those wire bytes are deterministic-CBOR of the closed relation payload (fact-plane.v1 candidateSchema.transportRepresentation). The hex encodes those SAME CBOR bytes, not canonical JSON UTF-8. Admission requires hex == deterministic_cbor(decodedRelationPayload).hex().
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct FactBatch3RootCandidatesItemCanonicalRelationPayloadHex(
    ::std::string::String,
);
impl ::std::ops::Deref for FactBatch3RootCandidatesItemCanonicalRelationPayloadHex {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<FactBatch3RootCandidatesItemCanonicalRelationPayloadHex>
for ::std::string::String {
    fn from(value: FactBatch3RootCandidatesItemCanonicalRelationPayloadHex) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for FactBatch3RootCandidatesItemCanonicalRelationPayloadHex {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() < 2usize {
            return Err("shorter than 2 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str>
for FactBatch3RootCandidatesItemCanonicalRelationPayloadHex {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for FactBatch3RootCandidatesItemCanonicalRelationPayloadHex {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de>
for FactBatch3RootCandidatesItemCanonicalRelationPayloadHex {
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
///`FactBatch3RootCandidatesItemLanguage`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct FactBatch3RootCandidatesItemLanguage(::std::string::String);
impl ::std::ops::Deref for FactBatch3RootCandidatesItemLanguage {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<FactBatch3RootCandidatesItemLanguage>
for ::std::string::String {
    fn from(value: FactBatch3RootCandidatesItemLanguage) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for FactBatch3RootCandidatesItemLanguage {
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
impl ::std::convert::TryFrom<&str> for FactBatch3RootCandidatesItemLanguage {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for FactBatch3RootCandidatesItemLanguage {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for FactBatch3RootCandidatesItemLanguage {
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
///`FactBatch3RootCandidatesItemLayer`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct FactBatch3RootCandidatesItemLayer(::std::string::String);
impl ::std::ops::Deref for FactBatch3RootCandidatesItemLayer {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<FactBatch3RootCandidatesItemLayer> for ::std::string::String {
    fn from(value: FactBatch3RootCandidatesItemLayer) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for FactBatch3RootCandidatesItemLayer {
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
impl ::std::convert::TryFrom<&str> for FactBatch3RootCandidatesItemLayer {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for FactBatch3RootCandidatesItemLayer {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for FactBatch3RootCandidatesItemLayer {
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
///`FactBatch3RootCandidatesItemProducer`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct FactBatch3RootCandidatesItemProducer(::std::string::String);
impl ::std::ops::Deref for FactBatch3RootCandidatesItemProducer {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<FactBatch3RootCandidatesItemProducer>
for ::std::string::String {
    fn from(value: FactBatch3RootCandidatesItemProducer) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for FactBatch3RootCandidatesItemProducer {
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
impl ::std::convert::TryFrom<&str> for FactBatch3RootCandidatesItemProducer {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for FactBatch3RootCandidatesItemProducer {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for FactBatch3RootCandidatesItemProducer {
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
///`FactBatch3RootCandidatesItemProducerVersion`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct FactBatch3RootCandidatesItemProducerVersion(::std::string::String);
impl ::std::ops::Deref for FactBatch3RootCandidatesItemProducerVersion {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<FactBatch3RootCandidatesItemProducerVersion>
for ::std::string::String {
    fn from(value: FactBatch3RootCandidatesItemProducerVersion) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for FactBatch3RootCandidatesItemProducerVersion {
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
impl ::std::convert::TryFrom<&str> for FactBatch3RootCandidatesItemProducerVersion {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for FactBatch3RootCandidatesItemProducerVersion {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for FactBatch3RootCandidatesItemProducerVersion {
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
///`FactBatch3RootCandidatesItemRelation`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct FactBatch3RootCandidatesItemRelation(::std::string::String);
impl ::std::ops::Deref for FactBatch3RootCandidatesItemRelation {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<FactBatch3RootCandidatesItemRelation>
for ::std::string::String {
    fn from(value: FactBatch3RootCandidatesItemRelation) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for FactBatch3RootCandidatesItemRelation {
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
impl ::std::convert::TryFrom<&str> for FactBatch3RootCandidatesItemRelation {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for FactBatch3RootCandidatesItemRelation {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for FactBatch3RootCandidatesItemRelation {
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
///`FactBatch3RootCandidatesItemRelationSchemaId`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct FactBatch3RootCandidatesItemRelationSchemaId(::std::string::String);
impl ::std::ops::Deref for FactBatch3RootCandidatesItemRelationSchemaId {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<FactBatch3RootCandidatesItemRelationSchemaId>
for ::std::string::String {
    fn from(value: FactBatch3RootCandidatesItemRelationSchemaId) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for FactBatch3RootCandidatesItemRelationSchemaId {
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
impl ::std::convert::TryFrom<&str> for FactBatch3RootCandidatesItemRelationSchemaId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for FactBatch3RootCandidatesItemRelationSchemaId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for FactBatch3RootCandidatesItemRelationSchemaId {
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
///`FactBatch3RootCandidatesItemResolution`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct FactBatch3RootCandidatesItemResolution(::std::string::String);
impl ::std::ops::Deref for FactBatch3RootCandidatesItemResolution {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<FactBatch3RootCandidatesItemResolution>
for ::std::string::String {
    fn from(value: FactBatch3RootCandidatesItemResolution) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for FactBatch3RootCandidatesItemResolution {
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
impl ::std::convert::TryFrom<&str> for FactBatch3RootCandidatesItemResolution {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for FactBatch3RootCandidatesItemResolution {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for FactBatch3RootCandidatesItemResolution {
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
///`FactBatch3RootCandidatesItemSourceUniverseId`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct FactBatch3RootCandidatesItemSourceUniverseId(::std::string::String);
impl ::std::ops::Deref for FactBatch3RootCandidatesItemSourceUniverseId {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<FactBatch3RootCandidatesItemSourceUniverseId>
for ::std::string::String {
    fn from(value: FactBatch3RootCandidatesItemSourceUniverseId) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for FactBatch3RootCandidatesItemSourceUniverseId {
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
impl ::std::convert::TryFrom<&str> for FactBatch3RootCandidatesItemSourceUniverseId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for FactBatch3RootCandidatesItemSourceUniverseId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for FactBatch3RootCandidatesItemSourceUniverseId {
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
///`FactBatch3RootCandidatesItemTargetUniverseId`
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct FactBatch3RootCandidatesItemTargetUniverseId(::std::string::String);
impl ::std::ops::Deref for FactBatch3RootCandidatesItemTargetUniverseId {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<FactBatch3RootCandidatesItemTargetUniverseId>
for ::std::string::String {
    fn from(value: FactBatch3RootCandidatesItemTargetUniverseId) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for FactBatch3RootCandidatesItemTargetUniverseId {
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
impl ::std::convert::TryFrom<&str> for FactBatch3RootCandidatesItemTargetUniverseId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for FactBatch3RootCandidatesItemTargetUniverseId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for FactBatch3RootCandidatesItemTargetUniverseId {
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
///Historical FactBatchV1/V2.stageId preserved as C-2 TEXT. Worker echo of the current requested stage's C-2 stageId (delivery.v2 StageRequestV1.stageId; rust-provider-protocol StageRequestV2.planStage.stageId). Host correlates batch.stageId == DispatchBindingV1.expectedStageId. Do not treat this string as execution-plan.stages[].ordinal or as Analyze request stageOrdinal.
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct FactBatch3RootStageId(::std::string::String);
impl ::std::ops::Deref for FactBatch3RootStageId {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<FactBatch3RootStageId> for ::std::string::String {
    fn from(value: FactBatch3RootStageId) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for FactBatch3RootStageId {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 255usize {
            return Err("longer than 255 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for FactBatch3RootStageId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for FactBatch3RootStageId {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for FactBatch3RootStageId {
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
///`Handshake1DigestHex`
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
pub struct Handshake1DigestHex(pub ::std::string::String);
impl ::std::ops::Deref for Handshake1DigestHex {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Handshake1DigestHex> for ::std::string::String {
    fn from(value: Handshake1DigestHex) -> Self {
        value.0
    }
}
impl ::std::convert::From<::std::string::String> for Handshake1DigestHex {
    fn from(value: ::std::string::String) -> Self {
        Self(value)
    }
}
impl ::std::fmt::Display for Handshake1DigestHex {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        self.0.fmt(f)
    }
}
impl ::std::str::FromStr for Handshake1DigestHex {
    type Err = ::std::convert::Infallible;
    fn from_str(value: &str) -> ::std::result::Result<Self, Self::Err> {
        Ok(Self(value.to_string()))
    }
}
///ExpectedRustIdentityV2 members unchanged except protocolMajor 3.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Handshake1ExpectedRustIdentityV3 {
    ///Selected Plan rust-v1 row hostTriple.
    #[serde(rename = "hostTriple")]
    pub host_triple: Handshake1IdentityText,
    #[serde(rename = "protocolMajor")]
    pub protocol_major: ExactInteger,
    ///Selected Plan rust-v1 row providerBuildId (verified signed release).
    #[serde(rename = "providerBuildId")]
    pub provider_build_id: Handshake1IdentityText,
    ///Selected Plan rust-v1 row rustCommitHash (resolved-inputs.v2 rust-v1 digestFields representation).
    #[serde(rename = "rustCommitHash")]
    pub rust_commit_hash: Handshake1DigestHex,
    ///Selected Plan rust-v1 row sysrootDigest.
    #[serde(rename = "sysrootDigest")]
    pub sysroot_digest: Handshake1DigestHex,
    ///Selected Plan rust-v1 row targetTriple.
    #[serde(rename = "targetTriple")]
    pub target_triple: Handshake1IdentityText,
}
///rust-semantic major-3 HelloAck. Every HelloAckV2 identity echo kept; protocolMajor 3; token array and identityVersions echoes.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Handshake1HelloAckV3 {
    ///Exact echo of Hello expectedCapabilities.
    pub capabilities: Handshake1RustCapabilitiesV3,
    ///HelloAckV2, unchanged: exact Hello expectedIdentity value.
    #[serde(rename = "hostTriple")]
    pub host_triple: Handshake1IdentityText,
    ///Exact echo of Hello identityVersions.
    #[serde(rename = "identityVersions")]
    pub identity_versions: Handshake1IdentityVersionsV1,
    #[serde(rename = "protocolMajor")]
    pub protocol_major: ExactInteger,
    ///HelloAckV2, unchanged: exact Hello expectedIdentity value.
    #[serde(rename = "providerBuildId")]
    pub provider_build_id: Handshake1IdentityText,
    ///HelloAckV2, unchanged: exact Hello expectedIdentity value.
    #[serde(rename = "rustCommitHash")]
    pub rust_commit_hash: Handshake1DigestHex,
    ///HelloAckV2, unchanged: exact Hello expectedIdentity value.
    #[serde(rename = "sysrootDigest")]
    pub sysroot_digest: Handshake1DigestHex,
    ///HelloAckV2, unchanged: exact Hello expectedIdentity value.
    #[serde(rename = "targetTriple")]
    pub target_triple: Handshake1IdentityText,
}
///rust-semantic major-3 Hello. Every HelloV2 member kept, capability record replaced by the token array, identityVersions added, limits ProtocolLimitsV3.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Handshake1HelloV3 {
    ///Replaces HelloV2 RustProviderCapabilityV2 with the section 9.1 token array (kept from the superseded HelloV3 definition).
    #[serde(rename = "expectedCapabilities")]
    pub expected_capabilities: Handshake1RustCapabilitiesV3,
    ///HelloV2 expectedIdentity, protocolMajor 3.
    #[serde(rename = "expectedIdentity")]
    pub expected_identity: Handshake1ExpectedRustIdentityV3,
    ///HelloV2, unchanged: raw SHA-256 of the exact bytes of docs/coop/artifacts/rust-provider-protocol.v2.json (x-opensip-wire-law expectedProtocolContractSha256).
    #[serde(rename = "expectedProtocolContractSha256")]
    pub expected_protocol_contract_sha256: Handshake1DigestHex,
    ///HelloV2, unchanged.
    #[serde(rename = "hostBuildId")]
    pub host_build_id: Handshake1IdentityText,
    ///Kept from the superseded HelloV3 definition.
    #[serde(rename = "identityVersions")]
    pub identity_versions: Handshake1IdentityVersionsV1,
    ///32-member closed map (section 9.3).
    pub limits: Handshake1ProtocolLimitsV3,
    #[serde(rename = "protocolMajor")]
    pub protocol_major: ExactInteger,
}
///rust-provider-protocol.v2 IdentityText: NFC, 1..4096 UTF-8 bytes, no C0/C1 control. NFC and the UTF-8 byte bound are checked by admission.
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Handshake1IdentityText(::std::string::String);
impl ::std::ops::Deref for Handshake1IdentityText {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Handshake1IdentityText> for ::std::string::String {
    fn from(value: Handshake1IdentityText) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Handshake1IdentityText {
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
impl ::std::convert::TryFrom<&str> for Handshake1IdentityText {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Handshake1IdentityText {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Handshake1IdentityText {
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
///native-evidence section 9.1 identity versions; HelloAck echoes the Hello value exactly.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Handshake1IdentityVersionsV1 {
    pub coverage: ExactInteger,
    pub fact: ExactInteger,
    pub plan: ExactInteger,
    pub snapshot: ExactInteger,
}
///delivery.v2 'non-empty NFC text' / 'verified descriptor text'. NFC is checked by admission.
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Handshake1NfcText(::std::string::String);
impl ::std::ops::Deref for Handshake1NfcText {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Handshake1NfcText> for ::std::string::String {
    fn from(value: Handshake1NfcText) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Handshake1NfcText {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Handshake1NfcText {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Handshake1NfcText {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Handshake1NfcText {
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
///rust-semantic HelloV3.limits: the 24 rust-provider-protocol.v2 limits members with identical values plus the eight native-evidence section 9.3 members (32). limitsHandshake semantic and deterministic-CBOR byte equality and limitPolicy apply unchanged.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Handshake1ProtocolLimitsV3 {
    #[serde(rename = "cancellationGraceMilliseconds")]
    pub cancellation_grace_milliseconds: ExactInteger,
    #[serde(rename = "maxAnalyzeStages")]
    pub max_analyze_stages: ExactInteger,
    #[serde(rename = "maxCandidateSpoolBytes")]
    pub max_candidate_spool_bytes: ExactInteger,
    #[serde(rename = "maxCanonicalRelationPayloadBytes")]
    pub max_canonical_relation_payload_bytes: ExactInteger,
    #[serde(rename = "maxCfgSets")]
    pub max_cfg_sets: ExactInteger,
    #[serde(rename = "maxCoverageEntriesPerFrame")]
    pub max_coverage_entries_per_frame: ExactInteger,
    #[serde(rename = "maxDependencySourceChunkBytes")]
    pub max_dependency_source_chunk_bytes: ExactInteger,
    #[serde(rename = "maxDependencySourceEntries")]
    pub max_dependency_source_entries: ExactInteger,
    #[serde(rename = "maxDependencySourcePackages")]
    pub max_dependency_source_packages: ExactInteger,
    #[serde(rename = "maxDependencySourceTotalBytes")]
    pub max_dependency_source_total_bytes: ExactInteger,
    #[serde(rename = "maxExpansionRows")]
    pub max_expansion_rows: ExactInteger,
    #[serde(rename = "maxFactBatchCandidates")]
    pub max_fact_batch_candidates: ExactInteger,
    #[serde(rename = "maxFactCandidatesTotal")]
    pub max_fact_candidates_total: ExactInteger,
    #[serde(rename = "maxFramePayloadBytes")]
    pub max_frame_payload_bytes: ExactInteger,
    #[serde(rename = "maxGeneratedFileRows")]
    pub max_generated_file_rows: ExactInteger,
    #[serde(rename = "maxPreparedOutputChunkBytes")]
    pub max_prepared_output_chunk_bytes: ExactInteger,
    #[serde(rename = "maxPreparedOutputEntries")]
    pub max_prepared_output_entries: ExactInteger,
    #[serde(rename = "maxPreparedOutputTotalBlobBytes")]
    pub max_prepared_output_total_blob_bytes: ExactInteger,
    #[serde(rename = "maxRelationsPerStage")]
    pub max_relations_per_stage: ExactInteger,
    #[serde(rename = "maxRequestFrames")]
    pub max_request_frames: ExactInteger,
    #[serde(rename = "maxRequestPayloadBytesTotal")]
    pub max_request_payload_bytes_total: ExactInteger,
    #[serde(rename = "maxRequestedCoverageKeysPerStage")]
    pub max_requested_coverage_keys_per_stage: ExactInteger,
    #[serde(rename = "maxResponseFrames")]
    pub max_response_frames: ExactInteger,
    #[serde(rename = "maxResponsePayloadBytesTotal")]
    pub max_response_payload_bytes_total: ExactInteger,
    #[serde(rename = "maxScratchBytes")]
    pub max_scratch_bytes: ExactInteger,
    #[serde(rename = "maxSnapshotChunkBytes")]
    pub max_snapshot_chunk_bytes: ExactInteger,
    #[serde(rename = "maxSnapshotEntries")]
    pub max_snapshot_entries: ExactInteger,
    #[serde(rename = "maxSnapshotTotalFileBytes")]
    pub max_snapshot_total_file_bytes: ExactInteger,
    #[serde(rename = "maxStderrBytes")]
    pub max_stderr_bytes: ExactInteger,
    #[serde(rename = "maxSubjectsPerStage")]
    pub max_subjects_per_stage: ExactInteger,
    #[serde(rename = "maxUnresolvedEdgesPerStage")]
    pub max_unresolved_edges_per_stage: ExactInteger,
    #[serde(rename = "normalExitGraceMilliseconds")]
    pub normal_exit_grace_milliseconds: ExactInteger,
}
///NORMATIVE field-level publication for native-evidence sections 9.1, 9.3, 9.4 and 9.6. HelloV3, HelloAckV3 and ProtocolLimitsV3 here SUPERSEDE the same-named $defs of native/native-evidence.schemas.v2.json, whose registered bytes are kept unchanged because that document's raw SHA-256 is a registered payloadSchemaDigest (native-evidence section 10); a byte change there would be a schema-document successor with re-registration. TypeScriptProtocolLimitsV1, TypeScriptHelloV2 and TypeScriptHelloAckV2 publish the typescript-semantic major-2 handshake. Every record is the JSON-vector form of a closed deterministic-CBOR map; handshake payloads carry no byte strings. Cross-record joins that a stock schema cannot express (descriptor digests and fields, identity and token echoes, contract digest, limit CBOR byte equality, candidate CBOR projection, TypeScript batch commitment) are executed by native/provider_wire_model.v1.py within that module's stated scope.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(transparent)]
pub struct Handshake1Root(pub ::serde_json::Value);
impl ::std::ops::Deref for Handshake1Root {
    type Target = ::serde_json::Value;
    fn deref(&self) -> &::serde_json::Value {
        &self.0
    }
}
impl ::std::convert::From<Handshake1Root> for ::serde_json::Value {
    fn from(value: Handshake1Root) -> Self {
        value.0
    }
}
impl ::std::convert::From<::serde_json::Value> for Handshake1Root {
    fn from(value: ::serde_json::Value) -> Self {
        Self(value)
    }
}
///rust-semantic token array: strictly unique ascending UTF-8 order, the four identity tokens present.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(transparent)]
pub struct Handshake1RustCapabilitiesV3(
    pub ::std::vec::Vec<Handshake1RustCapabilityToken>,
);
impl ::std::ops::Deref for Handshake1RustCapabilitiesV3 {
    type Target = ::std::vec::Vec<Handshake1RustCapabilityToken>;
    fn deref(&self) -> &::std::vec::Vec<Handshake1RustCapabilityToken> {
        &self.0
    }
}
impl ::std::convert::From<Handshake1RustCapabilitiesV3>
for ::std::vec::Vec<Handshake1RustCapabilityToken> {
    fn from(value: Handshake1RustCapabilitiesV3) -> Self {
        value.0
    }
}
impl ::std::convert::From<::std::vec::Vec<Handshake1RustCapabilityToken>>
for Handshake1RustCapabilitiesV3 {
    fn from(value: ::std::vec::Vec<Handshake1RustCapabilityToken>) -> Self {
        Self(value)
    }
}
///The rust-semantic members of native-evidence.schemas.v2.json#/$defs/CapabilityToken (section 9.1); typescript-semantic-facts-v1 is excluded.
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Handshake1RustCapabilityToken {
    #[serde(rename = "coverage-v3")]
    CoverageV3,
    #[serde(rename = "dependency-source-v1")]
    DependencySourceV1,
    #[serde(rename = "fact-identity-fact2")]
    FactIdentityFact2,
    #[serde(rename = "multi-stage-analyze-v1")]
    MultiStageAnalyzeV1,
    #[serde(rename = "native-context-v2")]
    NativeContextV2,
    #[serde(rename = "plan-identity-plan2")]
    PlanIdentityPlan2,
    #[serde(rename = "prepared-output-v3")]
    PreparedOutputV3,
    #[serde(rename = "resolution-completeness-v2")]
    ResolutionCompletenessV2,
    #[serde(rename = "rust-semantic-facts-v1")]
    RustSemanticFactsV1,
    #[serde(rename = "sealed-vfs-v1")]
    SealedVfsV1,
    #[serde(rename = "source-identity-snapshot2")]
    SourceIdentitySnapshot2,
    #[serde(rename = "target-attribution-v2")]
    TargetAttributionV2,
    #[serde(rename = "unresolved-edge-v1")]
    UnresolvedEdgeV1,
}
impl ::std::fmt::Display for Handshake1RustCapabilityToken {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::CoverageV3 => f.write_str("coverage-v3"),
            Self::DependencySourceV1 => f.write_str("dependency-source-v1"),
            Self::FactIdentityFact2 => f.write_str("fact-identity-fact2"),
            Self::MultiStageAnalyzeV1 => f.write_str("multi-stage-analyze-v1"),
            Self::NativeContextV2 => f.write_str("native-context-v2"),
            Self::PlanIdentityPlan2 => f.write_str("plan-identity-plan2"),
            Self::PreparedOutputV3 => f.write_str("prepared-output-v3"),
            Self::ResolutionCompletenessV2 => f.write_str("resolution-completeness-v2"),
            Self::RustSemanticFactsV1 => f.write_str("rust-semantic-facts-v1"),
            Self::SealedVfsV1 => f.write_str("sealed-vfs-v1"),
            Self::SourceIdentitySnapshot2 => f.write_str("source-identity-snapshot2"),
            Self::TargetAttributionV2 => f.write_str("target-attribution-v2"),
            Self::UnresolvedEdgeV1 => f.write_str("unresolved-edge-v1"),
        }
    }
}
impl ::std::str::FromStr for Handshake1RustCapabilityToken {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "coverage-v3" => Ok(Self::CoverageV3),
            "dependency-source-v1" => Ok(Self::DependencySourceV1),
            "fact-identity-fact2" => Ok(Self::FactIdentityFact2),
            "multi-stage-analyze-v1" => Ok(Self::MultiStageAnalyzeV1),
            "native-context-v2" => Ok(Self::NativeContextV2),
            "plan-identity-plan2" => Ok(Self::PlanIdentityPlan2),
            "prepared-output-v3" => Ok(Self::PreparedOutputV3),
            "resolution-completeness-v2" => Ok(Self::ResolutionCompletenessV2),
            "rust-semantic-facts-v1" => Ok(Self::RustSemanticFactsV1),
            "sealed-vfs-v1" => Ok(Self::SealedVfsV1),
            "source-identity-snapshot2" => Ok(Self::SourceIdentitySnapshot2),
            "target-attribution-v2" => Ok(Self::TargetAttributionV2),
            "unresolved-edge-v1" => Ok(Self::UnresolvedEdgeV1),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Handshake1RustCapabilityToken {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Handshake1RustCapabilityToken {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///JSON vector of the unchanged rust-semantic historical payload rust-provider-protocol.v2 FactBatchV2, admitted when target-attribution-v2 is not negotiated.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Handshake1RustFactBatchV2Vector {
    ///Exact Analyze analysisOrdinal echo.
    #[serde(rename = "analysisOrdinal")]
    pub analysis_ordinal: Handshake1Uint64,
    ///Contiguous from 0 for the stage.
    #[serde(rename = "batchIndex")]
    pub batch_index: Handshake1Uint64,
    ///Non-empty FactCandidateV1 JSON vectors with contiguous candidateOrdinal, length <= maxFactBatchCandidates.
    pub candidates: ::std::vec::Vec<FactBatch3PropertiesCandidatesItems>,
    ///StageRequestV2.planStage.stageId.
    #[serde(rename = "stageId")]
    pub stage_id: Handshake1StageIdText,
}
///`Handshake1Sha256Text`
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
pub struct Handshake1Sha256Text(pub ::std::string::String);
impl ::std::ops::Deref for Handshake1Sha256Text {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Handshake1Sha256Text> for ::std::string::String {
    fn from(value: Handshake1Sha256Text) -> Self {
        value.0
    }
}
impl ::std::convert::From<::std::string::String> for Handshake1Sha256Text {
    fn from(value: ::std::string::String) -> Self {
        Self(value)
    }
}
impl ::std::fmt::Display for Handshake1Sha256Text {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        self.0.fmt(f)
    }
}
impl ::std::str::FromStr for Handshake1Sha256Text {
    type Err = ::std::convert::Infallible;
    fn from_str(value: &str) -> ::std::result::Result<Self, Self::Err> {
        Ok(Self(value.to_string()))
    }
}
///C-2 stageId text, the historical FactBatchV1/V2 stageId type preserved on FactBatchV3.
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Handshake1StageIdText(::std::string::String);
impl ::std::ops::Deref for Handshake1StageIdText {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Handshake1StageIdText> for ::std::string::String {
    fn from(value: Handshake1StageIdText) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Handshake1StageIdText {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 255usize {
            return Err("longer than 255 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Handshake1StageIdText {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Handshake1StageIdText {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Handshake1StageIdText {
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
///typescript-semantic token array: strictly unique ascending UTF-8 order, the four identity tokens present.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(transparent)]
pub struct Handshake1TypeScriptCapabilitiesV2(
    pub ::std::vec::Vec<Handshake1TypeScriptCapabilityToken>,
);
impl ::std::ops::Deref for Handshake1TypeScriptCapabilitiesV2 {
    type Target = ::std::vec::Vec<Handshake1TypeScriptCapabilityToken>;
    fn deref(&self) -> &::std::vec::Vec<Handshake1TypeScriptCapabilityToken> {
        &self.0
    }
}
impl ::std::convert::From<Handshake1TypeScriptCapabilitiesV2>
for ::std::vec::Vec<Handshake1TypeScriptCapabilityToken> {
    fn from(value: Handshake1TypeScriptCapabilitiesV2) -> Self {
        value.0
    }
}
impl ::std::convert::From<::std::vec::Vec<Handshake1TypeScriptCapabilityToken>>
for Handshake1TypeScriptCapabilitiesV2 {
    fn from(value: ::std::vec::Vec<Handshake1TypeScriptCapabilityToken>) -> Self {
        Self(value)
    }
}
///The typescript-semantic members of native-evidence.schemas.v2.json#/$defs/CapabilityToken (section 9.1); the Rust-only dependency-source-v1, prepared-output-v3 and rust-semantic-facts-v1 are excluded (section 9.4).
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Handshake1TypeScriptCapabilityToken {
    #[serde(rename = "coverage-v3")]
    CoverageV3,
    #[serde(rename = "fact-identity-fact2")]
    FactIdentityFact2,
    #[serde(rename = "multi-stage-analyze-v1")]
    MultiStageAnalyzeV1,
    #[serde(rename = "native-context-v2")]
    NativeContextV2,
    #[serde(rename = "plan-identity-plan2")]
    PlanIdentityPlan2,
    #[serde(rename = "resolution-completeness-v2")]
    ResolutionCompletenessV2,
    #[serde(rename = "sealed-vfs-v1")]
    SealedVfsV1,
    #[serde(rename = "source-identity-snapshot2")]
    SourceIdentitySnapshot2,
    #[serde(rename = "target-attribution-v2")]
    TargetAttributionV2,
    #[serde(rename = "typescript-semantic-facts-v1")]
    TypescriptSemanticFactsV1,
    #[serde(rename = "unresolved-edge-v1")]
    UnresolvedEdgeV1,
}
impl ::std::fmt::Display for Handshake1TypeScriptCapabilityToken {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::CoverageV3 => f.write_str("coverage-v3"),
            Self::FactIdentityFact2 => f.write_str("fact-identity-fact2"),
            Self::MultiStageAnalyzeV1 => f.write_str("multi-stage-analyze-v1"),
            Self::NativeContextV2 => f.write_str("native-context-v2"),
            Self::PlanIdentityPlan2 => f.write_str("plan-identity-plan2"),
            Self::ResolutionCompletenessV2 => f.write_str("resolution-completeness-v2"),
            Self::SealedVfsV1 => f.write_str("sealed-vfs-v1"),
            Self::SourceIdentitySnapshot2 => f.write_str("source-identity-snapshot2"),
            Self::TargetAttributionV2 => f.write_str("target-attribution-v2"),
            Self::TypescriptSemanticFactsV1 => {
                f.write_str("typescript-semantic-facts-v1")
            }
            Self::UnresolvedEdgeV1 => f.write_str("unresolved-edge-v1"),
        }
    }
}
impl ::std::str::FromStr for Handshake1TypeScriptCapabilityToken {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "coverage-v3" => Ok(Self::CoverageV3),
            "fact-identity-fact2" => Ok(Self::FactIdentityFact2),
            "multi-stage-analyze-v1" => Ok(Self::MultiStageAnalyzeV1),
            "native-context-v2" => Ok(Self::NativeContextV2),
            "plan-identity-plan2" => Ok(Self::PlanIdentityPlan2),
            "resolution-completeness-v2" => Ok(Self::ResolutionCompletenessV2),
            "sealed-vfs-v1" => Ok(Self::SealedVfsV1),
            "source-identity-snapshot2" => Ok(Self::SourceIdentitySnapshot2),
            "target-attribution-v2" => Ok(Self::TargetAttributionV2),
            "typescript-semantic-facts-v1" => Ok(Self::TypescriptSemanticFactsV1),
            "unresolved-edge-v1" => Ok(Self::UnresolvedEdgeV1),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Handshake1TypeScriptCapabilityToken {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Handshake1TypeScriptCapabilityToken {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///JSON vector of the unchanged typescript-semantic historical payload delivery.v2 FactBatchV1, admitted when target-attribution-v2 is not negotiated.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Handshake1TypeScriptFactBatchV1Vector {
    #[serde(rename = "analysisOrdinal")]
    pub analysis_ordinal: ExactInteger,
    ///sha256 under domain opensip.ts-provider.fact-batch.v1 over deterministic-CBOR of the wire facts array.
    #[serde(rename = "batchCommitment")]
    pub batch_commitment: Handshake1Sha256Text,
    ///Contiguous from 0 for the stage.
    #[serde(rename = "batchIndex")]
    pub batch_index: Handshake1Uint64,
    ///Non-empty ordered FactCandidateV1 JSON vectors, length <= maxFactBatchFacts.
    pub facts: ::std::vec::Vec<FactBatch3PropertiesCandidatesItems>,
    ///Current requested stage (StageRequestV1.stageId).
    #[serde(rename = "stageId")]
    pub stage_id: Handshake1StageIdText,
}
///typescript-semantic major-2 HelloAck. Every HelloAckV1 member kept, including all provider/runtime descriptor verification; protocolMajor 1 -> 2 and the fixed capability array -> the negotiated echo; identityVersions added.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Handshake1TypeScriptHelloAckV2 {
    ///HelloAckV1 fixed three-token array replaced by the exact echo of Hello expectedCapabilities.
    pub capabilities: Handshake1TypeScriptCapabilitiesV2,
    ///HelloAckV1, unchanged.
    #[serde(rename = "defaultWorkBudgetProfileId")]
    pub default_work_budget_profile_id: ::serde_json::Value,
    ///HelloAckV1, unchanged.
    #[serde(rename = "defaultWorkBudgetProfileSha256")]
    pub default_work_budget_profile_sha256: ::serde_json::Value,
    ///Added: exact echo of Hello identityVersions.
    #[serde(rename = "identityVersions")]
    pub identity_versions: Handshake1IdentityVersionsV1,
    ///HelloAckV1, unchanged: verified runtime descriptor value.
    #[serde(rename = "modulesAbi")]
    pub modules_abi: Handshake1NfcText,
    ///HelloAckV1, unchanged: verified runtime descriptor value.
    #[serde(rename = "nodeVersion")]
    pub node_version: Handshake1NfcText,
    ///HelloAckV1, unchanged: selected release platformId, equal to the verified runtime descriptor value.
    #[serde(rename = "platformId")]
    pub platform_id: Handshake1NfcText,
    #[serde(rename = "protocolMajor")]
    pub protocol_major: ExactInteger,
    ///HelloAckV1, unchanged: verified provider descriptor value.
    #[serde(rename = "providerBuildId")]
    pub provider_build_id: Handshake1NfcText,
    ///HelloAckV1, unchanged: equals Hello expectedProviderDescriptorSha256.
    #[serde(rename = "providerDescriptorSha256")]
    pub provider_descriptor_sha256: Handshake1DigestHex,
    ///HelloAckV1, unchanged: equals Hello expectedRuntimeDescriptorSha256.
    #[serde(rename = "runtimeDescriptorSha256")]
    pub runtime_descriptor_sha256: Handshake1DigestHex,
    ///HelloAckV1, unchanged: verified provider descriptor value.
    #[serde(rename = "typescriptCompilerSha256")]
    pub typescript_compiler_sha256: Handshake1DigestHex,
    ///HelloAckV1, unchanged: verified provider descriptor value.
    #[serde(rename = "typescriptStdlibMerkleRoot")]
    pub typescript_stdlib_merkle_root: Handshake1DigestHex,
    ///HelloAckV1, unchanged: verified provider descriptor value.
    #[serde(rename = "typescriptVersion")]
    pub typescript_version: Handshake1NfcText,
    ///HelloAckV1, unchanged: verified runtime descriptor value.
    #[serde(rename = "v8Version")]
    pub v8_version: Handshake1NfcText,
}
///typescript-semantic major-2 Hello. Every HelloV1 member unchanged plus expectedCapabilities and identityVersions. No payload protocolMajor; the envelope protocolMajor is exactly 2.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Handshake1TypeScriptHelloV2 {
    ///Added: the selected signed capability row's tokens (section 9.1).
    #[serde(rename = "expectedCapabilities")]
    pub expected_capabilities: Handshake1TypeScriptCapabilitiesV2,
    ///HelloV1, unchanged: raw SHA-256 of the RFC 8785 bytes of the verified signed typescript-provider/identity.json.
    #[serde(rename = "expectedProviderDescriptorSha256")]
    pub expected_provider_descriptor_sha256: Handshake1DigestHex,
    ///HelloV1, unchanged: raw SHA-256 of the RFC 8785 bytes of the verified signed typescript-runtime/identity.json.
    #[serde(rename = "expectedRuntimeDescriptorSha256")]
    pub expected_runtime_descriptor_sha256: Handshake1DigestHex,
    ///HelloV1 hostBuildId, unchanged.
    #[serde(rename = "hostBuildId")]
    pub host_build_id: Handshake1NfcText,
    ///Added (section 9.1).
    #[serde(rename = "identityVersions")]
    pub identity_versions: Handshake1IdentityVersionsV1,
    ///HelloV1 'closed map equal to wireSchema.limits numeric fields', unchanged.
    pub limits: Handshake1TypeScriptProtocolLimitsV1,
}
///Exactly the ten numeric members of delivery.v2 typescriptSemanticSubstrate.providerProtocol.wireSchema.limits with identical values; limitRule is policy text and never a member.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Handshake1TypeScriptProtocolLimitsV1 {
    #[serde(rename = "maxAnalyzeStages")]
    pub max_analyze_stages: ExactInteger,
    #[serde(rename = "maxCoverageEntriesPerFrame")]
    pub max_coverage_entries_per_frame: ExactInteger,
    #[serde(rename = "maxFactBatchFacts")]
    pub max_fact_batch_facts: ExactInteger,
    #[serde(rename = "maxFactCandidatePayloadBytes")]
    pub max_fact_candidate_payload_bytes: ExactInteger,
    #[serde(rename = "maxFramePayloadBytes")]
    pub max_frame_payload_bytes: ExactInteger,
    #[serde(rename = "maxRelationsPerStage")]
    pub max_relations_per_stage: ExactInteger,
    #[serde(rename = "maxRequestedCoverageKeysPerStage")]
    pub max_requested_coverage_keys_per_stage: ExactInteger,
    #[serde(rename = "maxSnapshotChunkBytes")]
    pub max_snapshot_chunk_bytes: ExactInteger,
    #[serde(rename = "maxSnapshotEntries")]
    pub max_snapshot_entries: ExactInteger,
    #[serde(rename = "maxStderrBytes")]
    pub max_stderr_bytes: ExactInteger,
}
///`Handshake1Uint64`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(transparent)]
pub struct Handshake1Uint64(pub u64);
impl ::std::ops::Deref for Handshake1Uint64 {
    type Target = u64;
    fn deref(&self) -> &u64 {
        &self.0
    }
}
impl ::std::convert::From<Handshake1Uint64> for u64 {
    fn from(value: Handshake1Uint64) -> Self {
        value.0
    }
}
impl ::std::convert::From<u64> for Handshake1Uint64 {
    fn from(value: u64) -> Self {
        Self(value)
    }
}
impl ::std::fmt::Display for Handshake1Uint64 {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        self.0.fmt(f)
    }
}
impl ::std::str::FromStr for Handshake1Uint64 {
    type Err = <u64 as ::std::str::FromStr>::Err;
    fn from_str(value: &str) -> ::std::result::Result<Self, Self::Err> {
        Ok(Self(value.parse()?))
    }
}
impl ::std::convert::TryFrom<&str> for Handshake1Uint64 {
    type Error = <u64 as ::std::str::FromStr>::Err;
    fn try_from(value: &str) -> ::std::result::Result<Self, Self::Error> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<String> for Handshake1Uint64 {
    type Error = <u64 as ::std::str::FromStr>::Err;
    fn try_from(value: String) -> ::std::result::Result<Self, Self::Error> {
        value.parse()
    }
}
///rust-semantic BudgetExhausted: BudgetExhaustedV2 members, CoverageResultV3 coverage.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Startup1BudgetExhaustedV3 {
    #[serde(rename = "analysisOrdinal")]
    pub analysis_ordinal: Startup1Uint64,
    ///CoverageResultV3 in stage-major/key order; entry k belongs to the stage whose cumulative requested-key range contains k.
    pub coverage: ::std::vec::Vec<Native2CoverageResultV3>,
    #[serde(rename = "coverageCommitment")]
    pub coverage_commitment: Startup1Sha256Text,
    pub limit: Startup1Uint64,
    pub observed: Startup1Uint64,
    #[serde(rename = "triggerStageId")]
    pub trigger_stage_id: Startup1StageIdText,
    pub unit: Startup1BudgetExhaustedV3Unit,
}
///`Startup1BudgetExhaustedV3Unit`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Startup1BudgetExhaustedV3Unit {
    #[serde(rename = "work-units")]
    WorkUnits,
    #[serde(rename = "bytes")]
    Bytes,
    #[serde(rename = "items")]
    Items,
}
impl ::std::fmt::Display for Startup1BudgetExhaustedV3Unit {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::WorkUnits => f.write_str("work-units"),
            Self::Bytes => f.write_str("bytes"),
            Self::Items => f.write_str("items"),
        }
    }
}
impl ::std::str::FromStr for Startup1BudgetExhaustedV3Unit {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "work-units" => Ok(Self::WorkUnits),
            "bytes" => Ok(Self::Bytes),
            "items" => Ok(Self::Items),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Startup1BudgetExhaustedV3Unit {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Startup1BudgetExhaustedV3Unit {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///rust-semantic frame CoverageV3 payload: CoverageV2 wrapper with CoverageResultV3 entries.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Startup1CoverageV3 {
    #[serde(rename = "analysisOrdinal")]
    pub analysis_ordinal: Startup1Uint64,
    #[serde(rename = "coverageCommitment")]
    pub coverage_commitment: Startup1Sha256Text,
    ///entries[i] answers requestedCoverageDomain.keys[i] of the attributed stage; CoverageResultV3 is the entry type, never the frame.
    pub entries: ::std::vec::Vec<Native2CoverageResultV3>,
    #[serde(rename = "stageId")]
    pub stage_id: Startup1StageIdText,
}
///`Startup1DigestHex`
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
pub struct Startup1DigestHex(pub ::std::string::String);
impl ::std::ops::Deref for Startup1DigestHex {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Startup1DigestHex> for ::std::string::String {
    fn from(value: Startup1DigestHex) -> Self {
        value.0
    }
}
impl ::std::convert::From<::std::string::String> for Startup1DigestHex {
    fn from(value: ::std::string::String) -> Self {
        Self(value)
    }
}
impl ::std::fmt::Display for Startup1DigestHex {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        self.0.fmt(f)
    }
}
impl ::std::str::FromStr for Startup1DigestHex {
    type Err = ::std::convert::Infallible;
    fn from_str(value: &str) -> ::std::result::Result<Self, Self::Err> {
        Ok(Self(value.to_string()))
    }
}
///host-allocated ExecutionId text, exact AttemptRecord value (rust-semantic IdentityText rules checked by admission)
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Startup1ExecutionIdText(::std::string::String);
impl ::std::ops::Deref for Startup1ExecutionIdText {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Startup1ExecutionIdText> for ::std::string::String {
    fn from(value: Startup1ExecutionIdText) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Startup1ExecutionIdText {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Startup1ExecutionIdText {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Startup1ExecutionIdText {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Startup1ExecutionIdText {
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
///native-evidence 9.2 NativeContextVerified payload, both languages.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Startup1NativeContextVerifiedV1 {
    pub equal: ::serde_json::Value,
    #[serde(rename = "nativeContextId")]
    pub native_context_id: Startup1Sha256Text,
    #[serde(rename = "recomputedNativeContextId")]
    pub recomputed_native_context_id: Startup1Sha256Text,
}
///non-empty text; NFC is checked by admission
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Startup1NfcText(::std::string::String);
impl ::std::ops::Deref for Startup1NfcText {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Startup1NfcText> for ::std::string::String {
    fn from(value: Startup1NfcText) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Startup1NfcText {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Startup1NfcText {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Startup1NfcText {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Startup1NfcText {
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
///rust-semantic major-3 OpenUniverse: OpenUniverseV2 members with successor types; no mode booleans.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Startup1OpenUniverseV3 {
    #[serde(rename = "executionId")]
    pub execution_id: Startup1ExecutionIdText,
    #[serde(rename = "planId")]
    pub plan_id: Startup1PlanId2,
    #[serde(rename = "planIntentCommitment")]
    pub plan_intent_commitment: Startup1Sha256Text,
    #[serde(rename = "providerId")]
    pub provider_id: ::serde_json::Value,
    #[serde(rename = "repositoryResolution")]
    pub repository_resolution: Native2RepositoryResolutionV3,
    #[serde(rename = "snapshotId")]
    pub snapshot_id: Startup1SnapshotId2,
    pub universe: Startup1RustSemanticUniverseV2,
}
///`Startup1PlanId2`
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
pub struct Startup1PlanId2(pub ::std::string::String);
impl ::std::ops::Deref for Startup1PlanId2 {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Startup1PlanId2> for ::std::string::String {
    fn from(value: Startup1PlanId2) -> Self {
        value.0
    }
}
impl ::std::convert::From<::std::string::String> for Startup1PlanId2 {
    fn from(value: ::std::string::String) -> Self {
        Self(value)
    }
}
impl ::std::fmt::Display for Startup1PlanId2 {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        self.0.fmt(f)
    }
}
impl ::std::str::FromStr for Startup1PlanId2 {
    type Err = ::std::convert::Infallible;
    fn from_str(value: &str) -> ::std::result::Result<Self, Self::Err> {
        Ok(Self(value.to_string()))
    }
}
///Pre-Analyze Unavailable payload, both languages; only in the NativeContextVerified interval; carries no requested stage or coverage.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Startup1PreAnalyzeUnavailableV1 {
    #[serde(rename = "executionId")]
    pub execution_id: Startup1ExecutionIdText,
    #[serde(rename = "nativeContextId")]
    pub native_context_id: Startup1Sha256Text,
    #[serde(rename = "planId")]
    pub plan_id: Startup1PlanId2,
    pub reason: ::serde_json::Value,
    #[serde(rename = "recomputedNativeContextId")]
    pub recomputed_native_context_id: Startup1Sha256Text,
    #[serde(rename = "snapshotId")]
    pub snapshot_id: Startup1SnapshotId2,
}
///Closed JSON-vector records of deterministic-CBOR wire maps for OpenUniverse, UniverseAccepted, NativeContextVerified, pre-Analyze Unavailable, Coverage and terminal coverage payloads. Entry records CoverageResultV3, RepositoryResolutionV3 and the v2 resolvedInputs are referenced from the registered bundle by $id and are not redefined.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(transparent)]
pub struct Startup1Root(pub ::serde_json::Value);
impl ::std::ops::Deref for Startup1Root {
    type Target = ::serde_json::Value;
    fn deref(&self) -> &::serde_json::Value {
        &self.0
    }
}
impl ::std::convert::From<Startup1Root> for ::serde_json::Value {
    fn from(value: Startup1Root) -> Self {
        value.0
    }
}
impl ::std::convert::From<::serde_json::Value> for Startup1Root {
    fn from(value: ::serde_json::Value) -> Self {
        Self(value)
    }
}
///The resolved-inputs.v2 rust-v1 map with resolvedInputs replaced by RustUniverseV2ResolvedInputs and protocolMajor 3; every other member, constant and digest representation unchanged.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Startup1RustSemanticUniverseV2 {
    #[serde(rename = "capabilityManifestId")]
    pub capability_manifest_id: Startup1DigestHex,
    #[serde(rename = "cargoVersion")]
    pub cargo_version: Startup1NfcText,
    #[serde(rename = "hostTriple")]
    pub host_triple: Startup1NfcText,
    #[serde(rename = "licenseNoticeBundleSha256")]
    pub license_notice_bundle_sha256: Startup1DigestHex,
    #[serde(rename = "manifestId")]
    pub manifest_id: Startup1DigestHex,
    #[serde(rename = "platformId")]
    pub platform_id: Startup1NfcText,
    #[serde(rename = "protocolMajor")]
    pub protocol_major: ExactInteger,
    #[serde(rename = "providerArtifactId")]
    pub provider_artifact_id: ::serde_json::Value,
    #[serde(rename = "providerArtifactSha256")]
    pub provider_artifact_sha256: Startup1DigestHex,
    #[serde(rename = "providerBinarySha256")]
    pub provider_binary_sha256: Startup1DigestHex,
    #[serde(rename = "providerBuildId")]
    pub provider_build_id: Startup1NfcText,
    #[serde(rename = "resolvedInputs")]
    pub resolved_inputs: Native2RustUniverseV2ResolvedInputs,
    #[serde(rename = "rustCommitHash")]
    pub rust_commit_hash: Startup1DigestHex,
    #[serde(rename = "rustcDevLlvmDigest")]
    pub rustc_dev_llvm_digest: Startup1DigestHex,
    #[serde(rename = "rustcVersion")]
    pub rustc_version: Startup1NfcText,
    #[serde(rename = "schemaVersion")]
    pub schema_version: ExactInteger,
    ///component name -> 64-hex digest (rust-v1 digestRepresentation)
    #[serde(rename = "standardLibraryComponentDigests")]
    pub standard_library_component_digests: ::std::collections::BTreeMap<
        ::std::string::String,
        Startup1DigestHex,
    >,
    #[serde(rename = "sysrootDigest")]
    pub sysroot_digest: Startup1DigestHex,
    #[serde(rename = "targetTriple")]
    pub target_triple: Startup1NfcText,
    #[serde(rename = "toolchainArtifactId")]
    pub toolchain_artifact_id: ::serde_json::Value,
    #[serde(rename = "toolchainArtifactSha256")]
    pub toolchain_artifact_sha256: Startup1DigestHex,
}
///`Startup1Sha256Text`
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
pub struct Startup1Sha256Text(pub ::std::string::String);
impl ::std::ops::Deref for Startup1Sha256Text {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Startup1Sha256Text> for ::std::string::String {
    fn from(value: Startup1Sha256Text) -> Self {
        value.0
    }
}
impl ::std::convert::From<::std::string::String> for Startup1Sha256Text {
    fn from(value: ::std::string::String) -> Self {
        Self(value)
    }
}
impl ::std::fmt::Display for Startup1Sha256Text {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        self.0.fmt(f)
    }
}
impl ::std::str::FromStr for Startup1Sha256Text {
    type Err = ::std::convert::Infallible;
    fn from_str(value: &str) -> ::std::result::Result<Self, Self::Err> {
        Ok(Self(value.to_string()))
    }
}
///`Startup1SnapshotId2`
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
pub struct Startup1SnapshotId2(pub ::std::string::String);
impl ::std::ops::Deref for Startup1SnapshotId2 {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Startup1SnapshotId2> for ::std::string::String {
    fn from(value: Startup1SnapshotId2) -> Self {
        value.0
    }
}
impl ::std::convert::From<::std::string::String> for Startup1SnapshotId2 {
    fn from(value: ::std::string::String) -> Self {
        Self(value)
    }
}
impl ::std::fmt::Display for Startup1SnapshotId2 {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        self.0.fmt(f)
    }
}
impl ::std::str::FromStr for Startup1SnapshotId2 {
    type Err = ::std::convert::Infallible;
    fn from_str(value: &str) -> ::std::result::Result<Self, Self::Err> {
        Ok(Self(value.to_string()))
    }
}
///C-2 stageId text
#[derive(::serde::Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct Startup1StageIdText(::std::string::String);
impl ::std::ops::Deref for Startup1StageIdText {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<Startup1StageIdText> for ::std::string::String {
    fn from(value: Startup1StageIdText) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for Startup1StageIdText {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() > 255usize {
            return Err("longer than 255 characters".into());
        }
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Startup1StageIdText {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Startup1StageIdText {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for Startup1StageIdText {
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
///typescript-semantic BudgetExhausted: BudgetExhaustedV1 members, CoverageResultV3 coverage.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Startup1TypeScriptBudgetExhaustedV2 {
    #[serde(rename = "analysisOrdinal")]
    pub analysis_ordinal: ExactInteger,
    ///CoverageResultV3 in stage-major/key order; entry k belongs to the stage whose cumulative requested-key range contains k.
    pub coverage: ::std::vec::Vec<Native2CoverageResultV3>,
    #[serde(rename = "coverageCommitment")]
    pub coverage_commitment: Startup1Sha256Text,
    pub dimension: Startup1TypeScriptBudgetExhaustedV2Dimension,
    pub limit: Startup1Uint64,
    pub observed: Startup1Uint64,
    #[serde(rename = "triggerStageId")]
    pub trigger_stage_id: Startup1StageIdText,
}
///`Startup1TypeScriptBudgetExhaustedV2Dimension`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Startup1TypeScriptBudgetExhaustedV2Dimension {
    #[serde(rename = "sourceFilesVisited")]
    SourceFilesVisited,
    #[serde(rename = "astNodesVisited")]
    AstNodesVisited,
    #[serde(rename = "moduleResolutionQueries")]
    ModuleResolutionQueries,
    #[serde(rename = "typeQueries")]
    TypeQueries,
    #[serde(rename = "factsEmitted")]
    FactsEmitted,
    #[serde(rename = "factBytesEmitted")]
    FactBytesEmitted,
}
impl ::std::fmt::Display for Startup1TypeScriptBudgetExhaustedV2Dimension {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::SourceFilesVisited => f.write_str("sourceFilesVisited"),
            Self::AstNodesVisited => f.write_str("astNodesVisited"),
            Self::ModuleResolutionQueries => f.write_str("moduleResolutionQueries"),
            Self::TypeQueries => f.write_str("typeQueries"),
            Self::FactsEmitted => f.write_str("factsEmitted"),
            Self::FactBytesEmitted => f.write_str("factBytesEmitted"),
        }
    }
}
impl ::std::str::FromStr for Startup1TypeScriptBudgetExhaustedV2Dimension {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "sourceFilesVisited" => Ok(Self::SourceFilesVisited),
            "astNodesVisited" => Ok(Self::AstNodesVisited),
            "moduleResolutionQueries" => Ok(Self::ModuleResolutionQueries),
            "typeQueries" => Ok(Self::TypeQueries),
            "factsEmitted" => Ok(Self::FactsEmitted),
            "factBytesEmitted" => Ok(Self::FactBytesEmitted),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Startup1TypeScriptBudgetExhaustedV2Dimension {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Startup1TypeScriptBudgetExhaustedV2Dimension {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///typescript-semantic frame Coverage payload: CoverageV1 wrapper with CoverageResultV3 entries.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Startup1TypeScriptCoverageV2 {
    #[serde(rename = "analysisOrdinal")]
    pub analysis_ordinal: ExactInteger,
    #[serde(rename = "coverageCommitment")]
    pub coverage_commitment: Startup1Sha256Text,
    ///entries[i] answers requestedCoverageDomain.keys[i] of the attributed stage; CoverageResultV3 is the entry type, never the frame.
    pub entries: ::std::vec::Vec<Native2CoverageResultV3>,
    #[serde(rename = "stageId")]
    pub stage_id: Startup1StageIdText,
}
///typescript-semantic major-2 OpenUniverse: OpenUniverseV1 members with successor types.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Startup1TypeScriptOpenUniverseV2 {
    #[serde(rename = "executionId")]
    pub execution_id: Startup1ExecutionIdText,
    #[serde(rename = "planId")]
    pub plan_id: Startup1PlanId2,
    #[serde(rename = "planIntentCommitment")]
    pub plan_intent_commitment: Startup1Sha256Text,
    #[serde(rename = "providerId")]
    pub provider_id: ::serde_json::Value,
    #[serde(rename = "snapshotId")]
    pub snapshot_id: Startup1SnapshotId2,
    pub universe: Startup1TypeScriptSemanticUniverseV2,
    #[serde(rename = "universeKey")]
    pub universe_key: Startup1Sha256Text,
}
///The resolved-inputs.v2 typescript-v1 map with resolvedInputs replaced by TypeScriptUniverseV2ResolvedInputs and protocolMajor 2; every other member, constant and digest representation unchanged.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Startup1TypeScriptSemanticUniverseV2 {
    #[serde(rename = "capabilityManifestId")]
    pub capability_manifest_id: Startup1DigestHex,
    #[serde(rename = "manifestId")]
    pub manifest_id: Startup1DigestHex,
    #[serde(rename = "modulesAbi")]
    pub modules_abi: Startup1NfcText,
    #[serde(rename = "nodeVersion")]
    pub node_version: Startup1NfcText,
    #[serde(rename = "platformId")]
    pub platform_id: Startup1NfcText,
    #[serde(rename = "protocolMajor")]
    pub protocol_major: ExactInteger,
    #[serde(rename = "providerArtifactId")]
    pub provider_artifact_id: ::serde_json::Value,
    #[serde(rename = "providerArtifactSha256")]
    pub provider_artifact_sha256: Startup1DigestHex,
    #[serde(rename = "providerBuildId")]
    pub provider_build_id: Startup1NfcText,
    #[serde(rename = "providerDescriptorSha256")]
    pub provider_descriptor_sha256: Startup1DigestHex,
    #[serde(rename = "resolvedInputs")]
    pub resolved_inputs: Native2TypeScriptUniverseV2ResolvedInputs,
    #[serde(rename = "runtimeArtifactId")]
    pub runtime_artifact_id: ::serde_json::Value,
    #[serde(rename = "runtimeArtifactSha256")]
    pub runtime_artifact_sha256: Startup1DigestHex,
    #[serde(rename = "runtimeDescriptorSha256")]
    pub runtime_descriptor_sha256: Startup1DigestHex,
    #[serde(rename = "schemaVersion")]
    pub schema_version: ExactInteger,
    #[serde(rename = "typescriptCompilerSha256")]
    pub typescript_compiler_sha256: Startup1DigestHex,
    #[serde(rename = "typescriptStdlibMerkleRoot")]
    pub typescript_stdlib_merkle_root: Startup1DigestHex,
    #[serde(rename = "typescriptVersion")]
    pub typescript_version: Startup1NfcText,
    #[serde(rename = "v8Version")]
    pub v8_version: Startup1NfcText,
}
///typescript-semantic post-Analyze Unavailable (immediately after Analyze): UnavailableV1 members, CoverageResultV3 coverage, reason never native-context-mismatch.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Startup1TypeScriptUnavailableV2 {
    ///all requested stageIds in request order (inherited)
    #[serde(rename = "affectedStageIds")]
    pub affected_stage_ids: ::std::vec::Vec<Startup1StageIdText>,
    #[serde(rename = "analysisOrdinal")]
    pub analysis_ordinal: ExactInteger,
    ///CoverageResultV3 in stage-major/key order; entry k belongs to the stage whose cumulative requested-key range contains k.
    pub coverage: ::std::vec::Vec<Native2CoverageResultV3>,
    #[serde(rename = "coverageCommitment")]
    pub coverage_commitment: Startup1Sha256Text,
    pub reason: Startup1TypeScriptUnavailableV2Reason,
}
///`Startup1TypeScriptUnavailableV2Reason`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Startup1TypeScriptUnavailableV2Reason {
    #[serde(rename = "capability-missing")]
    CapabilityMissing,
    #[serde(rename = "identity-version-mismatch")]
    IdentityVersionMismatch,
    #[serde(rename = "node-modules-outside-read-set")]
    NodeModulesOutsideReadSet,
    #[serde(rename = "semantic-universe-incomplete")]
    SemanticUniverseIncomplete,
    #[serde(rename = "snapshot-resolution-input-missing")]
    SnapshotResolutionInputMissing,
    #[serde(rename = "unsupported-compiler-mode")]
    UnsupportedCompilerMode,
}
impl ::std::fmt::Display for Startup1TypeScriptUnavailableV2Reason {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::CapabilityMissing => f.write_str("capability-missing"),
            Self::IdentityVersionMismatch => f.write_str("identity-version-mismatch"),
            Self::NodeModulesOutsideReadSet => {
                f.write_str("node-modules-outside-read-set")
            }
            Self::SemanticUniverseIncomplete => {
                f.write_str("semantic-universe-incomplete")
            }
            Self::SnapshotResolutionInputMissing => {
                f.write_str("snapshot-resolution-input-missing")
            }
            Self::UnsupportedCompilerMode => f.write_str("unsupported-compiler-mode"),
        }
    }
}
impl ::std::str::FromStr for Startup1TypeScriptUnavailableV2Reason {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "capability-missing" => Ok(Self::CapabilityMissing),
            "identity-version-mismatch" => Ok(Self::IdentityVersionMismatch),
            "node-modules-outside-read-set" => Ok(Self::NodeModulesOutsideReadSet),
            "semantic-universe-incomplete" => Ok(Self::SemanticUniverseIncomplete),
            "snapshot-resolution-input-missing" => {
                Ok(Self::SnapshotResolutionInputMissing)
            }
            "unsupported-compiler-mode" => Ok(Self::UnsupportedCompilerMode),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Startup1TypeScriptUnavailableV2Reason {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
for Startup1TypeScriptUnavailableV2Reason {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///typescript-semantic major-2 UniverseAccepted: UniverseAcceptedV1 members; universeKey is the worker recomputation.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Startup1TypeScriptUniverseAcceptedV2 {
    #[serde(rename = "executionId")]
    pub execution_id: Startup1ExecutionIdText,
    #[serde(rename = "planId")]
    pub plan_id: Startup1PlanId2,
    #[serde(rename = "snapshotId")]
    pub snapshot_id: Startup1SnapshotId2,
    #[serde(rename = "universeKey")]
    pub universe_key: Startup1Sha256Text,
}
///`Startup1Uint64`
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(transparent)]
pub struct Startup1Uint64(pub u64);
impl ::std::ops::Deref for Startup1Uint64 {
    type Target = u64;
    fn deref(&self) -> &u64 {
        &self.0
    }
}
impl ::std::convert::From<Startup1Uint64> for u64 {
    fn from(value: Startup1Uint64) -> Self {
        value.0
    }
}
impl ::std::convert::From<u64> for Startup1Uint64 {
    fn from(value: u64) -> Self {
        Self(value)
    }
}
impl ::std::fmt::Display for Startup1Uint64 {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        self.0.fmt(f)
    }
}
impl ::std::str::FromStr for Startup1Uint64 {
    type Err = <u64 as ::std::str::FromStr>::Err;
    fn from_str(value: &str) -> ::std::result::Result<Self, Self::Err> {
        Ok(Self(value.parse()?))
    }
}
impl ::std::convert::TryFrom<&str> for Startup1Uint64 {
    type Error = <u64 as ::std::str::FromStr>::Err;
    fn try_from(value: &str) -> ::std::result::Result<Self, Self::Error> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<String> for Startup1Uint64 {
    type Error = <u64 as ::std::str::FromStr>::Err;
    fn try_from(value: String) -> ::std::result::Result<Self, Self::Error> {
        value.parse()
    }
}
///rust-semantic post-Analyze Unavailable (P3-25): UnavailableV2 members, CoverageResultV3 coverage, reason never native-context-mismatch.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Startup1UnavailableV3 {
    ///all requested stageIds in request order (inherited)
    #[serde(rename = "affectedStageIds")]
    pub affected_stage_ids: ::std::vec::Vec<Startup1StageIdText>,
    #[serde(rename = "analysisOrdinal")]
    pub analysis_ordinal: Startup1Uint64,
    ///CoverageResultV3 in stage-major/key order; entry k belongs to the stage whose cumulative requested-key range contains k.
    pub coverage: ::std::vec::Vec<Native2CoverageResultV3>,
    #[serde(rename = "coverageCommitment")]
    pub coverage_commitment: Startup1Sha256Text,
    pub reason: Startup1UnavailableV3Reason,
}
///`Startup1UnavailableV3Reason`
#[derive(
    ::serde::Deserialize,
    ::serde::Serialize,
    Clone,
    Copy,
    Debug,
    Eq,
    Hash,
    Ord,
    PartialEq,
    PartialOrd
)]
pub enum Startup1UnavailableV3Reason {
    #[serde(rename = "capability-missing")]
    CapabilityMissing,
    #[serde(rename = "dependency-source-incomplete")]
    DependencySourceIncomplete,
    #[serde(rename = "generated-cfg-unavailable")]
    GeneratedCfgUnavailable,
    #[serde(rename = "identity-version-mismatch")]
    IdentityVersionMismatch,
    #[serde(rename = "prepared-output-not-inert")]
    PreparedOutputNotInert,
    #[serde(rename = "prepared-output-stale")]
    PreparedOutputStale,
    #[serde(rename = "semantic-universe-incomplete")]
    SemanticUniverseIncomplete,
    #[serde(rename = "snapshot-resolution-input-missing")]
    SnapshotResolutionInputMissing,
    #[serde(rename = "unsupported-compiler-mode")]
    UnsupportedCompilerMode,
}
impl ::std::fmt::Display for Startup1UnavailableV3Reason {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        match *self {
            Self::CapabilityMissing => f.write_str("capability-missing"),
            Self::DependencySourceIncomplete => {
                f.write_str("dependency-source-incomplete")
            }
            Self::GeneratedCfgUnavailable => f.write_str("generated-cfg-unavailable"),
            Self::IdentityVersionMismatch => f.write_str("identity-version-mismatch"),
            Self::PreparedOutputNotInert => f.write_str("prepared-output-not-inert"),
            Self::PreparedOutputStale => f.write_str("prepared-output-stale"),
            Self::SemanticUniverseIncomplete => {
                f.write_str("semantic-universe-incomplete")
            }
            Self::SnapshotResolutionInputMissing => {
                f.write_str("snapshot-resolution-input-missing")
            }
            Self::UnsupportedCompilerMode => f.write_str("unsupported-compiler-mode"),
        }
    }
}
impl ::std::str::FromStr for Startup1UnavailableV3Reason {
    type Err = self::error::ConversionError;
    fn from_str(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "capability-missing" => Ok(Self::CapabilityMissing),
            "dependency-source-incomplete" => Ok(Self::DependencySourceIncomplete),
            "generated-cfg-unavailable" => Ok(Self::GeneratedCfgUnavailable),
            "identity-version-mismatch" => Ok(Self::IdentityVersionMismatch),
            "prepared-output-not-inert" => Ok(Self::PreparedOutputNotInert),
            "prepared-output-stale" => Ok(Self::PreparedOutputStale),
            "semantic-universe-incomplete" => Ok(Self::SemanticUniverseIncomplete),
            "snapshot-resolution-input-missing" => {
                Ok(Self::SnapshotResolutionInputMissing)
            }
            "unsupported-compiler-mode" => Ok(Self::UnsupportedCompilerMode),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Startup1UnavailableV3Reason {
    type Error = self::error::ConversionError;
    fn try_from(
        value: &str,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Startup1UnavailableV3Reason {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
///rust-semantic major-3 UniverseAccepted: exact recursive echo of OpenUniverseV3 members.
#[derive(::serde::Deserialize, ::serde::Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Startup1UniverseAcceptedV3 {
    #[serde(rename = "executionId")]
    pub execution_id: Startup1ExecutionIdText,
    #[serde(rename = "planId")]
    pub plan_id: Startup1PlanId2,
    #[serde(rename = "providerId")]
    pub provider_id: ::serde_json::Value,
    #[serde(rename = "repositoryResolution")]
    pub repository_resolution: Native2RepositoryResolutionV3,
    #[serde(rename = "snapshotId")]
    pub snapshot_id: Startup1SnapshotId2,
    pub universe: Startup1RustSemanticUniverseV2,
}

// Native07 inert carrier integration.

/// Owned inert byte carrier. The bounded CBOR decoder must check major type 2
/// and declared lengths before allocation; this serde bridge is not that codec.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct ByteString(Vec<u8>);
impl ByteString {
    pub fn from_vec(value: Vec<u8>) -> Self { Self(value) }
    pub fn as_slice(&self) -> &[u8] { &self.0 }
    pub fn into_vec(self) -> Vec<u8> { self.0 }
}
impl serde::Serialize for ByteString {
    fn serialize<S: serde::Serializer>(&self, serializer: S) -> Result<S::Ok, S::Error> {
        serializer.serialize_bytes(&self.0)
    }
}
impl<'de> serde::Deserialize<'de> for ByteString {
    fn deserialize<D: serde::Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        struct Bytes;
        impl<'de> serde::de::Visitor<'de> for Bytes {
            type Value = ByteString;
            fn expecting(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
                f.write_str("a byte string, not a sequence or text")
            }
            fn visit_bytes<E: serde::de::Error>(self, value: &[u8]) -> Result<Self::Value, E> {
                Ok(ByteString(value.to_vec()))
            }
            fn visit_byte_buf<E: serde::de::Error>(self, value: Vec<u8>) -> Result<Self::Value, E> {
                Ok(ByteString(value))
            }
        }
        // CBOR is self-describing. deserialize_byte_buf lets serde_json coerce
        // a text value into bytes; deserialize_any preserves the source kind.
        deserializer.deserialize_any(Bytes)
    }
}
fn required_value<'de, D, T>(deserializer: D) -> Result<T, D::Error>
where D: serde::Deserializer<'de>, T: serde::Deserialize<'de> {
    T::deserialize(deserializer)
}
// Tagged records do not use serde's Content buffer: it coerces empty maps to
// unit and byte strings to text. Keep each input's scalar kind until the actual
// text discriminator is known. Complex variant members are unselected here.
struct StrictMapKey(String);
impl<'de> serde::Deserialize<'de> for StrictMapKey {
    fn deserialize<D: serde::Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        struct Key;
        impl<'de> serde::de::Visitor<'de> for Key {
            type Value = StrictMapKey;
            fn expecting(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result { f.write_str("a text map key") }
            fn visit_str<E: serde::de::Error>(self, v: &str) -> Result<Self::Value, E> { Ok(StrictMapKey(v.to_owned())) }
            fn visit_string<E: serde::de::Error>(self, v: String) -> Result<Self::Value, E> { Ok(StrictMapKey(v)) }
        }
        deserializer.deserialize_any(Key)
    }
}
enum WireScalar { Text(String), Unsigned(u64), Bytes(ByteString), Bool(bool), Null }
impl<'de> serde::Deserialize<'de> for WireScalar {
    fn deserialize<D: serde::Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        struct Scalar;
        impl<'de> serde::de::Visitor<'de> for Scalar {
            type Value = WireScalar;
            fn expecting(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result { f.write_str("a native wire scalar") }
            fn visit_str<E: serde::de::Error>(self, v: &str) -> Result<Self::Value, E> { Ok(WireScalar::Text(v.to_owned())) }
            fn visit_string<E: serde::de::Error>(self, v: String) -> Result<Self::Value, E> { Ok(WireScalar::Text(v)) }
            fn visit_u64<E: serde::de::Error>(self, v: u64) -> Result<Self::Value, E> { Ok(WireScalar::Unsigned(v)) }
            fn visit_bytes<E: serde::de::Error>(self, v: &[u8]) -> Result<Self::Value, E> { Ok(WireScalar::Bytes(ByteString::from_vec(v.to_vec()))) }
            fn visit_byte_buf<E: serde::de::Error>(self, v: Vec<u8>) -> Result<Self::Value, E> { Ok(WireScalar::Bytes(ByteString::from_vec(v))) }
            fn visit_bool<E: serde::de::Error>(self, v: bool) -> Result<Self::Value, E> { Ok(WireScalar::Bool(v)) }
            fn visit_unit<E: serde::de::Error>(self) -> Result<Self::Value, E> { Ok(WireScalar::Null) }
        }
        deserializer.deserialize_any(Scalar)
    }
}
impl WireScalar {
    fn into_text<E: serde::de::Error>(self) -> Result<String, E> {
        match self { Self::Text(v) => Ok(v), _ => Err(E::custom("expected text scalar")) }
    }
    fn into_unsigned<E: serde::de::Error>(self) -> Result<u64, E> {
        match self { Self::Unsigned(v) => Ok(v), _ => Err(E::custom("expected unsigned scalar")) }
    }
    fn into_bytes<E: serde::de::Error>(self) -> Result<ByteString, E> {
        match self { Self::Bytes(v) => Ok(v), _ => Err(E::custom("expected byte string scalar")) }
    }
    fn into_bool<E: serde::de::Error>(self) -> Result<bool, E> {
        match self { Self::Bool(v) => Ok(v), _ => Err(E::custom("expected boolean scalar")) }
    }
    fn into_null<E: serde::de::Error>(self) -> Result<(), E> {
        match self { Self::Null => Ok(()), _ => Err(E::custom("expected null scalar")) }
    }
}
pub type Ts2DigestHex = String;

pub type Ts2Sha256Text = String;

pub type Ts2NfcText = String;

pub type Ts2StageIdText = String;

pub type Ts2SnapshotId2 = String;

pub type Ts2PlanId2 = String;

pub type Ts2ExecutionIdText = String;

pub type Ts2ProjectPath = String;

pub type Rust3IdentityText = String;

pub type Rust3DigestHex = String;

pub type Rust3Sha256Text = String;

pub type Rust3CanonicalPath = String;

pub type Rust3DependencySourcePath = String;

pub type Rust3StageIdText = String;

pub type Rust3SnapshotId2 = String;

pub type Rust3PlanId2 = String;

pub type Rust3CanonicalIdentifier = String;

pub type Rust3PackageKey = String;

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
pub enum Ts2FrameV2Field1Value {
#[serde(rename = "Analyze")]
Analyze,
#[serde(rename = "BudgetExhausted")]
BudgetExhausted,
#[serde(rename = "Cancel")]
Cancel,
#[serde(rename = "Cancelled")]
Cancelled,
#[serde(rename = "Complete")]
Complete,
#[serde(rename = "Coverage")]
Coverage,
#[serde(rename = "FactBatch")]
FactBatch,
#[serde(rename = "Hello")]
Hello,
#[serde(rename = "HelloAck")]
HelloAck,
#[serde(rename = "NativeContextVerified")]
NativeContextVerified,
#[serde(rename = "OpenUniverse")]
OpenUniverse,
#[serde(rename = "SnapshotAccepted")]
SnapshotAccepted,
#[serde(rename = "SnapshotFileChunk")]
SnapshotFileChunk,
#[serde(rename = "SnapshotManifest")]
SnapshotManifest,
#[serde(rename = "SnapshotSeal")]
SnapshotSeal,
#[serde(rename = "Unavailable")]
Unavailable,
#[serde(rename = "UniverseAccepted")]
UniverseAccepted,
}

#[derive(Clone, Debug)]
pub struct Ts2FrameV2 {
pub protocol_major: u64,
pub frame_type: Ts2FrameV2Field1Value,
pub sequence: u64,
pub payload: Ts2FrameV2Payload,
}

#[derive(Clone, Debug, serde::Serialize)]
#[serde(tag = "kind", deny_unknown_fields)]
pub enum Ts2SnapshotEntryV1 {
#[serde(rename = "file")]
File {
#[serde(rename = "path")]
path: Ts2ProjectPath,
#[serde(rename = "byteLength")]
byte_length: u64,
#[serde(rename = "contentSha256")]
content_sha256: Ts2DigestHex,
#[serde(rename = "linkTarget")]
link_target: (),
},
#[serde(rename = "symlink")]
Symlink {
#[serde(rename = "path")]
path: Ts2ProjectPath,
#[serde(rename = "byteLength")]
byte_length: u64,
#[serde(rename = "contentSha256")]
content_sha256: (),
#[serde(rename = "linkTarget")]
link_target: String,
},
}


impl<'de> serde::Deserialize<'de> for Ts2SnapshotEntryV1 {
    fn deserialize<D: serde::Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        struct Record;
        impl<'de> serde::de::Visitor<'de> for Record {
            type Value = Ts2SnapshotEntryV1;
            fn expecting(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result { f.write_str("a tagged native record with text keys") }
            fn visit_map<A: serde::de::MapAccess<'de>>(self, mut map: A) -> Result<Self::Value, A::Error> {
                let mut values: [Option<WireScalar>; 5] = std::array::from_fn(|_| None);
                while let Some(key) = map.next_key::<StrictMapKey>()? {
                    let index = match key.0.as_str() { "path" => 0,"kind" => 1,"byteLength" => 2,"contentSha256" => 3,"linkTarget" => 4, _ => return Err(serde::de::Error::unknown_field(&key.0, &["path","kind","byteLength","contentSha256","linkTarget"])) };
                    if values[index].is_some() { return Err(serde::de::Error::custom("duplicate native record member")); }
                    values[index] = Some(map.next_value::<WireScalar>()?);
                }
                let tag = values[1].take().ok_or_else(|| serde::de::Error::missing_field("kind"))?.into_text::<A::Error>()?;
                match tag.as_str() { "file" => Ok(Ts2SnapshotEntryV1::File { path: serde::Deserialize::deserialize(serde::de::value::StringDeserializer::<A::Error>::new(values[0].take().ok_or_else(|| serde::de::Error::missing_field("path"))?.into_text::<A::Error>()?))?,byte_length: values[2].take().ok_or_else(|| serde::de::Error::missing_field("byteLength"))?.into_unsigned::<A::Error>()?,content_sha256: serde::Deserialize::deserialize(serde::de::value::StringDeserializer::<A::Error>::new(values[3].take().ok_or_else(|| serde::de::Error::missing_field("contentSha256"))?.into_text::<A::Error>()?))?,link_target: values[4].take().ok_or_else(|| serde::de::Error::missing_field("linkTarget"))?.into_null::<A::Error>()? }),"symlink" => Ok(Ts2SnapshotEntryV1::Symlink { path: serde::Deserialize::deserialize(serde::de::value::StringDeserializer::<A::Error>::new(values[0].take().ok_or_else(|| serde::de::Error::missing_field("path"))?.into_text::<A::Error>()?))?,byte_length: values[2].take().ok_or_else(|| serde::de::Error::missing_field("byteLength"))?.into_unsigned::<A::Error>()?,content_sha256: values[3].take().ok_or_else(|| serde::de::Error::missing_field("contentSha256"))?.into_null::<A::Error>()?,link_target: serde::Deserialize::deserialize(serde::de::value::StringDeserializer::<A::Error>::new(values[4].take().ok_or_else(|| serde::de::Error::missing_field("linkTarget"))?.into_text::<A::Error>()?))? }), _ => Err(serde::de::Error::unknown_variant(&tag, &["file","symlink"])) }
            }
        }
        deserializer.deserialize_map(Record)
    }
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Ts2SnapshotManifestV1 {
#[serde(rename = "snapshotId")]
pub snapshot_id: Ts2SnapshotId2,
#[serde(rename = "manifestSha256")]
pub manifest_sha256: Ts2DigestHex,
#[serde(rename = "entries")]
pub entries: Vec<Ts2SnapshotEntryV1>,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Ts2SnapshotFileChunkV1 {
#[serde(rename = "snapshotId")]
pub snapshot_id: Ts2SnapshotId2,
#[serde(rename = "path")]
pub path: Ts2ProjectPath,
#[serde(rename = "chunkIndex")]
pub chunk_index: u64,
#[serde(rename = "byteOffset")]
pub byte_offset: u64,
#[serde(rename = "bytes")]
pub bytes: ByteString,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Ts2SnapshotSealV1 {
#[serde(rename = "snapshotId")]
pub snapshot_id: Ts2SnapshotId2,
#[serde(rename = "manifestSha256")]
pub manifest_sha256: Ts2DigestHex,
#[serde(rename = "entryCount")]
pub entry_count: u64,
#[serde(rename = "totalFileBytes")]
pub total_file_bytes: u64,
#[serde(rename = "totalChunkCount")]
pub total_chunk_count: u64,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Ts2SnapshotAcceptedV1 {
#[serde(rename = "snapshotId")]
pub snapshot_id: Ts2SnapshotId2,
#[serde(rename = "manifestSha256")]
pub manifest_sha256: Ts2DigestHex,
#[serde(rename = "entryCount")]
pub entry_count: u64,
#[serde(rename = "totalFileBytes")]
pub total_file_bytes: u64,
#[serde(rename = "totalChunkCount")]
pub total_chunk_count: u64,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Ts2ProviderWorkBudgetV1 {
#[serde(rename = "sourceFilesVisited")]
pub source_files_visited: u64,
#[serde(rename = "astNodesVisited")]
pub ast_nodes_visited: u64,
#[serde(rename = "moduleResolutionQueries")]
pub module_resolution_queries: u64,
#[serde(rename = "typeQueries")]
pub type_queries: u64,
#[serde(rename = "factsEmitted")]
pub facts_emitted: u64,
#[serde(rename = "factBytesEmitted")]
pub fact_bytes_emitted: u64,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
pub enum Ts2SubjectScopeV1Field0Value {
#[serde(rename = "all-snapshot-files")]
AllSnapshotFiles,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Ts2SubjectScopeV1 {
#[serde(rename = "scopeKind")]
pub scope_kind: Ts2SubjectScopeV1Field0Value,
#[serde(rename = "snapshotId")]
pub snapshot_id: Ts2SnapshotId2,
#[serde(rename = "subjectCount")]
pub subject_count: u64,
#[serde(rename = "subjectScopeCommitment")]
pub subject_scope_commitment: Ts2Sha256Text,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
pub enum Ts2CoverageKeyV1Field5Value {
#[serde(rename = "typescript-semantic")]
TypescriptSemantic,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Ts2CoverageKeyV1 {
#[serde(rename = "relation")]
pub relation: Native2Relation,
#[serde(rename = "resolution")]
pub resolution: Native2Rung,
#[serde(rename = "sourceUniverseId")]
pub source_universe_id: Ts2Sha256Text,
#[serde(rename = "targetUniverseId")]
pub target_universe_id: Ts2Sha256Text,
#[serde(rename = "subjectScopeCommitment")]
pub subject_scope_commitment: Ts2Sha256Text,
#[serde(rename = "producer")]
pub producer: Ts2CoverageKeyV1Field5Value,
#[serde(rename = "producerVersion")]
pub producer_version: Ts2NfcText,
#[serde(rename = "schemaVersion")]
pub schema_version: u64,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Ts2RequestedCoverageDomainV1 {
#[serde(rename = "subjectScope")]
pub subject_scope: Ts2SubjectScopeV1,
#[serde(rename = "keys")]
pub keys: Vec<Ts2CoverageKeyV1>,
#[serde(rename = "domainCommitment")]
pub domain_commitment: Ts2Sha256Text,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
pub enum Ts2StageRequestV1Field2Value {
#[serde(rename = "semantic-provider")]
SemanticProvider,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
pub enum Ts2StageRequestV1Field3Value {
#[serde(rename = "typescript-semantic")]
TypescriptSemantic,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Ts2StageRequestV1 {
#[serde(rename = "stageId")]
pub stage_id: Ts2StageIdText,
#[serde(rename = "stageOrdinal")]
pub stage_ordinal: u64,
#[serde(rename = "operator")]
pub operator: Ts2StageRequestV1Field2Value,
#[serde(rename = "providerId")]
pub provider_id: Ts2StageRequestV1Field3Value,
#[serde(rename = "dependsOn")]
pub depends_on: Vec<Ts2StageIdText>,
#[serde(rename = "relations")]
pub relations: Vec<Native2Relation>,
#[serde(rename = "budget")]
pub budget: Ts2ProviderWorkBudgetV1,
#[serde(rename = "requestedCoverageDomain")]
pub requested_coverage_domain: Ts2RequestedCoverageDomainV1,
}

#[derive(Clone, Debug, serde::Serialize)]
#[serde(tag = "kind", deny_unknown_fields)]
pub enum Ts2AnchorRefV1 {
#[serde(rename = "source-span")]
SourceSpan {
#[serde(rename = "snapshotId")]
snapshot_id: Ts2SnapshotId2,
#[serde(rename = "path")]
path: Ts2ProjectPath,
#[serde(rename = "contentSha256")]
content_sha256: Ts2DigestHex,
#[serde(rename = "startByte")]
start_byte: u64,
#[serde(rename = "endByte")]
end_byte: u64,
#[serde(rename = "factId")]
fact_id: (),
},
#[serde(rename = "fact-ref")]
FactRef {
#[serde(rename = "snapshotId")]
snapshot_id: (),
#[serde(rename = "path")]
path: (),
#[serde(rename = "contentSha256")]
content_sha256: (),
#[serde(rename = "startByte")]
start_byte: (),
#[serde(rename = "endByte")]
end_byte: (),
#[serde(rename = "factId")]
fact_id: String,
},
}


impl<'de> serde::Deserialize<'de> for Ts2AnchorRefV1 {
    fn deserialize<D: serde::Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        struct Record;
        impl<'de> serde::de::Visitor<'de> for Record {
            type Value = Ts2AnchorRefV1;
            fn expecting(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result { f.write_str("a tagged native record with text keys") }
            fn visit_map<A: serde::de::MapAccess<'de>>(self, mut map: A) -> Result<Self::Value, A::Error> {
                let mut values: [Option<WireScalar>; 7] = std::array::from_fn(|_| None);
                while let Some(key) = map.next_key::<StrictMapKey>()? {
                    let index = match key.0.as_str() { "kind" => 0,"snapshotId" => 1,"path" => 2,"contentSha256" => 3,"startByte" => 4,"endByte" => 5,"factId" => 6, _ => return Err(serde::de::Error::unknown_field(&key.0, &["kind","snapshotId","path","contentSha256","startByte","endByte","factId"])) };
                    if values[index].is_some() { return Err(serde::de::Error::custom("duplicate native record member")); }
                    values[index] = Some(map.next_value::<WireScalar>()?);
                }
                let tag = values[0].take().ok_or_else(|| serde::de::Error::missing_field("kind"))?.into_text::<A::Error>()?;
                match tag.as_str() { "source-span" => Ok(Ts2AnchorRefV1::SourceSpan { snapshot_id: serde::Deserialize::deserialize(serde::de::value::StringDeserializer::<A::Error>::new(values[1].take().ok_or_else(|| serde::de::Error::missing_field("snapshotId"))?.into_text::<A::Error>()?))?,path: serde::Deserialize::deserialize(serde::de::value::StringDeserializer::<A::Error>::new(values[2].take().ok_or_else(|| serde::de::Error::missing_field("path"))?.into_text::<A::Error>()?))?,content_sha256: serde::Deserialize::deserialize(serde::de::value::StringDeserializer::<A::Error>::new(values[3].take().ok_or_else(|| serde::de::Error::missing_field("contentSha256"))?.into_text::<A::Error>()?))?,start_byte: values[4].take().ok_or_else(|| serde::de::Error::missing_field("startByte"))?.into_unsigned::<A::Error>()?,end_byte: values[5].take().ok_or_else(|| serde::de::Error::missing_field("endByte"))?.into_unsigned::<A::Error>()?,fact_id: values[6].take().ok_or_else(|| serde::de::Error::missing_field("factId"))?.into_null::<A::Error>()? }),"fact-ref" => Ok(Ts2AnchorRefV1::FactRef { snapshot_id: values[1].take().ok_or_else(|| serde::de::Error::missing_field("snapshotId"))?.into_null::<A::Error>()?,path: values[2].take().ok_or_else(|| serde::de::Error::missing_field("path"))?.into_null::<A::Error>()?,content_sha256: values[3].take().ok_or_else(|| serde::de::Error::missing_field("contentSha256"))?.into_null::<A::Error>()?,start_byte: values[4].take().ok_or_else(|| serde::de::Error::missing_field("startByte"))?.into_null::<A::Error>()?,end_byte: values[5].take().ok_or_else(|| serde::de::Error::missing_field("endByte"))?.into_null::<A::Error>()?,fact_id: serde::Deserialize::deserialize(serde::de::value::StringDeserializer::<A::Error>::new(values[6].take().ok_or_else(|| serde::de::Error::missing_field("factId"))?.into_text::<A::Error>()?))? }), _ => Err(serde::de::Error::unknown_variant(&tag, &["source-span","fact-ref"])) }
            }
        }
        deserializer.deserialize_map(Record)
    }
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
pub enum Ts2FactCandidateV1Field3Value {
#[serde(rename = "derived")]
Derived,
#[serde(rename = "inventory")]
Inventory,
#[serde(rename = "semantic")]
Semantic,
#[serde(rename = "syntax")]
Syntax,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
pub enum Ts2FactCandidateV1Field4Value {
#[serde(rename = "typescript-semantic")]
TypescriptSemantic,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
pub enum Ts2FactCandidateV1Field7Value {
#[serde(rename = "typescript")]
Typescript,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Ts2FactCandidateV1 {
#[serde(rename = "candidateOrdinal")]
pub candidate_ordinal: u64,
#[serde(rename = "relation")]
pub relation: Native2Relation,
#[serde(rename = "resolution")]
pub resolution: Native2Rung,
#[serde(rename = "layer")]
pub layer: Ts2FactCandidateV1Field3Value,
#[serde(rename = "producer")]
pub producer: Ts2FactCandidateV1Field4Value,
#[serde(rename = "producerVersion")]
pub producer_version: Ts2NfcText,
#[serde(rename = "schemaVersion")]
pub schema_version: u64,
#[serde(rename = "language")]
pub language: Ts2FactCandidateV1Field7Value,
#[serde(rename = "sourceUniverseId")]
pub source_universe_id: Ts2Sha256Text,
#[serde(rename = "targetUniverseId")]
pub target_universe_id: Ts2Sha256Text,
#[serde(rename = "confidenceMillionths")]
pub confidence_millionths: u64,
#[serde(rename = "relationSchemaId")]
pub relation_schema_id: String,
#[serde(rename = "canonicalRelationPayload")]
pub canonical_relation_payload: ByteString,
#[serde(rename = "anchors")]
pub anchors: Vec<Ts2AnchorRefV1>,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Ts2FactBatchV1 {
#[serde(rename = "analysisOrdinal")]
pub analysis_ordinal: u64,
#[serde(rename = "stageId")]
pub stage_id: Ts2StageIdText,
#[serde(rename = "batchIndex")]
pub batch_index: u64,
#[serde(rename = "facts")]
pub facts: Vec<Ts2FactCandidateV1>,
#[serde(rename = "batchCommitment")]
pub batch_commitment: Ts2Sha256Text,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Ts2FactBatchV3 {
#[serde(rename = "schemaVersion")]
pub schema_version: u64,
#[serde(rename = "analysisOrdinal")]
pub analysis_ordinal: u64,
#[serde(rename = "stageId")]
pub stage_id: Ts2StageIdText,
#[serde(rename = "batchIndex")]
pub batch_index: u64,
#[serde(rename = "candidates")]
pub candidates: Vec<Ts2FactCandidateV1>,
#[serde(rename = "occupancyCompanions")]
pub occupancy_companions: Vec<Occupancy1Root>,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Ts2AnalyzeV1 {
#[serde(rename = "analysisOrdinal")]
pub analysis_ordinal: u64,
#[serde(rename = "executionId")]
pub execution_id: Ts2ExecutionIdText,
#[serde(rename = "snapshotId")]
pub snapshot_id: Ts2SnapshotId2,
#[serde(rename = "planId")]
pub plan_id: Ts2PlanId2,
#[serde(rename = "universeKey")]
pub universe_key: Ts2Sha256Text,
#[serde(rename = "stageRequests")]
pub stage_requests: Vec<Ts2StageRequestV1>,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Ts2StageResultV1 {
#[serde(rename = "stageId")]
pub stage_id: Ts2StageIdText,
#[serde(rename = "stageOrdinal")]
pub stage_ordinal: u64,
#[serde(rename = "factBatchCount")]
pub fact_batch_count: u64,
#[serde(rename = "factCount")]
pub fact_count: u64,
#[serde(rename = "coverageEntryCount")]
pub coverage_entry_count: u64,
#[serde(rename = "factCommitment")]
pub fact_commitment: Ts2Sha256Text,
#[serde(rename = "coverageCommitment")]
pub coverage_commitment: Ts2Sha256Text,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Ts2CompleteV1 {
#[serde(rename = "analysisOrdinal")]
pub analysis_ordinal: u64,
#[serde(rename = "stageResults")]
pub stage_results: Vec<Ts2StageResultV1>,
#[serde(rename = "factStreamCommitment")]
pub fact_stream_commitment: Ts2Sha256Text,
#[serde(rename = "coverageStreamCommitment")]
pub coverage_stream_commitment: Ts2Sha256Text,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
pub enum Ts2CancelV1Field2Value {
#[serde(rename = "host-shutdown")]
HostShutdown,
#[serde(rename = "user-interrupt")]
UserInterrupt,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Ts2CancelV1 {
#[serde(rename = "executionId", deserialize_with = "required_value")]
pub execution_id: Option<Ts2ExecutionIdText>,
#[serde(rename = "analysisOrdinal", deserialize_with = "required_value")]
pub analysis_ordinal: Option<u64>,
#[serde(rename = "reason")]
pub reason: Ts2CancelV1Field2Value,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
pub enum Ts2CancelledV1Field2Value {
#[serde(rename = "analysis")]
Analysis,
#[serde(rename = "handshake")]
Handshake,
#[serde(rename = "snapshot")]
Snapshot,
#[serde(rename = "universe")]
Universe,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Ts2CancelledV1 {
#[serde(rename = "executionId", deserialize_with = "required_value")]
pub execution_id: Option<Ts2ExecutionIdText>,
#[serde(rename = "analysisOrdinal", deserialize_with = "required_value")]
pub analysis_ordinal: Option<u64>,
#[serde(rename = "observedPhase")]
pub observed_phase: Ts2CancelledV1Field2Value,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Ts2SnapshotFileSubjectV1 {
#[serde(rename = "path")]
pub path: Ts2ProjectPath,
#[serde(rename = "contentSha256")]
pub content_sha256: Ts2DigestHex,
#[serde(rename = "byteLength")]
pub byte_length: u64,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
pub enum Rust3ProviderFrameV3Field1Value {
#[serde(rename = "host-to-worker")]
HostToWorker,
#[serde(rename = "worker-to-host")]
WorkerToHost,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
pub enum Rust3ProviderFrameV3Field3Value {
#[serde(rename = "Analyze")]
Analyze,
#[serde(rename = "BudgetExhausted")]
BudgetExhausted,
#[serde(rename = "Cancel")]
Cancel,
#[serde(rename = "Cancelled")]
Cancelled,
#[serde(rename = "Complete")]
Complete,
#[serde(rename = "CoverageV3")]
CoverageV3,
#[serde(rename = "DependencySourceAccepted")]
DependencySourceAccepted,
#[serde(rename = "DependencySourceChunk")]
DependencySourceChunk,
#[serde(rename = "DependencySourceManifest")]
DependencySourceManifest,
#[serde(rename = "DependencySourceSeal")]
DependencySourceSeal,
#[serde(rename = "FactBatch")]
FactBatch,
#[serde(rename = "Hello")]
Hello,
#[serde(rename = "HelloAck")]
HelloAck,
#[serde(rename = "NativeContextVerified")]
NativeContextVerified,
#[serde(rename = "OpenUniverse")]
OpenUniverse,
#[serde(rename = "PreparedOutputAccepted")]
PreparedOutputAccepted,
#[serde(rename = "PreparedOutputChunk")]
PreparedOutputChunk,
#[serde(rename = "PreparedOutputManifest")]
PreparedOutputManifest,
#[serde(rename = "PreparedOutputSeal")]
PreparedOutputSeal,
#[serde(rename = "ProviderFault")]
ProviderFault,
#[serde(rename = "SnapshotAccepted")]
SnapshotAccepted,
#[serde(rename = "SnapshotFileChunk")]
SnapshotFileChunk,
#[serde(rename = "SnapshotManifest")]
SnapshotManifest,
#[serde(rename = "SnapshotSeal")]
SnapshotSeal,
#[serde(rename = "Unavailable")]
Unavailable,
#[serde(rename = "UniverseAccepted")]
UniverseAccepted,
}

#[derive(Clone, Debug)]
pub struct Rust3ProviderFrameV3 {
pub protocol_major: u64,
pub direction: Rust3ProviderFrameV3Field1Value,
pub sequence: u64,
pub frame_type: Rust3ProviderFrameV3Field3Value,
pub payload: Rust3ProviderFrameV3Payload,
}

#[derive(Clone, Debug, serde::Serialize)]
#[serde(tag = "kind", deny_unknown_fields)]
pub enum Rust3SnapshotEntryV2 {
#[serde(rename = "file")]
File {
#[serde(rename = "path")]
path: Rust3CanonicalPath,
#[serde(rename = "byteLength")]
byte_length: u64,
#[serde(rename = "contentSha256")]
content_sha256: Rust3DigestHex,
#[serde(rename = "executable")]
executable: bool,
#[serde(rename = "targetBytes")]
target_bytes: (),
},
#[serde(rename = "symlink")]
Symlink {
#[serde(rename = "path")]
path: Rust3CanonicalPath,
#[serde(rename = "byteLength")]
byte_length: (),
#[serde(rename = "contentSha256")]
content_sha256: (),
#[serde(rename = "executable")]
executable: (),
#[serde(rename = "targetBytes")]
target_bytes: ByteString,
},
}


impl<'de> serde::Deserialize<'de> for Rust3SnapshotEntryV2 {
    fn deserialize<D: serde::Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        struct Record;
        impl<'de> serde::de::Visitor<'de> for Record {
            type Value = Rust3SnapshotEntryV2;
            fn expecting(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result { f.write_str("a tagged native record with text keys") }
            fn visit_map<A: serde::de::MapAccess<'de>>(self, mut map: A) -> Result<Self::Value, A::Error> {
                let mut values: [Option<WireScalar>; 6] = std::array::from_fn(|_| None);
                while let Some(key) = map.next_key::<StrictMapKey>()? {
                    let index = match key.0.as_str() { "path" => 0,"kind" => 1,"byteLength" => 2,"contentSha256" => 3,"executable" => 4,"targetBytes" => 5, _ => return Err(serde::de::Error::unknown_field(&key.0, &["path","kind","byteLength","contentSha256","executable","targetBytes"])) };
                    if values[index].is_some() { return Err(serde::de::Error::custom("duplicate native record member")); }
                    values[index] = Some(map.next_value::<WireScalar>()?);
                }
                let tag = values[1].take().ok_or_else(|| serde::de::Error::missing_field("kind"))?.into_text::<A::Error>()?;
                match tag.as_str() { "file" => Ok(Rust3SnapshotEntryV2::File { path: serde::Deserialize::deserialize(serde::de::value::StringDeserializer::<A::Error>::new(values[0].take().ok_or_else(|| serde::de::Error::missing_field("path"))?.into_text::<A::Error>()?))?,byte_length: values[2].take().ok_or_else(|| serde::de::Error::missing_field("byteLength"))?.into_unsigned::<A::Error>()?,content_sha256: serde::Deserialize::deserialize(serde::de::value::StringDeserializer::<A::Error>::new(values[3].take().ok_or_else(|| serde::de::Error::missing_field("contentSha256"))?.into_text::<A::Error>()?))?,executable: values[4].take().ok_or_else(|| serde::de::Error::missing_field("executable"))?.into_bool::<A::Error>()?,target_bytes: values[5].take().ok_or_else(|| serde::de::Error::missing_field("targetBytes"))?.into_null::<A::Error>()? }),"symlink" => Ok(Rust3SnapshotEntryV2::Symlink { path: serde::Deserialize::deserialize(serde::de::value::StringDeserializer::<A::Error>::new(values[0].take().ok_or_else(|| serde::de::Error::missing_field("path"))?.into_text::<A::Error>()?))?,byte_length: values[2].take().ok_or_else(|| serde::de::Error::missing_field("byteLength"))?.into_null::<A::Error>()?,content_sha256: values[3].take().ok_or_else(|| serde::de::Error::missing_field("contentSha256"))?.into_null::<A::Error>()?,executable: values[4].take().ok_or_else(|| serde::de::Error::missing_field("executable"))?.into_null::<A::Error>()?,target_bytes: values[5].take().ok_or_else(|| serde::de::Error::missing_field("targetBytes"))?.into_bytes::<A::Error>()? }), _ => Err(serde::de::Error::unknown_variant(&tag, &["file","symlink"])) }
            }
        }
        deserializer.deserialize_map(Record)
    }
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Rust3SnapshotManifestV2 {
#[serde(rename = "snapshotId")]
pub snapshot_id: Rust3SnapshotId2,
#[serde(rename = "manifestSha256")]
pub manifest_sha256: Rust3DigestHex,
#[serde(rename = "entries")]
pub entries: Vec<Rust3SnapshotEntryV2>,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Rust3SnapshotFileChunkV2 {
#[serde(rename = "snapshotId")]
pub snapshot_id: Rust3SnapshotId2,
#[serde(rename = "path")]
pub path: Rust3CanonicalPath,
#[serde(rename = "chunkIndex")]
pub chunk_index: u64,
#[serde(rename = "byteOffset")]
pub byte_offset: u64,
#[serde(rename = "bytes")]
pub bytes: ByteString,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Rust3SnapshotSealV2 {
#[serde(rename = "snapshotId")]
pub snapshot_id: Rust3SnapshotId2,
#[serde(rename = "manifestSha256")]
pub manifest_sha256: Rust3DigestHex,
#[serde(rename = "entryCount")]
pub entry_count: u64,
#[serde(rename = "totalFileBytes")]
pub total_file_bytes: u64,
#[serde(rename = "totalChunkCount")]
pub total_chunk_count: u64,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Rust3SnapshotAcceptedV2 {
#[serde(rename = "snapshotId")]
pub snapshot_id: Rust3SnapshotId2,
#[serde(rename = "manifestSha256")]
pub manifest_sha256: Rust3DigestHex,
#[serde(rename = "entryCount")]
pub entry_count: u64,
#[serde(rename = "totalFileBytes")]
pub total_file_bytes: u64,
#[serde(rename = "totalChunkCount")]
pub total_chunk_count: u64,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Rust3DependencySourceChunkV3 {
#[serde(rename = "dependencySourceSetId")]
pub dependency_source_set_id: Rust3Sha256Text,
#[serde(rename = "packageKey")]
pub package_key: Rust3PackageKey,
#[serde(rename = "path")]
pub path: Rust3DependencySourcePath,
#[serde(rename = "chunkIndex")]
pub chunk_index: u64,
#[serde(rename = "byteOffset")]
pub byte_offset: u64,
#[serde(rename = "bytes")]
pub bytes: ByteString,
}

pub type Rust3DependencySourceAcceptedV3 = Native2DependencySourceSealV3;

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
pub enum Rust3PreparedOutputEntryV3Field1Value {
#[serde(rename = "build-script-directives")]
BuildScriptDirectives,
#[serde(rename = "generated-file")]
GeneratedFile,
#[serde(rename = "macro-expansion")]
MacroExpansion,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Rust3PreparedOutputEntryV3 {
#[serde(rename = "outputOrdinal")]
pub output_ordinal: u64,
#[serde(rename = "kind")]
pub kind: Rust3PreparedOutputEntryV3Field1Value,
#[serde(rename = "planRow")]
pub plan_row: Native2PreparedOutputRowV3,
#[serde(rename = "logicalPath")]
pub logical_path: String,
#[serde(rename = "blobByteLength")]
pub blob_byte_length: u64,
#[serde(rename = "blobSha256")]
pub blob_sha256: Rust3DigestHex,
#[serde(rename = "contentByteLength")]
pub content_byte_length: u64,
#[serde(rename = "contentSha256")]
pub content_sha256: Rust3DigestHex,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Rust3PreparedOutputManifestV3 {
#[serde(rename = "planId")]
pub plan_id: Rust3PlanId2,
#[serde(rename = "manifestSha256")]
pub manifest_sha256: Rust3DigestHex,
#[serde(rename = "entries")]
pub entries: Vec<Rust3PreparedOutputEntryV3>,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Rust3PreparedOutputChunkV3 {
#[serde(rename = "planId")]
pub plan_id: Rust3PlanId2,
#[serde(rename = "outputOrdinal")]
pub output_ordinal: u64,
#[serde(rename = "chunkIndex")]
pub chunk_index: u64,
#[serde(rename = "byteOffset")]
pub byte_offset: u64,
#[serde(rename = "bytes")]
pub bytes: ByteString,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Rust3PreparedOutputSealV3 {
#[serde(rename = "planId")]
pub plan_id: Rust3PlanId2,
#[serde(rename = "manifestSha256")]
pub manifest_sha256: Rust3DigestHex,
#[serde(rename = "entryCount")]
pub entry_count: u64,
#[serde(rename = "totalBlobBytes")]
pub total_blob_bytes: u64,
#[serde(rename = "totalChunkCount")]
pub total_chunk_count: u64,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Rust3PreparedOutputAcceptedV3 {
#[serde(rename = "planId")]
pub plan_id: Rust3PlanId2,
#[serde(rename = "manifestSha256")]
pub manifest_sha256: Rust3DigestHex,
#[serde(rename = "entryCount")]
pub entry_count: u64,
#[serde(rename = "totalBlobBytes")]
pub total_blob_bytes: u64,
#[serde(rename = "totalChunkCount")]
pub total_chunk_count: u64,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Rust3SubjectV2 {
#[serde(rename = "subjectOrdinal")]
pub subject_ordinal: u64,
#[serde(rename = "subjectId")]
pub subject_id: String,
#[serde(rename = "path")]
pub path: Rust3CanonicalPath,
#[serde(rename = "startByte")]
pub start_byte: u64,
#[serde(rename = "endByte")]
pub end_byte: u64,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
pub enum Rust3CoverageKeyV2Field5Value {
#[serde(rename = "rust-semantic")]
RustSemantic,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Rust3CoverageKeyV2 {
#[serde(rename = "relation")]
pub relation: Native2Relation,
#[serde(rename = "resolution")]
pub resolution: Native2Rung,
#[serde(rename = "sourceUniverseId")]
pub source_universe_id: Rust3Sha256Text,
#[serde(rename = "targetUniverseId")]
pub target_universe_id: Rust3Sha256Text,
#[serde(rename = "subjectScopeCommitment")]
pub subject_scope_commitment: Rust3Sha256Text,
#[serde(rename = "producer")]
pub producer: Rust3CoverageKeyV2Field5Value,
#[serde(rename = "producerVersion")]
pub producer_version: Rust3IdentityText,
#[serde(rename = "schemaVersion")]
pub schema_version: u64,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Rust3StageAnalysisDomainV2 {
#[serde(rename = "subjects")]
pub subjects: Vec<Rust3SubjectV2>,
#[serde(rename = "requestedCoverageDomain")]
pub requested_coverage_domain: Vec<Rust3CoverageKeyV2>,
#[serde(rename = "domainCommitment")]
pub domain_commitment: Rust3Sha256Text,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
pub enum Rust3C2StageBudgetV1Field0Value {
#[serde(rename = "bytes")]
Bytes,
#[serde(rename = "items")]
Items,
#[serde(rename = "milliseconds")]
Milliseconds,
#[serde(rename = "work-units")]
WorkUnits,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Rust3C2StageBudgetV1 {
#[serde(rename = "unit")]
pub unit: Rust3C2StageBudgetV1Field0Value,
#[serde(rename = "limit")]
pub limit: u64,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
pub enum Rust3C2PlanStageV3Field0Value {
#[serde(rename = "fact-derivation")]
FactDerivation,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
pub enum Rust3C2PlanStageV3Field5Value {
#[serde(rename = "semantic-provider")]
SemanticProvider,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
pub enum Rust3C2PlanStageV3Field7Value {
#[serde(rename = "rust-semantic")]
RustSemantic,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Rust3C2PlanStageV3 {
#[serde(rename = "kind")]
pub kind: Rust3C2PlanStageV3Field0Value,
#[serde(rename = "stageId")]
pub stage_id: Rust3StageIdText,
#[serde(rename = "dependsOn", default, skip_serializing_if = "FieldPresence::is_missing")]
pub depends_on: FieldPresence<Vec<Rust3StageIdText>>,
#[serde(rename = "budget", default, skip_serializing_if = "FieldPresence::is_missing")]
pub budget: FieldPresence<Rust3C2StageBudgetV1>,
#[serde(rename = "relations")]
pub relations: Vec<Native2Relation>,
#[serde(rename = "operator")]
pub operator: Rust3C2PlanStageV3Field5Value,
#[serde(rename = "capabilityGrants", default, skip_serializing_if = "FieldPresence::is_missing")]
pub capability_grants: FieldPresence<Vec<Rust3CanonicalIdentifier>>,
#[serde(rename = "providerId", default, skip_serializing_if = "FieldPresence::is_missing")]
pub provider_id: FieldPresence<Rust3C2PlanStageV3Field7Value>,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Rust3StageRequestV2 {
#[serde(rename = "stageOrdinal")]
pub stage_ordinal: u64,
#[serde(rename = "planStage")]
pub plan_stage: Rust3C2PlanStageV3,
#[serde(rename = "analysisDomain")]
pub analysis_domain: Rust3StageAnalysisDomainV2,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Rust3AnalyzeV2 {
#[serde(rename = "analysisOrdinal")]
pub analysis_ordinal: u64,
#[serde(rename = "executionId")]
pub execution_id: Rust3IdentityText,
#[serde(rename = "snapshotId")]
pub snapshot_id: Rust3SnapshotId2,
#[serde(rename = "planId")]
pub plan_id: Rust3PlanId2,
#[serde(rename = "stages")]
pub stages: Vec<Rust3StageRequestV2>,
}

#[derive(Clone, Debug, serde::Serialize)]
#[serde(tag = "kind", deny_unknown_fields)]
pub enum Rust3AnchorRefV1 {
#[serde(rename = "source-span")]
SourceSpan {
#[serde(rename = "snapshotId")]
snapshot_id: Rust3SnapshotId2,
#[serde(rename = "path")]
path: Rust3CanonicalPath,
#[serde(rename = "contentSha256")]
content_sha256: Rust3DigestHex,
#[serde(rename = "startByte")]
start_byte: u64,
#[serde(rename = "endByte")]
end_byte: u64,
#[serde(rename = "factId")]
fact_id: (),
},
#[serde(rename = "fact-ref")]
FactRef {
#[serde(rename = "snapshotId")]
snapshot_id: (),
#[serde(rename = "path")]
path: (),
#[serde(rename = "contentSha256")]
content_sha256: (),
#[serde(rename = "startByte")]
start_byte: (),
#[serde(rename = "endByte")]
end_byte: (),
#[serde(rename = "factId")]
fact_id: String,
},
}


impl<'de> serde::Deserialize<'de> for Rust3AnchorRefV1 {
    fn deserialize<D: serde::Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        struct Record;
        impl<'de> serde::de::Visitor<'de> for Record {
            type Value = Rust3AnchorRefV1;
            fn expecting(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result { f.write_str("a tagged native record with text keys") }
            fn visit_map<A: serde::de::MapAccess<'de>>(self, mut map: A) -> Result<Self::Value, A::Error> {
                let mut values: [Option<WireScalar>; 7] = std::array::from_fn(|_| None);
                while let Some(key) = map.next_key::<StrictMapKey>()? {
                    let index = match key.0.as_str() { "kind" => 0,"snapshotId" => 1,"path" => 2,"contentSha256" => 3,"startByte" => 4,"endByte" => 5,"factId" => 6, _ => return Err(serde::de::Error::unknown_field(&key.0, &["kind","snapshotId","path","contentSha256","startByte","endByte","factId"])) };
                    if values[index].is_some() { return Err(serde::de::Error::custom("duplicate native record member")); }
                    values[index] = Some(map.next_value::<WireScalar>()?);
                }
                let tag = values[0].take().ok_or_else(|| serde::de::Error::missing_field("kind"))?.into_text::<A::Error>()?;
                match tag.as_str() { "source-span" => Ok(Rust3AnchorRefV1::SourceSpan { snapshot_id: serde::Deserialize::deserialize(serde::de::value::StringDeserializer::<A::Error>::new(values[1].take().ok_or_else(|| serde::de::Error::missing_field("snapshotId"))?.into_text::<A::Error>()?))?,path: serde::Deserialize::deserialize(serde::de::value::StringDeserializer::<A::Error>::new(values[2].take().ok_or_else(|| serde::de::Error::missing_field("path"))?.into_text::<A::Error>()?))?,content_sha256: serde::Deserialize::deserialize(serde::de::value::StringDeserializer::<A::Error>::new(values[3].take().ok_or_else(|| serde::de::Error::missing_field("contentSha256"))?.into_text::<A::Error>()?))?,start_byte: values[4].take().ok_or_else(|| serde::de::Error::missing_field("startByte"))?.into_unsigned::<A::Error>()?,end_byte: values[5].take().ok_or_else(|| serde::de::Error::missing_field("endByte"))?.into_unsigned::<A::Error>()?,fact_id: values[6].take().ok_or_else(|| serde::de::Error::missing_field("factId"))?.into_null::<A::Error>()? }),"fact-ref" => Ok(Rust3AnchorRefV1::FactRef { snapshot_id: values[1].take().ok_or_else(|| serde::de::Error::missing_field("snapshotId"))?.into_null::<A::Error>()?,path: values[2].take().ok_or_else(|| serde::de::Error::missing_field("path"))?.into_null::<A::Error>()?,content_sha256: values[3].take().ok_or_else(|| serde::de::Error::missing_field("contentSha256"))?.into_null::<A::Error>()?,start_byte: values[4].take().ok_or_else(|| serde::de::Error::missing_field("startByte"))?.into_null::<A::Error>()?,end_byte: values[5].take().ok_or_else(|| serde::de::Error::missing_field("endByte"))?.into_null::<A::Error>()?,fact_id: serde::Deserialize::deserialize(serde::de::value::StringDeserializer::<A::Error>::new(values[6].take().ok_or_else(|| serde::de::Error::missing_field("factId"))?.into_text::<A::Error>()?))? }), _ => Err(serde::de::Error::unknown_variant(&tag, &["source-span","fact-ref"])) }
            }
        }
        deserializer.deserialize_map(Record)
    }
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
pub enum Rust3FactCandidateV1Field3Value {
#[serde(rename = "derived")]
Derived,
#[serde(rename = "inventory")]
Inventory,
#[serde(rename = "semantic")]
Semantic,
#[serde(rename = "syntax")]
Syntax,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
pub enum Rust3FactCandidateV1Field4Value {
#[serde(rename = "rust-semantic")]
RustSemantic,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
pub enum Rust3FactCandidateV1Field7Value {
#[serde(rename = "rust")]
Rust,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Rust3FactCandidateV1 {
#[serde(rename = "candidateOrdinal")]
pub candidate_ordinal: u64,
#[serde(rename = "relation")]
pub relation: Native2Relation,
#[serde(rename = "resolution")]
pub resolution: Native2Rung,
#[serde(rename = "layer")]
pub layer: Rust3FactCandidateV1Field3Value,
#[serde(rename = "producer")]
pub producer: Rust3FactCandidateV1Field4Value,
#[serde(rename = "producerVersion")]
pub producer_version: Rust3IdentityText,
#[serde(rename = "schemaVersion")]
pub schema_version: u64,
#[serde(rename = "language")]
pub language: Rust3FactCandidateV1Field7Value,
#[serde(rename = "sourceUniverseId")]
pub source_universe_id: Rust3Sha256Text,
#[serde(rename = "targetUniverseId")]
pub target_universe_id: Rust3Sha256Text,
#[serde(rename = "confidenceMillionths")]
pub confidence_millionths: u64,
#[serde(rename = "relationSchemaId")]
pub relation_schema_id: String,
#[serde(rename = "canonicalRelationPayload")]
pub canonical_relation_payload: ByteString,
#[serde(rename = "anchors")]
pub anchors: Vec<Rust3AnchorRefV1>,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Rust3FactBatchV2 {
#[serde(rename = "analysisOrdinal")]
pub analysis_ordinal: u64,
#[serde(rename = "stageId")]
pub stage_id: Rust3StageIdText,
#[serde(rename = "batchIndex")]
pub batch_index: u64,
#[serde(rename = "candidates")]
pub candidates: Vec<Rust3FactCandidateV1>,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Rust3FactBatchV3 {
#[serde(rename = "schemaVersion")]
pub schema_version: u64,
#[serde(rename = "analysisOrdinal")]
pub analysis_ordinal: u64,
#[serde(rename = "stageId")]
pub stage_id: Rust3StageIdText,
#[serde(rename = "batchIndex")]
pub batch_index: u64,
#[serde(rename = "candidates")]
pub candidates: Vec<Rust3FactCandidateV1>,
#[serde(rename = "occupancyCompanions")]
pub occupancy_companions: Vec<Occupancy1Root>,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Rust3StageResultV2 {
#[serde(rename = "stageId")]
pub stage_id: Rust3StageIdText,
#[serde(rename = "factCount")]
pub fact_count: u64,
#[serde(rename = "coverageEntryCount")]
pub coverage_entry_count: u64,
#[serde(rename = "factCommitment")]
pub fact_commitment: Rust3Sha256Text,
#[serde(rename = "coverageCommitment")]
pub coverage_commitment: Rust3Sha256Text,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Rust3CompleteV2 {
#[serde(rename = "analysisOrdinal")]
pub analysis_ordinal: u64,
#[serde(rename = "stageResults")]
pub stage_results: Vec<Rust3StageResultV2>,
#[serde(rename = "factStreamCommitment")]
pub fact_stream_commitment: Rust3Sha256Text,
#[serde(rename = "coverageStreamCommitment")]
pub coverage_stream_commitment: Rust3Sha256Text,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
pub enum Rust3ProviderFaultV2Field2Value {
#[serde(rename = "ANALYZING")]
ANALYZING,
#[serde(rename = "READY_ANALYZE")]
READYANALYZE,
#[serde(rename = "READY_COMPLETE")]
READYCOMPLETE,
#[serde(rename = "READY_DEPENDENCY_MANIFEST")]
READYDEPENDENCYMANIFEST,
#[serde(rename = "READY_OPEN_UNIVERSE")]
READYOPENUNIVERSE,
#[serde(rename = "READY_PREPARED_MANIFEST")]
READYPREPAREDMANIFEST,
#[serde(rename = "READY_SNAPSHOT_MANIFEST")]
READYSNAPSHOTMANIFEST,
#[serde(rename = "RECEIVING_DEPENDENCY")]
RECEIVINGDEPENDENCY,
#[serde(rename = "RECEIVING_PREPARED")]
RECEIVINGPREPARED,
#[serde(rename = "RECEIVING_SNAPSHOT")]
RECEIVINGSNAPSHOT,
#[serde(rename = "WAIT_DEPENDENCY_ACCEPTED")]
WAITDEPENDENCYACCEPTED,
#[serde(rename = "WAIT_HELLO_ACK")]
WAITHELLOACK,
#[serde(rename = "WAIT_NATIVE_CONTEXT_VERIFIED")]
WAITNATIVECONTEXTVERIFIED,
#[serde(rename = "WAIT_PREPARED_ACCEPTED")]
WAITPREPAREDACCEPTED,
#[serde(rename = "WAIT_SNAPSHOT_ACCEPTED")]
WAITSNAPSHOTACCEPTED,
#[serde(rename = "WAIT_UNIVERSE_ACCEPTED")]
WAITUNIVERSEACCEPTED,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
pub enum Rust3ProviderFaultV2Field3Value {
#[serde(rename = "compiler-crash")]
CompilerCrash,
#[serde(rename = "input-rejected")]
InputRejected,
#[serde(rename = "internal-invariant")]
InternalInvariant,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Rust3ProviderFaultV2 {
#[serde(rename = "executionId", deserialize_with = "required_value")]
pub execution_id: Option<Rust3IdentityText>,
#[serde(rename = "analysisOrdinal", deserialize_with = "required_value")]
pub analysis_ordinal: Option<u64>,
#[serde(rename = "phase")]
pub phase: Rust3ProviderFaultV2Field2Value,
#[serde(rename = "faultKind")]
pub fault_kind: Rust3ProviderFaultV2Field3Value,
#[serde(rename = "detailCode")]
pub detail_code: Rust3IdentityText,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
pub enum Rust3CancelV2Field2Value {
#[serde(rename = "user-interrupt")]
UserInterrupt,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Rust3CancelV2 {
#[serde(rename = "executionId", deserialize_with = "required_value")]
pub execution_id: Option<Rust3IdentityText>,
#[serde(rename = "analysisOrdinal", deserialize_with = "required_value")]
pub analysis_ordinal: Option<u64>,
#[serde(rename = "reason")]
pub reason: Rust3CancelV2Field2Value,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
pub enum Rust3CancelledV2Field2Value {
#[serde(rename = "ANALYZING")]
ANALYZING,
#[serde(rename = "READY_ANALYZE")]
READYANALYZE,
#[serde(rename = "READY_COMPLETE")]
READYCOMPLETE,
#[serde(rename = "READY_DEPENDENCY_MANIFEST")]
READYDEPENDENCYMANIFEST,
#[serde(rename = "READY_OPEN_UNIVERSE")]
READYOPENUNIVERSE,
#[serde(rename = "READY_PREPARED_MANIFEST")]
READYPREPAREDMANIFEST,
#[serde(rename = "READY_SNAPSHOT_MANIFEST")]
READYSNAPSHOTMANIFEST,
#[serde(rename = "RECEIVING_DEPENDENCY")]
RECEIVINGDEPENDENCY,
#[serde(rename = "RECEIVING_PREPARED")]
RECEIVINGPREPARED,
#[serde(rename = "RECEIVING_SNAPSHOT")]
RECEIVINGSNAPSHOT,
#[serde(rename = "WAIT_DEPENDENCY_ACCEPTED")]
WAITDEPENDENCYACCEPTED,
#[serde(rename = "WAIT_HELLO_ACK")]
WAITHELLOACK,
#[serde(rename = "WAIT_NATIVE_CONTEXT_VERIFIED")]
WAITNATIVECONTEXTVERIFIED,
#[serde(rename = "WAIT_PREPARED_ACCEPTED")]
WAITPREPAREDACCEPTED,
#[serde(rename = "WAIT_SNAPSHOT_ACCEPTED")]
WAITSNAPSHOTACCEPTED,
#[serde(rename = "WAIT_UNIVERSE_ACCEPTED")]
WAITUNIVERSEACCEPTED,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Rust3CancelledV2 {
#[serde(rename = "executionId", deserialize_with = "required_value")]
pub execution_id: Option<Rust3IdentityText>,
#[serde(rename = "analysisOrdinal", deserialize_with = "required_value")]
pub analysis_ordinal: Option<u64>,
#[serde(rename = "observedPhase")]
pub observed_phase: Rust3CancelledV2Field2Value,
}

/// Inert selection only. No serde: decoding requires frameType and admitted host selector.
#[derive(Clone, Debug)]
pub enum Ts2FrameV2Payload {
Hello(Box<Handshake1TypeScriptHelloV2>),
OpenUniverse(Box<Startup1TypeScriptOpenUniverseV2>),
SnapshotManifest(Box<Ts2SnapshotManifestV1>),
SnapshotFileChunk(Box<Ts2SnapshotFileChunkV1>),
SnapshotSeal(Box<Ts2SnapshotSealV1>),
Analyze(Box<Ts2AnalyzeV1>),
Cancel(Box<Ts2CancelV1>),
HelloAck(Box<Handshake1TypeScriptHelloAckV2>),
UniverseAccepted(Box<Startup1TypeScriptUniverseAcceptedV2>),
SnapshotAccepted(Box<Ts2SnapshotAcceptedV1>),
NativeContextVerified(Box<Startup1NativeContextVerifiedV1>),
/// Host selector negotiated-target-attribution-v2 = false; not a wire tag.
FactBatch0(Box<Ts2FactBatchV1>),
/// Host selector negotiated-target-attribution-v2 = true; not a wire tag.
FactBatch1(Box<Ts2FactBatchV3>),
Coverage(Box<Startup1TypeScriptCoverageV2>),
/// Host selector host-phase = WAIT_NATIVE_CONTEXT_VERIFIED; not a wire tag.
Unavailable0(Box<Startup1PreAnalyzeUnavailableV1>),
/// Host selector host-phase = ANALYZING; not a wire tag.
Unavailable1(Box<Startup1TypeScriptUnavailableV2>),
BudgetExhausted(Box<Startup1TypeScriptBudgetExhaustedV2>),
Complete(Box<Ts2CompleteV1>),
Cancelled(Box<Ts2CancelledV1>),
}

/// Inert selection only. No serde: decoding requires frameType and admitted host selector.
#[derive(Clone, Debug)]
pub enum Rust3ProviderFrameV3Payload {
Hello(Box<Handshake1HelloV3>),
HelloAck(Box<Handshake1HelloAckV3>),
OpenUniverse(Box<Startup1OpenUniverseV3>),
UniverseAccepted(Box<Startup1UniverseAcceptedV3>),
SnapshotManifest(Box<Rust3SnapshotManifestV2>),
SnapshotFileChunk(Box<Rust3SnapshotFileChunkV2>),
SnapshotSeal(Box<Rust3SnapshotSealV2>),
SnapshotAccepted(Box<Rust3SnapshotAcceptedV2>),
DependencySourceManifest(Box<Native2DependencySourceManifestV3>),
DependencySourceChunk(Box<Rust3DependencySourceChunkV3>),
DependencySourceSeal(Box<Native2DependencySourceSealV3>),
DependencySourceAccepted(Box<Rust3DependencySourceAcceptedV3>),
PreparedOutputManifest(Box<Rust3PreparedOutputManifestV3>),
PreparedOutputChunk(Box<Rust3PreparedOutputChunkV3>),
PreparedOutputSeal(Box<Rust3PreparedOutputSealV3>),
PreparedOutputAccepted(Box<Rust3PreparedOutputAcceptedV3>),
NativeContextVerified(Box<Startup1NativeContextVerifiedV1>),
Analyze(Box<Rust3AnalyzeV2>),
/// Host selector negotiated-target-attribution-v2 = false; not a wire tag.
FactBatch0(Box<Rust3FactBatchV2>),
/// Host selector negotiated-target-attribution-v2 = true; not a wire tag.
FactBatch1(Box<Rust3FactBatchV3>),
CoverageV3(Box<Startup1CoverageV3>),
/// Host selector host-phase = WAIT_NATIVE_CONTEXT_VERIFIED; not a wire tag.
Unavailable0(Box<Startup1PreAnalyzeUnavailableV1>),
/// Host selector host-phase = ANALYZING; not a wire tag.
Unavailable1(Box<Startup1UnavailableV3>),
BudgetExhausted(Box<Startup1BudgetExhaustedV3>),
Complete(Box<Rust3CompleteV2>),
ProviderFault(Box<Rust3ProviderFaultV2>),
Cancel(Box<Rust3CancelV2>),
Cancelled(Box<Rust3CancelledV2>),
}
