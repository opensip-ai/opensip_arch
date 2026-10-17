//! M3-D r5 item 10 (unit D2b-3b; D2b plan r3 as amendments A1 and A2 amend
//! it): the TS2 codec's send side.
//! - **The host payload builders,** one per host frame family (DLV's
//!   `closedHostToWorkerFrames`: Hello, OpenUniverse, SnapshotManifest,
//!   SnapshotFileChunk, SnapshotSeal, Analyze and Cancel). Each builds its
//!   payload from the admitted Plan's values ([`Ts2Plan`]) and checks it
//!   against its closed schema: the carriers' record, or the product schema
//!   an extern frame names. So a host invariant refuses before spawn
//!   (section 3's "builder" rows).
//! - **LD-D2B-9's schedule constructor** (REQUEST-WIRE-ACCOUNTING): the
//!   canonical host send schedule. Every slot is measured as its exact
//!   envelope payload, with the greedy chunking, the entry bound, the frame
//!   bound and the one reserved maximal Cancel. C4 calls it at Plan time and
//!   owns the refusal.
//! - **The HOST-SEND-SCHEDULE sender:** it emits exactly the planned slots.
//!   Each frame is realized independently of the planner and compared with
//!   its slot before it becomes sent state. At most one Cancel is sent, under
//!   LD-D2B-7's law.
//!
//! The parameters each part implements are read from the carriers and
//! checked as implemented, so a changed law refuses rather than being
//! applied loosely.
use super::super::cbor::{self, Value};
use super::super::{
    FRAME_PREFIX_BYTES, MAX_FRAME_PAYLOAD_BYTES, built_commitment, manifest_digest, write_frame,
};
use super::carrier::{admit_extern, field};
use super::{HANDSHAKE, HostFrame, Law, Payload, RequestedKey, obj, path, strs, txt};
use opensip_identity::{
    JsonValue as J, RawSha256, digest_hex, hash_canonical_value, parse_json, raw_sha256,
};
use std::collections::BTreeMap;

/// The identity domain of a TypeScript semantic universe (startup-v1
/// `universeIdentity`, `native.semantic-universe.<language>.v2`;
/// identity-schemas.v3 `native-semantic-universe` row).
const UNIVERSE_DOMAIN: &str = "native.semantic-universe.typescript.v2";
/// The only Cancel reason the host sends (LD-D2B-7; HOST-SEND-SCHEDULE).
const CANCEL_REASON: &str = "user-interrupt";

/// One snapshot entry of C1's sealed snapshot inventory, in manifest order
/// (DLV `SnapshotEntryV1`; the carriers' `Ts2SnapshotEntryV1`).
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum SnapshotEntry {
    File {
        path: String,
        byte_length: u64,
        content_sha256: String,
    },
    Symlink {
        path: String,
        link_target: String,
    },
}

/// A selected stage's budget, as the admitted C-2 stage states it (DLV
/// `budgetProjection.admittedC2InputDomain`).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum StageBudget {
    Absent,
    WorkUnits(u64),
}

/// One selected stage, in the verified ExecutionPlan's logical order (DLV
/// `stageRequestProjection.selectedInput`).
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct StagePlan {
    pub stage_id: String,
    /// `None` when the C-2 stage has no `dependsOn`.
    pub depends_on: Option<Vec<String>>,
    pub relations: Vec<String>,
    pub budget: StageBudget,
    /// The requested keys in wire order, each with its per-key scope2
    /// commitment, minted by the Plan side (PER-KEY-SCOPE2).
    pub keys: Vec<RequestedKey>,
}

/// The admitted Plan's values for one TS2 worker (C4's, with no producer
/// yet): every input the host frames carry.
#[derive(Debug, Clone, PartialEq)]
pub struct Ts2Plan {
    pub host_build_id: String,
    pub expected_provider_descriptor_sha256: String,
    pub expected_runtime_descriptor_sha256: String,
    /// The selected signed capability row's tokens, as the Hello carries them
    /// (handshake-v1 `TypeScriptHelloV2.expectedCapabilities`; LD-D2B-18).
    pub capabilities: Vec<String>,
    /// The verified `providerBuildId`: every key's `producerVersion` (DLV
    /// `CoverageKeyV1.producerVersion`).
    pub provider_build_id: String,
    pub execution_id: String,
    pub snapshot_id: String,
    pub plan_id: String,
    pub plan_intent_commitment: String,
    /// The selected `TypeScriptSemanticUniverseV2`.
    pub universe: J,
    pub entries: Vec<SnapshotEntry>,
    pub stages: Vec<StagePlan>,
    /// The signed TypeScript provider budget profile's budget, by wire
    /// dimension: an absent stage budget's output (DLV `budgetProjection.absent`).
    pub default_budget: BTreeMap<String, u64>,
}

/// Why the Plan's request cannot be scheduled. Both refuse before spawn.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum PlanRefusal {
    /// A built payload fails its closed schema, or a value is not the law's:
    /// a host invariant.
    HostInvariant(String),
    /// REQUEST-WIRE-ACCOUNTING: the request does not fit under the canonical
    /// host send schedule. `route` is the carriers' route key; `faults` say
    /// which bound.
    ExceedsWireLimit { route: String, faults: Vec<String> },
}

/// Why the sender refused a frame before writing it (HOST-SEND-SCHEDULE's
/// `SENDER_DIVERGENCE`), or why the sealed snapshot could not supply it.
/// Each is the host's own failure: nothing is written, and nothing follows.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum SendRefusal {
    Divergence(String),
    Source(String),
    /// A frame after a refusal.
    AfterRefusal,
}

/// The sealed snapshot's bytes, read at send time (C1's custody; no producer
/// here). It returns exactly `length` bytes of `path` from `offset`, or fails.
pub trait SnapshotSource {
    fn read(&mut self, path: &str, offset: u64, length: usize) -> std::io::Result<Vec<u8>>;
}

/// A host frame type in the schedule.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SlotFrame {
    Hello,
    OpenUniverse,
    SnapshotManifest,
    SnapshotFileChunk,
    SnapshotSeal,
    Analyze,
}
impl SlotFrame {
    pub fn name(self) -> &'static str {
        match self {
            Self::Hello => "Hello",
            Self::OpenUniverse => "OpenUniverse",
            Self::SnapshotManifest => "SnapshotManifest",
            Self::SnapshotFileChunk => "SnapshotFileChunk",
            Self::SnapshotSeal => "SnapshotSeal",
            Self::Analyze => "Analyze",
        }
    }
    fn host_frame(self) -> HostFrame {
        match self {
            Self::Hello => HostFrame::Hello,
            Self::OpenUniverse => HostFrame::OpenUniverse,
            Self::SnapshotManifest => HostFrame::SnapshotManifest,
            Self::SnapshotFileChunk => HostFrame::SnapshotFileChunk,
            Self::SnapshotSeal => HostFrame::SnapshotSeal,
            Self::Analyze => HostFrame::Analyze,
        }
    }
}

/// A chunk slot's coordinates: its entry, `chunkIndex`, `byteOffset` and
/// byte length.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ChunkCoordinates {
    pub path: String,
    pub chunk_index: u64,
    pub byte_offset: u64,
    pub byte_length: u64,
}

/// One planned slot, with every member of HOST-SEND-SCHEDULE's `slotBinding`.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Slot {
    pub sequence: u64,
    pub frame: SlotFrame,
    pub chunk: Option<ChunkCoordinates>,
    pub total_chunk_count: Option<u64>,
    /// The exact envelope payload length (`lengthScope: envelope-payload`;
    /// the 40-byte prefix is excluded).
    pub payload_bytes: u64,
    /// SHA-256 of the planned payload's deterministic CBOR; for a chunk, of
    /// the payload without its `bytes` member.
    pub payload_sha256: [u8; 32],
    /// On an entry's last chunk slot: the entry's `contentSha256`, checked
    /// over the bytes actually sent.
    pub entry_content_sha256: Option<String>,
}

/// The immutable canonical host send schedule (REQUEST-WIRE-ACCOUNTING).
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Ts2Schedule {
    slots: Vec<Slot>,
    /// The reserved maximal Cancel's envelope payload length.
    cancel_reserve_bytes: u64,
}
impl Ts2Schedule {
    pub fn slots(&self) -> &[Slot] {
        &self.slots
    }
    pub fn cancel_reserve_bytes(&self) -> u64 {
        self.cancel_reserve_bytes
    }
}

/// The send side's law, read once and checked as implemented.
struct SendLaw {
    law: Law,
    /// Each host frame's payload selection (the carriers' `frames`).
    payloads: BTreeMap<String, Payload>,
    /// The envelope's `protocolMajor` constant (`Ts2FrameV2`).
    major: u64,
    /// `TypeScriptProtocolLimitsV1`'s ten constants, in member order.
    limits: Vec<(String, u64)>,
    /// `IdentityVersionsV1`'s constants.
    identity_versions: Vec<(String, u64)>,
    max_chunk: u64,
    max_entries: u64,
    frame_limit: u64,
    route: String,
}

fn admission_params<'j>(doc: &'j J, id: &str) -> Option<&'j BTreeMap<String, J>> {
    let J::Array(rows) = path(doc, &["admission"])? else {
        return None;
    };
    rows.iter()
        .filter_map(obj)
        .find(|r| r.get("id").and_then(txt) == Some(id))
        .and_then(|r| r.get("params"))
        .and_then(obj)
}

/// A schema's constant members, in its `required` order.
fn constants(schema: &J, def: &str) -> Result<Vec<(String, u64)>, String> {
    let d = path(schema, &["$defs", def]).ok_or(def)?;
    let names = strs(obj(d).and_then(|d| d.get("required"))).ok_or(def)?;
    names
        .into_iter()
        .map(|n| {
            let value = match path(d, &["properties", &n, "const"]) {
                Some(J::Integer(i)) => u64::try_from(i.get()).map_err(|_| format!("{def}.{n}"))?,
                _ => return Err(format!("{def}.{n} is not a constant")),
            };
            Ok((n, value))
        })
        .collect()
}

impl SendLaw {
    fn load() -> Result<Self, String> {
        let law = Law::load()?;
        let doc = parse_json(super::carrier::CARRIERS).map_err(|e| format!("carriers: {e}"))?;
        // REQUEST-WIRE-ACCOUNTING's parameters, as implemented here.
        let p =
            admission_params(&doc, "REQUEST-WIRE-ACCOUNTING").ok_or("REQUEST-WIRE-ACCOUNTING")?;
        let is = |k: &str, want: &J| p.get(k) == Some(want);
        let text = |s: &str| J::String(s.to_owned());
        if !(is("lengthScope", &text("envelope-payload"))
            && is("prefixIncluded", &J::Bool(false))
            && is("chunking", &text("greedy-max-chunk"))
            && is("schedule", &text("canonical-greedy"))
            && is("reserveCancel", &J::Bool(true))
            && path(&J::Object(p.clone()), &["entryBounds", "SnapshotManifest"])
                == Some(&text("maxSnapshotEntries"))
            && strs(p.get("totalsApplyTo"))
                .is_some_and(|t| !t.iter().any(|x| x == "typescript-semantic")))
        {
            return Err(
                "REQUEST-WIRE-ACCOUNTING's parameters are not those implemented".to_owned(),
            );
        }
        let route = path(&J::Object(p.clone()), &["route", "routeKey"])
            .and_then(txt)
            .ok_or("REQUEST-WIRE-ACCOUNTING route")?
            .to_owned();
        // HOST-SEND-SCHEDULE's parameters.
        let h = admission_params(&doc, "HOST-SEND-SCHEDULE").ok_or("HOST-SEND-SCHEDULE")?;
        let binding = [
            "sequence",
            "frameType",
            "entry",
            "chunkIndex",
            "byteOffset",
            "byteLength",
            "totalChunkCount",
            "payloadBytes",
            "payloadSha256",
            "entryContentSha256",
        ];
        if h.get("planConsumption") != Some(&text("exact-slot-sequence"))
            || path(&J::Object(h.clone()), &["cancel", "maxCount"]) != Some(&text("1"))
            || strs(h.get("slotBinding")).is_none_or(|b| b != binding)
        {
            return Err("HOST-SEND-SCHEDULE's parameters are not those implemented".to_owned());
        }
        // The host frames and their payloads; none is selected by a value.
        let J::Array(list) =
            path(&doc, &["protocols", "typescript-semantic", "frames"]).ok_or("frames")?
        else {
            return Err("frames".to_owned());
        };
        let mut payloads = BTreeMap::new();
        for f in list.iter().filter_map(obj) {
            if f.get("direction").and_then(txt) != Some("host-to-worker") {
                continue;
            }
            let name = f.get("frameType").and_then(txt).ok_or("frameType")?;
            let p = f.get("payload").and_then(obj).ok_or("payload")?;
            let selection = match p.get("t").and_then(txt) {
                Some("ref") => Payload::Record(p.get("ref").and_then(txt).ok_or("ref")?.to_owned()),
                Some("extern") => Payload::Extern(
                    p.get("schemaRef")
                        .and_then(txt)
                        .ok_or("schemaRef")?
                        .to_owned(),
                ),
                other => return Err(format!("{name}: payload form {other:?}")),
            };
            payloads.insert(name.to_owned(), selection);
        }
        let host: Vec<&str> = payloads.keys().map(String::as_str).collect();
        let mut seven = [
            "Hello",
            "OpenUniverse",
            "SnapshotManifest",
            "SnapshotFileChunk",
            "SnapshotSeal",
            "Analyze",
            "Cancel",
        ];
        seven.sort_unstable();
        if host != seven {
            return Err(format!(
                "the host frames are not the seven implemented: {host:?}"
            ));
        }
        let major = law
            .carriers
            .members("Ts2FrameV2")
            .into_iter()
            .find(|(n, _)| n == "protocolMajor")
            .and_then(|(_, t)| {
                obj(&t)
                    .and_then(|t| t.get("const"))
                    .and_then(txt)
                    .map(str::to_owned)
            })
            .and_then(|c| c.parse().ok())
            .ok_or("Ts2FrameV2.protocolMajor")?;
        let schema = parse_json(HANDSHAKE).map_err(|e| format!("handshake: {e}"))?;
        let limits = constants(&schema, "TypeScriptProtocolLimitsV1")?;
        let identity_versions = constants(&schema, "IdentityVersionsV1")?;
        let limit = |name: &str| {
            limits
                .iter()
                .find(|(n, _)| n == name)
                .map(|(_, v)| *v)
                .ok_or(format!("limit {name}"))
        };
        let frame_limit = limit("maxFramePayloadBytes")?;
        if frame_limit != MAX_FRAME_PAYLOAD_BYTES {
            return Err("maxFramePayloadBytes is not the reader's bound".to_owned());
        }
        Ok(Self {
            max_chunk: limit("maxSnapshotChunkBytes")?,
            max_entries: limit("maxSnapshotEntries")?,
            frame_limit,
            law,
            payloads,
            major,
            limits,
            identity_versions,
            route,
        })
    }

    fn domain(&self, field: &str) -> Result<&str, PlanRefusal> {
        self.law
            .domains
            .get(field)
            .map(String::as_str)
            .ok_or_else(|| PlanRefusal::HostInvariant(format!("no commitmentMap row for {field}")))
    }

    /// The closed check of a host frame's payload (section 3's builder).
    fn check(&self, frame: &str, payload: &Value) -> Result<(), String> {
        match self.payloads.get(frame).ok_or(frame)? {
            Payload::Record(r) => self.law.carriers.check_record(r, payload),
            Payload::Extern(r) => admit_extern(r, payload),
        }
    }

    /// The TS2 envelope (the carriers' `Ts2FrameV2`).
    fn envelope(&self, sequence: u64, frame: &str, payload: Value) -> Value {
        map(vec![
            ("protocolMajor", Value::Unsigned(self.major)),
            ("frameType", text(frame)),
            ("sequence", Value::Unsigned(sequence)),
            ("payload", payload),
        ])
    }
}

fn text(s: &str) -> Value {
    Value::Text(s.to_owned())
}
fn map(members: Vec<(&str, Value)>) -> Value {
    Value::Map(
        members
            .into_iter()
            .map(|(k, v)| (k.to_owned(), v))
            .collect(),
    )
}
fn texts(items: &[String]) -> Value {
    Value::Array(items.iter().map(|s| text(s)).collect())
}
fn invariant(e: impl std::fmt::Display) -> PlanRefusal {
    PlanRefusal::HostInvariant(e.to_string())
}

/// A JSON value as its CBOR form: integers stay exact, and JSON has no
/// float the identity parser admits (the carriers' `privateRepresentation`).
fn json_to_cbor(v: &J) -> Result<Value, String> {
    Ok(match v {
        J::Null => Value::Null,
        J::Bool(b) => Value::Bool(*b),
        J::Integer(i) => {
            let n = i.get();
            if n >= 0 {
                Value::Unsigned(u64::try_from(n).map_err(|_| "integer range")?)
            } else {
                Value::Negative(i64::try_from(n).map_err(|_| "integer range")?)
            }
        }
        J::String(s) => Value::Text(s.clone()),
        J::Array(a) => Value::Array(a.iter().map(json_to_cbor).collect::<Result<_, _>>()?),
        J::Object(o) => Value::Map(
            o.iter()
                .map(|(k, x)| Ok((k.clone(), json_to_cbor(x)?)))
                .collect::<Result<_, String>>()?,
        ),
    })
}

/// The length of a CBOR head with argument `n`.
fn head_len(major: u8, n: u64) -> u64 {
    let mut h = Vec::with_capacity(9);
    cbor::head(&mut h, major, n);
    h.len() as u64
}

/// A file entry's greedy chunk count (REQUEST-WIRE-ACCOUNTING `chunking`):
/// every chunk carries the maximum except the last, and a zero-length entry
/// has none.
fn chunk_count(length: u64, max_chunk: u64) -> u64 {
    length.div_ceil(max_chunk)
}

/// The built request: every host payload, each checked against its closed
/// schema, and the schedule planned from them.
pub struct Ts2Request {
    law: SendLaw,
    hello: Value,
    open_universe: Value,
    manifest: Value,
    seal: Value,
    analyze: Value,
    execution_id: String,
    snapshot_id: String,
    /// The `kind: file` entries in manifest order: path, length, contentSha256.
    files: Vec<(String, u64, String)>,
    schedule: Ts2Schedule,
}

impl std::fmt::Debug for Ts2Request {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("Ts2Request")
            .field("schedule", &self.schedule)
            .finish_non_exhaustive()
    }
}

impl Ts2Request {
    /// Build every host payload from the Plan's values, then the canonical
    /// send schedule (LD-D2B-9). C4 calls it at Plan time, after PlanId and
    /// every set admission and before spawn, and owns the refusal.
    pub fn build(plan: &Ts2Plan) -> Result<Self, PlanRefusal> {
        let law = SendLaw::load().map_err(invariant)?;
        // The entry bound, before the manifest is built (REQUEST-WIRE-ACCOUNTING
        // `entryBounds`): its refusal is the wire-limit route.
        if plan.entries.len() as u64 > law.max_entries {
            return Err(PlanRefusal::ExceedsWireLimit {
                route: law.route.clone(),
                faults: vec![format!(
                    "entries:SnapshotManifest {}>{}",
                    plan.entries.len(),
                    law.max_entries
                )],
            });
        }
        // LD-D2B-18's sender half: the Hello's array is the selection's, and
        // a payload variant inconsistent with it is a host invariant. The
        // census-bearing Analyze is D2b-3c's.
        if plan.capabilities.iter().any(|c| c == "symbol-census-v1") {
            return Err(invariant("symbol-census-v1 is D2b-3c's"));
        }
        let hello = map(vec![
            ("hostBuildId", text(&plan.host_build_id)),
            (
                "expectedProviderDescriptorSha256",
                text(&plan.expected_provider_descriptor_sha256),
            ),
            (
                "expectedRuntimeDescriptorSha256",
                text(&plan.expected_runtime_descriptor_sha256),
            ),
            (
                "limits",
                Value::Map(
                    law.limits
                        .iter()
                        .map(|(n, v)| (n.clone(), Value::Unsigned(*v)))
                        .collect(),
                ),
            ),
            ("expectedCapabilities", texts(&plan.capabilities)),
            (
                "identityVersions",
                Value::Map(
                    law.identity_versions
                        .iter()
                        .map(|(n, v)| (n.clone(), Value::Unsigned(*v)))
                        .collect(),
                ),
            ),
        ]);
        law.check("Hello", &hello).map_err(invariant)?;

        // OpenUniverse; universeKey is the host's own recomputation
        // (UNIVERSE-NATIVE-IDENTITY; startup-v1 `typescriptOpenUniverse`).
        let inputs = match &plan.universe {
            J::Object(o) => o.get("resolvedInputs"),
            _ => None,
        }
        .ok_or_else(|| invariant("the universe has no resolvedInputs"))?;
        let universe_key = format!(
            "sha256:{}",
            digest_hex(
                &hash_canonical_value(UNIVERSE_DOMAIN, inputs)
                    .map_err(|e| invariant(format!("{e:?}")))?
            )
        );
        let open_universe = map(vec![
            ("executionId", text(&plan.execution_id)),
            ("snapshotId", text(&plan.snapshot_id)),
            ("planId", text(&plan.plan_id)),
            ("planIntentCommitment", text(&plan.plan_intent_commitment)),
            ("providerId", text("typescript-semantic")),
            ("universe", json_to_cbor(&plan.universe).map_err(invariant)?),
            ("universeKey", text(&universe_key)),
        ]);
        law.check("OpenUniverse", &open_universe)
            .map_err(invariant)?;

        // SnapshotManifest, from C1's sealed inventory: every snapshotId echo
        // is OpenUniverse's (ECHO-SNAPSHOT2), and the digest is
        // TS2-MANIFEST-DIGEST's. The closed check holds TS2-SNAPSHOT-ORDER
        // and, at these host-sent path sites (and the chunks'),
        // TS2-LOGICAL-PATH-ADMISSION's lexical rule over each complete path
        // (PATH-SITE-SEGMENT-LAW).
        let mut files = Vec::new();
        let entries = Value::Array(
            plan.entries
                .iter()
                .map(|e| match e {
                    SnapshotEntry::File {
                        path,
                        byte_length,
                        content_sha256,
                    } => {
                        files.push((path.clone(), *byte_length, content_sha256.clone()));
                        map(vec![
                            ("path", text(path)),
                            ("kind", text("file")),
                            ("byteLength", Value::Unsigned(*byte_length)),
                            ("contentSha256", text(content_sha256)),
                            ("linkTarget", Value::Null),
                        ])
                    }
                    SnapshotEntry::Symlink { path, link_target } => map(vec![
                        ("path", text(path)),
                        ("kind", text("symlink")),
                        ("byteLength", Value::Unsigned(0)),
                        ("contentSha256", Value::Null),
                        ("linkTarget", text(link_target)),
                    ]),
                })
                .collect(),
        );
        let manifest_sha256 = manifest_digest(&entries);
        let manifest = map(vec![
            ("snapshotId", text(&plan.snapshot_id)),
            ("manifestSha256", text(&manifest_sha256)),
            ("entries", entries),
        ]);
        law.check("SnapshotManifest", &manifest)
            .map_err(invariant)?;

        // SnapshotSeal (SEAL-AGGREGATES), with checked sums.
        let mut total_bytes = 0u64;
        let mut total_chunks = 0u64;
        for (_, length, _) in &files {
            total_bytes = total_bytes
                .checked_add(*length)
                .ok_or_else(|| invariant("totalFileBytes overflows"))?;
            total_chunks = total_chunks
                .checked_add(chunk_count(*length, law.max_chunk))
                .ok_or_else(|| invariant("totalChunkCount overflows"))?;
        }
        let seal = map(vec![
            ("snapshotId", text(&plan.snapshot_id)),
            ("manifestSha256", text(&manifest_sha256)),
            ("entryCount", Value::Unsigned(plan.entries.len() as u64)),
            ("totalFileBytes", Value::Unsigned(total_bytes)),
            ("totalChunkCount", Value::Unsigned(total_chunks)),
        ]);
        law.check("SnapshotSeal", &seal).map_err(invariant)?;

        let analyze = Self::build_analyze(&law, plan, &universe_key, &files)?;
        law.check("Analyze", &analyze).map_err(invariant)?;

        let mut request = Self {
            law,
            hello,
            open_universe,
            manifest,
            seal,
            analyze,
            execution_id: plan.execution_id.clone(),
            snapshot_id: plan.snapshot_id.clone(),
            files,
            schedule: Ts2Schedule {
                slots: Vec::new(),
                cancel_reserve_bytes: 0,
            },
        };
        request.schedule = request.plan_schedule()?;
        Ok(request)
    }

    /// Analyze (DLV `multiStageAnalyze` and `stageRequestProjection`), echoing
    /// OpenUniverse's executionId, snapshotId, planId and universeKey
    /// (ECHO-OPEN-UNIVERSE): all and only the selected stages, in their order, with contiguous
    /// Analyze-relative ordinals (TS2-STAGE-PROJECTION;
    /// DISPATCH-STAGE-CORRELATION's builder side), each budget projected
    /// (TS2-BUDGET-PROJECTION) and each requested domain constructed
    /// (TS2-SUBJECT-SCOPE-RETAINED, TS2-DOMAIN-COMMITMENT, PER-KEY-SCOPE2).
    fn build_analyze(
        law: &SendLaw,
        plan: &Ts2Plan,
        universe_key: &str,
        files: &[(String, u64, String)],
    ) -> Result<Value, PlanRefusal> {
        // The subject scope: every file entry, in manifest order, which the
        // manifest's closed check makes strictly ascending by path bytes.
        let subjects = Value::Array(
            files
                .iter()
                .map(|(path, length, sha)| {
                    map(vec![
                        ("path", text(path)),
                        ("contentSha256", text(sha)),
                        ("byteLength", Value::Unsigned(*length)),
                    ])
                })
                .collect(),
        );
        let subject_scope = map(vec![
            ("scopeKind", text("all-snapshot-files")),
            ("snapshotId", text(&plan.snapshot_id)),
            ("subjectCount", Value::Unsigned(files.len() as u64)),
            (
                "subjectScopeCommitment",
                text(&built_commitment(
                    law.domain("Ts2SubjectScopeV1.subjectScopeCommitment")?,
                    &subjects,
                )),
            ),
        ]);
        let dimensions: Vec<String> = law
            .law
            .carriers
            .members("Ts2ProviderWorkBudgetV1")
            .into_iter()
            .map(|(n, _)| n)
            .collect();
        let mut stages = Vec::new();
        for (ordinal, stage) in plan.stages.iter().enumerate() {
            // The budget projection: absent takes the signed profile's six
            // values, work-units L gives L in every dimension, and the
            // projection emits 1..2^63-1 only (DLV `budgetProjection`; the
            // carriers' `Ts2ProviderWorkBudgetV1` note).
            let budget: Vec<(String, u64)> = match stage.budget {
                StageBudget::Absent => {
                    let keys: Vec<&String> = plan.default_budget.keys().collect();
                    let mut want: Vec<&String> = dimensions.iter().collect();
                    want.sort_unstable();
                    if keys != want {
                        return Err(invariant(
                            "the default budget profile is not the six dimensions",
                        ));
                    }
                    dimensions
                        .iter()
                        .map(|d| (d.clone(), plan.default_budget[d]))
                        .collect()
                }
                StageBudget::WorkUnits(limit) => {
                    dimensions.iter().map(|d| (d.clone(), limit)).collect()
                }
            };
            if budget.iter().any(|(_, v)| *v == 0 || *v > i64::MAX as u64) {
                return Err(invariant(format!(
                    "{}: a budget outside 1..2^63-1",
                    stage.stage_id
                )));
            }
            let keys = Value::Array(
                stage
                    .keys
                    .iter()
                    .map(|k| {
                        map(vec![
                            ("relation", text(&k.relation)),
                            ("resolution", text(&k.resolution)),
                            ("sourceUniverseId", text(&k.source_universe_id)),
                            ("targetUniverseId", text(&k.target_universe_id)),
                            ("subjectScopeCommitment", text(&k.subject_scope_commitment)),
                            ("producer", text("typescript-semantic")),
                            ("producerVersion", text(&plan.provider_build_id)),
                            ("schemaVersion", Value::Unsigned(1)),
                        ])
                    })
                    .collect(),
            );
            let preimage = map(vec![
                ("subjectScope", subject_scope.clone()),
                ("keys", keys.clone()),
            ]);
            let domain_commitment = built_commitment(
                law.domain("Ts2RequestedCoverageDomainV1.domainCommitment")?,
                &preimage,
            );
            stages.push(map(vec![
                ("stageId", text(&stage.stage_id)),
                ("stageOrdinal", Value::Unsigned(ordinal as u64)),
                ("operator", text("semantic-provider")),
                ("providerId", text("typescript-semantic")),
                (
                    "dependsOn",
                    texts(stage.depends_on.as_deref().unwrap_or(&[])),
                ),
                ("relations", texts(&stage.relations)),
                (
                    "budget",
                    Value::Map(
                        budget
                            .into_iter()
                            .map(|(n, v)| (n, Value::Unsigned(v)))
                            .collect(),
                    ),
                ),
                (
                    "requestedCoverageDomain",
                    map(vec![
                        ("subjectScope", subject_scope.clone()),
                        ("keys", keys),
                        ("domainCommitment", text(&domain_commitment)),
                    ]),
                ),
            ]));
        }
        Ok(map(vec![
            ("analysisOrdinal", Value::Unsigned(0)),
            ("executionId", text(&plan.execution_id)),
            ("snapshotId", text(&plan.snapshot_id)),
            ("planId", text(&plan.plan_id)),
            ("universeKey", text(universe_key)),
            ("stageRequests", Value::Array(stages)),
        ]))
    }

    /// A chunk's payload without its `bytes` member.
    fn chunk_header(&self, path: &str, index: u64, offset: u64) -> Value {
        map(vec![
            ("snapshotId", text(&self.snapshot_id)),
            ("path", text(path)),
            ("chunkIndex", Value::Unsigned(index)),
            ("byteOffset", Value::Unsigned(offset)),
        ])
    }

    /// The reserved maximal Cancel: the echo of the execution and analysis.
    fn maximal_cancel(&self) -> Value {
        map(vec![
            ("executionId", text(&self.execution_id)),
            ("analysisOrdinal", Value::Unsigned(0)),
            ("reason", text(CANCEL_REASON)),
        ])
    }

    /// The canonical host send schedule (REQUEST-WIRE-ACCOUNTING): Hello,
    /// OpenUniverse, SnapshotManifest, its greedy chunks, SnapshotSeal and
    /// Analyze, plus exactly one reserved maximal Cancel. TS2 declares no
    /// request totals, so only the frame bound applies: no planned frame is
    /// over maxFramePayloadBytes (FRAME-LIMIT's builder side).
    fn plan_schedule(&self) -> Result<Ts2Schedule, PlanRefusal> {
        let law = &self.law;
        let mut slots = Vec::new();
        let mut faults = Vec::new();
        let mut sequence = 0u64;
        let fault = |frame: &str, sequence: u64, n: u64, faults: &mut Vec<String>| {
            if n > law.frame_limit {
                faults.push(format!(
                    "frame:{frame} seq{sequence}:{n}>{}",
                    law.frame_limit
                ));
            }
        };
        for (frame, payload) in [
            (SlotFrame::Hello, &self.hello),
            (SlotFrame::OpenUniverse, &self.open_universe),
            (SlotFrame::SnapshotManifest, &self.manifest),
        ] {
            let n =
                cbor::encode(&law.envelope(sequence, frame.name(), payload.clone())).len() as u64;
            fault(frame.name(), sequence, n, &mut faults);
            slots.push(Slot {
                sequence,
                frame,
                chunk: None,
                total_chunk_count: None,
                payload_bytes: n,
                payload_sha256: raw_sha256(&cbor::encode(payload)),
                entry_content_sha256: None,
            });
            sequence += 1;
        }
        // The chunks: sized in closed form, never materialized. The probe is
        // the chunk envelope with an empty byte string; a chunk of `n` bytes
        // replaces its 1-byte head with `n`'s head and adds `n` bytes.
        for (path, length, sha) in &self.files {
            let k = chunk_count(*length, law.max_chunk);
            for i in 0..k {
                let offset = i * law.max_chunk;
                let n = if i + 1 < k {
                    law.max_chunk
                } else {
                    length - offset
                };
                let header = self.chunk_header(path, i, offset);
                let Value::Map(mut members) = header.clone() else {
                    unreachable!("a chunk header is a map");
                };
                for (name, t) in law.law.carriers.members("Ts2SnapshotFileChunkV1") {
                    if name != "bytes" {
                        let v = field(&members, &name)
                            .ok_or_else(|| invariant(format!("chunk {name}")))?;
                        law.law.carriers.check(&t, v, &name).map_err(invariant)?;
                    }
                }
                members.push(("bytes".to_owned(), Value::Bytes(Vec::new())));
                let probe =
                    cbor::encode(&law.envelope(sequence, "SnapshotFileChunk", Value::Map(members)))
                        .len() as u64;
                let size = probe - 1 + head_len(2, n) + n;
                fault("SnapshotFileChunk", sequence, size, &mut faults);
                slots.push(Slot {
                    sequence,
                    frame: SlotFrame::SnapshotFileChunk,
                    chunk: Some(ChunkCoordinates {
                        path: path.clone(),
                        chunk_index: i,
                        byte_offset: offset,
                        byte_length: n,
                    }),
                    total_chunk_count: None,
                    payload_bytes: size,
                    payload_sha256: raw_sha256(&cbor::encode(&header)),
                    entry_content_sha256: (i + 1 == k).then(|| sha.clone()),
                });
                sequence += 1;
            }
        }
        let total = match field_of(&self.seal, "totalChunkCount") {
            Some(Value::Unsigned(n)) => *n,
            _ => return Err(invariant("seal totalChunkCount")),
        };
        for (frame, payload, count) in [
            (SlotFrame::SnapshotSeal, &self.seal, Some(total)),
            (SlotFrame::Analyze, &self.analyze, None),
        ] {
            let n =
                cbor::encode(&law.envelope(sequence, frame.name(), payload.clone())).len() as u64;
            fault(frame.name(), sequence, n, &mut faults);
            slots.push(Slot {
                sequence,
                frame,
                chunk: None,
                total_chunk_count: count,
                payload_bytes: n,
                payload_sha256: raw_sha256(&cbor::encode(payload)),
                entry_content_sha256: None,
            });
            sequence += 1;
        }
        // The reserved Cancel, at the last sequence a Cancel can take, so its
        // payload is maximal.
        let cancel = self.maximal_cancel();
        law.check("Cancel", &cancel).map_err(invariant)?;
        let cancel_reserve_bytes =
            cbor::encode(&law.envelope(sequence, "Cancel", cancel)).len() as u64;
        fault("Cancel", sequence, cancel_reserve_bytes, &mut faults);
        if !faults.is_empty() {
            return Err(PlanRefusal::ExceedsWireLimit {
                route: law.route.clone(),
                faults,
            });
        }
        Ok(Ts2Schedule {
            slots,
            cancel_reserve_bytes,
        })
    }

    pub fn schedule(&self) -> &Ts2Schedule {
        &self.schedule
    }
    /// The built Hello, as the HelloAck must echo it.
    pub fn hello(&self) -> &Value {
        &self.hello
    }
    pub fn open_universe(&self) -> &Value {
        &self.open_universe
    }
    pub fn manifest(&self) -> &Value {
        &self.manifest
    }
    pub fn seal(&self) -> &Value {
        &self.seal
    }
    pub fn analyze(&self) -> &Value {
        &self.analyze
    }
}

fn field_of<'v>(v: &'v Value, name: &str) -> Option<&'v Value> {
    match v {
        Value::Map(m) => field(m, name),
        _ => None,
    }
}

/// One frame the sender accepted: its wire bytes (the 40-byte prefix and
/// the payload) and the host frame the receiver records.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Sent {
    pub bytes: Vec<u8>,
    pub frame: HostFrame,
}

/// Where the sender's own realization is (independent of the planner's
/// slot walk).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Cursor {
    Hello,
    OpenUniverse,
    Manifest,
    Chunk {
        entry: usize,
        index: u64,
        offset: u64,
    },
    Seal,
    Analyze,
    Done,
}

/// The HOST-SEND-SCHEDULE sender for one session.
pub struct Ts2Sender {
    request: Ts2Request,
    slot: usize,
    sequence: u64,
    /// The correlation actually sent (CANCEL-NULLABILITY).
    sent_execution_id: Option<String>,
    sent_analysis_ordinal: Option<u64>,
    cancelled: bool,
    refused: bool,
    /// The digest of the current entry's bytes sent so far.
    entry_digest: Option<RawSha256>,
    cursor: Cursor,
    realized_chunks: u64,
}

impl std::fmt::Debug for Ts2Sender {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("Ts2Sender")
            .field("slot", &self.slot)
            .field("sequence", &self.sequence)
            .field("cancelled", &self.cancelled)
            .finish_non_exhaustive()
    }
}

fn divergence(reason: &str, detail: impl std::fmt::Display) -> SendRefusal {
    SendRefusal::Divergence(format!("SENDER_DIVERGENCE:{reason}: {detail}"))
}

impl Ts2Sender {
    /// A sender that consumes `request`'s immutable schedule.
    pub fn new(request: Ts2Request) -> Self {
        Self {
            request,
            slot: 0,
            sequence: 0,
            sent_execution_id: None,
            sent_analysis_ordinal: None,
            cancelled: false,
            refused: false,
            entry_digest: None,
            cursor: Cursor::Hello,
            realized_chunks: 0,
        }
    }

    pub fn request(&self) -> &Ts2Request {
        &self.request
    }
    /// The next planned slot, if any is left and the transcript is open.
    pub fn next_slot(&self) -> Option<&Slot> {
        if self.cancelled || self.refused {
            return None;
        }
        self.request.schedule.slots.get(self.slot)
    }
    /// Whether the Hello slot has been sent: a Cancel is lawful only after it.
    pub fn hello_sent(&self) -> bool {
        self.slot > 0
    }
    pub fn cancelled(&self) -> bool {
        self.cancelled
    }
    /// Every slot consumed, or ended by the Cancel.
    pub fn complete(&self) -> bool {
        self.cancelled || self.slot == self.request.schedule.slots.len()
    }

    fn refuse(&mut self, r: SendRefusal) -> SendRefusal {
        self.refused = true;
        r
    }

    /// Realize the next frame from the request, independently of the
    /// planner (the reference's `realize`): the greedy chunk walk over the
    /// file entries, each chunk's bytes read from the sealed snapshot.
    pub fn realize_next(
        &mut self,
        source: &mut dyn SnapshotSource,
    ) -> Result<(SlotFrame, Value), SendRefusal> {
        if self.refused {
            return Err(SendRefusal::AfterRefusal);
        }
        // Every failure ends the transcript before it is returned (Codex
        // D2B3B-R1-RF-1): a later call refuses, and the source is not read
        // again.
        match self.realize(source) {
            Ok(realized) => Ok(realized),
            Err(r) => Err(self.refuse(r)),
        }
    }

    fn realize(
        &mut self,
        source: &mut dyn SnapshotSource,
    ) -> Result<(SlotFrame, Value), SendRefusal> {
        let max = self.request.law.max_chunk;
        loop {
            let (frame, payload, next) = match self.cursor {
                Cursor::Hello => (
                    SlotFrame::Hello,
                    self.request.hello.clone(),
                    Cursor::OpenUniverse,
                ),
                Cursor::OpenUniverse => (
                    SlotFrame::OpenUniverse,
                    self.request.open_universe.clone(),
                    Cursor::Manifest,
                ),
                Cursor::Manifest => (
                    SlotFrame::SnapshotManifest,
                    self.request.manifest.clone(),
                    Cursor::Chunk {
                        entry: 0,
                        index: 0,
                        offset: 0,
                    },
                ),
                Cursor::Chunk {
                    entry,
                    index,
                    offset,
                } => {
                    let Some((path, length, _)) = self.request.files.get(entry) else {
                        self.cursor = Cursor::Seal;
                        continue;
                    };
                    if offset >= *length {
                        self.cursor = Cursor::Chunk {
                            entry: entry + 1,
                            index: 0,
                            offset: 0,
                        };
                        continue;
                    }
                    let n = max.min(length - offset);
                    let wanted = usize::try_from(n)
                        .map_err(|_| SendRefusal::Source("chunk length".to_owned()))?;
                    let path = path.clone();
                    let bytes = source
                        .read(&path, offset, wanted)
                        .map_err(|e| SendRefusal::Source(format!("{path}@{offset}: {e}")))?;
                    if bytes.len() != wanted {
                        return Err(self.refuse(SendRefusal::Source(format!(
                            "{path}@{offset}: {} bytes, not {wanted}",
                            bytes.len()
                        ))));
                    }
                    let Value::Map(mut members) = self.request.chunk_header(&path, index, offset)
                    else {
                        unreachable!("a chunk header is a map");
                    };
                    members.push(("bytes".to_owned(), Value::Bytes(bytes)));
                    self.realized_chunks += 1;
                    (
                        SlotFrame::SnapshotFileChunk,
                        Value::Map(members),
                        Cursor::Chunk {
                            entry,
                            index: index + 1,
                            offset: offset + n,
                        },
                    )
                }
                Cursor::Seal => {
                    // The seal over what this walk emitted (SEAL-AGGREGATES).
                    let Value::Map(mut members) = self.request.seal.clone() else {
                        unreachable!("the seal is a map");
                    };
                    for (k, v) in &mut members {
                        if k == "totalChunkCount" {
                            *v = Value::Unsigned(self.realized_chunks);
                        }
                    }
                    (
                        SlotFrame::SnapshotSeal,
                        Value::Map(members),
                        Cursor::Analyze,
                    )
                }
                Cursor::Analyze => (
                    SlotFrame::Analyze,
                    self.request.analyze.clone(),
                    Cursor::Done,
                ),
                Cursor::Done => {
                    return Err(divergence("frame-not-planned", "the schedule is consumed"));
                }
            };
            self.cursor = next;
            return Ok((frame, payload));
        }
    }

    /// Admit one host frame against its planned slot (HOST-SEND-SCHEDULE).
    /// Every slot member is compared before the frame becomes sent state;
    /// a divergence refuses, nothing is written, and nothing follows.
    pub fn admit(
        &mut self,
        frame: SlotFrame,
        sequence: u64,
        payload: Value,
    ) -> Result<Sent, SendRefusal> {
        if self.refused {
            return Err(SendRefusal::AfterRefusal);
        }
        match self.check_slot(frame, sequence, payload) {
            Ok(sent) => Ok(sent),
            Err(r) => Err(self.refuse(r)),
        }
    }

    fn check_slot(
        &mut self,
        frame: SlotFrame,
        sequence: u64,
        payload: Value,
    ) -> Result<Sent, SendRefusal> {
        if self.cancelled {
            return Err(divergence("frame-after-cancel", frame.name()));
        }
        if sequence != self.sequence {
            return Err(divergence(
                "sequence",
                format!("{sequence}!={}", self.sequence),
            ));
        }
        let law = &self.request.law;
        let slot = self
            .request
            .schedule
            .slots
            .get(self.slot)
            .ok_or_else(|| divergence("frame-not-planned", frame.name()))?
            .clone();
        if slot.frame != frame {
            return Err(divergence(
                "frame-type",
                format!("{}!={}", frame.name(), slot.frame.name()),
            ));
        }
        let Value::Map(members) = &payload else {
            return Err(divergence("payload", "not a map"));
        };
        let mut chunk_bytes = None;
        let digest_over = if let Some(c) = &slot.chunk {
            let bytes = match field(members, "bytes") {
                Some(Value::Bytes(b)) => b,
                _ => return Err(divergence("chunk-schedule", "no bytes")),
            };
            let at = (
                field(members, "path"),
                field(members, "chunkIndex"),
                field(members, "byteOffset"),
                bytes.len() as u64,
            );
            let want = (
                Some(&Value::Text(c.path.clone())),
                Some(&Value::Unsigned(c.chunk_index)),
                Some(&Value::Unsigned(c.byte_offset)),
                c.byte_length,
            );
            if at != want {
                return Err(divergence("chunk-schedule", format!("slot {}", self.slot)));
            }
            chunk_bytes = Some(bytes.clone());
            Value::Map(
                members
                    .iter()
                    .filter(|(k, _)| k != "bytes")
                    .cloned()
                    .collect(),
            )
        } else {
            payload.clone()
        };
        if let Some(count) = slot.total_chunk_count
            && field(members, "totalChunkCount") != Some(&Value::Unsigned(count))
        {
            return Err(divergence("seal-count", format!("slot {}", self.slot)));
        }
        // The builder's closed check holds for what is actually sent.
        law.check(frame.name(), &payload)
            .map_err(|e| divergence("payload-schema", e))?;
        let bytes = write_frame(&law.envelope(sequence, frame.name(), payload))
            .ok_or_else(|| divergence("frame-limit", "over maxFramePayloadBytes"))?;
        let n = (bytes.len() - FRAME_PREFIX_BYTES) as u64;
        if n != slot.payload_bytes {
            return Err(divergence(
                "payload-bytes",
                format!("slot {}: {n}!={}", self.slot, slot.payload_bytes),
            ));
        }
        if raw_sha256(&cbor::encode(&digest_over)) != slot.payload_sha256 {
            return Err(divergence("payload-digest", format!("slot {}", self.slot)));
        }
        // Defensive (HOST-SEND-SCHEDULE `defensiveBranches`): reachable only
        // for a plan consumed under other limits.
        if n > law.frame_limit {
            return Err(divergence("frame-limit", n));
        }
        // CHUNK-CUSTODY: the entry's bytes actually sent hash to its digest.
        if let (Some(c), Some(b)) = (&slot.chunk, chunk_bytes) {
            let digest = if c.chunk_index == 0 {
                RawSha256::new()
            } else {
                self.entry_digest
                    .take()
                    .ok_or_else(|| divergence("chunk-content", "no entry digest"))?
            };
            let digest = digest
                .update(&b)
                .map_err(|_| divergence("chunk-content", "digest length"))?;
            match &slot.entry_content_sha256 {
                Some(want) => {
                    if &digest_hex(&RawSha256::finish(digest)) != want {
                        return Err(divergence("chunk-content", format!("slot {}", self.slot)));
                    }
                }
                None => self.entry_digest = Some(digest),
            }
        }
        // Every check passed: the frame becomes sent state.
        match frame {
            SlotFrame::OpenUniverse => {
                self.sent_execution_id =
                    match field(members_of(&self.request.open_universe), "executionId") {
                        Some(Value::Text(s)) => Some(s.clone()),
                        _ => None,
                    }
            }
            SlotFrame::Analyze => {
                self.sent_analysis_ordinal =
                    match field(members_of(&self.request.analyze), "analysisOrdinal") {
                        Some(Value::Unsigned(n)) => Some(*n),
                        _ => None,
                    }
            }
            _ => {}
        }
        self.sequence += 1;
        self.slot += 1;
        Ok(Sent {
            bytes,
            frame: frame.host_frame(),
        })
    }

    /// The next planned frame, realized and admitted.
    pub fn send_next(&mut self, source: &mut dyn SnapshotSource) -> Result<Sent, SendRefusal> {
        let (frame, payload) = self.realize_next(source)?;
        let sequence = self.sequence;
        self.admit(frame, sequence, payload)
    }

    /// The Cancel lawful now (CANCEL-NULLABILITY): the exact echo of what was
    /// sent, with reason `user-interrupt`; `None` before the Hello slot or
    /// once the transcript has ended.
    pub fn cancel_payload(&self) -> Option<Value> {
        if !self.hello_sent() || self.cancelled || self.refused {
            return None;
        }
        Some(map(vec![
            (
                "executionId",
                self.sent_execution_id.as_deref().map_or(Value::Null, text),
            ),
            (
                "analysisOrdinal",
                self.sent_analysis_ordinal
                    .map_or(Value::Null, Value::Unsigned),
            ),
            ("reason", text(CANCEL_REASON)),
        ]))
    }

    /// Admit a Cancel (HOST-SEND-SCHEDULE; LD-D2B-7): at most once, never
    /// before the Hello slot, the next sequence number, and the exact echo
    /// compared by deterministic-CBOR bytes. Nothing follows it.
    pub fn admit_cancel(&mut self, sequence: u64, payload: Value) -> Result<Sent, SendRefusal> {
        if self.refused {
            return Err(SendRefusal::AfterRefusal);
        }
        match self.check_cancel(sequence, payload) {
            Ok(sent) => Ok(sent),
            Err(r) => Err(self.refuse(r)),
        }
    }

    fn check_cancel(&mut self, sequence: u64, payload: Value) -> Result<Sent, SendRefusal> {
        if self.cancelled {
            return Err(divergence("frame-after-cancel", "Cancel"));
        }
        let want = self
            .cancel_payload()
            .ok_or_else(|| divergence("cancel-before-hello", format!("slot {}", self.slot)))?;
        if sequence != self.sequence {
            return Err(divergence(
                "sequence",
                format!("{sequence}!={}", self.sequence),
            ));
        }
        if cbor::encode(&payload) != cbor::encode(&want) {
            return Err(divergence("cancel-echo", format!("slot {}", self.slot)));
        }
        let law = &self.request.law;
        law.check("Cancel", &payload)
            .map_err(|e| divergence("payload-schema", e))?;
        let bytes = write_frame(&law.envelope(sequence, "Cancel", payload))
            .ok_or_else(|| divergence("frame-limit", "over maxFramePayloadBytes"))?;
        let n = (bytes.len() - FRAME_PREFIX_BYTES) as u64;
        // Defensive: unreachable once the echo is exact (the reserve is the
        // maximal echo).
        if n > self.request.schedule.cancel_reserve_bytes {
            return Err(divergence("cancel-over-reserve", n));
        }
        self.cancelled = true;
        self.sequence += 1;
        Ok(Sent {
            bytes,
            frame: HostFrame::Cancel {
                execution_id: self.sent_execution_id.clone(),
                analysis_ordinal: self.sent_analysis_ordinal,
            },
        })
    }

    /// The user interrupt's Cancel, built from the sent state and admitted.
    pub fn cancel(&mut self) -> Result<Sent, SendRefusal> {
        if self.refused {
            return Err(SendRefusal::AfterRefusal);
        }
        if self.cancelled {
            return Err(self.refuse(divergence("frame-after-cancel", "Cancel")));
        }
        let Some(payload) = self.cancel_payload() else {
            let r = divergence("cancel-before-hello", format!("slot {}", self.slot));
            return Err(self.refuse(r));
        };
        let sequence = self.sequence;
        self.admit_cancel(sequence, payload)
    }
}

fn members_of(v: &Value) -> &[(String, Value)] {
    match v {
        Value::Map(m) => m,
        _ => &[],
    }
}
