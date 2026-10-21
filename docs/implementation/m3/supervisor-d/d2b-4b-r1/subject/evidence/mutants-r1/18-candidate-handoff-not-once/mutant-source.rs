//! Rust3 worker receive admission (D2b-4a). This codec is separate from TS2:
//! the envelope, selected shape and immutable dispatch joins precede P3T.
use super::super::{
    ProcessEvent, ReceivedBytes, ReceivedFrame, Sequence,
    cbor::{self, Value},
    read_frame, received_commitment,
    table::{Event, Protocol, Run, Scalar, Table},
    ts2::{
        carrier::{self, Carriers, field},
        top_level_member,
    },
};
use super::{
    accounting::{CandidateBatch, ResponseAccounting, ResponseTotals},
    build,
    observations::ProviderFaultWindow,
    schemas::Rust3PayloadSchemas,
};
use opensip_contracts::generated::protocol::Rust3ProviderFrameV3Payload;
use opensip_identity::{JsonValue as J, digest_hex, parse_json, raw_sha256};
use std::{
    collections::{BTreeMap, BTreeSet},
    io::Read,
};
const RPP: &[u8] = include_bytes!("../../../data/rust-provider-protocol.v2.json");
const FACT_PLANE: &[u8] = include_bytes!("../../../data/fact-plane.v1.json");
const REGISTRY: &[u8] = include_bytes!("../../../data/relation-payload-schemas.v2.json");
/// Complete base plus FA2/RUST3-LIM wire-closure container bound (LD-D2B-2).
/// Byte-string contents have the separate embedded bound below.
pub const RUST3_FRAME_MAX_DEPTH: usize = 7;
pub const RELATION_PAYLOAD_MAX_DEPTH: usize = 1;
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Rust3Refusal {
    Context(String),
    Envelope(String),
    Schema(String),
    Admission(String),
    Table(String),
    Transport(String),
    AfterRefusal,
}
/// One stage projection from the admitted Plan. The host builder (4b) owns
/// exact Plan-stage-byte equality and domain reconstruction before spawn.
/// The receiver consumes its immutable projection; it never mints a Plan.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Rust3StageBinding {
    pub plan_stage: Value,
    pub analysis_domain: Value,
}
/// Trusted Plan/selection/snapshot projection supplied by the session
/// factory. No production factory is introduced by D2b-4a.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Rust3DispatchContext {
    pub hello: Value,
    pub open_universe: Value,
    pub snapshot_seal: Value,
    pub dependency_seal: Value,
    pub prepared_seal: Option<Value>,
    pub manifest_files: BTreeMap<String, (String, u64)>,
    pub universe_key: String,
    pub target_domain: BTreeSet<String>,
    pub analysis_ordinal: u64,
    pub stages: Vec<Rust3StageBinding>,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Rust3HostFrame {
    Hello,
    OpenUniverse,
    SnapshotManifest,
    SnapshotFileChunk,
    SnapshotSeal,
    DependencySourceManifest,
    DependencySourceChunk,
    DependencySourceSeal,
    PreparedOutputManifest,
    PreparedOutputChunk,
    PreparedOutputSeal,
    Analyze,
    Cancel {
        execution_id: Option<String>,
        analysis_ordinal: Option<u64>,
    },
}
impl Rust3HostFrame {
    fn name(&self) -> &str {
        match self {
            Self::Hello => "Hello",
            Self::OpenUniverse => "OpenUniverse",
            Self::SnapshotManifest => "SnapshotManifest",
            Self::SnapshotFileChunk => "SnapshotFileChunk",
            Self::SnapshotSeal => "SnapshotSeal",
            Self::DependencySourceManifest => "DependencySourceManifest",
            Self::DependencySourceChunk => "DependencySourceChunk",
            Self::DependencySourceSeal => "DependencySourceSeal",
            Self::PreparedOutputManifest => "PreparedOutputManifest",
            Self::PreparedOutputChunk => "PreparedOutputChunk",
            Self::PreparedOutputSeal => "PreparedOutputSeal",
            Self::Analyze => "Analyze",
            Self::Cancel { .. } => "Cancel",
        }
    }
}
/// Publication occurs only after all checks, response accounting and P3T.
/// Spool entries are the separate constructed records, never commitment inputs.
#[derive(Debug, Clone)]
pub struct Rust3Admitted {
    pub sequence: u64,
    pub trace: String,
    pub payload: Rust3ProviderFrameV3Payload,
    pub spool_entries: Vec<Vec<u8>>,
}
#[derive(Debug, Clone)]
struct RequestedKey {
    relation: String,
    resolution: String,
    source_universe_id: String,
    target_universe_id: String,
    subject_scope_commitment: String,
    subject_count: u64,
}
#[derive(Debug, Clone)]
struct Stage {
    expected_stage_id: String,
    relations: Vec<String>,
    budget: Option<(String, u64)>,
    keys: Vec<RequestedKey>,
}
#[derive(Debug, Default, Clone)]
struct StageLive {
    batches: u64,
    next_candidate: u64,
    facts: Vec<(usize, usize)>,
    coverage: Vec<(usize, usize)>,
}
struct Law {
    max_batch_candidates: u64,
    registry: BTreeMap<String, (Vec<String>, String, u64)>,
    layers: BTreeMap<String, String>,
    domains: BTreeMap<String, String>,
}
fn obj(v: &J) -> Option<&BTreeMap<String, J>> {
    if let J::Object(x) = v { Some(x) } else { None }
}
fn txt(v: &J) -> Option<&str> {
    if let J::String(x) = v { Some(x) } else { None }
}
fn path<'a>(v: &'a J, keys: &[&str]) -> Option<&'a J> {
    keys.iter().try_fold(v, |v, key| obj(v)?.get(*key))
}
fn map_of(v: &Value) -> Option<&[(String, Value)]> {
    if let Value::Map(f) = v { Some(f) } else { None }
}
fn text_of<'a>(f: &'a [(String, Value)], key: &str) -> Option<&'a str> {
    if let Some(Value::Text(x)) = field(f, key) {
        Some(x)
    } else {
        None
    }
}
fn u64_of(f: &[(String, Value)], key: &str) -> Option<u64> {
    if let Some(Value::Unsigned(x)) = field(f, key) {
        Some(*x)
    } else {
        None
    }
}
fn array_of<'a>(f: &'a [(String, Value)], key: &str) -> &'a [Value] {
    if let Some(Value::Array(x)) = field(f, key) {
        x
    } else {
        &[]
    }
}
fn child(frame: &ReceivedFrame, node: usize, f: &[(String, Value)], key: &str) -> Option<usize> {
    frame
        .children(node)
        .nth(f.iter().position(|(k, _)| k == key)?)
}
fn suffix(id: &str) -> Option<&str> {
    id.strip_prefix("sha256:")
}
fn contains_bytes(v: &Value) -> bool {
    match v {
        Value::Bytes(_) => true,
        Value::Array(xs) => xs.iter().any(contains_bytes),
        Value::Map(xs) => xs.iter().any(|(_, v)| contains_bytes(v)),
        _ => false,
    }
}
fn canonical_context(v: &Value) -> Result<Value, String> {
    let len = cbor::encoded_length(v).ok_or("context length overflow")?;
    if len > super::super::MAX_FRAME_PAYLOAD_BYTES {
        return Err("over-bound context frame".to_owned());
    }
    cbor::decode(
        &cbor::encode(v),
        cbor::Profile::Rust3,
        RUST3_FRAME_MAX_DEPTH,
    )
    .map_err(|e| format!("context CBOR: {e:?}"))
}
impl Law {
    fn load() -> Result<Self, String> {
        let carrier = parse_json(carrier::CARRIERS).map_err(|e| format!("carriers: {e}"))?;
        let Some(J::Array(pins)) = path(&carrier, &["sourcePins"]) else {
            return Err("source pins".to_owned());
        };
        for (key, bytes) in [
            ("rust2", RPP),
            ("factPlane", FACT_PLANE),
            ("relationRegistry2", REGISTRY),
        ] {
            let pin = pins
                .iter()
                .find(|p| path(p, &["key"]).and_then(txt) == Some(key))
                .ok_or("source pin")?;
            if path(pin, &["sha256"]).and_then(txt) != Some(digest_hex(&raw_sha256(bytes)).as_str())
            {
                return Err(format!("pin {key}"));
            }
        }
        let rel = parse_json(REGISTRY).map_err(|e| format!("registry: {e}"))?;
        let mut registry = BTreeMap::new();
        for (name, row) in
            obj(path(&rel, &["x-opensip-relation-registry", "relations"]).ok_or("relations")?)
                .ok_or("relations")?
        {
            let Some(J::Array(ladder)) = path(row, &["ladder"]) else {
                return Err("ladder".to_owned());
            };
            let ladder = ladder
                .iter()
                .map(|x| txt(x).map(str::to_owned).ok_or("rung"))
                .collect::<Result<Vec<_>, _>>()?;
            let schema = path(row, &["schemaId"])
                .and_then(txt)
                .ok_or("schemaId")?
                .to_owned();
            let Some(J::Integer(version)) = path(row, &["schemaVersion"]) else {
                return Err("schemaVersion".to_owned());
            };
            registry.insert(
                name.clone(),
                (
                    ladder,
                    schema,
                    u64::try_from(version.get()).map_err(|_| "schemaVersion")?,
                ),
            );
        }
        let plane = parse_json(
            top_level_member(FACT_PLANE, "relationRegistry").ok_or("fact plane registry")?,
        )
        .map_err(|e| format!("fact plane: {e}"))?;
        let mut layers = BTreeMap::new();
        for (name, row) in obj(path(&plane, &["relations"]).ok_or("layers")?).ok_or("layers")? {
            layers.insert(
                name.clone(),
                path(row, &["layer"])
                    .and_then(txt)
                    .ok_or("layer")?
                    .to_owned(),
            );
        }
        let Some(J::Array(rows)) = path(&carrier, &["commitmentMap", "rows"]) else {
            return Err("commitment rows".to_owned());
        };
        let mut domains = BTreeMap::new();
        for row in rows {
            if path(row, &["protocol"]).and_then(txt) == Some("rust-semantic")
                && let (Some(f), Some(d)) = (
                    path(row, &["field"]).and_then(txt),
                    path(row, &["domain"]).and_then(txt),
                )
            {
                domains.insert(f.to_owned(), d.to_owned());
            }
        }
        // This module implements only the retained envelope precheck and T016/
        // T020 guards, not the superseded Rust2 table. P3T remains the table.
        let rpp = parse_json(RPP).map_err(|e| format!("RPP: {e}"))?;
        let expected=parse_json(br#"{"when":{"op":"eq","left":"event.kind","right":{"const":"frame"}},"accept":{"op":"all","items":[{"op":"neq","left":"event.frameType","right":{"const":"UNKNOWN_FRAME"}},{"op":"eq","left":"event.payloadValid","right":{"const":true}},{"op":"directionMatchesFrameSchema"},{"op":"sequenceEqualsDirectionCounter"},{"op":"directionCounterLessThan","value":18446744073709551615}]},"onAccept":[{"op":"checkedIncrementDirectionCounter","amount":1}],"onReject":[{"op":"set","field":"phase","value":{"const":"FAULT"}}]}"#).map_err(|_|"expected frame precheck")?;
        if path(
            &rpp,
            &[
                "orderingAndStateMachine",
                "transitionAstV2",
                "framePrecheck",
            ],
        ) != Some(&expected)
        {
            return Err("unimplemented frame precheck".to_owned());
        }
        let Some(J::Array(rules)) = path(
            &rpp,
            &["orderingAndStateMachine", "transitionAstV2", "rules"],
        ) else {
            return Err("retained rules".to_owned());
        };
        for(id,json)in[("T016-FACT-BATCH",br#"{"op":"all","items":[{"op":"eq","left":"event.batchIndex","right":"state.nextBatchIndex"},{"op":"eq","left":"event.firstCandidateOrdinal","right":"state.nextCandidateOrdinal"},{"op":"between","value":"event.candidateCount","minimum":1,"maximumRef":"limits.maxFactBatchCandidates"}]}"#.as_slice()),("T020-BUDGET",br#"{"op":"all","items":[{"op":"eq","left":"event.budgetMatchesCurrentStage","right":{"const":true}},{"op":"in","value":"event.budgetUnit","values":["work-units","bytes","items"]}]}"#.as_slice())]{let rule=rules.iter().find(|r|path(r,&["id"]).and_then(txt)==Some(id)).ok_or("retained guard")?;let expected=parse_json(json).map_err(|_|"expected guard")?;if path(rule,&["guard"])!=Some(&expected){return Err(format!("unimplemented {id}"))}}
        let Some(J::Integer(max_batch)) = path(&rpp, &["limits", "maxFactBatchCandidates"]) else {
            return Err("maxFactBatchCandidates".to_owned());
        };
        let max_batch_candidates =
            u64::try_from(max_batch.get()).map_err(|_| "maxFactBatchCandidates")?;
        Ok(Self {
            max_batch_candidates,
            registry,
            layers,
            domains,
        })
    }
    fn domain(&self, field: &str) -> Result<&str, String> {
        self.domains
            .get(field)
            .map(String::as_str)
            .ok_or_else(|| format!("missing commitment domain {field}"))
    }
}
/// The actual stateful Rust3 receive side. No TS2 payload/context type is
/// accepted here and no peer input is translated between protocols.
pub struct Rust3Receiver<'t> {
    context: Rust3DispatchContext,
    stages: Vec<Stage>,
    live: Vec<StageLive>,
    law: Law,
    schemas: Rust3PayloadSchemas,
    run: Run<'t>,
    sequence: Sequence,
    refused: bool,
    target_attribution: bool,
    accounting: ResponseAccounting,
    fault_window: ProviderFaultWindow,
    cancel: Option<(Option<String>, Option<u64>, String)>,
    open_sent: bool,
    analyze_sent: bool,
    retained: Vec<ReceivedFrame>,
    candidate_spool_taken: bool,
}
impl<'t> Rust3Receiver<'t> {
    pub fn new(table: &'t Table, mut context: Rust3DispatchContext) -> Result<Self, Rust3Refusal> {
        use Rust3Refusal::Context;
        if table.protocol() != Protocol::Rust3 {
            return Err(Context("not Rust3 table".to_owned()));
        }
        let law = Law::load().map_err(Context)?;
        let schemas = Rust3PayloadSchemas::load().map_err(Context)?;
        let carriers = Carriers::load("Rust3").map_err(Context)?;
        context.hello = canonical_context(&context.hello).map_err(Context)?;
        context.open_universe = canonical_context(&context.open_universe).map_err(Context)?;
        context.snapshot_seal = canonical_context(&context.snapshot_seal).map_err(Context)?;
        context.dependency_seal = canonical_context(&context.dependency_seal).map_err(Context)?;
        if let Some(v) = &context.prepared_seal {
            context.prepared_seal = Some(canonical_context(v).map_err(Context)?)
        }
        for (name, v) in [
            ("Hello", &context.hello),
            ("OpenUniverse", &context.open_universe),
            ("SnapshotSeal", &context.snapshot_seal),
            ("DependencySourceSeal", &context.dependency_seal),
        ] {
            schemas
                .check_payload(name, v, "START", false)
                .map_err(Context)?;
        }
        let hello = map_of(&context.hello).ok_or_else(|| Context("Hello".to_owned()))?;
        if text_of(hello, "expectedProtocolContractSha256")
            != Some(digest_hex(&raw_sha256(RPP)).as_str())
        {
            return Err(Context("Hello protocol contract pin".to_owned()));
        }
        let target_attribution = array_of(hello, "expectedCapabilities")
            .iter()
            .any(|x| matches!(x,Value::Text(s)if s=="target-attribution-v2"));
        // Negotiated successor payloads are implemented by4c, never silently
        // interpreted as the base protocol by4a.
        if array_of(hello, "expectedCapabilities").iter().any(
            |x| matches!(x,Value::Text(s)if s=="symbol-census-v1"||s=="subject-scope-reference-v1"),
        ) {
            return Err(Context("successor session requires D2b-4c".to_owned()));
        }
        let open =
            map_of(&context.open_universe).ok_or_else(|| Context("OpenUniverse".to_owned()))?;
        let repo = field(open, "repositoryResolution")
            .and_then(map_of)
            .ok_or_else(|| Context("repositoryResolution".to_owned()))?;
        let universe = field(open, "universe")
            .and_then(map_of)
            .ok_or_else(|| Context("universe".to_owned()))?;
        let expected_identity = field(hello, "expectedIdentity")
            .and_then(map_of)
            .ok_or_else(|| Context("expectedIdentity".to_owned()))?;
        for (key, value) in expected_identity {
            if field(universe, key) != Some(value) {
                return Err(Context(format!("Hello/OpenUniverse Rust identity {key}")));
            }
        }
        let inputs = field(universe, "resolvedInputs")
            .and_then(map_of)
            .ok_or_else(|| Context("resolvedInputs".to_owned()))?;
        if field(repo, "preparedOutputSetId") != field(inputs, "preparedOutputSetId")
            || field(repo, "dependencySourceSetId") != field(inputs, "dependencySourceSetId")
        {
            return Err(Context("repository/universe resolution join".to_owned()));
        }
        let prepared = field(repo, "preparedOutputSetId") != Some(&Value::Null);
        if prepared != context.prepared_seal.is_some() {
            return Err(Context("prepared seal selection".to_owned()));
        }
        if let Some(v) = &context.prepared_seal {
            schemas
                .check_payload("PreparedOutputSeal", v, "START", false)
                .map_err(Context)?;
            if field(
                map_of(v).ok_or_else(|| Context("prepared seal".to_owned()))?,
                "planId",
            ) != field(open, "planId")
            {
                return Err(Context("prepared seal plan".to_owned()));
            }
        }
        if field(
            map_of(&context.snapshot_seal).ok_or_else(|| Context("snapshot seal".to_owned()))?,
            "snapshotId",
        ) != field(open, "snapshotId")
        {
            return Err(Context("snapshot seal snapshot".to_owned()));
        }
        if field(
            map_of(&context.dependency_seal)
                .ok_or_else(|| Context("dependency seal".to_owned()))?,
            "dependencySourceSetId",
        ) != field(repo, "dependencySourceSetId")
        {
            return Err(Context("dependency seal set".to_owned()));
        }
        if suffix(&context.universe_key).is_none_or(|s| {
            s.len() != 64
                || !s
                    .bytes()
                    .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
        }) {
            return Err(Context("native universe identity".to_owned()));
        }
        if context.stages.is_empty() || context.stages.len() > 256 {
            return Err(Context("stage count".to_owned()));
        }
        let mut stages = Vec::new();
        let mut ids = BTreeSet::new();
        for (index, s) in context.stages.iter_mut().enumerate() {
            s.plan_stage = canonical_context(&s.plan_stage).map_err(Context)?;
            s.analysis_domain = canonical_context(&s.analysis_domain).map_err(Context)?;
            let value = Value::Map(vec![
                ("stageOrdinal".to_owned(), Value::Unsigned(index as u64)),
                ("planStage".to_owned(), s.plan_stage.clone()),
                ("analysisDomain".to_owned(), s.analysis_domain.clone()),
            ]);
            carriers
                .check_record("Rust3StageRequestV2", &value)
                .map_err(Context)?;
            let p = map_of(&s.plan_stage).ok_or_else(|| Context("plan stage".to_owned()))?;
            let d =
                map_of(&s.analysis_domain).ok_or_else(|| Context("analysis domain".to_owned()))?;
            let id = text_of(p, "stageId")
                .ok_or_else(|| Context("stageId".to_owned()))?
                .to_owned();
            if !ids.insert(id.clone()) {
                return Err(Context("duplicate stageId".to_owned()));
            }
            let relations = array_of(p, "relations")
                .iter()
                .map(|x| {
                    if let Value::Text(s) = x {
                        Ok(s.clone())
                    } else {
                        Err(Context("relation".to_owned()))
                    }
                })
                .collect::<Result<Vec<_>, _>>()?;
            let budget = if let Some(v) = field(p, "budget") {
                let b = map_of(v).ok_or_else(|| Context("stage budget".to_owned()))?;
                Some((
                    text_of(b, "unit")
                        .ok_or_else(|| Context("budget unit".to_owned()))?
                        .to_owned(),
                    u64_of(b, "limit").ok_or_else(|| Context("budget limit".to_owned()))?,
                ))
            } else {
                None
            };
            // Base Rust3 examinedUniverse echoes the entire host stage's
            // inline subject inventory, independently of its scope digest.
            let subject_count = u64::try_from(array_of(d, "subjects").len())
                .map_err(|_| Context("subject count overflow".to_owned()))?;
            let mut keys = Vec::new();
            for value in array_of(d, "requestedCoverageDomain") {
                let k = map_of(value).ok_or_else(|| Context("coverage key".to_owned()))?;
                let get = |name| {
                    text_of(k, name)
                        .map(str::to_owned)
                        .ok_or_else(|| Context(format!("coverage key {name}")))
                };
                let key = RequestedKey {
                    relation: get("relation")?,
                    resolution: get("resolution")?,
                    source_universe_id: get("sourceUniverseId")?,
                    target_universe_id: get("targetUniverseId")?,
                    subject_scope_commitment: get("subjectScopeCommitment")?,
                    subject_count,
                };
                if key.source_universe_id != context.universe_key
                    || !context.target_domain.contains(&key.target_universe_id)
                    || !relations.contains(&key.relation)
                {
                    return Err(Context("requested coverage domain join".to_owned()));
                }
                keys.push(key);
            }
            stages.push(Stage {
                expected_stage_id: id,
                relations,
                budget,
                keys,
            });
        }
        let live = vec![StageLive::default(); stages.len()];
        Ok(Self {
            context,
            stages,
            live,
            law,
            schemas,
            run: table.start(),
            sequence: Sequence::default(),
            refused: false,
            target_attribution,
            accounting: ResponseAccounting::new().map_err(Context)?,
            fault_window: ProviderFaultWindow::new().map_err(Context)?,
            cancel: None,
            open_sent: false,
            analyze_sent: false,
            retained: Vec::new(),
            candidate_spool_taken: false,
        })
    }
    pub fn phase(&self) -> &str {
        self.run.phase()
    }
    pub fn terminal_kind(&self) -> Option<&str> {
        if let Some(Scalar::Text(v)) = self.run.field("terminalKind") {
            Some(v)
        } else {
            None
        }
    }
    pub fn totals(&self) -> ResponseTotals {
        self.accounting.totals()
    }
    pub fn remaining_payload_bytes(&self) -> u64 {
        self.accounting.remaining_payload_bytes()
    }
    /// Move the original admitted response envelopes to the participant's
    /// CANDIDATE_ONLY spool after clean protocol completion. This conveys no
    /// fact or Coverage admission: H still owns those decisions.
    ///
    /// No copy or re-encoding of the received bytes occurs. Response charging
    /// and every commitment precede retention, and the iterator moves each
    /// already retained byte buffer. Incomplete, refused, faulted or cancelled
    /// runs yield no spool. A completed spool can be taken only once.
    pub fn take_candidate_spool(&mut self) -> Option<impl Iterator<Item = Vec<u8>>> {
        if self.refused
            || false
            || self.phase() != "DONE"
            || !matches!(
                self.terminal_kind(),
                Some("complete" | "unavailable" | "budget-exhausted")
            )
        {
            return None;
        }
        self.candidate_spool_taken = true;
        Some(
            std::mem::take(&mut self.retained)
                .into_iter()
                .map(|frame| frame.payload),
        )
    }
    /// Settlement/fault cleanup only: the participant will admit no further
    /// response after this call. Invalidate the one-shot handoff permanently.
    pub(crate) fn discard_candidate_spool(&mut self) {
        self.retained.clear();
        self.candidate_spool_taken = true;
    }
    fn refused<T>(&mut self, error: Rust3Refusal) -> Result<T, Rust3Refusal> {
        self.refused = true;
        Err(error)
    }
    fn host_event(&self, frame: &Rust3HostFrame) -> Event {
        let mut event = Event::frame(frame.name());
        if *frame == Rust3HostFrame::OpenUniverse {
            event.dependency_mode = true;
            let repo = map_of(&self.context.open_universe)
                .and_then(|x| field(x, "repositoryResolution"))
                .and_then(map_of);
            event.prepared_mode =
                repo.and_then(|x| field(x, "preparedOutputSetId")) != Some(&Value::Null);
        }
        if *frame == Rust3HostFrame::Analyze {
            event.stage_count = self.stages.len() as i64;
        }
        event
    }
    pub fn admits(&self, frame: &Rust3HostFrame) -> bool {
        if self.refused {
            return false;
        }
        let mut run = self.run.clone();
        run.step(&self.host_event(frame));
        run.phase() != "FAULT"
    }
    fn step(&mut self, event: &Event) -> Result<String, Rust3Refusal> {
        let trace = self.run.step(event);
        if self.run.phase() == "FAULT" {
            self.refused(Rust3Refusal::Table(trace))
        } else {
            Ok(trace)
        }
    }
    pub fn sent(&mut self, frame: Rust3HostFrame) -> Result<String, Rust3Refusal> {
        if self.refused {
            return Err(Rust3Refusal::AfterRefusal);
        }
        let phase = self.phase().to_owned();
        if let Rust3HostFrame::Cancel {
            execution_id,
            analysis_ordinal,
        } = &frame
        {
            let want_exec = if self.open_sent {
                map_of(&self.context.open_universe)
                    .and_then(|f| text_of(f, "executionId"))
                    .map(str::to_owned)
            } else {
                None
            };
            let want_ordinal = if self.analyze_sent {
                Some(self.context.analysis_ordinal)
            } else {
                None
            };
            if *execution_id != want_exec || *analysis_ordinal != want_ordinal {
                return self.refused(Rust3Refusal::Admission(
                    "Cancel nullability/echo".to_owned(),
                ));
            }
            self.cancel = Some((execution_id.clone(), *analysis_ordinal, phase));
        }
        let trace = self.step(&self.host_event(&frame))?;
        let payload = match frame {
            Rust3HostFrame::OpenUniverse => {
                self.open_sent = true;
                self.context.open_universe.clone()
            }
            Rust3HostFrame::Analyze => {
                self.analyze_sent = true;
                Value::Map(vec![(
                    "analysisOrdinal".to_owned(),
                    Value::Unsigned(self.context.analysis_ordinal),
                )])
            }
            _ => Value::Map(Vec::new()),
        };
        if let Err(e) = self
            .fault_window
            .host_sent(&self.run, frame.name(), &payload)
        {
            return self.refused(Rust3Refusal::Admission(e));
        }
        Ok(trace)
    }
    pub fn process(&mut self, event: ProcessEvent) -> Result<String, Rust3Refusal> {
        if self.refused {
            return Err(Rust3Refusal::AfterRefusal);
        }
        self.step(&event.table_event())
    }
    pub fn read(&mut self, reader: &mut impl Read) -> Result<Option<Rust3Admitted>, Rust3Refusal> {
        if self.refused {
            return Err(Rust3Refusal::AfterRefusal);
        }
        match read_frame(
            reader,
            cbor::Profile::Rust3,
            RUST3_FRAME_MAX_DEPTH,
            Some(self.remaining_payload_bytes()),
        ) {
            Ok(Some(frame)) => self.receive(frame).map(Some),
            Ok(None) => Ok(None),
            Err(e) => self.refused(Rust3Refusal::Transport(format!("{e:?}"))),
        }
    }
    pub fn receive(&mut self, frame: ReceivedFrame) -> Result<Rust3Admitted, Rust3Refusal> {
        if self.refused {
            return Err(Rust3Refusal::AfterRefusal);
        }
        if frame.profile() != cbor::Profile::Rust3 {
            return self.refused(Rust3Refusal::Envelope(
                "not a Rust3 received-byte account".to_owned(),
            ));
        }
        let phase = self.phase().to_owned();
        let result = self.admit(&frame);
        let (sequence, name, event, retain) = match result {
            Ok(x) => x,
            Err(e) => return self.refused(e),
        };
        let env = map_of(frame.value()).ok_or_else(|| Rust3Refusal::Envelope("map".to_owned()))?;
        let payload =
            field(env, "payload").ok_or_else(|| Rust3Refusal::Envelope("payload".to_owned()))?;
        let fields = map_of(payload).ok_or_else(|| Rust3Refusal::Schema("map".to_owned()))?;
        let batch = if name == "FactBatch" {
            Some(CandidateBatch {
                analysis_ordinal: self.context.analysis_ordinal,
                stage_id: text_of(fields, "stageId")
                    .ok_or_else(|| Rust3Refusal::Admission("stageId".to_owned()))?,
                candidates: array_of(fields, "candidates"),
            })
        } else {
            None
        };
        let spool_entries = match self.accounting.charge(frame.payload().len() as u64, batch) {
            Ok(x) => x,
            Err(e) => {
                return self.refused(Rust3Refusal::Admission(format!("response safety: {e:?}")));
            }
        };
        let trace = self.step(&event)?;
        let payload = match build::convert(&name, payload, self.target_attribution, &phase) {
            Ok(x) => x,
            Err(e) => return self.refused(Rust3Refusal::Admission(e)),
        };
        self.fault_window.worker_admitted(&self.run);
        // Commitment calculations still borrow the original frame accounts.
        // Keep the terminal only after those calculations and all admission,
        // accounting, table and conversion steps have succeeded. At DONE,
        // 4b's participant can move the original envelopes without making an
        // uncharged pre-admission copy of their payloads.
        if retain
            || matches!(
                name.as_str(),
                "Complete" | "Unavailable" | "BudgetExhausted"
            )
        {
            self.retained.push(frame)
        }
        Ok(Rust3Admitted {
            sequence,
            trace,
            payload,
            spool_entries,
        })
    }
    fn current_stage(&self) -> usize {
        match self.run.field("stageIndex") {
            Some(Scalar::Int(i)) => usize::try_from(*i).unwrap_or(usize::MAX),
            _ => usize::MAX,
        }
    }
    fn admit(&mut self, frame: &ReceivedFrame) -> Result<(u64, String, Event, bool), Rust3Refusal> {
        use Rust3Refusal::{Admission, Envelope, Schema};
        let (name, sequence) = self
            .schemas
            .check_envelope(frame.value(), "worker-to-host")
            .map_err(Envelope)?;
        if !self.sequence.accept(sequence) {
            return Err(Envelope("worker sequence".to_owned()));
        }
        let env = map_of(frame.value()).ok_or_else(|| Envelope("envelope".to_owned()))?;
        let payload = field(env, "payload").ok_or_else(|| Envelope("payload".to_owned()))?;
        let node =
            child(frame, 0, env, "payload").ok_or_else(|| Envelope("payload node".to_owned()))?;
        self.schemas
            .check_payload(&name, payload, self.phase(), self.target_attribution)
            .map_err(Schema)?;
        let f = map_of(payload).ok_or_else(|| Schema("payload map".to_owned()))?;
        let stage = self.current_stage();
        let mut event = Event::frame(&name);
        let mut retain = false;
        let echoes_analysis = matches!(
            name.as_str(),
            "FactBatch" | "CoverageV3" | "BudgetExhausted" | "Complete"
        ) || (name == "Unavailable" && self.phase() == "ANALYZING");
        if echoes_analysis && u64_of(f, "analysisOrdinal") != Some(self.context.analysis_ordinal) {
            return Err(Admission("Analyze ordinal echo".to_owned()));
        }
        match name.as_str() {
            "HelloAck" => {
                self.hello_ack(f).map_err(Admission)?;
                event.identity_negotiated = true;
            }
            "UniverseAccepted" => {
                let open = map_of(&self.context.open_universe)
                    .ok_or_else(|| Admission("OpenUniverse".to_owned()))?;
                for (name, value) in f {
                    if field(open, name) != Some(value) {
                        return Err(Admission(format!("UniverseAccepted.{name} recursive echo")));
                    }
                }
            }
            "SnapshotAccepted" => {
                if payload != &self.context.snapshot_seal {
                    return Err(Admission("SnapshotAccepted is not Seal".to_owned()));
                }
            }
            "DependencySourceAccepted" => {
                if payload != &self.context.dependency_seal {
                    return Err(Admission("DependencySourceAccepted is not Seal".to_owned()));
                }
            }
            "PreparedOutputAccepted" => {
                if Some(payload) != self.context.prepared_seal.as_ref() {
                    return Err(Admission("PreparedOutputAccepted is not Seal".to_owned()));
                }
            }
            "NativeContextVerified" => {
                let native = self
                    .native_context_id()
                    .ok_or_else(|| Admission("nativeContextId".to_owned()))?;
                if text_of(f, "nativeContextId") != Some(native)
                    || text_of(f, "recomputedNativeContextId") != Some(native)
                {
                    return Err(Admission("native context echo/equality".to_owned()));
                }
            }
            "FactBatch" => {
                self.fact_batch(frame, node, f, stage).map_err(Admission)?;
                retain = true;
            }
            "CoverageV3" => {
                self.coverage(frame, node, f, stage).map_err(Admission)?;
                retain = true;
            }
            "Complete" => self.complete(f).map_err(Admission)?,
            "Unavailable" => {
                if self.phase() == "WAIT_NATIVE_CONTEXT_VERIFIED" {
                    self.pre_analyze_unavailable(f).map_err(Admission)?;
                } else {
                    self.terminal_coverage(
                        frame,
                        node,
                        f,
                        "Startup1UnavailableV3.coverageCommitment",
                        "provider-unavailable",
                    )
                    .map_err(Admission)?;
                    let want = self
                        .stages
                        .iter()
                        .map(|s| Value::Text(s.expected_stage_id.clone()))
                        .collect::<Vec<_>>();
                    if array_of(f, "affectedStageIds") != want.as_slice() {
                        return Err(Admission(
                            "affectedStageIds stage-major bijection".to_owned(),
                        ));
                    }
                }
            }
            "BudgetExhausted" => {
                let binding = self
                    .stages
                    .get(stage)
                    .ok_or_else(|| Admission("no current stage".to_owned()))?;
                let (unit, limit) = binding
                    .budget
                    .as_ref()
                    .ok_or_else(|| Admission("no current stage budget".to_owned()))?;
                if !["items", "bytes", "work-units"].contains(&unit.as_str())
                    || text_of(f, "unit") != Some(unit.as_str())
                    || u64_of(f, "limit") != Some(*limit)
                    || u64_of(f, "observed") != limit.checked_add(1)
                    || text_of(f, "triggerStageId") != Some(binding.expected_stage_id.as_str())
                {
                    return Err(Admission(
                        "T020 current-stage unit/limit/observed".to_owned(),
                    ));
                }
                self.terminal_coverage(
                    frame,
                    node,
                    f,
                    "Startup1BudgetExhaustedV3.coverageCommitment",
                    "budget-exhausted",
                )
                .map_err(Admission)?;
            }
            "ProviderFault" => {
                if !self.fault_window.matches(payload) {
                    return Err(Admission(
                        "ProviderFault joint worker observation".to_owned(),
                    ));
                }
            }
            "Cancelled" => {
                let (execution, ordinal, phase) = self
                    .cancel
                    .as_ref()
                    .ok_or_else(|| Admission("Cancelled without Cancel".to_owned()))?;
                let got_exec = match field(f, "executionId") {
                    Some(Value::Null) => None,
                    Some(Value::Text(s)) => Some(s.clone()),
                    _ => return Err(Admission("Cancelled executionId".to_owned())),
                };
                let got_ordinal = match field(f, "analysisOrdinal") {
                    Some(Value::Null) => None,
                    Some(Value::Unsigned(n)) => Some(*n),
                    _ => return Err(Admission("Cancelled ordinal".to_owned())),
                };
                if &got_exec != execution
                    || &got_ordinal != ordinal
                    || text_of(f, "observedPhase") != Some(phase.as_str())
                {
                    return Err(Admission("Cancelled echo/send phase".to_owned()));
                }
            }
            _ => return Err(Admission(format!("no worker admission for {name}"))),
        }
        Ok((sequence, name, event, retain))
    }
    fn native_context_id(&self) -> Option<&str> {
        let open = map_of(&self.context.open_universe)?;
        let universe = field(open, "universe").and_then(map_of)?;
        let inputs = field(universe, "resolvedInputs").and_then(map_of)?;
        text_of(inputs, "nativeContextId")
    }
    fn hello_ack(&self, f: &[(String, Value)]) -> Result<(), String> {
        let hello = map_of(&self.context.hello).ok_or("Hello")?;
        let expected = field(hello, "expectedIdentity")
            .and_then(map_of)
            .ok_or("expectedIdentity")?;
        if field(f, "capabilities") != field(hello, "expectedCapabilities")
            || field(f, "identityVersions") != field(hello, "identityVersions")
        {
            return Err("Hello capability/identity-version exact echo".to_owned());
        }
        for (key, value) in expected {
            if field(f, key) != Some(value) {
                return Err(format!("HelloAck.{key} expectedIdentity echo"));
            }
        }
        Ok(())
    }
    fn pre_analyze_unavailable(&self, f: &[(String, Value)]) -> Result<(), String> {
        let open = map_of(&self.context.open_universe).ok_or("OpenUniverse")?;
        for key in ["executionId", "snapshotId", "planId"] {
            if field(f, key) != field(open, key) {
                return Err(format!("Unavailable.{key} echo"));
            }
        }
        let native = self.native_context_id().ok_or("nativeContextId")?;
        if text_of(f, "nativeContextId") != Some(native)
            || text_of(f, "recomputedNativeContextId") == Some(native)
        {
            return Err("pre-Analyze context inequality".to_owned());
        }
        Ok(())
    }

    fn candidate(&self, c: &[(String, Value)], binding: &Stage) -> Result<(), String> {
        let relation = text_of(c, "relation").ok_or("relation")?;
        if !binding.relations.iter().any(|r| r == relation) {
            return Err(format!("relation {relation} is not requested by the stage"));
        }
        let (ladder, schema_id, version) = self
            .law
            .registry
            .get(relation)
            .ok_or(format!("relation {relation} is not registered"))?;
        if !ladder
            .iter()
            .any(|r| Some(r.as_str()) == text_of(c, "resolution"))
        {
            return Err("resolution is not a rung of the relation's ladder".to_owned());
        }
        let layer = self
            .law
            .layers
            .get(relation)
            .ok_or(format!("relation {relation} has no fact-plane layer"))?;
        if text_of(c, "layer") != Some(layer.as_str()) {
            return Err("layer is not the relation's".to_owned());
        }
        if field(c, "producerVersion")
            != map_of(&self.context.hello)
                .and_then(|f| field(f, "expectedIdentity"))
                .and_then(map_of)
                .and_then(|f| field(f, "providerBuildId"))
        {
            return Err("producerVersion is not the verified providerBuildId".to_owned());
        }
        if u64_of(c, "schemaVersion") != Some(*version)
            || text_of(c, "relationSchemaId") != Some(schema_id.as_str())
        {
            return Err("relationSchemaId or schemaVersion is not the registry's".to_owned());
        }
        if text_of(c, "sourceUniverseId") != Some(&self.context.universe_key) {
            return Err("sourceUniverseId is not OpenUniverse's universeKey".to_owned());
        }
        if !text_of(c, "targetUniverseId").is_some_and(|t| self.context.target_domain.contains(t)) {
            return Err("targetUniverseId is outside the admitted target domain".to_owned());
        }
        let Some(Value::Bytes(payload)) = field(c, "canonicalRelationPayload") else {
            return Err("canonicalRelationPayload".to_owned());
        };
        // Decode once under the registry's restricted profile (no negative
        // integer, no byte string) and its own depth bound; the decoder's
        // re-encoding comparison is the byte equality.
        let decoded = cbor::decode(payload, cbor::Profile::Rust3, RELATION_PAYLOAD_MAX_DEPTH)
            .map_err(|e| format!("canonicalRelationPayload: {}", e.code()))?;
        if contains_bytes(&decoded) {
            return Err("canonicalRelationPayload holds a byte string".to_owned());
        }
        for a in array_of(c, "anchors").iter().filter_map(map_of) {
            match text_of(a, "kind") {
                Some("fact-ref") => return Err("a fact-ref anchor".to_owned()),
                Some("source-span") => {
                    if text_of(a, "snapshotId")
                        != map_of(&self.context.open_universe)
                            .and_then(|f| text_of(f, "snapshotId"))
                    {
                        return Err("anchor snapshotId is not snapshot2".to_owned());
                    }
                    let (digest, length) = text_of(a, "path")
                        .and_then(|p| self.context.manifest_files.get(p))
                        .ok_or("anchor path is not a manifest file")?;
                    if text_of(a, "contentSha256") != Some(digest.as_str()) {
                        return Err("anchor contentSha256 is not the entry's".to_owned());
                    }
                    let (start, end) = (
                        u64_of(a, "startByte").ok_or("startByte")?,
                        u64_of(a, "endByte").ok_or("endByte")?,
                    );
                    if !(start < end && end <= *length) {
                        return Err("anchor span is empty or outside the file".to_owned());
                    }
                }
                _ => return Err("anchor kind".to_owned()),
            }
        }
        Ok(())
    }

    fn entry_echoes(entry: &Value, key: &RequestedKey) -> Result<(), String> {
        let e = map_of(entry).ok_or("entry")?;
        let k = field(e, "key").and_then(map_of).ok_or("entry key")?;
        let examined = field(e, "entry")
            .and_then(map_of)
            .and_then(|v| field(v, "examinedUniverse"))
            .and_then(map_of)
            .ok_or("examinedUniverse")?;
        let ok = text_of(k, "relation") == Some(&key.relation)
            && text_of(k, "resolution") == Some(&key.resolution)
            && text_of(k, "subjectScopeCommitment") == Some(&key.subject_scope_commitment)
            && text_of(k, "sourceUniverse") == suffix(&key.source_universe_id)
            && text_of(k, "targetUniverse") == suffix(&key.target_universe_id)
            && text_of(examined, "subjectScopeCommitment") == Some(&key.subject_scope_commitment)
            && u64_of(examined, "subjectCount") == Some(key.subject_count);
        if ok {
            Ok(())
        } else {
            Err("an entry is not its requested key's echo".to_owned())
        }
    }

    fn fact_batch(
        &mut self,
        frame: &ReceivedFrame,
        node: usize,
        f: &[(String, Value)],
        stage: usize,
    ) -> Result<(), String> {
        let binding = self.stages.get(stage).ok_or("no current stage")?;
        let live = self.live.get(stage).ok_or("no live stage")?;
        if text_of(f, "stageId") != Some(binding.expected_stage_id.as_str())
            || u64_of(f, "batchIndex") != Some(live.batches)
        {
            return Err("stageId/batchIndex not current stage".to_owned());
        }
        let candidates = array_of(f, "candidates");
        let first = candidates
            .first()
            .and_then(map_of)
            .and_then(|f| u64_of(f, "candidateOrdinal"));
        if candidates.is_empty()
            || candidates.len() as u64 > self.law.max_batch_candidates
            || first != Some(live.next_candidate)
        {
            return Err("T016 first candidate/count".to_owned());
        }
        let next_batch = live.batches.checked_add(1).ok_or("batchIndex overflow")?;
        let next_candidate = live
            .next_candidate
            .checked_add(candidates.len() as u64)
            .ok_or("candidateOrdinal overflow")?;
        for (i, c) in candidates.iter().enumerate() {
            let c = map_of(c).ok_or("candidate")?;
            if u64_of(c, "candidateOrdinal") != live.next_candidate.checked_add(i as u64) {
                return Err("candidateOrdinal continuity".to_owned());
            }
            self.candidate(c, binding)?;
        }
        if self.target_attribution {
            let companions = array_of(f, "occupancyCompanions");
            if companions.len() > candidates.len() {
                return Err("too many occupancy companions".to_owned());
            }
            let by_ordinal = candidates
                .iter()
                .filter_map(map_of)
                .map(|c| {
                    Ok((
                        u64_of(c, "candidateOrdinal").ok_or("candidateOrdinal")?,
                        text_of(c, "targetUniverseId").ok_or("targetUniverseId")?,
                    ))
                })
                .collect::<Result<BTreeMap<_, _>, String>>()?;
            for o in companions {
                let o = map_of(o).ok_or("companion")?;
                let ordinal = u64_of(o, "candidateOrdinal").ok_or("companion ordinal")?;
                if by_ordinal.get(&ordinal).copied() != text_of(o, "targetUniverseId") {
                    return Err("occupancy companion batch join".to_owned());
                }
            }
        }
        let list = child(frame, node, f, "candidates").ok_or("candidate nodes")?;
        let nodes = frame.children(list).collect::<Vec<_>>();
        if nodes.len() != candidates.len() {
            return Err("candidate provenance count".to_owned());
        }
        let live = &mut self.live[stage];
        live.batches = next_batch;
        live.next_candidate = next_candidate;
        let index = self.retained.len();
        live.facts.extend(nodes.into_iter().map(|n| (index, n)));
        Ok(())
    }
    fn coverage(
        &mut self,
        frame: &ReceivedFrame,
        node: usize,
        f: &[(String, Value)],
        stage: usize,
    ) -> Result<(), String> {
        let binding = self.stages.get(stage).ok_or("no current stage")?;
        if text_of(f, "stageId") != Some(binding.expected_stage_id.as_str()) {
            return Err("coverage current stage".to_owned());
        }
        let entries = array_of(f, "entries");
        if entries.len() != binding.keys.len() {
            return Err("coverage key bijection count".to_owned());
        }
        for (e, k) in entries.iter().zip(&binding.keys) {
            Self::entry_echoes(e, k)?;
        }
        let list = child(frame, node, f, "entries").ok_or("coverage nodes")?;
        let nodes = frame.children(list).collect::<Vec<_>>();
        let received = nodes
            .iter()
            .map(|n| frame.node(*n).ok_or("received coverage"))
            .collect::<Result<Vec<_>, _>>()?;
        if received.len() != entries.len()
            || text_of(f, "coverageCommitment")
                != Some(
                    commit(
                        self.law.domain("Startup1CoverageV3.coverageCommitment")?,
                        &received,
                    )
                    .as_str(),
                )
        {
            return Err("stage coverage commitment".to_owned());
        }
        let index = self.retained.len();
        self.live[stage].coverage = nodes.into_iter().map(|n| (index, n)).collect();
        Ok(())
    }
    fn terminal_coverage(
        &self,
        frame: &ReceivedFrame,
        node: usize,
        f: &[(String, Value)],
        domain_field: &str,
        deficiency: &str,
    ) -> Result<(), String> {
        let keys = self.stages.iter().flat_map(|s| &s.keys).collect::<Vec<_>>();
        let entries = array_of(f, "coverage");
        if keys.len() != entries.len() {
            return Err("terminal stage-major coverage count".to_owned());
        }
        for (e, k) in entries.iter().zip(keys) {
            Self::entry_echoes(e, k)?;
            let view = map_of(e)
                .and_then(|f| field(f, "entry"))
                .and_then(map_of)
                .ok_or("coverage entry")?;
            if text_of(view, "coverage") != Some("unknown")
                || text_of(view, "deficiency") != Some(deficiency)
            {
                return Err("terminal coverage unknown/deficiency".to_owned());
            }
        }
        let list = child(frame, node, f, "coverage").ok_or("terminal coverage node")?;
        let received = frame
            .children(list)
            .map(|n| frame.node(n).ok_or("received terminal coverage"))
            .collect::<Result<Vec<_>, _>>()?;
        if received.len() != entries.len()
            || text_of(f, "coverageCommitment")
                != Some(commit(self.law.domain(domain_field)?, &received).as_str())
        {
            return Err("terminal coverage commitment".to_owned());
        }
        Ok(())
    }
    fn retained_bytes(&self, at: &[(usize, usize)]) -> Option<Vec<ReceivedBytes<'_>>> {
        at.iter()
            .map(|(f, n)| self.retained.get(*f)?.node(*n))
            .collect()
    }
    fn complete(&self, f: &[(String, Value)]) -> Result<(), String> {
        let results = array_of(f, "stageResults");
        if results.len() != self.stages.len() {
            return Err("complete stage bijection count".to_owned());
        }
        let fact_domain = self.law.domain("Rust3StageResultV2.factCommitment")?;
        let coverage_domain = self.law.domain("Rust3StageResultV2.coverageCommitment")?;
        for ((r, s), live) in results.iter().zip(&self.stages).zip(&self.live) {
            let r = map_of(r).ok_or("stage result")?;
            if text_of(r, "stageId") != Some(s.expected_stage_id.as_str())
                || u64_of(r, "factCount") != Some(live.facts.len() as u64)
                || u64_of(r, "coverageEntryCount") != Some(live.coverage.len() as u64)
            {
                return Err("complete stage observed counts/order".to_owned());
            }
            let facts = self
                .retained_bytes(&live.facts)
                .ok_or("retained stage facts")?;
            let coverage = self
                .retained_bytes(&live.coverage)
                .ok_or("retained stage coverage")?;
            if text_of(r, "factCommitment") != Some(commit(fact_domain, &facts).as_str())
                || text_of(r, "coverageCommitment")
                    != Some(commit(coverage_domain, &coverage).as_str())
            {
                return Err("complete stage commitments".to_owned());
            }
        }
        let all_facts = self
            .live
            .iter()
            .flat_map(|s| s.facts.iter().copied())
            .collect::<Vec<_>>();
        let all_coverage = self
            .live
            .iter()
            .flat_map(|s| s.coverage.iter().copied())
            .collect::<Vec<_>>();
        let facts = self
            .retained_bytes(&all_facts)
            .ok_or("retained stream facts")?;
        let coverage = self
            .retained_bytes(&all_coverage)
            .ok_or("retained stream coverage")?;
        if text_of(f, "factStreamCommitment")
            != Some(
                commit(
                    self.law.domain("Rust3CompleteV2.factStreamCommitment")?,
                    &facts,
                )
                .as_str(),
            )
            || text_of(f, "coverageStreamCommitment")
                != Some(
                    commit(
                        self.law
                            .domain("Rust3CompleteV2.coverageStreamCommitment")?,
                        &coverage,
                    )
                    .as_str(),
                )
        {
            return Err("complete stream commitments".to_owned());
        }
        Ok(())
    }
}
fn commit(domain: &str, parts: &[ReceivedBytes<'_>]) -> String {
    #[cfg(test)]
    PROVENANCE.with_borrow_mut(|log| {
        log.push((
            domain.to_owned(),
            parts
                .iter()
                .map(|p| (p.as_bytes().as_ptr() as usize, p.as_bytes().len()))
                .collect(),
        ))
    });
    received_commitment(domain, parts)
}
#[cfg(test)]
type Provenance = Vec<(String, Vec<(usize, usize)>)>;
#[cfg(test)]
thread_local! {static PROVENANCE:std::cell::RefCell<Provenance>=const{std::cell::RefCell::new(Vec::new())};}

#[cfg(test)]
#[path = "receive_tests.rs"]
pub(super) mod tests;
