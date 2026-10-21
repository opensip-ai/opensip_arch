//! Complete canonical request construction from admitted, immutable Plan
//! projections. No source bytes are read here and no worker is spawned.
use super::super::super::{
    cbor::{self, Value},
    ts2::carrier::{self, Carriers},
};
use super::super::{RUST3_FRAME_MAX_DEPTH, Rust3DispatchContext, Rust3StageBinding};
use super::{
    dependency, domain, policy, prepared,
    schedule::{self, Chunk, Entry, Frame, Recorder},
    snapshot,
};
use opensip_identity::JsonValue as J;
use std::collections::BTreeMap;

/// C4 owns admission of these values and every native set before PlanId.
/// These are supplied values, not an admitted Plan capability or factory.
pub(super) struct Plan {
    pub host_build_id: String,
    pub expected_identity: Value,
    pub capabilities: Vec<String>,
    pub open: policy::Open,
    pub snapshot: Vec<snapshot::Entry>,
    pub universes: Vec<domain::Universe>,
    pub selected_universe: usize,
    pub stages: Vec<domain::Stage>,
    pub dependency_set: J,
    pub dependency_manifests: BTreeMap<String, J>,
    pub prepared_set: Option<J>,
    pub analysis_ordinal: u64,
}
#[derive(Debug, PartialEq, Eq)]
pub(super) enum Refusal {
    HostInvariant(String),
    WireLimit(schedule::Refusal),
    ProjectionLimit(&'static str),
    Arithmetic,
}
fn invariant(v: impl std::fmt::Debug) -> Refusal {
    Refusal::HostInvariant(format!("{v:?}"))
}
fn snapshot_error(v: snapshot::Refusal) -> Refusal {
    match v {
        snapshot::Refusal::Bound(k) => Refusal::ProjectionLimit(k),
        _ => invariant(v),
    }
}
fn dependency_error(v: dependency::Refusal) -> Refusal {
    match v {
        dependency::Refusal::Bound(k) => Refusal::ProjectionLimit(k),
        _ => invariant(v),
    }
}
fn prepared_error(v: prepared::Refusal) -> Refusal {
    match v {
        prepared::Refusal::Bound(k) => Refusal::ProjectionLimit(k),
        _ => invariant(v),
    }
}
fn domain_error(v: domain::Refusal) -> Refusal {
    match v {
        domain::Refusal::Bound(k) => Refusal::ProjectionLimit(k),
        domain::Refusal::InlineSubjectLimit => Refusal::ProjectionLimit("inline subjects"),
        _ => invariant(v),
    }
}
fn member<'a>(v: &'a Value, k: &str) -> Result<&'a Value, Refusal> {
    let Value::Map(v) = v else {
        return Err(invariant("object"));
    };
    carrier::field(v, k).ok_or_else(|| invariant(format!("missing {k}")))
}
fn text(v: &Value) -> Result<&str, Refusal> {
    if let Value::Text(v) = v {
        Ok(v)
    } else {
        Err(invariant("text"))
    }
}
fn number(v: &Value) -> Result<u64, Refusal> {
    if let Value::Unsigned(v) = v {
        Ok(*v)
    } else {
        Err(invariant("uint64"))
    }
}
fn array(v: &Value) -> Result<&[Value], Refusal> {
    if let Value::Array(v) = v {
        Ok(v)
    } else {
        Err(invariant("array"))
    }
}
fn t(v: &str) -> Value {
    Value::Text(v.into())
}
fn map(v: Vec<(&str, Value)>) -> Value {
    Value::Map(v.into_iter().map(|(k, v)| (k.into(), v)).collect())
}
fn add(a: u64, b: u64) -> Result<u64, Refusal> {
    a.checked_add(b).ok_or(Refusal::Arithmetic)
}
fn canonical(v: &Value, maximum: u64) -> Result<Value, Refusal> {
    if cbor::encoded_length(v).ok_or(Refusal::Arithmetic)? > maximum {
        return Err(invariant("over-bound Plan wire value"));
    }
    cbor::decode(
        &cbor::encode(v),
        cbor::Profile::Rust3,
        RUST3_FRAME_MAX_DEPTH,
    )
    .map_err(invariant)
}

pub(super) struct Request {
    pub plan: Plan,
    pub policy: policy::Policy,
    pub schedule: schedule::Schedule,
    pub context: Rust3DispatchContext,
    pub reference: bool,
}
impl Request {
    pub(super) fn build(mut plan: Plan) -> Result<Self, Refusal> {
        let policy = policy::Policy::load().map_err(invariant)?;
        let maximum = policy.limit("maxFramePayloadBytes").map_err(invariant)?;
        // Reject duplicate keys, non-NFC strings, negative integers and deep
        // data before an external JSON projection could lose their meaning.
        plan.expected_identity = canonical(&plan.expected_identity, maximum)?;
        plan.open.universe = canonical(&plan.open.universe, maximum)?;
        plan.open.repository_resolution = canonical(&plan.open.repository_resolution, maximum)?;
        for stage in &mut plan.stages {
            stage.plan_stage = canonical(&stage.plan_stage, maximum)?;
        }
        for universe in &mut plan.universes {
            universe.value = canonical(&universe.value, maximum)?;
        }
        let selected = plan
            .universes
            .get(plan.selected_universe)
            .ok_or_else(|| invariant("selected universe"))?;
        let provider = text(member(&plan.expected_identity, "providerBuildId")?)?;
        if selected.value != plan.open.universe
            || selected.provider_id != "rust-semantic"
            || selected.provider_version != provider
        {
            return Err(invariant("selected Rust universe/identity join"));
        }
        let reference = plan
            .capabilities
            .iter()
            .any(|v| v == "subject-scope-reference-v1");
        if plan.capabilities.iter().any(|v| v == "symbol-census-v1") {
            return Err(invariant(
                "census Analyze requires D2b-4c; offered token cannot be removed",
            ));
        }
        let hello = policy
            .hello(
                &plan.host_build_id,
                plan.expected_identity.clone(),
                &plan.capabilities,
            )
            .map_err(invariant)?;
        let open = policy.open(&hello, plan.open.clone()).map_err(invariant)?;
        let snap = snapshot::build(&policy, &plan.open.snapshot_id, &plan.snapshot, 2)
            .map_err(snapshot_error)?;
        let dep_sequence = add(4, snap.chunks)?;
        let dep_id = text(member(
            &plan.open.repository_resolution,
            "dependencySourceSetId",
        )?)?;
        let dep = dependency::build(
            &policy,
            &dependency::Input {
                set: &plan.dependency_set,
                manifests: &plan.dependency_manifests,
                set_id: dep_id,
            },
            dep_sequence,
        )
        .map_err(dependency_error)?;
        let prepared_id = member(&plan.open.repository_resolution, "preparedOutputSetId")?;
        let prep = match (&plan.prepared_set, prepared_id) {
            (None, Value::Null) => None,
            (Some(set), Value::Text(set_id)) => Some(
                prepared::build(
                    &policy,
                    &prepared::Input {
                        set,
                        set_id,
                        plan_id: &plan.open.plan_id,
                    },
                    add(6, add(snap.chunks, dep.chunks)?)?,
                )
                .map_err(prepared_error)?,
            ),
            _ => return Err(invariant("selected prepared set/nullability join")),
        };
        let expected = add(
            if prep.is_some() { 10 } else { 7 },
            add(
                add(snap.chunks, dep.chunks)?,
                prep.as_ref().map_or(0, |p| p.chunks),
            )?,
        )?;
        let cancel = map(vec![
            ("executionId", t(&plan.open.execution_id)),
            ("analysisOrdinal", Value::Unsigned(plan.analysis_ordinal)),
            ("reason", t("user-interrupt")),
        ]);
        Carriers::load("Rust3")
            .map_err(invariant)?
            .check_record("Rust3CancelV2", &cancel)
            .map_err(invariant)?;
        let cancel_bytes =
            schedule::envelope_length(expected, "Cancel", &cancel).map_err(Refusal::WireLimit)?;
        let bounds = schedule::Bounds {
            frame_bytes: maximum,
            payload_bytes: policy
                .limit("maxRequestPayloadBytesTotal")
                .map_err(invariant)?,
            frames: policy.limit("maxRequestFrames").map_err(invariant)?,
        };
        let mut recorder =
            Recorder::new(bounds, expected, cancel_bytes).map_err(Refusal::WireLimit)?;
        recorder
            .fixed(Frame::Hello, &hello, None)
            .map_err(Refusal::WireLimit)?;
        recorder
            .fixed(Frame::OpenUniverse, &open, None)
            .map_err(Refusal::WireLimit)?;
        recorder
            .fixed(Frame::SnapshotManifest, &snap.manifest, None)
            .map_err(Refusal::WireLimit)?;
        let chunk_max = policy.limit("maxSnapshotChunkBytes").map_err(invariant)?;
        let mut manifest_files = BTreeMap::new();
        for entry in &plan.snapshot {
            if let snapshot::Entry::File {
                path,
                byte_length,
                content_sha256,
                ..
            } = entry
            {
                manifest_files.insert(path.clone(), (content_sha256.clone(), *byte_length));
                record_chunks(
                    &mut recorder,
                    Frame::SnapshotFileChunk,
                    Entry::Snapshot(path.clone()),
                    *byte_length,
                    content_sha256,
                    chunk_max,
                    |index, offset| {
                        map(vec![
                            ("snapshotId", t(&plan.open.snapshot_id)),
                            ("path", t(path)),
                            ("chunkIndex", Value::Unsigned(index)),
                            ("byteOffset", Value::Unsigned(offset)),
                        ])
                    },
                )?;
            }
        }
        recorder
            .fixed(Frame::SnapshotSeal, &snap.seal, Some(snap.chunks))
            .map_err(Refusal::WireLimit)?;
        recorder
            .fixed(Frame::DependencySourceManifest, &dep.manifest, None)
            .map_err(Refusal::WireLimit)?;
        for entry in array(member(&dep.manifest, "entries")?)? {
            let key = text(member(entry, "packageKey")?)?;
            let path = text(member(entry, "path")?)?;
            record_chunks(
                &mut recorder,
                Frame::DependencySourceChunk,
                Entry::Dependency {
                    package_key: key.into(),
                    path: path.into(),
                },
                number(member(entry, "byteLength")?)?,
                text(member(entry, "contentSha256")?)?,
                policy
                    .limit("maxDependencySourceChunkBytes")
                    .map_err(invariant)?,
                |index, offset| {
                    map(vec![
                        ("dependencySourceSetId", t(dep_id)),
                        ("packageKey", t(key)),
                        ("path", t(path)),
                        ("chunkIndex", Value::Unsigned(index)),
                        ("byteOffset", Value::Unsigned(offset)),
                    ])
                },
            )?;
        }
        recorder
            .fixed(Frame::DependencySourceSeal, &dep.seal, Some(dep.chunks))
            .map_err(Refusal::WireLimit)?;
        if let Some(prep) = &prep {
            recorder
                .fixed(Frame::PreparedOutputManifest, &prep.manifest, None)
                .map_err(Refusal::WireLimit)?;
            for entry in array(member(&prep.manifest, "entries")?)? {
                let ordinal = number(member(entry, "outputOrdinal")?)?;
                record_chunks(
                    &mut recorder,
                    Frame::PreparedOutputChunk,
                    Entry::Prepared(ordinal),
                    number(member(entry, "blobByteLength")?)?,
                    text(member(entry, "blobSha256")?)?,
                    policy
                        .limit("maxPreparedOutputChunkBytes")
                        .map_err(invariant)?,
                    |index, offset| {
                        map(vec![
                            ("planId", t(&plan.open.plan_id)),
                            ("outputOrdinal", Value::Unsigned(ordinal)),
                            ("chunkIndex", Value::Unsigned(index)),
                            ("byteOffset", Value::Unsigned(offset)),
                        ])
                    },
                )?;
            }
            recorder
                .fixed(Frame::PreparedOutputSeal, &prep.seal, Some(prep.chunks))
                .map_err(Refusal::WireLimit)?;
        }
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
        let law = domain::Law::load().map_err(invariant)?;
        let derived = law
            .derive(domain::Input {
                snapshot: &plan.open.snapshot_id,
                files: &files,
                universes: &plan.universes,
                selected: plan.selected_universe,
                provider_build_id: provider,
                plan_stages: &plan.stages,
                bounds: domain::Bounds {
                    snapshot_entries: policy.limit("maxSnapshotEntries").map_err(invariant)?,
                    inline_subjects: policy.limit("maxSubjectsPerStage").map_err(invariant)?,
                    stages: policy.limit("maxAnalyzeStages").map_err(invariant)?,
                    keys_per_stage: policy
                        .limit("maxRequestedCoverageKeysPerStage")
                        .map_err(invariant)?,
                },
                reference,
            })
            .map_err(domain_error)?;
        let analyze = law
            .analyze(
                &derived,
                &domain::AnalyzeContext {
                    execution_id: &plan.open.execution_id,
                    snapshot_id: &plan.open.snapshot_id,
                    plan_id: &plan.open.plan_id,
                    analysis_ordinal: plan.analysis_ordinal,
                },
                reference,
                recorder.sequence().map_err(Refusal::WireLimit)?,
                maximum,
                recorder
                    .remaining_payload_bytes()
                    .map_err(Refusal::WireLimit)?,
            )
            .map_err(domain_error)?;
        recorder
            .fixed(Frame::Analyze, &analyze, None)
            .map_err(Refusal::WireLimit)?;
        let stages = array(member(&analyze, "stages")?)?
            .iter()
            .map(|s| {
                Ok(Rust3StageBinding {
                    plan_stage: member(s, "planStage")?.clone(),
                    analysis_domain: member(s, "analysisDomain")?.clone(),
                })
            })
            .collect::<Result<_, Refusal>>()?;
        let context = Rust3DispatchContext {
            hello,
            open_universe: open,
            snapshot_seal: snap.seal,
            dependency_seal: dep.seal,
            prepared_seal: prep.map(|p| p.seal),
            manifest_files,
            universe_key: derived.source_universe_id,
            target_domain: derived.target_domain,
            analysis_ordinal: plan.analysis_ordinal,
            stages,
        };
        Ok(Self {
            plan,
            policy,
            schedule: recorder.finish().map_err(Refusal::WireLimit)?,
            context,
            reference,
        })
    }
}
fn record_chunks(
    recorder: &mut Recorder,
    frame: Frame,
    entry: Entry,
    length: u64,
    digest: &str,
    maximum: u64,
    header: impl Fn(u64, u64) -> Value,
) -> Result<(), Refusal> {
    let count = schedule::chunk_count(length, maximum).map_err(Refusal::WireLimit)?;
    for index in 0..count {
        let offset = index.checked_mul(maximum).ok_or(Refusal::Arithmetic)?;
        let bytes = length
            .checked_sub(offset)
            .ok_or(Refusal::Arithmetic)?
            .min(maximum);
        let coordinates = Chunk {
            entry: entry.clone(),
            index,
            offset,
            length: bytes,
        };
        recorder
            .chunk(
                frame,
                &header(index, offset),
                &coordinates,
                if add(index, 1)? == count {
                    Some(digest)
                } else {
                    None
                },
            )
            .map_err(Refusal::WireLimit)?;
    }
    Ok(())
}

#[cfg(test)]
#[path = "request_tests.rs"]
mod tests;
