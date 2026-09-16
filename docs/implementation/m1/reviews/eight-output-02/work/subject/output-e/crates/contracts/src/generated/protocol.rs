// Generated trial: named28 profile, typify0.8.0; inert carriers only.
#![allow(unused_imports)]
use super::evidence::error;
use super::evidence::*;
use super::identity::*;
use super::invocation::*;
use super::output::*;
#[doc = "Host operational binding derived by dispatch from the actual Plan stage selected into THIS Analyze request. Not a protocol3 frame, not a worker field, not a new channel. FactBatch.stageId remains C-2 TEXT. Analyze may be a subset of execution-plan stages, so analyzeRequestOrdinal (contiguous in THIS Analyze) MUST NOT be equated with retainedStageOrdinal (execution-plan.stages[].ordinal). Host bind looks up the execution-plan row by retainedStageOrdinal and correlates the worker batch against expectedStageId / expectedAnalysisOrdinal / expectedBatchIndex / expectedFirstCandidateOrdinal."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Dispatch1Root {
    #[doc = "StageRequestV1.stageOrdinal / StageRequestV2.stageOrdinal: contiguous 0..n-1 in THIS Analyze request order. Provider Analyze may omit Plan stages, so this MAY differ from retainedStageOrdinal. Not echoed as FactBatch.stageId."]
    #[serde(rename = "analyzeRequestOrdinal")]
    pub analyze_request_ordinal: u64,
    #[doc = "AnalyzeV1/AnalyzeV2.analysisOrdinal for this Analyze. Worker FactBatch.analysisOrdinal must equal this integer. Omitting this observation cannot be replaced by a caller scalar on the batch."]
    #[serde(rename = "expectedAnalysisOrdinal")]
    pub expected_analysis_ordinal: u64,
    #[doc = "Contiguous batchIndex the host expects for this stage's next FactBatch (0..n-1 per requested stage)."]
    #[serde(rename = "expectedBatchIndex")]
    pub expected_batch_index: u64,
    #[doc = "candidateOrdinal of the first candidate in this batch. Batch 0 of a stage is 0. Later batches continue the per-stage candidate stream. Unique-increasing inside the batch is the candidateOrdinal array-order annotation; contiguous 0..n-1 across batches of one stage is a separate candidate-stream law."]
    #[serde(rename = "expectedFirstCandidateOrdinal")]
    pub expected_first_candidate_ordinal: u64,
    #[doc = "Exact C-2 stageId text of the selected Plan stage (StageRequestV1.stageId; StageRequestV2.planStage.stageId). Worker FactBatch.stageId must byte-equal this text."]
    #[serde(rename = "expectedStageId")]
    pub expected_stage_id: Dispatch1RootExpectedStageId,
    #[doc = "Retained Plan locator. Must equal execution-plan.planId and the stage-spec planId."]
    #[serde(rename = "planId")]
    pub plan_id: ::std::string::String,
    #[doc = "Stage-spec producerClosure of the retained stage. Occupancy joins this producer, not EnumerationPlan enumerator.closureId."]
    #[serde(rename = "producerClosure")]
    pub producer_closure: ::std::string::String,
    #[doc = "execution-plan.stages[].ordinal of the Plan stage this Analyze request selected. Host looks up the execution-plan row by this integer. Not FactBatch.stageId. Not analyzeRequestOrdinal."]
    #[serde(rename = "retainedStageOrdinal")]
    pub retained_stage_ordinal: u64,
    #[serde(rename = "schemaVersion")]
    pub schema_version: ExactInteger,
    #[doc = "execution-plan.stages[retainedStageOrdinal].stageSpecDigest. Host re-derives producerClosure from the stage spec at this digest."]
    #[serde(rename = "stageSpecDigest")]
    pub stage_spec_digest: ::std::string::String,
}
#[doc = "Exact C-2 stageId text of the selected Plan stage (StageRequestV1.stageId; StageRequestV2.planStage.stageId). Worker FactBatch.stageId must byte-equal this text."]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
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
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
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
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
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
#[doc = "`FactBatch3PropertiesCandidatesItems`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct FactBatch3PropertiesCandidatesItems {
    pub anchors: ::std::vec::Vec<::serde_json::Map<::std::string::String, ::serde_json::Value>>,
    #[serde(rename = "candidateOrdinal")]
    pub candidate_ordinal: u64,
    #[doc = "JSON-vector transcription of FactCandidateV1.canonicalRelationPayload. Those wire bytes are deterministic-CBOR of the closed relation payload (fact-plane.v1 candidateSchema.transportRepresentation). The hex encodes those SAME CBOR bytes, not canonical JSON UTF-8. Admission requires hex == deterministic_cbor(decodedRelationPayload).hex()."]
    #[serde(rename = "canonicalRelationPayloadHex")]
    pub canonical_relation_payload_hex:
        FactBatch3PropertiesCandidatesItemsCanonicalRelationPayloadHex,
    #[serde(rename = "confidenceMillionths")]
    pub confidence_millionths: i64,
    #[doc = "Verified TCB observation of one decode of the CBOR payload bytes. Not a wire field. Must round-trip to canonicalRelationPayloadHex via fact-plane _deterministic_cbor."]
    #[serde(rename = "decodedRelationPayload")]
    pub decoded_relation_payload: ::serde_json::Map<::std::string::String, ::serde_json::Value>,
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
#[doc = "JSON-vector transcription of FactCandidateV1.canonicalRelationPayload. Those wire bytes are deterministic-CBOR of the closed relation payload (fact-plane.v1 candidateSchema.transportRepresentation). The hex encodes those SAME CBOR bytes, not canonical JSON UTF-8. Admission requires hex == deterministic_cbor(decodedRelationPayload).hex()."]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct FactBatch3PropertiesCandidatesItemsCanonicalRelationPayloadHex(::std::string::String);
impl ::std::ops::Deref for FactBatch3PropertiesCandidatesItemsCanonicalRelationPayloadHex {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<FactBatch3PropertiesCandidatesItemsCanonicalRelationPayloadHex>
    for ::std::string::String
{
    fn from(value: FactBatch3PropertiesCandidatesItemsCanonicalRelationPayloadHex) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for FactBatch3PropertiesCandidatesItemsCanonicalRelationPayloadHex {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() < 2usize {
            return Err("shorter than 2 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str>
    for FactBatch3PropertiesCandidatesItemsCanonicalRelationPayloadHex
{
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
    for FactBatch3PropertiesCandidatesItemsCanonicalRelationPayloadHex
{
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de>
    for FactBatch3PropertiesCandidatesItemsCanonicalRelationPayloadHex
{
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
#[doc = "`FactBatch3PropertiesCandidatesItemsLanguage`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct FactBatch3PropertiesCandidatesItemsLanguage(::std::string::String);
impl ::std::ops::Deref for FactBatch3PropertiesCandidatesItemsLanguage {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<FactBatch3PropertiesCandidatesItemsLanguage> for ::std::string::String {
    fn from(value: FactBatch3PropertiesCandidatesItemsLanguage) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for FactBatch3PropertiesCandidatesItemsLanguage {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
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
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
    for FactBatch3PropertiesCandidatesItemsLanguage
{
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
#[doc = "`FactBatch3PropertiesCandidatesItemsLayer`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct FactBatch3PropertiesCandidatesItemsLayer(::std::string::String);
impl ::std::ops::Deref for FactBatch3PropertiesCandidatesItemsLayer {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<FactBatch3PropertiesCandidatesItemsLayer> for ::std::string::String {
    fn from(value: FactBatch3PropertiesCandidatesItemsLayer) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for FactBatch3PropertiesCandidatesItemsLayer {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
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
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for FactBatch3PropertiesCandidatesItemsLayer {
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
#[doc = "`FactBatch3PropertiesCandidatesItemsProducer`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct FactBatch3PropertiesCandidatesItemsProducer(::std::string::String);
impl ::std::ops::Deref for FactBatch3PropertiesCandidatesItemsProducer {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<FactBatch3PropertiesCandidatesItemsProducer> for ::std::string::String {
    fn from(value: FactBatch3PropertiesCandidatesItemsProducer) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for FactBatch3PropertiesCandidatesItemsProducer {
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
impl ::std::convert::TryFrom<&str> for FactBatch3PropertiesCandidatesItemsProducer {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
    for FactBatch3PropertiesCandidatesItemsProducer
{
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
#[doc = "`FactBatch3PropertiesCandidatesItemsProducerVersion`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct FactBatch3PropertiesCandidatesItemsProducerVersion(::std::string::String);
impl ::std::ops::Deref for FactBatch3PropertiesCandidatesItemsProducerVersion {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<FactBatch3PropertiesCandidatesItemsProducerVersion>
    for ::std::string::String
{
    fn from(value: FactBatch3PropertiesCandidatesItemsProducerVersion) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for FactBatch3PropertiesCandidatesItemsProducerVersion {
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
impl ::std::convert::TryFrom<&str> for FactBatch3PropertiesCandidatesItemsProducerVersion {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
    for FactBatch3PropertiesCandidatesItemsProducerVersion
{
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for FactBatch3PropertiesCandidatesItemsProducerVersion {
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
#[doc = "`FactBatch3PropertiesCandidatesItemsRelation`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct FactBatch3PropertiesCandidatesItemsRelation(::std::string::String);
impl ::std::ops::Deref for FactBatch3PropertiesCandidatesItemsRelation {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<FactBatch3PropertiesCandidatesItemsRelation> for ::std::string::String {
    fn from(value: FactBatch3PropertiesCandidatesItemsRelation) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for FactBatch3PropertiesCandidatesItemsRelation {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
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
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
    for FactBatch3PropertiesCandidatesItemsRelation
{
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
#[doc = "`FactBatch3PropertiesCandidatesItemsRelationSchemaId`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct FactBatch3PropertiesCandidatesItemsRelationSchemaId(::std::string::String);
impl ::std::ops::Deref for FactBatch3PropertiesCandidatesItemsRelationSchemaId {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<FactBatch3PropertiesCandidatesItemsRelationSchemaId>
    for ::std::string::String
{
    fn from(value: FactBatch3PropertiesCandidatesItemsRelationSchemaId) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for FactBatch3PropertiesCandidatesItemsRelationSchemaId {
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
impl ::std::convert::TryFrom<&str> for FactBatch3PropertiesCandidatesItemsRelationSchemaId {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
    for FactBatch3PropertiesCandidatesItemsRelationSchemaId
{
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for FactBatch3PropertiesCandidatesItemsRelationSchemaId {
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
#[doc = "`FactBatch3PropertiesCandidatesItemsResolution`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct FactBatch3PropertiesCandidatesItemsResolution(::std::string::String);
impl ::std::ops::Deref for FactBatch3PropertiesCandidatesItemsResolution {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<FactBatch3PropertiesCandidatesItemsResolution> for ::std::string::String {
    fn from(value: FactBatch3PropertiesCandidatesItemsResolution) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for FactBatch3PropertiesCandidatesItemsResolution {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
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
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
    for FactBatch3PropertiesCandidatesItemsResolution
{
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
#[doc = "`FactBatch3PropertiesCandidatesItemsSourceUniverseId`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct FactBatch3PropertiesCandidatesItemsSourceUniverseId(::std::string::String);
impl ::std::ops::Deref for FactBatch3PropertiesCandidatesItemsSourceUniverseId {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<FactBatch3PropertiesCandidatesItemsSourceUniverseId>
    for ::std::string::String
{
    fn from(value: FactBatch3PropertiesCandidatesItemsSourceUniverseId) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for FactBatch3PropertiesCandidatesItemsSourceUniverseId {
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
impl ::std::convert::TryFrom<&str> for FactBatch3PropertiesCandidatesItemsSourceUniverseId {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
    for FactBatch3PropertiesCandidatesItemsSourceUniverseId
{
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for FactBatch3PropertiesCandidatesItemsSourceUniverseId {
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
#[doc = "`FactBatch3PropertiesCandidatesItemsTargetUniverseId`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct FactBatch3PropertiesCandidatesItemsTargetUniverseId(::std::string::String);
impl ::std::ops::Deref for FactBatch3PropertiesCandidatesItemsTargetUniverseId {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<FactBatch3PropertiesCandidatesItemsTargetUniverseId>
    for ::std::string::String
{
    fn from(value: FactBatch3PropertiesCandidatesItemsTargetUniverseId) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for FactBatch3PropertiesCandidatesItemsTargetUniverseId {
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
impl ::std::convert::TryFrom<&str> for FactBatch3PropertiesCandidatesItemsTargetUniverseId {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
    for FactBatch3PropertiesCandidatesItemsTargetUniverseId
{
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for FactBatch3PropertiesCandidatesItemsTargetUniverseId {
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
#[doc = "CURRENT selected FactBatch payload iff Hello/HelloAck negotiated target-attribution-v2. Preserves the historical rust-semantic FactBatchV2 field names analysisOrdinal, stageId, batchIndex, candidates (the typescript-semantic historical FactBatchV1 names its array facts and carries batchCommitment). Occupancy is a PARALLEL occupancyCompanions array, not a FactCandidateV1 field. stageId is TEXT: the worker echo of the current requested C-2 stageId (StageRequestV1.stageId; StageRequestV2.planStage.stageId). It is NOT Analyze stageOrdinal and NOT execution-plan.stages[].ordinal. Provider Analyze may be a subset of Plan stages; host DispatchBindingV1 carries retainedStageOrdinal separately. When the token is absent the historical per-language payload remains: typescript-semantic delivery.v2 FactBatchV1 {analysisOrdinal, stageId, batchIndex, facts, batchCommitment}; rust-semantic rust-provider-protocol.v2 FactBatchV2 {analysisOrdinal, stageId, batchIndex, candidates}. A V3 payload without the token, or that language's historical payload with the token, is PROVIDER.PROTOCOL_VIOLATION."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct FactBatch3Root {
    #[doc = "Exact echo of AnalyzeV1/AnalyzeV2.analysisOrdinal for this Analyze. Host correlates against DispatchBindingV1.expectedAnalysisOrdinal."]
    #[serde(rename = "analysisOrdinal")]
    pub analysis_ordinal: u64,
    #[doc = "Contiguous from 0 for this requested stage, same as FactBatchV2. Host correlates against DispatchBindingV1.expectedBatchIndex."]
    #[serde(rename = "batchIndex")]
    pub batch_index: u64,
    #[doc = "Non-empty closed FactCandidateV1 membership as a JSON vector. No occupancy field. Array-order token candidateOrdinal (published in occupancy-companion.schema.v1.json x-opensip-order-vocabulary and implemented by canonical.py): integer unique strictly increasing by candidateOrdinal; gaps lawful at this annotation. Contiguous 0..n-1 across batches of one requested stage is a separate candidate-stream law, joined to DispatchBindingV1.expectedFirstCandidateOrdinal. Arrays are not silently sorted."]
    pub candidates: ::std::vec::Vec<FactBatch3RootCandidatesItem>,
    #[doc = "Zero or more OccupancyCompanionV1, each admitting as native/occupancy-companion.schema.v1.json including its allOf branches. Length <= candidates. Every candidateOrdinal names a candidate in this batch. Empty is lawful unknown except exact-id ephemeral. Same candidateOrdinal array-order token as candidates. Not silently sorted. This schema is independently complete via registered $ref; validators MUST resolve opensip.product.occupancy-companion.1 without mutating this dictionary at import time."]
    #[serde(rename = "occupancyCompanions")]
    pub occupancy_companions: ::std::vec::Vec<Occupancy1Root>,
    #[serde(rename = "schemaVersion")]
    pub schema_version: ExactInteger,
    #[doc = "Historical FactBatchV1/V2.stageId preserved as C-2 TEXT. Worker echo of the current requested stage's C-2 stageId (delivery.v2 StageRequestV1.stageId; rust-provider-protocol StageRequestV2.planStage.stageId). Host correlates batch.stageId == DispatchBindingV1.expectedStageId. Do not treat this string as execution-plan.stages[].ordinal or as Analyze request stageOrdinal."]
    #[serde(rename = "stageId")]
    pub stage_id: FactBatch3RootStageId,
}
#[doc = "`FactBatch3RootCandidatesItem`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct FactBatch3RootCandidatesItem {
    pub anchors: ::std::vec::Vec<::serde_json::Map<::std::string::String, ::serde_json::Value>>,
    #[serde(rename = "candidateOrdinal")]
    pub candidate_ordinal: u64,
    #[doc = "JSON-vector transcription of FactCandidateV1.canonicalRelationPayload. Those wire bytes are deterministic-CBOR of the closed relation payload (fact-plane.v1 candidateSchema.transportRepresentation). The hex encodes those SAME CBOR bytes, not canonical JSON UTF-8. Admission requires hex == deterministic_cbor(decodedRelationPayload).hex()."]
    #[serde(rename = "canonicalRelationPayloadHex")]
    pub canonical_relation_payload_hex: FactBatch3RootCandidatesItemCanonicalRelationPayloadHex,
    #[serde(rename = "confidenceMillionths")]
    pub confidence_millionths: i64,
    #[doc = "Verified TCB observation of one decode of the CBOR payload bytes. Not a wire field. Must round-trip to canonicalRelationPayloadHex via fact-plane _deterministic_cbor."]
    #[serde(rename = "decodedRelationPayload")]
    pub decoded_relation_payload: ::serde_json::Map<::std::string::String, ::serde_json::Value>,
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
#[doc = "JSON-vector transcription of FactCandidateV1.canonicalRelationPayload. Those wire bytes are deterministic-CBOR of the closed relation payload (fact-plane.v1 candidateSchema.transportRepresentation). The hex encodes those SAME CBOR bytes, not canonical JSON UTF-8. Admission requires hex == deterministic_cbor(decodedRelationPayload).hex()."]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct FactBatch3RootCandidatesItemCanonicalRelationPayloadHex(::std::string::String);
impl ::std::ops::Deref for FactBatch3RootCandidatesItemCanonicalRelationPayloadHex {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<FactBatch3RootCandidatesItemCanonicalRelationPayloadHex>
    for ::std::string::String
{
    fn from(value: FactBatch3RootCandidatesItemCanonicalRelationPayloadHex) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for FactBatch3RootCandidatesItemCanonicalRelationPayloadHex {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() < 2usize {
            return Err("shorter than 2 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for FactBatch3RootCandidatesItemCanonicalRelationPayloadHex {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
    for FactBatch3RootCandidatesItemCanonicalRelationPayloadHex
{
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl<'de> ::serde::Deserialize<'de> for FactBatch3RootCandidatesItemCanonicalRelationPayloadHex {
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
#[doc = "`FactBatch3RootCandidatesItemLanguage`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct FactBatch3RootCandidatesItemLanguage(::std::string::String);
impl ::std::ops::Deref for FactBatch3RootCandidatesItemLanguage {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<FactBatch3RootCandidatesItemLanguage> for ::std::string::String {
    fn from(value: FactBatch3RootCandidatesItemLanguage) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for FactBatch3RootCandidatesItemLanguage {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
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
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for FactBatch3RootCandidatesItemLanguage {
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
#[doc = "`FactBatch3RootCandidatesItemLayer`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
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
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
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
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for FactBatch3RootCandidatesItemLayer {
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
#[doc = "`FactBatch3RootCandidatesItemProducer`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct FactBatch3RootCandidatesItemProducer(::std::string::String);
impl ::std::ops::Deref for FactBatch3RootCandidatesItemProducer {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<FactBatch3RootCandidatesItemProducer> for ::std::string::String {
    fn from(value: FactBatch3RootCandidatesItemProducer) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for FactBatch3RootCandidatesItemProducer {
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
impl ::std::convert::TryFrom<&str> for FactBatch3RootCandidatesItemProducer {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for FactBatch3RootCandidatesItemProducer {
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
#[doc = "`FactBatch3RootCandidatesItemProducerVersion`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct FactBatch3RootCandidatesItemProducerVersion(::std::string::String);
impl ::std::ops::Deref for FactBatch3RootCandidatesItemProducerVersion {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<FactBatch3RootCandidatesItemProducerVersion> for ::std::string::String {
    fn from(value: FactBatch3RootCandidatesItemProducerVersion) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for FactBatch3RootCandidatesItemProducerVersion {
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
impl ::std::convert::TryFrom<&str> for FactBatch3RootCandidatesItemProducerVersion {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
    for FactBatch3RootCandidatesItemProducerVersion
{
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
#[doc = "`FactBatch3RootCandidatesItemRelation`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct FactBatch3RootCandidatesItemRelation(::std::string::String);
impl ::std::ops::Deref for FactBatch3RootCandidatesItemRelation {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<FactBatch3RootCandidatesItemRelation> for ::std::string::String {
    fn from(value: FactBatch3RootCandidatesItemRelation) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for FactBatch3RootCandidatesItemRelation {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
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
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for FactBatch3RootCandidatesItemRelation {
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
#[doc = "`FactBatch3RootCandidatesItemRelationSchemaId`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct FactBatch3RootCandidatesItemRelationSchemaId(::std::string::String);
impl ::std::ops::Deref for FactBatch3RootCandidatesItemRelationSchemaId {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<FactBatch3RootCandidatesItemRelationSchemaId> for ::std::string::String {
    fn from(value: FactBatch3RootCandidatesItemRelationSchemaId) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for FactBatch3RootCandidatesItemRelationSchemaId {
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
impl ::std::convert::TryFrom<&str> for FactBatch3RootCandidatesItemRelationSchemaId {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
    for FactBatch3RootCandidatesItemRelationSchemaId
{
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
#[doc = "`FactBatch3RootCandidatesItemResolution`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct FactBatch3RootCandidatesItemResolution(::std::string::String);
impl ::std::ops::Deref for FactBatch3RootCandidatesItemResolution {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<FactBatch3RootCandidatesItemResolution> for ::std::string::String {
    fn from(value: FactBatch3RootCandidatesItemResolution) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for FactBatch3RootCandidatesItemResolution {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
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
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for FactBatch3RootCandidatesItemResolution {
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
#[doc = "`FactBatch3RootCandidatesItemSourceUniverseId`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct FactBatch3RootCandidatesItemSourceUniverseId(::std::string::String);
impl ::std::ops::Deref for FactBatch3RootCandidatesItemSourceUniverseId {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<FactBatch3RootCandidatesItemSourceUniverseId> for ::std::string::String {
    fn from(value: FactBatch3RootCandidatesItemSourceUniverseId) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for FactBatch3RootCandidatesItemSourceUniverseId {
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
impl ::std::convert::TryFrom<&str> for FactBatch3RootCandidatesItemSourceUniverseId {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
    for FactBatch3RootCandidatesItemSourceUniverseId
{
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
#[doc = "`FactBatch3RootCandidatesItemTargetUniverseId`"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
#[serde(transparent)]
pub struct FactBatch3RootCandidatesItemTargetUniverseId(::std::string::String);
impl ::std::ops::Deref for FactBatch3RootCandidatesItemTargetUniverseId {
    type Target = ::std::string::String;
    fn deref(&self) -> &::std::string::String {
        &self.0
    }
}
impl ::std::convert::From<FactBatch3RootCandidatesItemTargetUniverseId> for ::std::string::String {
    fn from(value: FactBatch3RootCandidatesItemTargetUniverseId) -> Self {
        value.0
    }
}
impl ::std::str::FromStr for FactBatch3RootCandidatesItemTargetUniverseId {
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
impl ::std::convert::TryFrom<&str> for FactBatch3RootCandidatesItemTargetUniverseId {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
    for FactBatch3RootCandidatesItemTargetUniverseId
{
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
#[doc = "Historical FactBatchV1/V2.stageId preserved as C-2 TEXT. Worker echo of the current requested stage's C-2 stageId (delivery.v2 StageRequestV1.stageId; rust-provider-protocol StageRequestV2.planStage.stageId). Host correlates batch.stageId == DispatchBindingV1.expectedStageId. Do not treat this string as execution-plan.stages[].ordinal or as Analyze request stageOrdinal."]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
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
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
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
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
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
#[doc = "`Handshake1DigestHex`"]
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
#[doc = "ExpectedRustIdentityV2 members unchanged except protocolMajor 3."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Handshake1ExpectedRustIdentityV3 {
    #[doc = "Selected Plan rust-v1 row hostTriple."]
    #[serde(rename = "hostTriple")]
    pub host_triple: Handshake1IdentityText,
    #[serde(rename = "protocolMajor")]
    pub protocol_major: ExactInteger,
    #[doc = "Selected Plan rust-v1 row providerBuildId (verified signed release)."]
    #[serde(rename = "providerBuildId")]
    pub provider_build_id: Handshake1IdentityText,
    #[doc = "Selected Plan rust-v1 row rustCommitHash (resolved-inputs.v2 rust-v1 digestFields representation)."]
    #[serde(rename = "rustCommitHash")]
    pub rust_commit_hash: Handshake1DigestHex,
    #[doc = "Selected Plan rust-v1 row sysrootDigest."]
    #[serde(rename = "sysrootDigest")]
    pub sysroot_digest: Handshake1DigestHex,
    #[doc = "Selected Plan rust-v1 row targetTriple."]
    #[serde(rename = "targetTriple")]
    pub target_triple: Handshake1IdentityText,
}
#[doc = "rust-semantic major-3 HelloAck. Every HelloAckV2 identity echo kept; protocolMajor 3; token array and identityVersions echoes."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Handshake1HelloAckV3 {
    #[doc = "Exact echo of Hello expectedCapabilities."]
    pub capabilities: Handshake1RustCapabilitiesV3,
    #[doc = "HelloAckV2, unchanged: exact Hello expectedIdentity value."]
    #[serde(rename = "hostTriple")]
    pub host_triple: Handshake1IdentityText,
    #[doc = "Exact echo of Hello identityVersions."]
    #[serde(rename = "identityVersions")]
    pub identity_versions: Handshake1IdentityVersionsV1,
    #[serde(rename = "protocolMajor")]
    pub protocol_major: ExactInteger,
    #[doc = "HelloAckV2, unchanged: exact Hello expectedIdentity value."]
    #[serde(rename = "providerBuildId")]
    pub provider_build_id: Handshake1IdentityText,
    #[doc = "HelloAckV2, unchanged: exact Hello expectedIdentity value."]
    #[serde(rename = "rustCommitHash")]
    pub rust_commit_hash: Handshake1DigestHex,
    #[doc = "HelloAckV2, unchanged: exact Hello expectedIdentity value."]
    #[serde(rename = "sysrootDigest")]
    pub sysroot_digest: Handshake1DigestHex,
    #[doc = "HelloAckV2, unchanged: exact Hello expectedIdentity value."]
    #[serde(rename = "targetTriple")]
    pub target_triple: Handshake1IdentityText,
}
#[doc = "rust-semantic major-3 Hello. Every HelloV2 member kept, capability record replaced by the token array, identityVersions added, limits ProtocolLimitsV3."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Handshake1HelloV3 {
    #[doc = "Replaces HelloV2 RustProviderCapabilityV2 with the section 9.1 token array (kept from the superseded HelloV3 definition)."]
    #[serde(rename = "expectedCapabilities")]
    pub expected_capabilities: Handshake1RustCapabilitiesV3,
    #[doc = "HelloV2 expectedIdentity, protocolMajor 3."]
    #[serde(rename = "expectedIdentity")]
    pub expected_identity: Handshake1ExpectedRustIdentityV3,
    #[doc = "HelloV2, unchanged: raw SHA-256 of the exact bytes of docs/coop/artifacts/rust-provider-protocol.v2.json (x-opensip-wire-law expectedProtocolContractSha256)."]
    #[serde(rename = "expectedProtocolContractSha256")]
    pub expected_protocol_contract_sha256: Handshake1DigestHex,
    #[doc = "HelloV2, unchanged."]
    #[serde(rename = "hostBuildId")]
    pub host_build_id: Handshake1IdentityText,
    #[doc = "Kept from the superseded HelloV3 definition."]
    #[serde(rename = "identityVersions")]
    pub identity_versions: Handshake1IdentityVersionsV1,
    #[doc = "32-member closed map (section 9.3)."]
    pub limits: Handshake1ProtocolLimitsV3,
    #[serde(rename = "protocolMajor")]
    pub protocol_major: ExactInteger,
}
#[doc = "rust-provider-protocol.v2 IdentityText: NFC, 1..4096 UTF-8 bytes, no C0/C1 control. NFC and the UTF-8 byte bound are checked by admission."]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
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
impl ::std::convert::TryFrom<&str> for Handshake1IdentityText {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
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
#[doc = "native-evidence section 9.1 identity versions; HelloAck echoes the Hello value exactly."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Handshake1IdentityVersionsV1 {
    pub coverage: ExactInteger,
    pub fact: ExactInteger,
    pub plan: ExactInteger,
    pub snapshot: ExactInteger,
}
#[doc = "delivery.v2 'non-empty NFC text' / 'verified descriptor text'. NFC is checked by admission."]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
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
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Handshake1NfcText {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
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
#[doc = "rust-semantic HelloV3.limits: the 24 rust-provider-protocol.v2 limits members with identical values plus the eight native-evidence section 9.3 members (32). limitsHandshake semantic and deterministic-CBOR byte equality and limitPolicy apply unchanged."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
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
#[doc = "NORMATIVE field-level publication for native-evidence sections 9.1, 9.3, 9.4 and 9.6. HelloV3, HelloAckV3 and ProtocolLimitsV3 here SUPERSEDE the same-named $defs of native/native-evidence.schemas.v2.json, whose registered bytes are kept unchanged because that document's raw SHA-256 is a registered payloadSchemaDigest (native-evidence section 10); a byte change there would be a schema-document successor with re-registration. TypeScriptProtocolLimitsV1, TypeScriptHelloV2 and TypeScriptHelloAckV2 publish the typescript-semantic major-2 handshake. Every record is the JSON-vector form of a closed deterministic-CBOR map; handshake payloads carry no byte strings. Cross-record joins that a stock schema cannot express (descriptor digests and fields, identity and token echoes, contract digest, limit CBOR byte equality, candidate CBOR projection, TypeScript batch commitment) are executed by native/provider_wire_model.v1.py within that module's stated scope."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
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
#[doc = "rust-semantic token array: strictly unique ascending UTF-8 order, the four identity tokens present."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(transparent)]
pub struct Handshake1RustCapabilitiesV3(pub ::std::vec::Vec<Handshake1RustCapabilityToken>);
impl ::std::ops::Deref for Handshake1RustCapabilitiesV3 {
    type Target = ::std::vec::Vec<Handshake1RustCapabilityToken>;
    fn deref(&self) -> &::std::vec::Vec<Handshake1RustCapabilityToken> {
        &self.0
    }
}
impl ::std::convert::From<Handshake1RustCapabilitiesV3>
    for ::std::vec::Vec<Handshake1RustCapabilityToken>
{
    fn from(value: Handshake1RustCapabilitiesV3) -> Self {
        value.0
    }
}
impl ::std::convert::From<::std::vec::Vec<Handshake1RustCapabilityToken>>
    for Handshake1RustCapabilitiesV3
{
    fn from(value: ::std::vec::Vec<Handshake1RustCapabilityToken>) -> Self {
        Self(value)
    }
}
#[doc = "The rust-semantic members of native-evidence.schemas.v2.json#/$defs/CapabilityToken (section 9.1); typescript-semantic-facts-v1 is excluded."]
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
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
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
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
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
#[doc = "JSON vector of the unchanged rust-semantic historical payload rust-provider-protocol.v2 FactBatchV2, admitted when target-attribution-v2 is not negotiated."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Handshake1RustFactBatchV2Vector {
    #[doc = "Exact Analyze analysisOrdinal echo."]
    #[serde(rename = "analysisOrdinal")]
    pub analysis_ordinal: Handshake1Uint64,
    #[doc = "Contiguous from 0 for the stage."]
    #[serde(rename = "batchIndex")]
    pub batch_index: Handshake1Uint64,
    #[doc = "Non-empty FactCandidateV1 JSON vectors with contiguous candidateOrdinal, length <= maxFactBatchCandidates."]
    pub candidates: ::std::vec::Vec<FactBatch3PropertiesCandidatesItems>,
    #[doc = "StageRequestV2.planStage.stageId."]
    #[serde(rename = "stageId")]
    pub stage_id: Handshake1StageIdText,
}
#[doc = "`Handshake1Sha256Text`"]
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
#[doc = "C-2 stageId text, the historical FactBatchV1/V2 stageId type preserved on FactBatchV3."]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
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
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
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
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
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
#[doc = "typescript-semantic token array: strictly unique ascending UTF-8 order, the four identity tokens present."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
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
    for ::std::vec::Vec<Handshake1TypeScriptCapabilityToken>
{
    fn from(value: Handshake1TypeScriptCapabilitiesV2) -> Self {
        value.0
    }
}
impl ::std::convert::From<::std::vec::Vec<Handshake1TypeScriptCapabilityToken>>
    for Handshake1TypeScriptCapabilitiesV2
{
    fn from(value: ::std::vec::Vec<Handshake1TypeScriptCapabilityToken>) -> Self {
        Self(value)
    }
}
#[doc = "The typescript-semantic members of native-evidence.schemas.v2.json#/$defs/CapabilityToken (section 9.1); the Rust-only dependency-source-v1, prepared-output-v3 and rust-semantic-facts-v1 are excluded (section 9.4)."]
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
            Self::TypescriptSemanticFactsV1 => f.write_str("typescript-semantic-facts-v1"),
            Self::UnresolvedEdgeV1 => f.write_str("unresolved-edge-v1"),
        }
    }
}
impl ::std::str::FromStr for Handshake1TypeScriptCapabilityToken {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
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
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Handshake1TypeScriptCapabilityToken {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
#[doc = "JSON vector of the unchanged typescript-semantic historical payload delivery.v2 FactBatchV1, admitted when target-attribution-v2 is not negotiated."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Handshake1TypeScriptFactBatchV1Vector {
    #[serde(rename = "analysisOrdinal")]
    pub analysis_ordinal: ExactInteger,
    #[doc = "sha256 under domain opensip.ts-provider.fact-batch.v1 over deterministic-CBOR of the wire facts array."]
    #[serde(rename = "batchCommitment")]
    pub batch_commitment: Handshake1Sha256Text,
    #[doc = "Contiguous from 0 for the stage."]
    #[serde(rename = "batchIndex")]
    pub batch_index: Handshake1Uint64,
    #[doc = "Non-empty ordered FactCandidateV1 JSON vectors, length <= maxFactBatchFacts."]
    pub facts: ::std::vec::Vec<FactBatch3PropertiesCandidatesItems>,
    #[doc = "Current requested stage (StageRequestV1.stageId)."]
    #[serde(rename = "stageId")]
    pub stage_id: Handshake1StageIdText,
}
#[doc = "typescript-semantic major-2 HelloAck. Every HelloAckV1 member kept, including all provider/runtime descriptor verification; protocolMajor 1 -> 2 and the fixed capability array -> the negotiated echo; identityVersions added."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Handshake1TypeScriptHelloAckV2 {
    #[doc = "HelloAckV1 fixed three-token array replaced by the exact echo of Hello expectedCapabilities."]
    pub capabilities: Handshake1TypeScriptCapabilitiesV2,
    #[doc = "HelloAckV1, unchanged."]
    #[serde(rename = "defaultWorkBudgetProfileId")]
    pub default_work_budget_profile_id: ::serde_json::Value,
    #[doc = "HelloAckV1, unchanged."]
    #[serde(rename = "defaultWorkBudgetProfileSha256")]
    pub default_work_budget_profile_sha256: ::serde_json::Value,
    #[doc = "Added: exact echo of Hello identityVersions."]
    #[serde(rename = "identityVersions")]
    pub identity_versions: Handshake1IdentityVersionsV1,
    #[doc = "HelloAckV1, unchanged: verified runtime descriptor value."]
    #[serde(rename = "modulesAbi")]
    pub modules_abi: Handshake1NfcText,
    #[doc = "HelloAckV1, unchanged: verified runtime descriptor value."]
    #[serde(rename = "nodeVersion")]
    pub node_version: Handshake1NfcText,
    #[doc = "HelloAckV1, unchanged: selected release platformId, equal to the verified runtime descriptor value."]
    #[serde(rename = "platformId")]
    pub platform_id: Handshake1NfcText,
    #[serde(rename = "protocolMajor")]
    pub protocol_major: ExactInteger,
    #[doc = "HelloAckV1, unchanged: verified provider descriptor value."]
    #[serde(rename = "providerBuildId")]
    pub provider_build_id: Handshake1NfcText,
    #[doc = "HelloAckV1, unchanged: equals Hello expectedProviderDescriptorSha256."]
    #[serde(rename = "providerDescriptorSha256")]
    pub provider_descriptor_sha256: Handshake1DigestHex,
    #[doc = "HelloAckV1, unchanged: equals Hello expectedRuntimeDescriptorSha256."]
    #[serde(rename = "runtimeDescriptorSha256")]
    pub runtime_descriptor_sha256: Handshake1DigestHex,
    #[doc = "HelloAckV1, unchanged: verified provider descriptor value."]
    #[serde(rename = "typescriptCompilerSha256")]
    pub typescript_compiler_sha256: Handshake1DigestHex,
    #[doc = "HelloAckV1, unchanged: verified provider descriptor value."]
    #[serde(rename = "typescriptStdlibMerkleRoot")]
    pub typescript_stdlib_merkle_root: Handshake1DigestHex,
    #[doc = "HelloAckV1, unchanged: verified provider descriptor value."]
    #[serde(rename = "typescriptVersion")]
    pub typescript_version: Handshake1NfcText,
    #[doc = "HelloAckV1, unchanged: verified runtime descriptor value."]
    #[serde(rename = "v8Version")]
    pub v8_version: Handshake1NfcText,
}
#[doc = "typescript-semantic major-2 Hello. Every HelloV1 member unchanged plus expectedCapabilities and identityVersions. No payload protocolMajor; the envelope protocolMajor is exactly 2."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Handshake1TypeScriptHelloV2 {
    #[doc = "Added: the selected signed capability row's tokens (section 9.1)."]
    #[serde(rename = "expectedCapabilities")]
    pub expected_capabilities: Handshake1TypeScriptCapabilitiesV2,
    #[doc = "HelloV1, unchanged: raw SHA-256 of the RFC 8785 bytes of the verified signed typescript-provider/identity.json."]
    #[serde(rename = "expectedProviderDescriptorSha256")]
    pub expected_provider_descriptor_sha256: Handshake1DigestHex,
    #[doc = "HelloV1, unchanged: raw SHA-256 of the RFC 8785 bytes of the verified signed typescript-runtime/identity.json."]
    #[serde(rename = "expectedRuntimeDescriptorSha256")]
    pub expected_runtime_descriptor_sha256: Handshake1DigestHex,
    #[doc = "HelloV1 hostBuildId, unchanged."]
    #[serde(rename = "hostBuildId")]
    pub host_build_id: Handshake1NfcText,
    #[doc = "Added (section 9.1)."]
    #[serde(rename = "identityVersions")]
    pub identity_versions: Handshake1IdentityVersionsV1,
    #[doc = "HelloV1 'closed map equal to wireSchema.limits numeric fields', unchanged."]
    pub limits: Handshake1TypeScriptProtocolLimitsV1,
}
#[doc = "Exactly the ten numeric members of delivery.v2 typescriptSemanticSubstrate.providerProtocol.wireSchema.limits with identical values; limitRule is policy text and never a member."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
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
#[doc = "`Handshake1Uint64`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
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
#[doc = "rust-semantic BudgetExhausted: BudgetExhaustedV2 members, CoverageResultV3 coverage."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Startup1BudgetExhaustedV3 {
    #[serde(rename = "analysisOrdinal")]
    pub analysis_ordinal: Startup1Uint64,
    #[doc = "CoverageResultV3 in stage-major/key order; entry k belongs to the stage whose cumulative requested-key range contains k."]
    pub coverage: ::std::vec::Vec<Native2CoverageResultV3>,
    #[serde(rename = "coverageCommitment")]
    pub coverage_commitment: Startup1Sha256Text,
    pub limit: Startup1Uint64,
    pub observed: Startup1Uint64,
    #[serde(rename = "triggerStageId")]
    pub trigger_stage_id: Startup1StageIdText,
    pub unit: Startup1BudgetExhaustedV3Unit,
}
#[doc = "`Startup1BudgetExhaustedV3Unit`"]
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
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
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
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
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
#[doc = "rust-semantic frame CoverageV3 payload: CoverageV2 wrapper with CoverageResultV3 entries."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Startup1CoverageV3 {
    #[serde(rename = "analysisOrdinal")]
    pub analysis_ordinal: Startup1Uint64,
    #[serde(rename = "coverageCommitment")]
    pub coverage_commitment: Startup1Sha256Text,
    #[doc = "entries[i] answers requestedCoverageDomain.keys[i] of the attributed stage; CoverageResultV3 is the entry type, never the frame."]
    pub entries: ::std::vec::Vec<Native2CoverageResultV3>,
    #[serde(rename = "stageId")]
    pub stage_id: Startup1StageIdText,
}
#[doc = "`Startup1DigestHex`"]
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
#[doc = "host-allocated ExecutionId text, exact AttemptRecord value (rust-semantic IdentityText rules checked by admission)"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
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
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Startup1ExecutionIdText {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
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
#[doc = "native-evidence 9.2 NativeContextVerified payload, both languages."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Startup1NativeContextVerifiedV1 {
    pub equal: ::serde_json::Value,
    #[serde(rename = "nativeContextId")]
    pub native_context_id: Startup1Sha256Text,
    #[serde(rename = "recomputedNativeContextId")]
    pub recomputed_native_context_id: Startup1Sha256Text,
}
#[doc = "non-empty text; NFC is checked by admission"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
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
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        if value.chars().count() < 1usize {
            return Err("shorter than 1 characters".into());
        }
        Ok(Self(value.to_string()))
    }
}
impl ::std::convert::TryFrom<&str> for Startup1NfcText {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
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
#[doc = "rust-semantic major-3 OpenUniverse: OpenUniverseV2 members with successor types; no mode booleans."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
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
#[doc = "`Startup1PlanId2`"]
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
#[doc = "Pre-Analyze Unavailable payload, both languages; only in the NativeContextVerified interval; carries no requested stage or coverage."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
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
#[doc = "Closed JSON-vector records of deterministic-CBOR wire maps for OpenUniverse, UniverseAccepted, NativeContextVerified, pre-Analyze Unavailable, Coverage and terminal coverage payloads. Entry records CoverageResultV3, RepositoryResolutionV3 and the v2 resolvedInputs are referenced from the registered bundle by $id and are not redefined."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
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
#[doc = "The resolved-inputs.v2 rust-v1 map with resolvedInputs replaced by RustUniverseV2ResolvedInputs and protocolMajor 3; every other member, constant and digest representation unchanged."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
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
    #[doc = "component name -> 64-hex digest (rust-v1 digestRepresentation)"]
    #[serde(rename = "standardLibraryComponentDigests")]
    pub standard_library_component_digests:
        ::std::collections::BTreeMap<::std::string::String, Startup1DigestHex>,
    #[serde(rename = "sysrootDigest")]
    pub sysroot_digest: Startup1DigestHex,
    #[serde(rename = "targetTriple")]
    pub target_triple: Startup1NfcText,
    #[serde(rename = "toolchainArtifactId")]
    pub toolchain_artifact_id: ::serde_json::Value,
    #[serde(rename = "toolchainArtifactSha256")]
    pub toolchain_artifact_sha256: Startup1DigestHex,
}
#[doc = "`Startup1Sha256Text`"]
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
#[doc = "`Startup1SnapshotId2`"]
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
#[doc = "C-2 stageId text"]
#[derive(:: serde :: Serialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
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
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
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
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
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
#[doc = "typescript-semantic BudgetExhausted: BudgetExhaustedV1 members, CoverageResultV3 coverage."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Startup1TypeScriptBudgetExhaustedV2 {
    #[serde(rename = "analysisOrdinal")]
    pub analysis_ordinal: ExactInteger,
    #[doc = "CoverageResultV3 in stage-major/key order; entry k belongs to the stage whose cumulative requested-key range contains k."]
    pub coverage: ::std::vec::Vec<Native2CoverageResultV3>,
    #[serde(rename = "coverageCommitment")]
    pub coverage_commitment: Startup1Sha256Text,
    pub dimension: Startup1TypeScriptBudgetExhaustedV2Dimension,
    pub limit: Startup1Uint64,
    pub observed: Startup1Uint64,
    #[serde(rename = "triggerStageId")]
    pub trigger_stage_id: Startup1StageIdText,
}
#[doc = "`Startup1TypeScriptBudgetExhaustedV2Dimension`"]
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
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
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
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String>
    for Startup1TypeScriptBudgetExhaustedV2Dimension
{
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
#[doc = "typescript-semantic frame Coverage payload: CoverageV1 wrapper with CoverageResultV3 entries."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Startup1TypeScriptCoverageV2 {
    #[serde(rename = "analysisOrdinal")]
    pub analysis_ordinal: ExactInteger,
    #[serde(rename = "coverageCommitment")]
    pub coverage_commitment: Startup1Sha256Text,
    #[doc = "entries[i] answers requestedCoverageDomain.keys[i] of the attributed stage; CoverageResultV3 is the entry type, never the frame."]
    pub entries: ::std::vec::Vec<Native2CoverageResultV3>,
    #[serde(rename = "stageId")]
    pub stage_id: Startup1StageIdText,
}
#[doc = "typescript-semantic major-2 OpenUniverse: OpenUniverseV1 members with successor types."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
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
#[doc = "The resolved-inputs.v2 typescript-v1 map with resolvedInputs replaced by TypeScriptUniverseV2ResolvedInputs and protocolMajor 2; every other member, constant and digest representation unchanged."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
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
#[doc = "typescript-semantic post-Analyze Unavailable (immediately after Analyze): UnavailableV1 members, CoverageResultV3 coverage, reason never native-context-mismatch."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Startup1TypeScriptUnavailableV2 {
    #[doc = "all requested stageIds in request order (inherited)"]
    #[serde(rename = "affectedStageIds")]
    pub affected_stage_ids: ::std::vec::Vec<Startup1StageIdText>,
    #[serde(rename = "analysisOrdinal")]
    pub analysis_ordinal: ExactInteger,
    #[doc = "CoverageResultV3 in stage-major/key order; entry k belongs to the stage whose cumulative requested-key range contains k."]
    pub coverage: ::std::vec::Vec<Native2CoverageResultV3>,
    #[serde(rename = "coverageCommitment")]
    pub coverage_commitment: Startup1Sha256Text,
    pub reason: Startup1TypeScriptUnavailableV2Reason,
}
#[doc = "`Startup1TypeScriptUnavailableV2Reason`"]
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
            Self::NodeModulesOutsideReadSet => f.write_str("node-modules-outside-read-set"),
            Self::SemanticUniverseIncomplete => f.write_str("semantic-universe-incomplete"),
            Self::SnapshotResolutionInputMissing => {
                f.write_str("snapshot-resolution-input-missing")
            }
            Self::UnsupportedCompilerMode => f.write_str("unsupported-compiler-mode"),
        }
    }
}
impl ::std::str::FromStr for Startup1TypeScriptUnavailableV2Reason {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "capability-missing" => Ok(Self::CapabilityMissing),
            "identity-version-mismatch" => Ok(Self::IdentityVersionMismatch),
            "node-modules-outside-read-set" => Ok(Self::NodeModulesOutsideReadSet),
            "semantic-universe-incomplete" => Ok(Self::SemanticUniverseIncomplete),
            "snapshot-resolution-input-missing" => Ok(Self::SnapshotResolutionInputMissing),
            "unsupported-compiler-mode" => Ok(Self::UnsupportedCompilerMode),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Startup1TypeScriptUnavailableV2Reason {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
impl ::std::convert::TryFrom<::std::string::String> for Startup1TypeScriptUnavailableV2Reason {
    type Error = self::error::ConversionError;
    fn try_from(
        value: ::std::string::String,
    ) -> ::std::result::Result<Self, self::error::ConversionError> {
        value.parse()
    }
}
#[doc = "typescript-semantic major-2 UniverseAccepted: UniverseAcceptedV1 members; universeKey is the worker recomputation."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
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
#[doc = "`Startup1Uint64`"]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
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
#[doc = "rust-semantic post-Analyze Unavailable (P3-25): UnavailableV2 members, CoverageResultV3 coverage, reason never native-context-mismatch."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
#[serde(deny_unknown_fields)]
pub struct Startup1UnavailableV3 {
    #[doc = "all requested stageIds in request order (inherited)"]
    #[serde(rename = "affectedStageIds")]
    pub affected_stage_ids: ::std::vec::Vec<Startup1StageIdText>,
    #[serde(rename = "analysisOrdinal")]
    pub analysis_ordinal: Startup1Uint64,
    #[doc = "CoverageResultV3 in stage-major/key order; entry k belongs to the stage whose cumulative requested-key range contains k."]
    pub coverage: ::std::vec::Vec<Native2CoverageResultV3>,
    #[serde(rename = "coverageCommitment")]
    pub coverage_commitment: Startup1Sha256Text,
    pub reason: Startup1UnavailableV3Reason,
}
#[doc = "`Startup1UnavailableV3Reason`"]
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
            Self::DependencySourceIncomplete => f.write_str("dependency-source-incomplete"),
            Self::GeneratedCfgUnavailable => f.write_str("generated-cfg-unavailable"),
            Self::IdentityVersionMismatch => f.write_str("identity-version-mismatch"),
            Self::PreparedOutputNotInert => f.write_str("prepared-output-not-inert"),
            Self::PreparedOutputStale => f.write_str("prepared-output-stale"),
            Self::SemanticUniverseIncomplete => f.write_str("semantic-universe-incomplete"),
            Self::SnapshotResolutionInputMissing => {
                f.write_str("snapshot-resolution-input-missing")
            }
            Self::UnsupportedCompilerMode => f.write_str("unsupported-compiler-mode"),
        }
    }
}
impl ::std::str::FromStr for Startup1UnavailableV3Reason {
    type Err = self::error::ConversionError;
    fn from_str(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
        match value {
            "capability-missing" => Ok(Self::CapabilityMissing),
            "dependency-source-incomplete" => Ok(Self::DependencySourceIncomplete),
            "generated-cfg-unavailable" => Ok(Self::GeneratedCfgUnavailable),
            "identity-version-mismatch" => Ok(Self::IdentityVersionMismatch),
            "prepared-output-not-inert" => Ok(Self::PreparedOutputNotInert),
            "prepared-output-stale" => Ok(Self::PreparedOutputStale),
            "semantic-universe-incomplete" => Ok(Self::SemanticUniverseIncomplete),
            "snapshot-resolution-input-missing" => Ok(Self::SnapshotResolutionInputMissing),
            "unsupported-compiler-mode" => Ok(Self::UnsupportedCompilerMode),
            _ => Err("invalid value".into()),
        }
    }
}
impl ::std::convert::TryFrom<&str> for Startup1UnavailableV3Reason {
    type Error = self::error::ConversionError;
    fn try_from(value: &str) -> ::std::result::Result<Self, self::error::ConversionError> {
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
#[doc = "rust-semantic major-3 UniverseAccepted: exact recursive echo of OpenUniverseV3 members."]
#[derive(:: serde :: Deserialize, :: serde :: Serialize, Clone, Debug)]
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
