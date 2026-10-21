//! Synthetic pre-C4 public wire inputs. The recipe matches D2b's public
//! sender controls; descriptor authorities are separate literal projections.
use super::*;
use opensip_components::provider_protocol::{cbor::Value, ts2::*};
use opensip_identity::{JsonValue as J, digest_hex as hex};
use std::collections::{BTreeMap, BTreeSet};
#[path = "../tests/support/factory_ts2.rs"]
mod descriptors;
const MIB: u64 = 1_048_576;
const BUILD: &str = "typescript-provider 1.0.0";
const EXEC: &str = "exec1_0123456789abcdef0123456789abcdef";
const PATH: &str = "src/a.ts";
const TOKENS: [&str; 4] = [
    "coverage-v3",
    "fact-identity-fact2",
    "plan-identity-plan2",
    "source-identity-snapshot2",
];
fn h(c: char) -> String {
    c.to_string().repeat(64)
}
fn sha(c: char) -> String {
    format!("sha256:{}", h(c))
}
fn t(v: &str) -> Value {
    Value::Text(v.into())
}
fn get<'a>(v: &'a Value, k: &str) -> &'a Value {
    let Value::Map(rows) = v else { panic!("map") };
    &rows.iter().find(|(n, _)| n == k).unwrap().1
}
fn stage(r: &Ts2Request, i: usize) -> &Value {
    let Value::Array(rows) = get(r.analyze(), "stageRequests") else {
        panic!("stages")
    };
    &rows[i]
}
fn universe() -> J {
    parse_json(
        format!(
            r#"{{"schemaVersion":1,"manifestId":"{h1}","capabilityManifestId":"{h2}",
            "runtimeArtifactId":"typescript-runtime","runtimeArtifactSha256":"{h3}",
            "providerArtifactId":"typescript-provider","providerArtifactSha256":"{h4}",
            "runtimeDescriptorSha256":"{h4}","providerDescriptorSha256":"{h3}","protocolMajor":2,
            "providerBuildId":"{BUILD}","nodeVersion":"24.16.0","v8Version":"13.6","modulesAbi":"137",
            "typescriptVersion":"5.9.2","typescriptCompilerSha256":"{h1}","typescriptStdlibMerkleRoot":"{h2}",
            "platformId":"darwin-arm64","resolvedInputs":{{"schemaVersion":2,"languageMode":"ts-tsconfig",
            "configOrigin":"tsconfig","synthesizerVersion":null,"synthesizedOptions":null,
            "packageModuleType":"module","allowJs":false,"checkJs":false,"jsAdmittedToProgram":false,
            "jsDiagnosticsEnabled":false,"resolutionCompletenessImplied":false,"jsRootFiles":[],
            "programRootFiles":["src/a.ts"],"lockfileKind":"none","nodeModulesInReadSet":false,
            "executionCapableResolution":false,"tsconfigGraphHash":"{h2}","nativeContextId":"{s9}"}}}}"#,
            h1 = h('1'),
            h2 = h('2'),
            h3 = h('3'),
            h4 = h('4'),
            s9 = sha('9'),
        )
        .as_bytes(),
    )
    .unwrap()
}

fn content(path: &str, length: u64) -> Vec<u8> {
    let salt = path.bytes().fold(0u8, |s, b| s.wrapping_add(b));
    (0..length).map(|i| (i % 251) as u8 ^ salt).collect()
}
fn file(path: &str, length: u64) -> SnapshotEntry {
    SnapshotEntry::File {
        path: path.to_owned(),
        byte_length: length,
        content_sha256: hex(&raw_sha256(&content(path, length))),
    }
}
/// DLV `budgetProjection.absent.output`: the signed default profile.
fn default_budget() -> BTreeMap<String, u64> {
    BTreeMap::from_iter(
        [
            ("sourceFilesVisited", 200_000u64),
            ("astNodesVisited", 50_000_000),
            ("moduleResolutionQueries", 1_000_000),
            ("typeQueries", 5_000_000),
            ("factsEmitted", 1_000_000),
            ("factBytesEmitted", 1_073_741_824),
        ]
        .map(|(k, v)| (k.to_owned(), v)),
    )
}
fn plan() -> Ts2Plan {
    let key = |c: char| RequestedKey {
        relation: "calls".to_owned(),
        resolution: "syntactic-callee-name".to_owned(),
        source_universe_id: sha('5'),
        target_universe_id: sha('6'),
        subject_scope_commitment: sha(c),
    };
    Ts2Plan {
        host_build_id: "opensip-host 1.0.0".to_owned(),
        expected_provider_descriptor_sha256: h('3'),
        expected_runtime_descriptor_sha256: h('4'),
        capabilities: TOKENS.iter().map(|s| (*s).to_owned()).collect(),
        provider_build_id: BUILD.to_owned(),
        execution_id: EXEC.to_owned(),
        snapshot_id: format!("snapshot2:{}", h('7')),
        plan_id: format!("plan2:{}", h('8')),
        plan_intent_commitment: sha('e'),
        universe: universe(),
        entries: vec![
            file("src/a.ts", 2 * MIB + 5),
            file("src/b.ts", 0),
            SnapshotEntry::Symlink {
                path: "src/c.ts".to_owned(),
                link_target: "a.ts".to_owned(),
            },
            file("src/d.ts", 100),
        ],
        stages: vec![
            StagePlan {
                stage_id: "stage-one".to_owned(),
                depends_on: None,
                relations: vec!["calls".to_owned()],
                budget: StageBudget::Absent,
                keys: vec![key('c')],
            },
            StagePlan {
                stage_id: "stage-two".to_owned(),
                depends_on: Some(vec!["stage-one".to_owned()]),
                relations: vec!["calls".to_owned()],
                budget: StageBudget::WorkUnits(7),
                keys: vec![key('d')],
            },
        ],
        default_budget: default_budget(),
        symbol_census: None,
    }
}
fn context(tokens: &[&str]) -> DispatchContext {
    let provider = descriptors::provider();
    let runtime = descriptors::runtime();
    let budget = BTreeMap::from_iter(
        [
            "sourceFilesVisited",
            "astNodesVisited",
            "moduleResolutionQueries",
            "typeQueries",
            "factsEmitted",
            "factBytesEmitted",
        ]
        .iter()
        .map(|k| ((*k).to_owned(), 100u64)),
    );
    let key = |c: char| RequestedKey {
        relation: "calls".to_owned(),
        resolution: "syntactic-callee-name".to_owned(),
        source_universe_id: sha('5'),
        target_universe_id: sha('6'),
        subject_scope_commitment: sha(c),
    };
    let stage = |id: &str, ordinal: u64, c: char| StageBinding {
        expected_stage_id: id.to_owned(),
        stage_ordinal: ordinal,
        relations: vec!["calls".to_owned()],
        budget: budget.clone(),
        keys: vec![key(c)],
    };
    DispatchContext {
        capabilities: tokens.iter().map(|s| (*s).to_owned()).collect(),
        identity_versions: BTreeMap::from_iter([
            ("coverage".to_owned(), 3),
            ("fact".to_owned(), 2),
            ("plan".to_owned(), 2),
            ("snapshot".to_owned(), 2),
        ]),
        expected_provider_descriptor_sha256: h('3'),
        expected_runtime_descriptor_sha256: h('4'),
        provider_descriptor: provider,
        runtime_descriptor: runtime,
        execution_id: EXEC.to_owned(),
        snapshot_id: format!("snapshot2:{}", h('7')),
        plan_id: format!("plan2:{}", h('8')),
        universe_key: sha('5'),
        native_context_id: sha('9'),
        manifest_files: BTreeMap::from_iter([(PATH.to_owned(), (h('a'), 100))]),
        manifest_sha256: h('b'),
        entry_count: 1,
        total_file_bytes: 100,
        total_chunk_count: 1,
        stages: vec![stage("stage-one", 0, 'c'), stage("stage-two", 1, 'd')],
        target_domain: BTreeSet::from_iter([sha('6')]),
        symbol_census: None,
    }
}
fn context_of(p: &Ts2Plan, r: &Ts2Request) -> DispatchContext {
    let mut c = context(&TOKENS);
    let text = |v: &Value| match v {
        Value::Text(s) => s.clone(),
        _ => panic!("text"),
    };
    let number = |v: &Value| match v {
        Value::Unsigned(n) => *n,
        _ => panic!("uint"),
    };
    c.execution_id = p.execution_id.clone();
    c.snapshot_id = p.snapshot_id.clone();
    c.plan_id = p.plan_id.clone();
    c.capabilities = p.capabilities.clone();
    c.symbol_census = p.symbol_census.clone();
    c.universe_key = text(get(r.open_universe(), "universeKey"));
    c.manifest_sha256 = text(get(r.manifest(), "manifestSha256"));
    c.manifest_files = p
        .entries
        .iter()
        .filter_map(|e| match e {
            SnapshotEntry::File {
                path,
                byte_length,
                content_sha256,
            } => Some((path.clone(), (content_sha256.clone(), *byte_length))),
            SnapshotEntry::Symlink { .. } => None,
        })
        .collect();
    c.entry_count = number(get(r.seal(), "entryCount"));
    c.total_file_bytes = number(get(r.seal(), "totalFileBytes"));
    c.total_chunk_count = number(get(r.seal(), "totalChunkCount"));
    c.stages = p
        .stages
        .iter()
        .enumerate()
        .map(|(i, s)| StageBinding {
            expected_stage_id: s.stage_id.clone(),
            stage_ordinal: i as u64,
            relations: s.relations.clone(),
            budget: match get(stage(r, i), "budget") {
                Value::Map(b) => b.iter().map(|(k, v)| (k.clone(), number(v))).collect(),
                _ => unreachable!(),
            },
            keys: s.keys.clone(),
        })
        .collect();
    c
}
pub(super) struct Input {
    pub provider: Provider,
    pub provider_fields: DescriptorFields,
    pub runtime_fields: DescriptorFields,
    pub provider_digest: String,
    pub runtime_digest: String,
    pub capabilities: Vec<String>,
}
pub(super) fn typescript() -> Input {
    let plan = plan();
    let request = Ts2Request::build(&plan).unwrap();
    let context = context_of(&plan, &request);
    Input {
        provider: Provider::TypeScript {
            sender: Ts2Sender::new(request),
            context,
        },
        provider_fields: descriptors::provider(),
        runtime_fields: descriptors::runtime(),
        provider_digest: h('3'),
        runtime_digest: h('4'),
        capabilities: TOKENS.iter().map(|s| (*s).into()).collect(),
    }
}
