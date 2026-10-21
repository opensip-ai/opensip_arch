//! Hand conversion AFTER Rust3 envelope, schema, contextual admission and
//! table matching. No serde deserializer is applied to a wire value/byte.
use super::super::{
    cbor::Value,
    ts2::{build as common, carrier::field},
};
use opensip_contracts::{
    GeneratedJson,
    generated::{evidence::*, protocol::*},
};
use std::str::FromStr;
type R<T> = Result<T, String>;
fn map<'v>(v: &'v Value, at: &str) -> R<&'v [(String, Value)]> {
    match v {
        Value::Map(f) => Ok(f),
        _ => Err(format!("{at}: map")),
    }
}
fn get<'v>(f: &'v [(String, Value)], key: &str) -> R<&'v Value> {
    field(f, key).ok_or_else(|| format!("missing {key}"))
}
fn text(f: &[(String, Value)], key: &str) -> R<String> {
    match get(f, key)? {
        Value::Text(s) => Ok(s.clone()),
        _ => Err(format!("{key}: text")),
    }
}
fn unsigned(f: &[(String, Value)], key: &str) -> R<u64> {
    match get(f, key)? {
        Value::Unsigned(n) => Ok(*n),
        _ => Err(format!("{key}: uint64")),
    }
}
#[allow(
    clippy::unnecessary_fallible_conversions,
    reason = "infallible From would add an identity mint-census call"
)]
fn exact(f: &[(String, Value)], key: &str) -> R<ExactInteger> {
    ExactInteger::try_from(unsigned(f, key)?).map_err(|_| format!("{key}: integer"))
}
fn bools(f: &[(String, Value)], key: &str) -> R<bool> {
    match get(f, key)? {
        Value::Bool(x) => Ok(*x),
        _ => Err(format!("{key}: bool")),
    }
}
fn parse<T: FromStr>(f: &[(String, Value)], key: &str) -> R<T> {
    text(f, key)?.parse().map_err(|_| format!("{key}: carrier"))
}
fn optional<T: FromStr>(f: &[(String, Value)], key: &str) -> R<Option<T>> {
    match get(f, key)? {
        Value::Null => Ok(None),
        Value::Text(s) => s
            .parse()
            .map(Some)
            .map_err(|_| format!("{key}: nullable carrier")),
        _ => Err(format!("{key}: nullable text")),
    }
}
fn items<'v>(f: &'v [(String, Value)], key: &str) -> R<&'v [Value]> {
    match get(f, key)? {
        Value::Array(xs) => Ok(xs),
        _ => Err(format!("{key}: array")),
    }
}
fn texts<T: FromStr>(f: &[(String, Value)], key: &str) -> R<Vec<T>> {
    items(f, key)?
        .iter()
        .map(|v| match v {
            Value::Text(s) => s.parse().map_err(|_| format!("{key}: carrier")),
            _ => Err(format!("{key}: text item")),
        })
        .collect()
}
// Only schema-constant primitive members are open JSON in these generated
// types. This constructs inert data directly; no serde decoder is involved.
fn constant(f: &[(String, Value)], key: &str) -> R<GeneratedJson> {
    Ok(match get(f, key)? {
        Value::Text(s) => GeneratedJson::String(s.clone()),
        Value::Bool(x) => GeneratedJson::Bool(*x),
        _ => return Err(format!("{key}: primitive constant")),
    })
}
fn effect(v: &Value) -> R<Native2EffectV1> {
    let f = map(v, "effect")?;
    Ok(Native2EffectV1 {
        enforcement: parse(f, "enforcement")?,
        requested: parse(f, "requested")?,
    })
}
fn repository(v: &Value) -> R<Native2RepositoryResolutionV3> {
    let f = map(v, "repositoryResolution")?;
    let effects = match get(f, "effects")? {
        Value::Null => None,
        v => {
            let e = map(v, "effects")?;
            Some(Native2RepositoryResolutionV3Effects {
                environment: effect(get(e, "environment")?)?,
                filesystem_write: effect(get(e, "filesystemWrite")?)?,
                network: effect(get(e, "network")?)?,
                subprocess: effect(get(e, "subprocess")?)?,
            })
        }
    };
    Ok(Native2RepositoryResolutionV3 {
        authorization_id: optional(f, "authorizationId")?,
        dependency_source_set_id: text(f, "dependencySourceSetId")?,
        effects,
        prepared_output_set_id: optional(f, "preparedOutputSetId")?,
        worker_executes_repository_code: constant(f, "workerExecutesRepositoryCode")?,
    })
}
fn resolved(v: &Value) -> R<Native2RustUniverseV2ResolvedInputs> {
    let f = map(v, "resolvedInputs")?;
    let lock = map(get(f, "lockfileIdentity")?, "lockfileIdentity")?;
    let flags = map(get(f, "rustflags")?, "rustflags")?;
    let cfg_sets = items(f, "cfgSets")?
        .iter()
        .map(|v| {
            let x = map(v, "cfgSet")?;
            Ok(Native2RustUniverseV2ResolvedInputsCfgSetsItem {
                cfg: texts(x, "cfg")?,
                cfg_set_id: parse(x, "cfgSetId")?,
            })
        })
        .collect::<R<_>>()?;
    let edition = map(get(f, "edition")?, "edition")?
        .iter()
        .map(|(k, v)| {
            let Value::Unsigned(n) = v else {
                return Err("edition: uint64".to_owned());
            };
            #[allow(
                clippy::unnecessary_fallible_conversions,
                reason = "preserve identity mint census"
            )]
            let n = ExactInteger::try_from(*n).map_err(|_| "edition")?;
            Ok((k.clone(), n))
        })
        .collect::<R<_>>()?;
    let stripped = items(flags, "stripped")?
        .iter()
        .map(|v| {
            let x = map(v, "stripped")?;
            Ok(Native2RustflagsProjectionV1StrippedItem {
                flag: parse(x, "flag")?,
                reason: parse(x, "reason")?,
            })
        })
        .collect::<R<_>>()?;
    Ok(Native2RustUniverseV2ResolvedInputs {
        cfg_sets,
        config_projection_sha256: text(f, "configProjectionSha256")?,
        crate_root_paths: texts(f, "crateRootPaths")?,
        dependency_source_set_id: text(f, "dependencySourceSetId")?,
        edition,
        execution_capable_resolution: bools(f, "executionCapableResolution")?,
        lockfile_identity: Native2LockfileIdentityV1 {
            content_sha256: text(lock, "contentSha256")?,
            lockfile_version: exact(lock, "lockfileVersion")?,
            path: constant(lock, "path")?,
        },
        native_context_id: text(f, "nativeContextId")?,
        prepared_output_set_id: optional(f, "preparedOutputSetId")?,
        prepared_resolution: parse(f, "preparedResolution")?,
        rustflags: Native2RustflagsProjectionV1 {
            executable_selected: constant(flags, "executableSelected")?,
            honored: texts(flags, "honored")?,
            stripped,
        },
        schema_version: exact(f, "schemaVersion")?,
        source_unit_ownership_id: optional(f, "sourceUnitOwnershipId")?,
        unified_features_id: text(f, "unifiedFeaturesId")?,
    })
}
fn universe(v: &Value) -> R<Startup1RustSemanticUniverseV2> {
    let f = map(v, "universe")?;
    let standard_library_component_digests = map(
        get(f, "standardLibraryComponentDigests")?,
        "standardLibraryComponentDigests",
    )?
    .iter()
    .map(|(key, value)| {
        let Value::Text(s) = value else {
            return Err("component digest".to_owned());
        };
        Ok((key.clone(), Startup1DigestHex(s.clone())))
    })
    .collect::<R<_>>()?;
    Ok(Startup1RustSemanticUniverseV2 {
        capability_manifest_id: parse(f, "capabilityManifestId")?,
        cargo_version: parse(f, "cargoVersion")?,
        host_triple: parse(f, "hostTriple")?,
        license_notice_bundle_sha256: parse(f, "licenseNoticeBundleSha256")?,
        manifest_id: parse(f, "manifestId")?,
        platform_id: parse(f, "platformId")?,
        protocol_major: exact(f, "protocolMajor")?,
        provider_artifact_id: constant(f, "providerArtifactId")?,
        provider_artifact_sha256: parse(f, "providerArtifactSha256")?,
        provider_binary_sha256: parse(f, "providerBinarySha256")?,
        provider_build_id: parse(f, "providerBuildId")?,
        resolved_inputs: resolved(get(f, "resolvedInputs")?)?,
        rust_commit_hash: text(f, "rustCommitHash")?,
        rustc_dev_llvm_digest: parse(f, "rustcDevLlvmDigest")?,
        rustc_version: parse(f, "rustcVersion")?,
        schema_version: exact(f, "schemaVersion")?,
        standard_library_component_digests,
        sysroot_digest: parse(f, "sysrootDigest")?,
        target_triple: parse(f, "targetTriple")?,
        toolchain_artifact_id: constant(f, "toolchainArtifactId")?,
        toolchain_artifact_sha256: parse(f, "toolchainArtifactSha256")?,
    })
}
fn anchor(v: &Value) -> R<Rust3AnchorRefV1> {
    let f = map(v, "anchor")?;
    if text(f, "kind")? != "source-span" {
        return Err("unadmitted anchor kind".to_owned());
    }
    Ok(Rust3AnchorRefV1::SourceSpan {
        snapshot_id: parse(f, "snapshotId")?,
        path: parse(f, "path")?,
        content_sha256: parse(f, "contentSha256")?,
        start_byte: unsigned(f, "startByte")?,
        end_byte: unsigned(f, "endByte")?,
        fact_id: (),
    })
}
fn candidate(v: &Value) -> R<Rust3FactCandidateV1> {
    let f = map(v, "candidate")?;
    let Value::Bytes(payload) = get(f, "canonicalRelationPayload")? else {
        return Err("canonicalRelationPayload".to_owned());
    };
    Ok(Rust3FactCandidateV1 {
        candidate_ordinal: unsigned(f, "candidateOrdinal")?,
        relation: parse(f, "relation")?,
        resolution: parse(f, "resolution")?,
        layer: match text(f, "layer")?.as_str() {
            "derived" => Rust3FactCandidateV1Field3Value::Derived,
            "inventory" => Rust3FactCandidateV1Field3Value::Inventory,
            "semantic" => Rust3FactCandidateV1Field3Value::Semantic,
            "syntax" => Rust3FactCandidateV1Field3Value::Syntax,
            _ => return Err("layer".to_owned()),
        },
        producer: match text(f, "producer")?.as_str() {
            "rust-semantic" => Rust3FactCandidateV1Field4Value::RustSemantic,
            _ => return Err("producer".to_owned()),
        },
        producer_version: parse(f, "producerVersion")?,
        schema_version: unsigned(f, "schemaVersion")?,
        language: match text(f, "language")?.as_str() {
            "rust" => Rust3FactCandidateV1Field7Value::Rust,
            _ => return Err("language".to_owned()),
        },
        source_universe_id: parse(f, "sourceUniverseId")?,
        target_universe_id: parse(f, "targetUniverseId")?,
        confidence_millionths: unsigned(f, "confidenceMillionths")?,
        relation_schema_id: text(f, "relationSchemaId")?,
        canonical_relation_payload: ByteString::from_vec(payload.clone()),
        anchors: items(f, "anchors")?.iter().map(anchor).collect::<R<_>>()?,
    })
}
macro_rules! phase {
    ($f:expr,$key:literal,$ty:ident) => {
        match text($f, $key)?.as_str() {
            "ANALYZING" => $ty::ANALYZING,
            "READY_ANALYZE" => $ty::READYANALYZE,
            "READY_COMPLETE" => $ty::READYCOMPLETE,
            "READY_DEPENDENCY_MANIFEST" => $ty::READYDEPENDENCYMANIFEST,
            "READY_OPEN_UNIVERSE" => $ty::READYOPENUNIVERSE,
            "READY_PREPARED_MANIFEST" => $ty::READYPREPAREDMANIFEST,
            "READY_SNAPSHOT_MANIFEST" => $ty::READYSNAPSHOTMANIFEST,
            "RECEIVING_DEPENDENCY" => $ty::RECEIVINGDEPENDENCY,
            "RECEIVING_PREPARED" => $ty::RECEIVINGPREPARED,
            "RECEIVING_SNAPSHOT" => $ty::RECEIVINGSNAPSHOT,
            "WAIT_DEPENDENCY_ACCEPTED" => $ty::WAITDEPENDENCYACCEPTED,
            "WAIT_HELLO_ACK" => $ty::WAITHELLOACK,
            "WAIT_NATIVE_CONTEXT_VERIFIED" => $ty::WAITNATIVECONTEXTVERIFIED,
            "WAIT_PREPARED_ACCEPTED" => $ty::WAITPREPAREDACCEPTED,
            "WAIT_SNAPSHOT_ACCEPTED" => $ty::WAITSNAPSHOTACCEPTED,
            "WAIT_UNIVERSE_ACCEPTED" => $ty::WAITUNIVERSEACCEPTED,
            _ => return Err(format!("{}: phase", $key)),
        }
    };
}
pub(super) fn convert(
    name: &str,
    value: &Value,
    target_attribution: bool,
    host_phase: &str,
) -> R<Rust3ProviderFrameV3Payload> {
    let f = map(value, name)?;
    use Rust3ProviderFrameV3Payload as P;
    Ok(match name {
        "HelloAck" => {
            let iv = map(get(f, "identityVersions")?, "identityVersions")?;
            P::HelloAck(Box::new(Handshake1HelloAckV3 {
                capabilities: Handshake1RustCapabilitiesV3(texts(f, "capabilities")?),
                host_triple: parse(f, "hostTriple")?,
                identity_versions: Handshake1IdentityVersionsV1 {
                    coverage: exact(iv, "coverage")?,
                    fact: exact(iv, "fact")?,
                    plan: exact(iv, "plan")?,
                    snapshot: exact(iv, "snapshot")?,
                },
                protocol_major: exact(f, "protocolMajor")?,
                provider_build_id: parse(f, "providerBuildId")?,
                rust_commit_hash: text(f, "rustCommitHash")?,
                sysroot_digest: parse(f, "sysrootDigest")?,
                target_triple: parse(f, "targetTriple")?,
            }))
        }
        "UniverseAccepted" => P::UniverseAccepted(Box::new(Startup1UniverseAcceptedV3 {
            execution_id: parse(f, "executionId")?,
            plan_id: parse(f, "planId")?,
            provider_id: constant(f, "providerId")?,
            repository_resolution: repository(get(f, "repositoryResolution")?)?,
            snapshot_id: parse(f, "snapshotId")?,
            universe: universe(get(f, "universe")?)?,
        })),
        "SnapshotAccepted" => P::SnapshotAccepted(Box::new(Rust3SnapshotAcceptedV2 {
            snapshot_id: parse(f, "snapshotId")?,
            manifest_sha256: parse(f, "manifestSha256")?,
            entry_count: unsigned(f, "entryCount")?,
            total_file_bytes: unsigned(f, "totalFileBytes")?,
            total_chunk_count: unsigned(f, "totalChunkCount")?,
        })),
        "DependencySourceAccepted" => {
            P::DependencySourceAccepted(Box::new(Native2DependencySourceSealV3 {
                dependency_source_set_id: text(f, "dependencySourceSetId")?,
                entry_count: unsigned(f, "entryCount")?,
                manifest_sha256: text(f, "manifestSha256")?,
                total_bytes: unsigned(f, "totalBytes")?,
                total_chunk_count: unsigned(f, "totalChunkCount")?,
            }))
        }
        "PreparedOutputAccepted" => {
            P::PreparedOutputAccepted(Box::new(Rust3PreparedOutputAcceptedV3 {
                plan_id: parse(f, "planId")?,
                manifest_sha256: parse(f, "manifestSha256")?,
                entry_count: unsigned(f, "entryCount")?,
                total_blob_bytes: unsigned(f, "totalBlobBytes")?,
                total_chunk_count: unsigned(f, "totalChunkCount")?,
            }))
        }
        "NativeContextVerified" => {
            P::NativeContextVerified(Box::new(common::native_context_verified(value)?))
        }
        "FactBatch" if target_attribution => P::FactBatch1(Box::new(Rust3FactBatchV3 {
            schema_version: unsigned(f, "schemaVersion")?,
            analysis_ordinal: unsigned(f, "analysisOrdinal")?,
            stage_id: parse(f, "stageId")?,
            batch_index: unsigned(f, "batchIndex")?,
            candidates: items(f, "candidates")?
                .iter()
                .map(candidate)
                .collect::<R<_>>()?,
            occupancy_companions: items(f, "occupancyCompanions")?
                .iter()
                .map(common::occupancy)
                .collect::<R<_>>()?,
        })),
        "FactBatch" => P::FactBatch0(Box::new(Rust3FactBatchV2 {
            analysis_ordinal: unsigned(f, "analysisOrdinal")?,
            stage_id: parse(f, "stageId")?,
            batch_index: unsigned(f, "batchIndex")?,
            candidates: items(f, "candidates")?
                .iter()
                .map(candidate)
                .collect::<R<_>>()?,
        })),
        "CoverageV3" => P::CoverageV3(Box::new(Startup1CoverageV3 {
            analysis_ordinal: Startup1Uint64(unsigned(f, "analysisOrdinal")?),
            coverage_commitment: parse(f, "coverageCommitment")?,
            entries: items(f, "entries")?
                .iter()
                .map(common::coverage_result)
                .collect::<R<_>>()?,
            stage_id: parse(f, "stageId")?,
        })),
        "Unavailable" if host_phase == "WAIT_NATIVE_CONTEXT_VERIFIED" => {
            P::Unavailable0(Box::new(common::pre_analyze_unavailable(value)?))
        }
        "Unavailable" => P::Unavailable1(Box::new(Startup1UnavailableV3 {
            affected_stage_ids: texts(f, "affectedStageIds")?,
            analysis_ordinal: Startup1Uint64(unsigned(f, "analysisOrdinal")?),
            coverage: items(f, "coverage")?
                .iter()
                .map(common::coverage_result)
                .collect::<R<_>>()?,
            coverage_commitment: parse(f, "coverageCommitment")?,
            reason: parse(f, "reason")?,
        })),
        "BudgetExhausted" => P::BudgetExhausted(Box::new(Startup1BudgetExhaustedV3 {
            analysis_ordinal: Startup1Uint64(unsigned(f, "analysisOrdinal")?),
            coverage: items(f, "coverage")?
                .iter()
                .map(common::coverage_result)
                .collect::<R<_>>()?,
            coverage_commitment: parse(f, "coverageCommitment")?,
            limit: Startup1Uint64(unsigned(f, "limit")?),
            observed: Startup1Uint64(unsigned(f, "observed")?),
            trigger_stage_id: parse(f, "triggerStageId")?,
            unit: parse(f, "unit")?,
        })),
        "Complete" => {
            let stage_results = items(f, "stageResults")?
                .iter()
                .map(|v| {
                    let r = map(v, "stageResult")?;
                    Ok(Rust3StageResultV2 {
                        stage_id: parse(r, "stageId")?,
                        fact_count: unsigned(r, "factCount")?,
                        coverage_entry_count: unsigned(r, "coverageEntryCount")?,
                        fact_commitment: parse(r, "factCommitment")?,
                        coverage_commitment: parse(r, "coverageCommitment")?,
                    })
                })
                .collect::<R<_>>()?;
            P::Complete(Box::new(Rust3CompleteV2 {
                analysis_ordinal: unsigned(f, "analysisOrdinal")?,
                stage_results,
                fact_stream_commitment: parse(f, "factStreamCommitment")?,
                coverage_stream_commitment: parse(f, "coverageStreamCommitment")?,
            }))
        }
        "ProviderFault" => P::ProviderFault(Box::new(Rust3ProviderFaultV2 {
            execution_id: optional(f, "executionId")?,
            analysis_ordinal: match get(f, "analysisOrdinal")? {
                Value::Null => None,
                Value::Unsigned(n) => Some(*n),
                _ => return Err("analysisOrdinal".to_owned()),
            },
            phase: phase!(f, "phase", Rust3ProviderFaultV2Field2Value),
            fault_kind: match text(f, "faultKind")?.as_str() {
                "compiler-crash" => Rust3ProviderFaultV2Field3Value::CompilerCrash,
                "input-rejected" => Rust3ProviderFaultV2Field3Value::InputRejected,
                "internal-invariant" => Rust3ProviderFaultV2Field3Value::InternalInvariant,
                _ => return Err("faultKind".to_owned()),
            },
            detail_code: parse(f, "detailCode")?,
        })),
        "Cancelled" => P::Cancelled(Box::new(Rust3CancelledV2 {
            execution_id: optional(f, "executionId")?,
            analysis_ordinal: match get(f, "analysisOrdinal")? {
                Value::Null => None,
                Value::Unsigned(n) => Some(*n),
                _ => return Err("analysisOrdinal".to_owned()),
            },
            observed_phase: phase!(f, "observedPhase", Rust3CancelledV2Field2Value),
        })),
        _ => return Err(format!("no worker conversion for {name}")),
    })
}
