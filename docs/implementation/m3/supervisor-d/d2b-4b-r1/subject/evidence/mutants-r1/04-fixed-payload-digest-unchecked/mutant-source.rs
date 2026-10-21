//! Independent greedy realization and exact immutable-schedule admission.
//! This inert sender grants no worker/source authority. The D3a participant
//! owns acknowledgment gates and finishes each pending write before Cancel.
use super::super::super::{
    FRAME_PREFIX_BYTES,
    cbor::{self, Value},
    ts2::carrier::{self, Carriers},
    write_frame,
};
use super::super::Rust3HostFrame;
use super::{
    dependency, domain, policy, prepared,
    request::{Plan, Request},
    schedule::{self, Chunk, Entry, Frame},
    snapshot,
};
use opensip_identity::{RawSha256, digest_hex, raw_sha256};
use std::collections::BTreeMap;

#[derive(Debug, PartialEq, Eq)]
pub enum Refusal {
    Divergence(String),
    Source(String),
    AfterRefusal,
}
fn divergence(v: impl std::fmt::Debug) -> Refusal {
    Refusal::Divergence(format!("SENDER_DIVERGENCE: {v:?}"))
}
/// Reads exactly one bounded interval from the corresponding immutable C1,
/// dependency or prepared-output custody. No live-root path is supplied.
pub trait Source {
    fn read(&mut self, entry: &Entry, offset: u64, length: usize) -> std::io::Result<Vec<u8>>;
}
#[derive(Debug, PartialEq, Eq)]
pub struct Sent {
    pub bytes: Vec<u8>,
    pub frame: Rust3HostFrame,
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Family {
    Snapshot,
    Dependency,
    Prepared,
}
impl Family {
    fn index(self) -> usize {
        match self {
            Self::Snapshot => 0,
            Self::Dependency => 1,
            Self::Prepared => 2,
        }
    }
}
#[derive(Clone)]
struct Meta {
    position: usize,
    entry: Entry,
    length: u64,
    sha256: String,
}
#[derive(Clone, Copy)]
enum Cursor {
    Fixed(Frame),
    Chunks {
        family: Family,
        entry: usize,
        index: u64,
        offset: u64,
    },
    Done,
}
struct Fresh {
    fixed: BTreeMap<Frame, Value>,
    entries: [Vec<Meta>; 3],
}
struct Realized {
    frame: Frame,
    chunk: Option<Chunk>,
    final_digest: Option<String>,
}
pub struct Sender {
    request: Request,
    fresh: Fresh,
    cursor: Cursor,
    slot: usize,
    sequence: u64,
    realized: Option<Realized>,
    counts: [u64; 3],
    totals: schedule::Totals,
    entry_digest: Option<RawSha256>,
    sent_execution: Option<String>,
    sent_ordinal: Option<u64>,
    cancelled: bool,
    refused: bool,
}
fn field<'a>(v: &'a Value, k: &str) -> Result<&'a Value, Refusal> {
    let Value::Map(v) = v else {
        return Err(divergence("map"));
    };
    carrier::field(v, k).ok_or_else(|| divergence(k))
}
fn text(v: &Value) -> Result<&str, Refusal> {
    if let Value::Text(v) = v {
        Ok(v)
    } else {
        Err(divergence("text"))
    }
}
fn number(v: &Value) -> Result<u64, Refusal> {
    if let Value::Unsigned(v) = v {
        Ok(*v)
    } else {
        Err(divergence("uint64"))
    }
}
fn array(v: &Value) -> Result<&[Value], Refusal> {
    if let Value::Array(v) = v {
        Ok(v)
    } else {
        Err(divergence("array"))
    }
}
fn t(v: &str) -> Value {
    Value::Text(v.into())
}
fn map(v: Vec<(&str, Value)>) -> Value {
    Value::Map(v.into_iter().map(|(k, v)| (k.into(), v)).collect())
}
fn add(a: u64, b: u64) -> Result<u64, Refusal> {
    a.checked_add(b).ok_or_else(|| divergence("arithmetic"))
}
fn set_count(value: &Value, count: u64) -> Result<Value, Refusal> {
    let Value::Map(v) = value else {
        return Err(divergence("seal"));
    };
    let mut v = v.clone();
    let row = v
        .iter_mut()
        .find(|(k, _)| k == "totalChunkCount")
        .ok_or_else(|| divergence("seal count"))?;
    row.1 = Value::Unsigned(count);
    Ok(Value::Map(v))
}

impl Fresh {
    /// Rebuild from Plan values, never from the planner's slots or cached
    /// dispatch context. The bounded builders may be shared, not their output.
    fn build(plan: &Plan, policy: &policy::Policy) -> Result<Self, Refusal> {
        let hello = policy
            .hello(
                &plan.host_build_id,
                plan.expected_identity.clone(),
                &plan.capabilities,
            )
            .map_err(divergence)?;
        let open = policy.open(&hello, plan.open.clone()).map_err(divergence)?;
        let snap = snapshot::build(policy, &plan.open.snapshot_id, &plan.snapshot, 2)
            .map_err(divergence)?;
        let dep_id = text(field(
            &plan.open.repository_resolution,
            "dependencySourceSetId",
        )?)?;
        let dep = dependency::build(
            policy,
            &dependency::Input {
                set: &plan.dependency_set,
                manifests: &plan.dependency_manifests,
                set_id: dep_id,
            },
            add(4, snap.chunks)?,
        )
        .map_err(divergence)?;
        let prep = match (
            &plan.prepared_set,
            field(&plan.open.repository_resolution, "preparedOutputSetId")?,
        ) {
            (None, Value::Null) => None,
            (Some(set), Value::Text(set_id)) => Some(
                prepared::build(
                    policy,
                    &prepared::Input {
                        set,
                        set_id,
                        plan_id: &plan.open.plan_id,
                    },
                    add(6, add(snap.chunks, dep.chunks)?)?,
                )
                .map_err(divergence)?,
            ),
            _ => return Err(divergence("prepared selection")),
        };
        let files: Vec<_> = plan
            .snapshot
            .iter()
            .filter_map(|e| match e {
                snapshot::Entry::File {
                    path,
                    byte_length,
                    content_sha256,
                    ..
                } => Some(domain::File {
                    path: path.clone(),
                    byte_length: *byte_length,
                    content_sha256: content_sha256.clone(),
                }),
                _ => None,
            })
            .collect();
        let law = domain::Law::load().map_err(divergence)?;
        let derived = law
            .derive(domain::Input {
                snapshot: &plan.open.snapshot_id,
                files: &files,
                universes: &plan.universes,
                selected: plan.selected_universe,
                provider_build_id: text(field(&plan.expected_identity, "providerBuildId")?)?,
                plan_stages: &plan.stages,
                bounds: domain::Bounds {
                    snapshot_entries: policy.limit("maxSnapshotEntries").map_err(divergence)?,
                    inline_subjects: policy.limit("maxSubjectsPerStage").map_err(divergence)?,
                    stages: policy.limit("maxAnalyzeStages").map_err(divergence)?,
                    keys_per_stage: policy
                        .limit("maxRequestedCoverageKeysPerStage")
                        .map_err(divergence)?,
                },
                reference: plan
                    .capabilities
                    .iter()
                    .any(|v| v == "subject-scope-reference-v1"),
            })
            .map_err(divergence)?;
        let analyze_sequence = add(
            if prep.is_some() { 8 } else { 6 },
            add(
                add(snap.chunks, dep.chunks)?,
                prep.as_ref().map_or(0, |p| p.chunks),
            )?,
        )?;
        let analyze = law
            .analyze(
                &derived,
                &domain::AnalyzeContext {
                    execution_id: &plan.open.execution_id,
                    snapshot_id: &plan.open.snapshot_id,
                    plan_id: &plan.open.plan_id,
                    analysis_ordinal: plan.analysis_ordinal,
                },
                plan.capabilities
                    .iter()
                    .any(|v| v == "subject-scope-reference-v1"),
                analyze_sequence,
                policy.limit("maxFramePayloadBytes").map_err(divergence)?,
                policy
                    .limit("maxRequestPayloadBytesTotal")
                    .map_err(divergence)?,
            )
            .map_err(divergence)?;
        let snapshot_entries = plan
            .snapshot
            .iter()
            .enumerate()
            .filter_map(|(position, e)| match e {
                snapshot::Entry::File {
                    path,
                    byte_length,
                    content_sha256,
                    ..
                } => Some(Meta {
                    position,
                    entry: Entry::Snapshot(path.clone()),
                    length: *byte_length,
                    sha256: content_sha256.clone(),
                }),
                _ => None,
            })
            .collect();
        let mut dependency_entries = Vec::new();
        for (position, entry) in array(field(&dep.manifest, "entries")?)?.iter().enumerate() {
            dependency_entries.push(Meta {
                position,
                entry: Entry::Dependency {
                    package_key: text(field(entry, "packageKey")?)?.into(),
                    path: text(field(entry, "path")?)?.into(),
                },
                length: number(field(entry, "byteLength")?)?,
                sha256: text(field(entry, "contentSha256")?)?.into(),
            });
        }
        let mut prepared_entries = Vec::new();
        if let Some(p) = &prep {
            for (position, entry) in array(field(&p.manifest, "entries")?)?.iter().enumerate() {
                prepared_entries.push(Meta {
                    position,
                    entry: Entry::Prepared(number(field(entry, "outputOrdinal")?)?),
                    length: number(field(entry, "blobByteLength")?)?,
                    sha256: text(field(entry, "blobSha256")?)?.into(),
                });
            }
        }
        let mut fixed = BTreeMap::from([
            (Frame::Hello, hello),
            (Frame::OpenUniverse, open),
            (Frame::SnapshotManifest, snap.manifest),
            (Frame::SnapshotSeal, snap.seal),
            (Frame::DependencySourceManifest, dep.manifest),
            (Frame::DependencySourceSeal, dep.seal),
            (Frame::Analyze, analyze),
        ]);
        if let Some(p) = prep {
            fixed.insert(Frame::PreparedOutputManifest, p.manifest);
            fixed.insert(Frame::PreparedOutputSeal, p.seal);
        }
        Ok(Self {
            fixed,
            entries: [snapshot_entries, dependency_entries, prepared_entries],
        })
    }
}
impl Sender {
    pub fn new(request: Request) -> Result<Self, Refusal> {
        let fresh = Fresh::build(&request.plan, &request.policy)?;
        Ok(Self {
            request,
            fresh,
            cursor: Cursor::Fixed(Frame::Hello),
            slot: 0,
            sequence: 0,
            realized: None,
            counts: [0; 3],
            totals: schedule::Totals {
                payload_bytes: 0,
                frames: 0,
            },
            entry_digest: None,
            sent_execution: None,
            sent_ordinal: None,
            cancelled: false,
            refused: false,
        })
    }
    pub fn request(&self) -> &Request {
        &self.request
    }
    pub fn next_slot(&self) -> Option<&schedule::Slot> {
        if self.cancelled || self.refused {
            None
        } else {
            self.request.schedule.slots.get(self.slot)
        }
    }
    pub fn hello_sent(&self) -> bool {
        self.slot > 0
    }
    pub fn cancelled(&self) -> bool {
        self.cancelled
    }
    pub fn complete(&self) -> bool {
        self.cancelled || self.slot == self.request.schedule.slots.len()
    }
    fn latch<T>(&mut self, result: Result<T, Refusal>) -> Result<T, Refusal> {
        if result.is_err() {
            self.refused = true;
        }
        result
    }
    fn maximum(&self, family: Family) -> Result<u64, Refusal> {
        self.request
            .policy
            .limit(match family {
                Family::Snapshot => "maxSnapshotChunkBytes",
                Family::Dependency => "maxDependencySourceChunkBytes",
                Family::Prepared => "maxPreparedOutputChunkBytes",
            })
            .map_err(divergence)
    }
    pub fn realize_next(&mut self, source: &mut dyn Source) -> Result<(Frame, Value), Refusal> {
        if self.refused {
            return Err(Refusal::AfterRefusal);
        }
        let result = self.realize(source);
        self.latch(result)
    }
    fn realize(&mut self, source: &mut dyn Source) -> Result<(Frame, Value), Refusal> {
        if self.cancelled || self.realized.is_some() {
            return Err(divergence("ended or unconsumed realization"));
        }
        loop {
            match self.cursor {
                Cursor::Done => return Err(divergence("no ordinary frame remains")),
                Cursor::Fixed(frame) => {
                    let value = self
                        .fresh
                        .fixed
                        .get(&frame)
                        .ok_or_else(|| divergence("missing fresh frame"))?;
                    let (payload, next) = match frame {
                        Frame::Hello => (value.clone(), Cursor::Fixed(Frame::OpenUniverse)),
                        Frame::OpenUniverse => {
                            (value.clone(), Cursor::Fixed(Frame::SnapshotManifest))
                        }
                        Frame::SnapshotManifest => (
                            value.clone(),
                            Cursor::Chunks {
                                family: Family::Snapshot,
                                entry: 0,
                                index: 0,
                                offset: 0,
                            },
                        ),
                        Frame::SnapshotSeal => (
                            set_count(value, self.counts[0])?,
                            Cursor::Fixed(Frame::DependencySourceManifest),
                        ),
                        Frame::DependencySourceManifest => (
                            value.clone(),
                            Cursor::Chunks {
                                family: Family::Dependency,
                                entry: 0,
                                index: 0,
                                offset: 0,
                            },
                        ),
                        Frame::DependencySourceSeal => (
                            set_count(value, self.counts[1])?,
                            Cursor::Fixed(if self.request.plan.prepared_set.is_some() {
                                Frame::PreparedOutputManifest
                            } else {
                                Frame::Analyze
                            }),
                        ),
                        Frame::PreparedOutputManifest => (
                            value.clone(),
                            Cursor::Chunks {
                                family: Family::Prepared,
                                entry: 0,
                                index: 0,
                                offset: 0,
                            },
                        ),
                        Frame::PreparedOutputSeal => (
                            set_count(value, self.counts[2])?,
                            Cursor::Fixed(Frame::Analyze),
                        ),
                        Frame::Analyze => (value.clone(), Cursor::Done),
                        _ => return Err(divergence("chunk in fixed cursor")),
                    };
                    self.cursor = next;
                    self.realized = Some(Realized {
                        frame,
                        chunk: None,
                        final_digest: None,
                    });
                    return Ok((frame, payload));
                }
                Cursor::Chunks {
                    family,
                    entry,
                    index,
                    offset,
                } => {
                    let Some(meta) = self.fresh.entries[family.index()].get(entry) else {
                        self.cursor = Cursor::Fixed(match family {
                            Family::Snapshot => Frame::SnapshotSeal,
                            Family::Dependency => Frame::DependencySourceSeal,
                            Family::Prepared => Frame::PreparedOutputSeal,
                        });
                        continue;
                    };
                    if offset >= meta.length {
                        if meta.length == 0 && meta.sha256 != digest_hex(&raw_sha256(&[])) {
                            return Err(Refusal::Source("empty entry content digest".into()));
                        }
                        self.cursor = Cursor::Chunks {
                            family,
                            entry: entry
                                .checked_add(1)
                                .ok_or_else(|| divergence("entry overflow"))?,
                            index: 0,
                            offset: 0,
                        };
                        continue;
                    }
                    let maximum = self.maximum(family)?;
                    let length = maximum.min(
                        meta.length
                            .checked_sub(offset)
                            .ok_or_else(|| divergence("chunk offset"))?,
                    );
                    if length == 0
                        || offset
                            != index
                                .checked_mul(maximum)
                                .ok_or_else(|| divergence("chunk coordinate overflow"))?
                    {
                        return Err(divergence("greedy cursor"));
                    }
                    let wanted = usize::try_from(length).map_err(divergence)?;
                    let bytes = source
                        .read(&meta.entry, offset, wanted)
                        .map_err(|e| Refusal::Source(e.to_string()))?;
                    if bytes.len() != wanted {
                        return Err(Refusal::Source("custody returned wrong byte count".into()));
                    }
                    let end = add(offset, length)?;
                    let digest = (end == meta.length).then(|| meta.sha256.clone());
                    let coordinates = Chunk {
                        entry: meta.entry.clone(),
                        index,
                        offset,
                        length,
                    };
                    let (frame, payload) = match &meta.entry {
                        Entry::Snapshot(_) => (
                            Frame::SnapshotFileChunk,
                            snapshot::chunk(
                                &self.request.policy,
                                &self.request.plan.open.snapshot_id,
                                self.request
                                    .plan
                                    .snapshot
                                    .get(meta.position)
                                    .ok_or_else(|| divergence("snapshot position"))?,
                                index,
                                offset,
                                bytes,
                            )
                            .map_err(divergence)?,
                        ),
                        Entry::Dependency { .. } => {
                            let manifest = self
                                .fresh
                                .fixed
                                .get(&Frame::DependencySourceManifest)
                                .ok_or_else(|| divergence("dependency manifest"))?;
                            let row = array(field(manifest, "entries")?)?
                                .get(meta.position)
                                .ok_or_else(|| divergence("dependency position"))?;
                            (
                                Frame::DependencySourceChunk,
                                dependency::chunk(
                                    &self.request.policy,
                                    text(field(
                                        &self.request.plan.open.repository_resolution,
                                        "dependencySourceSetId",
                                    )?)?,
                                    row,
                                    index,
                                    offset,
                                    bytes,
                                )
                                .map_err(divergence)?,
                            )
                        }
                        Entry::Prepared(_) => {
                            let manifest = self
                                .fresh
                                .fixed
                                .get(&Frame::PreparedOutputManifest)
                                .ok_or_else(|| divergence("prepared manifest"))?;
                            let row = array(field(manifest, "entries")?)?
                                .get(meta.position)
                                .ok_or_else(|| divergence("prepared position"))?;
                            (
                                Frame::PreparedOutputChunk,
                                prepared::chunk(
                                    &self.request.policy,
                                    &self.request.plan.open.plan_id,
                                    row,
                                    index,
                                    offset,
                                    bytes,
                                )
                                .map_err(divergence)?,
                            )
                        }
                    };
                    self.counts[family.index()] = add(self.counts[family.index()], 1)?;
                    self.cursor = Cursor::Chunks {
                        family,
                        entry,
                        index: add(index, 1)?,
                        offset: end,
                    };
                    self.realized = Some(Realized {
                        frame,
                        chunk: Some(coordinates),
                        final_digest: digest,
                    });
                    return Ok((frame, payload));
                }
            }
        }
    }
    pub fn admit(&mut self, frame: Frame, sequence: u64, payload: Value) -> Result<Sent, Refusal> {
        if self.refused {
            return Err(Refusal::AfterRefusal);
        }
        let result = self.check(frame, sequence, payload);
        self.latch(result)
    }
    fn check(&mut self, frame: Frame, sequence: u64, payload: Value) -> Result<Sent, Refusal> {
        if self.cancelled || sequence != self.sequence {
            return Err(divergence("ended or sequence"));
        }
        let realized = self
            .realized
            .as_ref()
            .ok_or_else(|| divergence("no independent realization"))?;
        let slot = self
            .request
            .schedule
            .slots
            .get(self.slot)
            .ok_or_else(|| divergence("no planned slot"))?;
        if realized.frame != frame
            || slot.frame != frame
            || slot.sequence != sequence
            || slot.chunk != realized.chunk
            || slot.entry_content_sha256 != realized.final_digest
        {
            return Err(divergence("slot type/sequence/coordinates/final digest"));
        }
        let carriers = Carriers::load("Rust3").map_err(divergence)?;
        let payload_bytes =
            schedule::envelope_length(sequence, frame.name(), &payload).map_err(divergence)?;
        if payload_bytes != slot.payload_bytes {
            return Err(divergence("planned envelope byte length"));
        }
        let next = self.charged(payload_bytes, false)?;
        let next_sequence = add(self.sequence, 1)?;
        let next_slot = self
            .slot
            .checked_add(1)
            .ok_or_else(|| divergence("slot overflow"))?;
        if next_slot == self.request.schedule.slots.len()
            && (add(
                next.payload_bytes,
                self.request.schedule.cancel_reserve_bytes,
            )? != self.request.schedule.totals.payload_bytes
                || add(next.frames, 1)? != self.request.schedule.totals.frames)
        {
            return Err(divergence("final planned request totals"));
        }
        let mut next_digest = None;
        if let Some(chunk) = &realized.chunk {
            let bytes = match field(&payload, "bytes")? {
                Value::Bytes(b) => b,
                _ => return Err(divergence("chunk bytes")),
            };
            if bytes.len() as u64 != chunk.length
                || number(field(&payload, "chunkIndex")?)? != chunk.index
                || number(field(&payload, "byteOffset")?)? != chunk.offset
            {
                return Err(divergence("chunk coordinates"));
            }
            match &chunk.entry {
                Entry::Snapshot(path) => {
                    if field(&payload, "path")? != &t(path) {
                        return Err(divergence("snapshot path"));
                    }
                }
                Entry::Dependency { package_key, path } => {
                    if field(&payload, "packageKey")? != &t(package_key)
                        || field(&payload, "path")? != &t(path)
                    {
                        return Err(divergence("dependency identity"));
                    }
                }
                Entry::Prepared(ordinal) => {
                    if field(&payload, "outputOrdinal")? != &Value::Unsigned(*ordinal) {
                        return Err(divergence("prepared ordinal"));
                    }
                }
            }
            let Value::Map(fields) = &payload else {
                return Err(divergence("chunk map"));
            };
            let header = Value::Map(
                fields
                    .iter()
                    .filter(|(k, _)| k != "bytes")
                    .cloned()
                    .collect(),
            );
            if raw_sha256(&cbor::encode(&header)) != slot.payload_sha256 {
                return Err(divergence("chunk header digest"));
            }
            let record = match frame {
                Frame::SnapshotFileChunk => "Rust3SnapshotFileChunkV2",
                Frame::DependencySourceChunk => "Rust3DependencySourceChunkV3",
                Frame::PreparedOutputChunk => "Rust3PreparedOutputChunkV3",
                _ => return Err(divergence("chunk frame")),
            };
            carriers
                .check_record(record, &payload)
                .map_err(divergence)?;
            let digest = if chunk.index == 0 {
                if self.entry_digest.is_some() {
                    return Err(divergence("unfinished entry"));
                }
                RawSha256::new()
            } else {
                self.entry_digest
                    .take()
                    .ok_or_else(|| divergence("missing entry digest"))?
            };
            let digest = digest.update(bytes).map_err(divergence)?;
            if let Some(want) = &realized.final_digest {
                if digest_hex(&digest.finish()) != *want {
                    return Err(Refusal::Source("entry content digest".into()));
                }
            } else {
                next_digest = Some(digest);
            }
        } else {
            if self.entry_digest.is_some() {
                return Err(divergence("unfinished entry at fixed frame"));
            }
            if false && raw_sha256(&cbor::encode(&payload)) != slot.payload_sha256 {
                return Err(divergence("fixed payload digest"));
            }
            if let Some(count) = slot.total_chunk_count
                && field(&payload, "totalChunkCount")? != &Value::Unsigned(count)
            {
                return Err(divergence("seal chunk count"));
            }
            // Fresh fixed frames were individually schema-checked from Plan;
            // this exact digest binds that output before it becomes sent state.
        }
        let execution = if frame == Frame::OpenUniverse {
            Some(text(field(&payload, "executionId")?)?.to_owned())
        } else {
            self.sent_execution.clone()
        };
        let ordinal = if frame == Frame::Analyze {
            Some(number(field(&payload, "analysisOrdinal")?)?)
        } else {
            self.sent_ordinal
        };
        let envelope = schedule::envelope(sequence, frame.name(), payload);
        let bytes = write_frame(&envelope).ok_or_else(|| divergence("frame encoder refused"))?;
        if bytes
            .len()
            .checked_sub(FRAME_PREFIX_BYTES)
            .and_then(|n| u64::try_from(n).ok())
            != Some(payload_bytes)
        {
            return Err(divergence("encoded envelope size"));
        }
        // The same strict profile applies to what is sent, including duplicate
        // map keys that a JSON schema projection alone could erase.
        let decoded = cbor::decode(
            &bytes[FRAME_PREFIX_BYTES..],
            cbor::Profile::Rust3,
            super::super::RUST3_FRAME_MAX_DEPTH,
        )
        .map_err(divergence)?;
        check_envelope(&decoded, sequence, frame.name())?;
        self.entry_digest = next_digest;
        self.sent_execution = execution;
        self.sent_ordinal = ordinal;
        self.sequence = next_sequence;
        self.slot = next_slot;
        self.totals = next;
        self.realized = None;
        Ok(Sent {
            bytes,
            frame: host_frame(frame),
        })
    }
    fn charged(&self, bytes: u64, cancel: bool) -> Result<schedule::Totals, Refusal> {
        let total = add(self.totals.payload_bytes, bytes)?;
        let frames = add(self.totals.frames, 1)?;
        let reserve = if cancel {
            0
        } else {
            self.request.schedule.cancel_reserve_bytes
        };
        let reserve_frames = u64::from(!cancel);
        if bytes
            > self
                .request
                .policy
                .limit("maxFramePayloadBytes")
                .map_err(divergence)?
            || add(total, reserve)?
                > self
                    .request
                    .policy
                    .limit("maxRequestPayloadBytesTotal")
                    .map_err(divergence)?
            || add(frames, reserve_frames)?
                > self
                    .request
                    .policy
                    .limit("maxRequestFrames")
                    .map_err(divergence)?
        {
            return Err(divergence("defensive running request limit"));
        }
        Ok(schedule::Totals {
            payload_bytes: total,
            frames,
        })
    }
    pub fn send_next(&mut self, source: &mut dyn Source) -> Result<Sent, Refusal> {
        let (frame, payload) = self.realize_next(source)?;
        self.admit(frame, self.sequence, payload)
    }
    pub fn cancel_payload(&self) -> Option<Value> {
        if !self.hello_sent() || self.cancelled || self.refused || self.realized.is_some() {
            None
        } else {
            Some(map(vec![
                (
                    "executionId",
                    self.sent_execution.as_deref().map_or(Value::Null, t),
                ),
                (
                    "analysisOrdinal",
                    self.sent_ordinal.map_or(Value::Null, Value::Unsigned),
                ),
                ("reason", t("user-interrupt")),
            ]))
        }
    }
    pub fn admit_cancel(&mut self, sequence: u64, payload: Value) -> Result<Sent, Refusal> {
        if self.refused {
            return Err(Refusal::AfterRefusal);
        }
        let result = self.check_cancel(sequence, payload);
        self.latch(result)
    }
    fn check_cancel(&mut self, sequence: u64, payload: Value) -> Result<Sent, Refusal> {
        let expected = self
            .cancel_payload()
            .ok_or_else(|| divergence("Cancel not permitted"))?;
        if sequence != self.sequence || cbor::encode(&payload) != cbor::encode(&expected) {
            return Err(divergence("Cancel sequence/typed echo"));
        }
        Carriers::load("Rust3")
            .map_err(divergence)?
            .check_record("Rust3CancelV2", &payload)
            .map_err(divergence)?;
        let length = schedule::envelope_length(sequence, "Cancel", &payload).map_err(divergence)?;
        if length > self.request.schedule.cancel_reserve_bytes {
            return Err(divergence("Cancel reserve"));
        }
        let next = self.charged(length, true)?;
        let next_sequence = add(self.sequence, 1)?;
        let bytes = write_frame(&schedule::envelope(sequence, "Cancel", payload))
            .ok_or_else(|| divergence("Cancel frame"))?;
        let decoded = cbor::decode(
            &bytes[FRAME_PREFIX_BYTES..],
            cbor::Profile::Rust3,
            super::super::RUST3_FRAME_MAX_DEPTH,
        )
        .map_err(divergence)?;
        check_envelope(&decoded, sequence, "Cancel")?;
        self.cancelled = true;
        self.totals = next;
        self.sequence = next_sequence;
        Ok(Sent {
            bytes,
            frame: Rust3HostFrame::Cancel {
                execution_id: self.sent_execution.clone(),
                analysis_ordinal: self.sent_ordinal,
            },
        })
    }
    pub fn cancel(&mut self) -> Result<Sent, Refusal> {
        if self.refused {
            return Err(Refusal::AfterRefusal);
        }
        let Some(payload) = self.cancel_payload() else {
            return self.latch(Err(divergence("Cancel not permitted")));
        };
        self.admit_cancel(self.sequence, payload)
    }
}
pub(super) fn host_frame(frame: Frame) -> Rust3HostFrame {
    match frame {
        Frame::Hello => Rust3HostFrame::Hello,
        Frame::OpenUniverse => Rust3HostFrame::OpenUniverse,
        Frame::SnapshotManifest => Rust3HostFrame::SnapshotManifest,
        Frame::SnapshotFileChunk => Rust3HostFrame::SnapshotFileChunk,
        Frame::SnapshotSeal => Rust3HostFrame::SnapshotSeal,
        Frame::DependencySourceManifest => Rust3HostFrame::DependencySourceManifest,
        Frame::DependencySourceChunk => Rust3HostFrame::DependencySourceChunk,
        Frame::DependencySourceSeal => Rust3HostFrame::DependencySourceSeal,
        Frame::PreparedOutputManifest => Rust3HostFrame::PreparedOutputManifest,
        Frame::PreparedOutputChunk => Rust3HostFrame::PreparedOutputChunk,
        Frame::PreparedOutputSeal => Rust3HostFrame::PreparedOutputSeal,
        Frame::Analyze => Rust3HostFrame::Analyze,
    }
}

fn check_envelope(value: &Value, sequence: u64, name: &str) -> Result<(), Refusal> {
    let Value::Map(fields) = value else {
        return Err(divergence("envelope map"));
    };
    if fields.len() != 5
        || field(value, "protocolMajor")? != &Value::Unsigned(3)
        || field(value, "direction")? != &t("host-to-worker")
        || field(value, "sequence")? != &Value::Unsigned(sequence)
        || field(value, "frameType")? != &t(name)
    {
        return Err(divergence("closed Rust3 host envelope"));
    }
    field(value, "payload")?;
    Ok(())
}

#[cfg(test)]
#[path = "sender_tests.rs"]
pub(super) mod tests;
