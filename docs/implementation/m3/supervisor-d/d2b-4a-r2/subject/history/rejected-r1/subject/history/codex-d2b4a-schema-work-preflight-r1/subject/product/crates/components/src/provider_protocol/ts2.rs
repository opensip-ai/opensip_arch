//! M3-D r5 items 10 and 11 (unit D2b-3a; D2b plan r3 as amendments A1 and A2
//! amend it): the TS2 codec's receive side. Each worker frame takes
//! LD-D2B-12's steps 7 to 10 in order, and a refusal at any step is
//! `PROVIDER.PROTOCOL_VIOLATION`, recorded before the frame's payload is
//! published:
//! 7. the envelope (TS2-ENV-MAJOR, TS2-ENV-DIRECTION-BY-FRAME,
//!    TS2-ENV-SEQUENCE);
//! 8. the closed schema: the carrier-typed decode for the inherited frames
//!    (LD-D2B3-1), the product schema for the extern ones (LD-D2B3-2);
//! 9. the contextual admission (LD-D2B-15) against the immutable
//!    [`DispatchContext`] and the live state: the echoes, the stage
//!    correlation and batch counters, the candidate and anchor laws, and the
//!    commitments recomputed over the received bytes (LD-D2B-3);
//! 10. the transition table (D2b-2's engine over T2O), fed the event this
//!    module derives.
//!
//! Only then is the payload converted into the generated carriers
//! (`Ts2FrameV2Payload`). The host's own frames are recorded through
//! [`Ts2Receiver::sent`], which steps the same table; building and sending
//! them is D2b-3b's (`ts2/send.rs`), and the table's admission of a host
//! frame is [`Ts2Receiver::admits`]. FA-2's census payloads (unit D2b-3c, LD-D2B-16) are
//! selected by the symbol-census law's negotiation: with `symbol-census-v1`
//! in both token arrays, Complete is `TypeScriptCompleteV2`, admitted
//! piecewise with its census (LD-D2B3C-2 to LD-D2B3C-6).
use super::cbor::{self, Value};
use super::table::{Event, Protocol, Run, Scalar, Table};
use super::{ProcessEvent, ReceivedBytes, ReceivedFrame, Sequence, received_commitment};
use opensip_contracts::generated::protocol::{SymbolCensus1SymbolCensusV1, Ts2FrameV2Payload};
use opensip_identity::{JsonValue as J, digest_hex, parse_json, raw_sha256};
use std::collections::{BTreeMap, BTreeSet};

#[path = "ts2/build.rs"]
mod build;
#[path = "ts2/carrier.rs"]
pub(super) mod carrier;
#[path = "ts2/participant.rs"]
mod participant;
#[path = "ts2/send.rs"]
mod send;
use carrier::{Carriers, admit_extern, field};
pub use participant::Ts2Participant;
pub use send::{
    ChunkCoordinates, PlanRefusal, SendRefusal, Sent, Slot, SlotFrame, SnapshotEntry,
    SnapshotSource, StageBudget, StagePlan, Ts2Plan, Ts2Request, Ts2Schedule, Ts2Sender,
};

const FACT_PLANE: &[u8] = include_bytes!("../../data/fact-plane.v1.json");
const RELATION_REGISTRY: &[u8] = include_bytes!("../../data/relation-payload-schemas.v2.json");
const T2O: &[u8] = include_bytes!("../../data/typescript-protocol2-order.v1.json");
const HANDSHAKE: &[u8] = include_bytes!("../../../../schemas/sources/handshake-v1.schema.json");
const STARTUP: &[u8] = include_bytes!("../../../../schemas/sources/startup-v1.schema.json");
const STARTUP_ID: &str = "opensip.product.provider-startup.1";
const SYMBOL_CENSUS: &[u8] =
    include_bytes!("../../../../schemas/sources/symbol-census-v1.schema.json");
const CENSUS_ID: &str = "opensip.product.symbol-census.1";

/// A complete census's bound: its deterministic CBOR is at most 4,194,304
/// bytes (symbol-census-v1 `x-opensip-symbol-census-law.return`, "4194304
/// bytes of deterministic CBOR"; NE §9.8). The law's text is checked at load.
pub const CENSUS_MAX_BYTES: u64 = 4_194_304;

/// The deepest container nesting of any TS2 frame, the envelope included
/// (LD-D2B-2), over the inherited closure: the carriers' TS2 records and
/// every product schema their frames and extern members reach. The reader
/// takes it as its bound (`FrameAccumulator::new`). A test recomputes it
/// from those documents; D2b-3c recomputes it with FA-2's payloads.
pub const TS2_FRAME_MAX_DEPTH: usize = 7;
/// The deepest container nesting of a relation payload (LD-D2B-2's embedded
/// payload), over `relation-payload-schemas.v2.json`'s schemas; a test
/// recomputes it.
pub const RELATION_PAYLOAD_MAX_DEPTH: usize = 1;

/// A refusal, by step. Every one is `PROVIDER.PROTOCOL_VIOLATION`.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Ts2Refusal {
    /// The receiver's own data or context does not load: no frame is read.
    Context(String),
    /// Step 7.
    Envelope(String),
    /// Step 8.
    Schema(String),
    /// Step 9.
    Admission(String),
    /// Step 10: the table's trace (`T2-22`, `T2-23`, `post-terminal-frame`).
    Table(String),
    /// A frame after a refusal: a refusal ends the session.
    AfterRefusal,
}

/// The verified provider descriptor's and runtime descriptor's members the
/// HelloAck must equal (handshake-v1 `x-opensip-wire-law.typescriptDescriptorBinding`;
/// D2b plan r3 amendment A2), by their wire names.
pub type DescriptorFields = BTreeMap<String, Value>;

/// One requested coverage key (Analyze's `requestedCoverageDomain.keys[i]`).
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RequestedKey {
    pub relation: String,
    pub resolution: String,
    pub source_universe_id: String,
    pub target_universe_id: String,
    pub subject_scope_commitment: String,
}

/// One requested stage's `DispatchBindingV1` (LD-D2B-15).
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct StageBinding {
    pub expected_stage_id: String,
    /// The Analyze-relative ordinal, never the retained one.
    pub stage_ordinal: u64,
    pub relations: Vec<String>,
    /// The stage's `ProviderWorkBudgetV1`, by member name.
    pub budget: BTreeMap<String, u64>,
    pub keys: Vec<RequestedKey>,
}

/// The immutable context LD-D2B-15 lists, built by D4's session factory from
/// the admitted Plan before spawn (no producer exists yet).
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DispatchContext {
    /// The Hello's `expectedCapabilities`: the selected tokens (LD-D2B-18).
    pub capabilities: Vec<String>,
    /// The Hello's `identityVersions`.
    pub identity_versions: BTreeMap<String, u64>,
    pub expected_provider_descriptor_sha256: String,
    pub expected_runtime_descriptor_sha256: String,
    /// A2: the verified descriptors' `providerDescriptorFields` and
    /// `runtimeDescriptorFields`. The verified `providerBuildId` is one of
    /// them, and is also FactCandidateV1's `producerVersion`.
    pub provider_descriptor: DescriptorFields,
    pub runtime_descriptor: DescriptorFields,
    /// OpenUniverse's values.
    pub execution_id: String,
    pub snapshot_id: String,
    pub plan_id: String,
    pub universe_key: String,
    pub native_context_id: String,
    /// The sent manifest's `kind: file` entries: path to (contentSha256,
    /// byteLength); and the Seal's values.
    pub manifest_files: BTreeMap<String, (String, u64)>,
    pub manifest_sha256: String,
    pub entry_count: u64,
    pub total_file_bytes: u64,
    pub total_chunk_count: u64,
    /// The requested stages, in Analyze order.
    pub stages: Vec<StageBinding>,
    /// The host-admitted target domain (FP-CANDIDATE).
    pub target_domain: BTreeSet<String>,
    /// The census Analyze requested (unit D2b-3c, LD-D2B-16): its
    /// `enumeratorClosure`, or `None` when no census is owed.
    pub symbol_census: Option<String>,
}

/// A host frame the sender wrote, recorded for the echoes and the table.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum HostFrame {
    Hello,
    OpenUniverse,
    SnapshotManifest,
    SnapshotFileChunk,
    SnapshotSeal,
    Analyze,
    Cancel {
        execution_id: Option<String>,
        analysis_ordinal: Option<u64>,
    },
}

/// One admitted worker frame: its sequence, the table's trace, and the
/// payload as the generated carrier.
#[derive(Debug, Clone)]
pub struct Admitted {
    pub sequence: u64,
    pub trace: String,
    pub payload: Ts2FrameV2Payload,
    /// A census-bearing Complete's census (LD-D2B3C-3): `Ts2FrameV2Payload`
    /// has no census variant, so `payload` carries TypeScriptCompleteV2's
    /// inherited members as `Complete` and the census is here. An over-bound
    /// census is admitted as this typed event (LD-D2B3C-5).
    pub census: Option<SymbolCensus1SymbolCensusV1>,
}

/// A stage's live state (LD-D2B-15): the next `batchIndex` and
/// `candidateOrdinal`, and where its received candidates and entries lie.
#[derive(Debug, Clone, Default)]
struct StageLive {
    batches: u64,
    next_candidate: u64,
    facts: Vec<(usize, usize)>,
    coverage: Vec<(usize, usize)>,
}

/// One worker frame payload's carrier selection (the carriers' `frames`).
#[derive(Debug, Clone)]
enum Payload {
    Record(String),
    Extern(String),
}

/// The data the receiver loads once: the carrier records, the frame table
/// of payload selections, the commitment domains, the fact-plane registry
/// and the handshake and startup laws it reads.
struct Law {
    carriers: Carriers,
    frames: BTreeMap<String, BTreeMap<String, Payload>>,
    worker_frames: BTreeSet<String>,
    domains: BTreeMap<String, String>,
    /// relation -> (ladder, schemaId, schemaVersion), relation-payload-schemas.v2.
    registry: BTreeMap<String, (Vec<String>, String, u64)>,
    /// relation -> subjectKind, relation-payload-schemas.v2 (LD-D2B3C-6).
    subject_kinds: BTreeMap<String, String>,
    /// The census's law (LD-D2B3C-4, LD-D2B3C-5).
    census: CensusLaw,
    /// relation -> layer, fact-plane.v1 relationRegistry.
    layers: BTreeMap<String, String>,
    identity_tokens: Vec<String>,
    provider_fields: Vec<String>,
    runtime_fields: Vec<String>,
    /// TS2-OBSERVED-PHASE: the host phases at Cancel, and the phase observed.
    cancel_phases: Vec<String>,
    cancel_observed: String,
    /// Each piecewise extern payload's array member and its item schema.
    piecewise: BTreeMap<String, (String, String, Option<u64>, Option<u64>)>,
}

/// The census's law, read from symbol-census-v1 and checked as implemented
/// (LD-D2B3C-4, LD-D2B3C-5).
struct CensusLaw {
    /// CompleteSymbolCensusV1's `examinedPaths` and `rows`: maxItems, their
    /// item `$ref`s and their `x-opensip-order` annotations.
    paths_max: u64,
    rows_max: u64,
    path_ref: String,
    row_ref: String,
    paths_order: opensip_identity::ArrayOrder,
    rows_order: opensip_identity::ArrayOrder,
    /// The members' maxLength (scalars) and maxItems the over-bound
    /// within-bounds bound reads: LogicalPath, SubjectIdV1, qualifiedName,
    /// signatureTokens and its items.
    path_scalars: u64,
    subject_scalars: u64,
    name_scalars: u64,
    tokens_max: u64,
    token_scalars: u64,
}

impl CensusLaw {
    fn load() -> Result<Self, String> {
        let doc = parse_json(SYMBOL_CENSUS).map_err(|e| format!("symbol census: {e}"))?;
        let defs = |name: &str| path(&doc, &["$defs", name]).ok_or(format!("census {name}"));
        let int = |v: Option<&J>, what: &str| match v {
            Some(J::Integer(i)) => u64::try_from(i.get()).map_err(|_| what.to_owned()),
            _ => Err(format!("census {what}")),
        };
        let law = path(&doc, &["x-opensip-symbol-census-law", "return"])
            .and_then(txt)
            .ok_or("census return law")?;
        if !law.contains(&format!("{CENSUS_MAX_BYTES} bytes of deterministic CBOR")) {
            return Err("the census law's byte bound is not the implemented one".to_owned());
        }
        let complete = defs("CompleteSymbolCensusV1")?;
        let member = |m: &str| path(complete, &["properties", m]).ok_or(format!("census {m}"));
        let (paths, rows) = (member("examinedPaths")?, member("rows")?);
        let item_ref = |a: &J, what: &str| {
            path(a, &["items", "$ref"])
                .and_then(txt)
                .map(|r| format!("{CENSUS_ID}{r}"))
                .ok_or(format!("census {what} items"))
        };
        let order = |a: &J, what: &str| {
            opensip_identity::ArrayOrder::parse(
                path(a, &["x-opensip-order"]).ok_or(format!("census {what} order"))?,
            )
            .map_err(|e| format!("census {what} order: {e}"))
        };
        let row = defs("SymbolCensusRowV1")?;
        let row_member = |m: &str| path(row, &["properties", m]).ok_or(format!("census row {m}"));
        // The piecewise token leaf below implements exactly this closed
        // scalar shape. A future additional constraint must not be ignored.
        let token_item = path(row_member("signatureTokens")?, &["items"])
            .ok_or("census signatureTokens items")?;
        let token_fields = obj(token_item).ok_or("census signatureTokens item shape")?;
        if token_fields.len() != 3
            || token_fields
                .keys()
                .any(|key| !["type", "minLength", "maxLength"].contains(&key.as_str()))
            || path(token_item, &["type"]).and_then(txt) != Some("string")
            || int(
                path(token_item, &["minLength"]),
                "signatureTokens minLength",
            )? != 0
        {
            return Err("the census token item law is not the implemented scalar shape".to_owned());
        }
        let paths_max = int(path(paths, &["maxItems"]), "examinedPaths maxItems")?;
        let rows_max = int(path(rows, &["maxItems"]), "rows maxItems")?;
        if !law.contains(&format!("{rows_max} rows"))
            || !law.contains(&format!("{paths_max} examined paths"))
        {
            return Err("the census law's count bounds are not the schema's".to_owned());
        }
        Ok(Self {
            paths_max,
            rows_max,
            path_ref: item_ref(paths, "examinedPaths")?,
            row_ref: item_ref(rows, "rows")?,
            paths_order: order(paths, "examinedPaths")?,
            rows_order: order(rows, "rows")?,
            path_scalars: int(path(defs("LogicalPath")?, &["maxLength"]), "LogicalPath")?,
            subject_scalars: int(path(defs("SubjectIdV1")?, &["maxLength"]), "SubjectIdV1")?,
            name_scalars: int(
                path(row_member("qualifiedName")?, &["maxLength"]),
                "qualifiedName",
            )?,
            tokens_max: int(
                path(row_member("signatureTokens")?, &["maxItems"]),
                "signatureTokens",
            )?,
            token_scalars: int(
                path(row_member("signatureTokens")?, &["items", "maxLength"]),
                "signatureTokens items",
            )?,
        })
    }

    /// An upper bound on the deterministic CBOR of any complete census with
    /// `rows` rows and `paths` examined paths: each text at its maximum
    /// scalars of at most 4 UTF-8 bytes, each head at its widest 9 bytes. If
    /// even this fits under the bound, an over-bound census with these counts
    /// is within every bound (`native.symbol-census-over-bound-within-bounds`).
    fn max_complete_bytes(&self, rows: u64, paths: u64) -> u64 {
        let text = |scalars: u64| 9 + 4 * scalars;
        let key = |k: &str| 1 + k.len() as u64;
        let row = 9
            + key("nativeSubjectId")
            + text(self.subject_scalars)
            + key("path")
            + text(self.path_scalars)
            + key("qualifiedName")
            + text(self.name_scalars)
            + key("exported")
            + text("not-exported".len() as u64)
            + key("signatureTokens")
            + 9
            + self.tokens_max * text(self.token_scalars);
        9u64.saturating_add(key("state") + text("complete".len() as u64))
            .saturating_add(key("examinedPaths") + 9)
            .saturating_add(paths.saturating_mul(text(self.path_scalars)))
            .saturating_add(key("rows") + 9)
            .saturating_add(rows.saturating_mul(row))
    }
}

fn obj(v: &J) -> Option<&BTreeMap<String, J>> {
    match v {
        J::Object(o) => Some(o),
        _ => None,
    }
}
fn txt(v: &J) -> Option<&str> {
    match v {
        J::String(s) => Some(s),
        _ => None,
    }
}
fn strs(v: Option<&J>) -> Option<Vec<String>> {
    match v? {
        J::Array(a) => a.iter().map(|x| txt(x).map(str::to_owned)).collect(),
        _ => None,
    }
}
fn path<'j>(v: &'j J, keys: &[&str]) -> Option<&'j J> {
    keys.iter().try_fold(v, |v, k| obj(v)?.get(*k))
}

impl Law {
    fn load() -> Result<Self, String> {
        let carriers = Carriers::load("Ts2")?;
        let doc = parse_json(carrier::CARRIERS).map_err(|e| format!("carriers: {e}"))?;
        // The vendored registries are the carriers' own source pins.
        let J::Array(pins) = path(&doc, &["sourcePins"]).ok_or("sourcePins")? else {
            return Err("sourcePins".to_owned());
        };
        for (key, raw) in [
            ("factPlane", FACT_PLANE),
            ("relationRegistry2", RELATION_REGISTRY),
        ] {
            let pin = pins
                .iter()
                .filter_map(obj)
                .find(|p| p.get("key").and_then(txt) == Some(key))
                .ok_or(format!("pin {key}"))?;
            if pin.get("sha256").and_then(txt) != Some(digest_hex(&raw_sha256(raw)).as_str()) {
                return Err(format!("pin {key}"));
            }
        }
        // The frames: each worker frame's payload, by host selector value.
        let mut frames = BTreeMap::new();
        let mut worker_frames = BTreeSet::new();
        let J::Array(list) =
            path(&doc, &["protocols", "typescript-semantic", "frames"]).ok_or("frames")?
        else {
            return Err("frames".to_owned());
        };
        let selection = |p: &J| -> Result<Payload, String> {
            let p = obj(p).ok_or("payload")?;
            match p.get("t").and_then(txt) {
                Some("ref") => Ok(Payload::Record(
                    p.get("ref").and_then(txt).ok_or("ref")?.to_owned(),
                )),
                Some("extern") => Ok(Payload::Extern(
                    p.get("schemaRef")
                        .and_then(txt)
                        .ok_or("schemaRef")?
                        .to_owned(),
                )),
                other => Err(format!("payload form {other:?}")),
            }
        };
        for f in list.iter().filter_map(obj) {
            let name = f
                .get("frameType")
                .and_then(txt)
                .ok_or("frameType")?
                .to_owned();
            if f.get("direction").and_then(txt) != Some("worker-to-host") {
                continue;
            }
            worker_frames.insert(name.clone());
            let payload = f.get("payload").ok_or("payload")?;
            let mut by = BTreeMap::new();
            match obj(payload)
                .and_then(|p| p.get("alternatives"))
                .and_then(obj)
            {
                Some(alts) => {
                    for (k, p) in alts {
                        by.insert(k.clone(), selection(p)?);
                    }
                }
                None => {
                    by.insert(String::new(), selection(payload)?);
                }
            }
            frames.insert(name, by);
        }
        // The commitment domains, by field (COMMIT-MAP).
        let mut domains = BTreeMap::new();
        let J::Array(rows) = path(&doc, &["commitmentMap", "rows"]).ok_or("commitmentMap")? else {
            return Err("commitmentMap".to_owned());
        };
        for r in rows.iter().filter_map(obj) {
            if r.get("protocol").and_then(txt) == Some("typescript-semantic")
                && let (Some(f), Some(d)) =
                    (r.get("field").and_then(txt), r.get("domain").and_then(txt))
            {
                domains.insert(f.to_owned(), d.to_owned());
            }
        }
        // The fact-plane registry (FP-CANDIDATE).
        let rel = parse_json(RELATION_REGISTRY).map_err(|e| format!("relation registry: {e}"))?;
        let mut registry = BTreeMap::new();
        let mut subject_kinds = BTreeMap::new();
        for (name, r) in
            obj(path(&rel, &["x-opensip-relation-registry", "relations"]).ok_or("relations")?)
                .ok_or("relations")?
        {
            let ladder = strs(obj(r).and_then(|r| r.get("ladder"))).ok_or("ladder")?;
            let schema_id = path(r, &["schemaId"])
                .and_then(txt)
                .ok_or("schemaId")?
                .to_owned();
            let version = match path(r, &["schemaVersion"]) {
                Some(J::Integer(i)) => u64::try_from(i.get()).map_err(|_| "schemaVersion")?,
                _ => return Err("schemaVersion".to_owned()),
            };
            let kind = path(r, &["subjectKind"])
                .and_then(txt)
                .ok_or("subjectKind")?;
            subject_kinds.insert(name.clone(), kind.to_owned());
            registry.insert(name.clone(), (ladder, schema_id, version));
        }
        // fact-plane.v1.json holds JSON numbers the canonical reader refuses
        // (floats); its `relationRegistry` member is read alone, over its exact
        // bytes within the pinned file.
        let plane = top_level_member(FACT_PLANE, "relationRegistry")
            .ok_or("fact plane: relationRegistry")?;
        let plane = parse_json(plane).map_err(|e| format!("fact plane: {e}"))?;
        let mut layers = BTreeMap::new();
        for (name, r) in
            obj(path(&plane, &["relations"]).ok_or("relationRegistry")?).ok_or("relations")?
        {
            layers.insert(
                name.clone(),
                path(r, &["layer"]).and_then(txt).ok_or("layer")?.to_owned(),
            );
        }
        // The handshake law: the identity tokens (TypeScriptCapabilitiesV2's
        // `contains`) and the descriptor fields A2 names.
        let hs = parse_json(HANDSHAKE).map_err(|e| format!("handshake: {e}"))?;
        let J::Array(all_of) =
            path(&hs, &["$defs", "TypeScriptCapabilitiesV2", "allOf"]).ok_or("capabilities")?
        else {
            return Err("capabilities".to_owned());
        };
        let identity_tokens = all_of
            .iter()
            .map(|c| {
                path(c, &["contains", "const"])
                    .and_then(txt)
                    .map(str::to_owned)
            })
            .collect::<Option<Vec<_>>>()
            .ok_or("identity tokens")?;
        let binding = path(&hs, &["x-opensip-wire-law", "typescriptDescriptorBinding"])
            .ok_or("descriptor binding")?;
        let provider_fields =
            strs(path(binding, &["providerDescriptorFields"])).ok_or("providerDescriptorFields")?;
        let runtime_fields =
            strs(path(binding, &["runtimeDescriptorFields"])).ok_or("runtimeDescriptorFields")?;
        let t2o = parse_json(T2O).map_err(|e| format!("T2O: {e}"))?;
        let cancel_phases = strs(path(
            &t2o,
            &["cancellationObservedPhase", "hostPhasesAtCancel"],
        ))
        .ok_or("hostPhasesAtCancel")?;
        let cancel_observed = path(&t2o, &["cancellationObservedPhase", "observedPhase"])
            .and_then(txt)
            .ok_or("observedPhase")?
            .to_owned();
        // LD-D2B3-2: the extern payloads whose array may exceed the JSON
        // reader's bound are admitted piecewise. Each such member schema must
        // be exactly an array of one item `$ref` with count bounds.
        let st = parse_json(STARTUP).map_err(|e| format!("startup: {e}"))?;
        let mut piecewise = BTreeMap::new();
        for (def, member) in [
            ("TypeScriptCoverageV2", "entries"),
            ("TypeScriptUnavailableV2", "coverage"),
            ("TypeScriptBudgetExhaustedV2", "coverage"),
        ] {
            let m = obj(path(&st, &["$defs", def, "properties", member]).ok_or(def)?).ok_or(def)?;
            if m.get("type").and_then(txt) != Some("array")
                || m.keys().any(|k| {
                    ![
                        "type",
                        "items",
                        "minItems",
                        "maxItems",
                        "x-opensip-order",
                        "description",
                    ]
                    .contains(&k.as_str())
                })
            {
                return Err(format!("{def}.{member}: not a plain item array"));
            }
            let item = m.get("items").and_then(obj).ok_or(def)?;
            if item.len() != 1 {
                return Err(format!("{def}.{member}: item schema"));
            }
            let item_ref = item.get("$ref").and_then(txt).ok_or(def)?.to_owned();
            let bound = |k: &str| match m.get(k) {
                Some(J::Integer(i)) => u64::try_from(i.get()).ok(),
                _ => None,
            };
            piecewise.insert(
                format!("{STARTUP_ID}#/$defs/{def}"),
                (
                    member.to_owned(),
                    item_ref,
                    bound("minItems"),
                    bound("maxItems"),
                ),
            );
        }
        let census = CensusLaw::load()?;
        Ok(Self {
            subject_kinds,
            census,
            carriers,
            frames,
            worker_frames,
            domains,
            registry,
            layers,
            identity_tokens,
            provider_fields,
            runtime_fields,
            cancel_phases,
            cancel_observed,
            piecewise,
        })
    }

    fn domain(&self, field: &str) -> Result<&str, Ts2Refusal> {
        self.domains
            .get(field)
            .map(String::as_str)
            .ok_or_else(|| Ts2Refusal::Context(format!("no commitmentMap row for {field}")))
    }
}

/// The TS2 receiver for one session.
pub struct Ts2Receiver<'t> {
    context: DispatchContext,
    law: Law,
    run: Run<'t>,
    sequence: Sequence,
    refused: bool,
    target_attribution: bool,
    /// `symbol-census-v1` negotiated (in the Hello's array, which the
    /// HelloAck must echo exactly).
    census: bool,
    cancel: Option<(Option<String>, Option<u64>)>,
    retained: Vec<ReceivedFrame>,
    stages: Vec<StageLive>,
}

/// The `sha256:` suffix of a universe id (UNIVERSE-NATIVE-IDENTITY).
fn suffix(id: &str) -> Option<&str> {
    id.strip_prefix("sha256:")
}
fn map_of(v: &Value) -> Option<&[(String, Value)]> {
    match v {
        Value::Map(f) => Some(f),
        _ => None,
    }
}
fn text_of<'v>(f: &'v [(String, Value)], name: &str) -> Option<&'v str> {
    match field(f, name)? {
        Value::Text(s) => Some(s),
        _ => None,
    }
}
fn u64_of(f: &[(String, Value)], name: &str) -> Option<u64> {
    match field(f, name)? {
        Value::Unsigned(n) => Some(*n),
        _ => None,
    }
}
fn array_of<'v>(f: &'v [(String, Value)], name: &str) -> &'v [Value] {
    match field(f, name) {
        Some(Value::Array(a)) => a,
        _ => &[],
    }
}

impl<'t> Ts2Receiver<'t> {
    /// A receiver over `table` (T2O) and `context`. The context must name
    /// exactly A2's descriptor fields, and requests a census only with
    /// `symbol-census-v1`.
    pub fn new(table: &'t Table, context: DispatchContext) -> Result<Self, Ts2Refusal> {
        if table.protocol() != Protocol::Ts2 {
            return Err(Ts2Refusal::Context("not the TS2 table".to_owned()));
        }
        let law = Law::load().map_err(Ts2Refusal::Context)?;
        let keys = |d: &DescriptorFields| d.keys().cloned().collect::<BTreeSet<_>>();
        if keys(&context.provider_descriptor) != law.provider_fields.iter().cloned().collect()
            || keys(&context.runtime_descriptor) != law.runtime_fields.iter().cloned().collect()
        {
            return Err(Ts2Refusal::Context(
                "the descriptor fields are not A2's".to_owned(),
            ));
        }
        let census = context.capabilities.iter().any(|c| c == "symbol-census-v1");
        if !census && context.symbol_census.is_some() {
            return Err(Ts2Refusal::Context(
                "a census is requested without symbol-census-v1".to_owned(),
            ));
        }
        let target_attribution = context
            .capabilities
            .iter()
            .any(|c| c == "target-attribution-v2");
        let stages = vec![StageLive::default(); context.stages.len()];
        Ok(Self {
            context,
            law,
            run: table.start(),
            sequence: Sequence::default(),
            refused: false,
            target_attribution,
            census,
            cancel: None,
            retained: Vec::new(),
            stages,
        })
    }

    /// The table's phase.
    pub fn phase(&self) -> &str {
        self.run.phase()
    }

    /// The terminal the table recorded (`terminalKind`), once one is reached.
    pub fn terminal_kind(&self) -> Option<&str> {
        match self.run.field("terminalKind") {
            Some(Scalar::Text(kind)) => Some(kind),
            _ => None,
        }
    }

    /// Whether the table admits the host frame now (unit D2b-3b): a copy of
    /// the run is stepped with it, so no row is copied into code (LD-D2B-4).
    /// The sender writes a slot only when this holds.
    pub fn admits(&self, frame: &HostFrame) -> bool {
        if self.refused {
            return false;
        }
        let mut run = self.run.clone();
        run.step(&self.host_event(frame));
        run.phase() != "FAULT"
    }

    fn host_event(&self, frame: &HostFrame) -> Event {
        let mut event = Event::frame(match frame {
            HostFrame::Hello => "Hello",
            HostFrame::OpenUniverse => "OpenUniverse",
            HostFrame::SnapshotManifest => "SnapshotManifest",
            HostFrame::SnapshotFileChunk => "SnapshotFileChunk",
            HostFrame::SnapshotSeal => "SnapshotSeal",
            HostFrame::Analyze => "Analyze",
            HostFrame::Cancel { .. } => "Cancel",
        });
        if *frame == HostFrame::Analyze {
            event.stage_count = self.context.stages.len() as i64;
        }
        event
    }

    fn refuse(&mut self, r: Ts2Refusal) -> Ts2Refusal {
        self.refused = true;
        r
    }

    fn step(&mut self, event: &Event) -> Result<String, Ts2Refusal> {
        let trace = self.run.step(event);
        if self.run.phase() == "FAULT" {
            return Err(self.refuse(Ts2Refusal::Table(trace)));
        }
        Ok(trace)
    }

    /// Record a host frame the sender wrote, and step the table with it.
    pub fn sent(&mut self, frame: HostFrame) -> Result<String, Ts2Refusal> {
        if self.refused {
            return Err(Ts2Refusal::AfterRefusal);
        }
        let event = self.host_event(&frame);
        if let HostFrame::Cancel {
            execution_id,
            analysis_ordinal,
        } = frame
        {
            self.cancel = Some((execution_id, analysis_ordinal));
        }
        self.step(&event)
    }

    /// A process observation (LD-D2B-6), stepped through the table.
    pub fn process(&mut self, event: ProcessEvent) -> Result<String, Ts2Refusal> {
        if self.refused {
            return Err(Ts2Refusal::AfterRefusal);
        }
        self.step(&event.table_event())
    }

    /// Admit one received worker frame (steps 7 to 10), then convert it.
    pub fn receive(&mut self, frame: ReceivedFrame) -> Result<Admitted, Ts2Refusal> {
        if self.refused {
            return Err(Ts2Refusal::AfterRefusal);
        }
        match self.admit(&frame) {
            Ok((sequence, name, event, retain)) => {
                let trace = self.step(&event)?;
                let payload = self
                    .convert(&name, &frame)
                    .map_err(|e| self.refuse(Ts2Refusal::Admission(e)))?;
                let census = if name == "Complete" && self.census {
                    let v = map_of(frame.value())
                        .and_then(|env| field(env, "payload"))
                        .and_then(map_of)
                        .and_then(|f| field(f, "symbolCensus"))
                        .ok_or_else(|| {
                            self.refuse(Ts2Refusal::Admission("symbolCensus".to_owned()))
                        })?;
                    build::census(v).map_err(|e| self.refuse(Ts2Refusal::Admission(e)))?
                } else {
                    None
                };
                if retain {
                    self.retained.push(frame);
                }
                Ok(Admitted {
                    sequence,
                    trace,
                    payload,
                    census,
                })
            }
            Err(r) => Err(self.refuse(r)),
        }
    }

    /// Steps 7 to 9, returning the sequence, the frame type, the table
    /// event, and whether the frame's bytes are retained for a later
    /// commitment.
    fn admit(&mut self, frame: &ReceivedFrame) -> Result<(u64, String, Event, bool), Ts2Refusal> {
        use Ts2Refusal::{Admission, Envelope, Schema};
        // Step 7: the envelope, the carriers' Ts2FrameV2 (its payload apart).
        let Some(env) = map_of(frame.value()) else {
            return Err(Envelope("not a map".to_owned()));
        };
        let members = self.law.carriers.members("Ts2FrameV2");
        if env.len() != members.len() || members.iter().any(|(n, _)| field(env, n).is_none()) {
            return Err(Envelope("member set".to_owned()));
        }
        for (name, t) in &members {
            if name != "payload" {
                self.law
                    .carriers
                    .check(
                        t,
                        field(env, name).ok_or_else(|| Envelope(name.clone()))?,
                        name,
                    )
                    .map_err(Envelope)?;
            }
        }
        let name = text_of(env, "frameType")
            .ok_or_else(|| Envelope("frameType".to_owned()))?
            .to_owned();
        if !self.law.worker_frames.contains(&name) {
            return Err(Envelope(format!("{name} is not a worker-to-host frame")));
        }
        let sequence = u64_of(env, "sequence").ok_or_else(|| Envelope("sequence".to_owned()))?;
        if !self.sequence.accept(sequence) {
            return Err(Envelope(format!(
                "sequence {sequence}, expected {}",
                self.sequence.next()
            )));
        }
        let payload_node =
            child(frame, 0, env, "payload").ok_or_else(|| Envelope("payload node".to_owned()))?;
        let payload = field(env, "payload").ok_or_else(|| Envelope("payload".to_owned()))?;
        // Step 8: the closed schema of the selected payload.
        let selector = match name.as_str() {
            "FactBatch" => self.target_attribution.to_string(),
            "Unavailable" => self.run.phase().to_owned(),
            _ => String::new(),
        };
        let selected = self
            .law
            .frames
            .get(&name)
            .and_then(|by| by.get(&selector))
            .cloned();
        let Some(selected) = selected else {
            // No payload for this frame in this phase: the table refuses it
            // before any payload typing (the carriers' `host-phase` selector).
            return Ok((sequence, name.clone(), Event::frame(&name), false));
        };
        match &selected {
            // LD-D2B3C-2: with symbol-census-v1 negotiated, Complete is
            // TypeScriptCompleteV2 (the symbol-census law's negotiation; the
            // carriers predate FA-2). The inherited CompleteV1 then refuses at
            // this schema, and TypeScriptCompleteV2 without the token refuses
            // at the carriers' Ts2CompleteV1.
            _ if name == "Complete" && self.census => {
                census_complete(&self.law.census, payload).map_err(Schema)?
            }
            Payload::Record(r) => self.law.carriers.check_record(r, payload).map_err(Schema)?,
            Payload::Extern(r) => match self.law.piecewise.get(r) {
                Some((member, item, min, max)) => {
                    piecewise(r, payload, member, item, *min, *max).map_err(Schema)?
                }
                None => admit_extern(r, payload).map_err(Schema)?,
            },
        }
        // Step 9: the contextual admission, frame by frame.
        let f = map_of(payload).ok_or_else(|| Schema("payload".to_owned()))?;
        let mut event = Event::frame(&name);
        let mut retain = false;
        let stage = usize::try_from(match self.run.field("stageIndex") {
            Some(Scalar::Int(i)) => *i,
            _ => 0,
        })
        .unwrap_or(usize::MAX);
        match name.as_str() {
            "HelloAck" => {
                self.hello_ack(f).map_err(Admission)?;
                let caps: Vec<&str> = array_of(f, "capabilities")
                    .iter()
                    .filter_map(|v| {
                        if let Value::Text(s) = v {
                            Some(s.as_str())
                        } else {
                            None
                        }
                    })
                    .collect();
                event.identity_negotiated = self
                    .law
                    .identity_tokens
                    .iter()
                    .all(|t| caps.contains(&t.as_str()));
            }
            "UniverseAccepted" => {
                // ECHO-OPEN-UNIVERSE: each member is OpenUniverse's.
                for (m, want) in [
                    ("executionId", &self.context.execution_id),
                    ("snapshotId", &self.context.snapshot_id),
                    ("planId", &self.context.plan_id),
                    ("universeKey", &self.context.universe_key),
                ] {
                    if text_of(f, m) != Some(want.as_str()) {
                        return Err(Admission(format!(
                            "UniverseAccepted.{m} is not OpenUniverse's"
                        )));
                    }
                }
            }
            "SnapshotAccepted" => {
                // ACCEPTED-EQUALS-SEAL; ECHO-SNAPSHOT2; TS2-MANIFEST-DIGEST's echo.
                let ok = text_of(f, "snapshotId") == Some(&self.context.snapshot_id)
                    && text_of(f, "manifestSha256") == Some(&self.context.manifest_sha256)
                    && u64_of(f, "entryCount") == Some(self.context.entry_count)
                    && u64_of(f, "totalFileBytes") == Some(self.context.total_file_bytes)
                    && u64_of(f, "totalChunkCount") == Some(self.context.total_chunk_count);
                if !ok {
                    return Err(Admission("SnapshotAccepted is not the Seal".to_owned()));
                }
            }
            "NativeContextVerified" => {
                if text_of(f, "nativeContextId") != Some(&self.context.native_context_id)
                    || text_of(f, "recomputedNativeContextId")
                        != Some(&self.context.native_context_id)
                {
                    return Err(Admission(
                        "NativeContextVerified is not OpenUniverse's native context".to_owned(),
                    ));
                }
            }
            "FactBatch" => {
                self.fact_batch(frame, payload_node, f, stage)
                    .map_err(Admission)?;
                retain = true;
            }
            "Coverage" => {
                self.coverage(frame, payload_node, f, stage)
                    .map_err(Admission)?;
                retain = true;
            }
            "Complete" => self.complete(frame, payload_node, f).map_err(Admission)?,
            "Unavailable" => {
                if selector == "WAIT_NATIVE_CONTEXT_VERIFIED" {
                    self.pre_analyze_unavailable(f).map_err(Admission)?;
                    event.observations.push((
                        "unavailablePayload".to_owned(),
                        Scalar::Text("pre-analyze".to_owned()),
                    ));
                } else {
                    self.terminal_coverage(
                        frame,
                        payload_node,
                        f,
                        "coverage",
                        "Startup1TypeScriptUnavailableV2.coverageCommitment",
                        "provider-unavailable",
                    )
                    .map_err(Admission)?;
                    let want: Vec<&str> = self
                        .context
                        .stages
                        .iter()
                        .map(|s| s.expected_stage_id.as_str())
                        .collect();
                    let got: Vec<&str> = array_of(f, "affectedStageIds")
                        .iter()
                        .filter_map(|v| {
                            if let Value::Text(s) = v {
                                Some(s.as_str())
                            } else {
                                None
                            }
                        })
                        .collect();
                    if got != want {
                        return Err(Admission(
                            "affectedStageIds are not the requested stages".to_owned(),
                        ));
                    }
                    event.observations.push((
                        "unavailablePayload".to_owned(),
                        Scalar::Text("post-analyze".to_owned()),
                    ));
                }
            }
            "BudgetExhausted" => {
                self.terminal_coverage(
                    frame,
                    payload_node,
                    f,
                    "coverage",
                    "Startup1TypeScriptBudgetExhaustedV2.coverageCommitment",
                    "budget-exhausted",
                )
                .map_err(Admission)?;
                let trigger = text_of(f, "triggerStageId").unwrap_or_default();
                let binding = self
                    .context
                    .stages
                    .iter()
                    .find(|s| s.expected_stage_id == trigger)
                    .ok_or_else(|| {
                        Admission("triggerStageId is not a requested stage".to_owned())
                    })?;
                let dimension = text_of(f, "dimension").unwrap_or_default();
                let limit = *binding
                    .budget
                    .get(dimension)
                    .ok_or_else(|| Admission(format!("no budget for {dimension}")))?;
                if u64_of(f, "limit") != Some(limit) {
                    return Err(Admission("limit is not the requested budget".to_owned()));
                }
                if u64_of(f, "observed") != limit.checked_add(1) {
                    return Err(Admission("observed is not limit + 1".to_owned()));
                }
            }
            "Cancelled" => {
                // CANCELLED-ECHO, then TS2-OBSERVED-PHASE.
                let (execution, ordinal) = self
                    .cancel
                    .clone()
                    .ok_or_else(|| Admission("Cancelled without a Cancel".to_owned()))?;
                let got_execution = text_of(f, "executionId").map(str::to_owned);
                let got_ordinal = u64_of(f, "analysisOrdinal");
                if got_execution != execution || got_ordinal != ordinal {
                    return Err(Admission("Cancelled is not the Cancel's echo".to_owned()));
                }
                if let Some(Scalar::Text(at)) = self.run.field("cancelPhase")
                    && self.law.cancel_phases.contains(at)
                    && text_of(f, "observedPhase") != Some(self.law.cancel_observed.as_str())
                {
                    return Err(Admission(format!(
                        "observedPhase must be {}",
                        self.law.cancel_observed
                    )));
                }
            }
            other => return Err(Admission(format!("no admission for {other}"))),
        }
        Ok((sequence, name, event, retain))
    }

    /// HelloAck: LD-D2B-18's exact echo of the token array, the identity
    /// versions and the Hello's descriptor digests, and A2's descriptor
    /// fields.
    fn hello_ack(&self, f: &[(String, Value)]) -> Result<(), String> {
        let caps: Vec<Value> = self
            .context
            .capabilities
            .iter()
            .map(|c| Value::Text(c.clone()))
            .collect();
        if field(f, "capabilities") != Some(&Value::Array(caps)) {
            return Err("capabilities are not the Hello's array".to_owned());
        }
        let versions = Value::Map(
            self.context
                .identity_versions
                .iter()
                .map(|(k, v)| (k.clone(), Value::Unsigned(*v)))
                .collect(),
        );
        let got = field(f, "identityVersions").map(|v| match v {
            Value::Map(m) => {
                let mut m = m.clone();
                m.sort_by(|a, b| a.0.cmp(&b.0));
                Value::Map(m)
            }
            v => v.clone(),
        });
        if got.as_ref() != Some(&versions) {
            return Err("identityVersions are not the Hello's".to_owned());
        }
        if text_of(f, "providerDescriptorSha256")
            != Some(&self.context.expected_provider_descriptor_sha256)
            || text_of(f, "runtimeDescriptorSha256")
                != Some(&self.context.expected_runtime_descriptor_sha256)
        {
            return Err("descriptor digests are not the Hello's".to_owned());
        }
        for (name, want) in self
            .context
            .provider_descriptor
            .iter()
            .chain(&self.context.runtime_descriptor)
        {
            if field(f, name) != Some(want) {
                return Err(format!("{name} is not the verified descriptor's"));
            }
        }
        Ok(())
    }

    fn pre_analyze_unavailable(&self, f: &[(String, Value)]) -> Result<(), String> {
        for (m, want) in [
            ("executionId", &self.context.execution_id),
            ("snapshotId", &self.context.snapshot_id),
            ("planId", &self.context.plan_id),
            ("nativeContextId", &self.context.native_context_id),
        ] {
            if text_of(f, m) != Some(want.as_str()) {
                return Err(format!("Unavailable.{m} is not OpenUniverse's"));
            }
        }
        if text_of(f, "recomputedNativeContextId") == Some(&self.context.native_context_id) {
            return Err("recomputedNativeContextId equals nativeContextId".to_owned());
        }
        Ok(())
    }

    /// FactBatch: DISPATCH-STAGE-CORRELATION, COMMIT-TS2-FACT-BATCH (V1),
    /// FP-CANDIDATE, RELATION-PAYLOAD-CBOR, ANCHOR-WIRE-SPAN,
    /// ANCHOR-FACT-REF-REFUSED, ECHO-SNAPSHOT2 and OCCUPANCY-JOIN (V3).
    fn fact_batch(
        &mut self,
        frame: &ReceivedFrame,
        node: usize,
        f: &[(String, Value)],
        stage: usize,
    ) -> Result<(), String> {
        let binding = self.context.stages.get(stage).ok_or("no current stage")?;
        let live = &self.stages[stage];
        if text_of(f, "stageId") != Some(binding.expected_stage_id.as_str()) {
            return Err("stageId is not the current stage's".to_owned());
        }
        if u64_of(f, "batchIndex") != Some(live.batches) {
            return Err(format!("batchIndex is not {}", live.batches));
        }
        let member = if self.target_attribution {
            "candidates"
        } else {
            "facts"
        };
        let candidates = array_of(f, member);
        let first = candidates
            .first()
            .and_then(map_of)
            .and_then(|c| u64_of(c, "candidateOrdinal"));
        if first != Some(live.next_candidate) {
            return Err(format!(
                "the first candidateOrdinal is not {}",
                live.next_candidate
            ));
        }
        for c in candidates {
            self.candidate(map_of(c).ok_or("candidate")?, binding)?;
        }
        let list = child(frame, node, f, member).ok_or("candidates node")?;
        let nodes: Vec<usize> = frame.children(list).collect();
        if !self.target_attribution {
            let received: Vec<ReceivedBytes<'_>> =
                nodes.iter().filter_map(|n| frame.node(*n)).collect();
            let domain = self
                .law
                .domain("Ts2FactBatchV1.batchCommitment")
                .map_err(|e| format!("{e:?}"))?;
            if text_of(f, "batchCommitment") != Some(commit(domain, &received).as_str()) {
                return Err("batchCommitment".to_owned());
            }
        } else {
            // OCCUPANCY-JOIN.
            let companions = array_of(f, "occupancyCompanions");
            if companions.len() > candidates.len() {
                return Err("more occupancy companions than candidates".to_owned());
            }
            let by_ordinal: BTreeMap<u64, &str> = candidates
                .iter()
                .filter_map(map_of)
                .filter_map(|c| {
                    Some((
                        u64_of(c, "candidateOrdinal")?,
                        text_of(c, "targetUniverseId")?,
                    ))
                })
                .collect();
            for o in companions.iter().filter_map(map_of) {
                let ordinal = u64_of(o, "candidateOrdinal").ok_or("companion candidateOrdinal")?;
                match by_ordinal.get(&ordinal) {
                    Some(t) if text_of(o, "targetUniverseId") == Some(*t) => {}
                    Some(_) => {
                        return Err("companion targetUniverseId is not its candidate's".to_owned());
                    }
                    None => return Err("companion names no candidate of this batch".to_owned()),
                }
            }
        }
        let frame_index = self.retained.len();
        let live = &mut self.stages[stage];
        live.batches += 1;
        live.next_candidate = live
            .next_candidate
            .checked_add(candidates.len() as u64)
            .ok_or("candidateOrdinal overflow")?;
        live.facts
            .extend(nodes.into_iter().map(|n| (frame_index, n)));
        Ok(())
    }

    /// One candidate's wire law (FP-CANDIDATE), its payload
    /// (RELATION-PAYLOAD-CBOR) and its anchors.
    fn candidate(&self, c: &[(String, Value)], binding: &StageBinding) -> Result<(), String> {
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
        if field(c, "producerVersion") != self.context.provider_descriptor.get("providerBuildId") {
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
                    if text_of(a, "snapshotId") != Some(&self.context.snapshot_id) {
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

    /// The echo of each entry against its requested key (PER-KEY-SCOPE2,
    /// UNIVERSE-NATIVE-IDENTITY).
    /// Under a requested census, a `symbol`-kind key's two
    /// `subjectScopeCommitment` echoes are not checked here: the census
    /// decides them, and H checks them at clean settlement (X-FA2-D;
    /// LD-D2B3C-6). `census_decided` is that case.
    fn entry_echoes(entry: &Value, key: &RequestedKey, census_decided: bool) -> Result<(), String> {
        let e = map_of(entry).ok_or("entry")?;
        let k = field(e, "key").and_then(map_of).ok_or("entry key")?;
        let examined = field(e, "entry")
            .and_then(map_of)
            .and_then(|v| field(v, "examinedUniverse"))
            .and_then(map_of)
            .ok_or("examinedUniverse")?;
        let ok = text_of(k, "relation") == Some(&key.relation)
            && text_of(k, "resolution") == Some(&key.resolution)
            && (census_decided
                || text_of(k, "subjectScopeCommitment") == Some(&key.subject_scope_commitment))
            && text_of(k, "sourceUniverse") == suffix(&key.source_universe_id)
            && text_of(k, "targetUniverse") == suffix(&key.target_universe_id)
            && (census_decided
                || text_of(examined, "subjectScopeCommitment")
                    == Some(&key.subject_scope_commitment));
        if ok {
            Ok(())
        } else {
            Err("an entry is not its requested key's echo".to_owned())
        }
    }

    /// Coverage: the current stage, one entry per requested key in key
    /// order, and the stage-coverage commitment over the received entries.
    fn coverage(
        &mut self,
        frame: &ReceivedFrame,
        node: usize,
        f: &[(String, Value)],
        stage: usize,
    ) -> Result<(), String> {
        let binding = self.context.stages.get(stage).ok_or("no current stage")?;
        if text_of(f, "stageId") != Some(binding.expected_stage_id.as_str()) {
            return Err("stageId is not the current stage's".to_owned());
        }
        let entries = array_of(f, "entries");
        if entries.len() != binding.keys.len() {
            return Err("entry count is not the requested key count".to_owned());
        }
        for (e, k) in entries.iter().zip(&binding.keys) {
            let decided = self.context.symbol_census.is_some()
                && self.law.subject_kinds.get(&k.relation).map(String::as_str) == Some("symbol");
            Self::entry_echoes(e, k, decided)?;
        }
        let list = child(frame, node, f, "entries").ok_or("entries node")?;
        let nodes: Vec<usize> = frame.children(list).collect();
        let received: Vec<ReceivedBytes<'_>> =
            nodes.iter().filter_map(|n| frame.node(*n)).collect();
        let domain = self
            .law
            .domain("Startup1TypeScriptCoverageV2.coverageCommitment")
            .map_err(|e| format!("{e:?}"))?;
        if text_of(f, "coverageCommitment") != Some(commit(domain, &received).as_str()) {
            return Err("coverageCommitment".to_owned());
        }
        let frame_index = self.retained.len();
        self.stages[stage].coverage = nodes.into_iter().map(|n| (frame_index, n)).collect();
        Ok(())
    }

    /// The post-Analyze terminals: one unknown entry with the terminal's
    /// deficiency per requested key, stage-major, and the coverage-stream
    /// commitment over the received entries.
    fn terminal_coverage(
        &self,
        frame: &ReceivedFrame,
        node: usize,
        f: &[(String, Value)],
        member: &str,
        field_name: &str,
        deficiency: &str,
    ) -> Result<(), String> {
        let keys: Vec<&RequestedKey> = self.context.stages.iter().flat_map(|s| &s.keys).collect();
        let entries = array_of(f, member);
        if entries.len() != keys.len() {
            return Err("coverage is not one entry per requested key".to_owned());
        }
        for (e, k) in entries.iter().zip(keys) {
            // The terminals keep the requested commitment (NE §9.8).
            Self::entry_echoes(e, k, false)?;
            let view = map_of(e)
                .and_then(|e| field(e, "entry"))
                .and_then(map_of)
                .ok_or("entry")?;
            if text_of(view, "coverage") != Some("unknown")
                || text_of(view, "deficiency") != Some(deficiency)
            {
                return Err(format!(
                    "a terminal entry is not unknown with deficiency {deficiency}"
                ));
            }
        }
        let list = child(frame, node, f, member).ok_or("coverage node")?;
        let received: Vec<ReceivedBytes<'_>> =
            frame.children(list).filter_map(|n| frame.node(n)).collect();
        let domain = self.law.domain(field_name).map_err(|e| format!("{e:?}"))?;
        if text_of(f, "coverageCommitment") != Some(commit(domain, &received).as_str()) {
            return Err("coverageCommitment".to_owned());
        }
        Ok(())
    }

    /// The retained received bytes of `at`'s nodes.
    fn retained_bytes(&self, at: &[(usize, usize)]) -> Option<Vec<ReceivedBytes<'_>>> {
        at.iter()
            .map(|(f, n)| self.retained.get(*f)?.node(*n))
            .collect()
    }

    /// Complete: one result per requested stage in request order, its counts
    /// observed, and the four commitments recomputed over the retained
    /// received bytes (COMMIT-MAP).
    fn complete(
        &self,
        frame: &ReceivedFrame,
        node: usize,
        f: &[(String, Value)],
    ) -> Result<(), String> {
        if self.census {
            self.census_admission(frame, node, f)?;
        }
        let results = array_of(f, "stageResults");
        if results.len() != self.context.stages.len() {
            return Err("stageResults are not one per requested stage".to_owned());
        }
        let domain = |field: &str| {
            self.law
                .domain(field)
                .map(str::to_owned)
                .map_err(|e| format!("{e:?}"))
        };
        let (stage_facts, stage_coverage) = (
            domain("Ts2StageResultV1.factCommitment")?,
            domain("Ts2StageResultV1.coverageCommitment")?,
        );
        for ((r, binding), live) in results.iter().zip(&self.context.stages).zip(&self.stages) {
            let r = map_of(r).ok_or("stageResult")?;
            let facts = self.retained_bytes(&live.facts).ok_or("retained facts")?;
            let coverage = self
                .retained_bytes(&live.coverage)
                .ok_or("retained coverage")?;
            let ok = text_of(r, "stageId") == Some(&binding.expected_stage_id)
                && u64_of(r, "stageOrdinal") == Some(binding.stage_ordinal)
                && u64_of(r, "factBatchCount") == Some(live.batches)
                && u64_of(r, "factCount") == Some(live.facts.len() as u64)
                && u64_of(r, "coverageEntryCount") == Some(live.coverage.len() as u64);
            if !ok {
                return Err(format!(
                    "stage {}'s result is not as observed",
                    binding.expected_stage_id
                ));
            }
            if text_of(r, "factCommitment") != Some(commit(&stage_facts, &facts).as_str())
                || text_of(r, "coverageCommitment")
                    != Some(commit(&stage_coverage, &coverage).as_str())
            {
                return Err(format!("stage {}'s commitments", binding.expected_stage_id));
            }
        }
        let all_facts: Vec<(usize, usize)> = self
            .stages
            .iter()
            .flat_map(|s| s.facts.iter().copied())
            .collect();
        let all_coverage: Vec<(usize, usize)> = self
            .stages
            .iter()
            .flat_map(|s| s.coverage.iter().copied())
            .collect();
        let facts = self.retained_bytes(&all_facts).ok_or("retained facts")?;
        let coverage = self
            .retained_bytes(&all_coverage)
            .ok_or("retained coverage")?;
        if text_of(f, "factStreamCommitment")
            != Some(commit(&domain("Ts2CompleteV1.factStreamCommitment")?, &facts).as_str())
            || text_of(f, "coverageStreamCommitment")
                != Some(
                    commit(
                        &domain("Ts2CompleteV1.coverageStreamCommitment")?,
                        &coverage,
                    )
                    .as_str(),
                )
        {
            return Err("stream commitments".to_owned());
        }
        Ok(())
    }

    /// The census's contextual admission (LD-D2B-16; NE §9.8), each refusal
    /// under its law's internal key:
    /// - null exactly when the request's was;
    /// - a complete census: each row's path in `examinedPaths`, and its
    ///   received CBOR within [`CENSUS_MAX_BYTES`];
    /// - an over-bound census: refused when its counts are within every bound
    ///   (LD-D2B3C-5), and otherwise admitted as the typed event
    ///   [`Admitted::census`]. Its route, the subject-scope bound's
    ///   scope-limit route, is H's and that bound owner's, not D2b's.
    fn census_admission(
        &self,
        frame: &ReceivedFrame,
        node: usize,
        f: &[(String, Value)],
    ) -> Result<(), String> {
        let census = field(f, "symbolCensus").ok_or("symbolCensus")?;
        let requested = self.context.symbol_census.is_some();
        if (*census == Value::Null) == requested {
            return Err("native.symbol-census-null-mismatch: the census is null exactly when the request's was".to_owned());
        }
        let Some(c) = map_of(census) else {
            return Ok(());
        };
        match text_of(c, "state") {
            Some("complete") => {
                let paths: BTreeSet<&str> = array_of(c, "examinedPaths")
                    .iter()
                    .filter_map(|p| match p {
                        Value::Text(s) => Some(s.as_str()),
                        _ => None,
                    })
                    .collect();
                for row in array_of(c, "rows") {
                    let path = map_of(row)
                        .and_then(|r| text_of(r, "path"))
                        .ok_or("row path")?;
                    if !paths.contains(path) {
                        return Err(format!(
                            "native.symbol-census-path-not-examined: {path} is not an examined path"
                        ));
                    }
                }
                let at = child(frame, node, f, "symbolCensus").ok_or("census node")?;
                let bytes = frame.node(at).ok_or("census bytes")?.as_bytes().len() as u64;
                if bytes > CENSUS_MAX_BYTES {
                    return Err(format!(
                        "native.symbol-census-bound: a complete census of {bytes} bytes"
                    ));
                }
            }
            Some("over-bound") => {
                let (rows, paths) = (
                    u64_of(c, "rowCount").ok_or("rowCount")?,
                    u64_of(c, "examinedPathCount").ok_or("examinedPathCount")?,
                );
                let law = &self.law.census;
                if rows <= law.rows_max
                    && paths <= law.paths_max
                    && law.max_complete_bytes(rows, paths) <= CENSUS_MAX_BYTES
                {
                    return Err(format!(
                        "native.symbol-census-over-bound-within-bounds: {rows} rows and {paths} paths fit"
                    ));
                }
            }
            _ => return Err("census state".to_owned()),
        }
        Ok(())
    }

    /// Convert the admitted payload into the generated carrier.
    fn convert(&self, name: &str, frame: &ReceivedFrame) -> Result<Ts2FrameV2Payload, String> {
        let env = map_of(frame.value()).ok_or("envelope")?;
        let v = field(env, "payload").ok_or("payload")?;
        Ok(match name {
            "HelloAck" => Ts2FrameV2Payload::HelloAck(Box::new(build::hello_ack(v)?)),
            "UniverseAccepted" => {
                Ts2FrameV2Payload::UniverseAccepted(Box::new(build::universe_accepted(v)?))
            }
            "SnapshotAccepted" => {
                Ts2FrameV2Payload::SnapshotAccepted(Box::new(build::snapshot_accepted(v)?))
            }
            "NativeContextVerified" => Ts2FrameV2Payload::NativeContextVerified(Box::new(
                build::native_context_verified(v)?,
            )),
            "FactBatch" if self.target_attribution => {
                Ts2FrameV2Payload::FactBatch1(Box::new(build::fact_batch_v3(v)?))
            }
            "FactBatch" => Ts2FrameV2Payload::FactBatch0(Box::new(build::fact_batch_v1(v)?)),
            "Coverage" => Ts2FrameV2Payload::Coverage(Box::new(build::coverage(v)?)),
            "Unavailable" if field(map_of(v).ok_or("payload")?, "executionId").is_some() => {
                Ts2FrameV2Payload::Unavailable0(Box::new(build::pre_analyze_unavailable(v)?))
            }
            "Unavailable" => {
                Ts2FrameV2Payload::Unavailable1(Box::new(build::post_analyze_unavailable(v)?))
            }
            "BudgetExhausted" => {
                Ts2FrameV2Payload::BudgetExhausted(Box::new(build::budget_exhausted(v)?))
            }
            "Complete" => Ts2FrameV2Payload::Complete(Box::new(build::complete(v)?)),
            "Cancelled" => Ts2FrameV2Payload::Cancelled(Box::new(build::cancelled(v)?)),
            other => return Err(format!("no carrier for {other}")),
        })
    }
}

/// Every received-byte commitment goes through here (LD-D2B-3 item 5): its
/// parts are `ReceivedBytes`, which only a received frame makes. In tests
/// each part's address range is logged, so the provenance control can show
/// that every preimage lies inside a received payload.
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
/// The test-only provenance log: each commitment's domain and the (address, length) of each received part.
#[cfg(test)]
pub(crate) type Provenance = Vec<(String, Vec<(usize, usize)>)>;
#[cfg(test)]
thread_local! {
    pub(crate) static PROVENANCE: std::cell::RefCell<Provenance> = const { std::cell::RefCell::new(Vec::new()) };
}

/// The exact bytes of top-level member `key`'s value in the JSON object
/// `raw`: a scan that tracks string and nesting state, so a key inside a
/// string or a nested object never matches.
fn top_level_member<'r>(raw: &'r [u8], key: &str) -> Option<&'r [u8]> {
    let (mut depth, mut i) = (0usize, 0usize);
    let quoted = format!("\"{key}\"");
    while i < raw.len() {
        match raw[i] {
            b'"' => {
                let start = i;
                i += 1;
                while i < raw.len() && raw[i] != b'"' {
                    i += if raw[i] == b'\\' { 2 } else { 1 };
                }
                if depth == 1 && raw.get(start..=i) == Some(quoted.as_bytes()) {
                    let mut j = i + 1;
                    while raw.get(j).is_some_and(|b| b.is_ascii_whitespace()) {
                        j += 1;
                    }
                    if raw.get(j) == Some(&b':') {
                        return value_end(raw, j + 1);
                    }
                }
            }
            b'{' | b'[' => depth += 1,
            b'}' | b']' => depth = depth.checked_sub(1)?,
            _ => {}
        }
        i += 1;
    }
    None
}
/// The bytes of the one JSON value starting after `from` (whitespace first).
fn value_end(raw: &[u8], from: usize) -> Option<&[u8]> {
    let mut start = from;
    while raw.get(start).is_some_and(|b| b.is_ascii_whitespace()) {
        start += 1;
    }
    let (mut depth, mut i) = (0usize, start);
    while i < raw.len() {
        match raw[i] {
            b'"' => {
                i += 1;
                while i < raw.len() && raw[i] != b'"' {
                    i += if raw[i] == b'\\' { 2 } else { 1 };
                }
            }
            b'{' | b'[' => depth += 1,
            b'}' | b']' => {
                depth = depth.checked_sub(1)?;
                if depth == 0 {
                    return raw.get(start..=i);
                }
            }
            _ => {}
        }
        i += 1;
    }
    None
}

/// The node of map member `name`, where the map is node `node` with fields
/// `fields` in received order.
fn child(
    frame: &ReceivedFrame,
    node: usize,
    fields: &[(String, Value)],
    name: &str,
) -> Option<usize> {
    let at = fields.iter().position(|(k, _)| k == name)?;
    frame.children(node).nth(at)
}

fn contains_bytes(v: &Value) -> bool {
    match v {
        Value::Bytes(_) => true,
        Value::Array(a) => a.iter().any(contains_bytes),
        Value::Map(m) => m.iter().any(|(_, x)| contains_bytes(x)),
        _ => false,
    }
}

/// LD-D2B3-2: admit an extern payload whose array member may exceed the
/// JSON reader's bound piecewise. The wrapper is admitted with the array
/// reduced to its first item (so every other member, and the item type
/// once, are checked by the schema itself); every item is admitted by the
/// item schema; and the member's count bounds are checked as declared.
/// TypeScriptCompleteV2, admitted piecewise (LD-D2B3C-4, extending
/// LD-D2B3-2): a complete census may reach [`CENSUS_MAX_BYTES`] of CBOR,
/// beyond the JSON reader's bound. The payload is admitted with its census
/// elided to `null` (a member the schema admits). A complete census is
/// admitted with each array cut to its first item, then every examined path
/// and row by its own `$ref`, the arrays' counts against their `maxItems`,
/// and their `x-opensip-order` (canonical-set; by `nativeSubjectId`) by the
/// identity crate's order law over the whole array. A row's signature-token
/// array is also checked piecewise: JSON escaping can exceed the JSON byte
/// bound even while its received CBOR fits. The original row schema checks
/// the actual row with its first token. Remaining tokens take the exact
/// source-checked string/minLength=0/maxLength scalar leaf, and the original
/// count is checked against its pinned maxItems. No nested schema entrypoint
/// is selected; every field and constraint is checked before the table.
/// An over-bound census is admitted whole.
fn census_complete(law: &CensusLaw, payload: &Value) -> Result<(), String> {
    let complete = format!("{CENSUS_ID}#/$defs/TypeScriptCompleteV2");
    let Value::Map(fields) = payload else {
        return Err(format!("{complete}: not a map"));
    };
    let census = field(fields, "symbolCensus")
        .ok_or("native.symbol-census-token-without-payload: no symbolCensus")?;
    let elided = Value::Map(
        fields
            .iter()
            .map(|(k, v)| {
                (
                    k.clone(),
                    if k == "symbolCensus" {
                        Value::Null
                    } else {
                        v.clone()
                    },
                )
            })
            .collect(),
    );
    admit_extern(&complete, &elided)?;
    let Value::Map(c) = census else {
        return if *census == Value::Null {
            Ok(())
        } else {
            Err("symbolCensus: not a census".to_owned())
        };
    };
    match field(c, "state") {
        Some(Value::Text(s)) if s == "over-bound" => admit_extern(
            &format!("{CENSUS_ID}#/$defs/OverBoundSymbolCensusV1"),
            census,
        ),
        Some(Value::Text(s)) if s == "complete" => {
            let arrays = [
                (
                    "examinedPaths",
                    &law.path_ref,
                    law.paths_max,
                    &law.paths_order,
                ),
                ("rows", &law.row_ref, law.rows_max, &law.rows_order),
            ];
            let cut = Value::Map(
                c.iter()
                    .map(|(k, v)| match (arrays.iter().any(|(m, ..)| m == k), v) {
                        (true, Value::Array(items)) => {
                            let sample = items
                                .iter()
                                .take(1)
                                .map(|item| {
                                    if k == "rows" {
                                        census_row_sample(item)
                                    } else {
                                        item.clone()
                                    }
                                })
                                .collect();
                            (k.clone(), Value::Array(sample))
                        }
                        _ => (k.clone(), v.clone()),
                    })
                    .collect(),
            );
            admit_extern(&format!("{CENSUS_ID}#/$defs/CompleteSymbolCensusV1"), &cut)?;
            for (member, item_ref, max, order) in arrays {
                let Some(Value::Array(items)) = field(c, member) else {
                    return Err(format!("symbolCensus.{member}"));
                };
                if items.len() as u64 > max {
                    return Err(format!("native.symbol-census-bound: {member} over {max}"));
                }
                let mut json = Vec::with_capacity(items.len());
                for item in items {
                    if member == "rows" {
                        census_row(law, item)?;
                    } else {
                        admit_extern(item_ref, item)?;
                    }
                    json.push(carrier::to_json(item)?);
                }
                order
                    .verify(&json)
                    .map_err(|e| format!("native.symbol-census-row-order: {member}: {e}"))?;
            }
            Ok(())
        }
        _ => Err("symbolCensus: state".to_owned()),
    }
}

/// Keep every actual row field; shorten only an array-valued signatureTokens
/// to its first item. Invalid types remain invalid for the original schema.
fn census_row_sample(row: &Value) -> Value {
    let Value::Map(fields) = row else {
        return row.clone();
    };
    Value::Map(
        fields
            .iter()
            .map(|(key, value)| {
                let sample = match (key.as_str(), value) {
                    ("signatureTokens", Value::Array(tokens)) => {
                        Value::Array(tokens.iter().take(1).cloned().collect())
                    }
                    _ => value.clone(),
                };
                (key.clone(), sample)
            })
            .collect(),
    )
}

/// All actual non-token fields and the first token take the original row
/// schema. Law::load checks that every token leaf is exactly a string of
/// 0..=token_scalars Unicode scalars; later leaves are checked directly to
/// avoid repeating row-metadata serialization up to 256 times. Repeats and
/// supplied order stay intact. The original row is retained for ordering,
/// received-byte bounds, generated typing and H; no projection is forwarded.
fn census_row(law: &CensusLaw, row: &Value) -> Result<(), String> {
    let tokens = map_of(row)
        .and_then(|fields| field(fields, "signatureTokens"))
        .and_then(|value| match value {
            Value::Array(tokens) => Some(tokens),
            _ => None,
        })
        .ok_or("symbolCensus row.signatureTokens: not an array")?;
    if tokens.len() as u64 > law.tokens_max {
        return Err(format!(
            "native.symbol-census-bound: signatureTokens over {}",
            law.tokens_max
        ));
    }
    let sample = census_row_sample(row);
    admit_extern(&law.row_ref, &sample)?;
    for token in tokens.iter().skip(1) {
        match token {
            Value::Text(text) if text.chars().count() as u64 <= law.token_scalars => {}
            _ => return Err("symbolCensus signatureTokens item violates its schema".to_owned()),
        }
    }
    Ok(())
}

fn piecewise(
    schema_ref: &str,
    payload: &Value,
    member: &str,
    item_ref: &str,
    min: Option<u64>,
    max: Option<u64>,
) -> Result<(), String> {
    let Value::Map(fields) = payload else {
        return Err(format!("{schema_ref}: not a map"));
    };
    let Some(Value::Array(items)) = field(fields, member) else {
        return Err(format!("{schema_ref}: {member}"));
    };
    let n = items.len() as u64;
    if min.is_some_and(|m| n < m) || max.is_some_and(|m| n > m) {
        return Err(format!("{schema_ref}: {member} item count"));
    }
    let reduced = Value::Map(
        fields
            .iter()
            .map(|(k, v)| {
                if k == member {
                    (
                        k.clone(),
                        Value::Array(items.iter().take(1).cloned().collect()),
                    )
                } else {
                    (k.clone(), v.clone())
                }
            })
            .collect(),
    );
    admit_extern(schema_ref, &reduced)?;
    for item in items {
        admit_extern(item_ref, item)?;
    }
    Ok(())
}

#[cfg(test)]
#[path = "ts2_tests.rs"]
mod tests;
