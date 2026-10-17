//! M3-D r5 item 10 (unit D2b-3a): the admitted tree converted by hand into the
//! generated carriers ("The decoded tree is converted by hand-written,
//! schema-checked code into the generated carrier types"; serde never
//! deserializes wire bytes). Every conversion runs after the frame's closed
//! check, so a failure here is the codec's invariant, never a wire outcome;
//! it still refuses rather than guessing. The three open-JSON members the
//! generator emits for schema constants are built as `GeneratedJson`
//! (LD-D2B3-3).
use super::super::cbor::Value;
use super::carrier::field;
use opensip_contracts::GeneratedJson;
use opensip_contracts::generated::evidence::ExactInteger;
use opensip_contracts::generated::evidence::*;
use opensip_contracts::generated::protocol::*;
use std::str::FromStr;

type R<T> = Result<T, String>;

fn map<'v>(v: &'v Value, at: &str) -> R<&'v [(String, Value)]> {
    match v {
        Value::Map(f) => Ok(f),
        _ => Err(format!("{at}: map")),
    }
}
fn get<'v>(f: &'v [(String, Value)], name: &str) -> R<&'v Value> {
    field(f, name).ok_or_else(|| format!("missing {name}"))
}
fn text(f: &[(String, Value)], name: &str) -> R<String> {
    match get(f, name)? {
        Value::Text(s) => Ok(s.clone()),
        _ => Err(format!("{name}: text")),
    }
}
fn unsigned(f: &[(String, Value)], name: &str) -> R<u64> {
    match get(f, name)? {
        Value::Unsigned(n) => Ok(*n),
        _ => Err(format!("{name}: uint64")),
    }
}
#[allow(
    clippy::unnecessary_fallible_conversions,
    reason = "the infallible From would add a call to the mint census"
)]
fn exact(f: &[(String, Value)], name: &str) -> R<ExactInteger> {
    ExactInteger::try_from(unsigned(f, name)?).map_err(|_| format!("{name}: exact integer"))
}
fn parse<T: FromStr>(f: &[(String, Value)], name: &str) -> R<T> {
    text(f, name)?
        .parse()
        .map_err(|_| format!("{name}: carrier"))
}
fn opt_parse<T: FromStr>(f: &[(String, Value)], name: &str) -> R<Option<T>> {
    match get(f, name)? {
        Value::Null => Ok(None),
        Value::Text(s) => s.parse().map(Some).map_err(|_| format!("{name}: carrier")),
        _ => Err(format!("{name}: nullable text")),
    }
}
fn items<'v>(f: &'v [(String, Value)], name: &str) -> R<&'v [Value]> {
    match get(f, name)? {
        Value::Array(a) => Ok(a),
        _ => Err(format!("{name}: array")),
    }
}
fn texts<T: FromStr>(f: &[(String, Value)], name: &str) -> R<Vec<T>> {
    items(f, name)?
        .iter()
        .map(|v| match v {
            Value::Text(s) => s.parse().map_err(|_| format!("{name}: carrier")),
            _ => Err(format!("{name}: text item")),
        })
        .collect()
}
/// A schema constant the generator types as open JSON.
fn constant(f: &[(String, Value)], name: &str) -> R<GeneratedJson> {
    Ok(match get(f, name)? {
        Value::Text(s) => GeneratedJson::String(s.clone()),
        Value::Bool(b) => GeneratedJson::Bool(*b),
        _ => return Err(format!("{name}: constant")),
    })
}

pub(crate) fn hello_ack(v: &Value) -> R<Handshake1TypeScriptHelloAckV2> {
    let f = map(v, "HelloAck")?;
    let iv = map(get(f, "identityVersions")?, "identityVersions")?;
    Ok(Handshake1TypeScriptHelloAckV2 {
        capabilities: Handshake1TypeScriptCapabilitiesV2(texts(f, "capabilities")?),
        default_work_budget_profile_id: constant(f, "defaultWorkBudgetProfileId")?,
        default_work_budget_profile_sha256: constant(f, "defaultWorkBudgetProfileSha256")?,
        identity_versions: Handshake1IdentityVersionsV1 {
            coverage: exact(iv, "coverage")?,
            fact: exact(iv, "fact")?,
            plan: exact(iv, "plan")?,
            snapshot: exact(iv, "snapshot")?,
        },
        modules_abi: parse(f, "modulesAbi")?,
        node_version: parse(f, "nodeVersion")?,
        platform_id: parse(f, "platformId")?,
        protocol_major: exact(f, "protocolMajor")?,
        provider_build_id: parse(f, "providerBuildId")?,
        provider_descriptor_sha256: Handshake1DigestHex(text(f, "providerDescriptorSha256")?),
        runtime_descriptor_sha256: Handshake1DigestHex(text(f, "runtimeDescriptorSha256")?),
        typescript_compiler_sha256: Handshake1DigestHex(text(f, "typescriptCompilerSha256")?),
        typescript_stdlib_merkle_root: Handshake1DigestHex(text(f, "typescriptStdlibMerkleRoot")?),
        typescript_version: parse(f, "typescriptVersion")?,
        v8_version: parse(f, "v8Version")?,
    })
}

pub(crate) fn universe_accepted(v: &Value) -> R<Startup1TypeScriptUniverseAcceptedV2> {
    let f = map(v, "UniverseAccepted")?;
    Ok(Startup1TypeScriptUniverseAcceptedV2 {
        execution_id: parse(f, "executionId")?,
        plan_id: parse(f, "planId")?,
        snapshot_id: parse(f, "snapshotId")?,
        universe_key: parse(f, "universeKey")?,
    })
}

pub(crate) fn snapshot_accepted(v: &Value) -> R<Ts2SnapshotAcceptedV1> {
    let f = map(v, "SnapshotAccepted")?;
    Ok(Ts2SnapshotAcceptedV1 {
        snapshot_id: text(f, "snapshotId")?,
        manifest_sha256: text(f, "manifestSha256")?,
        entry_count: unsigned(f, "entryCount")?,
        total_file_bytes: unsigned(f, "totalFileBytes")?,
        total_chunk_count: unsigned(f, "totalChunkCount")?,
    })
}

pub(crate) fn native_context_verified(v: &Value) -> R<Startup1NativeContextVerifiedV1> {
    let f = map(v, "NativeContextVerified")?;
    Ok(Startup1NativeContextVerifiedV1 {
        equal: constant(f, "equal")?,
        native_context_id: parse(f, "nativeContextId")?,
        recomputed_native_context_id: parse(f, "recomputedNativeContextId")?,
    })
}

pub(crate) fn pre_analyze_unavailable(v: &Value) -> R<Startup1PreAnalyzeUnavailableV1> {
    let f = map(v, "Unavailable")?;
    Ok(Startup1PreAnalyzeUnavailableV1 {
        execution_id: parse(f, "executionId")?,
        native_context_id: parse(f, "nativeContextId")?,
        plan_id: parse(f, "planId")?,
        reason: constant(f, "reason")?,
        recomputed_native_context_id: parse(f, "recomputedNativeContextId")?,
        snapshot_id: parse(f, "snapshotId")?,
    })
}

fn anchor(v: &Value) -> R<Ts2AnchorRefV1> {
    let f = map(v, "anchor")?;
    match text(f, "kind")?.as_str() {
        "source-span" => Ok(Ts2AnchorRefV1::SourceSpan {
            snapshot_id: text(f, "snapshotId")?,
            path: text(f, "path")?,
            content_sha256: text(f, "contentSha256")?,
            start_byte: unsigned(f, "startByte")?,
            end_byte: unsigned(f, "endByte")?,
            fact_id: (),
        }),
        "fact-ref" => Ok(Ts2AnchorRefV1::FactRef {
            snapshot_id: (),
            path: (),
            content_sha256: (),
            start_byte: (),
            end_byte: (),
            fact_id: text(f, "factId")?,
        }),
        k => Err(format!("anchor kind {k}")),
    }
}

pub(crate) fn candidate(v: &Value) -> R<Ts2FactCandidateV1> {
    let f = map(v, "candidate")?;
    let Value::Bytes(payload) = get(f, "canonicalRelationPayload")? else {
        return Err("canonicalRelationPayload".to_owned());
    };
    Ok(Ts2FactCandidateV1 {
        candidate_ordinal: unsigned(f, "candidateOrdinal")?,
        relation: parse(f, "relation")?,
        resolution: parse(f, "resolution")?,
        layer: match text(f, "layer")?.as_str() {
            "derived" => Ts2FactCandidateV1Field3Value::Derived,
            "inventory" => Ts2FactCandidateV1Field3Value::Inventory,
            "semantic" => Ts2FactCandidateV1Field3Value::Semantic,
            "syntax" => Ts2FactCandidateV1Field3Value::Syntax,
            l => return Err(format!("layer {l}")),
        },
        producer: match text(f, "producer")?.as_str() {
            "typescript-semantic" => Ts2FactCandidateV1Field4Value::TypescriptSemantic,
            p => return Err(format!("producer {p}")),
        },
        producer_version: text(f, "producerVersion")?,
        schema_version: unsigned(f, "schemaVersion")?,
        language: match text(f, "language")?.as_str() {
            "typescript" => Ts2FactCandidateV1Field7Value::Typescript,
            l => return Err(format!("language {l}")),
        },
        source_universe_id: text(f, "sourceUniverseId")?,
        target_universe_id: text(f, "targetUniverseId")?,
        confidence_millionths: unsigned(f, "confidenceMillionths")?,
        relation_schema_id: text(f, "relationSchemaId")?,
        canonical_relation_payload: ByteString::from_vec(payload.clone()),
        anchors: items(f, "anchors")?.iter().map(anchor).collect::<R<_>>()?,
    })
}

fn occupancy(v: &Value) -> R<Occupancy1Root> {
    let f = map(v, "occupancyCompanion")?;
    Ok(Occupancy1Root {
        candidate_ordinal: unsigned(f, "candidateOrdinal")?,
        evaluation_native_id: opt_parse(f, "evaluationNativeId")?,
        exported: opt_parse(f, "exported")?,
        kind: parse(f, "kind")?,
        logical_path: opt_parse(f, "logicalPath")?,
        occupancy: parse(f, "occupancy")?,
        package_manifest_path: opt_parse(f, "packageManifestPath")?,
        schema_version: exact(f, "schemaVersion")?,
        target_native_id: parse(f, "targetNativeId")?,
        target_universe_id: parse(f, "targetUniverseId")?,
    })
}

pub(crate) fn fact_batch_v1(v: &Value) -> R<Ts2FactBatchV1> {
    let f = map(v, "FactBatch")?;
    Ok(Ts2FactBatchV1 {
        analysis_ordinal: unsigned(f, "analysisOrdinal")?,
        stage_id: text(f, "stageId")?,
        batch_index: unsigned(f, "batchIndex")?,
        facts: items(f, "facts")?.iter().map(candidate).collect::<R<_>>()?,
        batch_commitment: text(f, "batchCommitment")?,
    })
}

pub(crate) fn fact_batch_v3(v: &Value) -> R<Ts2FactBatchV3> {
    let f = map(v, "FactBatch")?;
    Ok(Ts2FactBatchV3 {
        schema_version: unsigned(f, "schemaVersion")?,
        analysis_ordinal: unsigned(f, "analysisOrdinal")?,
        stage_id: text(f, "stageId")?,
        batch_index: unsigned(f, "batchIndex")?,
        candidates: items(f, "candidates")?
            .iter()
            .map(candidate)
            .collect::<R<_>>()?,
        occupancy_companions: items(f, "occupancyCompanions")?
            .iter()
            .map(occupancy)
            .collect::<R<_>>()?,
    })
}

fn bools(f: &[(String, Value)], name: &str) -> R<bool> {
    match get(f, name)? {
        Value::Bool(b) => Ok(*b),
        _ => Err(format!("{name}: bool")),
    }
}

fn coverage_result(v: &Value) -> R<Native2CoverageResultV3> {
    let f = map(v, "CoverageResultV3")?;
    let k = map(get(f, "key")?, "key")?;
    let e = map(get(f, "entry")?, "entry")?;
    let cw = map(get(e, "closedWorld")?, "closedWorld")?;
    let eu = map(get(e, "examinedUniverse")?, "examinedUniverse")?;
    let rc = map(get(e, "resolutionCompleteness")?, "resolutionCompleteness")?;
    let Value::Unsigned(confidence) = get(e, "confidenceMillionths")? else {
        return Err("confidenceMillionths".to_owned());
    };
    Ok(Native2CoverageResultV3 {
        entry: Native2ViewEntryV3 {
            closed_world: Native2ClosedWorldV2 {
                dead_code_repair_eligible: bools(cw, "deadCodeRepairEligible")?,
                dynamic_dispatch: parse(cw, "dynamicDispatch")?,
                entry_points_recognized: parse(cw, "entryPointsRecognized")?,
                exports_closed: parse(cw, "exportsClosed")?,
                external_consumers: parse(cw, "externalConsumers")?,
                nonliteral_loading: parse(cw, "nonliteralLoading")?,
                reasons: texts(cw, "reasons")?,
            },
            confidence_millionths: i64::try_from(*confidence)
                .map_err(|_| "confidenceMillionths")?,
            coverage: parse(e, "coverage")?,
            deficiency: opt_parse(e, "deficiency")?,
            derivation_kinds: texts(e, "derivationKinds")?,
            examined_universe: Native2ExaminedUniverseV1 {
                subject_count: unsigned(eu, "subjectCount")?,
                subject_scope_commitment: text(eu, "subjectScopeCommitment")?,
            },
            native_cause: opt_parse(e, "nativeCause")?,
            relation: parse(e, "relation")?,
            resolution: parse(e, "resolution")?,
            resolution_completeness: Native2ResolutionCompletenessV2 {
                attempted: bools(rc, "attempted")?,
                examined_exhaustive: bools(rc, "examinedExhaustive")?,
                stage_terminal: opt_parse(rc, "stageTerminal")?,
                state: parse(rc, "state")?,
                unresolved_edge_classes: texts(rc, "unresolvedEdgeClasses")?,
                unresolved_edge_count: unsigned(rc, "unresolvedEdgeCount")?,
            },
        },
        key: Native2CoverageKeyV2 {
            relation: parse(k, "relation")?,
            resolution: parse(k, "resolution")?,
            source_universe: text(k, "sourceUniverse")?,
            subject_scope_commitment: text(k, "subjectScopeCommitment")?,
            target_universe: text(k, "targetUniverse")?,
        },
        schema_version: exact(f, "schemaVersion")?,
    })
}

pub(crate) fn coverage(v: &Value) -> R<Startup1TypeScriptCoverageV2> {
    let f = map(v, "Coverage")?;
    Ok(Startup1TypeScriptCoverageV2 {
        analysis_ordinal: exact(f, "analysisOrdinal")?,
        coverage_commitment: parse(f, "coverageCommitment")?,
        entries: items(f, "entries")?
            .iter()
            .map(coverage_result)
            .collect::<R<_>>()?,
        stage_id: parse(f, "stageId")?,
    })
}

pub(crate) fn post_analyze_unavailable(v: &Value) -> R<Startup1TypeScriptUnavailableV2> {
    let f = map(v, "Unavailable")?;
    Ok(Startup1TypeScriptUnavailableV2 {
        affected_stage_ids: texts(f, "affectedStageIds")?,
        analysis_ordinal: exact(f, "analysisOrdinal")?,
        coverage: items(f, "coverage")?
            .iter()
            .map(coverage_result)
            .collect::<R<_>>()?,
        coverage_commitment: parse(f, "coverageCommitment")?,
        reason: parse(f, "reason")?,
    })
}

pub(crate) fn budget_exhausted(v: &Value) -> R<Startup1TypeScriptBudgetExhaustedV2> {
    let f = map(v, "BudgetExhausted")?;
    Ok(Startup1TypeScriptBudgetExhaustedV2 {
        analysis_ordinal: exact(f, "analysisOrdinal")?,
        coverage: items(f, "coverage")?
            .iter()
            .map(coverage_result)
            .collect::<R<_>>()?,
        coverage_commitment: parse(f, "coverageCommitment")?,
        dimension: parse(f, "dimension")?,
        limit: Startup1Uint64(unsigned(f, "limit")?),
        observed: Startup1Uint64(unsigned(f, "observed")?),
        trigger_stage_id: parse(f, "triggerStageId")?,
    })
}

pub(crate) fn complete(v: &Value) -> R<Ts2CompleteV1> {
    let f = map(v, "Complete")?;
    let stage = |v: &Value| -> R<Ts2StageResultV1> {
        let s = map(v, "stageResult")?;
        Ok(Ts2StageResultV1 {
            stage_id: text(s, "stageId")?,
            stage_ordinal: unsigned(s, "stageOrdinal")?,
            fact_batch_count: unsigned(s, "factBatchCount")?,
            fact_count: unsigned(s, "factCount")?,
            coverage_entry_count: unsigned(s, "coverageEntryCount")?,
            fact_commitment: text(s, "factCommitment")?,
            coverage_commitment: text(s, "coverageCommitment")?,
        })
    };
    Ok(Ts2CompleteV1 {
        analysis_ordinal: unsigned(f, "analysisOrdinal")?,
        stage_results: items(f, "stageResults")?
            .iter()
            .map(stage)
            .collect::<R<_>>()?,
        fact_stream_commitment: text(f, "factStreamCommitment")?,
        coverage_stream_commitment: text(f, "coverageStreamCommitment")?,
    })
}

pub(crate) fn cancelled(v: &Value) -> R<Ts2CancelledV1> {
    let f = map(v, "Cancelled")?;
    let ordinal = match get(f, "analysisOrdinal")? {
        Value::Null => None,
        Value::Unsigned(n) => Some(*n),
        _ => return Err("analysisOrdinal".to_owned()),
    };
    let execution = match get(f, "executionId")? {
        Value::Null => None,
        Value::Text(s) => Some(s.clone()),
        _ => return Err("executionId".to_owned()),
    };
    Ok(Ts2CancelledV1 {
        execution_id: execution,
        analysis_ordinal: ordinal,
        observed_phase: match text(f, "observedPhase")?.as_str() {
            "analysis" => Ts2CancelledV1Field2Value::Analysis,
            "handshake" => Ts2CancelledV1Field2Value::Handshake,
            "snapshot" => Ts2CancelledV1Field2Value::Snapshot,
            "universe" => Ts2CancelledV1Field2Value::Universe,
            p => return Err(format!("observedPhase {p}")),
        },
    })
}
