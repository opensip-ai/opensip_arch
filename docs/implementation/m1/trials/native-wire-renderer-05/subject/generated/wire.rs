// INERT GENERATION TRIAL. Owner SHA256 3f8a45f22f72cc52a74762d39079f5cdeca185f39ccb8421cb2085726d3f6981
#![allow(unused_imports)]
use opensip_contracts::generated::evidence::*;
use opensip_contracts::generated::identity::*;
use opensip_contracts::generated::invocation::*;
use opensip_contracts::generated::output::*;
use opensip_contracts::generated::protocol::*;

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
pub path: Native2CanonicalPath,
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
