//! Pure retained input checks; no complete native closure or evaluator replay.
use crate::{
    CandidateError, CanonicalError, IdentityCandidate, IdentityDomain, JsonValue,
    RegisteredSchemas, canonical_bytes, parse_json, raw_sha256,
};
use alloc::{collections::BTreeMap, string::String, vec::Vec};

/// Inert supplied descriptor. Neither public field is an admission claim.
pub struct ObjectInput {
    pub domain: IdentityDomain,
    pub descriptor: JsonValue,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Error {
    MissingObject(String),
    MissingBlob([u8; 32]),
    ObjectDomain,
    ObjectIdentity,
    BlobDigest,
    BlobLength,
    NoncanonicalRecord,
    Canonical(CanonicalError),
    Candidate(CandidateError),
    ClosureRole {
        field: &'static str,
        expected: &'static str,
    },
    InvalidRoleField,
}

/// A hash-checked view of supplied bytes. It proves neither artifact semantics
/// nor ownership, authorization, durable retention or a complete closure.
pub struct RetainedBlob<'a> {
    digest: [u8; 32],
    bytes: &'a [u8],
}
impl RetainedBlob<'_> {
    pub fn digest(&self) -> [u8; 32] {
        self.digest
    }
    pub fn bytes(&self) -> &[u8] {
        self.bytes
    }
    pub fn require_length(&self, expected: u64) -> Result<(), Error> {
        if u64::try_from(self.bytes.len()).ok() == Some(expected) {
            Ok(())
        } else {
            Err(Error::BlobLength)
        }
    }
    /// Lexical/canonical admission only. The owner must still select and check
    /// its exact record schema, digest interpretation and semantic joins.
    pub fn canonical_record(&self) -> Result<JsonValue, Error> {
        let value = parse_json(self.bytes).map_err(Error::Canonical)?;
        if canonical_bytes(&value).map_err(Error::Canonical)? != self.bytes {
            return Err(Error::NoncanonicalRecord);
        }
        Ok(value)
    }
}

/// Borrows immutable caller-supplied values; has no I/O, fallback or cache.
/// Decode memoization and full contextual admission are distinct later owners.
pub struct RetainedInputs<'a> {
    registry: &'a RegisteredSchemas,
    objects: &'a BTreeMap<String, ObjectInput>,
    blobs: &'a BTreeMap<[u8; 32], Vec<u8>>,
}
impl<'a> RetainedInputs<'a> {
    pub fn new(
        registry: &'a RegisteredSchemas,
        objects: &'a BTreeMap<String, ObjectInput>,
        blobs: &'a BTreeMap<[u8; 32], Vec<u8>>,
    ) -> Self {
        Self {
            registry,
            objects,
            blobs,
        }
    }
    pub fn blob(&self, digest: [u8; 32]) -> Result<RetainedBlob<'_>, Error> {
        let raw = self.blobs.get(&digest).ok_or(Error::MissingBlob(digest))?;
        if raw_sha256(raw) != digest {
            return Err(Error::BlobDigest);
        }
        Ok(RetainedBlob { digest, bytes: raw })
    }
    fn candidate(
        &self,
        key: &str,
        domain: IdentityDomain,
        budget: usize,
    ) -> Result<IdentityCandidate<'a>, Error> {
        let input = self
            .objects
            .get(key)
            .ok_or_else(|| Error::MissingObject(key.into()))?;
        if input.domain != domain {
            return Err(Error::ObjectDomain);
        }
        let raw = canonical_bytes(&input.descriptor).map_err(Error::Canonical)?;
        let candidate = IdentityCandidate::from_json(self.registry, domain, &raw, budget)
            .map_err(Error::Candidate)?;
        if candidate.identifier() != key {
            return Err(Error::ObjectIdentity);
        }
        Ok(candidate)
    }
    /// Recompute the expected-domain identity and closure field roles. This
    /// method deliberately does not claim transitive blob/schema/native joins.
    pub fn object(
        &self,
        key: &str,
        domain: IdentityDomain,
        budget: usize,
    ) -> Result<IdentityCandidate<'a>, Error> {
        let candidate = self.candidate(key, domain, budget)?;
        let JsonValue::Object(value) = candidate.descriptor() else {
            return Err(Error::InvalidRoleField);
        };
        let kind = if domain == IdentityDomain::RegenerationKey {
            "cache-key"
        } else {
            domain.name()
        };
        for &(owner, field, expected) in CANDIDATE_CLOSURE_ROLES {
            if owner != kind {
                continue;
            }
            let Some(JsonValue::String(reference)) = value.get(field) else {
                return Err(Error::InvalidRoleField);
            };
            let closure = self.candidate(reference, IdentityDomain::Closure, budget)?;
            let JsonValue::Object(descriptor) = closure.descriptor() else {
                return Err(Error::InvalidRoleField);
            };
            if !matches!(descriptor.get("kind"),Some(JsonValue::String(actual)) if actual==expected)
            {
                return Err(Error::ClosureRole { field, expected });
            }
        }
        Ok(candidate)
    }
}
// Exact subset of selected identity-v3 closureKinds.byField for the 19 candidate
// domains. Stage-spec and native record rows belong to their later owners.
const CANDIDATE_CLOSURE_ROLES: &[(&str, &str, &str)] = &[
    ("subject-scope", "enumeratorClosure", "provider"),
    ("view", "producerClosure", "provider"),
    ("fact", "producerClosure", "provider"),
    ("finding", "ruleClosure", "detector"),
    ("evaluation-seal", "evaluatorClosure", "evaluator"),
    ("proof-bundle", "evaluatorClosure", "evaluator"),
    ("import", "producerClosure", "provider"),
    ("import", "adapterClosure", "adapter"),
    ("cache-key", "producerClosure", "provider"),
];

use crate::{SchemaAdmissionError, SchemaError};
use alloc::{collections::BTreeSet, format, string::ToString};
const IDENTITY_SCHEMA: &str = "urn:opensip:product-v1:identity:v3";

/// Development traversal limits. These are explicit work controls, not the
/// product's as-yet-unqualified M6 resource envelope.
#[derive(Clone, Copy)]
pub struct TraversalBudget {
    pub steps: usize,
    pub depth: usize,
    pub descriptor_work: usize,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum GraphError {
    Input(Error),
    Schema(SchemaAdmissionError),
    Interpretation(SchemaError),
    Law,
    Limit,
    Unsupported(&'static str),
    OwnerJoin,
    AmbiguousBranch,
    UntypedDigestArray,
    UndeclaredDigestProperty,
    NoncanonicalRecord,
    Frame(crate::DigestError),
    UnregisteredFrameDomain,
    UnregisteredSchemaDocument,
    UnannotatedFoundationDigest,
    DerivedIdentity,
    PayloadRegistryRow,
    AmbiguousPayloadRegistryRow,
    PayloadSchemaDocument,
    RelationLaw(&'static str),
    RelationRule(&'static str),
}
impl From<Error> for GraphError {
    fn from(e: Error) -> Self {
        Self::Input(e)
    }
}
impl From<SchemaAdmissionError> for GraphError {
    fn from(e: SchemaAdmissionError) -> Self {
        Self::Schema(e)
    }
}
/// Completed local structural checks. This is deliberately not a Run/closure or
/// replay admission token. Unsupported owner operations refuse this prototype.
pub struct StructuralChecks {
    objects: BTreeSet<String>,
    blobs: BTreeSet<[u8; 32]>,
    records: BTreeSet<([u8; 32], String)>,
    foreign: BTreeSet<([u8; 32], String, String)>,
}
impl StructuralChecks {
    pub fn object_count(&self) -> usize {
        self.objects.len()
    }
    pub fn blob_count(&self) -> usize {
        self.blobs.len()
    }
    pub fn record_count(&self) -> usize {
        self.records.len() + self.foreign.len()
    }
}
/// Callback requests are inert structural obligations, not admission tokens.
/// Only a closed evaluator composition may attach its own semantic guarantees.
pub enum StructuralObligation<'a> {
    Retention {
        annotation: &'a JsonValue,
        value: &'a str,
        siblings: Option<&'a JsonValue>,
    },
    StageSchema {
        digest: [u8; 32],
        siblings: Option<&'a JsonValue>,
    },
    Capability(&'a str),
    NativeFrame {
        value: &'a str,
        set: &'a str,
    },
    Payload {
        digest: [u8; 32],
        record: &'a JsonValue,
        siblings: &'a JsonValue,
    },
}
/// Optional structural diagnostics extension. A caller implementing this trait
/// cannot mint a Run, complete evaluator result or replay authority. Existing
/// inspect methods use a rejecting owner and retain their fail-closed behavior.
pub trait StructuralOwner {
    fn object(
        &mut self,
        _key: &str,
        _domain: IdentityDomain,
        _value: &JsonValue,
    ) -> Result<(), GraphError> {
        Ok(())
    }
    fn resolve(&mut self, obligation: StructuralObligation<'_>) -> Result<(), GraphError>;
}
struct RejectOwner;
impl StructuralOwner for RejectOwner {
    fn resolve(&mut self, obligation: StructuralObligation<'_>) -> Result<(), GraphError> {
        Err(GraphError::Unsupported(match obligation {
            StructuralObligation::Retention { .. } => "retention owner join",
            StructuralObligation::StageSchema { .. } => "stage output schema owner join",
            StructuralObligation::Capability(_) => "capability derivation",
            StructuralObligation::NativeFrame { .. } => "registered H-frame domain set",
            StructuralObligation::Payload { .. } => "payload-class owner joins",
        }))
    }
}
struct Walker<'s, 'a> {
    owners: &'s mut dyn StructuralOwner,
    inputs: &'s RetainedInputs<'a>,
    budget: TraversalBudget,
    checked: StructuralChecks,
    checked_laws: BTreeSet<String>,
}
fn map(v: &JsonValue) -> Result<&BTreeMap<String, JsonValue>, GraphError> {
    if let JsonValue::Object(o) = v {
        Ok(o)
    } else {
        Err(GraphError::Law)
    }
}
fn string(v: &JsonValue) -> Result<&str, GraphError> {
    if let JsonValue::String(s) = v {
        Ok(s)
    } else {
        Err(GraphError::Law)
    }
}
fn member<'v>(v: &'v JsonValue, key: &str) -> Result<&'v JsonValue, GraphError> {
    map(v)?.get(key).ok_or(GraphError::Law)
}
fn digest(s: &str) -> Result<[u8; 32], GraphError> {
    if s.len() != 64
        || !s
            .bytes()
            .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
    {
        return Err(GraphError::Law);
    }
    let mut out = [0; 32];
    for (i, pair) in s.as_bytes().chunks_exact(2).enumerate() {
        let n = |b: u8| if b <= b'9' { b - b'0' } else { b - b'a' + 10 };
        out[i] = (n(pair[0]) << 4) | n(pair[1]);
    }
    Ok(out)
}
impl RetainedInputs<'_> {
    /// Diagnostic local relation checks only. Does not admit native facts or a
    /// complete closure; syntax capability and retained source/body joins remain.
    pub fn inspect_relation_payload(
        &self,
        sha: [u8; 32],
        schema_sha: [u8; 32],
        fact: &JsonValue,
        budget: TraversalBudget,
    ) -> Result<(), GraphError> {
        self.relation_payload_admission(sha, schema_sha, fact, budget, false)
            .map(|_| ())
    }
    /// Shape, ladder and anchor checks before the evaluator's syntax gate.
    /// Returns whether the source-bound relation row requires a body identity
    /// join. Rung fields, universe, source and body checks remain mandatory.
    pub fn inspect_relation_prefix(
        &self,
        sha: [u8; 32],
        schema_sha: [u8; 32],
        fact: &JsonValue,
        budget: TraversalBudget,
    ) -> Result<bool, GraphError> {
        self.relation_payload_admission(sha, schema_sha, fact, budget, true)
    }
    fn relation_payload_admission(
        &self,
        sha: [u8; 32],
        schema_sha: [u8; 32],
        fact: &JsonValue,
        budget: TraversalBudget,
        prefix_only: bool,
    ) -> Result<bool, GraphError> {
        let handle = self
            .registry
            .current_record_schema("foundation/relation-payload-schemas.v2.json", "")?;
        if handle.document_sha256() != schema_sha {
            return Err(GraphError::PayloadSchemaDocument);
        }
        let document = self
            .registry
            .document("opensip.product.relation-payload.2")
            .ok_or(GraphError::Law)?;
        let row = crate::relations::row(
            document,
            string(member(fact, "relation")?)?,
            budget.steps,
            budget.depth,
        )?;
        let blob = self.blob(sha)?;
        let value = blob.canonical_record()?;
        self.blob(schema_sha)?;
        let selector = string(member(row, "selector")?)?
            .strip_prefix('#')
            .ok_or(GraphError::Law)?;
        self.registry
            .current_record_schema("foundation/relation-payload-schemas.v2.json", selector)?
            .admit_json(blob.bytes(), budget.descriptor_work)?;
        if prefix_only {
            crate::relations::payload_prefix(row, fact)?;
        } else {
            crate::relations::payload_rules(&value, row, fact, budget.steps, budget.depth)?;
        }
        Ok(map(row)?.contains_key("bodyIdentityJoin"))
    }
    /// Inspect the local relation laws plus the owning snapshot inventory joins.
    /// This remains diagnostic: native capability, universe ownership and body
    /// identity joins are not established. A body join explicitly refuses here.
    pub fn inspect_relation_sources(
        &self,
        sha: [u8; 32],
        schema_sha: [u8; 32],
        fact: &JsonValue,
        budget: TraversalBudget,
    ) -> Result<(), GraphError> {
        self.inspect_relation_snapshot(sha, schema_sha, fact, budget)?;
        let document = self
            .registry
            .document("opensip.product.relation-payload.2")
            .ok_or(GraphError::Law)?;
        let row = crate::relations::row(
            document,
            string(member(fact, "relation")?)?,
            budget.steps,
            budget.depth,
        )?;
        if map(row)?.contains_key("bodyIdentityJoin") {
            return Err(GraphError::Unsupported("relation body identity owner"));
        }
        Ok(())
    }
    /// Local payload and snapshot checks only. Body/native owners and complete
    /// Run selection remain separate, mandatory obligations of the evaluator.
    pub fn inspect_relation_snapshot(
        &self,
        sha: [u8; 32],
        schema_sha: [u8; 32],
        fact: &JsonValue,
        budget: TraversalBudget,
    ) -> Result<(), GraphError> {
        self.inspect_relation_payload(sha, schema_sha, fact, budget)?;
        let document = self
            .registry
            .document("opensip.product.relation-payload.2")
            .ok_or(GraphError::Law)?;
        let row = crate::relations::row(
            document,
            string(member(fact, "relation")?)?,
            budget.steps,
            budget.depth,
        )?;
        let value = self.blob(sha)?.canonical_record()?;
        let snapshot = self.object(
            string(member(fact, "snapshotId")?)?,
            IdentityDomain::Snapshot,
            budget.descriptor_work,
        )?;
        let JsonValue::Array(inventory) = member(snapshot.descriptor(), "sourceInventory")? else {
            return Err(GraphError::Law);
        };
        let JsonValue::Array(joins) = member(row, "snapshotJoins")? else {
            return Err(GraphError::Law);
        };
        let mut steps = budget.steps;
        for join in joins {
            steps = steps.checked_sub(1).ok_or(GraphError::Limit)?;
            if let Some(unless) = map(join)?.get("unless") {
                let actual = map(&value)?
                    .get(string(member(unless, "field")?)?)
                    .unwrap_or(&JsonValue::Null);
                if actual == member(unless, "equals")? {
                    continue;
                }
            }
            let path = member(&value, string(member(join, "pathField")?)?)?;
            let mut selected = None;
            for item in inventory {
                steps = steps.checked_sub(1).ok_or(GraphError::Limit)?;
                if member(item, "path")? == path {
                    selected = Some(item);
                    break;
                }
            }
            let item = selected.ok_or(GraphError::RelationRule("path not inventoried"))?;
            if string(member(join, "form")?)? == "inventoried-file" {
                let claimed = member(&value, string(member(join, "digestField")?)?)?;
                if member(item, "sha256")? != claimed {
                    return Err(GraphError::RelationRule("file content join"));
                }
                let length = member(&value, string(member(join, "lengthField")?)?)?;
                if member(item, "bytes")? != length {
                    return Err(GraphError::RelationRule("file length join"));
                }
                let JsonValue::Integer(n) = length else {
                    return Err(GraphError::Law);
                };
                self.blob(digest(string(claimed)?)?)?
                    .require_length(u64::try_from(n.get()).map_err(|_| GraphError::Law)?)?;
            }
            if let Some(field) = map(join)?.get("anchorPathField") {
                let JsonValue::Array(anchors) = member(fact, "anchors")? else {
                    return Err(GraphError::Law);
                };
                for anchor in anchors {
                    steps = steps.checked_sub(1).ok_or(GraphError::Limit)?;
                    if member(anchor, "path")? != member(&value, string(field)?)? {
                        return Err(GraphError::RelationRule("anchor foreign path"));
                    }
                }
            }
        }
        Ok(())
    }
    /// Rehash one canonical identity-bundle record and check its schema and
    /// collection order. Returned data is inert: references are not traversed,
    /// and this is not a selected Plan, native owner, closure or replay proof.
    pub fn identity_record_shape(
        &self,
        sha: [u8; 32],
        kind: &str,
        work: usize,
    ) -> Result<JsonValue, GraphError> {
        let value = self.blob(sha)?.canonical_record()?;
        self.check_identity_value_shape(&value, kind, work)?;
        Ok(value)
    }
    /// Schema and collection-order diagnostics on inert data, including derived
    /// records which need not be retained. No identity, references or admission.
    pub fn check_identity_value_shape(
        &self,
        value: &JsonValue,
        kind: &str,
        work: usize,
    ) -> Result<(), GraphError> {
        let raw = canonical_bytes(value).map_err(|e| GraphError::Input(Error::Canonical(e)))?;
        self.registry
            .schema(IDENTITY_SCHEMA, &format!("/$defs/{kind}"))?
            .admit_json(&raw, work)?;
        if kind != "semantic-configuration" {
            crate::descriptors::ordered(
                value,
                match kind {
                    "source-inventory" => "sourceInventory",
                    "owner-source-set" => "owner-source-set",
                    _ => "",
                },
            )
            .map_err(|e| GraphError::Input(Error::Candidate(e)))?;
        }
        Ok(())
    }
    /// Check derived inert data against a fixed current schema. The registry
    /// still comes from exact embedded source pins; this grants no references,
    /// identity, provenance or semantic admission to a caller-supplied value.
    pub fn check_current_value_shape(
        &self,
        value: &JsonValue,
        document: &str,
        selector: &str,
        work: usize,
    ) -> Result<(), GraphError> {
        let handle = self
            .registry
            .current_record_schema(document, selector.strip_prefix('#').ok_or(GraphError::Law)?)?;
        let raw = canonical_bytes(value).map_err(|e| GraphError::Input(Error::Canonical(e)))?;
        handle.admit_json(&raw, work)?;
        Ok(())
    }
    /// Rehash a canonical record against an embedded current schema selector.
    /// Schema bytes are already bound by RegisteredSchemas; this does not invent
    /// a requirement that the record store retain the schema artifact itself.
    /// Returns inert shaped data, without reference traversal or owner admission.
    pub fn current_record_shape(
        &self,
        sha: [u8; 32],
        document: &str,
        selector: &str,
        work: usize,
    ) -> Result<JsonValue, GraphError> {
        let handle = self
            .registry
            .current_record_schema(document, selector.strip_prefix('#').ok_or(GraphError::Law)?)?;
        let blob = self.blob(sha)?;
        let value = blob.canonical_record()?;
        handle.admit_json(blob.bytes(), work)?;
        Ok(value)
    }
    /// Rehash a record and its exact selected schema document, checking canonical
    /// JSON and shape only. Returns inert data, not producer/owner admission.
    pub fn registered_record_shape(
        &self,
        sha: [u8; 32],
        schema_sha: [u8; 32],
        document: &str,
        selector: &str,
        work: usize,
    ) -> Result<JsonValue, GraphError> {
        let handle = self
            .registry
            .current_record_schema(document, selector.strip_prefix('#').ok_or(GraphError::Law)?)?;
        if handle.document_sha256() != schema_sha {
            return Err(GraphError::PayloadSchemaDocument);
        }
        self.blob(schema_sha)?;
        let blob = self.blob(sha)?;
        let value = blob.canonical_record()?;
        handle.admit_json(blob.bytes(), work)?;
        Ok(value)
    }
    /// Inspect a local identity-bundle record. The result describes structural
    /// checks only and does not establish that a Plan selected this record.
    pub fn inspect_identity_record(
        &self,
        sha: [u8; 32],
        kind: &str,
        budget: TraversalBudget,
    ) -> Result<StructuralChecks, GraphError> {
        let mut rejected = RejectOwner;
        let mut walker = Walker {
            owners: &mut rejected,
            inputs: self,
            budget,
            checked_laws: BTreeSet::new(),
            checked: StructuralChecks {
                objects: BTreeSet::new(),
                blobs: BTreeSet::new(),
                records: BTreeSet::new(),
                foreign: BTreeSet::new(),
            },
        };
        walker.local_record(sha, kind, 0)?;
        Ok(walker.checked)
    }
    /// Inspect one explicit current owner record and its supported references.
    /// Choosing this selector does not establish that a Plan selected the record.
    pub fn inspect_current_record(
        &self,
        sha: [u8; 32],
        document: &str,
        selector: &str,
        budget: TraversalBudget,
    ) -> Result<StructuralChecks, GraphError> {
        let mut rejected = RejectOwner;
        self.inspect_current_record_with_owner(sha, document, selector, budget, &mut rejected)
    }
    /// Inspect a current record with an explicit diagnostic owner. A callback
    /// cannot establish complete evaluator admission or mint replay authority.
    pub fn inspect_current_record_with_owner(
        &self,
        sha: [u8; 32],
        document: &str,
        selector: &str,
        budget: TraversalBudget,
        owners: &mut dyn StructuralOwner,
    ) -> Result<StructuralChecks, GraphError> {
        let mut walker = Walker {
            owners,
            inputs: self,
            budget,
            checked_laws: BTreeSet::new(),
            checked: StructuralChecks {
                objects: BTreeSet::new(),
                blobs: BTreeSet::new(),
                records: BTreeSet::new(),
                foreign: BTreeSet::new(),
            },
        };
        walker.foreign_record(sha, document, selector, 0)?;
        Ok(walker.checked)
    }
    pub fn inspect_local_structure(
        &self,
        key: &str,
        domain: IdentityDomain,
        budget: TraversalBudget,
    ) -> Result<StructuralChecks, GraphError> {
        let mut rejected = RejectOwner;
        let mut walker = Walker {
            owners: &mut rejected,
            inputs: self,
            budget,
            checked_laws: BTreeSet::new(),
            checked: StructuralChecks {
                objects: BTreeSet::new(),
                blobs: BTreeSet::new(),
                records: BTreeSet::new(),
                foreign: BTreeSet::new(),
            },
        };
        walker.visit(key, domain, 0)?;
        Ok(walker.checked)
    }
    /// Inspect with an explicit diagnostic owner. This API does not establish
    /// that the callback discharged semantic obligations or ran later phases.
    /// It must never be used as a substitute for a fixed evaluator composition.
    pub fn inspect_structure_with_owner(
        &self,
        key: &str,
        domain: IdentityDomain,
        budget: TraversalBudget,
        owners: &mut dyn StructuralOwner,
    ) -> Result<StructuralChecks, GraphError> {
        let mut walker = Walker {
            inputs: self,
            owners,
            budget,
            checked_laws: BTreeSet::new(),
            checked: StructuralChecks {
                objects: BTreeSet::new(),
                blobs: BTreeSet::new(),
                records: BTreeSet::new(),
                foreign: BTreeSet::new(),
            },
        };
        walker.visit(key, domain, 0)?;
        Ok(walker.checked)
    }
}
impl Walker<'_, '_> {
    fn spend(&mut self, depth: usize) -> Result<(), GraphError> {
        if depth > self.budget.depth {
            return Err(GraphError::Limit);
        }
        self.budget.steps = self.budget.steps.checked_sub(1).ok_or(GraphError::Limit)?;
        Ok(())
    }
    fn document(&self, owner: &str) -> Result<&JsonValue, GraphError> {
        self.inputs.registry.document(owner).ok_or(GraphError::Law)
    }
    fn definition(&self, owner: &str, name: &str) -> Result<&JsonValue, GraphError> {
        member(member(self.document(owner)?, "$defs")?, name)
    }
    fn visit(&mut self, key: &str, domain: IdentityDomain, depth: usize) -> Result<(), GraphError> {
        self.spend(depth)?;
        if self.checked.objects.contains(key) {
            return Ok(());
        }
        let candidate = self
            .inputs
            .object(key, domain, self.budget.descriptor_work)?;
        let value = candidate.descriptor();
        let schema = self.definition(IDENTITY_SCHEMA, domain.name())?.clone();
        self.owners.object(key, domain, value)?;
        self.checked.objects.insert(key.to_string());
        self.walk(IDENTITY_SCHEMA, &schema, value, None, depth + 1)
    }
    fn blob(&mut self, sha: [u8; 32], depth: usize) -> Result<(), GraphError> {
        self.spend(depth)?;
        self.inputs.blob(sha)?;
        self.checked.blobs.insert(sha);
        Ok(())
    }
    fn dereference(&self, owner: &str, node: &JsonValue) -> Result<JsonValue, GraphError> {
        let mut node = node.clone();
        let mut count = 0;
        loop {
            let Some(reference) = map(&node)?.get("$ref") else {
                return Ok(node);
            };
            let name = string(reference)?
                .strip_prefix("#/$defs/")
                .ok_or(GraphError::Law)?;
            let mut merged = map(self.definition(owner, name)?)?.clone();
            for (k, v) in map(&node)? {
                if k != "$ref" {
                    merged.insert(k.clone(), v.clone());
                }
            }
            node = JsonValue::Object(merged);
            count += 1;
            if count > 8 {
                return Err(GraphError::Law);
            }
        }
    }
    fn carries_digest(
        &mut self,
        owner: &str,
        node: &JsonValue,
        depth: usize,
    ) -> Result<bool, GraphError> {
        self.spend(depth)?;
        match node {
            JsonValue::Object(o) => {
                if o.contains_key("x-opensip-digest") {
                    return Ok(true);
                }
                if let Some(JsonValue::String(p)) = o.get("pattern")
                    && let Some(head) = p
                        .strip_prefix('^')
                        .and_then(|p| p.split_once(':').map(|p| p.0))
                    && printed_domain(head).is_some()
                {
                    return Ok(true);
                }
                if let Some(JsonValue::String(r)) = o.get("$ref")
                    && let Some(name) = r.strip_prefix("#/$defs/")
                {
                    let child = self.definition(owner, name)?.clone();
                    return self.carries_digest(owner, &child, depth + 1);
                }
                for child in o.values() {
                    if self.carries_digest(owner, child, depth + 1)? {
                        return Ok(true);
                    }
                }
                Ok(false)
            }
            JsonValue::Array(a) => {
                for child in a {
                    if self.carries_digest(owner, child, depth + 1)? {
                        return Ok(true);
                    }
                }
                Ok(false)
            }
            _ => Ok(false),
        }
    }
    fn branch_matches(
        &self,
        owner: &str,
        node: &JsonValue,
        value: &JsonValue,
    ) -> Result<bool, GraphError> {
        // Preserve the selected owner's root assertions followed by the branch
        // overlay, exactly as the reference branch discriminator does.
        let mut combined: BTreeMap<_, _> = map(self.document(owner)?)?
            .iter()
            .filter(|(k, _)| k.as_str() != "$defs" && k.as_str() != "$ref")
            .map(|(k, v)| (k.clone(), v.clone()))
            .collect();
        combined.extend(map(node)?.clone());
        self.inputs
            .registry
            .matches_node(
                owner,
                &JsonValue::Object(combined),
                value,
                self.budget.descriptor_work,
            )
            .map_err(GraphError::Interpretation)
    }
    fn walk(
        &mut self,
        owner: &str,
        node: &JsonValue,
        value: &JsonValue,
        siblings: Option<&JsonValue>,
        depth: usize,
    ) -> Result<(), GraphError> {
        self.spend(depth)?;
        let mut node = self.dereference(owner, node)?;
        if let Some(JsonValue::Array(branches)) = map(&node)?.get("oneOf") {
            let mut matches = Vec::new();
            let mut options = Vec::new();
            for branch in branches {
                let option = self.dereference(owner, branch)?;
                if self.branch_matches(owner, &option, value)? {
                    matches.push(option.clone())
                }
                options.push(option)
            }
            if matches.len() != 1 {
                for option in &options {
                    if self.carries_digest(owner, option, depth + 1)? {
                        return Err(GraphError::AmbiguousBranch);
                    }
                }
                return Ok(());
            }
            let JsonValue::Object(ref mut merged) = node else {
                return Err(GraphError::Law);
            };
            merged.remove("oneOf");
            merged.extend(map(&matches[0])?.clone());
        }
        let schema = map(&node)?;
        match value {
            JsonValue::Null => Ok(()),
            JsonValue::String(text) => {
                if let Some(annotation) = schema.get("x-opensip-digest") {
                    return self.digest_field(annotation, text, siblings, depth + 1);
                }
                if let Some((prefix, _)) = text.split_once(':')
                    && let Some(domain) = printed_domain(prefix)
                    && matches!(schema.get("pattern"),Some(JsonValue::String(p)) if p.starts_with(&format!("^{prefix}:")))
                {
                    return self.visit(text, domain, depth + 1);
                }
                Ok(())
            }
            JsonValue::Array(a) => {
                let Some(items) = schema.get("items") else {
                    if self.carries_digest(owner, &node, depth + 1)? {
                        return Err(GraphError::UntypedDigestArray);
                    }
                    return Ok(());
                };
                for item in a {
                    self.walk(owner, items, item, siblings, depth + 1)?
                }
                Ok(())
            }
            JsonValue::Object(o) => {
                let properties = schema.get("properties").map(map).transpose()?;
                for (name, child) in o {
                    let selected = properties.and_then(|p| p.get(name)).or_else(|| {
                        schema
                            .get("additionalProperties")
                            .filter(|v| matches!(v, JsonValue::Object(_)))
                    });
                    match selected {
                        Some(s) => self.walk(owner, s, child, Some(value), depth + 1)?,
                        None => {
                            if self.carries_digest(owner, &node, depth + 1)? {
                                return Err(GraphError::UndeclaredDigestProperty);
                            }
                        }
                    }
                }
                if o.len() == 3
                    && o.contains_key("path")
                    && o.contains_key("sha256")
                    && o.contains_key("bytes")
                {
                    let sha = digest(string(&o["sha256"])?)?;
                    let JsonValue::Integer(n) = o["bytes"] else {
                        return Err(GraphError::Law);
                    };
                    self.inputs
                        .blob(sha)?
                        .require_length(u64::try_from(n.get()).map_err(|_| GraphError::Law)?)?;
                    self.checked.blobs.insert(sha);
                }
                Ok(())
            }
            _ => Ok(()),
        }
    }
    fn digest_field(
        &mut self,
        annotation: &JsonValue,
        text: &str,
        siblings: Option<&JsonValue>,
        depth: usize,
    ) -> Result<(), GraphError> {
        self.spend(depth)?;
        let row = map(annotation)?;
        let retention = row
            .get("retention")
            .map(string)
            .transpose()?
            .unwrap_or("preimage");
        if !["preimage", "fragment", "derived", "owner-retained"].contains(&retention) {
            return Err(GraphError::Law);
        }
        // These are obligations for later owner joins, not proven by an empty lookup.
        if matches!(retention, "fragment" | "owner-retained") {
            return self.owners.resolve(StructuralObligation::Retention {
                annotation,
                value: text,
                siblings,
            });
        }
        match string(member(annotation, "representation")?)? {
            "raw-artifact" => {
                let sha = digest(text)?;
                self.blob(sha, depth + 1)?;
                if let Some(class) = row.get("artifactClass") {
                    match string(class)? {
                        "registered-schema-document" => {
                            self.inputs.registered_schema_blob(sha)?;
                        }
                        "producer-interface-stage-output-schema" => {
                            return self.owners.resolve(StructuralObligation::StageSchema {
                                digest: sha,
                                siblings,
                            });
                        }
                        _ => return Err(GraphError::Law),
                    }
                }
                Ok(())
            }
            "capability-manifest-id" => self.owners.resolve(StructuralObligation::Capability(text)),
            "by-domain" => {
                let siblings = siblings.ok_or(GraphError::Law)?;
                let domain = string(member(siblings, "domain")?)?;
                let rules = member(
                    member(self.document(IDENTITY_SCHEMA)?, "x-opensip-digest-domains")?,
                    "byDomain",
                )?;
                let rule = member(rules, domain)?.clone();
                self.digest_field(&rule, text, Some(siblings), depth + 1)
            }
            "h-identity" => {
                if let Some(domain) = row.get("domain") {
                    // The selected feature owner retains this exact preimage
                    // inline. It is neither a core object nor a separate frame.
                    if string(domain)? == "native.framework-recognition.v1" {
                        if retention != "derived"
                            || row.get("form").map(string).transpose()? != Some("sha256-text")
                        {
                            return Err(GraphError::Law);
                        }
                        let recognition = member(siblings.ok_or(GraphError::Law)?, "recognition")?;
                        let expected = crate::hash_canonical_value(
                            "native.framework-recognition.v1",
                            recognition,
                        )
                        .map_err(GraphError::Frame)?;
                        if text != format!("sha256:{}", crate::digest_hex(&expected)) {
                            return Err(GraphError::DerivedIdentity);
                        }
                        return Ok(());
                    }
                    let domain =
                        IdentityDomain::parse(string(domain)?).map_err(|_| GraphError::Law)?;
                    self.visit(&format!("{}:{text}", domain.prefix()), domain, depth + 1)
                } else {
                    self.owners.resolve(StructuralObligation::NativeFrame {
                        value: text,
                        set: string(member(annotation, "domainSet")?)?,
                    })
                }
            }
            "canonical-record" => {
                let record = member(annotation, "record")?;
                if map(record)?.contains_key("bundle") {
                    let selector = string(member(record, "selector")?)?;
                    let kind = selector.strip_prefix("#/$defs/").ok_or(GraphError::Law)?;
                    self.local_record(digest(text)?, kind, depth + 1)
                } else if let Some(document) = map(record)?.get("document") {
                    self.foreign_record(
                        digest(text)?,
                        string(document)?,
                        string(member(record, "selector")?)?,
                        depth + 1,
                    )
                } else {
                    if map(record)?.contains_key("resolvedThrough") {
                        return Err(GraphError::Law);
                    }
                    let class = string(member(record, "payloadClass")?)?;
                    if !["parameter", "coverage"].contains(&class) {
                        return self.owners.resolve(StructuralObligation::Payload {
                            digest: digest(text)?,
                            record,
                            siblings: siblings.ok_or(GraphError::Law)?,
                        });
                    }
                    self.registered_payload(
                        digest(text)?,
                        record,
                        siblings.ok_or(GraphError::Law)?,
                        depth + 1,
                    )
                }
            }
            _ => Err(GraphError::Law),
        }
    }
    fn local_record(&mut self, sha: [u8; 32], kind: &str, depth: usize) -> Result<(), GraphError> {
        self.spend(depth)?;
        let key = (sha, kind.to_string());
        if self.checked.records.contains(&key) {
            return Ok(());
        }
        self.blob(sha, depth + 1)?;
        let blob = self.inputs.blob(sha)?;
        let value = blob.canonical_record()?;
        self.inputs
            .registry
            .schema(IDENTITY_SCHEMA, &format!("/$defs/{kind}"))?
            .admit_json(blob.bytes(), self.budget.descriptor_work)?;
        if kind != "semantic-configuration" {
            crate::descriptors::ordered(
                &value,
                match kind {
                    "source-inventory" => "sourceInventory",
                    "owner-source-set" => "owner-source-set",
                    _ => "",
                },
            )
            .map_err(|e| GraphError::Input(Error::Candidate(e)))?
        }
        if kind == "scope-descriptor" {
            for field in ["workspaceRoots", "pathPrefixes", "excludedPathPrefixes"] {
                let JsonValue::Array(paths) = member(&value, field)? else {
                    return Err(GraphError::Law);
                };
                for raw in paths {
                    let path = string(raw)?;
                    if path != "." && !crate::descriptors::path(path) {
                        return Err(GraphError::Input(Error::Candidate(
                            CandidateError::LogicalPath,
                        )));
                    }
                }
            }
        }
        if kind == "stage-spec" {
            let reference = string(member(&value, "producerClosure")?)?;
            let closure = self.inputs.candidate(
                reference,
                IdentityDomain::Closure,
                self.budget.descriptor_work,
            )?;
            if string(member(closure.descriptor(), "kind")?)? != "provider" {
                return Err(GraphError::Input(Error::ClosureRole {
                    field: "producerClosure",
                    expected: "provider",
                }));
            }
        }
        self.checked.records.insert(key);
        let schema = self.definition(IDENTITY_SCHEMA, kind)?.clone();
        self.walk(IDENTITY_SCHEMA, &schema, &value, None, depth + 1)
    }

    fn foreign_record(
        &mut self,
        sha: [u8; 32],
        document: &str,
        selector: &str,
        depth: usize,
    ) -> Result<(), GraphError> {
        self.spend(depth)?;
        let key = (sha, document.to_string(), selector.to_string());
        if self.checked.foreign.contains(&key) {
            return Ok(());
        }
        self.blob(sha, depth + 1)?;
        let blob = self.inputs.blob(sha)?;
        let value = blob.canonical_record()?;
        let pointer = selector.strip_prefix('#').unwrap_or(selector);
        let handle = self
            .inputs
            .registry
            .current_record_schema(document, pointer)?;
        let owner = handle.schema_id();
        handle.admit_json(blob.bytes(), self.budget.descriptor_work)?;
        self.checked.foreign.insert(key);
        if document.starts_with("foundation/") {
            self.foundation_digest_law(document, owner, depth + 1)?;
            let mut selected = self.document(owner)?;
            if !pointer.is_empty() {
                for token in pointer.strip_prefix('/').ok_or(GraphError::Law)?.split('/') {
                    let token = token.replace("~1", "/").replace("~0", "~");
                    selected = member(selected, &token)?;
                }
            }
            let selected = selected.clone();
            self.walk(owner, &selected, &value, None, depth + 1)?;
        }
        Ok(())
    }

    fn registered_payload(
        &mut self,
        sha: [u8; 32],
        record: &JsonValue,
        siblings: &JsonValue,
        depth: usize,
    ) -> Result<(), GraphError> {
        self.spend(depth)?;
        let class = string(member(record, "payloadClass")?)?;
        let schema_field = string(member(record, "schemaDigestField")?)?;
        let schema_sha = digest(string(member(siblings, schema_field)?)?)?;
        self.blob(sha, depth + 1)?;
        let blob = self.inputs.blob(sha)?;
        let value = blob.canonical_record()?;
        let JsonValue::Array(key_names) = member(record, "keyedBy")? else {
            return Err(GraphError::Law);
        };
        let mut keys = Vec::new();
        for key in key_names {
            let key = string(key)?;
            let v = if let Some(field) = key.strip_prefix("payload.") {
                map(&value)?
                    .get(field)
                    .ok_or(GraphError::PayloadRegistryRow)?
            } else {
                member(siblings, key)?
            };
            keys.push(v);
        }
        if keys.len() != 1 {
            return Err(GraphError::PayloadRegistryRow);
        }
        let classes = member(
            member(
                self.document(IDENTITY_SCHEMA)?,
                "x-opensip-payload-registry",
            )?,
            "classes",
        )?;
        let rows = map(member(member(classes, class)?, "rows")?)?;
        let row = if class == "parameter" {
            let selected = digest(string(keys[0])?)?;
            let mut matches = Vec::new();
            for row in rows.values() {
                let document = string(member(row, "document")?)?;
                if self
                    .inputs
                    .registry
                    .current_record_schema(document, "")?
                    .document_sha256()
                    == selected
                {
                    matches.push(row);
                }
            }
            match matches.len() {
                0 => return Err(GraphError::PayloadRegistryRow),
                1 => matches[0].clone(),
                _ => return Err(GraphError::AmbiguousPayloadRegistryRow),
            }
        } else {
            let key = match keys[0] {
                JsonValue::String(s) => s.clone(),
                JsonValue::Integer(i) => i.get().to_string(),
                _ => return Err(GraphError::PayloadRegistryRow),
            };
            rows.get(&key)
                .ok_or(GraphError::PayloadRegistryRow)?
                .clone()
        };
        let document = string(member(&row, "document")?)?;
        let selector = string(member(&row, "selector")?)?;
        let handle = self
            .inputs
            .registry
            .current_record_schema(document, selector.strip_prefix('#').ok_or(GraphError::Law)?)?;
        // This entire context selection/admission runs on EVERY reference.
        // A previous decode or foreign-record walk cannot authorize a new row.
        if handle.document_sha256() != schema_sha {
            return Err(GraphError::PayloadSchemaDocument);
        }
        self.blob(schema_sha, depth + 1)?;
        let raw = self.inputs.blob(sha)?;
        handle.admit_json(raw.bytes(), self.budget.descriptor_work)?;
        if class == "parameter" && document.starts_with("foundation/") {
            self.foreign_record(sha, document, selector, depth + 1)?;
        }
        Ok(())
    }

    fn foundation_digest_law(
        &mut self,
        document: &str,
        owner: &str,
        depth: usize,
    ) -> Result<(), GraphError> {
        self.spend(depth)?;
        // These exact bundles have a separate selected annotation sweep.
        if [
            "foundation/identity-schemas.v2.json",
            "foundation/identity-schemas.v3.json",
            "foundation/relation-payload-schemas.v2.json",
        ]
        .contains(&document)
            || self.checked_laws.contains(document)
        {
            return Ok(());
        }
        let schema = self.document(owner)?.clone();
        let defs = map(&schema)?.get("$defs").map(map).transpose()?;
        let bare = "^[0-9a-f]{64}(?![\\s\\S])";
        let hex_defs: BTreeSet<String> = defs.into_iter().flat_map(|d|d.iter())
            .filter(|(_,v)| matches!(v,JsonValue::Object(o) if matches!(o.get("pattern"),Some(JsonValue::String(p)) if p==bare)))
            .map(|(k,_)|k.clone()).collect();
        let root = JsonValue::Object(
            map(&schema)?
                .iter()
                .filter(|(k, _)| k.as_str() != "$defs")
                .map(|(k, v)| (k.clone(), v.clone()))
                .collect(),
        );
        self.digest_coverage_node(owner, &root, &hex_defs, false, &[], depth + 1)?;
        if let Some(defs) = defs {
            for (name, node) in defs {
                if !hex_defs.contains(name) {
                    self.digest_coverage_node(owner, node, &hex_defs, false, &[], depth + 1)?;
                }
            }
        }
        self.checked_laws.insert(document.to_string());
        Ok(())
    }

    fn digest_coverage_node(
        &mut self,
        owner: &str,
        node: &JsonValue,
        hex_defs: &BTreeSet<String>,
        covered: bool,
        chain: &[String],
        depth: usize,
    ) -> Result<(), GraphError> {
        self.spend(depth)?;
        if let JsonValue::Array(values) = node {
            for value in values {
                self.digest_coverage_node(owner, value, hex_defs, covered, chain, depth + 1)?;
            }
            return Ok(());
        }
        let JsonValue::Object(o) = node else {
            return Ok(());
        };
        let covered = covered || o.contains_key("x-opensip-digest");
        let reference = o.get("$ref").and_then(|v| {
            if let JsonValue::String(s) = v {
                Some(s.as_str())
            } else {
                None
            }
        });
        let local = reference.and_then(|s| s.strip_prefix("#/$defs/"));
        if matches!(o.get("pattern"),Some(JsonValue::String(p)) if p=="^[0-9a-f]{64}(?![\\s\\S])")
            || local.is_some_and(|s| hex_defs.contains(s))
        {
            return if covered {
                Ok(())
            } else {
                Err(GraphError::UnannotatedFoundationDigest)
            };
        }
        if let Some(name) = local {
            let reference = reference.ok_or(GraphError::Law)?;
            if !chain.iter().any(|s| s == reference) {
                let defs = map(member(self.document(owner)?, "$defs")?)?;
                if let Some(child) = defs.get(name) {
                    let child = child.clone();
                    let mut next = chain.to_vec();
                    next.push(reference.into());
                    self.digest_coverage_node(owner, &child, hex_defs, covered, &next, depth + 1)?;
                }
            }
        }
        for (key, child) in o {
            match key.as_str() {
                "properties" => {
                    if let JsonValue::Object(props) = child {
                        for schema in props.values() {
                            self.digest_coverage_node(
                                owner,
                                schema,
                                hex_defs,
                                covered,
                                &[],
                                depth + 1,
                            )?;
                        }
                    }
                }
                "items" | "additionalProperties" => {
                    self.digest_coverage_node(owner, child, hex_defs, covered, &[], depth + 1)?
                }
                "oneOf" | "anyOf" | "allOf" => {
                    if let JsonValue::Array(branches) = child {
                        for branch in branches {
                            self.digest_coverage_node(
                                owner,
                                branch,
                                hex_defs,
                                covered,
                                &[],
                                depth + 1,
                            )?;
                        }
                    }
                }
                _ => (),
            }
        }
        Ok(())
    }
}
fn printed_domain(prefix: &str) -> Option<IdentityDomain> {
    let name = match prefix {
        "fact2" => "fact",
        "snapshot2" => "snapshot",
        "closure2" => "closure",
        "import2" => "import",
        "plan2" => "plan",
        "scope2" => "subject-scope",
        "coverage2" => "coverage",
        "view2" => "view",
        "exec-plan2" => "execution-plan",
        "finding-key2" => "finding-fingerprint",
        "finding3" => "finding",
        "proof3" => "proof-bundle",
        "evidence3" => "semantic-evidence",
        "seal3" => "evaluation-seal",
        "run3" => "run",
        "cache2" => "cache-key",
        "regen2" => "regeneration-key",
        "policy-derivation3" => "policy-derivation",
        "subject3" => "evaluation-subject",
        _ => return None,
    };
    IdentityDomain::parse(name).ok()
}

/// Closed identity-v3 frame sets. Membership is distinct from native semantic
/// admission, nested retention, snapshot joins and universe binding.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum NativeFrameSet {
    Context,
    SemanticUniverse,
    Nested,
}
impl NativeFrameSet {
    pub fn name(self) -> &'static str {
        match self {
            Self::Context => "native-context",
            Self::SemanticUniverse => "native-semantic-universe",
            Self::Nested => "native-nested",
        }
    }
}

/// Exact retained frame and current registered shape only. No native ADMIT
/// status, selected Plan, complete closure or replay authority is represented.
pub struct FramedCandidate<'a> {
    digest: [u8; 32],
    domain: String,
    set: NativeFrameSet,
    row: JsonValue,
    shape: crate::ShapeValue<'a>,
}
impl FramedCandidate<'_> {
    pub fn digest(&self) -> [u8; 32] {
        self.digest
    }
    pub fn domain(&self) -> &str {
        &self.domain
    }
    pub fn domain_set(&self) -> NativeFrameSet {
        self.set
    }
    pub fn descriptor(&self) -> &JsonValue {
        self.shape.value()
    }
    pub fn schema(&self) -> &crate::SchemaHandle<'_> {
        self.shape.schema()
    }
    /// The selected immutable contract row names the still-outstanding joins.
    pub fn registry_row(&self) -> &JsonValue {
        &self.row
    }
}

impl<'a> RetainedInputs<'a> {
    /// Current-contract framing and shape, using the exact selected alias. A
    /// historical-profile reader requires a separately bound implementation.
    pub fn frame_candidate(
        &self,
        sha: [u8; 32],
        set: NativeFrameSet,
        budget: usize,
    ) -> Result<FramedCandidate<'a>, GraphError> {
        let blob = self.blob(sha)?;
        let rest = blob
            .bytes()
            .strip_prefix(b"opensip.product.v1\0")
            .ok_or(GraphError::Frame(crate::DigestError::FramePrefix))?;
        let cut = rest
            .iter()
            .position(|b| *b == 0)
            .filter(|i| *i > 0)
            .ok_or(GraphError::Frame(crate::DigestError::FrameDomain))?;
        let domain = core::str::from_utf8(&rest[..cut])
            .map_err(|_| GraphError::Frame(crate::DigestError::FrameDomain))?;
        if !domain.is_ascii() {
            return Err(GraphError::Frame(crate::DigestError::FrameDomain));
        }
        let identity = self
            .registry
            .document(IDENTITY_SCHEMA)
            .ok_or(GraphError::Law)?;
        let sets = member(member(identity, "x-opensip-digest-domains")?, "domainSets")?;
        let row = map(member(sets, set.name())?)?
            .get(domain)
            .ok_or(GraphError::UnregisteredFrameDomain)?
            .clone();
        let value = crate::parse_hash_preimage(domain, blob.bytes()).map_err(GraphError::Frame)?;
        let raw = canonical_bytes(&value).map_err(|e| GraphError::Input(Error::Canonical(e)))?;
        let document = string(member(&row, "document")?)?;
        let selector = string(member(&row, "selector")?)?;
        let selector = selector.strip_prefix('#').ok_or(GraphError::Law)?;
        let shape = self
            .registry
            .current_record_schema(document, selector)?
            .admit_json(&raw, budget)?;
        if crate::hash_canonical_value(domain, shape.value()).map_err(GraphError::Frame)? != sha {
            return Err(GraphError::Input(Error::BlobDigest));
        }
        Ok(FramedCandidate {
            digest: sha,
            domain: domain.into(),
            set,
            row,
            shape,
        })
    }

    /// Rehash the supplied schema blob and establish membership in the selected
    /// identity payload registry's document set (not all 48 available schemas).
    pub fn registered_schema_blob(&self, sha: [u8; 32]) -> Result<RetainedBlob<'_>, GraphError> {
        let blob = self.blob(sha)?;
        let identity = self
            .registry
            .document(IDENTITY_SCHEMA)
            .ok_or(GraphError::Law)?;
        let classes = member(member(identity, "x-opensip-payload-registry")?, "classes")?;
        let mut documents = BTreeSet::new();
        for body in map(classes)?.values() {
            if let Some(document) = map(body)?.get("document") {
                documents.insert(string(document)?);
            }
            if let Some(rows) = map(body)?.get("rows") {
                for row in map(rows)?.values() {
                    documents.insert(string(member(row, "document")?)?);
                }
            }
        }
        for document in documents {
            if self
                .registry
                .current_record_schema(document, "")?
                .document_sha256()
                == sha
            {
                return Ok(blob);
            }
        }
        Err(GraphError::UnregisteredSchemaDocument)
    }
}
