//! Fresh host reconstruction of Rust subjects and requested Coverage domains.
//! Inputs are the admitted Plan's immutable projections. These inert values
//! do not perform C1 custody, C4 Plan admission, scope2 minting or H settlement.
use super::super::super::{
    built_commitment,
    cbor::{self, Value},
    ts2::{
        carrier::{self, Carriers, field},
        top_level_member,
    },
};
use opensip_identity::{JsonValue as J, RawSha256, digest_hex, parse_json, raw_sha256};
use std::collections::{BTreeMap, BTreeSet};

const RPP: &[u8] = include_bytes!("../../../../data/rust-provider-protocol.v2.json");
const PLANE: &[u8] = include_bytes!("../../../../data/fact-plane.v1.json");
const REGISTRY: &[u8] = include_bytes!("../../../../data/relation-payload-schemas.v2.json");
const PROJECTION: &str = "28b7df5d1b2bc1a7390993f6468eca78786972877fbc18e82d6062f693678fd5";
const SOURCE_DOMAIN: &str = "opensip.rust-provider.universe.v2";
const GENERIC_DOMAIN: &str = "opensip.semantic-universe.v2";
const SUBJECT_DOMAIN: &str = "opensip.rust-provider.subject.v2";
const SCOPE_DOMAIN: &str = "opensip.rust-provider.subject-scope.v2";
const ANALYSIS_DOMAIN: &str = "opensip.rust-provider.analysis-domain.v2";

#[derive(Debug, PartialEq, Eq)]
pub(super) enum Refusal {
    Law(String),
    Schema(String),
    Input(&'static str),
    InlineSubjectLimit,
    Bound(&'static str),
    Arithmetic,
}
#[derive(Debug)]
pub(super) struct File {
    pub path: String,
    pub byte_length: u64,
    pub content_sha256: String,
}
#[derive(Debug)]
pub struct Universe {
    pub provider_id: String,
    pub provider_version: String,
    pub value: Value,
}
/// The exact per-key scope2 cells minted before spawn by C4. The codec
/// places these cells; it must not replace them with Rust's whole-subject
/// commitment (PER-KEY-SCOPE2). H consumes the same owned descriptors later.
#[derive(Debug)]
pub struct Scope {
    pub relation: String,
    pub resolution: String,
    pub source: String,
    pub target: String,
    pub commitment: String,
}
#[derive(Debug)]
pub struct Stage {
    pub plan_stage: Value,
    /// The verified Plan's resolved provider, including any C2 default. It
    /// is separate from optional literal members, which must stay absent.
    pub resolved_provider: Option<String>,
    pub scopes: Vec<Scope>,
}
#[derive(Debug, Clone, Copy)]
pub(super) struct Bounds {
    pub snapshot_entries: u64,
    pub inline_subjects: u64,
    pub stages: u64,
    pub keys_per_stage: u64,
}
#[derive(Debug)]
pub(super) struct DerivedStage {
    pub plan_stage: Value,
    pub keys: Value,
    pub domain_commitment: String,
}
#[derive(Debug)]
pub(super) struct Derived {
    pub source_universe_id: String,
    pub target_domain: BTreeSet<String>,
    pub subjects: Value,
    pub subject_scope: Value,
    pub stages: Vec<DerivedStage>,
}
pub(super) struct Input<'a> {
    pub snapshot: &'a str,
    pub files: &'a [File],
    pub universes: &'a [Universe],
    pub selected: usize,
    pub provider_build_id: &'a str,
    pub plan_stages: &'a [Stage],
    pub bounds: Bounds,
    pub reference: bool,
}
/// Exact echoes of the admitted OpenUniverse and chosen Analyze ordinal.
/// These values do not perform the parent builder's OpenUniverse joins.
pub(super) struct AnalyzeContext<'a> {
    pub execution_id: &'a str,
    pub snapshot_id: &'a str,
    pub plan_id: &'a str,
    pub analysis_ordinal: u64,
}
struct Relation {
    ladder: Vec<String>,
    same_only: bool,
    schema_version: u64,
}
pub(super) struct Law {
    carriers: Carriers,
    relations: BTreeMap<String, Relation>,
}
fn obj(v: &J) -> Option<&BTreeMap<String, J>> {
    if let J::Object(x) = v { Some(x) } else { None }
}
fn text(v: &J) -> Option<&str> {
    if let J::String(x) = v { Some(x) } else { None }
}
fn at<'a>(v: &'a J, path: &[&str]) -> Option<&'a J> {
    path.iter().try_fold(v, |v, k| obj(v)?.get(*k))
}
fn strings(v: &J) -> Option<Vec<String>> {
    if let J::Array(a) = v {
        a.iter().map(|v| text(v).map(str::to_owned)).collect()
    } else {
        None
    }
}
fn map(rows: Vec<(&str, Value)>) -> Value {
    Value::Map(rows.into_iter().map(|(k, v)| (k.to_owned(), v)).collect())
}
fn t(s: &str) -> Value {
    Value::Text(s.to_owned())
}
fn member<'a>(v: &'a Value, key: &str) -> Option<&'a Value> {
    if let Value::Map(m) = v {
        field(m, key)
    } else {
        None
    }
}
fn value_text<'a>(v: &'a Value, key: &str) -> Option<&'a str> {
    if let Some(Value::Text(t)) = member(v, key) {
        Some(t)
    } else {
        None
    }
}
fn schema_error(e: String) -> Refusal {
    Refusal::Schema(e)
}

impl Law {
    pub(super) fn load() -> Result<Self, Refusal> {
        let c =
            parse_json(carrier::CARRIERS).map_err(|e| Refusal::Law(format!("carriers: {e}")))?;
        let Some(J::Array(pins)) = at(&c, &["sourcePins"]) else {
            return Err(Refusal::Input("source pins"));
        };
        for (key, bytes) in [
            ("rust2", RPP),
            ("factPlane", PLANE),
            ("relationRegistry2", REGISTRY),
        ] {
            let matching: Vec<_> = pins
                .iter()
                .filter(|p| at(p, &["key"]).and_then(text) == Some(key))
                .collect();
            if matching.len() != 1
                || at(matching[0], &["sha256"]).and_then(text)
                    != Some(digest_hex(&raw_sha256(bytes)).as_str())
            {
                return Err(Refusal::Input("selected source pin"));
            }
        }
        // This is the precise selected algorithm implemented below, not a
        // generic interpretation of future rule prose. Changed recipes need
        // their own implementation/control review rather than a loose load.
        let projection =
            top_level_member(RPP, "planAndDomainProjection").ok_or(Refusal::Input("projection"))?;
        if digest_hex(&raw_sha256(projection)) != PROJECTION {
            return Err(Refusal::Input("unimplemented projection recipe"));
        }
        let commitments = parse_json(
            top_level_member(RPP, "commitments").ok_or(Refusal::Input("commitment recipes"))?,
        )
        .map_err(|e| Refusal::Law(format!("commitments: {e}")))?;
        for (name, expected) in [
            (
                "subjectScope",
                "sha256:hex(SHA-256(UTF8(opensip.rust-provider.subject-scope.v2) || 0x00 || deterministic-CBOR(subjects)))",
            ),
            (
                "analysisDomain",
                "sha256:hex(SHA-256(UTF8(opensip.rust-provider.analysis-domain.v2) || 0x00 || deterministic-CBOR({subjects,requestedCoverageDomain})))",
            ),
        ] {
            if at(&commitments, &[name]).and_then(text) != Some(expected) {
                return Err(Refusal::Input("unimplemented commitment recipe"));
            }
        }
        let Some(J::Array(rows)) = at(&c, &["commitmentMap", "rows"]) else {
            return Err(Refusal::Input("commitment rows"));
        };
        for (name, domain) in [
            ("Rust3SubjectV2.subjectId", SUBJECT_DOMAIN),
            (
                "Rust3StageAnalysisDomainV2.domainCommitment",
                ANALYSIS_DOMAIN,
            ),
        ] {
            let selected: Vec<_> = rows
                .iter()
                .filter(|r| {
                    at(r, &["protocol"]).and_then(text) == Some("rust-semantic")
                        && at(r, &["field"]).and_then(text) == Some(name)
                })
                .collect();
            if selected.len() != 1 || at(selected[0], &["domain"]).and_then(text) != Some(domain) {
                return Err(Refusal::Input("request commitment recipe"));
            }
        }
        let plane = parse_json(
            top_level_member(PLANE, "relationRegistry").ok_or(Refusal::Input("fact registry"))?,
        )
        .map_err(|e| Refusal::Law(format!("plane: {e}")))?;
        let plane = obj(at(&plane, &["relations"]).ok_or(Refusal::Input("fact relations"))?)
            .ok_or(Refusal::Input("fact relations"))?;
        let registry = parse_json(REGISTRY).map_err(|e| Refusal::Law(format!("registry: {e}")))?;
        let registry = obj(at(&registry, &["x-opensip-relation-registry", "relations"])
            .ok_or(Refusal::Input("relation rows"))?)
        .ok_or(Refusal::Input("relation rows"))?;
        if registry.len() != plane.len() + 1 || !registry.contains_key("unresolved-edge") {
            return Err(Refusal::Input("closed relation set"));
        }
        let mut relations = BTreeMap::new();
        for (name, row) in registry {
            let ladder = at(row, &["ladder"])
                .and_then(strings)
                .ok_or(Refusal::Input("ladder"))?;
            if ladder.is_empty() || ladder.iter().collect::<BTreeSet<_>>().len() != ladder.len() {
                return Err(Refusal::Input("empty or repeated rung"));
            }
            if let Some(old) = plane.get(name) {
                if at(old, &["ladder"]).and_then(strings).as_ref() != Some(&ladder) {
                    return Err(Refusal::Input("ladder mirror drift"));
                }
            } else if name != "unresolved-edge" || ladder != ["observed"] {
                return Err(Refusal::Input("unimplemented relation extension"));
            }
            let same_only = match at(row, &["universeRule"]).and_then(text) {
                Some("same-only") => true,
                Some("admitted-target") => false,
                _ => return Err(Refusal::Input("universe rule")),
            };
            let Some(J::Integer(version)) = at(row, &["schemaVersion"]) else {
                return Err(Refusal::Input("schema version"));
            };
            relations.insert(
                name.clone(),
                Relation {
                    ladder,
                    same_only,
                    schema_version: u64::try_from(version.get())
                        .map_err(|_| Refusal::Arithmetic)?,
                },
            );
        }
        if plane.keys().any(|name| !relations.contains_key(name)) {
            return Err(Refusal::Input("missing inherited relation"));
        }
        Ok(Self {
            carriers: Carriers::load("Rust3").map_err(Refusal::Law)?,
            relations,
        })
    }

    pub(super) fn derive(&self, input: Input<'_>) -> Result<Derived, Refusal> {
        let Input {
            snapshot,
            files,
            universes,
            selected,
            provider_build_id,
            plan_stages,
            bounds,
            reference,
        } = input;
        if u64::try_from(files.len()).map_err(|_| Refusal::Arithmetic)? > bounds.snapshot_entries {
            return Err(Refusal::Bound("snapshot entries"));
        }
        let snapshot_shape = parse_json(br#"{"t":"ref","ref":"Rust3SnapshotId2"}"#)
            .map_err(|_| Refusal::Input("snapshot scalar"))?;
        self.carriers
            .check(&snapshot_shape, &t(snapshot), "snapshotId")
            .map_err(schema_error)?;
        let digest_shape = parse_json(br#"{"t":"ref","ref":"Rust3DigestHex"}"#)
            .map_err(|_| Refusal::Input("digest scalar"))?;
        let source = universes
            .get(selected)
            .ok_or(Refusal::Input("selected universe"))?;
        if source.provider_id != "rust-semantic" || source.provider_version != provider_build_id {
            return Err(Refusal::Input("selected provider identity"));
        }
        let source_universe_id = built_commitment(SOURCE_DOMAIN, &source.value);
        let mut target_domain = BTreeSet::new();
        for (i, row) in universes.iter().enumerate() {
            target_domain.insert(if i == selected {
                source_universe_id.clone()
            } else {
                generic_universe_commitment(row)?
            });
        }
        let mut selected_files: Vec<_> = files
            .iter()
            .filter(|f| f.byte_length > 0 && f.path.ends_with(".rs"))
            .collect();
        selected_files.sort_by(|a, b| a.path.as_bytes().cmp(b.path.as_bytes()));
        if selected_files.is_empty() {
            return Err(Refusal::Input("empty Rust subject scope"));
        }
        if selected_files.windows(2).any(|p| p[0].path == p[1].path) {
            return Err(Refusal::Input("duplicate Rust path"));
        }
        let count = u64::try_from(selected_files.len()).map_err(|_| Refusal::Arithmetic)?;
        if !reference && count > bounds.inline_subjects {
            return Err(Refusal::InlineSubjectLimit);
        }
        let mut subjects = Vec::new();
        for (ordinal, f) in selected_files.into_iter().enumerate() {
            self.carriers
                .check(&digest_shape, &t(&f.content_sha256), "contentSha256")
                .map_err(schema_error)?;
            let preimage = map(vec![
                ("snapshotId", t(snapshot)),
                ("path", t(&f.path)),
                ("contentSha256", t(&f.content_sha256)),
                ("byteLength", Value::Unsigned(f.byte_length)),
            ]);
            let subject = map(vec![
                (
                    "subjectOrdinal",
                    Value::Unsigned(u64::try_from(ordinal).map_err(|_| Refusal::Arithmetic)?),
                ),
                (
                    "subjectId",
                    t(&format!(
                        "rust-file:{}",
                        built_commitment(SUBJECT_DOMAIN, &preimage)
                    )),
                ),
                ("path", t(&f.path)),
                ("startByte", Value::Unsigned(0)),
                ("endByte", Value::Unsigned(f.byte_length)),
            ]);
            // Reference preimages have no inline ordinal-255 cap. Every
            // remaining original subject field still obeys its owner shape.
            for (name, shape) in self.carriers.members("Rust3SubjectV2") {
                if name != "subjectOrdinal" {
                    self.carriers
                        .check(
                            &shape,
                            member(&subject, &name).ok_or(Refusal::Input("subject member"))?,
                            &name,
                        )
                        .map_err(schema_error)?;
                }
            }
            subjects.push(subject);
        }
        let subjects = Value::Array(subjects);
        let encoded_subjects = cbor::encode(&subjects);
        let scope = map(vec![
            ("scopeKind", t("nonempty-rs-files")),
            ("subjectCount", Value::Unsigned(count)),
            (
                "subjectScopeCommitment",
                t(&hash_encoded(SCOPE_DOMAIN, &encoded_subjects)?),
            ),
        ]);
        super::super::admit_extern(
            "opensip.product.rust-subject-scope.1#/$defs/RustSubjectScopeV1",
            &scope,
        )
        .map_err(schema_error)?;
        let mut stages = Vec::new();
        let mut stage_ids = BTreeSet::new();
        for stage in plan_stages {
            if value_text(&stage.plan_stage, "kind") != Some("fact-derivation")
                || value_text(&stage.plan_stage, "operator") != Some("semantic-provider")
            {
                continue;
            }
            if let Some(literal) = value_text(&stage.plan_stage, "providerId")
                && stage.resolved_provider.as_deref() != Some(literal)
            {
                return Err(Refusal::Input("resolved/literal provider mismatch"));
            }
            if stage.resolved_provider.as_deref() != Some("rust-semantic") {
                continue;
            }
            if u64::try_from(stages.len()).map_err(|_| Refusal::Arithmetic)? >= bounds.stages {
                return Err(Refusal::Bound("stages"));
            }
            self.carriers
                .check_record("Rust3C2PlanStageV3", &stage.plan_stage)
                .map_err(schema_error)?;
            let id = value_text(&stage.plan_stage, "stageId").ok_or(Refusal::Input("stage id"))?;
            if !stage_ids.insert(id.to_owned()) {
                return Err(Refusal::Input("duplicate selected stage"));
            }
            let Some(Value::Array(requested)) = member(&stage.plan_stage, "relations") else {
                return Err(Refusal::Input("stage relations"));
            };
            let mut requested_relations = Vec::new();
            let mut total = 0u64;
            for relation in requested {
                let Value::Text(relation) = relation else {
                    return Err(Refusal::Input("relation"));
                };
                if requested_relations.contains(&relation.as_str()) {
                    return Err(Refusal::Input("duplicate stage relation"));
                }
                requested_relations.push(relation.as_str());
                let rule = self
                    .relations
                    .get(relation)
                    .ok_or(Refusal::Input("unknown relation"))?;
                let targets = if rule.same_only {
                    1
                } else {
                    u64::try_from(target_domain.len()).map_err(|_| Refusal::Arithmetic)?
                };
                total = total
                    .checked_add(
                        u64::try_from(rule.ladder.len())
                            .map_err(|_| Refusal::Arithmetic)?
                            .checked_mul(targets)
                            .ok_or(Refusal::Arithmetic)?,
                    )
                    .ok_or(Refusal::Arithmetic)?;
            }
            if total == 0 || total > bounds.keys_per_stage {
                return Err(Refusal::Bound("coverage keys"));
            }
            if u64::try_from(stage.scopes.len()).map_err(|_| Refusal::Arithmetic)? != total {
                return Err(Refusal::Input("Plan scope binding count"));
            }
            let mut scopes = BTreeMap::new();
            for s in &stage.scopes {
                if scopes
                    .insert(
                        (
                            s.relation.as_str(),
                            s.resolution.as_str(),
                            s.source.as_str(),
                            s.target.as_str(),
                        ),
                        s.commitment.as_str(),
                    )
                    .is_some()
                {
                    return Err(Refusal::Input("duplicate Plan scope binding"));
                }
            }
            let mut keys = Vec::new();
            for relation in requested_relations {
                let rule = &self.relations[relation];
                for rung in &rule.ladder {
                    let targets: Vec<_> = if rule.same_only {
                        vec![&source_universe_id]
                    } else {
                        target_domain.iter().collect()
                    };
                    for target in targets {
                        let commitment = scopes
                            .remove(&(
                                relation,
                                rung.as_str(),
                                source_universe_id.as_str(),
                                target.as_str(),
                            ))
                            .ok_or(Refusal::Input("missing Plan scope binding"))?;
                        let key = map(vec![
                            ("relation", t(relation)),
                            ("resolution", t(rung)),
                            ("sourceUniverseId", t(&source_universe_id)),
                            ("targetUniverseId", t(target)),
                            ("subjectScopeCommitment", t(commitment)),
                            ("producer", t("rust-semantic")),
                            ("producerVersion", t(provider_build_id)),
                            ("schemaVersion", Value::Unsigned(rule.schema_version)),
                        ]);
                        self.carriers
                            .check_record("Rust3CoverageKeyV2", &key)
                            .map_err(schema_error)?;
                        keys.push(key);
                    }
                }
            }
            if !scopes.is_empty() {
                return Err(Refusal::Input("extra Plan scope binding"));
            }
            let keys = Value::Array(keys);
            let domain_commitment = analysis_commitment(&encoded_subjects, &keys)?;
            stages.push(DerivedStage {
                plan_stage: stage.plan_stage.clone(),
                keys,
                domain_commitment,
            });
        }
        if stages.is_empty() {
            return Err(Refusal::Input("no selected Rust stages"));
        }
        Ok(Derived {
            source_universe_id,
            target_domain,
            subjects,
            subject_scope: scope,
            stages,
        })
    }

    /// Materialize one host stage only after the request builder has sized
    /// the complete Analyze envelope. The signed selection chooses reference;
    /// an inline stage is never substituted for an offered reference token.
    pub(super) fn stage_request(
        &self,
        derived: &Derived,
        index: usize,
        reference: bool,
    ) -> Result<Value, Refusal> {
        let stage = derived
            .stages
            .get(index)
            .ok_or(Refusal::Input("stage index"))?;
        self.carriers
            .check_record("Rust3C2PlanStageV3", &stage.plan_stage)
            .map_err(schema_error)?;
        let key_shape = self
            .carriers
            .members("Rust3StageAnalysisDomainV2")
            .into_iter()
            .find_map(|(name, shape)| (name == "requestedCoverageDomain").then_some(shape))
            .ok_or(Refusal::Input("coverage domain type"))?;
        self.carriers
            .check(&key_shape, &stage.keys, "requestedCoverageDomain")
            .map_err(schema_error)?;
        let subject = if reference {
            ("subjectScope", derived.subject_scope.clone())
        } else {
            let Value::Array(subjects) = &derived.subjects else {
                return Err(Refusal::Input("subjects"));
            };
            if subjects.len() > 256 {
                return Err(Refusal::InlineSubjectLimit);
            }
            // Check the original wire type before cloning a potentially large
            // reference preimage. Its published maxItems is the inline cap.
            let shape = self
                .carriers
                .members("Rust3StageAnalysisDomainV2")
                .into_iter()
                .find_map(|(name, shape)| (name == "subjects").then_some(shape))
                .ok_or(Refusal::Input("inline subjects type"))?;
            self.carriers
                .check(&shape, &derived.subjects, "subjects")
                .map_err(schema_error)?;
            ("subjects", derived.subjects.clone())
        };
        let value = map(vec![
            (
                "stageOrdinal",
                Value::Unsigned(u64::try_from(index).map_err(|_| Refusal::Arithmetic)?),
            ),
            ("planStage", stage.plan_stage.clone()),
            (
                "analysisDomain",
                map(vec![
                    subject,
                    ("requestedCoverageDomain", stage.keys.clone()),
                    ("domainCommitment", t(&stage.domain_commitment)),
                ]),
            ),
        ]);
        if reference {
            super::super::admit_extern(
                "opensip.product.rust-subject-scope.1#/$defs/StageRequestV3",
                &value,
            )
            .map_err(schema_error)?;
        } else {
            self.carriers
                .check_record("Rust3StageRequestV2", &value)
                .map_err(schema_error)?;
        }
        Ok(value)
    }

    /// Size the complete envelope before copying subjects into any stage.
    /// `remaining_payload_bytes` is the request recorder's remaining budget
    /// after all other canonical slots and its maximal Cancel reserve.
    pub(super) fn analyze(
        &self,
        derived: &Derived,
        context: &AnalyzeContext<'_>,
        reference: bool,
        sequence: u64,
        max_frame_bytes: u64,
        remaining_payload_bytes: u64,
    ) -> Result<Value, Refusal> {
        let mut fields = vec![
            ("analysisOrdinal", Value::Unsigned(context.analysis_ordinal)),
            ("executionId", t(context.execution_id)),
            ("snapshotId", t(context.snapshot_id)),
            ("planId", t(context.plan_id)),
        ];
        for (name, value) in &fields {
            let shape = self
                .carriers
                .members("Rust3AnalyzeV2")
                .into_iter()
                .find_map(|(n, shape)| (n == *name).then_some(shape))
                .ok_or(Refusal::Input("Analyze member type"))?;
            self.carriers
                .check(&shape, value, name)
                .map_err(schema_error)?;
        }
        if derived.stages.is_empty() || derived.stages.len() > 256 {
            return Err(Refusal::Bound("Analyze stage count"));
        }
        // Empty-array encoding supplies exactly the length head to replace.
        // No stage or subject array is allocated for this computation.
        let count = u64::try_from(derived.stages.len()).map_err(|_| Refusal::Arithmetic)?;
        let array_head = match count {
            0..=23 => 1,
            24..=255 => 2,
            _ => 3,
        };
        let mut stages_length: u64 = array_head;
        for index in 0..derived.stages.len() {
            stages_length = stages_length
                .checked_add(stage_request_length(derived, index, reference)?)
                .ok_or(Refusal::Arithmetic)?;
        }
        let mut lengths = Vec::with_capacity(5);
        for (name, value) in &fields {
            lengths.push((
                *name,
                cbor::encoded_length(value).ok_or(Refusal::Arithmetic)?,
            ));
        }
        lengths.push(("stages", stages_length));
        let payload_length = map_length(&lengths)?;
        let envelope_length =
            super::schedule::envelope_length_for_payload(sequence, "Analyze", payload_length)
                .map_err(|_| Refusal::Arithmetic)?;
        if envelope_length > max_frame_bytes {
            return Err(Refusal::Bound("Analyze envelope bytes"));
        }
        if envelope_length > remaining_payload_bytes {
            return Err(Refusal::Bound("Analyze request bytes"));
        }
        let stages = (0..derived.stages.len())
            .map(|index| self.stage_request(derived, index, reference))
            .collect::<Result<Vec<_>, _>>()?;
        fields.push(("stages", Value::Array(stages)));
        let value = map(fields);
        if !reference {
            self.carriers
                .check_record("Rust3AnalyzeV2", &value)
                .map_err(schema_error)?;
        }
        Ok(value)
    }
}

/// Exact stage length without cloning the subject tree into each stage.
/// The outer request constructor must sum every stage and wrapper before
/// materialization; individual-stage fit is not complete Analyze fit.
pub(super) fn stage_request_length(
    derived: &Derived,
    index: usize,
    reference: bool,
) -> Result<u64, Refusal> {
    let stage = derived
        .stages
        .get(index)
        .ok_or(Refusal::Input("stage index"))?;
    let subject = if reference {
        ("subjectScope", &derived.subject_scope)
    } else {
        ("subjects", &derived.subjects)
    };
    let domain = map_length(&[
        (
            subject.0,
            cbor::encoded_length(subject.1).ok_or(Refusal::Arithmetic)?,
        ),
        (
            "requestedCoverageDomain",
            cbor::encoded_length(&stage.keys).ok_or(Refusal::Arithmetic)?,
        ),
        (
            "domainCommitment",
            cbor::encoded_length(&t(&stage.domain_commitment)).ok_or(Refusal::Arithmetic)?,
        ),
    ])?;
    map_length(&[
        (
            "stageOrdinal",
            cbor::encoded_length(&Value::Unsigned(
                u64::try_from(index).map_err(|_| Refusal::Arithmetic)?,
            ))
            .ok_or(Refusal::Arithmetic)?,
        ),
        (
            "planStage",
            cbor::encoded_length(&stage.plan_stage).ok_or(Refusal::Arithmetic)?,
        ),
        ("analysisDomain", domain),
    ])
}
fn map_length(members: &[(&str, u64)]) -> Result<u64, Refusal> {
    let probe = Value::Map(
        members
            .iter()
            .map(|(k, _)| ((*k).to_owned(), Value::Null))
            .collect(),
    );
    let mut length = cbor::encoded_length(&probe)
        .and_then(|n| n.checked_sub(u64::try_from(members.len()).ok()?))
        .ok_or(Refusal::Arithmetic)?;
    for (_, size) in members {
        length = length.checked_add(*size).ok_or(Refusal::Arithmetic)?;
    }
    Ok(length)
}

fn hash_encoded(domain: &str, encoded: &[u8]) -> Result<String, Refusal> {
    let digest = RawSha256::new()
        .update(domain.as_bytes())
        .and_then(|d| d.update(&[0]))
        .and_then(|d| d.update(encoded))
        .map_err(|_| Refusal::Arithmetic)?;
    Ok(format!("sha256:{}", digest_hex(&digest.finish())))
}
fn generic_universe_commitment(row: &Universe) -> Result<String, Refusal> {
    // No clone of the complete supplied universe tree. All three value
    // encodings are hashed in the canonical order of their encoded keys.
    let mut members = [
        (
            cbor::encode(&t("providerId")),
            cbor::encode(&t(&row.provider_id)),
        ),
        (
            cbor::encode(&t("providerVersion")),
            cbor::encode(&t(&row.provider_version)),
        ),
        (cbor::encode(&t("universe")), cbor::encode(&row.value)),
    ];
    members.sort_by(|a, b| a.0.cmp(&b.0));
    let mut digest = RawSha256::new()
        .update(GENERIC_DOMAIN.as_bytes())
        .and_then(|d| d.update(&[0, 0xa3]))
        .map_err(|_| Refusal::Arithmetic)?;
    for (key, value) in members {
        digest = digest
            .update(&key)
            .and_then(|d| d.update(&value))
            .map_err(|_| Refusal::Arithmetic)?;
    }
    Ok(format!("sha256:{}", digest_hex(&digest.finish())))
}

/// Hash the same closed map as built_commitment without cloning the complete
/// subject array for each stage. The subject encoding is shared once; the
/// two encoded keys are sorted by exactly the selected encoder's byte order.
fn analysis_commitment(subjects: &[u8], keys: &Value) -> Result<String, Refusal> {
    let encoded_keys = cbor::encode(keys);
    let mut members = [
        (cbor::encode(&t("subjects")), subjects),
        (
            cbor::encode(&t("requestedCoverageDomain")),
            encoded_keys.as_slice(),
        ),
    ];
    members.sort_by(|a, b| a.0.cmp(&b.0));
    let mut digest = RawSha256::new()
        .update(ANALYSIS_DOMAIN.as_bytes())
        .and_then(|d| d.update(&[0, 0xa2]))
        .map_err(|_| Refusal::Arithmetic)?;
    for (key, value) in members {
        digest = digest
            .update(&key)
            .and_then(|d| d.update(value))
            .map_err(|_| Refusal::Arithmetic)?;
    }
    Ok(format!("sha256:{}", digest_hex(&digest.finish())))
}

#[cfg(test)]
#[path = "domain_tests.rs"]
mod tests;
